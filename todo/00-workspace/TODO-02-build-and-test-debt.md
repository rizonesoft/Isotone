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

> **Goal:** The relaxations the import needed are retired where they belong to the workspace: no test is quarantined, Gesso builds with no diagnostic excused, the build output carries no temporary-project noise, no package ships that no code uses, the assertion library's license is a recorded decision, xUnit is current, the SDK pin is a released (GA) .NET 11 SDK rather than a release candidate, and the release workflow has produced a real prerelease from a tag.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `dotnet test Isotone.slnx` passed 1,026 tests on 2026-09-26, but only because three legacy tests are excluded through `TestCaseFilter` in `tests/Isotone.runsettings`: `ElementTooltipTests.ElementTooltip_FromElement_UsesUnnamedForNullName` (fails every run; `ElementTooltip.FromElement` in `src/Stilus/Bezier.Core/Services/CanvasHUDService.cs` line 242 falls back only on `null`, and the element name is empty) and the two `AssetLibraryServiceTests.ToggleFavorite_*` tests (flaky; `AssetLibraryService` writes to the real `%LOCALAPPDATA%\Bezier\Library`, line 113, so state leaks between tests and runs). `src/Gesso/Directory.Build.props` keeps `IDE0005`, `CS0618`, and `NU1701` as warnings. `docs/dev/build.md` lists the `*_wpftmp` folders under `artifacts/bin/`. Six packages are referenced by projects but used by no code: `ReactiveUI.WPF` and `SharpDX.DirectInput` (Gesso.UI; ReactiveUI only through two global usings), `SixLabors.ImageSharp` and `.Drawing` (Gesso.FileFormats; global usings only), `Newtonsoft.Json` and `AvalonEdit` (Bezier.Desktop). FluentAssertions 8.11.0 (Xceed community license) is used by five Gesso test files. xUnit is 2.9.3. No tag has been pushed, so `release.yml` has never run.
>
> **Corrected 2026-09-26:** the 2026-09-26 toolchain upgrade (one `build:` commit: .NET 11 RC, SkiaSharp 4, xUnit v3, AwesomeAssertions, Inno Setup 7, package prune) landed out of band and changed this starting line. It said: `IDE0005`, `CS0618`, and `NU1701` excused; six unused packages referenced; FluentAssertions 8.11.0; xUnit 2.9.3; SDK 10.0.400. Now: the SDK is pinned to `11.0.100-rc.1.26425.128` (`global.json`, `allowPrerelease`, `rollForward: disable`); `src/Gesso/Directory.Build.props` excuses only `IDE0005` and `CS0618` (NU1701 no longer fires: SkiaSharp.Views.WPF 4 on the `net11.0-windows10.0.26100.0` TFM restores OpenTK 4); ReactiveUI.WPF, SharpDX.DirectInput, SixLabors.ImageSharp and `.Drawing`, Newtonsoft.Json, and AvalonEdit are gone with their global usings and the unused `VsCodeDarkXml.xshd`; the test projects run `xunit.v3.mtp-off` 4.0.1 (VSTest, `OutputType` `Exe`) with AwesomeAssertions 9.6.0 in the five Gesso test files; `dotnet test Isotone.slnx` still passes 1,026 tests with the same three quarantined. What stays open here is verification, the decision log, and the GA SDK pin (§8).
<!-- claim: count "FullyQualifiedName!=" tests/Isotone.runsettings = 3 -->
<!-- claim: count "Name = element\.Name \?\? \"Unnamed\"" src/Stilus/Bezier.Core/Services/CanvasHUDService.cs = 1 -->
<!-- claim: count "IDE0005;CS0618</WarningsNotAsErrors>" src/Gesso/Directory.Build.props = 1 -->
<!-- claim: count "global using ReactiveUI;" src/Gesso/src/Gesso.UI/GlobalUsings.cs = 0 -->
<!-- claim: count "Include=\"Newtonsoft.Json\"|Include=\"AvalonEdit\"" src/Stilus/Bezier.Desktop/Bezier.Desktop.csproj = 0 -->
<!-- claim: count "PackageVersion Include=\"xunit.v3.mtp-off\" Version=\"4\." Directory.Packages.props = 1 -->
<!-- claim: count "PackageVersion Include=\"AwesomeAssertions\"" Directory.Packages.props = 1 -->
<!-- claim: count "\"version\": \"11\.0\.100-rc\.1\.26425\.128\"" global.json = 1 -->

