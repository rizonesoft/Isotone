# Shared Standards

Cross-cutting standards for every app in the Isotone Graphics Suite (Stilus, Gesso, Albumen, and the three planned apps Tinctura, Capio, and Folium) and for the shared libraries `isotone::core` and `isotone::ui`. App files ([`stilus.md`](stilus.md), [`gesso.md`](gesso.md), [`albumen.md`](albumen.md)) add to this file and never contradict it. [`AGENTS.md`](../AGENTS.md) holds the binding decisions; this file spells them out. How the C++ itself is written (the language, ownership, errors, threading, calling Windows, untrusted input, SIMD, suppressions, testing, and libraries) is [`cpp.md`](cpp.md); the architecture every rule here follows is `docs/specs/2026-10-22-native-stack-design.md`.

## The stack

| Concern | Choice | Notes |
| ------- | ------ | ----- |
| Language | C++23, compiled by the pinned MSVC toolset | One standard switch, set in `native/cmake/IsotoneTargets.cmake` and held by `scripts/native-std-check.py`; see [`cpp.md`](cpp.md) |
| Build | CMake with Ninja, the presets in `native/CMakePresets.json` | Every build runs inside the toolchain `native/toolchain.json` pins, entered by `scripts/dev-env.ps1`; x64 and ARM64 from the first commit |
| Runtime | The static C runtime (`/MT`) | No redistributable is installed with an app, and every imported DLL is a Windows system DLL (`native/system-dlls.txt`, `scripts/native-artifact-gate.py`) |
| UI | `isotone::ui`, our own toolkit on Win32, Direct2D, DirectWrite, Direct3D 11, and DirectComposition | **No third-party UI framework.** A control, a theme engine, or a docking library from outside is a defect |
| App structure | Documents and commands in the app's core library, surfaces in `isotone::ui` elements | One composition root per app; every command is registered once in the command registry of `isotone::core` |
| Logging | The structured log of `isotone::core` | Configured once per app; one line per action that changes a document or a setting |
| Rendering | Direct2D and DirectWrite for the interface and vector content; the shared pixel engine for raster content; Direct3D 11 for the GPU paths | A rendering library joins only for a measured need Direct2D cannot meet, through the dependency register |
| Packages | vcpkg in manifest mode, one committed baseline, static triplets | Every library enters through the register `docs/dev/native-libraries.md` |
| Tests | GoogleTest through CTest, Google Benchmark, libFuzzer | See [`testing.md`](testing.md) |
| Settings and JSON | Atomic JSON settings through `isotone::core` | The JSON library is nlohmann/json (`D01 T27 §2`, `docs/dev/native-libraries.md`), included only inside `isotone::core` |

**A dependency is a decision.** A library outside this table is added by a section that records why, registers it in `docs/dev/native-libraries.md` in the same commit as the code that first uses it, and checks its license against GPL-3.0: permissive (MIT, BSD, Apache-2.0) and LGPL are compatible; a license that forbids redistribution, needs a paid key, or restricts field of use is not. `scripts/native-deps-lint.py` keeps the register and the installed ports in step.

## Where code lives

```
native/
  core/      isotone::core, the shared non-UI library
  ui/        isotone::ui, the shared UI toolkit
  stilus/  gesso/  albumen/      one folder per app: its core library and its executable
  tests/     the GoogleTest suites, fixtures, and fuzz corpora, one folder per library or app
```

- An app's logic (its document model, commands, tools, engines, and format readers and writers) lives in that app's core library, which never includes a window header and is tested without a window. The app's executable is a thin shell over it and `isotone::ui`.
- **`isotone::core` and `isotone::ui` are shared from the start** (operator answer 2026-10-22, recorded in the spec): they are static libraries, each app's executable links its own copy, and no app installs, loads, or requires another app or a common runtime. Within them the suite rule holds piece by piece: a service or a control is added when the first app needs it, never speculatively, and the shared engines the plan names (the pixel engine, color management, the pixel engine extensions, the develop engine, the AI core) are shared by recorded operator exception.
- Anything else moves into a shared library only when two apps need it now. One app's need stays in that app with a comment naming the day it would move. A second copy of a behavior in a second app is a defect; so is a shared type only one app consumes outside those exceptions.
- An app never links another app's code, and never assumes another app is installed at run time.

## C++ style

[`cpp.md`](cpp.md) is the rule; `native/.clang-format` and `native/.clang-tidy` are its enforced form, and both start at zero findings. What every file also follows:

- Namespaces follow the folders: `isotone::core`, `isotone::ui`, `isotone::stilus`, `isotone::gesso`, `isotone::albumen`. Types and enumerators are `PascalCase` (`Bgra8`, `PremultiplyKernel::Avx2`); functions, variables, and namespaces are `snake_case` (`build_id()`, `best_supported_kernel()`); a named constant at namespace scope is `kPascalCase` (`kTilePixels`); macros (kept to the few the build needs) are `ISOTONE_UPPER_CASE`. This is the convention the code under `native/` already follows. A header is `snake_case.h` beside or under `include/isotone/<library>/`, with `#pragma once`.
- Text inside the program is UTF-8 (`/utf-8`, `std::string` and `std::string_view`); it becomes UTF-16 only at a Windows call, converted at that call.
- Numbers and dates written to a file, a log field, or a comparison are formatted independently of the user's locale (`std::format` with no locale, `std::to_chars`); text shown to a user is formatted for the user's locale through the localization services of `isotone::core`.
- No magic numbers: a threshold, size, or duration is a named constant or a setting; a value the interface shows is a design token (`design-contract.md`).
- Every public declaration of `isotone::core`, `isotone::ui`, and each app's core library carries a comment saying what it promises: its preconditions, what it returns or throws, and which thread may call it.

## Commands and state

