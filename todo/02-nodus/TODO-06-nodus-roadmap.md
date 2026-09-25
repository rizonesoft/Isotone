---
schema_version: 1
id: nodus-roadmap
domain: 02-nodus
status: draft
title: "TODO-06 -- Nodus Roadmap after 0.1.0"
depends_on: []
track: N6
---

# TODO-06 -- Nodus Roadmap after 0.1.0

> **Goal:** The long tail of the legacy Bezier roadmap, mined into buildable sections at feature grain: the shape, path, text, masking, appearance, artboard, document, precision, library, command, preference, format, freehand, performance, accessibility, color, print, scripting, and onboarding work that takes Nodus from a first release to a daily-driver vector editor. Each section is born complete, and each is expected to be split further by `groom-plan` before it runs.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The legacy roadmap (`docs/legacy/nodus-roadmap.md`, 3,199 lines, phases 0 to 25) was mined on 2026-09-26. Its check marks are unreliable (see `docs/legacy/README.md`): services exist for several of these features, but none is reachable from the app, and the triage in `D02 T02 §1` defers them to sections here. Phases 16 to 25 (collaboration, cross-platform, 3D, enterprise, industry suites, gamification, audio and video, sustainability, AR and VR) are deliberately not converted. Every section below names its legacy source with a `-> SOURCE:` line.
<!-- claim: lines docs/legacy/nodus-roadmap.md = 3199 -->
<!-- claim: exists src/Nodus/Bezier.Core/Services/SymbolLibraryService.cs -->
<!-- claim: exists src/Nodus/Bezier.Core/Services/CommandPaletteService.cs -->

## Inputs

- [`docs/legacy/nodus-roadmap.md`](../../docs/legacy/nodus-roadmap.md) -- the source of every section here; read the named legacy phase before grooming a section
- [`standards/nodus.md`](../../standards/nodus.md) -- the document model, tool, and SVG rules every section builds to
- `docs/dev/nodus/service-triage.md` (written by `D02 T02 §1`) -- the deferred services §11, §12, and §14 wire
- -> XREF: D02 T02 §1 -- the triage that hands the deferred services to §11, §12, and §14

## Outcome

- Every section below ships with its surface, its commands with undo, its settings, its log lines, its user-guide page, and its tests, like the 0.1.0 sections before it.
- No deferred service from the triage remains unwired when this file closes.

**Adjacency:** list=applicable @ D02 T06 §11; document=applicable @ D02 T06 §19; settings=applicable @ D02 T06 §13; reporting=applicable; notifications=applicable; permissions=not-applicable (file refusals are owned by the save and export sections in D02 T04); audit=applicable; exchange=applicable @ D02 T06 §14; reverse=applicable

**Adjacency rationale:** The asset library is the browsable list; print is the carried document; the Preferences dialog is the settings surface; measurement and document info are reporting; long operations on large documents notify through the status strip; every edit in every section is a logged, undoable command.

## Implementation Order

| Order | Section | Deliverable                                              | Depends On  | Status |
| :---: | :-----: | -------------------------------------------------------- | ----------- | :----: |
|   1   |   §1    | Shape tools: polygon, star, spiral, arc                  | D02 T05 §4  |  [ ]   |
|   2   |   §2    | Path editing: continue, join, break, reverse, simplify   | D02 T05 §4  |  [ ]   |
|   3   |   §3    | Text: area text, text on path, text to path             | D02 T05 §4  |  [ ]   |
|   4   |   §4    | Clipping, masks, and compound paths                      | D02 T05 §4  |  [ ]   |
|   5   |   §5    | Appearance: swatches, multiple fills, conic gradients    | D02 T05 §4  |  [ ]   |
|   6   |   §6    | Artboards: presets, duplicate, arrange, fit              | D02 T05 §4  |  [ ]   |
|   7   |   §7    | Documents in tabs, saved layouts, nested layers          | D02 T05 §4  |  [ ]   |
|   8   |   §8    | The contextual property bar                              | §7          |  [ ]   |
|   9   |   §9    | Transform precision and smart selection                  | D02 T05 §4  |  [ ]   |
|  10   |   §10   | Guides and measurement                                   | D02 T05 §4  |  [ ]   |
|  11   |   §11   | Symbols and the asset library                            | §7          |  [ ]   |
|  12   |   §12   | The command palette and the on-canvas HUD                | D02 T05 §4  |  [ ]   |
|  13   |   §13   | Preferences and shortcut remapping                       | D02 T05 §4  |  [ ]   |
|  14   |   §14   | More formats and the export dialog                       | D02 T05 §4  |  [ ]   |
|  15   |   §15   | Freehand tools: pencil, brush, eraser                    | §2          |  [ ]   |
|  16   |   §16   | Large documents: spatial index, culling, dirty regions   | D02 T05 §4  |  [ ]   |
|  17   |   §17   | Accessibility and localization                           | §13         |  [ ]   |
|  18   |   §18   | Brushes, patterns, and color tools                       | §5, §15     |  [ ]   |
|  19   |   §19   | Print and prepress                                       | §6          |  [ ]   |
|  20   |   §20   | Scripting and plugins                                    | §12         |  [ ]   |
|  21   |   §21   | Onboarding and the navigator                             | §13         |  [ ]   |

