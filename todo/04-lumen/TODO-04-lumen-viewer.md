---
schema_version: 1
id: lumen-viewer
domain: 04-lumen
status: draft
title: "TODO-04 -- Lumen Parity: the Fast Default Viewer"
depends_on: []
frozen: true
track: L4
---

# TODO-04 -- Lumen Parity: the Fast Default Viewer

> **Goal:** Lumen ships an IrfanView-class image viewer: `LumenViewer.exe`, a second executable in the Lumen install with its own minimal startup path, opens any image the suite reads in milliseconds from Explorer within a recorded, measured startup budget, can be registered as the Windows default viewer for every format it reads, browses the file's folder with prefetch, shows images at any zoom with correct orientation and display color, plays multi-page and animated files, runs fullscreen and quick slideshows, shows information, histogram, pixel values, QR codes, and text, performs file operations, and offers quick edits (rotate, crop, resize, color, effects, text, watermark, borders, lossless JPEG transforms) that run the batch engine's operations; the Lumen library is one keystroke away. Originals are safe by default and written only on opt-in (operator decision 2026-09-27, "Safe by default, opt-in writes"): quick edits save to a new file and rotation is stored as metadata unless the user turns on an in-place setting of `D04 T11 §1`'s `OriginalWritePolicy`, in which case Save and lossless rotation replace the original through its `InPlaceWriter`, atomically and after a verified backup copy. The code lives in `src/Lumen/Photon.Lumen.Viewer/` (the WPF exe, AssemblyName `LumenViewer`) and `src/Lumen/Photon.Lumen.Core/Viewer/`; it decodes only through the shared `Photon.Core/Formats/` registry (`D04 T13 §1`), applies display color through `D01 T04 §1`, applies quick edits through `D04 T11 §7`'s `IBatchOperation` implementations and the `Photon.Core` effect registry (`D01 T03`, `D01 T06`), and forwards to `Lumen.exe` through `D01 T02 §3`.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Lumen has no code at all (`src/Lumen` is absent), so there is no viewer project; the Lumen app itself is created by `D04 T01 §2`, and every checklist path below names the projects that section creates (`src/Lumen/Photon.Lumen.Core/`, `src/Lumen/Photon.Lumen.Desktop/`, `tests/Photon.Lumen.Tests/`). The app manifest `scripts/apps.psd1` still names the legacy project path `src/Lumen/Lumen.UI/Lumen.UI.csproj` and marks Lumen `Shipping  = $false`, and names no `LumenViewer` executable. `installer/Lumen.iss` refuses to compile without `/DLumenShipping` (three mentions) and registers no file type, while the shared `installer/common.iss` already sets `ChangesAssociations=yes`. `standards/lumen.md` states the frozen guard "Lumen never writes an original image" unless the user opts in, with the opt-in writes the operator approved on 2026-09-27 (recorded in the standard at the Lumen integration), which `D04 T11 §1` builds and this file's §11 and §16 consume. Nothing in `src/` registers a Windows capabilities key or sets a wallpaper. `docs/dev/lumen/` (where §1 records the startup budgets) does not exist yet.
<!-- claim: absent src/Lumen -->
<!-- claim: count "src/Lumen/Lumen.UI/Lumen.UI.csproj" scripts/apps.psd1 = 1 -->
<!-- claim: count "Shipping  = \$false" scripts/apps.psd1 = 1 -->
<!-- claim: count "LumenViewer" scripts/apps.psd1 = 0 -->
<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->
<!-- claim: count "assoc_" installer/Lumen.iss = 0 -->
<!-- claim: count "ChangesAssociations=yes" installer/common.iss = 1 -->
<!-- claim: count "Lumen never writes an original image" standards/lumen.md = 1 -->
<!-- claim: count "opt-in" standards/lumen.md = 5 -->
<!-- claim: count "RegisteredApplications" src/**/*.cs = 0 -->
<!-- claim: count "IDesktopWallpaper" src/**/*.cs = 0 -->
<!-- claim: absent docs/dev/lumen -->

## Inputs

- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard every writing section obeys, safe by default with the opt-in in-place writes of `D04 T11 §1`
- [`standards/shared.md`](../../standards/shared.md) -- window anatomy, atomic saves, settings, logging, and performance budgets
- [`standards/testing.md`](../../standards/testing.md) -- fixtures, goldens, and fidelity tolerances
- [`docs/parity/lumen-parity.md`](../../docs/parity/lumen-parity.md) -- the catalog rows each section owns (`LP-` ranges named in each context paragraph)
- [`docs/parity/lumen-section-design.md`](../../docs/parity/lumen-section-design.md) -- "The viewer architecture" and its budgets, which these sections were authored from
- IrfanView 4.76 (`i_view64.exe`, driven for behavior and key parity, version recorded in each section's stamp) and ACDSee Photo Studio Ultimate 2027 View mode and Quick View (from its user guide)
- Microsoft Learn: "Default Programs" and "Registering an Application for Use in Windows" (`Capabilities`, `RegisteredApplications`, `OpenWithProgids`), `IDesktopWallpaper`, `IFileOperation`, `Shell_NotifyIconW`, `SHChangeNotify`, `SetThreadExecutionState`, and `Windows.Media.Ocr` -- the platform APIs §3, §6, §8, §9, and §17 call
- The IJG `jpegtran` lossless transform (libjpeg-turbo 3.1, IJG, BSD-3-Clause, and zlib licenses) -- the reference and golden producer for §16
- ZXing.Net 0.16 (Apache-2.0) and Vortice.MediaFoundation (the Media Foundation bindings of Vortice.Windows, MIT, approved by the operator 2026-09-27) -- the dependencies §9 and §8 add, each recorded in `docs/dev/decisions.md` by the section that adds it; NAudio was not approved for Lumen (operator decision 2026-09-27)
- -> XREF: D04 T02 §8 -- Lumen 0.1.0 ships before every section here
- -> XREF: D01 T02 §3 -- single instance and file-open forwarding for §1, §17, and the hand-off to Lumen
- -> XREF: D01 T02 §5 -- the atomic writer §6's Save As and §13's tile export write through
- -> XREF: D01 T04 §1 -- display color transforms for §2
- -> XREF: D01 T03 §2 -- resampling and rotation for §4, §11, and §14
- -> XREF: D01 T03 §3 -- quantization and dithering for §12
- -> XREF: D01 T03 §4 -- tonal adjustments and `ToneCurve` for §12 and §15
- -> XREF: D01 T03 §6 -- blur, sharpen, and noise effects the §15 browser lists
- -> XREF: D01 T03 §7 -- distort effects the §15 browser lists
- -> XREF: D01 T06 §5 -- JPEG artifact reduction for §2's deblocking
- -> XREF: D01 T07 §5 -- the red-eye and pet-eye detector §12 applies
- -> XREF: D03 T11 §4 -- the LUT readers and color lookup behind §15's film simulation
- -> XREF: D04 T01 §4 -- the RAW decoder and embedded previews §2 consumes
- -> XREF: D04 T01 §8 -- the library grid §1 opens photos from and the `T` key filters until browse mode ships
- -> XREF: D04 T01 §11 -- the XMP sidecars §9 and §16 write ratings and orientation into
- -> XREF: D04 T02 §3 -- the histogram control §9 hosts
- -> XREF: D04 T02 §7 -- Edit in Imago from the viewer (§1)
- -> XREF: D04 T05 §1 -- browse mode, the target of the `T` key once it ships
- -> XREF: D04 T05 §6 -- the rename journal §6's renames follow once it ships
- -> XREF: D04 T08 §8 -- metadata writing into sidecars, and into originals only on the opt-in, which §9's metadata edits reach once it ships
- -> XREF: D04 T09 §6 -- develop's Auto Lens preview, which hooks into §2's display path beside §15's view-only Auto Lens filter
- -> XREF: D04 T09 §13 -- the Light EQ preview that hooks into §2's display path
- -> XREF: D01 T09 §2 -- the isolated 8BF filter host §15's Plug-in Filters category runs through (the former B-012 rows)
- -> XREF: D01 T09 §4 -- the plug-in manager §15's plug-in folders open
- -> XREF: D04 T11 §1 -- `OriginalGuard`, `OriginalWritePolicy`, and `InPlaceWriter`: the one opt-in path to an original that §11's Save and §16's in-place rotation use
- -> XREF: D04 T11 §2 -- the token engine §13 and §18 fill text with
- -> XREF: D04 T11 §5 -- `LosslessJpegTransform` and `OrientationCommand`, which §11 and §16 consume
- -> XREF: D04 T11 §7 -- the batch operations the quick edits of §11, §12, §13, and §15 apply
- -> XREF: D04 T11 §8 -- the text and watermark engine §13 uses
- -> XREF: D04 T11 §10 -- the batch dialog the viewer and §3's Explorer verbs open
- -> XREF: D04 T12 §4 -- printing a selection or the current image goes through Lumen's print module
- -> XREF: D04 T12 §8 -- Lumen parity output cites §8: the `SlideshowAudioPlayer` D04 T12 §8 reuses for slideshow music
- -> XREF: D04 T13 §1 -- the codec registry and its screen-size decode capability
- -> XREF: D04 T13 §2 -- the modern formats §2 displays
- -> XREF: D04 T13 §3 -- the format families §3 registers
- -> XREF: D04 T13 §4 -- the document and multi-page formats §3 registers and §10 pages through
- -> XREF: D04 T13 §5 -- RAW coverage and RAW+JPEG pairs §2 and §6 honor
- -> XREF: D04 T13 §6 -- the writers §6's Save As uses
- -> XREF: D04 T13 §8 -- the rare and historical formats §3 registers
- -> XREF: D04 T14 §3 -- the keymap editor the viewer's default keys register with
- -> XREF: D04 T14 §4 -- the preferences frame the viewer's settings pages move into
- -> XREF: D04 T14 §10 -- the Originals preferences group that renders the opt-in keys §11 and §16 read
- -> XREF: D04 T15 §1 -- Lumen 0.2.0 releases this file's Phase 30 sections
- -> XREF: D04 T15 §2 -- Lumen 0.3.0 releases this file's Phase 31 sections
- -> XREF: D04 T10 §12 -- Lumen AI cites §9: the Lumen Viewer's information tools, where D04 T10 §12 shows faces

## Outcome

- Double-clicking a 24-megapixel JPEG in Explorer shows it full screen within 450 ms cold and 250 ms warm on the reference machine recorded in `docs/dev/lumen/viewer-budgets.md`, a resident viewer shows it within 100 ms, and the assemblies loaded at first paint match a committed allow-list with no SQLite and no catalog.
- Lumen Viewer can be made the Windows default viewer for every extension the codec registry reads through Default Apps, without ever writing a `UserChoice` key, and unregistering leaves no value behind.
- A folder of any readable files browses with prefetch (next image within 50 ms cached), correct orientation, DNG geometry, and display color, with every zoom, fit, pan, magnifier, fullscreen, page, animation, and slideshow control IrfanView offers.
- File operations (Recycle Bin, rename, copy, move, clipboard, wallpaper, external editors) carry sidecars and RAW+JPEG partners with the file and refuse read-only and locked targets by name.
- Quick edits (geometry, color, effects, text, watermarks, borders, lossless JPEG transforms) apply the same `IBatchOperation` implementations as batch, pixel for pixel, with undo.
- With the default settings every original is byte-identical after any viewer session; with an in-place opt-in of `D04 T11 §1` on, the viewer's Save and lossless rotation replace the original only through its `InPlaceWriter`, after a verified backup copy, and never through a viewer-owned write path.

**Adjacency:** list=applicable @ D04 T04 §5; document=applicable @ D04 T12 §4; settings=applicable @ D04 T04 §14; reporting=applicable @ D04 T04 §9; notifications=applicable @ D04 T04 §2; permissions=applicable @ D04 T04 §6; audit=applicable @ D04 T04 §6; exchange=applicable @ D04 T04 §6; reverse=applicable @ D04 T04 §11

**Adjacency rationale:** The folder file list, position box, recent files, and hot folder of §5 and the quick slideshow list of §8 are the browsable lists. Printing from the viewer is a document path owned by Lumen's print module `D04 T12 §4`; the viewer only hands the image or selection to it. Every viewer option is a `Lumen.Viewer.*` key with a default and a named consumer, and §14 holds the largest set; the opt-in keys are `D04 T11 §1`'s `Lumen.Originals.InPlace.*`, which the viewer reads and never redefines. Image information, histogram, pixel values, and status fields of §9 are the reports. Decode failures name the format and decoder (§2), and folder-end and slideshow-end prompts notify (§5, §8). Read-only folders and locked files are refused by name on move, rename, delete, and save (§6), and an original is refused for writing unless `D04 T11 §1`'s policy allows the kind. One Serilog Information line per file operation and saved file is the audit (§6), and an opted-in original write is journaled by `D04 T11 §1`'s `InPlaceWriter`. Clipboard formats, drag and drop, Save As in every writable format, TXT slideshow lists, and PAL palettes are the exchange surface (§6, §8, §12). Quick-edit undo and redo (§11), the Recycle Bin for deletes (§6), orientation reset (§16), and `D04 T11 §1`'s Restore Original from Backup for an opted-in write are the reverses.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The Lumen Viewer: a second executable with a startup budget and the hand-off to Lumen | D04 T02 §8, D04 T13 §1, D01 T02 §3 |  [ ]   |
|   2   |   §2    | The viewer decode path: screen-size decode, prefetch, and display color | §1, D04 T13 §2, D04 T13 §5, D01 T04 §1 |  [ ]   |
|   3   |   §3    | Default viewer registration and shell integration | §1, D04 T13 §3, D04 T13 §4, D04 T13 §8 |  [ ]   |
|   4   |   §4    | Zoom, fit, pan, magnifier, and navigator | §2 |  [ ]   |
|   5   |   §5    | Browsing a folder in the viewer | §2 |  [ ]   |
|   6   |   §6    | File operations and hand-offs in the viewer | §5 |  [ ]   |
|   7   |   §7    | Fullscreen and presentation | §4, §5 |  [ ]   |
|   8   |   §8    | Quick slideshow in the viewer | §7 |  [ ]   |
|   9   |   §9    | Image information, histogram, and viewer tools | §4 |  [ ]   |
|  10   |   §10   | Multi-page and animated images in the viewer | §4, D04 T13 §4 |  [ ]   |
|  11   |   §11   | Quick edits I: rotate, flip, select, crop, resize, and canvas | §4, §6, D04 T11 §7 |  [ ]   |
|  12   |   §12   | Quick edits II: color corrections, color depth, and palettes | §11 |  [ ]   |
|  13   |   §13   | Quick edits IV: text, watermarks, borders, and combining images | §11, D04 T11 §8 |  [ ]   |
|  14   |   §14   | Viewer window and display options | §4, §5 |  [ ]   |
|  15   |   §15   | Quick edits III: the effects browser and viewer effects | §12, D03 T11 §4, D01 T09 §2, D01 T09 §4 |  [ ]   |
|  16   |   §16   | Lossless JPEG transforms to new files, or in place on opt-in | §11, D04 T11 §5 |  [ ]   |
|  17   |   §17   | Resident quick-start mode | §1 |  [ ]   |
|  18   |   §18   | Captions and info text through the token engine | §7, §8, §9, D04 T11 §2 |  [ ]   |

---

## 1. The Lumen Viewer: a second executable with a startup budget and the hand-off to Lumen

IrfanView opens an image before the user notices a window because it is a tiny native program; `Lumen.exe` cannot, because it pays for its dependency-injection container, its SQLite catalog, and its module shell before the first frame. So the viewer is a second executable, `LumenViewer.exe` (`Photon.Lumen.Viewer`), shipped inside the Lumen installer and portable ZIP and versioned with Lumen: `Main` starts reading and decoding the file on the thread pool before any window exists, and nothing heavier than the codec registry, the settings store, logging, and the theme loads before the first paint. The budgets are hard gates measured by this section's startup harness, not aims: cold start to the first full-screen pixel of a 24-megapixel JPEG at most 450 ms, warm start at most 250 ms, working set at most 200 MB for that image, and a committed allow-list of the assemblies loaded at first paint; WPF cannot be trimmed or compiled Native AOT, which is recorded as the reason the budget is not lower, so the exe publishes ReadyToRun with tiered PGO. The viewer also hands the current photo to Lumen with one key, so the catalog stays one keystroke away. It must not slow `Lumen.exe`'s own startup and never opens an original for writing. The resident quick-start mode (LP-0003) was split into §17 at authoring because this section would otherwise pass 24 items. It serves the acceptance-bar aim "Any image opens instantly". Catalog: LP-0001, LP-0002, LP-0004 to LP-0008 (7 features; LP-0003 is built by §17). -> SOURCE: parity-lumen-viewer-exe

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer/.
**Job:** a user double-clicks a photo in Explorer and sees it before they notice a window opening, and reaches the library, browse, develop, or Imago from it with one key. Consumer: none: this surface is the consumer of the codec registry, and `Lumen.exe` consumes the hand-off arguments.
**Treatment:** a borderless-feeling window with the image, a slim bottom toolbar, and a status strip; `Esc` closes; `T` opens the folder in Lumen, `Ctrl+L` opens the photo in the library, `Ctrl+E` hands it to Imago. Cheaper substitute that fails the checkpoint: launching `Lumen.exe` with a loupe, which pays for the catalog and module shell and misses the budget.
**Chrome:** consume the `Photon.UI` theme and dialog styles and `Photon.Core` settings, logging, and single instance. Do not build a dependency-injection container before the first paint.

**Requires:** display-session -- the startup harness launches the published viewer and times its first rendered frame

- [ ] Create `src/Lumen/Photon.Lumen.Viewer/Photon.Lumen.Viewer.csproj` (`net11.0-windows10.0.26100.0`, WPF, `AssemblyName` `LumenViewer`, `PublishReadyToRun` and `TieredPGO` true) referencing only `Photon.Core`, `Photon.UI`, and `Photon.Lumen.Core`, and add it to `Photon.slnx` (LP-0002, LP-0005). Done when: `dotnet build Photon.slnx -c Release` produces `LumenViewer.exe` with warnings as errors and the project file lists exactly those three references.
- [ ] Add `LumenViewer.exe` to the Lumen entry of `scripts/apps.psd1` as an extra executable published into the same folder as `Lumen.exe`. Done when: `pwsh scripts/publish.ps1 -App Lumen` leaves both executables side by side under `artifacts/publish/` and the portable ZIP of `scripts/package.ps1` contains both.
- [ ] Add a "Lumen Viewer" Start menu entry to `installer/Lumen.iss`, removed on uninstall. Done when: `ISCC /DLumenShipping installer/Lumen.iss` compiles and the installed Start menu lists "Lumen Viewer".
- [ ] Write `ViewerProgram.Main` in `src/Lumen/Photon.Lumen.Viewer/ViewerProgram.cs` (`[STAThread]`, no `App.xaml` `StartupUri`): parse the arguments with `ViewerArguments.Parse`, start `ViewerDecodeService.DecodeForScreenAsync(path)` on the thread pool, then construct the WPF `Application` and `ViewerWindow`. Done when: the startup trace shows the decode starting before the window is created. Cheaper substitute: a `StartupUri` window that decodes in `Loaded`.
- [ ] Show the first frame in `ViewerWindow` as soon as the screen-size decode completes, with the theme background before it. Done when: the trace's first-rendered-frame event carries the image's pixel size.
- [ ] Build dialog services lazily in `src/Lumen/Photon.Lumen.Viewer/Composition/ViewerServices.cs` on the first dialog or settings open. Done when: `Microsoft.Extensions.DependencyInjection` is absent from the first-paint allow-list below.
- [ ] Add `ViewerArguments` in `src/Lumen/Photon.Lumen.Core/Viewer/ViewerArguments.cs`: one or several file paths (quoted, with spaces), the `--startup-trace` switch, and unknown switches ignored with one Warning log line; command-line automation beyond opening files stays backlog B-041 (LP-0008). Done when: `ViewerArgumentsTests` cover paths with spaces, three files, and an unknown switch.
- [ ] Add the `--startup-trace` switch writing process start (`Process.StartTime`), window created, and the first `CompositionTarget.Rendering` with the image to `%LOCALAPPDATA%\Rizonesoft\Lumen\logs\viewer-startup.jsonl`. Done when: one launch appends one line with the three timestamps and the decoder name.
- [ ] Commit fixtures under `tests/fixtures/lumen/viewer/startup/`: a 24-megapixel JPEG and a CR3 with an embedded preview, both CC0 with their sources in `SOURCES.md`. Done when: both files and `SOURCES.md` are committed.
- [ ] Write `docs/dev/lumen/viewer-budgets.md`: the reference machine (CPU, RAM, disk, Windows build), the budgets (cold 450 ms, warm 250 ms, resident hand-off 100 ms from §17, next image 50 ms cached and 150 ms uncached and RAW embedded preview 200 ms from §2, working set 200 MB), how cold is produced (the standby list emptied with Sysinternals RAMMap `-Es`), and why WPF sets the floor. Done when: the page states every budget and the measurement method.
- [ ] Add `ViewerStartupTests` in `tests/Photon.Lumen.Tests/Viewer/ViewerStartupTests.cs`: launch the published exe with `--startup-trace` on the 24-megapixel fixture five times cold and five times warm and assert the median against the budgets, reading the peak working set from `Process.PeakWorkingSet64`; cold runs are skipped with a stated reason where RAMMap is absent. Done when: the test prints each median and fails when one is over budget.
- [ ] Add `ViewerAssemblyAllowListTests`: at first paint `AppDomain.CurrentDomain.GetAssemblies()` equals the committed list in `tests/fixtures/lumen/viewer/first-paint-assemblies.txt` (no `Microsoft.Data.Sqlite`, no catalog assembly, no dependency-injection container). Done when: adding an assembly fails the test naming the added assembly.
- [ ] Forward later opens to the running viewer through `D01 T02 §3`'s `SingleInstance` with the pipe name `Rizonesoft.LumenViewer` when `Lumen.Viewer.SingleInstance` (default on) is set, and open a new window otherwise (LP-0004, LP-0007). Done when: a second launch with a path leaves one process showing that path, and with the setting off leaves two.
- [ ] Add File, Open in New Window for the current file (LP-0004). Done when: the command opens a second window on the same image with its own folder position.
- [ ] Implement exit behavior (LP-0006): `Esc` closes, `Lumen.Viewer.WarnOnEscExit` asks first, unsaved quick edits prompt Save As through §6, and `Lumen.Viewer.DoubleClickCloses` closes on a double-click of the image. Done when: each setting is read back from `settings.json` and changes the behavior in a driven run.
- [ ] Add `ViewerHandoff` in `src/Lumen/Photon.Lumen.Core/Viewer/ViewerHandoff.cs` starting or forwarding to `Lumen.exe` with `--browse <folder> --select <file>` on `T`; until `D04 T05 §1` ships, Lumen opens the library grid of `D04 T01 §8` filtered to that folder (LP-0001). Done when: a driven `T` selects the photo in Lumen (capture).
- [ ] Map `Ctrl+L` to `--library <file>`, the Develop entry to `--develop <file>`, and `Ctrl+E` to `D04 T02 §7`'s Edit in Imago command, disabled with its tooltip when Imago is absent (LP-0001). Done when: `ViewerHandoffTests` assert each argument pair through a fake launcher.
- [ ] Teach `Lumen.exe` (`src/Lumen/Photon.Lumen.Desktop/App.xaml.cs`) to accept `--browse`, `--select`, `--library`, and `--develop` directly and through its single-instance forward, and add `F3` in the grid and loupe to open the selected photo in the viewer (LP-0001). Done when: `ViewerHandoffTests` cover the forwarded case and a driven `F3` opens the viewer on the selection.
- [ ] Log one Information line per open (`Viewer opened {Path} in {Ms} ms by {Decoder}`) and per hand-off (`Viewer handed {Path} to Lumen as {Mode}`). Done when: a test logger sees both.
- [ ] Add `docs/user/lumen/viewer.md` (opening files, keys, hand-offs) and commit the captures under `docs/captures/lumen/viewer/`. Done when: the page names every key in the Treatment and the capture folder holds the window and a hand-off.
- [ ] Commit: `"lumen: the Lumen Viewer as a fast second executable with a startup budget"`

**Test checkpoint:** Driven run with evidence plus unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewerStartupTests|FullyQualifiedName~ViewerAssemblyAllowListTests|FullyQualifiedName~ViewerArgumentsTests|FullyQualifiedName~ViewerHandoffTests"` exits 0 on the reference machine of `docs/dev/lumen/viewer-budgets.md`, and the stamp quotes the measured medians as hard gates: cold at most 450 ms, warm at most 250 ms, peak working set at most 200 MB for the 24-megapixel fixture; any value over budget fails the section. A driven `T` from the viewer selects the photo in Lumen (capture under `docs/captures/lumen/viewer/`). Cheaper substitute that fails: a loupe window inside `Lumen.exe`, which the allow-list test (SQLite loaded) and the cold timing both catch.

## 2. The viewer decode path: screen-size decode, prefetch, and display color

A viewer that decodes every file at full resolution on the UI thread feels slow no matter how fast it starts. This section makes the first pixels of any readable file come from a screen-size or embedded-preview decode, sharpens progressively to the full decode, prefetches the next image and keeps the previous one, rotates by EXIF, applies DNG opcode geometry, shows developed or original versions, color-manages to the monitor profile, and names the format and decoder when a file fails. The budgets are hard gates: next and previous image at most 50 ms from the prefetch cache and at most 150 ms uncached at screen size, and a RAW embedded preview at most 200 ms. It decodes only through the shared registry (`D04 T13 §1`): a viewer-private decoder is a defect. Catalog: LP-0009 to LP-0023 (15 features). -> SOURCE: parity-lumen-viewer-decode

**Fidelity:** docs/captures/lumen/viewer/ (baseline from §1); new captures to docs/captures/lumen/viewer-decode/.
**Job:** a user browsing a folder never waits on decoding, sees colors as the photographer intended, and sees why a file will not open. Consumer: none: this surface is the consumer of the registry and the color engine.
**Treatment:** a toolbar toggle between RAW embedded preview and RAW decode, press and hold `O` (configurable) for the original, a status-strip badge "Preview" until the full decode lands, and an in-window error panel naming the file, format, and decoder. Cheaper substitute that fails the checkpoint: decoding every file at full resolution on the UI thread.
**Chrome:** consume the `Photon.Core/Formats/` registry's screen-size capability, `D04 T01 §4`'s decoder, and `D01 T04 §1`'s transforms. Do not add a viewer-private decoder or color path.

**Requires:** display-session -- display color and next-image timings are measured on screen

- [ ] Add `ViewerDecodeService` in `src/Lumen/Photon.Lumen.Core/Viewer/Decoding/ViewerDecodeService.cs` asking the registry for `DecodeOptions.TargetSize` equal to the monitor's pixel size, which uses JPEG DCT scaling, JPEG 2000 and JPEG XL reduced levels, and RAW embedded previews where the codec offers them. Done when: `ViewerDecodeServiceTests` assert the decoded size per codec family on the fixtures.
- [ ] Schedule the full decode after the screen-size one and swap it in without a flash, showing the "Preview" badge until then (LP-0016). Done when: a driven zoom past the preview shows the badge clear and the log records both decodes.
- [ ] Add RAW display modes (LP-0009, LP-0014): embedded preview (default), half size, or full decode through `D04 T01 §4`, switched by the toolbar and `Lumen.Viewer.RawMode`, with a full decode when zooming past the preview's resolution. Done when: each mode's decoded size is asserted on the CR3 fixture.
- [ ] Add `PrefetchCache` in `src/Lumen/Photon.Lumen.Core/Viewer/Decoding/PrefetchCache.cs` (LP-0015): decode the next image in the browse direction and keep the previous one, bounded by `Lumen.Viewer.PrefetchMB` (default 512), cancelled on a direction change. Done when: `PrefetchCacheTests` assert eviction at the bound and cancellation within 50 ms.
- [ ] Apply orientation (LP-0013) from EXIF and from the catalog and sidecar orientation that §11 and §16 store, the catalog value winning. Done when: `ViewerDecodeServiceTests` show orientation 1 to 8 fixtures upright and a sidecar orientation overriding EXIF.
- [ ] Apply DNG opcode geometry for display (LP-0011): `WarpRectilinear` and `FixVignetteRadial` from `OpcodeList3` through `D01 T03 §2`. Done when: a DNG fixture with a `WarpRectilinear` opcode matches the Adobe DNG SDK `dng_validate` render within 2/255 (version recorded).
- [ ] Show the developed result when the photo has a catalog edit stack or a sidecar with develop settings (LP-0010), rendered at screen size through `D01 T07`'s pipeline loaded on first use, and show the original while `O` is held. Done when: a fixture with sidecar develop settings renders differently from its original and the press-and-hold restores the original.
- [ ] Convert tagged images from their profile and untagged ones as sRGB (`Lumen.Viewer.AssumeUntaggedAs`, default sRGB) to the monitor profile read per monitor through `D01 T04 §1`, re-rendering when the window moves to another monitor (LP-0017, LP-0021, LP-0023). Done when: `ViewerColorTests` map the Display P3 fixture to known sRGB values within delta E 1 against an sRGB monitor profile.
- [ ] Add `Lumen.Viewer.ApplyDisplayProfileOnSave` (default off) that §6's Save As reads to convert pixels to the display profile before writing (LP-0021). Done when: the key is read back from `settings.json` and §6's save test asserts it.
- [ ] Add display gamma (LP-0012) and legacy load-as-grayscale (LP-0018) as display-only transforms `Lumen.Viewer.DisplayGamma` and `Lumen.Viewer.LoadAsGray`. Done when: a gray-ramp fixture's displayed values follow the gamma and nothing is written to the file or catalog.
- [ ] Add JPEG deblocking and quantization smoothing on load (LP-0020, LP-0022) through `D01 T06 §5`, off by default (`Lumen.Viewer.JpegDeblock`, `Lumen.Viewer.JpegSmooth`). Done when: a quality-20 JPEG fixture's displayed pixels match the `D01 T06 §5` golden within 1/255.
- [ ] Notify the user of a decode failure with a typed panel and log it (LP-0019): "Lumen Viewer cannot open {Name}: {Format} is not supported by {Decoder} {Version}", or the decoder's own error for a damaged file. Done when: a truncated JPEG and an unknown extension each produce their message in the window and one Warning log line.
- [ ] Commit fixtures under `tests/fixtures/lumen/viewer/decode/`: orientation 1 to 8 JPEGs, a Display P3 tagged JPEG, an untagged PNG, a DNG with opcodes, a gray ramp, and a quality-20 JPEG, with sources in `SOURCES.md`. Done when: the files are committed.
- [ ] Add `ViewerNavigationTimingTests` to the startup harness: over a 200-file folder generated from the fixtures, time next and previous from the cache and uncached at screen size, and the first frame of the CR3's embedded preview. Done when: the test prints the medians and fails over 50 ms, 150 ms, or 200 ms respectively.
- [ ] Add the RAW modes, press-and-hold original, and display color sections to `docs/user/lumen/viewer.md` and commit captures of the P3 and orientation-6 fixtures under `docs/captures/lumen/viewer-decode/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: the viewer decode path with prefetch and display color"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewerDecodeServiceTests|FullyQualifiedName~PrefetchCacheTests|FullyQualifiedName~ViewerColorTests|FullyQualifiedName~ViewerNavigationTimingTests"` exits 0 on the reference machine, and the stamp quotes the hard gates: next and previous at most 50 ms cached and at most 150 ms uncached over the 200-file folder, and the RAW embedded preview's first frame at most 200 ms; captures show the P3 fixture and the orientation-6 fixture correct. Cheaper substitute that fails: a full-resolution decode per image, which the uncached timing catches.

## 3. Default viewer registration and shell integration

IrfanView's selling point is that it becomes the viewer for every image type. Windows 8 and later refuse programmatic changes to a user's default apps (the `UserChoice` key is hash-protected and reset when written), so Lumen Viewer registers as a capable application instead: `HKCU\Software\RegisteredApplications` names "Lumen Viewer", whose `Capabilities\FileAssociations` maps every extension the codec registry reads to a per-family ProgID, each extension gets an `OpenWithProgids` value, and "Make Lumen Viewer the default" opens Windows' Default Apps page for it, where one button sets it for all of them. IrfanView's per-extension "registry attempt" at forcing the default is deliberately not reproduced. Nothing here uses a COM shell extension: every Explorer verb is a static registry verb. It serves the acceptance-bar aim "Any image opens instantly ... and can be the Windows default viewer for every format Lumen reads". Catalog: LP-0024 to LP-0028 (5 features). -> SOURCE: parity-lumen-default-viewer

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-associations/.
**Job:** a user makes Lumen Viewer their photo viewer for every format in two clicks and can undo it. Consumer: Windows Default Apps and Explorer, which read the registered capabilities and verbs.
**Treatment:** an Associations page with format groups (images, RAW, documents, archives) and per-extension checkboxes, All, Images only, Clear, custom extensions, an all-users option when elevated, and a "Make Lumen Viewer the default" button that opens `ms-settings:defaultapps?registeredAppUser=Lumen%20Viewer`; a second-launch prompt offering it once. Cheaper substitute that fails the checkpoint: writing `UserChoice`, which Windows rejects by hash and resets.
**Chrome:** consume the preferences frame of `D04 T14 §4` when it ships (the page opens standalone before), `Photon.UI` dialog styles, and the suite icon set. Do not write a second registry helper where `Photon.Core` already has one.

**Requires:** display-session -- the Default Apps hand-off and Explorer verbs are driven on a desktop

- [ ] Add `ShellRegistration` in `src/Lumen/Photon.Lumen.Core/Viewer/Shell/ShellRegistration.cs` writing `HKCU\Software\RegisteredApplications\Lumen Viewer` = `Software\Rizonesoft\LumenViewer\Capabilities` with `ApplicationName`, `ApplicationDescription`, `ApplicationIcon`, and `FileAssociations` for each chosen extension (LP-0026). Source: Microsoft Learn, "Registering an Application for Use in Windows". Done when: `ShellRegistrationTests` read every value back from the redirected root.
- [ ] Write per-family ProgIDs (`LumenViewer.jpeg`, `LumenViewer.png`, `LumenViewer.raw`, `LumenViewer.document`, `LumenViewer.archive`, and one per remaining family) with `DefaultIcon` and `shell\open\command` = `"<install>\LumenViewer.exe" "%1"`, and one `OpenWithProgids` value per extension (LP-0026). Done when: the tests assert the command line and that no `UserChoice` key is opened.
- [ ] Take the extension list from `CodecRegistry.ReadableExtensions` grouped by family, plus `Lumen.Viewer.CustomExtensions` (LP-0025, LP-0026). Done when: a test registry with one extra codec yields its extension in the list without code changes.
- [ ] Write the `HKLM` variants only when the process is elevated and "All users" is ticked (LP-0026). Done when: an unelevated run with "All users" ticked is refused with "Registering for all users needs administrator rights" and writes nothing.
- [ ] Add the Associations page `src/Lumen/Photon.Lumen.Viewer/Settings/AssociationsPage.xaml` with format groups, per-extension checkboxes, All, Images only, Clear, and custom extensions, associating or disassociating per group (LP-0025, LP-0026). Done when: ticking the RAW group and applying registers every RAW extension and clearing it removes them (registry readback).
- [ ] Add "Make Lumen Viewer the default" opening `ms-settings:defaultapps?registeredAppUser=Lumen%20Viewer`, with the page text "Windows asks you to confirm the change on the next screen" (LP-0024). Done when: a driven click opens the Default Apps page for Lumen Viewer (capture).
- [ ] Offer the same hand-off once on the second launch when Lumen Viewer is not the default, recorded in `Lumen.Viewer.DefaultPromptShown` (LP-0024). Done when: the prompt shows on the second launch only (settings readback).
- [ ] Draw four per-family icons (image, RAW, document, archive) in house under `resources/icons/lumen-viewer/` as multi-size `.ico` files and list them with their license in `resources/icons/README.md` (LP-0028). Done when: the icons are committed and Explorer shows the RAW icon on a `.cr3` after registration (capture).
- [ ] Add Explorer verbs as static registry verbs (LP-0027): `Browse with Lumen` on `Directory`, `Directory\Background`, and `Drive`; `Open with Lumen Viewer`; a Send To shortcut; and context entries Slideshow (opens §8's dialog), Lossless rotate (§16), and Copy file names to the clipboard; the batch and multipage entries are added by `D04 T11 §10` and the combine entry by §13. Done when: `ShellRegistrationTests` assert each verb's command line.
- [ ] Add `--register` and `--unregister` to `ViewerArguments`, recording every value written in `Software\Rizonesoft\LumenViewer\Registered` so unregister removes exactly those. Done when: register then unregister leaves the redirected root with no value this section wrote.
- [ ] Add an unchecked installer task "Register Lumen Viewer for image types" to `installer/Lumen.iss` running `LumenViewer.exe --register`, with the uninstaller running `--unregister`. Done when: on a clean profile the task registers the capabilities and the uninstall leaves none (reg query output quoted).
- [ ] Call `SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, null, null)` after each registration change. Done when: Explorer refreshes the icons without a sign-out in the driven run.
- [ ] Log one Information line per registration change (`Registered Lumen Viewer for {Count} extensions ({Scope})`). Done when: a test logger sees it for register and unregister.
- [ ] Add `ShellRegistrationTests` in `tests/Photon.Lumen.Tests/Viewer/` over a redirected root (`HKCU\Software\PhotonTests\<guid>` through an `IRegistryRoot` seam), asserting register then unregister leaves no value and `UserChoice` is never touched. Done when: the tests pass and delete their root.
- [ ] Add `docs/user/lumen/default-viewer.md` (register, choose formats, make default, undo) and commit captures under `docs/captures/lumen/viewer-associations/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: register Lumen Viewer for every format it reads and hand off to Default Apps"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ShellRegistrationTests"` exits 0; on a clean user profile the installer task registers the capabilities, the Default Apps page lists Lumen Viewer, and after the user sets it a double-click on a `.heic` and a `.cr3` opens the viewer (captures under `docs/captures/lumen/viewer-associations/`); the uninstall leaves no value the install wrote (reg query quoted). Cheaper substitute that fails: `UserChoice` writes, which Windows resets on the next open and the test's `UserChoice` assertion refuses.

## 4. Zoom, fit, pan, magnifier, and navigator

Checking focus on a burst needs every zoom path IrfanView and ACDSee offer and the ability to keep the same view while stepping through images. This section adds a pure viewport model (zoom, offset, rotation, fit mode) with every zoom gesture and dialog, fit modes, zoom and pan locks, temporary view rotation, a navigator, and a magnifier, all without touching the file, the catalog, or the sidecar. Catalog: LP-0033 to LP-0043 (11 features). -> SOURCE: parity-lumen-viewer-zoom

**Fidelity:** docs/captures/lumen/viewer/ (baseline from §1); new captures to docs/captures/lumen/viewer-zoom/.
**Job:** a user checks focus and detail at any scale and keeps the same view while stepping through a burst. Consumer: none: this surface is the consumer of the decoded image.
**Treatment:** `+`, `-`, `Ctrl` plus wheel at the pointer, click to toggle 100 percent, a zoom value box and slider with presets, a Zoom To dialog, fit modes on number keys, `L` locks zoom and scroll, a navigator pane and overlay, a magnifier on `M`, and view rotation on `Ctrl+Alt+Left` and `Ctrl+Alt+Right`. Cheaper substitute that fails the checkpoint: fit and 100 percent only.
**Chrome:** consume `D01 T03 §2` resampling for display tiles and the `Photon.UI` theme. Do not add a second resampler.

**Requires:** display-session -- zoom and pan are driven on screen

- [ ] Add `ViewportModel` in `src/Lumen/Photon.Lumen.Core/Viewer/ViewportModel.cs` (zoom, offset, view rotation, fit mode, image and viewport sizes) with pure methods and no WPF types. Done when: `ViewportModelTests` construct it without a dispatcher.
- [ ] Add zoom steps from a fixed table or a step factor, centered zoom, and the calculation mode `Lumen.Viewer.ZoomStepMode` (LP-0043). Done when: the tests assert the next and previous step from 100 percent in both modes.
- [ ] Add zoom in, out, the slider, and the preset list (LP-0036), and the zoom value box in the status strip accepting a typed value (LP-0041). Done when: a driven zoom through each control lands on the stated percentage (log line per zoom change at Debug level).
- [ ] Add the Zoom To dialog with a typed percentage, click to toggle actual size, and `Ctrl` plus wheel zooming at the pointer (LP-0036). Done when: `ViewportModelTests.PointerAnchoredZoom` keeps the pointed image pixel under the pointer within half a pixel.
- [ ] Add fit modes (LP-0038): fit image, width, height, smaller side, reduce only, enlarge only, reduce or enlarge, the default mode `Lumen.Viewer.DefaultFit`, number-key shortcuts, and a fit toggle key. Done when: the tests assert each mode on landscape and portrait fixtures.
- [ ] Add zoom defaults (LP-0040): reset on image change or keep, auto shrink or enlarge, click zooming, and pan speed, each a `Lumen.Viewer.Zoom.*` key. Done when: each key is read back and changes the model's behavior in a test.
- [ ] Add zoom and pan lock on `L` (LP-0037), keeping zoom and the relative scroll position across images. Done when: `ViewportModelTests.LockSurvivesImageChange` passes on two differently sized fixtures.
- [ ] Add panning (LP-0035): hand drag, right-button drag when §14's right-button option says scroll, arrows with `Shift` faster and `Ctrl` slower, numeric keypad jumps to edges and corners, and the horizontal wheel. Done when: the tests assert each keypad jump's offset.
- [ ] Render display tiles through `D01 T03 §2` at non-integer zooms from the decoded image, cached per zoom level and discarded on image change. Done when: a driven zoom from 10 to 800 percent shows no blank tiles and the cache stays under `Lumen.Viewer.PrefetchMB`.
- [ ] Add the navigator pane and a quick overlay with a magnification slider and a draggable view marquee (LP-0034). Done when: dragging the marquee moves the view offset in a driven run (capture).
- [ ] Add the magnifier (LP-0033, LP-0042): an on-image lens on `M` or a pane, fixed or relative magnification, smooth or pixel display, reusable by §7 in fullscreen. Done when: the lens shows pixel display at 800 percent in a capture.
- [ ] Add temporary view rotation on `Ctrl+Alt+Left` and `Ctrl+Alt+Right` (LP-0039) as view state only. Done when: the tests assert rotation leaves the file hash, the catalog orientation, and the sidecar unchanged.
- [ ] Add `ViewportModelTests` in `tests/Photon.Lumen.Tests/Viewer/` covering fit modes, pointer-anchored zoom, steps, locks, and keypad jumps. Done when: the class passes.
- [ ] Add the zoom, fit, navigator, and magnifier section to `docs/user/lumen/viewer.md` and commit captures under `docs/captures/lumen/viewer-zoom/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: viewer zoom, fit, pan, navigator, and magnifier"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewportModelTests"` exits 0, and a driven session zooms at the pointer, locks zoom across a burst, and uses the magnifier and navigator (captures under `docs/captures/lumen/viewer-zoom/`). Cheaper substitute that fails: fit and 100 percent only, which the fit-mode and pointer-anchor tests catch.

## 5. Browsing a folder in the viewer

The viewer browses the opened file's folder the way IrfanView does: every navigation key, a position box with a pattern filter, sorting, loop rules, drag and drop, recent files and folders, and a hot folder that shows photos arriving from a camera maker's tether utility (tethered capture proper stays backlog B-048). The list comes from a large-fetch enumeration of the folder filtered to the registry's readable types, never from the catalog, so it works on a folder Lumen has never seen. Catalog: LP-0044 to LP-0058, LP-0252 (16 features). -> SOURCE: parity-lumen-viewer-browse

**Fidelity:** docs/captures/lumen/viewer/ (baseline from §1); new captures to docs/captures/lumen/viewer-browse/.
**Job:** a user steps through a folder or a card the way IrfanView does, including photos arriving in a watched folder. Consumer: §2's prefetch, §8's slideshow, and §14's filmstrip, which read the list.
**Treatment:** `Space` and `Backspace`, arrows, `Home`, `End`, `Page Up`, `Page Down`, `Ctrl+M` for random, a position box "12 / 340", browse buttons over the image, File, Open Recent, and View, Hot Folder. Cheaper substitute that fails the checkpoint: next and previous in name order only.
**Chrome:** consume the registry's readable-extension list, a large-fetch `FindFirstFileExW` enumeration, and `FileSystemWatcher`. Do not read the folder through the catalog.

**Requires:** display-session -- folder browsing is driven on screen

- [ ] Add `FolderFileList` in `src/Lumen/Photon.Lumen.Core/Viewer/Browse/FolderFileList.cs` enumerating the folder with `FindFirstFileExW` (`FindExInfoBasic`, `FIND_FIRST_EX_LARGE_FETCH`) filtered to associated, custom, or all readable types (LP-0055). Done when: `FolderFileListTests` list a mixed temp folder with each filter.
- [ ] Sort by name, natural, date, EXIF date (read lazily through the registry's metadata reader), size, extension, or none, with direction (LP-0053). Done when: the tests assert natural order (`img2` before `img10`) and EXIF-date order from fixtures.
- [ ] Continue into the next or previous sibling folder at the list's end when `Lumen.Viewer.ContinueIntoNextFolder` is on (LP-0047). Done when: the tests assert the crossing and the setting off stops at the end.
- [ ] Add navigation (LP-0045, LP-0252): next, previous, first, last, random (`Ctrl+M`), skip by N, `Home`, `End`, `Page Up`, `Page Down`. Done when: each key's target index is asserted in `FolderFileListTests.Navigation`.
- [ ] Add browse buttons over the image and keep the pointer on them after the window moves (LP-0045, LP-0056). Done when: a driven click series keeps the pointer on the button after a resize (capture).
- [ ] Add browsing options (LP-0057): other files in the folder, hidden files, a folder-end dialog, loop or stop, beep, wheel browsing, and always jump on page or wheel, each a `Lumen.Viewer.Browse.*` key. Done when: each key is read back and the end-of-folder rules are asserted in the tests.
- [ ] Add the position box (LP-0051) showing index of total, jumping by index or page, and filtering by a pattern such as `*2026*`. Done when: a pattern filter of a 1,000-file folder shows the matching count in a driven run.
- [ ] Add drag and drop (LP-0046, LP-0050): dropped files replace or join the list (`Lumen.Viewer.DropMode`), and dragging the image out gives other programs the file. Done when: dropping three files onto the viewer and dragging the current file into Explorer both work in a driven run.
- [ ] Add reopen and refresh of the current file and the folder list (LP-0049). Done when: a file added to the folder appears after refresh with the current image kept.
- [ ] Add recent files and recently saved files with clearing, and recent folders in dialogs (LP-0052, LP-0058), in `Lumen.Viewer.RecentFiles`, `Lumen.Viewer.RecentSaved`, and `Lumen.Viewer.RecentFolders` (default 10 each). Done when: the lists round-trip through `settings.json` and Clear empties them.
- [ ] Add the Open dialog (LP-0048) through `IFileOpenDialog` with the registry's format filter, the Explorer preview pane, and recent folders as places. Done when: the dialog filters to readable types in a driven run (capture).
- [ ] Add the hot folder (LP-0044, LP-0054) in `src/Lumen/Photon.Lumen.Core/Viewer/Browse/HotFolder.cs`: `FileSystemWatcher` on a chosen folder, show new images immediately or append, wait until a file's size is stable for 500 ms, include subfolders, clear after a delay, and rescan when the watcher's buffer overflows. Done when: `HotFolderTests` show a slowly written file only after it stops growing.
- [ ] Add `FolderFileListTests` and `HotFolderTests` in `tests/Photon.Lumen.Tests/Viewer/`. Done when: both classes pass.
- [ ] Add the browsing and hot-folder section to `docs/user/lumen/viewer.md` and commit captures under `docs/captures/lumen/viewer-browse/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: folder browsing, recent files, and hot folders in the viewer"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~FolderFileListTests|FullyQualifiedName~HotFolderTests"` exits 0, and a driven session browses a 1,000-file folder by keys, jumps by pattern, and shows a file copied into a hot folder within 1 second of its last write (timing quoted). Cheaper substitute that fails: name order only, which the natural and EXIF-date sort tests catch.

## 6. File operations and hand-offs in the viewer

A user who culls a card from the viewer alone needs deletes, renames, copies, moves, clipboard, saving, wallpaper, and external editors, with sidecars and RAW+JPEG partners following every file operation and no chance of overwriting an original by accident. Save follows the operator's 2026-09-27 decision "Safe by default, opt-in writes": here, in Phase 30, `Ctrl+S` always opens Save As with a new suggested name and a path equal to the opened original is refused, which is the safe default; the opt-in save over the original arrives with `D04 T11 §1`'s `OriginalWritePolicy` and `InPlaceWriter` in Phase 31 and is wired into the viewer by §11, so this section builds no write path to an original. File operations are explicit user file operations, not image writes. Refusals are this file's permissions surface (a read-only folder or a locked file is refused by name), each operation writes one audit log line, and the clipboard, drag-out, and Save As in every writable format are its exports. Catalog: LP-0029, LP-0030, LP-0116 to LP-0121, LP-0175 to LP-0178 (12 features; the paste-into-selection options of LP-0119 are built by §11, which owns the selection). -> SOURCE: parity-lumen-viewer-files

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-files/.
**Job:** a user culls and files a card from the viewer alone and never loses or overwrites an original by accident. Consumer: the file system and the Recycle Bin, and the catalog once `D04 T05 §6` ships.
**Treatment:** `Del` to the Recycle Bin with an optional prompt, `Shift+Del` permanent behind a confirmation, `F2` rename, `F7` move and `F8` copy with destination slots, `Ctrl+C` image, `Ctrl+Shift+C` path, `Ctrl+S` opening Save As with a suggested new name, Set as Wallpaper, Open With, and External Editors 1 to 3. Cheaper substitute that fails the checkpoint: Save overwriting the opened file.
**Chrome:** consume `D04 T13 §6`'s writers (JPEG, PNG, and TIFF through the registry until it ships), `Photon.Core`'s `AtomicFileWriter` (`D01 T02 §5`), and `IFileOperation` for the Recycle Bin. Do not write a second atomic writer or any write path to an original.

**Requires:** display-session -- file operations are driven from the viewer window

**Freeze check:** A driven session of delete, rename, move, quick-edit Save, Save As, and wallpaper over a copy of `tests/fixtures/lumen/viewer/files/` leaves every remaining original's SHA-256 and last-write time unchanged, Save onto the opened path is refused before any file is opened for writing, and every new file is written through `AtomicFileWriter` (killing the process mid-save leaves no partial file at the target). Fixture source: `tests/fixtures/lumen/viewer/files/` (created by this section).

- [ ] Add `ViewerFileOperations` in `src/Lumen/Photon.Lumen.Core/Viewer/Files/ViewerFileOperations.cs` over `IFileOperation` with `FOFX_RECYCLEONDELETE`, deleting the file with its `.xmp` sidecar and RAW+JPEG partner by base name when `Lumen.Viewer.DeleteSidecars` (default on) is set (LP-0175). Done when: `ViewerFileOperationsTests` show all three files in the Recycle Bin through `IFileOperation`'s sink.
- [ ] Add the delete prompt `Lumen.Viewer.ConfirmDelete`, `Shift+Del` permanent delete behind a confirmation naming the file, and after-delete behavior (next, previous, close, or return to browse) (LP-0175, LP-0120). Done when: each after-delete choice is asserted on the list index.
- [ ] Add rename on `F2` (LP-0178) renaming sidecars and the partner with the same base name, keeping the list index, and retrying three times on a sharing violation before refusing by name; the catalog record follows through `D04 T05 §6` once it ships. Done when: the tests rename a RAW+JPEG+XMP trio together and a locked file is refused with its name.
- [ ] Add Move to (`F7`) and Copy to (`F8`) with ten destination slots (`Lumen.Viewer.Destinations`), recent folders, and relative paths, carrying sidecars and partners (LP-0177, LP-0120). Done when: the tests move a trio into slot 3 and the list advances.
- [ ] Add name-clash handling (LP-0177): a replace dialog with both previews, keep both (numbered suffix), or skip, plus shortcut-only copy through `IShellLinkW`. Done when: each choice is asserted in a temp folder and the `.lnk` resolves to the source.
- [ ] Refuse a read-only destination and a locked source by name, leaving the list and both folders unchanged. Done when: the tests assert the messages "{Folder} is read-only" and "{File} is in use by another program".
- [ ] Add clipboard copy (LP-0176): `Ctrl+C` puts the image as `CF_DIBV5` and PNG, `Ctrl+Shift+C` the full path, a menu entry the file name, and Clear Clipboard empties it. Done when: a test reads the PNG back with the same pixel hash as the displayed image.
- [ ] Add paste as a new unsaved image (LP-0119) named by `Lumen.Viewer.PasteNamePattern` (default `Clipboard_{counter}`); pasting into a selection is §11's. Done when: `Ctrl+V` of a PNG on the clipboard shows an unsaved image titled `Clipboard_1`.
- [ ] Make Save and Save As (LP-0118, LP-0121) open a dialog by default with `<name>-edit.<ext>` suggested, format by type or extension, keep the original date and time, recent save folders, and an overwrite prompt for an existing file that is not the opened original, writing through `AtomicFileWriter` and the registry's writers and honoring §2's `Lumen.Viewer.ApplyDisplayProfileOnSave`. Done when: `ViewerSaveGuardTests.SaveAsNewFile` writes the new file and the original's hash is unchanged.
- [ ] Refuse a Save As path equal to the opened original with "Lumen never overwrites the original from the viewer. Choose a new name." (§11 extends this when the opt-in exists). Done when: `ViewerSaveGuardTests.RefusesOriginalPath` asserts the message and the unchanged hash. Cheaper substitute: a warning that still writes.
- [ ] Add Set as Wallpaper (LP-0116, LP-0117) through `IDesktopWallpaper`: centered, fill, tiled, stretched, proportional, span, a monitor choice, and a confirmation, writing the image as a copy under `%LOCALAPPDATA%\Rizonesoft\Lumen\wallpaper\`. Done when: a driven set on monitor 1 shows the copy's path in `IDesktopWallpaper::GetWallpaper` (quoted).
- [ ] Record the previous wallpaper path and position per monitor before each change and add Restore Previous Wallpaper (LP-0116). Done when: restore returns `GetWallpaper` to the recorded path.
- [ ] Add up to three external editors (LP-0029) in `Lumen.Viewer.ExternalEditors` (name, executable, arguments with `%1`) shown by name in the menu and the toolbar, a missing executable refused by name. Done when: a configured `notepad.exe` entry launches with the current path in a driven run.
- [ ] Add Open With (LP-0030) through `SHOpenWithDialog` and the shell `open` and `edit` verbs through `ShellExecuteExW`. Done when: a driven Open With lists the installed image apps (capture).
- [ ] Log one Information line per file operation (`{Operation} {Source} -> {Target}`), per saved file, and per wallpaper change. Done when: a test logger sees one line per operation in `ViewerFileOperationsTests`.
- [ ] Add `ViewerFileOperationsTests` and `ViewerSaveGuardTests` in `tests/Photon.Lumen.Tests/Viewer/` over the `tests/fixtures/lumen/viewer/files/` fixtures (a RAW+JPEG+XMP trio, a lone JPEG, a read-only folder made at test time). Done when: both classes pass and every fixture's hash is unchanged after every case.
- [ ] Add `docs/user/lumen/viewer-files.md` (delete, rename, copy, move, clipboard, save as a new file, wallpaper, and editors) and commit captures under `docs/captures/lumen/viewer-files/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: viewer file operations, save as a new file, wallpaper, and external editors"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewerFileOperationsTests|FullyQualifiedName~ViewerSaveGuardTests"` exits 0, and the unchanged-originals hash table over a driven session of delete, rename, move, quick-edit Save As, and wallpaper is quoted with every remaining original unchanged. Cheaper substitute that fails: Save in place, which `ViewerSaveGuardTests.RefusesOriginalPath` catches.

## 7. Fullscreen and presentation

Showing photos to others needs a fullscreen mode with only the image, every fit and resampling option, a backdrop, transitions, cursor hiding, spanning or choosing monitors, and touch-friendly mouse rules. Captions and info text with placeholders need the token engine `D04 T11 §2`, which ships in Phase 31 after this section, so they were split into §18 at authoring (LP-0078, LP-0084). The Explorer context-menu preview (LP-0031, PicaView) is not built: it needs an in-process COM shell extension, and the operator decided on 2026-09-27 not to plan `Photon.Lumen.ShellPreview`, so LP-0031 goes to the backlog at integration with the catalog row updated there. Catalog: LP-0077, LP-0079 to LP-0083, LP-0085 to LP-0087 (9 features built here; LP-0078 and LP-0084 built by §18; LP-0031 to the backlog). -> SOURCE: parity-lumen-viewer-fullscreen

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-fullscreen/.
**Job:** a user shows photos full screen to others with only the image. Consumer: none: this surface is the consumer of §4's viewport and §5's list.
**Treatment:** `F`, `Enter`, or a double-click toggles, `Esc` exits, quick fit keys 1 to 7, a fullscreen context menu with the viewer tools, a blurred-sides backdrop, and a crossfade. Cheaper substitute that fails the checkpoint: a maximized window.
**Chrome:** consume `D01 T03 §2` for resampling, §4's `ViewportModel` and magnifier, and the `Photon.UI` theme. Do not add a second renderer for fullscreen.

**Requires:** display-session -- fullscreen is captured on screen, including a second monitor

- [ ] Add `FullscreenController` in `src/Lumen/Photon.Lumen.Viewer/Fullscreen/FullscreenController.cs` toggling a borderless topmost window over the monitor on `F`, `Enter`, or a double-click, exiting on `Esc`, with `Lumen.Viewer.StartFullscreen` (LP-0077). Done when: a driven toggle covers the monitor with no taskbar visible (capture).
- [ ] Add the fullscreen context menu with the viewer tools (zoom, rotate view, slideshow, information, file operations) (LP-0077). Done when: every entry executes its viewer command in a driven run.
- [ ] Add fullscreen display options (LP-0080): original size, fit large only, fit all, stretch, fit width, height, or smaller side, a display multiplier, centering, and quick keys 1 to 7, as `Lumen.Viewer.Fullscreen.*` keys. Done when: `FullscreenLayoutTests` assert each mode's rectangle on four monitor sizes.
- [ ] Add fullscreen resampling on first display and on zoom (LP-0081) through `D01 T03 §2`. Done when: `Lumen.Viewer.Fullscreen.Resample` off shows nearest-neighbor pixels and on shows the Lanczos result (capture pair).
- [ ] Add the backdrop (LP-0082): screen color or blurred image sides built from a downscaled, blurred copy. Done when: a portrait image on a landscape monitor shows blurred sides (capture).
- [ ] Add transitions and a crossfade between images (LP-0083) with a duration setting and off respecting the Windows animation-effects setting. Done when: a driven next shows the fade and the animation-effects setting off shows a cut.
- [ ] Hide the cursor in fullscreen and show it briefly on movement (LP-0079). Done when: the cursor hides after `Lumen.Viewer.Fullscreen.CursorHideMs` (default 1,500) in a driven run.
- [ ] Add the fullscreen mouse rules (LP-0086): left or right button scrolling for touch screens, and left click previous and right click next. Done when: each rule's action is asserted through the command bindings in a test.
- [ ] Make unused keys end fullscreen unless `Lumen.Viewer.Fullscreen.UnusedKeysExit` is off (LP-0087). Done when: a driven unbound key exits with the setting on and not with it off.
- [ ] Add all-monitor spanning or a chosen monitor (LP-0085). Done when: a driven span on two monitors covers both (capture).
- [ ] Offer §4's magnifier in fullscreen. Done when: `M` shows the lens in fullscreen (capture).
- [ ] Add `FullscreenLayoutTests` in `tests/Photon.Lumen.Tests/Viewer/`. Done when: the class passes.
- [ ] Add the fullscreen section to `docs/user/lumen/viewer.md` and commit captures under `docs/captures/lumen/viewer-fullscreen/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: fullscreen presentation in the viewer"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~FullscreenLayoutTests"` exits 0, and captures under `docs/captures/lumen/viewer-fullscreen/` show fullscreen with blurred sides, the crossfade setting, and a two-monitor span. Cheaper substitute that fails: a maximized window, which the two-monitor span capture and the taskbar-hidden capture expose.

## 8. Quick slideshow in the viewer

IrfanView's quick slideshow plays a folder or a hand-picked list with music in seconds, distinct from the authored slideshow module of `D04 T12 §7`. This section adds the file-list dialog, per-image durations and captions, playback rules, background music, window or fullscreen presentation, saved TXT lists, and in-show actions; info text with placeholders during the show is §18's (it needs the token engine). Self-running EXE and screen-saver slideshows stay backlog B-049. Catalog: LP-0088 to LP-0100 (13 features; the placeholder info text of LP-0097 is built by §18). -> SOURCE: parity-lumen-viewer-slideshow

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-slideshow/.
**Job:** a user plays a folder or a hand-picked list with music in seconds. Consumer: none: this surface is the consumer of §5's list and §7's fullscreen renderer.
**Treatment:** `W` opens the Slideshow dialog (a list with add, add all, remove, sort, insert position, per-image duration and caption, timing, loop, random, music, window or fullscreen), Play starts, and the Image Advance keys work during play. Cheaper substitute that fails the checkpoint: a timer over the folder with no list.
**Chrome:** consume §7's fullscreen renderer, Windows Media Foundation through Vortice.MediaFoundation (MIT) for music, and the `Photon.UI` dialog styles. Do not add a second fullscreen window.

**Requires:** display-session -- playback is driven on screen

- [ ] Add `QuickSlideshowList` in `src/Lumen/Photon.Lumen.Core/Viewer/Slideshow/QuickSlideshowList.cs` (LP-0093, LP-0094): add, add all, remove, sort by name, date, size, extension, or EXIF date, insert position, a remembered start index, and per-image duration and caption. Done when: `QuickSlideshowListTests` cover each operation.
- [ ] Add the Slideshow dialog on `W` (LP-0092) in `src/Lumen/Photon.Lumen.Viewer/Slideshow/SlideshowDialog.xaml` over the list. Done when: a driven dialog adds a folder, reorders two files, and plays (capture).
- [ ] Add the start points (LP-0088, LP-0090): from the viewer, the current folder, a selection, the last used folder, automatic viewing, and append or remove the current file; Save and Append to a slideshow list. Done when: each start point opens the dialog with the expected list in a driven run.
- [ ] Add Image Advance (LP-0089): next, previous, pause, forward, reverse, or random sequence, repeat, and delay. Done when: `QuickSlideshowListTests.RandomWithoutRepeats` covers every item once per cycle.
- [ ] Add the playback rules (LP-0095): loop, close after last, skip unreadable files, advance by timer or key, random without repeats with history, and pause. Done when: an unreadable file in the list is skipped with one Warning log line and the show continues.
- [ ] Add the orientation filter (LP-0100): all, landscape only, or portrait only. Done when: the tests assert the filtered sequence on mixed fixtures.
- [ ] Add background music (LP-0096) through Windows Media Foundation: `SlideshowAudioPlayer` in `src/Lumen/Photon.Lumen.Core/Audio/` over the Media Engine (`IMFMediaEngine`) through Vortice.MediaFoundation (part of Vortice.Windows, MIT, approved by the operator 2026-09-27 in place of NAudio, which was not approved for Lumen; Vortice.Windows is already in `Directory.Packages.props` from `D03 T15 §4`), playing MP3, AAC, and WAV with loop, track advance, and a fade out through the engine's volume, for audio entries in the list or a looped MP3, with a `docs/dev/decisions.md` row recording the package and its license. Done when: `SlideshowAudioPlayerTests` with a fake engine assert track order, looping, and the final fade, and a driven show plays and loops an MP3 fixture (log line per track start).
- [ ] Add presentation (LP-0097): fullscreen through §7 or a window with position and size, and hide cursor. Done when: a window show at a set size and position is captured.
- [ ] Keep the system awake during a show with `SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)` and release it at the end (LP-0091). Done when: `powercfg /requests` lists LumenViewer during a show and not after (quoted).
- [ ] Add in-show actions (LP-0099): zoom, scroll, delete to the Recycle Bin through §6, copy, and animated images playing through §10's player once it ships. Done when: a driven delete during a show removes the file and the show continues.
- [ ] Load and save TXT lists with comments and relative paths, and persist the last list (LP-0098). Done when: `QuickSlideshowListTests.TxtRoundTrip` reproduces a list with comments and relative paths byte-for-byte.
- [ ] Add `QuickSlideshowListTests` in `tests/Photon.Lumen.Tests/Viewer/` with a committed MP3 fixture under `tests/fixtures/lumen/viewer/slideshow/` (CC0, source recorded). Done when: the class passes.
- [ ] Add `docs/user/lumen/viewer-slideshow.md` and commit captures under `docs/captures/lumen/viewer-slideshow/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: the quick slideshow in the viewer"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~QuickSlideshowListTests"` exits 0, and a driven slideshow of 20 images with an MP3 loops and then closes after the last image (Serilog lines quoted). Cheaper substitute that fails: a folder timer, which the TXT round trip and the list tests catch.

## 9. Image information, histogram, and viewer tools

"What is this file" is answered in the viewer: an information dialog, status and title fields, a histogram, pixel values, selection geometry, a develop settings summary, an editable properties pane, a byte view, QR and barcode reading, and text recognition. Rating, label, tag, caption, and keyword edits go to the catalog and, when enabled, the XMP sidecar through `D04 T01 §11`; embedding them into the original's bytes happens only through `D04 T08 §8`'s writer under `D04 T11 §1`'s `Lumen.Originals.InPlace.EmbedMetadata` opt-in, so the viewer never writes metadata into an original on its own. Custom status and title text with tokens is §18's. Catalog: LP-0101 to LP-0113 (13 features; the token form of LP-0106's custom status text is built by §18). -> SOURCE: parity-lumen-viewer-info

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-info/.
**Job:** a user answers "what is this file" and reads data from the image without leaving the viewer. Consumer: the catalog and sidecar for rating, label, tag, caption, and keyword edits.
**Treatment:** `I` for the Image Information dialog, a status strip with clickable rating, label, and tag, a histogram pane with channel toggles, a properties pane, pixel information on click with copy, Tools, Read Code, and Tools, Recognize Text. Cheaper substitute that fails the checkpoint: a file-size tooltip.
**Chrome:** consume the histogram control that `D04 T02 §3` placed in `Photon.UI`, the catalog and `D04 T01 §11`'s sidecar writer for metadata edits, and `D04 T08 §2`'s field list when it ships. Do not add a second histogram or sidecar writer.

**Requires:** display-session -- panes and dialogs are captured on screen

- [ ] Add `ImageInfo` in `src/Lumen/Photon.Lumen.Core/Viewer/Info/ImageInfo.cs` computing unique colors (cancellable), print size at the file's DPI, disk and memory size, folder index, and load time. Done when: `ImageInfoTests` count the colors of a 4,096-color fixture and the print size at 300 DPI.
- [ ] Add the Image Information dialog on `I` (LP-0109): name, folder, compression, original and current size and colors, unique colors, print size, disk and memory size, folder index, date, and load time. Done when: each field matches the fixture's known values (capture).
- [ ] Add the status strip and title fields (LP-0101, LP-0106): size, bit depth, index, zoom, file size, date, tag marker, pixel coordinates and color, selection, and the full path in the title, each toggled by a `Lumen.Viewer.Status.*` key. Done when: each key hides and shows its field (settings readback).
- [ ] Add the status-strip date choice (LP-0105): file date, EXIF date, or catalog capture time. Done when: the three choices show three dates on a fixture whose dates differ.
- [ ] Make rating, color label, and tag in the status strip clickable (LP-0101), writing the catalog and, when sidecars are enabled, the sidecar through `D04 T01 §11`, loading the catalog on first use (never at first paint). Done when: a driven rating click is read back from the catalog and the sidecar, and the original's hash is unchanged.
- [ ] Show selection origin, size, and ratio in the title while a selection exists (LP-0108). Done when: a driven selection shows its geometry in the title (capture).
- [ ] Add the histogram pane (LP-0103): R, G, B, and lightness toggles, bar or curve modes, the selection's histogram, and copying channel averages. Done when: `ImageInfoTests.Histogram` matches a numpy 2.x histogram of the fixture exactly.
- [ ] Add pixel information on click (LP-0111): coordinates, color, and palette index, with copy of the hex color and coordinates. Done when: a click on a known pixel of the palette fixture copies `#RRGGBB` and its index.
- [ ] Add the properties pane (LP-0102) reading metadata and editing caption, rating, and keywords into the catalog and sidecar, and the develop settings pane (LP-0104) listing the edit stack's non-default settings. Done when: a driven caption edit is read back from the sidecar and the develop pane lists a fixture's two changed settings.
- [ ] Add the byte view (LP-0107): a read-only HEX and ASCII view of the file with paging over 64 KiB pages. Done when: the first page of a JPEG fixture starts `FF D8 FF`.
- [ ] Add Tools, Read Code (LP-0110) through ZXing.Net 0.16 (Apache-2.0) over the displayed image or selection, results copyable, recorded as a dependency row in `docs/dev/decisions.md`. Done when: `QrReaderTests` decode a committed QR fixture's text.
- [ ] Add Tools, Recognize Text (LP-0112) through `Windows.Media.Ocr` with the installed languages, and a user-installed Tesseract run as an external process when `Lumen.Viewer.TesseractPath` is set, refused by name when absent; KADMOS is not supported and the menu says so. Done when: `OcrServiceTests` recognize a committed text fixture, skipped with a stated reason where no OCR language is installed.
- [ ] Group the utility entries above and Copy File List as the Tools menu (LP-0113), IrfanView's Tools plug-in grouping. Done when: the menu lists every tool and each opens its dialog in a driven run.
- [ ] Add `ImageInfoTests`, `QrReaderTests`, and `OcrServiceTests` in `tests/Photon.Lumen.Tests/Viewer/` with fixtures under `tests/fixtures/lumen/viewer/info/`. Done when: the classes pass.
- [ ] Add `docs/user/lumen/viewer-info.md` and commit captures under `docs/captures/lumen/viewer-info/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: image information, histogram, pixel values, codes, and text in the viewer"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ImageInfoTests|FullyQualifiedName~QrReaderTests|FullyQualifiedName~OcrServiceTests"` exits 0, and captures under `docs/captures/lumen/viewer-info/` show the information dialog, the histogram, a decoded QR fixture, and recognized text; a driven rating click is read back from the catalog with the original's hash unchanged. Cheaper substitute that fails: a tooltip, which the dialog field tests catch.

## 10. Multi-page and animated images in the viewer

Scanned documents and animations are pages and frames, not one picture. This section pages through multi-page TIFF, PDF, ICO, and DjVu files with page thumbnails and plays animated GIF, APNG, WebP, AVIF, ANI, and MNG files with frame stepping and speed, and can play a multi-page file as an animation. Viewing only: frame extraction and animation authoring stay backlog B-044, and the menu says so. Catalog: LP-0059 to LP-0061, LP-0114, LP-0972 (5 features). -> SOURCE: parity-lumen-viewer-pages

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-pages/.
**Job:** a user reads a scanned multi-page document and checks an animation frame by frame. Consumer: none: this surface is the consumer of the registry's multi-frame decoders.
**Treatment:** `Ctrl+Page Down` and `Ctrl+Page Up` for pages, a page box, a page thumbnail strip that shows itself for multi-page files, and animation controls (play, pause, step, speed) in the toolbar. Cheaper substitute that fails the checkpoint: showing page one and frame one only.
**Chrome:** consume the registry's `IMultiFrameDecoder` capability from `D04 T13 §1` and `D04 T13 §4`. Do not decode frames outside the registry.

**Requires:** display-session -- playback is observed on screen

- [ ] Add page navigation (LP-0059) in `src/Lumen/Photon.Lumen.Core/Viewer/Pages/PageNavigator.cs`: next, previous, first, last, and go to page, on `Ctrl+Page Down`, `Ctrl+Page Up`, and a page box. Done when: `PageNavigatorTests` assert page counts on the multi-page TIFF, PDF, ICO, and DjVu fixtures.
- [ ] Add the page thumbnail strip that shows itself for multi-page files (`Lumen.Viewer.AutoShowPages`) and a page view pane (LP-0059). Done when: opening the PDF fixture shows the strip and clicking page 3 shows page 3 (capture).
- [ ] Add `AnimationPlayer` in `src/Lumen/Photon.Lumen.Core/Viewer/Pages/AnimationPlayer.cs` (LP-0060, LP-0972): frame timing from the file, disposal and blending rules per format, stop, resume, and step. Done when: `AnimationPlayerTests` match per-frame goldens for GIF disposal modes and APNG blend operations.
- [ ] Add playback speed 0.25x to 4x and the toolbar controls (LP-0060). Done when: a 4x setting halves then halves again the measured frame interval in a test with a fake clock.
- [ ] Add animation on or off and "show the first frame only" (LP-0114) as `Lumen.Viewer.Animate`. Done when: the setting off shows frame one and the toolbar play starts it.
- [ ] Add Play Pages as Animation (LP-0061) with a chosen delay. Done when: the TIFF fixture's pages advance at the delay in a test with a fake clock.
- [ ] Say in the Image menu that frame extraction and animation authoring are planned in backlog B-044. Done when: the disabled entries' tooltips name B-044.
- [ ] Commit fixtures under `tests/fixtures/lumen/viewer/pages/`: a three-page TIFF, a four-page PDF, a multi-size ICO, a two-page DjVu, and GIF, APNG, animated WebP, animated AVIF, ANI, and MNG files, with per-frame goldens exported by ImageMagick 7.1 (version in `VERSION.txt`). Done when: the fixtures, goldens, and version file are committed.
- [ ] Add `PageNavigatorTests` and `AnimationPlayerTests` in `tests/Photon.Lumen.Tests/Viewer/`. Done when: both classes pass.
- [ ] Add the pages and animation section to `docs/user/lumen/viewer.md` and commit captures under `docs/captures/lumen/viewer-pages/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: multi-page and animated images in the viewer"`

**Test checkpoint:** Format fidelity proof plus unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~AnimationPlayerTests|FullyQualifiedName~PageNavigatorTests"` exits 0, every frame of the animated fixtures matches its ImageMagick 7.1 golden within 1/255 (version quoted), and a driven session steps a GIF and pages a PDF (captures). Cheaper substitute that fails: the first frame only, which the frame goldens catch.

## 11. Quick edits I: rotate, flip, select, crop, resize, and canvas

IrfanView's Image menu fixes a photo's framing and size in seconds. Every quick edit here applies the same `IBatchOperation` implementation the batch edit pipeline uses (`D04 T11 §7`) to a full-resolution working image in memory, with undo and redo, so the viewer and batch cannot disagree; the result saves through §6 as a new file by default. This section also wires the operator's 2026-09-27 opt-in ("Safe by default, opt-in writes") into the viewer: when `D04 T11 §1`'s `Lumen.Originals.InPlace.Save` is on, `Ctrl+S` on an edited image replaces the original through that section's `InPlaceWriter`, after its verified backup copy, and never through a viewer-owned write. Library rotate and flip store orientation as metadata through `D04 T11 §5`'s `OrientationCommand`, never in the original. It serves the acceptance-bar aim "Originals are never written" in its safe-by-default form. Catalog: LP-0122 to LP-0134, LP-0253 (14 features), plus the paste-into-selection options of LP-0119 that §6 hands here. -> SOURCE: parity-lumen-quick-edits-geometry

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-edit/.
**Job:** a user fixes a photo's framing and size in seconds and keeps the original untouched. Consumer: §6's Save and Save As, which write the working image.
**Treatment:** drag a selection, `Ctrl+Y` crop, `Shift+C` auto crop, `Ctrl+R` resize dialog, `Shift+V` canvas size, `Ctrl+U` fine rotation with a draw-a-line straighten, `Shift+U` auto adjust, and `Ctrl+Z` and `Ctrl+Shift+Z` with a configurable step count. Cheaper substitute that fails the checkpoint: edits applied to the decoded screen-size preview.
**Chrome:** consume `D04 T11 §7`'s `IBatchOperation` implementations and dialogs' shared controls, `D04 T11 §5`'s `OrientationCommand`, `D04 T11 §1`'s `OriginalWritePolicy` and `InPlaceWriter`, and `D01 T03 §2`. Do not implement a geometry operation or a write path to an original in the viewer.

**Requires:** display-session -- quick edits are driven in the viewer

**Freeze check:** Every quick edit changes only the in-memory working image; with every `Lumen.Originals.InPlace.*` key at its default (off), after a driven session of crop, straighten, resize, and canvas edits followed by Save and Save As over a copy of `tests/fixtures/lumen/viewer/edit/`, every original's SHA-256 and last-write time is unchanged, and library rotate and flip change only the catalog orientation and the sidecar's `tiff:Orientation`; with `Lumen.Originals.InPlace.Save` on, the viewer's Save calls only `InPlaceWriter`, whose verified backup's SHA-256 equals the original's pre-save hash. Fixture source: `tests/fixtures/lumen/viewer/edit/` (created by this section).

- [ ] Add `ViewerEditSession` in `src/Lumen/Photon.Lumen.Core/Viewer/Editing/ViewerEditSession.cs`: a full-resolution working image decoded on the first edit, an ordered list of applied `IBatchOperation` records, and undo and redo bounded by `Lumen.Viewer.UndoSteps` (default 10) (LP-0124). Done when: `ViewerEditSessionTests.UndoRestoresHash` restores the previous pixel hash after each operation.
- [ ] Add the rectangle selection (LP-0122): drag, resize with a ratio lock, move, select all, zoom into, and size from the clipboard image. Done when: `SelectionTests` assert the ratio lock and the clipboard size.
- [ ] Add ellipse, freehand, and inverted selections and the golden ratio, thirds, and fourths grids (LP-0126). Done when: the tests assert each shape's mask on a fixture.
- [ ] Add custom and maximized selections (LP-0125): exact position, size, and ratio with saved presets (`Lumen.Viewer.SelectionPresets`), maximize for popular ratios, center, and restore the last selection. Done when: `SelectionPresetTests` round-trip a preset and maximize 3:2 on a 4:3 fixture.
- [ ] Add the selection and editing options (LP-0134): selection and grid color, border thickness, grid size, auto-crop tolerance, and the cut background color, each a `Lumen.Viewer.Edit.*` key. Done when: each key is read back and applied in a capture.
- [ ] Add the selection actions (LP-0123): zoom to, copy, save as a new image through §6, print through `D04 T12 §4` once it ships (disabled with that ref until then), and set as wallpaper through §6. Done when: save-as-new writes the selection's pixels exactly.
- [ ] Add paste into a selection proportionally or at original size (LP-0119, handed from §6). Done when: a paste into a 100 by 50 selection of a 400 by 400 image yields a 50 by 50 proportional result.
- [ ] Add crop to selection, crop to the visible area, and auto crop of uniform borders with a tolerance and a preview selection (LP-0127) through `D04 T11 §7`'s crop operation. Done when: `ViewerEditSessionTests` equal the batch crop pixel for pixel.
- [ ] Add cut and cut outside with a fill color, and remove or insert strips (LP-0127). Done when: the tests assert the fill and the strip sizes.
- [ ] Add fine rotation and straighten (LP-0129): any angle, fill color, keep size or the best inner rectangle, straighten by drawing a line, on a selection, and fine-step keys. Done when: a line drawn at 3 degrees rotates by minus 3 degrees and equals the batch rotation pixel for pixel.
- [ ] Add the Resize dialog (LP-0130, LP-0131): pixels, cm, inches, percent, megapixels, standard sizes, keep aspect, saved custom sizes, every `D01 T03 §2` filter (Lanczos, Mitchell, B-spline, Bell, triangle, Hermite, Catmull-Rom, box, shrink), and gamma-correct resampling. Done when: each filter equals the batch resize pixel for pixel.
- [ ] Add resolution changes (LP-0128): change DPI with or without resampling, auto adjust DPI on resize, and resize by DPI. Done when: the saved file's DPI tag reads back as set.
- [ ] Add Canvas Size (LP-0132): per-side sizes including negative, anchor, extend to an aspect ratio, color, and saved settings. Done when: a negative left size crops that many columns.
- [ ] Add auto adjust colors from the image or selection statistics (LP-0133). Done when: the result equals the batch auto-adjust operation pixel for pixel.
- [ ] Add library rotate and flip (LP-0253) in the grid and loupe through `D04 T11 §5`'s `OrientationCommand`, storing orientation in the catalog and the sidecar's `tiff:Orientation`, honored by every render; in-place lossless JPEG rotation on opt-in is §16's. Done when: a rotation in the grid survives a catalog reopen, undoes as one step, and the original's hash is unchanged.
- [ ] When `OriginalWritePolicy` allows `Save` in place (`Lumen.Originals.InPlace.Save`, `D04 T11 §1`), make `Ctrl+S` on an edited image replace the original through `InPlaceWriter` after its first-use confirmation, show "Saved over the original (backup kept)" in the status strip, and extend §6's refusal text to name the setting ("... unless you allow it in Settings, Originals"); with the key off, Save stays §6's Save As. Done when: `ViewerSaveGuardTests.InPlaceOptIn` asserts the replaced bytes, the backup's hash, and the message with the key on, and the unchanged hash with it off. Cheaper substitute: `File.WriteAllBytes` over the original.
- [ ] Add `ViewerEditSessionTests`, `SelectionTests`, and `SelectionPresetTests` in `tests/Photon.Lumen.Tests/Viewer/` over fixtures in `tests/fixtures/lumen/viewer/edit/`, each operation compared with its `D04 T11 §7` counterpart. Done when: the classes pass.
- [ ] Add `docs/user/lumen/viewer-edit.md` (selections, crop, rotate, resize, canvas, undo, and where the result is saved) and commit captures under `docs/captures/lumen/viewer-edit/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: viewer quick edits for selection, crop, rotation, resize, and canvas"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewerEditSessionTests|FullyQualifiedName~SelectionTests|FullyQualifiedName~SelectionPresetTests|FullyQualifiedName~ViewerSaveGuardTests"` exits 0 with every operation equal to its batch counterpart pixel for pixel and the in-place Save refused with the key off and backed up with it on, and a driven crop, straighten, and resize saves a new file with the original's hash unchanged (hash table quoted). Cheaper substitute that fails: editing the display preview, which the full-resolution equality tests catch.

## 12. Quick edits II: color corrections, color depth, and palettes

IrfanView's color commands are fast corrections and conversions: brightness and contrast with profiles, grayscale and negative, channel swaps, transparency and replace color, sharpen, red and pet eye, color depth down and up with dithering, and palette editing. Each is an `IBatchOperation` from `D04 T11 §6` or `D04 T11 §7`, so the same settings run in batch, and each result saves through §6. Catalog: LP-0135 to LP-0146 (12 features). -> SOURCE: parity-lumen-quick-edits-color

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-color/.
**Job:** a user corrects or converts a photo's color and palette quickly, as in IrfanView's Image menu. Consumer: §6's Save and Save As.
**Treatment:** `Shift+G` Color Corrections dialog with live preview on the image and saved profiles, and Image menu entries for depth, grayscale, negative, swap channels, replace color, and palette. Cheaper substitute that fails the checkpoint: brightness and contrast only.
**Chrome:** consume `D01 T03 §3` quantization, `D01 T03 §4` and `D01 T03 §5` adjustments, and `D01 T07 §5`'s red-eye detector, all through `D04 T11` operations. Do not implement a color algorithm in the viewer.

**Requires:** display-session -- the dialogs are driven

- [ ] Add the Color Corrections dialog on `Shift+G` (LP-0138) with brightness, contrast, gamma, saturation, RGB balance, click-a-bright-area white balance, and live preview on the image through `ViewerEditSession`. Done when: `ColorQuickEditTests` equal the batch color operation for each slider pixel for pixel.
- [ ] Add color-correction profiles, saved values, and a dark dialog option (LP-0139) in `Lumen.Viewer.ColorProfiles`. Done when: a saved profile reapplies identically after a restart (settings readback).
- [ ] Add grayscale and negative of all or one channel (LP-0137). Done when: each variant equals its batch golden.
- [ ] Add channel swaps RBG, BGR, BRG, GRB, and GBR (LP-0144). Done when: each swap maps a pure-color fixture's channels as named.
- [ ] Add Decrease Color Depth (LP-0135): 2, 16, 256, or custom colors, black-and-white and gray palettes, the best-quality quantizer, dithering, and RGB565, through `D01 T03 §3`. Done when: a 16-color dithered result equals the `D01 T03 §3` golden.
- [ ] Add Increase Color Depth (LP-0136) to truecolor, 16-bit gray, 48-bit color, or 32-bit with alpha. Done when: the saved PNG's bit depth reads back as chosen.
- [ ] Add Set Transparent Color with tolerance and alpha intensity (LP-0140) and Replace Color with tolerance, make transparent, and a source color picked from the image (LP-0141). Done when: the tests assert the replaced pixel count within the tolerance.
- [ ] Add Sharpen with a set amount (LP-0142). Done when: it equals the batch sharpen operation pixel for pixel.
- [ ] Add red-eye reduction with gray intensity and green and yellow pet-eye variants (LP-0143) through `D01 T07 §5`. Done when: the red-eye fixture's pupil region matches the `D01 T07 §5` golden within 2/255.
- [ ] Add palette editing of indexed colors and JASC and Microsoft PAL import and export (LP-0145), with import mapping to the nearest color (LP-0146), in `src/Lumen/Photon.Lumen.Core/Viewer/Palettes/PalFile.cs`. Done when: `PalFileTests` round-trip both PAL flavors byte-equal.
- [ ] Register every command above as the named `IBatchOperation` so its settings open in the batch edit pipeline unchanged. Done when: a test serializes each dialog's settings and runs them through the batch runner with an equal result.
- [ ] Add `ColorQuickEditTests` and `PalFileTests` in `tests/Photon.Lumen.Tests/Viewer/` with fixtures and goldens in `tests/fixtures/lumen/viewer/color/`. Done when: both classes pass.
- [ ] Add `docs/user/lumen/viewer-color.md` and commit captures under `docs/captures/lumen/viewer-color/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: viewer color corrections, depth, and palettes"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ColorQuickEditTests|FullyQualifiedName~PalFileTests"` exits 0, and captures show the dialog's live preview and a 16-color dithered result saved as a new file with the original's hash unchanged. Cheaper substitute that fails: brightness and contrast only, which the per-command golden tests catch.

## 13. Quick edits IV: text, watermarks, borders, and combining images

Captioning, branding, framing, and tiling a photo should not need an editor. This section adds inserted text with placeholders and effects, image watermarks, paste-in and paste-beside collages, color highlights, speech bubbles, borders and frames, shaped crops and shadows, combining images side by side, and exporting tiles, each through `D04 T11 §8`'s overlay engine and `D04 T11 §2`'s tokens, saved through §6 or as new files. Layered editing hands off to Imago. Catalog: LP-0147 to LP-0158 (12 features). -> SOURCE: parity-lumen-quick-edits-overlays

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-overlays/.
**Job:** a user captions, brands, frames, or tiles a photo in the viewer without opening an editor. Consumer: §6's Save and Save As, and the tile and combine outputs.
**Treatment:** `Ctrl+T` or Edit, Insert Text with a preview dialog and profiles, Edit, Watermark with click-to-place, Image, Add Border, Image, Combine Side by Side, and Image, Export Tiles. Cheaper substitute that fails the checkpoint: text without placeholders or preview.
**Chrome:** consume `D04 T11 §8`'s text and watermark engine and `D04 T11 §2`'s tokens. Do not add a second text renderer.

**Requires:** display-session -- the dialogs are driven

- [ ] Add the Insert Text dialog on `Ctrl+T` (LP-0147) in `src/Lumen/Photon.Lumen.Viewer/Editing/InsertTextDialog.xaml`: at a click or in a selection, multi-line with tokens and tabs, font, size, style, color, alignment, rotation, antialiasing, and a transparent or colored box, rendered by `D04 T11 §8`. Done when: `OverlayQuickEditTests.TextTokens` render `$F` and `{name}` as the fixture's file name.
- [ ] Add the Insert Text extras (LP-0151): adjust font to zoom, add canvas above or below for the text, shadow and outline, live preview, profiles, `Ctrl`-click stamping, and pick color from the image. Done when: a stamped `Ctrl`-click series places three captions (capture).
- [ ] Add Watermark (LP-0148): corner and offset or center, click to place with preview, transparency, keeping PNG and GIF alpha, and from the selection, through `D04 T11 §8`. Done when: `OverlayQuickEditTests.WatermarkAlpha` keeps the watermark PNG's alpha in the result.
- [ ] Add Paste In (LP-0149), movable and resizable before applying, keeping the selection. Done when: a pasted image moved and resized lands at the final rectangle pixel for pixel.
- [ ] Add paste special on a side for simple collages with a paste counter for names (LP-0150). Done when: pasting right of a 400-wide image yields an 800-wide canvas.
- [ ] Add a color highlight on an area (LP-0152) and speech bubbles (LP-0155). Done when: each equals its batch operation golden.
- [ ] Add shaped crops and shadows (LP-0156): drop shadow, rounded corners, star, heart, cloud, hexagon, and snowflake. Done when: each shape's alpha mask matches its golden.
- [ ] Add borders and frames (LP-0154): up to four parts, presets, inside fading, broken edge and lines, and on a selection. Done when: a four-part frame's outer size equals the image plus the four widths.
- [ ] Add Combine Side by Side (LP-0153, LP-0158) in `src/Lumen/Photon.Lumen.Core/Viewer/Combine/ImageCombiner.cs`: horizontal or vertical, spacing, file-name labels, and a tiled grid, from the viewer list or a library selection, writing a new file through §6's Save As, and register its Explorer context verb beside §3's verbs. Done when: `OverlayQuickEditTests.CombineDimensions` asserts the combined size with spacing.
- [ ] Add Export Tiles (LP-0157): count or size, spacing, all pages, format, and folder, writing new files through `AtomicFileWriter` and refusing an existing name unless the user chose overwrite for tiles. Done when: `TileExportTests` write a 3 by 2 grid of the expected sizes.
- [ ] Add `OverlayQuickEditTests` and `TileExportTests` in `tests/Photon.Lumen.Tests/Viewer/` with fixtures in `tests/fixtures/lumen/viewer/overlays/`. Done when: both classes pass.
- [ ] Add `docs/user/lumen/viewer-overlays.md` and commit captures under `docs/captures/lumen/viewer-overlays/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: viewer text, watermarks, borders, and combined images"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~OverlayQuickEditTests|FullyQualifiedName~TileExportTests"` exits 0, and captures show a captioned, watermarked, framed photo and a side-by-side combination saved as new files with the originals' hashes unchanged. Cheaper substitute that fails: fixed text, which the token test catches.

## 14. Viewer window and display options

Some users want IrfanView's minimal window and others ACDSee's panels. This section completes the viewer window's layout, chrome, background, transparency display, display resampling quality, sizing and placement, channel view, grid overlay, always-on-top, and boss key, each a setting. It depends on §5 as well as §4 because the filmstrip shows §5's folder list, so it runs after §5 in Phase 30. Catalog: LP-0062 to LP-0075 (14 features). -> SOURCE: parity-lumen-viewer-window

**Fidelity:** docs/captures/lumen/viewer/ (baseline from §1); new captures to docs/captures/lumen/viewer-display/.
**Job:** a user shapes the viewer into a minimal IrfanView-style window or a panelled ACDSee-style one. Consumer: the viewer window, which reads every key at startup and on change.
**Treatment:** a bottom toolbar with icon sizes and add or remove buttons, an optional filmstrip, hide menu or caption permanently or per session (`Shift+Enter`), a thin border, a background color, tiled image, or theme color, checkerboard transparency, fit window to image or desktop, remember size and position, and one channel on `Shift+R`, `Shift+G`, `Shift+B`, `Shift+A`. Cheaper substitute that fails the checkpoint: a fixed window.
**Chrome:** consume `Photon.UI` theme resources for every color and size and `D01 T03 §2` for display resampling. Do not hardcode a color, size, or spacing the theme names.

**Requires:** display-session -- window layouts are captured on screen

- [ ] Add the bottom toolbar (LP-0062) with small, medium, and large icon sizes and a Customize Toolbar dialog adding and removing buttons, in `Lumen.Viewer.Toolbar.*`. Done when: a removed button stays removed after a restart (settings readback).
- [ ] Add the filmstrip over §5's `FolderFileList` and hiding the bottom panels (LP-0062). Done when: the filmstrip scrolls with next and previous in a driven run.
- [ ] Add chrome options (LP-0068): hide the menu or caption permanently or per session on `Shift+Enter`, hide the toolbar, and a thin border. Done when: each combination is captured.
- [ ] Add the right-button choice (LP-0069): context menu or scroll. Done when: the setting switches the behavior in a driven run.
- [ ] Add the background (LP-0065, LP-0066): default theme color, a custom color, a tiled image, or the main window color, and image centering. Done when: each choice is captured, with the default color read from the theme.
- [ ] Add transparency display (LP-0074): checkerboard, window color, or discard, including non-animated GIF transparency. Done when: `ViewerWindowSettingsTests.Checkerboard` finds the checker pattern under a transparent PNG fixture's transparent pixels.
- [ ] Add display resampling quality (LP-0064): smooth fit and zoom (Lanczos downscale through `D01 T03 §2`), show pixels above 100 percent, sharpen subsampled display, and refresh with resample after a 300 ms pause. Done when: the capture pair shows smooth and pixel display of one fixture.
- [ ] Add window sizing (LP-0073): fit window to image, fit to desktop, desktop width, height, or smaller side, and only for big images. Done when: each mode's window rectangle is asserted in `ViewerWindowSettingsTests`.
- [ ] Add placement (LP-0075): center on load, and remember size and position per monitor. Done when: a moved window reopens at the same place on the same monitor.
- [ ] Add always on top (LP-0063, `Lumen.Viewer.AlwaysOnTop`) and the boss key that minimizes and hides the viewer (LP-0067). Done when: both work in a driven run.
- [ ] Add a fixed grid overlay with spacing and color (LP-0070) and Clear Display that keeps the file list (LP-0071). Done when: the grid is captured and Clear Display then next shows the next image.
- [ ] Add the single-channel view in color or gray on `Shift+R`, `Shift+G`, `Shift+B`, and `Shift+A` (LP-0072) as a display transform. Done when: the red view of a pure-green fixture is black and nothing is written.
- [ ] Add `ViewerWindowSettingsTests` in `tests/Photon.Lumen.Tests/Viewer/` asserting each setting persists and applies. Done when: the class passes.
- [ ] Add the window and display section to `docs/user/lumen/viewer.md` and commit captures of the minimal and panelled layouts under `docs/captures/lumen/viewer-display/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: viewer window, chrome, and display options"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewerWindowSettingsTests"` exits 0, and captures under `docs/captures/lumen/viewer-display/` show the minimal and panelled layouts, the checkerboard, and a single-channel view. Cheaper substitute that fails: a fixed layout, which the settings round trip catches.

## 15. Quick edits III: the effects browser and viewer effects

IrfanView's effects browser lets a user try effects with a preview and one value each. Lumen adds no effect algorithm of its own: the browser lists the `Photon.Core` effect registry (`D01 T03`, `D01 T06`) by category, applies the chosen one through `D04 T11 §7`'s `EffectOperation`, and adds local contrast enhancement, curves, film simulation from CLUT files, and Auto Lens preview-through-a-filter while browsing. Film simulation reads `.cube` files through `D03 T11 §4`'s LUT readers in `src/Photon.Core/Imaging/Luts/` (Phase 18) rather than the develop LUT stage `D01 T07 §9`, which runs in Phase 36, after this section.  IrfanView also runs third-party Photoshop 8BF and Filter Factory filters from its effects menu and ACDSee lists Photoshop plug-in folders; those run through the suite plug-in host (`D01 T09 §2` in its isolated process, folders and status in `D01 T09 §4`'s manager), promoted from the former backlog entry B-012 by the operator's 2026-09-27 decision, never through a Lumen-private loader. Catalog: LP-0076, LP-0159 to LP-0168, LP-1157, LP-1159, LP-1224 (14 features). -> SOURCE: parity-lumen-quick-edits-effects

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/viewer-effects/.
**Job:** a user tries effects on a photo with a preview and saves the one they like. Consumer: §6's Save and Save As; Auto Lens is view-only.
**Treatment:** a resizable Effects Browser with a category list, before and after preview, a value slider per effect, and apply to the selection or the whole image; Image, Curves; an Auto Lens toggle in the toolbar. Cheaper substitute that fails the checkpoint: a menu of effects with fixed values and no preview.
**Chrome:** consume the effect registry of `D01 T03` and `D01 T06`, `D01 T03 §4`'s `ToneCurve`, `D03 T11 §4`'s LUT readers and color lookup, and the plug-in host client and manager of `D01 T09 §2` and `§4`. Do not add an algorithm or a plug-in loader to Lumen.

**Requires:** display-session -- the effects browser is driven

- [ ] Add `EffectsBrowserViewModel` in `src/Lumen/Photon.Lumen.Viewer/Effects/EffectsBrowserViewModel.cs` (LP-0159) listing registry entries by category with one primary value each and a preview on a downscaled copy, applied through `EffectOperation`. Done when: `EffectsBrowserTests.EveryIdResolves` resolves every listed id in the registry.
- [ ] Map the blur effects (LP-0160: blur, Gaussian, fast Gaussian, total variation, radial, zoom, motion, tilt-shift) to their registry ids. Done when: each id resolves and previews.
- [ ] Map the sharpen effects (LP-0161: sharpen, unsharp mask) and the tone and noise effects (LP-0163: median, add noise, sepia, color temperature, histogram equalize and stretch, chromatic aberration, radial brighten). Done when: each id resolves and previews.
- [ ] Map the stylize effects (LP-0162: 3D button, emboss, oil paint, edge detection, find edges, explosion, pixelize, fragment, solarize, metallic gold and ice, rock, stained glass, blinds) and the distort effects (LP-0164: rain drops, swirl, twirl, fish eye, cylinder, circular waves, horizontal and vertical shift, skew). Done when: each id resolves, and any the registry lacks is filed through `add-todo` against `D01 T06` with the gap named, never written in Lumen.
- [ ] Add local contrast enhancement (LP-0165) through the registry's local contrast (CLAHE-style) effect with strength and scale, not the AltaLux plug-in. Done when: it equals the registry effect's golden.
- [ ] Add Image, Curves (LP-0167): an RGB and per-channel curve dialog over `D01 T03 §4`'s `ToneCurve`. Done when: an S-curve's output on a gray ramp equals the `ToneCurve` evaluation.
- [ ] Add film simulation (LP-0166, LP-0168) reading `.cube` files through `D03 T11 §4`'s readers and Hald CLUT PNGs through a `HaldClutReader` added beside them in `src/Photon.Core/Imaging/Luts/`, applied through the shared color lookup; users add their own CLUT packs under `%LOCALAPPDATA%\Rizonesoft\Lumen\LUTs\` and none are bundled. Done when: a level-8 identity Hald CLUT leaves a fixture unchanged within 1/255 and a sepia `.cube` matches its golden.
- [ ] Add Auto Lens (LP-0076): a view-only filter chosen from the browser applied to every displayed image while browsing, persisting until turned off, never saved. Done when: browsing three images with Auto Lens shows the filter and every file's hash is unchanged.
- [ ] Add a Plug-in Filters category to the effects browser and Image, Plug-in Filters menu (LP-1157) that lists the 8BF and Filter Factory filters `D01 T09 §2`'s `PluginScanner` found, runs the chosen one on the viewer image (or the selection as `maskData`) through `PluginHostClient`, including 32-bit filters in the x86 host, with the filter's own dialog parented to the viewer window, one undo step, and Repeat Last Filter from the stored `FilterParameterBlob`. Done when: `ViewerPluginFilterTests` run the committed invert test filter from `tests/fixtures/plugins/filters/` on a fixture exactly, and killing the host mid-filter leaves the viewer running and the image unchanged. Cheaper substitute: loading the DLL in `LumenViewer.exe`, which the kill test cannot survive.
- [ ] Add the plug-in folders (LP-1159, LP-1224): Options, Plug-ins opens `D01 T09 §4`'s plug-in manager in Lumen with the keys `Lumen.Plugins.Folders` (default empty) and `Lumen.Plugins.AllowUnknown` (default off), shared by the viewer and the library app through the settings store, and a failing plug-in is disabled with the manager's message naming it. Done when: a settings readback lists an added folder and the manager shows the committed test plug-ins with their support status.
- [ ] Ship the isolated host with Lumen: add the `PluginHost` publish item `D01 T09 §1` defined to `Photon.Lumen.Viewer` and `Photon.Lumen.Desktop`, so the Lumen install and portable ZIP carry their own x64 and x86 `Photon.PluginHost.exe` and depend on no other app. Done when: `pwsh scripts/publish.ps1 -App Lumen` output contains both host builds.
- [ ] Add `EffectsBrowserTests` in `tests/Photon.Lumen.Tests/Viewer/`: every listed id resolves, and the preview and the full-size apply agree within 1/255 after scaling. Done when: the class passes.
- [ ] Add `docs/user/lumen/viewer-effects.md` and commit captures under `docs/captures/lumen/viewer-effects/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: the effects browser, curves, film simulation, and Auto Lens in the viewer"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~EffectsBrowserTests|FullyQualifiedName~ViewerPluginFilterTests"` exits 0, and captures show the browser preview, a third-party 8BF filter's dialog over the viewer (filter named with its version), and an Auto Lens session with every file's hash unchanged. Cheaper substitute that fails: fixed-value effects with no preview, which the preview agreement test exposes.

## 16. Lossless JPEG transforms to new files, or in place on opt-in

Rotating or cropping a JPEG by decoding and re-encoding loses quality; jpegtran-style transforms move DCT blocks and lose nothing. `D04 T11 §5` builds the one `LosslessJpegTransform` wrapper over libjpeg-turbo 3.1's `tjTransform` and the `OrientationCommand` earlier in Phase 31 so neither is built twice; this section brings them to the viewer, the grid, and a dialog with every jpegtran option. By default the toolbar and grid rotate store orientation as metadata and "Lossless transform to a new file" writes beside the original; under the operator's 2026-09-27 decision "Safe by default, opt-in writes", a user who turns on `D04 T11 §1`'s `Lumen.Originals.InPlace.Rotate` gets ACDSee's and IrfanView's in-place lossless rotation and crop, replaced only through that section's `InPlaceWriter` after its verified backup copy. Catalog: LP-0169 to LP-0174 (6 features). -> SOURCE: parity-lumen-lossless-jpeg

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/lossless-jpeg/.
**Job:** a user rotates or crops JPEGs without any recompression loss and without risking the camera file unless they chose to. Consumer: the new JPEG, the catalog orientation, or the original through `InPlaceWriter` on opt-in.
**Treatment:** toolbar rotate buttons store orientation by default; Image, Lossless Transform opens a dialog (transform, perfect or trim, optimize, progressive, markers keep, clean, or choose, update EXIF thumbnail and DPI, keep ICC, file date from EXIF) writing `<name>-rotated.jpg` or a chosen name, with "Apply to the original file (a backup copy is kept)" shown only when the in-place setting allows it. Cheaper substitute that fails the checkpoint: decode, rotate, and re-encode.
**Chrome:** consume `D04 T11 §5`'s `LosslessJpegTransform` and `OrientationCommand` and `D04 T11 §1`'s `OriginalWritePolicy` and `InPlaceWriter`. Do not write a second JPEG transform or a second write path to an original.

**Requires:** display-session -- the dialog is driven

**Freeze check:** With `Lumen.Originals.InPlace.Rotate` at its default (off), every command here writes a new file or changes only the catalog and sidecar orientation, a transform whose output path equals its input path is refused before any file is opened for writing, and after every transform on a copy of `tests/fixtures/lumen/viewer/lossless/` each original's SHA-256 and last-write time is unchanged; with the key on, the in-place transform calls only `InPlaceWriter`, whose verified backup's SHA-256 equals the pre-transform hash. Fixture source: `tests/fixtures/lumen/viewer/lossless/` (created by this section).

- [ ] Add `ViewerLosslessService` in `src/Lumen/Photon.Lumen.Core/Viewer/Lossless/ViewerLosslessService.cs` running `D04 T11 §5`'s `LosslessJpegTransform` for rotate 90, 180, and 270, flip horizontal and vertical, transpose, transverse, and perfect or trim edges from the viewer (LP-0171). Done when: `ViewerLosslessTests` compare each output's DCT coefficients with a jpegtran 3.1 golden exactly.
- [ ] Add MCU-aligned crop to the viewer's selection with the output file and the EXIF thumbnail updated (LP-0173). Done when: the crop's dimensions snap to the MCU grid and the coefficients match jpegtran's `-crop` golden.
- [ ] Add the dialog's options (LP-0172): optimize, progressive, JFIF marker, keep, clean, or choose markers, update the EXIF thumbnail, DPI, and ICC profile, and the output file date from EXIF or kept, extending `LosslessJpegTransform`'s options record in place where it lacks one. Done when: each option's effect on the output's markers is asserted with the input unchanged.
- [ ] Refuse an output path equal to the input path before opening anything for writing unless the call comes through `InPlaceWriter`. Done when: `ViewerLosslessTests.SamePathRefused` asserts the refusal and the unchanged hash.
- [ ] Make the viewer's and grid's toolbar rotate (LP-0169, LP-0170) run `OrientationCommand` by default, and add "Lossless transform to a new file" writing `<name>-rotated.jpg` beside the original, with flip on a selection. Done when: the default rotate changes only the catalog and sidecar and the new-file command writes the rotated JPEG.
- [ ] Add auto rotate by EXIF and orientation reset (LP-0171) acting on the new file by default. Done when: auto rotate of an orientation-6 fixture writes an orientation-1 JPEG whose pixels equal the displayed original.
- [ ] Add EXIF date edit, clean metadata, and thumbnail update (LP-0174) applied to the new file by default. Done when: the new file carries the edited date and the original is unchanged.
- [ ] When `OriginalWritePolicy` allows `Rotate` in place (`Lumen.Originals.InPlace.Rotate`), show "Apply to the original file (a backup copy is kept)" in the dialog and make the toolbar rotate transform JPEGs losslessly in place (clearing the stored orientation), each through `InPlaceWriter` after its first-use confirmation. Done when: `ViewerLosslessTests.InPlaceOptIn` asserts the replaced coefficients, the backup's hash, and the cleared orientation with the key on, and the unchanged hash with it off. Cheaper substitute: transforming straight over the original.
- [ ] Wire §3's Explorer Lossless rotate verb to the same service and policy. Done when: the verb writes a new file by default in a driven run.
- [ ] Add `ViewerLosslessTests` in `tests/Photon.Lumen.Tests/Viewer/` with fixtures and jpegtran 3.1 goldens (version in `VERSION.txt`) in `tests/fixtures/lumen/viewer/lossless/`. Done when: the class passes and every input hash is unchanged after the default cases.
- [ ] Add `docs/user/lumen/lossless-jpeg.md` (what lossless means, new file versus the in-place setting, the backup) and commit captures under `docs/captures/lumen/lossless-jpeg/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: lossless JPEG transforms in the viewer, to new files or in place on opt-in"`

**Test checkpoint:** Format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewerLosslessTests"` exits 0 with coefficient-level equality to the jpegtran 3.1 goldens (version quoted) for every transform and crop, the unchanged-input hash for every default case, and the in-place case's backup hash equal to the pre-transform hash. Cheaper substitute that fails: decode and re-encode, which the coefficient comparison catches.

## 17. Resident quick-start mode

IrfanView users who want the very fastest open keep the program loaded. This optional mode (off by default) starts Lumen Viewer hidden at sign-in and forwards later opens to it through `D01 T02 §3`'s single-instance pipe, with a notification-area icon; the budget is a hard gate: a forwarded open reaches its first frame within 100 ms. It was split from §1 at authoring so neither section is packed. It must say how much memory it holds and leave no trace when turned off. Catalog: LP-0003 (1 feature, moved from §1's range at authoring). -> SOURCE: parity-lumen-viewer-resident

