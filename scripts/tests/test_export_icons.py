#!/usr/bin/env python3
"""An independent proof of the committed icon rasters (D00 T03 §3).

It does not use scripts/export-icons.py to decide what is right. It holds its own copy of the source map from
docs/design/app-icons.md ("16 px | `<app>-16.svg` | 16, 20", and so on), renders every size of every app and of the
suite directly from the SVG that map names, and compares each with the committed PNG and with the matching entry of
the committed ICO, by decoded pixels. It also shows the comparison can tell the sources apart: a size rendered from
the wrong file differs from the committed one.

Run: python scripts/tests/test_export_icons.py
"""
from __future__ import annotations

import io
import struct
import unittest
from pathlib import Path

import resvg_py
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
ICONS = ROOT / "resources" / "icons"
APPS = ("stilus", "gesso", "albumen", "tinctura", "capio", "folium")
SUITE = "isotone"
# docs/design/app-icons.md: which SVG each size is rendered from (sizes 60, 72, 80, and 512 are the master's too).
DESIGN_LADDER = {
    "-16.svg": (16, 20),
    "-24.svg": (24, 30),
    "-32.svg": (32, 36),
    ".svg": (40, 48, 60, 64, 72, 80, 96, 128, 256, 512),
}
# docs/design/app-icons.md, "Export": the entries of each `.ico`.
DESIGN_ICO = (16, 20, 24, 30, 32, 40, 48, 64, 128, 256)


def render(svg: Path, size: int) -> Image.Image:
    data = bytes(resvg_py.svg_to_bytes(svg_path=str(svg), width=size, height=size))
    return Image.open(io.BytesIO(data)).convert("RGBA")


def opened(path: Path) -> Image.Image:
    """A committed image read whole, its file closed, in its own mode."""
    with Image.open(path) as image:
        image.load()
        return image.copy()


def pixels(image: Image.Image) -> tuple[tuple[int, int], bytes]:
    return image.size, image.tobytes()


def ico_entries(path: Path) -> list[tuple[int, bytes]]:
    data = path.read_bytes()
    _reserved, _kind, count = struct.unpack("<HHH", data[:6])
    out = []
    for n in range(count):
        w, _h, _c, _r, _p, _b, size, offset = struct.unpack("<BBBBHHII", data[6 + 16 * n:22 + 16 * n])
        out.append((w or 256, data[offset:offset + size]))
    return out


class Rasters(unittest.TestCase):
    def test_every_png_is_a_direct_render_of_the_svg_the_design_names(self):
        for name in (*APPS, SUITE):
            for suffix, sizes in DESIGN_LADDER.items():
                svg = ICONS / name / f"{name}{suffix}"
                for size in sizes:
                    with self.subTest(icon=name, size=size):
                        committed = opened(ICONS / name / "PNG" / f"{name}_{size}.png")
                        self.assertEqual(committed.mode, "RGBA")
                        self.assertEqual(pixels(committed), pixels(render(svg, size)))

    def test_every_ico_holds_the_design_ladder_as_the_committed_pngs(self):
        for name in (*APPS, SUITE):
            with self.subTest(icon=name):
                entries = ico_entries(ICONS / name / f"{name}.ico")
                self.assertEqual([size for size, _data in entries], list(DESIGN_ICO))
                for size, data in entries:
                    self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"), f"{name} {size} px is PNG-compressed")
                    committed = opened(ICONS / name / "PNG" / f"{name}_{size}.png").convert("RGBA")
                    self.assertEqual(pixels(Image.open(io.BytesIO(data)).convert("RGBA")), pixels(committed))

    def test_a_wrong_source_renders_differently(self):
        # Without this, a comparison that could not tell the master from a small variant would prove nothing.
        for name in (*APPS, SUITE):
            with self.subTest(icon=name):
                at16 = opened(ICONS / name / "PNG" / f"{name}_16.png").convert("RGBA")
                self.assertNotEqual(pixels(at16), pixels(render(ICONS / name / f"{name}.svg", 16)))
                at40 = opened(ICONS / name / "PNG" / f"{name}_40.png").convert("RGBA")
                self.assertNotEqual(pixels(at40), pixels(render(ICONS / name / f"{name}-32.svg", 40)))

    def test_every_splash_reads_back_at_its_size(self):
        for name in APPS:
            for width, height in ((640, 360), (960, 540), (1280, 720)):
                with self.subTest(icon=name, width=width):
                    image = opened(ICONS / name / "PNG" / f"{name}_splash_{width}.png")
                    self.assertEqual((image.size, image.mode), ((width, height), "RGBA"))

    def test_no_raster_is_committed_that_the_design_does_not_name(self):
        for name in (*APPS, SUITE):
            with self.subTest(icon=name):
                owed = {f"{name}_{size}.png" for sizes in DESIGN_LADDER.values() for size in sizes}
                if name != SUITE:
                    owed |= {f"{name}_splash_{w}.png" for w in (640, 960, 1280)}
                self.assertEqual({p.name for p in (ICONS / name / "PNG").iterdir()}, owed)


if __name__ == "__main__":
    unittest.main(verbosity=1)
