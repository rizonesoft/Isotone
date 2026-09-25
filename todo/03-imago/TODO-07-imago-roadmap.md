---
schema_version: 1
id: imago-roadmap
domain: 03-imago
status: draft
title: "TODO-07 -- Imago Roadmap after 0.1.0"
depends_on: []
track: I7
---

# TODO-07 -- Imago Roadmap after 0.1.0

> **Goal:** The long tail of the legacy Imago roadmap, mined into buildable sections at feature grain: non-destructive adjustments, masks, the rest of the filter catalog, layer styles, retouching, text and shape layers, the brush engine, print, more formats, RAW import, color management, plugins, scripting, performance, accessibility, workspaces, and smart selection. Each section is born complete and is expected to be split further by `groom-plan` before it runs.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The legacy roadmap (`docs/legacy/imago-roadmap.md`, 853 lines, phases 0 to 11) was mined on 2026-09-26. Several features have model types and no behavior: `AdjustmentLayer`, `TextLayer`, `ShapeLayer`, `SmartObjectLayer`, `LayerMask`, `VectorMask`, `ClippingMask`, `SoftProofing`, `ColorProfile`, the plugin interfaces in `Imago.Plugins.Abstractions`, and a Roslyn `ScriptEngine` in `Imago.Scripting` (62 lines). The "Killer Feature Ideas" list (AI editing, infinite canvas, node compositing, cloud collaboration) is not converted. Every section below names its legacy source with a `-> SOURCE:` line.
<!-- claim: lines docs/legacy/imago-roadmap.md = 853 -->
<!-- claim: exists src/Imago/src/Imago.Core/Layers/AdjustmentLayer.cs -->
<!-- claim: lines src/Imago/src/Imago.Scripting/ScriptEngine.cs = 62 -->

## Inputs

- [`docs/legacy/imago-roadmap.md`](../../docs/legacy/imago-roadmap.md) -- the source of every section; read the named legacy phase before grooming
- [`standards/imago.md`](../../standards/imago.md) -- the rules every section builds to
- -> XREF: D04 T01 §4 -- the Lumen RAW decoder §11 moves to `Photon.Core` when Imago imports RAW

## Outcome

- Every section below ships with its surface, commands with undo, settings, log lines, user-guide page, and tests, like the 0.1.0 sections before it.
- Every disabled "Planned" menu item from 0.1.0 is working when this file closes.

**Adjacency:** list=applicable; document=applicable @ D03 T07 §9; settings=applicable @ D03 T07 §17; reporting=applicable; notifications=applicable; permissions=not-applicable (file refusals are owned by the format sections in D03 T04); audit=applicable; exchange=applicable; reverse=applicable

**Adjacency rationale:** The preferences and workspace work is the settings and list surface; print is the carried document; soft-proof gamut warnings are reporting; long operations notify through the status strip; every edit is logged and undoable.

## Implementation Order

| Order | Section | Deliverable                                            | Depends On              | Status |
| :---: | :-----: | ------------------------------------------------------ | ----------------------- | :----: |
|   1   |   §1    | Adjustment layers                                      | D03 T06 §3              |  [ ]   |
|   2   |   §2    | Layer masks, clipping masks, and vector masks          | D03 T06 §3              |  [ ]   |
|   3   |   §3    | The rest of the filter catalog                         | D03 T06 §3              |  [ ]   |
|   4   |   §4    | Layer styles                                           | §2                      |  [ ]   |
|   5   |   §5    | Retouching tools                                       | D03 T06 §3              |  [ ]   |
|   6   |   §6    | Text layers                                            | D03 T06 §3              |  [ ]   |
|   7   |   §7    | Shape layers and vector tools                          | §2                      |  [ ]   |
|   8   |   §8    | The brush engine: tips, dynamics, presets              | D03 T06 §3              |  [ ]   |
|   9   |   §9    | Print                                                  | §12                     |  [ ]   |
|  10   |   §10   | More formats: WebP, HEIC, EXR, GIF, PSD write          | D03 T06 §3              |  [ ]   |
|  11   |   §11   | RAW import through the shared decoder                  | D03 T06 §3, D04 T01 §4  |  [ ]   |
|  12   |   §12   | Color management and soft proofing                     | D03 T06 §3              |  [ ]   |
|  13   |   §13   | Filter plugins                                         | §3                      |  [ ]   |
|  14   |   §14   | Scripting                                              | §13                     |  [ ]   |
|  15   |   §15   | Performance: memory, SIMD, startup                     | D03 T06 §3              |  [ ]   |
|  16   |   §16   | Accessibility and localization                         | §17                     |  [ ]   |
|  17   |   §17   | Workspaces, panels, and preferences                    | D03 T06 §3              |  [ ]   |
|  18   |   §18   | Smart selection: magic wand, quick select, color range | D03 T06 §3              |  [ ]   |

