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

> **Goal:** The repository holds no C#, XAML, .NET build, NuGet, MinVer, WPF, AvalonDock, SkiaSharp, or WinUI code or configuration, and nothing it runs still expects them: the last C# commit is tagged `csharp-final` so the imported apps stay readable as a behavior reference, `src/` and the .NET build files are gone, every gate, workflow, automation, script, skill, and document that drove the .NET build is removed or retargeted to the native build, and a gate fails if managed code comes back. The unattended campaign keeps running through the removal: no gate is left empty and no check goes red because its subject disappeared.

> [!IMPORTANT]
> **Current state (verified 2026-10-23):** The operator decided on 2026-10-23 to remove all C# in the first campaign section that can do it safely ("leave a clean repo, so clean out all the C# and WinUI3 stuff" and "Without breaking the unattended run"; `docs/dev/decisions.md`, "2026-10-23: The unattended campaign"), replacing the spec's rule that each C# tree retires at its native app's first release. Measured that day: 252 tracked `.cs`, `.xaml`, and `.csproj` files under `src/Stilus/` and `src/Gesso/`; the root .NET files `Isotone.slnx`, `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, and `nuget.config`; .NET steps in `.github/workflows/build.yml`, `release.yml`, and `pins.yml`; a NuGet ecosystem in `.github/dependabot.yml`; and .NET references in `scripts/` (`_common.ps1`, `apps.psd1`, `build.ps1`, `publish.ps1`, `package.ps1`, `check-all.ps1`, `check-dotnet-pin.py`, `check-vulnerable-packages.py`, `check-local-tools.py`, `design-lint.py`, `merge_prs.py`, `panel_slots.py`, `todo-claims.py`, `todo-graph.py`, `weakening-scan.py`, and the tests `test_build_props.py`, `test_merge_prs.py`, `test_pin_automations.py`), in `.conclave/automations/` (`README.md`, `alert.py`), in `.claude/` (two agent definitions and five skill files), in `installer/common.iss`, `tools/provision.ps1`, `.editorconfig`, `.gitattributes`, `.gitignore`, `resources/icons/README.md`, and in `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`. The repository holds no WinUI 3 code; WinUI is only mentioned in `.conclave/automations/README.md` and `scripts/tests/test_pin_automations.py`. `docs/design/.lint-baseline.json` records 2046 design-lint findings, all in the C# and XAML sources. 378 claim comments in `todo/` name paths under `src/`, all in files parked for the re-plan. `LICENSE-EXCEPTION.md` exists only for AvalonDock. The standards under `standards/` and the developer docs under `docs/dev/` are rewritten for C++ by `D00 T07 §2`, not here.
<!-- claim: exists Isotone.slnx -->
<!-- claim: exists global.json -->
<!-- claim: exists Directory.Packages.props -->
<!-- claim: exists nuget.config -->
<!-- claim: exists LICENSE-EXCEPTION.md -->
<!-- claim: exists scripts/check-dotnet-pin.py -->
<!-- claim: exists scripts/check-vulnerable-packages.py -->
<!-- claim: exists scripts/tests/test_build_props.py -->
<!-- claim: count "nuget" .github/dependabot.yml = 2 -->

## Inputs

