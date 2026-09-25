# Versioning and releases

The suite's apps version and release independently from one repository. Versions come from git tags through [MinVer](https://github.com/adamralph/minver). Nothing in the source tree holds a version number.

## Tag prefixes

| Tag | Versions | Released by `release.yml` as |
| --- | -------- | ---------------------------- |
| `nodus-v1.2.3` | Nodus projects (`src/Nodus/**`) | `Nodus-1.2.3-win-x64-Setup.exe`, `Nodus-1.2.3-win-x64-Portable.zip` |
| `imago-v1.2.3` | Imago projects (`src/Imago/**`) | `Imago-1.2.3-win-x64-Setup.exe`, `Imago-1.2.3-win-x64-Portable.zip` |
| `lumen-v1.2.3` | Lumen (planned) | Refused until Lumen ships (`scripts/apps.psd1`, `installer/Lumen.iss`) |
| `photon-v1.2.3` | Suite bundle | `Photon-1.2.3-win-x64-Setup.exe`, `Photon-1.2.3-win-x64-Portable.zip` |

Each app's overlay (`src/<App>/Directory.Build.props`) sets `MinVerTagPrefix`. MinVer only considers tags with that prefix, so a `nodus-v` tag never moves Imago's version.

## How a version is computed

- **On a tagged commit:** the tag's version, for example `nodus-v1.2.3` gives `1.2.3`.
- **After a tag:** the next patch as a prerelease with the commit height, for example `1.2.4-alpha.0.5` five commits after `nodus-v1.2.3`.
- **With no tag for that prefix:** `0.0.0-alpha.0.N`, where N is the commit height.
- **Build metadata:** the commit SHA, for example `0.0.0-alpha.0.2+2e87a3d...`. It appears in `ProductVersion` / `InformationalVersion`.

MinVer settings (root `Directory.Build.props`): `MinVerDefaultPreReleaseIdentifiers=alpha.0`, `MinVerAutoIncrement=patch`.

Assembly attributes:

| Attribute | Value |
| --------- | ----- |
| `InformationalVersion` / `ProductVersion` | Full SemVer plus the commit SHA |
| `AssemblyVersion` | `Major.0.0.0` (MinVer default: a binding-stable major) |
| `FileVersion` | `Major.Minor.Patch.Build`, where Build is `GITHUB_RUN_NUMBER` on CI and `0` locally. Win32 limits each part to 16 bits, so Build is taken modulo 65536. Set in `Directory.Build.targets`. |

To check what a project would get:

```powershell
dotnet msbuild src/Nodus/Bezier.Desktop/Bezier.Desktop.csproj -t:MinVer -getProperty:MinVerVersion
```

## Shared libraries

Shared code (a future `src/Photon.Core`, or anything else without an app overlay) defaults to the `photon-v` prefix. When an app is published, a shared library takes the version of that app:

- `scripts/publish.ps1` passes `-p:MinVerTagPrefix=<app>-v` on the command line.
- A command-line property is a **global property**, which overrides the value set in any project file.
- Every project in the app's closure, shared libraries included, is therefore versioned from the app's tags.
- `-Version x.y.z` (or `package.ps1 -Version`) passes `MinVerVersionOverride` in the same way.

So `Photon.Core.dll` inside the Nodus 1.2.3 installer reports 1.2.3, and inside Imago 0.4.0 it reports 0.4.0. In a plain `dotnet build Photon.slnx`, shared libraries carry the `photon-v` version.

The suite bundle (`package.ps1 -Suite`) passes the `photon-v` version to every app's publish. All binaries in a suite installer therefore carry the suite version.

## Cutting a release

1. Add a CHANGELOG section whose heading names the tag, for example `## [nodus-v0.2.0] - 2026-10-01`. The release workflow uses that section as the release notes. Without one, GitHub generates notes from the commits.
2. Tag the commit on `main` and push the tag:

   ```powershell
   git tag nodus-v0.2.0
   git push origin nodus-v0.2.0
   ```

3. `.github/workflows/release.yml` then:
   - resolves the app from the prefix
   - runs the tests
   - runs `scripts/package.ps1`
   - writes `SHA256SUMS`
   - creates the GitHub release with the installer, the ZIP, and the checksums

   A version with a hyphen (`0.2.0-beta.1`) is published as a prerelease.

Only annotated or lightweight tags that match `<prefix>-v<SemVer>` are accepted. Anything else fails the workflow at the first step.

## Local packaging of a specific version

```powershell
pwsh scripts/package.ps1 -App Imago -Version 0.2.0
pwsh scripts/package.ps1 -Suite -Version 1.0.0
```

With no `-Version`, the version is whatever MinVer computes for the current commit.
