---
schema_version: 1
id: lumen-parity-output
domain: 04-lumen
status: draft
title: "TODO-12 -- Lumen Parity: Export, Print, Slideshows, Web Galleries, and Books"
depends_on: []
frozen: true
track: L12
---

# TODO-12 -- Lumen Parity: Export, Print, Slideshows, Web Galleries, and Books

> **Goal:** Lumen's output reaches Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76 parity: the export dialog of `D04 T02 §6` grows every destination, naming, format, sizing, color, preset, metadata, watermark, and post-processing option the three apps offer, including DNG and HDR output and local publish folders; a Print module prints single images, grids, picture and custom packages, and contact sheets with printer profiles, print sharpening, and 16-bit output on the suite print frame; slideshows are authored with templates, overlays, titles, music, and transitions and exported to PDF and JPEG; web galleries, books, PDFs, and PowerPoint files are generated locally; and photos go out by email or to the user's own FTP or FTPS server (SFTP is backlog B-053). The code lives in `src/Lumen/Photon.Lumen.Core/Output/` (`Export/`, `Publish/`, `Print/`, `Slideshow/`, `Web/`, `Books/`, `Documents/`, `Share/`) and `src/Lumen/Photon.Lumen.Desktop/Views/Output/`. It consumes the suite engines and never duplicates them (operator decision 2026-09-27): the develop pipeline and export runner (`D04 T02 §2`, `D04 T02 §6`), the token and watermark engines (`D04 T11 §2`, `D04 T11 §8`), the codec writers and DNG writer (`D04 T13 §6`, `D04 T13 §7`), the print frame in `src/Photon.UI/Print/` (`D03 T18 §6`), the suite color engine (`D01 T04 §1`, `D01 T04 §2`), and the suite PDF writer (`D03 T17 §7`); it moves Imago's contact-sheet engine (`D03 T18 §7`) and FTP client (`D03 T17 §12`) to `Photon.Core` on this second use. Every output is a new file written through `AtomicFileWriter`; nothing in this file opens an original for writing. Video export is `D04 T16 §3` and `D04 T16 §6`; self-running EXE and screen-saver slideshows are backlog B-049.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Lumen has no code: `src/Lumen` does not exist, so there is no export, print, slideshow, web, book, or email surface. `todo/04-lumen/TODO-02-lumen-develop.md` §6 plans the first export dialog and `ExportRunner`, which §1 and §13 extend. There is no shared print frame yet: `src/Photon.UI` does not exist, and Imago's print section (`D03 T18 §6`, in `todo/03-imago/TODO-18-imago-parity-output.md`) is what moves Nodus's print frame into it. Lumen's print and contact-sheet idea was backlog B-035 (`lumen-roadmap-print`), which §4 promotes; the Lumen integration deleted the entry. No package the output features add is referenced in `Directory.Packages.props` yet (DocumentFormat.OpenXml, FluentFTP). **Corrected 2026-09-27:** also listed NAudio for slideshow music and SSH.NET for SFTP upload; the operator did not approve either for Lumen, so music plays through Windows Media Foundation over Vortice.MediaFoundation (the player `D04 T04 §8` builds) and SFTP is backlog B-053; the claim below still proves none of the four is referenced.
<!-- claim: absent src/Lumen -->
<!-- claim: absent src/Photon.UI -->
<!-- claim: exists todo/04-lumen/TODO-02-lumen-develop.md -->
<!-- claim: exists todo/03-imago/TODO-18-imago-parity-output.md -->
<!-- claim: count "NAudio|DocumentFormat.OpenXml|FluentFTP|SSH.NET" Directory.Packages.props = 0 -->

## Inputs

- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard, one output transform at the end, preview and export agree within a stated tolerance
- [`standards/shared.md`](../../standards/shared.md) -- atomic writes, refusals that name the target, progress and Cancel over one second, one log line per change, the shared-once rule
- [`docs/parity/lumen-section-design.md`](../../docs/parity/lumen-section-design.md) -- the blueprint for this file; [`docs/parity/lumen-parity.md`](../../docs/parity/lumen-parity.md) -- the catalog rows each section owns
- Lightroom Classic 15.5.1 help: Export, Publish Services, Print, Slideshow, Web, and Book modules; ACDSee Photo Studio Ultimate 2027 guide: Print, Contact Sheet, Slideshow, Create PDF, Create PPT, HTML Album, Send Email; IrfanView 4.76 help: Print dialog, Create Contact Sheet, HTML export, Save as PDF, Send by email
- PDF 1.7 (ISO 32000-1) with PdfPig as the read-back oracle and qpdf `--check`; ECMA-376 (Office Open XML) with the DocumentFormat.OpenXml `OpenXmlValidator`; the W3C Nu HTML Checker (`vnu.jar`) as the HTML oracle; exiftool 13 for metadata read-back; Adobe DNG SDK `dng_validate` as an oracle only
- Microsoft Learn: IMAPI2 (`IDiscMaster2`, `IDiscFormat2Data`), Simple MAPI `MAPISendMailW`, `System.Net.Mail.SmtpClient`, `ProtectedData` (DPAPI)
- [`todo/backlog.md`](../backlog.md) -- B-035 (`lumen-roadmap-print`) is promoted into §4 and leaves the backlog in the integration commit; B-049 (self-running slideshows) stays deferred, and the former B-043 (video) is `D04 T16`
- -> XREF: D04 T02 §6 -- the export runner, dialog, and presets that §1, §2, and §13 extend
- -> XREF: D04 T02 §7 -- stacking of exported files beside the original, reused by §13
- -> XREF: D04 T02 §8 -- Lumen 0.1.0, which every section here follows
- -> XREF: D04 T01 §10 -- the collections §3 publishes and §7, §10 save as slideshow and book collections
- -> XREF: D03 T18 §6 -- the print dialog frame in `Photon.UI/Print/` that §4 consumes through its `IPrintPageSource` seam
- -> XREF: D03 T18 §7 -- the contact-sheet engine §6 moves to `Photon.Core/Print/ContactSheets/`, and the PDF presentation builder §11 reuses
- -> XREF: D03 T17 §2 -- the PSD writer §2's flattened PSD and PSB export uses
- -> XREF: D03 T17 §7 -- the suite PDF writer in `Photon.Core/Pdf/` for books, contact sheets, slideshows, and Create PDF
- -> XREF: D03 T17 §12 -- the FluentFTP client §9 moves to `Photon.Core/Net/Ftp/`
- -> XREF: D03 T16 §1 -- the suite text engine for slideshow and book text
- -> XREF: D01 T03 §2 -- the resamplers export and print expose
- -> XREF: D01 T04 §1 -- ICC transforms for export spaces and printer profiles
- -> XREF: D01 T04 §2 -- rendering intents, proofing transforms, and the gamut warning in print
- -> XREF: D01 T07 §1 -- the SDR tone map §2's gain-map base rendition uses
- -> XREF: D01 T07 §6 -- the XMP develop settings §13 embeds into rendered outputs
- -> XREF: D02 T15 §11 -- `SuiteAppLocator`, used by §13's Open in Imago post-processing action
- -> XREF: D04 T11 §1 -- the Activity Manager every background output job reports to
- -> XREF: D04 T11 §2 -- the token engine for naming, captions, headers, footers, and templates
- -> XREF: D04 T11 §8 -- the watermark engine and editor
- -> XREF: D04 T13 §4 -- PDF page reading for §5's document printing
- -> XREF: D04 T13 §6 -- the codec writers and per-format option pages §1 and §2 list
- -> XREF: D04 T13 §7 -- the DNG writer §2 exports through
- -> XREF: D04 T04 §11 -- the viewer selection §5 prints
- -> XREF: D04 T04 §8 -- the `SlideshowAudioPlayer` (Windows Media Foundation through Vortice.MediaFoundation) §8 plays slideshow music through
- -> XREF: D04 T06 §5 -- collection sets that hold the print, slideshow, web, and book collections §4, §7, §9, and §10 save
- -> XREF: D04 T05 §12 -- the archive creator the Create menu of §11 lists
- -> XREF: D04 T08 §8 -- `ExportMetadataEmbedder`, which §13's metadata choices drive
- -> XREF: D04 T09 §15 -- soft proofing, whose proof transform §4's print color shares
- -> XREF: D04 T10 §1 -- the provenance store §13's AI results warning reads
- -> XREF: D04 T14 §1 -- the identity plate §5, §7, and §9 overlay
- -> XREF: D04 T15 §9 -- the Phase 38 release, `lumen-v0.10.0`
- -> XREF: D06 T01 §3 -- the Lumen user guide pages each section adds
- -> XREF: D04 T07 §1 -- Lumen parity import cites §4: the print module that replaces Copy Shop's printing path when it ships
- -> XREF: D04 T16 §6 -- clips, image audio, and MP4 export extend §8's slideshow; the clip skip in §8 names D04 T16 §6

## Outcome

- The export dialog offers every destination, naming, format, bit depth, color space, sizing, and resampling choice, JPEG size limits, multi-preset export, metadata filters, watermarks, and post-processing, all on the one `ExportRunner` of `D04 T02 §6`.
- Export writes PSD, PSB, TIFF with alpha, AVIF, JPEG XL, DNG, rendered DNG, HDR with gain maps, and original plus sidecar, each proven by a round trip.
- Hard Drive publish keeps a folder in step with a collection, rewriting only what changed and deleting only its own copies.
- The Print module prints single images, grids, packages, contact sheets, and PDF pages with managed color and print sharpening on the suite print frame; one contact-sheet engine exists in `src/Photon.Core/`.
- Slideshows, web galleries, books, PDFs, and PowerPoint files are authored and generated locally and validate against their format oracles.
- Photos go out by email through the mail client or SMTP at a size limit, and to the user's own FTP or FTPS server (SFTP is backlog B-053).
- No output ever writes, moves, or deletes an original.

**Adjacency:** list=applicable @ D04 T12 §13; document=applicable @ D04 T12 §4; settings=applicable @ D04 T12 §1; reporting=applicable @ D04 T12 §13; notifications=applicable @ D04 T12 §13; permissions=applicable @ D04 T12 §1; audit=applicable @ D04 T12 §1; exchange=applicable @ D04 T12 §2; reverse=applicable @ D04 T12 §3

