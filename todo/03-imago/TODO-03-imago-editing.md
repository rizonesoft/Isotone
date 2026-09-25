---
schema_version: 1
id: imago-editing
domain: 03-imago
status: draft
title: "TODO-03 -- Imago Documents, Layers, Tools, and History"
depends_on: []
track: I3
---

# TODO-03 -- Imago Documents, Layers, Tools, and History

> **Goal:** Imago edits real images: documents open in tabs with dirty tracking, every edit is an undo step in the suite history, a layers panel manages layers with blend modes and opacity, and the core tools (move, hand, zoom, marquee and lasso selections, brush and eraser, transform and crop, fill, gradient, and eyedropper) work on tiled layers with a color panel to drive them.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `Imago.UI/Services/DocumentService.cs` is a stand-in: `NewDocumentAsync`, `OpenDocumentAsync`, `SaveDocumentAsync`, and `ExportAsync` log a line, `await Task.Delay(10)` (four such awaits), and return true without touching a document. `MainWindowViewModel` binds 39 commands; the layer (new, duplicate, delete, merge down, flatten), image (size, canvas size, rotate, flip), edit (cut, copy, paste), and filter commands only log. The model is further along than the UI: `Imago.Core` has `ImagoDocument`, `Layer` and its subclasses (raster, group, adjustment, text, shape, smart object), `LayerMask`, `VectorMask`, `ClippingMask`, `Selection`, `SelectionTools`, `QuickMask`, and `CommandHistory` with persistence and snapshots, with tests for the document, history, raster layer, and tiles. There is no tool abstraction and no layers panel.
<!-- claim: count "await Task\.Delay\(10\);" src/Imago/src/Imago.UI/Services/DocumentService.cs = 4 -->
<!-- claim: count "\[RelayCommand" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 39 -->
<!-- claim: exists src/Imago/src/Imago.Core/Selections/SelectionTools.cs -->
<!-- claim: absent src/Imago/src/Imago.Core/Tools -->

## Inputs

- [`standards/imago.md`](../../standards/imago.md), [`standards/shared.md`](../../standards/shared.md) -- tiles, hot paths, every edit an undo step, the design contract
- [`docs/legacy/imago-roadmap.md`](../../docs/legacy/imago-roadmap.md) -- phases 3 (document model) and 4 (tool system), the source of this file
- -> XREF: D01 T02 §4 -- the suite undo history §2 wires Imago onto
- -> XREF: D03 T02 §2 -- the viewport every tool draws into
- -> XREF: D03 T04 §6 -- the recovery that restores documents into §2's history
- -> XREF: D03 T05 §1 -- the filter pipeline that commits through §2 and respects §5's selections

## Outcome

- File, New opens a dialog (size presets, resolution, bit depth, background); documents open in tabs with `name*` while dirty and a prompt before closing a dirty one.
- Every edit (paint stroke, layer change, transform, fill) is one entry in the suite `UndoHistory`, with a History panel listing them.
- The layers panel lists layers with thumbnails and adds, deletes, duplicates, reorders, renames, hides, locks, merges, and flattens, with blend mode and opacity controls; each is undoable.
- A tool abstraction drives move, hand, zoom, rectangular and elliptical marquee, lasso, brush, eraser, transform, crop, fill, gradient, and eyedropper, each with its options bar, cursor, and shortcut.
- A color panel holds foreground and background colors with a picker, hex entry, and swap.

**Adjacency:** list=applicable @ D03 T03 §3; document=not-applicable (printing is a roadmap item, D03 T07 §9); settings=applicable; reporting=applicable; notifications=applicable; permissions=not-applicable (file refusals are TODO-04's); audit=applicable @ D03 T03 §2; exchange=not-applicable (formats are TODO-04's); reverse=applicable @ D03 T03 §2

