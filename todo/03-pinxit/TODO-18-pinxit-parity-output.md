---
schema_version: 1
id: pinxit-parity-output
domain: 03-pinxit
status: draft
title: "TODO-18 -- Pinxit Parity: Export, Web Output, Color Management, and Print"
depends_on: []
frozen: true
track: I18
---

# TODO-18 -- Pinxit Parity: Export, Web Output, Color Management, and Print

> **Goal:** A Pinxit user exports anything (document, selection, layers, artboards, comps, generated assets) at any size and format from one Export As dialog or Quick Export, optimizes web images in Save for Web and Affinity's Export studio with slices and continuous export, builds image maps, sets suite-wide color settings with working spaces, policies, custom CMYK, assign and convert, display color management, and OpenColorIO, soft-proofs with gamut and deficient-vision views, and prints with Pinxit-managed color, marks, functions, separations, halftones, preflight, contact sheets, and PDF presentations. The color engine is `D01 T04 §1` to `D01 T04 §3` (Pinxit's hand-rolled `ColorProfile` and `SoftProofing` classes are retired), the print dialog frame, planner, marks, separations, halftones, and preflight engine move from Stilus (`D02 T13 §2`, `D02 T13 §3`, `D02 T13 §4`, `D02 T13 §5`, `D02 T13 §9`, `D02 T13 §10`) into `src/Isotone.Core/Print/`, `src/Isotone.Core/Preflight/`, and `src/Isotone.UI/Print/`, and the export queue, web encoder, slice model, and image map writer move from Stilus (`D02 T14 §15`, `D02 T14 §16`, `D02 T14 §17`) into `src/Isotone.Core/Export/`; Pinxit's surfaces live in `src/Pinxit/Isotone.Pinxit.Desktop/Views/Export/` and `Views/Print/`. Exporting never changes the document; color operations are undoable commands; nothing prints or converts silently.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Export is a logging stub: `src/Pinxit/src/Pinxit.UI/ViewModels/MainWindowViewModel.cs` only logs "Export dialog for" the document, over a five-format `ExportFormats` filter string in `src/Pinxit/src/Pinxit.UI/Services/IFileDialogService.cs`. Pinxit carries its own hand-rolled color classes: `src/Pinxit/src/Pinxit.Core/Colors/ColorProfile.cs` (130 lines, four built-in RGB profiles by primaries and gamma) and `src/Pinxit/src/Pinxit.Core/Colors/SoftProofing.cs` (178 lines, a matrix soft proof), which §4 and §5 retire in favor of the `D01 T04 §1` engine. No ICC engine exists anywhere in `src/` yet; `D01 T04 §1` adds lcms2. Pinxit has no printing code and no Print menu entry: no `.cs` or `.xaml` file under `src/Pinxit/src/` mentions `Print`. Backlog B-021 (print) and B-023 (color management and soft proofing) are promoted into §6 and §4; the integration that lands this file deletes both entries.
<!-- claim: count "Export dialog for" src/Pinxit/src/Pinxit.UI/ViewModels/MainWindowViewModel.cs = 1 -->
<!-- claim: count "ExportFormats = " src/Pinxit/src/Pinxit.UI/Services/IFileDialogService.cs = 1 -->
<!-- claim: lines src/Pinxit/src/Pinxit.Core/Colors/ColorProfile.cs = 130 -->
<!-- claim: count "public static ColorProfile \w+ \{ get; \}" src/Pinxit/src/Pinxit.Core/Colors/ColorProfile.cs = 4 -->
<!-- claim: lines src/Pinxit/src/Pinxit.Core/Colors/SoftProofing.cs = 178 -->
<!-- claim: count "lcms|IccProfile|ColorContext" src/**/*.cs = 0 -->
<!-- claim: count "Print" src/Pinxit/src/**/*.cs = 0 -->
<!-- claim: count "Print" src/Pinxit/src/**/*.xaml = 0 -->

## Inputs

- [`standards/pinxit.md`](../../standards/pinxit.md) -- color never changes profile silently; the GPU path keeps CPU parity
- [`standards/shared.md`](../../standards/shared.md) -- atomic writes, refusals that name the target, progress and Cancel over one second, one log line per change, the shared-once rule
- [`docs/parity/pinxit-section-design.md`](../../docs/parity/pinxit-section-design.md) -- the blueprint for this file; [`docs/parity/pinxit-parity.md`](../../docs/parity/pinxit-parity.md) -- the catalog rows each section owns
- ICC.1:2022 and lcms2 2.16 (`transicc` goldens); OpenColorIO 2.5 with its built-in `ocio://` ACES configs; Machado, Oliveira, and Fernandes 2009 (color vision deficiency simulation)
- Adobe Photoshop Generator asset naming documentation; the Zoomify tile format (`ImageProperties.xml`, `TileGroup` folders); GIMP 3.2.6 Image Map plug-in (CSIM, NCSA, and CERN map formats); HTML Living Standard `<map>` and `<area>`; Apple asset catalog `Contents.json` format
- Microsoft Learn `System.Printing.PrintQueue`, `XpsDocumentWriter`, `DocumentPropertiesW`, `WcsGetDefaultColorProfile`, and Simple MAPI; MuPDF `mutool draw` and PdfPig as print-to-PDF readers
- [`todo/backlog.md`](../backlog.md) -- B-021 (`legacy-pinxit-7.4`) is promoted into §6 and B-023 (`legacy-pinxit-1.3`) into §4; both entries leave the backlog in the integration commit
- -> XREF: D01 T03 §2 -- export resamplers
- -> XREF: D01 T03 §3 -- palette quantization for PNG-8 and GIF
- -> XREF: D01 T04 §1 -- profiles and transforms §4 consumes
- -> XREF: D01 T04 §2 -- intents, proofing transforms, and gamut checks §4 and §5 consume
- -> XREF: D01 T04 §3 -- CMYK, Lab, and multichannel conversions for Convert to Profile
- -> XREF: D02 T13 §1 -- Stilus's color settings, whose dialog shell §4 moves to `Isotone.UI` and whose defaults §4 moves to the suite settings file
- -> XREF: D02 T13 §2 -- the print dialog frame §6 moves
- -> XREF: D02 T13 §3 -- print tiling §6 consumes
- -> XREF: D02 T13 §4 -- printer marks, moved by D03 T17 §7 or by §6
- -> XREF: D02 T13 §5 -- separations, halftones, and inks §7 moves
- -> XREF: D02 T13 §9 -- the preflight engine §7 moves
- -> XREF: D02 T13 §10 -- the PostScript writer for §6's PostScript printer options
- -> XREF: D02 T14 §15 -- the export queue §1 moves
- -> XREF: D02 T14 §16 -- the web encoder §2 moves
- -> XREF: D02 T14 §17 -- the slice model and image map writer §2 moves
- -> XREF: D03 T02 §2 -- the viewport display transform §10 and §5 drive
- -> XREF: D03 T02 §3 -- blend gamma in the render graph from §4's advanced settings
- -> XREF: D03 T02 §5 -- the GPU path with CPU parity for §10's display transform
- -> XREF: D03 T04 §2 -- the save paths Export As extends
- -> XREF: D03 T08 §1 -- slices, soft proof layers, and document color settings persist through the contract
- -> XREF: D03 T08 §2 -- document profile and bleed in New Document
- -> XREF: D03 T08 §4 -- guides for slices and image maps, and slices as snap candidates
- -> XREF: D03 T08 §11 -- the proof color readout §5 enables in the samplers
- -> XREF: D03 T09 §11 -- comps to files
- -> XREF: D03 T09 §13 -- artboards to files
- -> XREF: D03 T10 §10 -- spot channels for separations
- -> XREF: D03 T11 §1 -- the adjustment host for the soft proof layer
- -> XREF: D03 T11 §4 -- the OpenColorIO wrapper §10 configures
- -> XREF: D03 T11 §5 -- semi-flatten for the Web filters
- -> XREF: D03 T11 §7 -- mode conversions Convert to Profile shares
- -> XREF: D03 T15 §4 -- the 32-bit preview §10's OCIO views drive
- -> XREF: D03 T16 §1 -- captions on contact sheets and presentations
- -> XREF: D03 T17 §1 -- the format registry Export As lists
- -> XREF: D03 T17 §5 -- the web codecs exports use
- -> XREF: D03 T17 §6 -- OCIO by filename for EXR exports
- -> XREF: D03 T17 §7 -- the PDF writer and printer marks renderer exports and print use; `D03 T17 §16` owns the EPS writer §7 writes halftones and transfer functions through
- -> XREF: D03 T17 §10 -- the metadata policy exports apply
- -> XREF: D03 T17 §11 -- the CMYK writers the CMYK proof workflow exports through
- -> XREF: D03 T20 §1 -- registers §9's Export studio as a workspace preset
- -> XREF: D03 T20 §4 -- preference pages that list the `Pinxit.Color.*` and `Pinxit.Export.*` keys
- -> XREF: D03 T20 §5 -- preference pages that list the `Pinxit.Print.*` keys
- -> XREF: D04 T07 §7 -- Albumen parity import cites §6: the `Isotone.UI/Print/` print dialog frame D04 T07 §7's Copy Shop prints through
- -> XREF: D04 T12 §4 -- Albumen parity output cites §6: the print dialog frame in `Isotone.UI/Print/` that D04 T12 §4 consumes through its `IPrintPageSource` seam; §7: the contact-sheet engine D04 T12 §6 moves to `Isotone.Core/Print/ContactSheets/`, and the PDF presentation builder D04 T12 §11 reuses
- -> XREF: D03 T22 §5 -- Pinxit batch and the Image Processor cite §1: the writers batch saves use; §9: the Export studio the asset generation hook of D03 T22 §4 drives
- -> XREF: D03 T23 §5 -- Pinxit video and animation cites §2: Save for Web, which D03 T23 §5 gives animation controls

