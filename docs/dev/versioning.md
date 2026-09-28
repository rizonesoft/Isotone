# Versioning and releases

The suite's apps version and release independently from one repository. Versions come from git tags through [MinVer](https://github.com/adamralph/minver). Nothing in the source tree holds a version number.

## Tag prefixes

| Tag | Versions | Built by `release.yml` as (uploaded to `download.rizonesoft.com`) |
| --- | -------- | ---------------------------- |
| `stilus-v1.2.3` | Stilus projects (`src/Stilus/**`) | `Stilus-1.2.3-win-x64-Setup.exe`, `Stilus-1.2.3-win-x64-Portable.zip` |
| `gesso-v1.2.3` | Gesso projects (`src/Gesso/**`) | `Gesso-1.2.3-win-x64-Setup.exe`, `Gesso-1.2.3-win-x64-Portable.zip` |
| `albumen-v1.2.3` | Albumen (planned) | Refused until Albumen ships (`scripts/apps.psd1`, `installer/Albumen.iss`) |
| `isotone-v1.2.3` | Suite bundle | `Isotone-1.2.3-win-x64-Setup.exe`, `Isotone-1.2.3-win-x64-Portable.zip` |

Each app's overlay (`src/<App>/Directory.Build.props`) sets `MinVerTagPrefix`. MinVer only considers tags with that prefix, so a `stilus-v` tag never moves Gesso's version.

## How a version is computed

- **On a tagged commit:** the tag's version, for example `stilus-v1.2.3` gives `1.2.3`.
- **After a tag:** the next patch as a prerelease with the commit height, for example `1.2.4-alpha.0.5` five commits after `stilus-v1.2.3`.
- **With no tag for that prefix:** `0.0.0-alpha.0.N`, where N is the commit height.
- **Build metadata:** the commit SHA, for example `0.0.0-alpha.0.2+5a8bdd4...`. It appears in `ProductVersion` / `InformationalVersion`.

MinVer settings (root `Directory.Build.props`): `MinVerDefaultPreReleaseIdentifiers=alpha.0`, `MinVerAutoIncrement=patch`.

Assembly attributes:

| Attribute | Value |
| --------- | ----- |
| `InformationalVersion` / `ProductVersion` | Full SemVer plus the commit SHA |
| `AssemblyVersion` | `Major.0.0.0` (MinVer default: a binding-stable major) |
| `FileVersion` | `Major.Minor.Patch.Build`, where Build is `GITHUB_RUN_NUMBER` on CI and `0` locally. Win32 limits each part to 16 bits, so Build is taken modulo 65536. Set in `Directory.Build.targets`. |

To check what a project would get:

```powershell
dotnet msbuild src/Stilus/Bezier.Desktop/Bezier.Desktop.csproj -t:MinVer -getProperty:MinVerVersion
```

## Shared libraries

Shared code (a future `src/Isotone.Core`, or anything else without an app overlay) defaults to the `isotone-v` prefix. When an app is published, a shared library takes the version of that app:

- `scripts/publish.ps1` passes `-p:MinVerTagPrefix=<app>-v` on the command line.
- A command-line property is a **global property**, which overrides the value set in any project file.
- Every project in the app's closure, shared libraries included, is therefore versioned from the app's tags.
- `-Version x.y.z` (or `package.ps1 -Version`) passes `MinVerVersionOverride` in the same way.

So `Isotone.Core.dll` inside the Stilus 1.2.3 installer reports 1.2.3, and inside Gesso 0.4.0 it reports 0.4.0. In a plain `dotnet build Isotone.slnx`, shared libraries carry the `isotone-v` version.

The suite bundle (`package.ps1 -Suite`) passes the `isotone-v` version to every app's publish. All binaries in a suite installer therefore carry the suite version.

## Suite and per-app releases

Per-app tags (`stilus-v*`, `gesso-v*`) release one app: `release.yml` runs `package.ps1 -App <App>` and publishes only that app's installer, portable ZIP, and `SHA256SUMS` (to `download.rizonesoft.com`, never attached to the GitHub release). It never builds or needs the suite installer. An `isotone-v*` tag releases the Isotone Graphics Suite: `package.ps1 -Suite` builds `Isotone-<version>-win-x64-Setup.exe` (`installer/Suite.iss`, one component per shipping app) and the combined portable ZIP. Installers are compiled with Inno Setup 7 as 64-bit Setup programs.

The toolchain is not a version input: moving the SDK pin (today the .NET 11 release candidate, GA through `D00 T02 §8`) changes no app's version. Only tags do.

## Cutting a release

1. Add a CHANGELOG section whose heading names the tag, for example `## [stilus-v0.2.0] - 2026-10-01`. The release workflow uses that section as the top of the release body. Without one, the body says so and links the commits of the tag.
2. Tag the commit on `main` and push the tag:

   ```powershell
   git tag stilus-v0.2.0
   git push origin stilus-v0.2.0
   ```

