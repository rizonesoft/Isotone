#!/usr/bin/env python3
"""The parity catalog checks (D00 T01 §6): every competitor source id placed once, every status in the grammar.

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
- `parity-np-duplicate`: a catalog feature id used on two rows.
- `parity-status-malformed`: a status outside the grammar.
- `parity-ref-dead`: a `plan` or `shipped-scope` ref naming no section, or a section carrying `> **Moved:**`.
- `parity-backlog-dead`: a `backlog B-NNN` id with no live entry in `todo/backlog.md`.
- `parity-input-damaged`: a catalog or source file the spec names is missing while `docs/parity/` exists, a row
  whose cell count differs from its table header, or a source id defined twice in one file. A damaged input never
  shrinks the denominator quietly: it fails naming the file and line.

A tree with no `docs/parity/` at all (a bare export of `todo/`) has nothing to check and validates.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# One catalog per app. `columns` maps each source column of the catalog to its inventory file and id shape.
# D00 T01 §7 and §8 add the Gesso and Albumen catalogs here.
CATALOGS = (
    {
        "app": "stilus",
        "path": "docs/parity/stilus-parity.md",
        "id": r"NP-\d{4}",
        "columns": (
            {"column": "Illustrator", "path": "docs/parity/sources/illustrator-30.8.md", "id": r"AI-\d{4}"},
            {"column": "CorelDRAW", "path": "docs/parity/sources/coreldraw-2026.md", "id": r"CD-\d{3,4}"},
        ),
    },
)

PARITY_CLASSES = (
    "parity-id-missing",
    "parity-id-duplicate",
    "parity-id-unknown",
    "parity-np-duplicate",
    "parity-status-malformed",
    "parity-ref-dead",
    "parity-backlog-dead",
    "parity-input-damaged",
)

STATUS_KINDS = ("plan", "shipped-scope", "backlog", "excluded", "other-app")
_REF = r"D\d{2} T\d{2} §\d+"
_STATUS_RES = (
    ("plan", re.compile(rf"^plan ({_REF})$")),
    ("shipped-scope", re.compile(rf"^shipped-scope ({_REF})$")),
    ("backlog", re.compile(r"^backlog (B-\d{3})$")),
    ("excluded", re.compile(r"^excluded: (\S.*)$")),
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


def _table_rows(text: str, id_re: str):
    """(line number, cells, header width) for every row whose first cell is an id of `id_re`.

    The width is the cell count of the nearest `| ID |` header above the row, or None when no header precedes it.
    """
    row_re = re.compile(rf"^\|\s*({id_re})\s*\|")
    width = None
    header: list[str] | None = None
    for lineno, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\|\s*ID\s*\|", line):
            header = split_row(line)
            width = len(header)
            continue
        if row_re.match(line):
            yield lineno, split_row(line), width, header


def parse_sources(root: Path, column: dict) -> tuple[dict[str, int], list[tuple[str, str]]]:
    """(source id -> defining line, problems) for one inventory file."""
    path = root / column["path"]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        return {}, [("parity-input-damaged", f"{column['path']}: the {column['column']} inventory cannot be read "
                                             f"({error.__class__.__name__}); restore it from git")]
    ids: dict[str, int] = {}
    problems: list[tuple[str, str]] = []
    for lineno, cells, width, _header in _table_rows(text, column["id"]):
        where = f"{column['path']}:{lineno}"
        if width is not None and len(cells) != width:
            problems.append(("parity-input-damaged", f"{where}: {cells[0]} has {len(cells)} cells against the "
                                                     f"header's {width}; repair the row"))
        if cells[0] in ids:
            problems.append(("parity-input-damaged", f"{where}: {cells[0]} is defined again (first at line "
                                                     f"{ids[cells[0]]}); a source id is defined once"))
            continue
        ids[cells[0]] = lineno
    return ids, problems


def parse_catalog(root: Path, spec: dict) -> tuple[list[dict], list[tuple[str, str]]]:
    """(rows, problems) for one catalog: each row's id, feature, source ids per column, category, status, notes."""
    path = root / spec["path"]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        return [], [("parity-input-damaged", f"{spec['path']}: the {spec['app']} catalog cannot be read "
                                             f"({error.__class__.__name__}); restore it from git")]
    rows: list[dict] = []
    problems: list[tuple[str, str]] = []
    for lineno, cells, width, header in _table_rows(text, spec["id"]):
        where = f"{spec['path']}:{lineno}"
        if header is None or len(cells) != width:
            got = "no `| ID |` header above it" if header is None else f"{len(cells)} cells against the header's {width}"
            problems.append(("parity-input-damaged", f"{where}: {cells[0]} has {got}; repair the row"))
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
    return rows, problems


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


