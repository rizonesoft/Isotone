---
schema_version: 1
id: nodus-editing
domain: 02-nodus
status: draft
title: "TODO-03 -- Editing Correctness: Undo, Clipboard, and the View Model Split"
depends_on: []
track: N3
---

# TODO-03 -- Editing Correctness: Undo, Clipboard, and the View Model Split

> **Goal:** Every edit a Nodus user can make is one undo step, the Edit menu does what it says, the 1,050-line main view model is split by responsibility so each part can be tested, and no menu item in the shipped app is a status-text stub: each one works or is disabled with a tooltip naming the section that will build it.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs` is 1,050 lines in twelve regions (window, status bar, context toolbar, view state, tool state, undo, file, edit, view, object, path, and help commands) with 33 `[ObservableProperty]` fields, and the main window binds 100 commands to it. `SelectTool.OnMouseUp` finishes a resize and a rotation with `// TODO: Add ResizeCommand for undo support` (line 315) and `// TODO: Add RotateCommand for undo support` (line 321): the transforms are applied live during the drag and nothing is recorded, so Ctrl+Z skips them. `ResizeCommand` and `RotateCommand` exist and are tested. `PropertyChangeCommand` exists and nothing uses it, not even a test: the context toolbar's `DocumentWidth`/`DocumentHeight` and the element geometry fields write straight to the model. `Cut`, `Copy`, `Paste`, `Duplicate`, `Delete`, `SelectAll`, `Preferences`, and `Close` only set `StatusText`; `Documentation`, `KeyboardShortcuts`, and `About` end in `// TODO` comments (lines 973, 980, 1046).
<!-- claim: lines src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 1050 -->
<!-- claim: count "// TODO: Add (Resize|Rotate)Command for undo support" src/Nodus/Bezier.Core/Tools/SelectTool.cs = 2 -->
<!-- claim: count "// TODO: (Open docs URL|Show keyboard shortcuts dialog|Show about dialog)" src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 3 -->
<!-- claim: count "StatusText = \"(Cut|Copy|Paste|Duplicate|Delete|Select All)\";" src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 6 -->
<!-- claim: count "PropertyChangeCommand" src/Nodus/Bezier.Desktop/**/*.cs = 0 -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- every edit is an undo step; view models over 400 lines split; logic out of code-behind
- [`standards/nodus.md`](../../standards/nodus.md) -- a drag records one command on mouse-up with start and end state
- `src/Nodus/Photon.Nodus.Core/Commands/` (after `D02 T01 §1`) -- the commands §1 and §4 record
- `docs/captures/nodus/main-window/` -- the baseline the split must not change
- -> XREF: D02 T02 §4 -- the arrange and align commands §5's sweep accounts for
- -> XREF: D01 T02 §4 -- the suite history that absorbs this file's commands once Imago needs it
- -> XREF: D02 T04 §1 -- the dirty prompt and atomic save that §5's Close command uses

## Outcome

- Resizing or rotating with the select tool records one `ResizeCommand` or `RotateCommand`, and Ctrl+Z restores the exact pre-drag geometry.
- `MainWindowViewModel` is a shell under 400 lines composing `DocumentViewModel`, `ToolsViewModel`, `ViewStateViewModel`, and command groups, each with tests.
- Cut, Copy, Paste, Duplicate, Delete, and Select All work on the selection through the Windows clipboard (SVG fragment plus an internal format) with undo.
- Every property edit in the context toolbar and properties panel is one undo step, and consecutive nudges of one field merge into one.
- A test enumerates every bound menu command and asserts it is either wired or disabled with a tooltip naming a resolvable section.

