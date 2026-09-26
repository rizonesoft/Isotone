# Nodus Parity

This folder is the evidence behind one operator decision: Nodus gets every CorelDRAW feature and every Illustrator feature. The operator's words, recorded 2026-09-26: "For Nodus, we need to add all(and I mean), all CorelDraw features and All Illustrator Features." The budget raise that pays for it is quoted in `todo/budget.json` ("New parity phases, up to +200").

## What is here

| File | Purpose |
| ---- | ------- |
| [`sources/illustrator-30.8.md`](sources/illustrator-30.8.md) | The Adobe Illustrator 30.8 feature inventory (August 2026 release), rows `AI-0001` to `AI-1294`, verbatim as compiled on 2026-09-26 |
| [`sources/coreldraw-2026.md`](sources/coreldraw-2026.md) | The CorelDRAW Graphics Suite 2026 v27.2 feature inventory (September 2026 update), rows `CD-001` to `CD-3041`, verbatim as compiled on 2026-09-26 |
| [`nodus-parity.md`](nodus-parity.md) | The unified catalog: every inventory row merged into Nodus features (`NP-####`), each with exactly one status |
| [`section-design.md`](section-design.md) | The authoring blueprint for the TODO files that own the planned features: files, sections, phases, dependencies, hints, and authoring batches. Integrated into `todo/` on 2026-09-26 (14 new TODO files, `D00 T01 §6`, Phases 4 to 13 of `todo/implementation-plan.md`); from then on the TODO files are the plan and this file is the design record |

The sources are provenance: each row names its version, its menu location, and the help page it came from. They are never edited except to append rows for a newer version (below).

## Sources and versions

- **Illustrator:** Adobe Illustrator 2026, version 30.8 (August 2026), current LTS 29.8.7; read from Adobe's help and release-notes pages through a browser session. The inventory lists its primary sources at its top.
- **CorelDRAW:** CorelDRAW Graphics Suite 2026, version 27.2 (September 2026 Update); read from the CorelDRAW Graphics Suite 2025 (v26) Help (the newest public Help) plus Corel's 2026 what's-new, update, and press pages. The inventory records that caveat at its top.

## The catalog

Each catalog row is one user-facing capability. Rows from both apps that do the same job, and duplicate rows inside one app (a tool and its menu entry, a docker and its command), are merged into one feature. Columns:

| Column | Meaning |
| ------ | ------- |
| `ID` | `NP-0001` onward. Stable: a number is never reused or renumbered |
| `Feature` | The capability in Nodus's words |
| `Illustrator` | The `AI-####` rows it covers, comma-separated, or `--` |
| `CorelDRAW` | The `CD-###` rows it covers, comma-separated, or `--` |
| `Category` | `core`, `format`, `print`, `ai`, `automation`, `cloud`, or `companion`, taken from the inventory rows |
| `Status` | Exactly one of the forms below |
| `Notes` | What Nodus does differently, a license note, or the reason for an exclusion |

Every `AI-####` and `CD-###` id appears in exactly one catalog row.

## Status grammar

Exactly one status per row:

| Status | Meaning |
| ------ | ------- |
| `plan <DNN TNN §N>` | A parity section owns the feature; the section is designed in `section-design.md` and authored under `todo/` |
| `shipped-scope <DNN TNN §N>` | A section that existed before the parity plan already owns the feature (for example `D02 T04 §2` for SVG open and save) |
| `backlog B-NNN` | The feature is kept as a `todo/backlog.md` entry, not a section (obsolete formats, work waiting on another app's shared code) |
| `excluded: <reason>` | Out of scope by operator decision: scripting, macros, and automation; cloud documents, libraries, sharing, and online services; hardware Nodus cannot run on |
| `other-app: <Imago|Lumen|none> <reason>` | A companion-app feature whose job belongs to another Photon app, or to none |

A `plan` or `shipped-scope` ref names a real section in `DNN TNN §N` form; a `backlog` id names a live backlog entry. Whether a planned feature has shipped is read from its section's Implementation Order row and stamp, never typed into the catalog.

## How to update

- **A new Illustrator or CorelDRAW version:** compile the new inventory the same way, and append its new rows to the matching file under `sources/` with the next free ids (`AI-1295` onward, `CD-3042` onward) and a version note in the row's Feature or Source cell. Never renumber an existing row. Then add each new id to the catalog: merge it into an existing feature when it is the same capability, or add a new `NP-` row at the end of the right area table with its status.
- **A new catalog row:** take the next free `NP-` number, even when the row sits in the middle of an area table.
- **Rerouting a feature:** change its status in place (for example from `backlog B-037` to `plan D02 T14 §11` when the backlog entry is promoted through `add-todo`), in the same commit that changes the plan.
- **Splitting a feature:** keep the original `NP-` row for one part and give each other part a new `NP-` number, moving its source ids with it.

## Enforcement

A validator check, planned in Phase 0 as `D00 T01 §6` and not built yet, will read both source files and the catalog and fail when an id is missing, duplicated, or unknown, when a status is outside the grammar, when a `plan` or `shipped-scope` ref does not resolve to a live section, or when a `backlog` id names no live entry. It will run inside `python scripts/todo-graph.py validate`, so the commit hook and CI refuse a catalog that has drifted from the plan. Until it ships, a change to a catalog status or to a section or backlog entry the catalog names is checked by hand against those rules in the same commit.
