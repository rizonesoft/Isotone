---
schema_version: 1
id: stilus-parity-print
domain: 02-stilus
status: draft
title: "TODO-13 -- Stilus Parity: Color Management, Print, Prepress, and PDF"
depends_on: []
track: N13
---

# TODO-13 -- Stilus Parity: Color Management, Print, Prepress, and PDF

> **Goal:** A Stilus user can take a drawing to a print shop or a desktop printer without leaving Stilus: the document carries its ICC profiles and policies, the screen soft-proofs the press, File, Print drives any Windows printer with tiling, marks, bleed, separations, overprint, trapping, flattening, imposition, and variable data, and Publish to PDF writes exact vector PDF with spot colors, layers, PDF/X and PDF/A presets, and security through Stilus's own content-stream writer on PDFsharp (MIT). This promotes backlog B-011 (source `legacy-stilus-9`) and consumes the `Isotone.Core` color engine of `D01 T04 §1` to `D01 T04 §3`.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** The document color mode is a bare enum in `src/Stilus/Bezier.Core/Services/FileOperationsService.cs` with RGB, CMYK, and Grayscale and no profile behind it, and the same file defines five print-category document presets (A4, A3, Letter, Legal, and Business Card) although nothing prints. No Stilus source touches WPF or .NET printing (`PrintDialog`, `System.Printing`, `XpsDocumentWriter`, `PrintVisual`). `src/Stilus/Bezier.Core/Services/ExportDialogService.cs` advertises a "Print" preset described as a high-quality PDF with no writer behind it, and File, Export, PDF in `src/Stilus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs` only sets status text; `D02 T04 §4` replaces it with an `SKDocument` exporter that §14 of this file supersedes. No PDF library is referenced by `Directory.Packages.props`, and `src/Stilus/Bezier.Core/Services/ImportService.cs` names the missing PDF library as its blocker. `src/Isotone.Core`, which will host the color engine this file consumes, does not exist yet; neither does `docs/dev/decisions.md` for the printing-path and PDFsharp rows, nor any capture home under `docs/captures`.
<!-- claim: count "^    CMYK,$" src/Stilus/Bezier.Core/Services/FileOperationsService.cs = 1 -->
<!-- claim: count "Category = PresetCategory.Print" src/Stilus/Bezier.Core/Services/FileOperationsService.cs = 5 -->
<!-- claim: count "PrintDialog|System\.Printing|XpsDocumentWriter|PrintVisual" src/Stilus/**/*.cs = 0 -->
<!-- claim: count "High-quality PDF for printing" src/Stilus/Bezier.Core/Services/ExportDialogService.cs = 1 -->
<!-- claim: count "StatusText = \"Export as PDF\.\.\.\";" src/Stilus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 1 -->
<!-- claim: count "PDFsharp|PdfPig|PdfSharp" Directory.Packages.props = 0 -->
<!-- claim: count "PDF vector extraction requires a dedicated library like PdfSharp or iText" src/Stilus/Bezier.Core/Services/ImportService.cs = 1 -->
<!-- claim: absent src/Isotone.Core -->
<!-- claim: absent docs/dev/decisions.md -->
<!-- claim: absent docs/captures -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- atomic writes, refusals that name the file and the reason, progress and cancel over one second, one log line per change
- [`standards/stilus.md`](../../standards/stilus.md) -- one renderer, every mutation a command, SVG native
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- the blueprint for this file; [`docs/parity/stilus-parity.md`](../../docs/parity/stilus-parity.md) -- the catalog rows each section owns
- [`todo/backlog.md`](../backlog.md) -- B-011 (Print and prepress, source `legacy-stilus-9`) is promoted by §2; B-023 (Pinxit color management, promoted on 2026-09-26 into `D03 T18 §4`) shares the `D01 T04` engine
- References: ISO 32000-1 (PDF 1.7), ISO 15930-1, -3, and -7 (PDF/X), ISO 19005-1 and -2 (PDF/A), ISO 14289-1 (PDF/UA), Adobe PostScript Language Reference third edition, DSC 3.0, PPD 4.3, OPI 2.0, Microsoft Learn `System.Printing` and `XpsDocumentWriter`
- -> XREF: D01 T04 §1 -- the engine, ICC transforms, default profiles, and monitor profile lookup §1 builds on
- -> XREF: D01 T04 §2 -- rendering intents, black point compensation, the proofing transform, and the gamut check §1 and §6 consume
- -> XREF: D01 T04 §3 -- bitmap CMYK and duotone modes that §1's Convert to Profile walks
- -> XREF: D01 T02 §2 -- the settings store every print, proof, and PDF setting lives in
- -> XREF: D01 T02 §4 -- the suite history every command here records in
- -> XREF: D01 T03 §3 -- dithering for print as bitmap in §8
- -> XREF: D02 T04 §4 -- the `SKDocument` PDF export §14 replaces, with its `PdfExporterTests` kept as a regression
- -> XREF: D02 T07 §1 -- the live-object contract for the Crop Marks and Trap effects and merge fields
- -> XREF: D02 T07 §3 -- the page and artboard model §2 prints
- -> XREF: D02 T07 §4 -- page sizes and facing pages §12 lays out, and the document bleed §4 reads
- -> XREF: D02 T09 §1 -- spot and registration colors §4, §5, and §14 output
- -> XREF: D02 T09 §7 -- gradients §14 writes as shadings
- -> XREF: D02 T09 §19 -- blend modes §14 writes in transparency groups
- -> XREF: D02 T09 §20 -- opacity masks §14 writes as soft masks
- -> XREF: D02 T10 §1 -- shaped text runs §14 embeds fonts for
- -> XREF: D02 T10 §2 -- the rich text model merge fields and text hyperlinks live in
- -> XREF: D02 T10 §13 -- the RTF reader and the DocumentFormat.OpenXml reference §13's data sources reuse
- -> XREF: D02 T11 §1 -- the live-effect framework for Crop Marks and Trap
- -> XREF: D02 T11 §10 -- the 3D and Materials meshes, materials, and renders §17 writes as interactive 3D annotations
- -> XREF: D02 T12 §1 -- the always-overprint-black flag Convert to Bitmap writes, honored by §7
- -> XREF: D02 T12 §2 -- the Document Raster Effects Settings resolution §8 prints at
- -> XREF: D02 T14 §2 -- PDF import, which moves the PdfPig reference §2 adds for tests into `Isotone.Stilus.Core`
- -> XREF: D02 T14 §9 -- EPS placement, which enables §15's EPS handling
- -> XREF: D02 T14 §17 -- more hyperlink schemes, bookmarks, and image maps built on the `Hyperlink` model §16 adds
- -> XREF: D02 T15 §4 -- generative print bleed, which reads §4's bleed box
- -> XREF: D02 T16 §11 -- styled QR code objects, built on the QR encoder §13 adds
- -> XREF: D03 T17 §7 -- Pinxit parity formats cites §4: printer marks D03 T17 §7 moves; §10: the PostScript writer D03 T17 §7 moves for EPS; §14: the PDF writer D03 T17 §7 moves; §15: PDF presets and standards D03 T17 §7 moves; §16: PDF security D03 T17 §7 moves
- -> XREF: D03 T18 §4 -- Pinxit parity export, color management, and print cites §1: Stilus's color settings, whose dialog shell D03 T18 §4 moves to `Isotone.UI` and whose defaults D03 T18 §4 moves to the suite settings file; §2: the print dialog frame D03 T18 §6 moves; §3: print tiling D03 T18 §6 consumes; §4: printer marks, moved by D03 T17 §7 or by D03 T18 §6; §5: separations, halftones, and inks D03 T18 §7 moves; §9: the preflight engine D03 T18 §7 moves; §10: the PostScript writer for D03 T18 §6's PostScript printer options

## Outcome

- The document carries RGB, CMYK, and gray ICC profiles with open, import, and paste policies; Assign and Convert to Profile are undoable commands; profiles embed on save and export and reopen without a system profile.
- File, Print prints any page or artboard range to any installed printer as vector output, with tiling, print styles, print to file, marks and bleed, separations with halftone screens, overprint, trapping, flattening, imposition, layout styles, and print merge.
- The canvas soft-proofs a chosen device, shows a gamut warning, overprint preview, and per-plate separations preview.
- Preflight names output problems in Print, PDF, and export dialogs, and Package collects the document, links, permitted fonts, and a report into one folder.
- Stilus writes its own PostScript and its own PDF: exact vector paths, shadings, patterns, transparency groups, Separation and DeviceN spots, ICC output, OCG layers, embedded font subsets, page boxes, PDF/X and PDF/A presets that pass veraPDF and rule checks, tagged accessible PDF, bookmarks, links, security, and linearization.

**Adjacency:** list=applicable @ D02 T13 §3; document=applicable @ D02 T13 §2; settings=applicable @ D02 T13 §1; reporting=applicable @ D02 T13 §9; notifications=applicable @ D02 T13 §2; permissions=applicable @ D02 T13 §16; audit=applicable @ D02 T13 §7; exchange=applicable @ D02 T13 §14; reverse=applicable @ D02 T13 §1

**Adjacency rationale:** Print styles, PDF presets, proof presets, and the ink list are the lists. The printed sheet and the PDF are the carried documents. Color settings, print styles, and PDF presets are settings with the print and PDF pipelines as their consumers. The print summary and the preflight report are the reports. A spooling job shows progress and a completion notification on the status strip. An offline printer, a read-only target, and a password-protected PDF are the refusal cases, and PDF permissions are enforced by encryption, not by a flag. Overprint, trap, assign, and convert are undoable commands with a log line in the history. PDF, PostScript, ICC, CSV, and XML are the exchange formats. Assign and Convert to Profile undo, and every preset delete is reversible until the dialog closes.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Document color settings: profiles, policies, assign, convert, and embed | D01 T04 §2 |  [ ]   |
|   2   |   §2    | The print dialog: printers, range, copies, placement, scaling, and preview | D02 T07 §3 |  [ ]   |
|   3   |   §3    | Print tiling, print styles, print to file, and print summaries | §2 |  [ ]   |
|   4   |   §4    | Printer's marks and bleed | §2 |  [ ]   |
|   5   |   §5    | Separations, halftone screens, and the ink manager | §2, §1 |  [ ]   |
|   6   |   §6    | Soft proofing, gamut warning, overprint preview, and separations preview | §1, §5 |  [ ]   |
|   7   |   §7    | Overprint attributes and trapping | §5 |  [ ]   |
|   8   |   §8    | Transparency flattening and the flattener preview | §2 |  [ ]   |
|   9   |   §9    | Preflight, Package, and Collect for Output | §2 |  [ ]   |
|  10   |   §10   | PostScript output and driver compatibility options | §2 |  [ ]   |
|  11   |   §11   | Imposition, binding, and page placement | §4 |  [ ]   |
|  12   |   §12   | Layout styles, labels, and banners | D02 T07 §4 |  [ ]   |
|  13   |   §13   | Print merge and variable data | §2, D02 T10 §2 |  [ ]   |
|  14   |   §14   | The PDF writer: spot colors, layers, and exact vector output | §1, D02 T04 §4 |  [ ]   |
|  15   |   §15   | PDF presets and standards: PDF/X, PDF/A, compatibility, compression, and marks | §14, §4 |  [ ]   |
|  16   |   §16   | PDF interactivity and security: bookmarks, hyperlinks, tagged PDF, and passwords | §14 |  [ ]   |
|  17   |   §17   | Interactive 3D models in PDF: U3D annotations | §14, §15, D02 T11 §10 |  [ ]   |

---

## 1. Document Color Settings: Profiles, Policies, Assign, Convert, and Embed

Every print, proof, and PDF path needs to know what the document's colors mean. Today the color mode is a label with no profile behind it, so a CMYK value has no defined appearance and nothing can be proofed. This section gives the document RGB, CMYK, and gray profiles with open, import, and paste policies, adds Assign and Convert to Profile as undoable commands, embeds the profile bytes on save and export so reopen needs no system profile, and renders the canvas through the display profile. It keeps CMYK numbers safe: they are never round-tripped through RGB unless a policy says to convert. Catalog: NP-2086 to NP-2102 (17 features: the Color Settings dialog, assign profile, appearance of black, extract and keep an embedded profile, default working profiles, the primary color mode, the spot definition policy, document color settings on the status bar, embed on save and export, convert to profile, color management presets, open and import and paste policies, missing and mismatched profile warnings, the safe CMYK workflow, and the web sRGB recommendation). **Pinxit second consumer (2026-09-26):** the color settings dialog shell moves to `Isotone.UI` and its defaults to the suite settings file in `D03 T18 §4`, Stilus consuming both unchanged.

