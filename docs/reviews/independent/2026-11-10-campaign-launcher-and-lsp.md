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

## Round 3: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T01:13:18Z
- Effort: medium
- Lines: 20
- Digest: 55f4e16a503daf75

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1497`: The launch reservation expires while its launcher can still be alive. Pause the first shortcut after `launch` returns, wait over 300 seconds, then invoke another shortcut before either starts Claude. Both receive `start` with different session IDs, and the second overwrites the launch record. Releasing both permits competing writers and can disable recovery for whichever acquires the guard first. An in-memory probe confirmed two distinct starts. Round 1’s launch-race fix remains incomplete.

2. P1 `scripts/campaign_guard.py:1475`: Restart accounting is persisted **after** spawning Claude. Terminating the watchdog between `Popen` and `_write_json`, or failing `_process_started` after `Popen`, leaves an actual resume uncounted. Let that child exit without changing the tree and repeat: the three-resume ceiling can be bypassed indefinitely. Five injected post-spawn failures produced five starts with no persisted watchdog state. Reserve the attempt durably before spawning.

## consistency: approve

## integration: needs-attention

3. P2 `scripts/campaign_guard.py:1292`: The resume prompt jumps directly to canonical heartbeat step 7, bypassing step 6’s mandatory stop after two stall-breaker trips. `watch()` also never checks that breaker state. Reproduce with a dead owner, runnable work, an expired launch reservation, and `claude-campaign-state.json` containing `{"trips":2,"stalled":true}`. The watchdog starts another session and instructs it to continue. The in-memory probe returned `resumed, attempt 1` despite the existing stop condition.

## source-defect: approve

## record: needs-attention

4. P2 `scripts/lsp-launch.py:17`: The claim that a killed session never leaves a language server behind exceeds the implementation. The Python launcher owns the job handle and waits indefinitely at line 137; nothing monitors the Claude process that started it. Killing Claude alone does not close the launcher’s handle. Reproduce with a server shim that remains running after stdin closes, terminate only Claude, and observe the launcher and server survive. Windows terminates the job when its last handle closes, not when an unrelated ancestor exits. [Microsoft job-object documentation](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects). The session-lifetime claim also appears in `tools/claude-plugins/README.md:14`.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 3

Round 3 was dispatched with a prompt that still named the round 2 range (the writer's error updating the scratch prompt), so it re-read the code as it was before the round 2 fixes and repeated round 2's four findings. Nothing new was raised; the fixes are the ones the round 2 response lists. Round 4 names the tip.

## Round 4: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T01:18:26Z
- Effort: medium
- Lines: 20
- Digest: 02984c8df9f70700

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1365`: Liveness checks require an exact working-directory match. A live Claude session started in `R:\GitHub\Isotone\native` is ignored, although it can edit the same repository. Both `watch()` and `launch()` can consequently start a competing writer. **Reproduce:** open Claude from `native/`, leave a dead campaign guard, then invoke the launcher or watchdog. An in-memory probe at the tip returned `resume` and `resumed, attempt 1` with that live session present. Detect ownership of the working tree, including sessions started in its subdirectories.

## consistency: approve

## integration: needs-attention

2. P2 `scripts/campaign_guard.py:1432`: A surviving launcher shell permanently suppresses recovery after Claude exits. `start-campaign.ps1:51` records `$PID`, but running `& ./scripts/start-campaign.ps1` from an existing PowerShell session leaves that process alive after the script returns. **Reproduce:** invoke it this way, terminate Claude without ending its guard, and leave PowerShell open. Every watchdog tick reports `the launcher is starting this session`; another launcher returns `starting`. The tip’s in-memory probe confirmed both decisions. Release the reservation when the launched command finishes while preserving protection during startup.

## source-defect: needs-attention

