---
schema_version: 1
id: pinxit-parity-painting
domain: 03-pinxit
status: draft
title: "TODO-12 -- Pinxit Parity: the Brush Engine, Painting Tools, Fills, Gradients, and Patterns"
depends_on: []
track: I12
---

# TODO-12 -- Pinxit Parity: the Brush Engine, Painting Tools, Fills, Gradients, and Patterns

> **Goal:** Pinxit paints like Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6: the brush engine in `src/Pinxit/Isotone.Pinxit.Core/Painting/` (which stays in Pinxit; Stilus's vector brushes never need it) grows computed, sampled, erodible, bristle, airbrush, and multi-nozzle tips, smoothing and stabilizers, build-up, wet edges, texture, dual brushes, and full pen dynamics with GIMP's dynamics matrix; brushes, dynamics, and tool presets live in searchable libraries that import ABR, GBR, GIH, VBR, and MyPaint MYB (painted by libmypaint); the brush, pencil, pixel, airbrush, ink, history, art history, mixer, smudge, color replacement, and eraser tools share one options model that the `D03 T13` retouch tools also consume; fill and stroke cover the Fill dialog, scripted patterns, line-art bucket fill, and stroke styles; gradients get every shape, interpolation, the GIMP segment editor, noise and diffusion gradients, and live gradient fill layers on the suite gradient model; patterns get a library, PAT import, pattern and fill layers, pattern preview, and the pattern stamp; and symmetry painting covers every competitor's modes. Every stroke is one undoable command recorded as tile snapshots, the engine allocates nothing per dab, and no Adobe, Affinity, MyPaint, or GIMP brush, gradient, or pattern pack is bundled; users import the files they own. This file promotes backlog B-020 (`legacy-pinxit-4.4`) into §1.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** There is no brush, painting, or tool code in Pinxit yet: no type in `src/Pinxit/src/Pinxit.Core` mentions a brush, and neither `src/Pinxit/src/Pinxit.Core/Painting` nor `src/Pinxit/src/Pinxit.Core/Tools` exists; `D03 T03 §4` and `§6` create the tool system and the round brush and eraser this file extends, and their catalog rows IP-0838 to IP-0844 are `shipped-scope` there. The only gradient in `Pinxit.Core` today is the `GradientMap` adjustment type name, and no pattern type exists. Raster layers tile at 256 px (`TileSize = 256` in `src/Pinxit/src/Pinxit.Core/Tiles/Tile.cs`), the unit that dab rendering, tile snapshots, and multi-threaded painting lock on. `src/Pinxit/src/Pinxit.UI/ViewModels/MainWindowViewModel.cs` binds no brush, gradient, or fill command. `src/Isotone.Core` does not exist yet, so the gradient model this file extends arrives by the `D03 T09 §8` move. These paths are today's names; `D03 T01 §1` renames them to `Isotone.Pinxit.*`, and every checklist item below names the renamed paths.
<!-- claim: count "Brush" src/Pinxit/src/Pinxit.Core/**/*.cs = 0 -->
<!-- claim: absent src/Pinxit/src/Pinxit.Core/Painting -->
<!-- claim: absent src/Pinxit/src/Pinxit.Core/Tools -->
<!-- claim: count "Gradient" src/Pinxit/src/Pinxit.Core/**/*.cs = 1 -->
<!-- claim: count "Pattern" src/Pinxit/src/Pinxit.Core/**/*.cs = 0 -->
<!-- claim: count "TileSize = 256" src/Pinxit/src/Pinxit.Core/Tiles/Tile.cs = 1 -->
<!-- claim: count "Brush|Gradient|Fill" src/Pinxit/src/Pinxit.UI/ViewModels/MainWindowViewModel.cs = 0 -->
<!-- claim: absent src/Isotone.Core -->

## Inputs

- [`standards/pinxit.md`](../../standards/pinxit.md) -- zero allocations per dab, SIMD with a scalar reference, tile snapshots, GPU parity where a GPU path exists
- [`standards/shared.md`](../../standards/shared.md) -- settings keys, Serilog lines, refusal messages, and the theme
- [`docs/parity/pinxit-parity.md`](../../docs/parity/pinxit-parity.md) -- the catalog rows IP-0737 to IP-0896 this file owns (per-section ranges in each context paragraph); IP-0838 to IP-0844 belong to `D03 T03 §6`, IP-0845 is excluded (cloud)
- [`docs/parity/pinxit-section-design.md`](../../docs/parity/pinxit-section-design.md) -- "What goes to Isotone.Core and Isotone.UI" (the brush engine stays in Pinxit) and "Formats and licensing" (libmypaint, no bundled content)
- [`../backlog.md`](../backlog.md) -- B-020, promoted into §1 (its dynamics and texture land in §2, its presets, ABR import, and import report in §3)
- GIMP 3.2.6 `devel-docs` for GBR, GIH, VBR, PAT, and GGR, and its `app/core/gimpbrush-load.c` and `gimpgradient-load.c` as the ABR and GRD reading references; Krita 5.2's ABR loader as the second ABR oracle
- Adobe Photoshop File Formats Specification -- the Descriptor structure and pattern data behind ABR settings, GRD, and Photoshop PAT; psd-tools (MIT) as the pattern-block reading oracle
- libmypaint 1.6.1 (ISC) and the MyPaint brush file format version 3 -- §4
- Fourey et al., "A fast and efficient semi-guided algorithm for flat coloring line-arts" (2018) -- GIMP's line-art fill reference for §8
- Orzan et al., "Diffusion Curves" (SIGGRAPH 2008) -- §9's diffusion gradient
- Autodesk's hatch pattern definition format -- §10's CAD `.pat` import
- -> XREF: D03 T03 §6 -- the `BrushEngine`, brush tool, and eraser this file extends
- -> XREF: D03 T03 §8 -- the paint bucket and gradient tool §8 and §9 extend
- -> XREF: D03 T03 §2 -- tile snapshots and history states the history brush reads
- -> XREF: D03 T08 §6 -- snapshots as history brush sources
- -> XREF: D03 T08 §1 -- the `pinxit:` contract fill, pattern, and symmetry elements register with
- -> XREF: D03 T09 §1 -- the transparency lock behind protect alpha and the non-paintable layer kinds
- -> XREF: D03 T09 §6 -- blend modes including Behind and Clear for paint modes, and the Kubelka-Munk pigment kernel §6's pigment mixing reuses
- -> XREF: D03 T09 §8 -- the gradient model moved to `src/Isotone.Core/Paint/Gradients/` that §9 extends, and the `IPatternLibrary` interface §10 implements
- -> XREF: D03 T10 §1 -- the selections fill and stroke read
- -> XREF: D03 T10 §3 -- the flood engine and `SampleSource` behind the bucket, magic eraser, background eraser, and color replacement limits
- -> XREF: D03 T10 §8 -- the border morphology Stroke Selection uses
- -> XREF: D03 T11 §9 -- the temporary eyedropper §5 wires and the intensity slider HDR painting reads
- -> XREF: D03 T11 §10 -- palette gradients §9's Gradients panel lists
- -> XREF: D03 T13 §1 -- retouch brush tools consuming §1's stabilizer and wet edges and §5's shared options
- -> XREF: D03 T13 §2 -- healing tools consuming §5's shared options
- -> XREF: D03 T13 §3 -- the content-aware engine behind the Fill dialog's content-aware contents
- -> XREF: D03 T13 §4 -- toning tools consuming §5's shared options and §11's symmetry
- -> XREF: D03 T15 §4 -- HDR display for §5's 32-bit painting
- -> XREF: D03 T16 §5 -- paths for stroke path, fill path, place along path, and symmetry from a path
- -> XREF: D03 T16 §7 -- shape layers that gain gradient fill and stroke contexts
- -> XREF: D03 T17 §3 -- PSD gradient and pattern fill layers read
- -> XREF: D03 T17 §13 -- PSD gradient and pattern fill layers written
- -> XREF: D03 T20 §6 -- pen, pressure curves, and input devices that feed §2's dynamics
- -> XREF: D03 T20 §7 -- the presets manager listing brushes, dynamics, tool presets, gradients, and patterns
- -> XREF: D01 T03 §3 -- ordered and error-diffusion dither for gradients
- -> XREF: D01 T06 §13 -- moves §9's `GradientEvaluator` into `Isotone.Core` as the gradient render ops' second consumer
- -> XREF: D03 T14 §1 -- Pinxit parity filters cites §1: the brush engine behind the filter brush; §9: gradients for the flare editor and the generated gradient picker
- -> XREF: D04 T13 §3 -- Albumen parity formats cites §3: the ABR tip reader D04 T13 §3 moves to `Isotone.Core/Formats/Abr/`

## Outcome

- The brush engine paints computed, sampled, erodible, bristle, airbrush, and multi-nozzle tips with smoothing, stabilizers, build-up, wet edges, texture, dual brushes, and full seeded pen dynamics at 0 B allocated per dab, replaying recorded strokes to goldens within 1/255.
- Brushes, dynamics, and tool presets live in searchable libraries; ABR, GBR, GIH, VBR, and MYB files import with a report of what mapped, and MyPaint brushes paint through libmypaint matching GIMP 3.2.6.
- Every painting, history, mixer, smudge, color replacement, and eraser tool of the three competitors works on one shared options model the retouch tools also consume.
- The Fill and Stroke dialogs, scripted patterns, bucket extensions, and GIMP's line-art fill work on the shared flood engine and selections.
- Gradients cover every shape, interpolation, repeat, and editor of the three apps on the suite gradient model, live as fill layers and masks, with GGR, GRD, SVG, CSS, and POV-Ray exchange.
- Patterns have a library, PAT and hatch import, live pattern fill and pattern layers, pattern preview, and the pattern stamp; symmetry painting covers every competitor's modes for paint and retouch brushes.

**Adjacency:** list=applicable @ D03 T12 §3; document=not-applicable (painting produces no printed output of its own; print is D03 T18 §6); settings=applicable @ D03 T12 §5; reporting=applicable @ D03 T12 §3; notifications=applicable @ D03 T12 §8; permissions=applicable @ D03 T12 §3; audit=applicable @ D03 T12 §1; exchange=applicable @ D03 T12 §3; reverse=applicable @ D03 T12 §5

**Adjacency rationale:** The Brushes, Tool Presets, MyPaint Brushes, Gradients, and Patterns panels with groups, tags, and search are the browsable lists. Every tool option is a `Pinxit.Painting.*`, `Pinxit.Tools.<Tool>.*`, `Pinxit.Gradients.*`, or `Pinxit.Patterns.*` key with a named consumer. The ABR and brush import report, stroke previews, and the bristle preview are the reporting. Large fills, line-art fill, diffusion gradients, and library imports report progress and cancel. Unsupported or corrupt brush, pattern, and gradient files are refused by name, and text, link, and vector layers are protected from silent rasterizing. Every stroke, fill, and library change writes one Serilog Information line. ABR, GBR, GIH, VBR, GDYN, MYB, GGR, GRD, SVG gradients, Photoshop and GIMP PAT, and CAD hatch PAT import, and ABR, GGR, CSS, and POV-Ray export. Every stroke, fill, and gradient is one undo step, and library deletes go to a recycle folder.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
| 1 | §1 | The brush engine I: tips, spacing, smoothing, and wet media | D03 T03 §6 | [ ] |
| 2 | §2 | The brush engine II: dynamics | §1, D03 T09 §8 | [ ] |
| 3 | §3 | Brush presets, libraries, and tool presets | §2 | [ ] |
| 4 | §4 | MyPaint brushes | §1, §3 | [ ] |
| 5 | §5 | Painting tools and history brushes | §2, D03 T08 §6, D03 T11 §9 | [ ] |
| 6 | §6 | Mixer brush, smudge, and color replacement | §5, D03 T09 §6, D03 T10 §3 | [ ] |
| 7 | §7 | Erasers | §5, D03 T10 §3 | [ ] |
| 8 | §8 | Fill and stroke | D03 T10 §1, D03 T10 §3, D03 T10 §8, §5 | [ ] |
| 9 | §9 | Gradients and the gradient editor | D03 T03 §8, D03 T09 §8, §3 | [ ] |
| 10 | §10 | Patterns | §8, §3, D03 T09 §8 | [ ] |
| 11 | §11 | Symmetry painting | §5 | [ ] |

---

## 1. The Brush Engine I: Tips, Spacing, Smoothing, and Wet Media

Painting is judged on its brush engine. The 0.1.0 engine (`D03 T03 §6`) stamps one round dab; this section grows it into computed, sampled, erodible, bristle, airbrush, and multi-nozzle tips, Photoshop smoothing and GIMP smooth stroke, Affinity's rope and window stabilizers, build-up, wet edges with a custom profile, noise and protect texture, a size and hardness HUD, and multi-threaded dab rendering, all at zero allocations per dab and replayed from recorded pen fixtures. It promotes backlog B-020; its dynamics and texture land in §2, and presets with ABR import and an import report in §3. Catalog: IP-0737 to IP-0755 (19 features). -> SOURCE: legacy-pinxit-4.4

**Fidelity:** Pinxit brush options bar, brush tips, stabilizer, and brush HUD -- docs/design/components/ (OptionsBar, ToolRail, Canvas, Slider, NumberBox, ComboBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/main-window/, docs/captures/golden/pinxit/brush-engine/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/ToolRail/README.md, docs/design/components/Canvas/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a painter gets strokes that feel like Photoshop, Affinity, or GIMP at pen speed on large canvases. Consumer: the target layer's tiles through one tile-snapshot stroke command.
**Treatment:** tip types chosen in the brush settings, smoothing and stabilizer controls on the options bar, a bristle preview window, and an Alt+right-drag HUD. Cheaper substitute that fails the checkpoint: one round dab with a hardness falloff.
**Chrome:** consume `D03 T03 §6`'s `BrushEngine`, the tool system, and `TileSnapshotCommand`; do not add a second dab rasterizer.

**Requires:** display-session -- pen strokes, the HUD, and captures need an interactive desktop

- [ ] Add the `BrushTip` base in `src/Pinxit/Isotone.Pinxit.Core/Painting/Tips/` rasterizing into a pooled dab buffer, and move the 0.1.0 round dab onto it as `ComputedTip`. Done when: the `D03 T03 §6` brush tests pass unchanged on `ComputedTip`.
- [ ] Extend `ComputedTip` with size, angle, roundness, hardness, spacing, flip X and Y, and GIMP's shared aspect ratio and angle (IP-0739, IP-0740). Done when: `BrushTipGoldenTests` replay a recorded stroke with a 30 degree, 50 percent round tip within 1/255 of its golden.
- [ ] Add `SampledTip`: an 8-bit mask or RGBA color tip up to 5,000 px (IP-0742). Done when: `BrushTipGoldenTests` replay a color sampled tip within 1/255.
- [ ] Add Define Brush Preset from the selection or image and New round and square brushes, keeping color tips when the preset is a color brush (IP-0738, IP-0742). Done when: `DefineBrushTests` define a tip from a selection and its mask equals the selection's pixels.
- [ ] Add `ErodibleTip` (point, flat, round, square, triangle, softness, wearing with stroke length, and Sharpen Tip), `BristleTip` (bristles, length, thickness, stiffness, angle), and `AirbrushTip` (hardness, distortion, granularity, spatter size and amount) (IP-0741). Done when: `BrushTipGoldenTests` replay a recorded stroke per tip type within 1/255. Cheaper substitute: one round dab with a hardness falloff.
- [ ] Add the bristle preview window showing the current bristle tip's state live (Photoshop) (IP-0737). Done when: a capture of the preview is committed under docs/captures/pinxit/brush-engine/.
- [ ] Add `NozzleSet`: several tips with a controller (random, sequential, pressure, direction) and interpolation between nozzles; §3's GIH import maps onto it (IP-0743). Done when: `NozzleSetTests` assert the sequential controller cycles tips in order.
- [ ] Add `StrokeSmoother` in `Painting/Input/`: Photoshop smoothing 0 to 100 percent with Pulled String, Stroke Catch-up, Catch-up on Stroke End, and Adjust for Zoom, and GIMP's Smooth Stroke quality and weight (IP-0744). Done when: `StrokeSmootherTests` show pulled-string lag equals the set length.
- [ ] Add `StrokeStabilizer` (Affinity) with Rope (length) and Window (size) modes for paint and erase (IP-0745, IP-0752, IP-0755). Done when: `StrokeStabilizerTests` replay a jittered stroke and the output's deviation falls below the set window.
- [ ] Add build-up and airbrush: timer-driven dabs at `rate` while the pen rests, accumulating to the flow limit (IP-0746). Done when: `BuildUpTests` rest the pen for one second and the dab count equals the rate.
- [ ] Add wet edges as the dab alpha profile raised at the rim, with Affinity's custom edge profile curve (IP-0747, IP-0753). Done when: `BrushTipGoldenTests` replay a wet-edge stroke within 1/255.
- [ ] Add Noise and Protect Texture (Photoshop) (IP-0748) and Flow stored in the preset (IP-0749). Done when: `BrushTipGoldenTests` replay a noisy stroke with a fixed seed byte-identically.
- [ ] Add `PaintThread` (GIMP): stroke events leave the UI thread and dabs render on per-tile workers with tile locks, count from `Pinxit.Painting.Threads` (default processor count minus one); XCF save threading is `D03 T17 §4` (IP-0750). Done when: `PaintThreadTests` render the same stroke with 1 and 8 threads byte-identically.
- [ ] Add the HUD (Photoshop): Alt+right-drag horizontal changes size, vertical changes hardness, with `Pinxit.Painting.HudVertical` = Hardness or Opacity (IP-0754). Done when: `BrushHudTests` map a drag to the expected size and hardness and a capture is committed.
- [ ] Add `BrushEngineOptions` in `Painting/` holding the stabilizer and wet edges as one object that §5's `PaintToolOptions` embeds, so every `D03 T13` brush-based retouch tool consumes them (Affinity) (IP-0751). Done when: `BrushEngineOptionsTests` apply one options instance to a brush stroke and an eraser stroke with the same stabilized path.
- [ ] Commit recorded strokes `tests/fixtures/pinxit/painting/strokes/*.json` (timestamped pen samples x, y, pressure, tilt, twist) replayed deterministically, with one golden PNG per tip type. Done when: the fixture README names each stroke and golden.
- [ ] Set the budgets: 0 B allocated per dab (`GC.GetAllocatedBytesForCurrentThread` over 10,000 dabs), and a 300 px sampled tip at 10 percent spacing renders 10,000 dabs on a 16-bit 8,000 by 6,000 layer under 1 second. Done when: `DabAllocationTests` quote 0 B per dab and `BrushEngineBenchmarks` quote the time.
- [ ] Record the undo name "Brush Stroke" in the suite history and log one Information line per stroke as `Painted {Tool} {Dabs} dabs on {Layer} in {Ms} ms`. Done when: a driven stroke quotes its line.
- [ ] Update `docs/user/pinxit/painting.md` with tip types, smoothing, stabilizers, build-up, wet edges, and the HUD. Done when: every control is documented.
- [ ] Commit: `"pinxit: brush tips, smoothing, stabilizers, build-up, wet edges, and threaded painting"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~BrushTipGoldenTests|FullyQualifiedName~StrokeSmootherTests|FullyQualifiedName~DabAllocationTests|FullyQualifiedName~PaintThreadTests|FullyQualifiedName~StrokeStabilizerTests"` exits 0, each recorded stroke per tip type replays within 1/255 of its golden, and `DabAllocationTests` quote 0 B per dab. Cheaper substitute that fails: allocating a dab bitmap per stamp, which the allocation test catches.

## 2. The Brush Engine II: Dynamics

A brush responds to the pen or it is not a painting brush. This section adds pen and stroke dynamics (pressure, tilt, azimuth, barrel rotation, velocity, direction, wheel, distance, fade, random) mapped by curves to shape, scattering, texture, dual brush, color, and transfer, plus brush pose and GIMP's dynamics matrix and editor, all seeded so redo and replay are byte-identical. Texture reads patterns through `D03 T09 §8`'s `IPatternLibrary`, which §10 later implements with the full library. Catalog: IP-0756 to IP-0765 (10 features).

**Fidelity:** Pinxit Brush Settings dynamics pages and the dynamics editor -- docs/design/components/ (Panel, Dialog, Slider, NumberBox, ComboBox, Checkbox, ToggleSwitch), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/brush-dynamics/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Dialog/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ToggleSwitch/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a painter can make a brush respond to the pen exactly as their Photoshop, Affinity, or GIMP brushes do. Consumer: §1's dab generator and every tool that paints with a brush.
**Treatment:** Brush Settings pages Shape Dynamics, Scattering, Texture, Dual Brush, Color Dynamics, Transfer, and Brush Pose, each with jitter, minimum, and control; and a matrix editor of inputs against outputs with curves. Cheaper substitute that fails the checkpoint: pressure to size only.
**Chrome:** consume §1's tips and `PaintThread`, the WPF stylus stack, and the curve editor of `D03 T05 §2`; do not read pen data outside one `PenSample` source.

**Requires:** display-session -- pen dynamics need an interactive desktop and a stylus or a recorded replay

- [ ] Add the `PenSample` source in `Painting/Input/`: pressure, tilt X and Y, azimuth, barrel rotation, and wheel from WPF `StylusPoint` properties (`NormalPressure`, `XTiltOrientation`, `YTiltOrientation`, `TwistOrientation`) and the Windows Ink pointer path, with mouse fallbacks; pressure curves and device settings are `D03 T20 §6`. Done when: `PenSampleTests` map synthetic stylus points to samples and the mouse fallback yields pressure 1.
- [ ] Add `DynamicsInput` (Pressure, Tilt, Azimuth, Barrel Rotation, Velocity, Direction, Wheel, Distance, Fade, Cyclic, Random) and `DynamicsMapping { Input, Output, Curve }` with ramp curves (IP-0757). Done when: `DynamicsMatrixTests` map each input through a linear curve on synthetic samples.
- [ ] Add the outputs opacity, size, angle, color, hardness, force, aspect ratio, spacing, rate, flow, and jitter (GIMP's matrix) plus fade length, repeat (none, loop, sawtooth, triangle), and color from gradient (IP-0764). Done when: `DynamicsMatrixTests` drive each output from each input and assert the dab parameter.
- [ ] Add the GIMP dynamics matrix editor of inputs against outputs with a curve per cell, reusing the `D03 T05 §2` curve editor (IP-0764). Done when: a capture of the editor is committed and `DynamicsEditorViewModelTests` toggle a cell and edit its curve. Cheaper substitute: pressure to size only.
- [ ] Add Shape Dynamics: size, angle, and roundness jitter with minimum and control, and flip X and Y jitter (IP-0756). Done when: `ShapeDynamicsTests` assert the size range stays within minimum and maximum over 1,000 dabs.
- [ ] Add Brush Pose and Brush Projection (Photoshop) overriding tilt, rotation, and pressure (IP-0758). Done when: `ShapeDynamicsTests` assert a posed brush ignores the pen's tilt.
- [ ] Add Scattering: scatter percent, both axes, count, count jitter, and GIMP's shared Apply Jitter amount (IP-0759). Done when: `ScatteringTests` assert the dab offset distribution's bound.
- [ ] Add Texture on `D03 T09 §8`'s `IPatternLibrary`: invert, scale, brightness, contrast, texture each tip, the modes multiply, subtract, darken, overlay, color dodge, color burn, linear burn, hard mix, linear height, and height, depth with minimum and jitter, and copy texture to other tools (IP-0760). Done when: `BrushTextureTests` replay a textured stroke within 1/255 of its golden.
- [ ] Add Dual Brush and Affinity sub-brushes: a second tip (or several) with its own size, spacing, scatter, count, dynamics, and blend mode, masking the primary (IP-0761). Done when: `DualBrushTests` replay a dual-brush stroke within 1/255.
- [ ] Add Color Dynamics: foreground and background jitter, hue, saturation, and brightness jitter, purity, and apply per tip (IP-0762). Done when: `ColorDynamicsTests` assert the hue range over 1,000 dabs.
- [ ] Add Transfer: opacity, flow, wetness, and mix jitter with controls (IP-0763). Done when: `TransferDynamicsTests` assert opacity follows pressure through the mapping curve.
- [ ] Add dynamics resources: the paint tool dynamics selector, Enable Dynamics, and dynamics options shared across paint tools, stored as `.pinxitdyn`; GIMP `.gdyn` is read in §3 (IP-0765). Done when: `DynamicsResourceTests` save, load, and apply a `.pinxitdyn` byte-equal.
- [ ] Seed every jitter from the `D01 T03` seeded counter RNG with a per-stroke seed stored in the stroke command, so redo and replay are byte-identical. Done when: `JitterDeterminismTests` replay a stroke twice and redo it, all byte-identical. Cheaper substitute: unseeded `Random`.
- [ ] Set the budget: all dynamics on add less than 25 percent to §1's 10,000-dab benchmark and keep 0 B per dab. Done when: `DabAllocationTests` and `BrushEngineBenchmarks` quote both with dynamics on.
- [ ] Commit recorded pen fixtures with tilt and barrel rotation and their goldens under `tests/fixtures/pinxit/painting/strokes/`. Done when: the fixture README names each.
- [ ] Update `docs/user/pinxit/painting.md` with every dynamics page and the matrix editor. Done when: every control is documented.
- [ ] Commit: `"pinxit: brush dynamics, texture, dual brush, and the dynamics matrix"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~DynamicsMatrixTests|FullyQualifiedName~JitterDeterminismTests|FullyQualifiedName~BrushTextureTests|FullyQualifiedName~DualBrushTests|FullyQualifiedName~PenSampleTests"` exits 0, and recorded pen strokes with pressure, tilt, and barrel rotation replay to their goldens within 1/255 and twice byte-identically. Cheaper substitute that fails: unseeded `Random` jitter, which the determinism test catches.

## 3. Brush Presets, Libraries, and Tool Presets

Painters bring their brush sets from the app they came from. This section adds the brush preset format and one generic resource library that §4, §9, and §10 reuse, the Brushes and Brush Settings panels, recent brushes, ABR import and export with an import report, Affinity brush exchange, GIMP's GBR, GIH, and VBR brushes with the parametric editor, clipboard brushes, dynamics presets, and tool presets with their panel. Catalog: IP-0766 to IP-0787 (22 features).

**Corrected 2026-09-27:** Albumen browses ABR files as images (`D04 T13 §3`), so it moves this section's ABR tip reader to `src/Isotone.Core/Formats/Abr/`; Pinxit's brush import repoints.

**Fidelity:** Pinxit Brushes and Tool Presets panels and Brush Settings -- docs/design/components/ (Panel, ListTree, OptionsBar, ToolRail, ContextMenu, Dialog, Slider, NumberBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/brush-library/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/ToolRail/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Dialog/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a painter can bring their brush sets from any of the three apps, find a brush fast, and save tool setups. Consumer: the active paint tool's brush and options.
**Treatment:** a Brushes panel with groups, search, recent brushes, and stroke-preview thumbnails; a Brush Settings panel with live preview and locks; GIMP's brush and dynamics dialogs as the same panel's commands; a Tool Presets panel with Current Tool Only. Cheaper substitute that fails the checkpoint: a flat list of tip images.
**Chrome:** consume §1 and §2 models, the theme, and the resource folder pattern `D03 T20 §7` manages; do not build a second library store per resource kind.

**Requires:** display-session -- the panels, the import report, and the editors need an interactive desktop

- [ ] Add `BrushPreset` (`.pinxitbrush` JSON: tip, dynamics, texture, dual, color, transfer, and optional tool settings, size, and color). Done when: `BrushPresetTests` round-trip a preset byte-equal.
- [ ] Add `ResourceLibrary<T>` in `Isotone.Pinxit.Core/Resources/` over `%LOCALAPPDATA%\Rizonesoft\Pinxit\Brushes\` with folders as groups, tags, favorites, search, and a recycle folder for deletes; §4, §9, and §10 reuse it. Done when: `BrushLibraryTests` search by tag, delete to the recycle folder, and restore.
- [ ] Refuse an unsupported or corrupt resource file by name with a refusal policy that leaves the library unchanged. Done when: `BrushLibraryTests` import a truncated file and assert the refusal text.
- [ ] Add `BrushesPanel.xaml` and `BrushesPanelViewModel`: groups and categories, search, recent brushes, list and thumbnail views with stroke previews, and default categories of brushes authored by Pinxit (IP-0771, IP-0787). Done when: `BrushesPanelViewModelTests` filter 500 brushes by search and a capture shows both views. Cheaper substitute: a flat list of tip images.
- [ ] Add GIMP's brush list commands: grid and list, tags, spacing, refresh, open as image, copy location, show in folder, and the context menu (IP-0778, IP-0767). Done when: `BrushesPanelViewModelTests` assert each command on a temporary library.
- [ ] Add the Brush Settings panel: live stroke preview, lock attributes, clear brush controls, reset, and create new brush from settings (IP-0770). Done when: `BrushSettingsViewModelTests` lock an attribute and assert switching presets keeps it.
- [ ] Add the preset picker and management: size, rename, duplicate, delete, move, update, reset, a modified indicator, and New Brush Preset options capture size, include tool settings, and include color (IP-0772, IP-0776). Done when: `BrushPresetTests` assert the modified indicator and each capture option.
- [ ] Add tool association (Affinity): a brush switches to its associated tool and each tool remembers its last brush in `Pinxit.Tools.<Tool>.LastBrush` (IP-0773). Done when: `BrushAssociationTests` pick an eraser brush and the eraser becomes active.
- [ ] Add recent brushes per layer (Affinity) as `pinxit:recent-brushes` on the layer element (IP-0769) and the shared paint tool brush selector (GIMP) (IP-0777). Done when: `BrushAssociationTests` reopen a document and the layer's recent brushes are listed.
- [ ] Add `AbrReader` in `src/Pinxit/Isotone.Pinxit.FileFormats/Brushes/Abr/`: ABR v1 and v2 sampled tips and v6 to v10 `samp` tips plus the `desc` descriptor mapped onto tips, dynamics, scattering, texture, dual brush, color, and transfer (IP-0768). Done when: `AbrReaderTests` load every fixture's tips byte-equal to GIMP 3.2.6's and Krita 5.2's loaded tips.
- [ ] Add the ABR import report listing per preset what mapped, what was approximated, and what was dropped, shown after import and logged at Information (IP-0768). Done when: `AbrReaderTests` assert the report entries for the v6 fixture.
- [ ] Add `AbrWriter` exporting v6 with sampled tips and the settings the descriptor maps (IP-0774). Done when: `AbrReaderTests` export a preset and reread it with the same tips and mapped settings.
- [ ] Add Affinity `.afbrushes` import and export from operator-exported samples; if the container proves undocumented, move those rows to backlog B-045 through `add-todo` in the same change and keep ABR as the Affinity interchange path (IP-0774). Done when: either `AfBrushesTests` read the committed sample or the backlog entry names the rows.
- [ ] Add GIMP GBR v2 grayscale and color brushes (IP-0780). Done when: `GimpBrushFormatTests` round-trip GBR fixtures byte-equal.
- [ ] Add GIH image hoses with ranks and selection modes (incremental, angular, random, velocity, pressure, xtilt, ytilt) mapped onto §1's `NozzleSet` (IP-0781). Done when: `GimpBrushFormatTests` round-trip a GIH fixture byte-equal.
- [ ] Add VBR with a parametric brush editor (circle, square, diamond, radius, spikes, hardness, aspect, angle, spacing) (IP-0782). Done when: `GimpBrushFormatTests` round-trip VBR fixtures byte-equal and a capture shows the editor.
- [ ] Add the clipboard brush and Paste as New Brush (GIMP): name, file, spacing, up to 8,192 px (IP-0766, IP-0779). Done when: `ClipboardBrushTests` paste an image and a brush with its pixels appears.
- [ ] Add legacy brush sets and Reset to factory brushes, restoring Pinxit's authored defaults only (IP-0775). Done when: `BrushLibraryTests` reset and the default category matches the shipped list.
- [ ] Add the dynamics presets dialog (GIMP): new, duplicate, delete, refresh, copy location, and show in folder over `.pinxitdyn`, plus GIMP `.gdyn` read (IP-0783). Done when: `DynamicsResourceTests` read a GIMP 3.2.6 `.gdyn` fixture into the matching matrix.
- [ ] Add `.pinxittoolpreset` JSON of any tool's options with the Tool Presets panel and options bar picker, Current Tool Only, save, restore, edit, delete, and GIMP's tool preset editor (IP-0784, IP-0785, IP-0786). Done when: `ToolPresetTests` save a preset for two tools and Current Tool Only lists one.
- [ ] Commit the fixtures: ABR v2 and v6 files the operator authors in Photoshop 27.10 from Pinxit-drawn tips and GBR, GIH, VBR, and GDYN files authored in GIMP 3.2.6, under CC0 in `tests/fixtures/pinxit/brushes/` with a README naming the source of each. Done when: the README lists every file.
- [ ] Log one Information line per import, export, and library change. Done when: a driven ABR import quotes its line and the report.
- [ ] Update `docs/user/pinxit/brushes.md` with the libraries, panels, formats, the import report, and tool presets. Done when: every control is documented.
- [ ] Commit: `"pinxit: brush libraries, ABR and GIMP brush formats, and tool presets"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~AbrReaderTests|FullyQualifiedName~GimpBrushFormatTests|FullyQualifiedName~ToolPresetTests|FullyQualifiedName~BrushLibraryTests|FullyQualifiedName~BrushPresetTests"` exits 0; every ABR fixture's tips match both GIMP 3.2.6's and Krita 5.2's loaded tips byte-equal and GBR, GIH, and VBR round-trip byte-equal. Cheaper substitute that fails: importing ABR tips while dropping every setting silently, which the import report assertion on the v6 fixture catches.

## 4. MyPaint Brushes

MyPaint brush files describe a brush engine of their own, and translating them into Pinxit settings would change how they paint. This section hosts libmypaint 1.6.1 through P/Invoke behind GIMP's MyPaint Brush tool, painting only through a tile adapter inside one tile-snapshot stroke, with MYB loading, the tool's options, and a MyPaint Brushes dialog on §3's resource library. Catalog: IP-0788 to IP-0791 (4 features).

**Fidelity:** Pinxit MyPaint brush options and the MyPaint Brushes dialog -- docs/design/components/ (OptionsBar, Dialog, ListTree, Slider, NumberBox, ToolRail), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/mypaint/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ToolRail/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a painter can use their MyPaint brush files in Pinxit with the same response. Consumer: the target layer's tiles.
**Treatment:** a MyPaint Brush tool with GIMP's options and a MyPaint Brushes dialog. Cheaper substitute that fails the checkpoint: converting MYB settings into Pinxit presets approximately.
**Chrome:** consume §1's `PaintThread`, tile snapshots, §3's `ResourceLibrary<T>`, and §2's `PenSample`; libmypaint paints only through the tile adapter.

**Requires:** display-session -- MyPaint strokes and the dialog need an interactive desktop

- [ ] Build libmypaint 1.6.1 (ISC) and json-c (MIT) for `win-x64` and `win-arm64` with `tools/native/libmypaint/build.ps1`, recording the SHA-256 and compiler in `SOURCE.txt`, binaries under `src/Pinxit/Isotone.Pinxit.Core/runtimes/<rid>/native/`, and licenses in THIRD-PARTY-NOTICES. Done when: the script produces both RIDs and a clean build copies them to the output. (**Corrected 2026-09-28:** `build/` is gitignored, so the build script and its provenance record are committed under `tools/native/`, with intermediate output under `build/native/`.)
- [ ] Record the libmypaint and json-c dependency with its GPL-3.0 compatibility check as a row in `docs/dev/decisions.md`. Done when: the row exists and names both licenses.
- [ ] Add `[LibraryImport("libmypaint")]` bindings in `Painting/MyPaint/Native/` for brush creation, settings, `mypaint_brush_stroke_to` with the 2.0 variant taking barrel rotation, and surface callbacks. Done when: `MyPaintNativeTests` create and destroy a brush with no leak over 1,000 iterations.
- [ ] Add `MyPaintSurfaceAdapter` implementing `MyPaintSurface2` `draw_dab` and `get_color` over Pinxit's 256 px tiles, converting libmypaint's 15-bit fixed-point premultiplied RGBA per tile inside one tile-snapshot stroke. Done when: `MyPaintStrokeTests` paint one dab and the tile pixels equal the converted fixed-point values within 1/255.
- [ ] Add MYB loading: JSON version 3 settings and input curves with the `_prev.png` preview, including MyPaint 2.0 settings (barrel rotation input, pigment, posterize, gridmap) (IP-0788, IP-0789). Done when: `MybLoaderTests` load MYB fixtures authored in MyPaint 2.0 (CC0) with every setting equal to the file. Cheaper substitute: translating MYB into Pinxit tip settings.
- [ ] Refuse an unsupported or corrupt MYB file by name. Done when: `MybLoaderTests` feed a truncated file and assert the refusal text.
- [ ] Add the MyPaint Brush tool options: radius, opacity, base opacity, hardness, gain (pressure gain), smooth stroke, erase, no erasing, and follow view zoom and rotation (IP-0790). Done when: `MyPaintToolOptionsTests` read each option's settings key and pass it to the brush.
- [ ] Add the MyPaint Brushes dialog on `ResourceLibrary<T>` over `%LOCALAPPDATA%\Rizonesoft\Pinxit\MyPaintBrushes\`: grid and list, tags, refresh, copy location, and show in folder; no brush pack is bundled (IP-0791). Done when: a capture of the dialog is committed and `MyPaintBrushesViewModelTests` list an imported brush.
- [ ] Seed libmypaint's random state per stroke and store the seed in the stroke command. Done when: `MyPaintStrokeTests` replay a stroke twice byte-identically.
- [ ] Record the undo name "MyPaint Brush" and log one Information line per stroke in §1's format. Done when: a driven stroke quotes its line.
- [ ] Commit the MYB fixtures and a GIMP 3.2.6 MyPaint golden (same brush and seed) under `tests/fixtures/pinxit/painting/mypaint/` with `reference.txt`. Done when: the fixture README names each file.
- [ ] Update `docs/user/pinxit/brushes.md` with MyPaint brushes. Done when: every option is documented.
- [ ] Commit: `"pinxit: MyPaint brushes on libmypaint"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~MyPaintStrokeTests|FullyQualifiedName~MybLoaderTests|FullyQualifiedName~MyPaintNativeTests"` exits 0, and the replayed stroke matches GIMP 3.2.6's MyPaint Brush output with the same brush and seed within 2/255 mean. Cheaper substitute that fails: translating MYB into Pinxit tip settings, which the golden rejects on a smudging MYB brush.

## 5. Painting Tools and History Brushes

Every paint tool and every retouch tool reads the same options, so they must be one model or they drift apart. This section adds `PaintToolOptions`, the pencil, pixel, airbrush, and ink tools, the painting conveniences (straight lines, number keys, temporary picker, on-canvas size), HDR painting, the non-paintable layer policy, and the history, undo, and art history brushes. Catalog: IP-0792 to IP-0813 (22 features).

**Fidelity:** Pinxit painting tools, history brushes, and their options bars -- docs/design/components/ (OptionsBar, ToolRail, Canvas, Slider, NumberBox, ComboBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/main-window/, docs/captures/golden/pinxit/paint-tools/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/ToolRail/README.md, docs/design/components/Canvas/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a painter gets every paint tool and shortcut they rely on, with one consistent options model. Consumer: the target layer's tiles and every `D03 T13` brush-based tool that binds the same options.
**Treatment:** one `PaintToolOptions` rendered on each tool's options bar, the GIMP ink blob editor, and the History panel source marker for the history brush. Cheaper substitute that fails the checkpoint: each tool with its own partial copy of options.
**Chrome:** consume §1 and §2, the `D03 T03 §2` history and `D03 T08 §6` snapshots, and `D03 T11 §9`'s temporary eyedropper; do not duplicate option controls per tool.

**Requires:** display-session -- the tools, shortcuts, and captures need an interactive desktop

- [ ] Add `PaintToolOptions` in `Painting/Tools/` with blend mode including Behind, Clear, and Overwrite from `D03 T09 §6`, opacity, flow, and force (GIMP brush gain) (IP-0809). Done when: `PaintToolOptionsTests` serialize one model per tool and each blend mode reaches the compositor.
- [ ] Add lock brush to view, incremental, hard edge, smooth stroke, jitter, and dynamics to `PaintToolOptions` (IP-0810). Done when: `PaintToolOptionsTests` assert incremental changes the stroke's accumulation.
- [ ] Add expand layers (amount; fill with transparency, background, foreground, or pattern; fill the layer mask with white or black) (IP-0793, IP-0794, IP-0795). Done when: `PaintToolOptionsTests` paint past a layer's bounds and the layer grows by the set amount with the chosen fill.
- [ ] Add Affinity's width, hardness, force pressure, and brush editor button to the options bar (IP-0796, IP-0797, IP-0811). Done when: a capture of the options bar is committed and `PaintToolOptionsTests` read each key.
- [ ] Bind every paint tool of this file and every `D03 T13` brush-based tool to the one `PaintToolOptions` view. Done when: `grep -rn "class .*OptionsView" src/Pinxit/Isotone.Pinxit.Desktop/Tools` finds one paint options view. Cheaper substitute: per-tool partial copies of options.
- [ ] Add straight and constrained lines: Shift+click draws a line from the last point and Ctrl+Shift constrains to 15 degree steps (GIMP) (IP-0798). Done when: `StraightLineTests` assert the constrained angle.
- [ ] Wire `D03 T11 §9`'s `TemporaryEyedropperModifier` (Alt, and Ctrl in GIMP's keymap) into every paint tool (IP-0799). Done when: `TemporaryEyedropperTests` sample with Alt in each paint tool.
- [ ] Add on-canvas size and hardness through §1's HUD with arrow keys rotating the nozzle angle (IP-0800), and number keys setting opacity with Shift+number setting flow (IP-0801). Done when: `PaintShortcutTests` press 5 and Shift+3 and assert opacity 50 percent and flow 30 percent.
- [ ] Add HDR painting: on 32-bit float documents dabs blend in float and keep values above 1.0 supplied by the `D03 T11 §9` intensity slider; HDR preview is `D03 T15 §4` (IP-0802). Done when: `HdrPaintingTests` paint intensity 2 and read 2.0 back from the tile.
- [ ] Add the non-paintable layer policy `Pinxit.Painting.OnNonPixelLayer` (`NewLayerAbove` as Affinity, `AskRasterize` as Photoshop, `Refuse`), never rasterizing text, link, or vector layers silently (IP-0803). Done when: `NonPixelLayerPolicyTests` assert each value on a text layer.
- [ ] Add the Pencil and Pixel tool: aliased coverage, Auto Erase (starting on the foreground color paints the background), and Affinity's alternate modifier to erase, paint the background color, or undo from the snapshot (IP-0804, IP-0813). Done when: `AutoEraseTests` start on the foreground color and paint the background color.
- [ ] Add the Airbrush tool (GIMP): rate, flow, and motion only on §1's build-up (IP-0805). Done when: `AirbrushToolTests` assert motion only stops dabs while the pen rests.
- [ ] Add the Ink tool (GIMP): size, angle, sensitivity to size, tilt, and speed, nib type circle, square, or diamond, and the blob shape editor, rendered as GIMP's convex blob hull between samples (IP-0806). Done when: `InkBlobTests` compare a recorded stroke against the GIMP 3.2.6 golden within 1/255.
- [ ] Add the history brush and undo brush: source a history state (`D03 T03 §2`) or a snapshot (`D03 T08 §6`) marked in the History panel, reconstructing only the tiles under the dab, with blend mode and protect alpha (IP-0792, IP-0807). Done when: `HistoryBrushTests` paint from an earlier state and only pixels under the stroke are restored. Cheaper substitute: reverting the whole layer.
- [ ] Add the Art History brush: styles Tight Short, Tight Medium, Tight Long, Loose Medium, Loose Long, Dab, Tight Curl, and Loose Curl, area, and tolerance, generating seeded strokes that sample the source state's color (IP-0808). Done when: `ArtHistoryBrushTests` produce byte-identical output from the same seed.
- [ ] Map protect alpha onto the `D03 T09 §1` transparency lock, one flag not a second lock (IP-0812). Done when: `PaintToolOptionsTests` toggle protect alpha and the layer's lock state changes.
- [ ] Record undo names per tool ("Pencil", "Ink", "History Brush") and log one Information line per stroke in §1's format. Done when: a driven history-brush stroke quotes its line.
- [ ] Update `docs/user/pinxit/painting.md` with the shared options, each paint tool, the painting shortcuts, HDR painting, and the history brushes. Done when: every control is documented.
- [ ] Commit: `"pinxit: shared paint options, pencil, pixel, airbrush, ink, and history brushes"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~PaintToolOptionsTests|FullyQualifiedName~AutoEraseTests|FullyQualifiedName~HistoryBrushTests|FullyQualifiedName~InkBlobTests|FullyQualifiedName~NonPixelLayerPolicyTests"` exits 0, and a driven history-brush stroke over a filtered region restores the pre-filter pixels under the stroke (region hash quoted) while pixels outside keep the filter. Cheaper substitute that fails: a history brush that reverts the whole layer, which the outside-region hash catches.

## 6. Mixer Brush, Smudge, and Color Replacement

Wet paint blends on the canvas, and recoloring keeps texture. This section adds Photoshop's Mixer Brush and Affinity's paint mixer brush with RGB and pigment mixing (the pigment path through `D03 T09 §6`'s Kubelka-Munk kernel, not a second mixer), the smudge options of all three apps, and the color replacement tools with sampling and limits on the `D03 T10 §3` flood engine. Catalog: IP-0814 to IP-0822 (9 features).

**Fidelity:** Pinxit mixer brush, smudge, and color replacement options bars -- docs/design/components/ (OptionsBar, ToolRail, Swatches, Slider, NumberBox, Canvas), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/main-window/, docs/captures/golden/pinxit/mixer/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/ToolRail/README.md, docs/design/components/Swatches/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a painter can blend wet paint on canvas and recolor areas while keeping texture. Consumer: the target layer's tiles.
**Treatment:** options bars with reservoir and pickup previews and mixing presets. Cheaper substitute that fails the checkpoint: a smudge that blurs.
**Chrome:** consume §5's `PaintToolOptions`, §1's engine, and the `D03 T10 §3` flood engine for replacement limits.

**Requires:** display-session -- wet mixing strokes need an interactive desktop

- [ ] Add `MixerBrush` (Photoshop): reservoir and pickup buffers per stroke, wet, load, mix, flow, sample all layers, and load and clean after each stroke (IP-0816). Done when: `MixerBrushTests` assert clean after stroke empties the reservoir and wet 0 behaves like the brush.
- [ ] Add the Mixer Brush blend presets (Dry, Moist, Wet, Very Wet and their load and mix variants) as data (IP-0817). Done when: `MixerBrushTests` load each preset and assert its wet, load, and mix values.
- [ ] Add the paint mixer brush (Affinity): strength, load, clean, auto load, auto clean, and mixing model RGB or Pigment (IP-0822). Done when: `MixerBrushTests` assert auto clean empties the reservoir between strokes.
- [ ] Blend the Pigment mixing model through `D03 T09 §6`'s Pigment mode kernel (IP-0327); Mixbox stays rejected (CC BY-NC 4.0 is not GPL-3.0 compatible) (IP-0818). Done when: `PigmentMixingTests` mix blue and yellow to green through the shared kernel while RGB gives gray, and `grep` finds no second Kubelka-Munk implementation. Cheaper substitute: RGB averaging labeled pigment.
- [ ] Add Smudge with GIMP's strength, rate, flow, no erasing effect, and sample merged (IP-0819). Done when: `SmudgeTests` compare a recorded stroke against the GIMP 3.2.6 smudge golden within 2/255. Cheaper substitute: a smudge that blurs.
- [ ] Add Photoshop's smudge strength, mode, finger painting, and sample all layers, and Affinity's smudge options, with §7's shared hard edge option (IP-0820). Done when: `SmudgeTests` assert finger painting deposits the foreground at stroke start.
- [ ] Add color replacement with modes hue, saturation, color, and luminosity (IP-0814). Done when: `ColorReplacementTests` replace a red with blue and keep the luminance texture within 1/255.
- [ ] Add color replacement sampling continuous, once, or background swatch, limits discontiguous, contiguous, or find edges through the `D03 T10 §3` flood engine bounded to the dab region, tolerance, and anti-alias (IP-0815, IP-0821). Done when: `ColorReplacementTests` assert the contiguous limit stops at an edge.
- [ ] Set the budget: mixer strokes at 0 B per dab and within 1.5 times §1's benchmark time. Done when: `DabAllocationTests` and `BrushEngineBenchmarks` quote both for the mixer.
- [ ] Record undo names "Mixer Brush", "Smudge", and "Color Replacement" and log one Information line per stroke. Done when: a driven pigment mix quotes its line.
- [ ] Update `docs/user/pinxit/painting.md` with the mixer brushes, smudge, and color replacement. Done when: every control is documented.
- [ ] Commit: `"pinxit: mixer brush, pigment mixing, smudge, and color replacement"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~MixerBrushTests|FullyQualifiedName~PigmentMixingTests|FullyQualifiedName~ColorReplacementTests|FullyQualifiedName~SmudgeTests"` exits 0, and a driven pigment mix of blue into yellow is captured beside the RGB mix under docs/captures/pinxit/mixer/. Cheaper substitute that fails: RGB averaging labeled pigment, which the blue-plus-yellow hue assertion catches.

## 7. Erasers

Removing pixels by brush, by color, or by region, and bringing them back, is its own tool family. This section adds eraser modes, erase to history, GIMP's anti-erase, the background eraser and Affinity's background erase brush, and the magic eraser and flood erase on the `D03 T10 §3` flood engine. Catalog: IP-0823 to IP-0831 (9 features).

**Fidelity:** Pinxit eraser tools and their options bars -- docs/design/components/ (OptionsBar, ToolRail, Slider, NumberBox, ComboBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/main-window/, docs/captures/golden/pinxit/erasers/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/ToolRail/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can remove pixels by brush, by color, or by region, and bring them back. Consumer: the target layer's alpha.
**Treatment:** eraser options bars and the anti-erase modifier. Cheaper substitute that fails the checkpoint: an eraser that paints white.
**Chrome:** consume §5's options and history source, and the `D03 T10 §3` flood engine.

**Requires:** display-session -- eraser strokes need an interactive desktop

- [ ] Add eraser modes brush, pencil, and block with flow, airbrush, and smoothing (Photoshop) (IP-0823). Done when: `EraserModeTests` assert block mode erases a square of the set size.
- [ ] Add the shared hard edge option for eraser and smudge (GIMP) (IP-0829). Done when: `EraserModeTests` assert hard edge leaves only 0 and full alpha.
- [ ] Add Erase to History through §5's history brush source (IP-0824). Done when: `EraseToHistoryTests` restore a painted-over region from the source state under the stroke only.
- [ ] Add anti-erase (GIMP, Alt): because Pinxit stores premultiplied pixels, colors under erased alpha come from the most recent history state where the pixel was visible (bounded by the history limit), documented in the tool's help (IP-0828). Done when: `AntiEraseTests` erase then anti-erase and the colors restore byte-equal. Cheaper substitute: raising alpha on black.
- [ ] Add the background eraser: tolerance, protect foreground color, sampling continuous, once, or background swatch, and limits discontiguous, contiguous, or find edges (IP-0825, IP-0826). Done when: `BackgroundEraserTests` assert protect foreground keeps the protected color.
- [ ] Add Affinity's background erase brush options on the same engine (IP-0830). Done when: `BackgroundEraserTests` run the Affinity option set on the same fixture.
- [ ] Add the magic eraser and flood erase: tolerance, anti-alias, contiguous, sample all layers, and opacity, through the `D03 T10 §3` flood engine (IP-0827, IP-0831). Done when: `MagicEraserTests` compare against a GIMP 3.2.6 fuzzy-select-and-clear golden within 1/255.
- [ ] Keep the `D03 T03 §6` rule that background layers without alpha erase to the background color. Done when: `EraserModeTests` erase on a background layer and read the background color.
- [ ] Record undo names "Eraser", "Background Eraser", and "Magic Eraser" and log one Information line per stroke or erase. Done when: a driven magic erase quotes its line.
- [ ] Update `docs/user/pinxit/painting.md` with the eraser family. Done when: every control is documented.
- [ ] Commit: `"pinxit: eraser modes, anti-erase, background eraser, and magic eraser"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~AntiEraseTests|FullyQualifiedName~MagicEraserTests|FullyQualifiedName~BackgroundEraserTests|FullyQualifiedName~EraserModeTests"` exits 0. Cheaper substitute that fails: anti-erase that raises alpha on black, which the byte-equal color restore in `AntiEraseTests` catches.

## 8. Fill and Stroke

Filling and outlining selections and regions is daily work, and GIMP's line-art fill is the tool flat colorists pick GIMP for. This section adds the Fill dialog and default fill shortcuts, Affinity's matte fill, scripted pattern fills as native generators, paint bucket extensions, the line-art bucket fill, and Stroke Selection with location, line styles, and stroking with a paint tool. Catalog: IP-0846 to IP-0860 (15 features).

**Fidelity:** Pinxit Fill and Stroke dialogs -- docs/design/components/ (Dialog, ComboBox, Slider, NumberBox, Swatches, Tabs, Progress), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/fill-stroke/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Swatches/README.md, docs/design/components/Tabs/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can fill and outline selections and regions with any content, including flat coloring of line art. Consumer: the target layer's tiles.
**Treatment:** modal Fill and Stroke dialogs, bucket options on the options bar, and GIMP's Stroke Selection dialog with Line and Paint Tool tabs. Cheaper substitute that fails the checkpoint: a bucket that floods from one layer with an RGB tolerance only.
**Chrome:** consume `D03 T10 §1` selections, the `D03 T10 §3` flood engine, `D03 T10 §8` border morphology, §5's paint tools, and §10's patterns when present; do not add a second flood fill.

**Requires:** display-session -- the dialogs and bucket fills need an interactive desktop

- [ ] Add `FillDialog.xaml` and `FillCommand`: contents Foreground, Background, Color, Pattern (§10), History, Black, 50 Percent Gray, and White, blending mode, opacity, and preserve transparency, as one "Fill" step (IP-0849, IP-0853). Done when: `FillDialogTests` fill with each content and assert preserve transparency keeps alpha.
- [ ] List Content-Aware (Affinity's inpainting) in the Fill dialog through `D03 T13 §3`, disabled with the tooltip "Planned: D03 T13 §3" until that section registers its engine (IP-0846). Done when: `FillDialogTests` assert the disabled entry and tooltip while no engine is registered.
- [ ] Add the default fills: Alt+Backspace foreground, Ctrl+Backspace background, Shift+Backspace the dialog, and Shift adding preserve transparency (IP-0860). Done when: `FillShortcutTests` assert each shortcut's fill.
- [ ] Add Matte (Affinity): fill transparent areas with a color behind existing pixels (IP-0847). Done when: `FillDialogTests` matte a half-transparent fixture and opaque pixels stay unchanged.
- [ ] Add scripted patterns Brick Fill, Cross Weave, Random Fill, Spiral, Symmetry Fill, and Frame as seeded native generators in `Painting/Fill/ScriptedPatterns/` (scripting itself is `D01 T10 §4`, in Pinxit `D03 T22 §2`) (IP-0854). Done when: `ScriptedPatternTests` produce byte-identical output per generator from the same seed.
- [ ] List Place Along Path disabled with the tooltip "Planned: D03 T16 §5" until that section registers paths. Done when: `ScriptedPatternTests` assert the disabled entry.
- [ ] Extend the paint bucket: source foreground, background, or pattern, mode and opacity, anti-alias, tolerance, contiguous, and all layers or chosen source layers through `D03 T10 §3`'s `SampleSource` (IP-0848). Done when: `BucketFillTests` fill from the composite and from a picked layer with different regions. Cheaper substitute: an RGB tolerance flood on one layer.
- [ ] Add Fill Whole Selection and Fill Similar Colors on `D03 T10 §3`'s `FloodSelector` (IP-0851, IP-0859). Done when: `BucketFillTests` fill every same-color region with Fill Similar Colors.
- [ ] Add the line-art fill (GIMP): line art detection by threshold with the source layer choice, maximum gap length, automatic closure by splines and segments, and fill borders, after Fourey et al. 2018 (IP-0852). Done when: `LineArtFillTests` close a 5 px gap at maximum gap 6 and not at 4.
- [ ] Cache the line-art detection until the source changes; budget: detection on a 24-megapixel line drawing under 1.5 seconds, with progress on the status strip and a completion notification for runs over one second, and Cancel. Done when: `LineArtFillTests` quote the time and assert the second fill reuses the cache.
- [ ] Add Stroke Selection (Photoshop): width, color, location inside, center, or outside, blending, opacity, and preserve transparency, through `D03 T10 §8` border morphology (IP-0850, IP-0855). Done when: `StrokeSelectionTests` assert location inside keeps every stroked pixel inside the mask.
- [ ] Add Stroke with a line style (GIMP): width, cap, join, miter limit, a dash pattern with presets, and antialiasing, rendering the selection boundary contour through SkiaSharp's stroker into the target tiles (IP-0856). Done when: `StrokeSelectionTests` compare a dashed stroke against the GIMP 3.2.6 golden within 1/255.
- [ ] Add Stroke with a paint tool (GIMP): the boundary contour as a synthetic stroke through any §5 tool with Emulate Brush Dynamics (pressure ramps in and out) (IP-0857). Done when: `StrokeSelectionTests` assert the emulated pressure ramp on the synthetic stroke.
- [ ] Add Fill Selection Outline (GIMP), with fill path and stroke path becoming available when `D03 T16 §5` registers paths (IP-0858). Done when: `FillDialogTests` fill a selection outline and assert the path commands' disabled tooltip names `D03 T16 §5`.
- [ ] Record undo names "Fill", "Bucket Fill", and "Stroke Selection" and log one Information line per fill and stroke. Done when: a driven line-art fill quotes its line.
- [ ] Commit the line-art fixtures and GIMP 3.2.6 goldens under `tests/fixtures/pinxit/fill/lineart/` with `reference.txt`. Done when: `LineArtFillTests` compare the golden within 1/255.
- [ ] Update `docs/user/pinxit/painting.md` with the Fill and Stroke dialogs, scripted patterns, the bucket options, and line-art fill. Done when: every control is documented.
- [ ] Commit: `"pinxit: the Fill and Stroke dialogs, scripted patterns, bucket extensions, and line-art fill"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~LineArtFillTests|FullyQualifiedName~StrokeSelectionTests|FullyQualifiedName~FillDialogTests|FullyQualifiedName~BucketFillTests|FullyQualifiedName~ScriptedPatternTests"` exits 0, with the line-art fill golden matching GIMP 3.2.6 within 1/255. Cheaper substitute that fails: a tolerance flood on line art, which leaks through the 5 px gap and fails the gap test.

## 9. Gradients and the Gradient Editor

Gradients are shared with Stilus through the model `D03 T09 §8` moves to `src/Isotone.Core/Paint/Gradients/`; this section extends that model with GIMP's segment model and builds the gradient tool with every shape, interpolation, and option, on-canvas stop editing, live gradient fill layers and gradients on masks, the Photoshop and GIMP editors, noise and diffusion gradients, the transparency tool, bitmap fills, a Gradients panel, and GGR, SVG, GRD, CSS, and POV-Ray exchange. Pinxit keeps no second sampler. Catalog: IP-0861 to IP-0881 (21 features).

**Fidelity:** Pinxit gradient tool, on-canvas stops, gradient editor, and Gradients panel -- docs/design/components/ (OptionsBar, ToolRail, Canvas, Dialog, Panel, ListTree, Swatches, Slider), plus the new `docs/design/components/GradientEditor/` spec this section writes first, per standards/design-contract.md; goldens under docs/captures/golden/pinxit/main-window/, docs/captures/golden/pinxit/gradients/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/ToolRail/README.md, docs/design/components/Canvas/README.md, docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Swatches/README.md, docs/design/components/Slider/README.md, new surface: docs/design/components/GradientEditor/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can build any gradient any of the three apps can, edit it on the canvas, and keep it live. Consumer: the target layer, a gradient fill layer, or a mask.
**Treatment:** a gradient line with draggable stops and midpoints, a gradient editor dialog with color and opacity stops, smoothness, and GIMP's segment operations, and a Gradients panel. Cheaper substitute that fails the checkpoint: a two-stop linear and radial tool.
**Chrome:** consume the `Isotone.Core` gradient model moved by `D03 T09 §8`, `D01 T03 §3` dithers, and the fill-layer contract of `D03 T08 §1`; do not keep a second sampler in Pinxit.

**Requires:** display-session -- on-canvas editing and the editor need an interactive desktop

- [ ] Write the design spec `docs/design/components/GradientEditor/README.md` and its `preview.html` card for the gradient editor (ramp, color and opacity stops, midpoints, segment editing, on-canvas stop handles): anatomy, every state, tokens, and sizes, with the design page regenerated by `python scripts/build-design-site.py`, before any XAML for it is written. Done when: the spec and its card exist and `python scripts/build-design-site.py --check` passes.
- [ ] Extend `GradientDefinition` in `src/Isotone.Core/Paint/Gradients/` with `GradientSegment { Left, Middle, Right, LeftColor, RightColor, EndpointColorType (Fixed, Foreground, ForegroundTransparent, Background, BackgroundTransparent), Blending (Linear, Curved, Sinusoidal, SphericalIncreasing, SphericalDecreasing, Step), Coloring (Rgb, HsvCcw, HsvCw) }`, mapping Stilus's stops to linear segments. Done when: Stilus's gradient tests stay green and `GradientSegmentTests` compare each blending function against the GIMP 3.2.6 golden within 1/255.
- [ ] Add interpolation and blend color space Perceptual, Linear, Classic, Smooth, and Stripes (Photoshop) and GIMP's perceptual RGB, linear RGB, and CIE Lab (IP-0869). Done when: `GradientGoldenTests` compare perceptual and Lab blends against their goldens. Cheaper substitute: sampling stops linearly in sRGB only.
- [ ] Add `GradientEvaluator` in `src/Pinxit/Isotone.Pinxit.Core/Painting/Gradients/GradientEvaluator.cs`, rendering a `GradientDefinition` over a shape into tiles (`D01 T06 §13` moves it to `Isotone.Core` as its second consumer), with the shapes linear, radial, angle, reflected, diamond, bi-linear, square, shaped (angular, spherical, dimpled from the selection's distance transform), conical symmetric and asymmetric, and spiral clockwise and counterclockwise (IP-0868). Done when: `GradientGoldenTests` compare every shape against the GIMP 3.2.6 gradient tool within 1/255.
- [ ] Add options reverse, transparency, mode and opacity, repeat none, sawtooth, triangular, or truncate, offset, and adaptive supersampling (max depth, threshold) (IP-0870). Done when: `GradientGoldenTests` compare every repeat mode against its golden.
- [ ] Add dither through `D01 T03 §3` with the preference `Pinxit.Gradients.Dither` (IP-0881). Done when: `GradientDitherTests` show no band longer than the golden's on an 8-bit ramp with dither on.
- [ ] Add on-canvas editing: stops, midpoints, and opacity on the gradient line, GIMP's instant mode and modify active gradient, and the 15 degree angle constraint (IP-0861, IP-0871). Done when: a driven edit drags a stop and the gradient updates live (capture).
- [ ] Add Affinity's rotate, reverse, aspect, and fill or stroke context on any layer kind, with stroke applying to shape layers once `D03 T16 §7` ships (IP-0879). Done when: `GradientContextTests` assert the stroke context is disabled with that section named while no shape layers exist.
- [ ] Add the gradient fill layer as `<pinxit:fill kind="gradient" v="1">` with the gradient and geometry as parameters and a rendered PNG fallback, re-editable on canvas (IP-0866). Done when: `GradientFillLayerTests` reopen a gradient fill layer live with parameters equal.
- [ ] Add live gradients on fill layers, layer masks, and adjustment layer masks (IP-0867). Done when: `GradientFillLayerTests` edit a live gradient mask and the masked composite updates.
- [ ] Add the gradient editor dialog with Photoshop color and opacity stops, stop types, smoothness, preview, and zoom (IP-0874). Done when: a capture of the editor is committed and `GradientEditorViewModelTests` add, move, and delete stops.
- [ ] Add GIMP's endpoint color types, color slots, drag colors, blending functions, and coloring type to the editor (IP-0876, IP-0877). Done when: `GradientEditorViewModelTests` set a Foreground endpoint and the gradient follows a foreground change.
- [ ] Add GIMP's segment operations flip, replicate, split at midpoint, split uniformly, delete, recenter midpoint, redistribute, and blend endpoint colors and opacity (IP-0878). Done when: `GradientSegmentTests` assert each operation's resulting segments.
- [ ] Add noise gradients (Photoshop): roughness, color model RGB, HSB, or Lab, restrict colors, add transparency, and randomize with a stored seed (IP-0875). Done when: `NoiseGradientDeterminismTests` produce byte-identical gradients from the same seed.
- [ ] Add the diffusion gradient fill (Affinity): colors at control points diffused by a multigrid Laplace solve (after Orzan et al. 2008) with progress and Cancel; budget: 4,000 by 4,000 under 2 seconds (IP-0862). Done when: `DiffusionGradientTests` reproduce the control colors exactly and quote the time.
- [ ] Add the transparency tool (Affinity): a transparency gradient on the layer's opacity with its own editor, written as a live gradient mask (IP-0863). Done when: `GradientFillLayerTests` reopen a transparency gradient live.
- [ ] Add the bitmap fill (Affinity): fill type Bitmap with extend none, repeat, reflect, or pad, quality, and scale with object, sharing §10's tiled image renderer (IP-0880). Done when: `BitmapFillTests` assert each extend mode at the fill's edge.
- [ ] Add the Gradients panel on `ResourceLibrary<T>` over `%LOCALAPPDATA%\Rizonesoft\Pinxit\Gradients\` (where `D03 T11 §10` writes palette gradients) with groups, import, export, legacy sets, picker, save preset, tags, grid and list, new, duplicate, delete, refresh, and copy location (IP-0864, IP-0872). Done when: `GradientsPanelViewModelTests` list a palette gradient and a capture is committed.
- [ ] Add GIMP GGR read and write and SVG `<linearGradient>` and `<radialGradient>` load (IP-0865). Done when: `GgrRoundTripTests` round-trip GGR fixtures byte-equal and an SVG fixture's stops load equal.
- [ ] Add Photoshop GRD import (descriptor structure, GIMP 3.2.6's GRD loader as oracle) and export as CSS and POV-Ray (IP-0873). Done when: `GrdImportTests` load a GRD fixture with stops equal to GIMP's import and the CSS export parses as a valid `linear-gradient()`.
- [ ] Refuse an unsupported or corrupt gradient file by name. Done when: `GrdImportTests` feed a truncated GRD and assert the refusal text.
- [ ] Record undo names "Gradient", "New Gradient Fill Layer", and "Edit Gradient" and log one Information line per gradient apply and library change. Done when: a driven gradient quotes its line.
- [ ] Commit the goldens against GIMP 3.2.6's gradient tool for every shape, repeat mode, and blending function under `tests/fixtures/pinxit/gradients/` with `reference.txt`. Done when: the fixture README names each golden.
- [ ] Update `docs/user/pinxit/gradients.md` with the tool, shapes, options, on-canvas editing, fill layers, the editors, noise and diffusion gradients, and files. Done when: every control is documented.
- [ ] Commit: `"pinxit: gradient shapes, the gradient editors, live gradient fills, and gradient files"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~GradientGoldenTests|FullyQualifiedName~GradientSegmentTests|FullyQualifiedName~GgrRoundTripTests|FullyQualifiedName~GrdImportTests|FullyQualifiedName~NoiseGradientDeterminismTests|FullyQualifiedName~GradientFillLayerTests"` exits 0; every shape, repeat mode, and blending-function golden matches GIMP 3.2.6 within 1/255 and GGR files round-trip byte-equal. Cheaper substitute that fails: sampling stops linearly in sRGB only, which the perceptual and GIMP spherical-blending goldens reject.

## 10. Patterns

Patterns come from every source a user has: Photoshop and GIMP PAT files, CAD hatches, any image, and tiles they paint themselves. This section implements `D03 T09 §8`'s `IPatternLibrary` with a full library on §3's `ResourceLibrary<T>`, replacing that interface's first implementation, and adds the Patterns panel, Define Pattern and clipboard patterns, PAT and hatch import, live pattern fill layers and tiled bitmap fills, Affinity's pattern layer with live tile painting, pattern preview, and the pattern stamp. Catalog: IP-0882 to IP-0896 (15 features).

**Fidelity:** Pinxit Patterns panel and pattern preview -- docs/design/components/ (Panel, ListTree, Dialog, Swatches, Canvas), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/patterns/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Dialog/README.md, docs/design/components/Swatches/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can collect patterns from any source, fill with them live, and design seamless tiles by painting across edges. Consumer: pattern fill layers, bitmap fills, brush texture (§2), the Fill dialog (§8), and the pattern stamp.
**Treatment:** a Patterns panel, a pattern fill layer with scale and angle, Affinity's pattern layer, and View, Pattern Preview. Cheaper substitute that fails the checkpoint: a fill that stamps a pattern once as pixels.
**Chrome:** consume §3's `ResourceLibrary<T>`, `D03 T09 §8`'s `IPatternLibrary`, §8's fill paths, and the `D03 T08 §1` contract; do not add a second resource store.

**Requires:** display-session -- the panel, tile painting, and pattern preview need an interactive desktop

- [ ] Add `PatternLibrary` implementing `D03 T09 §8`'s `IPatternLibrary` on `ResourceLibrary<PatternResource>` over `%LOCALAPPDATA%\Rizonesoft\Pinxit\Patterns\`, replacing that interface's first implementation. Done when: `PatternLibraryTests` resolve a PSD-embedded pattern id and a library pattern through the one interface.
- [ ] Add the Patterns panel and GIMP's patterns dialog: groups, import, export, legacy sets, grid and list, tags, duplicate, delete, refresh, open as image, copy location, and show in folder (IP-0883, IP-0892, IP-0896). Done when: `PatternsPanelViewModelTests` assert each command on a temporary library and a capture is committed.
- [ ] Add Define Pattern from the selection or document (IP-0885). Done when: `PatternLibraryTests` define a pattern whose tile equals the selection's pixels.
- [ ] Add Paste as New Pattern and the clipboard pattern (GIMP) (IP-0886, IP-0894). Done when: `PatternLibraryTests` paste an image and the clipboard pattern equals it.
- [ ] Add a Photoshop PAT reader in `src/Pinxit/Isotone.Pinxit.FileFormats/Patterns/` (`8BPT` header and pattern blocks per Adobe's specification, psd-tools as oracle), detected by content (IP-0888). Done when: `PatReaderTests` decode operator-authored Photoshop 27.10 fixtures byte-equal to psd-tools' decoded tiles.
- [ ] Add a GIMP PAT reader (`GPAT` per `devel-docs/pat.txt`) and PNG, JPEG, BMP, GIF, and TIFF files as patterns (IP-0893). Done when: `PatReaderTests` decode GIMP 3.2.6 fixtures byte-equal to GIMP's loaded tiles.
- [ ] Add CAD hatch `.pat` definitions (angle, origin, offset, dashes) rasterized into a tile at a chosen scale and line color (Affinity imports these as swatches, Pinxit as patterns) (IP-0889). Done when: `HatchPatternTests` match a 45 degree hatch at spacing 10 against its analytic golden.
- [ ] Refuse an unsupported or corrupt pattern file by name. Done when: `PatReaderTests` feed a truncated PAT and assert the refusal text.
- [ ] Add the pattern fill layer (Photoshop) as `<pinxit:fill kind="pattern" v="1">` with the pattern id (the tile embedded under `data/patterns/`), scale, angle, link with layer, and snap to origin (IP-0890). Done when: `PatternFillLayerTests` reopen a pattern fill layer live with parameters and tile equal. Cheaper substitute: a fill that stamps the pattern once as pixels.
- [ ] Add the tiled bitmap fill (Affinity) on the same renderer with Affinity's mapping options (IP-0882). Done when: `PatternFillLayerTests` assert the bitmap fill tiles seamlessly at a 45 degree angle.
- [ ] Add the pattern layer (Affinity): tile from selection, live tile painting where strokes wrap across tile edges, mirror, tile transform, and open the tile as a document, written as `<pinxit:pattern-layer>` (IP-0891). Done when: `TileWrapPaintingTests` assert a stroke crossing the right edge appears on the left.
- [ ] Add View, Pattern Preview showing the document tiled 3 by 3 and wrapping painting across the canvas edges, as `Pinxit.View.PatternPreview` (IP-0884, IP-0887). Done when: `TileWrapPaintingTests` paint across the canvas edge in preview and the wrapped pixels appear.
- [ ] Add the Pattern Stamp tool (Photoshop) with Aligned and Impressionist (seeded jittered sampling) on §5's options (IP-0895). Done when: `PatternStampTests` assert Aligned keeps the pattern phase across two strokes and Impressionist reproduces from the same seed.
- [ ] Record undo names "Define Pattern", "New Pattern Fill Layer", and "Pattern Stamp" and log one Information line per library change and fill. Done when: a driven pattern fill quotes its line.
- [ ] Commit the PAT fixtures (Photoshop PAT authored by the operator in Photoshop 27.10 from Pinxit tiles, GIMP PAT from GIMP 3.2.6, both CC0) and the hatch golden under `tests/fixtures/pinxit/patterns/` with a README naming the source of each. Done when: the README lists every file.
- [ ] Update `docs/user/pinxit/patterns.md` with the library, formats, pattern fill and pattern layers, pattern preview, and the pattern stamp. Done when: every control is documented.
- [ ] Commit: `"pinxit: patterns, pattern fill and pattern layers, pattern preview, and the pattern stamp"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~PatReaderTests|FullyQualifiedName~HatchPatternTests|FullyQualifiedName~TileWrapPaintingTests|FullyQualifiedName~PatternFillLayerTests|FullyQualifiedName~PatternLibraryTests"` exits 0; Photoshop PAT fixtures decode byte-equal to psd-tools' decoded tiles and GIMP PAT fixtures to GIMP 3.2.6's. Cheaper substitute that fails: filling with a pattern baked into pixels, which the live `pinxit:fill` reopen assertion catches.

## 11. Symmetry Painting

Mirrored, radial, and tiled designs are painted in one stroke in all three competitors. This section adds one `SymmetryModel` producing per-dab transforms for every competitor's mode, with axis count, mirror, and a lockable center, shared by paint brushes and the `D03 T13` retouch brushes and persisted in the document. Catalog: IP-0832 to IP-0837 (6 features).

**Fidelity:** Pinxit symmetry painting guides and options -- docs/design/components/ (OptionsBar, ToolRail, Canvas, Menu, NumberBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/symmetry/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/ToolRail/README.md, docs/design/components/Canvas/README.md, docs/design/components/Menu/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a painter can paint mirrored, radial, and tiled designs in one stroke. Consumer: §5's paint pipeline and every `D03 T13` brush-based tool.
**Treatment:** a symmetry menu on the options bar, on-canvas axis guides with a draggable, lockable center, and show or hide. Cheaper substitute that fails the checkpoint: mirroring the finished stroke as a layer copy.
**Chrome:** consume §5's paint pipeline and the overlay; retouch tools of `D03 T13` read the same `SymmetryModel`.

**Requires:** display-session -- symmetric strokes and guides need an interactive desktop

- [ ] Add `SymmetryModel` in `Painting/Symmetry/` producing per-dab transforms for vertical, horizontal, dual axis, diagonal, wavy (sine displacement), circle, spiral, parallel lines, and central mirror (IP-0832). Done when: `SymmetryModelTests` map a point to the analytic set for every mode. Cheaper substitute: mirroring the finished stroke as a layer copy.
- [ ] Add show or hide guides and on-canvas axis guides with a draggable center on the overlay (IP-0832). Done when: a capture of each mode's guide overlay is committed.
- [ ] Add radial and mandala: segment count 2 to 32, mirror within segments, kaleidoscope, and a lockable center (Photoshop and Affinity axis count, mirror, and lock) (IP-0833, IP-0837). Done when: `SymmetryModelTests` assert mirror parity for even and odd counts and the locked center refuses a drag.
- [ ] Add tiling (GIMP): interval X and Y, shift, and max strokes X and Y (IP-0835). Done when: `SymmetryModelTests` assert the tiling counts.
- [ ] Add symmetry from a custom path (Photoshop) with path transform; the path source lists work paths once `D03 T16 §5` registers them and is disabled with that section named until then (IP-0834). Done when: `SymmetryModelTests` assert the disabled path option names `D03 T16 §5`.
- [ ] Apply symmetry, mirror, and lock center on every `D03 T13` brush-based tool through the same model (Affinity) (IP-0836). Done when: `SymmetryModelTests` resolve the model from the shared `PaintToolOptions`.
- [ ] Interleave the mirrored dabs per input sample so the stroke is symmetric while it is drawn. Done when: `SymmetryStrokeGoldenTests` replay a recorded stroke per mode within 1/255 of goldens captured mid-stroke.
- [ ] Persist `<pinxit:symmetry mode="mandala" count="12" mirror="true" cx="..." cy="..." locked="true"/>` in the document metadata. Done when: `SymmetryPersistenceTests` reopen a document with the setting equal.
- [ ] Set the budget: a 32-way mandala with a 200 px brush keeps 0 B per dab and handles each input event under 16 ms; log one Information line per symmetric stroke (the stroke line plus mode). Done when: `SymmetryBudgetTests` quote the time and 0 B per dab.
- [ ] Update `docs/user/pinxit/painting.md` with symmetry painting. Done when: every mode and option is documented.
- [ ] Commit: `"pinxit: symmetry painting"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~SymmetryModelTests|FullyQualifiedName~SymmetryStrokeGoldenTests|FullyQualifiedName~SymmetryBudgetTests|FullyQualifiedName~SymmetryPersistenceTests"` exits 0, and the 32-way budget test quotes its time and 0 B per dab. Cheaper substitute that fails: mirroring the stroke after it ends, which the live-stroke golden (dabs interleaved per input sample) rejects.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes every stroke, brush, MyPaint, fill, gradient, and pattern fixture this file adds, with each GIMP, Krita, psd-tools, or MyPaint golden's version recorded
- [ ] `DabAllocationTests` quote 0 B per dab for every tip type, the mixer, and a 32-way mandala
- [ ] Every capture named in a Fidelity line exists under `docs/captures/pinxit/`, and every user guide page named in a section exists under `docs/user/pinxit/` **Corrected 2026-09-28:** every golden named in a Fidelity line exists under `docs/captures/golden/pinxit/` (approved through review); driven-run captures under `docs/captures/pinxit/` stay proof 4 evidence only.
- [ ] No second dab rasterizer, flood fill, gradient sampler, pigment mixer, or resource store exists in Pinxit (`grep` over `src/Pinxit` for each, quoted)
- [ ] No Adobe, Affinity, MyPaint, or GIMP brush, gradient, or pattern pack ships in the app resources (a resources README audit), and libmypaint and json-c appear in THIRD-PARTY-NOTICES
- [ ] B-020 is gone from `todo/backlog.md`, and §1 carries its source key
- [ ] Every catalog row IP-0737 to IP-0896 owned by this file is covered by a shipped section, and `docs/parity/pinxit-parity.md` statuses agree
- [ ] `python scripts/todo-claims.py` holds for this file
- [ ] `python scripts/todo-graph.py validate` clean
