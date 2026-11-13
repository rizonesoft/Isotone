#!/usr/bin/env python3
"""Export the app and suite icon rasters from their SVG sources (D00 T03 §3; docs/design/app-icons.md, "Export").

Every raster under resources/icons/ is rendered by this script from an SVG, never drawn or resampled by hand:

    resources/icons/<app>/PNG/<app>_<n>.png          16 sizes, each rendered at its own pixel size from the SVG the
                                                     ladder names (SOURCES below)
    resources/icons/<app>/PNG/<app>_splash_<w>.png   the Suite card splash at 640, 960, and 1280 px wide, for
                                                     marketing and as the reference for splash captures (apps only)
    resources/icons/<app>/<app>.ico                  ten PNG-compressed entries (ICO_SIZES), each the exact bytes of
                                                     the PNG committed for that size

for the six apps `scripts/build-app-icons.py` names in `APPS`, and the same for the suite icon (`isotone`), which has
no splash. A PNG is 8-bit RGBA with no text or time chunk, written to a temporary file beside its target and then
moved over it; a file whose decoded pixels already match is left alone, so a different zlib cannot churn the tree.

The splash SVGs set their text in Segoe UI Variable (Display and Text, by optical size), so a faithful splash render
needs that font. Without it the export refuses to write the splash files, and `--check` still requires each to
exist, decode, and read back at its size, names the pixel comparison it skipped, and fails only with
`--require-fonts` (which CI passes, so every candidate's splash pixels are compared on a host with the font).

Usage:
  python scripts/export-icons.py                          # render and write every raster
  python scripts/export-icons.py --check                  # compare the committed rasters with fresh renders
  python scripts/export-icons.py --check --require-fonts  # the same, failing where the splash font is missing
"""
from __future__ import annotations

import argparse
import ast
import io
import os
import struct
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "resources" / "icons"
SUITE = "isotone"
# The design's source map (docs/design/app-icons.md): 16 and 20 px from `-16.svg`, 24 and 30 from `-24.svg`, 32 and
# 36 from `-32.svg`, and 40 px and up from the master. Every size renders directly from its SVG at its own size.
SOURCES = {16: "16", 20: "16", 24: "24", 30: "24", 32: "32", 36: "32", 40: "master", 48: "master", 60: "master",
           64: "master", 72: "master", 80: "master", 96: "master", 128: "master", 256: "master", 512: "master"}
