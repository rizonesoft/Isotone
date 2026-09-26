---
schema_version: 1
id: nodus-parity-formats
domain: 02-nodus
status: draft
title: "TODO-14 -- Nodus Parity: File Formats, Export, and Web"
depends_on: []
frozen: true
track: N14
---

# TODO-14 -- Nodus Parity: File Formats, Export, and Web

> **Goal:** A Nodus user can open, place, and save the files the rest of the industry sends (SVG with every export option, PDF, Illustrator .ai, CorelDRAW .cdr and .cmx, EPS and PostScript, DWG and DXF, metafiles and plotter files, every common raster format, PSD, office documents), can batch-export artboards, pages, and assets for screens and the web with optimized previews, slices, links, and rollovers, can draw pixel-perfect, and can exchange artwork through the clipboard, placed files, and a scanner, with every reader and writer proven against committed fixtures and goldens from a named reference implementation.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `src/Nodus/Bezier.Core/Services/ImportService.cs` refuses PDF outright ("PDF import requires additional libraries") and routes AI, EPS, and PDF through three stub methods; the AI and EPS stubs only search the file text for an embedded `<svg` and otherwise fail ("Full AI support requires Adobe Illustrator"). `ImportService.ImportFromClipboard` already accepts SVG, image, and text clipboard payloads, but no app code calls it. `SvgExportOptions` in `SvgExporter.cs` has only minify, IDs, XML declaration, viewBox, decimal precision, and inline styles: no SVGZ, CSS, font, or image options. `ExportService` knows an ICO format (extension and MIME) that `D02 T06 §14` wires. Copy and Paste in `MainWindowViewModel` only set the status text (`D02 T03 §3` builds the real clipboard). `RawSvgDialog` shows the document's SVG source and copies it as plain text. `SkiaCanvas` passes a `PixelPreview` flag to the renderer only at zoom 8 or more, and `SkiaRenderer` threads the flag through without using it. No format package (PdfPig, PDFsharp, ACadSharp, NPOI, DocumentFormat.OpenXml) is referenced, there is no `tests/fixtures/` tree and no `docs/dev/decisions.md` yet, and `VectorElement` has no slice, rollover, or hyperlink model.
<!-- claim: count "PDF import requires additional libraries" src/Nodus/Bezier.Core/Services/ImportService.cs = 1 -->
<!-- claim: count "ImportFormat\.(Ai|Eps|Pdf) =>" src/Nodus/Bezier.Core/Services/ImportService.cs = 3 -->
<!-- claim: count "Full AI support requires Adobe Illustrator" src/Nodus/Bezier.Core/Services/ImportService.cs = 1 -->
<!-- claim: count "clipboard\.Has(Svg|Image|Text)" src/Nodus/Bezier.Core/Services/ImportService.cs = 3 -->
<!-- claim: count "public (int DecimalPrecision|bool UseInlineStyles)" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 2 -->
<!-- claim: count "ExportFormat\.Ico =>" src/Nodus/Bezier.Core/Services/ExportService.cs = 2 -->
<!-- claim: count "StatusText = \"(Copy|Paste)\";" src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 2 -->
<!-- claim: count "Clipboard\.SetText\(_svgContent\)" src/Nodus/Bezier.Desktop/Views/RawSvgDialog.xaml.cs = 1 -->
<!-- claim: count "PixelPreview && _state\.Zoom >= 8" src/Nodus/Bezier.Desktop/Controls/Canvas/SkiaCanvas.cs = 1 -->
<!-- claim: count "pixelPreview" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 6 -->
<!-- claim: count "PdfPig|PDFsharp|ACadSharp|NPOI|DocumentFormat\.OpenXml" Directory.Packages.props = 0 -->
<!-- claim: absent tests/fixtures -->
<!-- claim: absent docs/dev/decisions.md -->
<!-- claim: count "Rollover|Hyperlink" src/Nodus/Bezier.Core/Models/VectorElement.cs = 0 -->

## Inputs

- [`standards/nodus.md`](../../standards/nodus.md) -- SVG is native, one reader and one writer own it, Inkscape is the reference implementation
- [`standards/shared.md`](../../standards/shared.md) -- atomic saves, refusal messages, the dependency-license rule, performance budgets
- [`standards/testing.md`](../../standards/testing.md) -- fixtures, goldens, and the Fidelity trait every reader and writer owes
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- "Formats and licensing", the per-format dependency decisions this file records
- Specifications: PDF 2.0 (ISO 32000-2), Adobe Illustrator File Format Specification v7, Adobe Photoshop File Formats Specification, libcdr source (MPL-2.0, reference only), [MS-EMF] and [MS-WMF], ISO 8632 CGM, the HP-GL/2 reference, SVG 1.1 and SVG 2, the Adobe Swatch Exchange layout
- -> XREF: D02 T04 §2 -- SVG round-trip fixtures and tolerance, extended by §1
- -> XREF: D02 T04 §3 -- PNG and JPEG export through `RasterExporter`, extended by §12, §15, §16
- -> XREF: D02 T06 §14 -- File, Place, the one export dialog, WebP, ICO, and XAML writers, extended by §2, §12, §15, §19
- -> XREF: D02 T03 §3 -- the `ClipboardService` §1 and §19 extend with more flavors
- -> XREF: D02 T07 §1 -- the live-object contract and `nodus:` namespace export items, slices, and live traces persist through
- -> XREF: D02 T07 §3 -- pages and artboards every multi-page reader and exporter targets
- -> XREF: D02 T07 §5 -- layers, master layers, and the layer export flag
- -> XREF: D02 T07 §12 -- the view-mode switcher pixel preview joins
- -> XREF: D02 T08 §15 -- dimension objects CAD dimensions become
- -> XREF: D02 T09 §7 -- the gradient and fill model CDR fills and outlines (§7) map onto
- -> XREF: D02 T10 §2 -- the rich text model PDF, CDR, and office text import into
- -> XREF: D02 T10 §13 -- the text import and export flow and readers §14 reuses
- -> XREF: D02 T10 §14 -- tables spreadsheet data imports into
- -> XREF: D02 T11 §1 -- the live-effect framework CDR effects map onto
- -> XREF: D02 T12 §1 -- bitmap objects and convert to bitmap
- -> XREF: D02 T12 §7 -- the Links panel and Edit Original for linked EPS, PSD, workbooks, and placed files
- -> XREF: D02 T13 §10 -- the PostScript emitter the EPS writer and printing of placed EPS use
- -> XREF: D02 T13 §14 -- the PDF writer on PDFsharp the .ai writer and PDF clipboard wrap
- -> XREF: D01 T03 §3 -- palette quantization and dithering for PCX, PNG-8, and GIF
- -> XREF: D01 T04 §1 -- ICC transforms for CMYK JPEG, ICC-based PDF spaces, and web color modes
- -> XREF: D01 T04 §3 -- the duotone and DeviceN bitmap model for PDF and PSD spot channels
- -> XREF: D01 T02 §2 -- the settings store every format option persists in
- -> XREF: D01 T02 §4 -- the suite history every import and slice edit records into
- -> XREF: D03 T04 §1 -- Imago's codec decision, which decides whether §12's WIC codec moves to `Photon.Core`
- -> XREF: D03 T04 §5 -- Imago's PSD import, which consumes §13's reader from `Photon.Core` instead of building a second one

## Outcome

- SVG and SVGZ save and export with every option, CSS export, and SVG code on the clipboard, each proven against Inkscape.
- PDF, PDF-compatible and legacy .ai, CDR (RIFF and ZIP), CDX, CDT, CMX, EPS, PS, DXF, DWG, EMF, WMF, CGM, PLT, WPG, every common raster format, PSD, and office documents open or place as editable Nodus objects, each against committed fixtures and a named golden.
- .ai, CDR, CMX, EPS, DXF, DWG, EMF, WMF, CGM, PLT, WPG, raster, PSD, TXT, RTF, DOC, TTF, and PFB writers produce files that read back through Nodus and through the named reference implementation.
- Export for Screens, the export list panel, and Export for Web batch-export pages, artboards, and assets in every screen format and scale, in the background with progress.
- Slices, image maps, hyperlinks, bookmarks, and rollovers write to SVG, HTML, and PDF and read back.
- Pixel preview equals the 1x PNG export pixel for pixel, and pixel-aligned art keeps integer edges.
- Copy, paste, drag, place, and scan exchange vectors with other applications through every supported flavor.
- Every import and export writes a conversion report and one log line; every import undoes as one step.

**Adjacency:** list=applicable @ D02 T14 §15; document=applicable @ D02 T14 §5; settings=applicable @ D01 T02 §2; reporting=applicable @ D02 T14 §2; notifications=applicable @ D02 T14 §15; permissions=applicable @ D02 T14 §2; audit=applicable @ D02 T14 §19; exchange=applicable @ D02 T14 §1; reverse=applicable @ D02 T14 §17

**Adjacency rationale:** The export list (§15) is the list of export assets, searchable and filterable. The .ai and PDF a user sends onward (§5) are the carried documents. Every format option persists under `Nodus.Formats.<Format>.*` and `Nodus.Export.*` in the shared settings store with a default and a reader. Every import and export writes a conversion report listing what was expanded, rasterized, or dropped, first built for PDF (§2). Background export (§15) notifies progress, cancel, and completion. Password PDFs and PDFs whose permissions forbid extraction (§2), locked or read-only targets, a missing Ghostscript (§9) or WIC extension, and a protected CDR are refused by name. Every import, place, paste, and slice or link edit is one undoable command with one Serilog Information line (§19 for place and paste). This whole file is the suite's exchange layer, starting with SVG (§1). Every import undoes as one step; slices, links, and rollovers release and delete (§17); export items delete; no export overwrites a file without a prompt.

## Implementation Order

| Order | Section | Deliverable                                                                    | Depends On                   | Status |
| :---: | :-----: | ------------------------------------------------------------------------------ | ---------------------------- | :----: |
|   1   |   §1    | SVG options: SVGZ, styling modes, CSS export, and SVG code                     | D02 T04 §2                   |  [ ]   |
|   2   |   §2    | PDF import                                                                     | D02 T07 §3, D02 T06 §14, D02 T13 §2 |  [ ]   |
|   3   |   §3    | Illustrator import: PDF-compatible .ai files                                   | §2                           |  [ ]   |
|   4   |   §4    | Illustrator import: private data and legacy PostScript .ai                     | §3                           |  [ ]   |
|   5   |   §5    | Illustrator .ai export                                                         | D02 T13 §14                  |  [ ]   |
|   6   |   §6    | CorelDRAW import: containers, pages, layers, and objects                       | D02 T07 §5                   |  [ ]   |
|   7   |   §7    | CorelDRAW import: fills, outlines, text, effects, and bitmaps; CMX             | §6, D02 T11 §1, D02 T10 §2   |  [ ]   |
|   8   |   §8    | CorelDRAW CDR and CMX export                                                   | §7                           |  [ ]   |
|   9   |   §9    | EPS and PostScript import and export                                           | §3, D02 T13 §10, D02 T13 §15 |  [ ]   |
|  10   |   §10   | DXF and DWG import and export                                                  | D02 T08 §15                  |  [ ]   |
|  11   |   §11   | EMF, WMF, CGM, HPGL, and WPG                                                   | D02 T07 §3                   |  [ ]   |
|  12   |   §12   | Raster formats: import and export through WIC                                  | D02 T06 §14                  |  [ ]   |
|  13   |   §13   | Photoshop PSD import and export                                                | §12                          |  [ ]   |
|  14   |   §14   | Office and text documents, Export For Office, and font export                  | D02 T10 §13, D02 T10 §14, D02 T13 §13 |  [ ]   |
|  15   |   §15   | Export for Screens, asset export, and the export list                          | D02 T06 §14, D02 T07 §3      |  [ ]   |
|  16   |   §16   | Export for Web: optimized preview and web formats                              | §12                          |  [ ]   |
|  17   |   §17   | Slices, image maps, hyperlinks, rollovers, and SVG interactivity               | §1, D02 T13 §16              |  [ ]   |
|  18   |   §18   | Pixel-perfect drawing, pixel preview, and object hinting                       | D02 T07 §12                  |  [ ]   |
|  19   |   §19   | Clipboard formats, OLE objects, placing multiple files, and scanner acquire    | D02 T06 §14                  |  [ ]   |

---

## 1. SVG Options: SVGZ, Styling Modes, CSS Export, and SVG Code

