---
schema_version: 1
id: dev-automation
domain: 00-workspace
status: draft
title: "TODO-01 -- Dev-Automation Wiring"
depends_on: []
track: W1
---

# TODO-01 -- Dev-Automation Wiring

> **Goal:** The plan polices itself on every clone and every push: the commit hook refuses a broken staged tree, operator-only rows are marked so no runner takes them, the claims ratchet sits at what the tree measures, the review panel is proven end to end before the first stamp depends on it, and the first push to GitHub comes back green from both workflows.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The TODO tooling (`scripts/todo-graph.py` and its siblings), the skills under `.claude/skills/`, and the commit hook `tools/githooks/pre-commit` were carried from Resolute on 2026-09-26, and `tools/provision.ps1` (written the same day) sets `core.hooksPath`. None of it is committed yet: `git status` lists `tools/`, `scripts/`, `.claude/`, `.conclave/`, and `.github/` as untracked, so the hook has no index mode and no clone runs it. `REQUIRES_ALLOWED` in `scripts/todo-graph.py` holds only `display-session`, so the `todo/99-manual/` rows cannot yet carry the `operator` mark ScratchPad uses. `scripts/todo-claims.py` sets `COVERAGE_FLOOR = 1`, the value measured when the tree held one file. `python scripts/panel_slots.py validate` reports 7 slots and 7 registered models, and the `codex` CLI is on the PATH, but no review round has run in this repository.
<!-- claim: exists tools/githooks/pre-commit -->
<!-- claim: exists tools/provision.ps1 -->
<!-- claim: count "^COVERAGE_FLOOR = 1$" scripts/todo-claims.py = 1 -->
<!-- claim: count "^    \"display-session\",$" scripts/todo-graph.py = 1 -->
<!-- claim: count "^    \"operator\",$" scripts/todo-graph.py = 0 -->
<!-- claim: exists .conclave/panel.toml -->

## Inputs

- [`tools/githooks/pre-commit`](../../tools/githooks/pre-commit) -- the hook §1 wires in; it validates the staged tree in a temp checkout
- [`tools/provision.ps1`](../../tools/provision.ps1) -- sets `core.hooksPath` (§1) and provisions the SDK
- [`scripts/todo-graph.py`](../../scripts/todo-graph.py) -- `REQUIRES_ALLOWED` and `detect_context`, which §2 extends
- `R:\GitHub\ScratchPad\scripts\todo-graph.py` -- the source §2 ports the `operator` value and its self-test cases from (its D00 T01 §42)
- [`scripts/todo-claims.py`](../../scripts/todo-claims.py) -- `COVERAGE_FLOOR`, which §3 raises
- [`.conclave/panel.toml`](../../.conclave/panel.toml) and [`scripts/panel_slots.py`](../../scripts/panel_slots.py) -- the review panel §4 proves
- [`.github/workflows/build.yml`](../../.github/workflows/build.yml), [`.github/workflows/plan.yml`](../../.github/workflows/plan.yml) -- the workflows §5 reads back
- -> XREF: D99 T01 §1 -- the operator rows that carry the mark §2 adds; §2 edits that file

## Outcome

- `git ls-files -s tools/githooks/pre-commit` prints mode `100755`, and a provisioned clone refuses a commit whose staged tree fails `validate`.
- `validate` accepts `**Requires:** operator -- <reason>`, `query ready` lists those rows as runnable elsewhere, and every section in `todo/99-manual/` carries the mark.
- `COVERAGE_FLOOR` equals the number of `Current state` blocks carrying a claim on the day §3 ships.
- One review slot of each kind has run against a probe and its record is committed, so the first real stamp does not discover a broken panel.
- The first push of `main` has a green `build` run and a green `plan-gates` run, quoted by URL in `docs/dev/build.md`.

**Adjacency:** all=not-applicable (repository plumbing: gates, hooks, and CI with no user-facing records, settings, documents, or reversible user actions)

**Adjacency rationale:** Everything in this file is developer tooling. It has no user, no document, and no setting a person changes at runtime.

## Implementation Order

