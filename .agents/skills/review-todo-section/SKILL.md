---
name: review-todo-section
description: Quality-gate and stamp an implemented TODO section under the three-pass schedule -- self-review, round pass, completion and excellence pass, reconciliation when gaps are repaired, and deterministic JSON receipt stamping via todo-graph.py stamp. Also runs in audit stance on shipped sections. Use after process-todo-section or when asked whether a section is really done.
---

# Review TODO Section

The gate between "code exists" and `[x]` (`docs/todo-workflow.md`). Nothing flips an Implementation Order row by hand: `python scripts/todo-graph.py stamp` verifies the cross-family `three-pass` review chain in `docs/reviews/<NN-domain>/D<NN>-T<NN>-s<N>.md`, writes the canonical JSON receipt `docs/reviews/<slug>.json`, writes `> **Verified:**` + `> **Review:**`, and syncs `todo/implementation-plan.md`.

Every review pass runs through `scripts/review-dispatch.py --writer agy` against `.conclave/reviewers.toml` (`astra` on `gpt-6-astra` via `codex`, `[schedule] policy = "three-pass"`, `pass_cap = 33`, `blocking = ["P1", "P2"]`, no fallback). The writer's model family never reviews its own work.

## Step 0 -- resolve the argument

```powershell
python scripts/todo-graph.py resolve "$ARGUMENTS"
```

- Exit `0`: open section ready for post-build review and stamping.
- Exit `3`: section is already `[x]` -- run in **audit stance** (below).
- Any other exit: stop and report.

Let `$REF` be the printed canonical `skill arg` (`D<NN> T<NN> §<N>`) and `$RECORD` be `docs/reviews/<NN-domain>/D<NN>-T<NN>-s<N>.md` (which already holds Pass 1, `## Plan review: astra`, from `process-todo-section`).

## Workflow (Open Section)

### 1. Self-review and research pass

1. Read `git --no-replace-objects show` on the implementation commit(s), check every `[x]` item in the section against real code and tests, and run `lsp_diagnostics` (`isotone-lsp`) on touched C++ and Python files.
2. Check for Isotone-specific failure modes: non-atomic file writes or missing read-back, missing undo/redo or failure-path tests, violations of `standards/cpp.md` or `docs/dev/native-libraries.md`, hardcoded UI literals violating `standards/design-contract.md`, unowned controls, or unfalsifiable checkpoints. Fix any defect on `main` and re-run gates before invoking the external reviewer.
3. On feature plans and UI surfaces, run an in-session competitor research check (fanning out read-only `research` subagents if helpful per `standards/delegation.md`), filing out-of-scope ideas via `add-todo` (`todo/backlog.md` by default unless passing the admission test).

### 2. Pass 2 -- the review `round` (one pass under `three-pass`)

Under `policy = "three-pass"`, each section runs **one** `--kind round` pass (`adversarial`, `consistency`, `integration`, `source-defect`, `quality`, `optimization`, plus `design` when `--surface` is passed):

```powershell
$BUILT_SHA = (git rev-parse HEAD).Trim()
$keep = Join-Path "build/reviews" ([guid]::NewGuid().ToString("N").Substring(0, 12))
New-Item -ItemType Directory -Force $keep | Out-Null
python scripts/review-prompt.py --kind round --candidate $BUILT_SHA --ref "$REF" --purpose "<one or two sentences>" --governing "<todo-or-spec-path>" --out build/round-prompt.md
$ROUND_OUT = python scripts/review-dispatch.py --writer agy --kind round --candidate $BUILT_SHA --prompt build/round-prompt.md --keep $keep --record $RECORD
$ROUND_NUM = ($ROUND_OUT | ConvertFrom-Json).round
```

Pass `--base $BASE_SHA` to `review-prompt.py` when the build spans multiple commits, `--surface` to `review-dispatch.py` on surface sections, and `--paths <files>` when conditional lenses apply. `$ROUND_NUM` is the dispatcher's recorded round number (`1` normally, or higher if an earlier attempt exited without returning a review).