**Fidelity:** Document Color Settings: Profiles, Policies, Assign, Convert, and Embed -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/color-settings/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/color-settings/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can set the document's RGB, CMYK, and gray profiles and policies and convert or assign without surprise. Consumer: every render, print, and PDF path.
**Treatment:** Edit, Color Settings (Shift+Ctrl+K) with Default and Document tabs, and the Assign, Convert, mismatch, and missing profile dialogs. Cheaper substitute that fails the checkpoint: a CMYK dropdown that relabels the enum without an ICC transform.
**Chrome:** consume the `D01 T04` engine, the `Isotone.UI` dialog chrome, the settings store, and the suite history. Do not add a second profile loader or a Stilus-local transform cache.

**Requires:** display-session -- the dialogs and the status-bar flyout are driven and captured on an interactive desktop

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Color/DocumentColorSettings.cs`: RGB, CMYK, and gray profile references (by hash, with bytes), the primary color mode replacing the `ColorMode` enum, rendering intent, black point compensation, and the spot definition policy (Lab, CMYK, or RGB values) (CD-1564, CD-1569). Done when: `DocumentColorSettingsTests` construct defaults from the `D01 T04 §1` bundled profiles and every existing `ColorMode` use compiles against the new type.
- [ ] Persist the settings in SVG as a `<color-profile>` element per embedded profile plus `stilus:color-settings` (profile hashes, intent, policies); an embedded profile keeps its bytes so reopen needs no system profile (CD-233). Done when: `DocumentColorSettingsTests.RoundTrip` saves, deletes the profile from the test profile folder, reopens, and resolves every profile.
- [ ] Add the settings keys `Stilus.Color.Defaults.Rgb`, `.Cmyk`, and `.Gray` (CD-1563), `Stilus.Color.Policy.Open.{Rgb,Cmyk,Gray}` (UseEmbedded, AssignDefault, ConvertToDefault) (CD-1589), `Stilus.Color.Policy.ImportPaste.{Rgb,Cmyk,Gray}` (CD-1590), `Stilus.Color.WarnMismatch`, `Stilus.Color.WarnMissing`, `Stilus.Color.BlackOnScreen`, and `Stilus.Color.BlackOnOutput`, each with a default and a consumer. Done when: a test reads every key's default through `ISettingsStore` and a change writes one log line.
- [ ] Add `src/Stilus/Isotone.Stilus.Desktop/Views/Color/ColorSettingsDialog.xaml` (Edit, Color Settings, Shift+Ctrl+K) with Default and Document tabs over the settings and the document (AI-1095, CD-1562, CD-1603, CD-1604). Done when: a driven run changes the document CMYK profile and the capture shows both tabs. Cheaper substitute: one tab that edits only defaults.
- [ ] Add color management presets as JSON under `%LOCALAPPDATA%\Rizonesoft\Stilus\presets\color\`: General Purpose, Prepress, Web, Minimal Color Management, and Simulate Color Management Off, built on the freely redistributable profiles `D01 T04 §1` bundles, with Save and Delete preset (CD-1587, CD-1588). Done when: `ColorPresetStoreTests` apply each built-in and round-trip a user preset.
- [ ] Add `AssignProfileCommand` (keeps color numbers) (AI-1096, CD-1573). Done when: `AssignConvertCommandTests.Assign` asserts every stored number is unchanged and undo restores the previous profile.
- [ ] Add `ConvertToProfileCommand` (keeps appearance with a chosen intent), walking every fill, stroke, gradient stop, mesh node, and bitmap (bitmaps through `D01 T04 §3`) as one undo step (CD-1574). Done when: `AssignConvertCommandTests.Convert` converts the swatch fixture and its Lab values stay within dE00 0.5 of the `transicc` goldens.
- [ ] Log one Serilog Information line per assign or convert (profile from and to, intent, element count). Done when: a Serilog test logger asserts the line.
- [ ] Add `ProfileMismatchDialog` and `MissingProfileDialog` for open, import, and paste, driven by the policies and the warn settings (CD-1591 to CD-1594). Done when: a driven open of `tests/fixtures/stilus/icc/mismatched.svg` shows the mismatch dialog and each choice applies as named.
- [ ] Apply the import and paste policy when pasting between documents with different profiles. Done when: a test pastes a CMYK swatch between documents under each policy and asserts the numbers.
- [ ] Embed profiles on save and export: SVG `<color-profile>`, PNG and TIFF `iCCP` through WIC, and PDF OutputIntent and ICCBased through §14 (CD-1572). Done when: a PNG exported with an embedded profile reads back the same profile hash.
- [ ] Add Extract embedded profile on open or import, writing it into the profile folder `D01 T04 §1` names (CD-229, CD-2476). Done when: extracting from the embedded fixture writes a file with the expected hash.
- [ ] Guard the safe CMYK workflow: CMYK numbers are never round-tripped through RGB on open, import, paste, or print unless the policy converts (CD-1596). Done when: `SafeCmykTests` open, paste, and save a C40 M0 Y0 K0 swatch under the default policy and assert the numbers are exact.
- [ ] Add the Web preset's sRGB recommendation text in the dialog when the primary mode is RGB and the output target is web (CD-1597). Done when: the text appears in a driven run with the Web preset.
- [ ] Add Appearance of Black: rich or accurate black on screen and on output, consumed by the canvas renderer, §5, and §14 (AI-1097, AI-1183). Done when: a test renders K100 as `#000000` in rich mode and as the profile's K100 appearance in accurate mode.
- [ ] Add a status-bar flyout showing the document profiles that opens the dialog's Document tab (CD-1570). Done when: a driven run clicks the flyout and the capture shows the tab.
- [ ] Render the canvas through the display profile from the `D01 T04 §1` monitor profile lookup, re-rendering when the monitor profile changes. Done when: a test with a fake monitor profile asserts the final transform uses it.
- [ ] Commit fixtures under `tests/fixtures/stilus/icc/`: an SVG with an embedded FOGRA39-class CMYK profile, an untagged SVG, and a mismatched SVG, with `transicc` goldens and the lcms2 version in `reference.txt`. Done when: all three exist with goldens.
- [ ] Update the Stilus user guide page `docs/user/stilus/color-management.md`. Done when: the page documents every dialog control and policy.
- [ ] Commit: `"stilus: document color settings, policies, and assign and convert to profile"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `DocumentColorSettingsTests`, `AssignConvertCommandTests`, and `SafeCmykTests` reporting; `tests/fixtures/stilus/icc/embedded.svg` opened, converted to the CMYK default, saved, and reopened compares Lab values per swatch against the lcms2 `transicc` goldens within dE00 0.5 (worst value quoted); captures under `docs/captures/stilus/color-settings/` committed. Cheaper substitute that fails: storing the profile name without its bytes, which the reopen-without-system-profile test rejects.

## 2. The Print Dialog: Printers, Range, Copies, Placement, Scaling, and Preview

Printing is the oldest way a drawing leaves the editor, and Stilus cannot do it at all. This section builds Stilus's own print dialog on a recorded printing path, printing vector pages (never a screen raster) to any installed printer with range, copies, media, orientation, layers, placement, scaling, and previews. It promotes backlog B-011 (Print and prepress). Later sections add pages to this dialog. Catalog: NP-2117 to NP-2127 (11 features: the print dialog and command, copies, collate, reverse order and range, media size and orientation, print layers, placement origin, scaling, print to PDF, printer selection and driver preferences, Print Preview, the mini preview, and print to fit the paper size). -> SOURCE: legacy-stilus-9

**Fidelity:** The Print Dialog: Printers, Range, Copies, Placement, Scaling, and Preview -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/print-dialog/, docs/captures/golden/stilus/print-preview/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/RadioButton/README.md, new surface: docs/design/components/StilusPrintPreview/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/print-dialog/` and `docs/captures/stilus/print-preview/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can print chosen pages or artboards to any installed printer at the right size and position. Consumer: the Windows spooler and Microsoft Print to PDF.
**Treatment:** a category-paged dialog (General and Layout here, the pages later sections add) with a live mini preview. Cheaper substitute that fails the checkpoint: `System.Windows.Controls.PrintDialog.PrintVisual` of the canvas control, which prints the viewport raster at screen resolution.
**Chrome:** consume the `Isotone.UI` dialog chrome, numeric fields with units, the settings store, the status-strip progress, and the toast service. Do not build a second preview renderer: reuse the canvas scene renderer.

**Requires:** display-session -- printing to Microsoft Print to PDF and capturing the dialog need an interactive desktop

- [ ] Write the design spec `docs/design/components/StilusPrintPreview/README.md` and its `docs/design/components/StilusPrintPreview/preview.html` card (anatomy, every state, tokens, sizes) before any XAML is written, and regenerate the design page. Done when: the spec exists and `python scripts/build-design-site.py --check` passes.
- [ ] Measure both printing paths on this host and record the decision in `docs/dev/decisions.md`: WPF `PrintQueue`, `PrintTicket`, and `XpsDocumentWriter` with a `FixedDocument` of vector `DrawingVisual` pages, versus GDI (`StartDoc` with `DOCINFO.lpszOutput`), covering vector fidelity, CMYK and spot limits, and how the proof run names the output file without a prompt. Done when: the row quotes the measurement and names the chosen path. Source: Microsoft Learn `System.Printing.PrintQueue` and `System.Windows.Xps.XpsDocumentWriter`.
- [ ] Add PdfPig (Apache-2.0) to `Directory.Packages.props` as a test-only reference of `tests/Isotone.Stilus.Tests/`, with a `docs/dev/decisions.md` row naming the license and that `D02 T14 §2` later reuses it for import. Done when: the test project restores it and no `src/` project references it.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/PrintJobSettings.cs` (printer, copies, collate, reverse, range, media, orientation, layers mode, placement, scale). Done when: it serializes with a source-generated JSON context and round-trips.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/PrintPlanner.cs`: sheets, the page-to-sheet transform, and skip blank. Done when: `PrintPlannerTests` cover ranges, skip blank, scaling, placement, and orientation.
- [ ] Add `IPrintBackend` in `Isotone.Stilus.Core/Print/` with the chosen implementation in `src/Stilus/Isotone.Stilus.Desktop/Print/`, and `StilusDrawingVisualBuilder` translating the scene to WPF geometry (paths, gradients, bitmaps, text as glyph runs). Done when: `StilusDrawingVisualBuilderTests` assert a path fixture becomes one `PathGeometry` with the same point count.
- [ ] List printers from `LocalPrintServer.GetPrintQueues()` and read capabilities from `PrintQueue.GetPrintCapabilities()` (media sizes, printable area) (CD-2660). Done when: a test with the Microsoft Print to PDF queue reads its media list.
- [ ] Add a Preferences button that opens the driver sheet through `DocumentPropertiesW`, round-tripping DEVMODE with `PrintTicketConverter` (CD-2660). Done when: a driven run changes a driver setting and the returned ticket reflects it.
- [ ] Add `src/Stilus/Isotone.Stilus.Desktop/Views/Print/PrintDialog.xaml` (File, Print, Ctrl+P) with the General page: printer, copies, collate, reverse order (AI-1066, AI-1067, CD-2659, CD-2662, CD-2663, CD-2789). Done when: the capture of the General page is committed and printing two collated copies yields the expected page order.
- [ ] Add the range controls: all, current, a pages or artboards range string (`1-3,5`), even, odd, selection, ignore artboards, and skip blank (AI-1067). Done when: `PrintPlannerTests.Ranges` cover each form, including a malformed string refused by name.
- [ ] Add print layers: visible and printable, visible, or all, reading the layer printable flag from `D02 T02 §6` and adding it if absent (AI-1069). Done when: a non-printable layer is omitted in visible-and-printable mode.
- [ ] Add media and orientation from the queue with auto-rotate, transverse, and match orientation; changing size or orientation here updates the page through an undoable `SetPageSizeCommand` only when the user opts in (AI-1068, AI-1085, CD-2661). Done when: a test asserts the page is unchanged without the opt-in and changed with it, and undo restores it.
- [ ] Add the Layout page: a 9-point placement origin with drag in the mini preview and numeric X and Y (AI-1070), and scaling as in document, fit to page, custom percent, and reposition with size (AI-1071, CD-2664). Done when: `PrintPlannerTests.Placement` and `.Scaling` pass and the capture shows the page.
- [ ] Add print to fit the paper size, which requests a custom media size from the driver (CD-2675). Done when: a test asserts the ticket's media size equals the page size.
- [ ] Add the mini preview on the dialog rendering the `PrintPlanner` output through the canvas scene renderer (CD-2667). Done when: dragging the placement moves the art in the preview in a driven run.
- [ ] Add `src/Stilus/Isotone.Stilus.Desktop/Views/Print/PrintPreviewWindow.xaml` (File, Print Preview) with zoom and page navigation over the same planner output (CD-2666). Done when: the capture shows page 2 of the two-artboard fixture.
- [ ] Add a Print to PDF entry routed through an `IPdfJobWriter` seam backed by the `D02 T04 §4` `PdfExporter` until §14 replaces it (CD-2658, CD-2721). Done when: printing to PDF through the seam writes a file PdfPig reads.
- [ ] Run the print job off the UI thread with status-strip progress and Cancel, and notify the user on completion with a toast; refuse an offline or error-state printer with a message naming it. Done when: a driven run shows the progress and the completion notification, and a test backend in error state yields the refusal message.
- [ ] Log one Information line per job (`Printed {Pages} page(s) x {Copies} to {Printer}`). Done when: a Serilog test logger asserts the line.
- [ ] Update the Stilus user guide page `docs/user/stilus/printing.md`. Done when: the page documents every General and Layout control and Print Preview.
- [ ] Commit: `"stilus: the print dialog, print preview, and vector printing"`

**Test checkpoint:** Driven run plus unit test: `dotnet test Isotone.slnx` exits 0 with `PrintPlannerTests` and `StilusDrawingVisualBuilderTests` reporting; a driven print of `tests/fixtures/stilus/print/two-artboards.svg` to Microsoft Print to PDF is read with PdfPig, which asserts two pages, the media box of each artboard, and vector path operators present with no full-page image XObject (output quoted). Cheaper substitute that fails: `PrintVisual` of the canvas, which yields one image XObject per page.

## 3. Print Tiling, Print Styles, Print to File, and Print Summaries

A poster larger than the printer's paper prints across sheets, and a designer who prints the same way every week saves those settings once. This section adds tiling with overlap and tiling marks, the Print Tiling tool and its canvas overlay, saved print styles, print to file with split options, and the Summary page. PostScript print to file is added by §10, which enables the option here. Catalog: NP-2128 to NP-2132 (5 features: the print tiling tool and show or hide tiling, tiled pages with overlap and marks, the print summary and save summary, print presets and styles, and print to file with split options).

**Fidelity:** Print Tiling, Print Styles, Print to File, and Print Summaries -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/print-dialog/, docs/captures/golden/stilus/main-window/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the §2 print dialog; captured to `docs/captures/stilus/print-dialog/` (tiling controls, Summary page) and `docs/captures/stilus/main-window/` (tiling overlay). The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can print a poster across sheets and reuse named print settings. Consumer: `PrintPlanner` and the saved style files.
**Treatment:** tiling controls on the General page plus a canvas tiling overlay moved by the Print Tiling tool. Cheaper substitute that fails the checkpoint: scaling the poster down to one sheet.
**Chrome:** consume the §2 dialog, the existing tool rail and tool registration (`ToolBase` through the composition root), and the settings store. Do not add a second preset store beside the style files.

**Requires:** display-session -- the tiling tool and overlay are driven on the canvas

- [ ] Add tiling to `PrintPlanner`: none, full pages, or imageable areas; overlap in units or percent of page width; row-major tile order with tile labels (AI-1072, CD-2665). Done when: `PrintTilingTests.A1OnA4` tiles an A1 fixture onto 8 A4 sheets with 10 mm overlap.
- [ ] Draw tiling marks (corner ticks and tile labels) per tile; §4's mark renderer takes them over once it ships. Done when: each tile's output contains four corner ticks in a test.
- [ ] Add `PrintTilingTool` in the Hand tool's flyout that moves the tiling origin, and View, Show Print Tiling drawing the tile grid overlay; the origin persists as `stilus:print-tiling` on the document (AI-0900, AI-0918). Done when: a driven run drags the origin and the overlay capture is committed, and the origin survives reopen.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/PrintStyleStore.cs`: `PrintStyle` JSON under `%LOCALAPPDATA%\Rizonesoft\Stilus\presets\print-styles\` with Save As, Load, Delete, Import, and Export (AI-1083, CD-2670). Done when: `PrintStyleStoreTests` round-trip a style and refuse a foreign file that fails the schema by name.
- [ ] Add Edit, Print Presets, a dialog that lists the saved styles with the same commands, and the default style name in `Stilus.Print.DefaultStyle`. Done when: setting a default style preselects it in the print dialog in a driven run.
- [ ] Add print to file: PRN through the driver's spool output and PDF through the §2 seam; the PostScript option is present but disabled with the tooltip `Planned: D02 T13 §10` (AI-1084, CD-2722, CD-2723). Done when: a PRN file is written and `MenuAuditTests` resolve the PostScript tooltip.
- [ ] Add split options: single file, pages to separate files, and plates to separate files (the plates option enabled by §5). Done when: pages to separate files writes one file per page in a test.
- [ ] Add the Summary page listing every setting and warning, with Save Summary writing a UTF-8 text report (AI-1082). Done when: a saved summary for the poster job lists the tile count and overlap.
- [ ] Log one Information line per style save, delete, or import. Done when: a Serilog test logger asserts the lines.
- [ ] Update `docs/user/stilus/printing.md` with tiling, styles, print to file, and the summary. Done when: the page documents each control.
- [ ] Commit: `"stilus: print tiling, print styles, print to file, and the print summary"`

**Test checkpoint:** Unit test plus driven run: `dotnet test Isotone.slnx` exits 0 with `PrintTilingTests` (an A1 fixture tiles to 8 A4 sheets with 10 mm overlap) and `PrintStyleStoreTests` reporting, and a driven Microsoft Print to PDF run of the poster yields 8 pages read back with PdfPig (count quoted). Cheaper substitute that fails: fit to page, which yields 1 page.

## 4. Printer's Marks and Bleed

A print shop needs sheets it can trim and register: crop marks, registration targets, color bars, and art that runs past the trim so a slightly off cut shows no white edge. This section adds one `PrinterMarksRenderer` shared by print and PDF, document bleed with a bleed limit, a marks placement tool in Print Preview, marks attached to object bounds, the Crop Marks live effect, and Create Trim Marks. Catalog: NP-2133 to NP-2144 (12 features: the crop marks live effect, create trim marks, crop and trim marks with weight, offset, and style, Japanese crop marks, composite crop marks on all plates, bleed and bleed limit, registration marks, the color calibration bar, densitometer scales, file information and page number marks, the marks placement tool, and marks attached to the object bounding box).

**Fidelity:** Printer's Marks and Bleed -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/print-preview/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/Checkbox/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the §2 print dialog and Print Preview; captured to `docs/captures/stilus/print-preview/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a print shop receives sheets it can trim and register. Consumer: the printed sheet and §15's PDF marks.
**Treatment:** a Marks and Bleed page plus draggable marks in Print Preview. Cheaper substitute that fails the checkpoint: marks drawn at the page edge with no bleed extension of the art.
**Chrome:** consume the §2 dialog and preview, the `D02 T11 §1` effect framework, and the suite history. Do not duplicate mark geometry between print and PDF: one `PrinterMarksRenderer`.