| Order | Section | Deliverable                                   | Depends On | Status |
| :---: | :-----: | --------------------------------------------- | ---------- | :----: |
|   1   |   §1    | Wire the TODO gate into every clone           | --         |  [ ]   |
|   2   |   §2    | The operator requirement for manual rows      | --         |  [ ]   |
|   3   |   §3    | Raise the claims coverage floor               | --         |  [ ]   |
|   4   |   §4    | Prove the review panel end to end             | --         |  [ ]   |
|   5   |   §5    | First push: CI green and read back            | §1         |  [ ]   |
|   6   |   §6    | The parity catalog validator                  | §1         |  [ ]   |

---

## 1. Wire the TODO Gate into Every Clone

The hook is the only gate that runs before a commit exists, so a tree that fails `validate` never reaches the remote. It must stay a POSIX shell script with LF endings, because Git for Windows runs hooks under its own `sh`.

- [ ] Record `tools/githooks/pre-commit` as executable with `git update-index --chmod=+x tools/githooks/pre-commit`. Done when: `git ls-files -s tools/githooks/pre-commit` prints mode `100755`. Cheaper substitute: relying on the working-tree file mode, which Windows does not keep.
- [ ] Confirm `.gitattributes` pins `tools/githooks/pre-commit` to `eol=lf`. Done when: `git check-attr eol -- tools/githooks/pre-commit` prints `eol: lf`.
- [ ] Confirm `tools/provision.ps1` sets `git config core.hooksPath tools/githooks`. Done when: after `pwsh tools/provision.ps1`, `git config core.hooksPath` prints `tools/githooks`.
- [ ] Commit: `"workspace: wire the TODO gate into every clone"`

**Test checkpoint:** `git ls-files -s tools/githooks/pre-commit` prints `100755`; `git check-attr eol -- tools/githooks/pre-commit` prints `eol: lf`; in a provisioned clone, staging a TODO file whose Implementation Order row depends on a section that does not exist (for example `T07 §3`) and running `git commit` exits non-zero with `pre-commit: todo-graph validate is red on the staged tree` after the validator's `does not resolve` FATAL, and the same commit succeeds once the edge is restored.

## 2. The Operator Requirement for Manual Rows

