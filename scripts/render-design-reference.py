#!/usr/bin/env python3
"""Render the design reference: every component preview of docs/design/ as PNG.

The design contract (standards/design-contract.md, operator decisions
2026-09-27) makes each component spec under docs/design/components/ the
source a native isotone::ui control implements 1:1, and review-todo-section approves a
control's golden PNG only after comparing its first native UI render against the
design's own render. This script produces that design side: each
components/<Comp>/preview.html, with tokens.css, bundle.css, and bundle.js
injected exactly as the design page (scripts/build-design-site.py) injects
them, rendered by headless Microsoft Edge for every theme (dark, darkest,
medium, light) and density (compact, comfortable) with the Blue Highlight at
1x, into

    build/design-reference/<Comp>/<theme>-<density>.png      (gitignored)

plus build/design-reference/report.html, a side-by-side page that pairs each
reference with the native UI render of the same component, theme, and density when
one exists (docs/captures/golden/<area>/<Comp>/card-<theme>-<density>@1x.png,
an approved golden, else build/ui-renders/<Comp>/card-<theme>-<density>@1x.png,
the visual-test output planned in D00 T07 §3).

Edge is driven over the DevTools protocol with the small stdlib WebSocket
client below: no Node, no Playwright, no pip install. This is the review
aid, not the gate: CI runs it as an optional step on the Windows runner,
which ships Edge.

What a run proves, and records in build/design-reference/manifest.json: each
render's page carried the theme and density asked for (read back from the
page, not assumed), its background resolved to a color, the capture was not
cut at the size cap, and the picture is not blank; within one component the
themes are different pictures. A preview is laid out as the design page lays
it out: at its card's declared width when it has one, shrink-wrapped to its
content when it has none, and at the page's column width when it has no width
of its own (a surface that fills its card). The report is self-contained: the golden or
UI render it pairs with is copied under build/design-reference/_compare/, so
the uploaded artifact opens anywhere. `--verify <dir>` re-checks a directory
(a local run, or a downloaded `design-reference` artifact) against the
manifest and against the set docs/design/ says must exist.

The browser is owned: it starts inside a job object (a process group off
Windows), and every way out, a failed start, a render timeout, or a normal
close, ends the whole process tree and removes the temporary profile.

Usage:
  python scripts/render-design-reference.py                     # everything
  python scripts/render-design-reference.py --components Button,Checkbox --themes dark,light
  python scripts/render-design-reference.py --no-render          # write the HTML and the report only
  python scripts/render-design-reference.py --edge "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
  python scripts/render-design-reference.py --verify build/design-reference   # re-check a run or a downloaded artifact
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import importlib.util
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "design-reference"
THEMES = ["dark", "darkest", "medium", "light"]
DENSITIES = ["compact", "comfortable"]
EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
MAX_WIDTH, MAX_HEIGHT = 1600, 4000  # the capture's size cap; a render that reaches it is reported as clipped
CALL_TIMEOUT = 60.0  # seconds one DevTools command may take
BODY_PADDING = 16  # the margin the reference keeps around a preview, in px on every side
# The width of a card on the design page when its preview declares none: the page column (`.s-main`, 1180px wide
# with 32px of padding on each side, in scripts/build-design-site.py). A preview with no width of its own (a
# surface that fills its card, such as the Canvas) is laid out at this width, as the page lays it out.
COLUMN_WIDTH = 1180 - 2 * 32


def site_module():
    spec = importlib.util.spec_from_file_location("build_design_site", ROOT / "scripts" / "build-design-site.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def build_documents(site, comps: list[str] | None, themes: list[str], densities: list[str], highlight: str):
    """Yield (component id, theme, density, html, card width) for every combination."""
    tj = json.loads(site.read_text(site.DESIGN / "tokens.json"))
    site.COLOR_NAMES.clear()
    site.COLOR_NAMES.update(t["name"] for t in tj["color"]["tokens"])
    tokens_css = site.build_tokens_css(tj)
    css = site.read_text(site.COMPONENTS / "bundle.css")
    js = site.read_text(site.COMPONENTS / "bundle.js")
    for c in site.load_components(site.blob_map()):
        if comps is not None and c["id"] not in comps:
            continue
        for theme in themes:
            for density in densities:
                state = {"theme": theme, "highlight": highlight, "density": density, "lockhl": c["lockhl"]}
                head = ("<style>" + tokens_css + "\n" + css + "</style><script>" + js + "</script><script>"
                        + site.BRIDGE.replace("__STATE__", json.dumps(state)) + "</script>"
                        + "<style>html,body{margin:0}body{box-sizing:border-box;padding:" + str(BODY_PADDING) + "px;width:" + body_width(c["width"])
                        + ";background:var(--surface-panel)}</style>")
                src = c["html"]
                src = _sub_once(src, r"<html([^>]*)>", lambda m: "<html" + _strip_theme(m.group(1)) + f' data-theme="{theme}">')
                src = _sub_once(src, r"<head[^>]*>", lambda m: m.group(0) + head)
                src = _sub_once(src, r"<body[^>]*>", lambda m: m.group(0) + "<script>window.__phApply && __phApply();</script>")
                yield c["id"], theme, density, src, c["width"]


def body_width(card_width) -> str:
    """The CSS width of the preview's body, a border box: a card that declares its width is laid out at it, as
    the design page shows it (its content wraps there); one that declares none is shrink-wrapped."""
    if card_width:
        return f"{int(card_width)}px"
    return "max-content"


def _sub_once(src: str, pattern: str, fn) -> str:
    import re
    return re.sub(pattern, fn, src, count=1, flags=re.I)


def _strip_theme(attrs: str) -> str:
    import re
    return re.sub(r'\sdata-theme="[^"]*"', "", attrs)


# ---------------------------------------------------------------- a minimal WebSocket client (RFC 6455)

class WebSocket:
    def __init__(self, url: str, timeout: float = 60.0):
        assert url.startswith("ws://")
        rest = url[5:]
        hostport, _, path = rest.partition("/")
        host, _, port = hostport.partition(":")
        self.sock = socket.create_connection((host, int(port or 80)), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
               f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
        self.sock.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("websocket handshake closed")
            buf += chunk
        head, _, self.pending = buf.partition(b"\r\n\r\n")
        if b" 101 " not in head.split(b"\r\n", 1)[0]:
            raise ConnectionError(f"websocket handshake refused: {head[:80]!r}")

    def _recv_exact(self, n: int) -> bytes:
        while len(self.pending) < n:
            chunk = self.sock.recv(max(65536, n - len(self.pending)))
            if not chunk:
                raise ConnectionError("websocket closed")
            self.pending += chunk
        out, self.pending = self.pending[:n], self.pending[n:]
        return out

    def send(self, text: str) -> None:
        data = text.encode("utf-8")
        header = bytearray([0x81])
        n = len(data)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        mask = os.urandom(4)
        header += mask
        self.sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self) -> str:
        message = b""
        while True:
            b0, b1 = self._recv_exact(2)
            opcode, fin = b0 & 0x0F, b0 & 0x80
            n = b1 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._recv_exact(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._recv_exact(8))[0]
            mask = self._recv_exact(4) if b1 & 0x80 else None
            payload = self._recv_exact(n)
            if mask:
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
            if opcode == 0x8:
                raise ConnectionError("websocket closed by peer")
            if opcode == 0x9:  # ping: answer and keep reading
                continue
            message += payload
            if fin:
                return message.decode("utf-8")

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass


# The natural size of the laid-out preview: the right and bottom edges of its content, walking into every box that
# lets its content show and not into boxes that clip or scroll theirs, plus the body's padding.
MEASURE = (
    "(() => { const b = document.body; let w = 0, h = 0;"
    " (function walk(el){ for (let c = el.firstElementChild; c; c = c.nextElementSibling) {"
    "   const r = c.getBoundingClientRect(); if (!r.width && !r.height) continue;"
    "   const ov = getComputedStyle(c).overflowX;"
    "   const right = ov === 'visible' ? Math.max(r.right, r.left + c.scrollWidth) : r.right;"
    "   if (right > w) w = right; if (r.bottom > h) h = r.bottom; if (ov === 'visible') walk(c); } })(b);"
    " const cs = getComputedStyle(b);"
    " return [Math.ceil(w + (parseFloat(cs.paddingRight) || 0)), Math.ceil(h + (parseFloat(cs.paddingBottom) || 0))]; })()"
)


class ProcessTree:
    """Owns a child process and everything it starts, so nothing outlives the run.

    On Windows the child is put in a job object set to kill on close: children it starts join the job even after
    the launcher exits (msedge.exe hands off to a browser process and exits 0), and ending the job ends them all.
    Elsewhere the child leads a new session and the whole process group is signalled.
    """

    def __init__(self, argv: list[str]):
        self.job = None
        if os.name == "nt":
            self.proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                self.job = _job_for(int(self.proc._handle))
            except Exception:
                self.proc.kill()
                raise
        else:
            self.proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                         start_new_session=True)

    def end(self) -> None:
        """End the whole tree. Safe to call twice."""
        if os.name == "nt":
            if self.job is not None:
                _kernel32().TerminateJobObject(self.job, 1)
                _kernel32().CloseHandle(self.job)
                self.job = None
        else:
            import signal
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass  # every process of the group has already exited, which is the state wanted
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def _kernel32():
    import ctypes
    from ctypes import wintypes
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateJobObjectW.restype = wintypes.HANDLE
    k.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    k.SetInformationJobObject.restype = wintypes.BOOL
    k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
    k.AssignProcessToJobObject.restype = wintypes.BOOL
    k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    k.TerminateJobObject.restype = wintypes.BOOL
    k.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    k.CloseHandle.restype = wintypes.BOOL
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    return k


def _job_for(process_handle: int):
    """A job object that kills its processes when closed, holding the given process."""
    import ctypes
    from ctypes import wintypes

    class BasicLimits(ctypes.Structure):
        _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                    ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                    ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD),
                    ("SchedulingClass", wintypes.DWORD)]

    class IoCounters(ctypes.Structure):
        _fields_ = [(name, ctypes.c_uint64) for name in ("ReadOperationCount", "WriteOperationCount",
                                                         "OtherOperationCount", "ReadTransferCount",
                                                         "WriteTransferCount", "OtherTransferCount")]

    class ExtendedLimits(ctypes.Structure):
        _fields_ = [("BasicLimitInformation", BasicLimits), ("IoInfo", IoCounters),
                    ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                    ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

    k = _kernel32()
    job = k.CreateJobObjectW(None, None)
    if not job:
        raise OSError(ctypes.get_last_error(), "CreateJobObjectW failed")
    info = ExtendedLimits()
    info.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    ok = (k.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))  # JobObjectExtendedLimitInformation
          and k.AssignProcessToJobObject(job, process_handle))
    if not ok:
        error = ctypes.get_last_error()
        k.CloseHandle(job)
        raise OSError(error, "the browser could not be placed in a job object")
    return job


class Edge:
    """Headless Edge with one page, driven over CDP, and owned: whatever happens, `close` ends its process tree
    and removes its profile, and a start that fails closes itself before raising."""

    def __init__(self, exe: str, launch: list[str] | None = None, startup_timeout: float = 30.0):
        self.ws = None
        self.tree = None
        self.profile = tempfile.mkdtemp(prefix="isotone-design-ref-")
        try:
            # `launch` replaces the browser command (the tests pass a stand-in that never opens a port).
            self.tree = ProcessTree(launch if launch is not None else [
                exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                "--no-default-browser-check", "--force-device-scale-factor=1", "--remote-debugging-port=0",
                # A page the browser takes for a background one has its timers and frames throttled, and a
                # render waiting on a frame then never answers: switch the throttling off.
                "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                f"--user-data-dir={self.profile}", "about:blank"])
            port_file = Path(self.profile) / "DevToolsActivePort"
            deadline = time.time() + startup_timeout
            while not port_file.exists() or not port_file.read_text().strip():
                # The msedge.exe launcher may hand off to a broker process and
                # exit 0, so its exit is no failure; only the deadline is.
                if time.time() > deadline:
                    raise RuntimeError(f"Edge did not open its DevTools port within {startup_timeout:g} s")
                time.sleep(0.1)
            port = int(port_file.read_text().split()[0])
            targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=10).read())
            page = next(t for t in targets if t.get("type") == "page")
            self.ws = WebSocket(page["webSocketDebuggerUrl"])
            self.next_id = 0
            self.call("Page.enable")
        except BaseException as error:
            left = self.close()
            if left:
                raise RuntimeError(f"{error}; and {'; '.join(left)}") from error
            raise

    def call(self, method: str, **params):
        """One DevTools command and its answer, bounded: the socket times out when the browser is silent, and the
        deadline ends the wait when it keeps talking without answering."""
        self.next_id += 1
        mid = self.next_id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        deadline = time.time() + CALL_TIMEOUT
        while True:
            if time.time() > deadline:
                raise TimeoutError(f"{method} was not answered within {CALL_TIMEOUT:g} s")
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def evaluate(self, expr: str):
        res = self.call("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        return res.get("result", {}).get("value")

    def shoot(self, url: str, width: int, out: Path) -> dict:
        """Render `url` to `out` and return what the page and the picture say: the size, whether the size cap cut
        it, the theme and density the page carries, its background, and how many colors a thumbnail holds."""
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=800, deviceScaleFactor=1, mobile=False)
        self.call("Page.navigate", url=url)
        deadline = time.time() + 30
        while self.evaluate("document.readyState") != "complete":
            if time.time() > deadline:
                raise RuntimeError(f"{url} did not finish loading")
            time.sleep(0.05)
        # Fonts loaded and two frames painted, or two seconds, whichever comes first: a frame that never comes
        # must not hold the render (the screenshot forces its own frame).
        self.evaluate("Promise.race([document.fonts.ready.then(() => new Promise(r => requestAnimationFrame(() => "
                      "requestAnimationFrame(r)))), new Promise(r => setTimeout(r, 2000))])")
        size = self.evaluate(MEASURE) or [width, 800]
        natural_w, natural_h = max(1, int(size[0])), max(1, int(size[1]))
        fluid = natural_w <= 2 * BODY_PADDING
        if fluid:
            # Shrink-wrapped, the preview has no width at all: it fills whatever holds it. Lay it out at the
            # design page's column width, as the page does, and measure again.
            self.evaluate(f"document.body.style.width = '{COLUMN_WIDTH}px'")
            size = self.evaluate(MEASURE) or [COLUMN_WIDTH, natural_h]
            natural_w, natural_h = max(1, int(size[0])), max(1, int(size[1]))
        w, h = min(natural_w, MAX_WIDTH), min(natural_h, MAX_HEIGHT)
        self.call("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=False)
        page = self.evaluate(
            "(() => ({theme: document.documentElement.getAttribute('data-theme'),"
            " comfortable: document.body.classList.contains('ph-comfortable'),"
            " background: getComputedStyle(document.body).backgroundColor}))()") or {}
        clip = {"x": 0, "y": 0, "width": w, "height": h, "scale": 1}
        shot = self.call("Page.captureScreenshot", format="png", clip=clip, captureBeyondViewport=True)
        thumb = self.call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                          clip=dict(clip, scale=min(1.0, 240.0 / max(w, h))))
        out.parent.mkdir(parents=True, exist_ok=True)
        data = base64.b64decode(shot["data"])
        out.write_bytes(data)
        return {"width": w, "height": h, "natural_width": natural_w, "natural_height": natural_h, "fluid": fluid,
                "clipped": natural_w > MAX_WIDTH or natural_h > MAX_HEIGHT,
                "theme_attr": page.get("theme"), "comfortable": bool(page.get("comfortable")),
                "background": page.get("background") or "", "colors": png_colors(base64.b64decode(thumb["data"])),
                "sha256": hashlib.sha256(data).hexdigest()}

    def close(self) -> list[str]:
        """End the browser and remove its profile; safe to call twice. Teardown runs to the end whatever fails,
        and returns what it could not clean up (an empty list when nothing is left behind), which the caller
        reports as a failure of the run."""
        left: list[str] = []
        if self.ws is not None:
            try:
                self.call("Browser.close")  # a polite close; the tree is ended below whether or not it answers
            except (OSError, RuntimeError, ValueError):
                pass
            try:
                self.ws.close()
            except OSError:
                pass
            self.ws = None
        if self.tree is not None:
            try:
                self.tree.end()
            except OSError as error:
                left.append(f"the browser's process tree could not be ended ({error})")
            self.tree = None
        for _ in range(50):  # the profile's files unlock a moment after the last process ends
            shutil.rmtree(self.profile, ignore_errors=True)
            if not os.path.exists(self.profile):
                break
            time.sleep(0.1)
        else:
            left.append(f"the browser's profile {self.profile} could not be removed, so one of its processes may "
                        f"still be running")
        return left


# ---------------------------------------------------------------- what a render shows

def png_size(data: bytes) -> tuple[int, int] | None:
    """(width, height) of a PNG, or None when the bytes are not one."""
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", data[16:24])


def png_colors(data: bytes, limit: int = 64) -> int:
    """How many distinct colors a small 8-bit RGB or RGBA PNG holds, counted up to `limit`; 0 when it cannot be
    read. One color is a blank picture."""
    if png_size(data) is None:
        return 0
    width, height = png_size(data)
    depth, color_type, _c, _f, interlace = struct.unpack(">BBBBB", data[24:29])
    channels = {2: 3, 6: 4}.get(color_type)
    if depth != 8 or channels is None or interlace != 0:
        return 0
    idat, pos = b"", 8
    while pos + 8 <= len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        if kind == b"IDAT":
            idat += data[pos + 8:pos + 8 + length]
        pos += 12 + length
    try:
        raw = zlib.decompress(idat)
    except zlib.error:
        return 0
    stride = width * channels
    if len(raw) < (stride + 1) * height:
        return 0
    seen: set[bytes] = set()
    prev = bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        kind, row = raw[start], bytearray(raw[start + 1:start + 1 + stride])
        for x in range(stride):
            left = row[x - channels] if x >= channels else 0
            up = prev[x]
            if kind == 1:
                row[x] = (row[x] + left) & 255
            elif kind == 2:
                row[x] = (row[x] + up) & 255
            elif kind == 3:
                row[x] = (row[x] + ((left + up) >> 1)) & 255
            elif kind == 4:
                corner = prev[x - channels] if x >= channels else 0
                estimate = left + up - corner
                dl, du, dc = abs(estimate - left), abs(estimate - up), abs(estimate - corner)
                row[x] = (row[x] + (left if dl <= du and dl <= dc else up if du <= dc else corner)) & 255
        for x in range(0, stride, channels):
            seen.add(bytes(row[x:x + 3]))
            if len(seen) >= limit:
                return limit
        prev = row
    return len(seen)


def render_problems(entry: dict) -> list[str]:
    """What is wrong with one render, from what its page and its picture reported."""
    problems = []
    if entry.get("theme_attr") != entry["theme"]:
        problems.append(f"the page carries theme {entry.get('theme_attr')!r}, not {entry['theme']!r}")
    if bool(entry.get("comfortable")) != (entry["density"] == "comfortable"):
        problems.append(f"the page is {'comfortable' if entry.get('comfortable') else 'compact'}, not {entry['density']}")
    if entry.get("background", "") in ("", "transparent", "rgba(0, 0, 0, 0)"):
        problems.append("the page background did not resolve to a color (the tokens were not applied)")
    if entry.get("clipped"):
        problems.append(f"the content is larger than the {MAX_WIDTH} x {MAX_HEIGHT} capture and was cut")
    if entry.get("colors", 0) < 2:
        problems.append("the picture is blank (one color)")
    return problems


def set_problems(entries: list[dict]) -> list[str]:
    """What is wrong across renders: two themes of one component and density that are the same picture."""
    problems = []
    by: dict[tuple[str, str], dict[str, list[str]]] = {}
    for e in entries:
        if e.get("sha256"):
            by.setdefault((e["comp"], e["density"]), {}).setdefault(e["sha256"], []).append(e["theme"])
    for (comp, density), hashes in sorted(by.items()):
        for themes in hashes.values():
            if len(themes) > 1:
                problems.append(f"{comp} {density}: themes {', '.join(sorted(themes))} are the same picture")
    return problems


def find_edge(explicit: str | None) -> str | None:
    if explicit:
        return explicit if Path(explicit).exists() else None
    for c in EDGE_CANDIDATES:
        if Path(c).exists():
            return c
    return shutil.which("msedge")


# ---------------------------------------------------------------- report

def ui_render_for(comp: str, theme: str, density: str) -> tuple[str, Path] | None:
    """("golden" | "ui-render", path) of the native render to pair with a reference: the approved golden when one
    exists, else the UI render the visual harness wrote, else None."""
    # The visual harness lays every state out like the preview card as
    # card-<theme>-<density>@1x.png (standards/design-contract.md, Goldens).
    name = f"card-{theme}-{density}@1x.png"
    golden_root = ROOT / "docs" / "captures" / "golden"
    if golden_root.exists():
        for p in sorted(golden_root.rglob(name)):
            if p.parent.name == comp:
                return "golden", p
    p = ROOT / "build" / "ui-renders" / comp / name
    return ("ui-render", p) if p.exists() else None


def write_report(rows: list[tuple[str, str, str, Path | None]]) -> Path:
    """build/design-reference/report.html: reference beside native UI render.

    Self-contained: each native render is copied to `_compare/<Comp>/<kind>-<name>` inside the output folder and
    linked from there, so the folder opens the same after it is uploaded, downloaded, and extracted elsewhere.
    """
    OUT.mkdir(parents=True, exist_ok=True)
    compare = OUT / "_compare"
    shutil.rmtree(compare, ignore_errors=True)
    parts = []
    comps = sorted({r[0] for r in rows})
    for comp in comps:
        parts.append(f'<section id="{html.escape(comp)}"><h2>{html.escape(comp)}</h2>'
                     f'<p class="spec">Spec: <code>docs/design/components/{html.escape(comp)}/README.md</code></p>')
        for c, theme, density, ref in rows:
            if c != comp:
                continue
            ui = ui_render_for(comp, theme, density)
            ref_html = (f'<img src="{html.escape(ref.relative_to(OUT).as_posix())}" alt="design reference">'
                        if ref and ref.exists() else '<p class="none">not rendered</p>')
            if ui:
                kind, source = ui
                copy = compare / comp / f"{kind}-{source.name}"
                copy.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, copy)
                ui_html = (f'<img src="{html.escape(copy.relative_to(OUT).as_posix())}" alt="native UI render">'
                           f'<p class="src">{"approved golden" if kind == "golden" else "UI render, not yet approved"}: '
                           f'{html.escape(source.relative_to(ROOT).as_posix())}</p>')
            else:
                ui_html = '<p class="none">no native UI render yet (the visual harness writes build/ui-renders/)</p>'
            parts.append(f'<div class="pair"><h3>{theme} / {density}</h3><div class="cols">'
                         f'<figure><figcaption>Design reference</figcaption>{ref_html}</figure>'
                         f'<figure><figcaption>Native UI</figcaption>{ui_html}</figure></div></div>')
        parts.append("</section>")
    nav = "".join(f'<a href="#{html.escape(c)}">{html.escape(c)}</a>' for c in comps)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Design reference vs Native UI</title>
<style>
body{{font:13px/1.4 "Segoe UI Variable Text","Segoe UI",system-ui,sans-serif;margin:0;background:#1e1e1e;color:#e3e3e3}}
nav{{position:sticky;top:0;background:#282828;padding:8px 16px;display:flex;flex-wrap:wrap;gap:4px 12px;border-bottom:1px solid #3a3a3a}}
nav a{{color:#8ab4f8;text-decoration:none}} main{{padding:16px}} h2{{margin:24px 0 4px}} h3{{margin:12px 0 4px;font-size:13px;color:#b0b0b0}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} figure{{margin:0;background:#282828;padding:8px;border:1px solid #3a3a3a;overflow:auto}}
figcaption{{font-size:11px;color:#9a9a9a;margin-bottom:4px}} img{{image-rendering:pixelated;max-width:none}} .none,.src,.spec{{color:#9a9a9a}}
</style></head><body>
<nav>{nav}</nav><main>
<p>Generated by <code>scripts/render-design-reference.py</code>. Left: the design's own render of each component preview (docs/design is the source).
Right: the native UI render of the same component, theme, and density (an approved golden under <code>docs/captures/golden/</code>, else <code>build/ui-renders/</code>), copied beside this page.
Review compares them per <code>standards/design-contract.md</code>: exact tokens, geometry within 1 DIP, every state present.</p>
{"".join(parts)}
</main></body></html>
"""
    out = OUT / "report.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    return out