## Outcome

- One `ExportJob` model drives Export As, Quick Export, layers, artboards, and comps to files and PDF, and generated image assets, with a preview whose shown size equals the written file's size.
- Save for Web, the Export studio with continuous export, slices, and the Image Map editor produce the smallest good-looking web output and keep it current while editing.
- One suite color-settings file, read by Stilus, Pinxit, and Albumen, sets working spaces and policies; Assign and Convert to Profile, custom CMYK, display color management per view, and OpenColorIO run on the `D01 T04 §1` engine, and no second profile type exists in Pinxit.
- Soft proofing, gamut warning, deficient-vision proofs, and the soft proof adjustment layer show on screen what an output condition will produce.
- Printing uses the shared print dialog with Pinxit-managed color, marks, functions, PostScript options, tiling, separations, halftones, transfer functions, preflight, contact sheets, and PDF presentations.
- Exports and prints never change the open document.

**Adjacency:** list=applicable @ D03 T18 §1; document=applicable @ D03 T18 §6; settings=applicable @ D03 T18 §4; reporting=applicable @ D03 T18 §7; notifications=applicable @ D03 T18 §1; permissions=applicable @ D03 T18 §6; audit=applicable @ D03 T18 §4; exchange=applicable @ D03 T18 §2; reverse=applicable @ D03 T18 §4

**Adjacency rationale:** The lists are export presets (§1), the slices and export options panels (§2), preflight rules (§7), and profile lists filtered by class and space (§4). Print and its extras are this file's printed output (§6, §7). Settings are `Pinxit.Export.*`, `Pinxit.Color.*`, `Pinxit.Print.*`, and the shared suite color-settings file (§4), each with a named consumer and surfaced in `D03 T20 §4` and `D03 T20 §5`. Reporting is the estimated export sizes (§1), profile mismatch and missing-profile warnings (§4), and the preflight report (§7). Export and print progress with Cancel, continuous export status, and completion notifications are the notifications (§1, §2, §6). Read-only destinations, offline printers, missing or corrupt profiles, and absent OCIO configs are refused by name (§1, §4, §6). One Serilog Information line per export, conversion, assign, and print job is the audit trail (§1, §4, §6). Exchange is image map files (§2), color settings files, ICC profiles, and OCIO configs (§4), Xcode icon sets (§2), and PDF presentations (§7). Assign and Convert are undoable commands (§4), and exports and prints never change the document.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Export As and Quick Export | D03 T17 §5, D03 T09 §13, D03 T09 §11 |  [ ]   |
|   2   |   §8    | Layers, artboards, and comps to files and PDF, and generated image assets | §1, D03 T17 §7 |  [ ]   |
|   3   |   §2    | Save for Web, Web filters, and the Image Map editor | §1 |  [ ]   |
|   4   |   §9    | The Export studio: slices, per-slice formats, naming tokens, continuous export, and app icons | §2 |  [ ]   |
|   5   |   §3    | Slices | §2, §9 |  [ ]   |
|   6   |   §4    | Color settings, policies, custom CMYK, and assign and convert | D01 T04 §2, D03 T08 §1 |  [ ]   |
|   7   |   §10   | Display color management per view and OpenColorIO | §4, D03 T11 §4, D03 T15 §4 |  [ ]   |
|   8   |   §5    | Soft proofing and gamut warning | §4, §10 |  [ ]   |
|   9   |   §6    | Print | §4, D02 T13 §2 |  [ ]   |
|  10   |   §7    | Print output extras, contact sheets, PDF presentation, and preflight | §6, D03 T17 §7, D03 T17 §16 |  [ ]   |

---

## 1. Export As and Quick Export

Today Export only logs. Designers need to export exactly the pixels, size, format, and profile a client asks for, from the whole document, a selection, a layer, an artboard, or a comp, and re-export after edits without a dialog. This section builds one `ExportJob` model over `D03 T17 §1`'s registry and writers, runs it on the export queue Stilus built (`D02 T14 §15`, moved here into `Isotone.Core` as its second consumer), and puts Export As and Quick Export on top of it. The layer, artboard, and comp exports and Photoshop Generator-style asset generation are §8's, split from this section on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. Catalog: IP-1881 to IP-1883 and IP-1891 to IP-1899 (12 features: the Export As dialog, scale multiples with suffixes, Quick Export As, the export dialog with every format in one list and a live preview, export presets, the export area, export size and resampling, pixel format and depth and DPI, quality and matte and palettised output, the export color profile, include bleed, and the Quick Export panel).

**Fidelity:** Pinxit Export As dialog and Quick Export -- docs/design/components/ (Dialog, Panel, ListTree, Canvas, ComboBox, NumberBox, Slider, Progress, Menu), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/export-as/, docs/captures/golden/pinxit/quick-export/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Canvas/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Slider/README.md, docs/design/components/Progress/README.md, docs/design/components/Menu/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer exports exactly the pixels, size, format, and profile a client needs in one action, and re-exports after edits. Consumer: the exported files and whoever receives them.
**Treatment:** an Export As dialog with every registered format in one list, favorites, presets, scale multiples with suffixes, and a live zoomable preview of the encoded result with its real size; Quick Export as one command and an Affinity-style panel with a draggable preview. Cheaper substitute that fails the checkpoint: Save As under another name.
**Chrome:** consume the `D03 T17 §1` registry and writers, the moved export queue, the status strip, and the settings store. Do not add a second export queue.

**Requires:** display-session -- the dialog, preview, and panel captures need an interactive desktop

**Freeze check:** Every export writes through `AtomicFileWriter` to its chosen target and never to the open document's own path; the open document's pixels, path, and dirty state are unchanged by any export; a failed or cancelled export leaves any existing target byte-identical; a read-only target is refused by name before any write. Fixture source: `tests/fixtures/pinxit/export/` (created by this section).