**Adjacency rationale:** The lists are export presets (§13), print templates (§5), slideshow templates (§7), web templates (§9), published collections (§3), and book pages (§10), each with add, update, remove, import, and export. Exports, prints (§4, §5), PDFs and PPTX files (§11), galleries (§9), and books (§10) are the documents users carry. Every option is a `Lumen.Output.*` key or a saved preset read by its runner (§1 and every section after it). Reporting is the export summary and AI results warning (§13), the publish state counts (§3), and the print preview (§4). Background export, publish, upload, and burn jobs report through the Activity Manager of `D04 T11 §1` with a completion notification (§13, §3, §9). Read-only destinations, an original's own path, missing printers, missing mail clients, and failed FTP logins are refused by name (§1, §4, §12, §9). One Serilog Information line per export, print job, publish, upload, email, and generated document is the audit trail (§1 onward). Exchange is PDF, PPTX, HTML, JPEG, DNG, AVIF, JPEG XL, PSD, and template import and export (§2, §9, §11). A cancelled output leaves no partial file, republish replaces only published copies (§3), and nothing an output does touches an original.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Export extended: destinations, naming, formats, sizing, and color | D04 T02 §8, D04 T11 §2 |  [ ]   |
|   2   |   §13   | Export presets, metadata, watermarks, and post-processing | §1, D04 T11 §8 |  [ ]   |
|   3   |   §2    | Export formats and DNG output | §1, D04 T13 §6, D04 T13 §7 |  [ ]   |
|   4   |   §3    | Publish to local folders | §13 |  [ ]   |
|   5   |   §4    | Print I: the print module, page setup, and the print job | D04 T02 §8, D03 T18 §6 |  [ ]   |
|   6   |   §5    | Print II: packages, overlays, templates, and document printing | §4 |  [ ]   |
|   7   |   §6    | Contact sheets | §4, D03 T18 §7 |  [ ]   |
|   8   |   §7    | Slideshow I: templates, layout, overlays, and titles | D04 T11 §2 |  [ ]   |
|   9   |   §8    | Slideshow II: playback, music, transitions, and export | §7, D04 T04 §8 |  [ ]   |
|  10   |   §9    | Web galleries | D04 T11 §2 |  [ ]   |
|  11   |   §10   | Books | §4 |  [ ]   |
|  12   |   §11   | PDF and PowerPoint creation | §4 |  [ ]   |
|  13   |   §12   | Email and local sharing | §1 |  [ ]   |

---

## 1. Export Extended: Destinations, Naming, Formats, Sizing, and Color

The first export dialog of `D04 T02 §6` writes JPEG, TIFF, and PNG to one folder in three color spaces. Photographers need the destination, name, format, size, and color space the receiver asks for without a second tool. This section extends that dialog and its `ExportRunner` with Lightroom's and ACDSee's destination choices, the full rename template on the `D04 T11 §2` token engine, every `D04 T13 §6` writer with its option page, JPEG size limits, every sizing mode and resampling filter, and any ICC output space at 8, 16, or 32 bits. It must not add a second export runner, and it must refuse any destination that would overwrite an original. Catalog: LP-0849 to LP-0857 (9 features: export location options, export file naming, the JPEG size limit, output color space and bit depth, image sizing, the ACDSee destination choices, file format with settings, the ACDSee resize modes, and the resampling filters). -> SOURCE: parity-lumen-export-extended

**Fidelity:** Export dialog extended -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/lumen/export-extended/. **Corrected 2026-09-27:** cited docs/captures/lumen/export/ (baseline from `D04 T02 §6`) as the source; the captures under docs/captures/lumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can send a selection to exactly the folder, name, format, size, and color space the destination needs without a second tool. Consumer: the exported files and whoever receives them.
**Treatment:** Lightroom's collapsible sections (Export Location, File Naming, File Settings, Image Sizing) in the existing dialog, with a live example file name and an estimated output size. Cheaper substitute that fails the checkpoint: a fixed list of sizes and sRGB only.
**Chrome:** extend the `D04 T02 §6` dialog and `ExportRunner`; consume the `D04 T11 §2` token engine, the `D01 T03 §2` resamplers, the `D01 T04 §1` transforms, and the `D04 T13 §6` writers. Do not add a second export runner.

**Requires:** display-session -- the export dialog and its captures need an interactive desktop

**Freeze check:** Every export writes through `AtomicFileWriter` to a target that is never an original's path: a destination and name that resolve to any source photo's full path are refused by name before the job starts; a failed or cancelled export leaves any existing target byte-identical and no partial file; the unchanged-originals test of `D04 T02 §1` holds after a 50-photo export to "same folder as original". Fixture source: `tests/fixtures/lumen/export/` (created by this section).

- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Export/ExportDestination.cs` (LP-0849, LP-0854): specific folder, same folder as the original, choose folder later (asked when the job starts), Pictures, Desktop, or Documents through `Environment.GetFolderPath`, and an optional subfolder built from tokens. Done when: `ExportDestinationTests` resolve each kind for a fixture photo.
- [ ] Refuse, in `ExportDestination.Resolve`, any output path equal (case-insensitive, after `Path.GetFullPath`) to a source photo's path, naming the photo. Done when: `ExportDestinationTests` assert the refusal message and that no file was opened. Cheaper substitute: relying on the Overwrite choice, which would replace the original.
- [ ] Add the file naming page (LP-0850) on the `D04 T11 §2` template: custom text, start number, and extension case (lower, upper, as is), with the first three resulting names previewed, `Lumen.Output.Export.LastTemplate`, and a recent-templates list of ten. Done when: `ExportNamingTests` assert the template, start number, extension case, and collision handling with `D04 T02 §6`'s Overwrite, Skip, and Unique name.
- [ ] Add the File Settings format picker (LP-0855) listing every `D04 T13 §6` writer with its option page (quality, compression, bit depth, alpha, pixel format). Done when: a test asserts the picker lists exactly the registry's writable formats.
- [ ] Add the output color space and bit depth (LP-0852): sRGB, Display P3, Adobe RGB, ProPhoto RGB, Rec. 2020, or any installed ICC profile through `D01 T04 §1`; 8, 16, or 32-bit float where the format allows; the profile embedded. Done when: `ExportColorSpaceTests` read back the embedded ProPhoto and Rec. 2020 profiles through `D01 T04 §1`.
- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Export/JpegSizeLimiter.cs` (LP-0851): a binary search over quality in at most 8 encodes to the largest file under the limit; a limit unreachable at quality 0 is reported per photo, never silently exceeded. Done when: `JpegSizeLimitTests` land a 500 KB limit on the committed fixture under 500 KB within 8 encodes and report the unreachable case. Cheaper substitute: a quality slider.
- [ ] Add the Image Sizing model (LP-0853, LP-0856): long edge, short edge, width and height, dimensions (fit inside), megapixels, percentage, resolution in pixels per inch or centimeter, enlarge only, reduce only, or both, preserve aspect, and units in pixels, inches, or centimeters. Done when: `ExportSizingTests` resolve the output size for every mode on a 6000 by 4000 source.
- [ ] Add the resampling filter choice (LP-0857): bell, bicubic, box, B-spline, detail-preserving enlarge, Lanczos, Mitchell, and triangle from `D01 T03 §2`, defaulting to Lanczos for reduction and detail-preserving for enlargement. Done when: a test asserts the default per direction and that each filter name maps to a `D01 T03 §2` resampler.
- [ ] Show the estimated output size and example name live in the dialog, recomputed off the UI thread within 300 ms of a change. Done when: a driven change of quality updates the estimate (capture).
- [ ] Store every option under `Lumen.Output.Export.*` through the settings store and serialize the whole dialog into `D04 T02 §6`'s preset format with a `version` field so older presets load. Done when: `ExportPresetUpgradeTests` load a version 1 preset with the new fields at their defaults.
- [ ] Refuse a read-only destination folder by name before the job starts, the export's write permission policy. Done when: a test with a read-only temp folder asserts the message.
- [ ] Log one Serilog Information line per exported file (`Exported {Photo} to {Path} as {Format} {Width}x{Height} {Profile} {Bytes} bytes`), the export audit trail. Done when: a Serilog test logger asserts the line.
- [ ] Commit the export fixtures under `tests/fixtures/lumen/export/` with `reference.txt` naming the pipeline golden and its version. Done when: the fixture note exists.
- [ ] Add the fidelity test `ExportProPhotoTiffFidelityTests` (`[Trait("Category", "Fidelity")]`): a 16-bit ProPhoto TIFF export of the committed DNG matches the pipeline golden within 1/65535 after the stated resize. Done when: the test passes.
- [ ] Commit captures under `docs/captures/lumen/export-extended/` and update `docs/user/lumen/export.md` for every new option. Done when: every control appears in a capture and is documented with its default.
- [ ] Commit: `"lumen: export destinations, naming, formats, sizing, and color spaces"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ExportDestinationTests|FullyQualifiedName~ExportNamingTests|FullyQualifiedName~JpegSizeLimitTests|FullyQualifiedName~ExportColorSpaceTests|FullyQualifiedName~ExportSizingTests|FullyQualifiedName~ExportProPhotoTiffFidelityTests"` exits 0, with the original-path refusal asserted and the ProPhoto TIFF within 1/65535 of the golden; a driven export of 50 photos to "choose folder later" with a 500 KB limit is captured with its log lines quoted. Cheaper substitute that fails: a quality slider standing in for the size limit, which `JpegSizeLimitTests` catches.

## 2. Export Formats and DNG Output

A destination may want a modern, HDR, or archival format, or the untouched original with its metadata. This section adds flattened PSD and PSB, TIFF with transparency, AVIF and JPEG XL with quality, lossless, and HDR, DNG with Lightroom's options, rendered DNG with the edits baked in, HDR outputs with an SDR base and an ISO 21496-1 gain map, and "original plus sidecar", which copies the original's bytes and writes the metadata beside the copy. It adds no codec to `Photon.Lumen.Core`: every writer comes from `D04 T13 §6` and `D04 T13 §7`. Catalog: LP-0423, LP-0858 to LP-0863 (7 features: render to DNG with edits baked in, PSD and PSB, TIFF with transparency, DNG export options, AVIF and JPEG XL, original with updated XMP sidecar, and HDR output with gain maps). -> SOURCE: parity-lumen-export-formats

**Fidelity:** Export dialog format pages -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/lumen/export-extended/. **Corrected 2026-09-27:** cited docs/captures/lumen/export-extended/ as the source; the captures under docs/captures/lumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Slider/README.md, docs/design/components/RadioButton/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can export to the modern, HDR, or archival format a destination needs, or hand off the untouched original with its metadata. Consumer: the exported files and the applications that open them.
**Treatment:** new entries in §1's format picker with their option pages, and an HDR Output checkbox that enables the HDR spaces and the gain-map choice. Cheaper substitute that fails the checkpoint: an 8-bit SDR render saved under an HDR extension.
**Chrome:** consume the `D04 T13 §6` writers, the `D04 T13 §7` DNG writer, and the `D03 T17 §2` PSD writer through the registry. Do not add codecs in `Photon.Lumen.Core`.

