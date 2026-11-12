---
name: process-todo-section
description: Process exactly one TODO section end to end -- resolve it, validate and fact-check the plan against the repository, correct drifted claims, run the pre-build plan review, build it on main, run the gates, and hand to review-todo-section for round, completion, and stamp. Use whenever asked to process, implement, ship, continue, or finish a TODO section.
---

# Process TODO Section

One section, built cleanly on `main` (`docs/todo-workflow.md`). Never improvise around a drifted plan and never build a section you found to be wrong: validate the contract against the live repository, correct drifted claims in the TODO file visibly, pass the pre-build `plan` review, implement every item to 100% completion, run the section's gates, commit, and hand to `review-todo-section`.

## Step 0 -- resolve the argument before anything else

Never hand-translate a reference into a filename:

```powershell
python scripts/todo-graph.py resolve "$ARGUMENTS"
```

| Exit | Meaning | Action |
| :-: | --- | --- |
| `0` | Resolved, open, dependencies met | Proceed to Step 1 |
| `1` | Unknown TODO or section | Stop and report the unresolvable reference |
| `2` | No section reference in input | Stop and ask which section (in attended runs) |
| `3` | Already `[x]` | Do not rebuild; invoke `review-todo-section` in audit stance |
| `4` | Unmet dependencies | Stop at the dependency gate and list unmet sections |
| `5` | Section moved (`> **Moved:**`) | Stop and follow the target file named on the `Moved:` line |

Use the printed canonical `skill arg` (`D<NN> T<NN> §<N>`) everywhere: commit messages, `review-prompt.py --ref`, `todo-graph.py stamp`, and findings paths (`docs/reviews/<NN-domain>/D<NN>-T<NN>-s<N>.md`). Check any printed `needs` or `requires` capabilities against this machine (`pwsh scripts/dev-env.ps1 -Check -Arch x64` for native Windows toolchain work) and check `git status -sb` for unfamiliar uncommitted edits before proceeding. Always develop straight on `main`; never create feature branches or secondary worktrees.

## Delegation and tool discipline

- **Subagents read and never write (`standards/delegation.md`):** use `invoke_subagent` with `TypeName: "research"` on `inherit` only for parallel read-only source/spec/competitor checks during validation. Before and after any subagent call, verify tree cleanliness per `standards/delegation.md` and run `python scripts/panel_slots.py delegate-audit --session <Conversation ID>` when delegating.
- **Use `isotone-lsp` MCP tools:** inspect C/C++ (`clangd` + `clang-tidy`) and Python (`pyright`) symbols, references, and live diagnostics (`lsp_diagnostics`, `lsp_definition`, `lsp_references`, `lsp_hover`) instead of blind text greps.
- **Bound every command output:** redirect verbose build/test logs to ignored files under `build/` and inspect bounded summaries (`Select-Object -First` / `-Last`).

## Workflow

### 1. Read the whole contract and dependency stamps

Read the entire TODO file (`Goal`, `Current state`, `Inputs`, `Outcome`, `Adjacency`) and read the `Verified:` stamps and JSON receipts (`docs/reviews/<slug>.json`) of the sections in `Depends On` so you build on what actually shipped.

### 2. Validate and fact-check the section before building

Check all seven dimensions against the live repository: **Legitimacy**, **Currency**, **Consistency**, **Correctness**, **Sufficiency**, **Verifiability**, and **Accuracy**:

```powershell
python scripts/todo-graph.py validate
python scripts/todo-claims.py
python scripts/todo-graph.py query deferred
```

- Check every path, C++ target/header/symbol (`native/`, `standards/cpp.md`, `docs/dev/native-libraries.md`), token (`docs/design/tokens.json`), count, and `-> XREF:` target.
- Check **Deferrals** in both directions (`query deferred`): deferrals owned by this section are mandatory scope; drifted or already-shipped deferrals written by this section are updated or closed (`> **Resolved:**`).
- Check **Completeness** (`docs/completion-review-prompt.md`): every menu item, toolbar/rail button, keyboard shortcut, command palette entry, dialog state, setting + consumer, error/refusal path, atomic write + read-back, undo/redo step, persistence round trip, accessibility property, structured log event, and `docs/user/` guide update must be owned here or explicitly deferred to a resolving section.
- Check **`**Exceed:**`** (`AGENTS.md`): every competitor-facing feature section must carry an `**Exceed:**` paragraph naming at least one concrete, measurable improvement over the competition (speed/memory target on the `D00 T04 §2` benchmark harness, workflow step removed, missing capability, or higher output quality), built by a checklist item and proved by `Test checkpoint`. Only pure non-feature sections (workspace, tooling, CI, release mechanics) omit `**Exceed:**`, stating why in context.

### 3. Correct drifted claims and record `Started:`

