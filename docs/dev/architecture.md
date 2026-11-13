# Architecture

How the Isotone Graphics Suite is put together: the applications, the shared libraries, the rules that keep them independent, and where the code is going. The contract is the approved spec, [`docs/specs/2026-10-22-native-stack-design.md`](../specs/2026-10-22-native-stack-design.md); this page is its short form. The build itself is described in [build.md](build.md) and versioning in [versioning.md](versioning.md). The live plan is [`todo/`](../../todo/TODO-00-INDEX.md).

## The application family

Isotone is a family of standalone creative applications for Windows 11, written in C++23 with our own interface toolkit on Win32, Direct2D, DirectWrite, and Direct3D. They are developed together in one repository and distributed separately.

| App | Kind | Role | Focus | Formats it owns |
| --- | ---- | ---- | ----- | --------------- |
| **Stilus** | Vector editor (Illustrator alternative) | Structure and design | Precision illustration, typography, logos, scalable graphics | `.svg` first; PDF and raster export; Illustrator and CorelDRAW files by its parity plan |
| **Gesso** | Raster editor (Photoshop alternative) | Creation and manipulation | Painting, retouching, layer composition, pixel editing | `.png`, `.jpg`, `.tiff`, a native layered format, `.psd` and `.xcf` by its parity plan |
| **Albumen** | Digital darkroom, photo manager, and fast image viewer (Lightroom, ACDSee, and IrfanView alternative) | Development and organization | RAW processing, non-destructive editing, batch work, the photo library, the default viewer | Camera RAW and DNG in; JPEG, TIFF, PNG out |
| **Tinctura**, **Capio**, **Folium** | Color studio; screenshots and screen recording; page layout | Added 2026-10-23 | Planned after the first suite release | Set by their plans |

Albumen is the bridge from the camera to Gesso: "Edit in Gesso" hands a rendered image to Gesso when Gesso is installed, and refuses by name when it is not.

## Develop together, distribute separately