def parity_findings(graph, todos, root=None) -> list[tuple[str, str]]:
    """Every parity finding as (class, message); empty when the tree carries no `docs/parity/`."""
    root = _root(graph, root)
    if not (root / "docs" / "parity").is_dir():
        return []
    sections = _section_index(todos)
    loaded = graph.load_backlog()
    backlog = {e["id"] for e in loaded[0]} if loaded is not None else set()
    out: list[tuple[str, str]] = []
    for spec in CATALOGS:
        # An unreadable file is one `parity-input-damaged` finding, never a cascade: a missing catalog places
        # nothing, so its sources' ids are not each reported missing, and a missing inventory defines nothing, so
        # the catalog's cells for it are not each reported unknown.
        defined: dict[str, dict[str, int]] = {}
        readable: dict[str, bool] = {}
        for column in spec["columns"]:
            ids, problems = parse_sources(root, column)
            defined[column["column"]] = ids
            readable[column["column"]] = (root / column["path"]).is_file()
            out += problems
        rows, problems = parse_catalog(root, spec)
        out += problems
        catalog_readable = (root / spec["path"]).is_file()
        placed: dict[str, list[str]] = {}
        first_row: dict[str, int] = {}
        for row in rows:
            where = f"{spec['path']}:{row['line']}: {row['id']}"
            if row["id"] in first_row:
                out.append(("parity-np-duplicate", f"{where} is used again (first at line {first_row[row['id']]}); "
                                                   f"take the next free number"))
            else:
                first_row[row["id"]] = row["line"]
            kind, arg = parse_status(row["status"])
            if kind == "malformed":
                out.append(("parity-status-malformed", f"{where} has status {row['status']!r}, outside the grammar "
                                                       f"of docs/parity/README.md"))
            elif kind in ("plan", "shipped-scope"):
                hit = sections.get(" ".join(arg.split()))
                if hit is None:
                    out.append(("parity-ref-dead", f"{where} {kind} {arg} names no section in todo/"))
                elif hit[2].moved:
                    out.append(("parity-ref-dead", f"{where} {kind} {arg} names a section that moved out of the "
                                                   f"tree (`> **Moved:**`); point the row at its new owner"))
            elif kind == "backlog" and arg not in backlog:
                out.append(("parity-backlog-dead", f"{where} backlog {arg} names no live entry in todo/backlog.md"))
            for column in spec["columns"]:
                if not readable[column["column"]]:
                    continue
                shape = re.compile(rf"^{column['id']}$")
                for token in row["sources"][column["column"]]:
                    if not shape.match(token) or token not in defined[column["column"]]:
                        out.append(("parity-id-unknown", f"{where} places {token!r} in {column['column']}, which "
                                                         f"{column['path']} does not define"))
                        continue
                    placed.setdefault(token, []).append(f"{row['id']} (line {row['line']})")
        for column in spec["columns"] if catalog_readable else ():
            for sid, line in defined[column["column"]].items():
                rows_of = placed.get(sid, [])
                if not rows_of:
                    out.append(("parity-id-missing", f"{spec['path']}: {sid} ({column['path']}:{line}) is placed in "
                                                     f"no {spec['app']} catalog row"))
                elif len(rows_of) > 1:
                    out.append(("parity-id-duplicate", f"{spec['path']}: {sid} is placed in {len(rows_of)} rows: "
                                                       f"{', '.join(rows_of)}; a source id sits in exactly one"))
    return out


def parity_report(graph, todos, root=None) -> dict:
    """Per catalog: status totals, and per plan phase the features, distinct sections, and stamped sections.

    A `plan` or `shipped-scope` row counts under the phase whose table holds its section, or under `unplaced`;
    a section counts as stamped only when it carries a `Verified:` stamp, whatever its status kind says.
    """
    root = _root(graph, root)
    sections = _section_index(todos)
    phase_of: dict[str, str] = {}
    titles: dict[str, str] = {}
    for phase, info in graph.plan_phase_counts().items():
        titles[phase] = info["title"]
        for ref in info["refs"]:
            phase_of.setdefault(ref, phase)
    report: dict = {"catalogs": {}}
    for spec in CATALOGS:
        rows, _problems = parse_catalog(root, spec)
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
            print(f"{column['path']}: {len(ids)} {column['column']} ids" + (f", {len(problems)} problem(s)" if problems else ""))
        rows, problems = parse_catalog(root, spec)
        print(f"{spec['path']}: {len(rows)} {spec['app']} rows" + (f", {len(problems)} problem(s)" if problems else ""))
    return 0


if __name__ == "__main__":
    sys.exit(_self_check(Path(__file__).resolve().parent.parent))
