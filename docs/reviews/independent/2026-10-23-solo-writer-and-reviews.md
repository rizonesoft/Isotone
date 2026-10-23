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

## Round 3: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:26:16Z
- Effort: xhigh
- Lines: 20
- Digest: 4be46224a9059574

## adversarial: needs-attention

1. P1 `scripts/ci_watch.py:90`: the no-URL dispatch fallback still accepts an unrelated run. Against `76e14bf`, an in-memory probe dispatched at `12:00:00`, returned no URL, and listed only a successful run created at `11:59:57`. `dispatch_and_wait` returned exit 0 for that older run before seeing the dispatched run. A single visible concurrent run also passes. Counting visible candidates does not establish identity, and GitHub CLI explicitly supports dispatch responses without run details. [GitHub CLI source](https://github.com/cli/cli/blob/v2.102.0/pkg/cmd/workflow/run/run.go#L328-L335)

2. P1 `scripts/ci_watch.py:63`: the per-workflow limit is applied before filtering completed runs, so queued runs can conceal the latest completed failure. A probe against `76e14bf` with twenty newer queued runs followed by one completed failure produced `0 red, 0 checked`, allowing exit 0. Fetch completed runs explicitly or continue fetching until the relevant completed run is found. [GitHub CLI run-list options](https://cli.github.com/manual/gh_run_list)

## consistency: needs-attention

3. P2 `.claude/skills/process-todo-section/SKILL.md:258` and `.claude/skills/review-todo-section/SKILL.md:226`: independent and plan-review outages retain the old continuation rules instead of the new retry-and-park policy in `docs/dev/decisions.md:60`. Demonstrate with a transient outage during the independent pass, followed by successful panel rounds: the instructions permit recording the missing pass in the stamp without retrying it. The plan-review path likewise explicitly records an outage and continues without the prescribed backoff.

## integration: needs-attention

4. P2 `scripts/ci_watch.py:79` and `.claude/skills/process-phase/SKILL.md:67`: the prescribed repair dispatch cannot supply workflow inputs. A failed draft `release` run on `main` is monitored, but `.github/workflows/release.yml:41` requires `tag`; `ci_watch.py --dispatch release.yml` sends no inputs and exposes no way to provide them. The runner must invent another dispatch and verification path to finish that repair. [GitHub CLI workflow-input options](https://cli.github.com/manual/gh_workflow_run)

## source-defect: approve

## record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 3

Every finding was verified against the code and the cited documentation and is real.

1. P1, the no-URL dispatch fallback could accept an unrelated run: verified (the GitHub CLI can return a dispatch without run details). Counting candidates cannot prove identity, so the fallback is removed: a dispatch `gh` does not name by URL is unverifiable (exit 2), never a guess. The self-test's no-URL case must return 2.
2. P1, queued runs could fill the per-workflow limit and hide a completed failure: verified. The run list asks `gh` for completed runs only (`--status completed`); the fake run list returns twenty queued runs unless that filter is passed, and a mutant without it fails.
3. P2, the independent pass and the plan review kept the old outage rules: verified. The independent pass follows the full retry-then-`Review pending:` rule; the plan review retries with the same backoff and, being advisory, records a persistent outage and continues, while the panel and stamp rounds that need the reviewer still park.
4. P2, `--dispatch` could not supply workflow inputs: verified (`release.yml` requires `tag`). `--field name=value` passes inputs through, `process-phase` says to re-dispatch with the inputs the failed run used, and a mutant that drops them fails the self-test.

## Round 4: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:40:51Z
- Effort: xhigh
- Lines: 19
- Digest: 308e3f2f9a6fb593

## adversarial: needs-attention

1. P1 `scripts/ci_watch.py:54`: workflows are deduplicated by display name instead of identity. An in-memory probe with two active workflow IDs named `checks`, one newer success and one older failure, returned `([], 1)`, hiding the failed workflow and permitting exit 0. Preserve each workflow’s ID when aggregating; `gh` exposes `workflowDatabaseId`. [GitHub CLI fields](https://cli.github.com/manual/gh_run_list)

## consistency: approve

## integration: needs-attention

2. P2 `.claude/skills/review-todo-section/SKILL.md:153` and `:128`: the main panel’s outage rule says to retry the same round, but its keep folder is allocated per round. After a timeout leaves `sol.stderr.txt`, repeating the prescribed `round-N` invocation returns exit 2, “use a fresh folder per attempt,” before starting a reviewer. Allocate separate attempt folders for panel retries, as the corrected completion path does.

## source-defect: needs-attention

3. P1 `scripts/ci_watch.py:37`: GitHub commands do not pin the repository. An inherited `GH_REPO` redirects both monitoring and repair dispatches. A mocked subprocess probe with `GH_REPO=example/other` returned exit 0 using that repository’s green runs; `--dispatch` likewise targets the other repository. Bind every call to the validated repository explicitly. [GitHub CLI environment semantics](https://cli.github.com/manual/gh_help_environment)

## record: approve

HIGHEST: P1

OVERALL: needs-attention

## Response to round 4

Every finding was verified against the code and the cited documentation and is real.

1. P1, workflows were deduplicated by display name: verified. Runs carry `workflowDatabaseId` and are keyed by it, so two workflows sharing a name stay apart; a self-test case and a mutant keyed by name cover it.
2. P2, a panel retry reused its round's keep folder: verified. Each retry of a round runs in its own folder, `$RUNDIR/round-<N>-retry-<K>`, with its own summary, created first.
3. P1, `gh` calls were not bound to this repository: verified (an inherited `GH_REPO` redirects them). `ci_watch.py` reads the repository from `origin` (https or ssh), refuses a non-GitHub origin, passes `--repo owner/name` on every call, and removes `GH_REPO` from the call's environment; self-test cases and a mutant cover the binding.

## Round 5: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:49:19Z
- Effort: xhigh
- Lines: 21
- Digest: 41ed313149bfd654

## adversarial: needs-attention

1. P1 `scripts/todo-graph.py:5461`: `Review pending:` does not invalidate a checked row. An in-memory probe adding it to `D00 T01 §1` returned resolve exit 3, plan status `verified`, and validation exit 0. This matters for `.claude/skills/review-todo-section/SKILL.md:289`, whose stamp-outage path starts after the stamp and row flip are staged. Parking must explicitly unwind that state, and validation must reject a pending review alongside a verified row.

2. P3 `scripts/ci_watch.py:85`: workflow enumeration retains GitHub CLI’s implicit 50-workflow limit. A fixture with 51 active workflows, only the last failing, produced `checked=50`, `red=0`, exit 0. The per-workflow run queries therefore still cannot guarantee that every workflow was checked. [GitHub CLI workflow-list documentation](https://cli.github.com/manual/gh_workflow_list)

## consistency: approve

## integration: needs-attention

3. P2 `scripts/ci_watch.py:117`: dispatch verification returns exit 0 for `skipped` and `neutral`, but `scripts/campaign_guard.py:736` accepts repair evidence only for `success`. In-memory probes reproduced exit 0 followed by `green_evidence=False` for both conclusions. The prescribed repair path therefore reports green but cannot close its repair episode.

## source-defect: needs-attention

4. P1 `scripts/ci_watch.py:47`: repository binding still inherits `GH_HOST`. A probe with `GH_HOST=github.corp.example` produced `--repo rizonesoft/Isotone` while preserving that host override. GitHub CLI resolves this hostless repository argument against its default host, so monitoring and repair dispatches can target another server’s repository. Round 4 settles `GH_REPO`, but the hostname must also be bound explicitly. [GitHub CLI repository resolution](https://github.com/cli/cli/blob/v2.102.0/internal/ghrepo/repo.go#L36-L49), [environment documentation](https://cli.github.com/manual/gh_help_environment)

## record: approve

HIGHEST: P1

OVERALL: needs-attention

## Response to round 5

Every finding was verified against the code and the cited documentation and is real.

1. P1, `Review pending:` on a verified row was neither refused nor unwound: verified. `validate` raises the new FATAL class `review-pending-verified` (in `todo/README.md`'s severity table), with a self-test case that fails on a mutant without the rule; the stamp-review outage path first unwinds the staged stamp, row flip, and plan sync (`git restore --staged --worktree`) before writing the marker.
2. P3, `gh workflow list` stops at 50 workflows: verified. The list asks for up to 1000; a fixture with 51 workflows, only the last red, must report it, and a mutant without the limit fails.
3. P2, a dispatched `skipped` or `neutral` run exited 0 but cannot close a repair: verified. Only `success` exits 0; `skipped` and `neutral` are unverifiable (exit 2), since they ran nothing that could fail; self-test cases and a mutant cover both.
4. P1, `GH_HOST` still redirected a hostless `--repo`: verified. The repository is bound as `host/owner/name` from `origin`, and `GH_HOST` is removed from the call's environment with `GH_REPO`; self-test cases and a mutant cover it.

## Round 6: none

- Writer: claude
- Run: 2026-10-23T01:57:20Z
- Skipped: sol (exited 1)
- Lines: 1
- Digest: 0555d87060386853

No reviewer returned a review. This round is not an approval.

## Round 7: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T06:01:08Z
- Effort: xhigh
- Lines: 21
- Digest: 05719cb506e95e61

## adversarial: needs-attention

1. P1 `scripts/ci_watch.py:92` and `scripts/ci_watch.py:80`: a successful PR run can conceal a failed `main` push. Branch filtering does not exclude PR events. An in-memory fixture with one failed push followed by a successful PR from a fork’s `main`, sharing the workflow ID, returned `([], 1)`, permitting exit 0 without repairing main. [GitHub CLI source](https://github.com/cli/cli/blob/v2.102.0/pkg/cmd/run/shared/shared.go#L348-L374)
2. P1 `.claude/skills/review-todo-section/SKILL.md:179` and `docs/completion-review-prompt.md:33`: completion review lacks an output-validation gate or a retry rule for malformed responses. A mocked successful reviewer returning only `OVERALL: complete`, without the required `HIGHEST` line or evidence of consuming the candidate, was accepted by the dispatcher. Unlike panel review, this path has no subsequent checker to reject truncated output before recording completion.

## consistency: needs-attention

3. P2 `.claude/skills/process-todo-section/SKILL.md:149` and `docs/plans/2026-10-23-native-replan.md:45`: at `571cb71`, “genuinely nothing to exceed” permits an unrestricted exception to the mandatory improvement. A competitor-facing feature can claim that exception without an improvement or proof checkpoint, contradicting `AGENTS.md` and `docs/dev/decisions.md:77`. The exception must distinguish non-feature work.

## integration: approve

## source-defect: needs-attention

4. P2 `scripts/ci_watch.py:43`: repository parsing searches for a substring instead of validating the URL’s host. Both `https://notgithub.com/rizonesoft/Isotone.git` and `https://example.com/github.com/rizonesoft/Isotone.git` returned `github.com/rizonesoft/Isotone` in probes. Consequently, monitoring and repair dispatch can target a GitHub repository unrelated to the actual origin instead of refusing it.

## record: needs-attention

5. P3 `docs/dev/decisions.md:79`: “the sections already written carry their paragraphs” is false at the reviewed commit. `git grep -n -F '**Exceed:**' 571cb71 -- todo` returned no matches, exit 1. The record should describe the paragraphs as work still owed by correction and re-planning.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 6

Round 6 ran at `571cb71` after the capacity outage recorded above. Every finding was verified; finding 3 was already answered by `d3774c1`.

1. P1, a green pull request run could hide a red push on `main`: verified (branch filtering keeps pull request events). The watch keeps only events about `main` itself (push, schedule, dispatch, repository dispatch, workflow run, merge group); a self-test case and a mutant cover it.
2. P1, the completion review had no output gate: verified. `scripts/completion_check.py` requires a `CANDIDATE: <sha>` receipt matching the tip, well-formed numbered findings tagged `in-scope` or `out-of-scope`, a `HIGHEST:` line, a final `OVERALL:` line, and a verdict that agrees with the findings; a FAIL is a round with no review and is retried, never a pass. Its self-test has ten cases and fails on two mutants; the prompt states the receipt, step 5a runs the check, and check-all runs the self-test.
3. P2, the unrestricted "nothing to exceed" exception: already answered by `d3774c1` (only non-feature work is exempt).
4. P2, the repository match accepted look-alike hosts: verified. The whole remote URL is matched, scheme and host included; `notgithub.com` and a path containing `github.com` name no repository, with self-test cases.
5. P3, the decision record said existing sections carry the paragraph: verified false. It now says no section carries it yet and each gains it when corrected before building or rewritten by its re-plan section.

## Round 8: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T06:24:35Z
- Effort: xhigh
- Lines: 19
- Digest: b28f906066e25c6a

## adversarial: needs-attention

1. P1 `scripts/ci_watch.py:97` and `:82`: PR filtering happens after the 20-run fetch limit. A fixture containing one failed main push followed by twenty completed PR runs for the same workflow reproduced exit 0 and `0 workflow(s) checked, 0 red`; processing the full history correctly reported the failure. Round 6’s answer therefore protects only failures still inside the fetched window. Paginate until an eligible run is found, or filter events before limiting. [GitHub CLI limit semantics](https://cli.github.com/manual/gh_run_list)

## consistency: approve

## integration: needs-attention

2. P2 `scripts/ci_watch.py:40` and `:82`: the event whitelist silently excludes legitimate workflows running on main. A completed failed `check_suite` run passed to `red_runs` returned `([], 0)`, allowing a green report without checking that workflow. GitHub documents `check_suite` workflows as running against the default branch. Excluding PR runs must not silently exclude other main workflows. [GitHub event documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#check_suite)

## source-defect: needs-attention

3. P2 `scripts/ci_watch.py:37`: anchoring the remote regex still does not validate the URL’s hostname. Both `https://example.com#@github.com/rizonesoft/Isotone.git` and its `?@github.com` variant returned `github.com/rizonesoft/Isotone`, while URL parsing identifies `example.com` as their host. The optional userinfo expression consumes query and fragment delimiters, so monitoring and repair dispatch can still target a repository unrelated to origin. Parse and validate URL components before constructing the repository binding. [Python URL parsing](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit)

## record: approve

HIGHEST: P1

OVERALL: needs-attention

## Response to round 7

Every finding was verified against the code and the cited documentation and is real.

1. P1, pull request filtering ran after the fetch limit: verified. Each workflow is read in widening windows (20, 100, 500, 1000 completed runs on `main`) until one is about `main` itself or its history ends; a fixture with a red push behind twenty pull request runs must report it, and a mutant with one window fails.
2. P2, the event allow-list dropped `check_suite` and other main workflows: verified. The watch now excludes only pull request events and keeps every other event, with a `check_suite` case.
3. P2, the remote pattern accepted hosts hidden behind `#@` or `?@`: verified. The remote is parsed with `urlsplit` (scheme `https` or `ssh`, host exactly `github.com`, no query or fragment, a strict `owner/name` path) or matched as a strict scp-like form; both spoofs and a GitHub URL with a fragment name no repository, and mutants fail.
