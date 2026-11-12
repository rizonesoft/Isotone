#!/usr/bin/env python3
"""Tests for scripts/render-design-reference.py that need no browser.

What they prove (D00 T01 §9): a browser that never starts is ended with every process it started and its profile
removed; a blank picture, a wrong theme, a wrong density, a clipped capture, and two themes that are one picture
are each named; the report prefers the approved golden, falls back to the UI render, says when there is none, and
still resolves every image after its folder is copied elsewhere; and the re-check of a folder refuses a missing
render, a swapped file, and an incomplete set.

Run: python scripts/tests/test_render_design_reference.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import struct
import sys
import tempfile
import time
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
_spec = importlib.util.spec_from_file_location("render_design_reference", ROOT / "scripts" / "render-design-reference.py")
rdr = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = rdr
_spec.loader.exec_module(rdr)

# A stand-in browser: it starts a child of its own, records both process ids, and never opens a DevTools port.
# Both processes end by themselves after two minutes, so nothing is left behind even if a test is interrupted.
FAKE_BROWSER = """
import os, subprocess, sys, time
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
with open(sys.argv[1], "w") as f:
    f.write(f"{os.getpid()} {child.pid}")
time.sleep(120)
"""


def png(width: int, height: int, color_at) -> bytes:
    """An 8-bit RGB PNG whose pixel (x, y) is color_at(x, y)."""
    raw = b"".join(b"\x00" + b"".join(bytes(color_at(x, y)) for x in range(width)) for y in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def pid_alive(pid: int) -> bool:
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.OpenProcess.restype = wintypes.HANDLE
        k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        handle = k.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code = wintypes.DWORD()
        k.GetExitCodeProcess(handle, ctypes.byref(code))
        k.CloseHandle(handle)
        return code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    # A killed child of this process stays a zombie until reaped; a zombie is not running.
    try:
        return "Z" not in Path(f"/proc/{pid}/stat").read_text().split(")")[-1].split()[0]
    except OSError:
        return True


def entry(**over) -> dict:
    base = {"comp": "Button", "theme": "dark", "density": "compact", "theme_attr": "dark", "comfortable": False,
            "background": "rgb(50, 50, 50)", "clipped": False, "colors": 12}
    base.update(over)
    return base


class BrowserOwnership(unittest.TestCase):
    def test_a_browser_that_never_starts_is_ended_with_its_children_and_its_profile(self):
        with tempfile.TemporaryDirectory() as scratch:
            fake = Path(scratch) / "fake_browser.py"
            fake.write_text(FAKE_BROWSER, encoding="utf-8")
            pids = Path(scratch) / "pids.txt"
            before = set(Path(tempfile.gettempdir()).glob("isotone-design-ref-*"))
            started = time.time()
            with self.assertRaises(RuntimeError) as raised:
                rdr.Edge("unused", launch=[sys.executable, str(fake), str(pids)], startup_timeout=4.0)
            self.assertIn("did not open its DevTools port", str(raised.exception))
            self.assertLess(time.time() - started, 30, "the failed start is bounded")
            parent, child = (int(x) for x in pids.read_text().split())
            deadline = time.time() + 10
            while time.time() < deadline and (pid_alive(parent) or pid_alive(child)):
                time.sleep(0.1)
            self.assertFalse(pid_alive(parent), "the stand-in browser was ended")
            self.assertFalse(pid_alive(child), "the process the stand-in started was ended with it")
            self.assertEqual(set(Path(tempfile.gettempdir()).glob("isotone-design-ref-*")) - before, set(),
                             "the temporary profile was removed")

    def test_closing_twice_is_harmless(self):
        with tempfile.TemporaryDirectory() as scratch:
            fake = Path(scratch) / "fake_browser.py"
            fake.write_text(FAKE_BROWSER, encoding="utf-8")
            tree = rdr.ProcessTree([sys.executable, str(fake), str(Path(scratch) / "pids.txt")])
            tree.end()
            tree.end()
            self.assertIsNotNone(tree.proc.poll())


class StalledBrowser(unittest.TestCase):
    """A render that fails costs one render: the browser is closed and replaced, and the rest are rendered."""

    def setUp(self):
        self.scratch = Path(tempfile.mkdtemp(prefix="isotone-rdr-stall-"))
        self.saved = (rdr.ROOT, rdr.OUT)
        rdr.ROOT, rdr.OUT = self.scratch, self.scratch / "build" / "design-reference"

    def tearDown(self):
        rdr.ROOT, rdr.OUT = self.saved
        shutil.rmtree(self.scratch, ignore_errors=True)

    def docs(self, n: int):
        return [("Button", theme, "compact", "<html></html>", 600) for theme in rdr.THEMES[:n]]

    def test_a_failed_render_restarts_the_browser_and_the_rest_are_rendered(self):
        made: list[object] = []
        picture = png(8, 8, lambda x, y: (x * 30, y * 30, 0))

        class Fake:
            def __init__(self):
                self.closed = 0
                self.number = len(made)
                made.append(self)

            def shoot(self, url, width, out):
                theme = out.stem.split("-")[0]
                if theme == "darkest" and self.number == 0:
                    raise TimeoutError("Page.navigate was not answered within 60 s")
                out.parent.mkdir(parents=True, exist_ok=True)
                data = picture + theme.encode()
                out.write_bytes(data)
                return {"width": 8, "height": 8, "clipped": False, "theme_attr": theme, "comfortable": False,
                        "background": "rgb(1, 2, 3)", "colors": 9, "sha256": theme}

            def close(self):
                self.closed += 1
                return []

        rows, entries, failures = rdr.render_all(self.docs(4), Fake)
        self.assertEqual(len(made), 2, "the stalled browser was replaced once")
        self.assertEqual([b.closed for b in made], [1, 1], "each browser was closed exactly once")
        self.assertEqual(failures, 1)
        self.assertEqual([e["problems"] for e in entries],
                         [[], ["not rendered: Page.navigate was not answered within 60 s"], [], []])
        self.assertEqual([r[3] is not None for r in rows], [True, False, True, True])

    def test_a_browser_that_cannot_start_ends_the_rendering_with_every_render_recorded(self):
        def refuse():
            raise RuntimeError("Edge did not open its DevTools port within 30 s")

        rows, entries, failures = rdr.render_all(self.docs(3), refuse)
        self.assertEqual(failures, 3)
        self.assertTrue(all("the browser could not be started" in e["problems"][0] for e in entries))
        self.assertEqual([r[3] for r in rows], [None, None, None])

    def test_a_command_the_browser_never_answers_is_bounded(self):
        class Chatty:
            def send(self, text):
                pass

            def recv(self):
                return json.dumps({"method": "Page.frameNavigated"})

        browser = rdr.Edge.__new__(rdr.Edge)
        browser.ws, browser.next_id = Chatty(), 0
        saved, rdr.CALL_TIMEOUT = rdr.CALL_TIMEOUT, 0.2
        try:
            started = time.time()
            with self.assertRaises(TimeoutError):
                browser.call("Page.navigate", url="about:blank")
            self.assertLess(time.time() - started, 5)
        finally:
            rdr.CALL_TIMEOUT = saved


class PictureChecks(unittest.TestCase):
    def test_a_one_color_picture_is_blank_and_a_drawn_one_is_not(self):
        self.assertEqual(rdr.png_colors(png(8, 8, lambda x, y: (50, 50, 50))), 1)
        self.assertEqual(rdr.png_colors(png(8, 8, lambda x, y: (x * 30, y * 30, 0))), 64)
        self.assertEqual(rdr.png_colors(b"not a png"), 0)
        self.assertEqual(rdr.png_size(png(7, 3, lambda x, y: (0, 0, 0))), (7, 3))

    def test_a_declared_card_width_is_the_layout_width_and_none_is_shrink_wrapped(self):
        self.assertEqual(rdr.body_width(900), "900px")  # the body is a border box, so this is the card's width
        self.assertEqual(rdr.body_width("900"), "900px")
        self.assertEqual(rdr.body_width(None), "max-content")
        self.assertEqual(rdr.body_width(0), "max-content")
        self.assertEqual(rdr.COLUMN_WIDTH, 1116)

    def test_each_wrong_render_is_named(self):
        self.assertEqual(rdr.render_problems(entry()), [])
        cases = (
            (entry(theme_attr="light"), "carries theme 'light', not 'dark'"),
            (entry(comfortable=True), "is comfortable, not compact"),
            (entry(density="comfortable"), "is compact, not comfortable"),
            (entry(background="rgba(0, 0, 0, 0)"), "background did not resolve"),
            (entry(clipped=True), "was cut"),
            (entry(colors=1), "blank"),
        )
        for bad, needle in cases:
            problems = rdr.render_problems(bad)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn(needle, problems[0])

    def test_two_themes_that_are_one_picture_are_named(self):
        same = [entry(theme="dark", sha256="aa"), entry(theme="light", theme_attr="light", sha256="aa"),
                entry(theme="medium", theme_attr="medium", sha256="bb")]
        self.assertEqual(rdr.set_problems(same), ["Button compact: themes dark, light are the same picture"])
        self.assertEqual(rdr.set_problems([entry(sha256="aa"), entry(density="comfortable", sha256="aa")]), [])


class ReportAndVerify(unittest.TestCase):
    def setUp(self):
        self.scratch = Path(tempfile.mkdtemp(prefix="isotone-rdr-test-"))
        self.saved = (rdr.ROOT, rdr.OUT)
        rdr.ROOT, rdr.OUT = self.scratch, self.scratch / "build" / "design-reference"
        self.picture = png(8, 8, lambda x, y: (x * 30, y * 30, 0))

    def tearDown(self):
        rdr.ROOT, rdr.OUT = self.saved
        shutil.rmtree(self.scratch, ignore_errors=True)

    def reference(self, comp: str, theme: str, density: str, data: bytes | None = None) -> Path:
        path = rdr.OUT / comp / f"{theme}-{density}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if data is not None else self.picture)
        return path

    def native(self, kind: str, comp: str, theme: str, density: str) -> Path:
        base = (self.scratch / "docs" / "captures" / "golden" / "controls" if kind == "golden"
                else self.scratch / "build" / "ui-renders")
        path = base / comp / f"card-{theme}-{density}@1x.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(png(4, 4, lambda x, y: (200, 0, 0) if kind == "golden" else (0, 200, 0)))
        return path

    def test_the_report_prefers_the_golden_falls_back_and_resolves_after_extraction(self):
        golden = self.native("golden", "Button", "dark", "compact")
        self.native("ui-render", "Button", "dark", "compact")  # the golden wins over it
        fallback = self.native("ui-render", "Button", "light", "compact")
        rows = [("Button", "dark", "compact", self.reference("Button", "dark", "compact")),
                ("Button", "light", "compact", self.reference("Button", "light", "compact")),
                ("Button", "medium", "compact", self.reference("Button", "medium", "compact"))]
        report = rdr.write_report(rows)
        text = report.read_text(encoding="utf-8")
        self.assertIn('src="_compare/Button/golden-card-dark-compact@1x.png"', text)
        self.assertIn("approved golden: docs/captures/golden/controls/Button/card-dark-compact@1x.png", text)
        self.assertIn('src="_compare/Button/ui-render-card-light-compact@1x.png"', text)
        self.assertIn("UI render, not yet approved", text)
        self.assertEqual(text.count("no native UI render yet"), 1)
        self.assertEqual((rdr.OUT / "_compare" / "Button" / "golden-card-dark-compact@1x.png").read_bytes(),
                         golden.read_bytes())
        self.assertEqual((rdr.OUT / "_compare" / "Button" / "ui-render-card-light-compact@1x.png").read_bytes(),
                         fallback.read_bytes())
        # Extracted elsewhere, with the checkout gone, every image still resolves inside the folder.
        elsewhere = Path(tempfile.mkdtemp(prefix="isotone-rdr-extract-"))
        try:
            copy = elsewhere / "artifact"
            shutil.copytree(rdr.OUT, copy)
            shutil.rmtree(self.scratch / "docs")
            shutil.rmtree(self.scratch / "build" / "ui-renders")
            import re
            sources = re.findall(r'<img src="([^"]+)"', (copy / "report.html").read_text(encoding="utf-8"))
            self.assertEqual(len(sources), 5)
            for src in sources:
                self.assertFalse(src.startswith(("..", "/")) or ":" in src, src)
                self.assertTrue((copy / src).is_file(), src)
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)

    def manifest(self, entries: list[dict]) -> None:
        rdr.OUT.mkdir(parents=True, exist_ok=True)
        (rdr.OUT / "manifest.json").write_text(json.dumps({"renders": entries}), encoding="utf-8")

    def whole(self, theme: str, density: str = "compact") -> dict:
        data = png(8, 8, lambda x, y, t=theme: (x * 30, y * 30, len(t) * 20))
        path = self.reference("Button", theme, density, data)
        import hashlib
        return entry(theme=theme, theme_attr=theme, density=density, comfortable=density == "comfortable",
                     file=path.relative_to(rdr.OUT).as_posix(), width=8, height=8,
                     sha256=hashlib.sha256(data).hexdigest(), problems=[])

    def test_verify_accepts_a_whole_folder_and_names_each_defect(self):
        entries = [self.whole("dark"), self.whole("light")]
        owed = [("Button", "dark", "compact"), ("Button", "light", "compact")]
        rdr.write_report([("Button", e["theme"], "compact", rdr.OUT / e["file"]) for e in entries])
        self.manifest(entries)
        self.assertEqual(rdr.verify(rdr.OUT, owed), [])
        self.assertEqual(rdr.verify(rdr.OUT, owed + [("Button", "medium", "compact")]),
                         ["Button medium compact: not in the manifest"])
        (rdr.OUT / entries[0]["file"]).write_bytes(png(8, 8, lambda x, y: (1, 2, 3)))
        self.assertEqual(rdr.verify(rdr.OUT, owed),
                         ["Button dark compact: Button/dark-compact.png is not the file the run checked (its hash differs)"])
        (rdr.OUT / entries[0]["file"]).unlink()
        self.assertIn("Button dark compact: Button/dark-compact.png is missing", rdr.verify(rdr.OUT, owed))
        self.manifest([dict(self.whole("dark"), colors=1), self.whole("light")])
        self.assertEqual(rdr.verify(rdr.OUT, owed), ["Button dark compact: the picture is blank (one color)"])
        self.manifest([dict(self.whole("dark"), problems=["not rendered: timeout"]), self.whole("light")])
        self.assertEqual(rdr.verify(rdr.OUT, owed), ["Button dark compact: not rendered: timeout"])
        (rdr.OUT / "manifest.json").unlink()
        self.assertIn("cannot be read", rdr.verify(rdr.OUT, owed)[0])


if __name__ == "__main__":
    unittest.main(verbosity=1)