## Inputs

- [`docs/dev/build.md`](../../docs/dev/build.md) -- the debt list this file retires (quarantine, Gesso diagnostics, `*_wpftmp`, held-back majors, FluentAssertions license note)
- [`tests/Isotone.runsettings`](../../tests/Isotone.runsettings) -- the quarantine §1 empties
- [`src/Gesso/Directory.Build.props`](../../src/Gesso/Directory.Build.props) -- the relaxations §2 removes
- [`Directory.Packages.props`](../../Directory.Packages.props) -- package versions §4, §5, §6 change
- [`.github/workflows/release.yml`](../../.github/workflows/release.yml), [`scripts/package.ps1`](../../scripts/package.ps1) -- the pipeline §7 exercises
- [`global.json`](../../global.json) -- the SDK pin §8 moves from the release candidate to GA
- -> XREF: D02 T05 §4 -- the first product release, which §8 gates so nothing ships on a release-candidate SDK
- -> XREF: D02 T01 §1 -- the Stilus rename moves the test project §6 migrates; §6 runs after it
- -> XREF: D03 T04 §1 -- the Gesso codec decision that §4's removal of ImageSharp leaves open, and that §5's decision log records
- -> XREF: D03 T01 §1 -- the Gesso rename that waits for §2 and §4, and whose moved test projects §6 migrates

## Outcome

