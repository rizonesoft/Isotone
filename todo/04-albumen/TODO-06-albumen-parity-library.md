---
schema_version: 1
id: albumen-parity-library
domain: 04-albumen
status: draft
title: "TODO-06 -- Albumen Parity: Library, Collections, Search, and the Catalog"
depends_on: []
frozen: true
track: L6
---

# TODO-06 -- Albumen Parity: Library, Collections, Search, and the Catalog

> **Goal:** Albumen's library reaches Lightroom Classic and ACDSee parity on top of the 0.1.0 grid, loupe, and catalog, over both imported and browsed photos: every grid, loupe, filmstrip, survey, and second-window view option; label sets, flag and rating cycles, ACDSee tagging, and configurable auto advance; stacks, auto-stacks, and virtual copies; the full filter bar with text rules, attribute filters, metadata browser columns, and filter presets; collection sets, target and quick collections, and a smart-collection rule editor with every criterion; ACDSee categories, auto categories, and special items; quick and advanced search with saved searches and disk search; the Folders and Catalog panels with synchronize, relocate, missing-photo recovery, and offline volumes; scheduled catalog backup and maintenance (promoting B-036); multiple catalogs with import from Albumen, Lightroom Classic, and Photoshop Elements catalogs; smart previews for offline editing; the dashboard; and the Painter and Quick Develop. The code lives in `src/Albumen/Isotone.Albumen.Core/` (`Catalog/`, `Library/`, `Search/`, `Collections/`, `Maintenance/`, `CatalogExchange/`, `SmartPreviews/`) and `src/Albumen/Isotone.Albumen.Desktop/` (`Library/`, `Panels/`, `Dashboard/`); it extends `D04 T01 §5` to `§11` in place, moves or deletes an original only as an explicit user file operation into the Recycle Bin, and never writes an original image's bytes.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Albumen has no code: `src/Albumen` does not exist, and the library this file extends is planned in `todo/04-albumen/TODO-01-albumen-foundation.md` (`D04 T01 §5` catalog, `§7` preview cache, `§8` grid, `§9` loupe, `§10` keywords and collections, `§11` culling and sidecars). The foundation file already names the catalog location setting `Albumen.Catalog.Path` and the preview cache limit `Albumen.Cache.SizeMB` that §10 and §11 extend, and `standards/albumen.md` requires forward-only migrations with a backup before each, which every schema change here follows. Catalog maintenance and library statistics were backlog B-036 until the Albumen integration of 2026-09-27 promoted the entry into §9 and §12. Checklist paths name the projects `D04 T01 §2` creates.
<!-- claim: absent src/Albumen -->
<!-- claim: exists todo/04-albumen/TODO-01-albumen-foundation.md -->
<!-- claim: count "Albumen\.Catalog\.Path" todo/04-albumen/TODO-01-albumen-foundation.md = 1 -->
<!-- claim: count "Albumen\.Cache\.SizeMB" todo/04-albumen/TODO-01-albumen-foundation.md = 1 -->
<!-- claim: count "forward-only migrations" standards/albumen.md = 1 -->

## Inputs

- [`docs/parity/albumen-parity.md`](../../docs/parity/albumen-parity.md) -- the catalog rows each section owns (`LP-` ranges named in each context paragraph)
- [`docs/parity/albumen-section-design.md`](../../docs/parity/albumen-section-design.md) -- the design these sections were authored from ("Browse without importing", "The original-file guard holds everywhere")
- [`standards/albumen.md`](../../standards/albumen.md) -- the catalog rules (one SQLite file, forward-only migrations, backup before migration) and the original-file guard
- [`standards/shared.md`](../../standards/shared.md) -- the design contract, logging, atomic saves, and the performance budgets
- [`standards/testing.md`](../../standards/testing.md) -- fixtures and the fidelity tolerance rules
- SQLite 3 documentation (`VACUUM`, `PRAGMA integrity_check`, `REINDEX`, `ANALYZE`, the online backup API, FTS5) -- the maintenance and search primitives §7 and §9 use
- Lightroom Classic 15.5.1 `.lrcat` schema as observed read-only (`Adobe_images`, `AgLibraryFile`, `AgLibraryFolder`, `AgLibraryRootFolder`, `AgLibraryKeyword`, `AgLibraryKeywordImage`, `AgLibraryCollection`, `AgLibraryCollectionImage`) -- the import-only reader of §10
- -> XREF: D04 T02 §8 -- Albumen 0.1.0 ships before every section here
- -> XREF: D04 T01 §5 -- the catalog every section migrates forward
- -> XREF: D04 T01 §7 -- the preview cache §10 manages and §11 extends
- -> XREF: D04 T01 §8 -- the grid, sort, and filter bar §1 and §4 extend
- -> XREF: D04 T01 §9 -- the loupe, compare, and filmstrip §1 extends
- -> XREF: D04 T01 §10 -- keywords, collections, smart collections, and statistics §5 and §12 extend
- -> XREF: D04 T01 §11 -- culling keys, auto advance, and the XMP sidecar §2 extends
- -> XREF: D04 T02 §1 -- the edit stack virtual copies (§3) and Quick Develop (§13) write
- -> XREF: D04 T02 §5 -- develop presets the Painter and Quick Develop apply (§13)
- -> XREF: D04 T02 §7 -- the basic stacks §3 extends
- -> XREF: D04 T05 §2 -- the indexer and watcher §8 synchronizes through and §9's quarantine feeds
- -> XREF: D04 T05 §4 -- browse views share §1's cell renderer and show §7's disk-search results
- -> XREF: D04 T05 §6 -- the file operations and journal §2 and §8 move, rename, and recycle through
- -> XREF: D04 T05 §8 -- selective browsing §6's auto categories combine with
- -> XREF: D04 T13 §7 -- the DNG writer §11's smart previews use
- -> XREF: D03 T15 §4 -- the HDR display path §1 consumes for HDR photos
- -> XREF: D03 T17 §10 -- the EXIF, IPTC, and XMP readers in `Isotone.Core/Metadata/` §7's disk search reads through
- -> XREF: D01 T07 §1 -- the tone stages Quick Develop drives relatively (§13)
- -> XREF: D01 T07 §6 -- the XMP develop-settings exchange §10's Lightroom catalog import reads through
- -> XREF: D04 T07 §1 -- the import window consumes §8's Import to This Folder and previous-import entries
- -> XREF: D04 T07 §3 -- import applies §5's collections and §6's categories
- -> XREF: D04 T08 §1 -- the metadata model that fills §4's location and IPTC columns and §6's embed-pending special item
- -> XREF: D04 T08 §3 -- metadata presets the Painter of §13 enables when they ship
- -> XREF: D04 T08 §8 -- the metadata writer that takes over §2's and §6's sidecar writes and writes IPTC supplemental categories
- -> XREF: D04 T09 §15 -- soft-proof copies and develop's new files (`D04 T09 §16`, `D04 T09 §17`) stack and version through §3
- -> XREF: D04 T11 §1 -- the Activity Manager history that reopens §7's saved and advanced searches (LP-0759)
- -> XREF: D04 T10 §3 -- the People group of named people and the unnamed-faces item in §6's catalog pane
- -> XREF: D04 T10 §5 -- similarity search offered from §7 and similarity auto-stacks beside §3's
- -> XREF: D04 T12 §4, D04 T12 §7, D04 T12 §9, D04 T12 §10 -- output creations §5 saves as collections
- -> XREF: D04 T14 §3 -- the keymap editor that rebinds §2's keypad culling keys
- -> XREF: D04 T15 §4 -- `albumen-v0.5.0` releases this file's phase

## Outcome

- The grid, loupe, filmstrip, compare, survey, and a secondary display window carry every Lightroom and ACDSee view option, and sort, select, and custom order work on a 50,000-photo catalog.
- Culling works in Lightroom's flags and stars and ACDSee's tags and labels, with label sets, Refine, Delete Rejected to the Recycle Bin, keypad culling, and per-kind auto advance.
- Stacks, auto-stacks, and virtual copies group photos without duplicating a file.
- The filter bar, smart collections, categories, quick search, advanced search, and saved searches find any photo by any attribute in under 200 ms on 50,000 photos.
- The Folders and Catalog panels keep the catalog in step with the disk, rebind moved files, and keep offline volumes browsable.
- Catalog backups run on a schedule, pass an integrity check, restore to a catalog equal row by row, and survive corruption tests.
- Catalogs split, merge, and import from Lightroom Classic and Photoshop Elements without losing ratings, labels, keywords, or collections, and without writing the source catalog.
- Smart previews let develop continue offline, and the dashboard reports what the library holds.
- Every library command is one undo step with one Serilog Information line, and every original's bytes are unchanged.

**Adjacency:** list=applicable @ D04 T06 §1; document=not-applicable (the library prints and exports nothing itself; printed and exported output is D04 T12); settings=applicable @ D04 T06 §10; reporting=applicable @ D04 T06 §12; notifications=applicable @ D04 T06 §9; permissions=applicable @ D04 T06 §8; audit=applicable @ D04 T06 §2; exchange=applicable @ D04 T06 §10; reverse=applicable @ D04 T06 §2

**Adjacency rationale:** The grid, survey, filmstrip, and second window (§1) are the list, with every panel list (collections §5, categories §6, saved searches §7, folders and volumes §8) beside them. Every view, culling, filter, backup, and preview option is an `Albumen.*` key with a default and a named consumer, and §10's Catalog Settings is where the catalog-level ones live. The dashboard (§12) is the report, with §9's maintenance summary and §10's file listing. Backup, optimize, synchronize, and catalog import run with progress, Cancel, and a summary on the status strip (§9 owns the pattern). Read-only volumes, locked catalogs, missing folders, and offline media are refused or badged by name (§8, with §9's catalog lock). Every catalog-changing command writes one Serilog Information line and one history entry, which §2's culling commands set the pattern for. Smart-collection settings, keyword and catalog exports, Lightroom and Elements catalog import, and catalog export with negatives are the exchange surface (§10, with §5's `.lrsmcol` files). Every library command undoes through the suite history, remove-from-catalog is undoable in the session, and backups restore (§2 and §9).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | Library view extensions: cell styles, overlays, survey, and a second window | D04 T02 §8, D04 T05 §4 |  [ ]   |
|   2   |   §2    | Culling extensions: label sets, flag and rating cycles, tagging, and auto advance | §1, D04 T05 §6 |  [ ]   |
|   3   |   §3    | Stacks, versions, and virtual copies | §1 |  [ ]   |
|   4   |   §4    | The filter bar extended: text, attributes, metadata columns, and presets | §1 |  [ ]   |
|   5   |   §5    | Collections extended: sets, target and quick collections, and the smart-collection rule editor | §4 |  [ ]   |
|   6   |   §6    | Categories and auto categories | §5 |  [ ]   |
|   7   |   §7    | Quick search and advanced search | §4, D04 T05 §4, D03 T17 §10 |  [ ]   |
|   8   |   §8    | Folders and catalog panels: synchronize, relocate, missing photos, and offline volumes | §1, D04 T05 §2, D04 T05 §6 |  [ ]   |
|   9   |   §9    | Catalog backup and maintenance | §8 |  [ ]   |
|  10   |   §10   | Multiple catalogs, catalog settings, and preview management | §9, D01 T07 §6 |  [ ]   |
|  11   |   §11   | Smart previews and offline editing | §10, D04 T13 §7 |  [ ]   |
|  12   |   §12   | The dashboard and library statistics | §4, §9 |  [ ]   |
|  13   |   §13   | Painter and Quick Develop | §2, §5 |  [ ]   |