**Requires:** display-session -- the marks placement tool is driven in Print Preview

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/PrinterMarksRenderer.cs` emitting mark geometry as scene objects in the registration color: crop and trim marks with weight and offset, fold marks, and an exterior-only option (AI-1073, CD-2739). Done when: `PrinterMarksRendererTests` assert crop mark positions for Letter with 3 mm bleed and 6 mm offset.
- [ ] Add registration targets (CD-2742), a CMYK and spot color calibration bar (CD-2743), and a seven-step densitometer scale with editable densities (CD-2744). Done when: each mark is present at its documented position in a test.
- [ ] Add file information (job, profile, date, plate) and page number marks (CD-2745, CD-2746). Done when: the file-info mark's text contains the document name and date in a test.
- [ ] Add the mark style Roman or Japanese (double crop marks) with the preference `Stilus.Print.JapaneseCropMarks` (AI-1098, AI-1128). Done when: Japanese style emits two crop marks per corner.
- [ ] Add document bleed per side on the page model as `stilus:bleed` (reading `D02 T07 §4`'s value when present), use document bleed, and a bleed limit that clips art beyond the marks (CD-2741). Done when: a test asserts art extends 3 mm past the trim and is clipped at the bleed limit.
- [ ] Add composite crop marks on all plates as the preference `Stilus.Print.CompositeCropMarks`, consumed by §5 (CD-2740). Done when: the preference exists with a default and §5's plate test reads it.
- [ ] Add marks to objects: marks follow the selection bounding box instead of the page (CD-2748). Done when: a test places marks around a selected object's bounds.
- [ ] Add the Marks and Bleed page to the print dialog. Done when: the capture shows every control.
- [ ] Add `MarksPlacementTool` in Print Preview: auto-position or drag against an alignment rectangle, offsets saved in the print style (CD-2747). Done when: a driven run drags the calibration bar and the saved style holds the offset.
- [ ] Add the Crop Marks live effect through `D02 T11 §1`, with parameters in the `stilus:` namespace and the expanded marks as the fallback (AI-0673). Done when: reopening restores the effect live and an external reader sees the marks.
- [ ] Add Object, Create Trim Marks, an undoable command creating a grouped mark set around the selection (AI-0674). Done when: `CreateTrimMarksCommandTests` assert eight marks and that undo removes all of them.
- [ ] Commit `tests/fixtures/stilus/print/bleed-card.svg` and a golden SVG of its marks. Done when: `PrinterMarksRendererTests.BleedCardGolden` compares the marks element by element.
- [ ] Update `docs/user/stilus/printing.md` with marks and bleed. Done when: the page documents each mark and the placement tool.
- [ ] Commit: `"stilus: printer's marks, bleed, and trim marks"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Isotone.slnx` exits 0 with `PrinterMarksRendererTests` (the marks for `tests/fixtures/stilus/print/bleed-card.svg` compare element by element with the committed golden) and `CreateTrimMarksCommandTests` reporting, and the Microsoft Print to PDF output read with PdfPig shows art extending 3 mm past the trim box (coordinates quoted). Cheaper substitute that fails: marks with the art clipped at the trim.

## 5. Separations, Halftone Screens, and the Ink Manager

Prepress output is one plate per ink with the right screen, not a composite. This section adds composite or separated output, host-based plates rendered through the `D01 T04` transform, the ink manager with per-ink screens and aliases, film options, spot-to-process conversion, and print color management by Stilus or by the printer. In-RIP separations need a PostScript device and are enabled by §10; until then they are disabled naming it. Overprint flags arrive with §7, so objects knock out here. Catalog: NP-2145 to NP-2155 (11 features: composite or separations with plate choice, film output, convert spots to process, the ink manager and halftone screens, print color management, the PostScript halftone screen on a bitmap, printing with document or proof settings, output colors, preserve color numbers, the spot separations warning threshold, and separation order).

**Fidelity:** Separations, Halftone Screens, and the Ink Manager -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/print-dialog/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/ListTree/README.md, docs/design/components/Checkbox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the §2 print dialog with Color and Separations pages; captured to `docs/captures/stilus/print-dialog/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a prepress user can output one plate per ink with correct screens. Consumer: the printer or the plate files.
**Treatment:** an Output page with a plate list (print toggle, frequency, angle, dot shape) and an Ink Manager dialog. Cheaper substitute that fails the checkpoint: printing four grayscale conversions of the composite.
**Chrome:** consume the `D01 T04` transforms, the `D02 T09 §1` spot colors, and the §2 pipeline. Do not add a second CMYK conversion path.

