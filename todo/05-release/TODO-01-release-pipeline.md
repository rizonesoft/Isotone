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

> **Goal:** Every app release is proven on a machine that has never seen .NET, signed once a certificate exists, published for x64 and arm64, discoverable through winget, able to tell its user when a newer version is out, and bundled with its siblings as the Isotone Graphics Suite (`isotone-v1.0.0`, then `isotone-v1.1.0` after the post-release phases 42 to 45) without any app's version moving.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The pipeline exists and has not run on GitHub: `scripts/publish.ps1` (self-contained, `-Runtime` accepts `win-arm64`), `scripts/package.ps1` (per-app and `-Suite`), `installer/common.iss` with `ArchitecturesAllowed=x64compatible`, per-app `.iss` files and `Suite.iss`, and `.github/workflows/release.yml` triggered by `stilus-v*`, `pinxit-v*`, `albumen-v*`, and `isotone-v*` tags. A local Stilus installer was verified on 2026-09-26 (63.1 MB, silent per-user install and uninstall, per `docs/dev/build.md`). Nothing is signed: there is no certificate, and `standards/release.md` says so. Only x64 is published. No app checks for updates (Stilus's Check for Updates is a stub). No winget manifest exists. `Suite.iss` requires Stilus and Pinxit publishes and names Stilus's executable `Bezier.Desktop.exe`. **Corrected 2026-09-27:** by operator decision that day, binaries are distributed only from rizonesoft.com: `release.yml` uploads the installer, the portable ZIP, and `SHA256SUMS` to S3-compatible storage served as `download.rizonesoft.com` (`<slug>/<version>/<file>`, slug `stilus`, `pinxit`, `albumen`, or `isotone`) with a hash-pinned rclone, writes the update feed `update/<slug>.json` (stable) or `update/<slug>-prerelease.json` last, and creates a GitHub release with no attached files whose body (from `scripts/release-manifest.ps1`) carries the CHANGELOG notes, Download links, the SHA-256 table, and the tag's source link; a tag release fails when the storage secrets are missing, and the storage itself is the operator's step `D99 T01 §8`. Every section below that said a GitHub release carries assets now reads the files from `download.rizonesoft.com`. **Corrected 2026-09-28:** 63.1 MB was the pre-upgrade size; after the 2026-09-26 upgrade the Stilus installer is 66.0 MB (`docs/dev/build.md`); and only `release.yml` has never run, while `build` and `plan-gates` have run green since 2026-09-26.
<!-- claim: count "ArchitecturesAllowed=x64compatible" installer/common.iss = 1 -->
<!-- claim: exists installer/Suite.iss -->
<!-- claim: count "isotone-v\*" .github/workflows/release.yml = 1 -->
<!-- claim: count "signtool" scripts/package.ps1 = 0 -->
<!-- claim: exists scripts/release-manifest.ps1 -->
<!-- claim: count "gh release upload" .github/workflows/release.yml = 0 -->

## Inputs

- [`standards/release.md`](../../standards/release.md) -- versions, artifacts, signing policy, and the release checklist
- [`docs/dev/build.md`](../../docs/dev/build.md), [`docs/dev/versioning.md`](../../docs/dev/versioning.md) -- how the scripts and tags work
- [`scripts/package.ps1`](../../scripts/package.ps1), [`scripts/publish.ps1`](../../scripts/publish.ps1), [`installer/`](../../installer/common.iss), [`.github/workflows/release.yml`](../../.github/workflows/release.yml) -- what this file extends
- -> XREF: D01 T02 §2 -- the settings store that `Updates.CheckOnStartup` and `Updates.IncludePrereleases` (§4) persist through; §4 here owns the update check itself
- -> XREF: D02 T05 §4 -- the Stilus release that runs §1's procedure first
- -> XREF: D03 T06 §3 -- the Pinxit release that runs §1's procedure
- -> XREF: D04 T01 §2 -- Albumen's app creation that makes it a shipping app for §6
- -> XREF: D99 T01 §3 -- the operator step that supplies the certificate §2 needs
- -> XREF: D99 T01 §8 -- the operator step that provisions `download.rizonesoft.com` and the storage secrets every release here uploads to (§3, §5, §6) and the feed §4 reads
- -> XREF: D99 T01 §9 -- the product page URLs (`ISOTONE_SITE_URL`) §4's result dialog and §5's manifests link
- -> XREF: D06 T01 §4 -- the install guide that documents what §1 proves
- -> XREF: D02 T17 §1 -- the Stilus parity releases that run §1's clean-machine procedure
- -> XREF: D03 T20 §8 -- Pinxit parity workspace cites §4: the opt-in `UpdateChecker` D03 T20 §8 consumes
- -> XREF: D03 T21 §1 -- the Pinxit parity releases cites §1: the clean-machine procedure every release runs
- -> XREF: D04 T14 §6 -- Albumen parity workspace cites §1: the installer and portable ZIP whose switches D04 T14 §6 documents; §3: the win-arm64 builds D04 T14 §7's platform page states; §4: the opt-in update check D04 T14 §7 consumes
- -> XREF: D04 T15 §1 -- the Albumen parity releases cites §1: the clean-machine procedure every release runs
- -> XREF: D03 T21 §15 -- Pinxit 1.3.0, the Pinxit version §7's bundle carries
- -> XREF: D01 T10 §1 -- the suite automation system that starts after §6's first bundle and that §7's bundle installs once for all three apps
- -> XREF: D01 T11 §1 -- the suite media stack that starts after §6's first bundle and that §7's bundle installs once
- -> XREF: D01 T12 §1 -- the on-device model runtime that starts after §6's first bundle and that §7's bundle installs once, with no model weight in any package