# ---------------------------------------------------------------- the manifest and its re-check

def expected_set(site, comps: list[str] | None, themes: list[str], densities: list[str]) -> list[tuple[str, str, str]]:
    """Every (component, theme, density) docs/design/ says a run must render."""
    return [(c["id"], theme, density) for c in site.load_components(site.blob_map())
            if comps is None or c["id"] in comps for theme in themes for density in densities]


def verify(folder: Path, expected: list[tuple[str, str, str]]) -> list[str]:
    """Everything wrong with a rendered folder (a local run or a downloaded artifact), read from its manifest and
    its files: a render the set owes that is missing, a file that is not the one the run checked, a render the
    run found wrong, and a report image that does not resolve inside the folder."""
    import re
    manifest_path = folder / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = manifest["renders"]
    except (OSError, ValueError, KeyError) as error:
        return [f"{manifest_path.name} cannot be read ({error.__class__.__name__}); the run did not finish"]
    problems = []
    have = {(e["comp"], e["theme"], e["density"]): e for e in entries}
    for key in expected:
        if key not in have:
            problems.append(f"{key[0]} {key[1]} {key[2]}: not in the manifest")
    for key, entry in sorted(have.items()):
        label = " ".join(key)
        for problem in entry.get("problems", []):
            problems.append(f"{label}: {problem}")
        if "file" not in entry:
            continue  # the run already recorded why there is no picture
        path = folder / entry["file"]
        if not path.is_file():
            problems.append(f"{label}: {entry['file']} is missing")
            continue
        data = path.read_bytes()
        if png_size(data) != (entry.get("width"), entry.get("height")):
            problems.append(f"{label}: {entry['file']} is not a {entry.get('width')} x {entry.get('height')} PNG")
        elif hashlib.sha256(data).hexdigest() != entry.get("sha256"):
            problems.append(f"{label}: {entry['file']} is not the file the run checked (its hash differs)")
        for problem in render_problems(entry):
            if f"{label}: {problem}" not in problems:
                problems.append(f"{label}: {problem}")
    problems += set_problems(entries)
    report = folder / "report.html"
    if not report.is_file():
        problems.append("report.html is missing")
    else:
        for src in re.findall(r'<img src="([^"]+)"', report.read_text(encoding="utf-8")):
            target = (folder / html.unescape(src)).resolve()
            if not target.is_file() or folder.resolve() not in target.parents:
                problems.append(f"report.html links {src}, which does not resolve inside the folder")
    return problems


