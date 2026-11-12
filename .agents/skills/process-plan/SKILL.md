---
name: process-plan
description: Front door for todo/implementation-plan.md. Audits the plan, starts the campaign run guard and heartbeat, and runs process-phase on the first phase with a ready row, chaining phase after phase until every row is shipped, parked, or blocked. --audit is audit only; a named phase runs process-phase without chaining.
---

# Process the Implementation Plan

The campaign front door for `todo/implementation-plan.md` (`docs/todo-workflow.md`). Writes stay serial on `main`, and the session running this skill is the single writer on the repository (`AGENTS.md`). In Antigravity (`agy`), substitute this session's `Conversation ID` (from `<user_information>`) wherever `$CLAUDE_CODE_SESSION_ID` appears below, use `schedule` (`CronExpression: "3-59/5 * * * *"`, `IsDaemon: true`) for `CronCreate`, and use `manage_task` (`list` and `kill`) for `CronList` and `CronDelete`.

## 0. Route

```powershell
git status -sb
python scripts/todo-graph.py validate
python scripts/todo-graph.py query ready
```

- Unfamiliar uncommitted edits from another session -> stop and report.
- Argument `--audit` -> run Section 1 audit and stop without starting the guard.
- Argument names a single phase (`0`, `Phase 0`) -> invoke `process-phase` standalone (`--scope phase`); do not chain.
- Empty argument or whole-plan invocation -> run Section 1 audit, start the Run Guard, drain `review pending` sections, and immediately run `process-phase` on the first ready phase in the same turn, chaining across ready phases until `0 runnable now`. Never end the turn on an audit-only summary when ready work exists.

## 1. Audit the whole plan

```powershell
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --check
python scripts/todo-graph.py query ready
python scripts/todo-graph.py query blocked
python scripts/todo-graph.py query budget
python scripts/review_pin.py --check
python scripts/panel_slots.py delegate-probe
python -m unittest discover -s scripts/tests
```

Fix every FATAL (and run `python scripts/todo-graph.py plan --sync` if stale) before shipping. Record in the first phase's run file (`docs/phase-runs/<YYYY-MM-DD>-phase-<N>.md`): fatal count, `plan --check` status, ready count and first ref per phase, blocked count and blockers, `query budget` summary, review-pin status, starting phase, and `review pending` resume outcomes. If `0 runnable now` and `0 review pending`, report the remaining blocked/elsewhere rows (or run terminal clean-machine acceptance when zero `[ ]` rows remain) and stop.

### Run guard

Starting the first phase starts all four guard layers so unattended runs self-heal across idle turns and crashes:

- **Stop hook** (`python scripts/campaign_guard.py stop-hook` in `.agents/hooks.json`): blocks premature end-of-turn while ready work remains, allowing subagent/background task turns (`fullyIdle: false`) to wait naturally and recording any unexpected error for `python scripts/campaign_guard.py hook-error`. A closeout is a line `## Closeout run=<run id>` and a park is a column-0 `PARKED <UTC> run=<run id> <reason>` line.
- **Stall breaker:** trips after 3 consecutive blocked stops with no repository/run-file progress (ignoring `- bookkeeping:` notes).
- **Heartbeat** (`schedule` recurring cron + `manage_task`): resumes idle turns in-session with full context.
- **Watchdog** (`python scripts/run-guard.py watch`, every 10 minutes via Windows Task Scheduler): resumes a dead campaign session started via `scripts/start-campaign.ps1 -Runner agy|claude` in the runner that owns the guard under the OS session lock (`build/claude-campaign-session.lock`).

Start the guard in exact order:

1. Reconcile first: `CronList` (`manage_task` `list`), then `python scripts/campaign_guard.py reconcile --session $CLAUDE_CODE_SESSION_ID --jobs <comma-separated heartbeat job ids>`, deleting any stale job it names.
2. Mint a generation: `python scripts/campaign_guard.py mint-generation`, then `CronCreate` (`schedule` with `CronExpression: "3-59/5 * * * *"`, `IsDaemon: true`) using the canonical heartbeat prompt below.
3. Acquire the guard: `python scripts/campaign_guard.py acquire --session $CLAUDE_CODE_SESSION_ID --phase <N> --run-file <run file> --cron-id <job id> --generation <generation> --scope plan`. A refused `acquire` means another session owns the run: delete the job just created, start nothing, and report the owner.
4. Settle any prior dependency merge (`python scripts/merge_prs.py recover`, holding run-file lines in `build/merge-recovery-notes.txt` while reconciling `main`), and when remote CI is active verify `main` (`python scripts/ci_status.py` / `python scripts/review_prompt.py ci-wait`).
5. Append the guard acquisition and recovery lines to `## Critical events` in the phase run file, resume any `review pending` sections across all phases once through `review-todo-section`, and enter `process-phase` on Phase `<N>`.

