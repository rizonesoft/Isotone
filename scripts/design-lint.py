#!/usr/bin/env python3
"""design-lint: the design contract's static gate over the native C and C++ sources.

standards/design-contract.md (operator decisions 2026-09-27 and 2026-10-22)
makes docs/design/ the source every surface implements 1:1: every color, size,
radius, spacing, font, and duration comes from docs/design/tokens.json through
the generated token tables. This script reads (never edits) every C and C++
source and header under native/ (.c, .cc, .cpp, .cxx, .c++, .h, .hh, .hpp,
.hxx, .h++, .inl, .ipp) and reports each departure in UI sources (native/ui/
and each app's UI folders) as

    <file>:<line>:<rule>:<message>

Rules:

  color-literal          a 6- or 8-digit hex color literal (0xRRGGBB or
                         0xAARRGGBB in code, or #RRGGBB / #AARRGGBB in a
                         string literal)
  named-color            a D2D1::ColorF:: or ColorF:: named color constant
  color-api              D2D1::ColorF / ColorF / D2D1_COLOR_F built from
                         numeric literals, or RGB( / RGBA( / PALETTERGB(
  literal-geometry       D2D1::RectF, SizeF, Point2F, RoundedRect (or their
                         D2D1_* C structs), or a corner radius, stroke width,
                         padding, margin, or spacing built from numeric
                         literals other than 0
  literal-size           a font size built from a numeric literal other than 0
                         (in CreateTextFormat or a font-size assignment/setter)
  font-family-literal    a literal font family string (in CreateTextFormat or
                         a font-family assignment/setter)
  emoji                  an emoji glyph in a string literal: emoji are never
                         icons (standards/ui.md, Icons)
  backdrop               Mica, Acrylic, or a DWM system backdrop: docked
                         chrome is flat token surfaces

Files the theme generator writes (a header naming scripts/generate-theme.py or
docs/design/tokens.json as generated) are skipped: they are the one place token
values are literal. Comments are ignored.

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

NATIVE_EXTS = (
    ".c", ".cc", ".cpp", ".cxx", ".c++",
    ".h", ".hh", ".hpp", ".hxx", ".h++",
    ".inl", ".ipp",
)
SKIP_DIRS = frozenset({"CMakeFiles", "vcpkg_installed", "build", "out"})
TEST_DIRS = frozenset({"tests", "test"})
UI_DIRS = frozenset({
    "ui", "views", "dialogs", "panels", "controls", "chrome", "shell", "windows",
    "widgets", "theme", "themes", "styles",
})

WARN_RULES: set[str] = set()

GENERATED_MARK_RE = re.compile(r"(?:generate-theme\.py|docs/design/tokens\.json)", re.IGNORECASE)
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0000231A-\U0000231B\U000023E9-\U000023FA"
    "\U0000FE0F\U0001F1E6-\U0001F1FF]"
)
BACKDROP_RE = re.compile(
    r"\b(?:Mica(?:Alt)?|Acrylic\w*|SystemBackdrop\w*|WindowBackdropType|DWMWA_SYSTEMBACKDROP_TYPE|DWMSBT_\w+)\b"
)
HEX_IN_STRING_RE = re.compile(r"(?<![\w&#])#(?:[0-9A-Fa-f]{8}|[0-9A-Fa-f]{6})(?![0-9A-Za-z])")
HEX_LITERAL_RE = re.compile(r"\b0[xX]([0-9A-Fa-f][0-9A-Fa-f']*[0-9A-Fa-f])[uUlL]*\b")
NAMED_COLOR_RE = re.compile(r"\b(?:D2D1::)?ColorF::(?:Enum::)?(?!ColorF\b|Enum\b)[A-Za-z_]\w*")
RGB_MACRO_RE = re.compile(r"\b(?:PALETTE)?RGB(?:A)?\s*\(")
COLORF_HEAD_RE = re.compile(
    r"\b(?:(?:D2D1::)?ColorF|D2D1_COLOR_F)"
    r"(?:\s+[A-Za-z_]\w*(?:\s*=\s*(?=\{))?)?\s*([({])"
)
CREATE_BRUSH_RE = re.compile(r"\bCreateSolidColorBrush\s*\(")
GEOM_TYPE_HEAD_RE = re.compile(
    r"\b(?:(?:D2D1::)?(?:RectF|RectU|RectL|SizeF|SizeU|Point2F|Point2U|Point2L|RoundedRect)"
    r"|D2D1_(?:RECT_F|RECT_U|RECT_L|SIZE_F|SIZE_U|POINT_2F|POINT_2U|POINT_2L|ROUNDED_RECT))"
    r"(?:\s+[A-Za-z_]\w*(?:\s*=\s*(?=\{))?)?\s*([({])"
)
D2D_DRAW_STROKE_RE = re.compile(
    r"\b(?P<fn>DrawLine|DrawRectangle|DrawRoundedRectangle|DrawEllipse|DrawGeometry)\s*\("
)
GEOM_PROP_ASSIGN_RE = re.compile(
    r"\b(?P<name>(?:[A-Za-z_]\w*_?)?(?:corner_?radius|radius(?:_[xy]|[XY])?|stroke_?width|border_?width"
    r"|padding(?:_(?:left|right|top|bottom|h|v|x|y))?"
    r"|margin(?:_(?:left|right|top|bottom|h|v|x|y))?"
    r"|spacing|item_?spacing|(?:row|col|column)_?gap|gap))"
    r"\s*(?:=\s*(?P<rhs>[^;,\n}]+)|\{\s*(?P<brace>[^;}\n]+)\})",
    re.IGNORECASE,
)
GEOM_PROP_CALL_RE = re.compile(
    r"\b(?P<name>set_?(?:corner_?radius|radius|stroke_?width|border_?width|padding|margin|spacing|gap)"
    r"|corner_?radius|stroke_?width|border_?width|padding|margin|insets|thickness|spacing)\s*([({])",
    re.IGNORECASE,
)
FONT_SIZE_ASSIGN_RE = re.compile(
    r"\b(?P<name>(?:[A-Za-z_]\w*_?)?(?:font_?size|text_?size))"
    r"\s*(?:=\s*(?P<rhs>[^;,\n}]+)|\{\s*(?P<brace>[^;}\n]+)\})",
    re.IGNORECASE,
)
FONT_SIZE_CALL_RE = re.compile(
    r"\b(?P<name>set_?(?:font_?size|text_?size)|font_?size|text_?size)\s*([({])",
    re.IGNORECASE,
)
FONT_FAMILY_ASSIGN_RE = re.compile(
    r"\b(?P<name>(?:[A-Za-z_]\w*_?)?(?:font_?family|family_?name))"
    r"\s*(?:=|\{)\s*(?:L|u8|u|U)?\"(?P<val>[^\"]+)\"",
    re.IGNORECASE,
)
FONT_FAMILY_CALL_RE = re.compile(
    r"\b(?P<name>set_?font_?family|font_?family)\s*[({]\s*(?:L|u8|u|U)?\"(?P<val>[^\"]+)\"",
    re.IGNORECASE,
)
CREATE_TEXT_FORMAT_RE = re.compile(r"\bCreateTextFormat\s*\(")
STRING_TOKEN_RE = re.compile(r"(?:L|u8|u|U|R)?\"")
NUM_LITERAL_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:0[xX][0-9A-Fa-f']+|\d[\d']*(?:\.[\d']*)?|\.[\d']+)(?:[eE][+-]?[\d']+)?[fFlLuU]*"
)


# ---------------------------------------------------------------- inputs

def _has_native_ext(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(ext) for ext in NATIVE_EXTS)


def source_files(root: Path) -> list[Path]:
    """Every C and C++ source and header under native/."""
    native_root = root / "native"
    if not native_root.exists():
        return []
    files: list[Path] = []
    for f in sorted(native_root.rglob("*")):
        if not f.is_file() or not _has_native_ext(f):
            continue
        rel_parts = f.relative_to(native_root).parts
        if any(p in SKIP_DIRS for p in rel_parts):
            continue
        files.append(f)
    return files


def is_ui_source(rel: str) -> bool:
    """True when `rel` (POSIX path from repo root) is in native/ui/ or an app's UI folders."""
    parts = Path(rel).parts
    if len(parts) < 2 or parts[0] != "native":
        return False
    if any(p.lower() in TEST_DIRS for p in parts[1:]):
        return False
    if parts[1].lower() == "ui":
        return True
    if parts[1].lower() == "core":
        return False
    return any(p.lower() in UI_DIRS for p in parts[1:-1])


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
                    others.add(name[: -len(suffix)])
    for fam in tj.get("type", {}).get("families", {}):
        others.add(f"font-{fam}")
    for g in tj.get("type", {}).get("groups", []):
        for st in g.get("styles", []):
            others.add(f"type-{st['name']}")
    others.update({"type-caption", "type-body-compact", "type-body-comfortable", "type-title"})
    return colors, others