---

## 1. Shape Tools: Polygon, Star, Spiral, Arc

Rectangle, ellipse, and line are the only shape tools. Every competitor ships polygon and star tools with on-canvas controls for sides and inner radius; they are the most requested primitives after the basics. -> SOURCE: legacy-nodus-3.2

**Fidelity:** Nodus tool rail and canvas -- docs/captures/nodus/main-window/. New tools join the rail's shape flyout in the order rectangle, ellipse, polygon, star, spiral, arc, line.
**Job:** a designer can draw regular polygons, stars, spirals, and arcs and edit their parameters afterwards. Consumer: the document and the SVG writer.
**Treatment:** each tool draws from the center with Shift constraining rotation to 15 degrees; the context toolbar shows its parameters (sides 3 to 100; star points and inner radius ratio; spiral turns and decay; arc start, sweep, and closed or open); parameters stay editable after creation as `data-nodus-*` attributes that the SVG writer preserves, and the geometry is written as a plain `<path>` or `<polygon>` so other apps read it. Cheaper substitute that fails the checkpoint: shapes that become dumb paths at creation.
**Chrome:** consume `ToolBase`, the keymap, the icon catalog, and the history. Do not add a separate parameters window.

**Requires:** display-session -- drawing with the new tools needs an interactive desktop

- [ ] Add `PolygonTool`, `StarTool`, `SpiralTool`, and `ArcTool` in `Photon.Nodus.Core/Tools/` with geometry in `Photon.Nodus.Core/Geometry/Parametric/`. Done when: geometry tests assert vertex counts and radii for each.
- [ ] Add a `ParametricShape` element (or attributes on `SvgPath`) that the importer and exporter round-trip. Done when: a fidelity fixture per shape round-trips with parameters intact.
- [ ] Context toolbar parameter controls, each edit one undo step. Done when: a driven edit of star points then Ctrl+Z restores the shape.
- [ ] Keymap entries and user-guide pages for the four tools. Done when: the shortcuts dialog lists them.
- [ ] Commit: `"nodus: polygon, star, spiral, and arc tools with editable parameters"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the geometry and fidelity tests reporting; a driven run draws each shape, edits one parameter, saves, reopens in Inkscape (version quoted) and the shapes render there. Cheaper substitute that fails: parameters lost on reopen.

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

## 4. Clipping, Masks, and Compound Paths

The model has `SvgClipPath` and `SvgMask`, and the importer does not honor them on import (legacy 1.6 lists both as open); nothing in the UI makes one. -> SOURCE: legacy-nodus-1.6-4.4

**Fidelity:** Nodus canvas and Object menu -- docs/captures/nodus/main-window/.
**Job:** a designer can clip artwork to a shape, apply an opacity mask, and make compound paths with holes. Consumer: the document, the renderer, and the SVG writer.
**Treatment:** Object, Clipping Mask, Make and Release (top object clips the rest); Object, Compound Path, Make and Release (even-odd and nonzero fill rules); opacity masks from the Appearance panel (§5); the importer honors `clip-path`, `mask`, and `marker` references. Cheaper substitute that fails the checkpoint: clipping that the renderer ignores on reopen.
**Chrome:** consume the history, `SkiaRenderer` (`SKCanvas.ClipPath`, save layers for masks).

**Requires:** display-session -- clipping on the canvas needs an interactive desktop

- [ ] Importer support for `clip-path`, `mask`, and `marker`, with fixtures. Done when: the fixtures render against Inkscape goldens within the `D02 T04 §2` tolerance.
- [ ] Make and Release commands for clipping masks and compound paths with undo. Done when: tests cover each and its release.
- [ ] Renderer support for masks via save layers. Done when: the mask fixture passes its golden.
- [ ] Commit: `"nodus: clipping masks, opacity masks, and compound paths"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the clip, mask, and marker fixtures; a driven make-release-undo cycle is logged. Cheaper substitute that fails: grouping instead of clipping.

