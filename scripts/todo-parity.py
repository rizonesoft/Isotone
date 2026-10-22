#!/usr/bin/env python3
"""The parity catalog checks (D00 T01 §6, §7): every competitor source id placed once, every status in the grammar.

    python scripts/todo-parity.py            # self-check: the source and catalog row counts on today's files

`docs/parity/` holds the competitor inventories under `sources/` and one catalog per app that merges their rows into
that app's features, each with exactly one status (`docs/parity/README.md`, "Status grammar"). The catalog is plan
data like `todo/`, so `scripts/todo-graph.py validate` runs `parity_findings` beside `budget_findings`, and `query
parity` reports what each phase of the plan owns. Stdlib only, like the rest of the TODO tooling; loaded by
`todo-graph.py` through `importlib`, so it imports nothing from it and takes the graph module as an argument.

Every finding is FATAL (`SEVERITY_MAP` in `scripts/todo-graph.py`, mirrored in `todo/README.md`):

- `parity-id-missing`: a source id no catalog row places.
- `parity-id-duplicate`: a source id two catalog rows place.
- `parity-id-unknown`: a catalog cell naming an id its source does not define, or a token that is no id.
- `parity-np-duplicate`: a Stilus catalog feature id (`NP-`) used on two rows.
- `parity-ip-duplicate`: a Gesso catalog feature id (`IP-`) used on two rows (D00 T01 §7).
- `parity-status-malformed`: a status outside the grammar.
- `parity-ref-dead`: a `plan` or `shipped-scope` ref naming no section, or a section carrying `> **Moved:**`.
- `parity-backlog-dead`: a `backlog B-NNN` id with no live entry in `todo/backlog.md`.
- `parity-input-damaged`: a catalog or source file the spec names is missing while `docs/parity/` exists, a row
  whose cell count differs from its table header, or a source id defined twice in one file. A damaged input never
  shrinks the denominator quietly: it fails naming the file and line.
- `parity-totals-drift`: the catalog's Totals table or Areas list disagrees with its rows, or is missing, repeated,
  or malformed in part (D00 T01 §7), so the summary a reader trusts is the one the rows add up to.

Every message opens with its catalog's name (`stilus:`, `gesso:`), since one validator reads every catalog. A tree
with no `docs/parity/` at all (a bare export of `todo/`) has nothing to check and validates; with `docs/parity/`
present, every configured catalog and inventory must be there.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# One catalog per app, and one spec per catalog: its path, its feature-id shape and the class a reused feature id
# raises, and `columns`, mapping each source column of the catalog to its inventory file and id shape. A column's id
# shape may cover more than one family in one file (Photoshop's `PS-A-` and `PS-B-`). D00 T01 §8 adds Albumen here.
CATALOGS = (
    {
        "app": "stilus",
        "path": "docs/parity/stilus-parity.md",
        "id": r"NP-\d{4}",
        "duplicate": "parity-np-duplicate",
        "columns": (
            {"column": "Illustrator", "path": "docs/parity/sources/illustrator-30.8.md", "id": r"AI-\d{4}"},
            {"column": "CorelDRAW", "path": "docs/parity/sources/coreldraw-2026.md", "id": r"CD-\d{3,4}"},
        ),
    },
    {
        "app": "gesso",
        "path": "docs/parity/gesso-parity.md",
        "id": r"IP-\d{4}",
        "duplicate": "parity-ip-duplicate",
        "columns": (
            {"column": "Photoshop", "path": "docs/parity/sources/photoshop-27.10.md", "id": r"PS-[AB]-\d{4}"},
            {"column": "Affinity", "path": "docs/parity/sources/affinity-3.3.md", "id": r"AF-\d{4}"},
            {"column": "GIMP", "path": "docs/parity/sources/gimp-3.2.6.md", "id": r"GP-\d{4}"},
        ),
    },
)

PARITY_CLASSES = (
    "parity-id-missing",
    "parity-id-duplicate",
    "parity-id-unknown",
    "parity-np-duplicate",
    "parity-ip-duplicate",
    "parity-status-malformed",
    "parity-ref-dead",
    "parity-backlog-dead",
    "parity-input-damaged",
    "parity-totals-drift",
)

STATUS_KINDS = ("plan", "shipped-scope", "backlog", "excluded", "other-app")
_REF = r"D\d{2} T\d{2} §\d+"
_STATUS_RES = (
    ("plan", re.compile(rf"^plan ({_REF})$")),
    ("shipped-scope", re.compile(rf"^shipped-scope ({_REF})$")),
    ("backlog", re.compile(r"^backlog (B-\d{3})$")),
    # The three reasons of docs/parity/README.md, each optionally explained (D00 T01 §7).
    ("excluded", re.compile(r"^excluded: ((?:cloud|platform|removed)(?: \S.*)?)$")),
    ("other-app", re.compile(r"^other-app: ((?:Stilus|Gesso|Albumen|none) \S.*)$")),
)
# A cell separator is a pipe no backslash escapes, so `a \| b` stays one cell.
_CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


def split_row(line: str) -> list[str]:
    """The cells of one Markdown table row, trimmed, without the outer pipes."""
    body = line.rstrip("\r\n").strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [cell.strip() for cell in _CELL_SPLIT_RE.split(body)]


def _id_prefix(id_re: str) -> str:
    """'AI-' for r'AI-\\d{4}': the literal family prefix every id of the family opens with."""
    return re.match(r"[A-Za-z]+-", id_re).group(0)


_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


def _table_rows(text: str, id_re: str):
    """(line number, cells, header, id_ok, problem) for every data row of an `| ID |` table, and for every other
    table row whose first cell mentions the family prefix of `id_re` (`AI-`, `CD-`, `NP-`).

    Rows are recognised by the table they sit in, not by what their first cell holds (independent review
    2026-10-21, rounds 1 to 5, found five row shapes a content match missed): every row between an `| ID |`
    header and the end of its table is a data row, whatever its first cell says; a header is the line that opens
    its table and is followed by a separator row with its cell count, the one separator skipped, and a table
    ends only at a blank line (a format rule for the parity files, stricter than GitHub Markdown on purpose). Outside such tables, a row whose first cell mentions the prefix in any case or
    markup is reported too. `id_ok` says the first cell is one whole id of the family. `problem` is None for a
    sound row, else the first defect: a first cell that is no whole id, no `| ID |` header for the row, a header
    that repeats a column name (a second `Status` would overwrite the first), or a cell count that differs from
    the header's.
    """
    mention = re.compile(re.escape(_id_prefix(id_re)), re.IGNORECASE)
    id_full = re.compile(rf"^{id_re}$")
    header: list[str] | None = None
    header_line = 0
    lines = text.splitlines()
    at_table_start = True
    for lineno, line in enumerate(lines, 1):
        # The format rule, not renderer emulation (independent review rounds 9 and 10 found pipe-free rows and
        # autolinks a block grammar mishandled): a parity table ends only at a blank line. Under an `| ID |` header
        # every other line is a row, pipe-free or not, so nothing written into a table can leave the count; a
        # heading or note set directly under a table reads as a damaged row until a blank line separates it.
        # Outside a table, a line with no pipe is prose and is never a row.
        if not line.strip() or ("|" not in line and header is None):
            header, at_table_start = None, True
            continue
        opens_table, at_table_start = at_table_start, False
        # A header opens its table and is followed by a separator row; an `ID` line anywhere else is a data row,
        # so it cannot swap the header mid-table and drop itself from the count (independent review round 6).
        following = lines[lineno] if lineno < len(lines) else ""
        if (opens_table and re.match(r"^\s*\|?\s*ID\s*\|", line) and _SEPARATOR_RE.match(following)
                and len(split_row(following)) == len(split_row(line))):
            header, header_line = split_row(line), lineno
            continue
        # Only the separator directly under the header is structure, and only when it has the header's cell
        # count; a separator-shaped line anywhere else is a data row (independent review round 7).
        if header is not None and lineno == header_line + 1:
            continue
        cells = split_row(line)
        if header is None and not mention.search(cells[0]):
            continue
        id_ok = id_full.match(cells[0]) is not None
        problem = None
        if not id_ok:
            problem = f"{cells[0]!r} is not a whole id of its family"
        elif header is None:
            problem = f"{cells[0]} has no `| ID |` header above it"
        elif len(set(header)) != len(header):
            repeated = sorted({h for h in header if header.count(h) > 1})
            problem = f"{cells[0]} sits under the header at line {header_line}, which repeats {', '.join(repeated)}"
        elif len(cells) != len(header):
            problem = f"{cells[0]} has {len(cells)} cells against the header's {len(header)}"
        yield lineno, cells, header, id_ok, problem


def _read(root: Path, rel: str) -> tuple[str | None, str]:
    """(text, "") for a readable UTF-8 file, else (None, why): a missing file and undecodable bytes alike are
    damaged input, never a traceback (independent review round 4)."""
    try:
        return (root / rel).read_text(encoding="utf-8"), ""
    except UnicodeDecodeError as error:
        return None, f"is not valid UTF-8 (byte {error.start})"
    except OSError as error:
        return None, f"cannot be read ({error.__class__.__name__})"


def snapshot(root: Path) -> dict[str, tuple[str | None, str]]:
    """Every file the catalogs name, read once: path -> (text, "") or (None, why).

    `parity_findings` and `parity_report` take one snapshot and work only from it, so a report never counts
    bytes other than the ones it validated, even while a file changes underneath (independent review round 8).
    """
    out: dict[str, tuple[str | None, str]] = {}
    for spec in CATALOGS:
        for rel in [spec["path"]] + [c["path"] for c in spec["columns"]]:
            if rel not in out:
                out[rel] = _read(root, rel)
    return out


def parse_sources(root: Path, column: dict, texts: dict | None = None) -> tuple[dict[str, int], list[tuple[str, str]]]:
    """(source id -> defining line, problems) for one inventory file."""
    text, why = texts[column["path"]] if texts is not None else _read(root, column["path"])
    if text is None:
        return {}, [("parity-input-damaged", f"{column['path']}: the {column['column']} inventory {why}; "
                                             f"restore it from git")]
    ids: dict[str, int] = {}
    problems: list[tuple[str, str]] = []
    for lineno, cells, _header, id_ok, problem in _table_rows(text, column["id"]):
        where = f"{column['path']}:{lineno}"
        if problem is not None:
            problems.append(("parity-input-damaged", f"{where}: {problem}; repair the row"))
        if not id_ok:
            continue
        # A damaged row with a whole id still defines it, so the id stays in the denominator and is reported
        # missing too when no catalog row places it.
        if cells[0] in ids:
            problems.append(("parity-input-damaged", f"{where}: {cells[0]} is defined again (first at line "
                                                     f"{ids[cells[0]]}); a source id is defined once"))
            continue
        ids[cells[0]] = lineno
    if not ids:
        problems.append(("parity-input-damaged", f"{column['path']}: the {column['column']} inventory has no "
                                                 f"{_id_prefix(column['id'])} rows; restore it from git"))
    return ids, problems


def parse_catalog(root: Path, spec: dict, texts: dict | None = None) -> tuple[list[dict], list[tuple[str, str]]]:
    """(rows, problems) for one catalog: each row's id, feature, source ids per column, category, status, notes."""
    text, why = texts[spec["path"]] if texts is not None else _read(root, spec["path"])
    if text is None:
        return [], [("parity-input-damaged", f"{spec['path']}: the {spec['app']} catalog {why}; restore it from git")]
    rows: list[dict] = []
    problems: list[tuple[str, str]] = []
    seen_any = False
    for lineno, cells, header, _id_ok, problem in _table_rows(text, spec["id"]):
        seen_any = True
        where = f"{spec['path']}:{lineno}"
        if problem is not None:
            problems.append(("parity-input-damaged", f"{where}: {problem}; repair the row"))
            continue
        named = dict(zip(header, cells))
        missing = [c for c in ("Feature", "Category", "Status", "Notes") if c not in named]
        missing += [c["column"] for c in spec["columns"] if c["column"] not in named]
        if missing:
            problems.append(("parity-input-damaged", f"{where}: the table header lacks {', '.join(missing)}"))
            continue
        sources = {}
        for c in spec["columns"]:
            value = named[c["column"]]
            sources[c["column"]] = [] if value in ("--", "") else [t.strip() for t in value.split(",")]
        rows.append({
            "id": cells[0], "line": lineno, "feature": named["Feature"], "sources": sources,
            "category": named["Category"], "status": named["Status"], "notes": named["Notes"],
        })
    if not seen_any:
        problems.append(("parity-input-damaged", f"{spec['path']}: the {spec['app']} catalog has no "
                                                 f"{_id_prefix(spec['id'])} rows; restore it from git"))
    return rows, problems