- [ ] Move first: `BackgroundExportQueue` and the export naming logic of `D02 T14 §15` into `src/Isotone.Core/Export/` as their second consumer, with tests, repointing Stilus. Done when: `grep -rn "class BackgroundExportQueue" src` prints one path, under `src/Isotone.Core/`, and Stilus's export tests pass.
- [ ] Add `src/Pinxit/Isotone.Pinxit.Core/Export/ExportJob.cs` with its source: document, selection area, selection only, layer, artboard, or comp (IP-1893). Done when: `ExportJobTests` resolve the source bounds for each kind on a fixture.
- [ ] Add the size model (IP-1894): scale, width, height, aspect lock, and resampling nearest, bilinear, bicubic, and Lanczos 3 separable and non-separable through `D01 T03 §2`. Done when: `ExportJobTests` resolve the output size for every mode, including aspect-locked width only.
- [ ] Add pixel format, bit depth, and DPI override (IP-1895). Done when: a 16-bit export to PNG writes 16-bit and the DPI override lands in the file's pHYs chunk.
- [ ] Add quality, matte color, and palettised PNG and GIF through `D01 T03 §3` (IP-1896). Done when: a palettised PNG export has at most the chosen palette size.
- [ ] Add the export color profile (IP-1897): keep, convert to a chosen installed profile, embed, or unprofiled, listing profiles from the `D01 T04 §1` store. Done when: a convert-to-sRGB export of a Display P3 fixture matches the `transicc` conversion within 1/255 and embeds sRGB.
- [ ] Add include bleed (IP-1898) from the document bleed of `D03 T08 §2`. Done when: an export with bleed is larger by twice the bleed at the export resolution.
- [ ] Apply the `D03 T17 §10` metadata policy to every export. Done when: an export with GPS stripped has no GPS tag in exiftool 13's dump.
- [ ] Add `src/Pinxit/Isotone.Pinxit.Core/Export/ExportRunner.cs` running jobs on the moved queue off the UI thread through the registry's writers and `AtomicFileWriter`, with progress and Cancel on the status strip and a completion notification. Done when: a cancelled 100-megapixel export leaves the target absent and a completed one raises the notification.
- [ ] Add File, Export, Export As in `src/Pinxit/Isotone.Pinxit.Desktop/Views/Export/ExportAsDialog.xaml` (IP-1881, IP-1891): every registered format in one list with favorites, transparency, 8-bit PNG, quality, image and canvas size, metadata, and convert to sRGB. Done when: a driven export writes each favorite format and the capture shows the dialog. Cheaper substitute: Save As under another name.
- [ ] Add the live zoomable preview (IP-1891): re-encoded on change (debounced, cancellable) and showing the byte count of the actual encode. Done when: `ExportPreviewTests` assert the shown size equals the written file's byte count for PNG, JPEG, and WebP.
- [ ] Add scale multiples with suffixes (IP-1882), for example 1x, 2x @2x, and 3x @3x. Done when: one export writes three files with the suffixed names and the scaled sizes.
- [ ] Add export presets per format (IP-1892): built-in presets plus create, rename, and delete, stored as JSON under `%LOCALAPPDATA%\Rizonesoft\Pinxit\presets\export\`. Done when: a user preset survives a restart and a deleted one is gone.
- [ ] Add File, Export, Quick Export (IP-1883) with `Pinxit.Export.Quick.Format`, `Pinxit.Export.Quick.Quality`, and `Pinxit.Export.Quick.Location` (ask or same folder). Done when: with the location set to same folder, Quick Export writes beside the document with no dialog.
- [ ] Add a Quick Export toolbar button and an Affinity-style Quick Export panel with a draggable preview (IP-1899). Done when: a driven drag of the panel preview writes the export to the drop folder.
- [ ] Warn by name on per-format size limits (for example JPEG's 65,535 px) and refuse a read-only target folder by name. Done when: tests assert both messages.
- [ ] Log one Serilog Information line per exported file (`Exported {Source} to {Path} as {Format} {Width}x{Height} {Bytes} bytes in {ElapsedMs} ms`). Done when: a Serilog test logger asserts the line.
- [ ] Commit fixtures under `tests/fixtures/pinxit/export/` (a flat document, a selection, a 16-bit document, and a Display P3 document) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/export-as/` and `docs/captures/pinxit/quick-export/`, and write `docs/user/pinxit/export.md`. Done when: every control this section adds appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: Export As and Quick Export on one export job model"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ExportJobTests|FullyQualifiedName~ExportPreviewTests"` exits 0, resolving sizes for every mode and asserting the preview's shown size equals the written file's byte count; a driven Export As of each favorite format with scale multiples and a Quick Export beside the document are captured with the written file list quoted. Cheaper substitute that fails: Save As reuse, which ignores scale, area, and suffixes and fails those tests.

## 2. Save for Web, Web Filters, and the Image Map Editor

Web designers need the smallest good-looking files, sliced exports kept current while they edit, and clickable image maps. This section builds Photoshop's Save for Web with 2-up and 4-up optimization, lossy GIF, optimize to size, and Zoomify; the Web filters with semi-flatten; and GIMP's Image Map editor. Affinity's Export studio with per-slice formats and sizes, naming tokens, continuous export, and app icon sets is §9's, split from this section on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. The web encoder, the slice model, and the image map writer come from Stilus (`D02 T14 §16`, `D02 T14 §17`) and move into `Isotone.Core/Export/Web/` here; the slice model moves in this section rather than §3 because the slices output and §9's studio need it first. Catalog: IP-1902 to IP-1907 and IP-1915 to IP-1919 (11 features: the Image Map editor, the Save for Web dialog, GIF and PNG-8 reduction, PNG-24, JPEG, and WBMP options, slices output, Zoomify, the Web filters with semi-flatten, and the image map working area, areas, files, and grid and guides).

**Fidelity:** Pinxit Save for Web dialog and Image Map editor -- docs/design/components/ (Dialog, Tabs, Canvas, Slider, NumberBox, ComboBox, ListTree, ToolRail), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/save-for-web/, docs/captures/golden/pinxit/image-map/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Tabs/README.md, docs/design/components/Canvas/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/ListTree/README.md, docs/design/components/ToolRail/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a web designer ships the smallest good-looking files and builds clickable image maps. Consumer: browsers and the site the files are published to.
**Treatment:** a Save for Web dialog (original, optimized, 2-up, 4-up, presets, color table, size, preview in browser) and an Image Map editor window (areas list, source and gray views, grid and guides). Cheaper substitute that fails the checkpoint: a quality slider on JPEG export.
**Chrome:** consume §1's job model, the moved web encoder, slice model, and image map writer, and the `D03 T08 §4` guides. Do not add a second palette quantizer.

**Requires:** display-session -- the dialogs, the studio, and the editor need an interactive desktop

**Freeze check:** Save for Web, slices output, Zoomify, and image map saves write through `AtomicFileWriter` and never to the open document's own path; a failed or cancelled write leaves any existing target byte-identical; the open document is never changed by any of them except the slice edits the user makes, which are undoable. Fixture source: `tests/fixtures/pinxit/web/` (created by this section).

- [ ] Move first: the encoder half of `D02 T14 §16` (`WebEncoderSettings`, size estimates, presets) into `src/Isotone.Core/Export/Web/`, repointing Stilus. Done when: one `WebEncoderSettings` definition remains and Stilus's web export tests pass.
- [ ] Move the HTML `<map>` writer of `D02 T14 §17` into `src/Isotone.Core/Export/Web/ImageMap/`, repointing Stilus. Done when: one image map writer definition remains.
- [ ] Move the `Slice` model of `D02 T14 §17` (`src/Stilus/Isotone.Stilus.Core/Web/`) into `src/Isotone.Core/Export/Web/Slice.cs`, repointing Stilus, and persist Pinxit slices as `pinxit:slices` through the `D03 T08 §1` contract. Done when: `grep -rn "class Slice\b" src` prints one path, under `src/Isotone.Core/`, and a slice set round-trips `.pinxit`.
- [ ] Add File, Export, Save for Web in `src/Pinxit/Isotone.Pinxit.Desktop/Views/Export/SaveForWebDialog.xaml` (IP-1903): original, optimized, 2-up, and 4-up views with presets. Done when: the capture shows 4-up with four settings and their sizes. Cheaper substitute: a JPEG quality slider.
- [ ] Add optimize to size (IP-1903): a search over quality or color count that lands within 5 percent under a target size. Done when: `WebEncoderTests.OptimizeToSize` lands within 5 percent under three targets.
- [ ] Add image size, metadata, and sRGB conversion options, and preview in the default browser from a temporary page. Done when: preview writes a temporary HTML page that references the optimized image and opens the browser.
- [ ] Add GIF and PNG-8 reduction (IP-1904): perceptual, selective, adaptive, and restrictive through `D01 T03 §3`. Done when: `WebEncoderTests` assert the palette size and transparency index for each method.
- [ ] Add lossy LZW for GIF (implemented from its published description) and dither types and amount. Done when: size falls monotonically as lossy rises on a committed fixture.
- [ ] Add the color table with lock, add, delete, and web snap (IP-1904). Done when: a locked color survives a further reduction.
- [ ] Add PNG-24, JPEG, and WBMP options (IP-1905). Done when: size rises monotonically with JPEG quality on a committed fixture.
- [ ] Add slices output (IP-1906): one image per slice plus an HTML table or CSS layout with output settings. Done when: the written HTML parses and references one image per slice.
- [ ] Add Zoomify export (IP-1907): a 256 px JPEG pyramid in `TileGroupN` folders with `ImageProperties.xml` and an own HTML template. Done when: `ZoomifyTests` check tile counts per level and the XML attributes against the format.
- [ ] Add the Web filters menu with Semi-flatten (IP-1915) through `D03 T11 §5`. Done when: semi-flatten against a color leaves no partially transparent pixel.
- [ ] Add the Image Map editor window `src/Pinxit/Isotone.Pinxit.Desktop/Views/Export/ImageMapWindow.xaml` (IP-1902, IP-1916): the working area, an area list, and source and gray views. Done when: a driven run switches views and the capture shows both.
- [ ] Add image map areas (IP-1917): rectangle, circle, and polygon, with area info (URL, alt, target, and event attributes written, never executed) and reorder. Done when: a test asserts event attributes are written verbatim and no script is evaluated.
- [ ] Add image map files (IP-1918): open, recent, save, save as, and map info in CSIM, NCSA, and CERN formats through the moved writer. Done when: `ImageMapTests` round-trip all three formats and parse the HTML.
- [ ] Add the image map grid and guides (IP-1919): grid settings, use guides from `D03 T08 §4`, and create guide areas. Done when: create guide areas produces one area per guide cell.
- [ ] Log one Serilog Information line per Save for Web, Zoomify export, and image map save. Done when: a Serilog test logger asserts each line.
- [ ] Commit fixtures under `tests/fixtures/pinxit/web/` with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/save-for-web/` and `image-map/`, and write `docs/user/pinxit/web-output.md`. Done when: every window this section adds appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: Save for Web, the Web filters, and the Image Map editor"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~WebEncoderTests|FullyQualifiedName~ZoomifyTests|FullyQualifiedName~ImageMapTests"` exits 0, asserting palette size, transparency index, and monotonic size with quality, optimize-to-size within 5 percent under target, Zoomify tile counts and XML, and all three map formats round-tripping; captures committed. Cheaper substitute that fails: a JPEG quality slider, which the optimize-to-size and palette tests catch.

## 3. Slices

Web designers cut a comp into named, linked images. This section adds Photoshop's slice and slice select tools, auto slices around user slices, slices from guides, divide, options, layer-based slices, and slice display on the `Slice` model §2 moved into `Isotone.Core`, and it enables the Export studio's Draw Slice button. Catalog: IP-1920 to IP-1928 (9 features: slice display, snapping, lock, and clear, new layer-based slice, the slice tool, slices from guides, the slice select tool, user and auto slices, divide slice, slice options, and layer-based slices with revert to auto size).

**Fidelity:** Pinxit slice tools and slice options -- docs/design/components/ (ToolRail, OptionsBar, Canvas, Dialog, TextBox, ComboBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/slices/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/ToolRail/README.md, docs/design/components/OptionsBar/README.md, docs/design/components/Canvas/README.md, docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a web designer cuts a comp into named, linked images. Consumer: §2's slices output, and §9's Export studio and continuous export.
**Treatment:** the slice tool with styles, the slice select tool with order, align, and distribute, a Slice Options dialog, a Divide Slice dialog, and numbered slice overlays. Cheaper substitute that fails the checkpoint: exporting rectangles typed by hand.
**Chrome:** consume the moved `Slice` model, the `D03 T08 §4` guides and snapping, and the suite history. Do not add a second slice model.

**Requires:** display-session -- the slice tools need an interactive desktop

- [ ] Add `src/Pinxit/Isotone.Pinxit.Core/Web/SliceSet.cs` over §2's `Slice` model: user, auto, and layer-based slices with stacking order. Done when: `SliceTests` add, remove, and reorder slices.
- [ ] Add auto-slice generation around user slices so the canvas is always fully covered (IP-1925). Done when: `SliceTests.AutoCover` asserts full coverage with no overlap for five user-slice layouts.
- [ ] Add the Slice tool in `src/Pinxit/Isotone.Pinxit.Desktop/Tools/Web/SliceTool.cs` (IP-1922): normal, fixed aspect ratio, and fixed size styles, Shift for a square, and Alt from the center. Done when: a scripted fixed-size drag creates a slice of that size.
- [ ] Add Slices from Guides (IP-1923). Done when: two vertical and one horizontal guide produce six slices.
- [ ] Add the Slice Select tool (IP-1924): stacking order, align, and distribute. Done when: aligning three slices' tops sets equal y.
- [ ] Add promote to user slice and hide auto slices (IP-1925). Done when: a promoted auto slice keeps its bounds and becomes editable.
- [ ] Add Divide Slice (IP-1926) horizontally or vertically into N parts or by pixels. Done when: dividing a 300 px slice into three yields three 100 px slices.
- [ ] Add the Slice Options dialog (IP-1927): name, URL, target, message, alt, dimensions, and background type and color. Done when: every field round-trips `.pinxit`.
- [ ] Add layer-based slices (IP-1921, IP-1928) following layer or group bounds, with revert to auto size. Done when: `SliceTests.LayerBased` move the layer and the slice follows.
- [ ] Add numbered slice overlays, snapping, lock, and clear (IP-1920) under `Pinxit.Slices.ShowNumbers`, `Pinxit.Slices.LineColor`, and `Pinxit.Slices.Snap`. Done when: toggling each setting redraws without a restart.
- [ ] Enable the Export studio's Draw Slice button from §9 with this tool, and register slice edges as `D03 T08 §4` snap candidates. Done when: the button activates the Slice tool in a driven run and a crop edge snaps to a slice edge.
- [ ] Make every slice edit one undoable command with one Serilog Information line. Done when: a Serilog test logger asserts the line and undo reverses a divide.
- [ ] Commit captures under `docs/captures/pinxit/slices/` and extend `docs/user/pinxit/web-output.md` with slices. Done when: both tools and both dialogs appear in captures and the page documents them.
- [ ] Commit: `"pinxit: slices and the slice tools"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~SliceTests"` exits 0 covering auto-slice generation around user slices, divide, layer-based bounds following a moved layer, and a `.pinxit` round trip of every field; a driven capture of both tools is committed under `docs/captures/pinxit/slices/`. Cheaper substitute that fails: user slices only, which the auto-slice coverage test catches.