**Adjacency:** list=not-applicable (lists are the layers panel's, D02 T02 §6); document=not-applicable (no printed output); settings=not-applicable (no new settings); reporting=not-applicable (no summaries); notifications=not-applicable (no long operations); permissions=not-applicable (the clipboard can be locked by another process; §3 refuses with a message, which is its own item); audit=applicable; exchange=applicable; reverse=applicable @ D02 T03 §1

**Adjacency rationale:** This file is the reverse adjacency for Nodus: every edit gains an undo. The clipboard is an exchange surface (SVG on the Windows clipboard), and each recorded command logs its line.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On                                                   | Status |
| :---: | :-----: | ---------------------------------------------------- | ------------------------------------------------------------ | :----: |
|   1   |   §1    | Undo for resize and rotate                           | D02 T01 §2                                                   |  [ ]   |
|   2   |   §2    | Split the main window view model                     | D02 T01 §2                                                   |  [ ]   |
|   3   |   §3    | Clipboard and the Edit menu                          | §2, D02 T02 §3                                               |  [ ]   |
|   4   |   §4    | Property edits are undo steps                        | §2                                                           |  [ ]   |
|   5   |   §5    | Every menu command works or names its owner          | §3, §4, D02 T02 §4, D02 T02 §5, D02 T02 §6, D02 T02 §8, D02 T04 §1, D02 T04 §4, D02 T04 §5 |  [ ]   |

---

## 1. Undo for Resize and Rotate

`SelectTool` applies resize and rotation transforms live while dragging and records nothing when the drag ends, so undo silently skips the most common edits a user makes. The commands exist; the tool must capture each element's state when the drag starts and record one command on mouse-up.

- [ ] On resize and rotate drag start, `SelectTool` captures each selected element's pre-drag geometry (bounds and transform matrix) in `_originalElementBounds` or a new per-element snapshot. Done when: the snapshot is taken in `OnMouseDown` for both modes.
- [ ] On mouse-up in `SelectMode.Resizing`, record one `ResizeCommand` covering every selected element (a `CompositeCommand` for more than one) through the history's "already applied" path (record without re-executing). Done when: the `// TODO: Add ResizeCommand` line is gone.
- [ ] The same for `SelectMode.Rotating` with `RotateCommand`. Done when: the `// TODO: Add RotateCommand` line is gone.
- [ ] A drag that ends where it started (no net change) records nothing. Done when: a test asserts the history is unchanged after a zero-distance drag.
- [ ] Add `SelectToolUndoTests`: resize one element, undo, assert bounds equal the originals exactly; rotate two elements, undo, assert both matrices equal the originals; redo reapplies. Done when: the tests pass and fail with the recording removed.
- [ ] Commit: `"nodus: record resize and rotate drags as undo steps"`

**Requires:** display-session -- the driven drag-then-undo run needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `SelectToolUndoTests` reporting; `grep -c "TODO: Add" src/Nodus/Photon.Nodus.Core/Tools/SelectTool.cs` prints 0; a driven run resizes and rotates a rectangle, presses Ctrl+Z twice, and the saved file equals the pre-edit file (quote the diff: empty). Cheaper substitute that fails: recording a command that re-executes the transform on redo from the current state, which the exact-bounds assertion catches after rounding drift.

## 2. Split the Main Window View Model

At 1,050 lines the main view model owns window state, the status bar, the context toolbar, tools, undo, and every menu command, so no part can be tested without constructing all of it, and every later section edits the same file. `standards/shared.md` sets 400 lines as the point to split by responsibility. This section moves code without changing behavior.

**Fidelity:** Nodus main window -- docs/captures/nodus/main-window/. Pixel-identical before and after; the split is invisible to a user.
**Job:** a developer can test document, tool, and view behavior in isolation. Consumer: the main window's bindings.
**Treatment:** `MainWindowViewModel` keeps window title and composition and exposes child view models as properties; bindings change from `{Binding ZoomIn}` to `{Binding View.ZoomInCommand}` style paths. Cheaper substitute that fails the checkpoint: partial-class files of the same type, which keep one untestable object.
**Chrome:** consume the existing XAML and styles. Do not restyle anything in this section.

**Requires:** display-session -- proving the split window is unchanged needs an interactive desktop capture

- [ ] Extract `DocumentViewModel` (the document, file path, dirty state, document info, file commands) to `Photon.Nodus.Desktop/ViewModels/DocumentViewModel.cs`. Done when: its tests construct it with fake importer and exporter services.
- [ ] Extract `ToolsViewModel` (active tool, tool switching, tool options). Done when: its tests switch tools without a window.
- [ ] Extract `ViewStateViewModel` (zoom, panels, grid and ruler toggles, memory and GPU indicators, status bar text). Done when: its tests cover zoom steps and fit.
- [ ] Extract `EditCommands`, `ObjectCommands`, `PathCommands`, and `HelpCommands` groups (plain classes with `[RelayCommand]` members, each taking the services it needs). Done when: each group has a test class.
- [ ] Register the children in `AddNodusServices` and inject them into `MainWindowViewModel`. Done when: `MainWindowViewModel.cs` is under 400 lines (quote `wc -l`).
- [ ] Rebind `MainWindowView.xaml` to the new paths, and fail loudly on a broken binding in Debug (`PresentationTraceSources` binding errors logged at Warning). Done when: a Debug run of every menu produces 0 binding errors in the log.
- [ ] Commit: `"nodus: split the main window view model by responsibility"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the four new view-model test classes reporting; `wc -l src/Nodus/Photon.Nodus.Desktop/ViewModels/MainWindowViewModel.cs` is under 400; a driven run of every menu item logs 0 binding errors; a new capture `docs/captures/nodus/main-window/split-100.png` is identical to the pre-split capture taken in the same session. Cheaper substitute that fails: partial classes.

## 3. Clipboard and the Edit Menu

The Edit menu's clipboard items set status text. A vector editor's clipboard must round-trip within Nodus exactly and exchange with other apps as SVG: Inkscape and browsers read `image/svg+xml`, so Nodus writes both an internal format (exact) and SVG text (portable), and reads either.

**Fidelity:** Nodus main window, Edit menu -- docs/captures/nodus/main-window/. Menu order and shortcuts unchanged (Ctrl+X, Ctrl+C, Ctrl+V, Ctrl+D, Delete, Ctrl+A).
**Job:** a designer can cut, copy, paste, duplicate, delete, and select all, within Nodus and to and from other SVG-aware apps, and undo each. Consumer: the document, the Windows clipboard, and other applications.
**Treatment:** copy writes the selection as an SVG fragment (the `SvgExporter` path, one `<svg>` with the selected elements) under the clipboard formats `image/svg+xml` and `Nodus.Elements` (the internal serialization); paste prefers `Nodus.Elements`, falls back to SVG through `SvgImporter`, and places the result at the original position (or offset by 10 units if an identical element is under it); duplicate offsets by 10 units; each change is one undo step. Cheaper substitute that fails the checkpoint: an in-process list that other apps cannot see.
**Chrome:** consume `SvgExporter`, `SvgImporter`, `SelectionManager`, and the history. Do not add a second serializer.

**Requires:** display-session -- the clipboard round trip with another application needs an interactive desktop

- [ ] Add `ClipboardService` in `Photon.Nodus.Desktop/Services/` (write both formats, read either, retry once on `CLIPBRD_E_CANT_OPEN`, then refuse with "The clipboard is in use by another application. Try again."). Done when: `ClipboardServiceTests` cover both formats through a fake clipboard, and the busy case.
- [ ] Wire `Cut` (copy then delete as one undo step), `Copy`, `Paste`, `Duplicate`, and `Delete` (a `DeleteElementCommand` per element in one composite). Done when: each is one history entry with its own description.
- [ ] Wire `SelectAll` through `SelectionManager` (locked and hidden elements excluded). Done when: a test with one locked element asserts it is not selected.
- [ ] Commands that need a selection are disabled without one; Paste is disabled when the clipboard has neither format. Done when: the `CanExecute` tests pass.
- [ ] Update the Nodus user guide's editing page in `docs/user/nodus/`. Done when: the page lists each command and the SVG exchange.
- [ ] Commit: `"nodus: a real clipboard with SVG exchange and undo"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `ClipboardServiceTests` reporting; a driven run copies two shapes from Nodus and pastes into Inkscape (version quoted) and they appear, and copies a shape from Inkscape and pastes into Nodus and it appears with its fill; Ctrl+Z after paste removes exactly the pasted elements (log lines quoted). Cheaper substitute that fails: the internal format only, which the Inkscape step catches.

## 4. Property Edits Are Undo Steps

Typing a width into the context toolbar or dragging a number box writes straight to the model; `PropertyChangeCommand` exists for this and is used nowhere. Every property edit becomes a command, and consecutive edits of one field within a short window merge into one step so a scrubbed number box is not fifty undo entries.

- [ ] `PropertyChangeCommand` records element, property name, old value, and new value, and supports merging with a following command on the same element and property within 1 second (`TryMerge`). Done when: `PropertyChangeCommandTests` cover execute, undo, redo, and merge (also the first test the class has ever had).
- [ ] Route every setter in the context toolbar and properties panel that writes the model (document width and height, element X, Y, width, height, rotation, opacity, fill, stroke, stroke width, corner radius, name) through the command. Done when: `grep -n "Document.Width = \|Document.Height = " src/Nodus/Photon.Nodus.Desktop/ViewModels` prints nothing outside the command path.
- [ ] Each committed property command logs one Information line (`Set {Property} on {Element} from {Old} to {New}`); merged edits log once. Done when: a test logger asserts one line for a merged scrub.
- [ ] Commit: `"nodus: every property edit is one undo step"`

**Requires:** display-session -- the driven scrub-then-undo run on the number box needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `PropertyChangeCommandTests` reporting; a driven run changes a rectangle's width by scrubbing the number box, changes its fill, then Ctrl+Z twice restores width and fill exactly (log lines quoted, two entries not dozens). Cheaper substitute that fails: undo snapshots of the whole document per keystroke, which the merge assertion catches.

## 5. Every Menu Command Works or Names Its Owner

The surface-completeness rule in `todo/README.md` says every control on a shipped surface is working or deferred to a named section; a control disabled with a reason that names no section is missing. Nodus 0.1.0 ships its whole menu bar, so this section accounts for every item once the wiring sections have landed.

**Fidelity:** Nodus main window, every menu -- docs/captures/nodus/main-window/. Menu structure and wording unchanged except for items this section removes with a reason.
**Job:** a user never clicks a menu item that silently does nothing. Consumer: the user; the audit test is the developer's consumer.
**Treatment:** a `MenuAudit` test enumerates every `MenuItem` in the main window (loaded in an STA test) and asserts its command is either enabled-capable with a non-stub body or disabled with a tooltip matching `Planned: D\d\d T\d\d §\d+`, and that each named ref resolves. Cheaper substitute that fails the checkpoint: hiding unfinished items, which silently shrinks the product.
**Chrome:** consume the existing menus and the shared tooltip style. Do not add a "coming soon" dialog.

**Requires:** display-session -- the driven pass over every menu item needs an interactive desktop

- [ ] Add a `PlannedFeature` helper that disables a command and sets the menu item's tooltip to `Planned: <ref>` from one table in `Photon.Nodus.Desktop/Input/PlannedCommands.cs`. Done when: the table is the only place a planned ref is written.
- [ ] Classify every remaining stub: `Preferences` (planned `D02 T06 §13`), `Simplify` and `StrokeToPath` (planned `D02 T06 §2`), `TextToPath` (planned `D02 T06 §3`), `ExportXaml` (planned `D02 T06 §14`), `CheckUpdates` (planned `D05 T01 §4`), and any other the audit finds. Done when: `grep -n "StatusText = \"" src/Nodus/Photon.Nodus.Desktop/ViewModels` finds no command whose whole body is a status assignment.
- [ ] Implement `Close` (closes the document with the dirty prompt from `D02 T04 §1`, leaving an empty window) now rather than deferring it. Done when: File, Close on a dirty document prompts and on a clean one clears the canvas.
- [ ] Add `MenuAuditTests` as described in Treatment. The test asserts the tooltip shape; resolving each ref against `todo/` is the checkpoint's job, through the script. Done when: the test fails if any item has a stub body and no planned tooltip.
- [ ] Commit: `"nodus: every menu command works or names the section that builds it"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `MenuAuditTests` reporting; for every ref in `PlannedCommands.cs`, `python scripts/todo-graph.py resolve '<ref>'` exits 0 or 4 (quote the loop's output); a driven pass clicks every enabled menu item on a sample document and the log has 0 `[ERR]` lines. Cheaper substitute that fails: removing the unfinished items from the menu.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every test class this file added reporting
- [ ] A driven session of draw, resize, rotate, recolor, copy, paste, align, and undo of each leaves the document equal to its starting file
- [ ] `python scripts/todo-graph.py validate` clean
