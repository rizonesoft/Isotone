# Versioning and releases

The suite's apps version and release independently from one repository. The policy is [`standards/release.md`](../../standards/release.md); the decision is "SemVer from tags, automated" (operator, 2026-10-23, [decisions.md](decisions.md), "The unattended campaign"). Nothing in the source tree holds a version number.

**State on 2026-11-12:** the release workflow, its upload and feed steps, and the installer scripts exist; computing the version from the tag in CMake, the per-architecture packaging, and the changelog generation are planned in `todo/05-release/` (re-planned onto the native tree by `D00 T07 §5`). Until then the build reports the `ISOTONE_VERSION` cache variable (default `0.0.0`) and the real commit, `scripts/package.ps1` runs the advisory release gate and then stops, and `release.yml` refuses a release after the same gate. This page states the decided design and marks what is not built yet.

## Tag prefixes

| Tag | Versions | Released as (uploaded to `download.rizonesoft.com`) |
| --- | -------- | ---------------------------- |
| `stilus-v1.2.3` | Stilus | `Stilus-1.2.3-win-x64-Setup.exe`, `Stilus-1.2.3-win-x64-Portable.zip`, and the same pair for `win-arm64` |
| `gesso-v1.2.3` | Gesso | The same four files for Gesso |
| `albumen-v1.2.3` | Albumen | The same four files for Albumen |
| `isotone-v1.2.3` | Suite bundle | `Isotone-1.2.3-win-<arch>-Setup.exe`, `Isotone-1.2.3-win-<arch>-Portable.zip` |

Only tags with an app's own prefix move that app's version, so a `stilus-v` tag never moves Gesso's. The planned apps take `tinctura-v`, `capio-v`, and `folium-v` when their plans reach a release.

## How a version is computed

SemVer 2.0, computed by CMake from git at configure time (planned), with the same rules the retired tag-reading tool applied:

- **On a tagged commit:** the tag's version, for example `stilus-v1.2.3` gives `1.2.3`.
- **After a tag:** the next version as a prerelease with the commit height, where the next version is decided by the Conventional Commits since the tag that carry the app's scope: a breaking change (`!`) raises the major version, a `feat` the minor, a `fix` or `perf` the patch.
- **With no tag for that prefix:** `0.0.0-alpha.0.N`, where N is the commit height.
- **Build metadata:** the commit, for example `0.0.0-alpha.0.2+5a8bdd4c1f9e`.

What a binary carries:

| Where | Value |
| ----- | ----- |
| `isotone::core::version()` | The full SemVer (today the `ISOTONE_VERSION` cache variable, until the tag computation lands) |
| `isotone::core::build_id()` | The commit's first 12 hex digits, plus `-dirty` when tracked files differed from it; rewritten on every build by `native/cmake/WriteBuildId.cmake`, and read from `BUILD_ID.txt` in a `git archive` source tree |
| The version resource: product version | The full SemVer plus the commit |
| The version resource: file version | `Major.Minor.Patch.Build`, where Build is the CI run number and `0` locally. Win32 limits each part to 16 bits, so Build is taken modulo 65536 |

## Channels

A version with a hyphen is a prerelease in one of three channels: `alpha`, `beta`, and `rc` (`0.2.0-alpha.1`, `0.2.0-beta.3`, `0.2.0-rc.1`). Each channel has its own update feed, so a user on the stable feed is never offered a prerelease.

## Shared libraries

`isotone::core` and `isotone::ui` are static libraries and have no version of their own: each app's executable carries the copy it was built with, at that app's version. A suite bundle records which app versions it carries and does not re-version them.

## Changelogs

Each app's section of `CHANGELOG.md` is generated from the Conventional Commits carrying its scope (`feat(stilus):`, `fix(gesso):`, `perf(albumen):`), headed by the tag it ships as. The release workflow uses that section as the top of the release body; without one, the body says so and links the commits of the tag.

## Suite and per-app releases