## 4. Color Settings, Policies, Custom CMYK, and Assign and Convert

Pinxit's color is hand-rolled today: four RGB profiles by primaries and gamma and a matrix soft proof, with no ICC engine. This section retires those classes and puts every color decision on the suite engine of `D01 T04 §1` to `D01 T04 §3`: one color-settings file read by Stilus, Pinxit, and Albumen, working spaces and policies, conversion options, custom CMYK, Assign and Convert to Profile, and document profiles and indicators. Display color management per view and OpenColorIO are §10's, split from this section on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. Stilus's Color Settings dialog (`D02 T13 §1`) moves into `Isotone.UI` as the shared shell so no second dialog exists. This promotes backlog B-023. Catalog: IP-1931 to IP-1933, IP-1936 to IP-1949, and IP-1953 (18 features: keeping any RGB working space, intent and BPC, converting opened and placed images, opened-file profile handling, save color options, the Color Settings dialog, suite-shared settings, working spaces, policies and warnings, conversion options, advanced options, custom CMYK, assign, convert, the document profile, profile indicators, the Color Management submenu, and color settings preferences). -> SOURCE: legacy-pinxit-1.3

**Fidelity:** Pinxit Color Settings and Assign and Convert Profile dialogs -- docs/design/components/ (Dialog, ComboBox, Checkbox, RadioButton, ListTree, StatusBar), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/color-settings/, docs/captures/golden/pinxit/convert-profile/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/ListTree/README.md, docs/design/components/StatusBar/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer or prepress user keeps color correct from open to file across the suite. Consumer: every conversion, export, and print in Pinxit, §10's display transform, and Stilus and Albumen through the shared settings file.
**Treatment:** a Color Settings dialog (presets, working spaces, policies, conversion options, advanced, custom CMYK) with save and load, Assign Profile and Convert to Profile dialogs, an Image, Color Management submenu, and profile indicators in the status bar and title. Cheaper substitute that fails the checkpoint: sRGB assumed everywhere.
**Chrome:** consume the `D01 T04 §1` engine, `D03 T02 §3` for blend gamma, the moved dialog shell in `Isotone.UI`, and the suite history. Do not keep a second profile type.

**Requires:** display-session -- the dialogs and captures need an interactive desktop

