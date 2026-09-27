---
schema_version: 1
id: lumen-parity-import
domain: 04-lumen
status: draft
title: "TODO-07 -- Lumen Parity: Import, Devices, and Capture"
depends_on: []
frozen: true
track: L7
---

# TODO-07 -- Lumen Parity: Import, Devices, and Capture

> **Goal:** Lumen's import reaches Lightroom Classic, ACDSee, and IrfanView parity on top of `D04 T01 §6`'s safe add and copy: a full import window with sources, a candidate grid, Move mode, and new-only and duplicate filters; previews and smart previews built on import, a hash-verified second copy, renaming through the suite token engine, and destination organization; presets and everything applied during import, with metadata going to sidecars by default and into the imported files only when the user turned embedding on; phones and cameras over Windows Portable Devices and AutoPlay; auto import from watched folders as the tethered-shooting path (tethered capture proper stays backlog B-048); Copy as DNG and Convert to DNG; scanning through WIA and TWAIN with IrfanView's batch scanning and Copy Shop; and a screen capture utility. Browsing a folder without importing it (`D04 T05 §1`) stays the default way to see photos where they are; import is for cards, devices, copies, and organizing. The code lives in `src/Lumen/Photon.Lumen.Core/Import/`, `Devices/`, `Acquire/`, and `Capture/`, and `src/Lumen/Photon.Lumen.Desktop/Import/`; every path keeps the original-file guard as the operator's 2026-09-27 decision shapes it: a source is removed only after a hash-verified copy, and only into the Recycle Bin.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Lumen has no code: `src/Lumen` does not exist. Import is planned in `todo/04-lumen/TODO-01-lumen-foundation.md` (`D04 T01 §6`: Add or Copy, SHA-256 verified copies, duplicate skip, the `yyyy/yyyy-MM-dd` folder pattern, and MetadataExtractor for EXIF during import), and its Freeze check is where Lumen's original-file guard joins the frozen set. Imago's parity plan already moves Nodus's `WiaAcquireService` into `src/Photon.Core/Acquire/` and adds screenshots through `Windows.Graphics.Capture` in `todo/03-imago/TODO-17-imago-parity-formats.md` (`D03 T17 §12`), recording TWAIN as unsupported for Imago; §7 consumes the moved WIA service as its third consumer and adds TWAIN for Lumen, and §8 moves the screenshot code to `Photon.Core` on its second consumer. **Corrected 2026-09-27 (authoring):** the design had §7 move the WIA code out of Imago; `D03 T17 §12` already places it in `Photon.Core`, so §7 consumes it. Tethered capture has no backlog entry until the integration commit adds B-048. Checklist paths name the projects `D04 T01 §2` creates.
<!-- claim: absent src/Lumen -->
<!-- claim: count "yyyy/yyyy-MM-dd" todo/04-lumen/TODO-01-lumen-foundation.md = 1 -->
<!-- claim: count "MetadataExtractor" todo/04-lumen/TODO-01-lumen-foundation.md = 1 -->
<!-- claim: count "class WiaAcquireService" todo/03-imago/TODO-17-imago-parity-formats.md = 2 -->
<!-- claim: count "Windows\.Graphics\.Capture" todo/03-imago/TODO-17-imago-parity-formats.md = 1 -->

## Inputs

- [`docs/parity/lumen-parity.md`](../../docs/parity/lumen-parity.md) -- the catalog rows each section owns (`LP-` ranges named in each context paragraph)
- [`docs/parity/lumen-section-design.md`](../../docs/parity/lumen-section-design.md) -- the design these sections were authored from ("Tethered capture: evaluated, deferred to B-048", "Formats and licensing")
- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard; import copies are hash-verified
- [`standards/shared.md`](../../standards/shared.md) -- atomic writes, logging, progress and cancel, and the performance budgets
- Operator decision, 2026-09-27: "Safe by default, opt-in writes" -- metadata goes to sidecars by default, settings embed it into originals (XMP, IPTC, EXIF) as ACDSee does through the suite atomic writer with an optional backup copy, and import copies and moves honor the same rule; §3 applies it through `D04 T08 §9`
- Operator decision, 2026-09-27: tethered capture stays backlog B-048, and the watched-folder auto import of §5 covers tethered workflows through the camera maker's own tether utility
- Windows Portable Devices API (`IPortableDeviceManager`, `IPortableDeviceContent`, `IPortableDeviceResources`, `WPD_OBJECT_ORIGINAL_FILE_NAME`), AutoPlay handler registration (`EventHandlers`, `ShowPicturesOnArrival`, `MixedContentOnArrival`), and `CM_Request_Device_Eject` on Microsoft Learn -- §2 and §4
- TWAIN 2.5 specification and NTwain (MIT) over the TWAIN data source manager the scanner driver installs (never bundled) -- §7
- Adobe DNG Specification 1.7.1.0 and Adobe `dng_validate` as an oracle only -- §6
- -> XREF: D04 T02 §8 -- Lumen 0.1.0 ships before every section here
- -> XREF: D04 T01 §6 -- the import planner and runner every section extends, and the Freeze check this file keeps
- -> XREF: D04 T01 §7 -- previews built on import (§2)
- -> XREF: D04 T02 §5 -- develop presets applied during import (§3)
- -> XREF: D04 T05 §1 -- browsing without importing, the default this import sits beside
- -> XREF: D04 T05 §3 -- the folder tree where §4's device folders appear
- -> XREF: D04 T06 §5 -- collections §3 adds imported photos to
- -> XREF: D04 T06 §6 -- categories §3 applies during import
- -> XREF: D04 T06 §8 -- Import to This Folder and the previous-import entries §1 feeds
- -> XREF: D04 T06 §11 -- smart previews built on import (§2)
- -> XREF: D04 T08 §3 -- metadata presets applied during import (§3)
- -> XREF: D04 T08 §5 -- keywords applied during import (§3)
- -> XREF: D04 T08 §9 -- the opt-in embedder §3 routes metadata through for imported copies and files added in place
- -> XREF: D04 T11 §1 -- `OriginalWritePolicy`'s `Lumen.Originals.InPlace.EmbedMetadata` setting and `InPlaceWriter` backup rule that §3's embedding honors
- -> XREF: D04 T11 §2 -- the token engine for renaming on import (§2), scan names (§7), and capture names (§8)
- -> XREF: D04 T13 §5 -- RAW+JPEG pairs §2 keeps linked
- -> XREF: D04 T13 §6 -- the TIFF and PDF writers §7's multi-page scans use
- -> XREF: D04 T13 §7 -- the DNG writer for Copy as DNG and Convert to DNG (§6)
- -> XREF: D03 T17 §12 -- the WIA acquire service §7 consumes and the screenshot code §8 moves to `Photon.Core/Capture/`
- -> XREF: D03 T18 §6 -- the `Photon.UI/Print/` print dialog frame §7's Copy Shop prints through
- -> XREF: D04 T12 §4 -- the print module that replaces Copy Shop's printing path when it ships
- -> XREF: D04 T15 §5 -- `lumen-v0.6.0` releases this file's phase

