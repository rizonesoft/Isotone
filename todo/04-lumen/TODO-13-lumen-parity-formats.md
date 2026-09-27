---
schema_version: 1
id: lumen-parity-formats
domain: 04-lumen
status: draft
title: "TODO-13 -- Lumen Parity: Formats"
depends_on: []
frozen: true
track: L13
---

# TODO-13 -- Lumen Parity: Formats

> **Goal:** Lumen, the Lumen Viewer, and the batch tools read every image format Imago reads and every format IrfanView and ACDSee open that a GPL-3.0-compatible reader exists for, through one codec registry in `src/Photon.Core/Formats/` that Imago's readers and writers move into on this second consumer (never a copy); formats are detected by content, not extension; documents and multi-page files open as pages; RAW coverage is reported per camera with RAW+JPEG pairs handled as the user chooses; every writable format carries its per-format save options; and Lumen owns the suite's one DNG writer. Every reader and writer owes a format fidelity proof against a named reference, opening never changes a file, and writing produces a new file through the atomic writer unless the user opted into an in-place write for that operation (operator decision 2026-09-27, "safe by default, opt-in writes"), which then replaces the file atomically after an optional backup copy.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Lumen has no code and `Photon.Core` does not exist yet. Imago's format project `src/Imago/src/Imago.FileFormats/` holds only the `IImageFormat` interface: no codec and no registry; the `FormatRegistry` is planned by `D03 T17 §1` inside Imago's format project (renamed `src/Imago/Photon.Imago.FileFormats/` by then), with the shared codecs planned under `src/Photon.Core/Formats/`. No archive or compression package is referenced by the solution yet. Lumen is declared in `scripts/apps.psd1` but not shipping, and `installer/Lumen.iss` refuses to compile without `/DLumenShipping`. `standards/lumen.md` states the original-file guard ("Lumen never writes an original image" unless the user opts in, as the operator decided on 2026-09-27), with the opt-in in-place writes that `D04 T11 §1` builds as `OriginalWritePolicy` and `InPlaceWriter`.
<!-- claim: absent src/Lumen -->
<!-- claim: absent src/Photon.Core -->
<!-- claim: exists src/Imago/src/Imago.FileFormats/IImageFormat.cs -->
<!-- claim: count "FormatRegistry" src/Imago/src/**/*.cs = 0 -->
<!-- claim: count "SharpCompress" Directory.Packages.props = 0 -->
<!-- claim: count "Shipping  = \$false" scripts/apps.psd1 = 1 -->
<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->
<!-- claim: count "Lumen never writes an original image" standards/lumen.md = 1 -->

## Inputs

- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard and the decoder rules every reader here obeys
- [`standards/shared.md`](../../standards/shared.md) -- atomic writes, refusals that name the file and the reason, progress and Cancel over one second, one log line per change, a dependency is a decision
- [`standards/testing.md`](../../standards/testing.md) -- fixtures, goldens, and the `Fidelity` trait
- [`docs/parity/lumen-section-design.md`](../../docs/parity/lumen-section-design.md) -- the blueprint and its "Formats and licensing" table; [`docs/parity/lumen-parity.md`](../../docs/parity/lumen-parity.md) -- the catalog rows each section owns
- [`docs/dev/decisions.md`](../../docs/dev/decisions.md) -- every native payload's GPL-3.0 compatibility row
- Specifications each reader cites: TIFF 6.0, JFIF 1.02, PNG Third Edition, GIF89a, Adobe DNG Specification 1.7.1.0, ITU T.81 (process 14 lossless), ISO/IEC 15444-1 (JPEG 2000), ISO/IEC 18181 (JPEG XL), ISO/IEC 14495-1 (JPEG-LS), SMPTE 268M (DPX), DICOM PS3.5, [MS-NRBF] (the Paint.NET layer stream), MNG 1.0, Autodesk FLIC, Apple QuickDraw PICT opcodes
- Reference tools as oracles, versions recorded beside fixtures: libvips 8.16, ImageMagick 7.1, exiftool 13, Adobe `dng_validate` 1.7.1, darktable 5.0, `pdftoppm` 24, Ghostscript 10, `ddjvu` 3.5, CharLS 2.4 `charlstest`, libjpeg-turbo 3.1 `jpegtran`
- -> XREF: D03 T17 §1 -- the `FormatRegistry` §1 moves from Imago's format project to `Photon.Core/Formats/`
- -> XREF: D03 T17 §5 -- the modern web codecs §2 registers after the move and whose writers §6 moves
- -> XREF: D03 T17 §6 -- HDR, scientific, DICOM, and raw-data codecs §2, §3, and §8 consume
- -> XREF: D03 T17 §7 -- PDFium, SVG, metafile, and the Ghostscript runner §4 moves or consumes
- -> XREF: D03 T17 §8 -- legacy raster codecs §3 and §8 register, and whose writers §6 moves
- -> XREF: D03 T17 §9 -- legacy raster codecs II (ILBM, PSP, SFW, PVR) §3 and §8 register
- -> XREF: D03 T17 §11 -- the JPEG, PNG, and TIFF option records §6 moves to `Photon.Core/Formats/Options/`
- -> XREF: D03 T17 §2 -- PSD structure writing §3 uses for flattened PSD write
- -> XREF: D03 T17 §3 -- PSD read fidelity §3 uses for the composite read
- -> XREF: D03 T17 §4 -- the XCF reader §3 uses for the flattened read
- -> XREF: D03 T12 §3 -- the ABR tip reader §3 moves to `Photon.Core/Formats/Abr/`
- -> XREF: D01 T08 §1 -- the shared XPM and GEM IMG codecs §3 and §8 register instead of building their own
- -> XREF: D01 T08 §2 -- the shared Kodak Photo CD codec §8 registers, with its resolution choice, and the FlashPix reader (LP-1051)
- -> XREF: D01 T08 §3 -- the shared ICO and CUR codec and the executable icon extractors §3 registers
- -> XREF: D01 T08 §4 -- the shared PICT reader and rasterizer §8 registers
- -> XREF: D01 T08 §5 -- the shared Corel PHOTO-PAINT CPT reader §8 registers (LP-1045)
- -> XREF: D03 T15 §3 -- the tone-mapping operator §2 moves for HDR display
- -> XREF: D03 T16 §1 -- the shared text engine §8 renders font sample sheets and §4 renders text files through
- -> XREF: D01 T02 §4 -- the suite history the extension fix records its undo step in
- -> XREF: D01 T02 §5 -- the atomic writer every writer here saves through
- -> XREF: D01 T03 §2 -- resampling behind §1's scaled-decode fallback
- -> XREF: D01 T04 §1 -- ICC conversion for CMYK JPEG and profile carry-over
- -> XREF: D01 T07 §6 -- the XMP packet core §7 embeds develop settings with
- -> XREF: D04 T01 §4 -- the RAW decoder §5 extends and §7 writes DNG from
- -> XREF: D04 T01 §6 -- the import dialog that offers §5's RAW+JPEG pair choice
- -> XREF: D04 T02 §7 -- Edit in Imago, named by §3's layered-file notice
- -> XREF: D04 T04 §2 -- the viewer decodes through §1's registry and its scaled-decode capability
- -> XREF: D04 T04 §3 -- default-viewer registration lists every readable extension from §1's matrix
- -> XREF: D04 T04 §10 -- the viewer pages and plays §4's `IPagedImage` and §8's frame sequences
- -> XREF: D04 T05 §6 -- the file-operation journal §1's extension fix and §5's pairs route through once it ships
- -> XREF: D04 T06 §11 -- smart previews written by §7's lossy DNG
- -> XREF: D04 T07 §6 -- Convert to DNG consumes §7
- -> XREF: D04 T07 §7 -- multi-page scans written through §6's TIFF and PDF writers
- -> XREF: D04 T09 §6 -- flat-field corrections written as DNG through §7
- -> XREF: D04 T09 §16 -- photo merges written as DNG through §7
- -> XREF: D04 T11 §1 -- `OriginalGuard` and `OriginalWritePolicy`, which §6's save path consults
- -> XREF: D04 T11 §2 -- the token engine that takes over §4's page-suffix pattern
- -> XREF: D04 T11 §4 -- batch convert writes through §6's writers and option profiles
- -> XREF: D04 T12 §2 -- DNG export consumes §7
- -> XREF: D04 T12 §5 -- document printing reads PDF pages through §4
- -> XREF: D04 T14 §4 -- the file-handling preferences page that renders the `Lumen.Formats.*` keys §1, §4, §5, and §6 define
- -> XREF: D04 T14 §7 -- the installed codecs list that reads §1's `FormatMatrix`
- -> XREF: D04 T10 §8 -- Lumen AI cites §7: the DNG writer D04 T10 §8's outputs write through
- -> XREF: D02 T14 §10 -- Nodus's DXF and DWG reader on ACadSharp, whose reading §9 moves into `src/Photon.Core/Formats/Cad/` on its second consumer, Nodus repointing
- -> XREF: D02 T14 §11 -- Nodus's own `CgmReader` and `HpglReader`, which §9 moves into `src/Photon.Core/Formats/Vector/`, Nodus repointing
- -> XREF: D01 T08 §4 -- the `PictDrawing` drawing-operation model and rasterizer pattern §9's `CadDrawing` and `DrawingRasterizer` follow
- -> XREF: D01 T11 §1 -- the media stack and the optional FFmpeg runner that play FLV, the other half of LP-1050 whose SWF half §10 reads
- -> XREF: D04 T14 §4 -- the file-handling preferences page that renders §11's `Lumen.Formats.Gdal.*` keys and §9's `Lumen.Formats.Cad.*` keys
- -> XREF: D04 T15 §14 -- Lumen 1.4.0 releases §10 to §12; Lumen 0.2.0 (D04 T15 §1) releases §9
- Specifications for §9 to §12: ACadSharp's DXF and DWG object model (MIT), ISO 8632 CGM, the HP-GL/2 reference, the SWF File Format Specification version 19, the GDAL utility documentation (`gdalinfo`, `gdal_translate`, `--formats -json`) at https://gdal.org/programs/, and the clean-room structure notes §12 writes under `docs/dev/formats/`

## Outcome

- One `FormatRegistry` in `src/Photon.Core/Formats/` is the only registry under `src/`; Lumen, the Lumen Viewer, the batch tools, and Imago read through it, and a PNG named `.jpg` opens as PNG.
- Every modern, HDR, legacy, rare, document, and multi-page format in the catalog opens in Lumen within a stated tolerance of a named reference, and every writable one saves with its full option set, shared by export, convert, and Save As.
- Documents and multi-page files open as pages; multi-page TIFF and PDF files are built and pages extracted as new files.
- The RAW coverage table lists every supported camera with its decoder version, and RAW+JPEG pairs are one photo or two as the user chose.
- DNG files written by Lumen pass Adobe `dng_validate` with zero errors and reread bit-exact.
- Opening never changes a file; a write over an original happens only when the user opted into it for that operation, through an atomic replace after the optional backup.
- DXF, DWG, HPGL, and CGM drawings open in Lumen through the readers Nodus built, moved once into `Photon.Core` and rasterized within tolerance of LibreCAD, LibreOffice, and Inkscape goldens, with one reader of each format under `src/`.
- The first frame of a Flash SWF file renders through an own parser that never executes ActionScript, within tolerance of Ruffle's output.
- With a user-installed GDAL and its driver plug-ins, ECW, MrSID, JPM, and MRC open (and write where the driver writes); without them the formats are listed as unavailable with the reason, and no GDAL file ships in any package.
- Artweaver, BodyPaint 3D, Gemstone GSD, and ACDSee ACDC documents open as flattened composites from clean-room structure notes, or are rerouted to the backlog with the analysis evidence.

**Adjacency:** list=applicable @ D04 T13 §1; document=applicable @ D04 T13 §6; settings=applicable @ D04 T13 §1; reporting=applicable @ D04 T13 §5; notifications=applicable @ D04 T13 §1; permissions=applicable @ D04 T13 §6; audit=applicable @ D04 T13 §1; exchange=applicable @ D04 T13 §6; reverse=applicable @ D04 T13 §1

