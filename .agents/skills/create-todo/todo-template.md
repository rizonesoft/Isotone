---
schema_version: 1
id: CHANGEME-unique-kebab-id
domain: CHANGEME-NN-domain
status: active
title: "TODO-NN -- CHANGEME Title"
depends_on: []
---

# TODO-NN -- CHANGEME Title

> **Goal:** CHANGEME: one paragraph stating what is true when this file is finished, in plain terms.

> [!IMPORTANT]
> **Current state (verified CHANGEME-YYYY-MM-DD):** CHANGEME: what exists right now before this TODO runs, naming real paths and gaps.
<!-- claim: exists CHANGEME/path/that/exists -->

## Inputs

- [CHANGEME spec or design doc](CHANGEME-path) -- what this TODO consumes from it
- -> XREF: CHANGEME D<NN> T<NN> §<N> -- related work and what flows each way (reciprocate in the target file)

## Outcome

- CHANGEME: observable end state, not an activity.
- CHANGEME: second observable end state with its readback.

**Adjacency:** CHANGEME: `all=not-applicable (reason)` or all nine keys (`list`, `find`, `create`, `edit`, `delete`, `undo`, `persist`, `export`, `settings`) exactly once separated by semicolons.

**Adjacency rationale:** CHANGEME: substantive prose explaining the adjacency decisions above.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
| 1 | §1 | CHANGEME single-responsibility deliverable | -- | [ ] |
| 2 | §2 | CHANGEME second deliverable | §1 | [ ] |

---

## 1. CHANGEME Single-Responsibility Section Title

CHANGEME: one paragraph of context explaining why this section exists, what capability it delivers, and what it must not break. Feature sections add `**Exceed:**` naming the measurable improvement over the competition, built in the checklist and proved by the checkpoint; non-feature sections state in context that they have no competitor-facing feature.

**Needs:** Windows host (build/test)

- [ ] CHANGEME micro-step 1 in `native/CHANGEME/path.cpp` (one concrete action). Done when: CHANGEME observable end state. Cheaper substitute: CHANGEME shortcut or stub that must fail.
- [ ] CHANGEME micro-step 2 in `native/CHANGEME/path.cpp` (refusal, cancellation, or error-recovery path). Done when: bad input or failure aborts cleanly without partial state. Cheaper substitute: silent swallow or unverified write.
- [ ] CHANGEME micro-step 3 in `native/tests/CHANGEME_test.cpp` (falsifiable GoogleTest covering happy and refusal paths). Done when: CTest passes and fails if production logic is reverted.
- [ ] Commit: `"CHANGEME: one-line commit message"`

**Test checkpoint:** Unit tests -- `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with `Suite.Case` passing.

## 2. CHANGEME Surface or Follow-Up Section Title

CHANGEME: one paragraph of context. UI surface sections include `**Fidelity:**`, `**Design:**`, `**Job:**`, `**Treatment:**`, and `**Chrome:**` per `todo/README.md` and `standards/design-contract.md` (write `new surface: docs/design/components/<Name>/README.md` and author the spec in item 1 when no spec exists yet):

**Fidelity:** CHANGEME surface -- docs/design/components/CHANGEME/ per standards/design-contract.md; goldens under docs/captures/golden/CHANGEME-area/.
**Design:** docs/design/components/CHANGEME/README.md, docs/design/shell-layout.md#regions -- states: all in spec -- themes: all four -- density: both
**Job:** CHANGEME user job in one sentence.
**Treatment:** CHANGEME visual/interaction treatment matching docs/design/.
**Chrome:** CHANGEME shared controls and tokens consumed.

- [ ] CHANGEME micro-step in `native/CHANGEME/path.cpp`. Done when: CHANGEME observable end state. Cheaper substitute: CHANGEME wrong thing that must fail.
- [ ] Commit: `"CHANGEME: one-line commit message"`

**Test checkpoint:** Unit tests -- CHANGEME falsifiable command and expected output.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0 with every native, Python, and TODO gate `PASS`
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with this file's GoogleTest cases passing through CTest
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'python scripts/native-artifact-gate.py --policy shipping --require-built'` exits 0
- [ ] CHANGEME: file-level round-trip, fuzz corpus, or golden render checks owed by this file
- [ ] `python scripts/todo-graph.py validate` and `python scripts/todo-graph.py plan --check` exit 0