`todo/99-manual/` holds steps only the operator can perform (GitHub settings behind the owner's session, buying a certificate, taste calls). Without a mark, `query ready` offers them to a runner the moment their dependency ships, and the runner either stalls or fakes them. ScratchPad solved this with a declared-only `operator` value: no detector ever reports it, so only `--context operator` satisfies it. This section ports that value unchanged.

- [ ] Add `"operator"` to `REQUIRES_ALLOWED` in `scripts/todo-graph.py`, and extend the `detect_context` docstring to say `operator` is declared-only and never detected. Done when: `grep -n '"operator",' scripts/todo-graph.py` shows the tuple entry. Source: `R:\GitHub\ScratchPad\scripts\todo-graph.py` lines 240-275.
- [ ] Port ScratchPad's self-test cases for the value (the `**Requires:** operator` fixtures and the four `check(...)` cases near its lines 9179-9477: typo is FATAL, missing reason is FATAL, valid mark draws no FATAL, `query ready` names `requires operator (missing: operator)`). Done when: `python scripts/todo-graph.py self-test` prints a total four or more cases above the pre-change total with `0 failed`.
- [ ] Add an `operator` row to the Requires table in `todo/README.md` ("An operator at the keyboard with the owner's accounts; declared-only, never detected"). Done when: the table has two rows and `python scripts/todo-graph.py self-test` still reports `0 failed`.
- [ ] Add `**Requires:** operator -- <reason naming the account or purchase>` to every numbered section of `todo/99-manual/TODO-01-operator-setup.md`. Done when: `grep -c '^\*\*Requires:\*\* operator -- ' todo/99-manual/TODO-01-operator-setup.md` equals that file's section count.
- [ ] Add one sentence to the Phase 99 paragraph of `todo/implementation-plan.md` saying runners skip these rows because of the mark. Done when: the paragraph names `**Requires:** operator`.
- [ ] Commit: `"workspace: mark operator-only rows so no runner takes them"`

**Test checkpoint:** `python scripts/todo-graph.py self-test` reports `0 failed` with the new cases counted; `python scripts/todo-graph.py validate` exits 0; `python scripts/todo-graph.py query ready` lists every `D99 T01` row under runnable-elsewhere with `operator` missing, and `python scripts/todo-graph.py query ready --context operator` lists them as runnable. Cheaper substitute that fails: a prose "operator only" note, which `query ready` cannot read and which leaves the rows in the runnable list.

## 3. Raise the Claims Coverage Floor

`COVERAGE_FLOOR` in `scripts/todo-claims.py` is a ratchet: coverage may rise, never fall. It was set to 1 when the tree held one file; the tree authored on 2026-09-26 carries a claim on every `Current state` block, so the floor must rise to what is measured or the ratchet protects nothing.

- [ ] Run `python scripts/todo-claims.py --coverage` and read the covered-block count `N`. Done when: the number is quoted in the commit message body.
- [ ] Set `COVERAGE_FLOOR = N` in `scripts/todo-claims.py` and extend the comment above it with the date and the measurement, keeping its "measured, not wished" wording. Done when: `python scripts/todo-claims.py` prints `floor N` and exits 0.
- [ ] Commit: `"workspace: raise the claims coverage floor to the measured value"`

**Test checkpoint:** `python scripts/todo-claims.py` exits 0 and prints `coverage N/M, floor N`; deleting the claim lines from any one TODO's `Current state` block (in a scratch copy of the tree) makes it exit 1 naming coverage below the floor. Cheaper substitute that fails: leaving the floor at 1, which the scratch deletion does not trip.

## 4. Prove the Review Panel End to End

Every section ships through `review-todo-section`, which runs review slots from `.conclave/panel.toml` through `python scripts/panel_slots.py exec <slot>`. There are no fallback slots: a slot that cannot run parks the campaign. Discovering that on the first real stamp wastes a whole section's context, so this section runs each slot once against a probe first.

- [ ] Run `python scripts/panel_slots.py validate` and quote its summary line. Done when: it prints `panel slots ok` with the writer and slot counts.
- [ ] For each slot the review skill uses, run `python scripts/panel_slots.py exec <slot>` against a fixed probe prompt (a two-line diff that adds a typo to `docs/README.md` in a scratch worktree), capturing the verdict under `build/panel-probe/`. Done when: every slot returns a parseable verdict and names the typo, or the failing slot is named with its error.
- [ ] Record the probe in `docs/reviews/run-records.md` (date, slot names, CLI versions from `codex --version` and the writer harness, verdict per slot) and refresh the probe date in `.conclave/panel.toml` if the file carries one. Done when: `python scripts/todo-runs.py --check` exits 0 with the record present.
- [ ] Any slot that fails is filed through `add-todo` as a new section in this file with the error quoted, and this section's stamp names it. Done when: no slot failure is left only in the log.
- [ ] Commit: `"workspace: prove every review slot against a probe"`

**Test checkpoint:** `python scripts/panel_slots.py validate` exits 0; each `exec` run's verdict file under `build/panel-probe/` names the planted typo; `python scripts/todo-runs.py --check` exits 0. Cheaper substitute that fails: `validate` alone, which checks the table's shape and never starts a reviewer.

## 5. First Push: CI Green and Read Back

Two workflows guard `main`: `build` (restore, Release build, tests) and `plan-gates` (the TODO gates and the hook integrity). Neither has run on GitHub yet. A workflow nobody has seen green is a guess, so the first push is read back rather than assumed.

**Needs:** Windows host (build/test)

- [ ] Push `main` with the workspace spine committed. Done when: `git status -sb` shows `main` level with `origin/main`.
- [ ] Read back the `build` run with `gh run list --workflow build.yml --limit 1 --json conclusion,url`. Done when: `conclusion` is `success`; a failure is fixed in this section and re-pushed, never waited on.
- [ ] Read back the `plan-gates` run with `gh run list --workflow plan.yml --limit 1 --json conclusion,url`. Done when: `conclusion` is `success`.
- [ ] Add the two run URLs and the date to the CI table of `docs/dev/build.md` as the first recorded green runs. Done when: the table cites both URLs.
- [ ] Commit: `"workspace: record the first green CI runs"`

**Test checkpoint:** both `gh run list` queries return `success` for the pushed commit's SHA (`headSha` matches `git rev-parse HEAD`), and `docs/dev/build.md` cites the two URLs. Cheaper substitute that fails: a local `pwsh scripts/check-all.ps1`, which proves the machine and not the runner.

## 6. The Parity Catalog Validator

The Nodus parity catalog (`docs/parity/nodus-parity.md`) is plan data like `todo/`: 2,802 features merged from 1,294 Illustrator rows and 3,041 CorelDRAW rows, each with one status that points at a section, a backlog entry, an exclusion, or another app. Nothing checks it today, so a catalog row can silently lose its source id, point at a section that was renumbered or moved, or name a backlog entry that was promoted. The acceptance-bar aim "Nodus covers every CorelDRAW and Illustrator capability in the parity catalog" needs a gate before the first parity row runs, so the check joins `validate` beside the budget and backlog checks, and a `query parity` report gives each Nodus parity release (`D02 T17 §1` to `§10`) the per-phase counts it quotes. The status grammar and the update rules it enforces are in `docs/parity/README.md`. It owns no catalog rows of its own: it enforces them. Current state (verified 2026-09-26): no parity code exists in `scripts/` (`scripts/todo-parity.py` is absent), and `validate` wires its budget and backlog checks through `graph.budget_findings` in `scripts/todo-validate.py`, the pattern this section follows.
<!-- claim: absent scripts/todo-parity.py -->
<!-- claim: count "parity-id" scripts/todo-graph.py = 0 -->
<!-- claim: count "graph\.budget_findings\(todos\)" scripts/todo-validate.py = 1 -->
<!-- claim: exists docs/parity/sources/illustrator-30.8.md -->
<!-- claim: exists docs/parity/sources/coreldraw-2026.md -->

- -> XREF: D02 T17 §1 -- the Nodus releases that quote `query parity` for their phase
- -> XREF: D02 T17 §10 -- the 1.0.0 release that quotes the whole-catalog report as the acceptance-bar evidence

**Fidelity:** no surface of its own (stdlib tooling run by `validate`, the commit hook, and CI).

- [ ] Add `scripts/todo-parity.py` (stdlib only, like the other TODO tooling) with `parse_sources(repo)` reading every `| AI-#### |` row of `docs/parity/sources/illustrator-30.8.md` and every `| CD-### |` row of `docs/parity/sources/coreldraw-2026.md`. Done when: its self-check prints 1,294 Illustrator and 3,041 CorelDRAW ids on today's files.
- [ ] Add `parse_catalog(repo)` reading every `| NP-#### |` row of `docs/parity/nodus-parity.md` into (id, feature, Illustrator ids, CorelDRAW ids, category, status, notes). Done when: it returns 2,802 rows on today's file.
- [ ] Add `parse_status(text)` implementing the status grammar of `docs/parity/README.md`: `plan <DNN TNN §N>`, `shipped-scope <DNN TNN §N>`, `backlog B-NNN`, `excluded: <reason>`, and `other-app: <Imago|Lumen|none> <reason>`. Done when: each form parses and anything else returns a malformed marker.
- [ ] Add `parity_findings(graph, todos)` returning `(class, message)` pairs for `parity-id-missing` (a source id in no catalog row), `parity-id-duplicate` (a source id in two rows), and `parity-id-unknown` (a catalog id no source defines). Done when: each message names the id and the catalog line.
- [ ] Add `parity-np-duplicate` (an `NP-` id used twice) and `parity-status-malformed` (a status outside the grammar) to `parity_findings`. Done when: each message names the `NP-` id.
- [ ] Add `parity-ref-dead`: a `plan` or `shipped-scope` ref that `graph.resolve_ref` cannot find, or that names a section carrying a `> **Moved:**` marker. Done when: the message names the `NP-` id and the ref.
- [ ] Add `parity-backlog-dead`: a `backlog B-NNN` id with no live entry in `todo/backlog.md`, read through `graph.parse_backlog`. Done when: the message names the `NP-` id and the backlog id.
- [ ] Load `scripts/todo-parity.py` from `scripts/todo-graph.py` through `importlib.util.spec_from_file_location`, as `cmd_validate` loads `scripts/todo-validate.py`. Done when: `python scripts/todo-graph.py validate` runs with the module loaded and no import-time side effects (`sys.dont_write_bytecode` held as `adjacency_module` does).
- [ ] Call `parity_findings` from `scripts/todo-validate.py` beside `graph.budget_findings(todos)`, flagging each class, and skip the check when `docs/parity/nodus-parity.md` is absent so a bare-tree export still validates. Done when: `validate` on today's tree reports zero parity findings once the parity sections exist.
- [ ] Add the seven classes to `SEVERITY_MAP` in `scripts/todo-graph.py` as `fatal`. Done when: `python scripts/todo-graph.py self-test` reports `0 failed`.
- [ ] Add the seven rows to the per-class table in `todo/README.md` with their "Why" text, in the same commit as the map. Done when: the self-test's README-parity check passes; editing one side alone makes it fail.
- [ ] Add `query parity [--phase N] [--json]` to the `query` choices in `scripts/todo-graph.py`: per phase, the catalog rows planned to its sections and how many of those sections are stamped; per status kind, the totals. Done when: `python scripts/todo-graph.py query parity --phase 4` prints the Phase 4 rows and `--json` emits the same numbers as an object.
- [ ] Resolve a section's phase for `query parity` from the phase tables of `todo/implementation-plan.md`, the same source `query budget` reads. Done when: a section in no phase is reported under `unplaced` rather than dropped.
- [ ] Add self-test fixtures under the self-test's temporary tree: a tiny source pair, a tiny catalog, and a backlog with one entry. Done when: the fixtures are built in the self-test and leave nothing behind.
- [ ] Add self-test cases: one missing id, one duplicate source id, one unknown id, one duplicate `NP-` id, one malformed status, one dead ref, one ref to a Moved section, one dead backlog id, and one clean catalog with zero findings. Done when: each case asserts exactly its class and `self-test` reports `0 failed`.
- [ ] Add a self-test case for `query parity --phase N --json` over the fixture tree. Done when: the case asserts the planned and stamped counts.
- [ ] Confirm the check runs wherever `validate` runs: the commit hook (`tools/githooks/pre-commit`), the `plan-gates` workflow, and `scripts/check-all.ps1`, with no new CI job. Done when: a staged catalog with one id deleted is refused by the hook naming `parity-id-missing`.
- [ ] Add a short "Enforcement" note to `docs/parity/README.md` naming the seven classes and `query parity`. Done when: the README's Enforcement paragraph lists every class by name.
- [ ] Commit: `"workspace: validate the Nodus parity catalog against its sources and the plan"`

**Test checkpoint:** Unit test and static analysis: `python scripts/todo-graph.py self-test` reports `0 failed` with the new parity cases counted; `python scripts/todo-graph.py validate` exits 0 on the tree; deleting one `AI-` id from a scratch copy of the catalog makes `validate` exit 1 naming `parity-id-missing`, and pointing one row at `D02 T99 §1` makes it exit 1 naming `parity-ref-dead`; `python scripts/todo-graph.py query parity --phase 4 --json` prints the Phase 4 counts. Cheaper substitute that fails: a one-off script outside `validate` that CI never runs, which the hook refusal catches.

## Verification

- [ ] `python scripts/todo-graph.py self-test` reports `0 failed`
- [ ] `python scripts/todo-graph.py validate` clean
- [ ] `python scripts/todo-graph.py plan --check` clean
- [ ] `python scripts/todo-claims.py` exits 0 at the raised floor
- [ ] `pwsh scripts/check-all.ps1` exits 0
