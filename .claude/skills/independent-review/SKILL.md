---
name: independent-review
description: Get an independent review of your own work outside a TODO section from the reviewer pinned in .conclave/reviewers.toml (GPT-6.1 Sol, never the writer's family, no fallback) through scripts/review-dispatch.py, then verify and act on every finding. Use before calling a nontrivial workspace change done or before a commit that ships it; TODO sections review through review-todo-section instead.
---

# Independent review

Your own review is not enough for a nontrivial change: a different model reviews it. `.conclave/reviewers.toml` names who reviews Claude's work, and `scripts/review-dispatch.py` runs the round.

| Work written by | Reviewer | Fallback |
| --- | --- | --- |
| Claude Code on Opus 5.5 (the solo writer) | GPT-6.1 Sol, xhigh effort | none: a round Sol cannot return is retried with backoff and then parked |

The dispatcher refuses a reviewer of the writer's own family, and `python scripts/panel_slots.py validate` refuses a fallback or a second writer route (operator decisions 2026-09-25 and 2026-10-21). A TODO section never uses this skill: its panel, architecture, plan, stamp, and independent rounds run through the same dispatcher inside `review-todo-section` and `process-todo-section`.

## Steps

1. Review your own change first and fix what you find.
2. Write the review prompt to a scratch file, not the repository, from `docs/review-round-prompt.md`: name the candidate commit or range by its full sha, the governing documents, and the lenses that apply.
3. Run the round as the writer, keeping the raw evidence beside the review:

   ```bash
   KEEP=$(mktemp -d /tmp/review-XXXXXXXX)
   python scripts/review-dispatch.py --writer claude --prompt <scratch>/review-prompt.md --keep $KEEP --record docs/reviews/independent/<YYYY-MM-DD>-<topic>.md
   ```

4. Read the review. Verify every finding against the code before acting: fix what is real, and record why anything else is not, as text after the round (a `## Response to round N` heading), never inside it.
5. Commit fixes as new commits and run another round on the new tip, up to 33 rounds (operator decision 2026-10-23, raised from 22 for this build's complexity) (a round that returns no review does not count). From round 9 on, a round whose findings are all `P3` or advisory (its `HIGHEST: P3` line; the prompt asks for a `P1`, `P2` or `P3` tag on every finding, and an untagged one counts as `P1`) ends the loop, and its findings are filed as follow-up work. At the cap, file every leftover with an owner and say so in the record; nobody is asked. A unit that needs patching three rounds running gets re-thought, not patched again.

## Rules

- The dispatcher's JSON output and the `## Round N` section it appends are the evidence. A verdict with no record is an opinion. Independent records live under `docs/reviews/independent/`, apart from the per-section findings files the TODO validators read.
- Exit 1 means no review was returned. That is never an approval: say so, record it, and retry with the backoff `review-todo-section` states; if every retry fails, leave the work unshipped, record it as pending review, and carry on with work that does not depend on it, retrying at the next boundary.
- A reviewer that could not reach the work (its sandbox could not read the repository) replies `OVERALL: blocked`, which counts as no review. If its sandbox keeps failing, put the diff in the prompt.
- Reviewers run read-only. Never pass a reviewer a secret, and never ask it to edit files.
- Change reviewers only in `.conclave/reviewers.toml`, never by calling a model directly.
