# Gesso Standards

Gesso is the suite's raster editor. This file adds to [`shared.md`](shared.md) and never contradicts it. Gesso is being built natively from its plan in `todo/03-gesso/`; the C# prototype it grew from (Imago) is preserved at the `csharp-final` tag as a behavior reference (`git show csharp-final:<path>`), read to learn what a feature did and never extended.

## Code

| Folder | Holds |
| ------ | ----- |
| `native/gesso/` core library (`isotone::gesso`) | The document, layers, masks, selections, history, and the readers and writers of its formats. No window header: it is tested without a window |
| The shared engines (`isotone::core` and the engine libraries the plan names) | The pixel engine with its tile store, color management, and the pixel engine extensions, shared by recorded operator exception because Albumen and Stilus use them too |
| `native/gesso/` executable (`gesso.exe`) | The app shell: its composition root, its surfaces built from `isotone::ui`, and the canvas |
| `native/tests/gesso/` | The GoogleTest suites, fixtures, and fuzz corpora |

Settings and logs live under `%LOCALAPPDATA%\Rizonesoft\Gesso\`.

## Pixels

The pixel engine's data contract is the spec's "The engines":

- Pixel data lives in tiles in the scratch-backed tile store (copy-on-write, 256 by 256 by default), with memory, video memory, and undo budgets set from the machine's resources. Nothing holds a whole-image buffer except an import or export in flight, and an allocation failure ends the operation with a message and leaves the document as it was.
- Documents store 8-bit or 16-bit integer channels, or 32-bit float, per the document's mode. Processing runs in 32-bit float. A conversion between modes is explicit and named, and extended-range values are clamped only on conversion to an integer mode.
- **Colors are stored with straight alpha and composited premultiplied.** Premultiplied integer storage destroys color under low alpha and breaks file round trips, so straight storage keeps every channel exact; conversion to premultiplied happens only inside compositing and the filters that need it, and back on commit. Tests cover zero and near-zero alpha, round trips through each file format, and colors under fully transparent pixels. (This replaces the premultiplied working format this file named before the native re-plan; the premultiply kernels and the pixel-layout contract are `D00 T04 §2` and `D01 T03 §1`.)
- Color management is explicit: a document carries its profile, a pixel never changes profile silently, and transfer functions follow the document's profile with linear-light processing where an operation requires it.
- Not-a-number and infinities are replaced at import and never produced by an operation.

## Hot paths

Rendering, compositing, painting, and input are hot paths ([`cpp.md`](cpp.md), "SIMD and performance"):

- Zero allocations per frame or per dab: buffers are pooled or reused, and a hot loop builds no container.
- No virtual call, lock, or allocation per pixel.
- SIMD kernels (SSE4.1 and AVX2 with runtime dispatch on x64, NEON on ARM64) for per-pixel loops, each with a scalar reference the tests compare against: exact for integer kernels, within the spec's tolerance for float.
- A benchmark names the budget before an optimization lands, and its record under `docs/benchmarks/` is quoted in the section that lands it.

## GPU

- The GPU paths run on Direct3D 11 through the render thread, which owns the immediate context; engine work is cut into bounded dispatches the render thread interleaves with interface and canvas frames, interface frames first.
- Every GPU resource has one owner that can rebuild it from CPU-side state. A device loss, or a machine with no usable hardware device, falls back to the CPU path (or the WARP software device for the interface), logs one Warning, and produces the same pixels within the tolerance the tests state: at most 1 code value at 8-bit, at most 4 at 16-bit, and for float the larger of 2^-16 absolute and 2^-16 relative.
- HLSL naming: constant buffers `cbPascalCase`, textures `tPascalCase`, samplers `sPascalCase`; one shader per file.

## Formats

- Every codec is a format reader or writer and owes a format fidelity proof against a committed fixture ([`testing.md`](testing.md)), with the tolerance stated; every reader also owes its input-safety and fuzzing proofs.
- A codec that cannot represent a document (layers into JPEG, 16-bit into an 8-bit format) says so before it writes: flatten, convert, or refuse, never silently.
- Each codec library is chosen by a recorded decision (`docs/dev/decisions.md`), registered in `docs/dev/native-libraries.md` with its license checked against GPL-3.0, linked statically, and checked daily against advisories.