3. `.github/workflows/release.yml` then:
   - resolves the app from the prefix
   - refuses to go on when the distribution storage secrets are missing (a tag release fails; see below)
   - runs the tests
   - runs `scripts/package.ps1`
   - writes `SHA256SUMS`
   - writes the release body and the update feed with `scripts/release-manifest.ps1`
   - uploads the installer, the ZIP, and `SHA256SUMS` to `<base>/<slug>/<version>/` with rclone and downloads each file back from the public URL to check its size and hash
   - creates the GitHub release with no attached files: the body is the CHANGELOG section, Download links to the uploaded files, the SHA-256 table, and a link to the tag's source
   - writes the update feed to `<base>/update/<slug>.json` (or `<slug>-prerelease.json`) last, so the feed never names a release whose files or notes are missing

   A version with a hyphen (`0.2.0-beta.1`) is published as a prerelease.

## Where the binaries live

Operator decision 2026-09-27: binaries are distributed only from rizonesoft.com. The files sit in S3-compatible object storage behind the CDN host `download.rizonesoft.com` (the provider is not chosen yet); GitHub releases carry the release notes, GitHub's automatic source archives, the SHA-256 table, and links to the downloads, and never an installer or a ZIP.

| What | Where |
| ---- | ----- |
| Release files | `https://download.rizonesoft.com/<slug>/<version>/<file>`, slug `stilus`, `gesso`, `albumen`, or `isotone` (the suite), for example `https://download.rizonesoft.com/stilus/0.1.0/Stilus-0.1.0-win-x64-Setup.exe` |
| Checksums | `https://download.rizonesoft.com/<slug>/<version>/SHA256SUMS`, and the same table in the GitHub release body |
| Update feed | `https://download.rizonesoft.com/update/<slug>.json` for the latest stable release, `update/<slug>-prerelease.json` for the latest prerelease |
| Product page | one value, `ISOTONE_SITE_URL` (default `https://www.rizonesoft.com/`), with `?utm_source=github&utm_medium=<place>` on links from GitHub |
| Draft dry runs | under `drafts/` (`drafts/<slug>/<version>/`, `drafts/update/`), never the live paths |

The feed is JSON: `schema` (1), `app`, `name`, `version`, `prerelease`, `date`, `tag`, `url` (the x64 installer), `sha256`, `size`, `notes` (the GitHub release page), `page` (the product page), `source` (the tag on GitHub), `sha256sums`, and `files` (every file with its `name`, `kind`, `runtime`, `url`, `sha256`, and `size`). A published file is never replaced: the upload runs with `--immutable`, so re-running a release with different bytes fails instead of changing a download people already verified.

The workflow reads these repository settings (Settings, Secrets and variables, Actions):

| Name | Kind | Meaning |
| ---- | ---- | ------- |
| `ISOTONE_DL_S3_ENDPOINT` | secret | The S3 API endpoint of the storage provider |
| `ISOTONE_DL_S3_BUCKET` | secret | The bucket behind `download.rizonesoft.com` |
| `ISOTONE_DL_S3_ACCESS_KEY_ID` | secret | An access key limited to that bucket |
| `ISOTONE_DL_S3_SECRET_ACCESS_KEY` | secret | Its secret |
| `ISOTONE_DL_BASE_URL` | variable | The public base URL (default `https://download.rizonesoft.com`) |
| `ISOTONE_SITE_URL` | variable | The product page (default `https://www.rizonesoft.com/`), also the installer's publisher URL |

A pushed tag with any secret missing fails at its second step, before anything is built, so no release is ever published without its downloads. The upload tool is rclone (MIT), fetched from its official release and checked against a pinned SHA-256 (`RCLONE_VERSION` and `RCLONE_SHA256` in the workflow); the secrets reach rclone only as environment variables, never on a command line or in a log.

## The draft dry run

`release.yml` also runs from a manual dispatch with a `tag` input and `draft` (default true), the mode `D00 T02 §7` uses for `stilus-v0.1.0-alpha.1`:

```powershell
gh workflow run release.yml --ref main -f tag=stilus-v0.1.0-alpha.1 -f draft=true
```

The tag is not pushed: the draft release targets the dispatched commit, and a draft creates no tag until it is published. With the storage configured, the files and the feed go under `drafts/`; without it, the run skips the upload with a notice in its summary, and the files are only in the run's `dist-<tag>` workflow artifact (`gh run download <run id> -n dist-<tag>`). Delete the draft after inspection (`gh release delete <tag> --yes --cleanup-tag`) and remove its `drafts/` folder from the bucket.

Only annotated or lightweight tags that match `<prefix>-v<SemVer>` are accepted. Anything else fails the workflow at the first step.

## Local packaging of a specific version

```powershell
pwsh scripts/package.ps1 -App Gesso -Version 0.2.0
pwsh scripts/package.ps1 -Suite -Version 1.0.0
```

With no `-Version`, the version is whatever MinVer computes for the current commit.
