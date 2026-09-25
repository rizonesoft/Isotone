---
schema_version: 1
id: imago-adjustments
domain: 03-imago
status: draft
title: "TODO-05 -- Imago Filters and Adjustments for 0.1.0"
depends_on: []
track: I5
---

# TODO-05 -- Imago Filters and Adjustments for 0.1.0

> **Goal:** Imago's Filter and Image, Adjustments menus run real operations: one filter pipeline with live preview, cancellation, and progress; the core tonal and color adjustments (brightness and contrast, levels, curves, hue and saturation); and the blurs and sharpening every photo needs, each proven against reference output and each one undo step.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `MainWindowViewModel` has `GaussianBlur`, `MotionBlur`, `SurfaceBlur`, `UnsharpMask`, `SmartSharpen`, `AddNoise`, and `ReduceNoise` commands whose bodies log "Opening ... dialog" and do nothing. `Imago.Plugins.Abstractions` defines `IFilterPlugin` and `IPlugin`, which nothing implements or loads. `Imago.Core/Layers/AdjustmentLayer.cs` exists as a model type. The legacy roadmap's filter phase (5, 64 items) is entirely open.
<!-- claim: count "_logger\.Information\(\"Opening (Gaussian|Motion|Surface|Unsharp|Smart|Add Noise|Reduce Noise)" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 7 -->
<!-- claim: exists src/Imago/src/Imago.Plugins.Abstractions/IFilterPlugin.cs -->

## Inputs