---

## 1. Adjustment Layers

The 0.1.0 adjustments are destructive. Adjustment layers apply the same operations non-destructively above other layers, editable at any time, and are what makes PSD adjustment layers importable without rasterizing. -> SOURCE: legacy-imago-5.1-adjustment-layers

**Fidelity:** Layers panel with adjustment layers and the Properties panel -- docs/captures/imago/layers/.
**Job:** a user can add, edit, hide, and delete adjustments without touching pixels. Consumer: the render graph and the native format.
**Treatment:** Layer, New Adjustment Layer for each 0.1.0 adjustment plus exposure, vibrance, color balance, black and white, photo filter, channel mixer, gradient map, and selective color; parameters edited in a Properties panel with live update; stored in `.imago` and mapped from PSD. Cheaper substitute that fails the checkpoint: adjustment layers that bake on creation.
**Chrome:** consume the filter pipeline's `IImageFilter` implementations as render-graph nodes.

**Requires:** display-session -- the panels need an interactive desktop

- [ ] `AdjustmentNode` in the render graph evaluating an `IImageFilter` per tile, cached by parameters. Done when: an adjustment layer's composite equals the destructive result within 1/255.
- [ ] The Properties panel and the new adjustment set with goldens. Done when: each new adjustment passes its golden.
- [ ] Native format and PSD mapping. Done when: fixtures round-trip adjustment parameters.
- [ ] Commit: `"imago: non-destructive adjustment layers"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the adjustment-layer fixtures; a driven edit of a curves layer updates the canvas without changing the layer below (hash quoted). Cheaper substitute that fails: baked adjustments.

## 2. Layer Masks, Clipping Masks, and Vector Masks

The mask model exists (`LayerMask`, `VectorMask`, `ClippingMask`, `MaskTools`); nothing lets a user make or paint one. -> SOURCE: legacy-imago-1.6

**Fidelity:** Layers panel mask thumbnails -- docs/captures/imago/layers/.
**Job:** a user can hide parts of a layer non-destructively by painting a mask, clip a layer to the one below, and mask with a path. Consumer: the render graph and the formats.
**Treatment:** Add Mask (reveal all, hide all, from selection), paint the mask with the brush when its thumbnail is active, Alt-click to view it, disable, apply, and delete; Create Clipping Mask (Ctrl+Alt+G); vector masks from shape paths. Cheaper substitute that fails the checkpoint: masks applied destructively on creation.
**Chrome:** consume the brush engine, the layers panel, and the render graph.

**Requires:** display-session -- painting masks needs an interactive desktop

- [ ] Mask rendering in the render graph and mask editing mode. Done when: painting a mask hides pixels and undo restores them.
- [ ] Clipping and vector masks with native and PSD round trips. Done when: fixtures pass.
- [ ] Commit: `"imago: layer, clipping, and vector masks"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the mask fixtures; a driven mask paint and undo is logged. Cheaper substitute that fails: destructive masks.

## 3. The Rest of the Filter Catalog

The legacy plan lists motion and surface blur, smart sharpen, noise (add, reduce, median, dust and scratches), distort (twirl, pinch, spherize, wave, ripple, displace, polar coordinates), stylize (emboss, find edges, oil paint), and render (clouds, lens flare, lighting). The 0.1.0 menu carries the first five as disabled planned items. -> SOURCE: legacy-imago-5.2-5.7