**Requires:** display-session -- plates are printed to Microsoft Print to PDF and the pages captured

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/InkSet.cs`: process inks plus document spots, each with alias, print toggle, frequency, angle, dot shape (round, ellipse, line, square), and order, persisted in the print style (AI-1077, CD-2752, CD-2751). Done when: `InkSetTests` cover order changes and alias merging two spots onto one plate.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/SeparationRenderer.cs` rendering one 8-bit plate per ink through the `D01 T04` transform, preserving numbers or converting per policy, knocking out by default until §7 adds overprint flags. Done when: `SeparationRendererTests` assert plate tone values for C40 M0 Y0 K0 within 1 percent.
- [ ] Add composite or separations output with host-based separations printing each plate as a grayscale page labeled with the ink name (AI-1074, CD-2750). Done when: a driven print of the CMYK and spot fixture yields one page per selected ink.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/HalftoneScreen.cs` rasterizing host plates at printer resolution (AM screen per frequency, angle, and dot shape), reusing `D01 T03 §3` `HalftoneScreen` math. Done when: a test measures the screen angle and frequency of a plate within 1 percent.
- [ ] Show in-RIP separations only for a PostScript queue with a PPD; otherwise disabled with the tooltip `Planned: D02 T13 §10`. Done when: `MenuAuditTests` resolve the tooltip.
- [ ] Add film options: emulsion down (mirror), negative (invert), and printer resolution from the queue capabilities (AI-1075, CD-2769, CD-2770). Done when: tests assert a mirrored and an inverted plate.
- [ ] Add Convert all spot colors to process (AI-1076, CD-2682). Done when: the spot fixture prints to four process plates with the spot's CMYK alternate.
- [ ] Add output colors native, RGB, CMYK, or grayscale (CD-2681) and preserve color numbers (CD-2684). Done when: preserve numbers keeps C40 exact on the cyan plate and converting to grayscale yields one plate.
- [ ] Add print with document color settings or proof settings, the proof option reading §6's settings once shipped (CD-2679). Done when: a test with proof settings routes the render through the proofing transform.
- [ ] Add color management by Stilus (printer profile plus intent) or by the printer (CRD pass-through wired by §10) (AI-1080, CD-1595, CD-2680, CD-2683, CD-2685). Done when: a test asserts Stilus-managed output uses the chosen printer profile.
- [ ] Add the spot separations warning threshold `Stilus.Print.SpotWarning` (any, over 1, 2, or 3), shown on the Summary page (CD-2694). Done when: a four-spot document warns at threshold 3.
- [ ] Store a PostScript halftone screen on a bitmap as `stilus:halftone` (frequency, angle, dot shape), emitted by §10 (CD-1989). Done when: the attribute round-trips through save and reopen.
- [ ] Add the Color and Separations pages and the Ink Manager dialog (`Views/Print/InkManagerDialog.xaml`). Done when: the captures of both pages and the dialog are committed.
- [ ] Commit `tests/fixtures/stilus/print/cmyk-spot.svg` (process and a non-PANTONE spot) with lcms2-derived golden tone values per patch in `reference.txt`. Done when: the golden exists.
- [ ] Update `docs/user/stilus/printing.md` with separations and the ink manager. Done when: the page documents each control.
- [ ] Commit: `"stilus: separations, halftone screens, and the ink manager"`

**Test checkpoint:** Format fidelity proof plus driven run: `dotnet test Isotone.slnx` exits 0 with `SeparationRendererTests` comparing the plates of `tests/fixtures/stilus/print/cmyk-spot.svg` against the lcms2-derived golden tone values within 1 percent per patch, and `InkSetTests` reporting; the driven print yields one page per selected ink (page count and ink labels quoted from PdfPig). Cheaper substitute that fails: plates derived from an RGB render, which the C40 tone test rejects.

## 6. Soft Proofing, Gamut Warning, Overprint Preview, and Separations Preview

A designer should see how the press will render before paying for the run. This section applies the `D01 T04 §2` proofing transform to the canvas, adds the Color Proofing panel with presets, the gamut warning, export and print of the proof, Overprint Preview composed from the §5 plates, the Separations Preview panel, per-plate tabs in Print Preview, and a rasterize complex effects view. Catalog: NP-2103 to NP-2116 (14 features: overprint preview, proof setup, the proof colors toggle, the Separations Preview panel, the rasterize complex effects view, the Color Proofing panel, preserve numbers in the proof, the proof rendering intent, the gamut warning, proof presets, export soft proof, print proof, separations in Print Preview, and proof colors on by default).

**Fidelity:** Soft Proofing, Gamut Warning, Overprint Preview, and Separations Preview -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/color-proofing/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/color-proofing/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can see on screen how the press and its inks will render. Consumer: the canvas renderer and proof exports.
**Treatment:** View menu toggles plus a Color Proofing panel and a Separations Preview panel with per-plate eye toggles. Cheaper substitute that fails the checkpoint: a desaturation filter over the canvas.
**Chrome:** consume the `D01 T04` proofing transform, the §5 `SeparationRenderer`, and the `Isotone.UI` panel chrome. Do not render plates a second way.

**Requires:** display-session -- the proof toggles and the overlays are captured on the canvas

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Color/ProofSettings.cs` (device profile, preserve numbers, intent, simulate paper color, simulate black ink) including protanopia and deuteranopia simulations (AI-0914, CD-1580, CD-1581, CD-1582). Done when: `ProofTransformTests` simulate a FOGRA39-class device for sRGB patches within dE00 1.0 of the `transicc` goldens.
- [ ] Add proof presets as JSON under `%LOCALAPPDATA%\Rizonesoft\Stilus\presets\proof\` with save, delete, import, and export (CD-1584). Done when: a preset round-trips.
- [ ] Add View, Proof Colors (menu and status-bar button) and the preference `Stilus.Proof.OnByDefault` (AI-0915, CD-1578, CD-1602, CD-2887). Done when: toggling changes the canvas render hash and the preference turns proofing on for a new window.
- [ ] Apply the proofing transform as a final pass on each rendered canvas tile, cached per tile and per settings hash. Done when: a test asserts a cache hit on an unchanged redraw.
- [ ] Add the Color Proofing panel (`Views/Panels/ColorProofingPanel.xaml`) with device, intent, preserve numbers, simulate options, and presets (CD-1579, CD-1605). Done when: a driven run switches devices and the capture shows the panel.
- [ ] Add the gamut warning overlay with color and opacity from the panel, using the `D01 T04 §2` gamut check (CD-1583). Done when: a test marks a saturated sRGB green out of gamut for a FOGRA39-class device.
- [ ] Add View, Overprint Preview (Alt+Shift+Ctrl+Y) composing the §5 plates subtractively, spot inks from their Lab values, and knockout until §7 adds overprint flags (AI-0909, CD-042, CD-120). Done when: `OverprintPreviewTests` show C100 knocking out M100 as magenta now, and the §7 test flips it to blue.
- [ ] Add the Separations Preview panel (`Views/Panels/SeparationsPreviewPanel.xaml`): overprint toggle, per-plate visibility, and a spot-only view (AI-1086). Done when: hiding the cyan plate removes cyan from the canvas render in a test.
- [ ] Add composite and per-plate tabs to Print Preview (CD-2668, CD-2791). Done when: a capture shows the magenta plate tab.
- [ ] Add View, Rasterize Complex Effects rendering transparency and effects at output resolution for preview (CD-043, CD-121). Done when: the toggle changes the render of the transparency fixture to the flattened look.
- [ ] Add Export soft proof to JPEG and TIFF through WIC and to PDF (through §14 once shipped, `D02 T04 §4` before); CPT is refused by name (CD-1585). Done when: an exported proof JPEG matches the proofed canvas render within 1 of 255.
- [ ] Add Print proof routing the proofed render through §2 (CD-1586). Done when: a driven print proof writes a PDF whose image matches the proofed render.
- [ ] Update the Stilus user guide page `docs/user/stilus/soft-proofing.md`. Done when: the page documents both panels and every toggle.
- [ ] Commit: `"stilus: soft proofing, gamut warning, overprint preview, and separations preview"`

**Test checkpoint:** Unit test plus driven run: `dotnet test Isotone.slnx` exits 0 with `ProofTransformTests` (within dE00 1.0 of the `transicc` goldens) and `OverprintPreviewTests` reporting, and a proof-on capture with the gamut warning is committed under `docs/captures/stilus/color-proofing/`. Cheaper substitute that fails: a global saturation reduction, which the device-simulation golden rejects.

## 7. Overprint Attributes and Trapping

Misregistration on press leaves white gaps between inks unless objects overprint or trap. This section adds overprint fill and stroke attributes (including bitmaps and text), the Attributes panel, overprint black by threshold, document overprint handling, per-plate overprint, white overprint discard, the Trap command and Trap live effect, auto-spreading trap on print, and in-RIP trapping settings. Every attribute change is an undoable command with a line in the log and the history. It is borderline at 30 items, so object attributes and trapping are grouped. Catalog: NP-2156 to NP-2168 (13 features: the Trap command, overprint black by percentage, the Trap live effect, white overprint detection and discard, overprint fill and stroke on objects, the Attributes panel, overprint bitmap, document overprints, text overprint, overprint per separation, always overprint black and its threshold, auto-spreading trap, and in-RIP trapping settings).

**Fidelity:** Overprint Attributes and Trapping -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/attributes-panel/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Dialog/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/attributes-panel/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a prepress user can set objects to overprint and add traps so misregistration shows no gaps. Consumer: the §5 plates, the §6 preview, and the §14 PDF.
**Treatment:** Window, Attributes (Ctrl+F11) with overprint check boxes, and a Trap dialog. Cheaper substitute that fails the checkpoint: a flag that only changes the canvas look.
**Chrome:** consume the suite history, the `D02 T08 §10` path operations for trap geometry, and the `D02 T11 §1` effect framework. Do not add a second boolean engine.

**Requires:** display-session -- the Attributes panel and the Trap dialog are driven and captured

- [ ] Add `OverprintFill` and `OverprintStroke` attributes on every element, bitmaps and text runs included, persisted as `stilus:overprint-fill` and `stilus:overprint-stroke` (AI-1087, CD-544, CD-545, CD-546, CD-2757, CD-2758). Done when: the attributes round-trip through save and reopen.
- [ ] Add `SetOverprintCommand`, undoable, recording one history entry and one Serilog Information line. Done when: `OverprintCommandTests` assert the history entry, the log line, and undo.
- [ ] Add the Attributes panel (`Views/Panels/AttributesPanel.xaml`, Window, Attributes, Ctrl+F11) with overprint fill and stroke; its fill rule, reverse direction, image map, and note fields bind to the sections that own them and are disabled naming them until they ship (AI-1088). Done when: `MenuAuditTests` resolve every disabled field's tooltip and the capture is committed.
- [ ] Add Object, Overprint Fill, Overprint Stroke, and Overprint Bitmap menu items, the context menu entries, and the Properties panel toggles, all calling `SetOverprintCommand` (CD-1348, CD-1474, CD-2755, CD-2756). Done when: `MenuAuditTests` find each wired to the command.
- [ ] Teach §5's `SeparationRenderer` and §6's overprint preview to honor overprint flags. Done when: `OverprintPreviewTests` show C100 over M100 with overprint yields blue.
- [ ] Add Edit Colors, Overprint Black: black percentage threshold, fill and stroke, and include CMYK and spot blacks (AI-0481). Done when: a test sets overprint on every element at or above K95.
- [ ] Add print options: always overprint black with the threshold `Stilus.Print.OverprintBlackThreshold` (default 95), honoring `stilus:overprint-black` from `D02 T12 §1` (CD-2760, CD-2761). Done when: `OverprintBlackTests` assert K100 text overprints on the plates.
- [ ] Add document overprints ignore, preserve, or simulate (simulate rasterizes through §6) (CD-2753, CD-2754), and overprint graphics or text per plate (CD-2759). Done when: a test asserts each mode's plate output.
- [ ] Add Discard white overprint on output as a document option, with a detection pass that §9 preflight lists (AI-0975, AI-1090). Done when: a white overprinting object is removed from the plates and reported.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/TrapBuilder.cs` building trap objects with width, height, tint reduction, process traps, and reverse traps, spreading lighter into darker by neutral density, through `D02 T08 §10` path operations. Done when: `TrapBuilderTests` assert trap width and direction for yellow over cyan.
- [ ] Add Object, Trap (Pathfinder menu) running `TrapBuilder` as one undoable command (AI-0204, AI-1089). Done when: undo removes every trap object.
- [ ] Add the Trap live effect per `D02 T07 §1`, with parameters in `stilus:` and the expanded traps as the fallback (AI-0693). Done when: reopening restores it live.
- [ ] Add auto-spreading trap on print: overprinting outlines of the fill color up to a maximum or fixed width, and text above a size (CD-2762). Done when: a test asserts the spread outline on the plates.
- [ ] Add in-RIP trapping settings (widths, image placement, thresholds, ink types, color reduction) stored in the print style and emitted by §10 as trapping parameters and by §14 as the PDF `Trapped` key (CD-2763 to CD-2768). Done when: the settings round-trip in a style and a test asserts §14 writes `/Trapped /True` when enabled.
- [ ] Commit `tests/fixtures/stilus/print/trap.svg` and its trapped golden. Done when: `TrapBuilderTests.TrapGolden` compares element by element.
- [ ] Update the Stilus user guide page `docs/user/stilus/overprint-and-trapping.md`. Done when: the page documents the panel, commands, and options.
- [ ] Commit: `"stilus: overprint attributes, the Attributes panel, and trapping"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `OverprintCommandTests`, `OverprintBlackTests`, and `TrapBuilderTests` reporting; `tests/fixtures/stilus/print/trap.svg` trapped and saved compares element by element with its golden, and the §5 plates show the spread (tone at the trap edge quoted). Cheaper substitute that fails: a stroke added on the canvas only, which the plate test rejects.

## 8. Transparency Flattening and the Flattener Preview

Many RIPs and PDF/X-1a cannot carry transparency, so transparent art must be flattened into opaque regions, vector where possible and rasterized only where necessary. This section adds the flattener, its presets, Flatten Transparency as a command, the Flattener Preview panel that shows which regions rasterize, print as bitmap, and compatible gradient and mesh printing. Catalog: NP-2169 to NP-2174 (6 features: compatible gradient and mesh printing with raster effects resolution, print as bitmap and print flattening options, the Flatten Transparency command, the Flattener Preview panel, flattener presets and libraries, and gradient banding guidance).

**Fidelity:** Transparency Flattening and the Flattener Preview -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/flattener-preview/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Dialog/README.md, docs/design/components/Slider/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/flattener-preview/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can send transparent art to a device without transparency support and see which regions rasterize. Consumer: the §2 output, the §10 PostScript, and the §15 PDF/X-1a.
**Treatment:** a Flattener Preview panel highlighting regions on the canvas. Cheaper substitute that fails the checkpoint: rasterizing the whole page.
**Chrome:** consume the `D02 T08 §10` path operations, the `D01 T03` raster buffers, and the suite history. Do not add a second rasterizer.

**Requires:** display-session -- the preview highlight is captured on the canvas

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/TransparencyFlattener.cs`: a planar map of overlapping transparent regions through `D02 T08 §10` path operations, atomic regions kept as vectors where the raster/vector balance allows, else rasterized at the preset resolution with clip paths. Done when: `TransparencyFlattenerTests` flatten a 50 percent opacity overlap into 3 opaque regions with correctly blended colors.
- [ ] Add `FlattenerPreset` (raster/vector balance, line art and text resolution, gradient and mesh resolution, text to outlines, strokes to outlines, clip complex regions, anti-alias, preserve alpha, preserve overprints and spots) with High, Medium, and Low built-ins (AI-1093). Done when: each built-in's values are asserted in a test.
- [ ] Add Edit, Transparency Flattener Presets for custom presets with import and export under `%LOCALAPPDATA%\Rizonesoft\Stilus\presets\flattener\` (AI-1104). Done when: `FlattenerPresetStoreTests` round-trip a custom preset.
- [ ] Add Object, Flatten Transparency as one undoable command with one log line (object count in and out) (AI-1091). Done when: undo restores the original objects and the line is asserted.
- [ ] Add the Flattener Preview panel (`Views/Panels/FlattenerPreviewPanel.xaml`): highlight rasterized complex regions, transparent objects, all affected objects, expanded patterns, and outlined strokes and text; refresh; overprint mode (AI-1092). Done when: a driven run highlights rasterized regions on the fixture and the capture is committed.
- [ ] Add the print Advanced page: print as bitmap at a set dpi (1-bit devices dither through `D01 T03 §3`), overprint preserve, discard, or simulate, and the flattener preset (AI-1081, CD-2677). Done when: print as bitmap at 300 dpi yields one image per page in PdfPig and the 1-bit case contains only two values.
- [ ] Add compatible gradient and mesh printing, rasterizing shadings for older devices at the raster effects resolution from `D02 T12 §2` (AI-1079). Done when: a test asserts a rasterized shading at the document's raster resolution.
- [ ] Add banding guidance to the Summary page: gradient steps versus lpi and resolution with a warning under 256 steps (AI-1094). Done when: a low-step gradient produces the warning text.
- [ ] Add a budget test: a 2,000-object page with 200 transparent objects flattens under 5 seconds with cancellation. Done when: `FlattenerBudgetTests` quote the time.
- [ ] Commit `tests/fixtures/stilus/print/transparency.svg`. Done when: it exists with its expected region counts in `reference.txt`.
- [ ] Update the Stilus user guide page `docs/user/stilus/flattening.md`. Done when: the page documents the command, presets, and panel.
- [ ] Commit: `"stilus: transparency flattening, flattener presets, and the flattener preview"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `TransparencyFlattenerTests`, `FlattenerPresetStoreTests`, and `FlattenerBudgetTests` reporting; `tests/fixtures/stilus/print/transparency.svg` flattened renders within 1 percent of pixels of the unflattened render and contains no opacity attributes (both figures quoted). Cheaper substitute that fails: one full-page raster, which the vector-region count rejects.

