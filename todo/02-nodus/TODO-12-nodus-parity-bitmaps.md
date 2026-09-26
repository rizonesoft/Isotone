---
schema_version: 1
id: nodus-parity-bitmaps
domain: 02-nodus
status: draft
title: "TODO-12 -- Nodus Parity: Bitmaps, Tracing, and Raster Effects"
depends_on: []
track: N12
---

# TODO-12 -- Nodus Parity: Bitmaps, Tracing, and Raster Effects

> **Goal:** Nodus treats placed images as first-class bitmap objects: a designer can crop, resample, straighten, correct perspective, change color mode, mask colors, and rasterize vector art; apply every `Photon.Core` pixel-engine effect and adjustment non-destructively through an FX stack that persists in the `nodus:` namespace with a rasterized SVG fallback; trace bitmaps into editable vectors with a Nodus-local potrace port (outline) and skeletonization (centerline) behind both an Image Trace panel and a trace dialog; build vector and image mosaics and photo mockups; and manage linked files through a Links panel. `D02 T06 §14` (File, Place for images) is relocated into Phase 9 ahead of §1 so placing images exists before bitmap editing starts.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The bitmap element exists as `SvgImage` in `src/Nodus/Bezier.Core/Models/Elements/SvgImage.cs` with position, size, `Href`, `EmbeddedData`, and `MimeType`, and nothing else: no decoded pixels, no color mode, no resolution. `src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs` has no branch for it, so a parsed `<image>` is invisible on the canvas today. `src/Nodus/Bezier.Core/Services/ImportService.cs` can build an embedded image element from raster bytes (`ImportRasterImage`), but no file in `src/Nodus/Bezier.Desktop/` references `ImportService`; the service triage defers it to `D02 T06 §14`. The SVG reader `src/Nodus/Bezier.Core/Services/SvgParser.cs` never mentions filters, so a `<filter>` is dropped on open. There is no tracing code in Nodus (`src/Nodus/Bezier.Core/Tracing` does not exist), no mosaic code, and no link management.
<!-- claim: exists src/Nodus/Bezier.Core/Models/Elements/SvgImage.cs -->
<!-- claim: count "SvgImage" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->
<!-- claim: count "ImportRasterImage" src/Nodus/Bezier.Core/Services/ImportService.cs = 5 -->
<!-- claim: count "ImportService" src/Nodus/Bezier.Desktop/**/*.cs = 0 -->
<!-- claim: count "(?i)filter" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->
<!-- claim: absent src/Nodus/Bezier.Core/Tracing -->

## Inputs