- [ ] Implement each as an `IImageFilter` through the pipeline, each with a golden from libvips or GIMP (version recorded) and a fidelity test within a stated tolerance. Done when: every filter in the legacy list has a passing test or a recorded decision to drop it in `docs/dev/decisions.md`.
- [ ] Enable every planned filter menu item and remove its `PlannedCommands` entry. Done when: `MenuAuditTests` passes with no filter planned.
- [ ] GPU implementations for the three slowest filters with CPU parity tests. Done when: parity within 1/255 is quoted.
- [ ] Commit: `"imago: the full filter catalog"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` prints a result per filter; the GPU parity results are quoted. Cheaper substitute that fails: filters without goldens.

## 4. Layer Styles

Drop shadow, inner shadow, outer and inner glow, bevel and emboss, stroke, and color, gradient, and pattern overlays, editable and non-destructive. -> SOURCE: legacy-imago-5.8

**Fidelity:** Layer Style dialog -- new build, no baseline; captured to docs/captures/imago/layer-style/.
**Job:** a user can add and edit effects on a layer that follow its content. Consumer: the render graph and the formats.
**Treatment:** a Layer Style dialog with a list of effects and per-effect parameters, rendered as graph nodes after the layer, stored in `.imago`, and imported from PSD where the descriptor is readable. Cheaper substitute that fails the checkpoint: effects baked into pixels.
**Chrome:** consume the §2 masks and the render graph.

**Requires:** display-session -- the dialog needs an interactive desktop

- [ ] Effect nodes with goldens compared against Photoshop-produced fixtures (tool version recorded). Done when: each effect passes within a stated tolerance.
- [ ] The dialog, native storage, and PSD import. Done when: fixtures round-trip.
- [ ] Commit: `"imago: editable layer styles"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the style fixtures. Cheaper substitute that fails: baked effects.

## 5. Retouching Tools

Clone stamp, healing brush, spot healing, patch, red-eye, dodge, burn, and sponge. -> SOURCE: legacy-imago-4.6

**Fidelity:** Imago tool rail and canvas -- docs/captures/imago/main-window/.
**Job:** a user can remove blemishes and objects and locally lighten, darken, or desaturate. Consumer: the active layer.
**Treatment:** clone with aligned and sample-all-layers options; healing blends texture from the source with color from the target (a Poisson solve per dab region); spot healing samples automatically around the dab; dodge, burn, and sponge by range (shadows, midtones, highlights). Cheaper substitute that fails the checkpoint: healing implemented as a clone.
**Chrome:** consume the brush engine and the history.

**Requires:** display-session -- retouching on the canvas needs an interactive desktop

- [ ] Clone stamp and healing with tests on synthetic textures (healing's seam error below a stated bound). Done when: tests pass.
- [ ] Spot healing, patch, red-eye, dodge, burn, and sponge. Done when: each has a test and a capture.
- [ ] Commit: `"imago: clone, healing, and tonal retouching tools"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the retouching tests reporting the seam-error bound. Cheaper substitute that fails: clone-as-heal.

## 6. Text Layers

`TextLayer` exists; there is no text tool. -> SOURCE: legacy-imago-4.8

**Fidelity:** Text tool and Character panel -- new build, no baseline; captured to docs/captures/imago/text/.
**Job:** a user can add and edit live text with font, size, color, and paragraph settings. Consumer: the render graph and the formats.
**Treatment:** point and paragraph text rendered through SkiaSharp text shaping (HarfBuzz via `SkiaSharp.HarfBuzz`, license checked), editable until rasterized; stored as text in `.imago`; PSD text layers import as rasterized pixels with their text kept for re-editing where the engine data parses. Cheaper substitute that fails the checkpoint: text rasterized on commit.
**Chrome:** consume the tool system and the theme.

**Requires:** display-session -- text editing on the canvas needs an interactive desktop