## 9. Preflight, Package, and Collect for Output

A print shop rejects a job with missing fonts or RGB images, and it cannot print a document whose links point at the designer's disk. This section adds a preflight engine with savable styles, one preflight tab reused by the Print, PDF, and export dialogs, and File, Package (Collect for Output), which copies the document, its links, the fonts their licenses allow, and a report into one folder. Catalog: NP-2175 to NP-2178 (4 features: Package and Collect for Output, preflight in the Print, PDF, and export dialogs with savable styles, the banded fountain fill check, and the many-fonts threshold).

**Fidelity:** Preflight, Package, and Collect for Output -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/preflight/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Progress/README.md, docs/design/components/Checkbox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/preflight/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can see output problems before sending and hand a print shop everything needed. Consumer: the print shop folder.
**Treatment:** a Preflight tab with an issue list and a suggestion per issue, plus a Package dialog. Cheaper substitute that fails the checkpoint: copying the SVG alone.
**Chrome:** consume the settings store, the status-strip progress, and the `D02 T12 §7` `LinkManager`. Do not write a second link resolver.

**Requires:** display-session -- the Package dialog and the preflight tab are driven

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Preflight/PreflightEngine.cs` with `IPreflightRule` and `PreflightStyle` (enabled rules and thresholds) stored under `%LOCALAPPDATA%\Rizonesoft\Stilus\presets\preflight\` with save, delete, import, and export (CD-2669, CD-2696, CD-2781, CD-2788). Done when: `PreflightStyleStoreTests` round-trip a style.
- [ ] Add rules for missing or non-embeddable fonts and too many fonts over a threshold (CD-2695). Done when: each fires on its fixture in `PreflightEngineTests`.
- [ ] Add the banded fountain fill rule (steps versus span and lpi) (CD-2693). Done when: it fires on a 2-inch gradient with 32 steps at 150 lpi.
- [ ] Add rules for spot count, RGB or Lab in a CMYK job, images under an effective ppi, white overprint (from §7), hairlines, and off-page objects. Done when: each fires on its fixture in `PreflightEngineTests`.
- [ ] Add one preflight tab control in `src/Stilus/Isotone.Stilus.Desktop/Views/Preflight/PreflightTab.xaml` listing issues with a suggestion each, reused by the Print dialog, the PDF dialog (§15), and later export dialogs. Done when: the print dialog shows the tab with issues for the fixture and the capture is committed.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Preflight/PackageService.cs` and File, Package (Alt+Shift+Ctrl+P, also named Collect for Output): copy the document, copy links into a subfolder and relink the copy through `LinkManager`, copy fonts whose OS/2 `fsType` allows installable or editable embedding, and create a report (AI-0977, AI-0978, CD-2790). Done when: `PackageServiceTests` produce a folder whose document opens with every link resolved from the package and a restricted font skipped and listed.
- [ ] Write the report as UTF-8 text listing fonts, links, colors, inks, and preflight results, with one log line per package. Done when: the report for the fixture lists every link and the skipped font.
- [ ] Refuse a read-only or existing non-empty target folder with a message naming it, leaving nothing half-written. Done when: `PackageServiceTests.RefuseReadOnly` and `.RefuseNonEmpty` assert the message and an unchanged target.
- [ ] Run packaging with status-strip progress and Cancel. Done when: cancelling mid-copy leaves no target folder behind.
- [ ] Update the Stilus user guide page `docs/user/stilus/preflight-and-package.md`. Done when: the page documents every rule and the Package options.
- [ ] Commit: `"stilus: preflight and Package for output"`

**Test checkpoint:** Unit test plus driven run: `dotnet test Isotone.slnx` exits 0 with `PreflightEngineTests` (each rule fires on its fixture) and `PackageServiceTests` reporting; a driven Package of the linked fixture produces a folder whose document opens with every link resolved from the package (Links panel capture committed). Cheaper substitute that fails: absolute links left pointing at the source, which the open-from-package test rejects.

## 10. PostScript Output and Driver Compatibility Options

Imagesetters and many production RIPs take PostScript, and driver-generated PostScript from a GDI print loses spot colors, screens, and trapping. This section adds Stilus's own DSC-conforming `PostScriptWriter` with level, encoding, flatness, fountain steps, font download, bitmap compression and downsampling, halftones, in-RIP separations and trapping, PPD use, OPI links, and the driver compatibility options for non-PostScript printers. It enables §3's PostScript print-to-file option and §5's in-RIP separations. Ghostscript renders the fidelity goldens only when the user has installed it: it is AGPL, never bundled, and its version is recorded. Catalog: NP-2179 to NP-2188 (10 features: PostScript level and data format, OPI proxies and links, driver compatibility, bitmap output threshold and chunk overlap, bitmap downsampling, use a PPD, bitmap compression, optimize fountain fills and auto increase steps, auto increase flatness, and font download).

**Fidelity:** PostScript Output and Driver Compatibility Options -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/print-dialog/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the §2 print dialog with a PostScript page and the Printing preferences page; captured to `docs/captures/stilus/print-dialog/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a prepress user can write device-ready PostScript or print to a PostScript RIP. Consumer: the RIP and the `.ps` file.
**Treatment:** PostScript page controls enabled when the queue or the file target is PostScript. Cheaper substitute that fails the checkpoint: driver-generated PostScript from a GDI print.
**Chrome:** consume the §5 inks and screens, the §7 trapping settings, and the §2 pipeline. Do not add a second page renderer.

**Requires:** display-session -- the PostScript page is driven and captured

- [ ] Add `src/Stilus/Isotone.Stilus.Core/PostScript/PostScriptWriter.cs` writing DSC 3.0 output (`%%BoundingBox`, `%%Pages`, `%%DocumentProcessColors`, `%%PlateColor`), level 2 or 3, ASCII85 or binary (AI-1078, CD-2687). Done when: `PostScriptWriterTests.DscStructure` parse the comments of the fixture output and assert each.
- [ ] Write paths, and gradients as `shfill` at level 3 or stepped fills at level 2 with optimize fountain fills and auto increase steps (CD-2689, CD-2690). Done when: level 2 output of the gradient fixture contains no `shfill` and the step count follows the setting.
- [ ] Add flatness with auto increase (CD-2691). Done when: the `setflat` value in the output follows the setting and increases on a complex-path fixture.
- [ ] Write bitmaps with Flate or DCT compression and downsampling above a threshold (CD-2688, CD-2678). Done when: a 600 ppi image downsamples to the 300 ppi target in the output.
- [ ] Download fonts as Type 42 for TrueType and CFF as FontType 2 through `StartData`, or text as outlines; the TrueType to Type 1 option is documented as Type 42 (CD-2692). Done when: the text fixture's output embeds a Type 42 font and its glyph count equals the used glyphs.
- [ ] Emit `sethalftone` type 1 per plate from §5, `setpagedevice` Separations for in-RIP separations, and trapping parameters from §7, and pass a CRD through when the printer manages color. Done when: `PostScriptWriterTests.InRipSeparations` assert the `setpagedevice` dictionary.
- [ ] Add a PPD parser in `src/Stilus/Isotone.Stilus.Core/PostScript/PpdParser.cs` for `*DefaultResolution`, `*PageSize`, `*ColorDevice`, and `*LanguageLevel`, and the Use PPD option (CD-2686). Done when: `PpdParserTests` read a committed sample PPD.
- [ ] Add OPI: import a TIFF as an OPI proxy with its high-resolution path (`stilus:opi`), emit `%ALDImageFileName` comments, and hand the OPI dictionary to §14 (CD-2474, CD-2749, CD-2782). Done when: the output of the OPI fixture contains the comment with the path.
- [ ] Add driver compatibility preferences for GDI printers: text as graphics, software clipping, 64k bitmap chunks, and send curves (CD-2671 to CD-2674), plus the bitmap output threshold and chunk overlap (CD-2676), each a `Stilus.Print.Compat.*` setting consumed by the §2 backend. Done when: a test asserts each setting changes the backend's output mode.
- [ ] Enable §3's PostScript print-to-file option and §5's in-RIP separations for PostScript queues and file targets. Done when: `MenuAuditTests` find both enabled for a PostScript target.
- [ ] Add the PostScript page to the print dialog and the Printing preferences page. Done when: both captures are committed.
- [ ] Add format fidelity rendering: when a user-installed Ghostscript is found, render the output and compare with the canvas render within 2 percent of pixels, recording the Ghostscript version; otherwise run the structural tests alone and print that the render comparison was skipped and why. Done when: `PostScriptFidelityTests` report either the comparison or the named skip.
- [ ] Commit goldens under `tests/fixtures/stilus/postscript/` with `reference.txt` naming the Ghostscript version and command. Done when: every fixture has its golden.
- [ ] Update `docs/user/stilus/printing.md` with PostScript options and driver compatibility. Done when: the page documents each control.
- [ ] Commit: `"stilus: Stilus's own PostScript writer and driver compatibility options"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `PostScriptWriterTests` asserting the DSC structure and `PostScriptFidelityTests` comparing the output of `tests/fixtures/stilus/postscript/` rendered by a user-installed Ghostscript (external, AGPL, never bundled, version quoted) with the goldens within 2 percent of pixels. Cheaper substitute that fails: a `.ps` that embeds one page raster, which the DSC path and font assertions reject.

