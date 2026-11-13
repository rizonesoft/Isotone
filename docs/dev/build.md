# Building, packaging, and CI

How the Isotone Graphics Suite builds from the repository root: one native tree (`native/`), one pinned toolchain, one committed package baseline, and one command that runs every gate. The native tree's own page, [`native/README.md`](../../native/README.md), has the detail of the presets, the sanitizer lane, the analysis gates, the import and size gates, and the packages; this page is the map.

## Toolchain

| Tool | Version | Notes |
| ---- | ------- | ----- |
| Visual Studio 2026 | 18.11 or later, with the components `native/toolchain.json` lists | Supplies MSVC, the Windows SDK, CMake, Ninja, the LLVM tools, and vcpkg; see Native toolchain below. |
| PowerShell | 7.x | All `scripts/*.ps1` require `pwsh`. |
| Python | 3.x | The plan gates (`scripts/todo-graph.py` and friends) and the native checks; stdlib only. The icon generators' packages are pinned in `scripts/requirements-icons.txt`. |
| Inno Setup | 7.1 or newer | Only for installers. `scripts/_common.ps1` finds `ISCC.exe` under `Inno Setup 7` (or `$env:ISCC`) and refuses Inno Setup 6. |

`tools/provision.ps1` checks all of this and repairs what it can:

```powershell
pwsh tools/provision.ps1 -Verify   # report only; exit 1 on any fault
pwsh tools/provision.ps1           # repair, then verify
```

Repairs: installs the icon packages from `scripts/requirements-icons.txt` with pip, installs Inno Setup 7 through winget (`JRSoftware.InnoSetup.7`) with the official `innosetup-7.1.0-x64.exe` (SHA256 pinned) as the fallback, and sets `git config core.hooksPath tools/githooks`. A hooks path that already points somewhere else is left alone. The `native` leg never changes Visual Studio: it prints the exact `vs_installer.exe modify --add <component>` command for each component the pin needs and the machine lacks.

### Native toolchain

The C++ apps build with one exact toolchain, pinned in `native/toolchain.json` (`docs/dev/decisions.md`, "2026-10-23: The native toolchain pin"): Visual Studio 2026 18.12's MSVC toolset 14.52.37025 (compiler 19.52.37029) and bundled vcpkg 2026-09-26 (with an explicit `18.11.` rollout profile on MSVC toolset 14.51.36231 / compiler 19.51.36260 / vcpkg 2026-07-27 while GitHub Actions `windows-2025-vs2026` and `windows-11-vs2026-arm` complete their Visual Studio 18.12 image rollout), Windows SDK 10.0.26100.0, CMake 4.3.1-msvc1, Ninja 1.13.2, and LLVM 22.1.3 (clang-tidy, clang-format, clang-cl), read by the `toolchain-probe` workflow.

`scripts/dev-env.ps1` enters it and refuses anything else. It finds Visual Studio with `vswhere`, enters the toolset through `vcvarsall.bat -vcvars_ver=<toolset>` with the pinned SDK (`Launch-VsDevShell.ps1` cannot select a toolset), sets `VCPKG_ROOT` to the bundled vcpkg, and compares what the environment runs with the pin:

```powershell
pwsh scripts/dev-env.ps1 -Check -Arch x64     # one line per item, exit 1 on any mismatch or missing component
. ./scripts/dev-env.ps1 -Arch arm64           # this session, inside the ARM64 cross environment
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'cmake --version'   # one command inside it
```

Re-pinning after a Visual Studio or runner image update: run the `toolchain-probe` workflow, choose the newest toolset all three machines share, update `native/toolchain.json` and the decision record, and regenerate the test fixtures with `python scripts/tests/test_dev_env.py --write-fixtures`.

#### Reading the C# reference

The annotated tag `csharp-final` on `origin` marks commit `67872822e42422e3d527766d8656d09bf6066efa`, the last commit holding the imported C# Stilus and Gesso trees before `D00 T06 §3` removed them (`docs/dev/decisions.md`, "2026-10-23: The unattended campaign"). Re-plan and native build sections cite reference behavior from the imported apps as `csharp-final:<path>` (for example `csharp-final:src/Stilus/Bezier.Core/Services/CanvasHUDService.cs`), and inspect the tag directly from `main` without creating secondary git worktrees (`git worktree add` is prohibited by the trunk-only rule in `AGENTS.md` and `scripts/panel_slots.py agent-gate`):

```powershell
git ls-tree -r --name-only csharp-final -- src/                              # list every file in the imported C# trees
git show csharp-final:src/Stilus/Bezier.Core/Services/CanvasHUDService.cs    # read one reference file at csharp-final:<path>
git grep -n "CanvasHUDService" csharp-final -- src/                          # search across the imported C# sources and tests
```