- [ ] Text layout and the text tool with editing. Done when: tests assert line breaks and glyph advances for a fixture font.
- [ ] Native round trip and rasterize command. Done when: fixtures pass.
- [ ] Commit: `"imago: live text layers"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the text tests reporting; a text layer survives save and reopen editable. Cheaper substitute that fails: rasterized text.

## 7. Shape Layers and Vector Tools

`ShapeLayer` exists. Rectangles, ellipses, polygons, lines, custom shapes, and the pen tool as resolution-independent layers. -> SOURCE: legacy-imago-4.7

**Fidelity:** Shape tools and options bar -- docs/captures/imago/main-window/.
**Job:** a user can draw crisp, editable shapes and paths on raster documents. Consumer: the render graph, vector masks, and the formats.
**Treatment:** shape tools create shape layers with fill and stroke; a pen tool and path selection edit paths; paths also feed vector masks and selections. If the geometry code is the same as Nodus's, the shared parts move to `Photon.Core` through `add-todo` rather than being copied. Cheaper substitute that fails the checkpoint: shapes rasterized on creation.
**Chrome:** consume the tool system and §2's vector masks.

**Requires:** display-session -- shape drawing needs an interactive desktop

- [ ] Shape and pen tools producing shape layers. Done when: tests assert path geometry.
- [ ] Round trip through `.imago` and PSD vector data where readable. Done when: fixtures pass.
- [ ] Commit: `"imago: shape layers, the pen tool, and paths"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the shape tests reporting; shapes stay sharp at 800 percent zoom (capture). Cheaper substitute that fails: rasterized shapes.

## 8. The Brush Engine: Tips, Dynamics, Presets

The 0.1.0 brush is round. Painters need sampled tips, textures, scattering, shape and color dynamics, tilt, and saved presets, including importing ABR brushes. -> SOURCE: legacy-imago-4.4

**Fidelity:** Brush settings panel -- new build, no baseline; captured to docs/captures/imago/brush-settings/.
**Job:** a painter can build and save expressive brushes. Consumer: brush, eraser, clone, and mask painting.
**Treatment:** a brush settings panel (tip, spacing, dynamics per input: pressure, tilt, velocity), presets stored in the app-data folder, ABR import (version 6 and later) with an import report. Cheaper substitute that fails the checkpoint: presets that save only size and hardness.
**Chrome:** consume the brush engine and the settings store.

**Requires:** display-session -- brush painting needs an interactive desktop

- [ ] Sampled tips, texture, scattering, and dynamics with deterministic tests (seeded randomness). Done when: stroke goldens pass.
- [ ] Presets and ABR import. Done when: a fixture ABR imports its tips.
- [ ] Commit: `"imago: sampled brushes, dynamics, and presets"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the brush goldens reporting. Cheaper substitute that fails: size-only presets.

## 9. Print

Printing with size, position, color management, and marks. -> SOURCE: legacy-imago-7.4

**Fidelity:** Print dialog -- new build, no baseline; captured to docs/captures/imago/print/.
**Job:** a user can print an image at a chosen size with printer color management. Consumer: the printer.
**Treatment:** File, Print with a preview, scale to fit or exact size, position, printer-managed or Imago-managed color with a profile, and crop marks. Cheaper substitute that fails the checkpoint: printing a screenshot of the canvas.
**Chrome:** consume §12's color management.

**Requires:** display-session -- the print dialog needs an interactive desktop

- [ ] The print dialog and pipeline. Done when: printing to "Microsoft Print to PDF" produces a page at the requested size (measured from the PDF).
- [ ] Commit: `"imago: printing with size, color management, and marks"`

**Test checkpoint:** the PDF's image size equals the requested print size within 1 point (quoted). Cheaper substitute that fails: screen captures.

## 10. More Formats: WebP, HEIC, EXR, GIF, PSD Write

Each through `IImageFormat`, each with a fidelity fixture set; PSD write lets Imago hand layered work back to Photoshop users. -> SOURCE: legacy-imago-7.2-7.3

- [ ] WebP (SkiaSharp) and GIF (single frame) readers and writers with fixtures. Done when: fidelity tests pass.
- [ ] HEIC read through WIC when the HEIF extension is installed, refusing by name when it is not. Done when: the refusal message is tested and a fixture opens on a machine with the extension (quoted).
- [ ] OpenEXR read and write (32-bit float) through a recorded library decision. Done when: a fixture round-trips within float tolerance.
- [ ] PSD write of raster layers, groups, blend modes, opacity, and masks, verified by reopening in Imago and in Photopea or Photoshop (version recorded). Done when: fixtures round-trip and the external check is quoted.
- [ ] Commit: `"imago: WebP, HEIC, EXR, GIF, and PSD writing"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` passes every new format fixture. Cheaper substitute that fails: formats without fixtures.

## 11. RAW Import through the Shared Decoder

Lumen decodes RAW (`D04 T01 §4`). The day Imago imports RAW, the decoder adapter moves from `Photon.Lumen.Core` to `Photon.Core` and both apps consume it; nothing is copied. -> SOURCE: legacy-imago-7.2-raw

- [ ] Move the RAW decoder adapter and its tests to `Photon.Core` (and its native dependency with it), with Lumen consuming it unchanged. Done when: Lumen's RAW tests pass against the moved type and `grep` finds one decoder class.
- [ ] Imago opens RAW files through a minimal develop dialog (exposure, white balance, then open as a 16-bit document). Done when: a committed small DNG fixture opens with its dimensions.
- [ ] Commit: `"core: share the RAW decoder; Imago opens RAW files"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the moved decoder tests and an Imago RAW open test reporting; `grep -rn "class .*RawDecoder" src` prints one path under `src/Photon.Core/`. Cheaper substitute that fails: Imago referencing Lumen's assembly.