## 5. Appearance: Swatches, Multiple Fills, Conic Gradients

Designers reuse colors through swatches and stack fills and strokes on one object. Conic and mesh gradients are open in the legacy fills list. -> SOURCE: legacy-nodus-4.2-1.4

**Fidelity:** Appearance and Swatches panels -- new build, no baseline; captured to docs/captures/nodus/appearance/ and docs/captures/nodus/swatches/.
**Job:** a designer can define document swatches, apply them, stack fills and strokes, and use conic gradients. Consumer: the document and the SVG writer.
**Treatment:** a Swatches panel (document swatches written as SVG `<linearGradient>`/`<solidColor>` equivalents in `<defs>` with `id`s, plus global swatches in settings); an Appearance panel listing an element's fills and strokes in paint order with add, remove, reorder, and per-entry opacity (written as stacked duplicate elements in a group marked `data-nodus-appearance` so other apps render it); conic gradient fills rendered with `SKShader.CreateSweepGradient` and exported with a fallback raster pattern. Cheaper substitute that fails the checkpoint: one fill per element.
**Chrome:** consume the shared color picker once `Photon.UI` has one (file one through `add-todo` if Imago has built a picker by then); the theme.

**Requires:** display-session -- the panels need an interactive desktop

- [ ] Swatches panel and model with round trip. Done when: a fixture keeps its swatches after reopen.
- [ ] Appearance panel and stacked paint model with round trip. Done when: a two-fill fixture reopens with both fills.
- [ ] Conic gradient fill with export fallback. Done when: Inkscape renders the exported fallback.
- [ ] Commit: `"nodus: swatches, the appearance stack, and conic gradients"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the appearance model tests reporting; captures committed; round-trip fixtures pass. Cheaper substitute that fails: appearance kept only in memory.

## 6. Artboards: Presets, Duplicate, Arrange, Fit

Artboards exist (`ArtboardManager`); the legacy list leaves presets, duplicate, arrange, and fit-to-artwork open. -> SOURCE: legacy-nodus-4.6

**Fidelity:** Artboards panel and artboard tool -- docs/captures/nodus/main-window/.
**Job:** a designer can create artboards from presets (A4, Letter, social sizes, icon sizes), duplicate them with contents, arrange them in a grid, and fit one to its artwork. Consumer: the document, PDF export (one page per artboard), and raster export.
**Treatment:** preset list from one table; duplicate copies contained elements; Arrange lays out in rows with a spacing setting; Fit to Artwork resizes to the contained bounds; each is one undo step. Cheaper substitute that fails the checkpoint: presets that set the document size only.
**Chrome:** consume `ArtboardManager`, the history, and the export sections.

**Requires:** display-session -- artboard editing needs an interactive desktop

- [ ] Preset table and New Artboard from preset. Done when: tests assert sizes in document units.
- [ ] Duplicate, Arrange, and Fit to Artwork commands with undo. Done when: each has a test.
- [ ] Commit: `"nodus: artboard presets, duplicate, arrange, and fit"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the artboard tests reporting; a two-artboard document exports a two-page PDF with the right page sizes. Cheaper substitute that fails: one artboard per document.

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

