---
schema_version: 1
id: nodus-roadmap
domain: 02-nodus
status: draft
title: "TODO-06 -- Nodus after 0.1.0: Deferral Owners and Accessibility"
depends_on: []
track: N6
---

# TODO-06 -- Nodus after 0.1.0: Deferral Owners and Accessibility

> **Goal:** The Nodus work after its first release that the plan is already committed to: the sections that 0.1.0 work names as the owner of a disabled command, a planned menu stub, or a deferred service, and the accessibility and localization work the acceptance bar requires. When this file closes, no Nodus control defers to a section that does not ship, no triaged service is left unwired, and Nodus works without a mouse or eyes.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The legacy roadmap (`docs/legacy/nodus-roadmap.md`, 3,199 lines, phases 0 to 25) was mined into 21 sections on 2026-09-26. The same day the plan was bounded (`todo/budget.json`): the 13 sections nothing outside this file depends on, defers to, or names in the acceptance bar moved to `todo/backlog.md` as B-001 to B-013, and their section numbers are retired, never reused. What stays: path editing (§2) and text to path (§3), which `D02 T02 §5` and `D02 T03 §5` name for disabled or planned commands; tabs (§7), which `D02 T04 §6` names for multi-file open and §11 builds on; the three sections the triage in `D02 T02 §1` hands its deferred services to (§11, §12, §14); Preferences (§13), which `D02 T03 §5` and `D02 T05 §2` name; and accessibility (§17), which the acceptance bar names. Services exist for several of these features, but none is reachable from the app. Every section below names its legacy source with a `-> SOURCE:` line.
<!-- claim: lines docs/legacy/nodus-roadmap.md = 3199 -->
<!-- claim: exists src/Nodus/Bezier.Core/Services/SymbolLibraryService.cs -->
<!-- claim: exists src/Nodus/Bezier.Core/Services/CommandPaletteService.cs -->

## Inputs

- [`docs/legacy/nodus-roadmap.md`](../../docs/legacy/nodus-roadmap.md) -- the source of every section here; read the named legacy phase before grooming a section
- [`standards/nodus.md`](../../standards/nodus.md) -- the document model, tool, and SVG rules every section builds to
- `docs/dev/nodus/service-triage.md` (written by `D02 T02 §1`) -- the deferred services §11, §12, and §14 wire
- -> XREF: D02 T02 §1 -- the triage that hands the deferred services to §11, §12, and §14
- [`../backlog.md`](../backlog.md) -- the Nodus feature ideas that left this file (B-001 to B-013); one is promoted only through `add-todo` with the admission test and budget room

## Outcome

- Every section below ships with its surface, its commands with undo, its settings, its log lines, its user-guide page, and its tests, like the 0.1.0 sections before it.
- No deferred service from the triage remains unwired when this file closes, and no disabled or planned Nodus command names a section of this file that has not shipped.

**Adjacency:** list=applicable @ D02 T06 §11; document=not-applicable (printing and prepress wait in the backlog as B-011); settings=applicable @ D02 T06 §13; reporting=not-applicable (measurement and the Info panel wait in the backlog as B-007; document info lives in the status strip, D02 T03 §5); notifications=applicable; permissions=not-applicable (file refusals are owned by the save and export sections in D02 T04); audit=applicable; exchange=applicable @ D02 T06 §14; reverse=applicable

**Adjacency rationale:** The asset library is the browsable list; the Preferences dialog is the settings surface; long exports notify through the status strip; every edit in every section is a logged, undoable command.

## Implementation Order

| Order | Section | Deliverable                                              | Depends On  | Status |
| :---: | :-----: | -------------------------------------------------------- | ----------- | :----: |
| 1 | §2 | Path editing: continue, join, break, reverse, simplify   | D02 T05 §4  |  [ ]   |
| 2 | §3 | Text: area text, text on path, text to path             | D02 T05 §4  |  [ ]   |
| 3 | §7 | Documents in tabs, saved layouts, nested layers          | D02 T05 §4  |  [ ]   |
| 4 | §11 | Symbols and the asset library                            | §7          |  [ ]   |
| 5 | §12 | The command palette and the on-canvas HUD                | D02 T05 §4  |  [ ]   |
| 6 | §13 | Preferences and shortcut remapping                       | D02 T05 §4  |  [ ]   |
| 7 | §14 | More formats and the export dialog                       | D02 T05 §4  |  [ ]   |
| 8 | §17 | Accessibility and localization                           | §13         |  [ ]   |

