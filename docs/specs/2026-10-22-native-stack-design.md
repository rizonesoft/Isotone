# The native stack: C++20 with our own UI

**Status:** draft for the operator's review, revised 2026-10-22 after the operator's answers and an independent review (GPT-6.1 Sol at xhigh: 3 P1, 17 P2, and 1 P3, each answered below). Nothing in `todo/` changes on this spec's account until the operator approves it; the re-plan is filed from the approved version.

**Decision it serves:** the operator decided on 2026-10-22 that the suite moves from C# and WPF to C++20 with our own UI on Win32, Direct2D, DirectWrite, and Direct3D ("I feel that C++ and our own UI will get is much closer to Photoshop quality."), judged on "the most control and speed. + small output sizes and dependencies". The options, evidence, and cost are in `docs/dev/decisions.md` (2026-10-22: The native stack).

**Operator answers recorded here (2026-10-22):** Stilus is rewritten first; x64 and ARM64 are built and tested from day one; each app's publish folder has a 30 MB budget; the native code lives under `native/` beside `src/` during the move.

## How to read this spec

Everything marked **Default** is a justified default: the choice this spec makes so work can start, its reason, and its cost of changing. The operator can overturn any of them in review. **Open questions** at the end need the operator's call before the re-plan. Every goal is a number a named protocol measures; an impression is never evidence.

## Goals and how each is measured

### The reference environment

All performance numbers are measured on one recorded reference machine and display (**Default**: the development machine, its CPU, GPU, driver version, RAM, storage, Windows build, display resolution, scaling, and refresh rate written into `docs/dev/reference-machine.md` by the first benchmark section, and re-recorded when any of them changes), with the app's Release build, a fresh profile, and the fixtures named below.

### The goals

| Goal | Target at each app's first native release | Protocol |
| ---- | ----------------------------------------- | -------- |
| Cold start | Main window accepting input in under 500 ms at the median and under 800 ms at the maximum of 10 runs | Each run after a reboot and a 60 s idle (the cold condition: nothing of the app in the file cache), timed from the process creation time (`GetProcessTimes`) to the system time of the first presented frame after which a scripted keystroke is handled, both read in the same system-time units; 10 runs, median and maximum reported |
| Warm start | Under 250 ms at the median of 10 runs | The same, with the app run once beforehand |
| Interface frame cadence | At the display's refresh rate, no more than 1 missed vsync per 1,000 frames, and no single gap longer than two vsync intervals | 60 s each of panning, zooming, panel resizing, and window resizing on the fixture documents, with displayed-frame times taken from presentation statistics (`IDXGISwapChain::GetFrameStatistics` and PresentMon), not from renderer timings |
| Pen latency | 95 percent of stroke samples visible on the first vsync after the frame that includes them, none later than the second | Pointer events carry their `QueryPerformanceCounter` timestamp (`POINTER_INFO.PerformanceCount`); each presented frame records the newest sample it drew and its present id; presentation statistics give the vsync it was displayed on, in the same clock domain. Physical pen-to-photon latency is not claimed; a later section may add a hardware measurement |
| Output size | Each app's publish folder at or under 30 MB before optional content (operator answer) | `scripts/publish.ps1` reports the size and a gate fails over budget; exceeding it needs a decision entry, never a quiet increase |
| Dependencies | The executable imports only Windows system DLLs; every library is linked statically and registered | A gate reads the executable's import table (`dumpbin /dependents`) and the dependency register |
| Work lost to a crash | The saved file never; unsaved work at most the edits since the last checkpoint (see Document safety) | The crash tests in Document safety |