**Requires:** display-session -- the format pages and captures need an interactive desktop

**Freeze check:** Render to DNG, original plus sidecar, and every format here write a new file through `AtomicFileWriter` and never to the source's path; "original plus sidecar" opens the original read-only, copies it to the destination, verifies the copy's SHA-256 against the source before recording success, and deletes a mismatched copy; the source's SHA-256 and last-write time are unchanged after each format. Fixture source: `tests/fixtures/lumen/export/`.

- [ ] Add PSD and PSB export (LP-0858): a flat composite with its profile and resolution through the `Photon.Core` PSD writer moved by `D03 T17 §2`, switching to PSB above 30,000 pixels a side. Done when: `ExportFormatMatrixTests` read back a PSD and a 31,000-pixel PSB with the right header versions.
- [ ] Add TIFF with transparency (LP-0859): an unassociated alpha channel (`ExtraSamples = 2`) for photos whose develop crop or AI removal produced transparent areas. Done when: the matrix test reads the alpha channel back equal within 1/65535.
- [ ] Add AVIF and JPEG XL option pages (LP-0861): quality, lossless, speed, and HDR (PQ or HLG at 10 or 12 bits) through the moved libavif (BSD-2-Clause) and libjxl (BSD-3-Clause) writers. Done when: the matrix test round-trips each option set within its stated tolerance.
- [ ] Add the HDR Output checkbox (LP-0863): Rec. 2020 PQ and HLG and Display P3 PQ spaces, and an SDR base JPEG or AVIF with an ISO 21496-1 gain map whose SDR rendition comes from `D01 T07 §1`'s tone map. Done when: `GainMapExportTests` decode the SDR base with a reader that ignores gain maps and read the gain map back.
- [ ] Add DNG export (LP-0860): compatibility level, JPEG preview size, fast load data, lossy compression, and embed original raw through `D04 T13 §7`. Done when: `dng_validate` (Adobe DNG SDK, version quoted, oracle only) reports no errors for each option combination.
- [ ] Add Render to DNG (LP-0423): a linear DNG with the develop edits baked in, written as a new file into the destination. Done when: `RenderedDngTests` assert the linear DNG's pixels equal the pipeline render within 1/65535 and `dng_validate` passes.
- [ ] Add Original plus sidecar (LP-0862): copy the original's bytes, verify the hash, and write the catalog metadata into `<copy>.xmp` beside the copy. Done when: `OriginalWithSidecarTests` assert the copy's hash equals the source's and the sidecar carries the catalog's title, rating, and keywords. Cheaper substitute: re-encoding the original, which the hash check catches.
- [ ] Disable format options a writer cannot honor (for example 32-bit float in JPEG) with a tooltip naming the format's limit. Done when: a test asserts the disabled state and tooltip text for JPEG at 32 bits.
- [ ] Add the fidelity test `LosslessModernExportFidelityTests` (`[Trait("Category", "Fidelity")]`): the committed DNG exported to AVIF lossless and JPEG XL lossless decodes equal to the 16-bit pipeline render within 1/65535. Done when: the test passes.
- [ ] Log one Serilog Information line per exported file naming the format options. Done when: a Serilog test logger asserts the line for an HDR AVIF.
- [ ] Commit captures of each new option page under `docs/captures/lumen/export-extended/` and document each format in `docs/user/lumen/export.md`. Done when: every option page is captured and documented.
- [ ] Commit: `"lumen: export to PSD, AVIF, JPEG XL, DNG, HDR with gain maps, and original plus sidecar"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ExportFormatMatrixTests|FullyQualifiedName~GainMapExportTests|FullyQualifiedName~OriginalWithSidecarTests|FullyQualifiedName~RenderedDngTests|FullyQualifiedName~LosslessModernExportFidelityTests"` exits 0, with the lossless AVIF and JPEG XL comparisons within 1/65535 and `dng_validate` output on the rendered DNG quoted. Cheaper substitute that fails: renaming a JPEG to `.avif`, which the matrix round trip catches.

## 3. Publish to Local Folders

A photographer keeps a folder (a digital frame, a phone sync folder, a NAS share) in step with a collection without re-exporting everything. This section adds Lightroom's Publish Services panel with one service kind, Hard Drive, over §1 and §13's export runner and presets and the collections of `D04 T01 §10`. It tracks each photo's publish state, republishes only what changed, and deletes only files it published itself. Flickr, Adobe, and other online services are excluded as cloud. Catalog: LP-0864 to LP-0865 (2 features: the Publish Services panel with a hard drive service, publish states, publish, republish, mark up to date, and remove on next publish; and Go to Published Folder with service settings import and export). -> SOURCE: parity-lumen-publish-local

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/publish/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Menu/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Button/README.md, docs/design/components/Toast/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can keep a folder in step with a collection without re-exporting everything. Consumer: the published folder and the device or share that reads it.
**Treatment:** a Publish Services panel in the left panel with published collections, smart and folder-set groups, a Publish button, and the grid split into New Photos to Publish, Modified Photos to Re-Publish, Published Photos, and Photos to Remove. Cheaper substitute that fails the checkpoint: an export preset run by hand each time.
**Chrome:** consume §1 and §13's export runner and presets, the collections of `D04 T01 §10`, and the Activity Manager of `D04 T11 §1`. Do not add a second export runner.

**Requires:** display-session -- the publish panel and captures need an interactive desktop

**Freeze check:** Publish writes new and changed copies through `AtomicFileWriter` into the service's destination only; it deletes only files whose path and SHA-256 match a row of the `published` table, and only to the Recycle Bin; a destination that contains a source photo's own path is refused by name; a file the user added to the destination is never touched. Fixture source: `tests/fixtures/lumen/publish/` (created by this section).

- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Publish/PublishService.cs` with one kind, Hard Drive (LP-0864): destination folder, an export preset from §13, and published collections (manual, smart, and folder sets). Done when: `PublishServiceTests` create, rename, and delete a service and its collections.
- [ ] Add a catalog migration creating the `published` table (photo, collection, output path, edit version hash, output SHA-256, published time), tested on a copy of the previous version's catalog. Done when: the migration test opens the previous fixture catalog and finds the table.
- [ ] Add `PublishStateResolver` comparing the current edit version hash with the published one into New, Modified, Published, and To Remove. Done when: `PublishStateTests` flip a photo to Modified after a develop change and list a removed photo under To Remove.
- [ ] Add `PublishRunner`: publish writes New and Modified photos through §1's runner, deletes To Remove copies to the Recycle Bin only when their hash matches the table, and runs on the Activity Manager with progress and Cancel. Done when: `PublishRunnerTests` assert republish replaces only the published copy and a user-added file in the folder is untouched. Cheaper substitute: re-exporting every photo, which the state tests catch.
- [ ] Add Mark as Up to Date, which updates the table without writing any file. Done when: a test asserts no file write and the state change.
- [ ] Add the Publish Services panel and the four-way grid split in `src/Lumen/Photon.Lumen.Desktop/Views/Output/Publish/`. Done when: a driven publish shows the counts per group (capture).
- [ ] Add Go to Published Folder (LP-0865), opening Explorer at the destination, and service settings import and export as `.lumenpublish` JSON. Done when: a test round-trips a service through `.lumenpublish`.
- [ ] Refuse an unreachable or read-only destination by name and keep the states unchanged. Done when: a test with a read-only folder asserts the message and that no state changed.
- [ ] Log one Serilog Information line per publish run with the new, modified, removed, and failed counts. Done when: a Serilog test logger asserts the line.
- [ ] Commit fixtures under `tests/fixtures/lumen/publish/` with `reference.txt`, captures under `docs/captures/lumen/publish/`, and `docs/user/lumen/publish.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: publish collections to local folders"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~PublishServiceTests|FullyQualifiedName~PublishStateTests|FullyQualifiedName~PublishRunnerTests"` exits 0; a driven publish, develop change, and republish is captured with the log lines quoted and a before-and-after listing of the destination showing only the changed copy rewritten. Cheaper substitute that fails: re-exporting every photo, which `PublishStateTests` catches.

## 4. Print I: The Print Module, Page Setup, and the Print Job

Photographers print, and Lumen cannot print today. This section builds a Print module on the suite print frame that `D03 T18 §6` moved to `src/Photon.UI/Print/` and `src/Photon.Core/Print/`, contributing Lumen's pages through its `IPrintPageSource` seam: single images and contact-sheet grids, page setup, the print job to a printer or a JPEG file, print sharpening, and Lumen-managed or printer-managed color with the `D01 T04` engine. Printing from browse and the viewer opens the same frame. It must not build a second print dialog. This promotes backlog B-035. Catalog: LP-0895 to LP-0906 (12 features: the Print module, single image and contact sheet grid layouts, the print job, print sharpening, print color management, page setup and Print One Copy, saved print collections and which photos print, print from browse and the viewer with live preview, printer options, ACDSee print color management, the viewer's print commands, and printing selected images as single pages). -> SOURCE: lumen-roadmap-print

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/print/.
**Design:** docs/design/shell-layout.md#lumen-darkroom-and-photo-manager, docs/design/components/Panel/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Slider/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Dialog/README.md, docs/design/components/Button/README.md, new surface: docs/design/components/LumenPrint/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can print what they see, sized and color managed for the paper, from the library or straight from the viewer. Consumer: the printer, or the JPEG file of print to file.
**Treatment:** Lightroom's Print module (template browser left, preview center, Layout Style, Image Settings, Layout, Guides, Page, and Print Job panels right) with Print and Print One Copy; the viewer's File, Print opens the same frame with the current photo. Cheaper substitute that fails the checkpoint: sending the screen preview to the default printer.
**Chrome:** contribute Lumen pages to the `Photon.UI/Print/` frame of `D03 T18 §6` through `IPrintPageSource`; consume `D01 T04 §1` and `D01 T04 §2`, `D04 T02 §6`'s output sharpening, and the develop pipeline. Do not build a second print dialog.

**Requires:** display-session -- the Print module and the Microsoft Print to PDF proof need an interactive desktop

**Freeze check:** Printing opens every source photo read-only; print to file writes a new JPEG through `AtomicFileWriter` to a chosen path that is refused by name when it equals a source photo's path; the unchanged-originals test holds after printing the fixture set to file. Fixture source: `tests/fixtures/lumen/print/` (created by this section).

- [ ] Write the design spec `docs/design/components/LumenPrint/README.md` and `preview.html` (the print module: the page preview, layout guides, cells, and the right-dock print panels; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Print/LumenPrintPageSource.cs` implementing `IPrintPageSource` (LP-0895), rendering each cell from the develop pipeline at print resolution, so the preview and the job read the same pixels. Done when: `LumenPrintPageSourceTests` assert the preview bitmap equals the job bitmap downscaled within 1/255.
- [ ] Add the Single Image and Contact Sheet grid layouts (LP-0896): units, margins, page grid rows and columns, cell spacing and size, keep square, rotate to fit, and zoom to fill. Done when: `LumenPrintLayoutTests` assert cell geometry for each layout and margin set on A4 and Letter.
- [ ] Add the Guides panel (LP-0896): rulers, bleed, margins and gutters, image cells, and dimensions, drawn in the preview only. Done when: a capture shows each guide and a test asserts guides are absent from the job bitmap.
- [ ] Add the Print Job panel (LP-0897): printer or JPEG file, draft mode (cached previews), print resolution, JPEG quality and custom file dimensions for print to file, and 16-bit output where the driver accepts it. Done when: `PrintToFileTests` assert a 300 ppi JPEG has the stated pixel size and embedded profile.
- [ ] Add print sharpening (LP-0898): matte or glossy at low, standard, or high, reusing `D04 T02 §6`'s output sharpening at print resolution. Done when: a test asserts the same kernel parameters as export at equal resolution.
- [ ] Add print color (LP-0899, LP-0904): managed by printer or by Lumen with a printer profile, rendering intent, and black point compensation through `D01 T04 §2`, and print adjustment brightness and contrast applied to the print only. Done when: `PrintColorTransformTests` map known patches within delta E 1 of the `D01 T04` reference and assert the adjustment leaves the preview unchanged.
- [ ] Add soft proof and the gamut warning in the preview through `D01 T04 §2`, sharing the proof transform of `D04 T09 §15`. Done when: a capture shows the gamut overlay for the committed saturated fixture.
- [ ] Add Page Setup, Printer, Print, and Print One Copy (LP-0900, LP-0903): printer, paper, orientation, copies, page range, and resolution from the frame's printer pages. Done when: a driven Print One Copy to Microsoft Print to PDF writes one page.
- [ ] Add which photos print (LP-0901): all filmstrip photos, selected, or flagged, with page navigation, and Save as Print Collection through `D04 T01 §10`. Done when: a test asserts the page count for each choice and a saved print collection restores its layout.
- [ ] Add print from browse and the viewer (LP-0902, LP-0905, LP-0906): print all or selected images as single pages with the live preview, direct print with the current settings (Ctrl+Shift+P), and the Quick View print with captions and headers. Done when: a driven print from the viewer opens the frame with the current photo (capture).
- [ ] Refuse a missing or offline printer by name and keep the job settings. Done when: a test with a fake backend asserts the message.
- [ ] Store the module's state under `Lumen.Output.Print.*`. Done when: a restart restores the layout, printer, and color settings (test).
- [ ] Log one Serilog Information line per print job (printer or file, pages, copies, profile, intent). Done when: a Serilog test logger asserts the line.
- [ ] Run the proof through Microsoft Print to PDF and read the PDF back with PdfPig. Done when: the page size and placed image size match the layout within 0.5 mm (output quoted).
- [ ] Commit fixtures under `tests/fixtures/lumen/print/` with `reference.txt`, captures of each layout under `docs/captures/lumen/print/`, and `docs/user/lumen/print.md`. Done when: every panel is captured and documented.
- [ ] Commit: `"lumen: the print module with managed color, sharpening, and print to file"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~LumenPrintPageSourceTests|FullyQualifiedName~LumenPrintLayoutTests|FullyQualifiedName~PrintColorTransformTests|FullyQualifiedName~PrintToFileTests"` exits 0; the Microsoft Print to PDF read-back with PdfPig is quoted with page and image sizes within 0.5 mm. Cheaper substitute that fails: printing the screen preview, which the print-resolution pixel size test catches.