---

## 2. Path Editing: Continue, Join, Break, Reverse, Simplify

The pen and node tools draw and move nodes; real path work also needs continuing an open path, joining two end points, breaking at a node, reversing direction, simplifying a noisy path, and converting a stroke to its outline. `PathOperationsService` has signatures for several; `SKPath` supplies the geometry. -> SOURCE: legacy-nodus-3.3-3.4

**Fidelity:** Nodus canvas and Path menu -- docs/captures/nodus/main-window/.
**Job:** a designer can repair and refine paths node by node. Consumer: the document.
**Treatment:** pen continues an open path when started on its end node; Path, Join (two selected end nodes), Break at Node, Reverse, Close, Simplify (tolerance slider with live preview), and Stroke to Path (via `SKPaint.GetFillPath`), each one undo step. Cheaper substitute that fails the checkpoint: operations that rebuild the whole path and lose node types.
**Chrome:** consume the node tool, `PathOperationsService`, and the history.

**Requires:** display-session -- node-level editing on the canvas needs an interactive desktop

- [ ] Implement continue, join, break, reverse, and close in the node model with tests on node counts and types. Done when: each has a passing test and an undo test.
- [ ] Implement `Simplify` (Ramer-Douglas-Peucker on flattened segments, refit to cubics) and `StrokeToPath`. Done when: tests bound the node reduction and the outline area.
- [ ] Enable the `Simplify` and `StrokeToPath` menu items and remove their planned entries. Done when: `MenuAuditTests` passes with them enabled.
- [ ] Commit: `"nodus: continue, join, break, reverse, simplify, and outline paths"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the path-editing tests reporting; a driven session joins two open paths and simplifies the result, and undo restores each step (log lines quoted). Cheaper substitute that fails: join by grouping.

## 3. Text: Area Text, Text on Path, Text to Path

Point text exists. Layouts need text flowing inside a shape, text following a curve, and text converted to outlines for hand-off. -> SOURCE: legacy-nodus-3.5

**Fidelity:** Nodus canvas, text tool -- docs/captures/nodus/main-window/.
**Job:** a designer can flow text in a shape, set text along a path, and outline text. Consumer: the document and the SVG writer.
**Treatment:** dragging the text tool makes an area text box (SVG 2 `shape-inside` written with a `<foreignObject>`-free fallback of positioned `<tspan>` lines); clicking a path with the text tool attaches text with `<textPath>`; Path, Text to Path outlines glyphs through `SKFont.GetTextPath`. Cheaper substitute that fails the checkpoint: rasterized text.
**Chrome:** consume the text tool and `SkiaRenderer`'s font cache.

**Requires:** display-session -- text layout on the canvas needs an interactive desktop

- [ ] Area text layout with wrapping and alignment, round-tripped through SVG. Done when: a fixture renders line breaks identically after reopen.
- [ ] Text on path with start offset, round-tripped as `<textPath>`. Done when: Inkscape renders the saved file with text on the curve.
- [ ] Text to Path, enabling the planned menu item. Done when: the outlined glyph count matches the character count for a Latin sample.
- [ ] Commit: `"nodus: area text, text on a path, and text to outlines"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with text fidelity fixtures reporting; the three driven cases are captured. Cheaper substitute that fails: text to path that returns a bitmap.

## 7. Documents in Tabs, Saved Layouts, Nested Layers

Nodus opens one document at a time; the history and selection are app singletons. Multiple documents need per-document scopes, tabs with dirty markers, and dock layouts that persist. The layers panel shows nested groups as one row. -> SOURCE: legacy-nodus-2.4-2.9

**Fidelity:** Nodus main window with document tabs -- docs/captures/nodus/main-window/.
**Job:** a designer can work on several documents at once, each with its own undo and selection, and keep a panel layout. Consumer: every service scoped per document.
**Treatment:** AvalonDock document tabs with `name*` for dirty; a DI scope per document owning its history, selection, and tool state; Window, Save Layout and Reset Layout persisted to the app-data folder; the layers panel becomes a tree with expandable groups. Cheaper substitute that fails the checkpoint: tabs sharing one history.
**Chrome:** consume AvalonDock with the suite theme and the `Photon.Core` single-instance service for opening files into new tabs.

