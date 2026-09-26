---
schema_version: 1
id: imago-parity-selection
domain: 03-imago
status: draft
title: "TODO-10 -- Imago Parity: Selection, Refine, Channels, and Quick Mask"
depends_on: []
track: I10
---

# TODO-10 -- Imago Parity: Selection, Refine, Channels, and Quick Mask

> **Goal:** Imago selects like Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6: a tiled soft selection with floating selections, selections saved to channels and files, and a selection editor; marquee, lasso, and magnetic lasso extensions; the magic wand, select by color, and Color Range with tonal, skin, gamut, and alpha ranges; one local segmentation engine (GrabCut, guided-filter, closed-form, and global matting) behind quick selection, paint select, foreground select, intelligent scissors, and Focus Area; one Select and Mask workspace for every refine path; modify, transform, and float commands; the complete Select menu; and a Channels panel with alpha and spot channels and quick mask options. The code lives in `src/Imago/Photon.Imago.Core/Selection/` (the segmentation engine in `Selection/Segmentation/`, which stays in Imago until Lumen's local masks, backlog B-028, need subject masks) and `src/Imago/Photon.Imago.Desktop/Selection/`; it consumes the `D01 T03` resampler and histogram, the `D01 T04 §2` gamut masks, and the `D03 T09 §3` layer masks, and never re-implements them. Every selection change is one undoable command, every selection and channel persists through the `D03 T08 §1` contract, and nothing here talks to a network: AI selection (`D03 T19 §6`) only seeds this engine. This file promotes backlog B-027 (`legacy-imago-4.2-smart-selection`) into §3.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Imago's selection is one flat, untiled 8-bit array the size of the document (`private byte[]? _mask;` in `src/Imago/src/Imago.Core/Selections/Selection.cs`, 360 lines), so Select All on a large image allocates the whole canvas. `SelectionOperation` already has a GIMP-style `Difference` mode beside Replace, Add, Subtract, and Intersect. `src/Imago/src/Imago.Core/Selections/SelectionTools.cs` offers five static selectors (rectangle, ellipse, polygon, a tolerance magic wand with a `contiguous` flag, and an RGBA range), none of them a tool. `src/Imago/src/Imago.Core/Selections/QuickMask.cs` (121 lines) has enter, exit, and cancel but no options and no surface. There is no channel model anywhere in `Imago.Core`, and `src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs` binds no Select menu command. `D03 T03 §5` (Imago 0.1.0) adds the marquee, lasso, combine modes, feather, and marching ants this file extends; its catalog rows IP-0541 to IP-0545 are `shipped-scope` there. These paths are today's names; `D03 T01 §1` renames them to `Photon.Imago.*`, and every checklist item below names the renamed paths.
<!-- claim: count "private byte\[\]\? _mask;" src/Imago/src/Imago.Core/Selections/Selection.cs = 1 -->
<!-- claim: lines src/Imago/src/Imago.Core/Selections/Selection.cs = 360 -->
<!-- claim: count "^    Difference$" src/Imago/src/Imago.Core/Selections/Selection.cs = 1 -->
<!-- claim: count "public static void Select\w+\(" src/Imago/src/Imago.Core/Selections/SelectionTools.cs = 5 -->
<!-- claim: count "bool contiguous = true" src/Imago/src/Imago.Core/Selections/SelectionTools.cs = 1 -->
<!-- claim: lines src/Imago/src/Imago.Core/Selections/QuickMask.cs = 121 -->
<!-- claim: count "public void (Enter|Exit|Cancel)|public Selection\? (Exit|Cancel)" src/Imago/src/Imago.Core/Selections/QuickMask.cs = 3 -->
<!-- claim: count "class \w*Channel" src/Imago/src/Imago.Core/**/*.cs = 0 -->
<!-- claim: count "Select" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 0 -->

## Inputs

- [`standards/imago.md`](../../standards/imago.md) -- 256 px tiles, zero allocations per dab and per frame, SIMD with a scalar reference, every edit undoable
- [`standards/shared.md`](../../standards/shared.md) -- settings keys, Serilog lines, refusal messages, and the theme every surface here consumes
- [`docs/parity/imago-parity.md`](../../docs/parity/imago-parity.md) -- the catalog rows IP-0448 to IP-0564 this file owns (per-section ranges in each context paragraph); IP-0503 and IP-0521 belong to `D03 T09 §14` and IP-0541 to IP-0545 to `D03 T03 §5`
- [`docs/parity/imago-section-design.md`](../../docs/parity/imago-section-design.md) -- "The native format stays the OpenRaster layout" and "What goes to Photon.Core and Photon.UI" (the segmentation engine stays in Imago)
- [`../backlog.md`](../backlog.md) -- B-027, promoted into §3 (its quick selection lands in §5 and its Color Range in §4)
- Rother, Kolmogorov, and Blake, "GrabCut" (SIGGRAPH 2004); Boykov and Kolmogorov, "An Experimental Comparison of Min-Cut/Max-Flow Algorithms" (TPAMI 2004) -- §6's segmentation and graph cut
- He, Sun, and Tang, "Guided Image Filtering" (TPAMI 2013); Levin, Lischinski, and Weiss, "A Closed-Form Solution to Natural Image Matting" (TPAMI 2008); He et al., "A Global Sampling Method for Alpha Matting" (CVPR 2011); Germer et al., "Fast Multi-Level Foreground Estimation" (ICPR 2020) -- §6's matting and §7's refinement
- Mortensen and Barrett, "Intelligent Scissors for Image Composition" (SIGGRAPH 1995) -- §2's live wire and §5's scissors
- Felzenszwalb and Huttenlocher, "Distance Transforms of Sampled Functions" (Theory of Computing 2012) -- the transform §8 consumes from `Photon.Core`
- Pertuz et al., "Analysis of focus measure operators for shape-from-focus" (Pattern Recognition 2013) -- §6's Focus Area measure
- Hsu, Abdel-Mottaleb, and Jain, "Face Detection in Color Images" (TPAMI 2002) -- §4's skin-tone model
- GIMP 3.2.6 and its GEGL (`gegl:matting-levin`, `gegl:matting-global`, `gegl:paint-select`, fuzzy select, select by color, Grow, Shrink, Border, and `sel2path`) -- reference implementations and `gimp-console` goldens for §3, §6, §8, and §9
- -> XREF: D03 T03 §5 -- the marquee, lasso, combine modes, feather, and marching ants §1 and §2 extend
- -> XREF: D03 T08 §1 -- the document model and the `imago:` contract every selection and channel element registers with
- -> XREF: D03 T08 §4 -- the snapping service §1's selection edges snap through
- -> XREF: D03 T09 §1 -- the Layers panel search §9's Find Layers focuses
- -> XREF: D03 T09 §3 -- the layer masks §7 refines and outputs to and §4 writes Color Range into
- -> XREF: D03 T09 §14 -- the Layer, Matting operations and `ColorDecontaminator` §7 consumes, and the `Photon.Core` distance transform §8 consumes
- -> XREF: D03 T05 §1 -- the filter pipeline §10 runs on alpha channels and the dialog frame the dialogs here use
- -> XREF: D01 T03 §2 -- the resampler §1 and §8 transform masks with
- -> XREF: D01 T03 §4 -- the histogram percentiles §4's tonal ranges read
- -> XREF: D01 T04 §2 -- the `GamutMask` behind §4's Out of Gamut
- -> XREF: D03 T11 §8 -- extends §10's split and merge engine into decompose, compose, Apply Image, and Calculations
- -> XREF: D03 T11 §10 -- the colormap dialog that calls §3's select-by-index
- -> XREF: D03 T12 §8 -- Stroke Selection, which §1's selection editor invokes
- -> XREF: D03 T14 §1 -- live filters on alpha channels, the non-destructive half of IP-0558
- -> XREF: D03 T16 §5 -- implements §9's selection-to-path bridge
- -> XREF: D03 T13 §3 -- the content-aware engine that reads §1's selection model
- -> XREF: D03 T19 §6 -- AI selection that seeds §6's engine and serves §7's Object Aware mode
- -> XREF: D03 T17 §2 -- PSD write of alpha and spot channels (56-channel limit)
- -> XREF: D03 T17 §3 -- PSD read of alpha and spot channels
- -> XREF: D03 T17 §4 -- the XCF selection channel mapped onto §1's persisted selection
- -> XREF: D03 T18 §1 -- Imago parity export, color management, and print cites §10: spot channels for separations

## Outcome

- The selection is a tiled soft mask: Select All on a 20,000 by 20,000 document allocates under 1 MB, every combine mode (Replace, Add, Subtract, Intersect, Difference) is byte-equal to the old flat implementation, and floating selections anchor or become layers.
- Selections save to channels and to annotated PNG files, load back with every combine mode, and the active selection survives save and reopen of an `.imago` file.
- The marquee family, the mixed lasso, the magnetic lasso, the magic wand, select by color, Color Range, quick selection, paint select, foreground select, intelligent scissors, and Focus Area all produce masks proven against GIMP 3.2.6 goldens or committed expected masks.
- One Select and Mask workspace refines any selection or layer mask with matting and decontaminated colors and outputs to every target the three competitors offer.
- The Select menu holds every selection command in one organized, data-driven layout, including Reselect and the selection-to-path bridge.
- A Channels panel lists color, alpha, and spot channels, splits and merges channels, and drives quick mask with options; channels round-trip through `.imago`.

**Adjacency:** list=applicable @ D03 T10 §10; document=not-applicable (selections print nothing; spot channels reach print through D03 T18 §6); settings=applicable @ D03 T10 §1; reporting=applicable @ D03 T10 §4; notifications=applicable @ D03 T10 §6; permissions=applicable @ D03 T10 §10; audit=applicable @ D03 T10 §1; exchange=applicable @ D03 T10 §1; reverse=applicable @ D03 T10 §9

**Adjacency rationale:** The Channels panel rows, the saved selection and Select and Mask preset lists, and the Color Range presets are the browsable lists. Every tool option and dialog default is an `Imago.Selection.*`, `Imago.SelectAndMask.*`, or `Imago.Channels.*` key with a named consumer. Color Range and Focus Area previews, the selection editor thumbnail, and the selection bounds shown in the `D03 T08 §11` Info panel are the reporting. Segmentation, matting, and refine output over one second report progress and cancel. A size-mismatched selection file, the 56-channel limit, a non-grayscale selection PNG, and a locked channel are refused by name. Every selection and channel command writes one Serilog Information line and one undo step. Selection files are annotated grayscale PNG, Color Range and Select and Mask presets are JSON, and channels travel through the `imago:` contract and PSD. Every selection, channel, and quick mask change is one undo step, and Reselect restores the last selection.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
| 1 | §1 | The selection model: soft selections, saved selections, and the selection editor | D03 T08 §1 | [ ] |
| 2 | §2 | Marquee and lasso extensions | §1 | [ ] |
| 3 | §3 | Magic wand and select by color | §1 | [ ] |
| 4 | §4 | Color Range and tonal selection | §3 | [ ] |
| 5 | §6 | The local segmentation engine and Focus Area | §1 | [ ] |
| 6 | §5 | Quick selection, selection brush, foreground select, and intelligent scissors | §6 | [ ] |
| 7 | §7 | Select and Mask and refine selection | §6, D03 T09 §3, D03 T09 §14 | [ ] |
| 8 | §8 | Modify and transform selection | §1, D03 T09 §14 | [ ] |
| 9 | §9 | Select menu extensions | §8 | [ ] |
| 10 | §10 | The Channels panel, spot channels, and quick mask options | §1 | [ ] |

---

## 1. The Selection Model: Soft Selections, Saved Selections, and the Selection Editor

Every later section in this file writes into a selection, so the selection must first stop being one full-canvas byte array. This section replaces it with a tiled soft mask that keeps every combine mode, adds floating selections, the channel store that Save Selection writes into before the Channels panel exists, Save and Load Selection against channels and files, a GIMP-style selection editor, marching ants options, and pixel alignment with snapping, and persists the active selection in `.imago`. It must not change what an existing combine produces. Catalog: IP-0448 to IP-0456 (9 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/selection-model/ (Save Selection, Load Selection, selection editor, marching ants at 100 and 400 percent).
**Job:** a user can keep, reload, and inspect selections without losing them to the next click. Consumer: every paint, fill, filter, and transform command that reads the active selection, and §10's Channels panel.
**Treatment:** modal Save Selection and Load Selection dialogs with document, channel, name, invert, and operation; a dockable Selection Editor showing the mask with All, None, Invert, Save to Channel, To Path, and Stroke buttons; marching ants that can hide and pause. Cheaper substitute that fails the checkpoint: a single "last selection" slot.
**Chrome:** consume the `D03 T05 §1` dialog frame, the suite history, the overlay layer of `D03 T02 §2`, and the theme; do not add a second mask type beside `SelectionMask`.

**Requires:** display-session -- the dialogs, the editor, and the marching ants captures need an interactive desktop

- [ ] Add `src/Imago/Photon.Imago.Core/Selection/SelectionMask.cs`: 8-bit coverage in 256 px tiles where empty tiles are null and full tiles share one read-only instance, with `Combine(SelectionMask, SelectionOperation)` for Replace, Add, Subtract, Intersect, and Difference. Done when: `SelectionMaskTests` compare every combine mode byte-equal against the old flat `Selection` on 50 seeded random shapes.
- [ ] Repoint `Selection` and every caller (`SelectionTools`, `QuickMask`, the `D03 T03 §5` tools, the filter pipeline) at `SelectionMask` and delete the flat `byte[]`. Done when: `grep -rn "byte\[\]? _mask" src/Imago` prints nothing and the `D03 T03 §5` selection tests pass unchanged. Cheaper substitute: keeping the flat array behind an adapter, which the allocation assertion below catches.
- [ ] Set the budget in `SelectionMaskBenchmarks`: Select All on a 20,000 by 20,000 document allocates under 1 MB and combining two full-canvas masks runs under 50 ms. Done when: `SelectionMaskTests.SelectAllAllocatesUnderOneMegabyte` passes and the benchmark time is quoted in the section's evidence.
- [ ] Add `FloatingSelection` in `Photon.Imago.Core/Selection/FloatingSelection.cs`: a tile set with an offset attached to its target drawable, shown as a temporary "Floating Selection" row in the Layers panel (IP-0449). Done when: `FloatingSelectionTests` create a float over a layer and the layer list reports the temporary row.
- [ ] Add `AnchorFloatingSelectionCommand` (merging through the `D03 T03 §2` tile snapshot) and `FloatingSelectionToLayerCommand`; while a float exists every other edit refuses with "Anchor or convert the floating selection first", as GIMP does. Done when: `FloatingSelectionTests` assert the refusal text, the anchored pixels, and one undo step each.
- [ ] Add `DocumentChannels` in `Photon.Imago.Core/Selection/Channels/`: the ordered list of `AlphaChannel { Id, Name, SelectionMask Mask, Color, Opacity, ChannelKind (Alpha, Spot), ShowsSelected }` that §10 presents. Done when: `DocumentChannelsTests` add, remove, and reorder channels and each change is one undo step.
- [ ] Add `SaveSelectionCommand` and `SaveSelectionDialog.xaml` in `Photon.Imago.Desktop/Selection/`: document, channel (New or an existing channel), name, and operation Replace, Add, Subtract, Intersect (IP-0450). Done when: `SaveLoadSelectionTests` save into a new and an existing channel with each operation and read the channel mask back. Cheaper substitute: overwriting one hidden slot.
- [ ] Add `LoadSelectionCommand` and `LoadSelectionDialog.xaml`: source document of equal pixel size, channel (alpha channels, layer transparency, layer masks), Invert, and operation (IP-0451). Done when: `SaveLoadSelectionTests` load from each source kind, a document of another size is not listed, and the undo name is "Load Selection".
- [ ] Add `SelectionFileWriter` and `SelectionFileReader` in `Photon.Imago.Core/Selection/Files/`, so Save Selection to File exports and Load Selection from File imports an 8-bit grayscale PNG with an `iTXt` chunk keyed `imago:selection` holding `{ "v": 1, "width", "height", "x", "y" }`, written through the atomic writer (IP-0452). Done when: `SelectionFileTests` round-trip a feathered mask byte-equal.
- [ ] Load a selection file of another size by offering Scale (the `D01 T03 §2` bicubic resampler) or Place at Offset, and refuse a non-grayscale PNG by name. Done when: `SelectionFileTests` assert both size paths and the refusal text naming the file.
- [ ] Persist the active selection as `<imago:selection v="1" src="data/selection.png"/>` in the `D03 T08 §1` document metadata (not a stack layer, so GIMP and Krita opening the file as `.ora` ignore it), and each alpha channel as an `<imago:channel>` element. Done when: `SelectionPersistenceTests` save and reopen a document with a feathered selection and two channels, tile by tile byte-equal.
- [ ] Add `SelectionEditorPanel.xaml` and `SelectionEditorViewModel` (GIMP): live mask thumbnail, click-to-select-by-color in the preview through §3's engine, and buttons All, None, Invert, Save to Channel, To Path, and Stroke Selection (IP-0455). Done when: a driven run clicks each enabled button and the capture is committed.
- [ ] Disable the editor's To Path button with the tooltip "Planned: D03 T16 §5" and Stroke with "Planned: D03 T12 §8" until those sections register their implementations. Done when: `SelectionEditorViewModelTests` assert both tooltips while no implementation is registered.
- [ ] Add marching ants settings `Imago.Selection.ShowEdges` (View, Show, Selection Edges, Ctrl+H) and `Imago.Selection.PauseAntsWhileMoving` read by `SelectionOverlayRenderer` in `Photon.Imago.Rendering` (IP-0448, IP-0453). Done when: `SelectionOverlayTests` read both keys and the hidden state draws no contour.
- [ ] Add `Imago.Selection.AntsSpeed` (GIMP marching ants speed in ms per step, default 200) and a cached 50 percent marching-squares contour rebuilt only on mask change (IP-0456). Done when: `SelectionOverlayTests` assert the contour is rebuilt once per mask change and not per frame.
- [ ] Add `Imago.Selection.ForcePixelAlignment` (default true, Affinity) rounding marquee and transform edges to whole pixels, and `Imago.Snap.SelectionEdges` snapping selection edges to guides and grids through the `D03 T08 §4` snapping service (IP-0454). Done when: `SelectionAlignmentTests` draw a marquee at fractional coordinates and assert whole-pixel and snapped edges.
- [ ] Record undo names "Save Selection", "Load Selection", "Anchor Floating Selection", and "Floating Selection to Layer" in the suite history, and log one Information line per command as `Selection {Command} {Operation} {Source}`. Done when: a driven save and load quotes both log lines.
- [ ] Commit the fixture `tests/fixtures/imago/selection/soft-selection.imago` (a feathered ellipse plus two alpha channels) with a README naming what it covers. Done when: the fixture README lists the file and its features.
- [ ] Update `docs/user/imago/selection.md` with saved selections, selection files, floating selections, the selection editor, and the marching ants options. Done when: every control of this section is documented.
- [ ] Commit: `"imago: tiled soft selections, saved selections, floating selections, and the selection editor"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~SelectionMaskTests|FullyQualifiedName~SaveLoadSelectionTests|FullyQualifiedName~SelectionFileTests|FullyQualifiedName~FloatingSelectionTests|FullyQualifiedName~SelectionPersistenceTests"` exits 0, and `tests/fixtures/imago/selection/soft-selection.imago` is opened, saved, reopened, and compared tile by tile byte-equal. Cheaper substitute that fails: keeping the full-size `byte[]`, which the 1 MB allocation assertion on a 20,000 px canvas catches.

## 2. Marquee and Lasso Extensions

The 0.1.0 marquee and lasso (`D03 T03 §5`) draw basic shapes; the three competitors add fixed styles, numeric fields, single-pixel rows, rounded corners, GIMP's auto shrink and composition guides, and an edge-following magnetic lasso. This section adds the shared selection tool options every selection tool reads, a live-wire engine that §5's intelligent scissors reuse, and the mixed lasso gestures. It must not add a second polygon rasterizer. Catalog: IP-0457 to IP-0467 (11 features).

**Fidelity:** Imago options bar -- docs/captures/imago/main-window/; new captures to docs/captures/imago/marquee-lasso/ (marquee styles, composition guides, magnetic lasso anchors).
**Job:** a user can draw a precise geometric or edge-following selection in one gesture. Consumer: the active `SelectionMask`.
**Treatment:** marquee options (style Normal, Fixed Ratio, Fixed Size, swap, X, Y, W, H fields, corner radius, auto shrink, guides) and a magnetic lasso that snaps a live path to edges with anchor points. Cheaper substitute that fails the checkpoint: a magnetic lasso that is a plain polygon lasso.
**Chrome:** consume the `D03 T03 §4` tool system and options bar, §1's `SelectionMask`, and the overlay; do not add a second polygon rasterizer beside `SelectionTools.SelectPolygon`.

**Requires:** display-session -- drawing marquees and a magnetic lasso on the canvas needs an interactive desktop

- [ ] Add `SelectionToolOptions` in `Photon.Imago.Core/Selection/Tools/`: Antialias, Feather at creation (radius applied through the existing Gaussian feather before combine), and the combine mode, persisted as `Imago.Selection.Antialias` and `Imago.Selection.FeatherRadius` (IP-0457). Done when: `SelectionToolOptionsTests` assert the feathered edge profile and that both keys survive a restart.
- [ ] Bind every selection tool of this file to the one `SelectionToolOptions` instance on the options bar. Done when: `grep -rn "FeatherRadius" src/Imago/Photon.Imago.Desktop` shows only the shared options view. Cheaper substitute: per-tool copies of antialias and feather.
- [ ] Move the outline without pixels: drag inside with a selection tool moves only the mask, arrow keys nudge 1 px and Shift+arrow 10 px, Space while dragging repositions the marquee being drawn, and Ctrl+Alt drag (GIMP) moves the contents as a §1 float (IP-0458). Done when: `MoveSelectionOutlineTests` assert each gesture and one "Move Selection" step per gesture.
- [ ] Add Single Row and Single Column marquees (Photoshop) plus Affinity's set width or height field (IP-0459). Done when: `MarqueeStyleTests` assert a 1 px row across the canvas and a set-height row of 5 px.
- [ ] Add marquee style Normal, Fixed Ratio, and Fixed Size with a swap button (IP-0460), and GIMP's numeric position and size fields editable while the marquee is live (IP-0461). Done when: `MarqueeStyleTests` drag with each style and edit W while live, asserting the resulting bounds.
- [ ] Add rounded rectangle selection: GIMP's Rounded Corners option and Select, Rounded Rectangle (radius percent, concave) as a signed-distance mask so corners antialias exactly (IP-0464). Done when: `RoundedRectangleMaskTests` compare corner coverage against an analytic disc within 1/255.
- [ ] Add GIMP's highlight (dim outside while drawing) and composition guides while drawing (thirds, golden sections, diagonal lines) on the overlay (IP-0462). Done when: a driven marquee with each guide is captured.
- [ ] Add Auto Shrink and Shrink Merged (shrink the marquee to the bounding box of the non-transparent region under it) (IP-0463). Done when: `AutoShrinkTests` shrink over a centered opaque square and assert its bounds, with and without Shrink Merged.
- [ ] Add `LiveWire` in `Photon.Imago.Core/Selection/LiveWire/`: Dijkstra over a cost from gradient magnitude, Laplacian zero crossings, and gradient direction (Mortensen and Barrett 1995), computed lazily per 256 px tile with pooled buffers. Done when: `LiveWireTests` keep the path on a synthetic step edge within 1 px of it.
- [ ] Add `MagneticLassoTool` (Photoshop, Affinity): Width (search radius), Contrast (edge threshold), Frequency (auto anchor rate), click to add manual points, Backspace removes the last point (IP-0465). Done when: a driven magnetic lasso around `tests/fixtures/imago/selection/disc-on-noise.png` reaches IoU above 0.97 against the disc. Cheaper substitute: a polygon lasso that ignores edges.
- [ ] Add pen pressure changing width when `Imago.Selection.MagneticPenWidth` is on and `[` and `]` changing width by 1 px (IP-0466); budget: a path update under 16 ms on a 24-megapixel image. Done when: `MagneticLassoTests` assert the width changes and the budget test quotes its time.
- [ ] Add the mixed lasso (all three apps): Alt switches freehand and polygonal mid-gesture, Backspace or Delete removes the last polygon point, Enter or double-click closes, and the view auto-pans at the window edge (IP-0467). Done when: `MixedLassoTests` replay a recorded gesture with a switch and a removed point and assert the polygon.
- [ ] Record undo names per tool ("Rectangular Marquee", "Magnetic Lasso", and so on) through the existing tool command, and log one Information line per committed selection as `Selection {Tool} {Operation} {Bounds}`. Done when: the driven magnetic lasso run quotes its log line.
- [ ] Commit the fixture `tests/fixtures/imago/selection/disc-on-noise.png` with its expected mask. Done when: the fixture README names both files.
- [ ] Update `docs/user/imago/selection.md` with marquee styles, rounded rectangles, auto shrink, and the magnetic and mixed lasso. Done when: every option is documented.
- [ ] Commit: `"imago: marquee styles, rounded rectangles, and the magnetic lasso"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~LiveWireTests|FullyQualifiedName~RoundedRectangleMaskTests|FullyQualifiedName~MarqueeStyleTests|FullyQualifiedName~AutoShrinkTests|FullyQualifiedName~MixedLassoTests"` exits 0, and a driven magnetic lasso around `tests/fixtures/imago/selection/disc-on-noise.png` produces a mask within 2 px of the disc with IoU above 0.97 quoted. Cheaper substitute that fails: a polygon lasso that ignores edges, which the IoU assertion catches.

## 3. Magic Wand and Select by Color

The magic wand is the second selection tool most tutorials reach for, and GIMP splits it into fuzzy select and select by color with criteria the other two lack. This section builds one flood-select engine behind the Magic Wand, GIMP's fuzzy select and select by color, and Affinity's flood select, with the sample averager and sample source that painting, retouch, and color tools reuse. `SelectionTools.SelectByColor` becomes a thin call into it. It promotes backlog B-027; B-027's quick selection lands in §5 and its Color Range in §4. Catalog: IP-0468 to IP-0478 (11 features). -> SOURCE: legacy-imago-4.2-smart-selection

**Fidelity:** Imago options bar -- docs/captures/imago/main-window/; new captures to docs/captures/imago/magic-wand/ (drag-to-tolerance label, draw mask preview).
**Job:** a user can select a region or every pixel of a color in one click, and tune the tolerance by dragging. Consumer: the active `SelectionMask`, and `D03 T11 §10`'s colormap dialog through select-by-index.
**Treatment:** a Magic Wand tool (W) and a Select by Color tool (Shift+O) sharing one options set; dragging after the click changes tolerance live with the mask previewed. Cheaper substitute that fails the checkpoint: an RGB-distance flood fill on the active layer only.
**Chrome:** consume §1's mask and §2's `SelectionToolOptions`; do not keep `SelectionTools.SelectByColor` as a second implementation.

**Requires:** display-session -- clicking and dragging the wand on the canvas needs an interactive desktop

- [ ] Add `FloodSelector` in `Photon.Imago.Core/Selection/Flood/`: a scanline flood (contiguous) or a per-pixel threshold pass (global) with a pooled span stack (IP-0470, IP-0472). Done when: `FloodSelectorTests` select a bounded region contiguously and every matching pixel globally.
- [ ] Add 4- or 8-connectivity (`Diagonal neighbors`, GIMP) and an antialiased edge from the distance to the threshold (IP-0475). Done when: `FloodSelectorTests` flood a one-pixel diagonal line fixture and only 8-connectivity crosses it.
- [ ] Add Select Transparent Areas (GIMP) so a click on transparency selects the transparent region (IP-0474). Done when: `FloodSelectorTests` assert the option on and off over a transparent hole.
- [ ] Add `Criterion` Composite, Red, Green, Blue, Alpha, Hue, Saturation, Value, LCh Lightness, LCh Chroma, and LCh Hue (GIMP's criteria) and GIMP's Draw Mask preview in the quick mask color while the pointer is down (IP-0476). Done when: `FloodSelectorTests` isolate each hue sector of a synthetic HSV wheel with the Hue criterion.
- [ ] Add `SampleAverager` in `Photon.Imago.Core/Selection/Sampling/` with Point, 3 by 3, 5 by 5, 11 by 11, 31 by 31, 51 by 51, and 101 by 101 averages, the type `D03 T11 §9`'s eyedropper extends (IP-0471). Done when: `SampleAveragerTests` average a checker fixture exactly at every size.
- [ ] Add `SampleSource` (Current Layer, All Layers as the flattened composite, Current Layer and Below, and a picked layer list) as the one shared type painting and retouch tools also read (IP-0469, IP-0473). Done when: `SampleSourceTests` select from the composite and from a picked two-layer list with different results.
- [ ] Rewrite `SelectionTools.SelectByColor` and the magic wand selector as wrappers over `FloodSelector`. Done when: `grep -n "for (int y" src/Imago/Photon.Imago.Core/Selection/SelectionTools.cs` prints no flood loop and the old selector tests still pass. Cheaper substitute: keeping both code paths.
- [ ] Add `MagicWandTool` (W) with tolerance 0 to 255, antialias, contiguous, sample size, and sample source on the options bar (IP-0470). Done when: a driven click on a fixture region quotes the pixel count in the log line.
- [ ] Add drag to set tolerance (Affinity and GIMP): after pressing, horizontal drag changes tolerance with the mask previewed on the overlay and the value in a cursor label; release commits (IP-0477). Done when: `DragToleranceTests` map a 100 px drag to the expected tolerance and a capture shows the label.
- [ ] Add `SelectByColorTool` (Shift+O) and the Select, By Color command: global matching of the clicked color across the layer or merged composite with a threshold (IP-0478). Done when: `FloodSelectorTests` select every red pixel of a scattered-dot fixture.
- [ ] Add `SelectByIndex(IIndexedPixelSource, IndexPredicate, SelectionOperation)` over an interface that `D03 T11 §7`'s indexed documents implement, for the colormap dialog of `D03 T11 §10` (IP-0468). Done when: `SelectByIndexTests` select two indices of a fake indexed source with Replace, Add, Subtract, and Intersect.
- [ ] Set the budget: a global select on 24 megapixels under 150 ms, a contiguous fill of 10 megapixels under 200 ms, and zero allocations inside the scanline loop. Done when: `FloodSelectorBudgetTests` quote both times and 0 B allocated per scanline.
- [ ] Record undo names "Magic Wand" and "Select by Color" and log one Information line per selection with tool, tolerance, criterion, and pixel count. Done when: the driven wand run quotes the line.
- [ ] Commit GIMP 3.2.6 fuzzy-select and by-color goldens (threshold 15 and 60, antialias on) under `tests/fixtures/imago/selection/wand/` with `reference.txt` naming the `gimp-console` command and version. Done when: `FloodSelectorGoldenTests` compare each golden within 1/255.
- [ ] Update `docs/user/imago/selection.md` with the magic wand, select by color, criteria, sample size, and sample source. Done when: every option is documented.
- [ ] Commit: `"imago: magic wand, fuzzy select, and select by color on one flood engine"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~FloodSelectorTests|FullyQualifiedName~FloodSelectorGoldenTests|FullyQualifiedName~SampleAveragerTests|FullyQualifiedName~SelectByIndexTests"` exits 0, with the golden tests matching `gimp-console` fuzzy-select and by-color masks within 1/255 at two thresholds. Cheaper substitute that fails: RGB Euclidean distance only, which the hue-criterion golden rejects.

## 4. Color Range and Tonal Selection

Photoshop's Color Range and Affinity's sampled, tonal, and alpha selections select by color family or tonal band with a soft falloff, and both can write the result straight into a layer mask. This section adds the Color Range engine and dialog with previews and presets, the skin-tone and out-of-gamut ranges, and Affinity's select commands. Its preview reuses the renderer §6 builds when present. Catalog: IP-0479 to IP-0491 (13 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/color-range/ (dialog, each document preview mode, skin tones with faces).
**Job:** a user can select every pixel of a color family or tonal band with a soft, previewed falloff, including into a layer mask. Consumer: the active `SelectionMask` or the active `D03 T09 §3` layer mask.
**Treatment:** a modal Color Range dialog with Select list, fuzziness and range sliders, add and subtract eyedroppers, Invert, Localized Color Clusters, a thumbnail showing Selection or Image, a document preview of None, Grayscale, Black Matte, White Matte, or Quick Mask, and Save and Load. Cheaper substitute that fails the checkpoint: a hard RGB range with no preview.
**Chrome:** consume §3's `SampleAverager`, the `D03 T05 §1` dialog frame, and `D01 T04 §2`'s `GamutMask`; do not build a second preview compositor (reuse `SelectionPreviewRenderer` from §6 when it exists, otherwise §1's overlay renderer).

**Requires:** display-session -- the Color Range dialog and its previews need an interactive desktop

- [ ] Add `ColorRangeSelector` in `Photon.Imago.Core/Selection/ColorRange/`: sampled colors matched by distance in Lab with a smooth fuzziness falloff on Photoshop's 0 to 200 scale, add and subtract samples, and Invert (IP-0481). Done when: `ColorRangeSelectorTests` assert coverage falls monotonically as fuzziness decreases.
- [ ] Add Localized Color Clusters multiplying coverage by a spatial falloff from each sample point with the Range percent, exposed for `D03 T11 §4`'s Replace Color (IP-0488). Done when: `ColorRangeSelectorTests` show the mask shrinking as Range decreases.
- [ ] Add preset families Reds, Yellows, Greens, Cyans, Blues, and Magentas as feathered hue windows reusing `D01 T03 §5`'s `HueSaturationLightness` range constants (IP-0484). Done when: `ColorRangeSelectorTests` isolate each family on a hue wheel fixture and `grep` finds no second copy of the range constants.
- [ ] Add tonal ranges Highlights, Midtones, and Shadows with fuzziness and range sliders over luminance, band edges from `D01 T03 §4` `Histogram.Percentile`, and Affinity's Select Tonal Range command on the same code (IP-0485). Done when: `TonalRangeTests` select each band of a gray ramp at the expected percentiles.
- [ ] Add Skin Tones: an elliptical skin-color model in YCbCr (Hsu, Abdel-Mottaleb, and Jain 2002) with fuzziness, and Detect Faces weighting the mask toward face boxes from OpenCV's frontal-face Haar cascade through OpenCvSharp4 in `Selection/FaceBoxes.cs` (IP-0486). Done when: `SkinToneModelTests` classify committed synthetic skin and non-skin swatches correctly.
- [ ] Record the OpenCvSharp4 scope extension (from `Photon.Imago.Core/Photo/` to `Selection/FaceBoxes.cs`, Apache-2.0) as a row in `docs/dev/decisions.md`; AI face detection stays `D03 T19 §6`. Done when: the decisions row exists and names the license check.
- [ ] Add Out of Gamut through `D01 T04 §2`'s `GamutMask` against the document's CMYK proof profile (the active `D03 T18 §5` proof setup when present, otherwise `color.defaultCmykProfile`) (IP-0487). Done when: `GamutRangeTests` select sRGB 0,255,0 and not 128,128,128.
- [ ] Add `ColorRangeDialog.xaml` and `ColorRangeViewModel` with the thumbnail Selection or Image and document previews None, Grayscale, Black Matte, White Matte, and Quick Mask, redrawn at screen resolution first and refined on idle (IP-0482); budget: a slider change to an updated preview under 60 ms on 24 megapixels. Done when: a driven dialog captures each preview mode and the budget test quotes its time. Cheaper substitute: a hard RGB box range with no preview.
- [ ] Add Save and Load of settings as `.imagocolorrange` JSON (samples in Lab, fuzziness, range, mode) through the atomic writer; the Photoshop `.axt` format is not offered (IP-0483). Done when: `ColorRangePresetTests` round-trip a preset byte-equal and refuse a malformed file by name.
- [ ] Add Affinity's Select Sampled Color with color model RGB, HSL, or Lab and a tolerance (IP-0489). Done when: `ColorRangeSelectorTests` select the same fixture region in each model.
- [ ] Add Select Alpha Range (Fully Transparent, Partially Transparent, Opaque) (IP-0490). Done when: `AlphaRangeTests` select each class on a three-band alpha fixture.
- [ ] Add Selection from layer or composite luminosity (Ctrl+Shift+Alt+2 in Photoshop, luminosity as coverage) (IP-0491). Done when: `AlphaRangeTests` load a gray ramp's luminosity and coverage equals the ramp within 1/255.
- [ ] Add the mask entries: Layer Mask Properties, Color Range, and Affinity's Tonal Range for masks write the result into the active `D03 T09 §3` mask instead of the selection (IP-0479, IP-0480). Done when: `ColorRangeMaskTests` write into a layer mask and the selection stays unchanged.
- [ ] Record undo names "Color Range", "Select Tonal Range", and "Select Alpha Range", log one Information line with mode and pixel count, and show a summary that reports the selected pixel count and percent in the dialog footer. Done when: the driven Color Range run quotes the line.
- [ ] Commit `tests/fixtures/imago/selection/color-range/fruit.png` with a README. Done when: the driven run's mask hash is recorded beside it.
- [ ] Update `docs/user/imago/selection.md` with Color Range, tonal, skin, gamut, sampled color, and alpha range. Done when: every control is documented.
- [ ] Commit: `"imago: Color Range, tonal ranges, skin tones, and alpha range selection"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ColorRangeSelectorTests|FullyQualifiedName~TonalRangeTests|FullyQualifiedName~SkinToneModelTests|FullyQualifiedName~GamutRangeTests|FullyQualifiedName~AlphaRangeTests|FullyQualifiedName~ColorRangeMaskTests"` exits 0, and a driven Color Range with two add samples on `tests/fixtures/imago/selection/color-range/fruit.png` produces a mask whose hash is quoted, with its Black Matte preview captured. Cheaper substitute that fails: a hard RGB box range, which the fuzziness monotonic test catches.

## 5. Quick Selection, Selection Brush, Foreground Select, and Intelligent Scissors

Brush-driven selection is how most users select a subject today. This section adds Photoshop's Quick Selection, Affinity's Selection Brush with and without Snap to Edges, and GIMP's Paint Select, Foreground Select, and Intelligent Scissors, all driving §6's engine or §2's live wire, so there is no segmentation path outside `Selection/Segmentation/`. Catalog: IP-0495 to IP-0502 (8 features; IP-0495 and IP-0502 are the same GIMP Paint Select tool).

**Fidelity:** Imago options bar -- docs/captures/imago/main-window/; new captures to docs/captures/imago/quick-selection/ (quick selection stroke, foreground select trimap and preview, scissors boundary).
**Job:** a user can paint roughly over a subject and get a clean selection that grows stroke by stroke. Consumer: the active `SelectionMask`.
**Treatment:** a brush-driven tool family whose strokes become GrabCut seeds in an expanding region of interest, with add and subtract modes, auto-enhance, hard or soft edges, and GIMP's trimap-based foreground select with preview. Cheaper substitute that fails the checkpoint: region growing by color tolerance from the stroke.
**Chrome:** consume §6's engine and `SelectionPreviewRenderer`, §2's `LiveWire`, §3's `SampleSource`, and the `D03 T03 §6` brush cursor; do not add a segmentation path outside `Selection/Segmentation/`.

**Requires:** display-session -- painting selections on the canvas needs an interactive desktop

- [ ] Add `QuickSelectionSession` in `Photon.Imago.Core/Selection/Quick/`: each stroke adds foreground seeds (background with Alt) and §6's `GrabCut` re-solves only a region of interest dilated around the stroke, merging into the running mask (IP-0496). Done when: `QuickSelectionSessionTests` reach IoU above 0.95 with two strokes on a synthetic scene.
- [ ] Add `QuickSelectionTool` (W group, Photoshop; Affinity Selection Brush with Snap to Edges on) with size, hardness, spacing, and pen pressure from the `D03 T03 §6` brush settings, mode New, Add, Subtract, and Sample All Layers through §3's `SampleSource` (IP-0496). Done when: `QuickSelectionSessionTests` assert a subtract stroke removes a region. Cheaper substitute: color-tolerance region growing from the stroke.
- [ ] Set the budget: stroke release to updated mask under 250 ms on a 24-megapixel image, logged as elapsed milliseconds. Done when: `QuickSelectionBudgetTests` quote the time.
- [ ] Add Auto-Enhance (a guided-filter pass plus smoothing) and Affinity's Soft Edges toggle (keep the matte) against hard edges (threshold at 50 percent) (IP-0497). Done when: `QuickSelectionSessionTests` assert soft edges keep fractional coverage and hard edges hold only 0 and 255.
- [ ] Add the selection brush without snapping (Affinity Snap to Edges off, and Photoshop's plain overlay painting): paints coverage straight into the mask with the brush's hardness, shown as an overlay (IP-0498). Done when: `SelectionBrushTests` paint a stroke and assert the coverage profile equals the brush dab profile.
- [ ] Add `PaintSelectTool` (GIMP 3.2.6 Paint Select): progressive graph-cut selection from brush strokes with Mode Add or Subtract, stroke width, and a local region size, on the same region solver as Quick Selection with GIMP's parameters (IP-0495, IP-0502). Done when: `PaintSelectTests` compare one stroke against a GIMP 3.2.6 `gegl:paint-select` golden with IoU above 0.95.
- [ ] Add `ForegroundSelectTool` (GIMP): draw a rough outline as the trimap unknown band, then paint Foreground, Background, or Unknown with a stroke width and Preview Mode Color or Grayscale (IP-0499). Done when: `ForegroundSelectTests` build the trimap from an outline and paint strokes and assert its three classes.
- [ ] Add the foreground select engines Matting Levin and Matting Global with Levels and Iterations (§6's matting engines); Enter makes the matte the selection (IP-0500). Done when: `ForegroundSelectTests` run the trimap through each engine and assert the matte within 3/255 mean of §6's goldens.
- [ ] Add `IntelligentScissorsTool` (GIMP): click anchors, segments follow §2's `LiveWire`, Interactive Boundary shows the live segment while moving, Auto-edge snap nudges anchors to the strongest edge within 5 px, and Enter converts to a selection (IP-0501). Done when: `IntelligentScissorsTests` close a path on a disc fixture within 1 px.
- [ ] Record undo names "Quick Selection", "Paint Select", "Foreground Select", and "Intelligent Scissors" and log one Information line per tool with stroke count and elapsed milliseconds. Done when: the driven quick selection run quotes the line.
- [ ] Commit `tests/fixtures/imago/selection/quick/portrait-synthetic.png` with its expected mask and the GIMP paint-select golden with `reference.txt`. Done when: the fixture README names each file and the GIMP version.
- [ ] Update `docs/user/imago/selection.md` with quick selection, the selection brush, paint select, foreground select, and intelligent scissors. Done when: every option is documented.
- [ ] Commit: `"imago: quick selection, paint select, foreground select, and intelligent scissors"`

**Test checkpoint:** Driven run with evidence and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~QuickSelectionSessionTests|FullyQualifiedName~PaintSelectTests|FullyQualifiedName~ForegroundSelectTests|FullyQualifiedName~IntelligentScissorsTests"` exits 0, and a driven two-stroke quick selection on `tests/fixtures/imago/selection/quick/portrait-synthetic.png` logs its elapsed time under 250 ms with its IoU against the committed expected mask quoted above 0.95. Cheaper substitute that fails: color-tolerance region growing from the stroke, which the IoU assertion on a subject with mixed colors rejects.

## 6. The Local Segmentation Engine and Focus Area

Quick selection, foreground select, Select and Mask, Focus Area, and AI selection all need the same thing: turn rough strokes, boxes, or points into a clean matte, offline. This section builds that engine once in `Photon.Imago.Core/Selection/Segmentation/` (GrabCut on a max-flow solver, the guided filter, closed-form and global matting from a trimap, foreground estimation) with the one selection preview renderer §4 and §7 reuse, and ships Focus Area on a classical focus measure as its first surface. The engine stays in Imago until Lumen's local masks (backlog B-028) need subject masks. Catalog: IP-0492 to IP-0494 (3 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/focus-area/ (dialog, each view mode).
**Job:** a user can select the in-focus subject of a shallow depth-of-field photo, and every later selection tool can turn rough input into a clean matte offline. Consumer: the output target Focus Area names, §5's tools, §7's refine session, and `D03 T19 §6`'s AI selection.
**Treatment:** a Focus Area dialog with View (marching ants, overlay, on black, on white, black and white, on layers, reveal layer), In-Focus Range with Auto, Image Noise Level with Auto, Soften Edge, add and subtract brushes, Output To, and a Select and Mask button. Cheaper substitute that fails the checkpoint: a Sobel-threshold mask with no noise compensation.
**Chrome:** consume §1's mask, the `D03 T05 §1` dialog frame, and the overlay; the `SelectionPreviewRenderer` built here is the one §4 and §7 reuse.

**Requires:** display-session -- the Focus Area dialog and its view modes need an interactive desktop

- [ ] Add `MaxFlow` in `Selection/Segmentation/Graph/`: Boykov-Kolmogorov augmenting paths on a 4- or 8-connected grid graph with pooled node arrays; budget: a 2-megapixel region cut under 400 ms with zero managed allocations per iteration. Done when: `MaxFlowTests` equal a brute-force minimum cut on 8 by 8 graphs and the budget test quotes its time.
- [ ] Add `GrabCut` (Rother et al. 2004): 5-component full-covariance GMMs for foreground and background, iterative estimation with hard constraints, run on a downsampled region and upsampled with the guided filter. Done when: `GrabCutTests` reach IoU above 0.95 on a synthetic two-color scene.
- [ ] Add the entry `Segment(SegmentationRequest)` taking `Box`, `ForegroundStrokes`, `BackgroundStrokes`, or `Points`, the shape `D03 T19 §6` sends after an AI locate. Done when: `GrabCutTests` segment the same scene from a box and from points with IoU above 0.95 each.
- [ ] Add `GuidedFilter` (He, Sun, and Tang 2013, the fast variant with subsampling) for color-guided mask refinement with radius and epsilon. Done when: `GuidedFilterTests` equal the unsubsampled reference within 2/255 at subsample 1.
- [ ] Add `ClosedFormMatting` (Levin et al. 2008): the matting Laplacian over 3 by 3 windows solved by preconditioned conjugate gradient on a coarse-to-fine pyramid whose `Levels` and `Iterations` are GIMP's foreground select parameters. Done when: `MattingGoldenTests` compare against GIMP 3.2.6 `gegl:matting-levin` within a mean of 3/255 and a max of 24/255.
- [ ] Add `GlobalMatting` (He et al. 2011): global sampling of foreground and background pairs with randomized search and `Iterations`, the global matting from a trimap (IP-0492). Done when: `MattingGoldenTests` compare against `gegl:matting-global` within the same tolerances.
- [ ] Add `ForegroundEstimator` (Germer et al. 2020, multi-level) returning the foreground color estimate for a matte band, which §7 passes to `D03 T09 §14`'s `ColorDecontaminator`. Done when: `ForegroundEstimatorTests` recover a known foreground color on a synthetic composite within 3/255.
- [ ] Add `SelectionPreviewRenderer` in `Photon.Imago.Rendering/Selection/`: marching ants, overlay (color and opacity), on black, on white, black and white, on layers, onion skin, transparent, and reveal layer. Done when: `SelectionPreviewRendererTests` render each mode over a fixture and compare against goldens within 1/255.
- [ ] Add `FocusMeasure`: variance of the Laplacian over a window (Pertuz et al. 2013) on luminance, noise compensation from a MAD noise estimate (Image Noise Level Auto), and In-Focus Range with Auto from Otsu's method (IP-0493). Done when: `FocusMeasureTests` split a half-blurred, half-sharp fixture within 4 px of the true boundary.
- [ ] Add Soften Edge through `GuidedFilter` and the add and subtract brushes as hard constraints for a final `GrabCut` pass (IP-0493). Done when: `FocusMeasureTests` assert a subtract stroke removes its region from the result.
- [ ] Add `FocusAreaDialog.xaml` and `FocusAreaViewModel` with the View list over `SelectionPreviewRenderer`, the In-Focus Range and Image Noise Level sliders with Auto, and Soften Edge (IP-0493). Done when: a driven Focus Area on a committed shallow-focus fixture captures each view mode. Cheaper substitute: a Sobel-threshold mask with no noise compensation.
- [ ] Add Output To Selection, Layer Mask, New Layer, New Layer with Layer Mask, New Document, and New Document with Layer Mask, and the Select and Mask button that hands the result to §7 (disabled with "Planned: D03 T10 §7" until §7 registers its entry) (IP-0494). Done when: `FocusAreaOutputTests` produce each target's document object.
- [ ] Take `IProgress<double>` and `CancellationToken` at tile or iteration granularity on every engine entry point, notify the status strip progress indicator for any run over one second, and log one Information line per Focus Area apply as `Focus Area {Output} {Pixels}`. Done when: `SegmentationCancellationTests` cancel a GrabCut mid-run and the mask is unchanged.
- [ ] Commit the matting goldens under `tests/fixtures/imago/selection/matting/` with `reference.txt` naming the `gimp-console` commands and GIMP 3.2.6. Done when: the fixture README names each file.
- [ ] Update `docs/user/imago/selection.md` with Focus Area and its view modes. Done when: every control is documented.
- [ ] Commit: `"imago: the local segmentation and matting engine and Focus Area"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~MattingGoldenTests|FullyQualifiedName~MaxFlowTests|FullyQualifiedName~GrabCutTests|FullyQualifiedName~FocusMeasureTests|FullyQualifiedName~SelectionPreviewRendererTests"` exits 0, with closed-form and global matting alphas matching `gegl:matting-levin` and `gegl:matting-global` output within a mean delta of 3/255 and a max of 24/255 and GrabCut IoU quoted. Cheaper substitute that fails: a thresholded distance transform standing in for matting, which the golden rejects at hair edges.

## 7. Select and Mask and Refine Selection

Hair and fur are where selections fail, and all three competitors ship a refine workspace for them. This section builds one Select and Mask workspace (Photoshop layout, Affinity Refine Selection, and a compact legacy Refine Edge layout, all over one `RefineSession`) with view modes, refine tools, edge detection, global refinements, decontaminate colors, and every output target, reachable from every selection tool, layer masks, and Focus Area. The matting cleanup rows IP-0503 and IP-0521 (Remove Black and White Matte, Defringe) belong to `D03 T09 §14`, which this workspace calls with no second implementation. Catalog: IP-0504 to IP-0520 and IP-0522 (18 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/select-and-mask/ (workspace, Affinity layout, legacy layout, each view mode).
**Job:** a user can turn a rough selection or mask of hair or fur into a clean matte with decontaminated colors and send it where they need it. Consumer: the output target the user picks (selection, layer mask, new layer, or new document).
**Treatment:** a full-window modal workspace with its own toolbar (Quick Selection, Refine Edge brush, Brush, Object lasso, Hand, Zoom), a Properties column (View, Show Edge, Show Original, Real-time and High Quality Preview, Edge Detection, Global Refinements, Output), and presets. Cheaper substitute that fails the checkpoint: a Feather and Contract dialog labeled Refine.
**Chrome:** consume §6's engine and `SelectionPreviewRenderer`, §5's quick selection, the `D03 T09 §3` mask model, and the `D03 T09 §14` matting operations; do not build a second preview compositor or matting routine.

**Requires:** display-session -- the workspace, refine brushes, and view-mode captures need an interactive desktop

- [ ] Add `RefineSession` in `Photon.Imago.Core/Selection/Refine/`: the source mask, the refine band, brush edits, and parameters, producing the matte through §6 (`ClosedFormMatting` inside the band, `GuidedFilter` outside). Done when: `RefineSessionTests` refine a synthetic hair edge and the band's coverage becomes fractional while outside stays 0 or 255.
- [ ] Render the preview at screen resolution in real time and High Quality Preview at full resolution on idle (IP-0510); budget: a real-time refresh under 100 ms on a 24-megapixel image at fit zoom. Done when: `RefineSessionBudgetTests` quote the refresh time.
- [ ] Add the entry points: Select, Select and Mask (Alt+Ctrl+R), the Select and Mask button on every selection tool's options bar (IP-0505), Layer Mask Properties Refine and the mask context menu (IP-0504), and refining an existing mask later (IP-0518). Done when: `SelectAndMaskEntryTests` open the session from each entry with the right source mask.
- [ ] Add `Imago.Masks.DoubleClickOpens` (`Properties` default, `SelectAndMask`) so double-clicking a layer mask can open the workspace (IP-0522), and enable §6's Focus Area button. Done when: `SelectAndMaskEntryTests` assert both key values.
- [ ] Add `SelectAndMaskWorkspace.xaml` and `SelectAndMaskViewModel` with the toolbar Quick Selection (§5), Refine Edge brush (IP-0511), Brush (add or subtract, hardness), Object Selection as a lasso here (the AI object tool is `D03 T19 §6`), Hand, and Zoom (IP-0506). Done when: a driven session uses each tool and the capture is committed. Cheaper substitute: a Feather and Contract dialog labeled Refine.
- [ ] Add Clear Selection and Invert buttons (IP-0507). Done when: `SelectAndMaskViewModelTests` assert both on a fixture mask.
- [ ] Add view modes from `SelectionPreviewRenderer` (onion skin, marching ants, overlay, on black, on white, black and white, on layers, transparent) with view opacity and overlay color (IP-0508). Done when: each mode is captured under docs/captures/imago/select-and-mask/.
- [ ] Add Show Edge (the band only) and Show Original (IP-0509). Done when: `SelectAndMaskViewModelTests` assert Show Original renders the unrefined mask.
- [ ] Add Edge Detection Radius and Smart Radius (band width adapts to local edge contrast) with Refine Mode Color Aware (IP-0513). Done when: `RefineSessionTests` show Smart Radius narrowing the band on a hard edge and widening it on hair.
- [ ] Route Refine Mode Object Aware to `D03 T19 §6` when AI is configured, otherwise disable it with the tooltip "Planned: D03 T19 §6". Done when: `SelectAndMaskViewModelTests` assert the disabled state and tooltip without an AI key.
- [ ] Add Global Refinements Smooth, Feather, Contrast, and Shift Edge (Photoshop) (IP-0514). Done when: `RefineSessionTests` assert Shift Edge and Contrast change coverage monotonically.
- [ ] Add Affinity's Refine Selection controls Matte Edges, Border Width, Smooth, Feather, and Ramp (IP-0515) and its refine brushes Matte, Foreground, Background, and Feather with a width (IP-0512). Done when: `RefineSessionTests` assert each brush's effect on the band.
- [ ] Add Decontaminate Colors with Amount, reusing `D03 T09 §14`'s `ColorDecontaminator` fed with §6's `ForegroundEstimator` output for the band and blended by amount; output forces a new layer or document, as Photoshop does (IP-0516). Done when: `DecontaminateTests` remove a quoted mean of green cast from a green-screen hair fixture's edge pixels.
- [ ] Call `D03 T09 §14`'s Remove Black Matte, Remove White Matte, and Defringe from the workspace's Output menu (IP-0503 and IP-0521 are owned there). Done when: `grep -rn "class .*Defringe" src/Imago/Photon.Imago.Core/Selection` prints nothing.
- [ ] Add Output To Selection, Layer Mask, New Layer, New Layer with Layer Mask, New Document, and New Document with Layer Mask as one "Select and Mask" undo step whatever the target (IP-0517). Done when: `RefineSessionTests` produce the right document object for each target.
- [ ] Add `Imago.SelectAndMask.RememberSettings` and `.imagerefine` JSON presets in `%LOCALAPPDATA%\Rizonesoft\Imago\Presets\Refine\` written through the atomic writer (IP-0519). Done when: `RefinePresetTests` round-trip a preset and refuse a malformed file by name.
- [ ] Add `Imago.SelectAndMask.Layout` = `Workspace`, `AffinityDialog`, or `LegacyRefineEdge`, choosing the layout over the same `RefineSession` (IP-0520). Done when: a driven run captures each layout and `SelectAndMaskViewModelTests` assert one session type serves all three.
- [ ] Report progress and Cancel for full-resolution output, and log one Information line per output as `Select and Mask {Output} {Radius} {Decontaminate}`. Done when: a driven output quotes the line and a cancelled output leaves the document unchanged.
- [ ] Commit `tests/fixtures/imago/selection/refine/hair.png` with its rough lasso mask and the expected alpha. Done when: the fixture README names each file.
- [ ] Update `docs/user/imago/select-and-mask.md` with the workspace, tools, view modes, refinements, decontamination, outputs, presets, and layouts. Done when: every control is documented.
- [ ] Commit: `"imago: Select and Mask with refine brushes, decontaminate colors, and every output"`

**Test checkpoint:** Driven run with evidence and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~RefineSessionTests|FullyQualifiedName~DecontaminateTests|FullyQualifiedName~SelectAndMaskEntryTests|FullyQualifiedName~RefinePresetTests"` exits 0, and a driven refine of `tests/fixtures/imago/selection/refine/hair.png` from its rough lasso produces a matte within 4/255 mean of the committed expected alpha, with each view mode captured. Cheaper substitute that fails: Feather plus Contract labeled Refine, which the hair golden rejects.

## 8. Modify and Transform Selection

Reshaping a selection without touching pixels is daily work: border, smooth, expand, contract, grow, similar, GIMP's remove holes, sharpen, and distort, transforming the outline, floating by cut and copy, and loading coverage from layers. This section adds them on the exact Euclidean distance transform `D03 T09 §14` puts in `Photon.Core`, consumed rather than re-implemented. Catalog: IP-0523 to IP-0534 (12 features).

**Fidelity:** Imago Select menu -- docs/captures/imago/main-window/; new captures to docs/captures/imago/modify-selection/ (Border and Distort dialogs, Transform Selection handles).
**Job:** a user can reshape an existing selection numerically or by hand without touching pixels. Consumer: the active `SelectionMask`.
**Treatment:** Select, Modify dialogs with live preview on the marching ants, and Transform Selection with free-transform handles on the outline only. Cheaper substitute that fails the checkpoint: Expand by a square dilation.
**Chrome:** consume §1's mask, the `D03 T03 §7` transform handles, and the `D01 T03 §2` resampler; do not write a second transform-handle overlay.

**Requires:** display-session -- the dialogs and on-canvas selection transform need an interactive desktop

- [ ] Add `SelectionMorphology` in `Photon.Imago.Core/Selection/Modify/` over `src/Photon.Core/Imaging/Morphology/DistanceTransform.cs` from `D03 T09 §14` (Felzenszwalb and Huttenlocher 2012), with circular Expand and Contract (GIMP's Grow and Shrink) (IP-0526). Done when: `SelectionMorphologyTests` expand then contract a disc and restore it within 1 px, and `grep` finds no second distance transform in Imago.
- [ ] Add Border with width, alignment Inside, Center, or Outside, style Hard, Smooth, or Feathered, GIMP's lock to selection edge, and Affinity's Outline with rounding (IP-0524). Done when: `SelectionMorphologyTests` measure the border width for each alignment.
- [ ] Add Smooth (Photoshop sample radius) as a median of coverage within a disc (IP-0525). Done when: `SelectionMorphologyTests` remove a 2 px notch at radius 3.
- [ ] Add Remove Holes (GIMP), filling enclosed unselected regions by flooding from the border (IP-0530), and Sharpen (GIMP), thresholding at 50 percent to remove antialiasing (IP-0531). Done when: `SelectionMorphologyTests` fill a ring fixture's hole and assert Sharpen leaves only 0 and 255.
- [ ] Add the Apply effect at canvas bounds option on Border, Shrink, and Feather (treat outside the canvas as selected), as `Imago.Selection.ModifyTreatsOutsideAsSelected` (IP-0527). Done when: `SelectionMorphologyTests` shrink a full-canvas selection with the option on and off and assert the edge rows.
- [ ] Add Grow (contiguous) and Similar (global) through §3's `FloodSelector` seeded by every selected pixel with the magic wand tolerance (IP-0528). Done when: `GrowSimilarTests` grow a seed region to its color boundary and select a detached same-color region with Similar.
- [ ] Add Distort (GIMP): Threshold, Spread, Granularity, and Smoothing with Smooth horizontally and vertically, seeded so the same seed reproduces (IP-0532). Done when: `DistortSelectionTests` produce byte-identical masks from the same seed and different ones from another seed.
- [ ] Add `TransformSelectionCommand` (Photoshop, Affinity): scale, rotate, skew, distort, perspective, and warp handles on the outline through the `D03 T03 §7` transform overlay, resampling the mask with the `D01 T03 §2` bicubic resampler as one "Transform Selection" step (IP-0529). Done when: `TransformSelectionTests` rotate a mask 90 degrees four times back to its start within 1/255. Cheaper substitute: a second handle overlay drawn for selections.
- [ ] Add Edit, Cut and Float and Copy and Float creating §1's `FloatingSelection`; Anchor stays in §1 (IP-0533). Done when: `FloatingSelectionTests` cut and float and the source region becomes transparent in one step.
- [ ] Add Alpha to Selection (GIMP) with Replace, Add, Subtract, and Intersect (IP-0523). Done when: `LayerCoverageSelectionTests` load a layer's alpha with each operation.
- [ ] Add Ctrl+click on a layer, mask, or channel thumbnail to load its coverage (Photoshop), Ctrl+Shift adds, Ctrl+Alt subtracts, Ctrl+Shift+Alt intersects, with text and shape layers contributing their rendered glyph or shape alpha (IP-0534). Done when: `LayerCoverageSelectionTests` assert each modifier's combine mode.
- [ ] Set the budget: Expand by 50 px on 24 megapixels under 150 ms; log one Information line per command with its parameters. Done when: the budget test quotes the time and a driven Border quotes its line.
- [ ] Commit GIMP 3.2.6 Grow, Shrink, and Border goldens under `tests/fixtures/imago/selection/modify/` with `reference.txt`. Done when: `SelectionModifyGoldenTests` compare each within 1/255.
- [ ] Update `docs/user/imago/selection.md` with the Modify commands, Transform Selection, floating selections, and layer coverage loading. Done when: every command is documented.
- [ ] Commit: `"imago: modify, transform, and float selections"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~SelectionModifyGoldenTests|FullyQualifiedName~SelectionMorphologyTests|FullyQualifiedName~DistortSelectionTests|FullyQualifiedName~TransformSelectionTests|FullyQualifiedName~LayerCoverageSelectionTests"` exits 0, with Grow, Shrink, and Border masks matching `gimp-console` output within 1/255. Cheaper substitute that fails: square dilation, which the circular-grow golden rejects at corners.

## 9. Select Menu Extensions

Users coming from each competitor look for selection commands where their app keeps them. This section completes the Select menu in one data-driven layout: Reselect, layer selection, Find Layers, and the Selection to Path and Path to Selection commands with GIMP's tracing options, wired through a bridge interface that `D03 T16 §5` implements. Catalog: IP-0535 to IP-0540 (6 features).

**Fidelity:** Imago Select menu -- docs/captures/imago/main-window/; new capture of the Selection to Path advanced dialog to docs/captures/imago/select-menu/.
**Job:** a user finds every selection command where Photoshop, Affinity, or GIMP users expect it. Consumer: the command registry and the active selection.
**Treatment:** a Select menu grouping All, Deselect, Reselect, Inverse; layer selection; Color Range, Focus Area, and Select and Mask; Modify; Grow and Similar; Transform Selection; Quick Mask; Load, Save, and file; To Path and From Path. Cheaper substitute that fails the checkpoint: a flat alphabetical menu.
**Chrome:** consume the command registry and keymap of `D03 T03 §4`; the menu grows through `D03 T20 §3` later without renaming these commands.

**Requires:** display-session -- the menu and dialog captures need an interactive desktop

- [ ] Add `SelectionHistory` in `Photon.Imago.Core/Selection/` keeping the last non-empty mask per document by tile sharing (not a copy), and `ReselectCommand` (Shift+Ctrl+D) restoring it as one step (IP-0535). Done when: `ReselectTests` restore a byte-equal mask after Deselect and assert tile sharing. Cheaper substitute: a full-size copy per selection.
- [ ] Add Select All Layers (Alt+Ctrl+A), Deselect Layers, and Find Layers (Alt+Shift+Ctrl+F, focusing the `D03 T09 §1` Layers panel search) (IP-0536). Done when: `LayerSelectionCommandTests` assert each command's effect on the layer selection.
- [ ] Add `SelectMenuLayout.json` in `Photon.Imago.Desktop/Menus/` listing the groups and command ids above, loaded into the menu so `D03 T20 §3` customizes it without code (IP-0537). Done when: `SelectMenuLayoutTests` resolve every command id and find no duplicates.
- [ ] Add `ISelectionPathBridge` in `Photon.Imago.Core/Selection/Paths/` with `SelectionFromPath(pathId, operation, antialias, feather)` and `PathFromSelection(SelectionToPathOptions)`. Done when: the interface compiles with a fake implementation in `SelectionPathBridgeTests`.
- [ ] Add `SelectionToPathOptions` carrying GIMP's `sel2path` parameters (align threshold, corner always threshold, corner surround, corner threshold, error threshold, filter alternative surround, filter epsilon, filter iteration count, filter percent, keep knees, line reversion threshold, line threshold, reparametrize improvement, reparametrize threshold, subdivide search, subdivide surround, subdivide threshold, tangent surround) with GIMP 3.2.6's defaults (IP-0540). Done when: `SelectionToPathOptionsTests` assert every default equals GIMP's.
- [ ] Add the Selection to Path, Selection to Path (Advanced), and Path to Selection commands (from a path, shape layer, or curve, with §1's combine modes), disabled with the tooltip "Planned: D03 T16 §5" until that section registers the bridge implementation (IP-0538, IP-0539). Done when: `SelectMenuLayoutTests` assert the three commands are present and disabled with that tooltip while no bridge is registered.
- [ ] Add `SelectionToPathAdvancedDialog.xaml` over `SelectionToPathOptions` with Reset to GIMP defaults. Done when: the dialog capture is committed to docs/captures/imago/select-menu/.
- [ ] Write one Information line and one undo step per Select menu command. Done when: `grep -rn "Select" src/Imago/Photon.Imago.Desktop/Menus` finds no command whose handler only logs, quoted in the section's evidence.
- [ ] Update `docs/user/imago/selection.md` with the Select menu layout, Reselect, layer selection, and path conversion. Done when: every command is documented.
- [ ] Commit: `"imago: the Select menu, Reselect, layer selection, and the selection-to-path bridge"`

**Test checkpoint:** Unit test and static analysis clean: `dotnet test Photon.slnx --filter "FullyQualifiedName~ReselectTests|FullyQualifiedName~SelectMenuLayoutTests|FullyQualifiedName~SelectionToPathOptionsTests|FullyQualifiedName~LayerSelectionCommandTests"` exits 0, and a `grep` over `src/Imago/Photon.Imago.Desktop/Menus` finds no Select menu handler that only logs. Cheaper substitute that fails: Reselect storing a full-size copy per selection, which the tile-sharing assertion in `ReselectTests` catches.

## 10. The Channels Panel, Spot Channels, and Quick Mask Options

Channels are where saved selections live, where spot inks live, and where masks are painted by hand. This section adds a Channels panel over §1's `DocumentChannels` with per-mode color channels, alpha and spot channels with options, duplicate, reorder, lock, and color tags, channel-to-selection modifiers, Affinity's composite alpha and pixel selection channels, split and merge channels (the engine `D03 T11 §8` extends), painting and filtering channels, and Quick Mask with options. Catalog: IP-0546 to IP-0564 (19 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/channels/ (panel, Channel Options, New Spot Channel, Quick Mask Options, a spot channel in color).
**Job:** a user can store, edit, and combine masks as channels, keep spot inks, and paint a selection in quick mask. Consumer: the document's channel store, the active selection, and `D03 T17 §2`'s PSD writer.
**Treatment:** a dockable Channels panel listing the composite and per-mode color channels (RGB, CMYK, Lab, gray, and the `D03 T11 §7` modes), then alpha and spot channels, with eye, target, thumbnail, name, lock, and color tag, plus Channel Options and Quick Mask Options dialogs. Cheaper substitute that fails the checkpoint: a list of saved selections with no targeting or painting.
**Chrome:** consume `DocumentChannels` from §1, the `D03 T05 §1` filter pipeline, the `D03 T03 §6` brush, and the theme; do not add a second mask store.

**Requires:** display-session -- the panel, dialogs, and quick mask painting need an interactive desktop

- [ ] Add `ChannelsPanel.xaml` and `ChannelsPanelViewModel` in `Photon.Imago.Desktop/Channels/`: the composite plus component rows per mode (the `D03 T11 §7` mode list), thumbnails, eye and target toggles, and reset (IP-0546). Done when: `ChannelsPanelViewModelTests` list RGB and CMYK documents' rows in order. Cheaper substitute: a list of saved selections with no targeting.
- [ ] Add Ctrl+2 for the composite and Ctrl+3 onward for single channels (IP-0547), and Show Channels in Color as `Imago.Channels.ShowInColor` (IP-0548, IP-0564). Done when: `ChannelsPanelViewModelTests` assert each shortcut's target and the key's effect on thumbnails.
- [ ] Add alpha channel New, Delete, and Rename (IP-0550), Raise, Lower, and drag reorder (IP-0552), each one undo step. Done when: `ChannelModelTests` assert each command and its undo.
- [ ] Add Duplicate Channel to the same, another, or a new document with Invert (IP-0553). Done when: `ChannelModelTests` duplicate into a new document and assert inverted pixels.
- [ ] Add multi-select and GIMP's channel color tags (IP-0554). Done when: `ChannelsPanelViewModelTests` multi-select three channels and delete them in one step.
- [ ] Enforce a 56-channel limit matching Photoshop for PSD round trips, refused by name beyond it. Done when: `ChannelModelTests` assert the 57th New Channel is refused with the limit named.
- [ ] Add `ChannelOptionsDialog.xaml` for New Channel and Channel Options: name, Color Indicates Masked or Selected Areas, color, and opacity, stored on `AlphaChannel` and written as attributes of §1's `<imago:channel>` element (IP-0551). Done when: `ChannelPersistenceTests` round-trip every attribute.
- [ ] Add channel lock attributes (Affinity and GIMP): lock pixels, position, visibility, and editable, a lock policy that refuses the matching edit by name (IP-0549). Done when: `ChannelModelTests` assert each refusal text.
- [ ] Add channel to selection: the load button or Ctrl+click on the thumbnail, Ctrl+Shift add, Ctrl+Alt subtract, Ctrl+Shift+Alt intersect (Photoshop), and GIMP's Channel to Selection with Replace, Add, Subtract, and Intersect (IP-0555). Done when: `ChannelSelectionModifierTests` assert each modifier's combine mode.
- [ ] Add Affinity's composite alpha channel and a live Pixel Selection channel listed in the panel (IP-0556). Done when: `ChannelsPanelViewModelTests` show the Pixel Selection row updating when the selection changes.
- [ ] Add the channel context menu Load to (layer red, green, blue, alpha, mask, adjustment, filter, grayscale layer, mask layer), Invert, Clear, and Fill (IP-0557). Done when: `ChannelModelTests` load a channel into a layer's alpha and assert the pixels.
- [ ] Make a targeted alpha channel a paint target for every `D03 T03 §6` brush and a filter target for the `D03 T05 §1` pipeline (destructive); live filters on channels are `D03 T14 §1` (IP-0558). Done when: `ChannelPaintTests` paint a dab into a targeted channel and blur it, leaving the layer untouched.
- [ ] Add New Spot Channel (ink color from the picker or a user color book, solidity 0 to 100) and Spot Channel Options (Photoshop) (IP-0559). Done when: `SpotChannelTests` create a spot channel and round-trip its ink and solidity.
- [ ] Render spot channels in the composite at their solidity and add Merge Spot Channel into the color channels through `D01 T04 §1` (IP-0559). Done when: `SpotChannelTests` assert a merge at solidity 100 equals a multiply of the ink.
- [ ] Add `ChannelSplitter` and `ChannelMerger` in `Photon.Imago.Core/Channels/`: Split Channels into grayscale documents named `<name>_R` and so on, and Merge Channels back by mode and channel mapping (IP-0560). Done when: `SplitMergeChannelsTests` split then merge byte-identically on RGB and CMYK fixtures.
- [ ] Move `QuickMask` onto `SelectionMask` so every brush paints it, with Q toggling and the toolbox button reflecting the state (IP-0561, IP-0563). Done when: `QuickMaskTests` paint in quick mask and exit to the expected selection.
- [ ] Add `QuickMaskOptionsDialog.xaml`: Masked or Selected Areas, color, opacity, and Affinity's view style overlay, grayscale, or transparent, as `Imago.Channels.QuickMask.*` keys (IP-0562). Done when: `QuickMaskTests` read each key and a capture shows each view style.
- [ ] Record undo names "New Channel", "Channel Options", "Merge Spot Channel", "Split Channels", and "Quick Mask" and log one Information line per command. Done when: a driven spot channel merge quotes its line.
- [ ] Commit `tests/fixtures/imago/channels/three-alpha-one-spot.imago` with a README. Done when: `ChannelPersistenceTests` reopen it with every channel's name, color, opacity, solidity, and pixels equal.
- [ ] Update `docs/user/imago/channels.md` with the panel, alpha and spot channels, split and merge, and quick mask options. Done when: every control is documented.
- [ ] Commit: `"imago: the Channels panel, alpha and spot channels, split and merge, and quick mask options"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ChannelModelTests|FullyQualifiedName~ChannelSelectionModifierTests|FullyQualifiedName~SplitMergeChannelsTests|FullyQualifiedName~SpotChannelTests|FullyQualifiedName~ChannelPersistenceTests|FullyQualifiedName~QuickMaskTests"` exits 0, and `tests/fixtures/imago/channels/three-alpha-one-spot.imago` is opened, saved, reopened, and every channel's name, color, opacity, solidity, and pixels compare equal. Cheaper substitute that fails: storing channels as hidden layers, which the reopen assertion on channel kind and solidity catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` passes every selection, matting, modify, and channel fixture this file adds, with each GIMP 3.2.6 golden's version recorded in its `reference.txt`
- [ ] Every capture named in a Fidelity line exists under `docs/captures/imago/`, and every user guide page named in a section exists under `docs/user/imago/`
- [ ] No second mask store, preview compositor, flood fill, matting routine, or distance transform exists in Imago (`grep` over `src/Imago` for each, quoted)
- [ ] B-027 is gone from `todo/backlog.md`, and §3 carries its source key
- [ ] Every catalog row IP-0448 to IP-0564 owned by this file is covered by a shipped section, and `docs/parity/imago-parity.md` statuses agree
- [ ] `python scripts/todo-claims.py` holds for this file
- [ ] `python scripts/todo-graph.py validate` clean