---

## 1. Library view extensions: cell styles, overlays, survey, and a second window

The 0.1.0 grid and loupe (`D04 T01 §8`, `§9`) show a thumbnail, four badges, and a large photo; Lightroom and ACDSee users arrange every cell, overlay, and sort order, and use a second monitor as a loupe or survey. This section extends those views in place (never a second grid) over both library and browsed photos, and adds the survey view and a secondary display window with its own view and filter. It must not break the `D04 T01 §8` budget: grid frame time stays under 16 ms on 50,000 photos with every option on. Catalog: LP-0254 to LP-0267 (14 features: filmstrip options, the secondary display window, loupe info overlays, compare swap and make select, the survey view, loupe zoom ratios and the Navigator, loupe overlays, sort orders, custom order, selection commands, grid view options, the loupe info sets, HDR display, and the last selection per source). -> SOURCE: parity-albumen-library-views

**Groomed 2026-09-28:** LP-0266 (HDR display in the library) moved to `D04 T09 §3`: the HDR display path is Pinxit's until `D04 T09 §3` moves it to `Isotone.UI` in Phase 35, and no Albumen photo is HDR-edited before that section; this section now covers LP-0254 to LP-0265 and LP-0267 (13 features).

**Fidelity:** Library view options, survey, and the second window -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/survey/. **Corrected 2026-09-27:** cited docs/captures/albumen/main-window/ (baseline from `D04 T01 §8`) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Slider/README.md, docs/design/components/Tabs/README.md, docs/design/components/WindowChrome/README.md, new surface: docs/design/components/AlbumenGrid/README.md, new surface: docs/design/components/AlbumenLoupe/README.md, new surface: docs/design/components/AlbumenCompare/README.md, new surface: docs/design/components/AlbumenFilmstrip/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer arranges the library exactly as they cull, reads the information they care about on every cell, and uses a second monitor as a full-size loupe or survey while the main window stays on the grid. Consumer: culling (§2), the Painter and sync (§13), and every later library surface that reads the active and selected photos.
**Treatment:** View, View Options dialog with Grid and Loupe tabs (compact and expanded cells, extras, hover-only items, label tint, index numbers, header and rating footer, tooltips, two loupe info sets); N enters Survey; the Window, Secondary Display menu with Grid, Loupe (normal, live, locked), Compare, Survey, and Slideshow and a monitor chooser. Cheaper substitute that fails the checkpoint: a second window that mirrors the main one.
**Chrome:** consume the `D04 T01 §8` virtualizing grid and `D04 T01 §9` loupe (extended, not replaced), the `Isotone.UI` theme, the settings store, and the icon catalog. Do not invent a second cell renderer: `D04 T05 §4`'s browse views draw through the same one.

**Requires:** display-session -- view options, the survey, and the second window are driven on an interactive desktop with two monitors or a virtual second display