- [`standards/imago.md`](../../standards/imago.md) -- hot-path rules, GPU parity, fidelity tolerances
- [`docs/legacy/imago-roadmap.md`](../../docs/legacy/imago-roadmap.md) -- phase 5 (filters and effects), the source of this file
- libvips (https://www.libvips.org/) and GIMP -- the reference implementations for goldens, versions recorded beside them
- -> XREF: D03 T03 §2 -- the tile-snapshot history every filter commits through

## Outcome

- A filter runs through one pipeline: a dialog with parameters and a live preview on the canvas, progress in the status strip, Cancel that leaves the layer untouched, and one undo step on OK; filters respect the selection.
- Brightness and contrast, levels, curves, and hue and saturation work as destructive adjustments with histogram display where the competitor shows one.
- Gaussian blur, box blur, and unsharp mask match reference goldens within stated tolerances; the remaining filter menu items are disabled with tooltips naming their roadmap section.
- The filter pipeline is the internal contract `IFilterPlugin` will expose to plugins later.

**Adjacency:** list=not-applicable (no browsable records); document=not-applicable (no printed output); settings=applicable @ D03 T05 §1; reporting=applicable; notifications=applicable; permissions=not-applicable (no files written); audit=applicable; exchange=not-applicable (no formats); reverse=applicable @ D03 T05 §1

**Adjacency rationale:** Last-used filter parameters persist as settings; the levels and curves histograms are the reporting surface; progress and completion show in the status strip; every applied filter logs and undoes.

## Implementation Order

| Order | Section | Deliverable                                  | Depends On       | Status |
| :---: | :-----: | -------------------------------------------- | ---------------- | :----: |
|   1   |   §1    | The filter pipeline                          | D03 T03 §2, D03 T03 §5 |  [ ]   |
|   2   |   §2    | Core adjustments                             | §1               |  [ ]   |
|   3   |   §3    | Blur and sharpen                             | §1               |  [ ]   |

---

## 1. The Filter Pipeline

Every filter shares the same needs: parameters, a preview that updates as sliders move without blocking the UI, progress and cancellation on large images, selection masking, and one undo step. Building these once is what keeps sixty legacy filters from becoming sixty dialogs with sixty bugs. -> SOURCE: legacy-imago-5

**Fidelity:** Filter dialog frame -- new build, no baseline; captured to docs/captures/imago/filter-dialog/.
**Job:** a user can adjust a filter's parameters while watching the result on the canvas, then apply or cancel it. Consumer: every filter and adjustment.
**Treatment:** `IImageFilter` (parameters record, `Apply(TileRegion, CancellationToken, IProgress)`), a generic dialog frame hosting a filter's parameter view with Preview toggle, OK, Cancel, and Reset; preview renders the visible region at screen resolution first, then refines; Apply runs per tile in parallel with progress and commits through `TileSnapshotCommand`, masked by the selection with its feathering. Cheaper substitute that fails the checkpoint: a modal filter that blocks the UI thread with no preview.
**Chrome:** consume the tile store, the history, the status strip, and the theme. Do not build a dialog per filter from scratch.

**Requires:** display-session -- the preview and cancel drive needs an interactive desktop

- [ ] `IImageFilter`, `FilterRunner` (parallel per tile, cancellation, progress), and selection masking in `Photon.Imago.Core/Filters/`. Done when: `FilterRunnerTests` prove cancellation leaves tiles unchanged and masking leaves unselected pixels unchanged.
- [ ] The dialog frame with preview. Done when: a test filter (invert) previews and applies in a driven run.
- [ ] Last-used parameters persisted per filter in settings; one log line per applied filter with its parameters. Done when: a test logger asserts the line.
- [ ] Commit: `"imago: one filter pipeline with preview, progress, and cancel"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `FilterRunnerTests` reporting; a driven invert on a 50-megapixel image shows progress and Cancel mid-run leaves the pixel hash unchanged (quoted). Cheaper substitute that fails: a blocking apply.

## 2. Core Adjustments

The adjustments every photo edit uses first. Destructive in 0.1.0 (adjustment layers are `D03 T07 §1`), each through the §1 pipeline. -> SOURCE: legacy-imago-5.1

**Fidelity:** Adjustment dialogs -- new build, no baseline; captured to docs/captures/imago/adjustments/.
**Job:** a user can correct brightness, contrast, levels, curves, and hue and saturation with a live histogram. Consumer: the active layer.
**Treatment:** Image, Adjustments, Brightness/Contrast, Levels (per channel, input and output points, auto), Curves (per channel, up to 16 points, monotone cubic), and Hue/Saturation (master and six ranges, colorize); a histogram control shared by Levels and Curves. Cheaper substitute that fails the checkpoint: a single brightness slider.
**Chrome:** consume the §1 dialog frame; build the histogram control in Imago (Lumen will need one; move it to `Photon.UI` through `add-todo` when Lumen's develop panel is authored).

**Requires:** display-session -- the adjustment dialogs need an interactive desktop

- [ ] The four adjustments as `IImageFilter`s operating in the document's bit depth, with lookup tables for 8-bit and computed curves for 16-bit. Done when: each has unit tests on known values (levels 0-255 to 50-205 maps 128 to 128 within 1).
- [ ] Goldens from GIMP (version recorded) for levels, curves, and hue/saturation on a fixture photo; fidelity tests within 2/255. Done when: each passes.
- [ ] The histogram control and the four dialogs, keyboard operable. Done when: captures committed.
- [ ] Commit: `"imago: brightness and contrast, levels, curves, and hue and saturation"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the adjustment goldens within 2/255; a driven curves edit and undo restores the pixel hash. Cheaper substitute that fails: 8-bit processing of 16-bit documents, which a 16-bit fixture catches.

## 3. Blur and Sharpen

Blur and sharpening are the most used filters after adjustments. Gaussian blur must be separable and fast at large radii; unsharp mask is the standard sharpener. The other items in the Filter menu are disabled with tooltips naming `D03 T07 §3`. -> SOURCE: legacy-imago-5.2-5.3

**Fidelity:** Blur and sharpen dialogs -- new build, no baseline; captured to docs/captures/imago/blur/.
**Job:** a user can blur and sharpen a layer or selection with a preview. Consumer: the active layer.
**Treatment:** Gaussian blur (radius 0.1 to 1,000 px; separable, with a box-filter approximation above radius 64), box blur, and unsharp mask (amount, radius, threshold); motion blur, surface blur, smart sharpen, add noise, and reduce noise disabled with `Planned: D03 T07 §3`. Cheaper substitute that fails the checkpoint: a 2D convolution that takes minutes at radius 100.
**Chrome:** consume the §1 pipeline and dialog frame.

**Requires:** display-session -- the filter dialogs need an interactive desktop

- [ ] Gaussian, box, and unsharp mask filters with SIMD inner loops and scalar references. Done when: SIMD and scalar outputs match exactly.
- [ ] Goldens from libvips (`vips gaussblur`, `vips sharpen`, version recorded) and fidelity tests within 2/255. Done when: each passes.
- [ ] Disable the remaining filter commands with planned tooltips. Done when: no filter command body only logs.
- [ ] Benchmark Gaussian radius 100 on a 24-megapixel image. Done when: under 1 second on the development machine (quoted).
- [ ] Commit: `"imago: Gaussian blur, box blur, and unsharp mask"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the blur and sharpen goldens; the benchmark is quoted under 1 second. Cheaper substitute that fails: naive convolution, which the benchmark catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] Every Filter and Adjustments menu item works or names its section
- [ ] `python scripts/todo-graph.py validate` clean