## Outcome

- The import window lists cards, drives, devices, network folders, and discs, shows a checkable candidate grid with new-only and duplicate filters, and imports in Add, Copy, Move, or Copy as DNG mode.
- Move and every "remove the source" path send a source to the Recycle Bin only after its copy's SHA-256 matches; a corrupted copy leaves the source in place.
- Imports build previews and smart previews, write a hash-verified second copy, rename through the suite token engine, and organize destinations by folder, date, or source structure.
- Develop presets, metadata presets, keywords, categories, and collections apply in the import transaction; metadata lands in sidecars by default and is embedded into the imported copies only when the user enabled embedding.
- Phones and cameras import over Windows Portable Devices without a drive letter, and AutoPlay offers Lumen.
- A watched folder imports each file after its writer closes it, which is how a studio photographer shoots tethered through a camera maker's utility.
- Raw files convert to DNG with Lightroom's options, and the catalog switches to the DNG only after it validates.
- Scanners acquire through WIA and TWAIN, batch scans name and number pages, and Copy Shop prints copies; the screen capture utility saves named captures into the library.

**Adjacency:** list=applicable @ D04 T07 §1; document=applicable @ D04 T07 §7; settings=applicable @ D04 T07 §3; reporting=applicable @ D04 T07 §2; notifications=applicable @ D04 T07 §4; permissions=applicable @ D04 T07 §1; audit=applicable @ D04 T07 §1; exchange=applicable @ D04 T07 §6; reverse=applicable @ D04 T07 §1

**Adjacency rationale:** The source panel and candidate grid (§1) are the lists, with device lists (§4) and scan sources (§7) beside them. Copy Shop (§7) is the printed document this file owns. Every import, device, scan, and capture option is a `Lumen.*` key, and §3's import presets are settings users save and reuse. Import, second-copy, conversion, and batch-scan summaries are the reports (§2 owns the per-file summary). Card detection and AutoPlay (§4), progress and Cancel on every run, and the completion summary are the notifications. Read-only destinations, locked sources, devices refusing transfer, and missing TWAIN drivers are refused by name (§1 sets the refusal pattern). Every import run, conversion, scan, and capture writes one Serilog Information line and one history entry (§1). DNG (§6), multi-page TIFF and PDF scans (§7), and captured PNG and JPEG files (§8) are the exchange surface. An import undoes as a catalog removal, Move keeps its sources in the Recycle Bin, and auto import can be paused (§1 and §5).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The import window extended | D04 T02 §8, D04 T06 §8 |  [ ]   |
|   2   |   §2    | File handling on import: previews, backup copies, renaming, and destination folders | §1, D04 T11 §2, D04 T06 §11 |  [ ]   |
|   3   |   §3    | Apply during import and import presets | §2, D04 T08 §3, D04 T08 §5, D04 T08 §9, D04 T06 §5, D04 T06 §6 |  [ ]   |
|   4   |   §4    | Phones and cameras over Windows Portable Devices | §1, D04 T05 §3 |  [ ]   |
|   5   |   §5    | Auto import from watched folders | §3 |  [ ]   |
|   6   |   §6    | Convert to DNG | §1, D04 T13 §7 |  [ ]   |
|   7   |   §7    | Scanning and Copy Shop | §1, D03 T17 §12, D03 T18 §6, D04 T13 §6, D04 T11 §2 |  [ ]   |
|   8   |   §8    | Screen capture | §1, D03 T17 §12, D04 T11 §2 |  [ ]   |

---

## 1. The import window extended