## 8. The Contextual Property Bar

The context toolbar shows document size and selection geometry. Competitors show per-tool and per-selection controls: stroke for a path, font for text, corner radius for a rectangle. -> SOURCE: legacy-nodus-2.5

**Fidelity:** Nodus context toolbar -- docs/captures/nodus/main-window/.
**Job:** a designer can change the most-used properties of the current tool or selection without opening a panel. Consumer: the document through property commands.
**Treatment:** a template selector over the active tool and selection type, each template bound to property commands (`D02 T03 §4`) with merge. Cheaper substitute that fails the checkpoint: one static bar for everything.
**Chrome:** consume the property commands and the theme.

**Requires:** display-session -- the bar changes with the selection on the canvas

- [ ] Templates for select (geometry), text (font, size, alignment), path (stroke, fill), rectangle (corner radius), and each drawing tool (its options). Done when: a driven pass shows each template.
- [ ] Commit: `"nodus: a context toolbar that follows the tool and the selection"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with a template-selector test per case; captures per template committed. Cheaper substitute that fails: the static bar.

## 9. Transform Precision and Smart Selection

Precision work needs numeric transforms, reflect and skew, and repeating the last transform; selection needs "select same fill", "select same stroke", and deep select into groups. -> SOURCE: legacy-nodus-3.1

**Fidelity:** Transform dialog -- new build, no baseline; captured to docs/captures/nodus/transform/.
**Job:** a designer can move, scale, rotate, reflect, and skew by exact values, repeat the last transform, and select objects by shared attributes. Consumer: the document.
**Treatment:** Object, Transform, Transform Each (a dialog with move, scale, rotate, skew, reflect, reference point, copy); Object, Transform Again (Ctrl+D after a transform); Select, Same, Fill Color and Stroke Color; Ctrl+click deep-selects inside groups. Cheaper substitute that fails the checkpoint: reflect implemented as scale by -1 around the origin.
**Chrome:** consume `TransformService`, `SelectionManager`, and the history.

**Requires:** display-session -- the dialog and canvas selection need an interactive desktop

- [ ] Transform dialog and `TransformEachCommand`. Done when: tests assert exact matrices for each operation about each reference point.
- [ ] Transform Again and Select Same. Done when: tests cover both.
- [ ] Commit: `"nodus: numeric transforms, transform again, and select same"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the transform tests reporting; the dialog capture is committed. Cheaper substitute that fails: a transform dialog that edits only position.

## 10. Guides and Measurement

Ruler guides and snapping exist; numeric guide entry, guide locking, and a measure tool with distance, angle, and area are open. -> SOURCE: legacy-nodus-3.7-3.8

**Fidelity:** Nodus canvas and guides -- docs/captures/nodus/main-window/.
**Job:** a designer can place guides by value, lock them, and measure distances, angles, and areas. Consumer: snapping and the Info panel.
**Treatment:** double-clicking a guide opens a position box; View, Lock Guides; a Measure tool shows distance and angle live and writes nothing to the document; an Info panel shows selection bounds, path length, and area in the document unit. Cheaper substitute that fails the checkpoint: a measure tool that draws a line element.
**Chrome:** consume `SnapManager`, the overlay layer, and the unit settings.

**Requires:** display-session -- measuring on the canvas needs an interactive desktop

