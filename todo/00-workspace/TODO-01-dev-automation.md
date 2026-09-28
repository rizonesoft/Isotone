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
> **Current state (verified 2026-09-26):** The TODO tooling (`scripts/todo-graph.py` and its siblings), the skills under `.claude/skills/`, and the commit hook `tools/githooks/pre-commit` were carried from Resolute on 2026-09-26, and `tools/provision.ps1` (written the same day) sets `core.hooksPath`. None of it is committed yet: `git status` lists `tools/`, `scripts/`, `.claude/`, `.conclave/`, and `.github/` as untracked, so the hook has no index mode and no clone runs it. `REQUIRES_ALLOWED` in `scripts/todo-graph.py` holds only `display-session`, so the `todo/99-manual/` rows cannot yet carry the `operator` mark ScratchPad uses. `scripts/todo-claims.py` sets `COVERAGE_FLOOR = 1`, the value measured when the tree held one file. `python scripts/panel_slots.py validate` reports 7 slots and 7 registered models, and the `codex` CLI is on the PATH, but no review round has run in this repository. **Corrected 2026-09-28:** the spine was committed and pushed on 2026-09-26: the hook is tracked at mode 100755 with `eol: lf`, and this clone's `core.hooksPath` is `tools/githooks`, so §1's three items hold on today's tree and its fact-check ticks them with that evidence; §1 still owes the provisioned-clone refusal of its checkpoint.
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
- [`standards/design-contract.md`](../../standards/design-contract.md), [`docs/design/`](../../docs/design/README.md) -- the contract and the design system §9's gates enforce

## Outcome

- `git ls-files -s tools/githooks/pre-commit` prints mode `100755`, and a provisioned clone refuses a commit whose staged tree fails `validate`.
- `validate` accepts `**Requires:** operator -- <reason>`, `query ready` lists those rows as runnable elsewhere, and every section in `todo/99-manual/` carries the mark.
- `COVERAGE_FLOOR` equals the number of `Current state` blocks carrying a claim on the day §3 ships.
- One review slot of each kind has run against a probe and its record is committed, so the first real stamp does not discover a broken panel.
- The first push of `main` has a green `build` workflow run (job `build-windows`) and a green `plan-gates` run, quoted by URL in `docs/dev/build.md`.
- The design contract is enforced: every surface section names its `docs/design/` spec on a `**Design:**` line or is listed in the shrink-only `todo/.design-baseline`, `scripts/design-lint.py` refuses any new literal color, size, or font in the UI sources at commit time and in CI, and `scripts/render-design-reference.py` renders the design's own previews for review (§9).
- Docs cannot drift silently: `docs/facts.json` is the one source for names, roles, the description, and topics; `scripts/drift-check.py` refuses a retired name or a README fact that disagrees with it at commit time and in CI, Markdown claims are re-measured outside `todo/` too, CI reads the GitHub About bar against the facts, and review refuses a stamp while a doc still describes changed behavior the old way (§10).

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
|   7   |   §7    | The validator reads the Gesso parity catalog  | §6         |  [ ]   |
|   8   |   §8    | The validator reads the Albumen parity catalog  | §7         |  [ ]   |
|   9   |   §9    | The design contract gates                     | §1         |  [ ]   |
|  10   |   §10   | The drift gates                               | §1         |  [ ]   |

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

**Corrected 2026-09-28:** the workflows have run since 2026-09-26: the first green `build` run is https://github.com/rizonesoft/Isotone/actions/runs/36202856393 and the first green `plan-gates` run is https://github.com/rizonesoft/Isotone/actions/runs/36203128891 (the one before it failed); `plan.yml` also runs a `campaign-guard` job, and `pages.yml` deploys the design page. The first two items are verified against those runs rather than a new push, and the CI table item still records them.

**Needs:** Windows host (build/test)

- [ ] Push `main` with the workspace spine committed. Done when: `git status -sb` shows `main` level with `origin/main`.
- [ ] Read back the `build` run with `gh run list --workflow build.yml --limit 1 --json conclusion,url`. Done when: `conclusion` is `success`; a failure is fixed in this section and re-pushed, never waited on.
- [ ] Read back the `plan-gates` run with `gh run list --workflow plan.yml --limit 1 --json conclusion,url`. Done when: `conclusion` is `success`.
- [ ] Add the two run URLs and the date to the CI table of `docs/dev/build.md` as the first recorded green runs. Done when: the table cites both URLs.
- [ ] Commit: `"workspace: record the first green CI runs"`

**Test checkpoint:** both `gh run list` queries return `success` for the pushed commit's SHA (`headSha` matches `git rev-parse HEAD`), and `docs/dev/build.md` cites the two URLs. Cheaper substitute that fails: a local `pwsh scripts/check-all.ps1`, which proves the machine and not the runner.

## 6. The Parity Catalog Validator

The Stilus parity catalog (`docs/parity/stilus-parity.md`) is plan data like `todo/`: 2,802 features merged from 1,294 Illustrator rows and 3,041 CorelDRAW rows, each with one status that points at a section, a backlog entry, an exclusion, or another app. Nothing checks it today, so a catalog row can silently lose its source id, point at a section that was renumbered or moved, or name a backlog entry that was promoted. The acceptance-bar aim "Stilus covers every CorelDRAW and Illustrator capability in the parity catalog" needs a gate before the first parity row runs, so the check joins `validate` beside the budget and backlog checks, and a `query parity` report gives each Stilus parity release (`D02 T17 §1` to `§10`) the per-phase counts it quotes. The status grammar and the update rules it enforces are in `docs/parity/README.md`. It owns no catalog rows of its own: it enforces them. Current state (verified 2026-09-26): no parity code exists in `scripts/` (`scripts/todo-parity.py` is absent), and `validate` wires its budget and backlog checks through `graph.budget_findings` in `scripts/todo-validate.py`, the pattern this section follows.
<!-- claim: absent scripts/todo-parity.py -->
<!-- claim: count "parity-id" scripts/todo-graph.py = 0 -->
<!-- claim: count "graph\.budget_findings\(todos\)" scripts/todo-validate.py = 1 -->
<!-- claim: exists docs/parity/sources/illustrator-30.8.md -->
<!-- claim: exists docs/parity/sources/coreldraw-2026.md -->