def render_all(docs, make_browser) -> tuple[list[tuple[str, str, str, Path | None]], list[dict], int]:
    """Write every document and, with a browser factory, render it: (report rows, manifest entries, failures).

    One broken preview never hides the rest, and one stalled browser never holds them: after a render that
    raised, the browser is closed (its whole process tree ended) and a new one started for the next render. A
    browser that cannot be started ends the rendering, with every render still owed recorded as not rendered.
    """
    html_dir = OUT / "_html"
    rows: list[tuple[str, str, str, Path | None]] = []
    entries: list[dict] = []
    failures = 0
    browser = None
    dead = ""  # why no browser can be had any more
    left: list[str] = []
    try:
        for comp, theme, density, src, width in docs:
            doc = html_dir / comp / f"{theme}-{density}.html"
            doc.parent.mkdir(parents=True, exist_ok=True)
            doc.write_text(src, encoding="utf-8", newline="\n")
            png = OUT / comp / f"{theme}-{density}.png"
            entry = {"comp": comp, "theme": theme, "density": density}
            if make_browser is not None:
                png.unlink(missing_ok=True)  # a picture left by an earlier run is never passed off as this one's
                if browser is None and not dead:
                    try:
                        browser = make_browser()
                    except Exception as e:
                        dead = f"the browser could not be started ({e})"
                if browser is None:
                    entry["problems"] = [f"not rendered: {dead}"]
                else:
                    try:
                        entry.update(browser.shoot(doc.resolve().as_uri(), max(width or 0, 1200), png))
                        entry["file"] = png.relative_to(OUT).as_posix()
                        entry["problems"] = render_problems(entry)
                        print(f"{comp}/{theme}-{density}.png {entry['width']}x{entry['height']}", flush=True)
                    except Exception as e:
                        entry["problems"] = [f"not rendered: {e}"]
                        png.unlink(missing_ok=True)
                        left += browser.close()  # its state is unknown: the next render gets a new one
                        browser = None
                for problem in entry["problems"]:
                    failures += 1
                    print(f"render-design-reference: {comp} {theme} {density}: {problem}", flush=True)
                entries.append(entry)
            rows.append((comp, theme, density, png if png.exists() else None))
    finally:
        if browser is not None:
            left += browser.close()
    for problem in left + set_problems(entries):
        failures += 1
        print(f"render-design-reference: {problem}", flush=True)
    return rows, entries, failures


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--components", help="comma-separated component ids (default: all)")
    ap.add_argument("--themes", default=",".join(THEMES))
    ap.add_argument("--densities", default=",".join(DENSITIES))
    ap.add_argument("--highlight", default="blue", choices=["blue", "orange", "windows"])
    ap.add_argument("--edge", help="path to msedge.exe")
    ap.add_argument("--no-render", action="store_true", help="write the HTML documents and the report only")
    ap.add_argument("--verify", metavar="DIR", help="re-check a rendered folder or a downloaded artifact; renders nothing")
    args = ap.parse_args(argv)
    comps = [c.strip() for c in args.components.split(",")] if args.components else None
    themes = [t.strip() for t in args.themes.split(",") if t.strip()]
    densities = [d.strip() for d in args.densities.split(",") if d.strip()]
    bad = [t for t in themes if t not in THEMES] + [d for d in densities if d not in DENSITIES]
    if bad:
        print(f"render-design-reference: unknown theme or density {bad}")
        return 2
    site = site_module()
    if args.verify:
        expected = expected_set(site, comps, themes, densities)
        problems = verify(Path(args.verify), expected)
        for problem in problems:
            print(f"render-design-reference: {problem}")
        print(f"render-design-reference: verified {args.verify}: {len(expected)} render(s) owed, {len(problems)} problem(s)")
        return 1 if problems else 0
    docs = list(build_documents(site, comps, themes, densities, args.highlight))
    if not docs:
        print("render-design-reference: no component matched")
        return 2
    exe = None
    if not args.no_render:
        exe = find_edge(args.edge)
        if not exe:
            print("render-design-reference: Microsoft Edge not found; pass --edge, or --no-render for the HTML only")
            return 2
    rows, entries, failures = render_all(docs, (lambda: Edge(exe)) if exe else None)
    report = write_report(rows)
    if not args.no_render:
        (OUT / "manifest.json").write_text(json.dumps(
            {"highlight": args.highlight, "owed": len(docs), "failures": failures, "renders": entries},
            indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"render-design-reference: {len(rows)} reference(s), {failures} failure(s); report {report.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
