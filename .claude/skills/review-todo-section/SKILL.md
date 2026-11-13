---
name: review-todo-section
description: Quality-gate and stamp an implemented TODO section under the three-pass schedule -- self-review, round pass, completion and excellence pass, reconciliation when gaps are repaired, and deterministic JSON receipt stamping via todo-graph.py stamp. Also runs in audit stance on shipped sections. Use after process-todo-section or when asked whether a section is really done.
---

# Review TODO Section

The gate between "code exists" and `[x]` (`docs/todo-workflow.md`). Nothing flips an Implementation Order row by hand: `python scripts/todo-graph.py stamp` verifies the cross-family `three-pass` review chain in `docs/reviews/<NN-domain>/D<NN>-T<NN>-s<N>.md`, writes the canonical JSON receipt `docs/reviews/<slug>.json`, writes `> **Verified:**` + `> **Review:**`, and syncs `todo/implementation-plan.md`.

Every review pass runs through `scripts/review-dispatch.py` (`--writer claude` in Claude Code, `--writer agy` in Antigravity) against `.conclave/reviewers.toml` (`astra` on `gpt-6-astra` via `codex`, `[schedule] policy = "three-pass"`, `pass_cap = 33`, `blocking = ["P1", "P2"]`, no fallback). The writer's model family never reviews its own work.

## Step 0 -- resolve the argument

```bash
python scripts/todo-graph.py resolve "$ARGUMENTS"
```

- Exit `0`: open section ready for post-build review and stamping.
- Exit `3`: section is already `[x]` -- run in **audit stance** (below).
- Any other exit: stop and report.

Let `REF` be the printed canonical `skill arg` (`D<NN> T<NN> §<N>`) and `RECORD` be `docs/reviews/<NN-domain>/D<NN>-T<NN>-s<N>.md` (which already holds Pass 1, `## Plan review: astra`, from `process-todo-section`).

## Workflow (Open Section)

### 1. Self-review and research pass

1. Read `git --no-replace-objects show` on the implementation commit(s) and check every `[x]` item in the section against real code and tests.
2. Check for Isotone-specific failure modes: non-atomic file writes or missing read-back, missing undo/redo or failure-path tests, violations of `standards/cpp.md` or `docs/dev/native-libraries.md`, hardcoded UI literals violating `standards/design-contract.md`, unowned controls, or unfalsifiable checkpoints. Fix any defect on `main` and re-run gates before invoking the external reviewer.
3. On feature plans and UI surfaces, run an in-session competitor research check (`standards/delegation.md`), filing out-of-scope ideas via `add-todo` (`todo/backlog.md` by default unless passing the admission test).

### 2. Pass 2 -- the review `round` (one pass under `three-pass`)

Under `policy = "three-pass"`, each section runs **one** `--kind round` pass (`adversarial`, `consistency`, `integration`, `source-defect`, `quality`, `optimization`, plus `design` when `--surface` is passed):

```bash
BUILT_SHA=$(git rev-parse HEAD)
KEEP=$(mktemp -d build/review-XXXXXXXX)
mkdir -p "$KEEP/out"
python scripts/review-prompt.py --kind round --candidate "$BUILT_SHA" --ref "$REF" --purpose "<one or two sentences>" --governing "<todo-or-spec-path>" --out "$KEEP/round-prompt.md"
ROUND_OUT=$(python scripts/review-dispatch.py --writer claude --kind round --candidate "$BUILT_SHA" --prompt "$KEEP/round-prompt.md" --keep "$KEEP/out" --record "$RECORD")
ROUND_NUM=$(python -c 'import json, sys; print(json.load(sys.stdin)["round"])' <<<"$ROUND_OUT")
```

Pass `--base "$BASE_SHA"` to `review-prompt.py` when the build spans multiple commits, `--surface` to `review-dispatch.py` on surface sections, and `--paths <files>` when conditional lenses apply. `$ROUND_NUM` is the dispatcher's recorded round number (`1` normally, or higher if an earlier attempt exited without returning a review).

