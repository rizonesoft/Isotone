---
schema_version: 1
id: imago-parity-document
domain: 03-imago
status: draft
title: "TODO-08 -- Imago Parity: Document, Canvas, View, History, and the Image Menu"
depends_on: []
frozen: true
track: I8
---

# TODO-08 -- Imago Parity: Document, Canvas, View, History, and the Image Menu

> **Goal:** Imago's document foundation reaches Photoshop, Affinity Photo, and GIMP parity: a document model with precision (8-bit, 16-bit, and 32-bit float, perceptual or linear), separate X and Y resolution, pixel aspect ratio, and a transparent-background switch; one native-format contract (`imago:` parameters in the OpenRaster `stack.xml` beside a rendered PNG for every non-raster layer and document part) that every later live layer kind and document part registers with; the New Document dialog with presets and templates; the full zoom, rotate, flip, screen-mode, window, view-mode, display-filter, and navigator set; rulers, units, guides, grids, and snapping; measurement, count, notes, and the Info, Histogram, and Scope panels; snapshots, non-linear history, and history saved with the document; the Image menu's canvas, trim, reveal, and resampling commands; every clipboard and paste variant; and the crop and perspective-crop extensions. The code lives in `src/Imago/Photon.Imago.Core/` (`Documents/`, `Native/`, `Guides/`, `Snapping/`, `Analysis/`, `History/`), `src/Imago/Photon.Imago.Rendering/` (`Display/`, `Overlays/`), `src/Imago/Photon.Imago.FileFormats/Native/`, and `src/Imago/Photon.Imago.Desktop/`; it consumes the pixel engine (`D01 T03 §2` resampling, rotation, and perspective, `D01 T03 §4` histograms), color management (`D01 T04`), the suite history (`D01 T02 §4`), and the units converter and snapping core it moves out of Nodus on their second consumer; it never writes a second resampler, a second history stack, or a second container format, and view state never enters history.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `ImagoDocument` (`src/Imago/src/Imago.Core/Documents/ImagoDocument.cs`, 98 lines) holds one `Resolution` field defaulting to 72 and no pixel aspect ratio, precision curve, guides, or document parts; no Imago source names a pixel aspect at all. The bit-depth enum in `src/Imago/src/Imago.Core/Documents/BitDepth.cs` already names 32-bit float (`Bpc32 = 32`), which §1's precision readout labels. Undo is two linear lists in `src/Imago/src/Imago.Core/History/CommandHistory.cs` beside a 166-line `HistorySnapshot.cs`, so non-linear history (§6) has no model to extend until `D01 T02 §4` moves it to the suite. Zoom is one scalar clamped at 3,200 percent in `src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs`, and Cut, Copy, and Paste there only log. Guides exist only as a view-model flag (`_showGuides`); nothing in `Imago.Core` models a guide, and nothing in Imago computes a histogram. Checklist paths below name the post-rename `Photon.Imago.*` projects that `D03 T01 §1` creates; the claims name today's `Imago.*` paths and move with that rename.
<!-- claim: lines src/Imago/src/Imago.Core/Documents/ImagoDocument.cs = 98 -->
<!-- claim: count "private double _resolution = 72\.0" src/Imago/src/Imago.Core/Documents/ImagoDocument.cs = 1 -->
<!-- claim: count "PixelAspect" src/Imago/src/**/*.cs = 0 -->
<!-- claim: count "Bpc32 = 32" src/Imago/src/Imago.Core/Documents/BitDepth.cs = 1 -->
<!-- claim: count "private readonly List<ICommand> _redoStack" src/Imago/src/Imago.Core/History/CommandHistory.cs = 1 -->
<!-- claim: lines src/Imago/src/Imago.Core/History/HistorySnapshot.cs = 166 -->
<!-- claim: count "Math\.Min\(ZoomLevel \* 1\.25, 32\.0\)" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 1 -->
<!-- claim: count "(Cut|Copy|Paste) requested" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 3 -->
<!-- claim: count "private bool _showGuides" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 1 -->
<!-- claim: count "Guide" src/Imago/src/Imago.Core/**/*.cs = 0 -->
<!-- claim: count "Histogram" src/Imago/src/**/*.cs = 0 -->

## Inputs

- [`docs/parity/imago-parity.md`](../../docs/parity/imago-parity.md) -- the catalog rows each section owns (`IP-` ranges named in each context paragraph)
- [`docs/parity/imago-section-design.md`](../../docs/parity/imago-section-design.md) -- the design these sections were authored from, including the native-format decision for live content
- [`standards/imago.md`](../../standards/imago.md) -- tiles, premultiplied RGBA, 8, 16, and 32-bit float, zero allocations per frame, SIMD with a scalar reference, GPU parity, fidelity proofs, no silent profile change
- [`standards/shared.md`](../../standards/shared.md) -- the design contract, settings, logging, atomic saves, and performance rules
- [`standards/testing.md`](../../standards/testing.md) -- fixtures, goldens, and the fidelity tolerance rules
- OpenRaster 0.0.6 specification (`stack.xml`, `composite-op`, `isolation`) -- the container §1 extends
- Adobe Photoshop File Formats Specification -- image resources 1032 (grid and guides), 1064 (pixel aspect ratio), color samplers, and annotations read by §1, §4, and §5
- GIMP 3.2.6 (`gimp-console` batch mode as the `.ora` composite oracle; GEGL 0.4 `nohalo` and `lohalo` samplers, LGPL-3.0-or-later, as reference) and Krita 5.2 as a second `.ora` oracle
- libvips 8.16 and FFmpeg 7.1 (`hqx`, `xbr`) as resampling goldens; ImageMagick 7.1 `-distort Perspective` as the perspective-crop golden; numpy 2.x FFT as the FFT golden
- He, Sun, and Tang 2010 (guided filter) for §7's Preserve Details; Suzuki and Abe 1985 (border following) for §5's perimeter
- -> XREF: D03 T06 §3 -- Imago 0.1.0 ships before every section here
- -> XREF: D03 T01 §1 -- the rename the target paths assume
- -> XREF: D03 T04 §4 -- the native format §1 extends with the `imago:` contract
- -> XREF: D03 T04 §2 -- recent files §2 extends
- -> XREF: D03 T04 §5 -- the PSD adapter §1, §4, and §5 extend with resolution, pixel aspect, guide, and note resources
- -> XREF: D03 T03 §1 -- the New dialog §2 extends and the status strip §11 extends
- -> XREF: D03 T03 §2 -- the History panel and `TileSnapshotCommand` §6 extends
- -> XREF: D03 T03 §4 -- the zoom and hand tools and the temporary-tool mechanism §3 extends
- -> XREF: D03 T03 §7 -- Image Size, Canvas Size, and crop, which §1, §7, and §9 extend
- -> XREF: D03 T03 §8 -- the eyedropper sample size §11's sampler shares
- -> XREF: D03 T02 §1 -- the tile store whose reference counts §6's snapshots share
- -> XREF: D03 T02 §2 -- the viewport and mip cache §3 and §10 extend
- -> XREF: D03 T02 §5 -- GPU parity for §10's display filters
- -> XREF: D03 T01 §2 -- the ported `Ruler` control §4 extends
- -> XREF: D03 T05 §2 -- the histogram control §11 hosts
- -> XREF: D01 T02 §4 -- the suite history §6 builds its tree over
- -> XREF: D01 T02 §5 -- atomic writes for templates, logs, and exports
- -> XREF: D01 T03 §2 -- `Resampler`, `Rotator`, and `PerspectiveCorrector`, which §7 extends in place and §9 consumes
- -> XREF: D01 T03 §4 -- `Histogram` for §11
- -> XREF: D01 T04 §1 -- profile names and conversions for §1's profile tab and §11's readouts
- -> XREF: D02 T07 §9 -- `UnitConverter`, moved to `Photon.Core` by §4
- -> XREF: D02 T07 §11 -- the snapping core, moved to `Photon.Core` by §4
- -> XREF: D01 T06 §4 -- deconvolution reuses §11's `Fft2D`
- -> XREF: D03 T07 §17 -- workspaces the panels here dock into
- -> XREF: D03 T09 §1 -- layer kinds register with §1
- -> XREF: D03 T09 §7 -- layer effects register with §7's Scale Styles hook
- -> XREF: D03 T09 §13 -- artboards scope §4's guides and register snap candidates
- -> XREF: D03 T10 §1 -- selections float into §8's floating layer
- -> XREF: D03 T11 §7 -- precision and mode conversions over §1's fields
- -> XREF: D03 T11 §9 -- the Color Sampler tool places §11's sample points
- -> XREF: D03 T13 §3 -- content-aware crop fill through §9's hook
- -> XREF: D03 T16 §1 -- Paste without Formatting from §8 and the scale-marker label of §5
- -> XREF: D03 T16 §5 -- paths as a §1 document part and as §4 snap candidates
- -> XREF: D03 T17 §2 -- PSD write of guides, notes, samplers, and pixel aspect
- -> XREF: D03 T17 §3 -- PSD read of guides, notes, samplers, and pixel aspect
- -> XREF: D03 T17 §4 -- XCF guides, sample points, and precision
- -> XREF: D03 T17 §7 -- SVG and metafile readers that enable §8's Paste Special entries
- -> XREF: D03 T17 §10 -- metadata export of §6's XMP history log
- -> XREF: D03 T18 §3 -- slices as a §1 document part and §4 snap candidates
- -> XREF: D03 T18 §4 -- profile readout in §1's profile tab
- -> XREF: D03 T18 §5 -- proof color in §11's sampler readouts
- -> XREF: D03 T18 §6 -- print consumes §2's bleed
- -> XREF: D03 T15 §1 -- the Camera Raw filter and 32-bit editing that consume §1's float precision, §9's straighten and crop, and §11's scopes
- -> XREF: D03 T19 §1 -- provenance as a §1 document part
- -> XREF: D03 T19 §4 -- generative expand beside §9's crop extension
- -> XREF: D03 T19 §8 -- AI upscale beside §7's classical Preserve Details
- -> XREF: D03 T20 §4 -- preference pages over the navigation, units, guide, and grid keys added here
- -> XREF: D03 T21 §1 -- Imago 0.2.0 releases this file and re-proves §1's fallback in the previous release
- -> XREF: D03 T12 §5 -- Imago parity painting cites §6: snapshots as history brush sources; §1: the `imago:` contract fill, pattern, and symmetry elements register with
- -> XREF: D03 T14 §1 -- Imago parity filters cites §1: the `imago:` contract for filter stacks, live filter layers, planes, and projections

## Outcome

- Any `.imago` document with live content, renamed to `.ora`, opens in GIMP 3.2.6 and Krita 5.2 with every layer visible as pixels, and reopens live in Imago; unknown `imago:` data and newer schema versions survive a round trip byte-equivalent.
- `ImagoDocument` carries precision with a tone curve, separate X and Y resolution, pixel aspect ratio, a transparent-background switch, a comment, and a document-part bag, all shown in Image Properties and edited in Document Setup.
- The New Document dialog offers preset categories, saved presets, templates, and New from Clipboard, and the Document History panel locates moved files.
- Zoom from 1.5625 to 12,800 percent, rotate and flip view, screen modes, Show All, split view, view modes, display filters, the Navigator, and view points work without entering history, and tools hit exactly under a rotated, flipped view.
- Guides, grids, axis grids, rulers, custom units, and every snapping candidate family work through one units converter and one snapping core shared with Nodus.
- Measure, protractor, area, count, notes, the Measurement Log with CSV export, the Info, Pointer, Histogram, and Scope panels, and sample points read exact values in real-world units.
- Snapshots, non-linear history branches, and history saved with the document restore earlier states after a reopen.
- The Image menu resizes, resamples, rotates, trims, reveals, and fits the canvas with every Photoshop, Affinity, and GIMP method matched against committed goldens.
- Every clipboard and paste variant, named buffers, crop presets, straighten, overlays, crop beyond the canvas, and perspective crop place pixels exactly where they say, each edit one undo step.

**Adjacency:** list=applicable @ D03 T08 §2; document=applicable @ D03 T18 §6; settings=applicable @ D03 T08 §3; reporting=applicable @ D03 T08 §11; notifications=applicable @ D03 T08 §7; permissions=applicable @ D03 T08 §2; audit=applicable @ D03 T08 §6; exchange=applicable @ D03 T08 §1; reverse=applicable @ D03 T08 §6