**Fidelity:** docs/captures/lumen/viewer/ (baseline from §1); new captures to docs/captures/lumen/viewer-resident/.
**Job:** a user who opens images all day turns on "Keep Lumen Viewer ready" and every open is instant. Consumer: the `HKCU` Run key and the resident process, which read the setting.
**Treatment:** a settings toggle "Keep Lumen Viewer ready" with the measured idle memory stated beside it, a notification-area icon with Open, Settings, and Exit, and a hidden window that shows on each forwarded open. Cheaper substitute that fails the checkpoint: a Run-key launch of a normal window, which is visible at sign-in and still pays the cold start.
**Chrome:** consume `D01 T02 §3`'s `SingleInstance`, the `Photon.UI` theme, and the settings store. Do not use `System.Windows.Forms.NotifyIcon` (it loads WinForms at startup).

**Requires:** display-session -- the resident hand-off is timed on screen and the notification-area icon is driven

- [ ] Add `Lumen.Viewer.StayResident` (default off) that registers `"<install>\LumenViewer.exe" --resident` as the `LumenViewer` value under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` when turned on and removes it when turned off. Done when: `ResidentRegistrationTests` over the redirected registry root show the value appear and disappear.
- [ ] Start with `--resident` into a hidden window with the decode service warm and the single-instance server listening. Done when: a `--resident` launch shows no window and `ViewerStartupTests` can forward to it.
- [ ] Add `NotifyIconHost` in `src/Lumen/Photon.Lumen.Viewer/Tray/NotifyIconHost.cs` over `Shell_NotifyIconW` P/Invoke with Open, Settings, and Exit, re-adding the icon on the `TaskbarCreated` message. Done when: the icon survives an Explorer restart in a driven run.
- [ ] Show the image on a forwarded open and hide instead of exiting on close while resident; Exit from the icon ends the process and closes the pipe. Done when: after Exit, the next open is a cold start (trace quoted).
- [ ] Measure the resident process's idle working set after 60 seconds and record it in `docs/dev/lumen/viewer-budgets.md`, and show "Uses about {N} MB while waiting" beside the toggle from that measurement. Done when: the page and the toggle state the same figure.
- [ ] Add `ResidentHandoffTests` to the startup harness timing a forwarded open of the 24-megapixel fixture from the pipe write to the first rendered frame, five runs. Done when: the test prints the median and fails over 100 ms.
- [ ] Log one Information line when resident mode starts and stops and per forwarded open. Done when: a driven session's log shows the three lines.
- [ ] Add `ResidentRegistrationTests` in `tests/Photon.Lumen.Tests/Viewer/`. Done when: the class passes and deletes its registry root.
- [ ] Add the resident mode paragraph to `docs/user/lumen/viewer.md` and commit captures of the toggle and the icon menu under `docs/captures/lumen/viewer-resident/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: the resident quick-start mode of the viewer"`

