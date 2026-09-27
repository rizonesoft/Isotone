---
schema_version: 1
id: nodus-parity-document
domain: 02-nodus
status: draft
title: "TODO-07 -- Nodus Parity: Document Model, Pages, Layers, Selection, and View"
depends_on: []
track: N7
---

# TODO-07 -- Nodus Parity: Document Model, Pages, Layers, Selection, and View

> **Goal:** Nodus gains the document foundation every later parity file builds on: a live-object persistence contract in the `nodus:` SVG namespace with plain-SVG fallbacks, a spatial index that keeps a 10,000-object document interactive, one page and artboard model with Corel-style multipage views, full layer and Objects panel control, the Select menu and selection tools, isolation mode, a contextual property bar and Properties panel, rulers, grids, guides, measurement, the full snapping set, view modes and windows, a History panel with paste variants, and a New Document dialog with presets and templates, each edit one undo step and each tunable a setting.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The SVG writer and reader know nothing about artboards, so a saved document loses every artboard but the implicit document bounds, and no `nodus:` namespace exists yet: `SvgParser.cs` reads only `inkscape:label` from a foreign namespace. `ArtboardManager` (412 lines) already models artboards with create, duplicate, rename, resize, move, reorder, navigate, and grid, row, and column arrange, and `Artboard.cs` holds 24 presets; none of it is wired to a surface or persisted. `VectorDocument` holds a flat `Elements` collection with no layers or guides; `Layer` and `LayerManager` (449 lines) exist beside it, unused by the document. Guides live in a private list inside `SnapManager`, not in the document, so they are never saved, and `SnapTarget` knows only Grid, Guides, Objects, and SmartGuides. There is no spatial index: `SkiaRenderer` walks every element each frame and hit testing walks the list back to front. The canvas already draws rulers and a grid (`SkiaCanvas.ShowRulers`, `SkiaRenderer.RenderRulers`, `RenderGrid`), and zoom is clamped at 6,400 percent. No magic wand or lasso tool exists. Undo is Nodus-local (`HistoryManager`, 167 lines) until `D01 T02 §4` moves it to `Photon.Core`. Paths below name the post-rename `Photon.Nodus.*` projects (`D02 T01 §1`); the claims name today's `Bezier.*` paths.
<!-- claim: count "Artboard" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->
<!-- claim: count "Artboard" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->
<!-- claim: count "nodus:" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->
<!-- claim: count "inkscape:label|InkscapeNs \+ \"label\"" src/Nodus/Bezier.Core/Services/SvgParser.cs = 1 -->
<!-- claim: lines src/Nodus/Bezier.Core/Services/ArtboardManager.cs = 412 -->
<!-- claim: count "^        \(\"" src/Nodus/Bezier.Core/Models/Artboard.cs = 24 -->
<!-- claim: count "Layer" src/Nodus/Bezier.Core/Models/VectorDocument.cs = 0 -->
<!-- claim: lines src/Nodus/Bezier.Core/Services/LayerManager.cs = 449 -->
<!-- claim: count "private readonly List<Guide> _guides" src/Nodus/Bezier.Core/Services/SnapManager.cs = 1 -->
<!-- claim: count "Guide" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->
<!-- claim: count "SmartGuides = 8" src/Nodus/Bezier.Core/Services/SnapManager.cs = 1 -->
<!-- claim: count "RTree|SpatialIndex|QuadTree" src/Nodus/Bezier.Core/Services/*.cs = 0 -->
<!-- claim: count "foreach \(var element in document\.Elements\)" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 1 -->
<!-- claim: count "ShowRulers" src/Nodus/Bezier.Desktop/Controls/Canvas/SkiaCanvas.cs = 9 -->
<!-- claim: count "MaxZoom = 64\.0" src/Nodus/Bezier.Desktop/Controls/Canvas/CanvasState.cs = 1 -->
<!-- claim: count "Magic|Lasso" src/Nodus/Bezier.Core/Tools/*.cs = 0 -->
<!-- claim: lines src/Nodus/Bezier.Core/Services/HistoryManager.cs = 167 -->
<!-- claim: absent src/Photon.Core/History/UndoHistory.cs -->

## Inputs

- [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) -- the catalog rows each section owns (`NP-` ranges named in each context paragraph)
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- the design these sections were authored from, including the `nodus:` namespace decision
- [`standards/nodus.md`](../../standards/nodus.md) -- SVG is native, one render path, every mutation a command, Inkscape the fidelity oracle
- [`standards/shared.md`](../../standards/shared.md) -- the design contract, settings, logging, atomic saves, and performance rules
- `src/Nodus/Bezier.Core/Services/ArtboardManager.cs`, `LayerManager.cs`, `SnapManager.cs`, `SelectionManager.cs` -- the services §3, §5, §10, §11, and §6 grow into the document model
- -> XREF: D02 T05 §4 -- Nodus 0.1.0 ships first; every section here follows it
- -> XREF: D02 T01 §1 -- the rename to `Photon.Nodus.*` the target paths assume
- -> XREF: D02 T02 §3 -- the one selection owner §6 extends
- -> XREF: D02 T02 §6 -- the layers panel §5 grows into the Objects panel
- -> XREF: D02 T02 §7 -- basic snapping and the `Nodus.Snap.*` toggles §11 extends
- -> XREF: D02 T06 §7 -- per-document scopes, tabs, and the nested layer tree §3, §5, and §12 build on
- -> XREF: D02 T04 §1 -- atomic save and dirty tracking §14's Save a Copy, Revert, and locked-file refusals reuse
- -> XREF: D02 T04 §2 -- the SVG round-trip fixtures §1 extends with live fixtures
- -> XREF: D02 T04 §5 -- recent files and autosave, which §14's templates and §2's background save must not break
- -> XREF: D02 T03 §3 -- the clipboard service §13 and §3 extend
- -> XREF: D02 T03 §4 -- the property commands §8 writes through
- -> XREF: D01 T02 §4 -- the suite history §13's History panel reads
- -> XREF: D02 T06 §12 -- the HUD whose label style §10's measurement readouts share
- -> XREF: D02 T06 §13 -- the Preferences pages that list the settings added here
- -> XREF: D02 T08 §4 -- live shapes, the first consumer of §1's contract
- -> XREF: D02 T11 §1 -- the live-effect framework built on §1
- -> XREF: D02 T09 §21 -- symbol overrides persisted through §1
- -> XREF: D02 T13 §2 -- printing the pages §3 models and the bleed §4 stores
- -> XREF: D02 T13 §4 -- marks and bleed reading `nodus:bleed` from §4
- -> XREF: D02 T14 §3 -- Illustrator artboards landing in §3's page model
- -> XREF: D02 T14 §6 -- CorelDRAW pages and master layers landing in §3 and §5
- -> XREF: D02 T16 §4 -- Preferences pages over the settings this file adds
- -> XREF: D02 T16 §5 -- UI appearance preferences over the view keys §12 adds
- -> XREF: D02 T17 §1 -- Nodus 0.2.0 releases this file
- -> XREF: D02 T10 §2 -- the rich text model whose frames, threads, and path text persist under §1
- -> XREF: D02 T10 §5 -- glyph snapping that registers with §11's snap engine
- -> XREF: D02 T10 §6 -- paragraph layout reading §9's baseline grid
- -> XREF: D02 T09 §8 -- the gradient annotator whose visibility §12's toggle owns
- -> XREF: D01 T05 §3 -- the AI provenance record Nodus embeds in §1's root metadata
- -> XREF: D02 T15 §1 -- the Nodus provenance panel that writes into §1's document block
- -> XREF: D02 T12 §1 -- bitmap objects, whose FX stacks, live traces, and mockups persist through §1
- -> XREF: D03 T08 §4 -- Imago parity document and view cites §9: `UnitConverter`, moved to `Photon.Core` by D03 T08 §4; §11: the snapping core, moved to `Photon.Core` by D03 T08 §4
- -> XREF: D03 T20 §1 -- Imago parity workspace cites §8: `CompactNumberBox`, `UnitExpression`, and the contextual task bar host
- -> XREF: D01 T01 §5 -- the implicit field styles, focus tracker, and focus ring §8's `CompactNumberBox` template draws with

## Outcome

- A live object saved by Nodus reopens live in Nodus and renders as ordinary SVG in Inkscape and browsers; unknown `nodus:` data and foreign namespaces survive a round trip byte-equivalent.
- A generated 10,000-element, 1,000-artboard document pans and zooms at 60 fps with a viewport render under 16 ms and a hit test under 1 ms.
- Pages and artboards are one model, saved in the `nodus:` document block and as Inkscape pages, with the Artboards and Pages panel, the artboard tool, multipage views, page backgrounds, and live page numbers.
- Layers, sublayers, and master layers are part of the document, shown in one Objects panel tree, and survive save and reopen with their lock, print, and export flags.
- The Select menu, Select Same, magic wand, lasso, saved selections, isolation mode, and the contextual property bar work on the rendered app, each edit one undo step.
- Rulers, units, drawing scale, grids, guides, the measure tool, the Info panel, every snapping mode, every view mode, saved views, and window arrangement are available, with every tunable a `Nodus.*` setting that a named class reads.
- The History panel jumps to any state; every paste variant and quick-duplicate gesture places exactly where it says.
- The New Document dialog, presets, templates, document information, Save a Copy, Save Selected Only, Revert, and Close All work, with locked targets refused by name.

**Adjacency:** list=applicable @ D02 T07 §5; document=applicable @ D02 T13 §2; settings=applicable; reporting=applicable @ D02 T07 §10; notifications=applicable @ D02 T07 §2; permissions=applicable @ D02 T07 §14; audit=applicable; exchange=applicable @ D02 T07 §1; reverse=applicable

**Adjacency rationale:** The Objects panel search and filter, the Artboards and Pages panel find by name, saved views, and the template browser are the browsable lists. Pages, bleed, and page background are what print consumes; this file models them and `D02 T13 §2` prints them. Every toggle and value here is a `Nodus.*` key with a default and a named consumer. The Info panel, measure tool, document information, and History panel are the reports. Long operations report progress and cancel on the status strip, and background save reports completion there (§2). Locked or read-only save targets, unreadable template folders, and locked layers and artboards refuse edits by name (§14, §5, §3). Every command is one history entry with one Serilog Information line. The `nodus:` namespace contract, Inkscape page and guide interop, templates, and document presets are the exchange surface. Every create has undo, deleting pages and layers is restored by undo, and Revert returns to saved.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The live-object contract in the nodus namespace | D02 T05 §4 |  [ ]   |
|   2   |   §2    | Spatial index, culling, and dirty-region rendering | D02 T05 §4 |  [ ]   |
|   3   |   §3    | Pages and artboards: one model, panel, and commands | §1, D02 T06 §7 |  [ ]   |
|   4   |   §4    | Multipage views, page background, page numbers, navigation | §3 |  [ ]   |
|   5   |   §5    | Layers, master layers, lock and hide, the Objects panel | §3, D02 T06 §7 |  [ ]   |
|   6   |   §6    | Selection: Select menu, Select Same, wand, lasso, saved selections | D02 T05 §4 |  [ ]   |
|   7   |   §7    | Isolation mode and focus mode | §5 |  [ ]   |
|   8   |   §8    | The Properties panel and the contextual property bar | D02 T05 §4, D01 T01 §5 |  [ ]   |
|   9   |   §9    | Rulers, units, drawing scale, and grids | §3 |  [ ]   |
|  10   |   §10   | Guides, the Guides panel, the measure tool, the Info panel | §9 |  [ ]   |
|  11   |   §11   | Snapping modes, smart guides, dynamic and alignment guides | §10, D02 T02 §7 |  [ ]   |
|  12   |   §12   | View modes, zoom, rotate view, saved views, windows | §2 |  [ ]   |
|  13   |   §13   | History panel, repeat, paste variants, quick duplicates | D02 T05 §4 |  [ ]   |
|  14   |   §14   | New Document dialog, presets, templates, document information | §3 |  [ ]   |

---

## 1. The Live-Object Contract: Parameters in the Nodus Namespace with an Expanded SVG Fallback

SVG is Nodus's native format (`standards/nodus.md`), but parity adds live objects SVG cannot express: blends, envelopes, live shapes, symbol overrides, pages, and effect stacks. This section fixes one contract for all of them, for every document Nodus imports or exports, so no later file invents its own: parameters in the `nodus:` XML namespace, the expanded result as ordinary SVG geometry beside them, and a reader that restores the live object when the parameters are present and falls back to the geometry when they are not. It must not break the `D02 T04 §2` round-trip fixtures: a document with no live object writes no `nodus:` declaration at all. Catalog: NP-0001 to NP-0002 (Expand live objects with options; identify objects by name or XML ID).

**Fidelity:** Object, Expand dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/expand/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Object, Expand dialog -- new build, no baseline; captured to docs/captures/nodus/expand/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can turn any live object into plain paths and undo it. Consumer: the SVG reader and writer that open and save every file Nodus imports or exports, and every later live-object kind.
**Treatment:** a modal with Object, Fill, and Stroke checkboxes and a Gradient radio pair (Gradient Mesh disabled with a tooltip naming `D02 T09 §9`, Specify N objects), one history entry "Expand". Cheaper substitute that fails the checkpoint: Expand that only ungroups the fallback.
**Chrome:** consume `Photon.UI` dialog styles and the suite history. Do not add a second serializer.

**Requires:** display-session -- the Expand dialog run and the Inkscape open of a live fixture need an interactive desktop

- [ ] Record the namespace URI `https://schemas.rizonesoft.com/nodus/1` and the "SVG stays native, Inkscape-style namespace" rationale as a row in `docs/dev/decisions.md`. Done when: the row names the URI, the fallback rule, and the cost of changing it (every saved live document).
- [ ] Add `ILiveObject` in `src/Nodus/Photon.Nodus.Core/Live/ILiveObject.cs` with `string Kind`, `int SchemaVersion`, `IReadOnlyList<Guid> Sources`, `void WriteParameters(XElement target)`, and `IReadOnlyList<VectorElement> Expand()`, with XML documentation on each member. Done when: the project builds and the interface is the only live-object abstraction in the solution.
- [ ] Add `LiveObjectRegistry` in `src/Nodus/Photon.Nodus.Core/Live/LiveObjectRegistry.cs` with `Register(string kind, ILiveObjectReader reader)` and `TryRead(XElement group, out ILiveObject live)`, registered as a singleton in the Nodus composition root. Done when: `ServiceRegistrationTests` resolves it and a second registration of one kind throws naming the kind.
- [ ] Teach `SvgExporter` to declare `xmlns:nodus` on the root `<svg>` only when a live object or document block exists. Done when: `SvgRoundTripTests` over the existing `D02 T04 §2` fixtures still pass byte for byte and a probe document gains exactly one declaration.
- [ ] Write each live object as `<g id="..." nodus:kind="..." nodus:v="1" nodus:hash="...">` whose children are the expanded plain SVG plus one `<nodus:params/>` child carrying parameters as attributes and `nodus:src="#id1 #id2"` for sources, numbers formatted with `CultureInfo.InvariantCulture` and the `R` format. Done when: a saved probe object opens in a browser and shows its fallback geometry. Cheaper substitute: writing only the expanded geometry, which loses the live object.
- [ ] Compute `nodus:hash` as a SHA-1 over the canonical fallback markup in `src/Nodus/Photon.Nodus.Core/Live/FallbackHash.cs`. Done when: `FallbackHashTests` prove the hash is stable across attribute order and changes when one coordinate changes.
- [ ] Teach `SvgImporter` to ask the registry for `nodus:kind`: a known kind rebuilds the live object and regenerates its fallback; a hash mismatch opens a plain group and logs Warning `"{Kind} was edited outside Nodus; opened expanded"`, listed in the open summary. Done when: `LiveObjectContractTests.HashMismatchOpensExpanded` passes.
- [ ] Keep an unknown `nodus:kind` or a newer `nodus:v` verbatim in `UnknownLiveData` (an `XElement` on the element), render it from its fallback, and write it back unchanged. Done when: `LiveObjectContractTests.UnknownKindPreserved` compares the written block byte for byte.
- [ ] Keep foreign-namespace attributes (`inkscape:`, `sodipodi:`, `i:`, `x:`) on any element in `VectorElement.ForeignAttributes` and re-emit them. Done when: a fixture carrying all four prefixes round-trips with every attribute present.
- [ ] Add the document block: one `<nodus:document nodus:v="1">` inside `<metadata>`, written and read by `DocumentBlockSerializer` in `src/Nodus/Photon.Nodus.Core/Live/`, with named child slots for pages (§3), guides (§10), grids and units (§9), views (§12), and selections (§6), each slot owned by its section. Done when: an empty slot writes nothing and an unknown child block is preserved. Source: today's `SvgParser.cs` skips root `<metadata>`; it must now keep it.
- [ ] Teach the SVG reader to stop skipping the root `<metadata>` element (today's `SvgParser.cs` drops it): keep it on the document as `RootMetadata`, hand the `nodus:document` child to `DocumentBlockSerializer`, and preserve every child it does not own (RDF and Dublin Core for `§14`, `photon:provenance` records for `D02 T15 §1`, and any foreign block) verbatim for the writer, which emits the element only when it has content. Done when: `RootMetadataRoundTripTests` open a fixture carrying an RDF block, a `photon:provenance` child, and a foreign-namespace block, save, and compare each child byte for byte, and a document with no metadata still saves byte-identical to before.
- [ ] Write object names as `nodus:label` (reading `inkscape:label` as a fallback), notes as the standard SVG `<desc>`, and keep the `Guid` identity in `id`. Done when: a named, annotated element reopens with its name, notes, and `Id` equal.
- [ ] Add setting `Nodus.Svg.IdentifyBy` (`XmlId` default, `Name`) read by `SvgExporter`: `Name` writes `id` as a sanitized, unique form of the object name for web output (AI-1158). Done when: two objects named `Logo` write `id="Logo"` and `id="Logo-2"`, and the setting change logs one Information line.
- [ ] Add `ExpandCommand` in `src/Nodus/Photon.Nodus.Core/Commands/ExpandCommand.cs` that replaces each selected live object with `Expand()`'s result in place (same z-order, layer, and name), one undo step, logging `Expanded {Count} live object(s)`. Done when: undo restores the live object with its parameters intact.
- [ ] Add the Expand dialog `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/ExpandDialog.xaml` with `ExpandDialogViewModel` (Object, Fill, Stroke, Gradient radio pair, Gradient Mesh disabled naming `D02 T09 §9`), opened from Object, Expand. Done when: every control has an automation name, Enter and Escape work, and the capture is committed under `docs/captures/nodus/expand/`. Cheaper substitute: an Expand that ignores the checkboxes.
- [ ] Add a test-only `ProbeLiveObject` kind in `tests/Photon.Nodus.Tests/Live/ProbeLiveObject.cs` and `LiveObjectContractTests` covering write, reopen as live, hash mismatch, unknown kind, and `ExpandCommand` undo. Done when: all five cases pass.
- [ ] Commit fixtures under `tests/fixtures/nodus/svg-live/` (probe object, unknown future kind, Inkscape-edited fallback) with PNG goldens rendered by Inkscape and its version in `goldens/VERSION.txt`. Done when: the goldens and the version file are committed.
- [ ] Add `SvgLiveRoundTripTests` that open, save, and reopen every `svg-live` fixture and compare element by element plus the preserved unknown block byte for byte. Done when: the test passes and fails if the unknown block is dropped.
- [ ] Document the contract in `docs/dev/nodus/live-objects.md` (wire shape, registry, hash rule, preservation, how a later kind registers) and add an Expand page to `docs/user/nodus/`. Done when: both pages exist and the user page names the dialog's options.
- [ ] Commit: `"nodus: the live-object contract in the nodus namespace with an expanded SVG fallback"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~SvgLiveRoundTripTests|FullyQualifiedName~LiveObjectContractTests"` exits 0, every `tests/fixtures/nodus/svg-live/` file compares equal element by element after open, save, and reopen, the unknown block is byte-identical, and Inkscape's rendering of each saved file matches its golden within 1/255 (Inkscape version quoted). Cheaper substitute that fails: writing only the expanded geometry, which the reopen-as-live assertion catches.

## 2. Spatial Index, Culling, and Dirty-Region Rendering

Today the renderer walks every element each frame and hit testing walks the list back to front, which is fine at 0.1.0 sizes and fatal at parity sizes. This section adds an R-tree over visual bounds that the renderer, hit testing, marquee, and snapping all query, then culls to the viewport, redraws only dirty regions over cached pictures, and moves long operations to a cancellable worker whose progress and completion notifications appear on the status strip. It must not change what renders: the pixels before and after are identical. Promoted from backlog B-009 (the entry left the backlog when this file was integrated). Catalog: NP-0188 to NP-0196 (large canvas and 1,000 artboards, GPU or CPU rendering, anti-aliasing, live preview while dragging, smooth pan and zoom, Refresh Window, bitmap transform previews, background save, low-resolution navigation preview). -> SOURCE: legacy-nodus-12.1

**Fidelity:** Nodus main window, View menu and status strip -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/StatusBar/README.md, docs/design/shell-layout.md#nodus-vector -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Nodus main window, View menu and status strip -- docs/captures/nodus/main-window/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can pan, zoom, select, and drag in a 10,000-object or 1,000-artboard document without stutter. Consumer: the canvas and every tool.
**Treatment:** 60 fps pan and zoom with a low-resolution cached frame while moving; View, GPU Preview and Preview on CPU (Ctrl+E), View, Refresh (Ctrl+W), and a status-strip progress bar with Cancel. Cheaper substitute that fails the checkpoint: lowering render quality globally.
**Chrome:** consume the status strip and the settings store. Do not add a second progress surface.

**Requires:** display-session -- the frame-time measurement on a live canvas needs an interactive desktop

- [ ] Add `ISpatialIndex` in `src/Nodus/Photon.Nodus.Core/Spatial/ISpatialIndex.cs` with `Insert(Guid, Rect)`, `Update(Guid, Rect)`, `Remove(Guid)`, `Query(Rect, List<Guid>)` into a caller-owned list, `HitCandidates(Point, double, List<Guid>)` top-most first by z-order, `Nearest(Point, double, int, List<Guid>)`, and `Extent`. Done when: the interface builds with XML documentation and no member allocates a result collection.
- [ ] Implement `RTreeIndex` in the same folder: an own R*-tree with node capacity 16 and STR bulk load on open. Done when: `RTreeIndexTests.QueryMatchesBruteForce` over 5,000 random rects of random sizes equals a brute-force scan for 1,000 random queries.
- [ ] Add `DocumentSpatialIndex` subscribing to the document's element added, removed, and bounds-changed events, indexing `GetVisualBounds()` (stroke, markers, effects) and keeping `GetGeometricBounds()` for alignment. Done when: `RTreeIndexTests.TracksDocumentEvents` proves no caller updates the index by hand.
- [ ] Rewire `SkiaRenderer` to cull by viewport `Query` and delete the full `foreach (var element in document.Elements)` walk. Done when: a render of the 10,000-element fixture zoomed to one corner visits only the queried elements (counter asserted in a test).
- [ ] Rewire `SelectionManager.HitTestAndSelect` and `SelectInRect` to `HitCandidates` and `Query`, and `SnapManager` object candidates to `Nearest`. Done when: the existing selection and snapping tests pass unchanged and the old list walks are deleted.
- [ ] Add `DirtyRegionTracker` in `src/Nodus/Photon.Nodus.Desktop/Rendering/` that unions old and new visual bounds per change, and clip `SkiaCanvas` redraw to the dirty rect. Done when: `DirtyRegionTrackerTests` prove a moved element dirties exactly its old and new bounds.
- [ ] Cache one `SKPicture` per top-level element keyed by `Id` plus a change version, invalidated by the document's change events, with no allocation per frame (`standards/shared.md`). Done when: a frame with no change allocates zero bytes in a `GC.GetAllocatedBytesForCurrentThread` probe test.
- [ ] Add `Nodus.Render.Gpu` (true) consumed by `SkiaCanvas`: `SKGLElement` with a `GRContext`, falling back to `SKElement` with a Warning when context creation fails, toggled by View, GPU Preview and Preview on CPU (Ctrl+E). Done when: forcing a context failure in a test logs the Warning and renders on CPU.
- [ ] Add `Nodus.Render.AntiAlias` (true), `Nodus.Render.LivePreviewWhileDragging` (true; off draws an outline during drags), and `Nodus.Render.NavigationPreview` (`HideForMouse` default, `Always`, `Never`), each read by `SkiaCanvas` and each change logged. Done when: toggling each changes the rendered frame in a driven run.
- [ ] Draw a low-resolution cached frame while panning and zooming and re-render at full quality on idle. Done when: the frame-time log during a pan stays under 16.7 ms per frame on the reference machine.
- [ ] Add `VectorDocument.ScaleFactor` (1 or 10, the Large Canvas option) written as `nodus:scale` in the §1 document block and applied to displayed units. Done when: a Large Canvas document reopens with its scale and shows ten times the unit values.
- [ ] Add `LongOperation` in `src/Nodus/Photon.Nodus.Desktop/Services/LongOperation.cs` running any job expected to exceed one second on a worker with `CancellationToken` and `IProgress<double>` into the status strip with Cancel. Done when: `LongOperationTests.CancelLeavesDocumentUnchanged` passes, and the status strip must show completion or failure notifications.
- [ ] Make Save snapshot the model to an `XDocument` on the UI thread and write through the `D02 T04 §1` atomic writer on a `LongOperation`, so editing continues (CD-196), with a completion line in the status strip. Done when: a driven save of the 10,000-element fixture accepts a drag during the write and the saved file reopens equal to the snapshot. Cheaper substitute: saving on the UI thread with a busy cursor.
- [ ] Draw bitmap drag previews (CD-184) from the cached decoded `SKImage` under the live transform instead of resampling per frame. Done when: dragging a placed bitmap keeps frame time under 16.7 ms.
- [ ] Add View, Refresh Window (Ctrl+W) that drops the picture cache and redraws, logging one Information line. Done when: the log line appears and the cache counter resets.
- [ ] Add a fixture generator `tests/Photon.Nodus.Tests/Fixtures/LargeDocumentGenerator.cs` producing a 10,000-element and a 1,000-artboard document from a fixed seed. Done when: two runs produce byte-identical files.
- [ ] Add `tests/Photon.Nodus.Benchmarks/` (BenchmarkDotNet; the package decision recorded in `docs/dev/decisions.md` with its MIT license) measuring viewport render, hit test, and open over the generated documents. Done when: the project runs from `dotnet run -c Release` and prints the three numbers.
- [ ] Add the performance keys to the user guide page for View in `docs/user/nodus/`. Done when: the page names Ctrl+E, Ctrl+W, and the navigation preview options.
- [ ] Commit: `"nodus: a spatial index, viewport culling, and dirty-region rendering for large documents"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~RTreeIndexTests|FullyQualifiedName~DirtyRegionTrackerTests|FullyQualifiedName~LongOperationTests"` exits 0; the benchmark project reports viewport render under 16 ms, hit test under 1 ms, and open under 2 s on the generated fixtures (numbers quoted in the stamp); a driven run on the 10,000-element fixture quotes the frame-time log before and after. Cheaper substitute that fails: a uniform grid bucket, which the random-size brute-force comparison and the 1,000-artboard benchmark expose.

## 3. Pages and Artboards: One Model, the Artboards and Pages Panel, and Artboard Commands

Illustrator has artboards and CorelDRAW has pages; they are the same job, so Nodus has one model that is both, persisted through §1 and readable by Inkscape 1.2 and later as pages. `ArtboardManager` already holds the arrange math and is kept; what changes is that the model lives on the document, is saved, and has a surface. It must not break single-page documents: a document with one page writes no page block and opens as before. Promoted from backlog B-004 (the entry left the backlog when this file was integrated, together with B-011, which `D02 T13 §2` promoted). Catalog: NP-0003 to NP-0031 (the artboard tool, the Artboards and Pages panel, artboard commands and options, page size presets and printer size, orientation, and page dimensions on the property bar). -> SOURCE: legacy-nodus-4.6

**Fidelity:** Artboards and Pages panel, Artboard tool, Artboard Options and Page Size dialogs -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/artboards/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/Dialog/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Artboards and Pages panel, Artboard tool, Artboard Options and Page Size dialogs -- new build, no baseline; captured to docs/captures/nodus/artboards/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can create, size, arrange, rename, reorder, and delete pages or artboards and keep their art with them. Consumer: the document, the SVG writer, export, and print.
**Treatment:** a panel list with number, name, size, and lock columns; edge plus buttons on the active artboard; on-canvas labels renamable in place; every command one undo step. Cheaper substitute that fails the checkpoint: a list of rectangles drawn on a layer.
**Chrome:** consume AvalonDock panels, the icon catalog, the settings store, and the suite history. Do not add a second list control.

**Requires:** display-session -- the artboard tool, panel drag reorder, and label rename need an interactive desktop

- [ ] Add `Page` in `src/Nodus/Photon.Nodus.Core/Models/Page.cs` replacing `Artboard` (name, bounds, orientation, background color, locked, video settings, per-page size flag), owned by `VectorDocument.Pages` with an `ActivePage`. Done when: `Artboard.cs` is gone and every former caller compiles against `Page`.
- [ ] Rename `ArtboardManager` to `PageManager` over the document, keeping its arrange math. Done when: the arrange tests from `ArtboardManager` pass unchanged against `PageManager`.
- [ ] Write pages as `<nodus:page>` in the §1 document block and as Inkscape `<inkscape:page>` elements inside `sodipodi:namedview`; the reader accepts either. Done when: `PageSerializationTests` round-trip both forms and a single-page document writes neither.
- [ ] Add New, Duplicate (with contents), Delete, and Delete Empty page commands in `src/Nodus/Photon.Nodus.Core/Commands/Pages/`, each one undo step and one Information line. Done when: `PageCommandTests` prove each and its undo.
- [ ] Add Rename (one, or many at once with a numbered pattern) and Reorder commands. Done when: renaming three pages to `Card ##` yields `Card 01` to `Card 03` and undo restores the old names.
- [ ] Add Rearrange (grid by row or column, left-to-right or right-to-left, columns, spacing, move artwork) over the kept arrange math. Done when: a test rearranges six pages into two columns and the artwork moves with each page.
- [ ] Add Fit to Artwork Bounds, Fit to Selected Art, and Convert to Artboards (selected rectangles become pages). Done when: each command's resulting bounds equal the expected rectangles in `PageCommandTests`.
- [ ] Add Switch Orientation, Set Size (current page or all pages), and Lock Content (locked page content refuses edits with a status message naming the page). Done when: editing an element on a locked page is refused and logged.
- [ ] Add `ArtboardTool` (Shift+O) in `src/Nodus/Photon.Nodus.Core/Tools/ArtboardTool.cs`: draw, select by click, Shift, or marquee, move with the Move/Copy Artwork option, resize with Scale Artwork, and Alt-drag duplicate. Done when: `ArtboardToolTests` cover marquee select, move with artwork, and Alt-drag. Cheaper substitute: a tool that moves the page rectangle and leaves the art behind.
- [ ] Add Ctrl+D repeat of the last artboard action and the edge plus buttons that add or duplicate an artboard beside the active one. Done when: `ArtboardToolTests.RepeatLastAction` passes.
- [ ] Cut, copy, and paste artboards with their contents through the `D02 T03 §3` clipboard. Done when: a pasted artboard carries its elements at the same relative positions.
- [ ] Add the Artboard Options dialog `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/ArtboardOptionsDialog.xaml`: preset, width, height, orientation, X, Y, background color, center mark, cross hairs, video safe areas, pixel aspect ratio, fade outside, and update while dragging (`Nodus.Artboard.*` view keys). Done when: every field writes one `PageOptionsCommand` and the view keys are read by `SkiaRenderer`.
- [ ] Move the 24 presets into one `PagePresets` table in `src/Nodus/Photon.Nodus.Core/Pages/PagePresets.cs`, print sizes in points at 72 per inch converted to document units at 96 DPI. Done when: A4 resolves to 793.7 by 1122.5 document units in `PagePresetsTests`.
- [ ] Add the Page Size dialog and the no-selection property-bar size boxes: presets, custom sizes up to 1,800 by 1,800 inches, save and delete custom presets in `Nodus.Page.CustomPresets`, apply to current page or all pages. Done when: a saved custom preset survives restart (settings readback quoted).
- [ ] Add Get From Printer through `System.Printing.LocalPrintServer`'s default queue, refused by name when no printer exists. Done when: a test with a fake print queue sets the page to its imageable size and a missing printer shows "No default printer: page size unchanged."
- [ ] Add `PagesPanelViewModel` and `PagesPanel.xaml` in `src/Nodus/Photon.Nodus.Desktop/`: rows with number, name, size, lock, drag reorder, inline rename, find by name, and an empty-artboard badge. Done when: `PagesPanelViewModelTests` cover find and reorder, and the panel capture is committed.
- [ ] Add the page context menu: Duplicate, Rename, Lock, Delete, and Export disabled with the tooltip `Planned: D02 T14 §15`. Done when: `MenuAuditTests` accept the disabled item.
- [ ] Draw on-canvas page labels with double-click rename, the active page highlight border, and per-page background color in `SkiaRenderer`. Done when: a driven rename through the label logs one line and undo restores it.
- [ ] Add paste onto selected artboards (used by `D02 T07 §13`'s Paste on All Artboards). Done when: pasting with two artboards selected places one copy on each at the same offset.
- [ ] Commit `tests/fixtures/nodus/pages/three-pages.svg` with an Inkscape golden and version. Done when: the fixture opens in Inkscape with three pages (version quoted).
- [ ] Add a Pages and Artboards page to `docs/user/nodus/`. Done when: the page covers the tool, the panel, and every command.
- [ ] Commit: `"nodus: one page and artboard model with its panel, tool, and commands"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~PageSerializationTests|FullyQualifiedName~PageCommandTests|FullyQualifiedName~ArtboardToolTests"` exits 0, `three-pages.svg` reopens with pages equal by name, bounds, order, and background, and Inkscape shows three pages (version quoted); a driven run creating, reordering, and undoing artboards quotes its log lines. Cheaper substitute that fails: pages kept in memory only, which the reopen comparison catches.

## 4. Multipage Views, Page Background, Page Numbers, and Page Navigation

CorelDRAW lays out many pages on one canvas and numbers them with live fields; Illustrator shows artboards side by side. This section adds the layout service, the page views, page backgrounds, live page numbers, the navigator, and every page insert and go-to command over §3's model. It must not change single-page rendering. Catalog: NP-0032 to NP-0061 (the document navigator, spreads, interactive page resize, autofit, page border, bleed, printable area, page frame, page backgrounds, multipage and single page views and their layouts, free-form placement, zoom to selected pages, page thumbnails, facing pages, insert, duplicate, delete, rename, find, and go to page, and page numbers and their settings).

**Fidelity:** Document navigator, Multipage View Settings, Page Background dialog, Insert Page, Duplicate Page, Delete Page, Go to Page, Insert Page Number, and Page Number Settings dialogs -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/pages/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Canvas/README.md, docs/design/shell-layout.md#nodus-vector, new surface: docs/design/components/NodusPageNavigator/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Document navigator, Multipage View Settings, Page Background dialog, Insert Page, Duplicate Page, Delete Page, Go to Page, Insert Page Number, and Page Number Settings dialogs -- new build, no baseline; captured to docs/captures/nodus/pages/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can lay out and navigate a multipage document and number its pages. Consumer: the document, export, and print.
**Treatment:** page tabs with add-page buttons, pages laid out on one canvas in multipage view, page numbers as live fields. Cheaper substitute that fails the checkpoint: page numbers typed as static text.
**Chrome:** consume the §3 panel, the icon catalog, and `Photon.UI` dialog styles. Do not add a second page list.

**Requires:** display-session -- the navigator, multipage layout, and interactive page resize need an interactive desktop

- [ ] Write the design spec `docs/design/components/NodusPageNavigator/README.md` and its `docs/design/components/NodusPageNavigator/preview.html` card (anatomy, every state, tokens, sizes) before any XAML is written, and regenerate the design page. Done when: the spec exists and `python scripts/build-design-site.py --check` passes.
- [ ] Add `PageLayoutService` in `src/Nodus/Photon.Nodus.Core/Pages/PageLayoutService.cs` computing page origins for `Single`, `Grid` (columns, spacing), `Vertical`, `Horizontal`, and `Custom` (free positions per page), stored in the §1 document block. Done when: `PageLayoutServiceTests` assert origins for each layout.
- [ ] Add facing-page spreads (start on left or right) to the layout service. Done when: a test with five pages starting right places page 1 alone and pages 2 and 3 as a spread.
- [ ] Add `Nodus.Pages.DefaultViewMode` (Multipage default, Single) read by `DocumentFactory` for new documents. Done when: changing it changes the view of the next new document.
- [ ] Render multipage view through the §2 index and single page view showing only the active page. Done when: a driven switch between the views captures both under `docs/captures/nodus/pages/`.
- [ ] Add Zoom to Selected Pages and Show Spreads in the page thumbnails, both using the layout service. Done when: zooming to two selected pages fits their union.
- [ ] Add interactive page resize: page-label handles drag like a rectangle (Shift from center) and record one `SetPageSizeCommand`. Done when: undo restores the page size exactly. Cheaper substitute: resizing with no recorded command.
- [ ] Add Autofit Page that fits content on local layers with a margin. Done when: a test with a known object and a 10 px margin produces the expected page bounds.
- [ ] Add View, Page toggles for page border, bleed, and printable area (from the default printer's imageable area), each a `Nodus.View.*` key read by `SkiaRenderer`. Done when: each toggle changes the frame in a driven run.
- [ ] Store the bleed amount as `nodus:bleed` in the §1 document block, the value `D02 T13 §4` reads. Done when: a bleed of 3 mm survives reopen.
- [ ] Add Add Page Frame, which creates a page-sized rectangle as one command. Done when: the rectangle's bounds equal the page's.
- [ ] Add the Page Background dialog: none, solid color, or bitmap (linked path or embedded data URI, tiled default size or custom H and V with aspect lock), plus Print and Export Background. Done when: `PageBackgroundTests` cover each kind.
- [ ] Write the background as `<nodus:background>` plus a fallback `<rect>` or `<image>` in a locked `nodus:role="background"` group, and honor Print and Export Background in the `D02 T04 §3` and `D02 T04 §4` exporters. Done when: a PNG export with Export Background off omits it.
- [ ] Add Insert Page (count, before or after, size, orientation), Insert Before and After from the tab and label menus, and the New Page button, each one command. Done when: `PageCommandTests.InsertPages` cover each placement.
- [ ] Add Duplicate Page (layers only or with contents) and Duplicate to a new document named after the page. Done when: the new document opens untitled with the page's name and content.
- [ ] Add Delete Page (one, a range with Through, or the panel selection), Rename Page, Go to Page, and find page by name. Done when: deleting pages 2 through 4 of six leaves three and undo restores all six.
- [ ] Add `PageNumberField` in `src/Nodus/Photon.Nodus.Core/Pages/PageNumberField.cs` as a live text run (a §1 kind `pagenumber`) that renders its page's number and writes its current text as the fallback. Done when: `PageNumberFieldTests.RenumbersAfterReorder` passes. Cheaper substitute: static number text.
- [ ] Add Page Number Settings (Arabic, Roman, letters, start number) stored in the document block. Done when: a start of 5 in Roman numbers the first page V.
- [ ] Add Insert Page Number on the active layer, all pages, odd pages, or even pages, placing it on a master layer (§5 `MasterScope`), and hide it on one page through §5's Show Master Layers on Pages flag. Done when: odd-page numbers appear only on odd pages and hiding page 3's leaves the others.
- [ ] Add the document navigator strip under the canvas: first, previous, next, last, page tabs with add buttons. Done when: every button has a tooltip and an automation name, and a keyboard-only pass navigates all pages.
- [ ] Add list or grid page thumbnails with a size slider to the §3 panel. Done when: the slider size is a `Nodus.Pages.ThumbnailSize` key restored after restart.
- [ ] Commit a four-page fixture `tests/fixtures/nodus/pages/four-pages-background.svg` with a bitmap background and page numbers, plus its Inkscape golden. Done when: `PageFidelityTests` reopen it equal element by element.
- [ ] Extend the Pages page in `docs/user/nodus/` with views, backgrounds, numbering, and navigation. Done when: every dialog named above has a paragraph.
- [ ] Commit: `"nodus: multipage views, page backgrounds, live page numbers, and page navigation"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~PageNumberFieldTests|FullyQualifiedName~PageLayoutServiceTests|FullyQualifiedName~PageFidelityTests"` exits 0 and the four-page fixture round-trips element by element with its bitmap background and page numbers; a driven run of each view mode is captured. Cheaper substitute that fails: static number text, which `RenumbersAfterReorder` catches.

## 5. Layer Options, Sublayers, Master Layers, Lock and Hide Commands, and the Objects Panel

Layers exist as a class but not in the document; the `D02 T02 §6` panel is a list over elements. This section makes layers part of the model with sublayers and master layers, adds every lock, hide, move, merge, collect, and release command, and replaces the list with one Objects panel tree of pages, layers, and objects built on the `D02 T06 §7` tree control. It must not lose any 0.1.0 document: elements with no layer land on a default layer. Catalog: NP-0096 to NP-0135 (the lock and hide set, layer color, new layer and sublayer, Layer Options, per-layer outline, template layers, printable and exportable toggles, move and copy to layer, duplicate, delete, merge, flatten, collect, release, reverse, panel Hide Others, locate object, find and filter, panel options, group by drag, the Objects panel tree and its views, master layers, change layer to master or local, default and active layers, select activates layer, delete empty layers, show master layers on pages, fully expand, edit across layers, copy and paste a layer, and keep desktop objects on their layer).

**Fidelity:** The Objects panel, Layer Options dialog, Object, Lock and Hide submenus -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/objects-panel/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/LayersRow/README.md, docs/design/components/ListTree/README.md, docs/design/components/Dialog/README.md, docs/design/components/Menu/README.md, docs/design/components/ContextMenu/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: The Objects panel, Layer Options dialog, Object, Lock and Hide submenus -- docs/captures/nodus/main-window/ for the panel dock; new captures to docs/captures/nodus/objects-panel/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can organize, find, lock, hide, and restructure layers and objects. Consumer: the document, the renderer, the SVG writer, export, and print.
**Treatment:** one tree (pages, layers, sublayers, groups, objects) with eye, lock, print, and color columns and a target circle. Cheaper substitute that fails the checkpoint: a flat list with an indent.
**Chrome:** consume the `D02 T06 §7` layer tree control, the icon catalog, and the suite history. Do not build a second tree.

**Requires:** display-session -- panel drag, search, and per-layer view need an interactive desktop

- [ ] Add `VectorDocument.Layers` from the existing `Layer` class with sublayers, per-page local layers, document master layers (`MasterScope` All, Odd, Even), a default layer per new page, and an `ActiveLayer`. Done when: a 0.1.0 fixture opens with its elements on one default layer.
- [ ] Write layers as `<g nodus:layer="..." inkscape:groupmode="layer" inkscape:label="...">` so Inkscape shows them as layers, and read both forms. Done when: `LayerSerializationTests` round-trip layers, sublayers, and master scopes.
- [ ] Add the Layer Options dialog `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/LayerOptionsDialog.xaml`: name, color, template (locked, dimmed by percent, non-printing), show, preview or outline, lock, print, export, dim images, applied by one `LayerOptionsCommand`. Done when: every option survives reopen and undo restores the previous options.
- [ ] Add New Layer, New Sublayer, Duplicate, Delete, and Delete Empty in `src/Nodus/Photon.Nodus.Core/Commands/Layers/`, each one step with one Information line. Done when: `LayerCommandTests` prove each and its undo.
- [ ] Add Copy Layer and Paste Layer, Move to Layer, and Copy to Layer. Done when: moving three objects to a locked layer is refused naming the layer.
- [ ] Add Merge Selected, Flatten Artwork, and Collect in New Layer. Done when: merging two layers keeps stacking order and undo restores both.
- [ ] Add Release to Layers (Sequence and Build) and Reverse Order. Done when: Build on three objects yields layers holding one, two, and three objects.
- [ ] Add Change Layer To master or local, and master-layer placement on all, odd, or even pages. Done when: `MasterLayerTests` place content on odd pages only and a document reopens with the scope.
- [ ] Add the lock and hide set as one command family in `src/Nodus/Photon.Nodus.Core/Commands/Layers/LockHideCommands.cs`: 1. Lock Selection (Ctrl+2), Lock All Artwork Above, Lock Other Layers, Lock All Deselected, Unlock All (Alt+Ctrl+2). 2. Hide Selection (Ctrl+3), Hide All Artwork Above, Hide Other Layers, Hide Unselected, Show All (Alt+Ctrl+3). 3. Register the gestures in the `D02 T02 §8` keymap. Done when: `LockHideCommandTests` cover all ten and each undo, and `ShortcutsViewModelTests` list the gestures.
- [ ] Add per-layer outline or wireframe (Ctrl-click the eye) read by the §12 view-mode renderer per layer, and layer color tinting the selection bounding box and nodes. Done when: an outline layer beside a preview layer renders as a committed pixel golden.
- [ ] Route every print and export decision through one `Layer.IsPrintable` and `Layer.IsExportable` check consumed by the `D02 T04 §3` and `D02 T04 §4` exporters (and later `D02 T13 §2`). Done when: a non-printing layer is absent from a PDF export and present in the SVG.
- [ ] Add template layers (locked, dimmed by percent, non-printing) and View, Show and Hide Template layers read by §12. Done when: a template layer renders dimmed and is absent from export.
- [ ] Add `ObjectsPanelViewModel` in `src/Nodus/Photon.Nodus.Desktop/ViewModels/` over pages, layers, and objects with two views (Layers and Objects, or Pages, Layers, and Objects). Done when: `ObjectsPanelViewModelTests` build both trees for a two-page fixture.
- [ ] Add `ObjectsPanel.xaml` with eye, lock, print, and color columns and a target circle, replacing the `D02 T02 §6` list. Done when: the old `ItemsControl` panel is deleted and the capture is committed. Cheaper substitute: a flat list with an indent.
- [ ] Add drag to reorder, drag onto a group to group, and fully expand on Ctrl+click in the panel, each drag one command. Done when: a driven drag reorders and undo restores.
- [ ] Add Locate Object and Expand to Show Selection. Done when: selecting a nested object on canvas and invoking Locate scrolls to and highlights its row.
- [ ] Add search and filter by name and type, a thumbnail size slider, and Panel Options (row size, show thumbnails). Done when: `ObjectsPanelViewModelTests.FilterByType` passes and the options survive restart.
- [ ] Add panel-menu Hide Others, Outline Others, and Lock Others. Done when: each is one command with undo.
- [ ] Add setting `Nodus.Objects.EditAcrossLayers` read by `SelectionManager` and `Nodus.Objects.SelectActivatesLayer` read by the Objects panel. Done when: with edit-across off, a marquee selects only on the active layer.
- [ ] Add `Nodus.Objects.KeepDesktopObjectsOnLayer`, `Nodus.Objects.ShowMasterLayersOnPages` (read by §4 page numbers), and `Nodus.Objects.PasteRemembersLayers` (read by §13), each logged on change. Done when: each has a test proving its consumer changes behavior.
- [ ] Commit `tests/fixtures/nodus/layers/master-and-sublayers.svg` with an Inkscape golden and version. Done when: Inkscape shows the layers (version quoted).
- [ ] Add a Layers and the Objects panel page to `docs/user/nodus/`. Done when: every command above is named with its shortcut.
- [ ] Commit: `"nodus: layers in the document model, master layers, and the Objects panel"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~LayerSerializationTests|FullyQualifiedName~LayerCommandTests|FullyQualifiedName~MasterLayerTests|FullyQualifiedName~ObjectsPanelViewModelTests"` exits 0, `master-and-sublayers.svg` reopens with layers, sublayers, master scopes, and lock and print flags equal, and Inkscape shows the layers (version quoted). Cheaper substitute that fails: layers as plain named groups, which the master-scope and print-flag assertions catch.

## 6. Selection: the Select Menu, Select Same, Magic Wand, Lasso, and Saved Selections

`D02 T02 §3` gives selection one owner; this section gives it every way in both competitors to fill that owner: the full Select menu, Select Same and Select Object queries with tolerances, the magic wand, lasso, and group selection tools, saved selections and Corel selection groups, and the selection tool's modifiers. It must not add a second selection store. Catalog: NP-0149 to NP-0183 (group selection, the magic wand and its options, lasso and freehand pick, enclosure modes, select behind, skip effect bounds, Select All on the active artboard, Deselect, Reselect, Inverse, Next Above and Below, every Select Same and Select Object query, Global Edit, saved selections, the last-used and temporary selection tools, Objects panel target, bounding box show and reset, Tab cycling, select inside a group, and selection groups 0 to 9).

**Fidelity:** Select menu, Magic Wand panel, Lasso and Group Selection tools, Edit Selection dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/selection/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Panel/README.md, docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/Canvas/README.md, docs/design/components/Slider/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Select menu, Magic Wand panel, Lasso and Group Selection tools, Edit Selection dialog -- docs/captures/nodus/main-window/ for the menu; new captures to docs/captures/nodus/selection/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can select exactly the objects they mean by attribute, shape, region, or saved set. Consumer: `SelectionManager` and every command that acts on the selection.
**Treatment:** Select Same over a comparer per attribute with tolerances. Cheaper substitute that fails the checkpoint: Select Same matching exact color strings only.
**Chrome:** consume `SelectionManager`, the keymap, and the §2 index. Do not add a second selection store.

**Requires:** display-session -- lasso, magic wand, and modifier clicks on the canvas need an interactive desktop

- [ ] Add `SelectionQueries` in `src/Nodus/Photon.Nodus.Core/Selection/SelectionQueries.cs` with Select Same: Appearance, Appearance Attribute, Graphic Style, Blending Mode, Fill and Stroke, Fill Color, Opacity, Stroke Color, Stroke Weight, Shape, Symbol Instance, Link Block Series, and Font Family, Style, Size, Fill, and Stroke text variants, each with a tolerance. Done when: `SelectionQueriesTests` cover every variant; kinds whose feature lands later (`D02 T09 §15`, `D02 T09 §16`, `D02 T10 §2`) return empty and stay enabled.
- [ ] Add Select Object queries to the same class: All on Same Layers, Direction Handles, Brush Strokes, Clipping Masks, Stray Points, All Text, Point Type, Area Type, and Not Aligned to Pixel Grid. Done when: each query has a fixture test.
- [ ] Add Select, All on Active Artboard (Ctrl+Alt+A), Deselect (Shift+Ctrl+A), and Inverse. Done when: each is a menu item with its gesture in the keymap.
- [ ] Add Reselect (Ctrl+6) repeating the last Same or Object query. Done when: after Select Same Fill Color, adding a red object and Reselect includes it.
- [ ] Add Next Object Above and Below (Alt+Ctrl+] and [) using the z-order under the current selection. Done when: a test walks three stacked objects both ways.
- [ ] Add `MagicWandTool` (Y) in `src/Nodus/Photon.Nodus.Core/Tools/MagicWandTool.cs` and the Magic Wand panel: fill color, stroke color, stroke weight, opacity with tolerances, blending mode, and Use All Layers, stored as `Nodus.MagicWand.*`. Done when: a driven wand click selects the fixture's near-red objects within tolerance 20 and the log line is quoted.
- [ ] Add `LassoSelector` in `src/Nodus/Photon.Nodus.Core/Selection/` (polygon containment against node positions or bounds through the §2 index) shared by `LassoTool` (Q) and the freehand pick. Done when: `LassoSelectorTests` select exactly the objects inside a star-shaped lasso.
- [ ] Add the Group Selection tool that adds the next enclosing group on each click. Done when: three clicks on a nested object select the object, its group, and the outer group.
- [ ] Add marquee enclosure modes: E while dragging selects only fully enclosed objects, Alt switches to touching. Done when: `MarqueeModeTests` assert both sets on one fixture.
- [ ] Add select behind or hidden objects (Alt+click, or Ctrl+click twice) and select inside a group (Ctrl+click). Done when: a test selects the lower of two overlapping objects.
- [ ] Add Tab and Shift+Tab object cycling, the temporary selection tool (hold Ctrl), Space toggling the pick tool, and Ctrl+` returning to the last-used selection tool. Done when: `SelectionModifierTests` cover each.
- [ ] Add `Nodus.Selection.IgnoreEffectBounds` read by hit testing so shadows and effect bounds are skipped. Done when: clicking a shadow's extent with the setting on selects nothing.
- [ ] Add Save Selection and Edit Selection (rename, delete) stored as `<nodus:selection>` in the §1 document block, with the Edit Selection dialog. Done when: `SavedSelectionTests.RoundTrips` restores a saved selection after reopen.
- [ ] Add Corel selection groups: Ctrl+0 to 9 assign, the digit recalls, the digit twice zooms, Alt+digit adds, stored beside saved selections. Done when: a test assigns group 3, reopens, and recalls it.
- [ ] Add Start Global Edit: select objects matching the chosen one by appearance and size within the chosen artboards, with edits applied as one composite command. Done when: recoloring one of five matching objects under Global Edit recolors all five in one undo step.
- [ ] Add View, Hide or Show Bounding Box (Shift+Ctrl+B) as `Nodus.View.BoundingBox`, and Object, Transform, Reset Bounding Box re-aligning a rotated element's box as one command. Done when: a rotated rectangle's box is axis-aligned to its rotation after reset.
- [ ] Wire the Objects panel target circle (§5 when present, otherwise the `D02 T02 §6` list) to select the row's contents. Done when: clicking a layer's target selects every object on it.
- [ ] Add a Selection page to `docs/user/nodus/`. Done when: every query, tool, and gesture is listed.
- [ ] Commit: `"nodus: the full Select menu, Select Same, magic wand, lasso, and saved selections"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~SelectionQueriesTests|FullyQualifiedName~SavedSelectionTests|FullyQualifiedName~LassoSelectorTests"` exits 0; a driven magic-wand and lasso run quotes its log lines. Cheaper substitute that fails: exact-match Select Same, which the tolerance tests catch.

## 7. Isolation Mode and Focus Mode

Illustrator's isolation mode and CorelDRAW's Focus mode are the same job: edit inside a nested group without disturbing anything else. This section builds one mode that serves both, as view state rather than a document edit. It must not change the layer tree: entering and exiting write no history. Catalog: NP-0136 to NP-0143 (enter and exit, dimming, the breadcrumb bar, the isolated group in the Objects panel, step out one level, new objects join the group, which objects can be isolated, and double-click entry).

**Fidelity:** Isolation breadcrumb bar at the canvas top-left, Edit, Bring into Focus and Exit -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/isolation/.
**Design:** docs/design/components/Canvas/README.md, docs/design/components/Button/README.md, docs/design/components/Menu/README.md, new surface: docs/design/components/NodusIsolationBar/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Isolation breadcrumb bar at the canvas top-left, Edit, Bring into Focus and Exit -- new build, no baseline; captured to docs/captures/nodus/isolation/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can edit inside a nested group without disturbing the rest. Consumer: hit testing, the renderer, drawing tools, and the Objects panel.
**Treatment:** dimmed surroundings with an adjustable overlay and a clickable path of group names. Cheaper substitute that fails the checkpoint: locking every other object, which leaves the layer tree changed.
**Chrome:** consume the canvas overlay layer, the theme, and the Objects panel. Do not add a second tree view.

**Requires:** display-session -- double-click entry and the breadcrumb need an interactive desktop

- [ ] Write the design spec `docs/design/components/NodusIsolationBar/README.md` and its `docs/design/components/NodusIsolationBar/preview.html` card (anatomy, every state, tokens, sizes) before any XAML is written, and regenerate the design page. Done when: the spec exists and `python scripts/build-design-site.py --check` passes.
- [ ] Add `IsolationState` in `src/Nodus/Photon.Nodus.Core/Selection/IsolationState.cs`, one per document scope (`D02 T06 §7`), holding the isolated container path and writing no history. Done when: `IsolationStateTests.EnterExitWritesNoHistory` passes.
- [ ] Add entry by double-clicking a group with the selection tool (`Nodus.Isolation.DoubleClickEnters`, true), Edit, Bring into Focus, and Isolate Selected Group from the context and Objects panel menus. Done when: each entry path enters the same state.
- [ ] Add exit with Shift+Esc, double-click outside, or Exit, and Esc stepping up one level. Done when: `IsolationStateTests.StepUp` walks out of a three-level nest one level per Esc.
- [ ] Filter hit testing, marquee, Select All, and snapping to the isolated container through a predicate on the §2 index queries. Done when: a marquee across the whole canvas while isolated selects only the container's children.
- [ ] Add `Nodus.Isolation.OverlayOpacity` (percent) and `Nodus.Isolation.InactiveVisibility` (dim, hide, normal) read by `SkiaRenderer`. Done when: each value renders a committed capture under `docs/captures/nodus/isolation/`.
- [ ] Add the breadcrumb bar listing document, layer, and each nested group, with clicking a level moving isolation there. Done when: the bar's buttons have automation names and a keyboard-only pass reaches each.
- [ ] Insert new objects drawn while isolated into the isolated container. Done when: `IsolationStateTests.NewElementJoinsIsolatedGroup` passes. Cheaper substitute: drawing onto the active layer outside the group.
- [ ] Highlight the focus container in the Objects panel. Done when: the row carries the isolated style in a driven capture.
- [ ] Allow groups, symbols in edit mode (`D02 T06 §11`), compound paths, clipping groups, and text on a path to be isolated; refuse locked or hidden containers with a status message naming the reason. Done when: isolating a locked group shows "Cannot isolate: the group is locked." and logs it.
- [ ] Add an Isolation Mode page to `docs/user/nodus/`. Done when: entry, exit, and the settings are described.
- [ ] Commit: `"nodus: isolation mode that serves as Illustrator isolation and CorelDRAW focus mode"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~IsolationStateTests"` exits 0 including `NewElementJoinsIsolatedGroup`; a driven run isolates a nested group, draws inside, exits, and saves, and the saved group holds the new element (quoted). Cheaper substitute that fails: lock-everything-else, which the Objects panel lock state exposes.

## 8. The Properties Panel and the Contextual Property Bar

Illustrator's Control panel and Properties panel and CorelDRAW's property bar and Properties docker all do one job: show and set the exact values of whatever tool or selection is active. This section builds one property bar whose template follows the tool and selection, one Properties panel, and one numeric field control with math and units. Later tools register their templates here rather than growing their own strips. Promoted from backlog B-005 (the entry left the backlog when this file was integrated). Catalog: NP-2537 to NP-2550 (math in fields, scroll-proof fields, field keys, the Properties panel, quick actions, document properties with nothing selected, the contextual property bar, the contextual task bar, scroll and tab modes, style indicators, position, size, and scale boxes, and curve properties). **Imago second consumer (2026-09-26):** `CompactNumberBox`, `UnitExpression`, and the contextual task bar host move to `Photon.UI` and `Photon.Core/Units/` in `D03 T20 §1`, Nodus consuming them unchanged. -> SOURCE: legacy-nodus-2.5

**Fidelity:** Property bar under the menu, the Properties panel, and the contextual task bar -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/property-bar/.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/Panel/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Swatches/README.md, docs/design/components/Button/README.md, new surface: docs/design/components/ContextTaskBar/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Property bar under the menu, the Properties panel, and the contextual task bar -- docs/captures/nodus/main-window/ for the existing context toolbar and properties panel; new captures to docs/captures/nodus/property-bar/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can read and set the exact values of whatever tool or selection is active. Consumer: `D02 T03 §4` property commands and every later tool's options.
**Treatment:** templates keyed by tool and selection kind. Cheaper substitute that fails the checkpoint: one static toolbar with disabled boxes.
**Chrome:** consume the `CompactNumberBox` control (moved to `Photon.UI` when Imago needs it), the theme, and `D02 T03 §4` property commands. Do not add a second numeric box.
**Corrected 2026-09-27:** the specs are `docs/design/components/NumberBox/README.md` (the scrub label, units column, focus border) and `docs/design/components/OptionsBar/README.md` for the contextual property bar.
**Corrected 2026-09-27:** `CompactNumberBox`'s template draws its field states (rest, hover, focus border plus inner line, disabled, error) from the implicit TextBox styles and `Photon.Focus.IsKeyboardInitiated` of `D01 T01 §5`, and the property bar's combo boxes and toggles use the same dictionaries; the control adds only the scrub label and the units column.

**Requires:** display-session -- template switching and field entry need an interactive desktop

- [ ] Write the design spec `docs/design/components/ContextTaskBar/README.md` and its `docs/design/components/ContextTaskBar/preview.html` card (anatomy, every state, tokens, sizes) before any XAML is written, and regenerate the design page. Done when: the spec exists and `python scripts/build-design-site.py --check` passes.
- [ ] Add `PropertyBarTemplateSelector` in `src/Nodus/Photon.Nodus.Desktop/Views/PropertyBar/PropertyBarTemplateSelector.cs` picking a template from (active tool, selection kind), with a registration API later tools call. Done when: `PropertyBarTemplateSelectorTests` cover the tool and selection matrix.
- [ ] Add the no-selection template: page size, orientation, units, and nudge distance (§3, §9, §13). Done when: with nothing selected the bar shows the four fields bound to the document.
- [ ] Add the selection template: X, Y, W, H, scale factor percent with lock ratio, and rotation, writing through `D02 T03 §4` `PropertyChangeCommand` with the reference point from the Transform panel default (center). Done when: typing a width records one undo step and undo restores it. Cheaper substitute: fields that set the element directly with no command.
- [ ] Add `UnitExpression` in `src/Nodus/Photon.Nodus.Core/Units/UnitExpression.cs` evaluating `+ - * /`, parentheses, percentages, and unit suffixes such as `10mm+2pt`. Done when: `UnitExpressionTests` assert `10mm+2pt` equals 39.4583 px at 96 DPI and `50%*2` of 200 equals 200.
- [ ] Teach `CompactNumberBox` to evaluate `UnitExpression`, step with Up and Down (Shift for ten), apply and keep focus on Shift+Enter, and apply as a copy on Alt+Enter. Done when: `CompactNumberBoxTests` cover each key.
- [ ] Make `CompactNumberBox` ignore the mouse wheel unless focused (`Nodus.Fields.WheelNeedsFocus`, true). Done when: `CompactNumberBoxTests.WheelIgnoredUnfocused` passes.
- [ ] Add `PropertiesPanelViewModel` in `src/Nodus/Photon.Nodus.Desktop/ViewModels/` with sections Document (with no selection: page, units, rulers and grid toggles, a Preferences shortcut), Transform, Appearance summary, and Curve (node count, closed, path length). Done when: `PropertiesPanelViewModelTests` show the Curve section only for paths with the right node count.
- [ ] Add the Quick Actions section: context buttons such as Expand, Group, Isolate, and Arrange per selection kind. Done when: each button runs the same command as its menu item.
- [ ] Add scroll mode and tab mode (`Nodus.Properties.Mode`) to the panel. Done when: the mode survives restart and both are captured.
- [ ] Add style indicators that mark values overriding a style. Done when: a test with a style-backed element flags the overridden fill.
- [ ] Add the contextual task bar: a floating bar near the selection with the three most likely next commands per selection kind, toggled by `Nodus.View.ContextualTaskBar`. Done when: the bar follows the selection in a driven run and hides when toggled off.
- [ ] Retire the old context toolbar in `MainWindowView.xaml` in favor of the property bar; Illustrator's Control panel maps to it, so there are not two bars. Done when: the window has one bar and `MenuAuditTests` pass.
- [ ] Add a Property Bar and Properties Panel page to `docs/user/nodus/`. Done when: field math and the keys are documented.
- [ ] Commit: `"nodus: a contextual property bar, the Properties panel, and one numeric field with math"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~UnitExpressionTests|FullyQualifiedName~PropertyBarTemplateSelectorTests|FullyQualifiedName~CompactNumberBoxTests"` exits 0; a driven run types `50%*2` into width and undoes it (log quoted). Cheaper substitute that fails: a static bar, which the template-selector tests catch.

## 9. Rulers, Units, Drawing Scale, and Grids

Rulers and a grid already draw; what is missing is one units path every field and readout uses, a drawing scale, per-document ruler state, and the pixel, baseline, and transparency grids. It must extend `SkiaRenderer.RenderRulers` and `RenderGrid`, not replace them, and keep snap to grid as the `D02 T02 §7` toggle. Catalog: NP-0238 to NP-0253 (the transparency grid, show and hide rulers, global or artboard rulers, origin and units, video rulers, the document grid and its settings, units for general, stroke, and type, numbers without units as points, tick divisions, rulers per desktop and tablet mode, calibrate rulers, the pixel grid, align the page with the pixel grid, the baseline grid, and drawing scale). **Imago second consumer (2026-09-26):** `UnitConverter` moves to `Photon.Core` in `D03 T08 §4`, Nodus consuming it unchanged.

**Fidelity:** Rulers on the canvas with a right-click units menu, View, Rulers and Grid toggles, Document Options Rulers and Grid pages, Drawing Scale dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/rulers-grids/.
**Design:** docs/design/components/Canvas/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Rulers on the canvas with a right-click units menu, View, Rulers and Grid toggles, Document Options Rulers and Grid pages, Drawing Scale dialog -- docs/captures/nodus/main-window/ for the canvas rulers; new captures to docs/captures/nodus/rulers-grids/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can measure and lay out in the units and scale of the job. Consumer: rulers, `CompactNumberBox`, the HUD, and the exporters.
**Treatment:** units flow from one `UnitConverter` into rulers, fields, and the HUD. Cheaper substitute that fails the checkpoint: rulers in pixels only with a label.
**Chrome:** consume `SkiaRenderer.RenderRulers` and `RenderGrid` (extended, not replaced) and the settings store. Do not add a second units table.

**Requires:** display-session -- ruler interaction and grid display need an interactive desktop

- [ ] Add `UnitConverter` in `src/Nodus/Photon.Nodus.Core/Units/UnitConverter.cs` over px, pt, pc, in, mm, cm, m, ft, yd, Q, and user units under a drawing scale, the only conversion path for rulers, `CompactNumberBox`, the HUD, and exporters. Done when: `UnitConverterTests` cover every pair and a grep finds no other unit table in `src/Nodus`.
- [ ] Add settings `Nodus.Units.General`, `Nodus.Units.Stroke`, `Nodus.Units.Type`, and `Nodus.Units.NumbersWithoutUnitsArePoints` read by `UnitConverter` and `UnitExpression`. Done when: with the last on, typing `12` into a stroke field sets 12 pt.
- [ ] Add a drawing scale (for example 1 mm = 1 m) with the Drawing Scale dialog, applied by `UnitConverter` to displayed values. Done when: a 10 mm line reads 10 m at 1:1000 and the stored geometry is unchanged.
- [ ] Store ruler state in the §1 document block as `nodus:rulers` and `nodus:scale`: units, origin (global or per artboard, AI-0868), tick divisions, and drawing scale. Done when: `RulerStateSerializationTests` round-trip each.
- [ ] Add ruler interaction: Ctrl+R toggle, a right-click units menu, drag from the corner to set the origin, and double-click the corner to reset. Done when: a driven origin drag and reset is captured and each change logs one line.
- [ ] Add video rulers when an artboard has video settings (§3) and a separate show state for tablet mode (`Nodus.Rulers.ShowInTabletMode`). Done when: a video artboard shows its safe-area ruler marks.
- [ ] Add the Calibrate Rulers dialog that sets `Nodus.Rulers.ScreenDpi` from a measured on-screen length so 100 percent matches a physical ruler. Done when: the value is saved and read by §12's zoom relative to 1:1.
- [ ] Extend the document grid: show (Ctrl+'), lines or dots, spacing and subdivisions, color, and grids in back, stored as `nodus:grid` in the document block. Done when: `GridSettingsTests` round-trip each and a dots grid is captured.
- [ ] Add the pixel grid shown from 800 percent zoom with color and opacity keys, and Align Page with Pixel Grid rounding page origins to whole pixels as one command. Done when: a page at x = 10.4 moves to 10 and undo restores it.
- [ ] Add the baseline grid (spacing, start, color, show toggle) read by §11 snap to baseline grid and `D02 T10 §6`. Done when: the grid is stored in the document block and drawn in a capture.
- [ ] Add the transparency grid (Shift+Ctrl+D): a checkerboard behind artboards with size and colors as settings. Done when: toggling it is captured.
- [ ] Add a Rulers, Units, and Grids page to `docs/user/nodus/`. Done when: calibration and drawing scale are documented.
- [ ] Commit: `"nodus: rulers, one units converter, drawing scale, and the document, pixel, baseline, and transparency grids"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~UnitConverterTests|FullyQualifiedName~RulerStateSerializationTests|FullyQualifiedName~GridSettingsTests"` exits 0 (drawing scale and origin survive reopen); a driven run switching ruler units and origin is captured. Cheaper substitute that fails: a units label over pixel rulers, which the drawing-scale conversion test catches.

## 10. Guides, the Guides Panel, the Measure Tool, and the Info Panel

Guides live in `SnapManager`'s private list today, so a reopen loses them. This section moves guides into the document with angles, scope, lock, color, and presets, adds a Guides panel for numeric entry, a measure tool that writes nothing, and an Info panel. Promoted from backlog B-007 (the entry left the backlog when this file was integrated, and the `D02 T06` Adjacency reason that cited it now names this section). Catalog: NP-0254 to NP-0267 (the measure tool for distance, angle, and area with exclusions, Info panel area options, guides from the rulers, show, hide, lock, and clear, guide color and style, artboard-level and document-wide guides, the Info panel, select all guides, the Guides panel, angled guides, make and release guides, guide presets, and guides at drawing scale). -> SOURCE: legacy-nodus-3.7-3.8

**Fidelity:** Guides panel, Measure tool, Info panel, View, Guides submenu -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/guides/, docs/captures/golden/nodus/info-panel/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Canvas/README.md, docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Menu/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Guides panel, Measure tool, Info panel, View, Guides submenu -- new build, no baseline; captured to docs/captures/nodus/guides/ and docs/captures/nodus/info-panel/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can place exact guides and read exact measurements. Consumer: the document, snapping (§11), and the SVG writer.
**Treatment:** guides are document objects on a guides layer with numeric editing. Cheaper substitute that fails the checkpoint: guides kept in `SnapManager` memory, which a reopen loses.
**Chrome:** consume the §9 `UnitConverter`, the `D02 T06 §12` HUD label style, and AvalonDock panels. Do not add a second measurement readout.

**Requires:** display-session -- dragging guides from rulers and the measure tool need an interactive desktop

- [ ] Give `Guide` in `src/Nodus/Photon.Nodus.Core/Models/Guide.cs` an `Angle`, a `Scope` (document or a page id), `IsLocked`, a color, and a style, and move the list from `SnapManager._guides` to `VectorDocument.Guides`. Done when: `SnapManager` holds no guide list and its tests read the document's.
- [ ] Write guides as `<nodus:guide>` in the §1 document block and as Inkscape `sodipodi:guide` elements for interop, reading either. Done when: `GuideSerializationTests` round-trip both forms.
- [ ] Add Add, Move, Rotate, Delete, Lock, Unlock, Clear Guides, and Select All Guides commands, one step each. Done when: `GuideCommandTests` cover each and its undo.
- [ ] Add Make Guides (Ctrl+5, object outlines become object guides) and Release Guides. Done when: making guides from a circle and releasing them yields an equal circle.
- [ ] Create a guide by dragging from a ruler (Alt switches orientation): dropped inside an artboard it is artboard-level, outside document-wide (`Nodus.Guides.ArtboardLevelOnDrop`). Done when: a driven drag onto an artboard creates a page-scoped guide.
- [ ] Add Show and Hide (Ctrl+;) and Lock (Alt+Ctrl+;) as `Nodus.View.Guides*` keys read by `SkiaRenderer` and the §11 snap engine. Done when: hidden guides neither render nor snap.
- [ ] Add `GuidesPanelViewModel` and `GuidesPanel.xaml`: type (horizontal, vertical, angled by two points or angle), numeric position in current units, a list with select, move, rotate, delete, lock, color, and line style, and show guides at drawing scale. Done when: typing 25 mm adds a guide at 94.488 px and the panel is captured.
- [ ] Add guide presets: built-in margins, columns, and grid, plus user-defined presets saved to `Nodus.Guides.Presets`. Done when: applying a three-column preset adds the expected six guides.
- [ ] Add `MeasureTool` in `src/Nodus/Photon.Nodus.Core/Tools/MeasureTool.cs` on the eyedropper flyout: click-drag measures distance and angle, results on the HUD and in the Info panel, and the tool records no command. Done when: `MeasureToolTests.NoHistoryEntry` passes.
- [ ] Add area measurement: Shift-click builds a polygon, Shift-click inside it adds exclusions. Done when: `MeasureToolTests.AreaWithExclusion` equals a known polygon area minus its hole.
- [ ] Add `InfoPanelViewModel` and `InfoPanel.xaml`: cursor X and Y, selection X, Y, W, H, rotation, path length, area, fill and stroke summary, and measure-tool results. Done when: `InfoPanelViewModelTests` read a known rectangle's values in current units.
- [ ] Add Info panel Area Options: units and whether holes subtract. Done when: toggling hole subtraction changes a ring's area in the test.
- [ ] Commit `tests/fixtures/nodus/guides/angled-and-artboard.svg` with an Inkscape golden and version. Done when: Inkscape shows the guides (version quoted).
- [ ] Add a Guides and Measurement page to `docs/user/nodus/`. Done when: the tool, both panels, and presets are covered.
- [ ] Commit: `"nodus: guides in the document, the Guides panel, the measure tool, and the Info panel"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~GuideSerializationTests|FullyQualifiedName~GuideCommandTests|FullyQualifiedName~MeasureToolTests"` exits 0, `angled-and-artboard.svg` reopens with guides equal, Inkscape shows them (version quoted), and `MeasureToolTests.AreaWithExclusion` passes. Cheaper substitute that fails: in-memory guides, which the reopen comparison catches.

## 11. Snapping Modes, Smart Guides, and Dynamic and Alignment Guides

`SnapManager` snaps to grid, guides, and objects. Parity needs every point mode both competitors ship, smart guides with labels and spacing, and Corel's dynamic and alignment guides, all through one engine that ranks candidates found through the §2 index. It must keep the `D02 T02 §7` toggles working and stay under 2 ms per mouse move on the 10,000-element fixture. Natural split if it overruns 30 items: the Corel dynamic and alignment guide providers (not needed at authoring). Catalog: NP-0268 to NP-0307 (snap to pixel, point and node, endpoint, midpoint, center, quadrant, intersection, tangent, perpendicular, edge, text baseline, page, baseline grid, and self, the quick access menu, smart guides and every smart guide kind, equal spacing and distance guides, snap to last location, construction guide angles, tolerance, snap within the active artboard or isolated group, snapping off, automatic alignment, hold Q to suspend, dynamic guides and their options, the Live Guides panel, screen tips, alignment guides and their options, and snap location marks). **Imago second consumer (2026-09-26):** the snapping core moves to `Photon.Core` in `D03 T08 §4`, Nodus consuming it unchanged.

**Fidelity:** View, Snap To submenu, the snapping quick-access menu on the property bar, the Live Guides panel, and canvas overlays -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/snapping/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Panel/README.md, docs/design/components/Canvas/README.md, docs/design/components/Checkbox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: View, Snap To submenu, the snapping quick-access menu on the property bar, the Live Guides panel, and canvas overlays -- docs/captures/nodus/main-window/ for the menu; new captures to docs/captures/nodus/snapping/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can land a point exactly on the geometry they mean and see why it snapped. Consumer: every drawing and transform tool.
**Treatment:** every candidate names its mode in a screen tip and draws its mark. Cheaper substitute that fails the checkpoint: bounding-box snapping labeled as point snapping.
**Chrome:** consume the canvas overlay, the `guide-smart` canvas token (**Corrected 2026-09-27:** said the theme accent), the §2 index `Nearest`, and the `D02 T02 §7` toggles. Do not add a second snap engine.

**Requires:** display-session -- snapping feedback during drags needs an interactive desktop

- [ ] Replace `SnapTarget` with `SnapMode` flags in `src/Nodus/Photon.Nodus.Core/Snapping/SnapMode.cs`, keeping Grid, Guides, and Objects and adding Node, Endpoint, Midpoint, Center, Quadrant, Intersection, Tangent, Perpendicular, Edge, TextBaseline, Page, Pixel, BaselineGrid, and Self. Done when: the old enum is gone and the `D02 T02 §7` toggle tests pass against the new flags.
- [ ] Add one `SnapSettings` reading a `Nodus.Snap.<Mode>` key per mode. Done when: `SnapSettingsTests` round-trip every key.
- [ ] Add `NodeSnapProvider` (nodes, endpoints, midpoints, centers, quadrants) in `src/Nodus/Photon.Nodus.Core/Snapping/`. Done when: `SnapProviderTests.Node` finds each point kind on a circle and a path.
- [ ] Add `IntersectionSnapProvider` over segment intersections within the §2 query window. Done when: two crossing Bezier curves yield their analytic intersection within 1e-6.
- [ ] Add `TangentSnapProvider` and `PerpendicularSnapProvider` relative to the drag origin. Done when: the tangent from an external point to a circle lands on the analytic tangent point within 1e-6.
- [ ] Add `EdgeSnapProvider`, `PageSnapProvider`, `PixelSnapProvider`, and `BaselineSnapProvider` (the §9 baseline grid and text baselines). Done when: each has a fixture test.
- [ ] Rank candidates in `SnapManager` by screen distance, then mode priority, within `Nodus.Snap.RadiusPx`. Done when: `SnapRankingTests` prefer an endpoint over an edge at equal distance.
- [ ] Add global controls: Snap Off (Alt+Q) and its toolbar toggle, hold Q to suspend for one drag, snap to self (Ctrl+Shift+H), snap only within the active artboard, snap only to isolated objects (§7), and snap to last location. Done when: `SnapControlsTests` cover each.
- [ ] Draw snap marks per mode and screen tips naming the mode (`Nodus.Snap.ShowScreenTips`) in the overlay renderer. Done when: a driven drag captures each mode's tip under `docs/captures/nodus/snapping/`. Cheaper substitute: one generic mark for every mode.
- [ ] Add the snapping quick-access menu on the property bar listing every mode with a check. Done when: toggling a mode there changes its key and logs one line.
- [ ] Add `SmartGuideProvider` (Ctrl+U) with object and alignment guides, anchor and path labels, object highlighting, and measurement labels. Done when: `SmartGuideProviderTests.AlignsToCenter` passes.
- [ ] Add transform-tool smart guides, equal spacing guides, distance guides, and construction guides at up to six angles with a tolerance. Done when: `SmartGuideProviderTests.EqualSpacing` among three objects passes.
- [ ] Add glyph guides fed by `D02 T10 §5` when present, and the `Nodus.SmartGuides.*` preference keys. Done when: every smart-guide key has a named reader.
- [ ] Add `DynamicGuideProvider` (Shift+Alt+D): angles and custom angles, extend along a segment, tick spacing, intersection placement, a snap point queue of recent points, and line style and color. Done when: `DynamicGuideProviderTests` snap to a tick along a 30-degree guide.
- [ ] Add `AlignmentGuideProvider` (Shift+Alt+A): edges, centers, individual objects in a group, margins, intelligent spacing and dimensioning, and line style and color. Done when: `AlignmentGuideProviderTests` align to a group member's edge.
- [ ] Add `LiveGuidesPanelViewModel` and `LiveGuidesPanel.xaml` over the dynamic and alignment guide keys, plus the automatic alignment toggle on the toolbar. Done when: the panel is captured and each control writes its key.
- [ ] Add `SnapBenchmark` to `tests/Photon.Nodus.Benchmarks/` measuring candidate search per mouse move on the §2 10,000-element fixture. Done when: the benchmark reports under 2 ms.
- [ ] Add a Snapping page to `docs/user/nodus/`. Done when: every mode, guide kind, and shortcut is listed.
- [ ] Commit: `"nodus: every snapping mode, smart guides, and dynamic and alignment guides"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~SnapProviderTests|FullyQualifiedName~SmartGuideProviderTests|FullyQualifiedName~DynamicGuideProviderTests"` exits 0 (tangent from an external point to a circle within 1e-6); `SnapBenchmark` reports under 2 ms; a driven drag with each mode's screen tip is captured. Cheaper substitute that fails: bounds-only snapping, which the tangent and intersection tests catch.

## 12. View Modes, Zoom Commands, Rotate View, Saved Views, and Document Windows

Every view mode both competitors ship, the full zoom and pan set, rotate view, saved views, and window arrangement, all as view state per window that never writes history. It must keep hit testing and rulers correct under rotation and must not add a second zoom model beside `CanvasState`. Natural split if it overruns 30 items: document windows (not needed at authoring). Catalog: NP-0197 to NP-0237 (hand tool and pans, rotate view, the zoom tool and commands, fit commands, actual size, zoom to selection, outline, trim, presentation, screen modes, edge, artboard, template layer, gradient annotator, and corner widget toggles, saved views, new window, animated zoom, undock, cascade and tile, window list, page width and height, zoom levels, wheel behavior, scroll bars, full-screen preview, preview selected only, normal, enhanced, simple wireframe, and draft views, previous view mode, close window, tabbed documents, text zoom, zoom tool right-click action, zoom relative to 1:1, center mouse on zoom, zoom rates, and the default view mode).

**Fidelity:** View menu, Window menu, Zoom tool property bar, zoom levels list, Views panel, screen modes -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/view-modes/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/DocumentTabs/README.md, docs/design/shell-layout.md#nodus-vector -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: View menu, Window menu, Zoom tool property bar, zoom levels list, Views panel, screen modes -- docs/captures/nodus/main-window/ for the menus; new captures to docs/captures/nodus/view-modes/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can see the document the way the task needs and get anywhere in it fast. Consumer: the canvas and every window on a document.
**Treatment:** view state per window, never written to history. Cheaper substitute that fails the checkpoint: outline mode as zero-width strokes on the real renderer.
**Chrome:** consume `CanvasState`, the keymap, AvalonDock windows from `D02 T06 §7`, and the settings store. Do not add a second zoom model.

**Requires:** display-session -- view modes, zoom, rotation, and window arrangement need an interactive desktop

- [ ] Add `ViewMode` (Normal, Enhanced, Draft, Outline, SimpleWireframe) to `CanvasState` with one renderer strategy per mode in `SkiaRenderer`: outline draws geometry at 1 px with no fills or effects, draft skips effects and bitmap quality, enhanced enables full anti-aliasing and high-quality bitmaps. Done when: `ViewModeRendererTests` match a committed outline pixel golden within 1/255. Cheaper substitute: hairline strokes over fills.
- [ ] Add Ctrl+Y toggling Outline, Shift+F9 toggling the previous mode, and `Nodus.View.DefaultMode` for new documents. Done when: each gesture is in the keymap and the default is read by `DocumentFactory`.
- [ ] Add Trim view (clip to artboards) and Preview Selected Only. Done when: both are captured.
- [ ] Add Presentation Mode (one artboard full screen with arrow navigation) and screen modes (F cycles normal, full screen with menu, full screen). Done when: Esc leaves each and a driven run captures them.
- [ ] Add Full-screen Preview (F9) in normal or enhanced (`Nodus.View.FullScreenPreviewMode`). Done when: the setting changes the preview's renderer.
- [ ] Add `ZoomCommands` in `src/Nodus/Photon.Nodus.Desktop/ViewModels/ZoomCommands.cs`: In, Out, To Selection, To All Objects, To Page and Fit Artboard, To All Pages, Page Width, Page Height, and Actual Size (Ctrl+1). Done when: `ZoomCommandsTests` check each fit against known bounds, including under rotation.
- [ ] Add the zoom levels list box on the property bar and zoom relative to 1:1 using the §9 calibrated DPI. Done when: choosing 100 percent at calibrated DPI shows a 10 mm line as 10 physical mm (value computed in a test).
- [ ] Add animated zoom (`Nodus.Zoom.Animated`), honoring the Windows animation-effects setting. Done when: with animation effects off the zoom jumps.
- [ ] Add mouse and pan preferences: wheel default action zoom or scroll, center mouse when zooming, zoom rate and alternate (Ctrl+Shift) rate, the right-click action of the zoom and pan tools, and scroll bars, each a `Nodus.Zoom.*` or `Nodus.View.*` key. Done when: each key has a named reader and a test.
- [ ] Keep middle-button quick pan and Space pan from `D02 T02 §8` and the hand tool. Done when: the existing pan tests still pass.
- [ ] Add the Rotate View tool (Shift+H), View, Rotate View presets, Reset, and Rotate View to Selection, with `CanvasState.Rotation` in the view matrix. Done when: `RotateViewTests` prove hit testing and ruler values stay correct at 30 degrees.
- [ ] Add show and hide toggles as `Nodus.View.*` keys: edges (Ctrl+H), artboards, template layers, gradient annotator (read by `D02 T09 §8`), and corner widget (read by `D02 T08 §4`). Done when: each toggle has a menu item and a named reader.
- [ ] Add New View and Edit Views with the Views panel (zoom, center, rotation, page, view mode), stored as `<nodus:view>` in the §1 document block. Done when: `SavedViewTests` round-trip a view and recalling it restores all five values.
- [ ] Add Window, New Window on the same document sharing its scope (`D02 T06 §7`). Done when: an edit in one window renders in the other.
- [ ] Add Cascade, Tile Horizontally and Vertically, Arrange Icons, undock a document, the window list, Close Window, and the tabbed documents toggle. Done when: each is a Window menu item driven in a captured run.
- [ ] Add text zoom controls (CD-183) scaling text readability in the text editing overlay without changing document zoom, as `Nodus.View.TextZoom`. Done when: changing it leaves `CanvasState.Zoom` unchanged in a test.
- [ ] Add a View Modes and Navigation page to `docs/user/nodus/`. Done when: every mode and shortcut is listed.
- [ ] Commit: `"nodus: every view mode, the zoom and pan set, rotate view, saved views, and window arrangement"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~ZoomCommandsTests|FullyQualifiedName~ViewModeRendererTests|FullyQualifiedName~SavedViewTests|FullyQualifiedName~RotateViewTests"` exits 0, with the outline-mode pixel golden within 1/255; a driven run of each view mode is captured. Cheaper substitute that fails: outline as hairline strokes over fills, which the pixel golden catches.

## 13. History Panel, Repeat, Paste Variants, and Quick Duplicates

Undo exists; seeing and jumping through it, repeating the last command, and placing pastes and duplicates exactly are what parity adds. Everything reads the `D01 T02 §4` suite history and the `D02 T03 §3` clipboard service; nothing adds a second stack. Catalog: NP-0312 to NP-0326 (Alt-drag duplicate, paste in front and back, paste in place, paste on all artboards, paste without formatting, paste remembers layers, the History panel, nudge distances, the right-drag menu, Repeat, Paste Special, drop a copy while dragging, keypad duplicate in place, move a shape while drawing, and duplicate offset).

**Fidelity:** History panel, Edit menu additions, right-drag drop menu -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/history-panel/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Menu/README.md, docs/design/components/ContextMenu/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: History panel, Edit menu additions, right-drag drop menu -- docs/captures/nodus/main-window/ for the Edit menu; new captures to docs/captures/nodus/history-panel/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can step back to any earlier state and duplicate or paste exactly where they need. Consumer: the suite history and the clipboard service.
**Treatment:** the panel lists history entries by description with the current state marked; clicking jumps by undoing or redoing to it. Cheaper substitute that fails the checkpoint: a panel that only displays descriptions.
**Chrome:** consume the `D01 T02 §4` history, the `D02 T03 §3` clipboard service, and the keymap. Do not add a second undo stack.

**Requires:** display-session -- panel jumps, drag duplicates, and paste placement need an interactive desktop

- [ ] Add `HistoryPanelViewModel` in `src/Nodus/Photon.Nodus.Desktop/ViewModels/` over the suite history's `Changed` event: rows with description and time, the current row marked, and a click jumping by a sequence of Undo or Redo. Done when: `HistoryPanelViewModelTests.JumpRestoresState` jumps back three and forward two and the document equals each recorded state. Cheaper substitute: a read-only list.
- [ ] Add `HistoryPanel.xaml` and `Nodus.History.Levels` read by the history limit. Done when: the panel is captured and lowering the level trims the oldest entries.
- [ ] Add Repeat (Ctrl+R in the Corel keymap set; Transform Again stays `D02 T08 §12`) re-executing the last repeatable command on the current selection through `IRepeatableCommand.CloneFor(selection)`. Done when: repeating a fill change on a new selection records one step.
- [ ] Add Paste in Front (Ctrl+F) and Paste in Back (Ctrl+B) relative to the selected object. Done when: `PasteVariantsTests` assert z-order for each.
- [ ] Add Paste in Place (Shift+Ctrl+V) and Paste on All Artboards (Alt+Shift+Ctrl+V, same offset per artboard). Done when: `PasteVariantsTests` assert positions for each.
- [ ] Add Paste Without Formatting (plain text into text objects) and Paste Special listing the clipboard formats present. Done when: Paste Special shows the formats of a clipboard holding SVG and text.
- [ ] Make pasting honor `Nodus.Objects.PasteRemembersLayers` from §5. Done when: with it on, a pasted object lands on its original layer.
- [ ] Add quick duplicates: Alt-drag duplicate, Space drops a copy during a drag, right-click during a drag drops a copy, and keypad plus duplicates in place, each one command. Done when: `QuickDuplicateTests` cover each.
- [ ] Add the right-drag drop menu: Move Here, Copy Here, Copy Fill Here, Copy Outline Here, Copy All Properties, Cancel. Done when: each entry is one command and Cancel records nothing.
- [ ] Add move while drawing: the right mouse button or Space repositions a shape or line during creation through a shared `DrawGestureState` in `src/Nodus/Photon.Nodus.Core/Tools/`. Done when: the rectangle and ellipse tools consult it in `DrawGestureStateTests`.
- [ ] Add nudge: arrow keys, Ctrl micro, Shift super, with `Nodus.Nudge.Distance`, `Nodus.Nudge.Micro`, and `Nodus.Nudge.Super` in document units (also on the §8 no-selection bar), and consecutive nudges merged into one history entry within the suite merge window. Done when: `NudgeTests.MergesConsecutive` passes.
- [ ] Replace the fixed 10-unit duplicate offset from `D02 T03 §3` with `Nodus.Duplicate.OffsetX` and `Nodus.Duplicate.OffsetY`. Done when: Duplicate honors a changed offset and the change logs one line.
- [ ] Add a History, Paste, and Duplicate page to `docs/user/nodus/`. Done when: every variant and gesture is listed.
- [ ] Commit: `"nodus: the History panel, Repeat, paste variants, and quick duplicates"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~PasteVariantsTests|FullyQualifiedName~HistoryPanelViewModelTests|FullyQualifiedName~NudgeTests"` exits 0; a driven History panel jump quotes its log lines. Cheaper substitute that fails: a read-only history list, which the jump test catches.

## 14. The New Document Dialog, Document Presets, Templates, and Document Information

Starting the right document in one step, describing it for whoever receives it, and the file commands both competitors ship beyond Save and Save As. One `DocumentFactory` path serves the dialog, New without Dialog, and templates; every save goes through the `D02 T04 §1` atomic writer, and a target whose file permissions refuse the write is refused by name. It must not break recent files and autosave (`D02 T04 §5`). Catalog: NP-0062 to NP-0089 (the New Document dialog and its settings, custom presets, blank templates, New without Dialog, New from Template, Save as Template, Close and Close All, Save a Copy, Revert, Document Setup and its type options, document information, color mode, rendering resolution, preset categories, page view mode, bleed, and color profiles at creation, Save Selected Only, locked-file handling, template folders, template open with or without contents, import styles from a template, the template browser, favorites, properties, delete, and Open for Editing).

**Fidelity:** New Document dialog with a Templates tab, New from Template browser, Save as Template dialog, Document Setup dialog, Document Information dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/new-document/, docs/captures/golden/nodus/templates/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: New Document dialog with a Templates tab, New from Template browser, Save as Template dialog, Document Setup dialog, Document Information dialog -- new build, no baseline; captured to docs/captures/nodus/new-document/ and docs/captures/nodus/templates/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can start the right document in one step and describe it for whoever receives it. Consumer: `DocumentFactory`, the SVG writer, and later the color and print files.
**Treatment:** preset categories on the left, details on the right, blank templates as tiles. Cheaper substitute that fails the checkpoint: a width and height prompt.
**Chrome:** consume `Photon.UI` dialog styles, the settings store, the `D02 T04 §1` save paths, and the icon catalog. Do not add a second file writer.

**Requires:** display-session -- the dialogs and the template browser need an interactive desktop

- [ ] Add `DocumentSettings` in `src/Nodus/Photon.Nodus.Core/Documents/DocumentSettings.cs` (name, page count, units, width, height, orientation, color mode RGB or CMYK, rendering resolution, bleed, RGB, CMYK, and gray profile names, rendering intent, page view mode, scale factor from §2). Done when: the record builds with XML documentation.
- [ ] Add `DocumentFactory.Create(settings)` building pages (§3) and layers (§5) as the one creation path. Done when: `DocumentFactoryTests` create a document from each built-in preset with the expected pages and default layers.
- [ ] Record color mode, profiles, and rendering intent in the §1 document block for `D02 T09 §1` and `D02 T13 §1` to consume. Done when: a CMYK document reopens with its mode and profile names.
- [ ] Add built-in presets in `DocumentPresets` (Print, Web, Mobile and Devices, Social, Film and Video, Art and Illustration, with paper types) and custom presets saved and deleted in `Nodus.NewDocument.Presets`. Done when: a saved preset survives restart (settings readback quoted).
- [ ] Add `NewDocumentDialog.xaml` and `NewDocumentViewModel`: categories left, details right, blank template tiles, and Do Not Show Again setting `Nodus.NewDocument.ShowDialog`. Done when: the dialog is keyboard operable and captured. Cheaper substitute: a width and height prompt.
- [ ] Add New without Dialog (Alt+Ctrl+N) using the last settings. Done when: the command creates a document equal to the last dialog result.
- [ ] Add templates as `.svgt` files (SVG with a `<nodus:template>` block carrying name, category, and designer notes) and Save as Template with template properties. Done when: `TemplateRoundTripTests` save and reopen a template with its block equal.
- [ ] Add New from Template (untitled copy, with or without contents) and Open for Editing (the template itself). Done when: New from Template opens untitled and Open for Editing opens the `.svgt` path.
- [ ] Add Import Styles from a Template disabled with the tooltip `Planned: D02 T09 §15`. Done when: `MenuAuditTests` accept it.
- [ ] Add `TemplateBrowserViewModel` over local folders from `Nodus.Templates.Folders` (add, alias, rename, remove, browse recursively, reindex into `%LOCALAPPDATA%\Rizonesoft\Nodus\templates-index.json`). Done when: `TemplateBrowserViewModelTests` index a nested fixture folder.
- [ ] Add browser search, category filter, sort, favorites, a thumbnail size slider, a details pane, properties, and delete to the Recycle Bin. Done when: deleting a template moves it to the Recycle Bin (confirmation names the file) and the browser is captured.
- [ ] List unreadable template folders with the refusal reason. Done when: a denied folder shows "Cannot read <path>: access denied." and logs a Warning.
- [ ] Add Document Setup (Alt+Ctrl+P) and Document Options editing units, bleed, rendering resolution, and type options (stored for `D02 T10 §2`) as one `DocumentSetupCommand`. Done when: undo restores all four values.
- [ ] Add Document Information (title, author, subject, keywords, rating, notes, tags) written to SVG `<title>`, `<metadata>` RDF with Dublin Core, and an XMP packet, read back by the importer, replacing today's `Title`, `Author`, `Description`, and `License` setters. Done when: `DocumentInfoMetadataTests` round-trip Dublin Core and XMP.
- [ ] Add Save a Copy (Alt+Ctrl+S) and Save As another registered format, and Save Selected Only, all through the `D02 T04 §1` atomic writer. Done when: Save a Copy leaves the document's path and dirty state unchanged.
- [ ] Add Revert (F12, prompts naming the file, reloads from disk) and Close All. Done when: Revert after an edit restores the saved content and Close All prompts once per dirty document.
- [ ] Refuse locked or read-only save targets by name through `D02 T04 §1` with Save As offered. Done when: saving over a read-only fixture shows "Cannot save <file>: it is read-only." and the document stays dirty.
- [ ] Commit `tests/fixtures/nodus/metadata/doc-info.svg` and a `.svgt` template fixture with Inkscape evidence. Done when: Inkscape's Document Metadata shows the title and keywords (version quoted).
- [ ] Add New Document, Templates, and Document Information pages to `docs/user/nodus/`. Done when: every dialog is covered.
- [ ] Commit: `"nodus: the New Document dialog, presets, templates, and document information"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~DocumentFactoryTests|FullyQualifiedName~TemplateRoundTripTests|FullyQualifiedName~DocumentInfoMetadataTests"` exits 0, `doc-info.svg` and the template reopen with metadata and the template block equal, and Inkscape's Document Metadata shows the title and keywords (version quoted). Cheaper substitute that fails: metadata kept only in memory, which the reopen comparison catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with this file's test classes reporting
- [ ] Every fixture under `tests/fixtures/nodus/svg-live/`, `pages/`, `layers/`, `guides/`, and `metadata/` round-trips element by element and opens in Inkscape (version quoted)
- [ ] The benchmark project reports the §2 and §11 budgets met on the generated 10,000-element fixture
- [ ] `python scripts/todo-graph.py query parity --phase 4` reports every NP row planned to this file stamped
- [ ] `python scripts/todo-graph.py validate` clean
