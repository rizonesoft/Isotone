---
schema_version: 1
id: pinxit-adjustments
domain: 03-pinxit
status: draft
title: "TODO-05 -- Pinxit Filters and Adjustments for 0.1.0"
depends_on: []
track: I5
---

# TODO-05 -- Pinxit Filters and Adjustments for 0.1.0

> **Goal:** Pinxit's Filter and Image, Adjustments menus run real operations: one filter pipeline with live preview, cancellation, and progress; the core tonal and color adjustments (brightness and contrast, levels, curves, hue and saturation); and the blurs and sharpening every photo needs, each proven against reference output and each one undo step.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `MainWindowViewModel` has `GaussianBlur`, `MotionBlur`, `SurfaceBlur`, `UnsharpMask`, `SmartSharpen`, `AddNoise`, and `ReduceNoise` commands whose bodies log "Opening ... dialog" and do nothing. `Pinxit.Plugins.Abstractions` defines `IFilterPlugin` and `IPlugin`, which nothing implements or loads. `Pinxit.Core/Layers/AdjustmentLayer.cs` exists as a model type. The legacy roadmap's filter phase (5, 64 items) is entirely open.
<!-- claim: count "_logger\.Information\(\"Opening (Gaussian|Motion|Surface|Unsharp|Smart|Add Noise|Reduce Noise)" src/Pinxit/src/Pinxit.UI/ViewModels/MainWindowViewModel.cs = 7 -->
<!-- claim: exists src/Pinxit/src/Pinxit.Plugins.Abstractions/IFilterPlugin.cs -->

## Inputs

