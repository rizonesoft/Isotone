# TODO workflow

Imported from the Conclave-SDK `todo` and `reviewer` kits and tailored to the Isotone Graphics Suite (`AGENTS.md`, `todo/README.md`).

`todo/` is the live execution plan; format spec: `todo/README.md`. Markdown is canonical, and `build/` holds derived, gitignored projections.

Core mechanics: the Implementation Order table in each TODO file is the dependency graph; a row flips to `[x]` only through `python scripts/todo-graph.py stamp`, backed by a verified JSON review receipt in `docs/reviews/` under the `three-pass` review schedule in `.conclave/reviewers.toml`; `todo/implementation-plan.md` is synchronized by `python scripts/todo-graph.py plan --sync`, never ticked by hand; cross-references (`§N`, `TNN §N`, `DNN TNN §N`) are bidirectional; every section carries concrete micro-steps with `Done when:` criteria, a real `**Test checkpoint:**` mapped to `todo/README.md`'s proof table, `**Fidelity:**` and `**Design:**` lines on UI surfaces (`standards/design-contract.md`), and an `**Exceed:**` paragraph on competitor-facing features, and must be implementable with zero conversation context.

Granularity and 100% plan completeness:
- **Small, single-responsibility sections:** Never bundle multiple subsystems, dialogs, or workflows into one coarse umbrella section. Split every TODO file into small, single-responsibility sections (`<= 30` items per section, `<= 55` sections per file) that each deliver one coherent, testable capability.
- **Short table descriptions (`<= 88` chars):** Keep section headings (`## N. <Title>`), `Deliverable` cells in `Implementation Order`, and `Scope` cells in index tables to a concise noun phrase of at most 88 characters so raw Markdown table rows stay under 140 characters and never wrap in raw `.md` editors. Put file paths, symbols, CLI flags, and enumerations in the section body and micro-steps, never in the heading or table cell.
- **Granular micro-step checklist items:** Every section carries 1 to 30 buildable micro-step items ending with `- [ ] Commit: "<message>"`. Each non-Commit item names one action, a concrete path, symbol, or command in backticks, an observable `Done when:` in the same bullet, a `Cheaper substitute:` on UI and write items, and a source citation when copying behavior from a specification or reference implementation.
- **100% complete development plan and best-in-class product:** Running `process-plan` to completion must produce a 100% complete, shippable native C++23 suite with zero unowned surfaces, controls, parity rows (`docs/parity/`), settings, refusal/error paths, undo/reverse paths, or persistence read-backs, and every feature must match and measurably exceed its competitors. Never cap operator-requested planning and never silently drop scope (`todo/backlog.md`).

For TODO work, use the skill in your agent's isolated skill directory (`.agents/skills/` for Google Antigravity, `.claude/skills/` for Claude Code) that owns the step: capture through `add-todo`, author a file through `create-todo`, plan a feature or app through `plan-new-feature`, build through `process-todo-section`, review and stamp through `review-todo-section`, close a file through `process-todo-file`, run a phase or the plan through `process-phase` or `process-plan`, harden the tree through `groom-plan`.

The three-pass section lifecycle is:
1. Resolve and validate the section (`python scripts/todo-graph.py resolve`, `python scripts/todo-claims.py`), then run the one-pass pre-build **plan review** (`python scripts/review-prompt.py --kind plan` -> `python scripts/review-dispatch.py --writer <agy|claude> --kind plan --candidate HEAD`) before `> **Started:**` or any implementation edit.
2. Record `> **Started:** <UTC>`, act on valid plan-review findings, implement every micro-step straight on `main` (using `isotone-lsp` `clangd` and `pyright` alongside the native build and static-analysis gates), verify the Test checkpoint, and commit the candidate.
3. Run the one-pass **implementation review round** (`--kind round`) and the one-pass **completion review** (`--kind completion`) through `scripts/review-prompt.py` and `scripts/review-dispatch.py`; if completion raises a blocking (`P1`/`P2`) gap, fix every in-scope gap and run `--kind reconciliation` until clean (`complete`, `reconciled`, or non-blocking `filed` / `completed`).
4. Stamp mechanically through `python scripts/todo-graph.py stamp '<DNN TNN §N>' --sha <40-char SHA> --plan '<findings>' --review '<round>:<findings>:<verdict>' --completion '<findings>:<verdict>' --check '<command> -> <result>'` (where `<round>` is the `"round"` number returned by `review-dispatch.py --kind round`), which writes `docs/reviews/<slug>.json`, updates the TODO file, validates the graph, and synchronizes `todo/implementation-plan.md`, then commit the stamp.

## Rules for TODO work

- **Tests prove claims:** a section's Test checkpoint must be able to fail, maps to a usable runner in `todo/README.md`, and is recorded in `--check` on `todo-graph.py stamp`.
- **Commits:** trunk-based `main` only (never create feature branches or secondary git worktrees), concise imperative messages, the section ref in the commit. Review fix-loop commits append on `main`; never amend a candidate under review, never bypass hooks (`--no-verify`), and never force-push.
- **Autonomy, self-improvement, and self-healing:** decide technical questions from source, specifications, measurements, and driven runs without blocking on unnecessary prompts; repair broken gates, hooks, pins, or build state at their owning layer; and capture measured repository improvements through `add-todo`.

## Validation

```bash
python scripts/todo-graph.py self-test      # the graph tool's own fixture suite
python scripts/todo-graph.py validate       # structural, receipt, parity, design, and proof integrity
python scripts/todo-graph.py plan --check   # todo/implementation-plan.md is synchronized
python scripts/todo-claims.py               # measured Current-state claims match the tree
python scripts/todo-graph.py query ready    # dependency-safe work right now
python scripts/todo-graph.py query blocked  # sections waiting, and on what
python scripts/todo-graph.py query stats    # tree health
python scripts/todo-graph.py query deferred # open and resolved deferrals
python scripts/todo-graph.py query rounds   # review rounds and passes spent across JSON receipts
python scripts/review_pin.py --check        # .conclave/reviewers.toml schema and schedule check
python scripts/ci_status.py                 # CI state of watched workflows on main
```

Report only commands actually run, and distinguish static evidence, test output, and review proof.
