---
schema_version: 1
id: foundation-docking
domain: 01-core
status: draft
title: "TODO-23 -- Foundation: a Docked Panel That Floats and Redocks"
depends_on: []
frozen: false
track: F10
---

# TODO-23 -- Foundation: a Docked Panel That Floats and Redocks

> **Goal:** the docking mechanism is proved before controls depend on it: a panel docked in a column can be dragged out to float in its own window and dragged back to dock, keeping its state, across monitors of different DPI, with the dock layout saved and restored as JSON.

> [!IMPORTANT]
> **Current state (verified 2026-11-13):** No docking code exists. The full docking system (tab groups, columns, the saved workspace, the layout maps' default panels) is the UI library's, in `todo/01-core/TODO-01-isotone-ui.md`, which a later section of `D00 T07` re-plans; this file proves the float-and-redock mechanism it will build on.
<!-- claim: absent native/ui/src/dock -->

## Inputs

- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md), "Docking" and "The order of work" step 2 -- our own docking system, and the foundation proof of a docked panel that floats and redocks
- [`docs/design/components/Panel/README.md`](../../docs/design/components/Panel/README.md) -- what a panel holds; the host's placeholder panels carry no product content
- -> XREF: D01 T15 §3 -- the window and frames a floating panel uses
- -> XREF: D00 T07 §3 -- authored this file; every entry section waits on its stamp
- -> XREF: D01 T22 §2 -- the runner that drags the panel with real pointer input
- -> XREF: D01 T01 §8 -- the UI library's dock theme and document tabs, re-planned by `D00 T07 §5`, built on this file's float-and-redock mechanism

## Outcome

- `isotone::ui::DockLayout` holds columns of panels, can float a panel into its own top-level window and redock it into a column, and saves and restores itself as JSON.
- In the host, a panel dragged out floats, dragged back redocks, keeps its state both ways, and does so across monitors of different DPI.

**Adjacency:** list=not-applicable (no records); document=not-applicable (no printed output); settings=applicable @ D01 T23 §1; reporting=not-applicable (no data to summarize); notifications=not-applicable (no long-running work); permissions=not-applicable (writes no user file); audit=not-applicable (no document edits); exchange=not-applicable (no user files); reverse=applicable @ D01 T23 §2

**Adjacency rationale:** The dock layout is saved and restored with readback (§1); every float is reversed by redocking (§2).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The dock layout: columns, a floating window, and its JSON | D00 T07 §3, D01 T15 §3 |  [ ]   |
|   2   |   §2    | Float and redock by dragging, proved with real pointer input | §1, D01 T22 §2 |  [ ]   |

---

## 1. The Dock Layout: Columns, a Floating Window, and Its JSON

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the docking mechanism with placeholder panels.
**Needs:** Windows host (build/test)

The dock layout is a setting: it is saved with atomic write and readback, and a restored layout is clamped onto a visible monitor.

- [ ] Add `isotone::ui::DockLayout` in `native/ui/src/dock/`: a tree of columns holding panels, `float(panel, rect)` creating a top-level tool window that hosts the panel's element subtree, and `dock(panel, column, index)` returning it, with each panel's state (scroll position, its control values) kept across both. Done when: `DockLayout.FloatAndDockKeepPanelState` passes.
- [ ] Save the layout as JSON (columns, order, widths in DIPs, floating windows with their monitor-relative rectangles) with atomic write and readback, and restore it, clamping a floating window onto a visible monitor. Done when: `DockLayout.SaveRestoreRoundTrip` and `DockLayout.ClampsOffscreenFloat` pass.
- [ ] Commit: `"ui: the dock layout with floating panels"`

**Test checkpoint:** Unit test: `DockLayout.FloatAndDockKeepPanelState`, `DockLayout.SaveRestoreRoundTrip`, and `DockLayout.ClampsOffscreenFloat` pass through CTest on every preset. Cheaper substitute that fails: reparenting the panel's window, which loses DPI handling and drag-and-drop targets.

## 2. Float and Redock by Dragging, Proved with Real Pointer Input

**Fidelity:** no surface of its own (non-feature infrastructure: a foundation mechanism with no competitor-facing feature of its own, so no `**Exceed:**` paragraph; the product sections that use it carry theirs) -- the drag interaction on placeholder panels.
**Needs:** Windows host (build/test)
**Requires:** display-session -- convicted by docs/specs/2026-10-22-native-stack-design.md, "Testing and the gates" (docking windows keep their own driven tests on real hardware)

Every float is reversed by redocking: the layout can restore the panel to the column and index it came from.

- [ ] Drag a panel's header out of its column to float it, showing the drop target while dragging, and drag the floating window's header onto a column to redock it, through `WM_POINTER` input. Done when: the host's report records each transition.
- [ ] Add `DockDrive.DragOutAndBack` that drags the panel out and back with mouse and with pen input through the driven-input runner, on one monitor and across two monitors of different DPI where the machine has them, and reads the layout and the panel's state back through UI Automation after each move. Done when: it passes and its report names the monitors used.
- [ ] Commit: `"ui: float and redock a panel by dragging"`

**Test checkpoint:** Driven run with evidence: `ctest --preset x64-debug -L drive -R DockDrive` passes in a display session, `DockDrive.DragOutAndBack` reporting the panel floated and redocked with its state kept, by mouse and by pen, and across monitors of different DPI where available (output quoted with the monitors used). Cheaper substitute that fails: calling `float` and `dock` from a test, which never exercises hit testing or the drag's drop targets.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0
- [ ] `pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; try { cmake --workflow --preset x64-release } finally { Pop-Location }'` exits 0 with the `DockLayout.*` cases reporting through CTest
- [ ] `DockDrive.DragOutAndBack` passes on the reference machine
- [ ] `python scripts/todo-graph.py validate` clean
