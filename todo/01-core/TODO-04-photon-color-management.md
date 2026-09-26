---
schema_version: 1
id: photon-color-management
domain: 01-core
status: draft
title: "TODO-04 -- Photon.Core Color Management: ICC Transforms, Proofing, and Bitmap Color Modes"
depends_on: []
track: C4
---

# TODO-04 -- Photon.Core Color Management: ICC Transforms, Proofing, and Bitmap Color Modes

> **Goal:** Photon.Core gains one color-management engine for the suite under `src/Photon.Core/Color/`: a recorded decision (lcms2, MIT, through a thin `LibraryImport` P/Invoke wrapper with the native DLL bundled per RID, against Windows WCS as the rejected candidate), ICC v2 and v4 profile loading, RGB, CMYK, gray, and Lab transforms with rendering intents, black point compensation, proofing transforms, and a gamut API (§1 and §2, Phase 6), then bitmap color modes including duotone and multichannel (§3, Phase 10). It lives in Photon.Core, not in an app, because the operator-mandated Photon.Core pixel engine (`D01 T03 §3`) needs it for Lab, CMYK, and duotone bitmaps, and Imago's ICC work (`D03 T04 §2`) and Lumen's output transform (`D04 T02 §2`) are its next consumers; Nodus's color model (`D02 T09 §1`) is its first. The engine part of backlog B-023 (Imago color management) is superseded by this file's §1 decision.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `src/Photon.Core/` does not exist yet; `D01 T02 §1` creates it. No ICC code exists anywhere in the tree: no lcms binding, no WPF `ColorContext` use, and no profile type in any `.cs` file under `src/`. Nodus's only color type is the sRGB byte struct `Color` in `src/Nodus/Bezier.Core/Models/Color.cs` with HSL and HSV math and no CMYK, Lab, or spot representation. The engine decision sat in the backlog as part of B-023 (Imago color management), recorded there as undecided between an lcms2 wrapper and WCS; B-023 was reworded on 2026-09-26 to consume this file.
<!-- claim: absent src/Photon.Core/Photon.Core.csproj -->
<!-- claim: count "lcms|IccProfile|ColorContext" src/**/*.cs = 0 -->
<!-- claim: count "public readonly struct Color" src/Nodus/Bezier.Core/Models/Color.cs = 1 -->
<!-- claim: count "Cmyk|\bLab\b|Spot" src/Nodus/Bezier.Core/Models/Color.cs = 0 -->
<!-- claim: count "B-023\]" todo/backlog.md = 1 -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- the dependency rule (a package is a decision, license checked against GPL-3.0), logging, and async and cancellation rules this library follows
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- "Formats and licensing" records lcms2 (MIT) as the engine and WCS as the alternative; "What goes to Photon.Core and Photon.UI" records why this engine is shared
- [`docs/parity/nodus-parity.md`](../../docs/parity/nodus-parity.md) -- the catalog rows NP-2076 to NP-2085 this file owns
- [lcms2 2.16 API reference](https://github.com/mm2/Little-CMS/blob/master/doc/LittleCMS2.16%20API.pdf) -- the function set the wrapper binds; `transicc` is the golden oracle
- [ICC.1:2022 (profile version 4.4)](https://www.color.org/specification/ICC.1-2022-05.pdf) -- the profile format the loader validates
- [`../backlog.md`](../backlog.md) -- B-023's engine part is superseded by §1; its Assign, Convert, and soft-proof parts stay with Imago; the "wrapper moves to Photon.Core" note of B-011 (promoted into `D02 T13 §2`) is fulfilled by §1
- -> XREF: D01 T02 §1 -- Photon.Core and its app-data paths, which §1 builds inside
- -> XREF: D01 T02 §2 -- the settings store holding default profiles, intent, and black point keys
- -> XREF: D01 T03 §3 -- the pixel buffers and quantization §3 converts between modes
- -> XREF: D02 T09 §1 -- the first consumer: Nodus's `PaintColor` converts through §1 and warns through §2
- -> XREF: D02 T09 §2 -- the Color panel's out-of-gamut warning calls §2's gamut API
- -> XREF: D02 T13 §1 -- document color settings, profile UI, and Load Profile surface §1
- -> XREF: D02 T13 §6 -- soft proofing and the gamut overlay consume §2's proof transform and gamut mask
- -> XREF: D02 T13 §14 -- PDF output intents and DeviceN duotone images read §1 profiles and §3 specs
- -> XREF: D02 T12 §1 -- Nodus bitmap objects, whose Lab, CMYK, and duotone mode commands wait for §3
- -> XREF: D02 T14 §2 -- PDF import maps DeviceN duotone images into §3's `DuotoneSpec` and reads ICC-based spaces through §1
- -> XREF: D03 T04 §2 -- Imago's embedded PNG and JPEG profiles are this engine's next consumer
- -> XREF: D04 T02 §2 -- Lumen's output transform to sRGB, Display P3, and Adobe RGB is a later consumer

## Outcome

- `docs/dev/decisions.md` records lcms2 as the suite's color engine with WCS as the rejected candidate, both licenses, a coverage table, and the cost of changing.
- `src/Photon.Core/Color/` loads ICC v2 and v4 profiles, converts RGB, CMYK, gray, and Lab values and 8 and 16 bit buffers, and matches `transicc` goldens within Delta E 2000 0.5.
- Every rendering intent, black point compensation, preserve pure black, map gray to K, proofing transforms, and a gamut API with bring-into-gamut are available and tested against goldens.
- Bitmap buffers convert between Gray8, Rgb24, Lab24, and Cmyk32; duotone (one to four inks with curves and overprint colors) and multichannel images render, save, and reload exactly; Photoshop `.ado` ink files read.
- Nodus exposes the Duotone dialog from Bitmaps, Mode, applying one undoable command.

**Adjacency:** list=applicable; document=not-applicable (the engine prints nothing; PDF output intents are written by D02 T13 §15 and print by D02 T13 §2); settings=applicable; reporting=not-applicable (profile details are shown by the consumer's color settings surface, D02 T13 §1); notifications=not-applicable (a library: long bitmap conversions take IProgress and CancellationToken and the consuming app's status strip reports them); permissions=applicable @ D01 T04 §1; audit=applicable @ D01 T04 §1; exchange=applicable; reverse=applicable

**Adjacency rationale:** The profile store lists installed and system profiles filterable by class and color space; default profiles, intent, black point compensation, preserve black, and map gray are settings-store keys read by the transform factory; a corrupt or unreadable profile and the read-only system color folder are refused by name; every profile import and removal writes a log line and bitmap mode conversions are undoable commands in the consumer; ICC v2 and v4 profiles and duotone ink files are read and written with fixtures; an imported profile can be removed and every conversion undone.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The engine decision, the lcms2 wrapper, profiles, the profile store, and RGB, CMYK, gray, and Lab transforms | D01 T02 §1 |  [ ]   |
|   2   |   §2    | Rendering intents, black point compensation, proofing transforms, and gamut checks | §1 |  [ ]   |
|   3   |   §3    | Bitmap color modes, duotone, and multichannel, with the Nodus Duotone dialog | §2, D01 T03 §3 |  [ ]   |

---

## 1. The Color-Management Engine Decision and ICC Transforms

The suite needs one color engine, and it needs it before Nodus's color model (`D02 T09 §1`) can store CMYK and Lab values that convert the same way every time. This section records the engine decision, ships lcms2 natively per RID behind a thin source-generated P/Invoke wrapper, and gives `Photon.Core` profile loading, a profile store, default profiles, and value and buffer transforms between RGB, CMYK, gray, and Lab. It must not leak native handles or ship a profile whose license forbids redistribution. Catalog: NP-2076 to NP-2077 (2 features: NP-2076 Load ICC color profiles, NP-2077 Color engine choice, answered by the decision so settings show the engine name and version rather than a choice).

**Fidelity:** no surface of its own (Load Profile and the engine name are surfaced by `D02 T13 §1`).

**Needs:** Windows host (build/test)

- [ ] Add a decision row to `docs/dev/decisions.md`: lcms2 (MIT, GPL-3.0 compatible, ICC v4, proofing, K-preserving intents) against Windows WCS (`mscms.dll`, no package, weaker v4 support, no K-preserving intents), with license URLs, a coverage table, the cost of changing (one wrapper class), and the justified default lcms2. Done when: the row names both candidates, both licenses, and this section's ref.
- [ ] Build lcms2 2.16 or later for `win-x64` and `win-arm64` with `build/native/lcms2/build.ps1`, recording the source tarball SHA-256 and compiler version in `build/native/lcms2/SOURCE.txt`, and commit the binaries under `src/Photon.Core/runtimes/<rid>/native/lcms2.dll`. Done when: both DLLs exist and `SOURCE.txt` names the upstream tag and hash. Cheaper substitute: an unpinned DLL copied from another product, which the hash record rejects.
- [ ] Pack the natives from `src/Photon.Core/Photon.Core.csproj` (`<None Include="runtimes/**" Pack="true" CopyToOutputDirectory="PreserveNewest" />`) and add lcms2's MIT license text to `src/Photon.Core/THIRD-PARTY-NOTICES.md`. Done when: `dotnet publish` of Nodus for `win-x64` places `lcms2.dll` beside `Nodus.exe` and the notice file names lcms2.
- [ ] Add `src/Photon.Core/Color/Native/Lcms2.cs`: `[LibraryImport("lcms2")]` bindings for `cmsOpenProfileFromMem`, `cmsCloseProfile`, `cmsCreateTransform`, `cmsDoTransform`, `cmsDeleteTransform`, `cmsGetColorSpace`, `cmsGetDeviceClass`, `cmsGetProfileVersion`, `cmsGetProfileInfoUTF8`, `cmsCreate_sRGBProfile`, `cmsCreateLab4Profile`, and `cmsCreateGrayProfile`. Done when: the file compiles with `AllowUnsafeBlocks` off and the analyzers report no marshalling warning. Source: lcms2 2.16 API reference, section 3.
- [ ] Add `SafeProfileHandle` and `SafeTransformHandle` (`SafeHandle` subclasses releasing through `cmsCloseProfile` and `cmsDeleteTransform`) in `src/Photon.Core/Color/Native/`. Done when: `NativeHandleTests` create and dispose 10,000 transforms without the process private bytes growing more than 5 MB.
- [ ] Add `src/Photon.Core/Color/IccProfile.cs` (description, `ProfileClass`, `ColorSpace`, PCS, version, raw bytes, SHA-256) with `IccProfile.Load(ReadOnlySpan<byte>)` returning a result that names the failure for truncated, wrong-signature, or unsupported-class data. Done when: `IccProfileTests` load committed v2 and v4 fixtures and refuse a truncated copy with a message naming the file.
- [ ] Add `src/Photon.Core/Color/ColorValue.cs`: a `readonly record struct` carrying `ColorSpaceKind` (Rgb, Cmyk, Gray, Lab) and up to four `double` components with range validation. Done when: constructing CMYK with a component above 100 throws `ArgumentOutOfRangeException`.
- [ ] Add `src/Photon.Core/Color/ColorTransformService.cs`: `Convert(ColorValue, IccProfile source, IccProfile target, TransformOptions)` with transforms cached by profile-hash pair, intent, and flags, thread-safe through a `ConcurrentDictionary` of lazily created handles. Done when: `ColorTransformServiceTests` convert from four threads at once and the cache holds one transform per key.
- [ ] Add span-based bulk conversion `ConvertPixels(ReadOnlySpan<byte> source, PixelFormatKind, Span<byte> target, PixelFormatKind, ...)` for 8 and 16 bit RGB, RGBA (alpha copied untouched), CMYK, gray, and Lab. Done when: a 16 bit round trip sRGB to Lab to sRGB changes no channel by more than 1/65535 times 64.
- [ ] Add default profiles: sRGB, Lab D50, and gray gamma 2.2 built in through the lcms2 creators, plus one redistributable CMYK profile (the ECI `ISOcoated_v2_eci.icc` for FOGRA39, or an ICC-registry CRPC profile if the ECI terms fail review) under `src/Photon.Core/Color/Profiles/` with its license beside it. Done when: `DefaultProfilesTests` load all four and the license file quotes the redistribution grant. Cheaper substitute: bundling a vendor profile without its grant, which the license review refuses.
- [ ] Add `src/Photon.Core/Color/ColorProfileStore.cs` enumerating the suite folder `%LOCALAPPDATA%\Rizonesoft\Photon\Color\Profiles\` and read-only `%WINDIR%\System32\spool\drivers\color`, filterable by class and color space. Done when: `ColorProfileStoreTests` list a temp folder of three fixtures filtered to CMYK output profiles.
- [ ] `ColorProfileStore.Import(path)` validates by opening the profile, copies it into the suite folder through the atomic writer, refuses a corrupt file or a system-folder write by name (the permissions case: the Windows color folder is read-only to Nodus), and logs one Information line as the audit record; `Remove(id)` deletes only suite-folder profiles and logs. Done when: `ColorProfileStoreTests` import a v4 fixture, refuse `corrupt.icc` with a message naming it, refuse removing a system profile, and read the log lines back from an in-memory Serilog logger.
- [ ] Register settings keys `color.defaultRgbProfile`, `color.defaultCmykProfile`, and `color.defaultGrayProfile` in the `Photon.Core` settings store, with `ColorTransformService` and `D02 T09 §1`'s document profiles as the named consumers. Done when: a settings test changes the CMYK key and the next `ColorTransformService` default CMYK profile is the new one.
- [ ] Expose `ColorEngineInfo` (name `lcms2`, native version from `cmsGetEncodedCMMversion`) for the color settings surface of `D02 T13 §1`. Done when: a test asserts the version is at least 2160.
- [ ] Register `ColorTransformService`, `ColorProfileStore`, and `ColorEngineInfo` as singletons through `PhotonCoreServiceCollectionExtensions.AddPhotonColor()`. Done when: a composition test resolves all three from a fresh `ServiceCollection`.
- [ ] Commit fixtures under `tests/fixtures/core/icc/`: a v2 sRGB, a v4 sRGB, the default CMYK profile, a gray profile, `corrupt.icc`, and `samples-100.csv` (100 sRGB sample colors), plus `transicc-goldens.csv` produced by lcms2's own `transicc` with its version in `tests/fixtures/core/icc/VERSION.txt`. Done when: the folder README lists each file, its source, and its license.
- [ ] Add `TransiccGoldenTests` in `tests/Photon.Core.Tests/Color/` converting all 100 samples sRGB to CMYK, gray, and Lab and back through `ColorTransformService`. Done when: every sample is within Delta E 2000 0.5 of the golden.
- [ ] Commit: `"core: the lcms2 color engine, ICC profiles, the profile store, and value and buffer transforms"`

**Test checkpoint:** Unit test and builds clean: `dotnet build Photon.slnx -c Release` exits 0 and `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Core.Tests.Color"` exits 0 with `IccProfileTests`, `ColorTransformServiceTests`, `ColorProfileStoreTests`, and `TransiccGoldenTests` reporting; the golden test compares 100 committed sample colors through sRGB, CMYK, gray, and Lab against `transicc` output (version recorded) within Delta E 2000 0.5. Cheaper substitute that fails: hand-written sRGB-to-CMYK formulas, which the CMYK expectations reject.

## 2. Rendering Intents, Black Point Compensation, Proofing Transforms, and Gamut Checks

A value that converts is not yet a value that prints as intended: print designers choose an intent, keep 100 percent K black, simulate the press on screen, and need to know which colors fall outside the press gamut. This section adds those controls to the §1 engine as options and a proof transform, plus a gamut API that `D02 T09 §2`'s out-of-gamut warning and `D02 T13 §6`'s gamut overlay consume. Catalog: NP-2078 to NP-2081 (4 features: NP-2078 Bring color into gamut, NP-2079 Rendering intents: perceptual, relative, absolute, saturation, NP-2080 Preserve pure black, NP-2081 Map gray to CMYK black).

**Fidelity:** no surface of its own (consumed by `D02 T09 §2`'s gamut warning and by `D02 T13 §1` and `D02 T13 §6`).

**Needs:** Windows host (build/test)

- [ ] Add `src/Photon.Core/Color/RenderingIntent.cs` (Perceptual, RelativeColorimetric, Saturation, AbsoluteColorimetric) mapped to `INTENT_PERCEPTUAL`, `INTENT_RELATIVE_COLORIMETRIC`, `INTENT_SATURATION`, and `INTENT_ABSOLUTE_COLORIMETRIC`. Done when: a mapping test covers all four values.
- [ ] Extend `TransformOptions` with `Intent`, `BlackPointCompensation` (`cmsFLAGS_BLACKPOINTCOMPENSATION`), `PreservePureBlack`, and `MapGrayToK`, and include them in the §1 cache key. Done when: two conversions differing only in intent return different transforms from the cache.
- [ ] Implement preserve pure black through lcms2's `INTENT_PRESERVE_K_ONLY_PERCEPTUAL` and `INTENT_PRESERVE_K_ONLY_RELATIVE_COLORIMETRIC` for CMYK-to-CMYK transforms. Done when: `PreserveBlackTests` convert 0,0,0,100 between two CMYK profiles and get exactly 0,0,0,100.
- [ ] Implement map gray to K in `ColorTransformService`: neutral RGB or gray input (a <= 0.5 and b <= 0.5 in Lab) bypasses the CMYK profile and becomes K only, through the profile's K curve. Done when: `MapGrayToKTests` convert sRGB 128,128,128 to 0,0,0,K and a non-neutral color through the profile.
- [ ] Add `src/Photon.Core/Color/ProofTransform.cs` over `cmsCreateProofingTransform` with `cmsFLAGS_SOFTPROOFING`: simulate a device profile, simulate paper color (absolute colorimetric on the proof leg), and preserve numbers (identity when source and proof profile are the same space). Done when: `ProofTransformTests` match `transicc` proof goldens within Delta E 2000 0.5 for both paper-color settings.
- [ ] Add `IsInGamut(ColorValue, IccProfile)` in `src/Photon.Core/Color/GamutService.cs` through `cmsFLAGS_GAMUTCHECK` plus a Delta E 2000 round-trip threshold read from setting `color.gamutThreshold` (default 2.0). Done when: `GamutTests` report sRGB 0,255,0 out of gamut against the default CMYK profile and sRGB 128,128,128 in gamut.
- [ ] Add `BringIntoGamut(ColorValue, IccProfile)` by a relative colorimetric round trip through the target profile, returning the nearest printable color in the source space. Done when: the brought color of sRGB 0,255,0 passes `IsInGamut` and differs from the input by the round trip's Delta E.
- [ ] Add `GamutMask(ReadOnlySpan<byte> pixels, PixelFormatKind, IccProfile, Span<byte> mask)` for the gamut warning overlay of `D02 T13 §6`. Done when: a 3 by 1 fixture of in, out, in pixels yields mask 0, 255, 0.
- [ ] Register settings keys `color.renderingIntent` (default RelativeColorimetric), `color.blackPointCompensation` (default true), `color.preservePureBlack` (default true), and `color.mapGrayToK` (default false) with `TransformOptions.FromSettings` as the named consumer. Done when: a settings test flips each key and the next default options object reflects it.
- [ ] Bulk conversions above one second take `IProgress<double>` and `CancellationToken`; cancellation leaves the target span untouched past the last completed row and returns a cancelled result. Done when: a test cancels a 50-megapixel conversion after the first progress report and asserts the result is cancelled and no exception escapes.
- [ ] Measure a 100-megapixel RGB-to-CMYK conversion in `ColorPerformanceTests` (trait `Category=Performance`) and record the baseline in `docs/dev/color-engine.md`. Done when: the page quotes the machine, the time, and the megapixels per second.
- [ ] Add `RenderingIntentTests` comparing every intent with and without black point compensation against `transicc` goldens committed as `tests/fixtures/core/icc/intent-goldens.csv`. Done when: all 8 combinations over 100 samples are within Delta E 2000 0.5.
- [ ] Log each transform-cache miss at Debug with source, target, intent, and flags. Done when: an in-memory Serilog logger records one line per first use of a key.
- [ ] Commit: `"core: rendering intents, black point compensation, proofing, and gamut checks"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Core.Tests.Color"` exits 0 with `RenderingIntentTests`, `ProofTransformTests`, `GamutTests`, `PreserveBlackTests`, and `MapGrayToKTests` reporting; goldens from `transicc` for every intent with and without black point compensation and for the proof transform hold within Delta E 2000 0.5. Cheaper substitute that fails: ignoring the intent argument, which the perceptual versus relative expectations reject.

## 3. Bitmap Color Modes: Grayscale, Lab, CMYK, Duotone, and Multichannel

Placed bitmaps in a print document need the same color modes the press uses: grayscale, Lab, CMYK, duotone with spot inks, and multichannel plates. This section converts `D01 T03 §3`'s pixel buffers between modes through the §1 and §2 engine, adds the duotone and multichannel models and renderer, reads Photoshop `.ado` ink files, and gives Nodus a Duotone dialog. It runs in Phase 10 after the pixel engine ships. `D02 T12 §1`'s Lab, CMYK, and duotone mode commands wait for this section by name. Catalog: NP-2082 to NP-2085 (4 features: NP-2082 Duotone types: monotone to quadtone, NP-2083 Duotone ink tone curves, NP-2084 Duotone save and load inks, NP-2085 Duotone overprint colors).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/duotone/.
**Job:** a print designer can convert a placed bitmap to duotone or another color mode and print its inks as spot plates. Consumer: the bitmap object, separations (`D02 T13 §5`), and PDF DeviceN output (`D02 T13 §14`).
**Treatment:** a Duotone dialog with type (monotone, duotone, tritone, quadtone), per-ink color and tone curve, show all curves, save and load inks, and an overprint colors editor with live preview. Cheaper substitute that fails the checkpoint: a grayscale image tinted with one RGB color.
**Chrome:** consume the engine from §1 and §2, `D01 T03 §1`'s pixel buffers, the Nodus picker from `D02 T09 §2` for ink colors, and the theme. The dialog lives in `Photon.Nodus.Desktop` until a second app needs it; do not build a second curve editor or picker.

**Requires:** display-session -- the Duotone dialog needs an interactive desktop

- [ ] Add `src/Photon.Core/Color/BitmapModes/BitmapColorMode.cs` (Gray8, Rgb24, Lab24, Cmyk32, Duotone, Multichannel) and `BitmapModeConverter.cs` converting `D01 T03 §1` pixel buffers between Gray8, Rgb24, Lab24, and Cmyk32 through `ColorTransformService` with the document profiles and intent. Done when: `BitmapModeConverterTests` convert a 64 by 64 fixture through every pair and match `transicc` goldens within Delta E 2000 0.5.
- [ ] Make `BitmapModeConverter.ConvertAsync` cancellable with `IProgress<double>`; a cancelled conversion returns the untouched source buffer. Done when: a cancel test asserts the source hash is unchanged.
- [ ] Add `src/Photon.Core/Color/BitmapModes/DuotoneSpec.cs`: 1 to 4 inks (name, spot or process `ColorValue`), a tone curve per ink as up to 13 points on 0 to 100, and an overprint `ColorValue` per ink pair; the image stores its gray channel plus the spec. Done when: a spec with 5 inks is refused by name and a quadtone spec holds 6 overprint pairs.
- [ ] Add `DuotoneRenderer` compositing inks for display through the §2 proof transform, with overprint colors overriding the multiplicative mix of each ink pair. Done when: `DuotoneRendererTests` match committed snapshot goldens under `tests/fixtures/core/duotone/goldens/` within 2/255 per channel.
- [ ] Add property tests to `DuotoneRendererTests`: alpha is preserved, output is deterministic across two runs, and a monotone with a linear curve equals the ink's tint ramp. Done when: all three properties pass over 200 generated inputs.
- [ ] Add `DuotonePlateExtractor` producing one gray plate per ink (the curve applied to the gray channel) for `D02 T13 §5`'s separations. Done when: a duotone fixture yields two plates whose values equal the curves applied to the source.
- [ ] Add `src/Photon.Core/Color/BitmapModes/DuotoneInkFile.cs` saving and loading ink sets as `.photonduotone` JSON through System.Text.Json source generation and the atomic writer. Done when: a round trip of a tritone spec is equal member by member.
- [ ] Add `AdoReader` reading Photoshop `.ado` duotone files per Adobe's published Photoshop File Formats Specification (duotone options section). Done when: `AdoReaderTests` read the committed `tests/fixtures/core/duotone/sample-tritone.ado` into three inks with their curves and names, and refuse a truncated copy by name.
- [ ] Add `MultichannelImage` holding N named 8-bit channels as spot plates with no composite conversion, displayed through the same ink composite as duotone. Done when: a test converts a CMYK buffer to multichannel and back without changing any byte.
- [ ] Add `AutoConvertForEffect` helper: an RGB-only effect runs on an RGB copy and the result converts back to the image's mode, recording the round trip in the returned result. Done when: a test applies an identity effect to a CMYK buffer and the round-trip Delta E is reported and below 1.0.
- [ ] Add `src/Nodus/Photon.Nodus.Desktop/Views/Bitmaps/DuotoneDialog.xaml` and `DuotoneDialogViewModel` with type, per-ink color (the `D02 T09 §2` picker), per-ink curve editor, Show All Curves, Save Inks, Load Inks (`.photonduotone` and `.ado`), and an Overprint Colors editor, with live canvas preview. Done when: the view model test changes the type from duotone to tritone and a third ink row appears. Cheaper substitute: a single tint color field, which the per-ink plate assertion rejects.
- [ ] Wire Bitmaps, Mode (Grayscale, RGB, Lab, CMYK, Duotone, Multichannel) in Nodus, each mode change one undoable `SetBitmapColorModeCommand` logging `Converted {Element} to {Mode}` at Information. Done when: undo restores the original pixels byte for byte in `SetBitmapColorModeCommandTests`.
- [ ] Persist the duotone spec in Nodus SVG as `nodus:duotone` (JSON of the spec) on the `<image>` element with the gray channel as the image data and a composited RGB PNG as the fallback per the live-object contract of `D02 T07 §1`. Done when: reopening the saved fixture restores the spec exactly and Inkscape 1.4 shows the composited fallback.
- [ ] Note in `src/Photon.Core/Color/BitmapModes/README.md` that `D02 T14 §2`'s PDF import maps DeviceN duotone images into `DuotoneSpec`. Done when: the README names the ref.
- [ ] Commit fixtures under `tests/fixtures/core/duotone/`: `sample-tritone.ado`, `duotone-image.svg` (a Nodus SVG with a duotone image), and snapshot goldens, with a README naming each file's source and license. Done when: the README lists every file.
- [ ] Update `docs/user/nodus/bitmaps.md` with color modes and the Duotone dialog. Done when: every dialog control is documented.
- [ ] Capture the dialog to `docs/captures/nodus/duotone/`. Done when: the capture shows a tritone with three curves and the preview.
- [ ] Commit: `"core: bitmap color modes, duotone, and multichannel, with the Nodus Duotone dialog"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~BitmapModes"` exits 0 with `BitmapModeConverterTests`, `DuotoneRendererTests`, `AdoReaderTests`, and the round-trip test reporting; `tests/fixtures/core/duotone/` (the `.ado` file and the Nodus SVG with a duotone image) round-trips exactly, mode conversion goldens from `transicc` hold within Delta E 2000 0.5, and duotone snapshots hold within 2/255 per channel; a driven run converts a placed image to duotone and the log line is quoted. Cheaper substitute that fails: an RGB tint, which the per-ink plate assertion rejects.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Core.Tests.Color"` exits 0 with every test class of §1 to §3 reporting
- [ ] Every `transicc` golden and duotone fixture round trip passes, with the lcms2 and `transicc` versions recorded beside the fixtures
- [ ] `docs/dev/decisions.md` carries the engine row; `src/Photon.Core/THIRD-PARTY-NOTICES.md` carries lcms2's MIT license and the CMYK profile's grant
- [ ] Shared-once check: Nodus (`D02 T09 §1`) consumes this engine today; the pending second consumers are recorded as Imago's ICC work (`D03 T04 §2`) and Lumen's output transform (`D04 T02 §2`), not claimed as shipped
- [ ] `python scripts/todo-claims.py` holds for this file
- [ ] `python scripts/todo-graph.py validate` clean