`scripts/native-deps-lint.py` refuses any managed source or project file on `main`, so the reference lives only at the tag.

## One build description

| File | Role |
| ---- | ---- |
| `native/toolchain.json` | The toolchain pin `scripts/dev-env.ps1` enforces. |
| `native/CMakeLists.txt`, `native/cmake/` | The build. Every target goes through `isotone_add_library`, `isotone_add_executable`, `isotone_add_test`, `isotone_add_sanitizer_probe`, or `isotone_add_fuzz_target`, which apply the suite's flags (`/W4 /WX /permissive-`, the one C++23 switch, control-flow guard, and the rest). |
| `native/CMakePresets.json` | One configure, build, test, and workflow preset per configuration: `x64-debug`, `x64-release`, `x64-asan`, `x64-fuzz-msvc`, `x64-analyze`, `x64-dist`, and the ARM64 set. Ninja is the generator and `cl` the compiler. |
| `native/vcpkg.json`, `native/vcpkg-configuration.json`, `native/triplets/` | The package manifest, its one `builtin-baseline`, and the static overlay triplets (plain and AddressSanitizer, x64 and ARM64). |
| `native/.clang-format`, `native/.clang-tidy` | Formatting and static analysis, both held at zero findings. |
| `native/system-dlls.txt`, `native/sanitizer-dlls.txt`, `native/size-budget.json` | What an executable may import, and how large an app's publish folder may be. |
| `docs/dev/native-libraries.md` | The dependency register every third-party library enters through. |
| `.editorconfig`, `.gitattributes` | Whitespace and line endings for the whole tree. |

Nothing else configures the build.

### Output layout

All build output is under `artifacts/` (gitignored):

| Path | Contents |
| ---- | -------- |
| `artifacts/native/<preset>/` | One CMake build folder per preset in `native/CMakePresets.json` (its `compile_commands.json`, executables, and PDBs) |
| `artifacts/vcpkg_installed/<preset>/` | The vcpkg packages that preset installed, one root per preset |
| `artifacts/publish/<App>/<rid>/` | An app's publish folder (planned with native packaging; `scripts/native-artifact-gate.py --publish` holds it to its size budget) |
| `artifacts/dist/` | Installers, portable ZIPs, `SHA256SUMS` (planned with native packaging) |

The repository-root `build/` folder is a gitignored scratch area for logs, caches, and campaign guard state (for example `build/todo-cache.json`). Do not put tracked files there.

## Everyday commands

```powershell
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; cmake --workflow --preset x64-debug'     # configure, build, and test one preset
pwsh scripts/dev-env.ps1 -Arch x64 -Run 'Push-Location native; ctest --preset x64-debug -R BuildInfo'   # run the cases a change touches
pwsh scripts/native-format.ps1 -Check        # clang-format on every native source (-Fix rewrites them)
pwsh scripts/native-tidy.ps1                 # clang-tidy over the x64 Debug compile database (it builds only the isotone_generated target: the generated sources, no compile or link)
pwsh scripts/check-all.ps1                   # every gate (below); -SkipNative leaves the native stages out
```

`scripts/build.ps1` and `scripts/publish.ps1` are the retired wrappers of the removed build: each exits 1 naming the commands above until the native release path is planned (`D00 T07 §5`). `scripts/apps.psd1` is the app manifest the packaging scripts read: exe name, tag prefix, installer script, and whether the app ships.

### check-all.ps1

Runs every stage and reports a table at the end (exit 1 if any stage failed). Run it through `bosun run -- pwsh scripts/check-all.ps1` on a machine that queues heavy jobs.

