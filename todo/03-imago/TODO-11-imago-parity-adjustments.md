---
schema_version: 1
id: imago-parity-adjustments
domain: 03-imago
status: draft
title: "TODO-11 -- Imago Parity: Adjustment Layers, Adjustments, Image Modes, and Color"
depends_on: []
track: I11
---

# TODO-11 -- Imago Parity: Adjustment Layers, Adjustments, Image Modes, and Color

> **Goal:** Imago corrects tone and color like Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6: non-destructive adjustment layers with an Adjustments panel, a Properties page per kind, presets and Photoshop preset files, a targeted adjustment tool, and an adjustment brush; every tonal and color adjustment the three ship, from Levels and Curves extensions to color lookup with LUT files and OpenColorIO, gradient maps, match and replace color, and GIMP's Colors menu operations; image modes (bitmap, grayscale, duotone, indexed, RGB, CMYK, Lab, multichannel) and 8, 16, and 32-bit precision; channel operations (Apply Image, Calculations, decompose, compose); and the color panels, pickers, samplers, swatches, palettes, and color books. Imago code lives in `src/Imago/Photon.Imago.Core/Adjustments/`, `Color/`, and `Channels/` and `src/Imago/Photon.Imago.Desktop/Adjustments/` and `Color/`; every algorithm Imago adds joins the one `EffectRegistry` in `src/Photon.Core/Imaging/Adjust/`, palette files move to `src/Photon.Core/Color/Palettes/`, and everything consumes `D01 T03 §3` to `§5` and `§11`, `D01 T04 §1` to `§3`, and `D01 T05 §5` rather than growing a second curve, histogram, quantizer, or color conversion. No Adobe or Affinity preset, LUT, or color book is bundled; users import the files they own. This file promotes backlog B-014 (`legacy-imago-5.1-adjustment-layers`) into §1.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `src/Imago/src/Imago.Core/Layers/AdjustmentLayer.cs` is a 57-line model holding only an `AdjustmentType` enum of 16 kinds, with no parameters, mask, or rendering. `src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs` binds no Levels, Curves, or Hue/Saturation command; those dialogs arrive with `D03 T05 §2` (Imago 0.1.0), whose catalog rows IP-0669 to IP-0672 are `shipped-scope` there. The document `ColorSpace` enum (`src/Imago/src/Imago.Core/Documents/ColorSpace.cs`) lists RGB variants, CMYK, Lab, and grayscale but no indexed, bitmap, duotone, or multichannel mode, and `BitDepth` (`src/Imago/src/Imago.Core/Documents/BitDepth.cs`) has exactly 8, 16, and 32. Imago carries its own 342-line color converter (`src/Imago/src/Imago.Core/Colors/ColorConverter.cs`) with Lab and CMYK structs in `ColorModels.cs` that the suite engine (`D01 T04`) supersedes, so §7 and §9 convert through `Photon.Core` instead. There is no palette or swatch code anywhere in Imago, and `src/Photon.Core` does not exist yet to hold the moved palette readers. These paths are today's names; `D03 T01 §1` renames them to `Photon.Imago.*`, and every checklist item below names the renamed paths.
<!-- claim: lines src/Imago/src/Imago.Core/Layers/AdjustmentLayer.cs = 57 -->
<!-- claim: count "^    [A-Z][A-Za-z]*,?$" src/Imago/src/Imago.Core/Layers/AdjustmentLayer.cs = 16 -->
<!-- claim: count "Levels|Curves|HueSaturation" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 0 -->
<!-- claim: count "Indexed|Duotone|Multichannel|Bitmap" src/Imago/src/Imago.Core/Documents/ColorSpace.cs = 0 -->
<!-- claim: count "Bpc(8|16|32) = " src/Imago/src/Imago.Core/Documents/BitDepth.cs = 3 -->
<!-- claim: lines src/Imago/src/Imago.Core/Colors/ColorConverter.cs = 342 -->
<!-- claim: count "public readonly record struct (Lab|Cmyk)Color" src/Imago/src/Imago.Core/Colors/ColorModels.cs = 2 -->
<!-- claim: count "Palette|Swatch" src/Imago/src/**/*.cs = 0 -->
<!-- claim: absent src/Photon.Core -->

## Inputs

- [`standards/imago.md`](../../standards/imago.md) -- the premultiplied RGBA working format (§7 records the planar exception), 8, 16, and 32-bit float, SIMD with a scalar reference, and no silent profile change
- [`standards/shared.md`](../../standards/shared.md) -- settings keys, Serilog lines, refusal messages, and the theme
- [`docs/parity/imago-parity.md`](../../docs/parity/imago-parity.md) -- the catalog rows IP-0565 to IP-0731 this file owns, plus IP-2370, IP-2375, and IP-2385 (added 2026-09-27 for ACDSee Edit mode, which the Lumen catalog routes here) (per-section ranges in each context paragraph); IP-0604 and IP-0635 belong to `D01 T07 §2` and `§3`, IP-0656 to `D01 T06 §13`, IP-0669 to IP-0672 to `D03 T05 §2`
- [`docs/parity/imago-section-design.md`](../../docs/parity/imago-section-design.md) -- "What goes to Photon.Core and Photon.UI" (palette readers, the harmony engine, and the Duotone dialog move here) and "Formats and licensing" (OpenColorIO, no bundled presets or color books)
- [`../backlog.md`](../backlog.md) -- B-014, promoted into §1
- Adobe Photoshop File Formats Specification -- Curves `.acv`, Levels `.alv`, Hue/Saturation `.ahu`, Color Table `.act`, Swatches `.aco`, Duotone `.ado`, and the Descriptor structure
- Adobe Cube LUT Specification 1.0 (`.cube`), Autodesk `.3dl`, Cinespace `.csp`, IRIDAS `.look` -- §4's LUT readers and writers
- OpenColorIO 2.4 (BSD-3-Clause) with `ociobakelut` and `ocioconvert` -- §4's OCIO adjustment and its oracle
- GIMP 3.2.6 with its GEGL operations through `gimp-console` -- the golden oracle for §2, §3, §5, §6, and §8, and the palette, decompose, and color-tool behavior of §9 and §10; Krita 5.2 as the KPL oracle
- Reinhard et al., "Color Transfer between Images" (2001); Jobson, Rahman, and Woodell, "A Multiscale Retinex" (1997); Kolås, Farup, and Rizzi, "STRESS" (2011) -- Match Color, retinex, and c2g references
- -> XREF: D01 T03 §3 -- the quantizer, dithering, and posterize behind indexed and bitmap modes and §5's dither
- -> XREF: D01 T03 §4 -- the histogram, levels, tone curve, auto adjust, equalize, exposure, temperature, and white balance §2 extends
- -> XREF: D01 T03 §5 -- hue saturation, color balance, vibrance, selective color, replace colors, desaturate, black and white, channel mixer, invert, and threshold §3 to §5 use
- -> XREF: D01 T03 §11 -- photo filter, colorize, and sepia
- -> XREF: D01 T04 §1 -- the conversions every mode, LUT, and ink readout goes through
- -> XREF: D01 T04 §2 -- gamut checks and device links behind §9's warnings
- -> XREF: D01 T04 §3 -- mode conversions and duotone, whose dialog §7 moves to `Photon.UI`
- -> XREF: D01 T05 §5 -- brand kit palettes and the ASE reader and writer §10 reuses
- -> XREF: D01 T06 §9 -- extends §8's `ExpressionCompiler` with noise primitives instead of creating it
- -> XREF: D01 T06 §13 -- alien map, the engine IP-0656 waits on, and the Equations filter that consumes §8's compiler
- -> XREF: D01 T07 §1 -- the develop tone kernel §2's Light adjustment switches to
- -> XREF: D01 T07 §2 -- the clarity and dehaze kernels §2's kinds wait on
- -> XREF: D01 T07 §3 -- the grain kernel §4's Grain kind waits on
- -> XREF: D02 T09 §4 -- the palette file readers §10 moves to `Photon.Core`
- -> XREF: D02 T09 §5 -- the harmony engine §9 moves to `Photon.Core`
- -> XREF: D03 T09 §8 -- the `Photon.Core` gradient model §4's Gradient Map and §10's palette gradients use
- -> XREF: D03 T02 §4 -- the render graph and blend modes adjustment nodes join
- -> XREF: D03 T03 §8 -- the color panel, picker, and eyedropper §9 extends
- -> XREF: D03 T05 §1 -- the filter pipeline and dialog frame the Properties pages grow from
- -> XREF: D03 T05 §2 -- the Levels, Curves, and Hue/Saturation dialogs and the histogram control §1 to §3 grow into Properties pages
- -> XREF: D03 T08 §1 -- the document model and precision §7 extends and the `imago:` contract every adjustment registers with
- -> XREF: D03 T08 §11 -- the Info panel that displays §9's sampler readouts
- -> XREF: D03 T09 §3 -- the built-in masks of adjustment layers
- -> XREF: D03 T09 §6 -- the blend modes Apply Image and Calculations use
- -> XREF: D03 T10 §3 -- select by colormap index called from §10 and the `SampleAverager` §9 extends
- -> XREF: D03 T10 §4 -- the localized color clusters Replace Color reuses
- -> XREF: D03 T10 §10 -- the split and merge engine §8 extends
- -> XREF: D03 T12 §5 -- the paint tools that wire §9's temporary eyedropper
- -> XREF: D03 T12 §9 -- the full gradient editor around §4's gradient map, listing §10's palette gradients
- -> XREF: D03 T12 §10 -- patterns for §7's custom bitmap pattern
- -> XREF: D03 T14 §1 -- destructive adjustments on smart objects become smart filters; live Shadows/Highlights and Matte Look
- -> XREF: D03 T14 §2 -- the generated filter dialog that makes the alien map entry live
- -> XREF: D03 T15 §3 -- HDR toning on 32-bit conversion, which §7 hands off to
- -> XREF: D03 T15 §4 -- HDR display for §2's curve input range and §9's intensity slider
- -> XREF: D03 T17 §3 -- PSD adjustment layers read
- -> XREF: D03 T17 §13 -- PSD adjustment layers written
- -> XREF: D03 T18 §10 -- OCIO configuration management for §4's OCIO adjustment
- -> XREF: D03 T18 §5 -- the proof setup §9's gamut warning checks against
- -> XREF: D03 T19 §10 -- the Imago assistant, which builds its edits as §1's adjustment layers and sits beside §2's classical auto corrections
- -> XREF: D03 T19 §13 -- the brand kit palettes in Imago that join §10's swatch scopes
- -> XREF: D03 T20 §7 -- the presets manager listing adjustment presets, LUTs, and palettes
- -> XREF: D04 T04 §15 -- the Lumen Viewer cites §4: the LUT readers and color lookup behind D04 T04 §15's film simulation

## Outcome

- Adjustment layers are non-destructive render-graph nodes with built-in masks, clipping, child placement, and linked instances; they persist live in `.imago` with a rendered fallback GIMP and Krita show correctly.
- The Adjustments, Properties, and Quick Adjustments panels, the targeted adjustment tool, the adjustment brush, and presets (including Photoshop ACV, ALV, and AHU files) all work over one parameter-view system.
- Every tonal and color adjustment of the three competitors, and every GIMP Colors menu operation, exists as an adjustment kind or a destructive command, each proven against a GIMP 3.2.6, OpenColorIO, or lcms2 golden.
- Documents carry bitmap, grayscale, duotone, indexed, RGB, CMYK, Lab, and multichannel modes with native planes and 8, 16, and 32-bit integer and 16 and 32-bit float precision, converting knowingly and reopening exactly.
- Apply Image, Calculations, decompose, and compose work on layers and channels, on the suite's one expression compiler.
- The color panels, picker dialog, HUD picker, color samplers, harmonies, swatches, palettes, color books, and colormap dialog work over palette readers shared with Nodus in `Photon.Core`.