- [`docs/dev/decisions.md`](../../docs/dev/decisions.md) "2026-10-23: The unattended campaign" -- the removal decision and its tag
- [`docs/specs/2026-10-22-native-stack-design.md`](../../docs/specs/2026-10-22-native-stack-design.md) "The repository during the move" and "Dependencies and their upkeep" (the AvalonDock exception's retirement) -- what this file replaces and what it retires
- [`docs/plans/2026-10-23-native-replan.md`](../../docs/plans/2026-10-23-native-replan.md) -- the parking rule §3's claims change follows
- -> XREF: D00 T05 §8 -- the native CI job must be green before the .NET jobs go, so CI never builds nothing
- -> XREF: D00 T07 §1 -- the workspace re-plan supersedes the .NET build and test debt list and rewrites the repository-layout file against the tree this file leaves

## Outcome

- `git ls-files "*.cs" "*.csproj" "*.xaml" "*.slnx" "*.props" "*.targets" global.json nuget.config` prints nothing, and the annotated tag `csharp-final` on `origin` names the last commit that held them.
- `pwsh scripts/check-all.ps1`, every workflow, every scheduled automation, and the commit hooks run green with no .NET step, and `native-deps-lint` fails `managed-source` if a C#, XAML, or .NET project file is added.
- Outside the history records (`CHANGELOG.md`, `docs/dev/decisions.md`, `docs/legacy/`, `docs/reviews/`, `docs/phase-runs/`, `docs/specs/`, `docs/captures/`) and the parked TODO files the re-plan rewrites, no tracked file names .NET, NuGet, MinVer, WPF, XAML, AvalonDock, SkiaSharp, or WinUI as something the repository uses.

**Adjacency:** all=not-applicable (removing a retired toolchain and its gates: no records, settings, documents, or surfaces a user sees)

**Adjacency rationale:** No shipped app or user-visible surface changes: the C# apps never shipped, and the native apps that replace them are built by later sections.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Tag csharp-final and remove the C# trees and the .NET build | D00 T05 §8, D00 T04 §1 |  [ ]   |
|   2   |   §2    | Retire the .NET release path, pins, Dependabot ecosystem, and automations | §1 |  [ ]   |
|   3   |   §3    | Retarget the tooling, agents, skills, and root documents, and guard against managed code | §2 |  [ ]   |

---

## 1. Tag csharp-final and Remove the C# Trees and the .NET Build

The C# apps are a behavior reference, never extended (spec), so they remain readable through a tag rather than through a tree every gate must still build. The native gates exist by now (`D00 T05 §7`, `§8`), so removing the .NET stages leaves the runner and CI with real work.

- [ ] Confirm the starting line: `git status --short` is empty and `HEAD` equals `origin/main`; the latest CI run on `main` shows the native job green (`gh run list --workflow build.yml --branch main --limit 1`). Done when: both are quoted in the commit message. Cheaper substitute that fails: removing code while CI's native job has never passed, which leaves CI building nothing.
- [ ] Create the annotated tag `csharp-final` on `HEAD` with the message "Last commit holding the imported C# Stilus and Gesso; behavior reference for the native rewrite (docs/dev/decisions.md, 2026-10-23)" and push it. Done when: `git ls-remote --tags origin csharp-final` prints it.
- [ ] Add a "Reading the C# reference" paragraph to `docs/dev/` (where the native toolchain paragraph of `D00 T05 §1` lives): `git show csharp-final:<path>`, `git worktree add ../isotone-csharp csharp-final`, and that re-plan and build sections cite reference behavior as `csharp-final:<path>`. Done when: the paragraph names the tag and both commands.
- [ ] Remove `src/Stilus/`, `src/Gesso/`, `Isotone.slnx`, `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, and `nuget.config` with `git rm -r`. Done when: the Outcome's `git ls-files` command prints nothing.
- [ ] Remove the .NET stages from `scripts/check-all.ps1` (`build Debug`, `build Release`, `test`, the `test_build_props.py` gate, and the `-SkipBuild` switch's .NET meaning) and its header list, and delete `scripts/tests/test_build_props.py`. Done when: `pwsh scripts/check-all.ps1` exits 0 and names no `dotnet` command.
- [ ] Remove the .NET steps and setup (`actions/setup-dotnet`, `dotnet` commands, NuGet caches) from `.github/workflows/build.yml`, keeping the native jobs. Done when: `git grep -n -i "dotnet" .github/workflows/build.yml` prints nothing and a push's run is green.
- [ ] Remove the .NET entries from `.editorconfig` (C# and XAML sections), `.gitattributes` (`*.cs`, `*.csproj`, `*.xaml`, `*.slnx`, `*.props`), and `.gitignore` (`bin/`, `obj/`, `*.user` .NET entries, keeping `artifacts/` and `build/`), adding C and C++ entries to `.editorconfig` and `.gitattributes` that match `native/.clang-format`. Done when: none of the three files names a .NET file type.
- [ ] Commit: `"build(workspace): tag csharp-final and remove the C# trees and the .NET build"`

**Test checkpoint:** Driven run with evidence: `git ls-remote --tags origin csharp-final` prints the tag (quoted); `git ls-files "*.cs" "*.csproj" "*.xaml" "*.slnx" "*.props" "*.targets" global.json nuget.config` prints nothing; `git show csharp-final:src/Stilus/Bezier.sln` prints the old solution's first lines (quoted); `pwsh scripts/check-all.ps1` exits 0 with every native stage PASS and no .NET stage listed (summary quoted); the CI run for this commit is green (run id quoted). Cheaper substitute that fails: deleting `src/` without a tag, which loses the behavior reference the re-plan cites.

## 2. Retire the .NET Release Path, Pins, Dependabot Ecosystem, and Automations

The .NET SDK pin, the NuGet advisory check, NuGet Dependabot updates, and the .NET publish and package scripts would otherwise keep running on schedules and fail, or open pull requests, against code that no longer exists, which breaks an unattended run without any section having failed.

- [ ] Remove the NuGet ecosystem from `.github/dependabot.yml`, keeping `github-actions`. Done when: the file names no `nuget`.
- [ ] Remove the .NET SDK pin and NuGet advisory jobs from `.github/workflows/pins.yml`, delete `scripts/check-dotnet-pin.py` and `scripts/check-vulnerable-packages.py`, and remove their cases from `scripts/tests/test_pin_automations.py`; keep `scripts/lib/pin_proposal.py` and `scripts/lib/pin_sources.py` only if `scripts/check-local-tools.py` still imports them, else delete them. Done when: `pins.yml` runs green on dispatch, names no `dotnet`, and keeps the native advisory step of `D00 T04 §3` if that section has landed.
- [ ] Update `scripts/merge_prs.py` and `scripts/tests/test_merge_prs.py`: remove the .NET SDK pin exclusion and the NuGet pull-request handling, keeping GitHub Actions updates and any native pin pull requests. Done when: `python scripts/tests/test_merge_prs.py` passes and `merge_prs.py run --dry-run` (or its equivalent read-only mode) lists no .NET rule.
- [ ] Remove every .NET task from `.conclave/automations/tasks.json` and its README, and the .NET and WinUI references in `.conclave/automations/README.md` and `alert.py`; run `python scripts/tests/test_automations.py`. Done when: the test passes and the README names no .NET or WinUI job.
- [ ] Remove the .NET publish and package logic from `scripts/publish.ps1`, `scripts/package.ps1`, `scripts/build.ps1`, `scripts/_common.ps1`, and `scripts/apps.psd1`: each script that has no native work yet exits 1 with the message naming the section that will give it native work (the release re-plan in `D00 T07`), and `apps.psd1` keeps each app's name, slug, and tag prefix without .NET project paths. Remove the .NET job from `.github/workflows/release.yml`, leaving a job that fails with the same message on a tag push (no tag is pushed before the release re-plan lands). Remove the .NET runtime and publish-folder lines from `installer/common.iss`. Done when: none of these files names `dotnet`, `.csproj`, or MinVer.
- [ ] Retire the AvalonDock exception, as the spec assigns to the section that removes the last C# app: delete `LICENSE-EXCEPTION.md`, remove every reference to it (`AGENTS.md`, `README.md`, `scripts/publish.ps1`, `standards/release.md`, notices), and add to `docs/dev/decisions.md` under the 2026-10-19 license decision, or as a new entry if none exists, a line recording its retirement on this date with the reason. Done when: `git grep -n "LICENSE-EXCEPTION"` prints only history records.
- [ ] Commit: `"build(workspace): retire the .NET release path, pins, Dependabot ecosystem, and automations"`

**Test checkpoint:** Driven run with evidence: dispatched runs of `pins.yml` and `build.yml` are green (run ids quoted); `python scripts/tests/test_pin_automations.py`, `test_merge_prs.py`, and `test_automations.py` pass; `git grep -n -i -E "dotnet|nuget|minver" -- .github scripts .conclave installer` prints nothing (quoted). Cheaper substitute that fails: leaving the .NET pin job scheduled, which fails every night once `global.json` is gone and stalls the campaign's pull-request merger.

## 3. Retarget the Tooling, Agents, Skills, and Root Documents, and Guard Against Managed Code

The TODO tooling, the design lint, the delegate agents, the skills, and the root documents still name the .NET build. The claims in parked files point into the removed `src/`, and they must not turn the claims gate red: a parked file's sections are deferred, and its Current state is re-measured by the re-plan section that rewrites it.

- [ ] Make `scripts/todo-claims.py` skip the claims of a file whose status is `blocked` or `superseded` (deferred, as `query ready` and `query plan` treat it), reporting them as `deferred` in its totals, with self-test cases for both statuses; its coverage floor counts only files that are neither. Done when: `python scripts/todo-claims.py` exits 0 with the removed `src/` and reports the parked files' claims as deferred, and a mutant that checks deferred claims fails the self-test.
- [ ] Retarget `scripts/design-lint.py` to the native sources: scan `native/**/*.{h,hpp,cpp}` instead of the C# and XAML sources, keep its rule set and output format, and write an empty `docs/design/.lint-baseline.json`, because every recorded finding was in removed files; the C++ literal rules arrive with the UI toolkit's re-plan (`D00 T07`). Done when: `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` prints `0 error(s) ... 0 new, 0 stale`, its self-test passes, and the commit hook passes.
- [ ] Remove the .NET references from `scripts/todo-graph.py`, `scripts/weakening-scan.py`, and `scripts/panel_slots.py` (allowed commands, examples, and fixtures naming `dotnet`), replacing them with the native commands where a command is needed, and run each self-test. Done when: each self-test passes and `git grep -n -i "dotnet" scripts/` prints nothing.
- [ ] Update `.claude/agents/isotone-researcher.md`, `.claude/agents/mutation-tester.md`, and the skills `create-todo` (template), `groom-plan`, `plan-new-feature`, `process-todo-file`, and `process-todo-section` (including `gates.md`) to the native commands and proofs of `D00 T05 §10`. Done when: `git grep -n -i -E "dotnet|xunit|\.slnx" .claude/` prints nothing and `python scripts/panel_slots.py validate` passes.
- [ ] Update `AGENTS.md` (the .NET, WPF, CommunityToolkit.Mvvm, Microsoft.Extensions.DependencyInjection, Serilog, and xUnit bullets replaced by the native stack's equivalents from the spec, the path table's `src/` rows, and the Validation block), `README.md`, `CONTRIBUTING.md`, `tools/provision.ps1`, and `resources/icons/README.md`, so each describes only the native build. Done when: `git grep -n -i -E "dotnet|wpf|xaml|nuget|minver|avalondock|skiasharp|winui" -- AGENTS.md README.md CONTRIBUTING.md tools resources` prints nothing.
- [ ] Add the rule `managed-source` to `scripts/native-deps-lint.py` (`D00 T04 §1`): any tracked `.cs`, `.csproj`, `.xaml`, `.slnx`, `.sln`, `.props`, `.targets`, `global.json`, or `nuget.config` fails, with a self-test case. Done when: a probe `src/Probe.cs` fails the lint (quoted, then removed).
- [ ] Mark the supersession map rows this file settles: `D00 T02` (the .NET debt list, superseded by this file and `D00 T05`) and the build, release, and pin rows named by `D00 T07 §1`'s classification. Done when: `todo/supersession-2026-10.md` names this file for each.
- [ ] Commit: `"build(workspace): retarget the tooling to the native build and guard against managed code"`

**Test checkpoint:** Static evidence: the Outcome's `git grep` over the repository outside the history records and parked TODO files prints nothing (command and empty output quoted). Driven run with evidence: `pwsh scripts/check-all.ps1` exits 0 (summary quoted); `python scripts/todo-claims.py` reports the parked claims as deferred and exits 0; a probe `src/Probe.cs` makes `native-deps-lint` fail with `managed-source` (quoted, then removed); the commit hook passes on this commit. Cheaper substitute that fails: deleting the claims that point into `src/`, which erases the parked files' record of what they assumed.

## Verification

- [ ] `pwsh scripts/check-all.ps1` exits 0 with no .NET stage
- [ ] `git ls-files "*.cs" "*.csproj" "*.xaml" "*.slnx" "*.props" "*.targets" global.json nuget.config` prints nothing, and `csharp-final` is on `origin`
- [ ] The latest runs of `build.yml` and `pins.yml` on `main` are green
- [ ] `python scripts/todo-graph.py validate` clean
