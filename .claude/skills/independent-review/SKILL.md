---
name: independent-review
description: Get an independent review of your own work from the reviewer pinned in .conclave/reviewers.toml (GPT-6 Astra only, no fallback) through scripts/review-dispatch.py, then verify and act on every finding. Use before calling a nontrivial change outside a TODO section done, or before a commit that ships one. A TODO section's review runs through review-todo-section and the panel instead.
---

# Independent review

Your own review is not enough for a nontrivial change: a different model reviews it. `.conclave/reviewers.toml` names who reviews whose work, and `scripts/review-dispatch.py` runs the round.

| Work written by | Reviewed by |
| --- | --- |
| Claude (the only writer here) | GPT-6 Astra, with no fallback |

A TODO section is reviewed through `review-todo-section`, whose rounds run on `python scripts/panel_slots.py exec <slot>` (`.conclave/panel.toml`). This skill is for work outside a section: tooling, agent wiring, and other changes no section owns.

## Steps

1. Review your own change first and fix what you find.
2. Write the review prompt to a scratch file, not the repository, from `docs/review-round-prompt.md`: name the candidate commit or range, the governing documents, and the lenses that apply.
3. Run the round, naming yourself as the writer:

   ```bash
   python scripts/review-dispatch.py --writer claude --prompt <scratch>/review-prompt.md --record docs/reviews/<topic>.md
   ```

4. Read the review. Verify every finding against the code before acting: fix what is real, and record why anything else is not.
5. Commit fixes as new commits and run another round on the new tip, up to 3 rounds. A unit that needs patching three rounds running gets re-thought, not patched again.

## Rules

- The dispatcher's JSON output and the `## Round N` section it appends are the evidence. A verdict with no record is an opinion.
- Exit 1 means Astra returned no review. That is never an approval: say so, do not ship on it, and wait for the operator (there is no fallback reviewer).
- Reviewers run read-only. Never pass a reviewer a secret, and never ask it to edit files.
- Change reviewers only in `.conclave/reviewers.toml`, never by calling a model directly, and keep it agreeing with `.conclave/panel.toml`: no Claude-family reviewer, no fallback.
