---
schema_version: 1
id: albumen-browse
domain: 04-albumen
status: draft
title: "TODO-05 -- Albumen Parity: Browse Without Importing"
depends_on: []
frozen: true
track: L05
---

# TODO-05 -- Albumen Parity: Browse Without Importing

> **Goal:** A photographer can point Albumen at any folder and work there at once, ACDSee style: browse without importing, with the file system as the source of truth and the catalog as its cache (an `origin` of `browsed` or `library` per record); a background indexer fills metadata and thumbnails for chosen locations while idle; the folder tree, favorites, address bar, tabs, and home page navigate; file list views, thumbnails, sorting, grouping, filtering, and selection behave like a fast file manager; file operations copy, move, rename, and recycle photos with their sidecars and pairs and an undo journal; compare, the information palette, the basket, selective browsing, a private encrypted folder, calendar browsing, a duplicate finder, archives, and folder sync complete the job. Rating or keywording a browsed file creates its record with no import step, and browsing never writes an image byte of an original. Budgets: an unindexed folder of 5,000 JPEGs lists in at most 300 ms and shows its first screen of thumbnails in at most 1.5 s, a reopened indexed folder in at most 200 ms, and the indexer processes at least 50 JPEGs per second without raising the foreground frame time over 16 ms.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Albumen has no code. The foundation file plans a catalog of imported photos only, with no browsed membership, and no Albumen section plans the Recycle Bin or file operations yet. No archive package is in the solution (`Directory.Packages.props` has no SharpCompress). `standards/albumen.md` already says paths are stored relative to a root folder so a moved library can be reconnected, and states the unconditional original-file guard; the operator's 2026-09-27 decision (opt-in in-place writes) does not touch browsing, which writes only the catalog, sidecars, and user-requested file operations. **Corrected 2026-09-28:** `D04 T04 §6` plans the viewer's Recycle Bin and file operations, which §6 here takes over (see its journal item).
<!-- claim: absent src/Albumen -->
<!-- claim: count "browsed" todo/04-albumen/TODO-01-albumen-foundation.md = 0 -->
<!-- claim: count "Recycle" todo/04-albumen/TODO-01-albumen-foundation.md = 0 -->
<!-- claim: count "Recycle" todo/04-albumen/TODO-02-albumen-develop.md = 0 -->
<!-- claim: count "SharpCompress" Directory.Packages.props = 0 -->
<!-- claim: count "relative to a root folder" standards/albumen.md = 1 -->

## Inputs

- [`standards/albumen.md`](../../standards/albumen.md) -- the catalog rules (forward-only migrations, relative paths) and the original-file guard
- [`standards/shared.md`](../../standards/shared.md) -- performance budgets, logging, refusals that name the file, progress and Cancel over one second
- [`docs/parity/albumen-section-design.md`](../../docs/parity/albumen-section-design.md) -- the blueprint and "Browse without importing"; [`docs/parity/albumen-parity.md`](../../docs/parity/albumen-parity.md) -- the catalog rows each section owns
- ACDSee Photo Studio Ultimate 2027 User Guide, the Manage mode chapters; IrfanView 4.76 help `hlp_thumbnails.htm`; Lightroom Classic 15.5.1 duplicates view help
- Microsoft Learn: `FindFirstFileExW` with `FIND_FIRST_EX_LARGE_FETCH`, `IFileOperation`, `FileSystemWatcher` buffer overflow (`InternalBufferOverflowException`), Task Scheduler idle and logon triggers, `GetLastInputInfo`, `AesGcm`, `Rfc2898DeriveBytes`, `StrCmpLogicalW`, `IContextMenu`
- -> XREF: D01 T02 §4 -- the suite history every browse action records its undo step in
- -> XREF: D01 T02 §5 -- the atomic writer for sidecars, vault files, and archives
- -> XREF: D03 T17 §12 -- the SharpCompress archive opener §12 moves to `Isotone.Core/Formats/Archives/`
- -> XREF: D04 T01 §5 -- the catalog §1 adds `origin` and `browsed_folders` to
- -> XREF: D04 T01 §7 -- the preview cache §2 feeds and §4 reads
- -> XREF: D04 T01 §8 -- the library grid whose views, badges, and sort §4 and §5 extend
- -> XREF: D04 T01 §9 -- compare, which §7 extends to four images
- -> XREF: D04 T01 §11 -- sidecars that travel in §6
- -> XREF: D04 T02 §3 -- the histogram control §4 and §7 reuse
- -> XREF: D04 T04 §1 -- the viewer's hand-off and `T` key, which §1 retargets from the library grid to browse
- -> XREF: D04 T06 §3 -- stacks that §11's duplicates view groups into
- -> XREF: D04 T06 §4 -- the filter rule model §5 shares
- -> XREF: D04 T06 §7 -- search criteria §8's selective browsing shares
- -> XREF: D04 T06 §8 -- outside moves reconnect through it
- -> XREF: D04 T07 §1 -- the import window that stays one click away beside browsing
- -> XREF: D04 T07 §4 -- phone and camera folders that appear in §3's folder tree
- -> XREF: D04 T08 §1 -- the metadata model §2's indexer reads through
- -> XREF: D04 T08 §2 -- the properties pane whose file-name field renames through §6
- -> XREF: D04 T10 §3 -- face searches on §3's home page
- -> XREF: D04 T10 §5 -- visually similar photos beyond §11's exact duplicates
- -> XREF: D04 T11 §1 -- the Activity Manager the indexer, file operations, and sync report to
- -> XREF: D04 T11 §3 -- the rename journal §6 extends into the file-operation journal
- -> XREF: D04 T11 §9 -- the record resolver §1 implements so batch develop runs on browsed RAW files
- -> XREF: D04 T11 §10 -- the text file list format §8 shares
- -> XREF: D04 T13 §1 -- reading through the shared registry, and the extension fix §6 routes through its journal
- -> XREF: D04 T13 §5 -- RAW+JPEG pairs that travel together in §6
- -> XREF: D04 T12 §11 -- the Create menu that lists §12's archive creator
- -> XREF: D04 T15 §3 -- `albumen-v0.4.0`, which quotes §1's and §2's budgets
- -> XREF: D04 T14 §4 -- the viewer and browse preferences page that renders the `Albumen.Browse.*` and `Albumen.Indexer.*` keys

## Outcome

- Any folder opens in Albumen with no import, lists 5,000 JPEGs within 300 ms, and shows its first screen of thumbnails within 1.5 s; rating or keywording a browsed file creates its catalog record, and "Add to Library" promotes it in place.
- A low-priority indexer keeps chosen locations indexed while Albumen is idle or closed, without raising the foreground frame time over 16 ms.
- Folders, favorites, tabs, the address box, and the home page navigate; the file list offers every ACDSee view with overlays, columns, sorting, grouping, filtering, and selection.
- Copy, move, rename, and delete to the Recycle Bin carry sidecars, pairs, and catalog records together and undo from a journal.
- Compare shows four photos with analysis; baskets, selective browsing, the private vault, calendar browsing, the duplicate finder, archives, and folder sync work as ACDSee's do.
- No browse action writes an image byte of an original.

**Adjacency:** list=applicable @ D04 T05 §4; document=applicable @ D04 T05 §12; settings=applicable @ D04 T05 §2; reporting=applicable @ D04 T05 §11; notifications=applicable @ D04 T05 §2; permissions=applicable @ D04 T05 §6; audit=applicable @ D04 T05 §6; exchange=applicable @ D04 T05 §6; reverse=applicable @ D04 T05 §6

