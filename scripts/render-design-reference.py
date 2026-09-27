#!/usr/bin/env python3
"""Render the design reference: every component preview of docs/design/ as PNG.

The design contract (standards/design-contract.md, operator decisions
2026-09-27) makes each component spec under docs/design/components/ the
source a WPF control implements 1:1, and review-todo-section approves a
control's golden PNG only after comparing its first WPF render against the
design's own render. This script produces that design side: each
components/<Comp>/preview.html, with tokens.css, bundle.css, and bundle.js
injected exactly as the design page (scripts/build-design-site.py) injects
them, rendered by headless Microsoft Edge for every theme (dark, darkest,
medium, light) and density (compact, comfortable) with the Blue Highlight at
1x, into

    build/design-reference/<Comp>/<theme>-<density>.png      (gitignored)

plus build/design-reference/report.html, a side-by-side page that pairs each
reference with the WPF render of the same component, theme, and density when
one exists (docs/captures/golden/<area>/<Comp>/card-<theme>-<density>@1x.png,
an approved golden, else build/wpf-renders/<Comp>/card-<theme>-<density>@1x.png,
the visual-test output of D01 T01 §9).

Edge is driven over the DevTools protocol with the small stdlib WebSocket
client below: no Node, no Playwright, no pip install. This is the review
aid, not the gate: CI runs it as an optional step on the Windows runner,
which ships Edge.

Usage:
  python scripts/render-design-reference.py                     # everything
  python scripts/render-design-reference.py --components Button,Checkbox --themes dark,light
  python scripts/render-design-reference.py --no-render          # write the HTML and the report only
  python scripts/render-design-reference.py --edge "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
"""
from __future__ import annotations

import argparse
import base64
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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "design-reference"
THEMES = ["dark", "darkest", "medium", "light"]
DENSITIES = ["compact", "comfortable"]
EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


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
                        + "<style>html,body{margin:0}body{padding:16px;width:max-content;background:var(--surface-panel)}</style>")
                src = c["html"]
                src = _sub_once(src, r"<html([^>]*)>", lambda m: "<html" + _strip_theme(m.group(1)) + f' data-theme="{theme}">')
                src = _sub_once(src, r"<head[^>]*>", lambda m: m.group(0) + head)
                src = _sub_once(src, r"<body[^>]*>", lambda m: m.group(0) + "<script>window.__phApply && __phApply();</script>")
                yield c["id"], theme, density, src, c["width"]


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