**Adjacency:** list=applicable @ D03 T11 §10; document=not-applicable (no printed output; duotone and spot inks reach print through D03 T18 §6); settings=applicable @ D03 T11 §1; reporting=applicable @ D03 T11 §6; notifications=applicable @ D03 T11 §7; permissions=applicable @ D03 T11 §4; audit=applicable @ D03 T11 §1; exchange=applicable @ D03 T11 §10; reverse=applicable @ D03 T11 §1

**Adjacency rationale:** The Adjustments panel, preset lists, the LUT library, and the Swatches panel and Palettes dialog with search and tags are the browsable lists. Every default is an `Imago.Adjustments.*`, `Imago.Color.*`, or `Imago.Modes.*` key with a named consumer. Histograms in Levels, Curves, and Threshold, Match Color statistics, the histogram export, the total ink readout, and the Info panel samplers are the reporting. Mode conversions, LUT inference, and Apply Image over one second report progress and cancel. Unsupported preset or palette files, a device link that does not match the document, and masked or clipped adjustments in LUT export are refused by name. Every adjustment, conversion, and color command writes one Serilog Information line. ACV, ALV, AHU, ACT, ACO, ASE, ACB, GPL, KPL and the GIMP palette formats, CUBE, 3DL, CSP, LOOK, and ICC device links import and export. Every adjustment, mode change, and swatch edit is one undo step, and adjustment layers are non-destructive by construction.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
| 1 | §1 | Adjustment layers and the Adjustments and Properties panels | D03 T09 §3, D01 T03 §5 | [ ] |
| 2 | §2 | Tonal adjustment extensions: brightness and contrast, light, levels, and curves | §1, D01 T03 §4 | [ ] |
| 3 | §11 | Auto corrections, exposure, shadows and highlights, Light EQ, and GIMP tone operations | §2 | [ ] |
| 4 | §3 | Color adjustments I: hue, balance, vibrance, black and white, photo filter, selective color | §1 | [ ] |
| 5 | §4 | Color adjustments II: channel mixer, LUTs, gradient map, match and replace color, OCIO | §1, D01 T04 §1, D03 T09 §8, D03 T10 §4 | [ ] |
| 6 | §5 | Color adjustments III: threshold, posterize, invert, desaturate, color to alpha, and the photo effect kind | §1 | [ ] |
| 7 | §12 | GIMP color operations: exchange, rotate, color to gray, mono mixer, dither, extract, clip, and maps | §5 | [ ] |
| 8 | §6 | Color analysis | §2 | [ ] |
| 9 | §7 | Image modes and bit depth | D03 T08 §1, D01 T04 §3, D01 T03 §3 | [ ] |
| 10 | §8 | Channel operations: split, merge, decompose, compose, apply image, calculations | D03 T10 §10, D03 T09 §6 | [ ] |
| 11 | §9 | Color panels, pickers, eyedroppers, and color samplers | D03 T03 §8, D01 T04 §2, D03 T10 §3, D02 T09 §5 | [ ] |
| 12 | §10 | Swatches, palettes, and color libraries | §9, §7, D01 T05 §5, D02 T09 §4 | [ ] |

---

## 1. Adjustment Layers and the Adjustments and Properties Panels

An adjustment that bakes pixels on OK cannot be revisited, and every tutorial in all three competitors assumes adjustments stay live. This section replaces the enum-only `AdjustmentLayer` with a parameterized, masked, clippable layer rendered by the render graph, a kind registry the later sections add kinds to without touching the model, persistence through the `D03 T08 §1` contract, the Adjustments, Properties, and Quick Adjustments panels, linked instances, the targeted adjustment tool, the adjustment brush, and presets including Photoshop's preset files. It promotes backlog B-014; the integration commit also rewrites the `D03 T05 §2` context sentence that points at B-014. Catalog: IP-0565 to IP-0584 (20 features). **Corrected 2026-09-26 (integration):** the adjustment kinds are open to later sections, which register rather than edit them: Tone Compression (`D03 T15 §3`) joins at any bit depth. -> SOURCE: legacy-imago-5.1-adjustment-layers

**Fidelity:** new build, no baseline; captured to docs/captures/imago/adjustments-panel/ (Adjustments panel, a Properties page, Quick Adjustments, a targeted adjustment drag, the adjustment brush).
**Job:** a user can stack any adjustment above or inside a layer, re-edit it forever, and reuse settings as presets. Consumer: the render graph's composite and the saved `.imago` document.
**Treatment:** an Adjustments panel of kind icons and preset groups with hover preview, a Properties host (clip, view previous, reset, visibility, delete, opacity, blend mode, scrubby sliders, double-click reset), and a Quick Adjustments panel of sliders that create layers. Cheaper substitute that fails the checkpoint: an adjustment that bakes pixels on OK.
**Chrome:** consume the `D03 T05 §1` dialog frame's parameter views as Properties pages, the `D03 T05 §2` histogram control, the `D03 T09 §3` mask model, and the suite history; do not build a second parameter-view system.

**Requires:** display-session -- the panels, the targeted adjustment tool, and the adjustment brush need an interactive desktop