- **The plan gates:** `todo-graph.py self-test`, `validate`, and `plan --check`; `todo-claims.py`; `todo-findings.py --check`; `todo-runs.py --check`; `campaign_guard.py --self-test`.
- **The design gates:** `build-design-site.py --check`, `generate-ui-tokens.py --check` (the `isotone::ui` token tables are what `docs/design/tokens.json` generates) with `tests/test_generate_ui_tokens.py`, `build-app-icons.py --check`, `generate-small-icons.py --check`, `build-suite-mark.py --check`, `export-icons.py --check`, `tests/test_export_icons.py`, `design-lint.py --self-test`, `design-lint.py --baseline docs/design/.lint-baseline.json`, and `tests/test_render_design_reference.py`.
- **The trusted revision of the two shrink-only baselines.** `docs/design/.lint-baseline.json` and `todo/.design-baseline` may shrink freely and never grow unrecorded, and growth is judged against the baseline at a trusted revision, never against the candidate itself. `design-lint.py --base <rev>` and `todo-graph.py validate --base <rev>` name it; without the option it is `HEAD`, which in the commit hook is the parent of the commit being made. CI checks out the candidate, where `HEAD` is the candidate, so `build.yml` and `plan.yml` pass the revision the change started from: on `push` the commit before the push (`github.event.before`), on `pull_request` the base commit (`github.event.pull_request.base.sha`), and on `workflow_dispatch`, or a push with no earlier commit, the first parent (`HEAD^`). A `--base` that names no readable commit fails the run.
- **The review and automation tooling:** `panel_slots.py` (self-test and validate), `review_pin.py`, the review dispatcher, prompt, and three-pass tests, `ci_status`, `ci_watch`, `weakening-scan`, `completion_check`, the automations and pin automation tests, the merger tests, and the language-server MCP server's tests.
- **The native self-tests:** `native-deps-lint`, `check-native-advisories`, `native-std-check`, `native-pe-check`, and `native-artifact-gate`, plus the tests of `dev-env`, the format and tidy scripts, the sanitizer lane, the fuzz replay, and the ARM64 test runner.
- **The native stages** (skipped by `-SkipNative`): the environment check; configure, build, and CTest for `x64-debug` and `x64-release`; the benchmarks' smoke run; the AddressSanitizer preset; the fuzz preset; the ARM64 Debug, Release, and sanitizer builds; the `/analyze` presets; the distribution presets; clang-format and clang-tidy; the dependency register lint; and the import, static CRT, and size gates over every preset.

`.claude/skills/process-todo-section/gates.md` lists what each stage proves. A Python gate whose script is missing is skipped with a warning rather than failed.

## App icons

The icons are SVG sources; every raster is generated from them, never exported by hand. To change an icon, edit its geometry in `scripts/build-app-icons.py` (the suite icon: `scripts/build-suite-mark.py`, then `python scripts/generate-small-icons.py --in-place`), run it, then run `python scripts/export-icons.py`, and commit the SVGs and the rasters together. The export renders each app's sixteen PNG sizes from the SVG the ladder in `docs/design/app-icons.md` names, the three splash renders, and the ten-entry `.ico`, for the six apps and the suite. CI's `native` job runs every generator's `--check` and `export-icons.py --check --require-fonts`, which fails where the splash font (Segoe UI Variable) is missing rather than skipping it; `scripts/check-all.ps1` runs the same checks, each a SKIP with a warning when `scripts/requirements-icons.txt` is not installed.

## Publishing and packaging

Native packaging is planned in `todo/05-release/` (re-planned by `D00 T07 §5`): building the distribution presets, staging each app's publish folder, and producing the installer and portable ZIP per architecture. Today `scripts/package.ps1 -App <App>` runs the native advisory release gate (`python scripts/check-native-advisories.py --release-gate`) and then stops with a message naming that section.

**Per-app and suite releases are independent.** A `stilus-v*` or `gesso-v*` tag ships only that app's installer and ZIP; it never builds or needs the suite installer. An `isotone-v*` tag ships only the suite installer and ZIP. Either way the files are uploaded to `download.rizonesoft.com` (`<slug>/<version>/`), never attached to the GitHub release; [versioning.md](versioning.md) has the layout, the update feed, and the repository settings.

### Installers

`installer/common.iss` holds the shared defines and `[Setup]` directives. Each app script defines its name, exe, AppId GUID, and icon, then includes it.

- Per-user by default (`PrivilegesRequired=lowest`); the privileges dialog offers an all-users install.
- Each app has its own AppId and its own install folder (`{autopf}\<App>`). The suite has its own AppId, installs each app into its own subfolder of `{autopf}\Isotone Graphics Suite`, and uses its own ProgIDs, so it never shares folders or registry keys with the standalone installers.
- Built with Inno Setup 7: a 64-bit Setup program that installs in 64-bit mode, modern wizard following the system light or dark theme (`WizardStyle=modern dynamic`), LZMA2 max solid compression, uninstaller, Start menu shortcut, optional desktop icon.
- Supported OS: Windows 11. Windows 10 (1809 or later) can still install; on build < 22000 the wizard shows one non-blocking page saying Windows 10 is untested. Silent installs (`/SILENT`, `/VERYSILENT`) show no wizard pages, so they skip it.
- File associations are opt-in tasks: Stilus `.svg`; Gesso `.png`, `.jpg`/`.jpeg`, `.psd`.
- Version from `/DAppVersion` (SemVer) and `/DAppFileVersion` (four-part), passed by the packaging script.
- `Albumen.iss` refuses to compile unless `/DAlbumenShipping` is defined; `apps.psd1` marks Albumen as not shipping.
- App icons: the SVG sources under `resources/icons/<app>/` are built by `scripts/build-app-icons.py`, and every raster and ICO the installers and apps use by `scripts/export-icons.py` (App icons, below). Every app's ICO exists, Gesso's included; wiring it into `Gesso.exe` is `D03 T01 §4`'s.