- -> XREF: D02 T17 §1 -- the Stilus releases that quote `query parity` for their phase
- -> XREF: D02 T17 §10 -- the 1.0.0 release that quotes the whole-catalog report as the acceptance-bar evidence

**Fidelity:** no surface of its own (stdlib tooling run by `validate`, the commit hook, and CI).

- [ ] Add `scripts/todo-parity.py` (stdlib only, like the other TODO tooling) with `parse_sources(repo)` reading every `| AI-#### |` row of `docs/parity/sources/illustrator-30.8.md` and every `| CD-### |` row of `docs/parity/sources/coreldraw-2026.md`. Done when: its self-check prints 1,294 Illustrator and 3,041 CorelDRAW ids on today's files.
- [ ] Add `parse_catalog(repo)` reading every `| NP-#### |` row of `docs/parity/stilus-parity.md` into (id, feature, Illustrator ids, CorelDRAW ids, category, status, notes). Done when: it returns 2,802 rows on today's file.
- [ ] Add `parse_status(text)` implementing the status grammar of `docs/parity/README.md`: `plan <DNN TNN §N>`, `shipped-scope <DNN TNN §N>`, `backlog B-NNN`, `excluded: <reason>`, and `other-app: <Gesso|Albumen|none> <reason>`. Done when: each form parses and anything else returns a malformed marker.
- [ ] Add `parity_findings(graph, todos)` returning `(class, message)` pairs for `parity-id-missing` (a source id in no catalog row), `parity-id-duplicate` (a source id in two rows), and `parity-id-unknown` (a catalog id no source defines). Done when: each message names the id and the catalog line.
- [ ] Add `parity-np-duplicate` (an `NP-` id used twice) and `parity-status-malformed` (a status outside the grammar) to `parity_findings`. Done when: each message names the `NP-` id.
- [ ] Add `parity-ref-dead`: a `plan` or `shipped-scope` ref that `graph.resolve_ref` cannot find, or that names a section carrying a `> **Moved:**` marker. Done when: the message names the `NP-` id and the ref.
- [ ] Add `parity-backlog-dead`: a `backlog B-NNN` id with no live entry in `todo/backlog.md`, read through `graph.parse_backlog`. Done when: the message names the `NP-` id and the backlog id.
- [ ] Load `scripts/todo-parity.py` from `scripts/todo-graph.py` through `importlib.util.spec_from_file_location`, as `cmd_validate` loads `scripts/todo-validate.py`. Done when: `python scripts/todo-graph.py validate` runs with the module loaded and no import-time side effects (`sys.dont_write_bytecode` held as `adjacency_module` does).
- [ ] Call `parity_findings` from `scripts/todo-validate.py` beside `graph.budget_findings(todos)`, flagging each class, and skip the check when `docs/parity/stilus-parity.md` is absent so a bare-tree export still validates. Done when: `validate` on today's tree reports zero parity findings once the parity sections exist.
- [ ] Add the seven classes to `SEVERITY_MAP` in `scripts/todo-graph.py` as `fatal`. Done when: `python scripts/todo-graph.py self-test` reports `0 failed`.
- [ ] Add the seven rows to the per-class table in `todo/README.md` with their "Why" text, in the same commit as the map. Done when: the self-test's README-parity check passes; editing one side alone makes it fail.
- [ ] Add `query parity [--phase N] [--json]` to the `query` choices in `scripts/todo-graph.py`: per phase, the catalog rows planned to its sections and how many of those sections are stamped; per status kind, the totals. Done when: `python scripts/todo-graph.py query parity --phase 4` prints the Phase 4 rows and `--json` emits the same numbers as an object.
- [ ] Resolve a section's phase for `query parity` from the phase tables of `todo/implementation-plan.md`, the same source `query budget` reads. Done when: a section in no phase is reported under `unplaced` rather than dropped.
- [ ] Add self-test fixtures under the self-test's temporary tree: a tiny source pair, a tiny catalog, and a backlog with one entry. Done when: the fixtures are built in the self-test and leave nothing behind.
- [ ] Add self-test cases: one missing id, one duplicate source id, one unknown id, one duplicate `NP-` id, one malformed status, one dead ref, one ref to a Moved section, one dead backlog id, and one clean catalog with zero findings. Done when: each case asserts exactly its class and `self-test` reports `0 failed`.
- [ ] Add a self-test case for `query parity --phase N --json` over the fixture tree. Done when: the case asserts the planned and stamped counts.
- [ ] Confirm the check runs wherever `validate` runs: the commit hook (`tools/githooks/pre-commit`), the `plan-gates` workflow, and `scripts/check-all.ps1`, with no new CI job. Done when: a staged catalog with one id deleted is refused by the hook naming `parity-id-missing`.
- [ ] Add a short "Enforcement" note to `docs/parity/README.md` naming the seven classes and `query parity`. Done when: the README's Enforcement paragraph lists every class by name.
- [ ] Commit: `"workspace: validate the Stilus parity catalog against its sources and the plan"`