`D04 T01 §6` imports a folder in Add or Copy mode with a preview count. Lightroom's import window picks exactly which photos come in from a card, shows them large enough to decide, and can move instead of copy; ACDSee and IrfanView import by drag and drop and from the browser. This section extends the planner and runner in place (never a second import path) with sources, Move, the candidate grid, filters, a loupe, and a completion that opens the imported photos. Move is the dangerous mode: a source goes to the Recycle Bin only after its copy's SHA-256 matches, and never on read-only media. Catalog: LP-0407, LP-0432 to LP-0439 (9 features: Import to This Folder, the source panel, Move mode, the candidate grid, filters and grouping, the import preview, drag and drop, the browser's Import menu, and completion in a new tab). -> SOURCE: parity-lumen-import-window

**Fidelity:** docs/captures/lumen/import/ (baseline from `D04 T01 §6`); new captures to docs/captures/lumen/import-grid/.
**Job:** a photographer picks exactly which photos come in from a card, sees them large enough to decide, and can move instead of copy without ever risking the card's files. Consumer: the catalog, `D04 T06 §8`'s previous-import entries, and the browse tab that opens on completion.
**Treatment:** Lightroom's three-column import window (sources on the left; the candidate grid with Copy as DNG, Copy, Move, and Add across the top; destination and options on the right) with a compact mode; candidate filters All, New Photos, and Destination Folders; grouping by date or type; a loupe with E. Cheaper substitute that fails the checkpoint: import everything in a folder.
**Chrome:** consume `D04 T01 §6`'s `ImportPlanner` and `ImportRunner` (extended), `D04 T01 §7`'s embedded-preview extraction, `D04 T05 §6`'s Recycle Bin operation, and the theme. Do not add a second import runner.

**Requires:** display-session -- the import window is driven on an interactive desktop

- [ ] Add `ImportSource` in `src/Lumen/Photon.Lumen.Core/Import/Sources/ImportSource.cs` (LP-0432): removable drives first, card readers, local and network folders, and optical discs, with include subfolders, and favorites and recents in `Lumen.Import.Sources`; devices without drive letters join once §4 ships. Done when: `ImportSourceTests` order a fake removable drive before a fixed folder and persist a favorite.
- [ ] Add the source panel to `src/Lumen/Photon.Lumen.Desktop/Import/ImportWindow.xaml` with the three-column layout and a compact mode toggle. Done when: captures of both layouts are committed under docs/captures/lumen/import-grid/. Cheaper substitute: the 0.1.0 folder picker.
- [ ] Add Move mode to `ImportRunner` (LP-0433): copy, verify SHA-256, record in the catalog, then send the source to the Recycle Bin through `D04 T05 §6`, never a permanent delete. Done when: `ImportMoveTests` assert the source exists until verification and lands in the Recycle Bin after.
- [ ] Fall back from Move to Copy on read-only media with a message naming the volume. Done when: `ImportMoveTests.ReadOnlySource` asserts Copy and the message.
- [ ] Add a copy-corruption test hook to `ImportRunner` that flips a byte in the copy. Done when: `ImportMoveTests.CorruptCopyKeepsSource` asserts the source stays, the corrupt copy is removed, and the failure is listed by file name.
- [ ] Add the candidate grid (LP-0434) in `src/Lumen/Photon.Lumen.Desktop/Import/CandidateGrid.xaml`: checkboxes, check all and none, new, all, or custom selection, and view all or checked. Done when: `CandidateSelectionTests` assert each selection command on a 200-file fixture listing.
- [ ] Add candidate filters and grouping (LP-0435): all, new photos only (not in the catalog by hash), by destination folder, by date, by file type, and sort order. Done when: `CandidateSelectionTests.Filters` cover each.
- [ ] Add the import preview (LP-0436): a thumbnail size slider, a loupe from the embedded preview on E, higher-quality embedded previews when the file has them, and the compact dialog. Done when: a capture shows the loupe on a RAW candidate.
- [ ] Open the import window with dropped files or folders as the source (LP-0437). Done when: a driven drop of a folder onto the main window opens it with that source (capture).
- [ ] Add the Import menu entry in the browser (LP-0438) and Import to This Folder from `D04 T06 §8`'s Folders panel (LP-0407), which sets Add mode with that folder. Done when: `ImportEntryPointTests` assert the mode and source each entry sets.
- [ ] Open the imported photos in a new browse tab on completion (LP-0439), extending `D04 T01 §6`'s summary, and mark them as the current import for `D04 T06 §8`. Done when: a driven import ends in a tab showing exactly the imported set.
- [ ] Refuse by name a destination Windows denies write permission to (read-only, full, or locked) before any file is copied, and report a locked source file per file while the run continues. Done when: `ImportRefusalTests` assert both messages.
- [ ] Record each import as one suite history entry (undo removes the imported records; copied files stay on disk and the undo says so) and one Serilog Information line with the mode, counts, and bytes. Done when: `ImportHistoryTests` undo an import and a Serilog test logger asserts the line.
- [ ] Write `docs/user/lumen/import.md` covering sources, modes, the candidate grid, and Move's safety rule, and naming browse without importing as the alternative. Done when: every Treatment control is on the page.
- [ ] Commit: `"lumen: the full import window with sources, candidates, and Move"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ImportSourceTests|FullyQualifiedName~ImportMoveTests|FullyQualifiedName~CandidateSelectionTests|FullyQualifiedName~ImportEntryPointTests|FullyQualifiedName~ImportRefusalTests|FullyQualifiedName~ImportHistoryTests"` exits 0, proving the source stays until verification and lands in the Recycle Bin, and a driven import of a 200-photo card fixture with a custom selection imports exactly the checked set (captures under docs/captures/lumen/import-grid/). Cheaper substitute that fails: moving with `File.Move` across volumes, which `ImportMoveTests.CorruptCopyKeepsSource` catches.

**Freeze check:** Import opens every source read-only; Copy and Move write each copy through a temp name in the destination, verify its SHA-256 against the source, then rename; Move sends a source to the Recycle Bin only after that verification and never on read-only media; a failure mid-copy leaves the source untouched and no partial file; a test asserts every Copy-mode source's SHA-256 and last-write time are unchanged. Fixture source: `tests/fixtures/lumen/import/` (from `D04 T01 §6`) copied to a temp card folder per test.

## 2. File handling on import: previews, backup copies, renaming, and destination folders

Photographers land photos named and filed the way they always file them, with a backup copy made in the same pass. This section adds the right column's File Handling, File Renaming, and Destination panels: previews and smart previews built on import, a hash-verified second copy to another drive, renaming through `D04 T11 §2`'s token engine with persisted sequence counters, every destination organization, RAW+JPEG placement, and ejecting the card afterwards. A second-copy failure is reported per file and never blocks the primary import. Catalog: LP-0408, LP-0440 to LP-0447 (9 features: sequence counters, eject, previews on import, smart previews on import, the second copy, renaming templates, destination organization, folder options, and RAW+JPEG placement). -> SOURCE: parity-lumen-import-files

**Fidelity:** docs/captures/lumen/import/; new captures to docs/captures/lumen/import-file-handling/.
**Job:** a photographer lands photos named and filed the way they always file them, with a backup copy made in the same pass. Consumer: the destination tree, the backup drive, the preview cache, and the import summary.
**Treatment:** the right column's File Handling (Build Previews, Build Smart Previews, Don't Import Suspected Duplicates, Make a Second Copy To), File Renaming (template menu, custom text, shoot name, start number, extension case, a live sample), and Destination (Into Subfolder, Organize By Original Folders or By Date with a date format, Into One Folder) panels; Eject after import. Cheaper substitute that fails the checkpoint: a fixed rename pattern.
**Chrome:** consume `D04 T11 §2`'s token engine, `D04 T01 §7`'s preview builder, `D04 T06 §11`'s smart previews, `D04 T05 §2`'s indexer queue, and `AtomicFileWriter`. Do not add a second naming engine.

**Requires:** display-session -- the file-handling panels are driven on an interactive desktop

