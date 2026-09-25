---
schema_version: 1
id: build-test-debt
domain: 00-workspace
status: draft
title: "TODO-02 -- Build and Test Debt from the Import"
depends_on: []
track: W2
---

# TODO-02 -- Build and Test Debt from the Import

> **Goal:** The relaxations the import needed are retired where they belong to the workspace: no test is quarantined, Imago builds with no diagnostic excused, the build output carries no temporary-project noise, no package ships that no code uses, the assertion library's license is a recorded decision, xUnit is current, and the release workflow has produced a real prerelease from a tag.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `dotnet test Photon.slnx` passed 1,026 tests on 2026-09-26, but only because three legacy tests are excluded through `TestCaseFilter` in `tests/Photon.runsettings`: `ElementTooltipTests.ElementTooltip_FromElement_UsesUnnamedForNullName` (fails every run; `ElementTooltip.FromElement` in `src/Nodus/Bezier.Core/Services/CanvasHUDService.cs` line 242 falls back only on `null`, and the element name is empty) and the two `AssetLibraryServiceTests.ToggleFavorite_*` tests (flaky; `AssetLibraryService` writes to the real `%LOCALAPPDATA%\Bezier\Library`, line 113, so state leaks between tests and runs). `src/Imago/Directory.Build.props` keeps `IDE0005`, `CS0618`, and `NU1701` as warnings. `docs/dev/build.md` lists the `*_wpftmp` folders under `artifacts/bin/`. Six packages are referenced by projects but used by no code: `ReactiveUI.WPF` and `SharpDX.DirectInput` (Imago.UI; ReactiveUI only through two global usings), `SixLabors.ImageSharp` and `.Drawing` (Imago.FileFormats; global usings only), `Newtonsoft.Json` and `AvalonEdit` (Bezier.Desktop). FluentAssertions 8.11.0 (Xceed community license) is used by five Imago test files. xUnit is 2.9.3. No tag has been pushed, so `release.yml` has never run.
<!-- claim: count "FullyQualifiedName!=" tests/Photon.runsettings = 3 -->
<!-- claim: count "Name = element\.Name \?\? \"Unnamed\"" src/Nodus/Bezier.Core/Services/CanvasHUDService.cs = 1 -->
<!-- claim: count "IDE0005;CS0618;NU1701" src/Imago/Directory.Build.props = 1 -->
<!-- claim: count "global using ReactiveUI;" src/Imago/src/Imago.UI/GlobalUsings.cs = 1 -->
<!-- claim: count "Include=\"Newtonsoft.Json\"|Include=\"AvalonEdit\"" src/Nodus/Bezier.Desktop/Bezier.Desktop.csproj = 2 -->
<!-- claim: count "PackageVersion Include=\"xunit\" Version=\"2\.9\.3\"" Directory.Packages.props = 1 -->
<!-- claim: count "PackageVersion Include=\"FluentAssertions\" Version=\"8\." Directory.Packages.props = 1 -->

## Inputs

- [`docs/dev/build.md`](../../docs/dev/build.md) -- the debt list this file retires (quarantine, Imago diagnostics, `*_wpftmp`, held-back majors, FluentAssertions license note)
- [`tests/Photon.runsettings`](../../tests/Photon.runsettings) -- the quarantine §1 empties
- [`src/Imago/Directory.Build.props`](../../src/Imago/Directory.Build.props) -- the relaxations §2 removes
- [`Directory.Packages.props`](../../Directory.Packages.props) -- package versions §4, §5, §6 change
- [`.github/workflows/release.yml`](../../.github/workflows/release.yml), [`scripts/package.ps1`](../../scripts/package.ps1) -- the pipeline §7 exercises
- -> XREF: D02 T01 §1 -- the Nodus rename moves the test project §6 migrates; §6 runs after it
- -> XREF: D03 T04 §1 -- the Imago codec decision that §4's removal of ImageSharp leaves open, and that §5's decision log records
- -> XREF: D03 T01 §1 -- the Imago rename that waits for §2 and §4, and whose moved test projects §6 migrates