# ---------------------------------------------------------------- comment & string splitting

def split_cpp(text: str) -> tuple[str, list[tuple[int, int]]]:
    """Return (text with comments blanked, spans of string literal contents)."""
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
        # C++ raw string literal: R"delim(...)delim"
        if c == "R" and nxt == '"':
            paren = text.find("(", i + 2)
            if 0 <= paren <= i + 18 and "\n" not in text[i + 2:paren]:
                delim = text[i + 2:paren]
                close_seq = f"){delim}\""
                end = text.find(close_seq, paren + 1)
                if end < 0:
                    end = n
                spans.append((paren + 1, end))
                i = min(n, end + len(close_seq))
                continue
        if c == '"':
            start = i + 1
            j = start
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"' or text[j] == "\n":
                    break
                j += 1
            spans.append((start, j))
            i = j + 1
            continue
        if c == "'":
            # C++14 digit separator: e.g. 0xFF'1E'2E or 1'000
            prev_ch = text[i - 1] if i > 0 else ""
            if (prev_ch.isalnum() or prev_ch == "_") and nxt.isalnum():
                i += 1
                continue
            j = i + 1
            while j < n and text[j] != "'" and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            i = j + 1
            continue
        i += 1
    return "".join(out), spans


def _balanced_body(text: str, open_pos: int) -> tuple[str, int]:
    """Given the index of '(' or '{', return (inner slice, close index)."""
    opener = text[open_pos]
    closer = ")" if opener == "(" else "}"
    depth = 1
    i = open_pos + 1
    n = len(text)
    while i < n and depth > 0:
        ch = text[i]
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[open_pos + 1:i], i
        i += 1
    return text[open_pos + 1:], n


