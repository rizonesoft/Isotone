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

## Response to round 1

All six findings verified against the code and fixed in `dbbcd6f`: F1 and F2 (`launch` and `watch` read liveness under the guard lock, `launch` returns `busy` beside any live session and `starting` within five minutes of an earlier launch), F3 (the launcher joins its job object before starting the server), F4 and F5 (the watchdog signature is the Stop hook fingerprint, self-test cases `a-bookkeeping-note-is-not-watchdog-progress` and `an-untracked-edit-is-watchdog-progress`), F6 (the resume prompt reconciles the heartbeat job and replaces it only when missing). The record lens statements were corrected with them.

## Round 2: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T01:04:35Z
- Effort: medium
- Lines: 20
- Digest: e71821158e926098

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1497`: The five-minute reservation can expire while its launcher remains able to start Claude. PowerShell never revalidates the decision before spawning at `scripts/start-campaign.ps1:75`. **Reproduce:** suspend the first launcher after `launch`, wait 301 seconds, invoke another launcher, then release the first. An in-memory probe returned two `start` decisions with different session IDs. Both can start, and the overwritten launch record can disable recovery for whichever acquires the guard.

2. P1 `scripts/campaign_guard.py:1475`: Claude starts before its restart attempt is persisted. A failed `_write_json`, or termination between spawn and persistence, leaves a paid resume uncounted. **Reproduce:** prevent replacement of `claude-campaign-watch.json`, let each resumed process exit without changes, and repeat ticks. Injecting that persistence failure produced five unchanged resumes without reaching the three-resume ceiling. Persist the attempt before spawning.

## consistency: approve

## integration: needs-attention

3. P2 `scripts/campaign_guard.py:1292`: The watchdog prompt jumps directly to heartbeat step 7, bypassing step 6’s mandatory refusal when the stall counter reaches two trips. **Reproduce:** leave a dead owner with `claude-campaign-state.json` containing `trips: 2`, a matching launch record, and runnable work. The watchdog spawns it with instructions to resume work instead of executing the required stall closeout. Resume through the heartbeat’s decision sequence before entering step 7.

## source-defect: approve

## record: needs-attention

4. P2 `scripts/lsp-launch.py:16`, `tools/claude-plugins/README.md:14`: The claim that servers end with a killed session exceeds the containment implemented. The job binds servers to the Python launcher; nothing here binds that launcher to Claude’s lifetime. **Reproduce:** run the launcher beneath a parent process with a server that remains blocked, then terminate only the parent. A controlled process probe left both launcher and server alive. Windows does not automatically terminate children when their parent exits. [Microsoft process termination documentation](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process).

HIGHEST: P1
OVERALL: needs-attention

## Response to round 2

All four findings verified and fixed in the commit that carries this response: F1 (the launch record names the launcher process, and holds its place for as long as that process lives; the shortcut no longer passes `-NoExit`), F2 (the attempt is written before anything is started; self-test `a-failed-start-still-uses-its-attempt`), F3 (`watch` starts nothing once the Stop hook breaker has tripped twice, self-test `watch-honours-the-stop-hook-breaker`, and the resume prompt runs the heartbeat steps 2 to 7 in order), F4 (the launcher also exits when the process that started it exits, and the documents say exactly that).