## Outcome

- `tests/Photon.runsettings` carries no `TestCaseFilter`, and the full suite passes three runs in a row.
- `src/Imago/Directory.Build.props` excuses nothing but `NU1701`, which leaves with SkiaSharp 4.
- A clean Release build leaves no `*_wpftmp` folder under `artifacts/`.
- No project references a package that no code uses, each removal cited with its evidence.
- `docs/dev/decisions.md` exists and records the assertion library, with its license.
- Every test project runs on xUnit v3.
- A `nodus-v0.1.0-alpha.1` prerelease exists on GitHub with an installer, a portable ZIP, and a `SHA256SUMS` that matches them.

**Adjacency:** all=not-applicable (build configuration, test hygiene, and the release pipeline's first run: no user-facing records, settings, or documents)

**Adjacency rationale:** The only user-visible artifact is the dry-run prerelease, which exists to prove the pipeline; the apps' own release sections own what users see.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On                    | Status |
| :---: | :-----: | ---------------------------------------------------- | ----------------------------- | :----: |
|   1   |   §1    | Fix the quarantined tests and empty the quarantine   | --                            |  [ ]   |
|   2   |   §2    | Imago diagnostics to zero                            | --                            |  [ ]   |
|   3   |   §3    | Quiet the WPF temporary project output               | --                            |  [ ]   |
|   4   |   §4    | Prune packages no code uses                          | --                            |  [ ]   |
|   5   |   §5    | The assertion library decision and the decision log  | --                            |  [ ]   |
|   6   |   §6    | xUnit v3                                             | §5, D02 T01 §1, D03 T01 §1    |  [ ]   |
|   7   |   §7    | Release pipeline dry run on a prerelease tag         | D00 T01 §5                    |  [ ]   |

---

## 1. Fix the Quarantined Tests and Empty the Quarantine

A quarantine is debt with a collector, and this section is the collector. Both failures are in services the Nodus triage (`D02 T02 §1`) defers rather than deletes, so the tests must hold on their own now; the flaky pair is the more serious one, because a test that writes to the real `%LOCALAPPDATA%` touches the developer's own data.

- [ ] `ElementTooltip.FromElement` in `src/Nodus/Bezier.Core/Services/CanvasHUDService.cs` falls back to `"Unnamed"` when the name is null, empty, or whitespace (`string.IsNullOrWhiteSpace`). Done when: `ElementTooltip_FromElement_UsesUnnamedForNullName` passes. Cheaper substitute that fails: changing the test's expectation to `""`.
- [ ] `AssetLibraryService` takes its library folder through a constructor parameter (defaulting to the current `%LOCALAPPDATA%` path for the app), and `AssetLibraryServiceTests` passes a fresh temporary folder per test and deletes it in `Dispose`. Done when: running the class 20 times in a row (`for ($i=0;$i -lt 20;$i++){ dotnet test Photon.slnx --no-build --filter "FullyQualifiedName~AssetLibraryServiceTests" }`) passes every time and no file appears under `%LOCALAPPDATA%\Bezier\Library` during the runs.
- [ ] Remove the `TestCaseFilter` element from `tests/Photon.runsettings`, and keep the comment explaining what a quarantine entry must carry. Done when: the file has no `FullyQualifiedName!=`.
- [ ] Update the "Test quarantine" block of `docs/dev/build.md` to say the quarantine is empty and point at `standards/testing.md`. Done when: the table is gone and the sentence cites the standard.
- [ ] Commit: `"test: fix the three quarantined Nodus tests and empty the quarantine"`

**Test checkpoint:** `dotnet test Photon.slnx -c Release` exits 0 three runs in a row with the total test count three higher than the quarantined baseline and no skipped test; `grep -c FullyQualifiedName tests/Photon.runsettings` prints 0. Cheaper substitute that fails: a `[Fact(Skip=...)]` on the two flaky tests, which lowers the count.

## 2. Imago Diagnostics to Zero

Imago already builds with warnings as errors and code style enforced, except for three diagnostics kept as warnings. Two of them (`IDE0005` unnecessary usings, 12 sites; `CS0618` obsolete APIs, 2 sites) are cheap to clear now. `NU1701` comes from SkiaSharp.Views.WPF 3.x pulling .NET Framework OpenTK packages and leaves with the SkiaSharp 4 migration (`D02 T01 §6`), so it stays.

- [ ] Remove every unnecessary `using` the `IDE0005` warnings name, starting with `src/Imago/src/Imago.Core/GlobalUsings.cs` and `src/Imago/src/Imago.UI/GlobalUsings.cs`. Done when: `dotnet build Photon.slnx -c Release -v q 2>&1 | grep -c IDE0005` prints 0.
- [ ] Replace the two obsolete API calls `CS0618` names with their documented replacements (cite the replacement's Microsoft Learn or package doc URL in the commit body). Done when: the build reports no `CS0618` under `src/Imago/`.
- [ ] Change `WarningsNotAsErrors` in `src/Imago/Directory.Build.props` to `$(WarningsNotAsErrors);NU1701` and update its comment and the Imago block of `docs/dev/build.md`. Done when: the props file names only `NU1701`.
- [ ] Commit: `"build(imago): clear IDE0005 and CS0618 and stop excusing them"`

**Test checkpoint:** `dotnet build Photon.slnx -c Debug` and `-c Release` exit 0; reintroducing one unused `using System.Linq;` in any Imago file makes the Release build fail with `IDE0005` as an error. Cheaper substitute that fails: suppressing the IDs in `.editorconfig`.

## 3. Quiet the WPF Temporary Project Output

WPF markup compilation builds a generated `<Project>_<hash>_wpftmp` project, and under `UseArtifactsOutput` each one gets its own folder in `artifacts/bin/` and `artifacts/obj/`. They are harmless and noisy: a reader of `artifacts/` cannot tell which folders are real.

- [ ] Find the property that names the artifacts folder for the generated project (`ArtifactsProjectName` or the equivalent in the .NET 10 SDK's `Microsoft.NET.DefaultOutputPaths.targets`) and set it in `Directory.Build.props` so a `_wpftmp` project reuses its parent's folder, or `Directory.Build.targets` if the value is only known after evaluation. Done when: the chosen property and the SDK file and line that read it are cited in the commit body. Source: the SDK targets file shipped with the pinned SDK.
- [ ] Remove the `*_wpftmp` bullet from "Other known debt" in `docs/dev/build.md`. Done when: the bullet is gone.
- [ ] Commit: `"build: keep WPF temporary projects out of artifacts"`

**Test checkpoint:** after `Remove-Item artifacts -Recurse -Force; dotnet build Photon.slnx -c Release`, `Get-ChildItem artifacts -Recurse -Directory -Filter *_wpftmp*` returns nothing, and `dotnet test Photon.slnx -c Release --no-build` still exits 0 with the same test count. Cheaper substitute that fails: a post-build step that deletes the folders, which leaves them during the build and races incremental builds.

## 4. Prune Packages No Code Uses

A package reference is a dependency decision, a license to comply with, and bytes in every installer. Six references survive from the imports with no code behind them. Each removal cites its evidence: the grep that found no use.

- [ ] Remove `ReactiveUI.WPF` from `src/Imago/src/Imago.UI/Imago.UI.csproj` and its two global usings (`System.Reactive.Disposables`, `ReactiveUI`) from `src/Imago/src/Imago.UI/GlobalUsings.cs`. Done when: `grep -rn "ReactiveUI\|System.Reactive" src --include=*.cs --include=*.csproj` finds nothing and the build is green. Evidence: no `ReactiveObject`, `ReactiveCommand`, or `WhenActivated` in any file.
- [ ] Remove `SharpDX.DirectInput` from `Imago.UI.csproj`. Done when: `grep -rn SharpDX src` finds nothing. Evidence: no `SharpDX` namespace in any `.cs` file.
- [ ] Remove `SixLabors.ImageSharp` and `SixLabors.ImageSharp.Drawing` from `src/Imago/src/Imago.FileFormats/Imago.FileFormats.csproj` and their global usings. Done when: `grep -rn "SixLabors" src` finds nothing. Evidence: global usings only; 4.x needs a paid key; the codec choice is `D03 T04 §1`.
- [ ] Remove `Newtonsoft.Json` and `AvalonEdit` from `src/Nodus/Bezier.Desktop/Bezier.Desktop.csproj`, and delete `src/Nodus/Bezier.Desktop/Resources/VsCodeDarkXml.xshd` and its `Content` item (an AvalonEdit highlighting file nothing loads). Done when: `grep -rn "Newtonsoft\|AvalonEdit\|ICSharpCode" src` finds nothing. Evidence: no `JsonConvert`, no `TextEditor`, no `.xshd` loader.
- [ ] Remove the six `PackageVersion` entries from `Directory.Packages.props`, the dependabot ignore rules for ImageSharp in `.github/dependabot.yml`, and their rows from the package table of `docs/dev/build.md`. Done when: `dotnet restore Photon.slnx` exits 0 and no removed id appears in either file.
- [ ] Launch-smoke both apps from their Debug output (`Bezier.Desktop.exe`, `Imago.exe`): each reaches its main window and closes through its own menu. Done when: both stay up and the Imago log for the run (`%LOCALAPPDATA%\Imago\logs\`) has 0 `[ERR]` or `[FTL]` lines.
- [ ] Commit: `"build: remove six packages no code uses"`

**Requires:** display-session -- the launch smoke in `.claude/skills/process-todo-section/gates.md` needs an interactive desktop to show both main windows

**Test checkpoint:** `dotnet build Photon.slnx -c Release` exits 0; `dotnet test Photon.slnx` exits 0 with the same count as before the section; the grep lines above each print nothing; the published Imago folder (`pwsh scripts/publish.ps1 -App Imago`) contains no `ReactiveUI*.dll`, `SharpDX*.dll`, or `SixLabors*.dll`. Cheaper substitute that fails: removing only the `PackageVersion` lines, which fails restore.

## 5. The Assertion Library Decision and the Decision Log

FluentAssertions 8 is licensed by Xceed under a community license that is free for non-commercial use; this suite is GPL-3.0 open source, but "non-commercial" is a restriction a GPL distributor cannot pass on, and a contributor at a company may not qualify. The options are pinning 7.x (Apache-2.0, frozen), switching to AwesomeAssertions (the Apache-2.0 community fork of 7.x, API compatible), or plain xUnit `Assert`. **Justified default: AwesomeAssertions**, because it keeps the five Imago test files' syntax and receives fixes; the cost of changing later is one namespace per file. This section also creates the decision log every later "decide with evidence" section writes to.

- [ ] Create `docs/dev/decisions.md` with a short header (what a decision record holds: date, question, options with licenses, evidence, choice, cost of change, owner section) and link it from `docs/dev/architecture.md`. Done when: the file exists and the architecture page links it.
- [ ] Record the assertion-library decision as the first entry, citing each option's license text URL and the Xceed license terms. Done when: the entry names the choice and its cost of change.
- [ ] Replace `FluentAssertions` with `AwesomeAssertions` in `Directory.Packages.props` and the two Imago test projects, and change `using FluentAssertions;` to `using AwesomeAssertions;` in the five test files. Done when: `grep -rn "FluentAssertions" src tests Directory.Packages.props` finds nothing.
- [ ] Update the package table and the license note in `docs/dev/build.md`, and name the library in `standards/testing.md`. Done when: both files name AwesomeAssertions.
- [ ] Commit: `"test: record the assertion library decision and move to AwesomeAssertions"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the Imago test count unchanged (41 test methods before, same after); `docs/dev/decisions.md` has one entry with a license URL per option. Cheaper substitute that fails: a comment in `Directory.Packages.props` saying "license checked", which records no options and no evidence.

## 6. xUnit v3

xUnit v3 is a separate package family (`xunit.v3`), runs tests as executables, and is where fixes land; v2 is in maintenance. It runs after the renames so the migration touches each test project once, in its final place.

- [ ] Replace `xunit` with `xunit.v3` in `Directory.Packages.props` and every test project, keep `xunit.runner.visualstudio` at a v3-compatible version, and set `OutputType` `Exe` where the v3 template requires it. Done when: `dotnet restore Photon.slnx` exits 0. Source: https://xunit.net/docs/getting-started/v3/migration
- [ ] Fix every API break the migration guide lists that the build reports (`IAsyncLifetime` returning `ValueTask`, `ITestOutputHelper` namespace, removed `Assert` overloads). Done when: `dotnet build Photon.slnx -c Release` exits 0.
- [ ] Confirm `tests/Photon.runsettings` is still honored (results under `artifacts/TestResults`). Done when: a `.trx` file appears there after `dotnet test Photon.slnx --logger trx`.
- [ ] Update the xunit row of the package table in `docs/dev/build.md`. Done when: the row reads `xunit.v3` with no "held" reason.
- [ ] Commit: `"test: migrate every test project to xUnit v3"`

**Test checkpoint:** `dotnet test Photon.slnx -c Release` exits 0 with the same total test count as before the migration and a `.trx` under `artifacts/TestResults`; `grep -rn '"xunit"' Directory.Packages.props` finds no v2 entry. Cheaper substitute that fails: leaving v2 and pinning it forever.

## 7. Release Pipeline Dry Run on a Prerelease Tag

`release.yml` resolves the app from the tag prefix, runs the tests, packages, writes `SHA256SUMS`, and creates the GitHub release. It has never run. A prerelease tag proves the whole chain on a real runner without claiming a product release; the tag is a hyphenated version, so the workflow marks it prerelease and MinVer versions later commits above it.

**Needs:** Windows host (build/test)

- [ ] Run `pwsh scripts/package.ps1 -App Nodus -Version 0.1.0-alpha.1` locally first. Done when: `artifacts/dist/` holds the Setup exe and the portable ZIP.
- [ ] Add a `nodus-v0.1.0-alpha.1` heading to `CHANGELOG.md` under Nodus with one line: "Pipeline dry run of the imported Bezier code; not a product release." Done when: the heading exists, so the workflow lifts real notes.
- [ ] Push the tag `nodus-v0.1.0-alpha.1` on the commit that carries the changelog. Done when: `gh run list --workflow release.yml --limit 1 --json conclusion` prints `success`; a red run is fixed and re-tagged as `-alpha.2`, never force-moved.
- [ ] Download the release assets with `gh release download nodus-v0.1.0-alpha.1 -D build/release-dry-run` and verify `SHA256SUMS` with `Get-FileHash`. Done when: every listed hash matches.
- [ ] Install the downloaded Setup exe silently per-user (`/VERYSILENT /CURRENTUSER`), launch the installed app, and uninstall it (`unins000.exe /VERYSILENT`). Done when: the app starts, and after uninstall its folder under `%LOCALAPPDATA%\Programs` is gone.
- [ ] Record the run URL, asset sizes, and hashes in the "Publishing and packaging" part of `docs/dev/build.md`. Done when: the record cites the run URL.
- [ ] Commit: `"release: dry-run the release pipeline with nodus-v0.1.0-alpha.1"`

**Requires:** display-session -- launching the installed app to prove it starts needs an interactive desktop

**Test checkpoint:** `gh release view nodus-v0.1.0-alpha.1 --json isPrerelease,assets` shows `isPrerelease: true` and three assets; `Get-FileHash` of each downloaded asset matches its `SHA256SUMS` line; the silent install and uninstall both exit 0. Cheaper substitute that fails: a `workflow_dispatch` run that never exercises the tag-prefix resolution.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 three runs in a row with no quarantine
- [ ] `docs/dev/build.md` lists no debt this file retired
- [ ] `python scripts/todo-graph.py validate` clean
