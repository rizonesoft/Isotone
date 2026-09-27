#!/usr/bin/env python3
"""Build the Photon Interface design system page from docs/design/.

Writes ONE self-contained page, docs/design/index.html, the repository's own
view of the design system (operator decision 2026-09-27: "why don't
we create an html view the same as the artifact in the repo"). It is
published on GitHub Pages by .github/workflows/pages.yml at
https://rizonesoft.github.io/Photon/design/.

The page embeds:
  * tokens.css, generated from docs/design/tokens.json with the artifact
    page's naming: `:root, [data-theme="dark"]` for the first theme, one
    `[data-theme="<id>"]` block per further theme (overrides and aliases
    re-declared), `:root` for spacing, radius, size, duration and
    `--font-<family>`, and one `.<style>` class per type style;
  * the brand book (README.md) and the other prose sections, rendered from
    Markdown by the small converter below (stdlib only);
  * the foundations as tables with swatches per theme;
  * the app icons from resources/icons/<app>/ as inline SVG;
  * every components/<Comp>/preview.html as a live card in an iframe whose
    srcdoc carries tokens.css, components/bundle.css and bundle.js inline,
    as the artifact page does.

The output is deterministic (stable ordering, no timestamps, LF line ends),
so `--check` regenerates in memory and exits 1 when the committed page
differs. Edit the sources, never index.html.

Usage:
  python scripts/build-design-site.py            # write docs/design/index.html
  python scripts/build-design-site.py --check    # exit 1 on drift
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESIGN = ROOT / "docs" / "design"
COMPONENTS = DESIGN / "components"
ICONS = ROOT / "resources" / "icons"
OUT = DESIGN / "index.html"

APPS = ["nodus", "imago", "lumen"]
GROUP_ORDER = ["Foundations", "Actions", "Inputs", "Navigation", "Data", "Shell", "Feedback", "Canvas"]
PROSE_SECTIONS = [("shell-layout.md", "shell"), ("app-icons.md", "icons")]
REPO_BLOB = "https://github.com/rizonesoft/Photon/blob/main/docs/design/"


# ---------------------------------------------------------------- helpers

def read_text(path: Path) -> str:
    """Read a source as UTF-8 with LF line ends, whatever the checkout did."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "section"


def json_for_script(obj) -> str:
    """JSON that is safe inside <script type="application/json">."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).replace("<", "\\u003c")


# ---------------------------------------------------------------- tokens.css

def resolve_color(tokens: dict, name: str, theme: str, first: str, depth: int = 0) -> str:
    tok = tokens[name]
    val = tok["value"]
    v = val if isinstance(val, str) else val.get(theme, val.get(first))
    m = re.fullmatch(r"\{([A-Za-z0-9_.-]+)\}", v)
    if m and depth < 16:
        return resolve_color(tokens, m.group(1), theme, first, depth + 1)
    return v


def css_value(v: str) -> str:
    m = re.fullmatch(r"\{([A-Za-z0-9_.-]+)\}", v)
    return f"var(--{m.group(1)})" if m else v.lower() if v.startswith("#") else v


def build_tokens_css(tj: dict) -> str:
    themes = [t["id"] for t in tj["color"]["themes"]]
    first = themes[0]
    per_theme = list(tj["color"]["tokens"]) + list(tj.get("shadow", {}).get("tokens", []))
    blocks = []
    for i, theme in enumerate(themes):
        lines = []
        for tok in per_theme:
            val = tok["value"]
            if isinstance(val, str):
                v = val
                is_alias = v.startswith("{")
                if i > 0 and not is_alias:
                    continue
            else:
                v = val.get(theme, val.get(first))
                is_alias = v.startswith("{")
                if i > 0 and not is_alias and v == val.get(first):
                    continue
            lines.append(f"  --{tok['name']}: {css_value(v)};")
        sel = f':root, [data-theme="{theme}"]' if i == 0 else f'[data-theme="{theme}"]'
        blocks.append(sel + " {\n" + "\n".join(lines) + "\n}")
    single = []
    for fam in ["spacing", "radius", "size", "duration"]:
        for tok in tj.get(fam, {}).get("tokens", []):
            single.append(f"  --{tok['name']}: {tok['value']};")
    for key, stack in tj["type"]["families"].items():
        single.append(f"  --font-{key}: {stack};")
    blocks.append(":root {\n" + "\n".join(single) + "\n}")
    for group in tj["type"]["groups"]:
        for st in group["styles"]:
            fam = st.get("family", group["family"])
            decl = [f"font-family: var(--font-{fam})", f"font-size: {st['fontSize']}", f"line-height: {st['lineHeight']}", f"font-weight: {st['fontWeight']}"]
            if "letterSpacing" in st:
                decl.append(f"letter-spacing: {st['letterSpacing']}")
            blocks.append(f".{st['name']} {{ " + "; ".join(decl) + "; }")
    return "/* tokens.css: generated from docs/design/tokens.json by scripts/build-design-site.py */\n" + "\n".join(blocks) + "\n"


# ---------------------------------------------------------------- markdown

COLOR_NAMES: set[str] = set()


def inline(text: str) -> str:
    codes: list[str] = []

    def keep_code(m):
        body = m.group(1)
        chip = f'<span class="s-chip" style="background:var(--{body})" aria-hidden="true"></span>' if body in COLOR_NAMES else ""
        codes.append(f"<code>{chip}{esc(body)}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = esc(text)

    def link(m):
        label, href = m.group(1), html.unescape(m.group(2))
        if not re.match(r"^(https?:|mailto:|#)", href):
            href = REPO_BLOB + href
        return f'<a href="{esc(href)}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells, cur, in_code = [], "", False
    for ch in s:
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
    cells.append(cur.strip())
    return cells


def markdown(md: str, prefix: str, heads: list | None = None, shift: int = 0) -> str:
    """A small Markdown converter for the constructs docs/design uses.

    Headings, paragraphs, bullet and numbered lists (one line per item),
    pipe tables, fenced code, block quotes, bold, emphasis, code spans and
    links. `heads` collects (level, id, text) for the navigation.
    """
    lines = md.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    used: set[str] = set()
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            j = i + 1
            buf = []
            while j < n and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append('<div class="s-pre" tabindex="0"><pre><code>' + esc("\n".join(buf)) + "</code></pre></div>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = min(6, len(m.group(1)) + shift)
            text = m.group(2).strip()
            hid = f"{prefix}-{slug(text)}"
            k = 2
            while hid in used:
                hid = f"{prefix}-{slug(text)}-{k}"
                k += 1
            used.add(hid)
            if heads is not None:
                heads.append((len(m.group(1)), hid, text))
            out.append(f'<h{level} id="{hid}">{inline(text)}</h{level}>')
            i += 1
            continue
        if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            head = split_row(line)
            j = i + 2
            rows = []
            while j < n and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            t = ['<div class="s-table" tabindex="0"><table><thead><tr>']
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            i = j
            continue
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + markdown("\n".join(buf), prefix + "-q", None, shift) + "</blockquote>")
            continue
        buf = []
        while i < n and lines[i].strip() and not re.match(r"^(#{1,6}\s|```|\s*[-*]\s+|\s*\d+\.\s+|>|\s*\|)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if not buf:
            buf.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")
    return "\n".join(out)


# ---------------------------------------------------------------- sources

def parse_marker(src: str) -> tuple[dict, str]:
    first, _, rest = src.partition("\n")
    m = re.match(r"^\s*<!--\s*@dsCard(.*?)-->\s*$", first)
    if not m:
        return {}, src
    attrs = {}
    for a in re.finditer(r'([A-Za-z]+)=(?:"([^"]*)"|(\S+))', m.group(1)):
        attrs[a.group(1)] = a.group(2) if a.group(2) is not None else a.group(3)
    return attrs, rest


def svg_inline(path: Path) -> str:
    s = read_text(path).strip()
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    return s.strip()


def svg_data_uri(path: Path) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(read_text(path).encode("utf-8")).decode("ascii")


def blob_map() -> dict[str, str]:
    """Map the artifact's asset ids to data URIs of the repository files."""
    ds = json.loads(read_text(DESIGN / "design-system.json"))
    out = {}
    for group in ds.get("assetGroups", {}).values():
        for name, meta in group.get("files", {}).items():
            app = name.split("-")[0].split(".")[0]
            path = ICONS / app / name
            if path.exists():
                out[meta["blob"]] = svg_data_uri(path)
    return out


