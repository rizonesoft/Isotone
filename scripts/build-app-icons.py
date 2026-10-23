"""Build the app icons (operator decisions 2026-10-23: the Solid glyphs, concept 2, on the Direction C tile and spectrum
band, for Stilus, Gesso and Albumen, then for the three planned apps: Tinctura's hue ring, Capio's crop corners and
crosshair, Folium's layout page).

Writes, for each app in resources/icons/<app>/:
  <app>.svg          the master, 256 viewBox, for 48 px and up
  <app>-16.svg ...   the 16, 24 and 32 px variants: below 40 px each app shows its simplified glyph
  <app>-splash.svg   only the nested master icon inside the Suite card reference design is replaced

The glyphs are one geometry drawn two ways: the master (Stilus: the Bezier curve with its two square anchors;
Gesso: the paintbrush laying a tapered stroke; Albumen: the six-blade iris in its rim; Tinctura: a twelve-hue ring;
Capio: four crop corners around a crosshair; Folium: a page with a header, columns, and a placeholder frame) and the
small glyph (the curve heavier, the brush alone, the iris without its glints, the ring with wider gaps, the corners and
crosshair heavier, the page with three heavy lines). Edit this script, never the SVGs.
Usage: python scripts/build-app-icons.py          rewrite the files
       python scripts/build-app-icons.py --check  exit 1 when a committed file differs from what this script writes
Requires resvg-py and Pillow (the small variants are fitted to the rendered glyph bounds).
"""
import colorsys
import io
import math
import os
import re
import sys

import resvg_py
from xml.etree import ElementTree
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ICONS = os.path.join(ROOT, 'resources', 'icons')
APPS = ('stilus', 'gesso', 'albumen', 'tinctura', 'capio', 'folium')
SPEC = ['#FF4D6D', '#FF9A3C', '#FFD84A', '#4CC47A', '#29C5E6', '#5B7CFF', '#B45CFF']
TILE_TOP, TILE_BOTTOM = '#3D3E45', '#18191D'
BAND = 'M0 230C64 220 120 240 176 230S236 218 256 222'
WHITE = '#F2F3F5'
SVG_TAG = '{http://www.w3.org/2000/svg}svg'

# The glyph area above the band; every glyph is grown about its optical centre.
CX, CY = 128, 116
CURVE = 'M68 168C82 92 174 140 188 64'
ANCHORS = ((68, 168), (188, 64))
BRUSH_T = 'translate(124 112) rotate(45)'
HANDLE = 'M-6 -100C-6 -106 6 -106 6 -100L10 -24H-10Z'
FERRULE = 'M-11 -24H11L13 4H-13Z'
BRISTLE = 'M-13 4C-17 30 -9 54 0 74C9 54 17 30 13 4Z'
PAINT = 'M66 166C96 186 136 160 186 172C191 173 191 180 186 181C138 174 102 206 60 188C52 184 56 164 66 166Z'
GROW = {'stilus': 1.2, 'gesso': 1.12, 'albumen': 1.22, 'tinctura': 1.05, 'capio': 1.0, 'folium': 1.0}
RED = ('#FF4D6D', '#C9264A')
BLUE = ('#A3B5FF', '#5B7CFF', '#3550D6')
INK = '#8A93A6' 
# x0, width, corner radius, band top, band height on each small grid
TILE = {16: (0, 16, 3, 14, 2), 24: (1, 22, 4, 20.5, 2.5), 32: (1, 30, 6, 27.5, 3.5)}
PAD = {16: 1.5, 24: 2.6, 32: 3.2}