Fix any Step 2 findings in the TODO file before writing code (`**Corrected YYYY-MM-DD:**` notes; never narrow the promised outcome to fit a shortcut). Ensure the section carries `> **Started:** <YYYY-MM-DDTHH:MM:SSZ>` (keep an existing `Started:` timestamp untouched when resuming). Commit any pre-build TODO corrections + `Started:` on `main` (`todo: prepare <ref> for build`) and capture `$PLAN_SHA = (git rev-parse HEAD).Trim()`.

### 4. Pre-build `plan` review (Pass 1 of `three-pass`)

Every section under `[schedule] policy = "three-pass"` runs one cross-family `plan` review on `$PLAN_SHA` (at or before the commit where building starts) into `$RECORD = "docs/reviews/<NN-domain>/D<NN>-T<NN>-s<N>.md"`:

```powershell
$keep = Join-Path "build/reviews" ([guid]::NewGuid().ToString("N").Substring(0, 12))
New-Item -ItemType Directory -Force $keep | Out-Null
python scripts/review-prompt.py --kind plan --candidate $PLAN_SHA --ref "<ref>" --governing "<todo-or-spec-path>" --out build/plan-prompt.md
python scripts/review-dispatch.py --writer agy --kind plan --candidate $PLAN_SHA --prompt build/plan-prompt.md --keep $keep --record $RECORD
```

Pass `--fidelity "<Design specs>"` to `review-prompt.py` and `--surface` to `review-dispatch.py` when the section builds a UI surface, and pass `--paths <planned files>` to `review-dispatch.py` when conditional schedule lenses apply. If the `plan` review reports in-scope gaps in the section plan, update the section's checklist/checkpoint in the TODO file (and file out-of-scope gaps via `add-todo`) before writing production code; note that `$RECORD` holds one returned `## Plan review` block (`plan_record` enforces `len(returned) == 1`), so keep that single plan review block intact and record your pre-build adjustments as `- Implemented:` / `- Filed:` bullets under it before committing the updated TODO section. If the reviewer CLI fails or times out (exit 1), follow the backoff and `> **Review pending:**` outage rule in `review-todo-section`.

### 5. Build the contract on `main`

Work the checklist top to bottom, ticking `[x]` in the TODO file as each item's `Done when:` holds:

- Follow `standards/cpp.md` and `docs/specs/2026-10-22-native-stack-design.md` for all native C++23 code under `native/`, keeping `docs/dev/native-libraries.md` and `scripts/native-deps-lint.py` in lockstep with vcpkg.
- On UI surface sections (`standards/design-contract.md`): validate the `**Design:**` line first (writing `new surface:` specs in `docs/design/` as item 1 when needed), use only `docs/design/tokens.json` tokens (`python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` must report `0 new`), implement every spec state/theme/density/scale, and never write to `docs/captures/golden/` (goldens are approved only in `review-todo-section`).
- Enforce atomic temp-file-then-replace writes with read-back on every user document, preset, catalog, or settings write, and test failure paths (locked/read-only target, truncated/corrupt input, cancellation).
- Run `lsp_diagnostics` on every modified C++ and Python file so zero compiler, `clang-tidy`, or `pyright` diagnostics remain.

### 6. Run the Test checkpoint and owed gates

Execute the section's `**Test checkpoint:**` and every gate owed on `.agents/skills/process-todo-section/gates.md` (`pwsh scripts/check-all.ps1`, `python scripts/todo-graph.py validate`, `python scripts/todo-claims.py`). Fix any stale `<!-- claim: ... -->` assertions and surrounding prose in the same commit.

### 7. Commit on `main` and hand to `review-todo-section`

Commit the implementation with quoted commit-time gate evidence:

```text
<area>: <what now works> (<ref>)

<quoted Test checkpoint and check-all summary>
<plan corrections, if any>
```

When remote pushes are active for the run, capture `$BEFORE = (git ls-remote origin refs/heads/main).Split()[0]`, push `main`, and verify commit-specific push CI (`python scripts/review_prompt.py ci-wait $SHIP_SHA --since $BEFORE` and `python scripts/review_prompt.py ci-wait $SHIP_SHA --since $BEFORE --workflow build --workflow-path .github/workflows/build.yml`) plus watched branch status (`python scripts/ci_status.py`) per `process-phase`. Then immediately invoke `review-todo-section` on `<ref>` to run Pass 2 (`round`), Pass 3 (`completion`), any `reconciliation`, and `python scripts/todo-graph.py stamp`.

## Guardrails

- Never flip the Implementation Order row `[x]` by hand; `python scripts/todo-graph.py stamp` in `review-todo-section` owns the stamp and row flip.
- Never widen scope silently; route out-of-scope discoveries through `add-todo`.
- Never use `--no-verify`, feature branches, secondary worktrees, or em/en dashes (`--` only).
