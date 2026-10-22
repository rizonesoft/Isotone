---
schema_version: 1
id: isotone-layout-maps
domain: 01-core
status: blocked
title: "TODO-13 -- Layout Maps: Menus, Tools, Panels, and Buttons Where an Adobe User Expects Them"
depends_on: []
frozen: false
track: C13
---

# TODO-13 -- Layout Maps: Menus, Tools, Panels, and Buttons Where an Adobe User Expects Them

> **Goal:** A Photoshop user finds every Gesso command, tool, panel, and button where their hands expect it, an Illustrator user does the same in Stilus, and a Lightroom Classic user does the same in Albumen: the same menus in the same order with the same shortcuts, the same tools in the same groups, the same options bar per tool, and the same panels docked in the same places with their buttons in the same order. Each app follows a recorded layout map in `docs/design/layout-maps/`, captured from a driven run of the reference program where it is installed and from its documentation where it is not; a checker holds each map to its parity inventory, so every competitor feature has a recorded place in our app; shared tests fail the build when an app's real menus, tools, or panels drift from its map; and every section that builds one of those surfaces cites its map. Our product names, icons, and artwork stay our own (operator requests 2026-10-22: "can we have or are we already planning for things to be in the same place and layout as Adobe products. Same menu stracture/map. So anybody using photoshop can use our system", "Then add it to the todo system and plan", and "buttons, features and panels should also be in the expected places.").

> **Re-plan:** parked until the native re-plan reaches it (docs/plans/2026-10-23-native-replan.md).

