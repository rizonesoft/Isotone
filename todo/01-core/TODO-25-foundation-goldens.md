---
schema_version: 1
id: foundation-goldens
domain: 01-core
status: draft
title: "TODO-25 -- Foundation: the Goldens Environment and Its Repeatability Proof"
depends_on: []
frozen: false
track: F12
---

# TODO-25 -- Foundation: the Goldens Environment and Its Repeatability Proof

> **Goal:** a surface can be rendered offscreen on the WARP software device in a pinned reference environment, compared with its approved golden within the design contract's tolerance, and approved only through the review's path, and every golden renders identically, within that tolerance, twice and on two machines meeting the environment, so the golden render proof is something a stamp can stand on.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** `docs/captures/golden/` does not exist yet, and `todo/README.md`'s proof table marks the golden render proof `unusable for a stamp until D00 T07 §3 lands`; `D00 T07 §3` re-points that marker to §2 of this file, whose stamp activates it. The design reference renders of `scripts/render-design-reference.py` are the design's side of a comparison, not goldens.
<!-- claim: absent docs/captures/golden -->
<!-- claim: exists scripts/render-design-reference.py -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Testing and the gates", "Goldens" -- the pinned environment (the Windows build, the font files with Segoe UI Variable's hashes recorded and Cascadia Mono bundled under its license, fixed DirectWrite rendering parameters, a fixed DPI per golden, a fixed locale) and the repeatability proof
- [`standards/design-contract.md`](../../standards/design-contract.md) -- the tolerance, the folder layout under `docs/captures/golden/`, and the rule that only `review-todo-section` approves a golden
- -> XREF: D01 T16 §2 -- the WARP device this file renders on
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T01 §9 -- the per-control goldens of the UI library, re-planned by `D00 T07 §5`, which use this file's environment and compare and approve paths and own none of their own

## Outcome

- `isotone::ui::OffscreenRenderer` renders an element tree to a PNG on WARP after checking the pinned environment, refusing a machine whose environment differs.
- `scripts/goldens.py compare` compares renders with `docs/captures/golden/` within the contract's tolerance, and `scripts/goldens.py approve` writes goldens only on the review's path; both run in `check-all.ps1` and CI; the stamp of §2 turns the proof table's marker into the runner command.
- Every golden renders identically within tolerance twice and on two machines meeting the environment.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=not-applicable (the environment is pinned, not a setting); reporting=applicable @ D01 T25 §2; notifications=not-applicable (no long-running work a user starts); permissions=applicable @ D01 T25 §2; audit=applicable @ D01 T25 §2; exchange=not-applicable (no user files); reverse=applicable @ D01 T25 §2

**Adjacency rationale:** The compare report and its difference images are the report (§2); approving is refused outside the review's path, each approval is recorded, and an approved golden is replaced only by a new approval (§2).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Offscreen rendering on WARP in the pinned environment | D00 T07 §3, D01 T16 §2 |  [ ]   |
|   2   |   §2    | Compare and approve, in the gates | §1 |  [ ]   |
|   3   |   §3    | The repeatability proof | §2 |  [ ]   |

---

## 1. Offscreen Rendering on WARP in the Pinned Environment

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a render environment.
**Needs:** Windows host (build/test)

- [ ] Write the environment pin `native/tests/goldens/environment.json`: the Windows build, the SHA-256 of each Segoe UI Variable font file the design uses, the bundled Cascadia Mono files (under `native/tests/goldens/fonts/` with their SIL Open Font License), the DirectWrite rendering parameters (antialiasing mode, gamma, contrast), and the locale. Done when: the file parses and names each value.
- [ ] Add `isotone::ui::OffscreenRenderer` rendering an element tree at a given DPI into a WARP-backed Direct2D bitmap and writing a PNG, after checking every pin and refusing with the differing item named. Done when: `Offscreen.RefusesDifferentFontHash` and `Offscreen.RendersAtGivenDpi` pass.
- [ ] Commit: `"ui: offscreen WARP rendering in a pinned environment"`

**Test checkpoint:** Unit test: `Offscreen.RefusesDifferentFontHash` and `Offscreen.RendersAtGivenDpi` pass through CTest on the reference machine. Cheaper substitute that fails: rendering on the hardware device, whose output changes with the driver.

## 2. Compare and Approve, in the Gates

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the goldens tooling.
**Needs:** Windows host (build/test)

Approving is the one write here and its permissions are narrow: only the review's path may approve, each approval is recorded in the golden folder's `APPROVALS.md` as an audit history, and an approved golden is replaced, or deleted, only by a new approval.

- [ ] Add `scripts/goldens.py compare <area>` that renders each registered scenario through the offscreen renderer and compares it with `docs/captures/golden/<area>/<Comp>/` within the contract's tolerance, writing a report with a difference image per failure under `build/goldens/`, and `scripts/goldens.py approve` that writes goldens only when run by the review (a review record naming the section and its passed design lens is required), recording each approval in the golden folder's `APPROVALS.md`. Done when: `test_goldens.py` proves a matching render passes, a one-pixel difference beyond tolerance fails with its image, and an approval without a review record is refused.
- [ ] Run `goldens.py compare` in `scripts/check-all.ps1` and the `native` job of `.github/workflows/build.yml`. Done when: both list the stage.
- [ ] Activate the proof at this section's stamp: the golden render row's marker in `todo/README.md` names this section, and the stamp tool rewrites it to the runner command `python scripts/goldens.py compare` (`D00 T07 §3`). Done when: the marker names `D01 T25 §2` before the stamp and the runner command after it.
- [ ] Commit: `"tests: compare and approve goldens in the gates"`

**Test checkpoint:** Unit test and driven run with evidence: `python scripts/tests/test_goldens.py` passes (match, beyond-tolerance difference with its image, approval refused without a review record); `python scripts/goldens.py compare foundation` passes on a committed sample golden of the host's placeholder panel and fails with a difference image after one pixel of it is changed (both quoted, the change reverted). Cheaper substitute that fails: comparing by file hash, which fails on any encoder difference and passes nothing a reviewer can look at.

## 3. The Repeatability Proof

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- a proof about the environment.
**Needs:** Windows host (build/test)

- [ ] Render every registered golden twice on the reference machine in separate processes, and once on a second machine meeting the pinned environment (an ARM64 machine where the environment matches, recorded), and compare all renders pairwise within the contract's tolerance. Done when: the report lists every golden with zero failures and names both machines and their environments.
- [ ] Commit: `"tests: goldens render the same twice and on two machines"`

**Test checkpoint:** Driven run with evidence: the repeatability report (`build/goldens/repeatability.json`) lists every registered golden rendered twice on the reference machine and once on the second machine, every pair within tolerance, with both machines' Windows builds and font hashes (quoted). Cheaper substitute that fails: one render per golden, which cannot tell a deterministic environment from a lucky one.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0, with `goldens.py compare` among its stages
- [ ] `python scripts/tests/test_goldens.py` passes
- [ ] The proof table's golden render marker reads the runner command once §2 is stamped
- [ ] `python scripts/todo-graph.py validate` clean
