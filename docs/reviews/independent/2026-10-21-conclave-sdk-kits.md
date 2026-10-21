## Round 1: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T00:31:53Z
- Effort: high
- Lines: 25
- Digest: f08bbdba102e3620

## adversarial: needs-attention

1. **[P2] Query failures still block the session silently.** `scripts/campaign_guard.py:259` converts a timeout or launch failure into `(None, "")`; `stop_decision` then continues fingerprinting and blocking. The heartbeat receives no error. Reproduced in memory by making the ready-query subprocess raise `TimeoutExpired`: `decision=block`, `recorded_hook_error=False`. Propagate query failures to the hook’s fail-open error handler.

2. **[P2] The metadata limit no longer limits filesystem calls.** `scripts/campaign_guard.py:786` calls `os.stat()` before checking whether the path exceeds the hashing and metadata limits. Large untracked trees therefore still incur a filesystem operation per file, risking repeated hook delays and budget exhaustion. Reproduced with `CAMPAIGN_HASH_FILES=0`, `CAMPAIGN_STAT_FILES=1`, and three paths: three stat calls occurred. The removed PowerShell hook skipped metadata access beyond the limit.

## consistency: advisory

`standards/delegation.md:34` retains guidance about running validation after `forge.py sync`, although `AGENTS.md:41` explicitly prohibits that command because it overwrites Isotone’s adaptations. This contradiction predates the candidate but remains in the paragraph this candidate updates.

## integration: needs-attention

3. **[P2] The mutation-copy recipe cannot reproduce unstaged deletions.** `.claude/agents/mutation-tester.md:26` requires copying every path returned by `git ls-files --cached --others --exclude-standard`. An unstaged deleted tracked file remains in that listing but has no source to copy. Reproduce with a candidate that deletes an unrelated tracked file while modifying the mutation target: setup fails before the baseline runs. The copy procedure must preserve deletions, including unstaged ones.

## source-defect: needs-attention

4. **[P1] The adaptation drops the SDK’s scratch-ownership safeguard.** `.claude/agents/mutation-tester.md:26` copies into a fixed `<scratch>/mt-copy`, and line 38 unconditionally deletes that directory. Neither step requires it to be absent or newly created by this invocation. Reproduce by supplying a scratch directory containing an existing `mt-copy` with unrelated files: setup merges into it and teardown deletes those files. The SDK explicitly restricts removal to the worktree the agent created; the adapted procedure needs equivalent ownership protection.

Findings 1 and 2 also exist in the SDK guard at `kits/todo/templates/scripts/campaign_guard.py:244` and `:590`. They are inherited source defects.

## record: advisory

The claimed 123-case and 781-case self-test results were not independently rerun because those suites create files. Verification here used candidate-source inspection and in-memory probes. No files were modified.

OVERALL: needs-attention

## Response to round 1

Round 1 reviewed `8c2b243`, `ce1debc`, and `af1944e` (prompt: the run guard, query plan, and mutation-tester group). Every finding was checked against the code and holds; all four are fixed in the next commit, each with a regression case where code changed.

1. Fixed. `ready_rows` raises `GuardError` when `query ready` cannot run, exits non-zero, or prints neither shape, so the hook fails open and records the error for the heartbeat, and `end --reason plan-done` refuses. A phase-scoped run on the text summary still reads an unknown count, as designed. Cases `a-failed-ready-query-fails-open-and-is-recorded`, `plan-done-refuses-an-unreadable-ready-query`, and `an-unreadable-ready-summary-fails-open-and-is-recorded` fail with the old `return None, ""`.
2. Fixed. `fingerprint` counts a path past both bounds by its name before any `os.stat`. Case `past-the-stat-bound-a-path-costs-no-stat` fails with the old order.
3. Fixed. `mutation-tester` skips a listed path that no longer exists in the live tree, so an uncommitted deletion is reproduced in the copy.
4. Fixed. `mutation-tester` creates a fresh `<scratch>/mt-<run>` with `os.mkdir`, stops if it exists, and deletes only that folder.