**Test checkpoint:** Unit test and static analysis: `python scripts/todo-graph.py self-test` reports `0 failed` with the new parity cases counted; `python scripts/todo-graph.py validate` exits 0 on the tree; deleting one `AI-` id from a scratch copy of the catalog makes `validate` exit 1 naming `parity-id-missing`, and pointing one row at `D02 T99 §1` makes it exit 1 naming `parity-ref-dead`; `python scripts/todo-graph.py query parity --phase 4 --json` prints the Phase 4 counts. Cheaper substitute that fails: a one-off script outside `validate` that CI never runs, which the hook refusal catches.

## 7. The Validator Reads the Gesso Parity Catalog

The Gesso parity catalog (`docs/parity/gesso-parity.md`) is plan data like `todo/` and like the Stilus catalog `§6` already polices: 2,385 features (`IP-0001` to `IP-2385`; the last 18, added 2026-09-27 for the Albumen catalog's routes, carry no source id and are `§8`'s to check) merged from 3,176 Photoshop rows (two id families in one file, `PS-A-0001` to `PS-A-1750` and `PS-B-0001` to `PS-B-1426`), 2,762 Affinity rows, and 4,891 GIMP rows, each with one status that points at a section, a backlog entry, an exclusion, or another app. `§6` reads only the Stilus files, so a Gesso row can silently lose its source id, point at a renumbered or moved section, or name a promoted backlog entry. The acceptance-bar aim "Gesso covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog" needs the same gate before the first Gesso parity row (Phase 16) runs, and extending `§6`'s module keeps one validator for both catalogs instead of a second script: `scripts/todo-parity.py` becomes catalog-driven, the six catalog-agnostic classes run once per catalog, two classes are added (`parity-ip-duplicate` and `parity-totals-drift`), and `query parity` gains a `--catalog` flag that each Gesso parity release (`D03 T21 §1` to `§12`) quotes. The status grammar it enforces is the one `docs/parity/README.md` states after the Gesso decision (`other-app:` naming Stilus, Gesso, Albumen, or none; `excluded:` naming cloud, platform, or removed). It owns no catalog rows of its own: it enforces them. Current state (verified 2026-09-26): the Gesso catalog and its three sources exist with the counts claimed below, `§6` is not built (`scripts/todo-parity.py` is absent), and nothing in `scripts/todo-graph.py` names an `IP-` id.
<!-- claim: exists docs/parity/gesso-parity.md -->
<!-- claim: count "^\| IP-\d{4} \|" docs/parity/gesso-parity.md = 2385 -->
<!-- claim: count "^\| PS-A-\d{4} \|" docs/parity/sources/photoshop-27.10.md = 1750 -->
<!-- claim: count "^\| PS-B-\d{4} \|" docs/parity/sources/photoshop-27.10.md = 1426 -->
<!-- claim: count "^\| AF-\d{4} \|" docs/parity/sources/affinity-3.3.md = 2762 -->
<!-- claim: count "^\| GP-\d{4} \|" docs/parity/sources/gimp-3.2.6.md = 4891 -->
<!-- claim: count "IP-" scripts/todo-graph.py = 0 -->

- -> XREF: D03 T21 §1 -- the Gesso releases that quote `query parity --catalog gesso --phase N` for their phase
- -> XREF: D03 T21 §12 -- the 1.0.0 release that quotes the whole Gesso catalog report as the acceptance-bar evidence

**Fidelity:** no surface of its own (stdlib tooling run by `validate`, the commit hook, and CI).