## 11. Imposition, Binding, and Page Placement

Booklets and n-up sheets print pages out of order so that they fold and cut into the right order. This section adds imposition layouts in Print Preview: presets, the layout tool, pages across and down, single or double sided with a manual-duplex wizard, binding modes, page placement ordering, manual sequence and rotation, gutters with cut and fold marks from §4, and margins. Catalog: NP-2189 to NP-2196 (8 features: layout presets, edit, and save, the imposition layout tool, pages across and down with single or double sides, binding modes, placement auto-ordering, manual sequence and rotation, gutters with cut and fold locations, and margins).

**Fidelity:** Imposition, Binding, and Page Placement -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/print-preview/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends Print Preview; captured to `docs/captures/stilus/print-preview/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a user can print booklets and n-up sheets that fold and cut into the right order. Consumer: the `PrintPlanner` sheets.
**Treatment:** an imposition layout tool with Basic, Placements, Gutters and Finishing, and Margins modes. Cheaper substitute that fails the checkpoint: n-up in sequential order only.
**Chrome:** consume the §2 preview and the §4 fold and cut marks. Do not add a second sheet model.

**Requires:** display-session -- the imposition tool is driven in Print Preview

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/Imposition/ImpositionLayout.cs`: across, down, sides (single or double), binding (perfect, saddle stitch, collate and cut, custom), placement ordering, gutters, and margins (CD-2727 to CD-2731, CD-2738). Done when: it serializes and round-trips.
- [ ] Add `ImpositionPlanner` mapping document pages to signature frames with rotation; saddle stitch nests signatures and pads the page count to a multiple of 4. Done when: `ImpositionPlannerTests.SaddleStitch8` asserts sheet 1 front holds pages 8 and 1 and its back pages 2 and 7.
- [ ] Add placement ordering intelligent, sequential, and cloned (CD-2732, CD-2733, CD-2734). Done when: tests assert each ordering for a 2x2 layout.
- [ ] Add a manual per-frame sequence number and rotation (CD-2735). Done when: a manual sequence overrides the auto ordering in a test.
- [ ] Add gutters, auto or equal with a size, and cut and fold locations drawn by §4's `PrinterMarksRenderer` (CD-2736, CD-2737). Done when: fold marks appear at the fold line in a test.
- [ ] Add presets (2x2 4-up, 2x3 6-up, booklet) and saved layouts as JSON under `%LOCALAPPDATA%\Rizonesoft\Stilus\presets\imposition\` with edit and save (CD-2724, CD-2725). Done when: a saved layout reloads with every field.
- [ ] Add the imposition layout tool in Print Preview with Basic, Placements, Gutters and Finishing, and Margins modes (CD-2726). Done when: a driven run changes the binding mode in the tool and the capture is committed.
- [ ] Add the manual-duplex wizard: print fronts, prompt to reinsert, then print backs (CD-2727). Done when: a driven run with Microsoft Print to PDF produces a fronts file and a backs file in the expected order.
- [ ] Update `docs/user/stilus/printing.md` with imposition. Done when: the page documents each mode and the wizard.
- [ ] Commit: `"stilus: imposition, binding, and page placement"`

**Test checkpoint:** Unit test plus driven run: `dotnet test Isotone.slnx` exits 0 with `ImpositionPlannerTests` reporting, and an 8-page booklet printed to Microsoft Print to PDF yields 4 sheet sides in saddle-stitch order, read back with PdfPig (page labels per side quoted). Cheaper substitute that fails: sequential 2-up, which the saddle-stitch order assertion rejects.

## 12. Layout Styles, Labels, and Banners

Folded cards, brochures, labels, and banners are designed as panels that print in a different arrangement from how they are drawn. This section adds layout styles on the document, label definitions with a public-domain starter set and user import, Save as Default, and Border and Grommet for banner documents. Catalog: NP-2197 to NP-2206 (10 features: the Page Layout dialog and full page style, book and booklet styles, folded card styles, the tri-fold style, label presets, custom label styles, save page layout as default, the Border and Grommet banner document, banner border types, and grommet size, margin, placement, and distribution).

**Fidelity:** Layout Styles, Labels, and Banners -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/page-layout/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/page-layout/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a user can design folded cards, brochures, labels, and banners with panels that print in the right place. Consumer: the page model and §11's imposition.
**Treatment:** a Page Layout dialog with style thumbnails, a label picker with a preview, and a Border and Grommet dialog. Cheaper substitute that fails the checkpoint: a guide grid with no print mapping.
**Chrome:** consume the `D02 T07 §3` page model and the settings store. Do not add a second page size table.

**Requires:** display-session -- the dialogs are driven and captured

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Print/Layout/LayoutStyle.cs` on the document (`stilus:layout-style`): full page, book, booklet, tent, side-fold, top-fold, and tri-fold, each defining panels per sheet, their order, and rotation, consumed by `PrintPlanner` and §11 (CD-2311 to CD-2318). Done when: `LayoutStyleTests` assert the panel map of each style.
- [ ] Render fold guides on the canvas for folded styles, and auto-order tri-fold panels for printing. Done when: `LayoutStyleTests.TriFold` asserts the printed panel order matches the golden panel map.
- [ ] Add the Page Layout dialog (`Views/Dialogs/PageLayoutDialog.xaml`, Layout, Page Layout) with style thumbnails (CD-2374). Done when: a driven run switches to tri-fold and the capture is committed.
- [ ] Add `SetLayoutStyleCommand`, one undoable command per change. Done when: undo restores the previous style.
- [ ] Add label definitions as JSON (sheet size, rows, columns, margins, gutters, label size) with a small public-domain starter set under `src/Stilus/Isotone.Stilus.Core/Print/Layout/Labels/` and import of user files; no manufacturer catalog is bundled without a data license (CD-2319). Done when: a test loads the starter set and imports a user file.
- [ ] Add a label picker with a preview and a Customize label style dialog that saves a new definition (CD-2320); labels map to pages at print time. Done when: a custom 3x10 definition prints 30 labels per sheet through `PrintPlanner` in a test.
- [ ] Add Save as Default writing the page size and layout to `Stilus.Document.DefaultPage` (CD-2321). Done when: a new document uses the saved default.
- [ ] Add Layout, Border and Grommet creating a new banner document from the page or the selection with border types (page color, solid, stretch edges, mirror edges) and size (CD-2771, CD-2772). Done when: each border type renders its golden in `GrommetPlacementTests`.
- [ ] Add grommet markers by count or spacing at corners and sides, with size and margin (CD-2773, CD-2774). Done when: `GrommetPlacementTests` assert marker positions for count 8 and for 300 mm spacing.
- [ ] Update the Stilus user guide page `docs/user/stilus/page-layout.md`. Done when: the page documents each style, labels, and banners.
- [ ] Commit: `"stilus: layout styles, labels, and banner documents"`

**Test checkpoint:** Format fidelity proof plus unit test: `dotnet test Isotone.slnx` exits 0 with `LayoutStyleTests` and `GrommetPlacementTests` reporting; a tri-fold fixture saves and reopens with its style, and the printed sheet order matches the golden panel map. Cheaper substitute that fails: panels printed in document order, which the panel-map assertion rejects.

## 13. Print Merge and Variable Data

Personalized badges, cards, and certificates come from a spreadsheet. This section adds CorelDRAW's Print Merge (data sources, records, text, image, and QR fields, print or create a merged document) and Illustrator's Variables panel (variables bound to objects, data sets, XML and CSV libraries, one file per data set), on one data model. It owns the CSV reader `D02 T14 §14` later reuses, reuses the RTF reader and the DocumentFormat.OpenXml reference `D02 T10 §13` adds, and adds ZXing.Net for the QR field, which `D02 T16 §11` then builds its styled QR objects on. If it overflows 30 items at build time, the natural split is Print Merge versus the Variables panel. Catalog: NP-2207 to NP-2224 (18 features: the Variables panel and variable types, make dynamic, unbind, and select bound object, data sets, the variable library XML and CSV sources, export one file per data set, Print Merge create, load, and edit, data source formats, merge columns, merge records, clear and keep merge data, save, import, and sync the source, ODBC, text, image, and QR fields, update and find fields, print merged document, and create merged document).

**Fidelity:** Print Merge and Variable Data -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/print-merge/, docs/captures/golden/stilus/variables/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/Progress/README.md, docs/design/components/Panel/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to `docs/captures/stilus/print-merge/` and `docs/captures/stilus/variables/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a user can produce personalized cards or badges from a spreadsheet. Consumer: the printer, the merged document, and the per-set exports.
**Treatment:** a Configure Data Source dialog with a record grid, and a Variables panel. Cheaper substitute that fails the checkpoint: find and replace per record by hand.
**Chrome:** consume the `D02 T10 §2` text runs, the `D02 T10 §13` RTF reader, the §2 printing, and the suite history. Do not add a second CSV parser or a second QR encoder.

**Requires:** display-session -- the data source dialog and the panel are driven

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Merge/MergeDataSource.cs`: columns (text, numeric with format and auto-increment, path), records, and a record selection, persisted as `stilus:merge-data` when `Stilus.Merge.SaveInDocument` is on (CD-2701, CD-2702, CD-2890). Done when: `MergeDataSourceTests` round-trip the data through save and reopen.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Merge/Readers/CsvReader.cs` for CSV and TXT (RFC 4180 quoting, delimiter detection), the one CSV reader in Stilus. Done when: `MergeDataSourceTests.CsvQuoting` reads quoted commas, quotes, and newlines.
- [ ] Add RTF table sources through the `D02 T10 §13` RTF reader and XLSX through DocumentFormat.OpenXml with a sheet choice (CD-2700). Done when: tests read the committed RTF and XLSX fixtures into the expected records.
- [ ] Add ODBC sources through `System.Data.Odbc` with a connection string and a query, recorded in `docs/dev/decisions.md` as part of .NET (CD-2711). Done when: a test against the Microsoft Access Text Driver reading a CSV folder returns rows, or is skipped naming the missing driver.
- [ ] Add save data source to CSV, import a column, and sync (re-read a changed source) (CD-2708, CD-2709, CD-2710, CD-2712). Done when: a sync after editing the CSV fixture updates the records.
- [ ] Add the Configure Data Source dialog (`Views/Merge/ConfigureDataSourceDialog.xaml`): add, delete, and edit records, browse paths, view all or single, first, previous, next, last, go to record, select all or none, and clear merge data (CD-2697 to CD-2699, CD-2703 to CD-2707). Done when: a driven run edits a record and the capture shows the grid. Cheaper substitute: a read-only grid.
- [ ] Add merge text fields as live objects (`stilus:merge-field`), inside text runs or standalone (CD-2713). Done when: a text field renders the current record's value on the canvas.
- [ ] Add image placeholder fields with scaling (actual, fill, fit, stretch) and a reference point (CD-2714, CD-2715). Done when: each scaling mode's bounds are asserted in `MergeRenderTests`.
- [ ] Add ZXing.Net (Apache-2.0) with a `docs/dev/decisions.md` row and `src/Stilus/Isotone.Stilus.Core/Barcodes/QrMatrixEncoder.cs` returning the module matrix, and QR code fields with type and scaling drawn as vector modules (CD-2716). Done when: a QR field for a record decodes back to the record's value through ZXing.Net in a test.
- [ ] Add Update Field and Find Print Merge Fields in Find and Replace (CD-2717, CD-2718). Done when: find selects every merge field in the fixture.
- [ ] Add Print Merged Document through §2 and Create Merged Document writing one page per record (CD-2719, CD-2720). Done when: `MergeRenderTests` assert 3 records produce 3 pages with the right text.
- [ ] Add the Variables panel (`Views/Panels/VariablesPanel.xaml`) with visibility, text, linked file, and graph data variables bound to objects, Make Dynamic, Unbind, and Select Bound Object (AI-1234, AI-1235, AI-1236). Done when: making a text object dynamic and switching data sets changes its text in a driven run.
- [ ] Add data sets: capture, next, previous, rename, and delete (AI-1237). Done when: `VariableLibraryTests` cover each command with undo.
- [ ] Add the variable library XML (the Illustrator variable library schema) and CSV import and export with `@` image path columns (AI-1238, AI-1239). Done when: `VariableLibraryTests.XmlRoundTrip` round-trips the XML fixture byte-equal after normalization.
- [ ] Add Export one file per data set as a Stilus command (SVG, PDF, PNG) with progress and cancel (AI-1240). Done when: exporting 3 data sets writes 3 files with the right text.
- [ ] Log one Information line per merge, sync, and per-set export. Done when: a Serilog test logger asserts the lines.
- [ ] Commit fixtures under `tests/fixtures/stilus/merge/` (`badges.csv`, `badges.svg`, `badges.xlsx`, `badges.rtf`, a variable library XML) and the merged-document golden. Done when: every fixture exists.
- [ ] Update the Stilus user guide page `docs/user/stilus/print-merge.md`. Done when: the page documents the dialog, fields, and Variables panel.
- [ ] Commit: `"stilus: print merge and variable data"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `MergeDataSourceTests` (CSV quoting, the XLSX sheet, numeric auto-increment), `MergeRenderTests` (3 records produce 3 pages with the right text), and `VariableLibraryTests` reporting; `tests/fixtures/stilus/merge/badges.csv` with `badges.svg` creates a merged document compared element by element to its golden, and the variable library XML round-trips byte-equal after normalization. Cheaper substitute that fails: text replaced on one page only, which the three-page comparison rejects.