- [`standards/pinxit.md`](../../standards/pinxit.md) -- hot-path rules, GPU parity, fidelity tolerances
- [`docs/legacy/pinxit-roadmap.md`](../../docs/legacy/pinxit-roadmap.md) -- phase 5 (filters and effects), the source of this file
- libvips (https://www.libvips.org/) and GIMP -- the reference implementations for goldens, versions recorded beside them
- -> XREF: D03 T03 §2 -- the tile-snapshot history every filter commits through
- -> XREF: D01 T03 §1 -- the suite pixel engine §1's filter pipeline consumes instead of growing its own
- -> XREF: D02 T15 §9 -- the Stilus AI cleanup hand-off that targets §1's pipeline
- -> XREF: D03 T08 §11 -- Pinxit parity document and view cites §2: the histogram control D03 T08 §11 hosts
- -> XREF: D03 T10 §10 -- Pinxit parity selection and channels cites §1: the filter pipeline D03 T10 §10 runs on alpha channels and the dialog frame the dialogs there use
- -> XREF: D03 T11 §1 -- Pinxit parity adjustments and color cites §1: the filter pipeline and dialog frame the Properties pages grow from; §2: the Levels, Curves, and Hue/Saturation dialogs and the histogram control D03 T11 §1 to D03 T11 §3 grow into Properties pages
- -> XREF: D03 T14 §2 -- Pinxit parity filters cites §1: the filter pipeline and dialog frame D03 T14 §2 extends

## Outcome

- A filter runs through one pipeline: a dialog with parameters and a live preview on the canvas, progress in the status strip, Cancel that leaves the layer untouched, and one undo step on OK; filters respect the selection.
- Brightness and contrast, levels, curves, and hue and saturation work as destructive adjustments with histogram display where the competitor shows one.
- Gaussian blur, box blur, and unsharp mask match reference goldens within stated tolerances; the remaining filter menu items are disabled with tooltips naming their roadmap section.
- The filter pipeline is the internal contract `IFilterPlugin` will expose to plugins later.

**Adjacency:** list=not-applicable (no browsable records); document=not-applicable (no printed output); settings=applicable @ D03 T05 §1; reporting=applicable @ D03 T05 §2; notifications=applicable @ D03 T05 §1; permissions=not-applicable (no files written); audit=applicable @ D03 T05 §1; exchange=not-applicable (no formats); reverse=applicable @ D03 T05 §1

**Adjacency rationale:** Last-used filter parameters persist as settings; the levels and curves histograms are the reporting surface; progress and completion show in the status strip; every applied filter logs and undoes.

## Implementation Order

| Order | Section | Deliverable                                  | Depends On       | Status |
| :---: | :-----: | -------------------------------------------- | ---------------- | :----: |
|   1   |   §1    | The filter pipeline                          | D03 T03 §2, D03 T03 §5 |  [ ]   |
|   2   |   §2    | Core adjustments                             | §1               |  [ ]   |
|   3   |   §3    | Blur and sharpen                             | §1               |  [ ]   |

---

## 1. The Filter Pipeline

Every filter shares the same needs: parameters, a preview that updates as sliders move without blocking the UI, progress and cancellation on large images, selection masking, and one undo step. Building these once is what keeps sixty legacy filters from becoming sixty dialogs with sixty bugs. -> SOURCE: legacy-pinxit-5

**Fidelity:** Pinxit filter dialog frame with preview and progress -- docs/design/components/ (Dialog, Progress, Checkbox, Button, Canvas), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/filter-dialog/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Progress/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can adjust a filter's parameters while watching the result on the canvas, then apply or cancel it. Consumer: every filter and adjustment.
**Treatment:** `IImageFilter` (parameters record, `Apply(TileRegion, CancellationToken, IProgress)`), a generic dialog frame hosting a filter's parameter view with Preview toggle, OK, Cancel, and Reset; preview renders the visible region at screen resolution first, then refines; Apply runs per tile in parallel with progress and commits through `TileSnapshotCommand`, masked by the selection with its feathering. Cheaper substitute that fails the checkpoint: a modal filter that blocks the UI thread with no preview.
**Chrome:** consume the tile store, the history, the status strip, and the theme. Do not build a dialog per filter from scratch.

**Requires:** display-session -- the preview and cancel drive needs an interactive desktop

- [ ] `IImageFilter`, `FilterRunner` (parallel per tile, cancellation, progress), and selection masking in `Isotone.Pinxit.Core/Filters/`. Done when: `FilterRunnerTests` prove cancellation leaves tiles unchanged and masking leaves unselected pixels unchanged.
- [ ] The dialog frame with preview. Done when: a test filter (invert) previews and applies in a driven run.
- [ ] Last-used parameters persisted per filter in settings; one log line per applied filter with its parameters. Done when: a test logger asserts the line.
- [ ] Commit: `"pinxit: one filter pipeline with preview, progress, and cancel"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `FilterRunnerTests` reporting; a driven invert on a 50-megapixel image shows progress and Cancel mid-run leaves the pixel hash unchanged (quoted). Cheaper substitute that fails: a blocking apply.

## 2. Core Adjustments

The adjustments every photo edit uses first. Destructive in 0.1.0 (adjustment layers arrive in Phase 18 with `D03 T11 §1`), each through the §1 pipeline. **Corrected 2026-09-26:** said adjustment layers wait in the backlog as B-014; the Pinxit parity plan promoted B-014 into `D03 T11 §1`. -> SOURCE: legacy-pinxit-5.1

**Fidelity:** Pinxit adjustment dialogs with the histogram and curve editor -- docs/design/components/ (Dialog, Slider, NumberBox, ComboBox, Button), plus the new `docs/design/components/Histogram/` and `docs/design/components/CurveEditor/` specs this section writes first, per standards/design-contract.md; goldens under docs/captures/golden/pinxit/adjustments/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Button/README.md, new surface: docs/design/components/Histogram/README.md, new surface: docs/design/components/CurveEditor/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can correct brightness, contrast, levels, curves, and hue and saturation with a live histogram. Consumer: the active layer.
**Treatment:** Image, Adjustments, Brightness/Contrast, Levels (per channel, input and output points, auto), Curves (per channel, up to 16 points, monotone cubic), and Hue/Saturation (master and six ranges, colorize); a histogram control shared by Levels and Curves. Cheaper substitute that fails the checkpoint: a single brightness slider.
**Chrome:** consume the §1 dialog frame; build the histogram control in Pinxit (Albumen will need one; move it to `Isotone.UI` through `add-todo` when Albumen's develop panel is authored).

**Requires:** display-session -- the adjustment dialogs need an interactive desktop

- [ ] Write the design spec `docs/design/components/Histogram/README.md` and its `preview.html` card for the histogram control (per-channel display, clipping readouts): anatomy, every state, tokens, and sizes, with the design page regenerated by `python scripts/build-design-site.py`, before any XAML for it is written. Done when: the spec and its card exist and `python scripts/build-design-site.py --check` passes.
- [ ] Write the design spec `docs/design/components/CurveEditor/README.md` and its `preview.html` card for the curve editor (grid, points, channel curves, input and output fields): anatomy, every state, tokens, and sizes, with the design page regenerated by `python scripts/build-design-site.py`, before any XAML for it is written. Done when: the spec and its card exist and `python scripts/build-design-site.py --check` passes.
- [ ] The four adjustments as `IImageFilter`s operating in the document's bit depth, with lookup tables for 8-bit and computed curves for 16-bit. Done when: each has unit tests on known values (levels 0-255 to 50-205 maps 128 to 128 within 1).
- [ ] Goldens from GIMP (version recorded) for levels, curves, and hue/saturation on a fixture photo; fidelity tests within 2/255. Done when: each passes.
- [ ] The histogram control and the four dialogs, keyboard operable. Done when: captures committed.
- [ ] Commit: `"pinxit: brightness and contrast, levels, curves, and hue and saturation"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes the adjustment goldens within 2/255; a driven curves edit and undo restores the pixel hash. Cheaper substitute that fails: 8-bit processing of 16-bit documents, which a 16-bit fixture catches.

## 3. Blur and Sharpen

Blur and sharpening are the most used filters after adjustments. Gaussian blur must be separable and fast at large radii; unsharp mask is the standard sharpener. The other items in the Filter menu are disabled with tooltips naming `D03 T07 §3`. -> SOURCE: legacy-pinxit-5.2-5.3

**Fidelity:** Pinxit blur and sharpen dialogs -- docs/design/components/ (Dialog, Slider, NumberBox, ComboBox, Button), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/blur/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can blur and sharpen a layer or selection with a preview. Consumer: the active layer.
**Treatment:** Gaussian blur (radius 0.1 to 1,000 px; separable, with a box-filter approximation above radius 64), box blur, and unsharp mask (amount, radius, threshold); motion blur, surface blur, smart sharpen, add noise, and reduce noise disabled with `Planned: D03 T07 §3`. Cheaper substitute that fails the checkpoint: a 2D convolution that takes minutes at radius 100.
**Chrome:** consume the §1 pipeline and dialog frame.

**Requires:** display-session -- the filter dialogs need an interactive desktop

- [ ] Gaussian, box, and unsharp mask filters with SIMD inner loops and scalar references. Done when: SIMD and scalar outputs match exactly.
- [ ] Goldens from libvips (`vips gaussblur`, `vips sharpen`, version recorded) and fidelity tests within 2/255. Done when: each passes.
- [ ] Disable the remaining filter commands with planned tooltips. Done when: no filter command body only logs.
- [ ] Benchmark Gaussian radius 100 on a 24-megapixel image. Done when: under 1 second on the development machine (quoted).
- [ ] Commit: `"pinxit: Gaussian blur, box blur, and unsharp mask"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes the blur and sharpen goldens; the benchmark is quoted under 1 second. Cheaper substitute that fails: naive convolution, which the benchmark catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] Every Filter and Adjustments menu item works or names its section
- [ ] `python scripts/todo-graph.py validate` clean
