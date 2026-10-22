# The native stack: C++20 with our own UI

**Status:** draft for the operator's review, 2026-10-22. Nothing in `todo/` changes on this spec's account until the operator approves it; the re-plan is filed from the approved version.

**Decision it serves:** the operator decided on 2026-10-22 that the suite moves from C# and WPF to C++20 with our own UI on Win32, Direct2D, DirectWrite, and Direct3D ("I feel that C++ and our own UI will get is much closer to Photoshop quality."), judged on "the most control and speed. + small output sizes and dependencies". The options, evidence, and cost are in `docs/dev/decisions.md` (2026-10-22: The native stack).

## What this spec decides

Everything below marked **Default** is a justified default: the choice this spec makes so work can start, its reason, and its cost of changing. The operator can overturn any of them in review. The **Open questions** at the end are the ones that need the operator's call before the re-plan.

## Goals, measured

The point of the move is quality the user can feel, so each goal is a number a benchmark section measures on a stated reference machine, never an impression.

| Goal | Target at each app's first native release | How it is measured |
| ---- | ----------------------------------------- | ------------------ |
| Startup | Main window interactive in under 500 ms, cold | A timer from process start to the first frame that accepts input, logged |
| Interface frame time | Every UI frame under 8 ms at 120 Hz while panning, zooming, and resizing | Per-frame timings from the renderer, 99th percentile reported |
| Pen latency | A brush or pen stroke visible within one frame of the pointer event | Pointer timestamp against present timestamp |
| Output size | Each app's publish folder under 30 MB before optional content (**Default**: a budget, revised by recorded decision when a needed library cannot fit) | `scripts/publish.ps1` reports the size, and a gate fails over budget |
| Dependencies | Windows system components plus statically linked libraries, each recorded with its license | The dependency register (below) and a check that the executable imports only system DLLs |
| Crash safety | No document lost to a crash | Fuzzed file readers, sanitizer runs, and an autosave that a crash test restores |

## The toolchain

- **Language:** C++20, compiled by MSVC from Visual Studio 2026 (installed on the development machine, 18.11, with Windows SDK 10.0.26100). Modules are not used yet (**Default**: headers until MSVC, CMake, and clang-tidy handle modules together without workarounds; cost of changing later is mechanical).
- **Build:** CMake with Ninja and committed `CMakePresets.json` (Debug, Release, ASan; x64 and ARM64), which Visual Studio opens natively (**Default** over MSBuild projects: one build description for the editor, the scripts, and CI; cost of changing is rewriting the presets as `.vcxproj` files).
- **Runtime:** the static C runtime (`/MT`), so no Visual C++ redistributable is installed with an app.
- **Packages:** vcpkg in manifest mode, a committed baseline, and the `x64-windows-static` and `arm64-windows-static` triplets, so every library links into the executable.
- **Warnings and analysis:** `/W4 /WX /permissive-`, MSVC's `/analyze` on CI, clang-tidy with a committed configuration, and clang-format checked by a gate, the C++ equivalents of today's warnings-as-errors and `dotnet format` gates.
- **Tests:** GoogleTest for unit tests, run through CTest (**Default**: the most widely supported C++ test framework with CTest and Visual Studio integration; cost of changing is mechanical per test file). Fuzzing with libFuzzer (`/fsanitize=fuzzer`) for every file reader, and an AddressSanitizer build of the whole test suite on CI.
- **Platform:** Windows 11, x64 and ARM64 (**Default**: the suite already targets Windows 11; ARM64 is built from day one so it never becomes a port).

## The architecture

Four layers, each a static library or an executable, with the same sharing rule the suite already has: code moves into a shared library only when two apps need it.

### Isotone Core (`isotone::core`)

The non-UI foundation every app links: app-data paths, settings stored as JSON with atomic writes and readback, structured logging (one line per action that changes a document or a setting), the command registry (every command once, with its id, label, shortcut, and enabled state, the single source the menus, shortcuts, command search, and layout maps read), undo and redo as recorded commands, a task system on a thread pool, atomic file I/O, crash handling that writes a minidump and keeps the autosave, and the update check.