**Requires:** display-session -- tabbed documents need an interactive desktop

- [ ] Per-document DI scope for history, selection, and tool state. Done when: a test proves undo in one document does not affect another.
- [ ] Document tabs with dirty prompts per tab and on exit (listing every dirty document). Done when: a driven exit with two dirty tabs shows one prompt naming both.
- [ ] Saved and reset layouts. Done when: a layout survives a restart.
- [ ] Layers tree with nested groups. Done when: a nested fixture shows its hierarchy.
- [ ] Commit: `"nodus: multiple documents in tabs with per-document undo and saved layouts"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the scope tests reporting; the driven multi-document run is captured. Cheaper substitute that fails: a second window per document.

## 11. Symbols and the Asset Library

`SymbolLibraryService` and `AssetLibraryService` exist and are deferred here by the triage. Symbols (reusable definitions with instances) are how designers keep icon sets consistent; the asset library holds reusable artwork across documents. -> SOURCE: legacy-nodus-4.5-10.5

**Fidelity:** Symbols and Assets panels -- new build, no baseline; captured to docs/captures/nodus/symbols/ and docs/captures/nodus/assets/.
**Job:** a designer can make a symbol from a selection, place instances, edit the master and see every instance update, and store artwork in a searchable library. Consumer: the document (`<symbol>`/`<use>` in SVG) and the app-data library folder.
**Treatment:** symbols map to SVG `<symbol>` and `<use>`; the asset library is a folder of SVG files under the app-data folder with a searchable grid, drag onto canvas, and favorites; the services lose their "Deferred" markers. Cheaper substitute that fails the checkpoint: symbols that copy geometry into each instance.
**Chrome:** consume the deferred services, the icon catalog, and the theme.

**Requires:** display-session -- the panels need an interactive desktop

- [ ] Wire `SymbolLibraryService` with make, place, edit master, and break link, each undoable. Done when: a fixture with symbols round-trips.
- [ ] Wire `AssetLibraryService` (with the injected folder from `D00 T02 §1`) into a searchable panel with an empty state. Done when: search and favorites are tested.
- [ ] Commit: `"nodus: symbols and the asset library"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the symbol and library tests reporting; editing a master updates three instances on a driven run (capture). Cheaper substitute that fails: copied geometry.

## 12. The Command Palette and the On-Canvas HUD

`CommandPaletteService`, `CanvasHUDService`, and `PresetService` are deferred here. A command palette (Ctrl+K) makes every command reachable by name; the HUD shows live dimensions and angles while dragging. -> SOURCE: legacy-nodus-5.3-5.4

**Fidelity:** Command palette overlay and canvas HUD -- new build, no baseline; captured to docs/captures/nodus/command-palette/ and docs/captures/nodus/hud/.
**Job:** a user can run any command by typing its name, and see exact values while dragging. Consumer: the keymap's commands; the tools.
**Treatment:** Ctrl+K opens a filtered list of every keymap command with its gesture, fuzzy-matched, Enter runs; the HUD draws width, height, angle, and distance near the cursor during drags, respecting the unit setting. Cheaper substitute that fails the checkpoint: a palette with its own command list.
**Chrome:** consume the keymap, the overlay layer, and the theme.

**Requires:** display-session -- the overlay and HUD need an interactive desktop