The installer scripts were last exercised on 2026-09-26 against the removed prototypes; their first run against a native app is a section of `todo/05-release/`.

## CI

| Workflow | Trigger | What it does |
| -------- | ------- | ------------ |
| `.github/workflows/build.yml` (`build`) | every push and pull request to `main`, and manual dispatch | Job `native` on `windows-2025-vs2026`: the design-lint self-test and baseline gates, the pinned toolchain check for x64 and ARM64, the vcpkg binary cache, every native preset built and tested on x64 (ARM64 cross-built), the benchmarks' smoke run, the analysis, format, register, import, and size gates, and the optional design reference renders uploaded as the `design-reference` artifact. Job `native-arm64-tests` on `windows-11-vs2026-arm` runs the ARM64 test suites, the sanitizer lane included, on ARM64 hardware. A newer push cancels a run in progress. |
| `.github/workflows/plan.yml` (`plan-gates`) | changes to `scripts/`, `todo/`, `docs/reviews/`, `.claude/`, `.conclave/`, hooks, `AGENTS.md`, `docs/design/**`, and `resources/icons/**` | Job `plan-gates` on ubuntu-26.04: `todo-graph.py self-test`, `validate`, `plan --sync` followed by a clean `git status`, `campaign_guard.py --self-test`, commit-hook integrity (mode 100755, LF blob, eol attribute), the design-lint self-test, and the design page check. Job `campaign-guard` runs the guard self-test on windows-2025. |
| `.github/workflows/pages.yml` (`design-pages`) | changes to `docs/design/`, `resources/icons/`, `scripts/build-design-site.py` | Checks the committed design page against its sources and deploys it to https://rizonesoft.github.io/Isotone/design/. |
| `.github/workflows/fuzz.yml` (`fuzz`) | nightly, and manual dispatch | Builds the fuzz preset and runs every registered libFuzzer target for 5 minutes, uploading any crash, timeout, or out-of-memory input as the `fuzz-crash-inputs` artifact. |
| `.github/workflows/pins.yml` (`pins`) | daily, and manual dispatch | Checks every registered native library against advisories and the committed vcpkg baseline, and files an issue for a finding that needs the owner. |
| `.github/workflows/toolchain-probe.yml` | weekly, and manual dispatch | Reads the toolsets the runner images and the pin offer, the input to a re-pin. |
| `.github/workflows/release.yml` (`release`) | tags `stilus-v*`, `gesso-v*`, `albumen-v*`, `isotone-v*`; manual dispatch with `tag` and `draft` inputs | Runs the native advisory release gate, then refuses the release until native packaging is planned (`D00 T07 §5`). The planned pipeline is in [versioning.md](versioning.md). |
| `.github/dependabot.yml` | weekly | GitHub Actions (grouped). Native libraries are kept current by `pins.yml`, not by Dependabot. |

Every action is pinned by full commit SHA with the tag in a trailing comment. Dependency pull requests are merged at section boundaries by `scripts/merge_prs.py` (`D00 T01 §12`), and `scripts/ci_watch.py` names any workflow whose latest run on `main` is red.

The first recorded green runs, read back by `D00 T01 §5` (they are runs of the removed prototypes' build, kept as the record of the first green CI):

| Workflow | First green run | Commit | Date (UTC) |
| -------- | --------------- | ------ | ---------- |
| `build` | https://github.com/rizonesoft/Isotone/actions/runs/36202856393 | `7578c90` | 2026-09-25 23:55 (2026-09-26 local) |
| `plan-gates` | https://github.com/rizonesoft/Isotone/actions/runs/36203128891 | `819cd2f` | 2026-09-25 23:59 (2026-09-26 local; the run before it failed) |

## Packages

Third-party libraries come from vcpkg in manifest mode, pinned to one baseline, built by the pinned toolset through the suite's static triplets, and linked statically against the static C runtime. Each one is a recorded decision in the dependency register, [`native-libraries.md`](native-libraries.md), added in the same commit as the code that first uses it; `scripts/native-deps-lint.py` keeps the register and the installed ports in step, and `scripts/check-native-advisories.py` checks every registered library against advisories daily. [`native/README.md`](../../native/README.md), "Packages" and "Binary caching", has the commands and the cache keys.

## Known gaps

Each is owned by a section of the plan; nothing else is relaxed.

- The UI toolkit and the apps are not built yet: `native/` holds the toolchain, the build, the gates, and `isotone::core`'s first pieces. The foundations are authored by `D00 T07 §3`.
- Native packaging, the version computed from the tag, and the release pipeline's native steps are planned in `todo/05-release/` (`D00 T07 §5`).
- Code is not signed (installers and binaries): the certificate is an operator row in `todo/99-manual/`.

<!-- claim: exists docs/facts.json -->
<!-- claim: exists scripts/drift-check.py -->