def localize_blobs(src: str, blobs: dict[str, str]) -> str:
    """Point /_blob/<id> references (artifact asset URLs) at data URIs."""
    src = src.replace("/_blob/' + ", "' + ")
    src = re.sub(r"/_blob/([0-9a-f]{32})", lambda m: blobs.get(m.group(1), m.group(0)), src)
    return re.sub(r"'([0-9a-f]{32})'", lambda m: "'" + blobs[m.group(1)] + "'" if m.group(1) in blobs else m.group(0), src)


def load_components(blobs):
    comps = []
    for d in sorted(p for p in COMPONENTS.iterdir() if p.is_dir()):
        prev = d / "preview.html"
        if not prev.exists():
            continue
        attrs, body = parse_marker(read_text(prev))
        readme = d / "README.md"
        md = read_text(readme) if readme.exists() else ""
        title = d.name
        m = re.match(r"^#\s+(.+)\n", md)
        if m:
            title = m.group(1).strip()
            md = md[m.end():]
        body = localize_blobs(body, blobs)
        comps.append({
            "id": d.name,
            "title": title,
            "group": attrs.get("group", ""),
            "height": int(attrs.get("height", "120")),
            "width": int(attrs.get("width", "0")),
            "subtitle": attrs.get("subtitle", ""),
            "md": md,
            "html": body,
            "lockhl": ("hl-orange" in body or "hl-windows" in body),
        })
    return comps


# ---------------------------------------------------------------- page parts

def swatch(value: str) -> str:
    return f'<span class="s-sw"><span class="s-sw-c" style="background:{esc(value)}"></span><code>{esc(value)}</code></span>'