**Adjacency rationale:** The lists are the format matrix (§1) and the RAW coverage table (§5). Every writer in §6 and §7 produces a user file, and the multi-page editor (§4) builds one. Settings are `Lumen.Formats.*` keys (enabled handlers, save option profiles, Ghostscript location, render sizes, raw-open presets) and `Lumen.Import.RawJpegPairs`, each with a default and a named consumer, rendered by the preferences page of `D04 T14 §4`. The format matrix and the coverage report are the reporting. A wrong extension found on load and an unsupported camera are reported by name (§1, §5). Unreadable, locked, truncated, or encrypted files and an absent Ghostscript are refused by name (§1, §4). One Serilog Information line per write and per extension fix is the audit trail (§1, §6). Every format here is exchange. Writes are new files unless the user opted into an in-place write with a backup, and the extension fix is a rename with one undo step (§1).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The shared codec registry in Photon.Core | D04 T02 §8, D03 T17 §1, D03 T17 §5, D03 T17 §6, D03 T17 §8, D03 T17 §9 |  [ ]   |
|   2   |   §2    | Modern and HDR formats in Lumen | §1, D03 T15 §3 |  [ ]   |
|   3   |   §3    | Common legacy and special raster formats | §1, D03 T17 §2, D03 T17 §3, D03 T17 §4, D03 T12 §3, D01 T08 §1, D01 T08 §3 |  [ ]   |
|   4   |   §8    | Rare and historical raster formats | §3, D01 T08 §2, D01 T08 §4, D01 T08 §5 |  [ ]   |
|   5   |   §4    | Documents and multi-page formats | §1, D03 T17 §7 |  [ ]   |
|   6   |   §5    | RAW coverage and RAW+JPEG pairs | §1, D04 T01 §4 |  [ ]   |
|   7   |   §6    | Write formats and per-format save options | §1, D03 T17 §11, D04 T11 §1 |  [ ]   |
|   8   |   §7    | The DNG writer | §5 |  [ ]   |
|   9   |   §9    | CAD and plotter drawings: DXF, DWG, HPGL, and CGM | §1, D02 T14 §10, D02 T14 §11, D01 T08 §4 |  [ ]   |
|  10   |   §10   | Flash SWF: the first frame through an own parser | §1, D01 T11 §1 |  [ ]   |
|  11   |   §11   | ECW, MrSID, JPM, and MRC through an optional GDAL | §1, §4, D04 T14 §4 |  [ ]   |
|  12   |   §12   | Artweaver, BodyPaint 3D, Gemstone GSD, and ACDSee ACDC through clean-room analysis | §1, §3, §4 |  [ ]   |

---

## 1. The Shared Codec Registry in Photon.Core

Imago builds the suite's `FormatRegistry` and its codecs (`D03 T17 §1`, `§5`, `§6`, `§8`, `§9`) inside its own format project; Lumen is their second consumer, so they move to `src/Photon.Core/Formats/` in one move (never a copy) and gain what a viewer and a library need: content sniffing, a screen-size decode capability, and a per-handler enable switch. After this section Lumen, the Lumen Viewer, the batch tools, and Imago all read through one registry, and JPEG, PNG, TIFF, GIF, and BMP read and write with CMYK JPEG, high-bit and float TIFF, and alpha. The registry never opens a file for writing; the "Fix extension" command is a rename, recorded as one undo step. Catalog: LP-0981 to LP-0984 (4 features: the common formats, a wrong extension fixed on load, formats shipped in the app with handler toggles, and detection by content with extension rules for header-less formats). -> SOURCE: parity-lumen-codec-registry

**Fidelity:** no surface of its own; the format matrix and handler toggles are data this section generates, rendered by the file-handling preferences page of `D04 T14 §4` and the installed codecs list of `D04 T14 §7`, and the extension-fix offer rides the existing status strip of `D04 T01 §2`.

**Freeze check:** Every reader opens its file with `FileAccess.Read` and `FileShare.ReadWrite`; decoding the whole fixture set leaves every file's SHA-256 and last-write time unchanged; "Fix extension" renames the file and its sidecar through one undoable step and never writes a byte of either. Fixture source: `tests/fixtures/formats/common/` (created by this section).

- [ ] Move `FormatRegistry`, `IImageReader`, `IImageWriter`, and every reader registered by `D03 T17 §5`, `§6`, `§8`, and `§9` from Imago's format project (`src/Imago/Photon.Imago.FileFormats/`) to `src/Photon.Core/Formats/` with `git mv` in one commit, repointing Imago's composition root. Done when: `grep -rn "class FormatRegistry" src` prints one path, under `src/Photon.Core/Formats/`, and Imago's existing `FormatRegistryTests` pass unchanged. Cheaper substitute: a copy of the registry inside Lumen, which the one-path grep refuses.
- [ ] Reference `Photon.Core` from `src/Lumen/Photon.Lumen.Core/Photon.Lumen.Core.csproj` and register the one `FormatRegistry` instance in Lumen's composition root. Done when: `LumenProjectReferenceTests` assert no `Photon.Lumen.*.csproj` references an `Imago` project and Lumen resolves `FormatRegistry` from its container.
- [ ] Add `FormatSniffer.Detect(Stream)` in `src/Photon.Core/Formats/FormatSniffer.cs`, reading at most 64 KB of magic bytes per handler, ordered by signature specificity (LP-0984). Done when: `FormatSnifferTests` identify every fixture under `tests/fixtures/formats/common/` by content with its extension removed.
- [ ] Declare extension rules in the registry for header-less formats (raw pixel dumps, some legacy formats) as the fallback after sniffing fails (LP-0984). Done when: a test opens a header-less fixture by its extension and a `.dat` copy of it is refused naming "no signature and no extension rule".
- [ ] Return `SniffResult.ExtensionMismatch` when the content disagrees with the extension, and decode by content (LP-0982). Done when: a PNG fixture renamed `.jpg` decodes as PNG and the result names both formats.
- [ ] Add `ExtensionFixService` in `src/Lumen/Photon.Lumen.Core/Formats/ExtensionFixService.cs`: offer "Fix extension" on the status strip when `Lumen.Formats.OfferExtensionFix` (default true) is on, rename the file and its `.xmp` sidecar to the detected extension, update the catalog path, and record one "Fix Extension" step in the suite history (`D01 T02 §4`) so undo reverses the rename (LP-0982). Done when: `ExtensionFixTests` rename a mislabeled fixture with its sidecar, undo restores both names, and the file's SHA-256 is unchanged. Cheaper substitute: rewriting the file under the new name, which the hash assertion catches.
- [ ] Add `IImageReader.DecodeScaled(Stream, SizeInt target)` and a `ReaderCapabilities.ScaledDecode` flag, with a default that decodes in full and resamples through `D01 T03 §2`. Done when: `ScaledDecodeTests` assert every reader returns an image no smaller than the target on its long edge.
- [ ] Implement scaled JPEG decode through WIC's DCT scaling (1/2, 1/4, 1/8) (https://learn.microsoft.com/windows/win32/wic/-wic-codec-jpeg). Done when: a 24-megapixel fixture decodes to screen size at least three times faster than full decode (timings quoted) and within 2/255 mean of full decode plus resampling.
- [ ] Verify the common formats in Lumen (LP-0981): JPEG, PNG, TIFF at 8 and 16 bits and 32-bit float with alpha, GIF first frame and frame list, and BMP, all through the moved codecs. Done when: `FormatRegistryFidelityTests` decode each fixture of the set.
- [ ] Convert CMYK and YCCK JPEGs to the working space through `D01 T04 §1` with the embedded profile, or the default CMYK profile when none is embedded (LP-0981). Done when: a CMYK fixture matches libvips 8.16's `icc_import` output within 1/255.
- [ ] Add the `Lumen.Formats.Disabled` setting (default empty): the handlers the user switched off, read by the open filters, the viewer's association list (`D04 T04 §3`), and the batch file list (LP-0983). Done when: disabling WebP removes it from the open filter without a restart and a WebP file is refused naming the setting.
- [ ] Add `FormatMatrix.Generate()` in `src/Photon.Core/Formats/FormatMatrix.cs`, listing name, extensions, read, write, bit depths, alpha, layers as composite, multi-page, and metadata carried per handler. Done when: `FormatMatrixTests` assert one row per registered handler and no row without a handler.
- [ ] Generate `docs/user/lumen/formats.md` from `FormatMatrix` with a committed generator test. Done when: `FormatMatrixDocTests` fail when the committed page differs from the generated one.
- [ ] Return a typed `FormatReadException` naming the file and the reason for a truncated, unreadable, or locked file, never a partial image shown as whole. Done when: tests over a truncated JPEG, a zero-byte file, and a file locked with `FileShare.None` each assert the message names the file.
- [ ] Log one Serilog Information line per extension fix and one Warning line per refused read (`{Action} {Path} {Format} {Reason}`) as the audit trail, and alert the user on the status strip when a read is refused. Done when: a Serilog test sink asserts both lines.
- [ ] Commit fixtures under `tests/fixtures/formats/common/` (JPEG baseline, progressive, CMYK, and 24 megapixels; PNG 8 and 16 bits with alpha; TIFF 8, 16, and 32-bit float with alpha; GIF; BMP; a mislabeled PNG; a truncated JPEG) with `reference.txt` naming libvips 8.16 and its commands. Done when: every fixture carries its note.
- [ ] Add `FormatRegistryFidelityTests` (`[Trait("Category", "Fidelity")]`) comparing each decode with libvips 8.16 output: exact for 8-bit lossless formats, within 1/255 for JPEG. Done when: the test prints a tolerance per fixture.
- [ ] Add the unchanged-originals assertion over the whole fixture set: every read leaves SHA-256 and last-write time unchanged. Done when: `UnchangedOriginalsTests.FormatReads` passes.
- [ ] Commit: `"core: one codec registry in Photon.Core, read by Lumen and Imago"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~FormatSniffer|FullyQualifiedName~FormatRegistry|FullyQualifiedName~ExtensionFix|FullyQualifiedName~UnchangedOriginalsTests"` exits 0 with the per-fixture tolerances printed; `grep -rn "class FormatRegistry" src` prints one path under `src/Photon.Core/Formats/`. Cheaper substitute that fails: Lumen referencing Imago's format project, which `LumenProjectReferenceTests` refuse.

## 2. Modern and HDR Formats in Lumen

The modern web and camera formats and the HDR and scientific formats are already Imago's codecs (`D03 T17 §5`, `§6`); after §1's move Lumen registers them, adds DPX and Cineon, which Imago never needed, and gives HDR images a tone-mapped display for thumbnails and the viewer while exports keep their float data. Native payloads ship per runtime identifier inside the Lumen installer, each with its license row. Catalog: LP-0985 to LP-0991 (7 features: AVIF and HEIF, the HDR and scientific formats, JPEG 2000, JPEG XL, WebP, QOI, and JPEG XR). -> SOURCE: parity-lumen-modern-formats