SVG is Nodus's native format, and hand-off to the web needs control over how it is written: styling as attributes, internal CSS, or inline styles, fonts as text or outlines, images embedded or linked, the ID scheme, precision, and whether Nodus's own `nodus:` editing data is kept. This section adds SVGZ, one SVG Options dialog shared by Save As SVG (keeps the `nodus:` namespace) and Export SVG (plain SVG), CSS export for named objects, and SVG code on the clipboard, each proven against Inkscape. Because Save As SVG is the frozen document save path, the default options must reproduce today's output. Catalog: NP-2263 to NP-2268 (6 features). Admission: the acceptance-bar aim "Nodus covers every CorelDRAW and Illustrator capability in the parity catalog".

**Freeze check:** Save and Save As SVG with default options write bytes identical to the pre-change writer for every `D02 T04 §2` fixture (hash comparison in `SvgOptionsRoundTripTests.DefaultsUnchanged`); SVG and SVGZ saves go through the atomic writer, and killing the process mid-save leaves the original byte-identical; Export SVG never writes to the open document's own path without the overwrite prompt. Fixture source: `tests/fixtures/nodus/svg/` (from `D02 T04 §2`) and `tests/fixtures/nodus/svg-options/` (created by this section).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/svg-options/.
**Job:** a web designer can export SVG in the styling, ID, and precision a hand-off needs and copy CSS for named objects. Consumer: the written SVG file, the CSS text, and other applications through the clipboard.
**Treatment:** one SVG Options dialog shared by Save As SVG and Export SVG, with a Show Code preview, presets, and a CSS Properties panel with copy and export. Cheaper substitute that fails the checkpoint: a minify checkbox on the existing dialog.
**Chrome:** consume the `D02 T06 §14` export dialog shell, the settings store, and `Photon.UI` controls. Do not add a second code viewer beside `RawSvgDialog`.

**Requires:** display-session -- the options dialog, the CSS Properties panel, and clipboard paste need an interactive desktop

- [ ] Extend `SvgExportOptions` in `src/Nodus/Photon.Nodus.Core/Services/SvgExporter.cs` with `Styling` (PresentationAttributes, InternalCss, InlineStyle, ExternalCss), `FontMode` (SvgText, Outlines), `ImageMode` (Embed, Link, Preserve), `ObjectIds` (LayerNames, Minimal, Unique), `Responsive`, `Encoding` (UTF-8, UTF-16), and `KeepEditingData`. Done when: `SvgOptionsRoundTripTests` cover one fixture per value of each option.
- [ ] Default options reproduce today's writer output byte for byte. Done when: `SvgOptionsRoundTripTests.DefaultsUnchanged` hashes each `D02 T04 §2` fixture saved before and after.
- [ ] `KeepEditingData` is on for Save As SVG (the `nodus:` namespace kept) and off for Export SVG (plain SVG, no `nodus:` attribute or element). Done when: a test asserts no `nodus:` token in the exported fixture and its presence in the saved one.
- [ ] Add `SvgzCodec` (`GZipStream` over the reader and writer); `.svgz` joins `ImportService`'s extension table and the Save As filter. Done when: an SVGZ fixture decompresses to the byte-identical SVG and opens to the same model.
- [ ] Import options on `SvgImporter`: scaling Automatic, English, or Metric with a drawing scale, `clipPath` to clipping groups, `symbol` and `use` to symbols, linked and embedded images, `<a>` links, and metadata preserved, persisted under `Nodus.Formats.Svg.Import.*`. Done when: import tests assert each mapping on its fixture.
- [ ] Export fidelity rules: layers write as `<g id="<layer name>">`, symbols as `<symbol>`, effects the SVG profile cannot express rasterize through `D02 T12 §1` with a report line, and scope is document, page, or selection. Done when: `SvgExportFidelityTests` assert each rule on its fixture.
- [ ] Add the SVG Options dialog and view model (`Views/Export/SvgOptionsDialog.xaml`) with every option, named presets saved in the settings store, and a Show Code button. Done when: a view-model test asserts every option binds to `SvgExportOptions`; capture committed.
- [ ] Show Code opens the SVG the current options would write, read-only, reusing `RawSvgDialog`. Done when: a test asserts the dialog receives the writer's output for the current options.
- [ ] Add `CssExporter` in `src/Nodus/Photon.Nodus.Core/Web/` generating class rules for named objects (fill, stroke, opacity, size, position, gradients as `linear-gradient` and `radial-gradient`). Done when: `CssExporterTests` match the committed CSS golden exactly.
- [ ] Add `CssPropertiesPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/` with Copy and Export buttons and options (units, vendor-prefix-free only, all named objects or the selection). Done when: a view-model test asserts Copy places the golden text on a fake clipboard.
- [ ] Copy writes an `image/svg+xml` flavor and a plain-text SVG flavor beside the `D02 T03 §3` payload, honoring `Nodus.Clipboard.IncludeSvgCode`. Done when: a clipboard test asserts both flavors from a fake clipboard.
- [ ] Paste of SVG text creates art as one undoable `PasteSvgCommand`. Done when: a test pastes the fixture text and asserts one history step.
- [ ] Settings `Nodus.Formats.Svg.*` for every option with defaults matching Inkscape plain SVG, each read by `SvgExporter` or `SvgImporter`. Done when: a settings readback test asserts each default.
- [ ] Log `Exported SVG {Path} ({Styling}, {Precision} dp)` once per export. Done when: the line is asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/svg-options/` (one per styling, font, and ID mode, an SVGZ pair, and a CSS golden) with Inkscape `--export-plain-svg` renders as goldens and the Inkscape version in `goldens/VERSION.txt`. Done when: the folder README lists every fixture and what it proves.
- [ ] Update `docs/user/nodus/` with the SVG options page. Done when: every option is documented.
- [ ] Commit: `"nodus: SVG options, SVGZ, CSS export, and SVG code on the clipboard"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~SvgOptionsRoundTripTests|FullyQualifiedName~SvgExportFidelityTests|FullyQualifiedName~CssExporterTests"` exits 0: every option combination re-imports to the same model and renders within the `D02 T04 §2` tolerance of the Inkscape golden, default options are byte-identical to the previous writer, SVGZ decompresses to the byte-identical SVG, and the CSS golden matches exactly; the options dialog capture is committed. Cheaper substitute that fails: asserting the output "contains <svg", which a dropped `style` element passes.

## 2. PDF Import