- [ ] Retire first: delete `src/Pinxit/Isotone.Pinxit.Core/Colors/ColorProfile.cs` and `SoftProofing.cs` and route every caller to the `D01 T04 §1` and `D01 T04 §2` types (`IccProfile`, `ColorTransformService`, `ProofTransform`). Done when: `grep -rn "class ColorProfile\|class SoftProofing" src/Pinxit` prints nothing and Pinxit's tests pass.
- [ ] Add `src/Isotone.Core/Color/Settings/ColorSettings.cs` (IP-1939): one file `%LOCALAPPDATA%\Rizonesoft\Isotone\Color\color-settings.json` read by Stilus, Pinxit, and Albumen, written through `AtomicFileWriter`, and repoint Stilus's `D02 T13 §1` defaults and policies to it. Done when: a change saved from Pinxit is read by a Stilus `ColorSettings` instance in a test, and Stilus's color tests pass.
- [ ] Move the Color Settings dialog shell of `D02 T13 §1` into `src/Isotone.UI/Color/ColorSettingsDialog.xaml` with an app adapter, repointing Stilus. Done when: one dialog definition remains and both apps open it.
- [ ] Add the presets General Purpose, Prepress Europe FOGRA39, and Web sRGB, and save and load of `.isotonecolor` files (IP-1938); an unreadable settings file is refused by name. Done when: a saved `.isotonecolor` reloads equal and a corrupt one is refused naming the file.
- [ ] Add working spaces (IP-1940, IP-1953): RGB, CMYK, gray, spot dot gain, 32-bit linear RGB, and Lab defaults, plus default intent and BPC. Done when: a new document takes the working RGB profile.
- [ ] Keep any RGB working space end to end (IP-1931): documents in ProPhoto, Display P3, or a user profile render, save, and export with it and never pass through sRGB. Done when: a ProPhoto fixture saved and reopened keeps its profile bytes and values exactly.
- [ ] Add color management policies (IP-1941): off, preserve embedded, or convert to working, per RGB, CMYK, and gray, with mismatch and missing-profile prompts on open and paste (IP-1936). Done when: opening the mismatched fixture shows the prompt and each choice applies as named.
- [ ] Convert placed images to the working space per the policy (IP-1933). Done when: placing a Display P3 image into an sRGB document converts it within 1/255 of `transicc`.
- [ ] Add the conversion options (IP-1932, IP-1942): lcms2 as the one engine, intent, black point compensation, dither for 8-bit, and scene-referred compensation for 32-bit. Done when: Convert to Profile matches `transicc` goldens within Delta E 2000 0.5 for every intent with and without BPC.
- [ ] Add the advanced options (IP-1943): desaturate monitor colors, and RGB and text blend gamma consumed by the render graph of `D03 T02 §3`. Done when: a blend-gamma test composites two layers and matches its golden at gamma 1.0 and 2.2.
- [ ] Add `src/Isotone.Core/Color/Settings/CmykProfileBuilder.cs` (IP-1944) over lcms2's pipeline API (`cmsPipelineAlloc`, `cmsStageAllocCLut16bit`, `cmsSaveProfileToMem`) from inks, dot gain, GCR or UCR, black generation, black and total ink limits, and UCA through a Yule-Nielsen-modified Neugebauer model, writing an ICC v4 output profile. Done when: `CmykProfileBuilderTests` prove the total ink limit holds on a gamut sweep and neutrals go K-only under maximum GCR.
- [ ] Add the Custom CMYK dialog over the builder. Done when: a driven run builds a profile, it appears in the working CMYK list, and the capture shows the dialog.
- [ ] Add Image, Assign Profile (IP-1945) as one undoable command that keeps pixel values, with GIMP's Assign sRGB and Discard Color Profile. Done when: a test asserts pixel values are unchanged and undo restores the previous profile.
- [ ] Add Image, Convert to Profile (IP-1946) with engine, intent, BPC, dither, flatten, and advanced multichannel through `D01 T04 §3`, as one undoable command. Done when: a converted fixture matches `transicc` within Delta E 2000 0.5 and undo restores the original values exactly.
- [ ] Add the document profile to New Document and Document Setup (IP-1947) through `D03 T08 §2`. Done when: a new document created with Adobe RGB saves that profile.
- [ ] Add the profile indicator in the status bar and title (IP-1948). Done when: the capture shows the profile name and an untagged document shows "Untagged".
- [ ] Add the Image, Color Management submenu with Save Profile to File (IP-1949). Done when: the saved profile's bytes equal the document's.
- [ ] Add the save color options embed ICC profile and use proof setup (IP-1937). Done when: a PNG saved with embed off carries no iCCP chunk.
- [ ] Log one Serilog Information line per assign, convert, and color-settings change (from, to, intent, BPC) as the audit trail beside the history entry. Done when: a Serilog test logger asserts the lines.
- [ ] Commit fixtures under `tests/fixtures/pinxit/color/` (mismatched, untagged, ProPhoto, Display P3) with `transicc` goldens and `reference.txt` naming lcms2 2.16. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/color-settings/` and `convert-profile/`, and write `docs/user/pinxit/color-management.md`. Done when: every dialog this section adds appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: color settings, policies, custom CMYK, and assign and convert"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~Color"` exits 0 with Convert to Profile matching `transicc` goldens within Delta E 2000 0.5 for every intent with and without BPC, `CmykProfileBuilderTests` holding the total ink limit and K-only neutrals, and a ProPhoto fixture keeping its profile bytes and values through save and reopen; captures committed under `docs/captures/pinxit/color-settings/`. Cheaper substitute that fails: keeping `ColorProfile.cs` matrix math, which the CMYK goldens and the single-profile-type grep reject.

## 5. Soft Proofing and Gamut Warning

