---
schema_version: 1
id: lumen-foundation
domain: 04-lumen
status: draft
title: "TODO-01 -- Lumen: App Spine, Library, and RAW Decode"
depends_on: []
frozen: true
track: L1
---

# TODO-01 -- Lumen: App Spine, Library, and RAW Decode

> **Goal:** Lumen exists as the suite's third standalone app: it builds, installs, and starts like Nodus and Imago; it imports a folder of photos into a SQLite catalog without ever writing an original; it decodes camera RAW through a library chosen by recorded decision; and it shows the library as a fast, sortable, filterable grid with a loupe view, ratings, flags, color labels, keywords, and collections, with metadata optionally mirrored to XMP sidecars.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Lumen has no code. `src/Lumen.UI/TODO.md`, the only file it had, was a list of intentions (RAW formats CR2, NEF, ARW, DNG; exposure, white balance, curves; batch; collections and smart collections; "send to Imago") naming no library, database, or metadata choice; it was mined into this file and removed on 2026-09-26. `scripts/apps.psd1` declares Lumen with `Project = 'src/Lumen/Lumen.UI/Lumen.UI.csproj'` and `Shipping = $false`, and `installer/Lumen.iss` refuses to compile unless `/DLumenShipping` is defined. `resources/icons/lens.png` (512 by 512, an aperture illustration) is the candidate icon art. `standards/lumen.md` states the contract: originals are never written, the catalog is SQLite with forward-only migrations, the develop pipeline is float32 linear-light.
<!-- claim: absent src/Lumen -->
<!-- claim: count "Shipping  = \$false" scripts/apps.psd1 = 1 -->
<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->
<!-- claim: exists resources/icons/lens.png -->
<!-- claim: exists standards/lumen.md -->

## Inputs

- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard, the catalog, the pipeline, the decoder rules
- [`standards/shared.md`](../../standards/shared.md) -- the stack, the design contract, performance budgets
- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- `src/Lumen/Photon.Lumen.Core` and `Photon.Lumen.Desktop`, and the rule that Lumen never needs Imago at runtime
- [`.claude/skills/plan-new-feature/SKILL.md`](../../.claude/skills/plan-new-feature/SKILL.md) -- the rigor this file was planned with; §1 completes its competitor step with driven runs
- raw.pixls.us (https://raw.pixls.us/) -- CC0 RAW samples per camera, the source of the pinned decode corpus
- -> XREF: D04 T02 §1 -- the edit stack that stores develop settings in §5's catalog
- -> XREF: D03 T07 §11 -- moves §4's decoder adapter to `Photon.Core` when Imago imports RAW
- -> XREF: D05 T01 §6 -- the suite bundle that ships Lumen beside Nodus and Imago

## Job and non-goals

**Job:** a photographer with thousands of RAW and JPEG files on disk wants to bring them into one place, find the good ones fast (by date, rating, flag, label, keyword, camera, lens, or folder), and develop them without ever risking the originals. Done, to them, means: point Lumen at a card or a folder, see thumbnails within seconds, cull with the keyboard, and trust that nothing on disk changed except what they explicitly exported.

**Audience:** enthusiast and working photographers who today use Lightroom Classic, darktable, or a file browser plus an editor.

**Non-goals for this file:** tethered capture; cloud sync; face recognition; maps and GPS editing; printing, books, and slideshows; video; plugins. Each is at most a backlog candidate (`todo/backlog.md`), not a promise.

**Working name and one-line purpose:** Lumen, "the darkroom and library for your photos" (quoted by the About dialog, the installer, and the user guide).

**Home:** its own app. What it shares goes through `Photon.Core` and `Photon.UI` only where Nodus or Imago already need the same thing (logging, settings, single instance, theme, dialogs).

## Competitor survey

From documentation, to be confirmed and extended by driven runs in §1 (each row then names the version driven):

| Capability | Lightroom Classic (Adobe docs) | darktable (docs, 5.x) | What Lumen does, and what beats them |
| ---------- | ------------------------------ | --------------------- | ------------------------------------ |
| Import | Add, copy, move; build previews; duplicate detection | Add to library or copy and import; film rolls | Add or copy with hash-verified copies and a dry-run count before anything moves |
| Catalog | SQLite catalog, previews cache beside it | SQLite library, XMP sidecar per image by default | SQLite catalog plus optional sidecars; catalog backup before every migration |
| Culling | Grid and loupe, P/X/U flags, 0-5 stars, color labels | Lighttable, stars, reject, color labels | The same keys, plus auto-advance and a compare view, with every action undoable |
| Search | Library filter bar, smart collections | Collections module, tagging | One filter bar over metadata, saved as smart collections |
| RAW decode | Adobe Camera Raw engine | rawspeed plus LibRaw fallback | LibRaw-class decoding (decided in §3) with a pinned-corpus coverage table |
| Metadata safety | Writes XMP to sidecars only when asked; DNG can be written in place | Sidecars always | Never writes an original, proven by a test over every fixture |
| Weakness to beat | Slow on large catalogs; subscription | Steep learning curve; dense UI | Fast grid at 50,000 photos, a plain UI, free and open source |

## Outcome

- `src/Lumen/Photon.Lumen.Core`, `src/Lumen/Photon.Lumen.Desktop` (`Lumen.exe`), and `tests/Photon.Lumen.Tests` build in `Photon.slnx`; `scripts/apps.psd1` marks Lumen shipping and `installer/Lumen.iss` compiles without the guard.
- `docs/dev/decisions.md` records the RAW decoder choice with licenses, coverage on a pinned corpus, and speed.
- Import adds or copies folders into the catalog, hash-verifies copies, skips duplicates, reads EXIF and XMP, and writes nothing into any original.
- The grid shows 50,000 photos with scrolling under 16 ms per frame from cached thumbnails; the loupe shows full previews with a filmstrip.
- Ratings, flags, labels, keywords, and collections are stored in the catalog, undoable, searchable, and optionally mirrored to `.xmp` sidecars.
- `todo/README.md` lists Lumen's original-file guard in the frozen set.

**Adjacency:** list=applicable @ D04 T01 §8; document=not-applicable (contact sheets and prints wait in the backlog as B-035); settings=applicable @ D04 T01 §2; reporting=applicable @ D04 T01 §10; notifications=applicable; permissions=applicable; audit=applicable; exchange=applicable; reverse=applicable

**Adjacency rationale:** The grid is the list; import progress and its completion summary are the notifications; a read-only card or an unreadable file is the refusal case; library statistics per collection are reporting; every metadata change logs, undoes, and exchanges through XMP sidecars.

## Implementation Order

| Order | Section | Deliverable                                              | Depends On                     | Status |
| :---: | :-----: | -------------------------------------------------------- | ------------------------------ | :----: |
|   1   |   §1    | The competitor survey, driven                            | --                             |  [ ]   |
|   2   |   §2    | Create the Lumen app                                     | D01 T01 §3, D01 T02 §3         |  [ ]   |
|   3   |   §3    | The RAW decoder decision                                 | §1, D00 T02 §5                 |  [ ]   |
|   4   |   §4    | RAW decode with fidelity fixtures                        | §2, §3                         |  [ ]   |
|   5   |   §5    | The catalog database                                     | §2                             |  [ ]   |
|   6   |   §6    | Import                                                   | §4, §5                         |  [ ]   |
|   7   |   §7    | Thumbnails and the preview cache                         | §6                             |  [ ]   |
|   8   |   §8    | The library grid                                         | §7                             |  [ ]   |
|   9   |   §9    | Loupe, compare, and filmstrip                            | §8                             |  [ ]   |
|  10   |   §10   | Keywords, collections, and smart collections             | §8                             |  [ ]   |
|  11   |   §11   | Ratings, flags, labels, and XMP sidecars                 | §8                             |  [ ]   |

---

## 1. The Competitor Survey, Driven

`plan-new-feature` requires the competitor table to come from using the competitors, each row naming the version used. The table above is from documentation. This section drives darktable (free, installable) and records Lightroom Classic from Adobe's documentation where it cannot be run here, saying so per row.

**Needs:** Windows host (build/test)

- [ ] Install darktable's current Windows release, import the pinned sample folder (§4's corpus subset, 50 files), and record import speed, thumbnail time, culling keys, filter options, metadata written to disk (hash every original before and after), and XMP sidecar behavior. Done when: `docs/dev/lumen/competitor-survey.md` has a darktable section naming the version and each measurement.
- [ ] Record Lightroom Classic's equivalent behaviors from Adobe's help pages (URL per claim), marked "from documentation, not driven". Done when: every row cites a URL.
- [ ] Revise this file's competitor table, and any section whose Treatment the survey contradicts, in the same commit. Done when: the table names versions and every "beats" claim has a measurement or a cited source.
- [ ] Commit: `"lumen: drive the competitor survey and correct the plan"`