- [ ] Add `ImportPreviewPolicy` in `src/Lumen/Photon.Lumen.Core/Import/ImportPreviewPolicy.cs` (LP-0441): minimal, embedded and sidecar, standard, and 1:1, with replace-embedded-when-idle queued through `D04 T05 §2`'s indexer. Done when: `ImportPreviewPolicyTests` assert which cache entries exist after each choice.
- [ ] Build smart previews on import (LP-0442) through `D04 T06 §11`'s `SmartPreviewStore` when checked. Done when: a test imports three raws with the option and finds three proxies.
- [ ] Add `SecondCopyWriter` in `src/Lumen/Photon.Lumen.Core/Import/SecondCopyWriter.cs` (LP-0443): a parallel stream to a backup folder, each file written through a temp name and hash-verified like the primary. Done when: `SecondCopyTests` assert every backup hash equals its source.
- [ ] List second-copy failures per file in the summary without blocking the primary import. Done when: `SecondCopyTests.CorruptBackupReported` flips a byte in one backup and asserts the primary import completed and the failure is named.
- [ ] Add `ImportRenamer` in `src/Lumen/Photon.Lumen.Core/Import/ImportRenamer.cs` (LP-0444) over `D04 T11 §2` templates: custom name, sequence, date, filename, shoot name, camera, start number, and extension case, with a live sample. Done when: `ImportRenameTests` cover each token.
- [ ] Resolve name collisions within a run and against the destination with a numeric suffix, never overwriting. Done when: `ImportRenameTests.Collisions` asserts three colliding names get distinct suffixes.
- [ ] Persist import sequence counters (LP-0408) in `Lumen.Import.Sequence`. Done when: two runs continue the sequence across a restart.
- [ ] Add the File Renaming panel with the template menu and live sample. Done when: a capture under docs/captures/lumen/import-file-handling/ shows the sample updating. Cheaper substitute: a fixed pattern.
- [ ] Add `DestinationOrganizer` in `src/Lumen/Photon.Lumen.Core/Import/DestinationOrganizer.cs` (LP-0445): folder, named subfolder, by original folders, by capture or today's date nested or flat with a date format, and one folder, extending `D04 T01 §6`'s `yyyy/yyyy-MM-dd` pattern, with a preview of new folders. Done when: `DestinationOrganizerTests` cover every mode.
- [ ] Add the folder options (LP-0446): ignore camera-generated folder names (`DCIM\100CANON`) and show the parent folder. Done when: `DestinationOrganizerTests.IgnoreCameraFolders` passes.
- [ ] Add RAW+JPEG placement (LP-0447): same folder, or JPEG or RAW in a named subfolder, with pairs kept linked for `D04 T13 §5`. Done when: `RawJpegPlacementTests` cover each placement and assert the link.
- [ ] Add Eject after import (LP-0440) through `CM_Request_Device_Eject` after every handle closes, with a message naming the device when Windows refuses. Done when: `EjectTests` assert the call after close on a fake device and the refusal message.
- [ ] Add the per-file import summary (imported, skipped as duplicates, renamed, second copies verified, failures with reasons) as a report the user can copy. Done when: a capture shows the summary after a run with one failure.
- [ ] Log one Serilog Information line per run naming the template, the organization, and the second-copy result. Done when: a Serilog test logger asserts it.
- [ ] Write the File Handling, Renaming, and Destination parts of `docs/user/lumen/import.md`. Done when: every panel control is on the page.
- [ ] Commit: `"lumen: import file handling with previews, second copies, renaming, and destinations"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ImportPreviewPolicyTests|FullyQualifiedName~SecondCopyTests|FullyQualifiedName~ImportRenameTests|FullyQualifiedName~DestinationOrganizerTests|FullyQualifiedName~RawJpegPlacementTests|FullyQualifiedName~EjectTests"` exits 0, and a driven import with a template, date organization, and a second copy produces the expected tree in both locations with every hash matching its source (listing quoted). Cheaper substitute that fails: an unverified second copy, which `SecondCopyTests.CorruptBackupReported` catches.

**Freeze check:** The second copy and every renamed destination file are written through a temp name and verified by SHA-256 before the rename; sources are opened read-only and never renamed on the card; Eject runs only after every handle closes; a test asserts every source's SHA-256 and last-write time are unchanged after an import with renaming and a second copy. Fixture source: `tests/fixtures/lumen/import/` copied to a temp card folder.

## 3. Apply during import and import presets

A photographer sets up a shoot once (copyright, keywords, a look, a collection) and every later card lands ready. This section applies a develop preset, a metadata preset, keywords, categories, and custom fields in the same catalog transaction as the import, adds the photos to a collection, rotates from the camera orientation as metadata, chooses the catalog date source, and saves it all as import presets. It follows the operator's 2026-09-27 decision "Safe by default, opt-in writes": applied metadata goes to the catalog and the sidecar by default, and when the user has turned on embedding (`D04 T08 §9`), it is embedded into the verified destination copy (Copy, Move, Copy as DNG) or, in Add mode, into the file in place under the embedder's backup rule; a source on a card or device is never written. Catalog: LP-0448 to LP-0452, LP-0555 (6 features: add to collection, apply during import, import presets, automatic rotation, the date source, and a develop preset on import). -> SOURCE: parity-lumen-import-presets

**Fidelity:** docs/captures/lumen/import/; new captures to docs/captures/lumen/import-presets/.
**Job:** a photographer sets up a shoot once (copyright, keywords, a look, a collection) and every later card lands ready. Consumer: the catalog, the edit stack, sidecars, and, only when embedding is on, the imported files through `D04 T08 §9`.
**Treatment:** the Apply During Import panel (Develop Settings, Metadata with New inline, Keywords, Categories) and Add to Collection; an Import Preset menu at the bottom (save, update, rename, delete, none, recent); a line under Metadata saying where it will be written ("Sidecar files" or "Embedded in the imported copies"). Cheaper substitute that fails the checkpoint: applying metadata in a second pass after import.
**Chrome:** consume `D04 T02 §5`'s presets, `D04 T08 §3`'s metadata presets, `D04 T08 §5`'s keyword entry, `D04 T06 §6`'s categories, `D04 T06 §5`'s collections, `D04 T08 §8`'s metadata writer, and `D04 T08 §9`'s embedder. Do not add a second metadata writer.

**Requires:** display-session -- the import presets panel is driven on an interactive desktop

