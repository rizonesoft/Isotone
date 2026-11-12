---
name: independent-review
description: Get an independent review of your own work outside a TODO section from the reviewer pinned in .conclave/reviewers.toml (GPT-6 Astra, never the writer's family, no fallback) through scripts/review-prompt.py and scripts/review-dispatch.py, then verify and act on every finding. Use before calling a nontrivial workspace change done or before shipping it; TODO sections review through review-todo-section instead.
---

# Independent Review

Your own review is not enough for a nontrivial change: a cross-family model reviews it. `.conclave/reviewers.toml` names who reviews the writer's work (`astra` on `gpt-6-astra` via `codex` for `agy`), and `scripts/review-dispatch.py` runs every round read-only.

| Work written by | Reviewer | Fallback |
| --- | --- | --- |
| Antigravity (`agy`) on Gemini 4 Carbon (Medium) | GPT-6 Astra (`astra`), scheduled effort from `.conclave/reviewers.toml` | none: a round Astra cannot return is retried with backoff and then parked |

The dispatcher refuses a reviewer of the writer's own family, and `python scripts/panel_slots.py validate` plus `python scripts/review_pin.py --check` enforce the pin (`docs/dev/decisions.md`). A TODO section never uses this skill: its `plan`, `round`, `completion`, and `reconciliation` passes run through `process-todo-section` and `review-todo-section`.

## Steps

1. Review your own change first, check `isotone-lsp` diagnostics (`lsp_diagnostics`) on touched C++ and Python files, run the relevant local gates, and fix what you find.
2. Commit the candidate on `main` (always develop straight on `main`; never create branches or worktrees) and capture `CANDIDATE=$(git rev-parse HEAD)`.
3. Build the review prompt into an ignored scratch path under `build/` using `scripts/review-prompt.py` (which fills `docs/review-round-prompt.md` and refuses any unfilled `<placeholder>`):

```powershell
python scripts/review-prompt.py --kind round --candidate $CANDIDATE --purpose "<one or two sentences on what the change is for>" --governing "AGENTS.md, docs/todo-workflow.md" --out build/review-prompt.md
```

Pass `--base $BASE_SHA` as well when reviewing a multi-commit range `$BASE_SHA..$CANDIDATE`.

4. Dispatch the round as `agy` (adding `--surface` when the change touches UI tokens, design specs, or rendered surfaces so the `design` lens runs), keeping the raw output under an ignored scratch directory and appending the record to `docs/reviews/independent/<YYYY-MM-DD>-<topic>.md`:

```powershell
$keep = Join-Path "build/reviews" ([guid]::NewGuid().ToString("N").Substring(0, 12))
New-Item -ItemType Directory -Force $keep | Out-Null
python scripts/review-dispatch.py --writer agy --kind round --candidate $CANDIDATE --prompt build/review-prompt.md --keep $keep --record docs/reviews/independent/<YYYY-MM-DD>-<topic>.md
```

5. Parse the JSON summary printed to stdout (`verdict`, `highest`, `blocking`, `lenses`, `effort`) and read the recorded `## Round N` block. Verify every finding against the source code before acting: fix real defects, and record a `## Response to round N` block *after* the dispatcher's block (never edit inside a dispatcher-written block) stating what was fixed, refuted with file-and-line proof, or filed through `add-todo`.
6. When `"blocking": true` (`P1` or `P2` under `[schedule].blocking`), commit the fixes on `main`, capture the new `HEAD` SHA, rebuild the prompt with `scripts/review-prompt.py` on the new `--candidate` (or `--base $FIRST_BASE --candidate $NEW_HEAD`), and run the next round on the same `--record` file (the dispatcher automatically increments the round number and adjusts scheduled effort) until `"blocking": false`, up to the 33-pass cap in `.conclave/reviewers.toml` (a pass that returns no review does not count toward the cap). At `"blocking": false`, file any non-blocking `P3` findings that represent real follow-up work through `add-todo`, commit the updated review record on `main`, and report.

## Rules

- The dispatcher's JSON summary and the `## Round N` block it appends under `docs/reviews/independent/` are the evidence; never edit inside a recorded round block.
- Exit 1 means no review was returned (CLI missing, auth failure, timeout, empty reply, missing `LENS` lines, or `OVERALL: blocked`). Never treat exit 1 as approval: retry with backoff (15 minutes, 30 minutes, 1 hour, 2 hours, 4 hours), and if every retry fails, record the pending review and move to independent work.
- Reviewers run read-only (`codex exec --sandbox read-only --ephemeral`). Never pass secrets in prompts, and never ask a reviewer to edit files.
- Change reviewer routing or models only in `.conclave/reviewers.toml`, never by calling a reviewer CLI directly.