- [ ] Add `CatalogSpec` (name, catalog path, row-id regex, sources) and `SourceSpec` (file, id regex, catalog column name) dataclasses to `scripts/todo-parity.py`, stdlib only. Done when: `scripts/todo-graph.py` still loads the module with no import-time side effects and both types carry docstrings.
- [ ] Replace `§6`'s module-level Stilus constants with one `CATALOGS` table whose `stilus` entry is `docs/parity/stilus-parity.md`, `NP-####`, Illustrator `AI-####` (`docs/parity/sources/illustrator-30.8.md`, column `Illustrator`) and CorelDRAW `CD-###` (`docs/parity/sources/coreldraw-2026.md`, column `CorelDRAW`). Done when: `grep -n "illustrator-30.8" scripts/todo-parity.py` finds the path only inside the `stilus` spec and the Stilus self-test cases of `§6` pass unchanged. Cheaper substitute: a copy of `§6`'s module hard-wired to the Gesso files, a second implementation.
- [ ] Add the `gesso` entry to `CATALOGS`: `docs/parity/gesso-parity.md`, `IP-####`, Photoshop `PS-A-####` and `PS-B-####` (both from `docs/parity/sources/photoshop-27.10.md`, column `Photoshop`), Affinity `AF-####` (`docs/parity/sources/affinity-3.3.md`, column `Affinity`), and GIMP `GP-####` (`docs/parity/sources/gimp-3.2.6.md`, column `GIMP`). Done when: the spec lists four `SourceSpec` entries and two of them share one file.
- [ ] Change `parse_sources(repo)` to `parse_sources(repo, spec)`, reading every id family a spec names, including two families from one file. Done when: the module's self-check prints 1,750 `PS-A`, 1,426 `PS-B`, 2,762 `AF`, and 4,891 `GP` ids (10,829 in all) beside the unchanged 1,294 `AI` and 3,041 `CD` ids.
- [ ] Change `parse_catalog(repo)` to `parse_catalog(repo, spec)` finding its columns from each area table's header row (`| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |` for Gesso), not from fixed positions. Done when: it returns 2,385 `IP` rows and 2,802 `NP` rows on today's files, and a scratch copy with the `Affinity` and `GIMP` columns swapped in one area table parses to the same ids.
- [ ] Run the six catalog-agnostic classes of `§6` (`parity-id-missing`, `parity-id-duplicate`, `parity-id-unknown`, `parity-status-malformed`, `parity-ref-dead`, `parity-backlog-dead`) once per catalog in `parity_findings(graph, todos)`, prefixing every message with the catalog name. Done when: a finding reads `gesso: GP-0042 ...` or `stilus: ...` and no class name is duplicated per catalog.
- [ ] Add `parity-ip-duplicate` (an `IP-` id used twice), the Gesso counterpart of `parity-np-duplicate`, driven by the spec's row-id regex. Done when: the message names the `IP-` id and both catalog lines.
- [ ] Add `parity-totals-drift` for both catalogs: the header's Totals table (features and source rows per status kind and the grand total) or an Areas-list count (`- [Selection](#selection) (98)`) disagrees with the counted rows. Done when: the message names the table cell or area and both numbers, and today's two catalogs produce zero findings.
- [ ] Extend `parse_status(text)` to the grammar of `docs/parity/README.md` as it reads after the Gesso decision: `other-app:` accepts `Stilus`, `Gesso`, `Albumen`, or `none`, and `excluded:` accepts `cloud`, `platform`, and `removed`. Done when: the four `other-app: Stilus` rows and the `excluded: removed` rows of `docs/parity/gesso-parity.md` parse without a `parity-status-malformed` finding.
- [ ] Confirm `parity-ref-dead` treats `shipped-scope` refs into `D01 T03` and `D03 T05` to `D03 T07` like any other ref, and that refs to the relocated `D03 T07 §3`, `§11`, `§16`, and `§17` stay live because those sections are relocated, not Moved. Done when: `validate` on the integrated tree reports no `parity-ref-dead` for the 204 `shipped-scope` rows.
- [ ] Extend `parity-backlog-dead` to the ids the Gesso catalog names (B-045 and B-047 since 2026-09-27, when its former B-012 and B-024 rows moved onto the `D01 T09` plug-in host and its B-041 to B-044 and B-046 rows were planned in the post-release phases), read through `graph.parse_backlog`. Done when: the Gesso catalog's 92 `backlog` rows produce zero findings and a scratch row naming the deleted B-012 fails.
- [ ] Skip the Gesso pass when `docs/parity/gesso-parity.md` is absent, as `§6` skips Stilus, so a bare-tree export still validates. Done when: a scratch copy of the tree without the Gesso catalog validates with no parity finding.
- [ ] Extend `query parity` to `query parity [--catalog stilus|gesso|all] [--phase N] [--json]` in `scripts/todo-graph.py`, default `all`: per catalog separately, per phase the planned rows and how many of their sections are stamped, per status kind the totals, and a section in no phase reported under `unplaced`. Done when: `python scripts/todo-graph.py query parity --catalog gesso --phase 16` prints the Phase 16 rows and `--json` emits an object keyed by catalog with the same numbers.
- [ ] Add `parity-ip-duplicate` and `parity-totals-drift` to `SEVERITY_MAP` in `scripts/todo-graph.py` as `fatal`. Done when: `python scripts/todo-graph.py self-test` reports `0 failed`.
- [ ] Add the two rows to the per-class table in `todo/README.md` with their "Why" text, in the same commit as the map. Done when: the self-test's README-parity check passes; editing one side alone makes it fail.
- [ ] Add self-test fixtures under the self-test's temporary tree: a tiny Photoshop source with one `PS-A` and one `PS-B` row, tiny Affinity and GIMP sources, a three-row Gesso catalog with a Totals table and an Areas list, and a backlog carrying B-045. Done when: the fixtures are built in the self-test and leave nothing behind.
- [ ] Add self-test cases over the Gesso fixtures: one missing `PS-B` id, one duplicate `GP` id, one unknown `AF` id, one duplicate `IP-` id, one `other-app: Stilus` row (clean), one `excluded: removed` row (clean), one malformed status, one dead ref, one dead backlog id (B-099), one Totals mismatch, one Areas-count mismatch, and one clean catalog with zero findings. Done when: each case asserts exactly its class with the `gesso:` prefix and `self-test` reports `0 failed`.
- [ ] Add a self-test case for `query parity --catalog gesso --phase N --json` over the fixture tree, and one for `--catalog all` listing both catalogs. Done when: the cases assert the planned and stamped counts per catalog.
- [ ] Keep `§6`'s Stilus self-test cases running through the shared `CatalogSpec` path. Done when: the Stilus case count is unchanged and each still asserts its class, now with the `stilus:` prefix.
- [ ] Confirm the check runs wherever `validate` runs (the commit hook `tools/githooks/pre-commit`, the `plan-gates` workflow, and `scripts/check-all.ps1`) with no new CI job. Done when: a staged Gesso catalog with one `GP-` id deleted is refused by the hook naming `gesso:` and `parity-id-missing`.
- [ ] Update the Enforcement paragraph of `docs/parity/README.md` to say `D00 T01 §7` is built and to list `parity-ip-duplicate`, `parity-totals-drift`, and the `--catalog` flag. Done when: the paragraph names every parity class and both catalogs.
- [ ] Commit: `"workspace: validate the Gesso parity catalog against its sources and the plan"`

**Test checkpoint:** Unit test and static analysis: `python scripts/todo-graph.py self-test` reports `0 failed` with the Gesso cases counted; `python scripts/todo-graph.py validate` exits 0 on the integrated tree; deleting one `GP-` id from a scratch copy of `docs/parity/gesso-parity.md` makes `validate` exit 1 naming `gesso:` and `parity-id-missing`, and editing one Totals cell makes it exit 1 naming `parity-totals-drift`; `python scripts/todo-graph.py query parity --catalog gesso --phase 16 --json` prints the Phase 16 counts. Cheaper substitute that fails: a copy of `§6`'s script hard-wired to the Gesso file, which the self-test's single-module import and the Stilus cases (still passing through the shared `CatalogSpec` path) expose as a second implementation.