def _split_top_level_args(arg_text: str) -> list[str]:
    """Split a call's inner text on top-level commas."""
    parts: list[str] = []
    cur: list[str] = []
    depth = 0
    for ch in arg_text:
        if ch in "({[":
            depth += 1
        elif ch in ")}]" and depth > 0:
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _numeric_literals(expr: str) -> list[str]:
    return [m.group(0) for m in NUM_LITERAL_RE.finditer(expr)]


def _is_zero_literal(tok: str) -> bool:
    s = tok.replace("'", "").rstrip("fFlLuU")
    try:
        if s.lower().startswith("0x"):
            return int(s, 16) == 0
        return float(s) == 0.0
    except ValueError:
        return False


def _has_nonzero_literal(expr: str) -> bool:
    return any(not _is_zero_literal(tok) for tok in _numeric_literals(expr))


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


class Context:
    def __init__(self, root: Path):
        self.root = root
        self.color_tokens, self.other_tokens = load_tokens(root)
        self.files = source_files(root)
        self.texts: dict[Path, str] = {}
        for f in self.files:
            try:
                self.texts[f] = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue


def _generated(raw: str) -> bool:
    head = "\n".join(raw.split("\n")[:12])
    return bool(GENERATED_MARK_RE.search(head)) and "generated" in head.lower()


