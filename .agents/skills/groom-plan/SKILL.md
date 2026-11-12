---
name: groom-plan
description: Harden the todo tree for unattended execution -- sequence check, drift sweep, gap scan, complete-feature and Exceed pass, backlog triage (promote or leave; never drop) -- without moving rows between phases, ticking boxes, or starting a campaign. Use before a long run, or when the plan feels stale.
---

# Groom Plan

Harden `todo/` so every open section is accurate, complete, dependency-ordered, and ready for unattended execution (`docs/todo-workflow.md`). Grooming adds missing prerequisites, sharpens drifted claims, and files gaps; it never moves an existing row out of its phase, never ticks a `[ ]` box, never drops a backlog entry without operator words, never edits `todo/budget.json`, and never starts a campaign.

## Evidence first

```powershell
python scripts/todo-graph.py query sequence
python scripts/todo-claims.py
python scripts/todo-claims.py --coverage
```

Record `START_SHA=$(git rev-parse HEAD)` and mint a provenance ID (`python scripts/campaign_guard.py mint-generation`, or use the active campaign `run_id`): every new section discovered by the groom carries `**Origin:** discovered run=<run id> <YYYY-MM-DD> -- groom-plan <step>` directly under its heading. `query sequence` highlights dependency chains and cross-section review filings, which are leads to read carefully rather than blind reorder instructions.

## Workflow

### 1. Sequence check

Confirm every `Depends On` and file-level `depends_on` prerequisite sits no later than its consumer in `todo/implementation-plan.md`. Where an edge points to a later phase, never move the consumer's row across phases; split or add the minimal prerequisite section into the consumer's phase (or earlier) with a dated `**Groomed YYYY-MM-DD:**` note, and run `python scripts/todo-graph.py validate` after each structural edit.

### 2. Drift sweep

Verify concrete assertions in open sections against the live repository (native C++23 paths under `native/` per `docs/specs/2026-10-22-native-stack-design.md` and `standards/cpp.md`, vcpkg register entries in `docs/dev/native-libraries.md`, toolchain pins in `native/toolchain.json`, counts, XREFs, deferrals, and design specs). Correct stale claims in place with `**Corrected YYYY-MM-DD:**` or `**Groomed YYYY-MM-DD:**` notes so history remains visible. For any open surface section still in `todo/.design-baseline`, write its `**Design:**` line citing `docs/design/` specs (`standards/design-contract.md`), replace any legacy `docs/captures/<app>/` fidelity target with `docs/design/` + `docs/captures/golden/`, and shrink `todo/.design-baseline` via `python scripts/todo-graph.py design-baseline`.

### 3. Gap scan and Adjacency pass

Walk the plan domain by domain as a user of Stilus, Gesso, Albumen, Tinctura, Capio, and Folium: check for unowned surfaces, dead controls, missing error/recovery paths, settings without consumers, unverified parity rows (`docs/parity/`), and `python scripts/todo-graph.py query adjacency` advisories. Route every gap through `add-todo` (admission test decides live section/item versus `todo/backlog.md`).

### 4. Complete-feature and Exceed pass

Confirm every feature section plans a whole user-reachable feature (`docs/completion-review-prompt.md`): menu/rail/shortcut/panel entry points, states, atomic writes with read-back and failure tests, undo/redo, persistence round trips, accessibility, user guide updates, structured logging, and a concrete, measurable `**Exceed:**` improvement over the competition (`AGENTS.md`). Add missing in-scope micro-steps directly to open sections or file new sections via `add-todo`.

### 5. Backlog triage

```powershell
python scripts/todo-graph.py query backlog
python scripts/todo-graph.py query budget
```

Promote entries whose `promote when:` trigger is met and that pass `add-todo`'s admission test (carrying `-> SOURCE: <key>` on the new section and removing the backlog line in the same commit). Merge duplicate backlog entries into the lower ID while keeping ``merged: `<source-key>` (B-NNN, YYYY-MM-DD)`` on the survivor. Leave not-yet-due entries intact (fixing drifted `needs:` refs in place), and list genuinely obsolete entries for the operator rather than deleting them without verbatim operator approval under `## Removed with operator approval`.

### 6. Validate, sync, commit, and report

```powershell
python scripts/todo-claims.py
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --sync
python scripts/todo-graph.py plan --check
```

Commit on `main` as `todo: groom <scope> (<YYYY-MM-DD>)` and report sequenced prerequisites, corrected drift, filed sections and backlog IDs, `query growth --since <START_SHA>`, and updated plan totals.

## Guardrails

- Never move existing rows between phases, tick `[ ]` checkboxes, or start a campaign.
- Never grow `todo/.design-baseline` or `docs/design/.lint-baseline.json`, and never use em dashes or en dashes (`--` only). Both baselines stay empty: `python scripts/todo-graph.py query design` prints `0 exempt` and `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` prints `0 new, 0 stale` before and after the pass, and every open surface section carries a live `**Design:**` line (`standards/design-contract.md`).
