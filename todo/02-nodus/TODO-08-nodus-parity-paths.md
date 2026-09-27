---
schema_version: 1
id: nodus-parity-paths
domain: 02-nodus
status: draft
title: "TODO-08 -- Nodus Parity: Drawing, Paths, Shapes, Shaping, and Transform"
depends_on: []
track: N8
---

# TODO-08 -- Nodus Parity: Drawing, Paths, Shapes, Shaping, and Transform

> **Goal:** Give Nodus the full drawing and geometry toolset of Illustrator 30.8 and CorelDRAW 2026: every pen, curve, freehand, and shape tool; parametric live shapes and corners; node-level editing, cutting, and shaping brushes; the complete Pathfinder and shaping set with compound paths and clipping; numeric and interactive transforms, align, arrange, and step and repeat; and associative dimensions and connectors, each edit one undoable command and every live object persisted through the `nodus:` namespace with a plain-SVG fallback.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Nine tools derive from `ToolBase` today (select, pen, node edit, rectangle, ellipse, line, text, pan, zoom); there is no polygon, star, spiral, pencil, knife, eraser, transform, dimension, or connector tool (`PolygonTool.cs` and `PencilTool.cs` are absent). The pen tool is one 453-line file with Escape, Enter, and Backspace handling and no rubber band, continue, or auto add and delete; the node edit tool is one 700-line file whose keys 1, 2, and 3 convert nodes to corner, smooth, and symmetric, the only three `ControlPointType` values. `PathOperationsService` carries nine `Placeholder` markers (offset, simplify, stroke to path, bounds, split, and flatten among them). `ToolPoint` carries only X and Y: no pressure, tilt, or bearing reaches a tool. `SvgClipPath` and `SvgMask` model classes exist, but `SvgParser.cs` never reads `clipPath` and `SkiaRenderer` never clips. `AlignmentService` is ten static methods and `TransformService` is 201 lines of resize, rotate, snap-angle, and scale math. No connector code exists in core services. The Object menu's Transform submenu holds only the fixed 90 and 180 degree rotations and the two flips. Paths below name the post-rename `Photon.Nodus.*` projects (`D02 T01 §1`); the claims name today's `Bezier.*` paths.
<!-- claim: count ": ToolBase" src/Nodus/Bezier.Core/Tools/*.cs = 9 -->
<!-- claim: absent src/Nodus/Bezier.Core/Tools/PolygonTool.cs -->
<!-- claim: absent src/Nodus/Bezier.Core/Tools/PencilTool.cs -->
<!-- claim: lines src/Nodus/Bezier.Core/Tools/PenTool.cs = 453 -->
<!-- claim: lines src/Nodus/Bezier.Core/Tools/NodeEditTool.cs = 700 -->
<!-- claim: count "^    (Corner|Smooth|Symmetric),?$" src/Nodus/Bezier.Core/Models/ControlPoint.cs = 3 -->
<!-- claim: count "Placeholder" src/Nodus/Bezier.Core/Services/PathOperationsService.cs = 9 -->
<!-- claim: count "Pressure" src/Nodus/Bezier.Core/Interfaces/ITool.cs = 0 -->
<!-- claim: count "clipPath" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->
<!-- claim: count "SvgClipPath" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->
<!-- claim: count "public static" src/Nodus/Bezier.Core/Services/AlignmentService.cs = 10 -->
<!-- claim: lines src/Nodus/Bezier.Core/Services/TransformService.cs = 201 -->
<!-- claim: count "Connector" src/Nodus/Bezier.Core/Services/*.cs = 0 -->
<!-- claim: count "Rotate _180" src/Nodus/Bezier.Desktop/Views/MainWindowView.xaml = 1 -->

## Inputs

- [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) -- the catalog rows each section owns (`NP-` ranges named in each context paragraph)
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- the design these sections were authored from
- [`standards/nodus.md`](../../standards/nodus.md) -- tools derive from `ToolBase`, record their edits as commands, and follow the modifier norm (Shift constrains, Alt from center, Space pans)
- [`standards/shared.md`](../../standards/shared.md) -- settings, logging, performance budgets, and the design contract
- `src/Nodus/Bezier.Core/Tools/PenTool.cs`, `NodeEditTool.cs`, `Services/PathOperationsService.cs`, `AlignmentService.cs`, `TransformService.cs` -- the code §1, §6, §7, §12, and §14 extend
- -> XREF: D02 T06 §2 -- continue, join, break, reverse, simplify, and stroke to path: the node model every section here extends
- -> XREF: D02 T02 §4 -- align, arrange, rotate, and flip wired with `CompositeCommand`, which §12 and §14 extend
- -> XREF: D02 T02 §5 -- booleans on `SKPath.Op` and `ElementToPathConverter`, which §10 builds on
- -> XREF: D02 T03 §1 -- resize and rotate drags recorded as undo steps, the pattern §13 follows
- -> XREF: D02 T07 §1 -- the live-object contract live shapes, generators, compound shapes, intertwine, dimensions, and connectors persist under
- -> XREF: D02 T07 §8 -- the Properties panel and property bar that host every tool option
- -> XREF: D02 T07 §9 -- units and drawing scale for dimensions and field math
- -> XREF: D02 T07 §6 -- Select Same and deep select, the selection half of backlog B-006
- -> XREF: D02 T07 §11 -- the snapping modes the drawing tools consume
- -> XREF: D01 T02 §2 -- the settings store every tool default goes through
- -> XREF: D02 T09 §16 -- the brush engine on §3's fitted strokes
- -> XREF: D02 T11 §12 -- PowerClip on §11's clipping
- -> XREF: D02 T11 §17 -- Live Paint on §10's planar faces
- -> XREF: D02 T11 §19 -- pathfinder effects on §10's operations
- -> XREF: D02 T14 §10 -- DXF dimensions from §15
- -> XREF: D02 T16 §8 -- pen, touch, and dial input preferences over the stylus fields §3 adds
- -> XREF: D02 T17 §2 -- Nodus 0.3.0 releases this file
- -> XREF: D03 T09 §12 -- Imago parity layers cites §14: Nodus's align and distribute math, moved to `Photon.Core` by D03 T09 §12
- -> XREF: D03 T16 §6 -- Imago parity type and vectors cites §1: pen math D03 T16 §6 moves; §4: live-shape generators D03 T16 §7 moves; §6: node operations D03 T16 §6 moves; §7: curve actions D03 T16 §6 moves; §10: path geometry and booleans D03 T16 §5 moves

## Outcome

- Every pen, curve, line, arc, freehand, and smart-drawing tool both competitors ship draws in Nodus, each finished path one command, with stylus pressure, tilt, and bearing reaching the tools that use them.
- Rectangles, ellipses, polygons, stars, spirals, grids, flares, common shapes, and impact effects stay editable by their parameters after save and reopen, and render as plain SVG in Inkscape.
- Node editing, cutting, erasing, cropping, and the liquify and shape-editing brushes change real path geometry, each drag or stroke one undo step.
- Pathfinder, shaping, the Shape Builder, compound paths, clipping masks, draw inside, and intertwine produce and release real geometry, with `clipPath` read, rendered, and written.
- Transforms by number and by tool, Transform Again, Transform Each, align, distribute, arrange, and Step and Repeat place objects exactly, each apply one command.
- Dimensions and connectors stay attached to what they measure or connect and update when it moves.

**Adjacency:** list=applicable @ D02 T08 §5; document=not-applicable (this file produces geometry; printing and PDF output are D02 T13 §2 and D02 T13 §14); settings=applicable; reporting=applicable @ D02 T08 §7; notifications=applicable @ D02 T08 §10; permissions=applicable @ D02 T08 §14; audit=applicable; exchange=applicable @ D02 T08 §4; reverse=applicable

**Adjacency rationale:** The Common Shapes picker, the Coordinates object list, and the Pathfinder operation list are findable by name; tool search rides `D02 T16 §3`. Every tool default, the constrain angle, node display, eraser and knife defaults, and dimension and connector defaults go through the settings store with a named reading tool. The status-strip length, angle, and node count readouts of §2 and §6 and the Clean Up result count of §7 are the reports. Pathfinder, Shape Builder, Divide Objects Below, and Step and Repeat runs over a second report progress and completion on the status strip with cancel. Locked layers and locked objects refuse shaping, cutting, and reordering with a named status message, and §14 owns the locked layer order rule. Every tool stroke, node edit, shaping operation, and transform is one named history entry and one Serilog Information line. Live shapes, compound shapes, clipping, intertwine, dimensions, and connectors round-trip through SVG with `nodus:` parameters and plain fallbacks, and paths paste as SVG between documents. Every create has undo, and Expand Shape, Release Compound Path, Release Clipping Mask, Release Intertwine, Break Dimension Apart, Break Callout Apart, and Clear Transformations are the explicit reverses.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Pen, Bezier, and anchor point tools | D02 T06 §2 |  [ ]   |
|   2   |   §2    | Curvature, B-spline, polyline, 3-point, line and arc tools, parallel drawing | §1 |  [ ]   |
|   3   |   §3    | Pencil, freehand, smooth, path eraser, join, and smart drawing | §1 |  [ ]   |
|   4   |   §4    | Live shapes and live corners | D02 T07 §1, D02 T07 §8 |  [ ]   |
|   5   |   §5    | Grid, graph paper, flare, common shapes, and impact tools | §4 |  [ ]   |
|   6   |   §6    | Node editing: types, transforms, align, distribute, reduce | D02 T06 §2 |  [ ]   |
|   7   |   §7    | Join curves, average, offset, anchors, clean up, split into grid | §6 |  [ ]   |
|   8   |   §8    | Knife, scissors, eraser, virtual segment delete, crop | §6 |  [ ]   |
|   9   |   §9    | Liquify and shape-editing brushes | §6 |  [ ]   |
|  10   |   §10   | Pathfinder, shaping, and the shape builder | D02 T02 §5, D02 T07 §1 |  [ ]   |
|  11   |   §11   | Compound paths, clipping masks, draw inside and behind, intertwine | §10 |  [ ]   |
|  12   |   §12   | The Transform panel, dialogs, Transform Again, Transform Each | D02 T07 §8 |  [ ]   |
|  13   |   §13   | Rotate, reflect, scale, shear, reshape, and free transform tools | §12 |  [ ]   |
|  14   |   §14   | Align, distribute, arrange, and step and repeat extensions | §12 |  [ ]   |
|  15   |   §15   | Dimensions, connectors, and callouts | D02 T07 §9, D02 T07 §1 |  [ ]   |

---

## 1. Pen, Bezier, and Anchor Point Tools

The pen draws, but a designer correcting a path mid-stroke needs the rubber band, Space-move, Alt conversion, auto add and delete, continue and connect, and CorelDRAW's Bezier mode, without switching tools and without a second path engine. Every section here extends the `D02 T06 §2` node model; this one extends the pen. It must not change what a finished path is: one command per finished path. Catalog: NP-0331 to NP-0344 (click and drag anchors, rubber band, Space-drag, Alt anchor toggle, auto add and delete, continue and connect, the Add, Delete, and Anchor Point tools, the Bezier tool, angle constraint, hide bounding box after curve tools, node tracking, and freehand and Bezier defaults).

**Fidelity:** Nodus canvas and tool rail, Pen flyout -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/pen-tool/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/Tooltip/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Nodus canvas and tool rail, Pen flyout -- docs/captures/nodus/main-window/; overlay states captured to docs/captures/nodus/pen-tool/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can draw and correct Bezier paths node by node without switching tools. Consumer: the document and the node model.
**Treatment:** live rubber band and handle overlays drawn by the tool's `RenderOverlay`, one command per finished path. Cheaper substitute that fails the checkpoint: committing each click as its own element.
**Chrome:** consume the tool rail flyout, the `D02 T07 §8` property bar, the shared icon catalog, and the history. Do not add a second options strip.

**Requires:** display-session -- pen drawing, hover add and delete, and overlay captures need an interactive desktop

- [ ] Add a rubber-band preview segment from the last anchor to the pointer in `src/Nodus/Photon.Nodus.Core/Tools/PenTool.cs`, on by default under `Nodus.Tools.Pen.RubberBand`. Done when: `PenToolParityTests.RubberBandState` asserts the preview segment and the setting turns it off.
- [ ] Hold Space during a drag to move the anchor being placed (`PenTool.OnMouseMove` offsets the pending `ControlPoint`). Done when: `PenToolParityTests.SpaceMovesAnchor` moves the pending anchor without changing its handles.
- [ ] Hold Alt to convert or break the current handle as the Anchor Point tool does. Done when: an Alt-drag on the last anchor produces a cusp in a test.
- [ ] Add auto add and delete on hover: hit-test segments and anchors of the selected path through the `D02 T06 §2` node model, under `Nodus.Tools.Pen.AutoAddDelete` (true), Shift suspending it. Done when: `PenToolParityTests.AutoAddDelete` asserts node counts after a hover-click on a segment and on an anchor.
- [ ] Continue a path by clicking any open endpoint, and connect by closing onto another path's endpoint through the `D02 T06 §2` join as one `CompositeCommand`. Done when: `PenToolParityTests.ContinueAndJoin` joins two paths into one with the summed node count. Cheaper substitute: grouping the two paths.
- [ ] Add `PenMode.Bezier`: click places a straight node, drag pulls handles, double-click the last node forces the next segment straight, and Space finishes, as CorelDRAW's Bezier tool on the same engine. Done when: `PenToolParityTests.BezierMode` covers each gesture.
- [ ] Add `AddAnchorPointTool`, `DeleteAnchorPointTool`, and `AnchorPointTool` in `src/Nodus/Photon.Nodus.Core/Tools/`, registered in the Pen flyout with `+`, `-`, and Shift+C. Done when: `AnchorPointToolTests` cover add, delete, convert, and break, and the flyout capture is committed.
- [ ] Constrain segment and handle angles with Shift (and Ctrl in the CorelDRAW keymap) to `Nodus.Tools.ConstrainAngle` (15) through `TransformService.SnapAngle`. Done when: `PenToolParityTests.ConstrainAngle` asserts 15-degree multiples.
- [ ] Add `Nodus.Tools.NodeTracking` letting the pen, Bezier, and select tools grab a hovered node, and `Nodus.Tools.HideBoundingBoxAfterCurve` hiding the selection box after curve tools. Done when: each setting has a test proving its reader changes behavior.
- [ ] Add the `Nodus.Tools.Curve.*` settings group (smoothing, corner threshold, straight-line threshold, auto-join distance) read by §1, §2, and §3. Done when: every key has a named reader and a default in `docs/dev/nodus/settings.md`.
- [ ] Register the pen's options template with the `D02 T07 §8` property bar. Done when: selecting the pen shows rubber band, auto add and delete, and mode fields.
- [ ] Add `tests/Photon.Nodus.Tests/Tools/PenToolParityTests.cs` and `AnchorPointToolTests.cs`. Done when: both classes run in `dotnet test`.
- [ ] Add a Pen and Anchor Tools page to `docs/user/nodus/`. Done when: every gesture and setting is listed.
- [ ] Commit: `"nodus: the pen at parity, Bezier mode, and the anchor point tools"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~PenToolParityTests|FullyQualifiedName~AnchorPointToolTests"` exits 0; a driven run draws, continues, and joins two paths with undo restoring each step (log lines quoted, capture under `docs/captures/nodus/pen-tool/`). Cheaper substitute that fails: a join that groups the two paths, which the node-count assertion catches.

## 2. Curvature, B-Spline, Polyline, 3-Point Curve, Line and Arc Tools, and Parallel Drawing

Each drawing method suits a different shape: interpolating curves, precise lines and arcs, B-splines, polylines, and three-point curves, plus CorelDRAW's parallel drawing mode. Each tool owns its overlay and writes one path command; parallel mode writes the source and its offsets as one entry. The arc tool closes the arc part of backlog B-001 (the other B-001 shapes land in §4, which carries the entry's source key; the entry left the backlog when this file was integrated). Catalog: NP-0345 to NP-0364 (the curvature, line segment, arc, 2-point line, B-spline, polyline, and 3-point curve tools with their options and modifiers, perpendicular and tangential lines, clamped and floating B-spline points, auto-close, the length and angle readout, and parallel drawing with count, side, distance, preview, and from a selected path).

**Fidelity:** Tool rail flyouts and property bar -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/line-arc-options/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/Canvas/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail flyouts and property bar -- docs/captures/nodus/main-window/; new dialogs captured to docs/captures/nodus/line-arc-options/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can draw precise lines, arcs, and smooth curves by the method each shape suits. Consumer: the document.
**Treatment:** each tool owns its overlay and writes one path command; parallel mode writes the source and its offsets as one entry. Cheaper substitute that fails the checkpoint: parallel lines drawn as a stroke effect that does not produce separate editable paths.
**Chrome:** consume the `D02 T07 §8` property bar, the status strip readout slot, and the history.

**Requires:** display-session -- driving each drawing tool and capturing its overlay needs an interactive desktop

- [ ] Add `CurvatureTool` in `src/Nodus/Photon.Nodus.Core/Tools/CurvatureTool.cs`: an interpolating curve through clicked points (Catmull-Rom converted to cubic Beziers), double-click or Alt-click for a corner, and drag an existing point to move it. Done when: `CurvatureToolTests` assert the curve passes through every clicked point within 0.01 px.
- [ ] Add `LineSegmentTool` with `LineSegmentOptionsDialog` (length, angle, fill) opened on click. Done when: a typed 100 px at 30 degrees produces the exact endpoint.
- [ ] Add `ArcTool` with `ArcOptionsDialog` (X and Y lengths, open or closed, base axis, slope, fill) and drag modifiers C, F, and the arrow keys. Done when: `ArcGeometryTests` check the radius at sampled points of a drawn arc.
- [ ] Add `TwoPointLineTool` with perpendicular and tangential modes built on the `D02 T07 §11` perpendicular and tangent snap points, Ctrl extending past the target. Done when: a tangential line to a circle touches it at the analytic tangent point.
- [ ] Add `BSplineTool`: a uniform cubic B-spline converted to Bezier segments for rendering, V while clicking clamps a point, and the control polygon stored as `nodus:bspline` through the `D02 T07 §1` contract so §6 can edit it. Done when: `BSplineConversionTests` match a reference evaluation within 0.01 px.
- [ ] Add `PolylineTool`: click straight, drag curve, Alt draws circular arcs, Ctrl+Alt constrains the arc angle, double-click finishes. Done when: `PolylineArcTests` assert arc radii.
- [ ] Add `ThreePointCurveTool`: start, end, then bend point, Ctrl for a circular curve and Shift for a symmetrical one. Done when: `ThreePointCurveTests` cover both modifiers.
- [ ] Add the auto-close toggle on the property bar (`Nodus.Tools.Curve.AutoClose`). Done when: finishing with it on yields a closed path.
- [ ] Add a status-strip readout of segment length, angle, and total length in document units from `D02 T07 §9`. Done when: drawing a 1-inch line in inch units reads `1 in`.
- [ ] Add `ParallelDrawingOptions` (count, left, right, both, distance, preview) applied through `PathOperationsService.Offset` (§7) after each supported tool finishes, source and offsets recorded as one command. Done when: `ParallelDrawingTests` measure the offset distance at five sample points. Cheaper substitute: a stroke effect.
- [ ] Add Create Parallel from Selected, which adds offsets to an existing open path. Done when: the command adds the configured count as separate paths.
- [ ] Register each tool's options template with the property bar and its icon in the tool rail flyout. Done when: every tool shows its fields and the flyout is captured.
- [ ] Add a Lines, Arcs, and Curves page to `docs/user/nodus/`. Done when: each tool and modifier is listed.
- [ ] Commit: `"nodus: the curvature, line, arc, B-spline, polyline, and 3-point curve tools with parallel drawing"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~CurvatureToolTests|FullyQualifiedName~BSplineConversionTests|FullyQualifiedName~PolylineArcTests|FullyQualifiedName~ThreePointCurveTests|FullyQualifiedName~ParallelDrawingTests|FullyQualifiedName~ArcGeometryTests"` exits 0; a driven run draws one of each tool with parallel mode on (capture under `docs/captures/nodus/line-arc-options/`, log lines quoted). Cheaper substitute that fails: arcs approximated by polylines, which `ArcGeometryTests` catches by checking the radius at sampled points.

## 3. Pencil, Freehand, Smooth, Path Eraser, Join Tool, and Smart Drawing

Hand sketching needs raw input kept until release and then fitted to clean cubics, plus the tools that refit, erase, and join spans, local shape recognition, and CorelDRAW's LiveSketch. Stylus pressure, tilt, and bearing reach the tools for the first time here. Recognition is a local algorithm: no model and no network. Promoted from backlog B-008: the pencil and path eraser land here, the object eraser in §8, and the variable-width brush in `D02 T09 §17` (the entry left the backlog when this file was integrated). Catalog: NP-0365 to NP-0387 (the pencil and freehand tool, fidelity and smoothing, straight segments, extend, reshape, and connect, live preview, the Smooth, Path Eraser, and Join tools, shape recognition and the Shaper group, LiveSketch and all its options, erase back, stylus eraser flip, recognition level and delay, smart smoothing, corrections, and outline width). -> SOURCE: legacy-nodus-3.6

**Fidelity:** Tool rail and property bar -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/freehand/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/Slider/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail and property bar -- docs/captures/nodus/main-window/; recognition overlays captured to docs/captures/nodus/freehand/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can sketch by hand and get clean, editable curves and shapes. Consumer: the document and the `D02 T09 §16` brush engine.
**Treatment:** raw input points kept until release (or the LiveSketch timer) then fitted to cubics as one command. Cheaper substitute that fails the checkpoint: storing the raw polyline, which the node-count bound catches.
**Chrome:** consume the property bar, the stylus input service, and the history. Do not build a private stroke recorder in the view.

**Requires:** display-session -- freehand strokes and stylus input need an interactive desktop

- [ ] Add `Pressure`, `Tilt`, and `Bearing` to `ToolPoint` in `src/Nodus/Photon.Nodus.Core/Interfaces/ITool.cs`, defaulting to 1.0 and 0 for mouse input. Done when: existing tool tests pass unchanged.
- [ ] Fill the stylus fields from WPF `StylusPoint` in the canvas input path in `src/Nodus/Photon.Nodus.Desktop/Controls/Canvas/SkiaCanvas.cs`. Done when: a test with a synthetic `StylusPointCollection` delivers pressure 0.5 to the tool (source: Microsoft Learn, `StylusPoint.PressureFactor`).
- [ ] Add `CurveFitter` in `src/Nodus/Photon.Nodus.Core/Geometry/CurveFitter.cs`: Schneider's least-squares cubic fitting (Graphics Gems, 1990) with an error tolerance mapped from the fidelity or smoothing slider and corner detection by angle threshold. Done when: `CurveFitterTests` replay a committed trace under `tests/fixtures/nodus/input-traces/` within the max-deviation and node-count bounds.
- [ ] Add `PencilTool` (the Corel Freehand keymap alias) with Alt or click-click for straight segments and Shift constraining to 45 degrees. Done when: `PencilToolTests.StraightSegments` pass.
- [ ] Make the pencil extend a selected path when drawing near its end, reshape it when drawing over it, and join when ending on another end. Done when: `PencilToolTests.ExtendReshapeJoin` pass.
- [ ] Add erase back while drawing (Shift-drag backward) and a pencil options dialog with `Nodus.Tools.Pencil.*` keys (fidelity, smoothing, keep selected, close when near). Done when: erasing back removes the retraced span before release.
- [ ] Add live preview of the fitted curve with the element's stroke style while drawing (`Nodus.Tools.Pencil.LivePreview`, true). Done when: the preview is captured under `docs/captures/nodus/freehand/`.
- [ ] Add `SmoothTool` that refits the scrubbed span with a looser tolerance. Done when: a scrub over a noisy span reduces its nodes and keeps the endpoints.
- [ ] Add `PathEraserTool` that splits and removes the scrubbed span. Done when: erasing the middle of a line leaves two open paths.
- [ ] Add `JoinTool` that extends or trims both ends when scrubbed over a gap or overlap, and joins them. Done when: `JoinToolTests` join a gap and trim an overlap.
- [ ] Add `ShapeRecognizer` in `src/Nodus/Photon.Nodus.Core/Geometry/ShapeRecognizer.cs`: corner detection plus least-squares fits for line, rectangle, ellipse, triangle, and polygon, and scribble detection for delete and merge, with no model and no network. Done when: `ShapeRecognizerTests` map ten recorded gestures to their expected shape kinds.
- [ ] Add the Shaper group: the recognizer's merge and punch results persist as a live `nodus:shaper` group whose faces can be edited and restored through `D02 T07 §1`. Done when: a Shaper group reopens live and restoring a face brings it back.
- [ ] Add smart drawing options: recognition level, delay (10 ms to 2 s), smart smoothing for unrecognized strokes, outline width, and Esc removing the last curve, each a `Nodus.Tools.SmartDrawing.*` key. Done when: each key has a named reader.
- [ ] Add `LiveSketchTool` reusing `CurveFitter`: pending strokes merged after a timer of 0 to 5 s, include existing curves within 0 to 40 px, single-curve mode, preview, and smoothing. Done when: `LiveSketchTests` merge two strokes into one curve after the timer.
- [ ] Add the LiveSketch stylus eraser flip and inheritance of the re-sketched curve's properties. Done when: flipping a synthetic stylus erases a pending stroke and a re-sketch keeps the original stroke color.
- [ ] Add a Freehand and Smart Drawing page to `docs/user/nodus/`. Done when: every tool and option is listed.
- [ ] Commit: `"nodus: pencil, freehand fitting, smooth, path eraser, join, shape recognition, and LiveSketch"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~CurveFitterTests|FullyQualifiedName~ShapeRecognizerTests|FullyQualifiedName~PencilToolTests|FullyQualifiedName~LiveSketchTests"` exits 0 replaying the committed input traces; a driven stylus or mouse run's fitted result is saved and inspected (node count quoted). Cheaper substitute that fails: keeping every raw input point, which the node-count bound catches.

## 4. Live Shapes: Rectangle, Ellipse, Polygon, Star, Spiral, and Live Corners

Shapes that stay editable by their parameters after save and reopen, set by number or by on-canvas widget, and live corners on any path. This is the first consumer of the `D02 T07 §1` contract. Promoted from backlog B-001: polygon, star, and spiral with parameters editable after creation land here (the arc in §2), persisted through `D02 T07 §1` rather than `data-nodus-*` attributes (the entry left the backlog when this file was integrated). Natural split if it overruns 30 items: the Coordinates panel as a new section after §15 depending on §4 (not needed at authoring: the panel is one item with numbered sub-steps). Catalog: NP-0388 to NP-0425 (the spiral, rectangle, rounded rectangle, ellipse, polygon, star, 3-point rectangle, and 3-point ellipse tools, the shape options dialog, draw modifiers, live shapes with widgets, live corners and their types, rounding, hide above an angle, per-corner radius, scale corners, parameters surviving transforms, pie and arc, sides and points, star radii, sharpness, and perfect and complex stars, reshape a polygon into a star, spiral revolutions and expansion, Shape Properties, Convert to Shapes, Expand Shape, the Coordinates panel and every shape it creates, the Corners panel, and the corner skip rule). -> SOURCE: legacy-nodus-3.2

**Fidelity:** Tool rail, canvas widgets, and property bar -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/corners-panel/, docs/captures/golden/nodus/coordinates-panel/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/Panel/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail, canvas widgets, and property bar -- docs/captures/nodus/main-window/; new panels captured to docs/captures/nodus/corners-panel/ and docs/captures/nodus/coordinates-panel/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can draw shapes that stay editable by their parameters and set them by number. Consumer: the document, the SVG writer, and every later effect.
**Treatment:** shapes stored as live objects with parameters and expanded geometry. Cheaper substitute that fails the checkpoint: a polygon written as a plain path that loses its side count on reopen.
**Chrome:** consume the `D02 T07 §8` Properties panel for Shape Properties, the shared number boxes, the dock, and the history. Do not build a second property grid.

**Requires:** display-session -- widget dragging and panel captures need an interactive desktop

- [ ] Add the `LiveShape` hierarchy in `src/Nodus/Photon.Nodus.Core/Shapes/LiveShape.cs` implementing `ILiveObject`: `LiveRect` (per-corner type and radius), `LiveEllipse` (start and end angle, arc or pie, direction), `LivePolygon`, `LiveStar` (inner and outer radius, sharpness, complex flag), and `LiveSpiral` (revolutions, decay, logarithmic expansion), registered with `LiveObjectRegistry`. Done when: each kind writes and reopens through the registry.
- [ ] Keep `SvgRect` and `SvgEllipse` native when no extra parameter is set. Done when: a plain rectangle saves as `<rect>` with no `nodus:` attributes.
- [ ] Extend `RectangleTool` and `EllipseTool` to create live shapes and add `RoundedRectangleTool`, with double-click on the rectangle tool creating a page-sized rectangle. Done when: `LiveShapeToolTests` cover each.
- [ ] Add `ThreePointRectangleTool` (baseline constraint) and `ThreePointEllipseTool`. Done when: a three-point rectangle's base matches the drawn baseline angle.
- [ ] Add `PolygonTool`, `StarTool`, and `SpiralTool` in `src/Nodus/Photon.Nodus.Core/Tools/`. Done when: each creates its live kind with the default parameters.
- [ ] Apply the modifier norm to every shape tool per `standards/nodus.md`: Shift constrains, Alt draws from center, Space moves while drawing. Done when: `ShapeModifierTests` cover the three modifiers on each tool.
- [ ] Open `ShapeOptionsDialog` on a click without dragging for exact size, radius, sides, points, or spiral values. Done when: typed values produce exact geometry in a test.
- [ ] Add `LiveShapeWidgetOverlay` drawing pie handles, side-count and point-count handles, inner-radius handles, and corner widgets. Done when: dragging each handle records one command and the widgets are captured.
- [ ] Make dragging a polygon node symmetrically reshape it into a star, and add pie or arc direction change. Done when: `LiveShapeWidgetTests` assert the resulting star radii and the reversed sweep.
- [ ] Keep parameters through move, rotate, and scale of a live shape. Done when: a rotated star reopens with its point count and radii.
- [ ] Add `CornerSet` (round, inverted round, chamfer; absolute or relative rounding; per-corner or together; scale with object) stored as `nodus:corners` on any path with the expanded path as fallback. Done when: `CornerGeometryTests` assert the fillet arc radius and chamfer distances.
- [ ] Hide the corner widget above `Nodus.Selection.CornerWidgetMaxAngle`, read by the overlay (and toggled by `D02 T07 §12`'s corner widget key). Done when: a 170-degree corner shows no widget.
- [ ] Add the Corners panel `src/Nodus/Photon.Nodus.Desktop/Views/Panels/CornersPanel.xaml`: fillet, scallop, and chamfer (A and B distances with lock) applied to selected corners of any curve. Done when: the panel is captured under `docs/captures/nodus/corners-panel/`.
- [ ] Skip corners whose segments are too short and smooth or symmetrical nodes. Done when: `CornerGeometryTests.SkipRule` leaves those corners unchanged.
- [ ] Host Shape Properties (numeric shape parameters) in the `D02 T07 §8` Properties panel. Done when: editing sides in the panel records one command.
- [ ] Add Convert to Shapes (recognize rectangle, ellipse, and regular polygon within tolerance) and Expand Shape (live to plain path), each one undoable command. Done when: `ConvertToShapesTests` recognize each kind and undo restores the path.
- [ ] Add the Coordinates panel `src/Nodus/Photon.Nodus.Desktop/Views/Panels/CoordinatesPanel.xaml` with `CoordinatesPanelViewModel`: 1. rectangle and square; 2. ellipse and circle; 3. polygon and regular polygon; 4. star and complex star; 5. 2-point line; 6. multi-point curve; 7. Create or Replace, the origin selector, live preview, and set-by-click buttons. Done when: `CoordinatesPanelTests` build the exact geometry for typed values of every kind and the panel is captured.
- [ ] Commit `tests/fixtures/nodus/svg/live-shapes/` with Inkscape goldens of the expanded fallbacks and the Inkscape version. Done when: `LiveShapeRoundTripTests` open, save, reopen, and compare element by element, and Inkscape's rendering of the SVG Nodus exports matches within 0.5 px.
- [ ] Add a Shapes and Corners page to `docs/user/nodus/`. Done when: each tool, widget, and panel is covered.
- [ ] Commit: `"nodus: live shapes with widgets, live corners, and the Corners and Coordinates panels"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~LiveShapeRoundTripTests|FullyQualifiedName~CornerGeometryTests|FullyQualifiedName~CoordinatesPanelTests"` exits 0, every live-shapes fixture reopens with every parameter, and Inkscape's rendering of the fallback matches within 0.5 px (version quoted); a driven run drags each widget with undo (captures under `docs/captures/nodus/corners-panel/` and `docs/captures/nodus/coordinates-panel/`). Cheaper substitute that fails: writing only the expanded path, which the reopen parameter assertion catches.

## 5. Grid, Graph Paper, Flare, Common Shapes, and Impact Tools

Generators that produce editable objects: rectangular and polar grids, graph paper, the flare, stock common shapes with glyph handles, and CorelDRAW's Impact tool. Each generator is a live object with parameters and an expanded group fallback, and randomization is seeded so reopen reproduces it. Catalog: NP-0426 to NP-0443 (the rectangular and polar grid tools and modifiers, the flare tool, the Impact tool with every style, boundary, rotation, random, width, spacing, line style, break apart, and palette color option, the common shapes tool and picker, glyph handles, text inside a common shape, and the graph paper tool).

**Fidelity:** Tool rail, property bar, option dialogs, and the common shapes picker -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/common-shapes/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/Canvas/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/ListTree/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail, property bar, option dialogs, and the common shapes picker -- docs/captures/nodus/main-window/ and docs/captures/nodus/common-shapes/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can generate grids, flares, stock shapes, and comic impact lines as editable objects. Consumer: the document.
**Treatment:** each generator is a live object with parameters and an expanded group fallback. Cheaper substitute that fails the checkpoint: a raster flare or impact bitmap.
**Chrome:** consume the property bar, the shared picker and number box controls, the palette click behavior from `D02 T09 §4`, and the history.

**Requires:** display-session -- generator tools and picker captures need an interactive desktop

- [ ] Add `RectangularGridTool` and `PolarGridTool` in `src/Nodus/Photon.Nodus.Core/Tools/Generators/` with `GridOptionsDialog` (size, dividers, skew, frame, fill, compound ellipses). Done when: `GridGeneratorTests` assert divider counts and skew positions.
- [ ] Add live grid modifiers: arrows add or remove dividers, and F, V, X, and C skew in 10 percent steps. Done when: a test applies each key during a drag.
- [ ] Add `GraphPaperTool`: columns and rows, Shift from center, Ctrl square cells, producing a group of rectangles that Ungroup splits into cells. Done when: a 3 by 4 graph paper ungroups into 12 rectangles.
- [ ] Add `FlareTool` with `FlareOptionsDialog` (center, halo, rays, rings) as a live `nodus:flare` object whose fallback is a group of gradient-filled vector shapes. Done when: the flare reopens live and its fallback contains no `<image>`. Cheaper substitute: a raster flare.
- [ ] Add common-shape definitions in `src/Nodus/Photon.Nodus.Core/Shapes/CommonShapes/` for basic, arrow, flowchart, banner, and callout families with parametric glyph handles. Done when: `CommonShapeGlyphTests` move a glyph handle and assert the geometry.
- [ ] Add `CommonShapesTool` and the shape picker, a list of every family with search by name. Done when: the picker is captured under `docs/captures/nodus/common-shapes/` and searching "arrow" filters it.
- [ ] Make text inside a common shape use the shape as an area-text frame through `D02 T10 §8`; until that ships, the Add Text command is disabled with the tooltip `Planned: D02 T10 §8`. Done when: `MenuAuditTests` accept the disabled command.
- [ ] Add `ImpactTool` producing a live `nodus:impact` object with radial or parallel style, inner and outer boundary references, and rotation. Done when: `ImpactGeneratorTests` keep lines inside the boundaries.
- [ ] Add impact random start and end, width min, max, steps, and randomize, spacing min, max, steps, and randomize, line style, and widest point. Done when: each parameter changes the geometry in a test.
- [ ] Seed impact randomization and store the seed in the live parameters. Done when: `ImpactGeneratorTests.SameSeedSameGeometry` passes after reopen. Cheaper substitute: an unseeded random.
- [ ] Set impact color by palette click (fill) and right-click (outline) through the `D02 T09 §4` palette bar command. Done when: a palette click recolors the impact lines as one command.
- [ ] Add Break Impact Shape Apart, which expands to editable paths. Done when: undo restores the live object.
- [ ] Add `GeneratorBenchmark` to `tests/Photon.Nodus.Benchmarks/` regenerating a 1,000-line impact on a parameter change. Done when: it reports under 50 ms.
- [ ] Commit `tests/fixtures/nodus/svg/generators/` with Inkscape goldens of the fallbacks and the version. Done when: `GeneratorRoundTripTests` reopen every fixture with parameters and seed intact.
- [ ] Add a Generators page to `docs/user/nodus/`. Done when: each tool and its options are listed.
- [ ] Commit: `"nodus: grid, graph paper, flare, common shapes, and impact generators as live objects"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~GridGeneratorTests|FullyQualifiedName~ImpactGeneratorTests|FullyQualifiedName~CommonShapeGlyphTests|FullyQualifiedName~GeneratorRoundTripTests"` exits 0 and the format fidelity proof on `tests/fixtures/nodus/svg/generators/` keeps parameters and seed, with Inkscape rendering the fallback (version quoted). Cheaper substitute that fails: an unseeded random that changes on reopen, which the identical-geometry test catches.

## 6. Node Editing: Node Types, Node Transforms, Align, Distribute, and Reduce

The direct selection tool and CorelDRAW's shape tool at parity: every node type, handle and segment drag, node selection and navigation, add, delete, reduce, convert, smoothness, node transforms and reflection, node align and distribute, subpaths, B-spline control points, and Convert to Curves. Each node operation is one `PathEditCommand` capturing before and after node lists, so node types always survive. Catalog: NP-0444 to NP-0476 (the direct selection and shape tool, corner, smooth, and symmetrical nodes, handles for multiple anchors, remove anchors, align anchors, anchor fields, segment reshape, hover highlight, select all nodes, B-spline control points, Convert to Curves, node marquees, multi and consecutive selection, Tab navigation, node align and distribute, handle drag, convert to line and curve, smoothness, copy, cut, and duplicate segments, add node, reduce nodes, node shapes by type, stretch, scale, rotate, and skew nodes, extract subpath, subpaths and holes, reflect node edits, and swap node colors).

**Fidelity:** Canvas node overlay and property bar -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/node-editing/.
**Design:** docs/design/components/Canvas/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Button/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Canvas node overlay and property bar -- docs/captures/nodus/main-window/ and docs/captures/nodus/node-editing/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can reshape any path precisely at the node level. Consumer: the document and the `D02 T06 §2` node model.
**Treatment:** each node operation is one `PathEditCommand` capturing before and after node lists; node shapes by type (circle smooth, square cusp, diamond symmetrical). Cheaper substitute that fails the checkpoint: rebuilding the path from flattened points and losing node types.
**Chrome:** consume the `D02 T06 §2` node model, the property bar, the `D02 T02 §4` align commands, and the history.

**Requires:** display-session -- node dragging and overlay captures need an interactive desktop

- [ ] Add `PathEditCommand` in `src/Nodus/Photon.Nodus.Core/Commands/PathEditCommand.cs` capturing before and after node lists including types. Done when: `NodeTypeTests.UndoRestoresTypes` passes.
- [ ] Extend `NodeEditTool` (Direct Selection; the Corel Shape tool keymap alias) with segment drag adjusting both adjacent handles and handle drag with Alt moving the node too. Done when: `NodeEditToolTests.SegmentDrag` and `HandleDragAlt` pass.
- [ ] Add hover highlight of anchors (`Nodus.Selection.HighlightAnchorsOnHover`). Done when: the setting has a named reader and a capture.
- [ ] Add node type buttons corner (cusp), smooth, and symmetrical on the property bar with C and S key toggles. Done when: `NodeTypeTests` convert each way and preserve handle geometry where the type allows.
- [ ] Draw node glyphs by type (circle smooth, square cusp, diamond symmetrical) and add `Nodus.Selection.NodeColorsSwapped` (Ctrl+Shift+I). Done when: a capture under `docs/captures/nodus/node-editing/` shows all three shapes.
- [ ] Add show or hide handles for multiple selected anchors. Done when: the toggle changes the overlay for a three-node selection.
- [ ] Add rectangular and freehand node marquees, Ctrl toggles, Shift selecting a consecutive run, Select All Nodes, and Tab and Shift+Tab to the next and previous node. Done when: `NodeSelectionTests` cover each.
- [ ] Add add node on a segment, delete anchors, and remove anchors keeping the path. Done when: removing a node from a curve keeps the path closed and one command undoes it.
- [ ] Add anchor X and Y fields for the selected nodes to the `D02 T07 §8` property bar. Done when: typing X moves the node exactly.
- [ ] Add Convert to Line, Convert to Curve, and a curve smoothness slider that refits the selected segments. Done when: `NodeConvertTests` assert segment kinds after each.
- [ ] Add Reduce Nodes, dropping nodes within tolerance. Done when: `ReduceNodesTests` show the node count drop and the max deviation under the tolerance.
- [ ] Add Convert to Curves for shapes and text (text through `D02 T10 §2` outlines once it ships; until then text conversion is disabled with the tooltip `Planned: D02 T10 §2`). Done when: a live star converts to a plain path with equal geometry.
- [ ] Add node transforms: stretch or scale and rotate or skew selected nodes with their own handle set. Done when: `NodeTransformTests` assert the transformed coordinates.
- [ ] Add reflect node edits horizontally or vertically onto mirrored counterparts. Done when: moving one node of a symmetric path moves its mirror in a test.
- [ ] Add node align (left, right, top, bottom, centers) to active nodes, page edge, page center, grid, or a typed point, and node distribute by span or exact spacing, reusing `AlignmentService` math over node positions. Done when: `NodeAlignTests` cover each reference.
- [ ] Add subpaths: extract a subpath to its own object, and copy, cut, and duplicate selected segments as new objects, with holes following the fill rule from §11. Done when: extracting the hole of a ring yields a separate circle.
- [ ] Add B-spline control point editing for §2's `nodus:bspline`: float or clamp, add by double-clicking the control line, delete by double-clicking a point, and Shift multi-select. Done when: `BSplineEditTests` cover each.
- [ ] Extend `tests/Photon.Nodus.Tests/Tools/NodeEditToolTests.cs` with the cases above. Done when: the class runs green.
- [ ] Add a Node Editing page to `docs/user/nodus/`. Done when: every operation and key is listed.
- [ ] Commit: `"nodus: node editing at parity with node transforms, align, distribute, and reduce"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~NodeTypeTests|FullyQualifiedName~NodeTransformTests|FullyQualifiedName~NodeAlignTests|FullyQualifiedName~ReduceNodesTests|FullyQualifiedName~BSplineEditTests|FullyQualifiedName~NodeEditToolTests"` exits 0; a driven run converts, aligns, and scales nodes on a fixture path with undo restoring exact coordinates (log lines quoted). Cheaper substitute that fails: flattening to a polyline, which `NodeTypeTests` catches by asserting preserved handle types.

## 7. Join Curves, Average, Offset Path, Add Anchors, Clean Up, and Split into Grid

Path repair and subdivision commands, each one history entry with a preview in its dialog: Offset Path replaces a placeholder, Average and corner or smooth join build on the `D02 T06 §2` join, and the Join Curves panel adds CorelDRAW's gap modes. Catalog: NP-0477 to NP-0494 (Average, corner or smooth join, Offset Path, advanced Simplify, the smooth slider, Add and Remove Anchor Points, Divide Objects Below, Split Into Grid, Clean Up, refine segments in place, copy paths between documents, the Join Curves panel and its extend, chamfer, fillet, and Bezier modes, and extend curve to close).

**Fidelity:** Path menu and dialogs -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/path-commands/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Path menu and dialogs -- docs/captures/nodus/main-window/; Join Curves panel and the Offset, Simplify, and Split Into Grid dialogs captured to docs/captures/nodus/path-commands/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can repair, offset, and subdivide paths with one command each. Consumer: the document.
**Treatment:** each command is one history entry with a preview in its dialog. Cheaper substitute that fails the checkpoint: Offset Path implemented as a thicker stroke.
**Chrome:** consume the Path menu, shared dialog chrome, the dock, and the history.

**Requires:** display-session -- dialog previews and the Join Curves panel need an interactive desktop

- [ ] Replace the `Offset` placeholder in `src/Nodus/Photon.Nodus.Core/Services/PathOperationsService.cs`: stroke outline via `SKPaint.GetFillPath` at twice the distance with miter, round, or bevel joins and a miter limit, then keep the outer or inner contour with `SKPath.Op`. Done when: `OffsetPathTests` offset a 100 px square by 10 to 120 px bounds and the round-join area is within 0.5 percent of analytic.
- [ ] Add the Offset Path dialog with live preview. Done when: the preview updates as the distance changes and Cancel leaves the document unchanged. Cheaper substitute: a thicker stroke.
- [ ] Add Average (horizontal, vertical, both) and corner or smooth join (Shift+Ctrl+Alt+J) on the `D02 T06 §2` join. Done when: `AverageJoinTests` cover each.
- [ ] Add Simplify advanced options on the `D02 T06 §2` simplify: curve precision, corner angle threshold, convert to straight lines, show original overlay, and remember auto-simplify, plus the contextual smooth slider on selected segments. Done when: `SimplifyOptionsTests` assert node reduction per option.
- [ ] Add refine path segments in place (the smooth slider acting on the selected span only). Done when: nodes outside the span keep their coordinates.
- [ ] Add Add Anchor Points (the midpoint of each segment) and Remove Anchor Points (keep the path). Done when: Add doubles a square's nodes and Remove restores the geometry.
- [ ] Add Divide Objects Below: cut every unlocked object under the selected path with `SKPath.Op` and delete the cutter, as one `CompositeCommand`. Done when: `DivideObjectsBelowTests` skip a locked object and cut the rest.
- [ ] Add the Split Into Grid dialog: rows, columns, gutters, heights, widths, and add guides (through `D02 T07 §10`). Done when: `SplitIntoGridTests` produce the expected cells and guides.
- [ ] Add Clean Up: remove stray points, unpainted objects, and empty text paths, reporting the counts on the status strip. Done when: `CleanUpTests` assert each count and the status line.
- [ ] Add the Join Curves panel `src/Nodus/Photon.Nodus.Desktop/Views/Panels/JoinCurvesPanel.xaml` with gap tolerance and modes extend to intersection, chamfer, fillet with radius, and Bezier connection. Done when: `JoinCurvesTests` cover each mode and the panel is captured.
- [ ] Add extend curve to close, joining two selected end nodes with a straight segment. Done when: the result is one closed path.
- [ ] Copy paths between documents as SVG fragments on the clipboard in the suite clipboard format from `D02 T03 §3` (Photoshop path export is Imago's side). Done when: a path copied in one document pastes with equal geometry in another.
- [ ] Add a Path Commands page to `docs/user/nodus/`. Done when: every command and dialog is listed.
- [ ] Commit: `"nodus: offset path, average and join, simplify options, split into grid, clean up, and the Join Curves panel"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~OffsetPathTests|FullyQualifiedName~JoinCurvesTests|FullyQualifiedName~SplitIntoGridTests|FullyQualifiedName~CleanUpTests|FullyQualifiedName~DivideObjectsBelowTests"` exits 0; a driven run of each dialog with preview and undo is captured under `docs/captures/nodus/path-commands/`. Cheaper substitute that fails: offset as a wider stroke, which the bounds assertion on the resulting path catches.

## 8. Knife, Scissors, Eraser, Virtual Segment Delete, and the Crop Tool

Cutting, erasing, and cropping vector artwork directly on the canvas, each stroke one command producing closed, filled paths. The eraser reads the stylus fields §3 added. This is B-008's object eraser (owned with the pencil by §3's promotion). Catalog: NP-0495 to NP-0512 (the scissors, knife, eraser, crop, and virtual segment delete tools, eraser nib, pressure, tilt, and bearing, reduce nodes and defaults, straight-line and double-click erase, the stylus eraser end, virtual segment delete by marquee or curve and weld, knife modes, cut span, and outline options, and crop position, size, rotation, clear, and auto conversion).

**Fidelity:** Tool rail flyout and property bar -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/cutting-tools/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail flyout and property bar -- docs/captures/nodus/main-window/ and docs/captures/nodus/cutting-tools/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can cut, erase, and crop vector artwork directly on the canvas. Consumer: the document.
**Treatment:** each cut or erase stroke is one command producing closed, filled paths. Cheaper substitute that fails the checkpoint: an eraser that paints a white shape over the art.
**Chrome:** consume the property bar, the §3 stylus fields, and the history.

**Requires:** display-session -- cutting and erasing strokes need an interactive desktop

- [ ] Replace the `SplitPath` placeholder in `PathOperationsService` and add `ScissorsTool` splitting a path at a clicked anchor or segment point. Done when: `ScissorsToolTests` split a closed path into one open path and an open path into two.
- [ ] Add `KnifeTool` in `src/Nodus/Photon.Nodus.Core/Tools/Cutting/KnifeTool.cs` with freehand, 2-point (Shift+Ctrl constrains to 15 degrees), and Bezier modes cycled with A. Done when: `KnifeToolTests` cut a square by a diagonal into two closed paths whose areas sum to the original.
- [ ] Add knife cut span (gap or overlap of a set width). Done when: gap mode reduces the area sum by width times cut length within 0.5 percent.
- [ ] Add knife outline options: automatic, convert to objects, keep outlines. Done when: each option's result is asserted on a stroked fixture.
- [ ] Add `EraserTool` with nib size, round or square shape, angle, and roundness, erasing by `SKPath.Op` difference with the swept nib outline. Done when: `EraserToolTests` erase a stripe through a rectangle leaving two closed paths. Cheaper substitute: painting a background-colored shape.
- [ ] Map eraser pressure, tilt, and bearing from the §3 `ToolPoint` fields to nib size and angle. Done when: a synthetic pressure ramp widens the swept outline.
- [ ] Add straight-line erase (click, click, Ctrl constrains) and double-click area erase, and switch to the eraser when the stylus eraser end is used. Done when: each gesture has a test.
- [ ] Add `Nodus.Tools.Eraser.ReduceNodes` (true) and `Nodus.Tools.Eraser.Thickness` defaults. Done when: reduce-nodes on yields fewer nodes than off on the same stroke.
- [ ] Add `VirtualSegmentDeleteTool`: click deletes a segment between intersections, a marquee or an Alt-drawn curve deletes many, and Shift welds overlapping end points into one node. Done when: `VirtualSegmentDeleteTests` cover each.
- [ ] Add `CropTool`: a crop rectangle with position, size, and rotation on the property bar; Enter crops every unlocked object with `SKPath.Op` intersection; Esc or Clear removes the area. Done when: `CropToolTests` crop a fixture to the rectangle and skip locked objects.
- [ ] Convert text and live effects to curves before cropping, with a status line naming each converted object. Done when: cropping a live star logs the conversion.
- [ ] Disable knife and crop on bitmaps with the tooltip `Planned: D02 T12 §1`. Done when: `MenuAuditTests` accept the disabled state.
- [ ] Add `EraserBenchmark` to `tests/Photon.Nodus.Benchmarks/` over a 5,000-node path. Done when: it reports preview under 16 ms per dab with the commit on mouse-up.
- [ ] Add a Cutting and Erasing page to `docs/user/nodus/`. Done when: every tool and option is listed.
- [ ] Commit: `"nodus: scissors, knife, eraser, virtual segment delete, and the crop tool"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~KnifeToolTests|FullyQualifiedName~EraserToolTests|FullyQualifiedName~VirtualSegmentDeleteTests|FullyQualifiedName~CropToolTests"` exits 0; a driven run knifes, erases, and crops a fixture with undo (capture under `docs/captures/nodus/cutting-tools/`). Cheaper substitute that fails: painting background-colored shapes, which the area-sum assertion catches.

## 9. Liquify and Shape-Editing Brushes

Illustrator's liquify tools and CorelDRAW's shape-editing brushes push, twist, and roughen outlines organically. Dabs displace or insert nodes along the path each tick, and the whole drag is one command on mouse-up: these edit real nodes, not a live effect. Catalog: NP-0513 to NP-0535 (the Warp, Twirl, Pucker and Bloat, Scallop, Crystallize, and Wrinkle tools and their options, the Smooth, Smear, Smudge, and Roughen brushes with nib, rate, amount, pressure, dryout, tilt, bearing, and spike options, control range settings, and auto convert before roughen).

**Fidelity:** Tool rail flyout, property bar, and Liquify options dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/shape-brushes/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/Canvas/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail flyout, property bar, and Liquify options dialog -- docs/captures/nodus/main-window/ and docs/captures/nodus/shape-brushes/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can push, twist, and roughen outlines organically with a brush. Consumer: the document.
**Treatment:** dabs displace or insert nodes along the path each tick; the whole drag is one command on mouse-up. Cheaper substitute that fails the checkpoint: a live warp effect that leaves the path's nodes unchanged.
**Chrome:** consume the property bar, the §3 stylus fields, the shared brush cursor overlay, and the history.

**Requires:** display-session -- brush drags and stylus input need an interactive desktop

- [ ] Add `ShapeBrushBase` in `src/Nodus/Photon.Nodus.Core/Tools/Shaping/ShapeBrushBase.cs`: nib radius, rate, falloff, pressure mapping, detail (node insertion density), simplify after stroke, and dryout, tilt, and bearing from the §3 `ToolPoint` fields, recording one command on mouse-up. Done when: `ShapeBrushTests.OneCommandPerDrag` passes.
- [ ] Add `WarpTool` (drag displacement). Done when: its direction test moves nodes along the drag vector.
- [ ] Add `TwirlTool` (rotation about the nib, clockwise or counterclockwise, radius, rate, pressure). Done when: its test rotates nodes in the set direction.
- [ ] Add `AttractRepelTool` (Pucker and Bloat; Attract and Repel with nib, rate, and pressure). Done when: attract moves nodes toward the nib center and repel away.
- [ ] Add `ScallopTool`, `CrystallizeTool`, and `WrinkleTool` (complexity, affect anchors and handles). Done when: each has a direction and node-count test.
- [ ] Add the Liquify Tool Options dialog shared by every liquify tool (width, height, angle, intensity, pressure pen, detail, simplify, twirl rate, complexity, show brush size) under `Nodus.Tools.Liquify.*`. Done when: every key has a named reader and the dialog is captured.
- [ ] Add `SmoothBrushTool` (nib, rate, pressure). Done when: a smoothed noisy span loses nodes and keeps its ends.
- [ ] Add `SmearTool` (nib, amount, pressure, smooth or pointy). Done when: smooth and pointy produce different committed goldens.
- [ ] Add `SmudgeTool` (nib, pressure, dryout, tilt, bearing). Done when: a dryout of 50 shortens the smudge in a test.
- [ ] Add `RoughenTool` (nib, spike frequency, pressure, dryout, tilt, and spike direction fixed, stylus, or auto). Done when: spike frequency sets the spike count per 100 px in a test.
- [ ] Convert distortions, envelopes, and perspective objects to curves before roughening, with a status line naming each. Done when: roughening a live shape logs its conversion.
- [ ] Add control range settings: right-click a property-bar slider to set its min and max, persisted per control in the settings store. Done when: a changed range survives restart (settings readback quoted).
- [ ] Add Shift-drag to resize the nib interactively and Alt-drag to show the rate slider on the canvas. Done when: both gestures are captured.
- [ ] Commit dab sequences and node-coordinate goldens under `tests/fixtures/nodus/brush-dabs/` and replay them in `ShapeBrushTests` (node-count bound; closed paths stay closed). Done when: each tool has a golden and the test fails if a tool leaves nodes unchanged.
- [ ] Add `ShapeBrushBenchmark` to `tests/Photon.Nodus.Benchmarks/` on a 5,000-node path. Done when: it reports 60 dabs per second with preview under 16 ms.
- [ ] Add a Liquify and Shaping Brushes page to `docs/user/nodus/`. Done when: every tool and option is listed.
- [ ] Commit: `"nodus: liquify tools and the smooth, smear, smudge, and roughen brushes"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~ShapeBrushTests"` exits 0 replaying the committed dab sequences against their goldens; a driven run of each brush with undo is captured under `docs/captures/nodus/shape-brushes/`. Cheaper substitute that fails: a non-destructive effect, which the node-coordinate goldens catch.

## 10. Pathfinder, Shaping, and the Shape Builder

Every Pathfinder and CorelDRAW shaping operation, live compound shapes, and the Shape Builder, all on one `PlanarFaces` engine over `SKPath.Op`. The `D02 T02 §5` Path menu booleans stay and call the same commands. Catalog: NP-0541 to NP-0566 (the Shape Builder and its gap detection, open paths as closed, stroke click split, color source, and selection style, the Pathfinder and Shaping panels, live compound shapes, Divide, Trim, Merge, Crop, Outline, Minus Back, Back minus Front, Pathfinder options, Repeat Pathfinder, trim a target by sources, shaping a PowerClip frame, linked effects converted first, Weld and weld groups, weld a self-intersecting object, Intersect with one or several targets, create an object from an enclosed area, and Boundary).

**Fidelity:** Pathfinder panel -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/pathfinder-panel/, docs/captures/golden/nodus/main-window/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Button/README.md, docs/design/components/Icons/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Pathfinder panel -- new build, no baseline; captured to docs/captures/nodus/pathfinder-panel/; the Shape Builder overlay on docs/captures/nodus/main-window/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can build complex shapes from overlaps by command or by dragging across regions. Consumer: the document, and later Live Paint (`D02 T11 §17`) and pathfinder effects (`D02 T11 §19`).
**Treatment:** every operation is one command on `SKPath.Op`; compound shapes stay live. Cheaper substitute that fails the checkpoint: grouping the inputs and calling it a merge.
**Chrome:** consume `D02 T02 §5` `ElementToPathConverter` and the boolean service, the dock, the shared icon catalog, and the history; the Path menu entries from `D02 T02 §5` stay and call the same commands.

**Requires:** display-session -- the panel, Shape Builder drags, and captures need an interactive desktop

- [ ] Add `PlanarFaces` in `src/Nodus/Photon.Nodus.Core/Shaping/PlanarFaces.cs` splitting a set of paths into non-overlapping faces with `SKPath.Op`. Done when: `PlanarFacesTests` split three overlapping circles into seven faces.
- [ ] Add Divide, Trim (hidden areas removed; the Corel Simplify), and Merge (same-fill neighbors united) on `PlanarFaces`. Done when: `PathfinderTests` assert area and face count per operation.
- [ ] Add Crop (to the top object), Outline (edges as stroked segments), Minus Back (Corel Front minus Back), and Back minus Front. Done when: `PathfinderTests` assert area and face count per operation.
- [ ] Add CorelDRAW Trim of a target by sources: a marquee trims the bottom-most, click-select trims the last selected. Done when: `ShapingTargetRuleTests` cover both rules.
- [ ] Add Weld with the target's attributes: non-overlapping objects form a weld group and a self-intersecting single object breaks into subpaths. Done when: `WeldTests` cover all three cases.
- [ ] Add Intersect with one or several targets using the target's attributes, and Boundary (the outer outline for keylines). Done when: each has a test.
- [ ] Add leave-original source and target options on the Shaping panel. Done when: with leave-original on, the inputs remain after the operation.
- [ ] Convert linked effects (shadows, text on a path, blends, contours, extrusions) to curves before shaping, and reshape the frame when shaping a PowerClip frame (with `D02 T11 §12`; until it ships, frames are shaped as plain groups). Done when: a status line names each converted object.
- [ ] Add Create Object from Enclosed Area: a click-to-fill face picker on `PlanarFaces`, shared with `D02 T11 §17` smart fill. Done when: clicking inside three overlapping lines yields the enclosed face.
- [ ] Add the Pathfinder and Shaping panel `src/Nodus/Photon.Nodus.Desktop/Views/Panels/PathfinderPanel.xaml`, with every operation listed and findable by name. Done when: the panel is captured and every button runs the same command as the Path menu.
- [ ] Add Pathfinder Options (precision, remove redundant points, remove unpainted artwork after Divide and Outline) as `Nodus.Pathfinder.*`, and Repeat Pathfinder on Ctrl+4. Done when: each option changes a test result and Repeat reruns the last operation.
- [ ] Add live compound shapes (Alt-click a shape mode) as `nodus:compound-shape` with operands kept editable, and Make, Release, and Expand through `D02 T07 §1`. Done when: `CompoundShapeRoundTripTests` reopen a compound shape with its operands.
- [ ] Add `ShapeBuilderTool` (Shift+M) with hover highlight of faces and edges, drag to merge, and Alt-drag to delete. Done when: `ShapeBuilderTests` merge and delete faces. Cheaper substitute: grouping the inputs.
- [ ] Add Shape Builder options: gap detection (small, medium, large, custom), open filled paths treated as closed, stroke click splits in merge mode, color from swatches or artwork with a cursor swatch preview, freeform or straight selection, and highlight color. Done when: each option has a test or a capture.
- [ ] Run operations expected over a second on a `LongOperation` (`D02 T07 §2`) with status-strip progress and cancel, and add `PathfinderBenchmark` for Divide over 200 overlapping paths. Done when: the benchmark reports under 1 s, cancel leaves the document unchanged, and the status strip shows a completion notification naming the operation.
- [ ] Commit `tests/fixtures/nodus/svg/compound-shapes/` with Inkscape goldens of the fallback and the version. Done when: the fidelity round trip passes.
- [ ] Add a Pathfinder, Shaping, and Shape Builder page to `docs/user/nodus/`. Done when: every operation is listed.
- [ ] Commit: `"nodus: every Pathfinder and shaping operation, live compound shapes, and the Shape Builder"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~PathfinderTests|FullyQualifiedName~ShapeBuilderTests|FullyQualifiedName~CompoundShapeRoundTripTests|FullyQualifiedName~WeldTests"` exits 0, the format fidelity proof on the compound-shapes fixture passes with Inkscape rendering the fallback (version quoted), and a driven Shape Builder run with undo is captured under `docs/captures/nodus/pathfinder-panel/`. Cheaper substitute that fails: grouping inputs, which the face-count assertion catches.

## 11. Compound Paths, Clipping Masks, Draw Inside and Behind, and Intertwine

Punching holes, clipping artwork, drawing inside a shape, and weaving objects. The importer honors `clip-path` for the first time, the renderer clips through Skia on the real `clipPath` element, and the writer round-trips it, so a clip can always be released. Promoted from backlog B-002: the importer honors `clip-path` and the Object menu makes and releases clipping masks and compound paths; masks proper ride `D02 T09 §20` and markers `D02 T09 §12` (the entry left the backlog when this file was integrated). Catalog: NP-0567 to NP-0578 (Draw Normal, Behind, and Inside, make and release compound paths, the fill rule, Intertwine make, edit, and release, clipping masks, edit mask or contents, layer clipping masks, text as a clip, treat all objects as filled, and fill open curves). -> SOURCE: legacy-nodus-1.6-4.4

**Fidelity:** Object menu, drawing mode toggle on the tool rail, Layers panel commands -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/clipping/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/ToolRail/README.md, docs/design/components/Panel/README.md, docs/design/components/LayersRow/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Object menu, drawing mode toggle on the tool rail, Layers panel commands -- docs/captures/nodus/main-window/ and docs/captures/nodus/clipping/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can punch holes, clip artwork, draw inside a shape, and weave objects. Consumer: the document, the renderer, and the SVG writer.
**Treatment:** clipping renders through `SKCanvas.ClipPath` on the real `clipPath` element and round-trips as SVG `clipPath`. Cheaper substitute that fails the checkpoint: pre-cutting the content geometry so the mask cannot be released.
**Chrome:** consume the Object menu, the `D02 T07 §5` Layers panel, `D02 T07 §7` isolation mode for Edit Contents, and the history.

**Requires:** display-session -- clipping, draw inside, and intertwine need an interactive desktop

- [ ] Teach `SvgImporter` to read `clipPath` elements and `clip-path` references into `SvgClipPath`, including clips with their own transform and nested clips. Done when: `ClipPathRoundTripTests.Reads` load the nested fixture.
- [ ] Teach `SvgExporter` to write `clipPath` elements and `clip-path` references. Done when: `ClipPathRoundTripTests` round-trip element by element.
- [ ] Apply `SKCanvas.ClipPath` with the clip's transform in `SkiaRenderer`. Done when: the clipping fixture renders against its Inkscape golden within 1 percent pixel difference.
- [ ] Add Make Compound Path (Ctrl+8; Corel Combine Ctrl+L) and Release (Alt+Shift+Ctrl+8; Break Curve Apart Ctrl+K), text breaking into lines then words through `D02 T10 §2` once it ships. Done when: `CompoundPathTests` make and release a ring.
- [ ] Add the fill rule nonzero or even-odd on the Attributes section of the `D02 T07 §8` Properties panel, written as `fill-rule`. Done when: `CompoundPathTests.FillRuleArea` asserts different areas for a self-overlapping path.
- [ ] Add Make Clipping Mask (Ctrl+7) and Release (Alt+Ctrl+7). Done when: release restores the content's original geometry. Cheaper substitute: baking the clip into geometry.
- [ ] Add Edit Mask and Edit Contents, selecting the clip path or the contents and isolating through `D02 T07 §7`. Done when: editing contents moves the content under a fixed clip.
- [ ] Add the layer-level clipping mask from the Layers panel and live text as a clip path. Done when: a text clip round-trips with its text still editable.
- [ ] Add draw modes Normal, Behind, and Inside (Shift+D cycles), Inside creating a clip group on the selected object and placing new art in it. Done when: `DrawInsideTests` place a new rectangle inside a clip group.
- [ ] Add Intertwine as `nodus:intertwine`: zones drawn around overlaps switch which object is on top inside the zone (rendered by clipping a duplicate), with Edit adding zones and Release restoring stacking. Done when: `IntertwineTests` round-trip a zone and Release restores the original z-order.
- [ ] Add `Nodus.Document.FillOpenCurves` (a document option read by `SkiaRenderer`) and `Nodus.Selection.TreatAllAsFilled` (read by hit testing inside unfilled shapes). Done when: each has a test proving its reader.
- [ ] Commit `tests/fixtures/nodus/svg/clipping/` (nested clips, a clip with a transform, a text clip, a compound even-odd path) with Inkscape goldens and the version. Done when: the fixture set is committed.
- [ ] Add a Compound Paths and Clipping page to `docs/user/nodus/`. Done when: every command is listed.
- [ ] Commit: `"nodus: compound paths, clipping masks, draw inside and behind, and intertwine"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ClipPathRoundTripTests|FullyQualifiedName~CompoundPathTests|FullyQualifiedName~DrawInsideTests|FullyQualifiedName~IntertwineTests"` exits 0, the clipping fixtures compare element by element and render against Inkscape goldens within 1 percent pixel difference (version quoted), and a driven make, edit contents, and release with undo is captured under `docs/captures/nodus/clipping/`. Cheaper substitute that fails: baking the clip into geometry, which the release test catches.

## 12. The Transform Panel, Transform Dialogs, Transform Again, and Transform Each

Placing, sizing, rotating, and repeating transforms by exact numbers: one `TransformSpec` applied by one command, surfaced as the Transform panel, the Illustrator dialogs, and CorelDRAW's Transform docker tabs. Transform Again replays the last delta, never an absolute position. Promoted from backlog B-006: the transform dialog and Transform Again land here, and Select Same and deep select are owned by `D02 T07 §6` (the entry left the backlog when this file was integrated). Catalog: NP-0583 to NP-0605 (Transform Again, move, rotate, reflect, scale and mirror, and shear by number, Transform Each and its scaling, the Transform panel and docker, constrain, scale corners and strokes, pixel grid alignment, flip, transform objects or patterns, math and apply to a copy, nudge, move and scale many together or each, Clear Transformations, the reference point selector, copies, size by exact dimensions, and scale portion and fit to reference in the docker). -> SOURCE: legacy-nodus-3.1

**Fidelity:** Transform panel -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/transform-panel/, docs/captures/golden/nodus/transform-dialogs/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Dialog/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Transform panel -- new build, no baseline; captured to docs/captures/nodus/transform-panel/; Object, Transform dialogs captured to docs/captures/nodus/transform-dialogs/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can place, size, rotate, and repeat transforms by exact numbers. Consumer: the document and the §13 tools.
**Treatment:** every apply is one command with preview; Copy creates duplicates in the same entry; Transform Again replays the last recorded transform. Cheaper substitute that fails the checkpoint: Transform Again that re-applies the last absolute position rather than the delta.
**Chrome:** consume the `D02 T07 §8` Properties panel fields, the shared number box with expression parsing, the dock, and the history. Do not grow a second numeric field control.

**Requires:** display-session -- panel and dialog driving needs an interactive desktop

- [ ] Add `TransformSpec` in `src/Nodus/Photon.Nodus.Core/Transforms/TransformSpec.cs` (translate, rotate, scale, reflect, shear about a reference point; flags scale corners, scale strokes and effects, objects, patterns, copies). Done when: `TransformSpecTests` assert the expected matrix for each operation.
- [ ] Add `ApplyTransformCommand` built on `TransformService` applying a `TransformSpec` as one command, copies included in the same entry. Done when: undo removes the copies and restores the originals.
- [ ] Add the Transform panel `src/Nodus/Photon.Nodus.Desktop/Views/Panels/TransformPanel.xaml` with `TransformPanelViewModel`: the nine-point reference selector, X, Y, W, H, rotate, shear, and the flip menu. Done when: `TransformPanelViewModelTests` apply each field as one command.
- [ ] Add constrain proportions (or stretch non-proportionally), align to pixel grid, use preview bounds, and host Shape Properties from §4 in the panel. Done when: constrained W changes H proportionally in a test.
- [ ] Add scale corners and scale strokes and effects flags. Done when: scaling a 2 px stroked square by 200 percent with strokes on yields a 4 px stroke and with strokes off 2 px.
- [ ] Accept arithmetic and units in every field through the `D02 T07 §8` `UnitExpression`, with Alt+Enter applying to a copy. Done when: typing `+10mm` into X moves the object by 37.795 px.
- [ ] Add `MoveDialog`, `RotateDialog`, `ReflectDialog`, `ScaleDialog`, and `ShearDialog` under `src/Nodus/Photon.Nodus.Desktop/Views/Dialogs/Transform/`, each with Preview and Copy. Done when: each dialog is captured and Cancel after Preview leaves the document unchanged.
- [ ] Add the CorelDRAW Transform docker tabs Position (absolute or relative), Rotate (relative center or ruler coordinates), Scale and Mirror, Size, and Skew, with a copies count, mapped to the same `TransformSpec`. Done when: each tab produces the same matrix as its Illustrator dialog in a test.
- [ ] Add Scale Portion and Fit to Reference in the docker. Done when: fitting a square to a 50 by 80 rectangle yields its bounds.
- [ ] Transform objects, patterns, or both (panel menu and the backquote drag modifier), with pattern transforms written on the `D02 T09 §10` pattern fill once it ships. Done when: the option is honored by `ApplyTransformCommand` in a test with a probe pattern transform.
- [ ] Add Transform Again (Ctrl+D) storing the last `TransformSpec` in the document session and replaying it on the current selection. Done when: `TransformAgainTests` move then repeat three times to four equally spaced copies. Cheaper substitute: absolute replay.
- [ ] Add Transform Each (random, relative or absolute scaling) about each object's own reference point with a seeded random. Done when: `TransformEachTests` give the same result for the same seed.
- [ ] Add nudge by `Nodus.Editing.KeyboardIncrement` (Shift times ten) and move or scale multi-object selections together or each. Done when: scaling three objects each keeps their centers.
- [ ] Add Clear Transformations resetting an element's accumulated `transform` matrix to identity while keeping its position, as one command. Done when: a rotated rectangle clears to axis-aligned at the same center.
- [ ] Extend the Object, Transform submenu beyond the fixed 90 and 180 degree rotations and flips with every dialog and Transform Again and Each. Done when: `MenuAuditTests` pass with every item enabled.
- [ ] Add a Transform page to `docs/user/nodus/`. Done when: every field, dialog, and docker tab is listed.
- [ ] Commit: `"nodus: the Transform panel and docker, transform dialogs, Transform Again, and Transform Each"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~TransformSpecTests|FullyQualifiedName~TransformAgainTests|FullyQualifiedName~TransformEachTests|FullyQualifiedName~TransformPanelViewModelTests"` exits 0; a driven run of each dialog with Copy and undo is captured under `docs/captures/nodus/transform-panel/`, and a saved file is inspected for the resulting matrices. Cheaper substitute that fails: absolute replay, which `TransformAgainTests` catches.

## 13. Rotate, Reflect, Scale, Shear, Reshape, and Free Transform Tools

Interactive transforms around any pivot: the Illustrator tools, CorelDRAW's second-click rotate and skew handles, the free transform modes including perspective and free distort, and the Scale Portion and Fit to Reference tools. Every drag records one `ApplyTransformCommand` on mouse-up through the `D02 T03 §1` pattern, and one modifier policy governs every drawing and transform tool. Catalog: NP-0606 to NP-0621 (the Rotate, Reflect, Scale, Shear, Reshape, Free Transform, Scale Portion, and Fit to Reference tools, free transform modes, relative to object, and apply to duplicate, handle-drag modifiers, corner and side handles, mirror by Ctrl-drag, the angle of rotation box, and consistent constrain and draw-from-center modifiers).

**Fidelity:** Tool rail, canvas handles, and property bar -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/transform-tools/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/Canvas/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail, canvas handles, and property bar -- docs/captures/nodus/main-window/ and docs/captures/nodus/transform-tools/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can transform objects interactively around any pivot. Consumer: the document.
**Treatment:** every drag records one `ApplyTransformCommand` on mouse-up through the `D02 T03 §1` pattern. Cheaper substitute that fails the checkpoint: live-mutating matrices with nothing recorded.
**Chrome:** consume the §12 `TransformSpec`, the `SelectTool` handle overlay, the property bar, and the history.

**Requires:** display-session -- interactive transform drags need an interactive desktop

- [ ] Add `ModifierPolicy` in `src/Nodus/Photon.Nodus.Core/Tools/ModifierPolicy.cs` so constrain (Ctrl) and draw from center (Shift) behave consistently across drawing and transform tools, the CorelDRAW keymap swapping Ctrl and Shift per `D02 T16 §3`. Done when: `HandleModifierTests` run every drawing and transform tool through the policy.
- [ ] Add `RotateTool`, `ReflectTool`, `ScaleTool`, and `ShearTool` in `src/Nodus/Photon.Nodus.Core/Tools/Transform/`: click sets the pivot, drag transforms, Alt-click opens the §12 dialog, Alt-drag copies. Done when: `TransformToolTests` rotate about a moved pivot, shear by an angle, and reflect across an axis.
- [ ] Add the `SelectTool` second click toggling to rotate and skew handles with a movable center of rotation. Done when: a second click shows the rotate handles and dragging the center moves the pivot.
- [ ] Make corner handles scale proportionally, side handles stretch, and skew arrows slant. Done when: each handle has a test.
- [ ] Add handle modifiers: Shift from center, Ctrl integer multiples (100 percent increments), Alt stretch non-proportionally, and Ctrl-drag across mirroring. Done when: `HandleModifierTests` cover each.
- [ ] Add mirror buttons and the angle-of-rotation box on the property bar, each one command. Done when: typing 45 rotates the selection by 45 degrees in one step.
- [ ] Add `ReshapeTool`: stretch selected anchors while neighbors follow by falloff, keeping the overall shape. Done when: a test asserts neighbor displacement decays with distance.
- [ ] Add `FreeTransformTool` (E) with a widget offering Constrain, Free Transform, Perspective Distort, and Free Distort. Done when: the widget is captured under `docs/captures/nodus/transform-tools/`.
- [ ] Add CorelDRAW free transform modes: free rotation, angle reflection, free scale, free skew, relative to object, and apply to duplicate. Done when: each mode has a test.
- [ ] Map every node through a projective transform for Perspective Distort and a bilinear one for Free Distort, writing plain geometry, and expand live shapes first with a status line. Done when: `FreeDistortTests` map the four corners exactly.
- [ ] Add `ScalePortionTool` (drag a known span, type its length, scale the object) and `FitToReferenceTool` (scale and move into another object's bounds). Done when: `ScalePortionTests` scale a 50 px span typed as 100 px to double size.
- [ ] Record every drag as one `ApplyTransformCommand` on mouse-up. Done when: `TransformToolTests.UndoRestoresMatrix` restores the exact matrix after each tool. Cheaper substitute: live mutation with nothing recorded.
- [ ] Add a Transform Tools page to `docs/user/nodus/`. Done when: every tool and modifier is listed.
- [ ] Commit: `"nodus: rotate, reflect, scale, shear, reshape, free transform, scale portion, and fit to reference tools"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~TransformToolTests|FullyQualifiedName~FreeDistortTests|FullyQualifiedName~HandleModifierTests|FullyQualifiedName~ScalePortionTests"` exits 0; a driven run of each tool with undo restoring exact matrices is captured under `docs/captures/nodus/transform-tools/`. Cheaper substitute that fails: no recorded command, which the undo assertion catches.

## 14. Align, Distribute, Arrange, and Step and Repeat Extensions

`D02 T02 §4` wired the basic align, arrange, rotate, and flip commands; this section adds the Align panel and CorelDRAW docker with every reference, spacing with preview, artboard alignment, page and layer order, and Step and Repeat. Every button is one `CompositeCommand` from `AlignmentService` deltas. Locked layers refuse reordering by name: moves onto a locked layer go to the nearest editable layer. Catalog: NP-0622 to NP-0643 (Send to Current Layer, the Align panel and docker, center to page, distribute edges and centers, distribute spacing equal or exact with preview, align to selection, key object, or artboard, preview bounds, outline, or glyph bounds, shortcuts, align artboards, Step and Repeat, align to page edge or center, grid, or a point, text baseline references, distribute to selection or page, page and layer order, In Front Of and Behind, Reverse Order, and the locked layer rule).

**Fidelity:** Align panel and Step and Repeat panel -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/align-panel/, docs/captures/golden/nodus/step-and-repeat/, docs/captures/golden/nodus/main-window/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Button/README.md, docs/design/components/Icons/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Menu/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Align panel and Step and Repeat panel -- new build, no baseline; captured to docs/captures/nodus/align-panel/ and docs/captures/nodus/step-and-repeat/; Object, Arrange on docs/captures/nodus/main-window/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can line up, space, stack, and duplicate objects exactly. Consumer: the document.
**Treatment:** every button is one `CompositeCommand` from `AlignmentService` deltas; spacing previews before apply. Cheaper substitute that fails the checkpoint: a panel that only mirrors the `D02 T02 §4` menu.
**Chrome:** consume `D02 T02 §4` `CompositeCommand` and `AlignmentService`, the `D02 T07 §5` layers, the dock, the shortcut manager, and the history.

**Requires:** display-session -- panel driving and click-target arrange commands need an interactive desktop

- [ ] Add the Align panel `src/Nodus/Photon.Nodus.Desktop/Views/Panels/AlignPanel.xaml` (the Align and Distribute docker in the CorelDRAW workspace) with align six ways and distribute left, center, right, top, center, and bottom through `AlignmentService`. Done when: `AlignPanelTests` cover each button.
- [ ] Add distribute spacing, equal or by an exact distance. Done when: `DistributeSpacingTests` produce exact 12 px gaps across five objects.
- [ ] Draw a distribute spacing preview of ghost positions before apply. Done when: the preview is captured and Cancel records nothing.
- [ ] Add Align To: selection, key object (click a selected object to make it key), and artboard. Done when: `AlignPanelTests.KeyObject` leaves the key object unmoved.
- [ ] Add Align To page edge, page center, grid (`D02 T07 §9`), or a typed or clicked point, and distribute to selection, page, or exact object spacing. Done when: each reference has a test.
- [ ] Add one-click center on both axes and Center to Page (P, with horizontal and vertical variants). Done when: P centers the selection on the active page in one step.
- [ ] Add the bounds choice: preview bounds (stroke included), object outline, or glyph bounds, and the text reference first baseline, last baseline, or bounding box (baselines from `D02 T10 §2` once it ships). Done when: aligning two stroked squares by preview bounds differs from geometric bounds by the stroke width.
- [ ] Add Align Selected Artboards through the `D02 T07 §3` page model. Done when: aligning three artboards top moves their artwork with them.
- [ ] Register every align and distribute command with the shortcut manager so each can take a shortcut (action recording is excluded automation). Done when: `ShortcutsViewModelTests` list the commands.
- [ ] Add To Front or Back of Page and To Front or Back of Layer. Done when: `ArrangeCommandParityTests` assert page order versus layer order.
- [ ] Add In Front Of and Behind a clicked object, Reverse Order, and Send to Current Layer. Done when: `ArrangeCommandParityTests` cover each.
- [ ] Apply the locked layer policy: a move onto a locked layer goes to the nearest editable layer with a status message naming the locked layer. Done when: `ArrangeCommandParityTests.LockedLayerRule` asserts the destination and the message.
- [ ] Add the Step and Repeat panel (Ctrl+Shift+D): copies count and horizontal and vertical modes no offset, spacing between objects with direction, or offset, as one `CompositeCommand` for all copies. Done when: `StepAndRepeatTests` place ten copies exactly and undo removes them in one step.
- [ ] Run Step and Repeat over a second on a `LongOperation` with status-strip progress. Done when: `StepAndRepeatTests.ThousandCopies` completes under 1 s.
- [ ] Add an Align, Arrange, and Step and Repeat page to `docs/user/nodus/`. Done when: every reference and command is listed.
- [ ] Commit: `"nodus: the Align panel with every reference, page and layer order, and Step and Repeat"`

**Test checkpoint:** Unit test `dotnet test Photon.slnx --filter "FullyQualifiedName~AlignPanelTests|FullyQualifiedName~DistributeSpacingTests|FullyQualifiedName~ArrangeCommandParityTests|FullyQualifiedName~StepAndRepeatTests"` exits 0; a driven run aligns to a key object, distributes with preview, reverses order, and steps ten copies with undo (captures under `docs/captures/nodus/align-panel/` and `docs/captures/nodus/step-and-repeat/`). Cheaper substitute that fails: menu-only alignment, which the key-object test catches.

## 15. Dimensions, Connectors, and Callouts

Associative dimensions and live connectors for technical drawings and diagrams: live objects bound to the measured or connected elements that update when those move, persisted as `nodus:` parameters with an expanded plain-SVG group as fallback. Connectors route with an own orthogonal router (a visibility-graph approach after Wybrow, Marriott, and Stuckey 2009; libavoid is not ported). Catalog: NP-0649 to NP-0676 (the dimension tool, linear, angular, radial, segment, successive, and stacked dimensions, number format, prefix and suffix, arrows, line style, extension lines, label font and position, associative dimensions, break apart, defaults, the 2-leg callout and break callout apart, the connector tool, right-angle and rounded connectors, the anchor editing tool, segment editing, attachment on move, exit direction, auto anchor snap, anchor position, wrap, text labels, and connector defaults).

**Fidelity:** Tool rail flyouts, property bar, and Dimension Tool Options dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/nodus/main-window/, docs/captures/golden/nodus/dimensions/.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/Canvas/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Tool rail flyouts, property bar, and Dimension Tool Options dialog -- docs/captures/nodus/main-window/ and docs/captures/nodus/dimensions/. The source is now the design named on the Design line; the captures under `docs/captures/nodus/` are before records only, and the approved renders land under `docs/captures/golden/nodus/`.
**Job:** a designer can annotate technical drawings with measurements and diagrams with live connectors. Consumer: the document and DXF export (`D02 T14 §10`).
**Treatment:** dimensions and connectors are live objects bound to the measured or connected elements and update when those move. Cheaper substitute that fails the checkpoint: static lines and text that go stale on move.
**Chrome:** consume the `D02 T07 §9` units and drawing scale, `D02 T07 §11` snapping, the property bar, the `D02 T09 §12` arrowheads, and the history.

**Requires:** display-session -- dimension and connector drawing and rerouting need an interactive desktop

- [ ] Add `Dimension` in `src/Nodus/Photon.Nodus.Core/Annotations/Dimension.cs` implementing `ILiveObject` with kinds linear (horizontal, vertical, aligned), angular, radial (radius or diameter), and segment, bound to element ids and node indices, stored as `nodus:dimension` with an expanded group of lines, arrows, and text. Done when: a dimension reopens live and renders as plain SVG in Inkscape.
- [ ] Add `DimensionTool` (one tool with kind modes plus CorelDRAW flyout aliases) including segment dimensions across a marquee of segments. Done when: each kind has a creation test.
- [ ] Add automatic successive dimensioning and stacked chains from a base line. Done when: a test dimensions four points successively and stacked with the expected values.
- [ ] Add the number format: units, precision, fractional, decimal, or standard style, show units, leading zero, prefix and suffix, and drawing scale from `D02 T07 §9`. Done when: `DimensionFormatTests` cover each option.
- [ ] Add the style: arrow style and scale (from `D02 T09 §12` once it ships, a built-in arrow until then), line weight and type, extension line offset and overhang or hidden, and label font, size, and position (above, below, centered, inside, outside). Done when: each style option changes the expanded geometry in a test.
- [ ] Recompute associative dimensions on the measured element's change event, with static mode freezing the text. Done when: `AssociativeDimensionTests` move the target and assert the updated value. Cheaper substitute: static lines and text.
- [ ] Add Apply to All and Set as Default writing `Nodus.Tools.Dimension.*` defaults. Done when: a new dimension uses the saved defaults after restart.
- [ ] Add Break Dimension Apart and Break Callout Apart, each expanding to plain objects as one command. Done when: undo restores the live object.
- [ ] Add `Connector` in `src/Nodus/Photon.Nodus.Core/Annotations/Connector.cs` and `ConnectorTool` with straight, right-angle, and rounded right-angle connectors whose endpoints bind to anchors. Done when: a connector reopens bound to both elements.
- [ ] Add `OrthogonalRouter` in `src/Nodus/Photon.Nodus.Core/Annotations/OrthogonalRouter.cs` rerouting on element move and wrapping around objects whose wrap flag is on. Done when: `ConnectorRoutingTests` route around an obstacle and 500 connectors reroute under 16 ms after a move.
- [ ] Add `AnchorEditingTool`: add (double-click), move along the perimeter or to the center, delete, exit direction 0, 90, 180, or 270, auto anchor as a snap point, and position relative to the object. Done when: `AnchorEditingTests` cover each.
- [ ] Add connector segment editing: move the middle node, slide the ends, and add or merge corners. Done when: each edit is one command with undo.
- [ ] Add a connector text label that follows the connector, and connector defaults (geometric anchors as snap points, route distance) as `Nodus.Tools.Connector.*` settings. Done when: moving an endpoint moves the label and each key has a named reader.
- [ ] Add `TwoLegCalloutTool`: a leader with two segments, text, callout shape, and gap. Done when: a callout reopens live with its text.
- [ ] Commit `tests/fixtures/nodus/svg/annotations/` with Inkscape goldens of the fallback and the version. Done when: `AnnotationRoundTripTests` compare element by element.
- [ ] Add a Dimensions, Connectors, and Callouts page to `docs/user/nodus/`. Done when: every tool and option is listed.
- [ ] Commit: `"nodus: associative dimensions, routed connectors, and callouts"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~AnnotationRoundTripTests|FullyQualifiedName~DimensionFormatTests|FullyQualifiedName~AssociativeDimensionTests|FullyQualifiedName~ConnectorRoutingTests"` exits 0 and the annotations fixture round-trips with Inkscape rendering the fallback (version quoted); a driven run moves a connected and dimensioned object with the connector rerouting and the dimension updating, then undoes (capture under `docs/captures/nodus/dimensions/`). Cheaper substitute that fails: static annotation objects, which `AssociativeDimensionTests` catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with this file's test classes reporting
- [ ] Every fixture under `tests/fixtures/nodus/svg/live-shapes/`, `generators/`, `compound-shapes/`, `clipping/`, and `annotations/` round-trips element by element and opens in Inkscape (version quoted)
- [ ] The benchmark project reports the §5, §8, §9, §10, §14, and §15 budgets met
- [ ] `python scripts/todo-graph.py query parity --phase 5` reports every NP row planned to this file stamped
- [ ] `python scripts/todo-graph.py validate` clean