- [ ] Wire `CommandPaletteService` to the keymap. Done when: every keymap command is findable by name in a test.
- [ ] Wire `CanvasHUDService` into the select and shape tools. Done when: a capture shows the HUD during a resize.
- [ ] Decide `PresetService`'s fate (wire into tool presets or delete) and record it in the triage document. Done when: the service is wired or gone.
- [ ] Commit: `"nodus: a command palette and an on-canvas HUD"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with palette search tests reporting; captures committed. Cheaper substitute that fails: a palette listing menu headers only.

## 13. Preferences and Shortcut Remapping

Settings accumulate across sections (snapping, autosave, export defaults, units) with no surface except their menus. A Preferences dialog makes each reachable, and the shortcuts dialog gains remapping. -> SOURCE: legacy-nodus-11-5.5

**Fidelity:** Preferences dialog -- new build, no baseline; captured to docs/captures/nodus/preferences/.
**Job:** a user can change every Nodus setting in one place and remap shortcuts, with conflicts refused. Consumer: every setting's named consumer.
**Treatment:** a categorized dialog (General, Units, Canvas, Snapping, Autosave, Export, Shortcuts) bound to `NodusSettings`, applying on OK with Cancel reverting; the Shortcuts page edits the keymap with conflict detection and reset to defaults, stored in settings. Cheaper substitute that fails the checkpoint: a JSON file the user edits by hand.
**Chrome:** consume the settings store, the keymap, and the theme; share nothing with Imago until Imago builds its own preferences (then file a `Photon.UI` move).

**Requires:** display-session -- the dialog needs an interactive desktop

- [ ] Preferences dialog over every existing setting key, each with a label, default, and tooltip. Done when: a test enumerates `NodusSettings` keys and asserts each has a control.
- [ ] Shortcut remapping with conflicts refused by name. Done when: a remapped gesture survives restart and a conflicting one is refused.
- [ ] Enable File, Preferences and remove its planned entry. Done when: `MenuAuditTests` passes.
- [ ] Commit: `"nodus: a Preferences dialog and shortcut remapping"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the preferences tests reporting; a driven change of the autosave interval appears in `settings.json` and the log. Cheaper substitute that fails: settings without a surface.

## 14. More Formats and the Export Dialog

`ImportService`, `ExportDialogService`, and `CodeEditorService` are deferred here. Designers need placing raster images, importing EMF and PDF artwork, and exporting WebP, ICO, optimized SVG, and XAML or code snippets, with presets. -> SOURCE: legacy-nodus-10.2-10.4

**Fidelity:** Export dialog -- docs/captures/nodus/export-raster/ (from `D02 T04 §3`), extended.
**Job:** a designer can place images and export to every format a hand-off needs, from one dialog with presets. Consumer: the exported files and other applications.
**Treatment:** File, Place for PNG, JPEG, and WebP (embedded as data URIs or linked); one export dialog over every format with saved presets; XAML export enabled (removing its planned entry); each reader and writer with a fidelity fixture. Cheaper substitute that fails the checkpoint: one dialog per format.
**Chrome:** consume the deferred services, `AtomicFileWriter`, and the export sections' renderers.

**Requires:** display-session -- the dialog needs an interactive desktop

- [ ] Wire `ImportService` for placed images with fidelity fixtures. Done when: placed images round-trip.
- [ ] Wire `ExportDialogService` into one dialog with presets; add WebP, ICO, optimized SVG, and XAML writers, each with a fixture. Done when: every writer passes its fidelity test.
- [ ] Decide `CodeEditorService` (an SVG source view) against its need, record it in the triage, and wire or delete it. Done when: the service is wired or gone.
- [ ] Commit: `"nodus: placed images, more export formats, and one export dialog"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes every new format fixture; `MenuAuditTests` passes with XAML export enabled. Cheaper substitute that fails: formats without fixtures.

## 17. Accessibility and Localization

Every surface must be operable by keyboard and screen reader and translatable. -> SOURCE: legacy-nodus-13

- [ ] Audit every window with Accessibility Insights for Windows (version quoted) and fix every failure; add missing `AutomationProperties`. Done when: the audit report shows no failures and is committed under `docs/dev/nodus/accessibility/`.
- [ ] Move every user-visible string to `.resx` resources with a pseudo-localized build that proves no string is hardcoded. Done when: the pseudo-locale run shows every string transformed (capture).
- [ ] High contrast and 200 percent scaling pass on every window. Done when: captures at both are committed.
- [ ] Commit: `"nodus: accessibility audit fixes and localizable strings"`

**Requires:** display-session -- the accessibility audit and captures need an interactive desktop

**Test checkpoint:** the committed audit report shows zero failures; the pseudo-locale capture shows no untransformed string. Cheaper substitute that fails: adding automation names only to toolbar buttons.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] No service in `docs/dev/nodus/service-triage.md` is still marked deferred
- [ ] Every new format has a fidelity fixture
- [ ] `python scripts/todo-graph.py validate` clean