Clients send PDFs, and a designer must edit their paths and text, not a rendered picture of them. PdfPig (Apache-2.0) parses objects, streams, fonts, and encryption; Nodus interprets content streams with its own graphics-state interpreter so every path lands as an editable object. This section also builds the conversion report every later reader in this file reuses. Catalog: NP-2269 to NP-2276 (8 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/pdf-import/.
**Job:** a designer can open a client's PDF and edit its paths and text. Consumer: the document (pages, layers, objects) and the conversion report.
**Treatment:** a PDF Import dialog with page thumbnails (single, range, all), crop box, text as text or curves, maintain paragraphs, comments layer, crop to page, and a password prompt. Cheaper substitute that fails the checkpoint: placing the PDF as a rendered bitmap.
**Chrome:** consume the settings store, `Photon.UI` dialogs and thumbnails, and the `D02 T07 §3` page model. Do not add a PDF renderer.

**Requires:** display-session -- the import dialog and page thumbnails need an interactive desktop

- [ ] Move the existing PdfPig reference (Apache-2.0, added to `Directory.Packages.props` as a test-only reference of `tests/Photon.Nodus.Tests/` by `D02 T13 §2`) into `Photon.Nodus.Core`, and extend its `docs/dev/decisions.md` row to cover import (license checked against GPL-3.0, why PdfPig over a native renderer). Done when: the build is green, `Photon.Nodus.Core` references the one central PdfPig version, and the extended row names the license URL. Cheaper substitute: a second PdfPig entry or version, which the central package file refuses.
- [ ] Add `ConversionReport` in `src/Nodus/Photon.Nodus.Core/Formats/` (entries of kind Expanded, Rasterized, Approximated, Dropped, each with an object reference and a reason) and its toast summary, shared by every reader and writer in this file. Done when: `ConversionReportTests` assert the summary text for a report with one of each kind.
- [ ] Add `PdfContentInterpreter` in `src/Nodus/Photon.Nodus.Core/Formats/Pdf/`: graphics-state stack (CTM, clip, color spaces, line state, soft masks, blend modes) and path operators to `SvgPath`. Done when: `PdfContentInterpreterTests` assert the paths of the paths fixture within 1e-3 pt.
- [ ] Shadings: types 2 and 3 to gradients, types 4 to 7 to mesh, anything else approximated with a report line. Done when: the gradients fixture imports with gradient stops equal to the golden's.
- [ ] Form XObjects reused two or more times become symbols; images become `D02 T12 §1` bitmap objects; transparency groups and soft masks map to opacity and masks. Done when: the transparency fixture asserts group opacity and one symbol with two instances.
- [ ] Add `PdfImportOptions`: pages (single, range, all), target (new document pages or grouped objects on the current page), crop box (Bounding, Art, Crop, Trim, Bleed, Media), text as text or curves, maintain paragraphs, comments on a layer, crop content to page, persisted under `Nodus.Formats.Pdf.Import.*`. Done when: a settings readback asserts each default.
- [ ] Text reconstruction: glyph runs merge into lines by baseline and advance, and lines into paragraphs by leading and proximity when "maintain paragraphs" is on, otherwise one point-text object per run, into the `D02 T10 §2` rich text model. Done when: the text-flow fixture asserts paragraph count and text content.
- [ ] Text as curves converts glyph outlines to paths. Done when: the same fixture imported as curves has zero text objects and matches the golden render.
- [ ] Optional content groups become layers with visibility kept; annotations (text, line, shape, markup, ink, stamp) land on a non-printing Comments layer grouped by author. Done when: the OCG fixture asserts layer names and visibility, and the annotations fixture asserts the annotation count per author.
- [ ] Separation and DeviceN images keep their inks through the `D01 T04 §3` duotone model; ICC-based spaces convert through `D01 T04 §1`. Done when: the duotone fixture imports with its two ink names kept.
- [ ] Refuse by name a PDF whose permission flags forbid content extraction unless its owner password is entered ("<file> does not permit its content to be extracted"). Done when: a test over the restricted fixture asserts the refusal and the success with the owner password.
- [ ] Crop content to page clips everything outside the chosen box. Done when: a fixture with off-page art imports with a clip equal to the crop box.
- [ ] Password-protected PDFs prompt once; a refused password or a certificate-encrypted file is refused by name ("<file> is encrypted with a certificate; Nodus cannot open it"). Done when: tests assert the prompt, the success with the fixture password, and both refusals.
- [ ] Add the PDF Import dialog with page thumbnails rendered from the interpreter at thumbnail size. Done when: a view-model test asserts the page count and range parsing (`1-3, 5`); capture committed.
- [ ] Budget: a 200-page PDF opens its dialog in under a second (thumbnails lazy), and interpretation runs off the UI thread with progress and Cancel; a cancelled import changes nothing. Done when: a timing test on the generated 200-page fixture asserts under one second and a cancel test asserts an unchanged document.
- [ ] Replace the PDF refusal and stub in `ImportService` with the new reader, registered in the import table `D02 T06 §14` wires. Done when: `grep -n "PDF import requires additional libraries" src/Nodus` prints nothing.
- [ ] Log `Imported PDF {Path} ({Pages} pages, {Objects} objects, {ReportCount} report lines)`. Done when: the line is asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/pdf/` (paths, gradients, transparency groups, OCGs, annotations, text flow, duotone image, encrypted, extraction-restricted), authored for this suite with a README, and goldens rendered by Inkscape with poppler (`inkscape --pdf-poppler --export-type=png`, version in `goldens/VERSION.txt`). Done when: every fixture has a golden.
- [ ] Commit: `"nodus: PDF import with an own graphics-state interpreter and conversion reports"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~PdfImportFidelityTests|FullyQualifiedName~PdfContentInterpreterTests|FullyQualifiedName~ConversionReportTests"` exits 0: each imported fixture renders within the stated tolerance of the Inkscape with poppler golden, and text content, layer names, and annotation counts equal the golden's; the dialog capture is committed. Cheaper substitute that fails: a raster placement, which the text-content assertion catches.

## 3. Illustrator Import: PDF-Compatible .ai Files

Most modern `.ai` files are saved with PDF compatibility, so the §2 reader gives exact geometry for them; this section detects the flavor, maps artboards to pages and OCGs to layers, and replaces the embedded-`<svg` stub that finds nothing in a real file. Catalog: NP-2277 (1 feature).

**Fidelity:** no surface of its own (reuses the §2 import dialog with an Illustrator title and artboard wording).

- [ ] Add `AiFileDetector` in `src/Nodus/Photon.Nodus.Core/Formats/Ai/`: a `%PDF` header means PDF-compatible, `%!PS-Adobe` with `%%Creator: Adobe Illustrator` means legacy (handed to §4), anything else is refused by name. Done when: `AiFileDetectorTests` classify one fixture of each kind and a renamed PNG.
- [ ] Replace the `ImportAdobeIllustrator` stub in `ImportService` with the detector plus the §2 reader; `.ait` opens as a new untitled document. Done when: `grep -n "Full AI support requires Adobe Illustrator" src/Nodus` prints nothing and an `.ait` fixture opens untitled.
- [ ] Artboards map to pages (`D02 T07 §3`) by the PDF page boxes, keeping artboard names from the page labels. Done when: a three-artboard fixture opens as three named pages.
- [ ] OCGs map to layers with visibility and lock. Done when: the layers fixture asserts names, visibility, and lock state.
- [ ] Import options: text as text or curves; unsupported live features (appearance stacks, 3D, brushes) arrive as their PDF expansion with a report line each. Done when: a fixture with a 3D object imports with one Expanded report line naming it.
- [ ] A file saved without PDF compatibility is refused with a message naming §4's scope until §4 ships, then routed to §4. Done when: a test asserts the routing through the detector.
- [ ] Log `Imported AI {Path} ({Artboards} artboards, {Layers} layers)`. Done when: the line is asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/ai/pdf-compatible/` saved by Illustrator 30.8 (license note in the README: authored for this suite), with goldens from Inkscape with poppler and versions recorded. Done when: every fixture has a golden.
- [ ] Commit: `"nodus: open PDF-compatible Illustrator files with artboards and layers"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~AiPdfImportTests|FullyQualifiedName~AiFileDetectorTests"` exits 0: each fixture's render matches the Inkscape with poppler golden within tolerance and its page and layer lists equal the golden's. Cheaper substitute that fails: the current embedded-`<svg` search, which finds nothing in a real `.ai` and fails every fixture.

## 4. Illustrator Import: Private Data and Legacy PostScript .ai

The PDF part of an `.ai` gives geometry but loses live text, swatches, and symbols; the `AIPrivateData` streams keep them in Illustrator's PostScript-like operator language, which the published Illustrator File Format specification (v7) documents, as do legacy AI 3 to 8 files. This section parses that language so live text arrives as text, reads AICB from the clipboard, and appends [Converted] on opening legacy files. Catalog: NP-2278 (1 feature).

**Fidelity:** no surface of its own (library code behind the §2 dialog).

- [ ] Add `AiPrivateDataReader` in `src/Nodus/Photon.Nodus.Core/Formats/Ai/`: locate the `AIPrivateData` streams in the PDF, inflate (zlib), concatenate in order, and hand the text to the tokenizer. Done when: `AiPrivateDataTests.Extract` asserts the concatenated length and header line of the fixture.
- [ ] Add `AiTokenizer` for the AI PostScript subset (numbers, names, strings, arrays, procedures, comments with `%%` and `%_`). Done when: tokenizer tests cover each token kind.
- [ ] Add `AiPostScriptInterpreter` for the spec v7 operator subset: paths (`m l c v y`), painting (`f F s S b B`), groups (`u U`), layers (`Lb LB`, `Ln`), colors (`Xa XA`, `k K`, `g G`, `x X`), gradients (`Bd Bm`), and text (`To TO Tp TP`). Done when: `AiPrivateDataTests` assert layer names, live text strings, and swatch names on the private-data fixture.
- [ ] When private data is present it wins over the §3 PDF path, keeping live text, swatches, and symbols; unknown operators are counted in the conversion report, never dropped silently. Done when: a fixture with live text imports it as editable text where the §3 path gives curves (asserted), and an injected unknown operator appears in the report.
- [ ] Legacy AI 3 to 8 PostScript files open through the same interpreter. Done when: `AiLegacyTests` assert geometry against the goldens for the AI 8 and AI 3 fixtures.
- [ ] On opening a legacy file, the window title and default save name append " [Converted]" when `Nodus.Formats.Ai.AppendConvertedOnLegacy` is on (default on). Done when: a test asserts the name with the setting on and off.
- [ ] AICB clipboard read: register the Illustrator clipboard format and parse it with the same interpreter so paste from other vector editors keeps paths. Done when: a clipboard test with a recorded AICB payload asserts the pasted paths.
- [ ] Commit fixtures `tests/fixtures/nodus/ai/private-data/` and `tests/fixtures/nodus/ai/legacy/` saved by Illustrator 30.8 (current, AI 8, and AI 3 formats), with goldens from Inkscape with poppler for PDF-based files and from Inkscape's PostScript import through Ghostscript for legacy files, versions recorded. Done when: every fixture has a golden.
- [ ] Commit: `"nodus: read Illustrator private data and legacy PostScript AI files"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~AiPrivateDataTests|FullyQualifiedName~AiLegacyTests"` exits 0: a fixture with live text imports it as editable text through private data where the §3 path gives curves, and legacy fixtures match their goldens within tolerance. Cheaper substitute that fails: falling back to §3 for every file, which the live-text assertion catches.

## 5. Illustrator .ai Export

Handing a file to an Illustrator user means writing an `.ai` Illustrator opens and edits: PDF-based `.ai` through the `D02 T13 §14` PDF writer (layers as OCGs, artboards as pages) plus an `AIPrivateData` stream for what Nodus can express, a legacy EPS-based AI 8 writer, and AICB and PDF on the clipboard. Opening in Illustrator itself is an interoperability risk recorded here, not a CI gate. Catalog: NP-2279 to NP-2284 (6 features).

**Freeze check:** Saving as `.ai` writes through the atomic writer to the chosen path; the data-loss report is shown before writing, and Cancel writes nothing; a failed or interrupted write leaves any existing target byte-identical; the open SVG document's own file is never written by an `.ai` save. Fixture source: `tests/fixtures/nodus/ai/export/` (created by this section).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/ai-export/.
**Job:** a designer can hand a file to an Illustrator user who can edit it. Consumer: the written `.ai` file and whoever opens it.
**Treatment:** an Illustrator Options dialog (version, range, PDF compatibility, embed ICC, compression, save each artboard, text as text or curves, conversion and transparency options) with a data-loss report. Cheaper substitute that fails the checkpoint: renaming a PDF to `.ai`.
**Chrome:** consume the `D02 T13 §14` PDF writer, the `D02 T06 §14` export dialog shell, and the settings store. Do not add a second PDF writer.

**Requires:** display-session -- the options dialog and the report need an interactive desktop

- [ ] Add `AiWriter` in `src/Nodus/Photon.Nodus.Core/Formats/Ai/` wrapping the `D02 T13 §14` `PdfWriter`: one page per artboard, one OCG per layer, and the `/Illustrator` piece info. Done when: the export fixture re-imports through §3 with the same pages and layers.
- [ ] Add `AiPrivateDataWriter` writing paths, groups, layers, swatches, and text in the spec v7 operator subset as an `AIPrivateData` stream. Done when: re-import through §4 yields live text and the same swatch names.
- [ ] Options under `Nodus.Formats.Ai.Export.*`: version (CC, CS6, legacy AI 8), range (document, artboards, selection), Create PDF Compatible File, Embed ICC, Use Compression, Save Each Artboard Separately, and text as text or curves. Done when: a test per option asserts its effect on the written file.
- [ ] Conversion options: outlines to objects, simulate complex fills, spot to CMYK, include preview, and placed images linked or embedded. Done when: tests assert each on the export fixture.
- [ ] Add `AiLegacyWriter` emitting EPS-based AI 8 with a transparency choice: rasterize transparent areas (through `D02 T12 §1`) or drop transparency, one report line per object. Done when: `AiLegacyExportTests` assert both modes and their report lines.
- [ ] Conical and square gradients, which AI 8 cannot express, write as up to 256 filled bands, the count from the gradient's steps setting. Done when: `AiLegacyExportTests.GradientBands` asserts the band count.
- [ ] Live features Illustrator lacks expand through their `D02 T07 §1` fallbacks, and the export report lists each expansion. Done when: a fixture with a Nodus-only live object exports with one Expanded report line.
- [ ] Add the Illustrator Options dialog with the data-loss report before writing. Done when: a view-model test asserts Cancel writes nothing; capture committed.
- [ ] Clipboard write: AICB and PDF flavors beside SVG for paste into other editors and Imago, controlled by §19's clipboard settings. Done when: a clipboard test asserts both flavors and that each reads back through §4 and §2.
- [ ] Log `Exported AI {Path} v{Version} ({Artboards} artboards, {Expanded} expanded)`. Done when: the line is asserted.
- [ ] Record the interoperability risk with Illustrator itself in the user guide page and in `docs/dev/decisions.md`. Done when: both name the risk and the operator check that covers it.
- [ ] Commit fixtures `tests/fixtures/nodus/ai/export/` (a multi-artboard, multi-layer document with spot colors and text) with goldens rendered from the written files by Inkscape with poppler, versions recorded. Done when: the README lists them.
- [ ] Commit: `"nodus: save Illustrator .ai files, legacy AI 8, and AICB on the clipboard"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~AiExportRoundTripTests|FullyQualifiedName~AiLegacyExportTests"` exits 0: the exported `.ai` re-imports through §4 with the same layers, artboards, and live text (geometry within 1e-3 pt of the source model), and Inkscape with poppler renders it within tolerance of Nodus's own render; the dialog capture is committed. Cheaper substitute that fails: a PDF with an `.ai` extension, which the private-data read-back catches.

## 6. CorelDRAW Import: Containers, Pages, Layers, and Objects

CorelDRAW users moving to Nodus need their drawings to open with pages and layers intact. Nodus reads CDR with its own managed reader, libcdr (MPL-2.0) as the reference implementation and Inkscape with libcdr as the golden oracle; no native libcdr ships. This section reads the containers (RIFF CDR v7 to X3, X4 and later ZIP, CDX, CDT) and the structural and basic shape records. Catalog: NP-2285 to NP-2289 (5 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/cdr-import/.
**Job:** a CorelDRAW user moving to Nodus can open their drawings with pages and layers intact. Consumer: the document (pages, master layers, layers, objects).
**Treatment:** a CDR Import dialog with maintain layers and pages and a code page list, shown only when the file needs it. Cheaper substitute that fails the checkpoint: asking users to convert through Inkscape.
**Chrome:** consume the settings store and the `D02 T07 §3` and `§5` page and layer models. Do not add a native libcdr dependency.

**Requires:** display-session -- the options dialog needs an interactive desktop

- [ ] Record in `docs/dev/decisions.md` the CDR reader decision: an own managed reader, libcdr as reference, MPL-2.0 section 3.3 compatibility with GPL-3.0 verified against libcdr's file headers (none marked "Incompatible With Secondary Licenses"), and any file translated from libcdr keeping its MPL-2.0 header. Done when: the row names the libcdr commit checked.
- [ ] Add `CdrReader` in `src/Nodus/Photon.Nodus.Core/Formats/Cdr/` with a RIFF chunk walker for `CDR7` to `CDRD` and version detection. Done when: `CdrContainerTests` detect the version of every fixture.
- [ ] X4 and later: open the ZIP container with `System.IO.Compression.ZipArchive` (`content/riffData.cdr` plus `data/`). Done when: an X4-family fixture opens through the same walker.
- [ ] Add the `cmpr` compressed-list inflater and CDX handling. Done when: a CDX fixture opens with the same object count as its CDR twin.
- [ ] Object records: pages, master layers (all, odd, even), layers (visible, printable, locked, export flag), groups, curves, rectangles with corners, ellipses and arcs, polygons and stars, transforms, and object names. Done when: `CdrObjectFidelityTests` assert counts per record kind on each fixture.
- [ ] Options under `Nodus.Formats.Cdr.Import.*`: maintain layers and pages (off merges into one layer) and code page (automatic from the file, else a list from `Encoding.GetEncodings()` with `CodePagesEncodingProvider` registered). Done when: a legacy fixture with Cyrillic text imports correctly with code page 1251 chosen.
- [ ] Open makes a document; Import places a group on the current page; CDT opens as a new untitled document. Done when: tests assert each entry point's result.
- [ ] A password-protected or newer-than-known file is refused by name with the version found. Done when: tests assert both refusal sentences.
- [ ] Unknown records are counted in the conversion report and kept in a `nodus:cdr-unknown` note, never silently dropped. Done when: an injected unknown chunk appears in the report and the note.
- [ ] Add the CDR Import dialog, shown only when the file has non-Unicode text or multiple pages. Done when: a view-model test asserts when it shows; capture committed.
- [ ] Budget: a 10,000-object CDR opens in under five seconds with progress and Cancel. Done when: a timing test on the generated fixture asserts the budget.
- [ ] Log `Imported CDR {Path} v{Version} ({Pages} pages, {Objects} objects)`. Done when: the line is asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/cdr/` per version family (v7 to X3 RIFF, X4 to 2026 ZIP, CDX, CDT), authored or obtained with redistribution rights stated in the README, with goldens from Inkscape 1.4 with libcdr (version recorded). Done when: every fixture has a golden and a stated license.
- [ ] Commit: `"nodus: open CorelDRAW files with pages, layers, and objects"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~CdrContainerTests|FullyQualifiedName~CdrObjectFidelityTests"` exits 0: every fixture opens with the golden's page count, layer names, and object count, and renders within the stated tolerance of the Inkscape with libcdr golden; the dialog capture is committed. Cheaper substitute that fails: importing only the embedded preview thumbnail, which the object-count assertion catches.

## 7. CorelDRAW Import: Fills, Outlines, Text, Effects, and Bitmaps; CMX

The §6 reader gains the styling and content records: every fill and outline kind, artistic and paragraph text, CorelDRAW effects mapped to Nodus live effects where one exists (else their stored expanded geometry), embedded bitmaps, Painterly brushstrokes with their fallback bitmap, and the CMX reader. Catalog: NP-2290 (1 feature).

**Fidelity:** no surface of its own (reuses the §6 dialog).

- [ ] Add `CdrFillReader`: uniform, fountain (linear, radial, conical, square, with steps), two-color, full-color and bitmap patterns, texture (as its stored bitmap), PostScript fill (a named placeholder pattern with a report line), and mesh. Done when: `CdrStyleFidelityTests` render each fill fixture within tolerance of its golden.
- [ ] Add `CdrOutlineReader`: width, color, dashes, caps and joins, arrowheads, calligraphic nib, behind fill, and scale with object. Done when: each outline fixture renders within tolerance.
- [ ] Add `CdrTextReader`: artistic and paragraph text with styles and frames into the `D02 T10 §2` model, fonts matched by name with substitution reported. Done when: the text fixture asserts strings, frames, and one substitution report line for a missing font.
- [ ] Effects (blend, contour, envelope, extrude, drop shadow, lens, PowerClip, perspective, distortion) map to the `D02 T11 §1` live effects where Nodus has one, else to the stored expanded geometry with a report line. Done when: `CdrEffectMappingTests` assert live versus expanded per effect by type.
- [ ] Embedded bitmaps decode through §12's codecs into `D02 T12 §1` bitmap objects. Done when: the bitmap fixture asserts pixels equal the golden's within 1/255.
- [ ] Painterly brushstroke objects read as their pre-25 fallback bitmap with transparency, kept as a bitmap object with a report line. Done when: the brushstroke fixture asserts a bitmap object with alpha.
- [ ] Add `CmxReader` in `Formats/Cdr/`: CMX v5 to X6 in 16- and 32-bit variants through the same object model. Done when: `CmxReaderTests` render each CMX fixture within tolerance of its golden.
- [ ] Corel DESIGNER files that share the CDR container are read where compatible; others are refused by name. Done when: tests assert both outcomes.
- [ ] Extend `tests/fixtures/nodus/cdr/` with one file per fill, outline, text, and effect family plus CMX files, with goldens from Inkscape with libcdr (CMX through libcdr's CMX import), versions recorded. Done when: every new fixture has a golden.
- [ ] Commit: `"nodus: CorelDRAW fills, outlines, text, and effects, and the CMX reader"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~CdrStyleFidelityTests|FullyQualifiedName~CdrEffectMappingTests|FullyQualifiedName~CmxReaderTests"` exits 0: each style and effect fixture renders within tolerance of its Inkscape with libcdr golden, and the live-effect fixtures reopen as live objects (asserted by type). Cheaper substitute that fails: expanding every effect, which the live-type assertion catches.

## 8. CorelDRAW CDR and CMX Export

Returning a file to a CorelDRAW user needs a CDR writer. No open writer exists, so Nodus writes the RIFF layout libcdr reads, and the proof is a read-back through Nodus and through Inkscape with libcdr; opening in CorelDRAW itself is an operator check recorded as a risk, not a gate. Catalog: NP-2291 to NP-2298 (8 features).

**Freeze check:** Saving as CDR or CMX writes through the atomic writer to the chosen path; a save to an earlier version with "Ask when saving to an earlier version" on shows the prompt before writing, and Cancel writes nothing; a failed write leaves any existing target byte-identical; the open SVG document's own file is never written by a CDR save. Fixture source: `tests/fixtures/nodus/cdr/export/` (created by this section).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/cdr-export/.
**Job:** a designer can return a file to a CorelDRAW user. Consumer: the written CDR or CMX file and whoever opens it.
**Treatment:** a CDR Save Options dialog (version, keep appearance or keep editable, advanced compression and rebuild options, save CMX alongside, reference info) and an ask-on-earlier-version prompt. Cheaper substitute that fails the checkpoint: exporting SVG and telling the recipient to import it.
**Chrome:** consume the settings store and the `D02 T06 §14` export dialog shell. Do not add a second options framework.

**Requires:** display-session -- the options dialog and prompt need an interactive desktop

- [ ] Spike and record in `docs/dev/decisions.md` the earliest CDR version libcdr reads fully, which becomes the writer's target layout. Done when: the row names the version and the libcdr commit tested.
- [ ] Add `CdrWriter` in `src/Nodus/Photon.Nodus.Core/Formats/Cdr/`: RIFF writer for pages, layers, groups, curves, fills, outlines, text, and bitmaps. Done when: `CdrWriteReadBackTests` read each export fixture back through §6 and §7 to the same model.
- [ ] Save to an earlier version: keep appearance expands features the version lacks (brushstrokes to bitmaps, live effects to curves), keep editable writes the nearest editable form; the choice is per save. Done when: tests assert both modes on a fixture with a live effect.
- [ ] Advanced save options: compress bitmap effects, compress vector objects, store or rebuild texture fills, store or rebuild blends and extrusions, and save CMX alongside. Done when: a test per option asserts its effect on the written chunks.
- [ ] Reference info (title, subject, keywords, rating) writes to the CDR `INFO` records and reads back through §6. Done when: a round-trip test asserts all four fields.
- [ ] Settings `Nodus.Formats.Cdr.Export.DefaultVersion` and `Nodus.Formats.Cdr.Export.AskOnEarlierVersion` (default on), consumed by the save flow. Done when: a settings readback and a prompt test pass.
- [ ] Add `CmxWriter`: CMX 32-bit with RGB, CMYK, and named spot colors (no PANTONE data bundled). Done when: a CMX export reads back through §7's `CmxReader` to the same model.
- [ ] Add the CDR Save Options dialog and the earlier-version prompt. Done when: a view-model test asserts Cancel writes nothing; capture committed.
- [ ] Record the interoperability risk with CorelDRAW itself in the section's user guide page; no CorelDRAW-authored golden is claimed. Done when: the page names the risk.
- [ ] Log `Exported CDR {Path} v{Version} ({Mode})`. Done when: the line is asserted.
- [ ] Add `CdrLibcdrReadBackTests`: Inkscape with libcdr imports each written file and renders it within tolerance of Nodus's own render, marked with the Inkscape version; skipped by name when Inkscape is not installed. Done when: the tests pass on a machine with Inkscape 1.4 and report the skip reason otherwise.
- [ ] Commit: `"nodus: save CorelDRAW CDR and CMX files proven by libcdr read-back"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~CdrWriteReadBackTests|FullyQualifiedName~CdrLibcdrReadBackTests"` exits 0 on a machine with Inkscape 1.4: every export fixture reads back through §6 and §7 to the same model and renders through Inkscape with libcdr within tolerance (version quoted); the dialog capture is committed. Cheaper substitute that fails: a writer tested only by Nodus's own reader, which a symmetric bug passes and the libcdr read-back catches.

## 9. EPS and PostScript Import and Export

EPS still arrives from print shops and still goes to legacy RIPs. Illustrator-flavored EPS reads through the §4 AI interpreter; other EPS and PS or PRN files go through a user-installed Ghostscript run as an external process, never bundled (Ghostscript is AGPL-3.0), and refused by name when absent; or EPS is placed with its preview. The writer is Nodus's own on the `D02 T13 §10` PostScript emitter. The PostScript fixtures need Ghostscript 10.x installed on the test machine and are skipped by name otherwise. Catalog: NP-2299 to NP-2303 (5 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/eps/.
**Job:** a print shop's EPS logo opens as editable art, and a designer can send EPS to a legacy RIP. Consumer: the document on import; the written EPS and the RIP on export.
**Treatment:** an EPS Import dialog (editable or placed with preview, text as text or curves) and an EPS Export dialog with General and Advanced tabs, plus a Ghostscript location setting that says when Ghostscript is absent. Cheaper substitute that fails the checkpoint: bundling Ghostscript.
**Chrome:** consume the `D02 T13 §10` PostScript emitter, the settings store, and `Photon.UI` dialogs. Do not add a second PostScript emitter.

**Requires:** display-session -- the dialogs need an interactive desktop

- [ ] Add `EpsReader` in `src/Nodus/Photon.Nodus.Core/Formats/Eps/`: DOS EPS binary header (TIFF or WMF preview), `%%BoundingBox`, and `%%Creator: Adobe Illustrator` detection routing to the §4 interpreter. Done when: `EpsImportTests` route the Illustrator fixture to §4 and read the bounding box of the generic one.
- [ ] Add `GhostscriptBridge` in `Formats/Eps/`: find `gswin64c.exe` from `Nodus.Formats.Ghostscript.Path` or the registry, run it as an external process with `-dSAFER -sDEVICE=pdfwrite`, then import the PDF through §2. Done when: `GhostscriptBridgeTests` convert the generic fixture on a machine with Ghostscript 10.x.
- [ ] Record the Ghostscript decision in `docs/dev/decisions.md`: AGPL-3.0, never bundled, optional external tool. Done when: the row exists.
- [ ] With Ghostscript absent, import refuses by name ("PostScript import needs Ghostscript, which is not installed. Set its location in Preferences, Files.") and offers Place with Preview. Done when: `GhostscriptBridgeTests.Absent_RefusesByName` asserts the sentence with a fake locator.
- [ ] PS and PRN multi-page files import as pages or groups, with text as text or curves. Done when: the two-page PS fixture imports as two pages.
- [ ] Place EPS keeps the file linked with its preview through `D02 T12 §7` and prints the original PostScript through `D02 T13 §10`. Done when: a test asserts the link and the preview bitmap.
- [ ] Add `EpsWriter` on the `D02 T13 §10` emitter with general options: color output (Native, RGB, CMYK, Gray), convert spots, preview (None, TIFF 8-bit, TIFF 1-bit, transparent), text as curves, include fonts, PostScript level 2 or 3, and transparency flattening. Done when: `EpsWriterTests` assert each option's effect on the written header or body.
- [ ] Advanced options: bounding box (objects, page, bleed, crop marks), JPEG bitmap compression, preserve overprints and overprint black, and auto-increase fountain steps; OPI links recorded as not written. Done when: tests assert each option.
- [ ] Enable the EPS in PDF option `D02 T13 §15` added to the PDF presets disabled with the tooltip `Planned: D02 T14 §9`: a placed EPS writes as a PostScript XObject or as its preview per the preset, and the tooltip is removed. Done when: `PdfPresetStoreTests` assert the option is enabled, a PDF exported with a placed EPS carries the XObject or the preview image read back with PdfPig, and `MenuAuditTests` no longer find the tooltip.
- [ ] Illustrator EPS version choice writes the §5 legacy header. Done when: a test asserts the `%%Creator` and version comments.
- [ ] Settings `Nodus.Formats.Eps.*` with defaults, each read by the reader or writer. Done when: a settings readback asserts each default.
- [ ] Add the EPS Import and EPS Export dialogs and the Ghostscript location field. Done when: a view-model test asserts the absent-state message; captures committed.
- [ ] Log `Imported EPS {Path} ({Route})` and `Exported EPS {Path} (level {Level})`. Done when: both lines are asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/eps/` (Illustrator EPS, a generic EPS, a two-page PS) with goldens from Ghostscript 10.x `png16m` renders, version recorded. Done when: every fixture has a golden.
- [ ] Commit: `"nodus: EPS and PostScript import through Ghostscript, and an own EPS writer"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~EpsImportTests|FullyQualifiedName~EpsWriterTests|FullyQualifiedName~GhostscriptBridgeTests"` exits 0: on a machine with Ghostscript 10.x, EPS written by Nodus renders through Ghostscript within tolerance of Nodus's own render and each import fixture matches its Ghostscript golden; with Ghostscript absent the import refuses with the named message (asserted) and the Ghostscript-dependent cases report their skip reason. Cheaper substitute that fails: importing only the TIFF preview, which the vector-count assertion catches.

## 10. DXF and DWG Import and Export

Engineers' drawings must open at true scale with layers and dimensions, and cut paths must go back to CAD. ACadSharp (MIT) reads and writes both DXF and DWG in managed code. Catalog: NP-2304 to NP-2305 (2 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/cad/.
**Job:** an engineer's drawing opens at true scale with layers and dimensions, and a cut path goes back to CAD. Consumer: the document on import; the written DXF or DWG on export.
**Treatment:** a CAD Import dialog (layout, scale, units, scale lineweights, center or fit to artboard, merge layers, auto-reduce nodes) and a CAD Export dialog (version, units, scale, text as curves, bitmap format, unmapped fill color, group as block). Cheaper substitute that fails the checkpoint: DXF R12 only.
**Chrome:** consume the settings store and the `D02 T08 §15` dimension model. Do not add a second dimension type.

**Requires:** display-session -- the dialogs need an interactive desktop

- [ ] Add ACadSharp (MIT) to `Directory.Packages.props` and `Photon.Nodus.Core` with its `docs/dev/decisions.md` row. Done when: the build is green and the row names the license URL.
- [ ] Add `CadReader` in `src/Nodus/Photon.Nodus.Core/Formats/Cad/`: lines, polylines (bulges to arcs), circles, arcs, ellipses, splines to Beziers, hatches to fills, text and mtext, inserts to symbols, and layers with color and linetype. Done when: `CadImportFidelityTests` assert entity counts per kind on each fixture.
- [ ] Lineweights, model space or a chosen paper layout, and 3D entities projected to the XY view. Done when: the layouts fixture imports the chosen layout only.
- [ ] Dimensions (linear, aligned, angular, radial) become `D02 T08 §15` dimension objects, keeping associativity where the source has it. Done when: `CadDimensionMappingTests` assert the type and measured value of each dimension.
- [ ] Units from `$INSUNITS` with the scale option (Automatic, English, Metric, custom ratio) and scale lineweights on or off. Done when: a millimetre fixture imports at true size within 1e-6 drawing units.
- [ ] Import options: center or fit to artboard, merge layers, and auto-reduce nodes. Done when: tests assert each.
- [ ] Add `CadWriter`: versions R12 to 2018 as ACadSharp supports, outlines only, text as text or curves, bitmaps embedded in a chosen raster format or dropped, unmapped fills as a color or unfilled, groups as blocks, and selected art only. Done when: `CadExportRoundTripTests` write, read back through ACadSharp, and compare entity counts and geometry within 1e-6 drawing units.
- [ ] Settings `Nodus.Formats.Cad.Import.*` and `Nodus.Formats.Cad.Export.*`, each read by the reader or writer. Done when: a settings readback asserts each default.
- [ ] Add the CAD Import and CAD Export dialogs. Done when: view-model tests assert option binding; captures committed.
- [ ] Log `Imported CAD {Path} ({Entities} entities, {Dimensions} dimensions)` and `Exported CAD {Path} {Version}`. Done when: both lines are asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/cad/` (DXF and DWG per version family with dimensions, hatches, blocks, and layouts), with DXF goldens rendered by LibreCAD 2.2 (GPL-2.0, run as a tool, never bundled; version recorded); DWG is proven by ACadSharp round trips because the ODA tools' license does not allow their use in CI. Done when: the README records both decisions.
- [ ] Commit: `"nodus: DXF and DWG import and export with live dimensions"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~CadImportFidelityTests|FullyQualifiedName~CadExportRoundTripTests|FullyQualifiedName~CadDimensionMappingTests"` exits 0: DXF fixtures render within tolerance of the LibreCAD golden, DWG and DXF exports round-trip through ACadSharp with identical entity counts and geometry, and dimension fixtures reopen as live dimensions. Cheaper substitute that fails: exploding dimensions to lines, which the type assertion catches.

## 11. EMF, WMF, CGM, HPGL, and WPG

Clip art, plotter, and cutter files still circulate, and EMF is also the Office editing target (§14) and a clipboard flavor (§19). Nodus reads and writes each with its own code from the published specifications. Catalog: NP-2306 to NP-2310 (5 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/metafiles/.
**Job:** clip art, plotter, and cutter files open, and outlines go to a plotter or cutter. Consumer: the document on import; the written file and the device on export.
**Treatment:** one small options dialog per format that has options (HPGL import pen mapping, HPGL export pens and origin, CGM version and encoding, WPG version and colors), and none for EMF and WMF. Cheaper substitute that fails the checkpoint: rasterizing metafiles through WPF.
**Chrome:** consume the `D02 T06 §14` export dialog shell and the settings store. Do not add a per-format dialog framework.

**Requires:** display-session -- the options dialogs need an interactive desktop

- [ ] Add `EmfReader` in `src/Nodus/Photon.Nodus.Core/Formats/Metafile/` from [MS-EMF]: paths, polys, beziers, brushes, pens, text, bitmaps, clipping, and world transform; EMF+ records render through their EMF fallback with a report line. Done when: `MetafileFidelityTests` render each EMF fixture within tolerance of its golden.
- [ ] Add `WmfReader` from [MS-WMF], including the placeable header. Done when: each WMF fixture renders within tolerance.
- [ ] Add `EmfWriter` and `WmfWriter` (placeable WMF header), text kept as text, hairlines for thin strokes. Done when: `MetafileWriterRoundTripTests` re-import each through Nodus and through Inkscape within tolerance.
- [ ] Add `CgmReader` and `CgmWriter`: ISO 8632 binary and clear-text encodings, versions 1, 3, and 4, the WebCGM 1.0 profile on write. Done when: CGM fixtures render within tolerance of the LibreOffice golden and written files re-import.
- [ ] Add `HpglReader`: HP-GL and HP-GL/2 (PU, PD, PA, PR, AA, CI, SP, LT, PW, VS), scale, curve resolution, 256 pens mapped to colors, widths, and velocity, and a pen library reset. Done when: the PLT fixtures import with the mapped pen colors.
- [ ] Add `HpglWriter`: outlines only, curves flattened to segments at a tolerance, the pen table, and the plotter origin including top left. Done when: a written PLT re-imports within the flattening tolerance.
- [ ] Add `WpgReader` and `WpgWriter`: WPG 1.0 and 2.0, 16 or 256 colors, text as text or curves. Done when: WPG fixtures render within tolerance and written files re-import.
- [ ] Settings `Nodus.Formats.<Emf|Wmf|Cgm|Hpgl|Wpg>.*`, each read by its reader or writer. Done when: a settings readback asserts each default.
- [ ] Add the HPGL, CGM, and WPG options dialogs. Done when: view-model tests assert option binding; captures committed.
- [ ] Log `Imported {Format} {Path} ({Objects} objects)` and `Exported {Format} {Path}`. Done when: both lines are asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/metafile/` (EMF, WMF, CGM, PLT, WPG) with goldens from Inkscape 1.4 (EMF and WMF via libUEMF, WPG via libwpg, HPGL export as the writer oracle) and LibreOffice 25.x `soffice --convert-to png` for CGM, versions recorded. Done when: every fixture has a golden.
- [ ] Commit: `"nodus: EMF, WMF, CGM, HPGL, and WPG readers and writers"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~MetafileFidelityTests|FullyQualifiedName~MetafileWriterRoundTripTests"` exits 0: each reader fixture renders within tolerance of its named golden, and each writer's output re-imports through the reference implementation within tolerance. Cheaper substitute that fails: a writer proven only by Nodus's own reader, which a symmetric bug passes.

## 12. Raster Formats: Import and Export Through WIC

Any common image must place at the right size, and any page must export to the raster format a client asks for. WIC through WPF's `BitmapDecoder` and `BitmapEncoder` covers most formats with no dependency; WebP goes through SkiaSharp, AVIF and HEIF through the Windows Store extensions (refused by name when absent), and TGA and PCX through Nodus's own codecs. The codec lives in `Photon.Nodus.Desktop` until Imago's codec decision (`D03 T04 §1`) picks the same stack, when it moves to `Photon.Core`. Catalog: NP-2311 to NP-2331 (21 features).

**Fidelity:** docs/captures/nodus/export-raster/ (from `D02 T04 §3`), extended; the import surfaces are new build, no baseline, captured to docs/captures/nodus/raster-import/.
**Job:** a designer can place any common image at the right size and export any page to the raster format a client asks for. Consumer: the document's bitmap objects on import; the written files on export.
**Treatment:** the Import button's split menu (Import, Resample and Load, Crop and Load) with a crop preview, TIFF page and GIF frame pickers, and per-format export options pages in the one export dialog. Cheaper substitute that fails the checkpoint: one generic PNG-only path.
**Chrome:** consume the `D02 T04 §3` `RasterExporter`, the `D02 T06 §14` dialog, and the `D02 T12 §1` bitmap objects. Do not add a second raster pipeline.

**Requires:** display-session -- the dialogs and crop preview need an interactive desktop

- [ ] Add `WicCodec` in `src/Nodus/Photon.Nodus.Desktop/Formats/Raster/` over WPF `BitmapDecoder` and `BitmapEncoder` for BMP, GIF, JPEG, PNG, TIFF, ICO, and WMP; decoded frames become `D02 T12 §1` bitmap objects. Done when: `RasterDecodeFidelityTests` pass for each WIC format.
- [ ] WebP decode and encode through SkiaSharp. Done when: the WebP fixtures decode within tolerance and a written WebP decodes in ImageMagick to the source pixels within the stated PSNR.
- [ ] AVIF and HEIF (HEIC key image) through the WIC Store extensions, probed at startup; absent extensions are refused by name with the Store link text, never a crash. Done when: a test with the probe faked absent asserts the sentence, and on a machine with the extensions the fixtures decode.
- [ ] Add `TgaCodec` in `src/Nodus/Photon.Nodus.Core/Formats/Raster/` (8-bit gray to 32-bit, RLE, Normal or Enhanced). Done when: TGA fixtures decode pixel-exact and written files decode in ImageMagick to the source pixels.
- [ ] Add `PcxCodec` (versions 2.5 to 3.0, RLE, paletted through `D01 T03 §3`). Done when: PCX fixtures decode pixel-exact and round-trip.
- [ ] BMP variants: Windows BMP, DIB, RLE, and OS/2 v1.3 and v2.0 through an own header shim where WIC declines. Done when: each BMP variant fixture decodes pixel-exact.
- [ ] CUR import through the ICO decoder path, keeping the hotspot in object notes. Done when: the CUR fixture decodes and its hotspot is recorded.
- [ ] JPEG 2000: WIC has no JP2 codec; record in `docs/dev/decisions.md` the choice between CoreJ2K (BSD, managed) and OpenJPEG (BSD-2, native P/Invoke), with export quality and progression options; if neither is taken, JP2 is refused by name. Done when: the row exists and either the JP2 fixtures decode or the refusal is asserted.
- [ ] GIF import including animated frames (frame picker) and GIF export with transparency. Done when: an animated fixture exposes its frame count and a written GIF keeps the transparent index.
- [ ] JPEG import in gray, RGB, and CMYK with EXIF orientation, CMYK converting through `D01 T04 §1`. Done when: the CMYK fixture matches its golden within the stated tolerance and the rotated fixture places upright.
- [ ] PNG import with masks and transparency, including 16-bit. Done when: the 16-bit alpha fixture decodes within 1/65535 per channel.
- [ ] TIFF page selection on import and TIFF export options (compression, byte order, embed ICC). Done when: a multi-page fixture imports the chosen page and each export option is asserted in the written tags.
- [ ] Load partial file: a frame range from a multi-frame image. Done when: importing frames 2 to 3 of the fixture creates two bitmap objects.
- [ ] Combine the layers of a multi-layer bitmap on import (an option), else each layer becomes an object. Done when: a multi-layer TIFF imports both ways.
- [ ] Resample and Load (width, height, percent, resolution, maintain aspect). Done when: a test asserts the placed pixel size.
- [ ] Crop and Load with a numeric and handle-based crop preview. Done when: a test asserts the cropped pixel region equals the golden crop.
- [ ] Check for watermark reads EXIF, IPTC, and XMP copyright fields and shows them on import; no proprietary watermark detection (recorded). Done when: the fixture with a copyright field shows it in the import toast.
- [ ] Export options per format: color mode, resolution, anti-alias, transparency, and compression type where the format supports it, each on its page in the one export dialog. Done when: `RasterEncodeRoundTripTests` assert each option in the written file.
- [ ] Export notes written to the file's metadata (XMP description or PNG `tEXt`). Done when: a test reads the note back with ImageMagick.
- [ ] Hidden layers export unless the `D02 T07 §5` layer export flag is off. Done when: a test with one hidden exporting layer and one flagged off asserts the pixels.
- [ ] Settings `Nodus.Formats.Raster.<Format>.*`, each read by its codec. Done when: a settings readback asserts each default.
- [ ] Budget: a 100-megapixel TIFF places in under three seconds with progress and Cancel. Done when: a timing test on the generated fixture asserts the budget.
- [ ] Log `Placed {Format} {Path} ({Width}x{Height})` and `Exported {Format} {Path}`. Done when: both lines are asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/raster/` (one per format and variant: paletted, 16-bit, CMYK JPEG, multi-page TIFF, animated GIF, OS/2 BMP, RLE TGA, PCX, CUR) with decode goldens from ImageMagick 7 (`magick <file> rgba:`), version recorded. Done when: every fixture has a golden.
- [ ] Commit: `"nodus: raster import and export through WIC and own TGA and PCX codecs"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~RasterDecodeFidelityTests|FullyQualifiedName~RasterEncodeRoundTripTests|FullyQualifiedName~RasterImportOptionsTests"` exits 0: every decode fixture matches its ImageMagick golden (pixel-exact or within 1/255 for lossless, PSNR stated for lossy), and every writer's output decodes in ImageMagick to the source pixels; extension-gated cases report their skip or refusal by name. Cheaper substitute that fails: testing only PNG, which leaves TGA and PCX unproven.

## 13. Photoshop PSD Import and Export

Photoshop and Imago compositions arrive as layered PSD, and vector drawings go back layered. Nodus writes its own PSD reader and writer against Adobe's published specification. The reader lives in `Photon.Nodus.Core/Formats/Psd/` until Imago's PSD import (`D03 T04 §5`) needs it, when it moves to `Photon.Core` and Imago consumes it rather than building a second reader. Catalog: NP-2332 to NP-2335 (4 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/psd/.
**Job:** a Photoshop or Imago composition arrives as editable layers, and a vector drawing goes back layered. Consumer: the document on import; the written PSD on export.
**Treatment:** a PSD Import dialog (layer comp, layers to objects or flatten, import hidden layers, import slices) and PSD export options in the one export dialog. Cheaper substitute that fails the checkpoint: reading the composite image only.
**Chrome:** consume §12's bitmap path, the `D02 T12 §7` Links panel for linked PSD, and the settings store. Do not add a second bitmap decoder.

**Requires:** display-session -- the dialog needs an interactive desktop

- [ ] Add `PsdReader` in `src/Nodus/Photon.Nodus.Core/Formats/Psd/`: header, color modes (bitmap, gray, indexed, RGB 8 and 16, CMYK, Lab, duotone), layer and mask info, RLE and raw channels, and layer groups. Done when: `PsdReaderTests` parse each section of the fixtures.
- [ ] Masks, opacity, and blend modes mapped to Nodus blend modes; layer comps and slices read. Done when: a fixture with one layer per blend mode imports with the mapped modes.
- [ ] Spot channels become `D01 T04 §3` DeviceN bitmaps. Done when: the spot fixture keeps its ink names.
- [ ] Layers become bitmap objects in groups; text layers import as rasters with their string kept in object notes; shape layers import their vector masks as paths. Done when: the fixture's layer tree equals the psd-tools dump.
- [ ] Import options: layer comp, layers to objects or flatten, import hidden layers, import slices, persisted under `Nodus.Formats.Psd.Import.*`. Done when: tests assert each option.
- [ ] Place linked PSD keeps the link and the chosen comp through `D02 T12 §7`; comps switch from the placed object's properties. Done when: a test switches comps and asserts the relinked pixels.
- [ ] Add `PsdWriter`: flat or layered, color model, resolution, anti-alias, embed ICC, spot channels kept, text rasterized, and the maximum-compatibility composite always written. Done when: `PsdWriterReadBackTests` read written files back through Nodus and through psd-tools with the same layer count.
- [ ] Clipboard exchange with raster editors: paths as SVG and AICB flavors (§19), pixels as PNG and DIB; Imago is the first partner. Done when: a clipboard test asserts all four flavors.
- [ ] Add the PSD Import dialog and the PSD page in the export dialog. Done when: view-model tests assert binding; captures committed.
- [ ] Log `Imported PSD {Path} ({Layers} layers)` and `Exported PSD {Path} ({Mode})`. Done when: both lines are asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/psd/` (layered RGB, CMYK, 16-bit, duotone, with comps and masks) with goldens from psd-tools (MIT) layer dumps and GIMP 3.0 composites, versions recorded. Done when: every fixture has both goldens.
- [ ] Commit: `"nodus: layered PSD import and export against the published specification"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~PsdReaderTests|FullyQualifiedName~PsdWriterReadBackTests"` exits 0: each fixture's layer tree equals the psd-tools dump and its composite matches the GIMP golden within tolerance, and written PSDs read back in psd-tools and GIMP with the same layer count. Cheaper substitute that fails: the flattened composite, which the layer-tree assertion catches.

## 14. Office and Text Documents, Export For Office, and Font Export

Designers pull a client's copy deck into a layout and put artwork into Word or PowerPoint. This section imports TXT, RTF, DOC, DOCX, XLS, XLSX, and CSV, exports text as TXT, RTF, and DOC, adds the Export For Office dialog, and exports a curve as a TrueType or Type 1 glyph. DocumentFormat.OpenXml (MIT) handles OOXML and NPOI (Apache-2.0) the binary DOC and XLS; binary PPT, PUB, VSD, and WPD are backlog B-037, and VSDX and PPTX import have no catalog row and are filed through `add-todo` rather than built here. Catalog: NP-2336 to NP-2350 (15 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/export-for-office/.
**Job:** a designer can put artwork into a Word or PowerPoint file and pull a client's copy deck into a layout. Consumer: the document on import; Office applications through the written file or the clipboard.
**Treatment:** an Export For Office dialog (target: compatibility PNG, editing EMF, WordPerfect WPG; optimized for presentation 96, desktop 150, or commercial 300 dpi; preview with zoom, pan, and estimated size). Cheaper substitute that fails the checkpoint: a plain PNG export.
**Chrome:** consume §11's EMF and WPG writers, §12's PNG path, the `D02 T10 §13` text import dialog, and `Photon.UI` preview controls. Do not add a second text importer.

**Requires:** display-session -- the dialog and preview need an interactive desktop

- [ ] Add DocumentFormat.OpenXml (MIT) and NPOI (Apache-2.0) with `docs/dev/decisions.md` rows. Done when: the build is green and each row names its license URL.
- [ ] Add `OfficeTextReader` in `src/Nodus/Photon.Nodus.Core/Formats/Office/`: DOCX through OpenXml, DOC through NPOI HWPF, RTF by an own parser, and TXT with encoding detection, into the `D02 T10 §13` importing-text flow (keep fonts and formatting, or plain). Done when: `OfficeImportTests` assert text runs and formatting equal the LibreOffice goldens.
- [ ] Add `SpreadsheetReader`: XLS and XLSX through NPOI and CSV through the one Nodus CSV reader `D02 T13 §13` added (`src/Nodus/Photon.Nodus.Core/Merge/Readers/CsvReader.cs`), never a second parser, into `D02 T10 §14` tables; linked workbooks stay linked through `D02 T12 §7`. Done when: table cells equal the LibreOffice CSV golden for each fixture.
- [ ] Export text as TXT (all text objects in reading order). Done when: the TXT export of the fixture equals its golden.
- [ ] Export text objects as RTF (own writer) and DOC (NPOI, Word 97 binary; Word 6 and 7 recorded as not written). Done when: both read back through `OfficeTextReader` with the same runs.
- [ ] Add `ExportForOfficeDialog` with targets PNG (§12), EMF (§11), and WPG (§11), and layers flattened on export. Done when: `ExportForOfficeTests` assert the written format per target.
- [ ] Optimization: presentation 96, desktop 150, or commercial 300 dpi. Done when: the written dimensions equal the artwork size times the chosen dpi (asserted).
- [ ] Preview with zoom and pan, and an estimated size from a trial encode. Done when: a test asserts the estimate is within 5 percent of the written size; capture committed.
- [ ] Office copy: the clipboard carries EMF, PNG, and SVG flavors (§19) so Word and PowerPoint paste editable or faithful art. Done when: a clipboard test asserts the three flavors.
- [ ] Insert into office documents by file or clipboard; an OLE server is recorded as not built in `docs/dev/decisions.md`. Done when: the row exists and the user guide describes both routes.
- [ ] Add `GlyphExporter`: a combined curve exported as one unhinted glyph in a TTF (own `glyf`, `cmap`, `hmtx` writer), fills and outlines ignored, with character code, advance, and family name. Done when: `GlyphExportTests` load the TTF in `GlyphTypeface` and its outline matches the source curve within 1 font unit.
- [ ] Type 1 PFB glyph export (own charstring encoder). Done when: the fontTools `ttx` dump of the written font equals the golden.
- [ ] Missing-reader warning: a refused office format shows a warning, controlled by `Nodus.Formats.Office.WarnOnRefused` (re-enabled from settings). Done when: a test asserts the warning and the setting.
- [ ] Log `Imported {Format} {Path} ({Runs} runs, {Tables} tables)` and `Exported for Office {Path} ({Target}, {Dpi} dpi)`. Done when: both lines are asserted.
- [ ] Commit fixtures `tests/fixtures/nodus/office/` (DOCX, DOC, RTF, XLS, XLSX, CSV) with text and table goldens from LibreOffice 25.x `--convert-to txt` and `csv`, and glyph fixtures checked with fontTools `ttx` dumps, versions recorded. Done when: every fixture has a golden.
- [ ] Commit: `"nodus: office document import, Export For Office, and glyph export"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~OfficeImportTests|FullyQualifiedName~ExportForOfficeTests|FullyQualifiedName~GlyphExportTests"` exits 0: each office fixture imports with text runs and table cells equal to the LibreOffice golden, Export For Office writes the target format at the chosen resolution (dimensions asserted), and exported glyphs round-trip through fontTools and `GlyphTypeface`. Cheaper substitute that fails: plain-text import, which the formatting-run assertion catches.

## 15. Export for Screens, Asset Export, and the Export List

UI designers export every artboard and icon at several scales and formats in one action and re-export after edits. This section adds Export As with artboards, pages, and range; the export list panel with per-item format, destination, and settings bound to objects; the Export for Screens dialog; and background export with progress. The items are grouped as the design names them (A: Export As, B: export items and the list, C: Export for Screens) to stay inside the section cap; if it overruns during implementation, the natural split is Export As plus Export for Screens versus the export list panel. Catalog: NP-2407 to NP-2437 (31 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/export-for-screens/ and docs/captures/nodus/export-list/.
**Job:** a UI designer can export every artboard and icon at 1x, 2x, and 3x in PNG, SVG, and WebP in one action, and re-export after edits. Consumer: the written files and the document's persisted export items.
**Treatment:** an Export for Screens dialog with Artboards and Assets tabs and a format-scale grid, plus a dockable Export panel listing pages and objects with checkboxes, rename, suffix, format, destination, and settings. Cheaper substitute that fails the checkpoint: repeating Export As per file.
**Chrome:** consume the `D02 T06 §14` export dialog and writers, the `D02 T07 §3` artboard model, the settings store, and `Photon.UI` panels and progress. Do not duplicate the per-format options pages.

**Requires:** display-session -- the dialog, panel, and background export need an interactive desktop

- [ ] Group A: add `ExportAsCommand` with use artboards or pages, range text (`1-3, 5`), and export a page range with each page to its own file (NP-2409, NP-2422). Done when: `ExportAsTests` assert the file set for a range.
- [ ] Group A: this page only, selected objects only, and crop to page options (NP-2420, NP-2424, NP-2425). Done when: tests assert the bounds of each output.
- [ ] Group A: skip the format options dialog on export (`Nodus.Export.As.SkipOptionsDialog`, NP-2426), and every other Export As option persisted under `Nodus.Export.As.*`. Done when: a settings readback asserts each default.
- [ ] Group B: add `ExportItem` in `src/Nodus/Photon.Nodus.Core/Export/` (target page, artboard, object, or selection; name; suffix; format; destination; per-format settings), persisted as `nodus:export-item` elements per `D02 T07 §1` and removed when their object is deleted (NP-2435). Done when: a round-trip test saves and reopens items, and deleting an object removes its item in the same undo step.
- [ ] Group B: add `ExportListService` with add selection (one item per object, NP-2410), add current page (NP-2419), add all pages as separate pages or a page range (NP-2427), remove (NP-2428), duplicate for alternate settings (NP-2429), add new assets reusing an item's settings (NP-2430), and select all. Done when: `ExportListServiceTests` cover each operation and its undo.
- [ ] Group B: default format for new items (`Nodus.Export.List.DefaultFormat`, NP-2434) and ordering pages first in document order then objects in Objects panel order (NP-2435). Done when: tests assert the default and the ordering.
- [ ] Group B: add `ExportPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/` (NP-2418) with inline rename, suffix, and select all (NP-2423), per-item format and destination pickers (NP-2431), a settings button opening the format page (NP-2432), and Export Checked or Export All (NP-2433). Done when: a view-model test exports checked items only; capture committed.
- [ ] Group B: the Layers panel "Collect for Export" (NP-2407) and the artboard context menu "Export Selected Artboards" (NP-2408) feed the list. Done when: tests assert both add the expected items.
- [ ] Group C: add `ExportForScreensDialog` (NP-2411) with the Artboards tab (all, range, full document, include bleed, NP-2412) and the Assets tab showing the list (NP-2413). Done when: a view-model test asserts the artboard selection sent to the exporter; capture committed.
- [ ] Group C: formats PNG, PNG-8, JPG 100, 80, 50, and 20, SVG, PDF, WebP, and TIFF (NP-2414). Done when: `ExportForScreensTests` write one file per format and read each header.
- [ ] Group C: scales 0.5x to 4x or a width, height, or resolution with suffixes, and iOS and Android presets (NP-2415). Done when: a test asserts the file names and pixel sizes for the iOS preset.
- [ ] Group C: sub-folders per scale or format, open location after export, and per-format settings (NP-2416). Done when: a test asserts the folder layout.
- [ ] Outline-aware bitmap bounds: centered and outside strokes and partial pixels included, inside strokes keep size, shared with §16 (NP-2436). Done when: `OutlineAwareBoundsTests` assert bounds for each stroke alignment.
- [ ] Duplicate a page into a new document through `D02 T07 §3` and the document window service (NP-2421). Done when: a test asserts the new document holds an equal page.
- [ ] Add `BackgroundExportQueue`: PNG and JPEG always, all formats when `Nodus.Export.Background` is on, off the UI thread, with a progress strip, Cancel, and a completion toast notification; no partial file is left on cancel (NP-2417). Done when: `BackgroundExportCancelTests` cancel mid-batch and assert no partial file exists.
- [ ] No export overwrites an existing file without a prompt (Replace, Keep Both, Skip, apply to all). Done when: a test asserts the prompt and each choice.
- [ ] Log one line per exported file and one summary line per batch (`Exported {Count} files in {ElapsedMs} ms`). Done when: both are asserted.
- [ ] Write the recommended import and export formats guide `docs/user/nodus/formats.md` listing which Nodus format to use per destination application (NP-2437). Done when: the page covers every format in this file.
- [ ] Budget: 100 artboards at three scales and three formats export in under a minute on the reference machine. Done when: a timing test on the generated fixture asserts the budget.
- [ ] Commit: `"nodus: Export As, the export list, Export for Screens, and background export"`

**Test checkpoint:** Driven run with evidence plus unit test: a driven Export for Screens run of a three-artboard fixture writes exactly the expected file set (names, and dimensions read from headers, quoted), and `dotnet test Photon.slnx --filter "FullyQualifiedName~ExportListServiceTests|FullyQualifiedName~ExportForScreensTests|FullyQualifiedName~OutlineAwareBoundsTests|FullyQualifiedName~BackgroundExportCancelTests|FullyQualifiedName~ExportAsTests"` exits 0; captures of the dialog and panel are committed. Cheaper substitute that fails: exporting only the first artboard at 1x, which the file-set assertion catches.

## 16. Export for Web: Optimized Preview and Web Formats

A web designer compares encodings side by side and ships the smallest file that looks right. This section adds the Export for Web dialog for GIF, PNG-8, PNG-24, JPEG, and WebP with comparison previews, presets, estimates, palette editing, and the transformation options. Catalog: NP-2438 to NP-2450 (13 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/export-for-web/.
**Job:** a web designer can compare encodings side by side and ship the smallest file that looks right. Consumer: the written web image and the HTML text flag §17 reads.
**Treatment:** a dialog with preview layouts (one, two vertical, two horizontal, four), zoom 1:1 and fit, pan, per-pane format settings, color table, size and download estimate, presets, and preview in browser. Cheaper substitute that fails the checkpoint: the plain export dialog with a quality slider.
**Chrome:** consume §12's encoders, the `D01 T03 §3` quantization and dithering, and `Photon.UI` zoom and pan controls. Do not add a second quantizer.

**Requires:** display-session -- the preview dialog needs an interactive desktop

- [ ] Add `ExportForWebDialog` and its view model in `src/Nodus/Photon.Nodus.Desktop/Views/Export/`: pane layouts, shared zoom and pan, per-pane encoder settings, and re-encode debounced and cancellable. Done when: a view-model test asserts a settings change re-encodes only its pane; capture of the four-up layout committed.
- [ ] Add `WebEncoderSettings` for GIF and PNG-8 (palette algorithm, colors, dither type and amount, web snap, lossy, transparency, transparent sampled color, matte, interlace). Done when: `WebEncoderTests` assert palette size and transparency index in the written files.
- [ ] Web JPEG settings (quality, optimized, progressive, blur, matte, embed ICC), and PNG-24 and WebP settings (quality, lossless, alpha). Done when: tests assert each setting's effect and that size decreases monotonically with quality.
- [ ] Progressive JPEG needs an encoder WIC lacks: record the decision (a small own progressive encoder, or refused by name) in `docs/dev/decisions.md`. Done when: the row exists and the test asserts the chosen behavior.
- [ ] Palette editing in the color table: load, sample, add, edit, delete, and lock colors, through `D01 T03 §3`. Done when: a test locks a color and asserts it survives re-quantization.
- [ ] Matte color for anti-aliased edges and transparent background or a sampled color in paletted output. Done when: `WebEncoderTests.Matte` asserts the blended edge pixels.
- [ ] Anti-aliased and interlaced output options. Done when: a test asserts the interlace flag in the written PNG and GIF.
- [ ] Transformation: resize by units, width, height, percent, or resolution with aspect lock, and crop to page. Done when: a test asserts the output pixel size for each mode.
- [ ] Color mode and embedded profile through `D01 T04 §1`. Done when: a test asserts the embedded ICC in the JPEG.
- [ ] Estimates: file size from the actual encode and download time at `Nodus.Export.Web.ConnectionSpeed`. Done when: `WebEstimateTests` assert the size equals the encoded byte count and the time equals size over speed.
- [ ] Presets: apply, save, load, and delete, stored in the settings store (`Nodus.Export.Web.Presets`). Done when: `ExportForWebPresetTests` cover each operation.
- [ ] Preview in browser writes a temporary HTML page and opens it with the default browser. Done when: a test asserts the temp page references the encoded image.
- [ ] Make text web-compatible marks paragraph text for HTML output (`nodus:web-text`), read by §17's HTML writer. Done when: a round-trip test asserts the attribute survives save.
- [ ] Log `Exported for web {Path} ({Format}, {Bytes} bytes)`. Done when: the line is asserted.
- [ ] Commit: `"nodus: Export for Web with comparison previews, palettes, and presets"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~WebEncoderTests|FullyQualifiedName~ExportForWebPresetTests|FullyQualifiedName~WebEstimateTests"` exits 0, each encoder's output decoding in ImageMagick 7 to the expected palette size and pixels within the stated tolerance; a driven four-up capture is committed. Cheaper substitute that fails: a single preview pane, which the driven capture shows.

## 17. Slices, Image Maps, Hyperlinks, Rollovers, and SVG Interactivity

Designers cut pages into web slices, link objects, and make hover states without hand-writing HTML. Slices, links, bookmarks, and rollovers are document objects persisted through the `nodus:` namespace and written to SVG, HTML, and PDF. SVG event attributes and linked scripts are written, never executed. The items are grouped in four blocks (A slices, B links, C rollovers, D SVG interactivity). Catalog: NP-2451 to NP-2472 (22 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/slices/ and docs/captures/nodus/links-rollovers/.
**Job:** a designer can cut a page into web slices, link objects, and make hover states without hand-writing HTML. Consumer: the written SVG, HTML, and PDF, and the document's persisted slices and links.
**Treatment:** Slice and Slice Selection tools with numbered overlays, an Object, Slice menu, a Slice Options dialog, a Links and Rollovers panel (links, bookmarks, hotspot, alt text, rollover states), and an SVG Interactivity panel. Cheaper substitute that fails the checkpoint: a URL field on the object properties only.
**Chrome:** consume the shared icon catalog, the tool registration, the settings store, the suite history, and `Photon.UI` panels. Do not add a second overlay renderer.

**Requires:** display-session -- tools, overlays, panels, and live preview need an interactive desktop

- [ ] Group A: add the `Slice` model in `src/Nodus/Photon.Nodus.Core/Web/` (user or object-based; type Image, No Image, or HTML Text; name, URL, target, message, alt text, background), persisted as `nodus:slice` per `D02 T07 §1`. Done when: a round-trip test saves and reopens every field.
- [ ] Group A: add `SliceTool` (Shift+K) and `SliceSelectionTool` in `Photon.Nodus.Core/Tools/`, registered through the composition root. Done when: tool tests draw and select a slice.
- [ ] Group A: slice commands make, release, create from guides, create from selection, duplicate, combine, divide, delete all, and clip to artboard, each an undoable command. Done when: `SliceCommandTests` cover each command and its undo.
- [ ] Group A: show, hide, and lock slices. Done when: tests assert visibility and that locked slices refuse edits.
- [ ] Group A: add the Slice Options dialog for the model's fields. Done when: a view-model test asserts binding; capture committed.
- [ ] Group A: the slice overlay draws numbers and lines per `Nodus.Slices.ShowNumbers` and `Nodus.Slices.LineColor`. Done when: a settings readback and a capture show both.
- [ ] Group A: Save Selected Slices writes each slice through §16's encoder settings plus an optional HTML table. Done when: `SliceExportTests` assert the file set and the HTML table cells.
- [ ] Group B: extend the `Hyperlink` model `D02 T13 §16` added (`src/Nodus/Photon.Nodus.Core/Models/Hyperlink.cs`, http, https, mailto, file) with the ftp and bookmark schemes, add `Bookmark`, and carry both on objects and on text runs (the `D02 T10 §2` hyperlink field); never a second hyperlink type. Done when: model tests cover each scheme and a text-run link, and the `D02 T13 §16` round-trip test still passes.
- [ ] Group B: hotspot by shape or bounding box, and alternate text on linked objects. Done when: tests assert the hotspot region and alt text in the output.
- [ ] Group B: verify opens the link with the default handler; delete removes it and its bookmark references, as one undoable command. Done when: a test asserts delete and undo; verify is shown in the driven run.
- [ ] Group B: hotspot crosshatch and background indicator colors as settings (`Nodus.Links.HotspotColor`, `Nodus.Links.BackgroundColor`). Done when: a settings readback asserts both defaults.
- [ ] Group B output: SVG `<a>` and `<title>` (through §1), HTML image maps (`<map>` with rect or poly areas) with §16's images, and PDF link annotations and named destinations through the `D02 T13 §14` writer. Done when: `HyperlinkExportTests` read back each output (XML parse for SVG and HTML, PdfPig for PDF) with the same URLs and regions.
- [ ] Group C: add the `Rollover` group with Normal, Over, and Down states; create, edit, finish editing, delete, duplicate, or extract a state, and the target frame. Done when: `RolloverTests` cover each operation and its undo.
- [ ] Group C: live preview toggles hover and press on the canvas. Done when: a driven capture of the Over state is committed.
- [ ] Group C output: HTML with CSS `:hover` and `:active`, and SVG with CSS. Done when: `RolloverExportTests` parse the output and assert one rule per state.
- [ ] Add `LinksRolloversPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/` listing links, bookmarks, and rollovers with search. Done when: a view-model test filters by URL; capture committed.
- [ ] Group D: add `SvgInteractivityPanel` attaching event attributes from the SVG 1.1 event list and linking external JavaScript files; Nodus writes them to SVG and never executes them. Done when: a test asserts the attributes and `<script xlink:href>` in the written SVG and that no script engine is referenced by the solution.
- [ ] Release slices, links, and rollovers back to plain objects, each undoable. Done when: tests assert the objects remain and the web data is gone.
- [ ] Log `Slice {Command} ({Count})`, `Link set {Url} on {ObjectId}`, and `Rollover {Operation}`. Done when: each line is asserted.
- [ ] Commit: `"nodus: slices, image maps, hyperlinks, rollovers, and SVG interactivity"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~SliceCommandTests|FullyQualifiedName~SliceExportTests|FullyQualifiedName~HyperlinkExportTests|FullyQualifiedName~RolloverExportTests|FullyQualifiedName~RolloverTests"` exits 0: sliced and linked fixtures export to SVG, HTML, and PDF whose links read back (PdfPig for PDF, XML parse for SVG and HTML) with the same URLs and regions; a driven rollover live-preview capture is committed. Cheaper substitute that fails: storing URLs without writing them, which the read-back catches.

## 18. Pixel-Perfect Drawing, Pixel Preview, and Object Hinting

Icon designers need crisp small artwork that exports without blurry edges. Today's `PixelPreview` flag only activates at zoom 8 and the renderer ignores it; this section replaces it with a real preview at document resolution that equals the 1x export, adds per-object pixel alignment and the align command, object hinting, and the pixel-perfect workflow. Catalog: NP-2473 to NP-2477 (5 features).

**Fidelity:** docs/captures/nodus/main-window/, extended.
**Job:** an icon designer can draw crisp 16 px icons that export without blurry edges. Consumer: the canvas render and the exported bitmaps.
**Treatment:** View, Pixel Preview (Alt+Ctrl+Y) rendering at 1 px per document unit, scaled nearest-neighbour at every zoom, a pixel grid at 600 percent and above, Align to Pixel Grid in the Transform and Align panels, and Object Hinting in the Object menu. Cheaper substitute that fails the checkpoint: the existing flag that only activates at zoom 8.
**Chrome:** consume `SkiaRenderer`, the `D02 T07 §12` view-mode switcher, the Align panel, and the settings store. Do not add a second renderer.

**Requires:** display-session -- pixel preview and snapping need an interactive desktop

- [ ] Add `PixelPreviewRenderer` in `src/Nodus/Photon.Nodus.Desktop/Services/`: render the visible area at document resolution to an offscreen `SKSurface` (anti-aliased as export would), then draw it with nearest-neighbour sampling. Done when: `PixelPreviewTests` assert the preview bitmap equals the §15 PNG export pixels exactly for the icon fixture.
- [ ] Remove the unused `pixelPreview` flag from `SkiaRenderer` and the zoom-8 gate from `SkiaCanvas`. Done when: `grep -n "Zoom >= 8" src/Nodus` prints nothing.
- [ ] Pixel preview is a view mode in the `D02 T07 §12` switcher with Alt+Ctrl+Y, shared with the export preview of §15 and §16 so preview equals output. Done when: a test asserts the mode switch and shortcut.
- [ ] The pixel grid draws at 600 percent and above. Done when: a capture at 800 percent shows it.
- [ ] Add `PixelAlign` per object (`nodus:pixel-align`) snapping horizontal and vertical segment edges and nodes to whole or half pixels by stroke width on create and transform; rotation disables it. Done when: `PixelAlignTests` assert integer edges for 1 px strokes, half-integers for odd widths, and no snapping when rotated.
- [ ] `Nodus.PixelGrid.AlignNewObjects` sets the default for new art. Done when: a test with the setting on asserts new rectangles carry the flag.
- [ ] Align to Pixel Grid realigns selected objects once (undoable), with Select Objects Not Aligned to Pixel Grid beside it. Done when: tests assert both and the undo.
- [ ] Object hinting marks an object so export snaps its edges to the pixel grid at render time without changing geometry. Done when: a test asserts the geometry is unchanged and the exported edge pixels are fully opaque.
- [ ] Pixel-perfect workflow: pixel units, whole-number sizes in the Transform panel, pixel snapping, and a pixel-aligned page origin, enabled by the web and icon document presets. Done when: a test creates a document from the icon preset and asserts all four.
- [ ] `Nodus.PixelPreview.AntiAliasBitmaps` controls bitmap smoothing in pixel preview. Done when: a test asserts both renderings of a placed bitmap.
- [ ] Log `Pixel preview {On|Off}` and `Aligned {Count} objects to the pixel grid`. Done when: both lines are asserted.
- [ ] Commit: `"nodus: real pixel preview, pixel-grid alignment, and object hinting"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~PixelAlignTests|FullyQualifiedName~PixelPreviewTests"` exits 0: the pixel preview of the icon fixture is pixel-identical to its 1x PNG export, and aligned edges hold integer coordinates after move and scale; a capture at 800 percent is committed to `docs/captures/nodus/main-window/`. Cheaper substitute that fails: a zoomed normal render, which the pixel-identity assertion catches.

## 19. Clipboard Formats, OLE Objects, Placing Multiple Files, and Scanner Acquire

Artwork must move between Nodus, Imago, office apps, and other editors by copy, paste, drag, place, and scan without losing vectors. This section extends the `D02 T03 §3` `ClipboardService` to every flavor the file supports, builds the Import command with search, filters, multiple files, and a place gun, records the OLE decision (no container or server; linked placed files instead), and adds WIA acquire. The WIA test needs a WIA device or the WIA test device and is skipped by name otherwise. Catalog: NP-2351 to NP-2366 (16 features).

**Fidelity:** new build, no baseline; captured to docs/captures/nodus/import-place/.
**Job:** a designer can move artwork between Nodus, Imago, office apps, and other editors by copy, paste, drag, place, and scan without losing vectors. Consumer: the document and other applications through the clipboard.
**Treatment:** File, Import (Ctrl+I) with a search box, format filter, multi-select, and a place gun (click places at size, drag sizes, Enter centers, Space keeps the original position, grid placement), plus Clipboard Handling settings and File, Acquire Image. Cheaper substitute that fails the checkpoint: single-file place with bitmap-only paste.
**Chrome:** consume the `D02 T06 §14` place path, the `D02 T12 §7` linked files and Edit Original, the snapping engine, the settings store, and `Photon.UI` dialogs. Do not add a second clipboard service.

**Requires:** display-session -- the clipboard, drag and drop, place gun, and WIA dialog need an interactive desktop

- [ ] Extend `ClipboardService` in `src/Nodus/Photon.Nodus.Desktop/Services/`: copy writes the Nodus internal flavor, `image/svg+xml`, PDF (`D02 T13 §14`), AICB (§5), EMF (§11), PNG, and DIB. Done when: `ClipboardFlavorTests` assert every flavor on a fake clipboard.
- [ ] Paste picks the richest known flavor in order Nodus, SVG, PDF, AICB (§4), EMF, bitmap, text. Done when: tests offer each subset and assert the flavor chosen.
- [ ] Every flavor round-trips to the same model within tolerance. Done when: `ClipboardFlavorTests.RoundTrip` copies the fixture and pastes it back through each flavor.
- [ ] Clipboard settings `Nodus.Clipboard.CopyAsPdf`, `Nodus.Clipboard.CopyAsAicb` (preserve paths, or appearance and overprints), `Nodus.Clipboard.IncludeSvgCode`, and `Nodus.Clipboard.PasteTextWithoutFormatting`, each read by `ClipboardService`. Done when: a test per setting asserts its effect.
- [ ] Add `ImportCommand` (Ctrl+I) with a format filter list and All Formats. Done when: `ImportCommandTests` assert the filter string lists every enabled reader.
- [ ] Import search box over file name and metadata (title, subject, author, keywords, comments). Done when: a test finds a fixture by a keyword in its metadata.
- [ ] Multi-select queues files one by one or in a grid, and Skip the Options Dialog (`Nodus.Import.SkipOptionsDialog`). Done when: tests assert the queue order and the skip.
- [ ] Add the `PlaceGun` tool state: arrow keys cycle queued files, click places at original size, drag sizes, Enter centers on the page, grid placement by drag with arrow keys. Done when: `PlaceGunTests` assert each gesture's result.
- [ ] Space places at the original position for CDR, AI, and PDF imports. Done when: a test asserts the placed origin equals the source's.
- [ ] Active snapping applies while placing. Done when: a test with grid snapping asserts the snapped origin.
- [ ] Format registry settings enable, disable, and order import and export formats (`Nodus.Formats.Enabled`, `Nodus.Formats.Order`); all readers are built in, and the only optional components (Ghostscript, WIC extensions) are named where a format needs them. Done when: a test disables a format and asserts it leaves the filter list.
- [ ] Drag and drop from other applications accepts the same flavors as paste and files, and each drop records one history step. Done when: a test simulates a drop of each flavor and asserts one undoable history step.
- [ ] Record the OLE decision in `docs/dev/decisions.md`: no OLE container or server; Paste Link and Insert Object from File create a linked placed file through `D02 T12 §7` (embedded or linked by choice). Done when: the row exists and a test asserts Paste Link creates a linked placed file.
- [ ] Editing a linked or embedded object opens its source application with Edit Original and updates on file change. Done when: a test changes the linked file and asserts the placed object refreshes.
- [ ] Add `WiaAcquireService`: WIA 2.0 through the built-in `WIA.CommonDialog` COM automation for Select Source and Acquire from scanners and cameras; TWAIN recorded as not supported. Done when: `WiaAcquireTests` acquire from the WIA test device on a machine that has one and report the skip reason by name otherwise.
- [ ] Log `Imported {Count} files ({Formats})`, `Pasted {Flavor}`, and `Acquired image {Width}x{Height} from {Device}`. Done when: each line is asserted.
- [ ] Commit: `"nodus: every clipboard flavor, multi-file import with a place gun, linked objects, and WIA acquire"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ClipboardFlavorTests|FullyQualifiedName~ImportCommandTests|FullyQualifiedName~PlaceGunTests|FullyQualifiedName~WiaAcquireTests"` exits 0: copying a fixture and pasting it back through each flavor yields the same model within tolerance, and the WIA case passes or reports its skip reason; a driven multi-file import captures the place gun and the placed result under `docs/captures/nodus/import-place/`. Cheaper substitute that fails: a bitmap-only clipboard, which the vector flavor assertions catch.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` exits 0 with one result per fixture for every reader and writer in this file, and every skip names its missing tool (Inkscape, Ghostscript, WIC extension, WIA device)
- [ ] Every fixture folder under `tests/fixtures/nodus/` created here has a README naming its source, license, and the reference implementation and version of its goldens
- [ ] `docs/dev/decisions.md` carries a row for every package this file added (PdfPig, ACadSharp, DocumentFormat.OpenXml, NPOI) and every recorded decision (CDR reader, Ghostscript, JPEG 2000, progressive JPEG, OLE)
- [ ] Every format option persists and reads back after a restart (settings readback quoted)
- [ ] `docs/user/nodus/formats.md` lists every format this file reads or writes
- [ ] `python scripts/todo-graph.py validate` clean
