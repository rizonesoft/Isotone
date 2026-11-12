---
name: independent-review
description: Get an independent review of your own work outside a TODO section from the reviewer pinned in .conclave/reviewers.toml (GPT-6 Astra, never the writer's family, no fallback) through scripts/review-prompt.py and scripts/review-dispatch.py, then verify and act on every finding. Use before calling a nontrivial workspace change done or before shipping it; TODO sections review through review-todo-section instead.
---

# Independent Review

Your own review is not enough for a nontrivial change: a cross-family model reviews it. `.conclave/reviewers.toml` names who reviews the writer's work (`astra` on `gpt-6-astra` via `codex` for `agy` and `claude`), and `scripts/review-dispatch.py` runs every round read-only.

| Work written by | Reviewer | Fallback |
| --- | --- | --- |
| Antigravity (`agy`) or Claude Code (`claude`) | GPT-6 Astra (`astra`), scheduled effort from `.conclave/reviewers.toml` | none: a round Astra cannot return is retried with backoff and then parked |

The dispatcher refuses a reviewer of the writer's own family, and `python scripts/panel_slots.py validate` plus `python scripts/review_pin.py --check` enforce the pin. A TODO section never uses this skill: its `plan`, `round`, `completion`, and `reconciliation` passes run through `process-todo-section` and `review-todo-section`.

## Steps

1. Review your own change first, run the relevant local gates, and fix what you find.
2. Commit the candidate on `main` (always develop straight on `main`; never create branches or worktrees) and capture `CANDIDATE=$(git rev-parse HEAD)`.
3. Build the review prompt into an ignored scratch path under `build/` using `scripts/review-prompt.py`:

```bash
KEEP=$(mktemp -d build/review-XXXXXXXX)
mkdir -p "$KEEP/out"
python scripts/review-prompt.py --kind round --candidate "$CANDIDATE" --purpose "<one or two sentences>" --governing "AGENTS.md, docs/todo-workflow.md" --out "$KEEP/prompt.md"
python scripts/review-dispatch.py --writer claude --kind round --candidate "$CANDIDATE" --prompt "$KEEP/prompt.md" --keep "$KEEP/out" --record docs/reviews/independent/<YYYY-MM-DD>-<topic>.md
```

(Pass `--writer agy` when running inside Antigravity, `--base "$BASE_SHA"` when reviewing a commit range, and `--surface` on `review-dispatch.py` when UI surfaces or design tokens changed.)

4. Read the JSON summary (`verdict`, `highest`, `blocking`) and the recorded `## Round N` block. Verify every finding against the source code before acting: fix real defects, and append a `## Response to round N` block *after* the dispatcher's block (never edit inside a dispatcher-written block).
5. When `"blocking": true` (`P1` or `P2`), commit the fixes on `main`, rebuild the prompt on the new tip, and run the next round on the same `--record` file until `"blocking": false` (up to `pass_cap = 33`). File worthwhile `P3` follow-ups through `add-todo` and commit the review record on `main`.

## Rules

- Never edit inside a `## Round N` block written by `scripts/review-dispatch.py`.
- Exit 1 means no review was returned: retry with backoff (`15m`, `30m`, `1h`, `2h`, `4h`), never treat exit 1 as approval, and never call a reviewer CLI directly outside `scripts/review-dispatch.py`.