def n(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def grow(svg, factor):
    return f'<g transform="translate({CX} {CY}) scale({factor}) translate(-{CX} -{CY})">{svg}</g>'


def iris(radius=56, inner=22):
    """The hexagon opening and the six blades: each blade edge extends a hexagon side to the rim, so the blades
    tile the ring between the opening and the rim exactly."""
    hexv = [(CX + inner * math.cos(math.radians(-90 + 60 * i)), CY + inner * math.sin(math.radians(-90 + 60 * i)))
            for i in range(6)]
    ends = []
    for i in range(6):
        a, b = hexv[i], hexv[(i + 1) % 6]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        dx, dy = dx / length, dy / length
        fx, fy = b[0] - CX, b[1] - CY
        bb = fx * dx + fy * dy
        t = -bb + math.sqrt(bb * bb - (fx * fx + fy * fy - radius * radius))
        ends.append((b[0] + t * dx, b[1] + t * dy))
    blades = [f'M{n(hexv[(i + 1) % 6][0])} {n(hexv[(i + 1) % 6][1])}L{n(ends[i][0])} {n(ends[i][1])}'
              f'A{radius} {radius} 0 0 1 {n(ends[(i + 1) % 6][0])} {n(ends[(i + 1) % 6][1])}Z' for i in range(6)]
    return blades, 'M' + 'L'.join(f'{n(x)} {n(y)}' for x, y in hexv) + 'Z'


def hue_ring(gap, outer=76, inner=48):
    """Twelve hue segments, one every 30 degrees from red at the top, each a wedge of the ring with `gap` degrees
    of tile between neighbours."""
    out = ''
    for i in range(12):
        a0, a1 = math.radians(-90 + i * 30 + gap / 2), math.radians(-90 + (i + 1) * 30 - gap / 2)
        r, g, b = colorsys.hls_to_rgb(i / 12, 0.6, 0.85)
        col = '#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))
        o0, o1 = (CX + outer * math.cos(a0), CY + outer * math.sin(a0)), (CX + outer * math.cos(a1), CY + outer * math.sin(a1))
        i1, i0 = (CX + inner * math.cos(a1), CY + inner * math.sin(a1)), (CX + inner * math.cos(a0), CY + inner * math.sin(a0))
        out += (f'<path d="M{n(o0[0])} {n(o0[1])}A{outer} {outer} 0 0 1 {n(o1[0])} {n(o1[1])}L{n(i1[0])} {n(i1[1])}'
                f'A{inner} {inner} 0 0 0 {n(i0[0])} {n(i0[1])}Z" fill="{col}"/>')
    return out


def glyph_defs(app, p):
    """The glyph's gradients, ids prefixed with `p` (`stilus-c`, `gesso-c-s16`...)."""
    if app == 'gesso':
        return (f'<linearGradient id="{p}-wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0.5" stop-color="#F5923E"/>'
                f'<stop offset="0.5" stop-color="#D9741F"/></linearGradient>'
                f'<linearGradient id="{p}-metal" x1="0" y1="0" x2="1" y2="0"><stop offset="0.5" stop-color="#E3E6EA"/>'
                f'<stop offset="0.5" stop-color="#AEB4BD"/></linearGradient>'
                f'<linearGradient id="{p}-bristle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B8763E"/>'
                f'<stop offset="0.45" stop-color="#E88A3A"/><stop offset="1" stop-color="#FFC861"/></linearGradient>'
                f'<linearGradient id="{p}-paint" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E0701C"/>'
                f'<stop offset="0.55" stop-color="#F5923E"/><stop offset="1" stop-color="#FFD15A"/></linearGradient>')
    if app == 'capio':
        return (f'<linearGradient id="{p}-red" x1="0" y1="0" x2="1" y2="0"><stop offset="0.5" stop-color="{RED[0]}"/>'
                f'<stop offset="0.5" stop-color="{RED[1]}"/></linearGradient>')
    if app == 'folium':
        return (f'<linearGradient id="{p}-paper" x1="0" y1="0" x2="1" y2="0"><stop offset="0.5" stop-color="{WHITE}"/>'
                f'<stop offset="0.5" stop-color="#D9DEE6"/></linearGradient>'
                f'<linearGradient id="{p}-blue" x1="0" y1="0" x2="1" y2="0"><stop offset="0.5" stop-color="{BLUE[1]}"/>'
                f'<stop offset="0.5" stop-color="{BLUE[2]}"/></linearGradient>')
    if app == 'albumen':
        return (f'<linearGradient id="{p}-ring" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6A707A"/>'
                f'<stop offset="1" stop-color="#25272C"/></linearGradient>')
    return ''


def glyph(app, p, small):
    """The app's glyph in 256 space; `small` is the simplified glyph used below 40 px."""
    if app == 'stilus':
        out = (f'<path d="{CURVE}" fill="none" stroke="#127EA0" stroke-width="{25 if small else 18.5}" '
               f'stroke-linecap="round"/>'
               f'<path d="{CURVE}" fill="none" stroke="#29C5E6" stroke-width="{16 if small else 11.5}" '
               f'stroke-linecap="round" transform="translate(-1 -2)"/>')
        if not small:
            out += (f'<path d="{CURVE}" fill="none" stroke="#C7F4FC" stroke-opacity=".8" stroke-width="2.5" '
                    f'stroke-linecap="round" transform="translate(-3 -5)"/>')
        side = 32 if small else 22
        for x, y in ANCHORS:
            out += (f'<rect x="{n(x - side / 2)}" y="{n(y - side / 2)}" width="{side}" height="{side}" rx="3" '
                    f'fill="{WHITE}" stroke="#29C5E6" stroke-width="{6 if small else 4}"/>')
        return grow(out, GROW[app])
    if app == 'gesso':
        crimp = '' if small else '<path d="M-12 -10H12" stroke="#7D838D" stroke-width="2.5"/>'
        brush = (f'<g transform="{BRUSH_T}"><path d="{HANDLE}" fill="url(#{p}-wood)"/>'
                 f'<path d="{FERRULE}" fill="url(#{p}-metal)"/>{crimp}'
                 f'<path d="{BRISTLE}" fill="url(#{p}-bristle)"/></g>')
        if small:
            # The brush alone: the stroke turns to noise below 40 px (operator decision 2026-10-23).
            return brush
        gloss = ('<path d="M70 172C98 188 132 166 176 174" fill="none" stroke="#FFFFFF" stroke-opacity=".4" '
                 'stroke-width="2.5" stroke-linecap="round"/>')
        return grow(f'<path d="{PAINT}" fill="url(#{p}-paint)"/>{gloss}{brush}', GROW[app])
    if app == 'tinctura':
        return grow(hue_ring(gap=3.0 if small else 1.2), GROW[app])
    if app == 'capio':
        w, ring, tick = (22, 10, 10) if small else (16, 7, 7)
        out = ''
        for x, y, sx, sy in ((52, 42, 1, 1), (204, 42, -1, 1), (52, 190, 1, -1), (204, 190, -1, -1)):
            out += (f'<path d="M{x + sx * 44} {y}H{x}V{y + sy * 44}" fill="none" stroke="url(#{p}-red)" '
                    f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
        return out + (f'<circle cx="{CX}" cy="{CY}" r="24" fill="none" stroke="{WHITE}" stroke-width="{ring}"/>'
                      f'<path d="M128 78V96M128 136V154M90 116H108M148 116H166" stroke="{WHITE}" '
                      f'stroke-width="{tick}" stroke-linecap="round"/>')
    if app == 'folium':
        page = (f'<path d="M64 44C64 39 68 36 72 36H164L194 66V188C194 193 190 196 186 196H72C68 196 64 193 64 188Z" '
                f'fill="url(#{p}-paper)"/><path d="M164 36V60C164 63 166 66 170 66H194Z" fill="#B9C0CC"/>'
                f'<rect x="80" y="54" width="70" height="14" rx="4" fill="url(#{p}-blue)"/>'
                f'<rect x="134" y="84" width="44" height="40" rx="3" fill="{BLUE[0]}"/>'
                f'<path d="M134 84L178 124M178 84L134 124" stroke="{BLUE[2]}" stroke-width="{5 if small else 3}"/>'
                f'<rect x="134" y="84" width="44" height="40" rx="3" fill="none" stroke="{BLUE[2]}" '
                f'stroke-width="{5 if small else 3}"/>')
        if small:
            lines = ''.join(f'<path d="M80 {y}H122" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
                            for y in (100, 128, 156))
            lines += f'<path d="M136 152H176" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
        else:
            lines = ''.join(f'<path d="M80 {y}H122" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                            for y in (96, 110, 124, 138, 152, 166))
            lines += ''.join(f'<path d="M136 {y}H176" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
                             for y in (138, 152, 166))
        return grow(page + lines, GROW[app])
    blades, hexagon = iris()
    tones = ''.join(f'<path d="{b}" fill="{"#5FD58C" if i % 2 == 0 else "#38AE64"}"/>' for i, b in enumerate(blades))
    glint = '' if small else (
        '<path d="M84 92A50 50 0 0 1 116 66" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="3" '
        f'stroke-linecap="round"/><circle cx="{CX}" cy="{CY}" r="65" fill="none" stroke="#FFFFFF" '
        'stroke-opacity=".18" stroke-width="2"/>')
    return grow(f'<circle cx="{CX}" cy="{CY}" r="66" fill="url(#{p}-ring)"/><circle cx="{CX}" cy="{CY}" r="56" '
                f'fill="#0B0D10"/>{tones}<path d="{hexagon}" fill="#0B2414"/>{glint}', GROW[app])


def stops():
    return ''.join(f'<stop offset="{i / 6:.2f}" stop-color="{c}"/>' for i, c in enumerate(SPEC))


def master(app):
    p = f'{app}-c'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="256" height="256" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="{p}-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TILE_TOP}"/><stop offset="1" stop-color="{TILE_BOTTOM}"/></linearGradient>
    <linearGradient id="{p}-spec" x1="8" y1="0" x2="248" y2="0" gradientUnits="userSpaceOnUse">{stops()}</linearGradient>
    <clipPath id="{p}-clip"><rect x="8" y="8" width="240" height="240" rx="52"/></clipPath>
    {glyph_defs(app, p)}
  </defs>
  <rect x="8" y="8" width="240" height="240" rx="52" fill="url(#{p}-bg)"/>
  <g clip-path="url(#{p}-clip)">
    <path d="{BAND}V256H0Z" fill="url(#{p}-spec)"/>
    <path d="{BAND}" fill="none" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="2"/>
  </g>
  <rect x="9" y="9" width="238" height="238" rx="51" fill="none" stroke="#FFFFFF" stroke-opacity=".12" stroke-width="2"/>
  {glyph(app, p, False)}
</svg>
'''


def bounds(app):
    """The small glyph's rendered bounds in 256 space, measured on a 1024 px render."""
    p = f'{app}-c'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="1024" height="1024">'
           f'<defs>{glyph_defs(app, p)}</defs>{glyph(app, p, True)}</svg>')
    alpha = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg)))).split()[-1]
    return [v / 4 for v in alpha.getbbox()]


def small(app, sz):
    """The glyph alone, fitted to the box above the band on the size's own grid."""
    x0, w, rx, by, bh = TILE[sz]
    pad = PAD[sz]
    bx0, by0, bx1, by1 = x0 + pad, x0 + pad, x0 + w - pad, by - pad * 0.8
    gx0, gy0, gx1, gy1 = bounds(app)
    s = min((bx1 - bx0) / (gx1 - gx0), (by1 - by0) / (gy1 - gy0))
    cx, cy, gcx, gcy = (bx0 + bx1) / 2, (by0 + by1) / 2, (gx0 + gx1) / 2, (gy0 + gy1) / 2
    p = f'{app}-c-s{sz}'
    band = ''.join(f'<stop offset="{i / 6:.3f}" stop-color="{c}"/>' for i, c in enumerate(SPEC))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sz} {sz}" width="{sz}" height="{sz}">
<defs>
<linearGradient id="{p}-tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TILE_TOP}"/><stop offset="1" stop-color="{TILE_BOTTOM}"/></linearGradient>
<linearGradient id="{p}-spec" x1="{x0}" y1="0" x2="{x0 + w}" y2="0" gradientUnits="userSpaceOnUse">{band}</linearGradient>
<clipPath id="{p}-clip"><rect x="{x0}" y="{x0}" width="{w}" height="{w}" rx="{rx}"/></clipPath>
{glyph_defs(app, p)}
</defs>
<rect x="{x0}" y="{x0}" width="{w}" height="{w}" rx="{rx}" fill="url(#{p}-tile)"/>
<rect x="{x0}" y="{by}" width="{w}" height="{bh}" fill="url(#{p}-spec)" clip-path="url(#{p}-clip)"/>
<g transform="translate({cx:.3f} {cy:.3f}) scale({s:.4f}) translate({-gcx:.2f} {-gcy:.2f})">{glyph(app, p, True)}</g>
</svg>
'''


def splash(app, current):
    """The Suite card reference design with its nested master icon replaced; the card itself is hand-authored."""
    inner = master(app).split('\n', 1)[1].rsplit('</svg>', 1)[0]
    nested = f'<svg x="56" y="92" width="136" height="136" viewBox="0 0 256 256">\n{inner}</svg>'
    pattern = re.compile(r'<svg x="56" y="92" width="136" height="136" viewBox="0 0 256 256">.*?\n</svg>', re.S)
    # Counted before replacing, by parsed element (namespace and local name), not by tag text: a second nested icon (an old one left behind,
    # whatever its attributes) would otherwise survive under the new. The card is the root svg; the icon its only
    # nested one.
    root = ElementTree.fromstring(current)
    nested_svgs = sum(1 for el in root.iter(SVG_TAG)) - 1  # every SVG element under any prefix, the root excluded
    if nested_svgs != 1 or len(pattern.findall(current)) != 1:
        raise SystemExit(f'{app}-splash.svg holds {nested_svgs} nested svg elements; it must hold exactly one, the '
                         f'master icon at x 56, y 92')
    return pattern.sub(lambda _: nested, current)


def outputs():
    files = {}
    for app in APPS:
        folder = os.path.join(ICONS, app)
        files[os.path.join(folder, f'{app}.svg')] = master(app)
        for sz in (16, 24, 32):
            files[os.path.join(folder, f'{app}-{sz}.svg')] = small(app, sz)
        path = os.path.join(folder, f'{app}-splash.svg')
        with open(path, encoding='utf-8') as fh:
            files[path] = splash(app, fh.read())
    return files


def main(argv):
    check = argv[1:] == ['--check']
    if argv[1:] and not check:
        sys.exit('usage: build-app-icons.py [--check]')
    stale = []
    for path, text in outputs().items():
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        # A file not written yet (a newly added app) is stale, never an error.
        same = os.path.exists(path) and open(path, encoding='utf-8').read() == text
        if check:
            if not same:
                stale.append(rel)
            continue
        if not same:
            with open(path, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(text)
            print('wrote', rel)
    if check:
        for rel in stale:
            print(f'STALE {rel}: run python scripts/build-app-icons.py')
        print(f'app icons: {len(stale)} stale')
        return 1 if stale else 0
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
