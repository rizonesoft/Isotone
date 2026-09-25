---
schema_version: 1
id: nodus-service-triage
domain: 02-nodus
status: draft
title: "TODO-02 -- Core Service Triage: Wire, Defer, or Delete"
depends_on: []
track: N2
---

# TODO-02 -- Core Service Triage: Wire, Defer, or Delete

> **Goal:** No Nodus service exists only for its tests. Each of the services the app never calls is wired into a working command, handed to a named later section, or deleted with its tests; there is one SVG render path; and the selection, arrange, boolean, layers, snapping, and keyboard services the 0.1.0 release needs are reachable from the rendered app with undo.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `src/Nodus/Bezier.Core/Services/` holds 31 files. 25 of them are referenced by no file in `Bezier.Desktop` (measured by name with `grep -rlw`): AlignmentService, AnimationService, ArtboardManager (used only by `VectorDocument`), AssetLibraryService, CanvasHUDService, CanvasTooltipService, CodeEditorService, CommandPaletteService, ExportDialogService, ExportService, FileOperationsService, ImportService, LayerManager, MicroInteractionService, PathOperationsService, PresetService, SelectionManager, ShortcutManager, SnapManager, SymbolLibraryService, ThemeManager, ToastNotificationService, TransformService, VisualFeedbackService, and `SvgParser.cs` (which holds the `SvgImporter` class the app does use). All but the importer have a test file. Some are placeholders: `PathOperationsService.BooleanOp` returns its first input unchanged ("This will be implemented with SkiaSharp in the Desktop layer"), and the file carries 10 such "Placeholder" or "will be implemented" markers. The Object and Path menus call view-model commands (`AlignLeft`, `Rotate90Cw`, `Union`, and the rest) whose bodies only set `StatusText` (26 such bodies). `SelectTool` keeps its own `_selectedElements` list and never consults `SelectionManager`. Three Desktop services are dead too: `SvgVisualEditor.cs` (the only user of SharpVectors), `SvgCanvasRenderer.cs`, and `SvgOptimizerService.cs`; no `.cs` file uses Svg.Skia. The layers panel is an `ItemsControl` over `Document.Elements` with no reorder, lock, or visibility toggle.
<!-- claim: count "Placeholder|will be implemented" src/Nodus/Bezier.Core/Services/PathOperationsService.cs = 10 -->
<!-- claim: count "private readonly List<VectorElement> _selectedElements" src/Nodus/Bezier.Core/Tools/SelectTool.cs = 1 -->
<!-- claim: count "using SharpVectors" src/Nodus/Bezier.Desktop/Services/SvgVisualEditor.cs = 4 -->
<!-- claim: count "StatusText = \"(Align|Distribute|Rotate|Flip|Union|Subtract|Intersect|Exclude|Simplify|Convert|Group|Ungroup|Bring|Send)" src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 26 -->
<!-- claim: exists src/Nodus/Bezier.Core/Services/ThemeManager.cs -->

## Inputs

- [`standards/nodus.md`](../../standards/nodus.md) -- one SVG render path; the document model is the single source of truth; every mutation is a command
- [`docs/legacy/nodus-roadmap.md`](../../docs/legacy/nodus-roadmap.md) -- where each service came from (its checked items are unverified)
- `src/Nodus/Photon.Nodus.Core/Services/` (after `D02 T01 §1`) -- the services triaged here
- -> XREF: D02 T06 §11 -- owns the deferred symbol and asset library services
- -> XREF: D02 T06 §12 -- owns the deferred command palette and on-canvas HUD services
- -> XREF: D02 T06 §14 -- owns the deferred import and export-dialog services
- -> XREF: D02 T03 §5 -- the menu sweep that consumes every command this file wires

## Outcome

- `docs/dev/nodus/service-triage.md` gives every service in `Photon.Nodus.Core/Services/` a verdict (wired here, deferred to a named section, or deleted) with its evidence.
- The delete group is gone with its tests; the deferred group names a live `D02 T06` section each.
- SharpVectors and Svg.Skia are out of the solution, and one render path remains.
- Selection has one owner (`SelectionManager`), and every tool and command reads it.
- Arrange, align, distribute, rotate, flip, and the four boolean operations change the document through commands, with undo, from the menus.
- The layers panel reorders, hides, locks, and renames elements with undo; snapping and one keymap work on the canvas.

