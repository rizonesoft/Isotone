# native

The C++23 half of the Isotone Graphics Suite: the shared libraries and the apps, built with one pinned toolchain from one committed package baseline (`docs/specs/2026-10-22-native-stack-design.md`).

## Layout

| Folder | Holds |
| ------ | ----- |
| `core/` | `isotone::core`, the shared non-UI library |
| `ui/` | `isotone::ui`, the shared UI toolkit |
| `stilus/`, `gesso/`, `albumen/` | The three apps, each its own executable that links its own copy of the libraries |
| `tests/` | The GoogleTest suites and fuzz corpora, under one folder per library or app |
| `triplets/` | The vcpkg overlay triplets `isotone-x64`, `isotone-arm64`, `isotone-x64-asan`, and `isotone-arm64-asan` |
| `cmake/` | The shared CMake helpers |

`tinctura/`, `capio/`, and `folium/` join them when their plans (`todo/07-tinctura/`, `todo/08-capio/`, `todo/09-folium/`) build them. Today the folder holds the toolchain pin, the vcpkg manifest and configuration, the triplets, the CMake build, and `isotone::core`'s build identity with its test; the apps and the UI toolkit arrive with their own sections.

## Entering the environment

Every build runs inside the pinned toolchain (`toolchain.json`), entered by `scripts/dev-env.ps1`; see `docs/dev/build.md`, "Native toolchain".

```powershell
pwsh scripts/dev-env.ps1 -Check -Arch x64        # the machine matches the pin (it also checks the triplets and the SDK)
. ./scripts/dev-env.ps1 -Arch arm64              # this session, inside the ARM64 cross environment
```

## Building

`CMakePresets.json` holds one configure, build, test, and workflow preset per configuration, each with the Ninja generator, `cl` as the compiler, and its folder under `artifacts/native/<preset>/`. The presets live here, so a block that runs them enters `native/` first:

```powershell
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; cmake --workflow --preset x64-debug'      # configure, build, test
pwsh scripts/dev-env.ps1 -Arch arm64 -Run 'Push-Location native; cmake --workflow --preset arm64-release' # configure, build (an ARM64 test runs on ARM64)
```

| Preset | Build type | Tests | Notes |
| ------ | ---------- | ----- | ----- |
| `x64-debug`, `arm64-debug` | Debug | yes | |
| `x64-release`, `arm64-release` | Release | yes | Full PDBs, `/OPT:REF`, `/OPT:ICF` |
| `x64-asan` | RelWithDebInfo | yes | `/fsanitize=address` and `/INCREMENTAL:NO` on every target, packages from the `isotone-x64-asan` triplet; Debug's `/RTC` refuses AddressSanitizer |
| `arm64-asan` | RelWithDebInfo | on ARM64 | The same for ARM64, packages from `isotone-arm64-asan`; built on x64, its tests run on ARM64 |
| `x64-analyze`, `arm64-analyze` | Debug, Release | no | MSVC `/analyze` on every first-party target (`ISOTONE_ANALYZE`), its warnings errors |
| `x64-dist`, `arm64-dist` | Release | no | What an app release builds from: `BUILD_TESTING` off and the vcpkg `test` feature unrequested, so GoogleTest is never installed or linked |

Every target goes through `isotone_add_library` or `isotone_add_test` (`cmake/IsotoneTargets.cmake`), which apply `/W4 /WX /permissive- /utf-8 /Zc:__cplusplus /Zc:preprocessor /EHsc /external:anglebrackets /external:W0`, control-flow guard on the compiler and the linker, and `/CETCOMPAT` on x64 (Microsoft Learn documents it for x64 only). C++23 is the one switch `/std:c++23preview`, never the `/std:c++latest` CMake emits by default. A test preset with no registered test fails (`noTestsAction: error`), a test that runs past 300 seconds fails (so a blocked process never stalls a run), configure fails on any executable under `tests/` that `isotone_add_test` did not register, and GoogleTest discovery runs at test time, so a build never runs an ARM64 test executable on x64. MSVC's `CL` and `_CL_` environment variables are refused at configure and on every build (`cmake/CheckCompilerEnvironment.cmake`), because cl would add them to every compile; `scripts/dev-env.ps1` clears them on entry.

The build id (`isotone::core::build_id()`) is the commit's first 12 hex digits, plus `-dirty` when tracked files differ from it. `cmake/WriteBuildId.cmake` rewrites it on every build, so a commit or an edit changes it without reconfiguring; a `git archive` source tree has no `.git`, and reads the commit from `BUILD_ID.txt`, which `export-subst` stamps.

Two checks prove what the flags cannot show on their own:

```powershell
python scripts/native-std-check.py artifacts/native/x64-debug                                     # every C++ compile carries exactly one standard switch, the pinned one
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'python scripts/native-pe-check.py artifacts/native/x64-release'  # every executable has control-flow guard, and CET on x64
```

## The AddressSanitizer lane

The whole CTest suite also runs under AddressSanitizer, its dependencies built by the sanitizer triplets. Support in the pinned toolset (MSVC 14.51):

| Architecture | Status | Source |
| ------------ | ------ | ------ |
| x64 | Supported | Microsoft Learn, "AddressSanitizer" (x86 and x64) |
| ARM64 | Supported, in preview | Microsoft Learn, Visual Studio 2026 release notes: 18.0 ("You can now use AddressSanitizer with MSVC to target ARM64. This feature is in preview") and 18.6 (the MSVC 14.51 release, "Improved ASan for ARM64 support with comprehensive library packaging"); the toolset ships `lib/arm64/clang_rt.asan_dynamic-aarch64.lib`, `clang_rt.asan_static_runtime_thunk-aarch64.lib`, and `bin/HostArm64/arm64/clang_rt.asan_dynamic-aarch64.dll`, and the `arm64-asan` probe build links |

