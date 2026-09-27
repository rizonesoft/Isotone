---
schema_version: 1
id: stilus-documents
domain: 02-stilus
status: draft
title: "TODO-04 -- Stilus Documents: Save, Fidelity, Export, and Recovery"
depends_on: []
frozen: true
track: N4
---

# TODO-04 -- Stilus Documents: Save, Fidelity, Export, and Recovery

> **Goal:** A Stilus user's drawing is safe and portable: saving is atomic and never damages the file on disk, closing a changed document asks first, SVG round-trips are proven against committed fixtures, PNG, JPEG, and PDF export produce what the canvas shows, recent files and autosave work, a crash offers recovery, and double-clicking an `.svg` opens it in the running Stilus.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `MainWindowViewModel.Save` and `SaveAs` call `SvgExporter.ExportToFile` directly on the target path, so a crash or full disk mid-write truncates the user's file; `Document.IsDirty` is set false after a save, but nothing prompts on close or exit, and the window title never shows an unsaved marker. `ExportPng`, `ExportJpeg`, `ExportPdf`, and `ExportXaml` only set `StatusText`. `FileOperationsService` (recent files, autosave drafts under `%LOCALAPPDATA%\Bezier\Drafts`) and `ExportService` are referenced by no app code. `SvgImporterTests` and `SvgExporterTests` exist but no committed fixture is round-tripped; the only sample SVGs are `src/Stilus/test.svg` and `src/Stilus/bezier-sample.svg`. The app ignores command-line arguments, so the installer's opt-in `.svg` association (`installer/Stilus.iss`) would start an empty window.
<!-- claim: count "_svgExporter\.ExportToFile\(Document, (CurrentFilePath|dialog\.FileName)\)" src/Stilus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 2 -->
<!-- claim: count "StatusText = \"Export as (PNG|JPEG|PDF|XAML)\.\.\.\";" src/Stilus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 4 -->
<!-- claim: count "Path.Combine\(bezierFolder, \"Drafts\"\)" src/Stilus/Bezier.Core/Services/FileOperationsService.cs = 1 -->
<!-- claim: count "e\.Args" src/Stilus/Bezier.Desktop/App.xaml.cs = 0 -->
<!-- claim: exists src/Stilus/Bezier.Tests/SvgImporterTests.cs -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- atomic saves, autosave never over the user's file, refusal messages
- [`standards/stilus.md`](../../standards/stilus.md) -- SVG is the native format; Inkscape is the fidelity reference
- [`standards/testing.md`](../../standards/testing.md) -- fixtures, goldens, and the fidelity trait
- [`todo/README.md`](../README.md) -- the frozen-behavior rules this file's save and autosave sections join
- -> XREF: D01 T02 §5 -- moves this file's atomic writer to `Isotone.Core` when Pinxit's save needs it
- -> XREF: D02 T03 §5 -- the menu sweep that needs Close and the exports wired
- -> XREF: D02 T07 §1 -- the live-object contract whose fixtures extend §2's round trip; `D02 T07 §14` reuses §1's save and §5's recent files
- -> XREF: D02 T13 §14 -- the PDF writer that replaces §4's `SKDocument` export, keeping `PdfExporterTests` as a regression
- -> XREF: D02 T14 §1 -- SVG options that extend §2's fixtures; `D02 T14 §12`, `§15`, and `§16` extend §3's raster export
- -> XREF: D02 T16 §5 -- the preferences and welcome screen (`D02 T16 §7`) that drive §5's recent files and recovery

## Outcome

- Save and Save As write through an atomic writer, and an interrupted save leaves the previous file byte-identical.
- The title shows `Stilus - name.svg*` while dirty; New, Open, Close, and Exit on a dirty document ask Save, Don't Save, or Cancel.
- Committed SVG fixtures round-trip element by element, with Inkscape-rendered goldens beside them.
- PNG and JPEG export render the document through `SkiaRenderer` at a chosen scale and background; PDF export writes vector PDF through `SKDocument`.
- File, Open Recent lists the last ten files; autosave writes recovery drafts every two minutes; after a crash, the next start offers each draft.
- `Stilus.exe path.svg` opens the file, and a second launch hands the path to the running instance.
- `todo/README.md` lists Stilus's save path and autosave in the frozen set.

