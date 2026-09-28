"""Build the Isotone suite icon, wordmark, and lockups (operator decision 2026-09-28: icon A "Three Lights", wordmark 2).

Writes:
  resources/icons/isotone/isotone.svg            the suite icon master (256 viewBox, Direction C tile and band)
  resources/brand/isotone-wordmark-on-dark.svg   "isotone" with the Three Lights dot and GRAPHICS SUITE, light ink
  resources/brand/isotone-wordmark-on-light.svg  the same in dark ink
  resources/brand/isotone-lockup-on-dark.svg     icon plus wordmark, for dark grounds
  resources/brand/isotone-lockup-on-light.svg    icon plus wordmark, for light grounds

The letters are outlines of Sora (SIL Open Font License 1.1, resources/brand/fonts/), so the files never depend on an
installed font. The three lights mix by the screen formula, precomputed per overlap, so no renderer needs blend modes.
Usage: python scripts/build-suite-mark.py   (then python scripts/generate-small-icons.py --in-place for 16/24/32)
Requires fonttools.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
FONT = os.path.join(ROOT, 'resources', 'brand', 'fonts', 'Sora-wght.ttf')
SPEC = ['#FF4D6D', '#FF9A3C', '#FFD84A', '#4CC47A', '#29C5E6', '#5B7CFF', '#B45CFF']
LIGHTS = [('#29C5E6', 0, -1), ('#F5923E', -0.866, 0.5), ('#4CC47A', 0.866, 0.5)]  # Stilus, Gesso, Albumen


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def screen(*cols):
    out = (0, 0, 0)
    for c in cols:
        c = rgb(c)
        out = tuple(255 - (255 - a) * (255 - b) / 255 for a, b in zip(out, c))
    return '#%02X%02X%02X' % tuple(round(v) for v in out)


def lights(cx, cy, r, d, prefix):
    """Three overlapping circles of radius r whose centres sit d from (cx, cy); overlaps precomputed."""
    pts = [(cx + dx * d, cy + dy * d) for _, dx, dy in LIGHTS]
    cols = [c for c, _, _ in LIGHTS]
    ids = [f'{prefix}-l{i}' for i in range(3)]
    defs = ''.join(f'<clipPath id="{ids[i]}"><circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}"/></clipPath>' for i, (x, y) in enumerate(pts))
    c = lambda i, fill: f'<circle cx="{pts[i][0]:.2f}" cy="{pts[i][1]:.2f}" r="{r:.2f}" fill="{fill}"/>'
    body = ''.join(c(i, cols[i]) for i in range(3))
    for a, b in ((0, 1), (1, 2), (0, 2)):
        body += f'<g clip-path="url(#{ids[a]})">{c(b, screen(cols[a], cols[b]))}</g>'
    body += f'<g clip-path="url(#{ids[0]})"><g clip-path="url(#{ids[1]})">{c(2, screen(*cols))}</g></g>'
    return defs, body


def icon():
    stops = ''.join(f'<stop offset="{i / 6:.2f}" stop-color="{c}"/>' for i, c in enumerate(SPEC))
    ldefs, lbody = lights(128, 114, 45, 25, 'isotone-c')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="256" height="256" viewBox="0 0 256 256">
  <defs>
    <linearGradient id="isotone-c-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#34353B"/><stop offset="1" stop-color="#1E1F23"/></linearGradient>
    <linearGradient id="isotone-c-spec" x1="8" y1="0" x2="248" y2="0" gradientUnits="userSpaceOnUse">{stops}</linearGradient>
    <clipPath id="isotone-c-clip"><rect x="8" y="8" width="240" height="240" rx="48"/></clipPath>
    {ldefs}
  </defs>
  <rect x="8" y="8" width="240" height="240" rx="48" fill="url(#isotone-c-bg)"/>
  <g clip-path="url(#isotone-c-clip)">
    <path d="M0 226C64 214 120 238 176 226S236 212 256 216V256H0Z" fill="url(#isotone-c-spec)"/>
    <path d="M0 226C64 214 120 238 176 226S236 212 256 216" fill="none" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="2"/>
  </g>
  <rect x="9" y="9" width="238" height="238" rx="47" fill="none" stroke="#FFFFFF" stroke-opacity=".09" stroke-width="2"/>
  <g id="isotone-glyph">{lbody}</g>
</svg>
'''


class Face:
    def __init__(self, weight):
        f = TTFont(FONT)
        self.font = instantiateVariableFont(f, {'wght': weight})
        self.gs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font['head'].unitsPerEm

    def run(self, text, size, x, y, tracking=0.0):
        """Outline text at font size (px) with its baseline at y; returns (path d, advance end x)."""
        s = size / self.upm
        d = ''
        for ch in text:
            g = self.cmap[ord(ch)]
            pen = SVGPathPen(self.gs)
            self.gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
            d += pen.getCommands()
            x += self.gs[g].width * s + tracking
        return d, x

    def bounds(self, ch):
        bp = BoundsPen(self.gs)
        self.gs[self.cmap[ord(ch)]].draw(bp)
        return bp.bounds


def wordmark(ink, sub, x0=0.0, y0=0.0, align='center'):
    """The wordmark block; returns (svg fragment, width, height)."""
    big, small = Face(600), Face(500)
    size, track = 58, -1.5
    word = 'ısotone'
    _, width = big.run(word, size, 0, 0, track)
    width -= track
    sub_text = 'GRAPHICS SUITE'
    _, sw = small.run(sub_text, 12, 0, 0, 4.5)
    sw -= 4.5
    top_pad = 22
    base = y0 + top_pad + 44
    total_w = max(width, sw)
    wx = x0 + (total_w - width) / 2 if align == 'center' else x0
    d, _ = big.run(word, size, wx, base, track)
    # the Three Lights dot, centred over the dotless i's stem where Sora's own dot sits
    s = size / big.upm
    ib = big.bounds('ı'); jb = big.bounds('i')
    cx = wx + (ib[0] + ib[2]) / 2 * s
    dot_bottom = base - ib[3] * s
    dot_top = base - jb[3] * s
    cy = (dot_top + dot_bottom) / 2 - 1.0
    stem = (ib[2] - ib[0]) * s
    ldefs, lbody = lights(cx, cy, stem * 0.52, stem * 0.36, f'isotone-wm-{ink[1:]}')
    sx = x0 + (total_w - sw) / 2 if align == 'center' else x0 + 1
    sd, _ = small.run(sub_text, 12, sx, base + 30, 4.5)
    frag = f'<defs>{ldefs}</defs><path d="{d}" fill="{ink}"/>{lbody}<path d="{sd}" fill="{sub}"/>'
    return frag, total_w, top_pad + 44 + 30 + 6


def write(rel, svg):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(svg)
    print('wrote', rel)


def main():
    write('resources/icons/isotone/isotone.svg', icon())
    for name, ink, sub in (('on-dark', '#F2F2F3', '#A6A7AD'), ('on-light', '#1E1F23', '#5C5D63')):
        frag, w, h = wordmark(ink, sub, 0, 0)
        write(f'resources/brand/isotone-wordmark-{name}.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}"><title>Isotone Graphics Suite</title>{frag}</svg>\n')
        tile = 96
        frag, w, h = wordmark(ink, sub, tile + 22, 0, align='left')
        H = max(h, tile)
        ic = icon().split('\n', 1)[1].rsplit('</svg>', 1)[0]
        ic_svg = f'<svg x="0" y="{(H - tile) / 2:.1f}" width="{tile}" height="{tile}" viewBox="0 0 256 256">{ic}</svg>'
        W = tile + 22 + w
        write(f'resources/brand/isotone-lockup-{name}.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}"><title>Isotone Graphics Suite</title>{ic_svg}<g transform="translate(0 {(H - h) / 2:.1f})">{frag}</g></svg>\n')


if __name__ == '__main__':
    main()