- [ ] Add `ImportApplyOptions` in `src/Lumen/Photon.Lumen.Core/Import/ImportApplyOptions.cs` (LP-0449): metadata preset, keywords, categories, and ACDSee-style custom fields, applied to the catalog in the import transaction. Done when: `ImportApplyTests` assert each option on the fixture folder in one transaction.
- [ ] Apply a develop preset on import (LP-0555) as the first `D04 T02 §1` edit-stack entry. Done when: `ImportApplyTests.DevelopPreset` asserts the entry and that undo of the import removes it.
- [ ] Write applied metadata through `D04 T08 §8`'s `MetadataWriter`, which writes the sidecar while `D04 T11 §1`'s `Lumen.Originals.InPlace.EmbedMetadata` is off (the default). Done when: `ImportApplyTests.SidecarDefault` reads every applied field from the sidecar and asserts the imported file's bytes equal the source's.
- [ ] When `Lumen.Originals.InPlace.EmbedMetadata` is on, embed applied metadata through `D04 T08 §9` into the destination copy only after its SHA-256 verified against the source, then record the post-embed hash in the catalog. Done when: `ImportEmbedTests.CopyEmbedded` asserts the copy carries the fields (exiftool 13 readback), the source is byte-identical, and the catalog hash equals the embedded file's.
- [ ] In Add mode with embedding on, embed into the file in place through `D04 T08 §9` with its backup rule, and never into a file on removable or read-only media (sidecar instead, with a summary line naming why). Done when: `ImportEmbedTests.AddModeBackup` asserts the backup copy's hash equals the pre-import file and `ImportEmbedTests.RemovableFallsBack` asserts the sidecar.
- [ ] Add photos to a collection on import (LP-0448), including a new collection created inline. Done when: `ImportApplyTests.Collection` asserts membership and the inline creation.
- [ ] Add automatic rotation (LP-0451) from the EXIF orientation into the catalog orientation, never written into the file. Done when: `ImportApplyTests.Orientation` imports the eight orientation fixtures upright with every file hash unchanged.
- [ ] Add the catalog date source (LP-0452): EXIF date, file modified date, or a specific date. Done when: `ImportApplyTests.DateSource` covers each.
- [ ] Add the `ImportPreset` store (LP-0450) in `Lumen.Import.Presets` holding source-independent options: save, update, rename, delete, none, and recent. Done when: `ImportPresetTests` cover each command and assert a preset never stores a source path.
- [ ] Add the Apply During Import panel, the write-target line, and the Import Preset menu to the import window. Done when: captures under docs/captures/lumen/import-presets/ show both write-target texts. Cheaper substitute: a post-import batch.
- [ ] Log one Serilog Information line per import naming the preset and the write target. Done when: a Serilog test logger asserts it.
- [ ] Write the Apply During Import and presets part of `docs/user/lumen/import.md`, stating the sidecar default and the embedding setting. Done when: the page names both write targets.
- [ ] Commit: `"lumen: apply during import and import presets"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~ImportApplyTests|FullyQualifiedName~ImportEmbedTests|FullyQualifiedName~ImportPresetTests|FullyQualifiedName~UnchangedOriginalsTests"` exits 0, and a driven import with a preset yields photos carrying the metadata, keywords, look, and collection, with the sidecar holding the fields under the default and the sources on the fixture card byte-identical (hashes quoted). Cheaper substitute that fails: a post-import batch, which the single-transaction assertion in `ImportApplyTests` catches.

**Freeze check:** With `Lumen.Originals.InPlace.EmbedMetadata` off (the default), import writes applied metadata only to the catalog and sidecars and every imported file's bytes equal its source's; with embedding enabled, `D04 T08 §9` writes only into a destination copy after its hash verified, or into an Add-mode file after its backup copy verified, through the atomic writer; a source on a card, device, or read-only volume is never written; the operator's 2026-09-27 approval ("Safe by default, opt-in writes") is what permits the opt-in path. Fixture source: `tests/fixtures/lumen/import/` and `tests/fixtures/lumen/metadata/` (from `D04 T08 §1`).

## 4. Phones and cameras over Windows Portable Devices

Phones and many cameras connect over MTP or PTP with no drive letter, so a folder picker cannot see them. This section lists them as import sources and as read-only browsable folders in `D04 T05 §3`'s tree, streams their files into the import runner's verified copy, and registers AutoPlay so inserting a card or device can offer Lumen. Catalog: LP-0453 to LP-0454 (2 features: card detection and AutoPlay, and import from WIA and portable devices). -> SOURCE: parity-lumen-devices

**Fidelity:** docs/captures/lumen/import/; new captures to docs/captures/lumen/devices/.
**Job:** a photographer plugs in a phone or camera and imports from it like from a card, or just browses it. Consumer: §1's import runner and `D04 T05 §3`'s folder tree.
**Treatment:** devices listed first in the source panel with their icons; Windows AutoPlay offering "Import photos with Lumen" and "Browse with Lumen"; Preferences, Import, Show import dialog when a memory card is detected. Cheaper substitute that fails the checkpoint: asking the user to copy files off the phone first.
**Chrome:** consume the Windows Portable Devices COM API (part of Windows), §1's import runner, and `D04 T05 §3`'s folder tree for browsing. Do not add a second copy-and-verify path.

**Requires:** display-session -- a connected MTP device and AutoPlay are driven on an interactive desktop

- [ ] Add an `IPortableDeviceSession` wrapper in `src/Lumen/Photon.Lumen.Core/Devices/Wpd/` over `IPortableDeviceManager` and `IPortableDeviceContent` so tests can substitute a fake device. Done when: `WpdDeviceSourceTests` run against the fake with no device attached.
- [ ] Add `WpdDeviceSource` in `src/Lumen/Photon.Lumen.Core/Devices/WpdDeviceSource.cs` (LP-0454): enumerate devices, walk storage objects, and name files by `WPD_OBJECT_ORIGINAL_FILE_NAME`. Done when: `WpdDeviceSourceTests` list a fake device's DCIM tree.
- [ ] Stream device files through `IPortableDeviceResources` into §1's temp-name copy and SHA-256 verification, reading the device twice when it offers no stable hash. Done when: `WpdDeviceSourceTests.VerifiedCopy` asserts a verified copy from the fake and a mismatch on a fake that changes bytes between reads.
- [ ] List WIA cameras through the same source. Done when: `WpdDeviceSourceTests.WiaCamera` lists a fake WIA camera.
- [ ] Show devices first in §1's source panel with their icons. Done when: a capture under docs/captures/lumen/devices/ shows a phone first.
- [ ] Show device folders in `D04 T05 §3`'s tree as read-only virtual folders that browse without importing (LP-0454). Done when: `DeviceFolderTests` assert rename and delete are disabled with a tooltip saying the device is read-only.
- [ ] Refuse a device that denies transfer (locked phone, permission prompt dismissed) with a message naming the device and what to do. Done when: `WpdDeviceSourceTests.AccessDenied` asserts the message.
- [ ] Register AutoPlay handlers (LP-0453) for `ShowPicturesOnArrival` and `MixedContentOnArrival` per user in `installer/Lumen.iss`, launching `Lumen.exe --import <device>` and `Lumen.exe --browse <device>`. Done when: a driven card insertion on a clean install shows both Lumen entries in AutoPlay (capture).
- [ ] Add the card-detected setting `Lumen.Import.ShowOnCard` (default off) watching `WM_DEVICECHANGE`, with a notification in the status strip naming the card when the setting is off. Done when: `CardDetectionTests` raise a fake arrival and assert the window opens only when the setting is on.
- [ ] Log one Serilog Information line per device import naming the device model and counts. Done when: a Serilog test logger asserts it.
- [ ] Write the devices and AutoPlay part of `docs/user/lumen/import.md`. Done when: the page covers phones, cameras, and AutoPlay.
- [ ] Commit: `"lumen: import from phones and cameras over Windows Portable Devices"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~WpdDeviceSourceTests|FullyQualifiedName~DeviceFolderTests|FullyQualifiedName~CardDetectionTests"` exits 0, and a driven import from an MTP phone (model quoted) completes with verified copies and captures under docs/captures/lumen/devices/. Cheaper substitute that fails: requiring a drive letter, which the fake device without a path in `WpdDeviceSourceTests` catches.

