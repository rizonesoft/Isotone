---
schema_version: 1
id: release-pipeline
domain: 05-release
status: draft
title: "TODO-01 -- Distribution: Clean-Machine Proof, Signing, arm64, Updates, winget, and the Suite Bundle"
depends_on: []
track: R1
---

# TODO-01 -- Distribution: Clean-Machine Proof, Signing, arm64, Updates, winget, and the Suite Bundle

> **Goal:** Every app release is proven on a machine that has never seen .NET, signed once a certificate exists, published for x64 and arm64, discoverable through winget, able to tell its user when a newer version is out, and bundled with its siblings as the Photon Graphics Suite (`photon-v1.0.0`) without any app's version moving.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The pipeline exists and has not run on GitHub: `scripts/publish.ps1` (self-contained, `-Runtime` accepts `win-arm64`), `scripts/package.ps1` (per-app and `-Suite`), `installer/common.iss` with `ArchitecturesAllowed=x64compatible`, per-app `.iss` files and `Suite.iss`, and `.github/workflows/release.yml` triggered by `nodus-v*`, `imago-v*`, `lumen-v*`, and `photon-v*` tags. A local Nodus installer was verified on 2026-09-26 (63.1 MB, silent per-user install and uninstall, per `docs/dev/build.md`). Nothing is signed: there is no certificate, and `standards/release.md` says so. Only x64 is published. No app checks for updates (Nodus's Check for Updates is a stub). No winget manifest exists. `Suite.iss` requires Nodus and Imago publishes and names Nodus's executable `Bezier.Desktop.exe`.
<!-- claim: count "ArchitecturesAllowed=x64compatible" installer/common.iss = 1 -->
<!-- claim: exists installer/Suite.iss -->
<!-- claim: count "photon-v\*" .github/workflows/release.yml = 1 -->
<!-- claim: count "signtool" scripts/package.ps1 = 0 -->

## Inputs

- [`standards/release.md`](../../standards/release.md) -- versions, artifacts, signing policy, and the release checklist
- [`docs/dev/build.md`](../../docs/dev/build.md), [`docs/dev/versioning.md`](../../docs/dev/versioning.md) -- how the scripts and tags work
- [`scripts/package.ps1`](../../scripts/package.ps1), [`scripts/publish.ps1`](../../scripts/publish.ps1), [`installer/`](../../installer/common.iss), [`.github/workflows/release.yml`](../../.github/workflows/release.yml) -- what this file extends
- -> XREF: D01 T02 §4 -- the update check lands in `Photon.Core` beside the other shared services (§4 here owns it)
- -> XREF: D02 T05 §4 -- the Nodus release that runs §1's procedure first
- -> XREF: D03 T06 §3 -- the Imago release that runs §1's procedure
- -> XREF: D04 T01 §2 -- Lumen's app creation that makes it a shipping app for §6
- -> XREF: D99 T01 §3 -- the operator step that supplies the certificate §2 needs
- -> XREF: D06 T01 §4 -- the install guide that documents what §1 proves
- -> XREF: D02 T17 §1 -- the Nodus parity releases that run §1's clean-machine procedure

## Outcome

- `docs/dev/clean-machine.md` is the procedure every app release runs, and Nodus 0.1.0 is its first quoted run.
- With a certificate supplied from outside the repository, every executable, DLL we build, installer, and uninstaller is Authenticode-signed with a timestamp, and `signtool verify /pa` passes on each.
- `win-arm64` installers and ZIPs are produced per app and by the release workflow.
- Each app's Help, Check for Updates compares its version with the latest GitHub release for its tag prefix and offers the download page, with a setting to check on startup.
- winget manifests for each released app are submitted and install the app.
- `photon-v1.0.0` publishes the suite installer and ZIP carrying Nodus, Imago, and Lumen at their current versions.