**Adjacency rationale:** The template browser and recent-documents list (§2), the Images panel and navigator view points (§10), the Measurement Log (§5), the Buffers panel (§8), and the History panel (§6) are the browsable lists. Bleed and print size from §2 and §7 are what print consumes; `D03 T18 §6` prints them. Every toggle and value is an `Imago.*` key with a default and a named consumer; §3 adds the largest set. Image Properties (§1), the Info, Histogram, Scope, and Pointer panels (§11), and the Measurement Log (§5) are the reports. Resampling, rotation, trim, and history save report progress and cancel on the status strip (§7, §6), and the open summary names layers opened as pixels (§1). Read-only template folders, missing recent files, and locked documents are refused by name (§2), and locked guides refuse edits (§4). Every document-changing command is one history entry with one Serilog Information line, and §6 adds the history log. The `imago:` contract and `.ora` interop (§1), templates (§2), measurement CSV export (§5), clipboard formats (§8), and PSD and XCF resources through `D03 T17` are the exchange surface. Every document command undoes, snapshots and history branches restore earlier states (§6), and Revert restores the saved file.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The document model and the native-format contract for live content | D03 T06 §3, D03 T04 §4 |  [ ]   |
|   2   |   §2    | New document, presets, and templates | §1 |  [ ]   |
|   3   |   §3    | Zoom, rotate view, flip view, and screen modes | D03 T06 §3 |  [ ]   |
|   4   |   §4    | Rulers, units, guides, grids, and snapping | §1 |  [ ]   |
|   5   |   §5    | Measure, protractor, count, and notes | §4 |  [ ]   |
|   6   |   §6    | History extensions: snapshots, non-linear history, and saved history | §1, D01 T02 §4 |  [ ]   |
|   7   |   §7    | The Image menu: canvas, rotation, trim, reveal, and resampling | §1 |  [ ]   |
|   8   |   §8    | Clipboard and paste variants | §1 |  [ ]   |
|   9   |   §9    | Crop and straighten extensions | §7 |  [ ]   |
|  10   |   §10   | Windows, arrangement, view modes, display filters, and the navigator | §3 |  [ ]   |
|  11   |   §11   | Info, histogram, sample points, and scopes | §1 |  [ ]   |

---

## 1. The document model and the native-format contract for live content

Parity adds document content OpenRaster cannot express (adjustment and fill layers, styles, smart objects, text, channels, paths, guides, snapshots, provenance), and without one contract each later section would invent its own container. This section fixes it once: parameters in the `imago:` namespace of `stack.xml` beside a rendered PNG fallback for every non-raster layer, one `<imago:document>` block for document parts, and a reader that restores the live layer when its fallback hash matches and opens pixels when it does not. It also completes the document model (precision with a tone curve, X and Y resolution, pixel aspect ratio, transparent background) with the dialogs that read and edit it. It must not break `D03 T04 §4`: a document with no live content and no document part writes the same bytes as before. It serves the acceptance-bar aims "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog" and "Editing stays non-destructive". Catalog: IP-0001 to IP-0008 (8 features: image properties, transparent background, duplicate image, document setup, count unique colors, pixel aspect ratio, image comment, pixel aspect correction).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/image-properties/ and docs/captures/imago/document-setup/.
**Job:** a user can read everything about a document (size, print size, resolution, precision, profile, memory, history, element counts) and change its units, resolution, pixel aspect, and background without guessing, and any `.imago` renamed to `.ora` opens in GIMP and Krita with every layer visible. Consumer: the native reader and writer, and every later live layer kind and document part that registers with the contract.
**Treatment:** GIMP's tabbed Image Properties (Properties, Color Profile, Comment) and Affinity's Document Setup (dimensions with resample or anchor, DPI, units, transparent background) as modal dialogs; Image, Pixel Aspect Ratio and View, Pixel Aspect Ratio Correction menus; Image, Duplicate. Cheaper substitute that fails the checkpoint: writing only parameters with no fallback PNG, so other editors show blank layers.
**Chrome:** consume `Photon.UI` dialog styles, the settings store, `D03 T03 §7`'s Image Size and Canvas Size commands, and `D01 T04 §1`'s ICC reader. Do not add a second container or serializer.

**Requires:** display-session -- the dialogs and the GIMP and Krita open of a live fixture need an interactive desktop