## 5. Auto import from watched folders

Lightroom's Auto Import watches a folder and moves each new file into the library with naming, a develop preset, metadata, keywords, and previews applied. It is also Lumen's answer for tethered shooting (operator decision, 2026-09-27): tethered capture proper stays backlog B-048, because no GPL-compatible, supported Windows camera-control path exists, and a studio photographer instead shoots through the camera maker's own free tether utility (Canon EOS Utility, Nikon NX Tether, Sony Imaging Edge, Fujifilm X Acquire) writing into a watched folder, so each frame appears developed in Lumen seconds later. A file imports only after its writer closes it, never on the created event. Catalog: LP-0455 to LP-0456 (2 features: auto import with its settings, and the watched folder). -> SOURCE: parity-lumen-auto-import

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/auto-import/.
**Job:** a studio photographer shooting tethered through the camera maker's utility sees each frame appear developed in Lumen seconds later. Consumer: the catalog, the grid (the newest photo is selected), and the loupe.
**Treatment:** File, Auto Import, Enable Auto Import and Auto Import Settings (a watched folder that must be empty, destination and subfolder, naming, develop preset, metadata, keywords, and initial previews), a status-strip indicator while watching, and a note naming the tether utilities and B-048. Cheaper substitute that fails the checkpoint: a periodic folder rescan.
**Chrome:** consume §2's renaming and destination, §3's apply options and write-target rule, `FileSystemWatcher`, and §1's import runner. Do not add a second import runner.

**Requires:** display-session -- the settings dialog and a live drop are driven on an interactive desktop

- [ ] Add `AutoImportService` in `src/Lumen/Photon.Lumen.Core/Import/Auto/AutoImportService.cs` (LP-0455) watching the folder with `FileSystemWatcher` and rescanning on a buffer overflow. Done when: `AutoImportTests.Overflow` forces an overflow and every file still imports once.
- [ ] Wait until a file is stable (size unchanged across two probes and an exclusive-open probe succeeds) before importing it. Done when: `AutoImportTests.SlowWriter` has a writer thread write a file slowly and the file imports once, after close.
- [ ] Copy with verification into the destination through §1's runner, then recycle the file from the watched folder after verification. Done when: `AutoImportTests.RecycleAfterVerify` asserts the order.
- [ ] Apply §2's naming and destination and §3's develop preset, metadata, keywords, and write-target rule, and build initial previews. Done when: `AutoImportTests.Applied` asserts each on an imported file.
- [ ] Select the newest photo in the grid and loupe as each file lands. Done when: a test asserts the selection moves to the new record.
- [ ] Add the settings `Lumen.Import.Auto.*` (folder, destination, subfolder, naming, preset, metadata, keywords, previews) and refuse enabling on a non-empty watched folder by name (LP-0456). Done when: `AutoImportTests.NonEmptyRefused` asserts the message.
- [ ] Add the Auto Import Settings dialog in `src/Lumen/Photon.Lumen.Desktop/Import/AutoImportDialog.xaml` with the tether note naming B-048 and the vendor utilities. Done when: a capture under docs/captures/lumen/auto-import/ shows the note. Cheaper substitute: a rescan timer setting.
- [ ] Add Pause and Resume from the status-strip indicator, which a paused watcher honors by queueing files. Done when: `AutoImportTests.Pause` asserts queued files import on resume.
- [ ] Log one Serilog Information line per auto-imported file with its latency from close to catalog. Done when: a Serilog test logger asserts it.
- [ ] Write `docs/user/lumen/auto-import.md` with a tethered-shooting walkthrough through a vendor utility. Done when: the page names the utilities and B-048.
- [ ] Commit: `"lumen: auto import from a watched folder"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~AutoImportTests"` exits 0, proving no partial file is imported, and a driven drop of 20 files lands them developed with the median latency quoted from the log. Cheaper substitute that fails: importing on the created event, which `AutoImportTests.SlowWriter` catches.

**Freeze check:** Auto import copies each file through §1's verified path and recycles the watched-folder file only after verification; it writes metadata only as §3's write-target rule allows; a test asserts no file in the watched folder is removed before its copy verifies. Fixture source: `tests/fixtures/lumen/import/` copied into a temp watched folder.

## 6. Convert to DNG

Photographers who standardize on DNG want it done at import (Copy as DNG) or later (Convert Photos to DNG) with Lightroom's options, without losing metadata or risking the raw file. This section drives `D04 T13 §7`'s writer: a new DNG is validated before the catalog record switches to it, and the original goes to the Recycle Bin only when the user asked and validation passed. Converting writes new files, so embedding metadata into the DNG is always allowed. Catalog: LP-0409, LP-0457 to LP-0458 (3 features: Convert Photos to DNG, the Copy as DNG import mode, and the conversion options). -> SOURCE: parity-lumen-dng-convert

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/dng-convert/.
**Job:** a photographer standardizes on DNG without losing any metadata or risking the raw file. Consumer: the catalog, the develop pipeline through `D04 T01 §4`, and export.
**Treatment:** Copy as DNG at the top of the import window; Library, Convert Photos to DNG dialog (only raw files, move originals to the Recycle Bin after a successful conversion, extension case, JPEG preview size, embed fast load data, lossy compression, embed original raw, compatibility). Cheaper substitute that fails the checkpoint: renaming the raw file.
**Chrome:** consume `D04 T13 §7`'s writer, §1's import runner, and the catalog. Do not add a second DNG writer.

**Requires:** display-session -- the conversion dialog is driven on an interactive desktop