## 8. The Validator Reads the Albumen Parity Catalog

The Albumen parity catalog (`docs/parity/albumen-parity.md`) is plan data like `todo/` and like the Stilus and Gesso catalogs `§6` and `§7` already police: 1,622 features (`LP-0001` to `LP-1622`) merged from 1,857 Lightroom Classic rows, 5,182 ACDSee rows, and 1,880 IrfanView rows, each with one status that points at a section, a backlog entry, an exclusion, or another app. It is also the first catalog that routes into another catalog: 396 ACDSee Edit-mode and IrfanView Paint rows are `other-app: Gesso IP-####`, naming the Gesso row that plans the capability, and 18 Gesso rows (`IP-2368` to `IP-2385`) carry no Photoshop, Affinity, or GIMP id because they exist only for those routes, which `§7`'s `parity-id-missing` would otherwise misread. The acceptance-bar aim "Albumen covers every Lightroom Classic, ACDSee Photo Studio Ultimate, and IrfanView capability in its parity catalog" needs the same gate before the first Albumen parity row (Phase 30) runs, and extending `§7`'s `CATALOGS` table keeps one validator for three catalogs instead of a third script: the catalog-agnostic classes run once more for `albumen`, three classes are added (`parity-lp-duplicate`, `parity-ip-route-dead`, and `parity-orphan-row`), and `query parity --catalog albumen` gives each Albumen parity release (`D04 T15 §1` to `§10`) the per-phase report of counts it quotes. It owns no catalog rows of its own: it enforces them. Current state (verified 2026-09-27): the Albumen catalog and its three sources exist with the counts claimed below, the Gesso catalog holds 2,385 rows including the 18 source-less ones, `§6` is not built (`scripts/todo-parity.py` is absent), and nothing in `scripts/todo-graph.py` names an `LP-` id. -> SOURCE: parity-albumen-validator
<!-- claim: exists docs/parity/albumen-parity.md -->
<!-- claim: count "^\| LP-\d{4} \|" docs/parity/albumen-parity.md = 1622 -->
<!-- claim: count "^\| LR-\d{4} \|" docs/parity/sources/lightroom-classic-15.5.1.md = 1857 -->
<!-- claim: count "^\| AC-\d{4} \|" docs/parity/sources/acdsee-ultimate-2027.md = 5182 -->
<!-- claim: count "^\| IV-\d{4} \|" docs/parity/sources/irfanview-4.76.md = 1880 -->
<!-- claim: count "^\| IP-\d{4} \|" docs/parity/gesso-parity.md = 2385 -->
<!-- claim: count "LP-" scripts/todo-graph.py = 0 -->
<!-- claim: absent scripts/todo-parity.py -->

- -> XREF: D04 T15 §1 -- the Albumen releases that quote `query parity --catalog albumen --phase N` for their phase
- -> XREF: D04 T15 §10 -- the 1.0.0 release that quotes the whole Albumen catalog report and the zero `parity-ip-route-dead` count as the acceptance-bar evidence

**Fidelity:** no surface of its own (stdlib tooling run by `validate`, the commit hook, and CI).

