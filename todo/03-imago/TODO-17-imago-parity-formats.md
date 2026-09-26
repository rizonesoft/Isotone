---
schema_version: 1
id: imago-parity-formats
domain: 03-imago
status: draft
title: "TODO-17 -- Imago Parity: the File Menu and Every Format"
depends_on: []
frozen: true
track: I17
---

# TODO-17 -- Imago Parity: the File Menu and Every Format

> **Goal:** Imago's File menu does everything Photoshop, Affinity Photo, and GIMP do to get pixels in and out (open as, place embedded and linked, revert, close all, save a copy, a format matrix, export versus save semantics, clipboard, screenshots, scanners, URLs, archives), and it reads and writes every format those three apps carry: PSD and PSB with live adjustments, styles, text, and smart objects; GIMP XCF; WebP, AVIF, HEIF, JPEG XL, JPEG 2000, JPEG XR, and QOI; OpenEXR, Radiance, PFM, PNM, FITS, and DICOM; PDF, Photoshop PDF, EPS, SVG, WMF, and EMF; the long tail of legacy and resource formats; the full JPEG, PNG, and TIFF option sets; and EXIF, IPTC, and XMP metadata. Every codec registers with one `FormatRegistry` in `src/Imago/Photon.Imago.FileFormats/`, shared codecs live in `src/Photon.Core/Formats/`, `src/Photon.Core/Pdf/`, and `src/Photon.Core/Metadata/` (moved from Nodus on this second use, never copied), native libraries are the ones `docs/dev/decisions.md` records with GPL-3.0 checks, and every reader and writer owes a format fidelity proof against a named reference implementation. Opening never changes a file; saving goes through the atomic writer; what a format cannot carry is reported, never silently dropped.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `src/Imago/src/Imago.FileFormats/` holds only the `IImageFormat` interface (`IImageFormat.cs`, 42 lines); no codec exists. The File menu in `src/Imago/src/Imago.UI/Views/MainWindow.xaml` has New, Open, Save, Save As, Export, and Exit, with no Place, Revert, Close, Import, or Print entry. The open and export filters are hard-coded strings in `src/Imago/src/Imago.UI/Services/IFileDialogService.cs` that already list WebP twice with no codec behind them; §1's registry replaces them. The installer (`installer/Imago.iss`) registers a `.psd` association, and no Imago fixture folder exists (`tests/fixtures/imago` is absent). No PSD reader or writer exists anywhere in Nodus yet; `D02 T14 §13` builds both and `D03 T04 §5` moves the reader. Backlog B-022 (more formats and PSD write) is promoted into §5, with its PSD-write part in §2 and §13, EXR in §6, and GIF in §8; the integration that lands this file deletes the entry.
<!-- claim: lines src/Imago/src/Imago.FileFormats/IImageFormat.cs = 42 -->
<!-- claim: count "Header="(Place|Revert|Close|Print|Import)" src/Imago/src/Imago.UI/Views/MainWindow.xaml = 0 -->
<!-- claim: count "\*\.webp" src/Imago/src/Imago.UI/Services/IFileDialogService.cs = 2 -->
<!-- claim: count "\.psd" installer/Imago.iss = 7 -->
<!-- claim: absent tests/fixtures/imago -->
<!-- claim: count "PsdReader|PsdWriter" src/Nodus/**/*.cs = 0 -->

## Inputs

- [`standards/imago.md`](../../standards/imago.md) -- every codec owes a fidelity proof and says what it cannot carry before it writes
- [`standards/testing.md`](../../standards/testing.md) -- fixtures, goldens, and the Fidelity trait
- [`standards/shared.md`](../../standards/shared.md) -- atomic writes, refusals that name the file and the reason, progress and Cancel over one second, one log line per change, a dependency is a decision
- [`docs/parity/imago-section-design.md`](../../docs/parity/imago-section-design.md) -- the blueprint and the "Formats and licensing" table for this file; [`docs/parity/imago-parity.md`](../../docs/parity/imago-parity.md) -- the catalog rows each section owns
- Adobe Photoshop File Formats Specification (current edition), with psd-tools 1.10 and GIMP 3.2.6 as reading oracles; GIMP `devel-docs/XCF.md` at the 3.2.6 tag with `gimp-console-3.2` as the golden oracle; OpenRaster
- TIFF 6.0, BigTIFF, Adobe TIFF Technical Note 3 (floating-point predictor), and libtiff 4.7 `tiffinfo` and `tiffdump`; PNG Third Edition (W3C, with cICP, mDCV, and cLLI) and `pngcheck` 3.0; JFIF 1.02; CIPA DC-008-2023 (Exif 3.0); ISO 21496-1 and Google Ultra HDR 1.1 gain maps
- libwebp 1.5, libavif 1.2 with dav1d and libaom, libheif 1.19 with libde265 and x265, libjxl 0.11, OpenJPEG 2.5, OpenEXR 3.3, PDFium, and libjpeg-turbo 3.1, with their CLIs as oracles
- ISO 32000-2 (PDF 2.0), ISO 15930 (PDF/X-1a, X-3, X-4), Adobe EPS 3.0 (Technical Note 5002), MS-EMF and MS-WMF, DICOM PS3.5, PS3.10, and PS3.15 (2025), FITS 4.0, IPTC Photo Metadata Standard 2024.1, XMP Specification Parts 1 to 3
- Test-time oracles only: exiftool 13, ImageMagick 7.1, OpenImageIO 3.0 `oiiotool`, dcmtk 3.6 `dcm2pnm`, DirectXTex `texconv`, Ghostscript 10.x, MuPDF `mutool draw`, Inkscape 1.4
- [`todo/backlog.md`](../backlog.md) -- B-022 (`legacy-imago-7.2-7.3`) is promoted into §5 and leaves the backlog in the integration commit; B-038 (Nodus legacy raster formats) was promoted on 2026-09-27 into `D02 T18 §8` and `D02 T18 §9`, whose XCF import moves §4's decoding core to `Photon.Core`; B-044 (animation) owns animated GIF, WebP, and APNG; B-045 (Affinity files) relies on §3 as its interop path
- -> XREF: D01 T02 §3 -- single-instance file-open forwarding §1 routes through
- -> XREF: D01 T02 §5 -- the atomic writer every writer here saves through
- -> XREF: D01 T03 §2 -- mipmap and export resampling in §8
- -> XREF: D01 T03 §3 -- indexed quantization for GIF and palette formats in §8
- -> XREF: D01 T04 §1 -- profiles for every reader and writer, and the monitor profile §12 tags screenshots with
- -> XREF: D01 T04 §3 -- CMYK, Lab, and duotone buffers for PSD, TIFF, JPEG, and JPEG XL
- -> XREF: D01 T06 §1 -- the GEGL op-id map §4 translates XCF filter stacks through
- -> XREF: D01 T07 §4 -- HEIC depth maps become develop depth sources in §5
- -> XREF: D01 T07 §6 -- the XMP packet core §10 consumes
- -> XREF: D02 T13 §4 -- printer marks §7 moves
- -> XREF: D02 T13 §10 -- the PostScript writer §7 moves for EPS
- -> XREF: D02 T13 §14 -- the PDF writer §7 moves
- -> XREF: D02 T13 §15 -- PDF presets and standards §7 moves
- -> XREF: D02 T13 §16 -- PDF security §7 moves
- -> XREF: D02 T14 §2 -- PdfPig, which §1 and §7 reuse for annotations and text positions
- -> XREF: D02 T14 §9 -- the Ghostscript runner §7 moves
- -> XREF: D02 T14 §11 -- the EMF and WMF code §7 moves
- -> XREF: D02 T14 §12 -- the TGA, PCX, BMP, and CUR codecs §8 moves, and the JPEG 2000 decision §5 reconciles
- -> XREF: D02 T14 §13 -- the PSD writer §2 moves
- -> XREF: D02 T14 §16 -- Nodus's progressive JPEG path switches to §11's encoder
- -> XREF: D02 T14 §19 -- the WIA acquire service §12 moves
- -> XREF: D03 T03 §1 -- the document tabs §1 and §12 open into
- -> XREF: D03 T04 §1 -- the codec decision and the WIC codec it placed
- -> XREF: D03 T04 §2 -- PNG and JPEG readers and writers and the JPEG options dialog §11 extends
- -> XREF: D03 T04 §3 -- the TIFF reader and writer §11 extends
- -> XREF: D03 T04 §4 -- the native format and its atomic save
- -> XREF: D03 T04 §5 -- the PSD reader §2 and §3 extend
- -> XREF: D03 T08 §1 -- the contract live content maps onto
- -> XREF: D03 T08 §5 -- the notes that PDF annotations import into
- -> XREF: D03 T09 §5 -- blend ranges written to and read from PSD
- -> XREF: D03 T09 §7 -- layer styles written to and read from PSD
- -> XREF: D03 T09 §8 -- the rest of the layer styles in PSD
- -> XREF: D03 T09 §9 -- smart objects for place, open as smart object, and PSD smart objects
- -> XREF: D03 T09 §10 -- linked smart objects for place linked and XCF link layers
- -> XREF: D03 T09 §11 -- layer comps in PSD
- -> XREF: D03 T10 §6 -- the guided filter that refines HEIC depth maps
- -> XREF: D03 T10 §10 -- alpha and spot channels in PSD and TIFF
- -> XREF: D03 T11 §1 -- adjustment layers in PSD
- -> XREF: D03 T11 §4 -- the OpenColorIO wrapper for EXR color spaces
- -> XREF: D03 T11 §7 -- image modes and indexed conversion
- -> XREF: D03 T12 §3 -- the GBR and GIH readers §9 adds writers beside
- -> XREF: D03 T12 §10 -- the PAT reader §9 adds a writer beside
- -> XREF: D03 T14 §1 -- XCF filter stacks become live filters
- -> XREF: D03 T15 §4 -- 32-bit documents and HDR display for EXR, HDR, JPEG XR, and gain maps
- -> XREF: D03 T15 §5 -- auto-align for Load Files into Stack
- -> XREF: D03 T15 §10 -- astrophotography stacking consumes FITS
- -> XREF: D03 T15 §12 -- editable EXIF in develop
- -> XREF: D03 T16 §1 -- text layers in PSD, XCF, and PDF
- -> XREF: D03 T16 §5 -- paths and the moved SVG reader
- -> XREF: D03 T16 §7 -- shape and vector layers in PSD and XCF
- -> XREF: D03 T16 §8 -- the SVG writer §1's registry lists
- -> XREF: D03 T18 §1 -- Export As consumes the registry and every writer here
- -> XREF: D03 T18 §4 -- OCIO configuration and working spaces for EXR
- -> XREF: D03 T18 §6 -- consumes the printer marks renderer §7 moves
- -> XREF: D03 T18 §7 -- halftone screens and transfer functions written through §7's EPS and PDF writers
- -> XREF: D03 T19 §1 -- provenance written as XMP through §10
- -> XREF: D04 T01 §11 -- Lumen's sidecars consume §10's EXIF and IPTC code
- -> XREF: D03 T08 §6 -- the XMP history log §10 exports
- -> XREF: D03 T08 §8 -- the SVG and EMF paste entries §16 enables
- -> XREF: D03 T14 §6 -- EXIF lens data from §10 for its profile match
- -> XREF: D03 T15 §6 -- EXIF exposure values from §10 for bracket EVs
- -> XREF: D03 T20 §5 -- the Files and Export preference pages that surface the `Imago.Files.*`, `Imago.Formats.*`, and export metadata keys
- -> XREF: D01 T08 §1 -- the XPM, Pixar PXR, and Scitex CT codecs §8 and §9 register instead of writing their own
- -> XREF: D01 T08 §3 -- the ICO and CUR codec (moved from `D02 T14 §12`) §8 registers
- -> XREF: D02 T18 §8 -- Nodus's DCS reader and writer, which §9 moves to `Photon.Core` beside the EPS writer
- -> XREF: D02 T18 §9 -- Nodus's XCF import, which moves §4's decoding core to `Photon.Core`

## Outcome

- One `FormatRegistry` lists every reader and writer with its extensions, magic bytes, modes, depths, and what it carries; the File menu, the open and save filters, and the format matrix are generated from it and no filter string is hard-coded.
- Opening, placing, reverting, closing, and Save a Copy behave as the three competitors do, and nothing a user opens is ever written by opening it.
- PSD and PSB round-trip with layers, masks, channels, adjustments, styles, text, smart objects, and comps live, proven against psd-tools and GIMP; XCF reads and writes with layers, text, vector and link layers, and filter stacks, proven against GIMP 3.2.
- Every modern, HDR, scientific, document, vector, legacy, and resource format in the catalog opens and, where the competitors write it, saves, each within a stated tolerance of a named reference implementation, with a missing native library refused by name.
- JPEG, PNG, and TIFF expose their full option sets, including arithmetic JPEG, HDR PNG, BigTIFF, and layered TIFF, and EXIF, IPTC, and XMP are read, edited, templated, embedded, stripped, and written to sidecars.

**Adjacency:** list=applicable @ D03 T17 §12; document=applicable @ D03 T17 §7; settings=applicable @ D03 T17 §1; reporting=applicable @ D03 T17 §3; notifications=applicable @ D03 T17 §1; permissions=applicable @ D03 T17 §7; audit=applicable @ D03 T17 §1; exchange=applicable @ D03 T17 §1; reverse=applicable @ D03 T17 §1