- **Every command is registered once**, in the command registry of `isotone::core`, with its id, label, shortcut, and enabled state. Menus, shortcuts, the command search, tool buttons, and the layout maps all read that one registration, so a label, a shortcut, and an enabled state never disagree between two surfaces.
- A command that cannot run is disabled through its enabled state, with the reason available to its tooltip; it never runs and silently does nothing.
- A surface holds view state only (what is expanded, where the scroll is, which tab is in front). Anything a test would want to assert (a document's content, a selection, a setting, a computed value the user trusts) lives in the app's core library and is computed in exactly one place.
- Objects receive what they use through their constructors. There is no global service locator and no mutable singleton; process-wide services (settings, the log, the theme, the icon catalog) are created once in the app's composition root and passed down.

| Lifetime | Use for |
| -------- | ------- |
| The process | Settings, the log, the theme and token tables, the icon catalog, the task system |
| One open document | Its history, its selection, its tool state, its background tasks (cancelled before it closes) |
| One operation | Parsers, exporters, codecs, and a dialog's model |

## Logging

- One structured log per app, configured once through `isotone::core`. Files go to `%LOCALAPPDATA%\Rizonesoft\<App>\logs\<app>-<date>.log`, rolled daily, 7 files kept, 10 MB per file. A Debug build also writes to the debugger output.
- Never under `artifacts/` or `build/`: those are build output, and an installed app has neither.
- Structured fields, never text assembled by hand: an event has a message template and named values (`Saved {path} in {elapsed_ms} ms`), so a log can be searched by field.
- **One Information line per user action that changes a document or a setting**, naming the action and its target. This is the audit trail the adjacency contract calls `audit`.

| Level | Use for |
| ----- | ------- |
| Verbose | Inner loops, per-frame detail (off by default) |
| Debug | Developer diagnostics |
| Information | User actions and lifecycle: opened, saved, exported, setting changed |
| Warning | Recovered problems: a skipped file, a fallback taken |
| Error | A failed action the app survived |
| Fatal | The app is going down |

## Errors

The mechanics (exception types per module, converting an `HRESULT` at the call site, nothing thrown across a callback boundary) are in [`cpp.md`](cpp.md), "Errors". What every app adds:

- Expected failures (a file that will not parse, a refused write, a device that was lost) are part of the design, not surprises: the operation ends, the document is left as it was, and the user sees a message naming the action, the file, and what it needed.
- Nothing is swallowed. A failure is handled where something can be done about it, or it reaches the top of the action, is logged, and is shown.
- A crash loses nothing the user had: recovery never depends on code running in the crashing process (the spec's "Document safety" and "Crash diagnostics"). Dumps are collected out of process, encrypted, kept on the machine, and sent only when the user chooses to.

## Documents and user data

The contract is the spec's "Document safety": seven save invariants, the file identity contract, encrypted secondary copies, checkpoints, retirement, and recovery, each with named proofs. Its exact save sequence is designed and reviewed in the document safety foundation section. What every section that touches a user's file owes:

- **Every edit is an undo step.** An edit nobody can roll back is the most expensive defect class a creative tool has.
- **Saves are atomic and never weaken the file:** the new data is written beside the target under the target's own protection, made durable, and only then given the target's name; killing the process or cutting power at any instant leaves a complete old or new version at that name.
- Checkpoints go to the app's recovery folder, never over the user's file. Recovery offers what it found and deletes nothing without asking.
- A read-only file, a locked folder, or a full disk is refused with a message naming the file and the reason; the document stays open and dirty.
- Albumen never writes an original image unless the user opts in; a verified backup is taken by default. See [`albumen.md`](albumen.md).
- Settings live in `%LOCALAPPDATA%\Rizonesoft\<App>\settings\settings.json` (the `settings` folder beside the executable in portable mode), written atomically and read back through the `isotone::core` settings store. Every setting has a default, a consumer, and a log line when it changes.

## Performance

- Name the budget: a feature states the document size it must handle (a 10,000-node path set, a 100-megapixel image, a 50,000-photo library) and the time it must meet, measured on the reference machine (`docs/dev/reference-machine.md`) with the benchmark harness (`D00 T04 §2`), against the competitor where the section's Exceed paragraph says so.
- Anything slower than a second shows progress and can be cancelled; every background task is cancellable and holds its document weakly.
- No allocation per frame on a render or input path: buffers are pooled or reused, and a hot loop builds no container and takes no lock it can avoid.
- Every resource has one owning type that releases it (RAII); a GPU resource belongs to a renderer that can rebuild it after device loss.

## Commits

Conventional Commits: `<type>(<scope>): <description>`, imperative, types `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `chore`, with `!` for a breaking change. The scope is the app (`stilus`, `gesso`, `albumen`), a shared library (`core`, `ui`), or `workspace`: each app's changelog and next version are generated from the commits carrying its scope ([`release.md`](release.md)). TODO sections name their own commit message in their `Commit:` item; use it. One section is one logical change.

## The design contract

Every user-facing surface answers to the UI standard in [`ui.md`](ui.md), the binding summary of the Isotone Interface design system in [`docs/design/`](../docs/design/README.md): four brightness themes, the Highlight color for state and the app accent for identity only, type, spacing and density, focus, icons, window anatomy, accessibility, and the native toolkit mapping. `docs/design/tokens.json` is the source of every value, and the token tables of `isotone::ui` are generated from it; no surface hardcodes a color, size, or spacing value a token names. How the code is held to the design is [`design-contract.md`](design-contract.md). The captures under `docs/captures/<app>/` are a before record of the removed prototypes, never a fidelity source.

Two behavior rules every surface also follows:

- Confirmations name what, how many, and how large; refusals name the action and what it needed.
- Animated feedback respects the Windows "animation effects" setting.