## 14. The PDF Writer: Spot Colors, Layers, and Exact Vector Output

The PDF a print shop receives must say exactly what the document says: spot colors as spot colors, layers as layers, CMYK as CMYK, and every path at full precision. `SKDocument` (today's export from `D02 T04 §4`) cannot write Separation color spaces, optional content groups, or CMYK, so this section replaces it with Stilus's own content-stream writer on PDFsharp's object model. It owns font embedding with its own TrueType subsetter, the first candidate to move out if it grows. Catalog: NP-2225 to NP-2232 (8 features: Publish to PDF, the export range, page size from the document or the selection, export only objects on the page, embed and subset fonts, convert TrueType to Type 1 as a documented no-op, export all text as curves, and preserve layers as optional content groups).

**Fidelity:** The PDF Writer: Spot Colors, Layers, and Exact Vector Output -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/export-pdf/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the `D02 T04 §4` export dialog; captured to `docs/captures/stilus/export-pdf/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can send a PDF that a print shop's RIP reproduces exactly. Consumer: the PDF file, Acrobat, and RIPs.
**Treatment:** File, Publish to PDF with General and Objects pages. Cheaper substitute that fails the checkpoint: the `SKDocument` output, which cannot express spot colors, optional content groups, or CMYK.
**Chrome:** consume the §1 profiles, the atomic file writer, and the `D02 T04 §4` dialog shell. Do not keep two PDF writers after this section.

**Requires:** display-session -- the Publish to PDF dialog is driven and captured

- [ ] Add PDFsharp (MIT) to `Directory.Packages.props`, referenced by `Isotone.Stilus.Core`, with a `docs/dev/decisions.md` row (license versus GPL-3.0, why own content streams over `SKDocument`). Done when: the row exists and the build restores the package.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Pdf/PdfContentWriter.cs` emitting path, state, and drawing operators (`m l c h re`, `cm`, `q Q`, `gs`, `sh`, `Do`) with fixed 4-decimal invariant-culture precision. Done when: `PdfContentWriterTests` assert the operator stream for each primitive fixture.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Pdf/PdfResourceBuilder.cs` deduplicating ExtGState, ColorSpace, Pattern, Shading, XObject, and Font resources. Done when: two identical gradients yield one Shading resource in a test.
- [ ] Write gradients from `D02 T09 §7` as type 2 and 3 shadings with stitching functions, meshes from `D02 T09 §9` as type 6 or 7 shadings, and pattern fills from `D02 T09 §10` as tiling patterns. Done when: PdfPig reads each shading type from the gradient, mesh, and pattern fixtures.
- [ ] Write opacity, blend modes from `D02 T09 §19`, and opacity masks from `D02 T09 §20` as transparency groups with luminosity soft masks. Done when: the transparency fixture's page carries `/Group` and `/SMask` entries read back with PdfPig.
- [ ] Write spot colors as Separation color spaces with a Lab or CMYK alternate and a tint transform, multi-ink as DeviceN, native CMYK, and ICCBased spaces from §1. Done when: `PdfSpotColorTests` read the Separation name and alternate of the spot fixture.
- [ ] Write layers as OCGs with visibility and print state in `/OCProperties`, excluding master layers with a note in the log (CD-2552). Done when: `PdfOcgTests` read every layer name and its view and print state.
- [ ] Add an own TrueType `glyf` subsetter in `src/Stilus/Isotone.Stilus.Core/Pdf/Fonts/TrueTypeSubsetter.cs` and embed fonts as Type0 with CIDFontType2, CFF fonts embedded directly, and a ToUnicode CMap. Done when: `PdfFontEmbeddingTests` extract the text fixture's text through PdfPig unchanged and the subset holds only used glyphs.
- [ ] Respect OS/2 `fsType` (a restricted font is outlined and reported), apply the subset threshold, and add Export all text as curves; the TrueType to Type 1 option is a documented no-op (CD-2540, CD-2541, CD-2542, CD-2543). Done when: a restricted-font fixture writes outlines and a log line names the font.
- [ ] Write MediaBox, TrimBox, and BleedBox from the document bleed once §4 has shipped (BleedBox equals TrimBox before). Done when: the bleed card fixture's boxes read back with the 3 mm difference.
- [ ] Add the export range (document, several documents, selection, current page, pages), page size from the document or the selection, and only objects on the page, which clips off-page art (CD-2525, CD-2526, CD-2539). Done when: `PdfRangeTests` cover each range and the off-page clip.
- [ ] Add File, Publish to PDF (CD-2518) with General and Objects pages on the `D02 T04 §4` dialog shell, writing through the atomic file writer. Done when: the capture is committed and a read-only target is refused by name.
- [ ] Replace `PdfExporter` behind the `IPdfJobWriter` seam used by §2 and §6, keeping `PdfExporterTests` green on the new writer and deleting the `SKDocument` path. Done when: `grep -rn "SKDocument" src/Stilus` prints nothing and `PdfExporterTests` pass.
- [ ] Add a budget test: a 10,000-object page writes under 3 seconds with progress and cancel. Done when: `PdfBudgetTests` quote the time.
- [ ] Add render goldens under `tests/fixtures/stilus/pdf/` from MuPDF `mutool draw` (external, AGPL, test time only, version recorded in `reference.txt`). Done when: every fixture has a golden.
- [ ] Update the Stilus user guide page `docs/user/stilus/pdf.md`. Done when: the page documents the General and Objects pages.
- [ ] Commit: `"stilus: Stilus's own PDF writer with spot colors, layers, and embedded fonts"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `PdfContentWriterTests`, `PdfSpotColorTests`, `PdfOcgTests`, `PdfFontEmbeddingTests`, `PdfRangeTests`, and `PdfExporterTests` reporting; the fixtures under `tests/fixtures/stilus/pdf/` export, read back with PdfPig (paths, Separation names, OCG names, embedded fonts, text), and render against the MuPDF `mutool draw` goldens within 1 percent of pixels (version and worst figure quoted). Cheaper substitute that fails: the `SKDocument` output, which has no Separation color space.

## 15. PDF Presets and Standards: PDF/X, PDF/A, Compatibility, Compression, and Marks

"PDF/X-4" is a promise to a print shop's preflight, not a version number: it requires an output intent, a trim box, embedded fonts, and more. This section adds PDF presets with a standards enforcer for PDF/X-1a, X-3, X-4, and PDF/A, compatibility levels that gate features and report conflicts, compression and downsampling, marks and bleeds from §4, output color conversion, overprint and flattener options, the preflight tab, the summary, multi-document PDF, encoding, EPS handling, and complex fills as bitmaps. If it overflows 30 items at build time, the natural split is presets and dialog pages versus standards enforcement. Catalog: NP-2233 to NP-2251 (19 features: the Save as PDF dialog and its categories, PDF presets, PDF/X standards, compatibility levels, general options, compression and downsampling, marks and bleeds, output color conversion and profile inclusion, advanced overprint and flattener options, the summary, the current proof settings, spot conversion, PDF/A presets, distribution, editing, and web presets, several documents to one PDF, ASCII85 or binary encoding, EPS in PDF, complex fills as bitmaps, and the preflight tab).

**Fidelity:** PDF Presets and Standards: PDF/X, PDF/A, Compatibility, Compression, and Marks -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/export-pdf/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ListTree/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the §14 dialog with Preset, Compression, Marks and Bleeds, Output, Advanced, Preflight, and Summary pages; captured to `docs/captures/stilus/export-pdf/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can pick "PDF/X-4" and get a file the printer's preflight accepts. Consumer: print shop preflight and archives.
**Treatment:** a preset dropdown with standards compliance enforced by rule. Cheaper substitute that fails the checkpoint: setting the version key without enforcing the standard's rules.
**Chrome:** consume the §4 marks, the §8 flattener, the §9 preflight engine, and the §1 profiles. Do not add a second preset store beside the print styles.

**Requires:** display-session -- the preset pages are driven and captured

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Pdf/PdfExportSettings.cs` and `PdfPresetStore` (JSON under `%LOCALAPPDATA%\Rizonesoft\Stilus\presets\pdf\`) with create, edit, delete, import, and export (AI-1055, CD-2528). Done when: `PdfPresetStoreTests` round-trip a user preset.
- [ ] Ship built-in presets: High Quality Print, Press Quality, Smallest File Size, PDF/X-1a, PDF/X-3, PDF/X-4, Prepress, Archiving CMYK and RGB (PDF/A), Document Distribution, Editing, Web, and Current Proof Settings (AI-1056, CD-2775, CD-2776, CD-2777, CD-2519, CD-2520, CD-2522, CD-2523, CD-2524, CD-1599, CD-2521). Done when: each built-in loads and exports the fixture without error.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Pdf/PdfStandardEnforcer.cs` applying ISO 15930 rules for PDF/X (OutputIntent with `GTS_PDFX`, TrimBox, fonts embedded, no transparency for X-1a and X-3 through §8, no RGB for X-1a). Done when: `PdfStandardEnforcerTests` show X-1a rejecting an RGB image or converting it per the preset.
- [ ] Add ISO 19005 rules for PDF/A (XMP metadata, no encryption, embedded output profile). Done when: the PDF/A fixtures validate with veraPDF with zero failures (version recorded).
- [ ] Add compatibility 1.3 to 1.7 gating features (transparency needs 1.4, OCGs 1.5), reporting conflicts in the dialog instead of dropping silently (AI-1057, CD-2551). Done when: a 1.3 export of a layered document lists the OCG conflict.
- [ ] Add compression: Flate through `ZLibStream`, JPEG through WIC with quality, and an own LZW encoder; downsampling average, bicubic, or subsample with thresholds; compress text and line art; JPEG2000 and CCITT refused by name (AI-1059, CD-2536, CD-2537, CD-2538). Done when: `PdfCompressionTests` assert each filter name in the image dictionaries and the refusal message.
- [ ] Add ASCII85 or binary encoding (CD-2544). Done when: an ASCII85 export contains only ASCII bytes in its streams.
- [ ] Add marks and bleeds from §4's `PrinterMarksRenderer` with the bleed limit (AI-1060, CD-2783 to CD-2787). Done when: the bleed card export carries crop marks outside the TrimBox.
- [ ] Add output options: convert to destination, the profile inclusion policy, document or proof settings (§6), and convert spot colors (AI-1061, CD-1598, CD-1600, CD-1601). Done when: converting spots removes every Separation space from the spot fixture's export.
- [ ] Add Advanced options: preserve overprints, always overprint black, the font subset threshold, the flattener preset from §8, and render complex fills as bitmaps (AI-1062, CD-2778, CD-2779, CD-2554). Done when: an X-1a export of the transparency fixture contains no transparency group.
- [ ] Add General options: view after saving, thumbnails, layers from top-level layers, and one PDF from several open documents (AI-1058, CD-2527). Done when: exporting two open documents writes one PDF with both page sets.
- [ ] Add EPS in PDF as a PostScript XObject or its preview, stored in the preset and shown disabled with the tooltip `Planned: D02 T14 §9` until EPS placement exists (CD-2545). Done when: `MenuAuditTests` resolve the tooltip.
- [ ] Add the Preflight page reusing the §9 tab, and the Summary page with Save Summary (AI-1064, CD-2780). Done when: the X-1a preset with an RGB image lists the problem on the Preflight page.
- [ ] Add the Preset, Compression, Marks and Bleeds, Output, Advanced, Preflight, and Summary pages to the dialog (AI-1008). Done when: each page's capture is committed.
- [ ] Update `docs/user/stilus/pdf.md` with presets and standards. Done when: the page documents every preset and page.
- [ ] Commit: `"stilus: PDF presets, PDF/X and PDF/A standards, compression, and marks"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `PdfPresetStoreTests`, `PdfStandardEnforcerTests`, and `PdfCompressionTests` reporting; the PDF/A fixtures validate with veraPDF (version quoted) with zero failures, and the PDF/X fixtures pass the rule checks and carry the OutputIntent read back by PdfPig. Cheaper substitute that fails: a version key with RGB content in a PDF/X-1a file, which the enforcer test rejects.

## 16. PDF Interactivity and Security: Bookmarks, Hyperlinks, Tagged PDF, and Passwords

A PDF sent to a client is navigated, read by screen readers, and sometimes protected. This section adds hyperlinks, bookmarks, thumbnails, the on-start view, comments, symbols written once as form XObjects, tagged accessible PDF with alt text, open and permissions passwords enforced by encryption, and linearized web output. Object hyperlinks are a small model added here (`Hyperlink`: a URL on any element, persisted as an SVG `<a>`), which `D02 T14 §17` later extends with more schemes, bookmark targets, and image maps rather than adding a second model; text hyperlinks come from `D02 T10 §2`. Passwords never persist anywhere. Catalog: NP-2252 to NP-2261 (10 features: security with open and permissions passwords, tagged accessible PDF, symbols as reusable PDF objects, hyperlinks, bookmarks, page thumbnails, the on-start view, include comments, printing, editing, and copying permissions, and web optimization).

**Fidelity:** PDF Interactivity and Security: Bookmarks, Hyperlinks, Tagged PDF, and Passwords -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/export-pdf/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/Checkbox/README.md, docs/design/components/TextBox/README.md, docs/design/components/ListTree/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the §14 dialog with Document and Security pages; captured to `docs/captures/stilus/export-pdf/`. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can send an accessible, navigable, protected PDF. Consumer: PDF readers and screen readers.
**Treatment:** Document and Security pages whose password fields never persist. Cheaper substitute that fails the checkpoint: a permissions flag without encryption.
**Chrome:** consume the §14 writer, the `D02 T10 §2` text hyperlinks, and the `D02 T09 §21` symbols. Do not store passwords in presets or settings.

**Requires:** display-session -- the Security page and a password-protected open are driven

- [ ] Add `src/Stilus/Isotone.Stilus.Core/Models/Hyperlink.cs`: a URL (http, https, mailto, file) on any element persisted as an SVG `<a href>` wrapper, with `SetHyperlinkCommand` (undoable); `D02 T14 §17` extends this type. Done when: a hyperlinked rectangle round-trips through save and reopen.
- [ ] Write object and text hyperlinks as Link annotations with URI actions (CD-2531). Done when: `PdfLinkBookmarkTests` read each link's rectangle and URI with PdfPig.
- [ ] Write bookmarks from pages and named layers as the outline tree (CD-2532). Done when: the outline read back lists every page and named layer.
- [ ] Add the on-start view (page only, bookmarks, thumbnails) through `/PageMode` (CD-2534) and page thumbnails as `/Thumb` images from the page render (CD-2533). Done when: each `/PageMode` value and a `/Thumb` entry read back.
- [ ] Include comments as Text annotations (CD-2535). Done when: a document note appears as a Text annotation.
- [ ] Write symbols from `D02 T09 §21` once as form XObjects referenced per instance (CD-2530). Done when: a document with 50 instances of one symbol has one form XObject.
- [ ] Add tagged PDF: StructTreeRoot, MarkInfo, marked-content IDs per object, `Figure` with `/Alt` from the object's `<desc>` or `stilus:alt`, and reading order by layer order (AI-1065). Done when: `PdfTaggingTests` read every figure's alt text and the structure order.
- [ ] Add security through the PDFsharp security handler: open password and permissions password (AI-1063, CD-2546, CD-2550), with AES where the pinned version supports it and RC4-128 otherwise, recorded in the `docs/dev/decisions.md` row. Done when: `PdfSecurityTests` show PdfPig refusing the file without the password and opening it with it.
- [ ] Add permissions: printing none, low, or high; editing none, page assembly, or any except extraction; and copying (CD-2547, CD-2548, CD-2549). Done when: `PdfSecurityTests` read the permission bits back for each combination.
- [ ] Keep passwords out of presets, settings, and logs; the log line records only that encryption was applied. Done when: a test saves a preset from a dialog with passwords set and asserts neither password appears in the preset file, `settings.json`, or the log.
- [ ] Add Optimize for web through an own linearization post-pass (ISO 32000-1 Annex F hint tables) (CD-2553). Done when: `qpdf --check-linearization` (external, Apache-2.0, test time only, version recorded) passes on the fixture output, or the test is skipped naming the missing tool.
- [ ] Add the Document and Security pages to the dialog. Done when: both captures are committed and a driven open of a protected export prompts for the password.
- [ ] Update `docs/user/stilus/pdf.md` with interactivity, tagging, and security. Done when: the page documents both pages.
- [ ] Commit: `"stilus: PDF links, bookmarks, tagging, security, and linearization"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx` exits 0 with `PdfLinkBookmarkTests`, `PdfTaggingTests`, and `PdfSecurityTests` reporting; the fixtures validate as PDF/UA-1 in veraPDF (version quoted) and as linearized in qpdf, and the permission bits read back. Cheaper substitute that fails: `/Alt` missing on figures or a password stored in the preset, which the tagging and password-leak tests reject.

## 17. Interactive 3D Models in PDF: U3D Annotations

CorelDRAW keeps 3D models interactive in exported PDF (Compatibility Acrobat 8.0 or higher), so a reviewer rotates a product mockup in Acrobat Reader instead of looking at one frozen angle. Stilus's 3D and Materials objects (`D02 T11 §10`) already hold a `Mesh3D` with materials, lights, and a camera; this section writes them into the PDF of §14 as 3D annotations (ISO 32000-1 section 13.6, `/Subtype /3D`) carrying a U3D stream (ECMA-363 4th edition, 2007), with named views, activation and deactivation, lighting, rendering mode, and the rendered view as the annotation's appearance and poster so every other reader still shows the art. No maintained .NET writer exists for U3D or PRC: the Intel Universal 3D Sample Software (Apache-2.0, maintained fork github.com/ningfei/u3d) is native C++ and PRC's only open writer is Asymptote's `oPRCFile` (LGPL-3.0), so Stilus writes U3D with its own managed encoder built from ECMA-363, and uses the Intel sample's IDTF tools only as a test-time oracle. Both licenses are GPL-3.0 compatible, recorded in the decision item. -> SOURCE: parity-pdf-3d. Catalog: NP-2262 (1 feature: interactive 3D models in PDF).

**Fidelity:** Interactive 3D Models in PDF: U3D Annotations -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/export-pdf-3d/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the §14 Publish to PDF dialog; captured to `docs/captures/stilus/export-pdf-3d/` (the 3D option on the Objects page and Acrobat Reader showing the activated model). The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can send a PDF whose 3D mockup the reviewer can rotate, zoom, and switch views on. Consumer: Acrobat and Acrobat Reader, and any PDF reader through the poster appearance.
**Treatment:** an "Export 3D objects as interactive 3D" check box with a views list (default view plus the named views of each 3D object) and an activation choice (on page open, on click) on the §14 Objects page. Cheaper substitute that fails the checkpoint: embedding only the rendered bitmap, which the annotation-dictionary test catches.
**Chrome:** consume the §14 writer and dialog shell, the `D02 T11 §10` `Mesh3D`, `MaterialLibrary`, and `PathTracer`, and the settings store. Do not add a second PDF writer or a second 3D scene model.

**Requires:** display-session -- the Publish to PDF dialog is driven and captured, and the Acrobat Reader check is a driven run

- [ ] Record in `docs/dev/decisions.md` the 3D PDF decision: U3D (ECMA-363) written by an own managed encoder because Acrobat and Reader read it since PDF 1.6 and the Intel sample is native C++; PRC (ISO 14739-1) through Asymptote's LGPL-3.0 `oPRCFile` rejected because it needs a native build and adds no reader coverage; the Intel U3D sample (Apache-2.0, license verified 2026-09-27 at the ningfei/u3d fork) used only as a test-time oracle, and any file ported from it keeping its Apache-2.0 header and NOTICE. Done when: the row names both licenses, the commits checked, and the reason.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/Pdf/ThreeD/U3dBitStreamWriter.cs`: the ECMA-363 section 10 context-adaptive arithmetic coder (static and dynamic contexts, U8 to U32, F32, and strings). Done when: `U3dBitStreamWriterTests` encode the committed coder vectors and decode them back with an own test decoder built from the same clauses.
- [ ] Add `U3dFileWriter` with the file header, the modifier chain, and the node blocks (group, model, light, view) of ECMA-363 section 9. Done when: a single-triangle file matches the committed golden byte for byte.
- [ ] Add the CLOD mesh generator declaration and base mesh continuation blocks writing positions, normals, texture coordinates, and faces of each `Mesh3D` at full resolution (no progressive resolution updates). Done when: `U3dMeshTests` write the cube and the inflated-logo fixture meshes and the Intel sample's `IDTFConverter` export of the same geometry decodes to the same vertex and face counts.
- [ ] Map `MaterialLibrary` materials to U3D material and lit texture shader resources (diffuse, specular, emissive, opacity, one texture layer as PNG image resource). Done when: a test asserts each material's colors in the written resource block.
- [ ] Write the scene's lights (ambient, directional, point, spot) and the camera as U3D light and view nodes. Done when: a test reads back the light and view blocks with the own test decoder.
- [ ] Add `Pdf3DAnnotationWriter` on §14's `PdfResourceBuilder`: the `/3D` stream (`/Subtype /U3D`), the `/3DD` and `/3DV` view dictionaries (camera to world matrix, center of orbit, projection, background, render mode, lighting scheme), `/3DA` activation, and the page annotation at the object's bounds. Done when: `Pdf3DAnnotationTests` parse the written PDF with PdfPig and assert every key against ISO 32000-1 table 298 to table 304.
- [ ] Write the annotation's `/AP` appearance and the poster from the `D02 T11 §10` render of the default view, so readers without 3D support show the art. Done when: MuPDF `mutool draw` renders the page within the §14 tolerance of the non-3D export of the same page.
- [ ] Named views: the default view plus each saved 3D view of the object become `/VA` entries in document order. Done when: a test with three saved views asserts three `/3DV` entries with their names.
- [ ] Add the dialog option on the §14 Objects page with the views list and activation choice, persisted under `Stilus.Export.Pdf.ThreeD.*` and read by `Pdf3DAnnotationWriter`. Done when: a settings readback asserts each default and the dialog capture is committed.
- [ ] Refuse the option by name when the §15 preset forbids it: PDF/X and PDF/A presets and compatibility below Acrobat 7 (PDF 1.6) export the poster only with a report line. Done when: a PDF/X-4 export of the fixture has no `/3D` annotation and the report names the reason.
- [ ] Log `Exported 3D annotation {ElementId} ({Vertices} vertices, {Views} views)` once per 3D object. Done when: the line is asserted with a Serilog test logger.
- [ ] Commit fixtures `tests/fixtures/stilus/pdf-3d/` (cube, inflated logo with texture, revolved bottle with three views) with the Intel U3D sample `IDTFConverter` decode report and the PdfPig key dump as goldens, versions recorded. Done when: every fixture has its goldens.
- [ ] Update `docs/user/stilus/export-pdf.md` with interactive 3D, its views, and its limits (Acrobat and Reader only; other readers show the poster). Done when: the page covers the option and the refusal.
- [ ] Commit: `"stilus: interactive 3D models in exported PDF"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~U3dBitStreamWriterTests|FullyQualifiedName~U3dMeshTests|FullyQualifiedName~Pdf3DAnnotationTests"` exits 0: each fixture's U3D stream decodes through the Intel U3D sample tools to the source vertex, face, material, and view counts, and the PDF's 3D annotation keys match ISO 32000-1; driven run with evidence: the bottle fixture opened in Acrobat Reader activates and rotates, captured to `docs/captures/stilus/export-pdf-3d/`, and `mutool draw` renders the poster. Cheaper substitute that fails: embedding the rendered bitmap only, which the `/3D` annotation assertion catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx` exits 0 with every `tests/Isotone.Stilus.Tests/Color/`, `Print/`, `Preflight/`, `PostScript/`, `Merge/`, and `Pdf/` class reporting
- [ ] Every fixture under `tests/fixtures/stilus/icc/`, `print/`, `postscript/`, `merge/`, and `pdf/` carries its golden and `reference.txt` naming the oracle (lcms2 `transicc`, Ghostscript, MuPDF, veraPDF, qpdf) and its version
- [ ] `grep -rn "SKDocument" src/Stilus` prints nothing: one PDF writer remains
- [ ] `docs/dev/decisions.md` records the printing path, PdfPig (test only), PDFsharp, ZXing.Net, and the PDF encryption choice, each with its license
- [ ] B-011 is gone from `todo/backlog.md`, and its source key `legacy-stilus-9` is carried by §2 alone
- [ ] Every disabled control on this file's surfaces names a section that `python scripts/todo-graph.py resolve` resolves (`D02 T13 §10`, `D02 T14 §9`)
- [ ] `python scripts/todo-graph.py validate` clean
