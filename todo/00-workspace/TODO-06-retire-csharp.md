---
schema_version: 1
id: retire-csharp
domain: 00-workspace
status: draft
title: "TODO-06 -- Retire the C# Code and the .NET Toolchain"
depends_on: []
track: W6
---

# TODO-06 -- Retire the C# Code and the .NET Toolchain

> **Goal:** The repository holds no C#, XAML, .NET build, NuGet, MinVer, WPF, AvalonDock, SkiaSharp, or WinUI code or configuration, and nothing it runs still expects them: the last C# commit is tagged `csharp-final` so the imported apps stay readable as a behavior reference, `src/` and the .NET build files are gone, every gate, workflow, automation, script, skill, and root document that drove the .NET build is removed or retargeted to the native build, and a gate fails if managed code comes back. The unattended campaign keeps running through the removal: the sections run in the order that keeps every gate green on every commit (first retarget the gates that read the C# sources, then retire the .NET automations, and only then delete the code), so no commit hook refuses, no gate is left empty, and no scheduled job turns red because its subject disappeared.

> [!IMPORTANT]
> **Current state (verified 2026-10-23):** The operator decided on 2026-10-23 to remove all C# in the first campaign section that can do it safely ("leave a clean repo, so clean out all the C# and WinUI3 stuff" and "Without breaking the unattended run"; `docs/dev/decisions.md`, "2026-10-23: The unattended campaign"), replacing the spec's rule that each C# tree retires at its native app's first release. Measured that day: 252 tracked `.cs`, `.xaml`, and `.csproj` files under `src/Stilus/` and `src/Gesso/` (for example `src/Stilus/Bezier.Core/Bezier.Core.csproj`); the root .NET files `Isotone.slnx`, `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, and `nuget.config`; .NET steps in `.github/workflows/build.yml`, `release.yml`, and `pins.yml`; a NuGet ecosystem in `.github/dependabot.yml`; and .NET references in `scripts/` (`_common.ps1`, `apps.psd1`, `build.ps1`, `publish.ps1`, `package.ps1`, `check-all.ps1`, `check-dotnet-pin.py`, `check-vulnerable-packages.py`, `check-local-tools.py`, whose SDK branch reads `global.json` unconditionally, `design-lint.py`, `merge_prs.py`, `panel_slots.py`, `todo-claims.py`, `todo-graph.py`, `weakening-scan.py`, and the tests `test_build_props.py`, `test_merge_prs.py`, `test_pin_automations.py`), in `.conclave/automations/` (`README.md`, `alert.py`), in `.claude/` (two agent definitions and five skill files), in `installer/common.iss`, `tools/provision.ps1`, `.editorconfig`, `.gitattributes`, `.gitignore`, `resources/icons/README.md`, and in `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`. The repository holds no WinUI 3 code; WinUI is only mentioned in `.conclave/automations/README.md` and `scripts/tests/test_pin_automations.py`. `docs/design/.lint-baseline.json` records 2046 design-lint findings, all in the C# and XAML sources, so deleting them first would leave 1,479 stale baseline entries that the commit hook refuses. 378 claim comments in `todo/` name paths under `src/`, all in files parked for the re-plan, and `scripts/todo-claims.py` holds an absolute coverage floor of 78 blocks. `LICENSE-EXCEPTION.md` exists only for AvalonDock. The standards under `standards/` and the developer docs under `docs/dev/` are rewritten for C++ by `D00 T07 §2`, not here, so they are outside this file's checks.
<!-- claim: exists Isotone.slnx -->
<!-- claim: exists global.json -->
<!-- claim: exists Directory.Packages.props -->
<!-- claim: exists nuget.config -->
<!-- claim: exists LICENSE-EXCEPTION.md -->
<!-- claim: exists scripts/check-dotnet-pin.py -->
<!-- claim: exists scripts/check-vulnerable-packages.py -->
<!-- claim: exists scripts/tests/test_build_props.py -->
<!-- claim: exists src/Stilus/Bezier.Core/Bezier.Core.csproj -->
<!-- claim: count "global.json" scripts/check-local-tools.py = 4 -->
<!-- claim: count "COVERAGE_FLOOR = 78" scripts/todo-claims.py = 1 -->
<!-- claim: count "nuget" .github/dependabot.yml = 2 -->

