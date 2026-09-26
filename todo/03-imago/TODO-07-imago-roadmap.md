---
schema_version: 1
id: imago-roadmap
domain: 03-imago
status: draft
title: "TODO-07 -- Imago after 0.1.0: Deferral Owners and Accessibility"
depends_on: []
track: I7
---

# TODO-07 -- Imago after 0.1.0: Deferral Owners and Accessibility

> **Goal:** The Imago work after its first release that the plan is already committed to: the rest of the filter catalog that the 0.1.0 Filter menu names for its disabled items, RAW import through the decoder Lumen shares, and the workspaces, Preferences, accessibility, and localization work the acceptance bar requires. When this file closes, no Imago menu item is disabled as planned, and Imago works without a mouse or eyes. On 2026-09-26 the Imago parity plan relocated three of these sections into its phases without changing their addresses: the filter catalog (§3) runs first in Phase 21, where the filter surfaces and engine extensions extend it, workspaces and Preferences (§17) run first in Phase 27, and the accessibility and localization audit (§16) runs last in Phase 27 so it covers every parity surface; RAW import (§11) stays in Phase 31, after Lumen's decoder ships.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The legacy roadmap (`docs/legacy/imago-roadmap.md`, 853 lines, phases 0 to 11) was mined into 18 sections on 2026-09-26. The same day the plan was bounded (`todo/budget.json`): the 14 sections nothing outside this file depends on, defers to, or names in the acceptance bar moved to `todo/backlog.md` as B-014 to B-027, and their section numbers are retired, never reused. What stays: the filter catalog (§3), which `D03 T05 §3` names in the tooltips of its disabled filters; RAW import (§11), which `D04 T01` cross-references for the shared decoder; accessibility (§16), which the acceptance bar names; and workspaces and Preferences (§17), which §16 builds on and which enables the planned Preferences item. Several features have model types and no behavior, among them `AdjustmentLayer` and a Roslyn `ScriptEngine` in `Imago.Scripting` (62 lines), whose sections now wait in the backlog. Every section below names its legacy source with a `-> SOURCE:` line. **Corrected 2026-09-26:** the Imago parity plan promoted B-014 to B-023 and B-027 into its sections, merged B-025 (scripting) into the suite-wide B-041, and kept B-024 and B-026 in the backlog; `AdjustmentLayer` gains its behavior in `D03 T11 §1`, and the parity sections extend §3, §16, and §17 through their dependency edges.
<!-- claim: lines docs/legacy/imago-roadmap.md = 853 -->
<!-- claim: exists src/Imago/src/Imago.Core/Layers/AdjustmentLayer.cs -->
<!-- claim: lines src/Imago/src/Imago.Scripting/ScriptEngine.cs = 62 -->

## Inputs

- [`docs/legacy/imago-roadmap.md`](../../docs/legacy/imago-roadmap.md) -- the source of every section; read the named legacy phase before grooming
- [`standards/imago.md`](../../standards/imago.md) -- the rules every section builds to
- -> XREF: D04 T01 §4 -- the Lumen RAW decoder §11 moves to `Photon.Core` when Imago imports RAW
- -> XREF: D01 T07 §1 -- the suite develop engine cites §11: Imago's RAW open dialog develops through D01 T07 §1 instead of its own exposure and white balance code
- -> XREF: D03 T08 §1 -- Imago parity document and view cites §17: workspaces the panels there dock into
- -> XREF: D03 T14 §2 -- Imago parity filters cites §3: the legacy filter catalog whose disabled items D03 T14 §2 resolves
- -> XREF: D03 T15 §12 -- Imago parity photo (Camera Raw and merges) cites §11: RAW import: opens RAW into D03 T15 §12's studio and supplies camera RAW sources to RAW layers, merges, and astro frames when it ships in Phase 31
- -> XREF: D03 T20 §9 -- Imago parity workspace cites §17: workspaces and the Preferences dialog it extends; §16: the accessibility and localization audit that consumes D03 T20 §9's settings
- -> XREF: D03 T21 §12 -- the Imago parity releases cites §16: the accessibility and localization audit D03 T21 §12 depends on, so 1.0.0 ships no unaudited surface
- [`../backlog.md`](../backlog.md) -- the Imago feature ideas that left this file (B-014 to B-027); on 2026-09-26 the Imago parity plan promoted B-014 to B-023 and B-027 and merged B-025 into B-041, and the entries still there (B-024, B-026) are promoted only through `add-todo` with the admission test and budget room

## Outcome

- Every section below ships with its surface, commands with undo, settings, log lines, user-guide page, and tests, like the 0.1.0 sections before it.
- Every disabled "Planned" menu item from 0.1.0 that names a section of this file is working when this file closes.

**Adjacency:** list=applicable; document=not-applicable (printing arrives with the Imago parity phases in D03 T18 §6); settings=applicable @ D03 T07 §17; reporting=applicable; notifications=applicable; permissions=not-applicable (file refusals are owned by the format sections in D03 T04); audit=applicable; exchange=applicable; reverse=applicable @ D03 T07 §17

**Adjacency rationale:** The workspace and Preferences work is the settings and list surface; filter parity and RAW open results are reporting; long filters and RAW opens notify through the status strip; every edit is logged and undoable.

## Implementation Order