- If the round ends `OVERALL: approve` (`"blocking": false`): the round verdict for `stamp` is `${ROUND_NUM}:${RECORD}:clean`. File any worthwhile `P3` follow-ups via `add-todo`.
- If the round ends `OVERALL: needs-attention` with `"blocking": false` (`HIGHEST: P3` only): file any worthwhile `P3` follow-ups via `add-todo` (or address trivial ones on `main`), note dispositions directly at the bottom of `$RECORD` (never edit inside `## Round N`, and do not add a `## ` heading that would break block notes), and do **not** run a second `--kind round`; the round verdict for `stamp` is `${ROUND_NUM}:${RECORD}:fixed` (`todo-graph.py` maps `OVERALL: approve` to `clean` and `OVERALL: needs-attention` to `fixed`).
- If the round ends `OVERALL: needs-attention` with `"blocking": true` (`P1` or `P2`): fix every valid blocking finding in a new commit on `main`, re-run the section's `Test checkpoint` and owed gates (`.agents/skills/process-todo-section/gates.md`), and record `- Implemented:` / refutation bullets directly at the bottom of `$RECORD` (never edit inside the dispatcher's `## Round N` block, and do not add a `## ` heading that would break block notes). Under `three-pass`, do **not** run a second `--kind round` (the schedule has 1 round entry; Pass 3 + `reconciliation` verify the final candidate); the round verdict for `stamp` is `${ROUND_NUM}:${RECORD}:fixed`.

### 3. Pass 3 -- `completion` and excellence review

On the post-round candidate `$POST_ROUND_SHA = (git rev-parse HEAD).Trim()` (after committing any round-1 fixes and gate re-runs, and before committing `$RECORD` on top of it so `$POST_ROUND_SHA` is the code candidate, or include code + `$RECORD` together in `$POST_ROUND_SHA`):

```powershell
$keep = Join-Path "build/reviews" ([guid]::NewGuid().ToString("N").Substring(0, 12))
New-Item -ItemType Directory -Force $keep | Out-Null
python scripts/review-prompt.py --kind completion --candidate $POST_ROUND_SHA --ref "$REF" --purpose "<user, verb, consumer>" --governing "<todo-or-spec-path>" --out build/completion-prompt.md
python scripts/review-dispatch.py --writer agy --kind completion --candidate $POST_ROUND_SHA --prompt build/completion-prompt.md --keep $keep --record $RECORD
```

Add `--fidelity "<Design specs>"` to `review-prompt.py` and `--surface` to `review-dispatch.py` on surface sections. Inspect the JSON summary and the ending line (`COMPLETION: complete` or `COMPLETION: gaps`):