- [ ] Numeric guides and guide lock persisted in the document. Done when: guides survive save and reopen.
- [ ] Measure tool and Info panel with area via flattened paths. Done when: a 10 by 10 square reports area 100 and perimeter 40.
- [ ] Commit: `"nodus: numeric guides, guide locking, measurement, and the Info panel"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the measurement tests reporting; a driven measurement is captured. Cheaper substitute that fails: area from bounding boxes.

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

## 15. Freehand Tools: Pencil, Brush, Eraser

Sketching needs a pencil that fits smooth curves to input, a variable-width brush, and a path eraser. -> SOURCE: legacy-nodus-3.6

**Fidelity:** Nodus tool rail and canvas -- docs/captures/nodus/main-window/.
**Job:** a designer can sketch freehand and get clean, editable curves. Consumer: the document.
**Treatment:** pencil samples input (with WPF stylus pressure where present), smooths with a fidelity setting, and fits cubics (Schneider's algorithm); brush outlines a variable-width stroke into a filled path; eraser splits paths it crosses. Cheaper substitute that fails the checkpoint: polylines of raw input points.
**Chrome:** consume `ToolBase`, the §2 path operations, and the history.

**Requires:** display-session -- freehand input needs an interactive desktop

- [ ] Curve fitting with tests bounding the error and node count. Done when: a recorded input trace fixture fits within tolerance.
- [ ] Pencil, brush, and eraser tools with keymap entries and guide pages. Done when: each has a driven capture.
- [ ] Commit: `"nodus: pencil, brush, and eraser tools with curve fitting"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the fitting tests reporting against the recorded trace. Cheaper substitute that fails: raw polylines.

## 16. Large Documents: Spatial Index, Culling, Dirty Regions

`standards/shared.md` names the budget: a 10,000-node path set must stay interactive. Hit-testing and rendering are linear in element count today. -> SOURCE: legacy-nodus-12.1

- [ ] Add a benchmark project (`tests/Photon.Nodus.Benchmarks`, BenchmarkDotNet) with a generated 10,000-element document measuring hit-test and full render. Done when: baseline numbers are recorded in `docs/dev/nodus/performance.md`.
- [ ] Add an R-tree spatial index for hit-testing and viewport culling. Done when: hit-test time drops by at least 10x on the benchmark (quoted).
- [ ] Render only dirty regions on edits and cache static layers as pictures (`SKPicture`). Done when: a single-element move re-renders under 16 ms on the benchmark machine (quoted with its CPU).
- [ ] Long operations (open, export) over one second show progress in the status strip and can be cancelled. Done when: opening the generated document shows progress.
- [ ] Commit: `"nodus: interactive editing of 10,000-element documents"`

**Test checkpoint:** the benchmark run's before and after numbers are quoted; `dotnet test Photon.slnx` exits 0 with spatial-index tests reporting. Cheaper substitute that fails: a cap on element count.

## 17. Accessibility and Localization

Every surface must be operable by keyboard and screen reader and translatable. -> SOURCE: legacy-nodus-13

- [ ] Audit every window with Accessibility Insights for Windows (version quoted) and fix every failure; add missing `AutomationProperties`. Done when: the audit report shows no failures and is committed under `docs/dev/nodus/accessibility/`.
- [ ] Move every user-visible string to `.resx` resources with a pseudo-localized build that proves no string is hardcoded. Done when: the pseudo-locale run shows every string transformed (capture).
- [ ] High contrast and 200 percent scaling pass on every window. Done when: captures at both are committed.
- [ ] Commit: `"nodus: accessibility audit fixes and localizable strings"`

**Requires:** display-session -- the accessibility audit and captures need an interactive desktop

**Test checkpoint:** the committed audit report shows zero failures; the pseudo-locale capture shows no untransformed string. Cheaper substitute that fails: adding automation names only to toolbar buttons.

## 18. Brushes, Patterns, and Color Tools

Artistic work needs calligraphic and pattern brushes, pattern fills, and color harmony and recolor tools. -> SOURCE: legacy-nodus-6

**Fidelity:** Brushes panel and Recolor dialog -- new build, no baseline; captured to docs/captures/nodus/brushes/ and docs/captures/nodus/recolor/.
**Job:** a designer can apply brush styles to paths, fill with patterns, and recolor artwork by harmony rules. Consumer: the document.
**Treatment:** brushes are expanded to outlines on export so other apps render them; patterns map to SVG `<pattern>`; recolor maps a selection's colors through a harmony wheel with preview. Cheaper substitute that fails the checkpoint: brush styles that exist only in Nodus's renderer.
**Chrome:** consume §5's swatches and §15's brush outlining.

**Requires:** display-session -- the panels need an interactive desktop