**Adjacency rationale:** The file list (§4) and the baskets (§8) are the lists. Archives, text file lists, and synced copies are files the user keeps (§12, §8). Settings are `Albumen.Browse.*` and `Albumen.Indexer.*` keys (views, overlays, columns, sort memory, indexed locations, exclusions, confirmations, sync jobs), each with a default and a named consumer, rendered by `D04 T14 §4`. The preview pane information and histogram, the information palette, the duplicate report, and sync logs are the reporting (§4, §7, §11, §12). Indexer progress and file-operation conflicts and results reach the Activity Manager and its notifications (§2, §6). Read-only media, locked and network files, protected folders, and the private vault's password are refused by name (§6, §9). One Serilog Information line per file operation and per sync run, plus the journal, is the audit trail (§6, §12). Drag and drop and the file clipboard with other programs, archives, and text file lists are the exchange (§6, §8, §12). File operations undo from the journal and delete goes to the Recycle Bin (§6).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The browse model: folders without import, browsed and library photos | D04 T02 §8, D04 T13 §1, D04 T11 §9 |  [ ]   |
|   2   |   §2    | The background indexer | §1, D04 T11 §1 |  [ ]   |
|   3   |   §3    | The folder tree, favorites, address bar, tabs, and home page | §1 |  [ ]   |
|   4   |   §4    | File list views, thumbnails, and the preview pane | §2, §3 |  [ ]   |
|   5   |   §5    | Sort, group, filter, and select in browse | §4 |  [ ]   |
|   6   |   §6    | File operations: copy, move, rename, delete, and undo | §4, D04 T11 §3 |  [ ]   |
|   7   |   §7    | Info palette, properties, and compare images | §4, D04 T01 §9 |  [ ]   |
|   8   |   §8    | Image basket and selective browsing | §5, D04 T11 §10 |  [ ]   |
|   9   |   §9    | The private folder | §6 |  [ ]   |
|  10   |   §10   | Calendar and timeline browsing | §2 |  [ ]   |
|  11   |   §11   | Duplicate finder | §2, §6 |  [ ]   |
|  12   |   §12   | Archives and folder sync | §6, D03 T17 §12 |  [ ]   |

---

## 1. The Browse Model: Folders Without Import, Browsed and Library Photos

ACDSee users open a folder and start culling; Lightroom users import first. Albumen does both: the catalog (`D04 T01 §5`) gains an `origin` column (`library` for imported photos, `browsed` for files seen while browsing), browse views are driven by a fast file-system enumeration sorted and grouped in memory, and the catalog is their cache of metadata, thumbnails, and hashes keyed by path, size, and last-write time. The first rating, label, keyword, or develop change on a browsed file creates its record (and its sidecar when sidecars are on) with no import step; "Add to Library" promotes browsed records in place, and import (`D04 T01 §6`) stays for cards and copies. Catalog: LP-0179 to LP-0182 (4 features: the Manage-mode browse window, browsed folders entering the catalog with no import step, records built automatically with per-file fields, and the thumbnails-to-viewer hand-off). -> SOURCE: parity-albumen-browse-model

**Fidelity:** Albumen browse window -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/browse/. **Corrected 2026-09-27:** cited `docs/captures/albumen/main-window/` (the shell of `D04 T01 §2`) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/shell-layout.md#albumen-darkroom-and-photo-manager, docs/design/components/ListTree/README.md, docs/design/components/Menu/README.md, docs/design/components/Toast/README.md, docs/design/components/Dialog/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user opens a folder and starts culling within a second, with nothing to import first. Consumer: the catalog records rating and keywording create, and every later browse section.
**Treatment:** ACDSee Manage mode's file list pane, contents bar, status bar, task pane, and maximized and full-screen file list, opened by File, Browse Folder, a folder dropped on the window, or `Albumen.exe --browse <folder> --select <file>`; Lightroom-style import stays one click away. Cheaper substitute that fails the checkpoint: an import dialog shown when a folder is opened.
**Chrome:** consume the grid of `D04 T01 §8`, the preview cache (`D04 T01 §7`), and the catalog. Do not add a second grid control.

**Requires:** display-session -- browsing and the frame-time measurement need an interactive desktop

**Freeze check:** Browsing opens every file read-only; creating a browsed record writes only the catalog and, when `Albumen.Metadata.WriteSidecars` is on, `<name>.xmp` through `AtomicFileWriter`; the catalog migration takes a backup first and is forward-only; a browse session (browse, rate, keyword, add to library) leaves every image file's SHA-256 and last-write time unchanged. Fixture source: `tests/fixtures/albumen/browse/` (created by this section).

- [ ] Add a forward-only catalog migration in `src/Albumen/Isotone.Albumen.Core/Catalog/Migrations/`: `images.origin` (`library` or `browsed`, existing rows `library`), a `browsed_folders` table, a cache key of path, size, and last-write time, and a lazily computed hash, tested on the previous version's catalog per `D04 T01 §5` (LP-0180, LP-0181). Done when: `BrowseModelTests.Migration` opens the old catalog with every photo as `library`.
- [ ] Add `FolderEnumerator` in `src/Albumen/Isotone.Albumen.Core/Browse/FolderEnumerator.cs` over `FindFirstFileExW` with `FindExInfoBasic` and `FIND_FIRST_EX_LARGE_FETCH`, returning name, size, times, and attributes without opening files. Done when: `BrowseBudgetTests` list a generated 5,000-JPEG folder in at most 300 ms, timing and machine quoted.
- [ ] Add `BrowseViewModel` in `src/Albumen/Isotone.Albumen.Desktop/ViewModels/Browse/`: the file-system listing is the source of truth, merged with cached catalog data by the cache key, sorted and grouped in memory, first-screen thumbnails from embedded EXIF thumbnails. Done when: `BrowseBudgetTests` show the first screen of thumbnails in at most 1.5 s and a reopened indexed folder in at most 200 ms.
- [ ] Invalidate a cached entry whose size or last-write time changed, re-reading its metadata and thumbnail. Done when: a test edits a fixture outside Albumen and the browse view shows the new thumbnail.
- [ ] Create a browsed record implicitly on the first rating, label, flag, keyword, or develop change, with per-file fields filled from the file's metadata, and its sidecar when sidecars are on; no import step (LP-0181, LP-0180). Done when: `BrowseModelTests.ImplicitRecord` rates an unrecorded file and finds one `browsed` record and, with sidecars on, its `.xmp`.
- [ ] Add Library, Add to Library, which flips `origin` to `library` in place as one undo step. Done when: a test adds three browsed photos, undoes, and finds them `browsed` again.
- [ ] Keep browsed records whose file vanished only when they hold user data, shown as missing and reconnectable through `D04 T06 §8`; prune the rest from the cache. Done when: a test deletes two fixtures outside Albumen and only the rated one remains, marked missing.
- [ ] Add the browse window in `src/Albumen/Isotone.Albumen.Desktop/Views/Browse/BrowseView.xaml` (LP-0179): file list pane on `D04 T01 §8`'s grid, contents bar, status bar (item count, selection size), task pane, and maximize and full-screen file list. Done when: the capture shows each element on a fixture folder.
- [ ] Open folders from File, Browse Folder, a folder dropped on the window, and `Albumen.exe --browse <folder> --select <file>` through single-instance forwarding. Done when: a driven `--browse` launch selects the named file.
- [ ] Add the viewer hand-off (LP-0182): double-click opens `AlbumenViewer.exe` through `D04 T04 §1`, Tab switches between browse and the viewer, and Esc hides the viewer. Done when: a driven double-click, Tab, and Esc round trip is captured.
- [ ] Retarget the viewer's `T` key from the library filter to browse at the viewer's folder with the file selected. Done when: a driven `T` in the viewer opens browse with the file selected.
- [ ] Implement `D04 T11 §9`'s `ICatalogRecordResolver` to create browsed records, so batch develop applies presets to RAW files selected in browse (LP-0978). Done when: a driven batch develop from a browsed folder of RAW files leaves `browsed` records holding the preset.
- [ ] Refuse an unreadable folder, a disconnected network path, and an access-denied folder by name in the contents bar, never an empty list shown as a real one. Done when: tests for each case assert the message.
- [ ] Add the unchanged-originals assertion over a browse session (browse, rate, keyword, develop, add to library). Done when: `UnchangedOriginalsTests.BrowseSession` passes.
- [ ] Commit fixtures under `tests/fixtures/albumen/browse/` (a generator script for the 5,000-JPEG folder with EXIF thumbnails, a RAW set, a folder with sidecars) with `reference.txt`. Done when: rerunning the generator reproduces the folder's file count and sizes.
- [ ] Commit captures under `docs/captures/albumen/browse/` and write `docs/user/albumen/browse.md` (browse versus import, Add to Library). Done when: the window and every entry point appear in captures and the page documents them.
- [ ] Commit: `"albumen: browse any folder without importing"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~BrowseModel|FullyQualifiedName~BrowseBudget|FullyQualifiedName~UnchangedOriginalsTests"` exits 0 with the listing, first-screen, and reopen timings quoted; captures committed under `docs/captures/albumen/browse/`. Cheaper substitute that fails: importing silently on open, which the origin assertion catches.

## 2. The Background Indexer

