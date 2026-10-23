# C++ standard

How the suite's C++ is written, how it calls Windows, and how it treats untrusted input. Every rule here is held by a gate where one can hold it (`pwsh scripts/check-all.ps1` runs them all; `.claude/skills/process-todo-section/gates.md` names each stage), and by review where none can. The spec this follows is `docs/specs/2026-10-22-native-stack-design.md`; each heading names the section it follows.

## Language

Follows the spec's "The toolchain".

- C++23 by the one switch `D00 T05 §3` sets (`/std:c++23preview`, moving to `/std:c++23` when the pinned MSVC ships it), never `/std:c++latest`; `scripts/native-std-check.py` holds every compile to it.
- Headers and source files, no C++20 modules: the toolchain's module support is uneven across MSVC, clang-tidy, and clang-format, which all must read the same code.
- `/permissive-`, `/Zc:__cplusplus`, `/Zc:preprocessor`, `/utf-8`; no compiler extension outside what the Windows SDK headers themselves need.
- Every target is added through `isotone_add_library`, `isotone_add_test`, or `isotone_add_sanitizer_probe` (`native/cmake/IsotoneTargets.cmake`), so it takes the suite's flags; `/W4 /WX` makes every warning an error.

## Ownership and lifetimes

Follows the spec's "Threading and lifetimes".

- RAII for every resource: memory, handles, locks, COM interfaces, GDI and Direct3D objects. A resource without an owning type gets one before it is used twice.
- Value types and `std::unique_ptr` by default; `std::shared_ptr` only where ownership is genuinely shared and the design says why; `Microsoft::WRL::ComPtr` for every COM interface.
- No owning raw pointer, and no `new` or `delete` outside a factory function that returns an owning type. A raw pointer or reference is a non-owning borrow whose lifetime the caller guarantees.
- A background task holds its document weakly and carries the document's identity and edit version; its result is committed on the UI thread only if the document is still open at that version.

## Errors

Follows the spec's "Document safety" and "Crash diagnostics".

- Exceptions within a module; each module has its own error type deriving from `std::exception`, carrying what failed and why.
- An `HRESULT` or Win32 error is converted at the call site into the module's error type, naming the failing call (`CreateFileW`, `ID3D11Device::CreateTexture2D`) and the error code; nothing is passed up as a bare code.
- Nothing is thrown across a COM, Win32, or C callback boundary: such a callback catches everything and returns an error code.
- Every failure that touches a document is logged with the document's identity and the failing step, and every failure the user can see names the action and what it needed.

## Threading

Follows the spec's "Threading and lifetimes".

- The UI thread of each process is an OLE single-threaded apartment (`OleInitialize`); it owns every window, the element tree, Text Services Framework, the UI Automation providers' state, drag and drop, and the clipboard, and it is the only thread that changes a document.
- The render thread owns the Direct3D 11 immediate context and does every draw and present; the UI thread hands it immutable snapshots.
- Engines read immutable, copy-on-write snapshots and never see a half-applied edit; every task is cancellable, and a document's tasks are cancelled before it closes.

## Calling Windows

Follows the spec's "The architecture" and "Dependencies and their upkeep".