class Edge:
    """Headless Edge with one page, driven over CDP."""

    def __init__(self, exe: str):
        self.profile = tempfile.mkdtemp(prefix="isotone-design-ref-")
        self.proc = subprocess.Popen(
            [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
             "--no-default-browser-check", "--force-device-scale-factor=1", "--remote-debugging-port=0",
             f"--user-data-dir={self.profile}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        port_file = Path(self.profile) / "DevToolsActivePort"
        deadline = time.time() + 30
        while not port_file.exists() or not port_file.read_text().strip():
            # The msedge.exe launcher may hand off to a broker process and
            # exit 0, so its exit is no failure; only the deadline is.
            if time.time() > deadline:
                raise RuntimeError("Edge did not open its DevTools port within 30 s")
            time.sleep(0.1)
        port = int(port_file.read_text().split()[0])
        targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=10).read())
        page = next(t for t in targets if t.get("type") == "page")
        self.ws = WebSocket(page["webSocketDebuggerUrl"])
        self.next_id = 0
        self.call("Page.enable")

    def call(self, method: str, **params):
        self.next_id += 1
        mid = self.next_id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def evaluate(self, expr: str):
        res = self.call("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        return res.get("result", {}).get("value")

    def shoot(self, url: str, width: int, out: Path) -> tuple[int, int]:
        self.call("Emulation.setDeviceMetricsOverride", width=width, height=800, deviceScaleFactor=1, mobile=False)
        self.call("Page.navigate", url=url)
        deadline = time.time() + 30
        while self.evaluate("document.readyState") != "complete":
            if time.time() > deadline:
                raise RuntimeError(f"{url} did not finish loading")
            time.sleep(0.05)
        self.evaluate("document.fonts.ready.then(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))")
        size = self.evaluate(
            "(() => { const b = document.body; let w = 0, h = 0;"
            " (function walk(el){ for (let c = el.firstElementChild; c; c = c.nextElementSibling) {"
            "   const r = c.getBoundingClientRect(); if (!r.width && !r.height) continue;"
            "   const ov = getComputedStyle(c).overflowX;"
            "   const right = ov === 'visible' ? Math.max(r.right, r.left + c.scrollWidth) : r.right;"
            "   if (right > w) w = right; if (r.bottom > h) h = r.bottom; if (ov === 'visible') walk(c); } })(b);"
            " const cs = getComputedStyle(b);"
            " return [Math.ceil(w + (parseFloat(cs.paddingRight) || 0)), Math.ceil(h + (parseFloat(cs.paddingBottom) || 0))]; })()"
        ) or [width, 800]
        w, h = max(1, min(int(size[0]), 1600)), max(1, min(int(size[1]), 4000))
        self.call("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=False)
        shot = self.call("Page.captureScreenshot", format="png", clip={"x": 0, "y": 0, "width": w, "height": h, "scale": 1},
                         captureBeyondViewport=True)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(shot["data"]))
        return w, h

    def close(self) -> None:
        try:
            self.call("Browser.close")
        except Exception:
            pass
        self.ws.close()
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


def find_edge(explicit: str | None) -> str | None:
    if explicit:
        return explicit if Path(explicit).exists() else None
    for c in EDGE_CANDIDATES:
        if Path(c).exists():
            return c
    return shutil.which("msedge")


# ---------------------------------------------------------------- report

def wpf_render_for(comp: str, theme: str, density: str) -> Path | None:
    # The visual harness lays every state out like the preview card as
    # card-<theme>-<density>@1x.png (standards/design-contract.md, Goldens).
    name = f"card-{theme}-{density}@1x.png"
    golden_root = ROOT / "docs" / "captures" / "golden"
    if golden_root.exists():
        for p in sorted(golden_root.rglob(name)):
            if p.parent.name == comp:
                return p
    p = ROOT / "build" / "wpf-renders" / comp / name
    return p if p.exists() else None


def write_report(rows: list[tuple[str, str, str, Path | None]]) -> Path:
    """build/design-reference/report.html: reference beside WPF render."""
    OUT.mkdir(parents=True, exist_ok=True)
    parts = []
    comps = sorted({r[0] for r in rows})
    for comp in comps:
        parts.append(f'<section id="{html.escape(comp)}"><h2>{html.escape(comp)}</h2>'
                     f'<p class="spec">Spec: <code>docs/design/components/{html.escape(comp)}/README.md</code></p>')
        for c, theme, density, ref in rows:
            if c != comp:
                continue
            wpf = wpf_render_for(comp, theme, density)
            ref_html = (f'<img src="{html.escape(os.path.relpath(ref, OUT).replace(os.sep, "/"))}" alt="design reference">'
                        if ref and ref.exists() else '<p class="none">not rendered</p>')
            if wpf:
                wpf_html = (f'<img src="{html.escape(os.path.relpath(wpf, OUT).replace(os.sep, "/"))}" alt="WPF render">'
                            f'<p class="src">{html.escape(wpf.relative_to(ROOT).as_posix())}</p>')
            else:
                wpf_html = '<p class="none">no WPF render yet (tests/Isotone.UI.VisualTests writes build/wpf-renders/)</p>'
            parts.append(f'<div class="pair"><h3>{theme} / {density}</h3><div class="cols">'
                         f'<figure><figcaption>Design reference</figcaption>{ref_html}</figure>'
                         f'<figure><figcaption>WPF</figcaption>{wpf_html}</figure></div></div>')
        parts.append("</section>")
    nav = "".join(f'<a href="#{html.escape(c)}">{html.escape(c)}</a>' for c in comps)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Design reference vs WPF</title>
<style>
body{{font:13px/1.4 "Segoe UI Variable Text","Segoe UI",system-ui,sans-serif;margin:0;background:#1e1e1e;color:#e3e3e3}}
nav{{position:sticky;top:0;background:#282828;padding:8px 16px;display:flex;flex-wrap:wrap;gap:4px 12px;border-bottom:1px solid #3a3a3a}}
nav a{{color:#8ab4f8;text-decoration:none}} main{{padding:16px}} h2{{margin:24px 0 4px}} h3{{margin:12px 0 4px;font-size:13px;color:#b0b0b0}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} figure{{margin:0;background:#282828;padding:8px;border:1px solid #3a3a3a;overflow:auto}}
figcaption{{font-size:11px;color:#9a9a9a;margin-bottom:4px}} img{{image-rendering:pixelated;max-width:none}} .none,.src,.spec{{color:#9a9a9a}}
</style></head><body>
<nav>{nav}</nav><main>
<p>Generated by <code>scripts/render-design-reference.py</code>. Left: the design's own render of each component preview (docs/design is the source).
Right: the WPF render of the same component, theme, and density (an approved golden under <code>docs/captures/golden/</code>, else <code>build/wpf-renders/</code>).
Review compares them per <code>standards/design-contract.md</code>: exact tokens, geometry within 1 DIP, every state present.</p>
{"".join(parts)}
</main></body></html>
"""
    out = OUT / "report.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--components", help="comma-separated component ids (default: all)")
    ap.add_argument("--themes", default=",".join(THEMES))
    ap.add_argument("--densities", default=",".join(DENSITIES))
    ap.add_argument("--highlight", default="blue", choices=["blue", "orange", "windows"])
    ap.add_argument("--edge", help="path to msedge.exe")
    ap.add_argument("--no-render", action="store_true", help="write the HTML documents and the report only")
    args = ap.parse_args(argv)
    comps = [c.strip() for c in args.components.split(",")] if args.components else None
    themes = [t.strip() for t in args.themes.split(",") if t.strip()]
    densities = [d.strip() for d in args.densities.split(",") if d.strip()]
    bad = [t for t in themes if t not in THEMES] + [d for d in densities if d not in DENSITIES]
    if bad:
        print(f"render-design-reference: unknown theme or density {bad}")
        return 2
    site = site_module()
    docs = list(build_documents(site, comps, themes, densities, args.highlight))
    if not docs:
        print("render-design-reference: no component matched")
        return 2
    html_dir = OUT / "_html"
    rows: list[tuple[str, str, str, Path | None]] = []
    edge = None
    if not args.no_render:
        exe = find_edge(args.edge)
        if not exe:
            print("render-design-reference: Microsoft Edge not found; pass --edge, or --no-render for the HTML only")
            return 2
        edge = Edge(exe)
    failures = 0
    try:
        for comp, theme, density, src, width in docs:
            doc = html_dir / comp / f"{theme}-{density}.html"
            doc.parent.mkdir(parents=True, exist_ok=True)
            doc.write_text(src, encoding="utf-8", newline="\n")
            png = OUT / comp / f"{theme}-{density}.png"
            if edge is not None:
                try:
                    w, h = edge.shoot(doc.resolve().as_uri(), max(width or 0, 1200), png)
                    print(f"{comp}/{theme}-{density}.png {w}x{h}")
                except Exception as e:  # one broken preview never hides the rest
                    failures += 1
                    print(f"render-design-reference: {comp} {theme} {density}: {e}")
            rows.append((comp, theme, density, png if png.exists() else None))
    finally:
        if edge is not None:
            edge.close()
    report = write_report(rows)
    print(f"render-design-reference: {len(rows)} reference(s), {failures} failure(s); report {report.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
