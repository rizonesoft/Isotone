---
schema_version: 1
id: imago-rendering
domain: 03-imago
status: draft
title: "TODO-02 -- Imago Tiles, Viewport, and the Render Pipeline"
depends_on: []
track: I2
---

# TODO-02 -- Imago Tiles, Viewport, and the Render Pipeline

> **Goal:** Imago's pixels live in tiles, its layers composite through a render graph with every blend mode it names proven against golden images, the canvas shows the composite at any zoom with smooth pan, and a ComputeSharp GPU path produces the same pixels as the CPU path within a stated tolerance, falling back cleanly where no DirectX 12 device exists.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The pieces exist as scaffolding. `Imago.Core/Tiles/` has `Tile` (256 by 256, pooled byte buffers, 81 lines), `TileCoordinate`, and `TileCache` (a concurrent dictionary with a memory cap and least-recently-used eviction, 139 lines), and `TileTests` covers them; `RasterLayer` does not use tiles. `Imago.Rendering/` holds a `RenderContext` with zoom and pan math (45 lines), an `IRenderNode` interface and a `RenderNode` base (37 and 44 lines), an `IPixelShader` interface, and global usings for SkiaSharp and ComputeSharp; no node composites anything. `Imago.Core/Layers/BlendMode.cs` names the Photoshop blend modes (Normal through Luminosity) with categories, and no code implements one. The legacy roadmap's rendering phase (2, 40 items) is entirely open.
<!-- claim: lines src/Imago/src/Imago.Core/Tiles/TileCache.cs = 139 -->
<!-- claim: count "TileCache|Tile\b" src/Imago/src/Imago.Core/Layers/RasterLayer.cs = 0 -->
<!-- claim: lines src/Imago/src/Imago.Rendering/RenderContext.cs = 45 -->
<!-- claim: count "Multiply = 11," src/Imago/src/Imago.Core/Layers/BlendMode.cs = 1 -->

## Inputs