**Adjacency rationale:** The layers panel is the browsable list; tool options persist as settings; document info and the long-operation progress live in the status strip that §1 builds; the History panel is both audit and reverse.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On                   | Status |
| :---: | :-----: | ---------------------------------------------------- | ---------------------------- | :----: |
|   1   |   §1    | Documents in tabs with dirty tracking                | D03 T01 §5, D03 T02 §2       |  [ ]   |
|   2   |   §2    | Every edit in the suite history                      | §1, D01 T02 §4               |  [ ]   |
|   3   |   §3    | The layers panel                                     | §2, D03 T02 §4               |  [ ]   |
|   4   |   §4    | The tool system: move, hand, and zoom                | §1                           |  [ ]   |
|   5   |   §5    | Selection tools                                      | §4, §2                       |  [ ]   |
|   6   |   §6    | Brush and eraser                                     | §4, §2                       |  [ ]   |
|   7   |   §7    | Transform, crop, image size, and canvas size         | §5                           |  [ ]   |
|   8   |   §8    | Fill, gradient, eyedropper, and the color panel      | §4, §2                       |  [ ]   |

---

## 1. Documents in Tabs with Dirty Tracking

`DocumentService` pretends. This section makes documents real: an `ImagoDocument` per tab, created from the New dialog or opened by a codec (the codecs arrive in `D03 T04`; until then New is the only source), with dirty tracking and a close prompt. -> SOURCE: legacy-imago-3.1

**Fidelity:** Imago main window with document tabs -- docs/captures/imago/main-window/; the New dialog is new build, no baseline, captured to docs/captures/imago/new-document/.
**Job:** a user can create documents, switch between them in tabs, and never lose unsaved work by closing. Consumer: every tool and panel, which act on the active document.
**Treatment:** AvalonDock document tabs; File, New dialog with presets (screen sizes, print sizes at 300 ppi, square), width and height with units (px, in, cm, mm), resolution, 8 or 16 bit, background (white, transparent, background color); tab header `name*` when dirty; closing a dirty tab or exiting prompts Save, Don't Save, Cancel naming each dirty document; the status strip shows size, bit depth, and zoom. Cheaper substitute that fails the checkpoint: one document at a time.
**Chrome:** consume AvalonDock with the theme, the settings store (last New values), and `DialogService`.

**Requires:** display-session -- driving tabs and the New dialog needs an interactive desktop

- [ ] Replace `DocumentService`'s stand-ins with a real `DocumentManager` owning open `ImagoDocument`s, the active document, and per-document DI scopes. Done when: `grep -c "Task.Delay" src/Imago/Photon.Imago.Desktop/Services/DocumentService.cs` prints 0 (or the file is gone) and `DocumentManagerTests` cover open, activate, and close.
- [ ] New Document dialog and view model with presets from one table, remembering the last values in settings. Done when: `NewDocumentViewModelTests` cover unit conversion and validation (width and height 1 to 30,000 px).
- [ ] Tabs with dirty markers and the close and exit prompts. Done when: a driven close of a dirty tab prompts and Cancel keeps it.
- [ ] Status strip readouts (dimensions, bit depth, zoom, memory). Done when: they update when switching tabs.
- [ ] Commit: `"imago: real documents in tabs with dirty tracking"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `DocumentManagerTests` and `NewDocumentViewModelTests` reporting; a driven run creates two documents, edits one, and closing it prompts (capture); `grep -c "Task.Delay"` on the service prints 0. Cheaper substitute that fails: a single-document window.

## 2. Every Edit in the Suite History

Imago's `CommandHistory` moves onto the suite `UndoHistory` in `D01 T02 §4`; this section makes every Imago edit go through it and shows it. Raster edits record tile snapshots (only the tiles a stroke touched), so undo is exact and memory stays bounded. -> SOURCE: legacy-imago-1.4

**Fidelity:** History panel -- new build, no baseline; captured to docs/captures/imago/history/.
**Job:** a user can undo and redo any edit and jump back to any step in the History panel. Consumer: every editing command and tool.
**Treatment:** `TileSnapshotCommand` records before-tiles for the tiles an edit touched; Edit, Undo and Redo (Ctrl+Z, Ctrl+Shift+Z, Ctrl+Alt+Z steps back); a History panel lists steps with names ("Brush Stroke", "New Layer") and clicking a step reverts to it; the history limit is the setting `Imago.History.Limit` (default 100). Cheaper substitute that fails the checkpoint: full-document snapshots per step.
**Chrome:** consume `Photon.Core` `UndoHistory` and the theme. Do not keep a second history type.

**Requires:** display-session -- the History panel needs an interactive desktop

- [ ] Add `TileSnapshotCommand` capturing touched tiles before an edit and restoring them on undo. Done when: a test paints across four tiles, undoes, and asserts byte-identical tiles and that only four were stored.
- [ ] Wire Undo, Redo, and step-back commands and the per-document history. Done when: `ImagoHistoryTests` cover each.
- [ ] Add the History panel. Done when: clicking an earlier step reverts the canvas (driven, captured).
- [ ] Log one Information line per executed command. Done when: a test logger asserts it.
- [ ] Commit: `"imago: every edit is a step in the suite history"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the snapshot and history tests reporting; a driven sequence of three edits undone to the start leaves a document identical to the new one (pixel hash quoted). Cheaper substitute that fails: whole-document snapshots, which the four-tile storage assertion catches.