**Requires:** display-session -- driving darktable's user interface needs an interactive desktop

**Test checkpoint:** `docs/dev/lumen/competitor-survey.md` exists with darktable's version, a before-and-after hash table of the 50 originals (all unchanged or the difference named), and a URL per Lightroom claim. Cheaper substitute that fails: a table from memory, which carries no version and no hashes.

## 2. Create the Lumen App

Lumen needs the same spine as the other two: projects in the suite layout, a composition root on `Photon.Core` logging and settings, single instance, the `Photon.UI` theme, splash, and exception window, an About dialog, and a working publish and installer. It ships nothing useful yet; it proves Lumen builds, installs, and starts. -> SOURCE: lumen-notes-structure

**Fidelity:** Lumen main window shell -- new build, no baseline; follows the window anatomy in `standards/shared.md` and is captured to docs/captures/lumen/main-window/.
**Job:** a user can install Lumen, start it, and see an empty library with an Import button. Consumer: every later Lumen section.
**Treatment:** a main window with the module switcher (Library, Develop) at the top, a left panel (folders, collections), the center grid area with the empty state "Your library is empty. Import a folder of photos to begin." and an Import button, a right panel (metadata), and a status strip; Help, About Lumen through `Photon.UI`. Cheaper substitute that fails the checkpoint: a blank window.
**Chrome:** consume `Photon.UI` (theme, splash, exception window, About and shortcuts dialogs, icon catalog) and `Photon.Core` (logging, settings, single instance). Do not copy any of them.

**Requires:** display-session -- launching the new app needs an interactive desktop

- [ ] Create `src/Lumen/Photon.Lumen.Core/Photon.Lumen.Core.csproj` (`net11.0`), `src/Lumen/Photon.Lumen.Desktop/Photon.Lumen.Desktop.csproj` (`net11.0-windows10.0.26100.0` with `TargetPlatformMinVersion` 10.0.17763.0, WPF; **Corrected 2026-09-26:** said `net10.0` and `net10.0-windows`, the suite moved to .NET 11, `AssemblyName` Lumen), `src/Lumen/Directory.Build.props` (MinVer prefix `lumen-v`, `Product` Lumen), and `tests/Photon.Lumen.Tests`, all in `Photon.slnx`. Done when: `dotnet build Photon.slnx -c Release` builds them.
- [ ] The composition root with `UsePhotonLogging("Lumen")`, the settings store, and single instance. Done when: a launch logs its startup line to `%LOCALAPPDATA%\Rizonesoft\Lumen\logs\`.
- [ ] The shell window and empty state per Treatment. Done when: a capture is committed.
- [ ] The Lumen icon from `resources/icons/lens.png` into `resources/icons/lumen/` (sizes as for Nodus), with its source and license status recorded in `resources/icons/README.md` pending operator confirmation (`D99 T01 §4`). Done when: `Lumen.exe` shows it.
- [ ] Set `Project` to `src/Lumen/Photon.Lumen.Desktop/Photon.Lumen.Desktop.csproj` and `Shipping = $true` in `scripts/apps.psd1`, and remove the `/DLumenShipping` guard from `installer/Lumen.iss`. Done when: `pwsh scripts/package.ps1 -App Lumen -Version 0.0.1-dev` produces an installer and a ZIP.
- [ ] Update `AGENTS.md`, `docs/dev/architecture.md`, and `docs/dev/build.md` to show Lumen as existing. Done when: no file says Lumen has no code.
- [ ] Commit: `"lumen: create the app on the suite spine"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with a `LumenServiceRegistrationTests` class reporting; the packaged installer installs silently and `Lumen.exe` starts to the empty state (capture) with 0 `[ERR]` lines in its log. Cheaper substitute that fails: a project that builds but is not packaged.