- **One repository, one native tree** (`native/`, one CMake build with its presets), one set of gates, one plan.
- **Each app ships alone:** its own installer, its own install folder, its own copy of every shared library (they are static libraries linked into its executable), its own version tag (`stilus-v*`, `gesso-v*`, `albumen-v*`), its own changelog, its own user guide. A suite bundle (`isotone-v*`) packages a set of app versions without changing any of them.
- **No runtime dependency between apps.** An app may *offer* a hand-off to another (Albumen's "Edit in Gesso"), but it must work, and say so plainly, when the other app is absent. An update to Gesso can never break an installed Stilus, because nothing is shared on disk: no common runtime, no shared DLL, and no redistributable (the static C runtime, and only Windows system DLLs imported).

## Layout

```
native/
  toolchain.json  CMakePresets.json  vcpkg.json   the toolchain pin, the presets, the package manifest
  cmake/          the shared CMake helpers every target goes through
  core/           isotone::core, the shared non-UI library
  ui/             isotone::ui, the shared UI toolkit (planned: the native UI foundation creates it)
  stilus/  gesso/  albumen/          one folder per app: its core library and its executable (planned)
  tests/          the GoogleTest suites, fixtures, and fuzz corpora, one folder per library or app
  benchmarks/     the Google Benchmark harness
  triplets/       the vcpkg overlay triplets (x64 and ARM64, plain and AddressSanitizer)
```

Namespaces follow the folders: `isotone::core`, `isotone::ui`, `isotone::stilus`, `isotone::gesso`, `isotone::albumen`. Today the tree holds the toolchain, the build, the gates, and `isotone::core`'s build identity, premultiply kernels, error type, app-data folders, and structured log; the foundations, the toolkit, and the apps arrive with their own sections ([`native/README.md`](../../native/README.md)).

## The shared libraries

### isotone::core

The non-UI foundation every app links: app-data paths; settings stored as JSON with atomic writes and readback; structured logging (one line per action that changes a document or a setting); the command registry (every command once, with its id, label, shortcut, and enabled state, the single source the menus, shortcuts, command search, and layout maps read); undo and redo as recorded commands; document safety; the task system; atomic file I/O; localization services; crash diagnostics; and the update check.

Built so far (`D01 T27 §1`): `isotone::core::Error`, the module's exception, naming the failing call and its Win32 code; `resolve_app_folders` (`isotone/core/app_paths.h`), which puts an app's data under `%LOCALAPPDATA%\Rizonesoft\<App>\` (or beside the executable when a `portable` file sits there) with its `logs`, `settings`, and `recovery` folders, from sources a test can replace; and `isotone::core::Log` (`isotone/core/log.h`), one per app, created in the composition root and passed down: an event is a level, a message template, and named values, written as one JSON line to `logs\<app>-<date>.log`, a new part before a line would pass 10 MB, a new file at UTC midnight, the newest 7 files kept, a bounded memory buffer for a console, and the debugger output in a Debug build (`standards/shared.md`, "Logging"). A write never throws: a failed or torn write is counted in `failures()` and the next record starts on a fresh line.

### isotone::ui

Our own interface toolkit, drawn to [`docs/design/`](../design/README.md) with nothing in between and no third-party UI framework: Win32 windows with per-monitor DPI awareness and the title bar drawn by us; one Direct3D 11 device per process with Direct2D, DirectWrite, and DirectComposition; composition swap chains with partial redraw; device-loss recovery and the WARP fallback; the display color pipeline for SDR, Advanced Color, and HDR; a retained element tree with design tokens resolved at run time from tables generated from `docs/design/tokens.json`; every control in `docs/design/components/`; our own docking system; keyboard, pointer, pen, and touch input; one text editing model over the Text Services Framework; UI Automation providers for every element; shell dialogs, the clipboard, drag and drop, and printing; and localization.

### Sharing

`isotone::core` and `isotone::ui` are shared from the start (operator answer 2026-10-22: "Share fro mthe start, but the apps should be installable seperately also"), because every app consumes them by construction. Shared means shared source and build targets, never a shared install. The engines the plan names (the pixel engine, color management, the pixel engine extensions, the develop engine, and the AI core) are shared libraries by recorded operator exception. Everything else follows the suite rule piece by piece: a service or control is added when the first app needs it, and code moves into a shared library only when a second app needs it; until then it stays in its app with a note naming the day it would move. Stilus's vector engine and Albumen's catalog and RAW decoding belong to their apps until a second app needs them.

### What neither library does

Neither holds a document model, a tool, or a format specific to one app. The rendering pipelines differ on purpose: Stilus renders a vector scene through Direct2D geometry; Gesso composites tiled raster layers through the shared pixel engine with a Direct3D 11 GPU path; Albumen runs a floating-point develop pipeline.

## Inside an app

Every app has the same skeleton, set by [`standards/shared.md`](../../standards/shared.md) and [`standards/cpp.md`](../../standards/cpp.md):

- **Composition root:** process-wide services are created once and passed down through constructors; there is no service locator and no mutable singleton.
- **Commands:** every command is registered once in the command registry, and every surface reads that registration. Logic lives in the app's core library, which is tested without a window; a surface holds view state only.
- **Threads:** the UI thread (an OLE single-threaded apartment) owns every window and is the only thread that changes a document; a render thread owns the Direct3D context; engines read immutable snapshots; tasks are cancellable and hold their document weakly.
- **Logging:** the structured log of `isotone::core`, writing to `%LOCALAPPDATA%\Rizonesoft\<App>\logs\`, one line per action that changes a document or a setting.
- **Documents:** every edit is an undo step; saves meet the spec's seven invariants; checkpoints and recovery never overwrite the user's file; secondary copies of document data are encrypted.
- **Surfaces:** the suite's own controls drawn to their specs from design tokens; every icon-only control has a tooltip and a UI Automation name.

## Development goals

1. **Better, not a clone** (operator principle 2026-10-23): every feature first matches its competitor where users expect it, then beats it measurably, by its section's Exceed paragraph.
2. **Performance:** lightweight execution and fast startup; each feature names its budget on a large document and measures it on the reference machine.
3. **Interoperability:** "Edit in" hand-offs between the apps, over files, never over shared runtime state.
4. **Extensibility:** a plug-in surface where it earns its place, designed per app until a second app needs the same contract; scripting on Lua, linked statically.

## Decisions

Recorded decisions with their evidence and cost of change live in [decisions.md](decisions.md), one entry each.