A user needs to see on screen how a print condition or a color-blind viewer will see the image before committing to output. This section adds proof setups and presets, Proof Colors per view, gamut warning with color and opacity, deficient-vision proofs by Machado et al. 2009, Affinity's soft proof adjustment layer, GIMP's new-image proofing and CMYK proof workflow, and the proof status pop-over, all on the `D01 T04 §2` proofing transform and gamut mask. Catalog: IP-1955 to IP-1968 (14 features: the soft proof adjustment layer, proof setup and proof colors, gamut warning, deficient-vision proofing, new-image proofing, the CMYK proof then export workflow, custom proof conditions, proof presets, color blindness proofs as Affinity's row, the proof colors toggle, gamut warning color and opacity, soft-proof settings with the status pop-over, several coexisting proof layers, and soft-proof preferences).

**Fidelity:** Pinxit soft proofing and gamut warning -- docs/design/components/ (Dialog, Menu, Canvas, ComboBox, Checkbox, ToggleSwitch, StatusBar), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/soft-proof/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Menu/README.md, docs/design/components/Canvas/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ToggleSwitch/README.md, docs/design/components/StatusBar/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user sees on screen how a print condition or a color-blind viewer will see the image. Consumer: the viewport and, when chosen, the CMYK export.
**Treatment:** View, Proof Setup and Proof Colors, Gamut Warning, a Customize Proof Condition dialog, a soft proof adjustment layer, and a status-bar pop-over. Cheaper substitute that fails the checkpoint: a matrix tint that ignores the output profile.
**Chrome:** consume the `D01 T04 §2` `ProofTransform` and `GamutMask`, the `D03 T11 §1` adjustment host, and the viewport. Do not add a second proof pipeline.

**Requires:** display-session -- proofing on a live view needs an interactive desktop

- [ ] Add `src/Pinxit/Isotone.Pinxit.Core/Color/ProofSetup.cs` (IP-1956, IP-1966): profile, intent, BPC, simulate paper color, simulate black ink, and preserve numbers, with save and load of `.isotoneproof` files. Done when: a saved setup reloads equal.
- [ ] Add the Customize Proof Condition dialog (IP-1961) over `ProofSetup`. Done when: a driven run saves a custom condition and the capture shows the dialog.
- [ ] Add proof presets (IP-1962): working CMYK, individual plates, and RGB conditions. Done when: the Working Cyan Plate preset shows only the cyan plate's density in the proof.
- [ ] Add View, Proof Colors per view (IP-1964) through `ProofTransform` in the viewport pipeline, with the per-view proof state shown in the title and the proof color readout of `D03 T08 §11`'s samplers enabled. Done when: the samplers show proof values while Proof Colors is on, and proofed renders match `transicc` proof goldens within Delta E 2000 0.5 and two views of one document proof independently.
- [ ] Add Gamut Warning (IP-1957, IP-1965) as a `GamutMask` overlay with `Pinxit.Color.GamutWarningColor` and opacity. Done when: the gamut mask of a committed fixture matches `D01 T04 §2`'s bulk mask exactly.
- [ ] Add deficient-vision proofs (IP-1958, IP-1963): protanopia, deuteranopia, and tritanopia by the Machado et al. 2009 matrices at severity 1.0 in linear RGB. Done when: the matrices reproduce the published table and a test applies each to a fixture.
- [ ] Add the soft proof adjustment layer (IP-1955, IP-1967): a new adjustment kind on the `D03 T11 §1` host with profile, intent, BPC, and gamut check, several allowed at once, and hidden from export by default (`Pinxit.Color.ExportSoftProofLayers`, default false). Done when: an export with a soft proof layer present matches the export without it exactly.
- [ ] Add new-image proofing (IP-1959): a proof profile, intent, and BPC chosen in New Document. Done when: a new document opens with Proof Colors on under that setup.
- [ ] Add the CMYK proof then CMYK export workflow (IP-1960) through the `D03 T17 §11` CMYK writers. Done when: exporting after proofing to a CMYK profile writes a CMYK TIFF whose values match the proof transform's device values within 1/255.
- [ ] Add the status-bar proof pop-over (IP-1966) showing and changing the active setup. Done when: a driven run changes the intent from the pop-over and the view re-proofs.
- [ ] Add the soft-proof preferences (IP-1968): optimize soft proofing and mark out-of-gamut colors, each with a default and the viewport as consumer. Done when: toggling each changes the proof render without a restart.
- [ ] Log one Serilog Information line per proof setup change (profile, intent, BPC). Done when: a Serilog test logger asserts the line.
- [ ] Commit fixtures under `tests/fixtures/pinxit/proof/` with `transicc` proof goldens and `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/soft-proof/` (each proof view, the gamut warning, the dialog, the pop-over) and extend `docs/user/pinxit/color-management.md` with proofing. Done when: every control appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: soft proofing, gamut warning, and deficient-vision proofs"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~Proof"` exits 0 with proofed renders matching `transicc` proof goldens within Delta E 2000 0.5, the gamut mask of the committed fixture equal to `D01 T04 §2`'s bulk mask, and the deficient-vision matrices reproducing the published table; a driven capture of each view is committed. Cheaper substitute that fails: a tint overlay, which the proof goldens reject.

## 6. Print

Photographers print, and Pinxit cannot print at all today. This section builds File, Print on the print dialog frame, planner, backend, and preview Stilus built (`D02 T13 §2`, with tiling from `D02 T13 §3`), moved into `Isotone.Core/Print/` and `Isotone.UI/Print/` behind an `IPrintPageSource` seam (Stilus supplies vector visuals, Pinxit supplies the composited image at print resolution), and adds Pinxit's pages: Pinxit-managed color and hard proofing, position and size, selected-area printing, marks, functions, PostScript options, tiled and N-up layouts, and a paper mismatch warning. Separations arrive with §7. This promotes backlog B-021. Catalog: IP-1969 to IP-1981 (13 features: the print dialog, Print One Copy, printer and driver settings, the preview with match print colors, color handling, hard proofing, position and size, print selected area, printing marks, print functions, PostScript options, tiled and N-up layouts, and the paper size mismatch warning). -> SOURCE: legacy-pinxit-7.4

**Fidelity:** Pinxit Print dialog and print preview -- docs/design/components/ (Dialog, Canvas, ComboBox, NumberBox, Checkbox, Progress), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/print-dialog/, docs/captures/golden/pinxit/print-preview/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Canvas/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer prints at the right size with correct color and marks. Consumer: the Windows spooler and Microsoft Print to PDF.
**Treatment:** the shared category-paged print dialog with Pinxit pages (Color Management, Position and Size, Printing Marks, Functions, PostScript Options) and a live preview with match print colors, gamut warning, and paper white. Cheaper substitute that fails the checkpoint: `PrintVisual` of the canvas at screen resolution.
**Chrome:** consume the moved frame in `src/Isotone.UI/Print/`, the `D01 T04 §1` engine, §5's proofing, and the status strip. Do not build a second print dialog.

**Requires:** display-session -- printing to Microsoft Print to PDF and the captures need an interactive desktop

- [ ] Move first: `PrintJobSettings`, `PrintPlanner`, `IPrintBackend` with its XPS implementation, printer listing, and the driver sheet through `DocumentPropertiesW` from `D02 T13 §2` into `src/Isotone.Core/Print/` behind an `IPrintPageSource` seam, with the moved `PrintPlannerTests`, repointing Stilus. Done when: `grep -rn "class PrintPlanner" src` prints one path, under `src/Isotone.Core/`, and the moved `PrintPlannerTests` still pass.
- [ ] Move the print dialog shell and mini preview of `D02 T13 §2` into `src/Isotone.UI/Print/`, with category pages each app contributes, repointing Stilus. Done when: one dialog definition remains and Stilus's driven print still passes.
- [ ] Move `PrinterMarksRenderer` into `src/Isotone.Core/Print/` if `D03 T17 §7` has not already moved it. Done when: `grep -rn "class PrinterMarksRenderer" src` prints one path, under `src/Isotone.Core/`.
- [ ] Add `src/Pinxit/Isotone.Pinxit.Desktop/Print/PinxitPrintPageSource.cs` supplying the composited image at the print resolution, never the screen raster. Done when: a test at 300 ppi on a 4 by 6 inch print asserts a 1200 by 1800 px image.
- [ ] Add File, Print (IP-1969, IP-1971): printer, driver settings, copies, orientation, a description from the `D03 T17 §10` metadata, and settings remembered under `Pinxit.Print.*`. Done when: a driven print remembers the printer and copies on the next open. Cheaper substitute: `PrintVisual` of the canvas.
- [ ] Add File, Print One Copy (IP-1970) with the remembered settings and no dialog. Done when: a driven Print One Copy spools one page to Microsoft Print to PDF.
- [ ] Add the preview (IP-1972) with match print colors, gamut warning, and paper white through §5's proofing. Done when: the capture shows the preview with each option on.
- [ ] Add color handling (IP-1973): printer manages, Pinxit manages (an lcms2 transform to the printer profile with intent and BPC), or separations, which is disabled with a tooltip naming `D03 T18 §7` until that section enables it. Done when: with Pinxit managing color, the printed image equals the `transicc` conversion to the fixture printer profile within 1/255.
- [ ] Add hard proofing (IP-1974) with a proof setup and simulate paper color and black ink. Done when: a hard-proof print's pixels match the proof transform's output within 1/255.
- [ ] Add position and size (IP-1975): center, top and left, scale to fit, scale percent, print resolution, and units. Done when: `PinxitPrintLayoutTests` place a fixture at each setting and assert its rectangle on the page.
- [ ] Add Print Selected Area (IP-1976). Done when: printing with a selection prints only its bounds' pixels.
- [ ] Add printing marks (IP-1977): corner and center crop marks, registration, description, and labels through `PrinterMarksRenderer`. Done when: PdfPig reads the marks from the printed PDF as vector paths.
- [ ] Add print functions (IP-1978): emulsion down, negative, background, border, and bleed. Done when: negative inverts the printed image's channels, asserted on the PDF image.
- [ ] Add PostScript options (IP-1979): calibration bars, interpolation, and include vector data (text and shape layers as vectors) through the moved `PostScriptWriter`, shown only for PostScript printers. Done when: the page is hidden for Microsoft Print to PDF and shown for a PostScript test queue.
- [ ] Add tiled and N-up layouts (IP-1980) through the `D02 T13 §3` tiling in the moved planner. Done when: a poster fixture tiles onto the expected sheet count.
- [ ] Add the paper size mismatch warning (IP-1981). Done when: printing a landscape image to portrait paper without auto-rotate shows the warning.
- [ ] Run the job off the UI thread with progress and Cancel and a completion notification; refuse an offline printer, or one whose queue permissions deny the user, by name; log one Serilog Information line per job. Done when: a test backend in error state yields the refusal and a Serilog test logger asserts the job line.
- [ ] Commit fixtures under `tests/fixtures/pinxit/print/` (the image fixture and the fixture printer profile) with `reference.txt` naming lcms2 2.16 `transicc` and PdfPig. Done when: both carry their notes.
- [ ] Commit captures under `docs/captures/pinxit/print-dialog/` and `docs/captures/pinxit/print-preview/`, and write `docs/user/pinxit/print.md`. Done when: every page appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: print with Pinxit-managed color and marks on the shared print dialog"`

**Test checkpoint:** Driven run with evidence and unit test: a driven print of the committed fixture to Microsoft Print to PDF is read with PdfPig, which asserts one page, an image at the requested resolution (pixel size quoted), and marks as vector paths; with Pinxit managing color, the printed image equals the `transicc` conversion to the fixture printer profile within 1/255; `dotnet test Isotone.slnx --filter "FullyQualifiedName~PrintPlannerTests|FullyQualifiedName~PinxitPrintLayoutTests"` exits 0 with the moved Stilus tests passing. Cheaper substitute that fails: `PrintVisual` of the canvas, which the resolution assertion catches.

## 7. Print Output Extras, Contact Sheets, PDF Presentation, and Preflight

Prepress users send correct separations and check a file before it leaves, and photographers build contact sheets and presentations. This section adds spot and overprint global colors, transfer functions, halftone screens, separations with spot plates, a preflight panel with custom rules, PDF Presentation, and Contact Sheet, on the separation, halftone, ink, and preflight engines Stilus built (`D02 T13 §5`, `D02 T13 §9`), moved into `Isotone.Core` here, and on the `D03 T17 §7` PDF and EPS writers. Catalog: IP-1982 to IP-1988 (7 features: spot and overprint global colors, transfer functions, halftone screens per ink, separations with spot plates, the preflight panel with custom rules, PDF Presentation, and Contact Sheet).

**Corrected 2026-09-27:** Albumen's contact sheets (`D04 T12 §6`) move this section's contact-sheet builder, layout, and caption model to `src/Isotone.Core/Print/ContactSheets/`, and Albumen's PDF creation (`D04 T12 §11`) moves the PDF presentation builder to `src/Isotone.Core/Pdf/Presentation/` if it is still in Pinxit; Pinxit repoints.

**Fidelity:** Pinxit print output extras, contact sheet, PDF presentation, and preflight -- docs/design/components/ (Dialog, Panel, ListTree, ComboBox, NumberBox, Checkbox, Progress), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/separations/, docs/captures/golden/pinxit/preflight/, docs/captures/golden/pinxit/contact-sheet/, docs/captures/golden/pinxit/pdf-presentation/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/ComboBox/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a prepress user sends correct separations and checks a file before it leaves; a photographer builds contact sheets and presentations. Consumer: the printer or plate files, the preflight report, and the generated PDF and sheets.
**Treatment:** print pages for transfer, screens, and separations, a Preflight panel with a rule editor, and File, Automate style dialogs for Contact Sheet and PDF Presentation. Cheaper substitute that fails the checkpoint: printing the composite for every plate.
**Chrome:** consume the moved engines, the `D03 T17 §7` PDF writer, the `D03 T16 §1` text for captions, and the status strip. Do not render plates a second way.

**Requires:** display-session -- the dialogs, panel, and captures need an interactive desktop

**Freeze check:** Separation files, PDF Presentations, and contact sheets write through `AtomicFileWriter` to their chosen targets and never to an open document's path; the source images of a contact sheet or presentation are opened read-only and never written; a failed or cancelled run leaves any existing target byte-identical. Fixture source: `tests/fixtures/pinxit/prepress/` (created by this section).

- [ ] Move first: `SeparationRenderer`, `HalftoneScreen`, and `InkSet` of `D02 T13 §5` into `src/Isotone.Core/Print/`, and `PreflightEngine` of `D02 T13 §9` into `src/Isotone.Core/Preflight/`, with tests, repointing Stilus. Done when: `grep -rn "class SeparationRenderer\|class PreflightEngine" src` prints one path each, under `src/Isotone.Core/`.
- [ ] Add spot and overprint global colors (IP-1982): Affinity-style global colors flagged spot or overprint, feeding `D03 T10 §10` spot channels and the separations. Done when: a global color flagged spot creates a spot channel with its name.
- [ ] Add transfer functions (IP-1983): per-ink curves stored with the document and written to PostScript and PDF (`/TR`) through the `D03 T17 §16` and `D03 T17 §7` writers. Done when: PdfPig reads the `/TR` function of each ink from a written PDF.
- [ ] Add halftone screens per ink (IP-1984): frequency, angle, and shape, written to EPS and PDF through `D03 T17 §16` and `D03 T17 §7`. Done when: a written PDF's halftone dictionary carries each ink's frequency and angle.
- [ ] Add separations (IP-1985): one plate per process ink and spot channel, printed or saved to files, and enable §6's separations color handling. Done when: plates of the committed CMYK plus spot fixture equal the channel values within 1/255.
- [ ] Add the print pages for transfer, screens, and separations to the §6 dialog. Done when: the capture shows each page.
- [ ] Add the Pinxit preflight rules (IP-1986): effective resolution below a threshold, RGB content in CMYK output, out-of-gamut percentage, missing linked smart objects, missing fonts, spot channel count, and total ink over the limit. Done when: `PreflightRuleTests` fire each rule on its fixture and stay silent on a clean one.
- [ ] Add custom preflight rules as JSON profiles and a live Preflight panel with a rule editor (IP-1986). Done when: a custom rule saved in the editor fires on its fixture after a restart.
- [ ] Add File, Automate, PDF Presentation (IP-1987): open documents or files into a multi-page PDF with captions, background, and slideshow options (`/Trans`, `/Dur`, full screen) through the moved writer. Done when: a presentation reads back with PdfPig showing the page count and the `/Trans` entries.
- [ ] Add File, Automate, Contact Sheet (IP-1988): from a folder with columns, rows, sheet size and resolution, spacing, captions (file name) in `D03 T16 §1` text, flattened or layered, as a long operation with progress and Cancel. Done when: a contact sheet of a committed folder matches its golden layout.
- [ ] Log one Serilog Information line per separation job, preflight run, and generated sheet or presentation. Done when: a Serilog test logger asserts each line.
- [ ] Commit fixtures under `tests/fixtures/pinxit/prepress/` (CMYK plus spot, preflight rule fixtures, a contact-sheet folder with its golden) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/separations/`, `preflight/`, `contact-sheet/`, and `pdf-presentation/`, and write `docs/user/pinxit/prepress.md`. Done when: every dialog and panel appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: separations, halftones, preflight, contact sheets, and PDF presentations"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~Separation|FullyQualifiedName~PreflightRuleTests|FullyQualifiedName~ContactSheet|FullyQualifiedName~PdfPresentation"` exits 0 with plates of the committed CMYK plus spot fixture equal to the channel values within 1/255, each preflight rule firing on its fixture, a PDF Presentation reading back with PdfPig showing the page count and `/Trans` entries, and a contact sheet of the committed folder matching its golden layout. Cheaper substitute that fails: composite-per-plate printing, which the plate value test catches.

## 8. Layers, Artboards, and Comps to Files and PDF, and Generated Image Assets

Designers export every layer, artboard, or comp as its own file or PDF page in one action, and web teams keep image assets regenerated from layer names while they edit. This section adds those batch exports and Photoshop Generator-style asset generation on §1's `ExportJob`, `ExportRunner`, and presets, never a second export queue. Split from §1 on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. Catalog: IP-1884 to IP-1890, IP-1900, and IP-1901 (9 features: layers to files, artboards to files and PDF, comps to files and PDF, generated image assets, quick export for layers, comps to files as GIMP's row, artboards to files and PDF as Affinity's row, comps to files as Affinity's row, and layers to files with their options).