- [ ] Add the `albumen` entry to `§7`'s `CATALOGS` table in `scripts/todo-parity.py`: `docs/parity/albumen-parity.md`, row id `LP-####`, and sources Lightroom `LR-####` (`docs/parity/sources/lightroom-classic-15.5.1.md`, column `Lightroom`), ACDSee `AC-####` (`docs/parity/sources/acdsee-ultimate-2027.md`, column `ACDSee`), and IrfanView `IV-####` (`docs/parity/sources/irfanview-4.76.md`, column `IrfanView`). Done when: `grep -n "irfanview-4.76" scripts/todo-parity.py` finds the path only inside the `albumen` spec. Cheaper substitute: a copy of `§7`'s module hard-wired to the Albumen files, a second implementation.
- [ ] Confirm `parse_catalog(repo, spec)` finds the Albumen columns from each area table's header row `| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |` with no Stilus or Gesso code path changing behavior. Done when: it returns 1,622 `LP` rows on today's file and the Stilus and Gesso row counts are unchanged.
- [ ] Extend the module's self-check to print the Albumen figures beside `§6`'s and `§7`'s. Done when: it prints 1,857 `LR`, 5,182 `AC`, and 1,880 `IV` ids (8,919 in all) and 1,622 `LP` rows on today's files.
- [ ] Run the six catalog-agnostic classes (`parity-id-missing`, `parity-id-duplicate`, `parity-id-unknown`, `parity-status-malformed`, `parity-ref-dead`, `parity-backlog-dead`) and `§7`'s `parity-totals-drift` once more for the `albumen` catalog, every message prefixed `albumen:`. Done when: a finding reads `albumen: AC-0042 ...` and today's Albumen catalog produces zero `parity-totals-drift` findings.
- [ ] Add `parity-lp-duplicate` (an `LP-` id used twice), the counterpart of `parity-np-duplicate` and `parity-ip-duplicate`, driven by the spec's row-id regex. Done when: the message names the `LP-` id and both catalog lines.
- [ ] Extend `parse_status(text)` so `other-app: Gesso` accepts a following `IP-####` id, and an Albumen row routed to Gesso with no `IP-` id is `parity-status-malformed`. Done when: every one of the 396 `other-app: Gesso` rows parses with its `IP-` id and a scratch row without one is reported.
- [ ] Add `parity-ip-route-dead`: an `other-app: Gesso IP-####` status must name an `IP-` row that exists in `docs/parity/gesso-parity.md` and whose own status is not `other-app: Albumen` (no route loops). Done when: the message names the `LP-` row, the `IP-` id, and the reason (missing or loop), and today's catalogs produce zero findings.
- [ ] Relax `parity-id-missing` for Gesso rows with no source id in any column: such a row is valid only when its Notes name at least one `LP-` row whose status routes to it (today `IP-2368` to `IP-2385`), and document the rule in the module docstring. Done when: the 18 rows produce no finding on today's files.
- [ ] Add `parity-orphan-row`: a source-less Gesso row whose Notes name no `LP-` row routed to it. Done when: the message names the `IP-` id and the `LP-` ids its Notes cite.
- [ ] Confirm the status grammar of `docs/parity/README.md` as it reads after the Albumen decision: `other-app:` accepts `Stilus`, `Gesso`, `Albumen`, or `none`, `excluded:` accepts `cloud`, `platform`, and `removed`, and `shipped-scope` refs into `D04 T01`, `D04 T02`, `D01 T02`, and `D01 T07` resolve like any other ref, with `D04 T02 §9` (relocated into Phase 39, not Moved) staying live. Done when: the 52 `shipped-scope` rows and the 24 `excluded` rows of the Albumen catalog produce no finding.
- [ ] Confirm `parity-backlog-dead` covers the ids the Albumen catalog names (B-047, B-048, B-049, B-051, and B-052 since the 2026-09-27 promotions of B-041 to B-044 and B-050), read through `graph.parse_backlog`, and note in the module docstring that the Albumen integration added B-048 to B-051 and deleted the promoted Albumen entries (B-028 to B-032, B-034 to B-036) and that B-012 was deleted when the plug-in host was planned. Done when: with those entries live, the Albumen catalog's `backlog` rows produce zero findings and a row naming B-028 fails.
- [ ] Skip the Albumen pass when `docs/parity/albumen-parity.md` is absent, as `§6` and `§7` skip theirs, so a bare-tree export still validates. Done when: a scratch copy of the tree without the Albumen catalog validates with no parity finding.
- [ ] Extend `query parity` to `--catalog stilus|gesso|albumen|all` in `scripts/todo-graph.py`: the Albumen parity phases 30 to 39 answer `--catalog albumen --phase N`, and the `other-app: Gesso` rows are reported as a separate "routed to Gesso" count per Gesso phase so the Gesso releases see the Albumen-born rows they owe. Done when: `python scripts/todo-graph.py query parity --catalog albumen --phase 30` prints the Phase 30 report and `--json` emits the routed counts.
- [ ] Add `parity-lp-duplicate`, `parity-ip-route-dead`, and `parity-orphan-row` to `SEVERITY_MAP` in `scripts/todo-graph.py` as `fatal`. Done when: `python scripts/todo-graph.py self-test` reports `0 failed`.
- [ ] Add the three rows to the per-class table in `todo/README.md` with their "Why" text, in the same commit as the map. Done when: the self-test's README-parity check passes; editing one side alone makes it fail.
- [ ] Add self-test fixtures under the self-test's temporary tree: tiny Lightroom, ACDSee, and IrfanView sources, a four-row Albumen catalog with a Totals table and an Areas list, a two-row Gesso catalog with one source-less row naming an `LP-` id, and a backlog carrying B-048. Done when: the fixtures are built in the self-test and leave nothing behind.
- [ ] Add self-test cases over the Albumen fixtures: one missing `AC` id, one duplicate `IV` id, one unknown `LR` id, one duplicate `LP-` id, one `other-app: Gesso` row naming a dead `IP-` id, one route loop, one source-less Gesso row whose `LP-` reference does not route to it, one `excluded: cloud` row (clean), one dead backlog id (B-099), one Totals mismatch, and one clean catalog with zero findings. Done when: each case asserts exactly its class with the `albumen:` prefix and `self-test` reports `0 failed`.
- [ ] Add a self-test case for `query parity --catalog albumen --phase N --json` asserting the planned, stamped, and routed counts. Done when: the case passes.
- [ ] Keep `§6`'s and `§7`'s Stilus and Gesso self-test cases running unchanged through the shared `CatalogSpec` path. Done when: their case counts are unchanged and each still asserts its class.
- [ ] Confirm the check runs wherever `validate` runs (the commit hook `tools/githooks/pre-commit`, the `plan-gates` workflow, and `scripts/check-all.ps1`) with no new CI job. Done when: a staged Albumen catalog with one `AC-` id deleted is refused by the hook naming `albumen:` and `parity-id-missing`.
- [ ] Update the Enforcement paragraph of `docs/parity/README.md` to say `D00 T01 §8` is built and to list the three new classes and the `albumen` value of `--catalog`. Done when: the paragraph names every parity class and all three catalogs.
- [ ] Commit: `"workspace: validate the Albumen parity catalog against its sources, the plan, and the Gesso routes"`

**Test checkpoint:** Unit test and static analysis: `python scripts/todo-graph.py self-test` reports `0 failed` with the Albumen cases counted; `python scripts/todo-graph.py validate` exits 0 on the integrated tree; deleting one `AC-` id from a scratch copy of `docs/parity/albumen-parity.md` makes `validate` exit 1 naming `albumen:` and `parity-id-missing`, and changing one routed row to `other-app: Gesso IP-9999` makes it exit 1 naming `parity-ip-route-dead`; `python scripts/todo-graph.py query parity --catalog albumen --phase 30 --json` prints the Phase 30 counts. Cheaper substitute that fails: a copy of `§7`'s module hard-wired to the Albumen file, which the self-test's single-module import and the unchanged Stilus and Gesso cases expose as a second implementation.

## 9. The Design Contract Gates: the Design Line, design-lint, and the Reference Renders