## 3. The RAW Decoder Decision

The decoder is Lumen's most consequential dependency: it sets camera coverage, color quality, speed, and license. Candidates, with the facts this section must verify: **LibRaw** (dual-licensed LGPL-2.1 or CDDL-1.0; LGPL-2.1 combines with GPL-3.0) through a .NET wrapper such as Sdcb.LibRaw (check its license and its bundled LibRaw version); **Magick.NET** (Apache-2.0 wrapper; uses LibRaw internally for RAW; large native payload); **rawspeed** (LGPL-2.1, C++ with no C API, would need a native shim); **Windows RAW codecs through WIC** (Microsoft's Raw Image Extension from the Store; not redistributable, so coverage depends on the user's machine); **Adobe DNG SDK** (DNG only, Adobe's license). **Justified default:** LibRaw through a maintained wrapper, because its license fits, its camera list is the widest open one, and it exposes both the demosaiced image and the embedded preview Lumen's thumbnails need. Cost of changing: one adapter class behind `IRawDecoder`. -> SOURCE: lumen-notes-raw

- [ ] Build the pinned corpus list `tests/fixtures/lumen/raw/corpus.json` (file URL on raw.pixls.us, SHA-256, camera, format; at least CR2, CR3, NEF, ARW, RAF, ORF, RW2, and DNG, 2 files each) and a `scripts/fetch-raw-corpus.ps1` that downloads it into `build/fixtures/raw/` with hash checks. Done when: the script fetches and verifies every file.
- [ ] For each candidate that can run on Windows, measure: files decoded out of the corpus, median decode time for a 24-megapixel file, embedded-preview extraction, installed size, and license with its text URL. Done when: `docs/dev/decisions.md` carries the table with every cell filled or marked "cannot run on Windows" with the reason.
- [ ] Decide and record the choice and its cost of change. Done when: the entry names the decoder.
- [ ] Commit: `"lumen: decide the RAW decoder with coverage, speed, and license evidence"`

**Test checkpoint:** `pwsh scripts/fetch-raw-corpus.ps1` exits 0 with every hash verified; `docs/dev/decisions.md` has the decoder entry with a measured row per candidate. Cheaper substitute that fails: picking a wrapper by popularity, which leaves the coverage column empty.

## 4. RAW Decode with Fidelity Fixtures

The decoder sits behind `IRawDecoder` in `Photon.Lumen.Core/Raw/`: open a file read-only, return metadata, the embedded preview, and the demosaiced linear image in float32 with its camera-to-XYZ matrix. It owes a format fidelity proof against a reference decode.

**Freeze check:** The decoder opens originals with `FileAccess.Read` and `FileShare.Read` only; a test decodes every corpus and committed fixture and asserts each file's SHA-256 and last-write time are unchanged afterward. Fixture source: `tests/fixtures/lumen/raw/` (one small committed DNG) and the pinned corpus.

- [ ] Add `IRawDecoder` and the chosen adapter, with cancellation and a per-file timeout. Done when: `RawDecoderTests` decode the committed DNG to its expected dimensions and matrix.
- [ ] Commit one small DNG fixture (under 5 MB, CC0 from raw.pixls.us, license recorded) so the fidelity proof runs on every clone. Done when: `tests/fixtures/lumen/raw/README.md` lists it with its source.
- [ ] `RawDecodeFidelityTests` (`[Trait("Category", "Fidelity")]`): decode each file and compare with LibRaw's `dcraw_emu -4 -T` output (version recorded) within a stated tolerance, running the corpus when `build/fixtures/raw/` exists and the committed DNG always. Done when: every file passes or names the section owning its gap.
- [ ] Unsupported or corrupt files return a typed failure ("Lumen cannot decode <name>: <camera> is not supported by <decoder> <version>") that import records without stopping. Done when: a truncated-file test passes.
- [ ] Commit: `"lumen: RAW decoding behind one interface with fidelity proofs"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` prints a result per decoded file (quote the list with the tolerance); the unchanged-originals test passes over every file. Cheaper substitute that fails: comparing only image dimensions.

## 5. The Catalog Database