## 3. The Layers Panel

Layers are the core of raster editing, and the model supports them fully; nothing shows them. The panel lists layers top-first with thumbnails and exposes every layer command, each an undo step. -> SOURCE: legacy-imago-3.2-3.3

**Fidelity:** Layers panel -- new build, no baseline; captured to docs/captures/imago/layers/.
**Job:** a user can create, find, reorder, hide, lock, rename, blend, merge, and flatten layers. Consumer: the document and the render graph.
**Treatment:** a list with 40 px thumbnails (rendered from mip tiles, updated after edits), visibility and lock toggles, inline rename, drag reorder, a blend-mode combo and opacity slider for the selected layer, and buttons for new, duplicate, delete, and group; Layer menu commands (new, duplicate, delete, merge down, flatten) wired to the same commands. Cheaper substitute that fails the checkpoint: a list without thumbnails or blend controls.
**Chrome:** consume the shared icon catalog, the theme, and the render graph. Do not build a second list control style.

**Requires:** display-session -- driving the layers panel needs an interactive desktop

- [ ] `LayersPanelViewModel` with commands for every layer operation, each an undoable command. Done when: `LayersPanelViewModelTests` cover each and its undo.
- [ ] The panel view with thumbnails, toggles, rename, drag reorder, blend mode, and opacity (keyboard reachable, automation names). Done when: a driven pass exercises each.
- [ ] Wire the Layer menu commands (removing their log-only bodies). Done when: `grep -n "_logger.Information(\"Opening" src/Imago/Photon.Imago.Desktop/ViewModels/MainWindowViewModel.cs` shows no layer command.
- [ ] Commit: `"imago: a layers panel with thumbnails, blend modes, and opacity"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `LayersPanelViewModelTests` reporting; a driven run adds three layers, sets one to Multiply at 50 percent, merges down, and undoes each step (log lines quoted, capture committed). Cheaper substitute that fails: layer commands that log only.

## 4. The Tool System: Move, Hand, and Zoom

Imago has no tool abstraction. Every later tool needs one: activation by rail click or shortcut, a cursor, an options bar, pointer handling in document coordinates with pressure where available, and an overlay. The first three tools prove it. -> SOURCE: legacy-imago-4.1

**Fidelity:** Imago tool rail and options bar -- docs/captures/imago/main-window/.
**Job:** a user can pick a tool, see its options, and use it on the canvas. Consumer: the canvas input pipeline.
**Treatment:** `ImagoToolBase` in `Photon.Imago.Core/Tools/` with pointer events in document coordinates (including `StylusPoint` pressure), a cursor, an options view model, and an overlay; a `ToolManager` with keyboard switching (V move, H hand, Z zoom, and Space for temporary hand); options persisted per tool in settings. Cheaper substitute that fails the checkpoint: tool logic in the canvas code-behind.
**Chrome:** consume the keymap pattern Nodus uses (a keymap table the shortcuts dialog reads) and the theme.

**Requires:** display-session -- using tools on the canvas needs an interactive desktop

- [ ] Add `ImagoToolBase`, `ImagoToolManager`, and the options-bar host. Done when: `ToolManagerTests` cover activation, temporary switching, and options persistence.
- [ ] Move (moves the active layer's pixels or selection, one undo step per drag), Hand, and Zoom (click in, Alt-click out, drag to zoom a rectangle). Done when: each has tests and a driven run.
- [ ] A keymap table for Imago commands and tools, feeding menus and the future shortcuts dialog. Done when: `ImagoKeymapTests` assert no conflicts.
- [ ] Commit: `"imago: a tool system with move, hand, and zoom"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the tool tests reporting; a driven move of a layer by 10 px and undo restores it (pixel hash quoted). Cheaper substitute that fails: code-behind handlers per tool.