Per-app tags release one app: its installers, portable ZIPs, and `SHA256SUMS`, uploaded to `download.rizonesoft.com` and never attached to the GitHub release. They never build or need the suite installer. An `isotone-v*` tag releases the Isotone Graphics Suite: one installer with one component per shipping app (`installer/Suite.iss`) and the combined portable ZIP. Installers are compiled with Inno Setup 7 as 64-bit Setup programs.

Releases never block development: each app release is a release-candidate section the campaign completes (built, tested, packaged, ready to sign, notes written) and a publish section that waits on the operator's rows in `todo/99-manual/` (the signing certificate, the download storage and its secrets).

The toolchain is not a version input: moving the toolchain pin (`native/toolchain.json`) changes no app's version. Only tags and commits do.

## Cutting a release

1. The release-candidate section has passed: every gate, the advisory release gate, the changelog section headed by the tag.
2. Tag the commit on `main` and push the tag:

   ```powershell
   git tag stilus-v0.2.0
   git push origin stilus-v0.2.0
   ```

3. `.github/workflows/release.yml` then (the steps after the gate are the planned native pipeline):
   - resolves the app from the prefix
   - runs the native advisory release gate (`python scripts/check-native-advisories.py --release-gate`)
   - refuses to go on when the distribution storage secrets are missing (a tag release fails; see below)
   - builds the distribution presets (`x64-dist`, `arm64-dist`), runs the tests, and packages
   - writes `SHA256SUMS`
   - writes the release body and the update feed with `scripts/release-manifest.ps1`
   - uploads the files to `<base>/<slug>/<version>/` with rclone and downloads each file back from the public URL to check its size and hash
   - creates the GitHub release with no attached files: the body is the CHANGELOG section, Download links to the uploaded files, the SHA-256 table, and a link to the tag's source
   - writes the update feed last, so the feed never names a release whose files or notes are missing

## Where the binaries live

Operator decision 2026-09-27: binaries are distributed only from rizonesoft.com. The files sit in S3-compatible object storage behind the CDN host `download.rizonesoft.com` (the provider is not chosen yet); GitHub releases carry the release notes, GitHub's automatic source archives, the SHA-256 table, and links to the downloads, and never an installer or a ZIP.

| What | Where |
| ---- | ----- |
| Release files | `https://download.rizonesoft.com/<slug>/<version>/<file>`, slug `stilus`, `gesso`, `albumen`, or `isotone` (the suite), for example `https://download.rizonesoft.com/stilus/0.1.0/Stilus-0.1.0-win-x64-Setup.exe` |
| Checksums | `https://download.rizonesoft.com/<slug>/<version>/SHA256SUMS`, and the same table in the GitHub release body |
| Update feed | `https://download.rizonesoft.com/update/<slug>.json` for the latest stable release, and one feed per prerelease channel (file names fixed by the release pipeline's section in `todo/05-release/`; `scripts/release-manifest.ps1` writes one `update/<slug>-prerelease.json` today) |
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

A pushed tag with any secret missing fails before anything is built, so no release is ever published without its downloads. The upload tool is rclone (MIT), fetched from its official release and checked against a pinned SHA-256; the secrets reach rclone only as environment variables, never on a command line or in a log.

## The draft dry run

`release.yml` also runs from a manual dispatch with a `tag` input and `draft` (default true):

```powershell
gh workflow run release.yml --ref main -f tag=stilus-v0.1.0-alpha.1 -f draft=true
```

The tag is not pushed: the draft release targets the dispatched commit, and a draft creates no tag until it is published. With the storage configured, the files and the feed go under `drafts/`; without it, the run skips the upload with a notice in its summary, and the files are only in the run's `dist-<tag>` workflow artifact. Delete the draft after inspection (`gh release delete <tag> --yes --cleanup-tag`) and remove its `drafts/` folder from the bucket. The native pipeline's first dry run is a section of `todo/05-release/`.

Only annotated or lightweight tags that match `<prefix>-v<SemVer>` are accepted. Anything else fails the workflow at the first step.
