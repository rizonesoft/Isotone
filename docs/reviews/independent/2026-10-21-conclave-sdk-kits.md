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