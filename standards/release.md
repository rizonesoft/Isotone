# Release Standards

How each app, and the suite bundle, is versioned, packaged, and released. The mechanics (scripts, installers, CI) are described in [`docs/dev/build.md`](../docs/dev/build.md) and [`docs/dev/versioning.md`](../docs/dev/versioning.md); this file is the policy they implement.

## Versions and tags

- SemVer 2.0 per app, derived from git tags by MinVer. No version string is typed into a project file.
- Tag prefixes: `nodus-v*`, `imago-v*`, `lumen-v*` for the apps, and `photon-v*` for a suite bundle. A version with a hyphen (`0.1.0-alpha.1`) is a prerelease.
- **No app's version moves because another app shipped.** A suite bundle records which app versions it carries; it does not re-version them.
- `Photon.Core` and `Photon.UI` are not released on their own: each app ships the copy it was built with.

## Changelogs

- Each app keeps its own section in `CHANGELOG.md` (Keep a Changelog format), headed by the tag it ships as, so the release workflow can lift the notes for that tag.
- Every user-visible change adds a line in the commit that makes it.

## Artifacts

Each app release produces, under `artifacts/dist/`:

- `<App>-<version>-win-x64-Setup.exe`: Inno Setup, per-user by default with an all-users option, its own AppId and install folder, opt-in file associations, an uninstaller.
- `<App>-<version>-win-x64-Portable.zip`: the self-contained publish folder.
- `SHA256SUMS` covering both.

Self-contained .NET: no runtime prerequisite on the target machine. x64 today; win-arm64 is planned (`todo/05-release/`).

## Signing

Binaries and installers are not signed yet: there is no certificate. When one exists it is supplied to the packaging scripts from outside the repository (never in a tracked file, an argument, or a log), and signing is verified with `signtool verify /pa` before a release is published.

## The release checklist

A release tag is pushed only when every line holds, each quoted from a real run in the release section's evidence:

1. `pwsh scripts/check-all.ps1` exits 0 at the commit being tagged.
2. The app's `CHANGELOG.md` section is headed by the tag and lists every user-visible change since the last release.
3. The app's user guide under `docs/user/` covers every surface the release ships.
4. `pwsh scripts/package.ps1 -App <App>` produces the installer and the portable ZIP locally.
5. The installer installs, launches, and uninstalls on a clean Windows machine with no .NET SDK or runtime, per-user and all-users, and an upgrade over the previous release keeps the user's settings.
6. The portable ZIP runs from an empty folder.
7. After the tag is pushed, the `release` workflow is green and the GitHub release carries the installer, the ZIP, and `SHA256SUMS`, and the checksums match the downloads.