**Adjacency rationale:** The lists are the format list and matrix (§1), the document history dialog (§12), the PDF presets manager (§7), and metadata templates (§10). Photoshop PDF and PDF export (§7) and EPS (§16) are the documents a print shop receives; printing itself is `D03 T18 §6`. Settings are `Imago.Formats.<Format>.*` per codec and `Imago.Files.*`, each with a default and a named consumer. Every import returns a report naming what was rasterized, dropped, or mapped (§3 for PSD, §4 for XCF), and File Info shows the metadata (§10). Reads and writes over one second show progress and Cancel, and exports raise a completion notification (§1). Read-only targets, absent Ghostscript, missing native codecs, encrypted PDFs, and online reads without a user action are refused by name (§1, §5, §7, §12, §16). One Serilog Information line per open, save, place, and export with format, size, and milliseconds is the audit trail (§1, §15). Every format in this file is exchange. Revert to saved, Save a Copy never changing the document, and undoable places and metadata edits are the reverse (§1, §10).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | File menu extensions: open, revert, close, and save a copy | D03 T08 §1, D03 T09 §10, D03 T14 §11 |  [ ]   |
|   2   |   §15   | Place, export and overwrite semantics, notes import, Load Files into Stack, and watermarks | §1, D03 T09 §9 |  [ ]   |
|   3   |   §12   | Create from clipboard, screenshots, scanners, URLs, and archives | §1 |  [ ]   |
|   4   |   §2    | PSD and PSB write: structure | D03 T04 §5, D03 T09 §9 |  [ ]   |
|   5   |   §13   | PSD write: live content and editability options | §2, D03 T16 §1, D03 T11 §1, D03 T09 §8, D03 T09 §11 |  [ ]   |
|   6   |   §3    | PSD read fidelity: live adjustments, styles, text, and smart objects | §13 |  [ ]   |
|   7   |   §4    | GIMP XCF read | D03 T08 §1, D03 T14 §1, D03 T16 §7, D03 T16 §11, D03 T09 §10 |  [ ]   |
|   8   |   §14   | GIMP XCF write | §4 |  [ ]   |
|   9   |   §5    | Modern web formats: WebP, AVIF, HEIF, JPEG XL, JPEG 2000, QOI, JPEG XR | D03 T04 §1 |  [ ]   |
|  10   |   §6    | HDR and scientific formats | D03 T15 §4 |  [ ]   |
|  11   |   §7    | Document formats: PDF import, Photoshop PDF, and PDF export | D03 T16 §5, D02 T13 §14, D02 T14 §9, §15 |  [ ]   |
|  12   |   §16   | PostScript, EPS, SVG, and metafiles | §7, D03 T16 §5 |  [ ]   |
|  13   |   §8    | Common and legacy raster formats I | D03 T04 §1, D01 T08 §1, D01 T08 §3 |  [ ]   |
|  14   |   §9    | Legacy raster formats II and text and resource exports | §8, D01 T08 §1, D02 T18 §8 |  [ ]   |
|  15   |   §11   | JPEG, PNG, and TIFF option extensions | D03 T04 §3, D03 T16 §10 |  [ ]   |
|  16   |   §10   | Metadata: EXIF, IPTC, XMP, and File Info | D03 T08 §1 |  [ ]   |

---

## 1. File Menu Extensions: Open, Revert, Close, and Save a Copy

Every later section adds a codec, and without one registry each would add its own filter string and menu entry, which is how today's dialogs came to list WebP with no codec behind it. This section builds the `FormatRegistry` every codec registers with and generates the File menu, the dialogs' filters, and the format matrix from it, then adds the commands the competitors have around opening and saving: vector routing, Open As, open as smart object or layers, Revert, Close Others and All, and Save a Copy with content options. Placing, export and overwrite semantics, PDF notes import, Load Files into Stack, and watermark placement are §15's, split from this section on 2026-09-27 (operator decision to split the packed sections). The open document is never written by any of these except an explicit save. Catalog: IP-1704 to IP-1716 (13 features: open including vector files, drag to open, revert, close and close all, the open dialog, Open As, open as smart object or layers, shell open and drag to place, close others, Save a Copy, save content options, the format list and matrix, and revert as GIMP's row).

**Fidelity:** `docs/captures/imago/main-window/` for the File menu, extended; new build, no baseline for the format matrix and Save a Copy dialogs, captured to `docs/captures/imago/file-menu/`.
**Job:** a user gets any file in as a document, layer, or smart object and gets copies out without disturbing the open document. Consumer: the document tabs, the Layers panel, and the file on disk.
**Treatment:** File menu commands, the Windows common file dialog with a filter per registered format, a Save a Copy dialog with content options, a format matrix dialog with a customize list, and one combined save prompt for Close All. Cheaper substitute that fails the checkpoint: hard-coded filter strings.
**Chrome:** consume the registry, `AtomicFileWriter`, the `D03 T09 §9` and `D03 T09 §10` smart objects, the status strip, and the suite history. Do not add a second file dialog service.

**Requires:** display-session -- driving the File menu, dialogs, and drops needs an interactive desktop

**Freeze check:** Save a Copy writes through `AtomicFileWriter` to the chosen path and never to the open document's own path without the overwrite prompt; the document's path and dirty state are unchanged after it; a failed or interrupted write leaves any existing target byte-identical; opening and reverting never open a source file for writing. Fixture source: `tests/fixtures/imago/file-menu/` (created by this section) and `tests/fixtures/save-over/`.

- [ ] Extend `IImageFormat` with a `FormatCapabilities` record (extensions, magic bytes, read and write support, modes and depths, and what it carries: layers, alpha, spot, notes, ICC) in `src/Imago/Photon.Imago.FileFormats/FormatCapabilities.cs` (IP-1714). Done when: the existing PNG, JPEG, TIFF, native, and PSD formats declare their capabilities and a test lists them.
- [ ] Add `src/Imago/Photon.Imago.FileFormats/FormatRegistry.cs`: registration, lookup by extension and by magic bytes, and generated filter strings (All Readable plus one per format). Done when: `FormatRegistryTests` assert the generated filter lists every registered reader and a PNG renamed `.jpg` opens as PNG by its magic bytes.
- [ ] Delete the hard-coded `FileFilters` and `ExportFormats` strings in `IFileDialogService` and route every open, save, and export dialog through the registry. Done when: `grep -rn "\*\.webp" src/Imago` finds no string literal and the dialogs list only registered formats.
- [ ] Wire File, Open (IP-1704, IP-1708) through the Windows common file dialog with All Readable and per-format filters; browse, search, bookmarks, columns, and hidden files come from the common dialog itself, recorded in `docs/user/imago/files.md`. Done when: a driven open of each fixture opens it in a new tab.
- [ ] Route vector files to the import dialogs `D03 T17 §7` (PDF) and `D03 T17 §16` (SVG, EPS, AI) register; until each lands, its extensions are refused with a message naming it. Done when: `python scripts/todo-graph.py resolve 'D03 T17 §7'` and `python scripts/todo-graph.py resolve 'D03 T17 §16'` resolve and a test asserts each refusal text names its section.
- [ ] Add Open As (IP-1709), which forces a chosen format regardless of extension. Done when: Open As PNG on a `.dat` copy of a PNG fixture opens it.
- [ ] Add Open as Smart Object and Open as Layers (IP-1710) through `D03 T09 §9`. Done when: a driven Open as Smart Object yields one smart object layer whose content equals the file.
- [ ] Route shell open, drag and drop onto the window to open or onto a document to place, and single-instance forwarding through `D01 T02 §3` (IP-1705, IP-1711). Done when: a driven drop of two files opens two tabs and a drop onto an open document places a layer.
- [ ] Add File, Revert (IP-1706, IP-1716): reload from disk as one history step "Revert", disabled for a never-saved document with a tooltip saying why. Done when: a test edits, reverts, and the pixels equal the file, and undo restores the edit.
- [ ] Add Close, Close Others, and Close All (IP-1707, IP-1712) with one prompt listing every dirty document with Save, Don't Save, and Cancel. Done when: a driven Close All with two dirty documents shows one prompt naming both.
- [ ] Add File, Save a Copy (IP-1713) in `src/Imago/Photon.Imago.Desktop/Views/Files/SaveCopyDialog.xaml`, offering flattening formats, with the document keeping its path and dirty state. Done when: a test saves a copy of a dirty document and its path and dirty flag are unchanged. Cheaper substitute: Save As under another name, which changes the document's path.
- [ ] Add the content options (IP-1714): layers, alpha channels, spot colors, notes, and ICC profile, each enabled only when the chosen format's capabilities carry it. Done when: choosing JPEG disables Layers with a tooltip naming what JPEG cannot carry.
- [ ] Add the format matrix dialog (IP-1715) generated from the registry (bit depth and mode support per format) with a customize list stored in `Imago.Formats.Visible`. Done when: hiding a format removes it from the dialogs without a restart and the capture shows the matrix.
- [ ] Add `Imago.Files.LegacySaveAs` (default false), restoring Photoshop's legacy Save As that lists every writable format. Done when: with the setting on, Save As lists non-native formats.
- [ ] Register the SVG writer of `D03 T16 §8` as a write-only format, so the SVG export appears in the generated lists. Done when: the Save a Copy format list contains SVG.
- [ ] Register the Photoshop format plug-ins (`.8bi`) that `D01 T09 §3` hosts as `FormatRegistry` entries through the `D03 T14 §11` adapter, each named with its plug-in and marked third-party in the format matrix; a plug-in format that fails in the host is refused by name and never falls back silently to another codec. Done when: `FormatRegistryTests.PluginFormat` registers a stub plug-in format entry, the generated filter lists it with its plug-in name, and a failing stub is refused by name.
- [ ] Show progress with Cancel on the status strip for any read or write over one second, and a completion notification for exports. Done when: a driven save of a 100-megapixel fixture shows progress and Cancel leaves the target unchanged.
- [ ] Log one Serilog Information line per open and save (`{Action} {Format} {Path} {Width}x{Height} in {ElapsedMs} ms`) as the audit trail, and name the history step "Revert". Done when: a Serilog test logger asserts each line.
- [ ] Commit fixtures under `tests/fixtures/imago/file-menu/` (a mislabeled PNG, a `.dat` copy of a PNG, and one fixture per registered format) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/file-menu/` and the extended `docs/captures/imago/main-window/`, and write `docs/user/imago/files.md`. Done when: every File menu command this section adds appears in a capture and the page documents it.
- [ ] Commit: `"imago: the File menu on one format registry"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~FormatRegistryTests"` exits 0, asserting the generated filter lists every registered reader and the matrix matches each codec's declaration; a driven run opens, reverts, and saves a copy of the fixtures with captures committed and the unchanged source hash quoted. Cheaper substitute that fails: keeping hard-coded filters, which the registry test catches when a codec is added.

## 12. Create from Clipboard, Screenshots, Scanners, URLs, and Archives

Users start documents from whatever is at hand: the clipboard, a screenshot, a scanner, a URL, or a compressed archive. This section adds those sources on top of §1's registry, moving Nodus's WIA acquire service (`D02 T14 §19`) into `Photon.Core` as its second consumer, and it touches the network only when the user asks for a URL. Catalog: IP-1722 to IP-1731 (10 features: drops on the document tab bar, archives, Open Location, WIA acquire, new from clipboard, screenshots, copy image location and show in Explorer, the document history dialog, send by email, and document history multi-select).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/acquire/`.
**Job:** a user starts a document from whatever is at hand without saving an intermediate file. Consumer: the new document tab.
**Treatment:** File, New from Clipboard; File, Create, Screenshot with a region overlay and options; File, Acquire from a scanner or camera; Open Location; and the Document History dialog. Cheaper substitute that fails the checkpoint: shelling out to external tools.
**Chrome:** consume §1's registry, the moved WIA service, the settings store, and the status strip. Do not add a second archive or HTTP helper.

**Requires:** display-session -- screenshots, WIA dialogs, and drops need an interactive desktop

- [ ] Move first: `WiaAcquireService` of `D02 T14 §19` into `src/Photon.Core/Acquire/` as its second consumer (IP-1725), repointing Nodus; TWAIN stays unsupported, recorded in `docs/dev/decisions.md`. Done when: `grep -rn "class WiaAcquireService" src` prints one path, under `src/Photon.Core/`.
- [ ] Add File, Acquire (IP-1725) opening the WIA device dialog and creating a document from the acquired image with its resolution. Done when: a driven acquire from the WIA virtual device (or a skip naming the missing device) creates a document.
- [ ] Open files dropped on the document tab bar (IP-1722). Done when: a driven drop on the tab bar opens a new tab.
- [ ] Open archives (IP-1723): gz through `GZipStream` and zip through `ZipArchive` with an entry picker. Done when: `ArchiveOpenTests` open `.png.gz` and a two-entry `.zip` to identical pixels.
- [ ] Add SharpCompress (MIT) for bz2 and xz, with a new `docs/dev/decisions.md` row naming the license and that .NET reads neither format. Done when: `ArchiveOpenTests` open `.png.bz2` and `.png.xz` to identical pixels.
- [ ] Add File, Open Location (IP-1724): http and https through `HttpClient` only on the user's command, with `Imago.Files.OpenLocation.MaxMegabytes` (default 512), a content-type check, progress, and Cancel, plus `file:` URIs. Done when: `OpenLocationTests` fetch from a local `HttpListener` and refuse an oversize response by name.
- [ ] Add ftp locations through FluentFTP (MIT) with a `docs/dev/decisions.md` row; if the row declines the package, ftp URLs are refused by name. Done when: the decision row exists and a test covers the chosen behavior.
- [ ] Add File, New from Clipboard (IP-1726) for PNG, DIBV5 with alpha, and DIB flavors; the SVG flavor is disabled with a tooltip naming `D03 T17 §16`, whose rasterizer enables it. Done when: a test puts a DIBV5 with alpha on the clipboard and the new document keeps the alpha.
- [ ] Add File, Create, Screenshot (IP-1727) through `Windows.Graphics.Capture` for a window, the whole screen, or one monitor. Done when: a driven capture of a known window yields a document of its size.
- [ ] Add the screenshot options: region by an overlay, include decorations, pointer composited from `GetCursorInfo`, and a delay, with the document tagged with the monitor's profile through `D01 T04 §1`; selection delay is not available on Windows, documented in `docs/user/imago/acquire.md`. Done when: a capture with the pointer option contains the cursor image and the document carries the monitor profile.
- [ ] Add Copy Image Location and Show in Explorer (IP-1728). Done when: a test asserts the clipboard text equals the document path.
- [ ] Add the Document History dialog (IP-1729, IP-1731): a searchable list of recent documents with thumbnails, multi-select open, remove, and clear. Done when: a driven multi-select opens two recent documents.
- [ ] Add File, Send by Email (IP-1730): export a copy through §1, then Simple MAPI `MAPISendMailW` with the attachment; with no MAPI client the command is refused by name. Done when: a test with a fake MAPI shim receives the attachment path, and the no-client refusal is asserted.
- [ ] Log one Serilog Information line per acquire, screenshot, URL open, and archive open. Done when: a Serilog test logger asserts each line.
- [ ] Commit archive fixtures under `tests/fixtures/imago/archives/` with `reference.txt`, captures under `docs/captures/imago/acquire/`, and write `docs/user/imago/acquire.md`. Done when: every source in the Treatment appears in a capture and the page documents it.
- [ ] Commit: `"imago: new from clipboard, screenshots, scanners, URLs, and archives"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~ArchiveOpenTests|FullyQualifiedName~OpenLocationTests"` exits 0, opening `.png.gz`, `.png.bz2`, `.png.xz`, and `.zip` fixtures to identical pixels and refusing an oversize `HttpListener` response; a driven screenshot and clipboard run is captured under `docs/captures/imago/acquire/`. Cheaper substitute that fails: gz-only archives, which the bz2 and xz fixtures catch.