| Order | Section | Deliverable                                            | Depends On              | Status |
| :---: | :-----: | ------------------------------------------------------ | ----------------------- | :----: |
| 1 | §3 | The rest of the filter catalog                         | D03 T06 §3              |  [ ]   |
| 2 | §11 | RAW import through the shared decoder                  | D03 T06 §3, D04 T01 §4, D01 T07 §1, D03 T15 §12 |  [ ]   |
| 3 | §17 | Workspaces, panels, and preferences                    | D03 T06 §3              |  [ ]   |
| 4 | §16 | Accessibility and localization                         | §17, D03 T20 §8, D03 T20 §9 |  [ ]   |

---

## 3. The Rest of the Filter Catalog

The legacy plan lists motion and surface blur, smart sharpen, noise (add, reduce, median, dust and scratches), distort (twirl, pinch, spherize, wave, ripple, displace, polar coordinates), stylize (emboss, find edges, oil paint), and render (clouds, lens flare, lighting). The 0.1.0 menu carries the first five as disabled planned items. -> SOURCE: legacy-imago-5.2-5.7

- [ ] Implement each as an `IImageFilter` through the pipeline, each with a golden from libvips or GIMP (version recorded) and a fidelity test within a stated tolerance. Done when: every filter in the legacy list has a passing test or a recorded decision to drop it in `docs/dev/decisions.md`.
- [ ] Enable every planned filter menu item and remove its `PlannedCommands` entry. Done when: `MenuAuditTests` passes with no filter planned.
- [ ] GPU implementations for the three slowest filters with CPU parity tests. Done when: parity within 1/255 is quoted.
- [ ] Commit: `"imago: the full filter catalog"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` prints a result per filter; the GPU parity results are quoted. Cheaper substitute that fails: filters without goldens.

## 11. RAW Import through the Shared Decoder

Lumen decodes RAW (`D04 T01 §4`). The day Imago imports RAW, the decoder adapter moves from `Photon.Lumen.Core` to `Photon.Core` and both apps consume it; nothing is copied. -> SOURCE: legacy-imago-7.2-raw

- [ ] Move the RAW decoder adapter and its tests to `Photon.Core` (and its native dependency with it), with Lumen consuming it unchanged. Done when: Lumen's RAW tests pass against the moved type and `grep` finds one decoder class.
- [ ] Imago opens RAW files into the Develop studio (`D03 T15 §12`), developing through the suite develop engine (`D01 T07 §1`) with the decoder's output as a `RawDevelopSource`, then opens the result as a document in the workflow's bit depth (IP-1471). Done when: a committed small DNG fixture opens with its dimensions and a test asserts the render went through `DevelopPipeline`. **Corrected 2026-09-26:** said "a minimal develop dialog (exposure, white balance, then open as a 16-bit document)"; the Imago parity plan built the Develop studio and the shared engine first, so a second dialog would be a copy.
- [ ] Enable `File, Open RAW into Develop` and RAW layer sources, removing the `Planned: D03 T07 §11` entry `D03 T15 §12` registered in `PlannedCommands`, and register camera RAW with the focus-merge and astro frame loaders that refuse it by name until now (`D03 T15 §9`, `D03 T15 §10`). Done when: `MenuAuditTests` pass with no item planned to this section and a test loads a camera RAW fixture as a focus-merge source.
- [ ] Commit: `"core: share the RAW decoder; Imago opens RAW files"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the moved decoder tests, an Imago RAW open test through the Develop studio, and `MenuAuditTests` reporting; `grep -rn "class .*RawDecoder" src` prints one path under `src/Photon.Core/`. Cheaper substitute that fails: Imago referencing Lumen's assembly.

## 16. Accessibility and Localization

Every Imago surface keyboard- and screen-reader-operable and translatable. -> SOURCE: legacy-imago-6.5

- [ ] Audit every window with Accessibility Insights for Windows (version quoted) and fix every failure. Done when: the committed report shows none.
- [ ] Move strings to `.resx` with a pseudo-locale build. Done when: the pseudo-locale capture shows no untransformed string.
- [ ] High contrast and 200 percent captures of every window. Done when: committed.
- [ ] Commit: `"imago: accessibility fixes and localizable strings"`

**Requires:** display-session -- the audit needs an interactive desktop

**Test checkpoint:** the audit report shows zero failures. Cheaper substitute that fails: automation names on toolbar buttons only.

## 17. Workspaces, Panels, and Preferences

Saved panel layouts, a Preferences dialog over every Imago setting, and shortcut remapping. -> SOURCE: legacy-imago-6.2-6.6

**Fidelity:** Preferences dialog -- new build, no baseline; captured to docs/captures/imago/preferences/.
**Job:** a user can arrange panels, save workspaces, and change every setting and shortcut in one place. Consumer: every setting's consumer.
**Treatment:** Window, Workspace (save, switch, reset); Preferences categories bound to the settings store, applying on OK with Cancel reverting and Reset to Defaults restoring every value; shortcut remapping on the keymap. If Nodus's Preferences dialog frame (`D02 T06 §13`) fits, it moves to `Photon.UI` and both apps use it. Cheaper substitute that fails the checkpoint: settings without a surface.
**Chrome:** consume the settings store, the keymap, and AvalonDock.

**Requires:** display-session -- the dialog needs an interactive desktop

- [ ] Workspaces and Preferences with a test that every setting key has a control, Cancel reverting an edit, and Reset to Defaults restoring every value. Done when: the tests pass.
- [ ] Enable File, Preferences and remove its planned entry. Done when: `MenuAuditTests` passes.
- [ ] Commit: `"imago: workspaces and a Preferences dialog"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the preferences tests reporting. Cheaper substitute that fails: hand-edited JSON.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] No "Planned" menu item remains in Imago
- [ ] Every new format has a fidelity fixture
- [ ] `python scripts/todo-graph.py validate` clean