A whole photo drive becomes searchable only if something reads it in the background without slowing the app. One low-priority worker runs a priority queue (visible thumbnails first, then the selected folder, then the locations the user chose), pauses while the user develops or exports and, by setting, on battery, watches indexed locations for changes, and persists its progress across restarts; an opt-in per-user scheduled task runs `Albumen.exe --index` headless while Albumen is closed, with no service and no administrator rights. Catalog: LP-0183 to LP-0187 (5 features: high-quality and develop-aware thumbnails, excluded folders, indexing while idle and while closed, the catalog files dialog, and the indexer options). -> SOURCE: parity-albumen-indexer

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/indexer/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ToggleSwitch/README.md, docs/design/components/Button/README.md, docs/design/components/Progress/README.md, docs/design/components/Toast/README.md, docs/design/components/TextBox/README.md, docs/design/components/NumberBox/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user's whole photo drive becomes searchable in the background without slowing the app. Consumer: the catalog's cached metadata and the preview cache that browse, search, and the calendar read.
**Treatment:** ACDSee's Indexer options (index when idle, image files only or all, target catalog, folders to monitor), the Catalog Files dialog (add folders, file kinds, thumbnails, archive contents, RAW previews), and an Excluded Folders list with reset. Cheaper substitute that fails the checkpoint: a Windows service.
**Chrome:** consume §1, `D04 T11 §1`'s Activity Manager, the preview cache (`D04 T01 §7`), and Task Scheduler through `Microsoft.Win32.TaskScheduler` (MIT) or the `schtasks.exe` fallback, decided here. Do not add a second background queue.

**Requires:** display-session -- the idle-indexing drive and frame-time measurement need an interactive desktop