- `tests/Isotone.runsettings` carries no `TestCaseFilter`, and the full suite passes three runs in a row.
- `src/Gesso/Directory.Build.props` excuses no diagnostic. **Corrected 2026-09-26:** said "excuses nothing but `NU1701`, which leaves with SkiaSharp 4"; NU1701 already left with the toolchain upgrade.
- A clean Release build leaves no `*_wpftmp` folder under `artifacts/`.
- No project references a package that no code uses, each removal cited with its evidence.
- `docs/dev/decisions.md` exists and records the assertion library, with its license.
- Every test project runs on xUnit v3 (`xunit.v3.mtp-off`, VSTest), in its final place after the renames.
- `global.json` pins a released .NET 11 SDK (11.0.1xx GA), and every Microsoft.Extensions.* package matches its runtime.
- `release.yml` has a draft mode, and a `stilus-v0.1.0-alpha.1` draft release was built by it with an installer, a portable ZIP, and a `SHA256SUMS` that matches them, inspected, and deleted (**Corrected 2026-09-28:** read as: the draft release's body links them, kept in the `dist-<tag>` workflow artifact or under `drafts/` on `download.rizonesoft.com` once `D99 T01 §8` is done, and carries no attached files), so no public prerelease or tag remains (operator decision 2026-09-27).

**Adjacency:** all=not-applicable (build configuration, test hygiene, and the release pipeline's first run: no user-facing records, settings, or documents)

**Adjacency rationale:** The only artifact is the dry-run draft release, visible to maintainers only and deleted after inspection, which exists to prove the pipeline; the apps' own release sections own what users see.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On                    | Status |
| :---: | :-----: | ---------------------------------------------------- | ----------------------------- | :----: |
|   1   |   §1    | Fix the quarantined tests and empty the quarantine   | --                            |  [ ]   |
|   2   |   §2    | Gesso diagnostics to zero                            | --                            |  [ ]   |
|   3   |   §3    | Quiet the WPF temporary project output               | --                            |  [ ]   |
|   4   |   §4    | Prune packages no code uses                          | --                            |  [ ]   |
|   5   |   §5    | The assertion library decision and the decision log  | --                            |  [ ]   |
|   6   |   §6    | xUnit v3                                             | §5, D02 T01 §1, D03 T01 §1    |  [ ]   |
|   7   |   §7    | Release pipeline dry run as a draft release          | D00 T01 §5                    |  [ ]   |
|   8   |   §8    | Pin the .NET 11 GA SDK                               | --                            |  [ ]   |

---

## 1. Fix the Quarantined Tests and Empty the Quarantine

A quarantine is debt with a collector, and this section is the collector. Both failures are in services the Stilus triage (`D02 T02 §1`) defers rather than deletes, so the tests must hold on their own now; the flaky pair is the more serious one, because a test that writes to the real `%LOCALAPPDATA%` touches the developer's own data.

- [ ] `ElementTooltip.FromElement` in `src/Stilus/Bezier.Core/Services/CanvasHUDService.cs` falls back to `"Unnamed"` when the name is null, empty, or whitespace (`string.IsNullOrWhiteSpace`). Done when: `ElementTooltip_FromElement_UsesUnnamedForNullName` passes. Cheaper substitute that fails: changing the test's expectation to `""`.
- [ ] `AssetLibraryService` takes its library folder through a constructor parameter (defaulting to the current `%LOCALAPPDATA%` path for the app), and `AssetLibraryServiceTests` passes a fresh temporary folder per test and deletes it in `Dispose`. Done when: running the class 20 times in a row (`for ($i=0;$i -lt 20;$i++){ dotnet test Isotone.slnx --no-build --filter "FullyQualifiedName~AssetLibraryServiceTests" }`) passes every time and no file appears under `%LOCALAPPDATA%\Bezier\Library` during the runs.
- [ ] Remove the `TestCaseFilter` element from `tests/Isotone.runsettings`, and keep the comment explaining what a quarantine entry must carry. Done when: the file has no `FullyQualifiedName!=`.
- [ ] Update the "Test quarantine" block of `docs/dev/build.md` to say the quarantine is empty and point at `standards/testing.md`. Done when: the table is gone and the sentence cites the standard.
- [ ] Commit: `"test: fix the three quarantined Stilus tests and empty the quarantine"`

**Test checkpoint:** `dotnet test Isotone.slnx -c Release` exits 0 three runs in a row with the total test count three higher than the quarantined baseline and no skipped test; `grep -c FullyQualifiedName tests/Isotone.runsettings` prints 0. Cheaper substitute that fails: a `[Fact(Skip=...)]` on the two flaky tests, which lowers the count.

## 2. Gesso Diagnostics to Zero

Gesso already builds with warnings as errors and code style enforced, except for three diagnostics kept as warnings. Two of them (`IDE0005` unnecessary usings, 12 sites; `CS0618` obsolete APIs, 2 sites) are cheap to clear now. `NU1701` comes from SkiaSharp.Views.WPF 3.x pulling .NET Framework OpenTK packages and leaves with the SkiaSharp 4 migration (`D02 T01 §6`), so it stays. **Corrected 2026-09-26:** the 2026-09-26 toolchain upgrade (one `build:` commit: .NET 11 RC, SkiaSharp 4, xUnit v3, AwesomeAssertions, Inno Setup 7, package prune) already removed `NU1701` from the props file (it no longer fires) and fixed the new .NET 11 SDK diagnostics in Gesso (`IDE0054`, `IDE0330`, and three `IDE1006` names); the `CS0618` count is now 1 (WPF-UI `IContentDialogService.SetDialogHost` in `Views/MainWindow.xaml.cs`), so this section ends with no excused diagnostic at all.

**Corrected 2026-09-28:** `docs/dev/build.md` counts 6 `IDE0005` sites after the toolchain upgrade against the 12 above; the section re-counts from the build output rather than trusting either figure.

- [ ] Remove every unnecessary `using` the `IDE0005` warnings name, starting with `src/Gesso/src/Gesso.Core/GlobalUsings.cs` and `src/Gesso/src/Gesso.UI/GlobalUsings.cs`. Done when: `dotnet build Isotone.slnx -c Release -v q 2>&1 | grep -c IDE0005` prints 0.
- [ ] Replace the two obsolete API calls `CS0618` names with their documented replacements (cite the replacement's Microsoft Learn or package doc URL in the commit body). Done when: the build reports no `CS0618` under `src/Gesso/`.
- [ ] Remove `WarningsNotAsErrors` from `src/Gesso/Directory.Build.props` and update its comment and the Gesso block of `docs/dev/build.md`. Done when: the props file excuses nothing. **Corrected 2026-09-26:** said "change it to `NU1701` only"; NU1701 left out of band.
- [ ] Commit: `"build(gesso): clear IDE0005 and CS0618 and stop excusing them"`

**Test checkpoint:** `dotnet build Isotone.slnx -c Debug` and `-c Release` exit 0; reintroducing one unused `using System.Linq;` in any Gesso file makes the Release build fail with `IDE0005` as an error. Cheaper substitute that fails: suppressing the IDs in `.editorconfig`.

## 3. Quiet the WPF Temporary Project Output

WPF markup compilation builds a generated `<Project>_<hash>_wpftmp` project, and under `UseArtifactsOutput` each one gets its own folder in `artifacts/bin/` and `artifacts/obj/`. They are harmless and noisy: a reader of `artifacts/` cannot tell which folders are real.

- [ ] Find the property that names the artifacts folder for the generated project (`ArtifactsProjectName` or the equivalent in the .NET 11 SDK's `Microsoft.NET.DefaultOutputPaths.targets`; **Corrected 2026-09-26:** said the .NET 10 SDK, the pin moved) and set it in `Directory.Build.props` so a `_wpftmp` project reuses its parent's folder, or `Directory.Build.targets` if the value is only known after evaluation. Done when: the chosen property and the SDK file and line that read it are cited in the commit body. Source: the SDK targets file shipped with the pinned SDK.
- [ ] Remove the `*_wpftmp` bullet from "Other known debt" in `docs/dev/build.md`. Done when: the bullet is gone.
- [ ] Commit: `"build: keep WPF temporary projects out of artifacts"`

**Test checkpoint:** after `Remove-Item artifacts -Recurse -Force; dotnet build Isotone.slnx -c Release`, `Get-ChildItem artifacts -Recurse -Directory -Filter *_wpftmp*` returns nothing, and `dotnet test Isotone.slnx -c Release --no-build` still exits 0 with the same test count. Cheaper substitute that fails: a post-build step that deletes the folders, which leaves them during the build and races incremental builds.

## 4. Prune Packages No Code Uses

A package reference is a dependency decision, a license to comply with, and bytes in every installer. Six references survive from the imports with no code behind them. Each removal cites its evidence: the grep that found no use.

**Corrected 2026-09-26:** the six removals below were done out of band by the 2026-09-26 toolchain upgrade (one `build:` commit: .NET 11 RC, SkiaSharp 4, xUnit v3, AwesomeAssertions, Inno Setup 7, package prune), with this evidence: no `ReactiveObject`, `ReactiveCommand`, `WhenActivated`, `Observable.`, or `IObservable` in any file (ReactiveUI only through two global usings); no `SharpDX` namespace; `SixLabors` only in `Gesso.FileFormats/GlobalUsings.cs`; no `JsonConvert`, `TextEditor`, `ICSharpCode`, or `.xshd` loader. The build and 1,026 tests stayed green. The same audit found two more unused references this section does not own: `ComputeSharp` and `SkiaSharp.Views.WPF` in `Gesso.Rendering.csproj` (no `ComputeSharp` or `SK*` type in Gesso code), left in place because the rendering plan uses them (`D03 T02 §5` for ComputeSharp, `D03 T02 §2` for the canvas). So the items are rewritten to verify the removal on the current tree rather than perform it; none is ticked without the review stamp.

- [ ] Verify `ReactiveUI.WPF` and its two global usings (`System.Reactive.Disposables`, `ReactiveUI`) are gone from `src/Gesso/src/Gesso.UI/` (removed out of band). Done when: `grep -rn "ReactiveUI\|System.Reactive" src --include=*.cs --include=*.csproj` finds nothing and the build is green. Evidence: no `ReactiveObject`, `ReactiveCommand`, or `WhenActivated` in any file.
- [ ] Verify `SharpDX.DirectInput` is gone from `Gesso.UI.csproj` (removed out of band). Done when: `grep -rn SharpDX src` finds nothing. Evidence: no `SharpDX` namespace in any `.cs` file.
- [ ] Verify `SixLabors.ImageSharp` and `SixLabors.ImageSharp.Drawing` and their global usings are gone from `src/Gesso/src/Gesso.FileFormats/` (removed out of band). Done when: `grep -rn "SixLabors" src` finds nothing. Evidence: global usings only; 4.x needs a paid key; the codec choice is `D03 T04 §1`.
- [ ] Verify `Newtonsoft.Json`, `AvalonEdit`, `src/Stilus/Bezier.Desktop/Resources/VsCodeDarkXml.xshd`, and its `Content` item are gone (removed out of band). Done when: `grep -rn "Newtonsoft\|AvalonEdit\|ICSharpCode" src` finds nothing. Evidence: no `JsonConvert`, no `TextEditor`, no `.xshd` loader.
- [ ] Verify the six `PackageVersion` entries, the dependabot ignore rules for ImageSharp in `.github/dependabot.yml`, and their rows in `docs/dev/build.md` are gone (removed out of band). Done when: `dotnet restore Isotone.slnx` exits 0 and no removed id appears in either file.
- [ ] Launch-smoke both apps from their Debug output (`Bezier.Desktop.exe`, `Gesso.exe`): each reaches its main window and closes through its own menu. Done when: both stay up and the Gesso log for the run (`%LOCALAPPDATA%\Gesso\logs\`) has 0 `[ERR]` or `[FTL]` lines.
- [ ] Commit: `"build: remove six packages no code uses"`

**Requires:** display-session -- the launch smoke in `.claude/skills/process-todo-section/gates.md` needs an interactive desktop to show both main windows

**Test checkpoint:** `dotnet build Isotone.slnx -c Release` exits 0; `dotnet test Isotone.slnx` exits 0 with the same count as before the section; the grep lines above each print nothing; the published Gesso folder (`pwsh scripts/publish.ps1 -App Gesso`) contains no `ReactiveUI*.dll`, `SharpDX*.dll`, or `SixLabors*.dll`. Cheaper substitute that fails: removing only the `PackageVersion` lines, which fails restore.

## 5. The Assertion Library Decision and the Decision Log

FluentAssertions 8 is licensed by Xceed under a community license that is free for non-commercial use; this suite is GPL-3.0 open source, but "non-commercial" is a restriction a GPL distributor cannot pass on, and a contributor at a company may not qualify. The options are pinning 7.x (Apache-2.0, frozen), switching to AwesomeAssertions (the Apache-2.0 community fork of 7.x, API compatible), or plain xUnit `Assert`. **Justified default: AwesomeAssertions**, because it keeps the five Gesso test files' syntax and receives fixes; the cost of changing later is one namespace per file. Operator decision 2026-09-27: keep AwesomeAssertions; the choice is confirmed, not a default awaiting review, and the decision record says so. This section also creates the decision log every later "decide with evidence" section writes to.

**Corrected 2026-09-26:** the package switch was done out of band by the 2026-09-26 toolchain upgrade (one `build:` commit: .NET 11 RC, SkiaSharp 4, xUnit v3, AwesomeAssertions, Inno Setup 7, package prune) (AwesomeAssertions 9.6.0, five `using AwesomeAssertions;`, Gesso tests 41 before and after), and `docs/dev/build.md` and `standards/testing.md` already name it. What remains is the decision record itself and verifying the switch.

- [ ] Create `docs/dev/decisions.md` with a short header (what a decision record holds: date, question, options with licenses, evidence, choice, cost of change, owner section) and link it from `docs/dev/architecture.md`. Done when: the file exists and the architecture page links it.
- [ ] Record the assertion-library decision as the first entry, citing each option's license text URL and the Xceed license terms, with AwesomeAssertions as the choice confirmed by the operator 2026-09-27. Done when: the entry names the choice, the confirmation, and its cost of change.
- [ ] Verify `FluentAssertions` is replaced by `AwesomeAssertions` in `Directory.Packages.props`, the two Gesso test projects, and the five test files (switched out of band). Done when: `grep -rn "FluentAssertions" src tests Directory.Packages.props` finds nothing.
- [ ] Confirm the package table and the license note in `docs/dev/build.md` and `standards/testing.md` name AwesomeAssertions and point at the decision record. Done when: both files link `docs/dev/decisions.md`.
- [ ] Commit: `"test: record the assertion library decision and move to AwesomeAssertions"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with the Gesso test count unchanged (41 test methods before, same after); `docs/dev/decisions.md` has one entry with a license URL per option. Cheaper substitute that fails: a comment in `Directory.Packages.props` saying "license checked", which records no options and no evidence.

## 6. xUnit v3

xUnit v3 is a separate package family (`xunit.v3`), runs tests as executables, and is where fixes land; v2 is in maintenance. It runs after the renames so the migration touches each test project once, in its final place.

**Corrected 2026-09-26:** the migration itself was done out of band by the 2026-09-26 toolchain upgrade (one `build:` commit: .NET 11 RC, SkiaSharp 4, xUnit v3, AwesomeAssertions, Inno Setup 7, package prune), before the renames: `xunit.v3.mtp-off` 4.0.1 (the plain `xunit.v3` 4.x package brings `xunit.v3.mtp-v2`, and the .NET 11 SDK then refuses VSTest `dotnet test` with "Testing with VSTest target is no longer supported by Microsoft.Testing.Platform"), `xunit.runner.visualstudio` 4.0.0, `Microsoft.NET.Test.Sdk` 18.10.1, `OutputType` `Exe`, no source change needed. Discovery was proven: 985 + 33 + 8 = 1,026 passed, the three quarantined tests still discovered (988 with the filter off), and a `.trx` landed in `artifacts/TestResults`. The section is retargeted to what is left: re-proving it after both renames move the test projects, which is why its dependencies stand.

- [ ] After `D02 T01 §1` and `D03 T01 §1` move the test projects, confirm each still references `xunit.v3.mtp-off` and `xunit.runner.visualstudio`, sets `OutputType` `Exe`, and that no project references the plain `xunit` or `xunit.v3` id. Done when: `grep -rn 'Include="xunit"\|Include="xunit.v3"' --include=*.csproj .` prints nothing. Source: https://xunit.net/docs/getting-started/v3/migration
- [ ] Re-prove discovery on the moved projects: `dotnet test Isotone.slnx -c Release` reports the same per-assembly counts as before the renames. Done when: the counts are quoted before and after.
- [ ] Confirm `tests/Isotone.runsettings` is still honored (results under `artifacts/TestResults`). Done when: a `.trx` file appears there after `dotnet test Isotone.slnx --logger trx`.
- [ ] Confirm the package table in `docs/dev/build.md` lists `xunit.v3.mtp-off` with no "held" reason (updated out of band). Done when: the row is current.
- [ ] Commit: `"test: re-prove xUnit v3 discovery after the renames"`

**Test checkpoint:** `dotnet test Isotone.slnx -c Release` exits 0 with the same total test count as before the migration and a `.trx` under `artifacts/TestResults`; `grep -rn '"xunit"' Directory.Packages.props` finds no v2 entry. Cheaper substitute that fails: leaving v2 and pinning it forever.

## 7. Release Pipeline Dry Run as a Draft Release

`release.yml` resolves the app from the tag prefix, runs the tests, packages, writes `SHA256SUMS`, and creates the GitHub release. It has never run. Operator decision 2026-09-27: the dry run for `stilus-v0.1.0-alpha.1` runs as a **draft** GitHub release, never a public prerelease, and the draft is deleted after inspection. **Corrected 2026-09-27:** this section said the tag is pushed and the workflow publishes a public prerelease that stays on the Releases page; the operator chose a draft instead. So `release.yml` first gains a draft mode: a `workflow_dispatch` trigger with a required `tag` input and a `draft` input (default true) that runs the same tag resolution step as a tag push (the app from the prefix, the version from the rest) on the dispatched commit and passes `--draft --target <sha>` to `gh release create`. A draft release does not create its tag until it is published, so the dry run leaves no public release, no tag, and no version MinVer would build later commits above; the push trigger keeps publishing real releases unchanged.

**Corrected 2026-09-27, later the same day:** the operator decided that binaries are distributed only from rizonesoft.com (object storage behind `download.rizonesoft.com`), so a GitHub release, draft or not, carries no installer or ZIP: its body links the files, lists their SHA-256, and links the tag's source. `release.yml` was rewritten for that decision on 2026-09-27 and gained the draft mode this section asked for in the same change: the `workflow_dispatch` trigger with `tag` (validated by the one resolution step both triggers share) and `draft` (default true), `--draft --target <sha>` on a dispatch, and uploads under `drafts/` (`drafts/<slug>/<version>/`, `drafts/update/`) so a dry run never touches the live files or feeds. When the storage secrets are missing, the draft run skips the upload with a notice and keeps its files in the `dist-<tag>` workflow artifact, while a pushed tag fails before building. So the first item below verifies the mode rather than writing it, and the inspection reads the files from the workflow artifact (or from `drafts/` on `download.rizonesoft.com` when the operator's storage step `D99 T01 §8` is done) instead of from release assets.

**Needs:** Windows host (build/test)

- [ ] Add the draft mode to `.github/workflows/release.yml`: a `workflow_dispatch` trigger with inputs `tag` (required, validated against the `stilus-v*`, `gesso-v*`, `albumen-v*`, and `isotone-v*` patterns) and `draft` (boolean, default true); the tag resolution step reads the input on a dispatch and the pushed ref otherwise, so both paths share one resolution; a dispatched run with `draft: true` adds `--draft --target ${{ github.sha }}` to `gh release create`; the header comment and `standards/release.md` describe the mode (**Corrected 2026-09-27:** the mode landed with the distribution rewrite of `release.yml` that day, with uploads under `drafts/` and the skip-with-notice when storage is not configured; actionlint 1.7.12 reported nothing on the file then, so this item re-runs the check on the commit that dispatches and confirms the one shared resolution step). Done when: `actionlint` (version quoted) reports nothing on the file, and a review of the diff shows one resolution step used by both triggers.
- [ ] Run `pwsh scripts/package.ps1 -App Stilus -Version 0.1.0-alpha.1` locally first. Done when: `artifacts/dist/` holds the Setup exe and the portable ZIP.
- [ ] Add a `stilus-v0.1.0-alpha.1` heading to `CHANGELOG.md` under Stilus with one line: "Pipeline dry run of the imported Bezier code as a draft release, deleted after inspection; never published." Done when: the heading exists, so the workflow lifts real notes.
- [ ] Dispatch the draft run on the commit that carries the changelog: `gh workflow run release.yml --ref main -f tag=stilus-v0.1.0-alpha.1 -f draft=true`, without pushing the tag. Done when: `gh run list --workflow release.yml --limit 1 --json conclusion,event` prints `success` and `workflow_dispatch`; a red run is fixed, its draft (if any) deleted, and the run dispatched again, and no tag is ever pushed for the dry run.
- [ ] Inspect the draft: `gh release view stilus-v0.1.0-alpha.1 --json isDraft,isPrerelease,assets,body` shows `isDraft: true`, `isPrerelease: true`, no assets, and a body with the Download links (under `https://download.rizonesoft.com/drafts/stilus/0.1.0-alpha.1/`), the SHA-256 table, and the source link; the run summary shows either the upload or the "Upload skipped" notice naming the missing secrets; and `git ls-remote --tags origin stilus-v0.1.0-alpha.1` prints nothing (**Corrected 2026-09-27:** said three assets; a release carries none since the distribution decision). Done when: the outputs are quoted.
- [ ] Download the run's files with `gh run download <run id> -n dist-stilus-v0.1.0-alpha.1 -D build/release-dry-run` (or, when the upload ran, from the draft body's `drafts/` links) and verify `SHA256SUMS` and the body's SHA-256 table with `Get-FileHash` (**Corrected 2026-09-27:** said `gh release download` of the draft's assets, which no longer exist). Done when: every listed hash matches both.
- [ ] Install the downloaded Setup exe silently per-user (`/VERYSILENT /CURRENTUSER`), launch the installed app, and uninstall it (`unins000.exe /VERYSILENT`). Done when: the app starts, and after uninstall its folder under `%LOCALAPPDATA%\Programs` is gone.
- [ ] Delete the draft after inspection: `gh release delete stilus-v0.1.0-alpha.1 --yes --cleanup-tag`, and, when the upload ran, delete the `drafts/` folder from the bucket (`rclone purge dl:<bucket>/drafts` with the storage credentials from outside the repository). Done when: `gh release view stilus-v0.1.0-alpha.1` fails with "release not found", `git ls-remote --tags origin stilus-v0.1.0-alpha.1` prints nothing, and `https://download.rizonesoft.com/drafts/update/stilus-prerelease.json` returns 404 when the upload ran (all quoted).
- [ ] Record the run URL, asset sizes, hashes, and the deletion in the "Publishing and packaging" part of `docs/dev/build.md`. Done when: the record cites the run URL and states the draft was deleted.
- [ ] Commit: `"release: dry-run the release pipeline as a draft stilus-v0.1.0-alpha.1"`

**Requires:** display-session -- launching the installed app to prove it starts needs an interactive desktop

**Test checkpoint:** `gh release view stilus-v0.1.0-alpha.1 --json isDraft,isPrerelease,assets,body` showed `isDraft: true`, no assets, and a body linking the three files before deletion and fails with "release not found" after it; `Get-FileHash` of each downloaded file matched its `SHA256SUMS` line and the body's table; the silent install and uninstall both exited 0; `git ls-remote --tags origin stilus-v0.1.0-alpha.1` printed nothing throughout. Cheaper substitute that fails: a public prerelease from a pushed tag, which the operator refused and which the `isDraft` and `ls-remote` checks catch; and a dispatch path with its own tag parsing, which the one-resolution-step review catches.

## 8. Pin the .NET 11 GA SDK

The operator chose on 2026-09-26 to move to .NET 11 on its release candidate, `11.0.100-rc.1.26425.128`, with Microsoft.Extensions.* at the matching `11.0.0-rc.1.26425.128`. A release candidate carries a go-live license but not the support of a GA release, and .NET 11 GA ships in November 2026. This section moves the pin to GA the week it ships, so that `D02 T05 §4` (the first product release) never ships on a release candidate. It depends on an external event the graph cannot see: until the GA SDK is published, a runner that reaches this row parks it with the blocker "no .NET 11 GA SDK on dotnet.microsoft.com yet" named, and takes the next row.

**Needs:** .NET SDK (build/test)

- [ ] Precondition: the .NET 11 GA SDK (`11.0.100` or a later `11.0.1xx`) is listed at https://dotnet.microsoft.com/download/dotnet/11.0 and in `https://builds.dotnet.microsoft.com/dotnet/release-metadata/11.0/releases.json` with `release-type` not `preview`/`rc`. Done when: the SDK version and its release date are quoted; before then the row parks with this blocker.
- [ ] Install that SDK machine-wide (or through `pwsh tools/provision.ps1`), set `global.json` to it with `rollForward: disable`, and drop `allowPrerelease`. Done when: `dotnet --version` in the repo root prints the GA version and `pwsh tools/provision.ps1 -Verify` reports `sdk: OK`.
- [ ] Move `Microsoft.Extensions.DependencyInjection` and `Microsoft.Extensions.Hosting` in `Directory.Packages.props` to the `11.0.x` stable version matching the GA runtime (`dotnet package search Microsoft.Extensions.Hosting --exact-match`), and any other package that shipped an 11.0 stable alongside. Done when: `dotnet list Isotone.slnx package --outdated` shows no Microsoft.Extensions.* row and no prerelease version in use.
- [ ] Update the SDK version in `README.md` (badge and prerequisites), `CONTRIBUTING.md`, `AGENTS.md`, `docs/dev/build.md`, `docs/dev/README.md`, and the Directory.Packages.props comment. Done when: `grep -rn "11.0.100-rc" --include=*.md --include=*.props --include=*.json . | grep -v "^./docs/legacy/\|^./todo/"` prints nothing.
- [ ] Run `pwsh scripts/check-all.ps1` and `pwsh scripts/package.ps1 -App Stilus`, then launch the published Stilus and Gesso executables. Done when: every gate is `PASS` (table quoted) and both apps stay open 5 s.
- [ ] Commit: `"build: pin the .NET 11 GA SDK"`

**Test checkpoint:** `dotnet --version` prints the GA version with no `-rc`; `dotnet test Isotone.slnx -c Release` exits 0 with the same per-assembly counts as on the release candidate; editing `global.json` back to `11.0.100-rc.1.26425.128` on a machine without that SDK makes `dotnet build` fail naming it. Cheaper substitute that fails: `rollForward: latestFeature` on the RC pin, which silently builds on whatever SDK a machine has.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx` exits 0 three runs in a row with no quarantine
- [ ] `docs/dev/build.md` lists no debt this file retired
- [ ] `global.json` names a GA SDK (no `-rc` or `-preview`)
- [ ] `python scripts/todo-graph.py validate` clean