3. P2 `.claude/settings.json:39`: The directory marketplace uses a relative path where Claude Code documents an absolute path. Existing manual marketplace registration can conceal the fresh-clone failure. **Reproduce:** use a fresh Claude configuration, trust this checkout, and inspect plugin loading without first running `plugin marketplace add`. The relative directory registration can leave `isotone-lsp` unavailable. Provision an absolute registration derived from the checkout. See the [directory-source contract](https://code.claude.com/docs/en/settings-reference#marketplace-source-types) and [upstream reproduction](https://github.com/anthropics/claude-code/issues/23978).

## record: needs-attention

Findings 1 and 2 contradict the unconditional writer-exclusion and dead-session recovery claims at `docs/dev/decisions.md:169`, `docs/dev/decisions.md:170`, and `.claude/skills/process-plan/SKILL.md:64`. Their reproduction steps apply to these claims.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 4

Round 4 read the tip and raised three new findings, all verified and fixed in the commit that carries this response: F1 (a session started in any folder under the working tree counts as live here; self-test `a-session-in-a-subfolder-is-live-here`), F2 (the launcher runs `launch-done` when its session ends, so a shell left open frees its place; self-tests `an-open-launcher-holds-its-place`, `another-launcher-cannot-release-it`, `a-finished-launcher-frees-its-place`), F3 (the relative `extraKnownMarketplaces` entry is removed; the launcher registers the plugin folder per machine from where the clone is, and the README gives the same commands).

## Round 5: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T01:26:45Z
- Effort: medium
- Lines: 18
- Digest: b745eab0285930b5

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1404`: An incomplete session record bypasses writer exclusion. If a record names a running PID and this repository but omits `procStart`, the comparison silently drops it. Both `launch()` and `watch()` can then start beside that live session. This contradicts the stated rule that an unjudgeable record raises. **Reproduce:** supply a session record with valid `pid`, `sessionId`, and `cwd`, but no `procStart`, while `_process_started()` returns that process’s creation time. The tip’s in-memory probe returned `[]`. Validate required identity fields and refuse startup when identity cannot be established.

## consistency: approve

## integration: needs-attention

2. P2 `scripts/start-campaign.ps1:71`: Startup preparation occurs outside the `try/finally` that releases the launch reservation. A terminating error in scheduler-status parsing or marketplace setup leaves the reservation attached to the surviving PowerShell process indefinitely. The round 4 cleanup fix therefore covers Claude execution, but not the preceding startup failures. **Reproduce:** invoke the script from an existing PowerShell shell with Python available but `claude` unavailable. `launch` reserves the shell’s PID, line 83 throws, and `launch-done` never executes. After making Claude available, subsequent launches report `starting` while that shell remains open. Put all work following reservation acquisition inside the cleanup scope.

## source-defect: approve

## record: needs-attention

3. P2 `docs/dev/decisions.md:169`: The recorded reservation lifetime ends “when its session ends and it runs `launch-done`,” but finding 2 leaves a reservation indefinitely even though no session started. **Reproduce:** use finding 2’s startup-failure sequence. The implementation must release failed startup reservations before this lifecycle claim holds.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 5

Three findings, all verified and fixed in the commit that carries this response: F1 (a session record whose process runs but which has no `procStart` raises, so nothing starts; self-tests `a-record-that-cannot-be-judged-starts-nothing`, `a-reused-process-id-is-not-the-session`), F2 and F3 (everything the launcher does after `launch` sits inside the one `try`/`finally` that runs `launch-done`, and the decision record says so). The commit before this one (`fix(workspace): count sessions in subfolders as live ...`) went in with two self-test cases failing, `watch-drained-starts-nothing` and `watch-ignores-another-runs-record`: they asserted a fixed spawn count that the new cases had shifted, and the writer's command chain did not stop on the failure. Both assert a relative count now, and the self-test exits 0 with 225 cases.

## Round 6: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T01:33:10Z
- Effort: medium
- Lines: 20
- Digest: 2ff603c1a0cc0e1c

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1532`: A spawned resume can remain unrecorded, allowing a competing writer. Restart accounting is persisted before spawn, but child identity is persisted afterward. **Reproduce:** suspend the child before Claude writes its session record, then terminate the watchdog between `Popen` and the final state write. Invoke the launcher: it sees neither a recorded child nor a live session and authorizes another resume. An in-memory probe confirmed `child_exists=True`, no persisted child, and `next_launcher_action='resume'`.

2. P1 `scripts/campaign_guard.py:1356`: Failed Windows liveness queries are treated as proof of death. Both a failed `GetExitCodeProcess` and a failed `GetProcessTimes` return `None`, which `_session_live()` interprets as dead. This bypasses the latest fix’s refusal of unjudgeable sessions. **Reproduce:** keep a valid session record and inject a false return from `GetProcessTimes` for its running process. The probe returned `started_result=None` and `treated_as_live=False`; startup can proceed beside that session. Query failures must remain errors.

3. P1 `scripts/campaign_guard.py:1508`: A live session record with missing or empty `cwd` silently bypasses writer exclusion. `_session_live()` accepts its matching PID and `procStart`, but `_in_tree(None, root)` returns false; `launch()` repeats the same filtering. **Reproduce:** supply a record with a running PID, matching creation time and session ID, but omit `cwd`. Both decisions ignore the session instead of refusing an unjudgeable record. The in-memory probe confirmed that its identity passes while its folder filter excludes it.

## consistency: approve

## integration: approve

## source-defect: approve

## record: needs-attention

4. P2 `.claude/skills/process-plan/SKILL.md:64`: The unconditional claim that the watchdog “never starts beside a live session” remains unsupported. The lock does not cover an unrecorded surviving child, and unknown liveness can still become absence. **Reproduce:** use findings 1 through 3. The documented guarantee must be backed by those failure paths before it can be recorded as delivered.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 6

Four findings, all verified and fixed in the commit that carries this response. The exclusion rule was re-thought as fail-closed, not patched case by case: F2 (a process query that fails raises; only a missing or exited process reads as gone), F3 (a running session whose record lacks `sessionId` or `cwd` raises; self-tests `a-live-record-without-sessionId-starts-nothing`, `a-live-record-without-cwd-starts-nothing`), F1 (the watchdog writes a `spawning_at` mark with the attempt before it spawns; the mark holds the place for five minutes when no child was recorded, in `watch` and in `launch`; self-test `an-unrecorded-resume-holds-its-place`; a start that fails cleanly clears it), F4 (the skill states those three conditions).

## Round 7: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T01:40:09Z
- Effort: medium
- Lines: 18
- Digest: e8ee61ccd24d8cd7

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1563`: The exception handler clears the startup reservation even when Claude has already spawned. `_World.spawn()` calls `Popen` before `_process_started(child.pid)`, which can now raise on a failed process query. **Reproduce:** suspend the child before its session record appears and inject a `GetProcessTimes` failure after `Popen`. The handler removes `spawning_at` without recording or terminating the child. An immediate launcher invocation authorizes another resume. The in-memory probe confirmed `child_exists=True` and `next_launch='resume'`. Distinguish failure to create a process from failure to identify an existing child.

2. P1 `scripts/campaign_guard.py:1477`: The five-minute reservation expires without establishing that an unrecorded child died. **Reproduce:** suspend a spawned child before it registers its session, terminate the watchdog before it persists the child identity, wait 301 seconds, then invoke the launcher or another tick. Both ignore the expired marker and can start another writer while the first child remains alive. The in-memory probe returned `starting` before expiry and `resume` afterward with the child still present. Elapsed time alone cannot safely release uncertain process ownership.

## consistency: approve

## integration: approve

## source-defect: approve

## record: needs-attention

3. P2 `.claude/skills/process-plan/SKILL.md:64`, `docs/dev/decisions.md:170`: The unconditional claim that recovery never starts beside a live session remains unsupported. Findings 1 and 2 reproduce competing-start authorization at the specified tip. The round 6 response also describes process-query failures as fail-closed, but the post-spawn exception path clears the very reservation needed to preserve exclusion.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 7

Both P1 findings are real, and they are the third and fourth window found in a reservation built on timestamps and recorded process ids, so the unit was re-thought instead of patched again (the skill's rule for a unit patched three rounds running). The commit that carries this response replaces `launch`, `launch-done`, the launch grace window, and the `spawning_at` mark with one session slot: an operating-system lock (`build/claude-campaign-session.lock`) that `start` (the launcher) and `resume-headless` (the watchdog's supervisor) each take in the process that then runs Claude Code and stays alive until it ends, with Claude Code inside a kill-on-close job object (`scripts/lib/win_job.py`). The lock is held by a live process or free, so no elapsed time releases it (F2) and no failure after the spawn can drop it while the session lives (F1). `watch` only asks for a resume; the supervisor decides again under the slot and writes the attempt before it runs anything. Proved with real processes in a throwaway workspace: while a supervisor's session ran, the slot read held from another process, a second supervisor and `start` each exited 3, and killing the supervisor ended its session processes and freed the slot. Self-test: 231 cases, 0 failed.

## Round 8: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T01:53:02Z
- Effort: medium
- Lines: 20
- Digest: d9f5a2b72215ed05

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1604`: Writer exclusion still uses a liveness snapshot that can become stale before Claude starts at line 1620. Ordinary Claude sessions do not acquire `_SessionSlot`. **Reproduce:** pause the supervisor after `_live_in_tree()` returns empty, start an ordinary Claude session in this repository, then release the supervisor. It starts the campaign beside that live session. An in-memory probe reproduced this by introducing the attended session during `world.signature()`: `resume_headless()` still invoked `world.run()`. The slot must coordinate ordinary sessions too for the claimed exclusion guarantee to hold.

## consistency: approve

## integration: needs-attention

2. P2 `scripts/start-campaign.ps1:64`: Plugin installation is conditional on the marketplace being absent, rather than the plugin being absent. **Reproduce:** register this checkout’s marketplace without installing `isotone-lsp`, then invoke the launcher. The registration check succeeds, line 67 is skipped, and the campaign starts without the language servers. A mocked execution confirmed that only `plugin marketplace list` runs. Installation failure after successful marketplace registration leaves the same persistent failure on subsequent launches. Check plugin installation independently and handle its exit status.

## source-defect: needs-attention

Finding 2 relies on an invalid equivalence between marketplace registration, project enablement, and installation. Claude Code explicitly documents that project settings enable plugins but do not install them. See [the documented missing-install condition](https://code.claude.com/docs/en/plugins/troubleshooting#plugin-name-is-enabled-in-project-settings-but-isnt-installed-here).

## record: needs-attention

3. P2 `docs/dev/decisions.md:169`, `.claude/skills/process-plan/SKILL.md:64`: The unconditional claim that recovery never starts beside a live session exceeds the implementation. Finding 1 reproduces a competing start despite the new session slot. The documentation must distinguish exclusion between cooperating campaign launchers from exclusion against ordinary Claude sessions until both are enforced.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 8

Round 8 accepted the session slot between campaign sessions. Its three findings are fixed in the commit that carries this response. F1: a session the operator opens takes no lock, so certainty there is not available to this module; the starters now read the session records as their last step before running anything (self-test `the-supervisor-reads-liveness-itself`), a `SessionStart` hook (`campaign_guard.py session-note`) tells a session that opens while the slot is held that the campaign is the only writer (self-tests `another-session-is-told-a-campaign-runs`, `the-campaign-session-itself-gets-no-note`), and F3: the skill and the decision record now say exactly that, an instruction and not a lock. F2: the launcher checks the plugin's own installed-and-enabled state from `claude plugin list --json`, installs it when missing, and warns on a failed exit code.

## Round 9: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-11-10T02:00:26Z
- Effort: medium
- Lines: 18
- Digest: 93202929e6b969af

## adversarial: needs-attention

1. P1 `scripts/campaign_guard.py:1640`: The new SessionStart warning misses campaign startup before guard acquisition. **Reproduce:** pause `start()` after its liveness check, before Claude starts; open an ordinary session while no guard exists; then release the launcher. `session_note()` returns empty because `guard is None`, and the launcher starts beside the ordinary session. An in-memory probe confirmed `session_start_note=''` and `campaign_spawned=True` with the ordinary session live. The slot and launch record must protect this interval too.

## consistency: approve

## integration: needs-attention

2. P2 `scripts/campaign_guard.py:1601`: The supervisor does not repeat the drained-plan check before resuming. **Reproduce:** let `watch()` observe runnable work, delay the detached supervisor, and make the plan reach zero runnable rows and zero pending reviews before releasing it. `resume_headless()` still spends an attempt and invokes Claude. An in-memory probe confirmed this with both counts zero. Recheck the drain condition in the supervisor, which is supposed to make the final startup decision.

## source-defect: approve

## record: needs-attention

The SessionStart coverage described at `.claude/skills/process-plan/SKILL.md:64` is incomplete under finding 1: a session opening while the slot is held can receive no warning. The same paragraph’s statement that the watchdog starts nothing when the plan is drained fails under finding 2.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 9

Two findings, both fixed in the commit that carries this response: F1 (the session note names the campaign session from the launch record before the run's first `acquire`, so a session opened during startup is told; self-test `a-session-opened-during-startup-is-told`), F2 (the supervisor rechecks the drained plan under the slot; self-test `the-supervisor-rechecks-the-drained-plan`). The skill text matches both.