**Test checkpoint:** Driven run with evidence plus unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ResidentHandoffTests|FullyQualifiedName~ResidentRegistrationTests"` exits 0 on the reference machine, and the stamp quotes the hard gate: a forwarded open reaches its first frame in at most 100 ms (median of five); turning the setting off leaves no Run value (reg query quoted). Cheaper substitute that fails: a Run-key launch of a visible normal window, which the hidden-start assertion and the 100 ms gate catch.

## 18. Captions and info text through the token engine

Fullscreen info text, header and footer captions, the quick slideshow's info text, and the custom status and title text all fill placeholders (`$F`, `{name}`, EXIF fields) the way IrfanView does. Lumen has one token engine (`D04 T11 §2`), which ships in Phase 31 after §7, §8, and §9, so these were split into this section at authoring rather than growing a second, smaller placeholder engine in the viewer. It runs in Phase 31 after `D04 T11 §2`. Captions are drawn over the display and never modify the file. Catalog: LP-0078, LP-0084 (2 features), plus the placeholder info text of LP-0097 (from §8) and the custom status text of LP-0106 (from §9). -> SOURCE: parity-lumen-viewer-captions

**Fidelity:** docs/captures/lumen/viewer-fullscreen/ (baseline from §7); new captures to docs/captures/lumen/viewer-captions/.
**Job:** a user shows the file name, date, and exposure over the image in fullscreen, a slideshow, or the status strip, with the fields they choose. Consumer: none: this surface is the consumer of the token engine.
**Treatment:** a Captions page with header, footer, and info text fields using the token editor of `D04 T11 §2`, font, box color or transparent, position, alignment, and a toggle key; the slideshow dialog's info text field; and the status strip's custom text field. Cheaper substitute that fails the checkpoint: fixed text with no placeholders.
**Chrome:** consume `D04 T11 §2`'s token engine and editor and §7's fullscreen renderer. Do not add a second placeholder parser.

