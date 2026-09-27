# Release Standards

How each app, and the suite bundle, is versioned, packaged, and released. The mechanics (scripts, installers, CI) are described in [`docs/dev/build.md`](../docs/dev/build.md) and [`docs/dev/versioning.md`](../docs/dev/versioning.md); this file is the policy they implement.

## Versions and tags

- SemVer 2.0 per app, derived from git tags by MinVer. No version string is typed into a project file.
- Tag prefixes: `stilus-v*`, `pinxit-v*`, `albumen-v*` for the apps, and `isotone-v*` for a suite bundle. A version with a hyphen (`0.1.0-alpha.1`) is a prerelease. A pipeline dry run is a draft release made by dispatching `release.yml` in its draft mode with the tag as an input: the tag is never pushed, and the draft is deleted after inspection (operator decision 2026-09-27, `D00 T02 §7`).
- **No app's version moves because another app shipped.** A suite bundle records which app versions it carries; it does not re-version them.
- `Isotone.Core` and `Isotone.UI` are not released on their own: each app ships the copy it was built with.

## Changelogs

- Each app keeps its own section in `CHANGELOG.md` (Keep a Changelog format), headed by the tag it ships as, so the release workflow can lift the notes for that tag.
- Every user-visible change adds a line in the commit that makes it.

## Artifacts

Each app release produces, under `artifacts/dist/`:

- `<App>-<version>-win-x64-Setup.exe`: Inno Setup, per-user by default with an all-users option, its own AppId and install folder, opt-in file associations, an uninstaller.
- `<App>-<version>-win-x64-Portable.zip`: the self-contained publish folder.
- `SHA256SUMS` covering both.

## Distribution

Operator decision 2026-09-27: binaries are distributed only from rizonesoft.com.

- The installer, the portable ZIP, and `SHA256SUMS` are uploaded to S3-compatible object storage served as `download.rizonesoft.com`, at `<slug>/<version>/<file>` (slug `stilus`, `pinxit`, `albumen`, or `isotone` for the suite). A published file is never replaced.
- The update feed is `download.rizonesoft.com/update/<slug>.json` for the latest stable release and `update/<slug>-prerelease.json` for the latest prerelease; its fields are in [`docs/dev/versioning.md`](../docs/dev/versioning.md).
- A GitHub release carries the release notes, GitHub's automatic source archives, the SHA-256 table, and prominent links to the downloads. **No installer or ZIP is ever attached to a GitHub release.**
- winget manifests point at `download.rizonesoft.com` URLs.
- The product page is one configured value, `ISOTONE_SITE_URL` (default `https://www.rizonesoft.com/`, until the per-app pages are decided); a link from a GitHub surface adds `?utm_source=github&utm_medium=<place>`.
- A tag release fails when the storage is not configured, rather than publishing a release without downloads.

## Ownership text

The copyright holder is Rizonetech (Pty) Ltd: "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd", with the line "Rizonesoft is a brand of Rizonetech (Pty) Ltd." where the brand appears. The publisher users see stays Rizonesoft (`AppPublisher`, the About dialog's product link). The assembly metadata (`Company`, `Copyright` in `Directory.Build.props`), the installers (`AppCopyright`, `VersionInfoCopyright`, `VersionInfoCompany` in `installer/common.iss`), the About dialog, and the release body all use this wording. The GPL source offer is a link to the exact tag ("Source code: https://github.com/rizonesoft/Isotone/tree/<tag>"), shown in the About dialog and the installer. The names and icons are covered by [`TRADEMARKS.md`](../TRADEMARKS.md).

Self-contained .NET: no runtime prerequisite on the target machine. x64 today; win-arm64 is planned (`todo/05-release/`). Installers are built with Inno Setup 7 as 64-bit Setup programs (`SetupArchitecture=x64`).

The suite installer (`Isotone-<version>-win-x64-Setup.exe`, `installer/Suite.iss`, one component per shipping app) is built only from an `isotone-v*` tag or `scripts/package.ps1 -Suite`; a per-app release never needs it.

**Supported OS:** Windows 11 (23H2 or later), x64. Windows 10 22H2 is best-effort: .NET 11 supports only the Windows 10 LTSC and IoT editions, so the apps may run on consumer Windows 10 but are untested there. Builds keep `TargetPlatformMinVersion` 10.0.17763.0 and installers keep `MinVersion=10.0.17763`, so Windows 10 is never blocked; the interactive installer shows a non-blocking notice on Windows 10 (build < 22000), which silent installs skip.

## Signing

Binaries and installers are not signed yet: there is no certificate. When one exists it is supplied to the packaging scripts from outside the repository (never in a tracked file, an argument, or a log), and signing is verified with `signtool verify /pa` before a release is published.

## The release checklist

A release tag is pushed only when every line holds, each quoted from a real run in the release section's evidence:

1. `pwsh scripts/check-all.ps1` exits 0 at the commit being tagged.
2. The app's `CHANGELOG.md` section is headed by the tag and lists every user-visible change since the last release.
3. The app's user guide under `docs/user/` covers every surface the release ships.
4. `pwsh scripts/package.ps1 -App <App>` produces the installer and the portable ZIP locally.
5. The installer installs, launches, and uninstalls on a clean Windows 11 machine with no .NET SDK or runtime, per-user and all-users, and an upgrade over the previous release keeps the user's settings. An extra smoke on Windows 10 22H2 is optional and best-effort: a failure there is recorded, never a release blocker.
6. The portable ZIP runs from an empty folder.
7. After the tag is pushed, the `release` workflow is green; the installer, the ZIP, and `SHA256SUMS` download from `https://download.rizonesoft.com/<slug>/<version>/` and their hashes match `SHA256SUMS`; the GitHub release has no attached files and its body links those downloads, lists the same hashes, and links the tag's source; and `https://download.rizonesoft.com/update/<slug>.json` (or `<slug>-prerelease.json`) names the new version.