## 2. PSD and PSB Write: Structure

A PSD is how Imago work reaches Photoshop users, so the writer must carry the whole document structure, not a composite. Nodus builds the suite's PSD writer (`D02 T14 §13`); this section moves it into `Photon.Core` beside the reader `D03 T04 §5` already moved and maps Imago's layers, groups, masks, channels, paths, guides, and every mode and depth onto it, including PSB for large documents. Live content (adjustments, styles, text, smart objects) is §13's. Catalog: IP-1732 to IP-1733 (2 features: PSD write with layers, masks, modes, metadata, and the compatibility composite, and PSB large-document read and write, whose read side is §3).

**Fidelity:** no surface of its own (PSD appears in §1's format list; its options page is §13's)

**Freeze check:** PSD and PSB saves write through `AtomicFileWriter`; killing the process mid-save leaves any existing target byte-identical; a save to PSD never changes the open document or its `.imago` file. Fixture source: `tests/fixtures/imago/psd-write/` (created by this section).

- [ ] Move first: `PsdWriter` from `src/Nodus/Photon.Nodus.Core/Formats/Psd/` (`D02 T14 §13`) into `src/Photon.Core/Formats/Psd/` beside the moved reader, with its tests, repointing Nodus. Done when: `grep -rn "class PsdWriter" src` prints one path, under `src/Photon.Core/`, and Nodus's PSD export tests pass.
- [ ] Add `src/Imago/Photon.Imago.FileFormats/Psd/ImagoPsdExporter.cs` for raster layers with opacity, fill opacity, visibility, locks, and color labels. Done when: psd-tools 1.10 dumps the written fixture's layer tree with equal names, opacity, fill, visibility, and locks.
- [ ] Write groups as `lsct` section dividers, open or closed. Done when: a nested group fixture dumps with the same nesting and open state.
- [ ] Write layer masks with density and feather, and clipping. Done when: psd-tools reads each mask's bounds, density, and feather equal to the document's.
- [ ] Write blend-mode keys through the inverse of the reader's map. Done when: a one-layer-per-mode fixture reads back through the moved reader with every mode equal.
- [ ] Write alpha and spot channels from `D03 T10 §10` with Unicode names (resource 1045), alternate spot colors (1067), and display info (1077). Done when: psd-tools lists the channels with their names and GIMP 3.2 opens them.
- [ ] Write the resources resolution (1005), guides (1032), ICC profile (1039), XMP (1060), and JPEG thumbnail (1036). Done when: psd-tools reads each resource and the ICC bytes equal the document's profile.
- [ ] Write paths (2000 to 2997) and the clipping path (2999) from `D03 T16 §5`'s path set. Done when: the moved reader reads every path back with geometry within 1e-6 of the fixed-point encoding.
- [ ] Write RGB, gray, CMYK (through `D01 T04 §3`), Lab, indexed, and bitmap modes (IP-1732). Done when: each mode fixture composites in `gimp-console-3.2` within 1/255.
- [ ] Write 8, 16, and 32-bit depths through the `Lr16` and `Lr32` blocks. Done when: a 16-bit fixture reads back 16-bit through psd-tools with values equal.
- [ ] Write the maximize-compatibility composite unless §13's preference says never. Done when: a test asserts the composite is present by default and absent with the preference set to never.
- [ ] Write PSB (IP-1733): version 2 with 8-byte lengths for the keys the specification lists (LMsk, Lr16, Lr32, Layr, Mt16, Mt32, Mtrn, Alph, FMsk, lnk2, FEid, FXid, PxSD), chosen for documents over 30,000 px or 2 GB. Done when: a 40,000 px wide fixture writes as PSB and psd-tools reads its layer tree.
- [ ] Compress channels with RLE per scanline, and ZIP with prediction for 16 and 32 bit. Done when: a test asserts the compression field per channel and GIMP reads both.
- [ ] Register PSD and PSB write with §1's registry. Done when: Save a Copy lists PSD and PSB.
- [ ] Add `tests/Photon.Imago.FileFormats.Tests/Psd/PsdWriteBudgetTests.cs`: a 100-layer, 24-megapixel, 16-bit RGB document writes in under 10 s with progress and Cancel through `AtomicFileWriter`, and one Serilog Information line per write. Done when: the test prints the time and a Serilog test logger asserts the line.
- [ ] Record in `docs/dev/imago/psd.md` that opening the written files in Photoshop itself is an operator check recorded as a risk, not a gate. Done when: the page names the risk and this section.
- [ ] Commit fixtures under `tests/fixtures/imago/psd-write/` with psd-tools 1.10 dumps and GIMP composites, and `reference.txt` naming both versions and commands. Done when: every fixture carries its note.
- [ ] Commit: `"imago: PSD and PSB structure writing on the shared writer"`

**Test checkpoint:** Format fidelity proof: each written fixture under `tests/fixtures/imago/psd-write/` reads back through psd-tools 1.10 (layer tree dump equal), `gimp-console-3.2` (composite within 1/255), and the moved reader, including the 40,000 px wide PSB, reported by `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~Psd"`. Cheaper substitute that fails: a composite-only PSD, which the layer tree dump catches.

## 13. PSD Write: Live Content and Editability Options

A PSD that rasterizes every adjustment, style, and text layer cannot be edited further, and a PSD that writes everything live may not look identical in every reader. This section writes adjustment and fill layers, layer styles, text engine data, smart objects, comps, vector masks, and blend ranges as live blocks, with rendered pixels beside each for readers that ignore them, and gives the user Affinity's editability-versus-accuracy choice and Photoshop's compatibility settings, with an export report of everything rasterized. Catalog: IP-1734 to IP-1736 (3 features: compatibility and smallest file size, editability versus accuracy, and PSD save preferences).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/psd-options/`.
**Job:** a designer sends a PSD a Photoshop user can keep editing, or one that looks exactly right. Consumer: Photoshop, Affinity, GIMP, and psd-tools reading the file.
**Treatment:** a PSD options page with Preserve Editability and Preserve Accuracy presets, per-class rasterize switches, maximize compatibility (Always, Ask, Never), disable compression, smallest file size, and an export report. Cheaper substitute that fails the checkpoint: rasterizing every live layer.
**Chrome:** consume the §1 options shell and the moved writer. Do not add a second descriptor encoder.

**Requires:** display-session -- the options page and report need an interactive desktop

**Freeze check:** Live-content PSD saves write through `AtomicFileWriter`; the export report is shown before writing when anything will be rasterized and Cancel writes nothing; a failed write leaves any existing target byte-identical; the open document is never changed by a PSD save. Fixture source: `tests/fixtures/imago/psd-live/` (created by this section).

- [ ] Add an action-descriptor encoder in `src/Photon.Core/Formats/Psd/Descriptors/DescriptorWriter.cs` (the object, list, enum, unit float, and reference types the specification defines), with the decoder §3 needs beside it. Done when: `DescriptorTests` round-trip every type byte-identically.
- [ ] Write adjustment layers (`D03 T11 §1`) as `levl`, `curv`, `brit`, `blnc`, `hue2`, `selc`, `mixr`, `grdm`, `phfl`, `expA`, `vibA`, `blwh`, `clrL`, `nvrt`, `post`, and `thrs` blocks. Done when: psd-tools reads each block with parameters equal to the document (curve points, levels, hue ranges).
- [ ] Write fill layers as `SoCo`, `GdFl`, and `PtFl`. Done when: psd-tools reads each fill's color, gradient stops, or pattern id equal.
- [ ] Write each live layer's rendered pixels beside its block for readers that ignore the block. Done when: `gimp-console-3.2` composites every live fixture within 1/255 of Imago's render.
- [ ] Write layer styles (`D03 T09 §7`, `D03 T09 §8`) as the `lfx2` descriptor. Done when: psd-tools reads every effect's values equal to the document's.
- [ ] Write text (`D03 T16 §1`) as `TySh` with an own EngineData writer (the PostScript-like dictionary) for runs, font set, paragraph runs, and transform; attributes it cannot express are rasterized and listed in the report. Done when: psd-tools reads the text strings and font names equal to the story.
- [ ] Write smart objects (`D03 T09 §9`, `D03 T09 §10`) as `SoLd` or `PlLd` with embedded files in `lnk2` and linked files as `lnk3` entries. Done when: psd-tools extracts each embedded file byte-identical to the document's.
- [ ] Write layer comps (`D03 T09 §11`) as resource 1065. Done when: the moved reader reads every comp's name and visibility states back equal.
- [ ] Write vector masks and shape layers (`D03 T16 §7`) as `vmsk` or `vsms` with `vscg` and `vstk`, and blend ranges from `D03 T09 §5`. Done when: psd-tools reads the vector mask geometry and the blend ranges equal.
- [ ] Add `src/Photon.Core/Formats/Psd/PsdExportOptions.cs` (IP-1735) with per-class rasterize flags (layers, gradients, adjustments, effects, lines, blend ranges, text) and Affinity's Preserve Editability and Preserve Accuracy presets. Done when: a test asserts each preset's flag set and that the accuracy preset rasterizes every live class.
- [ ] Add compatibility (IP-1734): maximize compatibility Always, Ask, or Never, and smallest file size, which omits the composite. Done when: a test asserts the composite's presence for each choice.
- [ ] Add the save preferences `Imago.Formats.Psd.DisableCompression`, `Imago.Formats.Psd.MaximizeCompatibility`, and `Imago.Formats.Psd.SaveOverImported` (IP-1736), each with a default and the PSD writer as consumer. Done when: a test reads each default through `ISettingsStore`.
- [ ] Add the PSD options page in `src/Imago/Photon.Imago.Desktop/Views/Files/PsdOptionsPage.xaml` in §1's options shell with the presets, the per-class switches, and the compatibility choices. Done when: a driven save with the accuracy preset writes no live blocks and the capture shows the page. Cheaper substitute: a single "flatten" checkbox.
- [ ] Show an export report listing every rasterized item before writing and log it as one Information line. Done when: saving a fixture with an inexpressible text attribute lists it and a Serilog test logger asserts the line.
- [ ] Commit fixtures under `tests/fixtures/imago/psd-live/` with psd-tools 1.10 block dumps and GIMP composites, and `reference.txt`. Done when: every fixture carries its note.
- [ ] Assert the Imago round trip: Imago to PSD to Imago restores every live layer equal. Done when: `PsdLiveRoundTripTests` compare parameters and pixels within 1/255.
- [ ] Commit captures under `docs/captures/imago/psd-options/` and write `docs/user/imago/psd.md`. Done when: every option appears in a capture and the page documents it.
- [ ] Commit: `"imago: live adjustments, styles, text, and smart objects in written PSDs"`

**Test checkpoint:** Format fidelity proof: psd-tools 1.10 reads each written live block of the fixtures under `tests/fixtures/imago/psd-live/` with parameters equal to the document (curve points, style values, text strings and fonts, smart object bytes), `gimp-console-3.2` composites within 1/255, and `PsdLiveRoundTripTests` restore the live layers equal, all under `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~Psd"`. Cheaper substitute that fails: rasterized adjustments, which the psd-tools block assertion catches.

## 3. PSD Read Fidelity: Live Adjustments, Styles, Text, and Smart Objects

`D03 T04 §5` reads PSD structure and rasterizes what Imago could not yet hold, with an honest report. Now Imago holds all of it, so this section maps every block §13 writes back to live layers, in every mode and depth, and the import report shrinks to what Imago genuinely lacks (3D, video, unknown blocks). Affinity's own PSD export with Preserve Editability is the interop path for Affinity files (backlog B-045), so Affinity-made fixtures are part of the proof. Catalog: IP-1737 to IP-1740 (4 features: PSD import with live text and smart objects, PSD read fidelity across layers, masks, paths, guides, styles, and multichannel, PSD import options, and smart objects as editable placed documents).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/psd-import/`.
**Job:** a Photoshop or Affinity composition opens editable. Consumer: the opened document's layers.
**Treatment:** a PSD import options dialog (smart objects embedded or rasterized, text editable or pixels, remember choice) and the shrinking import report. Cheaper substitute that fails the checkpoint: stored pixels for every live layer.
**Chrome:** consume the moved reader, the descriptor decoder of §13, the moved `FontSubstitutionService`, and §1's registry. Do not add a second PSD parser.

**Requires:** display-session -- the import dialog needs an interactive desktop

- [ ] Extend the moved `PsdReader` and the Imago adapter to map every block §13 writes (adjustment and fill layers, `lfx2`, `TySh`, `SoLd`, `PlLd`, comps, `vmsk`, `vsms`, blend ranges) back to live layers. Done when: `PsdReadLiveTests` import the §13 fixtures and every live layer kind is restored.
- [ ] Read legacy `lrFX` effects into the same layer styles. Done when: a legacy-effects fixture imports its drop shadow live.
- [ ] Add an own EngineData parser into a `TextStory` (IP-1737), matching fonts through the moved `FontSubstitutionService` and reporting unknown fonts. Done when: text strings and font names equal the fixture's psd-tools EngineData dump.
- [ ] Open embedded `lnk2` smart objects (IP-1740) through §1's registry as editable placed documents, and linked files as `D03 T09 §10` links. Done when: an embedded PSD smart object opens for editing and saving it updates the parent layer.
- [ ] Read layers, groups, masks, paths, guides, styles, comps, fill layers, and vector masks (IP-1738). Done when: each fixture's layer tree equals its psd-tools dump.
- [ ] Read modes bitmap, gray, indexed, RGB, CMYK, Lab, duotone (through `D01 T04 §3`), and multichannel, at depths 1, 8, 16, and 32. Done when: each mode and depth fixture composites within 2/255 of the psd-tools composite.
- [ ] Read PSB (version 2 with 8-byte lengths). Done when: the 40,000 px wide §2 fixture imports with its layer tree.
- [ ] Add the PSD import options dialog (IP-1739) under `Imago.Formats.Psd.Import.*`: smart objects embedded or rasterized, text editable or pixels, and remember choice. Done when: with text set to pixels, text layers import as pixel layers, and remember choice skips the dialog next time. Cheaper substitute: no options.
- [ ] Shrink the import report to what Imago cannot hold (3D, video, unknown blocks), shown once and logged as one Information line. Done when: a fixture with a video layer lists only that layer in the report.
- [ ] Commit fixtures from Photoshop 27.10, Photopea, and Affinity by Canva 3.3 (tool and version recorded per file) under `tests/fixtures/imago/psd-import/`, each with its psd-tools composite and EngineData dump. Done when: every fixture carries `reference.txt`.
- [ ] Assert Affinity interop: fixtures exported from Affinity 3.3 with Preserve Editability open with their adjustments live. Done when: `PsdReadLiveTests.AffinityPreserveEditability` passes.
- [ ] Commit captures under `docs/captures/imago/psd-import/` and extend `docs/user/imago/psd.md` with import. Done when: the dialog and the report appear in captures and the page documents them.
- [ ] Commit: `"imago: PSD import with live adjustments, styles, text, and smart objects"`

