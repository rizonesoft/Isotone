---
schema_version: 1
id: albumen-foundation
domain: 04-albumen
status: draft
title: "TODO-01 -- Albumen: App Spine, Library, and RAW Decode"
depends_on: []
frozen: true
track: L1
---

# TODO-01 -- Albumen: App Spine, Library, and RAW Decode

> **Goal:** Albumen exists as the suite's third standalone app: it builds, installs, and starts like Stilus and Gesso; it imports a folder of photos into a SQLite catalog without ever writing an original (the guard is safe by default: an original is written only when the user later opts in through `D04 T11 §1`, which this file never does); it decodes camera RAW through a library chosen by recorded decision; and it shows the library as a fast, sortable, filterable grid with a loupe view, ratings, flags, color labels, keywords, and collections, with metadata optionally mirrored to XMP sidecars.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Albumen has no code. `src/Albumen.UI/TODO.md`, the only file it had, was a list of intentions (RAW formats CR2, NEF, ARW, DNG; exposure, white balance, curves; batch; collections and smart collections; "send to Gesso") naming no library, database, or metadata choice; it was mined into this file and removed on 2026-09-26. `scripts/apps.psd1` declares Albumen with `Project = 'src/Albumen/Albumen.UI/Albumen.UI.csproj'` and `Shipping = $false`, and `installer/Albumen.iss` refuses to compile unless `/DAlbumenShipping` is defined. `resources/icons/lens.png` (512 by 512, an aperture illustration) is the candidate icon art. **Corrected 2026-09-27:** the operator chose project-created SVG icons that day (Direction C, `resources/icons/README.md`): Albumen's is the aperture in viewfinder brackets in green, `resources/icons/albumen/albumen.svg` with hand-tuned `albumen-16.svg`, `-24.svg`, `-32.svg`, and `albumen-splash.svg` (**Corrected 2026-09-27:** said the neon art; it is now the Suite card splash reference design, 640 by 360, operator decision the same day), licensed GPL-3.0 with the repository. `lens.png` was removed the same day, and `D00 T03 §3` (Phase 1) generates `resources/icons/albumen/albumen.ico` and `PNG/albumen_*.png`, the ICO `installer/Albumen.iss` already names. `standards/albumen.md` states the contract: originals are never written, the catalog is SQLite with forward-only migrations, the develop pipeline is float32 linear-light. **Corrected 2026-09-28:** the removed notes file was `src/Lumen.UI/TODO.md` (its pre-rename path; `git show cf22f5c^:src/Lumen.UI/TODO.md`), whose wording was "send to Imago, export to Nodus" (the Stilus half is `D04 T14 §9`'s Send to Stilus); and the standard now reads "never written unless the user opts in" (`D04 T11 §1`), while this file builds no opt-in.
<!-- claim: absent src/Albumen -->
<!-- claim: count "Shipping  = \$false" scripts/apps.psd1 = 1 -->
<!-- claim: count "AlbumenShipping" installer/Albumen.iss = 3 -->
<!-- claim: absent resources/icons/lens.png -->
<!-- claim: exists resources/icons/albumen/albumen.svg -->
<!-- claim: exists standards/albumen.md -->

## Inputs

- [`standards/albumen.md`](../../standards/albumen.md) -- the original-file guard, the catalog, the pipeline, the decoder rules
- [`standards/shared.md`](../../standards/shared.md) -- the stack, the design contract, performance budgets
- [`docs/dev/architecture.md`](../../docs/dev/architecture.md) -- `src/Albumen/Isotone.Albumen.Core` and `Isotone.Albumen.Desktop`, and the rule that Albumen never needs Gesso at runtime
- [`.claude/skills/plan-new-feature/SKILL.md`](../../.claude/skills/plan-new-feature/SKILL.md) -- the rigor this file was planned with; §1 completes its competitor step with driven runs
- raw.pixls.us (https://raw.pixls.us/) -- CC0 RAW samples per camera, the source of the pinned decode corpus
- -> XREF: D04 T02 §1 -- the edit stack that stores develop settings in §5's catalog
- -> XREF: D03 T07 §11 -- moves §4's decoder adapter to `Isotone.Core` when Gesso imports RAW
- -> XREF: D05 T01 §6 -- the suite bundle that ships Albumen beside Stilus and Gesso
- -> XREF: D00 T03 §3 -- the app icon raster export (`resources/icons/albumen/albumen.ico` and `PNG/albumen_*.png` §2 wires in, including the `albumen_256.png` the shared Suite card splash shows; the `albumen_splash_*.png` renders are marketing only)
- -> XREF: D01 T07 §1 -- the suite develop engine cites §4: the RAW decoder supplies linear camera RGB and its matrix through D01 T07 §1's `IDevelopSource`; §11: Albumen's XMP sidecars consume D01 T07 §6's XMP core
- -> XREF: D03 T17 §10 -- Gesso parity formats cites §11: Albumen's sidecars consume D03 T17 §10's EXIF and IPTC code
- -> XREF: D04 T04 §2 -- the Albumen Viewer cites §4: the RAW decoder and embedded previews D04 T04 §2 consumes; §8: the library grid D04 T04 §1 opens photos from and the `T` key filters until browse mode ships; §11: the XMP sidecars D04 T04 §9 and D04 T04 §16 write ratings and orientation into
- -> XREF: D04 T05 §1 -- Albumen browse without importing cites §5: the catalog D04 T05 §1 adds its origin column and browse-folder table to; §7: the preview cache D04 T05 §2 feeds and D04 T05 §4 reads; §8: the library grid whose views, badges, and sort D04 T05 §4 and D04 T05 §5 extend; §9: compare, which D04 T05 §7 extends to four images; §11: sidecars that travel in D04 T05 §6
- -> XREF: D04 T06 §10 -- Albumen parity library cites §5: the catalog every section migrates forward; §7: the preview cache D04 T06 §10 manages and D04 T06 §11 extends; §8: the grid, sort, and filter bar D04 T06 §1 and D04 T06 §4 extend; §9: the loupe, compare, and filmstrip D04 T06 §1 extends; §10: keywords, collections, smart collections, and statistics D04 T06 §5 and D04 T06 §12 extend; §11: culling keys, auto advance, and the XMP sidecar D04 T06 §2 extends
- -> XREF: D04 T07 §2 -- Albumen parity import cites §6: the import planner and runner every section extends, and the Freeze check this file keeps; §7: previews built on import (D04 T07 §2)
- -> XREF: D04 T08 §1 -- Albumen parity metadata cites §6: metadata read on import, which D04 T08 §1 widens; §8: the grid badges D04 T08 §1's status badge and D04 T08 §8's pending overlay join; §10: the keyword hierarchy D04 T08 §5 extends; §11: the `XmpSidecar` writer D04 T08 §8 extends into the one metadata writer
- -> XREF: D04 T09 §1 -- Albumen parity develop cites §9: loupe, zoom, and filmstrip, which D04 T09 §1 extends; §11: XMP sidecars and their automatic-write setting, which D04 T09 §17 mirrors develop settings through
- -> XREF: D04 T10 §6 -- Albumen AI cites §6: import, which D04 T10 §6 and D04 T10 §12 hook for analysis and face-data import; §10: the keyword hierarchy person keywords join (D04 T10 §3); §11: culling commands D04 T10 §6 applies
- -> XREF: D04 T11 §1 -- the Albumen batch tools cites §7: previews and the preview cache D04 T11 §1's idle jobs and D04 T11 §4's thumbnail export read; §11: sidecars D04 T11 §3 renames and D04 T11 §5's orientation writes
- -> XREF: D04 T12 §3 -- Albumen parity output cites §10: the collections D04 T12 §3 publishes and D04 T12 §7, D04 T12 §10 save as slideshow and book collections
- -> XREF: D04 T13 §5 -- Albumen parity formats cites §4: the RAW decoder D04 T13 §5 extends and D04 T13 §7 writes DNG from; §6: the import dialog that offers D04 T13 §5's RAW+JPEG pair choice
- -> XREF: D01 T01 §8 -- the shared window chrome (with `D01 T01 §7`'s `IsotoneWindow`), document tabs, dock theme, and status bar §2's shell is built on
- -> XREF: D04 T14 §1 -- Albumen parity workspace cites §2: the shell, splash, and About D04 T14 §1 and D04 T14 §7 extend; §7: the preview cache D04 T14 §5 sizes and purges

## Job and non-goals

**Job:** a photographer with thousands of RAW and JPEG files on disk wants to bring them into one place, find the good ones fast (by date, rating, flag, label, keyword, camera, lens, or folder), and develop them without ever risking the originals. Done, to them, means: point Albumen at a card or a folder, see thumbnails within seconds, cull with the keyboard, and trust that nothing on disk changed except what they explicitly exported.

**Audience:** enthusiast and working photographers who today use Lightroom Classic, darktable, or a file browser plus an editor.

**Non-goals for this file:** tethered capture; cloud sync; face recognition; maps and GPS editing; printing, books, and slideshows; video; plugins. None is a promise of this file. Since the Albumen parity decision of 2026-09-27: tethered capture is backlog B-048 (watched-folder auto import, `D04 T07 §5`, covers the workflow); face detection and naming (`D04 T10 §2`, `§3`; face recognition is backlog B-052 since the operator's decision of 2026-09-27), maps and GPS editing (`D04 T08 §6`, `§7`), and printing, books, and slideshows (`D04 T12`) are planned Albumen parity sections; cloud sync stays excluded; video is `D04 T16`; third-party filter plug-ins run on the suite plug-in host (`D01 T09`, consumed by `D04 T04 §15` and `D04 T11 §7`) and scripting and recorded actions are `D04 T17` on `D01 T10`.

**Working name and one-line purpose:** Albumen, "the darkroom and library for your photos" (quoted by the About dialog, the installer, and the user guide).

**Home:** its own app. What it shares goes through `Isotone.Core` and `Isotone.UI` only where Stilus or Gesso already need the same thing (logging, settings, single instance, theme, dialogs).

## Competitor survey

From documentation, to be confirmed and extended by driven runs in §1 (each row then names the version driven):

| Capability | Lightroom Classic (Adobe docs) | darktable (docs, 5.x) | What Albumen does, and what beats them |
| ---------- | ------------------------------ | --------------------- | ------------------------------------ |
| Import | Add, copy, move; build previews; duplicate detection | Add to library or copy and import; film rolls | Add or copy with hash-verified copies and a dry-run count before anything moves |
| Catalog | SQLite catalog, previews cache beside it | SQLite library, XMP sidecar per image by default | SQLite catalog plus optional sidecars; catalog backup before every migration |
| Culling | Grid and loupe, P/X/U flags, 0-5 stars, color labels | Lighttable, stars, reject, color labels | The same keys, plus auto-advance and a compare view, with every action undoable |
| Search | Library filter bar, smart collections | Collections module, tagging | One filter bar over metadata, saved as smart collections |
| RAW decode | Adobe Camera Raw engine | rawspeed plus LibRaw fallback | LibRaw-class decoding (decided in §3) with a pinned-corpus coverage table |
| Metadata safety | Writes XMP to sidecars only when asked; DNG can be written in place | Sidecars always | Never writes an original, proven by a test over every fixture |
| Weakness to beat | Slow on large catalogs; subscription | Steep learning curve; dense UI | Fast grid at 50,000 photos, a plain UI, free and open source |

## Outcome

- `src/Albumen/Isotone.Albumen.Core`, `src/Albumen/Isotone.Albumen.Desktop` (`Albumen.exe`), and `tests/Isotone.Albumen.Tests` build in `Isotone.slnx`; `scripts/apps.psd1` marks Albumen shipping and `installer/Albumen.iss` compiles without the guard.
- `docs/dev/decisions.md` records the RAW decoder choice with licenses, coverage on a pinned corpus, and speed.
- Import adds or copies folders into the catalog, hash-verifies copies, skips duplicates, reads EXIF and XMP, and writes nothing into any original.
- The grid shows 50,000 photos with scrolling under 16 ms per frame from cached thumbnails; the loupe shows full previews with a filmstrip.
- Ratings, flags, labels, keywords, and collections are stored in the catalog, undoable, searchable, and optionally mirrored to `.xmp` sidecars.
- `todo/README.md` lists Albumen's original-file guard in the frozen set.

**Adjacency:** list=applicable @ D04 T01 §8; document=not-applicable (contact sheets and prints are the Albumen parity sections D04 T12 §4 to §6); settings=applicable @ D04 T01 §2; reporting=applicable @ D04 T01 §10; notifications=applicable @ D04 T01 §6; permissions=applicable @ D04 T01 §6; audit=applicable @ D04 T01 §11; exchange=applicable; reverse=applicable

**Adjacency rationale:** The grid is the list; import progress and its completion summary are the notifications; a read-only card or an unreadable file is the refusal case; library statistics per collection are reporting; every metadata change logs, undoes, and exchanges through XMP sidecars.

## Implementation Order

| Order | Section | Deliverable                                              | Depends On                     | Status |
| :---: | :-----: | -------------------------------------------------------- | ------------------------------ | :----: |
|   1   |   §1    | The competitor survey, driven                            | --                             |  [ ]   |
|   2   |   §2    | Create the Albumen app                                     | D01 T01 §3, D01 T02 §3, D00 T03 §3, D01 T01 §8 |  [ ]   |
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

- [ ] Install darktable's current Windows release, import the pinned sample folder (§4's corpus subset, 50 files), and record import speed, thumbnail time, culling keys, filter options, metadata written to disk (hash every original before and after), and XMP sidecar behavior. Done when: `docs/dev/albumen/competitor-survey.md` has a darktable section naming the version and each measurement.
- [ ] Record Lightroom Classic's equivalent behaviors from Adobe's help pages (URL per claim), marked "from documentation, not driven". Done when: every row cites a URL.
- [ ] Revise this file's competitor table, and any section whose Treatment the survey contradicts, in the same commit. Done when: the table names versions and every "beats" claim has a measurement or a cited source.
- [ ] Commit: `"albumen: drive the competitor survey and correct the plan"`

**Requires:** display-session -- driving darktable's user interface needs an interactive desktop

**Test checkpoint:** `docs/dev/albumen/competitor-survey.md` exists with darktable's version, a before-and-after hash table of the 50 originals (all unchanged or the difference named), and a URL per Lightroom claim. Cheaper substitute that fails: a table from memory, which carries no version and no hashes.

## 2. Create the Albumen App

Albumen needs the same spine as the other two: projects in the suite layout, a composition root on `Isotone.Core` logging and settings, single instance, the `Isotone.UI` theme, splash, and exception window, an About dialog, and a working publish and installer. It ships nothing useful yet; it proves Albumen builds, installs, and starts. -> SOURCE: albumen-notes-structure

**Fidelity:** Albumen main window shell -- new build, no baseline; follows the window anatomy in `docs/design/shell-layout.md` (**Corrected 2026-09-27:** said `standards/shared.md`) and is captured to docs/captures/albumen/main-window/.
**Design:** docs/design/components/WindowChrome/README.md, docs/design/components/Menu/README.md, docs/design/shell-layout.md#albumen-darkroom-and-photo-manager, docs/design/shell-layout.md#regions, docs/design/shell-layout.md#splash-and-home, docs/design/components/Splash/README.md, docs/design/components/Button/README.md, docs/design/components/StatusBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/Icons/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can install Albumen, start it, and see an empty library with an Import button. Consumer: every later Albumen section.
**Treatment:** a main window with the module switcher (Library, Develop) at the top, a left panel (folders, collections), the center grid area with the empty state "Your library is empty. Import a folder of photos to begin." and an Import button, a right panel (metadata), and a status strip; Help, About Albumen through `Isotone.UI`. Cheaper substitute that fails the checkpoint: a blank window.
**Chrome:** consume `Isotone.UI` (theme, splash, exception window, About and shortcuts dialogs, icon catalog) and `Isotone.Core` (logging, settings, single instance). Do not copy any of them.
**Corrected 2026-09-27:** the specs are `docs/design/shell-layout.md` (Albumen: Library and Develop as tabs in the title bar area after the menus, left dock, filmstrip, Home), `docs/design/components/WindowChrome/README.md`, and `docs/design/components/StatusBar/README.md`; the Import button is the view's one primary button in `accent-albumen`.
**Corrected 2026-09-27:** the shell window is `D01 T01 §7`'s `IsotoneWindow` (the Albumen mark, the menu bar in the title bar, Snap Layouts) with the Library and Develop tabs after the menus in its title bar, docked panels on `D01 T01 §8`'s AvalonDock theme, and the status strip as `IsotoneStatusBar`; every control uses the implicit styles of `D01 T01 §5` and `D01 T01 §6`.

**Requires:** display-session -- launching the new app needs an interactive desktop

- [ ] Create `src/Albumen/Isotone.Albumen.Core/Isotone.Albumen.Core.csproj` (`net11.0`), `src/Albumen/Isotone.Albumen.Desktop/Isotone.Albumen.Desktop.csproj` (`net11.0-windows10.0.26100.0` with `TargetPlatformMinVersion` 10.0.17763.0, WPF; **Corrected 2026-09-26:** said `net10.0` and `net10.0-windows`, the suite moved to .NET 11, `AssemblyName` Albumen), `src/Albumen/Directory.Build.props` (MinVer prefix `albumen-v`, `Product` Albumen), and `tests/Isotone.Albumen.Tests`, all in `Isotone.slnx`. Done when: `dotnet build Isotone.slnx -c Release` builds them.
- [ ] The composition root with `UseIsotoneLogging("Albumen")`, the settings store, and single instance. Done when: a launch logs its startup line to `%LOCALAPPDATA%\Rizonesoft\Albumen\logs\`.
- [ ] The shell window and empty state per Treatment. Done when: a capture is committed.
- [ ] The Albumen icon from `resources/icons/lens.png` into `resources/icons/albumen/` (sizes as for Stilus), with its source and license status recorded in `resources/icons/README.md` pending operator confirmation (`D99 T01 §4`) (**Corrected 2026-09-27:** `lens.png` is gone; the icon is the generated `resources/icons/albumen/albumen.ico` and `PNG/albumen_32.png` from `D00 T03 §3`, and the README already records its source and GPL-3.0 license, so this item sets `ApplicationIcon` to that ICO (linked, not copied) and the window icon to that PNG, and renders or re-exports nothing). Done when: `Albumen.exe` shows it.
- [ ] Set `Project` to `src/Albumen/Isotone.Albumen.Desktop/Isotone.Albumen.Desktop.csproj` and `Shipping = $true` in `scripts/apps.psd1`, and remove the `/DAlbumenShipping` guard from `installer/Albumen.iss`. Done when: `pwsh scripts/package.ps1 -App Albumen -Version 0.0.1-dev` produces an installer and a ZIP.
- [ ] Update `AGENTS.md`, `docs/dev/architecture.md`, and `docs/dev/build.md` to show Albumen as existing. Done when: no file says Albumen has no code.
- [ ] Write HKCU (HKLM for all-users) `App Paths\Albumen.exe` in `installer/Albumen.iss`, removed on uninstall, so `SuiteAppLocator` finds Albumen (**Groomed 2026-09-28:** Gesso's installer writes its entry and Albumen's did not). Done when: `reg query` shows the entry after install and none after uninstall.
- [ ] Commit: `"albumen: create the app on the suite spine"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with a `AlbumenServiceRegistrationTests` class reporting; the packaged installer installs silently and `Albumen.exe` starts to the empty state (capture) with 0 `[ERR]` lines in its log. Cheaper substitute that fails: a project that builds but is not packaged.

## 3. The RAW Decoder Decision

The decoder is Albumen's most consequential dependency: it sets camera coverage, color quality, speed, and license. Candidates, with the facts this section must verify: **LibRaw** (dual-licensed LGPL-2.1 or CDDL-1.0; LGPL-2.1 combines with GPL-3.0) through a .NET wrapper such as Sdcb.LibRaw (check its license and its bundled LibRaw version); **Magick.NET** (Apache-2.0 wrapper; uses LibRaw internally for RAW; large native payload); **rawspeed** (LGPL-2.1, C++ with no C API, would need a native shim); **Windows RAW codecs through WIC** (Microsoft's Raw Image Extension from the Store; not redistributable, so coverage depends on the user's machine); **Adobe DNG SDK** (DNG only, Adobe's license). **Justified default:** LibRaw through a maintained wrapper, because its license fits, its camera list is the widest open one, and it exposes both the demosaiced image and the embedded preview Albumen's thumbnails need. Cost of changing: one adapter class behind `IRawDecoder`. -> SOURCE: albumen-notes-raw

- [ ] Build the pinned corpus list `tests/fixtures/albumen/raw/corpus.json` (file URL on raw.pixls.us, SHA-256, camera, format; at least CR2, CR3, NEF, ARW, RAF, ORF, RW2, and DNG, 2 files each) and a `scripts/fetch-raw-corpus.ps1` that downloads it into `build/fixtures/raw/` with hash checks. Done when: the script fetches and verifies every file.
- [ ] For each candidate that can run on Windows, measure: files decoded out of the corpus, median decode time for a 24-megapixel file, embedded-preview extraction, installed size, and license with its text URL. Done when: `docs/dev/decisions.md` carries the table with every cell filled or marked "cannot run on Windows" with the reason.
- [ ] Decide and record the choice and its cost of change. Done when: the entry names the decoder.
- [ ] Commit: `"albumen: decide the RAW decoder with coverage, speed, and license evidence"`

**Test checkpoint:** `pwsh scripts/fetch-raw-corpus.ps1` exits 0 with every hash verified; `docs/dev/decisions.md` has the decoder entry with a measured row per candidate. Cheaper substitute that fails: picking a wrapper by popularity, which leaves the coverage column empty.

## 4. RAW Decode with Fidelity Fixtures

The decoder sits behind `IRawDecoder` in `Isotone.Albumen.Core/Raw/`: open a file read-only, return metadata, the embedded preview, and the demosaiced linear image in float32 with its camera-to-XYZ matrix. It owes a format fidelity proof against a reference decode.

**Freeze check:** The decoder opens originals with `FileAccess.Read` and `FileShare.Read` only; a test decodes every corpus and committed fixture and asserts each file's SHA-256 and last-write time are unchanged afterward. Fixture source: `tests/fixtures/albumen/raw/` (one small committed DNG) and the pinned corpus.

- [ ] Add `IRawDecoder` and the chosen adapter, with cancellation and a per-file timeout. Done when: `RawDecoderTests` decode the committed DNG to its expected dimensions and matrix.
- [ ] Commit one small DNG fixture (under 5 MB, CC0 from raw.pixls.us, license recorded) so the fidelity proof runs on every clone. Done when: `tests/fixtures/albumen/raw/README.md` lists it with its source.
- [ ] `RawDecodeFidelityTests` (`[Trait("Category", "Fidelity")]`): decode each file and compare with LibRaw's `dcraw_emu -4 -T` output (version recorded) within a stated tolerance, running the corpus when `build/fixtures/raw/` exists and the committed DNG always. Done when: every file passes or names the section owning its gap.
- [ ] Unsupported or corrupt files return a typed failure ("Albumen cannot decode <name>: <camera> is not supported by <decoder> <version>") that import records without stopping. Done when: a truncated-file test passes.
- [ ] Commit: `"albumen: RAW decoding behind one interface with fidelity proofs"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` prints a result per decoded file (quote the list with the tolerance); the unchanged-originals test passes over every file. Cheaper substitute that fails: comparing only image dimensions.

## 5. The Catalog Database

The catalog is a user document: losing it loses every rating and edit. SQLite through `Microsoft.Data.Sqlite` (MIT; SQLite is public domain), one file, WAL mode, a versioned schema with forward-only migrations, and a backup before every migration. -> SOURCE: albumen-notes-library

- [ ] Add `Isotone.Albumen.Core/Catalog/` with the schema (roots, folders, images with path relative to a root, file hash, capture time, camera, lens, dimensions, rating, flag, label; keywords; collections; edit stacks; a schema version table) and `CatalogMigrator`. Done when: `CatalogSchemaTests` create a fresh catalog and assert every table.
- [ ] Migrations are forward-only, each tested against a committed catalog of the previous version, with a backup copy taken first. Done when: a v1 to v2 test migration (a dummy column) passes on a fixture and the backup exists.
- [ ] Every write is transactional; a crash mid-transaction leaves the catalog opening at the previous state. Done when: a test kills a writer mid-transaction (a hook that throws) and reopens cleanly.
- [ ] The catalog location is a setting (`Albumen.Catalog.Path`), with File, New Catalog and Open Catalog. Done when: switching catalogs is tested.
- [ ] Commit: `"albumen: a transactional SQLite catalog with tested migrations"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `CatalogSchemaTests`, the migration test, and the interrupted-transaction test reporting. Cheaper substitute that fails: a JSON file per image.

## 6. Import

Import is where trust is won or lost: it must never touch an original, must say what it will do before it does it, and must survive a card pulled mid-copy. This section adds Albumen's original-file guard to the frozen set.

**Corrected 2026-09-27:** the original-file guard this section adds to the frozen set is the one `standards/albumen.md` states after the operator's 2026-09-27 decision ("Safe by default, opt-in writes"): Albumen never writes an original unless the user opts in, and then only through `D04 T11 §1`'s `InPlaceWriter` after a verified backup. This section builds no opt-in, so its freeze check holds unchanged, read as "with every `Albumen.Originals.*` opt-in at its default"; import's opt-in embedding into verified copies is `D04 T07 §3` over `D04 T08 §9`.

**Freeze check:** Import opens originals read-only; "Add" records paths without copying; "Copy" copies to the chosen folder through a temp name, verifies the copy's SHA-256 against the source, then renames, and only then records it; a failure mid-copy leaves the source untouched and no partial file in that folder; every original's hash and last-write time are unchanged after import. Fixture source: `tests/fixtures/albumen/import/` (a folder of small JPEGs and the DNG, with a nested folder and a duplicate).

**Fidelity:** Import dialog -- new build, no baseline; captured to docs/captures/albumen/import/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Progress/README.md, docs/design/components/Toast/README.md, docs/design/components/Button/README.md, docs/design/components/RadioButton/README.md, docs/design/components/Checkbox/README.md, new surface: docs/design/components/AlbumenImport/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can bring a card or folder into the library by adding in place or copying, see how many files and how much space before starting, and keep working while it runs. Consumer: the catalog and the grid.
**Treatment:** an Import dialog with the source (folder picker, removable drives listed first), mode (Add or Copy), target folder and folder pattern for Copy (`yyyy/yyyy-MM-dd`), include subfolders, skip duplicates (by hash), and a preview count ("1,204 photos, 38.2 GB; 12 duplicates will be skipped"); import runs in the background with progress in the status strip, Cancel, and a completion summary (imported, skipped, failed with reasons). Cheaper substitute that fails the checkpoint: a synchronous import that freezes the window.
**Chrome:** consume the catalog, `IRawDecoder` for metadata, MetadataExtractor (Apache-2.0) for EXIF and XMP in JPEGs and RAWs (dependency recorded), and the theme.

**Requires:** display-session -- driving the import dialog needs an interactive desktop

- [ ] Write the design spec `docs/design/components/AlbumenImport/README.md` and `preview.html` (the import window: sources, add or copy mode, the dry-run counts, background progress, and the summary; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] `ImportPlanner` (scan, hash, duplicate detection, counts) and `ImportRunner` (add or copy with verification, cancellation, per-file failure records). Done when: `ImportTests` cover add, copy, duplicate skip, a locked source file, a read-only target folder (refused by name), and cancel mid-copy leaving no partial file.
- [ ] Metadata extraction into the catalog (capture time, camera, lens, dimensions, existing XMP rating and keywords). Done when: tests assert extracted fields for fixtures.
- [ ] The dialog, background progress, and summary. Done when: a driven import of the fixture folder shows the summary (capture).
- [ ] The unchanged-originals test over the import fixtures. Done when: it passes.
- [ ] Add "Albumen original-file guard" to the frozen set in `todo/README.md`. Done when: the paragraph names it with this section's ref.
- [ ] Commit: `"albumen: safe import with verified copies and a dry-run count"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `ImportTests` and the unchanged-originals test reporting; a driven import of 1,000 generated JPEGs completes with progress and a summary (time quoted) and every source hash is unchanged. Cheaper substitute that fails: copy without verification, which the corrupted-copy test (a hook that flips a byte) catches.

## 7. Thumbnails and the Preview Cache

A library is only as fast as its thumbnails. RAW files carry embedded JPEG previews; using them makes a first view near-instant, with rendered previews replacing them after develop edits. -> SOURCE: albumen-notes-library-cache

- [ ] `PreviewCache` in `Isotone.Albumen.Core/Previews/`: thumbnails (256 px long edge) and standard previews (2,048 px) as JPEG files under the app-data cache, keyed by image id and edit version, with a size limit (setting `Albumen.Cache.SizeMB`, default 2,048) and least-recently-used eviction. Done when: `PreviewCacheTests` cover hit, miss, invalidation by edit version, and eviction.
- [ ] Extract embedded previews from RAWs through `IRawDecoder`; generate from pixels when none exists. Done when: tests assert a thumbnail for the DNG and a JPEG fixture.
- [ ] A background builder after import, prioritizing visible images. Done when: a 1,000-image import shows thumbnails within 10 seconds of completion (quoted).
- [ ] Commit: `"albumen: a preview cache fed by embedded RAW previews"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `PreviewCacheTests` reporting; the 1,000-image timing is quoted. Cheaper substitute that fails: decoding full RAWs for thumbnails, which the timing catches.

## 8. The Library Grid

The grid is where a photographer spends most of their time. It must scroll 50,000 photos smoothly, sort and filter instantly, and be driven entirely from the keyboard. -> SOURCE: albumen-notes-library-grid

**Fidelity:** Albumen library grid -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/library-grid/. **Corrected 2026-09-27:** cited docs/captures/albumen/main-window/ (the shell from §2) as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/shell-layout.md#albumen-darkroom-and-photo-manager, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Slider/README.md, docs/design/components/Icons/README.md, new surface: docs/design/components/AlbumenGrid/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can browse, sort, filter, and select photos across the whole library. Consumer: the loupe, metadata edits, develop, and export.
**Treatment:** a virtualized grid (`VirtualizingWrapPanel` or a custom virtualizing panel) with adjustable thumbnail size, badges for rating, flag, label, and edited state; sort by capture time, import time, file name, rating; a filter bar (text, rating at least N, flag, label, camera, lens, date range, folder); multi-select with Shift and Ctrl; arrow keys move; the left panel lists folders and collections with counts. Cheaper substitute that fails the checkpoint: a `ListBox` of all images without virtualization.
**Chrome:** consume the preview cache, the theme, and the icon catalog.

**Requires:** display-session -- measuring grid scrolling needs an interactive desktop

- [ ] Write the design spec `docs/design/components/AlbumenGrid/README.md` and `preview.html` (the thumbnail grid: cells, rating, flag, label, edited and stack badges, selection, thumbnail size, the filter bar, and the empty states; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] `LibraryViewModel` with sort, filter, and selection over catalog queries (indexed columns for each sort and filter). Done when: `LibraryViewModelTests` cover each filter against a seeded catalog.
- [ ] The virtualizing grid and badges. Done when: a capture shows badges.
- [ ] Measure scrolling a generated 50,000-image catalog (thumbnails from a small set, reused). Done when: median frame time under 16 ms and filter response under 200 ms (both quoted with the machine).
- [ ] Empty states: no photos match the filter ("No photos match these filters. Clear filters"), and an empty folder. Done when: both render.
- [ ] Commit: `"albumen: a virtualized library grid with sort and filters"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `LibraryViewModelTests` reporting; the 50,000-image measurements are quoted under budget. Cheaper substitute that fails: a non-virtualized list, which the frame-time budget catches.

## 9. Loupe, Compare, and Filmstrip

Culling needs a big view of one photo, a side-by-side compare, and a filmstrip to move through the selection. -> SOURCE: albumen-notes-library-loupe

**Fidelity:** Loupe and compare views -- new build, no baseline; captured to docs/captures/albumen/loupe/ and docs/captures/albumen/compare/.
**Design:** docs/design/shell-layout.md#albumen-darkroom-and-photo-manager, docs/design/components/Canvas/README.md, new surface: docs/design/components/AlbumenLoupe/README.md, new surface: docs/design/components/AlbumenCompare/README.md, new surface: docs/design/components/AlbumenFilmstrip/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can view a photo large, zoom to 100 percent to check focus, compare two candidates, and move through photos with the keyboard. Consumer: culling (ratings and flags from §11).
**Treatment:** E opens the loupe with the standard preview, Z toggles 100 percent at the clicked point (decoded on demand), C compares two selected photos with synchronized zoom, arrow keys move through the filmstrip at the bottom, G returns to the grid. Cheaper substitute that fails the checkpoint: opening the file in an external viewer.
**Chrome:** consume the preview cache, the decoder for 100 percent views, and the keymap pattern.

**Requires:** display-session -- the loupe needs an interactive desktop

- [ ] Write the design spec `docs/design/components/AlbumenLoupe/README.md` and `preview.html` (the loupe: fit and 100 percent views, zoom state, and info overlays; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Write the design spec `docs/design/components/AlbumenCompare/README.md` and `preview.html` (the compare view: two candidates with synchronized zoom and pan; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Write the design spec `docs/design/components/AlbumenFilmstrip/README.md` and `preview.html` (the filmstrip: the 96px strip above the status bar, its cells and selection; anatomy, every state, tokens, sizes) before building; Done when: the spec exists and the design page rebuild passes.
- [ ] Loupe with fit and 100 percent zoom. Done when: 100 percent on the DNG shows full resolution within 1 second (quoted).
- [ ] Compare view with synchronized zoom and pan, and the filmstrip. Done when: a driven compare is captured.
- [ ] Commit: `"albumen: loupe, compare, and filmstrip views"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with a view-model test for navigation; the 100 percent timing is quoted and captures committed. Cheaper substitute that fails: an external viewer.

## 10. Keywords, Collections, and Smart Collections

Finding photos later depends on keywords and collections; smart collections save a filter so it stays current. -> SOURCE: albumen-notes-library-collections

**Fidelity:** Keywords panel and collections list -- new build, no baseline; captured to docs/captures/albumen/keywords/ and docs/captures/albumen/collections/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/TextBox/README.md, docs/design/components/Dialog/README.md, docs/design/components/ContextMenu/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can tag photos with keywords, group them in collections, and save filters as smart collections that update themselves. Consumer: the grid's filters and the export batch.
**Treatment:** a keyword panel with autocomplete and a hierarchy (`Places > France > Paris`); collections (manual, drag photos in) and smart collections (a saved filter-bar state with rules joined by all or any); counts per collection and a library statistics summary (photos per year, per camera, rated share) in the left panel's header menu; every change undoable. Cheaper substitute that fails the checkpoint: keywords as free text in a comment field.
**Chrome:** consume the catalog, the filter bar from §8, and the history.

**Requires:** display-session -- the panels need an interactive desktop

- [ ] Keyword hierarchy and assignment with undo. Done when: tests cover assign, remove, rename a keyword across photos, and undo.
- [ ] Collections and smart collections. Done when: a smart collection "rated 4 or more, 2026" updates when a rating changes (test).
- [ ] Library statistics. Done when: a seeded catalog reports expected counts.
- [ ] Commit: `"albumen: keywords, collections, smart collections, and statistics"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with the keyword, collection, and statistics tests reporting; a driven session is captured. Cheaper substitute that fails: static collections only.

## 11. Ratings, Flags, Labels, and XMP Sidecars

Culling is ratings (0 to 5), flags (pick, reject, none), and color labels, set from the keyboard with auto-advance, stored in the catalog, and optionally written to `.xmp` sidecars so other tools see them. Sidecars sit beside originals and never replace them. -> SOURCE: albumen-notes-library-metadata

**Corrected 2026-09-27:** the Albumen parity files extend this section's `XmpSidecar` rather than replace it: `D04 T08 §8`'s `MetadataWriter` is its successor as the one metadata write path (whole-folder writes, embed pending, descript.ion, exported copies), and `D04 T08 §9` adds the opt-in embedding into supported originals; the automatic sidecar setting stays off by default as here (the parity files keep that interpretation), and this section's freeze check holds with every `Albumen.Originals.*` opt-in at its default.

**Freeze check:** Metadata changes write only the catalog and, when `Albumen.Metadata.WriteSidecars` is on, `<name>.xmp` beside the original through an atomic write; the original's bytes and last-write time are unchanged; an existing sidecar from another tool is read, merged (Albumen's fields updated, unknown fields preserved), and written back atomically. Fixture source: `tests/fixtures/albumen/xmp/` (a JPEG and the DNG with darktable- and Lightroom-style sidecars).

**Fidelity:** Grid and loupe with the metadata panel -- docs/design/ (the specs on the Design line below) per standards/design-contract.md; goldens under docs/captures/golden/albumen/metadata-panel/. **Corrected 2026-09-27:** cited docs/captures/albumen/main-window/ as the source; the captures under docs/captures/albumen/ are a before record, never the fidelity source.
**Design:** docs/design/shell-layout.md#albumen-darkroom-and-photo-manager, docs/design/components/Panel/README.md, docs/design/components/Icons/README.md, docs/design/components/ContextMenu/README.md, docs/design/components/Menu/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a photographer can cull fast from the keyboard and have ratings and keywords readable by other tools. Consumer: the grid filters, smart collections, and other applications reading XMP.
**Treatment:** 0-5 set rating, P, X, U set flags, 6-9 set labels, with auto-advance (Caps Lock or a setting), each an undo step logged; Metadata, Write to Sidecars and Read from Sidecars, plus the automatic setting (default off, stated on first use). Cheaper substitute that fails the checkpoint: writing XMP into the original JPEG.
**Chrome:** consume the catalog, the history, `AtomicFileWriter`, and an XMP writer (a small writer over `System.Xml`, or a recorded library decision).

**Requires:** display-session -- keyboard culling needs an interactive desktop

- [ ] Rating, flag, and label commands with undo and auto-advance. Done when: `CullingTests` cover each key and undo.
- [ ] `XmpSidecar` read, merge, and atomic write with the `xmp`, `dc`, and `lr` (hierarchical subject) namespaces darktable and Lightroom use. Done when: round-trip tests keep unknown fields byte-for-byte and darktable reads Albumen's rating back (driven, version quoted).
- [ ] The unchanged-originals test over the xmp fixtures. Done when: it passes.
- [ ] Commit: `"albumen: keyboard culling and safe XMP sidecars"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with `CullingTests` and the sidecar tests reporting; the unchanged-originals assertion passes; darktable shows a rating Albumen wrote (capture). Cheaper substitute that fails: embedding XMP in originals, which the unchanged-originals test catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes every RAW fixture
- [ ] The unchanged-originals tests of §4, §6, and §11 pass
- [ ] The 50,000-image grid budget is quoted
- [ ] `python scripts/todo-graph.py validate` clean