- [ ] Add `IndexerService` in `src/Albumen/Isotone.Albumen.Core/Indexing/IndexerService.cs`: a priority queue of visible items, the selected folder, and indexed locations, persisting progress in the catalog so a restart resumes (LP-0185, LP-0187). Done when: `IndexerQueueTests` stop mid-folder, restart, and resume at the next unindexed file.
- [ ] Run the worker at below-normal thread priority with background I/O priority (`SetThreadPriority` with `THREAD_MODE_BACKGROUND_BEGIN`). Done when: a test asserts the mode is set on the worker thread.
- [ ] Detect idle through `GetLastInputInfo` against `Albumen.Indexer.IdleSeconds` (default 60), pause while the user develops or exports, and pause on battery when `Albumen.Indexer.PauseOnBattery` (default true) is on. Done when: tests with a stubbed clock and power source assert each pause and resume.
- [ ] Register the indexer as an idle kind in `D04 T11 §1`'s Activity Manager with progress, pause, and resume, and alert the user through its notifications when a location becomes unreachable. Done when: the Activity Manager's Idle tab shows the indexer's counts in a capture.
- [ ] Add the headless `Albumen.exe --index` mode: no window, the same service, exiting when the queue empties or when `Albumen.exe` starts with a window. Done when: a driven `--index` run indexes a folder and exits with code 0, its log line quoted.
- [ ] Decide the scheduling path in `docs/dev/decisions.md`: `Microsoft.Win32.TaskScheduler` (MIT) versus `schtasks.exe`, with the license check and the reason. Done when: the row names this section and the choice.
- [ ] Add "Index while Albumen is closed" (default off): a per-user scheduled task with a logon trigger and an idle condition running `Albumen.exe --index`, removed when the option is turned off or Albumen is uninstalled; no service and no administrator rights (LP-0185). Done when: a driven toggle creates and removes the task, verified by `schtasks /query`.
- [ ] Watch indexed locations with `FileSystemWatcher`, applying create, rename, and delete, and rescanning a folder whose watcher raised `InternalBufferOverflowException` (LP-0187). Done when: `IndexerWatcherTests` cover each event and a forced overflow triggers the rescan.
- [ ] Add excluded folders with reset to defaults in `Albumen.Indexer.Exclusions` (defaults: Windows, Program Files, the recycle bins, Albumen's own data) (LP-0184). Done when: an excluded folder is never enqueued and reset restores the defaults.
- [ ] Add the indexer options in `src/Albumen/Isotone.Albumen.Desktop/Views/Indexing/IndexerOptionsPage.xaml` (LP-0187): index when idle, images only or all file types, target catalog, and folders to monitor, in `Albumen.Indexer.*`. Done when: a driven change of each option is read back from the settings file.
- [ ] Add the Catalog Files dialog (LP-0186): add folders without browsing them, file kinds, thumbnails, RAW previews, and archive contents, which stays disabled with the tooltip "Arrives with archive browsing (D04 T05 §12)" until §12 registers archives. Done when: adding a folder through the dialog enqueues it, and the archive option names §12.
- [ ] Replace embedded thumbnails with high-quality, develop-aware thumbnails in the background, extending `D04 T01 §7` (LP-0183). Done when: a developed photo's thumbnail matches its develop render downscaled within 2/255 after the indexer's pass.
- [ ] Measure the budget: at least 50 JPEGs per second (metadata plus thumbnail) with the foreground frame time under 16 ms while scrolling, on the reference machine. Done when: `IndexerBudgetTests` quote throughput and the frame-time median and 99th percentile.
- [ ] Commit captures under `docs/captures/albumen/indexer/` and write `docs/user/albumen/indexer.md`. Done when: the options page, the Catalog Files dialog, and the Activity Manager entry appear in captures and the page documents them.
- [ ] Remove the index task on uninstall: `installer/Albumen.iss` `[UninstallRun]` runs `Albumen.exe --unregister-index-task` (**Groomed 2026-09-28:** only turning the option off removed it). Done when: an uninstall with the option on leaves `schtasks /query` without the task (quoted).
- [ ] Commit: `"albumen: a background indexer for chosen folders"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~IndexerQueue|FullyQualifiedName~IndexerWatcher|FullyQualifiedName~IndexerBudget"` exits 0; a driven index of a 20,000-file drive reports throughput and frame times. Cheaper substitute that fails: indexing on the UI thread, which the frame-time budget catches.

## 3. The Folder Tree, Favorites, Address Bar, Tabs, and Home Page

Browse is only as fast as its navigation: a folder tree with drives, removable devices, and shell folders, a shortcuts and favorites pane, back, forward, and home, an address box for typed and pasted paths with recent folders, multi-folder and recursive browsing, tabs with per-tab state, a startup location, and a home page with quick searches and actions. Catalog: LP-0188 to LP-0197 (10 features: toolbar navigation, the folders pane, the shortcuts pane, the home page and its action buttons, multi-folder browsing, tabs, the startup location, per-tab state, and the address box). -> SOURCE: parity-albumen-browse-navigation

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/folders/`, `docs/captures/albumen/tabs/`, and `docs/captures/albumen/home/`.
**Design:** docs/design/shell-layout.md#albumen-darkroom-and-photo-manager, docs/design/components/ListTree/README.md, docs/design/components/Tabs/README.md, docs/design/components/TextBox/README.md, docs/design/components/Button/README.md, docs/design/components/Menu/README.md, docs/design/components/ContextMenu/README.md, docs/design/shell-layout.md#splash-and-home, docs/design/components/Icons/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user moves around their disks as fast as in Explorer and keeps several places open. Consumer: §1's browse view and the settings that restore the session.
**Treatment:** ACDSee's Folders pane with Easy-Select bars, Shortcuts pane, address box, browsing tabs, and Home page (quick search, recently modified and added, tagged and unnamed-face searches, import and maintenance buttons). Cheaper substitute that fails the checkpoint: a single folder picker dialog.
**Chrome:** consume `Isotone.UI` tree and tab styles, the settings store, and the icon catalog. Do not add a second folder picker.

**Requires:** display-session -- navigation panes and tabs need an interactive desktop

**Freeze check:** Delete Folder moves the folder to the Recycle Bin through `IFileOperation` with `FOFX_RECYCLEONDELETE` after a confirmation naming its file count, never a permanent delete; New Folder and Rename Folder write no file inside the folder, and a renamed folder's catalog paths update in one transaction with one undo step. Fixture source: `tests/fixtures/albumen/browse/` (created by §1).

- [ ] Add `FolderTreeViewModel` in `src/Albumen/Isotone.Albumen.Desktop/ViewModels/Browse/` (LP-0189): drives, removable devices refreshed on `WM_DEVICECHANGE`, and common shell folders (Pictures, Desktop, Downloads, OneDrive when present), with New Folder, Delete (to the Recycle Bin), and Rename Folder. Done when: `FolderNavigationTests` assert a USB insert adds the drive node and New Folder then Undo leaves no folder.
- [ ] Add home, back, and forward with a per-tab history (LP-0188). Done when: `FolderNavigationTests` walk three folders back and forward in two tabs independently.
- [ ] Add the Shortcuts pane (LP-0190): shortcuts to files, folders, and programs, folders of shortcuts, drag to create, run, rename, and delete, in `Albumen.Browse.Shortcuts`. Done when: a shortcut dragged in survives a restart and opens its folder.
- [ ] Add multi-folder and recursive browsing (LP-0193): Easy-Select check bars on the tree, Ctrl-click with subfolders, load all subfolders, and the tree context menu. Done when: checking two folders lists both folders' files in one view.
- [ ] Add tabs (LP-0194): new, open in new tab, middle-click, duplicate, close, close others, close left, close right, and next and previous tab. Done when: each command's test passes.
- [ ] Keep per-tab state (LP-0196): panes, filters, groups, and searches per tab, drag files between tabs (a move or copy through §6 once it ships, a hint before), and the last tab restored. Done when: a driven session with four tabs restarts and restores each tab's folder and filter.
- [ ] Add the address box (LP-0197): typed or pasted paths with completion, UNC and relative paths, recent folders with a count setting and clear, and focus options. Done when: `AddressBoxTests` parse local, UNC, `%USERPROFILE%`, and relative paths.
- [ ] Add the startup location (LP-0195) in `Albumen.Browse.Startup`: the home page, a start folder, or reopen the last or all tabs. Done when: each choice's driven restart lands where set.
- [ ] Add the home page in `src/Albumen/Isotone.Albumen.Desktop/Views/Browse/HomePage.xaml` (LP-0191): a quick search bar, recently modified and recently added with time windows and a date basis, and a tagged search. Done when: the recently added list shows files indexed in the last day of the fixture set.
- [ ] Show unnamed-face searches on the home page only when `D04 T10 §3` has shipped faces, hidden with no placeholder until then (LP-0191). Done when: `python scripts/todo-graph.py resolve 'D04 T10 §3'` resolves and a test asserts the tile is absent without faces.
- [ ] Add the home page action buttons (LP-0192): Import (`D04 T01 §6`), catalog backup and maintenance, and Catalog Files (§2). Done when: each button opens its target in a driven run.
- [ ] Refuse a vanished or access-denied folder chosen in the tree or the address box by name, keeping the current view. Done when: a test types a missing path and the message names it.
- [ ] Commit captures under `docs/captures/albumen/folders/`, `docs/captures/albumen/tabs/`, and `docs/captures/albumen/home/` and write `docs/user/albumen/browse-navigation.md`. Done when: every pane and command appears in a capture and the page documents it.
- [ ] Commit: `"albumen: folder tree, favorites, address bar, tabs, and home page"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~FolderNavigation|FullyQualifiedName~AddressBox"` exits 0; a driven session opens four tabs, restarts, and restores them, captured under `docs/captures/albumen/tabs/`. Cheaper substitute that fails: one folder at a time, which the tab restore test catches.

## 4. File List Views, Thumbnails, and the Preview Pane

The file list is where a photographer culls, so it offers every view ACDSee has on the one virtualizing grid of `D04 T01 §8`: thumbnails, tiles, thumbs plus details, filmstrip, icons, list, and details, with adjustable size and cell shape, overlay icons and their options, details columns, thumbnail styles and info fields, hover pop-ups, file-type choices, refresh and remove from list, and a preview pane with information and a histogram, all within the 16 ms frame budget. Catalog: LP-0198 to LP-0208 (11 features: the preview pane, view modes, size and cell shape, overlay icons, overlay options, details columns, file types shown, thumbnail style, hover pop-ups, info fields, and refresh and remove from list). -> SOURCE: parity-albumen-file-list

**Fidelity:** Browse file list views and the preview pane -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/file-list/. **Corrected 2026-09-27:** cited `docs/captures/albumen/main-window/` (the grid baseline from `D04 T01 §8`) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Slider/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Tooltip/README.md, new surface: docs/design/components/AlbumenGrid/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user sees exactly the information they cull by, in the layout they like, at scroll speed. Consumer: the browse view and every later section that lists files.
**Treatment:** ACDSee's view modes, thumbnail overlay icons with per-overlay toggles and color highlight cycling, the details columns editor, thumbnail style and info options, hover pop-ups, and the preview pane (image, information, histogram, delay, progressive instant preview). Cheaper substitute that fails the checkpoint: fixed thumbnails with no overlays.
**Chrome:** extend `D04 T01 §8`'s virtualizing grid, the preview cache, and the histogram control moved to `Isotone.UI` by `D04 T02 §3`. Do not add a second grid or a second histogram.

**Requires:** display-session -- views and frame times need an interactive desktop

- [ ] Write or extend the design spec `docs/design/components/AlbumenGrid/README.md` and `preview.html` with the browse view modes (tiles, details, film), overlay icons, info fields, and hover pop-ups (anatomy, every state, tokens, sizes; `D04 T01 §8` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Add the view modes (LP-0199): thumbnails, tiles, thumbs plus details, filmstrip, icons, list, and details, each a template on the virtualizing panel of `D04 T01 §8`. Done when: `FileListViewModelTests` switch every mode and the item count stays equal.
- [ ] Add size and cell shape (LP-0200): a zoom slider, size presets, portrait, landscape, or custom ratio cells, and spacing, in `Albumen.Browse.Thumbnails.*`. Done when: a custom 3:2 cell renders a portrait photo letterboxed inside it in a capture.
- [ ] Add overlay icons from an `IOverlayProvider` per kind (LP-0201): rating, label, format, category, collection, stack, shortcut, offline, excluded, tagged, rejected, geotagged, auto-rotated, developed, edited, sidecar, and snapshots. Done when: `OverlayProviderTests` assert each provider's condition on the fixtures.
- [ ] Add overlay display options (LP-0202): modes, color highlight cycling, per-overlay toggles, empty overlays on hover, and stack bars, in `Albumen.Browse.Overlays.*`. Done when: each toggle hides its overlay without a restart.
- [ ] Add details columns (LP-0203): choose, add, remove, reorder, reset, grid lines, full row select, auto width, highlight and click-to-sort, and any metadata field as a column. Done when: a column set with an EXIF lens column persists across a restart.
- [ ] Add file types shown (LP-0204): images, PDF, folders, archives, Office documents, hidden files, and THM and XMP files, in `Albumen.Browse.ShowKinds`. Done when: turning XMP on lists the sidecars and turning it off hides them.
- [ ] Add thumbnail style (LP-0205): drop shadow, slide background, folder style with content thumbnails, borders, colors, and high-quality scaling. Done when: each style option appears in a capture.
- [ ] Add info fields on thumbnails and tiles (LP-0207): file name and chosen metadata fields. Done when: choosing shutter speed shows it under each thumbnail in a capture.
- [ ] Add hover pop-ups (LP-0206): on hover or with Shift, auto hide, a larger thumbnail and chosen information. Done when: a driven hover shows the pop-up with the chosen fields.
- [ ] Add Refresh Thumbnails and Remove from List (which never deletes a file) (LP-0208). Done when: a test removes three items from the list and the folder listing still counts them.
- [ ] Add the preview pane in `src/Albumen/Isotone.Albumen.Desktop/Views/Browse/PreviewPane.xaml` (LP-0198): the image, information, the histogram from `Isotone.UI`, a display delay, size, progressive instant preview, and chosen fields. Done when: selecting a photo shows the embedded preview first and the full preview after, captured.
- [ ] Re-measure the frame budget with every overlay on: median under 16 ms while scrolling the 50,000-image catalog of `D04 T01 §8` in thumbnails and details views. Done when: the timings are quoted per view.
- [ ] Commit captures under `docs/captures/albumen/file-list/` (every view mode) and `docs/captures/albumen/preview-pane/` and write `docs/user/albumen/file-list.md`. Done when: every view and option appears in a capture and the page documents it.
- [ ] Commit: `"albumen: browse views, overlays, columns, and the preview pane"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~FileListViewModel|FullyQualifiedName~OverlayProvider"` exits 0; frame times with all overlays are quoted per view; captures of each view mode are committed. Cheaper substitute that fails: a non-virtualized details view, which the frame budget catches.

## 5. Sort, Group, Filter, and Select in Browse

Browse sorts, groups, filters, and selects the way ACDSee's menus do: natural name order, every date and metadata field, per-folder sort memory with a custom drag order, grouping by any attribute or processed state with collapsible headers, filters that share the library's rule model, and the full selection command set. Catalog: LP-0209 to LP-0213, LP-1058 (6 features: filters, grouping, sorting, selection commands, per-folder sort memory, and grouping by processed state). -> SOURCE: parity-albumen-browse-sort

**Fidelity:** Browse sort, group, filter, and select -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/browse-sort/. **Corrected 2026-09-27:** cited `docs/captures/albumen/file-list/` (the view §4 captured) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Menu/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/ContextMenu/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user orders and narrows a folder to what they need and selects it in one step. Consumer: §4's file list and every command that acts on the selection.
**Treatment:** ACDSee's Sort, Group, Filter, and Select menus with group headers, a table of contents, and select-group-by-header. Cheaper substitute that fails the checkpoint: sort by name only.
**Chrome:** consume §4, the catalog's indexed columns, and `D04 T06 §4`'s filter rule model when it has shipped, otherwise `D04 T01 §8`'s filter set. Do not add a second filter model.

**Requires:** display-session -- grouping and selection need an interactive desktop

- [ ] Add `BrowseSort` in `src/Albumen/Isotone.Albumen.Core/Browse/BrowseSort.cs` (LP-0211): natural name order with `StrCmpLogicalW` semantics, size, type, dates, EXIF date, dimensions, DPI, megapixels, orientation, caption, rating, tag, any metadata field, direction, and full path, extending `D04 T01 §8`. Done when: `BrowseSortTests` pass a natural-order table (`img2` before `img10`) and each metadata sort.
- [ ] Remember the sort per folder and keep a custom drag order per folder in `browsed_folders` (LP-0213). Done when: a folder reopened after a restart keeps its drag order.
- [ ] Add grouping (LP-0210): by any attribute, collapsible groups, hover preview on a collapsed header, a table of contents, group order, and select group by header. Done when: `BrowseGroupTests` group by camera and select one group by its header.
- [ ] Add grouping by processed state (developed, edited, untouched) (LP-1058). Done when: a folder with one developed photo shows it in the Developed group.
- [ ] Add filters (LP-0209): rating, category, label, and advanced filters through `D04 T06 §4`'s rule model once it ships, otherwise `D04 T01 §8`'s filter set. Done when: filtering by three stars and a red label shows the expected count.
- [ ] Add selection commands (LP-0212): click, Ctrl, Shift, Select All, All Files, All Images, Tagged, By Rating, Clear, Invert, and auto-select newly added files. Done when: `SelectionCommandTests` assert each command's selection.
- [ ] Keep sorting, grouping, and filtering a 5,000-file folder under 200 ms. Done when: the timing is quoted from `BrowseSortTests`.
- [ ] Commit captures under `docs/captures/albumen/browse-sort/` and extend `docs/user/albumen/file-list.md` with sorting, grouping, filtering, and selection. Done when: every menu appears in a capture and the page documents it.
- [ ] Commit: `"albumen: sort, group, filter, and select in browse"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~BrowseSort|FullyQualifiedName~BrowseGroup|FullyQualifiedName~SelectionCommand"` exits 0; a grouped and filtered 5,000-file folder responds under 200 ms (quoted). Cheaper substitute that fails: an ordinal string sort, which the natural-order table catches.

## 6. File Operations: Copy, Move, Rename, Delete, and Undo

Organizing files on disk from Albumen must not break the catalog or lose a sidecar. Photos are copied, moved, renamed inline, and deleted to the Recycle Bin through the Windows shell's `IFileOperation`, with sidecars, related files, and RAW+JPEG partners traveling together, catalog records following, a collision policy and replace dialog, the file clipboard and drag and drop with other programs, pixel or path copy, the Explorer context menu, and one undo journal that extends `D04 T11 §3`'s rename journal. File operations move and delete files; they never rewrite an image's bytes. Catalog: LP-0214 to LP-0225, LP-0973 (13 features: copy, delete to the Recycle Bin, inline rename, copy and move to a folder, traveling sidecars and related files, collision policy, pixel or path copy, the file clipboard and drag and drop, the replace dialog, catalog links kept, the Explorer context menu, sidecars moved with the photo, and dragging files to other programs). -> SOURCE: parity-albumen-file-operations

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/file-operations/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md, docs/design/components/Toast/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user organizes files on disk from Albumen without breaking the catalog or losing a sidecar, and can undo a mistake. Consumer: the files on disk, their sidecars, and the catalog records that follow them.
**Treatment:** ACDSee's Copy To and Move To dialogs (folder tree, recent folders, create folder), the Confirm File Replace dialog (both thumbnails, replace, rename to, skip, delete source or destination, apply to all, cancel), inline rename, and the shell context menu. Cheaper substitute that fails the checkpoint: `File.Move` of the image alone.
**Chrome:** consume `IFileOperation` for copy, move, and recycle, the catalog, `D04 T11 §3`'s journal, and `D04 T13 §5`'s pairs. Do not add a second journal or a second recycle path.

**Requires:** display-session -- file dialogs, drag and drop, and the shell menu need an interactive desktop

**Freeze check:** Copy, move, and rename never rewrite a file's bytes (the SHA-256 of every moved or copied file equals its source); a photo's sidecar and RAW+JPEG partner move in the same journaled step; delete goes to the Recycle Bin, and permanent delete needs Shift and a named confirmation; a cross-volume move deletes the source only after the copy is verified by hash. Fixture source: `tests/fixtures/albumen/file-ops/` (created by this section).

- [ ] Add `FileOperationService` in `src/Albumen/Isotone.Albumen.Core/Browse/Files/FileOperationService.cs` over `IFileOperation` for copy (LP-0214), move, and recycle, reporting progress and conflicts to `D04 T11 §1`'s Activity Manager. Done when: `FileOperationServiceTests` copy and move a fixture set and every hash matches.
- [ ] Extend `D04 T11 §3`'s `RenameJournal` into `FileOperationJournal` covering copy, move, rename, and recycle, with Edit, Undo for the last operation while the files are where Albumen put them. Done when: a test undoes a move of 20 files and every file and record is back.
- [ ] Add Copy To and Move To dialogs (LP-0217): folder tree, recent folders, create folder, and dragging onto tree folders. Done when: a driven Move To a new folder is captured and undone.
- [ ] Add delete to the Recycle Bin with `FOFX_RECYCLEONDELETE` and confirmation settings in `Albumen.Browse.ConfirmDelete` (LP-0215); permanent delete only with Shift and a named confirmation. Done when: a test recycles a file and restores it through the shell, and a Shift-delete without confirmation is refused.
- [ ] Add inline rename of a file or folder with click-to-edit (LP-0216), recorded in the journal; batch rename stays `D04 T11 §3`. Done when: a driven inline rename is undone.
- [ ] Move `.xmp` and `.thm` sidecars, related files (same base name), and `D04 T13 §5` RAW+JPEG partners with each photo (LP-0218, LP-0225). Done when: a test moves a pair with sidecars and every file arrives together.
- [ ] Keep catalog records attached through moves and renames inside Albumen (LP-0223); moves outside Albumen reconnect through `D04 T06 §8`. Done when: a moved photo keeps its rating and keywords in the catalog.
- [ ] Route `D04 T13 §1`'s `ExtensionFixService` through the journal so an extension fix is one journaled rename. Done when: an extension fix appears in the journal and undoes.
- [ ] Add the collision policy (LP-0219): ask, rename with a separator, replace, or skip, in `Albumen.Browse.Collision`. Done when: each policy's test row passes.
- [ ] Add the Confirm File Replace dialog (LP-0222): both thumbnails with sizes and dates, replace, rename to, skip, delete source or destination, apply to all, and cancel. Done when: a driven collision shows both thumbnails, captured.
- [ ] Add the file clipboard (LP-0221): cut, copy, and paste files keeping catalog data, with a confirmation for drag moves. Done when: a paste into another folder keeps the photo's rating in its new record.
- [ ] Add drag to other programs (LP-0973, LP-0221), which exports the files with `CF_HDROP` plus a PNG for pixel targets, and imports files dropped from other programs as a copy or move. Done when: `DragDropFormatTests` assert both formats on the data object and a driven drag into Explorer copies the file.
- [ ] Add Copy Image (pixels) and Copy Path to the clipboard (LP-0220). Done when: a test reads back the clipboard's bitmap size and the path text.
- [ ] Host the Windows Explorer context menu in the file list through `IContextMenu` (LP-0224). Done when: a driven right-click shows the shell's menu for the selected files, captured.
- [ ] Refuse a read-only destination, a locked file, and a folder whose permissions deny the write by name, keeping the rest of the operation. Done when: a test with one locked file moves the others and names the locked one.
- [ ] Log one Serilog Information line per file operation (`{Operation} {Count} {Source} -> {Target}`) as the audit trail beside the journal. Done when: a Serilog test sink asserts the line.
- [ ] Commit fixtures under `tests/fixtures/albumen/file-ops/` (RAW+JPEG pairs with sidecars, a locked-file recipe, a read-only folder recipe) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/albumen/file-operations/` and write `docs/user/albumen/file-operations.md`. Done when: every dialog appears in a capture and the page documents it.
- [ ] Repoint `D04 T04 §6`'s `ViewerFileOperations` (delete, rename, move, copy) onto `FileOperationService` and `FileOperationJournal`, so viewer file operations keep catalog records attached and undo from the journal (Ctrl+Z in the viewer while no pixel edit is pending) (**Groomed 2026-09-28:** nothing repointed them, which left viewer renames and moves detached from the catalog and without undo). Done when: a viewer F7 move of a RAW+JPEG+XMP trio appears in the journal and undoes, and `grep -rn "FOFX_RECYCLEONDELETE" src/Albumen` prints one path.
- [ ] Commit: `"albumen: file operations with sidecars, pairs, and undo"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~FileOperationService|FullyQualifiedName~DragDropFormat"` exits 0; a driven move of 200 RAW+JPEG pairs with sidecars between drives is undone and the catalog is quoted consistent. Cheaper substitute that fails: moving images without sidecars, which the travel test catches.

## 7. Info Palette, Properties, and Compare Images

Picking the best of a burst needs photos side by side with their settings. Compare Images shows up to four photos with a comparison list, layouts, synchronized zoom and pan, analysis (exposure warning, property differences in bold, histograms, a difference image), and culling and file actions, extending the two-up compare of `D04 T01 §9`; the information palette overlays camera and exposure data on the image. Saving from compare writes a new file, never the original. Catalog: LP-0226 to LP-0231 (6 features: the compare viewer, the information palette, culling and file actions, zoom and pan, analysis, and comparing the current image with another). -> SOURCE: parity-albumen-compare

**Fidelity:** Four-up compare and the information palette -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/info-palette/. **Corrected 2026-09-27:** cited `docs/captures/albumen/compare/` (the baseline from `D04 T01 §9`) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Button/README.md, docs/design/components/Menu/README.md, new surface: docs/design/components/AlbumenCompare/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user picks the best of a burst by comparing sharpness and settings side by side. Consumer: the ratings, tags, and deletions the compare view applies.
**Treatment:** ACDSee's Compare Images viewer (up to four, comparison list, send to view, drag in, swap, remove, layouts, zoom and pan lock, exposure warning, bold differences, histograms, tag, rate, categories, save as a new file, delete) and Info Palette. Cheaper substitute that fails the checkpoint: two windows opened side by side.
**Chrome:** extend `D04 T01 §9`'s compare view model, the histogram control, and §6's recycle. Do not add a second compare view.

**Requires:** display-session -- compare and the palette need an interactive desktop

- [ ] Write or extend the design spec `docs/design/components/AlbumenCompare/README.md` and `preview.html` with the four-up compare with locks and the analysis overlays (anatomy, every state, tokens, sizes; `D04 T01 §9` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Extend `D04 T01 §9`'s compare view model to up to four images (LP-0226): a comparison list, send to view, drag in, swap next or previous, remove, and one to four layouts. Done when: `CompareViewModelTests` load four photos and swap two.
- [ ] Add zoom and pan (LP-0229): actual size, fit, fit width and height, zoom to a value, and zoom and pan locks. Done when: with both locks on, zooming one pane zooms all four to the same scale and offset.
- [ ] Add analysis (LP-0230): an exposure warning overlay, property differences in bold, per-image histograms, and a metadata field setup. Done when: two photos differing only in ISO show ISO bold, captured.
- [ ] Add compare the current image with another (LP-0231): synchronized zoom and scroll, next and previous, and a difference image rendered as the absolute per-channel difference. Done when: `CompareViewModelTests` assert the difference image of two known fixtures pixel for pixel.
- [ ] Add actions (LP-0228): tag, tag all, rate, categories, Save As a new file (never the original), and delete to the Recycle Bin through §6. Done when: rating in compare updates the catalog and Save As refuses an original's path.
- [ ] Add the information palette in `src/Albumen/Isotone.Albumen.Desktop/Views/Browse/InfoPalette.xaml` (LP-0227): camera, lens, dimensions, size, exposure program, white balance, metering, flash, RAW, ISO, aperture, shutter, compensation, focal length, a chosen bottom line, and a position and opacity setting. Done when: `InfoPaletteTests` assert each field against the fixture's EXIF.
- [ ] Add keyboard access and logging: `Alt+C` opens compare with the selection, `1` to `4` pick the layout, `L` toggles both locks, and each rating, tag, delete, and Save As logs one Serilog Information line. Done when: a Serilog test sink asserts the lines after a keyboard-only compare session.
- [ ] Commit captures under `docs/captures/albumen/compare/` (four-up, locks, difference image) and `docs/captures/albumen/info-palette/` and write `docs/user/albumen/compare.md`. Done when: every control appears in a capture and the page documents it.
- [ ] Commit: `"albumen: four-up compare with analysis and the information palette"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~CompareViewModel|FullyQualifiedName~InfoPalette"` exits 0 with the synchronized zoom and difference-image values asserted; a driven four-up compare with zoom lock is captured. Cheaper substitute that fails: static side-by-side images, which the sync test catches.

## 8. Image Basket and Selective Browsing

Gathering photos from many folders for one task should not move them. Up to five image baskets collect references from browse, the viewer, or Explorer; selective browsing combines folder, catalog, and date criteria with match any or all; and file lists load and save as text files in the format `D04 T11 §10`'s batch dialog uses. Catalog: LP-0232 to LP-0235 (4 features: selective browsing, the image basket, adding the viewed image to the basket, and text file lists). -> SOURCE: parity-albumen-basket

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/basket/` and `docs/captures/albumen/selective-browsing/`.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/TextBox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user gathers photos from many folders for one task without moving them. Consumer: any command run on a basket's contents (batch, export, compare).
**Treatment:** ACDSee's Image Basket pane (baskets, add, remove, clear, rename, delete, active basket) and Selective Browsing pane (criteria rows, include toggles, any or all, auto hide). Cheaper substitute that fails the checkpoint: a temporary collection that copies files.
**Chrome:** consume §5, the catalog, `D04 T11 §10`'s `BatchFileList` text format, and `D04 T06 §7`'s criteria model when it has shipped. Do not add a second criteria model or a second list format.

**Requires:** display-session -- the panes need an interactive desktop

- [ ] Add `ImageBasketService` in `src/Albumen/Isotone.Albumen.Core/Browse/ImageBasketService.cs` (LP-0233): up to five baskets persisted in the catalog as references, with add, remove, clear, rename, delete, and the active basket. Done when: `ImageBasketTests` fill two baskets, restart, and find both.
- [ ] Add to the active basket from browse (a command and a drop onto the pane) and from Explorer (a drop onto the pane) (LP-0233). Done when: a driven drop of three Explorer files lists them in the basket.
- [ ] Add the viewer's Add to Basket command, forwarded from `AlbumenViewer.exe` to Albumen through single-instance forwarding (LP-0234). Done when: a driven add from the viewer appears in the active basket.
- [ ] Keep baskets reference-only: no file is moved or copied by adding, removing, or clearing. Done when: `ImageBasketTests` assert the source folders' listings unchanged.
- [ ] Add the Image Basket pane in `src/Albumen/Isotone.Albumen.Desktop/Views/Browse/ImageBasketPane.xaml` with running any command on the basket's contents. Done when: a driven batch convert from a basket lists its files.
- [ ] Add selective browsing (LP-0232): criteria rows over folders, catalog fields, and dates, include toggles, match any or all, remove and clear, and auto hide, through `D04 T06 §7`'s criteria model once it ships, otherwise the `D04 T01 §8` filter set. Done when: `SelectiveBrowsingTests` combine two folders and a date range with match all and assert the count.
- [ ] Load and save file lists as UTF-8 text, one path per line, sharing `D04 T11 §10`'s format (LP-0235). Done when: `FileListTextTests` round-trip a list saved here through the batch dialog.
- [ ] Commit captures under `docs/captures/albumen/basket/` and `docs/captures/albumen/selective-browsing/` and write `docs/user/albumen/basket.md`. Done when: both panes appear in captures and the page documents them.
- [ ] Commit: `"albumen: image baskets and selective browsing"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ImageBasket|FullyQualifiedName~SelectiveBrowsing|FullyQualifiedName~FileListText"` exits 0; a driven basket filled from three folders and the viewer is captured. Cheaper substitute that fails: a basket that copies files, which the no-move assertion catches.

## 9. The Private Folder

Some photos should stay out of sight on a shared machine. The private folder is a password-protected, encrypted vault under Albumen's app data, not a hidden folder: AES-256-GCM per file with a PBKDF2-SHA256 key from the user's password, files decrypted to memory only, sources moved in only after the encrypted copy is verified, and an honest statement that it is no substitute for disk encryption and that a lost password cannot be recovered. Catalog: LP-0236 to LP-0237 (2 features: the vault and its contents). -> SOURCE: parity-albumen-private-folder

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/private-folder/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/Button/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Toast/README.md, docs/design/components/ListTree/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user keeps some photos out of sight on a shared machine. Consumer: the vault on disk and the restore that returns the files.
**Treatment:** ACDSee's Private Folder (create with a password, open, close, add, restore, delete) with an explicit statement that it is not disk encryption and that a lost password cannot be recovered. Cheaper substitute that fails the checkpoint: a hidden folder attribute.
**Chrome:** consume `AesGcm` and `Rfc2898DeriveBytes` from .NET, §6's verified moves and recycle, and `Isotone.UI` dialogs. Do not add a crypto package.

**Requires:** display-session -- the vault dialogs need an interactive desktop

**Freeze check:** Adding a file writes its encrypted copy through `AtomicFileWriter`, decrypts it back, and compares the hash before the source is recycled through §6; restoring writes the plaintext to the chosen folder and verifies it before the vault entry is removed; no plaintext is ever written to disk while the vault is open. Fixture source: `tests/fixtures/albumen/private-vault/` (created by this section).

- [ ] Add `PrivateVault` in `src/Albumen/Isotone.Albumen.Core/Browse/Private/PrivateVault.cs` (LP-0236): a PBKDF2-SHA256 key (600,000 iterations, a per-vault salt), AES-256-GCM per file with a random 96-bit nonce, and an encrypted index, stored under `%LOCALAPPDATA%\Rizonesoft\Albumen\private\`. Done when: `PrivateVaultTests` round-trip a file and a flipped ciphertext byte fails the GCM tag check.
- [ ] Add create, open, and close, with the vault hidden from browse while closed and the key wiped from memory on close (LP-0236). Done when: a test closes the vault and the browse tree no longer lists it.
- [ ] Decrypt files to memory only for viewing and thumbnails, never to a temp file. Done when: `PrivateVaultTests.NoPlaintextOnDisk` scans the temp and app-data folders after viewing and closing and finds no plaintext match.
- [ ] Add files (LP-0237) with a warning dialog: encrypt, decrypt and compare the hash, remove the catalog data, then recycle the source through §6. Done when: a test adds a file and finds the source in the Recycle Bin only after the verification passed.
- [ ] Add restore to a normal folder and delete from the vault (LP-0237). Done when: a restored file's hash equals the original source's.
- [ ] Refuse a wrong password with an increasing delay, and say in the create dialog that no recovery exists and that the vault is not disk encryption. Done when: a test asserts the delay grows and the dialog text is captured.
- [ ] Log one Serilog Information line per add, restore, and delete, naming counts and never file names. Done when: a Serilog test sink asserts the line holds no file name.
- [ ] Commit captures under `docs/captures/albumen/private-folder/` and write `docs/user/albumen/private-folder.md` with its limits. Done when: every dialog appears in a capture and the page states the limits.
- [ ] Commit: `"albumen: an encrypted private folder"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~PrivateVault"` exits 0 covering the round trip, a wrong password, tamper detection by the GCM tag, and no plaintext on disk after close; a driven add, close, reopen, and restore cycle is captured with source and restored hashes quoted equal. Cheaper substitute that fails: a hidden attribute, which the no-plaintext test catches.

## 10. Calendar and Timeline Browsing

Photos are remembered by when they were taken, not by folder. A calendar pane browses by events, years, months, and days with a photo calendar, hover previews, a table of contents, skipped empty dates, a chosen date basis, filters, week and clock options, and per-date events with a description and chosen thumbnail, all from indexed catalog queries rather than folder enumeration. Catalog: LP-0238 to LP-0241 (4 features: the calendar pane, the date basis, calendar options, and calendar events). -> SOURCE: parity-albumen-calendar

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/calendar/`.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/TextBox/README.md, docs/design/components/ListTree/README.md, new surface: docs/design/components/AlbumenCalendar/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user finds photos by when they were taken without knowing the folder. Consumer: §4's file list, which shows the chosen date's photos.
**Treatment:** ACDSee's Calendar pane (events, year, month, and day views, the photo calendar, a floating pane) and its options. Cheaper substitute that fails the checkpoint: a date-range filter only.
**Chrome:** consume the catalog's indexed dates and the preview cache. Do not enumerate folders per click.

**Requires:** display-session -- the calendar pane needs an interactive desktop

- [ ] Write the design spec `docs/design/components/AlbumenCalendar/README.md` and `preview.html` (the calendar and timeline: year, month, and day cells with counts, events, and the empty states; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Add `CalendarViewModel` in `src/Albumen/Isotone.Albumen.Desktop/ViewModels/Browse/CalendarViewModel.cs` (LP-0238): events, year, month, and day views, a photo calendar with hover previews, a table of contents, skip empty dates, and a floating pane. Done when: a driven month view shows per-day counts equal to the catalog query's.
- [ ] Add the date basis (LP-0239): catalog date, date taken, modified, created, or loaded, in `Albumen.Browse.Calendar.DateBasis`. Done when: `CalendarQueryTests` return different counts per basis on the fixture set.
- [ ] Count in the photo's own capture time zone where the EXIF offset exists, else local time, stated in the pane's tooltip. Done when: `CalendarQueryTests` place a photo taken at 23:30 UTC-5 on its local day.
- [ ] Add options (LP-0240): filters, images and media only, start of week, and a 12- or 24-hour clock. Done when: switching the week start moves the month grid's first column.
- [ ] Add events (LP-0241): a description and chosen thumbnail per date, and restore the default thumbnail, stored in the catalog. Done when: `CalendarEventTests` persist an event across a restart.
- [ ] Serve counts from indexed queries in under 200 ms on the 50,000-image catalog of `D04 T01 §8`. Done when: the timing is quoted from `CalendarQueryTests`.
- [ ] Add the empty and missing states: "No photos on this date" for an empty day with skip-empty off, and a missing-file placeholder naming the file for a record whose file vanished. Done when: tests assert both texts.
- [ ] Commit captures under `docs/captures/albumen/calendar/` and write `docs/user/albumen/calendar.md`. Done when: every view appears in a capture and the page documents it.
- [ ] Commit: `"albumen: calendar browsing"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~CalendarQuery|FullyQualifiedName~CalendarEvent"` exits 0 with query timing quoted; captures committed under `docs/captures/albumen/calendar/`. Cheaper substitute that fails: enumerating folders per click, which the timing catches.

## 11. Duplicate Finder

Accidental copies waste space and confuse culling. Content-identical duplicates are found on demand (one list or two, files and folders, subfolders, exact content or same name, images only) and automatically across the catalog by the indexer, grouped as stacks in a duplicates view with set as original, and reviewed with previews, marks, recycle, and rename. Matching is by content, never by name alone unless the user chose it; visually similar photos are `D04 T10 §5`. Catalog: LP-0242 to LP-0245 (4 features: the duplicates view, automatic detection, the finder setup, and the review). -> SOURCE: parity-albumen-duplicates

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/duplicates/`.
**Design:** docs/design/components/ListTree/README.md, docs/design/components/Dialog/README.md, docs/design/components/Button/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Slider/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user reclaims space and removes accidental copies without losing a keeper. Consumer: the files recycled, the stacks formed, and the duplicate report.
**Treatment:** ACDSee's Duplicate Finder wizard (setup, review, finish) and Lightroom's duplicates view with set as original. Cheaper substitute that fails the checkpoint: matching by file name only.
**Chrome:** consume §2's hashes, §6's recycle, and the stacks of `D04 T06 §3` when they have shipped. Do not add a second hashing path.

**Requires:** display-session -- the finder and duplicates view need an interactive desktop

**Freeze check:** The finder only reads; deleting a duplicate recycles it through §6 and never touches the set's original; a set whose members all carry the delete mark is refused until one is kept. Fixture source: `tests/fixtures/albumen/duplicates/` (created by this section).

- [ ] Add `DuplicateFinder` in `src/Albumen/Isotone.Albumen.Core/Browse/Duplicates/DuplicateFinder.cs` (LP-0244): one or two lists, files and folders, subfolders, exact content (size, then xxHash64 of the first 64 KB, then SHA-256) or same name, and images only. Done when: `DuplicateFinderTests` cover content, name, and two-list modes, and a same-size, different-content pair is not a duplicate.
- [ ] Add automatic duplicate detection for the catalog (LP-0243) as `Albumen.Duplicates.AutoDetect` (default off), run by §2's indexer from its cached hashes. Done when: turning it on marks the planted duplicates after the indexer's pass.
- [ ] Add the duplicates view (LP-0242): sets as stacks (through `D04 T06 §3` when shipped, else grouped rows) with status, set as original, remove, and hide and show hidden. Done when: set as original moves the badge and persists.
- [ ] Add the review (LP-0245): sort sets, preview, mark for deletion, delete from list 1 or list 2 to the Recycle Bin through §6, rename, and review and finish with a summary report of freed space. Done when: a driven review recycles 100 planted duplicates and the report quotes the freed bytes.
- [ ] Refuse deleting every member of a set until one is kept, and say in the finder that visually similar photos are `D04 T10 §5`'s. Done when: a test marking all members gets the refusal.
- [ ] Run the finder as a job in `D04 T11 §1`'s Activity Manager with progress and Cancel for runs over one second, and log one Serilog Information line per run and per recycled file. Done when: a cancelled run leaves no file recycled and the log lines are asserted.
- [ ] Commit fixtures under `tests/fixtures/albumen/duplicates/` (a generator for 100 planted duplicates, a same-size different-content pair) with `reference.txt`. Done when: the generator reproduces the set.
- [ ] Commit captures under `docs/captures/albumen/duplicates/` and write `docs/user/albumen/duplicates.md`. Done when: every wizard page and the view appear in captures and the page documents them.
- [ ] Commit: `"albumen: duplicate finder and duplicates view"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~DuplicateFinder"` exits 0; a driven run over a folder with 100 planted duplicates finds exactly 100 with timing quoted. Cheaper substitute that fails: size-only matching, which the different-content pair catches.

## 12. Archives and Folder Sync

A zipped shoot should open without unpacking, and a backup copy of the photo folders should stay current. Albumen browses inside ZIP, RAR, 7z, ARJ, CAB, GZ, TAR, and TGZ archives like read-only folders, extracts to a folder, creates ZIP archives with optional recycling of sources after the archive is verified, and runs saved folder-sync jobs that mirror folders to a backup location on a schedule. SharpCompress (MIT) moves with Pinxit's archive opener (`D03 T17 §12`) to `Isotone.Core` on this second consumer; `System.IO.Compression` writes ZIP. Catalog: LP-0246 to LP-0250, LP-0974 (6 features: folder sync, create archive, remove sources after a verified archive, extract, browse inside archives, and the archive formats). -> SOURCE: parity-albumen-archives-sync

**Fidelity:** new build, no baseline; captured to `docs/captures/albumen/archives/` and `docs/captures/albumen/sync/`.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Button/README.md, docs/design/components/Progress/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user opens a zipped shoot without unpacking it and keeps a backup copy of their photo folders current. Consumer: the archive files, the extracted and synced copies, and the sync logs.
**Treatment:** ACDSee's Create Archive and Extract dialogs and Sync wizard (source, destination, error and log options, conflicts, name, schedule, edit, run saved syncs). Cheaper substitute that fails the checkpoint: extracting every archive to a temp folder to browse it.
**Chrome:** consume SharpCompress moved to `Isotone.Core/Formats/Archives/`, `System.IO.Compression`, §6, `D04 T11 §1`'s Activity Manager, §2's scheduled-task path, and the settings store. Do not add a second archive reader.

**Requires:** display-session -- the archive and sync dialogs need an interactive desktop

**Freeze check:** Archive browsing never writes the archive; creating an archive writes through `AtomicFileWriter`, and removing sources recycles them through §6 only after every entry's hash in the reopened archive matches its source; sync never deletes at the destination except in mirror mode, and then only to the Recycle Bin, logged per file. Fixture source: `tests/fixtures/albumen/archives/` (created by this section).

- [ ] Move `D03 T17 §12`'s archive opener (SharpCompress, MIT) from Pinxit to `src/Isotone.Core/Formats/Archives/` with `git mv`, repointing Pinxit, and add SharpCompress to `Directory.Packages.props` with a `docs/dev/decisions.md` row if the move has not already. Done when: `grep -rn "class ArchiveOpener" src` prints one path under `src/Isotone.Core/`.
- [ ] Browse archives as read-only virtual folders (LP-0250, LP-0974): ZIP, RAR, 7z, ARJ, CAB, GZ, TAR, and TGZ, listed in the folder tree and grouped with folders, entries decoded from a stream through the registry. Done when: `ArchiveBrowseTests` list and decode each format's fixture with no temp file written.
- [ ] Enable §2's "archive contents" option in the Catalog Files dialog, so the indexer caches archive entries. Done when: indexing a folder holding a ZIP caches its entries' thumbnails.
- [ ] Add Extract (LP-0249) of photos and documents: a target folder, create folder, and §6's collision policy. Done when: extracting the 7z fixture writes every entry byte-identical to its source.
- [ ] Add Create Archive (LP-0247) from a photo selection: ZIP only (RAR and 7z creation are not offered, stated in the dialog), compression level, subfolders, hidden files, AES-256 password through SharpCompress where supported (ZipCrypto refused, recorded in `docs/dev/decisions.md`), the output file, and add to or overwrite an existing archive. Done when: `CreateArchiveTests` reopen a password archive with the password and fail without it.
- [ ] Add remove sources after a verified archive (LP-0248): reopen the archive, compare every entry's hash with its source, then recycle the sources through §6; never an unverified delete. Done when: `CreateArchiveTests` corrupt one entry by fault injection and every source is kept.
- [ ] Add `SyncJob` in `src/Albumen/Isotone.Albumen.Core/Browse/Sync/SyncJob.cs` (LP-0246): source, destination, mirror or update mode, error and log options, a conflict rule, and a name, saved in `Albumen.Browse.SyncJobs`. Done when: `SyncJobTests` run mirror and update over a fixture pair and assert the destination listing.
- [ ] Add the Sync wizard with edit and run saved syncs, and scheduling through §2's scheduled-task path (LP-0246). Done when: a driven scheduled sync runs at its trigger and its log is quoted.
- [ ] Report each sync run in the Activity Manager with counts and a log file. Done when: the history shows the run's per-file rows.
- [ ] Commit fixtures under `tests/fixtures/albumen/archives/` (one per archive format, a password ZIP, a sync source and destination pair) with `reference.txt` naming 7-Zip 24 as the listing oracle. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/albumen/archives/` and `docs/captures/albumen/sync/` and write `docs/user/albumen/archives-sync.md`. Done when: every dialog appears in a capture and the page documents it.
- [ ] Commit: `"albumen: archives and folder sync"`

**Test checkpoint:** Unit test and driven run: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ArchiveBrowse|FullyQualifiedName~CreateArchive|FullyQualifiedName~SyncJob"` exits 0; a driven browse of the 7z fixture and a sync run to a second drive are captured with the log quoted. Cheaper substitute that fails: unzip to temp, which the no-temp-files assertion catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx --filter "FullyQualifiedName~Browse|FullyQualifiedName~Indexer|FullyQualifiedName~FileOperation|FullyQualifiedName~PrivateVault|FullyQualifiedName~Duplicate|FullyQualifiedName~Archive|FullyQualifiedName~SyncJob"` exits 0 with this file's test classes reporting
- [ ] The browse, indexer, and calendar budgets are quoted from a run on the reference machine
- [ ] `UnchangedOriginalsTests.BrowseSession` passes and the file-operation hash assertions hold
- [ ] `python scripts/todo-graph.py validate` clean