Consistency advisory: fixed. `standards/delegation.md` now says kit subagents are refreshed by porting SDK changes by hand, never by `forge.py sync`.

Record advisory: noted; the self-test figures are re-quoted from this session's runs in the fix commit (campaign_guard 127 cases, 0 failed).

Findings 1 and 2 also stand in the Conclave SDK's `kits/todo/templates/scripts/campaign_guard.py`; that repository is reported to the operator, not changed from here.

## Round 2: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-10-21T00:44:41Z
- Effort: high
- Lines: 19
- Digest: 38e12471d4452850

## adversarial: needs-attention

1. **Delegate guard bypass through abbreviated arguments.** [scripts/panel_slots.py:214](R:/GitHub/Isotone/scripts/panel_slots.py:214) blocks only `--writer`, but the dispatcher's argparse accepts `--w` and `--wri`. Reproduce with `python scripts/review-dispatch.py --w claude --prompt p --record docs/reviews/probe.md`: `shell_decision()` permits it, and the dispatcher accepts it. Confirmed with in-memory probes. A delegate can launch reviews and write review records despite the guard.

2. **Cancellation destroys the evidence `--keep` should preserve.** [scripts/review-dispatch.py:295](R:/GitHub/Isotone/scripts/review-dispatch.py:295) copies evidence only after `run()` returns normally, while the `finally` block always removes scratch. Interrupt an active review: partial stdout and stderr are deleted without reaching the keep directory. An in-memory `KeyboardInterrupt` reproduction produced zero `keep_file()` calls and one scratch-removal call. The previous direct redirections preserved those bytes.

## consistency: needs-attention

3. **Raw evidence writes are not atomic.** [scripts/review-dispatch.py:266](R:/GitHub/Isotone/scripts/review-dispatch.py:266) copies directly onto the destination; line 268 also writes directly. This violates the required atomic writes for data files. Reproduce by interrupting or fault-injecting a copy after its destination is opened: the retained evidence is incomplete, any previous destination has been truncated, and the enclosing cleanup deletes the source. Publish each evidence file through a temporary sibling and atomic replacement.

## integration: needs-attention

4. **A failed retry leaves a previous approval at the current review path.** [scripts/review-dispatch.py:308](R:/GitHub/Isotone/scripts/review-dispatch.py:308) skips writing `review.md` on failure but neither invalidates an existing file nor refuses a reused keep directory. Run a successful review, then rerun with the same `--keep` directory and a failing reviewer. Confirmed in memory: the second result reports `reviewer: null`, while `review.md` still contains `OVERALL: approve`. The skill's subsequent file-based checker can consume that stale approval, now beside the failed attempt's stderr. Refuse existing attempt artifacts or otherwise prevent their reuse.

## source-defect: approve

## record: approve

OVERALL: needs-attention

## Response to round 2

Round 2 reviewed `1b11445` and `21a2ed5` (the reviewer kit group). Every finding was checked against the code and holds; all four are fixed in the next commit, each with a regression case that fails when the old code is restored.

1. Fixed at both layers. `scripts/review-dispatch.py` parses with `allow_abbrev=False`, so `--w` is refused; and the delegate shell gate now refuses any dispatcher run except its read-only `--check-pin` and `--list-rounds` reports, whatever the option spelling. Cases: `test_an_abbreviated_option_is_refused`, and the shell-gate denials of `--w claude` and `--prompt p`.
2. Fixed. The kept stdout and stderr are copied in the `finally` that removes the scratch, so an interrupt keeps them. Case: `test_an_interrupted_attempt_still_keeps_what_the_reviewer_wrote`.
3. Fixed. `keep_file` publishes through a temporary sibling and `os.replace`, so a kept file is whole or absent. Case: `test_a_failed_copy_leaves_no_partial_kept_file`.
4. Fixed. `--keep` refuses a folder that already holds `review.md` or kept stdout or stderr, before any reviewer runs. Case: `test_a_reused_keep_folder_is_refused_before_any_reviewer_runs`.