- [ ] Record the `imago:` contract (namespace URI `https://schemas.rizonesoft.com/imago/1` as `D03 T04 §4` documents it, the fallback-PNG rule, the hash rule, and the preservation rule) as a row in `docs/dev/decisions.md`. Done when: the row names the URI, the fallback rule, and the cost of changing it (every saved live document).
- [ ] Add `Precision` (`BitDepth` 8, 16, or 32-float plus `ToneCurve { Perceptual, Linear }`) to `ImagoDocument` in `src/Imago/Photon.Imago.Core/Documents/ImagoDocument.cs`, labeled as GIMP 3.2 does ("16-bit integer, perceptual"). Done when: `DocumentPropertiesTests.PrecisionLabel` asserts the label for all six combinations; conversion stays `D03 T11 §7`'s. **Corrected 2026-09-26 (integration):** keep the `Bpc32` bound in `BitDepth.cs` consistent with the float tiles below, which keep values above 1.0; `D03 T15 §4` later replaces its normalized maximum with scene-linear float.
- [ ] Replace the single `Resolution` with `ResolutionX`, `ResolutionY`, and `ResolutionUnit`, and add `PixelAspectRatio` (default 1.0), `TransparentBackground`, `Units`, and `Comment` to `ImagoDocument`. Done when: every existing caller of `Resolution` compiles against `ResolutionX` and `DocumentPropertiesTests` round-trip each field.
- [ ] Add `DocumentParts` (the document-part bag, keyed by part name) to `ImagoDocument` in `src/Imago/Photon.Imago.Core/Documents/DocumentParts.cs`. Done when: a part added and removed leaves the bag empty and marks the document dirty once each.
- [ ] Add `IImagoElement` in `src/Imago/Photon.Imago.Core/Native/IImagoElement.cs` with `string Kind` (lowercase, such as `fill`, `adjustment`, `text`), `int SchemaVersion`, `WriteParameters(XElement target, INativeWriteContext context)` (the context adds ZIP entries under `imago/`), and `RenderFallback(TileGrid target)` for layer kinds, with XML documentation on each member. Done when: the project builds and it is the only live-element abstraction in Imago.
- [ ] Add `ImagoElementRegistry` in `src/Imago/Photon.Imago.Core/Native/ImagoElementRegistry.cs` with `RegisterLayerKind(kind, reader)` and `RegisterDocumentPart(name, reader)`, registered as a singleton in the Imago composition root. Done when: `ServiceRegistrationTests` resolves it and a second registration of one kind throws naming the kind.
- [ ] Teach `ImagoNativeFormat` in `src/Imago/Photon.Imago.FileFormats/Native/` to write every non-raster layer as an OpenRaster `<layer src="data/<guid>.png">` whose PNG is the rendered fallback at document size (16-bit PNG for 16 and 32-bit documents), carrying `imago:kind`, `imago:v`, `imago:hash` (SHA-256 of the fallback PNG bytes), and one `<imago:params>` child. Done when: a saved probe layer shows its fallback pixels in GIMP. Cheaper substitute: parameters with no fallback PNG.
- [ ] Write blend modes OpenRaster names as `composite-op="svg:*"`; write others as `svg:src-over` plus `imago:composite-op`, listed in the save's fallback report; keep OpenRaster `isolation` on groups. Done when: `NativeElementContractTests.BlendModeFallback` asserts both forms and the report lists the non-OpenRaster mode.
- [ ] Write one `<imago:document imago:v="1">` as the first child of `<image>` through `DocumentPartSerializer` in `src/Imago/Photon.Imago.FileFormats/Native/`, with one child block per registered part, each with its own `imago:v`, large payloads as ZIP entries under `imago/` referenced by path. Done when: a document with no part writes no `<imago:document>` element and `D03 T04 §4`'s fixtures save byte-identical.
- [ ] Store 32-bit float layers as `imago/float/<guid>.rgbaf` (little-endian RGBA32F in 256-pixel tiles) beside their 16-bit PNG fallback, and document the layout in `docs/dev/imago/native-format.md`. Done when: a float layer reopens with every value bit-identical, including values above 1.0.
- [ ] Teach the reader: a known kind whose fallback hash matches reopens live; a mismatch opens the PNG as a pixel layer and adds the Warning "{Kind} layer {Name} was edited outside Imago; opened as pixels" to the open summary. Done when: `NativeElementContractTests.HashMismatchOpensAsPixels` passes.
- [ ] Keep an unknown kind, a newer `imago:v`, or an unknown document block verbatim in `UnknownNativeData`, render it from its fallback, and write it back byte-equivalent. Done when: `NativeElementContractTests.UnknownKindPreserved` compares the written block byte for byte.
- [ ] Add `UniqueColorCounter` in `src/Imago/Photon.Imago.Core/Analysis/UniqueColorCounter.cs` (tile-parallel, 64-bit keys for 16-bit documents, cancellable) for IP-0005, reused by §11. Done when: `UniqueColorCounterTests` counts 4,096 on a 4,096-color ramp and cancels within 100 ms.
- [ ] Add the Image Properties dialog `src/Imago/Photon.Imago.Desktop/Views/Dialogs/ImagePropertiesDialog.xaml` (IP-0001, IP-0005, IP-0007): Properties tab with pixel and print size, X and Y resolution, color space, precision, file name, path, size, and type, tile-cache memory, undo and redo counts, layer, channel, and path counts, pixel count, and a Count unique colors button. Done when: each value matches the fixture document and the capture is committed. Cheaper substitute: a message box with width and height.
- [ ] Add the Color Profile tab (description, class, space, version, copyright through `D01 T04 §1`; assign and convert stay `D03 T18 §4`) and the Comment tab editing `Comment` as one undoable step. Done when: an sRGB fixture shows its description and a comment edit undoes.
- [ ] Add Document Setup `src/Imago/Photon.Imago.Desktop/Views/Dialogs/DocumentSetupDialog.xaml` (IP-0004): units, DPI with Rescale (through `D03 T03 §7`'s Image Size command) or keep pixels, dimensions with an anchor grid (the Canvas Size command). Done when: Rescale changes pixel size and keep-pixels changes only resolution, each one undo step.
- [ ] Add Image, Transparent Background (IP-0002) toggling the flag through one `SetDocumentPropertyCommand`; when off, the composite and every flattening export draw over opaque white as Affinity does. Done when: `DocumentPropertiesTests.TransparentBackgroundOff` asserts a white composite under a transparent layer; the new-document background choice stays `D03 T03 §1`'s.
- [ ] Add Image, Pixel Aspect Ratio (IP-0006) listing Square 1.0, D1/DV NTSC 0.9091, D1/DV PAL 1.0940, D1/DV NTSC Widescreen 1.2121, HDV 1080/DVCPRO HD 720 1.3333, D1/DV PAL Widescreen 1.4587, DVCPRO HD 1080 1.5, Anamorphic 2:1 2.0, plus custom values saved in `Imago.Document.CustomPixelAspects`. Done when: choosing a value is one undo step and the pixel hash is unchanged.
- [ ] Add View, Pixel Aspect Ratio Correction (IP-0008, `Imago.View.PixelAspectCorrection`, default on) that scales only the view's X axis in §3's view transform. Done when: a 2.0 document shows twice as wide with the pixel hash unchanged.
- [ ] Read PSD resource 1064 (pixel aspect ratio) and both resolutions in the `D03 T04 §5` adapter. Done when: a Photoshop-saved `pixel-aspect.psd` fixture (version recorded) opens with its ratio.
- [ ] Add Image, Duplicate (IP-0003) with a name and "Duplicate merged layers only", creating an untitled tab whose tiles are shared copy-on-write, with no entry in the source's history. Done when: `DuplicateImageTests` assert zero tile copies at duplicate time and the source history length unchanged.
- [ ] Name undo steps "Set Document Properties", "Toggle Transparent Background", and "Set Pixel Aspect Ratio", each writing one Serilog Information line with the document id and the changed fields. Done when: a driven edit of each logs exactly one line (quoted).
- [ ] Add a test-only `ProbeLayer` kind and a `probe` document part in `tests/Photon.Imago.Core.Tests/Native/` with `NativeElementContractTests` covering write, reopen live, hash mismatch, unknown kind, and newer version. Done when: all five cases pass.
- [ ] Commit fixtures under `tests/fixtures/imago/native-live/` (probe layer, unknown future kind, a fallback edited by GIMP, a 32-bit float layer) with composites exported by GIMP 3.2.6 `gimp-console` and Krita 5.2 from each file renamed `.ora`, versions in `VERSION.txt`. Done when: the fixtures, composites, and version file are committed.
- [ ] Add `NativeLiveRoundTripTests` in `tests/Photon.Imago.FileFormats.Tests/` that open, save, and reopen every `native-live` fixture and compare layer by layer, plus the preserved unknown block byte for byte, and compare Imago's composite with GIMP's within 1/255. Done when: the test passes and fails if the unknown block is dropped.
- [ ] Document the contract in `docs/dev/imago/native-format.md` (wire shape, registry, hash rule, preservation, how a later kind or part registers) and add Image Properties and Document Setup pages to `docs/user/imago/`. Done when: both pages exist and the user page names every field.
- [ ] Commit: `"imago: the document model and the imago namespace contract for live content"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~NativeLiveRoundTripTests|FullyQualifiedName~NativeElementContractTests|FullyQualifiedName~DocumentPropertiesTests"` exits 0; every `tests/fixtures/imago/native-live/` file compares equal layer by layer after open, save, and reopen, the preserved unknown block is byte-identical, and GIMP 3.2.6's composite of each file renamed `.ora` matches Imago's within 1/255 (versions quoted). Cheaper substitute that fails: parameters written with no fallback PNG, which the GIMP composite comparison catches as a blank layer.

**Freeze check:** Every `.imago` save goes through the `D01 T02 §5` atomic writer; a save of each `D03 T04 §4` fixture that holds no live content and no document part produces bytes identical to the pre-change writer (hash comparison in `NativeLiveRoundTripTests.PlainDocumentsUnchanged`); killing the process mid-save leaves the original byte-identical. Fixture source: `tests/fixtures/imago/native/` (from `D03 T04 §4`) and `tests/fixtures/imago/native-live/` (created by this section).

## 2. New document, presets, and templates

Starting the right document is the first thing a user does, and today the New dialog of `D03 T03 §1` takes a width and a height. This section extends that dialog (never replaces it) with preset categories, saved presets, precision, profile, pixel aspect, fill, comment, and bleed, adds one creation path every entry point uses, and adds GIMP's settings templates, Photoshop and Affinity content templates, New from Clipboard, and a Document History panel over `D03 T04 §2`'s recent files. It must not add a second recent-files store. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0009 to IP-0019 (11 features: document presets, new from clipboard, bleed, templates, template editing, recent documents, new-document options, preset details, content templates, document history, template panel).

**Fidelity:** docs/captures/imago/new-document/ (baseline from `D03 T03 §1`); new captures to docs/captures/imago/templates/ and docs/captures/imago/document-history/.
**Job:** a user starts the right document in one step, reuses their own sizes and templates, and reopens recent work even when it moved. Consumer: `DocumentFactory`, the one creation path.
**Treatment:** preset categories and Saved on the left, details on the right with an orientation swap, templates as tiles, a GIMP-style Templates panel and template editor, and a Document History panel with thumbnails and missing-file badges. Cheaper substitute that fails the checkpoint: a width and height prompt with a hard-coded list.
**Chrome:** consume the `D03 T03 §1` dialog (extended, not replaced), `Photon.UI` dialog styles, the settings store, `D01 T02 §5` for template writes, and the icon catalog. Do not add a second recent-files store.

**Requires:** display-session -- the New dialog, template browser, and Document History panel need an interactive desktop

- [ ] Add the `DocumentPreset` record in `src/Imago/Photon.Imago.Core/Documents/Presets/DocumentPreset.cs` (IP-0009): name, category, width, height, units, resolution, orientation, color mode, precision, tone curve, profile name, pixel aspect, background fill, bleed, artboard flag (read by `D03 T09 §13`), and comment. Done when: `DocumentPresetStoreTests` round-trip every field through JSON.
- [ ] Add the built-in categories Photo, Print, Art and Illustration, Web, Mobile, and Film and Video in `src/Imago/Photon.Imago.Core/Documents/Presets/BuiltInPresets.cs`, sizes named by paper or pixel size with no vendor content. Done when: `DocumentFactoryTests.BuiltInPresets` asserts each preset's size and resolution.
- [ ] Add `DocumentPresetStore` persisting user presets in `Imago.NewDocument.UserPresets`, favorites in `Imago.NewDocument.Favorites`, and the last used preset in `Imago.NewDocument.LastPreset`. Done when: a saved preset and a favorite survive an app restart (settings readback quoted).
- [ ] Add `DocumentFactory.Create(DocumentPreset)` in `src/Imago/Photon.Imago.Core/Documents/DocumentFactory.cs` as the one creation path for the dialog, New without Dialog (Alt+Ctrl+N, from the last preset), templates, and New from Clipboard, logging one Information line per create with preset, size, and precision. Done when: `grep -rn "new ImagoDocument(" src/Imago/Photon.Imago.Desktop` finds no caller outside the factory.
- [ ] Implement every background fill in `DocumentFactory` (white, black, background color, transparent, 50 percent gray in the document's tone curve, custom). Done when: `DocumentFactoryTests.HalfGray` asserts 128 in perceptual 8-bit and 0.5 in linear float.
- [ ] Extend `D03 T03 §1`'s New dialog (IP-0015, IP-0016) with a preset rail (Recent, Saved, categories) and a details pane with an orientation swap, color mode (RGB and Grayscale; CMYK and Lab rows disabled with a tooltip naming `D03 T11 §7`), precision and tone curve, profile list from `D01 T04 §1`'s installed-profile enumeration, pixel aspect (§1's list), fill, comment, and bleed. Done when: every control has an automation name and the capture is committed. Cheaper substitute: a width and height prompt.
- [ ] Add Save Preset and Delete Preset to the dialog's details pane. Done when: a saved preset appears under Saved and deleting it removes it from the setting.
- [ ] Add `ClipboardImageReader` in `src/Imago/Photon.Imago.Desktop/Clipboard/ClipboardImageReader.cs` reading PNG, `CF_DIBV5`, and `CF_DIB` into a tile grid (IP-0010); §8 extends it with writing. Done when: `ClipboardFormatTests.ReadPngWithAlpha` preserves alpha.
- [ ] Add the dialog's Clipboard preset (size and resolution of the clipboard image) and Edit, Paste As, New Image creating the document with the pixels. Done when: a driven copy from another app creates a document of that size (log line quoted).
- [ ] Store bleed (IP-0011) in the §1 document block as `<imago:bleed>`, draw it as a guide line in the view (hidden by §3's Preview mode), consumed by `D03 T18 §6`. Done when: a 3 mm bleed survives save and reopen.
- [ ] Add `TemplateStore` for GIMP-style settings templates (IP-0012, IP-0019) stored in `%LOCALAPPDATA%\Rizonesoft\Imago\templates.json` through the `D01 T02 §5` atomic writer. Done when: `DocumentPresetStoreTests.TemplatesAtomic` shows a killed write leaves the old file intact.
- [ ] Add the Templates panel `src/Imago/Photon.Imago.Desktop/Views/Panels/TemplatesPanel.xaml` listing templates with size, orientation, resolution, color space, precision, gamma, profiles, fill, and comment, with New, Duplicate, Delete, and Create Image from the selected template. Done when: each command works in a driven run and the capture is committed.
- [ ] Add the template editing dialog (IP-0013) opened by the panel's Edit command. Done when: editing a template's size and saving updates the panel row.
- [ ] Add content templates (IP-0012, IP-0017): an `.imago` file carrying an `<imago:template>` block (name, category, description), with File, Save as Template and File, New from Template opening an untitled copy. Done when: `ContentTemplateRoundTripTests` assert the block survives save and New from Template yields an untitled, clean document.
- [ ] Add File, Edit Template, which opens the template file itself for editing. Done when: saving it writes to the template path, not to an untitled copy.
- [ ] Read template folders from `Imago.Templates.Folders` (default `%LOCALAPPDATA%\Rizonesoft\Imago\templates\`) in the template browser tiles, listing an unreadable folder with its refusal "Cannot read <path>: access denied." and a Warning log line. Done when: a denied folder in a driven run shows the message.
- [ ] Refuse Affinity `.aftemplate` files by name ("Affinity templates are not supported; see backlog B-045") in the template browser. Done when: dropping one shows the message and opens nothing.
- [ ] Extend `D03 T04 §2`'s recent list (IP-0014) with `Imago.Files.RecentCount` (default 20, 0 to 100) and `Imago.Files.KeepRecent`. Done when: a count of 3 trims the menu to 3 entries and 0 with KeepRecent off records nothing.
- [ ] Add the Document History panel `src/Imago/Photon.Imago.Desktop/Views/Panels/DocumentHistoryPanel.xaml` (IP-0018): thumbnail, path, last opened, a missing badge, Locate (repoint through a file dialog), Remove Entry, and Clear. Done when: `RecentDocumentsTests` detect a moved file in a temp folder and Locate repoints it.
- [ ] Show missing entries disabled in File, Open Recent beside a Locate item. Done when: a missing entry cannot be opened and Locate works from the menu.
- [ ] Add New Document, Templates, and Document History pages to `docs/user/imago/`. Done when: every dialog and panel above is covered.
- [ ] Commit: `"imago: new-document presets, templates, and recent documents"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~DocumentFactoryTests|FullyQualifiedName~DocumentPresetStoreTests|FullyQualifiedName~ContentTemplateRoundTripTests|FullyQualifiedName~RecentDocumentsTests"` exits 0, and a driven run saves a template, creates a document from it, and locates a moved recent file, with the log lines quoted and captures committed under docs/captures/imago/templates/ and docs/captures/imago/document-history/. Cheaper substitute that fails: presets stored as a fixed table, which the saved-preset round trip catches.

## 3. Zoom, rotate view, flip view, and screen modes

Today zoom is one scalar clamped at 3,200 percent, and the canvas cannot rotate or flip. This section replaces it with a per-window view state and one view transform every tool, ruler, overlay, and hit test uses, then builds the full zoom, navigation, rotation, flip, screen-mode, padding, Extras, and Preview set on it. View state never enters history and logs only at Debug. It must not break `D03 T02 §2`'s viewport or mip cache: pixels on screen at 0 degrees and 100 percent are identical before and after. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0026 to IP-0051 (26 features). The natural split named by the design (window-level behaviors, birds-eye view, and flick panning) was not needed: the section fits in 30 items.

**Fidelity:** docs/captures/imago/main-window/ for the View menu and canvas; new captures to docs/captures/imago/view/.
**Job:** a user sees the image at the zoom, angle, and orientation the task needs and gets anywhere in it fast. Consumer: every tool, the rulers, and the overlays, which read `ViewTransform`.
**Treatment:** View menu zoom and screen-mode commands, the Zoom and Rotate View tools with options bars, a typed zoom field in the status strip, and canvas overlays whose visibility Extras governs. Cheaper substitute that fails the checkpoint: rotating the WPF control with a render transform, which leaves rulers, hit testing, and tools in unrotated coordinates.
**Chrome:** consume `D03 T02 §2`'s viewport and mip cache, `D03 T03 §4`'s tool system and temporary-tool mechanism, the keymap, and the settings store. Do not add a second zoom model.

**Requires:** display-session -- zoom, rotation, flicks, screen modes, and frame-time measurement need an interactive desktop

- [ ] Add `ViewState` in `src/Imago/Photon.Imago.Desktop/View/ViewState.cs` per window: zoom, center in document coordinates, rotation in degrees, flip horizontal and vertical, screen mode, and show-all. Done when: two windows on one document hold independent states and no change to either enters history.
- [ ] Add `ViewTransform` in `src/Imago/Photon.Imago.Desktop/View/ViewTransform.cs` composing scale, rotation about the view center, flip, and §1's pixel-aspect correction, with an exact inverse. Done when: `ViewTransformTests` round-trip 10,000 random points under rotation, flip, and pixel aspect within 1e-9.
- [ ] Route hit testing, the rulers, the overlays, and every tool's pointer mapping through `ViewTransform.Inverse` in `src/Imago/Photon.Imago.Desktop/Controls/Canvas/`. Done when: `ToolCoordinatesUnderRotationTests` place a brush dab at a document point at 37 degrees with the view flipped and it lands on that point. Cheaper substitute: a WPF `RotateTransform` on the canvas control.
- [ ] Draw tiles through the rotated matrix in the viewport on both the CPU and GPU paths without resampling document pixels. Done when: the document tile hash is unchanged after rotating the view and a capture at 37 degrees is committed.
- [ ] Add `ZoomCommands` in `src/Imago/Photon.Imago.Desktop/View/ZoomCommands.cs` (IP-0026, IP-0027): In and Out on a preset ladder from 1.5625 to 12,800 percent, Fit on Screen (Ctrl+0), Fill, 100 percent (Ctrl+1), 200 percent (Ctrl+2), Zoom to Selection (Shift+Ctrl+J), and Revert Zoom (backtick), replacing today's clamped `ZoomLevel`. Done when: `ZoomCommandsTests` assert fit, fill, and zoom-to-selection against known bounds and `grep -n "32\.0" MainWindowViewModel.cs` finds no clamp.
- [ ] Add the Custom Zoom dialog accepting a percent or a ratio such as `3:1`, and a typed zoom field in the status strip. Done when: typing `3:1` sets 300 percent and an invalid entry is refused with a tooltip.
- [ ] Add pointer navigation keys (IP-0028, IP-0048): wheel zooms or scrolls (`Imago.Navigation.WheelZooms`), zoom to the clicked point (`Imago.Navigation.ZoomToClickedPoint`), and Space pans or moves (`Imago.Navigation.SpaceBar`). Done when: toggling each key changes the gesture in a driven run (settings readback quoted).
- [ ] Add scrubby zoom by dragging with the Zoom tool (`Imago.Navigation.ScrubbyZoom`), animated zoom while held (`Imago.Navigation.AnimatedZoom`), and drag-to-zoom speed (`Imago.Navigation.DragZoomSpeed`) (IP-0029). Done when: each works in a driven run and its key is read by the Zoom tool.
- [ ] Add hold Z for a temporary zoom through `D03 T03 §4`'s temporary-tool mechanism. Done when: releasing Z returns to the previous tool.
- [ ] Add resize floating windows to fit when zooming (`Imago.View.ResizeWindowOnZoom`, IP-0030). Done when: zooming a floating window resizes it within the screen bounds.
- [ ] Add scroll, zoom, and rotate all windows together when Shift is held or the options-bar checkbox is on (IP-0031). Done when: a driven zoom with the box checked changes every open window.
- [ ] Add birds-eye view (IP-0032): hold H and press to zoom out to fit with a frame, release to zoom into the framed area, as Photoshop does. Done when: the release point becomes the new view center.
- [ ] Add flick panning with exponential decay (`Imago.Navigation.FlickPanning`, IP-0033) and overscroll past the canvas edge (`Imago.View.Overscroll`, IP-0049). Done when: a flick coasts and stops, and overscroll allows the canvas edge to reach the view center.
- [ ] Add Print Size (IP-0034) using `Imago.View.ScreenPpi`, detected from the monitor's physical size through `GetDeviceCaps` `HORZSIZE` and `HORZRES`, entered manually, or set by a Calibrate dialog that measures an on-screen line. Done when: a 1-inch document measures one inch with a ruler on the calibrated screen (driven, value quoted). Source: https://learn.microsoft.com/windows/win32/api/wingdi/nf-wingdi-getdevicecaps
- [ ] Add Actual Pixels and GIMP's Dot for Dot toggle (IP-0051): off shows the image at its physical size using §1's X and Y resolution. Done when: a 72 by 144 ppi document shows square pixels only with Dot for Dot on.
- [ ] Add the Rotate View tool (R, IP-0035) with an angle field, Shift for 15-degree steps, and Reset View (Esc or the button). Done when: Shift-drag lands on multiples of 15 and Reset returns to 0.
- [ ] Add rotation by modifier-scroll (`Imago.Navigation.RotateModifier`) and by touchpad rotation through WPF manipulation events (IP-0046, IP-0049). Done when: both rotate the view in a driven run. Source: https://learn.microsoft.com/dotnet/desktop/wpf/advanced/walkthrough-creating-your-first-touch-application
- [ ] Add View, Flip Horizontally and Flip Vertically (IP-0036) as view flags that mirror the transform and never touch pixels. Done when: the pixel hash is unchanged after both flips.
- [ ] Add screen modes (IP-0037): Standard, Full Screen with Menu Bar, and Full Screen, with F to cycle and Shift+F to reverse. Done when: a driven run captures each mode.
- [ ] Add show or hide for menu bar, scroll bars, status bar, and rulers (IP-0038, IP-0047), each with a separate full-screen default under `Imago.View.FullScreen.*`. Done when: hiding rulers in full screen leaves them visible in Standard.
- [ ] Add padding (IP-0039) from the theme, light checks, dark checks, or a custom color (`Imago.View.PaddingMode`, `Imago.View.PaddingColor`) with Keep Padding in Show All. Done when: each mode renders in a capture.
- [ ] Add View, Show All (IP-0040) rendering layer pixels beyond the canvas and turning off clip-to-canvas for the view only, as GIMP 2.10 does. Done when: a layer extending past the canvas shows fully and exports stay clipped.
- [ ] Add Extras (Ctrl+H, IP-0041, IP-0042) as the master toggle over layer edges, selection edges, target path, notes, count, pixel grid, guides, smart guides, slices, and canvas boundary, with a Show Extras Options dialog. Done when: turning Extras off hides every overlay and on restores the checked ones.
- [ ] Add Preview mode (IP-0043, IP-0045, `Imago.View.PreviewMode`) hiding guides, grids, margins, and bleed, as Affinity does. Done when: a capture in Preview mode shows no overlay.
- [ ] Extend `D03 T02 §2`'s pixel grid (IP-0044) with View, Show, Pixel Grid, `Imago.View.PixelGridMinZoom` (default 600 percent), and color and opacity keys. Done when: the grid appears at 600 percent and not at 500.
- [ ] Add image window preferences (IP-0050): initial zoom (fit or 1:1) with Limit initial zoom to 100 percent, resize window on image change, and Show All by default, as `Imago.View.*` keys the `D03 T20 §4` pages list. Done when: opening a small image with the limit on shows 100 percent.
- [ ] Measure panning a 100-megapixel document at a 37-degree view rotation. Done when: the median frame is under 16 ms, quoted with the machine.
- [ ] Add View menu, Zoom tool, Rotate View tool, and Screen Modes pages to `docs/user/imago/`. Done when: every command above is covered.
- [ ] Commit: `"imago: zoom, rotate and flip view, and screen modes"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewTransformTests|FullyQualifiedName~ZoomCommandsTests|FullyQualifiedName~ToolCoordinatesUnderRotationTests"` exits 0 (a brush dab placed at a document point lands on that point at 37 degrees with the view flipped), and a driven run captures each screen mode, a rotated view, and Show All under docs/captures/imago/view/ with the frame-time median quoted. Cheaper substitute that fails: a WPF `RotateTransform` on the canvas control, which the tool-coordinate test catches.

## 4. Rulers, units, guides, grids, and snapping

Exact placement needs units, guides, grids, and snapping, and Nodus already owns a units converter (`D02 T07 §9`) and a snapping core (`D02 T07 §11`). Imago is their second consumer, so this section moves both into `Photon.Core` first (a move, never a copy), then builds Imago's rulers, document guides persisted in the §1 block, configurable and axis grids, and Imago snap providers on the shared core. It must not change Nodus's behavior: Nodus's units and snapping tests pass unchanged after the moves. It serves the acceptance-bar aims "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog" and "Shared once, never copied". Catalog: IP-0068 to IP-0093 (26 features). The natural split named by the design (the grid and axis-grid items) was not needed: the section fits in 30 items.

**Fidelity:** docs/captures/imago/main-window/ for the rulers; new captures to docs/captures/imago/guides/, docs/captures/imago/grid/, and docs/captures/imago/snapping/.
**Job:** a user can place exact guides and grids in the units of the job and land moves, crops, and selections exactly where they mean. Consumer: the move, crop, and selection tools, which query the snapping engine, and the save, which persists guides and grids.
**Treatment:** ruler drags create guides, the View, Guides submenu and dialogs place them numerically, a Grid and Axis Manager configures grids, and a Snapping Manager lists every candidate with a check. Cheaper substitute that fails the checkpoint: guides kept in view-model memory, which a reopen loses.
**Chrome:** consume the ported `Ruler` control (`D03 T01 §2`, extended), §3's `ViewTransform`, the overlay layer, the moved `UnitConverter` and snapping core, and the settings store. Do not add a second units table or snap ranking.

**Requires:** display-session -- guide drags, grid display, and snapping feedback need an interactive desktop

- [ ] Move `UnitConverter` from `src/Nodus/Photon.Nodus.Core/Units/` (`D02 T07 §9`) into `src/Photon.Core/Units/` with its tests into `tests/Photon.Core.Tests/Units/`, and repoint Nodus. Done when: `grep -rn "class UnitConverter" src` finds one definition and Nodus's unit tests pass unchanged.
- [ ] Add the document-relative units percent and columns (`Imago.Units.ColumnWidth`, `Imago.Units.GutterWidth`) to the shared converter as context conversions. Done when: `UnitConverterTests.Columns` converts 2 columns plus a gutter to pixels.
- [ ] Add a GIMP-style Units editor `src/Imago/Photon.Imago.Desktop/Views/Dialogs/UnitsEditorDialog.xaml` (IP-0070) for user units (identifier, factor per inch, digits, symbol, abbreviation, singular, plural), stored in `%LOCALAPPDATA%\Rizonesoft\Imago\units.json` through the atomic writer and registered into the shared converter at startup. Done when: a user unit appears in every unit list after a restart.
- [ ] Extend the `Ruler` control (IP-0068, IP-0069) with units from `Imago.Units.Rulers` and a per-document override `imago:units`, a right-click units menu, and document alignment under §3's rotation. Done when: a capture shows rulers in millimetres and the override survives reopen.
- [ ] Add ruler origin: corner drag sets it, double-click resets it, persisted in the §1 block. Done when: a moved origin survives save and reopen.
- [ ] Add `Guide` in `src/Imago/Photon.Imago.Core/Guides/Guide.cs` (orientation, position in document pixels as a double, optional color, optional `ArtboardId` scoped by `D03 T09 §13`) and `ImagoDocument.Guides` with a document-level lock. Done when: `GuideCommandTests` add, move, and remove guides.
- [ ] Persist guides as `<imago:guides>` in the §1 document block through a registered part. Done when: `GuideSerializationTests` reopen `tests/fixtures/imago/guides/layout.imago` with every guide equal.
- [ ] Read PSD resource 1032 (grid and guides) in the `D03 T04 §5` adapter; writing is `D03 T17 §2`'s and XCF is `D03 T17 §4`'s. Done when: a Photoshop-produced `guides.psd` (tool and version recorded) opens with every guide equal.
- [ ] Add New Guide (orientation and position in any unit) and New Guide by Percent (IP-0071, IP-0072) under View, Guides, each one undoable step. Done when: a guide at 50 percent lands at the canvas center.
- [ ] Add New Guide Layout (IP-0073): columns and rows by number, width, and gutter, margins, center guides, clear existing, and presets in `Imago.Guides.LayoutPresets`. Done when: a 12-column layout creates the expected positions in `GuideCommandTests.Layout`.
- [ ] Add New Guides from Selection or layer bounds (IP-0074); shape layers join when `D03 T16 §7` lands. Done when: a rectangular selection yields four guides on its edges.
- [ ] Add Lock Guides (Alt+Ctrl+;), Clear Guides, Clear Selected Guides, and Clear Canvas Guides (IP-0077, IP-0078). Done when: locked guides refuse a drag with a status-strip message and each clear undoes.
- [ ] Add guide gestures (IP-0075, IP-0076): drag from a ruler (Alt switches orientation, Shift snaps to ruler ticks), move with the Move tool, Alt-drag clones, and drag onto a ruler deletes; guides may sit off-canvas. Done when: each gesture works in a driven run and is one undo step.
- [ ] Add the guide edit dialog on double-click (IP-0079) with position and per-guide color. Done when: a colored guide survives reopen.
- [ ] Add Show Grid (Ctrl+') and Show Guides (Ctrl+;) (IP-0080). Done when: both toggle overlays without entering history.
- [ ] Add `GridSettings` in `src/Imago/Photon.Imago.Core/Guides/GridSettings.cs` (IP-0081): spacing in units, subdivisions, style (lines, dashed, dots, or intersection crosses), color, opacity, and offset, per document as `<imago:grid>` with `Imago.Grid.*` defaults. Done when: `GridSettingsSerializationTests` round-trip every field.
- [ ] Add `AxisGrid` (IP-0082) for Affinity's Grid and Axis Manager types: basic, advanced with separate X and Y spacing, isometric, dimetric, trimetric, and oblique (axis angles and per-plane spacing). Done when: `AxisGridTests` assert isometric line angles of 30 and 150 degrees.
- [ ] Add the Grid and Axis Manager dialog configuring `GridSettings` and `AxisGrid`. Done when: a capture of an isometric grid is committed.
- [ ] Add `GridOverlay` in `src/Imago/Photon.Imago.Rendering/Overlays/GridOverlay.cs`. Done when: it draws under 1 ms per 1080p frame (measurement quoted).
- [ ] Move the geometry-agnostic snapping parts of `D02 T07 §11` (`SnapCandidate`, `SnapResult`, the radius and priority ranking, and the equal-spacing and distance-label math of `SmartGuideProvider`) from `src/Nodus/Photon.Nodus.Core/Snapping/` into `src/Photon.Core/Snapping/`; Nodus's providers stay in Nodus. Done when: Nodus's snapping tests pass unchanged and `grep -rn "class SnapResult" src` finds one definition.
- [ ] Add Imago snap providers in `src/Imago/Photon.Imago.Core/Snapping/` (IP-0084, IP-0085, IP-0087): guides, grid including axis grids, layer visual bounds (non-transparent extent cached per layer version), canvas edges and center, artboard edges and margins (registered by `D03 T09 §13`), and selection and pixel-selection bounds. Done when: `ImagoSnapProviderTests` snap a point to each family.
- [ ] Route the Move, crop, and selection tools through the snapping engine; path and shape key points are registered by `D03 T16 §5` and `§7`, and slices by `D03 T18 §3`. Done when: a driven crop edge snaps to a guide.
- [ ] Add equidistance, gap, and size candidates from the shared core, and smart guides drawing alignment lines and distance labels while moving layers or selections (`Imago.SmartGuides.Enabled`) (IP-0083, IP-0086, IP-0090). Done when: moving a layer between two others shows equal-spacing labels in a capture.
- [ ] Add Force Pixel Alignment (`Imago.Snap.ForcePixelAlignment`), Move by Whole Pixels (`Imago.Snap.MoveByWholePixels`), and the snapping toggle Shift+Ctrl+; (IP-0088, IP-0092). Done when: a transform with the first on lands on integer pixels.
- [ ] Add the Snapping Manager (IP-0084, IP-0089, IP-0091, IP-0093): master toggle, Snap To All and None, per-candidate checks, tolerance `Imago.Snap.TolerancePx` (default 8), presets `Imago.Snap.Presets`, only visible layers, and a per-layer Exclude from Snapping flag persisted through §1. Done when: an excluded layer never snaps and the flag survives reopen.
- [ ] Measure snap candidate search with 500 layers and 200 guides. Done when: it stays under 1 ms per pointer move (measurement quoted).
- [ ] Add Rulers and Units, Guides, Grids, and Snapping pages to `docs/user/imago/`. Done when: every command and dialog above is covered.
- [ ] Commit: `"imago: rulers, units, guides, grids, and snapping on shared cores"`

**Test checkpoint:** Unit test plus format fidelity proof plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~GuideCommandTests|FullyQualifiedName~GuideSerializationTests|FullyQualifiedName~GridSettingsSerializationTests|FullyQualifiedName~AxisGridTests|FullyQualifiedName~ImagoSnapProviderTests|FullyQualifiedName~UnitConverterTests"` exits 0, `GuideSerializationTests` reopen `layout.imago` and the Photoshop-produced `guides.psd` with every guide equal, and a driven guide layout, grid, and snapped layer move are captured. Cheaper substitute that fails: a second unit table in Imago, which the single-definition grep catches.

**Freeze check:** Guides, grid, units, and snapping exclusions are written as registered §1 document parts through the atomic writer; a document with none of them saves byte-identical to the pre-change writer (`GuideSerializationTests.NoGuidesUnchanged`). Fixture source: `tests/fixtures/imago/guides/` (created by this section).

## 5. Measure, protractor, count, and notes

Scientific, print, and forensic users measure in real units, count features, and annotate, and none of it may touch pixels. This section adds the measure tool with a protractor, region metrics, a measurement scale with scale markers, a recorder and Measurement Log with CSV export, the Count tool with automatic counting, and notes, all stored in the §1 document block. The measure tool records no history; everything else is one undo step. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0094 to IP-0107 (14 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/measure/, docs/captures/imago/measurement-log/, docs/captures/imago/count/, and docs/captures/imago/notes/.
**Job:** a user can measure distances, angles, and areas in real-world units, count features, keep a log they can export, and leave notes on the image. Consumer: the Measurement Log and its CSV export, and the save, which persists scale, counts, notes, and measurements.
**Treatment:** the Ruler (measure), Count, and Note tools on one flyout with options-bar readouts, Analysis menu commands, and dockable Measurement Log and Notes panels; markers draw on the overlay, never into pixels. Cheaper substitute that fails the checkpoint: readouts in pixels only, which the scale test catches.
**Chrome:** consume §4's `UnitConverter` and snapping, the overlay layer, the atomic writer for CSV, and AvalonDock. Do not add a second readout surface.

**Requires:** display-session -- the measure, count, and note tools on the canvas need an interactive desktop

- [ ] Add `MeasureTool` in `src/Imago/Photon.Imago.Core/Tools/MeasureTool.cs` (IP-0094): drag a line, Shift constrains to 45 degrees, options-bar readouts X, Y, W, H, A, L1, and L2 in current units, recording no history. Done when: `MeasureToolTests` assert distance on known points and the history length is unchanged.
- [ ] Add the protractor (IP-0095): Alt-drag from an endpoint adds a second arm and the readout shows the angle between arms, plus GIMP's optional info window. Done when: `MeasureToolTests.Protractor` asserts 90 degrees on a right angle.
- [ ] Add the Straighten Layer button handing the measured angle to §9's straighten. Done when: a driven straighten from a measured 3-degree line levels the horizon.
- [ ] Add `RegionMetrics` in `src/Imago/Photon.Imago.Core/Analysis/RegionMetrics.cs` (IP-0096): area by coverage-weighted pixel count, perimeter by border following (Suzuki and Abe 1985) on the selection or layer alpha, circularity 4 pi A over P squared, height, and width, in scale units. Done when: `RegionMetricsTests` measure a radius-50 disk's area within 0.5 percent and circularity above 0.99. Cheaper substitute: a bounding-box area.
- [ ] Add hover distances (IP-0097): with a layer or selection active, Ctrl-hover shows distances to the layer under the pointer and to the canvas edges. Done when: a capture shows the four distance labels.
- [ ] Add `MeasurementScale` in `src/Imago/Photon.Imago.Core/Analysis/MeasurementScale.cs` (IP-0098): pixel length, logical length, and logical units stored in the §1 block. Done when: a scale of 100 px to 1 cm survives reopen.
- [ ] Add Analysis, Set Measurement Scale with presets (`Imago.Measure.ScalePresets`) and "from the current measure line". Done when: setting from a 200 px line to 2 mm makes the readouts show millimetres.
- [ ] Add Place Scale Marker (IP-0099): length, label font and size, text, color, and bar, creating a `scale-marker` live layer registered with §1 that re-renders when the scale changes (a text layer once `D03 T16 §1` lands). Done when: changing the scale re-renders the marker and the layer reopens live.
- [ ] Add `MeasurementRecorder` in `src/Imago/Photon.Imago.Core/Analysis/MeasurementRecorder.cs` (IP-0100): Analysis, Record Measurements over the selection, measure line, or count, with the data points chosen in `Imago.Measure.DataPoints` (label, date and time, document, source, scale, scale units and factor, count, area, perimeter, circularity, height, width, gray minimum, maximum, mean, and median, integrated density, histogram). Done when: a recorded selection carries every chosen data point.
- [ ] Add the Measurement Log panel `src/Imago/Photon.Imago.Desktop/Views/Panels/MeasurementLogPanel.xaml` (IP-0101): one row per record, sort by column, select, and delete, saved with the document as `<imago:measurements>`. Done when: the log survives save and reopen.
- [ ] Add CSV export of the log (RFC 4180, UTF-8) through the atomic writer. Done when: `MeasurementLogExportTests` assert quoting of a label with a comma and a quote.
- [ ] Add `Note` (position, author `Imago.Notes.Author`, color, text, created) stored in the §1 block, and the Note tool (IP-0102). Done when: `NotesSerializationTests` round-trip two notes.
- [ ] Add Show Notes as an Extras item, Clear All, and a Notes panel with previous and next (IP-0103, IP-0107). Done when: previous and next move the view to each note in a driven run.
- [ ] Map the PSD annotations resource in the `D03 T04 §5` adapter on read; PSD write and full read are `D03 T17 §2` and `§3`. Done when: a Photoshop-produced `notes.psd` (version recorded) opens with its text notes.
- [ ] Add the Count tool (IP-0104, IP-0105) with numbered markers, count groups (name, color, visibility), marker and label sizes, Clear, and Show Count. Done when: counts in two groups survive reopen with their colors.
- [ ] Add `ConnectedComponents` in `src/Imago/Photon.Imago.Core/Analysis/ConnectedComponents.cs` and Automatic Count from Selection (IP-0106) counting 8-connected components of the selection mask above a minimum size. Done when: `ConnectedComponentsTests` count five blobs and ignore one below the minimum.
- [ ] Name undo steps "Add Note", "Add Count Marker", "Set Measurement Scale", "Record Measurement", and "Place Scale Marker", each writing one Information line; the measure tool writes none. Done when: a driven run logs one line per step (quoted).
- [ ] Add Measure, Count, Notes, and Measurement Log pages to `docs/user/imago/`. Done when: every tool, command, and panel above is covered.
- [ ] Commit: `"imago: measure, measurement log, count, and notes"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~MeasureToolTests|FullyQualifiedName~RegionMetricsTests|FullyQualifiedName~ConnectedComponentsTests|FullyQualifiedName~MeasurementLogExportTests|FullyQualifiedName~NotesSerializationTests"` exits 0, and a driven run sets a scale from a measured line, records a selection's area, auto-counts five blobs, and exports the log (the CSV committed under docs/captures/imago/measurement-log/ as evidence). Cheaper substitute that fails: a bounding-box area, which the disk-area test catches.

**Freeze check:** Scale, notes, counts, and measurements are written as registered §1 document parts through the atomic writer; a document with none saves byte-identical to the pre-change writer (`NotesSerializationTests.NoNotesUnchanged`). Fixture source: `tests/fixtures/imago/analysis/` (created by this section).

## 6. History extensions: snapshots, non-linear history, and saved history

Today's undo is two linear lists that die with the process. `D01 T02 §4` moves the suite history to `Photon.Core`; this section builds Imago's history tree over it with non-linear branches, copy-on-write snapshots, history saved with the document, and a history log, extending `D03 T03 §2`'s History panel rather than replacing it. It must not add a second undo stack, and a snapshot must copy no pixels until tiles diverge. It serves the acceptance-bar aims "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog" and "Editing stays non-destructive". Catalog: IP-0129 to IP-0141 (13 features).

**Fidelity:** docs/captures/imago/history/ (baseline from `D03 T03 §2`); new captures to docs/captures/imago/snapshots/.
**Job:** a user can try alternatives, keep named states, come back to them after reopening, and prove what was done to an image. Consumer: the History panel, the save, which persists snapshots and history, and the XMP history exported by `D03 T17 §10`.
**Treatment:** the History panel gains a snapshot area, branch rows, thumbnails and timestamps in an advanced view, and a scrub slider; a History Options dialog; File, New from state. Cheaper substitute that fails the checkpoint: snapshots as full-document copies, which the allocation test catches.
**Chrome:** consume the `D01 T02 §4` history and `D03 T03 §2`'s panel and `TileSnapshotCommand` (extended, not replaced). Do not add a second undo stack.

**Requires:** display-session -- the History panel, slider, and branch jumps need an interactive desktop

- [ ] Add `HistoryTree` in `src/Imago/Photon.Imago.Core/History/HistoryTree.cs` over the suite `UndoHistory` (`D01 T02 §4`), linear by default. Done when: with non-linear off, an edit after undo discards the redo branch exactly as today.
- [ ] Add Allow Non-Linear History (`Imago.History.AllowNonLinear`, IP-0136): an edit after an undo keeps the abandoned branch, and selecting any state replays undo and redo along the tree path. Done when: `HistoryTreeTests` show a branch survives an edit after undo and jumping to it restores the pixel hash.
- [ ] Show branches as indented rows in the History panel. Done when: a capture with one branch is committed.
- [ ] Add snapshot capture (IP-0133, IP-0135) From Full Document, Merged Layers, or Current Layer with a name, sharing tiles copy-on-write through reference counts on the `D03 T02 §1` tile store. Done when: `SnapshotCopyOnWriteTests` measure zero tile allocations at capture. Cheaper substitute: a deep copy of the document.
- [ ] Add Restore Snapshot as one history step "Restore Snapshot", and Delete Snapshot. Done when: restore returns the snapshot's pixel hash and undo reverses it.
- [ ] Add History Options (IP-0135): automatically create the first snapshot, new snapshot on save, show the New Snapshot dialog by default, and make layer visibility changes undoable (`Imago.History.VisibilityUndoable`). Done when: each option changes behavior in a driven run (settings readback quoted).
- [ ] Add `IPersistableCommand` (kind, JSON parameters, tile payload references) in `src/Imago/Photon.Imago.Core/History/IPersistableCommand.cs` and implement it on the tile-snapshot, property, and layer commands. Done when: each implementing command round-trips through JSON in `SavedHistoryRoundTripTests.CommandPersistence`.
- [ ] Save snapshots and, when `Imago.History.SaveWithDocument` or the per-document flag is on, the full history through §1 as `<imago:history>` with payloads under `imago/history/` (IP-0133, IP-0138, IP-0139). Done when: `SavedHistoryRoundTripTests` save, reopen, undo three steps, and equal the pre-edit hash.
- [ ] Cut the saved history before a command that cannot persist and say so in the save summary. Done when: a test-only non-persistable command yields a history starting after it and the summary names it.
- [ ] Add Toggle Last State (IP-0129). Done when: it alternates between the last two states in a driven run.
- [ ] Add a History slider scrubbing states with a live preview (IP-0130), as Affinity does. Done when: dragging the slider previews each state without committing.
- [ ] Add the advanced view (IP-0131): 64-pixel thumbnails from the mip cache when a step completes, memory capped by `Imago.History.ThumbnailBudgetMB`, and timestamps. Done when: past the cap, the oldest thumbnails are dropped and redrawn on demand.
- [ ] Add Delete State (and every later state) and Clear History with a confirmation (IP-0132). Done when: Cancel on the confirmation leaves the history intact.
- [ ] Add File, New Document from a state or snapshot (IP-0134). Done when: the new untitled document carries the state's pixel hash.
- [ ] Add New Layer from Snapshot (IP-0140) as one undoable step "New Layer from Snapshot". Done when: undo removes the layer.
- [ ] Add `HistoryLogWriter` in `src/Imago/Photon.Imago.Core/History/HistoryLogWriter.cs` (IP-0137, IP-0141) writing Sessions Only, Concise, or Detailed entries to the document's XMP history in the §1 block (exported by `D03 T17 §10`), to a text file (`Imago.History.LogFile`), or both (`Imago.History.LogTarget`, `Imago.History.LogDetail`), the file through the atomic writer. Done when: `HistoryLogWriterTests` assert each detail level's lines.
- [ ] Write one Serilog Information line for snapshot create, restore, and delete and for history save. Done when: a driven run logs each (quoted).
- [ ] Measure a snapshot of a 100-megapixel 16-bit document and the saved history of 50 brush strokes. Done when: the snapshot allocates under 1 MB until tiles diverge and the saved history adds at most twice the strokes' touched-tile bytes (both quoted).
- [ ] Commit `tests/fixtures/imago/history/three-strokes.imago` with its committed pre-edit hash. Done when: the fixture and hash file are committed.
- [ ] Add History, Snapshots, and History Log pages to `docs/user/imago/`. Done when: every option and command above is covered.
- [ ] Commit: `"imago: snapshots, non-linear history, and history saved with the document"`

**Test checkpoint:** Unit test plus format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~HistoryTreeTests|FullyQualifiedName~SnapshotCopyOnWriteTests|FullyQualifiedName~SavedHistoryRoundTripTests|FullyQualifiedName~HistoryLogWriterTests"` exits 0; `SavedHistoryRoundTripTests` reopens `tests/fixtures/imago/history/three-strokes.imago` and undoes to the committed pre-edit hash, and `SnapshotCopyOnWriteTests` measures zero tile allocations at capture. Cheaper substitute that fails: a snapshot that deep-copies the document, which the allocation assertion catches.

**Freeze check:** Snapshots and saved history are written as a registered §1 document part through the atomic writer and only when a snapshot exists or saving history is on; a document with neither saves byte-identical to the pre-change writer (`SavedHistoryRoundTripTests.NoHistoryUnchanged`); killing the process mid-save leaves the original byte-identical. Fixture source: `tests/fixtures/imago/history/` (created by this section).

## 7. The Image menu: canvas, rotation, trim, reveal, and resampling

The Image menu of `D03 T03 §7` covers Image Size, Canvas Size, 90-degree rotation, and flips. This section completes it with the Photoshop, Affinity, and GIMP canvas commands (relative Canvas Size with offsets, arbitrary rotation, crop to selection, trim, zealous crop, reveal all, fit and clip canvas, slice using guides), an extended Image Size with Print Size, and the shared `Resampler` of `D01 T03 §2` extended in place with every competitor method, Preserve Details, and pixel-art scalers. It must not add a second resampler in Imago. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0142 to IP-0163 (22 features).

**Fidelity:** docs/captures/imago/image-size/ and docs/captures/imago/canvas-size/ (baselines from `D03 T03 §7`); new captures to docs/captures/imago/image-menu/.
**Job:** a user can resize, resample, rotate, trim, and reshape the canvas with the exact method and units the job needs and see the result before committing. Consumer: the document, through one `TileSnapshotCommand` per command.
**Treatment:** extended Image Size and Canvas Size dialogs with a 1:1 preview pane, Print Size and Rotate Canvas dialogs, and Image menu commands. Cheaper substitute that fails the checkpoint: resampling through `SKBitmap.Resize`, which has no NoHalo or Lanczos goldens.
**Chrome:** consume `D01 T03 §2`'s `Resampler` and `Rotator` (extended in place), `TileSnapshotCommand`, the §4 converter, and `Photon.UI` dialog styles. Do not add a second resampler in Imago.

**Requires:** display-session -- the dialogs and their preview need an interactive desktop

- [ ] Extend Canvas Size (IP-0142, IP-0143) with Relative, the anchor grid, and extension color (foreground, background, white, black, gray, other; transparent on non-background layers), one command "Canvas Size". Done when: `CanvasCommandTests.Relative` grows a 100 px canvas by 20 px anchored top-left with the new area in the chosen color.
- [ ] Add GIMP's X and Y offsets with Center and Resize Layers (none, all, image-sized, visible) to Canvas Size. Done when: `CanvasCommandTests.Offsets` assert layer positions for each Resize Layers option.
- [ ] Add Image, Image Rotation, Arbitrary (IP-0144) through `Rotator` (`D01 T03 §2`) per layer, growing the canvas to hold the result; 90 and 180 degrees and flips stay `D03 T03 §7`'s. Done when: a 30-degree rotation keeps every corner pixel inside the new canvas.
- [ ] Add Crop to Selection with Delete Cropped Pixels (IP-0145). Done when: with Delete off, the cropped pixels reappear after Reveal All.
- [ ] Add Trim (IP-0146, IP-0160) by transparent pixels, top-left color, or bottom-right color with per-side checkboxes, also offered as GIMP's Crop to Content. Done when: `CanvasCommandTests.Trim` asserts the bounds for each mode.
- [ ] Add Zealous Crop (IP-0147) removing uniform rows and columns anywhere in the image. Done when: `CanvasCommandTests.ZealousCrop` removes an interior uniform band.
- [ ] Add Reveal All, Fit Canvas to Layers, Fit Canvas to Selection, and Clip Canvas (IP-0148, IP-0149, IP-0150). Done when: `CanvasCommandTests.FitAndReveal` assert each on known layer bounds.
- [ ] Add Slice Using Guides (IP-0151) creating untitled documents from the guide cells, refused by name above 500 cells ("Slice Using Guides would create N documents; the limit is 500."). Done when: a 2 by 3 guide grid yields six documents.
- [ ] Extend Image Size (IP-0152, IP-0153) with Constrain Proportions, units including percent, points, picas, and columns (§4 converter), Resample off (print size only), and separate X and Y resolution. Done when: resample off leaves the pixel hash unchanged.
- [ ] Add the 1:1 preview pane of the resampled result to Image Size (IP-0156). Done when: the preview updates within 200 ms on a 24-megapixel fixture.
- [ ] Add Fit To presets (IP-0157): 4 by 6 in, 5 by 7 in, 8 by 10 in at 300 ppi, 1024 by 768, 1280 by 800, 1366 by 768 at 72 ppi, and saved `Imago.ImageSize.Presets`. Done when: a saved preset appears after restart.
- [ ] Add Auto resolution from a screen frequency (lines per inch times 1.5 for Good or 2 for Best) and Fit Image (fit within W by H with Don't Enlarge) (IP-0162). Done when: 150 lpi Best gives 300 ppi and Don't Enlarge leaves a small image unchanged.
- [ ] Add the Print Size dialog (IP-0159) with width, height, and X and Y resolution that change resolution only and never resample. Done when: `PrintSizeTests` prove the pixel hash unchanged.
- [ ] Add Scale Styles (IP-0158): the resize command calls `IScalableLayerContent.Scale(factor)` on every layer's live content; `D03 T09 §7` registers layer effects, and until it ships the checkbox is disabled with a tooltip naming it. Done when: a probe live layer's parameter scales by the factor.
- [ ] Extend `Resampler` in `src/Photon.Core/Imaging/Geometry/` (`D01 T03 §2`) in place with `Automatic` (Bicubic Sharper when reducing, Preserve Details when enlarging), `BicubicSmoother` (Mitchell-Netravali B = C = 1/3), and `BicubicSharper` (Keys cubic with a = -1), documented as Imago's readings of Photoshop's options (IP-0154). Done when: `ResamplerExtensionTests` assert each kernel's weights at known offsets. Cheaper substitute: `SKBitmap.Resize`.
- [ ] Add `Lanczos2` and `Lanczos3NonSeparable` (radial, as Affinity offers) to the same `Resampler`. Done when: they match libvips 8.16 goldens within 2/255.
- [ ] Add `NoHalo` and `LoHalo` translated from GEGL 0.4 (LGPL-3.0-or-later, headers kept) with a `docs/dev/decisions.md` row recording the license. Done when: they match GIMP 3.2.6 `gimp-console` goldens within 2/255.
- [ ] Add `DetailPreservingUpscaler` beside the resampler (IP-0155, IP-0163): Lanczos-3 upscale plus a guided-filter detail layer (He, Sun, and Tang 2010) with a Reduce Noise slider that smooths the base; "Preserve Details 2.0" runs the same classical engine with a 1:1 preview and says so; AI upscaling is `D03 T19 §8`. Done when: a 2x upscale of a fixture has higher gradient energy than Lanczos-3 alone (figures quoted).
- [ ] Add pixel-art scalers (IP-0161) hq2x, hq3x, hq4x (Maxim Stepin's algorithm) and xBR 2x, 3x, 4x (Hyllian) as `ResampleMode` values, integer factors only, others refused by name. Done when: they match FFmpeg 7.1 `hqx` and `xbr` goldens exactly.
- [ ] Commit resampling goldens under `tests/fixtures/imaging/resample-ext/` with each fixture's reference command in `reference.txt`. Done when: every golden has its command and tool version.
- [ ] Make every command one undo step through `TileSnapshotCommand` with progress and cancel above 16 megapixels. Done when: cancelling a 100-megapixel resample leaves the document unchanged.
- [ ] Log one Information line per command (command, old and new size, method, milliseconds). Done when: a driven resize logs one line (quoted).
- [ ] Measure a 100-megapixel Lanczos resample against the `D01 T03 §2` memory ceiling. Done when: peak working set stays under the ceiling (quoted).
- [ ] Add Image Size, Canvas Size, Print Size, Trim, and Resampling Methods pages to `docs/user/imago/`. Done when: every command and method above is covered.
- [ ] Commit: `"imago: the Image menu with canvas, trim, and extended resampling"`

**Test checkpoint:** Unit test plus format fidelity proof against goldens: `dotnet test Photon.slnx --filter "FullyQualifiedName~CanvasCommandTests|FullyQualifiedName~ResamplerExtensionTests|FullyQualifiedName~PrintSizeTests"` exits 0; `ResamplerExtensionTests` match GIMP 3.2.6 NoHalo and LoHalo within 2/255, libvips 8.16 Lanczos-2 within 2/255, and FFmpeg 7.1 hqx and xBR exactly (reference commands in each fixture's `reference.txt`), and `PrintSizeTests` prove the pixel hash unchanged. Cheaper substitute that fails: mapping NoHalo to bicubic, which the NoHalo golden rejects.

## 8. Clipboard and paste variants

Cut, Copy, and Paste only log today. This section builds one clipboard service that writes PNG with straight alpha, `CF_DIBV5`, and a private live-layer format, then every Photoshop, Affinity, and GIMP cut, copy, and paste variant, floating paste, named buffers with a Buffers panel, Paste Special, and Purge. It extends §2's `ClipboardImageReader` and must not add a second clipboard wrapper; live layers paste live between Imago windows through §1's contract. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0164 to IP-0180 (17 features).

**Fidelity:** docs/captures/imago/main-window/ for the Edit menu; new captures to docs/captures/imago/buffers/ and docs/captures/imago/paste-special/.
**Job:** a user can move pixels and live layers between documents and other apps exactly where they need them. Consumer: the Windows clipboard, other apps reading PNG and DIBV5, and Imago windows reading the private layer format.
**Treatment:** Edit menu and Edit, Paste Special submenus, a Paste Special dialog listing the formats present, and a Buffers panel. Cheaper substitute that fails the checkpoint: a clipboard that carries only flattened 8-bit RGB, which the alpha and live-layer tests catch.
**Chrome:** consume §2's `ClipboardImageReader` (extended), §1's contract for live layers, `TileSnapshotCommand`, and AvalonDock. Do not add a second clipboard wrapper.

**Requires:** display-session -- clipboard exchange with other apps and the Buffers panel need an interactive desktop

- [ ] Add `ImagoClipboard` in `src/Imago/Photon.Imago.Desktop/Clipboard/ImagoClipboard.cs` writing PNG (straight alpha) and `CF_DIBV5`, with delayed rendering for large copies. Done when: `ClipboardFormatTests` round-trip PNG alpha and DIBV5 straight and premultiplied conversion. Source: https://learn.microsoft.com/windows/win32/dataxchg/standard-clipboard-formats
- [ ] Add the private `Photon.Imago.Layers` format serializing the copied layers through §1 so live layers paste live between Imago windows. Done when: `LiveLayerClipboardTests` paste a probe live layer live.
- [ ] Add `Imago.Clipboard.ExportOnExit`, rendering delayed formats on exit. Done when: with it on, a copy survives closing Imago and pastes in another app.
- [ ] Replace the log-only Cut, Copy, and Paste in `src/Imago/Photon.Imago.Desktop/ViewModels/MainWindowViewModel.cs` with commands over `ImagoClipboard` (IP-0164). Done when: `grep -n "requested" MainWindowViewModel.cs` finds no clipboard stub.
- [ ] Add Copy Merged (Shift+Ctrl+C, GIMP's Copy Visible) and Clear (IP-0168, IP-0172, IP-0176, IP-0177) on the selected layers. Done when: Copy Merged carries the composite of the selection.
- [ ] Add Cut across a layer group (IP-0175) as one step over every layer in the selected group. Done when: one undo restores every layer.
- [ ] Add Paste centered in the view or selection, and Paste in Place (Shift+Ctrl+V) (IP-0165, IP-0166). Done when: `PasteVariantTests` assert both positions.
- [ ] Add Paste Into (new layer masked by the selection; Affinity's Paste Inside makes it a clipped child) and Paste Outside (inverted mask) (IP-0173). Done when: `PasteVariantTests.PasteInto` asserts the mask equals the selection.
- [ ] Add Paste as New Layer with optional in place, and Paste as New Image through §2's `DocumentFactory` (IP-0178). Done when: Paste as New Image creates a document of the clipboard size.
- [ ] Add the `FloatingLayer` kind (IP-0167), GIMP's floating selection, attached to its target with Anchor (Ctrl+H) and To New Layer (Shift+Ctrl+N); `D03 T10 §1` floats selections into the same kind. Done when: `FloatingLayerTests` anchor into the target in one step.
- [ ] Add `BufferStore` in `src/Imago/Photon.Imago.Core/Clipboard/BufferStore.cs` (IP-0169) with Cut Named, Copy Named, and Copy Visible Named, tiles shared copy-on-write, capped by `Imago.Clipboard.MaxBuffers`. Done when: `BufferStoreTests` assert no tile copy at store time and eviction past the cap.
- [ ] Add the Buffers panel `src/Imago/Photon.Imago.Desktop/Views/Panels/BuffersPanel.xaml` (IP-0170) in list or grid with paste, paste into, paste as new layer, paste as new image, and delete. Done when: each command works in a driven run and the capture is committed.
- [ ] Add the Paste Special dialog (IP-0174) listing the formats present (private layers, PNG, DIBV5, DIB, text, SVG, EMF) and pasting the chosen one. Done when: choosing DIB pastes without alpha as expected.
- [ ] Disable the SVG and EMF entries and Prefer Metafile When Pasting (`Imago.Clipboard.PreferMetafile`, IP-0180) with a tooltip naming `D03 T17 §7` until its readers ship. Done when: the tooltip names the section and `python scripts/todo-graph.py resolve 'D03 T17 §7'` does not exit 1 or 2.
- [ ] Register Paste without Formatting (IP-0179), pasting plain text into a text layer in edit mode, enabled by `D03 T16 §1` with a tooltip naming it until then. Done when: the item is disabled with the tooltip.
- [ ] Add Edit, Purge (IP-0171): Clipboard, Histories (all documents, with a confirmation), and All; the video cache purge follows backlog B-043 and is absent. Done when: Purge Histories empties every open document's history after the confirmation.
- [ ] Name undo steps "Paste", "Paste in Place", "Paste Into", "Paste Outside", "Cut", and "Clear", with one Information line per paste (variant, format, and pixel size). Done when: a driven run logs one line per paste (quoted).
- [ ] Add Clipboard, Paste Variants, and Buffers pages to `docs/user/imago/`. Done when: every command above is covered.
- [ ] Commit: `"imago: clipboard, paste variants, and named buffers"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ClipboardFormatTests|FullyQualifiedName~PasteVariantTests|FullyQualifiedName~BufferStoreTests|FullyQualifiedName~FloatingLayerTests|FullyQualifiedName~LiveLayerClipboardTests"` exits 0, and a driven run copies a transparent layer from Imago into another app and back (alpha hash quoted) and pastes a live layer between two Imago windows. Cheaper substitute that fails: copying a flattened 24-bit DIB, which the alpha round trip catches.

## 9. Crop and straighten extensions

`D03 T03 §7` ships a crop tool with thirds and Delete Cropped Pixels. This section extends it with presets and numeric crop, center and selected-layer options, straighten, every overlay with cycling, classic mode and shield options, crop beyond the canvas with a fill hook that `D03 T13 §3` registers content-aware fill into, auto shrink, and the Perspective Crop tool on `D01 T03 §2`'s homography. It must not add a second rotation routine. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0181 to IP-0200 (20 features).

**Fidelity:** docs/captures/imago/main-window/ for the crop options bar (baseline from `D03 T03 §7`); new captures to docs/captures/imago/crop/ and docs/captures/imago/perspective-crop/.
**Job:** a user can crop to an exact size, ratio, or print format, straighten while cropping, and correct perspective in one step. Consumer: the document, through one "Crop" or "Perspective Crop" command.
**Treatment:** the crop options bar gains presets, swap, clear, numeric fields, overlay and shield menus; the Perspective Crop tool shares the flyout. Cheaper substitute that fails the checkpoint: a straighten that rotates without cropping to the largest rectangle, which the geometry test catches.
**Chrome:** consume `D03 T03 §7`'s crop tool (extended), `D01 T03 §2`'s `Rotator` and `PerspectiveCorrector`, §4's snapping, and the settings store. Do not add a second rotation routine.

**Requires:** display-session -- crop interaction and overlays need an interactive desktop

- [ ] Add crop presets (IP-0181, IP-0195) to the crop options bar: Unconstrained, Original Ratio, ratio, W by H by resolution, fixed aspect or size, units, and DPI with Resample, saved and deleted in `Imago.Crop.Presets`. Done when: `CropPresetStoreTests` round-trip a saved preset.
- [ ] Add Swap (X) and Clear (IP-0182). Done when: Swap turns 4 by 5 into 5 by 4.
- [ ] Add numeric X, Y, W, and H fields in the options bar (IP-0183). Done when: typed values move the crop box exactly.
- [ ] Add Expand from Center and Selected Layers Only (GIMP's current layer only) (IP-0184); Delete Cropped Pixels stays `D03 T03 §7`'s. Done when: Selected Layers Only crops one layer and leaves the canvas size.
- [ ] Add Auto Shrink to content with Shrink Merged (IP-0193). Done when: the box shrinks to the non-transparent bounds of the layer or composite.
- [ ] Add straighten (IP-0185, IP-0196): draw a line with the Straighten control or take the angle from §5's Measure tool, then crop through `Rotator.CropToRotatedRect` (`D01 T03 §2`). Done when: `CropGeometryTests` assert the straighten angle yields the largest axis-aligned rectangle.
- [ ] Add rotate the crop box by dragging outside it (IP-0190). Done when: a driven drag rotates the box and the commit rotates the image.
- [ ] Add overlays (IP-0186, IP-0187, IP-0197): thirds (existing), grid, diagonal, triangle, golden ratio, and golden spiral; O cycles, Shift+O cycles orientation; display Always, Auto, or Never. Done when: `CropGeometryTests.GoldenSpiral` asserts the spiral geometry and each overlay is captured.
- [ ] Add Affinity's darken border and reveal canvas overlay options (IP-0200). Done when: both render in a capture.
- [ ] Add Classic Mode (the box rotates, not the image) (IP-0188). Done when: in classic mode the view does not rotate during a box rotation.
- [ ] Add Show Cropped Area, Auto Center Preview, and the shield color and opacity with Auto Adjust Opacity (IP-0189). Done when: each changes the overlay in a capture.
- [ ] Add crop beyond the canvas (IP-0191, IP-0192): the canvas grows and the new area fills transparent or with the background. Done when: a crop 50 px beyond each edge grows the canvas by 100 px each way.
- [ ] Add `ICanvasExtensionFill` in `src/Imago/Photon.Imago.Core/Tools/Crop/ICanvasExtensionFill.cs` (IP-0199), the hook `D03 T13 §3` registers content-aware fill into; the Content-Aware checkbox is disabled with a tooltip naming it until then, and generative expand is `D03 T19 §4`. Done when: a test-only fill registered through the hook fills the grown area.
- [ ] Add the Perspective Crop tool (IP-0194): four draggable corners, W, H, and resolution, Front Image, and Show Grid, resampled through `PerspectiveCorrector`'s four-point homography (`D01 T03 §2`). Done when: `PerspectiveCropTests` match an ImageMagick 7.1 `-distort Perspective` golden within 2/255. Cheaper substitute: an affine skew.
- [ ] Add modifiers (IP-0198): Shift constrains, arrows nudge, Ctrl overrides §4's snapping, and Alt resizes around the center. Done when: each works in a driven run.
- [ ] Make each crop one undo step "Crop" or "Perspective Crop" with one Information line (box, angle, size, method). Done when: undo restores the canvas and a driven crop logs one line (quoted).
- [ ] Commit the perspective-crop fixture and golden under `tests/fixtures/imago/crop/` with the ImageMagick command in `reference.txt`. Done when: the fixture, golden, and command are committed.
- [ ] Add Crop Tool and Perspective Crop pages to `docs/user/imago/`. Done when: every option above is covered.
- [ ] Commit: `"imago: crop presets, straighten, overlays, and perspective crop"`

**Test checkpoint:** Format fidelity proof against a golden plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~PerspectiveCropTests|FullyQualifiedName~CropGeometryTests|FullyQualifiedName~CropPresetStoreTests"` exits 0 with `PerspectiveCropTests` matching the ImageMagick 7.1 golden within 2/255, and a driven crop with a 4 by 5 preset and a straighten line is captured under docs/captures/imago/crop/. Cheaper substitute that fails: a perspective crop by affine skew, which the homography golden rejects.

## 10. Windows, arrangement, view modes, display filters, and the navigator

With §3's per-window view state in place, a document can have several views, and views can be arranged, matched, split, filtered, and navigated. This section adds New Window, the arrange and match commands, shrink wrap, Affinity's view modes and split view, a view-only display filter stack, the Navigator panel with saved view points, and the Images panel. Display filters apply to display tiles only: they must never change document pixels or exports. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0052 to IP-0067 (16 features).

**Fidelity:** docs/captures/imago/main-window/ for the Window menu; new captures to docs/captures/imago/navigator/, docs/captures/imago/display-filters/, and docs/captures/imago/split-view/.
**Job:** a user can look at the same image several ways at once, compare, spot clipping, and jump to saved places. Consumer: the viewport, which renders each view through its own `ViewState` and filter stack.
**Treatment:** Window, Arrange commands over AvalonDock, a split-view divider on the canvas, a Display Filters dialog per view, and dockable Navigator and Images panels. Cheaper substitute that fails the checkpoint: a clip warning drawn by modifying layer pixels, which the unchanged-document hash catches.
**Chrome:** consume AvalonDock, §3's `ViewState`, `D03 T02 §2`'s `MipTileCache` for thumbnails, the GPU path of `D03 T02 §5`, and the icon catalog. Do not add a second thumbnail renderer.

**Requires:** display-session -- window arrangement, split view, and panel captures need an interactive desktop

- [ ] Add Window, New Window (IP-0052, IP-0064): a second view on the same `ImagoDocument` with its own `ViewState`, sharing history, selection, and dirty state, titled `name:2`; closing the last view closes the document with the usual prompt. Done when: an edit in one view shows in the other and closing one view does not prompt.
- [ ] Add a layout model `src/Imago/Photon.Imago.Desktop/View/WindowArrangement.cs` over AvalonDock (IP-0053, IP-0063): Consolidate All to Tabs, Tile All Vertically and Horizontally, 2-up to 6-up layouts, Cascade, Float in Window, and Float All in Windows. Done when: `WindowArrangementTests` assert the pane layout for 3-up and 6-up.
- [ ] Add Match Zoom, Match Location, Match Rotation, and Match All across open documents (IP-0064). Done when: Match All copies zoom, center, and rotation to every window.
- [ ] Add Shrink Wrap (Ctrl+J) and Center Image in Window (Shift+J) from GIMP (IP-0054). Done when: Shrink Wrap sizes a floating window to the image at the current zoom.
- [ ] Add `ViewMode { Pixels, RetinaPixels, Vector, Wireframe }` per view with `Imago.View.DefaultMode` (IP-0055): Retina renders at the monitor's device scale; Vector renders vector and text layer kinds at screen resolution and Wireframe draws their geometry and every layer's bounds, both falling back to Pixels until `D03 T16 §7` registers those kinds. Done when: Wireframe draws layer bounds in a capture.
- [ ] Add split view (IP-0056): a draggable vertical or horizontal divider, Affinity's split and mirrored split, each side with its own view mode and display filters. Done when: a capture shows Pixels on one side and Wireframe on the other.
- [ ] Add `DisplayFilterStack` in `src/Imago/Photon.Imago.Rendering/Display/DisplayFilterStack.cs` applied after compositing on display tiles only, per view, persisted in `Imago.View.DisplayFilters`. Done when: an export with every filter on matches the export with none.
- [ ] Add the Grayscale display filter (Rec. 709 luminance in the document's tone curve) (IP-0057). Done when: a pure red pixel displays at luminance 0.2126 in linear.
- [ ] Add the Clip Warning display filter (IP-0058, IP-0059): shadows, highlights, NaN and infinite float values, and alpha options for partially and fully transparent pixels, each with a color. Done when: `ClipWarningDisplayFilterTests` flag a 1.0, a 0.0, and a NaN float pixel and the document tile hash is unchanged. Cheaper substitute: colored pixels written into the composite.
- [ ] Add the Contrast and Gamma display filters (IP-0060). Done when: gamma 2.2 maps 0.5 to 0.5^(1/2.2) on display only.
- [ ] Add one GPU shader per filter under `src/Imago/Photon.Imago.Rendering/Shaders/` with CPU parity. Done when: `DisplayFilterGpuParityTests` match the CPU within 1/255 (skipped without a DirectX 12 device).
- [ ] Add the Display Filters dialog per view. Done when: each view keeps its own filters after a restart.
- [ ] Add the Navigator panel `src/Imago/Photon.Imago.Desktop/Views/Panels/NavigatorPanel.xaml` (IP-0061, IP-0067): thumbnail from the mip cache, draggable view box, zoom slider and buttons, and proxy view-box color `Imago.Navigator.ProxyColor`. Done when: dragging the box pans the view and the capture is committed.
- [ ] Add view points (IP-0062, IP-0066): named zoom, center, and rotation stored in the §1 block as `imago:views`, added from the Navigator, with View, Previous View Point and Next View Point. Done when: `ViewPointSerializationTests` round-trip two view points.
- [ ] List open documents in the Window menu and add the Images panel (IP-0065, GIMP) in list or grid with raise and new view. Done when: raise activates the document's window.
- [ ] Add Windows and Arrangement, View Modes, Display Filters, and Navigator pages to `docs/user/imago/`. Done when: every command and panel above is covered.
- [ ] Commit: `"imago: windows, view modes, display filters, and the navigator"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ClipWarningDisplayFilterTests|FullyQualifiedName~DisplayFilterGpuParityTests|FullyQualifiedName~ViewPointSerializationTests|FullyQualifiedName~WindowArrangementTests"` exits 0, and a driven run tiles three documents 3-up, matches zoom, opens a split view with Wireframe on one side, and captures the Navigator with a saved view point. Cheaper substitute that fails: a clip warning that writes colored pixels into the composite, which the tile-hash assertion catches.

**Freeze check:** View points are written as a registered §1 document part through the atomic writer; a document with none saves byte-identical to the pre-change writer (`ViewPointSerializationTests.NoViewPointsUnchanged`), and display filters and view modes never reach the saved file. Fixture source: `tests/fixtures/imago/views/` (created by this section).

## 11. Info, histogram, sample points, and scopes

Nothing in Imago computes a histogram or reads a pixel's value today. This section adds one pixel sampler that converts through `D01 T04` into every color model, GIMP-style sample points persisted in the §1 block, the Info and Pointer panels, status-strip readouts and title and status formats, a memory readout, the Histogram panel over `D01 T03 §4`'s `Histogram`, and a Scope panel with waveforms, parade, vectorscope, and power spectral density. The 2D FFT the spectral density needs goes into `Photon.Core` because `D01 T06 §4`'s deconvolution reuses it. It must not add a second histogram computation. It serves the acceptance-bar aim "Imago covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog". Catalog: IP-0108 to IP-0125 (18 features).

**Fidelity:** docs/captures/imago/main-window/ for the status strip; new captures to docs/captures/imago/info-panel/, docs/captures/imago/histogram/, and docs/captures/imago/scopes/.
**Job:** a user can read exact color values at any point in any model, watch tonal distribution and clipping while editing, and judge color with video-style scopes. Consumer: the user reading the panels, and the save, which persists sample points.
**Treatment:** dockable Info, Histogram, Scope, and Pointer panels in an Analysis group, sample points dragged from the rulers, a status-strip readout menu. Cheaper substitute that fails the checkpoint: an Info panel that shows only 8-bit RGB of the active layer.
**Chrome:** consume `D01 T03 §4`'s `Histogram`, `D03 T05 §2`'s histogram control, `D01 T04 §1` conversions, `D03 T03 §1`'s status strip, and AvalonDock. Do not add a second histogram computation.

**Requires:** display-session -- live panels, sample-point drags, and scope captures need an interactive desktop

- [ ] Add `PixelSampler` in `src/Imago/Photon.Imago.Core/Analysis/PixelSampler.cs` sampling the composite or the active layer at a point with sample size from point to 101 by 101 average, shared with `D03 T03 §8`'s eyedropper. Done when: `PixelSamplerTests.Average` asserts the 3 by 3 mean on a known pattern.
- [ ] Convert samples through `D01 T04` to RGB, HSB, HSV, LCh, Lab, xyY, CMYK (working CMYK profile), grayscale, web hex, total ink, and opacity; proof color joins when `D03 T18 §5` is active and is otherwise labeled "no proof". Done when: `PixelSamplerTests.Lab` asserts Lab of sRGB 255, 0, 0 equals the lcms2 value within 0.1 delta E. Cheaper substitute: hand-written sRGB formulas.
- [ ] Add `SamplePoint` in `src/Imago/Photon.Imago.Core/Analysis/SamplePoint.cs` (IP-0108, IP-0115): position, label, and readout mode (pixel, RGB percent or 0 to 255, gray, HSV, LCh, Lab, xyY, CMYK, total ink), persisted as `<imago:sample-points>`; the Color Sampler tool that places the same objects is `D03 T11 §9`'s and PSD and XCF mapping is `D03 T17`'s. Done when: `SamplePointSerializationTests` round-trip four points.
- [ ] Place sample points GIMP-style by Ctrl-dragging from a ruler, and move and delete them with the Move tool (IP-0111). Done when: a driven drag creates a point and a drag back onto the ruler deletes it.
- [ ] Add the Info panel `src/Imago/Photon.Imago.Desktop/Views/Panels/InfoPanel.xaml` (IP-0109, IP-0111): two configurable readouts, pointer position in units, selection width and height, and a sample-point list. Done when: switching a readout to Lab shows Lab values in a capture.
- [ ] Add the Info panel's status toggles and panel options (document sizes, profile, dimensions, measurement scale, scratch sizes, efficiency, timing, current tool). Done when: each toggle adds its line (settings readback quoted).
- [ ] Add the Pointer dialog (IP-0114): pointer position in pixels and units, selection bounding box, two channel readouts, and Sample Merged. Done when: Sample Merged switches the readout from the layer to the composite.
- [ ] Extend `D03 T03 §1`'s status strip (IP-0113) with a readout menu: document sizes as flattened and layered estimates, profile, dimensions, scratch sizes from the tile cache, efficiency as the share of tile reads served without spill, timing of the last operation, and current tool. Done when: each choice shows in a capture.
- [ ] Add GIMP-style format strings `Imago.View.TitleFormat` and `Imago.View.StatusFormat` (IP-0124) with `%f` file, `%D` dirty, `%t` type, `%L` layer count, `%w`, `%h`, `%z` zoom, and `%p` profile. Done when: `TitleFormatTests` expand every token.
- [ ] Add the memory readout (IP-0112): efficiency and pressure from `TileCache` hit and spill counters plus `GC.GetGCMemoryInfo()`, colored when spilling. Done when: forcing a spill colors the readout in a driven run.
- [ ] Add the Histogram panel `src/Imago/Photon.Imago.Desktop/Views/Panels/HistogramPanel.xaml` hosting `D03 T05 §2`'s control (IP-0110, IP-0116): channels RGB, R, G, B, luminosity, colors, and alpha, in compact, expanded, and all-channels views. Done when: each view renders in a capture.
- [ ] Add histogram sources (IP-0117): entire image, selected layer, and adjustment composite, with restriction to the selection and to a dragged range. Done when: restricting to a selection changes the pixel count to the selection's.
- [ ] Add histogram statistics (IP-0118): mean, standard deviation, median, pixels, level, count, percentile, and cache level, plus 32-bit minimum and maximum, and clipping counts at 0 and maximum. Done when: `HistogramStatisticsTests` assert each on synthetic ramps.
- [ ] Add unique colors through §1's `UniqueColorCounter` restricted to the selection, linear or logarithmic scale, linear or perceptual TRC, and uncached refresh (IP-0119). Done when: a 4,096-color ramp reports 4,096 unique colors.
- [ ] Compute the histogram on a worker through `D01 T03 §4`'s `Histogram`, cancellable and cached per tile version. Done when: `grep -rn "class Histogram" src/Imago` finds no second computation and a 24-megapixel 16-bit histogram completes under 150 ms (quoted).
- [ ] Add `Fft2D` in `src/Photon.Core/Imaging/Fourier/Fft2D.cs` (radix-2 with Bluestein for other sizes) so `D01 T06 §4`'s deconvolution reuses it. Done when: `Fft2DTests` match a numpy 2.x golden for a 64 by 64 fixture within 1e-9 and a 60 by 60 input takes the Bluestein path.
- [ ] Add the Scope panel `src/Imago/Photon.Imago.Desktop/Views/Panels/ScopePanel.xaml` (IP-0120, IP-0121) with gain control, intensity waveform, RGB waveform, and RGB parade (per-column histograms accumulated into a 256-row image). Done when: a horizontal gradient draws a diagonal waveform in a capture.
- [ ] Add the vectorscope (IP-0122): BT.709 Cb and Cr with 75 percent targets and a skin-tone line at 123 degrees. Done when: `ScopeTests` land pure red on the vectorscope red target.
- [ ] Add power spectral density (IP-0123): log magnitude of the centered 2D FFT of luminance on a 512 by 512 downsample through `Fft2D`. Done when: a vertical-stripe fixture shows a horizontal peak pair.
- [ ] Register Histogram, Info, Scope, and Pointer in AvalonDock and the Window menu in an Analysis group that also docks §5's Measurement Log (IP-0125). Done when: the group opens docked in a capture.
- [ ] Throttle panels to 10 updates per second while painting with zero allocations per update after warm-up. Done when: an allocation measurement over 100 updates reports zero after warm-up (quoted).
- [ ] Add Info, Pointer, Histogram, Scopes, and Sample Points pages to `docs/user/imago/`. Done when: every panel and readout above is covered.
- [ ] Commit: `"imago: info, sample points, histogram, and scopes"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~PixelSamplerTests|FullyQualifiedName~SamplePointSerializationTests|FullyQualifiedName~HistogramStatisticsTests|FullyQualifiedName~ScopeTests|FullyQualifiedName~Fft2DTests|FullyQualifiedName~TitleFormatTests"` exits 0, and a driven run drags two sample points from the rulers, switches one to Lab, and captures the Histogram and Scope panels on a fixture photo. Cheaper substitute that fails: readouts converted with hand-written sRGB formulas, which the lcms2 Lab comparison catches.

**Freeze check:** Sample points are written as a registered §1 document part through the atomic writer; a document with none saves byte-identical to the pre-change writer (`SamplePointSerializationTests.NoPointsUnchanged`). Fixture source: `tests/fixtures/imago/sample-points/` (created by this section).

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with this file's test classes reporting (`NativeLiveRoundTripTests`, `DocumentFactoryTests`, `ViewTransformTests`, `GuideSerializationTests`, `RegionMetricsTests`, `SavedHistoryRoundTripTests`, `ResamplerExtensionTests`, `ClipboardFormatTests`, `PerspectiveCropTests`, `ClipWarningDisplayFilterTests`, `Fft2DTests`)
- [ ] Every fixture under `tests/fixtures/imago/native-live/`, renamed `.ora`, opens in GIMP 3.2.6 and Krita 5.2 with every layer visible and matches Imago's composite within 1/255 (versions quoted)
- [ ] Every fixture under `tests/fixtures/imago/native-live/`, `guides/`, `history/`, `analysis/`, `views/`, and `sample-points/` round-trips through open, save, and reopen with parts equal
- [ ] `python scripts/todo-graph.py query parity --catalog imago --phase 16` reports every catalog row planned to this file stamped
- [ ] `python scripts/todo-graph.py validate` clean