ICO_SIZES = (16, 20, 24, 30, 32, 40, 48, 64, 128, 256)
SPLASH_SIZES = ((640, 360), (960, 540), (1280, 720))
SPLASH_FONT = "Segoe UI Variable"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def apps() -> tuple[str, ...]:
    """The apps `scripts/build-app-icons.py` builds, read from its `APPS` (one list, never a second copy)."""
    tree = ast.parse((ROOT / "scripts" / "build-app-icons.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "APPS" for t in node.targets):
            return tuple(ast.literal_eval(node.value))
    raise SystemExit("export-icons: scripts/build-app-icons.py names no APPS")


def source(name: str, size: int) -> Path:
    variant = SOURCES[size]
    return ICONS / name / (f"{name}.svg" if variant == "master" else f"{name}-{variant}.svg")


def render(svg: Path, width: int, height: int):
    """The SVG rendered at exactly width by height, as an RGBA Pillow image."""
    import resvg_py
    from PIL import Image

    data = bytes(resvg_py.svg_to_bytes(svg_path=str(svg), width=width, height=height))
    image = Image.open(io.BytesIO(data)).convert("RGBA")
    if image.size != (width, height):
        raise SystemExit(f"export-icons: {svg.relative_to(ROOT).as_posix()} rendered at {image.size}, not "
                         f"{(width, height)}")
    return image


def png_bytes(image) -> bytes:
    """8-bit RGBA PNG with no ancillary text or time chunk."""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", compress_level=9)
    return buffer.getvalue()


def ico_bytes(frames: list[tuple[int, bytes]]) -> bytes:
    """An ICO whose entries are the given PNGs, in order, byte for byte (no resampling, no re-encoding)."""
    header = struct.pack("<HHH", 0, 1, len(frames))
    offset = 6 + 16 * len(frames)
    entries, blobs = b"", b""
    for size, data in frames:
        side = 0 if size >= 256 else size  # 0 means 256 in an ICONDIRENTRY
        entries += struct.pack("<BBBBHHII", side, side, 0, 0, 1, 32, len(data), offset)
        blobs += data
        offset += len(data)
    return header + entries + blobs


def read_ico(data: bytes) -> list[tuple[int, int, bytes]]:
    """(width, height, the entry's bytes) for each entry of an ICO, in file order. Raises ValueError when the bytes
    are not an icon or an entry points outside them."""
    if len(data) < 6:
        raise ValueError("shorter than an ICONDIR")
    reserved, kind, count = struct.unpack("<HHH", data[:6])
    if reserved != 0 or kind != 1:
        raise ValueError("not an icon (ICONDIR reserved or type)")
    if len(data) < 6 + 16 * count:
        raise ValueError("the entry table runs past the end")
    out = []
    for n in range(count):
        w, h, _colors, _res, _planes, _bpp, size, offset = struct.unpack("<BBBBHHII", data[6 + 16 * n:22 + 16 * n])
        if offset + size > len(data):
            raise ValueError(f"entry {n} runs past the end")
        out.append((w or 256, h or 256, data[offset:offset + size]))
    return out


def decode(data: bytes):
    from PIL import Image

    return Image.open(io.BytesIO(data)).convert("RGBA")


def same_pixels(a, b) -> bool:
    return a.size == b.size and a.tobytes() == b.tobytes()


def font_present() -> bool:
    """Whether the splash font family is installed (system or per-user), found by the family names inside the font
    files rather than by file name."""
    from fontTools.ttLib import TTFont, TTLibError

    folders = [Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"]
    if os.environ.get("LOCALAPPDATA"):
        folders.append(Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts")
    folders += [Path("/usr/share/fonts"), Path.home() / ".fonts", Path.home() / ".local" / "share" / "fonts"]
    for folder in folders:
        if not folder.is_dir():
            continue
        for path in folder.rglob("*"):
            if path.suffix.lower() not in (".ttf", ".otf"):
                continue
            try:
                names = TTFont(str(path), lazy=True, fontNumber=0)["name"]
            except (TTLibError, OSError, KeyError, struct.error):
                continue  # not a font this reader can open: it is not the family
            if any(record.nameID in (1, 16) and record.toUnicode() == SPLASH_FONT for record in names.names):
                return True
    return False


def plan(name: str) -> tuple[dict[Path, Any], dict[Path, tuple[int, int]], Path, list[int]]:
    """For one icon set: the PNGs to render (path -> image), the splash PNGs (path -> size), the ICO path, and
    the ICO's entry sizes."""
    folder = ICONS / name
    pngs = {folder / "PNG" / f"{name}_{size}.png": render(source(name, size), size, size) for size in SOURCES}
    splash = {} if name == SUITE else {folder / "PNG" / f"{name}_splash_{w}.png": (w, h) for w, h in SPLASH_SIZES}
    return pngs, splash, folder / f"{name}.ico", list(ICO_SIZES)


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(handle, "wb") as out:
            out.write(data)
        os.replace(temp, path)
    except BaseException:
        if os.path.exists(temp):
            os.remove(temp)
        raise


def export() -> int:
    fonts = font_present()
    written = kept = 0
    refused = []
    for name in (*apps(), SUITE):
        pngs, splash, ico, ico_sizes = plan(name)
        frames: dict[int, bytes] = {}
        for path, image in pngs.items():
            data = png_bytes(image)
            if path.exists() and same_pixels(decode(path.read_bytes()), image):
                data = path.read_bytes()  # the committed PNG already holds these pixels: keep its exact bytes
                kept += 1
            else:
                write_atomic(path, data)
                written += 1
            frames[int(path.stem.rsplit("_", 1)[1])] = data
        ico_data = ico_bytes([(size, frames[size]) for size in ico_sizes])
        if not (ico.exists() and ico.read_bytes() == ico_data):
            write_atomic(ico, ico_data)
            written += 1
        else:
            kept += 1
        if not fonts:
            refused += [path for path in splash]
            continue
        for path, (w, h) in splash.items():
            image = render(ICONS / name / f"{name}-splash.svg", w, h)
            if path.exists() and same_pixels(decode(path.read_bytes()), image):
                kept += 1
                continue
            write_atomic(path, png_bytes(image))
            written += 1
    for path in refused:
        print(f"export-icons: REFUSED {path.relative_to(ROOT).as_posix()}: the splash font {SPLASH_FONT!r} is not "
              f"installed here, and a splash rendered without it would not be the design")
    print(f"export-icons: {written} written, {kept} unchanged" + (f", {len(refused)} splash file(s) refused" if refused else ""))
    return 1 if refused else 0


def check(require_fonts: bool) -> int:
    fonts = font_present()
    problems: list[str] = []
    skipped: list[str] = []
    compared = 0
    for name in (*apps(), SUITE):
        pngs, splash, ico, ico_sizes = plan(name)
        expected = set(pngs) | set(splash)
        for path, image in pngs.items():
            rel = path.relative_to(ROOT).as_posix()
            if not path.is_file():
                problems.append(f"MISSING {rel}")
                continue
            try:
                committed = decode(path.read_bytes())
            except OSError as error:
                problems.append(f"UNREADABLE {rel}: {error}")
                continue
            compared += 1
            if not same_pixels(committed, image):
                problems.append(f"DIFFERS {rel}: its pixels are not a fresh render of {source(name, image.size[0]).name}")
        rel = ico.relative_to(ROOT).as_posix()
        if not ico.is_file():
            problems.append(f"MISSING {rel}")
        else:
            try:
                entries = read_ico(ico.read_bytes())
            except ValueError as error:
                problems.append(f"UNREADABLE {rel}: {error}")
                entries = None
            if entries is not None:
                sizes = [w for w, _h, _d in entries]
                if sizes != ico_sizes or any(w != h for w, h, _d in entries):
                    problems.append(f"DIFFERS {rel}: its entries are {sizes}, not {ico_sizes}")
                else:
                    for (size, _h, data), want in zip(entries, ico_sizes):
                        if not data.startswith(PNG_SIGNATURE):
                            problems.append(f"DIFFERS {rel}: the {size} px entry is not PNG-compressed")
                            continue
                        compared += 1
                        image = pngs[ICONS / name / "PNG" / f"{name}_{want}.png"]
                        if not same_pixels(decode(data), image):
                            problems.append(f"DIFFERS {rel}: the {size} px entry is not the {name}_{want}.png render")
        for path, (w, h) in splash.items():
            rel = path.relative_to(ROOT).as_posix()
            if not path.is_file():
                problems.append(f"MISSING {rel}")
                continue
            try:
                committed = decode(path.read_bytes())
            except OSError as error:
                problems.append(f"UNREADABLE {rel}: {error}")
                continue
            if committed.size != (w, h):
                problems.append(f"DIFFERS {rel}: it is {committed.size[0]} by {committed.size[1]}, not {w} by {h}")
                continue
            if not fonts:
                skipped.append(rel)
                continue
            compared += 1
            if not same_pixels(committed, render(ICONS / name / f"{name}-splash.svg", w, h)):
                problems.append(f"DIFFERS {rel}: its pixels are not a fresh render of {name}-splash.svg")
        png_folder = ICONS / name / "PNG"
        if png_folder.is_dir():
            for path in sorted(png_folder.iterdir()):
                if path not in expected:
                    problems.append(f"STRAY {path.relative_to(ROOT).as_posix()}: this script does not produce it")
    for line in problems:
        print(f"export-icons: {line}")
    for rel in skipped:
        print(f"export-icons: {'FAILED' if require_fonts else 'SKIPPED'} the pixel comparison of {rel}: the splash "
              f"font {SPLASH_FONT!r} is not installed here (it exists and reads back at its size)")
    if skipped and require_fonts:
        problems.append("the splash font is missing and --require-fonts was given")
    print(f"export-icons: {compared} raster(s) compared, {len(problems)} problem(s)"
          + (f", {len(skipped)} splash comparison(s) skipped" if skipped else ""))
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Export the icon rasters from their SVG sources, or check them.")
    ap.add_argument("--check", action="store_true", help="compare the committed rasters with fresh renders")
    ap.add_argument("--require-fonts", action="store_true",
                    help="fail, rather than skip, where the splash font is not installed")
    args = ap.parse_args(argv)
    import importlib.util

    missing = [name for name in ("resvg_py", "PIL", "fontTools") if importlib.util.find_spec(name) is None]
    if missing:
        print(f"export-icons: {', '.join(missing)} not installed; run python -m pip install -r "
              f"scripts/requirements-icons.txt")
        return 2
    return check(args.require_fonts) if args.check else export()


if __name__ == "__main__":
    sys.exit(main())
