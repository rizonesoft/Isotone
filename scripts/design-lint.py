#!/usr/bin/env python3
"""design-lint: the design contract's static gate over the WPF sources.

standards/design-contract.md (operator decisions 2026-09-27) makes
docs/design/ the source every surface implements 1:1: every color, size,
radius, spacing, font, and duration comes from docs/design/tokens.json
through the Photon.UI dictionaries, colors through DynamicResource. This
script reads (never edits) src/**/*.xaml and src/**/*.cs of every UI
project (a csproj with <UseWPF>true</UseWPF> that is not a test project)
and reports each departure as

    <file>:<line>:<rule>:<message>

Rules (error unless marked warn):

  color-literal          a #RGB, #ARGB, #RRGGBB, or #AARRGGBB value in XAML
                         (attribute or element text) or in a C# string
  named-color            a named color (White, Red, ...) on a XAML brush or
                         color property; Transparent is allowed (hit testing)
  color-api              C# Color.FromRgb/FromArgb/FromScRgb, Colors.X,
                         Brushes.X (Transparent allowed), a new
                         SolidColorBrush built from a literal, or
                         ColorConverter.ConvertFromString
  static-color-resource  {StaticResource K} where K is a color or brush (a
                         color token, a key defined as a Color or Brush, a
                         key ending in Brush or Color, or any key on a brush
                         property): colors are DynamicResource so a theme,
                         Highlight, or density switch restyles live
  non-token-color        a color or brush resource key that is not a color
                         token of docs/design/tokens.json (nor Photon.App.*)
  unknown-resource-key   (warn) a resource key defined nowhere: not a token,
                         not a neutral density key, not an x:Key in any
                         scanned XAML, not added from C#. App-local style,
                         template, and converter keys are defined in the
                         app's own XAML and are therefore never reported.
  literal-size           a literal FontSize, Margin, Padding, CornerRadius,
                         or Height in XAML (attribute or Setter). Allowed:
                         0 in every component, Auto, NaN, and star sizes
                         (*, 2*), because they are layout-neutral; anything
                         else is a token reference
  font-family-literal    a FontFamily set to a literal in XAML, or
                         new FontFamily("...") in C#: families are tokens
  forbidden-framework    WPF-UI (Wpf.Ui, lepo.co) or FluentIcons usage
  emoji                  an emoji glyph in XAML text or a C# string: emoji
                         are never icons (standards/ui.md, Icons)
  backdrop               Mica, Acrylic, or a DWM system backdrop: docked
                         chrome is flat token surfaces

Files the theme generator writes (a header naming scripts/generate-theme.py
as generated) are skipped: they are the one place token values are literal.
Comments are ignored in both languages.

Legacy code (operator decision 2026-09-27: "Record existing violations,
fail new ones"): --baseline docs/design/.lint-baseline.json records the
violations of 2026-09-27 keyed by file, rule, and the normalized text of
the line (whitespace collapsed), with a count, so moving a line does not
break it. A run with --baseline passes recorded violations, fails every
new one, and fails a recorded entry that no longer occurs (stale: the
baseline only shrinks). --update-baseline rewrites the file removing
stale entries and never adds; --allow-add --reason "<text>" also adds the
current new violations and appends the reason to the file's history,
which requires a review-approved reason (review-todo-section records it
in the stamp). Every --baseline run also compares the file with HEAD: an
entry that grew without a new history entry carrying a reason, or an
edited history, fails. Warn-level findings never fail and are never
baselined.

Usage:
  python scripts/design-lint.py                               # every finding, exit 1 on any error
  python scripts/design-lint.py --baseline docs/design/.lint-baseline.json
  python scripts/design-lint.py --baseline docs/design/.lint-baseline.json --update-baseline
  python scripts/design-lint.py --baseline <file> --update-baseline --allow-add --reason "<review-approved reason>"
  python scripts/design-lint.py --summary --baseline <file>   # counts by rule
  python scripts/design-lint.py --self-test
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE = "docs/design/.lint-baseline.json"

WARN_RULES = {"unknown-resource-key"}

BRUSH_PROPS = {
    "Background", "Foreground", "BorderBrush", "Fill", "Stroke", "Color", "Brush", "CaretBrush",
    "SelectionBrush", "SelectionTextBrush", "OpacityMask", "GlowColor", "ShadowColor", "TextBrush",
    "HighlightBrush", "SeparatorBrush", "VerticalGridLinesBrush", "HorizontalGridLinesBrush",
    "AlternatingRowBackground", "RowBackground", "GridLinesBrush",
}
SIZE_PROPS = {"FontSize", "Margin", "Padding", "CornerRadius", "Height"}

# The WPF Colors class (System.Windows.Media.Colors), lower-cased.
NAMED_COLORS = {c.lower() for c in """
AliceBlue AntiqueWhite Aqua Aquamarine Azure Beige Bisque Black BlanchedAlmond Blue BlueViolet Brown
BurlyWood CadetBlue Chartreuse Chocolate Coral CornflowerBlue Cornsilk Crimson Cyan DarkBlue DarkCyan
DarkGoldenrod DarkGray DarkGreen DarkKhaki DarkMagenta DarkOliveGreen DarkOrange DarkOrchid DarkRed
DarkSalmon DarkSeaGreen DarkSlateBlue DarkSlateGray DarkTurquoise DarkViolet DeepPink DeepSkyBlue DimGray
DodgerBlue Firebrick FloralWhite ForestGreen Fuchsia Gainsboro GhostWhite Gold Goldenrod Gray Green
GreenYellow Honeydew HotPink IndianRed Indigo Ivory Khaki Lavender LavenderBlush LawnGreen LemonChiffon
LightBlue LightCoral LightCyan LightGoldenrodYellow LightGray LightGreen LightPink LightSalmon
LightSeaGreen LightSkyBlue LightSlateGray LightSteelBlue LightYellow Lime LimeGreen Linen Magenta Maroon
MediumAquamarine MediumBlue MediumOrchid MediumPurple MediumSeaGreen MediumSlateBlue MediumSpringGreen
MediumTurquoise MediumVioletRed MidnightBlue MintCream MistyRose Moccasin NavajoWhite Navy OldLace Olive
OliveDrab Orange OrangeRed Orchid PaleGoldenrod PaleGreen PaleTurquoise PaleVioletRed PapayaWhip
PeachPuff Peru Pink Plum PowderBlue Purple Red RosyBrown RoyalBlue SaddleBrown Salmon SandyBrown SeaGreen
SeaShell Sienna Silver SkyBlue SlateBlue SlateGray Snow SpringGreen SteelBlue Tan Teal Thistle Tomato
Turquoise Violet Wheat White WhiteSmoke Yellow YellowGreen
""".split()}

HEX_VALUE_RE = re.compile(r"^#(?:[0-9A-Fa-f]{3,4}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")
HEX_IN_TEXT_RE = re.compile(r"(?<![\w&#])#(?:[0-9A-Fa-f]{8}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3,4})(?![0-9A-Za-z])")
ATTR_RE = re.compile(r"(?P<prop>[A-Za-z_][\w.:]*)\s*=\s*\"(?P<val>[^\"]*)\"")
TAG_RE = re.compile(r"<(?P<name>[A-Za-z_][\w.:]*)(?P<attrs>(?:[^<>\"]|\"[^\"]*\")*)/?>")
ELEMENT_TEXT_RE = re.compile(r">(?P<text>[^<>]+)<")
RESOURCE_RE = re.compile(r"\{(?P<kind>StaticResource|DynamicResource)\s+(?:ResourceKey=)?(?P<key>[A-Za-z_][\w.\-]*)\s*\}")
KEY_DEF_RE = re.compile(r"<(?P<type>[A-Za-z_][\w.:]*)\b[^<>]*?\bx:Key\s*=\s*\"(?P<key>[^\"]+)\"")
CS_RESOURCE_ADD_RE = re.compile(r"Resources\s*(?:\[\s*\"(?P<a>[^\"]+)\"\s*\]\s*=|\.Add\(\s*\"(?P<b>[^\"]+)\")")
FORBIDDEN_RE = re.compile(r"(?:\bWpf\.Ui\b|schemas\.lepo\.co|\bwpfui\b|FluentIcons|FluentIcon\b|\bui:SymbolIcon\b)", re.IGNORECASE)
BACKDROP_RE = re.compile(r"\b(?:Mica(?:Alt)?|Acrylic\w*|SystemBackdrop\w*|WindowBackdropType|DWMWA_SYSTEMBACKDROP_TYPE|DWMSBT_\w+)\b")
CS_COLOR_API_RE = re.compile(
    r"\bColor\.From(?:Rgb|Argb|ScRgb)\s*\(|\b(?:Colors|Brushes)\.(?!Transparent\b)[A-Z]\w*|"
    r"\bnew\s+SolidColorBrush\s*\(\s*(?:Color\.|Colors\.|\(Color\)|ColorConverter)|\bColorConverter\.ConvertFromString\s*\("
)
CS_FONT_RE = re.compile(r"\bnew\s+FontFamily\s*\(\s*\"")
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0000231A-\U0000231B\U000023E9-\U000023FA"
    "\U0000FE0F\U0001F1E6-\U0001F1FF]"
)
GENERATED_MARK_RE = re.compile(r"generate-theme\.py", re.IGNORECASE)
NUMBER_LIST_RE = re.compile(r"^-?\d+(?:\.\d+)?(?:\s*[, ]\s*-?\d+(?:\.\d+)?){0,3}$")


# ---------------------------------------------------------------- inputs

def ui_projects(root: Path) -> list[Path]:
    """Directories of the UI projects: UseWPF true, not a test project."""
    out = []
    for proj in sorted((root / "src").rglob("*.csproj")):
        if any(part in ("bin", "obj") for part in proj.parts):
            continue
        try:
            text = proj.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not re.search(r"<UseWPF>\s*true\s*</UseWPF>", text, re.IGNORECASE):
            continue
        name = proj.stem
        if re.search(r"<IsTestProject>\s*true", text, re.IGNORECASE) or name.endswith(".Tests") or name.endswith("Tests"):
            continue
        out.append(proj.parent)
    return out


def source_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for d in ui_projects(root):
        for ext in ("*.xaml", "*.cs"):
            for f in d.rglob(ext):
                rel = f.relative_to(d).parts
                if any(p in ("bin", "obj") for p in rel):
                    continue
                if f.name.endswith((".g.cs", ".g.i.cs", ".Designer.cs", "AssemblyInfo.cs")):
                    continue
                files.add(f)
    return sorted(files)


def load_tokens(root: Path) -> tuple[set[str], set[str]]:
    """(color token names, every other allowed key) from docs/design/tokens.json."""
    path = root / "docs" / "design" / "tokens.json"
    colors: set[str] = set()
    others: set[str] = set()
    try:
        tj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return colors, others
    for t in tj.get("color", {}).get("tokens", []):
        colors.add(t["name"])
    for group in ("spacing", "radius", "shadow", "size", "duration"):
        for t in tj.get(group, {}).get("tokens", []):
            name = t["name"]
            others.add(name)
            for suffix in ("-compact", "-comfortable"):
                if name.endswith(suffix):
                    others.add(name[: -len(suffix)])  # the neutral density key
    for fam in tj.get("type", {}).get("families", {}):
        others.add(f"font-{fam}")
    for g in tj.get("type", {}).get("groups", []):
        for st in g.get("styles", []):
            others.add(f"type-{st['name']}")
    others.update({"type-caption", "type-body-compact", "type-body-comfortable", "type-title"})
    return colors, others


# ---------------------------------------------------------------- comment blanking

def blank_xml_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)


def split_cs(text: str) -> tuple[str, list[tuple[int, int]]]:
    """(text with comments blanked, spans of string and char literal contents)."""
    out = list(text)
    spans: list[tuple[int, int]] = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "/":
            j = text.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = " "
            i = j
            continue
        if c == "/" and nxt == "*":
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
            continue
        if text.startswith('"""', i):
            j = text.find('"""', i + 3)
            j = n if j < 0 else j
            spans.append((i + 3, j))
            i = j + 3
            continue
        if c == '"' or (c in "@$" and nxt == '"') or (c in "@$" and nxt in "@$" and i + 2 < n and text[i + 2] == '"'):
            verbatim = "@" in text[i:i + 2]
            start = text.find('"', i) + 1
            j = start
            while j < n:
                if verbatim and text[j] == '"' and j + 1 < n and text[j + 1] == '"':
                    j += 2
                    continue
                if not verbatim and text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"' or (not verbatim and text[j] == "\n"):
                    break
                j += 1
            spans.append((start, j))
            i = j + 1
            continue
        if c == "'":
            j = i + 1
            while j < n and text[j] != "'" and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            spans.append((i + 1, j))
            i = j + 1
            continue
        i += 1
    return "".join(out), spans