## 5. Print II: Packages, Overlays, Templates, and Document Printing

A photographer prints several sizes on one sheet, reuses layouts, and prints with captions as IrfanView and ACDSee users expect. This section adds Picture Package and Custom Package layouts, the print template browser, page overlays, captions, headers, and footers with tokens, IrfanView's size modes and print dialog details, resampling and printer adjustments, print profiles, multipage and selection printing, and printing PDF pages, all on §4's page source and frame. Catalog: LP-0907 to LP-0921, LP-0948 (16 features: the template browser, picture and custom packages, page overlays, ACDSee print layouts, print resampling filters, print gamma and printer adjustments, EXIF print information, custom print formats, captions and headers and footers, the IrfanView print dialog, print size modes, print profiles, header and footer placeholders, multipage printing, printing the current selection, and printing PDF and Office documents). -> SOURCE: parity-lumen-print-packages

**Fidelity:** Print module packages and templates -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/lumen/print/. **Corrected 2026-09-27:** cited docs/captures/lumen/print/ as the source; the captures under docs/captures/lumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, new surface: docs/design/components/LumenPrint/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can print a package of sizes on one sheet, reuse layouts, and print with captions. Consumer: the printer, or the JPEG file of print to file.
**Treatment:** Picture Package and Custom Package layout styles with rulers, grid snap, draggable cells, and Auto Layout; a Template Browser with user folders; Page panel overlays; an IrfanView-style Print Setup page with size modes. Cheaper substitute that fails the checkpoint: fixed layouts with no saved templates.
**Chrome:** consume §4's page source and frame, the `D04 T11 §2` token engine, the `D04 T11 §8` watermark engine, the identity plate of `D04 T14 §1`, and the `D04 T13 §4` PDF reader. Do not add a second layout engine.

**Requires:** display-session -- the package editor and captures need an interactive desktop