- [`standards/imago.md`](../../standards/imago.md) -- tiles, premultiplied RGBA, zero-allocation hot paths, GPU fallback rules
- [`docs/legacy/imago-roadmap.md`](../../docs/legacy/imago-roadmap.md) -- phases 1.2 (tiled image system) and 2 (rendering engine), the source of this file
- The W3C Compositing and Blending Level 1 specification (https://www.w3.org/TR/compositing-1/) -- the formulas §4 implements and tests against
- -> XREF: D03 T01 §2 -- the ported `ImageCanvas` that §2's viewport drives
- -> XREF: D03 T03 §4 -- the tool system that draws into §2's viewport
- -> XREF: D03 T08 §6 -- Imago parity document and view cites §1: the tile store whose reference counts D03 T08 §6's snapshots share; §2: the viewport and mip cache D03 T08 §3 and D03 T08 §10 extend; §5: GPU parity for D03 T08 §10's display filters
- -> XREF: D03 T09 §3 -- Imago parity layers cites §3: the render graph and `GroupNode` D03 T09 §3 to D03 T09 §8 extend; §4: the blend-mode registry and goldens D03 T09 §6 extends; §5: GPU parity for every compositing path there
- -> XREF: D03 T11 §1 -- Imago parity adjustments and color cites §4: the render graph and blend modes adjustment nodes join
- -> XREF: D03 T15 §1 -- Imago parity photo (Camera Raw and merges) cites §5: the ComputeSharp path the float display transform runs in
- -> XREF: D03 T18 §4 -- Imago parity export, color management, and print cites §2: the viewport display transform D03 T18 §4 and D03 T18 §5 drive; §3: blend gamma in the render graph from D03 T18 §4's advanced settings; §5: the GPU path with CPU parity for the display transform
- -> XREF: D03 T20 §5 -- Imago parity workspace cites §1: the tile cache and swap D03 T20 §5 tunes; §5: the ComputeSharp GPU path D03 T20 §5 toggles

## Outcome

- `RasterLayer` stores its pixels in tiles through `TileCache`, 8-bit and 16-bit per channel, and a 100-megapixel layer opens without allocating a whole-image buffer.
- The canvas renders the document composite at 1 to 3,200 percent zoom, redrawing only the tiles a pan or edit dirtied, within 16 ms per frame on a 100-megapixel document (measured and quoted).
- A render graph composites layers in order with opacity, visibility, and every blend mode the Compositing and Blending specification defines, each proven against a golden image.
- A ComputeSharp compositing path matches the CPU path within 1/255 per channel, and a machine without a DirectX 12 device falls back to the CPU with one Warning log line.

**Adjacency:** list=not-applicable (no browsable records); document=not-applicable (printing is a roadmap item); settings=applicable; reporting=applicable; notifications=not-applicable (rendering is continuous, not a job); permissions=not-applicable (no files written); audit=not-applicable (no user action changes a document here); exchange=not-applicable (codecs are TODO-04's); reverse=not-applicable (no edits)

**Adjacency rationale:** The GPU on/off switch and the tile cache size are settings; the status strip's zoom, position, and memory readouts are the reporting surface.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On              | Status |
| :---: | :-----: | ---------------------------------------------------- | ----------------------- | :----: |
|   1   |   §1    | The tiled image store                                | D03 T01 §1              |  [ ]   |
|   2   |   §2    | The viewport on the tiled document                   | §1, D03 T01 §2          |  [ ]   |
|   3   |   §3    | The render graph composites layers                   | §1                      |  [ ]   |
|   4   |   §4    | Blend modes with golden tests                        | §3                      |  [ ]   |
|   5   |   §5    | The ComputeSharp compositing path with CPU parity    | §4                      |  [ ]   |

---

## 1. The Tiled Image Store

`standards/imago.md` says pixel data lives in tiles and nothing holds a whole-image buffer. The tile types exist; no layer uses them. This section makes `RasterLayer` tile-backed so every later feature (painting, filters, compositing, codecs) works a tile at a time. -> SOURCE: legacy-imago-1.2

- [ ] `RasterLayer` owns a sparse tile grid (`TileGrid` in `Photon.Imago.Core/Tiles/`): tiles are created on first write, an unwritten tile reads as transparent, and bounds are the document size. Done when: `TileGridTests` cover read of an unwritten tile, write across a tile boundary, and bounds clipping.
- [ ] Support 8-bit and 16-bit per channel tiles (`BitDepth` exists in `Photon.Imago.Core/Documents/`), premultiplied RGBA. Done when: tests round-trip a gradient through both depths.
- [ ] Add region read and write APIs (`CopyRegion(Rect, Span<T>)`, `WriteRegion`) that walk tiles without allocating per call. Done when: a BenchmarkDotNet run in `tests/Photon.Imago.Benchmarks` shows 0 bytes allocated per call (quoted).
- [ ] `TileCache` eviction spills least-recently-used tiles of large documents to a scratch file under the app-data folder and reloads them transparently; the cache size is the setting `Imago.Tiles.CacheMB` (default 512). Done when: a test with a 64 MB cap writes a 256-megapixel layer and reads it back exactly.
- [ ] Commit: `"imago: tile-backed raster layers with spill to disk"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `TileGridTests` and the spill test reporting; the benchmark's allocation column reads 0 B for region reads (quoted with the machine's CPU). Cheaper substitute that fails: a `byte[]` per layer sliced into tile views, which the 256-megapixel test under a 64 MB cap cannot pass.

## 2. The Viewport on the Tiled Document

The ported `ImageCanvas` pans and zooms a bitmap. It must show the document composite at any zoom without rendering the whole image: only visible tiles, at a mip level suited to the zoom, re-rendered only when dirty. -> SOURCE: legacy-imago-2.1-2.5

**Fidelity:** Imago main window canvas -- docs/captures/imago/main-window/ (the canvas capture from `D03 T01 §2`).
**Job:** a user can pan and zoom a 100-megapixel image smoothly and read the zoom, cursor position, and memory in the status strip. Consumer: every Imago editing surface.
**Treatment:** `ImageCanvas` hosts an `SKElement` (or `SKGLElement` when available) and draws visible tiles from a per-zoom mip cache (levels at powers of two, built lazily per tile), with nearest-neighbor sampling above 100 percent and a pixel grid above 800 percent; the status strip shows zoom, cursor pixel, and cache memory. Cheaper substitute that fails the checkpoint: rendering the whole composite into one `WriteableBitmap` per frame.
**Chrome:** consume the ported `ImageCanvas`, `Ruler`, `CanvasContainer`, `RenderContext`, and the theme. Do not add a second canvas control.

**Requires:** display-session -- measuring pan and zoom on the live canvas needs an interactive desktop

- [ ] Add `MipTileCache` producing downsampled tiles (box filter, premultiplied) per level, invalidated by tile writes. Done when: tests assert a level-2 tile of a known pattern.
- [ ] `ImageCanvas` draws only tiles intersecting the viewport at the level nearest the zoom. Done when: a test with a fake surface counts drawn tiles for a known viewport.
- [ ] Zoom by Ctrl+wheel around the cursor, fit (Ctrl+0), 100 percent (Ctrl+1), and space-drag pan; rulers follow. Done when: a driven run exercises each.
- [ ] Status strip readouts for zoom, cursor pixel, and cache memory. Done when: they update live in a driven run.
- [ ] Measure frame time panning a generated 10,000 by 10,000 image at 25, 100, and 400 percent. Done when: the median frame time is under 16 ms at each (quoted with the machine).
- [ ] Commit: `"imago: a tiled, mip-mapped viewport with smooth pan and zoom"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the mip and culling tests reporting; the frame-time measurements are quoted; capture `docs/captures/imago/main-window/zoom-800.png` shows the pixel grid. Cheaper substitute that fails: whole-image rendering, which misses the 16 ms budget on the 100-megapixel image.

## 3. The Render Graph Composites Layers

The render graph is interfaces only. It must turn a document (layers in order, with visibility, opacity, and blend mode) into a composite, tile by tile, so only dirty tiles are recomposited after an edit. -> SOURCE: legacy-imago-2.2

- [ ] Implement `LayerNode`, `GroupNode` (pass-through and isolated groups), and `CompositeNode` in `Photon.Imago.Rendering/RenderGraph/`, evaluating per output tile. Done when: `RenderGraphTests` composite a three-layer document with one hidden layer and one at 50 percent opacity and assert exact pixels.
- [ ] Dirty tracking: a tile write marks the output tiles it affects; the graph recomposites only those. Done when: a test counts recomposited tiles after a one-pixel edit (exactly one).
- [ ] Normal blending over premultiplied RGBA with SIMD (`Vector<T>`) and a scalar reference the tests compare. Done when: SIMD and scalar outputs are identical on random tiles.
- [ ] Commit: `"imago: a tile-based render graph with dirty recompositing"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `RenderGraphTests` and the SIMD parity test reporting. Cheaper substitute that fails: recompositing the whole document per edit, which the one-tile count catches.

## 4. Blend Modes with Golden Tests

`BlendMode` names the Photoshop modes; none is implemented. Each separable and non-separable mode is implemented from the W3C Compositing and Blending formulas and proven against goldens, so a document opened from PSD later (`D03 T04 §5`) composites as its author saw it. -> SOURCE: legacy-imago-2.3

- [ ] Implement every separable mode in the specification (normal, multiply, screen, overlay, darken, lighten, color-dodge, color-burn, hard-light, soft-light, difference, exclusion) plus the Photoshop extras `BlendMode` names (linear burn and dodge, vivid, linear, and pin light, hard mix, darker and lighter color, subtract, divide, dissolve), and the non-separable hue, saturation, color, and luminosity. Done when: every `BlendMode` value maps to an implementation or is removed from the enum with a reason in the commit body.
- [ ] Commit goldens under `tests/fixtures/imago/blend/`: a base and a blend image, and per mode the expected result produced by a reference implementation (GIMP or libvips, with its version in `tests/fixtures/imago/blend/VERSION.txt`). Done when: every mode has a golden.
- [ ] `BlendModeFidelityTests` (`[Trait("Category", "Fidelity")]`) compare each mode's output with its golden, passing within 1/255 per channel (8-bit) and stating the tolerance. Done when: every mode passes or names the section owning its gap.
- [ ] Commit: `"imago: every blend mode, proven against reference goldens"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` prints a per-mode result for every `BlendMode` value, all passing within 1/255; swapping the multiply and screen formulas fails both. Cheaper substitute that fails: goldens produced by Imago itself, which prove nothing.

## 5. The ComputeSharp Compositing Path with CPU Parity

Compositing many large layers is the workload a GPU is for. ComputeSharp runs HLSL compute shaders written in C# on DirectX 12. The GPU path must produce the CPU path's pixels, and a machine without a suitable device must keep working. -> SOURCE: legacy-imago-2.4

- [ ] Add compositing shaders (`readonly partial struct` `IComputeShader` per mode family) in `Photon.Imago.Rendering/Shaders/`, uploading dirty tiles in batches. Done when: the GPU path composites the §3 test document.
- [ ] Add `GpuCompositor` with device selection, device-loss handling, and fallback to the CPU path with one Warning log line; the setting `Imago.Rendering.UseGpu` (default on) turns it off. Done when: a test forcing no device falls back and logs the line.
- [ ] `GpuParityTests` run every blend mode on both paths and compare within 1/255 per channel, skipping with a reason on machines without a DirectX 12 device (`[Trait("Requires", "gpu")]`). Done when: the tests pass on the development machine (GPU named in the quote).
- [ ] Benchmark a 20-layer 50-megapixel composite on both paths. Done when: both timings are quoted and recorded in `docs/dev/imago/performance.md`.
- [ ] Commit: `"imago: GPU compositing with CPU parity and a clean fallback"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `GpuParityTests` reporting every mode within tolerance on the development machine; the forced-fallback test passes; the benchmark timings are quoted. Cheaper substitute that fails: a GPU path with no parity test.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` passes every blend-mode golden
- [ ] The viewport frame-time and composite benchmarks are recorded
- [ ] `python scripts/todo-graph.py validate` clean