### Isotone UI (`isotone::ui`)

Our own interface toolkit, drawn to `docs/design/` with nothing in between. It is the largest new piece of work, and the parts a general-purpose framework would hand us are each a section with its own proof:

- **Windows and frames:** Win32 windows with per-monitor DPI awareness (v2), layout in device-independent pixels, and the Isotone title bar drawn by us with the menu bar inside it (DWM frame extension, hit testing that keeps Windows 11 snap layouts on the maximize button).
- **Rendering:** one Direct3D 11 device with Direct2D and DirectWrite on top, a flip-model swap chain per window, and DirectComposition so the document canvas is its own visual with its own swap chain: the interface redraws without touching the canvas, and the canvas redraws without touching the interface (**Default**: Direct3D 11 for its maturity and Direct2D interoperability; Direct3D 12 only where a measured engine need requires it).
- **Element tree:** a retained tree of elements with measure and arrange layout, invalidation, and dirty-rectangle redraw; styles resolved from the design tokens, which a generator turns from `docs/design/tokens.json` into a C++ header, so no color, size, or spacing is typed into the code (design-lint moves to the C++ sources).
- **Controls:** every component in `docs/design/components/` (buttons, inputs, number boxes, sliders, menus, context menus, tabs, lists and trees, the tool rail, the options bar, panels, dialogs, tooltips, toasts, the status bar), built as one set the apps share.
- **Docking:** our own docking system (panels, tab groups, columns, floating windows, the saved workspace as JSON), the layout maps' Panels part being its default.
- **Input:** keyboard focus and commands, pointer input through `WM_POINTER` for mouse, pen (pressure, tilt, barrel button), and touch, the mouse wheel and precision touchpad, and drag and drop through OLE.
- **Text:** text layout with DirectWrite, and text editing that supports input method editors through the Text Services Framework, so Chinese, Japanese, and Korean input works in every text box and in the apps' type tools.
- **Accessibility:** a UI Automation provider for every element, so screen readers, Windows' accessibility tools, and our own driven tests read the same tree (one investment buying both accessibility and testability).

### The engines

Each app's document engine is native and owned by that app until a second app needs it: Stilus's vector engine (geometry, paths, and rendering through Direct2D geometry), Gesso's raster engine (tiled documents at 8, 16, and 32-bit float per channel, blending and filters on Direct3D 11 compute shaders with a SIMD CPU path, color through LittleCMS), and Albumen's catalog and develop pipeline (SQLite for the catalog, LibRaw for RAW decoding). A library joins only by recorded decision (below).

### The apps

`stilus.exe`, `gesso.exe`, and `albumen.exe`: each a thin executable over the shared libraries and its engine, each shipped on its own, each with its own installer, version, and update feed, exactly as today. "Develop together, distribute separately" is unchanged.

## Dependencies

A library is a decision: it is added by the section that needs it, with its license and the URL of its license text in a register (`docs/dev/native-libraries.md`, which `D00 T04 §1` already plans), and it must be compatible with GPL-3.0. Linking is static. Candidates the plan already points to, each to be confirmed with its license text by the section that adds it: LittleCMS 2 (color), libpng, libjpeg-turbo, libwebp, and zlib-ng (image formats), LibRaw (RAW), SQLite (the catalog), spdlog (logging), nlohmann/json (settings and workspaces), and GoogleTest (tests). SkiaSharp and AvalonDock leave with the C# code; the AvalonDock exception in `LICENSE-EXCEPTION.md` is retired when the last C# app is removed, by the section that removes it. A rendering library such as Skia or Blend2D is added only if a measured need Direct2D cannot meet is recorded.

## Testing and the gates

The proof standard in `todo/README.md` carries over, re-expressed for C++:

- **Builds clean:** Debug and Release, x64 and ARM64, warnings as errors, `/analyze` and clang-tidy clean.
- **Static analysis clean:** clang-format and clang-tidy report nothing new on the touched files.
- **Unit test:** a GoogleTest case, cited by name.
- **Driven run with evidence:** the app driven through UI Automation (our own provider makes every control drivable), a log line, a settings readback, or a saved file inspected.
- **Format fidelity proof:** fixtures opened, saved, reopened, and compared, plus a fuzz target for every reader.
- **Goldens:** surfaces rendered offscreen with Direct3D's WARP software rasterizer, so golden images are deterministic on any machine and on CI, and compared with the approved goldens under `docs/captures/golden/` within the design contract's tolerance.

`scripts/check-all.ps1` runs the CMake configure, build, CTest, the format and analysis gates, and every TODO gate. CI builds on GitHub's Windows runners with the MSVC toolset pinned in the presets; the pin is one the runner image provides, checked by a gate.

## The repository during the move

- **Default:** the native code lives under `native/` (`native/core`, `native/ui`, `native/stilus`, `native/gesso`, `native/albumen`, and `native/tests`) beside today's `src/`, which holds the imported C# apps. Neither tree imports the other. When an app's native version ships its first release, its C# tree is removed in that release's section, and when the last one goes, `native/` can move to `src/` in one commit.
- The C# apps become a behavior reference: read to learn what each feature did and to reuse their test cases as specifications, never extended. Their remaining .NET debt sections are superseded by the re-plan rather than finished.
- `Isotone.slnx` and the .NET gates stay only as long as C# code remains in the tree.

## What carries over unchanged

The TODO system and its tooling, the review dispatcher and every review rule, the campaign guard, the design system (`docs/design/`, its tokens and component specs, now implemented in C++), the design contract, the layout maps (`D01 T13`), the parity inventories and catalogs, the user guides, the release and distribution decisions (per-app installers, signing, `download.rizonesoft.com`, the update feeds), and the licensing (GPL-3.0, the trademarks, the DCO).

## The order of work

1. **The native spine:** the toolchain, presets, vcpkg baseline, the gates, CI for x64 and ARM64, the test harness with WARP goldens and UI Automation driving, and the dependency register. Nothing user-visible.
2. **The de-risk sections, before anything is built on them:** a window with the Isotone title bar and a menu bar; a text box that takes IME input; a screen reader reading the controls; a docked panel that floats and redocks; and a GPU canvas that pans at 120 Hz with a pen stroke within one frame. Each ends in a driven proof. If one fails its bar, the spec is revised before more is built on it.
3. **Isotone UI's controls and docking**, then **Stilus native** to the behavior of today's Stilus and its 0.1.0 scope, with its layout map; its C# tree retires at that release.
4. **Gesso native**, then **Albumen**, the same way, each followed by its parity phases as the plan already orders them.

## Risks and how each is held

| Risk | How it is held |
| ---- | -------------- |
| Our own toolkit takes longer than a framework would | The de-risk sections prove the hardest pieces first; each control is a section with a checkpoint, so progress is measured, not hoped for |
| Accessibility and IME gaps | Both are de-risk sections with driven proofs (a screen reader session and an IME session), and the UI Automation tree is also the test driver, so gaps show as failing tests |
| Memory-safety crashes losing work | Sanitizer CI, a fuzz target per reader, autosave with a restore test, and atomic writes everywhere |
| Slower iteration in C++ | Small libraries, precompiled headers, Ninja, and unit tests that run without a window |
| A library that does not fit the size budget | The budget is a recorded default; exceeding it needs a decision entry, not a quiet increase |

## Open questions for the operator

1. **The rewrite order.** Default: Stilus first, as the plan orders it today. Alternative: Gesso first, since Photoshop-quality raster editing is where the native engine matters most.
2. **ARM64 from day one.** Default: yes, built and tested on CI from the spine onward. Alternative: x64 only until the first release, which saves CI time but risks a late port.
3. **The size budget.** Default: 30 MB per app's publish folder before optional content. A different number, or none, is the operator's call.
4. **Where the native code lives.** Default: `native/` during the move. Alternative: new folders directly under `src/` beside the C# trees.