> [!IMPORTANT]
> **Current state (verified 2026-10-22):** The design system already promises familiarity: principle 2 of `docs/design/README.md` is "Photoshop-familiar" (same window anatomy and shortcuts, "A Photoshop user should find every tool where their hands expect it"), and the options bar spec keeps Photoshop's order. Nothing records what each menu, tool group, options bar, or panel holds, or where: the component specs (`Menu`, `ToolRail`, `OptionsBar`, the dock theme) specify how those surfaces look, not their contents, and there is no `docs/design/layout-maps/`. The parity inventories place each competitor feature with a coarse `Where` column (a menu path such as `Filter > Blur`, `Toolbar`, `Options bar`, `Layers panel`, a dialog, or `Preferences`) but record no order or position: Photoshop 27.10 has 563 `command` rows, Illustrator 30.8 has 347, Lightroom Classic 15.5.1 has 715, and CorelDRAW 2026 has 781. This machine has Photoshop 27.11 and Illustrator 30.8.2 installed (`VersionInfo.ProductVersion`, 2026-10-22), so their layouts can be captured from driven runs; Lightroom Classic and CorelDRAW are not installed. The apps' main windows are made complete by `D02 T03 §5` (Stilus), `D03 T06 §2` (Gesso), and `D04 T01 §2` (Albumen's shell), and their menus, toolbars, and workspaces become user-editable in `D02 T16`, `D03 T20`, and `D04 T14`.
<!-- claim: count "Photoshop-familiar" docs/design/README.md = 1 -->
<!-- claim: count "layout-map" docs/design/components/Menu/README.md = 0 -->
<!-- claim: absent docs/design/layout-maps -->
<!-- claim: count "\| command \|" docs/parity/sources/photoshop-27.10.md = 563 -->
<!-- claim: count "\| command \|" docs/parity/sources/illustrator-30.8.md = 347 -->
<!-- claim: count "\| command \|" docs/parity/sources/lightroom-classic-15.5.1.md = 715 -->
<!-- claim: count "\| command \|" docs/parity/sources/coreldraw-2026.md = 781 -->

## Inputs

- [The design system's principles](../../docs/design/README.md) -- principle 2 ("Photoshop-familiar"), which §1 extends to each app's own reference program
- [The Menu](../../docs/design/components/Menu/README.md), [ToolRail](../../docs/design/components/ToolRail/README.md), and [OptionsBar](../../docs/design/components/OptionsBar/README.md) specs and [the shell layout](../../docs/design/shell-layout.md) -- how those surfaces look; the maps say what they hold and where
- [The design contract](../../standards/design-contract.md) -- the binding rule §1 adds a clause to
- [The parity inventories](../../docs/parity/sources/) -- every competitor feature with its `Where`, which §2 cross-checks each map against
- -> XREF: D02 T03 §6 -- Stilus's main window brought in line with its map, using §3's map and §6's test helpers
- -> XREF: D03 T06 §4 -- Gesso's main window brought in line with its map, using §4's map and §6's test helpers
- -> XREF: D04 T01 §12 -- Albumen's main window brought in line with its map, using §5's map and §6's test helpers
- -> XREF: D02 T16 §1 -- Stilus's workspaces, whose default workspace and Reset are §3's map
- -> XREF: D03 T20 §1 -- Gesso's workspaces, whose default workspace and Reset are §4's map
- -> XREF: D04 T14 §2 -- Albumen's toolbars, menus, and saved workspaces, whose defaults and Reset are §5's map

## Outcome

- `docs/design/layout-maps/` holds the format and one map per app, each naming its reference program and version, and recording every menu item, tool, options-bar control, panel, panel button, and panel menu item in the reference program's order and position, with what each is in our app (the same, renamed, not built yet with its owning section, ours only, or omitted with a reason).
- `python scripts/layout-map.py` passes in `scripts/check-all.ps1` and CI: every map is well formed, and every competitor feature its parity inventory places in a menu, the toolbar, the options bar, or a panel has a row in the map.
- Each app has tests that compare its real menus, tool rail, options bars, and default panel layout with its map, and fail on a missing, extra, misplaced, mislabelled, or wrongly bound item.
- Every TODO section that builds a menu, the tool rail, an options bar, or a panel cites its app's map on its Design line once the map exists, and `python scripts/todo-graph.py validate` refuses one that does not.

**Adjacency:** list=not-applicable (no records to browse); document=not-applicable (no printed output); settings=not-applicable (the user's own layout changes are the apps' workspace sections, D02 T16 §1, D03 T20 §1, and D04 T14 §2, which treat the map as the default); reporting=applicable @ D01 T13 §2; notifications=not-applicable (no events); permissions=not-applicable (nothing here writes a user file); audit=not-applicable (no history of its own; the maps change through reviewed commits); exchange=not-applicable (the competitor captures are design inputs, not a user import or export); reverse=not-applicable (no user edits)

**Adjacency rationale:** The maps are design data, like the component specs: they say what a surface holds and where, and the apps' workspace sections own what a user changes afterwards, so settings stays with them and each treats the map as the default its Reset returns to. The checker's coverage report (§2) and the test helpers' difference lists (§6) are the only reports, both for developers.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The layout-map format and the binding rule | -- |  [ ]   |
|   2   |   §2    | The layout-map checker | §1 |  [ ]   |
|   3   |   §7    | Every layout section cites its map | §1 |  [ ]   |
|   4   |   §3    | The Stilus map from a driven Illustrator run | §2 |  [ ]   |
|   5   |   §6    | The shared layout conformance test helpers | §2, D01 T01 §1 |  [ ]   |
|   6   |   §4    | The Gesso map from a driven Photoshop run | §3 |  [ ]   |
|   7   |   §5    | The Albumen map from Lightroom Classic's documentation | §2 |  [ ]   |

---

## 1. The Layout-Map Format and the Binding Rule

Design first: before any app's menus, tools, or panels are moved, `docs/design/` says what a layout map is and makes following it binding, so a section that builds one of those surfaces has a source to answer to rather than a memory of Photoshop. The decisions below are justified defaults, each with its cost of changing recorded in the README: changing one later is an edit to the README and a re-run of the checker, plus the per-app sections when it changes what the apps show.

- [ ] Write `docs/design/layout-maps/README.md`: one map file per app (`stilus.md`, `gesso.md`, `albumen.md`), each opening with its reference program, the exact version, and how each part was captured (driven, with the capture file, or from documentation, with a URL per part). Each map has five parts, every row carrying the reference program's place, its inventory id when one exists, our id, our label, our shortcut, and a Status: **Menus** (one table per top-level menu, in menu-bar order: item path, order, separators, shortcut); **Tools** (the tool rail top to bottom: group, the tools in each group with the default first, each tool's shortcut and the Shift cycle); **Options bar** (per tool, its controls left to right); **Panels** (the default workspace: each panel's dock side, column, tab group, order within the group, and whether it starts collapsed, plus each panel's buttons in order and its panel menu items); and **Shortcuts** (shortcuts that are not on a menu item). Done when: the README defines every part and its columns with one example row each.
- [ ] Define the Status vocabulary in the README: `same` (our feature, the reference program's label, place, and shortcut), `renamed` (our feature in the same place under our own label, with the reason, used only where the reference label is a product or trademark name such as "Camera Raw" or "Content-Aware Fill"), `planned` (not built yet: a menu item or tool is shown disabled in its place with a tooltip naming its owning section, as `D02 T03 §5` and `D03 T06 §2` require; a panel not built yet is listed disabled in the Window menu with its owner and keeps its place in the map), `own` (an Isotone-only feature, placed after the reference program's items in the group it fits best, behind a separator, never in a reference position), and `omitted` (a reference feature we will not offer, with the reason and the operator decision or backlog entry behind it). Done when: each status has its rule for each part.
- [ ] Define contexts for apps whose reference program changes its layout by mode: a map may declare named contexts (Lightroom Classic's Library, Develop, Map, Book, Slideshow, Print, and Web modules), each with its own menus, tools, and panels, and the parts common to all contexts listed once. Done when: the README shows a two-context example.
- [ ] Extend principle 2 of `docs/design/README.md` from "Photoshop-familiar" to each app's own reference program (Gesso to Photoshop, Stilus to Illustrator, Albumen to Lightroom Classic): its menus, tools, options bars, panels, and panel buttons follow its map in `docs/design/layout-maps/`. Add one line each to the `Menu`, `ToolRail`, and `OptionsBar` specs and to `docs/design/shell-layout.md` saying the contents, order, and default placement come from the app's map. Done when: each of those files links the maps folder.
- [ ] Add the clause to `standards/design-contract.md`: a surface that builds or changes a menu, the tool rail, an options bar, or a panel implements its app's map exactly (items, order, places, labels, shortcuts, statuses), proved by the app's layout map tests, and a difference needs a `**Design deviation:**` line like any other; a dialog or panel with a counterpart in the reference program also keeps that counterpart's control grouping and order and its button order, which the design-fidelity lens checks per surface. Done when: the contract names the maps, the tests, and the counterpart rule.
- [ ] Regenerate the design page as `docs/design/EDITING.md` describes. Done when: the page's check in `.github/workflows/pages.yml` passes on the commit.
- [ ] Commit: `"design: layout maps, the format and the binding rule"`

**Test checkpoint:** Driven run with evidence: `docs/design/layout-maps/README.md` exists with the five parts, the five statuses, and contexts; `grep -n "layout-maps" docs/design/README.md docs/design/components/Menu/README.md docs/design/components/ToolRail/README.md docs/design/components/OptionsBar/README.md docs/design/shell-layout.md standards/design-contract.md` prints a line in each; the design page check passes in CI on the commit (the `ci-wait` line quoted). Cheaper substitute that fails: a paragraph saying "follow Photoshop", which no checker or test can hold an app to.

## 2. The Layout-Map Checker

A map nobody checks drifts the way any recorded fact does. `scripts/layout-map.py` (stdlib Python 3, like `scripts/todo-parity.py`) holds each map to its own format and to the parity inventory of its reference program, so no competitor feature that lives in a menu, the toolbar, the options bar, or a panel can be left without a recorded place in our app.

- [ ] Add `scripts/layout-map.py`: read every map under `docs/design/layout-maps/`, and report `file:line: rule: message` for a malformed table, an unknown Status, a duplicate position within a menu, tool group, options bar, or dock group, a shortcut that is not `Ctrl`, `Shift`, `Alt` then a key in that order (the Menu spec's naming), two features bound to the same shortcut within one context, a `planned` row whose owning section does not resolve (`scripts/todo-graph.py resolve`), a `renamed` or `omitted` row with no reason, and one of our ids used for two different features. Done when: each rule has a failing and a passing fixture in `--self-test`.
- [ ] Cross-check each map against its reference program's inventory (`docs/parity/sources/<program>.md`): every `command` or `tool` row whose `Where` places it in a menu (a path whose first segment is one of the program's menus, or `... menu`), the toolbar, the options bar, a panel, or a panel menu appears in the map by its inventory id, with any status; rows placed in a dialog or in Preferences are reached through their menu item and are outside the map. Done when: deleting one mapped row from a fixture map reports that inventory id as missing, and an inventory id the map names that the inventory lacks is reported too.
- [ ] Print a per-map summary (rows by part and status, and inventory features placed of the total the cross-check covers) so the coverage is visible, and exit 1 on any finding. Done when: a clean run prints one summary line per map and exits 0.
- [ ] Wire `python scripts/layout-map.py` and `--self-test` into `scripts/check-all.ps1` (after design-lint, listed in its header comment), into `.github/workflows/plan.yml`, and into the Validation block of `AGENTS.md` with the `scripts/` row of its path table. Done when: `pwsh scripts/check-all.ps1` lists both as PASS and the workflow names the script.
- [ ] Commit: `"design: check every layout map against its reference inventory"`

**Test checkpoint:** Unit test and static analysis: `python scripts/layout-map.py --self-test` prints `0 failed` with a case per rule; with `README.md` alone (no maps yet) `python scripts/layout-map.py` exits 0 and says so; a scratch map missing one inventory toolbar tool fails with its id (quoted, then deleted); `pwsh scripts/check-all.ps1` lists both gates as PASS. Cheaper substitute that fails: checking only that each map parses, which passes a map that silently drops half the Layer menu or a whole tool group.

## 3. The Stilus Map from a Driven Illustrator Run

Stilus's reference is Illustrator: the menus, tools, and panels a vector designer's hands know. The map is captured from the installed Illustrator 30.8.2 in its Essentials workspace, not from memory, and CorelDRAW users get their shortcuts as an alternative set, since its layout cannot be followed at the same time.

**Requires:** display-session -- capturing Illustrator's menus, tools, and panels drives its user interface on an interactive desktop

- [ ] Write `scripts/capture-ui-tree.ps1`: launch an application by path, wait for its main window, and through UI Automation walk its menu bar (each top-level menu expanded in turn, each submenu recursively), its toolbars, and its docked panes (names, bounding rectangles, tab groups, and the buttons each holds, in order), then write `docs/design/layout-maps/sources/<program>-<version>.json` and close the app without saving anything. Screenshots it takes to help a person read a layout stay under `build/` and are never committed, because the reference program's artwork is not ours to redistribute. Done when: a run against Paint writes its menus, its toolbar, and its panes completely.
- [ ] Capture Illustrator 30.8.2 (`C:\Program Files\Adobe\Adobe Illustrator 2026\Support Files\Contents\Windows\Illustrator.exe`) with a new document open and the Essentials workspace reset, so document menus and the default panels are present, into `docs/design/layout-maps/sources/illustrator-30.8.2.json`. Where UI Automation cannot read a part (custom-drawn tools or panels), record that part from Adobe's Illustrator documentation with a URL, marked "from documentation, not driven". Done when: every top-level menu (File, Edit, Object, Type, Select, Effect, View, Window, Help), the toolbar with its groups, the Control and Properties panels' contents for the selection and the main tools, and the default panels with their positions and buttons are recorded.
- [ ] Write `docs/design/layout-maps/stilus.md` from the capture, all five parts: each row mapped to a Stilus feature (`same` or `renamed`) or marked `planned` with the Stilus section that builds it (the parity catalog `docs/parity/stilus-parity.md` names the owner of each Illustrator feature), `own` rows for Stilus-only features, and `omitted` rows with their reason. Done when: `python scripts/layout-map.py` reports Illustrator's placed inventory features all covered.
- [ ] Add the CorelDRAW 2026 shortcut set as a second Shortcuts table in `stilus.md`: each CorelDRAW shortcut from Corel's documentation (a URL per group, marked "from documentation, not driven"), mapped to the Stilus feature it should trigger, for `D02 T16 §3` to offer as an alternative shortcut set. Done when: the table covers every shortcut in the CorelDRAW inventory's shortcut rows.
- [ ] Add `docs/design/layout-maps/stilus.md` to the `**Design:**` line of every open section that builds a Stilus menu, the tool rail, an options bar, or a panel (the sections §7's rule names, or, before §7 ships, every section whose Fidelity line names one of those Stilus surfaces), each with a dated correction. Done when: `python scripts/todo-graph.py validate` passes and no such open section's Design line lacks the map.
- [ ] Commit: `"design: the Stilus layout map, captured from Illustrator 30.8.2"`

**Test checkpoint:** Driven run with evidence: `docs/design/layout-maps/sources/illustrator-30.8.2.json` exists from the capture script (its run output quoted with Illustrator's version); `python scripts/layout-map.py` exits 0 with Stilus's summary line showing every placed Illustrator inventory feature covered; a scratch copy of `stilus.md` with one toolbar row deleted fails the checker with that inventory id. Cheaper substitute that fails: a map typed from memory of Illustrator, which the capture file would contradict.

## 4. The Gesso Map from a Driven Photoshop Run

Gesso's reference is Photoshop, the program the suite's whole interface is modeled on. The installed Photoshop is 27.11, one minor version past the 27.10 the parity inventory pins, so the capture records 27.11 and the map notes any feature 27.10 lacks or 27.11 removed.

**Requires:** display-session -- capturing Photoshop's menus, tools, and panels drives its user interface on an interactive desktop

- [ ] Capture Photoshop 27.11 (`C:\Program Files\Adobe\Adobe Photoshop 2026\Photoshop.exe`) with a layered document open and the Essentials workspace reset, using §3's `scripts/capture-ui-tree.ps1`, into `docs/design/layout-maps/sources/photoshop-27.11.json`. Where UI Automation cannot read a part, record it from Adobe's Photoshop documentation with a URL, marked "from documentation, not driven". Done when: every top-level menu (File, Edit, Image, Layer, Type, Select, Filter, 3D where present, View, Plugins, Window, Help), the toolbar with every group and its default tool, the options bar of every tool, and the default panels (Layers, Channels, Paths, Properties, Adjustments, Libraries, Color, Swatches, Gradients, Patterns, and any others Essentials opens) with their positions, footer buttons, and panel menus are recorded.
- [ ] Write `docs/design/layout-maps/gesso.md` from the capture as §3 did for Stilus, each row mapped to a Gesso feature or marked `planned` with the owning Gesso section (`docs/parity/gesso-parity.md` names it), `renamed` only for Adobe product names (Camera Raw Filter, Content-Aware Fill, Neural Filters, Generative Fill), and a note on each feature that differs between 27.10 and 27.11. Done when: `python scripts/layout-map.py` reports Photoshop's placed inventory features all covered.
- [ ] Add `docs/design/layout-maps/gesso.md` to the `**Design:**` line of every open section that builds a Gesso menu, the tool rail, an options bar, or a panel (as §3 did for Stilus), each with a dated correction. Done when: `python scripts/todo-graph.py validate` passes and no such open section's Design line lacks the map.
- [ ] Commit: `"design: the Gesso layout map, captured from Photoshop 27.11"`

**Test checkpoint:** Driven run with evidence: `docs/design/layout-maps/sources/photoshop-27.11.json` exists from the capture script (its run output quoted with Photoshop's version); `python scripts/layout-map.py` exits 0 with Gesso's summary line showing every placed Photoshop inventory feature covered and the 27.10 to 27.11 differences listed. Cheaper substitute that fails: copying Photoshop's layout from a web page about an older version, which the capture's version line would contradict.

## 5. The Albumen Map from Lightroom Classic's Documentation

Albumen's reference is Lightroom Classic, whose menus, tool strip, and panels change with the module (Library, Develop, Map, Book, Slideshow, Print, Web). Lightroom Classic is not installed on this machine, so this map comes from Adobe's documentation, every part marked as such, until a driven capture replaces it.

- [ ] Record Lightroom Classic 15.5.1's layout per module from Adobe's documentation (a URL per part), using §1's contexts: the menus common to every module once, and each module's own menus, its tool strip (the Develop module's Crop, Remove, Red Eye, and Masking tools), its left and right panel stacks in order with each panel's controls in order, and its filmstrip and toolbar, with shortcuts from Adobe's shortcut pages. Done when: every module's layout is recorded, each part marked "from documentation, not driven".
- [ ] Write `docs/design/layout-maps/albumen.md`, each row mapped to an Albumen feature or marked `planned` with the owning Albumen section (`docs/parity/albumen-parity.md` names it), and the modules mapped to Albumen's pages (Library to Browse and the catalog, Develop to Develop, the output modules to Albumen's output sections). Done when: `python scripts/layout-map.py` reports Lightroom Classic's placed inventory features all covered.
- [ ] File through `add-todo` the driven capture that will replace the documentation once Lightroom Classic is installed on a machine the runner can use, as an operator row in `todo/99-manual/` if the install needs the operator's Adobe account. Done when: the row exists and this map's header names it.
- [ ] Add `docs/design/layout-maps/albumen.md` to the `**Design:**` line of every open section that builds an Albumen menu, tool strip, or panel (as §3 did for Stilus), each with a dated correction. Done when: `python scripts/todo-graph.py validate` passes and no such open section's Design line lacks the map.
- [ ] Commit: `"design: the Albumen layout map from Lightroom Classic 15.5.1"`

**Test checkpoint:** Driven run with evidence: `docs/design/layout-maps/albumen.md` exists with a context per Lightroom Classic module and a URL per part; `python scripts/layout-map.py` exits 0 with Albumen's summary line showing every placed Lightroom Classic inventory feature covered. Cheaper substitute that fails: one flat layout for all modules, which misplaces every module-specific menu, tool, and panel.

## 6. The Shared Layout Conformance Test Helpers

All three apps need the same checks, so they are written once in `Isotone.UI`'s test support and each app's tests only supply its map and a snapshot of its real window. They compare what a user would see with the map and report every difference at once.

- [ ] Add a `LayoutSnapshot` model to the `Isotone.UI` test support (the test project `D01 T01 §1` creates, shipped as a shared test library both apps' test projects reference): the menu tree (items, order, separators, enabled state, tooltip, `InputGestureText`), the tool rail (groups in order, tools in each group with the default first, each tool's shortcut and enabled state), each tool's options-bar controls in order, and the default dock layout (each pane's id, dock side, tab group, order, collapsed state, and its buttons in order). Add the builders that read a snapshot from a loaded WPF window (a menu walker, a tool rail walker over the shared `ToolRail` control, an options bar walker, and a dock layout reader over the window's docking manager) on the UI thread without showing it. Done when: each builder reads a fixture window built for it.
- [ ] Add `LayoutMapConformance`: load a map (with a context name when the map has contexts) and compare it with a `LayoutSnapshot`, part by part, returning every difference: missing, extra, wrong order or position, wrong label, wrong shortcut, and a `planned` row that is enabled or lacks the tooltip naming its owner. `own` rows follow their rule (after the reference items, behind a separator), `omitted` rows are absent, and a planned panel is checked in the Window menu rather than the dock. Done when: a fixture snapshot built to differ from a fixture map in each way returns exactly that difference.
- [ ] Format the differences as one readable report (part, path, expected, actual) so a failing app test names every drift in one run. Done when: a fixture with three differences across two parts fails with all three listed.
- [ ] Commit: `"ui: shared tests that hold an app's menus, tools, and panels to its layout map"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~LayoutMapConformance|FullyQualifiedName~LayoutSnapshot"` exits 0 with a case per difference kind and per builder; deleting the order comparison from the conformance helper fails the wrong-order cases (quoted, then restored). Cheaper substitute that fails: comparing only the set of labels, which passes a window with every item in the wrong place.

## 7. Every Layout Section Cites Its Map

The maps only steer the apps if the sections that build those surfaces read them. This section makes the citation part of the Design line grammar `scripts/todo-graph.py` already enforces, and orders every such section after the map it needs.

- [ ] Add the rule to `scripts/todo-graph.py validate` as `design-layout-map-missing` (FATAL): a section whose `**Fidelity:**` line names a menu bar, a named menu, "every menu", the tool rail or toolbar, an options bar, or a panel of Stilus, Gesso, or Albumen must depend, directly or through its dependencies, on the `D01 T13` section that writes `docs/design/layout-maps/<app>.md`, and once that map exists must cite it on its `**Design:**` line (before then it cannot, since `design-dead-ref` refuses a ref to a missing file). Context menus and dialogs are outside the rule; a dialog's counterpart order is held by the design contract's clause from §1. Done when: the self-test has a failing and a passing case for each clause.
- [ ] Run the rule over the tree and fix every section it names: add the `D01 T13` dependency where the order is missing, and add each map that exists by then to its sections' Design lines, each with a dated correction; a map written later is added to its sections' Design lines by the section that writes it (§3, §4, §5). Done when: `python scripts/todo-graph.py validate` reports no `design-layout-map-missing` and the commit body lists every section changed.
- [ ] Document the rule in `todo/README.md` (Surface fidelity, and the FATAL table) and in `standards/design-contract.md` beside §1's clause. Done when: both name the rule.
- [ ] Commit: `"todo: every menu, tool, and panel section cites its app's layout map"`

**Test checkpoint:** Unit test and static analysis: `python scripts/todo-graph.py self-test` reports `0 failed` with the new cases; `python scripts/todo-graph.py validate` exits 0; removing the map from one menu section's Design line fails `validate` with `design-layout-map-missing` naming it (quoted, then restored). Cheaper substitute that fails: a note in the README asking authors to cite the map, which the next section authored without it would pass.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0, with `layout-map self-test` and `layout-map` listed as PASS
- [ ] `python scripts/layout-map.py` prints one summary line per map, every placed competitor inventory feature covered
- [ ] `dotnet test Isotone.slnx` exits 0 with `LayoutMapConformance` and each app's layout map tests reporting
- [ ] `python scripts/todo-graph.py validate` clean, with no `design-layout-map-missing`
