---
name: process-todo-file
description: Close out a TODO file whose sections are all shipped -- sweep for loose ends, run the file-level Verification block, reconcile deferrals and frozen checks, update the indexes, and set status to done. Use when every Implementation Order row is [x], or when asked to close a whole TODO file.
---

# Process TODO File

Close out a finished TODO file (`docs/todo-workflow.md`), catching cross-section loose ends, orphaned deferrals, and integration gaps. When `process-phase` invokes this in **sweep-only mode** (some sections in the file belong to later phases and remain `[ ]`), run Steps 1-4 for the shipped rows only, skip Step 5, and keep `status: active`.

## Workflow

### 1. Confirm stamp and graph integrity

```powershell
python scripts/todo-graph.py validate
python scripts/todo-graph.py query adjacency --file <repo-relative-todo-path> --require-owned
```

Every `[x]` row must be covered by a valid `Verified:` stamp and JSON receipt (or grandfathered legacy record) with zero FATALs. Do not close a file while any row is `[ ]`.

### 2. Run the file-level `## Verification` block

Execute every item in the file's `## Verification` section for real, including the full gate sweep (`.agents/skills/process-todo-section/gates.md`):

```powershell
pwsh scripts/check-all.ps1
```

Plus every CTest, native artifact gate, fuzz smoke, round-trip fixture, or golden render check listed in `## Verification`, quoting real outputs (in sweep-only mode, record items owned by still-open sections as not-yet-runnable with their owning `D<NN> T<NN> §<N>` ref).

### 3. Loose-end and integration sweep

- Scan touched paths under `native/`, `scripts/`, and `docs/` for `TODO`, `FIXME`, `HACK`, `XXX`, or stubbed handlers: finish in-scope leftovers now or route out-of-scope items through `add-todo` (never leave silent stubs).
- Check `python scripts/todo-graph.py query deferred`: every open deferral written in this file must point to a live, still-open owner section (never `todo/backlog.md`).
- Confirm user-facing features are wired end to end (menu/rail/shortcut/command-palette entry points, settings consumers, undo/redo, atomic persistence, `docs/user/` documentation) and preserve standalone per-app distribution (`AGENTS.md`: no runtime dependency on another Isotone app).

### 4. Reconcile `frozen: true` contracts

If frontmatter sets `frozen: true`, confirm every `**Freeze check:**` ran against committed fixtures under `tests/fixtures/` (or `native/tests/fixtures/`) and no frozen behavior changed without recorded operator approval.

### 5. Graduate status and update indexes (exhausted files only)

- Set `status: done` in the YAML frontmatter.
- Move the file's entry in `todo/<NN-domain>/INDEX.md` to its **Completed** section with today's `YYYY-MM-DD` date, and update Active TODOs in `todo/TODO-00-INDEX.md`.
- Run `python scripts/todo-graph.py validate`, `python scripts/todo-graph.py plan --sync`, and `python scripts/todo-graph.py plan --check`.

### 6. Commit and report

Commit on `main` (`<domain>: complete TODO-NN -- <summary>`), quoting the `## Verification` outputs, deferred work and owners, any discovered filings (`query growth`), and `python scripts/todo-graph.py query budget`.

## Guardrails

- Never set `status: done` while any section in the file is `[ ]` or `> **Review pending:**`.
- Never delete section history or checklist detail on closeout, and never use em/en dashes (`--` only).