The fixture documents (a small, a typical, and a large document per app, the large one at the plan's documented limits) are committed with the first benchmark section.

## The toolchain

- **Language:** C++20 compiled by MSVC. The exact toolset version is pinned (below), not "whatever is installed". Modules are not used yet (**Default**: headers until MSVC, CMake, and clang-tidy handle modules together without workarounds; changing later is mechanical).
- **Build description:** CMake, with Ninja as the generator for scripts and CI and committed `CMakePresets.json` (Debug, Release, and the sanitizer configuration, for x64 and ARM64), which Visual Studio opens natively (**Default**; the alternative is the Visual Studio generator driving MSBuild from the same `CMakeLists.txt`, which changes the presets' generator, not the build description).
- **Pinning the toolchain:** Ninja cannot select a toolset by itself, so `scripts/dev-env.ps1` locates Visual Studio with `vswhere`, enters its developer environment for the pinned MSVC toolset (`-vcvars_ver`) and Windows SDK version and the target architecture, verifies `cl`'s reported version and the SDK, and refuses a mismatch; the presets use the external toolset strategy and every script and CI job runs inside that environment. CMake, Ninja, the LLVM tools (clang-tidy, clang-format), and the vcpkg tool are pinned to exact versions separately from the vcpkg ports baseline, each checked by a gate. The pinned toolset is one the CI runner image provides (Visual Studio Professional 2026, 18.11, with Windows SDK 10.0.26100 is installed on the development machine; the pin is chosen where both meet).
- **Runtime:** the static C runtime (`/MT`), so no Visual C++ redistributable is installed with an app.
- **Packages:** vcpkg in manifest mode with a committed baseline, using the static triplets for x64 and ARM64, plus a sanitizer triplet that builds dependencies with AddressSanitizer so the sanitizer configuration covers library code as well as ours.
- **Architectures:** x64 and ARM64 from day one (operator answer). ARM64 is cross-compiled on x64 for every build, and its tests run on an ARM64 Windows machine (a CI runner of that architecture, or a recorded local ARM64 machine if none is available), so cross-compiling is never mistaken for running.
- **Warnings and analysis:** `/W4 /WX /permissive-`, MSVC `/analyze` on CI, clang-tidy with a committed configuration, and clang-format checked by a gate, the C++ equivalents of today's warnings-as-errors and `dotnet format` gates.
- **Tests:** GoogleTest through CTest (**Default**: the most widely supported C++ test framework with CTest and Visual Studio; changing is mechanical per file).
- **Fuzzing:** every file reader has a fuzz target, built with libFuzzer. MSVC's `/fsanitize=fuzzer` is documented as experimental, so the first fuzzing section qualifies it against the pinned toolset and, if it falls short, builds the fuzz targets with clang-cl instead (a recorded decision either way). Each target keeps a committed seed corpus and every crashing input as a regression case under `native/tests/fuzz/<reader>/`; CI runs each target for a fixed budget (**Default**: 5 minutes per target per night) with `-rss_limit_mb` and `-timeout` limits, and the regression inputs on every build.

## The architecture

### Sharing, reconciled with the plan's decisions

The suite's rule is that shared code is built only when two apps need it. The plan already records operator exceptions built ahead of their second consumer (`todo/01-core/INDEX.md`): the pixel engine, color management, the AI core, the pixel engine extensions, and the develop engine. This spec keeps every one of them as a shared library, so the raster pixel engine and color management are shared from the start, not owned by Gesso as the first draft said.

Building a whole UI toolkit of our own is new, and its consumers are all three apps by construction: there is no version of this decision in which Stilus has its own toolkit and Gesso another. So this spec asks the operator to authorize `isotone::core` and `isotone::ui` as shared from the start (open question 1). Within them, the existing rule still holds piece by piece: a control or service is added when the first app needs it, never speculatively.

### Isotone Core (`isotone::core`)

The non-UI foundation every app links: app-data paths; settings stored as JSON with atomic writes and readback; structured logging (one line per action that changes a document or a setting); the command registry (every command once, with its id, label, shortcut, and enabled state, the single source the menus, shortcuts, command search, and layout maps read); undo and redo as recorded commands; document safety (below); the task system (below); atomic file I/O; localization services (below); crash diagnostics (below); and the update check.

### Isotone UI (`isotone::ui`)

Our own interface toolkit, drawn to `docs/design/` with nothing in between. It is the largest new piece of work, and each part a general-purpose framework would hand us has its own section with its own proof.

- **Windows and frames:** Win32 windows with per-monitor DPI awareness (v2) and layout in device-independent pixels rounded to physical pixels at every scale; the Isotone title bar drawn by us with the menu bar inside it (DWM frame extension, and hit testing that keeps Windows 11 snap layouts on the maximize button).
- **Rendering:** one Direct3D 11 device per process with Direct2D and DirectWrite over it, and DirectComposition: each window's interface is one visual with its own swap chain, and the document canvas is another visual with its own swap chain, so the two redraw independently (**Default**: Direct3D 11 for maturity and Direct2D interoperability; Direct3D 12 only where a measured engine need requires it).
- **Swap chains and partial redraw:** composition swap chains use `DXGI_SWAP_EFFECT_FLIP_SEQUENTIAL` (not `FLIP_DISCARD`, which does not support partial presentation) with `Present1` dirty and scroll rectangles. Because flip-model back buffers rotate, the renderer tracks each buffer's accumulated damage and redraws the union since that buffer was last presented. Tests alternate disjoint invalidations, scrolling, resizing, and occlusion and compare every presented frame with a full redraw.
- **Device loss:** every GPU resource is owned by a renderer that can rebuild it from CPU-side state. On device removal or reset (`DXGI_ERROR_DEVICE_REMOVED` or `DXGI_ERROR_DEVICE_RESET` from a present or a call), the renderer releases the device, recreates the device, the Direct2D and DirectComposition objects, the swap chains, and every resource, and redraws; documents live in CPU memory or the tile store, never only in video memory. If hardware initialization fails, the app runs on the WARP software device with a notice. Tests force device removal (the Direct3D debug layer's removal or `dxcap -forcetdr`) and start on WARP with the hardware adapter hidden, each proving the documents intact and the app usable.
- **Display color:** a shared display color pipeline, owned by `isotone::ui` for all three apps. When a monitor's Advanced Color is off, the window's swap chain is 8-bit and documents are converted from their profile to the monitor's ICC profile with LittleCMS. When Advanced Color is on (HDR or SDR wide color gamut), the swap chain is FP16 in scRGB (`DXGI_FORMAT_R16G16B16A16_FLOAT` with `DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709`), documents are converted to scRGB, and the interface is drawn at the user's SDR reference white level, because under Advanced Color Windows changes how ICC profiles apply (Microsoft's Advanced Color ICC profile guidance). The pipeline re-reads the monitor's color state when a window moves between monitors or the display configuration changes (`WM_DISPLAYCHANGE`, `WM_DPICHANGED`, `WM_WINDOWPOSCHANGED`, and the output's `IDXGIOutput6::GetDesc1`). Proofs: color patches measured through the pipeline against a known profile in SDR and in Advanced Color, and a window moved between an SDR and an Advanced Color monitor, re-converting without a wrong frame.
- **Element tree and theming:** a retained tree of elements with measure and arrange layout, invalidation, and dirty-rectangle redraw. Design tokens are resolved at run time from tables generated from `docs/design/tokens.json` (one per theme, Highlight, and density, plus the high-contrast mapping), so a style names a token key and never a value; switching theme, Highlight, or density, or Windows changing high contrast (`WM_SETTINGCHANGE`), reduced motion (`SPI_GETCLIENTAREAANIMATION`), or DPI, invalidates the styles that read the changed keys and redraws. This is the native equivalent of the design contract's `DynamicResource`, and layout rounding replaces WPF's: the design contract's exact values and 1 DIP tolerances carry over unchanged, and its WPF-named mechanisms are renamed to these equivalents in the re-plan. design-lint moves to the C++ sources.
- **Controls:** every component in `docs/design/components/` (buttons, inputs, number boxes, sliders, menus, context menus, tabs, lists and trees, the tool rail, the options bar, panels, dialogs, tooltips, toasts, the status bar), one set the apps share.
- **Docking:** our own docking system (panels, tab groups, columns, floating windows, and the saved workspace as JSON), with the layout maps' Panels part as its default.
- **Input:** keyboard focus and commands; pointer input through `WM_POINTER` for mouse, pen (pressure, tilt, barrel button), and touch; the wheel and precision touchpad.
- **Text:** one shared text editing model under every text box and the apps' type tools: grapheme-cluster-aware caret movement and deletion, bidirectional caret and selection, undo grouping, and font fallback through DirectWrite's system fallback; layout with DirectWrite. Input methods go through the Text Services Framework with a text store (`ITextStoreACP2`) that implements its lock protocol and reentrancy rules, composition start, update, commit, and cancel, focus changes during composition, and candidate-window placement at mixed DPI. Proofs: Chinese, Japanese, and Korean input sessions; Arabic and Hebrew caret and selection; combining sequences and emoji; and text on a transformed canvas.
- **Accessibility:** a UI Automation provider for every element, with the control patterns each control needs (Invoke, Toggle, Value, RangeValue, Selection and SelectionItem, ExpandCollapse, Scroll, Text, and Grid where they apply), the properties and the focus, selection, structure, and text events, fragment navigation, virtualized items for long lists, and a stated provider lifetime and threading rule (calls arrive on any thread and are answered from the UI thread's state). UI Automation tests read and invoke the tree, but because invoking through UI Automation bypasses the keyboard, pointer, hit testing, and IME paths, those paths have their own tests driven by `SendInput`, and named screen reader scenarios (Narrator, and NVDA) are run as driven checks with their transcripts recorded.
- **Desktop exchange:** shell file and folder dialogs (`IFileOpenDialog`, `IFileSaveDialog`, with each app's file types); the clipboard through OLE with delayed rendering, each app's formats (its own, plus PNG, SVG, and text as its sections define), and ownership released safely at exit; drag and drop through OLE (`RegisterDragDrop` after `OleInitialize`); and printing through Direct2D's print control (`ID2D1PrintControl`) with the Print Document Package API, covering printer capabilities, page settings, cancellation, and color handling. The existing per-app clipboard and printing sections keep their feature scope and are rewritten onto these contracts.
- **Localization:** translated resources per app, with plural and gender rules and locale-aware number, unit, and date formatting and parsing through the ICU that ships with Windows (`icu.dll`, a system component); right-to-left interface layout with mirroring; mnemonics and shortcuts that survive translation; and a pseudo-localization build (longer strings, accented characters, right-to-left) that the gates run. These foundations exist before controls and command labels become fixed interfaces.

### Threading and lifetimes

- **The UI thread** of each process is an OLE single-threaded apartment (`OleInitialize`). It owns every window, the element tree, Text Services Framework, the UI Automation providers' state, drag and drop, and the clipboard, and it is the only thread that changes a document: commands run there and are recorded for undo.
- **The GPU:** the Direct3D 11 immediate context is used from one thread at a time. A render thread owns it and does every draw and present; the UI thread hands it immutable render snapshots (the element tree's draw list and the document's visible tiles at a version), so a long engine job never blocks interface frames. Direct2D is created multithread-protected where the canvas and the interface share it.
- **Engines** read immutable document snapshots (copy-on-write tiles and geometry), so background work never sees a half-applied edit; results come back to the UI thread to be committed as commands.
- **Tasks** run on a thread pool in three priority classes: interactive (what the user is waiting on, bounded so a frame is never starved), background (previews, thumbnails, indexing), and idle. Every task is cancellable, and a document's tasks are cancelled before it closes.

### Document safety

The failure model: the process can die at any instruction (a crash, a hang the user ends, power loss), and no code is assumed to run after the failure. So recovery never depends on a crash handler.

- **Saving** writes a temporary file beside the target, flushes it to disk (`FlushFileBuffers`), and replaces the target atomically (`ReplaceFileW` or `MoveFileExW` with write-through), so an interrupted save leaves the previous file intact. A full disk or a write error fails the save with a message and leaves the previous file untouched.
- **Checkpoints:** each open document, untitled ones included, is checkpointed to the app's recovery folder with the same atomic write, alternating between two slots so a corrupted or interrupted checkpoint always leaves the previous good one; each checkpoint carries a checksum and the document's edit counter. **Default** cadence: the first checkpoint within 10 s of the first unsaved edit, then whenever there are unsaved edits and 60 s have passed or the user has been idle 5 s. So the most a crash loses is the edits since the last checkpoint: at most about 60 s of work, and under 10 s for a document edited only briefly.
- **Recovery** runs at the next start, independent of how the last process ended: it scans the recovery folder for checkpoints whose process is gone, validates each checksum, falls back to the other slot when one is bad, and offers each recovered document by name, untitled ones included. A disk-full checkpoint failure warns once and retries; it never deletes the last good checkpoint.
- **Proofs:** the process killed at random points during edits, saves, and checkpoints (`TerminateProcess` from a test driver), each run checking that the saved file is intact and the recovered document's contents equal its last checkpoint; a corrupted checkpoint slot; a full disk; and a kill before the first checkpoint.

### Crash diagnostics

Collecting a dump inside a crashing process can deadlock, so dumps are collected from outside it (**Default**: Windows Error Reporting local dumps, configured per executable by the installer to write minidumps into the app's own folder in the user's app data, keeping the newest 5). Dumps can contain document data, so they never leave the machine unless the user chooses to send one from the app's Help menu, which shows what is sent. Every build embeds its exact version and build id, and each release's symbol files (PDBs) are archived with that id and never shipped.

### The engines

Each engine is native. The pixel engine, color management, the pixel engine extensions, the develop engine, and the AI core are shared libraries by the existing operator exceptions; Stilus's vector engine (geometry, paths, and rendering through Direct2D geometry) and Albumen's catalog (SQLite) and RAW decoding (LibRaw) belong to their apps until a second app needs them.

The pixel engine's data contract carries over from its plan and is made explicit: documents store 8-bit and 16-bit integer or 32-bit float channels per the document's mode; processing runs in 32-bit float (and FP16 on the GPU only where a section measures the precision as sufficient); colors are stored with straight alpha and composited premultiplied; transfer functions follow the document's color profile, with linear-light processing where an operation requires it; extended-range values are kept in float documents and clamped only on conversion to integer modes; and the CPU, SIMD, and GPU paths agree within a stated tolerance (**Default**: within 1 code value at 8-bit and 1/4096 at float, per operation, checked by tests over fixed inputs). Tiles live in the scratch-backed tile store the plan already requires, with memory, video memory, and undo budgets set from the machine's resources; an allocation failure ends the operation with a message and leaves the document as it was.

### The apps

`stilus.exe`, `gesso.exe`, and `albumen.exe`: each a thin executable over the shared libraries and its engines, shipped on its own with its own installer, version, and update feed, as today. "Develop together, distribute separately" is unchanged.

## Dependencies and their upkeep

A library is a decision: the section that needs it adds it, records it in the dependency register (`docs/dev/native-libraries.md`) with its version, provenance, license and the URL of its license text, its advisory feed, the apps that link it, and its owning section, and it must be compatible with GPL-3.0. Linking is static, so a vulnerable library is fixed by rebuilding and releasing every app that links it: a scheduled job checks the register's versions against vulnerability advisories (the OSV database) and the vcpkg baseline, and a finding files a section to update, rebuild, and release the affected apps. Candidates the plan already points to, each confirmed with its license text by the section that adds it: LittleCMS 2, libpng, libjpeg-turbo, libwebp, zlib-ng, LibRaw, SQLite, spdlog, nlohmann/json, and GoogleTest. A rendering library such as Skia or Blend2D joins only for a measured need Direct2D cannot meet. SkiaSharp and AvalonDock leave with the C# code, and the AvalonDock exception in `LICENSE-EXCEPTION.md` is retired by the section that removes the last C# app.

## Testing and the gates

The proof standard in `todo/README.md` carries over, re-expressed for C++:

- **Builds clean:** Debug and Release, x64 and ARM64, warnings as errors, `/analyze` and clang-tidy clean.
- **Static analysis clean:** clang-format and clang-tidy report nothing new on the touched files.
- **Unit test:** a GoogleTest case, cited by name.
- **Driven run with evidence:** UI Automation for reading and invoking the interface, `SendInput` for the keyboard, pointer, and IME paths, a log line, a settings readback, or a saved file inspected.
- **Format fidelity proof:** fixtures opened, saved, reopened, and compared, plus each reader's fuzz target and its regression corpus.
- **Goldens:** surfaces rendered offscreen on the WARP software device in a pinned reference environment: the Windows build, the font files the design uses (Segoe UI Variable and Cascadia Mono are Windows system fonts we may not redistribute, so their file hashes are recorded and a golden run refuses a machine whose fonts differ), fixed DirectWrite rendering parameters (antialiasing mode, gamma, contrast), a fixed DPI per golden, and a fixed locale. The first goldens section proves repeatability by rendering every golden twice, on two machines meeting the pinned environment, within the design contract's tolerance. Offscreen goldens prove drawing, not presentation, so presentation, composition, docking windows, and input keep their own driven tests on real hardware.

`scripts/check-all.ps1` runs the environment check, the CMake configure and build, CTest, the format and analysis gates, the size and import gates, and every TODO gate. CI builds x64 and ARM64 on Windows runners inside `scripts/dev-env.ps1`'s pinned environment.

## The repository during the move

- The native code lives under `native/` (`native/core`, `native/ui`, `native/stilus`, `native/gesso`, `native/albumen`, and `native/tests`) beside today's `src/`, which holds the imported C# apps (operator answer). Neither tree imports the other. When an app's native version ships its first release, its C# tree is removed in that release's section; when the last one goes, `native/` may move to `src/` in one commit.
- The C# apps become a behavior reference: read to learn what each feature did and to reuse their test cases as specifications, never extended.
- `Isotone.slnx` and the .NET gates stay only as long as C# code remains in the tree.

## The re-plan, and what it must preserve

The re-plan is filed from the approved spec, and it starts with a supersession map (`todo/supersession-2026-10.md`, **Default** name): every existing section listed once as kept, rewritten onto the native stack (with its successor's ref), or superseded (with the reason and the successor that takes over its acceptance requirements). It preserves every stamp and record already made (stamped sections stay as they shipped; their successors are new sections), keeps every parity catalog reference resolving, and names each recorded decision that needs a replacement before either C# tree is deleted. Two already known:

- `D00 T04 §1`'s native-code policy is written for a C#-first suite (native code only by rule). It becomes the dependency register and the C++ standards for a native suite, keeping its register columns, its advisory requirement, and its rules for calling the operating system.
- The automation plan (`D01 T10`) builds C# scripting on Roslyn, which a native suite with only system dependencies cannot host. The scripting language is open question 2.

## What carries over unchanged

The TODO system and its tooling, the review dispatcher and every review rule, the campaign guard, the design system (`docs/design/` and its tokens and specs, implemented in C++), the design contract's values and tolerances, the layout maps (`D01 T13`, with the review findings of 2026-10-22 answered in the re-plan), the parity inventories and catalogs, the user guides, the release and distribution decisions (per-app installers, signing, `download.rizonesoft.com`, the update feeds), and the licensing (GPL-3.0, the trademarks, and the DCO).

## The order of work

1. **The native spine:** `scripts/dev-env.ps1` and the pinned toolchain, presets, the vcpkg baseline and triplets, the gates (build, analysis, format, size, imports, TODO), CI for x64 and ARM64 with ARM64 test execution, the test harness, and the dependency register. Nothing user-visible.
2. **The foundations, before anything is built on them,** each ending in its driven proof, and each able to send the spec back for revision if it fails its bar: document safety; the task system and threading; localization services; a window with the Isotone title bar and menu bar on the swap chain and partial-redraw contract; device-loss recovery and the WARP fallback; the display color pipeline in SDR and Advanced Color; the text editing model with TSF; UI Automation with the screen reader scenarios; a docked panel that floats and redocks; a GPU canvas meeting the frame cadence and pen latency goals; runtime theming; the goldens environment with its repeatability proof; and crash diagnostics.
3. **Isotone UI's controls and docking**, then **Stilus native** to the behavior of today's Stilus and its 0.1.0 scope, with its layout map; the C# Stilus tree retires at that release (operator answer: Stilus first).
4. **Gesso native**, then **Albumen**, the same way, each followed by its parity phases in the order the plan already gives them.

## Risks and how each is held

| Risk | How it is held |
| ---- | -------------- |
| Our own toolkit takes longer than a framework would | The foundations prove the hardest pieces first, and each control is a section with a checkpoint, so progress is measured |
| Accessibility, IME, or localization gaps | Each is a foundation with driven proofs (screen reader transcripts, IME sessions, pseudo-localization and right-to-left builds) before controls are built on it |
| Memory-safety crashes losing work | The document safety failure model and its kill tests, sanitizer builds that include dependencies, and fuzzing with retained regression inputs |
| GPU driver faults | Device-loss recovery and the WARP fallback, each forced in tests |
| Wrong colors on wide-gamut or HDR displays | The display color pipeline's measured proofs in SDR and Advanced Color |
| Slower iteration in C++ | Small libraries, precompiled headers, Ninja, and unit tests that run without a window |
| A library that does not fit the 30 MB budget | The budget gate; exceeding it needs a decision entry |
| A vulnerable statically linked library | The advisory job and the rebuild-and-release section it files |

## Open questions for the operator

1. **Shared from the start.** Authorize `isotone::core` and `isotone::ui` as shared libraries from the start, as an exception to "shared only when two apps need it" (their consumers are all three apps by construction), with controls and services still added only when the first app needs each. **Default:** yes.
2. **The scripting language.** The automation plan's C# scripting cannot run in a native suite without shipping the .NET runtime. **Default:** embed Lua (MIT, small, built for embedding, statically linked); alternatives are JavaScript through QuickJS (MIT) or Python through an embedded CPython (larger, and harder to keep inside the size budget).
