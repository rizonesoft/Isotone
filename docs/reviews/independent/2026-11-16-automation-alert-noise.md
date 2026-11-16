## Round 1: astra (`gpt-6-astra` via `codex`)

- Writer: claude
- Run: 2026-11-16T08:30:54Z
- Candidate: 29600db58344f2d5227c7bc969ff6911f7aa188b
- Effort: medium
- Lenses: adversarial, consistency, integration, quality, optimization, source-defect, docs-drift
- Lines: 31
- Digest: 03f87b9152f13673

### adversarial: needs-attention

1. **P2, `.conclave/automations/run.py:272`: Concurrent runs can email the same failure twice.** Reading the previous fingerprint, sending, and replacing the record are not serialized. Reproduce by running the documented `python .conclave/automations/run.py isotone-pr-merge` while its scheduled instance is sending a failure notification. Scheduler `IgnoreNew` does not cover direct Python invocations. An in-memory reproduction with two overlapping calls produced two emails for identical failures. The shared `alerted.json.tmp` also permits competing replacements. Serialize notification state per task, including recovery.

### consistency: approve

### integration: approve

### quality: needs-attention

2. **P3, `scripts/tests/test_automations.py:303`: The trigger test checks spelling, not trigger behavior.** It only forbids `$logon.Repetition` and requires `-RepetitionInterval $every` somewhere in the source. Removing the logon trigger from `$t` would still pass, despite eliminating the behavior named by the test. Inspect the constructed trigger objects through mocked scheduler commands or exported task XML.

### optimization: approve

### source-defect: approve

### docs-drift: needs-attention

3. **P2, `.conclave/automations/README.md:13`: The schedule description still states “every 60 minutes, from 15 minutes after logon.”** The recurring trigger now starts one hour after installation, independently of logon; logon adds a single delayed run. Reproduce by installing at 10:00 and logging on at 10:20: the logon run is at 10:35, while recurring runs remain anchored to 11:00. Document both independent triggers.

4. **P2, `.conclave/automations/alert.py:6`: The module contract still says “run.py calls `send_failure` when a task exits non-zero or times out, so a failed run is reported.”** Repeating an identical failure within 24 hours now returns before that call. Update the comment to describe suppression and reminders, distinguishing the explicit alert CLI from the runner’s policy.

LENS adversarial: findings
LENS consistency: clean
LENS integration: clean
LENS quality: findings
LENS optimization: clean
LENS source-defect: clean
LENS docs-drift: findings
HIGHEST: P2
OVERALL: needs-attention

## Response to round 1

1. Fixed. `run.py` now takes a per-task OS file lock (`build/automations/<name>/alert.lock`, `msvcrt` or `fcntl`, released when the handle closes or the process dies) around the record check, the send, the record write and the pass-time clear, so the shared `alerted.json.tmp` is only written under it. A lock held past `LOCK_WAIT_SECONDS` is reported as an unsent alert (exit 3, said in the log). Tests: `test_overlapping_runs_of_one_failure_send_one_email`, `test_a_lock_held_too_long_is_an_unsent_alert`.
2. Fixed within the installer tests' existing static style (the scheduler cmdlets cannot run hermetically in CI): the test now reads the `$t = @(...)` trigger list and requires the logon trigger in it, exactly one `-RepetitionInterval $every`, on the `-Once` time trigger, and no `.Repetition` assignment anywhere. The live registration was checked on this PC after reinstalling: `MSFT_TaskLogonTrigger` with no repetition and a 15-minute delay, `MSFT_TaskTimeTrigger` repeating `PT1H`.
3. Fixed. The README row now says once 15 minutes after each logon, and every 60 minutes counted from when the installer last ran.
4. Fixed. `alert.py`'s docstring describes the once-per-failure policy and the 24-hour reminder, and says the CLI always sends for the last run.
