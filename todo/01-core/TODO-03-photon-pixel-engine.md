---
schema_version: 1
id: photon-pixel-engine
domain: 01-core
status: draft
title: "TODO-03 -- Photon.Core Pixel Engine: Buffers, Resampling, Adjustments, and Bitmap Effects"
depends_on: []
track: C3
---

# TODO-03 -- Photon.Core Pixel Engine: Buffers, Resampling, Adjustments, and Bitmap Effects

> **Goal:** `Photon.Core/Imaging/` holds one deterministic, golden-tested pixel engine in pure managed C# with `System.Numerics.Vector<T>` SIMD: tiled RGBA8, RGBA16, and float buffers with premultiplied alpha, one effect contract (parameter schema, seed, preview at scale, progress, cancellation, serializable description), resampling and geometric correction, palette quantization and dithering, the tonal and color adjustments, and every bitmap effect family both competitors ship (blur, sharpen, noise, distort, artistic, brush-stroke, sketch, texture, creative, camera, color-transform, edge, custom, pixelate, video). It lives in `Photon.Core` by operator decision (2026-09-26) although Nodus (`D02 T12`) is its first consumer; Imago's filter pipeline (`D03 T05 §1`) is its planned second consumer, so nothing in it references WPF, a SkiaSharp view, or a Nodus type.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** There is no `src/Photon.Core/` yet; `D01 T02 §1` creates the project and this file adds its `Imaging/` folder. Imago already tiles its raster layers at 256 by 256 (`TileSize = 256` in `src/Imago/src/Imago.Core/Tiles/Tile.cs`), the tile size this engine adopts so its second consumer needs no re-tiling. Imago has a filter plug-in contract (`src/Imago/src/Imago.Plugins.Abstractions/IFilterPlugin.cs`), and its filter commands in `src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs` only log that a dialog would open; `D03 T05 §1` routes them through this engine. Nodus's bitmap element `src/Nodus/Bezier.Core/Models/Elements/SvgImage.cs` (120 lines) holds encoded bytes only (`EmbeddedData`, `MimeType`) with no decoded pixel access, and `src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs` draws no `SvgImage` at all. There is no decisions log yet: the first section that records a decision creates `docs/dev/decisions.md`.
<!-- claim: absent src/Photon.Core -->
<!-- claim: count "TileSize = 256" src/Imago/src/Imago.Core/Tiles/Tile.cs = 1 -->
<!-- claim: exists src/Imago/src/Imago.Plugins.Abstractions/IFilterPlugin.cs -->
<!-- claim: count "Opening Gaussian Blur dialog" src/Imago/src/Imago.UI/ViewModels/MainWindowViewModel.cs = 1 -->
<!-- claim: lines src/Nodus/Bezier.Core/Models/Elements/SvgImage.cs = 120 -->
<!-- claim: count "SvgImage" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->
<!-- claim: absent docs/dev/decisions.md -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- logging, settings, performance budgets, and determinism rules the engine follows
- [`standards/imago.md`](../../standards/imago.md) -- premultiplied RGBA tiles, SIMD with a scalar path the tests compare against, and the hot-path rules the second consumer already follows
- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- what lives in `Photon.Core`
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- the blueprint for this file; [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) -- the catalog rows each section owns
- GIMP 3.0, libvips 8.16, and ImageMagick 7.1 -- golden reference implementations; the exact version and command are recorded beside each fixture
- -> XREF: D01 T02 §1 -- the `Photon.Core` project this file extends
- -> XREF: D01 T02 §2 -- the settings store that holds engine defaults such as the tile cache size
- -> XREF: D01 T04 §3 -- Lab, CMYK, and duotone bitmap modes that convert through the color engine and hand RGBA buffers to this one
- -> XREF: D02 T12 §1 -- Nodus bitmap objects consume resampling, rotation, perspective, and quantization
- -> XREF: D02 T12 §2 -- the Nodus FX stack registers every effect of this engine
- -> XREF: D02 T12 §3 -- the Nodus Image Adjustment Lab composes the adjustments of §4 and §5
- -> XREF: D02 T12 §4 -- Nodus tracing quantizes through §3's `ColorReducer`
- -> XREF: D02 T13 §8 -- print as bitmap dithers 1-bit output through §3
- -> XREF: D02 T14 §12 -- raster export quantizes PCX, PNG-8, and GIF through §3
- -> XREF: D02 T15 §9 -- AI upscaling, which falls back to §2's local Lanczos resampler
- -> XREF: D03 T05 §1 -- Imago's filter pipeline, the planned second consumer
- -> XREF: D01 T06 §14 -- the pixel engine extensions cites §1: the contract, registry, `EffectDescription`, `TileRunner`, and golden harness it extends, never duplicates; §2: the `Resampler`, `InverseMapper`, `PerspectiveCorrector`, and `LensCorrector` the distort and lens kernels sample through; §3: the `HalftoneScreen` and dither kernels D01 T06 §14 extends; §5: the `Vibrance` math D01 T06 §3's depth of field reuses; §6: Gaussian, motion, radial, zoom, rank filters, smart blur, unsharp, and noise that D01 T06 §2, D01 T06 §4, and D01 T06 §5 extend; §7: `InverseMapEffect`, `Displace`, `MeshWarp`, `Pixelate`, `Offset`, `Emboss`, and `DiffuseGlow` that D01 T06 §6, D01 T06 §7, D01 T06 §8, D01 T06 §11, D01 T06 §13, and D01 T06 §14 extend; §8: `StrokeField` and `StrokeRenderer` that D01 T06 §11 and D01 T06 §12 reuse; §10: `ReliefLighting`, `CellPartition`, and `Vignette` that D01 T06 §8, D01 T06 §9, and D01 T06 §14 reuse; §11: `LightingEffects`, `LensFlare`, `BumpMap`, `Mezzotint`, `ColorHalftone`, the edge kernels, `UserDefinedConvolution`, and `Diffuse`, extended there
- -> XREF: D01 T07 §3 -- the suite develop engine cites §1: float tiles, the effect contract, the golden harness, and `CounterRng`; §2: `Resampler`, `LensCorrector`, and `PerspectiveCorrector`, which D01 T07 §3's geometry stage composes; §4: `Histogram`, `ToneCurve`, `TemperatureTint`, and white balance math D01 T07 §1 consumes; §5: `HslMath` and `Vibrance` formulas D01 T07 §2 evaluates on OkLCh; §6: `UnsharpMask`, `RemoveNoise`, and `AddNoise` D01 T07 §3 consumes
- -> XREF: D03 T08 §7 -- Imago parity document and view cites §2: `Resampler`, `Rotator`, and `PerspectiveCorrector`, which D03 T08 §7 extends in place and D03 T08 §9 consumes; §4: `Histogram` for D03 T08 §11
- -> XREF: D03 T09 §9 -- Imago parity layers cites §2: the resampler D03 T09 §9's smart objects resample their source with; §4: `ToneCurve` for contours and blend-range curves; §6: Gaussian blur for effects and live masks
- -> XREF: D03 T10 §1 -- Imago parity selection and channels cites §2: the resampler D03 T10 §1 and D03 T10 §8 transform masks with; §4: the histogram percentiles D03 T10 §4's tonal ranges read
- -> XREF: D03 T11 §5 -- Imago parity adjustments and color cites §3: the quantizer, dithering, and posterize behind indexed and bitmap modes and D03 T11 §5's dither; §4: the histogram, levels, tone curve, auto adjust, equalize, exposure, temperature, and white balance D03 T11 §2 extends; §5: hue saturation, color balance, vibrance, selective color, replace colors, desaturate, black and white, channel mixer, invert, and threshold D03 T11 §3 to D03 T11 §5 use; §11: photo filter, colorize, and sepia
- -> XREF: D03 T12 §1 -- Imago parity painting cites §3: ordered and error-diffusion dither for gradients
- -> XREF: D03 T13 §1 -- Imago parity retouching and transform cites §2: the resampler, inverse mapper, and perspective corrector D03 T13 §1, D03 T13 §5, D03 T13 §7, D03 T13 §8, and D03 T13 §11 sample through; §7: the `MeshWarp` and `Offset` D03 T13 §6 and D03 T13 §11 extend
- -> XREF: D03 T14 §1 -- Imago parity filters cites §1: the registry, descriptions, and effects every surface runs
- -> XREF: D03 T15 §1 -- Imago parity photo (Camera Raw and merges) cites §2: resampler and rotator for workflow size, alignment resampling, and scan straightening; §6: classical denoise pass on merged radiance
- -> XREF: D03 T17 §8 -- Imago parity formats cites §2: mipmap and export resampling in D03 T17 §8; §3: indexed quantization for GIF and palette formats in D03 T17 §8
- -> XREF: D03 T18 §1 -- Imago parity export, color management, and print cites §2: export resamplers; §3: palette quantization for PNG-8 and GIF
- -> XREF: D03 T19 §8 -- Imago AI cites §2: the Lanczos resampler for local fitting and the upscale fallback; §6: classical scratch, dust, and JPEG artifact passes in restoration and super zoom