def scan_cpp(ctx: Context, path: Path, rel: str, raw: str) -> list[Finding]:
    if not is_ui_source(rel):
        return []
    out: list[Finding] = []
    code, spans = split_cpp(raw)
    lines = raw.split("\n")

    def add(offset: int, rule: str, msg: str) -> None:
        ln = _line_of(raw, offset)
        out.append(Finding(rel, ln, rule, msg, _norm(lines[ln - 1] if ln - 1 < len(lines) else "")))

    # Blank string literal contents in `code_only_s` so identifiers inside strings do not match code rules.
    code_only = list(code)
    for a, b in spans:
        for k in range(max(0, a - 1), min(b + 1, len(code_only))):
            if code_only[k] != "\n":
                code_only[k] = " "
    code_only_s = "".join(code_only)

    # 1. Named colors: D2D1::ColorF::Red, ColorF::White, etc.
    for m in NAMED_COLOR_RE.finditer(code_only_s):
        add(m.start(), "named-color",
            f"`{m.group(0)}` is a named color constant; resolve a color token from the generated token tables")

    # 2. Color APIs: D2D1::ColorF / D2D1_COLOR_F / CreateSolidColorBrush built from numeric literals, and RGB( / RGBA(
    colorf_spans: list[tuple[int, int]] = []
    for m in COLORF_HEAD_RE.finditer(code_only_s):
        open_pos = m.start(1)
        body, end_pos = _balanced_body(code_only_s, open_pos)
        if _numeric_literals(body):
            colorf_spans.append((m.start(), end_pos))
            snippet = _norm(code[m.start(): min(end_pos + 1, len(code))])
            add(m.start(), "color-api",
                f"`{snippet}` builds a literal color from numbers; resolve a color token from the generated token tables")
    for m in CREATE_BRUSH_RE.finditer(code_only_s):
        open_paren = m.end() - 1
        body_clean, end_pos = _balanced_body(code_only_s, open_paren)
        args_clean = _split_top_level_args(body_clean)
        if args_clean and _numeric_literals(args_clean[0]) and not any(a <= m.start() <= b or m.start() <= a <= end_pos for a, b in colorf_spans):
            colorf_spans.append((m.start(), end_pos))
            add(m.start(), "color-api",
                "`CreateSolidColorBrush` builds a literal color from numbers; resolve a color token from the generated token tables")
    for m in RGB_MACRO_RE.finditer(code_only_s):
        add(m.start(), "color-api",
            f"`{m.group(0).strip()}` builds a literal color; resolve a color token from the generated token tables")

    # 3. 6- or 8-digit hex color literals in code (outside ColorF calls already reported above)
    for m in HEX_LITERAL_RE.finditer(code_only_s):
        digits = m.group(1).replace("'", "")
        if len(digits) in (6, 8) and not any(a <= m.start() <= b for a, b in colorf_spans):
            add(m.start(), "color-literal",
                f"`{m.group(0)}` is a {len(digits)}-digit hex color literal; resolve a color token instead")

    # 4. Literal geometry: D2D1::RectF, SizeF, Point2F, RoundedRect (and D2D1_* structs) with non-zero numeric literals
    for m in GEOM_TYPE_HEAD_RE.finditer(code_only_s):
        body, end_pos = _balanced_body(code_only_s, m.start(1))
        if _has_nonzero_literal(body):
            snippet = _norm(code[m.start(): min(end_pos + 1, len(code))])
            add(m.start(), "literal-geometry",
                f"`{snippet}` builds geometry from a non-zero numeric literal; use a size, spacing, or radius token")
    for m in D2D_DRAW_STROKE_RE.finditer(code_only_s):
        open_paren = m.end() - 1
        body_clean, _ = _balanced_body(code_only_s, open_paren)
        args_clean = _split_top_level_args(body_clean)
        stroke_idx = 3 if m.group("fn") == "DrawLine" else 2
        if len(args_clean) > stroke_idx and _has_nonzero_literal(args_clean[stroke_idx]):
            add(m.start(), "literal-geometry",
                f"`{m.group('fn')}` uses a literal stroke width; resolve a size token instead")

    # Corner radius, stroke width, padding, margin, or spacing built from numeric literals other than 0
    for m in GEOM_PROP_ASSIGN_RE.finditer(code_only_s):
        rhs = m.group("rhs") or m.group("brace") or ""
        if _has_nonzero_literal(rhs):
            add(m.start(), "literal-geometry",
                f"`{m.group('name')}` is set from a non-zero numeric literal; use a size, spacing, or radius token")
    for m in GEOM_PROP_CALL_RE.finditer(code_only_s):
        body, _ = _balanced_body(code_only_s, m.start(2))
        if _has_nonzero_literal(body):
            add(m.start(), "literal-geometry",
                f"`{m.group('name')}(...)` is called with a non-zero numeric literal; use a size, spacing, or radius token")

    # 5. Literal font family and font size
    for m in CREATE_TEXT_FORMAT_RE.finditer(code):
        open_paren = m.end() - 1
        body_code, _ = _balanced_body(code, open_paren)
        body_clean, _ = _balanced_body(code_only_s, open_paren)
        args_code = _split_top_level_args(body_code)
        args_clean = _split_top_level_args(body_clean)
        if args_code and STRING_TOKEN_RE.search(args_code[0]):
            add(m.start(), "font-family-literal",
                "`CreateTextFormat` uses a literal font family; resolve a font family token instead")
        if len(args_clean) >= 6 and _has_nonzero_literal(args_clean[5]):
            add(m.start(), "literal-size",
                "`CreateTextFormat` uses a literal font size; resolve a type size token instead")

    for m in FONT_FAMILY_ASSIGN_RE.finditer(code):
        add(m.start(), "font-family-literal",
            f"`{m.group('name')}` is set to literal family `\"{m.group('val')}\"`; use a font token")
    for m in FONT_FAMILY_CALL_RE.finditer(code):
        add(m.start(), "font-family-literal",
            f"`{m.group('name')}` is called with literal family `\"{m.group('val')}\"`; use a font token")

    for m in FONT_SIZE_ASSIGN_RE.finditer(code_only_s):
        rhs = m.group("rhs") or m.group("brace") or ""
        if _has_nonzero_literal(rhs):
            add(m.start(), "literal-size",
                f"`{m.group('name')}` is set from a non-zero numeric literal; use a type size token")
    for m in FONT_SIZE_CALL_RE.finditer(code_only_s):
        body, _ = _balanced_body(code_only_s, m.start(2))
        if _has_nonzero_literal(body):
            add(m.start(), "literal-size",
                f"`{m.group('name')}(...)` is called with a non-zero numeric literal; use a type size token")

    # 6. System backdrops
    for m in BACKDROP_RE.finditer(code_only_s):
        add(m.start(), "backdrop",
            f"`{m.group(0)}` asks for a system backdrop; chrome is flat token surfaces")

    # 7. String literals: 6- or 8-digit hex color strings and emoji glyphs
    for a, b in spans:
        s = raw[a:b]
        for m in HEX_IN_STRING_RE.finditer(s):
            add(a + m.start(), "color-literal",
                f"string `{m.group(0)}` is a literal hex color; resolve a color token instead")
        e = EMOJI_RE.search(s)
        if e:
            add(a + e.start(), "emoji",
                "a string carries an emoji glyph; emoji are never icons, use the icon catalog")

    return out


