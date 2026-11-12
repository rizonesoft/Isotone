# Release Standards

How each app, and the suite bundle, is versioned, packaged, and released. The mechanics (scripts, installers, CI) are described in [`docs/dev/build.md`](../docs/dev/build.md) and [`docs/dev/versioning.md`](../docs/dev/versioning.md); this file is the policy they implement.

## Versions and tags

- SemVer 2.0 per app, computed by CMake from the app's own git tags (operator decision 2026-10-23, "SemVer from tags, automated"). No version string is typed into a source or build file, and every binary embeds its version and its commit (`isotone::core::version()` and `build_id()`).
- Tag prefixes: `stilus-v*`, `gesso-v*`, `albumen-v*` for the apps, and `isotone-v*` for a suite bundle. A version with a hyphen is a prerelease in one of three channels, `alpha`, `beta`, and `rc` (`0.1.0-alpha.1`, `0.1.0-rc.2`), each feeding the update channel of the same name. A pipeline dry run is a draft release made by dispatching `release.yml` in its draft mode with the tag as an input: the tag is never pushed, and the draft is deleted after inspection (operator decision 2026-09-27; the native pipeline's dry run is planned in `todo/05-release/`).
- **No app's version moves because another app shipped.** A suite bundle records which app versions it carries; it does not re-version them.
- `isotone::core` and `isotone::ui` are not released on their own: they are static libraries, and each app's executable carries the copy it was built with.
- The Windows file version is the four-part `Major.Minor.Patch.Build`, the build number added by CI; the product version is the full SemVer with the commit.

## Changelogs

- Each app keeps its own section in `CHANGELOG.md` (Keep a Changelog format), headed by the tag it ships as, so the release workflow can lift the notes for that tag.
- Changelogs and the next version are generated from Conventional Commits carrying the app's scope (`feat(stilus):`, `fix(gesso):`, `perf(albumen):`, `!` for a breaking change): a `feat` raises the minor version, a `fix` or `perf` the patch, a breaking change the major. Every user-visible change is therefore a commit with the right type and scope.

## Artifacts

Each app release produces, under `artifacts/dist/`:

- `<App>-<version>-win-x64-Setup.exe`: Inno Setup, per-user by default with an all-users option, its own AppId and install folder, opt-in file associations, an uninstaller.
- `<App>-<version>-win-x64-Portable.zip`: the app's publish folder, which runs from any folder with nothing else installed.
- The same pair for `win-arm64`: both architectures are built and tested from the first release (the spec's "The toolchain").
- `SHA256SUMS` covering both.

## Distribution

Operator decision 2026-09-27: binaries are distributed only from rizonesoft.com.

- The installer, the portable ZIP, and `SHA256SUMS` are uploaded to S3-compatible object storage served as `download.rizonesoft.com`, at `<slug>/<version>/<file>` (slug `stilus`, `gesso`, `albumen`, or `isotone` for the suite). A published file is never replaced.
- The update feed is `download.rizonesoft.com/update/<slug>.json` for the latest stable release and a prerelease feed per channel (`alpha`, `beta`, `rc`), so a user on the stable feed is never offered a prerelease (the file names are fixed by the release pipeline's section in `todo/05-release/`; the script of the removed build wrote one `update/<slug>-prerelease.json`); its fields are in [`docs/dev/versioning.md`](../docs/dev/versioning.md).
- A GitHub release carries the release notes, GitHub's automatic source archives, the SHA-256 table, and prominent links to the downloads. **No installer or ZIP is ever attached to a GitHub release.**
- winget manifests point at `download.rizonesoft.com` URLs.
- The product page is one configured value, `ISOTONE_SITE_URL` (default `https://www.rizonesoft.com/`, until the per-app pages are decided); a link from a GitHub surface adds `?utm_source=github&utm_medium=<place>`.
- A tag release fails when the storage is not configured, rather than publishing a release without downloads.

## Ownership text

The copyright holder is Rizonetech (Pty) Ltd: "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd", with the line "Rizonesoft is a brand of Rizonetech (Pty) Ltd." where the brand appears. The publisher users see stays Rizonesoft (`AppPublisher`, the About dialog's product link). Each executable's version resource (`CompanyName`, `LegalCopyright`, written by the build), the installers (`AppCopyright`, `VersionInfoCopyright`, `VersionInfoCompany` in `installer/common.iss`), the About dialog, and the release body all use this wording. The GPL source offer is a link to the exact tag ("Source code: https://github.com/rizonesoft/Isotone/tree/<tag>"), shown in the About dialog and the installer. The names and icons are covered by [`TRADEMARKS.md`](../TRADEMARKS.md).

No runtime prerequisite on the target machine: every app links the static C runtime and imports only Windows system DLLs (`scripts/native-artifact-gate.py`), and its publish folder stays within the size budget `native/size-budget.json` sets. Installers are built with Inno Setup 7 as 64-bit Setup programs.

The suite installer (`Isotone-<version>-win-x64-Setup.exe`, `installer/Suite.iss`, one component per shipping app) is built only from an `isotone-v*` tag or `scripts/package.ps1 -Suite`; a per-app release never needs it.

**Supported OS:** Windows 11 (23H2 or later), x64 and ARM64. Windows 10 22H2 is best-effort: the apps may run there but are untested. Installers keep their minimum Windows version at 10.0.17763, so Windows 10 is never blocked; the interactive installer shows a non-blocking notice on Windows 10 (build < 22000), which silent installs skip.

## Release candidates and publishing

Releases never block development (the native re-plan, requirement 6): each app release is a release-candidate section the campaign completes (built, tested, packaged, ready to sign, notes and changelog written) and a publish section that waits on the operator's rows in `todo/99-manual/` (the signing certificate, the download storage and its secrets). No later phase depends on a publish section.

## Signing

Binaries and installers are not signed yet: there is no certificate. When one exists it is supplied to the packaging scripts from outside the repository (never in a tracked file, an argument, or a log), and signing is verified with `signtool verify /pa` before a release is published.

## The release checklist

A release tag is pushed only when every line holds, each quoted from a real run in the release section's evidence:

1. `pwsh scripts/check-all.ps1` exits 0 at the commit being tagged.
2. `python scripts/check-native-advisories.py --release-gate` exits 0 at the commit being tagged (enforced before packaging by `scripts/package.ps1` and `.github/workflows/release.yml`): a release section may not tag while the job reports an `advisory` for a library its app links, or while the job fails with an `unmapped` advisory identity, an `unchecked` failed or partial OSV/feed/baseline query, or a `baseline-mismatch` between `docs/dev/native-libraries.md` and `native/vcpkg.json`'s committed `builtin-baseline`; each failing outcome blocks the release with its own `release-gate blocked (<outcome>): ...` message (`D00 T04 §3`).
3. The app's `CHANGELOG.md` section is headed by the tag and lists every user-visible change since the last release.
4. The app's user guide under `docs/user/` covers every surface the release ships.
5. `pwsh scripts/package.ps1 -App <App>` produces the installer and the portable ZIP locally.
6. The installer installs, launches, and uninstalls on a clean Windows 11 machine with nothing else installed (no compiler, no redistributable), per-user and all-users, and an upgrade over the previous release keeps the user's settings. An extra smoke on Windows 10 22H2 is optional and best-effort: a failure there is recorded, never a release blocker.
7. The portable ZIP runs from an empty folder.
8. After the tag is pushed, the `release` workflow is green; the installer, the ZIP, and `SHA256SUMS` download from `https://download.rizonesoft.com/<slug>/<version>/` and their hashes match `SHA256SUMS`; the GitHub release has no attached files and its body links those downloads, lists the same hashes, and links the tag's source; and `https://download.rizonesoft.com/update/<slug>.json` (or the prerelease channel's feed) names the new version.