**Adjacency:** list=applicable @ D02 T02 §6; document=not-applicable (printing is a roadmap item, D02 T06 §19); settings=applicable @ D02 T02 §7; reporting=not-applicable (document info lives in the status strip, D02 T03 §5); notifications=not-applicable (every operation here is instant on a 0.1.0-sized document); permissions=not-applicable (no files are written here); audit=applicable @ D02 T02 §4; exchange=not-applicable (formats are D02 T04's); reverse=applicable @ D02 T02 §4

**Adjacency rationale:** The layers panel is the list of a document's elements; snapping options are settings; every arrange, align, boolean, and layers action is a command, so it is both logged (audit) and undoable (reverse).

## Implementation Order

| Order | Section | Deliverable                                          | Depends On                 | Status |
| :---: | :-----: | ---------------------------------------------------- | -------------------------- | :----: |
|   1   |   §1    | The triage record and the delete group               | D02 T01 §1                 |  [ ]   |
|   2   |   §2    | One SVG render path                                  | §1                         |  [ ]   |
|   3   |   §3    | Selection has one owner                              | §1, D02 T01 §2             |  [ ]   |
|   4   |   §4    | Arrange, align, distribute, rotate, and flip         | §3, D02 T03 §2             |  [ ]   |
|   5   |   §5    | Boolean path operations on SKPath.Op                 | §3, D02 T01 §6             |  [ ]   |
|   6   |   §6    | The layers panel on LayerManager                     | §3, D02 T03 §2             |  [ ]   |
|   7   |   §7    | Snapping on SnapManager                              | §3                         |  [ ]   |
|   8   |   §8    | One keymap on ShortcutManager                        | D02 T03 §2                 |  [ ]   |

---

## 1. The Triage Record and the Delete Group

Orphan code costs twice: it reads as a feature that exists, and it has to be kept compiling through every migration. The rule for a verdict: **wire** when the 0.1.0 release needs the behavior and the service does it (or can after a fix); **defer** when a roadmap section will need it and the code is sound, naming that section; **delete** when WPF or another owner already does the job, or the service is a placeholder a rewrite would replace anyway. The default verdicts below are this plan's; the section confirms each against the code and records any change with its reason.

| Service | Default verdict | Why |
| ------- | --------------- | --- |
| SelectionManager | wire (§3) | Selection must have one owner; `SelectTool` keeps a private list |
| AlignmentService, TransformService | wire (§4) | Align, distribute, rotate, and flip are menu commands with stub bodies |
| PathOperationsService | wire after a rewrite (§5) | Boolean ops are placeholders; `SKPath.Op` does the real work |
| LayerManager | wire (§6) | The layers panel needs reorder, hide, lock, rename |
| SnapManager | wire (§7) | Tools need snapping to grid, guides, and objects |
| ShortcutManager | wire (§8) | One keymap for dispatch and the shortcuts dialog |
| FileOperationsService | wire (`D02 T04 §5`) | Recent files and autosave drafts |
| ExportService | wire (`D02 T04 §3`) | Raster and optimized-SVG export |
| ArtboardManager | keep (used by `VectorDocument`) | Not an orphan |
| SymbolLibraryService, AssetLibraryService | defer (`D02 T06 §11`) | Symbols and the asset library are roadmap features |
| CommandPaletteService, CanvasHUDService, PresetService | defer (`D02 T06 §12`) | Palette and HUD are roadmap features |
| ImportService, ExportDialogService, CodeEditorService | defer (`D02 T06 §14`) | More formats and code export are roadmap features |
| ThemeManager | delete | The suite theme lives in `Photon.UI` (`D01 T01 §3`); Catppuccin switching is retired |
| AnimationService, MicroInteractionService, VisualFeedbackService, CanvasTooltipService | delete | UI effects modeled in a non-UI project; WPF storyboards and tooltips do this in the view |
| ToastNotificationService | delete | Status feedback goes through the status strip; a toast system, if wanted, is a `Photon.UI` feature filed through `add-todo` |

- [ ] Write `docs/dev/nodus/service-triage.md` with one row per file in `src/Nodus/Photon.Nodus.Core/Services/`: verdict, owner section (a `DNN TNN §N` ref that `python scripts/todo-graph.py resolve` accepts), evidence (the grep or file and line that justified it). Done when: every file in the folder has a row and every owner ref resolves.
- [ ] Delete `ThemeManager.cs`, `AnimationService.cs`, `MicroInteractionService.cs`, `VisualFeedbackService.cs`, `CanvasTooltipService.cs`, and `ToastNotificationService.cs` with their test files (`ThemeTests.cs`, `FluidMotionTests.cs`, and the matching classes in `UIPolishTests.cs`/`UIPolishPhase4Tests.cs`). Done when: `grep -rn "ThemeManager\|AnimationService\|MicroInteractionService\|VisualFeedbackService\|CanvasTooltipService\|ToastNotificationService" src tests` prints nothing.
- [ ] Put a one-line `// Deferred to D02 T06 §N (docs/dev/nodus/service-triage.md)` comment at the top of each deferred service. Done when: `grep -l "Deferred to D02 T06" src/Nodus/Photon.Nodus.Core/Services/*.cs` lists every deferred file.
- [ ] Commit: `"nodus: triage the orphan services and delete the ones WPF already covers"`

**Test checkpoint:** `dotnet build Photon.slnx -c Release` exits 0; `dotnet test Photon.slnx` exits 0 with the count lower by exactly the deleted test methods (quote before and after); every owner ref in the triage record resolves (`python scripts/todo-graph.py resolve '<ref>'` exit code 0 or 4, never 1 or 2). Cheaper substitute that fails: a triage table with no deletions, which leaves every orphan compiling.

## 2. One SVG Render Path

Three SVG stacks are referenced and one is used. The live path is `SvgImporter` (in `SvgParser.cs`) building the `VectorDocument`, rendered by `SkiaRenderer`. SharpVectors is used only by `SvgVisualEditor.cs`, which nothing calls; Svg.Skia is referenced and used by nothing. Keeping them costs installer size, a second pinned SkiaSharp consumer (Svg.Skia 4.9.1 is the reason SkiaSharp is held at 3.x), and a false impression of two renderers. **Decision (from this evidence): drop both.** The fidelity oracle for SVG is Inkscape (`standards/nodus.md`), not a second in-app renderer.

- [ ] Delete `src/Nodus/Photon.Nodus.Desktop/Services/SvgVisualEditor.cs`, `SvgCanvasRenderer.cs`, and `SvgOptimizerService.cs` (confirm with `grep -rlw` that nothing references each first; if `ExportService` needs optimization, it keeps its own `ExportSvgOptimized`). Done when: the three files are gone and the build is green.
- [ ] Remove `SharpVectors.Wpf` and `Svg.Skia` from `Photon.Nodus.Desktop.csproj` and `Directory.Packages.props`, and their rows from `docs/dev/build.md`. Done when: `grep -rn "SharpVectors\|Svg.Skia" src Directory.Packages.props` prints nothing.
- [ ] Record the decision in `docs/dev/decisions.md` (evidence: the greps; cost of change: re-adding a package if a second renderer is ever wanted for comparison tests). Done when: the entry exists.
- [ ] Rename `SvgParser.cs` to `SvgImporter.cs` so the file matches its class. Done when: `git log --follow` on the new name shows the history.
- [ ] Commit: `"nodus: one SVG render path; drop SharpVectors and Svg.Skia"`

**Test checkpoint:** `dotnet build Photon.slnx -c Release` exits 0; `dotnet test Photon.slnx` exits 0 with the same count; `pwsh scripts/publish.ps1 -App Nodus` output contains no `SharpVectors*.dll` or `Svg*.dll` (quote the `Get-ChildItem` result) and is smaller than before (quote both sizes). Cheaper substitute that fails: removing the package references and leaving `SvgVisualEditor.cs` excluded from compilation.

## 3. Selection Has One Owner

`SelectTool` holds the selection in a private list, so nothing else (the layers panel, the arrange commands, the properties panel, clipboard) can read or set it without going through the tool. `SelectionManager` exists for this and is unused. The selection becomes a document-scoped service every consumer reads.

- [ ] Register `SelectionManager` in `AddNodusServices` (singleton for now; per-document with tabs, `D02 T06 §7`). Done when: `ServiceRegistrationTests` resolves it.
- [ ] `SelectTool` reads and writes `SelectionManager` instead of `_selectedElements`; its `SelectionChanged` event is replaced by the manager's. Done when: the private list is gone and `SelectTool` tests pass against the manager.
- [ ] The view model's selection-dependent state (the properties panel, `CanExecute` of commands that need a selection) reads `SelectionManager`. Done when: selecting and deselecting on the canvas enables and disables Object, Group (log line quoted from a driven run).
- [ ] Deleting an element through undo or a command removes it from the selection. Done when: `SelectionManagerTests.RemovedElement_LeavesSelection` passes.
- [ ] Commit: `"nodus: one selection owner every tool and command reads"`

**Requires:** display-session -- the driven canvas run proving selection enables the Object menu needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `SelectionManagerTests` and the `SelectTool` tests reporting; `grep -n "_selectedElements" src/Nodus/Photon.Nodus.Core/Tools/SelectTool.cs` prints nothing; a driven run selects a rectangle and the Object, Group item becomes enabled. Cheaper substitute that fails: `SelectionManager` mirroring the tool's list, which leaves two sources of truth.

## 4. Arrange, Align, Distribute, Rotate, and Flip

The Object menu lists nineteen commands; their bodies set status text and do nothing. `AlignmentService` and `TransformService` compute the geometry, and `ReorderCommand`, `MoveCommand`, and `RotateCommand` exist. This section connects them, one command per action so each is one undo step and one log line.

**Fidelity:** Nodus main window, Object menu -- docs/captures/nodus/main-window/. Menu order, wording, and shortcuts unchanged; commands that need a selection are disabled without one.
**Job:** a designer can align, distribute, reorder, rotate, and flip selected objects and undo each. Consumer: the document, the canvas, and the history panel.
**Treatment:** each menu command runs a `CompositeCommand` built from the service's computed deltas, recorded as one history entry named after the action ("Align Left", "Flip Horizontal"). Cheaper substitute that fails the checkpoint: mutating element coordinates directly, which leaves nothing to undo.
**Chrome:** consume the existing menu, the shared history, and `SelectionManager`. Do not add a second alignment surface.

**Requires:** display-session -- driving the Object menu on the canvas needs an interactive desktop

- [ ] Add `CompositeCommand` (a named list of commands executed and undone as one) to `Photon.Nodus.Core/Commands/` if the history lacks one. Done when: `CompositeCommandTests` prove undo reverses in reverse order.
- [ ] Wire `AlignLeft`, `AlignCenter`, `AlignRight`, `AlignTop`, `AlignMiddle`, `AlignBottom` to `AlignmentService`, aligning to the selection bounds (to the artboard when one element is selected). Done when: `ArrangeCommandTests` cover each with two elements.
- [ ] Wire `DistributeHorizontally` and `DistributeVertically` (centers, three or more elements; disabled with fewer). Done when: tests cover three elements and the disabled state.
- [ ] Wire `BringToFront`, `BringForward`, `SendBackward`, `SendToBack` through `ReorderCommand`. Done when: tests assert the resulting z-order.
- [ ] Wire `Rotate90Cw`, `Rotate90Ccw`, `Rotate180`, `FlipHorizontal`, `FlipVertical` through `TransformService` about the selection center. Done when: tests assert the transformed bounds and that undo restores the original matrix exactly.
- [ ] Wire `Group` and `Ungroup` through `GroupCommand`/`UngroupCommand` (they exist and are tested). Done when: the menu items group and ungroup the selection with undo.
- [ ] Each command logs one Information line (`{Action} applied to {Count} element(s)`). Done when: a test logger asserts it for one command.
- [ ] Commit: `"nodus: wire arrange, align, distribute, rotate, flip, and group with undo"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `ArrangeCommandTests` and `CompositeCommandTests` reporting; a driven run of each menu item on a three-rectangle document followed by Ctrl+Z restores the original (log lines for apply and undo quoted; capture `docs/captures/nodus/main-window/arrange-100.png` of the aligned result). Cheaper substitute that fails: status text that says "Aligned", which the undo check exposes.

## 5. Boolean Path Operations on SKPath.Op

The Path menu's Union, Subtract, Intersect, and Exclude reach a service that returns its first input unchanged. SkiaSharp's `SKPath.Op` implements path booleans and `SKPath.Simplify` normalizes the result; the service is rewritten on them and wired with undo. It runs after SkiaSharp 4 (`D02 T01 §6`) so it is written once against the final API.

**Fidelity:** Nodus main window, Path menu -- docs/captures/nodus/main-window/. Menu wording unchanged; each operation disabled unless two or more path-convertible elements are selected.
**Job:** a designer can combine selected shapes into one path with union, subtract, intersect, or exclude, and undo it. Consumer: the document and the SVG writer.
**Treatment:** convert each selected element to an `SKPath` in document coordinates (rect, ellipse, circle, line, polygon, polyline, path), fold with `SKPath.Op` in z-order (subtract: bottom minus the rest), replace the inputs with one `SvgPath` carrying the bottom element's fill and stroke, as one history entry. Cheaper substitute that fails the checkpoint: grouping the inputs and calling it a union.
**Chrome:** consume the existing Path menu, `SelectionManager`, and the history. Do not add a Pathfinder panel in this section (roadmap, `D02 T06 §5`).

**Requires:** display-session -- driving the Path menu on the canvas needs an interactive desktop

- [ ] Add `SkiaSharp` to `Photon.Nodus.Core` (non-UI, allowed by `standards/nodus.md`) and rewrite `PathOperationsService.BooleanOp`, `BooleanOpMultiple`, and `Simplify` on `SKPath.Op` and `SKPath.Simplify`, removing every placeholder comment. Done when: `grep -c "Placeholder" src/Nodus/Photon.Nodus.Core/Services/PathOperationsService.cs` prints 0.
- [ ] Add `ElementToPathConverter` (each element type to `SKPath`, applying its transform). Done when: tests round-trip each element type's bounds.
- [ ] `PathOperationsTests` assert known results: two overlapping 10 by 10 squares offset by 5 give union area 175, intersect 25, subtract 75, exclude 150 (area measured by flattening). Done when: the four tests pass and fail against the old placeholder.
- [ ] Wire `Union`, `Subtract`, `Intersect`, `Exclude` in the view model as one command each; `Simplify` and `StrokeToPath` stay disabled with a tooltip naming `D02 T06 §2`. Done when: the menu items work on a driven run and the two disabled items show their owner.
- [ ] Commit: `"nodus: real boolean path operations on SKPath.Op with undo"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `PathOperationsTests` reporting the four area results; a driven run unions two overlapping rectangles, saves, reopens, and the file holds one `<path>` whose bounds equal the union's (quote the saved element); Ctrl+Z restores both rectangles. Cheaper substitute that fails: returning the first path, which the area tests catch.

## 6. The Layers Panel on LayerManager

The panel lists `Document.Elements` with an eye icon and a name, and does nothing else. A designer needs to find, reorder, hide, lock, and rename elements without hunting on the canvas. `LayerManager` holds the operations; this section wires them and makes the panel a real list.

**Fidelity:** Nodus main window, layers panel -- docs/captures/nodus/main-window/. Panel position, header, and row height unchanged; rows gain the controls below.
**Job:** a designer can find any element by name, select it, reorder it by drag, hide or lock it, and rename it, each undoable. Consumer: the document, `SelectionManager`, and the canvas.
**Treatment:** a `ListBox` bound to a `LayersPanelViewModel` over the document's elements in z-order (top first), with a visibility toggle, a lock toggle, inline rename on double-click or F2, drag-to-reorder, and two-way selection sync with the canvas; each change is a command. Cheaper substitute that fails the checkpoint: toggles that set `IsVisible` directly, which nothing can undo.
**Chrome:** consume `Photon.UI` icons (`Eye`, `EyeOff`, `LockClosed`, `LockOpen`) through the shared catalog and the theme resources. Do not add a second tree control for groups in this section (nested groups show as one row with the group name; expanding them is `D02 T06 §7`).

**Requires:** display-session -- driving the layers panel needs an interactive desktop

- [ ] Add `LayersPanelViewModel` in `Photon.Nodus.Desktop/ViewModels/` exposing rows (name, visible, locked, selected) in z-order and commands for toggle visibility, toggle lock, rename, and move. Done when: `LayersPanelViewModelTests` cover each command and undo.
- [ ] Route each change through `LayerManager` and a history command (`PropertyChangeCommand` for visibility, lock, and name; `ReorderCommand` for moves). Done when: each action is one history entry with its own description.
- [ ] Replace the panel's `ItemsControl` in `MainWindowView.xaml` with the `ListBox`, the toggles, inline rename, and drag reorder, with tooltips and automation names on the toggles. Done when: every row control is keyboard reachable (Tab into the list, arrows between rows, Space toggles visibility, F2 renames).
- [ ] Selection syncs both ways with `SelectionManager`; locked elements cannot be selected on the canvas; hidden elements are not rendered or hit-tested. Done when: tests cover lock and hide behavior in the hit-tester.
- [ ] An empty document shows "No elements yet. Draw a shape to start." in the panel. Done when: the empty state renders on a new document.
- [ ] Update the Nodus user guide page for the layers panel (`docs/user/nodus/`) in the same commit. Done when: the page describes every control.
- [ ] Commit: `"nodus: a working layers panel with reorder, hide, lock, and rename"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `LayersPanelViewModelTests` reporting; a driven run renames, hides, locks, and drags a row, then undoes all four in order (log lines quoted); capture `docs/captures/nodus/main-window/layers-100.png` committed. Cheaper substitute that fails: the existing read-only list with toggles bound one way.

## 7. Snapping on SnapManager

Precise work needs snapping: to the grid, to guides, and to other objects' edges and centers. `SnapManager` computes candidates and is unused; one of its paths is marked as a simplification. This section wires it into the select and shape tools behind View menu toggles, each a setting.

**Fidelity:** Nodus main window, View menu and canvas -- docs/captures/nodus/main-window/. Snap toggles appear under View, Snap To in the order grid, guides, objects.
**Job:** a designer can drop and drag shapes onto the grid, guides, and other objects' edges and centers, with a visible hint. Consumer: the select, rectangle, ellipse, line, and pen tools.
**Treatment:** during a drag, the active tool asks `SnapManager` for the nearest candidate within a screen-space tolerance (6 px, a setting), moves to it, and draws a thin guide line on the overlay; holding Ctrl while dragging suppresses snapping for that drag. Cheaper substitute that fails the checkpoint: rounding coordinates to the grid, which ignores objects and guides.
**Chrome:** consume the canvas overlay layer and the theme's accent brush for hints. Do not draw hints with a hardcoded color.

**Requires:** display-session -- dragging with snapping on the canvas needs an interactive desktop

- [ ] Finish the simplified path in `SnapManager` (the one marker it carries) and add `SnapManagerTests` for grid, guide, edge, and center candidates and the tolerance. Done when: the tests pass and the marker is gone.
- [ ] Call `SnapManager` from `SelectTool` moves and resizes and from the rectangle, ellipse, line, and pen tools. Done when: each tool's tests include one snapped drag.
- [ ] Add View, Snap To, Grid, Guides, Objects toggles persisted through the settings store (`Nodus.Snap.Grid`, `Nodus.Snap.Guides`, `Nodus.Snap.Objects`, `Nodus.Snap.TolerancePx`) with a log line per change. Done when: toggles survive a restart (settings readback quoted).
- [ ] Draw the snap hint on the canvas overlay using the theme accent. Done when: a capture shows the hint.
- [ ] Commit: `"nodus: snapping to grid, guides, and objects"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `SnapManagerTests` reporting; a driven run drags a rectangle to within 4 px of another's edge and the saved file shows the edges equal; turning Objects off in the View menu and repeating leaves them 4 px apart; `settings.json` shows the toggle (quoted). Cheaper substitute that fails: grid rounding only.

## 8. One Keymap on ShortcutManager

Shortcuts are scattered across `InputBinding`s in XAML and key handling in tools, so no dialog can list them and conflicts go unnoticed. `ShortcutManager` models a keymap with conflict detection and is unused. This section makes it the single source: menu gestures, tool keys, and the shortcuts dialog (`D02 T05 §2`) all read it.

- [ ] Register `ShortcutManager` and load the default keymap from one table in `Photon.Nodus.Desktop/Input/DefaultKeymap.cs` (every command and tool with its gesture, matching today's bindings). Done when: `DefaultKeymapTests` assert no two commands share a gesture.
- [ ] Generate the window's `InputBindings` and the menu items' `InputGestureText` from the keymap instead of XAML literals. Done when: `grep -c "InputGestureText=\"" src/Nodus/Photon.Nodus.Desktop/Views/MainWindowView.xaml` prints 0 and every shortcut still works on a driven run.
- [ ] Tool shortcuts (V, P, R, E, L, T, Z, H, Space for temporary pan) dispatch through the keymap. Done when: the tool tests use the keymap to activate tools.
- [ ] Commit: `"nodus: one keymap drives menus, tools, and gestures"`

**Requires:** display-session -- the driven shortcut run on the canvas needs an interactive desktop
**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `DefaultKeymapTests` reporting zero conflicts; adding a duplicate gesture to the table fails the test; a driven run exercises Ctrl+Z, Ctrl+Shift+Z, V, R, and Space-drag. Cheaper substitute that fails: a second hardcoded list for the dialog.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `docs/dev/nodus/service-triage.md` has a verdict for every service file and every owner ref resolves
- [ ] No Object or Path menu command sets only status text (`grep` quoted)
- [ ] `dotnet test Photon.slnx` exits 0 with every test class this file added reporting
- [ ] `python scripts/todo-graph.py validate` clean