## Inputs

- [`docs/dev/decisions.md`](../../docs/dev/decisions.md) "2026-10-23: The unattended campaign" -- the removal decision and its tag
- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md) "The repository during the move" and "Dependencies and their upkeep" (the AvalonDock exception's retirement) -- what this file replaces and what it retires
- [`docs/plans/2026-10-23-native-replan.md`](../../docs/plans/2026-10-23-native-replan.md) -- the parking rule §1's claims change follows
- -> XREF: D00 T05 §8 -- the native CI job must be green before the .NET jobs go, so CI never builds nothing
- -> XREF: D00 T07 §1 -- the workspace re-plan supersedes the .NET build and test debt list and rewrites the repository-layout file against the tree this file leaves

## Outcome

- `git ls-files "*.cs" "*.csproj" "*.xaml" "*.sln" "*.slnx" "*.props" "*.targets" "*.runsettings" global.json nuget.config` prints nothing, and the annotated tag `csharp-final` on `origin` names the last commit that held them.
- `pwsh scripts/check-all.ps1`, every workflow, every scheduled automation, and the commit hooks run green with no .NET step on every commit this file makes, and `native-deps-lint` fails `managed-source` if a C#, XAML, or .NET project file is added.
- Outside the history records (`CHANGELOG.md`, `docs/dev/decisions.md`, `docs/legacy/`, `docs/reviews/`, `docs/phase-runs/`, `docs/specs/`, `docs/captures/`), the standards, developer docs, and design-system implementation notes `D00 T07 §2` rewrites (`standards/`, `docs/dev/`, `docs/design/`), and `todo/` (whose files are parked for the re-plan or name the retired stack only as migration instructions, as this file does), no tracked file names .NET, NuGet, MinVer, WPF, XAML, AvalonDock, SkiaSharp, or WinUI as something the repository uses.

**Adjacency:** all=not-applicable (removing a retired toolchain and its gates: no records, settings, documents, or surfaces a user sees)

**Adjacency rationale:** No shipped app or user-visible surface changes: the C# apps never shipped, and the native apps that replace them are built by later sections.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Retarget the gates that read the C# sources | D00 T05 §8, D00 T04 §1 |  [ ]   |
|   2   |   §2    | Retire the .NET release path, pins, Dependabot ecosystem, and automations | §1, D00 T04 §3 |  [ ]   |
|   3   |   §3    | Tag csharp-final, remove the C# trees and the .NET build, and guard against managed code | §2, D00 T05 §10 |  [ ]   |

---

## 1. Retarget the Gates That Read the C# Sources

The claims gate and design-lint read the C# sources, and the commit hook runs design-lint, so they move off those sources while the sources still exist; deleting first would make the hook refuse the deleting commit. Nothing is deleted here.

- [ ] Make `scripts/todo-claims.py` defer the claims of a file whose status is `blocked` or `superseded` (deferred, as `query ready` and `query plan` treat it): it does not re-measure them and reports them as `deferred` in its totals, while a deferred file's claims still count toward coverage, because coverage measures that a Current state block is recorded as claims, not that the claims were re-measured today; the absolute floor (`COVERAGE_FLOOR`, 78) is unchanged and keeps holding over the whole tree. Add self-test cases: a parked file with a claim naming a missing path passes and is reported deferred; the same file unparked fails; coverage is unchanged by deferral. Done when: `python scripts/todo-claims.py` exits 0 with the coverage it had before, a probe that removes a parked file's target path still passes, and mutants that re-measure deferred claims or stop counting them toward coverage each fail the self-test. Cheaper substitute that fails: lowering the floor to the eligible files, which the rules forbid.
- [ ] Retarget `scripts/design-lint.py` to the native sources: scan every C and C++ source and header under `native/` (`.c`, `.cc`, `.cpp`, `.cxx`, `.c++`, `.h`, `.hh`, `.hpp`, `.hxx`, `.h++`, `.inl`, `.ipp`, the extensions CMake compiles as C and C++ plus included implementation files) instead of the C# and XAML sources, keep its output format, and write an empty `docs/design/.lint-baseline.json` in the same commit, because every recorded finding is in sources the lint no longer scans. Done when: `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` prints `0 error(s) ... 0 new, 0 stale` and the commit hook passes on this commit.
- [ ] Give design-lint its C++ rules in the same section, so the gate holds the native UI to `docs/design/` before the first foundation draws anything (`standards/design-contract.md`: a surface never hardcodes a value its theme names): in UI sources (`native/ui/` and each app's UI folders), a literal color (`D2D1::ColorF` or `D2D1_COLOR_F` built from numbers, `RGB(`, `ColorF::` named colors, and 6- or 8-digit hex color literals), literal geometry (`D2D1::RectF`, `SizeF`, `Point2F`, `RoundedRect`, or a corner radius, stroke width, padding, margin, or spacing built from numeric literals other than 0), and a literal font family or size each fail, while a value read from the generated token tables passes; with self-test fixtures failing on each literal kind and passing on the token form. Done when: probes of a literal `D2D1::ColorF(0.2f, 0.4f, 0.8f)` in a `.cpp` file, `D2D1::RectF(0, 0, 24, 24)` in a `.cc` file, and `D2D1::ColorF(D2D1::ColorF::Red)` in an `.inl` file, all in `native/ui/`, each fail the lint (quoted, then removed), and its self-test covers each extension.
- [ ] Commit: `"build(workspace): defer parked claims and retarget design-lint to the native sources"`

**Test checkpoint:** Driven run with evidence: `python scripts/todo-claims.py` exits 0 reporting the parked claims as deferred and the same coverage as before this section (both totals quoted); `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` prints `0 new, 0 stale` (quoted); the commit hook passes (its output quoted). Unit test: the self-tests of both scripts pass, and the named mutants fail them. Cheaper substitute that fails: deleting the claims that point into `src/`, which erases the parked files' record of what they assumed.

## 2. Retire the .NET Release Path, Pins, Dependabot Ecosystem, and Automations

The .NET SDK pin, the NuGet advisory check, NuGet Dependabot updates, the local SDK check, and the .NET publish and package scripts would otherwise keep running on schedules and fail, or open pull requests, the moment the .NET files go, which breaks an unattended run without any section having failed. They are retired while `global.json` still exists.

- [ ] Remove the NuGet ecosystem from `.github/dependabot.yml`, keeping `github-actions`. Done when: the file names no `nuget`.
- [ ] Remove the .NET SDK pin and NuGet advisory jobs from `.github/workflows/pins.yml`, delete `scripts/check-dotnet-pin.py` and `scripts/check-vulnerable-packages.py`, and remove their cases from `scripts/tests/test_pin_automations.py`. Done when: `pins.yml` keeps the native advisory job `D00 T04 §3` added (this section depends on it, so the workflow never has zero jobs), names no `dotnet`, and runs green on dispatch (`python scripts/ci_watch.py --dispatch pins.yml`).
- [ ] Remove the SDK branch of `scripts/check-local-tools.py` (its `global.json` read and `dotnet --list-sdks` check) with its fixtures and test cases, keeping the CLI and Python checks; keep `scripts/lib/pin_proposal.py` and `scripts/lib/pin_sources.py` only if a remaining script imports them, else delete them. Done when: `python scripts/check-local-tools.py check` passes on a scratch copy of the tree without `global.json`, and its tests pass.
- [ ] Update `scripts/merge_prs.py` and `scripts/tests/test_merge_prs.py`: remove the .NET SDK pin exclusion and the NuGet pull-request handling, keeping GitHub Actions updates and any native pin pull requests. Done when: `python scripts/tests/test_merge_prs.py` passes and the merger's rules name no .NET case.
- [ ] Remove every .NET task from `.conclave/automations/tasks.json` and its README, and the .NET and WinUI references in `.conclave/automations/README.md` and `alert.py`; run `python scripts/tests/test_automations.py`. Done when: the test passes and the README names no .NET or WinUI job.
- [ ] Remove the .NET publish and package logic from `scripts/publish.ps1`, `scripts/package.ps1`, `scripts/build.ps1`, `scripts/_common.ps1`, and `scripts/apps.psd1`: each script that has no native work yet exits 1 with the message naming the section that will give it native work (the release re-plan in `D00 T07`), and `apps.psd1` keeps each app's name, slug, and tag prefix without .NET project paths. Remove the .NET job from `.github/workflows/release.yml`, leaving a job that fails with the same message on a tag push (no tag is pushed before the release re-plan lands). Remove the .NET runtime and publish-folder lines from `installer/common.iss`. Done when: none of these files names `dotnet`, `.csproj`, or MinVer.
- [ ] Retire the AvalonDock exception, as the spec assigns to the section that removes the last C# app: delete `LICENSE-EXCEPTION.md`, remove every reference to it (`AGENTS.md`, `README.md`, `scripts/publish.ps1`, `standards/release.md`, notices), and record in `docs/dev/decisions.md`, under the 2026-10-19 license decision or as a new entry if none exists, its retirement on this date with the reason. Done when: `git grep -n "LICENSE-EXCEPTION"` prints only history records.
- [ ] Commit: `"build(workspace): retire the .NET release path, pins, Dependabot ecosystem, and automations"`

**Test checkpoint:** Driven run with evidence: `python scripts/ci_watch.py --dispatch pins.yml` exits 0 and `python scripts/ci_watch.py` reports no red workflow (both quoted); `python scripts/tests/test_pin_automations.py`, `test_merge_prs.py`, and `test_automations.py` pass, and `check-local-tools.py check` passes without `global.json` on a scratch copy (quoted); `git grep -n -i -E "dotnet|nuget|minver" -- .github scripts .conclave installer` prints only the .NET build steps §3 removes (`build.yml`, `check-all.ps1`, and `test_build_props.py`), listed and quoted. Cheaper substitute that fails: leaving the .NET pin job scheduled, which fails every night once `global.json` is gone and stalls the campaign's pull-request merger.

## 3. Tag csharp-final, Remove the C# Trees and the .NET Build, and Guard Against Managed Code

With the gates retargeted (§1) and the automations retired (§2), the code and the .NET build can go in one commit with nothing left to fail. The C# apps remain readable through the tag as the behavior reference the re-plan cites.

- [ ] Confirm the starting line: `git status --short` is empty, `HEAD` equals `origin/main`, the latest CI run on `main` shows the native job green, and `python scripts/ci_watch.py` reports no red workflow. Done when: all three are quoted in the commit message.
- [ ] Create the annotated tag `csharp-final` on `HEAD` with the message "Last commit holding the imported C# Stilus and Gesso; behavior reference for the native rewrite (docs/dev/decisions.md, 2026-10-23)" and push it. Done when: `git ls-remote --tags origin csharp-final` prints it.
- [ ] Add a "Reading the C# reference" paragraph beside the native toolchain paragraph of `D00 T05 §1` in `docs/dev/`: `git show csharp-final:<path>`, `git worktree add ../isotone-csharp csharp-final`, and that re-plan and build sections cite reference behavior as `csharp-final:<path>`. Done when: the paragraph names the tag and both commands.
- [ ] Remove `src/Stilus/`, `src/Gesso/`, `Isotone.slnx`, `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `nuget.config`, and `tests/Isotone.runsettings` with `git rm -r`. Done when: the Outcome's `git ls-files` command prints nothing.
- [ ] Remove the .NET stages from `scripts/check-all.ps1` (`build Debug`, `build Release`, `test`, the `test_build_props.py` gate, and the .NET meaning of `-SkipBuild`) and its header list, and delete `scripts/tests/test_build_props.py`; remove the .NET steps and setup (`actions/setup-dotnet`, `dotnet` commands, NuGet caches) from `.github/workflows/build.yml`, keeping the native jobs. Done when: `pwsh scripts/check-all.ps1` exits 0 and names no `dotnet` command, and `git grep -n -i "dotnet" .github/workflows/build.yml` prints nothing.
- [ ] Remove the .NET entries from `.editorconfig` (C# and XAML sections), `.gitattributes` (`*.cs`, `*.csproj`, `*.xaml`, `*.slnx`, `*.props`), and `.gitignore` (`bin/`, `obj/`, `*.user`, keeping `artifacts/` and `build/`), adding C and C++ entries to `.editorconfig` and `.gitattributes` that match `native/.clang-format`. Done when: none of the three files names a .NET file type.
- [ ] Remove the .NET references from `scripts/todo-graph.py`, `scripts/weakening-scan.py`, and `scripts/panel_slots.py` (allowed commands, examples, and fixtures naming `dotnet`), replacing them with the native commands where a command is needed, and run each self-test. Done when: each self-test passes and `git grep -n -i "dotnet" scripts/` prints nothing.
- [ ] Update `.claude/agents/isotone-researcher.md`, `.claude/agents/mutation-tester.md`, and the skills `create-todo` (template), `groom-plan`, `plan-new-feature`, `process-todo-file`, and `process-todo-section` (including `gates.md`) to the native commands and proofs of `D00 T05 §10`. Done when: `git grep -n -i -E "dotnet|xunit|\.slnx" .claude/` prints nothing and `python scripts/panel_slots.py validate` passes.
- [ ] Update `AGENTS.md` (the .NET, WPF, CommunityToolkit.Mvvm, Microsoft.Extensions.DependencyInjection, Serilog, and xUnit bullets replaced by the native stack's equivalents from the spec, the path table's `src/` rows, and the Validation block), `README.md`, `CONTRIBUTING.md`, `tools/provision.ps1`, and `resources/icons/README.md`, so each describes only the native build. Done when: `git grep -n -i -E "dotnet|wpf|xaml|nuget|minver|avalondock|skiasharp|winui" -- AGENTS.md README.md CONTRIBUTING.md tools resources` prints nothing.
- [ ] Add the rule `managed-source` to `scripts/native-deps-lint.py` (`D00 T04 §1`): any tracked `.cs`, `.csproj`, `.xaml`, `.slnx`, `.sln`, `.props`, `.targets`, `.runsettings`, `.ruleset`, `.nuspec`, `global.json`, `nuget.config`, or `packages.lock.json` fails, with a self-test case. Done when: a probe `src/Probe.cs` fails the lint (quoted, then removed).
- [ ] Mark the supersession map rows this file settles: the .NET build and test debt list (`D00 T02`, superseded by this file and `D00 T05`) and the build, release, and pin rows `D00 T07 §1` classifies. Done when: `todo/supersession-2026-10.md` names this file for each.
- [ ] Verify the tag by its peeled commit, not only its name: `git rev-parse csharp-final^{commit}` equals the verified pre-removal HEAD this section recorded, and the reference assets the native rewrite reads (the C# sources, test fixtures, and captures) are all reachable from it (D00-T05-S1-PR11). Done when: both checks are quoted in the commit body. -> SOURCE: plan-review-D00-T05-s1-2026-10-23-pr11 D00-T05-S1-PR11
- [ ] Commit: `"build(workspace): tag csharp-final, remove the C# code and the .NET build, and guard against managed code"`

**Test checkpoint:** Driven run with evidence: `git ls-remote --tags origin csharp-final` prints the tag; `git show csharp-final:src/Stilus/Bezier.Core/Bezier.Core.csproj` prints the old project's first lines; the Outcome's `git ls-files` command prints nothing; `pwsh scripts/check-all.ps1` exits 0 with every native stage PASS and no .NET stage (summary quoted); the CI run for this commit is green and `python scripts/ci_watch.py` reports no red workflow (run id and line quoted); a probe `src/Probe.cs` makes `native-deps-lint` fail with `managed-source` (quoted, then removed). Static evidence: the Outcome's stack `git grep` over the repository, outside the history records, `standards/`, `docs/dev/`, `docs/design/`, and `todo/`, prints nothing (command, with its exclusions as pathspecs, and empty output quoted). Cheaper substitute that fails: deleting `src/` without a tag, which loses the behavior reference the re-plan cites.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0 with no .NET stage
- [ ] `git ls-files "*.cs" "*.csproj" "*.xaml" "*.sln" "*.slnx" "*.props" "*.targets" "*.runsettings" global.json nuget.config` prints nothing, and `csharp-final` is on `origin`
- [ ] `python scripts/ci_watch.py` reports no red workflow on `main`
- [ ] `python scripts/todo-graph.py validate` clean