- [ ] Write or extend the design spec `docs/design/components/AlbumenGrid/README.md` and `preview.html` with the cell styles and view options (anatomy, every state, tokens, sizes; `D04 T01 §8` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Write or extend the design spec `docs/design/components/AlbumenLoupe/README.md` and `preview.html` with the loupe info and overlays and the zoom ratios (anatomy, every state, tokens, sizes; `D04 T01 §9` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Write or extend the design spec `docs/design/components/AlbumenCompare/README.md` and `preview.html` with the survey view and compare swap (anatomy, every state, tokens, sizes; `D04 T01 §9` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Write or extend the design spec `docs/design/components/AlbumenFilmstrip/README.md` and `preview.html` with the source indicator (anatomy, every state, tokens, sizes; `D04 T01 §9` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Add `GridCellOptions` in `src/Albumen/Isotone.Albumen.Core/Library/Views/GridCellOptions.cs` (LP-0264): compact and expanded styles, extras (index number, file name, dimensions, rating footer, header label), hover-only items, label tint strength, cell icons, and tooltips, stored as `Albumen.Library.Grid.*`. Done when: `GridCellOptionsTests` round-trip every field through the settings store with its default.
- [ ] Add `LoupeInfoOptions` in `src/Albumen/Isotone.Albumen.Core/Library/Views/LoupeInfoOptions.cs` (LP-0256, LP-0265): two configurable info sets of up to three lines each, cycled with I, shown briefly or always, plus the "Loading" and "Embedded preview" messages, stored as `Albumen.Library.Loupe.*`. Done when: `LoupeInfoOptionsTests` assert I cycles set 1, set 2, off.
- [ ] Extend the grid cell template in `src/Albumen/Isotone.Albumen.Desktop/Library/Views/GridCell.xaml` to draw every `GridCellOptions` item from theme resources with hover-only items bound to `IsMouseOver`. Done when: captures of compact and expanded cells are committed under docs/captures/albumen/main-window/. Cheaper substitute: a fixed cell with a single extra line.
- [ ] Extend `D04 T01 §9`'s filmstrip (LP-0254) with the source indicator and recent-sources menu, a quick filter, rating and stack-count badges, tooltips, navigator hover preview, and an unsynced badge. Done when: a capture shows each item and `FilmstripViewModelTests` assert the recent-sources list keeps its last eight entries.
- [ ] Extend the loupe zoom (LP-0259) to the ratios 1:16 to 11:1 with a zoom-position lock and add a Navigator panel in `src/Albumen/Isotone.Albumen.Desktop/Library/Panels/NavigatorPanel.xaml`. Done when: `LoupeZoomTests` assert the ratio list and that a locked position survives moving to the next photo.
- [ ] Add loupe overlays (LP-0260) in `src/Albumen/Isotone.Albumen.Desktop/Library/Overlays/`: grid, draggable guides, and a layout image (a PNG with opacity and matte) with an overlay edit mode. Done when: a capture shows a layout PNG at 50 percent opacity and the guide positions persist in `Albumen.Library.Loupe.Guides`.
- [ ] Add compare swap and make select (LP-0257) to `D04 T01 §9`'s compare view. Done when: `CompareViewModelTests` assert swap exchanges select and candidate and make select promotes the candidate.
- [ ] Add `SurveyViewModel` in `src/Albumen/Isotone.Albumen.Desktop/Library/SurveyViewModel.cs` (LP-0258): N shows the selection sized to fit, and a cell's X removes the photo from the survey without deselecting it. Done when: `SurveyViewModelTests` assert removal keeps the catalog selection. Cheaper substitute: the grid at a larger thumbnail size.
- [ ] Add `LibrarySort` in `src/Albumen/Isotone.Albumen.Core/Library/LibrarySort.cs` (LP-0261): capture, added, edit time, edit count, rating, pick, label, name, extension, type, and aspect, each with reverse, compiled to indexed `ORDER BY` clauses. Done when: `LibrarySortTests` assert every order on a seeded 5,000-photo catalog.
- [ ] Add a `custom_order` column per folder and collection through a forward migration in `src/Albumen/Isotone.Albumen.Core/Catalog/Migrations/`, filled by dragging cells (LP-0262), with drag disabled and a tooltip saying why when the source mixes folders. Done when: `LibrarySortTests.CustomOrderPersists` reopens the catalog and reads the dragged order back.
- [ ] Add `SelectionCommands` in `src/Albumen/Isotone.Albumen.Core/Library/SelectionCommands.cs` (LP-0263): select all, none, active only, and by flag, rating, and label with add, intersect, remove, and invert, keeping the active photo distinct from the selected set. Done when: `SelectionCommandTests` cover each command and operator.
- [ ] Add `SecondaryWindow` in `src/Albumen/Isotone.Albumen.Desktop/Library/SecondaryWindow.xaml` (LP-0255) with its own view mode (grid, loupe normal, live, locked, compare, survey, slideshow), filter bar, and monitor choice; ACDSee's second-monitor image view maps to Loupe live. Done when: `SecondaryWindowViewModelTests` assert live follows the main selection and locked does not. Cheaper substitute: a mirror of the main window.
- [ ] Remember the last selected photo per recent source (LP-0267) in `Albumen.Library.LastSelection`. Done when: a test switches sources twice and reads the selection back.
- [ ] Log one Serilog Information line per view-option change and per custom-order drag. Done when: a Serilog test logger asserts each line.
- [ ] Measure grid frame time with every cell option on over a generated 50,000-photo catalog. Done when: the median frame time is quoted under 16 ms with the machine named.
- [ ] Write `docs/user/albumen/library-views.md` covering View Options, the survey, overlays, sort, and the second window. Done when: every Treatment control is named on the page.
- [ ] Commit: `"albumen: library view options, survey, loupe overlays, and a second window"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~GridCellOptionsTests|FullyQualifiedName~LibrarySortTests|FullyQualifiedName~SelectionCommandTests|FullyQualifiedName~SecondaryWindowViewModelTests|FullyQualifiedName~SurveyViewModelTests"` exits 0 on the seeded catalog, and a driven session shows the survey and a locked second window on a second display (captures under docs/captures/albumen/survey/ and docs/captures/albumen/second-window/, grid median frame time quoted under 16 ms). Cheaper substitute that fails: a mirrored second window, which the locked-mode test catches.

## 2. Culling extensions: label sets, flag and rating cycles, tagging, and auto advance

`D04 T01 §11` ships ratings, flags, labels, and one auto-advance switch. Lightroom users cull with flag cycles, Refine, and named label sets; ACDSee users cull with a tag checkbox, the numeric keypad, and auto advance per metadata kind. This section adds both schemes over one set of culling commands, and Delete Rejected, which never deletes permanently: it removes from the catalog or moves the file with its sidecar and RAW+JPEG partner to the Recycle Bin through `D04 T05 §6`'s file operations. Label and tag values reach sidecars through `D04 T01 §11`'s writer until `D04 T08 §8`'s metadata writer takes over in Phase 34. Catalog: LP-0268 to LP-0280 (13 features: flag increase and decrease, label sets, Refine Photos, Delete Rejected, rating entry paths, auto advance in the viewer and the library, ratings and labels groups, label entry paths, auto advance options, keypad culling, tagging, and tag the current file). -> SOURCE: parity-albumen-culling

**Fidelity:** Culling: label sets, flags, tagging, and auto advance -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/label-sets/. **Corrected 2026-09-27:** cited docs/captures/albumen/main-window/ as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md, docs/design/components/Menu/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Panel/README.md, docs/design/components/Icons/README.md, docs/design/components/ToggleSwitch/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer culls a shoot entirely from the keyboard in the scheme they already know (Lightroom flags and stars or ACDSee tags and labels) and never loses a decision. Consumer: the filter bar (§4), smart collections (§5), the catalog pane (§6), and sidecars read by other tools.
**Treatment:** Metadata, Color Label Set submenu with Edit (rename five labels, save, switch, delete sets); Ctrl+Up and Ctrl+Down cycle flags; Library, Refine Photos; Photo, Delete Rejected Photos with Remove from Catalog or Move to Recycle Bin; a tag checkbox and reject mark on thumbnails; an Auto Advance toolbar toggle with a per-kind options page. Cheaper substitute that fails the checkpoint: auto advance for ratings only.
**Chrome:** consume `D04 T01 §11`'s culling commands (extended), `D04 T05 §6`'s file operations for the Recycle Bin, the suite history, and the settings store. Do not invent a second delete path.

**Requires:** display-session -- keyboard culling and the label-set dialog are driven on an interactive desktop

- [ ] Add `LabelSet` in `src/Albumen/Isotone.Albumen.Core/Library/Culling/LabelSet.cs` (LP-0269): five named colors, built-in Lightroom-style and ACDSee-style sets, and user sets in `Albumen.Culling.LabelSets`, with the active set's names written as the XMP label text so Lightroom reads them. Done when: `LabelSetTests` rename a label and read the new text back from the fixture sidecar.
- [ ] Add the Edit Label Set dialog in `src/Albumen/Isotone.Albumen.Desktop/Library/Dialogs/LabelSetDialog.xaml` (rename, save, switch, delete with confirmation naming the set). Done when: a capture is committed under docs/captures/albumen/label-sets/. Cheaper substitute: label names fixed in code.
- [ ] Add flag increase and decrease (LP-0268) on Ctrl+Up and Ctrl+Down cycling reject, none, pick. Done when: `CullingCycleTests` assert both directions and the wrap limits.
- [ ] Add Library, Refine Photos (LP-0270): unflagged become rejects and picks reset, as one undo step whose log line names the counts. Done when: `RefinePhotosTests` assert the counts and undo.
- [ ] Add Photo, Delete Rejected Photos (LP-0271) with a dialog offering Remove from Catalog or Move to Recycle Bin through `D04 T05 §6`, naming how many photos and how many bytes, never a permanent delete, with each sidecar and RAW+JPEG partner moved together. Done when: `DeleteRejectedTests` recycle a temp folder's rejects with their partners and undo the catalog removal.
- [ ] Add the rating and label entry paths (LP-0272, LP-0276): hover stars and label chips on thumbnails, drag-to-rate, catalog-pane drop targets, Set Rating and Set Label commands, status-bar and Properties fields, and clear and reset. Done when: `RatingEntryTests` assert each path sets the same catalog value with one undo step.
- [ ] Add the ACDSee-compatible `tagged` flag (LP-0279, LP-0280) stored in the catalog and written as `albumen:tagged` in Albumen's own XMP namespace (never as `acdsee:tagged`), with tag keys, tagged and rejected lists, clear tags, and tagging from the viewer and compare. Done when: `TaggingTests` assert the flag, the sidecar property, and clear tags.
- [ ] Draw the tag checkbox and reject mark on thumbnails through `GridCellOptions` (§1). Done when: a capture shows both marks.
- [ ] Add numeric-keypad culling (LP-0278) in the library key table in `src/Albumen/Isotone.Albumen.Desktop/Library/LibraryKeyTable.cs`: tag, labels, ratings, remove rating and label, next, and previous, registered so `D04 T14 §3`'s keymap can rebind them later. Done when: `KeypadCullingTests` assert each binding.
- [ ] Add `AutoAdvanceOptions` in `src/Albumen/Isotone.Albumen.Core/Library/Culling/AutoAdvanceOptions.cs` (LP-0273, LP-0274, LP-0277): per kind (tag, rating, label, category, keyword), per mode (library and viewer), and after keyword entry, extending `D04 T01 §11`'s single switch, stored as `Albumen.Culling.AutoAdvance.*`. Done when: `AutoAdvanceTests` cover each kind and mode.
- [ ] Add the Auto Advance toolbar toggle and its options page. Done when: a capture shows the toggle and the per-kind page.
- [ ] Add the Ratings and Labels groups of the catalog pane (LP-0275) with counts that filter on click, registered as groups §6's pane hosts. Done when: `CatalogPaneGroupTests` assert counts on a seeded catalog.
- [ ] Record every culling decision as one suite history entry and one Serilog Information line naming the command, the value, and the photo, so the audit trail and undo agree. Done when: a Serilog test logger asserts one line per decision in a 20-photo cull.
- [ ] Run the unchanged-originals test over `tests/fixtures/albumen/import/` after a cull, Refine, and Delete Rejected with Remove from Catalog. Done when: every fixture's SHA-256 and last-write time match.
- [ ] Write `docs/user/albumen/culling.md` covering both schemes, label sets, keypad keys, and auto advance. Done when: every key and dialog above is on the page.
- [ ] Commit: `"albumen: label sets, flag cycles, tagging, and configurable auto advance"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~LabelSetTests|FullyQualifiedName~RefinePhotosTests|FullyQualifiedName~DeleteRejectedTests|FullyQualifiedName~AutoAdvanceTests|FullyQualifiedName~TaggingTests|FullyQualifiedName~UnchangedOriginalsTests"` exits 0, and a driven 200-photo keyboard cull with the keypad and auto advance logs one line per decision (lines quoted). Cheaper substitute that fails: a permanent delete, which the Recycle Bin assertion in `DeleteRejectedTests` catches.

**Freeze check:** Delete Rejected never deletes a file permanently and never writes image bytes: Remove from Catalog touches only the catalog, and Move to Recycle Bin moves the photo, its sidecar, and its RAW+JPEG partner through `D04 T05 §6` only after the user confirms a dialog naming the count and size; every other culling command writes the catalog and, when enabled, the sidecar through an atomic write. Fixture source: `tests/fixtures/albumen/import/` (from `D04 T01 §6`) copied to a temp folder for the recycle case.

## 3. Stacks, versions, and virtual copies

`D04 T02 §7` stacks a Pinxit edit beside its original; photographers also group bursts, brackets, and interpretations. This section gives stacks every command, auto-stacking by time and distance, stacks inside collections, and stored behavior rules, and adds virtual copies: catalog records that share one file with their own edit stack and metadata, so an interpretation never duplicates a raw file. Similarity auto-stacks wait for `D04 T10 §5`. Catalog: LP-0281 to LP-0286 (6 features: stack commands, auto-stack by time and GPS, stacks in collections, the copy name field, virtual copies, and stack rules). -> SOURCE: parity-albumen-stacks

**Fidelity:** Stacks and virtual copies -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/stacks/. **Corrected 2026-09-27:** cited docs/captures/albumen/main-window/ as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Menu/README.md, docs/design/components/Panel/README.md, docs/design/components/TextBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Icons/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer groups bursts, brackets, and edits into one cell and keeps several interpretations of one negative without duplicating the file. Consumer: the grid, filters (§4), smart collections (§5), and export.
**Treatment:** Photo, Stacking submenu (Group, Unstack, Remove from Stack, Split, Collapse and Expand one or all, Move to Top, Up, Down); an Auto-Stack by Capture Time dialog with a seconds slider, a GPS distance, presets, and live counts; Photo, Create Virtual Copy (Ctrl+'); Set Copy as Master. Cheaper substitute that fails the checkpoint: stacks implemented as a collection.
**Chrome:** consume `D04 T02 §7`'s stack table (extended), `D04 T02 §1`'s edit stack for virtual copies, and the suite history. Do not add a second stack table.

**Requires:** display-session -- stack commands and the auto-stack dialog are driven on an interactive desktop

- [ ] Add `StackService` in `src/Albumen/Isotone.Albumen.Core/Library/Stacks/StackService.cs` over `D04 T02 §7`'s stack table (LP-0281): group, unstack, remove, split, collapse and expand one or all, move to top, up, and down, each one undo step. Done when: `StackServiceTests` cover each command and undo.
- [ ] Show member counts on the stack badge and a collapsed stack as one cell in `GridCell.xaml`. Done when: a capture under docs/captures/albumen/stacks/ shows a collapsed stack of five.
- [ ] Add `AutoStacker` in `src/Albumen/Isotone.Albumen.Core/Library/Stacks/AutoStacker.cs` (LP-0282): a capture-time gap threshold and a GPS distance limit, presets in `Albumen.Stacks.AutoPresets`, replace or keep existing stacks, and one undo step. Done when: `AutoStackerTests` stack a 300-photo burst fixture with known gaps into the expected count.
- [ ] Add the Auto-Stack dialog in `src/Albumen/Isotone.Albumen.Desktop/Library/Dialogs/AutoStackDialog.xaml` with a live dry-run count that updates as the slider moves, computed off the UI thread. Done when: a capture shows the count and a test asserts no catalog write before OK. Cheaper substitute: a fixed threshold with no preview.
- [ ] Add stack rules (LP-0286) stored in the catalog: members in one folder by default with a multi-folder option, a collapsed stack acting as its head for rating and filter, exclusions, and visibility by mode. Done when: `StackRuleTests` assert a filter on a collapsed stack matches through its head.
- [ ] Add stacks in collections (LP-0283): a collection stores its own stacking through a forward migration, independent of the folder's. Done when: `StackServiceTests.CollectionStackingIndependent` passes.
- [ ] Add `VirtualCopyService` in `src/Albumen/Isotone.Albumen.Core/Library/VirtualCopies/VirtualCopyService.cs` (LP-0285): a catalog record sharing the master's file, with its own `D04 T02 §1` edit stack and metadata overrides. Done when: `VirtualCopyTests` assert an edit on the copy leaves the master's settings unchanged and the file count unchanged.
- [ ] Add the Copy Name field (LP-0284) shown on the cell and in the metadata panel. Done when: a test sets and reads the name.
- [ ] Add Set Copy as Master (LP-0285) swapping roles in one undo step. Done when: `VirtualCopyTests.SetMaster` asserts the swap and its undo.
- [ ] Deleting a virtual copy removes only its record, and a virtual copy writes its XMP only into exported copies because the sidecar belongs to the master. Done when: `VirtualCopyTests.DeleteCopyKeepsFile` and `VirtualCopyTests.SidecarBelongsToMaster` pass.
- [ ] Log one Serilog Information line per stack command and virtual copy action. Done when: a Serilog test logger asserts each line.
- [ ] Write `docs/user/albumen/stacks.md` covering stacks, auto-stack, rules, and virtual copies. Done when: every Treatment command is on the page.
- [ ] Commit: `"albumen: full stacking, auto-stack, and virtual copies"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~StackServiceTests|FullyQualifiedName~AutoStackerTests|FullyQualifiedName~StackRuleTests|FullyQualifiedName~VirtualCopyTests"` exits 0, and a driven auto-stack of the burst fixture matches the expected stack count (capture under docs/captures/albumen/stacks/). Cheaper substitute that fails: duplicating the file for a virtual copy, which the file-count assertion in `VirtualCopyTests` catches.

## 4. The filter bar extended: text, attributes, metadata columns, and presets

`D04 T01 §8`'s filter bar filters by rating, flag, label, camera, lens, date, and folder. Lightroom's Library Filter adds Text, Attribute, and Metadata tabs with cascading columns and presets. This section compiles one `LibraryFilter` model to parameterized SQL over indexed columns, which §5's smart collections and §7's advanced search reuse, and holds the `D04 T01 §8` budget of 200 ms on 50,000 photos. Columns whose data a later phase adds (location and IPTC from `D04 T08 §1`, AI edits from `D04 T10`) are registered now and show zero counts, never an error. Catalog: LP-0308 to LP-0320 (13 features: attribute filters, the filter bar, presets and lock, text fields, text rules, metadata columns, and the date, file, camera, location, IPTC, develop, and AI column families). -> SOURCE: parity-albumen-filter-bar

**Fidelity:** Library filter bar -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/filter-bar/. **Corrected 2026-09-27:** cited docs/captures/albumen/main-window/ as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/shell-layout.md#albumen-darkroom-and-photo-manager, docs/design/components/Tabs/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Menu/README.md, docs/design/components/ListTree/README.md, docs/design/components/Icons/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer narrows 50,000 photos to the ones they want in a few clicks by text, attributes, or cascading metadata columns, and reuses the filter. Consumer: the grid, the second window (§1), smart collections (§5), and search (§7).
**Treatment:** the `D04 T01 §8` bar grows Text (field and rule pickers with `!` and `+` operators), Attribute (flag, edited, rating comparison, label, kind, stacked), and Metadata (up to eight cascading columns, flat or hierarchical, multi-select) tabs, a preset menu, None, and a lock icon. Cheaper substitute that fails the checkpoint: a single search box.
**Chrome:** consume `D04 T01 §8`'s `LibraryViewModel` queries (extended with indexes), the settings store, and the icon catalog. Do not add a second query builder.

**Requires:** display-session -- the filter bar is driven on an interactive desktop

- [ ] Add the `LibraryFilter` model in `src/Albumen/Isotone.Albumen.Core/Search/Filters/LibraryFilter.cs` and `FilterSqlCompiler` compiling it to parameterized SQL (LP-0309), with None, enable and disable, and Ctrl+F focusing Text. Done when: `FilterSqlCompilerTests` assert no user text reaches SQL unparameterized.
- [ ] Add the Text filter fields (LP-0311): any searchable field, filename, copy name, title, caption, keywords, searchable metadata, IPTC, and EXIF. Done when: `TextFilterTests` match each field on a seeded catalog.
- [ ] Add the Text rules and operators (LP-0312): contains, contains all, contains words, does not contain, starts with, ends with, `!` negation, and `+` word anchoring. Done when: `TextFilterTests` cover each rule and operator.
- [ ] Add the Attribute filter (LP-0308): flag, edited state, rating at least, at most, and equal, color label including custom and none, kind (master, virtual copy, video), and stacked status. Done when: `AttributeFilterTests` cover each attribute.
- [ ] Add `MetadataColumnRegistry` in `src/Albumen/Isotone.Albumen.Core/Search/Filters/MetadataColumnRegistry.cs` (LP-0313) with up to eight cascading columns, flat or hierarchical, multi-select, and None, each column's counts from a grouped query restricted by the columns to its left. Done when: `MetadataColumnTests` assert cascading counts on a seeded catalog.
- [ ] Register the date and file columns (LP-0314, LP-0315): date, year and month, day and month, file type, flag, rating, exported, label, keywords, and edit. Done when: each column reports seeded counts.
- [ ] Register the camera and exposure columns (LP-0316): camera, serial number, lens, focal length, shutter, aperture, ISO, and flash. Done when: each column reports seeded counts.
- [ ] Register the location and IPTC columns (LP-0317, LP-0318): has GPS, GPS location, sublocation, city, state, country, creator, copyright status, and job, reading the fields `D04 T08 §1` fills. Done when: each reports zero counts on today's catalog and seeded counts on a fixture with the fields filled.
- [ ] Register the develop-state and AI columns (LP-0319, LP-0320): aspect, HDR, depth, masking, remove modes, point color, settings, smart preview, snapshots, treatment, metadata status, has AI, generative, needs update, edit type, removal, denoise, raw details, and super resolution. Done when: every column registers and a column with no data yet shows zero counts.
- [ ] Add filter presets and the lock (LP-0310): built-in and user presets in `Albumen.Library.FilterPresets`, and a lock that carries the filter across folders and collections. Done when: `FilterPresetTests` save, apply, and delete a preset and assert the lock carries across a source change.
- [ ] Add the three tabs, preset menu, None, and lock icon to `src/Albumen/Isotone.Albumen.Desktop/Library/FilterBar.xaml` with keyboard access to every picker. Done when: captures of each tab are committed under docs/captures/albumen/filter-bar/. Cheaper substitute: one search box.
- [ ] Add indexes for every filterable column through a forward migration. Done when: `EXPLAIN QUERY PLAN` for each column filter in `FilterIndexTests` names an index.
- [ ] Add `FilterPerformanceTests` over a generated 50,000-photo catalog. Done when: every filter kind answers under 200 ms (quoted with the machine).
- [ ] Write `docs/user/albumen/filter-bar.md`. Done when: every tab, field, rule, and column family is on the page.
- [ ] Commit: `"albumen: the full filter bar with text, attributes, metadata columns, and presets"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~FilterSqlCompilerTests|FullyQualifiedName~TextFilterTests|FullyQualifiedName~AttributeFilterTests|FullyQualifiedName~MetadataColumnTests|FullyQualifiedName~FilterPresetTests|FullyQualifiedName~FilterPerformanceTests"` exits 0 with the 50,000-photo response times quoted under 200 ms, and the three tabs are captured. Cheaper substitute that fails: filtering in memory after loading every record, which `FilterPerformanceTests` catches.

## 5. Collections extended: sets, target and quick collections, and the smart-collection rule editor

`D04 T01 §10` has flat collections and smart collections joined by all or any. Lightroom nests collections in sets, collects picks with B into a target or the Quick Collection, and edits smart collections with nested groups over nine criterion families. This section adds all of it, reusing §4's SQL compiler for smart rules, exchanges smart-collection settings with Lightroom's `.lrsmcol` files, and gives output creations (`D04 T12`) a home as collections. Criteria whose data arrives in a later phase are listed and match nothing until then. Catalog: LP-0321 to LP-0338 (18 features: target and Quick Collection, removal, the Create Collection dialog, sets, smart collections, smart-collection exchange, collection filter and labels, output creations, the nine criterion families, and the Organize pane group). -> SOURCE: parity-albumen-collections

**Fidelity:** Collections and the smart-collection editor -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/smart-collection-editor/. **Corrected 2026-09-27:** cited docs/captures/albumen/collections/ (baseline from `D04 T01 §10`) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/ComboBox/README.md, docs/design/components/TextBox/README.md, docs/design/components/Button/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Menu/README.md, docs/design/components/Panel/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer groups work by project in nested sets, collects picks with one key, and keeps living smart collections on any attribute. Consumer: the grid, export, `D04 T07 §3`'s Add to Collection on import, and `D04 T12`'s output creations.
**Treatment:** Create Collection and Create Collection Set dialogs; B adds to the target collection, Ctrl+B shows the Quick Collection, Save and Clear Quick Collection; the smart-collection editor with Match all, any, or none, rows grouped by Alt-click into nested groups, and criteria menus by family. Cheaper substitute that fails the checkpoint: smart collections limited to rating and date.
**Chrome:** consume `D04 T01 §10`'s collection tables and rule engine (extended), §4's `FilterSqlCompiler`, and the suite history. Do not add a second rule engine.

**Requires:** display-session -- the collections panel and rule editor are driven on an interactive desktop

- [ ] Add collection sets (LP-0324) as a parent table with nesting through a forward migration in `src/Albumen/Isotone.Albumen.Core/Collections/`. Done when: `CollectionSetTests` nest three levels, move a collection between sets, and undo.
- [ ] Extend the Create Collection dialog (LP-0323) with include selected photos, make new virtual copies (§3), inside a set, and duplicate collection, and add photos by drag, context menu, or the Organize pane. Done when: `CollectionSetTests.CreateOptions` cover each option.
- [ ] Add the target collection and Quick Collection (LP-0321): one target at a time, B toggles membership, Ctrl+B shows the Quick Collection, and Save and Clear Quick Collection. Done when: `QuickCollectionTests` toggle, save as a named collection, and clear.
- [ ] Add removal from the selected collection or from all collections (LP-0322). Done when: a test removes from all and undoes.
- [ ] Add the `SmartRule` tree in `src/Albumen/Isotone.Albumen.Core/Collections/Smart/SmartRule.cs` (LP-0325): match all, any, or none, nested groups, and operators per data type, compiled through §4's `FilterSqlCompiler`. Done when: `SmartRuleCompilerTests` assert a three-level nested rule on a seeded catalog.
- [ ] Register the attribute and source criteria (LP-0329, LP-0330): rating, flag, label color and text, smart preview, snapshots, adjustments, edits, cropped, folder, collection, publish collection, published via, and exported. Done when: `SmartRuleCompilerTests` cover each criterion.
- [ ] Register the file and date criteria (LP-0331, LP-0332): filename, copy name, file type, DNG fast-load data, dimensions, megapixels, aspect, bit depth, color mode and profile, and capture and edit dates with absolute, relative, and range operators. Done when: `SmartRuleCompilerTests` cover each criterion and a relative date rule moves with a fake clock.
- [ ] Register the camera, location, and IPTC text criteria (LP-0333, LP-0334, LP-0335): camera and exposure fields, location and GPS, title, caption, alt text, extended description, keywords, creator, job, and copyright status. Done when: `SmartRuleCompilerTests` cover each criterion.
- [ ] Register the searchable-text, metadata-status, develop, and AI criteria (LP-0336, LP-0337), listed and matching nothing until `D04 T08 §1`, `D04 T09`, and `D04 T10` supply their data. Done when: each criterion registers and a rule on absent data returns zero rows without an error.
- [ ] Add the smart-collection editor in `src/Albumen/Isotone.Albumen.Desktop/Collections/SmartCollectionEditor.xaml` with Alt-click grouping, criteria menus by family, and a live match count. Done when: a capture under docs/captures/albumen/smart-collection-editor/ shows a nested group. Cheaper substitute: flat all-or-any rows.
- [ ] Add smart-collection exchange (LP-0326) in `src/Albumen/Isotone.Albumen.Core/Collections/Smart/SmartCollectionExchange.cs`: Lightroom-compatible `.lrsmcol` Lua tables for the criteria both share (read and write) and Albumen JSON for the rest, with unknown criteria reported by name, never dropped silently. Done when: `SmartCollectionExchangeTests` read a committed Lightroom 15.5.1 `.lrsmcol` fixture and write it back equal.
- [ ] Add the collections filter, sort, and color labels (LP-0327) to the Collections panel. Done when: a test filters the panel by name and a capture shows a colored collection.
- [ ] Add the `kind` column (print, slideshow, web, book) for output creations (LP-0328) so `D04 T12 §4`, `§7`, `§9`, and `§10` save their layouts as collections here. Done when: `CollectionKindTests` create one of each kind and filter the panel by kind.
- [ ] Add the Organize pane collections group (LP-0338). Done when: a capture shows the group with counts.
- [ ] Log one Serilog Information line per collection change and smart-rule save. Done when: a Serilog test logger asserts each line.
- [ ] Write `docs/user/albumen/collections.md` covering sets, the Quick Collection, and every criterion family. Done when: every family is on the page.
- [ ] Commit: `"albumen: collection sets, quick collection, and the full smart-collection editor"`

**Test checkpoint:** Unit test plus format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~CollectionSetTests|FullyQualifiedName~QuickCollectionTests|FullyQualifiedName~SmartRuleCompilerTests|FullyQualifiedName~SmartCollectionExchangeTests|FullyQualifiedName~CollectionKindTests"` exits 0, the `.lrsmcol` fixture round-trips with every shared criterion equal, and a driven nested smart collection updates live when a rating changes (capture). Cheaper substitute that fails: flat all-or-any rules, which the nested-group test catches.

## 6. Categories and auto categories

ACDSee users find photos through the Catalog pane: hierarchical categories that are not keywords, auto categories computed from metadata (camera, lens, year), and special items such as Uncategorized, combined with Easy-Select bars. This section adds that pane, hosting §2's Ratings and Labels groups and, when `D04 T10 §3` ships, the People group. Categories live in the catalog and in sidecars as `albumen:categories`; writing them as IPTC supplemental categories is `D04 T08 §8`'s. Catalog: LP-0339 to LP-0346 (8 features: the catalog pane, Easy-Select, categories, auto categories, special items, pane options, quick category sets, and the Organize pane group). -> SOURCE: parity-albumen-categories

**Fidelity:** new build, no baseline; captured to docs/captures/albumen/catalog-pane/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Dialog/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Button/README.md, docs/design/components/Tooltip/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** an ACDSee user finds photos the way they always have: by clicking categories, auto categories such as camera or year, and special items like Uncategorized, combined with match all or any. Consumer: the grid, §4's filter compiler, and `D04 T07 §3`'s categories applied on import.
**Treatment:** a Catalog pane with Categories, Auto Categories, People, Ratings, Labels, Keywords, Saved Searches, and Special Items groups, Easy-Select bars to add a group to the match, and a quick-category button grid. Cheaper substitute that fails the checkpoint: categories stored as keywords.
**Chrome:** consume the catalog, §5's rule compiler, the suite history, and the icon catalog. Do not store categories in the keyword table.

**Requires:** display-session -- the catalog pane is driven on an interactive desktop

- [ ] Add the `Category` tree in `src/Albumen/Isotone.Albumen.Core/Catalog/Categories/CategoryTree.cs` (LP-0341) in its own tables through a forward migration: create, edit, move, filter, assign, unassign, uncategorize, and the Set Categories command. Done when: `CategoryTreeTests` cover each command with undo.
- [ ] Delete a category with a confirmation naming the category and how many photos it holds. Done when: `CategoryTreeTests.DeleteConfirms` asserts the text and the undo.
- [ ] Write categories to sidecars as `albumen:categories` in Albumen's XMP namespace through `D04 T01 §11`'s writer. Done when: `CategoryTreeTests.SidecarField` reads the field back and asserts `dc:subject` is untouched.
- [ ] Add auto categories (LP-0342) computed from indexed metadata groupings (camera, lens, year, ISO bands, file type, commonly used), multi-select, and combined with ratings, categories, and `D04 T05 §8`'s selective browsing. Done when: `AutoCategoryTests` assert groupings on a seeded catalog.
- [ ] Add special items (LP-0343): all images, embed pending (filled by `D04 T08 §8`), uncategorized, no keywords, unnamed faces (filled by `D04 T10 §3`, empty until then), tagged, and rejected; **Corrected 2026-09-27:** said auto-named and suggested faces too, which need face recognition, now backlog B-052 after the operator did not approve Albumen's local face models. Done when: `SpecialItemTests` assert each item's count on a seeded catalog.
- [ ] Add the Catalog pane in `src/Albumen/Isotone.Albumen.Desktop/Panels/CatalogPane.xaml` (LP-0339) hosting every group with counts and click to search. Done when: a capture under docs/captures/albumen/catalog-pane/ shows every group. Cheaper substitute: a flat list of keywords.
- [ ] Add Easy-Select (LP-0340): bars that add a group to the match with all or any, compiled through §5. Done when: `EasySelectTests` assert a category-plus-rating combination on a seeded catalog.
- [ ] Add the pane options (LP-0344): icons, the Easy-Select bar and its tooltip, assign by clicking, and delete confirmations, stored as `Albumen.CatalogPane.*`. Done when: a test toggles each option through the settings store.
- [ ] Add quick category sets (LP-0345): a button grid with rows, columns, `Child < Parent` syntax, and assignment state. Done when: `QuickCategoryTests` parse the syntax and toggle an assignment.
- [ ] Add the Organize pane categories group (LP-0346). Done when: a capture shows it.
- [ ] Log one Serilog Information line per category change. Done when: a Serilog test logger asserts it.
- [ ] Write `docs/user/albumen/categories.md`. Done when: every group, Easy-Select, and quick sets are on the page.
- [ ] Commit: `"albumen: categories, auto categories, special items, and the catalog pane"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~CategoryTreeTests|FullyQualifiedName~AutoCategoryTests|FullyQualifiedName~SpecialItemTests|FullyQualifiedName~EasySelectTests|FullyQualifiedName~QuickCategoryTests"` exits 0, and a driven Easy-Select combination returns the expected count on a seeded catalog (capture). Cheaper substitute that fails: categories aliased to keywords, which `CategoryTreeTests.SidecarField` catches.

## 7. Quick search and advanced search

The filter bar narrows what is on screen; search finds what the user can name. This section adds a quick search bar over an FTS5 index, an advanced search pane with every criterion type and saved searches listed in §6's catalog pane, and IrfanView's disk search, which finds files and their metadata in folders never indexed and shows the results in `D04 T05 §4`'s browser without cataloging them. Disk search reads metadata through the shared `Isotone.Core/Metadata/` readers of `D03 T17 §10`, not through an Albumen copy. Catalog: LP-0347 to LP-0359 (13 features: the advanced search pane, saved searches, quick search, quick search fields, advanced options, presets, folder handling, filename, text and people, and metadata criteria, and disk search by name, by metadata, and with results in the browser). -> SOURCE: parity-albumen-search

**Fidelity:** new build, no baseline; captured to docs/captures/albumen/search/.
**Design:** docs/design/components/TextBox/README.md, docs/design/components/Menu/README.md, docs/design/components/ComboBox/README.md, docs/design/components/ListTree/README.md, docs/design/components/Panel/README.md, docs/design/components/Dialog/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user types a word and finds matching photos across names, metadata, categories, keywords, and people, or builds a precise query they can rerun later, including over folders never indexed. Consumer: the grid, the catalog pane's Saved Searches group, and `D04 T11 §1`'s activity history, which reopens a search.
**Treatment:** a search box with a scope menu and history; an Advanced Search pane (Match all or any, sources: catalog, folders, current view; file types; a criterion picker; a preset menu); Saved Searches in the catalog pane; Search Files (IrfanView) as a dialog whose results open in the browser. Cheaper substitute that fails the checkpoint: search limited to filenames.
**Chrome:** consume §4's `FilterSqlCompiler`, `D04 T05 §4`'s browser for disk results, the `D03 T17 §10` readers, and the settings store. Do not add a second metadata reader.

**Requires:** display-session -- the search pane and dialog are driven on an interactive desktop

- [ ] Add an FTS5 table in `src/Albumen/Isotone.Albumen.Core/Search/SearchIndex.cs` over names, captions, titles, keywords, categories, AI keywords, and people names, maintained by triggers through a forward migration (LP-0350). Done when: `SearchIndexTests` assert a keyword edit is searchable in the same transaction.
- [ ] Add quick search (LP-0349): scope, match types (contains, whole word, starts with), classic operators (AND, OR, NOT, quotes), and history in `Albumen.Search.History`. Done when: `QuickSearchTests` cover each match type and operator.
- [ ] Add the quick search box with its scope menu and history dropdown in `src/Albumen/Isotone.Albumen.Desktop/Search/QuickSearchBox.xaml`. Done when: a capture shows the scope menu.
- [ ] Add `AdvancedSearchQuery` in `src/Albumen/Isotone.Albumen.Core/Search/Advanced/` (LP-0351): match all or any, sources, file types, AND and OR groups, per-criterion options, and history, compiled through §4. Done when: `AdvancedSearchCompilerTests` assert a two-group query on a seeded catalog.
- [ ] Add folder handling (LP-0353): folders, folders and contents, and contents only. Done when: a test covers each mode.
- [ ] Add the filename criterion (LP-0354) with any or all terms, history autocomplete, and a `WildcardMatcher` supporting `*`, `?`, sets, ranges, and escapes. Done when: `WildcardMatcherTests` cover each construct.
- [ ] Add the text, people, keyword, category, rating, and label criteria (LP-0355). Done when: `AdvancedSearchCompilerTests` cover each.
- [ ] Add the metadata criterion types (LP-0356): string, date and time, lookup list, integer, and rational, with literal semicolons escaped. Done when: `AdvancedSearchCompilerTests.MetadataTypes` cover each type.
- [ ] Add the Advanced Search pane in `src/Albumen/Isotone.Albumen.Desktop/Search/AdvancedSearchPane.xaml` with keyboard access to every row. Done when: a capture under docs/captures/albumen/search/ shows a two-group query. Cheaper substitute: a text box with a syntax.
- [ ] Add search presets and saved searches (LP-0347, LP-0348, LP-0352): choose, save, and delete, listed in §6's catalog pane and rerun with one click. Done when: `SavedSearchTests` save, list, rerun, and delete.
- [ ] Add `DiskSearch` in `src/Albumen/Isotone.Albumen.Core/Search/Disk/DiskSearch.cs` (LP-0357): name pattern, start folder with subfolders, and a file date range, cancellable, without writing the catalog. Done when: `DiskSearchTests` find fixtures in a temp tree and assert no catalog row is added.
- [ ] Add metadata text search to `DiskSearch` (LP-0358): EXIF, IPTC, comments, exact phrase, and any metadata present, read through the `D03 T17 §10` readers. Done when: `DiskSearchTests.MetadataText` finds a caption in a JPEG fixture.
- [ ] Add the Search Files dialog showing results as thumbnails in `D04 T05 §4`'s browser (LP-0359). Done when: a driven disk search opens its results in a browse tab (capture).
- [ ] Measure quick search on a generated 50,000-photo catalog. Done when: the median answer time is quoted under 200 ms.
- [ ] Write `docs/user/albumen/search.md`. Done when: quick, advanced, saved, and disk search are on the page.
- [ ] Commit: `"albumen: quick search, advanced search, saved searches, and disk search"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~SearchIndexTests|FullyQualifiedName~QuickSearchTests|FullyQualifiedName~AdvancedSearchCompilerTests|FullyQualifiedName~WildcardMatcherTests|FullyQualifiedName~SavedSearchTests|FullyQualifiedName~DiskSearchTests"` exits 0, quick search over 50,000 photos answers under 200 ms (quoted), and a saved search reruns from the catalog pane (capture). Cheaper substitute that fails: `LIKE` scans, which the timing catches.

## 8. Folders and catalog panels: synchronize, relocate, missing photos, and offline volumes

Photographers move folders in Explorer, unplug drives, and archive to discs; a catalog that loses track of them loses their work. This section adds the Folders panel with volumes, the Catalog panel's sets, synchronize, missing-folder and missing-photo recovery, a rebind service that finds files moved outside Albumen, drive mapping, and offline volumes that stay browsable from cached thumbnails. Rename, move, and delete go through `D04 T05 §6`'s file operations and never touch image bytes. Catalog: LP-0360, LP-0365 to LP-0378 (15 features: current and previous import, the Catalog panel, volumes, folder operations, synchronize, parent display, missing folders, folder labels and favorites, subfolder display, go to folder, remove or recycle, missing photos, rebind, drive mapping, and offline media). -> SOURCE: parity-albumen-folders

**Fidelity:** Folders and catalog panels -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/folders-panel/. **Corrected 2026-09-27:** cited docs/captures/albumen/main-window/ as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Dialog/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Menu/README.md, docs/design/components/Icons/README.md, docs/design/components/Button/README.md, docs/design/components/Progress/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer keeps the catalog in step with the disk, finds what moved, and still sees photos on a disconnected drive or disc. Consumer: the grid, `D04 T07 §1`'s Import to This Folder, and §9's restore with drive mapping.
**Treatment:** the Folders panel with volume headers (free space, counts, online dot); a Synchronize Folder dialog (import new, remove missing, rescan metadata, with a dry-run count); Find Missing Folder, Update Location, Show Parent, folder color and favorite badges; the Catalog panel entries; and an offline-volume manager. Cheaper substitute that fails the checkpoint: a folder list that goes stale until reimport.
**Chrome:** consume `D04 T05 §2`'s indexer and watcher, `D04 T05 §6`'s file operations for rename, move, and recycle, the catalog, and the suite history. Do not add a second file-operation path.

**Requires:** display-session -- the panels and relocation dialogs are driven on an interactive desktop

- [ ] Add the volume model in `src/Albumen/Isotone.Albumen.Core/Catalog/Volumes/VolumeService.cs` (LP-0366): volume serial, label, type, online state, and free space, refreshed on `WM_DEVICECHANGE`. Done when: `VolumeStateTests` flip a fake volume offline and online.
- [ ] Add the Folders panel volume headers in `src/Albumen/Isotone.Albumen.Desktop/Panels/FoldersPanel.xaml` with free space, counts, and the online dot. Done when: a capture under docs/captures/albumen/folders-panel/ shows an offline volume dimmed.
- [ ] Add the folder operations (LP-0367): add, create, rename, move by drag, remove from catalog, and show in Explorer, with rename and move through `D04 T05 §6`, and a rename or move that Windows denies permission for (a read-only volume, a locked folder) refused by name with the catalog unchanged. Done when: `FolderOperationTests` rename and move a temp folder, assert the catalog paths follow, undo, and assert the refusal on a read-only folder.
- [ ] Add folder color labels, favorites, and the folder filter (LP-0371), subfolder display and path styles (LP-0372), and Go to Folder and Go to Collection (LP-0373). Done when: `FolderPanelViewModelTests` cover each.
- [ ] Add `FolderSynchronizer` in `src/Albumen/Isotone.Albumen.Core/Catalog/Volumes/FolderSynchronizer.cs` (LP-0368): new files imported in place (Add), missing removed, and metadata rescanned, with a dry-run count before anything changes. Done when: `FolderSynchronizerTests` assert the dry-run counts equal the applied changes in a temp tree.
- [ ] Add the Synchronize Folder dialog showing the dry-run counts. Done when: a capture shows the counts. Cheaper substitute: synchronize without a preview.
- [ ] Add parent display (LP-0369): Show Parent Folder and Hide This Parent. Done when: a test asserts the tree before and after.
- [ ] Add missing folders (LP-0370): a badge, Update Folder Location, Find Missing Folder, and an alert when a parent is missing. Done when: `MissingPhotoTests.FolderRelocated` moves a temp folder and relocates it with every rating kept.
- [ ] Add the Catalog panel (LP-0360, LP-0365): all photographs, current and previous import (selected during import), missing photographs, added by previous export, errors, and updated photos. Done when: `CatalogPanelTests` assert each set's count on a seeded catalog.
- [ ] Add remove photos from the catalog or move them to the Recycle Bin (LP-0374) through `D04 T05 §6`, with a confirmation naming count and size. Done when: a test recycles a temp photo and its sidecar and undoes the catalog removal.
- [ ] Add find missing photos and locate a missing photo (LP-0375) with a file picker that checks size and capture time before rebinding. Done when: `MissingPhotoTests.LocateOne` passes.
- [ ] Add `RebindService` in `src/Albumen/Isotone.Albumen.Core/Catalog/Volumes/RebindService.cs` (LP-0376) matching files moved outside Albumen by size, capture time, and content hash, listing ambiguous matches instead of guessing. Done when: `RebindServiceTests` rebind files moved in a temp tree and report two identical-size files as ambiguous.
- [ ] Add drive mapping (LP-0377) when importing or restoring a catalog: a dialog mapping each missing root to a present volume. Done when: `DriveMappingTests` remap `E:\` to `F:\` and every photo resolves.
- [ ] Add photo discs and offline media (LP-0378): new, browse offline from cached thumbnails, update, identify by serial or label, and rebind. Done when: `VolumeStateTests.OfflineBrowse` lists an offline volume's photos from the cache.
- [ ] Log one Serilog Information line per folder operation, synchronize, relocation, and rebind. Done when: a Serilog test logger asserts each line.
- [ ] Write `docs/user/albumen/folders.md`. Done when: every panel, dialog, and recovery path is on the page.
- [ ] Commit: `"albumen: folders and catalog panels with synchronize, relocate, and offline volumes"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~VolumeStateTests|FullyQualifiedName~FolderOperationTests|FullyQualifiedName~FolderSynchronizerTests|FullyQualifiedName~MissingPhotoTests|FullyQualifiedName~RebindServiceTests|FullyQualifiedName~DriveMappingTests|FullyQualifiedName~CatalogPanelTests"` exits 0, and a driven session moves a fixture folder in Explorer, Albumen marks it missing, Find Missing Folder relocates it, and every rating survives (log lines and captures under docs/captures/albumen/missing-photos/). Cheaper substitute that fails: path-only matching, which `RebindServiceTests` catches.

**Freeze check:** Folder rename, move, and remove, and photo recycle go through `D04 T05 §6`'s file operations after a confirmation naming count and size; none opens an image for writing, and a test asserts every moved fixture's SHA-256 equals its pre-move hash. Synchronize, relocation, rebind, and drive mapping write only the catalog. Fixture source: `tests/fixtures/albumen/import/` copied to a temp tree per test.

## 9. Catalog backup and maintenance

The catalog is a user document holding years of ratings and edits, so it needs what Lightroom and ACDSee give it: scheduled backups that are tested, a restore, a lock against a second writer, and repair tools. This section promotes backlog B-036 (**Corrected 2026-09-28:** the entry left the backlog in the 2026-09-27 integration; library statistics are §12). A backup uses SQLite's online backup API, never a file copy of an open WAL-mode catalog, and a backup that includes images copies them with hash verification and never moves them. Catalog: LP-0379 to LP-0388 (10 features: optimize and relaunch, the catalog lock, scheduled backup, optimize from preferences, the backup wizard, restore, maintenance, database optimize, rebuild thumbnails and metadata, and quarantine). -> SOURCE: albumen-roadmap-catalog

**Fidelity:** new build, no baseline; captured to docs/captures/albumen/backup/ and docs/captures/albumen/maintenance/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/RadioButton/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md, docs/design/components/Progress/README.md, docs/design/components/StatusBar/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer never loses years of ratings and edits to a corrupt or deleted catalog and can repair it when it misbehaves. Consumer: the catalog, §8's drive mapping on restore, and §12's Database tab.
**Treatment:** Catalog Settings, Backup page (schedule: never, weekly on exit, daily on exit, every exit; folder; test integrity; optimize after; compress); the backup-on-exit dialog with Skip This Time; a Backup and Restore wizard; File, Optimize Catalog and Relaunch and Optimize; a Database Maintenance dialog. Cheaper substitute that fails the checkpoint: a file copy of the open catalog.
**Chrome:** consume the catalog, `Microsoft.Data.Sqlite` (MIT) and its online backup API, `System.IO.Compression`, `AtomicFileWriter`, the status strip progress, and the settings store. Do not add a second progress pattern.

**Requires:** display-session -- the backup wizard, the exit dialog, and the maintenance dialog are driven on an interactive desktop

- [ ] Add `CatalogBackupService` in `src/Albumen/Isotone.Albumen.Core/Maintenance/CatalogBackupService.cs` (LP-0381) writing a SQLite online backup into a dated folder under `Albumen.Backup.Folder`. Done when: `CatalogBackupTests.OnlineBackup` backs up a catalog under concurrent writes and the copy holds every committed row.
- [ ] Run `PRAGMA integrity_check` on each backup copy and refuse a failing copy by name. Done when: `CatalogBackupTests.CorruptionRefused` flips one byte in a scratch backup and the check names the file.
- [ ] Add optional optimize-after and ZIP compression of the backup, and retention by `Albumen.Backup.Keep` (default 10). Done when: `CatalogBackupTests.Retention` keeps exactly the newest ten.
- [ ] Add the schedule `Albumen.Backup.Schedule` (weekly on exit, daily on exit, every exit, or off) with the backup-on-exit dialog and Skip This Time. Done when: `BackupScheduleTests` assert when each schedule fires with a fake clock, and a capture of the dialog is committed.
- [ ] Show backup and optimize progress with Cancel on the status strip, and a completion notification naming the backup folder, its size, and the integrity result. Done when: a driven backup shows the notification (capture) and a cancelled backup leaves no partial folder.
- [ ] Add the Backup and Restore wizard (LP-0383) in `src/Albumen/Isotone.Albumen.Desktop/Maintenance/BackupWizard.xaml`: new or update backup, location, thumbnails, image and media files (copied with SHA-256 verification, never moved), scopes, daily folders, and a reminder interval. Done when: `BackupWizardTests` back up a temp folder with images and every copied hash matches its source. Cheaper substitute: an unverified folder copy.
- [ ] Add restore (LP-0384): choose a backup, verify integrity, restore to a new path (never over the open catalog), and remap drives through §8. Done when: `CatalogBackupTests.RestoreEqual` restores and compares every table row by row.
- [ ] Add the catalog lock (LP-0380): a lock file beside the catalog with the process id and machine name, a second open refused with a message naming the holder, and a stale lock from a dead process cleared after confirmation. Done when: `CatalogLockTests` cover held, refused, and stale.
- [ ] Add optimize (LP-0379, LP-0382, LP-0386): `VACUUM`, `REINDEX`, `ANALYZE`, and orphan removal, from File, Optimize Catalog, from Preferences, and as Relaunch and Optimize. Done when: `OptimizeTests` assert the orphan count drops to zero and the catalog opens.
- [ ] Add the Database Maintenance dialog (LP-0385) in `src/Albumen/Isotone.Albumen.Desktop/Maintenance/MaintenanceDialog.xaml`: per-folder records, remove thumbnails, remove all info for a folder (with a confirmation naming the folder and count), remove orphan folders, and change binding. Done when: `MaintenanceTests` cover each command with undo where the catalog allows.
- [ ] Add rebuild thumbnails and metadata for a selection or folder (LP-0387) through `D04 T05 §2`'s indexer queue. Done when: a test rebuilds a folder and asserts refreshed cache entries.
- [ ] Add the quarantine (LP-0388): files that fail to decode twice are listed, skipped by the indexer, and re-enabled from the list, controlled by `Albumen.Maintenance.Quarantine` (default on). Done when: `QuarantineTests` assert a truncated fixture is quarantined after two failures and re-enabled.
- [ ] Log one Serilog Information line per backup, restore, optimize, and maintenance run with its duration and result. Done when: a Serilog test logger asserts each line.
- [ ] Write `docs/user/albumen/catalog-backup.md` covering schedules, the wizard, restore, the lock, and maintenance. Done when: every Treatment control is on the page.
- [ ] Treat `AlbumenViewer.exe` and `Albumen.exe --index` as cooperating writers: they register in the lock file and open the catalog in WAL mode with a busy timeout, while a second `Albumen.exe` UI instance, another machine, or another user is refused by name; the headless indexer yields and exits when `Albumen.exe` starts (**Groomed 2026-09-28:** the lock as written refused Albumen's own viewer and indexer). Done when: `CatalogLockTests.CooperatingProcesses` write a rating from the viewer while `Albumen.exe` holds the lock and refuse a second UI instance.
- [ ] Commit: `"albumen: scheduled catalog backups, restore, and maintenance"`

**Test checkpoint:** Unit test plus format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~CatalogBackupTests|FullyQualifiedName~BackupScheduleTests|FullyQualifiedName~BackupWizardTests|FullyQualifiedName~CatalogLockTests|FullyQualifiedName~OptimizeTests|FullyQualifiedName~MaintenanceTests|FullyQualifiedName~QuarantineTests"` exits 0: a backup of the fixture catalog restores to a catalog whose every table compares equal row by row, and the corruption test fails the integrity check by name; a driven backup on exit completes with progress (log quoted). Cheaper substitute that fails: copying the open file, which `CatalogBackupTests.OnlineBackup` shows losing committed WAL rows.

**Freeze check:** A backup reads the catalog through the online backup API and writes only into the backup folder; restore writes a new catalog path and never overwrites the open catalog; image files included in a backup are copied and hash-verified, never moved or opened for writing, and a test asserts every source image's SHA-256 and last-write time are unchanged. Fixture source: `tests/fixtures/albumen/catalog/` (a small catalog created by this section) and `tests/fixtures/albumen/import/`.

## 10. Multiple catalogs, catalog settings, and preview management

Photographers split catalogs between a laptop and a desktop, merge them back, and arrive from Lightroom or Photoshop Elements with years of ratings, labels, keywords, and collections. This section adds recent catalogs, catalog export with negatives, import from another Albumen catalog, a read-only Lightroom Classic and Elements catalog importer that never writes the source file, ACDSee's compressed and XML exports, a file listing, catalog settings, and preview building and discarding. Lightroom's schema is undocumented, so the importer is proven on a committed fixture and reports anything it cannot map by name. Catalog: LP-0389 to LP-0400 (12 features: Elements import, Albumen catalog import, catalog export, preview building, recent catalogs, catalog settings, preview settings, catalog settings from preferences, Lightroom import, multiple catalogs, ACDSee catalog export, and the file listing). -> SOURCE: parity-albumen-catalogs

**Fidelity:** new build, no baseline; captured to docs/captures/albumen/catalog-exchange/ and docs/captures/albumen/catalog-settings/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Menu/README.md, docs/design/components/ListTree/README.md, docs/design/components/Checkbox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/RadioButton/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Progress/README.md, docs/design/components/WindowChrome/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer splits and merges catalogs between machines and moves from Lightroom or Elements without losing ratings, labels, keywords, and collections. Consumer: the catalog, §11's smart previews in exports, and the preview cache.
**Treatment:** File, New Catalog, Open Catalog, Open Recent; File, Export as Catalog (negatives, previews, selected only); File, Import from Another Catalog with a changed-photos policy (preserve old settings as a virtual copy, replace non-raw only); File, Import from Lightroom Classic Catalog with a summary; Catalog Settings (location, previews, file handling); Library, Previews submenu. Cheaper substitute that fails the checkpoint: an importer that brings photos but not their metadata.
**Chrome:** consume the catalog, `Microsoft.Data.Sqlite` (MIT) opened `Mode=ReadOnly` for `.lrcat`, `D04 T01 §7`'s preview cache, `D01 T07 §6`'s XMP settings reader, and the suite history. Do not add a second SQLite provider.

**Requires:** display-session -- the catalog dialogs are driven on an interactive desktop

- [ ] Add recent catalogs and the catalog name in the title bar (LP-0393, LP-0398), extending `D04 T01 §5`'s New and Open Catalog, stored in `Albumen.Catalog.Recent`. Done when: `CatalogSwitchTests` open three catalogs and read the recent list back in order.
- [ ] Add `CatalogExporter` in `src/Albumen/Isotone.Albumen.Core/CatalogExchange/CatalogExporter.cs` (LP-0391): a folder, collection, or selection as a new catalog with negatives (copied and hash-verified), previews, and selected-only. Done when: `CatalogExportImportTests.Export` exports a subset and every copied negative's hash matches.
- [ ] Add `AlbumenCatalogImporter` (LP-0390): file handling (add, copy, move to the Recycle Bin after verification), a changed-existing-photos policy, old settings preserved as a virtual copy through §3's `VirtualCopyService`, and replace non-raw only. Done when: `CatalogExportImportTests.RoundTrip` imports an export into an empty catalog and compares every table row by row.
- [ ] Add `LightroomCatalogImporter` in `src/Albumen/Isotone.Albumen.Core/CatalogExchange/Lightroom/` (LP-0397) opening `.lrcat` with `Mode=ReadOnly` and mapping ratings, flags, labels, keywords with hierarchy, collections, and file locations. Done when: `LightroomCatalogImporterTests` import a committed small `.lrcat` fixture made with Lightroom Classic 15.5.1 (version recorded in its README) with every documented value equal.
- [ ] Read each imported photo's develop settings from its `crs` XMP through `D01 T07 §6`, and report unmappable settings by name in the summary. Done when: the fixture's exposure and white balance arrive in the edit stack and an unknown setting is named.
- [ ] Assert the `.lrcat` file's SHA-256 is unchanged after import. Done when: `LightroomCatalogImporterTests.SourceUntouched` passes.
- [ ] Add Photoshop Elements catalog import (LP-0389) on the same read-only path over the Elements schema. Done when: a committed Elements fixture (version recorded) imports its tags and ratings, or the section records that no fixture could be produced and names the owner that will add one.
- [ ] Add the import summary dialog (imported, skipped with reasons, unmapped fields). Done when: a capture under docs/captures/albumen/catalog-exchange/ shows the summary.
- [ ] Add ACDSee-style exports (LP-0399): a compressed catalog of all or selected items and an XML text export of chosen fields, with location options and optimize after import. Done when: `CatalogTextExportTests` validate the XML against its schema file.
- [ ] Add the file listing (LP-0400) as a tab-separated text table of chosen fields written through `AtomicFileWriter`. Done when: `FileListingTests` assert the header and a row.
- [ ] Add Catalog Settings (LP-0394, LP-0396) in `src/Albumen/Isotone.Albumen.Desktop/Catalog/CatalogSettingsDialog.xaml`: location with Show in Explorer, file handling, and the same page reachable from Preferences. Done when: a capture under docs/captures/albumen/catalog-settings/ is committed.
- [ ] Add preview settings (LP-0395): standard preview size and quality and auto-discard of 1:1 previews after a period, extending `D04 T01 §7` as `Albumen.Previews.*`. Done when: `PreviewManagementTests.AutoDiscard` removes 1:1 previews older than the period with a fake clock.
- [ ] Add Library, Previews: Build Standard, Build 1:1, and Discard 1:1 (LP-0392), queued through `D04 T05 §2`'s indexer with progress. Done when: `PreviewManagementTests` build and discard for a selection.
- [ ] Log one Serilog Information line per catalog switch, export, and import with counts. Done when: a Serilog test logger asserts each line.
- [ ] Write `docs/user/albumen/catalogs.md` covering multiple catalogs, export, import from Albumen, Lightroom, and Elements, and previews. Done when: every Treatment command is on the page.
- [ ] Commit: `"albumen: multiple catalogs, catalog exchange, and Lightroom catalog import"`

**Test checkpoint:** Format fidelity proof plus unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~CatalogSwitchTests|FullyQualifiedName~CatalogExportImportTests|FullyQualifiedName~LightroomCatalogImporterTests|FullyQualifiedName~CatalogTextExportTests|FullyQualifiedName~FileListingTests|FullyQualifiedName~PreviewManagementTests"` exits 0: the Lightroom fixture imports with every rating, label, keyword path, and collection membership equal to the fixture's documented values and its SHA-256 unchanged, and an Albumen export and import compares equal table by table. Cheaper substitute that fails: importing files only, which the metadata comparison catches.

**Freeze check:** Catalog export copies negatives with hash verification and never moves or writes the source images; the Lightroom and Elements importers open their source catalogs read-only and a test asserts the source file's SHA-256 is unchanged; import with Move sends a source to the Recycle Bin only after its copy verifies. Fixture source: `tests/fixtures/albumen/catalogs/` (the `.lrcat` and Elements fixtures, created by this section) and `tests/fixtures/albumen/import/`.

## 11. Smart previews and offline editing

A photographer on a laptop wants to keep developing when the photo drive is at home. Lightroom's smart previews are lossy DNG proxies at 2,560 px that develop reads when the original is offline; edits stay in normalized coordinates, so they apply unchanged to the original when it returns. This section builds them on `D04 T13 §7`'s DNG writer. Catalog: LP-0401, LP-0554 (2 features: smart previews and the original or smart preview indicator). -> SOURCE: parity-albumen-smart-previews

**Fidelity:** Smart previews and offline editing -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/smart-previews/. **Corrected 2026-09-27:** cited docs/captures/albumen/develop/ (baseline from `D04 T02 §3`) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Menu/README.md, docs/design/components/Progress/README.md, docs/design/components/StatusBar/README.md, docs/design/components/Icons/README.md, new surface: docs/design/components/AlbumenDevelop/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer keeps developing on a laptop when the photo drive is at home, and the edits apply to the originals when it returns. Consumer: `D04 T02 §2`'s develop pipeline, export, catalog export (§10), and `D04 T07 §2`'s build-on-import option.
**Treatment:** Library, Previews, Build and Discard Smart Previews; a status line under the histogram (Original, Smart Preview, Original and Smart Preview); a cache size readout in Catalog Settings. Cheaper substitute that fails the checkpoint: developing on the 2,048 px JPEG preview.
**Chrome:** consume `D04 T13 §7`'s lossy DNG writing, `D04 T02 §2`'s pipeline, and the preview cache. Do not add a second DNG writer.

**Requires:** display-session -- the offline develop check is driven on an interactive desktop

- [ ] Write or extend the design spec `docs/design/components/AlbumenDevelop/README.md` and `preview.html` with the smart-preview indicator under the histogram (window or module layout only; the panels come from the shared `docs/design/components/DevelopPanels/README.md`; (anatomy, every state, tokens, sizes; `D04 T02 §3` writes the spec) before building; Done when: the spec covers it and the design page rebuild passes.
- [ ] Add `SmartPreviewStore` in `src/Albumen/Isotone.Albumen.Core/SmartPreviews/SmartPreviewStore.cs` (LP-0401): lossy DNG at 2,560 px long edge through `D04 T13 §7` in `<catalog>.smartpreviews/`, keyed by image id and file hash. Done when: `SmartPreviewStoreTests` build, find, and discard a proxy.
- [ ] Enforce the size limit `Albumen.SmartPreviews.MaxMB` and report per-photo status and the total size in Catalog Settings. Done when: `SmartPreviewStoreTests.Limit` refuses a build past the limit with a message naming it.
- [ ] Add Build and Discard Smart Previews to Library, Previews, queued with progress and Cancel. Done when: a test builds proxies for a selection and cancels midway leaving no partial file.
- [ ] Fall back to the smart preview as the develop source when the original's volume is offline (from §8), keeping settings in normalized coordinates (`D01 T07`). Done when: `OfflineDevelopTests` develop from the proxy and render the original after the volume returns with crops and masks aligned within 1/255 after resampling to the same size.
- [ ] Add the indicator under the histogram (LP-0554) and a smart-preview state column in §4's filter bar. Done when: a capture shows each of the three states.
- [ ] Render exports while offline from the smart preview at its size and say so in the export summary. Done when: `OfflineDevelopTests.ExportSummary` asserts the summary line.
- [ ] Include smart previews in §10's catalog export when chosen. Done when: `CatalogExportImportTests.SmartPreviews` finds them in the exported catalog.
- [ ] Log one Serilog Information line per build, discard, and offline fallback. Done when: a Serilog test logger asserts each line.
- [ ] Write `docs/user/albumen/smart-previews.md`. Done when: building, the indicator, offline develop, and export are on the page.
- [ ] Commit: `"albumen: smart previews for offline develop"`

**Test checkpoint:** Unit test plus format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~SmartPreviewStoreTests|FullyQualifiedName~OfflineDevelopTests"` exits 0, with a proxy render and the original render of the same settings agreeing within 1/255 after resampling to the same size; a driven offline develop with the fixture drive disconnected is captured under docs/captures/albumen/smart-previews/. Cheaper substitute that fails: JPEG previews, which clip the highlights the comparison keeps.

## 12. The dashboard and library statistics

`D04 T01 §10` shows a statistics summary in a header menu; ACDSee has a Dashboard mode that tells a photographer what they shoot, with what, and how healthy the library is. This section extends the statistics into that mode, drawn with the suite theme and no charting package, and completes backlog B-036's statistics half. Catalog: LP-0402 to LP-0406 (5 features: the dashboard mode, overview, database, cameras, and files tabs). -> SOURCE: parity-albumen-dashboard

**Fidelity:** new build, no baseline; captured to docs/captures/albumen/dashboard/.
**Design:** docs/design/components/Tabs/README.md, docs/design/components/ListTree/README.md, new surface: docs/design/components/AlbumenDashboard/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer sees what they shoot, with what, and how big and healthy the library is. Consumer: none: this surface is the consumer of the catalog's statistics.
**Treatment:** a Dashboard module with Overview (photos by year or month, database, camera, and file summaries), Database (size, path, files and folders, orphans, last backup, thumbnail cache), Cameras (most used body, lens, focal length, aperture, shutter, ISO charts with toggles), and Files (formats, bit depths, top 20 resolutions). Cheaper substitute that fails the checkpoint: a text dump of counts.
**Chrome:** consume grouped catalog queries, the `Isotone.UI` theme brushes, and WPF drawing for charts. Do not add a charting package.

**Requires:** display-session -- the dashboard is driven on an interactive desktop

- [ ] Write the design spec `docs/design/components/AlbumenDashboard/README.md` and `preview.html` (the dashboard: tabs, bar and pie charts drawn from theme brushes, and the tables; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Extend `D04 T01 §10`'s statistics into `LibraryStatistics` in `src/Albumen/Isotone.Albumen.Core/Library/Statistics/LibraryStatistics.cs` (LP-0402) with grouped queries per tab, cached and invalidated by catalog change counters. Done when: `LibraryStatisticsTests` match known counts on a seeded catalog and a rating change invalidates the cache.
- [ ] Add the Overview tab (LP-0403): photos by year or month and the database, camera, and file summaries. Done when: a capture under docs/captures/albumen/dashboard/ is committed.
- [ ] Add the Database tab (LP-0404): size and path, file and folder breakdown, orphans, last backup date read from §9, and thumbnail cache size. Done when: a test asserts the last-backup value after a §9 backup.
- [ ] Add the Cameras tab (LP-0405): most used body, lens, focal length, aperture, shutter, and ISO charts with graph toggles. Done when: a capture shows each chart.
- [ ] Add the Files tab (LP-0406): format and bit-depth charts and the top 20 resolutions. Done when: `LibraryStatisticsTests.TopResolutions` asserts the order on the seeded catalog.
- [ ] Add a `StatChart` control in `src/Albumen/Isotone.Albumen.Desktop/Dashboard/StatChart.cs` drawing bar and line charts with theme brushes, keyboard focus on bars, and an `AutomationProperties.Name` per bar. Done when: `StatChartTests` assert the automation names for a three-bar series. Cheaper substitute: a text table.
- [ ] Clicking a bar filters the library through §4's `LibraryFilter`. Done when: a test clicks the 2025 bar and the grid filter holds that year.
- [ ] Measure dashboard rendering on a generated 50,000-photo catalog. Done when: the render time is quoted under 500 ms.
- [ ] Write `docs/user/albumen/dashboard.md`. Done when: every tab is on the page.
- [ ] Commit: `"albumen: the dashboard with catalog, camera, and file statistics"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~LibraryStatisticsTests|FullyQualifiedName~StatChartTests"` exits 0 with the seeded counts matched, and the dashboard renders under 500 ms on 50,000 photos (quoted, captured). Cheaper substitute that fails: counting by loading every record, which the timing catches.

## 13. Painter and Quick Develop

Lightroom's Painter sprays one attribute over scattered photos, and its Quick Develop panel nudges a whole selection without entering Develop. This section adds both on top of §2's culling commands, §5's target collection, `D04 T01 §10`'s keywords, `D04 T02 §5`'s presets, and `D04 T02 §1`'s edit stack. Quick Develop applies relative deltas so each photo keeps its own values. Painting a metadata preset waits for `D04 T08 §3` and is disabled with a tooltip naming it until then. Catalog: LP-0287 to LP-0289 (3 features: painting flags, ratings, and labels, the Painter modes, and Quick Develop). -> SOURCE: parity-albumen-painter

**Fidelity:** new build, no baseline; captured to docs/captures/albumen/painter/ and docs/captures/albumen/quick-develop/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Button/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Menu/README.md, docs/design/components/Slider/README.md, docs/design/components/Icons/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer applies one attribute to many scattered photos by painting over them, and nudges exposure on a whole selection without entering Develop. Consumer: the catalog, the edit stack, and sidecars through `D04 T01 §11`.
**Treatment:** the grid toolbar's spray can with a Paint menu and value field, drag to spray, Alt to erase; the Quick Develop panel in the right column with small and large relative steps and Reset All. Cheaper substitute that fails the checkpoint: absolute settings that overwrite each photo's values.
**Chrome:** consume §2's culling commands, §5's target collection, `D04 T01 §10` keywords, `D04 T02 §5` presets, `D04 T02 §1`'s edit stack, and `D01 T07 §1`'s tone stages. Do not add a second preset store.

**Requires:** display-session -- painting over the grid is driven on an interactive desktop

- [ ] Add `PainterTool` in `src/Albumen/Isotone.Albumen.Desktop/Library/Painter/PainterTool.cs` (LP-0287, LP-0288) with modes keywords, label, flag, rating, develop preset, rotation (metadata orientation), and target collection. Done when: `PainterToolTests` apply each mode to three cells.
- [ ] Add the metadata-preset mode, disabled with a tooltip naming `D04 T08 §3` until that section ships. Done when: a test asserts the disabled state and the tooltip text.
- [ ] Add erase with Alt and one undo step per stroke. Done when: `PainterToolTests.EraseAndUndo` passes.
- [ ] Add the spray-can cursor, Paint menu, and value field to the grid toolbar, with auto-dismiss after a stroke as `Albumen.Painter.AutoDismiss`. Done when: a capture under docs/captures/albumen/painter/ shows the toolbar in each mode.
- [ ] Log one Serilog Information line per stroke naming the mode, the value, and the photo count. Done when: a Serilog test logger asserts one line for a 30-photo stroke.
- [ ] Add `QuickDevelopService` in `src/Albumen/Isotone.Albumen.Core/Develop/QuickDevelopService.cs` (LP-0289) adding relative deltas (exposure plus or minus one third or one stop, contrast, highlights, shadows, whites, blacks, clarity, vibrance) to each photo's current `DevelopSettings`. Done when: `QuickDevelopTests` assert per-photo differences are kept after a step.
- [ ] Add saved preset, crop ratio, treatment, white balance preset, and Reset All to `QuickDevelopService`, each one undo step across the selection. Done when: `QuickDevelopTests` cover each and undo.
- [ ] Add the Quick Develop panel in `src/Albumen/Isotone.Albumen.Desktop/Library/Panels/QuickDevelopPanel.xaml` with keyboard-operable steps and the applied delta shown in the status strip. Done when: a capture under docs/captures/albumen/quick-develop/ is committed. Cheaper substitute: absolute sliders.
- [ ] Log one Serilog Information line per Quick Develop step with the delta and photo count. Done when: a Serilog test logger asserts it.
- [ ] Write `docs/user/albumen/painter-quick-develop.md`. Done when: every mode and step is on the page.
- [ ] Commit: `"albumen: the Painter and Quick Develop"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~PainterToolTests|FullyQualifiedName~QuickDevelopTests"` exits 0, and a driven stroke over 30 photos adds a keyword to each as one undo entry (log line quoted). Cheaper substitute that fails: absolute Quick Develop values, which the per-photo difference test catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx` exits 0 with this file's test classes reporting (`LibrarySortTests`, `DeleteRejectedTests`, `VirtualCopyTests`, `FilterPerformanceTests`, `SmartRuleCompilerTests`, `CategoryTreeTests`, `DiskSearchTests`, `RebindServiceTests`, `CatalogBackupTests`, `LightroomCatalogImporterTests`, `OfflineDevelopTests`, `LibraryStatisticsTests`, `QuickDevelopTests`)
- [ ] The unchanged-originals tests of §2, §8, §9, and §10 pass over `tests/fixtures/albumen/import/`
- [ ] The 50,000-photo budgets of §1, §4, §7, and §12 are quoted from one run on the reference machine
- [ ] The Lightroom `.lrcat` fixture and the `.lrsmcol` fixture round-trip as §5 and §10 state, versions quoted
- [ ] `python scripts/todo-graph.py query parity --catalog albumen --phase 33` reports every catalog row planned to this file stamped
- [ ] `python scripts/todo-graph.py validate` clean