## 12. Color Management and Soft Proofing

`ColorProfile` and `SoftProofing` exist in the model. Imago needs profile assignment and conversion, a display profile for the canvas, soft proofing against a printer or CMYK profile, and gamut warnings. -> SOURCE: legacy-imago-1.3

- [ ] Choose a color-management engine (lcms2 through a wrapper, or WCS through Windows) by recorded decision with license checked. Done when: the decision entry exists.
- [ ] Assign and Convert to Profile commands, a display-profile-aware canvas, soft proof with gamut warning overlay. Done when: converting a fixture sRGB image to Display P3 matches the engine's reference transform within 1/255.
- [ ] If Nodus's soft proofing (`D02 T06 §19`) uses the same engine, move the shared wrapper to `Photon.Core`. Done when: one wrapper exists.
- [ ] Commit: `"imago: color management and soft proofing"`

**Requires:** display-session -- soft proofing on the canvas needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with conversion tests reporting; a gamut-warning capture is committed. Cheaper substitute that fails: profiles stored but ignored.

## 13. Filter Plugins

`IFilterPlugin` and `IPlugin` exist and nothing loads them. Plugins load from the app-data `plugins` folder in isolated `AssemblyLoadContext`s and appear in the Filter menu. -> SOURCE: legacy-imago-8.1-8.3

- [ ] Plugin loading with version checks and isolation; a failing plugin is disabled with a message and never crashes Imago. Done when: tests load a sample plugin and a throwing one.
- [ ] A plugin manager dialog listing, enabling, and disabling plugins. Done when: a capture is committed.
- [ ] A sample plugin project and a developer page `docs/dev/imago/plugins.md`. Done when: the sample builds and appears in the menu.
- [ ] Commit: `"imago: filter plugins in isolated load contexts"`

**Requires:** display-session -- the plugin manager needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the plugin-loading tests reporting both cases. Cheaper substitute that fails: loading plugins into the default context.

## 14. Scripting

`Imago.Scripting` holds a 62-line Roslyn `ScriptEngine`. Scripts automate edits through the same commands the UI uses. -> SOURCE: legacy-imago-8.4

- [ ] A documented scripting object model (document, layers, selection, filters) where every script run is one undoable transaction. Done when: a sample script runs and undoes in one step.
- [ ] A Scripts menu from the app-data `scripts` folder with errors reported by line. Done when: a syntax error reports its line.
- [ ] If Nodus chose the same host (`D02 T06 §20`), the host moves to `Photon.Core`. Done when: one host exists.
- [ ] Commit: `"imago: scripting over the command surface"`

**Requires:** display-session -- running scripts from the menu needs an interactive desktop

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with scripting tests reporting. Cheaper substitute that fails: scripts outside the history.

## 15. Performance: Memory, SIMD, Startup