Both lanes are required. The `x64-asan` test preset puts the toolset's runtime folder (`bin/Hostx64/x64`, which holds `clang_rt.asan_dynamic-x86_64.dll`) first on `PATH` and sets `ASAN_OPTIONS=halt_on_error=1:detect_leaks=0` (MSVC's AddressSanitizer has no leak detection). ARM64 executables cannot run on x64, so `arm64-asan` builds here and its tests run on ARM64, with `clang_rt.asan_dynamic-aarch64.dll` carried beside them (`D00 T05 §8`).

`tests/sanitizer/asan_probe_test.cpp` writes one byte past a heap allocation. The `asan_probe` test (label `asan-probe`) passes only when the sanitizer's `SUMMARY: AddressSanitizer: heap-buffer-overflow` line naming `asan_probe_test.cpp` appears in its output, so a build that is not instrumented runs to its end without the report and fails; it is built only in the sanitizer presets.

## Format and analysis

Every first-party source is formatted by `.clang-format` and checked by `.clang-tidy` (`native-tidy.ps1` removes the two MSVC switches clang-cl does not implement, so any other unknown switch still fails) (the seven families the spec names, every warning an error) and by MSVC code analysis; all three start at zero findings, with no baseline to grow into:

```powershell
pwsh scripts/native-format.ps1 -Check     # clang-format on every source the next commit would carry (-Fix rewrites them)
pwsh scripts/native-tidy.ps1              # clang-tidy over every translation unit in the x64 Debug compile database
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; cmake --preset x64-analyze; cmake --build --preset x64-analyze'   # /analyze
```

The tests take the same clang-tidy checks as the libraries. Under `/analyze`, test executables turn off C6326 alone, which GoogleTest's assertion macros raise in every test (`cmake/IsotoneTargets.cmake`).

## Imports and size

An app runs on a clean Windows install with nothing else installed, and its publish folder stays within the budget the operator set:

```powershell
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'python scripts/native-artifact-gate.py'                                    # every preset folder and its vcpkg root
python scripts/native-artifact-gate.py --publish artifacts/publish/<App>/<rid>                                        # one publish folder against its budget
```

- `system-dlls.txt` names every DLL an executable may import, each with its reason and the section that needs it, plus the `api-ms-win-*` and `ext-ms-win-*` API sets. A section that imports another system DLL adds it in its own commit. Delay-loaded imports are held to the same list.
- `sanitizer-dlls.txt` adds the toolset's AddressSanitizer runtime for the sanitizer presets only; the shipping policy never reads it.
- The vcpkg root of every preset holds no DLL, and every installed library names the static CRT (`LIBCMT` or `LIBCMTD`, never `MSVCRT`).
- `size-budget.json` sets 30 decimal megabytes per app, program databases and named optional content excluded, and the gate fails `budget-undocumented` unless `docs/dev/decisions.md` ("2026-10-23: The output size budget") states the same number.

The folders are the configure presets of `CMakePresets.json`, never a sweep of `artifacts/native/`, so a stale or probe folder never decides a result. `--policy shipping` or `--policy asan` limits a run to one policy's presets, `--require-built` fails a preset that was never built, and `--asan-coverage` proves every sanitized compile and package instrumented; a dumpbin result the gate cannot read (a malformed image, a format change) fails, an app-local copy of a system DLL fails, and a folder under `artifacts/publish/native/` that no budget names fails.

`pwsh scripts/check-all.ps1` runs every native stage after the .NET and Python gates (`.claude/skills/process-todo-section/gates.md` lists what each proves); `-SkipNative` leaves them out.

## Packages

vcpkg in manifest mode: `vcpkg.json` pins every port to one `builtin-baseline` (the registry commit `9eec002df1cd109f8f104cd966a763daf9751489`, release `2026.10.16`), and `vcpkg-configuration.json` adds the overlay triplets and no registry, so that baseline stays the only one. Every library links statically against the static CRT (`/MT`), built with the pinned MSVC toolset (each triplet sets `VCPKG_PLATFORM_TOOLSET_VERSION` to the pin's selector, which `dev-env.ps1 -Check` enforces). The `test` feature holds GoogleTest; an app build never requests it.

Each install writes its own root under `artifacts/vcpkg_installed/<preset or manual-triplet>/`, never inside `native/` and never shared, because a manifest install removes what another triplet or feature put in its root:

```powershell
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'vcpkg install --x-manifest-root=native --x-install-root=artifacts/vcpkg_installed/manual-isotone-x64 --triplet isotone-x64 --x-feature=test'
```

Every new library is added through the dependency register of `D00 T04 §1` in the same commit as the code that uses it ([`docs/dev/native-libraries.md`](../docs/dev/native-libraries.md), which that section writes).

## Binary caching

- **Locally:** vcpkg's default binary cache (`%LOCALAPPDATA%\vcpkg\archives`), with no setting: a second install of the same port, triplet, and toolchain restores in seconds instead of building.
- **In CI:** a `files` binary source, `VCPKG_BINARY_SOURCES=clear;files,<workspace>/build/vcpkg-cache,readwrite`, in a folder `actions/cache` restores and saves under the key `vcpkg-<runner.os>-<triplet>-<the builtin-baseline>-${{ hashFiles('native/vcpkg.json', 'native/vcpkg-configuration.json', 'native/triplets/**', 'native/toolchain.json') }}`. The key carries everything vcpkg hashes into a package's ABI that the repository controls, so a changed manifest, triplet, or toolchain pin opens a fresh cache instead of restoring the old one under a key GitHub will never overwrite. `D00 T05 §8` uses exactly this key.