The operator asked on 2026-09-27 whether the design, graphics, and docs were wired into the TODO system so that every item implements the design 1:1, and asked for "a design contract, policies, rules, inforcement scripts, etc.", choosing that pixel perfect means "Exact tokens + ±1 DIP geometry + approved goldens", that legacy code is handled by "Record existing violations, fail new ones", and that goldens are signed off by the "Review panel only". The infrastructure was built in the same attended session, before this section was filed; this section records it as delivered work so it runs through `process-todo-section` (whose fact-check ticks each item that is already true, with its evidence) and `review-todo-section` like any other change, instead of landing unreviewed. It is operator-directed and a new section rather than items folded into §1 or §6, because it is its own subject with its own gates, and widening a planned section with delivered work would blur what that section's review covers. The Design lines themselves are added across the tree by a later backfill that shrinks `todo/.design-baseline`; the WPF visual regression harness is `D01 T01 §9`.

**Fidelity:** no surface of its own -- validator rules, a lint script, a render script, and documentation.

**Needs:** Windows host (build/test)

- [ ] `standards/design-contract.md` (binding) states the design-first rule, what fidelity means (exact tokens; geometry within 1 DIP at 100, 150, and 200 percent; every state, theme, Highlight, and density the spec lists; type styles), goldens under `docs/captures/golden/<area>/<Comp>/` approved only by `review-todo-section` and pixel-diffed in CI with a stated tolerance, `**Design deviation:**` lines, the enforcement table, and the definition of done for a UI section, and it is linked from `standards/ui.md`, `standards/README.md`, and `AGENTS.md`. Done when: `Select-String design-contract.md standards/ui.md, standards/README.md, AGENTS.md` finds each link and the file has no em dash.
- [ ] `todo/README.md` "Surface fidelity" makes the design the Fidelity source (the old-app captures of `D00 T03 §2` a before record only) and defines the `**Design:**` line grammar, `new surface:`, the baseline, and `**Design deviation:**`. Done when: the section carries the grammar block and the severity table carries the six design classes.
- [ ] `scripts/todo-graph.py` and `scripts/todo-validate.py` add the FATAL classes `design-missing`, `design-malformed`, `design-dead-ref` (paths under `docs/design/`, anchors checked against Markdown headings slugged GitHub-style and HTML ids), `design-baseline-stale`, `design-baseline-grown` (a ref HEAD does not list), and `design-deviation-open-at-release` (an open deviation beside a stamped release section of its app), plus `query design` and the shrink-only `design-baseline` subcommand, with self-test cases for every class and the ratchet. Done when: `python scripts/todo-graph.py self-test` prints `0 failed` with the `design:` cases reporting.
- [ ] `todo/.design-baseline` lists every surface section that had no Design line on 2026-09-27 (generated with `python scripts/todo-graph.py design-baseline --init`, which refuses once HEAD carries the file). Done when: `python scripts/todo-graph.py query design` prints the baseline count and `0 missing and unlisted`, and `validate` reports 0 fatal.
- [ ] `scripts/design-lint.py` (stdlib) scans the UI projects' XAML and C# for literal colors, named colors, color APIs, `StaticResource` colors, non-token color keys, unknown keys (warn), literal sizes, literal font families, WPF-UI and FluentIcons, emoji, and system backdrops, printing `file:line:rule:message`, with `docs/design/.lint-baseline.json` recording the violations of 2026-09-27 by file, rule, and normalized line text (shrink-only `--update-baseline`, `--allow-add --reason`, and a HEAD comparison that refuses unrecorded growth) and a `--self-test`. Done when: `python scripts/design-lint.py --self-test` prints `0 failed` and `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` prints `0 new, 0 stale`.
- [ ] The lint is wired into `tools/githooks/pre-commit` (the staged tree, after `validate`), `scripts/check-all.ps1` (self-test and baseline gates), `.github/workflows/build.yml` (both steps), and `.github/workflows/plan.yml` (the self-test). Done when: a staged XAML file with a new literal color makes the hook exit non-zero naming `design-lint`, and the same commit passes once the color is a token key (both quoted).
- [ ] `scripts/render-design-reference.py` renders every component preview of `docs/design/components/` per theme and density with the Blue Highlight at 1x through headless Edge over the DevTools protocol (a stdlib WebSocket client) into `build/design-reference/<Comp>/<theme>-<density>.png`, with `build/design-reference/report.html` pairing each with the WPF card render when one exists, and runs as an optional CI step whose output is uploaded. Done when: `python scripts/render-design-reference.py` prints `0 failure(s)` with one reference per component, theme, and density (quoted count).
- [ ] The skills carry the contract: `process-todo-section` (read the Design specs, tokens, and the contract before a surface; token keys only; run design-lint; produce WPF renders; never approve goldens), `review-todo-section` (the `design-fidelity` lens, golden approval after it passes, the stamp's `Design:` verification line, refusal on new lint violations or open deviations), `groom-plan` (a live Design line on every surface section; baseline shrink), `create-todo` and its template, `plan-new-feature` (Design line required; new surfaces add their spec first), `add-todo`, and `.claude/skills/process-todo-section/gates.md` (the design-lint and visual regression gates). Done when: `Select-String design-fidelity, design-lint` finds each skill and `validate` reports no skill citation problem.
- [ ] Commit: `"workspace: the design contract, the Design line and its baseline, design-lint, and the design reference renders"`

**Test checkpoint:** `python scripts/todo-graph.py self-test` prints `0 failed`; `python scripts/todo-graph.py validate` reports 0 fatal and 0 warnings; `python scripts/design-lint.py --self-test` prints `0 failed`; `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` exits 0 with `0 new, 0 stale`, and exits 1 naming the file after a probe `Background="#FF0000"` is added to a UI XAML file (quoted, then reverted); a probe surface section without a Design line in a scratch copy of the tree fails `validate` with `design-missing`; `python scripts/render-design-reference.py --components Button` renders eight PNGs. Cheaper substitute that fails: a prose rule in a standard with no gate, which the probes above (a literal color and a missing Design line, both refused) show is enforced.

## 10. The Drift Gates: Product Facts, Retired Names, Doc Claims, and the GitHub Mirror

The operator asked on 2026-09-27, after the rename to Isotone, "how are we preventing drift in docs, readme's, suporting files, comments, descriptions, etc. like the repo description", and then "add what you have to". Until this section ships, drift is caught only inside the plan: `todo-claims.py` re-measures claims in TODO files, `validate` checks the plan's structure, and `design-lint.py` checks UI literals. Nothing re-checks the README, `docs/`, `standards/`, the changelog, or code comments, and nothing reads the repository's settings on GitHub, which is how the About description still said "Photon Graphics Suite ... Nodus vector editor, Imago raster editor, Lumen digital darkroom. .NET 10" after the rename. It is operator-directed and a new section beside §9 because it is its own gate with its own scripts; it is in Phase 0 so the long run starts with it enforced. The social preview image can only be set in the web UI, so it stays with `D99 T01 §1`.

**Corrected 2026-09-28:** the About description, topics, and homepage were set by the operator on 2026-09-27, so the first `--check-github` compares against those values rather than the drifted description this section cites.

-> XREF: D99 T01 §1 -- the About bar row: its description and topics become the values `docs/facts.json` owns and `--sync-github` applies

**Fidelity:** no surface of its own -- a facts file, a check script, hook and CI wiring, and a review lens.

**Needs:** Windows host (build/test)

- [ ] Add `docs/facts.json`, the one source for product facts: the suite name, each app's name, slug, tag prefix, and one-line role, the repository description, the topics (ten on 2026-09-28), the homepage, and `retired` (the retired names Photon, Nodus, Imago, Lumen and the phrase ".NET 10", each with its replacement and the date). Versions are not copied into it: it names where each comes from (`global.json` for the SDK, `Directory.Packages.props` for packages, `installer/common.iss` for Inno Setup). Done when: the file parses and `docs/dev/README.md` links it with one sentence saying facts change here first.
- [ ] Add `scripts/drift-check.py` (stdlib) with `--self-test`: rule `retired-name` fails any retired word in a tracked text file, whole-word and case-aware as the 2026-09-27 rename matched, except under `docs/legacy/`, inside the verbatim operator quotes, `todo/budget.json` history, historic `git show <sha>:` paths, and backlog `merged:` markers, with an allowlist in `docs/facts.json` that grows only with a reason; rule `readme-facts` fails when the README's description line or badge versions differ from `docs/facts.json` and the pinned versions. Done when: `python scripts/drift-check.py --self-test` prints `0 failed` with a case per rule and per allowlist kind, and `python scripts/drift-check.py` prints `0 finding(s)` on the tree.
- [ ] Let claim lines (the `claim:` HTML comments) live in any Markdown file under `docs/`, `standards/`, and the root READMEs, not only in TODO files: `scripts/todo-claims.py` re-measures them with the same verbs and reports them by path. Done when: a claim added to `docs/dev/build.md` is measured and a false one fails (both quoted), and the self-test covers the new scope.
- [ ] Add `--check-github` and `--sync-github`: the check reads `gh repo view rizonesoft/Isotone --json description,repositoryTopics,homepageUrl` and fails on any difference from `docs/facts.json`; the sync applies the facts with `gh repo edit` under the operator's own login (the CI token cannot edit repository settings), printing each change before making it. Done when: the check names the difference against a changed probe value in a scratch facts file, and a real `--sync-github` run by the operator leaves the check clean (both quoted).
- [ ] Wire the gates: `tools/githooks/pre-commit` runs `drift-check.py` on the staged tree after `validate`; `scripts/check-all.ps1` runs the self-test and the check; `.github/workflows/plan.yml` runs both plus `--check-github` (read-only, with the workflow token). Done when: a staged README line naming "Imago" makes the hook exit non-zero naming `drift-check`, and the same commit passes once the line is fixed (both quoted).
- [ ] Add a `docs-drift` lens to `review-todo-section`, run in-session beside `source-defect`: the candidate range must update every doc, README, standard, XML doc comment, and code comment that describes behavior the range changed, and a stamp is refused while one still describes the old behavior. Name it in `.claude/skills/process-todo-section/gates.md` too. Done when: `Select-String docs-drift` finds both skills and the stamp template carries a `Docs:` verification line.
- [ ] Commit: `"workspace: the drift gates: product facts, retired names, doc claims, and the GitHub mirror"`

**Test checkpoint:** Unit test and driven run: `python scripts/drift-check.py --self-test` prints `0 failed`; `python scripts/drift-check.py` prints `0 finding(s)` on the tree and exits 1 naming the file and `retired-name` after a probe line "Imago raster editor" is added to `README.md` (quoted, then reverted); `python scripts/drift-check.py --check-github` exits 0 after the operator's sync and names the field after a probe difference; `python scripts/todo-claims.py` measures a claim in `docs/dev/build.md`. Cheaper substitute that fails: a one-off grep during the rename, which is what let the GitHub description drift.

## Verification

- [ ] `python scripts/todo-graph.py self-test` reports `0 failed`
- [ ] `python scripts/todo-graph.py validate` clean
- [ ] `python scripts/todo-graph.py plan --check` clean
- [ ] `python scripts/todo-claims.py` exits 0 at the raised floor
- [ ] `pwsh scripts/check-all.ps1` exits 0