# ---------------------------------------------------------------- scanning

class Finding:
    __slots__ = ("file", "line", "rule", "message", "text")

    def __init__(self, file: str, line: int, rule: str, message: str, text: str):
        self.file, self.line, self.rule, self.message, self.text = file, line, rule, message, text

    @property
    def severity(self) -> str:
        return "warn" if self.rule in WARN_RULES else "error"

    def key(self) -> tuple[str, str, str]:
        return (self.file, self.rule, self.text)

    def render(self) -> str:
        msg = f"(warn) {self.message}" if self.severity == "warn" else self.message
        return f"{self.file}:{self.line}:{self.rule}:{msg}"


def _norm(line: str) -> str:
    return " ".join(line.split())


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _layout_neutral(val: str) -> bool:
    v = val.strip()
    if v in ("Auto", "NaN", "*") or re.fullmatch(r"\d*(?:\.\d+)?\*", v):
        return True
    if NUMBER_LIST_RE.match(v):
        return all(float(p) == 0 for p in re.split(r"[\s,]+", v) if p)
    return False


class Context:
    def __init__(self, root: Path):
        self.root = root
        self.color_tokens, self.other_tokens = load_tokens(root)
        self.files = source_files(root)
        self.defined: dict[str, str] = {}   # key -> defining element type
        self.cs_defined: set[str] = set()
        self.texts: dict[Path, str] = {}
        for f in self.files:
            try:
                raw = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            self.texts[f] = raw
            if f.suffix == ".xaml":
                for m in KEY_DEF_RE.finditer(blank_xml_comments(raw)):
                    self.defined.setdefault(m.group("key"), m.group("type").split(":")[-1])
            else:
                for m in CS_RESOURCE_ADD_RE.finditer(raw):
                    self.cs_defined.add(m.group("a") or m.group("b"))

    def is_colorish(self, key: str, prop: str | None) -> bool:
        if key in self.color_tokens or key.startswith("Photon.App."):
            return True
        kind = self.defined.get(key, "")
        if kind in ("Color", "SolidColorBrush", "LinearGradientBrush", "RadialGradientBrush", "Brush", "DrawingBrush"):
            return True
        if re.search(r"(?:Brush|Color)$", key):
            return True
        if prop in BRUSH_PROPS and not re.search(r"(?:Style|Template|Converter|Selector)$", key):
            return True
        return False

    def known(self, key: str) -> bool:
        return (key in self.color_tokens or key in self.other_tokens or key in self.defined
                or key in self.cs_defined or key.startswith("Photon."))