**Fidelity:** no surface of its own (the formats appear in the viewer, browse, and batch through the registry; option pages are §6's).

- [ ] Register the moved WebP codec (libwebp, BSD-3-Clause) for Lumen, with transparency (LP-0989). Done when: a lossless WebP fixture with alpha decodes bit-exact against `dwebp`.
- [ ] Register AVIF (libavif, BSD-2-Clause) and HEIF, HEIC, and HIF (libheif, LGPL-3.0, dynamically linked) read and write, showing animated AVIF as its first frame and reading an AVIF's XMP sidecar (LP-0985). Done when: `ModernFormatFidelityTests` decode the AVIF, animated AVIF, HEIC, and HIF fixtures within the PSNR floor of `avifdec` and `heif-dec`.
- [ ] Register JPEG XL read and write (libjxl, BSD-3-Clause) (LP-0988). Done when: a lossless JPEG XL fixture decodes bit-exact against `djxl`.
- [ ] Register JPEG 2000 JP2, JPC, and J2K read and write with 48-bit color (OpenJPEG, BSD-2-Clause) (LP-0987). Done when: a 16-bit-per-channel JP2 fixture decodes exactly against `opj_decompress`.
- [ ] Register QOI read and write (own code from `D03 T17 §5`) (LP-0990). Done when: a QOI round trip is exact.
- [ ] Register JPEG XR, HD Photo HDP, JXR, and WDP read (jxrlib, BSD-2-Clause, moved by `D03 T17 §5`) (LP-0991). Done when: a JXR fixture decodes within 1/255 of `JxrDecApp`.
- [ ] Register OpenEXR, Radiance HDR, and FITS from `D03 T17 §6` (LP-0986). Done when: the EXR, HDR, and FITS fixtures decode within 1e-4 of OpenImageIO 3.0 `oiiotool`.
- [ ] Add DPX and Cineon read in `src/Photon.Core/Formats/Dpx/DpxReader.cs` from SMPTE 268M, decoding 10-bit log to linear with the header's reference white and black (LP-0986). Done when: DPX and Cineon fixtures match ImageMagick 7.1 decodes within 1/1023.
- [ ] Move the tone-mapping operator of `D03 T15 §3` to `src/Photon.Core/Imaging/ToneMap/` (second consumer) and apply it to HDR sources for thumbnails and the viewer, never to exported data. Done when: `grep -rn "class .*ToneMapOperator" src` prints paths only under `src/Photon.Core/` and an EXR thumbnail matches the operator's golden within 1/255.
- [ ] Register scaled decode (§1's capability) for AVIF and JPEG XL through the codecs' downsampled and progressive decode where they offer it. Done when: `ScaledDecodeTests` report the AVIF and JXL fixtures decoding to screen size faster than full decode, timings quoted.
- [ ] Refuse a missing native library by name ("libheif is not installed with this copy of Lumen") instead of falling back to WIC Store extensions. Done when: `NativeCodecLoaderTests` delete the payload in a temp copy and assert the message.
- [ ] Record each native payload per runtime identifier in `docs/dev/decisions.md` with its license and linking mode, and add the payloads to Lumen's package file list checked by `scripts/package.ps1`. Done when: the package script fails on a missing payload in a dry run.
- [ ] Commit fixtures under `tests/fixtures/formats/modern/` with `reference.txt` naming libvips 8.16, `dwebp`, `avifdec`, `heif-dec`, `djxl`, `opj_decompress`, `JxrDecApp`, `oiiotool`, and ImageMagick 7.1 with versions and commands. Done when: every fixture carries its note.
- [ ] Add `ModernFormatFidelityTests` (`[Trait("Category", "Fidelity")]`) reading and writing each fixture: lossless within 0, lossy within the stated PSNR floor per format. Done when: the test prints one result per format and direction.
- [ ] Commit: `"lumen: modern and HDR formats through the shared registry"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~ModernFormat"` exits 0 printing a result per format and direction with its tolerance, and `NativeCodecLoaderTests` pass. Cheaper substitute that fails: WIC codecs from the Store, which the missing-payload refusal test and the clean-machine run of the release expose.

## 3. Common Legacy and Special Raster Formats

Icons, textures, and the older paint programs' files are what a photo manager meets in a user's folders, so Lumen reads the common legacy and special formats (ICO, CUR, ANI, PCX and DCX, TGA, WBMP, PSD and PSB composites, XCF flattened, DICOM, PSP, SFW, PDN, DDS and game textures, EXE and DLL icons, XBM, XPM, PNM) and writes those with writers, mostly by registering Imago's moved codecs and the shared legacy codecs of `D01 T08` (ICO, CUR, XPM, and executable icons) and adding a few small own readers. Layered files show their composite; layered editing is Imago's, and the notice says so. Catalog: LP-0992 to LP-1003 (12 features: ABR brushes browsed as images, icons and cursors, PCX and DCX, PSD and PSB, TGA, WBMP, DICOM, PSP, SFW, and PDN, XCF, game and texture formats, icons from executables, and the X11 and PNM bitmaps). -> SOURCE: parity-lumen-legacy-formats

**Fidelity:** no surface of its own (formats appear through the registry; the layered-file notice reuses the viewer's information bar).

**Freeze check:** Every writer registered here (PCX, DCX, TGA, WBMP, flattened PSD) saves through `AtomicFileWriter` to a new path; a failed or interrupted write leaves any existing target byte-identical; reading an executable for its icons parses its resource tables through `D01 T08 §3`'s extractors and never loads or executes it. Fixture source: `tests/fixtures/formats/legacy/` (created by this section).

- [ ] Register the shared `IcoCodec` of `D01 T08 §3` for ICO (every resolution as a page) and CUR, and the ANI codec of `D03 T17 §8` (frames as pages) (LP-0993). Done when: a five-size ICO fixture opens as five pages matching ImageMagick 7.1 exactly and `grep -rn "class IcoCodec" src` prints one path.
- [ ] Register PCX and multi-page DCX read and write (LP-0994). Done when: a three-page DCX fixture round-trips every page exactly.
- [ ] Register TGA read and write (LP-0996). Done when: RLE and uncompressed TGA fixtures round-trip exactly.
- [ ] Register WBMP read from `D03 T17 §8` and add a WBMP writer in `src/Photon.Core/Formats/Raster/WbmpWriter.cs` (type 0, 1-bit with a threshold) (LP-0997). Done when: a written WBMP decodes in ImageMagick 7.1 exactly.
- [ ] Register XBM read from `D03 T17 §8`, the shared XPM codec of `D01 T08 §1`, and PBM, PGM, and PPM read from `D03 T17 §6` (LP-1003). Done when: each fixture matches GIMP 3.2's decode exactly.
- [ ] Register PSD and PSB composite read and flattened PSD write from `src/Photon.Core/Formats/Psd/`, moving any part of `D03 T17 §2` and `§3` still in Imago's project there with `git mv` (LP-0995). Done when: a layered PSD composite matches psd-tools 1.10's composite within 1/255 and `grep -rn "class PsdReader" src` prints one path.
- [ ] Register the GIMP XCF flattened read from `D03 T17 §4`, moved to `src/Photon.Core/Formats/Xcf/` (LP-1000). Done when: an XCF fixture's composite matches GIMP 3.2's PNG export within 1/255.
- [ ] Show a notice on layered files (PSD, PSB, XCF, PSP, PDN): "Layers are shown flattened. Open in Imago to edit layers.", with the Edit in Imago command of `D04 T02 §7`. Done when: a test asserts the notice appears for the layered fixtures and not for flat ones.
- [ ] Register the DICOM DCM, ACR, and IMA reader of `D03 T17 §6` (own code; fo-dicom is MS-PL and stays out) (LP-0998). Done when: a DICOM fixture matches dcmtk 3.6 `dcm2pnm` within 1/255 at the same window.
- [ ] Register Paint Shop Pro PSP and Seattle FilmWorks SFW read from `D03 T17 §9` (LP-0999). Done when: the PSP composite matches GIMP 3.2 within 1/255 and SFW matches ImageMagick 7.1 exactly.
- [ ] Add a Paint.NET PDN reader in `src/Photon.Core/Formats/Pdn/PdnReader.cs`: the `PDN3` header and XML header, then the layer stream parsed by an own [MS-NRBF] record reader (never `BinaryFormatter`), compositing visible layers by blend mode and opacity (LP-0999). Done when: a PDN fixture matches Paint.NET 5's own PNG export within 1/255 and a test asserts no `BinaryFormatter` reference in the assembly.
- [ ] Register DDS through BCnEncoder.Net (MIT) and Dreamcast PVR from `D03 T17 §8` and `§9` (LP-1001). Done when: DDS fixtures match DirectXTex `texconv` within the stated BCn tolerance.
- [ ] Add WAD3, Quake WAL, and Blizzard BLP readers in `src/Photon.Core/Formats/Games/` from their published descriptions, each texture or mip level a page (LP-1001). Done when: fixtures match their committed ImageMagick or reference-viewer goldens exactly.
- [ ] Register icons from EXE, DLL, and ICL files (LP-1002) through `D01 T08 §3`'s `ExecutableIconSource` (its PE and NE resource parsers, which never load the file), each icon group a page named by its resource name or ordinal. Done when: an ICL fixture and a copy of `shell32.dll` both list their icon groups as pages and `IconExtractorSafetyTests` still pass.
- [ ] Move the ABR tip reader of `D03 T12 §3` to `src/Photon.Core/Formats/Abr/` with `git mv` and register ABR files as browsable images, each tip a page (LP-0992). Done when: an ABR fixture opens one page per tip and Imago's brush import still passes its tests.
- [ ] Commit fixtures under `tests/fixtures/formats/legacy/` with `reference.txt` naming ImageMagick 7.1, GIMP 3.2, psd-tools 1.10, dcmtk 3.6, DirectXTex `texconv`, and Paint.NET 5 per fixture. Done when: every fixture carries its note.
- [ ] Add `LegacyFormatFidelityTests` (`[Trait("Category", "Fidelity")]`) comparing every read with its oracle and round-tripping every writer (read, write, reread). Done when: the test lists every format with read and write results.
- [ ] Commit: `"lumen: common legacy and special raster formats"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~LegacyFormat"` exits 0 listing every format with its read and write result and tolerance. Cheaper substitute that fails: a thumbnail-only reader for PSD or PDN, which the full-resolution pixel comparison catches.

## 4. Documents and Multi-Page Formats

ACDSee and IrfanView users browse and rate PDFs and scans beside their photos, so Lumen opens PDF, XPS, SVG, EMF, WMF, WPG, DjVu, PostScript, EPS, and text files as page images, gives every multi-page container one page model the viewer pages through, and builds and splits multi-page TIFF and PDF files, always as new files. Ghostscript (AGPL-3.0) is never bundled; DjVuLibre is GPL-2.0-or-later and so compatible with GPL-3.0. Catalog: LP-1004 to LP-1014 (11 features: documents in the viewer with a per-type open choice, PDF viewing, vector and metafile images, text files as images, the multipage editor, extract pages, render settings, DjVu, PostScript and EPS, text files shown as images, and multi-page containers). -> SOURCE: parity-lumen-documents

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/documents/` and `docs/captures/lumen/multipage-editor/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md, docs/design/components/Menu/README.md, docs/design/components/Toast/README.md, docs/design/components/NumberBox/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user browses and rates PDFs and scans beside photos and assembles a multi-page file without another tool. Consumer: the viewer's page navigation (`D04 T04 §10`), the catalog, and the written TIFF or PDF.
**Treatment:** a per-type choice to open documents in the viewer or their own application; the viewer's page bar with page and magnification readouts; IrfanView's multipage editor (add files or a list, arrange, delete, append the current image, save as TIFF or PDF) and Extract Pages dialog (range, format, name suffix). Cheaper substitute that fails the checkpoint: opening PDFs in the default reader only.
**Chrome:** consume the registry, the viewer's page navigation (`D04 T04 §10`), the suite PDF writer in `Photon.Core/Pdf/`, `AtomicFileWriter`, and `Photon.UI` dialog styles. Do not add a second PDF renderer.

**Requires:** display-session -- the multipage editor and document viewing need an interactive desktop

**Freeze check:** The multipage editor and Extract Pages write through `AtomicFileWriter` to paths that are never a source file of the operation (a test asserts the refusal); a failed or cancelled save leaves no partial file and any existing target byte-identical; opening a document never opens it for writing. Fixture source: `tests/fixtures/formats/documents/` (created by this section).

- [ ] Move whatever of `D03 T17 §7`'s PDFium reader (BSD-3-Clause and Apache-2.0), SVG reader, and EMF and WMF readers still lives in Imago's project to `src/Photon.Core/Formats/Pdf/` and `src/Photon.Core/Formats/Vector/` with `git mv`, repointing Imago. Done when: `grep -rn "class PdfiumDocument" src` prints one path under `src/Photon.Core/`.
- [ ] Rasterize PDF pages at `Lumen.Formats.Pdf.RenderDpi` (default 150) and SVG at `Lumen.Formats.Svg.RenderSize` (default 2,048 px long edge) (LP-1010). Done when: changing the setting changes the decoded size without a restart.
- [ ] Add `IPagedImage` in `src/Photon.Core/Formats/Paging/IPagedImage.cs` (page count, page size, decode page, scaled decode page) for TIFF, DCX, ICO, PDF, DjVu, and MPO, with an MPO's second images as pages (LP-1014). Done when: `PagedImageTests` report the page count of each multi-page fixture equal to its oracle's.
- [ ] Add the document commands to the viewer's page bar of `D04 T04 §10` (LP-1005): page back and forward, zoom, fit page, fit width, page number and magnification readouts, Page Up and Page Down, next file, open in the default app, and print through the viewer's print command. Done when: a driven run pages a 20-page PDF fixture and the readouts are captured.
- [ ] Render XPS pages through WPF's `XpsDocument` and `DocumentPaginator` into pixels (https://learn.microsoft.com/dotnet/api/system.windows.xps.packaging.xpsdocument) (LP-1004). Done when: an XPS fixture's first page matches a committed golden within 2/255 mean.
- [ ] Let rating, label, and keywords apply to documents like photos, and add `Lumen.Formats.Documents.OpenIn` (Viewer or DefaultApp, per type) (LP-1004); Office documents stay unsupported with a message. Done when: a driven run rates a PDF, and with DefaultApp set for PDF, Enter opens the default reader.
- [ ] Register SVG, EMF, and WMF from `D03 T17 §7` and add a WordPerfect WPG reader in `src/Photon.Core/Formats/Vector/WpgReader.cs` for its bitmap and vector records (LP-1006). Done when: a WPG fixture matches the committed LibreOffice-rendered golden within 2/255 mean.
- [ ] Route PostScript, EPS, PS, and AI through the Ghostscript runner in `src/Photon.Core/Formats/PostScript/` (LP-1012): user-installed, matching bitness, located by `Lumen.Formats.Ghostscript.Path` or the registry, with text and graphics antialiasing settings (LP-1010). Done when: an EPS fixture renders within 2/255 mean of Ghostscript 10's own PNG output.
- [ ] Refuse PostScript files by name when Ghostscript is absent ("Ghostscript is not installed; install it or set its location in Preferences, File Handling") and never bundle it. Done when: a test with the path unset asserts the message and `scripts/package.ps1`'s file list has no `gs*.dll`.
- [ ] Add DjVu read with pages through DjVuLibre `libdjvulibre` over P/Invoke in `src/Photon.Core/Formats/DjVu/`, native per runtime identifier, with a `docs/dev/decisions.md` row quoting its "version 2 of the license, or (at your option) any later version" grant (LP-1011). Done when: a DjVu fixture's pages match `ddjvu` 3.5 within 2/255 mean.
- [ ] Render text files as images with `Lumen.Formats.Text.Font`, `.Size`, `.Foreground`, and `.Background` through the shared text engine (`D03 T16 §1`), one feature built once for LP-1007 and LP-1013. Done when: a UTF-8 text fixture renders to the committed golden exactly.
- [ ] Refuse encrypted PDFs with a password prompt and a corrupt document with a typed failure naming the file. Done when: tests over an encrypted and a truncated PDF assert the prompt and the message.
- [ ] Add the multipage editor in `src/Lumen/Photon.Lumen.Desktop/Views/Formats/MultipageEditor.xaml` (LP-1008): add files or a text list, arrange by drag, delete, append the current image, and save as TIFF or PDF (the suite PDF writer in `Photon.Core/Pdf/`) to a new path. Done when: a driven build of a five-page TIFF from fixtures rereads five pages equal to the sources. Cheaper substitute: appending pages into an existing file, which the new-path assertion catches.
- [ ] Add the Extract Pages dialog (LP-1009): page range, target format from the registry's writers, and a `{name}_p{page}` suffix, each page a new file. Done when: extracting pages 2 to 4 of the DjVu fixture writes three files whose pixels match the source pages.
- [ ] Commit fixtures under `tests/fixtures/formats/documents/` (PDF, encrypted PDF, XPS, SVG, EMF, WMF, WPG, EPS, DjVu, MPO, text) with `reference.txt` naming `pdftoppm` 24, Ghostscript 10, and `ddjvu` 3.5. Done when: every fixture carries its note.
- [ ] Add `DocumentFormatFidelityTests` (`[Trait("Category", "Fidelity")]`) rendering fixture pages and comparing with the oracles within 2/255 mean, and a multipage round trip that rereads page count and pixels. Done when: the test prints one result per format.
- [ ] Commit captures under `docs/captures/lumen/documents/` and `docs/captures/lumen/multipage-editor/` and write `docs/user/lumen/documents.md`. Done when: every command in the Treatment appears in a capture and the page documents it.
- [ ] Commit: `"lumen: documents and multi-page formats"`

**Test checkpoint:** Format fidelity proof and driven run: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~DocumentFormat|FullyQualifiedName~PagedImage"` exits 0 per format; a driven multipage build is reread with its page count quoted and captured under `docs/captures/lumen/multipage-editor/`. Cheaper substitute that fails: first page only, which the page-count assertion catches.

## 5. RAW Coverage and RAW+JPEG Pairs

Photographers who shoot RAW+JPEG see doubled thumbnails in a naive browser, and photographers buying a new body need to know before import whether Lumen reads it. This section treats a RAW+JPEG pair as one photo with the JPEG as a sidecar or as two photos, as the user chooses, and publishes a coverage table generated from the decoder that `D04 T01 §3` chose, with the decoder's version and a path to request a camera. Catalog: LP-1015 to LP-1017 (3 features: RAW+JPEG pairs, JPEG XL compressed DNG, and the camera coverage table). -> SOURCE: parity-lumen-raw-coverage

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/raw-coverage/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/Menu/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer knows before buying or importing whether Lumen reads their camera, and shoots RAW+JPEG without doubled thumbnails. Consumer: the catalog, the grid, and the import dialog.
**Treatment:** Help, Supported Cameras (a searchable maker and model table with the decoder version, a tested column, a JPEG XL DNG column, and a "Request a camera" link to the decoder's upstream tracker) and a choice "Treat a JPEG next to a RAW file as: part of the RAW photo, a separate photo". Cheaper substitute that fails the checkpoint: a static camera list copied into the docs.
**Chrome:** consume `D04 T01 §4`'s decoder adapter, the catalog migrations of `D04 T01 §5`, and `Photon.UI` list styles. Do not add a second camera list.

**Requires:** display-session -- the coverage dialog capture needs an interactive desktop

- [ ] Add `RawPairPolicy` in `src/Lumen/Photon.Lumen.Core/Raw/RawPairPolicy.cs` with `Lumen.Import.RawJpegPairs` = `Sidecar` (default) or `Separate` (LP-1015). Done when: `RawPairPolicyTests` import a mixed folder under each policy and count the expected records.
- [ ] Detect pairs by base name (case-insensitive) and capture time within two seconds, so a renamed JPEG from another shot is not paired. Done when: a test over a mixed folder with one false pair (same name, 30 seconds apart) pairs only the true ones.
- [ ] Add a forward-only catalog migration for a `paired_file` column with a pair badge in the grid, tested on the previous version's catalog per `D04 T01 §5`. Done when: `CatalogMigrationTests` open the old catalog and the grid shows the badge on a pair.
- [ ] Switch the policy on an existing catalog without losing metadata: splitting a pair copies the RAW record's rating, label, and keywords to the JPEG record, and merging keeps the RAW's, as one undo step. Done when: a test switches both ways and undo restores the record count and fields.
- [ ] Move or remove both members of a pair when the photo is removed from the catalog, and hand pair travel on disk to `D04 T05 §6`'s file operations. Done when: removing a paired photo removes one record and names both files in the log line.
- [ ] Offer the policy choice in the import dialog of `D04 T01 §6` and in Lumen's Preferences window (rehomed by `D04 T14 §4`). Done when: a driven import with the choice set to Separate shows two thumbnails for a pair.
- [ ] Generate the coverage table at build time from the decoder's camera list (LibRaw's `libraw_cameraList` when `D04 T01 §3` chose LibRaw) into `src/Lumen/Photon.Lumen.Core/Raw/cameras.json` with the decoder version (LP-1017). Done when: `CameraCoverageTests` assert the JSON's count equals the decoder's list length.
- [ ] Mark the models of `D04 T01 §4`'s pinned corpus as tested, with the decode result. Done when: every corpus camera appears as tested in the JSON.
- [ ] Add Help, Supported Cameras in `src/Lumen/Photon.Lumen.Desktop/Views/Help/SupportedCamerasDialog.xaml`: search, maker and model columns, decoder version, tested and JPEG XL DNG columns, and a "Request a camera" link to the decoder's upstream tracker. Done when: a driven search for "Z 8" shows the row and the capture is committed.
- [ ] Generate `docs/user/lumen/cameras.md` from the JSON with a generator test. Done when: the test fails when the committed page differs.
- [ ] Report an unsupported model by name with the decoder version and the request link ("Lumen's RAW decoder 0.21 does not read the Example X1 yet"), stating that decoder updates arrive with Lumen releases. Done when: a test with a stubbed unknown model asserts the message.
- [ ] Decode JPEG XL compressed DNG (DNG 1.7) when the decoder release reports support, otherwise refuse with a typed failure naming the missing support, and show the capability as a column (LP-1016). Done when: a JXL DNG fixture decodes or is refused by name according to the decoder's reported capability.
- [ ] Commit fixtures under `tests/fixtures/lumen/raw-pairs/` (the committed DNG, a RAW+JPEG pair, a false pair, a JXL DNG) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Add a fidelity test decoding the pair fixtures through the pair policy and comparing with `D04 T01 §4`'s golden. Done when: the RAW decode matches the golden within its stated tolerance.
- [ ] Commit the capture under `docs/captures/lumen/raw-coverage/` and extend `docs/user/lumen/formats.md` with RAW+JPEG pairs. Done when: the dialog and the choice appear in captures and the page documents them.
- [ ] Commit: `"lumen: RAW coverage table and RAW+JPEG pairs"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~RawPairPolicy|FullyQualifiedName~CameraCoverage|FullyQualifiedName~CatalogMigration"` exits 0 covering both policies, the false pair, and a policy switch with undo; the coverage dialog capture shows the decoder version. Cheaper substitute that fails: treating pairs as duplicates, which the pair-count test catches.

## 6. Write Formats and Per-Format Save Options

Every writable format carries options, and IrfanView users expect them the moment they pick a format in Save As; Lumen shares one option set per format across export, batch convert, the viewer's Save As, and the batch tools, stores named profiles, and restricts which formats the save dialogs offer. Imago's writers and option records move to `Photon.Core` on this second consumer, and Imago's option-page renderer moves to `Photon.UI`. A save whose target is an original goes through `D04 T11 §1`'s `OriginalWritePolicy`: refused by name unless the user opted into in-place writes for that operation, and then an atomic replace after the optional backup copy. Catalog: LP-1018 to LP-1028 (11 features: JPEG options, JPEG metadata carry-over, options shown on Save As, JPEG size targeting, and GIF, PNG, legacy, TIFF, JPEG 2000, WebP and JPEG XL options, and the save-dialog restriction list). -> SOURCE: parity-lumen-save-options

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/save-options/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Slider/README.md, docs/design/components/TextBox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Button/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user saves exactly the file they need (a size-capped JPEG, a lossless WebP, a 1-bit TIFF) and reuses the settings. Consumer: the written file, export (`D04 T02 §6`), batch convert (`D04 T11 §4`), and the viewer's Save As.
**Treatment:** IrfanView's per-format Save options panel beside the Save As dialog, opened automatically for formats with options, with named profiles and a JPEG preview dialog (estimated quality, target size, live size readout). Cheaper substitute that fails the checkpoint: fixed defaults per format.
**Chrome:** consume the option records moved to `Photon.Core/Formats/Options/`, the option renderer moved to `Photon.UI`, the settings store, `AtomicFileWriter`, and `D04 T11 §1`'s `OriginalWritePolicy`. Do not add a second options dialog per format.

**Requires:** display-session -- the save options panel and JPEG preview need an interactive desktop

**Freeze check:** Every Lumen save writes through `AtomicFileWriter`; a target equal to an original is refused naming the file unless `OriginalWritePolicy` allows the operation in place, in which case the backup copy (when `Lumen.Originals.BackupBeforeInPlace` is on) is written and verified by hash before the atomic replace; a failed or cancelled write leaves the target byte-identical. The in-place path is the operator-approved change of 2026-09-27 ("safe by default, opt-in writes"). Fixture source: `tests/fixtures/formats/save-options/` (created by this section).

- [ ] Move the writers and option records of `D03 T17 §5`, `§8`, and `§11` to `src/Photon.Core/Formats/` (writers) and `src/Photon.Core/Formats/Options/` (records) with `git mv`, repointing Imago's save dialog. Done when: `grep -rn "record JpegWriteOptions" src` prints one path under `src/Photon.Core/Formats/Options/` and Imago's writer tests pass unchanged.
- [ ] Move Imago's option-page renderer (the descriptor shell of `D03 T17 §1`) to `src/Photon.UI/Formats/FormatOptionsView.xaml` as `SaveOptionsPanel`, repointing Imago. Done when: Imago's option pages render from the moved control and `grep -rn "class SaveOptionsPanel" src` prints one path.
- [ ] Add JPEG options (LP-1018): quality, progressive, optimized Huffman tables, subsampling 4:4:4, 4:2:2, and 4:2:0, grayscale, saved defaults, and named profiles in `Lumen.Formats.Jpeg.Profiles`. Done when: exiftool 13 reads back the subsampling and progressive flag of each written combination.
- [ ] Add JPEG metadata carry-over (LP-1019): keep EXIF, IPTC, XMP, and comment each by choice, reset orientation to 1 after a pixel rotation, and an embedded and DCF thumbnail policy. Done when: exiftool 13 shows each kept block and orientation 1 on a rotated output.
- [ ] Add JPEG size targeting (LP-1021): estimate the source's quality from its quantization tables, binary-search quality to a target size, and a preview dialog with the live file size. Done when: `JpegSizeTargetTests` hit a 500 KB target within 5 percent on the fixture set and estimate a known quality-85 file as 85 plus or minus 2.
- [ ] Open `SaveOptionsPanel` automatically on Save As when the chosen format has options, governed by `Lumen.Formats.ShowOptionsOnSave` (default true) (LP-1020). Done when: a driven Save As to WebP shows the panel without a click and the capture is committed.
- [ ] Add GIF options (LP-1022): interlaced, automatic or custom transparent color, palette index, window color, single frame only (animation authoring is Imago's `D03 T23 §5`). Done when: ImageMagick 7.1 reads back the interlace flag and transparent index.
- [ ] Add PNG options (LP-1023): compression level, automatic or custom transparency, window color, synthetic alpha, and an optimize pass (own zlib pass, plus oxipng (MIT) as an optional external tool when installed). Done when: the optimized output rereads pixel-exact and is no larger than the unoptimized one.
- [ ] Add legacy options (LP-1024): PNM binary or ASCII, ICO transparency and window color, TGA and BMP RLE. Done when: each written variant rereads exactly in ImageMagick 7.1.
- [ ] Add TIFF options (LP-1025): compression per color and 1-bit images (none, LZW, ZIP, JPEG, CCITT G3 and G4, PackBits), grayscale palette, and save all pages. Done when: libtiff 4.7 `tiffinfo` reports each compression of the written fixtures.
- [ ] Add JPEG 2000 options (LP-1026): quality, target bytes, lossless (OpenJPEG, BSD-2-Clause). Done when: a lossless JP2 round-trips exactly and a target-bytes write lands within 5 percent.
- [ ] Add WebP and JPEG XL options (LP-1027): quality, lossless, effort, keep metadata. Done when: lossless outputs reread exactly and exiftool 13 finds the kept metadata.
- [ ] Add `Lumen.Formats.SaveList` restricting the formats offered in save dialogs (LP-1028). Done when: removing TGA hides it from Save As and batch convert without a restart.
- [ ] Store option profiles per format with export and import as JSON beside Lumen's presets. Done when: an exported profile imported on a clean settings file writes identical bytes.
- [ ] Warn before writing what the chosen format cannot carry (alpha to JPEG, 16 bits to GIF, layers of a composite), from the registry's capabilities. Done when: a test asserts the warning text for alpha to JPEG.
- [ ] Route every Lumen save through `OriginalGuard` and `OriginalWritePolicy` of `D04 T11 §1`: a new path writes through `AtomicFileWriter`; a path equal to an original is refused by name unless the policy allows the operation in place. Done when: `SaveGuardTests` assert the refusal with the policy off and, with it on, a verified backup plus an atomic replace. Cheaper substitute: writing straight over the original, which the killed-process test of the backup path catches.
- [ ] Add the Options button to §4's Extract Pages dialog and multipage editor save, opening the chosen format's panel. Done when: extracting pages as JPEG at quality 60 writes files exiftool reads as quality 60.
- [ ] Commit fixtures under `tests/fixtures/formats/save-options/` with `reference.txt` naming libvips 8.16, exiftool 13, ImageMagick 7.1, and libtiff 4.7. Done when: every fixture carries its note.
- [ ] Add `WriterOptionFidelityTests` (`[Trait("Category", "Fidelity")]`) writing each option combination and rereading it with libvips 8.16 and exiftool 13 (subsampling, progressive flag, metadata presence, target size within 5 percent). Done when: the test prints each option's reread result.
- [ ] Commit captures under `docs/captures/lumen/save-options/` and write `docs/user/lumen/save-options.md`. Done when: every format's panel and the JPEG preview appear in captures and the page documents them.
- [ ] Commit: `"lumen: per-format save options shared by export, convert, and Save As"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~WriterOption|FullyQualifiedName~SaveGuard|FullyQualifiedName~JpegSizeTarget"` exits 0 quoting each option's reread result, the in-place refusal with the policy off, and the verified backup with it on. Cheaper substitute that fails: options only on export, which the driven Save As capture and the `ShowOptionsOnSave` test catch.

## 7. The DNG Writer

Convert to DNG, render to DNG, and smart previews all need a DNG writer, and the suite needs exactly one. Lumen owns it in `Photon.Lumen.Core/Dng/`, written from the Adobe DNG Specification 1.7.1.0 with its own lossless JPEG encoder, and validated by Adobe's `dng_validate`; Adobe's DNG SDK is an oracle only, never a dependency. Its consumers are `D04 T07 §6` (Convert to DNG), `D04 T06 §11` (smart previews), and `D04 T12 §2` (DNG export). The source file is opened read-only and never written. Catalog: LP-1029 (1 feature: GoPro GPR write, which is DNG with VC-5 compression through the same writer interface). -> SOURCE: parity-lumen-dng-writer

**Fidelity:** no surface of its own (the conversion dialogs are `D04 T07 §6` and `D04 T12 §2`).

**Freeze check:** `DngWriter` opens its source read-only and asserts the source's SHA-256 unchanged after every write; output goes through `AtomicFileWriter` to a new path, never the source's; a failed or cancelled write leaves no partial DNG. Fixture source: `tests/fixtures/lumen/dng-writer/` (created by this section).

- [ ] Add `DngWriter` in `src/Lumen/Photon.Lumen.Core/Dng/DngWriter.cs` writing the DNG 1.7 layout: IFD0 with the preview, a raw SubIFD, `DNGVersion` 1.7.1.0 and `DNGBackwardVersion` by compatibility level. Done when: `dng_validate` 1.7.1 accepts an uncompressed write of the committed DNG fixture with zero errors.
- [ ] Write mosaic data with `CFARepeatPatternDim` and `CFAPattern`, or linear raw with `PhotometricInterpretation` LinearRaw, from `D04 T01 §4`'s decoded raw buffer. Done when: both a Bayer and a linear fixture validate with zero errors.
- [ ] Write the color tags `ColorMatrix1` and `ColorMatrix2`, `CalibrationIlluminant1` and `2`, `ForwardMatrix` where known, `AsShotNeutral`, `BaselineExposure`, `DefaultCrop`, `ActiveArea`, and `BlackLevel` and `WhiteLevel`. Done when: `dng_validate -v` prints the matrices equal to the decoder's.
- [ ] Copy `OpcodeList1` to `3` from the decoder where present. Done when: a fixture with a lens-correction opcode list rereads with the list byte-equal.
- [ ] Add an own lossless JPEG encoder in `src/Lumen/Photon.Lumen.Core/Dng/LosslessJpegEncoder.cs` (ITU T.81 process 14, predictor 1) tiled 256 by 256. Done when: `LosslessJpegTests` round-trip random 16-bit tiles bit-exact through the decoder's lossless JPEG path.
- [ ] Write lossy DNG as baseline JPEG tiles for smart previews at 2,560 px on the long edge. Done when: a lossy write validates with zero errors and decodes within 2/255 after develop.
- [ ] Write JPEG XL compressed raw (DNG 1.7) behind `DngWriteOptions.Compression = JpegXl` when libjxl is present, refused by name otherwise. Done when: a JXL write validates with zero errors when libjxl is installed and the refusal is asserted without it.
- [ ] Add `DngWriteOptions` (compatibility level, preview size none, medium, or full, fast-load data, lossy, embed original raw) in `src/Lumen/Photon.Lumen.Core/Dng/DngWriteOptions.cs`. Done when: each option combination validates with zero errors.
- [ ] Embed the original raw file as `OriginalRawFileData` with `OriginalRawFileName` and its digest when asked. Done when: extracting the embedded data with `dng_validate -extract` yields a file byte-identical to the source.
- [ ] Write `RawImageDigest` or `NewRawImageDigest` and the fast-load preview when asked. Done when: `dng_validate` reports the digest as valid.
- [ ] Write EXIF and XMP, including develop settings through `D01 T07 §6`'s XMP core. Done when: exiftool 13 reads back the camera model, capture time, and a develop setting equal to the catalog's.
- [ ] Write GoPro GPR through the GPR SDK (Apache-2.0 or MIT) as DNG with VC-5 compression behind the same writer interface, native per runtime identifier, with a `docs/dev/decisions.md` row (LP-1029). Done when: a written GPR decodes through the SDK's own `gpr_tools` to the same raw data.
- [ ] Open the source read-only, write through `AtomicFileWriter` to a new path, and assert the source's SHA-256 unchanged after the write. Done when: `DngWriterGuardTests` pass and a killed-process test leaves no partial file.
- [ ] Commit fixtures under `tests/fixtures/lumen/dng-writer/` (the committed DNG, a linear DNG, a corpus subset of three makes, a GoPro GPR) with `reference.txt` naming `dng_validate` 1.7.1 and exiftool 13. Done when: every fixture carries its note.
- [ ] Add `DngWriterFidelityTests` (`[Trait("Category", "Fidelity")]`): each write validates with zero errors and rereads through `D04 T01 §4` bit-exact for lossless or within 2/255 after develop for lossy. Done when: the test quotes `dng_validate` output per fixture.
- [ ] Commit: `"lumen: a DNG writer validated against dng_validate"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~DngWriter|FullyQualifiedName~LosslessJpeg"` exits 0 with `dng_validate` output quoted at zero errors per fixture and the bit-exact reread passing. Cheaper substitute that fails: wrapping a JPEG in a TIFF container, which `dng_validate` rejects.

## 8. Rare and Historical Raster Formats

IrfanView's Formats plug-in reads a long tail no other competitor carries: home-computer formats, fax formats, Photo CD, PICT, and a raw-pixel open for undocumented dumps. Lumen reads them through small managed readers in `Photon.Core/Formats/Rare/` from published descriptions, registers the shared GEM IMG, Photo CD, FlashPix, PICT, and Corel PHOTO-PAINT CPT codecs of `D01 T08` rather than building its own, reads and writes JPEG-LS through CharLS, and shows font files and the embedded thumbnails of Affinity and Canvas documents. The formats that need a proprietary SDK, a removed runtime, or an undocumented layout are planned apart: CAD and plotter drawings in §9, Flash SWF in §10, ECW, MrSID, JPM, and MRC through an optional GDAL in §11, and the undocumented layered formats in §12. Catalog: LP-1030 to LP-1042, LP-1045, LP-1051 (15 features: Affinity and Canvas thumbnails, the rare raster set, Photo CD, PICT, raw pixel open, JPEG-LS, raw binary and YUV, Photo CD load resolution, TIFF annotations, font sample rendering, FLIF, WBZ, WBC, and WSQ, MNG, JNG, FLI, and FLC, TrueType preview, CPT, and FlashPix). -> SOURCE: parity-lumen-rare-formats

**Corrected 2026-09-27:** at authoring FlashPix (LP-1051) and Corel PHOTO-PAINT CPT (LP-1045) were in the backlog entry for formats without a GPL-compatible reader because none existed; the operator's 2026-09-27 "Group 1: plan them all" decision planned both in `D01 T08` (FlashPix in `§2`, CPT in `§5`), so the Lumen integration moves them here as registrations of those shared codecs. MRC (LP-1621) and Artweaver, BodyPaint 3D, Gemstone GSD, and ACDSee ACDC (LP-1622) were promoted by the operator on 2026-09-27 into §11 and §12.

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/raw-open/` and `docs/captures/lumen/photo-cd/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can see any old image they own and pull pixels out of an undocumented dump. Consumer: the viewer, browse thumbnails, and batch convert reading the decoded image.
**Treatment:** IrfanView's Open as RAW dialog (width, height, header bytes, bits per pixel, color order, planar or interleaved, vertical flip, saved presets) and a Photo CD resolution choice (Base/16 to 64Base). Cheaper substitute that fails the checkpoint: a guessed raw size with no dialog.
**Chrome:** consume `Photon.UI` dialog styles, the settings store, and the registry. Do not add a second raw-data codec beside `D03 T17 §6`'s.

**Requires:** display-session -- the raw-open dialog and its captures need an interactive desktop

**Freeze check:** Raw binary, YUV, and JPEG-LS writers save through `AtomicFileWriter` to new paths; a failed or cancelled write leaves any existing target byte-identical; TIFF annotations are drawn as an overlay and never merged into pixels or written back. Fixture source: `tests/fixtures/formats/rare/` (created by this section).

- [ ] Register Amiga IFF and LBM through `D03 T17 §9`'s ILBM reader and add Atari Degas (PI1 to PI3, PC1 to PC3) and NEOchrome readers in `src/Photon.Core/Formats/Rare/Atari/` (LP-1031). Done when: each fixture matches ImageMagick 7.1 or its reference-viewer golden exactly.
- [ ] Add Commodore 64 Koala and Art Studio and ZX Spectrum SCR readers in `src/Photon.Core/Formats/Rare/EightBit/` with their fixed palettes (LP-1031). Done when: fixtures match committed goldens from the format's reference viewer exactly.
- [ ] Register the shared GEM IMG codec of `D01 T08 §1` and add SIF, Casio CAM, and G3 fax (ITU-T T.4) and Structured Fax readers in `src/Photon.Core/Formats/Rare/` (LP-1031). Done when: each fixture matches its golden exactly and `grep -rn "class GemImgCodec" src` prints one path.
- [ ] Add readers for Windows clipboard CLP, GLCD, MAKI MAG, Utah RLE, Mosaic, Bio-Rad PIC, ICS, and AT&T ICN in `src/Photon.Core/Formats/Rare/`, and register SGI and RGBA and Sun raster from `D03 T17 §8` (LP-1031). Done when: each fixture matches its golden exactly.
- [ ] Register the shared `PhotoCdCodec` of `D01 T08 §2` (Base/16 to 64Base with the Huffman residual planes) for Lumen (LP-1032). Done when: `grep -rn "class PhotoCdCodec" src` prints one path and a PCD fixture at Base matches ImageMagick 7.1 within 1/255.
- [ ] Add `Lumen.Formats.PhotoCd.Resolution` (Base/16 to 64Base, default Base), passed as `D01 T08 §2`'s `PhotoCdDecodeOptions`, and a resolution choice on open (LP-1037). Done when: a driven open at 4Base yields 3,072 by 2,048 and the capture is committed.
- [ ] Register the shared FlashPix reader of `D01 T08 §2` (the highest resolution level, with its color space tagged through `D01 T04 §1`) for Lumen (LP-1051), through the same `IRasterCodec` adapter as the other `D01 T08` codecs. Done when: `grep -rn "class FlashPixCodec" src` prints one path and an FPX fixture matches ImageMagick 7.1 within the tolerance `D01 T08 §2` states.
- [ ] Register the shared CPT reader of `D01 T08 §5` for Lumen as a flattened read (LP-1045), with the layered-file notice naming Imago; if `D01 T08 §5` rerouted CPT with its analysis evidence instead, reroute LP-1045 to the clean-room analysis of §12 in `docs/parity/lumen-parity.md` in this section's commit and say so. Done when: a CPT fixture's composite matches the `D01 T08 §5` golden within its tolerance, or the catalog row names `plan D04 T13 §12` with the reroute evidence cited.
- [ ] Register the shared PICT reader and `PictRasterizer` of `D01 T08 §4` (bitmap opcodes, QuickTime-wrapped JPEG stills, vector opcodes rasterized, unhandled opcodes reported by number) for Lumen at `Lumen.Formats.Pict.RenderDpi` (default 144) (LP-1033); no QuickTime dependency. Done when: the core PICT fixtures render within 1/255 of their LibreOffice goldens through Lumen's registry.
- [ ] Add the Open as RAW dialog in `src/Lumen/Photon.Lumen.Desktop/Views/Formats/RawOpenDialog.xaml` (width, height, header bytes, bits per pixel, color order, planar or interleaved, vertical flip) with named presets in `Lumen.Formats.RawPresets` (LP-1034). Done when: a driven open of a 16-bit planar dump matches its source pixels and the capture is committed. Cheaper substitute: guessing the size, which the planar fixture defeats.
- [ ] Register raw binary and YUV read and write (I420, NV12, YUY2, UYVY; header, interleaved or planar, channel order) through `D03 T17 §6`'s raw data codec (LP-1036). Done when: a YUV round trip is exact and an I420 fixture matches `ffmpeg`'s committed RGB golden within 1/255.
- [ ] Add JPEG-LS lossless and near-lossless read and write through CharLS (BSD-3-Clause) over P/Invoke, native per runtime identifier, with a `docs/dev/decisions.md` row (LP-1035). Done when: a lossless round trip is exact and a written file decodes in CharLS's own `charlstest` identically.
- [ ] Add FLIF read through `libflif_dec` (Apache-2.0; the LGPL encoder is not shipped), Webshots WBZ and WBC as own container readers over the JPEG codec, and WSQ through NIST NBIS (public domain) (LP-1040). Done when: each fixture matches its reference decoder's committed golden.
- [ ] Add MNG (the LC profile) and JNG readers over the PNG and JPEG codecs, and Autodesk FLI and FLC readers from the FLIC description, each as a frame sequence the viewer plays through `D04 T04 §10` (LP-1041); authoring is Imago's `D03 T23 §5`. Done when: frame counts and the first and last frames match ImageMagick 7.1.
- [ ] Draw TIFF annotation tags (tag 32932, Wang Imaging annotations) as an overlay layer in the viewer, toggled by `Lumen.Formats.Tiff.ShowAnnotations` (default true), never merged into pixels (LP-1038). Done when: an annotated fixture shows the overlay in a capture and the decoded pixels equal the unannotated golden.
- [ ] Render TTF, OTF, and FON font files as a sample sheet with custom text in `Lumen.Formats.FontSample` through `Photon.Core/Text/` (moved by `D03 T16 §1`), with an own FNT parser for FON bitmap fonts; one feature built once for LP-1039 and LP-1042. Done when: a TTF and a FON fixture render to their committed goldens exactly.
- [ ] Read the embedded thumbnails of Affinity (`.afphoto`, `.afdesign`, `.afpub`) and Canvas documents from their containers without parsing the documents (LP-1030); opening them stays Imago's B-045. Done when: each fixture's thumbnail matches the committed PNG extracted by hand, and the notice names Imago.
- [ ] Commit fixtures under `tests/fixtures/formats/rare/` (public-domain samples, each with its source URL in `README.md`) with `reference.txt` naming ImageMagick 7.1 or the format's reference viewer per fixture. Done when: every fixture carries its note and source.
- [ ] Add `RareFormatFidelityTests` (`[Trait("Category", "Fidelity")]`) looping every fixture through the registry and comparing with its golden. Done when: the test prints one result per format, and a registered extension with no fixture fails the loop.
- [ ] Commit captures under `docs/captures/lumen/raw-open/` and `docs/captures/lumen/photo-cd/` and extend `docs/user/lumen/formats.md` with the rare formats and raw open. Done when: both dialogs appear in captures and the page documents them.
- [ ] Commit: `"lumen: rare and historical raster formats, raw pixel open, JPEG-LS"`

**Test checkpoint:** Format fidelity proof and driven run: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~RareFormat"` exits 0 with one result per format and tolerance; the JPEG-LS round trip matches `charlstest`; a driven raw open of a 16-bit planar dump is captured under `docs/captures/lumen/raw-open/`. Cheaper substitute that fails: listing extensions without readers, which the fixture loop's missing-fixture check catches.

## 9. CAD and Plotter Drawings: DXF, DWG, HPGL, and CGM

IrfanView reads DXF, DWG, HPGL, and CGM through shareware CAD plug-ins, and engineers keep drawings beside their photos. Nodus already reads all four with its own code: DXF and DWG on ACadSharp (MIT) in `D02 T14 §10`, and CGM and HPGL with its own `CgmReader` and `HpglReader` in `D02 T14 §11`. Lumen is their second consumer, so this section moves the reading (not Nodus's mapping to editable objects) into `Photon.Core` once, producing a neutral drawing-operation model in the pattern of `D01 T08 §4`'s `PictDrawing` that Nodus maps to objects and a rasterizer renders for Lumen; no reader is copied and no proprietary CAD SDK is used. The operator's 2026-09-27 decision planned the formats deferred after the first release as real sections, and this part runs in the Lumen parity formats phase because its dependencies (Phase 11) are met there. Catalog: LP-1053 (1 feature: CAD formats DXF, DWG, HPGL, and CGM). -> SOURCE: parity-lumen-cad-formats

**Fidelity:** Lumen CAD render options dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/lumen/cad-options/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user browses, rates, and views CAD and plotter drawings beside photos without a CAD program. Consumer: the viewer, browse thumbnails, and batch convert reading the rasterized drawing.
**Treatment:** a CAD render options dialog reached from File Handling and from the viewer's context menu: render size, background (white, black, or transparent), model space or a named layout, line weights on or off, and a pen-color map for HPGL. Cheaper substitute that fails the checkpoint: embedding the DWG's thumbnail preview instead of rendering the drawing, which the entity-level golden comparison catches.
**Chrome:** consume the moved readers, `DrawingRasterizer`, the registry of §1, the settings store, and `Photon.UI` dialog styles. Do not add a second DXF, CGM, or HPGL parser beside the moved ones.

**Requires:** display-session -- the render options dialog and its captures need an interactive desktop

**Freeze check:** The moved readers open files with `FileAccess.Read` and `FileShare.ReadWrite` and never write; rendering the whole CAD fixture set leaves every file's SHA-256 and last-write time unchanged. Fixture source: `tests/fixtures/formats/cad/` (created by this section).

- [ ] Add `src/Photon.Core/Formats/Drawing/DrawingModel.cs`: layers with visibility and color, operations (line, polyline with bulges, arc, circle, ellipse, spline flattened to a stated tolerance, hatch with solid and pattern fills, text run with font, height, rotation, and alignment, raster image reference, and point), line weights, and the drawing extents, in drawing units with a unit tag. Done when: `DrawingModelTests` build one drawing with each operation and enumerate it.
- [ ] Move the ACadSharp reading of `D02 T14 §10` (`CadReader`'s document load, block expansion, layout enumeration, and dimension explosion) into `src/Photon.Core/Formats/Cad/CadDrawingReader.cs` producing a `DrawingModel` per layout, with `git mv` where whole files move, and repoint Nodus's `CadReader` to map from the model. Done when: `grep -rn "using ACadSharp" src` prints paths only under `src/Photon.Core/Formats/Cad/` and every Nodus CAD test from `D02 T14 §10` passes unchanged.
- [ ] Move ACadSharp's `PackageReference` from Nodus's project to `Photon.Core` and update its `docs/dev/decisions.md` row to name both consumers. Done when: `dotnet list src/Nodus package` no longer lists ACadSharp directly and the row names Lumen.
- [ ] Move `CgmReader` and `HpglReader` of `D02 T14 §11` into `src/Photon.Core/Formats/Vector/` producing `DrawingModel`, repointing Nodus's CGM and HPGL import (the writers stay in Nodus: only Nodus writes them). Done when: `grep -rn "class CgmReader\|class HpglReader" src` prints one path each, under `src/Photon.Core/`, and Nodus's metafile tests pass.
- [ ] Add `src/Photon.Core/Formats/Drawing/DrawingRasterizer.cs` rendering a `DrawingModel` through SkiaSharp into a `PixelBuffer<Rgba8>` at a requested long edge, fitting the extents, honoring layer visibility, line weights, and the background choice. Done when: `DrawingRasterizerTests` render a line, arc, hatch, and text fixture to committed goldens exactly.
- [ ] Register DXF, DWG, CGM, and HPGL (`.plt`, `.hpgl`, `.hgl`) in §1's registry as read-only formats decoding through `DrawingRasterizer`, with content sniffing (DXF `SECTION` group code, DWG `AC10xx` version string, CGM binary and clear-text headers, HPGL `IN;` or `PU` prologue). Done when: `FormatSniffTests` pick each fixture by content with a wrong extension.
- [ ] Add `Lumen.Formats.Cad.RenderSize` (default 3,000 px long edge), `.Background` (White), `.Space` (Model or a layout name), `.LineWeights` (true), and `Lumen.Formats.Hpgl.PenColors`, each read by the rasterizer on every decode. Done when: changing the render size in settings changes the decoded size without a restart (test asserts).
- [ ] Implement the screen-size decode capability of §1 for drawings by rasterizing at the requested size rather than downscaling a full render. Done when: a thumbnail request for a large DWG fixture allocates no buffer larger than the request (allocation test).
- [ ] Add the CAD render options dialog in `src/Lumen/Photon.Lumen.Desktop/Views/Formats/CadOptionsDialog.xaml` with the Treatment's controls, reached from Preferences, File Handling and the viewer's context menu on a drawing. Done when: a driven run switches a DWG fixture from model space to a layout and the capture shows both. Cheaper substitute: a fixed render size with no dialog.
- [ ] Refuse a drawing that references external xrefs or fonts it cannot find by rendering what exists and listing the missing references in the image information panel of `D04 T04 §9`, never failing silently. Done when: a fixture with a missing xref renders and the panel lists the xref name.
- [ ] Refuse encrypted or corrupt DWG files with a typed failure naming the file and the ACadSharp reason. Done when: a truncated DWG fixture yields the message and no exception reaches the viewer.
- [ ] Commit fixtures under `tests/fixtures/formats/cad/` (DXF R12 and 2018, DWG 2000, 2007, and 2018 with blocks, hatches, dimensions, text, and layouts, CGM binary and clear text, HPGL and HP-GL/2 plots) with `reference.txt` naming LibreCAD 2.2 PNG export for DXF and DWG, LibreOffice 25.x `soffice --convert-to png` for CGM, and Inkscape 1.4 for HPGL, with versions and commands. Done when: every fixture carries its note and its source or license.
- [ ] Add `CadFormatFidelityTests` (`[Trait("Category", "Fidelity")]`) rendering every fixture at the golden's size and comparing within 3/255 mean, plus the Nodus import tests run over the same fixtures through the moved readers. Done when: the test prints one result per fixture with its tolerance.
- [ ] Log one Serilog Information line per drawing decode with format, version, entity count, and milliseconds. Done when: a test logger asserts the line.
- [ ] Commit captures under `docs/captures/lumen/cad/` and extend `docs/user/lumen/formats.md` with CAD and plotter drawings and the render options. Done when: the dialog appears in a capture and the page documents every option.
- [ ] Commit: `"lumen: CAD and plotter drawings through Nodus's readers moved to Photon.Core"`

**Test checkpoint:** Format fidelity proof and driven run: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~CadFormat|FullyQualifiedName~DrawingRasterizer|FullyQualifiedName~Nodus.Tests.Cad"` exits 0 with every fixture within tolerance of its LibreCAD, LibreOffice, or Inkscape golden and Nodus's CAD and metafile tests green against the moved readers; `grep -rn "class CgmReader\|class HpglReader\|using ACadSharp" src` prints paths only under `src/Photon.Core/`; a driven model-to-layout switch is captured under `docs/captures/lumen/cad/`. Cheaper substitute that fails: showing the DWG's embedded thumbnail, which the entity-level golden comparison catches.

## 10. Flash SWF: the First Frame Through an Own Parser

IrfanView shows Flash files through a plug-in that needs the removed Flash runtime. The files still sit in archives, and the first frame is almost always the picture the user wants to see. This section reads SWF with an own managed parser built from the SWF File Format Specification version 19 and renders the first frame's shapes, bitmaps, and text outlines, never executing ActionScript and needing no Flash runtime. FLV, the other half of the catalog row, is video and plays through the optional FFmpeg of `D01 T11 §1` in Lumen's playback (`D04 T16 §2`). Catalog: LP-1050 (1 feature: Flash SWF and FLV; the SWF part here, the FLV part in `D04 T16 §2`). -> SOURCE: parity-lumen-swf

**Fidelity:** no surface of its own (SWF decodes into §1's registry and the viewer of `D04 T04 §2` shows it like any image).

**Freeze check:** The SWF reader opens files read-only and never writes; decoding the fixture set leaves every SHA-256 and last-write time unchanged. Fixture source: `tests/fixtures/formats/swf/` (created by this section).

- [ ] Add `src/Photon.Core/Formats/Swf/SwfHeaderReader.cs` for the `FWS` (uncompressed), `CWS` (zlib through `ZLibStream`), and `ZWS` (LZMA) signatures, the frame rectangle in twips, frame rate, and frame count. Done when: `SwfHeaderTests` read each fixture's header equal to the values `swfdump` 0.9.2 prints, recorded in the fixture note.
- [ ] Vendor the managed LZMA decoder of the 7-Zip LZMA SDK (public domain) as source under `src/Photon.Core/Formats/Swf/Lzma/` with its notice and a `docs/dev/decisions.md` row. Done when: a `ZWS` fixture decompresses to the byte length its header states.
- [ ] Add the tag reader in `SwfTagReader.cs` (short and long record headers), keeping the dictionary of character definitions up to the first `ShowFrame`, and skipping every other tag by its length with the unhandled tag codes reported. Done when: a fixture with unknown tags parses to its first frame and the report lists their codes.
- [ ] Parse `DefineShape` 1 to 4: fill styles (solid RGB and RGBA, linear, radial, and focal radial gradients, clipped and repeating bitmap fills), line styles including `LineStyle2` joins and caps, and the edge records (straight and curved, style changes, move-to). Done when: `SwfShapeTests` assert the edge and style counts of each shape fixture.
- [ ] Decode bitmaps: `DefineBits` with `JPEGTables`, `DefineBitsJPEG2`, `DefineBitsJPEG3` and `4` with their zlib alpha planes, and `DefineBitsLossless` 1 and 2 (colormapped and direct). Done when: each bitmap decodes pixel-exact against the same bitmap exported by `swfextract` 0.9.2, recorded.
- [ ] Parse `PlaceObject` 1 to 3 with matrices, color transforms, depth, and clip depth, and `DefineSprite` placed on the first frame rendered at its own first frame. Done when: a fixture with a clipped sprite renders to its golden.
- [ ] Render `DefineText` and `DefineText2` through `DefineFont` 1 to 3 glyph outlines as shapes, and `DefineEditText` as its initial text through the shared text engine (`D03 T16 §1`) where the font is a device font. Done when: a text fixture renders within tolerance of its golden.
- [ ] Add `SwfFrameRasterizer.cs` rendering the display list of the first frame through SkiaSharp at the frame size scaled to the request, honoring the background color from `SetBackgroundColor`. Done when: `SwfRasterizerTests` render a vector-only fixture exactly equal to the committed golden.
- [ ] Never execute ActionScript: `DoAction`, `DoABC`, and `DoInitAction` tags are skipped and reported, and a test asserts no code path interprets them. Done when: an ActionScript fixture renders its static first frame and the report lists the skipped tags.
- [ ] Register SWF in §1's registry with content sniffing on the three signatures, the screen-size decode capability rendering at the requested size, and the viewer's image information naming "first frame of N". Done when: a `.swf` renamed `.bin` opens as SWF and the information panel shows the frame count.
- [ ] Refuse a corrupt or truncated SWF with a typed failure naming the file and the byte offset, and a file whose first frame is empty with "This Flash file draws nothing on its first frame". Done when: tests assert both messages.
- [ ] Commit fixtures under `tests/fixtures/formats/swf/` (made with the free tools listed in the note: shapes and gradients, JPEG and lossless bitmaps with alpha, sprites and clipping, font text, an ActionScript file, `CWS` and `ZWS` variants) with PNG goldens rendered by Ruffle (MIT or Apache-2.0, run as a tool, never bundled; version and command recorded). Done when: every fixture carries its note.
- [ ] Add `SwfFidelityTests` (`[Trait("Category", "Fidelity")]`) comparing each first frame with the Ruffle golden within 3/255 mean. Done when: the test prints one result per fixture with its tolerance.
- [ ] Extend `docs/user/lumen/formats.md` with Flash SWF (first frame only, no animation or ActionScript) and a pointer to FLV playback. Done when: the page states both limits.
- [ ] Commit: `"lumen: Flash SWF first frame through an own parser"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~Swf|FullyQualifiedName~SwfHeader|FullyQualifiedName~SwfShape"` exits 0 with every fixture's first frame within 3/255 mean of Ruffle's golden and every bitmap pixel-exact against `swfextract`; the ActionScript fixture renders statically with its code tags reported. Cheaper substitute that fails: extracting only the largest embedded JPEG, which the vector-only fixture's golden comparison catches.

## 11. ECW, MrSID, JPM, and MRC Through an Optional GDAL

IrfanView reads ECW, MrSID, and JPM through the vendors' proprietary SDK plug-ins and MRC through a 32-bit plug-in, none of which Photon can ship under GPL-3.0. GDAL (MIT) reads the wavelet formats through the same vendors' driver plug-ins, so Lumen offers them through a GDAL the user installs (for example OSGeo4W), run as an external process and never bundled or linked: the pattern of the Ghostscript runner of §4 and `D02 T14 §9`. Lumen converts through a temporary GeoTIFF it reads with its own TIFF codec, reads the driver list and each driver's capabilities from GDAL itself so write options appear only where the installed driver writes, and disables and explains the formats when GDAL or a driver is absent. A format no installable GDAL driver opens is rerouted with the evidence rather than left planned. Catalog: LP-1046, LP-1047, LP-1048, LP-1621 (4 features: JPM read and write, ECW and MrSID read and write, MrSID and JPM loading options, and MRC read). -> SOURCE: parity-lumen-proprietary-formats

**Fidelity:** Lumen File Handling preferences, the GDAL group -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/lumen/gdal-preferences/.
**Design:** docs/design/components/TextBox/README.md, docs/design/components/Button/README.md, docs/design/components/ListTree/README.md, docs/design/components/Toast/README.md, docs/design/components/Checkbox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user who owns GIS or document-archive imagery opens ECW, MrSID, JPM, and MRC files in Lumen by pointing it at their own GDAL. Consumer: the viewer, browse thumbnails, and batch convert reading the converted raster; the preferences group reads GDAL's driver list.
**Treatment:** a GDAL group on the File Handling page of `D04 T14 §4`: the GDAL location with Browse and Detect, a status line (version found or "not found"), a driver list showing each of ECW, MrSID, JP2 and JPM, and MRC with read and write capability or "driver not installed", and an overview-level choice for MrSID and ECW loading. Cheaper substitute that fails the checkpoint: registering the extensions and failing on open, which the absent-driver message test catches.
**Chrome:** consume the external-process runner pattern of `D04 T13 §4`'s Ghostscript runner, §1's registry and TIFF codec, the settings store, and the `D04 T14 §4` page. Do not bundle, link, or P/Invoke any GDAL library.

**Requires:** display-session -- the preferences group and its captures need an interactive desktop

**Freeze check:** GDAL reads the source through `gdal_translate` into a temporary file under Lumen's temp folder, never the source's folder; writes go to new paths through a temporary file and an atomic rename; an in-place write over an original is refused unless `OriginalWritePolicy` (`D04 T11 §1`) allows it; decoding the fixture set leaves every source's SHA-256 and last-write time unchanged. Fixture source: `tests/fixtures/formats/gdal/` (created by this section).

- [ ] Record the GDAL decision in `docs/dev/decisions.md`: GDAL (MIT) and its vendor driver plug-ins are optional, user-installed, run only as external processes (`gdalinfo`, `gdal_translate`), never bundled, linked, or loaded in-process, so no proprietary SDK license reaches Photon's GPL-3.0 binaries. Done when: the row names the licenses, the process boundary, and this section.
- [ ] Add `src/Photon.Core/Formats/Gdal/GdalLocator.cs` finding `gdalinfo.exe` and `gdal_translate.exe` from `Lumen.Formats.Gdal.Path`, then `PATH`, then the OSGeo4W default folder, and reading `gdalinfo --version`. Done when: `GdalLocatorTests` over fake executables assert the search order and the parsed version.
- [ ] Add `GdalDriverCatalog.cs` running `gdalinfo --formats -json` once per session and caching each driver's short name, long name, and capabilities (raster, read, `CreateCopy`, virtual I/O). Done when: a recorded JSON fixture yields ECW read and write, MrSID read only, and JPEG2000 read.
- [ ] Add `GdalRunner.cs` running `gdal_translate -of GTiff -co COMPRESS=DEFLATE` from the source into a temp file with a timeout (`Lumen.Formats.Gdal.TimeoutSeconds`, default 120), cancellation that kills the process, and stderr captured into the failure message. Done when: a test with a fake executable that hangs asserts the timeout message and no orphan process.
- [ ] Map the screen-size decode capability to `gdal_translate -outsize <w> <h>` and the overview choice to `-ovr <level>` (MrSID and ECW loading options, LP-1048), stored in `Lumen.Formats.Gdal.OverviewLevel` (default Auto). Done when: a thumbnail request produces a temp file of the requested size (test with a fake runner asserting the arguments).
- [ ] Map band layouts: RGB, RGBA, single-band gray, and paletted bands with `-expand rgb`, and 16-bit data scaled with the dataset's statistics (`-scale`) into 8 or 16 bits as the TIFF codec reads it. Done when: a test asserts the argument list for each layout from recorded `gdalinfo -json` output.
- [ ] Register ECW (`.ecw`), MrSID (`.sid`), JPM (`.jpm`, `.jpgm`), and MRC (`.mrc`) in §1's registry through a `GdalBackedCodec` whose availability comes from the driver catalog, so the format matrix of §1 shows each as available, "needs GDAL", or "needs the <driver> GDAL driver". Done when: `FormatMatrixTests` with no GDAL list all four as unavailable with their reasons.
- [ ] Show the refusal on open when GDAL or the driver is absent ("ECW needs GDAL with the ECW plug-in; install it or set its location in Preferences, File Handling") and never attempt a fallback decode. Done when: a test asserts the exact message per format.
- [ ] Add writing where the installed driver advertises `CreateCopy` (LP-1046, LP-1047): ECW with a target compression ratio (`-co TARGET=<percent>`) and JPM with quality, through §6's write path to a new file via a temp GeoTIFF source, with the options shown only when the capability exists. Done when: a test with a recorded capability set asserts the options appear for ECW and not for MrSID.
- [ ] Add the GDAL group to the File Handling page of `D04 T14 §4` with the Treatment's controls and Detect running `GdalLocator`. Done when: a driven run with a GDAL install shows the version and driver list in a capture, and without one shows "not found".
- [ ] Assert the package never ships GDAL: `scripts/package.ps1`'s file list for Lumen contains no `gdal*.dll`, `gdal*.exe`, or `*ECW*` or `*MrSID*` library. Done when: `PackageContentsTests` fail on a planted `gdal304.dll`.
- [ ] Commit fixtures under `tests/fixtures/formats/gdal/` only where their license permits (ECW and MrSID samples from the vendors' free sample sets with their terms in `README.md`), with PNG goldens produced by `gdal_translate` at the recorded GDAL version, and `[Trait("Requires", "gdal")]` fidelity tests that skip with a reason when GDAL or the driver is absent. Done when: every fixture carries its note, and on a machine with GDAL the tests compare within 1/255.
- [ ] Verify MRC and JPM on a GDAL install with every driver plug-in the vendors offer: if no installable GDAL driver opens MRC (LP-1621) or JPM (LP-1046), reroute that row in `docs/parity/lumen-parity.md` to the backlog through `add-todo` with the driver list quoted as evidence, in this section's commit. Done when: each of the two rows either names a passing fidelity result or names its new backlog entry with the evidence.
- [ ] Log one Serilog Information line per GDAL conversion with driver, source size, output size, and milliseconds, and one Warning per refusal. Done when: a test logger asserts both.
- [ ] Extend `docs/user/lumen/formats.md` with the GDAL route: what to install, how Lumen finds it, which formats it enables, and that Lumen never ships it. Done when: the page names every setting and message above.
- [ ] Commit: `"lumen: ECW, MrSID, JPM, and MRC through an optional user-installed GDAL"`

**Test checkpoint:** Unit test plus format fidelity proof where GDAL is present: `dotnet test Photon.slnx --filter "FullyQualifiedName~Gdal|FullyQualifiedName~FormatMatrix|FullyQualifiedName~PackageContents"` exits 0, proving the search order, the argument mapping, the absent-driver messages, the timeout kill, and that no GDAL file ships; on a machine with GDAL and its drivers the `Requires=gdal` fidelity tests compare each fixture within 1/255 of `gdal_translate`'s own PNG and the preferences capture shows the driver list. Cheaper substitute that fails: listing the extensions as supported without GDAL, which the absent-driver message test catches.

## 12. Artweaver, BodyPaint 3D, Gemstone GSD, and ACDSee ACDC Through Clean-Room Analysis

ACDSee and IrfanView open four layered formats whose vendors publish no description: Artweaver (`.awd`), BodyPaint 3D (`.b3d`), Gemstone GSD, and ACDSee's own ACDC documents. The operator approved clean-room reverse engineering of undocumented formats on 2026-09-27 and planned these as a real section. The procedure keeps the work clean: an analysis role studies sample files the project creates or legally owns and writes a structure note; an implementation role builds only from that note; no vendor program is disassembled or its code read beyond observing the files it writes. Each reader produces the flattened composite (and layers as pages where the note establishes them), with the layered-file notice naming Imago, the suite's layered editor. A format whose structure cannot be established is rerouted to the backlog with the analysis evidence, never left half-read. Catalog: LP-1622 (1 feature: Artweaver, BodyPaint 3D, Gemstone GSD, and ACDSee ACDC layered documents). -> SOURCE: parity-lumen-cleanroom-formats

**Fidelity:** no surface of its own (flattened reads into §1's registry; the viewer shows them and the layered-file notice of §3 names Imago).

**Freeze check:** Every clean-room reader opens its file read-only and never writes; decoding the fixture set leaves every SHA-256 and last-write time unchanged. Fixture source: `tests/fixtures/formats/cleanroom/` (created by this section).

- [ ] Write the procedure in `docs/dev/formats/clean-room.md`: the two roles, what the analysis role may use (sample files, hex and structure viewers, the vendor application run as a black box to create and export samples), what it may not (disassembly, decompilation, or reading vendor code or SDK headers), and that the implementation role reads only the notes. Done when: the page exists and names the operator's 2026-09-27 approval.
- [ ] Obtain the vendor applications legally (Artweaver Free, a BodyPaint 3D or Cinema 4D trial, Gemstone's editor, ACDSee Photo Studio's trial) and record each version and license in `tests/fixtures/formats/cleanroom/README.md`. Done when: every application used carries its version, source URL, and license terms.
- [ ] Create sample files per format with controlled content (a solid-color layer, a gradient layer, a layer with alpha, hidden layers, a blend mode, a text layer where the format has one, and sizes of 1x1, 257x129, and 4096x4096) and export each composite to PNG from the same application as the golden. Done when: every sample has its PNG golden and a manifest of what it contains.
- [ ] Write `docs/dev/formats/artweaver-awd.md` from the Artweaver samples: signature, container layout, header fields, layer records, compression, pixel order, and the composite if stored. Done when: the note explains every byte range of the samples it covers or marks it unknown.
- [ ] Write `docs/dev/formats/bodypaint-b3d.md` from the BodyPaint 3D samples with the same structure. Done when: the note covers the samples as above.
- [ ] Write `docs/dev/formats/gemstone-gsd.md` from the Gemstone samples with the same structure. Done when: the note covers the samples as above.
- [ ] Write `docs/dev/formats/acdsee-acdc.md` from the ACDSee samples with the same structure. Done when: the note covers the samples as above.
- [ ] Add `src/Photon.Core/Formats/CleanRoom/AwdReader.cs` built only from its note, producing the composite (and layers as `IPagedImage` pages of §4 where the note establishes them). Done when: every Artweaver sample's composite matches its golden within 1/255.
- [ ] Add `B3dReader.cs` built only from its note, as above. Done when: every BodyPaint sample's composite matches its golden within 1/255.
- [ ] Add `GsdReader.cs` built only from its note, as above. Done when: every Gemstone sample's composite matches its golden within 1/255.
- [ ] Add `AcdcReader.cs` built only from its note, as above. Done when: every ACDC sample's composite matches its golden within 1/255.
- [ ] Register the four readers in §1's registry with content sniffing from the notes' signatures and the layered-file notice of §3 naming Imago. Done when: each sample renamed to a wrong extension opens by content and shows the notice.
- [ ] Refuse a variant the note does not cover (an unknown version, compression, or record) with a typed failure naming the file, the format, and the offset, never guessing pixels. Done when: a mutated sample yields the message.
- [ ] Reroute any format whose structure the analysis cannot establish well enough to pass its goldens: split its part of LP-1622 into a new catalog row that names a new backlog entry filed through `add-todo`, with the analysis note committed as the evidence, in this section's commit. Done when: each of the four formats either passes its fidelity test or names its backlog entry with the note cited.
- [ ] Add `CleanRoomFidelityTests` (`[Trait("Category", "Fidelity")]`) looping every sample against its vendor-exported golden. Done when: the test prints one result per sample with its tolerance.
- [ ] Extend `docs/user/lumen/formats.md` with the four formats (flattened view; edit layers in Imago where it opens them). Done when: the page lists each format with its limits.
- [ ] Commit: `"lumen: Artweaver, BodyPaint 3D, Gemstone GSD, and ACDC through clean-room readers"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~CleanRoom"` exits 0 with every sample's composite within 1/255 of the vendor application's own PNG export, and each format's structure note is committed under `docs/dev/formats/`; any rerouted format's catalog row names its backlog entry with the note as evidence. Cheaper substitute that fails: showing an embedded thumbnail and calling it the image, which the 4096x4096 sample's golden comparison catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` passes every fixture under `tests/fixtures/formats/` and `tests/fixtures/lumen/dng-writer/` with tolerances printed
- [ ] `grep -rn "class FormatRegistry" src` prints exactly one path, under `src/Photon.Core/Formats/`, and no `Photon.Lumen.*.csproj` references an Imago project
- [ ] The unchanged-originals test over every format fixture passes, and `SaveGuardTests` prove the in-place path writes only with the policy on and a verified backup
- [ ] `docs/user/lumen/formats.md` and `docs/user/lumen/cameras.md` equal their generated forms
- [ ] `grep -rn "class CgmReader\|class HpglReader\|using ACadSharp" src` prints paths only under `src/Photon.Core/`, and Nodus's CAD and metafile tests pass against the moved readers
- [ ] No Lumen package contains a GDAL or vendor SDK file (`PackageContentsTests`), and every clean-room format has its structure note under `docs/dev/formats/` or a backlog entry with the evidence
- [ ] `python scripts/todo-graph.py validate` clean