**Fidelity:** Pinxit export of layers, artboards, and comps and generated image assets -- docs/design/components/ (Dialog, Panel, LayersRow, ContextMenu, Menu, ComboBox, ToggleSwitch), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/export-as/, docs/captures/golden/pinxit/batch-export/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/LayersRow/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Menu/README.md, docs/design/components/ComboBox/README.md, docs/design/components/ToggleSwitch/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a designer exports every layer, artboard, or comp in one action and keeps generated assets current as they edit. Consumer: the exported files, PDF pages, and asset folders, and whoever receives them.
**Treatment:** Export Layers to Files, Artboards to Files and PDF, and Comps to Files and PDF dialogs with a target folder, prefix, and per-format options; Layers panel context-menu exports; File, Generate, Image Assets as a toggle. Cheaper substitute that fails the checkpoint: exporting each layer by hand through Export As, which the file-count tests catch.
**Chrome:** consume §1's `ExportJob`, `ExportRunner`, and presets, the moved export queue, the `D03 T17 §7` PDF writer, and the `D03 T09 §13` artboards and `D03 T09 §11` comps. Do not add a second export queue.

**Requires:** display-session -- the dialogs, the context menu, and the captures need an interactive desktop

**Freeze check:** Every batch export and asset regeneration writes through `AtomicFileWriter` to its chosen targets and never to the open document's own path; asset generation writes only inside `<document>-assets/`; the open document's pixels, path, and dirty state are unchanged; a failed or cancelled export leaves any existing target byte-identical. Fixture source: `tests/fixtures/pinxit/export/` (created by §1, extended here).

- [ ] Add Export Layers to Files (IP-1884, IP-1901): a target folder, prefix, visible only, trim, and per-format options. Done when: a three-layer fixture writes three trimmed files named with the prefix.
- [ ] Add Quick Export and Export As for layers from the Layers panel context menu (IP-1888). Done when: a driven right-click export of one layer writes one file.
- [ ] Add artboards to files (IP-1885, IP-1890) through `D03 T09 §13`. Done when: a two-artboard fixture writes two files sized to their artboards.
- [ ] Add artboards to PDF through the `D03 T17 §7` PDF writer. Done when: PdfPig reads one page per artboard with its media box.
- [ ] Add comps to files (IP-1886, IP-1889, IP-1900) through `D03 T09 §11`. Done when: a three-comp fixture writes three files whose pixels differ as the comps do.
- [ ] Add comps to PDF through the `D03 T17 §7` PDF writer. Done when: PdfPig reads one page per comp.
- [ ] Add Generate Image Assets (IP-1887): Photoshop Generator syntax in layer names (for example `200% hero@2x.png, 80% hero.jpg`, folders, and a `default` layer) parsed by `src/Pinxit/Isotone.Pinxit.Core/Export/AssetNameParser.cs`, regenerated on change into `<document>-assets/`. Done when: `AssetNameParserTests` pass Adobe's documented examples and an edit to a tagged layer rewrites only its assets.
- [ ] Add `BatchExportTests` in `tests/Isotone.Pinxit.Core.Tests/Export/` asserting file names, counts, and sizes for layers, artboards, and comps on the committed fixtures. Done when: the tests pass and fail when a hidden layer is exported with visible only on.
- [ ] Log one Serilog Information line per batch export and asset regeneration naming the source kind, file count, and milliseconds. Done when: a Serilog test logger asserts the line.
- [ ] Commit fixtures under `tests/fixtures/pinxit/export/` (layers, artboards, comps, Generator-named layers) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/batch-export/` and extend `docs/user/pinxit/export.md`. Done when: every control this section adds appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: layers, artboards, and comps to files and PDF, and generated assets"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~BatchExportTests|FullyQualifiedName~AssetNameParserTests"` exits 0, passing Adobe's documented Generator examples and asserting file names, counts, and sizes for layers, artboards, and comps; PdfPig reads one page per artboard and per comp; a driven export of layers, artboards, and comps is captured with the written file list quoted. Cheaper substitute that fails: per-layer Export As by hand, which the file-count tests catch.

## 9. The Export Studio: Slices, Per-Slice Formats, Naming Tokens, Continuous Export, and App Icons

Affinity's Export studio keeps sliced exports current while a designer edits: slices from layers and groups, several formats and sizes per slice, naming tokens and folders, export visibility independent of the canvas, continuous export that rewrites only what changed, and app icon sets. This section builds that studio as its own window on §2's moved slice model and web encoder and §1's export job; `D03 T20 §1` registers it as a workspace preset when workspaces land. Split from §2 on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. Catalog: IP-1908 to IP-1914 (7 features: the Export studio, per-item export visibility, the slices panel, the export options panel, naming tokens, continuous export, and app icon presets).