- [ ] Write or extend the design spec `docs/design/components/LumenPrint/README.md` and `preview.html` with the packages, the template browser, the page overlays, and the captions (anatomy, every state, tokens, sizes; `D04 T12 §4` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Add Picture Package and Custom Package layouts (LP-0908, LP-0910) in `src/Lumen/Photon.Lumen.Core/Output/Print/PackageLayout.cs`: standard cell sizes, rulers, grid snap, draggable cells, Auto Layout, new page, full page, predefined multi-image layouts, and prints per photo. Done when: `PicturePackageLayoutTests` place a 1 of 5x7 and 4 of wallet package on Letter with the stated cell sizes.
- [ ] Add the Template Browser (LP-0907): built-in and user templates as `.lumenprint` JSON in folders, with save, update, import, and export. Done when: `PrintTemplateStoreTests` round-trip a template and load an older version.
- [ ] Add page overlays (LP-0909): background color, identity plate, watermark, page numbers, page info, crop marks, and photo info captions. Done when: `PrintOverlayTests` find each overlay in the preview bitmap at its anchor.
- [ ] Add captions, headers, and footers (LP-0915, LP-0919) with fonts, alignment, line limits, and `D04 T11 §2` tokens, IrfanView's placeholders accepted through the token engine's `$` alias. Done when: `PrintOverlayTests` render a `{Filename}` caption and `$N` header as the expected text.
- [ ] Add the size modes and custom formats (LP-0914, LP-0917): original DPI, best fit, fill paper, stretch, custom size and margins, scale, center, position including negative offsets, number of prints, auto rotate, crop or shrink to fit, borderless where the driver allows, and no overflow. Done when: `PrintSizeModeTests` assert each mode's placed size on A4 and Letter.
- [ ] Add the IrfanView print dialog details (LP-0916): default printer, driver values remembered per printer (the DEVMODE saved under `Lumen.Output.Print.Drivers`), color or black-and-white preview, and orientation auto rotate. Done when: a test restores a saved DEVMODE for a fake printer.
- [ ] Add the print resampling filter choice (LP-0911) from `D01 T03 §2`. Done when: a test asserts each filter name maps to a resampler.
- [ ] Add print gamma and printer exposure, contrast, and sharpness (LP-0912), applied to the print only. Done when: a test asserts the preview is unchanged and the job bitmap changes.
- [ ] Write the Exif Print tags (LP-0913) into print-to-file JPEGs for printers that read them. Done when: exiftool 13 reads the tags from a print-to-file output (quoted).
- [ ] Add print profiles (LP-0918): save the whole print setup without printing and load it by name. Done when: a test round-trips a profile.
- [ ] Add multipage printing (LP-0920): page ranges, odd or even, reverse, all pages, copies, and collate. Done when: a test asserts the page order for odd pages reversed with two collated copies.
- [ ] Add print only the viewer's selection (LP-0921) from `D04 T04 §11`. Done when: a driven print of a viewer selection prints only that rectangle (PDF read-back quoted).
- [ ] Add document printing (LP-0948): PDF pages through the `D04 T13 §4` reader with page ranges, pages per sheet, duplex, and collation; Office documents handed to their associated application's `print` verb; a mixed selection prints images and documents in selection order. Done when: `DocumentPrintTests` select pages 2 to 4 of the committed PDF and assert three placed pages.
- [ ] Log one Serilog Information line per package and document print job. Done when: a Serilog test logger asserts the line.
- [ ] Commit captures of the package editor, template browser, and Print Setup page under `docs/captures/lumen/print/` and extend `docs/user/lumen/print.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: print packages, templates, overlays, and document printing"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~PicturePackageLayoutTests|FullyQualifiedName~PrintTemplateStoreTests|FullyQualifiedName~PrintSizeModeTests|FullyQualifiedName~PrintOverlayTests|FullyQualifiedName~DocumentPrintTests"` exits 0; a package printed through Microsoft Print to PDF reads back with PdfPig showing each cell size within 0.5 mm (quoted). Cheaper substitute that fails: a single fixed package layout, which `PicturePackageLayoutTests` catches.

## 6. Contact Sheets

A photographer makes an index print or an image map of a shoot in one dialog. Imago already builds contact sheets (`D03 T18 §7`); Lumen is the second consumer, so this section moves that engine to `src/Photon.Core/Print/ContactSheets/` first and builds ACDSee's and IrfanView's Contact Sheet dialog on it, with image, PDF, HTML image map, and print outputs. It must not leave a second contact-sheet builder anywhere in `src/`. Catalog: LP-0922 to LP-0925 (4 features: contact sheets as image files or HTML image maps, the print contact sheet format, contact sheets from a selection, and contact sheet output). -> SOURCE: parity-lumen-contact-sheets

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/contact-sheet/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/TextBox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Button/README.md, docs/design/components/ListTree/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can make an index print or an image map of a shoot in one dialog. Consumer: the sheet files, the printer, or the browser that opens the image map.
**Treatment:** a Contact Sheet dialog (Layout, Text, and Output tabs) with a live preview, reachable from Create, browse, and the Print module's contact sheet layout. Cheaper substitute that fails the checkpoint: a screenshot of the grid.
**Chrome:** consume the moved contact-sheet engine, §4's page source for printing, the `D03 T17 §7` PDF writer, and the `D04 T11 §2` token engine. Do not write a second contact-sheet builder.

**Requires:** display-session -- the dialog and captures need an interactive desktop

- [ ] Move first: the contact-sheet builder, layout, and caption model of `D03 T18 §7` from Imago to `src/Photon.Core/Print/ContactSheets/`, repointing Imago's File, Automate, Contact Sheet. Done when: `grep -rn "class ContactSheet" src` prints paths only under `src/Photon.Core/`, and Imago's contact-sheet golden test still passes.
- [ ] Add the layout model (LP-0924): columns and rows, cell size and spacing, paper size, stretch small images, and background color or image. Done when: `ContactSheetLayoutTests` place 20 cells of a 4 by 5 sheet on A4 with the stated spacing.
- [ ] Add appearance (LP-0922, LP-0923): frames, thumbnail effects (shadow, border), page background, and presets. Done when: a test renders a framed cell with a shadow into the preview bitmap.
- [ ] Add header, footer, and captions with `D04 T11 §2` tokens and IrfanView's placeholders through the `$` alias (LP-0924). Done when: a test renders a caption `{Filename} {Date}` as the expected text.
- [ ] Add image file output (LP-0922, LP-0925): a name pattern and destination, one file per sheet through `AtomicFileWriter`. Done when: a test writes three sheets named by the pattern.
- [ ] Add PDF output through the suite PDF writer. Done when: PdfPig reads one image per cell from the PDF of the fixture folder.
- [ ] Add HTML image map output (LP-0922): a page per sheet with `<map>` areas linking each cell to its image. Done when: `ContactSheetHtmlMapTests` assert each area covers its cell and the page validates in the W3C Nu HTML Checker (version quoted).
- [ ] Add print output through §4 and show-in-viewer output (LP-0925). Done when: a driven print of a sheet goes through the §4 frame (capture).
- [ ] Add saved profiles and one sheet from the selected thumbnails (LP-0925). Done when: a test round-trips a profile and builds a sheet from three selected photos.
- [ ] Add the Contact Sheet dialog in `src/Lumen/Photon.Lumen.Desktop/Views/Output/ContactSheet/` with the live preview. Done when: a driven change of columns updates the preview (capture).
- [ ] Add the fidelity test `ContactSheetGoldenTests` (`[Trait("Category", "Fidelity")]`): a sheet of the committed fixture folder matches its golden image within 1/255. Done when: the test passes.
- [ ] Log one Serilog Information line per generated sheet set. Done when: a Serilog test logger asserts the line.
- [ ] Commit captures under `docs/captures/lumen/contact-sheet/` and `docs/user/lumen/contact-sheets.md`. Done when: every tab is captured and documented.
- [ ] Commit: `"lumen: contact sheets on the shared engine"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ContactSheet"` exits 0 with the golden comparison within 1/255, the PdfPig read-back showing one image per cell, and the HTML validator output quoted. Cheaper substitute that fails: a second contact-sheet builder in Lumen, which the move grep catches.

## 7. Slideshow I: Templates, Layout, Overlays, and Titles

A photographer designs a good-looking show from a collection without leaving Lumen. This section builds the Slideshow module's authoring half: a `SlideshowDocument`, a template browser, slide layout, overlays with tokens, backdrops, and intro and ending title screens, rendered through the develop pipeline so the editor preview and the played slide are the same pixels. Playback, music, and export are §8. Catalog: LP-0926 to LP-0932 (7 features: the Slideshow module, the template browser, slide options and layout, overlays, backdrop, intro and ending title screens, and header and footer captions). -> SOURCE: parity-lumen-slideshow-authoring

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/slideshow/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Swatches/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/TextBox/README.md, new surface: docs/design/components/LumenSlideshow/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can design a good-looking show from a collection without leaving Lumen. Consumer: §8's player and exporters.
**Treatment:** Lightroom's Slideshow module (Template Browser and preview left, slide editor center, Options, Layout, Overlays, Backdrop, Titles, and Playback panels right) with an on-slide text tool. Cheaper substitute that fails the checkpoint: a fixed black background with centered photos.
**Chrome:** consume the develop pipeline for slide renders, the `D04 T11 §2` token engine, the `D04 T11 §8` watermarks, the identity plate of `D04 T14 §1`, and the suite text engine of `D03 T16 §1`. Do not add a second text renderer.

**Requires:** display-session -- the module and captures need an interactive desktop

- [ ] Write the design spec `docs/design/components/LumenSlideshow/README.md` and `preview.html` (the slideshow module: the slide preview, overlays, backdrop, and title screens; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Slideshow/SlideshowDocument.cs` (LP-0926): template, photo source, layout, overlays, backdrop, titles, and playback settings, versioned JSON, saved as a slideshow collection through `D04 T01 §10`. Done when: `SlideshowDocumentTests` round-trip a document and load an older version.
- [ ] Add `SlideRenderer` producing a slide bitmap from the document and a photo through the develop pipeline. Done when: `SlideRenderTests` render a slide with border, shadow, and overlays equal to its golden within 1/255.
- [ ] Add the Template Browser (LP-0927): built-in and user templates as `.lumenslides` JSON, folders, preview on hover, save, import, and export. Done when: `SlideshowTemplateStoreTests` round-trip a template.
- [ ] Add slide options and layout (LP-0928): zoom to fill, stroke border with color and width, cast shadow with opacity, offset, radius, and angle, margins with linked guides, and aspect preview for screen, 16:9, and 4:3. Done when: a test asserts the photo rectangle for each aspect and margin set.
- [ ] Add the overlays (LP-0929): identity plate, watermark, rating stars, and text overlays with shadow placed by the on-slide text tool with `D04 T11 §2` tokens. Done when: `SlideRenderTests` find a `{Title}` overlay rendered with the photo's title.
- [ ] Add header and footer captions (LP-0932) with alignment, background, font, and metadata tokens. Done when: a test renders both captions at their anchors.
- [ ] Add the backdrop (LP-0930): color wash with angle and opacity, background image, and background color. Done when: a golden slide with a color wash matches within 1/255.
- [ ] Add intro and ending title screens (LP-0931) with color and identity plate. Done when: a test asserts the title slides are first and last in the rendered sequence.
- [ ] Add the Slideshow module view in `src/Lumen/Photon.Lumen.Desktop/Views/Output/Slideshow/` with the editor, panels, and filmstrip. Done when: a driven edit of a text overlay shows in the preview (capture). Cheaper substitute: overlays drawn only in the preview, which the golden slide render catches.
- [ ] Store the module's last-used template and options under `Lumen.Output.Slideshow.*`. Done when: a restart restores them (test).
- [ ] Log one Serilog Information line per saved slideshow or template. Done when: a Serilog test logger asserts the line.
- [ ] Commit captures of each panel under `docs/captures/lumen/slideshow/` and `docs/user/lumen/slideshow.md` for authoring. Done when: every panel is captured and documented.
- [ ] Commit: `"lumen: the slideshow module with templates, layout, overlays, and titles"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~SlideshowDocumentTests|FullyQualifiedName~SlideRenderTests|FullyQualifiedName~SlideshowTemplateStoreTests"` exits 0 with every golden slide within 1/255; captures of the editor are committed. Cheaper substitute that fails: overlays drawn only in the preview, which the golden slide render catches.

## 8. Slideshow II: Playback, Music, Transitions, and Export

A photographer plays a show to music on any screen and hands it to others as a PDF or images. This section adds the full-screen player (impromptu or configured, from the module, a selection, a folder, or a folder with subfolders), manual or timed advance, fades, transitions, pan and zoom and multi-up variations, display effects, music from tracks or folders fitted to the show, per-image project content, and export to PDF with page transitions and to JPEG slides. Audio plays through Windows Media Foundation over Vortice.MediaFoundation (part of Vortice.Windows, MIT, approved by the operator 2026-09-27), reusing the `SlideshowAudioPlayer` the viewer's quick slideshow builds (`D04 T04 §8`); NAudio was not approved for Lumen. Video clips and video export are `D04 T16 §6`; EXE and screen-saver output are backlog B-049. Catalog: LP-0301, LP-0933 to LP-0944 (13 features: the impromptu slideshow of the selection, slideshow sources and saved collections, music with fit to music, playback options, PDF and JPEG export, the ACDSee sources and Configure dialog, transitions, variations, display effects, background and duration options, music from folders, save settings as default, and project content). -> SOURCE: parity-lumen-slideshow-playback

**Fidelity:** Slideshow player -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/lumen/slideshow-player/. **Corrected 2026-09-27:** cited docs/captures/lumen/slideshow/ as the source; the captures under docs/captures/lumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Button/README.md, new surface: docs/design/components/LumenSlideshow/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can play a show to music on any screen and hand it to others as a PDF or images. Consumer: the viewer of the show, and the PDF and JPEG files.
**Treatment:** Lightroom's Playback panel and Play button, ACDSee's Configure Slideshow dialog (Basic, Advanced, Text, and Audio tabs), a full-screen player with autohiding controls, and Export PDF Slideshow and Export JPEG Slideshow. Cheaper substitute that fails the checkpoint: a timer that swaps photos with no transition or music.
**Chrome:** consume §7's document and renderer, the develop pipeline, `D04 T04 §8`'s `SlideshowAudioPlayer` (Media Foundation through Vortice.MediaFoundation) for audio, and the suite PDF writer of `D03 T17 §7`. Do not add a second slide renderer.

**Requires:** display-session -- full-screen playback and audio need an interactive desktop

- [ ] Write or extend the design spec `docs/design/components/LumenSlideshow/README.md` and `preview.html` with the player and the Configure dialog (anatomy, every state, tokens, sizes; `D04 T12 §7` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Add the photo sources (LP-0301, LP-0933, LP-0937): impromptu slideshow of the selection (Ctrl+Enter), saved slideshow collections, all filmstrip, selected, or flagged photos, a folder, or a folder with subfolders, with remembered contents. Done when: `SlideshowSourceTests` assert the photo list for each source.
- [ ] Add `src/Lumen/Photon.Lumen.Desktop/Views/Output/Slideshow/SlideshowPlayer.xaml` rendering two slides ahead on a background thread, with a choice of screen and quality (LP-0935). Done when: a driven 100-slide show at 2 seconds per slide drops no slide (log of render times quoted).
- [ ] Add the playback options (LP-0935, LP-0941): manual or auto advance, slide and fade durations, fade color, random, repeat, stretch small images, background color, preview in the module, and autohiding controls. Done when: `SlideshowTimingTests` assert the schedule for auto advance with fades.
- [ ] Add the transitions (LP-0938): crossfade, slide, wipe, zoom, and random, previewed in the Configure dialog. Done when: a test renders the midpoint frame of each transition equal to its golden within 1/255.
- [ ] Add the variations (LP-0939): pan and zoom with a strength, 2-up, 4-up, and collage. Done when: a test asserts the cell count and placement of each multi-up variation.
- [ ] Add the display effects (LP-0940): black and white, sepia, vivid, and soft through the develop pipeline. Done when: a test asserts each effect changes the slide as its develop preset does.
- [ ] Add music (LP-0934, LP-0942): `D04 T04 §8`'s `SlideshowAudioPlayer` (Windows Media Foundation through Vortice.MediaFoundation, no second audio stack) plays MP3, AAC, and WAV from chosen tracks or folders, with a fade out at the end. Done when: a test with a fake audio engine asserts track order and the final fade, and `grep -rn "NAudio" src` prints nothing.
- [ ] Add Fit to Music: slide durations computed from the tracks' total length. Done when: `SlideshowTimingTests` assert fit to music over two tracks sums to their length within one frame.
- [ ] Add the project content (LP-0944): per-image transitions, durations, captions, order, hidden controls, background audio, transition quality, and output size saved in the `SlideshowDocument`, and Save Settings as Default (LP-0943). Done when: a test round-trips per-image overrides and the saved default applies to a new show.
- [ ] Add Export PDF Slideshow (LP-0936) through the suite PDF writer with page transitions (`/Trans`, `/Dur`) and full-screen page mode, written through `AtomicFileWriter`. Done when: `SlideshowPdfExportTests` read the page count and `/Trans` entries with PdfPig.
- [ ] Add Export JPEG Slideshow (LP-0936): one JPEG per slide at a chosen size with the overlays rendered. Done when: `SlideshowJpegExportTests` assert the slide count and pixel size.
- [ ] Say in the player's context menu that video clips are skipped until `D04 T16 §6`, and skip them with one Warning log line per clip. Done when: a test with a video file in the source asserts the skip and the line.
- [ ] Log one Serilog Information line per playback start and per export. Done when: a Serilog test logger asserts both lines.
- [ ] Commit captures of the player and Configure dialog under `docs/captures/lumen/slideshow-player/` and extend `docs/user/lumen/slideshow.md` with playback, music, and export. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: slideshow playback, music, transitions, and PDF and JPEG export"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~SlideshowSourceTests|FullyQualifiedName~SlideshowTimingTests|FullyQualifiedName~SlideshowPdfExportTests|FullyQualifiedName~SlideshowJpegExportTests"` exits 0 with the PdfPig read-back of the `/Trans` entries quoted; a driven playback with music is captured with its log line. Cheaper substitute that fails: exporting a PDF of plain pages, which the `/Trans` read-back catches.

## 9. Web Galleries

A photographer publishes a gallery to their own site with no service account. This section moves Imago's FluentFTP client wrapper (`D03 T17 §12`) to `src/Photon.Core/Net/Ftp/` first, then builds a Web module and the ACDSee HTML album and IrfanView HTML export paths on own HTML, CSS, and JavaScript templates (licensed MIT inside every generated asset, so a user's site inherits no GPL obligation), with preview in the browser, export to a folder, and upload over FTP or FTPS through FluentFTP (MIT, approved by the operator 2026-09-27). SFTP is backlog B-053 because the operator did not approve SSH.NET for Lumen on 2026-09-27; export to a local folder stays. Online gallery services are excluded as cloud. Catalog: LP-0866, LP-0949 to LP-0957 (10 features: FTP transfer of selected files, the Web module, templates and layout styles, site info and appearance with click-to-edit, output settings, upload to the user's own server, preview and export, the HTML album wizard, IrfanView's HTML export, and IrfanView's template placeholders). -> SOURCE: parity-lumen-web-galleries

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/web/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Dialog/README.md, docs/design/components/Button/README.md, docs/design/components/Progress/README.md, docs/design/components/Toast/README.md, new surface: docs/design/components/LumenWebGallery/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can publish a gallery to their own site with no service account. Consumer: the browsers that open the gallery, and the user's server.
**Treatment:** Lightroom's Web module (Layout Style, Site Info, Color Palette, Appearance, Image Info, Output Settings, and Upload Settings panels) with a click-to-edit live preview, plus ACDSee's HTML Album wizard reachable from Create. Cheaper substitute that fails the checkpoint: a folder of JPEGs with an index listing file names.
**Chrome:** consume the develop pipeline and §1's export runner, the `D04 T11 §2` token engine, the `D04 T11 §8` watermarks, the identity plate of `D04 T14 §1`, and the moved FluentFTP wrapper. Do not add a second FTP client or an SSH library.

**Requires:** display-session -- the Web module, browser preview, and captures need an interactive desktop

**Freeze check:** Export to folder builds the gallery in a staging folder beside the target and renames it into place, so a cancelled or failed export leaves any existing gallery byte-identical; upload writes only under the configured remote folder; source photos are opened read-only. Fixture source: `tests/fixtures/lumen/web/` (created by this section).

- [ ] Write the design spec `docs/design/components/LumenWebGallery/README.md` and `preview.html` (the web gallery module: the live preview with click-to-edit text and the site, look, output, and upload panels; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Move first: the FluentFTP (MIT) client wrapper of `D03 T17 §12` from Imago to `src/Photon.Core/Net/Ftp/`, repointing Imago's URL opener. Done when: `grep -rn "FluentFTP" src --include=*.cs` finds the wrapper only under `src/Photon.Core/Net/Ftp/` and Imago's FTP open test passes.
- [ ] Add own templates (LP-0949, LP-0950) in `src/Lumen/Photon.Lumen.Core/Output/Web/Templates/` (grid, track, square, album) with an MIT license header inside every generated HTML, CSS, and JavaScript asset, recorded in `docs/dev/decisions.md`. Done when: a test asserts every generated asset starts with the MIT header.
- [ ] Add user templates (LP-0950): save, update, import, and export as `.lumenweb` packages. Done when: a test round-trips a user template.
- [ ] Add site and look settings (LP-0951): site title, collection title and description, contact and link, color palette, cell sizes, rows and columns, borders, and image info captions from tokens. Done when: `WebGalleryGeneratorTests` find each setting in the generated pages.
- [ ] Add click-to-edit text in the live preview (LP-0951), writing back to the gallery settings. Done when: a driven edit of the site title in the preview updates the setting (capture).
- [ ] Add output settings (LP-0952): JPEG quality, metadata choice through §13's filters, watermark, sharpening, and optional HDR AVIF images with JPEG fallbacks in `<picture>`. Done when: a test asserts the `<picture>` element lists the AVIF source before the JPEG.
- [ ] Add preview in the default browser from a temp folder with reload (LP-0954). Done when: a driven preview opens the browser on the temp index page.
- [ ] Add export to a folder through staging then rename (LP-0954), with advanced settings, web collections saved through `D04 T01 §10`, and which photos. Done when: a test cancels an export midway and asserts the previous gallery is byte-identical.
- [ ] Map the ACDSee HTML album wizard (LP-0955) onto the same templates, reachable from Create. Done when: a driven wizard run produces the same pages as the module with the same settings.
- [ ] Accept IrfanView's HTML export options and template placeholders (LP-0956, LP-0957) through the token engine's `$` alias: title, background, image and thumbnail links, previous, next, back, and self links, name parts, size, text, alignment, and targets. Done when: `WebTemplateTokenTests` render every IrfanView placeholder to its expected value.
- [ ] Add upload (LP-0953): FTP and FTPS (explicit and implicit TLS, the server certificate checked against the Windows store with a named refusal) with server presets, remote subfolder, the password stored with DPAPI (`ProtectedData`, current user), and progress on the Activity Manager; the protocol list offers no SFTP entry (backlog B-053). Done when: `GalleryUploadTests` upload to a local test FTP server with and without TLS and list the expected remote files.
- [ ] Add a plain FTP transfer of the selected files (LP-0866) over the same client. Done when: a test uploads three selected photos' exports to the test server.
- [ ] Refuse a failed login or unreachable server by name without retrying silently. Done when: a test with a wrong password asserts the message.
- [ ] Log one Serilog Information line per gallery export and upload (pages, images, bytes, server without the password). Done when: a Serilog test logger asserts the line and that no password appears.
- [ ] Commit fixtures under `tests/fixtures/lumen/web/` with `reference.txt`, captures under `docs/captures/lumen/web/`, and `docs/user/lumen/web-galleries.md`. Done when: every panel is captured and documented.
- [ ] Commit: `"lumen: web galleries from own templates with FTP and FTPS upload"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~WebGalleryGeneratorTests|FullyQualifiedName~WebTemplateTokenTests|FullyQualifiedName~GalleryUploadTests"` exits 0; every generated page of each template validates with zero errors in the W3C Nu HTML Checker (version quoted) and every link resolves; a driven export and upload to a local FTP server is captured. Cheaper substitute that fails: an index page of file names, which the template tests catch.

## 10. Books

A photographer lays out a book of a trip and gets a print-ready PDF. This section builds a Book module: a `BookDocument` with size, cover, pages, cells, text frames, and backgrounds, auto layout with presets, page templates and custom layouts, page numbers and captions, guides and cell zoom, text from metadata with type styles, and export to PDF with embedded fonts or to JPEG pages. Blurb upload is excluded as cloud. Catalog: LP-0958 to LP-0966 (9 features: the Book module, book settings, auto layout, pages and layouts, page numbers and captions, guides and cells, text, backgrounds, and views with export and preferences). -> SOURCE: parity-lumen-books

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/book/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/TextBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md, docs/design/components/Swatches/README.md, new surface: docs/design/components/LumenBook/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can lay out a book of a trip and get a print-ready PDF. Consumer: the PDF or JPEG pages and the print service the user sends them to.
**Treatment:** Lightroom's Book module (Book Settings, Auto Layout, Page, Guides, Cell, Text, Type, and Background panels) with multi-page, spread, and single-page views. Cheaper substitute that fails the checkpoint: one photo per page with no text.
**Chrome:** consume §4's color path, the suite PDF writer of `D03 T17 §7` with embedded fonts, the suite text engine of `D03 T16 §1`, and the develop pipeline. Do not rasterize text into page images.

**Requires:** display-session -- the Book module and captures need an interactive desktop

- [ ] Write the design spec `docs/design/components/LumenBook/README.md` and `preview.html` (the book module: page and spread views, cells, guides, page text, and backgrounds; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Books/BookDocument.cs` (LP-0958): size, cover, pages with layouts and cells, text frames, and backgrounds, versioned JSON saved as a book collection (LP-0966). Done when: `BookDocumentTests` round-trip a 20-page book.
- [ ] Add book settings (LP-0959): PDF or JPEG output, page sizes (square, portrait, landscape), JPEG quality, color profile, resolution, sharpening, and media type. Done when: a test asserts each setting reaches the exporter.
- [ ] Add auto layout (LP-0960) with presets (one photo per page, left blank right photo, with captions) and Clear Layout. Done when: `BookLayoutTests` auto-lay 40 photos with a preset to the expected page count.
- [ ] Add page templates and page editing (LP-0961): add, remove, duplicate, custom layouts, and copy and paste layout. Done when: a test pastes a layout onto three pages and asserts their cells.
- [ ] Add page numbers and page captions (LP-0962). Done when: a test renders page numbers at the chosen corner on every page but the cover.
- [ ] Add guides, cells, padding, and photo zoom and pan in cells (LP-0963). Done when: a test asserts the photo crop inside a cell after a zoom.
- [ ] Add text (LP-0964): photo and page text from metadata tokens, type settings and style presets, targeted type adjustment, and caption refresh when metadata changes. Done when: `BookCaptionRefreshTests` change a title in the catalog and assert the caption updates.
- [ ] Add backgrounds per page or global (LP-0965): color, graphic, or photo with opacity. Done when: a golden page with a photo background matches within 1/255.
- [ ] Add the views (LP-0966): multi-page, spread, and single page, and book preferences (default fill, text safe area). Done when: a driven switch through the three views is captured.
- [ ] Add export to PDF with fonts embedded and to JPEG pages, written through `AtomicFileWriter`. Done when: `BookPdfExportTests` read page size, image placement within 0.5 mm, and embedded fonts with PdfPig, and qpdf `--check` passes (version quoted).
- [ ] Log one Serilog Information line per book export. Done when: a Serilog test logger asserts the line.
- [ ] Commit captures under `docs/captures/lumen/book/` and `docs/user/lumen/books.md`. Done when: every panel is captured and documented.
- [ ] Commit: `"lumen: the book module with PDF and JPEG export"`

**Test checkpoint:** Format fidelity proof and unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~BookDocumentTests|FullyQualifiedName~BookLayoutTests|FullyQualifiedName~BookPdfExportTests|FullyQualifiedName~BookCaptionRefreshTests"` exits 0; the book PDF of the fixture reads back with PdfPig as stated and passes qpdf `--check` (version quoted). Cheaper substitute that fails: rasterizing text into page images, which the embedded-font check catches.

## 11. PDF and PowerPoint Creation

A user hands a set of photos to someone as one PDF or a PowerPoint deck, without Office. This section adds a Create menu with ACDSee-style wizards for slideshow PDFs, one PDF for all images or one per image, multi-page TIFF or PDF from a selection, IrfanView's Save as PDF with document properties, compression, and security, and PowerPoint presentations written with DocumentFormat.OpenXml (MIT), new or appended. Catalog: LP-0967 to LP-0970, LP-0979 (5 features: the Create menu, Create PDF, Create PowerPoint, multi-page TIFF or PDF from a selection, and Save as PDF with properties, compression, and security). -> SOURCE: parity-lumen-create-documents

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/create/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can hand a set of photos to someone as one PDF or a PowerPoint deck. Consumer: the PDF and PPTX files and the applications that open them.
**Treatment:** a Create menu (Slideshow, PDF, PowerPoint, Album, Archive) opening ACDSee-style wizards with a preview and an output page. Cheaper substitute that fails the checkpoint: a PDF with one uncompressed full-size image per page and no options.
**Chrome:** consume the suite PDF writer of `D03 T17 §7` and Imago's PDF presentation builder of `D03 T18 §7`, DocumentFormat.OpenXml for PPTX, the `D04 T13 §6` multi-page TIFF writer, and the `D04 T11 §2` token engine. Do not add a second PDF writer.

**Requires:** display-session -- the wizards and captures need an interactive desktop

**Freeze check:** Every PDF, TIFF, and PPTX is written through `AtomicFileWriter`; "append to an existing presentation" writes the combined deck to a temp file beside the target and replaces it atomically only after the Open XML validator reports zero errors, so a failure leaves the user's existing PPTX byte-identical; source photos are opened read-only. Fixture source: `tests/fixtures/lumen/create/` (created by this section).

- [ ] Add the Create menu (LP-0967) with Slideshow (§8), PDF, PowerPoint, Album (§9), and Archive (`D04 T05 §12`) entries. Done when: a driven open of each entry shows its wizard (captures).
- [ ] If Imago's PDF presentation builder of `D03 T18 §7` is still in Imago, move it to `src/Photon.Core/Pdf/Presentation/` first and repoint Imago. Done when: `grep -rn "class PdfPresentation" src` prints one path, under `src/Photon.Core/`, and Imago's presentation test passes.
- [ ] Add Create PDF (LP-0968): a slideshow PDF with transitions and background, one PDF for all images, or one PDF per image, with order, names, and location. Done when: `CreatePdfTests` read the page count and `/Trans` entries of each kind with PdfPig.
- [ ] Add Save as PDF options (LP-0979): title, subject, author, and keywords; per-color-type compression (JPEG for color, Flate for grayscale, CCITT Group 4 for 1-bit); and paper size and fit. Done when: `CreatePdfTests` read the metadata and each image's filter with PdfPig.
- [ ] Add PDF security (LP-0979): user and owner passwords and print, copy, and modify permissions through the suite writer's security. Done when: `CreatePdfTests` read the encryption permissions of a protected PDF.
- [ ] Add multi-page TIFF or PDF from a selection (LP-0970) through the `D04 T13 §6` writer. Done when: `MultipageTiffTests` read back one page per selected photo.
- [ ] Add DocumentFormat.OpenXml (MIT) with a `docs/dev/decisions.md` row recording the license check. Done when: the row exists and the package is in `Directory.Packages.props`.
- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Documents/PptxWriter.cs` (LP-0969): a new PPTX with images per slide, slide duration (advance after), and linked or embedded images. Done when: `PptxWriterTests` pass the `OpenXmlValidator` with zero errors and read back the slide count and timing.
- [ ] Add a user-supplied design template `.potx`, captions, titles, and notes from tokens (LP-0969). Done when: `PptxWriterTests` read back the notes text and the template's slide master.
- [ ] Add append to an existing presentation (LP-0969) through the temp-then-replace path of the freeze check. Done when: a test appends three slides and asserts the deck's original slides are unchanged and a forced failure leaves the file byte-identical. Cheaper substitute: rewriting the target in place.
- [ ] Log one Serilog Information line per generated PDF, TIFF, or PPTX. Done when: a Serilog test logger asserts the line.
- [ ] Run the fidelity check: the PPTX of the fixture converts in LibreOffice Impress 25 headless (`soffice --convert-to pdf`) and the converted page count equals the slide count (version quoted). Done when: the output is quoted.
- [ ] Commit fixtures under `tests/fixtures/lumen/create/` with `reference.txt`, captures under `docs/captures/lumen/create/`, and `docs/user/lumen/create.md`. Done when: every wizard page is captured and documented.
- [ ] Commit: `"lumen: create PDFs and PowerPoint presentations"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~CreatePdfTests|FullyQualifiedName~PptxWriterTests|FullyQualifiedName~MultipageTiffTests"` exits 0; the Open XML validator result, the LibreOffice conversion page count, and the PdfPig read-back are quoted. Cheaper substitute that fails: a PPTX template zip with images swapped in, which the validator catches.

## 12. Email and Local Sharing

A user emails a few photos at a sensible size without leaving Lumen, or sends them to their own FTP server. This section adds an `EmailService` that renders attachments through §1's runner under a size limit and hands them to the default mail client through Simple MAPI or sends them over SMTP, reachable from export, browse, and the viewer, and FTP to the user's own server over §9's client. Photo-site uploads stay excluded as cloud. Catalog: LP-0867 to LP-0872, LP-0971 (7 features: export to email, the Send menu, the email wizard, upload to the user's FTP server, FTP transfer of a selection, email from the viewer and thumbnails, and IrfanView's MAPI or SMTP send). -> SOURCE: parity-lumen-email-share

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/email/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md, docs/design/components/Menu/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can email a few photos at a sensible size without leaving Lumen. Consumer: the mail client or SMTP server, and the recipients.
**Treatment:** an Email Photos dialog (recipients through the mail client's address book, size limit, convert to JPEG, send through the mail client or SMTP) opened from Send, File, Email, the export destination Email, the viewer, and browse. Cheaper substitute that fails the checkpoint: attaching originals at full size.
**Chrome:** consume §1's export runner for the attachments, Simple MAPI (`MAPISendMailW`, part of Windows), `System.Net.Mail.SmtpClient` with the password stored through DPAPI, and the `Photon.Core/Net/Ftp/` client of §9. Do not add a second FTP client.

**Requires:** display-session -- the mail client hand-off needs an interactive desktop

**Freeze check:** Attachments are rendered as new files into a Lumen temp folder under `%LOCALAPPDATA%\Rizonesoft\Lumen\Temp\Email\`, never beside or over an original; the cleanup deletes only files in that folder that the email job itself created. Fixture source: `tests/fixtures/lumen/export/`.

- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Share/EmailAttachmentPlanner.cs` (LP-0869): long edge and total size limits met by downscaling through §1, and convert to JPEG. Done when: `EmailAttachmentPlannerTests` meet a 5 MB total for ten 24-megapixel photos. Cheaper substitute: attaching originals, which the size-limit test catches.
- [ ] Add `MapiSender` calling `MAPISendMailW` with the attachments and `MAPI_DIALOG` so the user's client opens the message (LP-0867, LP-0868, LP-0971). Done when: `MapiSenderTests` with a fake MAPI entry point assert the attachment paths and recipients.
- [ ] Fall back, when no MAPI client is registered, to opening the temp folder and a `mailto:` link, saying why. Done when: a test with the fake reporting `MAPI_E_LOGIN_FAILURE` asserts the fallback message.
- [ ] Add `SmtpSender` (LP-0869, LP-0971) with server, port, TLS, and account under `Lumen.Output.Email.*` and the password stored with DPAPI. Done when: `SmtpSenderTests` send to a local SMTP test server and assert the attachments.
- [ ] Add the Email Photos dialog in `src/Lumen/Photon.Lumen.Desktop/Views/Output/Share/` with add and remove, recipients, the size limit, and the send method. Done when: a driven send opens the default mail client with two attachments (capture).
- [ ] Add the Send menu and email from the export destination list, browse, and the viewer (LP-0867, LP-0868, LP-0872). Done when: a driven email from the viewer attaches the current photo's rendition.
- [ ] Add FTP to the user's own server (LP-0870, LP-0871): server, user, password, remote folder, and progress through §9's client. Done when: a test uploads a selection to the local test FTP server.
- [ ] Delete temp attachments after the mail client returns or after 24 hours. Done when: a test asserts the cleanup deletes only the job's files.
- [ ] Log one Serilog Information line per email and FTP transfer (count, bytes, method, never the password). Done when: a Serilog test logger asserts the line.
- [ ] Commit captures under `docs/captures/lumen/email/` and `docs/user/lumen/email-and-sharing.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: email through the mail client or SMTP, and FTP to the user's server"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~EmailAttachmentPlannerTests|FullyQualifiedName~MapiSenderTests|FullyQualifiedName~SmtpSenderTests"` exits 0; a driven send opens the default mail client with two attachments (capture). Cheaper substitute that fails: attaching originals, which the size-limit test catches.

## 13. Export Presets, Metadata, Watermarks, and Post-Processing

A photographer repeats the right export in one click and trusts what metadata leaves the machine. This section adds built-in and user preset folders, Export with Preset and Export with Previous without the dialog, multi-preset export, Lightroom's metadata choices with person and location removal through `D04 T08 §8`'s `ExportMetadataEmbedder`, develop settings embedded in rendered outputs on request, the `D04 T11 §8` watermark, adding exports to the catalog stacked with the source, post-processing actions, disc burning through IMAPI2, completion sounds, and a warning when stored AI results need recomputing. It must not write a second watermark renderer. Catalog: LP-0424, LP-0873 to LP-0888, LP-0980 (18 features: include develop settings, remove person info, export and burn to disc, export with preset and with previous, built-in presets and user folders, multi-preset export, add to catalog and stack, metadata choices, the watermark, post-processing, the completion sound, the AI results warning, the export actions folder, export from develop in several copies, the rename template with recent templates, the ACDSee metadata options, presets listed in the menu, and export to several formats at once). -> SOURCE: parity-lumen-export-presets

**Fidelity:** Export dialog presets, metadata, watermarks, and post-processing -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/lumen/export-presets/. **Corrected 2026-09-27:** cited docs/captures/lumen/export-extended/ as the source; the captures under docs/captures/lumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/Menu/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/TextBox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Button/README.md, docs/design/components/Toast/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can repeat the right export in one click and trust what metadata leaves the machine. Consumer: the exported files, the catalog (stacked exports), and the post-processing programs.
**Treatment:** a preset tree on the dialog's left (built-in and user folders) with checkboxes for multi-preset export; File, Export with Previous (Ctrl+Alt+Shift+E) and Export with Preset submenus; Metadata, Watermarking, and Post-Processing sections. Cheaper substitute that fails the checkpoint: one preset at a time and metadata all-or-nothing.
**Chrome:** consume the `D04 T11 §8` watermark engine and editor, the stacking of `D04 T02 §7`, the Activity Manager of `D04 T11 §1`, `D04 T08 §8`'s `ExportMetadataEmbedder`, and the provenance store of `D04 T10 §1`. Do not write a second watermark renderer.

**Requires:** display-session -- the preset tree, submenus, and a disc burn need an interactive desktop

**Freeze check:** Embedded develop settings, metadata filtering, and watermarks apply only to the rendered output written through `AtomicFileWriter`; burning stages copies of the outputs, never originals; post-processing actions receive only output paths; `ExportDevelopSettingsEmbedTests` assert every original's SHA-256 is unchanged after a multi-preset export with every option on. Fixture source: `tests/fixtures/lumen/export/`.

- [ ] Add `src/Lumen/Photon.Lumen.Core/Output/Export/ExportPresetStore.cs` (LP-0876, LP-0888): built-in presets (Web JPEG, Full-size TIFF, Email, Print TIFF) plus user preset folders with add, update with current settings, remove, rename, import, and export as `.lumenexport` JSON. Done when: `ExportPresetStoreTests` round-trip every operation and load an older version.
- [ ] Add the preset tree to the dialog and the File, Export with Preset submenu listing the presets (LP-0888). Done when: a driven Export with Preset writes without opening the dialog (log line quoted).
- [ ] Add Export with Previous (LP-0875) on Ctrl+Alt+Shift+E, repeating the last job's settings. Done when: a test asserts the previous settings are used verbatim.
- [ ] Add multi-preset export (LP-0877, LP-0980): tick several presets to write one file per preset into a parent folder with per-preset subfolders and a conflict suffix. Done when: `MultiPresetExportTests` write three files in three folders from three presets.
- [ ] Add export from develop (LP-0885): several copies, each with its own format and size, in one job. Done when: a test writes a JPEG and a TIFF of one photo in one job.
- [ ] Add the rename template section shared with §1 (LP-0886): original-name and sequence tokens, metadata fields, recent templates, and start number. Done when: a test asserts the recent-templates list holds the last ten distinct templates.
- [ ] Add the metadata choices (LP-0879, LP-0887): copyright only, copyright and contact, all except camera and camera raw info, all; write keywords as the Lightroom hierarchy; include catalog fields (rating, label, title, caption); preserve the last-modified date, each applied through `ExportMetadataEmbedder`. Done when: `ExportMetadataFilterTests` read each choice's output with exiftool 13 and assert the field set.
- [ ] Add Remove Person Info (LP-0873: person keywords and MWG face regions) and Remove Location (EXIF GPS and XMP location fields). Done when: `ExportMetadataFilterTests` find no GPS, XMP location, person keyword, or `mwg-rs:Regions` in the output (exiftool dump quoted). Cheaper substitute: stripping only EXIF GPS.
- [ ] Add Include Develop Settings (LP-0424): the `photon-develop:` and `crs` XMP of `D01 T07 §6` embedded into rendered JPEG, TIFF, PNG, and PSD outputs. Done when: `ExportDevelopSettingsEmbedTests` find the XMP block in each output and the original's hash unchanged.
- [ ] Add the Watermarking section (LP-0880) on the `D04 T11 §8` engine and editor (text or graphic, shadow, opacity, anchor, inset, presets), applied at output size. Done when: a test asserts the watermark's pixel position scales with the output size.
- [ ] Add Add to This Catalog and Stack with Original (LP-0878): exported files enter the catalog with origin `library`, stacked with the source through `D04 T02 §7`. Done when: a test asserts the new record and its stack membership.
- [ ] Add the post-processing actions (LP-0881, LP-0884): do nothing, show in Explorer, open in Imago through `D02 T15 §11`'s `SuiteAppLocator`, open in another application, or run a program from `%APPDATA%\Rizonesoft\Lumen\Export Actions\` with the output paths as arguments; only programs the user placed there run. Done when: `ExportPostProcessTests` with a fake launcher assert each action's command line.
- [ ] Add Burn to Disc (LP-0874) as a destination through IMAPI2 (`IDiscMaster2`, `IDiscFormat2Data`): stage the outputs to a temp folder, then burn with progress on the Activity Manager; a machine without a writer hides the destination with a tooltip saying why. Done when: `DiscBurnPlannerTests` with a fake recorder assert the staged file list and the hidden-destination tooltip.
- [ ] Add the completion sound (LP-0882) through the Windows sound event `Lumen.Output.Export.Sound`, governed by the system Sounds settings. Done when: a test asserts the event is raised once per finished job.
- [ ] Add the AI results warning (LP-0883): before the job, photos whose stored AI masks or removals `D04 T10 §1` marks stale are listed with Update, Export Anyway, and Cancel. Done when: a test with one stale photo asserts the prompt lists it and Cancel writes nothing.
- [ ] Show the job summary on completion (written, skipped, failed with reasons) through the Activity Manager notification. Done when: a driven 50-photo multi-preset export shows the summary (capture).
- [ ] Log one Serilog Information line per preset run and per post-processing action. Done when: a Serilog test logger asserts both lines.
- [ ] Commit captures of the preset tree and new sections under `docs/captures/lumen/export-extended/` and extend `docs/user/lumen/export.md`. Done when: every control is captured and documented.
- [ ] Commit: `"lumen: export presets, metadata choices, watermarks, and post-processing"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~ExportPresetStoreTests|FullyQualifiedName~MultiPresetExportTests|FullyQualifiedName~ExportMetadataFilterTests|FullyQualifiedName~ExportPostProcessTests|FullyQualifiedName~ExportDevelopSettingsEmbedTests|FullyQualifiedName~DiscBurnPlannerTests"` exits 0; the exiftool 13 dump of a person-and-location-stripped export is quoted; a driven multi-preset export with a watermark is captured. Cheaper substitute that fails: stripping only EXIF GPS, which leaves XMP location and face regions that `ExportMetadataFilterTests` catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with every test class named in §1 to §13 reporting, and `dotnet test Photon.slnx --filter "Category=Fidelity"` passes this file's export, contact-sheet, and format goldens
- [ ] The unchanged-originals test of `D04 T02 §1` passes after a session that exports, publishes, prints to file, builds a contact sheet, a slideshow PDF, a gallery, a book, a PDF, a PPTX, and an email over the fixture set
- [ ] `grep -rn "class ContactSheet" src` and `grep -rn "FluentFTP" src --include=*.cs` print paths only under `src/Photon.Core/`
- [ ] Every generated HTML page validates in the W3C Nu HTML Checker, every PPTX passes the Open XML validator, and every book PDF passes qpdf `--check` (versions quoted)
- [ ] `docs/dev/decisions.md` carries a license row for Vortice.MediaFoundation (added by `D04 T04 §8`), DocumentFormat.OpenXml, FluentFTP, and the MIT gallery templates, and `grep -rn "NAudio\|Renci.SshNet" src` prints nothing
- [ ] B-035 is gone from `todo/backlog.md`, and its source key `lumen-roadmap-print` is carried by §4 alone
- [ ] `python scripts/todo-claims.py` holds for this file
- [ ] `python scripts/todo-graph.py validate` clean