- [ ] Replace the enum-only model with `AdjustmentLayer { string Kind; EffectDescription Parameters; LayerMask Mask; bool ClippedToBelow; Guid? LinkId }` in `src/Imago/Photon.Imago.Core/Adjustments/AdjustmentLayer.cs` (IP-0569). Done when: `AdjustmentLayerTests` construct a layer per kind and the old `AdjustmentType` enum is gone from `Photon.Imago.Core`.
- [ ] Add `AdjustmentKindRegistry` mapping each kind id (`levels`, `curves`, `hue-saturation`, and so on) to a `D01 T03` `EffectRegistry` id and a Properties page type, so §2 to §5 register kinds without touching the model. Done when: `AdjustmentKindRegistryTests` register a fake kind and resolve its effect and page.
- [ ] Add `AdjustmentNode` in `src/Imago/Photon.Imago.Rendering/RenderGraph/`: applies the fused lookup or matrix of the `D01 T03` effect to the composite below, through the built-in mask at the layer's opacity and blend mode, re-rendering only tiles under a changed region. Done when: `AdjustmentLayerRenderTests` assert a levels layer over a fixture equals the destructive result within 1/255. Cheaper substitute: baking pixels on OK.
- [ ] Add clipped placement (only the clipped base) and Affinity child placement (only its parent layer, group, vector object, or frame content) to `AdjustmentNode` (IP-0570). Done when: `AdjustmentLayerRenderTests` assert the clipped and child results leave other layers unchanged.
- [ ] Set the budget: five stacked adjustment layers on 24 megapixels refresh the viewport under 33 ms at fit zoom. Done when: `AdjustmentNodeBudgetTests` quote the time.
- [ ] Add insertion: auto-mask from the active selection (IP-0571), `Imago.Adjustments.NewPlacement` (`AboveSelected` or `ClippedToSelected`, Affinity) (IP-0572, IP-0583), and Alt+Ctrl+G to clip. Done when: `AdjustmentInsertionTests` create a layer with a selection active and assert its mask, and read both placement values.
- [ ] Add creation from Layer, New Adjustment Layer, the Layers panel button, and the fill and adjustment content options (IP-0566, IP-0582). Done when: a driven run creates one layer from each entry and the log quotes each.
- [ ] Persist through `D03 T08 §1` as `<imago:adjustment kind="curves" v="1">` with an `<imago:params>` child holding the `EffectDescription` JSON; the stack PNG is the adjusted composite of everything below, clipped to the mask at the layer's opacity, and Imago discards it on load and restores the live layer. Done when: `AdjustmentPersistenceTests` reopen a stack live with parameters equal and assert the fallback PNG equals the flattened render.
- [ ] Add `AdjustmentsPanel.xaml` and `AdjustmentsPanelViewModel` in `Photon.Imago.Desktop/Adjustments/`: kind icons in Photoshop order, preset groups per kind, and a hover preview that renders the viewport with the preset applied and restores on leave (IP-0565, IP-0584). Done when: `AdjustmentsPanelViewModelTests` assert the hover preview restores the original view and a capture is committed.
- [ ] Add the Properties host (IP-0573): re-edit, clip to layer, view previous state (backslash), reset, visibility, merge down, delete, opacity, and blend mode. Done when: `AdjustmentPropertiesViewModelTests` assert each command on a fixture layer.
- [ ] Add `ScrubbySlider` in `Photon.Imago.Desktop/Controls/` with scrubby labels and double-click-to-reset, used by every Properties slider. Done when: `ScrubbySliderTests` assert a drag changes the value by the scaled delta and double-click restores the default.
- [ ] Add `QuickAdjustmentsPanel.xaml` (Affinity): sliders for exposure, contrast, saturation, vibrance, and temperature, each creating or editing its adjustment layer, auto buttons, and reset (IP-0578). Done when: `QuickAdjustmentsViewModelTests` move the exposure slider and one exposure layer exists.
- [ ] Add linked instances (Affinity adjustment symbols): layers sharing a `LinkId` share parameters, written as `imago:link-id`; editing one updates all in one command, and Unlink copies (IP-0574). Done when: `LinkedAdjustmentTests` edit one of two linked layers and both change in one undo step.
- [ ] Add Merge Adjustment Down, baking through the `D03 T03 §2` tile snapshot (IP-0575). Done when: `AdjustmentLayerRenderTests` merge down and the pixels equal the live render within 1/255.
- [ ] Add destructive Image, Adjustments commands running the same kinds through the `D03 T05 §1` pipeline, with Alt reopening the last-used settings (IP-0576). Done when: `DestructiveAdjustmentTests` apply twice with Alt and assert the remembered parameters.
- [ ] On a smart object, route a destructive adjustment to a smart filter once `D03 T14 §1` registers it, and ask to rasterize until then. Done when: `DestructiveAdjustmentTests` assert the rasterize prompt text naming `D03 T14 §1` while no smart-filter host is registered.
- [ ] Add `TargetedAdjustmentTool`: on-image drag for Curves (adds a point at the sampled value, vertical drag moves it), Hue/Saturation (drag changes saturation of the sampled range, Ctrl+drag changes hue), and Black and White (drag changes the sampled color's weight) (IP-0577). Done when: `TargetedAdjustmentTests` drag on a known pixel and assert the curve point and slider changes.
- [ ] Add `AdjustmentBrushTool` (Affinity): choose a kind, paint with the `D03 T03 §6` brush (width, opacity, flow, hardness, blend mode, erase) into the mask of a new adjustment layer that starts hidden-all (IP-0579). Done when: a driven stroke creates one layer whose mask coverage matches the stroke.
- [ ] Add `.imagoadj` presets holding a `D01 T03 §4` `AdjustmentPreset` in `%LOCALAPPDATA%\Rizonesoft\Imago\Presets\Adjustments\` with save, load, rename, delete, and reorder, written through the atomic writer (IP-0567). Done when: `AdjustmentPresetTests` round-trip a preset and refuse a malformed file by name.
- [ ] Add built-in presets for Levels, Curves, Hue/Saturation, Black and White, and Channel Mixer authored by Imago as data; no Adobe preset file is shipped (IP-0568). Done when: `AdjustmentPresetTests` load every built-in preset and a resources README lists their authorship.
- [ ] Read and write Photoshop `.acv`, `.alv`, and `.ahu` per Adobe's specification (IP-0581). Done when: `PhotoshopPresetFileTests` read fixtures written by Photoshop 27.10 from Imago-authored settings, write them, and reread byte-equal.
- [ ] Add `AdjustmentsMenuLayout.json` with GIMP's Colors menu groups Auto, Components, Desaturate, Info, Map, and Tone Mapping beside the Photoshop list, so every GIMP Colors command has a home (IP-0580). Done when: `AdjustmentsMenuLayoutTests` resolve every command id and find no duplicates.
- [ ] Record undo names "New Adjustment Layer", "Edit Adjustment", "Merge Adjustment Down", and "Adjustment Brush" in the suite history and log one Information line per command as `Adjustment {Command} {Kind} {Layer}`. Done when: the driven run quotes the lines.
- [ ] Commit `tests/fixtures/imago/adjustments/stack.imago` (levels, curves, hue-saturation, one clipped, one child, one linked) and the ACV, ALV, and AHU fixtures with a README naming their source. Done when: the README lists each file.
- [ ] Update `docs/user/imago/adjustments.md` with adjustment layers, the three panels, linked instances, the targeted adjustment tool, the adjustment brush, and presets. Done when: every control is documented.
- [ ] Commit: `"imago: adjustment layers, the Adjustments and Properties panels, presets, and the adjustment brush"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~AdjustmentLayerRenderTests|FullyQualifiedName~AdjustmentPersistenceTests|FullyQualifiedName~PhotoshopPresetFileTests|FullyQualifiedName~LinkedAdjustmentTests|FullyQualifiedName~AdjustmentPresetTests"` exits 0; `tests/fixtures/imago/adjustments/stack.imago` reopens live with parameters equal, its `.ora` fallback opened by GIMP 3.2.6 `gimp-console` flattens within 1/255 of Imago's render, and the ACV, ALV, and AHU fixtures round-trip byte-equal. Cheaper substitute that fails: baking on OK, which the reopen-as-live assertion catches.

## 2. Tonal Adjustment Extensions

The 0.1.0 Levels, Curves, and Brightness/Contrast (`D03 T05 §2`) cover the basics; the three competitors add color models, working spaces, eyedroppers, clipping display, and curve modes and display options. This section grows Brightness/Contrast, Light, Levels, and Curves into adjustment kinds and Properties pages on `D01 T03 §4`, never a second kernel; the auto corrections, exposure, shadows and highlights, equalize, Light EQ, and GIMP's tone operations are §11 (split out on 2026-09-27 so each half stays reviewable in one pass). Clarity and dehaze (IP-0604) are `D01 T07 §2`'s rows; this section registers their kinds disabled until that section enables them. Catalog: IP-0585 to IP-0590 and IP-0592 to IP-0595 (10 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/tonal/ (Levels, Curves with display options, Light).
**Job:** a user can correct tone with every control a Photoshop, Affinity, or GIMP tutorial names. Consumer: the adjustment layer's parameters and the render graph.
**Treatment:** Properties pages for each kind with channel and color-model pickers, eyedroppers, clipping display, and curve tools and display options. Cheaper substitute that fails the checkpoint: an RGB-only Levels with no eyedroppers.
**Chrome:** consume §1's Properties host, the `D03 T05 §2` histogram control and curve editor, and the `D03 T10 §3` `SampleAverager`; do not re-implement any `D01 T03 §4` kernel.

**Requires:** display-session -- the adjustment pages and eyedroppers need an interactive desktop

- [ ] Extend Brightness/Contrast with legacy and linear modes, Auto, and Edit as Levels (convert the parameters to an equivalent levels layer) on `D01 T03 §4` `Light` and `Levels` (IP-0585). Done when: `BrightnessContrastTests` assert Edit as Levels renders within 1/255 of the original.
- [ ] Add the Light adjustment (exposure, contrast, highlights, shadows, whites, blacks) composed from `D01 T03 §4` `Exposure`, `Light`, and `Levels` endpoints behind a version selector that switches to legacy Brightness/Contrast (IP-0586). Done when: `LightAdjustmentTests` assert each slider moves only its tonal band on a gray ramp.
- [ ] Leave the Light kind's parameters stable so `D01 T07 §1` swaps the composition for the develop tone kernel with no user-visible change. Done when: `LightAdjustmentTests` serialize the parameter set and the schema version is recorded in the `imago:adjustment` element.
- [ ] Add Levels crossed levels for negatives and Edit as Curves (Affinity) (IP-0587). Done when: `LevelsExtensionTests` assert crossed input levels invert a ramp and Edit as Curves renders within 1/255.
- [ ] Add `ColorModelAdapter` converting tiles with `D01 T04 §1` so Levels and Curves work in RGB, gray, CMYK, Lab, and on the alpha channel (IP-0588). Done when: `ColorModelAdapterTests` run Lab levels at identity on an RGB document within 1/255. Cheaper substitute: Levels only in RGB.
- [ ] Add GIMP's working space linear, non-linear, or perceptual and the linear or logarithmic histogram to Levels and Curves (IP-0589). Done when: `LevelsExtensionTests` compare levels in linear space against the GIMP 3.2.6 golden.
- [ ] Add black, gray, and white point eyedroppers and pick-from-image with sample average and sample merged through the `D03 T10 §3` `SampleAverager` (IP-0590). Done when: `LevelsEyedropperTests` pick a known gray and assert the resulting gamma.
- [ ] Add Alt-drag clipping display on Levels and Curves endpoints (IP-0592). Done when: a driven Alt-drag is captured showing clipped pixels.
- [ ] Extend `D01 T03 §4` `ToneCurve` with `NodeType` (smooth or corner) and add pencil and freehand modes with smoothing (IP-0593). Done when: `CurvesExtensionTests` compare corner-node curves against the GIMP 3.2.6 golden and `grep` finds no second curve type in Imago.
- [ ] Add curve display options: light or pigment percent, 4 by 4 or 10 by 10 grid, channel overlays, baseline, histogram, and intersection line (IP-0594). Done when: `CurvesDisplayOptionsTests` read each option's settings key.
- [ ] Add the Curves input range min and max, enabled on 32-bit float documents (HDR display is `D03 T15 §4`) (IP-0595). Done when: `CurvesExtensionTests` map an input of 4.0 on a float document through a range of 0 to 8.
- [ ] Register the clarity and dehaze kinds (IP-0604, owned by `D01 T07 §2`), pages, and `imago:` elements now, listed disabled with the tooltip "Planned: D01 T07 §2" until that section enables them. Done when: `AdjustmentKindRegistryTests` assert both kinds are registered and disabled with that tooltip.
- [ ] Set the budget: every page's slider change updates the viewport under 60 ms on 24 megapixels; log one Information line per adjustment apply. Done when: `TonalPageBudgetTests` quote the time.
- [ ] Commit goldens against GIMP 3.2.6 in `tests/fixtures/imaging/tonal-ext/` for levels in linear space and curves with corner nodes, with tolerances in each `reference.txt`. Done when: the fixture README names each golden and the `gimp-console` command.
- [ ] Update `docs/user/imago/adjustments.md` with Brightness/Contrast, Light, Levels, and Curves and every option. Done when: every control is documented.
- [ ] Commit: `"imago: brightness and contrast, light, levels, and curves extensions"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ColorModelAdapterTests|FullyQualifiedName~CurvesExtensionTests|FullyQualifiedName~LevelsExtensionTests|FullyQualifiedName~LevelsEyedropperTests|FullyQualifiedName~LightAdjustmentTests|FullyQualifiedName~BrightnessContrastTests"` exits 0, with the levels-in-linear-space and corner-node curve GIMP 3.2.6 goldens passing within their stated tolerance. Cheaper substitute that fails: Levels only in RGB, which the Lab and CMYK channel tests catch.

## 3. Color Adjustments I: Hue, Balance, Vibrance, Black and White, Photo Filter, Selective Color

The daily color adjustments of all three apps, each an adjustment kind and a destructive command over the `D01 T03 §5` kernels, with the range controls, hue curves, and presets the 0.1.0 Hue/Saturation dialog lacks, plus GIMP's hue-chroma, saturation, and color temperature operations. Catalog: IP-0608 to IP-0619 (12 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/color-adjust-1/ (Hue/Saturation with range bars, hue curves, Black and White, Photo Filter, Selective Color).
**Job:** a user can shift, saturate, balance, and tint colors by range with the controls they know. Consumer: the adjustment layer's parameters and the render graph.
**Treatment:** Properties pages with range bars and eyedroppers for Hue/Saturation, a hue-curve editor, and the preset lists each competitor ships as named data. Cheaper substitute that fails the checkpoint: a master-only Hue/Saturation.
**Chrome:** consume §1's host, the `D03 T05 §2` page, and `D01 T03 §5` kernels; do not add a second HSL helper beside `HslMath`.

**Requires:** display-session -- the adjustment pages need an interactive desktop

- [ ] Add Hue/Saturation range parameters to `D01 T03 §5` `HueSaturationLightness`: four-slider range bars with falloff, GIMP's Overlap, and an HSV computation mode (IP-0608). Done when: `ColorAdjustGoldenTests` compare hue-saturation with overlap against the GIMP 3.2.6 golden within 2/255. Cheaper substitute: a master-only Hue/Saturation.
- [ ] Add the Hue/Saturation page's add and subtract range eyedroppers and Affinity's hue wheel with draggable range nodes (IP-0608). Done when: `HueSaturationPageTests` pick a color and the range bar centers on its hue.
- [ ] Add `HueCurves` in `src/Photon.Core/Imaging/Adjust/`: hue versus saturation, hue versus hue, and hue versus luma on periodic monotone splines, with a page reusing the curve editor (IP-0609). Done when: `HueCurvesTests` assert the identity curve is exact and the wrap at 360 degrees is continuous.
- [ ] Add the Color Balance page (shadows, midtones, highlights, preserve luminosity) over `D01 T03 §5` (IP-0610). Done when: `ColorBalancePageTests` assert preserve luminosity keeps a gray ramp's luminance within 1/255.
- [ ] Add the Vibrance page with saturation over `D01 T03 §5` `Vibrance` (IP-0611, IP-0619). Done when: `VibrancePageTests` assert saturated pixels change less than muted ones.
- [ ] Add Color and Vibrance (Photoshop): temperature and tint from `D01 T03 §4` `TemperatureTint` fused with `D01 T03 §5` `Vibrance` and saturation in one kind (IP-0612). Done when: `ColorAndVibranceTests` equal the sequential application within 1/255.
- [ ] Add the Black and White page: six color sliders, tint hue and saturation, and Auto with weights from the image's hue distribution (documented), over `D01 T03 §5` `BlackAndWhite` (IP-0613). Done when: `BlackAndWhiteTests` assert Auto's weights on a two-hue fixture.
- [ ] Add Photo Filter and Lens Filter on `D01 T03 §11` `PhotoFilter` with color, density, preserve luminosity, and a filter preset list of warming, cooling, and color filters authored by Imago as named colors (IP-0614). Done when: `PhotoFilterTests` apply each preset and assert the density scaling.
- [ ] Add Selective Color on `D01 T03 §5` `SelectiveColor` with nine color families, CMYK sliders, relative or absolute, passing the document's CMYK profile through `D01 T04 §1` (IP-0615). Done when: `SelectiveColorTests` assert relative and absolute differ as Photoshop documents on a reds fixture.
- [ ] Add `HueChroma` (LCh hue, chroma, lightness) in the registry with its GEGL op id (IP-0616). Done when: `ColorAdjustGoldenTests` compare against `gegl:hue-chroma` within 2/255.
- [ ] Add `Saturation` with interpolation color space native, CIE LCh, or linear (IP-0617). Done when: `ColorAdjustGoldenTests` compare each space against `gegl:saturation` within 2/255.
- [ ] Add color temperature from original to intended Kelvin as a second mode of `TemperatureTint` (IP-0618). Done when: `ColorAdjustGoldenTests` compare against `gegl:color-temperature` within 2/255.
- [ ] Register every kind with §1 so it writes its `imago:adjustment` element and exists as a destructive command; log one Information line per apply. Done when: `AdjustmentKindRegistryTests` resolve each kind of this section.
- [ ] Commit the goldens under `tests/fixtures/imaging/color-adjust-1/` with `reference.txt` naming the `gimp-console` commands and GIMP 3.2.6. Done when: the fixture README names each golden.
- [ ] Update `docs/user/imago/adjustments.md` with each color adjustment of this section. Done when: every control is documented.
- [ ] Commit: `"imago: hue, balance, vibrance, black and white, photo filter, selective color, and GIMP hue operations"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ColorAdjustGoldenTests|FullyQualifiedName~HueCurvesTests|FullyQualifiedName~BlackAndWhiteTests|FullyQualifiedName~SelectiveColorTests"` exits 0, with the GIMP 3.2.6 goldens passing within 2/255. Cheaper substitute that fails: hue ranges without falloff, which the overlap golden rejects.

## 4. Color Adjustments II: Channel Mixer, LUTs, Gradient Map, Match and Replace Color, OCIO

Grading needs lookup tables, color transfer, and gradient maps that exchange with other tools. This section adds the Channel Mixer in any color model, color lookup with LUT files, ICC abstract and device-link profiles, LUT inference, a LUT library and LUT export, Gradient Map on the suite gradient model, Match Color and color transfer, Replace Color, Sample Colorize, White Balance with pickers, the OCIO adjustment, and the Split Toning, Recolor, and Normals kinds. The Grain kind (IP-0635) is `D01 T07 §3`'s row; this section registers it disabled until that section enables it. Gradients come from the model `D03 T09 §8` moves to `src/Photon.Core/Paint/Gradients/`; this section adds no gradient code of its own. Catalog: IP-0620 to IP-0634, IP-0636 to IP-0638, and IP-2375 (19 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/color-adjust-2/ (Color Lookup, LUT library, Gradient Map, Match Color, OCIO).
**Job:** a user can grade with LUTs and color transfers, map tones to a gradient, and exchange grades with other tools. Consumer: the adjustment layer's parameters, the render graph, and the LUT files other tools read.
**Treatment:** Properties pages plus a LUT library window with categories and a Match Color dialog with source statistics. Cheaper substitute that fails the checkpoint: a `.cube` reader with trilinear lookup and no export.
**Chrome:** consume §1's host, the `Photon.Core` gradient model moved by `D03 T09 §8`, the `D01 T04 §1` engine, and `D03 T10 §4`'s localized clusters; do not add a second LUT sampler or gradient sampler.

**Requires:** display-session -- the pages, the library window, and the Match Color dialog need an interactive desktop

- [ ] Add the Channel Mixer page: output channel, source sliders, constant, total readout, monochrome, and preserve luminosity (GIMP), over `D01 T03 §5` `ChannelMixer` (IP-0620). Done when: `ChannelMixerTests` assert the total readout and monochrome output on a fixture.
- [ ] Add the Channel Mixer color model RGB, CMYK, Lab, or HSL (Affinity) through §2's `ColorModelAdapter`, and alpha as an output for keying (IP-0621). Done when: `ChannelMixerTests` key a green background to alpha and assert coverage.
- [ ] Add LUT readers and writers in `src/Photon.Core/Imaging/Luts/` for `.cube` (1D and 3D, domain min and max), `.3dl`, `.csp` (with prelut), and `.look` (IP-0637). Done when: `LutFormatTests` round-trip each format byte-equal after reread.
- [ ] Add a `ColorLookup` effect with tetrahedral interpolation, dither, and table order RGB or BGR, plus ICC abstract and device-link profiles through `D01 T04 §1` (IP-0622). Done when: `LutFormatTests` apply a CUBE baked by `ociobakelut` within 1/255 of `ocioconvert`. Cheaper substitute: trilinear interpolation.
- [ ] Enforce the device-link policy: refuse a device link whose input space does not match the document by name, and add ICC device-link export through lcms2 `cmsTransform2DeviceLink` (IP-0637). Done when: `DeviceLinkTests` assert the refusal text and reapply an exported link within 1/255.
- [ ] Add Infer LUT (Affinity): fit a 33-cube lattice from a source and graded image pair by per-cell averaging and Laplacian fill of empty cells, with progress and Cancel (IP-0623). Done when: `InferLutTests` reproduce a fixture graded by a known LUT within 2/255.
- [ ] Add the LUT library window (Affinity) over `%LOCALAPPDATA%\Rizonesoft\Imago\LUTs\` with category folders, import, export, sort, rename, and move (IP-0624). Done when: `LutLibraryTests` import a CUBE into a category and rename it.
- [ ] Read Affinity `.afluts` category files from operator-exported samples, and if the container proves undocumented move that row to backlog B-045 through `add-todo` in the same change. Done when: either `LutLibraryTests` read the committed sample or the backlog entry names the row.
- [ ] Add Export Color Lookup Tables: sample the identity lattice (17, 33, or 65) through the top-level, unmasked, unclipped adjustment layers only, writing CUBE, 3DL, CSP, and LOOK; any masked or clipped adjustment is listed by name and excluded, as Photoshop does (IP-0625). Done when: `LutExportTests` export a two-layer stack, reapply it within 1/255, and assert the excluded-layer list.
- [ ] Add the Gradient Map page: stop bar with color and opacity stops, reverse, dither (`D01 T03 §3`), and interpolation Perceptual, Linear, or Classic on the `D03 T09 §8` `GradientDefinition`; the full editor dialog arrives in `D03 T12 §9` (IP-0626). Done when: `GradientMapTests` map a gray ramp through a three-stop gradient within 1/255.
- [ ] Add From Active Gradient reading the gradient tool's current gradient (IP-0638). Done when: `GradientMapTests` assert the created map equals the active gradient's stops.
- [ ] Add Match Color: Reinhard et al. statistics in Lab with luminance, color intensity, fade, neutralize, source document and layer, use selection in source or target for statistics, and save and load statistics as JSON (IP-0627). Done when: `MatchColorTests` assert target statistics equal source statistics within 1 percent at full strength.
- [ ] Add color transfer from a preset or reference image with luminance, intensity, saturation, hue, and preserve luminance (IP-0636). Done when: `MatchColorTests` assert preserve luminance keeps the target's luminance within 1/255.
- [ ] Add Replace Color on `D01 T03 §5` `ReplaceColors` with fuzziness, localized clusters from `D03 T10 §4`, add and subtract eyedroppers, and an HSL result (IP-0628). Done when: `ReplaceColorTests` recolor one fruit of a fixture and leave the other hue unchanged.
- [ ] Add Sample Colorize (GIMP): map a grayscale image through a sample image's luminance-to-color table (IP-0629). Done when: `SampleColorizeTests` compare against the GIMP 3.2.6 golden within 2/255.
- [ ] Add the White Balance adjustment (Affinity) with click, drag, and marquee pickers averaging a neutral through `D01 T03 §4` `WhiteBalance` (IP-0630). Done when: `WhiteBalanceAdjustmentTests` neutralize a cast patch with each picker.
- [ ] Build OpenColorIO 2.4 per RID with a thin C shim `photon_ocio` (OCIO exposes only C++) under `build/native/opencolorio/`, recording the SHA-256 and compiler in `SOURCE.txt` and the BSD-3-Clause license check in a `docs/dev/decisions.md` row. Done when: the native build script produces `win-x64` and `win-arm64` binaries and the decisions row exists.
- [ ] Add the OCIO adjustment (Affinity): P/Invoke in `src/Photon.Core/Color/Ocio/`, source and destination color space pickers, and the built-in `ocio://default` config until `D03 T18 §10` adds config management (IP-0631). Done when: `OcioAdjustmentTests` match `ocioconvert` output within 1/255 on `tests/fixtures/imago/color/ocio/`.
- [ ] Add the Split Toning (highlight and shadow hue and saturation, balance) (IP-0632), Recolor (hue, saturation, lightness) (IP-0633), and Normals (rotation, scale, flip X and Y, OpenGL and DirectX conversion) (IP-0634) kinds in the registry. Done when: `NewColorKindTests` assert each kind on a fixture, including a Normals OpenGL to DirectX flip of the green channel.
- [ ] Register the Grain kind (IP-0635, owned by `D01 T07 §3`) with its page, disabled with the tooltip "Planned: D01 T07 §3" until that section enables it. Done when: `AdjustmentKindRegistryTests` assert the disabled state and tooltip.
- [ ] Add one-click photo looks as built-in look presets (IP-2375; ACDSee Edit-mode special effects, Lumen row LP-1387): blue steel, childhood, dramatic, gloom, grunge, lomo, purple haze, seventies, and somber, each a Photon-authored `.cube` LUT plus a parameter set over existing kinds (Color Lookup, Split Toning, Curves) in `src/Photon.Core/Imaging/Luts/Looks/`, applied as one adjustment group in one undo step. Done when: `LookPresetTests` apply each look to a fixture and match its committed golden within 1/255. Cheaper substitute: shipping ACDSee's or any vendor's preset data.
- [ ] Log one Information line per apply, LUT import, and LUT export. Done when: a driven LUT export quotes its line.
- [ ] Update `docs/user/imago/adjustments.md` with the channel mixer, LUTs and the library, gradient map, match and replace color, white balance, OCIO, and the new kinds. Done when: every control is documented.
- [ ] Commit: `"imago: channel mixer, color lookup and LUTs, gradient map, match and replace color, and OCIO"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~LutFormatTests|FullyQualifiedName~OcioAdjustmentTests|FullyQualifiedName~InferLutTests|FullyQualifiedName~MatchColorTests|FullyQualifiedName~GradientMapTests|FullyQualifiedName~LutExportTests"` exits 0; LUT round trips are byte-equal after reread and the OCIO adjustment matches OpenColorIO 2.4 `ocioconvert` output within 1/255 on `tests/fixtures/imago/color/ocio/`. Cheaper substitute that fails: trilinear interpolation, which the tetrahedral OCIO golden rejects at saturated corners.

## 5. Color Adjustments III: Threshold, Posterize, Invert, Desaturate, Color to Alpha, and GIMP Color Operations

GIMP's Colors menu and Affinity's color filters hold a long tail of operations users expect to find by name. This section adds the everyday ones (threshold, local threshold, posterize, invert, desaturate, color to alpha, colorize, sepia, matte look, semi-flatten) and ACDSee's Photo effect kind in `src/Photon.Core/Imaging/Adjust/Color/` in the one `EffectRegistry`, each tagged with its GEGL op id for `D01 T06 §1`'s map, each golden-tested against GIMP 3.2.6, and each an adjustment kind or a destructive command with a generated page; the rest of GIMP's color operations (exchange, rotate, color to gray, mono mixer, dither, extract component, clip, hot, palette map, negative darkroom) are §12, split out on 2026-09-27 onto the golden harness this section builds. Alien Map (IP-0656) is `D01 T06 §13`'s row; this section registers its menu entry disabled until that engine lands. Catalog: IP-0639 to IP-0645, IP-0648, IP-0655, IP-0658, IP-0659, IP-0662 to IP-0664, and IP-2370 (15 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/color-adjust-3/ (Threshold with histogram, Color to Alpha, Photo effect, Colors, Map entries).
**Job:** a user finds every GIMP Colors command and every Affinity color filter with the same controls. Consumer: the adjustment layer's parameters or the target layer's pixels.
**Treatment:** generated pages from each effect's parameter schema through the `D03 T05 §1` frame, with a histogram on Threshold. Cheaper substitute that fails the checkpoint: disabled menu items with no pages.
**Chrome:** consume §1's host and the generated parameter views; do not hand-build a dialog per operation.

**Requires:** display-session -- the generated pages need an interactive desktop

- [ ] Add a golden harness for this section under `tests/fixtures/imaging/color-ops/<op>/` with `input.png`, `expected.png`, and `reference.txt` naming the `gimp-console` command, GIMP 3.2.6, and the tolerance. Done when: `ColorOpsGoldenTests` enumerate every folder and fail on a missing `reference.txt`.
- [ ] Add Threshold with channel choice (value, red, green, blue, alpha) and a histogram on `D01 T03 §5` `Threshold` (IP-0639), and Threshold Alpha (IP-0662). Done when: `ColorOpsGoldenTests` compare both against GIMP 3.2.6.
- [ ] Add `LocalThreshold` with radius, antialiasing, and levels (Affinity) (IP-0640). Done when: `LocalThresholdTests` binarize an unevenly lit text fixture legibly (the expected mask within 1 percent of pixels).
- [ ] Add the Posterize page on `D01 T03 §3` (IP-0641). Done when: `ColorOpsGoldenTests` compare 4 levels against `gegl:posterize`.
- [ ] Extend `D01 T03 §5` `Invert` with perceptual and linear space (IP-0642) and add `ValueInvert` (IP-0643). Done when: `ColorOpsGoldenTests` compare both against GIMP 3.2.6.
- [ ] Add Luma and Value to `D01 T03 §5` `Desaturate` beside Luminance, Lightness, and Average (IP-0644). Done when: `ColorOpsGoldenTests` compare every mode against `gegl:desaturate`.
- [ ] Add `ColorToAlpha` with transparency and opacity thresholds (IP-0645, IP-0664) and Affinity's Erase White Paper as its white preset (IP-0659). Done when: `ColorOpsGoldenTests` compare soft edges against `gegl:color-to-alpha`. Cheaper substitute: thresholding alpha against a key color.
- [ ] Add the Colorize page (hue, saturation, lightness, color) on `D01 T03 §11` `Colorize` (IP-0648). Done when: `ColorOpsGoldenTests` compare against `gegl:colorize`.
- [ ] Add the Sepia page with strength and sRGB on `D01 T03 §11` `SepiaToning` (IP-0655). Done when: `ColorOpsGoldenTests` compare against `gegl:sepia`.
- [ ] Add `MatteLook` (lifted blacks and faded contrast, Affinity) as a kind; its live filter form is `D03 T14 §1` (IP-0658). Done when: `MatteLookTests` assert the black point lifts by the set amount.
- [ ] Add `SemiFlatten` against the background color (IP-0663). Done when: `ColorOpsGoldenTests` compare against `gegl:semi-flatten`.
- [ ] Add the Photo effect adjustment kind (IP-2370; ACDSee Edit mode, Lumen row LP-1329): one kind whose parameter is a list of preset photographic looks (sepia, cross-process, bleach bypass, and similar) with a strength slider, each look a parameter set over the `D01 T03 §5` and `D01 T03 §11` kernels and §4's Color Lookup, stored in `imago:adjustment` with the look id. Done when: `PhotoEffectKindTests` render each look on a fixture within 1/255 of its committed golden and switching the look is one undo step. Cheaper substitute: one destructive Sepia command renamed Photo effect.
- [ ] Register the Colors, Map, Alien Map entry (IP-0656, owned by `D01 T06 §13`) disabled with the tooltip "Planned: D01 T06 §13"; it becomes live through `D03 T14 §2`'s generated dialog. Done when: `AdjustmentsMenuLayoutTests` assert the disabled entry and tooltip.
- [ ] Run the `D01 T03 §1` property suite over every operation of this section (transparent stays transparent, the same seed is identical, SIMD equals scalar). Done when: `ColorOpsPropertyTests` pass for each registered id.
- [ ] Set the budget: every per-pixel operation of this section under 150 ms on 24 megapixels; log one Information line per apply. Done when: `ColorOpsBudgetTests` quote each time.
- [ ] Update `docs/user/imago/adjustments.md` with every operation of this section and the Photo effect looks under their Colors menu group. Done when: every command is documented.
- [ ] Commit: `"imago: threshold, posterize, invert, desaturate, color to alpha, and the photo effect kind"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ColorOpsGoldenTests|FullyQualifiedName~ColorOpsPropertyTests|FullyQualifiedName~LocalThresholdTests|FullyQualifiedName~MatteLookTests|FullyQualifiedName~PhotoEffectKindTests"` exits 0, with every operation's GIMP 3.2.6 golden passing within the tolerance its `reference.txt` states. Cheaper substitute that fails: color to alpha by thresholding alpha against a key color, which the `gegl:color-to-alpha` golden rejects on soft edges.

## 6. Color Analysis

GIMP's Colors, Info menu reads color out of an image rather than changing it: Color Enhance, Border Average, Export Histogram, and Smooth Palette. This section adds them, with the histogram export as the file's color reporting. Catalog: IP-0665 to IP-0668 (4 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/color-analysis/ (Border Average, Export Histogram dialog, Smooth Palette result).
**Job:** a user can analyze and extract color information the way GIMP's Colors, Info menu does. Consumer: the foreground color, a written histogram file, or a new palette document.
**Treatment:** generated parameter pages, a save dialog for the histogram export, and a new-image result for Smooth Palette. Cheaper substitute that fails the checkpoint: a histogram screenshot instead of data.
**Chrome:** consume the `D01 T03 §4` `Histogram`, the generated pages, and the color panel's foreground color.

**Requires:** display-session -- the pages and the export dialog need an interactive desktop

- [ ] Add `ColorEnhance` (stretch chroma in LCh) in the registry with its GEGL op id (IP-0665). Done when: `ColorEnhanceGoldenTests` compare against `gegl:color-enhance` within 2/255.
- [ ] Add Border Average: thickness and bucket size, the most frequent quantized border color set as the foreground color, one Information line, and no document change (IP-0666). Done when: `BorderAverageTests` yield the frame color of a framed fixture and the document stays clean.
- [ ] Add Export Histogram, which exports and reports per-channel counts from `D01 T03 §4` `Histogram` for the layer or selection as CSV or plain text in GIMP's column layout (value, count per channel), through the atomic writer (IP-0667). Done when: `HistogramExportTests` assert the counts sum to the pixel count on 8-bit and 16-bit fixtures. Cheaper substitute: a 256-bin export from a 16-bit layer.
- [ ] Refuse a read-only or locked histogram target by name, leaving no partial file. Done when: `HistogramExportTests` export to a read-only path and assert the refusal text and no file.
- [ ] Add Smooth Palette: width, height, search depth, and a seeded random walk minimizing color distance, opening a new document with the striped palette (IP-0668). Done when: `SmoothPaletteTests` produce byte-identical documents from the same seed.
- [ ] Log one Information line per command with its parameters. Done when: a driven Border Average quotes its line.
- [ ] Update `docs/user/imago/adjustments.md` with the Colors, Info commands. Done when: every command is documented.
- [ ] Commit: `"imago: color enhance, border average, histogram export, and smooth palette"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ColorEnhanceGoldenTests|FullyQualifiedName~BorderAverageTests|FullyQualifiedName~HistogramExportTests|FullyQualifiedName~SmoothPaletteTests"` exits 0, with `ColorEnhanceGoldenTests` matching GIMP 3.2.6 within 2/255 and the histogram sums checking. Cheaper substitute that fails: exporting a 256-bin 8-bit histogram from a 16-bit layer, which the 16-bit fixture's count test catches.

## 7. Image Modes and Bit Depth

Print and archival work needs documents that really are CMYK, Lab, grayscale, duotone, indexed, or bitmap, at the precision the output needs, converted knowingly. This section adds the document mode, precision, and encoding model, native planar storage for non-RGB modes (recorded as an exception to the premultiplied RGBA working format), every conversion and its dialogs through `D01 T04 §3`, the Duotone dialog moved from Nodus to `Photon.UI` as its second consumer, indexed and bitmap modes on the `D01 T03 §3` quantizer, the color table editor, and precision conversion with dither. Imago's own `ColorConverter` stops being used for any conversion. Catalog: IP-0673 to IP-0688 (16 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/modes/ (Indexed Color, Bitmap, Duotone, Color Table, Convert Precision, the merge prompt).
**Job:** a user can edit in the color mode and precision their output needs and convert between them knowingly. Consumer: the document's planes and every later save, export, and print.
**Treatment:** Image, Mode (the Photoshop list plus GIMP's Mode and Encoding submenus) with conversion dialogs and a merge or flatten prompt when layers would change appearance. Cheaper substitute that fails the checkpoint: CMYK stored as RGB with a CMYK label.
**Chrome:** consume `D01 T04 §3` converters and duotone model, `D01 T03 §3` quantizer and dithers, and the Duotone dialog moved from Nodus; do not keep Imago's own `ColorConverter` for any conversion.

**Requires:** display-session -- the conversion dialogs need an interactive desktop

- [ ] Move `DuotoneDialog.xaml` and `DuotoneDialogViewModel` from `src/Nodus/Photon.Nodus.Desktop/Views/Bitmaps/` into `src/Photon.UI/Color/Duotone/` as their second consumer and repoint Nodus. Done when: Nodus's duotone tests pass against the moved dialog and `grep -rln "class DuotoneDialogViewModel" src` finds only the `Photon.UI` copy.
- [ ] Retire every conversion in Imago's `Colors/ColorConverter.cs` in favor of `D01 T04 §1`, keeping only display helpers that call it. Done when: `grep -rn "ColorConverter\.\(Rgb\|Lab\|Cmyk\)" src/Imago` prints nothing and the Imago color tests pass on the suite engine.
- [ ] Add to the `D03 T08 §1` document `DocumentColorMode { Bitmap, Grayscale, Duotone, Indexed, Rgb, Cmyk, Lab, Multichannel }`, `Precision { U8, U16, U32, F16, F32 }`, and `Encoding { Linear, NonLinear, Perceptual }` (GIMP) (IP-0684, IP-0685). Done when: `DocumentModeModelTests` construct each combination the three competitors allow and refuse the rest by name.
- [ ] Add `PlanarTile` stores (N channels plus alpha, 256 px tiles) so grayscale, CMYK, Lab, duotone, and multichannel layers keep native planes and composite for display through the `D01 T04` display transform. Done when: `ModeRoundTripTests` save and reopen a CMYK document plane-exact. Cheaper substitute: CMYK stored as RGB with a label.
- [ ] Record the planar storage as an exception to `standards/imago.md`'s premultiplied RGBA working format in a `docs/dev/decisions.md` row and add the sentence to the standard in the same change. Done when: both the decisions row and the standard's sentence exist.
- [ ] Route RGB-only operations on non-RGB documents through `D01 T04 §3` `AutoConvertForEffect`. Done when: `ModeRoundTripTests` blur a CMYK layer and the result stays CMYK.
- [ ] Add conversions RGB, CMYK, Lab, grayscale, and multichannel through `D01 T04 §3` `BitmapModeConverter` with the document profiles and intent (IP-0674, IP-0675, IP-0676, IP-0682). Done when: `ModeRoundTripTests` convert RGB to Lab to RGB within Delta E 2000 0.5 against `transicc`.
- [ ] Add the merge or flatten prompt when adjustment layers, blend modes, or styles would render differently after a conversion (IP-0681). Done when: `ModeConversionPromptTests` assert the prompt appears for a document with a Multiply layer and not for a single layer.
- [ ] Add Conditional Mode Change with source-mode checkboxes and a target mode, run as one command (IP-0688). Done when: `ModeConversionPromptTests` convert only matching documents.
- [ ] Add Bitmap mode from grayscale only: 50 Percent Threshold, Pattern Dither, Diffusion Dither, Halftone Screen (frequency, angle, shape), Custom Pattern (any grayscale image, or a library pattern once `D03 T12 §10` ships), and output resolution, through `D01 T03 §3` `BilevelConverter` and `HalftoneScreen` (IP-0673). Done when: `BitmapModeTests` convert a gray ramp with each method and assert only 0 and 1 remain.
- [ ] Add Duotone monotone to quadtone with inks, curves, overprint colors, and presets (`.ado` and `.photonduotone`) through `D01 T04 §3` and the moved dialog, storing `<imago:duotone>` beside the gray plane (IP-0677). Done when: `DuotoneModeTests` reopen a tritone document with its spec equal.
- [ ] Add Indexed mode with palettes Exact, System, Web, Uniform, Adaptive, Optimized, Custom, Previous, and GIMP's Generate Optimum, Web, Black and White, and Custom palette, color count, forced colors, transparency and matte, dither None, Diffusion (with amount), Pattern, or Noise, preserve exact colors, remove unused colors, and dither transparency, through `D01 T03 §3` `PaletteBuilder` and `PalettedConverter` (IP-0678, IP-0683). Done when: `IndexedConversionTests` assert the palette size bound, forced colors present, and exact colors preserved.
- [ ] Make indexed documents implement `D03 T10 §3`'s `IIndexedPixelSource`. Done when: `IndexedConversionTests` select an index through `SelectByIndex`.
- [ ] Add the Color Table editor (Photoshop) with load and save `.act`, and GIMP's Rearrange Colormap (drag reorder remaps indices) and Set Colormap from a palette (IP-0679). Done when: `ColorTableTests` reorder two entries and the pixels keep their colors.
- [ ] Add precision conversion for 8, 16, and 32-bit per channel and GIMP's integer and float precisions (IP-0680, IP-0684). Done when: `PrecisionTests` convert each pair and reopen at the target precision.
- [ ] Add dithering when reducing precision on layers, text layers, and channels as `Imago.Modes.DitherOnReduce` (`D01 T03 §3` ordered or Floyd-Steinberg) (IP-0686). Done when: `PrecisionTests` convert a 16-bit ramp to 8 with dither and no band is longer than the golden's.
- [ ] Add Affinity's 32-bit to 8 or 16-bit conversion with a chosen output profile; HDR toning on conversion is `D03 T15 §3` (IP-0687). Done when: `PrecisionTests` convert a float document with a named profile and the profile is recorded.
- [ ] Persist `<imago:mode kind="cmyk" precision="u16" encoding="perceptual"/>` in the document metadata, native planes as 16-bit grayscale PNGs under `data/planes/<layer-id>/`, `<imago:colormap>` for indexed documents, and every layer's stack PNG as its RGBA display conversion. Done when: `ModeRoundTripTests` reopen every fixture exactly and GIMP 3.2.6 opens the `.ora` fallback with the right picture within 1/255.
- [ ] Report progress on the status strip and notify completion with Cancel for any conversion over one second; budget: 24-megapixel RGB to CMYK under 1.5 seconds. Done when: `ModeConversionBudgetTests` quote the time and a cancelled conversion leaves the document unchanged.
- [ ] Record undo names "Convert to {Mode}" and "Convert Precision" and log one Information line with source and target mode, precision, profile, and intent. Done when: a driven CMYK conversion quotes its line.
- [ ] Commit `tests/fixtures/imago/modes/` (CMYK, Lab, duotone, indexed, and bitmap documents) with `transicc` goldens and the GIMP 3.2.6 indexed golden, each with its tolerance in `reference.txt`. Done when: the fixture README names every file.
- [ ] Update `docs/user/imago/modes.md` with every mode, conversion, the color table, and precision. Done when: every control is documented.
- [ ] Commit: `"imago: image modes, native CMYK and Lab planes, indexed and bitmap modes, duotone, and precision"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ModeRoundTripTests|FullyQualifiedName~IndexedConversionTests|FullyQualifiedName~PrecisionTests|FullyQualifiedName~BitmapModeTests|FullyQualifiedName~DuotoneModeTests"` exits 0; `tests/fixtures/imago/modes/` documents reopen exactly, conversions match `transicc` goldens within Delta E 2000 0.5, and the indexed conversion matches GIMP 3.2.6 within its recorded tolerance. Cheaper substitute that fails: storing CMYK as RGB with a label, which the plane-exact reopen assertion catches.

## 8. Channel Operations: Split, Merge, Decompose, Compose, Apply Image, Calculations

Mathematical blending of channels and layers, and pulling an image apart by color model and back, is the last piece of the color workflow. This section extends `D03 T10 §10`'s `ChannelSplitter` and `ChannelMerger` into GIMP's decompose and compose, adds Apply Image with equations and Calculations, and builds the suite's one expression compiler at the path `D01 T06 §9` later extends with noise primitives. Catalog: IP-0689 to IP-0694 (6 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/channel-ops/ (Apply Image, equations mode, Calculations, Decompose).
**Job:** a user can blend channels and layers mathematically and pull an image apart by color model and put it back. Consumer: the target layer, a new channel, a selection, or a new document.
**Treatment:** modal Apply Image and Calculations dialogs with live preview and an equations mode, and Decompose and Compose dialogs. Cheaper substitute that fails the checkpoint: Apply Image limited to Normal blending of RGB composites.
**Chrome:** consume `D03 T10 §10`'s `ChannelSplitter` and `ChannelMerger`, the `D03 T09 §6` blend modes, and the `D03 T05 §1` dialog frame; do not add a second blend-mode implementation.

**Requires:** display-session -- the dialogs and previews need an interactive desktop

- [ ] Add `ApplyImageCommand` and `ApplyImageDialog.xaml`: source document of the same size, layer or Merged, channel (color, alpha, transparency, layer mask, and `D03 T10 §10` channels) with invert, blending (every `D03 T09 §6` mode plus Add and Subtract with scale and offset), opacity, preserve transparency, and Affinity's scale to fit (IP-0689). Done when: `ApplyImageTests` assert each blend mode equals the `D03 T09 §6` compositor on the same inputs. Cheaper substitute: Normal blending of RGB composites only.
- [ ] Add the Apply Image mask with its own source, layer, channel, and invert, as one "Apply Image" step. Done when: `ApplyImageTests` apply through a half mask and assert the unmasked half unchanged.
- [ ] Add `ExpressionCompiler` at `src/Photon.Core/Imaging/Procedural/Expressions/ExpressionCompiler.cs`: a whitelisted parser to `System.Linq.Expressions` delegates compiled once and run over float spans, with no Roslyn and no reflection over user text (IP-0690). Done when: `ExpressionCompilerTests` name parser errors with their column and reject an unknown identifier.
- [ ] Give the compiler variables SR, SG, SB, SA, DR, DG, DB, DA, x, y, w, h, functions sin, cos, tan, pow, sqrt, abs, min, max, clamp, lerp, and seeded rand, and a chosen color space RGB, HSL, or Lab (IP-0690). Done when: `ExpressionCompilerTests` evaluate identity expressions exactly and SIMD equals scalar.
- [ ] Add the Apply Image equations mode (per-channel expressions in the chosen color space) on the compiler; `D01 T06 §9`, `D01 T06 §13`'s Equations filter, and `D03 T14 §10` consume it (IP-0690). Done when: `ApplyImageTests` apply `DR*0.5+SR*0.5` and equal the 50 percent Normal blend within 1/255.
- [ ] Add `CalculationsCommand` and dialog: two sources (document, layer, channel, invert), blending, opacity, a mask, and result New Document, New Channel, or Selection (IP-0691). Done when: `CalculationsTests` produce each result kind.
- [ ] Add Decompose to RGB, RGBA, Alpha, HSV, HSL, CMYK, Lab, LCh, and YCbCr (ITU R470, R709, R470 256, R709 256) as layers or separate images, writing `imago:decompose-source` so Recompose can rebuild the source (IP-0692). Done when: `DecomposeGoldenTests` match GIMP 3.2.6 decompose layers for every model within 1/255.
- [ ] Add Compose and Recompose through `ChannelMerger` (IP-0693). Done when: `DecomposeGoldenTests` decompose then compose and return the source within 1/255 for every model.
- [ ] List alpha channels, spot channels, and layer masks in every source picker of Apply Image and Calculations (IP-0694). Done when: `ChannelSourcePickerTests` list each kind from a fixture document.
- [ ] Set the budget: Apply Image on 24 megapixels under 200 ms and an equation under 400 ms, with progress and Cancel beyond one second; log one Information line per command. Done when: `ChannelOpsBudgetTests` quote both times. Cheaper substitute: an interpreter walking the tree per pixel.
- [ ] Commit GIMP 3.2.6 decompose and compose goldens for every model under `tests/fixtures/imago/channel-ops/` with `reference.txt`. Done when: the fixture README names each golden.
- [ ] Update `docs/user/imago/channels.md` with Apply Image, equations, Calculations, and decompose and compose. Done when: every control is documented.
- [ ] Commit: `"imago: Apply Image, equations, Calculations, and decompose and compose"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~DecomposeGoldenTests|FullyQualifiedName~ExpressionCompilerTests|FullyQualifiedName~ApplyImageTests|FullyQualifiedName~CalculationsTests|FullyQualifiedName~ChannelOpsBudgetTests"` exits 0; decompose then compose returns the source within 1/255 for every model and matches GIMP 3.2.6's layers. Cheaper substitute that fails: an interpreter walking the tree per pixel, which the 400 ms budget test catches.

## 9. Color Panels, Pickers, Eyedroppers, and Color Samplers

Picking and sampling color is constant in a paint session. This section extends the `D03 T03 §8` eyedropper and the `Photon.UI` picker it moved: larger sample sizes and layer sampling, the sampling ring, the temporary eyedropper modifier, desktop sampling, a HUD picker, color samplers with Info panel readouts, every color panel mode, gamut and web warnings, the Photoshop picker dialog, color history, the None swatch, GIMP's Color Picker tool, and color harmonies on the engine moved from Nodus to `Photon.Core`. Catalog: IP-0695 to IP-0716 (22 features). **Corrected 2026-09-26 (integration):** the color panel gains an intensity slider for unbounded 32-bit paint colors in `D03 T15 §4`, so its color value is linear-light float, not bytes.

**Fidelity:** docs/captures/imago/color/ from `D03 T03 §8`; new captures to docs/captures/imago/color-panels/ (each panel mode, the picker dialog, the HUD picker, sampler readouts, harmonies).
**Job:** a user can pick, sample, and reason about color in any model with every competitor's convenience. Consumer: the foreground and background colors, the document's samplers, and the swatches.
**Treatment:** the color panel gains model sliders with dynamic tracks, wheel, boxes, cubes, ramps, palette, and watercolor modes; the picker dialog; a HUD picker; a color sampler tool with pinned markers; a harmonies panel. Cheaper substitute that fails the checkpoint: the Windows color dialog.
**Chrome:** consume the `Photon.UI` `ColorPicker` that `D03 T03 §8` moved, `D01 T04 §1` and `§2`, and the moved harmony engine; do not build a second picker control.

**Requires:** display-session -- the panels, the dialog, the HUD, and screen sampling need an interactive desktop

- [ ] Move `HarmonyEngine` from `src/Nodus/Photon.Nodus.Core/Color/Harmonies/` (`D02 T09 §5`) into `src/Photon.Core/Color/Harmonies/` as its second consumer and repoint Nodus. Done when: `HarmonyEngineTests` pass against the moved engine and `grep -rln "class HarmonyEngine" src` finds only the `Photon.Core` copy.
- [ ] Add Imago's Harmonies panel (Affinity chords): harmony types, preview, lock base color, and Add Chord to Swatches (IP-0709). Done when: `HarmoniesPanelViewModelTests` add a triad to the swatches.
- [ ] Extend the eyedropper to the `D03 T10 §3` `SampleAverager` sizes up to 101 by 101 and sample Current Layer, Current and Below, All Layers, All Layers No Adjustments, and Current and Below No Adjustments (IP-0695). Done when: `SampleAverageTests` average a 101 by 101 checker exactly. Cheaper substitute: a point-only eyedropper.
- [ ] Add the sampling ring (new and current color over a gray ring) as `Imago.Color.SamplingRing` (IP-0696). Done when: a driven sample captures the ring.
- [ ] Add `TemporaryEyedropperModifier`: Alt in painting and fill tools samples into the foreground; `D03 T12 §5` wires it into every paint tool (IP-0697). Done when: `TemporaryEyedropperTests` switch to sampling while Alt is down and back on release.
- [ ] Add sample anywhere on screen: dragging from the canvas past the window samples desktop pixels through a GDI `BitBlt` of the averaged region under the cursor, per-monitor DPI aware (IP-0698). Done when: a driven sample of a known on-screen pixel reads its hex in the panel and the log.
- [ ] Add the HUD color picker: Alt+Shift+right-drag shows a hue strip or hue wheel in Small, Medium, or Large per `Imago.Color.HudPicker` (IP-0699). Done when: a driven HUD pick is captured and the chosen hue lands in the foreground.
- [ ] Add the picker preference `Imago.Color.PickerKind` (app or system picker) (IP-0716). Done when: `ColorPickerPreferenceTests` read the key and open the chosen picker.
- [ ] Add `ColorSamplerTool` with up to 10 persistent samplers, sample size, move, delete, and Clear All, stored as `<imago:samplers>`, with readouts in the `D03 T08 §11` Info panel (IP-0700). Done when: `ColorSamplerPersistenceTests` save and reopen four samplers with positions equal.
- [ ] Add color panel modes as modes of the `Photon.UI` picker: sliders RGB, HSB, HSL, CMYK, Lab, Web, and Grayscale with dynamic tracks, wheel, boxes, cubes, ramps, palette, and GIMP's watercolor selector (IP-0701, IP-0715). Done when: `ColorPanelModeTests` round-trip a color through every slider model and each mode is captured.
- [ ] Add Affinity's panel extras: a tint slider for global colors, opacity and noise, lock slider model, move sliders together, and copy hex (IP-0702). Done when: `ColorPanelModeTests` assert move-together scales every component by the same factor.
- [ ] Add the Intensity slider for unbounded values on 32-bit documents (HDR display is `D03 T15 §4`) (IP-0703), and show the color space name with the values (GIMP) (IP-0704). Done when: `ColorPanelModeTests` set intensity 2 on a float document and the foreground holds values above 1.0.
- [ ] Add warnings: the gamut warning through `D01 T04 §2` `IsInGamut` against the proof profile with click to bring into gamut, the web-safe warning, and Only Web Colors (IP-0705). Done when: `ColorWarningTests` assert sRGB 0,255,0 warns against the CMYK default and the snap result passes `IsInGamut`.
- [ ] Add the Color Picker dialog (Photoshop): HSB, RGB, Lab, CMYK, hex, sample from the image while open, Add to Swatches, and Color Libraries (§10) (IP-0706). Done when: a driven dialog samples the image and adds a swatch. Cheaper substitute: the Windows color dialog.
- [ ] Add the total ink coverage readout in the CMYK selector (GIMP) through `D01 T04 §1` (IP-0713). Done when: `InkCoverageTests` match `transicc` totals for five samples.
- [ ] Add color history and recent colors per session and per document (IP-0707) and the None transparent swatch (Affinity) (IP-0708). Done when: `ColorHistoryTests` keep the latest 20 in order and None sets a transparent fill.
- [ ] Add GIMP's Color Picker tool with pick target Set Foreground, Set Background, Add to Palette, or Pick Only, an average radius, a loupe, and apply to the selection's fill (IP-0710, IP-0714). Done when: `ColorPickerToolTests` assert each pick target.
- [ ] Add the Color Picker tool's sample merged including layer filters (the merged composite already renders live filters) (IP-0712) and the Shift info window with pixel, RGB, HSV, LCh, and CMYK readouts (IP-0711). Done when: `ColorPickerToolTests` sample merged over a live-filtered layer and the info window lists every readout.
- [ ] Log one Information line per sampler change and swatch add; picking a color is not a document change and does not log. Done when: a driven sampler add quotes its line.
- [ ] Update `docs/user/imago/color.md` with the eyedropper, samplers, panel modes, warnings, the picker dialog, the Color Picker tool, and harmonies. Done when: every control is documented.
- [ ] Commit: `"imago: color panel modes, the picker dialog, HUD picker, samplers, and harmonies"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~SampleAverageTests|FullyQualifiedName~ColorSamplerPersistenceTests|FullyQualifiedName~HarmonyEngineTests|FullyQualifiedName~InkCoverageTests|FullyQualifiedName~ColorPanelModeTests"` exits 0, a driven sample of a known pixel through each sample size shows the expected hex in the panel, and each panel mode is captured under docs/captures/imago/color-panels/. Cheaper substitute that fails: a point-only eyedropper, which the 101 by 101 average test catches.

## 10. Swatches, Palettes, and Color Libraries

Users arrive with palettes from every tool they have used. This section moves Nodus's palette readers and writers to `Photon.Core` as their second consumer, routes ASE through the `D01 T05 §5` brand kit's one reader and writer, adds the missing formats, and builds the Swatches panel with document, application, system, and brand-kit scopes, global and registration colors, user-imported color books, GIMP's Palettes dialog, editor, and commands, palette-to-gradient, and the colormap dialog for §7's indexed documents. Catalog: IP-0717 to IP-0731 (15 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/swatches/ (Swatches panel, Palettes dialog, palette editor, colormap dialog, the color book empty state).
**Job:** a user can keep, import, export, and apply palettes from any tool they came from. Consumer: the foreground color, global color references in fill layers, and the palette files other tools read.
**Treatment:** a Swatches panel with groups, search, grid or list, and scopes, a Palettes dialog and editor, and a Colormap dialog for indexed images. Cheaper substitute that fails the checkpoint: a fixed swatch strip that cannot open a user's ASE or GPL file.
**Chrome:** consume the moved palette readers, the `D01 T05 §5` ASE reader and writer and brand kits, and §9's picker; do not keep a third ASE implementation.

**Requires:** display-session -- the panel, the dialogs, and the editor need an interactive desktop

- [ ] Move the palette file readers and writers from `src/Nodus/Photon.Nodus.Core/Color/PaletteFiles/` (`D02 T09 §4`) into `src/Photon.Core/Color/Palettes/` as their second consumer and repoint Nodus. Done when: `NodusPaletteRegressionTests` prove Nodus reads the same palettes after the move.
- [ ] Route ASE through `src/Photon.Core/Brand/Ase/` from `D01 T05 §5` and delete the Nodus-local `AseReader`. Done when: `grep -rln "class AseReader" src` finds only the `Photon.Core/Brand/Ase/` copy.
- [ ] Add readers for ACT, CSS, RIFF PAL, Swatchbooker SBZ, CIE Lab text, Procreate `.swatches`, Krita KPL, and plain text in `src/Photon.Core/Color/Palettes/` (IP-0728). Done when: `PaletteFormatTests` read each committed fixture with every color, name, and group equal to the GIMP 3.2.6 or Krita 5.2 import.
- [ ] Add writers for GPL, KPL, CSS, PHP, Python, Java, text, ACO, and ASE (IP-0718, IP-0729, IP-0730). Done when: `PaletteFormatTests` round-trip each writable format byte-equal.
- [ ] Refuse an unsupported or corrupt palette file by name with the import leaving the library unchanged. Done when: `PaletteFormatTests` feed a truncated GPL and assert the refusal text.
- [ ] Read Affinity `.afpalette` from operator-exported samples, and if the container proves undocumented move that row to backlog B-045 through `add-todo` in the same change (IP-0718). Done when: either `PaletteFormatTests` read the committed sample or the backlog entry names the row.
- [ ] Add `SwatchesPanel.xaml` and `SwatchesPanelViewModel` in `Photon.Imago.Desktop/Color/`: groups, New Swatch from the foreground, add from a color or the selected layer's color, edit, search, list and grid, per-swatch opacity, legacy sets, and reset (IP-0717, IP-0731). Done when: `SwatchesPanelViewModelTests` search a 200-swatch library and add from the foreground. Cheaper substitute: a fixed swatch strip.
- [ ] Add palette scopes (Affinity): the document palette stored as `<imago:swatches>`, application palettes in `%LOCALAPPDATA%\Rizonesoft\Imago\Palettes\`, read-only system palettes authored by Imago, a default per color format, and the active `D01 T05 §5` brand kit palettes as their own scope (IP-0719). Done when: `PaletteScopeTests` reopen a document with its palette and list the brand kit scope.
- [ ] Add Create Palette from document, image, or gradient: the N most frequent colors through `D01 T03 §3` `ColorReducer`, or sampled gradient stops (IP-0720). Done when: `PaletteFromImageTests` produce the four colors of a four-color fixture.
- [ ] Add global colors and a registration color (Affinity): swatches referenced by id from fill layers and, later, shape and text layers; editing a global swatch updates every reference in one command (IP-0721). Done when: `GlobalColorTests` edit a global swatch and two fill layers change in one undo step.
- [ ] Add color libraries: user-imported ACB and ASE color books shown in the picker and the swatches through the moved `AcbReader`; nothing PANTONE-licensed ships, and the empty state explains importing a book the user owns (IP-0722). Done when: `ColorLibraryTests` import an ACB fixture and a capture shows the empty state.
- [ ] Add GIMP's Palettes dialog: grid or list, tags, new, duplicate, delete, refresh, show in folder, and copy location (IP-0723). Done when: `PalettesDialogViewModelTests` assert each command on a temporary folder.
- [ ] Add the palette editor: edit, New from FG or BG, delete color, zoom, and edit active palette (IP-0724). Done when: `PaletteEditorTests` add from FG and delete a color in two undo steps.
- [ ] Add the palette commands Export As, Offset, Sort (hue, saturation, value, luminance, and reverse), and Merge (IP-0725). Done when: `PaletteCommandTests` sort by hue and merge two palettes.
- [ ] Add Palette to Gradient and Palette to Repeating Gradient writing gradient resources into `%LOCALAPPDATA%\Rizonesoft\Imago\Gradients\` on the `Photon.Core` gradient model moved by `D03 T09 §8`; the Gradients panel listing them is `D03 T12 §9` (IP-0726). Done when: `PaletteToGradientTests` write a gradient whose stops equal the palette.
- [ ] Add the Colormap dialog (GIMP) for §7's indexed documents: edit an entry, add from FG or BG, delete unused, index and hex display, and Select by index through `D03 T10 §3`'s `SelectByIndex` with Replace, Add, Subtract, and Intersect (IP-0727). Done when: `ColormapDialogTests` edit an entry and the pixels using it change.
- [ ] Record undo names "Add Swatch", "Edit Global Color", and "Edit Colormap" and log one Information line per library change, import, and export. Done when: a driven palette import quotes its line.
- [ ] Commit the palette fixtures under `tests/fixtures/core/palettes/` with GIMP 3.2.6 and Krita 5.2 import oracles and a README naming the source of each. Done when: the README lists every format.
- [ ] Update `docs/user/imago/color.md` with swatches, scopes, global colors, color books, the Palettes dialog and editor, and the colormap dialog. Done when: every control is documented.
- [ ] Commit: `"imago: swatches, palettes, color books, and the colormap dialog on shared palette readers"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~PaletteFormatTests|FullyQualifiedName~NodusPaletteRegressionTests|FullyQualifiedName~GlobalColorTests|FullyQualifiedName~ColormapDialogTests"` exits 0; every fixture in `tests/fixtures/core/palettes/` reads with every color, name, and group equal to the oracle's import, writable formats round-trip byte-equal, and Nodus's palette tests pass on the moved code. Cheaper substitute that fails: an Imago-local GPL parser, which a `grep` for a second palette reader outside `Photon.Core` catches.

## 11. Auto Corrections, Exposure, Shadows and Highlights, Light EQ, and GIMP Tone Operations

Split from §2 on 2026-09-27 so each half stays reviewable in one pass: §2 owns Brightness/Contrast, Light, Levels, and Curves, and this section owns the one-click corrections and the tone operations beside them: Auto Tone, Auto Contrast, Auto Color, and auto levels with Photoshop's Auto Color Correction Options, Auto White Balance, exposure with offset and black level, Shadows/Highlights as a command and an adjustment kind, Equalize, GIMP's stretch contrast, retinex, and contrast curve, and ACDSee's Light EQ tone equalizer. Every operation lands in `src/Photon.Core/Imaging/Adjust/` on `D01 T03 §4`, never a second kernel. Catalog: IP-0591, IP-0596 to IP-0603, IP-0605 to IP-0607, and IP-2385 (13 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/tonal-auto/ (Auto Color Correction Options, Exposure, Shadows/Highlights, Light EQ).
**Job:** a user can correct tone in one click or with the exposure, shadow, and highlight controls a Photoshop, Affinity, GIMP, or ACDSee tutorial names. Consumer: the adjustment layer's parameters, the target layer's pixels for destructive commands, and the render graph.
**Treatment:** commands and filters for the auto corrections, an Options dialog for Auto Color Correction, and Properties pages for Exposure, Shadows/Highlights, and Light EQ. Cheaper substitute that fails the checkpoint: a single Auto command with no options and no per-band tone control.
**Chrome:** consume §1's Properties host, §2's eyedroppers and curve editor, the `D03 T05 §2` histogram control, and the `D03 T10 §3` `SampleAverager`; do not re-implement any `D01 T03 §4` kernel.

**Requires:** display-session -- the adjustment pages, the options dialog, and on-image dragging need an interactive desktop

- [ ] Add Auto Tone, Auto Contrast, Auto Color, and auto levels as commands (IP-0599) and as filters (IP-0605). Done when: `AutoCorrectionTests` apply each and compare against the `D01 T03 §4` `AutoAdjust` result.
- [ ] Add Photoshop's Auto Color Correction Options dialog: Enhance Monochromatic Contrast, Enhance Per Channel Contrast, Find Dark and Light Colors, Enhance Brightness and Contrast, Snap Neutral Midtones, target shadow, midtone, and highlight colors, and clip percentages, added to `AutoAdjust` as algorithm parameters (IP-0591). Done when: `AutoColorOptionsTests` assert each algorithm on a color-cast fixture.
- [ ] Add Auto White Balance as a command (IP-0600) and a filter (IP-0606) on `D01 T03 §4` `WhiteBalance` gray-world mode. Done when: `AutoCorrectionTests` neutralize a cast gray patch within 2/255.
- [ ] Extend `D01 T03 §4` `Exposure` and `Gamma` with offset and black level (GIMP) and add eyedroppers to the Exposure page (IP-0596). Done when: `ExposureTests` compare against the GIMP 3.2.6 `gegl:exposure` golden.
- [ ] Add `ShadowsHighlights` in `src/Photon.Core/Imaging/Adjust/`: Photoshop amount, tone, radius, color, midtone, and black and white clip, plus GIMP's white point adjustment and compress, as local luminance through the `D01 T03 §6` Gaussian then tone curves (IP-0597). Done when: `TonalExtensionGoldenTests` compare against GIMP 3.2.6 `gegl:shadows-highlights`.
- [ ] Register Shadows/Highlights as an adjustment kind (as in Affinity Photo 2) with Affinity's default and 1.6 algorithms as two parameter presets; its live filter form is `D03 T14 §1` (IP-0607). Done when: `AdjustmentKindRegistryTests` resolve the kind and both presets.
- [ ] Add Equalize with Equalize Selected Area Only or Entire Image Based on Selection on `D01 T03 §4` `Equalize` (IP-0598). Done when: `EqualizeSelectionTests` assert both options on a fixture with a selection.
- [ ] Add `StretchContrast` and `StretchContrastHsv` in `src/Photon.Core/Imaging/Adjust/`, each tagged with its GEGL op id for `D01 T06 §1`'s map (IP-0601). Done when: `TonalExtensionGoldenTests` compare both against GIMP 3.2.6.
- [ ] Add `Retinex` (uniform, low, and high levels, scale, divisions, dynamic; multiscale retinex as GIMP's plug-in) with progress and Cancel (IP-0602). Done when: `TonalExtensionGoldenTests` compare against the GIMP 3.2.6 retinex golden within its `reference.txt` tolerance.
- [ ] Add `ContrastCurve` for grayscale images (IP-0603). Done when: `TonalExtensionGoldenTests` compare against the GIMP 3.2.6 golden.
- [ ] Add the Light EQ adjustment kind and filter (IP-2385; ACDSee Edit mode, Lumen row LP-1497): auto, one-step, basic, and per-band brightening and darkening, advanced curves, and on-image drag that picks the band under the pointer, rendering through the tone-equalizer develop stage the Lumen authoring adds to the suite develop engine as `D01 T07 §7`; that stage does not exist yet, so until it ships the kind is registered disabled with the tooltip "Planned: D01 T07 §7", exactly as §2 registers clarity and dehaze. Done when: `AdjustmentKindRegistryTests` assert the disabled state and tooltip, and once the stage exists `LightEqTests` assert each mode moves only its bands on a gray ramp. Cheaper substitute: a Shadows/Highlights preset labeled Light EQ.
- [ ] Set the budget: every page's slider change updates the viewport under 60 ms on 24 megapixels, with retinex reporting progress and Cancel; log one Information line per command or adjustment apply. Done when: `TonalAutoBudgetTests` quote the time.
- [ ] Commit goldens against GIMP 3.2.6 in `tests/fixtures/imaging/tonal-ext/` for stretch contrast, retinex, shadows-highlights, and exposure, with tolerances in each `reference.txt`. Done when: the fixture README names each golden and the `gimp-console` command.
- [ ] Update `docs/user/imago/adjustments.md` with the auto corrections and their options, Exposure, Shadows/Highlights, Equalize, the GIMP tone operations, and Light EQ. Done when: every control is documented.
- [ ] Commit: `"imago: auto corrections, exposure, shadows and highlights, light EQ, and GIMP tone operations"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~TonalExtensionGoldenTests|FullyQualifiedName~AutoColorOptionsTests|FullyQualifiedName~AutoCorrectionTests|FullyQualifiedName~ExposureTests|FullyQualifiedName~EqualizeSelectionTests|FullyQualifiedName~AdjustmentKindRegistryTests"` exits 0, with every GIMP 3.2.6 golden passing within its stated tolerance and Auto Color neutralizing the cast fixture. Cheaper substitute that fails: one Auto command without the options dialog, which `AutoColorOptionsTests` catch per algorithm.

## 12. GIMP Color Operations: Exchange, Rotate, Color to Gray, Mono Mixer, Dither, Extract, Clip, and Maps

Split from §5 on 2026-09-27 so each half stays reviewable in one pass: GIMP's Colors menu and Affinity's color filters carry a long tail of operations beyond §5's everyday set. This section adds them in `src/Photon.Core/Imaging/Adjust/Color/` in the one `EffectRegistry`, each tagged with its GEGL op id for `D01 T06 §1`'s map, each golden-tested against GIMP 3.2.6 through §5's harness, and each an adjustment kind or a destructive command with a generated page. Catalog: IP-0646, IP-0647, IP-0649 to IP-0654, IP-0657, IP-0660, and IP-0661 (11 features).

**Fidelity:** new build, no baseline; captured to docs/captures/imago/color-adjust-4/ (Color Exchange, Rotate Colors, Color to Gray, Dither, Extract Component, Palette Map).
**Job:** a user finds every remaining GIMP Colors command and Affinity color filter with the same controls. Consumer: the adjustment layer's parameters or the target layer's pixels.
**Treatment:** generated pages from each effect's parameter schema through the `D03 T05 §1` frame. Cheaper substitute that fails the checkpoint: disabled menu items with no pages.
**Chrome:** consume §1's host, §5's golden harness, and the generated parameter views; do not hand-build a dialog per operation.

**Requires:** display-session -- the generated pages need an interactive desktop

- [ ] Add `ColorExchange` with per-channel thresholds (IP-0646). Done when: `ColorOpsGoldenTests` compare against `gegl:color-exchange`.
- [ ] Add `RotateColors` with source and destination hue ranges and gray handling (IP-0647). Done when: `ColorOpsGoldenTests` compare against `gegl:color-rotate`.
- [ ] Add `ColorToGray` (c2g) with radius, samples, iterations, and enhance shadows, seeded, with progress and Cancel (IP-0649). Done when: `ColorOpsGoldenTests` compare against `gegl:c2g` within its stated tolerance and the same seed reproduces byte-identically.
- [ ] Add `MonoMixer` with preserve luminosity (IP-0650). Done when: `ColorOpsGoldenTests` compare against `gegl:mono-mixer`.
- [ ] Extend `D01 T03 §3` dithering with per-channel levels and the methods random, random covariant, arithmetic add and XOR (and covariant), blue noise and covariant, with a seed (IP-0651). Done when: `ColorOpsGoldenTests` compare each method against `gegl:dither`.
- [ ] Add Affinity's Monochrome Dither and Web-Safe Dither as presets of the extended dither (IP-0660). Done when: `DitherPresetTests` assert web-safe output uses only the 216 web colors.
- [ ] Add `ExtractComponent` (RGB, HSV, HSL, CMYK, YCbCr, Lab, LCh, alpha, with invert and linear output) (IP-0652). Done when: `ColorOpsGoldenTests` compare each component against `gegl:component-extract`.
- [ ] Add `RgbClip` with low and high limits (IP-0653) and `Hot` (PAL or NTSC, reduce luminance or saturation, blacken) (IP-0654). Done when: `ColorOpsGoldenTests` compare both against GIMP 3.2.6.
- [ ] Add `PaletteMap` recoloring by value from a palette parameter; the command offers §10's active palette once §10 registers it and a grayscale ramp until then (IP-0657). Done when: `PaletteMapTests` recolor a ramp through a three-color palette.
- [ ] Add `NegativeDarkroom` with GEGL's film and paper response presets (data LGPL-3.0, attributed in THIRD-PARTY-NOTICES) (IP-0661). Done when: `ColorOpsGoldenTests` compare against `gegl:negative-darkroom`.
- [ ] Run the `D01 T03 §1` property suite over every operation of this section (transparent stays transparent, the same seed is identical, SIMD equals scalar). Done when: `ColorOpsPropertyTests` pass for each id this section registers.
- [ ] Set the budget: every per-pixel operation under 150 ms on 24 megapixels, with c2g and other spatial ones reporting progress and Cancel; log one Information line per apply. Done when: `ColorOpsBudgetTests` quote each time for this section's ids.
- [ ] Update `docs/user/imago/adjustments.md` with every operation of this section under its Colors menu group. Done when: every command is documented.
- [ ] Commit: `"imago: GIMP color operations: exchange, rotate, color to gray, dither, extract, clip, and maps"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ColorOpsGoldenTests|FullyQualifiedName~ColorOpsPropertyTests|FullyQualifiedName~PaletteMapTests|FullyQualifiedName~DitherPresetTests"` exits 0, with every operation's GIMP 3.2.6 golden passing within the tolerance its `reference.txt` states and c2g reproducing byte-identically under one seed. Cheaper substitute that fails: ordered dithering standing in for every method, which the per-method `gegl:dither` goldens reject.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` passes every adjustment, LUT, mode, channel operation, and palette fixture this file adds, with each GIMP, OpenColorIO, Krita, or lcms2 golden's version recorded
- [ ] Every capture named in a Fidelity line exists under `docs/captures/imago/`, and every user guide page named in a section exists under `docs/user/imago/`
- [ ] No second curve, histogram, quantizer, color conversion, LUT sampler, harmony engine, ASE reader, or palette reader exists in Imago (`grep` over `src/Imago` for each, quoted)
- [ ] No Adobe or Affinity preset, LUT, or color book and no PANTONE data ships in the app resources (a resources README audit)
- [ ] B-014 is gone from `todo/backlog.md`, and §1 carries its source key
- [ ] Every catalog row IP-0565 to IP-0731, IP-2370, IP-2375, and IP-2385 owned by this file is covered by a shipped section, and `docs/parity/imago-parity.md` statuses agree
- [ ] `python scripts/todo-claims.py` holds for this file
- [ ] `python scripts/todo-graph.py validate` clean
