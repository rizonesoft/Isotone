---
schema_version: 1
id: nodus-parity-effects
domain: 02-nodus
status: draft
title: "TODO-11 -- Nodus Parity: Interactive and Live Effects"
depends_on: []
track: N11
---

# TODO-11 -- Nodus Parity: Interactive and Live Effects

> **Goal:** Give Nodus every interactive and live vector effect Illustrator 30.8 and CorelDRAW 2026 users reach for (blend, contour, envelope and warp, distortion, shadows, glows and bevels, classic and modern 3D, lenses, PowerClip, symmetry, perspective, puppet warp, Live Paint and smart fill, repeats, and path effects), each one a live object under the live-object contract (`D02 T07 §1`) that sits in the Appearance stack (`D02 T09 §14`), renders through SkiaSharp at draw time (shadows and glows as Skia image filters, never through the Phase 9 pixel engine), expands to plain SVG geometry, survives a save and reopen as the same editable effect, and is undone by one step of the suite history. When this file closes, every catalog feature in `docs/parity/nodus-parity.md` whose status is `plan D02 T11 §N` (NP-1432 to NP-1726, 295 features) is shipped, which serves the acceptance-bar aim "Nodus covers every CorelDRAW and Illustrator capability in the parity catalog".

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** No effect model, registry, or effects folder exists in the core project (`src/Nodus/Bezier.Core/Effects` is absent). The offset operation every contour, offset path, and block shadow needs is a placeholder in `src/Nodus/Bezier.Core/Services/PathOperationsService.cs` ("Placeholder - actual implementation uses SkiaSharp path effects") that returns its input, and so is the boolean operation the live pathfinder effects and Live Paint need ("This will be implemented with SkiaSharp in the Desktop layer"); `StrokeToPath` in the same file is a placeholder too. The core project (`src/Nodus/Bezier.Core/Bezier.Core.csproj`) references no SkiaSharp package today, although `standards/nodus.md` allows it for geometry. The renderer, `src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs`, is one 840-line file with no Skia image filters (no shadow, glow, or feather path) that never applies a clip path, although `src/Nodus/Bezier.Core/Models/Elements/SvgClipPath.cs` exists in the model, so PowerClip starts from the model only. The SVG writer (`src/Nodus/Bezier.Core/Services/SvgExporter.cs`) emits no `nodus:` data yet; `D02 T07 §1` adds it before this file runs. There are 9 tool classes on `ToolBase` under `src/Nodus/Bezier.Core/Tools/` and none is an effect tool. A per-element `BlendMode` enum exists in `src/Nodus/Bezier.Core/Models/VectorElement.cs` and is what shadow merge modes and glow modes reuse. Paths below use the Photon.Nodus names `D02 T01 §1` introduces; the claims use today's names.
<!-- claim: absent src/Nodus/Bezier.Core/Effects -->
<!-- claim: count "Placeholder - actual implementation uses SkiaSharp path effects" src/Nodus/Bezier.Core/Services/PathOperationsService.cs = 1 -->
<!-- claim: count "This will be implemented with SkiaSharp in the Desktop layer" src/Nodus/Bezier.Core/Services/PathOperationsService.cs = 1 -->
<!-- claim: count "SkiaSharp" src/Nodus/Bezier.Core/Bezier.Core.csproj = 0 -->
<!-- claim: count "SKImageFilter" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->
<!-- claim: lines src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 840 -->
<!-- claim: exists src/Nodus/Bezier.Core/Models/Elements/SvgClipPath.cs -->
<!-- claim: count "ClipPath" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->
<!-- claim: count "nodus:" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->
<!-- claim: count "class \w+Tool\b" src/Nodus/Bezier.Core/Tools/*.cs = 9 -->
<!-- claim: absent src/Nodus/Bezier.Core/Tools/BlendTool.cs -->
<!-- claim: count "public enum BlendMode" src/Nodus/Bezier.Core/Models/VectorElement.cs = 1 -->

## Inputs

- [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) -- the catalog rows each section owns (Blend, contour, envelope, and distort; 3D, shadows, glows, and bevels; Lenses, PowerClip, perspective, symmetry, and repeats)
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- the blueprint this file was authored from, with its recorded decisions on names and the `nodus:` namespace
- [`standards/nodus.md`](../../standards/nodus.md) -- the document model, commands for every mutation, one render path through `SkiaRenderer`, Inkscape as the fidelity oracle, and SkiaSharp allowed in the core for geometry
- [`standards/shared.md`](../../standards/shared.md) -- commands, logging, settings, and view-model rules every section builds to
- Illustrator 30.8 and CorelDRAW 2026 user guides -- the behavior each effect matches; Inkscape (path effects, the Interpolate extension, filter rendering) -- the golden reference for expanded fallbacks, version recorded beside each fixture
- -> XREF: D02 T01 §1 -- the rename to Photon.Nodus that every path in this file assumes
- -> XREF: D02 T07 §1 -- the live-object contract and the generic Expand every effect persists and expands through
- -> XREF: D02 T07 §2 -- the dirty-region rendering that §1's effect cache plugs into
- -> XREF: D02 T07 §7 -- focus mode, which opens effect groups, lenses, and distortions
- -> XREF: D02 T07 §8 -- the property bar that hosts every effect tool's options
- -> XREF: D02 T07 §11 -- the snapping engine that §13's symmetry lines and §14's perspective lines register with
- -> XREF: D02 T08 §4 -- the live rectangle and live corners that §8's round corners and §9's extruded rectangles use
- -> XREF: D02 T08 §6 -- the node overlay that §3's node mapping and §5's envelope editing reuse
- -> XREF: D02 T08 §7 -- the destructive offset path command that shares §4's offset kernel
- -> XREF: D02 T08 §8 -- knife, eraser, and crop, which flatten perspective effects first
- -> XREF: D02 T08 §10 -- the pathfinder and intersection kernels that §7, §17, and §19 call
- -> XREF: D02 T08 §11 -- the clipping masks that §12's PowerClip builds on
- -> XREF: D02 T09 §2 -- the shared color controls every effect panel consumes
- -> XREF: D02 T09 §3 -- the swatch cursor preview that §17's Live Paint bucket shows
- -> XREF: D02 T09 §7 -- gradients inside blends and extrusions
- -> XREF: D02 T09 §9 -- the mesh editor §5 must not duplicate
- -> XREF: D02 T09 §14 -- the Appearance stack that holds every live effect
- -> XREF: D02 T09 §15 -- graphic styles that carry effects
- -> XREF: D02 T09 §19 -- the blend modes that shadow and glow merge modes reuse
- -> XREF: D02 T09 §20 -- the transparency feather whose mask builder §8's feather shares
- -> XREF: D02 T10 §2 -- text objects under envelopes, 3D, and perspective
- -> XREF: D02 T10 §8 -- paragraph text frames that an envelope reshapes
- -> XREF: D02 T12 §2 -- raster effects, the lower half of the Effect menu §1 builds
- -> XREF: D02 T13 §7 -- overprint, which block shadows and bevel inks carry
- -> XREF: D02 T13 §14 -- the PDF writer that prints and exports effects as their expanded geometry
- -> XREF: D02 T14 §5 -- Illustrator `.ai` effect interchange
- -> XREF: D02 T14 §7 -- CorelDRAW `.cdr` effect interchange
- -> XREF: D02 T14 §11 -- the HPGL and cutter export that §4's cuttable contours feed
- -> XREF: D02 T15 §2 -- AI turntable generation, whose help text points users to §10's 3D and Materials instead
- -> XREF: D01 T02 §2 -- the settings store every `Nodus.*` effect key goes through
- -> XREF: D01 T02 §4 -- the suite history every effect command records into

## Outcome

- One effect registry and stack evaluator drive every live effect; each effect evaluates lazily from stored parameters, caches its output, and redraws a 10,000-object document with 500 live effects from cache in a 16 ms pan frame.
- Blend, contour, envelope, warp, distort, shadow, glow, feather, scribble, round corners, bevel, classic 3D, extrude, 3D and Materials, lens, puppet warp, repeat, objects on a path, and the path effects are live objects that reopen live from SVG and expand to plain SVG geometry any reader draws.
- PowerClip frames, symmetry groups, perspective grids and bound objects, and Live Paint groups keep their contents as real editable objects.
- Every create, edit, clear, release, break apart, and expand is one undoable command with one Serilog Information line, and Release restores the source objects exactly.
- 3D objects render photorealistically through an own deterministic CPU path tracer and export to OBJ, glTF, and USDA validated by the Khronos and OpenUSD validators.

**Adjacency:** list=applicable @ D02 T11 §3; document=applicable @ D02 T13 §14; settings=applicable; reporting=not-applicable (effects have no domain summary beyond the Appearance panel and Document Info owned by D02 T07 §14); notifications=applicable @ D02 T11 §10; permissions=applicable @ D02 T11 §1; audit=applicable @ D02 T11 §1; exchange=applicable @ D02 T11 §10; reverse=applicable @ D02 T11 §1

**Adjacency rationale:** Every effect family ships a preset list through one `EffectPresetStore` (§3): blend, envelope, distortion, shadow, extrusion, 3D material, bevel profile, and perspective grid presets. Effects print and export as their expanded geometry through the PDF writer of `D02 T13 §14`. Per-tool defaults, preset folders, 3D render quality, and the PowerClip preferences all go through the settings store with a named consumer. There is no reporting surface: the Appearance panel and Document Info already summarize an object. The ray-traced render, Live Paint on large art, and 3D export report progress and a completion notification on the status strip. A locked layer or locked object refuses Make, Clear, and Break Apart by name, and a read-only 3D export target is refused by name. Exchange is the `nodus:` SVG parameters with an expanded fallback, 3D export to OBJ, glTF, and USDA, and presets imported and exported as JSON. Clear, Release, Break Apart, and Expand are each undoable.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
| 1 | §1 | The live-effect framework: effect stack, parameters, copy, clone, clear, and expand | D02 T09 §14 | [ ] |
| 2 | §2 | Blend: tool, steps, spacing, easing, and color acceleration | §1 | [ ] |
| 3 | §3 | Blend on a path, node mapping, split, fuse, compound blends, and presets | §2 | [ ] |
| 4 | §4 | Contour | §1 | [ ] |
| 5 | §5 | Envelope distort and warp | §1 | [ ] |
| 6 | §6 | The distort tool and Distort & Transform effects | §1 | [ ] |
| 7 | §7 | Drop, inner, perspective, and block shadows | §1 | [ ] |
| 8 | §8 | Glows, feather, scribble, round corners, and bevels | §7 | [ ] |
| 9 | §9 | 3D extrude and revolve: geometry, lighting, bevels, and vanishing points | §1 | [ ] |
| 10 | §10 | 3D and Materials: inflate, plane, materials, mapped art, ray-traced rendering, and 3D export | §9 | [ ] |
| 11 | §11 | Lenses | §1 | [ ] |
| 12 | §12 | PowerClip frames | D02 T08 §11 | [ ] |
| 13 | §13 | Symmetry drawing mode | §1 | [ ] |
| 14 | §14 | The perspective grid and drawing planes | D02 T07 §11 | [ ] |
| 15 | §15 | Perspective objects and the Add Perspective effect | §14, §5 | [ ] |
| 16 | §16 | Puppet warp | §1 | [ ] |
| 17 | §17 | Live Paint and smart fill | D02 T08 §10 | [ ] |
| 18 | §18 | Repeats and objects on a path | §1 | [ ] |
| 19 | §19 | Path effects: convert to shape, offset, outline, and pathfinder effects | §1, D02 T08 §10 | [ ] |

---

## 1. The live-effect framework: effect stack, parameters, copy, clone, clear, and expand

Every section after this one is an effect, and without one shared contract each would invent its own persistence, cache, and undo, which is how three copies of one bug ship. This section builds the vector effect registry and the stack evaluator in `Photon.Nodus.Core/Effects/` that every later section plugs into, the Effect menu, Copy Effect From, Clone Effect From, Clear Effect, Break Apart, Expand, and a render cache. It must not bypass the Appearance stack of `D02 T09 §14` or the generic Expand of `D02 T07 §1`. Catalog: NP-1432 to NP-1435 (4 features): resolution-independent effect parameters, the vector and raster split of the Effect menu, the generic Clear Effect, and effects in focus mode. Copy Effect From, Clone Effect From, Break Apart, and Expand are the shared machinery the per-effect catalog rows of §2 to §19 call.

**Fidelity:** extends the main window menus -- docs/captures/nodus/main-window/.
**Job:** a user can add, edit, copy, clone, clear, and expand a live effect from the Effect and Object menus. Consumer: the Appearance stack of `D02 T09 §14`, the renderer, and the SVG writer.
**Treatment:** effects evaluate lazily from stored parameters and cache their output per object. Cheaper substitute that fails the checkpoint: applying each effect destructively once and storing only the result.
**Chrome:** consume the Appearance panel of `D02 T09 §14`, the shared icon catalog, and the suite history; do not invent a second effect list or a second undo stack.

**Requires:** display-session -- the Effect menu and the Copy Effect From pick mode are driven and captured on the canvas

- [ ] Reference SkiaSharp from `src/Nodus/Photon.Nodus.Core/Photon.Nodus.Core.csproj` for geometry (`SKPath`, `SKPathMeasure`, `SKPath.Op`), as `standards/nodus.md` allows, with no WPF reference. Done when: the core builds and a test asserts the core assembly references no `PresentationCore`.
- [ ] Add `IVectorEffect` in `src/Nodus/Photon.Nodus.Core/Effects/IVectorEffect.cs`: `Id`, `Kind` (vector or raster), a `Parameters` record, `Evaluate(EffectInput) -> EffectOutput` (geometry plus paint), `Bounds`, and `Expand()`. Done when: a test effect implements it and the solution builds.
- [ ] Add `EffectRegistry` in `src/Nodus/Photon.Nodus.Core/Effects/EffectRegistry.cs` registered through the composition root; each later section registers its effects there. Done when: `EffectRegistryTests` register and resolve a test effect and reject a duplicate id.
- [ ] Build the Effect menu from the registry, vector effects on top and the raster effects of `D02 T12 §2` below a separator (the raster group is empty with its owner named until that section ships). Done when: a view-model test asserts the menu order and a driven run captures the menu to `docs/captures/nodus/main-window/effect-menu.png`.
- [ ] Add `EffectStackEvaluator` in `src/Nodus/Photon.Nodus.Core/Effects/EffectStackEvaluator.cs` walking the Appearance stack items of `D02 T09 §14` in order and feeding each effect the previous output; parameters are in document units so a raster effects resolution change re-evaluates without editing parameters. Done when: `EffectStackEvaluatorTests` assert order dependence with two test effects.
- [ ] Add `EffectCache` in `src/Nodus/Photon.Nodus.Desktop/Rendering/EffectCache.cs` keyed by object id, parameter hash, and source version, invalidated through the document change events and the dirty regions of `D02 T07 §2`. Done when: `EffectCacheTests` assert a hit after a pan and a miss after a parameter edit. Cheaper substitute: re-evaluating every effect every frame.
- [ ] Meet the cache budget: a 10,000-object document with 500 live effects redraws a pan frame in 16 ms from cache. Done when: `EffectCacheBenchmarks` asserts the budget on the build machine and prints the measured time.
- [ ] Persist each effect as `nodus:effect` elements with typed parameters under the `D02 T07 §1` contract and its expanded geometry as the plain-SVG fallback; unknown effect kinds are preserved verbatim. Done when: `EffectRoundTripTests` save, reopen live, and expand a registered test effect, and an unknown kind survives a round trip byte for byte.
- [ ] Add `CopyEffectFromCommand` in `src/Nodus/Photon.Nodus.Core/Commands/Effects/`: Object, Copy Effect submenu entries enter a pick mode (arrow cursor) that copies the picked object's effect parameters onto the selection. Done when: a test copies a test effect's parameters and one undo removes them.
- [ ] Add `CloneEffectFromCommand`: Object, Clone Effect entries link the selection's effect to a master by id; a master edit propagates to every clone in one command. Done when: a test edits the master and asserts two clones updated in one history entry.
- [ ] Add `ClearEffectCommand` removing the top interactive effect (generic over the registry) and `BreakEffectApartCommand` (Ctrl+K on an effect group) turning output into real objects while keeping the source. Done when: tests cover both and their undo.
- [ ] Expand reuses the generic Expand of `D02 T07 §1`. Done when: a test expands a test effect and the result equals its fallback geometry element by element.
- [ ] Focus mode (`D02 T07 §7`) opens an effect group with its control objects editable and the generated parts dimmed. Done when: a driven run enters focus mode on an effect group and the capture shows the dimmed parts.
- [ ] Refuse Make, Clear, and Break Apart on a locked layer or locked object with a status message naming the lock, following the edit permissions the layer model enforces. Done when: a test asserts the refusal text and an unchanged history.
- [ ] Every effect mutation records one `IEditorCommand` in the suite history (`D01 T02 §4`) and writes one Serilog Information line naming the effect kind and object id, so the undo history and the log audit every effect edit. Done when: a test logger asserts one line per mutation.
- [ ] Add a shared effect test harness in `tests/Photon.Nodus.Tests/Effects/EffectTestHarness.cs`: load a fixture, evaluate, save, reopen, compare parameters and the expanded fallback element by element, and render against a committed golden within a stated tolerance. Done when: `EffectRoundTripTests` use it and the later sections' round-trip tests can reuse it.
- [ ] Commit `tests/fixtures/nodus/svg/effects/stack-basic.svg` and its golden. Done when: the fixture carries two stacked test effects and the golden names the Inkscape version that rendered the fallback.
- [ ] Update `docs/user/nodus/effects.md` with the Effect menu, Copy and Clone Effect From, Clear, Break Apart, and Expand. Done when: every command is listed.
- [ ] Commit: `"nodus: the live-effect framework with its registry, stack, and cache"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~EffectRoundTripTests"` saves and reopens `tests/fixtures/nodus/svg/effects/stack-basic.svg`, comparing parameters and the expanded fallback element by element. Unit test: `EffectRegistryTests`, `EffectStackEvaluatorTests`, and `EffectCacheTests` pass. Driven run with evidence: the Effect menu and the Copy Effect From pick mode captured under `docs/captures/nodus/main-window/`. Cheaper substitute that fails the checkpoint: a substitute that only rasterizes the effect output, which loses the live effect on reopen.

## 2. Blend: tool, steps, spacing, easing, and color acceleration

A blend is the classic live effect: intermediate shapes and colors between key objects that update when a key object moves. A one-shot duplicate-and-tint is not a blend. This section adds live blends between two or more key objects with the Blend tool, Make, Release, Expand, the Blend panel, steps and spacing, easing, rotation and loop, object and color acceleration, and the color path. Catalog: NP-1436 to NP-1451 (16 features): the Blend tool, make and release, expand, reverse front to back, the Blend panel, smooth color, specified steps, and specified distance, orientation, easing, rotation and loop, object acceleration, color acceleration, accelerated sizing, the color path, and live key-object editing.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/blend-panel/.
**Job:** a user can blend shapes and tune steps, spacing, easing, and color, seeing the blend update live. Consumer: the effect stack of §1 and the SVG writer.
**Treatment:** shape interpolation with node correspondence and color interpolation in the document color space, with a live preview while dragging sliders. Cheaper substitute that fails the checkpoint: a one-shot duplicate-and-tint that is not live and loses the blend on reopen.
**Chrome:** consume the `Photon.UI` sliders and number boxes, the shared color controls of `D02 T09 §2`, and the property bar of `D02 T07 §8`; do not invent a second panel dock.

**Requires:** display-session -- the Blend tool is driven on the canvas and the panel is captured

- [ ] Add `BlendEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Blend/BlendEffect.cs`: key object ids, spine id, `Spacing` (smooth color, specified steps, specified distance), `Orientation` (page, path), `Rotation`, `Loop`, `Easing` (none, in, out, in-out, out-in, ramp 0 to 100), `ObjectAcceleration`, `ColorAcceleration`, `AccelerateSizing`, and `ColorPath` (direct, clockwise, counterclockwise), registered in §1's registry. Done when: `BlendEffectTests` construct each parameter and the registry resolves the kind.
- [ ] Add `ShapeInterpolator` in `src/Nodus/Photon.Nodus.Core/Effects/Blend/ShapeInterpolator.cs`: normalize both paths to matching node counts (subdivide by arc length), interpolate nodes and handles, and handle compound paths with unequal subpath counts. Done when: `ShapeInterpolatorTests` blend a square to a circle and a two-subpath shape to a one-subpath shape and match the goldens.
- [ ] Add `ColorInterpolator` in `src/Nodus/Photon.Nodus.Core/Effects/Blend/ColorInterpolator.cs`: solid fills and gradient stops, direct or clockwise and counterclockwise travel around HSB hue. Done when: `BlendColorPathTests` assert the midpoint color for each path.
- [ ] Bitmap, pattern, and texture fills do not progress in a blend (the CorelDRAW fill restriction), shown with a status hint naming the fill kind. Done when: a test blends two pattern-filled objects and asserts the intermediate fills equal the start fill and the hint text.
- [ ] Smooth color computes the step count from the color distance; specified steps and specified distance place steps exactly. Done when: `BlendSpacingTests` assert step count and spacing for each mode.
- [ ] Easing curves (none, in, out, in-out, out-in, ramp) and object and color acceleration with accelerated sizing. Done when: `BlendEasingTests` compare step positions to the committed goldens.
- [ ] Rotation of intermediate steps and Loop (steps travel around the rotation center). Done when: a golden shows the rotated steps.
- [ ] Add `BlendTool` (W) in `src/Nodus/Photon.Nodus.Core/Tools/BlendTool.cs`: click objects or anchor points in order, or drag from one object to another. Done when: `BlendToolTests` create a three-key blend by clicks and a two-key blend by drag. Cheaper substitute: duplicate-and-tint.
- [ ] Commands under Object, Blend: Make (Alt+Ctrl+B), Release (Alt+Shift+Ctrl+B), Expand, Reverse Front to Back, and Break Blend Apart (Ctrl+K), each in `src/Nodus/Photon.Nodus.Core/Commands/Effects/Blend/`. Done when: tests cover each and Release restores the key objects exactly.
- [ ] Add `BlendPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/BlendPanel.xaml` (Window, Blend and Effects, Blend): Make, Expand, Release, Reverse, steps, spacing, orientation, an easing curve preview, appearance shift, rotation, loop, and color path, with live preview while dragging sliders. Done when: a driven run captures the panel to `docs/captures/nodus/blend-panel/panel.png` and each control has a view-model test.
- [ ] Live editing: moving or recoloring a key object with direct selection re-evaluates the blend through §1's cache; a 1,000-step blend re-evaluates under 50 ms. Done when: `BlendBenchmarks` asserts the budget and a test moves a key object and asserts the steps moved.
- [ ] Settings `Nodus.Blend.DefaultSteps` and `Nodus.Blend.DefaultSpacing` through the settings store (`D01 T02 §2`), consumed by `BlendTool`. Done when: a test changes the default and a new blend uses it.
- [ ] Persist `nodus:blend` parameters with the intermediate steps as the expanded fallback group. Done when: `BlendRoundTripTests` reopen the blend live through §1's harness.
- [ ] Commit fixtures under `tests/fixtures/nodus/svg/blend/` with goldens compared to Inkscape's Interpolate extension for linear step placement (version recorded beside the fixture) and own snapshot goldens for easing and color paths. Done when: each fixture has its goldens and version line.
- [ ] Every blend command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/blends.md`. Done when: every tool gesture, command, and panel control is listed.
- [ ] Commit: `"nodus: live blends with steps, easing, and color paths"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Nodus.Tests.Effects.Blend"` exits 0 with `ShapeInterpolatorTests`, `BlendEasingTests`, `BlendColorPathTests`, and `BlendSpacingTests` matching the step-geometry goldens on `tests/fixtures/nodus/svg/blend/`. Format fidelity proof: `BlendRoundTripTests` reopen every fixture live. Driven run with evidence: the Blend tool and panel captured under `docs/captures/nodus/blend-panel/`. Cheaper substitute that fails the checkpoint: storing only expanded steps, which the reopen-as-live check catches.

## 3. Blend on a path, node mapping, split, fuse, compound blends, and presets

A blend becomes a layout tool when it follows a path and when a designer controls which nodes correspond and where the blend splits. This section adds blends along a spine or freehand path, node mapping, start and end replacement, split and fuse, compound blends, copy and clone, clear, and the preset store every later effect section reuses. Catalog: NP-1452 to NP-1468 (17 features): replace and reverse spine, blend along full path and rotate along, fit to a new path, show path and detach, freehand path blends, node mapping, show start and end, new start and end, split, fuse, compound blends, copy and clone blend, clear blend, and blend presets.

**Fidelity:** extends docs/captures/nodus/blend-panel/.
**Job:** a user can put a blend on a path, map nodes, split, fuse, and chain blends. Consumer: `BlendEffect` of §2 and the SVG writer.
**Treatment:** arc-length parameterized placement along the spine with node correspondence the user can override. Cheaper substitute that fails the checkpoint: placing steps on the straight chord and ignoring the path.
**Chrome:** consume §2's panel, the shared preset store built here, and the node overlay of `D02 T08 §6`; do not invent a second node editor.

**Requires:** display-session -- path blends, node mapping, and split are driven on the canvas

- [ ] Add `BlendSpine` in `src/Nodus/Photon.Nodus.Core/Effects/Blend/BlendSpine.cs`: an arc-length table over the spine path with `FullPath` and `RotateAlong`. Done when: `BlendSpineTests` assert equal arc spacing within 0.01 px on a Bezier spine. Cheaper substitute: steps on the straight chord.
- [ ] Object, Blend: Replace Spine and Reverse Spine, one command each. Done when: tests replace the spine with a circle and reverse it, asserting step order.
- [ ] Property bar New Path (fit the blend to a picked path), Show Path, and Detach From Path. Done when: tests cover each and Detach restores the straight blend.
- [ ] Freehand path blend: Alt+drag with the Blend tool records a freehand spine; the shape tool edits spine nodes and the blend follows. Done when: a driven run draws a freehand blend and edits a spine node, captured to `docs/captures/nodus/blend-panel/path-blend.png`.
- [ ] Add the `NodeMap` parameter: Map Nodes mode picks one node on the start and one on the end through the node overlay of `D02 T08 §6`, stored as node indices in `nodus:blend`. Done when: a test maps nodes and the intermediate twist matches the golden.
- [ ] Show Start and Show End select the key objects; New Start and New End pick a replacement object in one command. Done when: tests assert selection and replacement with undo.
- [ ] Add `SplitBlendCommand` promoting an intermediate step to a key object, and `FuseBlendCommand` rejoining split or compound blends. Done when: `BlendSplitFuseTests` split then fuse and the result equals the original blend.
- [ ] Compound blends by dragging onto the start or end object of another blend (shared key object id). Done when: `CompoundBlendTests` chain two blends and moving the shared key updates both.
- [ ] Copy Effect Blend From and Clone Effect Blend From through §1's commands; Clear Blend removes the blend keeping the key objects. Done when: tests cover each with undo.
- [ ] Add `EffectPresetStore` in `src/Nodus/Photon.Nodus.Core/Effects/Presets/EffectPresetStore.cs`, shared by every later effect section: JSON files under `%LOCALAPPDATA%\Rizonesoft\Nodus\Presets\<Kind>\`, apply, save, delete, import, and export, written atomically. Done when: `EffectPresetStoreTests` round trip a preset, refuse a malformed file by name, and refuse a read-only folder by name.
- [ ] Blend presets under `Presets\Blend\` in the Blend panel's preset list. Done when: a test saves and applies a blend preset.
- [ ] Persist spine id, `FullPath`, `RotateAlong`, the node map, and compound links in `nodus:blend`. Done when: `BlendRoundTripTests` gain fixtures `tests/fixtures/nodus/svg/blend/path-*.svg` that reopen with Replace Spine still working.
- [ ] Every command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/blends.md` for path blends, node mapping, split and fuse, and presets. Done when: every command is listed.
- [ ] Commit: `"nodus: blends on paths, node mapping, split and fuse, and effect presets"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~BlendSpineTests|FullyQualifiedName~BlendSplitFuseTests|FullyQualifiedName~CompoundBlendTests|FullyQualifiedName~EffectPresetStoreTests"` exits 0. Format fidelity proof: `BlendRoundTripTests` on `tests/fixtures/nodus/svg/blend/path-*.svg` round trip the spine, node map, and compound links. Driven run with evidence: a freehand path blend captured under `docs/captures/nodus/blend-panel/`. Cheaper substitute that fails the checkpoint: baking the path blend into plain groups, which Replace Spine after reopen exposes.

## 4. Contour

Contours are concentric offset copies that must be truly equidistant: scaled copies are not, and they visibly bunch on concave shapes. This section adds the shared offset kernel that replaces today's placeholder, a live contour effect with the Contour tool and panel, and cuttable outlines. Catalog: NP-1469 to NP-1482 (14 features): the Contour tool and panel, to center, inside, and outside, steps and offset, object and color acceleration, corner styles, fill and outline end colors, the color path, break apart, copy and clone, and cuttable outlines.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/contour-panel/.
**Job:** a user can add concentric contours and tune their direction, spacing, corners, and colors. Consumer: the effect stack of §1 and the SVG writer.
**Treatment:** true geometric offset curves with mitered, round, or bevel joins. Cheaper substitute that fails the checkpoint: scaled copies of the source, which are not equidistant.
**Chrome:** consume the shared color controls, the `Photon.UI` number boxes, and §1's commands; do not invent a second offset routine beside `D02 T08 §7`.

**Requires:** display-session -- the Contour tool handle drag and the panel are driven and captured

- [ ] Add `OffsetKernel` in `src/Nodus/Photon.Nodus.Core/Geometry/OffsetKernel.cs`: stroke-outline based offset (`SKPaint.GetFillPath` plus `SKPath.Op` cleanup) with mitered, round, and bevel joins and a miter limit. Done when: `OffsetKernelTests` assert every output sample lies at the offset distance from the source within 0.05 px on committed shapes. Cheaper substitute: scaled copies, which fail the distance property.
- [ ] Replace the `PathOperationsService.Offset` placeholder with a call to `OffsetKernel`, shared with `D02 T08 §7` and §19. Done when: `grep -c "Placeholder - actual implementation uses SkiaSharp path effects" src/Nodus/Photon.Nodus.Core/Services/PathOperationsService.cs` prints 0 and the existing `PathOperationsService` tests pass.
- [ ] Add `ContourEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Contour/ContourEffect.cs`: `Direction` (to center, inside, outside), `Steps`, `Offset`, `ObjectAcceleration`, `ColorAcceleration`, `Corners`, `FillEndColor` (a second color for gradient fills), `OutlineEndColor`, and `ColorPath` (linear, clockwise, counterclockwise). Done when: `ContourEffectTests` assert step count and spacing per direction.
- [ ] To-center contours stop when the offset collapses the shape, with no degenerate steps. Done when: a test on a thin shape asserts no empty or self-intersecting step.
- [ ] Color progression from the source fill and outline to the end colors along the color path. Done when: tests assert the midpoint colors for each path.
- [ ] Add `ContourTool` in `src/Nodus/Photon.Nodus.Core/Tools/ContourTool.cs`: dragging from the object edge sets direction and offset; the end-fill handle accepts a palette color drop. Done when: a driven run creates an outside contour by drag and drops an end color, captured to `docs/captures/nodus/contour-panel/tool.png`.
- [ ] Add `ContourPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/ContourPanel.xaml` (Effects, Contour, Ctrl+F9). Done when: a driven run captures the panel and each control has a view-model test.
- [ ] Break Contour Apart separates the source from a group of contour steps; Copy and Clone Effect Contour From through §1. Done when: tests cover each with undo.
- [ ] Cuttable outlines: contour steps are closed, non-overlapping curves with fills stacked, so an HPGL or PDF cutter export (`D02 T14 §11`) sees one cut line per step. Done when: a test asserts pairwise non-intersection of the expanded steps.
- [ ] Meet the budget: 100 contour steps on a 500-node path evaluate under 200 ms; slower runs move off the UI thread with cancellation. Done when: `ContourBenchmarks` asserts the budget and a cancellation test leaves the document unchanged.
- [ ] Persist `nodus:contour` with the expanded steps as the fallback; commit fixtures under `tests/fixtures/nodus/svg/contour/` with fallbacks compared to Inkscape's Offset path effect output (version recorded). Done when: `ContourRoundTripTests` reopen every fixture live.
- [ ] Contour presets under `Presets\Contour\` through `EffectPresetStore`. Done when: a test saves and applies a contour preset.
- [ ] Every contour command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/contours.md`. Done when: the tool, panel, and commands are listed.
- [ ] Commit: `"nodus: live contours on a shared offset kernel"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~OffsetKernelTests|FullyQualifiedName~ContourEffectTests"` exits 0 with the equidistance property holding within 0.05 px. Format fidelity proof: `ContourRoundTripTests` on `tests/fixtures/nodus/svg/contour/` with fallbacks compared to the Inkscape Offset golden. Driven run with evidence: the Contour tool and panel captured under `docs/captures/nodus/contour-panel/`. Cheaper substitute that fails the checkpoint: scaled copies, which fail the equidistance property.

## 5. Envelope distort and warp

An envelope bends artwork and text into a shape while both stay editable; moving only anchor points kinks every curve, so the mapping must reach handles and subdivide adaptively. This section adds envelope distortion (make with warp, mesh, or top object; release; expand; edit contents), the CorelDRAW envelope modes, presets, node editing and mapping modes, envelopes on paragraph text frames and bitmaps, and the Warp effect with its fifteen styles. If the section overflows at build time, the natural split is the envelope engine with the Illustrator commands versus the CorelDRAW envelope tool and panel (section-design sizing note), spending Phase 8's spare ceiling. Catalog: NP-1483 to NP-1504 (22 features): make with warp, make with mesh and mesh editing, from a top object or curve, release and expand, edit contents or envelope, envelope options, warped text, warp options and styles, copy envelope from, the Envelope tool and panel, the four modes, presets, add new envelope, clear, keep lines, node editing and types, constrained moves, the four mapping modes, paragraph text frames, and bitmaps.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/envelope-panel/ and docs/captures/nodus/warp-dialog/.
**Job:** a user can bend artwork and text into a shape and keep editing both. Consumer: the effect stack of §1, the text frames of `D02 T10 §8`, and the SVG writer.
**Treatment:** a bilinear Coons or mesh map applied to every node and handle with adaptive subdivision so curves stay smooth. Cheaper substitute that fails the checkpoint: moving only anchor points, which kinks curves.
**Chrome:** consume the shared node overlay, the `EffectPresetStore` of §3, and the `Photon.UI` dialog chrome; do not invent a second mesh editor beside `D02 T09 §9`.

**Requires:** display-session -- envelope node drags, mesh editing, and the Warp dialog are driven and captured

- [ ] Add `EnvelopeEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Envelope/EnvelopeEffect.cs`: `Source` (warp, mesh rows by columns, top object, curve), `Mode` (straight line, single arc, double arc, unconstrained), `Mapping` (horizontal, original, putty, vertical), `KeepLines`, `Fidelity`, `DistortAppearance`, `DistortLinearGradients`, `DistortPatternFills`, and `PreserveShape` (clip or transparency). Done when: `EnvelopeEffectTests` construct each parameter and the registry resolves the kind.
- [ ] Add `MeshMap` in `src/Nodus/Photon.Nodus.Core/Effects/Envelope/MeshMap.cs`: a Coons patch per cell with adaptive subdivision of segments by flatness until the error is under the fidelity tolerance. Done when: `MeshMapTests` assert the maximum deviation from a dense-sampled reference stays under the tolerance. Cheaper substitute: an anchor-only mapper, which fails the smoothness check.
- [ ] The four mapping modes (horizontal, original, putty, vertical) and Keep Lines (straight segments stay straight). Done when: `EnvelopeMappingModeTests` compare each mode to its golden.
- [ ] Add `WarpEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Warp/WarpEffect.cs`: styles arc, arc lower, arc upper, arch, bulge, shell lower, shell upper, flag, wave, fish, rise, fisheye, inflate, squeeze, and twist; horizontal or vertical, bend, and distortion H and V, sharing `MeshMap`. Done when: `WarpStyleTests` match one golden per style.
- [ ] Add the Warp dialog in `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/Distort/WarpDialog.xaml` with a Preview check box rendering through §1's cache. Done when: a driven run captures the dialog to `docs/captures/nodus/warp-dialog/dialog.png`.
- [ ] Commands under Object, Envelope Distort: Make with Warp (Alt+Shift+Ctrl+W), Make with Mesh (Alt+Ctrl+M), Make with Top Object (Alt+Ctrl+C), Release, Expand, Edit Contents or Edit Envelope. Done when: tests cover each and Release restores the source and the envelope shape exactly.
- [ ] Mesh editing for Make with Mesh: move mesh points and handles, add rows and columns, through the node overlay of `D02 T08 §6`. Done when: a test moves a mesh point and the art follows the golden.
- [ ] Add the Envelope Options dialog: anti-alias, fidelity, distort appearance, distort linear gradients, distort pattern fills, and preserve shape using clip or transparency. Done when: view-model tests assert each option reaches the effect.
- [ ] CorelDRAW commands: Create Envelope From (another curve), Add New Envelope over an existing one, and Clear Envelope; Copy Envelope From through §1. Done when: tests cover each with undo.
- [ ] Add `EnvelopeTool` in `src/Nodus/Photon.Nodus.Core/Tools/EnvelopeTool.cs`: double-click adds or deletes nodes, marquee and freehand multi-select, node types cusp, smooth, and symmetrical, and segment to line or curve. Done when: `EnvelopeToolTests` add a node, change its type, and convert a segment.
- [ ] Constrained node moves: Ctrl, Shift, and Ctrl+Shift constrain the drag as CorelDRAW does (opposite node mirrored, both axes). Done when: tests assert each constrained move's result.
- [ ] Add `EnvelopePanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/EnvelopePanel.xaml` (Effects, Envelope, Ctrl+F7) with the mode, mapping, and keep-lines controls. Done when: a driven run captures the panel to `docs/captures/nodus/envelope-panel/panel.png`.
- [ ] Envelope presets under `Presets\Envelope\` through `EffectPresetStore`, with save. Done when: a test saves and applies a preset.
- [ ] Text: an envelope on paragraph text reshapes the frame and the text reflows through `D02 T10 §8`; on point text it maps glyph outlines while the text stays editable; warped text is the Warp effect on a text object. Done when: `EnvelopeTextTests` edit the text after enveloping and assert it stays live.
- [ ] Bitmaps: an envelope on a placed image renders as an `SKCanvas.DrawVertices` triangle mesh at draw time and expands to a resampled embedded image; the pixel engine is not used. Done when: a render golden of an enveloped fixture image matches within tolerance.
- [ ] Persist `nodus:envelope` and `nodus:warp` with expanded geometry as the fallback; commit fixtures under `tests/fixtures/nodus/svg/envelope/`. Done when: `EnvelopeRoundTripTests` reopen every fixture live.
- [ ] Every envelope and warp command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/envelopes.md`. Done when: every command, mode, and panel control is listed.
- [ ] Commit: `"nodus: envelope distort, the Envelope tool, and warp styles"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~MeshMapTests|FullyQualifiedName~WarpStyleTests|FullyQualifiedName~EnvelopeMappingModeTests|FullyQualifiedName~EnvelopeTextTests"` exits 0 with the fifteen warp-style and four mapping-mode goldens on `tests/fixtures/nodus/svg/envelope/`. Format fidelity proof: `EnvelopeRoundTripTests` reopen every fixture live. Driven run with evidence: the panel and Warp dialog captured under `docs/captures/nodus/`. Cheaper substitute that fails the checkpoint: an anchor-only mapper, which fails the smoothness check against the dense-sampled reference.

## 6. The distort tool and Distort & Transform effects

Distortions must be editable later and must look the same after every redraw, which rules out unseeded randomness. This section adds the CorelDRAW Distort tool (push and pull, zipper, twister, center handle, presets, stacked distortions) and the Illustrator Distort & Transform effects (free distort, pucker and bloat, roughen, transform with copies, tweak, twist, zig zag) as live effects. Catalog: NP-1505 to NP-1519 (15 features): free distort, pucker and bloat with push and pull, roughen, transform with copies, tweak, twist with twister, zig zag with zipper, copy and clone distortion from, the Distort tool, the center handle and command, presets, stacked distortions, clear distortion, and distortion in focus mode.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/distort-effects/.
**Job:** a user can distort a shape interactively or by numbers and edit it later. Consumer: the effect stack of §1 and the SVG writer.
**Treatment:** deterministic seeded randomness for roughen and tweak so a reopen shows the same result. Cheaper substitute that fails the checkpoint: unseeded random, which changes the art on every redraw.
**Chrome:** consume the `Photon.UI` dialog chrome with live preview, the property bar, and the `EffectPresetStore` of §3; do not invent a second transform dialog beside `D02 T08 §12`.

**Requires:** display-session -- distort tool drags and effect dialogs with preview are driven and captured

- [ ] Add `FreeDistortEffect` (four-corner map) and `PuckerBloatEffect` (percent; CorelDRAW push and pull maps to it) in `src/Nodus/Photon.Nodus.Core/Effects/Distort/`. Done when: `DistortEffectTests` compare each to its golden.
- [ ] Add `RoughenEffect` (size, detail, relative or absolute, smooth or corner, `Seed`) and `TweakEffect` (horizontal and vertical amounts, anchors and handles, `Seed`). Done when: `DistortEffectTests` assert the same seed gives byte-equal expansion and a new seed differs. Cheaper substitute: unseeded random.
- [ ] Add `TransformEffect` (scale, move, rotate, reflect, random, copies, reference point). Done when: a test with 5 copies asserts 6 outputs with the stepped transforms.
- [ ] Add `TwistEffect` (angle; the CorelDRAW twister adds direction and rotations) and `ZigZagEffect` (size, ridges per segment, smooth or corner; the CorelDRAW zipper adds frequency). Done when: `DistortEffectTests` assert node-count growth and bounds for each.
- [ ] Add `DistortTool` in `src/Nodus/Photon.Nodus.Core/Tools/DistortTool.cs` with mode buttons push and pull, zipper, and twister on the property bar. Done when: a driven run applies each mode by drag, captured to `docs/captures/nodus/distort-effects/tool.png`.
- [ ] The diamond center handle and the Center Distortion command; the zipper frequency slider handle on the canvas. Done when: tests move the center and assert the distortion re-centers.
- [ ] Stacked distortions: each drag appends a new entry to the effect stack; Clear Distortion removes the most recent one. Done when: `StackedDistortionTests` stack three and clear one, asserting two remain.
- [ ] Add the dialogs under `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/Distort/` (Free Distort, Pucker and Bloat, Roughen, Transform, Tweak, Twist, Zig Zag) with a Preview check box rendering through §1's cache. Done when: a driven run captures each dialog and each field has a view-model test.
- [ ] Distortion presets under `Presets\Distortion\` through `EffectPresetStore`; Copy and Clone Effect Distortion From through §1. Done when: tests cover each.
- [ ] Focus mode shows the object and its distortion together through `D02 T07 §7`. Done when: a driven run captures a distortion in focus mode.
- [ ] Persist each effect under `nodus:` with expanded paths as the fallback; commit fixtures under `tests/fixtures/nodus/svg/distort/` with roughen and zig zag compared to Inkscape's Roughen and Zig Zag path effects for shape class (version recorded) and own snapshot goldens for exact output. Done when: `DistortRoundTripTests` reopen every fixture live.
- [ ] Every distortion command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/distortions.md`. Done when: the tool modes, every dialog, and the commands are listed.
- [ ] Commit: `"nodus: the Distort tool and live Distort & Transform effects"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~DistortEffectTests|FullyQualifiedName~StackedDistortionTests"` exits 0 with the determinism property (same seed, byte-equal expansion) and the per-effect goldens on `tests/fixtures/nodus/svg/distort/`. Format fidelity proof: `DistortRoundTripTests` reopen every fixture live. Driven run with evidence: the Distort tool and dialogs captured under `docs/captures/nodus/distort-effects/`. Cheaper substitute that fails the checkpoint: an unseeded roughen, which fails determinism.

## 7. Drop, inner, perspective, and block shadows

Shadows must stay sharp at every zoom and editable after a reopen, which a baked bitmap copy cannot do; routing them through the Phase 9 pixel engine would also invert the phase order. This section adds drop shadows (flat and perspective), inner shadows, and vector block shadows as live effects, rendered with Skia image filters at draw time. If the section overflows at build time, block shadows are the natural split (a separate vector engine, section-design sizing note), spending Phase 8's spare ceiling. Catalog: NP-1530 to NP-1555 (26 features): flat drop shadows, the shadow tool with drop and inner modes, perspective shadows with angle, stretch, and fade, inner shadow width, merge mode, color, opacity, feathering with direction and edge type, offset, presets, the one-shadow rule, copy and clone, break apart and clear for drop and inner shadows, and the block shadow tool with depth, direction, color, remove holes, from outline, expand, overprint, simplify, break apart, and clear.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/shadow-tool/.
**Job:** a user can drag a shadow off an object and tune it on the property bar. Consumer: the effect stack of §1, the renderer, and the SVG writer.
**Treatment:** Skia image filters at render time (`SKImageFilter.CreateDropShadow`, blur, offset, color filter) for drop and inner shadows, vector geometry for block shadows. Cheaper substitute that fails the checkpoint: a baked bitmap copy, or routing through the `Photon.Core` pixel engine of Phase 9.
**Chrome:** consume the shared color controls, the blend modes of `D02 T09 §19`, the property bar, and the `EffectPresetStore` of §3; do not invent a second blur.

**Requires:** display-session -- shadow tool drags and the property bar are driven and captured

- [ ] Add `ShadowEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Shadow/ShadowEffect.cs`: `Kind` (drop, perspective, inner), `Color`, `MergeMode` (the `BlendMode` enum, default Multiply), `Opacity`, `Feather`, `FeatherDirection` (average, inside, outside, Gaussian), `EdgeType` (linear, squared, inverse squared, flat), `Offset`, `Angle`, `Stretch`, `Fade`, and `InnerWidth`. Done when: `ShadowEffectTests` construct each and the registry resolves the kind.
- [ ] Add `ShadowRenderer` in `src/Nodus/Photon.Nodus.Desktop/Rendering/ShadowRenderer.cs` building an `SKImageFilter` chain from the parameters for flat drop shadows. Done when: `ShadowFilterTests` compare the rendered alpha profile against a reference Gaussian within 2 levels. Cheaper substitute: a baked bitmap copy, which the zoom-sharpness check catches.
- [ ] Perspective shadows skew the silhouette with a matrix (angle, stretch) then fade with a gradient shader mask (fade). Done when: a golden per angle and fade matches within tolerance.
- [ ] Inner shadows use the inverted alpha clipped to the shape, with `InnerWidth`. Done when: a golden matches and no pixel falls outside the shape.
- [ ] Feather direction and edge type shape the blur falloff. Done when: `ShadowFilterTests` assert the falloff curve per edge type.
- [ ] Merge mode through the `BlendMode` enum of `D02 T09 §19`, color, and opacity. Done when: a golden per merge mode on a colored backdrop matches.
- [ ] Add `ShadowTool` in `src/Nodus/Photon.Nodus.Core/Tools/ShadowTool.cs` (drop and inner modes): drag from the center for flat, from an edge for perspective. Done when: a driven run creates both, captured to `docs/captures/nodus/shadow-tool/drag.png`.
- [ ] One shadow per object, refused on blends, contours, bevels, and extrusions with a status message naming the rule. Done when: a test asserts each refusal text and an unchanged history.
- [ ] Shadow property bar: presets, color, merge mode, opacity, feather, direction, edge, offset, angle, stretch, fade, and Copy Shadow Properties. Done when: every control has a view-model test.
- [ ] Add `BlockShadowEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Shadow/BlockShadowEffect.cs` and its tool: depth, direction, color, remove holes, from object outline, expand, overprint, and simplify; geometry is the union of swept copies through the boolean kernel of `D02 T08 §10`. Done when: `BlockShadowTests` assert the union outline against goldens with and without holes.
- [ ] Commands: Break Drop Shadow Apart (to an embedded bitmap at the raster effects resolution), Break Inner Shadow Apart, Break Block Shadow Apart, Clear Shadow, and Clear Block Shadow; Copy and Clone Effect Shadow From through §1. Done when: tests cover each with undo.
- [ ] Shadow presets under `Presets\Shadow\` through `EffectPresetStore`: apply, add, and delete. Done when: a test adds and deletes a preset.
- [ ] Drop and inner shadows write an SVG `filter` fallback (`feGaussianBlur`, `feOffset`, `feFlood`, `feComposite`) so any SVG viewer renders them; block shadows write plain paths with overprint carried for `D02 T13 §7`. Done when: `ShadowRoundTripTests` reopen live and Inkscape renders the filter fallback within tolerance of the golden (version recorded).
- [ ] Meet the budget: 1,000 shadowed objects redraw from cache at interactive frame rate, with shadow bitmaps cached per zoom bucket. Done when: `ShadowBenchmarks` asserts under 16 ms per cached frame.
- [ ] Every shadow command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/shadows.md`. Done when: both tools, the property bar, and the commands are listed.
- [ ] Commit: `"nodus: live drop, inner, perspective, and block shadows"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ShadowFilterTests|FullyQualifiedName~BlockShadowTests"` exits 0 with the rendered snapshot goldens on `tests/fixtures/nodus/svg/shadow/`. Format fidelity proof: `ShadowRoundTripTests` reopen live, with the SVG-filter fallback rendered by Inkscape and compared within tolerance. Driven run with evidence: the shadow tool drag captured under `docs/captures/nodus/shadow-tool/`. Cheaper substitute that fails the checkpoint: a baked-bitmap shadow, which fails the reopen-as-live and zoom-sharpness checks.

## 8. Glows, feather, scribble, round corners, and bevels

Stylize effects finish the Appearance vocabulary: glows and soft edges reuse §7's filter chain, scribble and round corners are geometry, and the CorelDRAW bevel is shaded facets that keep named inks for print. A glow baked into a thick blurred stroke has no parameter left to edit after a reopen. This section adds inner and outer glow, feather, round corners, scribble, and the Bevel effect with its panel. Catalog: NP-1556 to NP-1571 (16 features): feather, inner glow, outer glow, round corners, scribble, break bevel apart, copy and clone bevel, the Bevel panel, soft edge and emboss bevels, bevel offset, shadow and light colors, intensity, direction, and altitude, spot and process colors, and clear bevel.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/stylize-effects/ and docs/captures/nodus/bevel-panel/.
**Job:** a user can add glows, soft edges, sketchy fills, rounded corners, and bevels and edit them later. Consumer: the effect stack of §1, the renderer, and the SVG writer.
**Treatment:** glows and feather as Skia image filters reusing §7's filter chain; the bevel as shaded vector facets or a lit height field at render time. Cheaper substitute that fails the checkpoint: a glow as a thick blurred stroke baked into the file.
**Chrome:** consume §7's `ShadowRenderer` filter builders, the shared color controls, and the `Photon.UI` dialog chrome; do not invent a second light-direction control beside §9's.

**Requires:** display-session -- effect dialogs with preview and the Bevel panel are driven and captured

- [ ] Add `GlowEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Stylize/GlowEffect.cs`: inner or outer, mode, color, opacity, blur, and inner source center or edge, rendered by dilate plus blur filters from §7's builders. Done when: `GlowEffectTests` compare inner and outer goldens within tolerance. Cheaper substitute: a baked blurred stroke.
- [ ] Add `FeatherEffect`: the feather radius as a blurred alpha mask, sharing the mask builder of `D02 T09 §20`'s transparency feather while staying a distinct effect. Done when: a test asserts the edge alpha ramp spans the radius.
- [ ] Add `RoundCornersEffect`: a radius applied to every corner node through the live-corner routine of `D02 T08 §4`. Done when: a test rounds a star and asserts every corner arc radius.
- [ ] Add `ScribbleEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Stylize/ScribbleEffect.cs`: angle, path overlap, variation, stroke width, curviness, spacing, and `Seed`. Done when: `ScribbleDeterminismTests` assert the same seed gives byte-equal output.
- [ ] Ship the scribble presets (Default, Childlike, Dense, Loose, Moire, Sharp, Sketch, Snarl, Swash, Tight, Zig-zag) as built-in preset files in `EffectPresetStore`. Done when: a test loads each preset and renders its golden.
- [ ] Add dialogs for glow, feather, round corners, and scribble under `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/Stylize/` with Preview through §1's cache. Done when: a driven run captures each to `docs/captures/nodus/stylize-effects/`.
- [ ] Add `BevelEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Bevel/BevelEffect.cs`: style soft edge or emboss, offset to center or distance, shadow color, light color, intensity, direction 0 to 360, and altitude 0 to 90 (disabled for emboss). Done when: `BevelFacetTests` assert facet shading follows Lambert with the given light vector.
- [ ] Spot and process colors are kept as named inks in the bevel facets for print. Done when: a test bevels a spot-filled shape and every facet references the spot ink with a tint.
- [ ] Add `BevelPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/BevelPanel.xaml` (Effects, Bevel) with every bevel parameter; direction and altitude are `Photon.UI` number boxes here, and §9 swaps in its shared light-direction control. Done when: a driven run captures the panel to `docs/captures/nodus/bevel-panel/panel.png` and each control has a view-model test.
- [ ] Clear Bevel through §1's Clear Effect; Break Bevel Apart yields facet objects; Copy and Clone Effect Bevel From through §1. Done when: tests cover each with undo.
- [ ] Glows and feather write SVG filter fallbacks; the bevel writes facet paths, with soft edges rendered as stepped facets at `Nodus.Bevel.FacetSteps`. Done when: `StylizeRoundTripTests` reopen every fixture under `tests/fixtures/nodus/svg/stylize/` and `tests/fixtures/nodus/svg/bevel/` live and a changed glow color after reopen re-renders.
- [ ] Every stylize and bevel command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/stylize.md`. Done when: every effect, dialog, and panel control is listed.
- [ ] Commit: `"nodus: glows, feather, scribble, round corners, and bevels"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~GlowEffectTests|FullyQualifiedName~ScribbleDeterminismTests|FullyQualifiedName~BevelFacetTests"` exits 0 with the snapshot goldens on `tests/fixtures/nodus/svg/stylize/` and `bevel/`. Format fidelity proof: `StylizeRoundTripTests` reopen live. Driven run with evidence: the dialogs and the Bevel panel captured under `docs/captures/nodus/`. Cheaper substitute that fails the checkpoint: a baked glow, which has no parameter to edit after reopen.

## 9. 3D extrude and revolve: geometry, lighting, bevels, and vanishing points

Vector 3D is a real mesh projected into shaded vector faces; offset copies of an outline stacked to fake depth fall apart the moment the object rotates. This section adds the classic Illustrator 3D effects (extrude and bevel, revolve, rotate with shading and mapped art) and the CorelDRAW Extrude tool and panel with presets, types, rotation, vanishing points, color modes, drape fills, extrusion bevels, and three lights. It also places the one light-direction sphere control in `Photon.UI` for §8 and §10 to reuse. Catalog: NP-1572 to NP-1593 (22 features): classic extrude, revolve, and rotate, classic shading, lighting, and map art, break extrude apart, copy and clone extrude, the Extrude panel, presets, extrusion types, extrusion inside a group, the rotation widget, direction by vanishing point, depth, rounded corners on extruded rectangles, clear extrusion, color modes, drape fills, extrusion bevels, three lights, vanishing point locking, and copying and sharing vanishing points.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/extrude-panel/ and docs/captures/nodus/3d-classic-dialog/.
**Job:** a user can give flat art vector 3D depth and light it. Consumer: the effect stack of §1, the renderer, and the SVG writer.
**Treatment:** a real 3D mesh from the profile, projected and hidden-surface sorted into vector faces with flat or smooth shading steps. Cheaper substitute that fails the checkpoint: offset copies of the outline stacked to fake depth.
**Chrome:** consume the shared color controls, the `Photon.UI` dialog chrome, and the `EffectPresetStore` of §3; the light-direction sphere control lives in `Photon.UI` once and is reused by §8 and §10.

**Requires:** display-session -- the extrude rotation widget, vanishing point drags, and dialogs are driven and captured

- [ ] Add `Mesh3D` and `Camera` (rotation X, Y, Z and perspective) in `src/Nodus/Photon.Nodus.Core/ThreeD/`. Done when: `CameraTests` project a unit cube and match the golden vertices.
- [ ] Add `ProfileExtruder` (depth, cap on or off, bevel profile, caps triangulated through `src/Nodus/Photon.Nodus.Core/Geometry/Triangulator.cs`, the one triangulator §16 also uses) and `ProfileRevolver` (angle, offset, from left or right edge) in `src/Nodus/Photon.Nodus.Core/ThreeD/`. Done when: `ProfileExtruderTests` assert vertex and face counts for a square and a star, and a revolve of a half-circle yields a sphere within tolerance.
- [ ] Add `FaceSorter` in `src/Nodus/Photon.Nodus.Core/ThreeD/FaceSorter.cs`: BSP split of intersecting faces and painter order. Done when: `FaceSorterTests` assert no face is drawn over a nearer face on the cube and torus fixtures.
- [ ] Add `Classic3DEffect` in `src/Nodus/Photon.Nodus.Core/Effects/ThreeD/Classic3DEffect.cs`: kind extrude and bevel, revolve, or rotate; surface wireframe, no shading, diffuse, or plastic; lights with intensity, ambient, highlight, and blend steps. Done when: `Classic3DTests` match a golden per surface kind. Cheaper substitute: stacked offset outlines, which fail the rotation golden.
- [ ] Map art from a symbol onto a chosen surface of a classic 3D object. Done when: a test maps a symbol onto the front face and the mapped paths follow the face's projection.
- [ ] Add `Classic3DDialog` (Effect, 3D and Materials, 3D Classic) in `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/ThreeD/Classic3DDialog.xaml` with preview through §1's cache. Done when: a driven run captures it to `docs/captures/nodus/3d-classic-dialog/dialog.png`.
- [ ] Add `LightDirectionControl` in `src/Photon.UI/Controls/LightDirectionControl.xaml`, a sphere with a draggable light point, used by §9 and §10 and swapped into §8's Bevel panel in place of its direction and altitude number boxes. Done when: a control test sets direction and altitude by drag math, the control has automation names, and a driven run captures the Bevel panel with it.
- [ ] Add `ExtrudeEffect` in `src/Nodus/Photon.Nodus.Core/Effects/ThreeD/ExtrudeEffect.cs` (CorelDRAW): type (small back, small front, big back, big front, back parallel, front parallel), depth, vanishing point locked to object or page, shared vanishing point id, rotation, color (object fill, solid, shading), drape fills, bevel (use, depth, angle, show only), and up to three numbered lights with intensity. Done when: `ExtrudeEffectTests` match a golden per type.
- [ ] Add `ExtrudeTool` in `src/Nodus/Photon.Nodus.Core/Tools/ExtrudeTool.cs`: drag to extrude, the vanishing point handle, the depth slider handle, and the rotation widget. Done when: a driven run extrudes and rotates an object, captured to `docs/captures/nodus/extrude-panel/tool.png`.
- [ ] Extrusion inside a group, and rounded corners on extruded rectangles following the live rectangle of `D02 T08 §4`. Done when: tests extrude a grouped object and a rounded rectangle and match the goldens.
- [ ] Vanishing point locking to object or page and Copy VP From, with shared vanishing points moving every extrusion that shares them. Done when: `ExtrudeVanishingPointTests` move a shared vanishing point and assert both extrusions update.
- [ ] Add `ExtrudePanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/ExtrudePanel.xaml` (Effects, Extrude) with every parameter and presets under `Presets\Extrude\`. Done when: a driven run captures the panel and each control has a view-model test.
- [ ] Commands: Clear Extrusion, Break Extrude Apart (faces become paths), and Copy and Clone Effect Extrude From through §1. Done when: tests cover each with undo.
- [ ] Persist `nodus:extrude` and `nodus:classic3d` with expanded face paths and their shading as the fallback; commit fixtures under `tests/fixtures/nodus/svg/extrude/`. Done when: `ThreeDRoundTripTests` reopen every fixture live.
- [ ] Meet the budget: a 200-node profile extrudes and sorts under 100 ms; a revolve with 64 segments under 300 ms, with cancellation beyond one second. Done when: `ThreeDBenchmarks` asserts both budgets.
- [ ] Every 3D command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/3d.md` for classic 3D and extrusions. Done when: every control on the dialog, tool, and panel is listed.
- [ ] Commit: `"nodus: classic 3D and the Extrude tool with vanishing points and lights"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ProfileExtruderTests|FullyQualifiedName~FaceSorterTests|FullyQualifiedName~ExtrudeVanishingPointTests"` exits 0 with the face-order property and the snapshot goldens of expanded faces on `tests/fixtures/nodus/svg/extrude/`. Format fidelity proof: `ThreeDRoundTripTests` reopen every fixture live. Driven run with evidence: the Extrude panel and classic 3D dialog captured under `docs/captures/nodus/`. Cheaper substitute that fails the checkpoint: stacked-outline fakes, which fail the rotation golden.

## 10. 3D and Materials: inflate, plane, materials, mapped art, ray-traced rendering, and 3D export

Illustrator's modern 3D adds inflate, materials, lighting with shadows, and a ray-traced render, and exports to 3D apps; Nodus matches the job with its own parametric materials (no Adobe Substance, no cloud library) and its own deterministic CPU path tracer, with no external renderer and no GPU dependency. The preview and the render come from one `Mesh3D` from §9. If the section overflows at build time, the natural split is modeling and preview versus the path tracer and 3D export (section-design sizing note), spending Phase 8's spare ceiling. Catalog: NP-1594 to NP-1611 (18 features): the 3D and Materials panel, plane, extrude with twist, taper, and caps, revolve, inflate, bevels and custom bevel profiles, rotation presets and perspective, the on-canvas widget, built-in and custom materials, mapped artwork, lighting presets and parameters, cast shadows, the ray-traced render, OBJ, glTF, and USDA export, and 3D on live text.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/3d-materials-panel/.
**Job:** a user can turn art into a lit, textured 3D object, render it photorealistically, and export it to a 3D app. Consumer: the effect stack of §1, the renderer, and the exported 3D files.
**Treatment:** a real-time Skia-rasterized preview plus an own deterministic CPU path tracer for the final render, both from one `Mesh3D`. Cheaper substitute that fails the checkpoint: a shaded vector preview labelled as ray traced, or a dependency on Substance or an online material library.
**Chrome:** consume §9's mesh and `LightDirectionControl`, the `Photon.UI` tabs and sliders, the status strip progress indicator, and the `EffectPresetStore` of §3; do not invent a second renderer beside `SkiaRenderer` for the preview.

**Requires:** display-session -- the rotation widget, panel tabs, and render progress are driven and captured

- [ ] Add `Materials3DEffect` in `src/Nodus/Photon.Nodus.Core/Effects/ThreeD/Materials3DEffect.cs`: object type plane, extrude (depth, twist, taper, caps), revolve (angle, offset, direction), and inflate (depth, volume, one or both sides). Done when: `Materials3DEffectTests` assert mesh counts per type and `MeshInflateTests` assert the inflated volume against the analytic value for a disk within 1 percent.
- [ ] 3D bevels (shape, width, height, repeats, space, inside or outside) with custom bevel profiles saved as paths under `Presets\Bevel3D\`. Done when: a test applies a custom profile and the bevel cross-section matches it.
- [ ] Rotation presets and X, Y, Z angles with perspective; `Rotation3DWidget` on the canvas in `src/Nodus/Photon.Nodus.Desktop/Canvas/Rotation3DWidget.cs`, one command per drag. Done when: a driven run rotates by the widget and the log shows one command.
- [ ] Add `MaterialLibrary` in `src/Nodus/Photon.Nodus.Core/ThreeD/Materials/MaterialLibrary.cs`: built-in parametric PBR materials (base color, roughness, metallic, a normal from procedural noise, emissive) authored in the repository as JSON. Done when: a test loads every built-in material and validates it against the schema.
- [ ] Custom materials saved by the user under `Presets\Materials3D\`; a Substance `.sbsar` file is refused by name with a status message. Done when: tests save a custom material and assert the `.sbsar` refusal text.
- [ ] Graphics mapping: add artwork to the Graphics tab as a symbol reference placed on a chosen surface with scale, rotation, and repeat, through a per-face UV unwrap in `src/Nodus/Photon.Nodus.Core/ThreeD/UvMapper.cs`. Done when: `UvMapperTests` assert no UV overlap on the cube and the mapped art's placement.
- [ ] Lighting: presets Standard, Diffuse, Top Left, and Right; per light color, intensity, rotation, height, and softness through `LightDirectionControl`; multiple lights; ambient. Done when: a test renders each preset's preview golden.
- [ ] Cast shadows with position, distance, and bounds. Done when: a preview golden shows the shadow and moves with the distance setting.
- [ ] Preview: the triangle mesh rasterized with `SKCanvas.DrawVertices` and a shading pass inside `SkiaRenderer`, cached per parameter hash; a 20,000-triangle mesh previews under 33 ms. Done when: `PreviewBenchmarks` asserts the budget.
- [ ] 3D on live text keeps the text object and re-meshes on edit. Done when: a test edits the text after applying 3D and the mesh updates while the text stays editable.
- [ ] Add the 3D and Materials panel in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/Materials3DPanel.xaml` with Object, Materials, and Lighting tabs and the Render button. Done when: a driven run captures each tab to `docs/captures/nodus/3d-materials-panel/`.
- [ ] Add `PathTracer` in `src/Nodus/Photon.Nodus.Core/ThreeD/PathTracer/PathTracer.cs`: an own CPU path tracer with a BVH, GGX microfacet shading, area lights, seeded sampling, and `Parallel.For` tiles. Done when: `PathTracerDeterminismTests` assert the same seed gives identical pixels. Cheaper substitute: a shaded vector preview labelled as ray traced.
- [ ] Prove the path tracer converges: a white furnace test (a white diffuse sphere in a uniform white environment renders uniformly white within tolerance). Done when: `PathTracerConvergenceTests` pass.
- [ ] Render settings quality levels and a denoise pass; the output is an embedded image with the live parameters kept so the render can be redone. Done when: a test renders at low quality and re-renders after a parameter change.
- [ ] Render progress on the status strip with cancel and a completion notification; a medium-quality 1,000 by 1,000 render finishes in under 60 s on 8 cores. Done when: `PathTracerBenchmarks` asserts the budget and a cancellation test leaves the document unchanged.
- [ ] Settings `Nodus.ThreeD.RenderQuality`, `Nodus.ThreeD.RenderThreads`, and `Nodus.ThreeD.PreviewQuality` with consumers in `PathTracer` and the preview. Done when: a test changes each and asserts its consumer reads it.
- [ ] Record the decision in `docs/dev/decisions.md`: an own CPU path tracer, no external renderer, no GPU dependency, and no Substance materials. Done when: the row states each exclusion and its reason.
- [ ] Add `ObjWriter` (with MTL) in `src/Nodus/Photon.Nodus.Core/ThreeD/Export/ObjWriter.cs`. Done when: `ObjWriterTests` export the cube fixture and compare it to the committed golden under `tests/fixtures/nodus/obj/`.
- [ ] Add `GltfWriter` (glTF 2.0 binary) in `src/Nodus/Photon.Nodus.Core/ThreeD/Export/GltfWriter.cs`. Done when: `GltfWriterTests` export fixtures under `tests/fixtures/nodus/gltf/` whose Khronos glTF-Validator reports (version recorded) are committed with zero errors.
- [ ] Add `UsdaWriter` in `src/Nodus/Photon.Nodus.Core/ThreeD/Export/UsdaWriter.cs`. Done when: `UsdaWriterTests` export fixtures under `tests/fixtures/nodus/usda/` whose OpenUSD `usdchecker` reports (version recorded) are committed clean.
- [ ] Add File, Export, 3D Object through the atomic writer, refusing a read-only target by name and reporting progress on the status strip. Done when: a test exports all three formats and a read-only target yields the refusal text.
- [ ] Persist `nodus:materials3d` with the preview image or the rendered image plus expanded faces as the fallback. Done when: `Materials3DRoundTripTests` reopen live and the fallback shows in Inkscape.
- [ ] Every 3D and Materials command logs one Serilog Information line, and each render and export logs its elapsed time. Done when: a test logger asserts the lines.
- [ ] Update `docs/user/nodus/3d.md` for 3D and Materials, rendering, and 3D export. Done when: every tab, control, and export option is listed.
- [ ] Commit: `"nodus: 3D and Materials with an own path tracer and 3D export"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ObjWriterTests|FullyQualifiedName~GltfWriterTests|FullyQualifiedName~UsdaWriterTests"` exports the committed fixtures and matches the validator goldens. Unit test: `PathTracerDeterminismTests` and `PathTracerConvergenceTests` (the white furnace test) pass. Driven run with evidence: the panel tabs and render progress captured under `docs/captures/nodus/3d-materials-panel/`. Cheaper substitute that fails the checkpoint: a vector-shading substitute, which fails the furnace test, and a Substance dependency, which fails the license row.

## 11. Lenses

A lens changes how the art beneath it looks while both stay live; a screenshot pasted into the lens shape goes stale the moment the art beneath moves. This section adds the eleven CorelDRAW lens types with the Lens panel, viewpoint, remove face, frozen lenses, feathered edges, restrictions, copy, and focus mode, rendered vector-exact through the lens shape. Catalog: NP-1612 to NP-1631 (20 features): copy lens from, the Lens panel, brighten, color add, color limit, custom color map, fish eye, heat map, invert, magnify, tinted grayscale, transparency, and wireframe lenses, restrictions, viewpoint, remove face, frozen, editing the lens shape, feathered edges, and lenses in focus mode.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/lens-panel/.
**Job:** a user can place a shape that changes how the art beneath it looks and move it around live. Consumer: the renderer and the SVG writer.
**Treatment:** vector-exact lenses re-render the objects beneath through the lens shape as a clip (magnify, wireframe, and the color lenses as `SKColorFilter`), and fish eye as an `SKRuntimeEffect` warp of the backdrop. Cheaper substitute that fails the checkpoint: a screenshot pasted into the lens shape.
**Chrome:** consume the shared color controls, §1's cache, and the `Photon.UI` panel chrome; do not invent a second color model beside `D02 T09 §1`.

**Requires:** display-session -- lens drags over art, frozen lenses, and viewpoint editing are driven and captured

- [ ] Add `LensEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Lens/LensEffect.cs`: `Type`, rate or amount, color, from and to colors with direct, forward, or reverse rainbow, `Viewpoint`, `RemoveFace`, `Frozen`, and `Feather`. Done when: `LensEffectTests` construct each type and the registry resolves the kind.
- [ ] Add `LensRenderer` in `src/Nodus/Photon.Nodus.Desktop/Rendering/LensRenderer.cs` rendering the document beneath the lens clipped to the lens path. Done when: a render test moves the art beneath and the lens output changes accordingly. Cheaper substitute: a screenshot, which the moved-art test catches.
- [ ] Color lenses as `SKColorFilter`: brighten, color add, color limit, invert, heat map, tinted grayscale, custom color map (direct, forward, reverse rainbow), and transparency. Done when: `LensColorFilterTests` assert per-type color math against reference formulas on sample colors.
- [ ] Magnify (a scale transform about the lens center) and wireframe (outline paint with the lens's outline and fill colors). Done when: goldens for both match within 1 level.
- [ ] Fish eye as an `SKRuntimeEffect` warp of the backdrop, with the rate as its parameter. Done when: a golden matches within tolerance.
- [ ] Viewpoint: an edit handle on the canvas that moves the point the lens looks at without moving the lens. Done when: a test moves the viewpoint and the magnified region follows.
- [ ] Remove Face (the lens affects only objects, not the page background) and Frozen (captures the objects beneath as a frozen group that can be ungrouped into its captured objects). Done when: tests assert both, including ungrouping a frozen lens.
- [ ] Lens edges feather through §8's feather mask; the lens shape stays editable with every shape tool. Done when: a test edits the lens shape's nodes and the lens follows, and a feather golden matches.
- [ ] Restrictions: lenses refuse contour, bevel, extrude, drop shadow groups, and blends with a status message naming the rule. Done when: `LensRestrictionTests` assert each refusal.
- [ ] Add `LensPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/LensPanel.xaml` (Effects, Lens, Alt+F3) with live apply. Done when: a driven run drags a lens over art, captured to `docs/captures/nodus/lens-panel/`.
- [ ] Copy Effect Lens From through §1; focus mode shows the lens and object together through `D02 T07 §7`. Done when: tests cover copy with undo and a driven run captures focus mode.
- [ ] Fallback: color lenses expand to recolored vector copies clipped to the lens shape, magnify to scaled clipped copies, fish eye to node-mapped distorted copies; parameters in `nodus:lens`. Done when: `LensExpandTests` compare the expanded fallback to the live render within 1 level and `LensRoundTripTests` reopen live.
- [ ] Every lens command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/lenses.md`. Done when: every lens type and panel control is listed.
- [ ] Commit: `"nodus: live lenses"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~LensColorFilterTests|FullyQualifiedName~LensExpandTests|FullyQualifiedName~LensRestrictionTests"` exits 0 with snapshot goldens per lens type on `tests/fixtures/nodus/svg/lens/` and the expand-versus-render comparison within 1 level. Format fidelity proof: `LensRoundTripTests` reopen live. Driven run with evidence: a lens dragged over art captured under `docs/captures/nodus/lens-panel/`. Cheaper substitute that fails the checkpoint: a screenshot substitute, which fails when the art beneath changes.

## 12. PowerClip frames

PowerClip puts art inside a frame shape while the contents stay real, editable objects that can come back out; a destructive intersection cannot give them back. This section builds PowerClip frames on the clipping masks of `D02 T08 §11`: place inside, nested and empty frames, drag content in, remove frame, the floating toolbar, select, center, fit, fill, stretch, copy, edit and finish editing, lock, extract, and the PowerClip preferences. It is the first user of the clip path the renderer never applied before. Catalog: NP-1632 to NP-1648 (17 features): copy PowerClip from, place inside frame, nested frames, empty frames, drag into a frame with drop behavior, remove frame, the floating toolbar, select contents, center, fit proportionally, fill proportionally, stretch to fill, edit and finish editing, lock contents, extract contents, auto-center, and empty-frame lines.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/powerclip-toolbar/.
**Job:** a user can put art into a frame shape, position it, and pull it out again. Consumer: the document, the renderer, and the SVG writer.
**Treatment:** a container object whose frame clips its contents at render time and in SVG as a `clipPath`, with the contents kept as real editable objects. Cheaper substitute that fails the checkpoint: destructive intersection of the contents with the frame.
**Chrome:** consume the clipping-mask renderer of `D02 T08 §11`, the floating toolbar pattern in `Photon.UI`, and the settings store; do not invent a second clip implementation.

**Requires:** display-session -- drag into a frame, the floating toolbar, and edit mode are driven and captured

- [ ] Add `PowerClipFrame` in `src/Nodus/Photon.Nodus.Core/Models/Elements/PowerClipFrame.cs`: a group subtype holding the frame path and the contents, with `LockContents` and `IsEmpty`. Done when: `PowerClipModelTests` build nested frames and assert the tree.
- [ ] Render frames with `SKCanvas.ClipPath` (anti-aliased) in `SkiaRenderer` through the clipping-mask renderer of `D02 T08 §11`, including nested frames. Done when: a render golden of a two-level nested fixture matches within tolerance. Cheaper substitute: destructive intersection, which Extract Contents exposes.
- [ ] Empty frames draw an X according to `Nodus.PowerClip.ShowEmptyLines` (always, including print and export, or on screen only). Done when: `PowerClipSettingsTests` assert the X is in the export under "always" and absent under "on screen only".
- [ ] Commands in `src/Nodus/Photon.Nodus.Core/Commands/PowerClip/`: Place Inside Frame, Create Empty Frame, Remove Frame, and Extract Contents. Done when: `PowerClipCommandTests` place, extract, and remove, and extracted contents equal the originals element by element.
- [ ] Lock Contents to PowerClip (contents move with the frame when locked, stay put when unlocked). Done when: a test moves a frame with and without the lock and asserts the contents' positions.
- [ ] Center, Fit Proportionally, Fill Proportionally, and Stretch to Fill. Done when: `PowerClipFitTests` assert the bounds math for each.
- [ ] Copy PowerClip From: copies the picked frame's contents into the selected frame through §1's pick mode. Done when: a test copies and undo restores.
- [ ] Edit PowerClip and Finish Editing (double-click): edit mode shows the frame in wireframe and the contents at full opacity; Select Contents selects them without entering edit mode. Done when: a driven run enters edit mode, moves a content object, and finishes, captured to `docs/captures/nodus/powerclip-toolbar/edit.png`.
- [ ] Drag content onto a frame with `Nodus.PowerClip.DragBehavior` (ignore frame, add content, replace existing); the W key adds to a full frame. Done when: tests assert each behavior.
- [ ] `Nodus.PowerClip.AutoCenter` (when completely outside, always, never) centers new content. Done when: `PowerClipSettingsTests` assert each value.
- [ ] Add `PowerClipToolbar`, a floating control in `src/Nodus/Photon.Nodus.Desktop/Canvas/PowerClipToolbar.xaml` built on the `Photon.UI` floating toolbar pattern: Edit, Select Contents, Extract, Lock, and the fit and center commands. Done when: a driven run captures the toolbar under a selected frame and each button has a view-model test.
- [ ] Write `<g>` plus `<clipPath>` with `nodus:powerclip` parameters so plain viewers show the clip. Done when: `PowerClipRoundTripTests` reopen nested frames as frames and Inkscape renders the clip fallback within tolerance (version recorded).
- [ ] Every PowerClip command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/powerclip.md`. Done when: every command, toolbar button, and preference is listed.
- [ ] Commit: `"nodus: PowerClip frames"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~PowerClipRoundTripTests"` reopens nested frames as frames on `tests/fixtures/nodus/svg/powerclip/`, with Inkscape rendering the clip fallback. Unit test: `PowerClipCommandTests`, `PowerClipFitTests`, and `PowerClipSettingsTests` pass. Driven run with evidence: the floating toolbar and edit mode captured under `docs/captures/nodus/powerclip-toolbar/`. Cheaper substitute that fails the checkpoint: destructive intersection, which fails Extract Contents.

## 13. Symmetry drawing mode

Symmetry drawing mirrors every stroke in real time around up to twelve lines; duplicating once after drawing loses the link the moment the primary changes. This section adds live symmetry groups with create, edit and finish, line count, repositioning and rotation, center, preview, lines, dragging objects in, single-entity transforms, snapping to the lines, fusing open curves, remove, and break link or apart. Catalog: NP-1649 to NP-1661 (13 features): break link and break apart, create, edit and finish, line count, reposition and rotate lines, center X and Y, full preview, show lines, drag objects in, the group as one entity, snap to symmetry lines, fuse open curves, and remove symmetry.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/symmetry-mode/.
**Job:** a user can draw once and see every mirrored copy update in real time. Consumer: the effect stack of §1, the renderer, and the SVG writer.
**Treatment:** copies are generated live from the primary objects by reflection transforms. Cheaper substitute that fails the checkpoint: duplicating once after drawing.
**Chrome:** consume the snapping of `D02 T07 §11`, the floating toolbar pattern shared with §12, and the property bar; do not invent a second edit-mode chrome beside focus mode.

**Requires:** display-session -- drawing inside symmetry edit mode is driven and captured

- [ ] Add `SymmetryGroup` in `src/Nodus/Photon.Nodus.Core/Models/Elements/SymmetryGroup.cs`: primary objects, `LineCount` 1 to 12, `Center`, `Angle`, `ShowFullPreview`, and `ShowLines`; copies are generated on evaluation, never stored except as the fallback. Done when: `SymmetryGroupTests` assert exact copies for line counts 1, 2, 6, and 12.
- [ ] Commands under Object, Symmetry: Create New Symmetry, Edit Symmetry (double-click or Ctrl+click), Finish Editing Symmetry, and Remove Symmetry. Done when: `SymmetryCommandTests` cover each with undo.
- [ ] Break Symmetry Link and Break Symmetry Apart (Ctrl+K) both leave a regular group with the copies as real objects. Done when: tests assert the resulting group equals the expanded fallback element by element.
- [ ] Edit mode overlay: symmetry lines draggable and rotatable, a center handle, and outline-only copies unless full preview is on. Done when: a driven run draws in edit mode, captured to `docs/captures/nodus/symmetry-mode/edit.png`, and each handle drag records one command.
- [ ] Property bar controls: line count, center X and Y, angle, full preview, and show lines. Done when: each control has a view-model test.
- [ ] Snap to Symmetry Lines in View, Snap To (default on) as a snap provider registered with `D02 T07 §11`. Done when: `SymmetrySnapTests` snap a node to a mirror line within 0.01 px.
- [ ] Fuse Open Curves joins an open curve whose ends touch a mirror line with its reflected copy into one closed path. Done when: `FuseOpenCurvesTests` assert one closed path with the expected node count.
- [ ] Drag objects onto a symmetry group to add them as primaries (the W key when the group is not empty). Done when: a test drops an object and asserts it becomes a primary with its copies.
- [ ] The group behaves as a single entity: transforms, fills, outlines, and transparency on the group apply to all copies. Done when: a test fills the group and every copy renders the fill.
- [ ] Editing a primary updates every copy in the same frame. Done when: a test moves a primary node and asserts every copy moved. Cheaper substitute: a one-time duplicate, which this test catches.
- [ ] Persist expanded copies in a `<g>` with `nodus:symmetry` parameters. Done when: `SymmetryRoundTripTests` reopen `tests/fixtures/nodus/svg/symmetry/` live.
- [ ] Every symmetry command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/symmetry.md`. Done when: every command and property bar control is listed.
- [ ] Commit: `"nodus: symmetry drawing mode"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~SymmetryRoundTripTests"` reopens symmetry groups live with snapshot goldens on `tests/fixtures/nodus/svg/symmetry/`. Unit test: `SymmetryGroupTests` and `FuseOpenCurvesTests` pass. Driven run with evidence: drawing in edit mode captured under `docs/captures/nodus/symmetry-mode/`. Cheaper substitute that fails the checkpoint: a duplicate-once substitute, which fails the edit-primary-updates-copies test.

## 14. The perspective grid and drawing planes

Drawing in perspective needs a projective grid model that shape tools draw through, not a guide image to trace over. This section adds a perspective grid with one-, two-, and three-point types, define grid and presets, rulers, snap and lock, on-canvas widgets, active plane switching, and CorelDRAW's Draw in Perspective with its field, camera lines, locking, restricted areas, and horizon and line display. Catalog: NP-1662 to NP-1678 (17 features): the grid tool, one-, two-, and three-point types, show and hide, rulers, snap, lock grid and station point, define grid, presets, the widgets, the active plane and plane switching, hiding the widget, Draw in Perspective, fill page, camera lines, lock field, restricted areas, snap to perspective lines, and horizon and line display.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/perspective-grid/.
**Job:** a user can set up a perspective and draw shapes that land on its planes. Consumer: the shape tools of `D02 T08 §4`, §15's bound objects, and the document.
**Treatment:** a projective grid model with a homography per plane that shape tools draw through. Cheaper substitute that fails the checkpoint: a static guide image.
**Chrome:** consume the snapping providers of `D02 T07 §11`, the guides color settings of `D02 T07 §10`, and the `EffectPresetStore` of §3; do not invent a second snapping engine.

**Requires:** display-session -- grid widgets, plane-switching keys, and drawing on planes are driven and captured

- [ ] Add `PerspectiveGrid` in `src/Nodus/Photon.Nodus.Core/Perspective/PerspectiveGrid.cs`: type (one, two, or three point, with worm and bird eye views), vanishing points, horizon, ground level, viewing angle and distance, gridline spacing, extent, station point, and `Locked`. Done when: `PerspectiveGridTests` build each type and assert its vanishing points.
- [ ] Add `PlaneHomography` per plane (left, right, horizontal, top, side, orthographic) in `src/Nodus/Photon.Nodus.Core/Perspective/PlaneHomography.cs`. Done when: `PlaneHomographyTests` assert grid lines converge on the vanishing points within 0.01 px. Cheaper substitute: a static guide image, which the draw-on-plane test catches.
- [ ] Add `PerspectiveGridTool` (Shift+P) in `src/Nodus/Photon.Nodus.Core/Tools/PerspectiveGridTool.cs` with widgets for vanishing points, horizon, ground level, extent, cell size, viewport resize, and camera lines, each drag one command. Done when: a driven run drags each widget, captured to `docs/captures/nodus/perspective-grid/widgets.png`.
- [ ] The plane-switching widget with keys 1 to 4 (left, horizontal, right, none) and Hide Grid Widget. Done when: a test presses each key and asserts the active plane.
- [ ] Shape tools of `D02 T08 §4` draw through the active plane homography. Done when: `DrawOnPlaneTests` draw a rectangle on each plane and match the goldens.
- [ ] View, Perspective Grid: the One, Two, and Three Point presets, Show or Hide (Ctrl+Shift+I), Show Rulers, Snap to Grid, Lock Grid, and Lock Station Point. Done when: tests toggle each and the state persists with the document.
- [ ] Add the Define Grid dialog, Save Grid as Preset, and the Perspective Grid Presets manager (Edit menu) under `Presets\PerspectiveGrid\`. Done when: `PerspectiveGridPresetTests` round trip a preset and the dialog fields map to the model.
- [ ] CorelDRAW Object, Perspective, Draw in Perspective: a perspective group with a field (drag, or Enter to fill the page). Done when: a test fills the page and asserts the field bounds.
- [ ] Draw in Perspective floating toolbar: type, plane, lock field, show horizon with opacity and color, and show lines with density, opacity, and color. Done when: each control has a view-model test and the display settings persist in the settings store.
- [ ] Camera lines and restricted areas: drawing over vanishing points is refused by name, and Draw in Perspective is unavailable in focus mode with its reason shown. Done when: tests assert both refusals.
- [ ] Snap To Perspective Lines (default on) as a snap provider registered with `D02 T07 §11`. Done when: `PerspectiveSnapTests` snap a node to a grid line.
- [ ] Grid state persists per document in `nodus:perspective-grid`; display colors follow the guides settings of `D02 T07 §10`. Done when: a round-trip test restores the grid and its lock state.
- [ ] Every grid command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/perspective.md` for the grid and Draw in Perspective. Done when: every widget, command, and toolbar control is listed.
- [ ] Commit: `"nodus: the perspective grid and drawing planes"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~PlaneHomographyTests|FullyQualifiedName~PerspectiveGridPresetTests|FullyQualifiedName~PerspectiveSnapTests|FullyQualifiedName~DrawOnPlaneTests"` exits 0 with snapshot goldens of grid rendering and rectangles drawn on each plane on `tests/fixtures/nodus/svg/perspective-grid/`. Format fidelity proof: preset and grid-state round trip. Driven run with evidence: grid widgets and plane switching captured under `docs/captures/nodus/perspective-grid/`. Cheaper substitute that fails the checkpoint: a static guide image, which fails the draw-on-plane test.

## 15. Perspective objects and the Add Perspective effect

Art in perspective must stay editable: text in perspective that is baked into projected outlines can never be retyped. This section binds objects to perspective planes (the perspective selection tool, attach, release, move plane to match, editable text and symbols, perpendicular moves, CorelDRAW perspective groups) and adds the Add Perspective envelope-style effect with one- and two-point node drags, copy, and clear. Catalog: NP-1679 to NP-1698 (20 features): the perspective selection tool, attach and move to plane, release and break apart, move plane to match, editable text and symbols, perpendicular move and copy, copy perspective from, plain-group fallback, edit perspective group, move along a plane, reshape on a plane, transform limits, Add Perspective, one- and two-point node drags, symmetric drags, vanishing point drags, editing with the shape tool, linked groups, flattening by split, crop, or erase, and clear perspective.

**Fidelity:** extends docs/captures/nodus/perspective-grid/.
**Job:** a user can move, scale, and edit art that stays in perspective, or push any object into perspective by dragging its corners. Consumer: the document, the renderer, and the SVG writer.
**Treatment:** objects keep their flat source geometry plus a plane binding, projected on render. Cheaper substitute that fails the checkpoint: baking the projected geometry, so text stops being editable.
**Chrome:** consume §14's grid and homographies and §5's `MeshMap`; do not invent a second projection routine.

**Requires:** display-session -- perspective selection moves, perpendicular moves, and Add Perspective node drags are driven and captured

- [ ] Add `PerspectiveBinding` in `src/Nodus/Photon.Nodus.Core/Perspective/PerspectiveBinding.cs`: plane id, plane offset, and the flat source geometry, evaluated through `PlaneHomography`. Done when: `PerspectiveBindingTests` project a bound rectangle and match the golden.
- [ ] Add `PerspectiveSelectionTool` (Shift+V) in `src/Nodus/Photon.Nodus.Core/Tools/PerspectiveSelectionTool.cs`: move and scale on the plane, Alt-drag copy, arrow keys move along the plane, and the 5 key perpendicular move and copy. Done when: tests assert each gesture's plane offset and position.
- [ ] Commands under Object, Perspective: Attach to Active Plane, Release with Perspective, and Move Plane to Match Object. Done when: tests cover each with undo, and release keeps the projected look as plain geometry.
- [ ] Text and symbols stay live in perspective: Edit Text opens the flat text for editing and re-projects on commit. Done when: `PerspectiveTextEditTests` retype a bound text object and assert the projection updates. Cheaper substitute: baked outlines, which this test catches.
- [ ] CorelDRAW perspective groups: Move to Plane (orthogonal, top, left, right, side), Edit Perspective Group, and Break Perspective Group Apart. Done when: tests cover each with undo.
- [ ] Perspective group limits: move and proportional scale only; rotate, skew, and non-proportional scale are refused with a status message. Done when: tests assert each refusal text.
- [ ] Reshape on a plane: the shape tool reshapes on a temporary orthographic plane and re-projects. Done when: a test moves a node and the flat source changes by the inverse projection.
- [ ] Perspective on linked groups (blends, contours, extrusions) keeps the link live. Done when: a test binds a blend and moving a key object updates the projected blend.
- [ ] Add `AddPerspectiveEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Perspective/AddPerspectiveEffect.cs` (Object, Add Perspective): a four-corner projective map through §5's `MeshMap`. Done when: `AddPerspectiveEffectTests` map a square to a trapezoid and match the golden.
- [ ] Node drags: Ctrl constrains to one-point, a free drag gives two-point, Ctrl+Shift drags symmetrically, and vanishing point handles move the vanishing points. Done when: tests assert each drag's resulting corners.
- [ ] Edit the effect with the shape tool; refuse Add Perspective on paragraph text and bitmaps by name. Done when: tests assert the shape-tool edit and both refusals.
- [ ] Knife, crop, and eraser (`D02 T08 §8`) flatten the effect first with a status note. Done when: a test cuts a perspective object and the status note is shown and the result is plain geometry.
- [ ] Copy Effect Perspective From through §1, and Clear Perspective. Done when: tests cover both with undo.
- [ ] Fallback: projected geometry as plain paths in plain groups so older readers and other viewers get regular groups; parameters in `nodus:perspective`. Done when: `PerspectiveRoundTripTests` reopen `tests/fixtures/nodus/svg/perspective/` with text in perspective still editable.
- [ ] Every perspective command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/perspective.md` for bound objects and Add Perspective. Done when: every tool gesture and command is listed.
- [ ] Commit: `"nodus: perspective objects and the Add Perspective effect"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~PerspectiveRoundTripTests"` reopens `tests/fixtures/nodus/svg/perspective/` with text in perspective editable. Unit test: `PerspectiveBindingTests`, `AddPerspectiveEffectTests`, and `PerspectiveTextEditTests` pass with their snapshot goldens. Driven run with evidence: perpendicular moves and node drags captured under `docs/captures/nodus/perspective-grid/`. Cheaper substitute that fails the checkpoint: a baking substitute, which fails the editable-text check.

## 16. Puppet warp

Puppet warp bends art naturally around pins; moving only the anchors nearest the cursor tears curves and shears shapes. This section adds the Puppet Warp tool with pins, mesh display and expansion, and mesh density, working on vector paths and placed images as a live effect over an as-rigid-as-possible solver. Catalog: NP-1520 to NP-1521 (2 features): the Puppet Warp tool and pins, and the mesh options (show, expand, select all pins).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/puppet-warp/.
**Job:** a user can pin art and drag pins to bend it naturally. Consumer: the effect stack of §1 and the SVG writer.
**Treatment:** as-rigid-as-possible deformation of a triangulated mesh, with path nodes and handles mapped through barycentric coordinates. Cheaper substitute that fails the checkpoint: moving only the nearest anchors.
**Chrome:** consume the property bar and the on-canvas handle overlay; do not invent a second triangulator beside §10's mesh code.

**Requires:** display-session -- pin placement and drags are driven and captured

- [ ] Add `PuppetWarpEffect` in `src/Nodus/Photon.Nodus.Core/Effects/PuppetWarp/PuppetWarpEffect.cs`: pins (rest and current positions, rotation), `MeshDensity`, `ExpandMesh`, and source ids. Done when: the registry resolves the kind and a test constructs pins.
- [ ] Add a constrained Delaunay triangulation of the outline with mesh density and expansion in `src/Nodus/Photon.Nodus.Core/Geometry/Triangulator.cs`, or extend it when §9's cap triangulation already added it: the core holds one triangulator. Done when: `TriangulatorTests` assert every triangle lies inside the expanded outline and density changes the triangle count.
- [ ] Add `ArapSolver` in `src/Nodus/Photon.Nodus.Core/Effects/PuppetWarp/ArapSolver.cs`: a precomputed factorization and an iterative local-global solve. Done when: `ArapSolverTests` assert rigid motion is preserved with two pins and the same input gives identical output. Cheaper substitute: an anchor nudge, which fails the rigidity test.
- [ ] Map path nodes and handles through barycentric coordinates of their containing triangles. Done when: a test warps a circle and every node stays on the deformed mesh.
- [ ] Meet the budget: under 16 ms per drag frame for 2,000 triangles. Done when: `ArapSolverBenchmarks` asserts the budget.
- [ ] Add `PuppetWarpTool` in `src/Nodus/Photon.Nodus.Core/Tools/PuppetWarpTool.cs`: click adds a pin, Alt-drag near a pin rotates, Shift adds to the selection, Delete removes. Done when: tests assert each gesture's pin state.
- [ ] Property bar: Show Mesh, Expand Mesh, mesh density, and Select All Pins. Done when: each control has a view-model test and a driven run captures the mesh to `docs/captures/nodus/puppet-warp/mesh.png`.
- [ ] Commit each drag on mouse-up as one command capturing the pin state. Done when: a test drags a pin and asserts one history entry whose undo restores the rest pose.
- [ ] Placed images warp by `SKCanvas.DrawVertices` on the deformed mesh at render time; expand writes a resampled embedded image. Done when: a render golden of a warped fixture image matches within tolerance.
- [ ] Persist `nodus:puppet-warp` with the expanded geometry as the fallback. Done when: `PuppetWarpRoundTripTests` reopen `tests/fixtures/nodus/svg/puppet-warp/` live.
- [ ] Every puppet warp command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/puppet-warp.md`. Done when: every gesture and property bar control is listed.
- [ ] Commit: `"nodus: puppet warp on an as-rigid-as-possible solver"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ArapSolverTests|FullyQualifiedName~TriangulatorTests"` exits 0 with the rigidity and determinism properties and snapshot goldens on `tests/fixtures/nodus/svg/puppet-warp/`. Format fidelity proof: `PuppetWarpRoundTripTests` reopen live. Driven run with evidence: pin placement and a drag captured under `docs/captures/nodus/puppet-warp/`. Cheaper substitute that fails the checkpoint: an anchor-nudge substitute, which fails the rigidity test.

## 17. Live Paint and smart fill

Live Paint colors the regions formed by overlapping paths as if they were separate shapes while the paths stay editable; running Divide once loses the paths. This section builds a planar map on the intersection kernels of `D02 T08 §10`, Live Paint groups with the bucket and selection tools and gap detection, and the CorelDRAW Smart Fill tool. Catalog: NP-1699 to NP-1709 (11 features): Live Paint make, the bucket with double and triple click, bucket options, the selection tool, merge, release, expand, gap options and show gaps, the Smart Fill tool, its fill and outline options, and filling the outside area.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/live-paint/.
**Job:** a user can color the regions formed by overlapping paths as if they were separate shapes, and keep editing the paths. Consumer: the document, the renderer, and the SVG writer.
**Treatment:** a planar map (the arrangement of all path segments into faces and edges) rebuilt on edit, with fills attached to faces by a stable point sample. Cheaper substitute that fails the checkpoint: running Divide once, which loses the live paths.
**Chrome:** consume the boolean and intersection kernels of `D02 T08 §10` and the swatch cursor preview of `D02 T09 §3`; do not invent a second curve-intersection routine.

**Requires:** display-session -- bucket clicks, double and triple clicks, and gap preview are driven and captured

- [ ] Add `PlanarMap` in `src/Nodus/Photon.Nodus.Core/Geometry/PlanarMap.cs`: segment intersection through the Bezier clipping kernel of `D02 T08 §10`, a half-edge structure, and faces with holes. Done when: `PlanarMapTests` assert face counts on the fixtures and the Euler characteristic.
- [ ] Gap closing by a distance tolerance. Done when: `GapDetectionTests` close a 2 px gap at the medium setting and leave it open at small.
- [ ] Add `LivePaintGroup` in `src/Nodus/Photon.Nodus.Core/Models/Elements/LivePaintGroup.cs`: source paths, face fills, and edge strokes keyed by sample points so edits keep colors where faces persist. Done when: `LivePaintColorStabilityTests` move a path and the surviving faces keep their colors. Cheaper substitute: a one-shot Divide, which this test catches.
- [ ] Commands under Object, Live Paint: Make (Alt+Ctrl+X), Merge, Release (paths with a 0.5 pt black stroke), and Expand (faces and edges to paths). Done when: tests cover each with undo.
- [ ] Add the Gap Options dialog (small, medium, large, custom, preview color, Close Gaps with Paths) and View, Show Live Paint Gaps. Done when: a driven run captures the gap preview to `docs/captures/nodus/live-paint/gaps.png`.
- [ ] Add `LivePaintBucketTool` (K) in `src/Nodus/Photon.Nodus.Core/Tools/LivePaintBucketTool.cs`: paint fills and strokes with the swatch cursor preview of `D02 T09 §3`; double-click fills across unstroked edges; triple-click fills all same-colored faces. Done when: tests assert each click kind's painted faces.
- [ ] Bucket options: paint fills, paint strokes, highlight color and width. Done when: each option has a view-model test and persists in settings.
- [ ] Add `LivePaintSelectionTool` (Shift+L) selecting faces and edges. Done when: a test selects a face and an edge and deletes the face's fill.
- [ ] Add `SmartFillTool` in `src/Nodus/Photon.Nodus.Core/Tools/SmartFillTool.cs`: creates a new filled object from the enclosed area under the click using the planar map of the visible objects. Done when: `SmartFillTests` click inside two overlapping circles and assert the new object equals their intersection.
- [ ] Smart fill fill options (default, specify, none) and outline options (default, specify width and color, none); clicking outside any area creates an object from the outline of all objects on the page. Done when: `SmartFillTests` assert each option and the outside-area result.
- [ ] Meet the budget: a planar map of 2,000 segments builds under 500 ms, moving off the UI thread beyond one second with cancellation and status strip progress. Done when: `PlanarMapBenchmarks` asserts the budget and a cancellation test leaves the document unchanged.
- [ ] Persist expanded face and edge paths with `nodus:livepaint` parameters. Done when: `LivePaintRoundTripTests` reopen `tests/fixtures/nodus/svg/livepaint/` live with colors intact.
- [ ] Every Live Paint and smart fill command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/live-paint.md`. Done when: every tool, command, and option is listed.
- [ ] Commit: `"nodus: Live Paint and smart fill on a planar map"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~LivePaintRoundTripTests"` reopens `tests/fixtures/nodus/svg/livepaint/` live with snapshot goldens. Unit test: `PlanarMapTests`, `LivePaintColorStabilityTests`, `GapDetectionTests`, and `SmartFillTests` pass. Driven run with evidence: bucket fills and the gap preview captured under `docs/captures/nodus/live-paint/`. Cheaper substitute that fails the checkpoint: a one-shot Divide, which fails the edit-a-path-keeps-colors test.

## 18. Repeats and objects on a path

Repeating art radially, in a grid, mirrored, or along a path is only useful when editing the source once updates every instance; static copies made once do not. This section adds live radial, grid, and mirror repeats, Objects on Path, and the CorelDRAW Fit Objects to Path panel with its distribution and rotation options. Catalog: NP-1710 to NP-1726 (17 features): the Objects on Path tool and attach, its options and tool options, detach and expand, radial, grid, and mirror repeats with options, release and expand repeats, and the Fit Objects to Path panel with keep originals, duplicates, group all, treat as contiguous, order, distribution, reference point, and rotation.

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/repeats/ and docs/captures/nodus/fit-objects-to-path/.
**Job:** a user can repeat art radially, in a grid, or mirrored, and lay objects along a path, editing the source once. Consumer: the effect stack of §1, the renderer, and the SVG writer.
**Treatment:** repeat instances are generated live from one source through `SvgUse`-style references. Cheaper substitute that fails the checkpoint: static copies made once.
**Chrome:** consume §3's arc-length table, the `Photon.UI` panel chrome, and the on-canvas handle overlay; do not invent a second path-measuring routine.

**Requires:** display-session -- repeat handles, objects-on-path widgets, and the Fit Objects to Path panel are driven and captured

- [ ] Add `RepeatEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Repeat/RepeatEffect.cs` with `Radial` (instances, radius, reverse overlap). Done when: `RepeatEffectTests` assert 12 instances at the right angles and radius.
- [ ] `Grid` (horizontal and vertical spacing, grid or brick by row or column, flip rows, flip columns) and `Mirror` (axis angle). Done when: `RepeatEffectTests` assert each layout against goldens.
- [ ] On-canvas handles for count, radius, spacing, and axis, each drag one command. Done when: a driven run drags each handle, captured to `docs/captures/nodus/repeats/handles.png`.
- [ ] Object, Repeat: Radial, Grid, Mirror, Options (dialog), Release, and Expand; editing the source in isolation updates every instance. Done when: tests cover each with undo, and editing the source moves every instance. Cheaper substitute: static copies, which the edit-source test catches.
- [ ] Add `ObjectsOnPathEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Repeat/ObjectsOnPathEffect.cs`: attach path id, objects, pivot, rotate, spacing, shuffle seed, and move all, placing by §3's `BlendSpine` arc-length table. Done when: `ObjectsOnPathTests` assert even arc-length spacing within 0.01 px.
- [ ] Add `ObjectsOnPathTool` in `src/Nodus/Photon.Nodus.Core/Tools/ObjectsOnPathTool.cs` with widgets for pivot, rotation, and spacing, and its tool options dialog for the default pivot and rotation. Done when: tests drive each widget's math and the defaults persist in settings.
- [ ] Object, Objects on Path: Attach, Detach, and Expand. Done when: tests cover each with undo; Detach restores the objects' original positions.
- [ ] Add `FitObjectsToPathPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/FitObjectsToPathPanel.xaml` (Object, Fit Objects to Path): keep originals, duplicates, group all, treat as contiguous, and order (selection, reverse, by area, width, height). Done when: a driven run captures the panel to `docs/captures/nodus/fit-objects-to-path/panel.png` and each option has a view-model test.
- [ ] Distribution (uniform gaps or even reference points) and the reference point. Done when: `FitObjectsToPathTests` assert both distributions' positions.
- [ ] Rotation: ignore initial rotation, style (uniform, progressive, jitter, progressive jitter), start angle, spin angle, revolutions, range, and clockwise. Done when: `FitObjectsToPathTests` assert each rotation style.
- [ ] Apply produces real objects as one command. Done when: a test applies and one undo removes every produced object.
- [ ] Persist repeats and objects on a path as live `nodus:repeat` and `nodus:objects-on-path` with `<use>` element fallbacks so plain viewers draw every instance. Done when: `RepeatRoundTripTests` reopen `tests/fixtures/nodus/svg/repeat/` live and Inkscape renders the `<use>` fallback within tolerance (version recorded).
- [ ] Meet the budget: a radial repeat of 360 instances of a 1,000-node source renders from cache at interactive frame rate. Done when: `RepeatBenchmarks` asserts under 16 ms per cached frame.
- [ ] Every repeat and objects-on-path command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/repeats.md`. Done when: every command, handle, and panel option is listed.
- [ ] Commit: `"nodus: live repeats, objects on a path, and Fit Objects to Path"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~RepeatRoundTripTests"` reopens `tests/fixtures/nodus/svg/repeat/` live, with Inkscape rendering the `<use>` fallback. Unit test: `RepeatEffectTests`, `ObjectsOnPathTests`, and `FitObjectsToPathTests` pass with snapshot goldens. Driven run with evidence: repeat handles and the panel captured under `docs/captures/nodus/`. Cheaper substitute that fails the checkpoint: static copies, which fail the edit-source-updates-instances test.

## 19. Path effects: convert to shape, offset, outline, and pathfinder effects

The live path effects apply the same shape and path operations as the destructive commands but keep the sources, so a change to a source updates the result. This section adds Convert to Shape, Offset Path, Outline Object, Outline Stroke, and the Pathfinder effects, all calling the kernels of `D02 T08 §7` and `D02 T08 §10` and §4's `OffsetKernel` on every evaluation. Catalog: NP-1522 to NP-1529 (8 features): convert to shape, offset path, outline object, outline stroke, the live shape modes (add, intersect, exclude, subtract, minus back), the live pathfinders (divide, trim, merge, crop, outline), hard mix, and soft mix.

**Fidelity:** extends the Effect menu captured in docs/captures/nodus/main-window/, plus new dialogs captured to docs/captures/nodus/path-effects/.
**Job:** a user can apply shape and path operations that stay live when the source changes. Consumer: the effect stack of §1 and the SVG writer.
**Treatment:** effects that call the same kernels as the destructive commands of `D02 T08 §7` and `D02 T08 §10` on every evaluation. Cheaper substitute that fails the checkpoint: running the destructive command once and discarding the sources.
**Chrome:** consume the boolean kernels of `D02 T08 §10`, §4's `OffsetKernel`, and the `Photon.UI` dialog chrome; do not invent a second boolean engine.

**Requires:** display-session -- effect dialogs with preview are driven and captured

- [ ] Add `ConvertToShapeEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Path/ConvertToShapeEffect.cs`: rectangle, rounded rectangle, or ellipse; size absolute or relative (extra width and height); corner radius. Done when: `ConvertToShapeEffectTests` assert the result bounds for each mode.
- [ ] Add `OffsetPathEffect` (offset, joins, miter limit) through §4's `OffsetKernel`. Done when: `OffsetPathEffectTests` assert the live result equals the destructive `D02 T08 §7` command output node for node.
- [ ] Add `OutlineStrokeEffect` through a stroke-to-path kernel that replaces the `PathOperationsService.StrokeToPath` placeholder. Done when: the placeholder text is gone from `src/Nodus/Photon.Nodus.Core/Services/PathOperationsService.cs` and a test asserts the outline area of a stroked line.
- [ ] Add `OutlineObjectEffect`: text is treated as its outlines for alignment and following effects while the text stays live. Done when: a test aligns an outlined text object by its glyph bounds and the text remains editable.
- [ ] Add `PathfinderEffect` in `src/Nodus/Photon.Nodus.Core/Effects/Path/PathfinderEffect.cs` on a group: add, intersect, exclude, subtract, minus back, divide, trim, merge, crop, and outline. Done when: `PathfinderEffectTests` assert each operation matches the destructive `D02 T08 §10` command output node for node. Cheaper substitute: run once and discard the sources, which the edit-source test catches.
- [ ] Hard mix (component-wise maximum in overlaps) and soft mix (mixing rate) on fills. Done when: `MixEffectTests` assert the overlap colors against reference formulas.
- [ ] Pathfinder options (precision, remove redundant points, divide and outline remove unpainted artwork) shared with the settings of `D02 T08 §10`. Done when: a test changes precision in one place and both the command and the effect read it.
- [ ] Add the dialogs for Convert to Shape, Offset Path, and Pathfinder options under `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/Path/` with Preview through §1's cache. Done when: a driven run captures each to `docs/captures/nodus/path-effects/`.
- [ ] Editing a source path updates the live result. Done when: a test moves a source node under each effect and the result changes.
- [ ] Fallback: the result geometry as plain paths with the source group kept in `nodus:pathfinder` (and `nodus:effect` for the others) so a reopen restores the live group. Done when: `PathEffectRoundTripTests` reopen `tests/fixtures/nodus/svg/path-effects/` live.
- [ ] Every path effect command logs one Serilog Information line. Done when: a test logger asserts one line per command.
- [ ] Update `docs/user/nodus/effects.md` with the path effects. Done when: every effect and dialog field is listed.
- [ ] Commit: `"nodus: live path effects and pathfinder effects"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~PathfinderEffectTests|FullyQualifiedName~OffsetPathEffectTests|FullyQualifiedName~ConvertToShapeEffectTests|FullyQualifiedName~MixEffectTests"` exits 0 with the equivalence tests against the `D02 T08 §10` commands. Format fidelity proof: `PathEffectRoundTripTests` reopen `tests/fixtures/nodus/svg/path-effects/` live. Driven run with evidence: the dialogs captured under `docs/captures/nodus/path-effects/`. Cheaper substitute that fails the checkpoint: a run-once substitute, which fails the edit-source-updates-result test.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every test class this file added reporting
- [ ] Every effect fixture under `tests/fixtures/nodus/svg/` that this file commits reopens live and its expanded fallback renders within tolerance of its golden; the OBJ, glTF, and USDA fixtures pass their validators
- [ ] Every catalog row with status `plan D02 T11 §N` in `docs/parity/nodus-parity.md` (NP-1432 to NP-1726) names a section of this file whose row is `[x]`
- [ ] `src/Nodus/Photon.Nodus.Core/Services/PathOperationsService.cs` no longer carries the offset or stroke-to-path placeholder text this file replaces (§4, §19)
- [ ] The Nodus user guide pages under `docs/user/nodus/` for effects, blends, contours, envelopes, distortions, shadows, stylize, 3D, lenses, PowerClip, symmetry, perspective, puppet warp, Live Paint, and repeats exist and match the shipped surfaces
- [ ] `python scripts/todo-graph.py validate` clean