## 5. Selection Tools

`Selection`, `SelectionTools`, and `QuickMask` exist in the model; no tool makes a selection. -> SOURCE: legacy-imago-4.2

**Fidelity:** Imago canvas with marching ants -- docs/captures/imago/main-window/.
**Job:** a user can select regions by rectangle, ellipse, or freehand lasso, add, subtract, and intersect selections, feather them, and have edits respect them. Consumer: every painting, fill, filter, and transform command.
**Treatment:** rectangular and elliptical marquee (Shift square, Alt from center), lasso and polygonal lasso; Shift adds, Alt subtracts, Shift+Alt intersects; Select, All, Deselect, Inverse, Feather; marching ants drawn on the overlay; the selection is an 8-bit mask in tiles. Cheaper substitute that fails the checkpoint: selections as rectangles only.
**Chrome:** consume `Selection` in `Photon.Imago.Core` and the overlay layer.

**Requires:** display-session -- drawing selections on the canvas needs an interactive desktop

- [ ] Marquee and lasso tools producing `Selection` masks with modifiers. Done when: tests assert mask coverage for each shape and each combine mode.
- [ ] Select menu commands and feather. Done when: tests cover inverse and a 4 px feather profile.
- [ ] Marching ants overlay. Done when: a capture shows it at 100 and 400 percent.
- [ ] Commit: `"imago: marquee and lasso selections with combine modes"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the selection tests reporting; a driven fill inside an elliptical selection leaves pixels outside it unchanged (hash of an outside region quoted). Cheaper substitute that fails: rectangle-only selection.

## 6. Brush and Eraser

Painting is the first thing a raster editor is judged on: a round brush with size, hardness, opacity, and flow, spacing that stays smooth at speed, pressure from a pen, and an eraser. -> SOURCE: legacy-imago-4.3-4.4

**Fidelity:** Imago canvas and brush options bar -- docs/captures/imago/main-window/.
**Job:** a user can paint and erase smooth strokes with a mouse or a pen. Consumer: the active layer's tiles.
**Treatment:** dabs stamped along a spline-interpolated path at a spacing percentage, each dab a precomputed hardness falloff, blended into tiles with opacity and flow, pressure mapped to size and opacity when a stylus reports it; `[` and `]` resize; the eraser writes alpha (or background color on a locked-transparency layer); one undo step per stroke. Cheaper substitute that fails the checkpoint: drawing WPF line segments.
**Chrome:** consume the tool system, `TileSnapshotCommand`, and the color panel.

**Requires:** display-session -- painting on the canvas needs an interactive desktop

- [ ] `BrushEngine` in `Photon.Imago.Core/Painting/` with dab generation, spacing, and blending, allocation-free per dab. Done when: tests assert a straight stroke's coverage profile and a benchmark shows 0 B per dab.
- [ ] Brush and eraser tools with options (size 1 to 5,000 px, hardness, opacity, flow, spacing, pressure toggles) persisted in settings. Done when: options survive a restart.
- [ ] Commit: `"imago: a smooth brush and eraser with pen pressure"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the brush tests reporting; a recorded stroke fixture replayed through the engine matches its golden within 1/255 (test quoted); a driven stroke with a pen shows width variation (capture). Cheaper substitute that fails: WPF polylines.