The budgets in `standards/shared.md` applied to Imago: a 100-megapixel, 50-layer document stays responsive, and cold start is under two seconds. -> SOURCE: legacy-imago-9

- [ ] Benchmarks for open, paint, composite, and filter on the 100-megapixel document in `tests/Photon.Imago.Benchmarks`. Done when: baselines are recorded in `docs/dev/imago/performance.md`.
- [ ] Fix the top three measured costs (with before and after numbers). Done when: each improvement is quoted.
- [ ] ReadyToRun and startup trimming of work before the first window. Done when: cold start is measured under 2 seconds on the development machine (quoted).
- [ ] Commit: `"imago: measured performance work on large documents and startup"`

**Test checkpoint:** the before and after benchmark tables are quoted in the stamp. Cheaper substitute that fails: optimizations without measurements.

## 16. Accessibility and Localization

Every Imago surface keyboard- and screen-reader-operable and translatable. -> SOURCE: legacy-imago-6.5

- [ ] Audit every window with Accessibility Insights for Windows (version quoted) and fix every failure. Done when: the committed report shows none.
- [ ] Move strings to `.resx` with a pseudo-locale build. Done when: the pseudo-locale capture shows no untransformed string.
- [ ] High contrast and 200 percent captures of every window. Done when: committed.
- [ ] Commit: `"imago: accessibility fixes and localizable strings"`

**Requires:** display-session -- the audit needs an interactive desktop

**Test checkpoint:** the audit report shows zero failures. Cheaper substitute that fails: automation names on toolbar buttons only.

## 17. Workspaces, Panels, and Preferences

Saved panel layouts, a Preferences dialog over every Imago setting, and shortcut remapping. -> SOURCE: legacy-imago-6.2-6.6

**Fidelity:** Preferences dialog -- new build, no baseline; captured to docs/captures/imago/preferences/.
**Job:** a user can arrange panels, save workspaces, and change every setting and shortcut in one place. Consumer: every setting's consumer.
**Treatment:** Window, Workspace (save, switch, reset); Preferences categories bound to the settings store; shortcut remapping on the keymap. If Nodus's Preferences dialog frame (`D02 T06 §13`) fits, it moves to `Photon.UI` and both apps use it. Cheaper substitute that fails the checkpoint: settings without a surface.
**Chrome:** consume the settings store, the keymap, and AvalonDock.

**Requires:** display-session -- the dialog needs an interactive desktop

- [ ] Workspaces and Preferences with a test that every setting key has a control. Done when: the test passes.
- [ ] Enable File, Preferences and remove its planned entry. Done when: `MenuAuditTests` passes.
- [ ] Commit: `"imago: workspaces and a Preferences dialog"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the preferences tests reporting. Cheaper substitute that fails: hand-edited JSON.

## 18. Smart Selection: Magic Wand, Quick Select, Color Range

Selecting by color and edges is the next step after marquees and lassos. -> SOURCE: legacy-imago-4.2-smart-selection

**Fidelity:** Selection tools and the Color Range dialog -- docs/captures/imago/main-window/; the dialog is new build, no baseline, captured to docs/captures/imago/color-range/.
**Job:** a user can select regions by color similarity and by painting over an object's edges. Consumer: every selection-aware command.
**Treatment:** magic wand (tolerance, contiguous, sample all layers), quick selection (brush-driven region growing on an edge map), Select, Color Range with fuzziness and a preview; Select and Mask refinement (edge radius, smooth, feather) as a follow-up section filed through `add-todo` if it does not fit. Cheaper substitute that fails the checkpoint: magic wand only.
**Chrome:** consume the selection model and the tool system.

**Requires:** display-session -- selecting on the canvas needs an interactive desktop

- [ ] Magic wand and color range with tests on fixtures. Done when: selected coverage matches expected masks.
- [ ] Quick selection. Done when: a fixture object is selected within a stated boundary error.
- [ ] Commit: `"imago: magic wand, quick selection, and color range"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the smart-selection tests reporting. Cheaper substitute that fails: wand only.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] No "Planned" menu item remains in Imago
- [ ] Every new format has a fidelity fixture
- [ ] `python scripts/todo-graph.py validate` clean