def scan(root: Path) -> list[Finding]:
    ctx = Context(root)
    findings: list[Finding] = []
    for f, raw in ctx.texts.items():
        if _generated(raw):
            continue
        rel = f.relative_to(root).as_posix()
        findings += scan_cpp(ctx, f, rel, raw)
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
    import contextlib
    import io
    import tempfile

    cases: list[tuple[str, object, object]] = []

    def check(name: str, got: object, want: object) -> None:
        cases.append((name, got, want))

    with tempfile.TemporaryDirectory(prefix="design-lint-selftest-") as tmp:
        root = Path(tmp)
        (root / "docs" / "design").mkdir(parents=True)
        (root / "docs" / "design" / "tokens.json").write_text(json.dumps({
            "color": {"tokens": [{"name": "surface-panel"}, {"name": "text-primary"}]},
            "size": {"tokens": [{"name": "control-h-compact"}, {"name": "control-h-comfortable"}]},
            "spacing": {"tokens": [{"name": "space-2"}]},
            "radius": {"tokens": [{"name": "radius-md"}]},
            "type": {"families": {"sans": "x"}, "groups": [{"styles": [{"name": "body"}]}]},
        }), encoding="utf-8")

        ui_dir = root / "native" / "ui"
        ui_dir.mkdir(parents=True)
        app_ui_dir = root / "native" / "stilus" / "ui"
        app_ui_dir.mkdir(parents=True)
        core_dir = root / "native" / "core" / "src"
        core_dir.mkdir(parents=True)
        test_dir = root / "native" / "tests"
        test_dir.mkdir(parents=True)

        # Non-UI core and test files are scanned into Context.files but exempt from UI surface rules.
        (core_dir / "math.cpp").write_text("int k = 0x1E1E2E;\n", encoding="utf-8")
        (test_dir / "ui_test.cpp").write_text("auto c = D2D1::ColorF(0.2f, 0.4f, 0.8f);\n", encoding="utf-8")

        # Generated token table file is skipped.
        (ui_dir / "generated_tokens.hpp").write_text(
            "// Generated from docs/design/tokens.json by scripts/generate-theme.py. Do not edit.\n"
            "inline constexpr auto kPanel = D2D1::ColorF(0.2f, 0.2f, 0.2f);\n",
            encoding="utf-8",
        )

        # Cover every C/C++ extension CMake compiles plus included implementation files:
        # .c, .cc, .cpp, .cxx, .c++, .h, .hh, .hpp, .hxx, .h++, .inl, .ipp
        ext_probes: list[tuple[Path, str, str]] = [
            (ui_dir / "probe_c.c", "unsigned long c = RGB(30, 30, 46);\n", "color-api"),
            (ui_dir / "probe_cc.cc", "auto r = D2D1::RectF(0, 0, 24, 24);\n", "literal-geometry"),
            (ui_dir / "probe_cpp.cpp", "auto c = D2D1::ColorF(0.2f, 0.4f, 0.8f);\n", "color-api"),
            (ui_dir / "probe_cxx.cxx", "D2D1_COLOR_F raw_c{0.1f, 0.2f, 0.3f, 1.0f};\n", "color-api"),
            (ui_dir / "probe_cpp_plus.c++", "uint32_t hex6 = 0x1E1E2E;\n", "color-literal"),
            (ui_dir / "probe_h.h", "uint32_t hex8 = 0xFF1E1E2E;\n", "color-literal"),
            (ui_dir / "probe_hh.hh", "const char* css = \"#1E1E2E\";\n", "color-literal"),
            (ui_dir / "probe_hpp.hpp", "auto sz = D2D1::SizeF(120.0f, 28.0f);\n", "literal-geometry"),
            (ui_dir / "probe_hxx.hxx", "auto pt = D2D1::Point2F(8.0f, 12.0f);\n", "literal-geometry"),
            (ui_dir / "probe_hpp_plus.h++", "auto rr = D2D1::RoundedRect(bounds, 4.0f, 4.0f);\n", "literal-geometry"),
            (ui_dir / "probe_inl.inl", "auto named = D2D1::ColorF(D2D1::ColorF::Red);\n", "named-color"),
            (app_ui_dir / "probe_ipp.ipp", "float padding = 8.0f;\n", "literal-geometry"),
        ]
        for path, body, _ in ext_probes:
            path.write_text(body, encoding="utf-8")

        # Comprehensive UI fixture covering remaining literal kinds AND passing token forms.
        panel_cpp = (
            "// D2D1::ColorF(1.0f, 0.0f, 0.0f); /* 0xFF0000 D2D1::RectF(0, 0, 10, 10) */\n"  # 1 comment: clean
            "void draw_panel() {\n"
            "  auto ok_col = tokens.color(ColorToken::SurfacePanel);\n"                       # 3 token color: clean
            "  auto ok_zero = D2D1::RectF(0, 0, 0, 0);\n"                                     # 4 zero rect: clean
            "  auto ok_rect = D2D1::RectF(0.0f, 0.0f, tokens.size(SizeToken::ControlH), tokens.size(SizeToken::ControlH));\n"  # 5 token rect: clean
            "  auto ok_pt = D2D1::Point2F(tokens.space(SpaceToken::Space2), 0.0f);\n"         # 6 token point: clean
            "  auto ok_rr = D2D1::RoundedRect(ok_rect, tokens.radius(RadiusToken::Md), tokens.radius(RadiusToken::Md));\n"  # 7 token rounded: clean
            "  float corner_radius = tokens.radius(RadiusToken::Md);\n"                       # 8 token radius: clean
            "  float stroke_width = tokens.size(SizeToken::Hairline);\n"                      # 9 token stroke: clean
            "  float margin = 0.0f;\n"                                                        # 10 zero margin: clean
            "  float spacing = tokens.space(SpaceToken::Space2);\n"                           # 11 token spacing: clean
            "  dwrite->CreateTextFormat(tokens.font_family(FontToken::Sans), nullptr, w, s, st, tokens.font_size(TypeToken::Body), L\"en-us\", &fmt);\n"  # 12 token font: clean
            "  float corner_radius = 4.0f;\n"                                                 # 13 literal-geometry
            "  float stroke_width = 1.5f;\n"                                                  # 14 literal-geometry
            "  float margin = 12.0f;\n"                                                       # 15 literal-geometry
            "  float spacing = 6.0f;\n"                                                       # 16 literal-geometry
            "  dwrite->CreateTextFormat(L\"Segoe UI\", nullptr, w, s, st, 12.0f, L\"en-us\", &fmt);\n"  # 17 font-family-literal + literal-size
            "  const wchar_t* font_family = L\"Inter\";\n"                                    # 18 font-family-literal
            "  float font_size = 14.0f;\n"                                                    # 19 literal-size
            "  const char* bad_emoji = \"Done ✅\";\n"                                         # 20 emoji
            "  int bd = DWMWA_SYSTEMBACKDROP_TYPE;\n"                                         # 21 backdrop
            "  D2D1::ColorF copy_c = {0.2f, 0.4f, 0.8f};\n"                                   # 22 color-api
            "  float strokeWidth = 1.5f;\n"                                                   # 23 literal-geometry
            "  const wchar_t* fontFamily = L\"Inter\";\n"                                     # 24 font-family-literal
            "  float fontSize = 14.0f;\n"                                                     # 25 literal-size
            "}\n"
        )
        (ui_dir / "panel.cpp").write_text(panel_cpp, encoding="utf-8")

        found = scan(root)
        by_file_rule = {(Path(f.file).name, f.line, f.rule) for f in found}
        for path, _, expected_rule in ext_probes:
            check(f"extension {path.suffix} scanned and flagged ({expected_rule})",
                  (path.name, 1, expected_rule) in by_file_rule, True)

        panel_got = sorted((f.line, f.rule) for f in found if Path(f.file).name == "panel.cpp")
        panel_want = sorted([
            (13, "literal-geometry"),
            (14, "literal-geometry"),
            (15, "literal-geometry"),
            (16, "literal-geometry"),
            (17, "font-family-literal"),
            (17, "literal-size"),
            (18, "font-family-literal"),
            (19, "literal-size"),
            (20, "emoji"),
            (21, "backdrop"),
            (22, "color-api"),
            (23, "literal-geometry"),
            (24, "font-family-literal"),
            (25, "literal-size"),
        ])
        check("panel.cpp flags every literal kind and passes every token form", panel_got, panel_want)
        check("non-UI core, tests, and generated token files produce no findings",
              [f.file for f in found if "core/" in f.file or "tests/" in f.file or "generated_tokens" in f.file],
              [])
        check("render is file:line:rule:message",
              next(f.render() for f in found if f.rule == "backdrop").startswith("native/ui/panel.cpp:21:backdrop:"),
              True)

        class A:
            summary = False
            verbose = False
            update_baseline = False
            allow_add = False
            reason = ""
            baseline = "docs/design/.lint-baseline.json"

        def _run(**kw) -> tuple[int, str]:
            a = A()
            for k, v in kw.items():
                setattr(a, k, v)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = run(root, a)
            return code, buf.getvalue()

        total_errors = len(found)
        bl = root / "docs" / "design" / ".lint-baseline.json"
        code, out = _run()
        check("no baseline file: every error is new, exit 1", (code, "0 recorded" in out), (1, True))
        code, out = _run(update_baseline=True)
        check("--update-baseline never adds without --allow-add", (code, json.loads(bl.read_text())["entries"]), (1, []))
        code, out = _run(update_baseline=True, allow_add=True)
        check("--allow-add without a reason writes nothing", (code, "needs --reason" in out), (1, True))
        code, out = _run(update_baseline=True, allow_add=True, reason="fixture: record violations")
        data = json.loads(bl.read_text())
        check("--allow-add --reason records every error and the reason",
              (code, sum(e["count"] for e in data["entries"]), data["history"][-1]["reason"]),
              (0, total_errors, "fixture: record violations"))
        code, out = _run()
        check("recorded violations pass", (code, " 0 new, 0 stale" in out), (0, True))
        # Move a line: insert a blank line at the top of probe_cpp.cpp; keys are line text, not numbers.
        (ui_dir / "probe_cpp.cpp").write_text("\nauto c = D2D1::ColorF(0.2f, 0.4f, 0.8f);\n", encoding="utf-8")
        code, out = _run()
        check("a moved line still matches its baseline entry", code, 0)
        # A new violation fails.
        (ui_dir / "probe_cpp.cpp").write_text(
            "auto c = D2D1::ColorF(0.2f, 0.4f, 0.8f);\nauto c2 = D2D1::ColorF(0.9f, 0.1f, 0.1f);\n",
            encoding="utf-8",
        )
        code, out = _run()
        check("a new violation fails naming it", (code, ":color-api:" in out and "0.9f" in out), (1, True))
        # A fixed violation leaves a stale entry, which fails until the baseline shrinks.
        (ui_dir / "probe_cpp.cpp").write_text("auto c = tokens.color(ColorToken::SurfacePanel);\n", encoding="utf-8")
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
        grown["entries"].append({"file": "native/ui/x.cpp", "rule": "color-literal", "text": "int c = 0x112233;", "count": 1})
        check("an entry added against HEAD without a reasoned history entry is refused",
              any("without a history entry" in p for p in head_growth(root, bl, grown, json.dumps(head))), True)
        grown["history"].append({"date": "2026-11-09", "removed": 0, "added": 1, "reason": "review-approved: fixture"})
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Static design-contract lint over the native C and C++ UI sources.")
    ap.add_argument("--baseline", help="compare against (or update) a baseline JSON file")
    ap.add_argument("--update-baseline", action="store_true", help="shrink the baseline to the current violations")
    ap.add_argument("--allow-add", action="store_true", help="with --update-baseline, also record new violations")
    ap.add_argument("--reason", help="review-approved reason required with --allow-add")
    ap.add_argument("--summary", action="store_true", help="print rule counts")
    ap.add_argument("--verbose", action="store_true", help="also print warning findings in --baseline mode")
    ap.add_argument("--self-test", action="store_true", help="run the built-in self-test")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    return run(REPO, args)


if __name__ == "__main__":
    sys.exit(main())