## Outcome

- `src/Photon.Core/Imaging/` holds premultiplied RGBA8, RGBA16, and float buffers with 256-pixel tiles, one `IPixelEffect` contract, an `EffectRegistry`, and JSON effect descriptions that round-trip byte-identical.
- Resampling (nearest, bilinear, bicubic, Lanczos-3), rotation, perspective, and lens correction match libvips and ImageMagick goldens within stated tolerances.
- 1-bit and paletted conversion with seven dither methods and seven palette types, plus posterize, match ImageMagick and GIMP goldens where a reference exists.
- Every tonal and color adjustment and every bitmap effect family both competitors ship is registered, deterministic for a seed, cancellable at tile granularity, and proven by a reference golden or a committed snapshot golden plus property tests.
- Every effect run writes one Serilog Information line, and nothing in `Photon.Core/Imaging/` references WPF, a SkiaSharp view, or a Nodus type.

**Adjacency:** list=not-applicable (an engine has no browsable records; the effect registry is listed by the Nodus Effects menu, D02 T12 §2); document=not-applicable (no printed output of its own); settings=applicable @ D01 T02 §2; reporting=applicable @ D01 T03 §4; notifications=applicable @ D01 T03 §1; permissions=not-applicable (the engine reads and writes no files; texture, frame, and displacement maps arrive as buffers from the app); audit=applicable @ D01 T03 §1; exchange=applicable @ D01 T03 §1; reverse=not-applicable (effects are pure functions from buffer to buffer; undo belongs to the consumers' history, D01 T02 §4)

**Adjacency rationale:** The tile cache size is the one engine setting, stored through the suite settings store. Reporting is the histogram of §4 and the per-effect timing in the log. Progress and cancellation flow through `IProgress<EffectProgress>` and `CancellationToken` from §1 and are shown by the consumers' status strips. Every `Apply` writes one Information line with the effect id, parameter hash, pixel count, and elapsed time. Effect descriptions serialize to JSON for the consumers' `nodus:` namespace and presets, and §4 reads Corel `.pst` curve presets. Effects never mutate their source, so reversal is the consumers' undo.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Pixel buffers, the effect contract, and the golden harness | D01 T02 §1 |  [ ]   |
|   2   |   §2    | Resampling, rotation, straighten, perspective, and lens correction | §1 |  [ ]   |
|   3   |   §3    | Palette quantization and dithering | §1 |  [ ]   |
|   4   |   §4    | Tonal adjustments | §1 |  [ ]   |
|   5   |   §5    | Color adjustments | §4 |  [ ]   |
|   6   |   §6    | Blur, sharpen, and noise | §1 |  [ ]   |
|   7   |   §7    | Distort and 3D-style effects | §2 |  [ ]   |
|   8   |   §8    | Artistic and art-stroke effects | §6 |  [ ]   |
|   9   |   §9    | Brush-stroke and sketch effects | §6 |  [ ]   |
|  10   |   §10   | Texture and creative effects | §6 |  [ ]   |
|  11   |   §11   | Camera, color-transform, edge, custom, pixelate, and video effects | §5, §6 |  [ ]   |

---

## 1. Pixel Buffers, the Effect Contract, and the Golden Harness

Every later section runs on the buffers, the effect contract, and the golden harness built here, so they are built once and proven before any effect lands. Buffers are premultiplied by default and tiled at Imago's 256-pixel tile size so the second consumer needs no re-tiling; the contract carries a seed, a preview scale, progress, and cancellation so every effect is deterministic and interruptible; the harness compares against reference goldens with a stated tolerance and writes a diff image on failure. Catalog: NP-1824 to NP-1826 (3 features: automatic conversion to RGB for RGB-only effects, manual bitmap inflation, and auto inflation for effects).

**Fidelity:** no surface of its own (the Nodus effect surfaces are D02 T12 §2 and D02 T12 §3)

- [ ] Add `src/Photon.Core/Imaging/Pixels/Rgba8.cs`, `Rgba16.cs`, and `RgbaF.cs` as `readonly record struct` pixel types with explicit conversions between them. Done when: `PixelTypeTests` round-trip every 8-bit value through 16-bit and float and back unchanged. Source: `standards/imago.md` "Pixels" (8-bit, 16-bit, and a float path, conversions explicit and named).
- [ ] Add `src/Photon.Core/Imaging/PixelBuffer.cs`: `PixelBuffer<TPixel>` with width, height, stride, `Span<TPixel>` row access, a `IsPremultiplied` flag, and `Premultiply()` and `Unpremultiply()`; no SkiaSharp or WPF type in its public API. Done when: `PixelBufferTests` prove premultiply then unpremultiply returns the original within 1 of 255 for alpha above 0, and a public-API reflection test finds no `SkiaSharp` or `System.Windows` type.
- [ ] Add `src/Photon.Core/Imaging/TiledPixelBuffer.cs` with 256 by 256 tiles (the value of Imago's `Tile.TileSize`) and `TileCache` bounded by the setting `Photon.Imaging.TileCacheMegabytes` (default 512) read through `ISettingsStore` from `D01 T02 §2`. Done when: `TileCacheTests` show the cache evicting least-recently-used tiles once the configured size is reached, and changing the setting changes the ceiling without a restart.
- [ ] Add `src/Photon.Core/Imaging/Effects/IPixelEffect.cs` with `Id`, `Version`, `Category`, `Schema`, `ExpandBounds(Rect)`, and `Apply(source, destination, parameters, EffectContext)`. Done when: the interface compiles with XML documentation on every member and a test effect (`InvertTestEffect`) implements it.
- [ ] Add `src/Photon.Core/Imaging/Effects/EffectParameterSchema.cs`: typed parameters (number with range, default, and unit; integer; boolean; enum; color as `RgbaF`; point; curve; buffer reference) with `Validate(parameters)`. Done when: `EffectParameterSchemaTests` reject an out-of-range value by name and fill a missing value with its default.
- [ ] Add `src/Photon.Core/Imaging/Effects/EffectContext.cs` carrying `Seed`, `PreviewScale`, `IProgress<EffectProgress>`, and `CancellationToken`, plus `CounterRng` (a counter-based random generator keyed by seed, tile, and pixel) so random effects are independent of tile order. Done when: `CounterRngTests` produce identical values for the same key regardless of call order.
- [ ] Add `src/Photon.Core/Imaging/Effects/TileRunner.cs` that runs an effect tile by tile in parallel, reports progress per tile (the consumers notify the user through their status strips), and observes cancellation between tiles. Done when: `EffectContractTests.CancelStopsWithinOneTile` cancels after the first progress report and asserts at most one further tile completes.
- [ ] Add `src/Photon.Core/Imaging/Effects/EffectRegistry.cs` discovering effects by an `[PixelEffect]` attribute and exposing them by id and by category for the consumers' menus. Done when: `EffectRegistryTests` find the test effect by id and list its category.
- [ ] Add `src/Photon.Core/Imaging/Effects/EffectDescription.cs` (id, version, parameters, seed) with a source-generated `System.Text.Json` context, the format consumers export and import in their documents and presets. Done when: `EffectContractTests.DescriptionRoundTrip` serializes, deserializes, and reserializes a description of every parameter type byte-identically.
- [ ] Add `src/Photon.Core/Imaging/BitmapInflation.cs`: `Inflate(buffer, pixels, percent, keepAspect)` for manual inflation (CD-2109) and `AutoInflate(buffer, IPixelEffect, parameters)` that grows by the effect's `ExpandBounds` margin (CD-2110); the document-level default (CD-2111) is read by the consumer, not stored here. Done when: `BitmapInflationTests` assert the inflated sizes for pixels, percent, and keep-aspect cases and that a Gaussian-radius margin is added on every side.
- [ ] Add `src/Photon.Core/Imaging/ColorModeAdapter.cs`: `ToRgba(buffer, SourceMode)` for grayscale, paletted, and 1-bit sources, returning a `ModeChanged` flag so the consumer can tell the user (CD-2108); Lab and CMYK sources arrive through `D01 T04 §3`. Done when: `ColorModeAdapterTests` convert each source mode and assert the flag.
- [ ] Add a SIMD path with `System.Numerics.Vector<T>` beside a scalar reference path in `src/Photon.Core/Imaging/Simd/VectorOps.cs` (premultiply, lerp, lookup application). Done when: `SimdParityTests` run both paths on 100 random buffers and assert bit-exact equality.
- [ ] Add the golden harness `tests/Photon.Core.Tests/Imaging/GoldenHarness.cs`: loads `tests/fixtures/imaging/<effect>/input.png`, runs the effect, compares with `expected.png` by maximum and mean channel delta within a per-effect tolerance, and writes `actual.png` and `diff.png` under `build/golden-diffs/` on failure. Done when: a deliberately altered expected image fails with both metrics quoted in the message.
- [ ] Add `tests/fixtures/imaging/README.md` defining `reference.txt` (reference implementation, its version, and the exact command) required beside every golden. Done when: a harness test fails any fixture folder without `reference.txt`.
- [ ] Add property-test helpers in `tests/Photon.Core.Tests/Imaging/EffectProperties.cs`: output bounds equal `ExpandBounds`, the same seed gives identical bytes, a fully transparent input stays transparent, and alpha is preserved where the effect declares it. Done when: the helpers pass on the test effect and fail on a mutant that ignores the seed.
- [ ] Log one Serilog Information line per `Apply` as the engine's audit trail (`Applied {EffectId} v{Version} params {ParamHash} on {Pixels} px in {ElapsedMs} ms`) from `TileRunner`. Done when: a test with a Serilog test logger asserts the line and its properties.
- [ ] Add the 100-megapixel budget test `tests/Photon.Core.Tests/Imaging/Budget/LargeBufferBudgetTests.cs` (`[Trait("Category", "Budget")]`): a per-pixel effect on a 10,000 by 10,000 RGBA8 tiled buffer allocates less than one extra full-size buffer, measured with `GC.GetAllocatedBytesForCurrentThread`. Done when: the test passes and prints the measured bytes; a mutant that copies the whole buffer fails it.
- [ ] Create `docs/dev/decisions.md` if absent and add the row "Pixel engine: pure managed C# with `System.Numerics.Vector<T>` SIMD in `Photon.Core/Imaging/`, no native imaging dependency, GPL-3.0 clean" with the reasons (determinism, testability, second consumer). Done when: the row names this section.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's filter pipeline (`D03 T05 §1`) wraps `IPixelEffect` for its layers. Done when: the README names the consumer and the contract members it uses.
- [ ] Commit: `"core: pixel buffers, the effect contract, and the golden harness"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx` exits 0 with `PixelBufferTests`, `TileCacheTests`, `EffectContractTests` (including `CancelStopsWithinOneTile` and `DescriptionRoundTrip`), `BitmapInflationTests`, `ColorModeAdapterTests`, `SimdParityTests`, and `LargeBufferBudgetTests` reporting, with the measured allocation quoted. Cheaper substitute that fails: a single flat `byte[]` buffer with straight alpha and no cancellation, which the budget test and the cancellation test reject.

## 2. Resampling, Rotation, Straighten, Perspective, and Lens Correction

Every bitmap object Nodus places will be resized, straightened, or corrected, and Imago's Image Size and rotate canvas commands need the same math. This section builds the geometric operations once, as separable resamplers and inverse-mapped transforms on premultiplied float rows, and proves them against libvips and ImageMagick. Catalog: NP-1727 to NP-1733 (7 features: resample interpolation, maintain aspect, maintain file size, resolution change, the GPU resampling decision, lens distortion correction, and perspective correction).

**Fidelity:** no surface of its own (the Resample and Straighten dialogs are D02 T12 §1)

- [ ] Add `src/Photon.Core/Imaging/Geometry/Resampler.cs` with `ResampleMode { NearestNeighbor, Bilinear, Bicubic, Lanczos3 }` using separable kernels on premultiplied float rows. Done when: `ResamplerTests` downsample and upsample every fixture in each mode. Source: the libvips `vips resize` kernel definitions (Corel's two modes are CD-1972 and CD-1973).
- [ ] Commit libvips 8.16 goldens under `tests/fixtures/imaging/resample/` for each mode at 50 and 200 percent with `reference.txt`. Done when: bicubic and Lanczos match within a maximum delta of 2 of 255 and nearest matches exactly.
- [ ] Add `src/Photon.Core/Imaging/Geometry/ResampleRequest.cs` (pixel width and height, or physical size plus horizontal and vertical dpi, `MaintainAspect`, `MaintainFileSize`) with a pure `Resolve()` returning target pixels and dpi (CD-1977, CD-1978, CD-1979). Done when: `ResampleRequestTests` cover aspect only, file size only, both, and independent horizontal and vertical dpi.
- [ ] Measure a 24-megapixel Lanczos resample in `tests/Photon.Core.Tests/Imaging/Budget/ResampleBudgetTests.cs` and record the GPU decision (CD-1980) as a row in `docs/dev/decisions.md`: the managed SIMD path is the only resampler, no GPU path is built, AI upsampling stays with `D02 T15 §9`, with the measured time as evidence. Done when: the row quotes the measured milliseconds.
- [ ] Add `src/Photon.Core/Imaging/Geometry/Rotator.cs`: rotate by any angle with bicubic sampling into an expanded canvas. Done when: `RotatorTests` match an ImageMagick 7.1 `-rotate` golden within 2 of 255 for 7.5 and minus 12 degrees.
- [ ] Add `Rotator.CropToRotatedRect(angle, width, height, keepAspect)` returning the largest axis-aligned rectangle inside the rotated image, for the straighten dialog. Done when: tests assert the rectangle for 0, 5, 15, and 45 degrees against closed-form values.
- [ ] Add `src/Photon.Core/Imaging/Geometry/InverseMapper.cs`: sample a source through any `Map(x, y) -> (u, v)` with a chosen `ResampleMode` and an edge mode (wrap, clamp, transparent, color). Done when: an identity map reproduces the input bit-exactly in every edge mode.
- [ ] Add `src/Photon.Core/Imaging/Geometry/PerspectiveCorrector.cs`: vertical and horizontal keystone correction from two angles, and a four-point homography variant (CD-1986, and the engine for CD-2075). Done when: `PerspectiveCorrectorTests` map a synthetic keystoned grid back to a rectangle with corner error under 0.5 pixel.
- [ ] Add `src/Photon.Core/Imaging/Geometry/LensCorrector.cs`: radial distortion `r' = r(1 + k1 r^2 + k2 r^4)` with a single user amount mapped to `k1` for barrel and pincushion (CD-1982). Done when: `LensCorrectorTests` match an ImageMagick 7.1 `-distort Barrel` golden under `tests/fixtures/imaging/lens/` within 2 of 255.
- [ ] Register `Resample`, `Rotate`, `CorrectPerspective`, and `CorrectLens` as effects in the `EffectRegistry` with schemas, so consumers can store them as `EffectDescription`. Done when: each round-trips through `DescriptionRoundTrip`.
- [ ] Report progress and observe cancellation for every operation over 16 megapixels. Done when: a cancellation test on a 20-megapixel rotate stops within one tile.
- [ ] Add a 100-megapixel Lanczos downsample budget case to `LargeBufferBudgetTests`. Done when: it stays under the §1 allocation ceiling.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Image Size and rotate canvas commands reuse `Resampler` and `Rotator` through `D03 T05 §1`. Done when: the README lists them.
- [ ] Commit: `"core: resampling, rotation, perspective, and lens correction"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx` exits 0 with `ResamplerTests`, `RotatorTests`, `PerspectiveCorrectorTests`, and `LensCorrectorTests` comparing against the libvips 8.16 and ImageMagick 7.1 goldens in `tests/fixtures/imaging/resample/`, `rotate/`, `perspective/`, and `lens/` (maximum delta 2 of 255 for bicubic, quoted per fixture). Cheaper substitute that fails: delegating to `SKBitmap.Resize`, which has no Lanczos mode and misses the libvips golden.

## 3. Palette Quantization and Dithering

1-bit and paletted bitmaps, posterize, tracing, and web export all reduce colors, so reduction is built once with every dither and palette type both competitors expose. Error diffusion is one class driven by kernel tables, palettes are built by named strategies, and the whole thing is deterministic for a seed so a trace or an export reproduces. Catalog: NP-1734 to NP-1752 (19 features: seven 1-bit methods, seven palette types, paletted dithering and intensity, paletted presets, processed palette editing, range sensitivity, and posterize).

**Fidelity:** no surface of its own (the Black and White and Paletted dialogs are D02 T12 §1)

- [ ] Add `src/Photon.Core/Imaging/Quantize/BilevelConverter.cs` with `BilevelMethod { LineArt, Ordered, Halftone, CardinalityDistribution, Jarvis, Stucki, FloydSteinberg }` and an `Intensity` parameter (threshold for line art, bias for the rest) (CD-1996 to CD-2002). Done when: `BilevelConverterTests` produce only 0 and 1 values for every method.
- [ ] Add `src/Photon.Core/Imaging/Quantize/ErrorDiffuser.cs` driven by kernel tables for Floyd-Steinberg, Jarvis-Judice-Ninke, and Stucki with serpentine scanning. Done when: the Floyd-Steinberg output matches an ImageMagick 7.1 `-dither FloydSteinberg -monochrome` golden under `tests/fixtures/imaging/quantize/` exactly.
- [ ] Add Jarvis and Stucki property tests (mean luminance preserved within 1 percent on a gradient, no run of identical output longer than the kernel width on a 50 percent gray field). Done when: both pass and a kernel-table mutant fails them.
- [ ] Add `src/Photon.Core/Imaging/Quantize/OrderedDither.cs` with 2x2 to 8x8 Bayer matrices. Done when: the 8x8 output on a ramp matches a GIMP 3.0 ordered dither golden.
- [ ] Implement `CardinalityDistribution` as a blue-noise threshold with a committed 64 by 64 blue-noise mask, documented in the class as Nodus's reading of the Corel option. Done when: a committed snapshot golden matches and the method's XML documentation says it is an interpretation.
- [ ] Add `src/Photon.Core/Imaging/Quantize/HalftoneScreen.cs` (screen type round, line, square, cross, ellipse; angle; lines per inch; output dpi). Done when: `HalftoneScreenTests` measure the dot pitch and angle from the output within 1 percent.
- [ ] Add `src/Photon.Core/Imaging/Quantize/PaletteBuilder.cs` with `Uniform` (6x7x6 levels), `StandardVga` (the fixed 16 colors), `Grayscale` (256), `System` (the Windows 20-color table as a committed constant), and `Custom` (a caller-supplied color list) (CD-2010, CD-2011, CD-2014, CD-2015, CD-2016). Done when: `PaletteBuilderTests` assert each palette's size and first and last entries.
- [ ] Add `Adaptive` (median cut) to `PaletteBuilder`. Done when: a 16-color adaptive palette of a fixture matches a GIMP 3.0 indexed-conversion palette within 4 of 255 per entry after sorting.
- [ ] Add `Optimized` (octree over color frequency) with `RangeSensitivity` (a focus color and a weight that reserves more entries near it) (CD-2013, CD-2020). Done when: raising the weight increases the number of palette entries within 32 of the focus color on a fixture, asserted in a test.
- [ ] Add `src/Photon.Core/Imaging/Quantize/PalettedConverter.cs`: `Convert(buffer, palette, DitherMethod, intensity)` returning an `IndexedBuffer` whose `Palette` is editable (the processed palette, CD-2019). Done when: `PalettedConverterTests` assert every output index is valid and editing a palette entry changes only pixels with that index.
- [ ] Add `src/Photon.Core/Imaging/Quantize/QuantizePreset.cs` (palette type, color count, dither, intensity, sensitivity) with JSON save and load (CD-2018). Done when: a preset round-trips byte-identically.
- [ ] Add `src/Photon.Core/Imaging/Quantize/ColorReducer.cs`: `Reduce(buffer, maxColors, seed)` as the public entry point `D02 T12 §4` tracing and web export call. Done when: the same seed yields identical indexed output twice and the palette size never exceeds `maxColors`.
- [ ] Register a `Posterize` effect (levels per channel 2 to 32) in the `EffectRegistry` (CD-2224). Done when: it matches a GIMP 3.0 posterize golden exactly for 4 and 8 levels.
- [ ] Add a budget case: an optimized 256-color palette on a 24-megapixel image completes under 2 seconds with progress and cancellation. Done when: `QuantizeBudgetTests` quotes the time and a cancellation case stops within one tile.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Indexed mode and posterize through `D03 T05 §1`. Done when: the README lists them.
- [ ] Commit: `"core: palette quantization, dithering, and posterize"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx` exits 0 with `BilevelConverterTests`, `PaletteBuilderTests`, `PalettedConverterTests`, and `QuantizeBudgetTests` reporting, the Floyd-Steinberg, ordered, adaptive, and posterize outputs matching the ImageMagick 7.1 and GIMP 3.0 goldens in `tests/fixtures/imaging/quantize/`, and the palette-size, index-validity, and same-seed property tests passing. Cheaper substitute that fails: nearest-color mapping with no diffusion, which the Floyd-Steinberg golden rejects.

## 4. Tonal Adjustments

Tone is the first thing anybody corrects in a placed photo. This section builds the histogram and every tonal adjustment both competitors ship as registered adjustments: pure lookups fused per pixel with SIMD, proven against GIMP. It also defines the multi-adjustment preset data that the Nodus Adjustment Lab stores. Catalog: NP-1827 to NP-1835 (9 features: auto adjust, levels, equalize, sample and target, tone curve and its presets, tone curve channel tools, light, gamma, and white balance).

**Fidelity:** no surface of its own (the Nodus adjustment dialogs and Image Adjustment Lab are D02 T12 §3)

- [ ] Add `src/Photon.Core/Imaging/Adjust/Histogram.cs`: per-channel and luminance histograms (256 bins for 8-bit, 65,536 for 16-bit) computed tile-parallel, with `Percentile(channel, p)`, mean, and median, and a `HistogramSummary` report (count, mean, median, clipped percent per channel) the consumers display. Done when: `HistogramTests` count synthetic ramps exactly and percentile queries return the expected bins.
- [ ] Add `src/Photon.Core/Imaging/Adjust/Levels.cs` (input black, gamma, input white, output black and white, per channel and composite). Done when: `LevelsTests` match a GIMP 3.0 `gimp-drawable-levels` golden within 1 of 255.
- [ ] Add `AutoAdjust` (clip 0.1 percent per channel through `Histogram.Percentile`, neutralize the midtone) (CD-2271). Done when: it matches a GIMP 3.0 auto stretch golden within 2 of 255 on the committed fixture.
- [ ] Add `Equalize` with the histogram target models flat, normal, and custom as a parameter (CD-2273). Done when: `EqualizeTests` show the flat model's output histogram within 5 percent of uniform on a fixture.
- [ ] Add `SampleAndTarget`: sampled shadow, midtone, and highlight colors mapped to target colors per channel on the levels lookup (CD-2274). Done when: a test maps sampled colors exactly onto the targets.
- [ ] Add `src/Photon.Core/Imaging/Adjust/ToneCurve.cs` with `CurveStyle { Curve, Straight, Freehand, Gamma }` evaluated through monotone cubic splines into 256 and 65,536 entry lookups (CD-2275). Done when: `ToneCurveTests` match a GIMP 3.0 curves golden within 1 of 255 for a three-node curve.
- [ ] Add `Smooth()`, `Mirror()`, and `Reset(channel)` and `ResetAll()` on the curve model, and an all-channels composite view (CD-2277). Done when: tests assert mirror symmetry and that reset restores the identity lookup.
- [ ] Add `src/Photon.Core/Imaging/Adjust/CorelCurvePresetReader.cs`, a read-only parser for Corel `.pst` curve presets (CD-2276), with a committed sample under `tests/fixtures/imaging/adjust/presets/`. Done when: the sample reads into the expected node list and a malformed file returns a named error.
- [ ] Add `Light` (brightness, contrast, intensity, highlights, shadows, midtones) (CD-2278). Done when: `LightTests` assert identity at zero and monotone output for each slider on a ramp.
- [ ] Add `Gamma` (CD-2280) and `Exposure` (stops in linear light). Done when: `Gamma` matches a GIMP 3.0 levels-gamma golden within 1 of 255 and a one-stop exposure doubles linear values below clipping.
- [ ] Add `TemperatureTint` (Kelvin shift and green-magenta tint in linear light) and `WhiteBalance` (auto gray-world or a sampled neutral) (CD-2281). Done when: `WhiteBalanceTests` bring a tinted gray card fixture to neutral within 1 of 255 per channel.
- [ ] Fuse every adjustment into one per-pixel lookup or 3x3 matrix where possible, using the §1 SIMD path. Done when: a budget test applies each adjustment to a 24-megapixel image under 150 ms and quotes the times.
- [ ] Add `src/Photon.Core/Imaging/Adjust/AdjustmentPreset.cs`: an ordered list of `EffectDescription` with JSON serialization, the data `D02 T12 §3` stores and applies. Done when: a three-adjustment preset round-trips byte-identically.
- [ ] Register every adjustment in the `EffectRegistry` under the `Adjust` category. Done when: `EffectRegistryTests` list the nine features' adjustments.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's levels, curves, and brightness and contrast (`D03 T05 §2`) run on these types through `D03 T05 §1`. Done when: the README lists them.
- [ ] Commit: `"core: histogram and tonal adjustments"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx` exits 0 with `HistogramTests`, `LevelsTests`, `ToneCurveTests`, `LightTests`, and `WhiteBalanceTests` reporting, levels and curves matching the GIMP 3.0 goldens in `tests/fixtures/imaging/adjust/` within 1 of 255, and the budget times quoted. Cheaper substitute that fails: a curve evaluated by linear interpolation between nodes, which the spline golden rejects.

## 5. Color Adjustments

Color correction completes the adjustment set. Each adjustment is a lookup or matrix built on shared HSL and RGB matrix helpers, fused per pixel, and proven against GIMP where GIMP has the same operation, or by snapshot goldens plus property tests where it does not. Catalog: NP-1836 to NP-1846 (11 features: invert, threshold, color balance, hue saturation lightness, black and white, vibrance, selective color, replace colors current and legacy, desaturate, and channel mixer).

**Fidelity:** no surface of its own (menus and dialogs are D02 T12 §3)

- [ ] Add `src/Photon.Core/Imaging/Adjust/HslMath.cs` and `RgbMatrix.cs` (RGB to HSL and back, 3x4 matrices with composition). Done when: `HslMathTests` round-trip every 8-bit gray and 10,000 random colors within 1 of 255.
- [ ] Add `HueSaturationLightness` with a master range plus reds, yellows, greens, cyans, blues, and magentas, each with feathered edges (CD-2282). Done when: it matches a GIMP 3.0 hue-saturation golden under `tests/fixtures/imaging/color/` within 2 of 255.
- [ ] Add `ColorBalance` (cyan-red, magenta-green, yellow-blue for shadows, midtones, and highlights, with `PreserveLuminance`) (CD-2279). Done when: it matches a GIMP 3.0 color-balance golden within 2 of 255.
- [ ] Add `Vibrance` (saturation boost weighted by inverse saturation; skin-tone protection off by default and documented) (CD-2284). Done when: a property test shows already saturated pixels move less than muted ones, and a snapshot golden matches.
- [ ] Add `SelectiveColor` (CMYK percentage shifts for reds, yellows, greens, cyans, blues, magentas, whites, neutrals, and blacks; relative and absolute), computed in RGB with the naive CMY conversion documented until `D01 T04 §1` provides profile-accurate CMYK (CD-2285). Done when: a snapshot golden matches and a property test shows a reds-only shift leaves a pure blue pixel unchanged.
- [ ] Add `ReplaceColors` (sampled color, hue range ring, saturation range, smoothing, HSL output) (CD-2286). Done when: a test replaces a red swatch with green and leaves a blue swatch unchanged.
- [ ] Add `ReplaceColorsLegacy`, mapping the older parameter set onto the same kernel (CD-2287). Done when: a legacy parameter set and its mapped current set produce identical bytes.
- [ ] Add `Desaturate` (luminosity, average, and lightness modes) (CD-2288). Done when: it matches a GIMP 3.0 desaturate golden exactly for each mode.
- [ ] Add `BlackAndWhite` (six per-color weights plus tint hue and strength) (CD-2283, CD-2291). Done when: a snapshot golden matches and all-equal weights reproduce `Desaturate` luminosity within 1 of 255.
- [ ] Add `ChannelMixer` (3x3 plus a constant, monochrome flag) (CD-2289). Done when: it matches a GIMP 3.0 channel-mixer golden within 1 of 255.
- [ ] Add `Invert` (CD-2223) and `Threshold` (level, plus a band mode with low and high) (CD-2225). Done when: invert twice is the identity and threshold output contains only black and white.
- [ ] Fuse each adjustment into one lookup or matrix per pixel. Done when: the §4 budget test covers these adjustments and each stays under 150 ms on 24 megapixels.
- [ ] Register every color adjustment in the `EffectRegistry` under the `Adjust` category. Done when: `EffectRegistryTests` list all eleven.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's hue and saturation adjustment (`D03 T05 §2`) through `D03 T05 §1`. Done when: the README lists it.
- [ ] Commit: `"core: color adjustments"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx` exits 0 with `ColorAdjustTests` comparing hue-saturation, color balance, desaturate, and channel mixer against the GIMP 3.0 goldens in `tests/fixtures/imaging/color/` (tolerances quoted), snapshot goldens matching for vibrance, selective color, and black and white, and the property tests passing. Cheaper substitute that fails: a hue shift by rotating RGB channels, which the hue-saturation golden rejects.

## 6. Blur, Sharpen, and Noise

Blur, sharpen, and noise are the most used effect families and the base several later families build on (glow, sketch, lighting). Twenty-eight effects fit one section because they share five kernel families; each checklist item is one family or one tightly related group, never one effect per item. Catalog: NP-1847 to NP-1874 (28 features: Gaussian, radial, smart, tune, motion, zoom, and bokeh blur; directional smooth, jaggy despeckle, low pass, smooth, soften; local equalization; dust and scratch; tune sharpen; add noise, 3-D stereo noise, maximum, median, minimum, tune noise, remove moire, remove noise; adaptive unsharp, directional sharpen, high pass, sharpen, and unsharp mask).

**Fidelity:** no surface of its own (menus, gallery, and FX panel are D02 T12 §2)

- [ ] Add `src/Photon.Core/Imaging/Effects/Blur/GaussianBlur.cs`: separable exact kernel up to radius 32 and a three-box approximation above it, with `ExpandBounds` equal to three sigma. Done when: it matches a libvips 8.16 `gaussblur` golden within 1 of 255 at radius 4 and 50.
- [ ] Add `LowPass`, `Soften`, and `Smooth` as parameterized presets on `GaussianBlur` (CD-2144, CD-2150, CD-2149). Done when: each is registered with its own id and a snapshot golden matches.
- [ ] Add line-integral samplers `MotionBlur` (angle, distance), `RadialBlur` (spin angle, center, quality), and `ZoomBlur` (center, amount) (CD-2145, CD-2146, CD-2151, CD-2252, AI-0737). Done when: `MotionBlur` matches an ImageMagick 7.1 `-motion-blur` golden within 3 of 255 and radial and zoom match snapshot goldens.
- [ ] Add `BokehBlur` (disc kernel with highlight boost) (CD-2251) and `SmartBlur` (radius, threshold, and normal, edge-only, and overlay-edge modes as a thresholded bilateral) (CD-2148, AI-0738). Done when: both match snapshot goldens and smart blur leaves a hard edge fixture within 2 of 255 at threshold 50.
- [ ] Add edge-aware smoothing `DirectionalSmooth` and `JaggyDespeckle` (CD-2141, CD-2143). Done when: both match snapshot goldens and reduce the gradient energy of a noisy flat region by at least half.
- [ ] Add `TuneBlur`, `TuneSharpen`, and `TuneNoise` as parameter-set browsers (four, four, and nine variants) over the underlying effects, each registered under its own id for the `D02 T12 §2` thumbnail pickers (CD-2140, CD-2169, CD-2202). Done when: each variant's description resolves to an underlying effect and parameters in a test.
- [ ] Add `src/Photon.Core/Imaging/Effects/Sharpen/FrequencySplit.cs` and on it `UnsharpMask` (percentage, radius, threshold) (CD-2209). Done when: it matches a GIMP 3.0 unsharp-mask golden and an ImageMagick 7.1 `-unsharp` golden within 2 of 255.
- [ ] Add `Sharpen` (edge level, threshold, preserve colors by sharpening luminance only), `AdaptiveUnsharp`, `DirectionalSharpen`, and `HighPass` on the same split (CD-2208, CD-2205, CD-2206, CD-2207). Done when: `HighPass` matches a snapshot golden and preserve-colors keeps hue within 1 degree on a colored edge fixture.
- [ ] Add rank filters `Median`, `Minimum`, and `Maximum` with a sliding histogram (constant time per pixel in the radius) (CD-2200, CD-2201, CD-2199). Done when: each matches an ImageMagick 7.1 `-statistic` golden exactly at radius 3.
- [ ] Add `DustAndScratch` (median gated by a contrast threshold) and `RemoveNoise` (adaptive median) (CD-2168, CD-2204). Done when: both remove the committed salt-and-pepper fixture's specks and leave its edges within 2 of 255.
- [ ] Add seeded noise generators `AddNoise` (uniform, Gaussian, spike; amount; color or mono) and `ThreeDStereoNoise` (random-dot stereogram from a luminance depth map), both on `CounterRng` (CD-2197, CD-2198). Done when: the same seed yields identical bytes under two different tile orders and a different seed differs.
- [ ] Add `RemoveMoire` (a notch in a low-pass band) and `RemoveJpegArtifacts` (classical 8x8 block deblocking, no model) (CD-2203). Done when: the deblocking lowers the measured blockiness metric of a quality-20 JPEG fixture by at least 30 percent.
- [ ] Add `LocalEqualization` (CLAHE with tile size and clip limit) (CD-2167). Done when: it matches a snapshot golden and the output histogram per tile respects the clip limit.
- [ ] Add a budget test: Gaussian radius 50 on 24 megapixels under 400 ms. Done when: `BlurBudgetTests` quotes the time.
- [ ] Add a cancellation test for every effect over one second on a 24-megapixel buffer. Done when: each stops within one tile.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Blur and Sharpen menu (`D03 T05 §3`) routes its stub commands here through `D03 T05 §1`. Done when: the README lists the effects it wires.
- [ ] Commit: `"core: blur, sharpen, and noise effects"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx` exits 0 with `BlurSharpenNoiseTests` comparing against the libvips 8.16, GIMP 3.0, and ImageMagick 7.1 goldens in `tests/fixtures/imaging/blur/`, `sharpen/`, and `noise/` with per-effect tolerances quoted, the seed-determinism tests for the noise generators passing, and `BlurBudgetTests` quoting its time. Cheaper substitute that fails: a box blur registered as Gaussian, which the libvips `gaussblur` golden rejects.

## 7. Distort and 3D-Style Effects

Distortions are all inverse maps: each effect supplies where an output pixel samples from, and the §2 `InverseMapper` does the sampling, so there are no holes and one edge-mode implementation. The two interactive editors (mesh warp and 3-D rotate) are parameter editors in Nodus; here they are parameters. Catalog: NP-1875 to NP-1897 (23 features: diffuse glow, glass, ocean ripple, texture and glass surface controls, 3-D rotate, cylinder, emboss, page curl, pinch and punch, sphere, zig zag, blocks, displace, mesh warp, offset, pixelate, ripple, shear, swirl, tile, wet paint, whirlpool, and wind).

**Fidelity:** no surface of its own (the mesh warp and 3-D rotate interactive editors are parameter editors in D02 T12 §2)

- [ ] Add `src/Photon.Core/Imaging/Effects/Distort/InverseMapEffect.cs`, a base class whose subclasses supply `Map(x, y) -> (u, v)` and sample through the §2 `InverseMapper` with wrap, clamp, transparent, or color edges. Done when: a zero-strength subclass reproduces the input bit-exactly.
- [ ] Add `Ripple`, `Shear`, `Swirl`, `PinchPunch`, `Sphere`, `Cylinder`, and `ZigZag` on `InverseMapEffect` (CD-2190, CD-2191, CD-2192, CD-2121, CD-2122, CD-2117, CD-2124). Done when: swirl, pinch, and ripple match ImageMagick 7.1 `-swirl`, `-implode`, and `-wave` goldens within 3 of 255 and the rest match snapshot goldens.
- [ ] Add `Whirlpool` (with savable styles as `EffectDescription` JSON), `OceanRipple`, and `Offset` (tile, stretch, or color fill) on the same base (CD-2195, AI-0749, CD-2188). Done when: snapshot goldens match and offset by the full width is the identity in wrap mode.
- [ ] Add `Displace` reading a displacement-map buffer supplied by the consumer, with horizontal and vertical scale and tile or stretch fit (CD-2186). Done when: a zero map is the identity and a constant map shifts the image by the expected pixels.
- [ ] Add `src/Photon.Core/Imaging/Effects/Distort/SurfaceTexture.cs` (scaling, relief, light direction, invert, and a loaded texture buffer) with built-in procedural textures (frosted, blocks, canvas, tiny lens) and no bundled third-party images (AI-0777). Done when: each built-in texture renders a snapshot golden.
- [ ] Add `Glass` on `Displace` plus `SurfaceTexture` (AI-0748). Done when: a snapshot golden matches for each built-in texture.
- [ ] Add `MeshWarp` (up to 10 gridlines, node positions as parameters, savable presets as `EffectDescription` JSON) through bilinear patch inversion (CD-2187). Done when: an undisturbed mesh is the identity and a moved node displaces only its four patches.
- [ ] Add `ThreeDRotate` (yaw and pitch on a plane, best fit) through a projective map (CD-2115). Done when: zero angles are the identity and best fit keeps the output inside the source bounds.
- [ ] Add `PageCurl` (corner, vertical or horizontal, opaque or transparent, curl and background colors, width and height percent) as a cylinder projection with shading (CD-2120). Done when: a snapshot golden matches for each corner.
- [ ] Add `Emboss` (depth, level, direction, and original color, gray, black, or other color modes) as a directional derivative (CD-2118). Done when: a flat input produces a flat mid-gray in gray mode and snapshot goldens match.
- [ ] Add `DiffuseGlow` (grain, glow amount, clear amount) combining seeded noise from `CounterRng` with a highlight blur from §6 (AI-0747). Done when: a snapshot golden matches and the output is seed-deterministic.
- [ ] Add cell and streak operations `Blocks`, `Pixelate` (square, rectangular, circular), `Tile`, `WetPaint`, and `Wind` (strength, direction, opacity), with seeded randomness (CD-2185, CD-2189, CD-2193, CD-2194, CD-2196). Done when: pixelate cells are uniform in color and snapshot goldens match.
- [ ] Register all 23 effects in the `EffectRegistry` under the `Distort` category and run the §1 property suite over them (bounds from `ExpandBounds`, seed determinism, transparent in stays transparent). Done when: `DistortTests` report the property suite per effect.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Distort filter menu through `D03 T05 §1`. Done when: the README lists it.
- [ ] Commit: `"core: distort and 3D-style effects"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx` exits 0 with `DistortTests` comparing swirl, pinch, and ripple against the ImageMagick 7.1 goldens in `tests/fixtures/imaging/distort/`, every other effect against its committed snapshot golden, and the identity-at-zero and coverage property tests passing for all 23. Cheaper substitute that fails: forward-mapped distortion that leaves holes, which the identity and coverage tests reject.

## 8. Artistic and Art-Stroke Effects

Twenty-eight painterly and drawing-media effects have no open reference implementation, so they are built on three shared primitives (a stroke orientation field, a seeded stroke renderer, and a procedural paper texture) and each effect is a parameter set over them. Proof is by committed snapshot goldens at two parameter sets plus the §1 property suite, and one checklist item covers a group, never a single effect. Catalog: NP-1898 to NP-1925 (28 features: colored pencil, cutout, dry brush, film grain, fresco, neon glow, paint daubs, palette knife, plastic wrap, poster edges, rough pastels, smudge stick, sponge, underpainting, watercolor, pointillist, charcoal, conte crayon, crayon, cubist, dabble, impressionist, pastels, pen and ink, scraperboard, sketch pad, water marker, and wave paper).

**Fidelity:** no surface of its own (the Effect Gallery that previews these is D02 T12 §2)

- [ ] Add `src/Photon.Core/Imaging/Effects/Artistic/StrokeField.cs`: a structure-tensor orientation field built from the §6 gradients with a smoothing radius. Done when: `StrokeFieldTests` recover the orientation of a synthetic sine grating within 2 degrees.
- [ ] Add `src/Photon.Core/Imaging/Effects/Artistic/StrokeRenderer.cs`: seeded dabs and strokes along a `StrokeField` with size, length, pressure, and color sampling, drawn on `CounterRng` so output is tile-order independent. Done when: two tile orders produce identical bytes.
- [ ] Add `src/Photon.Core/Imaging/Effects/Artistic/PaperTexture.cs`: procedural paper and canvas grains (fine, rough, canvas, laid) with scale and relief. Done when: each grain renders a snapshot golden.
- [ ] Add the painterly group as parameter sets over the primitives: dry brush, paint daubs (brush size and type), palette knife, fresco, impressionist, dabble, smudge stick, underpainting, and sponge (AI-0723, AI-0727, AI-0728, CD-2131, AI-0725, CD-2130, CD-2129, AI-0732, AI-0734, CD-2221, AI-0733). Done when: each is registered with a schema and two snapshot goldens.
- [ ] Add `Watercolor` with granulation and edge darkening on the paper texture (AI-0735, CD-2137). Done when: two snapshot goldens match and edge pixels are darker than region interiors on a flat-color fixture.
- [ ] Add the drawing-media group: colored pencil, rough pastels, pastels, crayon, conte crayon (foreground and background colors as RGBA parameters), charcoal, sketch pad, scraperboard, water marker, and wave paper (AI-0721, AI-0731, CD-2132, CD-2127, AI-0758, CD-2126, AI-0756, CD-2125, CD-2136, CD-2135, CD-2138, CD-2139). Done when: each is registered with two snapshot goldens.
- [ ] Add `PenAndInk` with cross-hatch and stipple styles (CD-2133, CD-2250). Done when: stipple output contains only ink and paper colors and snapshot goldens match for both styles.
- [ ] Add the graphic group: cutout (§3 posterize plus region simplification), poster edges, cubist, film grain, plastic wrap, and neon glow (AI-0722, AI-0730, CD-2128, AI-0724, AI-0729, AI-0726). Done when: each is registered with two snapshot goldens and cutout's distinct color count never exceeds its levels parameter.
- [ ] Add `Pointillist` (colored dots with size and lightness) (AI-0753, CD-2134). Done when: two snapshot goldens match and dot density scales with the size parameter.
- [ ] Route all randomness through `EffectContext.Seed`. Done when: the §1 seed-determinism property passes for all 28 effects under two tile orders.
- [ ] Commit snapshot goldens at two parameter sets per effect under `tests/fixtures/imaging/artistic/` with `reference.txt` stating "snapshot: no reference implementation" and the Nodus commit that produced them. Done when: every effect folder has both goldens and the file.
- [ ] Run the §1 property suite (bounds, determinism by seed, alpha preservation, near-identity at minimum strength where defined) over every effect. Done when: `ArtisticTests` report it per effect.
- [ ] Assert no two effects produce identical output on the same fixture and seed. Done when: a pairwise hash test passes across all 28.
- [ ] Add budget tests: any effect on a 12-megapixel image under 3 seconds with progress and cancellation, and a preview at `PreviewScale` 0.25 under 250 ms for the gallery. Done when: `ArtisticBudgetTests` quote the worst times.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Artistic filter menu through `D03 T05 §1`. Done when: the README lists it.
- [ ] Commit: `"core: artistic and art-stroke effects"`

**Test checkpoint:** Unit test with snapshot goldens: `dotnet test Photon.slnx` exits 0 with `ArtisticTests` matching every committed snapshot in `tests/fixtures/imaging/artistic/`, the §1 property suite and the pairwise distinct-output test passing for all 28 effects, and `ArtisticBudgetTests` quoting times. Cheaper substitute that fails: one posterize relabeled per effect, which the pairwise distinct-output and seed-determinism tests expose.

## 9. Brush-Stroke and Sketch Effects

The brush-stroke and sketch families reuse the §8 stroke field and renderer, and the sketch family is two-color: luminance maps onto a foreground and a background color that the consumer passes as RGBA values, never as references to a Nodus swatch, so Imago can pass its own. If §8 has not landed when this section runs, this section builds `StrokeField` and `StrokeRenderer` and §8 consumes them. Catalog: NP-1926 to NP-1946 (21 features: accented edges, angled strokes, crosshatch, dark strokes, ink outlines, spatter, sprayed strokes, sumi-e, bas relief, chalk and charcoal, chrome, graphic pen, halftone pattern, note paper, photocopy, plaster, reticulation, stamp, torn edges, water paper, and glowing edges).

**Fidelity:** no surface of its own (the Effect Gallery is D02 T12 §2)

- [ ] Confirm `StrokeField` and `StrokeRenderer` from §8 exist in `src/Photon.Core/Imaging/Effects/Artistic/`; if not, build them there with their §8 tests. Done when: `StrokeFieldTests` pass in this section's build.
- [ ] Add the brush-stroke group in `src/Photon.Core/Imaging/Effects/BrushStrokes/`: accented edges, angled strokes, crosshatch, and dark strokes (AI-0739, AI-0740, AI-0741, AI-0742). Done when: each is registered with two snapshot goldens.
- [ ] Add ink outlines, spatter, sprayed strokes, and sumi-e to the same folder (AI-0743, AI-0744, AI-0745, AI-0746). Done when: each is registered with two snapshot goldens and spatter is seed-deterministic.
- [ ] Add `src/Photon.Core/Imaging/Effects/Sketch/TwoColorMapper.cs`: maps a scalar field onto the segment between a foreground and a background `RgbaF` parameter. Done when: a property test asserts every output pixel lies on that segment within 1 of 255.
- [ ] Add relief-style sketch effects on `TwoColorMapper`: bas relief, chrome, note paper, plaster, and water paper (AI-0754, AI-0757, AI-0761, AI-0763, AI-0767). Done when: each is registered with two snapshot goldens and passes the two-color property.
- [ ] Add drawing-style sketch effects: chalk and charcoal, graphic pen, photocopy, stamp, and torn edges (AI-0755, AI-0759, AI-0762, AI-0765, AI-0766). Done when: each is registered with two snapshot goldens and passes the two-color property.
- [ ] Add `HalftonePattern` (dot, circle, line) and `Reticulation` (seeded) (AI-0760, AI-0764). Done when: halftone line spacing matches its size parameter within 1 pixel and both pass the two-color property.
- [ ] Add `GlowingEdges` (edge width, brightness, smoothness) from the §6 gradient and Gaussian blur (AI-0768). Done when: a flat input yields black output and snapshot goldens match.
- [ ] Commit snapshot goldens at two parameter sets per effect under `tests/fixtures/imaging/sketch/` and `tests/fixtures/imaging/brush-strokes/` with `reference.txt`. Done when: every effect folder has both goldens.
- [ ] Run the §1 property suite over all 21 effects. Done when: `BrushSketchTests` report it per effect.
- [ ] Assert color parameters are plain `RgbaF` values in every sketch schema. Done when: a reflection test finds no parameter typed as anything but `RgbaF` for colors.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Brush Strokes and Sketch filter menus through `D03 T05 §1`. Done when: the README lists them.
- [ ] Commit: `"core: brush-stroke and sketch effects"`

**Test checkpoint:** Unit test with snapshot goldens: `dotnet test Photon.slnx` exits 0 with `BrushSketchTests` matching every committed snapshot in `tests/fixtures/imaging/sketch/` and `brush-strokes/`, and the two-color property passing for the twelve sketch effects. Cheaper substitute that fails: a grayscale threshold registered as each sketch effect, which the two-color property with non-gray colors and the snapshot set reject.

## 10. Texture and Creative Effects

Texture and creative effects share two primitives: relief lighting over a height map and seeded cell partitions. Most of the 27 effects are parameter sets over those two, grouped one item per group. Only procedural textures ship: canvas maps and frames come from the user's own files as buffers, and no Corel or Adobe content is bundled. Catalog: NP-1947 to NP-1973 (27 features: crystallize, craquelure, grain, mosaic tiles, patchwork, stained glass, texturizer, fabric, frame, glass block, mosaic, scatter, smoked glass, vignette, vortex, brick wall, bubbles, canvas, cobblestone, elephant skin, etching, plastic, plaster wall, relief sculpture, screen door, stone, and The Boss bitmap bevel).

**Fidelity:** no surface of its own (the Effect Gallery is D02 T12 §2)

- [ ] Add `src/Photon.Core/Imaging/Effects/Texture/ReliefLighting.cs`: shade a height map with light direction, elevation, depth, and color. Done when: a flat height map yields uniform shading and a hemisphere height map lights the side facing the light, asserted in `ReliefLightingTests`.
- [ ] Add `src/Photon.Core/Imaging/Effects/Texture/CellPartition.cs`: seeded Voronoi and grid cells with a size parameter. Done when: cells are stable for a seed and the cell count scales inversely with the square of the cell size within 10 percent.
- [ ] Add the procedural height sources: brick, cobblestone, stone, plaster, elephant skin, bubbles, screen door, canvas weave, and craquelure cracks. Done when: each renders a snapshot golden.
- [ ] Add relief effects on those sources: craquelure, brick wall, cobblestone, stone, plaster wall, elephant skin, bubbles, and screen door (AI-0769, CD-2210, CD-2213, CD-2220, CD-2217, CD-2214, CD-2211, CD-2219). Done when: each is registered with two snapshot goldens.
- [ ] Add `Texturizer` (built-in procedural texture or a loaded buffer) and `Canvas` (preset or loaded canvas map) (AI-0774, CD-2212). Done when: a loaded uniform buffer is the identity at full strength and snapshot goldens match.
- [ ] Add `Etching`, `Plastic`, and `ReliefSculpture` as relief lighting over the image's own luminance (CD-2215, CD-2216, CD-2218). Done when: each is registered with two snapshot goldens.
- [ ] Add `Grain` with the eleven Illustrator grain types (regular, soft, sprinkles, clumped, contrasty, enlarged, stippled, horizontal, vertical, speckle) (AI-0770). Done when: each type renders a distinct snapshot golden.
- [ ] Add the cell group: stained glass (piece size, solder width and color), crystallize (cell size), mosaic tiles, patchwork, mosaic with elliptical pieces, and glass block (AI-0773, CD-2179, AI-0751, CD-2172, AI-0771, AI-0772, CD-2176, CD-2175). Done when: each is registered with two snapshot goldens and passes the cell-count property.
- [ ] Add `Fabric` (needlepoint, rug hooking, quilt, strings, ribbons, tissue collage) (CD-2173). Done when: each style renders a distinct snapshot golden.
- [ ] Add the creative group: `Frame` (a frame buffer supplied by the consumer, opacity, blur and feather, scale, rotation), `Vignette` (ellipse, circle, rectangle, square; color; offset; fade), `SmokedGlass` (tint, opacity, blur), `Scatter` (direction, amount), and `Vortex` (inner and outer direction) (CD-2174, CD-2180, CD-2178, CD-2177, CD-2181). Done when: each is registered with two snapshot goldens and vignette with zero fade leaves the center pixel unchanged.
- [ ] Add `BitmapBevel` (The Boss: width, height, smoothness, light direction and elevation, color) on the alpha edge through `ReliefLighting` (CD-2249). Done when: an opaque rectangle gains a lit and a shaded edge and its interior is unchanged.
- [ ] Commit snapshot goldens at two parameter sets per effect under `tests/fixtures/imaging/texture/` with `reference.txt`, and assert no bundled image asset exists under `src/Photon.Core/Imaging/`. Done when: every effect folder has both goldens and a test finds no `.png`, `.jpg`, or `.bmp` embedded resource in `Photon.Core`.
- [ ] Run the §1 property suite over all 27 effects. Done when: `TextureCreativeTests` report it per effect.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Texture and Stylize filter menus through `D03 T05 §1`. Done when: the README lists them.
- [ ] Commit: `"core: texture and creative effects"`

**Test checkpoint:** Unit test with snapshot goldens: `dotnet test Photon.slnx` exits 0 with `TextureCreativeTests` matching every committed snapshot in `tests/fixtures/imaging/texture/`, the cell-count and seed-stability property tests passing, and the no-bundled-image test passing. Cheaper substitute that fails: one tiled bitmap overlay for every texture effect, which the snapshot set and the no-bundled-image test expose.

## 11. Camera, Color-Transform, Edge, Custom, Pixelate, and Video Effects

The last families reuse what the earlier sections built: camera effects are §5 matrices and §6 blurs, lighting is §10 relief lighting, edge effects share §6 gradient kernels, and custom convolution is a general kernel with a divisor and offset. References are named per fixture where one exists and snapshot goldens cover the rest. Catalog: NP-1974 to NP-1994 (21 features: color halftone, mezzotint, de-interlace, NTSC colors, colorize, diffuse, lens flare, lighting effects, photo filter, sepia toning, spot filter, time machine, bit planes, psychedelic, solarize, edge detect, find edges, trace contour, band pass, bump map, and user-defined convolution).

**Fidelity:** no surface of its own (menus and FX panel are D02 T12 §2)

- [ ] Add the camera matrices in `src/Photon.Core/Imaging/Effects/Camera/`: `Colorize` (hue, saturation), `SepiaToning`, and `PhotoFilter` (color, density, preserve luminosity) on the §5 `RgbMatrix` (CD-2152, CD-2157, CD-2156). Done when: each matches a snapshot golden and photo filter with preserve luminosity keeps luminance within 1 of 255.
- [ ] Add `Diffuse` and `SpotFilter` (focus ellipse, blur, darken) on the §6 Gaussian (CD-2153, CD-2158). Done when: spot filter leaves the focus center unchanged and snapshot goldens match.
- [ ] Add `TimeMachine` as seven named parameter sets over §5 adjustments and the §10 grain (CD-2159). Done when: each style resolves to its composed descriptions and renders a snapshot golden.
- [ ] Add `LensFlare` (brightness, lens type 50-300 mm zoom, 35 mm, 105 mm, position) (CD-2154). Done when: the flare center pixel is the brightest and snapshot goldens match per lens type.
- [ ] Add `LightingEffects` (spot, flood, and sun lights with color, intensity, direction, and cone; a texture channel for embossing; savable presets as `EffectDescription` JSON) through the §10 `ReliefLighting` (CD-2155). Done when: a preset round-trips and snapshot goldens match for each light type.
- [ ] Add the color-transform group: `BitPlanes` (per-channel bit selection), `Psychedelic`, and `Solarize` (CD-2160, CD-2162, CD-2163). Done when: bit plane 7 of a ramp equals a 128 threshold and solarize matches a GIMP 3.0 golden.
- [ ] Add `ColorHalftone` (maximum radius, per-channel screen angles) (AI-0750, CD-2161). Done when: it matches a GIMP 3.0 newsprint golden under `tests/fixtures/imaging/camera/` within the tolerance recorded in its `reference.txt`.
- [ ] Add the edge group sharing Sobel and Prewitt kernels with §6: `EdgeDetect` (background white, black, or other; sensitivity), `FindEdges` (soft or solid; level), and `TraceContour` (level; upper or lower edge pixels) (CD-2164, CD-2165, CD-2166). Done when: a flat input yields a flat output and `EdgeDetect` matches an ImageMagick 7.1 `-edge` golden within 3 of 255.
- [ ] Add `BandPass` (inner and outer radius on the §6 frequency split) and `BumpMap` (preset or loaded map buffer; surface and light) (CD-2182, CD-2183). Done when: band pass with equal radii yields a flat output and bump map with a flat map is the identity.
- [ ] Add `UserDefinedConvolution` (3x3 to 7x7 kernel, divisor, offset) (CD-2184, CD-2254). Done when: a 5x5 kernel matches an ImageMagick 7.1 `-morphology Convolve` golden exactly.
- [ ] Add `Mezzotint` (dots, lines, strokes; seeded) (AI-0752). Done when: output contains only the channel extremes and is seed-deterministic.
- [ ] Add `Deinterlace` (odd or even; duplicate or interpolate) (AI-0775, CD-2222). Done when: duplicate mode makes each odd row equal its even neighbor.
- [ ] Add `NtscColors` (clamp YIQ saturation and luminance to broadcast-safe limits) (AI-0776). Done when: no output pixel exceeds the documented YIQ limits on a saturated fixture.
- [ ] Register all 21 effects in the `EffectRegistry` with categories Camera, Color Transform, Contour, Custom, Pixelate, and Video, and run the §1 property suite and cancellation tests. Done when: `CameraColorEdgeTests` report the suite per effect.
- [ ] Record the second consumer in `src/Photon.Core/Imaging/README.md`: Imago's Render, Stylize, and Other filter menus through `D03 T05 §1`. Done when: the README lists them.
- [ ] Commit: `"core: camera, color-transform, edge, custom, and video effects"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx` exits 0 with `CameraColorEdgeTests` comparing color halftone, solarize, edge detect, and the 5x5 user convolution against the GIMP 3.0 and ImageMagick 7.1 goldens in `tests/fixtures/imaging/camera/`, `edge/`, and `custom/`, snapshot goldens matching for the rest, and the property suite passing for all 21. Cheaper substitute that fails: a fixed 3x3 kernel for user-defined convolution, which the 5x5 golden rejects.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every `tests/Photon.Core.Tests/Imaging/` class reporting, including the budget tests with their times quoted
- [ ] Every fixture folder under `tests/fixtures/imaging/` carries `reference.txt` naming its reference implementation and version, or saying it is a snapshot
- [ ] `grep -rn "System.Windows\|SkiaSharp.Views\|Photon.Nodus" src/Photon.Core/Imaging` prints nothing
- [ ] The engine has one consumer today (Nodus, `D02 T12`); its pending second consumer is Imago's filter pipeline (`D03 T05 §1`), recorded in `src/Photon.Core/Imaging/README.md` rather than claimed as present
- [ ] `python scripts/todo-graph.py validate` clean