**Adjacency:** list=applicable @ D02 T04 §5; document=applicable @ D02 T04 §4; settings=applicable @ D02 T04 §5; reporting=not-applicable (document info is the status strip's); notifications=applicable; permissions=applicable; audit=applicable @ D02 T04 §1; exchange=applicable @ D02 T04 §2; reverse=applicable @ D02 T04 §5

**Adjacency rationale:** Recent files are the list of documents; PDF export is the carried document; the autosave interval is a setting; long exports show progress; a read-only target is the refusal case; every save logs a line; SVG is the exchange format; recovery is the reverse of a crash.

## Implementation Order

| Order | Section | Deliverable                                            | Depends On              | Status |
| :---: | :-----: | ------------------------------------------------------ | ----------------------- | :----: |
|   1   |   §1    | Atomic save and dirty tracking                         | D02 T01 §2              |  [ ]   |
|   2   |   §2    | SVG round-trip fidelity fixtures                       | D02 T01 §1, D00 T03 §1  |  [ ]   |
|   3   |   §3    | PNG and JPEG export                                    | §2, D02 T03 §2          |  [ ]   |
|   4   |   §4    | PDF export                                             | §3                      |  [ ]   |
|   5   |   §5    | Recent files, autosave, and crash recovery             | §1, D01 T02 §2          |  [ ]   |
|   6   |   §6    | Open from the command line and the .svg association    | §1, D01 T02 §3          |  [ ]   |

---

## 1. Atomic Save and Dirty Tracking

Saving over a user's file is the most dangerous thing Stilus does. Today it writes in place, so a crash, a full disk, or an exception halfway through the SVG writer leaves a truncated file and no original. This section makes the save atomic and makes unsaved changes visible and impossible to lose by closing the window. It adds the save path to the frozen set.

**Freeze check:** Save-over writes to a temp file in the target directory, flushes to disk, and replaces the target with `File.Replace` (a rename when the target does not exist); killing the process after the temp write and before the replace leaves the original byte-identical; a read-only target, a locked target, or a full disk is refused with a message naming the file and the reason, and the document stays open and dirty. Fixture source: `tests/fixtures/stilus/save-over/` (created by this section).

**Fidelity:** Stilus main window title and the unsaved-changes prompt -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/main-window/, docs/captures/golden/stilus/save-prompt/.
**Design:** docs/design/components/WindowChrome/README.md, docs/design/components/Dialog/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Stilus main window title and the unsaved-changes prompt -- docs/captures/stilus/main-window/ for the title; the prompt is new build, no baseline, captured to docs/captures/stilus/save-prompt/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can save without risk and cannot lose unsaved work by closing. Consumer: the file on disk and the user.
**Treatment:** `AtomicFileWriter` in `Isotone.Stilus.Core/IO/`; the title shows `Stilus - <name>*` while dirty; a three-button prompt ("Save changes to <name> before closing?" Save, Don't Save, Cancel) on New, Open, Close, and Exit (including the window close button). Cheaper substitute that fails the checkpoint: a `.bak` copy made before writing in place, which still truncates the target on failure.
**Chrome:** consume the standard WPF `MessageBox` for the prompt until a shared dialog exists; the theme resources for the title. Do not write a second save path for Save As.

**Requires:** display-session -- the driven close-with-unsaved-changes run needs an interactive desktop

- [ ] Add `Isotone.Stilus.Core/IO/AtomicFileWriter.cs` (`WriteAsync(path, Func<Stream, Task>)`: temp file `.<name>.<guid>.tmp` in the same folder, `FileOptions.WriteThrough`, `Flush(true)`, then `File.Replace` or `File.Move`; temp deleted on failure). Done when: `AtomicFileWriterTests` cover success, interrupted write (a test hook throws after the temp write), read-only target, locked target, and missing folder.
- [ ] `SvgExporter` gains `Export(VectorDocument, Stream)`; Save and Save As write through `AtomicFileWriter`. Done when: `grep -n "ExportToFile" src/Stilus/Isotone.Stilus.Desktop` prints nothing.
- [ ] A failed save shows "Could not save <name>: <reason>. Your document is still open and has not been changed on disk." and leaves `IsDirty` true. Done when: a view-model test with a failing writer asserts both.
- [ ] Dirty tracking: every executed, undone, or redone command marks the document dirty; saving marks it clean; undoing back to the saved state marks it clean (history tracks the save point). Done when: `DirtyTrackingTests` cover all four.
- [ ] The title binds to name and dirty state; the prompt guards New, Open, Close, Exit, and `Window.Closing`. Done when: a driven run of each path on a dirty document shows the prompt, and Cancel keeps the document.
- [ ] Log `Saved {Path} ({Bytes} bytes, {ElapsedMs} ms)` and `Save of {Path} failed: {Reason}`. Done when: both appear on a driven run with a read-only target.
- [ ] Add "Stilus document save path" to the frozen set paragraph in `todo/README.md`. Done when: the paragraph names it with this section's ref.
- [ ] Commit: `"stilus: atomic save, dirty tracking, and the unsaved-changes prompt"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `AtomicFileWriterTests` and `DirtyTrackingTests` reporting; the interrupted-write test asserts the fixture's SHA-256 is unchanged; a driven run saves over a read-only copy of `tests/fixtures/stilus/svg/bezier-sample.svg`, sees the refusal message, and the log line is quoted; closing a dirty window shows the prompt (capture committed). Cheaper substitute that fails: writing to a `.bak` first, which the interrupted-write hash assertion catches.

## 2. SVG Round-Trip Fidelity Fixtures

SVG is Stilus's native format, so its reader and writer owe a format fidelity proof: open a committed fixture, save it, reopen it, and compare element by element. Inkscape is the reference implementation: each fixture has a PNG golden rendered by Inkscape, and Stilus's rendering of the reopened file is compared against it within a stated tolerance.

- [ ] Build the fixture set under `tests/fixtures/stilus/svg/`: the two moved samples plus one small file per feature the importer claims (rect with rx, circle, ellipse, line, polyline, polygon, path with every command letter including arcs, group with transform, linear and radial gradients, text, image by data URI, `use` with `symbol`, `clipPath`, dashed stroke), each authored for this suite (license: GPL-3.0, recorded in the folder README). Done when: the README lists every file and the feature it covers.
- [ ] Render each fixture with Inkscape (`inkscape --export-type=png --export-dpi=96`, version recorded in `tests/fixtures/stilus/svg/goldens/VERSION.txt`) into `goldens/`. Done when: every fixture has a golden.
- [ ] Add `SvgRoundTripTests` (`[Trait("Category", "Fidelity")]`): for each fixture, import, export to a stream, re-import, and compare the two models element by element (type, id, geometry within 1e-6, fill, stroke, transform, text content). Done when: every fixture passes, or a failing one is filed through `add-todo` as a new section here with the diff quoted, and its case is marked with a skip reason naming that section.
- [ ] Add `SvgRenderFidelityTests`: render each re-imported fixture through `SkiaRenderer` to a bitmap and compare with the golden, passing when at most 0.5 percent of pixels differ by more than 8/255 in any channel (tolerance recorded in the test). Done when: the comparison runs for every fixture, with skip reasons naming sections for known gaps.
- [ ] Commit: `"stilus: prove SVG round trips and rendering against committed fixtures"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` exits 0 and prints one result per fixture for both test classes (quote the per-fixture list, including any skip with its section ref); editing the exporter to drop `transform` attributes makes the group fixture fail. Cheaper substitute that fails: asserting the reopened file "has elements", which the transform mutation passes.

## 3. PNG and JPEG Export

Raster export is how most vector work leaves the editor. `SkiaRenderer` already draws the document; export renders it off-screen at a chosen scale with a chosen background and encodes it. `ExportService` holds option types and dimension math and is wired here.

**Fidelity:** Export dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/export-raster/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/NumberBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Slider/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Export dialog -- new build, no baseline; captured to docs/captures/stilus/export-raster/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can export the document or the selection as PNG or JPEG at 1x, 2x, 3x, or a custom width, with a transparent or white background (JPEG always opaque). Consumer: the exported file.
**Treatment:** File, Export, PNG or JPEG opens a small dialog (scale or width, background, JPEG quality 1 to 100, "selection only" when there is one) then a save dialog; export renders off the UI thread with a progress bar and Cancel for renders over one second, and writes through `AtomicFileWriter`. Cheaper substitute that fails the checkpoint: `RenderTargetBitmap` of the on-screen canvas, which exports the zoom level and the UI overlays.
**Chrome:** consume `SkiaRenderer`, the theme resources, and `AtomicFileWriter`. Do not add a second renderer for export.

**Requires:** display-session -- driving the export dialog needs an interactive desktop

- [ ] Add `RasterExporter` in `Isotone.Stilus.Desktop/Services/` (document or selection, scale, background, format, quality) rendering to an `SKSurface` and encoding with `SKImage.Encode`. Done when: `RasterExporterTests` render the fixture set at 2x and compare against the Inkscape goldens rendered at 192 DPI within the §2 tolerance.
- [ ] Add `RasterExportDialog` and its view model; remember the last options in settings (`Stilus.Export.Raster.*`). Done when: the options survive a restart.
- [ ] Wire `ExportPng` and `ExportJpeg`; long renders show progress and can be cancelled (the partial file is never written). Done when: a cancel test asserts no file exists.
- [ ] Log `Exported {Format} {Path} ({Width}x{Height})`. Done when: the line appears on a driven run.
- [ ] Update the Stilus user guide export page. Done when: the page documents every option.
- [ ] Commit: `"stilus: PNG and JPEG export through the Skia renderer"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `RasterExporterTests` reporting per-fixture pixel comparisons; a driven export of `bezier-sample.svg` at 2x produces a PNG of exactly twice the document size (quote the dimensions from the file header) with a transparent background; capture of the dialog committed. Cheaper substitute that fails: exporting the visible canvas.

## 4. PDF Export

PDF is the document a designer sends to a printer or a client. SkiaSharp's `SKDocument.CreatePdf` records canvas drawing as vector PDF, so the same `SkiaRenderer` calls produce it: paths stay paths, text stays text where the font can be embedded.

**Fidelity:** Export PDF dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/export-pdf/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: Export PDF dialog -- new build, no baseline; captured to docs/captures/stilus/export-pdf/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can export the document as a vector PDF, one page per artboard. Consumer: the PDF file and whoever opens it.
**Treatment:** File, Export, PDF writes one page per artboard (the document bounds when there is none) at the artboard's size in points (1 px = 0.75 pt), embeds fonts that permit embedding, and sets title and creator metadata. Cheaper substitute that fails the checkpoint: a PDF wrapping a PNG, which the text-extraction check catches.
**Chrome:** consume `SkiaRenderer` and `AtomicFileWriter`. Do not add a PDF library.

**Requires:** display-session -- driving the PDF export and opening the result needs an interactive desktop

- [ ] Add `PdfExporter` using `SKDocument.CreatePdf` with `SKDocumentPdfMetadata` (Title from the file name, Creator "Stilus <version>"). Done when: `PdfExporterTests` export the text fixture and assert the PDF contains the text as a text object (the string appears in the decompressed content stream, parsed with a minimal reader in the test) and that page size equals the artboard size in points.
- [ ] Wire `ExportPdf` through the same options pattern as §3 (artboards: all or current). Done when: a two-artboard document exports two pages.
- [ ] Update the Stilus user guide export page. Done when: PDF is documented.
- [ ] Commit: `"stilus: vector PDF export with one page per artboard"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `PdfExporterTests` reporting; a driven export opened in a PDF viewer shows vector edges at 800 percent zoom and selectable text (capture committed); the page size read from the file matches. Cheaper substitute that fails: rasterizing to PDF.

## 5. Recent Files, Autosave, and Crash Recovery

A designer who loses an hour to a crash stops using the app. Autosave writes a recovery draft of each dirty document on an interval, to the app's data folder and never over the user's file; the next start after a crash offers what it found. Recent files make the work findable again. `FileOperationsService` has recent-file and draft code; this section wires it onto the `Isotone.Core` settings store and app-data paths. Autosave joins the frozen set.

**Freeze check:** Autosave writes only to `%LOCALAPPDATA%\Rizonesoft\Stilus\recovery\` through `AtomicFileWriter`, never to the document's own path; a draft is deleted only after a successful save of its document or an explicit Discard in the recovery prompt; killing the process during an autosave leaves the previous draft readable. Fixture source: `tests/fixtures/stilus/save-over/`.

**Fidelity:** File, Open Recent submenu and the recovery prompt -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/main-window/, docs/captures/golden/stilus/recovery/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: File, Open Recent submenu and the recovery prompt -- docs/captures/stilus/main-window/ for the menu; the recovery prompt is new build, no baseline, captured to docs/captures/stilus/recovery/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can reopen recent work in two clicks and get back unsaved work after a crash. Consumer: the user; the drafts' consumer is the recovery prompt.
**Treatment:** Open Recent lists up to 10 files (missing ones shown disabled with "(not found)" and removable), with Clear Recent; autosave every 2 minutes (a setting, 0 turns it off) of dirty documents only; on start, if drafts exist from a session that did not exit cleanly, a dialog lists each (name, time, size) with Recover, Discard, and Later. Cheaper substitute that fails the checkpoint: saving the user's file automatically, which violates the freeze check.
**Chrome:** consume the `Isotone.Core` settings store and app-data paths, `AtomicFileWriter`, and the theme. Do not keep `FileOperationsService`'s own paths.

**Requires:** display-session -- the kill-and-recover drive needs an interactive desktop

- [ ] Move `FileOperationsService`'s recent-file list onto `StilusSettings` (`Stilus.RecentFiles`, max 10) and its draft folder onto `AppDataPaths.Recovery`. Done when: `grep -n "LocalApplicationData" src/Stilus` prints nothing.
- [ ] Wire File, Open Recent (with Clear Recent) and add each opened or saved file to the list. Done when: `RecentFilesTests` cover ordering, the cap, and missing files.
- [ ] Add `AutosaveService` (timer, dirty documents only, `AtomicFileWriter`, a session marker file deleted on clean exit) and the `Stilus.Autosave.IntervalMinutes` setting (default 2). Done when: `AutosaveServiceTests` cover interval, clean-document skip, and draft deletion after save.
- [ ] Add the recovery dialog shown at startup when a stale session marker and drafts exist. Done when: a driven kill-and-restart offers the draft and Recover opens it dirty and untitled-with-original-name.
- [ ] Log each autosave at Debug and each recovery action at Information. Done when: the lines appear in a driven run.
- [ ] Add "Stilus autosave and recovery" to the frozen set in `todo/README.md`. Done when: the paragraph names it with this section's ref.
- [ ] Commit: `"stilus: recent files, autosave drafts, and crash recovery"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `RecentFilesTests` and `AutosaveServiceTests` reporting; a driven run draws a shape, waits for the autosave line in the log, kills `Stilus.exe` with `Stop-Process -Force`, restarts, and the recovery dialog offers the draft; Recover shows the shape; the original file on disk is unchanged (SHA-256 before and after quoted). Cheaper substitute that fails: autosaving to the document path.

## 6. Open from the Command Line and the .svg Association

The installer offers an `.svg` association that starts `Stilus.exe "%1"`; today Stilus ignores its arguments, so the association opens an empty window. With the shared single-instance service, a second launch with a path hands it to the running window.

- [ ] `App.OnStartup` reads `e.Args`; each existing `.svg` path opens (the first into the startup document, further ones as the multi-document work allows: until tabs exist, the first opens and the rest are listed in a message naming `D02 T06 §7`). Done when: `Stilus.exe tests\fixtures\stilus\svg\bezier-sample.svg` opens the sample.
- [ ] Use `Isotone.Core` single instance: a second launch forwards its paths and exits; the running window activates and opens the first path through the dirty prompt. Done when: a driven second launch opens the file in the first window and only one `Stilus` process remains.
- [ ] A path that does not exist or is not SVG shows "Stilus cannot open <path>: <reason>." and logs a Warning. Done when: a driven launch with a `.txt` path shows the message.
- [ ] Commit: `"stilus: open files from the command line and the .svg association"`

**Requires:** display-session -- the driven second-launch run needs an interactive desktop

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with a `StartupArgumentsTests` class for path filtering; a driven run launches Stilus, then launches it again with the sample path: one process remains (`Get-Process Stilus` count 1) and the sample is open (log line quoted); after installing with the association task, double-clicking an `.svg` in Explorer opens it. Cheaper substitute that fails: opening a second window per file.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes every SVG fixture or names the section owning each skip
- [ ] The freeze checks of §1 and §5 pass on the committed fixtures
- [ ] `todo/README.md` lists both frozen behaviors
- [ ] `python scripts/todo-graph.py validate` clean