**Adjacency:** list=not-applicable (no browsable records); document=not-applicable (release notes are the changelog's); settings=applicable @ D05 T01 §4; reporting=not-applicable (no summaries); notifications=applicable; permissions=applicable; audit=applicable; exchange=not-applicable (no user formats); reverse=applicable

**Adjacency rationale:** The update check is a setting and a notification; install scope (per-user versus all-users) is the permission surface, proven on refusal (all-users without elevation); uninstall is the reverse of install; each release records its evidence in the changelog and the workflow run.

## Implementation Order

| Order | Section | Deliverable                                              | Depends On                                 | Status |
| :---: | :-----: | -------------------------------------------------------- | ------------------------------------------ | :----: |
|   1   |   §1    | The clean-machine install procedure                      | D00 T02 §7                                 |  [ ]   |
|   2   |   §2    | Sign binaries and installers                             | §1                                         |  [ ]   |
|   3   |   §3    | win-arm64 publish and installers                         | D02 T05 §4                                 |  [ ]   |
|   4   |   §4    | The update check                                         | D01 T02 §2, D02 T05 §4                     |  [ ]   |
|   5   |   §5    | winget manifests                                         | D02 T05 §4, D03 T06 §3, D04 T02 §8         |  [ ]   |
|   6   |   §6    | The suite bundle: photon-v1.0.0                          | §4, D02 T05 §4, D03 T06 §3, D04 T02 §8, D06 T01 §4 |  [ ]   |

---

## 1. The Clean-Machine Install Procedure

A developer machine has the .NET SDK and runtimes, so a self-contained publish that accidentally depends on an installed runtime passes there and fails for users. Every release is proven on a clean Windows 11 machine (a Windows Sandbox instance or a VM snapshot), and the procedure is written once so each app's release section runs the same steps. **Corrected 2026-09-26:** the supported OS is Windows 11 (23H2 or later); Windows 10 22H2 is best-effort because .NET 11 supports only its LTSC and IoT editions, so an extra Windows 10 22H2 smoke is optional and its failures are recorded, never blocking.

**Needs:** Clean Windows machine (no .NET SDK)

- [ ] Write `docs/dev/clean-machine.md`: how to get a clean Windows 11 machine (Windows Sandbox with a `.wsb` file mapping `artifacts/dist` read-only, committed as `tools/sandbox/clean-machine.wsb`), and the steps: confirm `dotnet --list-runtimes` fails, install per-user silently, launch, open a fixture, save, close, check the log for errors, uninstall, confirm the install folder and Start menu entry are gone; repeat all-users (elevated) and confirm a non-elevated all-users install is refused with the Inno Setup message; upgrade over the previous release and confirm settings survive; on Windows 10 22H2 (optional, best-effort), confirm the interactive installer shows the "not officially supported" notice and a `/VERYSILENT` install does not. Done when: the page and the `.wsb` file exist.
- [ ] Run the procedure for Nodus on the current build and quote each step. Done when: every step passes, or each failure is filed through `add-todo` with its owner.
- [ ] Commit: `"release: a written clean-machine install procedure, run for Nodus"`

**Requires:** display-session -- the Windows Sandbox session and the installer UI need an interactive desktop

**Test checkpoint:** the quoted run shows `dotnet --list-runtimes` absent, a successful per-user and all-users install, the app window, a saved fixture, an uninstall leaving no folder, and settings surviving an upgrade (a `settings.json` readback). Cheaper substitute that fails: installing on the development machine, where the runtime check cannot fail.

## 2. Sign Binaries and Installers

Unsigned installers trigger SmartScreen warnings and cannot build reputation. The operator has no certificate today (`D99 T01 §3`), so this row waits on its `Needs:` line; the plumbing is written so that supplying a certificate is the only step left. Credentials never enter the repository, arguments, or logs.

**Needs:** Signing certificate (release)

- [ ] `scripts/sign.ps1` signs a list of files with `signtool sign /fd SHA256 /tr <RFC 3161 timestamp URL> /td SHA256`, reading the certificate from the Windows certificate store by thumbprint (`PHOTON_SIGN_THUMBPRINT`) or from a cloud signing service's CLI, never from a file path in the repository. Done when: the script refuses to run without the environment variable and prints no secret.
- [ ] `scripts/package.ps1` signs the app's own executables and DLLs after publish and the installer and uninstaller through Inno Setup's `SignTool` directive in `installer/common.iss`, only when signing is configured. Done when: an unsigned build still works without the variable.
- [ ] `release.yml` signs when the repository secret is configured (the certificate stays in the signing service or an encrypted secret; the workflow never echoes it). Done when: a dry run on a prerelease tag produces signed assets.
- [ ] `signtool verify /pa /all` on every signed file is part of the release checklist in `standards/release.md`. Done when: the checklist line exists.
- [ ] Commit: `"release: sign binaries and installers when a certificate is supplied"`

**Test checkpoint:** on a prerelease tag with signing configured, `signtool verify /pa` passes for the installer, the uninstaller, and the app executable (quoted); the workflow log contains no certificate material (grep of the downloaded log for the thumbprint and `BEGIN` prints nothing). Cheaper substitute that fails: a self-signed certificate, which `verify /pa` rejects.

## 3. win-arm64 Publish and Installers

Windows on Arm machines run x64 apps under emulation, slowly. .NET 11 and WPF support `win-arm64`; SkiaSharp ships arm64 native assets. `publish.ps1` already takes `-Runtime win-arm64`; the installers and workflow do not.

**Needs:** Windows host (build/test)

- [ ] `installer/common.iss` sets `ArchitecturesAllowed` and `ArchitecturesInstallIn64BitMode` from the `Runtime` define (`x64compatible` or `arm64`). Done when: `pwsh scripts/package.ps1 -App Nodus -Runtime win-arm64` produces an arm64 installer.
- [ ] Every native dependency ships an arm64 asset (SkiaSharp, the RAW decoder, ComputeSharp's DirectX runtime); any that does not is named with its fallback. Done when: the publish folder for each app lists arm64 native DLLs (quoted).
- [ ] `release.yml` builds both runtimes and uploads both sets of assets with `SHA256SUMS` covering all. Done when: a prerelease tag produces six assets per app.
- [ ] A launch on arm64 hardware (or an arm64 VM), or, if none is available, the gap recorded with an owner through `add-todo`. Done when: one or the other is quoted.
- [ ] Commit: `"release: win-arm64 installers and ZIPs for every app"`

**Requires:** display-session -- launching the arm64 build needs an interactive desktop
**Test checkpoint:** a prerelease tag's release lists `win-x64` and `win-arm64` installers and ZIPs for the app, and `dumpbin /headers` (or `Get-PEArchitecture` via a small script) on the arm64 executable reports `AA64`. Cheaper substitute that fails: an x64 build renamed arm64, which the header check catches.

## 4. The Update Check

Users should learn a new version exists without the app phoning home silently. Each app asks GitHub for the latest release with its own tag prefix, only when the user asks or has allowed a startup check, and offers the release page; it never downloads or installs by itself. Every app needs it, so it lives in `Photon.Core`.

**Fidelity:** Help, Check for Updates and its result dialog -- new build, no baseline; captured to docs/captures/nodus/update-check/ (and the Imago and Lumen equivalents).
**Job:** a user can find out whether a newer release of the app they run exists and open its download page. Consumer: the user.
**Treatment:** `UpdateChecker` in `Photon.Core/Updates/` queries `https://api.github.com/repos/rizonesoft/Photon/releases` (unauthenticated, with a user agent naming the app and version), filters by the app's tag prefix and prerelease preference, and compares SemVer; the result dialog says "You have the latest version (x)." or "Nodus y is available (you have x). What's new: ..." with Open Download Page; a setting `Updates.CheckOnStartup` (default off, offered once on first run) and `Updates.IncludePrereleases` (default off); network failure says "Could not check for updates: <reason>." and logs a Warning. Cheaper substitute that fails the checkpoint: comparing version strings as text.
**Chrome:** consume `Photon.Core` settings and logging, the `Photon.UI` dialog shell, and the theme. Do not add a per-app update client.

**Requires:** display-session -- the update dialog needs an interactive desktop

- [ ] `UpdateChecker` with an injectable HTTP handler, SemVer comparison, prefix filtering, and a 10-second timeout. Done when: `UpdateCheckerTests` cover newer, same, older, prerelease filtering, another app's tag ignored, and network failure.
- [ ] The dialog and the Help menu item in every shipping app, replacing each app's planned stub. Done when: `MenuAuditTests` in each app pass with the item enabled.
- [ ] The two settings and the first-run offer. Done when: the startup check runs only when enabled (test).
- [ ] Commit: `"core: an opt-in update check against each app's GitHub releases"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `UpdateCheckerTests` reporting all six cases; a driven check from Nodus against the live API shows the correct result for the running version (capture and log line). Cheaper substitute that fails: text comparison, which `0.10.0` versus `0.9.0` catches.

## 5. winget Manifests

winget is how many Windows users install software. Each released app gets a manifest in `microsoft/winget-pkgs` pointing at its GitHub release installer, with silent switches and the per-user scope. Unsigned installers are accepted but may be flagged; signing (§2) is recommended first, not required.

**Needs:** Windows host (build/test)

- [ ] Author manifests with `wingetcreate new` for `Rizonesoft.Nodus`, `Rizonesoft.Imago`, and `Rizonesoft.Lumen` (installer URL, SHA-256, `InstallerType: inno`, `Scope: user` and `machine` entries, license GPL-3.0, publisher Rizonesoft), keeping copies under `installer/winget/`. Done when: `winget validate` passes on each.
- [ ] `winget install --manifest installer/winget/<App>` installs each app locally. Done when: each installs and starts (quoted).
- [ ] Submit the manifests with `wingetcreate submit` (the operator's GitHub account authorizes the fork; this runs with `gh` credentials the agent has, or is handed to the operator if not). Done when: the pull requests are open (URLs quoted), or the handoff is recorded as a `D99` row.
- [ ] A release step (script or workflow job) updates the manifests on each new app release with `wingetcreate update`. Done when: it is documented in `docs/dev/build.md`.
- [ ] Commit: `"release: winget manifests for Nodus, Imago, and Lumen"`

**Test checkpoint:** `winget validate` exits 0 for each manifest; `winget install --manifest` installs each app (quoted); the submission PR URLs are quoted. Cheaper substitute that fails: manifests never validated.

## 6. The Suite Bundle: photon-v1.0.0

The suite bundle packages all three apps in one installer and one ZIP without changing any app's version. It runs once each app has shipped its first release. The tag `photon-v1.0.0` marks the first bundle; its version is the bundle's, not an app's.

**Needs:** Clean Windows machine (no .NET SDK)

- [ ] `installer/Suite.iss` requires Lumen when Lumen ships (mirroring the Nodus and Imago checks) and its component list names each app with its own version from its latest tag. Done when: the suite installer's component page shows three apps with their versions.
- [ ] A `photon-v1.0.0` section in `CHANGELOG.md` listing the app versions the bundle carries. Done when: it exists.
- [ ] Run the clean-machine procedure for the suite installer: install all three, uninstall one component, confirm the others still run and no standalone install's registry keys were touched. Done when: every step passes (quoted).
- [ ] Push `photon-v1.0.0`; verify the workflow, the assets, and `SHA256SUMS`. Done when: all pass (URLs and hashes quoted).
- [ ] Commit: `"release: the Photon Graphics Suite 1.0.0 bundle"`

**Requires:** display-session -- the suite installer's component page and the app launches need an interactive desktop

**Test checkpoint:** `gh release view photon-v1.0.0 --json assets` lists the suite installer, ZIP, and checksums; the clean-machine run shows three apps installed side by side with their own versions in their About dialogs. Cheaper substitute that fails: a bundle that re-versions every app to 1.0.0, which the About dialogs catch.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0
- [ ] Every app release since this file shipped has a quoted clean-machine run
- [ ] `signtool verify /pa` passes on every asset once signing is configured
- [ ] `python scripts/todo-graph.py validate` clean
