---
name: process-phase
description: Runner that takes one phase of todo/implementation-plan.md to 100% -- repair the phase, verify spine dependencies, gap-check it, then ship section after section via process-todo-section plus review-todo-section, parking only when every leftover row is blocked or runnable-elsewhere in this context. Use when the user says process, run, or finish a phase.
---

# Process Phase

One phase of `todo/implementation-plan.md`, driven straight on `main` to 100% completion, or parked when every remaining row is blocked or runnable-elsewhere (`docs/todo-workflow.md`). Never stop mid-phase on questions you can resolve from the source, specifications, measurements, or driven runs (`AGENTS.md`); obey an explicit operator stop/pause immediately by ending the run guard first.

**Three valid endings only:** all rows `[x]` with a written closeout (`## Closeout run=<run id>`), every leftover row blocked/runnable-elsewhere with a written park record (`PARKED <UTC> run=<run id> <reason>` at column 0), or an explicit operator pause. Never bypass a gate (`--no-verify`, `--amend`, force-push, feature branches, and secondary worktrees are forbidden).

## Step 0 -- open the phase run

1. Check `git status -sb` on `main` for unfamiliar uncommitted edits.
2. Open `docs/phase-runs/<YYYY-MM-DD>-phase-<N>.md` (reading any prior run file for Phase `<N>` first) with sections `## Phase repairs`, `## Shipped-row verification`, `## Gap audit`, `## Sections`, `## Critical events`, and `## Lessons`. Append findings as they happen so nothing is lost on crash.
3. Record `- run start: <git rev-parse HEAD>` in `## Critical events` plus the phase's line from `python scripts/todo-graph.py query budget`. Every section this run discovers on its own carries `**Origin:** discovered run=<run id> <YYYY-MM-DD> -- <source>` under its heading (`run_id` from `build/claude-campaign-guard.json`).
4. **Run guard:** if entered from `process-plan`, verify `build/claude-campaign-guard.json` names this session's `Conversation ID` and the `schedule` heartbeat task is active (`manage_task` `list`). If invoked standalone for one phase, start the guard exactly as `process-plan` specifies, passing `--scope phase` instead of `--scope plan`.

## Step 1 -- repair the phase and verify dependency spine

1. Run `python scripts/todo-graph.py validate` and fix any FATALs. Drain any section in this phase marked `> **Review pending:**` once through `review-todo-section` before picking new work.
2. Run `python scripts/todo-graph.py plan --check` (and `plan --sync` if stale).
3. Run `python scripts/todo-graph.py resolve '<ref>'` on every open row in this phase: exit `0` is runnable now; exit `4` with unmet dependencies outside this phase or runnable-elsewhere in this context is a leftover (never drag later-phase rows across phases); exit `1`/`2` is repaired immediately against the TODO file.
4. Scan open sections' TODO files for phase-level drift and correct with `**Corrected YYYY-MM-DD:**` notes.
5. **Spine check:** for shipped `[x]` rows in this phase that an open row here depends on, confirm `resolve` exits `3` with a valid stamp/receipt and re-run their `Test checkpoint`; if any regressed, reopen and repair via `review-todo-section` in audit stance (`todo-graph.py unstamp`).

## Step 2 -- gap-audit the phase

Read the phase end to end as a user and check for unowned surfaces, dead controls, or domain handoff gaps. Route every gap through `add-todo` the same turn (admission test decides live section/item with `**Origin:**` versus `todo/backlog.md`), place new live rows into the phase table where dependencies allow, run `python scripts/todo-graph.py plan --sync`, and log every filing in `## Gap audit`.

## Step 3 -- ship row by row (`process-todo-section` -> `review-todo-section`)

For each runnable-now `[ ]` row in table order, run `process-todo-section` (which runs pre-build `plan` review, builds on `main`, runs gates, and commits) followed immediately by `review-todo-section` (which runs `round`, `completion`, any `reconciliation`, `todo-graph.py stamp`, `todo-findings.py --write`, and the stamp commit).

At every section boundary (after each stamp):

1. Check growth (`python scripts/todo-graph.py query growth --since <run start>`), check heartbeat health and 7-day expiry (`manage_task` `list`, `python scripts/campaign_guard.py health --session <Conversation ID> --jobs <ids>`, `python scripts/campaign_guard.py expiry --session <Conversation ID>`), and retry any `> **Review pending:**` row in scope.
2. When remote pushes/CI are active on `origin/main`: verify push CI (`python scripts/ci_status.py --sha (git rev-parse HEAD) --wait` and `python scripts/review_prompt.py ci-wait <HEAD> --since <before>` plus `--workflow build --workflow-path .github/workflows/build.yml`), run `python scripts/ci_watch.py` across scheduled/dispatched workflows on `main` (repairing any red workflow within the bounded 3-attempt episode tracked by `python scripts/campaign_guard.py repair attempt|close|status`), and run `python scripts/merge_prs.py run --campaign` (`D00 T01 §12`, holding run-file notes in `build/merge-recovery-notes.txt` until the clean-tree merge/recovery check settles, then appending to the phase run file).
3. On release sections (`<app>-v*`, `isotone-v*`), complete the `todo/backlog.md` review item (`add-todo` promotion or operator deferral; in unattended mode, park if unreviewed entries require operator deferral words).

Re-check skipped rows after each stamp as dependencies clear. When only blocked or runnable-elsewhere rows remain, write the column-0 `PARKED <UTC> run=<run id> <reason>` record in `docs/phase-runs/<YYYY-MM-DD>-phase-<N>.md`, commit it on `main`, end the guard if standalone (`--reason park` + `manage_task` `kill` + `cancel-confirmed`), and return to `process-plan`.

## Step 4 -- closeout

When every row in the phase is `[x]`:

1. Invoke `process-todo-file` on every TODO file touched by this phase (full closeout when exhausted, sweep-only when later-phase rows remain).
2. Run `pwsh scripts/check-all.ps1` and `python scripts/todo-graph.py plan --check`.
3. Write `## Closeout run=<run id>` in the phase run file (shipped rows, repairs, closed files, `query budget`, `query growth --since <run start>`, and backlog changes), commit on `main`, end the guard if standalone (`--reason closeout`), and return to `process-plan` (or report if standalone).

## Guardrails

- Never ship rows outside `process-todo-section` + `review-todo-section`, and never tick `todo/implementation-plan.md` by hand.
- Never leave a standalone run guarded after closeout, park, or operator stop, and never use em/en dashes (`--` only).
