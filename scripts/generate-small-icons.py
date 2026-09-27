"""Generate the 16, 24 and 32 px app icon variants from the master SVGs.

Each variant carries the main glyph alone (Stilus nib, Pinxit brush, Albumen aperture),
scaled to fill the space above the spectrum band (operator decision 2026-09-27).
Usage: python scripts/generate-small-icons.py --in-place   (rewrites resources/icons/<app>/<app>-{16,24,32}.svg)
Requires resvg-py and Pillow (see scripts/requirements-icons.txt once D00 T03 §3 ships).
"""
import re, io, resvg_py
from PIL import Image
import os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','resources','icons')
SPEC=['#FF4D6D','#FF9A3C','#FFD84A','#4CC47A','#29C5E6','#5B7CFF','#B45CFF']
# glyph-only fragments in 256 space, taken from the masters (inner transforms kept, outer scale removed)
def master(app): return open(f'{R}/{app}/{app}.svg',encoding='utf-8').read()
def defs(app):
    d=re.search(r'<defs>(.*?)</defs>',master(app),re.S).group(1)
    keep=[m.group(0) for m in re.finditer('<(linearGradient|radialGradient|clipPath)[^>]*id="([^"]+)"[^>]*>.*?</'+chr(92)+'1>',d,re.S) if not re.search('-(bg|spec|clip)"',m.group(0).split('>')[0])]
    return '<defs>'+''.join(keep)+'</defs>'
def frag(app, sz):
    m=master(app)
    if app=='stilus':
        g=re.search(r'<g transform="translate\(104 183\) rotate\(45\) scale\(1\)">.*?</g>',m,re.S).group(0)
        if sz==16:  # solid nib: drop the keyhole, keep a slit
            g=g.replace(' fill-rule="evenodd"','').replace('ZM-3.5 -43.57A11 11 0 1 1 3.5 -43.57L1.2 -10L-1.2 -10Z','Z')
            g=g.replace('</g>','<path d="M0 -6V-58" stroke="#1E1F23" stroke-width="9" stroke-linecap="round"/></g>')
        return g
    if app=='pinxit':
        return re.search(r'<g transform="translate\(78 180\) rotate\(45\) scale\(0.94\)">.*?</g>',m,re.S).group(0)
    if app=='albumen':
        body=m[m.index('<circle cx="128" cy="128" r="57"'):m.index('</g>\n</svg>') if '</g>\n</svg>' in m else m.rindex('</g>')]
        body=body.split('<circle cx="123" cy="122"')[0]  # drop the highlight dot
        if sz==16: body=body.replace('stroke-width="4"','stroke-width="7"')
        return body
def bbox(app,sz):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="1024" height="1024">{defs(app)}{frag(app,sz)}</svg>'
    a=Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=svg)))).split()[-1]
    return [v/4 for v in a.getbbox()]
TILE={16:(0,16,3,14,2),24:(1,22,4,20.5,2.5),32:(1,30,6,27.5,3.5)}  # x0,w,rx,bandY,bandH
def small(app,sz):
    x0,w,rx,by,bh=TILE[sz]
    # glyph box above the band
    pad={16:1.5,24:2.6,32:3.2}[sz]
    bx0,by0,bx1,by1=x0+pad, x0+pad, x0+w-pad, by-pad*0.8
    gx0,gy0,gx1,gy1=bbox(app,sz)
    s=min((bx1-bx0)/(gx1-gx0),(by1-by0)/(gy1-gy0))
    cx,cy=(bx0+bx1)/2,(by0+by1)/2; gcx,gcy=(gx0+gx1)/2,(gy0+gy1)/2
    stops=''.join(f'<stop offset="{i/6:.3f}" stop-color="{c}"/>' for i,c in enumerate(SPEC))
    d=defs(app).replace('<defs>','').replace('</defs>','')
    d=re.sub(r'id="'+app+r'-c-', f'id="{app}-c-s{sz}-', d); fr=frag(app,sz).replace(f'url(#{app}-c-',f'url(#{app}-c-s{sz}-')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sz} {sz}" width="{sz}" height="{sz}">
<defs>
<linearGradient id="{app}-c-s{sz}-tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#34353B"/><stop offset="1" stop-color="#1E1F23"/></linearGradient>
<linearGradient id="{app}-c-s{sz}-spec" x1="{x0}" y1="0" x2="{x0+w}" y2="0" gradientUnits="userSpaceOnUse">{stops}</linearGradient>
<clipPath id="{app}-c-s{sz}-clip"><rect x="{x0}" y="{x0}" width="{w}" height="{w}" rx="{rx}"/></clipPath>
{d}
</defs>
<rect x="{x0}" y="{x0}" width="{w}" height="{w}" rx="{rx}" fill="url(#{app}-c-s{sz}-tile)"/>
<rect x="{x0}" y="{by}" width="{w}" height="{bh}" fill="url(#{app}-c-s{sz}-spec)" clip-path="url(#{app}-c-s{sz}-clip)"/>
<g transform="translate({cx:.3f} {cy:.3f}) scale({s:.4f}) translate({-gcx:.2f} {-gcy:.2f})">{fr}</g>
</svg>
'''
import sys
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: generate-small-icons.py --in-place | <out-dir>')
    for app in ['stilus', 'pinxit', 'albumen']:
        out = os.path.join(R, app) if sys.argv[1] == '--in-place' else sys.argv[1]
        for sz in (16, 24, 32):
            with open(os.path.join(out, f'{app}-{sz}.svg'), 'w', encoding='utf-8', newline='\n') as f:
                f.write(small(app, sz))