**Test checkpoint:** Format fidelity proof: the fixtures under `tests/fixtures/imago/psd-import/` import with each layer's composite within 2/255 of the psd-tools composite and text strings and font names equal to its EngineData dump, reported by `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~PsdRead"`. Cheaper substitute that fails: stored pixels only, which the live-layer-kind assertion catches.

## 4. GIMP XCF Read

GIMP's XCF is fully documented and GIMP is the oracle, so Imago reads it with its own code from `devel-docs/XCF.md`, every version and precision GIMP 3.2 writes, restoring layers, groups, masks, channels, paths, guides, parasites, text, GIMP 3.2's link and vector layers, and its non-destructive filter stacks as live filters. GIMP is GPL-3.0-or-later, so translated logic is compatible. Catalog: IP-1741 (1 feature: GIMP XCF read and write including compressed XCF and saved filter stacks; §14 is its write half).

**Fidelity:** no surface of its own (XCF appears in §1's format list; the import report is §1's)

- [ ] Add `src/Imago/Photon.Imago.FileFormats/Xcf/XcfReader.cs` from `devel-docs/XCF.md` at the GIMP 3.2.6 tag (tag recorded in the file header): versions 0 through the version GIMP 3.2 writes, with 32-bit and 64-bit offsets. Done when: `XcfReaderTests` read the header and property list of one fixture per version.
- [ ] Read precisions 8, 16, and 32-bit integer, half, float, and double in linear or perceptual encoding. Done when: each precision fixture reads within 1/255 (1e-4 for float) of GIMP's own PNG or EXR export.
- [ ] Read compression none, RLE, and zlib, re-tiling GIMP's 64 px tiles into Imago's 256 px tiles. Done when: each compression fixture composites within 1/255.
- [ ] Read layers, groups (item paths), and layer masks. Done when: the layer tree equals a Script-Fu dump of the fixture.
- [ ] Read channels (the selection and saved channels with color and opacity) into `D03 T10 §10` channels. Done when: a fixture's saved channel imports with its color and opacity.
- [ ] Read paths (legacy and current) into the `D03 T16 §5` path set. Done when: path geometry matches the Script-Fu dump within 1e-6.
- [ ] Read guides, sample points, the grid, and resolution. Done when: each equals the Script-Fu dump.
- [ ] Read the `icc-profile`, comment, and `gimp-image-metadata` parasites, keeping every unknown parasite for §14. Done when: the profile bytes equal the fixture's and an unknown parasite survives in the document model.
- [ ] Map GIMP legacy and default layer modes to Imago blend modes, reporting unmapped modes by name. Done when: a one-layer-per-mode fixture maps every mode or names it in the report.
- [ ] Read the `gimp-text-layer` parasite (markup) into `D03 T16 §1` text layers, keeping pixels and reporting when a font is missing. Done when: a text fixture imports its string and font live, and a missing-font fixture imports pixels with a report line.
- [ ] Read GIMP 3.2 link layers into `D03 T09 §10` linked layers and vector layers into `D03 T16 §11`. Done when: both fixtures import live.
- [ ] Read GIMP 3 non-destructive filter stacks into `D03 T14 §1` live filters through the `D01 T06 §1` GEGL op-id map; unknown ops stay as pixels with a report line. Done when: a fixture with a Gaussian blur filter imports a live blur with equal parameters.
- [ ] Open compressed XCF (`.xcf.gz`, `.xcf.bz2`, `.xcf.xz`) through §12's archive readers. Done when: each compressed fixture composites like the uncompressed one.
- [ ] Register XCF read with §1's registry, returning the import report. Done when: File, Open lists XCF.
- [ ] Commit fixtures produced by committed `gimp-console-3.2` batch scripts per version and precision under `tests/fixtures/imago/xcf/`, with GIMP's PNG exports and Script-Fu layer tree dumps and `reference.txt`. Done when: rerunning the scripts reproduces the dumps.
- [ ] Commit: `"imago: read GIMP XCF with layers, text, vector layers, and filter stacks"`

**Test checkpoint:** Format fidelity proof: the fixtures under `tests/fixtures/imago/xcf/` import with the composite within 1/255 of GIMP's own PNG export (1e-4 for float) and a layer tree equal to the Script-Fu dump, reported by `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~Xcf"`. Cheaper substitute that fails: the flattened preview, which the layer tree check catches.

## 14. GIMP XCF Write

Imago writes XCF with the same structures §4 reads, choosing the lowest version that holds the features used as GIMP does, with a choice between GIMP 2.10 and 3.x compatibility. Imago-only content (adjustment layers, styles, smart objects) writes as pixels plus `imago-*` parasites, so GIMP shows pixels and Imago restores the live layers. Catalog: owns no catalog rows (IP-1741, owned by §4, covers read and write; this section is its write half).