- If the round ends `OVERALL: approve` (`"blocking": false`): the round verdict for `stamp` is `${ROUND_NUM}:${RECORD}:clean`. File any worthwhile `P3` follow-ups via `add-todo`.
- If the round ends `OVERALL: needs-attention` with `"blocking": false` (`HIGHEST: P3` only): file any worthwhile `P3` follow-ups via `add-todo` (or address trivial ones on `main`), note dispositions directly at the bottom of `$RECORD` (never edit inside `## Round N`, and do not add a `## ` heading that breaks block notes), and do **not** run a second `--kind round`; the round verdict for `stamp` is `${ROUND_NUM}:${RECORD}:fixed` (`todo-graph.py` maps `OVERALL: approve` to `clean` and `OVERALL: needs-attention` to `fixed`).
- If the round ends `OVERALL: needs-attention` with `"blocking": true` (`P1` or `P2`): fix every valid blocking finding in a new commit on `main`, re-run the section's `Test checkpoint` and owed gates (`.claude/skills/process-todo-section/gates.md`), and record `- Implemented:` / refutation bullets directly at the bottom of `$RECORD` (never edit inside `## Round N`, and do not add a `## ` heading that breaks block notes). Under `three-pass`, do **not** run a second `--kind round`; the round verdict for `stamp` is `${ROUND_NUM}:${RECORD}:fixed`.

### 3. Pass 3 -- `completion` and excellence review

On the post-round candidate `POST_ROUND_SHA=$(git rev-parse HEAD)`:

```bash
mkdir -p "$KEEP/comp"
python scripts/review-prompt.py --kind completion --candidate "$POST_ROUND_SHA" --ref "$REF" --purpose "<user, verb, consumer>" --governing "<todo-or-spec-path>" --out "$KEEP/completion-prompt.md"
python scripts/review-dispatch.py --writer claude --kind completion --candidate "$POST_ROUND_SHA" --prompt "$KEEP/completion-prompt.md" --keep "$KEEP/comp" --record "$RECORD"
```

Add `--fidelity "<Design specs>"` to `review-prompt.py` and `--surface` to `review-dispatch.py` on surface sections. Inspect the JSON summary and ending line (`COMPLETION: complete` or `COMPLETION: gaps`):