## Outcome

- `docs/dev/clean-machine.md` is the procedure every app release runs, and Stilus 0.1.0 is its first quoted run.
- With a certificate supplied from outside the repository, every executable, DLL we build, installer, and uninstaller is Authenticode-signed with a timestamp, and `signtool verify /pa` passes on each.
- `win-arm64` installers and ZIPs are produced per app and uploaded by the release workflow to `download.rizonesoft.com`.
- Each app's Help, Check for Updates compares its version with its update feed on `download.rizonesoft.com` (`update/<slug>.json`, plus `update/<slug>-prerelease.json` when prereleases are included) and offers the product page, with a setting to check on startup.
- winget manifests for each released app point at `download.rizonesoft.com` installer URLs, are submitted, and install the app.
- `isotone-v1.0.0` publishes the suite installer and ZIP on `download.rizonesoft.com`, carrying Stilus, Pinxit, and Albumen at their current versions.
- `isotone-v1.1.0` publishes the second bundle carrying Stilus 1.2.0, Pinxit 1.3.0, and Albumen 1.4.0 at their own versions.

**Adjacency:** list=not-applicable (no browsable records); document=not-applicable (release notes are the changelog's); settings=applicable @ D05 T01 §4; reporting=not-applicable (no summaries); notifications=applicable @ D05 T01 §4; permissions=applicable @ D05 T01 §1; audit=not-applicable (release evidence is the changelog and the workflow log); exchange=not-applicable (no user formats); reverse=applicable @ D05 T01 §1

**Adjacency rationale:** The update check is a setting and a notification; install scope (per-user versus all-users) is the permission surface, proven on refusal (all-users without elevation); uninstall is the reverse of install; each release records its evidence in the changelog and the workflow run.

## Implementation Order

| Order | Section | Deliverable                                              | Depends On                                 | Status |
| :---: | :-----: | -------------------------------------------------------- | ------------------------------------------ | :----: |
|   1   |   §1    | The clean-machine install procedure                      | D00 T02 §7                                 |  [ ]   |
|   2   |   §2    | Sign binaries and installers                             | §1                                         |  [ ]   |
|   3   |   §3    | win-arm64 publish and installers                         | D02 T05 §4                                 |  [ ]   |
|   4   |   §4    | The update check                                         | D01 T02 §2, D02 T05 §4                     |  [ ]   |
|   5   |   §5    | winget manifests                                         | D02 T05 §4, D03 T06 §3, D04 T02 §8         |  [ ]   |
|   6   |   §6    | The suite bundle: isotone-v1.0.0                          | §4, D02 T05 §4, D03 T06 §3, D04 T02 §8, D06 T01 §4 |  [ ]   |
|   7   |   §7    | The suite bundle: isotone-v1.1.0 | §6, D02 T17 §12, D03 T21 §15, D04 T15 §14 |  [ ]   |
|   8   |   §8    | Third-party notices in every package | D00 T02 §7 |  [ ]   |

---

## 1. The Clean-Machine Install Procedure

A developer machine has the .NET SDK and runtimes, so a self-contained publish that accidentally depends on an installed runtime passes there and fails for users. Every release is proven on a clean Windows 11 machine (a Windows Sandbox instance or a VM snapshot), and the procedure is written once so each app's release section runs the same steps. **Corrected 2026-09-26:** the supported OS is Windows 11 (23H2 or later); Windows 10 22H2 is best-effort because .NET 11 supports only its LTSC and IoT editions, so an extra Windows 10 22H2 smoke is optional and its failures are recorded, never blocking.

**Needs:** Clean Windows machine (no .NET SDK)

- [ ] Write `docs/dev/clean-machine.md`: how to get a clean Windows 11 machine (Windows Sandbox with a `.wsb` file mapping `artifacts/dist` read-only, committed as `tools/sandbox/clean-machine.wsb`), and the steps: confirm `dotnet --list-runtimes` fails, install per-user silently, launch, open a fixture, save, close, check the log for errors, uninstall, confirm the install folder and Start menu entry are gone; repeat all-users (elevated) and confirm a non-elevated all-users install is refused with the Inno Setup message; upgrade over the previous release and confirm settings survive; on Windows 10 22H2 (optional, best-effort), confirm the interactive installer shows the "not officially supported" notice and a `/VERYSILENT` install does not. Done when: the page and the `.wsb` file exist.
- [ ] Run the procedure for Stilus on the current build and quote each step. Done when: every step passes, or each failure is filed through `add-todo` with its owner.
- [ ] Commit: `"release: a written clean-machine install procedure, run for Stilus"`

**Requires:** display-session -- the Windows Sandbox session and the installer UI need an interactive desktop

**Test checkpoint:** the quoted run shows `dotnet --list-runtimes` absent, a successful per-user and all-users install, the app window, a saved fixture, an uninstall leaving no folder, and settings surviving an upgrade (a `settings.json` readback). Cheaper substitute that fails: installing on the development machine, where the runtime check cannot fail.

## 2. Sign Binaries and Installers

Unsigned installers trigger SmartScreen warnings and cannot build reputation. The operator has no certificate today (`D99 T01 §3`), so this row waits on its `Needs:` line; the plumbing is written so that supplying a certificate is the only step left. Credentials never enter the repository, arguments, or logs.

**Needs:** Signing certificate (release)

- [ ] `scripts/sign.ps1` signs a list of files with `signtool sign /fd SHA256 /tr <RFC 3161 timestamp URL> /td SHA256`, reading the certificate from the Windows certificate store by thumbprint (`ISOTONE_SIGN_THUMBPRINT`) or from a cloud signing service's CLI, never from a file path in the repository. Done when: the script refuses to run without the environment variable and prints no secret.
- [ ] `scripts/package.ps1` signs the app's own executables and DLLs after publish and the installer and uninstaller through Inno Setup's `SignTool` directive in `installer/common.iss`, only when signing is configured. Done when: an unsigned build still works without the variable.
- [ ] `release.yml` signs when the repository secret is configured (the certificate stays in the signing service or an encrypted secret; the workflow never echoes it). Done when: a dry run on a prerelease tag produces signed assets.
- [ ] `signtool verify /pa /all` on every signed file is part of the release checklist in `standards/release.md`. Done when: the checklist line exists.
- [ ] Commit: `"release: sign binaries and installers when a certificate is supplied"`

**Test checkpoint:** on a prerelease tag with signing configured, `signtool verify /pa` passes for the installer, the uninstaller, and the app executable (quoted); the workflow log contains no certificate material (grep of the downloaded log for the thumbprint and `BEGIN` prints nothing). Cheaper substitute that fails: a self-signed certificate, which `verify /pa` rejects.

## 3. win-arm64 Publish and Installers

Windows on Arm machines run x64 apps under emulation, slowly. .NET 11 and WPF support `win-arm64`; SkiaSharp ships arm64 native assets. `publish.ps1` already takes `-Runtime win-arm64`; the installers and workflow do not.

**Needs:** Windows host (build/test)

- [ ] `installer/common.iss` sets `ArchitecturesAllowed` and `ArchitecturesInstallIn64BitMode` from the `Runtime` define (`x64compatible` or `arm64`). Done when: `pwsh scripts/package.ps1 -App Stilus -Runtime win-arm64` produces an arm64 installer.
- [ ] Every native dependency ships an arm64 asset (SkiaSharp, the RAW decoder, ComputeSharp's DirectX runtime); any that does not is named with its fallback. Done when: the publish folder for each app lists arm64 native DLLs (quoted).
- [ ] `release.yml` builds both runtimes and uploads both sets of files to `download.rizonesoft.com/<slug>/<version>/` with `SHA256SUMS` covering all, `scripts/release-manifest.ps1` listing both in the release body and the feed's `files` (**Corrected 2026-09-27:** said uploads both sets of assets to the GitHub release, which carries no binaries since the operator's distribution decision). Done when: a prerelease tag's download folder holds six files per app and its release body links all six.
- [ ] A launch on arm64 hardware (or an arm64 VM), or, if none is available, the gap recorded with an owner through `add-todo`. Done when: one or the other is quoted.
- [ ] Commit: `"release: win-arm64 installers and ZIPs for every app"`

**Requires:** display-session -- launching the arm64 build needs an interactive desktop
**Test checkpoint:** a prerelease tag's download folder on `download.rizonesoft.com` and its release body list `win-x64` and `win-arm64` installers and ZIPs for the app, and `dumpbin /headers` (or `Get-PEArchitecture` via a small script) on the arm64 executable reports `AA64`. Cheaper substitute that fails: an x64 build renamed arm64, which the header check catches.

## 4. The Update Check

Users should learn a new version exists without the app phoning home silently. Each app reads its own update feed, only when the user asks or has allowed a startup check, and offers the product page; it never downloads or installs by itself. Every app needs it, so it lives in `Isotone.Core`.

**Corrected 2026-09-27:** said each app asks the GitHub releases API for the latest release with its tag prefix and offers the release page. Operator decision 2026-09-27: binaries ship only from rizonesoft.com, so the check reads the feed `release.yml` writes to `https://download.rizonesoft.com/update/<slug>.json` (latest stable) and, with prereleases included, `update/<slug>-prerelease.json`, taking the higher SemVer of the two; the feed's fields are in `docs/dev/versioning.md` (`version`, `url`, `sha256`, `notes`, `page`, `date`). The base URL is one setting with the default `https://download.rizonesoft.com`, never typed at a call site.

**Fidelity:** Help, Check for Updates and its result dialog -- new build, no baseline; captured to docs/captures/stilus/update-check/ (and the Pinxit and Albumen equivalents).
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/Button/README.md, docs/design/components/Checkbox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can find out whether a newer release of the app they run exists and open its download page. Consumer: the user.
**Treatment:** `UpdateChecker` in `Isotone.Core/Updates/` reads `https://download.rizonesoft.com/update/<slug>.json` (and `<slug>-prerelease.json` when prereleases are included) over HTTPS with a user agent naming the app and version, refuses a feed whose `app` is not its own, and compares SemVer; the result dialog says "You have the latest version (x)." or "Stilus y is available (you have x). What's new: ..." linking the feed's `notes`, with Open Download Page opening the feed's `page` (the product page, `https://www.rizonesoft.com/` until `D99 T01 §9` decides per-app pages) with `?utm_source=app&utm_medium=update-check`; a setting `Updates.CheckOnStartup` (default off, offered once on first run) and `Updates.IncludePrereleases` (default off); network failure says "Could not check for updates: <reason>." and logs a Warning. Cheaper substitute that fails the checkpoint: comparing version strings as text.
**Chrome:** consume `Isotone.Core` settings and logging, the `Isotone.UI` dialog shell, and the theme. Do not add a per-app update client.

**Requires:** display-session -- the update dialog needs an interactive desktop

- [ ] `UpdateChecker` with an injectable HTTP handler, SemVer comparison, the stable and prerelease feeds, and a 10-second timeout (**Corrected 2026-09-27:** said prefix filtering over the GitHub releases API; the feed replaces it). Done when: `UpdateCheckerTests` cover newer, same, older, prerelease filtering (the prerelease feed read only when included, the higher version winning), another app's feed refused (`app` mismatch), and network failure.
- [ ] The dialog and the Help menu item in every shipping app, replacing each app's planned stub. Done when: `MenuAuditTests` in each app pass with the item enabled.
- [ ] The two settings and the first-run offer. Done when: the startup check runs only when enabled (test).
- [ ] Commit: `"core: an opt-in update check against each app's update feed"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `UpdateCheckerTests` reporting all six cases; a driven check from Stilus against the live feed `https://download.rizonesoft.com/update/stilus.json` shows the correct result for the running version (capture and log line). Cheaper substitute that fails: text comparison, which `0.10.0` versus `0.9.0` catches.

## 5. winget Manifests

winget is how many Windows users install software. Each released app gets a manifest in `microsoft/winget-pkgs` pointing at its installer on `download.rizonesoft.com`, with silent switches and the per-user scope. **Corrected 2026-09-27:** said pointing at its GitHub release installer; GitHub releases carry no binaries since the operator's distribution decision, so every `InstallerUrl` is `https://download.rizonesoft.com/<slug>/<version>/<App>-<version>-win-x64-Setup.exe` and `PackageUrl` is the product page. Unsigned installers are accepted but may be flagged; signing (§2) is recommended first, not required.

**Needs:** Windows host (build/test)

- [ ] Author manifests with `wingetcreate new` for `Rizonesoft.Stilus`, `Rizonesoft.Pinxit`, and `Rizonesoft.Albumen` (installer URL on `download.rizonesoft.com` and its SHA-256 from the release's `SHA256SUMS`, `InstallerType: inno`, `Scope: user` and `machine` entries, license GPL-3.0, publisher Rizonesoft, `PublisherUrl` and `PackageUrl` from `ISOTONE_SITE_URL`, `Copyright: Copyright (C) 2025-2026 Rizonetech (Pty) Ltd`), keeping copies under `installer/winget/`. Done when: `winget validate` passes on each.
- [ ] `winget install --manifest installer/winget/<App>` installs each app locally. Done when: each installs and starts (quoted).
- [ ] Submit the manifests with `wingetcreate submit` (the operator's GitHub account authorizes the fork; this runs with `gh` credentials the agent has, or is handed to the operator if not). Done when: the pull requests are open (URLs quoted), or the handoff is recorded as a `D99` row.
- [ ] A release step (script or workflow job) updates the manifests on each new app release with `wingetcreate update`, reading the installer URL and hash from the update feed. Done when: it is documented in `docs/dev/build.md`.
- [ ] Commit: `"release: winget manifests for Stilus, Pinxit, and Albumen"`

**Test checkpoint:** `winget validate` exits 0 for each manifest and every `InstallerUrl` starts with `https://download.rizonesoft.com/`; `winget install --manifest` installs each app (quoted); the submission PR URLs are quoted. Cheaper substitute that fails: manifests never validated.

## 6. The Suite Bundle: isotone-v1.0.0

The suite bundle packages all three apps in one installer and one ZIP without changing any app's version. It runs once each app has shipped its first release. The tag `isotone-v1.0.0` marks the first bundle; its version is the bundle's, not an app's.

**Needs:** Clean Windows machine (no .NET SDK)

**Corrected 2026-09-27:** added the backlog review before the tag (operator decision 2026-09-27, "Release-time backlog gate", with "No drop without operator approval"; `todo/README.md`, The budget and the backlog): every backlog entry, whatever its app, is promoted into a section or deferred by the operator in words recorded on the entry as a `reviewed: isotone-v1.0.0` field, and `validate` refuses this section's stamp while one is unreviewed (`release-backlog-unreviewed`).

- [ ] `installer/Suite.iss` requires Albumen when Albumen ships (mirroring the Stilus and Pinxit checks) and its component list names each app with its own version from its latest tag. Done when: the suite installer's component page shows three apps with their versions.
- [ ] An `isotone-v1.0.0` section in `CHANGELOG.md` listing the app versions the bundle carries. Done when: it exists.
- [ ] Run the clean-machine procedure for the suite installer: install all three, uninstall one component, confirm the others still run and no standalone install's registry keys were touched. Done when: every step passes (quoted).
- [ ] Run the backlog review for `isotone-v1.0.0`: list the entries with `python scripts/todo-graph.py query backlog`, and for every entry, whatever its `app:` (a suite release reviews the whole backlog), either promote it into a section through `add-todo` or ask the operator whether it may wait and append `-- reviewed: isotone-v1.0.0 <YYYY-MM-DD> deferred by operator: "<their words>"` to the entry (`-- reviewed: isotone-v1.0.0 <YYYY-MM-DD> promoted DNN TNN §N` when only part of it became a section). Done when: every in-scope entry is promoted or carries a `reviewed: isotone-v1.0.0` field (list quoted), so the stamp passes `release-backlog-unreviewed`.
- [ ] Push `isotone-v1.0.0`; verify the workflow, the files under `https://download.rizonesoft.com/isotone/1.0.0/`, `SHA256SUMS`, and the feed `update/isotone.json` (**Corrected 2026-09-27:** said the assets, which are no longer attached to the GitHub release). Done when: all pass (URLs and hashes quoted).
- [ ] `installer/Suite.iss`'s `albumen` component carries `AlbumenViewer.exe` and offers the same unchecked "Register Albumen Viewer for image types" task (install runs `--register`, uninstall `--unregister`), registering under the suite's own ProgIDs so a standalone Albumen install's associations are untouched (**Groomed 2026-09-28:** the suite bundle defined only `Albumen.exe`). Done when: the clean-machine run opens a `.heic` from Explorer in the viewer after the suite install, and the standalone install's registry keys are unchanged (export diff quoted).
- [ ] Commit: `"release: the Isotone Graphics Suite 1.0.0 bundle"`

**Requires:** display-session -- the suite installer's component page and the app launches need an interactive desktop

**Test checkpoint:** `gh release view isotone-v1.0.0 --json assets,body` shows no assets and a body linking the suite installer, ZIP, and `SHA256SUMS` under `https://download.rizonesoft.com/isotone/1.0.0/`, whose downloads match their hashes; the clean-machine run shows three apps installed side by side with their own versions in their About dialogs. Cheaper substitute that fails: a bundle that re-versions every app to 1.0.0, which the About dialogs catch.

## 7. The Suite Bundle: isotone-v1.1.0

The second suite bundle carries the apps at the versions the post-release phases ship: Stilus 1.2.0 (`D02 T17 §12`, Phase 42), Pinxit 1.3.0 (`D03 T21 §15`, Phase 44), and Albumen 1.4.0 (`D04 T15 §14`, Phase 45), after the operator planned the work deferred "after the first release" (suite automation, video and audio, animation, on-device models, the GPU develop path, and Albumen's remaining formats) as real sections on 2026-09-27 because features must not be left behind. Like `§6` it changes no app's version: the tag `isotone-v1.1.0` is the bundle's version, and each app keeps its own tag and About version. It also proves the shared pieces those phases added to `Isotone.Core` and `Isotone.UI` (the automation system of `D01 T10`, the media stack of `D01 T11`, the on-device model runtime of `D01 T12`) install once side by side without one app's uninstall breaking another. -> SOURCE: parity-suite-release-1.1.0

**Needs:** Clean Windows machine (no .NET SDK)

**Requires:** display-session -- the suite installer's component page and the app launches need an interactive desktop

- [ ] Update `installer/Suite.iss` so its component list names Stilus 1.2.0, Pinxit 1.3.0, and Albumen 1.4.0 with each version read from the app's latest tag. Done when: the suite installer's component page shows the three apps with those versions (capture committed under `docs/captures/suite/release-1.1.0/`).
- [ ] Add an `isotone-v1.1.0` section to `CHANGELOG.md` listing the app versions the bundle carries and linking each app's own release notes. Done when: it exists and names all three versions.
- [ ] Build `pwsh scripts/package.ps1 -Suite -Version 1.1.0`. Done when: the suite installer, the suite ZIP, and `SHA256SUMS` exist under `artifacts/dist/`, and the ZIP carries no FFmpeg, GDAL, or `.onnx` file (file list quoted).
- [ ] Run the clean-machine procedure of `§1` for the suite installer: upgrade over `isotone-v1.0.0`, confirm each app's About version, run one recorded action in each app, play a video fixture in Pinxit and Albumen, uninstall one component, and confirm the other two still start and run their automation and media features. Done when: every step passes (quoted).
- [ ] Confirm no standalone install's registry keys were touched by the suite install or the component uninstall. Done when: the before-and-after registry export diff is quoted with no change under the standalone apps' keys.
- [ ] Run the backlog review for `isotone-v1.1.0`: list the entries with `python scripts/todo-graph.py query backlog`, and for every entry, whatever its `app:` (a suite release reviews the whole backlog), either promote it into a section through `add-todo` or ask the operator whether it may wait and append `-- reviewed: isotone-v1.1.0 <YYYY-MM-DD> deferred by operator: "<their words>"` to the entry (`-- reviewed: isotone-v1.1.0 <YYYY-MM-DD> promoted DNN TNN §N` when only part of it became a section). Done when: every in-scope entry is promoted or carries a `reviewed: isotone-v1.1.0` field (list quoted), so the stamp passes `release-backlog-unreviewed`.
- [ ] Push the tag `isotone-v1.1.0`; verify the workflow, the files under `https://download.rizonesoft.com/isotone/1.1.0/`, `SHA256SUMS`, and the feed `update/isotone.json`. Done when: all pass (URLs and hashes quoted).
- [ ] Confirm with `git tag --points-at HEAD` that only `isotone-v1.1.0` points at the release commit and no app tag moved. Done when: the output is quoted.
- [ ] Commit: `"release: the Isotone Graphics Suite 1.1.0 bundle"`

**Test checkpoint:** Driven run with evidence: `gh release view isotone-v1.1.0 --json assets,body` shows no assets and a body linking the suite installer, ZIP, and `SHA256SUMS` under `https://download.rizonesoft.com/isotone/1.1.0/`, whose downloads match their hashes; the clean-machine run shows Stilus 1.2.0, Pinxit 1.3.0, and Albumen 1.4.0 installed side by side with their own versions in their About dialogs, and the two remaining apps still run after one component's uninstall. Cheaper substitute that fails: a bundle that re-versions every app to 1.1.0, which the About dialogs catch.

## 8. Third-Party Notices in Every Package

**Origin:** discovered run=d1b2e37f2025 2026-09-28 -- groom-plan gap scan

Every installer and ZIP already ships third-party code that asks for attribution with the binaries (SkiaSharp and CommunityToolkit under MIT, Serilog under Apache-2.0, AvalonDock under MS-PL, SharpVectors under BSD), yet no notices file exists and nothing ships one: `installer/common.iss` packs only `LICENSE`, and no script copies notices into a publish folder. Sections that add dependencies append to a notices file at two different paths (the root `THIRD-PARTY-NOTICES` in `D02 T10`, `D03 T11`, and `D03 T12`; `src/Isotone.Core/THIRD-PARTY-NOTICES.md` in `D01 T04` and `D03 T17`). This is a defect in shipped work and a prerequisite of the first release, `D02 T05 §4`, so it is filed as a section: one canonical file, checked against the packages, in every package.

**Fidelity:** no surface of its own -- a notices file, a check script, and packaging wiring; the About dialog link is the About sections' own surface.

**Needs:** Windows host (build/test)

- [ ] Add `THIRD-PARTY-NOTICES.md` at the repository root with one entry per shipped package and bundled data set: name, version, license, copyright, and the license text or its canonical URL. Done when: every `PackageVersion` in `Directory.Packages.props` that a shipping project references has an entry.
- [ ] Add `scripts/notices.py` (stdlib) whose `--check` fails when a package a shipping project references has no entry, or an entry names a package no project references, and run it in `scripts/check-all.ps1` and `build.yml`. Done when: adding a probe `PackageReference` without an entry fails the check naming it, and the tree passes (both quoted).
- [ ] Make `scripts/publish.ps1` copy `THIRD-PARTY-NOTICES.md` beside `LICENSE` into every publish folder, so each installer and portable ZIP carries it. Done when: `artifacts/dist/` for Stilus contains the file inside the ZIP and the installed folder (listing quoted).
- [ ] Rewrite the plan's references to the two other paths (`THIRD-PARTY-NOTICES` and `src/Isotone.Core/THIRD-PARTY-NOTICES.md`) to the one root file. Done when: `grep -rn "THIRD-PARTY-NOTICES" todo | grep -v "THIRD-PARTY-NOTICES.md"` and `grep -rn "Isotone.Core/THIRD-PARTY" todo` print nothing outside this section.
- [ ] Commit: `"release: one third-party notices file, checked and shipped in every package"`

**Test checkpoint:** Unit test and driven run: `python scripts/notices.py --check` exits 0 on the tree and exits 1 naming a probe package added without an entry (quoted, then reverted); `pwsh scripts/package.ps1 -App Stilus` produces a ZIP whose listing includes `THIRD-PARTY-NOTICES.md` (quoted). Cheaper substitute that fails: a notices file in the repository that no package carries.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0
- [ ] Every app release since this file shipped has a quoted clean-machine run
- [ ] `signtool verify /pa` passes on every published file once signing is configured
- [ ] `gh release list` shows `isotone-v1.0.0` and `isotone-v1.1.0`, each carrying the app versions its `CHANGELOG.md` section names
- [ ] No GitHub release carries an attached installer or ZIP (`gh release view <tag> --json assets` for each release)
- [ ] `python scripts/todo-graph.py validate` clean