The catalog is a user document: losing it loses every rating and edit. SQLite through `Microsoft.Data.Sqlite` (MIT; SQLite is public domain), one file, WAL mode, a versioned schema with forward-only migrations, and a backup before every migration. -> SOURCE: lumen-notes-library

- [ ] Add `Photon.Lumen.Core/Catalog/` with the schema (roots, folders, images with path relative to a root, file hash, capture time, camera, lens, dimensions, rating, flag, label; keywords; collections; edit stacks; a schema version table) and `CatalogMigrator`. Done when: `CatalogSchemaTests` create a fresh catalog and assert every table.
- [ ] Migrations are forward-only, each tested against a committed catalog of the previous version, with a backup copy taken first. Done when: a v1 to v2 test migration (a dummy column) passes on a fixture and the backup exists.
- [ ] Every write is transactional; a crash mid-transaction leaves the catalog opening at the previous state. Done when: a test kills a writer mid-transaction (a hook that throws) and reopens cleanly.
- [ ] The catalog location is a setting (`Lumen.Catalog.Path`), with File, New Catalog and Open Catalog. Done when: switching catalogs is tested.
- [ ] Commit: `"lumen: a transactional SQLite catalog with tested migrations"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `CatalogSchemaTests`, the migration test, and the interrupted-transaction test reporting. Cheaper substitute that fails: a JSON file per image.

## 6. Import

Import is where trust is won or lost: it must never touch an original, must say what it will do before it does it, and must survive a card pulled mid-copy. This section adds Lumen's original-file guard to the frozen set.

**Freeze check:** Import opens originals read-only; "Add" records paths without copying; "Copy" copies to the chosen folder through a temp name, verifies the copy's SHA-256 against the source, then renames, and only then records it; a failure mid-copy leaves the source untouched and no partial file in that folder; every original's hash and last-write time are unchanged after import. Fixture source: `tests/fixtures/lumen/import/` (a folder of small JPEGs and the DNG, with a nested folder and a duplicate).

**Fidelity:** Import dialog -- new build, no baseline; captured to docs/captures/lumen/import/.
**Job:** a photographer can bring a card or folder into the library by adding in place or copying, see how many files and how much space before starting, and keep working while it runs. Consumer: the catalog and the grid.
**Treatment:** an Import dialog with the source (folder picker, removable drives listed first), mode (Add or Copy), target folder and folder pattern for Copy (`yyyy/yyyy-MM-dd`), include subfolders, skip duplicates (by hash), and a preview count ("1,204 photos, 38.2 GB; 12 duplicates will be skipped"); import runs in the background with progress in the status strip, Cancel, and a completion summary (imported, skipped, failed with reasons). Cheaper substitute that fails the checkpoint: a synchronous import that freezes the window.
**Chrome:** consume the catalog, `IRawDecoder` for metadata, MetadataExtractor (Apache-2.0) for EXIF and XMP in JPEGs and RAWs (dependency recorded), and the theme.

**Requires:** display-session -- driving the import dialog needs an interactive desktop

- [ ] `ImportPlanner` (scan, hash, duplicate detection, counts) and `ImportRunner` (add or copy with verification, cancellation, per-file failure records). Done when: `ImportTests` cover add, copy, duplicate skip, a locked source file, a read-only target folder (refused by name), and cancel mid-copy leaving no partial file.
- [ ] Metadata extraction into the catalog (capture time, camera, lens, dimensions, existing XMP rating and keywords). Done when: tests assert extracted fields for fixtures.
- [ ] The dialog, background progress, and summary. Done when: a driven import of the fixture folder shows the summary (capture).
- [ ] The unchanged-originals test over the import fixtures. Done when: it passes.
- [ ] Add "Lumen original-file guard" to the frozen set in `todo/README.md`. Done when: the paragraph names it with this section's ref.
- [ ] Commit: `"lumen: safe import with verified copies and a dry-run count"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `ImportTests` and the unchanged-originals test reporting; a driven import of 1,000 generated JPEGs completes with progress and a summary (time quoted) and every source hash is unchanged. Cheaper substitute that fails: copy without verification, which the corrupted-copy test (a hook that flips a byte) catches.

## 7. Thumbnails and the Preview Cache

A library is only as fast as its thumbnails. RAW files carry embedded JPEG previews; using them makes a first view near-instant, with rendered previews replacing them after develop edits. -> SOURCE: lumen-notes-library-cache

