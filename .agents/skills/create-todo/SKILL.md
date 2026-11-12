---
name: create-todo
description: Author a whole new TODO file -- frontmatter, Goal, Current state, Inputs, Outcome with Adjacency, Implementation Order, sections, Verification -- then wire indexes, XREFs, and the plan. Use when add-todo routes here.
---

# Create TODO

Author a new `todo/<NN-domain>/TODO-<NN>-<short-name>.md` file when a subject has no existing file owner or when an existing file reached the 55-section structural cap (`docs/todo-workflow.md`). Always search first as `add-todo` specifies so no two files split one subject.

## Workflow

### 1. Confirm domain, number, and provenance

Pick the owning domain from `todo/TODO-00-INDEX.md` and take the next free `TODO-NN` number in `todo/<NN-domain>/INDEX.md` (creating a new `todo/<NN-kebab>/INDEX.md` and appending to `todo/TODO-00-INDEX.md` only when a genuinely new domain is required). Operator-directed files carry no `**Origin:**` lines; campaign-discovered files pass `add-todo`'s admission test per section and carry `**Origin:** discovered run=<run id> <YYYY-MM-DD> -- <source>` under each section heading, routing non-qualifying ideas to `todo/backlog.md`.

### 2. Author from the template

Copy `.agents/skills/create-todo/todo-template.md` to `todo/<NN-domain>/TODO-<NN>-<short-name>.md` and complete every block with zero `CHANGEME` leftovers:

- **Frontmatter:** `schema_version: 1`, globally unique kebab-case `id` (2-60 chars), `domain` matching the folder name, `status: active` (or `draft` only when explicitly requested), `title: "TODO-NN -- Title"`, optional `depends_on: []`.
- **Goal & Current state:** plain-language goal paragraph, plus a dated `Current state` block citing real repository paths and `<!-- claim: ... -->` assertions verified by `python scripts/todo-claims.py`.
- **Inputs & Outcome:** concrete specs (`docs/specs/`, `docs/design/`, `standards/cpp.md`), existing files consumed, bidirectional `-> XREF:` links, observable end states, and the mandatory `**Adjacency:**` + `**Adjacency rationale:**` lines (`todo/README.md`).
- **Implementation Order:** one row per numbered section (`1..N`, max 55 sections per file) with explicit `Depends On` edges (`--` only when standalone) and `[ ]` status.
- **Sections:** single-responsibility deliverables (max 30 items per section), `**Exceed:**` paragraph on every competitor-facing feature section (`AGENTS.md`), granular micro-steps naming backticked paths/symbols + `Done when:` + `Cheaper substitute:` + `Commit:`, falsifiable `**Test checkpoint:**` naming one of the proof kinds in `todo/README.md`, `**Fidelity:**` + `**Design:**` + `**Job:**` + `**Treatment:**` + `**Chrome:**` on surface sections (`standards/design-contract.md`, writing `new surface: docs/design/<path>.md` as item 1 when a spec does not exist yet), and `**Needs:**` / `**Requires:**` from the closed lists in `todo/README.md` when needed.
- **Verification:** file-level build, CTest, artifact-gate, round-trip, and `todo-graph.py validate` checks that `process-todo-file` will execute on completion.

### 3. Wire, validate, and commit

- Add the file verbatim to `todo/<NN-domain>/INDEX.md` and under Active TODOs in `todo/TODO-00-INDEX.md`.
- Reciprocate every `-> XREF:` in its target TODO files, and update `docs/parity/*-parity.md` in the same commit if parity feature ownership moved.
- Place every section row in `todo/implementation-plan.md` no earlier than any dependency's phase, then run:

```powershell
python scripts/todo-claims.py
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --sync
python scripts/todo-graph.py plan --check
```

- Commit on `main` as `todo: author <id> (<n> sections)` and report the file link, phase placement, dependency edges, and plan totals.

## Guardrails

- Never author stub sections or leave `CHANGEME` placeholders.
- Never omit `**Adjacency:**`, and never add surface sections without a validating `**Design:**` line (never grow `todo/.design-baseline`).
- Never use em dashes or en dashes anywhere (`--` only), and write one line per Markdown paragraph and bullet.