- [`standards/nodus.md`](../../standards/nodus.md) -- SVG is native, one renderer, every mutation is a command, Inkscape is the fidelity reference
- [`standards/shared.md`](../../standards/shared.md) -- budgets, progress and cancel over one second, one log line per document change, the design contract
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- the blueprint for this file; [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) -- the catalog rows each section owns
- potrace 1.16 by Peter Selinger (GPL-2.0-or-later, compatible with the suite's GPL-3.0) -- the ported outline tracing algorithm and the black-and-white golden oracle for §4
- Inkscape 1.4 Trace Bitmap (potrace-based, multiscan colors and centerline) -- the second tracing oracle for §4 and §5, and the SVG filter golden renderer for §8
- W3C Filter Effects Module Level 1 and SVG 1.1 chapter 15 -- the SVG filter primitives §8 reads, renders, and writes
- -> XREF: D02 T06 §14 -- File, Place for images and `SvgImage` rendering, relocated into Phase 9 ahead of §1
- -> XREF: D01 T03 §1 -- pixel buffers, the effect contract, and the registry the FX stack wraps
- -> XREF: D01 T03 §2 -- resampling, rotation, and perspective behind the §1 dialogs
- -> XREF: D01 T03 §3 -- 1-bit and paletted conversion for §1 and the color reduction §4 traces through
- -> XREF: D01 T03 §4 -- tonal adjustments and presets data behind §3 and the trace adjustments page
- -> XREF: D01 T03 §5 -- color adjustments behind §3
- -> XREF: D02 T07 §1 -- the live-object contract the FX stack, live traces, and mockups persist through
- -> XREF: D02 T11 §1 -- the live-effect framework the FX stack registers raster effects in
- -> XREF: D02 T11 §5 -- the envelope mesh the mockups warp through
- -> XREF: D02 T11 §11 -- the lens framework the bitmap effect lens joins
- -> XREF: D02 T11 §17 -- Live Paint for editing expanded trace results
- -> XREF: D01 T04 §3 -- the Lab, CMYK, and duotone conversions the §1 mode commands wait for
- -> XREF: D02 T15 §9 -- AI upsampling, shown disabled on the §5 adjustments page until it ships
- -> XREF: D02 T15 §10 -- AI-assisted tracing that extends §5
- -> XREF: D01 T02 §3 -- single-instance forwarding Edit Bitmap in Imago relies on
- -> XREF: D02 T14 §9 -- EPS placement, which keeps placed EPS linked through §7 and reads its low-resolution proxy setting
- -> XREF: D02 T13 §7 -- honors the `nodus:overprint-black` flag §1's Convert to Bitmap writes
- -> XREF: D02 T13 §8 -- prints raster effects at the §2 Document Raster Effects Settings resolution
- -> XREF: D01 T06 §1 -- the pixel engine extensions cites §2: Nodus's effect gallery lists the new effects from the registry with no Nodus change
- -> XREF: D03 T09 §10 -- Imago parity layers cites §7: Nodus's `LinkManager`, moved to `Photon.Core` by D03 T09 §10

## Outcome

- A placed image is a bitmap object with decoded pixels, color mode, pixel size, and effective ppi on the status bar, and every bitmap command (crop, crop to shape, resample, straighten, correct perspective, rasterize, mode change, color mask, monochrome coloring, make pixel perfect) is one undoable command that survives save and reopen as a live value.
- Every `Photon.Core` pixel effect and adjustment appears in the Effects menu, stacks non-destructively in the FX panel, previews at screen scale, and reopens as a live stack while other SVG readers see a rasterized fallback image.
- The Image Adjustment Lab composes tone and color corrections with a live histogram, snapshots, and presets, as one FX stack entry.
- Outline and centerline tracing produce editable vectors from logos, sketches, and photos, matching potrace 1.16 and Inkscape 1.4 goldens, through a live trace object, an Image Trace panel, and a trace dialog with presets.
- Pointillizer, PhotoCocktail, Object Mosaic, and photo mockups turn photos into mosaics and place art onto product photos.
- The Links panel reports missing and modified linked files, relinks, updates, embeds, and unembeds them.
- SVG filters stay live `<filter>` elements through open, edit, render, and save.

**Adjacency:** list=applicable @ D02 T12 §7; document=applicable @ D02 T13 §1; settings=applicable @ D01 T02 §2; reporting=applicable @ D02 T12 §4; notifications=applicable @ D02 T12 §7; permissions=applicable @ D02 T12 §7; audit=applicable @ D02 T12 §1; exchange=applicable @ D02 T12 §8; reverse=applicable @ D02 T12 §2

**Adjacency rationale:** The Links panel with its missing, modified, and embedded filters is the main list, beside the trace preset list and the PhotoCocktail library browser. Rasterized effects and bitmaps print through the print pipeline, which also honors the always-overprint-black flag. Every tunable (straighten grid, trace defaults, link update policy, raster effect resolution) lives in the suite settings store. Reporting is the bitmap info on the status bar, trace statistics, link file info, and the Lab histogram. Effects, traces, and mosaics show progress and cancel on the status strip, and missing or modified links raise alerts per the update policy. A missing, locked, or read-only linked file is refused by name on relink and unembed. Every edit is an undoable command with one Serilog line in the history. SVG `<image>` and `<filter>` round trips, color-mask files, trace presets, palette files, and unembedded images are the exchange formats. Undo reverses every command, a trace releases back to its image, and flatten and break link are undoable.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Bitmap objects: crop, resample, rasterize, convert to bitmap, color mask, and straighten | D01 T03 §2, D02 T06 §14 |  [ ]   |
|   2   |   §2    | The effect stack on objects: FX panel, effect gallery, preview, flatten, and effect lenses | D01 T03 §1, D02 T11 §1 |  [ ]   |
|   3   |   §3    | Adjustments in Nodus: the Image Adjustment Lab and adjustment presets | D01 T03 §5, §2 |  [ ]   |
|   4   |   §4    | The tracing engine: outline tracing, color quantization, and stacking | D01 T03 §3 |  [ ]   |
|   5   |   §5    | Centerline tracing, the Image Trace panel, and PowerTRACE | §4 |  [ ]   |
|   6   |   §6    | Photo artwork: Pointillizer, PhotoCocktail, Object Mosaic, and mockups | §1, D02 T11 §5 |  [ ]   |
|   7   |   §7    | The Links panel and linked sources | §1 |  [ ]   |
|   8   |   §8    | SVG filter effects | §2 |  [ ]   |

---

## 1. Bitmap Objects: Crop, Resample, Rasterize, Convert to Bitmap, Color Mask, and Straighten

A designer who places a photo expects to fix it where it sits: crop it, straighten it, reduce it, mask a background color, or turn vector art into a bitmap. This section gives `SvgImage` decoded pixels and a color mode and wires every bitmap command onto the `D01 T03` engine, each as one undoable command whose result survives save and reopen as a live value rather than a flattened guess. `D02 T06 §14` (File, Place and `SvgImage` rendering) is relocated into Phase 9 ahead of this section, so this section starts from placed, visible images. Lab, CMYK, and Duotone modes are present but disabled naming `D01 T04 §3`, which ships their conversions in Phase 10. Catalog: NP-1753 to NP-1783 (31 features: crop image and its resolution, make pixel perfect, rasterize and convert to bitmap with dithered, overprint black, anti-aliasing, and transparent background options, convert to bitmap on export, bitmap info on the status bar, crop to an irregular shape and node editing of the boundary, the Resample dialog, straighten with its crop, grid, and remember options, monochrome coloring, the bitmap color mask panel with hide or show, tolerance, save and open, and edit color, the seven bitmap modes, and correct perspective).

**Fidelity:** new build, no baseline; captured to `docs/captures/nodus/bitmaps/` (Bitmaps menu, Resample, Straighten Image, Correct Perspective, Convert to Bitmap, Black and White, and Paletted dialogs, Bitmap Mask panel), main window changes to `docs/captures/nodus/main-window/`.
**Job:** a designer can place a photo and fix, reduce, and mask it without leaving Nodus. Consumer: the document and the SVG writer.
**Treatment:** modal dialogs with live preview, the color mask as a dockable panel, crop handles and boundary node editing on the canvas. Cheaper substitute that fails the checkpoint: a single Image Properties dialog with numeric fields and no preview.
**Chrome:** consume the shared theme, the icon catalog, the suite history (`D01 T02 §4`), the settings store (`D01 T02 §2`), `Photon.UI` numeric controls, and the Nodus color picker from `D02 T09 §2`. Do not add a second color picker or a Nodus-local undo.

**Requires:** display-session -- the dialogs, on-canvas crop handles, and boundary node editing need an interactive desktop

- [ ] Confirm the relocated `D02 T06 §14` has shipped: File, Place embeds and links PNG, JPEG, and WebP, and `SkiaRenderer` draws `SvgImage`. Done when: `python scripts/todo-graph.py resolve 'D02 T06 §14'` exits 3 and a placed PNG fixture renders on the canvas.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Imaging/IBitmapCodec.cs` (decode to and encode from `PixelBuffer<Rgba8>`, 1-bit, gray, indexed, and RGB PNG) and `src/Nodus/Photon.Nodus.Desktop/Imaging/WicBitmapCodec.cs` over WPF `BitmapDecoder` and `BitmapEncoder`, injected through the composition root. Done when: `WicBitmapCodecTests` decode the PNG and JPEG fixtures under `tests/fixtures/nodus/svg/bitmaps/` to the expected pixel hashes and re-encode 1-bit, gray, and indexed PNG losslessly. Source: Microsoft Learn, `System.Windows.Media.Imaging.BitmapDecoder`.
- [ ] Extend `src/Nodus/Photon.Nodus.Core/Models/Elements/SvgImage.cs` with a lazily decoded `PixelBuffer` cache (invalidated when `EmbeddedData` or `Href` changes), `ColorMode`, `PixelWidth`, `PixelHeight`, and `EffectivePpi`. Done when: `SvgImageTests` assert the cache decodes once and the ppi for a 300 by 300 pixel image drawn at 72 by 72 document units is 300.
- [ ] Show color mode, pixel size, and effective ppi of a selected bitmap on the status strip (CD-1968). Done when: a driven run selects the photo fixture and the capture shows "RGB 24-bit, 3000 x 2000 px, 300 ppi". Cheaper substitute: the file name only.
- [ ] Add `CropImageCommand` (Object, Crop Image) with on-canvas crop handles, Enter to apply and Escape to cancel, and a resolution field that resamples the kept pixels (AI-0205, AI-0206). Done when: `BitmapCommandTests.CropImage` asserts the pixel size and the undo restores the original bytes by SHA-256.
- [ ] Add `CropBitmapToShapeCommand` that keeps the pixels and stores an irregular boundary as an SVG `clipPath` referenced by the image (CD-1969, CD-2074). Done when: a reopen test restores the boundary as a live crop and an external reader (Inkscape 1.4) renders the clipped result within the fidelity tolerance.
- [ ] Let the node editing tool edit the bitmap boundary's nodes, each drag one command (CD-1970). Done when: a driven run moves a boundary node and Ctrl+Z restores it (log lines quoted).
- [ ] Add Bitmaps, Resample (`Views/Dialogs/ResampleDialog.xaml`) over `D01 T03 §2` `ResampleRequest`: mode, width and height in pixels or physical units, horizontal and vertical dpi, maintain aspect, maintain file size, before and after pixel counts (CD-1971). Done when: `ResampleDialogViewModelTests` cover each option and OK runs `ResampleBitmapCommand`, which re-encodes the embedded image. Cheaper substitute: scaling the element without resampling pixels.
- [ ] Add Bitmaps, Straighten Image (`Views/Dialogs/StraightenDialog.xaml`) with an angle up to plus or minus 15 degrees and a live preview over `Rotator` (CD-1981). Done when: a driven run straightens the tilted-horizon fixture and the capture shows the preview.
- [ ] Add the straighten crop options (crop and resample to original size, crop only, no crop) through `Rotator.CropToRotatedRect` (CD-1983), grid size and color (CD-1984), and Remember settings stored under `Nodus.Bitmaps.Straighten.*` (CD-1985). Done when: `StraightenDialogViewModelTests` assert each crop option's output size and the remembered values survive a restart.
- [ ] Add Bitmaps, Correct Perspective with four on-canvas corner handles and vertical and horizontal sliders over `PerspectiveCorrector` (CD-2075). Done when: `BitmapCommandTests.CorrectPerspective` rectifies the keystoned-sign fixture within the `D01 T03 §2` tolerance and undo restores it.
- [ ] Add one `RasterizeCommand` behind Object, Rasterize and Bitmaps, Convert to Bitmap, with a dialog for resolution and color mode (AI-0211, CD-1961). Done when: rasterizing the vector fixture at 150 ppi yields an `SvgImage` of the expected pixel size in the same position.
- [ ] Add the Convert to Bitmap options dithered, anti-aliasing, and transparent background (CD-1962, CD-1964, CD-1965). Done when: tests assert a transparent background leaves alpha 0 outside the art and anti-aliasing off yields only the art's exact colors on its edges.
- [ ] Add Always overprint black, stored as `nodus:overprint-black="true"` on the result for `D02 T13 §7` to honor (CD-1963). Done when: the attribute round-trips through save and reopen.
- [ ] Offer the same option set (size, resolution, color mode, dithering) in the raster export dialog from `D02 T06 §14` through one shared `RasterizeOptions` view model (CD-1966). Done when: a test asserts both dialogs bind the same view model type.
- [ ] Add the Bitmaps, Mode submenu with RGB (24-bit) and Grayscale (8-bit) commands and the Black and White (1-bit) dialog over `D01 T03 §3` `BilevelConverter` with every method and intensity (CD-2021, CD-2003, CD-1995). Done when: each command changes `ColorMode`, re-encodes the image as RGB, gray, or 1-bit PNG, and records `nodus:color-mode`.
- [ ] Add the Paletted (8-bit) dialog: palette type, color count, dithering and intensity, range sensitivity, the processed palette editor, and presets saved under `%LOCALAPPDATA%\Rizonesoft\Nodus\presets\paletted\` (CD-2009). Done when: a preset saved in the dialog reloads with every field and the result is an indexed PNG with at most the chosen count of colors. Cheaper substitute: a fixed 256-color palette.
- [ ] Show Lab (24-bit), CMYK (32-bit), and Duotone (8-bit) in the Mode submenu disabled with the tooltip `Planned: D01 T04 §3` (CD-2022, CD-2023, CD-2004). Done when: `MenuAuditTests` finds each item disabled with a tooltip that `python scripts/todo-graph.py resolve 'D01 T04 §3'` resolves.
- [ ] Color a 1-bit bitmap from the palette: a click sets the background color and a right-click the foreground, stored as `nodus:mono-colors` with the recolored PNG as the fallback (CD-1988). Done when: reopening restores the two colors as live values and an external reader shows the recolored image.
- [ ] Add the Bitmap Mask panel (`Views/Panels/BitmapMaskPanel.xaml`): up to 10 color slots, hide or show selected colors, tolerance per slot, an eyedropper, and Edit Color through the Nodus color picker (CD-1990, CD-1991, CD-1992, CD-1994). Done when: masking the white backdrop of the product fixture at tolerance 10 makes it transparent on the canvas and the capture shows the panel.
- [ ] Save and open masks as Nodus JSON and read Corel `.ini` masks, with a committed `.ini` fixture under `tests/fixtures/nodus/bitmaps/masks/` (CD-1993). Done when: `BitmapMaskFileTests` read the `.ini` fixture into the expected slots and round-trip the JSON.
- [ ] Persist the mask as `nodus:color-mask` parameters with the masked PNG as the fallback. Done when: reopening restores the slots live and an external reader shows the masked image.
- [ ] Add Object, Make Pixel Perfect (`MakePixelPerfectCommand`) snapping path nodes and bitmap bounds to the 1-pixel grid at 72 ppi document units (AI-0210). Done when: a test asserts every node of the fixture lands on a whole pixel and undo restores the original coordinates.
- [ ] Run every bitmap command over 1 second off the UI thread with status-strip progress and Cancel, never blocking the UI. Done when: a driven run cancels a resample of the 24-megapixel fixture, the image is unchanged, and the cancel log line is quoted.
- [ ] Record every command in the history with one Serilog Information line (`Bitmap {Command} on {ElementId}: {Summary}`). Done when: `BitmapCommandTests` assert one history entry and one log line per command with a Serilog test logger.
- [ ] Add the reopen test `BitmapRoundTripTests`: crop, crop to shape, mode, mask, and mono colors survive save and reopen as live values, not as the fallback. Done when: every case passes against the fixtures in `tests/fixtures/nodus/svg/bitmaps/`.
- [ ] Update the Nodus user guide page `docs/user/nodus/bitmaps.md` in the same commit. Done when: the page documents every command, dialog, and panel control.
- [ ] Commit: `"nodus: bitmap objects with crop, resample, straighten, modes, and color masks"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Photon.slnx` exits 0 with `WicBitmapCodecTests`, `BitmapCommandTests`, `BitmapMaskFileTests`, and `BitmapRoundTripTests` reporting (each command, its undo, and SVG reopen as a live value against `tests/fixtures/nodus/svg/bitmaps/`), and a driven session places, straightens, masks, and converts the photo fixture to paletted with captures committed under `docs/captures/nodus/bitmaps/` and the log lines quoted. Cheaper substitute that fails: mode changes applied only to the on-screen preview, which the reopen test rejects.

## 2. The Effect Stack on Objects: FX Panel, Effect Gallery, Preview, Flatten, and Effect Lenses

Bitmap effects must stay editable: a designer tunes a blur after reopening the file, hides it for a proof, reorders it under a grain, and flattens only when ready. This section registers every `D01 T03` effect as a raster effect in the `D02 T11 §1` effect stack, so one stack holds vector and raster effects alike, and adds the FX panel, the Effect Gallery, the Document Raster Effects Settings, cached preview, flatten, and the bitmap effect lens. The stack persists as `nodus:` parameters with a rasterized `<image>` fallback, so other SVG readers still see the look. Catalog: NP-1995 to NP-2008 (14 features: Document Raster Effects Settings, Rasterize as a live effect, the Effect Gallery, the bitmap effect lens, the non-destructive stack in the FX panel, effects on vector and bitmap objects, add effect, show or hide one effect, show or hide all effects of an object, reorder, delete, before and after preview, reset effect settings, and flatten effects).

**Fidelity:** new build, no baseline; captured to `docs/captures/nodus/effects-panel/` (FX panel, Effect Gallery, Document Raster Effects Settings) and `docs/captures/nodus/main-window/` (Effects menu).
**Job:** a designer can stack, tune, reorder, hide, and flatten bitmap effects on vector or bitmap objects and keep editing them after reopening. Consumer: the renderer, the SVG writer, and export.
**Treatment:** an FX panel list with eye toggles, drag reorder, per-effect parameter editors, and a full or split before and after preview. Cheaper substitute that fails the checkpoint: a one-shot destructive filter per menu item.
**Chrome:** consume the `D02 T11 §1` effect registry and stack evaluator, the shared theme and icon catalog, the suite history, and the settings store. Do not build a second effect list beside the appearance stack.

**Requires:** display-session -- the FX panel, the Effect Gallery, and the live preview need an interactive desktop

- [ ] Add `src/Nodus/Photon.Nodus.Core/Effects/BitmapEffectNode.cs`, which registers every `D01 T03` `IPixelEffect` in the `D02 T11 §1` registry as a raster effect with its schema. Done when: `EffectStackTests.EveryEngineEffectRegistered` asserts the Nodus registry holds one raster entry per `Photon.Core` `EffectRegistry` id.
- [ ] Generate the Effects menu from `EffectRegistry` categories so every engine effect has a menu item without hand wiring. Done when: `MenuAuditTests` count one enabled item per registered effect.
- [ ] Rasterize vector objects for raster effects at the Document Raster Effects Settings (color model, resolution 72, 150, 300, or custom; white or transparent background; anti-alias; clipping mask; added margin; preserve spot colors), stored per document as `nodus:raster-effects` with defaults under `Nodus.Effects.Raster.*` (AI-0644). Done when: changing the resolution to 300 re-renders the stack at 300 ppi, asserted in a test.
- [ ] Read the auto-inflate document default from `nodus:raster-effects` and pass it to `D01 T03 §1` `BitmapInflation.AutoInflate`. Done when: a blurred bitmap's bounds grow by the blur margin with auto inflate on and not with it off.
- [ ] Register Rasterize as a live effect using the same settings (AI-0694). Done when: it appears in the stack and reopening keeps it live.
- [ ] Add the FX panel (`Views/Panels/EffectsPanel.xaml`, a tab of the Properties panel) listing the selected object's stack, with Add effect from a category menu (CD-2100). Done when: a driven run adds Gaussian Blur to a vector star and the capture shows the entry.
- [ ] Add the eye toggle per effect and a show or hide all toggle for an object, also on the Layers panel row (CD-2101, CD-2102). Done when: `EffectStackTests.HideEffect` asserts the rendered hash equals the unaffected render while hidden.
- [ ] Add drag reorder and Delete for applied effects, each one undoable command (CD-2103, CD-2104). Done when: reorder and delete undo in tests and a driven run shows both. Cheaper substitute: up and down buttons with no undo.
- [ ] Generate each effect's parameter editor from `EffectParameterSchema` (sliders, numeric boxes, enums, colors, points, curves), with Reset to defaults (CD-2106), each change one undoable command merged while a slider drags. Done when: a slider drag records one history entry, and Reset restores every default.
- [ ] Add full and split before and after preview for the selected effect (CD-2105). Done when: a driven run shows the split view capture.
- [ ] Add `src/Nodus/Photon.Nodus.Desktop/Rendering/EffectRenderCache.cs` keyed by object content hash, stack hash, and zoom bucket, rendering at `PreviewScale` while a slider moves and at full resolution on release, and cancelling a superseded render. Done when: `EffectRenderCacheTests` assert a cache hit on an unchanged redraw and a cancelled superseded job.
- [ ] Add the Effect Gallery dialog (`Views/Dialogs/EffectGalleryDialog.xaml`): a thumbnail grid of the artistic, brush-stroke, distort, sketch, stylize, and texture effects with a stacked-list builder (AI-0720). Done when: a driven run builds a two-effect stack in the gallery and OK adds both to the FX panel.
- [ ] Add the Tune blur, Tune sharpen, and Tune noise thumbnail pickers over the `D01 T03 §6` tune variants. Done when: picking a variant adds its underlying effect with the variant's parameters.
- [ ] Apply effects to vector and bitmap objects alike, vector objects rasterized per the settings above (CD-2096, CD-2097, CD-2094, CD-2095, CD-2099). Done when: `EffectStackTests` apply the same stack to the star and to the photo fixture.
- [ ] Persist the stack as a `<nodus:effects>` child with one `<nodus:effect id version seed ...>` per entry, and write the rasterized result as an `<image>` fallback. Done when: `EffectStackRoundTripTests` reopen the fixtures under `tests/fixtures/nodus/svg/effects/` with a live stack and Inkscape 1.4 renders the fallback within the fidelity tolerance.
- [ ] Add Flatten Effects, which replaces the object with an `SvgImage` of the rendered pixels as one undoable command (CD-2107). Done when: flatten then undo restores the live stack and object.
- [ ] Add the bitmap effect lens as a lens type in the `D02 T11 §11` framework that applies a stack to everything beneath the lens shape (CD-1920, CD-2098). Done when: a lens with Invert over half the photo fixture inverts only the covered half.
- [ ] Add a budget test: a five-effect stack on a 12-megapixel bitmap previews at screen scale under 200 ms per parameter change and renders in full with progress and cancel. Done when: `EffectStackBudgetTests` quote the times.
- [ ] Log one Information line per stack change (`Effect {Action} {EffectId} on {ElementId}`). Done when: a Serilog test logger asserts the lines.
- [ ] Update the Nodus user guide page `docs/user/nodus/effects.md`. Done when: the page documents every FX panel and gallery control.
- [ ] Commit: `"nodus: the non-destructive bitmap effect stack, FX panel, and effect gallery"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Photon.slnx` exits 0 with `EffectStackTests` (add, reorder, hide, delete, flatten, undo), `EffectStackRoundTripTests` (reopen restores the live stack; Inkscape 1.4 sees the fallback image within tolerance), `EffectRenderCacheTests`, and `EffectStackBudgetTests` reporting, and a driven FX panel session is captured to `docs/captures/nodus/effects-panel/`. Cheaper substitute that fails: storing only the rasterized result, which the reopen-as-live test rejects.

## 3. Adjustments in Nodus: the Image Adjustment Lab and Adjustment Presets

Correcting a placed photo's tone and color should not need another app. This section puts every `D01 T03 §4` and `§5` adjustment on an Effects, Adjust submenu as entries of the §2 stack (so they stay non-destructive), adds the Image Adjustment Lab that composes the common corrections with a live histogram and snapshots, and adds multi-adjustment presets. The histogram control stays Nodus-local until Imago's `D03 T05 §2` needs it, then moves to `Photon.UI`. Catalog: NP-2009 to NP-2023 (15 features: adjustment presets, the Image Adjustment Lab with auto adjust, white and black point tools, temperature, tint, saturation, brightness and contrast, highlights, shadows and midtones, histogram, snapshots, undo, redo and reset to original, remember settings, and preview modes, and live preview of adjustments).

**Fidelity:** new build, no baseline; captured to `docs/captures/nodus/adjustments/` (Image Adjustment Lab, Levels, Tone Curve, and Hue/Saturation/Lightness dialogs).
**Job:** a designer can correct a photo's tone and color inside Nodus with before and after comparison. Consumer: the FX stack of §2.
**Treatment:** the Lab as one dialog with auto adjust, white and black point droppers, temperature, tint, saturation, brightness, contrast, highlights, shadows, and midtones, a live histogram, snapshots, and full, before and after, or split preview. Cheaper substitute that fails the checkpoint: sliders with no histogram and no preview.
**Chrome:** consume the shared theme, `Photon.UI` sliders and numeric boxes, the suite history, and the settings store. The histogram control stays Nodus-local until `D03 T05 §2` needs it; do not write a second adjustment evaluator beside the engine.

**Requires:** display-session -- the Lab and the adjustment dialogs need an interactive desktop

- [ ] Add the Effects, Adjust submenu with one command per engine adjustment (auto adjust, levels, equalize, sample and target, tone curve, light, gamma, white balance, color balance, hue saturation lightness, black and white, vibrance, selective color, replace colors, replace colors legacy, desaturate, channel mixer, invert, threshold). Done when: `MenuAuditTests` count one enabled item per adjustment.
- [ ] Generate each adjustment dialog from its schema through `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/AdjustmentDialog.xaml`, with hand-built views for Levels (histogram with input and output sliders) and Tone Curve. Done when: every adjustment opens a dialog in a driven run and the capture set is committed.
- [ ] Apply every committed adjustment as an entry in the §2 FX stack, never to the pixels. Done when: reopening an adjusted photo shows the adjustment live in the FX panel.
- [ ] Add a Live preview toggle that previews on the canvas or only in the dialog (CD-2290), remembered as `Nodus.Adjust.LivePreview`. Done when: toggling it off leaves the canvas render hash unchanged while a slider moves.
- [ ] Build the Tone Curve dialog: curve, straight, freehand, and gamma styles; a channel selector with an all-channels display; smooth, mirror, reset channel, and reset all; an eyedropper that places a node at the sampled level; import of Corel `.pst` presets through `D01 T03 §4`. Done when: `ToneCurveDialogViewModelTests` cover each command and the `.pst` fixture imports.
- [ ] Add `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/ImageAdjustmentLabDialog.xaml` with `ImageAdjustmentLabViewModel` whose controls map onto `D01 T03 §4` and `§5` adjustments composed into one ordered stack entry (CD-2258). Done when: `AdjustmentLabTests.CompositionMatchesEngine` asserts the Lab output equals the equivalent engine stack bit-exactly.
- [ ] Add Lab auto adjust and white point and black point droppers (CD-2259, CD-2260). Done when: clicking the white point on the gray card fixture's white patch sets it to 255 per channel in a test.
- [ ] Add Lab temperature, tint, and saturation (CD-2261, CD-2262, CD-2263). Done when: each slider changes the composed stack's matching parameter in a test.
- [ ] Add Lab brightness and contrast, and highlights, shadows, and midtones (CD-2264, CD-2265). Done when: each slider maps onto `Light` parameters in a test.
- [ ] Add the Lab histogram bound to `D01 T03 §4` `Histogram` recomputed on the preview buffer after each change (CD-2266), as the Nodus-local control `src/Nodus/Photon.Nodus.Desktop/Controls/HistogramView.xaml`. Done when: a test asserts the bound bins change after a brightness step and the capture shows the histogram.
- [ ] Add Lab snapshots: numbered thumbnails, click to compare (CD-2267). Done when: a driven run takes two snapshots and comparing one restores its settings in the preview.
- [ ] Add Lab dialog-local undo, redo, and reset to original, committed as one history entry on OK (CD-2268). Done when: three Lab edits, two undos, and OK leave exactly one history entry holding the first edit.
- [ ] Add Lab Remember settings stored as `Nodus.AdjustmentLab.Remembered` (CD-2269) and full, before and after, and split preview modes (CD-2270). Done when: remembered settings survive a restart and each preview mode is captured.
- [ ] Add adjustment presets (CD-2257): built-in Black and White, Color, and Tone groups plus user presets as `AdjustmentPreset` JSON under `%LOCALAPPDATA%\Rizonesoft\Nodus\presets\adjustments\`, applied from the FX panel with save, rename, delete, import, and export. Done when: `AdjustmentPresetStoreTests` round-trip a user preset and refuse an import that fails the schema by name.
- [ ] Log one Information line per committed adjustment or preset application. Done when: a Serilog test logger asserts the line.
- [ ] Update the Nodus user guide page `docs/user/nodus/adjustments.md`. Done when: the page documents every Lab control and preset command.
- [ ] Commit: `"nodus: image adjustments, the Adjustment Lab, and adjustment presets"`

**Test checkpoint:** Unit test plus driven run: `dotnet test Photon.slnx` exits 0 with `AdjustmentLabTests` (Lab composition equals the equivalent engine stack bit-exactly), `ToneCurveDialogViewModelTests`, and `AdjustmentPresetStoreTests` reporting, remembered settings persist across a restart (settings readback quoted), and a driven Lab session with split preview is captured to `docs/captures/nodus/adjustments/`. Cheaper substitute that fails: a Lab that applies destructively on OK, which the §2 reopen-as-live test rejects.

## 4. The Tracing Engine: Outline Tracing, Color Quantization, and Stacking

Tracing turns a logo, a sketch, or a photo into editable vectors, and it is the one bitmap feature both competitors treat as core. This section builds the engine in `Photon.Nodus.Core/Tracing/` (it stays Nodus-local: no second app traces): a port of potrace 1.16 for outline tracing, multi-color tracing over `D01 T03 §3` color reduction with abutting or stacked output, the fidelity and cleanup options both competitors expose, stroke output for thin regions, and trace statistics. Potrace is GPL-2.0-or-later, which the GPL-3.0 suite may combine; every ported file keeps its notice. Catalog: NP-2028 to NP-2041 (14 features: color mode, palette, paths, corners and noise, abutting or overlapping method, fills and strokes with maximum stroke width, snap curves to lines and ignore white, trace statistics, detail, smoothing, corner smoothness, remove background, group by color, merge adjacent, and number of colors).

**Fidelity:** no surface of its own (the Image Trace panel and the trace dialog are §5)

- [ ] Add `docs/dev/decisions.md` row "Tracing: port of potrace 1.16 (GPL-2.0-or-later, combinable with GPL-3.0) in `Photon.Nodus.Core/Tracing/Potrace/`, stays in Nodus until a second app traces", naming this section. Done when: the row exists with the license reasoning.
- [ ] Port potrace path decomposition (`Tracing/Potrace/PathDecomposer.cs`) with the turn policies and speckle suppression `turdsize`, each ported file carrying the GPL-2.0-or-later notice crediting Peter Selinger. Done when: `PotraceTests.Decompose` yields the same path count as the potrace 1.16 CLI on every black-and-white fixture. Source: potrace 1.16 `decompose.c`.
- [ ] Port the optimal polygon and vertex adjustment (`Tracing/Potrace/PolygonOptimizer.cs`). Done when: vertex counts match potrace 1.16 on the fixtures. Source: potrace 1.16 `trace.c`.
- [ ] Port corner detection with `alphamax` and curve optimization with `opttolerance` (`Tracing/Potrace/CurveFitter.cs`). Done when: the traced output of every black-and-white fixture differs from the potrace 1.16 SVG by under 0.5 percent rasterized XOR area with a matching path count.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Tracing/TraceOptions.cs` (a record): mode (color, grayscale, black and white with threshold), palette (automatic, limited, full tone, document swatches), color count, paths, corners, noise, detail, smoothing, corner smoothness, method (abutting or overlapping), create fills, create strokes with maximum stroke width, snap curves to lines, ignore white, remove background (auto or sampled color, whole image), merge adjacent, and group by color (AI-0784 to AI-0788, AI-0791, CD-2042 to CD-2044, CD-2046 to CD-2049, CD-2051, CD-2052). Done when: the record serializes with a source-generated JSON context and round-trips.
- [ ] Map the Illustrator names (paths, corners, noise) and the Corel names (detail, smoothing, corner smoothness) onto potrace parameters through one documented table in `Tracing/ParameterMap.cs`. Done when: `ParameterMapTests` assert each slider's extremes map to the documented `turdsize`, `alphamax`, and `opttolerance` values.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Tracing/ColorTracer.cs`: quantize through `D01 T03 §3` `ColorReducer` with a seed, split per color, and trace each mask with the potrace port; document swatches mode maps to the nearest document swatch. Done when: a 16-color trace of the logo fixture yields at most 16 fill colors, identical across two runs with the same seed.
- [ ] Add overlapping mode (each color traced unioned with all lighter-ranked colors and stacked bottom up) and abutting mode (upper shapes subtracted so paths share edges) with `SKPath.Op`. Done when: `AbuttingGapTests` find no uncovered pixel between neighboring colors in either mode.
- [ ] Add stroke output: regions thinner than the maximum stroke width become centerline strokes through `Tracing/Skeleton/ZhangSuenSkeletonizer.cs`, which §5 reuses. Done when: a 3-pixel line fixture traces as one stroke of width 3 within 0.5.
- [ ] Add post-processing in `Tracing/PostProcess.cs`: snap near-straight Beziers to lines within tolerance, ignore white, remove the background (auto or sampled color), merge adjacent same-color paths with `SKPath.Op` union, and group by color. Done when: `PostProcessTests` assert each option changes the output as named.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Tracing/TraceResult.cs`: paths, anchor count, color count, elapsed time, and `Estimate(options, image)` for the time estimate and statistics report §5 shows before and after tracing (AI-0792). Done when: statistics on the logo fixture equal the counted output and the estimate is within a factor of two of the measured time.
- [ ] Observe cancellation per color layer and report progress. Done when: cancelling a 64-color trace of the 24-megapixel photo fixture stops within one layer.
- [ ] Add budget tests: a 2-megapixel logo at 16 colors under 2 seconds and a 24-megapixel photo at 64 colors cancellable with progress. Done when: `TraceBudgetTests` quote the times.
- [ ] Commit goldens under `tests/fixtures/nodus/trace/`: potrace 1.16 CLI SVGs for the black-and-white fixtures and Inkscape 1.4 Trace Bitmap multiscan colors SVGs for the color fixtures, each with `reference.txt` naming the version and exact command. Done when: every fixture has its golden and `reference.txt`.
- [ ] Commit: `"nodus: the tracing engine with a potrace port and color stacking"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx` exits 0 with `PotraceTests` and `TracerTests` comparing against the potrace 1.16 and Inkscape 1.4 goldens in `tests/fixtures/nodus/trace/` (rasterized XOR area under 0.5 percent and matching path counts for black and white; color counts and XOR area quoted for color), `AbuttingGapTests` finding no uncovered pixel, and `TraceBudgetTests` quoting times. Cheaper substitute that fails: marching-squares polygons with no curve fitting, which the anchor-count and XOR goldens reject.

## 5. Centerline Tracing, the Image Trace Panel, and PowerTRACE

Tracing only earns its place when a designer can choose a preset, preview it, fix the colors, and change their mind later. This section adds centerline tracing on the §4 skeletonizer, shape and gradient detection, a live trace object that keeps its source and options, the Image Trace panel (Illustrator's workflow) and the trace dialog with Quick, Outline, and Centerline Trace (Corel's workflow), both on one engine and one preset store. It fits 30 items by grouping presets as data files and color operations as one item; if it overflows at build time the natural split is centerline plus the live trace object versus the trace dialog. Catalog: NP-2042 to NP-2075 (34 features: lettering trace, the Image Trace panel, make and expand and release, one-click and classic presets, preview and view modes, gradient and shape detection, preset management, editing trace results, quick trace, centerline trace and its two presets, outline trace and its six presets, the trace dialog with its pages, zoom, pan, and fit, type switching, result details and time estimate, delete or keep the original, dialog undo, redo, and reset, color sorting, selecting, editing, merging, deleting, and palette open and save, pre-trace adjustments, and trace defaults).

**Fidelity:** new build, no baseline; captured to `docs/captures/nodus/trace/` (Image Trace panel, the trace dialog in each preview mode, the Bitmaps, Trace submenu).
**Job:** a designer can turn a logo, sketch, or photo into editable vectors with presets, preview, and color control, and change the settings later on a live trace. Consumer: the document (paths or a live trace object).
**Treatment:** a live trace object with Make, Make and Expand, Release, and Expand; a dialog with before and after, large preview, wireframe overlay, zoom, pan, fit, and a Colors page. Cheaper substitute that fails the checkpoint: a one-shot trace with no preview and no live object.
**Chrome:** consume the shared theme and icon catalog, the suite history, the settings store, the swatch and palette file readers and writers from `D02 T09 §4`, and Live Paint from `D02 T11 §17`. Do not write a second palette reader.

**Requires:** display-session -- the panel, the dialog, and its preview modes need an interactive desktop

- [ ] Add `src/Nodus/Photon.Nodus.Core/Tracing/CenterlineTracer.cs`: skeletonize with the §4 `ZhangSuenSkeletonizer`, prune spurs shorter than a threshold, walk skeleton graphs into open and closed polylines, and fit Beziers (CD-2025). Done when: `CenterlineTests` match the Inkscape 1.4 centerline goldens under `tests/fixtures/nodus/trace/centerline/` within 0.5 percent rasterized XOR area of the stroked result.
- [ ] Add shape detection (circles, ellipses, and rectangles become live shapes from `D02 T08 §4`) and gradient detection (linear gradients with a smoothness slider) as `TraceOptions` flags (AI-0790, AI-0789). Done when: a traced circle fixture yields one live ellipse and a gradient fixture yields one linear gradient fill.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Models/Elements/LiveTraceElement.cs`: a source image reference plus `TraceOptions`, persisted as `nodus:trace` parameters with the traced paths as the plain-SVG fallback per `D02 T07 §1`. Done when: `LiveTraceTests.Reopen` restores the live trace with its options and an external reader sees the paths.
- [ ] Add Make, Make and Expand, Release (restores the image), and Expand commands, each undoable, and Expand then Live Paint through `D02 T11 §17` (AI-0780, AI-0794). Done when: Release restores the original image bytes by SHA-256 and undo reverses each command.
- [ ] Add the Image Trace panel (`Views/Panels/ImageTracePanel.xaml`) with one-click preset buttons (auto color, high color, low color, grayscale, black and white, outline), the preset list, mode, palette, colors, and an Advanced expander over every `TraceOptions` field (AI-0779, AI-0781). Done when: a driven run traces the logo fixture from each one-click button and the captures are committed. Cheaper substitute: a preset list with no advanced options.
- [ ] Add panel view modes (tracing result, with outlines, outlines, outlines with source, source image) and statistics (paths, anchors, colors) (AI-0783, AI-0792). Done when: each view mode is captured on the logo fixture.
- [ ] Add trace presets as JSON under `%LOCALAPPDATA%\Rizonesoft\Nodus\presets\trace\` with save, rename, delete, import, and export (AI-0793). Done when: `TracePresetStoreTests` round-trip a user preset and refuse an import that fails the schema by name.
- [ ] Commit the built-in presets as data files under `src/Nodus/Photon.Nodus.Core/Tracing/Presets/`: the Illustrator one-click set and classic list, the Corel outline presets (line art, logo, detailed logo, clipart, low quality image, high quality image), the centerline presets (technical illustration, line drawing), and a Lettering preset (AI-0782, CD-2029 to CD-2034, CD-2026, CD-2027). Done when: `TracePresetSnapshotTests` trace a fixed fixture with every preset and match a committed snapshot per preset, and no two presets produce identical output.
- [ ] Make the Lettering preset trace text images into outlines grouped per connected glyph (AI-0423). Done when: the lettering fixture yields one group per glyph.
- [ ] Add the trace dialog (`Views/Dialogs/TraceDialog.xaml`) with Settings, Colors, and Adjustments pages, and before and after, large preview, and wireframe overlay with an opacity slider (CD-2035, CD-2036, CD-2037, CD-2038). Done when: each preview mode is captured on the photo fixture.
- [ ] Add dialog zoom, pan, and fit (CD-2039), trace type and image type switchers (CD-2040), and object, node, and color counts with the §4 time estimate (CD-2041). Done when: switching image type re-runs the preview and the counts update in a driven run.
- [ ] Add Delete original image (off by default) (CD-2045) and dialog undo, redo, and reset (CD-2050). Done when: reset restores the preset's settings and delete original removes the image in one undoable command.
- [ ] Build the Colors page: sort by similarity or frequency, select by swatch or eyedropper, edit color through the Nodus color picker, merge (average or first selected, from the trace defaults), delete (replaced by the next color), and open and save the palette through the `D02 T09 §4` palette readers and writers (CD-2053 to CD-2057). Done when: `TraceColorsViewModelTests` cover each operation and a palette saved from the page reopens in the Swatches panel.
- [ ] Build the Adjustments page: classical pre-trace brightness, contrast, blur, and JPEG artifact removal from `D01 T03 §4` and `D01 T03 §6`, with AI upsampling shown disabled with the tooltip `Planned: D02 T15 §9` (CD-2058). Done when: a blur on the page changes the preview and `MenuAuditTests` finds the disabled item with a resolving tooltip.
- [ ] Add the Bitmaps, Trace submenu: Quick Trace (method from `Nodus.Trace.QuickMethod`), the Outline Trace submenu with its six presets, and the Centerline Trace submenu with its two presets (CD-2024, CD-2072, CD-2028, CD-2090, CD-2091, CD-2084 to CD-2089). Done when: each item opens the dialog on its preset, and Quick Trace traces with no dialog.
- [ ] Add a Trace preferences page with the quick trace method and merge colors behavior (CD-2889), consumed by Quick Trace and the Colors page. Done when: changing the quick method changes Quick Trace's output in a test.
- [ ] Log one Information line per trace (preset, colors, paths, elapsed) and per live trace command. Done when: a Serilog test logger asserts the lines.
- [ ] Update the Nodus user guide page `docs/user/nodus/tracing.md`. Done when: the page documents the panel, the dialog, every preset, and every command.
- [ ] Commit: `"nodus: centerline tracing, live traces, the Image Trace panel, and the trace dialog"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Photon.slnx` exits 0 with `LiveTraceTests` (reopen restores options; Release restores the image by SHA-256), `CenterlineTests` against the Inkscape 1.4 centerline goldens, `TracePresetSnapshotTests` (one snapshot per preset, all distinct), `TracePresetStoreTests`, and `TraceColorsViewModelTests` reporting, and a driven session traces the logo fixture in each preview mode with captures under `docs/captures/nodus/trace/`. Cheaper substitute that fails: presets that only change the color count, which the per-preset distinct-snapshot test rejects.

## 6. Photo Artwork: Pointillizer, PhotoCocktail, Object Mosaic, and Mockups

Both competitors turn photos into artwork: CorelDRAW's Pointillizer (vector mosaics) and PhotoCocktail (a mosaic of other photos), and Illustrator's Object Mosaic and mockups (art placed onto a product photo). This section builds all four in Nodus on the §1 bitmap object and the `D02 T11 §5` envelope mesh, with local templates only: there is no cloud template library and no automatic surface detection, a recorded scope decision. Catalog: NP-1784 to NP-1806 (23 features: Object Mosaic, create mockup, local mockup templates, edit mockup content and release, the Pointillizer panel with density, scale, screen angle, keep original, limit colors, tracking methods, merge adjacent, weld overlap, and tile shape, and the PhotoCocktail panel with its library folder, keep original, grid, blending, duplicates and spacing, composition, edges, and output priority).

**Fidelity:** new build, no baseline; captured to `docs/captures/nodus/mosaics/` (Pointillizer panel, PhotoCocktail panel, Object Mosaic dialog, Mockup panel).
**Job:** a designer can turn a photo into a vector mosaic or a mosaic of other photos, or place art onto a product photo. Consumer: the document.
**Treatment:** dockable panels with live counts and Apply, with Escape cancelling a running build. Cheaper substitute that fails the checkpoint: fixed-size square tiles only.
**Chrome:** consume the shared theme, the icon catalog, the suite history, the settings store, and the `D02 T11 §5` envelope mesh. Do not write a second mesh warp.

**Requires:** display-session -- the panels and on-canvas mockup editing need an interactive desktop

- [ ] Add `src/Nodus/Photon.Nodus.Core/Mosaic/Pointillizer.cs` with density (tiles per square inch), scale, screen angle, limit colors through `D01 T03 §3`, and keep original, working on bitmaps and on rasterized vector selections (CD-2227 to CD-2231). Done when: `MosaicTests.PointillizerDensity` asserts tile counts for two densities within 2 percent of the expected value.
- [ ] Add the Pointillizer tracking methods (uniform with white matte, size by opacity, size by luminosity) (CD-2232, CD-2233, CD-2234). Done when: a size-distribution test shows tile sizes correlate with luminosity above 0.9 in luminosity mode and are equal in uniform mode.
- [ ] Add Pointillizer merge adjacent up to N and weld overlapping tiles into clusters (CD-2235, CD-2236). Done when: both options reduce the tile count on the fixture, asserted in a test.
- [ ] Add Pointillizer tile shapes: circle, square, preset shapes, or a selected closed path (CD-2237). Done when: a selected star path produces star tiles.
- [ ] Add the Pointillizer panel (`Views/Panels/PointillizerPanel.xaml`) with a live tile count, Apply, and Escape to cancel; the output is a group of real paths with one fill each, created in one undoable command (CD-2226, CD-2248, CD-2255). Done when: a driven run builds a mosaic, the capture shows the count, and undo removes the group.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Mosaic/PhotoCocktailIndex.cs`: index a folder of images (average Lab color and a small thumbnail per image) cached as JSON under `%LOCALAPPDATA%\Rizonesoft\Nodus\photococktail\` (CD-2239). Done when: indexing the fixture folder writes one entry per image and a second run reuses the cache.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Mosaic/PhotoCocktail.cs`: grid columns with auto rows, blending percentage, duplicates with minimum spacing, composition (single bitmap, bitmap stack, bitmap array), edges (remove partial or stretch), output priority (document dpi, custom dpi, tile size, output size), and keep original (CD-2240 to CD-2246). Done when: `MosaicTests.PhotoCocktailNearest` asserts each cell picks the nearest-color tile and the spacing rule holds.
- [ ] Add the PhotoCocktail panel (`Views/Panels/PhotoCocktailPanel.xaml`) with the library browser; a folder it cannot read is refused by name; single-bitmap output renders through the engine with progress and cancel (CD-2238, CD-2247, CD-2256). Done when: a driven run builds a mosaic from the fixture folder and a read-denied folder shows the refusal message.
- [ ] Add Object, Create Object Mosaic (`Views/Dialogs/ObjectMosaicDialog.xaml`): tile count or size, spacing, color or gray, resize by percent, and delete raster, outputting grouped rectangles (AI-0209). Done when: a 10 by 10 mosaic of the fixture yields 100 rectangles with the averaged colors.
- [ ] Add `src/Nodus/Photon.Nodus.Core/Models/Elements/MockupElement.cs`: art, a target photo, and a user-fitted envelope mesh from `D02 T11 §5`, with shading from the photo's luminance (AI-0953). Done when: `MosaicTests.MockupShading` asserts shaded art is darker where the photo is darker.
- [ ] Add the Mockup panel (`Views/Panels/MockupPanel.xaml`) with Edit Content, Edit Mockup, and Release (AI-0955). Done when: Release returns the original art unchanged and undo reverses it.
- [ ] Save and preview mockups as local templates under `%LOCALAPPDATA%\Rizonesoft\Nodus\mockups\`, recording in `docs/dev/decisions.md` that there is no cloud template library and no automatic surface detection (AI-0954, AI-0956). Done when: a saved template reapplies to new art and the decision row exists.
- [ ] Persist Pointillizer and Object Mosaic output as plain SVG, and mockups as `nodus:mockup` parameters with the warped, shaded art as the fallback. Done when: `MockupRoundTripTests` reopen a mockup live and an external reader sees the fallback.
- [ ] Add a budget test: a 20,000-tile Pointillizer build under 5 seconds with progress. Done when: `MosaicBudgetTests` quote the time.
- [ ] Log one Information line per mosaic or mockup command. Done when: a Serilog test logger asserts the lines.
- [ ] Update the Nodus user guide page `docs/user/nodus/photo-artwork.md`. Done when: the page documents every panel control.
- [ ] Commit: `"nodus: Pointillizer, PhotoCocktail, Object Mosaic, and mockups"`

**Test checkpoint:** Unit test plus driven run: `dotnet test Photon.slnx` exits 0 with `MosaicTests` (tile counts for density and scale, merge and weld reduce counts, the tracking-method size distribution, PhotoCocktail picks the nearest-color tile, mockup shading), `MockupRoundTripTests`, and `MosaicBudgetTests` reporting, and a driven session is captured to `docs/captures/nodus/mosaics/`. Cheaper substitute that fails: a Pointillizer that ignores the tracking method, which the size-distribution test rejects.

## 7. The Links Panel and Linked Sources

Linked images are how large documents stay small, and a moved folder is how they break. This section adds one `LinkManager` that resolves, watches, and reports every linked source, and a Links panel that finds missing and modified files and fixes them: relink, update, embed, unembed, and placement options, with the update policy as a setting. It also adds Edit Original and Edit Bitmap in Imago, which launches Imago only when it is installed and says so by name when it is not. Catalog: NP-1807 to NP-1823 (17 features: the Links panel, relink, update link, and go to link, relink all instances, auto relink from the same folder, edit original, embed, unembed, and break link, link file info, placement options, filters and sort, the update links preference, the low-resolution EPS proxy, edit original with the system default app, the linked symbol libraries view, the Sources panel, linked documents and tables as sources, place or import as linked, and edit bitmap in Imago).

**Fidelity:** new build, no baseline; captured to `docs/captures/nodus/links/` (Links panel, Link File Info, Placement Options, Sources view).
**Job:** a designer can see every linked file, fix missing ones, update modified ones, and embed or unembed them. Consumer: the document and its SVG `href` values.
**Treatment:** a list with status badges (missing, modified, embedded), filters and sort, and prompts per the update policy. Cheaper substitute that fails the checkpoint: a static list with no status and no relink.
**Chrome:** consume the shared theme, the icon catalog, the suite history, the settings store, and the file dialogs File, Place uses. Do not add a second file watcher service.

**Requires:** display-session -- the panel, the relink dialogs, and Edit Original launches need an interactive desktop

- [ ] Add `src/Nodus/Photon.Nodus.Core/Links/LinkManager.cs`: enumerate linked `SvgImage` elements and other linked sources, resolve relative and absolute paths against the document folder, and report each link's state (ok, missing, modified, embedded). Done when: `LinkManagerTests` report each state for fixtures in a temp folder.
- [ ] Watch linked folders with one `FileSystemWatcher` per folder inside `LinkManager`, raising modified and missing events on the UI dispatcher. Done when: a test touches a linked file and receives one modified event within 2 seconds.
- [ ] Persist links with `href` relative when possible, and store `nodus:link` with the original absolute path, size, and modified time for relink heuristics. Done when: `LinkManagerTests.MovedFolder` opens a document whose folder moved with its images and resolves every link.
- [ ] Add the Links panel (`Views/Panels/LinksPanel.xaml`) with status badges, filters (missing, modified, embedded), and sort by name, status, or type (AI-0933, CD-1748, AI-0941). Done when: a driven run with a missing and a modified link shows both badges and the missing filter lists only the missing one. Cheaper substitute: a list with no badges.
- [ ] Add Relink (a file dialog), Update Link, and Go To Link (selects and scrolls to the element) (AI-0934, CD-2487), each one undoable command. Done when: tests relink a missing image and undo restores the old `href`.
- [ ] Add Relink all instances (on by default) and Auto relink other missing files found in the same folder (AI-0935, AI-0936). Done when: relinking one of three missing images from a folder that holds all three fixes all three in one command.
- [ ] Add Link File Info (name, format, color space, location, ppi, dimensions, scale, rotation, modified date) (AI-0939). Done when: the dialog's values for the photo fixture match its file header in a test.
- [ ] Add Placement Options for relink (preserve transforms, bounds, fit, fill, center, clip to bounding box) (AI-0940). Done when: each option's resulting bounds are asserted in `PlacementOptionsTests`.
- [ ] Add Embed (reads bytes into a data URI) and Unembed (writes PNG or TIFF through the §1 codec beside the document and relinks), and Break link for linked Nodus sources, each undoable (AI-0938, CD-2488). Done when: `LinkManagerTests.EmbedUnembedRoundTrip` restores identical pixels.
- [ ] Refuse by name a relink or unembed into a read-only or locked folder, or of a missing or locked file, with the permission problem named in the message. Done when: `LinkManagerTests.ReadOnlyRefusal` asserts the message and no state change.
- [ ] Add the update links policy `Nodus.Links.UpdateMode` (Automatic, Manual, AskWhenModified), consumed by `LinkManager` when the window activates; in AskWhenModified mode Nodus will notify the user with an alert that lists the modified links (AI-0942, AI-1178). Done when: tests cover each mode's behavior on a modified link.
- [ ] Add the low-resolution proxy setting for linked EPS `Nodus.Links.EpsLowResProxy`, read by the EPS placement `D02 T14 §9` adds (AI-1176). Done when: the setting appears on the Links preferences page and a test asserts `LinkManager` exposes it to placement code.
- [ ] Add Edit Original (Edit menu and panel) launching the file with the system default app or a chosen app from `Nodus.Links.EditOriginalApp`, and updating on save through the watcher (AI-0937, AI-1103, AI-1179, CD-2486). Done when: a driven run edits a linked PNG in the default app, saves, and the canvas updates (log line quoted).
- [ ] Add Edit Bitmap in Imago: locate `Imago.exe` through the `App Paths` registry key, launch it with the path (single-instance forwarding per `D01 T02 §3` hands it to a running Imago), and update on save; when Imago is not installed the command is disabled with the tooltip "Imago is not installed" (CD-2073). Done when: a test with a fake registry shows the disabled state and a driven run with Imago installed opens the bitmap in Imago.
- [ ] Add a Link option to File, Place and File, Import (CD-1967, CD-2463, CD-2473, CD-2485). Done when: placing with Link on writes an `href` and no `EmbeddedData`.
- [ ] Add the Sources view (a tab of the Links panel) listing linked Nodus SVG documents and CSV tables (`D02 T10 §14`) with attribution; CDR and XLS sources appear disabled with the tooltips `Planned: D02 T14 §6` and `Planned: D02 T14 §14`; linked symbol libraries from `D02 T09 §21` show as a filter (CD-580, CD-2484, CD-1686, CD-263). Done when: `MenuAuditTests` resolve both tooltips and a linked SVG document appears in the view.
- [ ] Add a budget test: a document with 500 linked images opens and reports every status without blocking the UI thread. Done when: `LinkBudgetTests` quote the time and a UI-responsiveness probe stays under 100 ms.
- [ ] Log one Information line per link command and per detected missing or modified file. Done when: a Serilog test logger asserts the lines.
- [ ] Update the Nodus user guide page `docs/user/nodus/links.md`. Done when: the page documents every panel control and policy.
- [ ] Commit: `"nodus: the Links panel, link manager, and linked sources"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Photon.slnx` exits 0 with `LinkManagerTests` (missing and modified detection in a temp folder, `MovedFolder`, relink all instances, `EmbedUnembedRoundTrip` with identical pixels, `ReadOnlyRefusal`), `PlacementOptionsTests`, and `LinkBudgetTests` reporting, and a driven session fixes a missing link by auto relink with captures under `docs/captures/nodus/links/`. Cheaper substitute that fails: absolute `href` values only, which the moved-folder test rejects.

## 8. SVG Filter Effects

SVG filters are the one kind of effect that survives in a browser, so web designers need them to stay live `<filter>` elements rather than rasterized pixels. This section reads every SVG 1.1 filter primitive, renders it through SkiaSharp image filters where exact and through `D01 T03` kernels where not, writes it back unchanged, and adds Apply SVG Filter, built-in presets of Nodus's own, import, and a code editor. Catalog: NP-2024 to NP-2026 (3 features: apply SVG filter, import SVG filters and edit filter code, and built-in SVG filter presets).

**Fidelity:** new build, no baseline; captured to `docs/captures/nodus/svg-filters/` (Apply SVG Filter dialog and the filter code editor).
**Job:** a web designer can apply and edit standard SVG filters that survive in browsers. Consumer: the renderer, the SVG writer, and browsers reading the output.
**Treatment:** filters stay live `<filter>` elements in the SVG, never rasterized. Cheaper substitute that fails the checkpoint: rasterizing the filter into an image on save.
**Chrome:** consume the §2 FX stack entry type, the shared theme, and the raw SVG editor pattern of `RawSvgDialog`. Do not write a second XML editor.

**Requires:** display-session -- the dialog and the code editor need an interactive desktop

- [ ] Add `src/Nodus/Photon.Nodus.Core/Models/Filters/` types for `<filter>` (with `filterUnits`, `primitiveUnits`, and region) and every SVG 1.1 primitive (feGaussianBlur, feOffset, feBlend, feColorMatrix, feComponentTransfer, feComposite, feConvolveMatrix, feDiffuseLighting, feSpecularLighting, feDisplacementMap, feFlood, feImage, feMerge, feMorphology, feTile, feTurbulence). Done when: each type has a unit test constructing it from its attributes. Source: SVG 1.1 chapter 15.
- [ ] Teach `SvgParser` to read `<filter>` in `<defs>` and `filter="url(#id)"` on elements into those types, preserving unknown primitives verbatim. Done when: `SvgFilterTests.ReadAllPrimitives` parses the fixture holding every primitive and an unknown one survives a round trip byte-equal after normalization.
- [ ] Add `src/Nodus/Photon.Nodus.Desktop/Rendering/SvgFilterRenderer.cs` evaluating the primitive graph with SkiaSharp image filters where exact (`SKImageFilter.CreateBlur`, `CreateColorFilter`, `CreateDisplacementMapEffect`, `CreateMerge`, `CreateOffset`) and through `D01 T03` kernels otherwise, honoring the units and the filter region. Done when: each fixture renders within 1 percent of pixels at more than 8 of 255 difference from its Inkscape 1.4 golden.
- [ ] Teach `SvgExporter` to write `<filter>` definitions back unchanged in `<defs>` and keep `filter="url(#id)"` on the element. Done when: `SvgFilterTests.RoundTrip` compares every fixture element by element after save and reopen.
- [ ] Represent an applied SVG filter as an FX stack entry of type `svg-filter` in §2 so it shows in the FX panel with its eye toggle and delete. Done when: hiding the entry removes the `filter` attribute from the render but keeps the definition.
- [ ] Add Effect, SVG Filters, Apply SVG Filter (`Views/Dialogs/ApplySvgFilterDialog.xaml`) listing built-in presets and document filters with a preview (AI-0701). Done when: a driven run applies the drop shadow preset and the capture shows the preview.
- [ ] Ship Nodus's own built-in presets as SVG files under `src/Nodus/Photon.Nodus.Core/Filters/Presets/` (blur, drop shadow, bevel, dilate, erode, turbulence, woodgrain, and similar), with no Adobe preset names copied (AI-0703). Done when: a test finds no preset id beginning with `AI_` and every preset renders against its golden.
- [ ] Add Import SVG Filter, reading `<filter>` definitions from any SVG file into the document (AI-0702). Done when: importing from the fixture adds its filters without duplicating ids.
- [ ] Add New and Edit filter code opening the `RawSvgDialog` editor pattern with XML validation that refuses a malformed filter by line and column (AI-0702). Done when: a test submits malformed XML and asserts the refusal message.
- [ ] Commit fixtures under `tests/fixtures/nodus/svg/filters/` with goldens rendered by Inkscape 1.4 and Chromium (versions and commands in `reference.txt`). Done when: every primitive has a fixture and both goldens.
- [ ] Log one Information line per applied, imported, or edited filter. Done when: a Serilog test logger asserts the lines.
- [ ] Update the Nodus user guide page `docs/user/nodus/svg-filters.md`. Done when: the page documents the dialog, presets, import, and editor.
- [ ] Commit: `"nodus: live SVG filter effects with presets, import, and a code editor"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx` exits 0 with `SvgFilterTests` rendering each fixture in `tests/fixtures/nodus/svg/filters/` against its Inkscape 1.4 golden within the stated tolerance and round-tripping it element by element; a driven apply of a preset is captured to `docs/captures/nodus/svg-filters/`. Cheaper substitute that fails: dropping `<filter>` on save, which the round-trip test rejects.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every `tests/Photon.Nodus.Tests/Bitmaps/`, `Effects/`, `Tracing/`, `Mosaic/`, `Links/`, and `Svg/SvgFilterTests` class reporting
- [ ] Every fixture under `tests/fixtures/nodus/trace/` and `tests/fixtures/nodus/svg/filters/` carries `reference.txt` naming its oracle (potrace 1.16, Inkscape 1.4, Chromium) and version
- [ ] Every ported potrace file under `src/Nodus/Photon.Nodus.Core/Tracing/Potrace/` carries the GPL-2.0-or-later notice, and `docs/dev/decisions.md` records the port
- [ ] Every disabled control on this file's surfaces names a section that `python scripts/todo-graph.py resolve` resolves (`D01 T04 §3`, `D02 T15 §9`, `D02 T14 §6`, `D02 T14 §14`)
- [ ] Captures under `docs/captures/nodus/bitmaps/`, `effects-panel/`, `adjustments/`, `trace/`, `mosaics/`, `links/`, and `svg-filters/` are committed, and the matching `docs/user/nodus/` pages exist
- [ ] `python scripts/todo-graph.py validate` clean