- [ ] Add `DngConversionOptions` in `src/Lumen/Photon.Lumen.Core/Import/Dng/DngConversionOptions.cs` (LP-0458): extension case, JPEG preview size, fast load data, lossy compression, embed original raw, and compatibility version, stored as `Lumen.Dng.*`. Done when: `DngConversionTests.OptionsReachWriter` asserts each option reaches `D04 T13 §7`'s writer.
- [ ] Add `DngConversionService` (LP-0409) writing the DNG beside the original, carrying the catalog metadata and develop settings into its XMP. Done when: `DngConversionTests.MetadataCarried` reads the fields back with exiftool 13.
- [ ] Validate each new DNG (decode through `D04 T01 §4`, plus Adobe `dng_validate` as an oracle where installed) before switching the catalog record. Done when: `DngConversionTests.SwitchAfterValidation` asserts the order and a validation failure keeps the raw record.
- [ ] Move the original to the Recycle Bin only when the user ticked it and validation passed. Done when: `DngConversionTests.OriginalKeptOnFailure` asserts the raw stays on a forced failure.
- [ ] Add the Copy as DNG import mode (LP-0457) writing DNGs into the destination, copying the raw only when Embed Original Raw is on. Done when: `DngConversionTests.CopyAsDng` imports a raw fixture as a DNG and the card's file is byte-identical.
- [ ] Add the Convert Photos to DNG dialog in `src/Lumen/Photon.Lumen.Desktop/Import/ConvertToDngDialog.xaml` with only-raw filtering and a confirmation naming the count before recycling originals. Done when: a capture under docs/captures/lumen/dng-convert/ is committed. Cheaper substitute: renaming the file to `.dng`.
- [ ] Run conversions in the background with progress, Cancel, and a summary naming converted, skipped, and failed files. Done when: a test cancels midway and asserts no partial DNG.
- [ ] Log one Serilog Information line per conversion. Done when: a Serilog test logger asserts it.
- [ ] Write `docs/user/lumen/dng.md`. Done when: every option is on the page.
- [ ] Commit: `"lumen: Copy as DNG and Convert to DNG"`

**Test checkpoint:** Format fidelity proof plus unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~DngConversionTests"` exits 0, and converting the committed raw fixtures yields DNGs that decode through `D04 T01 §4` within the stated tolerance of the original decode, with the originals' hashes unchanged when not recycled. Cheaper substitute that fails: switching the catalog before validation, which `DngConversionTests.SwitchAfterValidation` catches.

**Freeze check:** Conversion writes a new DNG through the atomic writer and never opens the raw for writing; the catalog switches only after validation; the raw goes to the Recycle Bin only when chosen and validated; a test asserts every unrecycled raw's SHA-256 and last-write time are unchanged. Fixture source: `tests/fixtures/lumen/raw/` (from `D04 T01 §4`).

## 7. Scanning and Copy Shop

IrfanView users digitize prints and documents in batches: a TWAIN source, a file-name pattern with a counter, multi-page TIFF or PDF output, and Copy Shop to scan and print copies. This section adds scanning through the WIA service `D03 T17 §12` moved to `Photon.Core/Acquire/` (Lumen is its third consumer) and TWAIN through NTwain (MIT) over the data source manager the scanner driver installs, never bundled. Scanners whose drivers are 32-bit only are listed as unavailable with the reason, since a 64-bit process cannot load them. Scans are new files added to the catalog in place. Catalog: LP-0459 to LP-0464 (6 features: the scan destination, single scans through TWAIN or WIA, the second scan destination row, source selection and batch scanning, batch scan naming, and Copy Shop). -> SOURCE: parity-lumen-scanning

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/scan/.
**Job:** a user digitizes prints and documents straight into the library, many pages in one go, or makes copies with a scanner and printer. Consumer: the catalog, the destination folder, and the printer.
**Treatment:** File, Acquire (Select Source, Acquire, a Batch Scanning dialog with pattern, counter start, step, digits, skip existing, remember counter, destination, format, multi-page, keep scanner UI open); File, Copy Shop (scanner, preview, DPI, printer, copies). Cheaper substitute that fails the checkpoint: WIA only, which drops IrfanView's TWAIN batch workflow.
**Chrome:** consume `WiaAcquireService` in `Photon.Core/Acquire/` (from `D03 T17 §12`), NTwain (MIT), `D04 T11 §2`'s tokens, `D04 T13 §6`'s TIFF and PDF writers, and the `Photon.UI/Print/` dialog frame (from `D03 T18 §6`). Do not copy the WIA service into Lumen.

**Requires:** display-session -- a scanner driver's user interface is driven on an interactive desktop

- [ ] Consume `WiaAcquireService` from `src/Photon.Core/Acquire/` for WIA scanners and cameras. Done when: `grep -rn "class WiaAcquireService" src` prints one path, under `src/Photon.Core/`.
- [ ] Add NTwain (MIT) to `Directory.Packages.props` with a `docs/dev/decisions.md` row naming the license, that the TWAIN DSM comes from the scanner driver and is never bundled, and that Imago's "TWAIN unsupported" row is unchanged. Done when: the row exists and the package restores.
- [ ] Add `TwainSource` in `src/Lumen/Photon.Lumen.Core/Acquire/Twain/TwainSource.cs` (LP-0460, LP-0462): Select Source and single acquire through the 64-bit DSM. Done when: `TwainSourceTests` acquire one page from the TWAIN virtual scanner sample data source where installed, or skip with the reason named.
- [ ] List 32-bit-only TWAIN sources as unavailable with a tooltip naming the reason. Done when: `TwainSourceTests.ThirtyTwoBitListed` asserts the entry and tooltip against a fake DSM listing.
- [ ] Refuse scanning with a message naming the missing driver when no DSM or WIA device exists. Done when: `ScanRefusalTests` assert the message.
- [ ] Add the scan destination folder (LP-0459, LP-0461) as `Lumen.Scan.Destination`, with scans added to the catalog in place. Done when: `BatchScanNamingTests.Destination` asserts catalog records in that folder.
- [ ] Add batch scan naming (LP-0463) through `D04 T11 §2`: a pattern, counter start, step, digits, skip existing, and remember counter in `Lumen.Scan.Counter`. Done when: `BatchScanNamingTests` cover each option and a restart continues the counter.
- [ ] Write multi-page TIFF or PDF output through `D04 T13 §6`'s writers, keeping the scanner UI open between pages when chosen. Done when: `BatchScanNamingTests.MultiPage` writes a three-page TIFF from three fake pages and reopens it with three pages.
- [ ] Add the Batch Scanning dialog in `src/Lumen/Photon.Lumen.Desktop/Acquire/BatchScanDialog.xaml`. Done when: a capture under docs/captures/lumen/scan/ is committed. Cheaper substitute: a single-page acquire only.
- [ ] Add Copy Shop (LP-0464) in `src/Lumen/Photon.Lumen.Desktop/Acquire/CopyShopDialog.xaml`: scanner, preview, DPI, printer, and copies, printing through the `Photon.UI/Print/` frame until `D04 T12 §4`'s print module ships. Done when: a driven Copy Shop run prints to the Microsoft Print to PDF printer and the PDF holds the requested copies.
- [ ] Log one Serilog Information line per scan and per Copy Shop run. Done when: a Serilog test logger asserts each.
- [ ] Write `docs/user/lumen/scanning.md` covering WIA, TWAIN, 32-bit drivers, batch scanning, and Copy Shop. Done when: every Treatment control is on the page.
- [ ] Commit: `"lumen: scanning through WIA and TWAIN, batch scanning, and Copy Shop"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~BatchScanNamingTests|FullyQualifiedName~TwainSourceTests|FullyQualifiedName~ScanRefusalTests"` exits 0 (TWAIN tests skipped with a named reason where no DSM is installed), and a driven batch scan of three pages from the TWAIN sample source writes a three-page TIFF into the catalog (capture). Cheaper substitute that fails: a copied WIA class in Lumen, which the `grep -rn "class WiaAcquireService" src` item catches.