def colors_section(tj: dict) -> str:
    themes = tj["color"]["themes"]
    first = themes[0]["id"]
    toks = {t["name"]: t for t in tj["color"]["tokens"]}
    head = "".join(f'<th data-th="{t["id"]}">{esc(t["name"])}</th>' for t in themes)
    rows = []
    for t in tj["color"]["tokens"]:
        cells = []
        for th in themes:
            raw = t["value"] if isinstance(t["value"], str) else t["value"].get(th["id"], t["value"].get(first))
            val = resolve_color(toks, t["name"], th["id"], first)
            note = ""
            m = re.fullmatch(r"\{(.+)\}", raw)
            if m:
                note = f'<span class="s-alias">= {esc(m.group(1))}</span>'
            cells.append(f'<td data-th="{th["id"]}">{swatch(val)}{note}</td>')
        rows.append(f'<tr><th scope="row"><code><span class="s-chip" style="background:var(--{t["name"]})" aria-hidden="true"></span>{esc(t["name"])}</code></th>{"".join(cells)}<td class="s-usage">{inline(t.get("usage", ""))}</td></tr>')
    return (f'<p>{inline(tj["color"].get("note", ""))}</p>'
            f'<div class="s-table s-colors" tabindex="0"><table><thead><tr><th>Token</th>{head}<th>Usage</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def type_section(tj: dict) -> str:
    out = []
    fams = tj["type"]["families"]
    out.append('<div class="s-table" tabindex="0"><table><thead><tr><th>Family</th><th>Stack</th></tr></thead><tbody>'
               + "".join(f"<tr><td><code>--font-{esc(k)}</code></td><td style=\"font-family:var(--font-{esc(k)})\">{esc(v)}</td></tr>" for k, v in fams.items())
               + "</tbody></table></div>")
    for g in tj["type"]["groups"]:
        out.append(f'<h4>{esc(g["name"])}</h4>')
        if g.get("note"):
            out.append(f'<p class="s-muted">{inline(g["note"])}</p>')
        out.append('<div class="s-type">')
        for st in g["styles"]:
            meta = f'{st["fontSize"]} / {st["lineHeight"]}, {st["fontWeight"]}' + (f', {st["letterSpacing"]}' if "letterSpacing" in st else "")
            sample = st.get("sample", st["name"])
            upper = ' style="text-transform:uppercase"' if st["name"] == "section-header" else ""
            out.append(f'<div class="s-type-row"><div class="s-type-meta"><code>{esc(st["name"])}</code><span>{esc(meta)}</span></div>'
                       f'<div class="s-type-sample {esc(st["name"])}"{upper}>{esc(sample)}</div><div class="s-usage">{inline(st.get("usage", ""))}</div></div>')
        out.append("</div>")
    return "\n".join(out)


def simple_table(tokens: list, visual) -> str:
    rows = "".join(f'<tr><th scope="row"><code>{esc(t["name"])}</code></th><td><code>{esc(str(t["value"]))}</code></td><td>{visual(t)}</td><td class="s-usage">{inline(t.get("usage", ""))}</td></tr>' for t in tokens)
    return f'<div class="s-table" tabindex="0"><table><thead><tr><th>Token</th><th>Value</th><th>Sample</th><th>Usage</th></tr></thead><tbody>{rows}</tbody></table></div>'


def px(v: str) -> float:
    m = re.match(r"^([\d.]+)px$", str(v))
    return float(m.group(1)) if m else 0.0


def foundations(tj: dict) -> list[tuple[str, str, str]]:
    themes = tj["color"]["themes"]
    first = themes[0]["id"]
    parts = [("colors", "Colors", colors_section(tj)), ("type", "Type", type_section(tj))]
    parts.append(("spacing", "Spacing", f'<p>{inline(tj["spacing"].get("note", ""))}</p>' + simple_table(
        tj["spacing"]["tokens"], lambda t: f'<span class="s-bar" style="width:var(--{t["name"]})"></span>')))
    parts.append(("radius", "Radius", f'<p>{inline(tj["radius"].get("note", ""))}</p>' + simple_table(
        tj["radius"]["tokens"], lambda t: f'<span class="s-radius" style="border-radius:var(--{t["name"]})"></span>')))
    shadow_rows = []
    for t in tj["shadow"]["tokens"]:
        vals = "".join(f'<li><span>{esc(th["name"])}</span> <code>{esc(t["value"].get(th["id"], t["value"].get(first)) if isinstance(t["value"], dict) else t["value"])}</code></li>' for th in themes)
        shadow_rows.append(f'<div class="s-shadow-card"><div class="s-shadow-demo" style="box-shadow:var(--{t["name"]})"></div><div><code>{esc(t["name"])}</code><ul class="s-plain">{vals}</ul><p class="s-usage">{inline(t.get("usage", ""))}</p></div></div>')
    parts.append(("shadows", "Shadows", f'<p>{inline(tj["shadow"].get("note", ""))}</p><div class="s-shadows">' + "".join(shadow_rows) + "</div>"))
    parts.append(("sizes", "Sizes", f'<p>{inline(tj["size"].get("note", ""))}</p>' + simple_table(
        tj["size"]["tokens"], lambda t: f'<span class="s-bar s-bar-muted" style="width:min(var(--{t["name"]}), 160px)"></span>' if px(t["value"]) >= 1 else "")))
    parts.append(("motion", "Motion", f'<p>{inline(tj["duration"].get("note", ""))} Hover or focus a sample to play it.</p>' + simple_table(
        tj["duration"]["tokens"], lambda t: (f'<span class="s-motion" tabindex="0" role="img" aria-label="{esc(t["name"])} sample" style="--d:var(--{t["name"]})"><span></span></span>' if t["name"] != "ease-out" else f'<span class="s-motion" tabindex="0" role="img" aria-label="ease-out sample" style="--d:var(--duration-slow);--e:var(--ease-out)"><span></span></span>'))))
    return parts


def icons_gallery() -> str:
    cells = []
    for app in APPS:
        d = ICONS / app
        name = app.capitalize()
        ladder = "".join(f'<figure class="s-ic s-ic-{s}"><div class="s-ic-art">{svg_inline(d / f"{app}-{s}.svg")}</div><figcaption><code>{app}-{s}.svg</code></figcaption></figure>' for s in ("16", "24", "32"))
        cells.append(f'<div class="s-app"><h4>{name}</h4><div class="s-app-row">'
                     f'<figure class="s-ic s-ic-master"><div class="s-ic-art">{svg_inline(d / f"{app}.svg")}</div><figcaption><code>{app}.svg</code> master, shown at 96</figcaption></figure>'
                     f'<div class="s-ladder">{ladder}</div>'
                     f'<figure class="s-ic s-ic-splash"><div class="s-ic-art">{svg_inline(d / f"{app}-splash.svg")}</div><figcaption><code>{app}-splash.svg</code> Suite card splash, reference design</figcaption></figure>'
                     "</div></div>")
    return '<div class="s-apps">' + "".join(cells) + '</div><p class="s-muted">Source files: <code>resources/icons/&lt;app&gt;/</code>. The small files are hand-tuned; they are shown at their native size on the page ground.</p>'


# ---------------------------------------------------------------- page

CSS = r"""
:root { color-scheme: dark; }
:root[data-theme="light"] { color-scheme: light; }
* { box-sizing: border-box; }
html { scroll-padding-top: 72px; -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--canvas-surround); color: var(--text-primary); font-family: var(--font-sans); font-size: 14px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
a { color: var(--state-text); }
a:focus-visible, button:focus-visible, input:focus-visible + span, [tabindex]:focus-visible, summary:focus-visible, iframe:focus-visible { outline: var(--focus-ring-w) solid var(--focus-ring); outline-offset: 1px; }
code { font-family: var(--font-mono); font-size: 12px; background: var(--surface-field); border: 1px solid var(--divider); border-radius: var(--radius-sm); padding: 0 4px; }
pre code { white-space: pre; border: 0; background: none; padding: 0; font-size: 12px; line-height: 1.35; }
.s-skip { position: absolute; left: -9999px; top: 0; z-index: 100; background: var(--state); color: var(--state-on); padding: 8px 12px; }
.s-skip:focus { left: 8px; top: 8px; }
.s-top { position: sticky; top: 0; z-index: 20; display: flex; align-items: center; gap: 12px 20px; flex-wrap: wrap; padding: 10px 20px; background: var(--frame); border-bottom: 1px solid var(--divider); }
.s-brand { display: flex; align-items: center; gap: 10px; margin-right: auto; min-width: 0; }
.s-brand strong { font-size: 15px; white-space: nowrap; }
.s-brand span { color: var(--text-secondary); font-size: 12px; white-space: nowrap; }
.s-band { width: 22px; height: 22px; border-radius: 5px; background: #2b2c31; position: relative; overflow: hidden; flex: none; }
.s-band::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 5px; background: linear-gradient(90deg, #ff4d6d, #ff9a3c, #ffd84a, #4cc47a, #29c5e6, #5b7cff, #b45cff); }
.s-menu-btn, .s-sw-btn { display: none; }
.s-sw-btn { align-items: center; gap: 6px; height: 32px; padding: 0 10px; border: 1px solid var(--divider-strong); border-radius: var(--radius-sm); background: var(--surface-control); color: var(--text-primary); font: inherit; font-size: 12px; cursor: pointer; }
.s-sw-btn:hover, .s-menu-btn:hover { background: var(--surface-control-hover); }
.s-switches { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center; }
.s-seg { border: 0; margin: 0; padding: 0; display: flex; align-items: center; gap: 6px; min-width: 0; }
.s-seg legend { float: left; font-size: 12px; color: var(--text-secondary); margin-right: 6px; padding: 0; }
.s-seg .s-opts { display: inline-flex; border: 1px solid var(--divider-strong); border-radius: var(--radius-sm); overflow: hidden; background: var(--surface-control); }
.s-seg label { position: relative; display: block; }
.s-seg input { position: absolute; opacity: 0; inset: 0; margin: 0; cursor: pointer; }
.s-seg label span { display: block; padding: 3px 9px; font-size: 12px; line-height: 18px; white-space: nowrap; cursor: pointer; }
.s-seg label + label span { border-left: 1px solid var(--divider-strong); }
.s-seg label:hover span { background: var(--surface-control-hover); }
.s-seg input:checked + span { background: var(--state); color: var(--state-on); }
.s-seg input:focus-visible + span { outline-offset: -2px; }
.s-layout { display: grid; grid-template-columns: 248px minmax(0, 1fr); align-items: start; }
.s-nav { position: sticky; top: var(--s-top-h, 53px); height: calc(100vh - var(--s-top-h, 53px)); overflow-y: auto; background: var(--surface-panel); border-right: 1px solid var(--divider); padding: 12px 0 24px; font-size: 13px; }
.s-nav h2 { margin: 16px 16px 4px; font-size: 11px; line-height: 14px; font-weight: 600; letter-spacing: .04em; text-transform: uppercase; color: var(--text-secondary); }
.s-nav h3 { margin: 10px 16px 2px 24px; font-size: 11px; font-weight: 600; color: var(--text-secondary); }
.s-nav ul { list-style: none; margin: 0; padding: 0; }
.s-nav a { display: block; padding: 3px 16px 3px 16px; color: var(--text-primary); text-decoration: none; border-left: 2px solid transparent; }
.s-nav ul ul a { padding-left: 28px; color: var(--text-secondary); }
.s-nav a:hover { background: var(--surface-hover); color: var(--text-primary); }
.s-nav a[aria-current="true"] { border-left-color: var(--state-line); background: var(--state-subtle); color: var(--text-primary); }
.s-nav a:focus-visible { outline-offset: -2px; }
.s-main { min-width: 0; padding: 24px 32px 64px; max-width: 1180px; }
.s-sec { margin: 0 0 48px; }
.s-sec > h2 { font-size: 22px; line-height: 1.3; margin: 0 0 12px; font-weight: 600; }
.s-prose h2 { font-size: 18px; margin: 32px 0 8px; font-weight: 600; }
.s-prose h3 { font-size: 15px; margin: 24px 0 6px; font-weight: 600; }
.s-prose h4, .s-sec h4 { font-size: 13px; margin: 20px 0 6px; font-weight: 600; }
.s-prose p, .s-prose li { max-width: 78ch; }
.s-prose > :first-child { margin-top: 0; }
.s-prose ul, .s-prose ol { padding-left: 22px; }
.s-prose blockquote { margin: 12px 0; padding: 4px 12px; border-left: 2px solid var(--divider-strong); color: var(--text-secondary); }
.s-panel { background: var(--surface-panel); border: 1px solid var(--divider); border-radius: var(--radius-lg); padding: 20px 24px; }
.s-muted, .s-usage { color: var(--text-secondary); }
.s-usage { font-size: 12px; line-height: 1.45; }
.s-table td.s-usage { min-width: 300px; }
.s-table { overflow-x: auto; margin: 12px 0; border: 1px solid var(--divider); border-radius: var(--radius-sm); }
.s-table table { border-collapse: collapse; width: 100%; font-size: 13px; }
.s-table th, .s-table td { text-align: left; vertical-align: top; padding: 6px 10px; border-bottom: 1px solid var(--divider); }
.s-table thead th { background: var(--surface-tabstrip); font-size: 12px; font-weight: 600; color: var(--text-secondary); white-space: nowrap; }
.s-table tbody tr:last-child > * { border-bottom: 0; }
.s-table tbody th { font-weight: 400; white-space: nowrap; }
.s-table code, .s-type-meta code { white-space: nowrap; }
.s-colors td[data-th] { white-space: nowrap; }
.s-colors .s-current { background: var(--state-subtle); }
.s-sw { display: inline-flex; align-items: center; gap: 6px; }
.s-sw-c { width: 26px; height: 18px; border-radius: var(--radius-sm); box-shadow: inset 0 0 0 1px rgba(128,128,128,.45); background-clip: padding-box; flex: none; }
.s-sw code { background: none; border: 0; padding: 0; font-size: 11px; }
.s-alias { display: block; font-size: 11px; color: var(--text-secondary); }
.s-chip { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 4px; vertical-align: -1px; box-shadow: inset 0 0 0 1px rgba(128,128,128,.55); }
.s-type { border: 1px solid var(--divider); border-radius: var(--radius-sm); background: var(--surface-panel); }
.s-type-row { display: grid; grid-template-columns: 200px minmax(0, 1fr) minmax(0, 1.2fr); gap: 12px; align-items: center; padding: 10px 12px; border-bottom: 1px solid var(--divider); }
.s-type-row:last-child { border-bottom: 0; }
.s-type-meta { display: flex; flex-direction: column; gap: 2px; font-size: 11px; color: var(--text-secondary); }
.s-type-meta code { align-self: flex-start; }
.s-type-sample { color: var(--text-primary); overflow-wrap: anywhere; }
.s-bar { display: inline-block; height: 12px; min-width: 1px; background: var(--state); border-radius: 1px; vertical-align: middle; }
.s-bar-muted { background: var(--text-secondary); }
.s-radius { display: inline-block; width: 40px; height: 28px; background: var(--surface-control); border: 1px solid var(--border-control); }
.s-shadows { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.s-shadow-card { display: flex; gap: 16px; padding: 16px; background: var(--surface-panel); border: 1px solid var(--divider); border-radius: var(--radius-sm); }
.s-shadow-demo { flex: none; width: 56px; height: 56px; background: var(--surface-raised); border: 1px solid var(--border-popup); border-radius: var(--radius-md); margin: 4px; }
.s-plain { list-style: none; padding: 0; margin: 6px 0; font-size: 11px; }
.s-plain li span { display: inline-block; min-width: 80px; color: var(--text-secondary); }
.s-plain code { white-space: normal; }
.s-motion { display: inline-block; width: 120px; height: 16px; background: var(--surface-field); border: 1px solid var(--divider); border-radius: var(--radius-round); position: relative; }
.s-motion span { position: absolute; left: 2px; top: 2px; width: 10px; height: 10px; border-radius: var(--radius-round); background: var(--state); transition: transform var(--d) var(--e, var(--ease-out)); }
.s-motion:hover span, .s-motion:focus-visible span { transform: translateX(104px); }
.s-apps { display: grid; gap: 16px; }
.s-app { background: var(--frame); border: 1px solid var(--divider); border-radius: var(--radius-sm); padding: 12px 16px 16px; }
.s-app h4 { margin: 0 0 8px; }
.s-app-row { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 20px; }
.s-ladder { display: flex; align-items: flex-end; gap: 16px; padding: 12px; background: var(--surface-panel); border-radius: var(--radius-sm); }
.s-ic { margin: 0; display: flex; flex-direction: column; align-items: center; gap: 6px; }
.s-ic figcaption { font-size: 11px; color: var(--text-secondary); text-align: center; }
.s-ic figcaption code { font-size: 10px; }
.s-ic-art svg { display: block; }
.s-ic-16 svg { width: 16px; height: 16px; }
.s-ic-24 svg { width: 24px; height: 24px; }
.s-ic-32 svg { width: 32px; height: 32px; }
.s-ic-master svg { width: 96px; height: 96px; }
.s-ic-splash svg { width: 320px; height: 180px; max-width: 100%; }
.s-group > h3 { font-size: 16px; margin: 32px 0 12px; font-weight: 600; color: var(--text-secondary); letter-spacing: .02em; }
.s-card { background: var(--surface-panel); border: 1px solid var(--divider); border-radius: var(--radius-lg); margin: 0 0 24px; overflow: hidden; }
.s-card-h { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; padding: 14px 20px 10px; }
.s-card-h h4 { margin: 0; font-size: 16px; font-weight: 600; }
.s-card-h p { margin: 0; color: var(--text-secondary); font-size: 13px; }
.s-card-h .s-note { flex-basis: 100%; font-size: 12px; color: var(--text-secondary); }
.s-stage { position: relative; overflow: hidden; border-top: 1px solid var(--divider); border-bottom: 1px solid var(--divider); background: var(--surface-panel); }
.s-stage iframe { display: block; border: 0; width: 100%; transform-origin: 0 0; background: transparent; }
.s-card-b { padding: 4px 20px 16px; }
.s-card-b details > summary { cursor: pointer; padding: 8px 0; color: var(--text-secondary); font-size: 13px; }
.s-cover .s-stage { border-radius: var(--radius-lg); border: 1px solid var(--divider); }
.s-cover { margin-bottom: 24px; }
.s-pre { overflow-x: auto; background: var(--surface-field); border: 1px solid var(--divider); border-radius: var(--radius-sm); padding: 10px 12px; margin: 12px 0; }
.s-pre pre { margin: 0; }
.s-foot { color: var(--text-secondary); font-size: 12px; border-top: 1px solid var(--divider); padding-top: 16px; }
.s-scrim { display: none; }
@media (max-width: 900px) {
  .s-top { padding: 8px 16px; gap: 8px 12px; }
  .s-menu-btn { display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border: 1px solid var(--divider-strong); border-radius: var(--radius-sm); background: var(--surface-control); color: var(--text-primary); padding: 0; cursor: pointer; }
  .s-brand span { display: none; }
  .s-switches { width: 100%; gap: 6px 12px; display: none; }
  body.s-sw-open .s-switches { display: flex; }
  .s-sw-btn { display: inline-flex; }
  .s-seg legend { min-width: 64px; }
  .s-layout { display: block; }
  .s-nav { position: fixed; z-index: 30; left: 0; top: 0; bottom: 0; height: auto; width: min(300px, 85vw); transform: translateX(-100%); transition: transform var(--duration-standard) var(--ease-out); box-shadow: var(--shadow-dialog); visibility: hidden; }
  body.s-nav-open .s-nav { transform: none; visibility: visible; }
  body.s-nav-open .s-scrim { display: block; position: fixed; inset: 0; z-index: 25; background: var(--scrim); }
  .s-main { padding: 16px 16px 48px; }
  .s-panel { padding: 16px; }
  .s-card-h, .s-card-b { padding-left: 16px; padding-right: 16px; }
  .s-type-row { grid-template-columns: minmax(0, 1fr); gap: 4px; }
  .s-prose p, .s-prose li, .s-type .s-usage { overflow-wrap: anywhere; }
}
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition: none !important; animation: none !important; } }
"""

BRIDGE = r"""(function () {
  var S = __STATE__;
  function apply() {
    document.documentElement.setAttribute('data-theme', S.theme);
    var b = document.body; if (!b) return;
    b.classList.toggle('ph-comfortable', S.density === 'comfortable');
    if (!S.lockhl) { b.classList.toggle('hl-orange', S.highlight === 'orange'); b.classList.toggle('hl-windows', S.highlight === 'windows'); }
    report();
  }
  var pending = false;
  function report() {
    if (pending) return; pending = true;
    requestAnimationFrame(function () {
      pending = false;
      var b = document.body; if (!b) return;
      var h = 0, kids = b.children;
      for (var i = 0; i < kids.length; i++) { var r = kids[i].getBoundingClientRect(); if (r.bottom > h) h = r.bottom; }
      var cs = getComputedStyle(b);
      h = Math.ceil(h + window.scrollY + (parseFloat(cs.marginBottom) || 0) + (parseFloat(cs.paddingBottom) || 0));
      // Natural width: the right edge of the laid-out content, walking into every box that lets its content show
      // (a fixed-width window such as the Cover's 960px frame, or a state grid wider than the card), not into
      // boxes that clip or scroll their content.
      var w = 0, sx = window.scrollX;
      (function walk(el) {
        for (var c = el.firstElementChild; c; c = c.nextElementSibling) {
          var cr = c.getBoundingClientRect(); if (!cr.width && !cr.height) continue;
          var ov = getComputedStyle(c).overflowX;
          var right = ov === 'visible' ? Math.max(cr.right, cr.left + c.scrollWidth) : cr.right;
          if (right + sx > w) w = Math.ceil(right + sx);
          if (ov === 'visible') walk(c);
        }
      })(b);
      w = Math.min(w, 1600);
      parent.postMessage({ phSite: 1, w: w, h: h }, '*');
    });
  }
  window.__phApply = apply;
  addEventListener('message', function (e) {
    var d = e.data; if (!d || !d.phSet) return;
    S.theme = d.theme; S.highlight = d.highlight; S.density = d.density; apply();
  });
  addEventListener('load', function () {
    report();
    if (window.ResizeObserver) { var ro = new ResizeObserver(report); ro.observe(document.documentElement); if (document.body) ro.observe(document.body); }
  });
  addEventListener('resize', report);
})();"""

JS = r"""(function () {
  'use strict';
  var KEY = 'photon-design-site';
  var OPTS = { theme: ['dark', 'darkest', 'medium', 'light'], highlight: ['blue', 'orange', 'windows'], density: ['compact', 'comfortable'] };
  var state = { theme: 'dark', highlight: 'blue', density: 'compact' };
  var data = JSON.parse(document.getElementById('s-data').textContent);
  var tokensCss = document.getElementById('s-tokens').textContent;
  var root = document.documentElement;

  function load() {
    try { var s = JSON.parse(localStorage.getItem(KEY) || '{}'); for (var k in OPTS) if (OPTS[k].indexOf(s[k]) >= 0) state[k] = s[k]; } catch (e) { }
    // A query string overrides without persisting: ?theme=light&highlight=orange&density=comfortable (used for captures).
    try { var q = new URLSearchParams(location.search); for (var k2 in OPTS) { var v = q.get(k2); if (OPTS[k2].indexOf(v) >= 0) state[k2] = v; } } catch (e) { }
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { } }

  function applyHost() {
    root.setAttribute('data-theme', state.theme);
    document.body.classList.toggle('hl-orange', state.highlight === 'orange');
    document.body.classList.toggle('hl-windows', state.highlight === 'windows');
    document.body.classList.toggle('ph-comfortable-host', state.density === 'comfortable');
    var inputs = document.querySelectorAll('.s-seg input');
    for (var i = 0; i < inputs.length; i++) inputs[i].checked = state[inputs[i].name] === inputs[i].value;
    var cells = document.querySelectorAll('.s-colors [data-th]');
    for (var j = 0; j < cells.length; j++) cells[j].classList.toggle('s-current', cells[j].getAttribute('data-th') === state.theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', getComputedStyle(root).getPropertyValue('--frame').trim());
  }

  // ---- preview frames
  var frames = [];
  function buildDoc(f) {
    var src = data.previews[f.id];
    var st = { theme: state.theme, highlight: state.highlight, density: state.density, lockhl: f.lockhl };
    var head = '<style>' + tokensCss + '\n' + data.css + '</style><script>' + data.js + '<\/script><script>' + data.bridge.replace('__STATE__', JSON.stringify(st)) + '<\/script>';
    src = src.replace(/<html([^>]*)>/i, function (m, a) { return '<html' + a.replace(/\sdata-theme="[^"]*"/, '') + ' data-theme="' + st.theme + '">'; });
    src = src.replace(/<head[^>]*>/i, function (m) { return m + head; });
    src = src.replace(/<body[^>]*>/i, function (m) { return m + '<script>window.__phApply && __phApply();<\/script>'; });
    return src;
  }
  function layout(f) {
    var cw = f.stage.clientWidth || 1;
    var w = Math.max(cw, f.width || 0, f.natW || 0);
    var s = Math.min(1, cw / w);
    var h = Math.max(f.height, f.h || 0);
    f.el.style.width = w + 'px';
    f.el.style.height = h + 'px';
    f.el.style.transform = s < 1 ? 'scale(' + s + ')' : '';
    f.stage.style.height = Math.ceil(h * s) + 'px';
    f.el.title = s < 1 ? f.title + ' preview, scaled to ' + Math.round(s * 100) + '% to fit' : f.title + ' preview';
  }
  function mount(f) {
    if (f.mounted) return; f.mounted = true;
    f.el.srcdoc = buildDoc(f);
  }
  function initFrames() {
    var list = document.querySelectorAll('.s-stage[data-preview]');
    for (var i = 0; i < list.length; i++) {
      var st = list[i];
      var f = { id: st.getAttribute('data-preview'), stage: st, el: st.querySelector('iframe'), title: st.getAttribute('data-title'), height: +st.getAttribute('data-height') || 120, width: +st.getAttribute('data-width') || 0, lockhl: st.hasAttribute('data-lockhl') };
      frames.push(f); layout(f);
    }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { var f = frames.filter(function (x) { return x.stage === en.target; })[0]; if (f) { mount(f); io.unobserve(en.target); } } });
      }, { rootMargin: '800px 0px' });
      frames.forEach(function (f) { io.observe(f.stage); });
    } else frames.forEach(mount);
  }
  addEventListener('message', function (e) {
    var d = e.data; if (!d || !d.phSite) return;
    for (var i = 0; i < frames.length; i++) if (frames[i].el.contentWindow === e.source) {
      var f = frames[i]; var cw = f.stage.clientWidth;
      f.h = d.h; if (d.w > cw + 1 && d.w > (f.natW || 0)) f.natW = d.w;
      layout(f); break;
    }
  });
  var rt;
  addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(function () { setTopH(); frames.forEach(function (f) { f.natW = 0; layout(f); }); }, 120);
  });
  function broadcast() {
    var msg = { phSet: 1, theme: state.theme, highlight: state.highlight, density: state.density };
    frames.forEach(function (f) { if (f.mounted && f.el.contentWindow) f.el.contentWindow.postMessage(msg, '*'); });
  }

  // ---- navigation
  function setTopH() { var t = document.querySelector('.s-top'); if (t) root.style.setProperty('--s-top-h', t.offsetHeight + 'px'); }
  function initNav() {
    var btn = document.querySelector('.s-menu-btn'), nav = document.getElementById('s-nav'), scrim = document.querySelector('.s-scrim');
    function close(focusBtn) { document.body.classList.remove('s-nav-open'); btn.setAttribute('aria-expanded', 'false'); if (focusBtn) btn.focus(); }
    btn.addEventListener('click', function () {
      var open = !document.body.classList.contains('s-nav-open');
      document.body.classList.toggle('s-nav-open', open); btn.setAttribute('aria-expanded', String(open));
      if (open) { var a = nav.querySelector('a'); if (a) a.focus(); }
    });
    scrim.addEventListener('click', function () { close(true); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a') && document.body.classList.contains('s-nav-open')) close(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('s-nav-open')) close(true); });
    var links = nav.querySelectorAll('a[href^="#"]'), map = {};
    for (var i = 0; i < links.length; i++) map[links[i].getAttribute('href').slice(1)] = links[i];
    if (!('IntersectionObserver' in window)) return;
    var current = null;
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var a = map[en.target.id]; if (!a) return;
        if (current) current.removeAttribute('aria-current');
        a.setAttribute('aria-current', 'true'); current = a;
      });
    }, { rootMargin: '-80px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var t = document.getElementById(id); if (t) spy.observe(t); });
  }

  function initSwitches() {
    var sb = document.querySelector('.s-sw-btn');
    sb.addEventListener('click', function () {
      var open = !document.body.classList.contains('s-sw-open');
      document.body.classList.toggle('s-sw-open', open); sb.setAttribute('aria-expanded', String(open)); setTopH();
    });
    var inputs = document.querySelectorAll('.s-seg input');
    for (var i = 0; i < inputs.length; i++) inputs[i].addEventListener('change', function (e) {
      state[e.target.name] = e.target.value; save(); applyHost(); broadcast();
    });
  }

  load(); applyHost(); setTopH(); initSwitches(); initNav(); initFrames();
})();"""


def seg(name: str, legend: str, options: list[tuple[str, str]]) -> str:
    opts = "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if k == 0 else ""}><span>{esc(t)}</span></label>' for k, (v, t) in enumerate(options))
    return f'<fieldset class="s-seg"><legend>{esc(legend)}</legend><div class="s-opts">{opts}</div></fieldset>'


def stage(c: dict) -> str:
    lock = " data-lockhl" if c["lockhl"] else ""
    width = f' data-width="{c["width"]}"' if c["width"] else ""
    return (f'<div class="s-stage" data-preview="{esc(c["id"])}" data-title="{esc(c["title"])}" data-height="{c["height"]}"{width}{lock}>'
            f'<iframe title="{esc(c["title"])} preview" sandbox="allow-scripts"></iframe></div>')


def highlight_rules(bundle_css: str) -> str:
    """The Highlight option rules of bundle.css, so the page chrome follows the Highlight switch too."""
    start = bundle_css.find("/* Highlight color options")
    end = bundle_css.find("html, body {", start)
    return bundle_css[start:end].strip() + "\n" if start >= 0 and end > start else ""


def build() -> str:
    tj = json.loads(read_text(DESIGN / "tokens.json"))
    COLOR_NAMES.clear()
    COLOR_NAMES.update(t["name"] for t in tj["color"]["tokens"])
    tokens_css = build_tokens_css(tj)
    blobs = blob_map()
    comps = load_components(blobs)
    cover = next((c for c in comps if c["id"] == "Cover"), None)
    cards = [c for c in comps if c["id"] != "Cover"]

    # groups in design order, then any other group by name, ungrouped last
    groups: dict[str, list] = {}
    for c in cards:
        groups.setdefault(c["group"] or "Other", []).append(c)
    order = [g for g in GROUP_ORDER if g in groups] + sorted(g for g in groups if g not in GROUP_ORDER and g != "Other") + (["Other"] if "Other" in groups else [])

    nav: list[str] = []
    body: list[str] = []

    # Overview
    ov_heads: list = []
    brand = markdown(read_text(DESIGN / "README.md"), "ov", ov_heads)
    cover_html = f'<div class="s-cover">{stage(cover)}</div>' if cover else ""
    body.append(f'<section class="s-sec" id="overview" aria-labelledby="overview-h"><h2 id="overview-h">Photon Interface</h2>{cover_html}<div class="s-panel s-prose">{brand}</div></section>')
    nav.append('<h2>Overview</h2><ul><li><a href="#overview">Brand book</a><ul>' + "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for lvl, hid, t in ov_heads if lvl == 2) + "</ul></li></ul>")

    # Foundations
    nav.append("<h2>Foundations</h2><ul>")
    for fid, title, content in foundations(tj):
        body.append(f'<section class="s-sec" id="f-{fid}" aria-labelledby="f-{fid}-h"><h2 id="f-{fid}-h">{esc(title)}</h2>{content}</section>')
        nav.append(f'<li><a href="#f-{fid}">{esc(title)}</a></li>')
    nav.append("</ul>")

    # Prose sections: shell layout and app icons
    nav.append("<h2>Guides</h2><ul>")
    for fname, prefix in PROSE_SECTIONS:
        md = read_text(DESIGN / fname)
        m = re.match(r"^#\s+(.+)\n", md)
        title = m.group(1).strip() if m else fname
        if m:
            md = md[m.end():]
        extra = icons_gallery() if prefix == "icons" else ""
        sid = f"g-{prefix}"
        body.append(f'<section class="s-sec" id="{sid}" aria-labelledby="{sid}-h"><h2 id="{sid}-h">{esc(title)}</h2>{extra}<div class="s-panel s-prose">{markdown(md, prefix)}</div></section>')
        nav.append(f'<li><a href="#{sid}">{esc(title)}</a></li>')
    nav.append("</ul>")

    # Components
    nav.append("<h2>Components</h2>")
    comp_html = ['<section class="s-sec" id="components" aria-labelledby="components-h"><h2 id="components-h">Components</h2>'
                 '<p class="s-muted">Each card is the live preview from <code>docs/design/components/&lt;Comp&gt;/preview.html</code> with its guidelines. The Theme, Highlight and Density switches above apply to every preview.</p>']
    for g in order:
        gid = "cg-" + slug(g)
        comp_html.append(f'<div class="s-group" id="{gid}"><h3>{esc(g)}</h3>')
        nav.append(f'<h3>{esc(g)}</h3><ul>')
        for c in groups[g]:
            cid = "c-" + c["id"]
            note = '<p class="s-note">Shows all three Highlight options side by side, so the Highlight switch leaves it as is.</p>' if c["lockhl"] else ""
            readme = markdown(c["md"], cid, None, shift=2) if c["md"].strip() else ""
            guide = f'<div class="s-card-b s-prose">{readme}</div>' if readme else ""
            comp_html.append(f'<article class="s-card" id="{cid}" aria-labelledby="{cid}-h"><header class="s-card-h"><h4 id="{cid}-h">{esc(c["title"])}</h4>'
                             f'<p>{esc(c["subtitle"])}</p>{note}</header>{stage(c)}{guide}</article>')
            nav.append(f'<li><a href="#{cid}">{esc(c["title"])}</a></li>')
        comp_html.append("</div>")
        nav.append("</ul>")
    comp_html.append("</section>")
    body.extend(comp_html)

    body.append('<footer class="s-foot"><p>Generated from <a href="https://github.com/rizonesoft/Photon/tree/main/docs/design"><code>docs/design/</code></a> by <code>scripts/build-design-site.py</code>. '
                'Edit the sources, never this page. The UI standard is <a href="https://github.com/rizonesoft/Photon/blob/main/standards/ui.md"><code>standards/ui.md</code></a>.</p></footer>')

    data = {
        "css": read_text(COMPONENTS / "bundle.css"),
        "js": read_text(COMPONENTS / "bundle.js"),
        "bridge": BRIDGE,
        "previews": {c["id"]: c["html"] for c in comps},
    }

    switches = (seg("theme", "Theme", [("dark", "Dark"), ("darkest", "Darkest"), ("medium", "Medium Gray"), ("light", "Light")])
                + seg("highlight", "Highlight", [("blue", "Blue"), ("orange", "Photon orange"), ("windows", "Windows accent")])
                + seg("density", "Density", [("compact", "Compact"), ("comfortable", "Comfortable")]))

    page = f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Photon Interface, the design system of the Photon Graphics Suite (Nodus, Imago, Lumen): themes, tokens, controls, and app icons.">
<meta name="theme-color" content="#282828">
<meta name="generator" content="scripts/build-design-site.py">
<title>Photon Interface</title>
<!-- Generated from docs/design/ by scripts/build-design-site.py. Do not edit: change the sources and regenerate. -->
<style id="s-tokens">
{tokens_css}</style>
<style>
{highlight_rules(data["css"])}{CSS.strip()}
</style>
</head>
<body>
<a class="s-skip" href="#s-main">Skip to content</a>
<header class="s-top">
<button class="s-menu-btn" type="button" aria-controls="s-nav" aria-expanded="false" aria-label="Sections"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
<div class="s-brand"><span class="s-band" aria-hidden="true"></span><strong>Photon Interface</strong><span>Design system of Nodus, Imago and Lumen</span></div>
<button class="s-sw-btn" type="button" aria-controls="s-switches" aria-expanded="false">Display</button>
<div class="s-switches" id="s-switches" role="group" aria-label="Preview settings">{switches}</div>
</header>
<div class="s-layout">
<nav class="s-nav" id="s-nav" aria-label="Sections">
{"".join(nav)}
</nav>
<div class="s-scrim" aria-hidden="true"></div>
<main class="s-main" id="s-main" tabindex="-1">
{chr(10).join(body)}
</main>
</div>
<script type="application/json" id="s-data">{json_for_script(data)}</script>
<script>
{JS}
</script>
</body>
</html>
"""
    return page


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="regenerate in memory and exit 1 if docs/design/index.html differs")
    ap.add_argument("--out", type=Path, default=OUT, help="output path (default docs/design/index.html)")
    args = ap.parse_args(argv)
    page = build()
    if args.check:
        if not args.out.exists():
            print(f"build-design-site: {args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out} is missing; run python scripts/build-design-site.py", file=sys.stderr)
            return 1
        current = args.out.read_bytes().decode("utf-8").replace("\r\n", "\n")
        if current != page:
            print("build-design-site: docs/design/index.html is stale; run python scripts/build-design-site.py and commit the result", file=sys.stderr)
            return 1
        print("build-design-site: docs/design/index.html is current")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)
    print(f"build-design-site: wrote {args.out} ({len(page.encode('utf-8'))} bytes, {len(data_count(page))} previews)")
    return 0


def data_count(page: str) -> list:
    return re.findall(r'data-preview="', page)


if __name__ == "__main__":
    sys.exit(main())