At every section boundary, check heartbeat health and expiry (`python scripts/campaign_guard.py health --session $CLAUDE_CODE_SESSION_ID --jobs <ids>` and `expiry --session $CLAUDE_CODE_SESSION_ID`), replacing expiring jobs before continuing. Every run termination (`closeout`, `park`, `plan-done`, `operator-stop`, `escalation`, `stall`) runs `python scripts/campaign_guard.py end --session $CLAUDE_CODE_SESSION_ID --reason <reason>`, deletes the heartbeat job, confirms deletion, and runs `python scripts/campaign_guard.py cancel-confirmed --cron-id <job> --session $CLAUDE_CODE_SESSION_ID`.

Canonical heartbeat prompt:

```text
Claude run-guard heartbeat for Isotone Phase <N> (run file <run file>, generation <generation>). This session went idle while a campaign run may still be open. Check, then act, in this turn.

1. Run `python scripts/campaign_guard.py whoami --session $CLAUDE_CODE_SESSION_ID --generation <generation>`. If it prints NOT THE OWNER or NOT THE CURRENT JOB, CronDelete this job, confirm it gone with CronList, run `python scripts/campaign_guard.py cancel-confirmed --cron-id <this job> --session $CLAUDE_CODE_SESSION_ID --if-pending yes`, and reply with that line. If it prints MALFORMED GUARD, run step 2, report the malformed guard, and stop.
2. Run `python scripts/campaign_guard.py hook-error --session $CLAUDE_CODE_SESSION_ID`, append any printed line to <run file>'s Critical events, and acknowledge with `--ack "<that line>"`.
3. Run `python scripts/campaign_guard.py pending-cancel --session $CLAUDE_CODE_SESSION_ID`; for any job named, CronDelete it, confirm it gone with CronList, and run `python scripts/campaign_guard.py cancel-confirmed --cron-id <that job> --session $CLAUDE_CODE_SESSION_ID`.
4. If step 1 printed NO GUARD, run `python scripts/campaign_guard.py reset-state --expect-no-guard yes`, CronDelete this job, confirm it gone with CronList, then run `cancel-confirmed` (`--cron-id <this job> --session $CLAUDE_CODE_SESSION_ID --if-pending yes`), and reply RUN FINISHED.
5. If <run file> has `## Closeout run=<run id>` or column-0 `PARKED ... run=<run id>` and step 1 printed scope=phase, run `python scripts/campaign_guard.py end --session $CLAUDE_CODE_SESSION_ID --reason closeout` (or `park`), CronDelete this job, confirm it gone with CronList, then run `cancel-confirmed`, and reply RUN FINISHED. With scope=plan, run `python scripts/todo-graph.py query ready`: if `0 runnable now` and nonzero `review pending`, retry each pending section once through `review-todo-section` and reply WAITING ON REVIEWER; if `0 runnable now` and `0 review pending`, run `python scripts/campaign_guard.py end --session $CLAUDE_CODE_SESSION_ID --reason plan-done`, CronDelete this job, confirm it gone with CronList, then run `cancel-confirmed`, and reply RUN FINISHED.
6. If `build/claude-campaign-state.json` has `trips >= 2`, append the stall cause to Critical events, run `python scripts/campaign_guard.py end --session $CLAUDE_CODE_SESSION_ID --reason stall`, CronDelete this job, confirm it gone with CronList, then run `cancel-confirmed`, and report the stall.
7. Otherwise run `python scripts/merge_prs.py recover` (holding notes in `build/merge-recovery-notes.txt`), verify CI when active, append `- bookkeeping: heartbeat resumed <UTC>` to Critical events, re-run `python scripts/todo-graph.py query ready`, retry pending reviews in scope, and continue shipping from the open section in <run file> (`process-plan` for scope=plan, `process-phase` for scope=phase).
```

## 2. Chaining after phase closeout or park

After `process-phase` closes out or parks a phase, run `python scripts/todo-graph.py query ready`:

- Another phase has a runnable-now row -> cancel the old heartbeat job, schedule a new heartbeat with a fresh generation for the next phase and its `docs/phase-runs/<YYYY-MM-DD>-phase-<M>.md`, re-point the guard via `python scripts/campaign_guard.py acquire` (`--scope plan`), and start `process-phase` on Phase `<M>` in the same turn.
- `0 runnable now` with nonzero `review pending` -> keep the guard and heartbeat live so pending reviews retry on schedule.
- Zero `[ ]` rows remain anywhere -> execute the `05-release` clean-machine acceptance verification before running `end --reason plan-done` and cancelling the heartbeat.

## 3. Guardrails

- Never ship sections outside `process-todo-section` + `review-todo-section`, never tick `todo/implementation-plan.md` by hand, never block an unattended run with `ask_question`, and never use em/en dashes (`--` only).