def _generated(raw: str) -> bool:
    head = "\n".join(raw.split("\n")[:8])
    return bool(GENERATED_MARK_RE.search(head)) and "generated" in head.lower()


def scan_xaml(ctx: Context, path: Path, rel: str, raw: str) -> list[Finding]:
    out: list[Finding] = []
    text = blank_xml_comments(raw)
    lines = raw.split("\n")

    def add(offset: int, rule: str, msg: str) -> None:
        ln = _line_of(text, offset)
        out.append(Finding(rel, ln, rule, msg, _norm(lines[ln - 1] if ln - 1 < len(lines) else "")))

    for tag in TAG_RE.finditer(text):
        name = tag.group("name")
        local = name.split(":")[-1]
        attrs = list(ATTR_RE.finditer(tag.group("attrs")))
        base = tag.start("attrs")
        amap = {a.group("prop"): a for a in attrs}
        setter_prop = None
        if local == "Setter" and "Property" in amap:
            setter_prop = amap["Property"].group("val").split(".")[-1]
        for a in attrs:
            full = a.group("prop")
            prop = full.split(".")[-1].split(":")[-1]
            val = a.group("val")
            off = base + a.start()
            if full.startswith("xmlns"):
                if FORBIDDEN_RE.search(val):
                    add(off, "forbidden-framework", f"`{full}` imports `{val}`; WPF-UI and FluentIcons leave the suite")
                continue
            eff_prop = setter_prop if (local == "Setter" and prop == "Value") else prop
            if HEX_VALUE_RE.match(val.strip()):
                add(off, "color-literal", f"`{full}=\"{val}\"` is a literal color; bind a color token through DynamicResource")
            elif eff_prop in BRUSH_PROPS and val.strip().lower() in NAMED_COLORS:
                add(off, "named-color", f"`{eff_prop}` is the named color `{val}`; bind a color token through DynamicResource")
            for r in RESOURCE_RE.finditer(val):
                key, kind = r.group("key"), r.group("kind")
                colorish = ctx.is_colorish(key, eff_prop)
                if kind == "StaticResource" and colorish:
                    add(off, "static-color-resource",
                        f"`{{StaticResource {key}}}` on `{eff_prop}` freezes a color; use DynamicResource")
                if colorish and key not in ctx.color_tokens and not key.startswith("Photon.App."):
                    add(off, "non-token-color",
                        f"`{key}` is a color or brush key that is not a color token of docs/design/tokens.json")
                elif not ctx.known(key):
                    add(off, "unknown-resource-key", f"`{key}` is defined nowhere the lint can see")
            if eff_prop in SIZE_PROPS and "{" not in val and not _layout_neutral(val):
                if NUMBER_LIST_RE.match(val.strip()):
                    add(off, "literal-size", f"`{eff_prop}=\"{val}\"` is a literal size; use a size, spacing, radius, or type token")
            if eff_prop == "FontFamily" and "{" not in val and val.strip():
                add(off, "font-family-literal", f"`FontFamily=\"{val}\"` is a literal family; use the font token")
            if EMOJI_RE.search(val):
                add(off, "emoji", f"`{full}` carries an emoji glyph; emoji are never icons, use the icon catalog")
            if BACKDROP_RE.search(val):
                add(off, "backdrop", f"`{full}=\"{val}\"` asks for a system backdrop; chrome is flat token surfaces")
        if FORBIDDEN_RE.search(name):
            add(tag.start(), "forbidden-framework", f"`<{name}>` is a WPF-UI or FluentIcons element")
        if BACKDROP_RE.search(local):
            add(tag.start(), "backdrop", f"`<{name}>` is a system backdrop; chrome is flat token surfaces")
    for m in ELEMENT_TEXT_RE.finditer(text):
        body = m.group("text")
        if not body.strip():
            continue
        off = m.start("text")
        stripped = body.strip()
        if HEX_VALUE_RE.match(stripped):
            add(off + body.index(stripped), "color-literal",
                f"element text `{stripped}` is a literal color; colors come from the generated token dictionaries")
        if EMOJI_RE.search(body):
            add(off + EMOJI_RE.search(body).start(), "emoji", "element text carries an emoji glyph; emoji are never icons")
    return out