**Fidelity:** Pinxit Export Studio -- docs/design/components/ (Panel, Canvas, ListTree, LayersRow, ToolRail, ComboBox, TextBox), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/export-studio/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Canvas/README.md, docs/design/components/ListTree/README.md, docs/design/components/LayersRow/README.md, docs/design/components/ToolRail/README.md, docs/design/components/ComboBox/README.md, docs/design/components/TextBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a web or app designer keeps every sliced export current while editing and ships app icon sets. Consumer: browsers, app stores, and the folders the files are published to.
**Treatment:** the Export studio window (slices, export options, and layers panels with continuous export and a status indicator), naming-token fields, and app icon presets. Cheaper substitute that fails the checkpoint: re-exporting every slice on each change, which the changed-slice test catches.
**Chrome:** consume §2's moved slice model and web encoder, §1's job model and runner, the settings store, and the dock. Do not add a second slice model.

**Requires:** display-session -- the studio window and captures need an interactive desktop

**Freeze check:** Studio exports and continuous export write through `AtomicFileWriter` and never to the open document's own path; continuous export rewrites only the changed slices' files; a failed or cancelled write leaves any existing target byte-identical; the open document is never changed except by the slice and export-visibility edits the user makes, which are undoable. Fixture source: `tests/fixtures/pinxit/web/` (created by §2, extended here).

- [ ] Add the Export studio window `src/Pinxit/Isotone.Pinxit.Desktop/Views/Export/ExportStudioWindow.xaml` (IP-1908): a layout of the Slices, Export Options, and Layers panels, with slices created from layers and groups; its Draw Slice button is disabled with a tooltip naming `D03 T18 §3`, whose slice tool enables it. Done when: a driven run creates slices from two layers and the capture shows the studio.
- [ ] Add per-item export visibility independent of canvas visibility (IP-1909). Done when: a layer hidden for export but visible on canvas is absent from its slice's output and present on screen.
- [ ] Add the Slices panel (IP-1910): multiple formats per slice and 1x, 2x, and 3x or absolute sizes with DPI scaling. Done when: one slice with two formats and two sizes writes four files.
- [ ] Add the Export Options panel (IP-1911): per-slice or default settings, presets, and copy and paste of setups. Done when: pasting a setup onto a second slice gives equal settings.
- [ ] Add naming tokens and folder paths (IP-1912), for example `{slice}/{name}@{scale}x.{ext}`. Done when: a test expands every token for a fixture slice.
- [ ] Add continuous export (IP-1913): subscribe to document change events, debounce, and re-export only slices whose bounds intersect the change, with a status indicator. Done when: `ContinuousExportTests` edit inside one slice and only that slice's files change.
- [ ] Add app icon presets (IP-1914) for iOS, Android, Windows, and macOS sets, with Xcode `AppIcon.appiconset/Contents.json`. Done when: the iOS preset writes every size its `Contents.json` lists and the JSON parses.
- [ ] Log one Serilog Information line per studio export and continuous re-export naming the slices and files written. Done when: a Serilog test logger asserts each line.
- [ ] Commit studio fixtures under `tests/fixtures/pinxit/web/` (a two-slice document and an icon source) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/export-studio/` and extend `docs/user/pinxit/web-output.md` with the studio. Done when: every panel appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: the Export studio with continuous export and app icon sets"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ContinuousExportTests"` exits 0 with only the changed slice rewritten, a slice with two formats and two sizes writes four files, every naming token expands for a fixture slice, and the iOS icon preset writes every size its `Contents.json` lists; a driven run creates slices from two layers with the studio captured. Cheaper substitute that fails: re-exporting every slice on each change, which the changed-slice test catches.

## 10. Display Color Management per View and OpenColorIO

What a user sees must be what the file holds, on whichever monitor the window sits: per-monitor profiles, a per-view display transform on the CPU and GPU paths with parity, and for 32-bit work OpenColorIO configurations, display and view transforms, and the ACES view, applied to exports from 32-bit documents too. This section builds that on §4's suite color settings and the `D01 T04 §1` engine, with one OpenColorIO configuration choice replacing the fixed `ocio://default` of `D03 T11 §4` and the per-view config file of `D03 T15 §4`. Split from §4 on 2026-09-27 (operator decision to split the packed sections) along the seam the design named. Catalog: IP-1934, IP-1935, IP-1950 to IP-1952, and IP-1954 (6 features: the OCIO configuration, the ACES display filter, per-view display color management, OCIO display and view transforms, OCIO 2.5 configurations, and display color management preferences).

**Fidelity:** Pinxit display color management per view and OCIO -- docs/design/components/ (Menu, ComboBox, ToggleSwitch, Dialog), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/ocio/, docs/captures/golden/pinxit/display-color/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Menu/README.md, docs/design/components/ComboBox/README.md, docs/design/components/ToggleSwitch/README.md, docs/design/components/Dialog/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer sees correct color on every monitor and grades 32-bit work through the view transform the pipeline uses. Consumer: the `D03 T02 §2` viewport and `D03 T02 §5` GPU path, the `D03 T15 §4` 32-bit preview, and exports from 32-bit documents.
**Treatment:** per-view color management toggles (color-manage this view, intent, BPC, speed or fidelity) in the View menu, and OCIO configuration, display, and view pickers with ACES exposure stops. Cheaper substitute that fails the checkpoint: one sRGB display transform for every monitor, which the monitor-move test catches.
**Chrome:** consume §4's suite settings, the `D01 T04 §1` engine, the `D03 T11 §4` OCIO wrapper, `D03 T02 §2` and `D03 T02 §5` for display, and the settings store. Do not add a second display transform.

**Requires:** display-session -- the display transform on a live view and the monitor move need an interactive desktop

- [ ] Read the per-monitor profile through `WcsGetDefaultColorProfile`, refreshed on display change and when the window moves to another monitor (IP-1954). Done when: a test with a fake WCS provider asserts the display transform uses the new monitor's profile after a move.
- [ ] Add per-view display color management (IP-1950, IP-1954): a color-manage-this-view toggle, intent, BPC, and optimize for speed (8-bit LUT) or fidelity (float), applied in the `D03 T02 §2` viewport and on the `D03 T02 §5` GPU path with CPU parity. Done when: CPU and GPU display transforms agree within 1/255 on a committed fixture.
- [ ] Add OpenColorIO configuration choice (IP-1952): the built-in `ocio://` configs of OCIO 2.5, a user config file, or `$OCIO`, through the `D03 T11 §4` wrapper, replacing the fixed `ocio://default` of `D03 T11 §4`'s OCIO adjustment and the per-view config file of `D03 T15 §4`; an absent or invalid config is refused by name. Done when: selecting an invalid file shows the refusal naming it and both consumers read the chosen config.
- [ ] Add OCIO display and view transforms (IP-1934) and the ACES display with exposure stops (IP-1935) on the `D03 T15 §4` 32-bit preview. Done when: the ACES view of a committed EXR matches OpenImageIO 3.0 `oiiotool --ociodisplay` output within 1/255.
- [ ] Apply OCIO view transforms to exports from 32-bit documents (IP-1951), and register the suite configuration for `D03 T17 §6`'s OCIO-by-filename handling. Done when: an 8-bit export from a 32-bit document with the ACES view matches the preview within 1/255.
- [ ] Log one Serilog Information line per display color management toggle and OCIO configuration, display, or view change. Done when: a Serilog test logger asserts the lines.
- [ ] Commit fixtures under `tests/fixtures/pinxit/color/` (an EXR and a two-monitor fake WCS profile set) with `oiiotool` goldens and `reference.txt` naming OCIO 2.5 and OpenImageIO 3.0. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/pinxit/ocio/` and `docs/captures/pinxit/display-color/`, and extend `docs/user/pinxit/color-management.md` with display color management and OCIO. Done when: every toggle and picker appears in a capture and the page documents it.
- [ ] Commit: `"pinxit: display color management per view and OpenColorIO"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~DisplayColor|FullyQualifiedName~Ocio"` exits 0 with CPU and GPU display transforms agreeing within 1/255 on a committed fixture, the display transform following a fake WCS provider's monitor change, the ACES view of the committed EXR matching OpenImageIO 3.0 `oiiotool --ociodisplay` within 1/255, and an 8-bit export from a 32-bit document matching the preview within 1/255; captures committed. Cheaper substitute that fails: one sRGB display transform for every monitor, which the monitor-move test catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx` exits 0 with every export, web, slice, color, proof, print, and prepress test class of this file reporting
- [ ] `grep -rn "class ColorProfile\|class SoftProofing" src/Pinxit` prints nothing, and `grep -rn "class BackgroundExportQueue\|class PrintPlanner\|class SeparationRenderer\|class PreflightEngine" src` prints one path each, all under `src/Isotone.Core/`
- [ ] Every fixture folder this file creates carries `reference.txt` naming its oracle (lcms2 `transicc`, OCIO, PdfPig, exiftool) and version
- [ ] Every disabled control on this file's surfaces names a section that `python scripts/todo-graph.py resolve` resolves (`D03 T18 §3`, `D03 T18 §7`)
- [ ] B-021 and B-023 are gone from `todo/backlog.md`, and their source keys `legacy-pinxit-7.4` and `legacy-pinxit-1.3` are carried by §6 and §4 alone
- [ ] `python scripts/todo-graph.py validate` clean
