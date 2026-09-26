# Imago Standards

Imago is the suite's raster editor. This file adds to [`shared.md`](shared.md) and never contradicts it. It replaces the imported `src/Imago/STANDARDS.md`, whose naming, async, and documentation rules now live in `shared.md`, and whose ReactiveUI section is retired: Imago uses CommunityToolkit.Mvvm like every other app.

## Projects

| Project | Holds |
| ------- | ----- |
| `Photon.Imago.Core` (today `Imago.Core`) | Document, layers, masks, selections, tiles, history, color |
| `Photon.Imago.Rendering` (today `Imago.Rendering`) | The render graph, compositing, blend modes, the ComputeSharp GPU path and its CPU fallback |
| `Photon.Imago.FileFormats` (today `Imago.FileFormats`) | Codecs and the native layered format |
| `Photon.Imago.Plugins.Abstractions`, `Photon.Imago.Scripting` | The plugin contract and the scripting host (roadmap) |
| `Photon.Imago.Desktop` (today `Imago.UI`) | The WPF app; `AssemblyName` Imago (`Imago.exe`) |

Settings and logs live under `%LOCALAPPDATA%\Rizonesoft\Imago\`.

## Pixels

- Pixel data lives in tiles (`Tile`, `TileCache`, 256 by 256 by default). Nothing holds a whole-image buffer except an import or export in flight.
- The working format is premultiplied RGBA; 8-bit and 16-bit per channel documents are both first-class, and a 32-bit float path exists for adjustments. A conversion between them is explicit and named.
- Color management is explicit: a document carries its profile, and a pixel never changes profile silently.

## Hot paths

Rendering, compositing, painting, and input are hot paths:

- Zero allocations per frame or per dab: `Span<T>`, `stackalloc` for small buffers, `ArrayPool<T>` and object pools for large ones.
- No LINQ, no boxing, no closures capturing per-pixel state.
- SIMD (`Vector<T>`, `System.Runtime.Intrinsics`) for per-pixel loops, with a scalar path the tests compare against.
- A benchmark names the budget before an optimization lands, and the result is quoted in the section that lands it.

## GPU

- ComputeSharp shaders are `readonly partial struct` types implementing `IComputeShader`, one shader per file under `Photon.Imago.Rendering/Shaders/`.
- Every GPU resource has one owner that disposes it. A device loss or a machine without a DirectX 12 device falls back to the CPU path, logs one Warning, and produces the same pixels within the tolerance the tests state.
- HLSL naming: constant buffers `cbPascalCase`, textures `tPascalCase`, samplers `sPascalCase`.

## Formats

- Every codec is a format reader or writer and owes a format fidelity proof against a committed fixture ([`testing.md`](testing.md)), with the tolerance stated.
- A codec that cannot represent a document (layers into JPEG, 16-bit into an 8-bit format) says so before it writes: flatten, convert, or refuse, never silently.
- The codec library is chosen by a recorded decision (`docs/dev/decisions.md`) with its license checked against GPL-3.0. SixLabors.ImageSharp was referenced but used by no code and was removed on 2026-09-26, and 4.x fails the build without a paid license key; the plan removes it, and bringing any version back needs its own recorded decision.