def scan_cs(ctx: Context, path: Path, rel: str, raw: str) -> list[Finding]:
    out: list[Finding] = []
    code, spans = split_cs(raw)
    lines = raw.split("\n")

    def add(offset: int, rule: str, msg: str) -> None:
        ln = _line_of(raw, offset)
        out.append(Finding(rel, ln, rule, msg, _norm(lines[ln - 1] if ln - 1 < len(lines) else "")))

    # Code outside strings: blank string contents so API names inside strings do not match.
    code_only = list(code)
    for a, b in spans:
        for k in range(a, min(b, len(code_only))):
            if code_only[k] != "\n":
                code_only[k] = " "
    code_only_s = "".join(code_only)
    for m in CS_COLOR_API_RE.finditer(code_only_s):
        add(m.start(), "color-api", f"`{m.group(0).strip()}` builds a literal color; resolve a color token resource instead")
    for m in CS_FONT_RE.finditer(code):
        add(m.start(), "font-family-literal", "`new FontFamily(\"...\")` is a literal family; use the font token")
    for m in FORBIDDEN_RE.finditer(code_only_s):
        add(m.start(), "forbidden-framework", f"`{m.group(0)}` is WPF-UI or FluentIcons")
    for m in BACKDROP_RE.finditer(code_only_s):
        add(m.start(), "backdrop", f"`{m.group(0)}` asks for a system backdrop; chrome is flat token surfaces")
    for a, b in spans:
        s = raw[a:b]
        for m in HEX_IN_TEXT_RE.finditer(s):
            if HEX_VALUE_RE.match(m.group(0)):
                add(a + m.start(), "color-literal", f"string `{m.group(0)}` is a literal color; resolve a color token instead")
        e = EMOJI_RE.search(s)
        if e:
            add(a + e.start(), "emoji", "a string carries an emoji glyph; emoji are never icons, use the icon catalog")
    return out