## 7. Transform, Crop, Image Size, and Canvas Size

Resizing, rotating, and cropping are daily operations; the Image menu's size, rotate, and flip commands only log. -> SOURCE: legacy-imago-4.5-3.4

**Fidelity:** Transform handles and the Image Size and Canvas Size dialogs -- docs/captures/imago/main-window/ for handles; the dialogs are new build, no baseline, captured to docs/captures/imago/image-size/ and docs/captures/imago/canvas-size/.
**Job:** a user can free-transform a layer or selection, crop, resample the image, change the canvas, and rotate or flip the whole image. Consumer: the document.
**Treatment:** Edit, Free Transform (Ctrl+T) with scale, rotate, and move handles, Enter commits one undo step with bicubic resampling; crop tool with a rule-of-thirds overlay and delete or hide cropped pixels; Image Size (resample methods: nearest, bilinear, bicubic, Lanczos) and Canvas Size (anchor grid) dialogs; Image, Rotate 90, 180, and Flip wired. Cheaper substitute that fails the checkpoint: transforms that preview with WPF render transforms and never resample pixels.
**Chrome:** consume the tool system, the history, and `DialogService`.

**Requires:** display-session -- transform handles and dialogs need an interactive desktop

- [ ] Resampling kernels with tests against goldens from libvips (version recorded). Done when: each method passes within 2/255.
- [ ] Free transform and crop tools. Done when: a driven transform and crop each undo in one step.
- [ ] Image Size, Canvas Size, rotate, and flip commands. Done when: `grep` finds no log-only body for them.
- [ ] Commit: `"imago: free transform, crop, image size, canvas size, rotate, and flip"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the resampling fidelity tests reporting per method; rotating a known image 90 degrees four times returns identical pixels (hash quoted). Cheaper substitute that fails: render-transform previews.

## 8. Fill, Gradient, Eyedropper, and the Color Panel

The remaining basic tools and the color panel every painting tool reads. -> SOURCE: legacy-imago-4.3

**Fidelity:** Color panel -- new build, no baseline; captured to docs/captures/imago/color/.
**Job:** a user can pick colors, fill regions, draw gradients, and sample colors from the image. Consumer: brush, fill, and gradient tools.
**Treatment:** a color panel with foreground and background swatches, swap (X) and reset (D), an HSV square and hue strip, RGB and hex fields; paint bucket with tolerance and contiguous options; linear and radial gradient tool from foreground to background with dithering; eyedropper with sample size (point, 3 by 3, 5 by 5) and current layer or composite. Cheaper substitute that fails the checkpoint: the Windows color dialog.
**Chrome:** consume the theme; the picker is built in Imago now and moves to `Photon.UI` when Nodus's appearance work (`D02 T06 §5`) needs one, through `add-todo`.

**Requires:** display-session -- the color panel and tools need an interactive desktop

- [ ] Color panel and view model with HSV and hex conversions tested. Done when: `ColorPanelViewModelTests` round-trip hex and HSV.
- [ ] Paint bucket, gradient, and eyedropper tools, each fill an undo step. Done when: tests assert a flood fill's region on a fixture and gradient endpoints.
- [ ] Commit: `"imago: fill, gradient, eyedropper, and a color panel"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the color and fill tests reporting; a driven eyedrop of a known pixel shows its hex in the panel (capture). Cheaper substitute that fails: the system color dialog.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] No Imago edit command logs without acting (`grep` for log-only bodies, quoted)
- [ ] A driven session of new, paint, select, transform, layer, and undo-all returns the starting pixels
- [ ] `python scripts/todo-graph.py validate` clean