_NUMBER_RE = r"\**([0-9][0-9,]*)\**"
_TOTALS_HEADER = ["Status", "Features", "Source rows"]
_AREA_RE = re.compile(r"^- \[(?P<name>[^\]]+)\]\(#(?P<anchor>[^)\s]+)\) \((?P<n>[0-9][0-9,]*)\)$")


def _anchor(heading: str) -> str:
    """The anchor GitHub gives a heading's text: lower case, punctuation other than `-` and `_` dropped, each space a
    `-` ('3D (removed)' -> '3d-removed'), so an Areas link is checked against the section it must open."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def _anchors(lines: list[str]) -> dict[int, str]:
    """Line index -> anchor for every ATX heading, in document order: a slug already taken gets GitHub's `-1`,
    `-2`, ... suffix, so two headings whose text differs only in punctuation get different anchors (independent
    review round 2), and a link that opens the earlier one is not taken for the later."""
    out: dict[int, str] = {}
    used: dict[str, int] = {}
    for i, line in enumerate(lines):
        m = re.match(r"^#{1,6} +(.*?)\s*#*\s*$", line)
        if not m:
            continue
        base = _anchor(m.group(1))
        slug = base
        while slug in used:
            used[base] += 1
            slug = f"{base}-{used[base]}"
        used.setdefault(base, 0)
        used[slug] = used.get(slug, 0)
        out[i] = slug
    return out


def _count(text: str) -> int | None:
    """2385 for '2385', '2,385', or '**2,385**' (commas, when used, at every thousand, and at most nine digits, so a
    runaway number is malformed, never an integer conversion that fails: independent review round 1); None for
    anything else."""
    m = re.fullmatch(_NUMBER_RE, text.strip())
    if not m or not re.fullmatch(r"\d{1,9}|\d{1,3}(,\d{3}){1,2}", m.group(1)):
        return None
    return int(m.group(1).replace(",", ""))


def totals_findings(spec: dict, text: str, rows: list[dict]) -> list[tuple[str, str]]:
    """`parity-totals-drift` for one readable catalog with rows (D00 T01 §7): the Totals table (features and source
    rows per status kind and in all) and the Areas list (`- [Name](#anchor) (N)`, one per `## Name` heading that holds
    rows) must each be there exactly once, well formed, and equal to what the rows add up to. A part deleted, repeated,
    or malformed is drift too, so removing summary data never passes the reconciliation."""
    out: list[tuple[str, str]] = []
    where = spec["path"]

    def drift(msg: str) -> None:
        out.append(("parity-totals-drift", f"{where}: {msg}"))

    lines = text.splitlines()
    # What the rows add up to.
    want: dict[str, list[int]] = {kind: [0, 0] for kind in STATUS_KINDS}
    for row in rows:
        kind, _arg = parse_status(row["status"])
        if kind in want:
            want[kind][0] += 1
            want[kind][1] += sum(len(v) for v in row["sources"].values())
    want_total = [len(rows), sum(sum(len(v) for v in r["sources"].values()) for r in rows)]
    # The Totals table: the one whose header is exactly Status | Features | Source rows.
    tables = [i for i, line in enumerate(lines) if line.strip().startswith("|") and split_row(line) == _TOTALS_HEADER]
    if len(tables) != 1:
        drift(f"has {len(tables)} Totals tables (`| Status | Features | Source rows |`); it carries exactly one")
    else:
        seen: dict[str, int] = {}
        start = tables[0] + 1
        sep = lines[start] if start < len(lines) else ""
        # The line under the header must be its separator: anything else is a row, never skipped unread
        # (independent review round 1).
        if _SEPARATOR_RE.match(sep) and len(split_row(sep)) == 3:
            start += 1
        else:
            drift(f"Totals table at line {tables[0] + 1} has no separator row under its header")
        for lineno in range(start, len(lines)):
            line = lines[lineno]
            if not line.strip():
                break
            cells = split_row(line)
            label = cells[0].strip("`*")
            if len(cells) != 3 or label not in (*STATUS_KINDS, "Total") or not cells[0].strip("`*") or \
                    _count(cells[1]) is None or _count(cells[2]) is None:
                drift(f"Totals row at line {lineno + 1} ({line.strip()!r}) is not a status kind or Total with two counts")
                continue
            if label in seen:
                drift(f"Totals row `{label}` at line {lineno + 1} repeats the one at line {seen[label]}")
                continue
            seen[label] = lineno + 1
            got = [_count(cells[1]), _count(cells[2])]
            exp = want_total if label == "Total" else want[label]
            for col, g, e in zip(("Features", "Source rows"), got, exp):
                if g != e:
                    drift(f"Totals `{label}` {col} says {g:,} but the rows add up to {e:,}")
        for label in (*STATUS_KINDS, "Total"):
            if label not in seen:
                drift(f"Totals table has no `{label}` row")
    # The Areas list against the rows under each `## ` heading.
    heads = [(i, line[3:].strip()) for i, line in enumerate(lines) if line.startswith("## ")]
    anchors = _anchors(lines)
    anchor_of = {name: anchors.get(i, _anchor(name)) for i, name in reversed(heads)}
    first_head: dict[str, int] = {}
    for i, name in heads:
        # One section per area: two headings of one name would merge their rows under one Areas entry
        # (independent review round 1).
        if name in first_head:
            drift(f"area heading `{name}` at line {i + 1} repeats the one at line {first_head[name]}; "
                  f"each area has one section")
        else:
            first_head[name] = i + 1
    per_area: dict[str, int] = {}
    for row in rows:
        area = None
        for i, name in heads:
            if i < row["line"] - 1:
                area = name
        if area is None or area == "Areas":
            drift(f"{row['id']} (line {row['line']}) sits under no area heading")
            continue
        per_area[area] = per_area.get(area, 0) + 1
    starts = [i for i, name in heads if name == "Areas"]
    if len(starts) != 1:
        drift(f"has {len(starts)} `## Areas` lists; it carries exactly one")
        return out
    listed: dict[str, int] = {}
    for lineno in range(starts[0] + 1, len(lines)):
        line = lines[lineno]
        if line.startswith("## "):
            break
        if not line.strip():
            continue
        m = _AREA_RE.match(line.strip())
        if not m or _count(m.group("n")) is None:
            drift(f"Areas entry at line {lineno + 1} ({line.strip()!r}) is not `- [Name](#anchor) (N)`")
            continue
        name = m.group("name")
        if name in listed:
            drift(f"Areas entry `{name}` at line {lineno + 1} repeats the one at line {listed[name]}")
            continue
        listed[name] = lineno + 1
        want_anchor = anchor_of.get(name, _anchor(name))
        if m.group("anchor") != want_anchor:
            # The link must open the section it counts (independent review rounds 1 and 2).
            drift(f"Areas entry `{name}` (line {lineno + 1}) links #{m.group('anchor')}, but its heading's anchor "
                  f"is #{want_anchor}")
        n = _count(m.group("n"))
        if name not in per_area:
            drift(f"Areas entry `{name}` (line {lineno + 1}) names no area heading with rows")
        elif n != per_area[name]:
            drift(f"Areas entry `{name}` says {n:,} but its section holds {per_area[name]:,} rows")
    for name in per_area:
        if name not in listed:
            drift(f"area `{name}` holds {per_area[name]:,} rows but the Areas list has no entry for it")
    return out


def parse_status(text: str) -> tuple[str, str]:
    """(kind, argument) for a status in the grammar of `docs/parity/README.md`, else ("malformed", text)."""
    for kind, rx in _STATUS_RES:
        m = rx.match(text.strip())
        if m:
            return kind, m.group(1)
    return "malformed", text


def _section_index(todos) -> dict[str, tuple]:
    """'D02 T10 §7' -> (todo, section number, section) for every section in the tree."""
    out = {}
    for t in todos:
        dom = t.domain.split("-")[0]
        for num, s in t.sections.items():
            out[f"D{dom} T{t.number} §{num}"] = (t, num, s)
    return out


def _root(graph, root) -> Path:
    return Path(root) if root is not None else graph.TODO_DIR.parent


def parity_findings(graph, todos, root=None, texts: dict | None = None) -> list[tuple[str, str]]:
    """Every parity finding as (class, message); empty when the tree carries no `docs/parity/`."""
    root = _root(graph, root)
    parity = root / "docs" / "parity"
    if not parity.exists() and not parity.is_symlink():
        return []
    if not parity.is_dir():
        # Only true absence skips the check; a file or a dangling link where the folder belongs is damage
        # (independent review round 11).
        return [("parity-input-damaged", "docs/parity exists but is not a folder; restore it from git")]
    texts = texts if texts is not None else snapshot(root)
    sections = _section_index(todos)
    loaded = graph.load_backlog()
    backlog = {e["id"] for e in loaded[0]} if loaded is not None else set()
    out: list[tuple[str, str]] = []
    for spec in CATALOGS:
        # An unreadable file is one `parity-input-damaged` finding, never a cascade: a missing catalog places
        # nothing, so its sources' ids are not each reported missing, and a missing inventory defines nothing, so
        # the catalog's cells for it are not each reported unknown.
        found: list[tuple[str, str]] = []
        defined: dict[str, dict[str, int]] = {}
        readable: dict[str, bool] = {}
        for column in spec["columns"]:
            ids, problems = parse_sources(root, column, texts)
            defined[column["column"]] = ids
            readable[column["column"]] = texts[column["path"]][0] is not None
            found += problems
        rows, problems = parse_catalog(root, spec, texts)
        found += problems
        catalog_readable = texts[spec["path"]][0] is not None
        placed: dict[str, list[str]] = {}
        first_row: dict[str, int] = {}
        for row in rows:
            where = f"{spec['path']}:{row['line']}: {row['id']}"
            if row["id"] in first_row:
                found.append((spec["duplicate"], f"{where} is used again (first at line {first_row[row['id']]}); "
                                                 f"take the next free number"))
            else:
                first_row[row["id"]] = row["line"]
            kind, arg = parse_status(row["status"])
            if kind == "malformed":
                found.append(("parity-status-malformed", f"{where} has status {row['status']!r}, outside the grammar "
                                                       f"of docs/parity/README.md"))
            elif kind in ("plan", "shipped-scope"):
                hit = sections.get(" ".join(arg.split()))
                if hit is None:
                    found.append(("parity-ref-dead", f"{where} {kind} {arg} names no section in todo/"))
                elif hit[2].moved:
                    found.append(("parity-ref-dead", f"{where} {kind} {arg} names a section that moved out of the "
                                                   f"tree (`> **Moved:**`); point the row at its new owner"))
            elif kind == "backlog" and arg not in backlog:
                found.append(("parity-backlog-dead", f"{where} backlog {arg} names no live entry in todo/backlog.md"))
            for column in spec["columns"]:
                if not readable[column["column"]]:
                    continue
                shape = re.compile(rf"^{column['id']}$")
                for token in row["sources"][column["column"]]:
                    if not shape.match(token) or token not in defined[column["column"]]:
                        found.append(("parity-id-unknown", f"{where} places {token!r} in {column['column']}, which "
                                                         f"{column['path']} does not define"))
                        continue
                    placed.setdefault(token, []).append(f"{row['id']} (line {row['line']})")
        for column in spec["columns"] if catalog_readable else ():
            for sid, line in defined[column["column"]].items():
                rows_of = placed.get(sid, [])
                if not rows_of:
                    found.append(("parity-id-missing", f"{spec['path']}: {sid} ({column['path']}:{line}) is placed in "
                                                     f"no {spec['app']} catalog row"))
                elif len(rows_of) > 1:
                    found.append(("parity-id-duplicate", f"{spec['path']}: {sid} is placed in {len(rows_of)} rows: "
                                                       f"{', '.join(rows_of)}; a source id sits in exactly one"))
        if catalog_readable and rows:
            # An empty catalog is already damage; the summary is reconciled against rows that parsed.
            found += totals_findings(spec, texts[spec["path"]][0], rows)
        out += [(cls, f"{spec['app']}: {msg}") for cls, msg in found]
    return out


def parity_report(graph, todos, root=None) -> dict:
    """Per catalog: status totals, and per plan phase the features, distinct sections, and stamped sections.

    A `plan` or `shipped-scope` row counts under the phase whose table holds its section, or under `unplaced`;
    a section counts as stamped only when it carries a `Verified:` stamp, whatever its status kind says. Every
    parity finding (`parity_findings`) is listed under `problems`, and a report with problems is not evidence.
    """
    root = _root(graph, root)
    sections = _section_index(todos)
    phase_of: dict[str, str] = {}
    titles: dict[str, str] = {}
    for phase, info in graph.plan_phase_counts().items():
        titles[phase] = info["title"]
        for ref in info["refs"]:
            phase_of.setdefault(ref, phase)
    # The counts are evidence only while the catalogs validate: a damaged, empty, or drifted catalog would report
    # short counts as if they were whole (independent review 2026-10-21, rounds 1 and 2), so every parity finding
    # rides the report as a problem and `query parity` refuses it.
    texts = snapshot(root)
    report: dict = {"catalogs": {}, "problems": [msg for _cls, msg in parity_findings(graph, todos, root, texts)]}
    if not (root / "docs" / "parity").is_dir():
        report["problems"].append("no docs/parity/ in this tree, so there is no catalog to report on")
    for spec in CATALOGS:
        rows, _problems = parse_catalog(root, spec, texts)
        totals = {kind: 0 for kind in STATUS_KINDS}
        totals["malformed"] = 0
        phases: dict[str, dict] = {}
        for row in rows:
            kind, arg = parse_status(row["status"])
            totals[kind] += 1
            if kind not in ("plan", "shipped-scope"):
                continue
            ref = " ".join(arg.split())
            key = phase_of.get(ref, "unplaced")
            bucket = phases.setdefault(key, {"title": titles.get(key, "in no phase table"), "features": 0,
                                             "sections": set(), "stamped_sections": set(), "rows": []})
            bucket["features"] += 1
            bucket["sections"].add(ref)
            hit = sections.get(ref)
            if hit is not None and hit[1] in hit[0].verified_sections:
                bucket["stamped_sections"].add(ref)
            bucket["rows"].append({"id": row["id"], "status": kind, "ref": ref, "feature": row["feature"]})
        ordered = sorted(phases, key=lambda p: (p == "unplaced", int(p) if p.isdigit() else 0))
        report["catalogs"][spec["app"]] = {
            "path": spec["path"],
            "rows": len(rows),
            "totals": totals,
            "phases": {
                p: {"title": phases[p]["title"], "features": phases[p]["features"],
                    "sections": len(phases[p]["sections"]), "stamped_sections": len(phases[p]["stamped_sections"]),
                    "rows": phases[p]["rows"]}
                for p in ordered
            },
        }
    return report


def _self_check(root: Path) -> int:
    for spec in CATALOGS:
        for column in spec["columns"]:
            ids, problems = parse_sources(root, column)
            # One column may hold several families (Photoshop's PS-A- and PS-B-): each is counted too.
            families: dict[str, int] = {}
            for sid in ids:
                families[sid.rsplit("-", 1)[0]] = families.get(sid.rsplit("-", 1)[0], 0) + 1
            split = f" ({', '.join(f'{n} {k}' for k, n in sorted(families.items()))})" if len(families) > 1 else ""
            print(f"{column['path']}: {len(ids)} {column['column']} ids{split}"
                  + (f", {len(problems)} problem(s)" if problems else ""))
        rows, problems = parse_catalog(root, spec)
        print(f"{spec['path']}: {len(rows)} {spec['app']} rows" + (f", {len(problems)} problem(s)" if problems else ""))
    return 0


if __name__ == "__main__":
    sys.exit(_self_check(Path(__file__).resolve().parent.parent))