def scan(root: Path) -> list[Finding]:
    ctx = Context(root)
    findings: list[Finding] = []
    for f, raw in ctx.texts.items():
        if _generated(raw):
            continue
        rel = f.relative_to(root).as_posix()
        if f.suffix == ".xaml":
            findings += scan_xaml(ctx, f, rel, raw)
        else:
            findings += scan_cs(ctx, f, rel, raw)
    findings.sort(key=lambda x: (x.file, x.line, x.rule, x.message))
    return findings


# ---------------------------------------------------------------- baseline

def load_baseline(path: Path) -> dict:
    if not path.exists():
        return {"schema": 1, "entries": [], "history": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != 1 or not isinstance(data.get("entries"), list):
        raise ValueError(f"{path}: not a schema 1 lint baseline")
    return data


def baseline_counts(data: dict) -> dict[tuple[str, str, str], int]:
    out: dict[tuple[str, str, str], int] = {}
    for e in data["entries"]:
        out[(e["file"], e["rule"], e["text"])] = out.get((e["file"], e["rule"], e["text"]), 0) + int(e.get("count", 1))
    return out


def compare(findings: list[Finding], data: dict) -> tuple[list[Finding], list[tuple[tuple[str, str, str], int]]]:
    """(new error findings, stale baseline entries with their surplus count)."""
    base = baseline_counts(data)
    seen: dict[tuple[str, str, str], int] = {}
    new: list[Finding] = []
    for f in findings:
        if f.severity != "error":
            continue
        k = f.key()
        seen[k] = seen.get(k, 0) + 1
        if seen[k] > base.get(k, 0):
            new.append(f)
    stale = [(k, n - seen.get(k, 0)) for k, n in sorted(base.items()) if n > seen.get(k, 0)]
    return new, stale


def write_baseline(path: Path, findings: list[Finding], data: dict, allow_add: bool, reason: str) -> tuple[int, int]:
    base = baseline_counts(data)
    cur: dict[tuple[str, str, str], int] = {}
    for f in findings:
        if f.severity == "error":
            cur[f.key()] = cur.get(f.key(), 0) + 1
    new_counts: dict[tuple[str, str, str], int] = {}
    removed = added = 0
    for k in set(base) | set(cur):
        b, c = base.get(k, 0), cur.get(k, 0)
        keep = min(b, c)
        if allow_add:
            keep = c
            added += max(0, c - b)
        removed += max(0, b - c)
        if keep:
            new_counts[k] = keep
    history = list(data.get("history", []))
    today = _dt.date.today().isoformat()
    if removed or added:
        entry = {"date": today, "removed": removed, "added": added}
        if added:
            entry["reason"] = reason
        history.append(entry)
    out = {
        "schema": 1,
        "note": data.get("note", "Recorded design-lint violations (standards/design-contract.md). Shrink-only: "
                                 "scripts/design-lint.py --update-baseline removes entries that no longer occur; "
                                 "adding needs --allow-add with a review-approved reason, recorded in history."),
        "entries": [
            {"file": k[0], "rule": k[1], "text": k[2], "count": n}
            for k, n in sorted(new_counts.items())
        ],
        "history": history,
    }
    # One entry per line: a shrink is a one-line diff per fixed violation.
    body = ",\n".join("  " + json.dumps(e, ensure_ascii=False) for e in out["entries"])
    text = ('{\n "schema": 1,\n "note": ' + json.dumps(out["note"], ensure_ascii=False) + ',\n "entries": [\n'
            + body + ("\n" if body else "") + ' ],\n "history": '
            + json.dumps(history, ensure_ascii=False) + "\n}\n")
    path.write_text(text, encoding="utf-8", newline=chr(10))
    return removed, added


# ---------------------------------------------------------------- CLI

def run(root: Path, args) -> int:
    findings = scan(root)
    errors = [f for f in findings if f.severity == "error"]
    warns = [f for f in findings if f.severity == "warn"]
    if args.summary:
        by: dict[str, int] = {}
        for f in findings:
            by[f.rule] = by.get(f.rule, 0) + 1
        for rule in sorted(by):
            print(f"{rule}: {by[rule]}")
    if not args.baseline:
        if not args.summary:
            for f in findings:
                print(f.render())
        print(f"design-lint: {len(errors)} error(s), {len(warns)} warning(s) in {len(Context(root).files)} file(s)")
        return 1 if errors else 0
    bpath = (root / args.baseline) if not Path(args.baseline).is_absolute() else Path(args.baseline)
    try:
        data = load_baseline(bpath)
    except (ValueError, KeyError) as e:
        print(f"design-lint: {e}")
        return 1
    if args.update_baseline:
        if args.allow_add and not (args.reason or "").strip():
            print("design-lint: --allow-add needs --reason \"<review-approved reason>\"; nothing written")
            return 1
        removed, added = write_baseline(bpath, findings, data, args.allow_add, args.reason or "")
        print(f"design-lint: baseline {bpath.relative_to(root).as_posix() if bpath.is_relative_to(root) else bpath}: "
              f"{removed} removed, {added} added")
        data = load_baseline(bpath)
    grown = head_growth(root, bpath, data)
    for g in grown:
        print(g)
    new, stale = compare(findings, data)
    if args.verbose:
        for f in warns:
            print(f.render())
    for f in new:
        print(f.render())
    for (file, rule, text), n in stale:
        print(f"{file}:0:{rule}:stale baseline entry (x{n}) no longer occurs: {text[:100]!r}; "
              "run --update-baseline to shrink the baseline")
    recorded = sum(baseline_counts(data).values())
    print(f"design-lint: {len(errors)} error(s) ({recorded} recorded in the baseline), {len(new)} new, "
          f"{len(stale)} stale, {len(warns)} warning(s)")
    return 1 if (new or stale or grown) else 0


def head_growth(root: Path, bpath: Path, data: dict, head_text: str | None = None) -> list[str]:
    """Problems with the baseline against the committed one: an entry that
    grew without a new history entry carrying a reason, or history that was
    edited. Skipped (no problems) when HEAD has no baseline or git is absent."""
    if head_text is None:
        try:
            import subprocess
            rel = bpath.relative_to(root).as_posix()
            res = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], capture_output=True, timeout=30)
            if res.returncode != 0:
                return []
            head_text = res.stdout.decode("utf-8")
        except Exception:
            return []
    try:
        head = json.loads(head_text)
    except ValueError:
        return []
    out: list[str] = []
    hist, head_hist = data.get("history", []), head.get("history", [])
    if hist[: len(head_hist)] != head_hist:
        out.append(f"{bpath.name}:0:baseline-history:the baseline history differs from HEAD; history is append-only")
    added_now = [h for h in hist[len(head_hist):] if h.get("added")]
    base, head_counts = baseline_counts(data), baseline_counts(head)
    grew = [k for k, n in base.items() if n > head_counts.get(k, 0)]
    if grew and not any(str(h.get("reason", "")).strip() for h in added_now):
        for k in grew[:20]:
            out.append(f"{k[0]}:0:{k[1]}:baseline entry added against HEAD without a history entry carrying a "
                       f"review-approved reason: {k[2][:100]!r}")
    return out


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    import tempfile

    cases: list[tuple[str, object, object]] = []

    def check(name, got, want):
        cases.append((name, got, want))

    with tempfile.TemporaryDirectory(prefix="design-lint-selftest-") as tmp:
        root = Path(tmp)
        (root / "docs" / "design").mkdir(parents=True)
        (root / "docs" / "design" / "tokens.json").write_text(json.dumps({
            "color": {"tokens": [{"name": "surface-panel"}, {"name": "text-primary"}]},
            "size": {"tokens": [{"name": "control-h-compact"}, {"name": "control-h-comfortable"}]},
            "spacing": {"tokens": [{"name": "space-2"}]},
            "type": {"families": {"sans": "x"}, "groups": [{"styles": [{"name": "body"}]}]},
        }), encoding="utf-8")
        app = root / "src" / "App"
        app.mkdir(parents=True)
        (app / "App.csproj").write_text("<Project><PropertyGroup><UseWPF>true</UseWPF></PropertyGroup></Project>", encoding="utf-8")
        tests = root / "src" / "App.Tests"
        tests.mkdir(parents=True)
        (tests / "App.Tests.csproj").write_text("<Project><PropertyGroup><UseWPF>true</UseWPF></PropertyGroup></Project>", encoding="utf-8")
        (tests / "Bad.xaml").write_text('<Border Background="#FF0000"/>\n', encoding="utf-8")
        (app / "obj").mkdir()
        (app / "obj" / "Gen.xaml").write_text('<Border Background="#FF0000"/>\n', encoding="utf-8")
        xaml = (
            '<Window xmlns:ui="http://schemas.lepo.co/wpfui/2022/xaml">\n'                    # 1 forbidden
            '  <Window.Resources>\n'
            '    <SolidColorBrush x:Key="Base">#1E1E2E</SolidColorBrush>\n'                    # 3 color-literal
            '    <Style x:Key="LocalStyle" TargetType="Button"/>\n'
            '  </Window.Resources>\n'
            '  <!-- <Border Background="#123456"/> -->\n'                                       # 6 comment: nothing
            '  <Border Background="{StaticResource Base}" Margin="0" Padding="0,0,0,0"/>\n'    # 7 static + non-token
            '  <Border Background="{DynamicResource surface-panel}" Height="Auto"/>\n'          # 8 clean
            '  <Border Background="White" BorderBrush="Transparent" Style="{StaticResource LocalStyle}"/>\n'  # 9 named
            '  <TextBlock FontSize="12" Margin="8,4" FontFamily="Segoe UI" Text="Done ✅"/>\n'   # 10 size x2, font, emoji
            '  <Setter Property="Background" Value="{StaticResource surface-panel}"/>\n'       # 11 static only
            '  <Setter Property="Height" Value="24"/>\n'                                       # 12 literal-size
            '  <Border Height="{DynamicResource control-h}" Width="100"/>\n'                   # 13 clean
            '  <Border Tag="{DynamicResource NoSuchKey}"/>\n'                                  # 14 warn unknown
            '  <RowDefinition Height="2*"/>\n'                                                 # 15 clean
            '  <ui:SymbolIcon Symbol="Home"/>\n'                                               # 16 forbidden element
            '</Window>\n'
        )
        (app / "Main.xaml").write_text(xaml, encoding="utf-8")
        cs = (
            "using Wpf.Ui.Controls;\n"                                                  # 1 forbidden
            "class A {\n"
            "  // var c = Colors.Red; Color.FromRgb(1,2,3);\n"                          # 3 comment: nothing
            "  void M() {\n"
            "    var b = new SolidColorBrush(Color.FromRgb(1, 2, 3));\n"                # 5 color-api x2
            "    var t = Brushes.Transparent;\n"                                         # 6 clean
            "    var s = \"#FF6B35\"; var e = \"✖ close\";\n"                        # 7 color-literal + emoji
            "    var f = new FontFamily(\"Segoe UI\");\n"                                 # 8 font
            "    var m = \"Colors.Red is fine in a string\";\n"                          # 9 clean
            "    Resources[\"FromCode\"] = null; /* Mica */\n"                            # 10 clean
            "    window.WindowBackdropType = 2;\n"                                        # 11 backdrop
            "  }\n}\n"
        )
        (app / "A.cs").write_text(cs, encoding="utf-8")
        (app / "Themes").mkdir()
        (app / "Themes" / "Dark.xaml").write_text(
            "<!-- Generated from docs/design/tokens.json by scripts/generate-theme.py. Do not hand-edit. -->\n"
            '<ResourceDictionary><SolidColorBrush x:Key="surface-panel" Color="#323232"/></ResourceDictionary>\n',
            encoding="utf-8")
        found = scan(root)
        got = sorted((f.file.split("/")[-1], f.line, f.rule) for f in found)
        want = sorted([
            ("Main.xaml", 1, "forbidden-framework"),
            ("Main.xaml", 3, "color-literal"),
            ("Main.xaml", 7, "static-color-resource"),
            ("Main.xaml", 7, "non-token-color"),
            ("Main.xaml", 9, "named-color"),
            ("Main.xaml", 10, "literal-size"),
            ("Main.xaml", 10, "literal-size"),
            ("Main.xaml", 10, "font-family-literal"),
            ("Main.xaml", 10, "emoji"),
            ("Main.xaml", 11, "static-color-resource"),
            ("Main.xaml", 12, "literal-size"),
            ("Main.xaml", 14, "unknown-resource-key"),
            ("Main.xaml", 16, "forbidden-framework"),
            ("A.cs", 1, "forbidden-framework"),
            ("A.cs", 5, "color-api"),
            ("A.cs", 7, "color-literal"),
            ("A.cs", 7, "emoji"),
            ("A.cs", 8, "font-family-literal"),
            ("A.cs", 11, "backdrop"),
        ])
        check("scan finds exactly the fixture's violations", got, want)
        check("test projects, obj/, and generated theme files are skipped",
              [f.file for f in found if "Tests" in f.file or "/obj/" in f.file or "Themes" in f.file], [])
        check("unknown-resource-key is warn-level",
              {f.severity for f in found if f.rule == "unknown-resource-key"}, {"warn"})
        check("render is file:line:rule:message",
              next(f.render() for f in found if f.rule == "backdrop").startswith("src/App/A.cs:11:backdrop:"), True)
        check("layout-neutral values", [_layout_neutral(v) for v in ("0", "0,0,0,0", "Auto", "*", "3*", "NaN", "4", "0,1")],
              [True, True, True, True, True, True, False, False])

        class A:  # argparse stand-in
            summary = False
            verbose = False
            update_baseline = False
            allow_add = False
            reason = ""
            baseline = "docs/design/.lint-baseline.json"

        import io
        import contextlib

        def _run(**kw) -> tuple[int, str]:
            a = A()
            for k, v in kw.items():
                setattr(a, k, v)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = run(root, a)
            return code, buf.getvalue()

        bl = root / "docs" / "design" / ".lint-baseline.json"
        code, out = _run()
        check("no baseline file: every error is new, exit 1", (code, "0 recorded" in out), (1, True))
        code, out = _run(update_baseline=True)
        check("--update-baseline never adds without --allow-add", (code, json.loads(bl.read_text())["entries"]), (1, []))
        code, out = _run(update_baseline=True, allow_add=True)
        check("--allow-add without a reason writes nothing", (code, "needs --reason" in out), (1, True))
        code, out = _run(update_baseline=True, allow_add=True, reason="fixture: record the legacy violations")
        data = json.loads(bl.read_text())
        check("--allow-add --reason records every error and the reason",
              (code, sum(e["count"] for e in data["entries"]), data["history"][-1]["reason"]),
              (0, 18, "fixture: record the legacy violations"))
        code, out = _run()
        check("recorded violations pass", (code, " 0 new, 0 stale" in out), (0, True))
        # Move a line: insert a blank line at the top of Main.xaml; keys are line text, not numbers.
        (app / "Main.xaml").write_text("\n" + xaml.replace("\n", "\n", 1), encoding="utf-8")
        code, out = _run()
        check("a moved line still matches its baseline entry", code, 0)
        # A new violation fails.
        (app / "Main.xaml").write_text(xaml.replace("</Window>", '  <Border Background="#00FF00"/>\n</Window>'), encoding="utf-8")
        code, out = _run()
        check("a new violation fails naming it", (code, ':color-literal:`Background="#00FF00"`' in out), (1, True))
        # A second copy of a recorded line is new too (counts, not presence).
        (app / "Main.xaml").write_text(xaml.replace("</Window>", '  <Setter Property="Height" Value="24"/>\n</Window>'), encoding="utf-8")
        code, out = _run()
        check("a second copy of a recorded line is new", (code, " 1 new" in out), (1, True))
        # A fixed violation leaves a stale entry, which fails until the baseline shrinks.
        (app / "Main.xaml").write_text(xaml.replace('    <SolidColorBrush x:Key="Base">#1E1E2E</SolidColorBrush>\n',
                                                    '    <SolidColorBrush x:Key="Base" Color="{DynamicResource surface-panel}"/>\n'),
                                       encoding="utf-8")
        code, out = _run()
        check("a fixed violation is a stale entry and fails", (code, "stale baseline entry" in out), (1, True))
        before = sum(e["count"] for e in json.loads(bl.read_text())["entries"])
        code, out = _run(update_baseline=True)
        after = sum(e["count"] for e in json.loads(bl.read_text())["entries"])
        check("--update-baseline removes the stale entry and passes", (code, before - after), (0, 1))
        check("the shrink is recorded in history", json.loads(bl.read_text())["history"][-1]["removed"], 1)
        # HEAD comparison: growth needs a new history entry with a reason; history is append-only.
        head = json.loads(bl.read_text())
        grown = json.loads(bl.read_text())
        grown["entries"].append({"file": "src/App/Main.xaml", "rule": "color-literal", "text": "<x/>", "count": 1})
        check("an entry added against HEAD without a reasoned history entry is refused",
              any("without a history entry" in p for p in head_growth(root, bl, grown, json.dumps(head))), True)
        grown["history"].append({"date": "2026-09-27", "removed": 0, "added": 1, "reason": "review-approved: fixture"})
        check("an entry added with a reasoned history entry passes", head_growth(root, bl, grown, json.dumps(head)), [])
        edited = json.loads(bl.read_text())
        edited["history"][0]["reason"] = "rewritten"
        check("an edited history entry is refused",
              any("append-only" in p for p in head_growth(root, bl, edited, json.dumps(head))), True)
        check("no HEAD baseline skips the comparison", head_growth(root, bl, grown), [])

    failed = [(n, g, w) for n, g, w in cases if g != w]
    for n, g, w in failed:
        print(f"design-lint self-test: FAIL {n}: got {g!r}, want {w!r}", file=sys.stderr)
    print(f"design-lint self-test: {len(cases)} cases, {len(failed)} failed")
    return 1 if failed else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=str(REPO), help="checkout root (default: this repository)")
    ap.add_argument("--baseline", help=f"recorded violations, e.g. {DEFAULT_BASELINE}")
    ap.add_argument("--update-baseline", action="store_true", help="rewrite the baseline, removing entries that no longer occur")
    ap.add_argument("--allow-add", action="store_true", help="with --update-baseline: also record new violations (needs --reason)")
    ap.add_argument("--reason", help="the review-approved reason recorded when --allow-add adds entries")
    ap.add_argument("--summary", action="store_true", help="print counts by rule")
    ap.add_argument("--verbose", action="store_true", help="with --baseline: also print warn-level findings")
    ap.add_argument("--self-test", action="store_true", help="run the fixture suite")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if (args.update_baseline or args.allow_add) and not args.baseline:
        ap.error("--update-baseline and --allow-add need --baseline")
    return run(Path(args.root).resolve(), args)


if __name__ == "__main__":
    sys.exit(main())