**Requires:** display-session -- captions are captured over fullscreen and the slideshow

- [ ] Add `CaptionOverlay` in `src/Lumen/Photon.Lumen.Viewer/Fullscreen/CaptionOverlay.cs` rendering header, footer, and info text over the displayed image from token templates evaluated by `D04 T11 §2` for the current file. Done when: `CaptionOverlayTests` render `$F` and `{exif.exposure}` as the fixture's values.
- [ ] Add header and footer captions (LP-0078): text, alignment, font, background color, and show or hide, in `Lumen.Viewer.Captions.*`. Done when: each key is read back and applied in a capture.
- [ ] Add fullscreen info text (LP-0084): font, box color or transparent, position, and a toggle key. Done when: the toggle key shows and hides it in a driven run.
- [ ] Add the slideshow's info text with placeholders (LP-0097, from §8) to the Slideshow dialog, drawn by `CaptionOverlay`. Done when: a driven slideshow shows each image's name and date.
- [ ] Add custom status and title text with tokens (LP-0106, from §9), evaluated on image change. Done when: a custom status `{index}/{count} {name}` shows `3/20 IMG_0003.JPG` on the fixture folder.
- [ ] Re-evaluate captions only on image change and cache them, keeping next-image navigation within §2's budget. Done when: `ViewerNavigationTimingTests` still pass with captions on.
- [ ] Assert captions never write to the file, the catalog, or the sidecar. Done when: `CaptionOverlayTests.NoWrites` finds every hash unchanged after a session.
- [ ] Add `CaptionOverlayTests` in `tests/Photon.Lumen.Tests/Viewer/`. Done when: the class passes.
- [ ] Add the captions section to `docs/user/lumen/viewer.md` and commit captures under `docs/captures/lumen/viewer-captions/`. Done when: the page and captures exist.
- [ ] Commit: `"lumen: viewer captions and info text through the token engine"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~CaptionOverlayTests|FullyQualifiedName~ViewerNavigationTimingTests"` exits 0 with the navigation budgets still met, and captures show header, footer, and info text in fullscreen and a slideshow. Cheaper substitute that fails: fixed caption text, which the token rendering test catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Lumen.Tests.Viewer"` exits 0 with every class named in this file reporting
- [ ] The startup harness on the reference machine meets every budget in `docs/dev/lumen/viewer-budgets.md` (cold 450 ms, warm 250 ms, resident 100 ms, next image 50 ms cached and 150 ms uncached, RAW preview 200 ms, working set 200 MB), medians quoted
- [ ] The freeze checks of §6, §11, and §16 pass: with every `Lumen.Originals.InPlace.*` key at its default every fixture original is byte-identical after a full viewer session, and the opt-in Save and rotation go only through `D04 T11 §1`'s `InPlaceWriter`
- [ ] `python scripts/todo-graph.py query parity --catalog lumen --phase 30` and `--phase 31` report every row planned to this file owned by a stamped section
- [ ] `python scripts/todo-graph.py validate` clean