- Windows SDK headers only; no undocumented API, and no API reached through an undocumented ordinal or structure.
- Each process calls `SetDefaultDllDirectories(LOAD_LIBRARY_SEARCH_SYSTEM32)` before it loads anything at run time, so no DLL is ever found in the current directory or on `PATH`.
- **Loading a module at run time.** A first-party `LoadLibraryW`, `LoadLibraryExW` (and their `A` forms), or `LoadPackagedLibrary` names its module as a string literal, and that module is either a Windows system DLL in `native/system-dlls.txt` or a module the register (`docs/dev/native-libraries.md`, Runtime module) lists; a system DLL loads with `LoadLibraryW` or with `LoadLibraryExW` and `LOAD_LIBRARY_SEARCH_SYSTEM32`, and a registered module only with `LoadLibraryExW` and `LOAD_LIBRARY_SEARCH_APPLICATION_DIR` (after `SetDefaultDllDirectories(LOAD_LIBRARY_SEARCH_SYSTEM32)`, a plain `LoadLibraryW` never searches the app's folder), so each loads from System32 or the app's own folder. `scripts/native-deps-lint.py` refuses a call it cannot resolve to one of those (`loadlibrary-unresolved`), because the import gate (`D00 T05 §6`) sees static and delay-loaded imports only.
- COM objects are created through `CoCreateInstance` (or `CoCreateInstanceEx`) with an explicit class context, never `CLSCTX_ALL`.
- Every DLL an executable imports, delay-loaded ones included, is a Windows system DLL (`native/system-dlls.txt`); `scripts/native-artifact-gate.py` holds every build to it.

## Untrusted input

Follows the spec's "Document safety" and "The toolchain" (Fuzzing).

Parsing a file the user opens is the suite's largest attack surface: every reader treats every byte as hostile.

- A reader parses through bounds-checked spans and a reader cursor that refuses a read past the end; no reader indexes a raw buffer.
- Every size and count read from the input is checked against the input that remains and against a limit the reader states, before anything is allocated from it.
- Size arithmetic is checked (an overflowing multiplication or addition is an error, not a wrap).
- Every reader has a fuzz target and a regression corpus (`D00 T05 §9`, under `native/tests/fuzz/<reader>/`), and its tests run in the AddressSanitizer lane (`D00 T05 §5`).

## SIMD and performance

Follows the spec's "Goals and how each is measured" and "The engines".

- Every SIMD kernel has a scalar reference it is tested against: exact agreement for integer kernels, the spec's stated tolerance for floating point.
- x64 kernels use SSE4.1 and AVX2 with runtime dispatch on the CPU's features; ARM64 kernels use NEON.
- An optimization lands with a benchmark record (`D00 T04 §2`, `docs/benchmarks/`) measured on the reference machine, never on an impression.

## Formatting and analysis

Follows the spec's "The toolchain" (Warnings and analysis).

- `native/.clang-format` formats every source (`scripts/native-format.ps1 -Check`), and `native/.clang-tidy` and MSVC `/analyze` hold every translation unit at zero findings (`D00 T05 §4`): there is no baseline to grow into.
- **Suppressions.** A finding is fixed, not suppressed, unless the analyzer is wrong about this code; then the suppression is as narrow as the tools allow and carries its reason on the same line:
  - clang-tidy: `// NOLINT(<one check>): <reason>` or `// NOLINTNEXTLINE(<one check>): <reason>`, naming exactly one check. A bare `NOLINT`, a `NOLINT` naming several checks or `*`, and a `NOLINTBEGIN` and `NOLINTEND` block are refused.
  - MSVC: `#pragma warning(suppress: <number>) // <reason>` on the line before the statement. `#pragma warning(disable: ...)` in a source file is refused.
  - A target-wide exception (a warning off for a whole target, an extra argument to a tool) lives only in `native/cmake/` or a gate script, marked with a `WORKAROUND: <reason>` comment directly above it.
  - `scripts/native-deps-lint.py` refuses each of these as `suppression-unreasoned`.

## Testing

Follows the spec's "Testing and the gates".

- GoogleTest cases are named `Suite.Case` in the words of the behavior they prove (`BuildInfo.BuildIdShape`), registered through `isotone_add_test`, which a configure-time guard requires.
- Tests run headless: no window, no message box, no dialog; every test preset fails a test after 300 seconds.
- A section proves its work by the proof standard in `todo/README.md` re-expressed for C++ (`D00 T05 §10`), quoting each gate's output.

## Libraries

Follows the spec's "Dependencies and their upkeep".

- A library enters only through the register, `docs/dev/native-libraries.md`, in the same commit as the code that first uses it, with a row for every port it pulls in, transitive ones included.
- Linked statically against the static CRT, from the vcpkg baseline, built by the pinned toolset through the suite's triplets.
- Its license is GPL-3.0 compatible (the allowed list is in `scripts/native-deps-lint.py`); its notices ship with every app that links it.
- A library built without a CRT directive (assembly only, or `/Zl`) says so in its row's CRT column with the reason, which is the only way the import gate accepts one.
- `scripts/native-deps-lint.py` keeps the register and the installed ports in step, and `scripts/check-native-advisories.py` (`D00 T04 §3`) checks every registered library against advisories daily.