- [ ] `PreviewCache` in `Photon.Lumen.Core/Previews/`: thumbnails (256 px long edge) and standard previews (2,048 px) as JPEG files under the app-data cache, keyed by image id and edit version, with a size limit (setting `Lumen.Cache.SizeMB`, default 2,048) and least-recently-used eviction. Done when: `PreviewCacheTests` cover hit, miss, invalidation by edit version, and eviction.
- [ ] Extract embedded previews from RAWs through `IRawDecoder`; generate from pixels when none exists. Done when: tests assert a thumbnail for the DNG and a JPEG fixture.
- [ ] A background builder after import, prioritizing visible images. Done when: a 1,000-image import shows thumbnails within 10 seconds of completion (quoted).
- [ ] Commit: `"lumen: a preview cache fed by embedded RAW previews"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `PreviewCacheTests` reporting; the 1,000-image timing is quoted. Cheaper substitute that fails: decoding full RAWs for thumbnails, which the timing catches.

## 8. The Library Grid

The grid is where a photographer spends most of their time. It must scroll 50,000 photos smoothly, sort and filter instantly, and be driven entirely from the keyboard. -> SOURCE: lumen-notes-library-grid

**Fidelity:** Lumen library grid -- docs/captures/lumen/main-window/ (the shell from §2).
**Job:** a photographer can browse, sort, filter, and select photos across the whole library. Consumer: the loupe, metadata edits, develop, and export.
**Treatment:** a virtualized grid (`VirtualizingWrapPanel` or a custom virtualizing panel) with adjustable thumbnail size, badges for rating, flag, label, and edited state; sort by capture time, import time, file name, rating; a filter bar (text, rating at least N, flag, label, camera, lens, date range, folder); multi-select with Shift and Ctrl; arrow keys move; the left panel lists folders and collections with counts. Cheaper substitute that fails the checkpoint: a `ListBox` of all images without virtualization.
**Chrome:** consume the preview cache, the theme, and the icon catalog.

**Requires:** display-session -- measuring grid scrolling needs an interactive desktop

- [ ] `LibraryViewModel` with sort, filter, and selection over catalog queries (indexed columns for each sort and filter). Done when: `LibraryViewModelTests` cover each filter against a seeded catalog.
- [ ] The virtualizing grid and badges. Done when: a capture shows badges.
- [ ] Measure scrolling a generated 50,000-image catalog (thumbnails from a small set, reused). Done when: median frame time under 16 ms and filter response under 200 ms (both quoted with the machine).
- [ ] Empty states: no photos match the filter ("No photos match these filters. Clear filters"), and an empty folder. Done when: both render.
- [ ] Commit: `"lumen: a virtualized library grid with sort and filters"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `LibraryViewModelTests` reporting; the 50,000-image measurements are quoted under budget. Cheaper substitute that fails: a non-virtualized list, which the frame-time budget catches.

## 9. Loupe, Compare, and Filmstrip

Culling needs a big view of one photo, a side-by-side compare, and a filmstrip to move through the selection. -> SOURCE: lumen-notes-library-loupe

**Fidelity:** Loupe and compare views -- new build, no baseline; captured to docs/captures/lumen/loupe/ and docs/captures/lumen/compare/.
**Job:** a photographer can view a photo large, zoom to 100 percent to check focus, compare two candidates, and move through photos with the keyboard. Consumer: culling (ratings and flags from §11).
**Treatment:** E opens the loupe with the standard preview, Z toggles 100 percent at the clicked point (decoded on demand), C compares two selected photos with synchronized zoom, arrow keys move through the filmstrip at the bottom, G returns to the grid. Cheaper substitute that fails the checkpoint: opening the file in an external viewer.
**Chrome:** consume the preview cache, the decoder for 100 percent views, and the keymap pattern.

**Requires:** display-session -- the loupe needs an interactive desktop

