## Round 1: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T00:59:14Z
- Effort: xhigh
- Lines: 25
- Digest: f2c07473e8285365

## adversarial: needs-attention

1. P1 `scripts/ci_watch.py:37` and `scripts/ci_watch.py:78`: the global 100-run limit can silently omit an unresolved failed workflow. An in-memory probe with one failed `pins` run followed by 100 successful `build` runs returned exit 0 and `1 workflow(s) checked, 0 red`. The full history correctly reported `pins` red. `gh --limit` limits total runs fetched, not runs per workflow. [GitHub CLI manual](https://cli.github.com/manual/gh_run_list)

## consistency: needs-attention

2. P1 `.claude/skills/review-todo-section/SKILL.md:181`: completion fixes require another panel round “inside the cap,” but completion review happens after panel sign-off, which can occur at round 33 (`:146`). Reproduce with a section reaching round 33 whose completion review then finds an in-scope missing entry point: fixing it requires round 34, while stamping without that round violates the new requirement. No exhaustion path reconciles these instructions.

## integration: needs-attention

3. P2 `.claude/skills/process-phase/SKILL.md:67`: scheduled workflow failures are routed into a repair procedure that pushes a repair commit and waits for CI, without starting the affected workflow. `.github/workflows/pins.yml:14` allows only schedule and manual dispatch. After a repair push, `pins` therefore remains red until another invocation occurs; waiting for `pins` on the repaired SHA returns unverifiable. The runner must invent the dispatch and verification step.

4. P2 `.claude/skills/review-todo-section/SKILL.md:153`: per-section parking is recorded only in findings and run-file prose, without integrating it into campaign selection. `resolve` and `query ready` do not recognize `REVIEW PENDING`; an in-memory probe left a ready section at resolve exit 0 with that marker present. When only pending sections remain, `process-phase` can park, but `process-plan/SKILL.md:25` still selects a phase containing those ready rows. The instructions lack a consistent handoff for excluding parked implementations while retaining their review retries.

## source-defect: needs-attention

5. P2 `.claude/skills/review-todo-section/SKILL.md:179`: the completion command supplies `$RUNDIR/completion` to `--keep` without creating it. The dispatcher requires an existing directory (`scripts/review-dispatch.py:558`); a fresh-directory probe returned exit 2, “not a folder.” Furthermore, the prescribed outage retry reuses that fixed directory, which the dispatcher refuses once attempt artifacts exist (`:562`). Unlike the architecture and stamp examples, this step needs directory creation and distinct attempt directories.

## record: needs-attention

6. P3 `docs/reviews/run-records.md:5` and `AGENTS.md:42`: current operational descriptions still advertise the retired contract. The records header specifies a 22-round cap and waiting for the operator after failure; the AGENTS paths table describes `[reviewers.*]` and `[routes]`. Reading these alongside the candidate’s schema-2 pin and 33-round parking rules demonstrates the contradictions. These are current explanatory text, separate from historical round records.

HIGHEST: P1

OVERALL: needs-attention

## Response to round 1

Every finding was verified against the code or the cited documentation and is real.

1. P1, the global run limit can hide a red workflow: verified (`gh run list --limit` limits the total). `ci_watch.py` now lists the active workflows and reads each one's runs separately; a self-test case puts one red `pins` run behind a hundred green `build` runs and must report it.
2. P1, completion fixes could need a round past the cap: verified. Completion fixes have their own allowance of up to 3 panel rounds beyond the loop's last round; a gap still open after it is filed like a cap leftover, its entry point disabled with `Planned:`.
3. P2, a repair push does not re-run a scheduled workflow: verified (`pins.yml` runs on schedule and dispatch only). `ci_watch.py --dispatch <workflow>` starts the workflow on `main` and waits for the run it started (green 0, red 1, unverifiable 2), with self-test cases including an older green run that must not answer for it; `process-phase` makes it the repair's read-back and adds `workflow_dispatch` to any scheduled workflow lacking it.
4. P2, `REVIEW PENDING` was invisible to campaign selection: verified. It is now a section marker, `> **Review pending:** <UTC> candidate <range>: <reason>`, which `todo-graph.py` parses: the section leaves `query ready`, reads `blocked` in `query plan`, and `query blocked` names the reason; self-test cases fail on a mutant without the rule. The skills write the marker, retry pending reviews at every boundary, and remove the marker when the review resumes.
5. P2, the completion review's keep folder was never created and would be reused: verified. Each attempt creates `$RUNDIR/completion-<N>` and a retry takes the next N.
6. P3, current descriptions advertised the retired shape and cap: verified. The run-records header and the AGENTS path table now describe the schema-2 pin, the 33-round cap, and the retry-then-park rule, keeping the history.

## Round 2: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:11:31Z
- Effort: xhigh
- Lines: 22
- Digest: 78aa9a0db2dbd99e

## adversarial: needs-attention

1. P1 `scripts/ci_watch.py:71`: dispatch verification selects the oldest run inside a window starting 60 seconds before dispatch, without binding its ID or SHA. An in-memory probe containing an earlier successful run and the newly dispatched failed run returned exit 0 for the earlier run. This can approve a failed repair.

## consistency: needs-attention

2. P3 `scripts/panel_slots.py:10`: the current module documentation still says an unavailable reviewer “waits for the operator.” Reading it against the new retry-and-park rule demonstrates a remaining operational contradiction.

## integration: needs-attention

3. P2 `scripts/todo-graph.py:3737`: parking affects queries but bypasses the runner’s resolution gates. For the same dependency-free section carrying `Review pending:`, an in-memory probe produced `0 runnable now`, while `resolve` and `resolve_exit_code` both returned 0. `.claude/skills/process-phase/SKILL.md:69` selects rows through `resolve`, so round 1’s parking answer remains incomplete.

4. P2 `.claude/skills/process-phase/SKILL.md:67`: scheduled repairs now use `ci_watch --dispatch` as their read-back, but the prescribed repair-close step requires evidence that output cannot supply. Passing its `GREEN pins run ...: success ...` line to `campaign_guard.repair(..., action="close")` reproduced rejection at `scripts/campaign_guard.py:824`, which accepts only a SHA-bound `ci-wait:` line. A successful repair needs an additional, unspecified verification step.

## source-defect: needs-attention

5. P2 `scripts/ci_watch.py:37`: the shared `gh()` wrapper parses every nonempty stdout as JSON, including `gh workflow run`. Installed GitHub CLI 2.102.0 can return a plain run URL on successful dispatch. Mocking that documented successful response made `main(["--dispatch", "pins.yml"])` exit 2 before polling. The dispatch self-tests return `None`, concealing this failure. [GitHub CLI source](https://github.com/cli/cli/blob/v2.102.0/pkg/cmd/workflow/run/run.go#L360-L363)

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 2

Every finding was verified against the code and is real.

1. P1, the dispatch read-back could take an older run: verified. `--dispatch` now binds to the run `gh workflow run` names by URL and views that run alone; without a URL it accepts only the single `workflow_dispatch` run created after the dispatch and is unverifiable (exit 2) when there are more, never a guess. Self-test cases cover an earlier green run beside a red dispatched one, a concurrent run with and without a URL, and mutants that ignore the URL or the ambiguity each fail.
2. P3, `panel_slots.py`'s module text still said a failed round waits for the operator: verified and corrected, with the schema-2 pin described.
3. P2, `resolve` ignored the parking rules: verified. One function, `parked_reason`, now serves `resolve`, `resolve_exit_code`, and the queries: a section of a blocked or superseded file, or with `Review pending:`, exits 4 with its reason. Self-test cases fail on a mutant without it, and a live `resolve` of a parked section exits 4.
4. P2, `repair close` could not accept a dispatched run's read-back: verified. `campaign_guard.py` checks evidence through `green_evidence`, which accepts the `ci-wait:` push line or the `ci-watch:` line `--dispatch` prints, both bound to the sha and the workflow and saying `success`, with self-test cases for both and for a red, another workflow, another sha, and another prefix; `process-phase` names the line as the repair's evidence.
5. P2, `gh workflow run` prints a URL, not JSON: verified. `gh()` returns text and each caller parses what it expects; the dispatch fixture now returns the plain URL gh 2.102 prints.