## 8. Screen capture

IrfanView and ACDSee include a capture utility: the desktop, a monitor, a window, a region, or a scrolling object, triggered by a hotkey or a timer, saved to a named file or sent to the viewer, clipboard, or printer. This section moves Imago's `Windows.Graphics.Capture` screenshot code from `D03 T17 §12` to `Photon.Core/Capture/` on this second consumer and builds the utility on it. Captures are new files. Catalog: LP-0465 to LP-0470 (6 features: the resident utility, capture sources, destinations and triggers, capture modes, triggers and output options, and region capture). -> SOURCE: parity-lumen-capture

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/capture/.
**Job:** a user grabs a window or region into a file or the library with one hotkey. Consumer: the catalog, the viewer, the clipboard, and the printer.
**Treatment:** File, Capture Screen dialog (IrfanView and ACDSee options), a notification-area icon while resident with Capture and Exit, and a region picker overlay. Cheaper substitute that fails the checkpoint: Print Screen to the clipboard only.
**Chrome:** consume the screenshot code moved to `Photon.Core/Capture/`, `D04 T11 §2`'s tokens, `AtomicFileWriter`, and the `Photon.UI/Print/` frame. Do not keep a second capture implementation in Imago.

**Requires:** display-session -- screen capture is driven on an interactive desktop

- [ ] Move Imago's screenshot capture code of `D03 T17 §12` to `src/Photon.Core/Capture/ScreenCaptureService.cs` and repoint Imago. Done when: `grep -rn "class ScreenCaptureService" src` prints one path, under `src/Photon.Core/`, and Imago's screenshot test passes against the moved type.
- [ ] Add the capture sources (LP-0466, LP-0468, LP-0470): desktop, monitor, window, client area, region, child window, menu under the cursor, and a fixed rectangle. Done when: `CaptureSourceTests` capture a known test window by handle to its exact client size.
- [ ] Add auto-scroll object capture (LP-0468) in `src/Lumen/Photon.Lumen.Core/Capture/ScrollStitcher.cs`: send scroll messages and stitch overlapping strips by row matching. Done when: `ScrollStitcherTests` reconstruct a synthetic page from overlapping strips exactly.
- [ ] Add the region picker overlay in `src/Lumen/Photon.Lumen.Desktop/Capture/RegionOverlay.xaml` with a magnifier and pixel dimensions. Done when: a capture under docs/captures/lumen/capture/ shows the overlay.
- [ ] Add hotkey triggers through `RegisterHotKey` (LP-0467, LP-0469), reporting a conflicting hotkey by name. Done when: `HotkeyRegistrationTests` assert the conflict message.
- [ ] Add timer triggers with a count and a countdown, and cursor inclusion and highlight. Done when: `CaptureTriggerTests` assert three timed captures with a fake clock.
- [ ] Add the outputs (LP-0467, LP-0469): to the viewer, clipboard, printer, or a file named through `D04 T11 §2` and written through `AtomicFileWriter`, with an optional beep on save and the file added to the catalog. Done when: `CaptureNamingTests` assert the name pattern and the catalog record.
- [ ] Add the resident utility (LP-0465): a notification-area icon with Capture, include cursor, and Exit, controlled by `Lumen.Capture.Resident`. Done when: a driven run shows the icon and its menu (capture).
- [ ] Add the Capture Screen dialog in `src/Lumen/Photon.Lumen.Desktop/Capture/CaptureDialog.xaml` with every source, trigger, and output. Done when: a capture of the dialog is committed. Cheaper substitute: clipboard-only Print Screen.
- [ ] Log one Serilog Information line per capture naming the source and output. Done when: a Serilog test logger asserts it.
- [ ] Write `docs/user/lumen/capture.md`. Done when: every source, trigger, and output is on the page.
- [ ] Commit: `"lumen: screen capture with hotkeys, timers, and auto scroll"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~CaptureSourceTests|FullyQualifiedName~ScrollStitcherTests|FullyQualifiedName~HotkeyRegistrationTests|FullyQualifiedName~CaptureTriggerTests|FullyQualifiedName~CaptureNamingTests"` exits 0 with the stitcher reconstructing the synthetic page exactly, and a driven region capture by hotkey saves a named PNG added to the catalog (capture). Cheaper substitute that fails: `CopyFromScreen` of the whole desktop only, which the window and region captures refuse.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx` exits 0 with this file's test classes reporting (`ImportMoveTests`, `CandidateSelectionTests`, `SecondCopyTests`, `ImportRenameTests`, `DestinationOrganizerTests`, `ImportApplyTests`, `ImportEmbedTests`, `WpdDeviceSourceTests`, `AutoImportTests`, `DngConversionTests`, `BatchScanNamingTests`, `ScrollStitcherTests`)
- [ ] The unchanged-originals test passes over `tests/fixtures/lumen/import/` after a Copy import with renaming, a second copy, an import preset with embedding off, and a DNG conversion without recycling
- [ ] `grep -rn "class WiaAcquireService\|class ScreenCaptureService" src` prints one path each, under `src/Photon.Core/`
- [ ] `python scripts/todo-graph.py query parity --catalog lumen --phase 34` reports every catalog row planned to this file stamped
- [ ] `python scripts/todo-graph.py validate` clean