- [ ] Brush library with calligraphic and pattern brushes, expanded on export. Done when: an exported brushed path renders in Inkscape.
- [ ] Pattern fills and the Recolor dialog. Done when: fixtures round-trip patterns and a recolor test maps a known palette.
- [ ] Commit: `"nodus: brushes, pattern fills, and recolor"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the brush and recolor tests reporting; captures committed. Cheaper substitute that fails: renderer-only brushes.

## 19. Print and Prepress

A designer prints proofs and prepares files for print shops: bleed, crop marks, and CMYK proofing. -> SOURCE: legacy-nodus-9

**Fidelity:** Print dialog -- new build, no baseline; captured to docs/captures/nodus/print/.
**Job:** a designer can print artboards with marks and bleed and soft-proof colors against a CMYK profile. Consumer: the printer and the PDF export.
**Treatment:** File, Print through the Windows print dialog with artboard selection, scaling, crop marks, and bleed; PDF export gains bleed and marks; View, Proof Colors applies an ICC CMYK profile through a color-management library chosen by a recorded decision (lcms2 bindings or equivalent, license checked). Cheaper substitute that fails the checkpoint: printing a screenshot of the canvas.
**Chrome:** consume the PDF exporter and the artboard model.

**Requires:** display-session -- the print dialog needs an interactive desktop

- [ ] Print with marks and bleed. Done when: printing to "Microsoft Print to PDF" shows marks at the bleed offset (file committed).
- [ ] Soft proofing with a recorded color-management decision in `docs/dev/decisions.md`. Done when: a proof of a known color matches the profile's conversion within a stated delta E.
- [ ] Commit: `"nodus: printing with marks and bleed, and CMYK soft proofing"`

**Test checkpoint:** the printed PDF and the proof test are quoted; the decision entry exists. Cheaper substitute that fails: canvas screenshots.

## 20. Scripting and Plugins

Power users automate repetitive work. The legacy plan named JavaScript scripting and plugins; this suite's Imago already has a Roslyn scripting host project. Nodus's scripting starts from a stable command surface: scripts call the same commands the keymap does. -> SOURCE: legacy-nodus-7.4

- [ ] Decide the scripting language and host (C# scripting through Roslyn as Imago has, or a JavaScript engine), license checked, recorded in `docs/dev/decisions.md`; if both editors choose the same host, file its move to `Photon.Core` through `add-todo`. Done when: the entry exists.
- [ ] Expose a documented object model (document, selection, commands) to scripts, with every script edit recorded as one undoable transaction. Done when: a sample script that aligns and recolors a selection runs and undoes in one step.
- [ ] A Scripts menu listing scripts from the app-data `scripts` folder, with errors shown with line numbers. Done when: a script with a syntax error reports its line.
- [ ] Commit: `"nodus: scripting over the command surface"`

**Requires:** display-session -- running scripts from the menu needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with scripting-host tests reporting; the sample script run is logged and undone. Cheaper substitute that fails: scripts that edit the model outside the history.

## 21. Onboarding and the Navigator

First-run users need orientation, and large artboards need a navigator (minimap). -> SOURCE: legacy-nodus-5.8-5.9

**Fidelity:** First-run welcome and Navigator panel -- new build, no baseline; captured to docs/captures/nodus/welcome/ and docs/captures/nodus/navigator/.
**Job:** a new user can start from a template or a recent file on first run; any user can pan a large document from a thumbnail. Consumer: the user.
**Treatment:** a welcome surface on start with no document (New from preset, Open, recent files, a link to the guide), dismissible and remembered; a Navigator panel with a live thumbnail and a draggable viewport rectangle. Cheaper substitute that fails the checkpoint: a static splash image.
**Chrome:** consume the artboard presets, recent files, and the renderer.

**Requires:** display-session -- the surfaces need an interactive desktop

- [ ] Welcome surface with its settings key. Done when: it shows on first run and not after "Don't show again".
- [ ] Navigator panel. Done when: dragging its rectangle pans the canvas (capture).
- [ ] Commit: `"nodus: a welcome surface and a navigator panel"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the welcome settings test reporting; captures committed. Cheaper substitute that fails: a splash image.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] No service in `docs/dev/nodus/service-triage.md` is still marked deferred
- [ ] Every new format has a fidelity fixture
- [ ] `python scripts/todo-graph.py validate` clean
