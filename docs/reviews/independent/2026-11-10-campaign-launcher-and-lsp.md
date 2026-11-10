## Round 1: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T00:49:40Z
- Effort: medium
- Lines: 26
- Digest: 57df6e0931baf9a3

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1469`: Launching is not atomic with reserving the writer. `launch()` releases its lock before PowerShell starts Claude, without recording a pending launch. Two shortcut invocations before `acquire` both receive `start`, with different session IDs; the second overwrites the first launch record. If the first session acquires the guard, its launch record no longer matches and watchdog recovery is disabled. A tick can likewise race the launcher because its liveness snapshot at line 1417 precedes the graph queries and lock. **Reproduce:** pause the shortcut after `launch`, invoke another shortcut or watchdog tick, then release both. In-memory probes confirmed both launch decisions and the stale-snapshot spawn.

2. P1 `scripts/start-campaign.ps1:62`: A different live Claude session only produces a warning, then execution starts or resumes the campaign anyway. `launch()` refuses only the guard owner’s session, despite returning all other live sessions in `live_here`. This violates the explicit rule against starting beside any live session in the folder. **Reproduce:** leave another Claude session open in this repository and invoke the shortcut with no guard or a dead campaign owner. The mocked decision returned `resume` with another session live.

3. P2 `scripts/lsp-launch.py:129`: The server starts running before it is assigned to the kill-on-close job. Terminating the launcher between `Popen` and assignment leaves an unbound server. A shim can also create descendants before assignment; assigning its parent afterward does not retroactively contain those descendants. **Reproduce:** break immediately before line 131, terminate the launcher, and inspect the server process. Create the process already associated with the job, or suspend it until containment is established. [Windows job inheritance rules](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) apply only after association.

## consistency: needs-attention

4. P2 `scripts/campaign_guard.py:1391`: The new progress signature omits untracked file contents. `git status --porcelain` records their paths, while `git diff HEAD` excludes them. Repeated changes within an existing untracked file or directory therefore look like no progress and can exhaust the three-resume limit. The existing `fingerprint()` already handles untracked contents. **Reproduce:** create an untracked source file, sample the signature, change its contents without changing its path, and sample again. The signature remains unchanged.

## integration: needs-attention

5. P1 `scripts/campaign_guard.py:1439`: Mandatory resume bookkeeping defeats the restart ceiling. `RESUME_PROMPT` requires appending a timestamped `- bookkeeping: watchdog resume ...` event, but `_World.signature()` includes that tracked run-file diff. Each otherwise stalled resume changes the signature and resets `restarts` to zero. The existing Stop-hook fingerprint explicitly excludes bookkeeping lines; the watchdog does not. **Reproduce:** let each resumed session append only its required bookkeeping event and exit. Six simulated ticks all returned `resumed, attempt 1`. This permits indefinite paid resumes without implementation progress.

## source-defect: advisory

6. P3 `scripts/campaign_guard.py:1282`: The prompt states that the heartbeat job died with the process. Claude Code documents that unexpired recurring `CronCreate` tasks are restored on `--resume`. The reconciliation step can accommodate this, but the explanation incorrectly presents replacement as universally necessary. **Reproduce:** create a recurring task, exit, resume the session, and inspect `CronList`. Update the wording to distinguish restored, expired, and missing tasks. [Claude Code scheduling limitations](https://code.claude.com/docs/en/scheduled-tasks#limitations).

## record: needs-attention

The guarantees recorded at `docs/dev/decisions.md:169` and `docs/dev/decisions.md:170` are unsupported: “never beside a live session” fails under findings 1 and 2, and the three-resume stall bound fails under finding 5. The unconditional server-lifetime guarantee at `scripts/lsp-launch.py:14` also exceeds what its startup sequence guarantees under finding 3.

HIGHEST: P1
OVERALL: needs-attention
