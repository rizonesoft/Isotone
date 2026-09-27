# Lumen Parity -- Section Design

> **Integrated 2026-09-27.** This design is now a record; the TODO files under `todo/04-lumen/` (and `D00 T01 §8`, `D01 T07 §7` to `§9`) are the plan, and every place the integration departed from it is recorded in those files: the originals policy is safe by default with opt-in writes owned by `D04 T11 §1` (not the frozen no-write guard below), `D01 T07 §7` runs in Phase 23, the guided filter and the PatchMatch solver are built in `Photon.Core` by Imago, the former B-012 rows moved to the plug-in host `D01 T09` and FlashPix and CPT to the legacy codecs `D01 T08`, the Explorer preview (LP-0031) is backlog B-051, the update check `D05 T01 §4` runs in Phase 39, and six sections were added at authoring (`D04 T04 §17`, `§18`, `D04 T08 §9`, `D04 T09 §17`, `D04 T10 §12`, `D04 T14 §10`).

The authoring blueprint for the TODO files that bring Lumen to parity with Adobe Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76, written 2026-09-27 from the unified catalog in [`lumen-parity.md`](lumen-parity.md). It follows the structure of the Nodus design ([`section-design.md`](section-design.md)) and the Imago design ([`imago-section-design.md`](imago-section-design.md)), which are the precedent for every rule below. Agents who author the TODO files follow this document; the integration commit wires what they write into `todo/`. Nothing here is a section yet: sections exist only once authored under `todo/` and placed in `todo/implementation-plan.md`.

## Summary

- **Operator decisions (2026-09-27):** "Now Lumen. I want features from Lightroom, but I've alwyas been loving ACDSee photo manager and IrfanView". The programs are Lightroom Classic, ACDSee Photo Studio Ultimate (its layered Edit mode routes to Imago), and IrfanView. The approved option is "New Lumen parity phases, up to +200", placed "Parity after Lumen 0.1.0": after today's Phase 29 (Lumen 0.1.0) and before today's Phase 30 (Distribution and the suite bundle). The three pillars the operator chose: a **fast default image viewer** (IrfanView-style, opening any image in milliseconds from Explorer, able to be the Windows default viewer for every format it reads, with the catalog one keystroke away), **browse without importing** (ACDSee-style direct folder browsing with background indexing; Lightroom-style import stays an option), and **batch tools are core** (batch rename, convert, resize, and export are Lumen sections, not the suite-wide deferred batch system). Recorded actions, macros, scripting, and command-line automation stay suite-wide and deferred (B-041, B-042); video and animation stay deferred (B-043, B-044); cloud, sync, and sharing services are excluded; AI runs on the shared AI core with its three pillars.
- **Budget (coordinator update, 2026-09-27):** the plan budget is being redesigned in parallel: per-phase and total ceilings are removed for operator-directed planning, only sections a campaign discovers on its own are limited (15 per phase run), and the backlog cap becomes 500. Every section designed here is operator-directed (this decision and the approved "+200" option), so it needs no Origin stamp and this design carries no ceiling snapshot or budget history entry. The count stays near the operator's guidance without padding: **138 new sections**.
- **Sources:** 1,857 Lightroom Classic rows (`LR-0001` to `LR-1857`), 5,182 ACDSee rows (`AC-0001` to `AC-5182`), and 1,880 IrfanView rows (`IV-0001` to `IV-1880`), 8,919 in all, copied verbatim with provenance headers into `sources/`.
- **Catalog:** 1,620 features (`LP-0001` to `LP-1620`), every source id in exactly one row (checked, see "Catalog check" below). Keyboard-shortcut and menu rows (1,144 of them) are folded into the feature they trigger (1,083 rows) or into keymap features of the "Keyboard shortcuts and menus" area.
- **Routing to Imago:** 396 features covering 1,609 source rows (ACDSee Edit mode and its shortcuts, ACDSee's generative tools, IrfanView's Paint plug-in, and one Lightroom row) are `other-app: Imago`, each naming the Imago catalog row that covers the capability; 18 capabilities no Imago row covered were added to [`imago-parity.md`](imago-parity.md) as `IP-2368` to `IP-2385`, each planned in an existing Imago section (see "Imago additions").
- **New sections:** 138: 137 in the ten new Lumen parity phases 30 to 39 (including the 10 release sections `D04 T15 §1` to `§10` and the three new develop-engine stages `D01 T07 §7` to `§9` in Phase 36), plus `D00 T01 §8` (the Lumen catalog validator) in Phase 0, which the budget redesign leaves room for; in 12 new TODO files (`todo/04-lumen/TODO-04` to `TODO-15`; `TODO-03` is a retired address) and two existing files. One existing section moves: `D04 T02 §9` (Lumen accessibility) from old Phase 32 to Phase 39, last before Lumen 1.0.0.
- **Phases:** ten new phases 30 to 39; old 30 (Distribution and the suite bundle) becomes 40 and old 31 (Imago RAW import through the shared decoder) becomes 41; old 32 (Lumen after 0.1.0: accessibility) leaves the plan because its only row moves into Phase 39; Phase 99 stays.
- **Backlog:** promotes B-028 to B-032 and B-034 to B-036 into sections, rewords B-012, B-033, B-042, B-043, and B-046, and adds B-048 (tethered capture), B-049 (self-running slideshows), and B-050 (formats needing proprietary or GPL-incompatible libraries): 23 entries become 18.

### Catalog features by status

| Status | Features | Source rows | Detail |
| ------ | -------: | ----------: | ------ |
| `plan` | 1,070 | 6,269 | owned by 124 new sections |
| `shipped-scope` | 52 | 282 | owned by 16 existing sections (`D04 T01 §2`, `§4` to `§11`, `D04 T02 §1`, `§3` to `§7`, `D01 T02 §4`) |
| `backlog` | 75 | 529 | B-012 4, B-041 21, B-042 1, B-043 33, B-044 1, B-047 2, B-048 1, B-049 5, B-050 7 |
| `excluded` | 24 | 209 | cloud 20, platform 3, removed 1 |
| `other-app` | 399 | 1,630 | Imago 396, none 3 |
| **Total** | **1,620** | **8,919** | |

By source: Lightroom Classic 1,615 rows planned, 131 shipped-scope, 70 backlog, 40 excluded, 1 other-app; ACDSee 3,073 planned, 141 shipped-scope, 210 backlog, 166 excluded, 1,592 other-app (Imago); IrfanView 1,581 planned, 10 shipped-scope, 249 backlog (mostly command-line switches and video), 3 excluded, 37 other-app (the Paint plug-in).

### Catalog features by category

| Category | Features |
| -------- | -------: |
| core | 1,174 |
| automation | 137 |
| ai | 107 |
| format | 92 |
| cloud | 45 |
| print | 44 |
| video | 21 |

### New sections per phase

| Phase | Title | New sections | Relocated rows | Section total | Planned features |
| ---: | ----- | ---: | ---: | ---: | ---: |
| 0 | Workspace spine (existing phase): `D00 T01 §8` | 1 | 0 | 1 | 0 |
| 30 | Lumen parity I: shared formats and the fast default viewer | 18 | 0 | 18 | 174 |
| 31 | Lumen parity II: batch tools and viewer quick edits | 18 | 0 | 18 | 165 |
| 32 | Lumen parity III: browse without importing | 13 | 0 | 13 | 75 |
| 33 | Lumen parity IV: library, collections, search, and the catalog | 14 | 0 | 14 | 132 |
| 34 | Lumen parity V: metadata, keywords, places, import, and capture | 17 | 0 | 17 | 128 |
| 35 | Lumen parity VI: develop I, the panels | 12 | 0 | 12 | 90 |
| 36 | Lumen parity VII: develop II, masking, ACDSee stages, soft proofing, and photo merge | 9 | 0 | 9 | 32 |
| 37 | Lumen AI: faces, keywords, similarity, culling, and masks | 12 | 0 | 12 | 75 |
| 38 | Lumen parity VIII: export, print, slideshows, web galleries, and books | 14 | 0 | 14 | 119 |
| 39 | Lumen parity IX: workspace, preferences, help, and Lumen 1.0.0 | 10 | 1 | 11 | 80 |
| **0, 30-39** | | **138** | **1** | **139** | **1,070** |

### New files

| File | Frontmatter id | Phases | Sections | Planned features | Batch |
| ---- | -------------- | ------ | ---: | ---: | :---: |
| `todo/00-workspace/TODO-01-dev-automation.md` (existing, new `§8`) | `dev-automation` | 0 | 1 | 0 | A |
| `todo/01-core/TODO-07-photon-develop.md` (existing, new `§7` to `§9`) | `photon-develop` | 36 | 3 | 0 | D |
| `todo/04-lumen/TODO-04-lumen-viewer.md` | `lumen-viewer` | 30, 31 | 16 | 179 | A |
| `todo/04-lumen/TODO-05-lumen-browse.md` | `lumen-browse` | 32 | 12 | 75 | B |
| `todo/04-lumen/TODO-06-lumen-parity-library.md` | `lumen-parity-library` | 33 | 13 | 132 | C |
| `todo/04-lumen/TODO-07-lumen-parity-import.md` | `lumen-parity-import` | 34 | 8 | 43 | C |
| `todo/04-lumen/TODO-08-lumen-parity-metadata.md` | `lumen-parity-metadata` | 34 | 8 | 85 | C |
| `todo/04-lumen/TODO-09-lumen-parity-develop.md` | `lumen-parity-develop` | 35, 36 | 16 | 122 | D |
| `todo/04-lumen/TODO-10-lumen-ai.md` | `lumen-ai` | 37 | 11 | 75 | D |
| `todo/04-lumen/TODO-11-lumen-batch.md` | `lumen-batch` | 31 | 10 | 98 | B |
| `todo/04-lumen/TODO-12-lumen-parity-output.md` | `lumen-parity-output` | 38 | 13 | 119 | E |
| `todo/04-lumen/TODO-13-lumen-parity-formats.md` | `lumen-parity-formats` | 30, 31 | 8 | 62 | B |
| `todo/04-lumen/TODO-14-lumen-parity-workspace.md` | `lumen-parity-workspace` | 39 | 9 | 80 | E |
| `todo/04-lumen/TODO-15-lumen-parity-releases.md` | `lumen-parity-releases` | 30 to 39 | 10 | 0 | A |

## How to use this blueprint

- Author one file at a time through `create-todo` (the skill's template, frontmatter, Goal, Current state with claims, Inputs, Outcome with the Adjacency line, Implementation Order, sections, Verification), taking the file's frontmatter id and title, its Goal, its Current-state facts, and every section below exactly as numbered, titled, and ordered.
- Each section's **Hints** are the concrete items it must implement; expand them into micro-steps (one action, a named path, Done when, the cheaper substitute on UI and write items, a source cite) under the 30-item cap, add the `Commit:` item, and write the **Proof** as the Test checkpoint. A section that cannot hold its hints in 30 items is split at authoring time (the file design's "Sizing concerns" names the natural split); otherwise its lowest-value catalog rows move to the backlog through `add-todo` and the catalog is updated in the same commit.
- Each section's **Catalog** line lists the `LP-` features it owns. The authored section names those ranges in its context paragraph ("Catalog: LP-0123 to LP-0150") so the catalog, the section, and the validator agree.
- UI sections carry `Fidelity:`, `Job:`, `Treatment:`, and `Chrome:` (`todo/README.md`, "The second layer the runner reads"); library sections say "no surface of its own". Sections that drive the app carry `**Requires:** display-session -- <reason>`; release sections carry `**Needs:** Clean Windows machine (no .NET SDK)`.
- A section that promotes a backlog entry carries that entry's source key as its `-> SOURCE:` line (see "Backlog changes"); the integration commit deletes the entry. Every other new section carries `-> SOURCE: parity-lumen-<short-name>`.
- Cross-file edges: `Depends On` always uses full refs. Where a section's Inputs name another file's section with `-> XREF:`, the integration commit adds the reciprocal line in the target file (one-sided XREFs are FATAL).
- These sections are operator-directed (the 2026-09-27 decision); under the redesigned budget they carry no Origin stamp.

## Recorded decisions

### Names and paths

Every Lumen parity section runs after Lumen 0.1.0 (`D04 T02 §8`, Phase 29), so hints and checklist items name the target paths `D04 T01 §2` creates: `src/Lumen/Photon.Lumen.Core/`, `src/Lumen/Photon.Lumen.Desktop/` (`Lumen.exe`), `tests/Photon.Lumen.Tests/`, `src/Photon.Core/`, `src/Photon.UI/`, `tests/Photon.Core.Tests/`. Current-state blocks, by contrast, cite today's facts, because a `<!-- claim: -->` must hold on the day the file is authored: `src/Lumen` is absent, `scripts/apps.psd1` still names `src/Lumen/Lumen.UI/Lumen.UI.csproj` with `Shipping = $false`, `installer/Lumen.iss` refuses to compile without `/DLumenShipping` and registers no file type, and `standards/lumen.md` states the original-file guard. If a file is authored after `D04 T01 §2` has shipped, its claims use the real paths directly.

One new project is created, with a recorded reason: `src/Lumen/Photon.Lumen.Viewer/` (`LumenViewer.exe`), the fast default viewer, because its startup budget cannot pay for the library app's composition root, catalog, and module shell (see "The viewer architecture"). It ships inside the Lumen installer and the Lumen portable ZIP, never alone, and is versioned with Lumen (`lumen-v*`). Everything else lives in the existing projects: the viewer's non-UI code in `Photon.Lumen.Core/Viewer/`, browsing and the indexer in `Photon.Lumen.Core/Browse/` and `Photon.Lumen.Core/Indexing/`, batch in `Photon.Lumen.Core/Batch/`, faces in `Photon.Lumen.Core/Faces/`, AI in `Photon.Lumen.Core/AI/`, maps in `Photon.Lumen.Core/Places/`, output in `Photon.Lumen.Core/Output/` (`Print/`, `Slideshow/`, `Web/`, `Books/`), the DNG writer in `Photon.Lumen.Core/Dng/`. The indexer is a mode of `Lumen.exe` (`Lumen.exe --index`), not a service and not a third executable.

### The original-file guard holds everywhere

`standards/lumen.md` makes "Lumen never writes an original image" a frozen behavior, and the parity catalog does not relax it. Features that the competitors implement by rewriting the original are planned in the guard's form, with a note on the catalog row:

- **Metadata written into the file** (Lightroom's "Save Metadata to File" for JPEG, TIFF, and DNG; ACDSee's "Embed ACDSee Metadata"; IrfanView's IPTC and comment editors): Lumen writes the XMP sidecar and embeds the metadata into exported and converted copies, never into the original's bytes.
- **Lossless JPEG rotate and crop in place** (ACDSee, IrfanView): Lumen stores the orientation in the catalog and the sidecar (every viewer honors it), and "Lossless transform to a new file" writes the transformed JPEG beside the original.
- **Save over the original from the viewer or the batch tools:** Save (Ctrl+S) on an edited image opens Save As with a new suggested name; batch output goes to new files; "delete the original after conversion" becomes "move the original to the Recycle Bin after the converted file is verified".
- **File operations are not image writes:** rename, move, copy, and delete to the Recycle Bin are explicit user file operations, planned in full (`D04 T05 §6`, `D04 T11 §3`), with the sidecar and RAW+JPEG partner moved with the photo and an undo journal where the file system allows.

The operator may later choose to relax the guard for a named operation (in-place lossless rotation is the likeliest request from IrfanView and ACDSee users); that is a change to a frozen behavior, recorded in "Decisions for the operator to confirm", not something any section does on its own.

### The viewer architecture (pillar 1: a fast default image viewer)

- **A second executable with a minimal startup path.** `LumenViewer.exe` (`Photon.Lumen.Viewer`, WPF) opens one image as fast as the machine allows: `Main` parses the arguments and starts reading and decoding the file on a thread-pool thread before any window exists; the window is created in parallel and shows the first frame as soon as a screen-size decode is ready; no dependency-injection container, catalog, SQLite provider, or module shell is constructed before the first paint (services for dialogs are built lazily). It references `Photon.Core` (codecs, settings, logging, single instance), `Photon.UI` (theme), and `Photon.Lumen.Core` only for the RAW adapter, which .NET loads only when a RAW file is opened. Publish is ReadyToRun with tiered PGO; WPF cannot be trimmed or compiled Native AOT, which is recorded as the reason the budget is not lower.
- **Measurable budgets** (recorded in `docs/dev/lumen/viewer-budgets.md` with the reference machine, and asserted by `D04 T04 §1`'s startup harness, which launches the published exe and timestamps process start to the first rendered frame through a `--startup-trace` switch): cold start to the first full-screen pixel of a 24-megapixel JPEG at most 450 ms; warm start (files in the OS cache, process not running) at most 250 ms; hand-off to an already running or resident viewer at most 100 ms; next and previous image at most 50 ms from the prefetch cache and at most 150 ms uncached at screen size; a RAW file's embedded preview at most 200 ms; the assemblies loaded at first paint are a committed allow-list (no `Microsoft.Data.Sqlite`, no catalog); working set at most 200 MB for a 24-megapixel image. CI asserts the allow-list and relative timings on every build; the absolute budgets are quoted per release on the reference machine.
- **Optional resident mode** (off by default, IrfanView-style instant opens): "Keep Lumen Viewer ready" starts the viewer hidden at sign-in, and later opens are forwarded to it through `D01 T02 §3`'s single-instance pipe; the setting says how much memory it holds.
- **The catalog one keystroke away.** `T` (IrfanView's thumbnails key) opens the current folder in Lumen's browse mode with the image selected, `Ctrl+L` opens the photo in the Lumen library (importing nothing unless the user asks), and `Ctrl+E` hands it to Imago through `D04 T02 §7`; all three start or forward to `Lumen.exe` through `D01 T02 §3`'s file-open forwarding with a `--browse <folder> --select <file>` argument pair. Lumen's grid and loupe open the selected photo in the viewer with `F3`.
- **Default viewer for every format it reads.** Windows 8 and later refuse programmatic changes to a user's defaults (the `UserChoice` key is hash-protected), so the viewer registers as a capable application instead: `HKCU\Software\RegisteredApplications` names `Lumen Viewer`, whose `Capabilities\FileAssociations` maps every extension the codec registry reads to a per-family ProgID (`LumenViewer.jpeg`, `LumenViewer.raw`, and so on) with its own icon, and each extension gets an `OpenWithProgids` entry. "Make Lumen Viewer the default" then opens `ms-settings:defaultapps?registeredAppUser=Lumen%20Viewer`, where Windows 11 offers one "Set default" button for all of them. IrfanView's per-extension association dialog becomes the chooser of which families are registered. The installer task registers the capabilities (harmless; it takes no default) and never writes `UserChoice`.
- **Shared decoders, never viewer-private ones.** The viewer decodes through the same `Photon.Core/Formats/` registry as Lumen's library, Imago, and the batch tools (`D04 T13 §1`), with screen-size decode (JPEG DCT scaling through WIC, embedded previews for RAW, reduced resolution levels for JPEG 2000 and JPEG XL where the codec offers them) as a registry capability, not a viewer fork.
- **Quick edits in the viewer run the batch operations.** Rotate, crop, resize, color corrections, effects, text, and watermark in the viewer apply the same `IBatchOperation` implementations as the batch edit pipeline (`D04 T11 §7`) to the in-memory image, with undo, and save through Save As; layered editing and painting hand off to Imago.

### Browse without importing (pillar 2)

- **Two kinds of catalog membership.** The catalog (`D04 T01 §5`) gains an `origin` column: `library` for imported photos and `browsed` for files Lumen has seen while browsing a folder. Browse views are driven by the file system (a large-fetch `FindFirstFileEx` enumeration of the folder, sorted and grouped in memory), and the catalog is their cache: metadata, thumbnails, and hashes keyed by path, size, and last-write time. Rating, labeling, keywording, or developing a browsed file creates its catalog record (origin `browsed`) and, when sidecars are enabled, its sidecar, with no import step. "Add to Library" turns browsed records into library records in place; Lightroom-style import (`D04 T01 §6`, extended by `D04 T07`) stays for cards and copies.
- **The background indexer.** `Photon.Lumen.Core/Indexing/` runs one low-priority worker (below-normal thread priority, I/O priority hints) over a priority queue (visible thumbnails first, then the selected folder, then the indexed locations the user chose); it pauses while the user develops or exports and, by setting, on battery; it watches indexed locations with `FileSystemWatcher` and rescans a folder whose watcher buffer overflowed; progress persists across restarts. "Index when idle" optionally registers a per-user scheduled task (at sign-in, when idle) that runs `Lumen.exe --index` headless: no service and no administrator rights.
- **Budgets** (in `docs/dev/lumen/browse-budgets.md`): an unindexed folder of 5,000 JPEGs lists in at most 300 ms and shows its first screen of thumbnails from embedded EXIF thumbnails in at most 1.5 s; a reopened indexed folder shows thumbnails in at most 200 ms; the indexer processes at least 50 JPEGs per second (metadata plus thumbnail) on the reference machine without raising the foreground frame time over 16 ms.
- **The private folder** is an encrypted vault under Lumen's app data (AES-256-GCM per file from `System.Security.Cryptography`, a PBKDF2-SHA256 key from the user's password), not a hidden folder; moving files in is an explicit file operation with verification, files decrypt to memory for viewing, and the section states the honest limit that it is no substitute for disk encryption.

### Batch tools are core (pillar 3)

- **Lumen's own batch system.** `Photon.Lumen.Core/Batch/` holds one job engine: a job is an ordered list of `IBatchOperation`s (rename, convert, resize, rotate, color, develop, the ACDSee Batch Edit and IrfanView advanced operations, text and watermark, export) applied to a file list, run in the background with the Activity Manager (queue, progress, pause, cancel, per-file results and a log), always with a dry run that lists every output name, conflict, and skipped file before anything is written. Outputs are new files written through `AtomicFileWriter`; renames and moves are journaled so they can be undone. Pixel operations reuse the suite pixel engine's effects (`D01 T03`, `D01 T06`) and the develop engine (`D01 T07`), never a copy.
- **One token engine** (`D04 T11 §2`) for batch rename, export naming (extending `D04 T02 §6`'s `{date}-{name}-{seq}` template), import renaming, text overlays, fullscreen and slideshow captions, and print captions; it reads IrfanView's `$`-patterns (`$N`, `$F`, `$E36867`, `$I120`, and the rest) as an accepted alias syntax, so an IrfanView user's saved patterns keep working.
- **What stays deferred.** Recorded actions and macros, scripting, plug-in SDKs, and command-line switches beyond opening a file or folder stay in the suite-wide B-041; batch driven by recorded actions and droplets stays in B-042, which the integration rewords to say Lumen's rename, convert, resize, edit, develop, and export batches are core Lumen sections (`D04 T11`) and not part of it.

### AI: Lumen's own, on the three pillars, local where it should be

Every competitor AI row maps to the Lumen feature that does the same job. The runtime for model-backed jobs is OpenRouter with the user's key through `D01 T05`; nothing is sent without an explicit user action and the send preview, and the preview names every photo, crop, or face that leaves the machine.

- **Faces stay local.** Face detection and recognition run on the machine through OpenCV's YuNet detector (model MIT) and SFace recognizer (model Apache-2.0) on OpenCvSharp4 (Apache-2.0, already a suite dependency through `D03 T15 §5`), with the two model files (about 40 MB) bundled with their license texts; embeddings live in the catalog, clustering is by cosine distance with a user threshold, and nothing about a face is ever sent to a network by the People features. Face regions read and write as MWG regions in XMP sidecars, so Lightroom, digiKam, and Picasa-style tags interchange.
- **Similarity is local and classical.** "Find similar", visual duplicates, and auto-stacking by similarity use perceptual hashes (DCT pHash and dHash) with color and layout signatures in a Hamming-distance index, all own code; semantic "find photos of..." search runs over AI descriptions the user chose to generate (below).
- **Vision through OpenRouter, on request.** AI keywords, captions, alt text, and the descriptions behind natural-language search send a downscaled copy (at most 1,024 px, metadata stripped) to a vision model and land as suggestions the user accepts or rejects, each acceptance one undoable catalog command. Assisted culling scores focus, exposure, and near-duplicates locally; "eyes closed" and expression checks send face crops only when the user enables them, with that fact in the send preview.
- **Masks by locating, not guessing.** AI develop masks (subject, sky, background, objects, people and their parts, landscape classes) ask a vision model for boxes and points as JSON and turn them into masks with the local segmentation engine Imago built (`D03 T10 §6`), which moves to `Photon.Core` on this second consumer; the mask is stored as develop data like any other `D01 T07 §4` component, so it re-renders at any resolution.
- **Pixels from models are new files or cached patches.** Super resolution uses the image-generation adapter Imago built (`D03 T19 §2`, `§8`), moved to `Photon.Core/AI/` by `D04 T10 §8`, and writes a new DNG or TIFF beside the original; generative removal stores its patch as develop data with the provenance record, so it reverts like any spot. Denoise is the classical engine (`D01 T07 §3`); a machine-learning denoiser is B-046 and the catalog rows say so.
- **Explainable and reproducible.** Every AI action writes the suite provenance record (`D01 T05 §3`) into the catalog, shown in the photo's history and embedded as XMP in exports; re-run and compare work as in Imago.

On-device inference beyond OpenCV's small face models (ONNX segmentation, denoise, tagging) stays in B-046.

### Formats and licensing

Every dependency is checked against GPL-3.0 in the section that adds it, with a `docs/dev/decisions.md` row.

| Need | Decision | License | Why |
| ---- | -------- | ------- | --- |
| Reading every format Imago reads | Imago's codec readers move from `Photon.Imago.FileFormats` to `Photon.Core/Formats/` on their second consumer, with content sniffing and a screen-size decode capability (`D04 T13 §1`); Lumen, the viewer, the batch tools, and Imago read through the one registry | As each codec (libwebp BSD-3, libavif BSD-2, libheif LGPL-3.0, libjxl BSD-3, OpenJPEG BSD-2, OpenEXR BSD-3, BCnEncoder.Net MIT, own code) | Shared once, never copied |
| Camera RAW | The decoder `D04 T01 §3` decides (justified default LibRaw, LGPL-2.1 or CDDL-1.0, through a maintained wrapper), extended for coverage reporting and RAW+JPEG pairs by `D04 T13 §5` | LGPL-2.1 | Already decided by the foundation file |
| PDF pages, multi-page documents | PDFium, moved with Imago's reader (`D03 T17 §7`) to `Photon.Core` | BSD-3-Clause and Apache-2.0 | The reference rasterizer |
| PostScript and EPS | The user-installed Ghostscript runner Imago moved to `Photon.Core/Formats/PostScript/` | Ghostscript AGPL-3.0, never bundled | As Imago decided |
| DjVu | DjVuLibre `libdjvulibre` through P/Invoke, native per RID (`D04 T13 §4`) | GPL-2.0-or-later, compatible with GPL-3.0 | The reference decoder; only Lumen reads DjVu |
| Archives (browse into ZIP, 7z, RAR; create ZIP) | SharpCompress for reading, moved with Imago's archive opener (`D03 T17 §12`); `System.IO.Compression` for writing ZIP (`D04 T05 §12`) | MIT | RAR and 7z are read-only; creating them is not offered |
| DNG writing (convert to DNG, render to DNG, smart previews) | Own writer in `Photon.Lumen.Core/Dng/` from the Adobe DNG Specification 1.7.1.0 with own lossless JPEG (ITU T.81 process 14) encoding; Adobe's DNG SDK and `dng_validate` as an oracle only (`D04 T13 §7`) | Own code | The SDK's license is permissive but a writer needs no second native payload |
| Proprietary or GPL-incompatible formats (ECW, MrSID, JBIG2 through AGPL jbig2dec, DWG, Flash) | Not planned: B-050 | Various | No compatible reader |
| Faces | OpenCvSharp4 with YuNet and SFace models (`D04 T10 §2`) | Apache-2.0 (wrapper, SFace), MIT (YuNet) | Local, small, and accurate enough; no face leaves the machine |
| Map tiles and offline basemap | Own slippy-map control on SkiaSharp (Web Mercator XYZ tiles, clustering) (`D04 T08 §6`); the tile source is a setting, defaulting to OpenStreetMap's standard tiles under the OSMF tile usage policy (identifying User-Agent, visible attribution, HTTP caching, no bulk prefetch), with an offline basemap from Natural Earth 1:50m vectors bundled and rendered locally | OSM data ODbL (attribution), Natural Earth public domain | No cloud dependency is required: the map works offline at country-to-region scale, and online tiles are one setting away |
| Reverse geocoding | Offline, from the GeoNames `cities1000` and admin-code dumps bundled and indexed with a k-d tree (`D04 T08 §7`) | CC BY 4.0 (attribution in About) | Lightroom's address lookup needs Google's service; an offline lookup to city, state, and country needs none |
| GPX track logs | Own reader over `System.Xml` (`D04 T08 §7`) | Own code | Small, documented format |
| Scanners | WIA 2.0, moved with Imago's acquisition code (`D03 T17 §12`), plus TWAIN through NTwain over the TWAIN data source manager the scanner driver installs (never bundled) (`D04 T07 §7`) | Windows; NTwain MIT | IrfanView's TWAIN batch scanning needs TWAIN |
| Phones and cameras without a drive letter | Windows Portable Devices (MTP and PTP) through its COM API (`D04 T07 §4`) | Part of Windows | No package |
| Screen capture | `Windows.Graphics.Capture`, moved with Imago's screenshot code (`D03 T17 §12`) | Part of Windows | No package |
| Slideshow music | NAudio over Media Foundation (`D04 T12 §7`) | MIT | MP3, AAC, and WAV playback with fades |
| PowerPoint output | DocumentFormat.OpenXml (`D04 T12 §11`) | MIT | The Open XML SDK writes PPTX without Office |
| PDF output (books, contact sheets, slideshows) | The suite PDF writer (PDFsharp, moved to `Photon.Core/Pdf/` by `D03 T17 §7`) | MIT | One PDF writer for the suite |
| Web gallery upload | FluentFTP (FTP and FTPS, moved with Imago's reader to `Photon.Core`) and SSH.NET (SFTP) (`D04 T12 §9`) | MIT (both) | Uploading to the user's own server is not a cloud service |
| Web gallery templates | Own HTML, CSS, and JavaScript templates, licensed MIT inside the generated gallery (`D04 T12 §9`) | Own code (MIT for the generated assets) | A user's website must not inherit GPL obligations from a template |
| Email | Simple MAPI (`MAPISendMailW`) through the default mail client, with a folder-and-`mailto:` fallback (`D04 T12 §12`) | Part of Windows | No mail service of Lumen's own |
| Disc burning | IMAPI2 (`D04 T12 §1`) | Part of Windows | Lightroom's burn-to-disc export target |
| Text recognition and barcodes in the viewer | `Windows.Media.Ocr` (built into Windows 10 and 11) and ZXing.Net (`D04 T04 §9`) | Part of Windows; Apache-2.0 | IrfanView's OCR and QR plug-ins without bundling Tesseract models |
| Private folder encryption | `AesGcm` and `Rfc2898DeriveBytes` from .NET (`D04 T05 §9`) | Part of .NET | No package |
| Tethered capture | Not planned: B-048 (see below) | -- | -- |

Nothing Adobe, ACDSee, or IrfanView ships is bundled: no Adobe camera or lens profiles (users point Lumen at the DCP and LCP files they own, read by `D01 T07`), no ACDSee presets, LUTs, or brush files, no IrfanView plug-ins or skins; users import the files they own.

### Tethered capture: evaluated, deferred to B-048

Lightroom's tethered capture drives a camera over USB. On Windows the options are: the vendors' SDKs (Canon EDSDK, Nikon SDK, Sony Camera Remote SDK), which are proprietary, registration-gated, and not redistributable with a GPL-3.0 program; libgphoto2 (LGPL-2.1, license-compatible), which has no supported Windows build and needs each camera's driver replaced with WinUSB (Zadig), breaking the vendor's own software and Windows' MTP access; and Windows Portable Devices' still-capture command over PTP, which only some cameras implement and which exposes no live view or settings control. None meets the suite's bar of a proven, supported path, so tethered capture proper is backlog B-048 with those findings, and Lumen covers the tethered workflow through `D04 T07 §5`: auto import from a watched folder that the camera maker's free tether utility writes into, with rename, develop preset, metadata, and previews applied as each file lands.

### Maps, places, and privacy

`D04 T08 §6` promotes B-034: a map view with the tile source above, placing photos by drag and drop, clusters, saved locations (with a "private" flag that strips GPS from exports inside the radius), and a location filter; `D04 T08 §7` adds GPX track logs with a time-zone offset, reverse geocoding offline, and removing location on export (already an option in `D04 T02 §6`, extended to saved locations). No map feature requires a network; online tiles, when enabled, send only tile coordinates.

### Output: consume the suite's print and PDF code

- **Print** (`D04 T12 §4`, `§5`, promoting B-035) runs on the print dialog frame in `Photon.UI/Print/` (moved from Nodus by `D03 T18 §6`) and the suite color engine (`D01 T04`), with printer profiles, rendering intent, print sharpening, and 16-bit output; print to JPEG writes a file.
- **Contact sheets** (`D04 T12 §6`) move Imago's contact-sheet engine (`D03 T18 §7`) to `Photon.Core` on this second consumer.
- **Slideshows, web galleries, and books** are Lumen's own (`D04 T12 §7` to `§10`); their PDF output goes through the suite PDF writer, video export is B-043, and self-running EXE and screen-saver slideshows are B-049.

### Out of scope, deferred, and other apps

- **Cloud and online services** (`excluded: cloud`): Adobe accounts, Lightroom cloud sync and shared albums, Adobe Portfolio and Adobe Stock, Blurb upload, Flickr, SmugMug, Zenfolio and other photo-site uploaders, ACDSee 365, SeeDrive, OneDrive integration, and ACDSee Mobile Sync.
- **Deferred to after the first release** (operator decision 2026-09-26, not excluded): suite scripting, macros, plug-in SDKs, and command-line automation (B-041), action-based batch and droplets (B-042), video and audio (B-043, reworded suite-wide), animation authoring and frame extraction (B-044).
- **Kept in the backlog**: tethered capture (B-048), self-running slideshows (B-049), proprietary formats (B-050), on-device models (B-046), Content Credentials (B-047), and a GPU develop path (B-033, no measured failure yet).
- **Other apps** (`other-app`): ACDSee Edit mode, ACDSee's generative image tools, and IrfanView's Paint plug-in are layered pixel editing and route to Imago rows; third-party products (legacy ACDSee database files, vendor utilities) route to none.

### Routing ACDSee Edit mode to Imago

ACDSee's Edit mode is a layered pixel editor (layers, adjustment layers, masks, selections, drawing tools, text, layer effects, 246 special-effect options, geometry, exposure, color, and detail tools, plus the AI face editor, sky replacement, and the credit-based generative tools); the operator routes it to Imago. Every such row is `other-app: Imago <IP-####> <reason>`, where the IP id is the Imago catalog row that already plans the capability, so the Lumen catalog never duplicates an Imago section. Edit-mode shortcuts point at the Imago row of the tool they trigger or at Imago's shortcut rows (`IP-2147` and its neighbors). Three kinds of Edit-mode rows stay in Lumen: moving between Lumen and the editor (`shipped-scope D04 T02 §7`, Edit in Imago), rating, labeling, tagging, and navigation keys that work in every ACDSee mode (the Lumen keymap `D04 T14 §3` and `D04 T01 §11`), and ACDSee Actions recording (B-041). IrfanView's Paint plug-in and Lightroom's "Edit in Firefly" route to Imago the same way.

### Imago additions

Eighteen Edit-mode capabilities had no Imago row. Each is now a row of [`imago-parity.md`](imago-parity.md) (`IP-2368` to `IP-2385`, added in this change with no Photoshop, Affinity, or GIMP id and a note naming the Lumen row and the ACDSee ids), planned in the most fitting existing Imago section; the integration commit adds one checklist item to each named section (every target stays at or under 30 items; counts from `todo/implementation-plan.md` today) and extends that section's `Catalog:` line.

| IP id | Capability | Imago section | Items today, after |
| ----- | ---------- | ------------- | ---: |
| IP-2368 | Smart brushing on filter and adjustment brushes (restrict strokes by color or brightness tolerance) | `D03 T14 §1` | 24, 25 |
| IP-2369 | One-click masked background adjustments from an AI subject mask (black and white background) | `D03 T19 §15` | 13, 14 |
| IP-2370 | Photo effect adjustment layer with preset photographic looks | `D03 T11 §5` | 26, 27 |
| IP-2371 | Insert image metadata fields as text in a text layer | `D03 T16 §4` | 20, 21 |
| IP-2372 | Face edit framework: landmarks, face selector, symmetric link, presets | `D03 T19 §11` | 12, 15 (with IP-2373 and IP-2374) |
| IP-2373 | Face color retouching over face landmarks (eyes, teeth, brows, lips, blush, eyeshadow) | `D03 T19 §11` | (above) |
| IP-2374 | Hair recolor with an automatic hair mask | `D03 T19 §11` | (above) |
| IP-2375 | One-click photo looks as built-in look presets | `D03 T11 §4` | 23, 24 |
| IP-2376 | Collage effect | `D01 T06 §11` | 16, 17 |
| IP-2377 | Furry edges effect | `D01 T06 §12` | 18, 19 |
| IP-2378 | Jiggle distortion | `D01 T06 §6` | 22, 25 (with IP-2379 and IP-2381) |
| IP-2379 | Pixel explosion | `D01 T06 §6` | (above) |
| IP-2380 | Rain render | `D01 T06 §9` | 20, 21 |
| IP-2381 | Water reflection | `D01 T06 §6` | (above) |
| IP-2382 | Water drops | `D01 T06 §8` | 23, 24 |
| IP-2383 | Watermark placement with saved images, anchors, keyed transparency, blend, and presets | `D03 T17 §1` | 27, 28 |
| IP-2384 | Decorative border frames with textures, irregular edges, and raised edges | `D03 T14 §9` | 15, 16 |
| IP-2385 | Light EQ tone equalizer as a filter and adjustment layer | `D03 T11 §2` | 26, 27; consumes `D01 T07 §7` |

`D00 T01 §8` teaches the Imago catalog check that these rows carry no source id by design (see its hints). The Imago catalog's Totals line and Areas counts are updated in this change.

### Backlog changes

Promoted into Lumen parity sections (each promoted entry is deleted from `todo/backlog.md` in the commit that authors its section, which is the integration commit when the batches land together, and its source key rides the section's `-> SOURCE:` line):

| Entry | Source key | Promoted into |
| ----- | ---------- | ------------- |
| B-028 Local adjustments: brush, linear, and radial masks | `lumen-roadmap-local` | `D04 T09 §9` |
| B-029 Detail: sharpening and noise reduction | `lumen-roadmap-detail` | `D04 T09 §5` |
| B-030 Lens corrections | `lumen-roadmap-lens` | `D04 T09 §6` |
| B-031 Color grading and HSL | `lumen-roadmap-color` | `D04 T09 §4` |
| B-032 HDR and panorama merge | `lumen-roadmap-merge` | `D04 T09 §16` (which moves Imago's alignment, HDR, panorama, and focus-merge engines to `Photon.Core/Photo/`, as the entry said) |
| B-034 Map and GPS | `lumen-roadmap-map` | `D04 T08 §6` (track logs in `§7`) |
| B-035 Contact sheets and print | `lumen-roadmap-print` | `D04 T12 §4` (contact sheets in `§6`) |
| B-036 Catalog maintenance and library statistics | `lumen-roadmap-catalog` | `D04 T06 §9` (statistics in `§12`) |

Kept: **B-033** (a GPU develop path) stays, with no measured failure yet; its `needs` field names B-029, which this change deletes, so it is reworded to `needs: D04 T09 §5, D01 T07 §1`. **B-026** (Imago performance), **B-039** (RAW import in Nodus), **B-044**, **B-045**, and **B-047** are unchanged.

Reworded:

- **B-012** (third-party filter plug-in hosts): Lumen's viewer effects (`D04 T04 §15`) and batch edit pipeline (`D04 T11 §7`) become hosts too, since IrfanView loads 8BF and Filter Factory filters; `needs` gains `D04 T04 §15`.
- **B-042** (suite-wide batch processing and droplets): the summary says Lumen's batch rename, convert, resize, rotate, color, edit, develop, and export are core Lumen sections (`D04 T11`, operator decision 2026-09-27) and not part of this entry, which keeps batch driven by recorded actions, droplets, conditional actions, data-driven graphics, and batch runs started from the command line (IrfanView's `/convert` family).
- **B-043** (video layers and the timeline) becomes suite-wide as "Video and audio": `app: suite`, and the summary adds Lumen's video cataloging and playback, trimming and frame capture, ACDSee's Media mode, audio attached to images, video in slideshows and slideshow video export, and IrfanView's video and audio playback.
- **B-046** (on-device models): the summary names Lumen's machine-learning denoise, tagging, and similarity embeddings as further consumers and states that Lumen's face detection and recognition are not in this entry (they run locally through OpenCV's small models in `D04 T10 §2`).

New entries (ids taken in order; drafts in the entry grammar; each names `app: lumen`):

```
- [B-048] Tethered capture -- app: lumen -- source: parity-lumen-tether -- added: 2026-09-27 -- summary: Lightroom-style tethered shooting: camera detection over USB, remote capture with a shutter button and interval, camera settings shown, live view where the body supports it, and each frame imported with naming, develop preset, and metadata as it lands -- needs: D04 T07 §5 -- why deferred: the vendor SDKs (Canon EDSDK, Nikon SDK, Sony Camera Remote SDK) are proprietary and not redistributable with a GPL-3.0 program; libgphoto2 (LGPL-2.1) has no supported Windows build and needs each camera's driver replaced with WinUSB, which breaks the vendor's software; Windows Portable Devices' still-capture command is implemented by only some cameras and has no live view; the watched-folder auto import (D04 T07 §5) covers the workflow through the vendor's own tether utility -- promote when: a GPL-compatible Windows capture path is proven on at least two camera brands, or the operator accepts a per-vendor optional plug-in model
- [B-049] Self-running slideshows -- app: lumen -- source: parity-lumen-slideshow-exe -- added: 2026-09-27 -- summary: save a slideshow as a standalone EXE or a screen saver (.scr), burn it to CD, DVD, or Blu-ray with autorun, and ACDSee's Showroom desktop slideshow gadget -- needs: D04 T12 §8 -- why deferred: an executable output embeds a player that must be signed, maintained, and kept clear of antivirus heuristics; the PDF, JPEG, and web-gallery outputs already share a slideshow -- promote when: a user needs an offline self-running show and the suite signing certificate (D99 T01 §3) exists
- [B-050] Formats needing proprietary or GPL-incompatible libraries -- app: lumen -- source: parity-lumen-proprietary-formats -- added: 2026-09-27 -- summary: ECW, MrSID, and JPM; JBIG2 (the reference decoder jbig2dec is AGPL-3.0); FlashPix and MRC; CAD formats (DWG, DXF, HPGL, CGM) that IrfanView reads through proprietary plug-ins; Flash SWF and FLV; and undocumented layered formats (Artweaver, BodyPaint, Corel PHOTO-PAINT CPT, Gemstone GSD, ACDSee ACDC), each needing a fidelity fixture when promoted -- needs: D04 T13 §8 -- why deferred: no GPL-3.0-compatible reader exists or the format is undocumented -- promote when: a compatible reader appears, or a user supplies a real file and a license path is recorded
```

Backlog count after the integration: 23 minus 8 promoted plus 3 new is 18, against the cap (500 after the budget redesign).

### The Imago and Nodus catalogs

Beyond the eighteen added rows, no Imago or Nodus status changes: the Imago rows that already said `other-app: Lumen` (IP-1504 fullscreen review, IP-1505 filmstrip sync, IP-1506 raw developer hand-off, IP-1853 Bridge browsing) and Nodus's NP-2798 (AfterShot) are now covered by Lumen sections (`D04 T04 §7`, `D04 T09 §12`, `D04 T02 §7`, `D04 T05 §1`, and the develop file), which their notes may cite at integration without a status change.

## Phase layout and renumbering

The ten Lumen parity phases sit after Phase 29 (Lumen 0.1.0) and before the old Phase 30 (Distribution and the suite bundle). Each ends with a Lumen release section in `D04 T15`. Within a phase, rows run in the order listed; the relocated `D04 T02 §9` (accessibility and localization) runs last in Phase 39 before the release, so it audits every parity surface. `D00 T01 §8` joins Phase 0 after `§7`.

| Phase | Rows in order |
| ---: | ----- |
| 0 | (existing rows), `D00 T01 §8` after `D00 T01 §7` |
| 30 | `D04 T13 §1`, `D04 T13 §2`, `D04 T13 §3`, `D04 T13 §8`, `D04 T13 §4`, `D04 T13 §5`, `D04 T04 §1`, `D04 T04 §2`, `D04 T04 §3`, `D04 T04 §4`, `D04 T04 §14`, `D04 T04 §5`, `D04 T04 §6`, `D04 T04 §9`, `D04 T04 §10`, `D04 T04 §7`, `D04 T04 §8`, `D04 T15 §1` |
| 31 | `D04 T11 §1`, `D04 T11 §2`, `D04 T11 §3`, `D04 T13 §6`, `D04 T11 §4`, `D04 T11 §5`, `D04 T11 §6`, `D04 T11 §8`, `D04 T11 §7`, `D04 T13 §7`, `D04 T11 §9`, `D04 T11 §10`, `D04 T04 §11`, `D04 T04 §16`, `D04 T04 §12`, `D04 T04 §15`, `D04 T04 §13`, `D04 T15 §2` |
| 32 | `D04 T05 §1`, `D04 T05 §2`, `D04 T05 §3`, `D04 T05 §4`, `D04 T05 §5`, `D04 T05 §6`, `D04 T05 §7`, `D04 T05 §8`, `D04 T05 §9`, `D04 T05 §10`, `D04 T05 §11`, `D04 T05 §12`, `D04 T15 §3` |
| 33 | `D04 T06 §1`, `D04 T06 §2`, `D04 T06 §3`, `D04 T06 §4`, `D04 T06 §5`, `D04 T06 §6`, `D04 T06 §7`, `D04 T06 §8`, `D04 T06 §9`, `D04 T06 §10`, `D04 T06 §11`, `D04 T06 §12`, `D04 T06 §13`, `D04 T15 §4` |
| 34 | `D04 T08 §1`, `D04 T08 §8`, `D04 T08 §2`, `D04 T08 §3`, `D04 T08 §4`, `D04 T08 §5`, `D04 T07 §1`, `D04 T07 §2`, `D04 T07 §3`, `D04 T07 §4`, `D04 T07 §5`, `D04 T07 §6`, `D04 T07 §7`, `D04 T07 §8`, `D04 T08 §6`, `D04 T08 §7`, `D04 T15 §5` |
| 35 | `D04 T09 §1`, `D04 T09 §2`, `D04 T09 §3`, `D04 T09 §4`, `D04 T09 §5`, `D04 T09 §6`, `D04 T09 §7`, `D04 T09 §8`, `D04 T09 §10`, `D04 T09 §11`, `D04 T09 §12`, `D04 T15 §6` |
| 36 | `D04 T09 §9`, `D01 T07 §7`, `D01 T07 §8`, `D01 T07 §9`, `D04 T09 §13`, `D04 T09 §14`, `D04 T09 §15`, `D04 T09 §16`, `D04 T15 §7` |
| 37 | `D04 T10 §1`, `D04 T10 §2`, `D04 T10 §3`, `D04 T10 §4`, `D04 T10 §5`, `D04 T10 §6`, `D04 T10 §7`, `D04 T10 §8`, `D04 T10 §9`, `D04 T10 §10`, `D04 T10 §11`, `D04 T15 §8` |
| 38 | `D04 T12 §1`, `D04 T12 §13`, `D04 T12 §2`, `D04 T12 §3`, `D04 T12 §4`, `D04 T12 §5`, `D04 T12 §6`, `D04 T12 §7`, `D04 T12 §8`, `D04 T12 §9`, `D04 T12 §10`, `D04 T12 §11`, `D04 T12 §12`, `D04 T15 §9` |
| 39 | `D04 T14 §1`, `D04 T14 §2`, `D04 T14 §3`, `D04 T14 §4`, `D04 T14 §5`, `D04 T14 §6`, `D04 T14 §7`, `D04 T14 §8`, `D04 T14 §9`, `D04 T02 §9`, `D04 T15 §10` |

**Renumbering of the existing phases:**

| Old | New | Title |
| --- | --- | ----- |
| 0 to 29 | 0 to 29 | unchanged (Phase 0 gains `D00 T01 §8`) |
| -- | 30 to 39 | the Lumen parity phases above |
| 30 | 40 | Distribution and the suite bundle |
| 31 | 41 | Imago after 0.1.0: RAW import through the shared decoder (keeps `D03 T07 §11`) |
| 32 | -- | leaves the plan: its only row, `D04 T02 §9`, moves to Phase 39 |
| 99 | 99 | Manual: operator-only steps |

Prose that names an old phase number (`todo/implementation-plan.md` headings and paragraphs, including Phase 29's and Phase 41's paragraphs; the domain `INDEX.md` phase lines, where `todo/04-lumen/INDEX.md` becomes "Phases 28 to 39" and `todo/03-imago/INDEX.md` changes "31" to "41"; `todo/TODO-00-INDEX.md`; `AGENTS.md`; the `D04 T01` and `D04 T02` Goal, non-goals, and Outcome sentences that name Phase 32 or list maps, printing, face recognition, and tethered capture as non-goals) is updated in the same commit; no section ref changes. The redesigned budget (schema 2 of `todo/budget.json`) has no per-phase ceiling, so no budget entry is written for the new, renumbered, or removed phases; phases have no size limit and these operator-directed sections carry no Origin line.

## Acceptance bar additions

New rows for "The acceptance bar" in `todo/implementation-plan.md`:

| Aim | Owned by |
| --- | -------- |
| Lumen covers every Lightroom Classic, ACDSee Photo Studio Ultimate, and IrfanView capability in its parity catalog | `D00 T01 §8` (the catalog gate) · `D04 T15 §1`-`§10` (each release reconciles its phase) |
| Any image opens instantly: the Lumen Viewer shows the first pixel within its recorded startup budget and can be the Windows default viewer for every format Lumen reads | `D04 T04 §1` · `D04 T04 §2` · `D04 T04 §3` · `D04 T13 §1` |
| Any folder can be browsed without importing it, indexed in the background | `D04 T05 §1` · `D04 T05 §2` |
| Batch tools rename, convert, resize, edit, develop, and export with a dry run first, and never write an original | `D04 T11 §1` · `D04 T11 §3` · `D04 T11 §4` · `D04 T11 §7` · `D04 T11 §9` |
| Faces are detected and recognized on the machine and never sent anywhere | `D04 T10 §2` · `D04 T10 §3` |

Existing rows gain owners: "Originals are never written" adds `D04 T04 §11` · `D04 T04 §16` · `D04 T05 §6` · `D04 T08 §8` · `D04 T11 §1`; "Every edit has a reverse" adds `D04 T05 §6` · `D04 T11 §3`; "Shared once, never copied" adds `D04 T13 §1` · `D04 T13 §6` · `D04 T09 §16` · `D04 T10 §7` · `D04 T10 §8` · `D04 T12 §6` · `D01 T07 §9`; "Formats are proven, not assumed" adds `D04 T13 §1` · `D04 T13 §2` · `D04 T13 §3` · `D04 T13 §4` · `D04 T13 §6` · `D04 T13 §7` · `D04 T13 §8`; "No dependency without a reason and a license" adds `D04 T10 §2` · `D04 T08 §6` · `D04 T08 §7` · `D04 T13 §4` · `D04 T07 §7` · `D04 T12 §8` · `D04 T12 §9` · `D04 T12 §11`; "AI results are editable, undoable, and reproducible" adds `D04 T10 §1` · `D04 T10 §4` · `D04 T10 §7`; "Nothing leaves the machine without an explicit user action" adds `D04 T10 §1` · `D04 T08 §6`; "It works without a mouse or eyes" keeps `D04 T02 §9`, which now runs last in Phase 39.

## Authoring batches

Five disjoint file sets of roughly equal size, so five agents can author in parallel. Each batch writes only its own files; every `-> XREF:` it writes into another batch's file, or into an existing file, is listed in its report, and the integration commit adds the reciprocal lines, the index rows, the plan rows, the backlog changes, the Imago additions, and the `D04 T02 §9` relocation in one pass.

| Batch | Files | Sections | Subject |
| :---: | ----- | ---: | ------- |
| A | `TODO-04-lumen-viewer.md`, `TODO-15-lumen-parity-releases.md`, `D00 T01 §8` | 27 | the fast default viewer, its quick edits, the ten releases, and the catalog validator |
| B | `TODO-13-lumen-parity-formats.md`, `TODO-11-lumen-batch.md`, `TODO-05-lumen-browse.md` | 30 | the shared codec registry and formats, the batch tools, and browsing without importing |
| C | `TODO-06-lumen-parity-library.md`, `TODO-07-lumen-parity-import.md`, `TODO-08-lumen-parity-metadata.md` | 29 | the library, collections, search, the catalog, import and capture, metadata, keywords, and places |
| D | `TODO-09-lumen-parity-develop.md`, `D01 T07 §7`-`§9`, `TODO-10-lumen-ai.md` | 30 | develop, the three new develop-engine stages, and Lumen AI |
| E | `TODO-12-lumen-parity-output.md`, `TODO-14-lumen-parity-workspace.md`, the `D04 T02 §9` relocation | 22 | export, print, slideshows, web galleries, books, the workspace, preferences, and help |

## Integration commit checklist

- Author or collect the 12 new files and the new `D00 T01 §8` and `D01 T07 §7` to `§9`; list each new file in `todo/04-lumen/INDEX.md` and `todo/TODO-00-INDEX.md`, and the new sections in the existing files' Implementation Order tables.
- Add the ten Lumen parity phases to `todo/implementation-plan.md` (heading, one paragraph, one table each, from "Phase paragraphs" below), add `D00 T01 §8` to Phase 0, move `D04 T02 §9` into Phase 39, renumber old 30 and 31 to 40 and 41, remove old Phase 32, and add the acceptance-bar rows and owners.
- Record the budget per the redesigned rules (operator-directed sections, no ceiling snapshot); delete the eight promoted backlog entries, reword B-012, B-033, B-042, B-043, and B-046, and add B-048 to B-050.
- Add the eighteen Imago checklist items listed in "Imago additions" to their sections, with each section's `Catalog:` line extended by its new IP id.
- Update `D04 T01`'s Job and non-goals (tethered capture is B-048; face recognition, maps, printing, books, and slideshows are planned in the parity files; cloud sync stays excluded; video is B-043; plug-ins are B-041), `D04 T02`'s Goal and Outcome for the relocation of `§9` (and its Depends On: add `D04 T14 §9` and `D04 T12 §13`), and `todo/04-lumen/INDEX.md`'s paragraph and phase line.
- Update `standards/lumen.md`: the `Photon.Lumen.Viewer` project row, the browsed-versus-library catalog membership, and the guard's list of operations that write new files instead of originals; update `docs/dev/architecture.md`'s target layout with the viewer project.
- Reciprocate every cross-file `-> XREF:` the batch reports list (including the Imago sections whose code moves: `D03 T10 §6`, `D03 T11 §4`, `D03 T15 §5`, `§6`, `§7`, `§9`, `D03 T17 §5` to `§9`, `§11`, `§12`, `D03 T18 §6`, `§7`, `D03 T19 §2`, `§8`, `§11`, `§14`, and the engines `D01 T03`, `D01 T04`, `D01 T05`, `D01 T06`, `D01 T07`), plus `D04 T01` and `D04 T02` sections the parity sections extend.
- Update `AGENTS.md` (the `docs/parity/` row and the plan paragraph naming the Lumen decision and phases), `README.md`, and `CHANGELOG.md` as the Nodus and Imago integrations did; `docs/parity/README.md` is updated in this change.
- Run `python scripts/todo-graph.py validate`, `plan --sync`, `plan --check`, `query budget`, and `python scripts/todo-claims.py`; all clean.

## Phase paragraphs

### Phase 30 -- Lumen parity I: shared formats and the fast default viewer

The first pillar comes first. Imago's codec readers move to `Photon.Core/Formats/` as Lumen becomes their second consumer, Lumen reads every modern, HDR, legacy, rare, document, multi-page, and RAW format the three competitors open, and the Lumen Viewer ships as a second executable with a recorded startup budget: screen-size decode with prefetch and display color, registration as a capable default viewer for every format it reads, zoom and display options, folder browsing, file operations and hand-offs, image information and viewer tools, multi-page and animated images, fullscreen, and the viewer's own slideshow, with the Lumen library one keystroke away. It ends with `lumen-v0.2.0`.

### Phase 31 -- Lumen parity II: batch tools and viewer quick edits

The third pillar follows, because the viewer's quick edits run its operations. Lumen gets its own batch engine with the Activity Manager, one token engine that also reads IrfanView's patterns, batch rename with undo, write formats with every per-format option, batch convert, resize, rotate, and color, text overlays and watermarks, the ACDSee and IrfanView batch edit pipeline, the DNG writer, batch develop and export, and the batch dialog reachable from Explorer and the viewer; then the viewer's quick edits (rotate, select, crop, resize, lossless JPEG transforms to new files, color corrections, effects, text, watermarks, and borders), all saved as new files. It ends with `lumen-v0.3.0`.

### Phase 32 -- Lumen parity III: browse without importing

The second pillar: any folder opens in Lumen without an import, with browsed photos cached in the catalog and a background indexer keeping thumbnails and metadata ready, a folder tree with favorites and tabs, file-list views and thumbnails, sorting, grouping, filtering, full file operations with undo, the info palette and compare, the image basket and selective browsing, an encrypted private folder, calendar browsing, a duplicate finder, and archives and folder sync. It ends with `lumen-v0.4.0`.

### Phase 33 -- Lumen parity IV: library, collections, search, and the catalog

Lightroom's and ACDSee's library catches up over both browsed and imported photos: view options, a survey view and a second window, culling extensions, stacks and virtual copies, the extended filter bar, collection sets and the full smart-collection rule editor, ACDSee categories, quick and advanced search, the folders and catalog panels with offline volumes, catalog backup and maintenance, multiple catalogs, smart previews for offline editing, the dashboard, and Painter and Quick Develop. It ends with `lumen-v0.5.0`.

### Phase 34 -- Lumen parity V: metadata, keywords, places, import, and capture

Metadata comes before the import extensions that apply it: every EXIF, IPTC, and XMP field read and tracked, sidecar and exported-copy writing, the metadata panel and properties pane, metadata presets, capture time editing, and keyword extensions; then the import window, file handling, import presets, phones and cameras over Windows Portable Devices, watched-folder auto import, DNG conversion, scanning, and screen capture; then the map view with offline reverse geocoding and track logs. It ends with `lumen-v0.6.0`.

### Phase 35 -- Lumen parity VI: develop I, the panels

Develop's panels reach Lightroom and ACDSee on the suite develop engine: the extended workspace with reference view and overlays, history and saving semantics, profiles and white balance, tone curve, color mixer, point color, and color grading, detail, lens corrections, transform and calibration, effects and crop, remove and red eye, presets and defaults, and sync. It ends with `lumen-v0.7.0`.

### Phase 36 -- Lumen parity VII: develop II, masking, ACDSee stages, soft proofing, and photo merge

Local work and the stages only ACDSee has: masking with brushes, gradients, range masks, and pixel targeting; three new stages in the suite develop engine (the tone equalizer, soft focus and skin tune, and LUTs, blend modes, and looks), whose Lumen surfaces are Light EQ, soft focus, skin tune, color LUTs, and develop effects; soft proofing; and photo merge, which moves Imago's alignment, HDR, panorama, and focus-merge engines to `Photon.Core`. It ends with `lumen-v0.8.0`.

### Phase 37 -- Lumen AI: faces, keywords, similarity, culling, and masks

AI comes after the library, metadata, and develop surfaces it feeds. Lumen maps every competitor AI job to a non-destructive, explainable feature on the shared AI core: the AI menu with the send gate and provenance, local face detection and recognition and the People view with face tags, AI keywords, captions, and alt text, similar photos, assisted culling, AI develop masks, Enhance (denoise, raw details, super resolution), generative and distraction removal, lens blur with estimated depth, and adaptive presets with natural-language search. It ends with `lumen-v0.9.0`.

### Phase 38 -- Lumen parity VIII: export, print, slideshows, web galleries, and books

Output catches up with Lightroom's modules and ACDSee's creation tools: the extended export dialog, presets, metadata, watermarks, and post-processing, more export formats and DNG output, local publish folders, the print module with packages and templates, contact sheets, slideshows with music and PDF export, web galleries with upload to the user's own server, books, PDF and PowerPoint creation, and email. It ends with `lumen-v0.10.0`.

### Phase 39 -- Lumen parity IX: workspace, preferences, help, and Lumen 1.0.0

The last parity phase customizes and audits the whole surface once it exists: modes and the module picker, toolbars, menus, pane layout, saved workspaces, and touch, the keymap with its alternative key sets, every preference page, settings storage and portable mode, help, languages, and updates, themes, external editors, and the accessibility and localization audit (`D04 T02 §9`, moved here from old Phase 32) over every parity surface. It ends with `lumen-v1.0.0`, which declares the parity catalog complete.

### Phase 40 -- Distribution and the suite bundle (was Phase 30)

Unchanged in content; its paragraph now says it runs after Lumen 1.0.0, so the first suite bundle carries Lumen at its parity release.

### Phase 41 -- Imago after 0.1.0: RAW import through the shared decoder (was Phase 31)

Unchanged in content; its paragraph's phase numbers are updated (the moved Imago rows now sit in Phases 21 and 27, and the suite release is Phase 40).

## Integration notes from the design pass

Findings the per-batch design agents reported that cross file boundaries; the integration commit resolves each.

- **Reciprocal XREFs.** Every file design's "Inputs and XREFs" line lists the sections in other files it consumes or feeds, with the reason. The integration commit adds the reciprocal line in each target, including the existing files `D00 T01` (`§7`), `D01 T01` (`§3`, `§4`), `D01 T02` (`§2`, `§3`), `D01 T03` (`§2` to `§7`), `D01 T04` (`§1`, `§2`), `D01 T05` (`§1` to `§4`), `D01 T06` (`§3`, `§5`, `§12`), `D01 T07` (`§1` to `§6`, and its Implementation Order gains `§7` to `§9`), `D02 T15 §11`, `D03 T10 §6`, `D03 T11` (`§2`, `§4`), `D03 T12 §3` (the ABR tip reader moved for `D04 T13 §3`), `D03 T13 §3`, `D03 T14 §6`, `D03 T15` (`§1`, `§4` to `§7`, `§9`, `§12`), `D03 T16 §1`, `D03 T17` (`§2`, `§5` to `§12`), `D03 T18` (`§6`, `§7`), `D03 T19` (`§2`, `§6`, `§8`, `§9`, `§14`, `§15`), `D03 T20` (`§1` to `§4`, `§6`, `§8`, `§9`), `D04 T01` (`§2`, `§4` to `§11`), `D04 T02` (`§1` to `§9`), `D05 T01` (`§1`, `§3`, `§4`), `D06 T01 §3`, and `D06 T02 §3` (one-sided XREFs are FATAL). Cross-references between the new files (for example `D04 T11 §2`'s token engine, used by import, export, slideshows, print, and web galleries) need their reciprocal lines inside the new files too.
- **Code moves, each the first item of the Lumen section named, with a `**Corrected 2026-09-27:**` note on the Imago section that built it:** Imago's codec readers and writers to `Photon.Core/Formats/` (`D04 T13 §1`, `§6`); PDFium (`D04 T13 §4`); the EXIF, IPTC, and XMP readers of `D03 T17 §10` (`D04 T08 §1`); the archive opener (`D04 T05 §12`), WIA acquisition (`D04 T07 §7`), screenshot capture (`D04 T07 §8`), and FluentFTP (`D04 T12 §9`) of `D03 T17 §12`; the contact-sheet engine of `D03 T18 §7` and, if still inside Imago, its PDF presentation builder (`D04 T12 §6`, `§11`); alignment, HDR, panorama, and focus merge with OpenCvSharp4 (`ImageAligner`, `MatBridge`, the HDR merger, `PanoramaStitcher`, `FocusMerger`) to `Photon.Core/Photo/` (`D04 T09 §16`); `GrabCut`, `GuidedFilter`, and the matting classes to `Photon.Core/Imaging/Segmentation/` and `VisionLocator` to `Photon.Core/AI/Vision/` (`D04 T10 §7`); `GenerationRequestBuilder`, `GenerationCompositor`, `ImageModelCaps`, and `UpscaleService` to `Photon.Core/AI/Images/` (`D04 T10 §8`); `DistractionFinder` (`D04 T10 §9`); `DepthEstimator` to `Photon.Core/AI/Depth/` (`D04 T10 §10`).
- **Corrected after the design pass:** `D01 T07 §9` moves nothing: Imago's 3D LUT readers are already planned in `src/Photon.Core/Imaging/Luts/` by `D03 T11 §4`, so the develop LUT stage reuses them and depends on that section.
- **Keys changed from the competitors, recorded in the viewer design:** `T` in the viewer opens the folder in Lumen's browse mode (IrfanView's thumbnails key), so the viewer's Insert Text moves to `Ctrl+T`; until `D04 T05 §1` ships in Phase 32, `T` opens the folder as a library filter over `D04 T01 §8`, and `D04 T05 §1` retargets it.
- **Decisions for the operator to confirm at integration:** (1) the original-file guard stays frozen for the viewer and the batch tools: no in-place save, no in-place lossless rotation, no metadata written into originals (see "The original-file guard holds everywhere"); (2) the second executable `Photon.Lumen.Viewer`; (3) PicaView's Explorer context-menu preview (LP-0031) needs an in-process COM shell extension, which `D04 T04 §7` plans as an optional project `Photon.Lumen.ShellPreview` with a fallback to the backlog if Explorer stability cannot be proven (the only other candidate new project); (4) the new dependencies, all GPL-3.0-compatible: OpenCvSharp4 in Lumen with the YuNet (MIT) and SFace (Apache-2.0) models, DjVuLibre (GPL-2.0-or-later), NTwain (MIT), ZXing.Net (Apache-2.0), NAudio (MIT), DocumentFormat.OpenXml (MIT), SSH.NET (MIT), libjpeg-turbo 3.1 for lossless JPEG transforms (IJG, BSD-3-Clause, zlib), and the bundled GeoNames (CC BY 4.0) and Natural Earth (public domain) data; (5) OpenStreetMap standard tiles as the default online map source under the OSMF tile usage policy, with the map fully usable offline; (6) MIT licensing for generated web-gallery templates; (7) idle and scheduled indexing through `Microsoft.Win32.TaskScheduler` (MIT) or a `schtasks.exe` fallback, recorded as a decision in `D04 T05 §2`.
- **Catalog rows the design agents flagged** (statuses unchanged; each is a candidate for a merge or reroute at authoring through `add-todo`, in the same commit as the section that owns it): near-duplicates LP-0290 and LP-0560 (reference view), LP-0420 and LP-0693 (automatic face detection), LP-0455 and LP-0456 (auto import), LP-0459 and LP-0461 (scan destination), LP-0273 and LP-0274 (auto advance), LP-0379 and LP-0382 (optimize catalog), LP-0592 against LP-0586 and LP-0590 (raw defaults), LP-1007 and LP-1013 (text files rendered as images, built once in `D04 T13 §4`), LP-1039 and LP-1042 (font sample rendering, built once in `D04 T13 §8`); GoPro GPR write (LP-1029, `D04 T13 §7`) needs the gpr SDK (Apache-2.0 or MIT) and could be B-050; saving thumbnails as image files (LP-0797, `D04 T11 §4`) could sit in `D04 T05 §4`; OCR is split between LP-0112 (`D04 T04 §9`, `Windows.Media.Ocr` first, a user-installed Tesseract optional) and LP-0722 (`D04 T10 §4`); FTP transfer is split between `D04 T12 §9` (LP-0866) and `§12` (LP-0870, LP-0871) over one client; viewer-only previews LP-0652 (Auto Lens) and LP-0635, LP-0636 (Light EQ) could move from develop to `D04 T04 §15`; disk file search LP-0357 to LP-0359 sits in `D04 T06 §7` but searches the disk; Photoshop Elements catalog import (LP-0389) and Office-document printing (LP-0948) could be `other-app: none`; the Store edition fragment of LP-1138 is not planned; LP-1086 (Edit in Imago as layers or a linked raw document) needs an Imago open-as-layers entry point no Imago section plans yet, so its hint degrades to one TIFF per photo until one exists; LP-0113 ("Tools plug-in: additional utility functions") is read as the viewer's Tools menu grouping.
- **Controls deferred by name to later phases** (legitimate, each names its owner): the viewer's `T` hand-off reaches browse mode in Phase 32 (`D04 T05 §1`); smart previews (`D04 T06 §11`, Phase 33) and DNG conversion (`D04 T07 §6`, Phase 34) wait on the DNG writer (`D04 T13 §7`, Phase 31); face tags in the metadata panel appear when `D04 T10 §3` ships (Phase 37); AI masks in the masking panel appear when `D04 T10 §7` ships; the keymap editor of `D04 T14 §3` (Phase 39) re-binds the default keys every earlier section registers.
- **Sizing watch list.** Sections with the densest catalog lines are the likeliest to pass 30 checklist items; each file design's "Sizing concerns" names the natural split: `D04 T04 §4`, `§5`, `§11`, `§14`; `D04 T05 §4`, `§6`; `D04 T06 §1`, `§5`, `§8`; `D04 T08 §2`, `§5`; `D04 T09 §9`, `§1`, `§2`; `D04 T10 §3`; `D04 T11 §2`, `§7`; `D04 T12 §5`, `§13`; `D04 T13 §3`. Phases have no size limit under the redesigned budget, so a split adds a section in the same phase.
- **AGENTS.md and standards.** Its `docs/parity/` row describes the Nodus and Imago evidence only; the integration extends it to name the Lumen inventories, catalog, and design, and `standards/lumen.md` gains the viewer project and the browse model.
- **Backlog ids named before they exist.** `lumen-parity.md` names B-048 to B-050, which become live entries in the integration commit; until then `D00 T01 §8` is not built, so nothing refuses them.

## Catalog check

`python check_lumen_catalog.py` (the scratch check, run 2026-09-27 against the files in this folder, this design, the live `todo/` tree, `todo/backlog.md`, and `imago-parity.md`; the rules `D00 T01 §8` turns into validator classes):

- Source ids: 1,857 Lightroom Classic, 5,182 ACDSee, 1,880 IrfanView, 8,919 in all; each source file's ids unique and sequential.
- Catalog rows: 1,620 (LP-0001 to LP-1620), ids unique and sequential: True.
- Source ids placed: 8,919 exactly once; missing 0; duplicated 0; unknown 0.
- Statuses: plan 1,070 (6,269 source rows); shipped-scope 52 (282 source rows); backlog 75 (529 source rows); excluded 24 (209 source rows); other-app 399 (1,630 source rows).
- Plan refs: 124 distinct sections, all designed here: True; shipped-scope refs: 16 distinct existing sections, all live: True; `other-app: Imago` rows: 396, every one naming an `IP-` row that exists in `imago-parity.md` (including the 18 added rows): True.
- Backlog ids named: B-012, B-041, B-042, B-043, B-044, B-047 (live today) and B-048, B-049, B-050 (the new entries drafted in "Backlog changes").
- Designed sections with no catalog row of their own: `D00 T01 §8`, `D01 T07 §7`, `D01 T07 §8`, `D01 T07 §9`, and the release sections `D04 T15 §1` to `§10` (the validator, the three engine stages whose features sit on their Lumen surfaces `D04 T09 §13` and `§14` and on IP-2385, and the releases).
- Every designed section's Catalog line equals its rows in the catalog (128 lines checked, 0 mismatches).
- Result: clean.

## File designs

### todo/00-workspace/TODO-01-dev-automation.md -- one new section in an existing file

- **Phase(s):** 0 (the workspace spine; the operator's 2026-09-27 budget redesign removes the per-phase ceilings for operator-directed planning, so `§8` sits beside `§6` and `§7` where the validator already lives)
- **Why here:** the Lumen catalog is plan data like `todo/` and like the Nodus and Imago catalogs `§6` and `§7` already police; the acceptance-bar aim that Lumen covers every Lightroom Classic, ACDSee, and IrfanView capability in its catalog needs the same gate before the first Lumen parity row (Phase 30) runs, and extending `§7`'s `CatalogSpec` table keeps one validator for three catalogs instead of a third script. The Lumen catalog also routes 396 rows into the Imago catalog (`other-app: Imago IP-####`), and 18 Imago rows (IP-2368 to IP-2385) exist only because of those routes, so the two catalogs must be checked against each other.

#### §8. The validator reads the Lumen parity catalog

- **Deliverable:** `validate` refuses a Lumen parity catalog that has drifted from its three sources, from the plan, or from the Imago catalog it routes into, exactly as `§6` and `§7` do for Nodus and Imago, and `query parity --catalog lumen` reports per-phase coverage of the Lumen parity phases.
- **Depends On:** §7
- **Phase:** 0
- **Surface:** no surface of its own (stdlib tooling run by `validate`, the commit hook, and CI)
- **Runs:** none
- **Catalog:** owns no catalog rows (it enforces them)
- **Source:** `-> SOURCE: parity-lumen-validator`
- **Hints:**
  - Context claims, true today and to be re-measured on the authoring day: `<!-- claim: exists docs/parity/lumen-parity.md -->` `<!-- claim: count "^\| LP-\d{4} \|" docs/parity/lumen-parity.md = 1620 -->` `<!-- claim: count "^\| LR-\d{4} \|" docs/parity/sources/lightroom-classic-15.5.1.md = 1857 -->` `<!-- claim: count "^\| AC-\d{4} \|" docs/parity/sources/acdsee-ultimate-2027.md = 5182 -->` `<!-- claim: count "^\| IV-\d{4} \|" docs/parity/sources/irfanview-4.76.md = 1880 -->` `<!-- claim: count "^\| IP-\d{4} \|" docs/parity/imago-parity.md = 2385 -->` `<!-- claim: count "LP-" scripts/todo-graph.py = 0 -->` `<!-- claim: absent scripts/todo-parity.py -->` (the module `§6` creates; re-measure as `exists` once `§6` ships).
  - Add the `lumen` entry to `§7`'s `CATALOGS` table in `scripts/todo-parity.py`: `docs/parity/lumen-parity.md`, row id `LP-####`, sources Lightroom `LR-####` (`docs/parity/sources/lightroom-classic-15.5.1.md`, column `Lightroom`), ACDSee `AC-####` (`docs/parity/sources/acdsee-ultimate-2027.md`, column `ACDSee`), and IrfanView `IV-####` (`docs/parity/sources/irfanview-4.76.md`, column `IrfanView`); `parse_catalog` finds the columns from each area table's header row `| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |`, so no Nodus or Imago code path changes behavior.
  - Self-check on today's files prints 1,857 `LR`, 5,182 `AC`, and 1,880 `IV` ids (8,919 in all) and 1,620 `LP` rows, beside `§6`'s and `§7`'s figures.
  - Run the six catalog-agnostic classes (`parity-id-missing`, `parity-id-duplicate`, `parity-id-unknown`, `parity-status-malformed`, `parity-ref-dead`, `parity-backlog-dead`) and `§7`'s `parity-totals-drift` once more for the `lumen` catalog with the `lumen:` prefix; add `parity-lp-duplicate` (an `LP-` id used twice), the counterpart of `parity-np-duplicate` and `parity-ip-duplicate`.
  - Add `parity-ip-route-dead`: an `other-app: Imago IP-####` status in the Lumen catalog must name an `IP-` row that exists in `docs/parity/imago-parity.md` and whose own status is not `other-app: Lumen` (no route loops); a Lumen row routed to Imago with no `IP-` id is `parity-status-malformed`. The message names the `LP-` row, the `IP-` id, and the reason.
  - Relax `parity-id-missing` for Imago rows with no source id in any column: such a row is valid only when its Notes name at least one `LP-` row whose status routes to it (today IP-2368 to IP-2385, added 2026-09-27 for ACDSee Edit mode); otherwise report the new class `parity-orphan-row` naming the `IP-` id. Document the rule in the module docstring.
  - Status grammar per `docs/parity/README.md` as it reads after the Lumen decision: `other-app:` accepts `Nodus`, `Imago`, `Lumen`, or `none`, `excluded:` accepts `cloud`, `platform`, and `removed`, and `shipped-scope` refs into `D04 T01`, `D04 T02`, `D01 T02`, and `D01 T07` resolve like any other ref; `D04 T02 §9`, relocated into Phase 39, stays live.
  - Backlog ids: `parity-backlog-dead` covers the ids the Lumen catalog uses today (B-012, B-041, B-042, B-043, B-044, B-047, B-048, B-049, B-050: 75 rows); the integration commit adds B-048 to B-050 before `validate` goes green, and the promoted Lumen entries (B-028 to B-032, B-034 to B-036) are deleted then, so a Lumen row naming one of them fails.
  - `query parity [--catalog nodus|imago|lumen|all] [--phase N] [--json]` gains `lumen`; the Lumen parity phases 30 to 39 quote `--catalog lumen --phase N`, and the `other-app: Imago` rows are reported as a separate "routed to Imago" count per Imago phase so the Imago releases see the Lumen-born rows they owe.
  - Add `parity-lp-duplicate`, `parity-ip-route-dead`, and `parity-orphan-row` to `SEVERITY_MAP` in `scripts/todo-graph.py` as `fatal` and their rows to the per-class table in `todo/README.md` in the same commit; skip the Lumen pass when `docs/parity/lumen-parity.md` is absent, as `§6` and `§7` skip theirs.
  - Self-test fixtures in the temporary tree: tiny Lightroom, ACDSee, and IrfanView sources, a four-row Lumen catalog with a Totals table and an Areas list, a two-row Imago catalog with one source-less row naming an `LP-` id, and a backlog carrying B-048; cases: one missing `AC` id, one duplicate `IV` id, one unknown `LR` id, one duplicate `LP-` id, one `other-app: Imago` row naming a dead `IP-` id, one source-less Imago row whose `LP-` reference does not route to it, one `excluded: cloud` row (clean), one dead backlog id (B-099), one Totals mismatch, and one clean catalog; one `query parity --catalog lumen --phase N --json` count.
  - Update the Enforcement paragraph of `docs/parity/README.md` to say `D00 T01 §8` is built and to list the three new classes and the `lumen` value of `--catalog`.
  - Commit: `"workspace: validate the Lumen parity catalog against its sources, the plan, and the Imago routes"`
- **Proof:** unit plus static: `python scripts/todo-graph.py self-test` reports `0 failed` with the Lumen cases counted; `validate` exits 0 on the integrated tree; deleting one `AC-` id from a scratch copy of `lumen-parity.md` makes `validate` exit 1 naming `lumen: parity-id-missing`, and changing one routed row to `other-app: Imago IP-9999` makes it exit 1 naming `parity-ip-route-dead`; `query parity --catalog lumen --phase 30 --json` prints the Phase 30 counts; cheaper substitute that fails: a copy of `§7`'s module hard-wired to the Lumen file, which the self-test's single-module import and the unchanged Nodus and Imago cases expose as a second implementation.

### todo/01-core/TODO-07-photon-develop.md -- three new sections in an existing file

- **Phase(s):** 36 (all three, before `D04 T09 §13` and `§14`)
- **Why here:** Light EQ, soft focus, skin tune, develop LUTs, blend modes, and looks are develop stages, and the suite rule is that every develop stage lives in `Photon.Core/Develop/` (`D04 T02 §2`'s grep forbids an `IDevelopStage` under `src/Lumen/`). Two consumers exist from the day they land: Lumen's panels (`D04 T09 §13`, `§14`) and Imago's Camera Raw filter and Develop studio (`D03 T15 §1`, `§12`), which list registered stages, plus the new Imago catalog row IP-2385 (Light EQ as a filter and adjustment layer on `D03 T11 §2`). They own no catalog rows; the Lumen rows sit on the surfaces.
- **Inputs and XREFs:** the existing file's inputs; ACDSee Photo Studio Ultimate 2027 user guide (Light EQ, soft focus, skin tune, develop effects) for behavior; darktable 5.0 tone equalizer as the published reference for band-based exposure; Adobe Cube LUT Specification 1.0; -> XREF: D04 T09 §13 (Light EQ, soft focus, skin tune panels); -> XREF: D04 T09 §14 (LUTs, blend, effects panels); -> XREF: D03 T15 §1 (the Camera Raw filter lists the new stages); -> XREF: D03 T11 §2 (IP-2385, Light EQ as an Imago adjustment); -> XREF: D03 T11 §4 (the LUT readers in `src/Photon.Core/Imaging/Luts/` §9 applies); -> XREF: D01 T06 §12 (glow and diffuse kernels §8 composes).

#### §7. The tone equalizer stage

- **Deliverable:** `ToneEqualizerStage` in `Photon.Core/Develop/Stages/`: exposure adjustment per tone band (nine bands over scene-referred luminance, smoothed by a guided filter so edges keep their contrast), brighten and darken amplitudes, contrast, an auto mode from the luminance histogram, and a band graph data source, with its settings group in `DevelopSettings`.
- **Depends On:** §1
- **Phase:** 36
- **Surface:** no surface of its own (engine; Lumen's panel is `D04 T09 §13`)
- **Runs:** none
- **Catalog:** owns no catalog rows (Lumen's LP-0635 to LP-0637 sit on `D04 T09 §13`; Imago's IP-2385 on `D03 T11 §2`)
- **Source:** `-> SOURCE: parity-lumen-tone-equalizer`
- **Hints:**
  - `ToneEqualizerSettings` (bands as exposure offsets in EV at centers from -8 EV to 0 EV, brighten and darken amplitude, contrast, mode Basic, Standard, Advanced as UI hints only) added to `DevelopSettings` with a schema version bump and identity defaults.
  - Luminance mask via guided filter (He, Sun, and Tang 2013, the `GuidedFilter` of `D01 T06`) at a radius relative to image size, so preview and export agree.
  - Stage position after exposure and before the tone curve; SIMD path with a scalar reference within 1e-5.
  - `AutoToneEqualizer` from the luminance histogram, deterministic.
  - Tests: `ToneEqualizerStageTests` (identity at defaults within 1/65535, a +1 EV shadow band lifts only shadows), `ToneEqualizerResolutionTests` (preview and full agree within 1/255 after resampling).
  - Register in the stage registry so `D03 T15 §1` lists it.
  - Commit: `"core: the tone equalizer develop stage"`
- **Proof:** unit: the tests pass with the scalar and SIMD paths compared; cheaper substitute that fails: a curve preset, which cannot lift a band independently of edges.

#### §8. Soft focus, glow, and skin tune stages

- **Deliverable:** `SoftFocusStage` (strength, brightness, contrast, tonal width) and `SkinTuneStage` (smoothing, glow, radius, with an optional mask input from `§4`) in `Photon.Core/Develop/Stages/`, composing existing blur and glow kernels.
- **Depends On:** §1, D01 T06 §12
- **Phase:** 36
- **Surface:** no surface of its own (engine; Lumen's panel is `D04 T09 §13`)
- **Runs:** none
- **Catalog:** owns no catalog rows (LP-0638 and LP-0639 sit on `D04 T09 §13`)
- **Source:** `-> SOURCE: parity-lumen-soft-focus`
- **Hints:**
  - Soft focus as a screen or soft-light blend of a Gaussian-blurred copy weighted by a tonal-width luminance window; glow as the highlights-only variant.
  - Skin tune as edge-preserving smoothing (bilateral or guided filter) plus a glow term, limited by an optional mask component.
  - Radii in normalized image units so preview and export agree.
  - Tests: `SoftFocusStageTests`, `SkinTuneStageTests` (identity at zero, resolution agreement within 1/255).
  - Register both in the stage registry.
  - Commit: `"core: soft focus, glow, and skin tune develop stages"`
- **Proof:** unit: tests pass; cheaper substitute that fails: a plain blur, which the tonal-width test distinguishes.

#### §9. Develop LUTs, blend modes, and looks

- **Deliverable:** `LookStage` in `Photon.Core/Develop/Stages/` applying a 3D LUT (read by `src/Photon.Core/Imaging/Luts/`, which `D03 T11 §4` builds) or a named look (color overlay, gradient map, cross process) with amount, opacity, and a blend mode from the suite blend math, in the output-referred part of the pipeline.
- **Depends On:** §1, D03 T11 §4
- **Phase:** 36
- **Surface:** no surface of its own (engine; Lumen's panel is `D04 T09 §14`)
- **Runs:** none
- **Catalog:** owns no catalog rows (LP-0640 to LP-0642 sit on `D04 T09 §14`)
- **Source:** `-> SOURCE: parity-lumen-develop-looks-stage`
- **Hints:**
  - Reuse `D03 T11 §4`'s `.cube` and `.3dl` readers from `src/Photon.Core/Imaging/Luts/` (already shared; no move needed) with tetrahedral interpolation; LUT identity by file hash stored in settings with the path, missing LUT reported by name and bypassed.
  - Blend modes normal, screen, multiply, dodge, burn, overlay, difference, darken, lighten, hard and soft light, hue, saturation, color, luminosity, dissolve (seeded), exclusion, from the suite blend definitions.
  - Looks as JSON definitions in `Photon.Core/Develop/Looks/` authored for the suite (no vendor looks).
  - Tests: `LookStageTests` (identity LUT is identity within 1/65535; amount 0 is identity; a known CUBE fixture matches a reference within 1/255), `MissingLutTests`.
  - Commit: `"core: develop LUT, blend, and look stage"`
- **Proof:** unit: tests pass; cheaper substitute that fails: a second LUT reader, which a grep for `.cube` parsing outside `Imaging/Luts/` catches.

### todo/04-lumen/TODO-04-lumen-viewer.md -- `lumen-viewer`

- **Title:** "TODO-04 -- Lumen Parity: the Fast Default Viewer"
- **Phase(s):** 30 (§1 to §10, §14), 31 (§11 to §13, §15, §16)
- **Goal:** Lumen ships an IrfanView-class image viewer: `LumenViewer.exe`, a second executable in the Lumen install with its own minimal startup path, opens any image the suite reads in milliseconds from Explorer, can be registered as the Windows default viewer for every format it reads, browses the file's folder with prefetch, shows images at any zoom with correct orientation and display color, plays multi-page and animated files, runs fullscreen and quick slideshows, shows information, histogram, pixel values, QR codes, and text, performs file operations, and offers quick edits (rotate, crop, resize, color, effects, text, watermark, borders, lossless JPEG transforms) that run the batch engine's operations and always save to a new file; the Lumen library is one keystroke away. The code lives in `src/Lumen/Photon.Lumen.Viewer/` (the WPF exe, AssemblyName `LumenViewer`) and `src/Lumen/Photon.Lumen.Core/Viewer/`; it decodes only through the shared `Photon.Core/Formats/` registry (`D04 T13 §1`), applies display color through `D01 T04`, applies quick edits through `D04 T11 §7`'s `IBatchOperation` implementations and the `Photon.Core` effect registry (`D01 T03`, `D01 T06`), forwards to `Lumen.exe` through `D01 T02 §3`, and never writes an original image.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code at all, so there is no viewer project. `<!-- claim: absent src/Lumen -->`
  - The app manifest still names the legacy project path and marks Lumen as not shipping, so the viewer exe has no publish entry yet. `<!-- claim: count "src/Lumen/Lumen.UI/Lumen.UI.csproj" scripts/apps.psd1 = 1 -->` `<!-- claim: count "Shipping  = \$false" scripts/apps.psd1 = 1 -->`
  - The Lumen installer refuses to compile without its guard and registers no file type, which §3 changes. `<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->` `<!-- claim: count "assoc_" installer/Lumen.iss = 0 -->` `<!-- claim: count "ChangesAssociations=yes" installer/common.iss = 1 -->`
  - The original-file guard the quick edits obey is frozen in the Lumen standard. `<!-- claim: count "Lumen never writes an original image" standards/lumen.md = 1 -->`
  - Nothing in the repository registers a Windows capabilities key or sets a wallpaper yet. `<!-- claim: count "RegisteredApplications" src/**/*.cs = 0 -->` `<!-- claim: count "IDesktopWallpaper" src/**/*.cs = 0 -->`
- **Inputs and XREFs:** `standards/lumen.md` (the original-file guard), `standards/shared.md` (window anatomy, performance budgets), `standards/testing.md`; `docs/parity/lumen-section-design.md` ("The viewer architecture", the budgets) and `docs/parity/lumen-parity.md` (LP-0001 to LP-0178 and the rows named per section); IrfanView 4.76 (i_view64.exe, driven for behavior and key parity, version recorded), ACDSee Photo Studio Ultimate 2027 View mode and Quick View (from its user guide), Microsoft Learn: "Default Programs" and "Registering an Application for Use in Windows" (Capabilities, `RegisteredApplications`, `OpenWithProgids`), `IDesktopWallpaper`, `Windows.Media.Ocr`; the IJG `jpegtran` lossless transform (libjpeg-turbo 3.1, IJG and BSD-3-Clause) as the reference for §16; ZXing.Net 0.16 (Apache-2.0); NAudio 2.2 (MIT); -> XREF: D04 T02 §8 (Lumen 0.1.0 ships before every section here); -> XREF: D01 T02 §3 (single instance and file-open forwarding for the resident mode and the hand-off to Lumen); -> XREF: D01 T04 §1 (display color transforms for §2); -> XREF: D01 T03 §2 (resampling and rotation for §4, §11, §14); -> XREF: D01 T03 §3 (quantization and dithering for §12); -> XREF: D01 T03 §6 and D01 T03 §7 (effects the §15 browser lists); -> XREF: D01 T06 §5 (JPEG artifact reduction for §2's deblocking); -> XREF: D01 T07 §9 (the LUT stage behind §15's film simulation); -> XREF: D04 T01 §4 (the RAW decoder and embedded previews §2 consumes); -> XREF: D04 T01 §8 (the library grid §1 opens photos from); -> XREF: D04 T02 §7 (Edit in Imago from the viewer); -> XREF: D04 T05 §1 (browse mode, the target of the `T` key once it ships; until then `T` opens the folder filter of the library grid); -> XREF: D04 T11 §2 (the token engine for fullscreen text, captions, and inserted text); -> XREF: D04 T11 §7 (the batch operations the quick edits apply); -> XREF: D04 T11 §8 (the watermark engine §13 uses); -> XREF: D04 T12 §4 (printing a selection or the current image goes through Lumen's print module); -> XREF: D04 T13 §1, D04 T13 §2, D04 T13 §3, D04 T13 §4, D04 T13 §5, D04 T13 §8 (the codec registry and the formats §2, §3, and §10 display and register); -> XREF: D04 T14 §3 (the keymap editor the viewer's default keys register with); -> XREF: D04 T15 §1 and D04 T15 §2 (the releases that ship this file's phases).
- **Adjacency:** list=applicable (the folder file list and position box in §5, the quick slideshow list in §8, recent files in §5); document=applicable @ D04 T12 §4 (printing from the viewer goes to the print module); settings=applicable (every viewer option is a `Lumen.Viewer.*` key with a default and a named consumer); reporting=applicable (image information, histogram, pixel values, and status fields in §9); notifications=applicable (decode failures name the format and decoder; slideshow end and folder end prompts); permissions=applicable (read-only folders and locked files refused by name on move, rename, and delete; the original is never opened for writing); audit=applicable (one Serilog Information line per file operation and per saved new file); exchange=applicable (clipboard image and path, drag and drop, Save As in every writable format, TXT slideshow lists, PAL palettes); reverse=applicable (quick-edit undo and redo in §11, file operations undone through the Recycle Bin, orientation reset)

#### §1. The Lumen Viewer: a second executable with a startup budget and the hand-off to Lumen

- **Deliverable:** `LumenViewer.exe` exists as a second executable in the Lumen install, starts decoding before its window exists, meets the recorded cold, warm, and resident budgets with a committed assembly allow-list at first paint, opens the files named on its command line, handles single or multiple windows, offers an optional resident quick-start mode with a notification-area icon, and hands the current photo to Lumen with one key.
- **Depends On:** D04 T02 §8, D04 T13 §1, D01 T02 §3
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer/. Job: a user double-clicks a photo in Explorer and sees it before they notice a window opening, and reaches the library, browse, develop, or Imago from it with one key. Treatment: a borderless-feeling window with the image, a slim bottom toolbar, and a status strip; `Esc` closes; `T` opens the folder in Lumen, `Ctrl+L` opens the photo in the library, `Ctrl+E` hands it to Imago; the resident mode shows a notification-area icon with Open and Exit. Cheaper substitute that fails: launching `Lumen.exe` with a loupe, which pays for the catalog and module shell and misses the budget. Chrome: consume `Photon.UI` theme and dialog styles and `Photon.Core` settings, logging, and single instance; build no DI container before the first paint.
- **Runs:** `Requires: display-session -- the startup harness launches the published viewer and times its first rendered frame`
- **Catalog:** LP-0001 to LP-0008 (8 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-exe`
- **Hints:**
  - Create `src/Lumen/Photon.Lumen.Viewer/Photon.Lumen.Viewer.csproj` (`net11.0-windows10.0.26100.0`, WPF, `AssemblyName` `LumenViewer`, `PublishReadyToRun` and `TieredPGO` on) referencing `Photon.Core`, `Photon.UI`, and `Photon.Lumen.Core`; add it to `Photon.slnx`, to `scripts/apps.psd1`'s Lumen entry as an extra exe published into the same folder, and to `installer/Lumen.iss` (Start menu entry "Lumen Viewer") (LP-0002, LP-0005).
  - `ViewerProgram.Main`: parse arguments, start `ViewerDecodeService.DecodeForScreenAsync(path)` on the thread pool, then create the WPF `Application` and `ViewerWindow` in parallel; show the first frame when the screen-size decode completes; construct dialog services lazily; open one or several files given on the command line (LP-0008, the plain open only; other switches are B-041).
  - Startup harness `tests/Photon.Lumen.Tests/Viewer/ViewerStartupTests` plus a `--startup-trace` switch that logs process start, window created, and first `CompositionTarget.Rendering` with the image; `docs/dev/lumen/viewer-budgets.md` records the reference machine and the budgets: cold at most 450 ms, warm at most 250 ms, resident hand-off at most 100 ms, RAW embedded preview at most 200 ms, working set at most 200 MB for 24 megapixels (LP-0005).
  - `ViewerAssemblyAllowListTests`: at first paint `AppDomain.CurrentDomain.GetAssemblies()` matches the committed list in `tests/fixtures/lumen/viewer/first-paint-assemblies.txt` (no `Microsoft.Data.Sqlite`, no catalog assembly); a change to the list fails with the added names.
  - Window instances (LP-0004, LP-0007): `Lumen.Viewer.SingleInstance` (default on) forwards later opens to the running viewer through `D01 T02 §3`, otherwise a new window opens; Open in New Window for the current file.
  - Exit behavior (LP-0006): `Esc` closes, `Lumen.Viewer.WarnOnEscExit`, ask to save unsaved quick edits (Save As, §6), double-click on the image closes when `Lumen.Viewer.DoubleClickCloses` is on.
  - Resident mode (LP-0003): `Lumen.Viewer.StayResident` (default off) registers `LumenViewer.exe --resident` under `HKCU\...\Run`, keeps a hidden window and a notification-area icon (`System.Windows.Forms.NotifyIcon` avoided: a WPF `Shell_NotifyIcon` P/Invoke wrapper in `Photon.Lumen.Viewer/Tray/`), and the settings page states the memory it holds.
  - Hand-off (LP-0001): `ViewerHandoff` starts or forwards to `Lumen.exe` with `--browse <folder> --select <file>` (`T`), `--library <file>` (`Ctrl+L`), `--develop <file>`, or Edit in Imago (`Ctrl+E` through `D04 T02 §7`); Lumen's grid and loupe open the selected photo in the viewer with `F3` and return with `Esc`; until `D04 T05 §1` ships, `--browse` opens the library grid filtered to the folder.
  - Tests: `ViewerArgumentsTests` (paths with spaces, several files, unknown switches ignored with a log line), `ViewerHandoffTests` with a fake launcher and forwarder.
  - Commit: `"lumen: the Lumen Viewer as a fast second executable with a startup budget"`
- **Proof:** driven run with evidence plus unit: the startup harness quotes cold, warm, and resident timings for the 24-megapixel JPEG fixture on the reference machine under budget, `ViewerAssemblyAllowListTests` passes, and a driven `T` from the viewer selects the photo in Lumen (capture); cheaper substitute that fails: a loupe window inside `Lumen.exe`, which the assembly allow-list test and the cold-start timing both catch.

#### §2. The viewer decode path: screen-size decode, prefetch, and display color

- **Deliverable:** the viewer shows the first pixels of any readable file from a screen-size or embedded-preview decode, sharpens progressively to the full decode, prefetches the next and keeps the previous image, rotates by EXIF, applies DNG opcode geometry, shows developed or original versions, color-manages tagged and untagged images to the monitor profile, optionally deblocks JPEGs, and names the format and decoder when a file fails.
- **Depends On:** §1, D04 T13 §2, D04 T13 §5, D01 T04 §1
- **Phase:** 30
- **Surface:** UI. Fidelity: docs/captures/lumen/viewer/ (baseline from §1). Job: a user browsing a folder never waits on decoding, sees colors as the photographer intended, and sees why a file will not open. Treatment: a toolbar toggle between RAW embedded preview and RAW decode, press and hold `O` (configurable) for the original, a status-strip badge "Preview" until the full decode lands, and an in-window error panel naming the file, format, and decoder. Cheaper substitute that fails: decoding every file at full resolution on the UI thread. Chrome: consume the `Photon.Core/Formats/` registry's screen-size capability, `D04 T01 §4`'s decoder, and `D01 T04 §1`'s transforms; no viewer-private decoder.
- **Runs:** `Requires: display-session -- display color and next-image timings are measured on screen`
- **Catalog:** LP-0009 to LP-0023 (15 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-decode`
- **Hints:**
  - `ViewerDecodeService` in `Photon.Lumen.Core/Viewer/`: asks the registry for `DecodeOptions.TargetSize` = monitor size, uses JPEG DCT scaling, JPEG 2000 and JPEG XL reduced levels, and RAW embedded previews where the codec offers them, then schedules the full decode; progressive display (LP-0016).
  - RAW display modes (LP-0009, LP-0014): embedded preview (default), half size, or full decode through `D04 T01 §4`, switched by toolbar and `Lumen.Viewer.RawMode`, with automatic full decode when zooming past the preview.
  - `PrefetchCache` (LP-0015): decode the next image in browse direction and keep the previous one, bounded by `Lumen.Viewer.PrefetchMB` (default 512), cancelled on direction change; next or previous at most 50 ms from the cache and at most 150 ms uncached (quoted).
  - Orientation (LP-0013) from EXIF and from the catalog and sidecar orientation `D04 T04 §16` stores; DNG opcode geometry (LP-0011): `WarpRectilinear` and `FixVignetteRadial` opcodes applied for display.
  - Developed versus original (LP-0010): when the photo has a catalog edit stack or a sidecar with develop settings, render through `D01 T07`'s pipeline at screen size; press and hold shows the original.
  - Display color (LP-0017, LP-0021, LP-0023): tagged images convert from their profile, untagged as sRGB (setting), to the monitor profile read per monitor through `D01 T04 §1`; option to apply the profile to pixels on save (§6).
  - Display gamma (LP-0012) and legacy load-as-grayscale (LP-0018) as display-only options `Lumen.Viewer.DisplayGamma` and `Lumen.Viewer.LoadAsGray`.
  - JPEG deblocking and quantization smoothing on load (LP-0020, LP-0022) through `D01 T06 §5`, off by default.
  - Typed failure (LP-0019): "Lumen Viewer cannot open <name>: <format> is not supported by <decoder> <version>" in the window and the log.
  - Tests: `ViewerDecodeServiceTests` (target size honored per codec family, orientation 1 to 8 fixtures, cancellation), `PrefetchCacheTests`, `ViewerColorTests` (a Display P3 tagged fixture maps to known sRGB values within delta E 1).
  - Commit: `"lumen: the viewer decode path with prefetch and display color"`
- **Proof:** unit plus driven: the tests pass, next and previous timings over a 200-file folder are quoted under budget, and captures show a P3 fixture and an orientation 6 fixture correct; cheaper substitute that fails: full-resolution decode per image, which the next-image timing catches.

#### §3. Default viewer registration and shell integration

- **Deliverable:** Lumen Viewer registers as a capable application for every extension the codec registry reads, lets the user choose which format groups to register, hands off to Windows Default Apps to become the default viewer, and adds Explorer verbs (Open with Lumen Viewer, Browse with Lumen, Send To, and context operations), without ever writing a `UserChoice` key.
- **Depends On:** §1, D04 T13 §3, D04 T13 §4, D04 T13 §8
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-associations/. Job: a user makes Lumen Viewer their photo viewer for every format in two clicks and can undo it. Treatment: an Associations page with format groups (images, RAW, documents, archives) and per-extension checkboxes, All, Images only, Clear, custom extensions, all-users option when elevated, and a "Make Lumen Viewer the default" button that opens `ms-settings:defaultapps?registeredAppUser=Lumen%20Viewer`; a second-launch prompt offering it once. Cheaper substitute that fails: writing `UserChoice`, which Windows rejects by hash and resets. Chrome: consume the settings page frame of `D04 T14 §4` when it ships (the page opens standalone before), `Photon.UI` dialog styles, and the icon catalog.
- **Runs:** `Requires: display-session -- the Default Apps hand-off and Explorer verbs are driven on a desktop`
- **Catalog:** LP-0024 to LP-0028 (5 features)
- **Source:** `-> SOURCE: parity-lumen-default-viewer`
- **Hints:**
  - `ShellRegistration` in `Photon.Lumen.Core/Viewer/Shell/`: writes `HKCU\Software\RegisteredApplications\Lumen Viewer` to `Software\Rizonesoft\LumenViewer\Capabilities` with `ApplicationName`, `ApplicationDescription`, and `FileAssociations` for each chosen extension, per-family ProgIDs (`LumenViewer.jpeg`, `LumenViewer.raw`, `LumenViewer.document`, and so on) with icons, and `OpenWithProgids` values; `HKLM` variants only when elevated and "all users" is ticked (LP-0026).
  - Extension list comes from the registry (`CodecRegistry.ReadableExtensions`), so a format added later appears automatically; format groups and associate or disassociate per group (LP-0025).
  - Per-format icons (LP-0028): a small icon set in `resources/icons/lumen-viewer/` (image, RAW, document, archive), drawn in house, recorded in `resources/icons/README.md`.
  - Default hand-off (LP-0024): the button and the one-time second-launch prompt (`Lumen.Viewer.DefaultPromptShown`) open the Default Apps page; the page states that Windows asks the user to confirm.
  - Explorer verbs (LP-0027): `Browse with Lumen` on folders and drives, `Open with Lumen Viewer`, a Send To shortcut, and context entries for slideshow (§8), batch (`D04 T11 §10`), lossless rotation (§16), and copying a file-name list, all as static verbs in the registry (no COM extension).
  - Installer: `installer/Lumen.iss` gains an unchecked task "Register Lumen Viewer for image types" that runs `LumenViewer.exe --register` and uninstall runs `--unregister`, removing every value it wrote.
  - `SHChangeNotify(SHCNE_ASSOCCHANGED)` after each change so Explorer refreshes icons.
  - Tests: `ShellRegistrationTests` against a redirected registry root (`RegistryKey` under a temp `HKCU\Software\PhotonTests` hive), asserting register then unregister leaves no value behind and `UserChoice` is never touched.
  - Commit: `"lumen: register Lumen Viewer for every format it reads and hand off to Default Apps"`
- **Proof:** unit plus driven: `ShellRegistrationTests` pass; on a clean user profile the installer task registers the capabilities, the Default Apps page lists Lumen Viewer, and after the user sets it a double-click on a `.heic` and a `.cr3` opens the viewer (captures); cheaper substitute that fails: `UserChoice` writes, which Windows resets on the next open.

#### §4. Zoom, fit, pan, magnifier, and navigator

- **Deliverable:** the viewer zooms by every competitor gesture and dialog with fit modes, zoom and pan locks, view rotation, a navigator, and a magnifier, all without touching the file.
- **Depends On:** §2
- **Phase:** 30
- **Surface:** UI. Fidelity: docs/captures/lumen/viewer/ (baseline from §1), new captures to docs/captures/lumen/viewer-zoom/. Job: a user checks focus and detail at any scale and keeps the same view while stepping through a burst. Treatment: `+`, `-`, `Ctrl` plus wheel at the pointer, click to toggle 100 percent, a zoom value box and slider with presets, a Zoom To dialog, fit modes on number keys, `L` locks zoom and scroll, navigator pane and overlay, magnifier on `M`, view rotation on `Ctrl+Alt+Left` and `Right`. Cheaper substitute that fails: fit and 100 percent only. Chrome: consume `D01 T03 §2` resampling for display tiles and the theme.
- **Runs:** `Requires: display-session -- zoom and pan are driven on screen`
- **Catalog:** LP-0033 to LP-0043 (11 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-zoom`
- **Hints:**
  - `ViewportModel` in `Photon.Lumen.Core/Viewer/` (zoom, offset, rotation, fit mode) with pure math tests; zoom steps from a fixed table or a step factor, centered zoom, zoom calculation per `Lumen.Viewer.ZoomStepMode` (LP-0043).
  - Zoom commands (LP-0036, LP-0041): in, out, slider, preset list, Zoom To dialog with a typed percentage, click toggles actual size, `Ctrl` plus wheel zooms at the pointer; a zoom value box in the status strip.
  - Fit modes (LP-0038): fit image, width, height, smaller side, reduce only, enlarge only, reduce or enlarge, default mode, fit toggle key.
  - Zoom defaults (LP-0040): reset on image change or keep, auto shrink or enlarge, click zooming, pan speed; zoom and pan lock across images (LP-0037).
  - Pan (LP-0035): hand drag, right-button drag when §14's right-button option says scroll, arrows with `Shift` and `Ctrl` speeds, numeric keypad jumps to edges and corners, horizontal wheel.
  - Navigator (LP-0034): a pane and a quick overlay with magnification slider and draggable marquee; magnifier (LP-0033, LP-0042): on-image lens or pane with fixed or relative magnification and smooth or pixel display, also in fullscreen (§7).
  - Temporary view rotation (LP-0039) is view state only and never enters the file, the catalog, or the sidecar.
  - Tests: `ViewportModelTests` (fit modes on landscape and portrait fixtures, pointer-anchored zoom keeps the pointed pixel, locks survive image change).
  - Commit: `"lumen: viewer zoom, fit, pan, navigator, and magnifier"`
- **Proof:** unit plus driven: `ViewportModelTests` pass and a driven session zooms at the pointer, locks zoom across a burst, and uses the magnifier (captures); cheaper substitute that fails: fit and 100 percent only, which the fit-mode tests catch.

#### §14. Viewer window and display options

- **Deliverable:** the viewer window's layout, chrome, background, transparency display, display resampling quality, window sizing and placement, channel view, grid overlay, and always-on-top and boss-key behavior are complete and each is a setting.
- **Depends On:** §4
- **Phase:** 30
- **Surface:** UI. Fidelity: docs/captures/lumen/viewer/ (baseline from §1), new captures to docs/captures/lumen/viewer-display/. Job: a user shapes the viewer into a minimal IrfanView-style window or a panelled ACDSee-style one. Treatment: a bottom toolbar with icon sizes and add or remove buttons, an optional filmstrip, hide menu or caption permanently or per session (`Shift+Enter`), thin border, background color, tiled image, or theme color, checkerboard transparency, fit window to image or desktop, remember size and position, show one channel on `Shift+R`, `G`, `B`, `A`. Cheaper substitute that fails: a fixed window. Chrome: consume `Photon.UI` theme resources for every color and size; no hardcoded values.
- **Runs:** `Requires: display-session -- window layouts are captured on screen`
- **Catalog:** LP-0062 to LP-0075 (14 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-window`
- **Hints:**
  - Layout (LP-0062): image area, bottom toolbar (icon size small, medium, large; customize buttons), filmstrip of the folder, hide bottom panels; settings `Lumen.Viewer.Toolbar.*`.
  - Chrome (LP-0068): hide menu or caption permanently or per session, toolbar, thin border; right button opens the context menu or scrolls (LP-0069).
  - Background (LP-0065, LP-0066): default, custom color, tiled image, main window color, and image centering; transparency display (LP-0074): checkerboard, window color, or discard, including non-animated GIF transparency.
  - Display resampling quality (LP-0064): smooth fit and zoom (`D01 T03 §2` Lanczos for downscale), show pixels above 100 percent, sharpen subsampled display, refresh with resample after a pause.
  - Window sizing (LP-0073): fit window to image, fit to desktop, desktop width, height, or smaller side, only for big images; placement (LP-0075): center on load, remember size and position per monitor.
  - Always on top and the boss key (LP-0063, LP-0067): `Lumen.Viewer.AlwaysOnTop`; a key minimizes and hides the viewer.
  - Fixed grid overlay (LP-0070) with spacing and color; clear the display without closing the file list (LP-0071); show one channel in color or gray (LP-0072) as a display transform.
  - Tests: `ViewerWindowSettingsTests` (each setting persists and applies), a pixel test that the checkerboard renders under a transparent PNG fixture.
  - Commit: `"lumen: viewer window, chrome, and display options"`
- **Proof:** unit plus driven: the tests pass and captures show the minimal and panelled layouts, the checkerboard, and a single-channel view; cheaper substitute that fails: a fixed layout, which the settings round trip catches.

#### §5. Browsing a folder in the viewer

- **Deliverable:** the viewer browses the opened file's folder and beyond with next, previous, first, last, random, skip, jump, a position box with a pattern filter, sorting, loop rules, drag and drop, recent files and folders, a watched hot folder, and the modern open dialog.
- **Depends On:** §2
- **Phase:** 30
- **Surface:** UI. Fidelity: docs/captures/lumen/viewer/ (baseline from §1). Job: a user steps through a folder or a card the way IrfanView does, including photos arriving from a tethered camera utility. Treatment: `Space` and `Backspace`, arrows, `Home`, `End`, `Page Up`, `Page Down`, `Ctrl+M` for random, a position box "12 / 340", browse buttons over the image, File, Open Recent, and View, Hot Folder. Cheaper substitute that fails: next and previous in name order only. Chrome: consume the registry's readable-extension list, a large-fetch enumeration, and `FileSystemWatcher`.
- **Runs:** `Requires: display-session -- folder browsing is driven on screen`
- **Catalog:** LP-0044 to LP-0058, LP-0252 (16 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-browse`
- **Hints:**
  - `FolderFileList` in `Photon.Lumen.Core/Viewer/`: enumerates the folder with `FindFirstFileEx` (large fetch), filtered to associated, custom, or all readable types (LP-0055), sorted by name, natural, date, EXIF date, size, extension, or none with direction (LP-0053); continue into the next folder at the end (LP-0047).
  - Navigation (LP-0045, LP-0252): next, previous, first, last, random, skip by N, `Home`, `End`, `Page Up`, `Page Down`, browse buttons over the image; options (LP-0057): include other files, hidden files, folder-end dialog, loop, or stop, beep, wheel browsing, always jump on page or wheel; keep the pointer on browse buttons after the window moves (LP-0056).
  - Position box (LP-0051): index of total, jump by index or page, filter by pattern such as `*2026*`.
  - Drag and drop (LP-0046, LP-0050): dropped files replace or join the list, drag the current file out to another program.
  - Reopen and refresh (LP-0049); recent files and recently saved files with clearing, recent folders in dialogs (LP-0052, LP-0058).
  - Open dialog (LP-0048): the modern `IFileOpenDialog` with the registry's format filter and preview, recent folders.
  - Watched folders (LP-0044, LP-0054): View, Hot Folder follows a folder with `FileSystemWatcher`, shows new images immediately or appends, waits until a file stops growing, includes subfolders, clears after a delay.
  - Tests: `FolderFileListTests` (natural sort, EXIF date sort from fixtures, pattern filter, hidden-file option, end-of-folder rules), `HotFolderTests` with a temp folder and a slowly written file.
  - Commit: `"lumen: folder browsing, recent files, and hot folders in the viewer"`
- **Proof:** unit plus driven: the tests pass and a driven session browses a 1,000-file folder by keys, jumps by pattern, and shows a file copied into a hot folder within 1 second (quoted); cheaper substitute that fails: name order only, which the sort tests catch.

#### §6. File operations and hand-offs in the viewer

- **Deliverable:** from the viewer a user deletes to the Recycle Bin, renames, copies or moves to destination slots, copies the image or its name to the clipboard, pastes, saves quick-edit results as new files, sets the wallpaper from a copy, and opens the file in external editors or its Windows-associated app, with sidecars following every file operation and the original never written.
- **Depends On:** §5
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-files/. Job: a user culls a card from the viewer alone and never loses or overwrites an original by accident. Treatment: `Del` to the Recycle Bin with an optional prompt, `Shift+Del` permanent behind a confirmation, `F2` rename, `F7` move and `F8` copy with destination slots, `Ctrl+C` image, `Ctrl+Shift+C` path, `Ctrl+S` opening Save As with a suggested new name, Set as Wallpaper, Open With, External Editors 1 to 3. Cheaper substitute that fails: Save overwriting the file. Chrome: consume `D04 T13 §6`'s writers when they ship (JPEG, PNG, and TIFF through the registry before), `Photon.Core`'s `AtomicFileWriter`, `SHFileOperation` or `IFileOperation` for the Recycle Bin.
- **Runs:** `Requires: display-session -- file operations are driven from the viewer window`
- **Catalog:** LP-0029 to LP-0030, LP-0116 to LP-0121, LP-0175 to LP-0178 (12 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-files`
- **Hints:**
  - `ViewerFileOperations` in `Photon.Lumen.Core/Viewer/Files/` over `IFileOperation` (Recycle Bin, undo in Explorer's own history): delete with sidecars (`.xmp` and RAW+JPEG partner by base name), permanent delete behind a confirmation, jump to next or return to browse after delete or move (LP-0175, LP-0120).
  - Rename (LP-0178) renames sidecars with the same base name, keeps the list index, and retries on sharing violation; the catalog record follows through `D04 T05 §6` once it ships.
  - Copy and move to (LP-0177): up to ten destination slots and recent folders, relative paths, shortcut-only copy, duplicate on name clash, a replace dialog with both previews.
  - Clipboard (LP-0176, LP-0119): copy the image as `CF_DIBV5` and PNG, copy the file name or full path, clear; paste into the viewer as a new unsaved image or into a selection proportionally or at original size, with a name pattern.
  - Save (LP-0118, LP-0121): Save always opens Save As with `<name>-edit.<ext>` suggested, format by type or extension, keep the original date and time option, recent save folders, overwrite prompt; a path equal to the opened original is refused with "Lumen never overwrites an original. Choose a new name." (the original-file guard).
  - Wallpaper (LP-0116, LP-0117): `IDesktopWallpaper` with centered, fill, tiled, stretched, proportional, span, monitor choice, restore previous, confirmation; the image is written as a copy under `%LOCALAPPDATA%\Rizonesoft\Lumen\wallpaper\`.
  - External editors (LP-0029): up to three configured editors named in the menu and toolbar, launched with the current path; Open With the associated app and shell Edit (LP-0030).
  - Tests: `ViewerFileOperationsTests` in a temp folder (delete takes the sidecar, rename renames the partner, move into a read-only folder refused by name), `ViewerSaveGuardTests` (saving onto the opened path is refused; every fixture's hash unchanged after a session).
  - Commit: `"lumen: viewer file operations, save as new file, wallpaper, and external editors"`
- **Proof:** unit plus driven: the tests pass, the unchanged-originals assertion holds over a driven session of delete, rename, move, quick-edit Save As, and wallpaper (hash table quoted); cheaper substitute that fails: Save in place, which `ViewerSaveGuardTests` catches.

#### §9. Image information, histogram, and viewer tools

- **Deliverable:** the viewer shows image information, status and title fields, a histogram, pixel values, selection geometry, a develop settings summary, an editable properties pane, a byte view, QR and barcode reading, and text recognition.
- **Depends On:** §4
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-info/. Job: a user answers "what is this file" and reads data from the image without leaving the viewer. Treatment: `I` for the Image Information dialog, a status strip with clickable rating, label, and tag, a histogram pane with channel toggles, a properties pane, pixel info on click with copy, Tools, Read Code, and Tools, Recognize Text. Cheaper substitute that fails: a file-size tooltip. Chrome: consume the histogram control moved to `Photon.UI` by `D04 T02 §3`, the catalog for rating and label writes, and `D04 T08 §2`'s fields when it ships.
- **Runs:** `Requires: display-session -- panes and dialogs are captured on screen`
- **Catalog:** LP-0101 to LP-0113 (13 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-info`
- **Hints:**
  - Image Information dialog (LP-0109): name, folder, compression, original and current size and colors, unique colors, print size, disk and memory size, folder index, date, load time.
  - Status and title (LP-0101, LP-0105, LP-0106, LP-0108): size, bit depth, index, zoom, file size, chosen date (file, EXIF, catalog), tag marker, pixel coordinates and color, selection origin, size, and ratio, full path, custom status text with tokens from `D04 T11 §2`; rating, label, and tag clickable, written to the catalog and sidecar.
  - Histogram pane (LP-0103): R, G, B, and lightness toggles, bar or curve modes, selection histogram, copy channel averages.
  - Pixel information (LP-0111): coordinates, color, palette index on click, copy hex color and coordinates.
  - Properties pane (LP-0102) reads metadata and edits caption, rating, and keywords to the catalog and sidecar; develop settings pane (LP-0104) lists the edit stack's non-default settings.
  - Byte view (LP-0107): a read-only HEX and ASCII view of the file's first megabytes with paging.
  - QR and barcodes (LP-0110): ZXing.Net (Apache-2.0) over the displayed image or selection, results copyable.
  - Text recognition (LP-0112): `Windows.Media.Ocr` with installed languages (part of Windows), with a user-installed Tesseract (Apache-2.0) run as an external process when configured and refused by name when absent; KADMOS is not supported.
  - Tools menu (LP-0113): the utility entries above plus copy file list, grouped as IrfanView's Tools plug-in did.
  - Tests: `ImageInfoTests` (unique colors on a fixture, print size at DPI), `QrReaderTests` on a committed QR fixture, `OcrServiceTests` skipped with a reason where no OCR language is installed.
  - Commit: `"lumen: image information, histogram, pixel values, codes, and text in the viewer"`
- **Proof:** unit plus driven: the tests pass and captures show the information dialog, histogram, a decoded QR fixture, and recognized text; cheaper substitute that fails: a tooltip, which the dialog field tests catch.

#### §10. Multi-page and animated images in the viewer

- **Deliverable:** the viewer pages through multi-page TIFF, PDF, ICO, and DjVu files with page thumbnails and plays animated GIF, APNG, WebP, AVIF, ANI, and MNG files with frame stepping and speed, and can play a multi-page file as an animation.
- **Depends On:** §4, D04 T13 §4
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-pages/. Job: a user reads a scanned multi-page document and checks an animation frame by frame. Treatment: `Ctrl+Page Down` and `Ctrl+Page Up` for pages, a page box, a page thumbnail strip that shows itself for multi-page files, and animation controls (play, pause, step, speed) in the toolbar. Cheaper substitute that fails: showing page one and frame one only. Chrome: consume the registry's `IMultiFrameDecoder` capability from `D04 T13 §1` and `§4`.
- **Runs:** `Requires: display-session -- playback is observed on screen`
- **Catalog:** LP-0059 to LP-0061, LP-0114, LP-0972 (5 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-pages`
- **Hints:**
  - Page navigation (LP-0059): next, previous, first, last, go to page, page thumbnails with auto show, a page view pane, page keys.
  - `AnimationPlayer` in `Photon.Lumen.Core/Viewer/` (LP-0060, LP-0972): frame timing from the file, stop, resume, step, speed 0.25x to 4x, disposal and blending rules per format, an option to show the first frame only (LP-0114).
  - Play pages as an animation (LP-0061) with a chosen delay.
  - Viewing only: frame extraction and animated authoring stay B-044, and the menu says so.
  - Tests: `AnimationPlayerTests` (GIF disposal modes and APNG blend ops against committed fixtures and per-frame goldens), page count tests for multi-page TIFF and PDF fixtures.
  - Commit: `"lumen: multi-page and animated images in the viewer"`
- **Proof:** unit plus driven: the frame goldens match and a driven session steps a GIF and pages a PDF (captures); cheaper substitute that fails: first frame only, which the frame goldens catch.

#### §7. Fullscreen and presentation

- **Deliverable:** fullscreen viewing with every fit and resampling option, backdrop, transitions, info text with placeholders, header and footer captions, cursor hiding, all-monitor spanning, touch-friendly mouse rules, and the Explorer context-menu preview.
- **Depends On:** §4, §5
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-fullscreen/. Job: a user shows photos full screen to others with only the image and the text they chose. Treatment: `F`, `Enter`, or double-click toggles, `Esc` exits, quick fit keys 1 to 7, a fullscreen context menu with viewer tools, info text and header or footer overlays, a blurred-sides backdrop, crossfade. Cheaper substitute that fails: a maximized window. Chrome: consume `D04 T11 §2`'s token engine for text, `D01 T03 §2` for resampling, and the theme.
- **Runs:** `Requires: display-session -- fullscreen is captured on screen, including a second monitor`
- **Catalog:** LP-0031, LP-0077 to LP-0087 (12 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-fullscreen`
- **Hints:**
  - Toggle and exit (LP-0077): `F`, `Enter`, double-click, `Esc`, start in fullscreen, context menu with viewer tools; unused keys end fullscreen unless disabled (LP-0087).
  - Display options (LP-0080, LP-0081): original size, fit large only, fit all, stretch, fit width, height, or smaller side, a display multiplier, centering, quick keys 1 to 7, resampling on first display and on zoom.
  - Backdrop (LP-0082): screen color or blurred image sides; transitions and crossfade (LP-0083).
  - Overlays (LP-0078, LP-0084): header and footer captions and info text with tokens, font, box color or transparent, position, alignment, toggle; never modify the file.
  - Cursor (LP-0079): hidden in fullscreen, shown briefly on move; mouse rules (LP-0086): left or right button scrolling for touch, left click previous and right click next.
  - All monitors (LP-0085): span or choose a monitor.
  - Explorer context-menu preview (LP-0031): a small in-process COM shell extension `Photon.Lumen.ShellPreview` (IContextMenu3 owner-drawn preview with EXIF lines, main or sub-menu placement, size, show original, enable switch), isolated from the app like Imago's shell thumbnail project and loading only `Photon.Core/Formats/` readers; if its Explorer-stability proof fails, the section moves this row to the backlog through `add-todo` and updates the catalog.
  - Tests: `FullscreenLayoutTests` (fit modes on four monitor sizes), a token rendering test for the info text.
  - Commit: `"lumen: fullscreen presentation and the Explorer preview"`
- **Proof:** unit plus driven: the tests pass and captures show fullscreen with info text, blurred sides, and the Explorer context-menu preview; cheaper substitute that fails: a maximized window, which the monitor-span capture exposes.

#### §8. Quick slideshow in the viewer

- **Deliverable:** the viewer's quick slideshow: a file-list dialog, per-image durations and captions, playback rules, background music, window or fullscreen presentation, saved TXT lists, and in-show actions, distinct from the authored slideshow module of `D04 T12 §7`.
- **Depends On:** §7
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-slideshow/. Job: a user plays a folder or a hand-picked list with music in seconds. Treatment: `W` opens the Slideshow dialog (list with add, add all, remove, sort, insert position, per-image duration and caption, timing, loop, random, music, window or fullscreen, info text), Play starts; Image Advance keys during play. Cheaper substitute that fails: a timer over the folder with no list. Chrome: consume §7's fullscreen renderer, NAudio (MIT) for music, and the token engine.
- **Runs:** `Requires: display-session -- playback is driven on screen`
- **Catalog:** LP-0088 to LP-0100 (13 features)
- **Source:** `-> SOURCE: parity-lumen-viewer-slideshow`
- **Hints:**
  - `QuickSlideshowList` in `Photon.Lumen.Core/Viewer/Slideshow/` (LP-0093, LP-0094): add, add all, remove, sort by name, date, size, extension, or EXIF date, insert position, remembered start index, per-image duration and caption.
  - Start points (LP-0088, LP-0090, LP-0092): from the viewer, the current folder, a selection, append or remove the current file, last used folder; Save and append to a slideshow list.
  - Image Advance (LP-0089): next, previous, pause, forward, reverse, or random sequence, repeat, delay.
  - Playback rules (LP-0095): loop, close after last, skip unreadable files, advance by timer or key, random without repeats with history, pause; orientation filter all, landscape, or portrait (LP-0100).
  - Music (LP-0096): audio entries in the list or a loop MP3 through NAudio over Media Foundation.
  - Presentation (LP-0097): fullscreen or window with position and size, hide cursor, info text with tokens; keep the system awake with `SetThreadExecutionState` (LP-0091).
  - During play (LP-0099): zoom, scroll, delete to the Recycle Bin, copy, and animated images play.
  - List files (LP-0098): load and save TXT lists with comments and relative paths; persisted last list.
  - Tests: `QuickSlideshowListTests` (TXT round trip with relative paths and comments, random without repeats covers every item once).
  - Commit: `"lumen: the quick slideshow in the viewer"`
- **Proof:** unit plus driven: the tests pass and a driven slideshow of 20 images with an MP3 loops and closes after last (log quoted); cheaper substitute that fails: a folder timer, which the TXT round trip and list tests catch.

#### §11. Quick edits I: rotate, flip, select, crop, resize, and canvas

- **Deliverable:** in the viewer, selections of every shape with saved presets and grids, crop, cut, auto crop, fine rotation and straighten, resize and resample with every filter, DPI changes, canvas size, auto adjust, and undo, each applied through the batch engine's operations to the in-memory image and saved only as a new file; library rotate and flip store orientation as metadata.
- **Depends On:** §4, D04 T11 §7
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-edit/. Job: a user fixes a photo's framing and size in seconds and keeps the original untouched. Treatment: drag a selection, `Ctrl+Y` crop, `Shift+C` auto crop, `Ctrl+R` resize dialog, `Shift+V` canvas size, `Ctrl+U` fine rotation with a draw-a-line straighten, `Shift+U` auto adjust, `Ctrl+Z` and `Ctrl+Shift+Z` with a configurable step count. Cheaper substitute that fails: edits applied to the decoded preview. Chrome: consume `D04 T11 §7`'s `IBatchOperation` implementations and `D01 T03 §2`; the dialogs share their controls with the batch edit pipeline.
- **Runs:** `Requires: display-session -- quick edits are driven in the viewer`
- **Catalog:** LP-0122 to LP-0134, LP-0253 (14 features)
- **Source:** `-> SOURCE: parity-lumen-quick-edits-geometry`
- **Hints:**
  - `ViewerEditSession` in `Photon.Lumen.Core/Viewer/Editing/`: a full-resolution working image, an ordered list of applied `IBatchOperation` records, undo and redo with `Lumen.Viewer.UndoSteps` (LP-0124); leaving with unsaved edits prompts Save As (§6).
  - Selections (LP-0122, LP-0125, LP-0126): rectangle with ratio lock, ellipse, freehand, inverted, exact position and size with saved presets, maximize for popular ratios, center, restore last, size from the clipboard image, golden ratio, thirds, and fourths grids; options for colors, thickness, grid size (LP-0134).
  - Selection actions (LP-0123): zoom to, copy, save as a new image, print through `D04 T12 §4`, set as wallpaper.
  - Crop (LP-0127): to selection, to the visible area, auto crop uniform borders with tolerance and a preview selection, cut and cut outside with a fill color, remove or insert strips.
  - Fine rotation (LP-0129): any angle, fill color, keep size or best inner rectangle, straighten by drawing a line, on a selection, fine-step keys.
  - Resize (LP-0130, LP-0131, LP-0128): pixels, cm, inches, percent, megapixels, standard sizes, keep aspect, saved custom sizes, every filter `D01 T03 §2` provides (Lanczos, Mitchell, B-spline, Bell, triangle, Hermite, Catmull-Rom, box, shrink), gamma-correct option, DPI change with or without resampling.
  - Canvas size (LP-0132): per-side sizes including negative, anchor, extend to an aspect ratio, color, saved settings; auto adjust colors from image or selection statistics (LP-0133).
  - Library rotate and flip (LP-0253): the grid and loupe store orientation in the catalog and the sidecar (`tiff:Orientation`), which every render honors; never the original.
  - Tests: `ViewerEditSessionTests` (each operation equals its batch counterpart pixel for pixel on fixtures, undo restores the previous hash), `SelectionPresetTests`.
  - Commit: `"lumen: viewer quick edits for selection, crop, rotation, resize, and canvas"`
- **Proof:** unit plus driven: the equality tests pass and a driven crop, straighten, and resize saves a new file with the original's hash unchanged (quoted); cheaper substitute that fails: editing the display preview, which the full-resolution equality test catches.

#### §16. Lossless JPEG transforms to new files

- **Deliverable:** lossless JPEG rotate, flip, transpose, crop to selection, marker cleaning, EXIF date and thumbnail updates, from the viewer, the grid, and a dialog, always written to a new file (or stored as orientation metadata), with every jpegtran option.
- **Depends On:** §11
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/lossless-jpeg/. Job: a user rotates or crops JPEGs without any recompression loss and without risking the camera file. Treatment: toolbar rotate buttons store orientation; Image, Lossless Transform opens a dialog (transform, perfect or trim, optimize, progressive, markers keep, clean, or choose, update EXIF thumbnail and DPI, keep ICC, file date from EXIF) writing `<name>-rotated.jpg` or a chosen name. Cheaper substitute that fails: decode, rotate, and re-encode. Chrome: consume libjpeg-turbo 3.1's `tjTransform` through the P/Invoke that `D03 T17 §11` adds and `D04 T13 §6` moves to `Photon.Core` (IJG and BSD-3-Clause and zlib licenses).
- **Runs:** `Requires: display-session -- the dialog is driven`
- **Catalog:** LP-0169 to LP-0174 (6 features)
- **Source:** `-> SOURCE: parity-lumen-lossless-jpeg`
- **Hints:**
  - `LosslessJpegTransformer` in `Photon.Lumen.Core/Viewer/Lossless/` over `tjTransform`: rotate 90, 180, 270, flip, transpose, transverse, perfect or trim edges, MCU-aligned crop (LP-0171, LP-0173).
  - Options (LP-0172): optimize, progressive, JFIF marker, keep, clean, or choose markers, update the EXIF thumbnail, DPI, ICC profile, output file date from EXIF or kept.
  - Toolbar and grid rotate (LP-0169, LP-0170): store orientation as metadata by default; "Lossless transform to a new file" writes beside the original; auto rotate by EXIF and orientation reset act on the new file.
  - EXIF date edit, clean metadata, and thumbnail update (LP-0174) apply to the new file only.
  - A guard assertion: the transformer's output path must differ from the input path, or it throws before opening anything for writing.
  - Tests: `LosslessJpegTransformerTests` (the DCT coefficients of the output equal a jpegtran 3.1 golden for each transform on committed fixtures; MCU-aligned crop dimensions; the input hash is unchanged).
  - Commit: `"lumen: lossless JPEG transforms written to new files"`
- **Proof:** format fidelity: coefficient-level comparison with the jpegtran goldens (version recorded) for every transform, plus the unchanged-input hash; cheaper substitute that fails: decode and re-encode, which the coefficient comparison catches.

#### §12. Quick edits II: color corrections, color depth, and palettes

- **Deliverable:** in the viewer, color corrections with profiles, grayscale and negative, channel swaps, transparency color and replace color, sharpen, red and pet eye, color depth decrease and increase with dithering, and palette editing, each a batch operation saved as a new file.
- **Depends On:** §11
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-color/. Job: a user corrects or converts a photo's color and palette quickly, as in IrfanView's Image menu. Treatment: `Shift+G` Color Corrections dialog with live preview on the image and saved profiles, Image menu entries for depth, grayscale, negative, swap channels, replace color, palette. Cheaper substitute that fails: brightness and contrast only. Chrome: consume `D01 T03 §3` quantization, `D01 T03 §4` and `§5` tonal and color adjustments, and `D01 T07 §5`'s red-eye detector.
- **Runs:** `Requires: display-session -- the dialogs are driven`
- **Catalog:** LP-0135 to LP-0146 (12 features)
- **Source:** `-> SOURCE: parity-lumen-quick-edits-color`
- **Hints:**
  - Color Corrections (LP-0138, LP-0139): brightness, contrast, gamma, saturation, RGB balance, click a bright area for white balance, live preview, saved profiles, dark dialog option.
  - Grayscale and negative of all or one channel (LP-0137); swap channels RBG, BGR, BRG, GRB, GBR (LP-0144).
  - Decrease color depth (LP-0135): 2, 16, 256, or custom colors, black and white and gray palettes, best-quality quantizer, dithering, RGB565, through `D01 T03 §3`; increase depth to truecolor, 16-bit gray, 48-bit, or 32-bit with alpha (LP-0136).
  - Transparency (LP-0140, LP-0141): set a transparent color with tolerance and alpha intensity, replace color with tolerance or make transparent, pick from the image.
  - Sharpen with a set amount (LP-0142); red eye with gray intensity and green and yellow pet eye (LP-0143) through `D01 T07 §5`.
  - Palettes (LP-0145, LP-0146): edit indexed colors, export and import JASC and Microsoft PAL files, import maps to the nearest color.
  - Every command is an `IBatchOperation` from `D04 T11 §6` or `§7`, so the same settings run in batch.
  - Tests: `ColorQuickEditTests` (each operation against its batch golden), `PalFileTests` (round trip).
  - Commit: `"lumen: viewer color corrections, depth, and palettes"`
- **Proof:** unit plus driven: the tests pass and captures show the dialog preview and a 16-color dithered result saved as a new file; cheaper substitute that fails: brightness and contrast only, which the operation list tests catch.

#### §15. Quick edits III: the effects browser and viewer effects

- **Deliverable:** an effects browser in the viewer that lists the `Photon.Core` effect registry's blur, sharpen, stylize, distort, tone, and noise effects with a preview and one value each, plus local contrast enhancement, SmartCurve-style curves, film simulation from CLUT files, and Auto Lens preview-through-a-filter while browsing.
- **Depends On:** §12
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-effects/. Job: a user tries effects on a photo with a preview and saves the one they like as a new file. Treatment: a resizable Effects Browser with a category list, before and after preview, a value slider per effect, apply to selection or whole image; Image, Curves; Auto Lens toggle in the toolbar. Cheaper substitute that fails: a menu of effects with fixed values and no preview. Chrome: consume the effect registry of `D01 T03` and `D01 T06`; add no algorithm to Lumen.
- **Runs:** `Requires: display-session -- the effects browser is driven`
- **Catalog:** LP-0076, LP-0159 to LP-0168 (11 features)
- **Source:** `-> SOURCE: parity-lumen-quick-edits-effects`
- **Hints:**
  - `EffectsBrowserViewModel` (LP-0159) lists registry entries by category with one primary value each and a preview on a downscaled copy, applied through `EffectOperation` (`D04 T11 §7`).
  - Blur (LP-0160: blur, Gaussian, fast Gaussian, total variation, radial, zoom, motion, tilt-shift), sharpen (LP-0161), stylize (LP-0162: 3D button, emboss, oil paint, edge detection, find edges, explosion, pixelize, fragment, solarize, metallic, rock, stained glass, blinds), tone and noise (LP-0163), distort (LP-0164): map each to its registry id; an effect the registry lacks is filed through `add-todo` against `D01 T06`, never written in Lumen.
  - Local contrast enhancement (LP-0165): the registry's local contrast (CLAHE-style) effect with strength and scale, own implementation, not the AltaLux plug-in.
  - Curves (LP-0167): an RGB and per-channel curve dialog over `D01 T03 §4`'s `ToneCurve`.
  - Film simulation (LP-0166, LP-0168): Hald CLUT and `.cube` files through `D01 T07 §9`'s LUT stage; users add their own CLUT packs; none bundled.
  - Auto Lens (LP-0076): a view-only filter chosen from the browser applied to every displayed image while browsing, persisting until turned off, never saved.
  - Tests: `EffectsBrowserTests` (every listed id resolves in the registry; preview and full-size apply agree within 1/255 after scaling).
  - Commit: `"lumen: the effects browser, curves, film simulation, and Auto Lens in the viewer"`
- **Proof:** unit plus driven: the tests pass and captures show the browser preview and an Auto Lens session; cheaper substitute that fails: fixed-value effects, which the preview agreement test exposes.

#### §13. Quick edits IV: text, watermarks, borders, and combining images

- **Deliverable:** in the viewer, inserted text with placeholders and effects, image watermarks, paste-in and paste-beside collages, color highlights, speech bubbles, borders and frames, shaped crops and shadows, combining images side by side, and exporting image tiles, each saved as a new file.
- **Depends On:** §11, D04 T11 §8
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/viewer-overlays/. Job: a user captions, brands, frames, or tiles a photo in the viewer without opening an editor. Treatment: `Ctrl+T` or Edit, Insert Text with a preview dialog and profiles, Edit, Watermark with click-to-place, Image, Add Border, Image, Combine Side by Side, Image, Export Tiles. Cheaper substitute that fails: text without placeholders or preview. Chrome: consume `D04 T11 §8`'s text and watermark engine and `D04 T11 §2`'s tokens; layered editing hands off to Imago.
- **Runs:** `Requires: display-session -- the dialogs are driven`
- **Catalog:** LP-0147 to LP-0158 (12 features)
- **Source:** `-> SOURCE: parity-lumen-quick-edits-overlays`
- **Hints:**
  - Insert text (LP-0147, LP-0151): at a click or in a selection, multi-line with tokens and tabs, font, size, style, color, alignment, rotation, antialiasing, box, shadow and outline, adjust font to zoom, add canvas above or below, profiles, `Ctrl`-click stamping, pick color from the image.
  - Watermark (LP-0148): corner and offset or center, click to place with preview, transparency, keeps PNG and GIF alpha, from the selection, through `D04 T11 §8`.
  - Paste in (LP-0149) movable and resizable before applying; paste on a side for simple collages with a paste counter (LP-0150).
  - Color highlight on an area (LP-0152), speech bubbles (LP-0155), shaped crops and shadows (LP-0156: drop shadow, rounded corners, star, heart, cloud, hexagon, snowflake).
  - Borders and frames (LP-0154): up to four parts, presets, inside fading, broken edge and lines, on a selection.
  - Combine images side by side (LP-0153, LP-0158): horizontal or vertical, spacing, file-name labels, tiled grid, from the viewer list or a library selection.
  - Export tiles (LP-0157): count or size, spacing, all pages, format and folder; writes new files.
  - Tests: `OverlayQuickEditTests` (text with `$F` and `{name}` tokens renders expected names; watermark alpha kept; combined image dimensions), `TileExportTests`.
  - Commit: `"lumen: viewer text, watermarks, borders, and combined images"`
- **Proof:** unit plus driven: the tests pass and captures show a captioned, watermarked, framed photo and a side-by-side combination saved as new files; cheaper substitute that fails: fixed text, which the token test catches.

#### Sizing concerns

- §1 carries a new project, the startup harness, and the resident mode; if it passes 30 items, the resident mode (LP-0003) splits into its own section within Phase 30.
- §6 mixes file operations with wallpaper and external editors; the natural split is wallpaper and editors (LP-0029, LP-0030, LP-0116, LP-0117) into a sibling section.
- §7's Explorer context-menu preview (LP-0031) needs an in-process COM shell extension; it is the likeliest row to move to the backlog if Explorer stability cannot be proven, recorded in the section's first item.
- §11 and §13 hold many options per feature; their dialogs share controls with `D04 T11 §7`, which keeps them under 30 items only if the batch dialogs ship first.

### todo/04-lumen/TODO-05-lumen-browse.md -- `lumen-browse`

- **Title:** "TODO-05 -- Lumen Parity: Browse Without Importing"
- **Phase(s):** 32
- **Goal:** A photographer can point Lumen at any folder and work there at once, ACDSee style: browse without importing, with the file system as the source of truth and the catalog as its cache (an `origin` of `browsed` or `library` per record); a background indexer fills metadata and thumbnails for chosen locations while idle; the folder tree, favorites, address bar, tabs, and home page navigate; file list views, thumbnails, sorting, grouping, filtering, and selection behave like a fast file manager; file operations copy, move, rename, and recycle photos with their sidecars and pairs and an undo journal; compare, information palette, basket, selective browsing, a private encrypted folder, calendar browsing, a duplicate finder, archives, and folder sync complete the job. Rating or keywording a browsed file creates its record with no import step, and no image byte of an original is ever written. Budgets: an unindexed folder of 5,000 JPEGs lists in at most 300 ms and shows its first screen of thumbnails in at most 1.5 s, a reopened indexed folder in at most 200 ms, and the indexer processes at least 50 JPEGs per second without raising the foreground frame time over 16 ms.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code; the foundation plans a catalog of imported photos only, with no browsed membership. `<!-- claim: absent src/Lumen -->` `<!-- claim: count "browsed" todo/04-lumen/TODO-01-lumen-foundation.md = 0 -->`
  - No Lumen section plans the Recycle Bin or file operations yet. `<!-- claim: count "Recycle" todo/04-lumen/TODO-01-lumen-foundation.md = 0 -->` `<!-- claim: count "Recycle" todo/04-lumen/TODO-02-lumen-develop.md = 0 -->`
  - No archive package is in the solution. `<!-- claim: count "SharpCompress" Directory.Packages.props = 0 -->`
  - `standards/lumen.md` already says paths are stored relative to a root so moved libraries reconnect. `<!-- claim: count "relative to a root folder" standards/lumen.md = 1 -->`
- **Inputs and XREFs:** `standards/lumen.md`, `standards/shared.md` (performance budgets, logging); `docs/parity/lumen-parity.md`; ACDSee Photo Studio Ultimate 2027 User Guide, Manage mode chapters; IrfanView 4.76 help `hlp_thumbnails.htm`; Microsoft Learn: `FindFirstFileExW` with `FIND_FIRST_EX_LARGE_FETCH`, `IFileOperation`, `FileSystemWatcher` buffer overflow, Task Scheduler idle triggers; -> XREF: D04 T01 §5 (the catalog §1 adds `origin` to); -> XREF: D04 T01 §7 (the preview cache §2 feeds and §4 reads); -> XREF: D04 T01 §8 (the library grid whose views, badges, and sort §4 and §5 extend); -> XREF: D04 T01 §9 (compare, which §7 extends to four images); -> XREF: D04 T01 §11 (sidecars that travel in §6); -> XREF: D04 T13 §1 (reading through the shared registry); -> XREF: D04 T04 §1 (the viewer's `T` key opens browse at the viewer's folder; §1 retargets it from the library grid to browse); -> XREF: D04 T11 §1 (the Activity Manager the indexer and file operations report to) and D04 T11 §3 (batch rename shares §6's journal); -> XREF: D04 T06 §8 (outside moves reconnect through it) and D04 T06 §7 (selective browsing shares its criteria); -> XREF: D04 T10 §5 (visually similar photos beyond §11's exact duplicates); -> XREF: D03 T17 §12 (the SharpCompress archive opener §12 moves to `Photon.Core`).
- **Adjacency:** list=applicable (the file list in §4 and the basket in §8); document=applicable (archives, file lists, and synced copies are files the user keeps); settings=applicable (views, overlays, columns, sort memory, indexed locations, exclusions, confirmations, sync jobs, as `Lumen.Browse.*` keys); reporting=applicable (preview pane information and histogram, the information palette, duplicate reports, sync logs); notifications=applicable (indexer progress in the Activity Manager, file operation conflicts and results); permissions=applicable (read-only media, locked and network files, protected folders refused by name; the private folder's password); audit=applicable (one Serilog Information line per file operation and per sync run, and the journal); exchange=applicable (drag and drop and the file clipboard with other programs, archives, text file lists); reverse=applicable (file operations journaled and undoable; delete goes to the Recycle Bin)

#### §1. The browse model: folders without import, browsed and library photos

- **Deliverable:** Lumen's Manage-mode browse window shows any folder at once from a file-system enumeration, with catalog records created automatically as `browsed` (with per-file fields) when the user rates, labels, keywords, or develops a file, an "Add to Library" command, and the thumbnails-to-viewer hand-off (double-click, Tab, Esc).
- **Depends On:** D04 T02 §8, D04 T13 §1
- **Phase:** 32
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/ (the shell of `D04 T01 §2`), new captures to docs/captures/lumen/browse/. Job: a user opens a folder and starts culling within a second, with nothing to import first. Treatment: ACDSee Manage mode's file list pane, contents bar, status bar, task pane, maximized and full-screen file list; Lightroom-style import stays one click away. Chrome: consume the grid of `D04 T01 §8`, the preview cache, and the catalog; do not add a second grid control. Cheaper substitute that fails: an import dialog shown when a folder is opened.
- **Runs:** `Requires: display-session -- browsing and the frame-time measurement need an interactive desktop`
- **Catalog:** LP-0179 to LP-0182 (4 features)
- **Source:** `-> SOURCE: parity-lumen-browse-model`
- **Hints:**
  - Catalog migration (forward-only, tested on the previous version's catalog per `D04 T01 §5`): `images.origin` (`library` or `browsed`), `browsed_folders` table, cache key path plus size plus last-write time, hash computed lazily (LP-0180, LP-0181).
  - `FolderEnumerator` in `Photon.Lumen.Core/Browse/` with `FindFirstFileExW` large fetch, returning entries in under 300 ms for 5,000 files (measured and quoted); the view sorts and groups in memory.
  - Implicit records (LP-0181): the first metadata or develop change on a browsed file creates its record (origin `browsed`) and the sidecar when enabled; no import step (LP-0180).
  - Add to Library: flips `origin` in place with one undo step; `D04 T01 §6` import stays for copies and cards.
  - Browse window (LP-0179): file list pane, contents bar, status bar, task pane, maximize and full-screen file list.
  - Viewer hand-off (LP-0182): double-click opens `LumenViewer.exe` through `D04 T04 §1`, Tab switches between browse and viewer, Esc hides the viewer; `D04 T04 §1`'s `T` key now opens browse at the viewer's folder with the file selected.
  - Budget test `BrowseBudgetTests` (generated 5,000-JPEG folder with EXIF thumbnails): listing at most 300 ms, first screen of thumbnails at most 1.5 s, quoted with the machine.
  - Unchanged-originals assertion over a browse session (browse, rate, keyword, add to library).
  - Commit: `"lumen: browse any folder without importing"`
- **Proof:** unit plus driven: `BrowseModelTests` (implicit record creation, add to library, migration) and `BrowseBudgetTests` pass with timings quoted; captures committed; cheaper substitute that fails: importing silently on open, which the origin assertion catches.

#### §2. The background indexer

- **Deliverable:** A low-priority indexer fills metadata and high-quality, develop-aware thumbnails for folders the user chooses to monitor, while Lumen is idle and optionally while it is closed (a per-user scheduled task running `Lumen.exe --index`), with exclusions, a catalog files dialog to add folders without browsing, file-kind choices, pause and resume, and change watching.
- **Depends On:** §1
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/indexer/. Job: a user's whole photo drive becomes searchable in the background without slowing the app. Treatment: ACDSee's Indexer options (index when idle, image files only or all, target catalog, folders to monitor) and Catalog Files dialog (add folders, file kinds, thumbnails, archive contents, RAW previews), an Excluded Folders list with reset. Chrome: consume §1, `D04 T11 §1`'s Activity Manager, the preview cache (`D04 T01 §7`), and Task Scheduler through `Microsoft.Win32.TaskScheduler` or the `schtasks` CLI (decision recorded; the package option is MIT). Cheaper substitute that fails: a Windows service.
- **Runs:** `Requires: display-session -- the idle-indexing drive and frame-time measurement need an interactive desktop`
- **Catalog:** LP-0183 to LP-0187 (5 features)
- **Source:** `-> SOURCE: parity-lumen-indexer`
- **Hints:**
  - `IndexerService` in `Photon.Lumen.Core/Indexing/`: priority queue (visible, selected folder, indexed locations), below-normal thread and I/O priority, persisted progress (LP-0185, LP-0187).
  - Idle detection through `GetLastInputInfo`; pause while developing or exporting and on battery by `Lumen.Indexer.PauseOnBattery` (default true).
  - `--index` headless mode of `Lumen.exe` and an opt-in scheduled task at sign-in when idle, per user, no administrator rights (LP-0185).
  - Monitored folders with `FileSystemWatcher`; a buffer overflow triggers a rescan of that folder (LP-0187).
  - Excluded folders with reset to defaults (LP-0184), `Lumen.Indexer.Exclusions`.
  - Catalog files dialog (LP-0186): add folders without browsing, file kinds (images only or all), thumbnails, archive contents, RAW previews; target catalog.
  - High-quality and develop-aware thumbnails replacing embedded ones in the background (LP-0183), extending `D04 T01 §7`.
  - Budget: at least 50 JPEGs per second metadata plus thumbnail with foreground frame time under 16 ms while scrolling, measured and quoted.
  - Tests: `IndexerQueueTests` (priorities, pause, resume after restart), `IndexerWatcherTests` (create, rename, delete, overflow rescan).
  - Commit: `"lumen: a background indexer for chosen folders"`
- **Proof:** unit plus driven: the tests pass; a driven index of a 20,000-file drive reports throughput and frame times; cheaper substitute that fails: indexing on the UI thread, which the frame-time budget catches.

#### §3. The folder tree, favorites, address bar, tabs, and home page

- **Deliverable:** Browse navigation: a folder tree with drives, removable devices, and shell folders (new, delete, rename folder), a shortcuts and favorites pane, back, forward, and home, an address box with typed and pasted paths and recent folders, multi-folder and recursive browsing, tabs with per-tab state, the startup location, and a home page with quick searches and actions.
- **Depends On:** §1
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/folders/, docs/captures/lumen/tabs/, and docs/captures/lumen/home/. Job: a user moves around their disks as fast as in Explorer and keeps several places open. Treatment: ACDSee's Folders pane with Easy-Select bars, Shortcuts pane, address box, browsing tabs, and Home page (quick search, recently modified and added, tagged and unnamed-face searches, import and maintenance buttons). Chrome: consume `Photon.UI` tree and tab styles, the settings store, and the icon catalog. Cheaper substitute that fails: a single folder picker dialog.
- **Runs:** `Requires: display-session -- navigation panes and tabs need an interactive desktop`
- **Catalog:** LP-0188 to LP-0197 (10 features)
- **Source:** `-> SOURCE: parity-lumen-browse-navigation`
- **Hints:**
  - `FolderTreeViewModel`: drives, removable devices (refresh on `WM_DEVICECHANGE`), common shell folders, new, delete (Recycle Bin), rename folder (LP-0189).
  - Toolbar home, back, forward with a per-tab history (LP-0188).
  - Shortcuts pane (LP-0190): shortcuts to files, folders, and programs, folders of shortcuts, drag to create, run, rename, delete, stored in `Lumen.Browse.Shortcuts`.
  - Multi-folder and recursive browsing (LP-0193): Easy-Select check bars, Ctrl-click with subfolders, load all subfolders, tree context menu.
  - Tabs (LP-0194, LP-0196): new, open in new tab, middle-click, duplicate, close, close others, left, right, next and previous; per-tab panes, filters, groups, and searches; drag files between tabs; last tab restored.
  - Address box (LP-0197): typed or pasted paths with completion, recent folders with count and clear, focus options.
  - Startup location (LP-0195): home page, start folder, reopen last or all tabs, `Lumen.Browse.Startup`.
  - Home page (LP-0191, LP-0192): quick search bar, recently modified and added with time windows and date basis, tagged and unnamed-face searches (face searches appear when `D04 T10 §3` ships), import, backup and maintenance, catalog files buttons.
  - Tests: `FolderNavigationTests` (history, tabs, restore), `AddressBoxTests` (path parsing, UNC, relative).
  - Commit: `"lumen: folder tree, favorites, address bar, tabs, and home page"`
- **Proof:** unit plus driven: the tests pass; a driven session opens four tabs, restarts, and restores them (captured); cheaper substitute that fails: one folder at a time, which the tab restore test catches.

#### §4. File list views, thumbnails, and the preview pane

- **Deliverable:** The browse file list offers thumbnails, tiles, thumbs plus details, filmstrip, icons, list, and details views, adjustable thumbnail size and cell shape, overlay icons and display options, details columns, thumbnail styles and info fields, hover pop-ups, which file types show, refresh and remove from list, and a preview pane with information and histogram.
- **Depends On:** §2, §3
- **Phase:** 32
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/ (grid baseline from `D04 T01 §8`), new captures to docs/captures/lumen/file-list/ and docs/captures/lumen/preview-pane/. Job: a user sees exactly the information they cull by, in the layout they like, at scroll speed. Treatment: ACDSee's view modes, thumbnail overlay icons with per-overlay toggles and color highlight cycling, details columns editor, thumbnail style and info options, hover pop-ups, and preview pane (image, information, histogram, delay, progressive instant preview). Chrome: extend `D04 T01 §8`'s virtualizing grid (never a second one), the preview cache, and the histogram control moved to `Photon.UI` by `D04 T02 §3`. Cheaper substitute that fails: fixed thumbnails with no overlays.
- **Runs:** `Requires: display-session -- views and frame times need an interactive desktop`
- **Catalog:** LP-0198 to LP-0208 (11 features)
- **Source:** `-> SOURCE: parity-lumen-file-list`
- **Hints:**
  - View modes (LP-0199): thumbnails, tiles, thumbs plus details, filmstrip, icons, list, details, all on the virtualizing panel, extending `D04 T01 §8`.
  - Size and cell shape (LP-0200): zoom slider, presets, portrait, landscape, or custom ratio, spacing.
  - Overlay icons (LP-0201): rating, label, format, category, collection, stack, shortcut, offline, excluded, tagged, rejected, geotagged, auto-rotated, developed, edited, sidecar; display options (LP-0202): modes, color highlight cycling, per-overlay toggles, empty overlays on hover, stack bars.
  - Details columns (LP-0203): choose, add, remove, reorder, reset, grid lines, full row select, auto width, highlight and click-to-sort; any metadata field as a column.
  - File types shown (LP-0204): images, PDF, folders, archives, Office documents, hidden files, THM and XMP, `Lumen.Browse.ShowKinds`.
  - Thumbnail style (LP-0205): shadow, slide background, folder style with contents, borders, colors, high-quality scaling; info fields on thumbnails and tiles (LP-0207); hover pop-ups on hover or Shift with chosen fields (LP-0206).
  - Refresh thumbnails and remove items from the list without deleting (LP-0208).
  - Preview pane (LP-0198): image, information, histogram, delay, size, progressive instant preview, chosen fields.
  - Frame-time budget re-measured with every overlay on (under 16 ms median on the 50,000-image catalog of `D04 T01 §8`).
  - Tests: `FileListViewModelTests` (views, column persistence, kinds filter), `OverlayProviderTests`.
  - Commit: `"lumen: browse views, overlays, columns, and the preview pane"`
- **Proof:** unit plus driven: the tests pass; frame times with all overlays are quoted; captures of each view mode committed; cheaper substitute that fails: a non-virtualized details view, which the budget catches.

#### §5. Sort, group, filter, and select in browse

- **Deliverable:** Browse sorts by name (natural), size, type, dates, EXIF date, dimensions, DPI, megapixels, orientation, caption, rating, tag, any metadata field, and full path, remembers sort per folder with a custom drag order, groups by any attribute or processed state with collapsible groups, filters by rating, category, label, and advanced criteria, and offers the full set of selection commands.
- **Depends On:** §4
- **Phase:** 32
- **Surface:** UI. Fidelity: docs/captures/lumen/file-list/. Job: a user orders and narrows a folder to what they need and selects it in one step. Treatment: ACDSee's Sort, Group, Filter, and Select menus with group headers, table of contents, and select-group-by-header. Chrome: consume §4 and the catalog's indexed columns. Cheaper substitute that fails: sort by name only.
- **Runs:** `Requires: display-session -- grouping and selection need an interactive desktop`
- **Catalog:** LP-0209 to LP-0213, LP-1058 (6 features)
- **Source:** `-> SOURCE: parity-lumen-browse-sort`
- **Hints:**
  - `BrowseSort` (LP-0211): natural name sort (`StrCmpLogicalW` semantics), size, type, dates, EXIF date, dimensions, DPI, megapixels, orientation, caption, rating, tag, any metadata field, direction, full path; extends `D04 T01 §8`.
  - Per-folder sort memory and custom drag order (LP-0213) stored in the catalog's `browsed_folders`.
  - Grouping (LP-0210, LP-1058): any attribute or processed state (developed, edited), collapsible groups, hover preview, table of contents, group order, select group by header.
  - Filters (LP-0209): rating, category, label, advanced filters sharing `D04 T06 §4`'s rule model when present, otherwise the `D04 T01 §8` filter set.
  - Selection (LP-0212): click, Ctrl, Shift, select all, all files, all images, tagged, by rating, clear, invert, auto-select new files.
  - Tests: `BrowseSortTests` (natural order table, metadata sorts), `BrowseGroupTests`, `SelectionCommandTests`.
  - Commit: `"lumen: sort, group, filter, and select in browse"`
- **Proof:** unit plus driven: the tests pass; a grouped and filtered 5,000-file folder responds under 200 ms (quoted); cheaper substitute that fails: ordinal string sort, which the natural-order table catches.

#### §6. File operations: copy, move, rename, delete, and undo

- **Deliverable:** Photos are copied, moved, renamed inline, and deleted to the Recycle Bin from browse, with sidecars, related files, and RAW+JPEG partners traveling together, catalog records following, a collision policy and replace dialog, the file clipboard and drag and drop with other programs, pixel or path copy to the clipboard, the Explorer context menu, and an undo journal.
- **Depends On:** §4
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/file-operations/. Job: a user organizes files on disk from Lumen without breaking the catalog or losing a sidecar, and can undo a mistake. Treatment: ACDSee's Copy To and Move To dialogs (folder tree, recent folders, create folder), the Confirm File Replace dialog (both thumbnails, replace, rename to, skip, delete source or destination, apply to all), inline rename, and the shell context menu. Chrome: consume `IFileOperation` (Windows) for copy, move, and recycle, the catalog, and `D04 T11 §3`'s journal. Cheaper substitute that fails: `File.Move` of the image alone.
- **Runs:** `Requires: display-session -- file dialogs, drag and drop, and the shell menu need an interactive desktop`
- **Catalog:** LP-0214 to LP-0225, LP-0973 (13 features)
- **Source:** `-> SOURCE: parity-lumen-file-operations`
- **Hints:**
  - `FileOperationService` in `Photon.Lumen.Core/Browse/Files/` over `IFileOperation`: copy (LP-0214), copy to and move to with folder tree, recent folders, create folder, drag onto tree folders (LP-0217).
  - Delete to the Recycle Bin with confirmation settings (LP-0215), `Lumen.Browse.ConfirmDelete`; permanent delete only with Shift and a named confirmation.
  - Inline rename of a file or folder, click to edit (LP-0216); batch rename is `D04 T11 §3` and shares `RenameJournal`.
  - Sidecars, related files, RAW+JPEG partners, and catalog records travel together (LP-0218, LP-0225, LP-0223); moves outside Lumen reconnect through `D04 T06 §8`.
  - Collision policy (LP-0219): ask, rename with separator, replace, skip; the Confirm File Replace dialog (LP-0222) with both thumbnails and apply to all.
  - File clipboard and drag and drop (LP-0221, LP-0973): cut, copy, paste files keeping catalog data, drag to other programs (`CF_HDROP` plus a PNG for pixel targets), confirm drag moves.
  - Copy image pixels or path to the clipboard (LP-0220).
  - Windows Explorer context menu in the file list (LP-0224) through `IContextMenu` hosting.
  - Undo journal: every operation undoable from Edit, Undo while the files are still where Lumen put them; Recycle Bin restores through the shell.
  - Tests: `FileOperationServiceTests` (sidecar and pair travel, collision policies, catalog follow-up, undo), `DragDropFormatTests`.
  - Commit: `"lumen: file operations with sidecars, pairs, and undo"`
- **Proof:** unit plus driven: the tests pass; a driven move of 200 RAW+JPEG pairs with sidecars between drives is undone and the catalog is quoted consistent; cheaper substitute that fails: moving images without sidecars, which the travel test catches.

#### §7. Info palette, properties, and compare images

- **Deliverable:** The information palette overlays camera and exposure data on the image, and Compare Images shows up to four photos with a comparison list, layouts, synchronized zoom and pan, analysis (exposure warning, property differences in bold, histograms, a difference image), and culling and file actions, extending the two-up compare of `D04 T01 §9`.
- **Depends On:** §4, D04 T01 §9
- **Phase:** 32
- **Surface:** UI. Fidelity: docs/captures/lumen/compare/ (baseline from `D04 T01 §9`), new captures to docs/captures/lumen/info-palette/. Job: a user picks the best of a burst by comparing sharpness and settings side by side. Treatment: ACDSee's Compare Images viewer (up to four, comparison list, send to view, drag in, swap, remove, layouts, zoom and pan lock, exposure warning, bold differences, histograms, tag, rate, categories, save as a new file, delete) and Info Palette. Chrome: extend `D04 T01 §9`'s compare view model, the histogram control, and §6's recycle. Cheaper substitute that fails: two windows opened side by side.
- **Runs:** `Requires: display-session -- compare and the palette need an interactive desktop`
- **Catalog:** LP-0226 to LP-0231 (6 features)
- **Source:** `-> SOURCE: parity-lumen-compare`
- **Hints:**
  - Compare up to four (LP-0226): comparison list, send to view, drag in, swap next or previous, remove, layouts one to four.
  - Zoom and pan (LP-0229): actual size, fit, fit width and height, zoom to, zoom lock, pan lock.
  - Analysis (LP-0230): exposure warning overlay, property differences in bold, per-image histograms, metadata field setup.
  - Current versus another (LP-0231): synced zoom and scroll, next and previous, difference image rendered as an absolute difference.
  - Actions (LP-0228): tag, tag all, rate, categories, save as a new file (never the original), delete to the Recycle Bin.
  - Information palette (LP-0227): camera, lens, dimensions, size, exposure program, white balance, metering, flash, RAW, ISO, aperture, shutter, compensation, focal length, chosen position and opacity.
  - Tests: `CompareViewModelTests` (four-up sync, lock, difference image values), `InfoPaletteTests`.
  - Commit: `"lumen: four-up compare with analysis and the information palette"`
- **Proof:** unit plus driven: the tests pass; a driven four-up compare with zoom lock is captured; cheaper substitute that fails: static side-by-side images, which the sync test catches.

#### §8. Image basket and selective browsing

- **Deliverable:** Up to five image baskets collect files across folders from browse, the viewer, or Explorer; selective browsing combines folder, catalog, and date criteria with match any or all; and file lists load and save as text files.
- **Depends On:** §5
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/basket/ and docs/captures/lumen/selective-browsing/. Job: a user gathers photos from many folders for one task without moving them. Treatment: ACDSee's Image Basket pane (baskets, add, remove, clear, rename, delete, active basket) and Selective Browsing pane (criteria rows, include toggles, any or all, auto hide). Chrome: consume §5, the catalog, and `D04 T06 §7`'s criteria model when present. Cheaper substitute that fails: a temporary collection that copies files.
- **Runs:** `Requires: display-session -- the panes need an interactive desktop`
- **Catalog:** LP-0232 to LP-0235 (4 features)
- **Source:** `-> SOURCE: parity-lumen-basket`
- **Hints:**
  - `ImageBasketService` (LP-0233): up to five baskets persisted in the catalog, add from browse, the viewer (LP-0234, a viewer command forwarded to Lumen), or Explorer (drop onto the pane), active basket, remove, clear, rename, delete.
  - Selective browsing (LP-0232): criteria rows over folders, catalog fields, and dates, include toggles, match any or all, remove and clear, auto hide.
  - File lists (LP-0235): load and save a text list of paths (UTF-8, one per line), shared with `D04 T11 §10`.
  - Baskets hold references only; no file moves.
  - Tests: `ImageBasketTests`, `SelectiveBrowsingTests`, `FileListTextTests`.
  - Commit: `"lumen: image baskets and selective browsing"`
- **Proof:** unit plus driven: the tests pass; a driven basket filled from three folders and the viewer is captured; cheaper substitute that fails: a basket that copies files, which the no-move assertion catches.

#### §9. The private folder

- **Deliverable:** A password-protected, encrypted vault under Lumen's app data: create, open, close (hidden when closed), add files with a warning (catalog data removed, originals moved in after verification), restore to a normal folder, delete, and no password recovery.
- **Depends On:** §6
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/private-folder/. Job: a user keeps some photos out of sight on a shared machine. Treatment: ACDSee's Private Folder (create with password, open, close, add, restore, delete) with an explicit statement that it is not disk encryption and that a lost password cannot be recovered. Chrome: consume `AesGcm` and `Rfc2898DeriveBytes` from .NET, §6's verified moves, and `Photon.UI` dialogs. Cheaper substitute that fails: a hidden folder attribute.
- **Runs:** `Requires: display-session -- the vault dialogs need an interactive desktop`
- **Catalog:** LP-0236 to LP-0237 (2 features)
- **Source:** `-> SOURCE: parity-lumen-private-folder`
- **Hints:**
  - `PrivateVault` in `Photon.Lumen.Core/Browse/Private/`: PBKDF2-SHA256 (600,000 iterations, per-vault salt) key, AES-256-GCM per file with a random nonce, an encrypted index; files stored under `%LOCALAPPDATA%\Rizonesoft\Lumen\private\` (LP-0236).
  - Create, open, close, hidden when closed; decrypt to memory only for viewing, never to a temp file.
  - Add files (LP-0237): warning, move in with verification (decrypt and compare hash) before the source is recycled, catalog data removed; restore to a normal folder; delete.
  - No recovery: the dialog says so; a wrong password is refused with a delay.
  - Tests: `PrivateVaultTests` (round trip, wrong password, tamper detection by GCM tag, no plaintext on disk after close).
  - Commit: `"lumen: an encrypted private folder"`
- **Proof:** unit plus driven: the tests pass; a driven add, close, reopen, restore cycle is captured with source and restored hashes quoted equal; cheaper substitute that fails: a hidden attribute, which the no-plaintext test catches.

#### §10. Calendar and timeline browsing

- **Deliverable:** A calendar pane browses by events, years, months, and days with a photo calendar, hover previews, a table of contents, skipped empty dates, a chosen date basis, filters, week start and clock options, and per-date events with a description and chosen thumbnail.
- **Depends On:** §2
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/calendar/. Job: a user finds photos by when they were taken without knowing the folder. Treatment: ACDSee's Calendar pane (events, year, month, day views, photo calendar, floating pane) and its options. Chrome: consume the catalog's indexed dates and the preview cache. Cheaper substitute that fails: a date-range filter only.
- **Runs:** `Requires: display-session -- the calendar pane needs an interactive desktop`
- **Catalog:** LP-0238 to LP-0241 (4 features)
- **Source:** `-> SOURCE: parity-lumen-calendar`
- **Hints:**
  - `CalendarViewModel` (LP-0238): events, year, month, day views, photo calendar with hover previews, table of contents, skip empty dates, floating pane.
  - Date basis (LP-0239): catalog date, date taken, modified, created, loaded, `Lumen.Browse.Calendar.DateBasis`.
  - Options (LP-0240): filters, images and media only, start of week, 12 or 24 hour clock.
  - Events (LP-0241): description and chosen thumbnail per date, restore default thumbnail, stored in the catalog.
  - Counts come from indexed queries, not enumeration; response under 200 ms on the 50,000-image catalog.
  - Tests: `CalendarQueryTests` (counts per basis and time zone), `CalendarEventTests`.
  - Commit: `"lumen: calendar browsing"`
- **Proof:** unit plus driven: the tests pass with query timing quoted; captures committed; cheaper substitute that fails: enumerating folders per click, which the timing catches.

#### §11. Duplicate finder

- **Deliverable:** Content-identical duplicates are found on demand (one list or two, files and folders, subfolders, exact content or same name, images only) and automatically for the whole catalog, grouped as stacks in a duplicates view with status, set as original, remove, hide and show hidden, and reviewed with previews, marks, recycle, and rename.
- **Depends On:** §2, §6
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/duplicates/. Job: a user reclaims space and removes accidental copies without losing a keeper. Treatment: ACDSee's Duplicate Finder wizard (setup, review, finish) and Lightroom's duplicates view with set-as-original. Chrome: consume §2's hashes, §6's recycle, and the stacks of `D04 T06 §3` when present. Cheaper substitute that fails: matching by file name only.
- **Runs:** `Requires: display-session -- the finder and duplicates view need an interactive desktop`
- **Catalog:** LP-0242 to LP-0245 (4 features)
- **Source:** `-> SOURCE: parity-lumen-duplicates`
- **Hints:**
  - `DuplicateFinder` (LP-0244): one or two lists, files and folders, subfolders, exact content (size, then xxHash64 of the first 64 KB, then SHA-256) or same name, images only.
  - Automatic detection for the catalog (LP-0243) as a setting, run by the indexer.
  - Duplicates view (LP-0242): groups as stacks with status, set as original, remove, hide and show hidden.
  - Review (LP-0245): sort sets, preview, mark for deletion, delete from list 1 or 2 to the Recycle Bin, rename, review and finish.
  - Visually similar photos are `D04 T10 §5`, and the dialog says so.
  - Tests: `DuplicateFinderTests` (content, name, two-list modes; a same-size different-content pair is not a duplicate).
  - Commit: `"lumen: duplicate finder and duplicates view"`
- **Proof:** unit plus driven: the tests pass; a driven run over a folder with 100 planted duplicates finds exactly 100 with timing quoted; cheaper substitute that fails: size-only matching, which the different-content pair catches.

#### §12. Archives and folder sync

- **Deliverable:** Lumen browses inside ZIP, RAR, 7z, ARJ, CAB, GZ, TAR, and TGZ archives like folders (archives listed in the tree and grouped with folders), extracts to a folder, creates ZIP archives (with password, subfolders, hidden files, add to or overwrite) with optional recycling of sources after a verified archive, and runs saved folder-sync jobs that mirror folders to a backup location on a schedule.
- **Depends On:** §6
- **Phase:** 32
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/archives/ and docs/captures/lumen/sync/. Job: a user opens a zipped shoot without unpacking it and keeps a backup copy of their photo folders current. Treatment: ACDSee's Create Archive and Extract dialogs and Sync wizard (source, destination, error and log options, conflicts, name, schedule, edit, run saved syncs). Chrome: consume SharpCompress (MIT) moved with `D03 T17 §12`'s archive opener to `Photon.Core/Formats/Archives/`, `System.IO.Compression` for writing ZIP, §6, and the settings store. Cheaper substitute that fails: extracting every archive to a temp folder to browse it.
- **Runs:** `Requires: display-session -- the archive and sync dialogs need an interactive desktop`
- **Catalog:** LP-0246 to LP-0250, LP-0974 (6 features)
- **Source:** `-> SOURCE: parity-lumen-archives-sync`
- **Hints:**
  - First item: move `D03 T17 §12`'s archive opener (SharpCompress, MIT) from Imago to `src/Photon.Core/Formats/Archives/`; Imago repoints; no copy.
  - Archive browsing (LP-0250, LP-0974): ZIP, RAR, 7z, ARJ, CAB, GZ, TAR, TGZ as virtual folders read-only, listed in the tree and grouped with folders; entries decode through the registry from a stream.
  - Extract (LP-0249): target folder, create folder, collision policy from §6.
  - Create archive (LP-0247): ZIP only (RAR and 7z creation are not offered), settings, subfolders, hidden files, password (ZipCrypto refused in favor of AES through SharpCompress where supported, recorded), output file, add to or overwrite an existing archive.
  - Remove sources after a verified archive (LP-0248): reopen the archive and compare every entry's hash, then recycle through §6; never an unverified delete.
  - Folder sync (LP-0246): `SyncJob` (source, destination, mirror or update, error and log options, conflict rule, name, schedule through the same scheduled-task path as §2), edit and run saved syncs, logs in the Activity Manager.
  - Tests: `ArchiveBrowseTests` (each format fixture), `CreateArchiveTests` (verification before recycle), `SyncJobTests` (mirror, update, conflicts).
  - Commit: `"lumen: archives and folder sync"`
- **Proof:** unit plus driven: the tests pass; a driven browse of a 7z fixture and a sync run to a second drive are captured with the log quoted; cheaper substitute that fails: unzip to temp, which the no-temp-files assertion catches.

#### Sizing concerns

- §4 and §6 each carry 11 to 13 features with UI-heavy items; §4's natural split if it passes 30 is "views and thumbnails" versus "overlays and columns", and §6's is "file operations" versus "clipboard, drag and drop, and the shell menu".
- §2 depends on the scheduled-task decision; if `Microsoft.Win32.TaskScheduler` (MIT) is rejected, `schtasks.exe` is the recorded fallback and costs two items.
- §12 combines archives and sync because both are file-management jobs over the same service; split at authoring if sync scheduling grows.

### todo/04-lumen/TODO-06-lumen-parity-library.md -- `lumen-parity-library`

- **Title:** "TODO-06 -- Lumen Parity: Library, Collections, Search, and the Catalog"
- **Phase(s):** 33
- **Goal:** Lumen's library reaches Lightroom Classic and ACDSee parity on top of the 0.1.0 grid, loupe, and catalog: every grid, loupe, filmstrip, survey, and second-window view option; label sets, flag and rating cycles, ACDSee tagging, and configurable auto advance; stacks, auto-stacks, and virtual copies; the full filter bar with text rules, attribute filters, metadata browser columns, and filter presets; collection sets, target and quick collections, and a smart-collection rule editor with every criterion; ACDSee categories, auto categories, and special items; quick and advanced search with saved searches and disk search; the Folders and Catalog panels with synchronize, relocate, missing-photo recovery, and offline volumes; scheduled catalog backup and maintenance (promoting B-036); multiple catalogs with import from Lumen, Lightroom Classic, and Photoshop Elements catalogs; smart previews for offline editing; the dashboard; and the Painter and Quick Develop. The code lives in `src/Lumen/Photon.Lumen.Core/` (`Catalog/`, `Library/`, `Search/`, `Collections/`, `Maintenance/`, `CatalogExchange/`, `SmartPreviews/`) and `src/Lumen/Photon.Lumen.Desktop/` (`Library/`, `Panels/`, `Dashboard/`); it extends `D04 T01 §5` to `§11` in place and never writes an original image.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code; the library it extends is planned in `D04 T01 §8` to `§11`. `<!-- claim: absent src/Lumen -->` `<!-- claim: exists todo/04-lumen/TODO-01-lumen-foundation.md -->`
  - The catalog location is already a setting named in the foundation file, and catalog maintenance waits in the backlog as B-036. `<!-- claim: count "Lumen.Catalog.Path" todo/04-lumen/TODO-01-lumen-foundation.md = 1 -->` `<!-- claim: count "^- \[B-036\]" todo/backlog.md = 1 -->`
  - The preview cache size setting the preview-management section extends is named in the foundation file. `<!-- claim: count "Lumen.Cache.SizeMB" todo/04-lumen/TODO-01-lumen-foundation.md = 1 -->`
  - `standards/lumen.md` requires forward-only migrations and a backup before each. `<!-- claim: count "forward-only migrations" standards/lumen.md = 1 -->`
- **Inputs and XREFs:** `standards/lumen.md` (catalog, original-file guard), `standards/shared.md`, `standards/testing.md`; SQLite 3 documentation (`VACUUM`, `PRAGMA integrity_check`, `REINDEX`, the online backup API); Lightroom Classic's `.lrcat` schema as observed read-only (tables `Adobe_images`, `AgLibraryFile`, `AgLibraryFolder`, `AgLibraryKeyword`, `AgLibraryCollection`) for the import-only reader; -> XREF: D04 T01 §5 (the catalog every section migrates forward); -> XREF: D04 T01 §7 (previews §10 manages and §11 extends); -> XREF: D04 T01 §8 (grid, sort, and filter bar §1, §4 extend); -> XREF: D04 T01 §9 (loupe, compare, and filmstrip §1 extends); -> XREF: D04 T01 §10 (keywords, collections, smart collections, and statistics §5 and §12 extend); -> XREF: D04 T01 §11 (culling keys and auto advance §2 extends); -> XREF: D04 T02 §7 (the basic stacks §3 extends); -> XREF: D04 T02 §8 (Lumen 0.1.0 ships first); -> XREF: D04 T05 §2 (the indexer §8's synchronize and rebind reuse); -> XREF: D04 T05 §4 (browse views share §1's cell renderer); -> XREF: D04 T13 §7 (the DNG writer smart previews use); -> XREF: D03 T15 §4 (the HDR display path §1 consumes for HDR photos); -> XREF: D01 T07 §1 (the tone stages Quick Develop drives relatively); -> XREF: D04 T12 §4, D04 T12 §7, D04 T12 §9, D04 T12 §10 (output creations §5 saves as collections); -> XREF: D04 T10 §3 (people entries in §6's catalog pane); -> XREF: D04 T10 §5 (similarity search offered from §7).
- **Adjacency:** list=applicable @ D04 T06 §1 (grid, survey, filmstrip, and every panel list); document=not-applicable (the library prints nothing; output is D04 T12); settings=applicable (every view, culling, filter, backup, and preview option is a `Lumen.*` key with a default and a consumer); reporting=applicable @ D04 T06 §12 (dashboard and statistics, catalog maintenance reports in §9); notifications=applicable (backup, optimize, synchronize, and catalog import run with progress, cancel, and a summary); permissions=applicable (read-only volumes, locked catalogs, missing folders, and offline media refused or badged by name); audit=applicable (one Serilog Information line per catalog-changing command and per maintenance run); exchange=applicable (smart-collection settings, keyword and catalog exports, Lightroom and Elements catalog import, catalog export with negatives); reverse=applicable (every library command undoes through the suite history; backups restore; remove-from-catalog is undoable until the session ends)

#### §1. Library view extensions: cell styles, overlays, survey, and a second window

- **Deliverable:** The grid, loupe, filmstrip, and compare views gain every Lightroom and ACDSee view option, a survey view, loupe overlays and info sets, full sort orders with custom order, selection commands, HDR display of HDR-edited photos, and a secondary display window with its own view and filter.
- **Depends On:** D04 T02 §8, D04 T05 §4
- **Phase:** 33
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/ (baseline from `D04 T01 §8`), new captures to docs/captures/lumen/survey/ and docs/captures/lumen/second-window/. Job: a photographer arranges the library exactly as they cull, reads the information they care about on every cell, and uses a second monitor as a full-size loupe or survey while the main window stays on the grid. Treatment: View, View Options dialog with Grid and Loupe tabs (compact and expanded cells, extras, hover-only items, label tint, index numbers, header and rating footer, tooltips, two loupe info sets); N enters Survey; the Window, Secondary Display menu with Grid, Loupe (normal, live, locked), Compare, Survey, and Slideshow and a monitor chooser. Cheaper substitute that fails: a second window that mirrors the main one. Chrome: consume the `D04 T01 §8` virtualizing grid and `D04 T01 §9` loupe (extended, not replaced), `Photon.UI` theme, the settings store, and the icon catalog.
- **Runs:** `Requires: display-session -- view options, the survey, and the second window need an interactive desktop with two monitors or a virtual second display`
- **Catalog:** LP-0254 to LP-0267 (14 features)
- **Source:** `-> SOURCE: parity-lumen-library-views`
- **Hints:**
  - `GridCellOptions` and `LoupeInfoOptions` records in `Photon.Lumen.Core/Library/Views/` (LP-0264, LP-0256, LP-0265): compact and expanded styles, extras, hover-only items, label tint, cell icons, index numbers, header and footer fields, and two configurable loupe info sets cycled with I, shown briefly or always, with the loading and embedded-preview messages; stored as `Lumen.Library.Grid.*` and `Lumen.Library.Loupe.*`.
  - Filmstrip (LP-0254): source indicator with recent sources, quick filter, rating and stack-count badges, tooltips, navigator hover, and an unsynced badge; extends `D04 T01 §9`'s filmstrip.
  - Loupe (LP-0259, LP-0260): zoom ratios 1:16 to 11:1 with zoom-position lock and a Navigator panel; overlays for grid, draggable guides, and a layout image (PNG with opacity and matte) with an overlay edit mode.
  - Compare swap and make select (LP-0257) and Survey view (LP-0258): N shows the selection sized to fit, a cell's X removes it from the survey without deselecting.
  - Sort orders (LP-0261, LP-0262): capture, added, edit time, edit count, rating, pick, label, name, extension, type, aspect, reverse; a `custom_order` column per folder and collection filled by drag, disabled with a tooltip when the source mixes folders.
  - Selection commands (LP-0263): select all, none, active only, by flag, rating, and label with add, intersect, remove, and invert, and the active versus selected photo distinction the Painter and sync consume.
  - `SecondaryWindow` in `Photon.Lumen.Desktop/Library/` (LP-0255): its own view mode, filter bar, and monitor, following the main selection in live mode and freezing in locked mode; ACDSee's second-monitor image view maps to Loupe live.
  - HDR display (LP-0266): HDR-edited photos render through the `D03 T15 §4` HDR swap chain path when `Lumen.Library.HdrDisplay` is on and the monitor reports advanced color, SDR tone-mapped otherwise.
  - Remember the last selected photo per recent source (LP-0267) in `Lumen.Library.LastSelection`.
  - Tests: `GridCellOptionsTests`, `LibrarySortTests` (every order on a seeded catalog, custom order persists across restart), `SelectionCommandTests`, `SecondaryWindowViewModelTests` (live versus locked).
  - Commit: `"lumen: library view options, survey, loupe overlays, and a second window"`
- **Proof:** unit plus driven: the sort and selection tests pass on a seeded 5,000-photo catalog and a driven session shows the survey and a locked second window on a second display (captures committed, grid frame time still under 16 ms, quoted); cheaper substitute that fails: a mirrored second window, which the locked-mode test catches.

#### §2. Culling extensions: label sets, flag and rating cycles, tagging, and auto advance

- **Deliverable:** Culling gains label sets with custom names, flag increase and decrease and the Refine pass, delete rejected photos, every rating and label entry path, ACDSee tagging, numeric-keypad culling, and configurable auto advance per metadata kind in the library and the viewer.
- **Depends On:** §1
- **Phase:** 33
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/, new captures to docs/captures/lumen/label-sets/. Job: a photographer culls a shoot entirely from the keyboard in the scheme they already know (Lightroom flags and stars or ACDSee tags and labels) and never loses a decision. Treatment: Metadata, Color Label Set submenu with Edit (rename five labels, save, switch, delete sets); Ctrl+Up and Ctrl+Down cycle flags; Library, Refine Photos; Photo, Delete Rejected Photos with Remove from Catalog or Move to Recycle Bin; tag checkbox and reject mark on thumbnails; an Auto Advance toolbar toggle with a per-kind options page. Cheaper substitute that fails: auto advance for ratings only. Chrome: consume `D04 T01 §11`'s culling commands (extended), the suite history, and the settings store.
- **Runs:** `Requires: display-session -- keyboard culling and the label-set dialog need an interactive desktop`
- **Catalog:** LP-0268 to LP-0280 (13 features)
- **Source:** `-> SOURCE: parity-lumen-culling`
- **Hints:**
  - `LabelSet` in `Photon.Lumen.Core/Library/Culling/` (LP-0269): five named colors, built-in Lightroom-style and ACDSee-style sets, user sets in `Lumen.Culling.LabelSets`; the XMP label text written by `D04 T01 §11` follows the active set's names so Lightroom reads them.
  - Flag cycle (LP-0268) and Refine Photos (LP-0270): unflagged become rejects and picks reset, one undo step with a count in the log line.
  - Delete Rejected Photos (LP-0271): a dialog offering Remove from Catalog or Move to Recycle Bin (`FileSystem.DeleteFile` with `RecycleOption.SendToRecycleBin`), never a permanent delete, with sidecar and RAW+JPEG partner moved together.
  - Rating and label entry paths (LP-0272, LP-0276): hover stars and label chips on thumbnails, drag-to-rate, catalog-pane drop targets, Set Rating and Set Label commands, status-bar and Properties fields, clear and reset.
  - Tagging (LP-0279, LP-0280): an ACDSee-compatible `tagged` flag stored in the catalog and as `acdsee:tagged` is not written; Lumen writes `lumen:tagged` in its own XMP namespace; tag keys, tagged and rejected lists, clear tags, and tagging from the viewer and compare.
  - Numeric keypad culling (LP-0278): keypad bindings for tag, labels, ratings, remove, next, and previous, registered with `D04 T14 §3`'s keymap later and working from day one through the library's key table.
  - `AutoAdvanceOptions` (LP-0273, LP-0274, LP-0277): per kind (tag, rating, label, category, keyword), per mode (library and viewer), after keyword entry, with the toolbar toggle; extends `D04 T01 §11`'s single auto-advance switch.
  - Ratings and labels groups in the catalog pane (LP-0275) count photos and filter on click.
  - Tests: `LabelSetTests` (rename round-trip into XMP), `RefinePhotosTests`, `DeleteRejectedTests` (catalog removal and Recycle Bin with a temp folder, undo of catalog removal), `AutoAdvanceTests` (each kind and mode).
  - Commit: `"lumen: label sets, flag cycles, tagging, and configurable auto advance"`
- **Proof:** unit plus driven: the culling tests pass and a driven 200-photo keyboard cull with the keypad and auto advance is logged one line per decision; the unchanged-originals assertion over the fixtures still holds after Delete Rejected with Remove from Catalog; cheaper substitute that fails: a permanent delete, which the Recycle Bin test catches.

#### §3. Stacks, versions, and virtual copies

- **Deliverable:** Stacks gain every command, auto-stacking by capture time and GPS distance with a live preview, stacks inside collections, and stored rules for how a collapsed stack behaves, and virtual copies arrive with names and set-copy-as-master.
- **Depends On:** §1
- **Phase:** 33
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/, new captures to docs/captures/lumen/stacks/. Job: a photographer groups bursts, brackets, and edits into one cell and keeps several interpretations of one negative without duplicating the file. Treatment: Photo, Stacking submenu (Group, Unstack, Remove, Split, Collapse and Expand one or all, Move to Top, Up, Down), Auto-Stack by Capture Time dialog with a seconds slider, GPS distance, presets, and live counts; Photo, Create Virtual Copy (Ctrl+'); Set Copy as Master. Cheaper substitute that fails: stacks as a collection. Chrome: consume `D04 T02 §7`'s stack table (extended), the edit stack of `D04 T02 §1` for virtual copies, and the history.
- **Runs:** `Requires: display-session -- stack commands and the auto-stack dialog need an interactive desktop`
- **Catalog:** LP-0281 to LP-0286 (6 features)
- **Source:** `-> SOURCE: parity-lumen-stacks`
- **Hints:**
  - `StackService` in `Photon.Lumen.Core/Library/Stacks/` over `D04 T02 §7`'s stack table (LP-0281): group, unstack, remove, split, collapse and expand one or all, move to top, up, and down, member counts on the badge.
  - `AutoStacker` (LP-0282): gap threshold by capture time and a GPS distance limit, presets, a dry-run count shown live, replace or keep existing stacks, one undo step.
  - Stack rules (LP-0286): members in one folder by default with a multi-folder option, a collapsed stack acts as its head for rating and filter, exclusions, visibility by mode, all stored in the catalog.
  - Stacks in collections (LP-0283): a collection stores its own stacking, independent of the folder's.
  - `VirtualCopy` (LP-0284, LP-0285): a catalog record sharing the file with its own edit stack and metadata overrides, a Copy Name field, and Set Copy as Master swapping roles; virtual copies write their XMP only into exported copies because a sidecar belongs to the master.
  - Tests: `StackServiceTests`, `AutoStackerTests` (a 300-photo burst fixture with known gaps), `VirtualCopyTests` (edit independence, set master, delete copy leaves the file).
  - Commit: `"lumen: full stacking, auto-stack, and virtual copies"`
- **Proof:** unit plus driven: the stacking and virtual-copy tests pass and a driven auto-stack of the burst fixture matches the expected stack count (captured); cheaper substitute that fails: duplicating the file for a virtual copy, which the file-count assertion catches.

#### §4. The filter bar extended: text, attributes, metadata columns, and presets

- **Deliverable:** The library filter bar gains Lightroom's Text, Attribute, and Metadata tabs with every field, operator, and column, filter presets, and a lock across sources.
- **Depends On:** §1
- **Phase:** 33
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/, new captures to docs/captures/lumen/filter-bar/. Job: a photographer narrows 50,000 photos to the ones they want in a few clicks by text, attributes, or cascading metadata columns, and reuses the filter. Treatment: the `D04 T01 §8` bar grows Text (field and rule pickers with `!` and `+` operators), Attribute (flag, edited, rating comparison, label, kind, stacked), and Metadata (up to eight cascading columns, flat or hierarchical, multi-select) tabs, a preset menu, None, and a lock icon. Cheaper substitute that fails: a single search box. Chrome: consume `D04 T01 §8`'s `LibraryViewModel` queries (extended with indexes), the settings store, and the icon catalog.
- **Runs:** `Requires: display-session -- the filter bar needs an interactive desktop`
- **Catalog:** LP-0308 to LP-0320 (13 features)
- **Source:** `-> SOURCE: parity-lumen-filter-bar`
- **Hints:**
  - `LibraryFilter` model in `Photon.Lumen.Core/Search/Filters/` compiled to parameterized SQL (LP-0309): None, enable and disable, find (Ctrl+F focuses Text).
  - Text filter (LP-0311, LP-0312): any searchable field, filename, copy name, title, caption, keywords, searchable metadata, IPTC, EXIF; rules contains, contains all, contains words, does not contain, starts with, ends with; `!` negates and `+` anchors a word.
  - Attribute filter (LP-0308): flag, edited state, rating with at least, at most, and equal, color label including custom and none, kind (master, virtual copy, video), stacked status.
  - Metadata columns (LP-0313 to LP-0320): a column registry with counts per value from grouped queries: dates (date, year and month, day and month), file and attributes, camera and exposure (camera, serial, lens, focal length, shutter, aperture, ISO, flash), location (has GPS, GPS, sublocation, city, state, country), IPTC creator, copyright status, job, develop state (aspect, HDR, depth, masking, remove modes, point color, smart preview, snapshots, treatment, metadata status), AI edits (has AI, generative, needs update, edit type, removal, denoise, raw details, super resolution); columns whose data a later phase adds show zero counts, never an error.
  - Presets and lock (LP-0310): built-in and user presets in `Lumen.Library.FilterPresets`, a lock that carries the filter across folders and collections.
  - Indexes added by a forward migration for every filterable column; `FilterPerformanceTests` asserts under 200 ms on 50,000 photos, the `D04 T01 §8` budget.
  - Tests: `TextFilterTests` (each rule and operator), `AttributeFilterTests`, `MetadataColumnTests` (cascading counts), `FilterPresetTests`.
  - Commit: `"lumen: the full filter bar with text, attributes, metadata columns, and presets"`
- **Proof:** unit plus driven: the filter tests pass and the 50,000-photo response time is quoted under 200 ms; cheaper substitute that fails: filtering in memory after loading every record, which the timing catches.

#### §5. Collections extended: sets, target and quick collections, and the smart-collection rule editor

- **Deliverable:** Collections gain sets and nesting, a target collection and the Quick Collection, removal from one or all collections, a smart-collection editor with nested rule groups and every Lightroom criterion, import and export of smart-collection settings, collection filtering and labels, and output creations saved as collections.
- **Depends On:** §4
- **Phase:** 33
- **Surface:** UI. Fidelity: docs/captures/lumen/collections/ (baseline from `D04 T01 §10`), new captures to docs/captures/lumen/smart-collection-editor/. Job: a photographer groups work by project in nested sets, collects picks with one key, and keeps living smart collections on any attribute. Treatment: Create Collection and Create Collection Set dialogs, B adds to the target collection, Ctrl+B shows the Quick Collection, Save and Clear Quick Collection; the smart-collection editor with Match all, any, or none, rows grouped by Alt-click into nested groups, and criteria menus by family. Cheaper substitute that fails: smart collections limited to rating and date. Chrome: consume `D04 T01 §10`'s collection tables and rule engine (extended), §4's filter compiler, and the history.
- **Runs:** `Requires: display-session -- the collections panel and rule editor need an interactive desktop`
- **Catalog:** LP-0321 to LP-0338 (18 features)
- **Source:** `-> SOURCE: parity-lumen-collections`
- **Hints:**
  - Collection sets (LP-0324) as a parent table with nesting; Create Collection dialog (LP-0323) with include selected, make virtual copies, inside a set, and duplicate; add by drag, context menu, or the Organize tab; the Organize pane collections group (LP-0338).
  - Target collection and Quick Collection (LP-0321): one target at a time, B toggles membership, Quick Collection saved as a named collection and cleared; removal from the selected or all collections (LP-0322).
  - `SmartRule` tree in `Photon.Lumen.Core/Collections/Smart/` (LP-0325): all, any, none, nested groups, operators per data type, compiled through §4's SQL builder.
  - Criteria families: attributes (LP-0329), sources including folder, collection, publish collection, and exported (LP-0330), files including DNG fast-load data and bit depth (LP-0331), dates with absolute, relative, and range operators (LP-0332), camera and exposure (LP-0333), location and GPS (LP-0334), IPTC text (LP-0335), searchable text and metadata status (LP-0336), develop and AI state (LP-0337); criteria whose data arrives in a later phase are listed and match nothing until then.
  - Import and export of smart-collection settings (LP-0326) as Lightroom-compatible `.lrsmcol` Lua tables for the criteria both share (read and write), and Lumen JSON for the rest; unknown criteria are reported by name, never dropped silently.
  - Collections filter, sort, and color labels (LP-0327).
  - Output creations (LP-0328): a `kind` column (print, slideshow, web, book) so `D04 T12 §4`, `§7`, `§9`, and `§10` save their layouts as collections here.
  - Tests: `CollectionSetTests`, `QuickCollectionTests`, `SmartRuleCompilerTests` (every criterion family and nested groups on a seeded catalog), `SmartCollectionExchangeTests` (a Lightroom `.lrsmcol` fixture read and written back equal).
  - Commit: `"lumen: collection sets, quick collection, and the full smart-collection editor"`
- **Proof:** unit plus fidelity: the rule compiler tests pass and the `.lrsmcol` fixture round-trips with every shared criterion equal; a driven nested smart collection updates live when a rating changes (captured); cheaper substitute that fails: flat all-or-any rules, which the nested-group test catches.

#### §6. Categories and auto categories

- **Deliverable:** ACDSee's catalog pane arrives: hierarchical categories distinct from keywords, auto categories from metadata, special items, Easy-Select combinations, quick category sets, and the pane's options.
- **Depends On:** §5
- **Phase:** 33
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/catalog-pane/. Job: an ACDSee user finds photos the way they always have: by clicking categories, auto categories such as camera or year, and special items like Uncategorized, combined with match all or any. Treatment: a Catalog pane with Categories, Auto Categories, People, Ratings, Labels, Keywords, Saved Searches, and Special Items groups, Easy-Select bars to add a group to the match, and a quick-category button grid. Cheaper substitute that fails: categories stored as keywords. Chrome: consume the catalog, §5's rule compiler, the history, and the icon catalog.
- **Runs:** `Requires: display-session -- the catalog pane needs an interactive desktop`
- **Catalog:** LP-0339 to LP-0346 (8 features)
- **Source:** `-> SOURCE: parity-lumen-categories`
- **Hints:**
  - `Category` tree in `Photon.Lumen.Core/Catalog/Categories/` (LP-0341): create, edit, delete with confirmation, move, filter, assign and unassign, uncategorize, Set Categories command; written to sidecars as `lumen:categories` and on request as IPTC supplemental categories through `D04 T08 §8`.
  - Auto categories (LP-0342) computed from indexed metadata groupings (camera, lens, year, ISO bands, file type, commonly used), multi-select, combined with ratings, categories, and `D04 T05 §8`'s selective browsing.
  - Special items (LP-0343): all images, embed pending (from `D04 T08 §8`), uncategorized, no keywords, unnamed, auto-named, and suggested faces (from `D04 T10 §3`, empty until then), tagged, rejected.
  - Catalog pane (LP-0339, LP-0340): groups with counts, Easy-Select match all or any, click to search.
  - Options (LP-0344): icons, Easy-Select bar and tooltip, assign by clicking, delete confirmations; quick category sets (LP-0345) with rows, columns, and `Child < Parent` syntax.
  - Organize pane categories group (LP-0346).
  - Tests: `CategoryTreeTests`, `AutoCategoryTests` (seeded catalog groupings), `EasySelectTests`.
  - Commit: `"lumen: categories, auto categories, special items, and the catalog pane"`
- **Proof:** unit plus driven: category and Easy-Select tests pass and a driven Easy-Select combination returns the expected count on a seeded catalog (captured); cheaper substitute that fails: categories aliased to keywords, which the separate-XMP-field test catches.

#### §7. Quick search and advanced search

- **Deliverable:** A quick search bar with scope, match types, operators, and history; an advanced search pane with sources, criteria of every type, AND and OR, presets, and saved searches in the catalog pane; and a disk search for files and file metadata outside the catalog.
- **Depends On:** §4
- **Phase:** 33
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/search/. Job: a user types a word and finds matching photos across names, metadata, categories, keywords, and people, or builds a precise query they can rerun later, including over folders never indexed. Treatment: a search box with a scope menu and history; an Advanced Search pane (Match all, sources: catalog, folders, current view; file types; criterion picker; preset menu); Saved Searches in the catalog pane; Search Files (IrfanView) as a dialog whose results open in the browser. Cheaper substitute that fails: search limited to filenames. Chrome: consume §4's filter compiler, `D04 T05 §4`'s browser for disk results, and the settings store.
- **Runs:** `Requires: display-session -- the search pane needs an interactive desktop`
- **Catalog:** LP-0347 to LP-0359 (13 features)
- **Source:** `-> SOURCE: parity-lumen-search`
- **Hints:**
  - SQLite FTS5 table over names, captions, titles, keywords, categories, AI keywords, and people names, maintained by triggers (LP-0349, LP-0350); quick search scope, match types, classic operators, and history in `Lumen.Search.History`.
  - Advanced search (LP-0351): match all or any, sources, file types, criteria picker, AND and OR groups, per-criterion options, history; folder handling folders, folders and contents, contents only (LP-0353).
  - Criteria: filename with any or all terms, autocomplete, and wildcard sets, ranges, and escapes (LP-0354); text, people, keyword, category, rating, and label (LP-0355); metadata types string, date and time, lookup list, integer, rational, with literal semicolons (LP-0356).
  - Presets and saved searches (LP-0347, LP-0348, LP-0352) listed in the catalog pane and rerun with one click.
  - Disk search (LP-0357, LP-0358, LP-0359): name pattern, start folder with subfolders, file date range, and metadata text (EXIF, IPTC, comments, exact phrase, any present) read through the `D04 T08 §1` reader without cataloging; results shown as thumbnails in the browser.
  - Tests: `QuickSearchTests`, `AdvancedSearchCompilerTests`, `WildcardMatcherTests`, `DiskSearchTests` (temp folder with fixtures).
  - Commit: `"lumen: quick search, advanced search, saved searches, and disk search"`
- **Proof:** unit plus driven: the search tests pass; quick search over 50,000 photos answers under 200 ms (quoted); a saved search reruns from the catalog pane (captured); cheaper substitute that fails: `LIKE` scans, which the timing catches.

#### §8. Folders and catalog panels: synchronize, relocate, missing photos, and offline volumes

- **Deliverable:** The Folders panel shows volumes with free space and online status and supports add, create, rename, move, remove, synchronize, parent display, colors, and favorites; the Catalog panel lists all photographs, previous import, missing, and error sets; missing folders and photos are found and relocated, files moved outside Lumen are rebound, drives are remapped, and offline media (photo discs) stay browsable.
- **Depends On:** §1, D04 T05 §2
- **Phase:** 33
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/, new captures to docs/captures/lumen/folders-panel/ and docs/captures/lumen/missing-photos/. Job: a photographer keeps the catalog in step with the disk, finds what moved, and still sees photos on a disconnected drive or disc. Treatment: the Folders panel with volume headers (free space, counts, online dot), Synchronize Folder dialog (import new, remove missing, rescan metadata with a dry-run count), Find Missing Folder, Update Location, Show Parent, folder color and favorite badges, the Catalog panel entries, and an offline-volume manager. Cheaper substitute that fails: a folder list that goes stale until reimport. Chrome: consume the `D04 T05 §2` indexer and watcher, `D04 T05 §6`'s file operations for rename and move, the catalog, and the history.
- **Runs:** `Requires: display-session -- the panels and relocation dialogs need an interactive desktop`
- **Catalog:** LP-0360, LP-0365 to LP-0378 (15 features)
- **Source:** `-> SOURCE: parity-lumen-folders`
- **Hints:**
  - Volume model in `Photon.Lumen.Core/Catalog/Volumes/` (LP-0366, LP-0378): volume serial, label, type, online state, free space; offline volumes keep cached thumbnails browsable; photo discs identified by serial or label and rebound.
  - Folder operations (LP-0367, LP-0371, LP-0372, LP-0373): add, create, rename, move by drag, remove from catalog, show in Explorer, color labels, favorites, folder filter, subfolder display and path styles, go to folder and collection; rename and move go through `D04 T05 §6` and never touch image bytes.
  - `FolderSynchronizer` (LP-0368): new files imported in place, missing removed, metadata rescanned, with a dry-run preview.
  - Parent display (LP-0369) and missing folders (LP-0370): update location, find missing folder, alert on parent.
  - Catalog panel (LP-0360, LP-0365): all photographs, current and previous import, missing photographs, added by previous export, errors, updated photos.
  - Remove photos from catalog or Recycle Bin (LP-0374), find and locate missing photos (LP-0375), `RebindService` matching moved files by size, capture time, and hash (LP-0376), drive mapping on import or restore (LP-0377).
  - Tests: `FolderSynchronizerTests`, `RebindServiceTests` (files moved in a temp tree), `VolumeStateTests`, `MissingPhotoTests`.
  - Commit: `"lumen: folders and catalog panels with synchronize, relocate, and offline volumes"`
- **Proof:** unit plus driven: the tests pass; a driven session moves a fixture folder in Explorer, Lumen marks it missing, Find Missing Folder relocates it, and every rating survives (log lines and captures); cheaper substitute that fails: path-only matching, which the rebind test catches.

#### §9. Catalog backup and maintenance

- **Deliverable:** Scheduled catalog backups with an integrity test, optimize, compression, and retention, an ACDSee-style backup wizard including images, restore from backup, catalog locking, optimize and relaunch, database maintenance (per-folder records, orphans, rebinding, thumbnails), and a quarantine for files that fail to read.
- **Depends On:** §8
- **Phase:** 33
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/backup/ and docs/captures/lumen/maintenance/. Job: a photographer never loses years of ratings and edits to a corrupt or deleted catalog and can repair it when it misbehaves. Treatment: Catalog Settings, Backup page (schedule: never, on exit weekly, daily, every exit; folder; test integrity; optimize after; compress); the backup-on-exit dialog with Skip; a Backup and Restore wizard; File, Optimize Catalog and Relaunch and Optimize; a Database Maintenance dialog. Cheaper substitute that fails: a file copy of the open catalog. Chrome: consume the catalog, `Microsoft.Data.Sqlite` (MIT) online backup API, `System.IO.Compression`, and the settings store.
- **Runs:** `Requires: display-session -- the backup wizard and maintenance dialog need an interactive desktop`
- **Catalog:** LP-0379 to LP-0388 (10 features)
- **Source:** `-> SOURCE: lumen-roadmap-catalog` (promotes B-036)
- **Hints:**
  - `CatalogBackupService` in `Photon.Lumen.Core/Maintenance/` (LP-0381): SQLite online backup into a dated folder, `PRAGMA integrity_check` on the copy, optional optimize and ZIP, retention count `Lumen.Backup.Keep`, schedule `Lumen.Backup.Schedule`, skip once; runs before exit with progress.
  - Backup wizard (LP-0383): new or update backup, location, thumbnails, image and media files (copied, hash-verified, never moved), scopes, daily folders, reminder interval.
  - Restore (LP-0384): choose a backup, verify integrity, restore to a new path, and remap drives through §8.
  - Optimize (LP-0379, LP-0382, LP-0386): `VACUUM`, `REINDEX`, `ANALYZE`, orphan removal, relaunch-and-optimize.
  - Catalog lock (LP-0380): a lock file with process id and machine name; a second open refused by name.
  - Maintenance (LP-0385, LP-0387): per-folder records, remove thumbnails, remove all info for a folder, orphan folders, change binding, rebuild thumbnails and metadata for a selection.
  - Quarantine (LP-0388): files that fail to decode twice are listed, skipped by the indexer, and re-enabled from the list, controlled by `Lumen.Maintenance.Quarantine`.
  - Tests: `CatalogBackupTests` (backup, integrity, retention, restore to a new path equal row by row), `CatalogLockTests`, `OptimizeTests`, `QuarantineTests`; a corruption test flips a byte in a scratch catalog and asserts the integrity check refuses it by name.
  - Commit: `"lumen: scheduled catalog backups, restore, and maintenance"`
- **Proof:** unit plus fidelity: a backup of the fixture catalog restores to a catalog whose every table compares equal row by row; the corruption test fails the integrity check by name; a driven backup on exit completes with progress (log quoted); cheaper substitute that fails: copying the open file, which the WAL-mode test shows losing committed rows.

#### §10. Multiple catalogs, catalog settings, and preview management

- **Deliverable:** New, open, and recent catalogs with the name in the title bar; export a folder, collection, or selection as a catalog with negatives and previews; import from another Lumen catalog, a Lightroom Classic catalog, and a Photoshop Elements catalog read-only; ACDSee-style compressed and XML exports and a file listing; catalog settings; and preview building and discarding.
- **Depends On:** §9
- **Phase:** 33
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/catalog-exchange/ and docs/captures/lumen/catalog-settings/. Job: a photographer splits and merges catalogs between machines and moves from Lightroom or Elements without losing ratings, labels, keywords, and collections. Treatment: File, New Catalog, Open Catalog, Open Recent; File, Export as Catalog (negatives, previews, selected only); File, Import from Another Catalog with a changed-photos policy (preserve old settings as a virtual copy, replace non-raw only); File, Import from Lightroom Classic Catalog with a summary; Catalog Settings (location, previews, file handling); Library, Previews submenu. Cheaper substitute that fails: an importer that brings photos but not their metadata. Chrome: consume the catalog, `Microsoft.Data.Sqlite` (MIT) for reading `.lrcat` read-only, `D04 T01 §7`'s preview cache, and the history.
- **Runs:** `Requires: display-session -- the catalog dialogs need an interactive desktop`
- **Catalog:** LP-0389 to LP-0400 (12 features)
- **Source:** `-> SOURCE: parity-lumen-catalogs`
- **Hints:**
  - Multiple catalogs (LP-0393, LP-0398): recent list, name in the title bar, extends `D04 T01 §5`'s New and Open Catalog.
  - `CatalogExporter` in `Photon.Lumen.Core/CatalogExchange/` (LP-0391): subset copy with negatives (hash-verified), previews, and selected-only; ACDSee compressed export and XML text export of chosen fields (LP-0399).
  - `LumenCatalogImporter` (LP-0390): file handling (add, copy, move), changed existing photos policy, virtual copy for old settings, replace non-raw only.
  - `LightroomCatalogImporter` (LP-0397): opens `.lrcat` with `Mode=ReadOnly`, maps ratings, flags, labels, keywords with hierarchy, collections, and file locations, writes a summary; develop settings are read from each photo's `crs` XMP through `D01 T07 §6`; the `.lrcat` file hash is unchanged afterwards. Elements catalogs (LP-0389) use the same path over the Elements schema.
  - Catalog settings (LP-0394, LP-0396) and preview settings (LP-0395): standard preview size and quality, auto-discard 1:1 after a period; Build Standard, Build 1:1, and Discard 1:1 previews (LP-0392) extend `D04 T01 §7`.
  - File listing (LP-0400) as a tab-separated text table of chosen fields.
  - Tests: `CatalogExportImportTests` (export a subset, import into an empty catalog, compare), `LightroomCatalogImporterTests` over a committed small `.lrcat` fixture made with Lightroom Classic 15.5 (version recorded), `PreviewManagementTests`.
  - Commit: `"lumen: multiple catalogs, catalog exchange, and Lightroom catalog import"`
- **Proof:** fidelity plus unit: the Lightroom fixture imports with every rating, label, keyword path, and collection membership equal to the fixture's documented values, and the fixture's SHA-256 is unchanged; a round-trip Lumen export and import compares equal; cheaper substitute that fails: importing files only, which the metadata comparison catches.

#### §11. Smart previews and offline editing

- **Deliverable:** Smart previews (lossy DNG proxies at 2,560 px long edge) are built, discarded, counted, and included in catalog exports, and develop uses them when the original is offline, with an indicator under the histogram.
- **Depends On:** §10, D04 T13 §7
- **Phase:** 33
- **Surface:** UI. Fidelity: docs/captures/lumen/develop/ (baseline from `D04 T02 §3`), new captures to docs/captures/lumen/smart-previews/. Job: a photographer keeps developing on a laptop when the photo drive is at home, and the edits apply to the originals when it returns. Treatment: Library, Previews, Build and Discard Smart Previews; a status line under the histogram (Original, Smart Preview, Original and Smart Preview); a cache size readout in Catalog Settings. Cheaper substitute that fails: developing on the 2,048 px JPEG preview. Chrome: consume `D04 T13 §7`'s lossy DNG writing, `D04 T02 §2`'s pipeline, and the preview cache.
- **Runs:** `Requires: display-session -- the offline develop check needs an interactive desktop`
- **Catalog:** LP-0401, LP-0554 (2 features)
- **Source:** `-> SOURCE: parity-lumen-smart-previews`
- **Hints:**
  - `SmartPreviewStore` in `Photon.Lumen.Core/SmartPreviews/` (LP-0401): lossy DNG at 2,560 px in `<catalog>.smartpreviews/`, keyed by image id and file hash, size limit `Lumen.SmartPreviews.MaxMB`, status per photo, included in catalog export.
  - The develop source falls back to the smart preview when the original's volume is offline; settings stay in normalized coordinates (`D01 T07`), so edits apply unchanged to the original later.
  - The indicator (LP-0554) under the histogram and a filter column for smart-preview state in §4.
  - Export while offline renders from the smart preview at its size and says so in the export summary.
  - Tests: `SmartPreviewStoreTests`, `OfflineDevelopTests` (render from proxy versus original after the volume returns, crops and masks align within 1/255 after resize).
  - Commit: `"lumen: smart previews for offline develop"`
- **Proof:** unit plus fidelity: a proxy render and the original render of the same settings agree within 1/255 after resampling to the same size; a driven offline develop with the fixture drive disconnected is captured; cheaper substitute that fails: JPEG previews, which clip the highlights the comparison keeps.

#### §12. The dashboard and library statistics

- **Deliverable:** A Dashboard mode with overview, database, cameras, and files tabs and charts, extending `D04 T01 §10`'s library statistics.
- **Depends On:** §4
- **Phase:** 33
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/dashboard/. Job: a photographer sees what they shoot, with what, and how big and healthy the library is. Treatment: a Dashboard module with Overview (photos by year or month, database, camera, and file summaries), Database (size, path, files and folders, orphans, last backup, thumbnail cache), Cameras (most used body, lens, focal length, aperture, shutter, ISO charts with toggles), and Files (formats, bit depths, top 20 resolutions). Cheaper substitute that fails: a text dump of counts. Chrome: consume grouped catalog queries, the `Photon.UI` theme, and WPF drawing for charts (no charting package).
- **Runs:** `Requires: display-session -- the dashboard needs an interactive desktop`
- **Catalog:** LP-0402 to LP-0406 (5 features)
- **Source:** `-> SOURCE: parity-lumen-dashboard`
- **Hints:**
  - `LibraryStatistics` in `Photon.Lumen.Core/Library/Statistics/` extends `D04 T01 §10` (LP-0402) with grouped queries per tab, cached and invalidated by catalog change counters.
  - Overview (LP-0403), Database (LP-0404, reading §9's last backup), Cameras (LP-0405), Files (LP-0406).
  - Bar and line charts drawn by a small `StatChart` control in `Photon.Lumen.Desktop/Dashboard/` with theme brushes and keyboard focus on bars; clicking a bar filters the library through §4.
  - Tests: `LibraryStatisticsTests` on a seeded catalog with known counts.
  - Commit: `"lumen: the dashboard with catalog, camera, and file statistics"`
- **Proof:** unit plus driven: statistics tests match the seeded counts and the dashboard renders under 500 ms on 50,000 photos (quoted, captured); cheaper substitute that fails: counting by loading every record, which the timing catches.

#### §13. Painter and Quick Develop

- **Deliverable:** The Painter tool sprays keywords, labels, flags, ratings, metadata presets, develop presets, rotation, and target-collection membership with an erase mode, and the Quick Develop panel applies saved presets, crop ratio, treatment, white balance, and relative tone steps to a selection from the library.
- **Depends On:** §2
- **Phase:** 33
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/painter/ and docs/captures/lumen/quick-develop/. Job: a photographer applies one attribute to many scattered photos by painting over them, and nudges exposure on a whole selection without entering Develop. Treatment: the grid toolbar's spray can with a Paint menu and value field, drag to spray, Alt to erase; the Quick Develop panel in the right column with small and large relative steps and Reset All. Cheaper substitute that fails: absolute settings that overwrite each photo's values. Chrome: consume §2's culling commands, `D04 T01 §10` keywords, `D04 T02 §5` presets, `D04 T02 §1`'s edit stack, and `D01 T07 §1`'s tone stages.
- **Runs:** `Requires: display-session -- painting over the grid needs an interactive desktop`
- **Catalog:** LP-0287 to LP-0289 (3 features)
- **Source:** `-> SOURCE: parity-lumen-painter`
- **Hints:**
  - `PainterTool` in `Photon.Lumen.Desktop/Library/` (LP-0287, LP-0288): modes keywords, label, flag, rating, metadata preset (from `D04 T08 §3`, disabled with a tooltip until it ships), develop preset, rotation (metadata orientation), target collection; erase with Alt; one undo step per stroke.
  - `QuickDevelopService` in `Photon.Lumen.Core/Develop/` (LP-0289): relative deltas added to each photo's current `DevelopSettings` (exposure plus one third or one stop, and so on), saved preset, crop ratio, treatment, white balance preset, Reset All, one undo step across the selection.
  - Painter surface: the spray-can cursor and value field in the grid toolbar, the Paint menu, auto-dismiss after a stroke as a setting (`Lumen.Painter.AutoDismiss`), and one Serilog Information line per stroke naming the mode, the value, and the photo count; Quick Develop steps are keyboard operable and show the delta applied in the status strip.
  - Tests: `PainterToolTests` (each mode and erase), `QuickDevelopTests` (relative deltas keep per-photo differences).
  - Commit: `"lumen: the Painter and Quick Develop"`
- **Proof:** unit plus driven: the tests pass and a driven stroke over 30 photos adds a keyword to each as one undo entry (log quoted); cheaper substitute that fails: absolute Quick Develop values, which the per-photo difference test catches.

#### Sizing concerns

`§5` (18 features, nine criteria families) is the likeliest to pass 30 items; the natural split is the rule editor and criteria (kept) versus sets, target, and quick collections (a sibling section). `§8` (15 features) splits at the offline-volume model if needed. `§10`'s Lightroom importer is the riskiest item (undocumented schema); if it cannot hold, it moves to a sibling section rather than dropping Elements import.

### todo/04-lumen/TODO-07-lumen-parity-import.md -- `lumen-parity-import`

- **Title:** "TODO-07 -- Lumen Parity: Import, Devices, and Capture"
- **Phase(s):** 34
- **Goal:** Lumen's import reaches Lightroom Classic, ACDSee, and IrfanView parity on top of `D04 T01 §6`'s safe add and copy: a full import window with sources, a candidate grid, Move mode, new-only and duplicate filters; previews and smart previews built on import, a hash-verified second copy, renaming through the suite token engine, and destination organization; presets and everything applied during import; phones and cameras over Windows Portable Devices and AutoPlay; auto import from watched folders as the tether path (tethered capture proper stays B-048); Copy as DNG and Convert to DNG; scanning through WIA and TWAIN with IrfanView's batch scanning and Copy Shop; and a screen capture utility. The code lives in `src/Lumen/Photon.Lumen.Core/Import/`, `Devices/`, `Acquire/`, and `Capture/`, and `src/Lumen/Photon.Lumen.Desktop/Import/`; every path keeps the original-file guard (Move removes a source only after a hash-verified copy, into the Recycle Bin).
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code; import is planned in `D04 T01 §6` with a folder pattern and hash-verified copies. `<!-- claim: absent src/Lumen -->` `<!-- claim: count "yyyy/yyyy-MM-dd" todo/04-lumen/TODO-01-lumen-foundation.md = 1 -->`
  - The foundation file already names MetadataExtractor (Apache-2.0) for reading EXIF during import. `<!-- claim: count "MetadataExtractor" todo/04-lumen/TODO-01-lumen-foundation.md = 1 -->`
  - Imago's parity plan owns the WIA scanner and `Windows.Graphics.Capture` code this file moves to `Photon.Core`. `<!-- claim: count "Windows.Graphics.Capture" todo/03-imago/TODO-17-imago-parity-formats.md = 1 -->`
  - Tethered capture has no backlog entry yet; the integration adds B-048. `<!-- claim: count "B-048" todo/backlog.md = 0 -->`
- **Inputs and XREFs:** `standards/lumen.md` (the original-file guard; import copies are hash-verified), `standards/shared.md`; Windows Portable Devices API documentation (`IPortableDeviceManager`, `IPortableDeviceContent`, `WPD_OBJECT_ORIGINAL_FILE_NAME`), AutoPlay handler registration (`EventHandlers`, `ShowPicturesOnArrival`), WIA 2.0, TWAIN 2.5 specification; NTwain (MIT) over the scanner driver's installed TWAIN data source manager (never bundled); -> XREF: D04 T01 §6 (the import planner and runner every section extends); -> XREF: D04 T01 §7 (previews built on import); -> XREF: D04 T02 §8 (Lumen 0.1.0 ships first); -> XREF: D04 T06 §8 (Import to This Folder and previous-import entries); -> XREF: D04 T06 §11 (smart previews on import); -> XREF: D04 T08 §3 (metadata presets applied during import); -> XREF: D04 T08 §5 (keywords applied during import); -> XREF: D04 T11 §2 (the token engine for renaming on import); -> XREF: D04 T13 §7 (the DNG writer for Copy as DNG); -> XREF: D03 T17 §12 (WIA acquisition and screenshot capture moved to `Photon.Core` by §7 and §8); -> XREF: D04 T12 §4 (Copy Shop prints through the print engine when it ships).
- **Adjacency:** list=applicable @ D04 T07 §1 (candidate grid, device and source lists); document=applicable @ D04 T07 §7 (Copy Shop prints scans); settings=applicable (every import, device, scan, and capture option is a `Lumen.*` key; presets are settings); reporting=applicable (import, conversion, and batch-scan summaries); notifications=applicable (card detection, progress, cancel, completion, capture beep); permissions=applicable (read-only destinations, locked sources, devices refusing transfer, and missing TWAIN drivers refused by name); audit=applicable (one Serilog Information line per import run, conversion, scan, and capture); exchange=applicable (DNG, TIFF, PDF scans, captured PNG and JPEG); reverse=applicable (imports undo as a catalog removal; Move keeps sources in the Recycle Bin until verified; auto-import can be paused)

#### §1. The import window extended

- **Deliverable:** The import window gains a source panel of devices, card readers, drives, network folders, and discs with favorites and recents, Move mode, a checkable candidate grid with new-only and custom selections, filters and grouping, a loupe preview, drag-and-drop import, Import to This Folder, and a completion that opens the imported photos in a new tab.
- **Depends On:** D04 T02 §8, D04 T06 §8
- **Phase:** 34
- **Surface:** UI. Fidelity: docs/captures/lumen/import/ (baseline from `D04 T01 §6`), new captures to docs/captures/lumen/import-grid/. Job: a photographer picks exactly which photos come in from a card, sees them large enough to decide, and can move instead of copy without ever risking the card's files. Treatment: Lightroom's three-column import window (source, candidate grid with Copy as DNG, Copy, Move, Add across the top, destination and options on the right) with a compact mode; candidate filters All, New, Destination Folders; grouping by date or type; a loupe with E. Cheaper substitute that fails: import-everything-in-a-folder. Chrome: consume `D04 T01 §6`'s `ImportPlanner` and `ImportRunner` (extended), `D04 T01 §7`'s embedded-preview extraction, and the theme.
- **Runs:** `Requires: display-session -- the import window needs an interactive desktop`
- **Catalog:** LP-0407, LP-0432 to LP-0439 (9 features)
- **Source:** `-> SOURCE: parity-lumen-import-window`
- **Hints:**
  - `ImportSource` model in `Photon.Lumen.Core/Import/Sources/` (LP-0432): removable drives first, card readers, local and network folders, optical discs, include subfolders, favorites and recents in `Lumen.Import.Sources`; devices without drive letters appear once §4 ships.
  - Move mode (LP-0433): copy, verify SHA-256, record, then send the source to the Recycle Bin (never delete permanently); sources on read-only media fall back to Copy with a message.
  - Candidate grid (LP-0434): checkboxes, check all and none, new, all, or custom selection, view all or checked; filters and grouping by new-only, destination folder, date, file type, and sort order (LP-0435).
  - Preview (LP-0436): thumbnail size slider, loupe from the embedded preview, higher-quality embedded previews when available, compact dialog.
  - Drag files or folders onto Lumen (LP-0437) opens the window with them as the source; Import menu in the browser (LP-0438); Import to This Folder from the Folders panel (LP-0407) sets Add mode with the folder.
  - Completion opens the imported photos in a new browse tab (LP-0439), extending `D04 T01 §6`'s summary.
  - Tests: `ImportMoveTests` (verify then recycle; a hook that corrupts the copy leaves the source), `CandidateSelectionTests`, `ImportSourceTests`.
  - Commit: `"lumen: the full import window with sources, candidates, and Move"`
- **Proof:** unit plus driven: the Move test proves the source stays until verification and lands in the Recycle Bin; a driven import of a 200-photo card fixture with a custom selection imports exactly the checked set (captured); cheaper substitute that fails: moving with `File.Move` across volumes, which the corruption hook catches.

#### §2. File handling on import: previews, backup copies, renaming, and destination folders

- **Deliverable:** Import builds previews (minimal, embedded, standard, 1:1) and optional smart previews, writes a hash-verified second copy, renames through the suite token engine with sequence counters, organizes destinations by folder, date, or source structure, places RAW+JPEG pairs, and ejects the device afterwards.
- **Depends On:** §1, D04 T11 §2
- **Phase:** 34
- **Surface:** UI. Fidelity: docs/captures/lumen/import/, new captures to docs/captures/lumen/import-file-handling/. Job: a photographer lands photos named and filed the way they always file them, with a backup copy made in the same pass. Treatment: the right column's File Handling (Build Previews, Build Smart Previews, Don't Import Suspected Duplicates, Make a Second Copy To), File Renaming (template menu, custom text, shoot name, start number, extension case, sample), and Destination (Into Subfolder, Organize By Original Folders or By Date with date format, Into One Folder) panels; Eject after import. Cheaper substitute that fails: a fixed rename pattern. Chrome: consume `D04 T11 §2`'s token engine, `D04 T01 §7`'s preview builder, `D04 T06 §11`'s smart previews, and `AtomicFileWriter`.
- **Runs:** `Requires: display-session -- the file-handling panels need an interactive desktop`
- **Catalog:** LP-0408, LP-0440 to LP-0447 (9 features)
- **Source:** `-> SOURCE: parity-lumen-import-files`
- **Hints:**
  - Previews on import (LP-0441): minimal, embedded and sidecar, standard, 1:1, with replace-embedded-when-idle through the indexer queue; smart previews (LP-0442) through `D04 T06 §11`.
  - Second copy (LP-0443): a parallel stream to a backup folder, each file hash-verified like the primary; failures listed per file, never blocking the primary import.
  - Renaming (LP-0444, LP-0408): templates from `D04 T11 §2` with custom name, sequence, date, filename, shoot name, camera, start number, extension case, and a live sample; import sequence counters persisted in `Lumen.Import.Sequence`.
  - Destination (LP-0445, LP-0446): folder, named subfolder, by original folders, by capture or today's date nested or flat with a date format, one folder, ignore camera-generated folder names (`DCIM\100CANON`), show parent; extends `D04 T01 §6`'s `yyyy/yyyy-MM-dd` pattern.
  - RAW+JPEG placement (LP-0447): same folder or JPEG or RAW in a named subfolder, pairs kept linked for `D04 T13 §5`.
  - Eject (LP-0440) through `CM_Request_Device_Eject` after all handles close, with a message when Windows refuses.
  - Tests: `ImportRenameTests` (templates and collisions), `DestinationOrganizerTests` (every organization mode), `SecondCopyTests` (verified backup, corrupted-backup hook), `RawJpegPlacementTests`.
  - Commit: `"lumen: import file handling with previews, second copies, renaming, and destinations"`
- **Proof:** unit plus driven: the tests pass and a driven import with a template, date organization, and a second copy produces the expected tree in both locations with every hash matching the source (quoted); cheaper substitute that fails: an unverified second copy, which the corrupted-backup hook catches.

#### §3. Apply during import and import presets

- **Deliverable:** Import applies a develop preset, a metadata preset, keywords, categories, and custom fields, adds the photos to a collection, rotates from camera orientation as metadata, chooses the catalog date source, and saves everything as import presets.
- **Depends On:** §2, D04 T08 §3, D04 T08 §5
- **Phase:** 34
- **Surface:** UI. Fidelity: docs/captures/lumen/import/, new captures to docs/captures/lumen/import-presets/. Job: a photographer sets up a shoot once (copyright, keywords, a look, a collection) and every later card lands ready. Treatment: the Apply During Import panel (Develop Settings, Metadata with New inline, Keywords, Categories) and Add to Collection; an Import Preset menu at the bottom (save, update, rename, delete, none, recent). Cheaper substitute that fails: applying metadata in a second pass after import. Chrome: consume `D04 T02 §5`'s presets, `D04 T08 §3`'s metadata presets, `D04 T08 §5`'s keyword entry, `D04 T06 §6`'s categories, and `D04 T06 §5`'s collections.
- **Runs:** `Requires: display-session -- the import presets panel needs an interactive desktop`
- **Catalog:** LP-0448 to LP-0452, LP-0555 (6 features)
- **Source:** `-> SOURCE: parity-lumen-import-presets`
- **Hints:**
  - `ImportApplyOptions` in `Photon.Lumen.Core/Import/` (LP-0449, LP-0555): develop preset stored as the first edit-stack entry, metadata preset, keywords, categories, and custom fields written to the catalog and, when sidecars are on, the sidecar in the same transaction.
  - Add to collection (LP-0448), including a new collection created inline.
  - Automatic rotation (LP-0451) from the EXIF orientation into the catalog orientation; nothing written into the original.
  - Date source (LP-0452): EXIF date, file modified date, or a specific date for the catalog capture time.
  - `ImportPreset` store (LP-0450) in `Lumen.Import.Presets` holding source-independent options.
  - Tests: `ImportApplyTests` (each apply option on the fixture folder, sidecar content checked), `ImportPresetTests`.
  - Commit: `"lumen: apply during import and import presets"`
- **Proof:** unit plus driven: the tests pass and a driven import with a preset yields photos carrying the metadata, keywords, look, and collection with the unchanged-originals test over the import fixtures still green; cheaper substitute that fails: a post-import batch, which the single-transaction test catches.

#### §4. Phones and cameras over Windows Portable Devices

- **Deliverable:** Phones and cameras connected over MTP or PTP appear as import sources and as browsable folders without a drive letter, and inserting a card or device can show Lumen's import through AutoPlay.
- **Depends On:** §1
- **Phase:** 34
- **Surface:** UI. Fidelity: docs/captures/lumen/import/, new captures to docs/captures/lumen/devices/. Job: a photographer plugs in a phone or camera and imports from it like from a card. Treatment: devices listed first in the source panel with their icons; Windows AutoPlay offering "Import photos with Lumen" and "Browse with Lumen"; Preferences, Import, Show import dialog when a memory card is detected. Cheaper substitute that fails: asking the user to copy files off the phone first. Chrome: consume the Windows Portable Devices COM API (part of Windows), the import runner, and `D04 T05 §3`'s folder tree for browsing.
- **Runs:** `Requires: display-session -- a connected MTP device and AutoPlay need an interactive desktop`
- **Catalog:** LP-0453 to LP-0454 (2 features)
- **Source:** `-> SOURCE: parity-lumen-devices`
- **Hints:**
  - `WpdDeviceSource` in `Photon.Lumen.Core/Devices/` (LP-0454): enumerate devices, walk storage objects, stream files through `IPortableDeviceResources` into the import runner's verified copy; WIA cameras through the same source.
  - Device folders in the browse tree (LP-0454) as read-only virtual folders.
  - AutoPlay (LP-0453): handler registration for `ShowPicturesOnArrival` and `MixedContentOnArrival` in `installer/Lumen.iss` (per user), launching `Lumen.exe --import <device>`; the card-detected setting `Lumen.Import.ShowOnCard` watches `WM_DEVICECHANGE`.
  - Tests: `WpdDeviceSourceTests` over a fake `IPortableDevice` wrapper; a driven import from a real phone is the device proof.
  - Commit: `"lumen: import from phones and cameras over Windows Portable Devices"`
- **Proof:** unit plus driven: the fake-device tests pass and a driven import from an MTP phone (model quoted) completes with verified copies and captures; cheaper substitute that fails: requiring a drive letter, which the fake device without a path catches.

#### §5. Auto import from watched folders

- **Deliverable:** Lumen watches a folder, moves new files into a destination with naming, a develop preset, metadata, keywords, and initial previews as each lands: the tethered workflow through the camera maker's own utility (tethered capture proper is B-048).
- **Depends On:** §3
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/auto-import/. Job: a studio photographer shooting through the camera maker's tether utility sees each frame appear developed in Lumen seconds later. Treatment: File, Auto Import, Enable and Auto Import Settings (watched folder that must be empty, destination and subfolder, naming, develop, metadata, keywords, initial previews). Cheaper substitute that fails: a periodic folder rescan. Chrome: consume §2's handling, §3's apply options, `FileSystemWatcher`, and the import runner.
- **Runs:** `Requires: display-session -- the settings dialog and a live drop need an interactive desktop`
- **Catalog:** LP-0455 to LP-0456 (2 features)
- **Source:** `-> SOURCE: parity-lumen-auto-import`
- **Hints:**
  - `AutoImportService` in `Photon.Lumen.Core/Import/Auto/` (LP-0455, LP-0456): watch, wait until the file is closed and stable (size and exclusive-open probe), copy with verification into the destination, recycle from the watched folder after verification, apply options, build previews, select the newest photo in the grid.
  - Settings in `Lumen.Import.Auto.*`; the watched folder must be empty when enabled (refused by name otherwise).
  - A note in the dialog and the user guide names B-048 and the vendor utilities as the tether path.
  - Tests: `AutoImportTests` (a writer thread slowly writing a file; the file imports once, after close).
  - Commit: `"lumen: auto import from a watched folder"`
- **Proof:** unit plus driven: the test proves no partial file is imported; a driven drop of 20 files lands them developed with the latency quoted; cheaper substitute that fails: importing on the created event, which the slow-writer test catches.

#### §6. Convert to DNG

- **Deliverable:** Copy as DNG on import and Convert Photo to DNG in the library write DNG files with Lightroom's conversion options, replacing the catalog reference and handling the original per the guard.
- **Depends On:** §1, D04 T13 §7
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/dng-convert/. Job: a photographer standardizes on DNG without losing any metadata or risking the raw file. Treatment: Copy as DNG at the top of the import window; Library, Convert Photos to DNG dialog (only raw files, delete originals after successful conversion as move to Recycle Bin, extension case, JPEG preview size, embed fast load data, lossy compression, embed original raw, compatibility). Cheaper substitute that fails: renaming the raw file. Chrome: consume `D04 T13 §7`'s writer, the import runner, and the catalog.
- **Runs:** `Requires: display-session -- the conversion dialog needs an interactive desktop`
- **Catalog:** LP-0409, LP-0457 to LP-0458 (3 features)
- **Source:** `-> SOURCE: parity-lumen-dng-convert`
- **Hints:**
  - `DngConversionService` in `Photon.Lumen.Core/Import/Dng/` (LP-0409, LP-0458): options passed to `D04 T13 §7`; the new DNG is validated (Adobe `dng_validate` as the oracle where installed) before the catalog record is switched; the original goes to the Recycle Bin only when the user ticked it and validation passed.
  - Copy as DNG import mode (LP-0457) writes DNGs into the destination and never copies the raw unless Embed Original Raw is on.
  - Metadata and develop settings carried into the DNG's XMP.
  - Tests: `DngConversionTests` (options reach the writer, catalog switch after validation, original kept on validation failure).
  - Commit: `"lumen: Copy as DNG and Convert to DNG"`
- **Proof:** fidelity plus unit: converting the committed raw fixtures yields DNGs that decode through `D04 T01 §4` within the stated tolerance of the original decode, and the originals' hashes are unchanged when not recycled; cheaper substitute that fails: switching the catalog before validation, which the failure test catches.

#### §7. Scanning and Copy Shop

- **Deliverable:** Scanning through WIA and TWAIN with source selection, single and batch scans with a file-name pattern and counter, multi-page TIFF or PDF output, a destination folder, and IrfanView's Copy Shop (scan and print copies).
- **Depends On:** §1
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/scan/. Job: a user digitizes prints and documents straight into the library, many pages in one go, or makes copies with a scanner and printer. Treatment: File, Acquire (Select Source, Acquire, Batch Scanning dialog with pattern, counter start, step, digits, skip existing, remember counter, destination, format, multi-page, keep scanner UI open); File, Copy Shop (scanner, preview, DPI, printer, copies). Cheaper substitute that fails: WIA only, which drops IrfanView's TWAIN batch workflow. Chrome: consume WIA acquisition moved from `D03 T17 §12` to `Photon.Core/Acquire/`, NTwain (MIT) over the driver's TWAIN data source manager, `D04 T11 §2` tokens, and the print dialog frame.
- **Runs:** `Requires: display-session -- a scanner driver UI needs an interactive desktop`
- **Catalog:** LP-0459 to LP-0464 (6 features)
- **Source:** `-> SOURCE: parity-lumen-scanning`
- **Hints:**
  - First item: move the WIA acquisition code of `D03 T17 §12` from `Photon.Imago.Desktop` to `Photon.Core/Acquire/Wia/` on this second consumer and repoint Imago (never a copy).
  - `TwainSource` in `Photon.Lumen.Core/Acquire/Twain/` over NTwain (MIT, license row in `docs/dev/decisions.md`), the TWAIN DSM that the scanner driver installs (not bundled); 32-bit-only drivers are listed as unavailable with the reason (LP-0460).
  - Destination folder (LP-0459, LP-0461) as a setting, scans added to the catalog in place.
  - Batch scanning (LP-0462, LP-0463): name pattern through `D04 T11 §2`, counter, step, digits, skip existing, remember counter, format, multi-page TIFF or PDF through `D04 T13 §6` writers, scanner UI kept open.
  - Copy Shop (LP-0464): scan, preview, DPI, printer, copies; printing through the `Photon.UI/Print/` frame (the full print module arrives with `D04 T12 §4`).
  - Tests: `BatchScanNamingTests`, `TwainSourceTests` over the TWAIN virtual scanner sample data source where installed (skipped with a reason otherwise), `WiaMoveTests` (Imago still acquires through the moved code).
  - Commit: `"lumen: scanning through WIA and TWAIN, batch scanning, and Copy Shop"`
- **Proof:** unit plus driven: naming tests pass and a driven batch scan of three pages from the TWAIN sample source writes a three-page TIFF into the catalog (captured); cheaper substitute that fails: a copied WIA class in Lumen, which a grep for a second `WiaAcquirer` catches.

#### §8. Screen capture

- **Deliverable:** A capture utility with desktop, monitor, window, client area, region, fixed rectangle, and auto-scroll sources, hotkey and timer triggers with countdown, cursor inclusion and highlight, and output to the viewer, clipboard, printer, or a named file, optionally resident in the notification area.
- **Depends On:** §1
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/capture/. Job: a user grabs a window or region into a file or the library with one hotkey. Treatment: File, Capture/Screenshot dialog (IrfanView and ACDSee options), a notification-area icon while resident with Exit, and a region picker overlay. Cheaper substitute that fails: Print Screen to the clipboard only. Chrome: consume `Windows.Graphics.Capture` code moved from `D03 T17 §12` to `Photon.Core/Capture/`, `D04 T11 §2` tokens, and the atomic writer.
- **Runs:** `Requires: display-session -- screen capture needs an interactive desktop`
- **Catalog:** LP-0465 to LP-0470 (6 features)
- **Source:** `-> SOURCE: parity-lumen-capture`
- **Hints:**
  - First item: move the screenshot code of `D03 T17 §12` to `Photon.Core/Capture/` on this second consumer and repoint Imago.
  - Sources (LP-0466, LP-0468, LP-0470): desktop, monitor, window, client area, region, child window, menu under the cursor, fixed rectangle, auto-scroll object capture (scroll messages plus stitching of overlapping strips).
  - Triggers and output (LP-0467, LP-0469): hotkey via `RegisterHotKey`, timer with count and countdown, cursor and highlight, to viewer, clipboard, printer, or a file named through `D04 T11 §2` with a beep on save.
  - Resident utility (LP-0465): notification-area icon, include cursor, exit.
  - Tests: `CaptureNamingTests`, `ScrollStitcherTests` (synthetic overlapping strips), `HotkeyRegistrationTests` (conflict reported by name).
  - Commit: `"lumen: screen capture with hotkeys, timers, and auto scroll"`
- **Proof:** unit plus driven: the stitcher test reconstructs a synthetic page exactly; a driven region capture by hotkey saves a named PNG added to the catalog (captured); cheaper substitute that fails: `CopyFromScreen` of the whole desktop only, which the window and region captures refuse.

#### Sizing concerns

`§1` and `§2` are the densest; if `§2` exceeds 30 items, the second copy and eject split into a sibling section. `§7`'s TWAIN path depends on a data source manager on the test machine; the section keeps the WIA path proven on every clone and marks TWAIN tests skipped with a reason, never failed.

### todo/04-lumen/TODO-08-lumen-parity-metadata.md -- `lumen-parity-metadata`

- **Title:** "TODO-08 -- Lumen Parity: Metadata, Keywords, and Places"
- **Phase(s):** 34
- **Goal:** Lumen reads, shows, edits, and writes every metadata field Lightroom Classic, ACDSee, and IrfanView handle (EXIF, IPTC Core and Extension, XMP, MWG mappings, comments, and descript.ion captions) with status and conflict tracking; edits land in the catalog and in XMP sidecars, and embedding into files happens only in exported and converted copies, never in an original; the metadata panel and properties pane with every field set and custom views; metadata presets and sync; capture-time editing and batch time stamps; the full keyword toolset; and a map view with offline basemap, geotagging, saved and private locations, GPX track logs, and offline reverse geocoding (promoting B-034). The code lives in `src/Lumen/Photon.Lumen.Core/Metadata/`, `Keywords/`, and `Places/`, and `src/Lumen/Photon.Lumen.Desktop/Metadata/` and `Map/`.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code; sidecars are planned in `D04 T01 §11` behind a setting that defaults off. `<!-- claim: absent src/Lumen -->` `<!-- claim: count "Lumen.Metadata.WriteSidecars" todo/04-lumen/TODO-01-lumen-foundation.md = 1 -->`
  - Map and GPS wait in the backlog as B-034. `<!-- claim: count "^- \[B-034\]" todo/backlog.md = 1 -->`
  - `standards/lumen.md` limits metadata writes to the catalog and sidecars. `<!-- claim: count "Never into the original's own bytes" standards/lumen.md = 1 -->`
  - Imago's parity plan owns the EXIF, IPTC, and XMP code this file consumes. `<!-- claim: count "## 10. Metadata: EXIF, IPTC, XMP, and File Info" todo/03-imago/TODO-17-imago-parity-formats.md = 1 -->`
- **Inputs and XREFs:** `standards/lumen.md`; IPTC Photo Metadata Standard 2024.1 (Core and Extension); Metadata Working Group Guidelines 2.0 (reconciliation of EXIF, IPTC-IIM, and XMP, face and region schema); EXIF 3.0 (CIPA DC-008); Adobe XMP Specification Part 1 to 3; GPX 1.1 schema; GeoNames `cities1000` and admin-code dumps (CC BY 4.0, attribution in About); Natural Earth 1:50m vectors (public domain); OpenStreetMap Foundation Tile Usage Policy; exiftool 13 as the reading oracle for fidelity tests; -> XREF: D04 T01 §11 (the XMP sidecar writer §8 extends); -> XREF: D04 T01 §10 (the keyword hierarchy §5 extends); -> XREF: D04 T01 §6 (metadata read on import, which §1 widens); -> XREF: D04 T02 §6 (export metadata choices and remove location that §7's private locations extend); -> XREF: D04 T02 §8 (Lumen 0.1.0 ships first); -> XREF: D04 T05 §2 (the indexer reads metadata through §1); -> XREF: D03 T17 §10 (EXIF, IPTC, XMP, and File Info code, moved to `Photon.Core/Metadata/` by §1 on its second consumer); -> XREF: D01 T07 §6 (the XMP packet core §8 writes through); -> XREF: D04 T11 §2 (placeholders in metadata fields and presets); -> XREF: D04 T06 §4 (location and IPTC filter columns fed by §1); -> XREF: D04 T07 §3 (metadata presets and keywords applied during import); -> XREF: D04 T10 §3 (MWG face regions written through §8); -> XREF: D04 T10 §4 (AI keywords land in §5's list); -> XREF: D04 T12 §13 (export embeds metadata into copies through §8).
- **Adjacency:** list=applicable @ D04 T08 §5 (keyword list, sets, and the map's pin list); document=not-applicable (metadata prints through D04 T12 captions); settings=applicable (field sets, views, autocomplete, sidecar policy, tile source, and geocoding options are `Lumen.*` keys); reporting=applicable (metadata status, embed-pending counts, and track-log match reports); notifications=applicable (embed and geotag runs show progress and a summary); permissions=applicable (read-only media and read-only sidecars refused by name); audit=applicable (one Serilog Information line per metadata-changing command); exchange=applicable (XMP sidecars, keyword list text, metadata preset files, descript.ion, GPX); reverse=applicable (every metadata edit, geotag, and time shift undoes through the suite history, and time edits keep the original value to revert)

#### §1. The metadata model: every EXIF, IPTC, and XMP field read and tracked

- **Deliverable:** One metadata model in the catalog holds every EXIF, IPTC Core and Extension, XMP, MWG-reconciled, and Lumen field read from every supported format, with metadata status (up to date, changed on disk, conflict) and a resolution badge, IPTC keyword and supplemental-category import, and hierarchy-separator handling.
- **Depends On:** D04 T02 §8, D04 T05 §2
- **Phase:** 34
- **Surface:** no surface of its own beyond the status badge on grid cells (a small addition to `D04 T01 §8`'s badges); the panels are §2.
- **Runs:** none
- **Catalog:** LP-0410 to LP-0411, LP-0477 to LP-0484 (10 features)
- **Source:** `-> SOURCE: parity-lumen-metadata-model`
- **Hints:**
  - First item: move the EXIF, IPTC, and XMP reading code of `D03 T17 §10` from `Photon.Imago.FileFormats` to `Photon.Core/Metadata/` on this second consumer and repoint Imago; MetadataExtractor (Apache-2.0) stays the container parser.
  - `MetadataRecord` in `Photon.Lumen.Core/Metadata/` with typed EXIF, IPTC Core and Extension (contact, content, image, status, copyright, persons, locations, artwork, models, releases, licensor, digital source type) (LP-0479), XMP, and Lumen fields (caption, notes, author, database date) (LP-0481), stored in catalog tables with an FTS projection for `D04 T06 §7`.
  - Readers for every source (LP-0483, LP-0484): EXIF in JPEG, TIFF, RAW, HEIC, CR3, WebP, PNG; IPTC-IIM in JPEG, TIFF, and RAW; XMP embedded and in sidecars; comments.
  - `MwgReconciler` (LP-0480) applying MWG 2.0 precedence between EXIF, IPTC, and XMP for description, creator, copyright, and date created, with the raw per-source values available for display.
  - Import metadata while cataloging (LP-0411, LP-0482): EXIF and IPTC, IPTC keywords and supplemental categories into Lumen keywords and categories, embedded catalog metadata, database date from EXIF; keyword hierarchy separators (`|`, `/`, `>`) configurable (LP-0477).
  - `MetadataStatus` (LP-0478): per photo, the file's and sidecar's last-write time and XMP digest against the catalog's; changed on disk, conflict, and a badge with Read from File or Overwrite Settings.
  - Relocation (LP-0410): metadata stays in the catalog and sidecars so a moved file is rebound by `D04 T06 §8`; per-format embedding is only for exported copies (§8).
  - Tests: `MetadataReaderFidelityTests` (`[Trait("Category", "Fidelity")]`: every field of a committed fixture set compared with exiftool 13 output, version recorded), `MwgReconcilerTests`, `MetadataStatusTests` (sidecar edited by another tool flags conflict).
  - Commit: `"lumen: one metadata model for EXIF, IPTC, XMP, and MWG with status tracking"`
- **Proof:** format fidelity: every field of the fixtures (JPEG, TIFF, DNG, CR3, HEIC, WebP, PNG) equals exiftool's reading; the conflict test flags an externally edited sidecar; cheaper substitute that fails: reading EXIF only, which the IPTC Extension fixture catches.

#### §8. Writing metadata: sidecars, pending writes, and exported copies

- **Deliverable:** Save Metadata to File writes XMP sidecars for every format (and for a whole folder), Read Metadata from File reloads them, embed-pending tracks unwritten catalog metadata with an overlay, special item, and reminder, IPTC keywords and categories are written with merge or overwrite, descript.ion captions import and export, catalog records rebuild from sidecars, and privacy removal and in-file embedding apply only to exported and converted copies.
- **Depends On:** §1
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/embed-pending/. Job: a photographer knows their metadata is safe outside the catalog and readable by other tools, without Lumen ever rewriting a photo. Treatment: Metadata, Save Metadata to File (Ctrl+S) and Read Metadata from File; an embed-pending overlay icon and a special item; Tools, Embed Metadata dialog (all or selected, options, reminder, on shutdown, network drives, summary) whose wording says "sidecar" and states the guard; Export's metadata page for embedding into copies. Cheaper substitute that fails: writing XMP into originals, which the frozen guard forbids. Chrome: consume `D04 T01 §11`'s `XmpSidecar` (extended), `D01 T07 §6`'s XMP packet core, `AtomicFileWriter`, and the history.
- **Runs:** `Requires: display-session -- the embed dialog and pending overlay need an interactive desktop`
- **Catalog:** LP-0416 to LP-0418, LP-0526 to LP-0534, LP-0975 (13 features)
- **Source:** `-> SOURCE: parity-lumen-metadata-write`
- **Hints:**
  - `MetadataWriter` in `Photon.Lumen.Core/Metadata/Write/` (LP-0526, LP-0416): sidecar for every format including JPEG, TIFF, and DNG (where Lightroom writes in place), atomic, merging unknown fields byte-for-byte; a whole-folder save; Read from File reloads.
  - Sidecar details (LP-0417): large develop data split into `lumen:develop` blocks, fast writes of changed properties only, the conflict badge from §1.
  - Embed pending (LP-0528, LP-0529): a `pending` flag set by every metadata command, the overlay and special item, Embed Metadata for all or selected, clear pending, reminder and on-shutdown options, network drives, a summary; everything written to sidecars, and the dialog names the guard.
  - IPTC keywords and categories (LP-0532) written as `dc:subject` and `photoshop:SupplementalCategories` in the sidecar with merge or overwrite.
  - DNG preview and metadata update (LP-0527) refreshes Lumen's preview cache and sidecar, never the DNG.
  - Create EXIF data for JPEGs without it (LP-0534) as `exif:` properties in the sidecar.
  - Rebuild catalog records from embedded metadata and sidecars (LP-0530).
  - descript.ion (LP-0418, LP-0975): read as captions; export writes the folder's `descript.ion` text file atomically (a text file beside the photos, not an image write).
  - Read-only media (LP-0531) refused by name with the pending flag kept.
  - `ExportMetadataEmbedder` (LP-0533): embedding into exported and converted copies and privacy removal (EXIF, IPTC, Lumen fields, GPS) used by `D04 T12 §13` and `D04 T11 §4`, never an original.
  - Tests: `SidecarWriteFidelityTests` (`[Trait("Category", "Fidelity")]`: sidecars for each fixture format read back by exiftool 13 and by darktable 5.0 and Lightroom-style readers with every written field equal), `UnknownFieldPreservationTests`, `EmbedPendingTests`, `ExportEmbedTests`, and the unchanged-originals test over every fixture after save, embed, and rebuild.
  - Commit: `"lumen: sidecar metadata writing, embed pending, and embedding into exported copies"`
- **Proof:** format fidelity plus unit: every sidecar round-trips through exiftool with written fields equal and unknown fields byte-identical; every original's SHA-256 and last-write time is unchanged after Save Metadata, Embed Metadata, and Rebuild; cheaper substitute that fails: in-place XMP writing, which the unchanged-originals test catches.

#### §2. The metadata panel and properties pane

- **Deliverable:** A metadata panel with every Lightroom field set and a customizable default, file, basic, and EXIF fields, editing across a selection with mixed values, autocomplete, placeholders, jump arrows, and target-photo display; an ACDSee properties pane with metadata views, custom views, Organize and File tabs; and IrfanView's EXIF, IPTC, and comment dialogs, all writing through §8.
- **Depends On:** §1
- **Phase:** 34
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/ (the metadata panel area from `D04 T01 §2`), new captures to docs/captures/lumen/metadata-panel/ and docs/captures/lumen/properties-pane/. Job: a photographer reads and edits any field for one photo or hundreds at once, in the layout they already know. Treatment: Lightroom's Metadata panel with a field-set menu; ACDSee's Properties pane with Metadata, Organize, and File tabs and a view picker; the viewer's Information dialog with EXIF, IPTC, and Comment buttons. Cheaper substitute that fails: a read-only EXIF list. Chrome: consume §1's model, §8's writer, `D04 T11 §2` tokens, `Photon.UI` controls, and the history.
- **Runs:** `Requires: display-session -- the panels and dialogs need an interactive desktop`
- **Catalog:** LP-0412, LP-0485 to LP-0503 (20 features)
- **Source:** `-> SOURCE: parity-lumen-metadata-panel`
- **Hints:**
  - `MetadataFieldSet` definitions in `Photon.Lumen.Core/Metadata/Views/` (LP-0485): default, EXIF, EXIF and IPTC, IPTC, IPTC Extension, large caption, location, minimal, quick describe, and a customizable default; custom views built by picking fields in a tree with maker notes and row hiding (LP-0495, LP-0493).
  - Fields: file with rename (through `D04 T05 §6`) and folder link (LP-0486), basic (title, caption, alt text, extended description, rating, label, capture time with milliseconds, original and cropped dimensions) (LP-0487), EXIF (LP-0488).
  - Multi-selection editing (LP-0489): mixed values shown as such, apply to all, keep field while moving next, Enter applies, Esc discards, Tab navigation; show target photo only (LP-0491); jump arrows filter the grid (LP-0490).
  - Autocomplete (LP-0412) from used values with clear; placeholders, sequence numbers, and append mode (LP-0498) through `D04 T11 §2`.
  - Properties pane (LP-0492, LP-0493, LP-0494, LP-0496, LP-0497): browse-mode pane with views, adjustable field width, Organize tab, and File tab (read-only and hidden attributes are file attributes, image bytes untouched).
  - Captions while viewing (LP-0499) in the viewer's info strip.
  - IrfanView dialogs (LP-0500 to LP-0503): modeless EXIF information that follows browsing with copy lines and tag choice, IPTC editing for the current photo and selected thumbnails, Unicode comments; every save goes through §8 into sidecars.
  - Tests: `MetadataFieldSetTests`, `MultiEditTests` (mixed values and apply-to-all with undo), `PlaceholderFieldTests`, `IptcDialogViewModelTests`.
  - Commit: `"lumen: the metadata panel, properties pane, and metadata dialogs"`
- **Proof:** unit plus driven: the tests pass and a driven edit of the caption on 100 selected photos is one undo step and one sidecar write per photo (log quoted), with the unchanged-originals test green; cheaper substitute that fails: single-photo editing, which the multi-edit test catches.

#### §3. Metadata presets and synchronizing metadata

- **Deliverable:** Metadata presets covering every field group with placeholders, an existing-value token, a shortcut preset, and import and export; Sync Metadata, auto sync, copy and paste metadata with chosen fields; and IrfanView's apply IPTC and comment from the first image to a selection.
- **Depends On:** §2
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/metadata-presets/. Job: a photographer stamps copyright and contact on every photo in one action and copies a caption across a set. Treatment: the metadata panel's Preset menu with Edit Presets (field groups with checkboxes), Metadata, Sync Metadata with a field checklist, Copy and Paste Metadata, and an auto-sync toggle. Cheaper substitute that fails: presets that overwrite untouched fields. Chrome: consume §2's field sets, §8's writer, `D04 T11 §2` tokens, and the history.
- **Runs:** `Requires: display-session -- the preset editor needs an interactive desktop`
- **Catalog:** LP-0504 to LP-0506 (3 features)
- **Source:** `-> SOURCE: parity-lumen-metadata-presets`
- **Hints:**
  - `MetadataPreset` in `Photon.Lumen.Core/Metadata/Presets/` (LP-0504): checked field groups only, an existing-value token that keeps a field, placeholders, a shortcut preset, import and export as Lightroom `.lrtemplate`-compatible metadata presets where fields map and Lumen JSON otherwise.
  - Sync, auto sync, copy and paste (LP-0505) with a field checklist, one undo step per batch.
  - Apply IPTC and comment from the first image (LP-0506) writes sidecars through §8.
  - Tests: `MetadataPresetTests` (unchecked fields untouched), `MetadataSyncTests`, `MetadataPresetExchangeTests` (a Lightroom metadata preset fixture read).
  - Commit: `"lumen: metadata presets and metadata sync"`
- **Proof:** unit plus fidelity: the preset fixture reads with every mapped field equal and unchecked fields stay untouched; cheaper substitute that fails: whole-record overwrite, which the untouched-field test catches.

#### §4. Capture time editing

- **Deliverable:** Edit Capture Time (a specified date, a time-zone shift, the file's creation date, revert to original) and ACDSee's Batch Adjust Time Stamp over EXIF original, digitized, and modified dates, file-system dates, and the catalog date, written to the catalog and sidecars (file-system dates as file attributes), never into a raw or JPEG file.
- **Depends On:** §2, §8
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/capture-time/. Job: a photographer fixes a camera clock set to the wrong zone for a whole trip and undoes it if wrong. Treatment: Metadata, Edit Capture Time dialog with the three modes and a before and after preview; Tools, Batch Adjust Time Stamp wizard (which stamps, use another stamp, a specific date, shift to a new start, shift by an offset); IrfanView's Change EXIF Date as the same dialog. Cheaper substitute that fails: editing the catalog date only. Chrome: consume §1's model, §8's writer, and the history.
- **Runs:** `Requires: display-session -- the dialog and wizard need an interactive desktop`
- **Catalog:** LP-0413, LP-0507 to LP-0511 (6 features)
- **Source:** `-> SOURCE: parity-lumen-capture-time`
- **Hints:**
  - `CaptureTimeEditor` in `Photon.Lumen.Core/Metadata/Time/` (LP-0507): specified date, shift by hours and minutes for zones, file creation date, revert to the stored original value (`lumen:originalDateTime`).
  - Batch Adjust Time Stamp (LP-0509): EXIF original, digitized, modified, file created and modified, catalog date; sources and shift modes; file-system dates set with `File.SetCreationTime` and `SetLastWriteTime` (attributes, not image bytes), which the unchanged-originals test measures by content hash only for this command and says so.
  - Write date changes into raw files (LP-0413, LP-0508) and EXIF date edits (LP-0510, LP-0511): sidecar `exif:DateTimeOriginal` and `xmp:CreateDate`, never the raw or JPEG.
  - Tests: `CaptureTimeEditorTests` (zone shift over a DST boundary, revert), `BatchTimeStampTests`, and a content-hash unchanged test over the fixtures.
  - Commit: `"lumen: capture time editing and batch time stamps"`
- **Proof:** unit plus fidelity: shifted dates read back from sidecars by exiftool equal the expected values and every original's content hash is unchanged; cheaper substitute that fails: writing EXIF in place, which the content-hash test catches.

#### §5. Keyword extensions

- **Deliverable:** Keyword entry with separators, autocomplete, and hierarchy syntax; keyword shortcut and toggle; suggestions; keyword sets and quick-keyword grids; a keyword list with counts, filters, partial checks, and bulk assignment; keywords created with synonyms, parents, and export flags; tree editing with merge; purge; keyword list import and export; IPTC keyword pickers and separator conflict handling.
- **Depends On:** §2
- **Phase:** 34
- **Surface:** UI. Fidelity: docs/captures/lumen/keywords/ (baseline from `D04 T01 §10`), new captures to docs/captures/lumen/keyword-sets/. Job: a photographer tags fast with sets and suggestions, keeps a clean hierarchy, and brings their Lightroom keyword list along. Treatment: the Keywording panel (entry modes: keyword tags, containing keywords, will export; suggestions; keyword set grid) and the Keyword List panel (filter, counts, checkboxes, arrows, context menu with edit, merge by rename, delete, copy and paste); ACDSee's Keywords group in the Organize pane with quick-keyword grids up to 250. Cheaper substitute that fails: a flat keyword text box. Chrome: consume `D04 T01 §10`'s hierarchy (extended), §8 for `lr:hierarchicalSubject` and `dc:subject`, and the history.
- **Runs:** `Requires: display-session -- keyword panels need an interactive desktop`
- **Catalog:** LP-0414, LP-0512 to LP-0525 (15 features)
- **Source:** `-> SOURCE: parity-lumen-keywords`
- **Hints:**
  - Entry (LP-0512, LP-0525): comma or space separators, autocomplete, `Child < Parent` hierarchy syntax.
  - Keyword shortcut and toggle (LP-0513) with Shift+K; suggestions from nearby-in-time and similar photos (LP-0517), similarity through capture proximity now and `D04 T10 §5` later.
  - Keyword sets and quick grids (LP-0518): built-in and custom sets, Alt+number, rows and columns up to 250, assignment state, stored as presets.
  - Keyword list (LP-0519, LP-0522, LP-0523): counts, text and people filters, partial checkboxes, multi-select bars, select all, clear, assign, unassign, unassign all, count arrows, browse by keyword, Organize pane group.
  - Create keyword (LP-0520) with synonyms, parent, default parent, apply on creation, and export flags (include on export, export containing keywords, export synonyms), read by `D04 T12 §13`.
  - Tree editing (LP-0521): drag to reorganize, merge by rename, delete, edit, copy and paste; purge unused keywords and unused IPTC keywords (LP-0514).
  - Keyword list exchange (LP-0515): tab-indented text with `[synonym]` and `{brackets}` excluded markers, Lightroom's format read and written.
  - Entry modes (LP-0516) extend `D04 T01 §10`; IPTC keyword picker with a stored value list (LP-0524); separator conflict dialogs for keywords and categories containing the separator (LP-0414).
  - Tests: `KeywordEntryTests`, `KeywordListExchangeTests` (a Lightroom keyword export fixture round-trips byte-equal), `KeywordMergeTests`, `KeywordSetTests`.
  - Commit: `"lumen: keyword sets, suggestions, synonyms, and keyword list exchange"`
- **Proof:** unit plus fidelity: the Lightroom keyword fixture imports and exports byte-equal and a merge by rename moves every photo's keyword with one undo step; cheaper substitute that fails: flat keywords, which the hierarchy round-trip catches.

#### §6. The map view and places

- **Deliverable:** A Map module on Lumen's own slippy-map control with markers, clusters, a navigator, map styles from configurable tile sources, an offline Natural Earth basemap, place search from an offline gazetteer, geotagging by drag, saved locations with radius, overlays and locks, a location filter, the metadata panel, a map pane in browse, and hand-offs to external maps.
- **Depends On:** §1
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/map/. Job: a travel photographer sees where every photo was taken and places the ones without GPS by dragging them, with or without a network. Treatment: a Map module (Lightroom layout: map center, filmstrip below, Saved Locations and Metadata panels, a filter bar with Visible on Map, Tagged, Untagged), a style menu, a place-search box, and ACDSee's Map pane in browse. Cheaper substitute that fails: an embedded web map, which needs a browser engine and a network. Chrome: consume own `MapControl` on SkiaSharp (Web Mercator XYZ tiles), an HTTP tile fetcher with an identifying User-Agent and disk cache, §8 for GPS writes to sidecars, and the history.
- **Runs:** `Requires: display-session -- the map needs an interactive desktop`
- **Catalog:** LP-0537 to LP-0550 (14 features)
- **Source:** `-> SOURCE: lumen-roadmap-map` (promotes B-034)
- **Hints:**
  - `MapControl` in `Photon.Lumen.Desktop/Map/` (LP-0537, LP-0538): pan, zoom, markers, clusters with a preview, select by pin, navigator overview, pin legend; tiles from `TileSource` definitions in `Lumen.Map.TileSources`.
  - Tile sources (LP-0539): the default OpenStreetMap standard layer under the OSMF Tile Usage Policy (identifying User-Agent `Lumen/<version>`, visible attribution, HTTP cache honoring `max-age`, no bulk prefetch), user-added XYZ sources with their own attribution for satellite, terrain, hybrid, light, and dark styles, and an "offline only" switch; license row in `docs/dev/decisions.md` (OSM data ODbL).
  - Offline basemap: Natural Earth 1:50m land, borders, and places (public domain) bundled and rendered locally when tiles are off or unreachable.
  - Place search (LP-0540) over the bundled GeoNames gazetteer (CC BY 4.0) shared with §7.
  - Geotagging (LP-0543, LP-0544): drag photos onto the map, refresh pins, delete GPS, remove from map, view on map; GPS written to the catalog and sidecars through §8, kept independent of develop reset (LP-0548).
  - Saved locations with radius (LP-0545), overlays and locks (LP-0541), the location filter bar (LP-0542), the metadata panel in the map (LP-0546), and supported formats and default location (LP-0548).
  - Browse map pane (LP-0547) and external hand-offs (LP-0549, LP-0550): open the GPS position in the user's browser or app with a user-chosen URL template.
  - Tests: `WebMercatorTests`, `ClusterTests`, `TileCacheTests` (User-Agent and cache headers asserted on a local test server), `GeotagTests` (sidecar GPS read back by exiftool).
  - Commit: `"lumen: the map view with offline basemap, geotagging, and saved locations"`
- **Proof:** unit plus driven: the tests pass; a driven session with the network disabled shows the Natural Earth basemap and geotags five photos by drag (captures), and their sidecars read back the coordinates in exiftool; cheaper substitute that fails: an online-only map, which the offline session refuses.

#### §7. Track logs, geotagging, and offline reverse geocoding

- **Deliverable:** GPX track logs auto-tag photos by capture time with a time-zone offset and track navigation, reverse geocoding fills city, state, country, and country code offline as suggestions, suggested locations export, and private saved locations strip GPS from exports.
- **Depends On:** §4, §6
- **Phase:** 34
- **Surface:** UI. Fidelity: new captures to docs/captures/lumen/tracklogs/. Job: a photographer whose camera has no GPS matches a phone's track to a day of photos and gets place names filled in without sending anything online. Treatment: the map toolbar's track-log button (Load Tracklog, Auto-Tag Selected Photos, Set Time Zone Offset, Next and Previous Track), an address-lookup suggestion row in the Location field set, and a Private checkbox on saved locations. Cheaper substitute that fails: an online geocoding call. Chrome: consume §6's map and gazetteer, §4's time model, §8's writer, and `D04 T02 §6`'s remove-location option.
- **Runs:** `Requires: display-session -- the track-log workflow needs an interactive desktop`
- **Catalog:** LP-0415, LP-0551 to LP-0553 (4 features)
- **Source:** `-> SOURCE: parity-lumen-tracklogs`
- **Hints:**
  - `GpxReader` in `Photon.Lumen.Core/Places/Gpx/` (own code over `System.Xml`, GPX 1.1) and `TrackMatcher` (LP-0553): interpolation between points, maximum gap, time-zone offset, next and previous track, a match report per photo.
  - `ReverseGeocoder` (LP-0551, LP-0415): GeoNames `cities1000` plus admin1 and country codes (CC BY 4.0) in a k-d tree; suggestions shown dimmed until accepted; attribution in About.
  - Export of suggested locations (LP-0415) as accepted values in bulk.
  - Private locations (LP-0552): GPS stripped from exports inside a private radius, applied by `D04 T12 §13` and `D04 T11 §4`, extending `D04 T02 §6`'s remove-location option.
  - Tests: `GpxReaderTests` (fixture from a phone), `TrackMatcherTests` (offset and gaps), `ReverseGeocoderTests` (known coordinates to expected city and country), `PrivateLocationExportTests`.
  - Commit: `"lumen: GPX track logs, offline reverse geocoding, and private locations"`
- **Proof:** unit plus driven: the matcher tags the fixture day's photos within the expected distance, geocoding returns the expected places with no network (firewall-blocked run quoted), and an export inside a private location has no GPS (exiftool); cheaper substitute that fails: a web geocoder, which the offline run refuses.

#### Sizing concerns

`§2` (20 features) and `§8` (13 features with two fidelity proofs) are the densest; `§2` splits at the ACDSee properties pane and IrfanView dialogs, and `§8` at export embedding if either exceeds 30 items. `§6`'s own map control is the largest engineering item in this file; if it cannot hold, the browse map pane and external hand-offs move to a sibling section rather than adding a map dependency.

### todo/04-lumen/TODO-09-lumen-parity-develop.md -- `lumen-parity-develop`

- **Title:** "TODO-09 -- Lumen Parity: Develop"
- **Phase(s):** 35 (§1 to §8, §10 to §12), 36 (§9, §13 to §16)
- **Goal:** Lumen's develop module reaches Lightroom Classic and ACDSee Develop parity on the suite develop engine: the workspace (tool strip, before and after and reference views, pixel readouts, overlays, panel organization), history, snapshots, and saving develop results as data or as new files, profiles and white balance, presence, the tone curve, color mixer, point color, color grading and ACDSee's Color EQ, color wheel, tone wheels, and split tone, detail, lens corrections with flat-field, Upright, transform, calibration and process versions, effects and crop extensions, masking with brushes, gradients, range masks and pixel targeting, remove, heal, clone and red eye, preset and default management, sync and auto sync, the ACDSee extras (Light EQ, soft focus, skin tune, develop LUTs, blend modes, and effects), soft proofing, and photo merges (HDR, panorama, HDR panorama, focus stacking). Every panel is a surface over `Photon.Core/Develop/` (`D01 T07`) and stores its values in Lumen's edit stack (`D04 T02 §1`); no develop stage is implemented under `src/Lumen/` (the grep of `D04 T02 §2` stays green), the ACDSee-only stages are added to the suite engine by `D01 T07 §7` to `§9`, and the merge engines move from Imago to `Photon.Core/Photo/` on this second consumer. Originals are never written: saving develop results writes settings to the catalog and sidecar, or a new rendered file beside the original.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no source tree, so every path here is a target path created by `D04 T01 §2`. `<!-- claim: absent src/Lumen -->`
  - The suite develop engine is planned, not built, with six sections; this design adds §7 to §9. `<!-- claim: absent src/Photon.Core -->` `<!-- claim: count "^## \d+\. " todo/01-core/TODO-07-photon-develop.md = 6 -->`
  - Lumen's develop file already owns the edit stack, pipeline, panel, crop, presets, export, Edit in Imago, the release, and accessibility. `<!-- claim: count "^## \d+\. " todo/04-lumen/TODO-02-lumen-develop.md = 9 -->`
  - The five develop backlog entries this file promotes (B-028 to B-032) are live today. `<!-- claim: count "^- \[B-0(28|29|30|31|32)\]" todo/backlog.md = 5 -->`
  - No lens database reader and no OpenCV binding exist in the repository yet. `<!-- claim: count "lensfun|Lensfun" src/**/*.cs = 0 -->` `<!-- claim: count "OpenCvSharp" Directory.Packages.props = 0 -->`
- **Inputs and XREFs:** `standards/lumen.md` (float32 linear light, one output transform, preview and export agree, originals never written), `standards/shared.md`, `standards/testing.md`; `docs/parity/lumen-parity.md` (the rows each section owns) and `docs/parity/lumen-section-design.md`; Adobe DNG Specification 1.7.1.0 (opcodes `WarpRectilinear`, `FixVignetteRadial`, `GainMap` for §6); Adobe XMP Camera Raw settings namespace (presets and settings files for §11); darktable 5.0 `darktable-cli` and exiftool 13 as reference tools (versions recorded beside fixtures); -> XREF: D04 T02 §1 (the edit stack every panel writes, extended by §2); -> XREF: D04 T02 §2 (the pipeline and output transform §3 extends); -> XREF: D04 T02 §3 (the develop module §1 extends); -> XREF: D04 T02 §4 (crop §8 extends); -> XREF: D04 T02 §5 (presets and sync §11 and §12 extend); -> XREF: D04 T02 §8 (Lumen 0.1.0 ships before every section here); -> XREF: D04 T01 §9 (loupe, zoom, and filmstrip §1 extends); -> XREF: D01 T07 §1 (settings, pipeline, profiles, process versions for §1, §3, §7); -> XREF: D01 T07 §2 (presence, color mixer, point color, grading, calibration for §3, §4, §7); -> XREF: D01 T07 §3 (detail, lens, geometry, vignette, grain for §5 to §8); -> XREF: D01 T07 §4 (the masking engine §9 surfaces); -> XREF: D01 T07 §5 (spots, red eye, pet eye for §10); -> XREF: D01 T07 §6 (presets, snapshots, XMP exchange for §2, §11, §12); -> XREF: D01 T07 §7, D01 T07 §8, D01 T07 §9 (the ACDSee stages §13 and §14 surface); -> XREF: D01 T04 §2 (proofing transforms and gamut checks for §15); -> XREF: D03 T14 §6 (the lensfun and LCP reader §6 reads through); -> XREF: D03 T15 §4 (the HDR display path §3 consumes); -> XREF: D03 T15 §5, D03 T15 §6, D03 T15 §7, D03 T15 §9 (alignment, HDR, panorama, and focus merge that §16 moves to `Photon.Core/Photo/`); -> XREF: D03 T13 §3 (the content-aware provider §10 reaches through `D01 T07 §5`); -> XREF: D04 T10 §7 (AI masks that join §9's mask list); -> XREF: D04 T10 §8 (Enhance consumes §5's panel); -> XREF: D04 T10 §9 (generative remove joins §10's tool); -> XREF: D04 T10 §11 (AI auto settings beside §3's classical auto); -> XREF: D04 T13 §7 (the DNG writer §6's flat-field and §16's merges write through); -> XREF: D04 T11 §9 (batch develop applies §11's presets); -> XREF: D04 T12 §13 (export presets reuse §2's save-a-copy renderer).
- **Adjacency:** list=applicable (presets list and groups in §11, history and snapshots in §2, the mask list in §9, the merge image list in §16); document=applicable @ D04 T09 §2 (save a rendered copy); settings=applicable (every panel option is a `Lumen.Develop.*` key with a default and a consumer); reporting=applicable (histogram and pixel readouts in §1, proof gamut warnings in §15); notifications=applicable (background saving, merge progress and completion, outdated preset warnings); permissions=applicable (read-only preset folders, missing DCP or LUT files, offline originals refused by name); audit=applicable (one Serilog Information line per committed develop step, preset import, and merge); exchange=applicable (crs XMP presets and settings files, DCP profiles, CUBE and 3DL LUTs, DNG output of merges and flat-field); reverse=applicable @ D04 T02 §1 (every panel change is an edit-stack step; restore to original is one undoable command)

#### §1. The develop workspace extended: tool strip, views, reference, and overlays

- **Deliverable:** The develop module gains the tool strip and edit mode switcher, every before and after layout, a reference view with a locked photo, pixel readouts, a histogram that adjusts tone regions by dragging, zoom presets and a navigator, grid and layout overlays, panel organization (tabs, groups, solo, collapse, detach), scrubby value fields, a collections panel, and the develop filmstrip with fullscreen.
- **Depends On:** D04 T02 §8
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/develop/ (baseline from `D04 T02 §3`), new captures to docs/captures/lumen/develop-views/. Job: a photographer judges an edit against the original or a reference photo at any zoom and reaches every tool and panel from the keyboard. Treatment: Lightroom's tool strip under the histogram (crop, remove, red eye, masking, lens blur), before and after cycling with Y and Alt+Y, reference view with Shift+R, ACDSee's tabbed panes as an alternative panel layout. Cheaper substitute that fails: a single before and after toggle only. Chrome: extend `D04 T02 §3`'s module and `D04 T01 §9`'s loupe, consume the histogram control `D04 T02 §3` moves to `Photon.UI`, the theme, and the icon catalog.
- **Runs:** `Requires: display-session -- the develop views and overlays need an interactive desktop`
- **Catalog:** LP-0290, LP-0556 to LP-0568 (14 features)
- **Source:** `-> SOURCE: parity-lumen-develop-workspace`
- **Hints:**
  - `DevelopToolStrip` in `Photon.Lumen.Desktop/Develop/` with modes Crop, Remove, Red Eye, Masking, Lens Blur (LP-0558); each mode is a `IDevelopToolMode` with enter and exit, the Lens Blur and AI entries disabled with a tooltip naming `D04 T10 §10` and `§7` until they land.
  - `BeforeAfterLayout` enum (LeftRight, LeftRightSplit, TopBottom, TopBottomSplit, Split with a draggable divider) in `Photon.Lumen.Desktop/Develop/Views/` (LP-0559); Y cycles, Alt+Y top and bottom, Shift+Y split, `Lumen.Develop.BeforeAfterLayout`.
  - Reference view (LP-0290, LP-0560): a locked reference photo set by dragging from the filmstrip, left and right or top and bottom, rendered from the preview cache (never the full pipeline), kept per session.
  - Histogram drag-to-adjust (LP-0556): the histogram control maps x to blacks, shadows, exposure, highlights, whites regions and issues edit-stack steps through `D04 T02 §1`; the camera info line (ISO, lens, focal length, aperture, shutter) under it.
  - Pixel readouts (LP-0557): RGB in percent (linear ProPhoto), 0 to 255 (output space), or Lab, with original and edited values from `DevelopPipeline` probes, `Lumen.Develop.Readout`.
  - Zoom and navigator (LP-0561): Fit, Fill, 1:1, 2:1 to 11:1 and 1:4 to 1:2 presets, zoom slider, navigator panel; extends `D04 T01 §9`'s zoom state.
  - Overlays (LP-0565, LP-0562): alignment grid with size and opacity, guides, layout image overlay (a PNG laid over the photo, opacity and matte), loupe info overlay and messages, pin and overlay visibility (Auto, Always, Never, Selected).
  - Panel organization (LP-0566, LP-0564, LP-0568): tabs and groups, solo mode (Alt-click), expand and collapse all, per-panel eye toggle that bypasses the panel's settings group in preview, changed-tab markers, detachable panes, scrubby numeric fields (drag the label), and optional undo and redo buttons.
  - Collections panel in develop (LP-0563) reuses the library collections list; filmstrip with previous and next and F for fullscreen (LP-0567).
  - Tests: `BeforeAfterLayoutTests`, `HistogramDragMappingTests` (a drag in each region yields one step on the right parameter), `PixelReadoutTests` (known pixel gives expected percent, 8-bit, and Lab values), `PanelBypassTests` (eye toggle changes preview only, never the stack).
  - Commit: `"lumen: develop workspace views, reference, overlays, and panel organization"`
- **Proof:** unit plus driven: the tests above pass; a driven session cycles every before and after layout, sets a reference photo, drags the histogram's shadows region (one edit-stack step logged), and captures each view; cheaper substitute that fails: a static before and after toggle, which `BeforeAfterLayoutTests` catch.

#### §2. History, snapshots, and saving develop results

- **Deliverable:** History and snapshots grow to Lightroom's before-state controls, hover previews, snapshot management, clear history, and per-group reset, and ACDSee's develop save semantics become edit-stack operations: done, save, discard, cancel, automatic saving when switching photos, restore to original, commit as a new baked file, save as and save a copy, copy to clipboard, developed and snapshot badges, and settings mirrored to the sidecar.
- **Depends On:** §1
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/develop/ extended with docs/captures/lumen/develop-history/. Job: a photographer can step back through any edit, compare states, and leave develop knowing exactly what was saved, with the original untouched. Treatment: History and Snapshots panels with hover preview (Shift pauses), a before-state menu (copy after to before, swap, set from step or snapshot), per-panel reset menu, ACDSee's Done, Save, Discard, and Cancel on leaving, and a Save As dialog for rendered copies. Cheaper substitute that fails: a Save that writes into the original, which the unchanged-originals test refuses. Chrome: extend `D04 T02 §1`'s edit stack and `D04 T02 §3`'s panels; render copies through `D04 T02 §6`'s `ExportRunner`; consume `D01 T07 §6` snapshots and XMP.
- **Runs:** `Requires: display-session -- the history and save flows need an interactive desktop`
- **Catalog:** LP-0569 to LP-0583 (15 features)
- **Source:** `-> SOURCE: parity-lumen-develop-history`
- **Freeze check:** No save, commit, restore, or snapshot path opens an original for writing; the unchanged-originals test of `D04 T02 §1` is extended to run every command here over the import fixtures.
- **Hints:**
  - Before state (LP-0569): `EditStack.BeforePointer` separate from the current step; commands Copy After to Before, Copy Before to After, Swap, Set Before from Step or Snapshot, each one undoable step.
  - Hover preview (LP-0570): hovering a history step or snapshot renders it into the loupe from the cached demosaic; Shift held pauses it.
  - Snapshot management (LP-0571, LP-0574, LP-0583): update with current settings, rename, delete, create from a history step, a snapshots toolbar in the viewer and develop, snapshot and developed badges on thumbnails (LP-0577) and in the viewer status bar, return to last used settings.
  - Clear history and undo all (LP-0572) with a confirmation naming the step count; clearing keeps snapshots.
  - Per-group reset menu (LP-0573): reset to last saved, default, or last used, save group as preset (feeds §11), copy and paste group.
  - Leaving develop (LP-0576, LP-0580): Done (keep), Save (write the settings to the catalog and sidecar), Discard (drop unsaved steps), Cancel with Esc; `Lumen.Develop.AutoSaveOnSwitch` (default on) saves in the background so RAW switching stays fast; one log line per save.
  - Restore to original (LP-0575): removes develop settings from one or many photos as one batch undo step; the original file is untouched.
  - Commit and save as (LP-0578, LP-0579): render through `ExportRunner` to a new file beside the original (`<name>-developed.<ext>` by default) with metadata, catalog information, settings, and embedded profile choices, stacked with the original; the original is never replaced.
  - Copy developed image to the clipboard (LP-0581) as a 16-bit PNG and DIB.
  - Sidecar mirroring (LP-0582): settings written as `photon-develop:` and `crs:` XMP through `D01 T07 §6` to `<name>.xmp` for RAW and rendered formats when `Lumen.Metadata.WriteSidecars` is on; never an `[Originals]` folder, never the original.
  - Tests: `BeforeStateTests`, `SnapshotManagementTests`, `DevelopSaveSemanticsTests` (done, save, discard, cancel), `CommitAsNewFileTests` (new file exists, original hash unchanged), `SidecarMirrorTests`.
  - Commit: `"lumen: develop history, snapshots, and save semantics that never write the original"`
- **Proof:** unit plus driven: the tests pass and the extended unchanged-originals test passes over every command; a driven session edits, discards, saves, commits a copy, and restores to original with log lines quoted; cheaper substitute that fails: a Save writing into the JPEG, which the hash assertion catches.

#### §3. Profiles, white balance, and presence

- **Deliverable:** The Basic panel gains the profile browser (groups, favorites, grid and list, creative amount, DCP and LUT profile import), treatment, the white balance picker with loupe and strength, texture, clarity and dehaze, auto tone and per-slider auto, output color space for RAW, and HDR editing with SDR preview.
- **Depends On:** §1
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/develop/ extended with docs/captures/lumen/profile-browser/. Job: a photographer picks a starting look, neutralizes color from a gray point, and sets presence without leaving the Basic panel. Treatment: Lightroom's profile browser opened from the profile row, a white balance eyedropper with a magnifying loupe and neutral-pixel highlight, Shift-double-click per-slider auto. Cheaper substitute that fails: a fixed profile list with no import. Chrome: extend `D04 T02 §3`'s Basic panel; consume `D01 T07 §1` profiles and auto tone, `D01 T07 §2` presence, `D03 T15 §4`'s HDR display path.
- **Runs:** `Requires: display-session -- the profile browser and picker need an interactive desktop`
- **Catalog:** LP-0616 to LP-0622 (7 features)
- **Source:** `-> SOURCE: parity-lumen-develop-basic`
- **Hints:**
  - Profile browser (LP-0618) in `Photon.Lumen.Desktop/Develop/Profiles/` listing `D01 T07 §1`'s profile catalog by group, favorites in `Lumen.Develop.ProfileFavorites`, grid and list, hover preview, creative profile amount 0 to 200; import DCP and LUT-based profiles into the suite profile folder; no Adobe or camera-matching profiles are bundled.
  - Treatment color or black and white (LP-0617) switches the settings group and the color mixer's mode (§4).
  - White balance picker (LP-0619): loupe of 9 by 9 pixels with RGB readout, neutral-pixel highlight overlay, strength 0 to 100 percent, W key.
  - Texture, clarity, dehaze (LP-0620) sliders bound to `D01 T07 §2`.
  - Auto tone and auto white balance (LP-0621): `D01 T07 §1`'s classical analysis; per-slider auto on Shift-double-click; a tooltip names `D04 T10 §11` for AI auto settings.
  - Output color space for RAW (LP-0622): default `Lumen.Develop.OutputSpace` (sRGB, Display P3, Adobe RGB, ProPhoto) with embedded profile, extending `D04 T02 §2`'s output transform.
  - HDR editing (LP-0616): an HDR toggle using `D03 T15 §4`'s display path where the display supports it, visualize HDR ranges, HDR limit, SDR preview and rendition settings, extended histogram and curve range; SDR tone-mapped preview otherwise.
  - Tests: `ProfileBrowserViewModelTests` (groups, favorites, amount), `WhiteBalancePickerTests` (a gray card fixture pick neutralizes within delta E 2), `DevelopHdrSettingsTests` (HDR off yields identical output to 0.1.0).
  - Commit: `"lumen: profile browser, white balance picker, presence, and HDR editing"`
- **Proof:** unit plus driven: the tests pass; a driven session imports a user DCP, applies it at 50 percent, picks white balance on the gray card, and toggles HDR with captures; cheaper substitute that fails: profiles hard-coded in the app.

#### §4. Tone curve, color mixer, point color, and color grading

- **Deliverable:** Lumen's color surfaces reach Lightroom and ACDSee: per-channel tone curves with presets and the targeted adjustment tool, the eight-band color mixer and black and white mix, point color, three-way color grading, and ACDSee's Color EQ, color wheel, tone wheels, and split tone mapped onto the suite engine's color stages.
- **Depends On:** §3
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/develop/ extended with docs/captures/lumen/color/. Job: a photographer shifts specific colors and tones precisely, by slider or by dragging on the photo. Treatment: Lightroom's Tone Curve, Color Mixer, Point Color, and Color Grading panels, with ACDSee's Color EQ, color wheel, tone wheels, and split tone as alternative views of the same settings. Cheaper substitute that fails: ACDSee controls stored in a second settings record. Chrome: consume `D01 T07 §1` curves and `D01 T07 §2` mixer, point color, and grading; one `DevelopSettings` record.
- **Runs:** `Requires: display-session -- the color panels and targeted tool need an interactive desktop`
- **Catalog:** LP-0584, LP-0623 to LP-0631 (10 features)
- **Source:** `-> SOURCE: lumen-roadmap-color` (promotes B-031)
- **Hints:**
  - Tone curve (LP-0623): RGB, red, green, blue point curves, curve presets saved as XMP, refine saturation, point readout, black, midtone, and white points with auto, camera or standard base curve, clipping display.
  - Targeted adjustment (LP-0584): Ctrl+Alt+Shift+T tool that maps a drag on the photo to the curve region or the mixer band under the pointer, one step per drag.
  - Color mixer (LP-0624): HSL and per-color modes over eight bands with an All view; black and white mix with auto mix and ACDSee's contrast and colorization (LP-0625).
  - Point color (LP-0626): sampled swatches with hue, saturation, luminance shift, variance, range, visualize range, and use inside masks through §9.
  - Color grading (LP-0627): shadows, midtones, highlights, global wheels, single wheel views, luminance, blending, balance, fine control with Ctrl.
  - ACDSee mappings documented in `Photon.Lumen.Core/Develop/AcdseeMapping.cs`: Color EQ (LP-0628, saturation, brightness, hue, contrast per color, both quality modes) onto the mixer plus a per-band contrast parameter added to `D01 T07 §2`'s mixer if absent (a `Corrected` note in that file); color wheel (LP-0629) onto point color ranges; tone wheels (LP-0630) onto grading; split tone (LP-0631) onto grading highlights and shadows with balance.
  - Tests: `TargetedAdjustmentTests`, `AcdseeColorMappingTests` (each ACDSee control changes only its mapped parameter and round-trips through the edit stack), `ColorPanelsViewModelTests`.
  - Commit: `"lumen: tone curve, color mixer, point color, color grading, and ACDSee color panels"`
- **Proof:** unit plus driven: the tests pass; a driven session drags the targeted tool on sky blue (one step) and captures each panel; cheaper substitute that fails: a second ACDSee settings record, which `AcdseeColorMappingTests` refuse.

#### §5. Detail: sharpening and noise reduction

- **Deliverable:** The Detail panel with sharpening (amount, radius, detail, masking with the Alt mask view, threshold), classical noise reduction (luminance with detail and contrast, color with detail and smoothness, strength, tonal and frequency range, legacy compatibility), and a movable detail zoom preview.
- **Depends On:** §1
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/detail/. Job: a high-ISO photographer sharpens edges and suppresses noise while judging at 1:1. Treatment: Lightroom's Detail panel with the preview window and target, Alt-drag showing the mask as grayscale. Cheaper substitute that fails: sliders judged on a fit-size preview only. Chrome: consume `D01 T07 §3`'s `UnsharpMask`, `RemoveNoise`, and denoise kernels; no stage in Lumen.
- **Runs:** `Requires: display-session -- the detail preview needs an interactive desktop`
- **Catalog:** LP-0632 to LP-0634 (3 features)
- **Source:** `-> SOURCE: lumen-roadmap-detail` (promotes B-029)
- **Hints:**
  - Sharpening controls (LP-0632) bound to `D01 T07 §3`; ACDSee's threshold mapped onto the same stage; Alt-drag renders the mask or radius visualization through a pipeline debug output.
  - Detail zoom preview (LP-0633): a 1:1 window of 256 by 256 px with a movable target, rendered at full resolution for its crop only.
  - Noise reduction (LP-0634): luminance, detail, contrast; color, detail, smoothness; ACDSee strength and tonal and frequency range as parameters of the same stage; legacy compatibility follows the photo's process version (§7).
  - A tooltip on the denoise controls names the Enhance dialog `D04 T10 §8` and B-046 for a machine-learning denoiser.
  - Tests: `DetailPreviewTests` (the crop render equals the full render at the same pixels within 1/255), `DetailPanelViewModelTests`.
  - Commit: `"lumen: detail panel with sharpening, noise reduction, and a 1:1 preview"`
- **Proof:** unit plus driven: tests pass; a driven session on a high-ISO fixture shows the Alt mask view and the detail window (captures); cheaper substitute that fails: fit-size judgment, which the crop-equals-full test guards.

#### §6. Lens corrections

- **Deliverable:** Lens profile corrections matched from EXIF with custom make, model, and profile, saved and mapped lens defaults, chromatic aberration removal, defringe with pickers, manual distortion and vignetting, DNG opcode and distortion tags applied automatically, ACDSee's Auto Lens viewer filter, and flat-field correction written as a new DNG.
- **Depends On:** §1
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/lens/. Job: a photographer removes distortion, vignetting, and fringing with one click and fixes what profiles miss by hand. Treatment: Lightroom's Lens Corrections panel (Profile and Manual tabs) with a fringe picker. Cheaper substitute that fails: manual sliders only. Chrome: consume `D01 T07 §3` and the lensfun and LCP reader of `D03 T14 §6`; the flat-field output through `D04 T13 §7`.
- **Runs:** `Requires: display-session -- the lens panel needs an interactive desktop`
- **Catalog:** LP-0647 to LP-0653, LP-0976 (8 features)
- **Source:** `-> SOURCE: lumen-roadmap-lens` (promotes B-030)
- **Hints:**
  - Profile corrections (LP-0648): enable, auto match through `LensMatcher`, custom make, model, and profile, distortion and vignetting amounts, bundled lensfun data (CC BY-SA 3.0, attribution in About), user LCP files, saved lens defaults per lens and mapped defaults in `Lumen.Develop.LensDefaults`.
  - Chromatic aberration (LP-0647) by profile or automatic; defringe (LP-0650) with purple and green amount and hue, fringe picker, ACDSee's red and cyan and blue and yellow shifts mapped onto the defringe stage.
  - Manual corrections (LP-0649): distortion with constrain crop, lens vignetting amount and midpoint, ACDSee's vignette correction strength and radius.
  - DNG opcodes and tags (LP-0653, LP-0976): `WarpRectilinear`, `FixVignetteRadial`, and `GainMap` opcodes read from DNG files and applied before profile corrections, reported in the panel as "Applied from file".
  - Auto Lens in the viewer (LP-0652): a preview-only toggle rendering viewer images through the lens profile, `Lumen.Viewer.AutoLens` restored at startup; never saved.
  - Flat-field (LP-0651): select a reference frame, compute a smoothed gain map, write `<name>-flatfield.dng` through `D04 T13 §7` stacked with the original.
  - Tests: `LensPanelViewModelTests`, `DngOpcodeTests` (opcode fixture corrected within 1/255 of `dng_validate` output), `FlatFieldTests` (new file written, original hash unchanged).
  - Commit: `"lumen: lens corrections, DNG opcodes, and flat-field"`
- **Proof:** unit plus fidelity: the DNG opcode fixture matches the reference within tolerance; a driven session applies a profile from EXIF on a wide-angle fixture (capture); cheaper substitute that fails: ignoring embedded opcodes, which `DngOpcodeTests` catch.

#### §7. Transform, Upright, and calibration

- **Deliverable:** Upright (auto, level, vertical, full, guided with up to four guides and a loupe), transform sliders, ACDSee's perspective filter, rotate 90 and 5 degree nudges, calibration, and process versions with legacy pipeline emulation.
- **Depends On:** §6
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/transform/. Job: an architecture photographer straightens converging lines and keeps old edits rendering as they did. Treatment: Lightroom's Transform panel with Upright buttons and the Guided tool, Calibration panel, and a process version row with Update. Cheaper substitute that fails: rotation only. Chrome: consume `D01 T07 §3` geometry and Upright, `D01 T07 §2` calibration, `D01 T07 §1` `ProcessVersion`.
- **Runs:** `Requires: display-session -- guided upright needs an interactive desktop`
- **Catalog:** LP-0585, LP-0654 to LP-0659, LP-0977 (8 features)
- **Source:** `-> SOURCE: parity-lumen-develop-transform`
- **Hints:**
  - Upright modes (LP-0654) with reanalyze and Shift cycling; guided upright (LP-0655) with up to four guides in normalized coordinates and a loupe while dragging.
  - Transform sliders (LP-0656): vertical, horizontal, rotate, aspect, scale, offset X and Y, shear, constrain crop; ACDSee perspective (LP-0659) maps onto the same parameters.
  - Rotate 90 and nudge 5 degrees (LP-0658) as crop-angle steps.
  - Calibration (LP-0657): shadows tint and primary hue and saturation.
  - Process versions (LP-0585, LP-0977): a version row showing the photo's version, Update to Current as one undoable step with a before and after preview; photos from older Lumen releases keep rendering bit-identically through the engine's version switch.
  - Tests: `UprightSurfaceTests`, `ProcessVersionUpdateTests` (an old-version fixture renders identically until updated), `TransformPanelViewModelTests`.
  - Commit: `"lumen: upright, transform, calibration, and process versions"`
- **Proof:** unit plus driven: tests pass; a driven guided upright on a building fixture captured; cheaper substitute that fails: silently upgrading old photos, which `ProcessVersionUpdateTests` catch.

#### §8. Effects and crop extensions

- **Deliverable:** Post-crop vignette and grain panels, crop extensions (custom and previous ratios, crop from center, auto straighten, constrain to image, reset), every crop guide overlay, and exact crop size with units and resolution.
- **Depends On:** §1
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/crop/ (baseline from `D04 T02 §4`) and docs/captures/lumen/effects/. Job: a photographer crops to an exact print size along a golden spiral and finishes with vignette and grain. Treatment: Lightroom's Effects panel and crop overlay cycling with O, ACDSee's exact crop fields. Cheaper substitute that fails: thirds only. Chrome: extend `D04 T02 §4`; consume `D01 T07 §3` vignette and grain.
- **Runs:** `Requires: display-session -- the crop overlays need an interactive desktop`
- **Catalog:** LP-0660 to LP-0664 (5 features)
- **Source:** `-> SOURCE: parity-lumen-develop-effects`
- **Hints:**
  - Post-crop vignette (LP-0660): style (highlight priority, color priority, paint overlay), amount, midpoint, roundness, feather, highlights.
  - Grain (LP-0661): amount, size, roughness, and ACDSee's smoothing mapped onto `D01 T07 §3`.
  - Crop extensions (LP-0662): custom ratios in `Lumen.Develop.Crop.CustomRatios`, previous ratio, Alt from center, auto straighten, constrain to image, reset and crop to original.
  - Overlays (LP-0663): thirds, grid, diagonal, triangle, golden ratio, golden spiral, aspect frames, O cycles and Shift+O rotates, show mode, outside opacity.
  - Exact size (LP-0664): width and height in px, cm, in with resolution, constrain list with defaults, maximize, rotate crop, arrow-key resize, preview cropped.
  - Tests: `CropOverlayGeometryTests`, `ExactCropSizeTests` (a 10 by 15 cm at 300 ppi request yields 1181 by 1772 px), `EffectsPanelViewModelTests`.
  - Commit: `"lumen: crop overlays, exact crop size, vignette, and grain"`
- **Proof:** unit plus driven: tests pass; captures of each overlay; cheaper substitute that fails: overlays drawn but no exact size, which `ExactCropSizeTests` catch.

#### §10. Remove, heal, clone, and red eye

- **Deliverable:** The Remove tool with heal, clone, and content-aware modes (size, feather, opacity, source sampling and refresh, stroke-shaped spots), visualize spots and overlay modes, and red eye and pet eye correction, all as develop data.
- **Depends On:** §1
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/remove/. Job: a photographer removes dust and blemishes and fixes red eye without leaving develop. Treatment: Lightroom's Remove tool (Q) with mode buttons and Visualize Spots (A), red eye tool with pet eye mode. Cheaper substitute that fails: clone only. Chrome: consume `D01 T07 §5` and its content-aware provider seam to `D03 T13 §3`.
- **Runs:** `Requires: display-session -- the remove tools need an interactive desktop`
- **Catalog:** LP-0683 to LP-0686 (4 features)
- **Source:** `-> SOURCE: parity-lumen-develop-remove`
- **Hints:**
  - Remove tool (LP-0683): heal and clone modes, size, feather, opacity, source auto-pick and refresh (slash key), drag strokes into shaped spots, toggle mode, skip auto fill; spots stored as `D01 T07 §5` data in normalized coordinates.
  - Content-aware mode (LP-0684) through `D01 T07 §5`'s provider; when the content-aware engine is unavailable the mode is disabled with a tooltip naming it.
  - Visualize spots (LP-0685): an edge-map view with threshold, overlay modes (always, selected, never).
  - Red eye and pet eye (LP-0686): pupil size, darken, catchlight.
  - A tooltip on the generative variant names `D04 T10 §9`.
  - Tests: `RemoveToolViewModelTests`, `SpotResolutionIndependenceTests` (a spot renders the same at two scales within 1/255), `RedEyeSurfaceTests`.
  - Commit: `"lumen: remove, heal, clone, visualize spots, and red eye"`
- **Proof:** unit plus driven: tests pass; a driven dust-removal session on a sensor-dust fixture captured; cheaper substitute that fails: pixel patches stored as bitmaps, which the resolution test catches.

#### §11. Presets and defaults extended

- **Deliverable:** Preset management (create with a settings checklist, update, rename, move, groups, manage dialog), amount and stacking, import and export (XMP, ZIP, Lumen files), visibility and partial compatibility, bundled Lumen preset sets, scoped presets, applying presets from filmstrip, library, and viewer, per-photo settings files, and develop defaults per camera, serial, and ISO.
- **Depends On:** §3
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/presets/ (baseline from `D04 T02 §5`). Job: a photographer organizes hundreds of presets and makes each camera open with the right defaults. Treatment: Lightroom's Presets panel with an Amount slider, Manage Presets dialog, New Preset checklist, and Raw Defaults preferences page. Cheaper substitute that fails: presets as a flat unordered list. Chrome: extend `D04 T02 §5`; consume `D01 T07 §6` `DevelopPresetStore` and crs exchange.
- **Runs:** `Requires: display-session -- preset dialogs need an interactive desktop`
- **Catalog:** LP-0586 to LP-0595 (10 features)
- **Source:** `-> SOURCE: parity-lumen-develop-presets`
- **Hints:**
  - Defaults (LP-0586, LP-0592): reset to Lumen default, set default globally or per camera model, serial, and ISO, raw defaults, save new sharpening and noise defaults, stored through `D01 T07 §6`.
  - Amount and stacking (LP-0587): amount 0 to 200 percent, several presets applied as consecutive steps with a stack list.
  - Management (LP-0588, LP-0594): create with a settings checklist, global, tab, and group scopes with select all, update from current, rename, delete, move, groups and categories, last-used preset.
  - Import and export (LP-0589): crs XMP, ZIP bundles, and Lumen JSON with a tree selection; an import report names unmapped fields.
  - Visibility (LP-0590): filter by name, show partially compatible presets, store presets with the catalog, restore built-in presets.
  - Bundled sets (LP-0591): Lumen's own film, cinematic, moody, and similar presets authored in the repository (license: the project's GPL-3.0), no Adobe or ACDSee presets.
  - Apply from filmstrip, library, and viewer (LP-0593) as batch undo steps.
  - Settings files (LP-0595): export and import per-photo settings as `<name>.xmp` beside the photo, never into the original.
  - Tests: `PresetAmountStackingTests`, `PresetScopeTests`, `RawDefaultsResolutionTests` (serial beats model beats global), `PresetImportReportTests`.
  - Commit: `"lumen: preset management, amount, import and export, and raw defaults"`
- **Proof:** unit plus driven: tests pass; a driven session imports a crs preset ZIP and applies it at 50 percent to 20 photos with one undo step; cheaper substitute that fails: global defaults only, which `RawDefaultsResolutionTests` catch.

#### §12. Sync, copy and paste, and auto sync extended

- **Deliverable:** Snapshot sync, paste from previous with the Previous button, saved copy subsets and modified-only copy, sync without dialog, auto sync, match total exposures, develop settings commands and summary pane from library and viewer, and scaling pasted local settings to targets of other dimensions.
- **Depends On:** §11
- **Phase:** 35
- **Surface:** UI. Fidelity: docs/captures/lumen/presets/ extended with docs/captures/lumen/sync/. Job: a photographer carries one edit across a shoot in the fewest keystrokes. Treatment: Lightroom's Sync and Auto Sync switch, Ctrl+Alt+V previous, ACDSee's develop settings summary pane. Cheaper substitute that fails: sync of global settings only. Chrome: extend `D04 T02 §5`; consume `D01 T07 §6` `DevelopClipboard`.
- **Runs:** `Requires: display-session -- auto sync needs an interactive desktop`
- **Catalog:** LP-0596 to LP-0601 (6 features)
- **Source:** `-> SOURCE: parity-lumen-develop-sync`
- **Hints:**
  - Sync snapshots (LP-0596) across the selection by name.
  - Previous (LP-0597): paste the settings of the previously selected photo.
  - Copy subsets (LP-0598): saved custom subsets in `Lumen.Develop.CopySubsets` and modified-only.
  - Sync without dialog, auto sync mode, match total exposures (LP-0599) as one batch undo step each.
  - Library and viewer commands and a develop settings summary pane (LP-0600).
  - Scaling (LP-0601): masks, spots, and crops are in normalized coordinates and rotated for orientation differences; a test pastes onto portrait and landscape targets.
  - Tests: `AutoSyncTests`, `MatchTotalExposuresTests`, `PasteScalingTests`.
  - Commit: `"lumen: auto sync, previous, copy subsets, and match exposures"`
- **Proof:** unit plus driven: tests pass; auto sync over 50 photos logs one batch step; cheaper substitute that fails: per-photo undo, which the batch undo assertion catches.

#### §9. Masking: brush, gradients, range masks, and pixel targeting

- **Deliverable:** The masking panel over `D01 T07 §4`: brush masks with A and B brushes and eraser, auto mask and smart brushing, linear and radial gradients with brush editing and conversion, color and luminance range masks, set operations and refinement, the masks panel and overlay, the local adjustment set with presets, copying masks between photos, and ACDSee's pixel targeting.
- **Depends On:** §4
- **Phase:** 36
- **Surface:** UI. Fidelity: docs/captures/lumen/masking/. Job: a photographer adjusts only the sky, a face, or the shadows with masks they can refine and reuse. Treatment: Lightroom's Masking panel (Shift+W) with component add, subtract, intersect, the overlay color and modes, and ACDSee's pixel targeting as a mask refinement tab. Cheaper substitute that fails: masks rasterized at preview resolution. Chrome: consume `D01 T07 §4`'s `LocalAdjustmentSet` and mask components; AI components join from `D04 T10 §7`.
- **Runs:** `Requires: display-session -- painting masks needs an interactive desktop`
- **Catalog:** LP-0667 to LP-0682 (16 features)
- **Source:** `-> SOURCE: lumen-roadmap-local` (promotes B-028)
- **Hints:**
  - Masking tool and group (LP-0668) with the local adjustment set (LP-0679): amount, temperature, tint, tone, presence, hue, saturation, fill light, color tint, color EQ, curve, point color, sharpness, noise, moire, defringe as `D01 T07 §4` exposes them.
  - Brush (LP-0669): A and B brushes and eraser with size, feather, flow, density, pen pressure, Shift straight lines, faster brushing, delete strokes; auto mask and smart brushing by color, brightness, or both with tolerance (LP-0670).
  - Gradients (LP-0671, LP-0672, LP-0673): linear with guides and 45 degree lock, radial with feather, squareness, circle constraint, invert, expand to image, brush editing of gradients, convert to brush.
  - Range masks (LP-0674): color and luminance with refine, smoothness, luminance map, add detail.
  - Set operations (LP-0675, LP-0667, LP-0676): add, subtract, intersect, invert, duplicate and invert, rename, hide, enable, clear, up to 24 masks, drag components, delete empty masks, feather and edge shift refinement.
  - Panel and overlay (LP-0677, LP-0678): dock or float, auto hide, component badges, overlay color and modes with cycling, pin visibility, hover to reveal strokes.
  - Presets and reuse (LP-0680, LP-0681): local adjustment presets, copy, paste, and duplicate masks between photos (normalized coordinates).
  - Pixel targeting (LP-0682): tone grabber, color wheels, invert, smoothness, add detail, skin targeting, presets, mapped onto `D01 T07 §4` range components.
  - Tests: `MaskPanelViewModelTests`, `MaskSetOperationTests`, `MaskResolutionIndependenceTests` (preview and export masks agree within 1/255), `PixelTargetingMappingTests`.
  - Commit: `"lumen: masking with brushes, gradients, range masks, and pixel targeting"`
- **Proof:** unit plus driven: tests pass; a driven session brushes a sky mask, subtracts a luminance range, and exports, with preview and export compared; cheaper substitute that fails: preview-resolution bitmaps, which the resolution test catches.

#### §13. Light EQ, soft focus, and skin tune

- **Deliverable:** ACDSee's Light EQ (basic, standard, advanced modes, bands, graph, auto, on-image click and wheel), its instant view and auto preview toggle in the viewer, soft focus, and skin tune panels over the new suite stages.
- **Depends On:** §9, D01 T07 §7, D01 T07 §8
- **Phase:** 36
- **Surface:** UI. Fidelity: docs/captures/lumen/light-eq/. Job: an ACDSee user brightens shadows and tames highlights by tone band, softens portraits, and smooths skin as they did before. Treatment: ACDSee's Light EQ panel with its three modes and the band graph, clicking or wheeling on the image to lift the band under the pointer. Cheaper substitute that fails: Light EQ as a curves preset. Chrome: consume `D01 T07 §7` and `§8`; one `DevelopSettings` record.
- **Runs:** `Requires: display-session -- on-image Light EQ needs an interactive desktop`
- **Catalog:** LP-0635 to LP-0639 (5 features)
- **Source:** `-> SOURCE: parity-lumen-develop-lighteq`
- **Hints:**
  - Light EQ panel (LP-0637) in `Photon.Lumen.Desktop/Develop/LightEq/`: basic (brighten, darken, contrast), standard (band sliders), advanced (curve graph with amplitude), auto; click or wheel on the image adjusts the band under the pointer as one merged step.
  - Viewer instant view and auto preview toggle (LP-0635, LP-0636): preview-only, never saved, `Lumen.Viewer.AutoLightEq`.
  - Soft focus (LP-0638): strength, brightness, contrast, tonal width.
  - Skin tune (LP-0639): smoothing, glow, radius, optionally limited by a mask from §9.
  - Tests: `LightEqPanelViewModelTests` (band mapping), `SoftFocusSkinSurfaceTests`.
  - Commit: `"lumen: Light EQ, soft focus, and skin tune panels"`
- **Proof:** unit plus driven: tests pass; a driven Light EQ session on a backlit fixture with captures; cheaper substitute that fails: a curves preset, which the band-mapping test refuses.

#### §14. Color LUTs, develop blend modes, and develop effects

- **Deliverable:** Color LUTs in develop (CUBE and 3DL import, remove, refresh, apply from a list), develop blend modes, and ACDSee's develop effects (photo looks, color overlay, gradient map, cross process) with opacity and blend mode.
- **Depends On:** §9, D01 T07 §9
- **Phase:** 36
- **Surface:** UI. Fidelity: docs/captures/lumen/develop-effects/. Job: a photographer applies a film LUT or a look at partial strength with a blend mode, non-destructively. Treatment: ACDSee's Color LUTs and Effects groups in the Develop tune tab. Cheaper substitute that fails: LUTs baked into an exported copy. Chrome: consume `D01 T07 §9`.
- **Runs:** `Requires: display-session -- the LUT list needs an interactive desktop`
- **Catalog:** LP-0640 to LP-0642 (3 features)
- **Source:** `-> SOURCE: parity-lumen-develop-looks`
- **Hints:**
  - LUT list (LP-0642) from `Lumen.Develop.LutFolders` with import copying the file into the suite LUT folder, remove, refresh, hover preview, and apply with amount.
  - Blend modes (LP-0641) and effect opacity on the develop look stage.
  - Effects (LP-0640): Lumen's own look set, color overlay, gradient map, cross process as `D01 T07 §9` looks.
  - Tests: `DevelopLutListTests` (import of an unreadable file refused by name), `DevelopLookSurfaceTests`.
  - Commit: `"lumen: develop LUTs, blend modes, and effects"`
- **Proof:** unit plus driven: tests pass; a CUBE LUT applied at 60 percent with soft light captured; cheaper substitute that fails: baking into exports.

#### §15. Soft proofing

- **Deliverable:** Soft proofing in develop: proof profile and intent, simulate paper and ink, monitor and destination gamut warnings, proof background, create a proof copy, and the soft proofing toggle with an emulated device profile.
- **Depends On:** §1
- **Phase:** 36
- **Surface:** UI. Fidelity: docs/captures/lumen/soft-proof/. Job: a photographer sees how a print or web export will look and fixes out-of-gamut colors first. Treatment: Lightroom's S toggle and Soft Proofing panel; Create Proof Copy makes a virtual copy tagged with the profile. Cheaper substitute that fails: a preview with no gamut warning. Chrome: consume `D01 T04 §2`'s proofing transforms and gamut checks.
- **Runs:** `Requires: display-session -- soft proofing needs an interactive desktop`
- **Catalog:** LP-0602 to LP-0603 (2 features)
- **Source:** `-> SOURCE: parity-lumen-develop-proof`
- **Hints:**
  - Proof settings (LP-0602, LP-0603): profile list from `D01 T04 §1`, perceptual or relative intent, simulate paper and ink, background color, stored per photo in `DevelopSettings` view state (not rendered).
  - Gamut warnings: monitor (blue) and destination (red) overlays from `D01 T04 §2` gamut checks.
  - Proof copy: a virtual copy through `D04 T06 §3` when that section has shipped; until then a snapshot named after the profile.
  - Tests: `SoftProofSettingsTests`, `GamutWarningOverlayTests` (a saturated fixture flags the expected pixels for a CMYK profile).
  - Commit: `"lumen: soft proofing with gamut warnings"`
- **Proof:** unit plus driven: tests pass; a driven proof against a user-installed printer profile captured; cheaper substitute that fails: no gamut overlay.

#### §16. Photo merge: HDR, panorama, and focus stacking

- **Deliverable:** Lightroom's Photo Merge and ACDSee's Photomerge in Lumen: HDR merge with deghosting, panorama with projections and boundary warp, HDR panorama in one step, focus stacking, headless merges, and a Photomerge hub, all writing new DNG or TIFF files stacked with their sources, after moving Imago's alignment, HDR, panorama, and focus-merge engines to `Photon.Core/Photo/`.
- **Depends On:** §2, D03 T15 §7, D03 T15 §9
- **Phase:** 36
- **Surface:** UI. Fidelity: docs/captures/lumen/photo-merge/. Job: a photographer merges brackets or a sweep into one editable raw-like file without leaving Lumen. Treatment: Photo, Photo Merge (HDR Ctrl+H, Panorama Ctrl+M, HDR Panorama, Focus Stack) preview dialogs with options and Merge, Shift-headless variants, and ACDSee's hub listing images, output format, location, and metadata retention. Cheaper substitute that fails: sending sources to Imago for merging, which breaks the no-runtime-dependency rule. Chrome: consume the moved engines, `D04 T13 §7`'s DNG writer, `D04 T11 §1` for background jobs, and catalog stacks.
- **Runs:** `Requires: display-session -- the merge dialogs need an interactive desktop`
- **Catalog:** LP-0687 to LP-0692 (6 features)
- **Source:** `-> SOURCE: lumen-roadmap-merge` (promotes B-032)
- **Hints:**
  - First item: move `ImageAligner`, `MatBridge`, the HDR merger, `PanoramaStitcher`, and `FocusMerger` from `src/Imago/Photon.Imago.Core/Photo/` to `src/Photon.Core/Photo/` with their tests to `tests/Photon.Core.Tests/Photo/`, OpenCvSharp4 (Apache-2.0) moving with them in `Directory.Packages.props`; Imago's dialogs repoint; `D03 T15 §5`, `§6`, `§7`, `§9` get a `Corrected` note. Done when: `grep -rn "class PanoramaStitcher" src` finds only `Photon.Core`.
  - HDR merge (LP-0687): auto align, auto settings, deghost none, low, medium, high with overlay, stack with sources, floating-point DNG output (16-bit float or 32-bit float), headless merge with last settings.
  - Panorama (LP-0688): spherical, cylindrical, perspective, auto projection, boundary warp, fill edges through the content-aware provider when available, auto crop, several outputs, vignette compensation, headless.
  - HDR panorama (LP-0689) in one step: brackets grouped by time, merged per position, then stitched.
  - Focus stacking (LP-0692): all or selected images, auto align, limits, sources kept stacked.
  - Photomerge hub (LP-0691): image list, output format (DNG, TIFF 16-bit), location, metadata retention; "Merge in the editor" (LP-0690) is answered by Lumen merging itself, with Edit in Imago offered afterwards.
  - Merges run as background jobs on `D04 T11 §1` with progress and cancel; outputs are new files, the originals untouched.
  - Tests: `PhotoCoreArchitectureTests` (no Imago type referenced from `Photon.Core/Photo/`), `LumenHdrMergeTests` (a synthetic bracket merges within tolerance of the Imago golden), `LumenPanoramaTests`, `FocusStackTests`, the unchanged-originals assertion.
  - Commit: `"lumen: HDR, panorama, and focus merges on the engines moved to Photon.Core"`
- **Proof:** unit plus fidelity: the moved engines' Imago goldens still pass from `Photon.Core.Tests`, Lumen's merge tests pass, and a driven merge of the committed bracket fixture writes a DNG stacked with its sources (capture); cheaper substitute that fails: a copied engine in Lumen, which the move grep and the architecture test catch.

#### Sizing concerns

- §9 carries 16 features and 187 source rows, the densest here; if it passes 30 items, split pixel targeting and mask presets into a new section in Phase 36.
- §1 and §2 are each near 15 features of UI; §2's save semantics could split from snapshot management at authoring.
- §16's move items plus four merge kinds are dense; the move alone can become its own section if the first item exceeds three steps.

### todo/04-lumen/TODO-10-lumen-ai.md -- `lumen-ai`

- **Title:** "TODO-10 -- Lumen AI: Faces, Keywords, Similarity, Culling, and Masks"
- **Phase(s):** 37
- **Goal:** Lumen's AI answers every Lightroom and ACDSee AI job on the suite's three pillars: results are editable, structured data applied as undoable catalog or edit-stack commands; the features are suite-aware (shared AI core, shared segmentation and image adapters moved to `Photon.Core`); and every action is explainable and reproducible through the provenance record. Faces are detected and recognized locally (OpenCV YuNet and SFace on OpenCvSharp4) and never leave the machine; similarity is local perceptual hashing; keywords, captions, alt text, OCR, eye-state culling, and AI mask locating use an OpenRouter vision model with the user's key only after an explicit send with a preview; super resolution and generative removal use the image adapter moved from Imago; denoise is classical with a machine-learning variant in B-046. Code lives in `Photon.Lumen.Core/AI/` and `Photon.Lumen.Core/Faces/`, with shared pieces moved to `Photon.Core/AI/` and `Photon.Core/Imaging/Segmentation/`.
- **Current-state facts to verify (with claim candidates):**
  - Lumen and Photon.Core have no code. `<!-- claim: absent src/Lumen -->` `<!-- claim: absent src/Photon.Core -->`
  - No code talks to OpenRouter or OpenCV yet; the AI core is planned in `D01 T05`. `<!-- claim: count "OpenRouter" src/**/*.cs = 0 -->` `<!-- claim: count "OpenCvSharp" Directory.Packages.props = 0 -->` `<!-- claim: exists todo/01-core/TODO-05-photon-ai.md -->`
  - On-device models beyond this file's face models stay in the backlog. `<!-- claim: count "^- \[B-046\]" todo/backlog.md = 1 -->`
- **Inputs and XREFs:** `standards/lumen.md`, `standards/shared.md`; `docs/parity/lumen-section-design.md` ("AI: Lumen's own, on the three pillars"); OpenCV Zoo `face_detection_yunet` (MIT) and `face_recognition_sface` (Apache-2.0) model cards; Metadata Working Group Guidelines 2.0 (face regions); Zauner 2010 (perceptual hashing); OpenRouter API documentation; -> XREF: D01 T05 §1 (client and structured output); -> XREF: D01 T05 §2 (keys and settings); -> XREF: D01 T05 §3 (provenance record); -> XREF: D01 T05 §4 (the send gate and shared AI surfaces); -> XREF: D03 T10 §6 (segmentation engine moved by §7); -> XREF: D03 T19 §2 (image-generation adapter moved by §8); -> XREF: D03 T19 §8 (upscale service moved by §8); -> XREF: D03 T19 §6 (the locate schema and `VisionLocator` §7 moves); -> XREF: D03 T19 §9 (distraction finder §9 reuses); -> XREF: D03 T19 §14 (depth estimation §10 moves); -> XREF: D03 T19 §15 (develop AI mask components §7 feeds); -> XREF: D03 T15 §5 (OpenCvSharp4 already a suite dependency); -> XREF: D04 T05 §2 (idle-time jobs run through the indexer); -> XREF: D04 T05 §11 (duplicate finder §5 extends); -> XREF: D04 T06 §3 (stacks §5 and §6 create); -> XREF: D04 T08 §2 (face regions in the metadata panel); -> XREF: D04 T08 §5 (keywords §4 promotes into); -> XREF: D04 T09 §5 (detail panel §8 extends); -> XREF: D04 T09 §9 (masking panel §7 extends); -> XREF: D04 T09 §10 (remove tool §9 extends); -> XREF: D04 T11 §1 (batch runners for §8); -> XREF: D04 T13 §7 (DNG writer for §8 outputs).
- **Adjacency:** list=applicable (People view in §3, AI keyword review in §4, culling results in §6); document=not-applicable (no document of its own; §8 writes new files through the DNG writer); settings=applicable (`Lumen.AI.*` keys, each automatic run opt-in); reporting=applicable (usage and cost per action, culling scores, similarity groups); notifications=applicable (queue progress, send previews, cost warnings); permissions=applicable (no key, no network, or a declined send refused by name; faces never sent by People features); audit=applicable (one provenance record and one log line per AI action); exchange=applicable (MWG face regions, keywords, and captions in XMP; face data imported from Lightroom and Picasa); reverse=applicable (every acceptance is one undoable command; AI outputs are new files or develop data that revert)

#### §1. AI in Lumen: the AI menu, the send gate, and provenance

- **Deliverable:** An AI menu and settings page in Lumen over `D01 T05`, the explicit-send gate naming every photo, crop, or face that would leave the machine, per-action cost and usage, provenance records stored in the catalog with an AI data store beside it (with repair), shown in each photo's history and embedded as XMP on export.
- **Depends On:** D04 T02 §8, D01 T05 §4
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/ai/. Job: a user knows what each AI action will send, cost, and change, and can inspect or rerun any past result. Treatment: an AI menu grouping every AI command, a settings page (key through `D01 T05 §2`, model per task, automatic runs off by default), the shared send preview, and a Provenance tab in the photo history. Cheaper substitute that fails: sending on click with no preview. Chrome: consume `D01 T05 §1` to `§4` and their `Photon.UI` surfaces.
- **Runs:** `Requires: display-session -- the send preview needs an interactive desktop`
- **Catalog:** LP-0419 (1 features)
- **Source:** `-> SOURCE: parity-lumen-ai-core`
- **Hints:**
  - `LumenAiTask` in `Photon.Lumen.Core/AI/` (Keywords, Caption, AltText, Ocr, EyeState, Locate, Upscale, Remove, Depth) resolving to `D01 T05 §2` tasks with a model per task.
  - Catalog tables `ai_provenance` (record json, photo id, task, hashes) and an AI data store folder beside the catalog for cached masks, patches, and depth maps (LP-0419), with a repair command that re-links or purges orphans.
  - Send preview lists thumbnails of exactly what leaves (downscaled to `Lumen.AI.MaxEdge`, default 1024, metadata stripped) and the estimated cost.
  - Provenance tab: prompt, model, parameters, seed honored flag, hashes, cost; rerun and compare; XMP embedding on export through `D04 T12 §13`.
  - Tests: `LumenAiSendGateTests` (no request without a confirmed preview), `AiDataStoreRepairTests`, `ProvenanceCatalogTests`.
  - Commit: `"lumen: the AI menu, send gate, and provenance"`
- **Proof:** unit plus driven: tests pass over the recorded OpenRouter transport of `D01 T05 §1`; a driven send preview captured; cheaper substitute that fails: implicit sends, which the gate test refuses.

#### §2. The local face engine

- **Deliverable:** Face detection and recognition on the machine: YuNet detection and SFace 128-dimensional embeddings through OpenCvSharp4, a background detection queue (automatic or on demand, pause, redetect, rerun on changed images, remove face data), recognition from named faces with sensitivity, and idle-time detection through the indexer.
- **Depends On:** §1
- **Phase:** 37
- **Surface:** no surface of its own beyond the settings page rows (People surfaces are §3)
- **Runs:** none
- **Catalog:** LP-0420, LP-0693 to LP-0698 (7 features)
- **Source:** `-> SOURCE: parity-lumen-faces-engine`
- **Hints:**
  - Add OpenCvSharp4 (Apache-2.0) to `Photon.Lumen.Core` if not yet referenced after `D04 T09 §16`'s move, and bundle `face_detection_yunet_2023mar.onnx` (MIT) and `face_recognition_sface_2021dec.onnx` (Apache-2.0) under `Photon.Lumen.Core/Faces/Models/` with license texts; record both in `docs/dev/decisions.md`.
  - `FaceDetector` over OpenCV's `FaceDetectorYN` (falling back to `Net.ReadNetFromONNX` with own post-processing if the wrapper lacks it) returning boxes and five landmarks in normalized coordinates; `FaceEmbedder` over `FaceRecognizerSF` with alignment.
  - Catalog tables `faces` (photo, box, landmarks, embedding, person id, state) and `people`; clustering by cosine distance with thresholds for conservative, moderate, aggressive (LP-0695).
  - `FaceDetectionQueue` (LP-0694, LP-0697, LP-0698): catalog-wide or selection, pause, redetect selected, rerun on changed images, remove all face data; automatic or on demand as a catalog setting (LP-0420, LP-0693); idle runs through `D04 T05 §2` (LP-0696).
  - No face data or crop is ever sent to a network by this engine; a test asserts the AI client is never called.
  - Tests: `FaceDetectorTests` (a committed CC0 group photo yields the expected face count), `FaceRecognitionTests` (same-person pairs closer than different-person pairs on a small committed set), `FaceQueueTests`, `FacesNeverSentTests`.
  - Commit: `"lumen: local face detection and recognition"`
- **Proof:** unit: tests pass and a timing on 1,000 photos is quoted; cheaper substitute that fails: sending faces to a cloud model, which `FacesNeverSentTests` refuse.

#### §3. People: named faces, suggestions, and face tags

- **Deliverable:** The People view and mode with named and unnamed people, grouped unnamed faces, naming by name bar and dialog, suggestions to confirm or deny, merge and manage people, person keywords, search by person, faces in the viewer with the face tool, face regions read and written as MWG regions in sidecars, face data imported from Lightroom and Picasa, delete face records or source images, and People preferences.
- **Depends On:** §2, D04 T08 §2
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/people/. Job: a family photographer names everyone once and finds every photo of a person. Treatment: Lightroom's People view (O) with named and unnamed stacks and ACDSee's People mode with group naming, confirm all and deny all, and a face tool in the viewer. Cheaper substitute that fails: face tags stored only in Lumen with no MWG exchange. Chrome: consume §2, the metadata panel `D04 T08 §2`, keywords `D04 T01 §10`, and the viewer `D04 T04 §9`.
- **Runs:** `Requires: display-session -- the People view needs an interactive desktop`
- **Catalog:** LP-0291, LP-0361, LP-0421, LP-0699 to LP-0716 (21 features)
- **Source:** `-> SOURCE: parity-lumen-people`
- **Hints:**
  - People view and mode (LP-0291, LP-0700, LP-0702, LP-0704) with named, unnamed, and person views, counts beyond 9,999, a catalog-pane People group with face search options (LP-0361).
  - Unnamed faces grouped by embedding similarity or ungrouped, name or delete a whole group (LP-0705); face grid multi-select, face or source thumbnails, send sources to viewer or develop (LP-0706); people folders filter (LP-0707).
  - Naming (LP-0701, LP-0711, LP-0714): name bar with Enter advancing, Name Faces dialog, rename, remove name, profile face, suggestions with pending indicator, confirm, deny, edit inline, confirm all, deny all.
  - Manage people (LP-0712): merge, rename, remove, group by name, count, or suggestions, sort, collapse.
  - Person keywords (LP-0699) as a keyword type in `D04 T01 §10`'s hierarchy, excluded from export by `D04 T12 §13`'s option.
  - Search by person in catalog, quick, and advanced search (LP-0709).
  - Viewer faces (LP-0703, LP-0708): show outlines, face tool to draw or edit outlines, detection as each photo opens (local), unsupported locations reported.
  - MWG regions (LP-0710, LP-0715, LP-0421): read and write `mwg-rs:Regions` in sidecars through `D04 T08 §8`; import embedded or sidecar face data from Lightroom and Picasa when cataloging.
  - Delete (LP-0713): face records only, or source images to the Recycle Bin after confirmation; preferences (LP-0716).
  - Tests: `PeopleViewModelTests`, `SuggestionCommandTests` (confirm all is one undo step), `MwgRegionsRoundTripTests` (a Lightroom-written sidecar region round-trips byte-stable in unknown fields).
  - Commit: `"lumen: people, face naming, and MWG face regions"`
- **Proof:** unit plus driven: tests pass; a driven session names five faces, confirms suggestions, and digiKam or Lightroom-style sidecars show the regions (exiftool output quoted); cheaper substitute that fails: Lumen-only tags, which the MWG round trip catches.

#### §4. AI keywords, captions, and alt text

- **Deliverable:** AI keywords through an OpenRouter vision model (queue, run and rerun on selection, pause, priority scan), a separate AI keyword tree searchable in quick and advanced search, review and promotion into user keywords, captions and alt text drafts, OCR of an image or selection, and AI keyword options with opt-in idle runs.
- **Depends On:** §1, D04 T08 §5
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/ai-keywords/. Job: a user tags a large shoot quickly and accepts only the keywords they agree with. Treatment: ACDSee's AI Keywords group in the Organize tab with assign one, selected, or all, and a Describe command writing caption and alt text drafts into the metadata panel. Cheaper substitute that fails: keywords written straight into user keywords. Chrome: consume §1, `D01 T05 §1` structured output, and the keyword store.
- **Runs:** `Requires: display-session -- the review surface needs an interactive desktop`
- **Catalog:** LP-0362, LP-0717 to LP-0722 (7 features)
- **Source:** `-> SOURCE: parity-lumen-ai-keywords`
- **Hints:**
  - Schema `Photon.Lumen.Core/AI/Schemas/keywords.v1.json` (keywords with optional parent, caption, alt text, detected text) validated on every reply.
  - `AiKeywordQueue` (LP-0717): viewed folder first, run or rerun on selection, clear queue, pause, priority scan; automatic runs only after the user approves a send scope (LP-0721), never on by default.
  - AI keyword tree stored apart from user keywords (LP-0718, LP-0362) and searchable.
  - Review (LP-0719, LP-0720): assign one, selected, or all to user keywords, remove, filter, each acceptance one undoable command; embedding AI keywords into sidecars only after acceptance.
  - Captions and alt text drafts land in the metadata panel fields as proposals.
  - OCR (LP-0722): the vision model returns text; a user-installed Tesseract (Apache-2.0), located by `Lumen.AI.TesseractPath`, is the local path run as an external process.
  - Tests: `KeywordSchemaTests`, `AiKeywordAcceptanceTests`, `AiKeywordQueueTests` over the recorded transport.
  - Commit: `"lumen: AI keywords, captions, alt text, and OCR"`
- **Proof:** unit plus driven: tests pass; a driven run over 20 photos with review captured; cheaper substitute that fails: direct writes to user keywords, which the acceptance test refuses.

#### §5. Similar photos and visual duplicates

- **Deliverable:** A local visual similarity index (DCT pHash, dHash, color and layout signatures) with idle indexing, reanalyze, and rerun, find similar and reverse image search, group by similarity with sensitivity, a similarity criterion in search, and auto-stack by similarity, GPS, capture time, or a combination.
- **Depends On:** §1, D04 T05 §11
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/similar/. Job: a user finds every shot related to one photo and collapses bursts into stacks. Treatment: Lightroom's visual search from the library and ACDSee's Group by Similarity with a sensitivity slider. Cheaper substitute that fails: exact-hash duplicates only. Chrome: consume the indexer `D04 T05 §2`, stacks `D04 T06 §3`, and search `D04 T06 §7`.
- **Runs:** `Requires: display-session -- the similarity views need an interactive desktop`
- **Catalog:** LP-0292 to LP-0293, LP-0363, LP-0723 to LP-0727 (8 features)
- **Source:** `-> SOURCE: parity-lumen-similarity`
- **Hints:**
  - `SimilarityIndex` in `Photon.Lumen.Core/AI/Similarity/` (own code): 64-bit pHash and dHash plus an 8 by 8 color layout signature per photo, a BK-tree over Hamming distance (LP-0723), idle indexing through `D04 T05 §2`, reanalyze selected, rerun on changed images; no GPU required.
  - Find similar and reverse search (LP-0292, LP-0725) and a search criterion with a similarity slider (LP-0363).
  - Group by similarity with sensitivity and an analyze-first prompt (LP-0726), stored sensitivity (LP-0727).
  - Auto-stack by similarity, GPS, capture time, or a combination, plus manual custom stacks (LP-0293, LP-0724) through `D04 T06 §3`.
  - Tests: `PerceptualHashTests` (resized and recompressed copies within distance 6), `SimilarityGroupingTests`, `AutoStackTests`.
  - Commit: `"lumen: local similarity search and auto-stacking"`
- **Proof:** unit plus driven: tests pass; a 10,000-photo index timing quoted; cheaper substitute that fails: byte hashes, which the recompressed-copy test catches.

#### §6. Assisted culling

- **Deliverable:** Background culling analysis (subject and eye focus, eyes open, exposure, misfires, documents), select and reject criteria, results with batch flag, rating, label, collection, auto stack of similar shots, per-photo scores with override, badges, a catalog setting, and analysis at import.
- **Depends On:** §2, §5
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/culling/. Job: a wedding photographer gets a first cut in minutes and overrides any verdict. Treatment: Lightroom's Assisted Culling dialog with criteria and a results grid, badges with hover reasons. Cheaper substitute that fails: verdicts applied as final flags with no reasons. Chrome: consume §2 faces, §5 similarity, and the culling commands of `D04 T01 §11`.
- **Runs:** `Requires: display-session -- the culling review needs an interactive desktop`
- **Catalog:** LP-0294 to LP-0299, LP-0422, LP-0728 (8 features)
- **Source:** `-> SOURCE: parity-lumen-culling`
- **Hints:**
  - `CullingAnalyzer` (LP-0295): subject focus as variance of the Laplacian inside the largest face or a center-weighted region, eye focus on landmark crops, exposure clipping statistics, misfire detection (near-black or near-uniform frames), all local.
  - Eyes open and document detection through the vision model on face crops or thumbnails only when enabled, named in the send preview (LP-0295, LP-0296, LP-0297).
  - Criteria (LP-0296, LP-0297) with thresholds; results (LP-0298): selects, rejects, all, auto stack similar, batch flag, rating, label, collection; removing rejects deletes catalog records only.
  - Scores and override (LP-0299): per-photo and per-face scores, badge hover reasons (LP-0294), manual override as an undoable command.
  - Catalog setting and import-time analysis (LP-0422, LP-0728).
  - Tests: `CullingAnalyzerTests` (blurred and sharp fixtures separate), `CullingResultCommandTests`.
  - Commit: `"lumen: assisted culling with local scores and optional eye-state checks"`
- **Proof:** unit plus driven: tests pass; a driven cull of a 200-photo fixture set with results captured; cheaper substitute that fails: opaque verdicts, which the per-photo score assertions catch.

#### §7. AI masks in develop

- **Deliverable:** Subject, sky, and background masks, landscape classes, object masks by brush or box, and people masks with parts, located by the vision model and cut by the local segmentation engine moved from Imago to `Photon.Core`, stored as develop mask components, recomputed on copy, sync, and presets, with outdated-mask warnings.
- **Depends On:** §1, D04 T09 §9, D03 T10 §6
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/masking/ extended with docs/captures/lumen/ai-masks/. Job: a photographer masks the sky or a person's skin in one click and refines it like any mask. Treatment: Lightroom's Select Subject, Sky, Background, Objects, People, and Landscape entries in the masking panel. Cheaper substitute that fails: masks returned as model bitmaps at model resolution. Chrome: consume the moved segmentation engine, `VisionLocator`, `D01 T07 §4`, and `D04 T09 §9`'s panel.
- **Runs:** `Requires: display-session -- the masking entries need an interactive desktop`
- **Catalog:** LP-0729 to LP-0733 (5 features)
- **Source:** `-> SOURCE: parity-lumen-ai-masks`
- **Hints:**
  - First item: move `GrabCut`, `GuidedFilter`, `GlobalMatting`, and `ClosedFormMatting` from `src/Imago/Photon.Imago.Core/Selection/Segmentation/` to `src/Photon.Core/Imaging/Segmentation/`, and the `locate.v1.json` schema and `VisionLocator` from `Photon.Imago.Core/AI/` to `Photon.Core/AI/Vision/`; Imago repoints; `D03 T10 §6` and `D03 T19 §6` get `Corrected` notes.
  - Mask kinds (LP-0730, LP-0731, LP-0732, LP-0733): subject, sky, background, landscape classes, objects by brush or box, people with parts; each an AI component in `D01 T07 §4` storing the locate reply, the cut parameters, and a cached mask in the AI data store.
  - Recompute on copy, sync, presets, and focus on subject, with update all and outdated warnings (LP-0729); every recompute is a send with preview.
  - Tests: `SegmentationMoveArchitectureTests`, `AiMaskComponentTests` (a recorded locate reply yields the same mask at two resolutions within 1/255), `OutdatedMaskTests`.
  - Commit: `"lumen: AI masks in develop on the shared segmentation engine"`
- **Proof:** unit plus driven: tests pass over recorded replies; a driven sky mask captured; cheaper substitute that fails: model bitmaps, which the resolution test catches.

#### §8. Enhance: denoise, raw details, and super resolution

- **Deliverable:** The Enhance dialog and rules (denoise, raw details, super resolution, headless enhance, background runs), classical denoise and enhanced demosaic, super resolution through the image adapter moved to `Photon.Core/AI/` with a classical fallback, target sizes, batch runners, and an enhanced keyword, every output a new file.
- **Depends On:** §1, D04 T09 §5, D04 T13 §7, D03 T19 §8
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/enhance/. Job: a photographer cleans high-ISO raws and enlarges a crop for print without touching the original. Treatment: Lightroom's Enhance dialog with preview and ACDSee's AI Denoise and Super Resolution dialogs with output options and batch. Cheaper substitute that fails: replacing the original. Chrome: consume the moved adapter, `D01 T07 §3`, `D04 T11 §1`, and `D04 T13 §7`.
- **Runs:** `Requires: display-session -- the Enhance dialog needs an interactive desktop`
- **Catalog:** LP-0734 to LP-0742 (9 features)
- **Source:** `-> SOURCE: parity-lumen-enhance`
- **Hints:**
  - First item: move `GenerationRequestBuilder`, `GenerationCompositor`, `ImageModelCaps`, and `UpscaleService` from `src/Imago/Photon.Imago.Core/AI/` to `src/Photon.Core/AI/Images/`; Imago repoints; `D03 T19 §2` and `§8` get `Corrected` notes.
  - Denoise (LP-0736, LP-0739): classical engine for Bayer, X-Trans, linear DNG, small raw, with strength, preview, output folder options; tooltip names B-046 for a machine-learning denoiser.
  - Raw details (LP-0737): enhanced demosaic from the decoder or a high-quality classical demosaic, written as a linear DNG.
  - Super resolution (LP-0738, LP-0740, LP-0742): 2x linear through the moved `UpscaleService` tiled at model caps, classical detail-preserving fallback offline, 16,000 px limit, target size modes sharing `D04 T11 §5`'s size math.
  - Enhance dialog and rules (LP-0735): apply once, headless, background runs; enhanced keyword (LP-0734).
  - Batch (LP-0741) on `D04 T11 §1`: same or chosen folder, subfolder, overwrite rules, preserve dates, metadata, catalog data; "replace original" becomes a new file.
  - Tests: `EnhanceOutputTests` (a new DNG written, original hash unchanged), `UpscaleMoveArchitectureTests`, `SuperResolutionTargetSizeTests`.
  - Commit: `"lumen: Enhance with denoise, raw details, and super resolution as new files"`
- **Proof:** unit plus driven: tests pass over the recorded transport; a driven batch of five raws writes five DNGs stacked with originals; cheaper substitute that fails: overwriting originals, which the hash test refuses.

#### §9. Generative and distraction removal

- **Deliverable:** Generative remove with variations (generate, cycle, delete, report), object detection while brushing a removal, and distraction removal of people, reflections, and dust, results stored as develop spot data with cached patches and provenance.
- **Depends On:** §7, §8, D04 T09 §10
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/remove/ extended with docs/captures/lumen/generative-remove/. Job: a photographer removes a tourist or a reflection and can switch variations or revert any time. Treatment: Lightroom's Remove tool with the Generative AI option, variation arrows, and Distraction Removal buttons. Cheaper substitute that fails: pixels baked into the photo. Chrome: consume the moved adapter (§8), `DistractionFinder` from `D03 T19 §9` moved beside it, and `D04 T09 §10`.
- **Runs:** `Requires: display-session -- the remove tool needs an interactive desktop`
- **Catalog:** LP-0743 to LP-0745 (3 features)
- **Source:** `-> SOURCE: parity-lumen-generative-remove`
- **Hints:**
  - Generative spot kind in `D01 T07 §5` data: region in normalized coordinates, prompt template hash, variations cached as PNG patches in the AI data store, selected index (LP-0743).
  - Object detection while brushing (LP-0744): locate within the brushed area and cut with the segmentation engine, add and subtract.
  - Distraction removal (LP-0745): people, reflections, dust categories through `DistractionFinder`, rerun per photo on paste with a send.
  - Tests: `GenerativeSpotTests` (revert restores the pre-spot render bit-identically), `VariationCycleTests`.
  - Commit: `"lumen: generative and distraction removal as develop data"`
- **Proof:** unit plus driven: tests pass over recorded replies; a driven removal with three variations captured; cheaper substitute that fails: baked pixels, which the revert test catches.

#### §10. Lens blur and depth

- **Deliverable:** Lens blur from depth (amount, focus range, subject, point or area focus, visualize depth, focus and blur brushes, bokeh shapes and boost), depth range masks, device depth maps from HEIC read locally, estimated depth otherwise, and blur-background adaptive presets.
- **Depends On:** §7
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/lens-blur/. Job: a portrait photographer softens the background with believable bokeh and says where focus falls. Treatment: Lightroom's Lens Blur panel with Visualize Depth and focus brushes. Cheaper substitute that fails: a uniform background blur. Chrome: consume the depth estimator moved from `D03 T19 §14`, `D01 T07 §4` depth components, and `D01 T06 §3` bokeh kernels.
- **Runs:** `Requires: display-session -- lens blur needs an interactive desktop`
- **Catalog:** LP-0746 to LP-0749 (4 features)
- **Source:** `-> SOURCE: parity-lumen-lens-blur`
- **Hints:**
  - First item: move `DepthEstimator` from `src/Imago/Photon.Imago.Core/AI/Depth/` to `src/Photon.Core/AI/Depth/`; Imago repoints with a `Corrected` note in `D03 T19 §14`.
  - Depth sources: embedded HEIC and portrait depth maps read locally, estimated depth otherwise (honest label in the panel), cached in the AI data store.
  - Lens blur (LP-0747, LP-0748): amount, focal range, subject, point or area focus, visualize depth, focus and blur brushes, bokeh shapes circle, bubble, five-blade, ring, anamorphic, cat eye, boost.
  - Depth range masks (LP-0746) as `D01 T07 §4` components; blur-background adaptive presets recomputed on paste (LP-0749).
  - Tests: `LensBlurSettingsTests`, `DepthSourceTests` (embedded depth wins over estimation), `BokehShapeTests`.
  - Commit: `"lumen: lens blur from embedded or estimated depth"`
- **Proof:** unit plus driven: tests pass; a driven portrait blur with Visualize Depth captured; cheaper substitute that fails: uniform blur.

#### §11. Adaptive presets, AI auto settings, and natural-language search

- **Deliverable:** Adaptive presets (subject, sky, portrait, landscape) that build AI masks when applied, an adaptive color profile from local scene analysis, AI auto settings beside the classical auto, and natural-language search over stored AI descriptions.
- **Depends On:** §4, §7
- **Phase:** 37
- **Surface:** UI. Fidelity: docs/captures/lumen/presets/ extended with docs/captures/lumen/adaptive/. Job: a photographer applies a look that adapts to each photo's subject and finds photos by describing them. Treatment: Lightroom's Adaptive preset groups and a search field accepting sentences ("red car at night"). Cheaper substitute that fails: presets with fixed masks. Chrome: consume §7, §4's descriptions, and `D04 T09 §11`.
- **Runs:** `Requires: display-session -- adaptive presets need an interactive desktop`
- **Catalog:** LP-0750 to LP-0751 (2 features)
- **Source:** `-> SOURCE: parity-lumen-adaptive`
- **Hints:**
  - Adaptive presets (LP-0751) store AI mask recipes, recomputed per photo on apply with a send preview; Lumen authors its own adaptive preset set.
  - Adaptive color profile (LP-0750): a scene-adapted look from local histogram and color statistics, no Adobe profile bundled.
  - AI auto settings: the vision model proposes `DevelopSettings` deltas as JSON validated against a whitelist, applied as one undoable step and recorded in provenance.
  - Natural-language search over descriptions stored by §4 (only photos the user chose to describe).
  - Tests: `AdaptivePresetRecipeTests`, `AiAutoSettingsValidationTests` (out-of-range values refused by name), `DescriptionSearchTests`.
  - Commit: `"lumen: adaptive presets, AI auto settings, and natural-language search"`
- **Proof:** unit plus driven: tests pass over recorded replies; a driven adaptive portrait preset across three photos captured; cheaper substitute that fails: fixed masks.

#### Sizing concerns

- §3 carries 21 features of People surfaces; if it passes 30 items, split the viewer face tool and MWG exchange (LP-0703, LP-0708, LP-0710, LP-0711, LP-0715, LP-0421) into a new section in Phase 37.
- §8 combines a move, two classical paths, super resolution, and batch; the batch runner may split at authoring.
- §7's move of four segmentation classes and the locator is the first item; if the move grows beyond three items, it becomes its own section.

### todo/04-lumen/TODO-11-lumen-batch.md -- `lumen-batch`

- **Title:** "TODO-11 -- Lumen Batch Tools: Rename, Convert, Resize, Edit, and Export"
- **Phase(s):** 31
- **Goal:** Batch work is core Lumen (operator decision 2026-09-27): one job engine in `Photon.Lumen.Core/Batch/` runs ordered `IBatchOperation`s (rename, convert, resize, rotate and flip, color, the ACDSee Batch Edit and IrfanView advanced operations, text and watermarks, develop, export) over a file list in the background under one Activity Manager, always with a dry run listing every output name, conflict, and skip before anything is written; one token engine names files and fills overlays across the app and accepts IrfanView's `$`-patterns; outputs are new files through the atomic writer, renames and moves are journaled and undoable, and no original's bytes are ever written. Pixel operations reuse the suite pixel engine and the develop engine, never a copy. Recorded actions, droplets, scripting, and command-line switches stay in B-041 and B-042.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code; the only batch it plans today is develop sync (`D04 T02 §5`) and export (`D04 T02 §6`) with one naming template. `<!-- claim: absent src/Lumen -->` `<!-- claim: count "\{date\}-\{name\}-\{seq\}" todo/04-lumen/TODO-02-lumen-develop.md = 1 -->`
  - The suite-wide batch entry B-042 exists and covers action-based batch; the integration rewords it to exclude Lumen's core batch. `<!-- claim: count "\[B-042\]" todo/backlog.md = 1 -->`
  - The suite pixel engine the operations reuse is planned, not built. `<!-- claim: exists todo/01-core/TODO-03-photon-pixel-engine.md -->` `<!-- claim: absent src/Photon.Core -->`
- **Inputs and XREFs:** `standards/lumen.md` (the guard), `standards/shared.md` (logging, cancellation, atomic writes); `docs/parity/lumen-parity.md`; IrfanView 4.76 help pages `hlp_batch_conversion.htm` and `hlp_text_patternoptions.htm` (the `$`-pattern alias list); ACDSee Photo Studio Ultimate 2027 User Guide batch chapters; Exif 3.0 and IPTC IIM 4.2 (token tag numbers); -> XREF: D01 T02 §5 (the atomic writer every output uses); -> XREF: D01 T03 §2, D01 T03 §4, D01 T03 §5, D01 T03 §6 (resampling, tone, color, noise and sharpen kernels the operations call); -> XREF: D01 T06 §1 (the effect registry advanced filters list); -> XREF: D01 T04 §1 and D01 T04 §2 (ICC conversion for §6); -> XREF: D01 T07 §7 (the tone equalizer stage Batch Edit Light EQ calls); -> XREF: D04 T02 §5 and D04 T02 §6 (develop presets and export the §9 runners reuse); -> XREF: D04 T13 §1 and D04 T13 §6 (reading and per-format writing); -> XREF: D04 T04 §1 (the viewer opens the batch dialog, and its quick edits in D04 T04 §11 to §16 run §7's operations); -> XREF: D04 T05 §6 (single-file rename and file operations share §3's journal); -> XREF: D04 T07 §2 and D04 T12 §1 (import renaming and export naming consume §2); -> XREF: D04 T12 §13 (export watermarks consume §8); -> XREF: D04 T10 §8 (batch denoise and super resolution runners queue in §1).
- **Adjacency:** list=applicable (the batch file list in §10 and Activity history in §1); document=applicable (every output file); settings=applicable (batch profiles, rename presets, token templates, overwrite and destination rules as `Lumen.Batch.*` keys); reporting=applicable (completion reports and the per-file history of §1); notifications=applicable (queued and completed toasts with errors, skips, and warnings); permissions=applicable (read-only destinations, locked files, files open in develop refused by name); audit=applicable (one Serilog Information line per job and per output, and the rename journal); exchange=applicable (outputs in every writable format; batch profiles export as JSON); reverse=applicable (rename and move journals undo; outputs are new files so originals are untouched)

#### §1. The batch engine and the Activity Manager

- **Deliverable:** `Photon.Lumen.Core/Batch/` holds the job engine (a job is an ordered list of `IBatchOperation`s over a file list, with a mandatory dry run) and one Activity Manager pane lists every background job in Lumen (import, export, convert, develop, indexing, faces, similarity, AI keywords) with pause, resume, cancel, reorder, idle-time jobs, notifications, and a history with per-file details.
- **Depends On:** D04 T02 §8, D04 T13 §1
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/activity-manager/. Job: a user starts long jobs and keeps working, sees what is queued, running, and done, and finds any output or failure afterward. Treatment: ACDSee's Activity Manager pane (queued, running, idle, history tabs) with a status-bar indicator, Lightroom's activity centre progress, toasts with Show and Browse output buttons, a history details view (status, name, source, destination, preset). Chrome: consume `Photon.UI` list and toast styles, the settings store, and `D01 T02 §5`. Cheaper substitute that fails: a modal progress dialog per job.
- **Runs:** `Requires: display-session -- the Activity Manager pane and toasts need an interactive desktop`
- **Catalog:** LP-0471, LP-0752 to LP-0761 (11 features)
- **Source:** `-> SOURCE: parity-lumen-batch-engine`
- **Hints:**
  - `BatchJob`, `IBatchOperation` (`Plan(BatchItem) -> BatchPlanStep`, `Execute(ImageBuffer, BatchContext)`), `BatchPlanner.DryRun()` returning every output path, conflict, and skip; `BatchRunner` executes only a confirmed plan (LP-0761).
  - Guard: `OriginalGuard.AssertNotOriginal(path)` on every write target (the catalog knows every original and every source of the job); outputs go through `AtomicFileWriter`; a test proves a full job leaves every source's SHA-256 and last-write time unchanged (LP-0761).
  - `ActivityManager` in `Photon.Lumen.Core/Activity/`: queue with priorities, pause, resume, cancel, reorder, pause and resume all, clear all (LP-0753, LP-0756); one registry every long job reports to, including import's progress and cancel (LP-0471).
  - Idle activities (LP-0755): idle-time job kinds (previews `D04 T01 §7`, similarity `D04 T10 §5`, AI keywords `D04 T10 §4`, faces `D04 T10 §2`) with states and per-kind toggles `Lumen.Activity.Idle.*`; the jobs themselves belong to their sections.
  - Concurrency (LP-0757): parallel items bounded by `Lumen.Batch.MaxParallel` (default core count minus one), never two jobs on the same file, files open in develop skipped with a reason, pause while the user exports or develops by setting.
  - Pane and indicator (LP-0752, LP-0754, LP-0760): queued jobs with progress, remaining count, status-bar entry; convert jobs report per-file status.
  - Notifications (LP-0758): queued and completed toasts with error, skip, and warning counts, Show and Browse output buttons, mute options `Lumen.Activity.Notifications.*`, result report text file beside the output on request.
  - History (LP-0759): completed jobs persisted in the catalog with per-file rows (status, name, source, destination, preset), clear items, reopen a saved search through `D04 T06 §7` when present.
  - Tests: `BatchPlannerTests` (dry run lists every output and conflict), `ActivityManagerTests` (pause, cancel, reorder, one job per file), `BatchGuardTests` (write over an original refused, sources unchanged).
  - Commit: `"lumen: the batch engine and one Activity Manager"`
- **Proof:** unit plus driven: the three test classes pass; a driven run queues a 500-file convert and an import together, pauses and resumes, and the history details and toasts are captured with timings quoted; cheaper substitute that fails: running jobs without a dry run, which `BatchPlannerTests` refuse.

#### §2. The token engine

- **Deliverable:** One token engine names files and fills text across Lumen (batch rename, export and import naming, output folders, text overlays, slideshow, print, web, book, fullscreen captions) with file, date, image, EXIF, IPTC, XMP, GPS, maker-note, counter, and special tokens, an editor dialog with live sample, file-name sanitizing rules, and IrfanView's `$`-patterns accepted as an alias syntax.
- **Depends On:** §1
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/token-editor/. Job: a user builds any name or caption from the photo's data once and reuses it everywhere, including patterns they wrote in IrfanView. Treatment: Lightroom's Filename Template Editor and Text Template Editor (token pickers by group, typed text, live example, presets), ACDSee's rename template field with `*` and `#` placeholders, and an "IrfanView patterns" help tab listing `$` aliases. Chrome: consume the metadata readers (`D03 T17 §10` code in `Photon.Core/Metadata/`) and `Photon.UI` dialogs. Cheaper substitute that fails: a fixed `{date}-{name}-{seq}` template.
- **Runs:** `Requires: display-session -- the template editor needs an interactive desktop`
- **Catalog:** LP-0762 to LP-0774 (13 features)
- **Source:** `-> SOURCE: parity-lumen-token-engine`
- **Hints:**
  - `TokenEngine` in `Photon.Lumen.Core/Tokens/`: parse `{group:name|format}` tokens and the IrfanView alias grammar (`$N`, `$F`, `$D`, `$E36867`, `$I120`, `$T(%Y-%m-%d)`, `$Wx$H`, `#` counters) into one AST; evaluation against a `TokenContext` (file, image, catalog, metadata, counter, job) (LP-0763, LP-0766).
  - File tokens (LP-0767): folder path, last subfolder, name with or without extension, extension, corrected extension, size, folder index, page index, substring ranges.
  - Date and time tokens with strftime-style formats (LP-0768); image tokens width, height, bits, DPI, megapixels, aspect, print size, compression, comment (LP-0769).
  - EXIF tokens for any standard tag by name or number (LP-0771), IPTC tokens for any dataset (LP-0770), GPS latitude, longitude, altitude, time, direction, and a combined pair (LP-0773), Nikon, Canon, and Fuji maker-note fields as far as the reader decodes them (LP-0774).
  - Special tokens and counters (LP-0772): new line, literal `$`, pipe, hash, counter width, start and step, numbers or letters; where each token applies is declared per consumer.
  - Sanitizing rules (LP-0762): illegal characters and spaces replaced per `Lumen.Tokens.IllegalCharReplacement` and `Lumen.Tokens.SpaceReplacement`, reserved Windows names refused.
  - Editors (LP-0763, LP-0764, LP-0765): filename template editor, text template editor for captions, rename templates dialog with system and user templates, `*` and `#` placeholders, insert metadata, live sample; presets and recent templates in `Lumen.Tokens.Templates` (LP-0766).
  - `D04 T02 §6`'s `{date}-{name}-{seq}` template becomes a token template with no behavior change, proven by its existing tests.
  - Tests: `TokenEngineTests` (every token group on fixtures with known EXIF and IPTC), `IrfanViewPatternTests` (a table of IrfanView help examples and their expected outputs), `FileNameSanitizerTests`.
  - Commit: `"lumen: one token engine with IrfanView pattern aliases"`
- **Proof:** unit: the three test classes pass with the IrfanView example table quoted; cheaper substitute that fails: per-feature string replacement, which the shared-engine grep (one `TokenEngine` type used by export, rename, and overlays) exposes.

#### §3. Batch rename

- **Deliverable:** Batch rename runs an ordered, checkable list of up to ten operations (template, search and replace, case, insert, remove, strip spaces) with a live preview of old and new names, presets and history, conflict handling, rename in place or copy and move to a folder, sidecars and RAW+JPEG partners renamed together, catalog records following, and an undo journal; single-photo rename with a template uses the same engine.
- **Depends On:** §2
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/batch-rename/. Job: a user renames hundreds of photos predictably, sees every new name first, and can undo. Treatment: ACDSee's Batch Rename dialog with its operation list and preview grid, IrfanView's rename pattern and search-and-replace fields, and Lightroom's Rename Photo with a template. Chrome: consume §1, §2, `D04 T05 §6`'s file-operation journal, and the catalog. Cheaper substitute that fails: renaming without a preview.
- **Runs:** `Requires: display-session -- the rename dialog and its preview need an interactive desktop`
- **Catalog:** LP-0300, LP-0775 to LP-0784 (11 features)
- **Source:** `-> SOURCE: parity-lumen-batch-rename`
- **Hints:**
  - `RenamePipeline` of `IRenameOperation` (LP-0775): template (LP-0777, tokens from §2, numbers or letters, fixed start or auto-detected continuation, clear templates), search and replace with literal text or a metadata value, case-sensitive, include extension (LP-0778), case change for name and extension (LP-0779), insert and remove text at prefix, suffix, position, before or after text, from the right, overwrite, delimiters (LP-0780), strip spaces (LP-0781).
  - Preview grid (LP-0784): old name, new name, conflict marker; Test Rename computes without touching files.
  - Conflicts (LP-0782): duplicate names and extension changes resolved by ask, skip, or rename with a suffix, decided before the run.
  - In place or copy and move to an output folder (LP-0783): sidecars (`.xmp`, `.thm`) and RAW+JPEG partners renamed together; catalog records follow; image bytes are never rewritten.
  - Journal and undo: `RenameJournal` records every rename; Edit, Undo Rename reverses the whole batch, and names changed outside Lumen since are reported, not overwritten.
  - Presets, last used settings, pattern history, and saved rename profiles (LP-0776) in `Lumen.Batch.Rename.*`.
  - Rename Photo with a template for one or many selected photos in the library (LP-0300) opens the same dialog pre-filled.
  - Tests: `RenamePipelineTests` (each operation and order), `RenameConflictTests`, `RenameJournalTests` (undo restores every name, sidecars and pairs included).
  - Commit: `"lumen: batch rename with preview, pairs, and undo"`
- **Proof:** unit plus driven: the tests pass; a driven rename of 1,000 files with sidecars is undone and the before and after listings quoted equal; cheaper substitute that fails: renaming the image only, which the sidecar assertion catches.

#### §4. Batch convert

- **Deliverable:** Batch convert writes many images to any writable format with per-format options, destination rules (same folder, subfolder, chosen folder, token-driven folders, recreated folder structure), overwrite rules that never touch an original, metadata, catalog fields, and profile carry-over, preserved or set file dates, vector and multi-page source handling, page extraction and tiles, thumbnails saved as files, and optional removal of sources to the Recycle Bin only after a verified conversion.
- **Depends On:** §1, D04 T13 §6
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/batch-convert/. Job: a user turns a folder of anything into the format they need in one pass and trusts the originals are safe. Treatment: IrfanView's batch conversion output settings (format with Options, output folder, subfolder rules, overwrite choice) and ACDSee's Batch Convert destination and options pages. Chrome: consume §1, §2, the registry, and `D04 T13 §6`'s options panel. Cheaper substitute that fails: converting into the source folder over files with the same name.
- **Runs:** `Requires: display-session -- the convert pages need an interactive desktop`
- **Catalog:** LP-0785 to LP-0797 (13 features)
- **Source:** `-> SOURCE: parity-lumen-batch-convert`
- **Hints:**
  - `ConvertOperation` (LP-0789, LP-0786): output format, format options from `D04 T13 §6`, pixel format and color space conversion through `D01 T04 §1`.
  - Destination rules shared by every runner (LP-0785, LP-0793, LP-0794, LP-0795): same as source, a new subfolder, a specific folder, token-driven folders such as `{exif:DateTimeOriginal|yyyy}\{exif:DateTimeOriginal|MM}`, recreate the source structure.
  - Overwrite rules (LP-0790): ask, skip, replace, rename, numbered copy; replace applies to earlier outputs only and `OriginalGuard` refuses any original.
  - Metadata carry-over (LP-0787): EXIF, IPTC, XMP, ICC profile, and catalog fields (rating, keywords, label) embedded in the new file only; file dates kept or set (LP-0788).
  - Remove originals after conversion (LP-0791): opt-in, moves sources to the Recycle Bin (`IFileOperation` with `FOFX_RECYCLEONDELETE`) only after the output is reread and verified, and keeps sources whose metadata the output cannot hold.
  - Vector sources rasterized at a set size and multi-page sources (every page, multi-page to multi-page TIFF or PDF) (LP-0792); extract pages and export image tiles for a selection (LP-0796).
  - Save each thumbnail as an image file (LP-0797) as a convert source mode reading the preview cache.
  - Tests: `ConvertOperationTests` (every writable format reread), `DestinationRuleTests`, `OverwriteRuleTests` (an original can never be replaced), `RecycleAfterVerifyTests` (a corrupt output keeps the source).
  - Commit: `"lumen: batch convert with safe destinations and verified recycling"`
- **Proof:** unit plus fidelity: the tests pass; a converted fixture set rereads through the registry within each format's tolerance and the originals' hashes are quoted unchanged; cheaper substitute that fails: deleting sources after writing, which the corrupt-output test catches.

#### §5. Batch resize, rotate, and flip

- **Deliverable:** Batch resize by dimensions, long or short edge, percentage, megapixels, or print size with fit, stretch, and letterbox methods, enlarge and reduce rules, the full resampling filter list, and presets; batch rotate and flip including transpose, transverse, and EXIF auto-rotate, lossless JPEG operations into new files, and rotate from the file list stored as orientation metadata.
- **Depends On:** §4
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/batch-resize/ and docs/captures/lumen/batch-rotate/. Job: a user sizes and orients a whole shoot for a destination in one step. Treatment: ACDSee's Batch Resize (percentage, width and height, actual print size, resample filter, fit options, presets with shortcuts) and Batch Rotate/Flip (per-image angle with Next Image, force lossless) and IrfanView's resize fields. Chrome: consume §1, §4's destination rules, `D01 T03 §2`, and `D04 T04 §16`'s lossless JPEG transform code. Cheaper substitute that fails: pixel rotation that re-encodes JPEGs.
- **Runs:** `Requires: display-session -- the resize and rotate pages need an interactive desktop`
- **Catalog:** LP-0798 to LP-0807 (10 features)
- **Source:** `-> SOURCE: parity-lumen-batch-resize`
- **Hints:**
  - `ResizeOperation` (LP-0799): width and height, long or short edge, percentage, megapixels, print size with units and resolution, aspect preserved, fit-within rules; modes enlarge only, reduce only, both, min and max dimensions, DPI only (LP-0801); fitting best fit, stretch, letterbox with a color (LP-0806).
  - Filters (LP-0800) through `D01 T03 §2`: box, triangle, Bell, B-spline, bicubic, Mitchell, Lanczos, and a detail-preserving enlarge filter mapped from ACDSee's proprietary ClearIQZ name.
  - Presets with keyboard shortcuts, JPEG options, remember as default (LP-0805) in `Lumen.Batch.Resize.Presets`.
  - `RotateOperation` (LP-0802): 90, 180, flip, transpose, transverse, auto-rotate by EXIF, one angle for all or per image with Next Image; force lossless for JPEG writing a renamed new file beside the source or to a chosen folder (LP-0803, LP-0807, lossless crop and comment on a selection).
  - Rotate from the file list and auto-rotate overlay action (LP-0798): orientation stored in the catalog and sidecar through `D04 T04 §11`'s orientation command; no file written.
  - "Replace the original" rows (LP-0804) are offered only as a new file or as orientation metadata; the dialog says why.
  - Tests: `ResizeOperationTests` (every mode's output dimensions), `ResamplingFilterTests` (against `D01 T03 §2` goldens), `LosslessRotateTests` (DCT coefficients preserved, output rereads, source unchanged).
  - Commit: `"lumen: batch resize, rotate, and flip"`
- **Proof:** unit: the tests pass with jpegtran 3.1's output as the lossless oracle (byte-identical scan data); cheaper substitute that fails: decode and re-encode rotation, which the coefficient comparison catches.

#### §6. Batch color: exposure, profiles, and color depth

- **Deliverable:** Batch adjust exposure (exposure, auto, contrast, fill light, shared or per image), batch levels and auto levels, batch tone curves, and batch ICC profile conversion with rendering intent, each as batch operations writing new files.
- **Depends On:** §4
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/batch-color/. Job: a user evens out a set's brightness or converts a delivery set to a client's profile in one pass. Treatment: ACDSee's Batch Adjust Exposure (exposure, contrast, fill light, levels, auto levels, tone curves tabs with Next Image) and Batch Convert ICC Profile (source or embedded, target, intent). Chrome: consume §1, §4, `D01 T03 §4`, `D01 T04 §1` and `§2`. Cheaper substitute that fails: a single brightness slider.
- **Runs:** `Requires: display-session -- the color pages need an interactive desktop`
- **Catalog:** LP-0808 to LP-0811 (4 features)
- **Source:** `-> SOURCE: parity-lumen-batch-color`
- **Hints:**
  - `ExposureOperation` (LP-0808): exposure, auto, contrast, fill light, shared or per-image values with Next Image, presets.
  - `LevelsOperation` (LP-0809) through `D01 T03 §4`: channel, black, gamma, white, clipping readout, eyedroppers, auto contrast and color with strength and tolerance.
  - `CurvesOperation` (LP-0810): channel, histogram, draggable curve, stored as control points.
  - `IccConvertOperation` (LP-0811) through `D01 T04 §1` and `§2`: source profile or embedded, target profile, rendering intent, black point compensation, output to new files with JPEG options.
  - Color depth changes for batch (grayscale, palette, 16-bit) are the advanced operations of §7 and reuse `D01 T03 §3`.
  - Tests: `BatchColorOperationTests` against `D01 T03 §4` goldens; `IccConvertOperationTests` compare with lcms2 `transicc` values within delta E 0.5.
  - Commit: `"lumen: batch exposure, levels, curves, and profile conversion"`
- **Proof:** unit: the tests pass with delta E quoted; cheaper substitute that fails: assigning a profile instead of converting, which the delta E check catches.

#### §8. Text overlays and watermarks

- **Deliverable:** One overlay engine renders text overlays (font, style, rotation, size, color, opacity, alignment, symbols, tokens, box with border, fill, bevel, shadow, and blend mode) and image watermarks (file, aspect, alpha or keyed transparency, position in pixels or percent, blend mode, opacity) for batch, export, the viewer, slideshows, and print.
- **Depends On:** §2
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/overlay-editor/. Job: a user stamps a caption or logo on many photos exactly where they want it and reuses it on export. Treatment: ACDSee's Batch Edit Text Overlay and Watermark pages and IrfanView's Insert text and Watermark dialogs (start corner, offsets, rectangle size, font scaled to desktop height). Chrome: consume §2, `Photon.Core/Text/` (HarfBuzz engine moved by `D03 T16 §1`), `D01 T03` blend math, and `Photon.UI` dialogs. Cheaper substitute that fails: text drawn by GDI without shaping.
- **Runs:** `Requires: display-session -- the overlay editor needs an interactive desktop`
- **Catalog:** LP-0829 to LP-0833 (5 features)
- **Source:** `-> SOURCE: parity-lumen-overlays`
- **Hints:**
  - `OverlaySpec` record in `Photon.Lumen.Core/Overlays/` (text and image layers, anchor, offsets in pixels or percent, scale relative to image or desktop height) with JSON presets in `Lumen.Overlays.Presets`.
  - Text (LP-0829): font, style, rotation, size, color, opacity, alignment, symbols, tokens from §2 evaluated per image.
  - Box (LP-0830): offsets, border and fill with transparency, bevel, drop shadow, blend mode for box and text.
  - Image watermark (LP-0831): file, keep aspect when resizing, alpha channel or keyed transparent color with tolerance, position, blend mode, opacity.
  - IrfanView insert text and watermark (LP-0832, LP-0833): start corner, offsets, rectangle size, placeholders, font scaled to desktop height.
  - `OverlayRenderer.Render(ImageBuffer, OverlaySpec, TokenContext)` used by `TextOverlayOperation` and `WatermarkOperation`, and by `D04 T12 §13`, `D04 T04 §13`, and print.
  - Tests: `OverlayRendererTests` (placement at each anchor within 1 px, blend and opacity against goldens, token text per image).
  - Commit: `"lumen: one text overlay and watermark engine"`
- **Proof:** unit plus driven: the renderer tests pass; a driven batch stamps 100 photos with a token caption and a logo and a sample is captured; cheaper substitute that fails: a second renderer inside export, which the single-type grep exposes.

#### §7. The batch edit pipeline

- **Deliverable:** The ACDSee Batch Edit wizard and IrfanView's advanced batch options become one ordered edit profile of operations (rotate and straighten, crop, color cast and white point, channel mixer, sepia, grayscale, negative, exposure, Light EQ, noise removal, sharpening, vignette and frame effects, color depth, auto adjust, brightness, contrast, gamma, saturation, color balance, replace color, blur, median, any registry effect, canvas size and border, DPI, text and watermark) with a before-and-after preview, output options, progress, a completion log, and saved profiles.
- **Depends On:** §5, §6, §8
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/batch-edit/. Job: a user builds a recipe of edits once, previews it on any photo of the set, and runs it on thousands. Treatment: ACDSee's Batch Edit wizard (operation list with presets, preview with original and final, next and previous image, zoom, fit, actual size, output page, progress page with per-image bars, completion log) with IrfanView's advanced options folded in as operations and a custom processing order. Chrome: consume §1, §5, §6, §8, the effect registry (`D01 T06 §1`), `D01 T03`, and `D01 T07 §7`. Cheaper substitute that fails: a fixed operation order.
- **Runs:** `Requires: display-session -- the wizard and preview need an interactive desktop`
- **Catalog:** LP-0812 to LP-0828 (17 features)
- **Source:** `-> SOURCE: parity-lumen-batch-edit`
- **Hints:**
  - `EditProfile` (ordered operations with parameters, saved in `Lumen.Batch.EditProfiles`) and the wizard (LP-0812, LP-0824, custom processing order and saved option profiles); the same operations run the viewer's quick edits (`D04 T04 §11` to `§16`).
  - Preview (LP-0813): original and final, next and previous image, zoom, fit, actual size, rendered at screen size and cancelled on change.
  - Output page, progress with per-image bars, completion log, browse output in Explorer or Lumen, save as preset (LP-0814).
  - Geometry: rotate with presets, custom angle, background, straighten by a drawn line, auto crop (LP-0815); crop by proportion or area with orientation rules and from the current selection (LP-0816); canvas size and border or frame (LP-0827); set DPI (LP-0828).
  - Color and tone: color cast removal, white point presets, temperature, tint, saturation (LP-0817, `D01 T03 §5`); channel mixer grayscale, sepia, grayscale, negative (LP-0818); exposure, contrast, fill light, brightness, gamma with exposure warning (LP-0819, `D01 T03 §4`); Light EQ through the tone equalizer stage `D01 T07 §7` (LP-0820); IrfanView color depth, auto adjust, brightness, contrast, gamma, saturation, balance, replace color (LP-0825, `D01 T03 §3` to `§5`).
  - Detail: noise removal variants (despeckle, square, X, plus, hybrid) (LP-0821) and sharpening amount, radius, threshold (LP-0822) through `D01 T03 §6`.
  - Vignette with focal point, zones, round or rectangular, and frame effects (LP-0823) and blur, median, and any registry effect (LP-0826) through the effect registry.
  - Tests: `EditProfileTests` (order is honored; each operation matches its engine golden), `EditPreviewTests` (preview equals full render downscaled within 1/255).
  - Commit: `"lumen: the batch edit pipeline"`
- **Proof:** unit plus driven: the tests pass; a driven profile of eight operations runs on 200 photos with the completion log and captures quoted; cheaper substitute that fails: operations reimplemented in Lumen, which a grep for kernel code under `src/Lumen/` exposes.

#### §9. Batch develop and batch export

- **Deliverable:** Develop presets apply to many photos as a background job from the library or browse (RAW included), optionally exported with the full export options, and batch export writes several outputs per photo (folders, names, formats, sizes) in one queued pass with a preset applied while exporting or converting.
- **Depends On:** §7, D04 T02 §6
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/batch-develop/. Job: a user applies a look to a whole shoot and delivers several sizes and formats without babysitting. Treatment: ACDSee's Batch Develop (preset, apply only or apply and export) and Batch Export (multiple output rows), and Lightroom's apply-preset-to-selection. Chrome: consume `D04 T02 §5` presets, `D04 T02 §6`'s `ExportRunner`, and §1. Cheaper substitute that fails: one export run per output size.
- **Runs:** `Requires: display-session -- the batch develop and export pages need an interactive desktop`
- **Catalog:** LP-0834 to LP-0838, LP-0978 (6 features)
- **Source:** `-> SOURCE: parity-lumen-batch-develop`
- **Hints:**
  - `ApplyPresetOperation` (LP-0834, LP-0838, LP-0978): applies a `D04 T02 §5` preset to each photo's edit stack as one batch undo step, as a background job, including browsed RAW files (their records are created as browsed).
  - Batch develop then export (LP-0837): preset plus the full export options.
  - Preset during export or convert (LP-0836): the export and convert runners accept a preset applied to a temporary settings copy, leaving the edit stack unchanged.
  - Multi-output export (LP-0835): `ExportRunner` takes several output specs (folder, naming, format, size) per photo in one decode, queued in §1.
  - Tests: `BatchDevelopTests` (one undo step restores all stacks), `MultiOutputExportTests` (one decode, N outputs, each reread).
  - Commit: `"lumen: batch develop and multi-output export"`
- **Proof:** unit plus driven: the tests pass; a driven batch develop of 300 RAW files with three outputs each runs with timing quoted; cheaper substitute that fails: decoding once per output, which the decode counter in the test catches.

#### §10. The batch dialog: file lists, profiles, and running from Explorer and the viewer

- **Deliverable:** One batch dialog assembles a file list (add, remove, add all, subfolders, load and save text lists, sort by name, date, size, extension, or EXIF date, preview), works in convert, rename, or convert-and-rename mode, saves and applies batch presets together, opens from the Batch menu with the selection, from the viewer (IrfanView's B key), and from the Explorer context menu, and remembers the last folders.
- **Depends On:** §3, §9, D04 T04 §1
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/batch-dialog/. Job: a user starts any batch from wherever they are, including Explorer, without opening the library. Treatment: IrfanView's Batch Conversion/Rename dialog (work as convert, rename, or both; input list with sort and preview; output settings; start with a progress dialog) and ACDSee's Batch menu with the tag-then-batch workflow. Chrome: consume §1 to §9, `D01 T02 §3` forwarding, and the registry. Cheaper substitute that fails: batch only from the library selection.
- **Runs:** `Requires: display-session -- the dialog and the Explorer verb need an interactive desktop`
- **Catalog:** LP-0839 to LP-0846 (8 features)
- **Source:** `-> SOURCE: parity-lumen-batch-dialog`
- **Hints:**
  - Batch menu and start with the selection (LP-0839); tag-then-batch, including renaming non-image files (LP-0840).
  - File list (LP-0842): add and remove, add all, subfolders, load and save a text list, sort by name, date, size, extension, EXIF date, preview the selected entry.
  - Modes (LP-0844): convert, rename, convert and rename, each composing §3 and §4 operations in one job.
  - Presets (LP-0841): save, update, delete, apply several export presets together, convert presets bound to shortcuts, in `Lumen.Batch.Presets`.
  - From the viewer (LP-0843): `B` opens the dialog with the viewer's folder list through `D04 T04 §1`'s hand-off.
  - Start with a progress dialog and remember the last batch folder (LP-0845) in `Lumen.Batch.LastFolders`.
  - Explorer context menu (LP-0846): a `Convert with Lumen` verb for selected files registered by the installer task of `D04 T04 §3`, launching `Lumen.exe --batch @listfile` through single-instance forwarding; no shell extension DLL.
  - Tests: `BatchFileListTests` (sort orders, text list round trip), `BatchModeTests`, `ExplorerVerbTests` (argument parsing of the list file).
  - Commit: `"lumen: the batch dialog, reachable from Explorer and the viewer"`
- **Proof:** unit plus driven: the tests pass; a driven Explorer right-click convert of 50 files is captured with the Activity Manager entry; cheaper substitute that fails: a verb that opens the library only, which the driven run catches.

#### Sizing concerns

- §2 folds 289 source rows into 13 token families; the checklist stays under 30 only because the IrfanView alias table is data (one test table), not one item per token.
- §7 owns 17 features; if the wizard and preview push it past 30 items, split "the edit profile and wizard" from "the operations" at authoring.
- §1 is shared infrastructure for every long job in Lumen; its idle-activity kinds are registrations only, the jobs live in their sections.

### todo/04-lumen/TODO-12-lumen-parity-output.md -- `lumen-parity-output`

- **Title:** "TODO-12 -- Lumen Parity: Export, Print, Slideshows, Web Galleries, and Books"
- **Phase(s):** 38
- **Goal:** Lumen's output reaches Lightroom Classic, ACDSee Photo Studio Ultimate, and IrfanView parity: the export dialog of `D04 T02 §6` grows every destination, naming, format, sizing, color, preset, metadata, watermark, and post-processing option the three apps offer, including DNG and HDR output and local publish services; a Print module prints single images, grids, picture and custom packages, and contact sheets with printer profiles, print sharpening, and 16-bit output on the suite print frame; slideshows are authored with templates, overlays, titles, music, and transitions and exported to PDF and JPEG; web galleries, books, PDFs, and PowerPoint files are generated locally; and photos go out by email or to the user's own FTP or SFTP server. The code lives in `src/Lumen/Photon.Lumen.Core/Output/` (`Export/`, `Publish/`, `Print/`, `Slideshow/`, `Web/`, `Books/`, `Documents/`, `Share/`) and `src/Lumen/Photon.Lumen.Desktop/Views/Output/`; it consumes the develop pipeline and export runner (`D04 T02 §2`, `D04 T02 §6`), the token engine and watermark engine (`D04 T11 §2`, `D04 T11 §8`), the codec writers and DNG writer (`D04 T13 §6`, `D04 T13 §7`), the print frame in `Photon.UI/Print/` (`D03 T18 §6`), the suite color engine (`D01 T04`), and the suite PDF writer (`D03 T17 §7`); it moves Imago's contact-sheet engine (`D03 T18 §7`) and FTP client (`D03 T17 §12`) to `Photon.Core` on this second use. Nothing in this file opens an original for writing: every output is a new file written through `AtomicFileWriter`, and video export and self-running slideshows are backlog B-043 and B-049.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code, so there is no export, print, or slideshow surface yet; `D04 T02 §6` plans the first export dialog. `<!-- claim: absent src/Lumen -->` `<!-- claim: exists todo/04-lumen/TODO-02-lumen-develop.md -->`
  - There is no shared print frame yet: `Photon.UI` does not exist, and Imago's print section (`D03 T18 §6`) is what moves Nodus's frame there. `<!-- claim: absent src/Photon.UI -->` `<!-- claim: exists todo/03-imago/TODO-18-imago-parity-output.md -->`
  - Lumen's print and contact-sheet idea is a backlog entry today, which §4 promotes. `<!-- claim: count "^- \[B-035\]" todo/backlog.md = 1 -->`
  - No package the output features need is referenced yet (NAudio, DocumentFormat.OpenXml, FluentFTP, SSH.NET). `<!-- claim: count "NAudio|DocumentFormat.OpenXml|FluentFTP|SSH.NET" Directory.Packages.props = 0 -->`
  - `standards/lumen.md` states the guard every output here keeps. `<!-- claim: count "Lumen never writes an original image" standards/lumen.md = 1 -->`
- **Inputs and XREFs:** `standards/lumen.md` (original-file guard, one output transform at the end, preview and export agree), `standards/shared.md`, `standards/testing.md`; `docs/parity/lumen-parity.md` (the rows each section owns); Lightroom Classic 15.5.1 Export, Publish Services, Print, Slideshow, Web, and Book help pages; ACDSee Ultimate 2027 guide chapters on Print, Contact Sheet, Slideshow, Create PDF, Create PPT, HTML Album, Send Email; IrfanView 4.76 Print dialog and HTML export help; PDF 1.7 (ISO 32000-1) with PdfPig as the read-back oracle; ECMA-376 (Office Open XML) with DocumentFormat.OpenXml's validator; the W3C Nu HTML Checker (vnu.jar) as the HTML oracle; OSMF and Blurb are not consulted (cloud excluded); -> XREF: D04 T02 §6 (the export runner, dialog, and presets §1, §2, and §13 extend); -> XREF: D04 T02 §7 (stacking of exported files beside the original, reused by §13); -> XREF: D04 T02 §8 (Lumen 0.1.0, which every section follows); -> XREF: D03 T18 §6 (the print dialog frame in `Photon.UI/Print/` §4 consumes and contributes Lumen pages to); -> XREF: D03 T18 §7 (the contact-sheet engine §6 moves to `Photon.Core/Print/ContactSheets/` and the PDF presentation builder §11 reuses); -> XREF: D03 T17 §7 (the suite PDF writer in `Photon.Core/Pdf/` for books, contact sheets, slideshows, and Create PDF); -> XREF: D03 T17 §12 (the FluentFTP client §9 moves to `Photon.Core/Net/Ftp/`); -> XREF: D01 T04 §1 and D01 T04 §2 (printer profiles, rendering intents, soft proof and gamut warning in print); -> XREF: D01 T03 §2 (the resamplers export and print expose); -> XREF: D03 T16 §1 (the suite text engine in `Photon.Core/Text/` for book and slideshow text); -> XREF: D04 T11 §2 (tokens); -> XREF: D04 T11 §8 (watermarks); -> XREF: D04 T13 §4 (PDF page reading for document printing); -> XREF: D04 T13 §6 and D04 T13 §7 (writers and DNG); -> XREF: D04 T09 §15 (soft proofing the print page shares); -> XREF: D04 T10 §1 (the AI results warning of §13 reads the provenance store); -> XREF: D04 T15 §9 (the Phase 38 release); -> XREF: D06 T01 §3 (the Lumen user guide pages each section adds).
- **Adjacency:** list=applicable (export presets, print templates, slideshow templates, web templates, published collections, and book pages are lists with add, update, remove, import, and export); document=applicable (exports, prints, PDFs, PPTX files, galleries, and books are the documents users carry); settings=applicable (every option is a `Lumen.Output.*` key or a saved preset); reporting=applicable (export and publish summaries, print preview, and the AI results warning); notifications=applicable (background export, publish, upload, and burn jobs report through the Activity Manager of `D04 T11 §1` with a completion notification); permissions=applicable (read-only destinations, missing printers, missing mail clients, and failed FTP logins are refused by name); audit=applicable (one Serilog Information line per export, print job, publish, upload, email, and generated document); exchange=applicable (PDF, PPTX, HTML, JPEG, DNG, AVIF, JPEG XL, PSD, template import and export); reverse=applicable (a cancelled output leaves no partial file; republish replaces only published copies; nothing an output does touches an original)

#### §1. Export extended: destinations, naming, formats, sizing, and color

- **Deliverable:** The export dialog of `D04 T02 §6` gains Lightroom's and ACDSee's destination choices, the full rename template on the token engine, per-format settings and pixel formats, target file size for JPEG, width-and-height, dimension, and resolution sizing with every resampling filter, and any ICC output space at 8, 16, or 32 bits.
- **Depends On:** D04 T02 §8, D04 T11 §2
- **Phase:** 38
- **Surface:** UI. Fidelity: docs/captures/lumen/export/ (baseline from `D04 T02 §6`), new captures to docs/captures/lumen/export-extended/. Job: a photographer sends a selection to exactly the folder, name, format, size, and color space the destination needs without a second tool. Treatment: Lightroom's collapsible sections (Export Location, File Naming, File Settings, Image Sizing) in the existing dialog, with a live example file name and an estimated output size. Cheaper substitute that fails: a fixed list of sizes and sRGB only. Chrome: extend the `D04 T02 §6` dialog and `ExportRunner`, consume the token engine, `D01 T03 §2` resamplers, `D01 T04 §1` transforms, and the `D04 T13 §6` writers; do not add a second export runner.
- **Runs:** `Requires: display-session -- the export dialog and captures need an interactive desktop`
- **Catalog:** LP-0849 to LP-0857 (9 features)
- **Source:** `-> SOURCE: parity-lumen-export-extended`
- **Hints:**
  - `ExportDestination` in `Photon.Lumen.Core/Output/Export/` (LP-0849, LP-0854): specific folder, same folder as the original, choose folder later (asked when the job starts), standard user folders (Pictures, Desktop, Documents), optional subfolder with tokens; a destination equal to an original's path with the same name is refused by name before the job runs.
  - File naming (LP-0850): the rename template from `D04 T11 §2` with custom text, start number, and extension case (lower, upper, as is); the dialog shows the first three resulting names; `Lumen.Export.LastTemplate` and a recent-templates list.
  - File settings (LP-0855): format picker listing every `D04 T13 §6` writer with its option page (quality, compression, bit depth, alpha, pixel format), and the output color space and bit depth (LP-0852): sRGB, Display P3, Adobe RGB, ProPhoto RGB, Rec. 2020, or any installed ICC profile through `D01 T04 §1`, 8, 16, or 32-bit float where the format allows, with the profile embedded.
  - JPEG size limit (LP-0851): binary search over quality (at most 8 encodes) to the largest file under the limit; a limit unreachable at quality 0 is reported per photo, not silently exceeded.
  - Image sizing (LP-0853, LP-0856): long edge, short edge, width and height, dimensions (fit inside), megapixels, percentage, resolution in pixels per inch or centimeter, enlarge only, reduce only, or both, preserve aspect, units in pixels, inches, or centimeters.
  - Resampling filter choice (LP-0857): bell, bicubic, box, B-spline, detail-preserving enlarge, Lanczos, Mitchell, triangle from `D01 T03 §2`, default Lanczos for reduction and detail-preserving for enlargement.
  - Settings in `Lumen.Output.Export.*` through the settings store; the whole dialog state serializes into the preset format `D04 T02 §6` defined, versioned so older presets load.
  - Tests: `ExportDestinationTests` (each destination, the refusal of an original's path), `ExportNamingTests` (template, start number, extension case, collision with `D04 T02 §6`'s Overwrite, Skip, Unique), `JpegSizeLimitTests` (a 500 KB limit on the committed fixture lands under 500 KB within 8 encodes), `ExportColorSpaceTests` (ProPhoto and Rec. 2020 profiles embedded and read back by `D01 T04 §1`).
  - Fidelity: a 16-bit ProPhoto TIFF export of the committed DNG matches the pipeline golden within 1/65535 after the stated resize.
  - Update `docs/user/lumen/export.md` for every new option.
  - Commit: `"lumen: export destinations, naming, formats, sizing, and color spaces"`
- **Proof:** unit plus fidelity: the four test classes pass and the ProPhoto TIFF fidelity comparison reports within tolerance; a driven export of 50 photos to "choose folder later" with a size limit is captured; cheaper substitute that fails: a JPEG quality slider standing in for the size limit, which `JpegSizeLimitTests` catches.

#### §13. Export presets, metadata, watermarks, and post-processing

- **Deliverable:** Exports run from built-in and user presets (several at once, with previous, without the dialog), with Lightroom's metadata choices and person and location removal, the watermark engine, develop settings embedded on request, the result added to the catalog and stacked, post-processing actions, disc burning, completion sounds, and a warning when stored AI results need recomputing.
- **Depends On:** §1, D04 T11 §8
- **Phase:** 38
- **Surface:** UI. Fidelity: docs/captures/lumen/export-extended/. Job: a photographer repeats the right export in one click and trusts what metadata leaves the machine. Treatment: a preset tree on the dialog's left (built-in, user folders) with checkboxes for multi-preset export, File, Export with Previous (Ctrl+Alt+Shift+E) and Export with Preset submenus, Metadata, Watermarking, and Post-Processing sections. Cheaper substitute that fails: one preset at a time and metadata all-or-nothing. Chrome: consume the `D04 T11 §8` watermark engine and editor, the catalog stacking of `D04 T02 §7`, the Activity Manager of `D04 T11 §1`, and the provenance store of `D04 T10 §1`; do not write a second watermark renderer.
- **Runs:** `Requires: display-session -- the preset tree, submenus, and a disc burn need an interactive desktop`
- **Catalog:** LP-0424, LP-0873 to LP-0888, LP-0980 (18 features)
- **Source:** `-> SOURCE: parity-lumen-export-presets`
- **Hints:**
  - Presets (LP-0875, LP-0876, LP-0888): built-in presets (Web JPEG, Full-size TIFF, Email, Print TIFF) plus user preset folders with add, update with current settings, remove, rename, import, and export (`.lumenexport` JSON); Export with Preset and Export with Previous run without the dialog; presets listed in File, Export.
  - Multi-preset export (LP-0877, LP-0885, LP-0980): tick several presets to write one file per preset, a parent folder with per-preset subfolders, and a conflict suffix; export from develop writes several copies with their own format and size in one job.
  - Metadata choices (LP-0879, LP-0887): copyright only, copyright and contact, all except camera and camera raw info, all; remove person info (LP-0873: person keywords and MWG face regions), remove location; write keywords as the Lightroom hierarchy; preserve the last-modified date; include catalog fields (rating, label, title, caption).
  - Include develop settings (LP-0424): an option writes the `photon-develop:` and `crs` XMP of `D01 T07 §6` into rendered JPEG, TIFF, PNG, and PSD outputs (never into the original).
  - Watermark (LP-0880): the `D04 T11 §8` engine and editor (text or graphic, shadow, opacity, anchor, inset, presets) applied at output size.
  - Add to catalog and stack (LP-0878): exported files enter the catalog with origin `library`, stacked with the source through `D04 T02 §7`'s stacks.
  - Post-processing (LP-0881, LP-0884): do nothing, show in Explorer, open in Imago (through `D02 T15 §11`'s `SuiteAppLocator`), open in another application, or run a program from the export actions folder `%APPDATA%\Rizonesoft\Lumen\Export Actions\` with the file list as arguments; programs only the user placed there run.
  - Burn to disc (LP-0874): IMAPI2 (`IDiscMaster2`, `IDiscFormat2Data`, part of Windows) as a destination, writing to a staging folder first and burning with progress; a machine without a writer hides the destination with a tooltip saying why.
  - Completion sound (LP-0882) through the system sound `Lumen.Output.Export.Sound`, and the AI warning (LP-0883): before the job, photos whose stored AI masks or removals are marked stale by `D04 T10 §1` are listed with Update, Export Anyway, and Cancel.
  - Rename template in the export dialog (LP-0886) with original-name and sequence tokens, metadata fields, recent templates, and start number, shared with §1.
  - Tests: `ExportPresetStoreTests` (round trip, older versions load), `MultiPresetExportTests` (three presets yield three files in three folders), `ExportMetadataFilterTests` (each choice; person and location removal verified by reading the output with exiftool 13), `ExportPostProcessTests` (fake launcher), `ExportDevelopSettingsEmbedTests` (the XMP block present in outputs, the original's hash unchanged).
  - Commit: `"lumen: export presets, metadata choices, watermarks, and post-processing"`
- **Proof:** unit plus driven: the five test classes pass; exiftool output of a person-and-location-stripped export is quoted; a driven multi-preset export with a watermark is captured; cheaper substitute that fails: stripping only EXIF GPS, which leaves XMP location and face regions that `ExportMetadataFilterTests` catches.

#### §2. Export formats and DNG output

- **Deliverable:** Export writes flattened PSD and PSB, TIFF with transparency, AVIF and JPEG XL with quality, lossless, and HDR, DNG with Lightroom's options, rendered DNG with edits baked in, HDR outputs with an SDR base and gain map, and "original plus sidecar" that copies the original bytes and writes the metadata beside them.
- **Depends On:** §1, D04 T13 §6, D04 T13 §7
- **Phase:** 38
- **Surface:** UI. Fidelity: docs/captures/lumen/export-extended/. Job: a photographer exports to the modern, HDR, or archival format a destination needs, or hands off the untouched original with its metadata. Treatment: new entries in §1's format picker with their option pages, and an HDR Output checkbox that enables HDR spaces and the gain-map choice. Cheaper substitute that fails: an 8-bit SDR render saved under an HDR extension. Chrome: consume the `D04 T13 §6` writers and the `D04 T13 §7` DNG writer; do not add codecs in `Photon.Lumen.Core`.
- **Runs:** `Requires: display-session -- the format pages need an interactive desktop`
- **Catalog:** LP-0423, LP-0858 to LP-0863 (7 features)
- **Source:** `-> SOURCE: parity-lumen-export-formats`
- **Hints:**
  - PSD and PSB (LP-0858): a flat composite with profile and resolution through the `Photon.Core` PSD writer moved by `D03 T17 §2`; PSB above 30,000 pixels a side.
  - TIFF with transparency (LP-0859): an alpha channel for photos whose develop crop or AI removal produced transparent areas, marked as unassociated alpha.
  - AVIF and JPEG XL (LP-0861): quality, lossless, speed, and HDR (PQ or HLG, 10 or 12 bit) through the moved libavif (BSD-2-Clause) and libjxl (BSD-3-Clause) writers.
  - HDR output (LP-0863): HDR color spaces (Rec. 2020 PQ and HLG, Display P3 PQ) and an SDR base JPEG or AVIF with an ISO 21496-1 gain map for compatibility, with the SDR rendition from `D01 T07 §1`'s tone map.
  - DNG export (LP-0860): compatibility level, JPEG preview size, fast load data, lossy compression, and embed original raw through `D04 T13 §7`.
  - Render to DNG (LP-0423): a linear DNG with the develop edits baked in, written as a new file beside or into the destination, never over the source.
  - Original plus sidecar (LP-0862): copy the original bytes unchanged (hash verified after copy) and write the catalog's metadata into an `.xmp` sidecar next to the copy.
  - Tests: `ExportFormatMatrixTests` (each format round-trips through its reader within its stated tolerance), `GainMapExportTests` (the SDR base decodes on a reader without gain-map support and the gain map reads back), `OriginalWithSidecarTests` (hash equal to the original, sidecar fields present), `RenderedDngTests` (`dng_validate` from the Adobe DNG SDK used as an oracle only, version quoted).
  - Fidelity: the committed DNG exported to AVIF lossless and JPEG XL lossless decodes equal to the 16-bit pipeline render within 1/65535.
  - Commit: `"lumen: export to PSD, AVIF, JPEG XL, DNG, HDR with gain maps, and original plus sidecar"`
- **Proof:** format fidelity proof: the lossless AVIF and JPEG XL comparisons and `dng_validate` on the rendered DNG are quoted, and `OriginalWithSidecarTests` passes; cheaper substitute that fails: renaming a JPEG to `.avif`, which the matrix round trip catches.

#### §3. Publish to local folders

- **Deliverable:** A Publish Services panel with a Hard Drive service publishes collections to local or network folders, tracks each photo's publish state (new, modified, published, to remove), republishes changed photos, marks up to date, removes published copies, opens the destination, and imports and exports service settings.
- **Depends On:** §13
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/publish/. Job: a photographer keeps a folder (a frame, a phone sync folder, a NAS share) in step with a collection without re-exporting everything. Treatment: Lightroom's Publish Services panel in the left panel with published collections, smart and folder-set groups, a Publish button, and the grid split into New Photos to Publish, Modified Photos to Re-Publish, Published Photos, and Photos to Remove. Cheaper substitute that fails: an export preset run by hand each time. Chrome: consume §1 and §13's export runner and presets, the collections of `D04 T01 §10`, and the Activity Manager; Flickr, Adobe, and other online services are excluded as cloud.
- **Runs:** `Requires: display-session -- the publish panel needs an interactive desktop`
- **Catalog:** LP-0864 to LP-0865 (2 features)
- **Source:** `-> SOURCE: parity-lumen-publish-local`
- **Hints:**
  - `PublishService` in `Photon.Lumen.Core/Output/Publish/` with one kind, Hard Drive (LP-0864): destination folder, an export preset, and published collections (manual, smart, and folder sets).
  - A `published` catalog table (photo, collection, output path, edit version hash, published time) and a state resolver comparing the current edit version with the published one.
  - Publish writes new and modified photos, deletes only files it published itself (to the Recycle Bin, never originals), and marks up to date without writing.
  - Go to Published Folder (LP-0865) opens Explorer at the destination; service settings import and export as `.lumenpublish` JSON.
  - Tests: `PublishStateTests` (develop change flips to modified; removal lists the photo), `PublishRunnerTests` (republish replaces only the published copy; a file the user added to the folder is untouched).
  - One Serilog Information line per publish with counts.
  - Commit: `"lumen: publish collections to local folders"`
- **Proof:** unit plus driven: the two test classes pass; a driven publish, develop change, and republish is captured with the log lines quoted; cheaper substitute that fails: re-exporting every photo, which `PublishStateTests` catches.

#### §4. Print I: the print module, page setup, and the print job

- **Deliverable:** A Print module prints single images and contact-sheet grids with margins, page grid, cell spacing and size, and guides; sends the job to a printer or to a JPEG file with draft mode, print resolution, 16-bit output, print sharpening, and Lumen- or printer-managed color with a printer profile, rendering intent, and print adjustments; and prints from browse and the viewer with a live preview.
- **Depends On:** D04 T02 §8, D03 T18 §6
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/print/. Job: a photographer prints what they see, sized and color managed for the paper, from the library or straight from the viewer. Treatment: Lightroom's Print module (template browser left, preview center, Layout Style, Image Settings, Layout, Guides, Page, and Print Job panels right), with Print and Print One Copy; the viewer's File, Print opens the same frame with the current photo. Cheaper substitute that fails: sending the screen preview to the default printer. Chrome: contribute Lumen pages to the `Photon.UI/Print/` frame moved by `D03 T18 §6` through its `IPrintPageSource` seam, and consume `D01 T04 §1` and `§2`, `D04 T02 §6`'s output sharpening, and the develop pipeline; do not build a second print dialog.
- **Runs:** `Requires: display-session -- the Print module and the Microsoft Print to PDF proof need an interactive desktop`
- **Catalog:** LP-0895 to LP-0906 (12 features)
- **Source:** `-> SOURCE: lumen-roadmap-print` (promotes B-035)
- **Hints:**
  - `LumenPrintPageSource : IPrintPageSource` in `Photon.Lumen.Core/Output/Print/` renders each cell from the develop pipeline at print resolution (LP-0895), so the preview and the job read the same pixels.
  - Layouts (LP-0896): single image and contact sheet grid with units, margins, page grid rows and columns, cell spacing and size, keep square, and guides (rulers, bleed, margins, cells, dimensions).
  - Print job (LP-0897): printer or JPEG file, draft mode (cached previews), print resolution, JPEG quality and custom file dimensions for print to file, 16-bit output where the driver accepts it.
  - Print sharpening (LP-0898): matte or glossy, low, standard, high, reusing `D04 T02 §6`'s output sharpening at print resolution.
  - Color (LP-0899, LP-0904): managed by printer or by Lumen with a printer profile, rendering intent, black point compensation, soft proof and gamut warning through `D01 T04 §2` (shared with `D04 T09 §15`), and print adjustment brightness and contrast applied only to the print.
  - Page setup, printer settings, Print, and Print One Copy (LP-0900, LP-0903): printer, paper, orientation, copies, page range, resolution from the frame's printer pages.
  - Which photos print and saved print collections (LP-0901): all filmstrip photos, selected, or flagged; page navigation; save the print as a collection.
  - Print from browse and the viewer (LP-0902, LP-0905, LP-0906): print all or selected images as single pages with the live preview, direct print with current settings, and the Quick View print with captions and headers.
  - Tests: `LumenPrintLayoutTests` (cell geometry for each layout and margin set), `PrintColorTransformTests` (a printer profile and intent map known patches within delta E 1 of the `D01 T04` reference), `PrintToFileTests` (JPEG at 300 ppi has the stated pixel size and embedded profile).
  - Proof run through Microsoft Print to PDF: the PDF's page size and placed image size read back with PdfPig match the layout within 0.5 mm.
  - Commit: `"lumen: the print module with managed color, sharpening, and print to file"`
- **Proof:** unit plus driven: the three test classes pass and the Microsoft Print to PDF read-back is quoted; captures of each layout are committed; cheaper substitute that fails: printing the screen preview, which the print-resolution pixel size test catches.

#### §5. Print II: packages, overlays, templates, and document printing

- **Deliverable:** Picture and custom package layouts, the print template browser, page overlays (background, identity plate, watermark, page numbers and info, crop marks, captions), IrfanView's print size modes and dialog options, headers and footers with tokens, resampling and printer adjustments, print profiles, multipage and selection printing, and printing PDF pages.
- **Depends On:** §4
- **Phase:** 38
- **Surface:** UI. Fidelity: docs/captures/lumen/print/. Job: a photographer prints a package of sizes on one sheet, reuses layouts, and prints with captions exactly as IrfanView and ACDSee users expect. Treatment: Picture Package and Custom Package layout styles with rulers, grid snap, draggable cells, and Auto Layout; a Template Browser with user folders; Page panel overlays; an IrfanView-style Print Setup page with size modes. Cheaper substitute that fails: fixed layouts with no saved templates. Chrome: consume §4's page source and frame, the token engine (`D04 T11 §2`), the watermark engine (`D04 T11 §8`), the identity plate of `D04 T14 §1`, and the `D04 T13 §4` PDF reader.
- **Runs:** `Requires: display-session -- the package editor and captures need an interactive desktop`
- **Catalog:** LP-0907 to LP-0921, LP-0948 (16 features)
- **Source:** `-> SOURCE: parity-lumen-print-packages`
- **Hints:**
  - Picture package and custom package (LP-0908, LP-0910): standard cell sizes, rulers, grid snap, drag cells, auto layout, new page, and predefined multi-image layouts with prints per photo.
  - Template browser (LP-0907): built-in and user templates as `.lumenprint` JSON with save, update, import, and export.
  - Page overlays (LP-0909): background color, identity plate, watermark, page numbers, page info, crop marks, and photo info captions.
  - Captions, headers, and footers (LP-0915, LP-0919) with fonts, alignment, line limits, and `D04 T11 §2` tokens.
  - Size modes and custom formats (LP-0914, LP-0917): original DPI, best fit, fill paper, stretch, custom size and margins, scale, center, position, number of prints, auto rotate, crop or shrink to fit, borderless where the driver allows, no overflow.
  - IrfanView print dialog details (LP-0916): default printer, remembered driver values per printer (DEVMODE saved in settings), color or black-and-white preview, orientation auto rotate.
  - Print resampling filters (LP-0911) from `D01 T03 §2`; print gamma and printer exposure, contrast, sharpness (LP-0912) applied to the print only; EXIF print information for printers that read it (LP-0913) through the Exif Print tags on print to file.
  - Print profiles (LP-0918): save the whole print setup without printing; multipage printing (LP-0920) with page ranges, odd or even, reverse, copies, collate; print only the viewer's selection (LP-0921) from `D04 T04 §11`.
  - Document printing (LP-0948): PDF pages through the `D04 T13 §4` reader with page ranges, pages per sheet, duplex, and collation; Office documents are handed to their associated application's print verb and a mixed selection prints images and documents in order.
  - Tests: `PicturePackageLayoutTests`, `PrintTemplateStoreTests`, `PrintSizeModeTests` (each mode's placed size on A4 and Letter), `PrintOverlayTests` (token captions and page numbers render in the preview bitmap), `DocumentPrintTests` (PDF page range selection).
  - Commit: `"lumen: print packages, templates, overlays, and document printing"`
- **Proof:** unit plus driven: the five test classes pass; a package printed through Microsoft Print to PDF reads back with PdfPig showing each cell size within 0.5 mm; cheaper substitute that fails: a single fixed package layout, which `PicturePackageLayoutTests` catches.

#### §6. Contact sheets

- **Deliverable:** Contact sheets from a selection or folder as image files, PDF, HTML image maps, or prints, with columns, rows, cell size and spacing, paper size, frames and thumbnail effects, backgrounds, headers, footers, and captions with tokens, saved as presets, on Imago's contact-sheet engine moved to `Photon.Core`.
- **Depends On:** §4, D03 T18 §7
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/contact-sheet/. Job: a photographer makes an index print or an image map of a shoot in one dialog. Treatment: ACDSee's and IrfanView's Contact Sheet dialog (layout, text, output tabs) with a live preview, reachable from Create, browse, and the Print module's contact sheet layout. Cheaper substitute that fails: a screenshot of the grid. Chrome: consume the moved engine, §4's page source for printing, the suite PDF writer, and the token engine.
- **Runs:** `Requires: display-session -- the dialog and captures need an interactive desktop`
- **Catalog:** LP-0922 to LP-0925 (4 features)
- **Source:** `-> SOURCE: parity-lumen-contact-sheets`
- **Hints:**
  - Move first: the contact-sheet engine of `D03 T18 §7` (the builder, layout, and caption model behind File, Automate, Contact Sheet) from `Photon.Imago.Core` to `src/Photon.Core/Print/ContactSheets/`, repointing Imago. Done when a grep finds one contact-sheet builder, under `src/Photon.Core/`, and Imago's contact-sheet golden still passes.
  - Layout (LP-0924): columns and rows, cell size and spacing, paper size, stretch small images, background color or image.
  - Appearance (LP-0922, LP-0923): frames, thumbnail effects (shadow, border), page background, presets.
  - Text: header, footer, and captions with `D04 T11 §2` tokens.
  - Output (LP-0922, LP-0925): image files with a name pattern and destination, PDF through the suite writer, HTML image maps (a page per sheet linking each cell to its image), print through §4, or show in the viewer; profiles saved; one sheet from selected thumbnails.
  - Tests: `ContactSheetLayoutTests` (a 4 by 5 sheet on A4 places 20 cells with the stated spacing), `ContactSheetHtmlMapTests` (the map's areas cover each cell and validate in the W3C Nu HTML Checker).
  - Fidelity: a contact sheet of the committed fixture folder matches its golden image within 1/255, and the PDF version reads back with PdfPig showing one image per cell.
  - Commit: `"lumen: contact sheets on the shared engine"`
- **Proof:** format fidelity proof plus unit: the golden comparison, the PdfPig read-back, and the HTML validator output are quoted; cheaper substitute that fails: a second contact-sheet builder in Lumen, which the move grep catches.

#### §7. Slideshow I: templates, layout, overlays, and titles

- **Deliverable:** A Slideshow module with a template browser, slide layout (zoom to fill, stroke border, cast shadow, margins, aspect preview), overlays (identity plate, watermark, rating stars, text with tokens and shadow), backdrop (color wash, image, color), intro and ending title screens, and header and footer captions.
- **Depends On:** D04 T11 §2
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/slideshow/. Job: a photographer designs a good-looking show from a collection without leaving Lumen. Treatment: Lightroom's Slideshow module (Template Browser and preview left, slide editor center, Options, Layout, Overlays, Backdrop, Titles, Playback panels right) with an on-slide text tool. Cheaper substitute that fails: a fixed black background with centered photos. Chrome: consume the develop pipeline for slide renders, the token engine, `D04 T11 §8` watermarks, the identity plate of `D04 T14 §1`, and the suite text engine (`D03 T16 §1`).
- **Runs:** `Requires: display-session -- the module and captures need an interactive desktop`
- **Catalog:** LP-0926 to LP-0932 (7 features)
- **Source:** `-> SOURCE: parity-lumen-slideshow-authoring`
- **Hints:**
  - `SlideshowDocument` in `Photon.Lumen.Core/Output/Slideshow/` (LP-0926): template, photo source, layout, overlays, backdrop, titles, and playback settings, saved as a slideshow collection.
  - Template browser (LP-0927): built-in and user templates as `.lumenslides` JSON, folders, preview on hover, save, import, export.
  - Layout and options (LP-0928): zoom to fill, stroke border with color and width, cast shadow with opacity, offset, radius, and angle, margins with linked guides, aspect preview for screen, 16:9, and 4:3.
  - Overlays (LP-0929, LP-0932): identity plate, watermark, rating stars, text overlays with shadow placed by the text tool with `D04 T11 §2` tokens, and header and footer captions with alignment, background, and font.
  - Backdrop (LP-0930): color wash with angle and opacity, background image, background color.
  - Titles (LP-0931): intro and ending screens with color and identity plate.
  - Tests: `SlideRenderTests` (a slide with border, shadow, and overlays matches its golden within 1/255), `SlideshowTemplateStoreTests`.
  - Commit: `"lumen: the slideshow module with templates, layout, overlays, and titles"`
- **Proof:** unit plus driven: the two test classes pass and captures of the editor are committed; cheaper substitute that fails: overlays drawn only in the preview, which the golden slide render catches.

#### §8. Slideshow II: playback, music, transitions, and export

- **Deliverable:** Slideshows play from the module, a selection, a folder, or a folder with subfolders (impromptu or configured), with manual or timed advance, fades, pan and zoom, 2-up, 4-up, and collage variations, transitions, display effects, music from tracks or folders fitted to the show, and export to PDF and JPEG slides; ACDSee-style slideshow projects save their content.
- **Depends On:** §7
- **Phase:** 38
- **Surface:** UI. Fidelity: docs/captures/lumen/slideshow/. Job: a photographer plays a show to music on any screen and hands it to others as a PDF or images. Treatment: Lightroom's Playback panel and Play button, ACDSee's Configure Slideshow dialog (basic, advanced, text, audio tabs), a full-screen player with autohiding controls, and Export PDF Slideshow and Export JPEG Slideshow. Cheaper substitute that fails: a timer that swaps photos with no transition or music. Chrome: consume §7's document, the develop pipeline, NAudio (MIT) over Media Foundation for audio, and the suite PDF writer; video export and video clips are backlog B-043, EXE and screen-saver output B-049.
- **Runs:** `Requires: display-session -- full-screen playback and audio need an interactive desktop`
- **Catalog:** LP-0301, LP-0933 to LP-0944 (13 features)
- **Source:** `-> SOURCE: parity-lumen-slideshow-playback`
- **Hints:**
  - Sources (LP-0301, LP-0933, LP-0937): impromptu slideshow of the selection (Ctrl+Enter), saved slideshow collections, all filmstrip, selected, or flagged photos, a folder or a folder with subfolders, remembered contents.
  - Player (LP-0935, LP-0941): `SlideshowPlayer` in `Photon.Lumen.Desktop/Views/Output/Slideshow/` rendering ahead on a background thread; manual or auto advance, slide and fade durations, fade color, random, repeat, screen choice, quality, preview in the module, autohide controls, stretch small images, background color.
  - Transitions (LP-0938): crossfade, slide, wipe, zoom, and random, previewed in the dialog; variations (LP-0939): pan and zoom with a strength, 2-up, 4-up, and collage; display effects (LP-0940): black and white, sepia, vivid, soft through the develop pipeline.
  - Music (LP-0934, LP-0942): NAudio (MIT, `docs/dev/decisions.md` row) plays MP3, AAC, and WAV from chosen tracks or folders, with fit slides to music (durations computed from track lengths) and fade out at the end.
  - Project content (LP-0944): per-image transitions, durations, captions, order, hidden controls, background audio, transition quality, and output size saved in the `SlideshowDocument`; save settings as default (LP-0943).
  - Export (LP-0936): PDF through the suite PDF writer with page transitions (`/Trans`, `/Dur`) and full screen, and JPEG slides at a chosen size with the overlays rendered.
  - Tests: `SlideshowTimingTests` (fit to music over two tracks sums to their length within one frame), `SlideshowPdfExportTests` (PdfPig reads the page count and `/Trans` entries), `SlideshowJpegExportTests` (slide count and pixel size).
  - Commit: `"lumen: slideshow playback, music, transitions, and PDF and JPEG export"`
- **Proof:** unit plus format fidelity proof: the three test classes pass with the PdfPig read-back quoted; a driven playback with music is captured with the log line; cheaper substitute that fails: exporting a PDF of plain pages, which the `/Trans` read-back catalogs as missing.

#### §9. Web galleries

- **Deliverable:** A Web module and the ACDSee HTML album and IrfanView HTML export paths build HTML galleries from own templates (grid, track, square, and album styles) with site info, colors, appearance, image info, output settings, and tokens, preview them in the browser, export them to a folder, and upload them to the user's own FTP or SFTP server; a plain FTP transfer of selected files uses the same client.
- **Depends On:** D04 T11 §2
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/web/. Job: a photographer publishes a gallery to their own site with no service account. Treatment: Lightroom's Web module (Layout Style, Site Info, Color Palette, Appearance, Image Info, Output Settings, Upload Settings) with a click-to-edit live preview, plus ACDSee's HTML Album wizard reachable from Create. Cheaper substitute that fails: a folder of JPEGs with an index listing file names. Chrome: consume the develop pipeline and export runner, the token engine, `D04 T11 §8` watermarks, the FluentFTP client moved from `D03 T17 §12`, and SSH.NET; online gallery services are excluded as cloud.
- **Runs:** `Requires: display-session -- the Web module, browser preview, and captures need an interactive desktop`
- **Catalog:** LP-0866, LP-0949 to LP-0957 (10 features)
- **Source:** `-> SOURCE: parity-lumen-web-galleries`
- **Hints:**
  - Move first: the FluentFTP (MIT) client wrapper of `D03 T17 §12` from Imago to `src/Photon.Core/Net/Ftp/`, repointing Imago's URL opener; add SSH.NET (MIT) for SFTP with a `docs/dev/decisions.md` row. Done when a grep finds one FTP wrapper, under `src/Photon.Core/`.
  - Templates (LP-0949, LP-0950): own HTML, CSS, and JavaScript templates in `src/Lumen/Photon.Lumen.Core/Output/Web/Templates/` (grid, track, square, album), shipped with an MIT license header inside every generated asset so a user's site carries no GPL obligation (recorded in `docs/dev/decisions.md`); user templates saved, updated, imported, and exported.
  - Site and look (LP-0951): site title, collection title and description, contact and link, color palette, cell sizes, rows and columns, borders, image info captions from tokens, click-to-edit text in the preview.
  - Output (LP-0952): JPEG quality, metadata choice, watermark, sharpening, and optional HDR AVIF images with JPEG fallbacks.
  - Preview and export (LP-0954): preview in the default browser from a temp folder, reload, export to a folder atomically (staging then rename), advanced settings, web collections, which photos.
  - ACDSee HTML album and IrfanView HTML export (LP-0955, LP-0956, LP-0957): the wizard maps onto the same templates; IrfanView's template placeholders (title, background, image and thumbnail links, previous, next, back, and self links, name parts, size, text, alignment, targets) are accepted through the token engine's `$` alias.
  - Upload (LP-0953, LP-0866): FTP, FTPS, and SFTP with server presets, remote subfolder, password stored with DPAPI, progress in the Activity Manager, and a plain transfer of selected files.
  - Tests: `WebGalleryGeneratorTests` (every generated page validates in the W3C Nu HTML Checker, version quoted, and every link resolves), `WebTemplateTokenTests` (IrfanView placeholders), `GalleryUploadTests` against a local test FTP server and an in-process SFTP stub.
  - Commit: `"lumen: web galleries from own templates with FTP and SFTP upload"`
- **Proof:** format fidelity proof plus unit: the HTML validator reports zero errors on each template's output and the link check passes; a driven export and upload to a local FTP server is captured; cheaper substitute that fails: an index page of file names, which the template tests catch.

#### §10. Books

- **Deliverable:** A Book module lays out photo books with auto layout presets, page templates, custom layouts, page numbers and captions, guides and cell zoom, photo and page text from metadata with type styles, backgrounds, and exports the book to PDF or JPEG pages with quality, profile, resolution, and sharpening, saved as a book collection.
- **Depends On:** §4
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/book/. Job: a photographer lays out a book of a trip and gets a print-ready PDF. Treatment: Lightroom's Book module (Book Settings, Auto Layout, Page, Guides, Cell, Text, Type, Background panels) with multi-page, spread, and single-page views; Blurb upload is excluded as cloud. Cheaper substitute that fails: one photo per page with no text. Chrome: consume §4's color path, the suite PDF writer (`D03 T17 §7`) with embedded fonts, the suite text engine (`D03 T16 §1`), and the develop pipeline.
- **Runs:** `Requires: display-session -- the Book module and captures need an interactive desktop`
- **Catalog:** LP-0958 to LP-0966 (9 features)
- **Source:** `-> SOURCE: parity-lumen-books`
- **Hints:**
  - `BookDocument` in `Photon.Lumen.Core/Output/Books/` (LP-0958): size, cover, pages with layouts and cells, text frames, backgrounds; saved as a book collection (LP-0966).
  - Book settings (LP-0959): PDF or JPEG output, page sizes (square, portrait, landscape), JPEG quality, color profile, resolution, sharpening, media type.
  - Auto layout (LP-0960) with presets (one photo per page, left blank right photo, with captions) and Clear Layout; page templates, add, remove, duplicate, custom layouts, copy and paste layout (LP-0961).
  - Page numbers and captions (LP-0962); guides, cells, padding, and photo zoom in cells (LP-0963).
  - Text (LP-0964): photo and page text from metadata tokens, type settings and style presets, targeted type adjustment, and caption refresh when metadata changes.
  - Backgrounds (LP-0965) per page or global: color, graphic, or photo with opacity.
  - Views (LP-0966): multi-page, spread, single page; export to PDF with fonts embedded and to JPEG pages; book preferences (default fill, text safe area).
  - Tests: `BookLayoutTests` (auto layout of 40 photos with a preset yields the expected page count), `BookPdfExportTests` (PdfPig reads page size, image placement within 0.5 mm, and embedded fonts), `BookCaptionRefreshTests`.
  - Commit: `"lumen: the book module with PDF and JPEG export"`
- **Proof:** format fidelity proof plus unit: the book PDF of the fixture reads back with PdfPig as stated and validates with qpdf `--check` (version quoted); cheaper substitute that fails: rasterizing text into page images, which the embedded-font check catches.

#### §11. PDF and PowerPoint creation

- **Deliverable:** A Create menu builds slideshow PDFs, one PDF for all images or one per image, multi-page TIFF or PDF from a selection, IrfanView's Save as PDF with document properties, compression, security, and paper fit, and PowerPoint presentations (new or appended) with slide duration, images per slide, linked images, a design template, captions, titles, and notes, without Office.
- **Depends On:** §4
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/create/. Job: a user hands a set of photos to someone as one PDF or a PowerPoint deck. Treatment: a Create menu (Slideshow, PDF, PowerPoint, Album, Archive; LP-0967) opening ACDSee-style wizards with a preview and an output page. Cheaper substitute that fails: a PDF with one uncompressed full-size image per page and no options. Chrome: consume the suite PDF writer and Imago's PDF presentation builder moved with it (`D03 T17 §7`, `D03 T18 §7`), DocumentFormat.OpenXml (MIT) for PPTX, the `D04 T13 §6` multi-page TIFF writer, and the token engine for captions.
- **Runs:** `Requires: display-session -- the wizards and captures need an interactive desktop`
- **Catalog:** LP-0967 to LP-0970, LP-0979 (5 features)
- **Source:** `-> SOURCE: parity-lumen-create-documents`
- **Hints:**
  - Create menu (LP-0967) with Slideshow (§8), PDF, PowerPoint, Album (§9), and Archive (`D04 T05 §12`) entries.
  - Create PDF (LP-0968): slideshow PDF with transitions and background, one PDF for all images, or one per image; order, names, location; if Imago's PDF presentation builder of `D03 T18 §7` is still in `Photon.Imago.Core`, move it to `src/Photon.Core/Pdf/Presentation/` first and repoint Imago.
  - Save as PDF (LP-0979): title, subject, author, keywords, per-color-type compression (JPEG, Flate, CCITT for 1-bit), security passwords and permissions through the suite writer's security, paper size and fit.
  - Multi-page TIFF or PDF from a selection (LP-0970).
  - Create PowerPoint (LP-0969): DocumentFormat.OpenXml (MIT, `docs/dev/decisions.md` row) writes a new PPTX or appends slides to an existing one, with images per slide, slide duration (advance after), linked or embedded images, a user-supplied design template `.potx`, captions, titles, and notes from tokens.
  - Tests: `CreatePdfTests` (PdfPig reads page count, metadata, and encryption permissions), `PptxWriterTests` (the Open XML SDK validator reports zero errors; slide count, notes text, and timing read back), `MultipageTiffTests`.
  - Fidelity: the PPTX of the fixture opens in LibreOffice Impress 25 headless (`soffice --convert-to pdf`) and the converted page count equals the slide count (version quoted).
  - Commit: `"lumen: create PDFs and PowerPoint presentations"`
- **Proof:** format fidelity proof: the Open XML validator, the LibreOffice conversion, and the PdfPig read-back are quoted; cheaper substitute that fails: a PPTX template zip with images swapped in, which the validator catches.

#### §12. Email and local sharing

- **Deliverable:** Photos go out by email through the default mail client (Simple MAPI) or an SMTP account, resized and converted to JPEG under a size limit, from export, browse, and the viewer, and to the user's own FTP server; photo-site uploads stay excluded.
- **Depends On:** §1
- **Phase:** 38
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/email/. Job: a user emails a few photos at a sensible size without leaving Lumen. Treatment: an Email Photos dialog (recipients with the address book of the mail client, size limit, convert to JPEG, send through mail client or SMTP) opened from Send, File, Email, the export destination Email, the viewer, and browse. Cheaper substitute that fails: attaching originals at full size. Chrome: consume §1's export runner for the attachments, Simple MAPI (`MAPISendMailW`, part of Windows), `System.Net.Mail.SmtpClient` for SMTP with the password stored through DPAPI, and the `Photon.Core/Net/Ftp/` client of §9.
- **Runs:** `Requires: display-session -- the mail client hand-off needs an interactive desktop`
- **Catalog:** LP-0867 to LP-0872, LP-0971 (7 features)
- **Source:** `-> SOURCE: parity-lumen-email-share`
- **Hints:**
  - `EmailService` in `Photon.Lumen.Core/Output/Share/` (LP-0867, LP-0869, LP-0971): render attachments through §1 to a temp folder (long edge and total size limit), then `MAPISendMailW` with the attachments, or SMTP with server, port, TLS, and account settings in `Lumen.Output.Email.*`.
  - No MAPI client: fall back to opening the temp folder and a `mailto:` link, saying why.
  - Send menu and email from browse and the viewer (LP-0868, LP-0872): selected files, the current photo; uploads to photo sites are excluded as cloud.
  - FTP to the user's own server (LP-0870, LP-0871): server, user, password, remote folder, progress, through §9's client.
  - Temp attachments are deleted after the mail client returns or after 24 hours.
  - Tests: `EmailAttachmentPlannerTests` (size limit met by downscaling), `MapiSenderTests` with a fake MAPI entry point, `SmtpSenderTests` against a local SMTP test server.
  - Commit: `"lumen: email through the mail client or SMTP, and FTP to the user's server"`
- **Proof:** unit plus driven: the three test classes pass; a driven send opens the default mail client with two attachments (capture); cheaper substitute that fails: attaching originals, which the size-limit test catches.

#### Sizing concerns

- §13 carries 18 features over presets, metadata, watermark, post-processing, and burning; if it passes 30 items, burning to disc and the export actions folder split into their own section with Phase 38's room.
- §5 carries 16 print features; document printing (LP-0948) is the natural split if needed.
- §9 bundles the FTP move with galleries; the move is one item and must stay first.

### todo/04-lumen/TODO-13-lumen-parity-formats.md -- `lumen-parity-formats`

- **Title:** "TODO-13 -- Lumen Parity: Formats"
- **Phase(s):** 30 (§1, §2, §3, §8, §4, §5), 31 (§6, §7)
- **Goal:** Lumen, the Lumen Viewer, and the batch tools read every image format Imago reads and every format IrfanView and ACDSee open that a GPL-3.0-compatible reader exists for, through one codec registry in `src/Photon.Core/Formats/` that Imago's readers and writers move into on this second consumer (never a copy); formats are detected by content, not extension; documents and multi-page files open as pages; RAW coverage is reported per camera with RAW+JPEG pairs handled as the user chooses; every writable format carries its per-format save options; and Lumen owns the suite's one DNG writer. Every reader and writer owes a format fidelity proof against a named reference, opening never changes a file, and writing always produces a new file through the atomic writer.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code and `Photon.Core` does not exist yet. `<!-- claim: absent src/Lumen -->` `<!-- claim: absent src/Photon.Core -->`
  - Imago's format project today holds only an interface, no codec and no registry; the `FormatRegistry` is planned by `D03 T17 §1` inside Imago's format project. `<!-- claim: exists src/Imago/src/Imago.FileFormats/IImageFormat.cs -->` `<!-- claim: count "FormatRegistry" src/Imago/src/**/*.cs = 0 -->` `<!-- claim: count "FormatRegistry" todo/03-imago/TODO-17-imago-parity-formats.md = 5 -->`
  - No archive or compression package is referenced by the solution yet. `<!-- claim: count "SharpCompress" Directory.Packages.props = 0 -->`
  - Lumen is declared but not shipping. `<!-- claim: count "Shipping  = \$false" scripts/apps.psd1 = 1 -->` `<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->`
- **Inputs and XREFs:** `standards/lumen.md` (original-file guard, decoder rules), `standards/shared.md`, `standards/testing.md`; `docs/parity/lumen-parity.md` (the rows each section owns); `docs/dev/decisions.md` (each dependency's GPL-3.0 row); the specifications each reader cites (TIFF 6.0, JFIF, PNG 1.2, GIF89a, Adobe DNG Specification 1.7.1.0, ITU T.81 process 14, ISO/IEC 15444-1, ISO/IEC 18181, SMPTE 268M, DICOM PS3.5); reference tools as oracles, versions recorded beside fixtures: libvips 8.16, ImageMagick 7.1, exiftool 13, Adobe `dng_validate` 1.7.1, darktable 5.0; -> XREF: D03 T17 §1 (the `FormatRegistry` §1 moves to `Photon.Core/Formats/`); -> XREF: D03 T17 §5 (modern web codecs §2 consumes after the move); -> XREF: D03 T17 §6 (HDR and scientific codecs §2 and §3 consume); -> XREF: D03 T17 §7 (PDFium, SVG, metafile, and Ghostscript runner §4 consumes); -> XREF: D03 T17 §8 and D03 T17 §9 (legacy raster codecs §3 and §8 consume); -> XREF: D03 T17 §11 (JPEG, PNG, and TIFF option sets §6 moves beside the writers); -> XREF: D03 T17 §2 and D03 T17 §3 (PSD composite read and flat write, §3); -> XREF: D03 T17 §4 (XCF flattened read, §3); -> XREF: D03 T12 §3 (ABR tip reader, §3); -> XREF: D04 T01 §4 (the RAW decoder §5 extends and §7 writes DNG from); -> XREF: D04 T04 §2 and D04 T04 §10 (the viewer decodes and pages through this registry); -> XREF: D04 T04 §3 (default-viewer registration lists every readable extension from §1); -> XREF: D04 T11 §4 (batch convert writes through §6); -> XREF: D04 T07 §6, D04 T06 §11, D04 T12 §2 (DNG conversion, smart previews, and DNG export consume §7); -> XREF: D04 T05 §12 (archives, which move SharpCompress with Imago's archive opener).
- **Adjacency:** list=applicable (the format matrix in §1 and the RAW coverage table in §5); document=applicable (every writer in §6 and §7 produces a user file); settings=applicable (enabled format handlers, per-format save option profiles, Ghostscript location, RAW+JPEG policy, all `Lumen.Formats.*` keys); reporting=applicable (the format matrix and the RAW coverage report); notifications=applicable (a wrong extension found on load and an unsupported camera are reported by name); permissions=applicable (unreadable, locked, or truncated files refused by name; Ghostscript absent refused by name); audit=applicable (one Serilog Information line per write and per extension fix); exchange=applicable (every format here is exchange); reverse=applicable (writes are new files; an extension fix is a rename with undo through `D04 T05 §6`)

#### §1. The shared codec registry in Photon.Core

- **Deliverable:** Imago's `FormatRegistry` and its readers move from `Photon.Imago.FileFormats` to `src/Photon.Core/Formats/` on their second consumer, gaining content sniffing, a screen-size decode capability, and a per-handler enable switch, so Lumen, the Lumen Viewer, the batch tools, and Imago all read through one registry; JPEG, PNG, TIFF, GIF, and BMP read and write with CMYK JPEG, high-bit and float TIFF, and alpha.
- **Depends On:** D04 T02 §8, D03 T17 §5, D03 T17 §6, D03 T17 §8, D03 T17 §9
- **Phase:** 30
- **Surface:** no surface of its own beyond the Formats page of Lumen's About and Preferences (format matrix and handler toggles), which reuses `Photon.UI` list styles.
- **Runs:** none
- **Catalog:** LP-0981 to LP-0984 (4 features)
- **Source:** `-> SOURCE: parity-lumen-codec-registry`
- **Hints:**
  - First item: move `FormatRegistry`, `IImageReader`, `IImageWriter`, and every reader registered by `D03 T17 §5`, `§6`, `§8`, `§9` from `src/Imago/Photon.Imago.FileFormats/` to `src/Photon.Core/Formats/` in one commit with `git mv`, repointing Imago's composition root; a grep proves no second copy (`FormatRegistry` defined once under `src/`).
  - Content sniffing (LP-0984, LP-0982): `FormatSniffer.Detect(Stream)` reads at most 64 KB of magic bytes per handler, ordered by specificity; header-less formats (raw pixels, some legacy) fall back to extension rules listed in the registry.
  - Wrong-extension handling (LP-0982, LP-0984): opening a PNG named `.jpg` decodes as PNG and offers "Fix extension" (a rename through `D04 T05 §6`, logged), never a rewrite; setting `Lumen.Formats.OfferExtensionFix` (default true).
  - Screen-size decode capability: `IImageReader.DecodeScaled(Stream, SizeInt target)` implemented by WIC JPEG DCT scaling, embedded previews, and codec resolution levels; the default falls back to full decode plus `D01 T03 §2` resampling.
  - Common formats (LP-0981): JPEG (WIC decode and libjpeg-turbo writer moved with `D03 T17 §11`), PNG, TIFF 8, 16, and 32-bit float with alpha, GIF first frame and frames for the viewer, BMP; CMYK JPEG converted through `D01 T04 §1` with the embedded profile.
  - Handler toggles (LP-0983): no plug-in package; every handler ships in the app and `Lumen.Formats.Disabled` lists handlers the user switched off, read by the viewer's association list and the open filters.
  - Format matrix: `FormatMatrix.Generate()` lists name, extensions, read, write, depths, alpha, layers-as-composite, multi-page, metadata carried; the Lumen About page and `docs/user/lumen/formats.md` are generated from it.
  - Fidelity: `FormatRegistryFidelityTests` (`[Trait("Category", "Fidelity")]`) decode `tests/fixtures/formats/common/` and compare with libvips 8.16 output within 0 for 8-bit lossless formats and 1/255 for JPEG decoded by the same IDCT; a truncated file returns a typed failure naming the file.
  - The unchanged-originals assertion over the whole fixture set: every read leaves SHA-256 and last-write time unchanged.
  - Commit: `"core: one codec registry in Photon.Core, read by Lumen and Imago"`
- **Proof:** unit plus fidelity: `FormatRegistryTests` (sniffing, extension fallback, handler toggle) and `FormatRegistryFidelityTests` pass with tolerances quoted; `grep -rn "class FormatRegistry" src` prints one path under `src/Photon.Core/Formats/`; cheaper substitute that fails: Lumen referencing `Photon.Imago.FileFormats`, which the `Photon.Lumen.*.csproj` grep for Imago references refuses.

#### §2. Modern and HDR formats in Lumen

- **Deliverable:** Lumen reads and writes WebP, AVIF, HEIF and HEIC, JPEG XL, JPEG 2000, and QOI, reads JPEG XR, and reads OpenEXR, Radiance HDR, FITS, DPX, and Cineon through the moved codecs, with HDR images tone-mapped for display and thumbnails.
- **Depends On:** §1
- **Phase:** 30
- **Surface:** no surface of its own (the formats appear in the viewer, browse, and batch through the registry)
- **Runs:** none
- **Catalog:** LP-0985 to LP-0991 (7 features)
- **Source:** `-> SOURCE: parity-lumen-modern-formats`
- **Hints:**
  - Register the moved `D03 T17 §5` codecs for Lumen: WebP with transparency (LP-0989, libwebp BSD-3-Clause), AVIF and HEIF including HIF and HEIC with animated AVIF shown as the first frame and sidecar XMP read (LP-0985, libavif BSD-2-Clause, libheif LGPL-3.0), JPEG XL (LP-0988, libjxl BSD-3-Clause), JPEG 2000 JP2, JPC, J2K with 48-bit color (LP-0987, OpenJPEG BSD-2-Clause), QOI (LP-0990, own code).
  - JPEG XR, HD Photo HDP, JXR, WDP read (LP-0991) through jxrlib (BSD-2-Clause) as moved by `D03 T17 §5`.
  - HDR and scientific (LP-0986): OpenEXR and Radiance HDR from `D03 T17 §6`; FITS from the same section; DPX and Cineon through an own reader from SMPTE 268M in `src/Photon.Core/Formats/Dpx/`, 10-bit log decoded to linear.
  - Display: HDR sources get the suite tone map (`D03 T15 §3`'s operator where moved, otherwise a Reinhard fallback recorded as a default) for thumbnails and the viewer; exports keep float data.
  - Screen-size decode for AVIF and JPEG XL (progressive and downsampled decode where the codec offers it) registered as the §1 capability.
  - Native payloads per RID recorded in `docs/dev/decisions.md` with their licenses; Lumen's installer carries them, checked by the package script's file list.
  - Fidelity: `ModernFormatFidelityTests` read and write each fixture in `tests/fixtures/formats/modern/` and compare with libvips 8.16 (lossless within 0, lossy within the stated PSNR floor); DPX golden from ImageMagick 7.1.
  - Commit: `"lumen: modern and HDR formats through the shared registry"`
- **Proof:** format fidelity: `ModernFormatFidelityTests` print a result per format and direction with its tolerance; cheaper substitute that fails: WIC codecs from the Store, which the clean-machine run in the release lacks.

#### §3. Common legacy and special raster formats

- **Deliverable:** Lumen reads the common legacy and special raster formats (ICO, CUR, ANI, PCX and DCX, TGA, WBMP, PSD and PSB composite, XCF flattened, DICOM, PSP, SFW, PDN, DDS and game textures, EXE and DLL icons, XBM, XPM, PNM) and writes those that have writers, and browses ABR brush files as images.
- **Depends On:** §1
- **Phase:** 30
- **Surface:** no surface of its own
- **Runs:** none
- **Catalog:** LP-0992 to LP-1003 (12 features)
- **Source:** `-> SOURCE: parity-lumen-legacy-formats`
- **Hints:**
  - Register the moved `D03 T17 §8` codecs: ICO with every resolution as a page, CUR, animated ANI (LP-0993); PCX and multi-page DCX read and write (LP-0994); TGA read and write (LP-0996); WBMP read and write (LP-0997); XBM, XPM, PBM, PGM, PPM read (LP-1003).
  - PSD and PSB composite read and flattened PSD write (LP-0995) through the `D03 T17 §2` and `§3` code moved to `Photon.Core/Formats/Psd/`; layered editing is Imago's, and the viewer says so on a layered file.
  - GIMP XCF flattened read (LP-1000) through `D03 T17 §4`'s reader moved to `Photon.Core/Formats/Xcf/`.
  - DICOM DCM, ACR, IMA (LP-0998) through `D03 T17 §6`'s own reader (fo-dicom is MS-PL and stays out).
  - Paint Shop Pro PSP and Seattle FilmWorks SFW from `D03 T17 §9`; Paint.NET PDN through an own reader of its documented container (LP-0999).
  - Game and texture formats (LP-1001): DDS through BCnEncoder.Net (MIT) and PVR from `D03 T17 §8` and `§9`; WAD3, Quake WAL, and Blizzard BLP through own readers from their published descriptions.
  - Icons from EXE, DLL, and ICL (LP-1002) through `LoadLibraryEx` with `LOAD_LIBRARY_AS_DATAFILE` and resource enumeration, each icon a page; no code in the file is executed.
  - ABR brush files browsed as images (LP-0992) through the ABR tip reader of `D03 T12 §3` moved to `Photon.Core/Formats/Abr/`, each tip a page.
  - Fidelity: `LegacyFormatFidelityTests` over `tests/fixtures/formats/legacy/` against ImageMagick 7.1 and GIMP 3.2 exports (lossless within 0), writers round-tripped read, write, reread.
  - Commit: `"lumen: common legacy and special raster formats"`
- **Proof:** format fidelity: `LegacyFormatFidelityTests` list every format with read and write results; cheaper substitute that fails: a thumbnail-only reader, which the pixel comparison catches.

#### §8. Rare and historical raster formats

- **Deliverable:** Lumen reads the long tail IrfanView's Formats plug-in carries (Amiga, Atari, C64, ZX Spectrum, GEM IMG, IFF and LBM, Sun raster, SGI, fax formats, Kodak Photo CD, PICT, FLIF, WBZ and WBC, WSQ, MNG, JNG, FLI and FLC, TIFF annotations, font files as sample sheets), opens any file as raw pixels or YUV with a header dialog, reads and writes JPEG-LS, and shows the embedded thumbnails of Affinity and Canvas documents.
- **Depends On:** §3
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/raw-open/ and docs/captures/lumen/photo-cd/. Job: a user can see any old image they own and pull pixels out of an undocumented dump. Treatment: IrfanView's Open as RAW dialog (width, height, header bytes, bits per pixel, color order, planar or interleaved, vertical flip, saved presets) and a Photo CD resolution choice (Base/16 to 16BASE). Chrome: consume `Photon.UI` dialog styles and the settings store. Cheaper substitute that fails: a guessed raw size with no dialog.
- **Runs:** `Requires: display-session -- the raw-open dialog and its captures need an interactive desktop`
- **Catalog:** LP-1030 to LP-1042 (13 features)
- **Source:** `-> SOURCE: parity-lumen-rare-formats`
- **Hints:**
  - `src/Photon.Core/Formats/Rare/` managed readers from published descriptions (LP-1031): Amiga IFF and LBM, Atari (Degas, NEO), C64 (Koala, Art Studio), ZX Spectrum SCR, GEM IMG, SIF, G3 fax and Structured Fax, Casio CAM; SGI and Sun raster consume the `D03 T17 §8` readers.
  - Kodak Photo CD read up to 16BASE with Huffman residuals (LP-1032) and the load-resolution choice `Lumen.Formats.PhotoCd.Resolution` (LP-1037).
  - Macintosh PICT bitmap opcodes and QuickTime-wrapped still images through an own reader (LP-1033), no QuickTime dependency; vector opcodes rasterized where documented, the rest reported.
  - Raw pixel open (LP-1034) and raw binary and YUV read and write (LP-1036) consume `D03 T17 §6`'s raw data codec; the dialog stores named presets in `Lumen.Formats.RawPresets`.
  - JPEG-LS lossless and near-lossless read and write (LP-1035) through CharLS (BSD-3-Clause), native per RID.
  - FLIF, Webshots WBZ and WBC, and WSQ (LP-1040), WSQ from NIST NBIS (public domain); MNG, JNG, FLI, and FLC read as frame sequences played by `D04 T04 §10` (LP-1041), authoring stays B-044.
  - TIFF annotation tags drawn as an overlay layer in the viewer, never merged into pixels (LP-1038).
  - Font files (TTF, OTF, FON) shown as a sample sheet with custom text `Lumen.Formats.FontSample` (LP-1039, LP-1042) through `Photon.Core/Text/` (moved from Nodus by `D03 T16 §1`); the two catalog rows are one feature and are built once.
  - Affinity and Canvas embedded thumbnails read from the container without parsing documents (LP-1030); opening them remains Imago B-045.
  - Fidelity: `RareFormatFidelityTests` over `tests/fixtures/formats/rare/` (public-domain samples with sources in the README) against ImageMagick 7.1 or the format's reference viewer output, versions recorded; JPEG-LS round trip against CharLS's own tool.
  - Commit: `"lumen: rare and historical raster formats, raw pixel open, JPEG-LS"`
- **Proof:** format fidelity plus driven: `RareFormatFidelityTests` pass per format with tolerances; a driven raw open of a 16-bit planar dump is captured; cheaper substitute that fails: listing extensions without readers, which the fixture loop catches.

#### §4. Documents and multi-page formats

- **Deliverable:** Lumen opens PDF, XPS, SVG, EMF, WMF, WPG, DjVu, PostScript, EPS, and text files as page images, navigates every multi-page container (TIFF, DCX, ICO, PDF, DjVu, MPO), extracts pages, and builds or edits multi-page TIFF and PDF files as new files.
- **Depends On:** §1, D03 T17 §7
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/documents/ and docs/captures/lumen/multipage-editor/. Job: a user browses and rates PDFs and scans beside photos and assembles a multi-page file without another tool. Treatment: a per-type choice to open documents in the viewer or their own application; IrfanView's multipage editor (add files or a list, arrange, delete, append the current image, save as TIFF or PDF) and Extract Pages dialog (range, format, name suffix). Chrome: consume the registry, the viewer's page navigation (`D04 T04 §10`), and `Photon.UI` dialogs. Cheaper substitute that fails: opening PDFs in the default reader only.
- **Runs:** `Requires: display-session -- the multipage editor and document viewing need an interactive desktop`
- **Catalog:** LP-1004 to LP-1014 (11 features)
- **Source:** `-> SOURCE: parity-lumen-documents`
- **Hints:**
  - Move `D03 T17 §7`'s PDFium reader (BSD-3-Clause and Apache-2.0) and its SVG and metafile readers to `src/Photon.Core/Formats/Pdf/` and `Formats/Vector/`; PDF pages rasterize at `Lumen.Formats.Pdf.RenderDpi` (LP-1005, LP-1010).
  - PDF viewing (LP-1005): page back and forward, zoom, fit page and width, page number and magnification readouts, next file, open in the default app, print; XPS through WPF `DocumentViewer` rendered to pixels (LP-1004); rating, label, and tag apply to documents like photos; Office documents stay `other-app: none`.
  - Vector and metafile images as pixels (LP-1006): SVG, EMF, WMF from `D03 T17 §7`, WordPerfect WPG through an own reader of its bitmap and vector records.
  - PostScript, EPS, PS, and AI (LP-1012) through the Ghostscript runner Imago moved to `Photon.Core/Formats/PostScript/`: user-installed, matching bitness, located by `Lumen.Formats.Ghostscript.Path`, refused by name when absent; Ghostscript (AGPL-3.0) is never bundled; antialiasing and render size settings (LP-1010).
  - DjVu read with pages (LP-1011) through DjVuLibre `libdjvulibre` (GPL-2.0-or-later) via P/Invoke, native per RID, decision row recorded.
  - Text files rendered as images with a font and colors `Lumen.Formats.Text.*` (LP-1007, LP-1013; one feature built once).
  - Multi-page model (LP-1014): `IPagedImage` for TIFF, DCX, ICO, PDF, DjVu, and MPO (MPO second images as pages), consumed by `D04 T04 §10`.
  - Multipage editor (LP-1008): builds a new TIFF or PDF from files or a list, writes through the atomic writer to a new path, never over a source; PDF writing through the suite PDF writer in `Photon.Core/Pdf/`.
  - Extract pages (LP-1009): range, target format from §6, name suffix `_p{page}` through the token engine when present, each page a new file.
  - Fidelity: `DocumentFormatFidelityTests` render fixture pages and compare with `pdftoppm` 24 (PDF), Ghostscript 10 (PS), `ddjvu` 3.5 (DjVu) within 2/255 mean; multipage round trip rereads page count and pixels.
  - Commit: `"lumen: documents and multi-page formats"`
- **Proof:** format fidelity plus driven: fidelity tests pass per format; a driven multipage build is reread with its page count quoted and captured; cheaper substitute that fails: first page only, which the page-count assertion catches.

#### §5. RAW coverage and RAW+JPEG pairs

- **Deliverable:** RAW+JPEG pairs are handled as one photo with the JPEG as a sidecar or as two photos by setting, the RAW coverage table lists every supported maker and model with its decoder version and a path to request a camera, and JPEG XL compressed DNG decodes where the decoder supports it.
- **Depends On:** §1, D04 T01 §4
- **Phase:** 30
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/raw-coverage/. Job: a photographer knows before buying or importing whether Lumen reads their camera, and shoots RAW+JPEG without doubled thumbnails. Treatment: Help, Supported Cameras (searchable maker and model table with decoder version and a "request a camera" link to the decoder's upstream tracker) and a Preferences choice "Treat JPEG next to RAW as: sidecar, separate photo". Chrome: consume `D04 T01 §4`'s decoder and `Photon.UI` list styles. Cheaper substitute that fails: a static camera list copied into docs.
- **Runs:** `Requires: display-session -- the coverage dialog capture needs an interactive desktop`
- **Catalog:** LP-1015 to LP-1017 (3 features)
- **Source:** `-> SOURCE: parity-lumen-raw-coverage`
- **Hints:**
  - `RawPairPolicy` in `Photon.Lumen.Core/Raw/` (LP-1015): `Lumen.Import.RawJpegPairs` = `Sidecar` (default) or `Separate`; paired files share one catalog record with a pair badge, and file operations move both (`D04 T05 §6`).
  - Coverage table (LP-1017): generated at build time from the decoder's camera list (LibRaw's `libraw_cameraList` when `D04 T01 §3` chose LibRaw), stored as `Photon.Lumen.Core/Raw/cameras.json`, shown in Help and `docs/user/lumen/cameras.md`; the pinned corpus result from `D04 T01 §4` marks tested models.
  - Unsupported model message names the decoder version and links to the request page; decoder updates arrive with Lumen releases, stated in the dialog.
  - JPEG XL compressed DNG (LP-1016): enabled when the decoder release reports support, otherwise a typed failure naming the missing support; the coverage table has a column for it.
  - Pair detection by base name and capture time within 2 seconds, case-insensitive extensions, tested on mixed folders.
  - Fidelity: the committed DNG plus a RAW+JPEG fixture pair decode through the pair policy and match `D04 T01 §4`'s golden.
  - Commit: `"lumen: RAW coverage table and RAW+JPEG pairs"`
- **Proof:** unit plus driven: `RawPairPolicyTests` cover both policies and a move of a pair; the coverage dialog is captured with the decoder version quoted; cheaper substitute that fails: treating pairs as duplicates, which the pair test catches.

#### §6. Write formats and per-format save options

- **Deliverable:** Every writable format carries its option set (JPEG quality, progressive, Huffman optimization, subsampling, metadata carry-over, size targeting; GIF, PNG, TIFF, PNM, ICO, TGA, BMP, JPEG 2000, WebP, JPEG XL options), shown automatically on Save As, stored as named profiles, and shared by export, convert, the viewer's Save As, and the batch tools, with a restriction list of formats offered in save dialogs.
- **Depends On:** §1, D03 T17 §11
- **Phase:** 31
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/save-options/. Job: a user saves exactly the file they need (a size-capped JPEG, a lossless WebP, a 1-bit TIFF) and reuses the settings. Treatment: IrfanView's per-format Save options panel beside the Save As dialog, opened automatically for formats with options, with named profiles and a JPEG preview dialog (estimated quality, target size, live size readout). Chrome: consume `D03 T17 §11`'s option records moved to `Photon.Core/Formats/Options/`, the settings store, and `Photon.UI` dialog styles. Cheaper substitute that fails: fixed defaults per format.
- **Runs:** `Requires: display-session -- the save options panel and JPEG preview need an interactive desktop`
- **Catalog:** LP-1018 to LP-1028 (11 features)
- **Source:** `-> SOURCE: parity-lumen-save-options`
- **Hints:**
  - First item: move the writers and option records of `D03 T17 §5`, `§8`, `§11` to `src/Photon.Core/Formats/` (writers) and `Formats/Options/` (records); Imago's save dialog repoints; no copy.
  - JPEG (LP-1018): quality, progressive, optimized Huffman, subsampling 4:4:4, 4:2:2, 4:2:0, grayscale, saved defaults and named profiles `Lumen.Formats.Jpeg.Profiles`.
  - JPEG metadata carry-over (LP-1019): keep EXIF, IPTC, XMP, comment; reset orientation after a pixel rotation; embedded and DCF thumbnail policy; applies to new files only.
  - Size targeting (LP-1021): estimate the source's quality from its quantization tables, binary-search quality to a target size, and a preview dialog with the live size.
  - Options on Save As (LP-1020): `SaveOptionsPanel` opens automatically when the chosen format has options, `Lumen.Formats.ShowOptionsOnSave`.
  - GIF (LP-1022): interlace, automatic or custom transparent color, palette index, single frame only (animation authoring is B-044); PNG (LP-1023): compression level, transparency color, synthetic alpha, optimize pass (own zlib pass, with oxipng (MIT) as an optional external tool if installed).
  - Legacy (LP-1024): PNM binary or ASCII, ICO transparency, TGA and BMP RLE; TIFF (LP-1025): compression per color and 1-bit, grayscale palette, save all pages.
  - JPEG 2000 (LP-1026): quality, target bytes, lossless through OpenJPEG (BSD-2-Clause); WebP and JPEG XL (LP-1027): quality, lossless, effort, keep metadata.
  - Restrict formats in save dialogs (LP-1028): `Lumen.Formats.SaveList`.
  - Every writer writes through `AtomicFileWriter` to a new path; a path equal to an original's is refused by name (the original-file guard).
  - Fidelity: `WriterOptionFidelityTests` write each option combination and reread with libvips 8.16 and exiftool 13 (subsampling, progressive flag, metadata presence, target size within 5 percent).
  - Commit: `"lumen: per-format save options shared by export, convert, and Save As"`
- **Proof:** format fidelity: `WriterOptionFidelityTests` quote each option's reread result; the guard test refusing a write over an original passes; cheaper substitute that fails: options only on export, which the Save As test catches.

#### §7. The DNG writer

- **Deliverable:** `Photon.Lumen.Core/Dng/` writes DNG 1.7 files (linear or mosaic raw data with lossless JPEG, lossy DNG for smart previews, optional embedded original raw, fast-load data, and a JPEG preview) consumed by Convert to DNG, render to DNG, and smart previews, and writes GoPro GPR through the GPR SDK.
- **Depends On:** §5
- **Phase:** 31
- **Surface:** no surface of its own (the conversion dialogs are `D04 T07 §6` and `D04 T12 §2`)
- **Runs:** none
- **Catalog:** LP-1029 (1 feature)
- **Source:** `-> SOURCE: parity-lumen-dng-writer`
- **Hints:**
  - `DngWriter` from the Adobe DNG Specification 1.7.1.0: IFD0 with the preview, raw IFD with CFA pattern or linear raw, `ColorMatrix1/2`, `AsShotNeutral`, `DefaultCrop`, `BaselineExposure`, opcode lists copied from the decoder where present.
  - Own lossless JPEG encoder (ITU T.81 process 14, predictor 1) tiled 256 by 256; lossy DNG as baseline JPEG tiles for smart previews (2,560 px long edge); JPEG XL compression behind a setting when libjxl is present.
  - Options record `DngWriteOptions`: compatibility level, preview size (none, medium, full), embed fast-load data, lossy, embed original raw file (as `OriginalRawFileData`).
  - Metadata: EXIF, XMP including develop settings through `D01 T07 §6`, never altering the source file.
  - GoPro GPR write (LP-1029) through the gpr SDK (Apache-2.0 or MIT) as DNG with VC-5, behind the same writer interface.
  - Output always a new file through the atomic writer; the source is opened read-only and its hash asserted unchanged.
  - Fidelity: `DngWriterFidelityTests` write the committed DNG fixture and a corpus subset, validate with Adobe `dng_validate` 1.7.1 (zero errors), reread through `D04 T01 §4` and compare the raw data bit-exactly (lossless) or within 2/255 after develop (lossy).
  - Commit: `"lumen: a DNG writer validated against dng_validate"`
- **Proof:** format fidelity: `dng_validate` output quoted with zero errors and the bit-exact reread passes; cheaper substitute that fails: wrapping a JPEG in a TIFF container, which `dng_validate` rejects.

#### Sizing concerns

- §3 and §8 each register a dozen formats; each format is a small reader but owes a fixture, so the checklists run near 25 items; the natural split if either passes 30 is by origin (moved Imago codecs versus own readers).
- §4 carries PDFium, DjVuLibre, Ghostscript, the multipage editor, and page extraction; split at authoring into "documents as pages" and "the multipage editor" if the editor's items overflow.
- LP-1007 and LP-1013 (text files as images) and LP-1039 and LP-1042 (font sample rendering) are duplicate catalog rows for one capability each; the hints build each once.

### todo/04-lumen/TODO-14-lumen-parity-workspace.md -- `lumen-parity-workspace`

- **Title:** "TODO-14 -- Lumen Parity: Workspace, Preferences, and Help"
- **Phase(s):** 39
- **Goal:** Lumen's workspace reaches Lightroom Classic, ACDSee, and IrfanView parity once every parity surface exists: modes and the module picker with the identity plate, panel groups, screen modes, and lights out; customizable toolbars, menus, favorite menus, dockable panes, saved workspaces, and touch input; one default keymap with the shortcut editor and overlay; preference pages for general behavior, interface, file handling, the viewer and browse, performance, caches, color management, and display; settings storage with portable mode, administrator deployment, and migration from earlier installations; help, languages, and updates; themes and appearance; and external editors beyond Edit in Imago. The code lives in `src/Lumen/Photon.Lumen.Desktop/Workspace/`, `Preferences/`, and `Help/`, and `Photon.Lumen.Core/Settings/`; it consumes the workspace, toolbar, menu, and shortcut-set frames Imago moved to `src/Photon.UI/Workspace/` (`D03 T20 §1` to `§3`), the preference and warning registries and system-info report moved by `D03 T20`, the settings store (`D01 T02 §2`), the theme (`D01 T01 §3`), and the update check (`D05 T01 §4`), never a second copy. The relocated accessibility and localization audit (`D04 T02 §9`) runs after this file, last before Lumen 1.0.0.
- **Current-state facts to verify (with claim candidates):**
  - Lumen has no code and no settings of its own yet. `<!-- claim: absent src/Lumen -->`
  - The shared workspace frames do not exist yet: `Photon.UI` is absent, and Imago's workspace file moves them from Nodus. `<!-- claim: absent src/Photon.UI -->` `<!-- claim: exists todo/03-imago/TODO-20-imago-parity-workspace.md -->`
  - The Lumen installer is guarded and registers no file type or setting. `<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->` `<!-- claim: count "\[Registry\]" installer/Lumen.iss = 0 -->`
  - The suite update check is planned in the release file. `<!-- claim: count "^## 4\. The Update Check" todo/05-release/TODO-01-release-pipeline.md = 1 -->`
  - `scripts/apps.psd1` still names the legacy Lumen project path. `<!-- claim: count "src/Lumen/Lumen.UI/Lumen.UI.csproj" scripts/apps.psd1 = 1 -->`
- **Inputs and XREFs:** `standards/shared.md` (window anatomy, theme resources, settings store, one log line per settings change), `standards/lumen.md`; Lightroom Classic 15.5.1 workspace, preferences, and keyboard shortcut pages; ACDSee Ultimate 2027 Options dialog and Keyboard Shortcuts chapters; IrfanView 4.76 Properties dialog, INI, and Options menu help; -> XREF: D03 T20 §1 (the `Photon.UI/Workspace/` frame, panes, and saved workspaces §1 and §2 consume); -> XREF: D03 T20 §2 (toolbar customization frame §2 consumes); -> XREF: D03 T20 §3 (menus, shortcut sets, and command search §3 consumes); -> XREF: D03 T20 §4 (the `PreferenceKeyRegistry` and `WarningRegistry` §4 consumes); -> XREF: D03 T20 §6 (touch and pen input handling §2 reuses); -> XREF: D03 T20 §8 (`SystemInfoReport` and help plumbing §7 consumes); -> XREF: D03 T20 §9 (interface appearance and language switching §7 and §8 follow); -> XREF: D01 T02 §2 (the settings store §6 extends with portable and deployment modes); -> XREF: D01 T01 §3 (the suite theme §8 consumes); -> XREF: D01 T04 §1 (display color management §5 configures); -> XREF: D05 T01 §4 (the update check §7 consumes); -> XREF: D05 T01 §1 and D05 T01 §3 (installer switches, portable ZIP, and arm64 builds §6 and §7 document); -> XREF: D02 T15 §11 (`SuiteAppLocator` §9 consumes); -> XREF: D04 T02 §7 (Edit in Imago, which §9 extends to other editors); -> XREF: D04 T02 §9 (the audit that runs after this file); -> XREF: D04 T01 §2 (the shell, splash, and About §1 and §7 extend); -> XREF: D06 T01 §3 (the Lumen user guide §7 links); -> XREF: D04 T15 §10 (Lumen 1.0.0).
- **Adjacency:** list=applicable (workspaces, toolbars, favorite menus, shortcut sets, external editors, and language packs are managed lists); document=not-applicable (no document of its own); settings=applicable (this file is the settings surface; every page writes `Lumen.*` keys with defaults and a named consumer); reporting=applicable (system info and the installed codecs list); notifications=applicable (update available, settings imported, reset done); permissions=applicable (a read-only portable folder, a locked deployment key, and a missing editor are refused by name); audit=applicable (one Serilog Information line per settings change); exchange=applicable (workspace, keymap, and settings export and import; migration from earlier installations); reverse=applicable (reset to defaults per page and at launch; import is undoable by restoring the backup it takes)

#### §1. Modes, the module picker, and panels

- **Deliverable:** Lumen's modes (Library, Browse, Develop, Map, Book, Slideshow, Print, Web, People, Dashboard, and the viewer) sit in a customizable module picker with an identity plate, per-module key switching and history, panel groups with solo mode, auto hide, and swap, screen modes, and lights out; ACDSee's modes map onto them.
- **Depends On:** D04 T02 §8
- **Phase:** 39
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/ (baseline from `D04 T01 §2`), new captures to docs/captures/lumen/workspace/. Job: a photographer moves between tasks by key and hides everything but the photo when judging it. Treatment: Lightroom's module picker with an Identity Plate Editor, modules hidden by right-click, F5 to F8 panel toggles, Tab and Shift+Tab, solo mode, end marks, auto hide and show, F full-screen cycling, and L lights out with dim level and color. Cheaper substitute that fails: fixed tabs with no panel control. Chrome: consume the `Photon.UI/Workspace/` frame (`D03 T20 §1`) and the theme; do not add a second panel host.
- **Runs:** `Requires: display-session -- the workspace needs an interactive desktop`
- **Catalog:** LP-1059 to LP-1065 (7 features)
- **Source:** `-> SOURCE: parity-lumen-modes`
- **Hints:**
  - Module picker (LP-1059): show or hide the picker and individual modules, button style, condensed buttons, icons; state in `Lumen.Workspace.Modules`.
  - Identity plate (LP-1060): styled text or a graphic, editor with fonts and colors for the picker, presets, reused by print, slideshow, and web overlays (`D04 T12 §5`, `§7`, `§9`).
  - Panel groups (LP-1061): left, right, top, and bottom groups with show or hide, solo mode, end marks, auto hide and show, hide individual panels, swap left and right.
  - Screen modes (LP-1062): normal, full screen with menu bar, full screen, hide panels, full-screen preview; lights out (LP-1063) with dim level and color.
  - Module switching (LP-1064): Ctrl+Alt+1 to 7 per module, back and forward through module history, return to the previous module.
  - ACDSee mapping (LP-1065): Manage maps to Browse, View and Media to the viewer and library, Develop, and Dashboard; a mode switcher lists them with their ACDSee names as tooltips.
  - Tests: `ModuleNavigatorTests` (history, hidden modules skipped), `PanelLayoutStateTests` (solo mode and swap persist across restart).
  - Commit: `"lumen: modes, the module picker, identity plate, panels, and screen modes"`
- **Proof:** unit plus driven: the two test classes pass and captures of each screen mode and lights out are committed; cheaper substitute that fails: panels that forget their state, which the persistence test catches.

#### §2. Toolbars, menus, pane layout, saved workspaces, and touch

- **Deliverable:** Toolbars and menus are customizable per module (buttons, labels, tooltips with shortcuts, custom menus, up to 15 favorite commands, a task pane), panes dock, float to a second monitor, stack as tabs, and auto hide, workspaces save, load, and reset per mode, dialogs and the browser window remember size and position, text fields edit with spelling check, and the viewer answers touch and tablet mode.
- **Depends On:** §1
- **Phase:** 39
- **Surface:** UI. Fidelity: docs/captures/lumen/workspace/. Job: a user arranges Lumen for their screens and hands and gets it back next time. Treatment: a Customize Toolbar dialog, a Favorites menu, Window, Workspaces and Panes menus, a docking compass, and a Tablet Mode dialog. Cheaper substitute that fails: saving only window size. Chrome: consume the `Photon.UI/Workspace/` toolbar, menu, and docking frames (`D03 T20 §1`, `§2`) and Imago's touch handling (`D03 T20 §6`); do not add a second layout serializer.
- **Runs:** `Requires: display-session -- docking, a second monitor, and touch need an interactive desktop`
- **Catalog:** LP-1066 to LP-1079 (14 features)
- **Source:** `-> SOURCE: parity-lumen-workspace-layout`
- **Hints:**
  - Toolbars (LP-1066, LP-1079): per-module items, show or hide, the customize dialog, add or remove buttons, text labels, tooltips with shortcuts, reset, position, and the zoom box on the toolbar.
  - Menus (LP-1073, LP-1077): custom menus and button appearance; Favorites with up to 15 commands, add from any menu by right-click, remove, clear.
  - Task pane (LP-1072): context-sensitive common tasks for the current mode and selection.
  - Panes (LP-1068, LP-1069): Window, Panes menu to open or close any pane; docking compass, float to a second monitor, stack as tabs, resize, auto hide, return to the previous location.
  - Workspaces (LP-1070): save, load, default, reset per mode, stored as the shared frame's package with the `.lumenws` extension.
  - Window memory (LP-1076, LP-1078): dialogs and the browser window remember size and position per monitor configuration.
  - Text fields (LP-1067): cut, copy, paste, WPF spell check with the Windows spelling languages, and a special characters flyout; color controls copy and paste values through the clipboard (LP-1075).
  - Touch (LP-1071, LP-1074): swipe, hold and swipe, press and hold, double tap to switch mode, pinch zoom and pan in the viewer and loupe, and a Tablet Mode dialog enlarging touch targets.
  - Tests: `ToolbarCustomizationTests`, `FavoritesMenuTests` (limit of 15), `LumenWorkspaceRoundTripTests` (a saved `.lumenws` restores dock layout, toolbars, and menus), `TouchGestureMapTests` (manipulation deltas map to zoom and pan).
  - Commit: `"lumen: customizable toolbars and menus, docking, saved workspaces, and touch"`
- **Proof:** unit plus driven: the four test classes pass; a driven float of a pane to a second monitor and back is captured; cheaper substitute that fails: fixed toolbars, which the customization test catches.

#### §3. The keymap and shortcuts

- **Deliverable:** One default Lumen keymap covers every command with Lightroom's keys as the base and alternative key sets that follow ACDSee and IrfanView, a shortcut editor per mode with conflict warnings and right-click reassignment from menus, the Ctrl+/ overlay per module, library navigation and application keys, focus and context-menu keys, and the Lumen keys kept around the Edit in Imago hand-off.
- **Depends On:** §2
- **Phase:** 39
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/keymap/. Job: a user coming from Lightroom, ACDSee, or IrfanView keeps their muscle memory and can change any key. Treatment: Edit, Keyboard Shortcuts with mode categories, commands, current keys, assign with conflict warning, remove, reset all, and a key-set picker (Lumen, ACDSee keys, IrfanView keys); the Ctrl+/ overlay lists the current module's keys. Cheaper substitute that fails: a read-only shortcut list. Chrome: consume the shortcut-set frame moved to `Photon.UI/Workspace/` by `D03 T20 §3` and the About and shortcuts dialog of `D01 T01 §4`.
- **Runs:** `Requires: display-session -- the editor and overlay need an interactive desktop`
- **Catalog:** LP-1125 to LP-1129, LP-1216 to LP-1217 (7 features)
- **Source:** `-> SOURCE: parity-lumen-keymap`
- **Hints:**
  - `LumenKeymap` in `Photon.Lumen.Desktop/Workspace/Keymap/`: a default set generated from every command's registered default key (each parity section registered its keys), with a test that no two commands in one scope share a key.
  - Alternative key sets `ACDSee keys` and `IrfanView keys` shipped as shortcut-set files, chosen in the editor; unmapped commands fall back to the default set.
  - Shortcut editor (LP-1127): per-mode categories, commands, current keys, assign with conflict warning, remove, reset all, and change a menu item's key by right-click on it.
  - Overlay (LP-1125): Ctrl+/ shows the current module's keys, dismissed by any key.
  - Library navigation keys (LP-1126), application close keys (LP-1128), focus and context-menu keys (LP-1129: Tab and Shift+Tab through panes, Shift+F10 and the Menu key), and the filmstrip, tag, reject, metadata, keyword, preset, and caption keys around the Edit in Imago hand-off (LP-1216, LP-1217).
  - Tests: `KeymapConflictTests` (default and each alternative set conflict-free), `ShortcutSetRoundTripTests`, `KeymapCoverageTests` (every command in the command registry has a default or is listed as unbound on purpose).
  - Export the default keymap to `docs/user/lumen/keyboard-shortcuts.md` from a generator so the page cannot drift.
  - Commit: `"lumen: the default keymap, alternative key sets, the editor, and the overlay"`
- **Proof:** unit plus driven: the three test classes pass and the generated shortcuts page is committed; a driven reassignment with a conflict warning is captured; cheaper substitute that fails: a hand-typed shortcut page, which the generator comparison catches.

#### §4. Preferences I: general, interface, file handling, and the viewer and browse pages

- **Deliverable:** An Options dialog with pages for every mode and subsystem holds startup and catalog-at-launch choices, prompts and their reset, completion sounds, interface tweaks, date and time format, proxy, error reporting opt-out, dialog profiles, the viewer start folder, and browse window and file list behavior.
- **Depends On:** §1
- **Phase:** 39
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/preferences/. Job: a user finds and changes any behavior in one place and can undo a bad change by resetting a page. Treatment: an Options dialog with a page tree (General, Interface, File Handling, Viewer, Browse, Performance, Color, External Editing), a search box, and Reset Page; each page lists the keys other sections registered. Cheaper substitute that fails: a raw JSON file. Chrome: consume `PreferenceKeyRegistry` and `WarningRegistry` moved by `D03 T20 §4` and the settings store; pages for keys defined elsewhere are generated from the registry, never duplicated.
- **Runs:** `Requires: display-session -- the Options dialog needs an interactive desktop`
- **Catalog:** LP-0472, LP-1096 to LP-1109 (15 features)
- **Source:** `-> SOURCE: parity-lumen-preferences-general`
- **Hints:**
  - Options dialog (LP-1102) generated from `PreferenceKeyRegistry` with search and Reset Page.
  - Startup (LP-1096): splash, default catalog at launch (most recent, prompt, specific), catalog chooser when Ctrl is held at launch.
  - Prompts (LP-1099): reset all warning dialogs through `WarningRegistry`; remember last selection per source (LP-1100).
  - Sounds (LP-0472, LP-1098): completion sounds for import, the watched-folder import, and export mapped to Windows sound events so the system Sounds settings govern them.
  - Interface tweaks (LP-1097): zoom clicked point to center, font smoothing, Auto Sync notifications; date and time output format, system or custom (LP-1103).
  - Network proxy (LP-1101) used by the AI client, map tiles, uploads, and the update check; error reporting opt-out (LP-1105): no crash data leaves the machine unless the user sends a report.
  - Dialog profiles (LP-1108): named sets of dialog settings saved and loaded; hide common folders in open and save dialogs (LP-1107).
  - Viewer and browse pages (LP-1104, LP-1106, LP-1109): title bar path and catalog name, folder tree density and expanders, clear path history on exit, overlay on excluded folders, hot tracking, animations, image-type highlighting, auto scroll while building, Esc warning, viewer start folder.
  - Tests: `PreferencePagesTests` (every registered key appears on exactly one page), `ProxySettingsTests`, `ResetPageTests`.
  - Commit: `"lumen: the Options dialog with general, interface, viewer, and browse pages"`
- **Proof:** unit plus driven: the three test classes pass and captures of each page are committed; cheaper substitute that fails: a hand-built page missing registered keys, which `PreferencePagesTests` catches.

#### §5. Preferences II: performance, caches, color management, and display

- **Deliverable:** Performance and display pages set display color management (monitor profile, default input profile for untagged images, managed thumbnails), GPU preferences and GPU selection, the develop cache location, size, and purge, parallel preview generation and HDR display in the library, and warn when the display is not true color.
- **Depends On:** §4
- **Phase:** 39
- **Surface:** UI. Fidelity: docs/captures/lumen/preferences/. Job: a user trades speed for disk and sees accurate color on their monitor. Treatment: Performance and Color pages in §4's dialog with a cache usage bar and a Purge button, and a profile details readout. Cheaper substitute that fails: a GPU on/off switch that changes nothing. Chrome: consume `D01 T04 §1` for display transforms, the preview cache of `D04 T01 §7`, and the develop cache; the GPU develop path itself is backlog B-033.
- **Runs:** `Requires: display-session -- display profile readout and purge need an interactive desktop`
- **Catalog:** LP-1110 to LP-1115 (6 features)
- **Source:** `-> SOURCE: parity-lumen-preferences-performance`
- **Hints:**
  - Display color (LP-1110): the monitor profile per display read through `D01 T04 §1`, the engine name, default input profile for untagged images, managed thumbnails toggle, and profile details.
  - GPU (LP-1111, LP-1114): auto, custom, off for display and preview work, GPU preview generation, and primary or automatic adapter selection; the develop engine stays on the CPU path until B-033 is promoted, and the page says so.
  - Develop cache (LP-1112): location, maximum size, and purge with the current usage.
  - Previews (LP-1113): parallel preview generation count, HDR display in the library (consuming `D03 T15 §4`'s HDR display path where Imago moved it), and hover previews for presets, history, and snapshots.
  - True color warning (LP-1115) when the display reports under 24 bits.
  - Tests: `DisplayProfileSelectionTests`, `CachePurgeTests` (purge frees the stated bytes and keeps the catalog intact).
  - Commit: `"lumen: performance, cache, color management, and display preferences"`
- **Proof:** unit plus driven: the two test classes pass and a purge is captured with the log line; cheaper substitute that fails: an unmanaged preview, which the display profile test catches.

#### §6. Settings storage, portable mode, and migration

- **Deliverable:** Settings can be reset at launch or on demand, stored with the catalog where Lightroom stores presets, run portably from a folder or USB stick with settings beside the program, copied to another PC, frozen read-only, redirected and locked by administrators, installed silently with documented switches, and imported from a previous installation with its presets and sets.
- **Depends On:** §4
- **Phase:** 39
- **Surface:** UI. Fidelity: docs/captures/lumen/preferences/. Job: a user carries Lumen and its settings between machines, and an administrator deploys it with locked defaults. Treatment: a Settings page showing the settings folder with Copy, Export, Import, Reset, and Freeze, and a first-run Import Settings prompt when an earlier installation is found. Cheaper substitute that fails: settings only in the registry. Chrome: extend the settings store of `D01 T02 §2` with a portable root and a deployment overlay; installer switches live in `D05 T01`.
- **Runs:** `Requires: display-session -- the import prompt and portable run need an interactive desktop`
- **Catalog:** LP-0425, LP-1116 to LP-1123 (9 features)
- **Source:** `-> SOURCE: parity-lumen-settings-storage`
- **Hints:**
  - Portable mode (LP-1121): a `Lumen.portable` marker beside `Lumen.exe` and `LumenViewer.exe` makes the settings store, logs, caches, and default catalog live under `.\Data\`; a read-only medium is refused by name with a fallback offer.
  - Settings file (LP-1122): location shown, copy to another PC as one `.lumensettings` package, read-only freeze, UTF-8 encoding.
  - Presets stored with the catalog (LP-0425): develop, export, and metadata presets optionally in the catalog folder so a catalog moves with them.
  - Reset (LP-1116): at launch by holding Ctrl+Shift, or from the page, taking a backup first.
  - Migration (LP-1117 to LP-1119): on first run and on demand, import settings, metadata views and presets, label, category, and keyword sets, search presets and history, new image presets, develop, export, batch, rename, resize presets, and external editors from a previous Lumen installation (and from the settings package).
  - Administrator deployment (LP-1123): a machine-wide `deployment.json` redirecting the settings folder, setting the default language, locking the toolbar, disabling delete, forcing browsing mode, restricting save formats, and suppressing prompts; locked keys show as read-only with a tooltip.
  - Installer options (LP-1120): document silent install, folder, shortcuts, file associations, settings folder, and silent uninstall switches of the Inno Setup installer built in `D05 T01`, in `docs/user/lumen/deployment.md`.
  - Tests: `PortableModeTests` (all writes under `.\Data\` with the marker present), `DeploymentOverlayTests` (locked keys refuse writes), `SettingsMigrationTests` (a fixture of an earlier installation imports each set), `SettingsResetTests`.
  - Commit: `"lumen: portable mode, deployment settings, reset, and migration"`
- **Proof:** unit plus driven: the four test classes pass; the portable ZIP run from a USB-like folder writes nothing under `%LOCALAPPDATA%` (a before-and-after listing quoted); cheaper substitute that fails: a portable flag that still writes logs to `%LOCALAPPDATA%`, which the listing catches.

#### §7. Help, learning, languages, and updates

- **Deliverable:** Help opens the Lumen user guide, context help on F1, bundled readme files, community, feedback, and support links; a first-run quick start sets the start folder, folders to index, and the backup reminder; the interface language switches on the fly from language packs with a translation kit; updates are checked through the suite's opt-in check; system info and the installed codecs list support troubleshooting; the platform page states 64-bit and ARM64 support.
- **Depends On:** §1
- **Phase:** 39
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/help/. Job: a new user gets going in a minute and a stuck user finds help or reports a problem with the facts attached. Treatment: a Help menu (User Guide, Context Help F1, Keyboard Shortcuts, What's New, Check for Updates, System Info, Installed Codecs, About), a Quick Start dialog on first run, and a Language page. Cheaper substitute that fails: a Help menu that opens the project home page only. Chrome: consume `SystemInfoReport` and the help plumbing moved by `D03 T20 §8`, the language switching of `D03 T20 §9`, the update check of `D05 T01 §4`, and the About dialog of `D04 T01 §2`.
- **Runs:** `Requires: display-session -- the help surfaces need an interactive desktop`
- **Catalog:** LP-1132 to LP-1140 (9 features)
- **Source:** `-> SOURCE: parity-lumen-help`
- **Hints:**
  - User guide and links (LP-1134, LP-1139): open `docs/user/lumen/` pages as published by `D06 T02 §3`, bundled readme files, and project community and feedback links.
  - Context help (LP-1137): F1 maps the focused surface to its user-guide page through a `HelpTopicMap` with a test that every mapped page exists.
  - Quick start (LP-1136): start folder, folders to index (feeding `D04 T05 §2`), backup reminder interval, show at startup.
  - Languages (LP-1135): on-the-fly switch through `D03 T20 §9`'s mechanism over `.resx` resources (from `D04 T02 §9`), language packs as satellite assemblies, and a translation kit (the neutral `.resx` files and a README) under `docs/dev/lumen/translation.md`.
  - Updates (LP-1132): Check for Updates consumes `D05 T01 §4`, opt-in, nothing sent without the user's action.
  - Troubleshooting (LP-1133, LP-1140): System Info (version, OS, GPU, caches, catalog size) and an Installed Codecs list (every `Photon.Core/Formats/` codec with its native library version) copyable to the clipboard.
  - Platform (LP-1138): 64-bit and ARM64 (`D05 T01 §3`), the supported Windows range, Unicode paths throughout; a Store edition is recorded as not planned.
  - Tests: `HelpTopicMapTests`, `InstalledCodecsReportTests`, `LanguageSwitchTests` (a pseudo-locale switch updates open windows).
  - Commit: `"lumen: help, quick start, languages, updates, and system info"`
- **Proof:** unit plus driven: the three test classes pass; captures of Quick Start, System Info, and a language switch are committed; cheaper substitute that fails: an F1 key that opens the guide's front page, which `HelpTopicMapTests` catches.

#### §8. Themes and appearance

- **Deliverable:** Lumen follows the suite theme with dark and light modes and a theme choice, a main window background fill and panel font size, high-DPI rendering, and toolbar icon sizes and icon sets standing in for IrfanView skins, with no third-party skin art bundled.
- **Depends On:** §1
- **Phase:** 39
- **Surface:** UI. Fidelity: docs/captures/lumen/main-window/. Job: a user sets Lumen to match their eyes and screen. Treatment: an Appearance page with theme (dark, light, system), background fill, panel font size, toolbar button size, and icon set. Cheaper substitute that fails: hard-coded colors per window. Chrome: consume the suite theme resources of `D01 T01 §3` and the icon catalog; no surface hardcodes a color.
- **Runs:** `Requires: display-session -- theme captures at several DPI settings need an interactive desktop`
- **Catalog:** LP-1080 to LP-1083, LP-1124 (5 features)
- **Source:** `-> SOURCE: parity-lumen-appearance`
- **Hints:**
  - Theme choice and dark mode (LP-1081, LP-1124): dark, light, and follow Windows, switching live through the suite theme dictionaries.
  - Background fill and panel font size (LP-1080) as theme overrides stored in `Lumen.Appearance.*`.
  - High DPI (LP-1082): per-monitor v2 awareness in both executables' manifests, with captures at 100, 150, and 200 percent.
  - Toolbar skins (LP-1083): toolbar button size and icon sets from the Photon icon catalog; IrfanView skin files are not read and no third-party art ships.
  - Tests: `ThemeResourceAuditTests` (a XAML scan finds no literal colors in Lumen views), `ThemeSwitchTests`.
  - Commit: `"lumen: themes, background, font size, high DPI, and icon sizes"`
- **Proof:** unit plus driven: the two test classes pass and captures at three DPI settings in both themes are committed; cheaper substitute that fails: a dark theme applied to the main window only, which the XAML audit catches.

#### §9. External editors

- **Deliverable:** Photos open in additional external editors (up to ten, per extension, with a default editor on Ctrl+Alt+X) with per-editor presets for TIFF, PSD, or PSB, color space, bit depth, resolution, and compression, a choice of editing a copy with Lumen adjustments, a copy of the original, or the original non-raw file, HDR hand-off in HDR spaces, file naming, stacking with the original, and the round trip back into the catalog; Edit in Imago gains layers and a linked raw document.
- **Depends On:** §4
- **Phase:** 39
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/lumen/external-editors/. Job: a photographer finishes a photo in whatever editor they own and sees the result back in the library. Treatment: an External Editing page (editor list with add, edit, remove, default, per-extension mapping, presets) and Photo, Edit In submenu with Imago first and the configured editors after. Cheaper substitute that fails: Open With passing the original path only. Chrome: extend `D04 T02 §7`'s `EditInService` (render, launch, watch, stack) and consume `D02 T15 §11`'s `SuiteAppLocator` for Imago; do not write a second hand-off service.
- **Runs:** `Requires: display-session -- launching an external editor needs an interactive desktop`
- **Catalog:** LP-1084 to LP-1091 (8 features)
- **Source:** `-> SOURCE: parity-lumen-external-editors`
- **Hints:**
  - Editor registry (LP-1089, LP-1091): up to ten editors with name, executable, arguments, per-extension defaults, shortcuts and toolbar buttons, Editors menu, multiple images per launch.
  - Copy presets (LP-1084, LP-1088): TIFF, PSD, or PSB, color space, bit depth, resolution, compression, file naming with tokens, stack with original.
  - Edit choices (LP-1085): a copy with Lumen adjustments, a copy of the original, or the original non-raw file; "Edit Original" launches the editor on the original's path (the editor, not Lumen, may write it) with a first-use explanation, and Lumen itself never opens it for writing.
  - HDR hand-off (LP-1087): Rec. 2020 PQ or linear scene-referred 32-bit TIFF for HDR photos.
  - Default editor (LP-1090) on Ctrl+Alt+X.
  - Edit in Imago as layers or a linked raw document (LP-1086): several photos passed to Imago's open-as-layers command line, or a raw file with its develop settings as XMP for Imago's Develop studio.
  - Round trip: the `D04 T02 §7` watcher refreshes the stacked copy when the editor saves.
  - Tests: `ExternalEditorRegistryTests`, `EditCopyPresetTests` (each preset's output format, depth, and profile), `EditOriginalGuardTests` (Lumen opens no handle for write on the original during the flow).
  - Commit: `"lumen: external editors with presets, round trip, and stacking"`
- **Proof:** unit plus driven: the three test classes pass; a driven edit in a second editor (Paint.NET or GIMP, version quoted) refreshes the stacked copy (capture); cheaper substitute that fails: passing the original path for every edit, which `EditCopyPresetTests` catches.

#### Sizing concerns

- §2 carries 14 features across toolbars, menus, docking, workspaces, text fields, and touch; touch (LP-1071, LP-1074) is the natural split with Phase 39's room if the checklist passes 30 items.
- §4 carries 15 features but most are keys on generated pages; the risk is the viewer and browse pages, which the registry generation keeps small.

### todo/04-lumen/TODO-02-lumen-develop.md -- one relocated section

`D04 T02 §9` (Accessibility and localization) keeps its address and moves from old Phase 32 (Lumen after 0.1.0: accessibility), which leaves the plan, into Phase 39 as its last row before `D04 T15 §10` (Lumen 1.0.0), exactly as Imago's `D03 T07 §16` moved to the end of Phase 27; no new section is created.

- **Why:** the audit must cover every Lumen surface the parity phases add (the viewer, browse, library, import, metadata and map, develop, AI, batch, output, and workspace), so it runs after the last of them and before 1.0.0 declares the catalog complete; running it after 0.1.0 would audit a fraction of the app and ship 1.0.0 unaudited.
- **Depends On:** keeps `§8` and gains `D04 T14 §9` and `D04 T12 §13` (the last rows of the workspace and output files), plus `D04 T04 §13`, `D04 T05 §12`, `D04 T06 §13`, `D04 T07 §8`, `D04 T08 §7`, `D04 T09 §16`, `D04 T10 §11`, and `D04 T11 §10` (the last row of each parity file), so the audit follows every parity surface.
- **Scope added at integration:** the Accessibility Insights audit (version quoted) runs over both executables (`Lumen.exe` and `LumenViewer.exe`) and every module and dialog captured under `docs/captures/lumen/`, keyboard reachability is checked against `D04 T14 §3`'s generated keymap, and the pseudo-locale build covers every `.resx` string the parity sections added; the checklist gains those items inside the 30-item cap.
- **Integration edits:** `D04 T02`'s Goal and Outcome sentence about §9 running after the suite release is corrected with a `**Corrected 2026-09-27:**` note; `todo/04-lumen/INDEX.md` changes its phase line to "Phases 28, 29, and 30 to 39"; the acceptance-bar row "It works without a mouse or eyes" keeps `D04 T02 §9`, which now runs last in Phase 39; `D04 T15 §10` depends on it.

### todo/04-lumen/TODO-15-lumen-parity-releases.md -- `lumen-parity-releases`

- **Title:** "TODO-15 -- Lumen Parity Releases: 0.2.0 to 1.0.0"
- **Phase(s):** 30 to 39, one release section at the end of each
- **Goal:** Each Lumen parity phase ends with a published, independently installable Lumen release on its own `lumen-v*` tag, proven on a clean machine with the original-file guard re-checked on the installed build, whose release notes list the parity catalog features the phase completed, so progress is shipped rather than accumulated; `lumen-v1.0.0` at the end of Phase 39 declares the catalog complete (every `plan` row stamped, every other row carrying its recorded status).
- **Current-state facts to verify (with claim candidates):**
  - Lumen's only planned release so far is 0.1.0 (`D04 T02 §8`), and Lumen has no code or tag yet. `<!-- claim: exists todo/04-lumen/TODO-02-lumen-develop.md -->` `<!-- claim: absent src/Lumen -->`
  - The release standard the sections follow is `standards/release.md`. `<!-- claim: exists standards/release.md -->`
  - The Lumen installer script exists but refuses to compile until Lumen ships. `<!-- claim: count "LumenShipping" installer/Lumen.iss = 3 -->`
- **Inputs and XREFs:** `standards/release.md`, `standards/lumen.md` (the guard re-checked per release); `docs/parity/lumen-parity.md` (the catalog each release reconciles); -> XREF: D04 T02 §8 (the 0.1.0 release procedure every section repeats); -> XREF: D05 T01 §1 (the clean-machine procedure); -> XREF: D00 T01 §8 (`query parity --catalog lumen`, quoted by each release); -> XREF: D06 T01 §3 (the Lumen user guide each release extends); -> XREF: D04 T02 §9 (the accessibility audit §10 depends on).
- **Adjacency:** list=not-applicable (releases are listed by GitHub Releases); document=applicable (release notes and user-guide pages); settings=not-applicable (no settings of its own); reporting=applicable @ D00 T01 §8 (the per-phase parity report each release quotes); notifications=not-applicable (no runtime surface); permissions=not-applicable (no files written by the app); audit=applicable (the tag, the release notes, and the stamped rows are the audit trail); exchange=not-applicable (no formats of its own); reverse=applicable (a failed clean-machine install or a changed original blocks the tag; the previous release stays current)

Every section below has the same shape; only the phase, the version, and the dependency list differ.

- **Depends On:** the previous release section (`§1` depends on `D04 T02 §8`) plus every other row of its phase, in the phase order of "Phase layout and renumbering".
- **Surface:** no surface of its own (the release artifacts are the installer, the portable ZIP, the notes, and the tag)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)` and `Requires: display-session -- launching the installed app and the viewer on the clean machine needs an interactive desktop`
- **Catalog:** owns no catalog rows (it reconciles them)
- **Source:** `-> SOURCE: parity-lumen-release-<version>`
- **Hints:**
  - Run `python scripts/todo-graph.py query parity --catalog lumen --phase <N>` and quote it: every catalog row planned to a section of the phase is owned by a stamped section; a row that cannot ship is moved to the backlog through `add-todo` with the catalog updated in the same commit, never left planned and unshipped.
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every gate `PASS`.
  - Write the `lumen-v<version>` section of `CHANGELOG.md` listing the phase's user-visible features by catalog area, and add or update the user-guide pages under `docs/user/` for every new surface.
  - Package locally and run the clean-machine procedure from `D05 T01 §1` (install per-user and all-users, start `Lumen.exe` and `LumenViewer.exe`, one driven action per new surface with captures under `docs/captures/lumen/release-<version>/`, uninstall leaving no registry value the install wrote).
  - Re-run the original-file guard on the installed build: import, browse, develop, batch, and export over a copied fixture folder, then quote the before-and-after SHA-256 table of every original (all unchanged).
  - Quote the viewer's startup budget on the reference machine (`docs/dev/lumen/viewer-budgets.md`) and the browse budget once `D04 T05 §2` has shipped, so a regression blocks the tag.
  - Confirm no Lumen or Lumen Viewer menu item is disabled without naming a planned section or a backlog id.
  - Push `lumen-v<version>`; verify the workflow, the assets, and `SHA256SUMS`; run the portable ZIP from an empty folder; update `README.md`'s Lumen status line; no other app's version moves.
  - Commit: `"release: Lumen <version>"`.
- **Proof:** driven run with evidence: the clean-machine install log, the smoke captures, the unchanged-originals hash table from the installed build, the quoted `query parity` output with zero unshipped planned rows for the phase, and `gh release view lumen-v<version> --json isPrerelease,assets` showing a non-prerelease with its assets; cheaper substitute that fails: tagging from a developer machine, which the clean-machine log and installed-build hash table refuse.

| Section | Title | Phase | Version |
| ------- | ----- | ---: | ------- |
| §1 | Lumen 0.2.0 (Phase 30) | 30 | `lumen-v0.2.0` |
| §2 | Lumen 0.3.0 (Phase 31) | 31 | `lumen-v0.3.0` |
| §3 | Lumen 0.4.0 (Phase 32) | 32 | `lumen-v0.4.0` |
| §4 | Lumen 0.5.0 (Phase 33) | 33 | `lumen-v0.5.0` |
| §5 | Lumen 0.6.0 (Phase 34) | 34 | `lumen-v0.6.0` |
| §6 | Lumen 0.7.0 (Phase 35) | 35 | `lumen-v0.7.0` |
| §7 | Lumen 0.8.0 (Phase 36) | 36 | `lumen-v0.8.0` |
| §8 | Lumen 0.9.0 (Phase 37) | 37 | `lumen-v0.9.0` |
| §9 | Lumen 0.10.0 (Phase 38) | 38 | `lumen-v0.10.0` |
| §10 | Lumen 1.0.0 (Phase 39): the parity catalog complete | 39 | `lumen-v1.0.0` |

§1 adds one item: `LumenViewer.exe` is in the installer and the portable ZIP, and the clean-machine run registers it for image types through the installer task and opens a `.heic` and a `.cr3` from Explorer after the user confirms it in Default Apps. §10 adds three items: `query parity --catalog lumen` over every phase reports zero `plan` rows owned by an unstamped section and zero `parity-ip-route-dead` findings (every row routed to Imago names a live Imago row); the README and the Lumen user guide state parity with Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76 with the catalog link; and the accessibility audit `D04 T02 §9` is among its dependencies, so 1.0.0 never ships an unaudited surface.

#### Sizing concerns

- Every release section stays near 14 items; §1 and §10 add one and three.
