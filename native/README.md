# native

The C++23 half of the Isotone Graphics Suite: the shared libraries and the apps, built with one pinned toolchain from one committed package baseline (`docs/specs/2026-10-22-native-stack-design.md`).

## Layout

| Folder | Holds |
| ------ | ----- |
| `core/` | `isotone::core`, the shared non-UI library |
| `ui/` | `isotone::ui`, the shared UI toolkit |
| `stilus/`, `gesso/`, `albumen/` | The three apps, each its own executable that links its own copy of the libraries |
| `tests/` | The GoogleTest suites and fuzz corpora, under one folder per library or app |
| `triplets/` | The vcpkg overlay triplets `isotone-x64`, `isotone-arm64`, and `isotone-x64-asan` |
| `cmake/` | The shared CMake helpers |

`tinctura/`, `capio/`, and `folium/` join them when their plans (`todo/07-tinctura/`, `todo/08-capio/`, `todo/09-folium/`) build them. Today the folder holds the toolchain pin, the vcpkg manifest and configuration, and the triplets; the CMake build and the code arrive with `D00 T05 §3` onward.

## Entering the environment

Every build runs inside the pinned toolchain (`toolchain.json`), entered by `scripts/dev-env.ps1`; see `docs/dev/build.md`, "Native toolchain".

```powershell
pwsh scripts/dev-env.ps1 -Check -Arch x64        # the machine matches the pin (it also checks the triplets and the SDK)
. ./scripts/dev-env.ps1 -Arch arm64              # this session, inside the ARM64 cross environment
```

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