| Completion reply | Action | `--completion` flag for `stamp` |
| --- | --- | --- |
| `COMPLETION: complete` | Ready to stamp `$POST_ROUND_SHA`. | `${RECORD}:complete` |
| `COMPLETION: gaps` with `"blocking": false` (`HIGHEST: P3` only) and out-of-scope gaps filed | File each out-of-scope gap via `add-todo`, append `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under `## Completion review:` in `$RECORD` (no `## ` heading!), and commit `$RECORD` (keeping `--sha $POST_ROUND_SHA`). | `${RECORD}:filed` |
| `COMPLETION: gaps` with `"blocking": false` (`HIGHEST: P3` only) and zero filed sections | Note dispositions under `## Completion review:` without `- Filed:` lines, commit `$RECORD` (keeping `--sha $POST_ROUND_SHA`). | `${RECORD}:completed` |
| `COMPLETION: gaps` with `"blocking": true` (`P1` or `P2`) | Repair every in-scope gap in code (never narrow the section's contract promises!), file genuinely out-of-scope gaps via `add-todo`, append `- Implemented: ...` and `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under `## Completion review:` in `$RECORD` (no `## ` heading!), re-run gates into `$KEEP/gates.txt`, commit on `main` (`REPAIRED_SHA`), and run Step 4 (`reconciliation`). | `${RECORD}:<reconciled|filed|completed>` (per Step 4) |

### 4. Pass 4+ -- `reconciliation` loop (only when Completion returned blocking gaps)

Run `--kind reconciliation` on `$REPAIRED_SHA` (`--failed "$POST_ROUND_SHA"`, `--last "$LAST_SHA"`, starting with `LAST_SHA="$POST_ROUND_SHA"`):

```bash
mkdir -p "$KEEP/rec-1"
python scripts/review-prompt.py --kind reconciliation --candidate "$REPAIRED_SHA" --failed "$POST_ROUND_SHA" --last "$LAST_SHA" --ref "$REF" --findings "$RECORD" --gates "$KEEP/gates.txt" --governing "<todo-or-spec-path>" --out "$KEEP/reconciliation-prompt.md"
python scripts/review-dispatch.py --writer claude --kind reconciliation --candidate "$REPAIRED_SHA" --prompt "$KEEP/reconciliation-prompt.md" --keep "$KEEP/rec-1" --record "$RECORD"
```

Inspect the reconciliation pass's JSON summary and ending line (inside `pass_cap = 33`):

- `RECONCILIATION: complete`: stop. Do **not** append `- Filed:` lines after the final `RECONCILIATION: complete` block. Keep `FINAL_SHA="$REPAIRED_SHA"` and pass `--completion "${RECORD}:reconciled"` to `stamp`.
- `RECONCILIATION: gaps` with `"blocking": false` (`HIGHEST: P3` only): stop -- do **not** run another `--kind reconciliation` (`review-dispatch.py` and `todo-graph.py` refuse reconciling a pass whose worst finding is below `blocking`). Keep `FINAL_SHA="$REPAIRED_SHA"` (the candidate reviewed by that final reconciliation pass). If out-of-scope `P3` gaps are filed via `add-todo`, append `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under that final `## Reconciliation review` block in `$RECORD` (no `## ` heading!), commit the filed `todo/` changes and `$RECORD` on `main`, and pass `--completion "${RECORD}:filed"` with `--sha "$FINAL_SHA"`. If zero sections are filed, note dispositions under that `## Reconciliation review` block without `- Filed:` lines, commit `$RECORD` on `main`, and pass `--completion "${RECORD}:completed"` with `--sha "$FINAL_SHA"`.
- `RECONCILIATION: gaps` with `"blocking": true` (`P1` or `P2`): repair every in-scope blocking gap on `main` (never narrowing the section's contract promises), file genuinely out-of-scope gaps via `add-todo`, append `- Implemented: ...` and `- Filed: D<NN> T<NN> §<N> (<gap>)` directly under that `## Reconciliation review` block in `$RECORD` (no `## ` heading!), re-run gates into `$KEEP/gates.txt`, set `LAST_SHA="$REPAIRED_SHA"`, commit the repair (`REPAIRED_SHA=$(git rev-parse HEAD)`), and run the next `--kind reconciliation` pass.

### 5. Surface golden approval and release backlog gate

- On UI surface sections (`standards/design-contract.md`), once `design-lint.py` reports `0 new, 0 stale` and the `design` lens passed, approve goldens into `docs/captures/golden/` when the visual harness is active.
- The `design-fidelity` lens of `standards/design-contract.md` is the dispatcher's `design` lens, scheduled when `--surface` is passed: it reads the UI renders under `build/ui-renders/` beside the design reference (`python scripts/render-design-reference.py --components <Comp>`, then `python scripts/render-design-reference.py --verify build/design-reference --components <Comp>`: the re-check owes every component unless it is given the same selection as the run). Approve goldens only after it passes. Refuse the stamp while `design-lint.py` reports a new violation or the section leaves a `**Design deviation:**` open without its follow-up section, and give the stamp a `--check "Design: <specs> -> design-fidelity clean, goldens docs/captures/golden/<area>/<Comp>/"` line.
- The `docs-drift` lens (`.conclave/reviewers.toml`, `[schedule.lenses]`) runs in every round through the dispatcher: the reviewer names each README, document, standard, skill, and source comment that still describes behaviour the range changed. A `P1` or `P2` finding under it blocks the stamp like any other; fix the text in the same range. Give the stamp a `--check "Docs: <the documents the range updated, or 'none describe the changed behaviour'> -> docs-drift clean"` line.
- On release sections (`stilus-v*`, `gesso-v*`, `albumen-v*`, `isotone-v*`), confirm every `todo/backlog.md` entry in scope was promoted or carries an operator `reviewed:` deferral (`release-backlog-unreviewed`).

### 6. Stamp via `todo-graph.py stamp` and commit

Let `FINAL_SHA` be the exact commit SHA reviewed by the final pass (`$POST_ROUND_SHA` when no reconciliation ran, or the final `$REPAIRED_SHA` reviewed by the last reconciliation pass -- whether it ended `RECONCILIATION: complete` or non-blocking `RECONCILIATION: gaps`). First commit `$RECORD` (and any out-of-scope `todo/` section filed from a non-blocking final pass) if modified (`docs: record review passes for <ref>`), keeping `--sha "$FINAL_SHA"`, then run:

```bash
python scripts/todo-graph.py stamp "$REF" --sha "$FINAL_SHA" --plan "$RECORD" --review "${ROUND_NUM}:${RECORD}:<clean|fixed>" --completion "${RECORD}:<complete|reconciled|filed|completed>" --check "<Test checkpoint command -> exit 0 summary>" --check "Docs: <documents the range updated> -> docs-drift clean" --check ".github/workflows/build.yml on $FINAL_SHA -> success <run url>" --check ".github/workflows/plan.yml on $FINAL_SHA -> success <run url>"
python scripts/todo-findings.py --write
python scripts/todo-graph.py validate
python scripts/todo-graph.py plan --check
python scripts/todo-runs.py --check
```

Commit the updated TODO file, `docs/reviews/<slug>.json`, `todo/implementation-plan.md`, and `docs/reviews/findings.md` on `main` (`todo: stamp <ref>`). When remote pushes are active, capture `BEFORE=$(git ls-remote origin refs/heads/main | cut -f1)`, push `main` (`STAMP_SHA=$(git rev-parse HEAD)`), and verify commit-specific push CI (`python scripts/review_prompt.py ci-wait "$STAMP_SHA" --since "$BEFORE"` and `python scripts/review_prompt.py ci-wait "$STAMP_SHA" --since "$BEFORE" --workflow build --workflow-path .github/workflows/build.yml`) plus watched branch status (`python scripts/ci_status.py`).

## Outage rule (no fallback)

If `review-dispatch.py` exits `1`, never substitute a writer-family review and never stamp without the pass. Retry the same pass in a fresh `--keep` folder with backoff (`15m`, `30m`, `1h`, `2h`, `4h`). If all retries fail, add `> **Review pending:** <UTC> candidate <base>..<head>: <reason>` under the section heading, run `python scripts/todo-findings.py --write`, commit on `main`, leave the row `[ ]`, and continue with independent ready rows.

## Audit stance (`resolve` exit `3`)

Inspect the stamped commit(s) and `docs/reviews/<slug>.json` (or legacy prose `Review:` record), and re-run the section's `**Test checkpoint:**`. On regression, reopen via `python scripts/todo-graph.py unstamp "$REF" --reason "<what regressed and owning repair>"` (which revokes `docs/reviews/<slug>.json` or archives a legacy prose stamp's metadata to `docs/reviews/<slug>.revoked-*.json` and archives the prior cycle's findings and any `.attest.json` / `-review-outcomes.json` sidecars to `*.revoked-*.*`), run `python scripts/todo-findings.py --write`, `python scripts/todo-graph.py validate`, and `python scripts/todo-runs.py --check`, and commit on `main`.

## Guardrails

- Never edit inside a `## Plan review`, `## Round N`, `## Completion review`, or `## Reconciliation review` block written by `scripts/review-dispatch.py`.
- Never write `> **Verified:**` or `docs/reviews/<slug>.json` by hand; always use `python scripts/todo-graph.py stamp`.
- Never narrow a section's contract between a failed completion review and its reconciliation review, and never use em/en dashes (`--` only).