**Fidelity:** no surface of its own (XCF write options are option descriptors that §1's options shell renders)

**Freeze check:** XCF saves write through `AtomicFileWriter`; a failed or interrupted write leaves any existing target byte-identical; a GIMP 2.10 compatibility save shows its rasterization report before writing and Cancel writes nothing; the open document is never changed by an XCF save. Fixture source: `tests/fixtures/imago/xcf-write/` (created by this section).

- [ ] Add `src/Imago/Photon.Imago.FileFormats/Xcf/XcfWriter.cs` writing layers, groups, masks, channels, paths, guides, sample points, grid, resolution, and parasites, with zlib compression by default and RLE as an option. Done when: `gimp-console-3.2` opens each written fixture with the layer tree equal to the document.
- [ ] Write the lowest XCF version that holds the features used (GIMP's rule). Done when: a plain raster document writes a version GIMP 2.10 reads, and a document with a vector layer writes the 3.x version.
- [ ] Add `Imago.Formats.Xcf.Compatibility` (GIMP 2.10 or GIMP 3.x, default 3.x); 2.10 rasterizes link layers, vector layers, and filter stacks with a report. Done when: a 2.10 save of the vector fixture lists the rasterized layer in the report.
- [ ] Write text layers as the `gimp-text-layer` parasite with rendered pixels. Done when: GIMP 3.2 opens the text layer editable.
- [ ] Write adjustment layers, styles, and smart objects as pixels plus `imago-*` parasites per the `D03 T08 §1` contract. Done when: an Imago round trip restores each live layer from its parasite.
- [ ] Write back every unknown parasite §4 read, unchanged. Done when: a round trip of a fixture with an unknown parasite keeps its bytes.
- [ ] Register XCF write, with the compression and compatibility option descriptors, in §1's registry. Done when: Save a Copy lists XCF with both options.
- [ ] Log one Serilog Information line per XCF write (version, compression, layers, milliseconds). Done when: a Serilog test logger asserts the line.
- [ ] Record in `docs/dev/imago/xcf.md` that Nodus's XCF import (`D02 T18 §9`, promoted from backlog B-038 on 2026-09-27) moves §4's decoding core to `Photon.Core` and consumes it, while this writer stays in Imago. Done when: the page names `D02 T18 §9`, §4, and this section.
- [ ] Commit fixtures under `tests/fixtures/imago/xcf-write/` with `reference.txt` naming `gimp-console-3.2` and, where installed, `gimp-console-2.10`. Done when: every fixture carries its note.
- [ ] Commit: `"imago: write GIMP XCF with a compatibility choice"`

**Test checkpoint:** Format fidelity proof: written fixtures open in `gimp-console-3.2` and, where installed, `gimp-console-2.10` (skipped naming the missing version otherwise) with the layer tree equal and the composite within 1/255, and the Imago round trip restores live content from the parasites, reported by `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~XcfWrite"`. Cheaper substitute that fails: always writing the newest version, which the GIMP 2.10 open test catches.

## 5. Modern Web Formats: WebP, AVIF, HEIF, JPEG XL, JPEG 2000, QOI, JPEG XR

The modern web and camera formats each have a reference library, and the WIC Store extensions many Windows machines lack are not a dependable substitute, so Imago ships the reference libraries natively per RID with a GPL-3.0 check and a decisions row each. HEIC depth maps become develop depth sources and gain-map HDR files open as 32-bit documents. This promotes backlog B-022, whose PSD-write part lands in §2 and §13, EXR in §6, and GIF in §8; animation stays backlog B-044. Catalog: IP-1742 to IP-1753 (12 features: WebP, AVIF, HEIF and HEIC, HEJ2, JPEG XL, JPEG 2000 JP2, JPEG 2000 codestream, JPEG XR open, QOI, WebP lossless export, gain-map HDR open, and HEIC depth-map refinement). -> SOURCE: legacy-imago-7.2-7.3

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/web-formats/`.
**Job:** a user opens and exports every modern web and camera format with the options its reference encoder offers. Consumer: browsers, phones, and the other tools reading the files.
**Treatment:** one options page per format in §1's shell with a live size estimate. Cheaper substitute that fails the checkpoint: the WIC Store extensions many machines lack.
**Chrome:** consume the registry, the atomic writer, and the native loader. Do not add a second native loading path.

**Requires:** display-session -- the options pages need an interactive desktop

**Freeze check:** Every writer here saves through `AtomicFileWriter`; a failed or interrupted encode leaves any existing target byte-identical; a lossy format shows its flatten or depth notice before writing and Cancel writes nothing; the open document is never changed by an export. Fixture source: `tests/fixtures/imago/web-formats/` (created by this section).

- [ ] Build libwebp 1.5, libavif 1.2 with dav1d and libaom, libheif 1.19 with libde265 and x265, libjxl 0.11, and OpenJPEG 2.5 for `win-x64` and `win-arm64` with `build/native/<lib>/build.ps1` scripts recording source hashes in `SOURCE.txt` (the lcms2 pattern of `D01 T04 §1`), committed under `src/Photon.Core/runtimes/<rid>/native/`. Done when: every DLL exists for both RIDs and each `SOURCE.txt` names the upstream tag and hash.
- [ ] Add each library's license to `src/Photon.Core/THIRD-PARTY-NOTICES.md` and one `docs/dev/decisions.md` row per library with its GPL-3.0 check, recording the HEVC patent exposure for libde265 and x265 and kvazaar as the alternative encoder. Done when: every row names its license and this section.
- [ ] Add `src/Photon.Core/Formats/Native/NativeCodecLoader.cs` that loads each library on first use and refuses a missing one by name ("AVIF needs avif.dll, which is missing from this installation"). Done when: `NativeCodecLoaderTests` delete a DLL in a test folder and assert the refusal names it.
- [ ] Add WebP decode (IP-1742) through SkiaSharp's bundled libwebp as Nodus does. Done when: decoding the fixtures matches `dwebp` output within 1/255 (bit-exact for lossless).
- [ ] Add WebP encode (IP-1742, IP-1751) through libwebp P/Invoke: lossy or lossless, quality, alpha quality, preset, sharp YUV, and method, with EXIF, XMP, and ICC chunks; animation is backlog B-044. Done when: written files decode in `dwebp` exactly for lossless and within a stated PSNR for lossy.
- [ ] Add AVIF decode and encode (IP-1743) through libavif: lossless, quality, 4:4:4, 4:2:2, or 4:2:0, 8, 10, or 12 bit, speed, and metadata. Done when: fixtures decode within 1/255 of `avifdec` and written files decode in `avifdec` within the stated PSNR.
- [ ] Add AVIF HDR: PQ and HLG through CICP from and to `D03 T15 §4` 32-bit documents. Done when: a PQ fixture opens into a 32-bit document with its CICP values read back.
- [ ] Add HEIF and HEIC decode and encode (IP-1744) through libheif: quality, chroma, depth, speed, and metadata. Done when: fixtures decode within 1/255 of `heif-dec`.
- [ ] Open the HEIC depth-map auxiliary image (IP-1753) as a layer or as a `D01 T07 §4` depth source, refined on import with the `D03 T10 §6` guided filter. Done when: a depth fixture imports a depth layer whose edges align with the image within 2 px after refinement.
- [ ] Add HEJ2 export (IP-1745) through libheif's OpenJPEG plugin. Done when: a written HEJ2 decodes in `heif-dec` within the stated PSNR.
- [ ] Add JPEG XL decode and encode (IP-1746) through libjxl: lossless, distance, effort, bit depth, CMYK through the K extra channel, and metadata boxes. Done when: fixtures decode within 1/255 of `djxl` and lossless writes decode exactly.
- [ ] Add JPEG 2000 JP2 (IP-1747) through OpenJPEG: lossless, quality layers, ICT, resolutions, progression orders, cinema 2K and 4K profiles, tiles, ROI, CMYK, and metadata. Done when: fixtures decode within 1/255 of `opj_decompress`.
- [ ] Add the J2K codestream (IP-1748) and reconcile with `D02 T14 §12`: if Nodus chose OpenJPEG, move its binding to `src/Photon.Core/Formats/Jpeg2000/`; otherwise switch Nodus's JP2 path to this one. Done when: `grep -rn "opj_decode\|OpenJpeg" src --include=*.cs` shows one binding.
- [ ] Add JPEG XR decode (IP-1749) through WIC's built-in decoder, including half and float HDR into `D03 T15 §4` 32-bit documents. Done when: a float JPEG XR fixture opens as 32-bit with values within 1e-3 of the WIC reference decode.
- [ ] Add an own QOI codec (IP-1750) from the QOI 1.0 specification in `src/Photon.Core/Formats/Qoi/`. Done when: the reference test images round-trip bit-exactly.
- [ ] Open gain-map HDR files (IP-1752): Ultra HDR JPEG (MPF plus `hdrgm` XMP, ISO 21496-1) and HEIF gain maps into a 32-bit document or shown through `D03 T15 §4`. Done when: an Ultra HDR fixture reconstructs HDR values within 1 percent of the libultrahdr reference decode.
- [ ] Add one options page per format in §1's shell with a live size estimate from a real encode. Done when: the estimate equals the written file's byte count for each format.
- [ ] Register every codec with §1's registry and log one Serilog Information line per read and write. Done when: File, Open lists each format and a Serilog test logger asserts the lines.
- [ ] Commit fixtures under `tests/fixtures/imago/web-formats/` with `reference.txt` naming `dwebp`, `avifdec`, `heif-dec`, `djxl`, and `opj_decompress` with versions. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/web-formats/` and write `docs/user/imago/web-formats.md`. Done when: every options page appears in a capture and the page documents it.
- [ ] Commit: `"imago: WebP, AVIF, HEIF, JPEG XL, JPEG 2000, JPEG XR, and QOI"`

**Test checkpoint:** Format fidelity proof: each format's fixtures under `tests/fixtures/imago/web-formats/` decode within 1/255 (bit-exact for lossless) of the reference CLI (`dwebp`, `avifdec`, `heif-dec`, `djxl`, `opj_decompress`), and written files decode in the same CLI within the stated PSNR or exactly for lossless, reported by `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~WebFormats"`; `NativeCodecLoaderTests` assert the missing-native refusal. Cheaper substitute that fails: the WIC Store extensions, which the refusal test on a clean machine exposes.

## 6. HDR and Scientific Formats

VFX, astronomy, and medical users bring formats where every bit and every channel matters: OpenEXR with every compression and multipart layers, Radiance, PFM, the PNM family, float TIFF, FITS with Bayer data, and DICOM. OpenEXR ships natively; the small formats are own managed codecs; DICOM is an own reader because fo-dicom's MS-PL license is GPL-incompatible. HDR output adds gain-map JPEG and HDR PNG, whose chunk writer this section starts and §11 extends. Catalog: IP-1754 to IP-1771 (18 features: EXR alpha and multichannel options, HDR gain maps and CICP output, EXR compression and precision, Radiance HDR, PFM, the PNM family, float TIFF with the predictor, FITS, DICOM, Photoshop Raw, EXR and TIFF compression choices, EXR color space from filename, EXR per-channel precision, the EXR color space conversion on import, EXR alpha options, multichannel EXR as layers, FITS with Bayer, and multi-file DICOM).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/hdr-formats/`.
**Job:** a VFX, astronomy, or medical user opens and writes their formats with the options their tools expect. Consumer: compositors, astronomy software, and PACS viewers reading the files.
**Treatment:** EXR, FITS, DICOM, and raw data import and export option pages in §1's shell. Cheaper substitute that fails the checkpoint: EXR through an 8-bit path.
**Chrome:** consume the registry, the `D03 T15 §4` 32-bit documents, and the `D03 T11 §4` OCIO wrapper. Do not add a second float pipeline.

**Requires:** display-session -- the option pages need an interactive desktop

**Freeze check:** Every writer here saves through `AtomicFileWriter`; a failed or interrupted write leaves any existing target byte-identical; DICOM anonymize writes only to a new file and never to the opened one; the open document is never changed by an export. Fixture source: `tests/fixtures/imago/hdr-formats/` (created by this section).

- [ ] Build OpenEXR 3.3 and Imath per RID with `build/native/openexr/build.ps1` (source hash in `SOURCE.txt`), binding its C API (`openexr_core`) in `src/Photon.Core/Formats/Exr/`, with a BSD-3-Clause notice and a `docs/dev/decisions.md` row. Done when: both RIDs' DLLs are committed and the row names the license.
- [ ] Read and write scanline and tiled EXR with compressions none, RLE, ZIP, ZIPS, PIZ, PXR24, B44, B44A, DWAA, and DWAB (IP-1756, IP-1764). Done when: one fixture per compression decodes within 1e-4 of `oiiotool` and each write re-reads equal per channel.
- [ ] Write half or float per channel class (IP-1766) and an export precision choice. Done when: a test asserts the pixel type per channel in the written header.
- [ ] Read and write multichannel and multipart EXR as layers (IP-1754, IP-1769). Done when: a four-part fixture opens as four layers named after its parts and writes back with equal part names.
- [ ] Add alpha associate, unpremultiply, and perturb zero alpha (IP-1768). Done when: a test asserts each option's effect on a pixel with zero alpha and nonzero color.
- [ ] Add EXR color space from a filename affix (IP-1765, IP-1767) through the `D03 T11 §4` OCIO wrapper's configuration (the suite configuration choice of `D03 T18 §10` applies once it lands), converting on import and export. Done when: `plate_acescg.exr` converts to the working space within 1e-4 of `ociocheck` or `oiiotool --colorconvert`.
- [ ] Add own Radiance HDR RGBE with RLE (IP-1757) in `src/Photon.Core/Formats/Radiance/`. Done when: fixtures decode within 1e-4 of `oiiotool` and round trips re-read equal.
- [ ] Add own PFM (IP-1758). Done when: round trips are exact.
- [ ] Add own PBM, PGM, PPM, and PAM, binary and ASCII, with 16-bit maxval (IP-1759). Done when: round trips are exact for every variant.
- [ ] Verify whether WIC honors the TIFF floating-point predictor (predictor 3); if not, add `src/Imago/Photon.Imago.FileFormats/Tiff/TiffFloatPredictor.cs` applying it on read and write, recorded in `docs/dev/decisions.md` (IP-1760). Done when: a float TIFF with predictor 3 reads within 1e-6 of `oiiotool` and the decision row quotes the verification.
- [ ] Add HDR output for 32-bit documents (IP-1755): Ultra HDR gain-map JPEG and 16-bit PQ PNG with cICP, mDCV, and cLLI through a new `src/Photon.Core/Formats/Png/PngWriter.cs` core that §11 extends with the full option set. Done when: `pngcheck` 3.0 validates the cICP chunk and an Ultra HDR decoder reconstructs the HDR values within 1 percent.
- [ ] Add FITS 4.0 read (IP-1761): the primary HDU and image extensions, BITPIX 8, 16, 32, -32, and -64, BZERO and BSCALE, with header cards kept as metadata. Done when: fixtures decode within 1e-4 of `oiiotool` and every header card is readable in File Info.
- [ ] Add `BAYERPAT` debayering (bilinear) for FITS (IP-1770). Done when: an RGGB fixture debayers within 1/255 of its committed golden.
- [ ] Add FITS export with BITPIX choice and header cards. Done when: an exported FITS re-reads with equal values and cards.
- [ ] Add an own DICOM PS3.10 reader (IP-1762) for implicit and explicit VR little endian, big endian, JPEG baseline, JPEG lossless process 14 (own decoder), and RLE lossless; fo-dicom is not used (MS-PL is GPL-incompatible), recorded in `docs/dev/decisions.md`. Done when: each transfer-syntax fixture matches dcmtk 3.6 `dcm2pnm` within 1/255 at the same window.
- [ ] Open DICOM frames as layers and overlays (60xx) as a layer, with window width and level. Done when: a multi-frame fixture opens one layer per frame and the window matches `dcm2pnm`.
- [ ] Add DICOM anonymize per the PS3.15 Basic Profile and Secondary Capture export. Done when: an anonymized export has none of the profile's identifying tags, asserted by re-reading it.
- [ ] Load multiple DICOM files into one document ordered by Instance Number (IP-1771). Done when: three shuffled files load as three layers in instance order.
- [ ] Add Photoshop Raw (IP-1763): header size, planar or interleaved, byte order, and GIMP's palette layouts. Done when: round trips are exact for each layout.
- [ ] Add the EXR, FITS, DICOM, and raw data option pages in §1's shell. Done when: the capture shows each page and each option reaches its codec.
- [ ] Register every codec with §1's registry, register FITS as an astro frame source for `D03 T15 §10` (whose FITS refusal is removed), and log one Serilog Information line per read and write. Done when: File, Open lists each format and the astro frame source test of `D03 T15 §10` accepts a FITS frame.
- [ ] Commit fixtures under `tests/fixtures/imago/hdr-formats/` with `reference.txt` naming OpenImageIO 3.0 `oiiotool` and dcmtk 3.6 `dcm2pnm` with commands. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/hdr-formats/` and write `docs/user/imago/hdr-scientific-formats.md`. Done when: every page appears in a capture and the page documents it.
- [ ] Commit: `"imago: OpenEXR, Radiance, PFM, PNM, FITS, DICOM, and raw data"`

**Test checkpoint:** Format fidelity proof: EXR, HDR, PFM, and FITS fixtures under `tests/fixtures/imago/hdr-formats/` decode within 1e-4 of OpenImageIO 3.0 `oiiotool` output and written files re-read equal per channel; DICOM fixtures match dcmtk 3.6 `dcm2pnm` within 1/255 at the same window; PNM round trips are exact; all reported by `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~HdrFormats"`. Cheaper substitute that fails: one EXR compression, which the per-compression fixtures catch.

## 7. Document Formats: PDF Import, Photoshop PDF, and PDF Export

Print shops receive PDF, and designers bring PDF to rasterize. Imago rasterizes PDF with PDFium (the reference rasterizer; Nodus's PdfPig path builds vector objects, a different job) and writes Photoshop PDF on the PDF, PostScript, metafile, and printer-marks code Nodus built (`D02 T13 §4`, `D02 T13 §10`, `D02 T13 §14` to `D02 T13 §16`, `D02 T14 §9`, `D02 T14 §11`), each moved into `Photon.Core` here as its second consumer. This section also enables the PDF half of §1's vector routing and the PDF page picker §15 deferred to it. PostScript, EPS, AI, SVG, and metafiles are §16's, split from this section on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. Catalog: IP-1772, IP-1773, IP-1775 to IP-1780, IP-1786 to IP-1792, and IP-1795 (16 features: PDF import options and import, Photoshop PDF save, the PDF presets manager, PDF compression, PDF output color, PDF security, PDF export options, PDF export compatibility and PDF/X, PDF export color and spots, optional content layers, fonts and links, printer marks, passwords and permissions, the rasterization policy, and the presets manager as Affinity's row).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/pdf-import/` and `docs/captures/imago/pdf-export/`.
**Job:** a user rasterizes PDF pages in and sends print-ready PDF out. Consumer: print shops, PDF readers, and preflight tools.
**Treatment:** a PDF import dialog (pages with thumbnails or images, crop box, size, resolution, mode, reverse, anti-aliasing, fill transparent, editable text), and a Save Adobe PDF dialog with a presets manager and General, Compression, Output, Security, Marks, and Summary pages. Cheaper substitute that fails the checkpoint: `SKDocument` PDF output.
**Chrome:** consume the moved writer, presets, standards enforcer, security handler, and printer-marks renderer, the `D01 T04 §1` output intents, and §1's registry. Do not add a second PDF writer.

**Requires:** display-session -- the dialogs and captures need an interactive desktop

**Freeze check:** Photoshop PDF and PDF saves write through `AtomicFileWriter`; a failed or interrupted write leaves any existing target byte-identical; passwords never reach presets, settings, or logs; importing a PDF never opens the source for writing. Fixture source: `tests/fixtures/imago/pdf/` (created by this section).

- [ ] Move first: the PDF writer of `D02 T13 §14` (`PdfContentWriter`, `PdfResourceBuilder`, `TrueTypeSubsetter`), its presets and standards of `D02 T13 §15` (`PdfPresetStore`, `PdfStandardEnforcer`), and its security of `D02 T13 §16` into `src/Photon.Core/Pdf/`, repointing Nodus. Done when: `grep -rn "class PdfContentWriter\|class PdfPresetStore" src` prints one path each, under `src/Photon.Core/`, and Nodus's PDF tests pass.
- [ ] Move `GhostscriptBridge` (`D02 T14 §9`) and `PostScriptWriter` (`D02 T13 §10`) into `src/Photon.Core/Formats/PostScript/`, the EMF and WMF readers and writers of `D02 T14 §11` into `src/Photon.Core/Formats/Metafile/`, and `PrinterMarksRenderer` (`D02 T13 §4`) into `src/Photon.Core/Print/` for `D03 T18 §6`, repointing Nodus. Done when: one definition of each remains and Nodus's tests pass.
- [ ] Add PDFium through a thin `LibraryImport` P/Invoke (`FPDF_LoadMemDocument`, `FPDF_RenderPageBitmapWithMatrix`) in `src/Photon.Core/Pdf/Import/`, built per RID with `SOURCE.txt`, with BSD-3-Clause and Apache-2.0 notices and a `docs/dev/decisions.md` row. Done when: the row names both licenses and a missing DLL is refused by name through `NativeCodecLoader`.
- [ ] Add the PDF import dialog (IP-1772, IP-1773): pages with thumbnails or embedded images; media, crop, bleed, trim, or art box; size, resolution, mode, reverse order, anti-aliasing, fill transparent; and a password prompt for encrypted files. Done when: imports match `pdfium_test --png` at the same DPI within 1/255 and a wrong password is refused by name.
- [ ] Import editable text from PdfPig text positions as `D03 T16 §1` text layers above the page (IP-1772). Done when: a one-line PDF imports a text layer whose string equals the PDF text.
- [ ] Add the Save Adobe PDF dialog General page (IP-1775): presets, PDF/X-1a, X-3, and X-4, compatibility 1.4 to 2.0, preserve editing (the `.imago` package embedded as an attachment Imago reopens live), thumbnails, fast web view (linearized when the writer supports it, otherwise refused by name and recorded), and a Summary page. Done when: a preserve-editing PDF reopens in Imago with its layers live.
- [ ] Add the PDF presets manager (IP-1776, IP-1795) on the moved `PdfPresetStore`: create, edit, import, export, and delete. Done when: a user preset round-trips through export and import.
- [ ] Add the Compression page (IP-1777): downsampling, ZIP, JPEG, JPEG 2000 through §5's OpenJPEG, and 16 to 8 bit. Done when: PdfPig reads each image's filter as chosen.
- [ ] Add the Output page (IP-1778): color conversion, profile inclusion, and output intent through `D01 T04 §1`. Done when: PdfPig reads the output intent's profile bytes equal to the chosen profile.
- [ ] Add the Security page (IP-1779, IP-1791): open password, permissions password and permissions, and AES-256 through the moved security handler. Done when: PdfPig refuses the file without the password and reads the permission bits with it.
- [ ] Add PDF export options (IP-1780): layers as pages, reverse order, root layers only, apply masks, vectorize text and shape layers, omit hidden layers, fill transparent, text as image, and open when complete. Done when: a three-layer fixture exported as pages yields three pages in the chosen order.
- [ ] Add export compatibility and the PDF/X standards (IP-1786) enforced by the moved `PdfStandardEnforcer`. Done when: the enforcer's rule tests pass on a PDF/X-4 export.
- [ ] Add spot colors and overprint black (IP-1787) through `D01 T04 §1`, writing Separation color spaces. Done when: PdfPig reads the Separation names equal to the document's spot channels.
- [ ] Add layers as optional content (IP-1788). Done when: PdfPig reads one optional content group per layer with the layer names.
- [ ] Add embed and subset fonts, text as curves, and hyperlinks and bookmarks (IP-1789). Done when: PdfPig reads a subset font for a text layer and a bookmark per artboard.
- [ ] Add printer marks (IP-1790) through `PrinterMarksRenderer`: crop, registration, color bars, and page information. Done when: the marks render as vector paths in the MuPDF `mutool draw` golden within 1 percent of pixels.
- [ ] Add the rasterization policy for PDF, SVG, and EPS output (IP-1792): raster DPI, rasterize nothing, everything, or unsupported, and downsample images. Done when: a test asserts a vector shape stays a path under "nothing" and becomes an image under "everything".
- [ ] Register the PDF reader and the Photoshop PDF and PDF writers with §1's registry, enabling §1's vector routing for PDF, §15's PDF page picker for Place, and PDF placement in `D03 T09 §9`, removing each tooltip. Done when: File, Open on a PDF opens this section's dialog, placing a PDF shows the page picker, and the owning sections' disabled-state tests are updated to assert the enabled controls and pass.
- [ ] Log one Serilog Information line per PDF import and export with format, pages, and milliseconds, never a password. Done when: a Serilog test logger asserts the line and a password-leak test finds no password in logs, settings, or presets.
- [ ] Commit fixtures under `tests/fixtures/imago/pdf/` with `reference.txt` naming `pdfium_test` and MuPDF `mutool draw` with versions and commands. Done when: every fixture carries its note.
- [ ] Record in `docs/dev/imago/pdf.md` that Acrobat preflight of PDF/X output is an operator check recorded as a risk, not a gate. Done when: the page names the risk and this section.
- [ ] Commit captures under `docs/captures/imago/pdf-import/` and `pdf-export/`, and write `docs/user/imago/pdf-eps.md` with its PDF pages. Done when: every dialog page appears in a capture and the page documents it.
- [ ] Commit: `"imago: PDF import, Photoshop PDF, and PDF export on the shared writer"`

**Test checkpoint:** Format fidelity proof: PDF imports match `pdfium_test --png` at the same DPI within 1/255; written PDFs read back with PdfPig (optional content names, output intent, Separation names, encryption) and render against MuPDF `mutool draw` goldens within 1 percent of pixels; PDF/X conformance is proven by the moved enforcer's rule tests; Nodus's PDF, PostScript, and metafile tests pass after the moves; all under `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~Pdf"`. Cheaper substitute that fails: `SKDocument`, which has no Separation color space or optional content.

## 8. Common and Legacy Raster Formats I

Icons, cursors, textures, and the X11 and workstation formats are small and documented, and WIC lacks most of them, so Imago reads and writes them with own codecs, Nodus's raster codecs (`D02 T14 §12`) moved into `Photon.Core` as their second consumer, and the ICO, CUR, and XPM codecs `D01 T08 §3` and `D01 T08 §1` already put there; DDS block compression uses BCnEncoder.Net (MIT). Animated GIF is backlog B-044. Catalog: IP-1796 to IP-1813 (18 features: BMP, single-frame GIF, ICO, CUR, ANI, ICNS, DDS, DDS mipmaps, TGA, PCX and DCX, XBM, XPM, XWD, Sun raster, SGI, farbfeld, WBMP, and the GIMP 3 format additions).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/legacy-formats/`.
**Job:** a user opens and writes icon, texture, and legacy raster files with their format's options. Consumer: the apps, engines, and systems reading the files.
**Treatment:** one options page per writable format in §1's shell (BMP, GIF, ICO, CUR, ANI, DDS, TGA, XBM, SGI, Sun). Cheaper substitute that fails the checkpoint: routing everything through WIC, which lacks most of these.
**Chrome:** consume the registry, the moved codecs, and the `D01 T08 §1` and `D01 T08 §3` codecs. Do not add a second TGA, PCX, ICO, CUR, or XPM codec.

**Requires:** display-session -- the option pages need an interactive desktop

**Freeze check:** Every writer here saves through `AtomicFileWriter`; a failed or interrupted write leaves any existing target byte-identical; an indexed or 1-bit target shows its conversion notice before writing and Cancel writes nothing. Fixture source: `tests/fixtures/imago/legacy-formats/` (created by this section).

- [ ] Move first: `TgaCodec`, `PcxCodec`, and the OS/2 BMP shim of `D02 T14 §12` from `src/Nodus/Photon.Nodus.Core/Formats/Raster/` into `src/Photon.Core/Formats/Raster/`, repointing Nodus (its ICO and CUR codec already moved there with `D01 T08 §3`), and consume the WIC codec where `D03 T04 §1` placed it. Done when: `grep -rn "class TgaCodec\|class PcxCodec" src` prints one path each, under `src/Photon.Core/`.
- [ ] Add BMP (IP-1796): RLE4 and RLE8, V4 and V5 color space info, 16-bit 565 and 555, 24, and 32 with alpha and bitfields, OS/2, and row order. Done when: each variant matches `magick <file> rgba:` exactly and writes decode exactly.
- [ ] Add single-frame GIF (IP-1797): indexed conversion through `D01 T03 §3` and `D03 T11 §7`, interlace, and comment; animation is backlog B-044. Done when: a written GIF decodes in ImageMagick 7.1 exactly to the indexed pixels.
- [ ] Register ICO (IP-1798) through the `D01 T08 §3` codec (per-size BMP or PNG entries with PNG compression) instead of writing a second one. Done when: a multi-size ICO round-trips every entry exactly.
- [ ] Register CUR (IP-1799) through the `D01 T08 §3` codec with save type, PNG compression, and hot spot. Done when: the hot spot round-trips.
- [ ] Add ANI (IP-1800): the RIFF `anih`, `rate`, `seq`, and INFO name and author chunks, with frames as layers. Done when: an ANI fixture opens one layer per frame and its frames match GIMP 3.2's export.
- [ ] Add ICNS (IP-1801): an own reader and writer for PNG and JPEG 2000 entries (§5's OpenJPEG) with the color profile. Done when: an ICNS round-trips every entry and profile.
- [ ] Add BCnEncoder.Net (MIT) to `Directory.Packages.props` with a `docs/dev/decisions.md` row naming the license. Done when: the row names this section.
- [ ] Add DDS (IP-1802): BC1 to BC7, uncompressed formats, cube, volume, and array save types, flip, and transparent index. Done when: fixtures decode within the stated BCn tolerance of DirectXTex `texconv` output.
- [ ] Add DDS mipmaps (IP-1803): generate with `D01 T03 §2` filters or keep, wrap mode, gamma-correct filtering, and alpha-test coverage preservation. Done when: a test asserts each mip level's alpha-test coverage within 1 percent of the top level.
- [ ] Add TGA (IP-1804) through the moved codec: bits per pixel, RLE, and origin. Done when: round trips are exact.
- [ ] Add PCX through the moved codec and an own DCX container (IP-1805). Done when: a DCX fixture opens one layer per page.
- [ ] Add XBM (IP-1806): X10 or X11, prefix, comment, hot spot, and mask file. Done when: fixtures match GIMP 3.2's decode exactly and writes decode in GIMP exactly.
- [ ] Register XPM (IP-1807) through the `D01 T08 §1` codec (the X11 color-name table included there). Done when: fixtures match GIMP 3.2's decode exactly.
- [ ] Add XWD (IP-1808). Done when: fixtures match ImageMagick 7.1 exactly.
- [ ] Add Sun raster (IP-1809), standard or RLE. Done when: round trips are exact.
- [ ] Add SGI (IP-1810): none, RLE, and aggressive RLE. Done when: round trips are exact and ImageMagick 7.1 decodes each write.
- [ ] Add farbfeld (IP-1811) and WBMP read (IP-1812). Done when: farbfeld round trips exactly and WBMP matches ImageMagick 7.1.
- [ ] Document IP-1813 in `docs/dev/imago/formats.md`: the GIMP 3 format additions land here, with QOI and JPEG XL in §5, ILBM in §9, and PAM in §6. Done when: the page maps every addition to its section.
- [ ] Add the option pages for BMP, GIF, ICO, CUR, ANI, DDS, TGA, XBM, SGI, and Sun raster in §1's shell. Done when: the capture shows each page.
- [ ] Register every codec with §1's registry and log one Serilog Information line per read and write. Done when: File, Open lists each format.
- [ ] Commit fixtures under `tests/fixtures/imago/legacy-formats/` with `reference.txt` naming ImageMagick 7.1, GIMP 3.2, or DirectXTex `texconv` per fixture. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/legacy-formats/` and write `docs/user/imago/legacy-formats.md`. Done when: every page appears in a capture and the page documents it.
- [ ] Commit: `"imago: common and legacy raster formats on the shared codecs"`

**Test checkpoint:** Format fidelity proof: decode goldens from ImageMagick 7.1 (`magick <file> rgba:`), GIMP 3.2 for XBM, XPM, and ANI, and DirectXTex `texconv` for DDS match pixel-exact for lossless formats and within the stated BCn tolerance, with every writer's output decoding in the same oracle, under `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~LegacyFormats"`. Cheaper substitute that fails: WIC only, which the ANI, DDS, and SGI fixtures refuse.

## 9. Legacy Raster Formats II and Text and Resource Exports

The long tail: Amiga, Pixar, prepress, camera, game, and hobby formats GIMP and Photoshop still open, and GIMP's exports of an image as C source, HTML, ASCII art, or a GIMP brush, pipe, or pattern. Each is a small own codec or exporter registered with §1's registry and proven against ImageMagick, GIMP, or committed golden text. Catalog: IP-1814 to IP-1833 (20 features: IFF and ILBM, Pixar PXR, Scitex CT, Photoshop DCS, MPO, Paint Shop Pro, KiSS CEL, Alias PIX, PlayStation TIM, PVR and PAA, SFW, JIF, C source, C header, HTML table, colored HTML text, ASCII art, and GIMP brush, brush pipe, and pattern export).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/resource-exports/`.
**Job:** a user opens old and game files and exports images as code, HTML, text art, or GIMP resources. Consumer: compilers, browsers, terminals, and GIMP reading the output.
**Treatment:** option pages for C source, HTML table, colored HTML, ASCII art, DCS, TIM, and the GIMP resources. Cheaper substitute that fails the checkpoint: skipping the text exports.
**Chrome:** consume the registry, the `D03 T12 §3` and `D03 T12 §10` resource readers, the `D01 T08 §1` Pixar PXR and Scitex CT codecs, and Nodus's moved DCS code. Do not add a second brush or pattern reader, Pixar or Scitex CT codec, or DCS writer.

**Requires:** display-session -- the option pages need an interactive desktop

**Freeze check:** Every writer and exporter here saves through `AtomicFileWriter`; a failed or interrupted write leaves any existing target byte-identical; the open document is never changed by an export. Fixture source: `tests/fixtures/imago/legacy-formats-2/` (created by this section).

- [ ] Add IFF ILBM read with HAM and EHB (IP-1814). Done when: fixtures match ImageMagick 7.1 exactly.
- [ ] Register Pixar PXR read and write (IP-1815) through the `D01 T08 §1` codec instead of writing a second one. Done when: round trips are exact.
- [ ] Register Scitex CT write (IP-1816) through the `D01 T08 §1` codec instead of writing a second one. Done when: ImageMagick 7.1 decodes the written file exactly.
- [ ] Move Nodus's DCS reader and writer (`D02 T18 §8`) into `src/Photon.Core/Formats/PostScript/` beside §7's moved EPS writer, repointing Nodus, and add Photoshop DCS 1.0 and 2.0 (IP-1817) on it: single or multiple files with a composite. Done when: one DCS writer definition remains, under `src/Photon.Core/`, Nodus's DCS tests pass, and the plates of a written DCS 2.0 file render through Ghostscript within tolerance of the channel values.
- [ ] Add MPO read (IP-1818): the MPF index into layers. Done when: a two-image MPO opens two layers.
- [ ] Add Paint Shop Pro read (IP-1819): layers and the selection shape from the published PSP file format description. Done when: a PSP fixture opens its layers within 1/255 of GIMP 3.2's import.
- [ ] Add KiSS CEL read and write (IP-1820). Done when: round trips are exact and GIMP 3.2 decodes the write.
- [ ] Add Alias PIX read and write (IP-1821). Done when: round trips are exact.
- [ ] Add PlayStation TIM read and write (IP-1822) with type and image and palette origin. Done when: round trips keep the origins.
- [ ] Add Dreamcast PVR and Arma PAA read (IP-1823). Done when: fixtures match their committed goldens.
- [ ] Add SFW read (IP-1824) and JIF read (IP-1825). Done when: fixtures match ImageMagick 7.1 exactly.
- [ ] Add C source export (IP-1826): name, comment, GLib types, macros, RLE, alpha, RGB565, and opacity, as GIMP's exporter offers. Done when: output matches committed golden text and compiles with a test C compiler where present (skipped naming it otherwise).
- [ ] Add C header export (IP-1827). Done when: output matches committed golden text.
- [ ] Add HTML table export (IP-1828): full document, cellspan, compressed tags, caption, cell content, border, size, padding, and spacing. Done when: output matches committed golden text and parses with `System.Xml` in HTML mode.
- [ ] Add colored HTML text export (IP-1829): characters, file source, font size, and separate CSS. Done when: output matches committed golden text.
- [ ] Add ASCII art export (IP-1830) with an own glyph-density renderer (not aalib) writing text, HTML, ANSI, printer, IRC, and man page formats. Done when: each format matches committed golden text.
- [ ] Add GIMP brush (GBR) export (IP-1831) beside the `D03 T12 §3` reader, per GIMP's devel-docs. Done when: the written brush loads in `gimp-console-3.2` as a brush.
- [ ] Add GIMP brush pipe (GIH) export (IP-1832). Done when: the written pipe loads in `gimp-console-3.2` with its cell count.
- [ ] Add GIMP pattern (PAT) export with its description (IP-1833) beside the `D03 T12 §10` reader. Done when: the written pattern loads in `gimp-console-3.2` with its description.
- [ ] Add the option pages for C source, HTML table, colored HTML, ASCII art, DCS, TIM, and the GIMP resources in §1's shell. Done when: the capture shows each page.
- [ ] Register every codec and exporter with §1's registry and log one Serilog Information line per read and write. Done when: File, Open and Save a Copy list each format.
- [ ] Commit fixtures under `tests/fixtures/imago/legacy-formats-2/` with `reference.txt` naming the oracle per fixture (ImageMagick 7.1 or GIMP 3.2) and the golden text files. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/resource-exports/` and extend `docs/user/imago/legacy-formats.md`. Done when: every page appears in a capture and the page documents it.
- [ ] Commit: `"imago: legacy formats and text and resource exports"`

**Test checkpoint:** Format fidelity proof: decode goldens from ImageMagick 7.1 or GIMP 3.2 per format (oracle recorded per fixture) match, written GBR, GIH, and PAT files load in `gimp-console-3.2` as a brush, pipe, and pattern, and C, HTML, and ASCII outputs match committed golden text, under `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~LegacyFormats2"`. Cheaper substitute that fails: read-only support for writable formats, which the writer round trips catch.

## 10. Metadata: EXIF, IPTC, XMP, and File Info

Photographers live in their metadata: captions, keywords, copyright, GPS, and camera data travel with every file, and Lumen needs the same readers and writers for its sidecars. This section adds EXIF and IPTC IIM readers and writers to `Photon.Core/Metadata/` beside the XMP packet core of `D01 T07 §6`, the File Info dialog and Metadata panel, a Location panel that goes online only after the user confirms, templates, export embedding and stripping, and sidecars; it also wires metadata into the writers of §5, §11, and §2, which leave it to this section. Catalog: IP-1860 to IP-1876 (17 features: the image comment, title and imported PDF metadata, EXIF orientation, the metadata editor, IPTC Core, IPTC Extension, GPS, DICOM metadata, the metadata viewer, audio, video, and Photoshop panels, templates, export embedding and stripping, editable EXIF in develop, the Location panel, the Metadata panel, strip GPS and EXIF, and XMP sidecars).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/file-info/` and `docs/captures/imago/metadata-panel/`.
**Job:** a photographer views, edits, templates, and strips metadata. Consumer: the saved and exported files, and every tool that reads their metadata.
**Treatment:** File Info (description, IPTC, IPTC Extension, camera data, GPS, raw XMP, history), a Metadata panel, a Location panel with a map, and export metadata policies. Cheaper substitute that fails the checkpoint: an XMP-only editor.
**Chrome:** consume the `D01 T07 §6` XMP core, the settings store, and the suite history. Do not add a second XMP parser.

**Requires:** display-session -- the dialog, panels, and map need an interactive desktop

**Freeze check:** Metadata edits change the document, never the file on disk, until the user saves; embedding writes through each format's writer and `AtomicFileWriter`; sidecar `.xmp` files are written atomically beside the file and never into the image's own bytes; Strip GPS on export never changes the open document. Fixture source: `tests/fixtures/imago/metadata/` (created by this section).

- [ ] Consume `XmpPacket` from `D01 T07 §6` for every XMP read and write in Imago. Done when: `grep -rn "class XmpPacket" src` prints one path, under `src/Photon.Core/`.
- [ ] Add `src/Photon.Core/Metadata/Exif/ExifReader.cs` and `ExifWriter.cs` for the IFD0, Exif, GPS, and Interop IFDs per Exif 3.0, including UTF-8 strings, so Lumen's `D04 T01 §11` consumes them. Done when: exiftool 13 reads back every written tag from a JPEG fixture equal.
- [ ] Add `src/Photon.Core/Metadata/Iptc/IptcIimReader.cs` and `IptcIimWriter.cs` (the 8BIM 1028 resource). Done when: exiftool 13 reads back every written IPTC IIM field equal.
- [ ] Add `DocumentMetadata` persisted as `metadata.xmp` in the `.imago` package, registered with the `D03 T08 §1` contract, including the image comment (IP-1860) and title and imported PDF metadata (IP-1861). Done when: a document's metadata round-trips `.imago` byte-equivalent after canonicalization.
- [ ] Add EXIF orientation handling on import (IP-1862): `Imago.Files.ExifOrientation` Ask, Always, or Never, with a rotate dialog for Ask. Done when: each of the eight orientation fixtures opens upright with Always.
- [ ] Add File Info's description page (IP-1863): title, author, description writer, rating, keywords, copyright status, notice, and URL. Done when: each field written to a JPEG reads back through exiftool 13 equal.
- [ ] Add the IPTC Core page (IP-1864): contact, dates, genre, scene, location, headline, subject, instructions, credit, and source. Done when: exiftool 13 reads each field back equal.
- [ ] Add the IPTC Extension 2024.1 page (IP-1865) including persons, locations, artwork, models, releases, supplier, registry, licensor, and digital source type. Done when: exiftool 13 reads each field back equal.
- [ ] Add the Metadata panel (IP-1874) for viewing and editing File, EXIF, IPTC, and rights fields beside the canvas. Done when: an edit in the panel appears in File Info and saves.
- [ ] Add the viewer pages (IP-1868): EXIF camera data, IPTC, XMP, and raw XMP. Done when: the raw XMP page shows the canonical packet of the fixture.
- [ ] Add read-only audio, video, and Photoshop metadata pages (IP-1869). Done when: a fixture with Photoshop XMP fields shows them read-only.
- [ ] Show DICOM fields (IP-1867: patient, study, series, equipment) from §6's reader in File Info. Done when: a DICOM fixture's patient and study fields appear.
- [ ] Add GPS view and edit (IP-1866). Done when: an edited latitude writes and exiftool 13 reads it back within 1e-7 degrees.
- [ ] Add Strip GPS and Strip All EXIF (IP-1875) as undoable commands. Done when: after Strip GPS a saved file has no GPS tag in exiftool 13's dump.
- [ ] Add the Location panel (IP-1873) with OpenStreetMap tiles fetched only after the user opens the panel and confirms online use, a tile URL setting (`Imago.Metadata.MapTileUrl`), attribution, and a tile cache. Done when: a test asserts no network request before the confirmation and the attribution text is shown.
- [ ] Add metadata templates (IP-1870): save, apply (append or replace), import, and export. Done when: applying a template in append mode keeps existing keywords and adds the template's.
- [ ] Add the export metadata policy (IP-1871): embed or strip per category, and update dimensions, timestamps, software, and thumbnail automatically. Done when: an export with GPS stripped and copyright kept shows exactly that in exiftool 13's dump.
- [ ] Wire EXIF, IPTC, and XMP embedding into the JPEG, TIFF, PNG, WebP, PSD, JPEG XL, AVIF, and HEIF writers of §2, §5, and §11, enabling the metadata options §11 left to this section. Done when: exiftool 13 reads the same copyright notice back from each format's written fixture.
- [ ] Expose `ExifEditSession` for editable EXIF in develop (IP-1872), consumed by `D03 T15 §12`. Done when: a test edits the camera model through the session and the develop document's metadata changes.
- [ ] Add XMP sidecars (IP-1876): export and import `.xmp` beside the file and auto-load on open (`Imago.Metadata.AutoLoadSidecars`, default true). Done when: a sidecar's keywords appear after opening its image, and an exported sidecar re-imports equal.
- [ ] Serve the consumers that waited on this section: the XMP history log of `D03 T08 §6` exports through `XmpPacket`, `D03 T14 §6` matches lens profiles from EXIF, and `D03 T15 §6` reads bracket exposure values from EXIF. Done when: each consumer's test is updated to read through the new readers and passes.
- [ ] Name the history step "Edit Metadata" and log one Serilog Information line per edit, strip, and sidecar write. Done when: a Serilog test logger asserts each line.
- [ ] Commit fixtures under `tests/fixtures/imago/metadata/` (JPEG, TIFF, PNG, WebP, PSD, orientation set, DICOM, sidecar) with `reference.txt` naming exiftool 13. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/file-info/` and `docs/captures/imago/metadata-panel/` and write `docs/user/imago/metadata.md`. Done when: every page and panel appears in a capture and the page documents it.
- [ ] Commit: `"imago: EXIF, IPTC, and XMP metadata with File Info and sidecars"`

**Test checkpoint:** Format fidelity proof: exiftool 13 reads back every written field from the JPEG, TIFF, PNG, WebP, and PSD fixtures under `tests/fixtures/imago/metadata/`, unknown XMP survives a round trip byte-equivalent after canonicalization, and Strip GPS leaves no GPS tag, under `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~Metadata"`. Cheaper substitute that fails: XMP only, which exiftool's EXIF and IPTC IIM checks catch.

## 11. JPEG, PNG, and TIFF Option Extensions

The three most common formats need their full option sets: arithmetic coding and scan scripts in JPEG, HDR chunks and every PNG color type, and every TIFF compression with BigTIFF, pyramids, GeoTIFF, and Photoshop layers. WIC's encoders cannot write most of these, so JPEG moves to libjpeg-turbo, PNG to the chunk-level writer §6 started, and TIFF to a writer chosen by a recorded decision. Metadata embedding in these writers is §10's, which runs next and enables those options by name. Catalog: IP-1834 to IP-1843 (10 features: JPEG encoding options, JPEG export options, PNG export options, TIFF export options, TIFF layers, Photoshop data in JPEG and TIFF, CMYK JPEG, TIFF, and JPEG XL, HDR PNG options, TIFF with layers, and the layered TIFF prompt).

**Fidelity:** extends the JPEG options dialog of `D03 T04 §2` (`docs/captures/imago/jpeg-options/`); new build, no baseline for the PNG and TIFF options, captured to `docs/captures/imago/png-tiff-options/`.
**Job:** a user controls exactly how the three most common formats are encoded. Consumer: every app reading the written files.
**Treatment:** JPEG, PNG, and TIFF option pages with live preview and a real size estimate, saved defaults, and the layered TIFF prompt. Cheaper substitute that fails the checkpoint: WIC's quality slider only.
**Chrome:** consume the registry, §2's PSD layer section, and the `D01 T04 §1` and `D01 T04 §3` color engine. Do not add a second PNG or JPEG encoder.

**Requires:** display-session -- the option pages need an interactive desktop

**Freeze check:** JPEG, PNG, and TIFF saves keep going through `AtomicFileWriter`; with default options, PNG and TIFF saves of every `D03 T04 §2` and `D03 T04 §3` fixture still decode pixel-exact to the document; a failed or interrupted write leaves any existing target byte-identical; the layered TIFF prompt appears before writing when `Imago.Formats.Tiff.AskLayered` is on and Cancel writes nothing. Fixture source: `tests/fixtures/imago/png/`, `jpeg/`, and `tiff/` (from `D03 T04 §2` and `D03 T04 §3`) and `tests/fixtures/imago/png-tiff-options/` (created by this section).

- [ ] Build libjpeg-turbo 3.1 per RID with `build/native/libjpeg-turbo/build.ps1` (`SOURCE.txt`), binding it in `src/Photon.Core/Formats/Jpeg/`, with its IJG, BSD-3-Clause, and zlib notices and a new `docs/dev/decisions.md` row. Done when: both RIDs' DLLs are committed and the row names the three licenses.
- [ ] Add the JPEG encoding options (IP-1834): optimize, progressive with scan scripts, subsampling 4:4:4, 4:2:2, 4:2:0, and 4:1:1, DCT method, arithmetic coding, restart markers, and smoothing. Done when: libjpeg-turbo `djpeg` and exiftool 13 confirm each option in the written files.
- [ ] Switch Nodus's progressive JPEG path (`D02 T14 §16`) to this encoder. Done when: `grep -rn "JpegBitmapEncoder" src/Nodus` finds no progressive path and Nodus's JPEG export tests pass.
- [ ] Add the JPEG export options (IP-1835): matte, a size estimate from a real encode, live preview, and use original quality estimated from the quantization tables as GIMP does. Done when: the estimate equals the written byte count and the original-quality estimate of a quality-85 fixture reads 85.
- [ ] Add CMYK JPEG with the Adobe APP14 marker, thumbnail, and comment; EXIF, IPTC, and XMP options are disabled with a tooltip naming `D03 T17 §10`, which enables them. Done when: a CMYK JPEG reads back CMYK through ImageMagick 7.1 and `python scripts/todo-graph.py resolve 'D03 T17 §10'` resolves.
- [ ] Extend the `PngWriter` §6 created (IP-1836): gray, gray-alpha, RGB, RGBA, and indexed at 8 or 16 bit, compression 0 to 9, Adam7, tRNS, bKGD, oFFs, pHYs, tIME, and iTXt and zTXt, with defaults under `Imago.Formats.Png.*`. Done when: `pngcheck` 3.0 validates every chunk and libpng decodes each variant exactly.
- [ ] Add the HDR PNG options to the PNG page (IP-1841): PQ, HLG, and BT.709 transfer, primaries, and full range (cICP), with mDCV and cLLI. Done when: `pngcheck` 3.0 reports the cICP values chosen.
- [ ] Decide the TIFF writer: an own writer versus LibTiff.NET (BSD-3-Clause), recorded in `docs/dev/decisions.md` with the measurement. Done when: the row names the choice and its evidence.
- [ ] Add the TIFF options (IP-1837): JPEG, PackBits, CCITT G3 and G4, LZW, and Deflate compression, interleaved or planar, byte order, transparent pixel colors, and CMYK. Done when: libtiff 4.7 `tiffdump` confirms each tag and compression.
- [ ] Add BigTIFF, pyramid sub-IFDs, and GeoTIFF tags kept from import. Done when: `tiffinfo` reports BigTIFF and the sub-IFD count, and the GeoTIFF tags of a fixture survive a round trip.
- [ ] Add layered TIFF (IP-1838, IP-1842): Photoshop-style layers in tag 37724 through §2's PSD layer section, with save and crop layers and layer compression. Done when: ImageMagick 7.1 reads the layered TIFF's layers.
- [ ] Add `Imago.Formats.Tiff.AskLayered` (IP-1843, default true) prompting before a layered TIFF save. Done when: a test asserts the prompt with the setting on and none with it off.
- [ ] Add Photoshop data in JPEG and TIFF (IP-1839): APP13 and tag 34377 image resources for clipping paths (2000 to 2999, from `D03 T16 §5`'s clipping flag through `D03 T16 §10`'s `ExportClippingPath`) and guides (1032). Done when: exiftool 13 reads the clipping path name and psd-tools' resource parser reads the guides.
- [ ] Add CMYK JPEG, TIFF, and JPEG XL import and export with a CMYK profile (IP-1840) through `D01 T04 §1` and `D01 T04 §3`; PSD CMYK is §2 and §3's. Done when: a CMYK TIFF round-trips its channel values exactly with its profile.
- [ ] Add the JPEG, PNG, and TIFF option pages with live preview and saved defaults, extending the `D03 T04 §2` JPEG dialog. Done when: the captures show each page and a changed default is used by the next save.
- [ ] Commit fixtures under `tests/fixtures/imago/png-tiff-options/` with `reference.txt` naming `djpeg`, exiftool 13, `pngcheck` 3.0, libtiff 4.7, and ImageMagick 7.1. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/jpeg-options/` (refreshed) and `docs/captures/imago/png-tiff-options/`, and write `docs/user/imago/jpeg-png-tiff.md`. Done when: every option appears in a capture and the page documents it.
- [ ] Commit: `"imago: full JPEG, PNG, and TIFF options with layered TIFF and CMYK"`

**Test checkpoint:** Format fidelity proof: libjpeg-turbo `djpeg` and exiftool 13 confirm each JPEG option in written files, `pngcheck` 3.0 validates every PNG chunk and libpng decodes it exactly, libtiff 4.7 `tiffdump` confirms each TIFF tag and compression, and ImageMagick 7.1 reads the layered TIFF's layers, under `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~JpegPngTiff"`. Cheaper substitute that fails: WIC's encoder, which cannot write arithmetic coding, cICP, or BigTIFF and fails those assertions.

## 15. Place, Export and Overwrite Semantics, Notes Import, Load Files into Stack, and Watermarks

Users bring other files into an open document (embedded or linked, a PDF page, annotations as notes, a folder of frames as a stack, a watermark at a fixed anchor) and expect GIMP's and Photoshop's rules for what Save does to a file that was imported rather than native. This section adds those commands on §1's registry and dialogs. Placing never opens a source file for writing, and overwriting an imported file warns before any loss. Split from §1 on 2026-09-27 (operator decision to split the packed sections). Catalog: IP-1717 to IP-1721 and IP-2383 (6 features: export and overwrite semantics, place embedded and linked, notes from PDF or FDF, place embedded as Affinity's row, Load Files into Stack, and watermark placement with saved images, anchors, keyed transparency, blend, and presets).

**Fidelity:** `docs/captures/imago/file-menu/` (baseline from §1), extended; new build, no baseline for the watermark dialog, captured to `docs/captures/imago/watermark/`.
**Job:** a user brings any file into the open document as a layer, a smart object, notes, a stack, or a watermark, and saves an imported file knowing what a lossy format drops. Consumer: the Layers panel, the `D03 T08 §5` notes, and the file on disk.
**Treatment:** File, Place Embedded, Place Linked, Place Watermark, Import, Notes, and Load Files into Stack commands; a PDF page picker; a watermark dialog with an image list, an anchor grid, and presets; File, Overwrite <name> and Export To <name> for imported files with the lossy-format notice. Cheaper substitute that fails the checkpoint: Open followed by copy and paste, which loses the link and the placement preferences.
**Chrome:** consume §1's registry and dialogs, `AtomicFileWriter`, the `D03 T09 §9` and `D03 T09 §10` smart objects, the settings store, and the suite history. Do not add a second file dialog service.

**Requires:** display-session -- driving Place, the page picker, the watermark dialog, and drops needs an interactive desktop

**Freeze check:** Overwrite <name> shows the lossy-format notice before writing and Cancel writes nothing; every write goes through `AtomicFileWriter`, and a failed or interrupted write leaves any existing target byte-identical; placing, importing notes, loading a stack, and placing a watermark never open a source file for writing (source hashes quoted); watermark presets are written through the settings store. Fixture source: `tests/fixtures/imago/file-menu/` (created by §1, extended here).

- [ ] Add export and overwrite semantics (IP-1717): `Imago.Files.SaveNativeOnly` (GIMP's rule; default false), and File, Overwrite <name> and Export To <name> for imported files. Done when: with the setting on, Save offers only `.imago` and Overwrite <name> writes the imported format.
- [ ] Show the lossy-format notice before saving over an imported non-native file ("Saving over <name> as JPEG loses layers and quality. Save anyway?"). Done when: a test asserts the notice and that Cancel writes nothing.
- [ ] Add File, Place Embedded (IP-1718, IP-1720) through `D03 T09 §9` with the placement preferences resize to canvas, always create smart object, and skip transform. Done when: placing a larger fixture with resize to canvas fits it inside the canvas.
- [ ] Add File, Place Linked (IP-1718) through `D03 T09 §10`. Done when: editing the linked file on disk updates the placed layer after the link refresh.
- [ ] Add a PDF page picker for placing PDF files, which `D03 T17 §7` enables when its PDFium importer lands; until then placing a PDF is refused naming that section. Done when: the refusal text names the section and it resolves.
- [ ] Add File, Import, Notes (IP-1719): PDF text annotations read through PdfPig (Apache-2.0, already in the suite since `D02 T14 §2`) into `D03 T08 §5` notes, and FDF through a small own parser on PdfPig's tokenizer. Done when: a PDF fixture with three annotations imports three notes with their text and positions.
- [ ] Add File, Load Files into Stack (IP-1721): one layer per file, optional auto-align through `D03 T15 §5`, and optional convert to smart object. Done when: loading three fixtures yields three layers named after the files, aligned when the option is on.
- [ ] Add File, Place Watermark (IP-2383) in `src/Imago/Photon.Imago.Desktop/Views/Files/WatermarkDialog.xaml`: a saved watermark image list (`Imago.Watermark.Images`), nine anchor positions with pixel offsets, a keyed transparency color with a tolerance, blend mode and opacity, and named presets in `Imago.Watermark.Presets`, placing the watermark as a new layer (a smart object through `D03 T09 §9` when embedding) as one undo step "Place Watermark", after ACDSee Photo Studio Ultimate 2027's Edit-mode Watermark tool (user guide, Watermark). Done when: `WatermarkPlacementTests` place a fixture watermark at the bottom-right anchor with a 16 px offset and keyed white, and assert the layer bounds, alpha 0 on the keyed pixels, and one history step. Cheaper substitute: a Place Embedded the user positions by hand, which the anchor test catches.
- [ ] Log one Serilog Information line per place, import, stack load, watermark placement, and overwrite (`{Action} {Format} {Path} in {ElapsedMs} ms`), and name the history steps "Place Embedded", "Place Linked", and "Place Watermark". Done when: a Serilog test logger asserts each line.
- [ ] Commit fixtures under `tests/fixtures/imago/file-menu/` (a PDF with annotations, an FDF, three stack images, a watermark PNG with a white key) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/file-menu/` and `docs/captures/imago/watermark/`, and extend `docs/user/imago/files.md`. Done when: every command this section adds appears in a capture and the page documents it.
- [ ] Commit: `"imago: place, export semantics, notes import, stacks, and watermarks"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~WatermarkPlacementTests"` exits 0, and a driven run places embedded and linked (editing the linked file on disk updates the layer after the link refresh), imports three PDF annotations as notes, loads three files into a stack, places a watermark at an anchor, and cancels an Overwrite at the lossy-format notice, with captures committed and every source hash quoted unchanged. Cheaper substitute that fails: Open followed by copy and paste, which the linked-update step catches.

## 16. PostScript, EPS, SVG, and Metafiles

Print shops still receive EPS, and designers bring EPS, AI, SVG, and metafiles to rasterize. This section runs the user's own Ghostscript for PostScript (never bundled, because it is AGPL), writes EPS on the PostScript writer §7 moved into `Photon.Core`, rasterizes SVG with Nodus's SVG renderer moved here as its second consumer, and reads and writes WMF and EMF through the metafile code §7 moved. It also enables the SVG, EPS, and AI half of §1's vector routing and the SVG clipboard flavor §12 deferred to it. Split from §7 on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. Catalog: IP-1774, IP-1781 to IP-1785, IP-1793, and IP-1794 (8 features: PostScript, EPS, and AI import, EPS save, PostScript and EPS export, SVG import, WMF import, WMF and EMF export, EPS level and minimize size, and metafile export options).

**Fidelity:** new build, no baseline; captured to `docs/captures/imago/eps/` and `docs/captures/imago/metafile/`.
**Job:** a user rasterizes EPS, AI, SVG, and metafiles in and sends EPS and metafiles out. Consumer: the document on import; PostScript RIPs and metafile readers on export.
**Treatment:** a PostScript import dialog, an SVG size dialog, a metafile DPI dialog, EPS options, and metafile options. Cheaper substitute that fails the checkpoint: rasterizing EPS or SVG through WPF, which the Ghostscript and Inkscape comparisons catch.
**Chrome:** consume the moved Ghostscript runner, `PostScriptWriter`, EMF and WMF code, and SVG renderer, and §1's registry and options shell. Do not add a second PostScript writer or SVG renderer.

**Requires:** display-session -- the dialogs and captures need an interactive desktop

**Freeze check:** EPS and metafile saves write through `AtomicFileWriter`; a failed or interrupted write leaves any existing target byte-identical; importing an EPS, AI, SVG, or metafile never opens the source for writing and Ghostscript runs with `-dSAFER`. Fixture source: `tests/fixtures/imago/eps/` and `metafile/` (created by this section).

- [ ] Move the SVG renderer into `src/Photon.Core/Vector/Svg/` beside the reader `D03 T16 §5` moved, repointing Nodus. Done when: one SVG renderer definition remains.
- [ ] Add PostScript, EPS, and AI import (IP-1774) through the moved runner with `-dSAFER`, `-dTextAlphaBits`, `-dGraphicsAlphaBits`, bounding box, and coloring; AI opens through its embedded PDF stream; an absent Ghostscript is refused by name; no AI export. Done when: an EPS fixture renders within the stated tolerance of Ghostscript 10.x and the absent-runner refusal is asserted.
- [ ] Add EPS save (IP-1781, IP-1782, IP-1793) on the moved `PostScriptWriter`: TIFF preview 1 or 8 bit or none, ASCII85, binary, or JPEG encoding, halftone screen and transfer inclusion, vector data, size, offset, unit, rotation, PostScript level 2 or 3, and minimize size. Done when: a written EPS renders through Ghostscript within the stated tolerance of Imago's render.
- [ ] Add SVG import (IP-1783) rasterized at a chosen size by the moved renderer, and enable §12's SVG clipboard flavor. Done when: an SVG fixture imports within 1/255 of Inkscape 1.4's render at the same size.
- [ ] Add WMF and EMF import (IP-1784) rasterized at a chosen DPI through the moved readers. Done when: fixtures import within the stated tolerance of Inkscape 1.4's render.
- [ ] Add WMF and EMF export (IP-1785, IP-1794): vector layers as records and raster layers as bitmap records, with enhanced metafile and clip transparency options. Done when: exported files re-import through Inkscape 1.4 within the stated tolerance.
- [ ] Register the PostScript, EPS, AI, SVG, WMF, and EMF readers and the EPS, WMF, and EMF writers with §1's registry, enabling §1's vector routing for those files, the SVG and EMF paste entries of `D03 T08 §8`, and SVG and EPS placement in `D03 T09 §9`, removing each tooltip. Done when: File, Open on an EPS and an SVG opens their import dialogs, and the owning sections' disabled-state tests are updated to assert the enabled controls and pass.
- [ ] Log one Serilog Information line per PostScript, SVG, and metafile import and export with format and milliseconds. Done when: a Serilog test logger asserts the line.
- [ ] Commit fixtures under `tests/fixtures/imago/eps/` and `metafile/` with `reference.txt` naming Ghostscript 10.x and Inkscape 1.4 with versions and commands. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/imago/eps/` and `docs/captures/imago/metafile/`, and extend `docs/user/imago/pdf-eps.md` with PostScript, EPS, SVG, and metafiles. Done when: every dialog appears in a capture and the page documents it.
- [ ] Commit: `"imago: PostScript, EPS, SVG, and metafiles on the shared writers"`

**Test checkpoint:** Format fidelity proof: EPS imports render within the stated tolerance of Ghostscript 10.x and the absent-runner refusal is asserted; a written EPS renders through Ghostscript within tolerance of Imago's render; SVG imports match Inkscape 1.4's render at the same size within 1/255; WMF and EMF imports match Inkscape 1.4 within tolerance and exported files re-import through Inkscape 1.4 within tolerance; all under `dotnet test Photon.slnx --filter "Category=Fidelity&FullyQualifiedName~Eps|FullyQualifiedName~Svg|FullyQualifiedName~Metafile"`. Cheaper substitute that fails: rasterizing through WPF, which the Ghostscript and Inkscape comparisons catch.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` exits 0 with every fixture folder under `tests/fixtures/imago/` from this file reporting within its stated tolerance
- [ ] Every fixture folder this file creates carries `reference.txt` naming its oracle (psd-tools, GIMP, ImageMagick, OpenImageIO, dcmtk, DirectXTex, PDFium, Ghostscript, MuPDF, Inkscape, exiftool, libtiff, pngcheck, or a reference CLI) and version
- [ ] `grep -rn "class PsdWriter\|class PdfContentWriter\|class GhostscriptBridge\|class WiaAcquireService\|class TgaCodec" src` prints one path each, all under `src/Photon.Core/`
- [ ] `docs/dev/decisions.md` has a row with a GPL-3.0 check for every native library and package this file adds (libwebp, libavif, dav1d, libaom, libheif, libde265, x265, libjxl, OpenJPEG, OpenEXR, PDFium, libjpeg-turbo, SharpCompress, FluentFTP, BCnEncoder.Net, and the TIFF writer choice)
- [ ] Every disabled control on this file's surfaces names a section that `python scripts/todo-graph.py resolve` resolves (`D03 T17 §7`, `D03 T17 §10`, `D03 T17 §15`, `D03 T17 §16`)
- [ ] B-022 is gone from `todo/backlog.md`, and its source key `legacy-imago-7.2-7.3` is carried by §5 alone
- [ ] `python scripts/todo-graph.py validate` clean