- [ ] Loupe with fit and 100 percent zoom. Done when: 100 percent on the DNG shows full resolution within 1 second (quoted).
- [ ] Compare view with synchronized zoom and pan, and the filmstrip. Done when: a driven compare is captured.
- [ ] Commit: `"lumen: loupe, compare, and filmstrip views"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with a view-model test for navigation; the 100 percent timing is quoted and captures committed. Cheaper substitute that fails: an external viewer.

## 10. Keywords, Collections, and Smart Collections

Finding photos later depends on keywords and collections; smart collections save a filter so it stays current. -> SOURCE: lumen-notes-library-collections

**Fidelity:** Keywords panel and collections list -- new build, no baseline; captured to docs/captures/lumen/keywords/ and docs/captures/lumen/collections/.
**Job:** a photographer can tag photos with keywords, group them in collections, and save filters as smart collections that update themselves. Consumer: the grid's filters and the export batch.
**Treatment:** a keyword panel with autocomplete and a hierarchy (`Places > France > Paris`); collections (manual, drag photos in) and smart collections (a saved filter-bar state with rules joined by all or any); counts per collection and a library statistics summary (photos per year, per camera, rated share) in the left panel's header menu; every change undoable. Cheaper substitute that fails the checkpoint: keywords as free text in a comment field.
**Chrome:** consume the catalog, the filter bar from §8, and the history.

**Requires:** display-session -- the panels need an interactive desktop

- [ ] Keyword hierarchy and assignment with undo. Done when: tests cover assign, remove, rename a keyword across photos, and undo.
- [ ] Collections and smart collections. Done when: a smart collection "rated 4 or more, 2026" updates when a rating changes (test).
- [ ] Library statistics. Done when: a seeded catalog reports expected counts.
- [ ] Commit: `"lumen: keywords, collections, smart collections, and statistics"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the keyword, collection, and statistics tests reporting; a driven session is captured. Cheaper substitute that fails: static collections only.

## 11. Ratings, Flags, Labels, and XMP Sidecars

Culling is ratings (0 to 5), flags (pick, reject, none), and color labels, set from the keyboard with auto-advance, stored in the catalog, and optionally written to `.xmp` sidecars so other tools see them. Sidecars sit beside originals and never replace them. -> SOURCE: lumen-notes-library-metadata

**Freeze check:** Metadata changes write only the catalog and, when `Lumen.Metadata.WriteSidecars` is on, `<name>.xmp` beside the original through an atomic write; the original's bytes and last-write time are unchanged; an existing sidecar from another tool is read, merged (Lumen's fields updated, unknown fields preserved), and written back atomically. Fixture source: `tests/fixtures/lumen/xmp/` (a JPEG and the DNG with darktable- and Lightroom-style sidecars).

**Fidelity:** Grid and loupe with the metadata panel -- docs/captures/lumen/main-window/.
**Job:** a photographer can cull fast from the keyboard and have ratings and keywords readable by other tools. Consumer: the grid filters, smart collections, and other applications reading XMP.
**Treatment:** 0-5 set rating, P, X, U set flags, 6-9 set labels, with auto-advance (Caps Lock or a setting), each an undo step logged; Metadata, Write to Sidecars and Read from Sidecars, plus the automatic setting (default off, stated on first use). Cheaper substitute that fails the checkpoint: writing XMP into the original JPEG.
**Chrome:** consume the catalog, the history, `AtomicFileWriter`, and an XMP writer (a small writer over `System.Xml`, or a recorded library decision).

**Requires:** display-session -- keyboard culling needs an interactive desktop

- [ ] Rating, flag, and label commands with undo and auto-advance. Done when: `CullingTests` cover each key and undo.
- [ ] `XmpSidecar` read, merge, and atomic write with the `xmp`, `dc`, and `lr` (hierarchical subject) namespaces darktable and Lightroom use. Done when: round-trip tests keep unknown fields byte-for-byte and darktable reads Lumen's rating back (driven, version quoted).
- [ ] The unchanged-originals test over the xmp fixtures. Done when: it passes.
- [ ] Commit: `"lumen: keyboard culling and safe XMP sidecars"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `CullingTests` and the sidecar tests reporting; the unchanged-originals assertion passes; darktable shows a rating Lumen wrote (capture). Cheaper substitute that fails: embedding XMP in originals, which the unchanged-originals test catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` passes every RAW fixture
- [ ] The unchanged-originals tests of §4, §6, and §11 pass
- [ ] The 50,000-image grid budget is quoted
- [ ] `python scripts/todo-graph.py validate` clean