| Completion reply | Action | `--completion` flag for `stamp` |
| --- | --- | --- |
| `COMPLETION: complete` | Ready to stamp `$POST_ROUND_SHA`. | `${RECORD}:complete` |
| `COMPLETION: gaps` with `"blocking": false` (`HIGHEST: P3` only) and out-of-scope gaps filed | File each out-of-scope gap via `add-todo`, append `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under the `## Completion review:` block in `$RECORD` (no `## ` heading!), and commit `$RECORD` (keeping `--sha $POST_ROUND_SHA`). | `${RECORD}:filed` |
| `COMPLETION: gaps` with `"blocking": false` (`HIGHEST: P3` only) and zero filed sections | Note dispositions under `## Completion review:` without `- Filed:` lines, commit `$RECORD` (keeping `--sha $POST_ROUND_SHA`). | `${RECORD}:completed` |
| `COMPLETION: gaps` with `"blocking": true` (`P1` or `P2`) | Repair every in-scope gap in code (never narrow the section's contract promises -- `stamp` verifies the section contract text did not change between failed completion and reconciliation!), file genuinely out-of-scope gaps via `add-todo`, append `- Implemented: ...` and `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under `## Completion review:` in `$RECORD` (no `## ` heading!), re-run gates saving output to `build/gates.txt`, commit on `main` (`$REPAIRED_SHA`), and run Step 4 (`reconciliation`). | `${RECORD}:<reconciled|filed|completed>` (per Step 4) |

### 4. Pass 4+ -- `reconciliation` loop (only when Completion returned blocking gaps)

Run `--kind reconciliation` on `$REPAIRED_SHA` (`--failed $POST_ROUND_SHA`, `--last <previous reviewed SHA>`, starting with `$LAST_SHA = $POST_ROUND_SHA`):

```powershell
$keep = Join-Path "build/reviews" ([guid]::NewGuid().ToString("N").Substring(0, 12))
New-Item -ItemType Directory -Force $keep | Out-Null
python scripts/review-prompt.py --kind reconciliation --candidate $REPAIRED_SHA --failed $POST_ROUND_SHA --last $LAST_SHA --ref "$REF" --findings $RECORD --gates build/gates.txt --governing "<todo-or-spec-path>" --out build/reconciliation-prompt.md
python scripts/review-dispatch.py --writer agy --kind reconciliation --candidate $REPAIRED_SHA --prompt build/reconciliation-prompt.md --keep $keep --record $RECORD
```

Inspect the reconciliation pass's JSON summary and ending line (inside `pass_cap = 33`):

- `RECONCILIATION: complete`: stop. Do **not** append `- Filed:` lines after the final `RECONCILIATION: complete` block (`verdict == "reconciled"` requires zero unclosed `- Filed:` notes on the final reconciliation block). Keep `$FINAL_SHA = $REPAIRED_SHA` and pass `--completion "${RECORD}:reconciled"` to `stamp`.
- `RECONCILIATION: gaps` with `"blocking": false` (`HIGHEST: P3` only): stop -- do **not** run another `--kind reconciliation` (`review-dispatch.py` and `todo-graph.py` refuse reconciling a pass whose worst finding is below `blocking`). Keep `$FINAL_SHA = $REPAIRED_SHA` (the candidate reviewed by that final reconciliation pass). If out-of-scope `P3` gaps are filed via `add-todo`, append `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under that final `## Reconciliation review` block in `$RECORD` (no `## ` heading!), commit the filed `todo/` changes and `$RECORD` on `main`, and pass `--completion "${RECORD}:filed"` with `--sha $FINAL_SHA`. If zero sections are filed, note dispositions under that `## Reconciliation review` block without `- Filed:` lines, commit `$RECORD` on `main`, and pass `--completion "${RECORD}:completed"` with `--sha $FINAL_SHA`.
- `RECONCILIATION: gaps` with `"blocking": true` (`P1` or `P2`): repair every in-scope blocking gap on `main` (never narrowing the section's contract promises), file genuinely out-of-scope gaps via `add-todo`, append `- Implemented: ...` and `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under that `## Reconciliation review` block in `$RECORD` (no `## ` heading!), re-run gates into `build/gates.txt`, set `$LAST_SHA = $REPAIRED_SHA`, commit the repair (`$REPAIRED_SHA = (git rev-parse HEAD).Trim()`), and run the next `--kind reconciliation` pass.

### 5. Surface golden approval and release backlog gate

- On UI surface sections (`standards/design-contract.md`), once `design-lint.py` reports `0 new, 0 stale` and the `design` lens passed, approve goldens into `docs/captures/golden/` when the visual harness is active.
- On release sections (`stilus-v*`, `gesso-v*`, `albumen-v*`, `isotone-v*`), confirm every `todo/backlog.md` entry in scope was promoted or carries an operator `reviewed:` deferral (`release-backlog-unreviewed`).

### 6. Stamp via `todo-graph.py stamp` and commit

Let `$FINAL_SHA` be the exact commit SHA reviewed by the final pass (`$POST_ROUND_SHA` when no reconciliation ran, or the final `$REPAIRED_SHA` reviewed by the last reconciliation pass -- whether it ended `RECONCILIATION: complete` or non-blocking `RECONCILIATION: gaps`). First commit `$RECORD` (and any out-of-scope `todo/` section filed from a non-blocking final pass) if modified (`docs: record review passes for <ref>`), keeping `--sha $FINAL_SHA`, then run:

```powershell
python scripts/todo-graph.py stamp "$REF" --sha $FINAL_SHA --plan $RECORD --review "${ROUND_NUM}:${RECORD}:<clean|fixed>" --completion "${RECORD}:<complete|reconciled|filed|completed>" --check "<Test checkpoint command -> exit 0 summary>" --check "pwsh scripts/check-all.ps1 -> exit 0"
python scripts/todo-findings.py --write
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --check
python scripts/todo-runs.py --check
```

Commit the updated TODO file, `docs/reviews/<slug>.json`, `todo/implementation-plan.md`, and `docs/reviews/findings.md` on `main` (`todo: stamp <ref>`). When remote pushes are active, capture `$BEFORE = (git ls-remote origin refs/heads/main).Split()[0]`, push `main` (`$STAMP_SHA = (git rev-parse HEAD).Trim()`), and verify commit-specific push CI (`python scripts/review_prompt.py ci-wait $STAMP_SHA --since $BEFORE` and `python scripts/review_prompt.py ci-wait $STAMP_SHA --since $BEFORE --workflow build --workflow-path .github/workflows/build.yml`) plus watched branch status (`python scripts/ci_status.py`).

## Outage rule (no fallback)

If `review-dispatch.py` exits `1` (CLI unreachable, auth failure, timeout, incomplete reply, or `OVERALL: blocked`), never substitute a writer-family review and never stamp without the pass. Retry the same pass in a fresh `--keep` folder with backoff (`15m`, `30m`, `1h`, `2h`, `4h`; use `schedule` in attended/campaign runs rather than shell sleeps). If all retries fail, add `> **Review pending:** <UTC> candidate <base>..<head>: <reason>` under the section heading, run `python scripts/todo-findings.py --write`, commit on `main`, leave the row `[ ]`, and let `process-phase` / `process-plan` continue with independent ready rows and retry at the next boundary.

## Audit stance (`resolve` exit `3`)

When auditing an already-shipped `[x]` section:

1. Inspect the stamped commit(s) and `docs/reviews/<slug>.json` (or legacy prose `Review:` record), and re-run the section's `**Test checkpoint:**` against today's repository.
2. If the section still holds, report the verified commit and live checkpoint output without modifying the stamp.
3. If the section regressed, reopen it cleanly with `python scripts/todo-graph.py unstamp "$REF" --reason "<what regressed and owning repair>"` (which revokes `docs/reviews/<slug>.json` or archives a legacy prose stamp's metadata to `docs/reviews/<slug>.revoked-*.json`, archives the prior cycle's findings and any `.attest.json` / `-review-outcomes.json` sidecars to `*.revoked-*.*` so the repair cycle starts a fresh three-pass findings file while keeping historical findings and panel runs checkable, writes `> **Unstamped:**`, flips the row back to `[ ]`, syncs `todo/implementation-plan.md`, and lists downstream suspect sections), run `python scripts/todo-findings.py --write`, `python scripts/todo-graph.py validate`, and `python scripts/todo-runs.py --check`, and commit the reopen on `main`.

## Guardrails

- Never edit inside a `## Plan review`, `## Round N`, `## Completion review`, or `## Reconciliation review` block written by `scripts/review-dispatch.py`.
- Never write `> **Verified:**` or `docs/reviews/<slug>.json` by hand; always use `python scripts/todo-graph.py stamp`.
- Never narrow a section's contract between a failed completion review and its reconciliation review.
- Never use em dashes or en dashes (`--` only).
