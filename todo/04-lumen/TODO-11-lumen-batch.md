---
schema_version: 1
id: lumen-batch
domain: 04-lumen
status: draft
title: "TODO-11 -- Lumen Batch Tools: Rename, Convert, Resize, Edit, and Export"
depends_on: []
frozen: true
track: L11
---

# TODO-11 -- Lumen Batch Tools: Rename, Convert, Resize, Edit, and Export

> **Goal:** Batch work is core Lumen (operator decision 2026-09-27): one job engine in `Photon.Lumen.Core/Batch/` runs ordered `IBatchOperation`s (rename, convert, resize, rotate and flip, color, the ACDSee Batch Edit and IrfanView advanced operations, text and watermarks, develop, export) over a file list in the background under one Activity Manager, always with a dry run listing every output name, conflict, and skip before anything is written; one token engine names files and fills overlays across the app and accepts IrfanView's `$`-patterns; renames and moves are journaled and undoable; pixel operations reuse the suite pixel engine and the develop engine, never a copy. Originals are safe by default with opt-in writes (operator decision 2026-09-27): every batch writes new files unless the user explicitly chose an in-place overwrite for that operation, which `OriginalWritePolicy` allows only with the setting on, a verified backup copy by default, and an atomic replace through the suite atomic writer. Recorded actions, droplets, scripting, and command-line switches stay in B-041 and B-042.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Lumen has no code. The only batch work Lumen plans today is develop sync (`D04 T02 §5`) and export (`D04 T02 §6`), with one naming template, `{date}-{name}-{seq}`. The suite-wide batch entry B-042 in `todo/backlog.md` covers action-based batch; the integration rewords it to exclude Lumen's core batch tools. The suite pixel engine the operations reuse is planned (`todo/01-core/TODO-03-photon-pixel-engine.md`), not built, and `Photon.Core` does not exist yet. `standards/lumen.md` states the original-file guard as safe by default with opt-in in-place writes (the operator's 2026-09-27 decision, recorded in the standard at the Lumen integration), which §1 here builds.
<!-- claim: absent src/Lumen -->
<!-- claim: count "\{date\}-\{name\}-\{seq\}" todo/04-lumen/TODO-02-lumen-develop.md = 1 -->
<!-- claim: count "\[B-042\]" todo/backlog.md = 1 -->
<!-- claim: exists todo/01-core/TODO-03-photon-pixel-engine.md -->
<!-- claim: absent src/Photon.Core -->

## Inputs

- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard this file enforces and extends with the opt-in in-place path
- [`standards/shared.md`](../../standards/shared.md) -- logging, cancellation, progress over one second, atomic writes, refusals that name the file
- [`docs/parity/lumen-section-design.md`](../../docs/parity/lumen-section-design.md) -- the blueprint; [`docs/parity/lumen-parity.md`](../../docs/parity/lumen-parity.md) -- the catalog rows each section owns
- IrfanView 4.76 help pages `hlp_batch_conversion.htm` and `hlp_text_patternoptions.htm` (the `$`-pattern alias list); ACDSee Photo Studio Ultimate 2027 User Guide, the Batch chapters; Lightroom Classic 15.5.1 Filename Template Editor and Text Template Editor help
- Exif 3.0 (CIPA DC-008-2023) and IPTC IIM 4.2 (token tag numbers); ITU T.81 and libjpeg-turbo 3.1 `transupp` (lossless transforms, with `jpegtran` as the oracle); lcms2 `transicc` (the ICC oracle)
- Microsoft Learn: `IFileOperation` and `FOFX_RECYCLEONDELETE`; "Verbs and File Associations" (`MultiSelectModel`)
- -> XREF: D01 T02 §3 -- single-instance forwarding the Explorer verb and the viewer's `B` key use in §10
- -> XREF: D01 T02 §4 -- the suite history that records batch develop and orientation as undo steps
- -> XREF: D01 T02 §5 -- the atomic writer every output and every in-place replace uses
- -> XREF: D01 T03 §2 -- resampling filters §5 calls
- -> XREF: D01 T03 §3 -- palette quantization for §7's color depth
- -> XREF: D01 T03 §4 -- tonal kernels §6 and §7 call
- -> XREF: D01 T03 §5 -- color kernels §7 calls
- -> XREF: D01 T03 §6 -- noise and sharpen kernels §7 calls
- -> XREF: D01 T06 §1 -- the effect registry §7's filters and frame effects list
- -> XREF: D01 T04 §1 -- ICC conversion for §4 and §6
- -> XREF: D01 T04 §2 -- rendering intents and black point compensation for §6
- -> XREF: D01 T09 §2 -- the isolated 8BF filter host §7's `PluginFilterOperation` runs through (the former B-012 row LP-1160)
- -> XREF: D01 T07 §7 -- the tone equalizer stage §7's Light EQ operation calls (Phase 23, before this file)
- -> XREF: D03 T16 §1 -- the shared text engine §8 shapes overlay text with
- -> XREF: D03 T17 §10 -- the EXIF and IPTC readers §2's tokens evaluate through
- -> XREF: D04 T01 §7 -- previews and the preview cache §1's idle jobs and §4's thumbnail export read
- -> XREF: D04 T01 §11 -- sidecars §3 renames and §5's orientation writes
- -> XREF: D04 T02 §5 -- develop presets §9 applies
- -> XREF: D04 T02 §6 -- the export runner and naming template §2 and §9 extend
- -> XREF: D04 T04 §1 -- the viewer opens §10's dialog with `B`
- -> XREF: D04 T04 §3 -- the installer task that registers §10's Explorer verb
- -> XREF: D04 T04 §11 -- the viewer's quick edits run §5 to §8's operations and consume §5's orientation command
- -> XREF: D04 T04 §13 -- viewer text and watermark consume §8's renderer
- -> XREF: D04 T04 §16 -- the viewer's lossless JPEG transforms consume §5's `LosslessJpegTransform`
- -> XREF: D04 T05 §1 -- browse supplies browsed records to §9's preset runner
- -> XREF: D04 T05 §6 -- file operations extend §3's journal
- -> XREF: D04 T05 §8 -- file lists share §10's text list format
- -> XREF: D04 T06 §7 -- saved searches §1's history reopens
- -> XREF: D04 T07 §2 -- import renaming consumes §2
- -> XREF: D04 T08 §8 -- metadata writing, whose exported-copy embedding §4 calls for converted files
- -> XREF: D04 T08 §9 -- the opt-in metadata embedder that writes through §1's `InPlaceWriter`
- -> XREF: D04 T09 §11 -- the develop presets and defaults §9 applies
- -> XREF: D04 T09 §16 -- photo merges that run as §1 jobs
- -> XREF: D04 T09 §17 -- develop's opt-in writes to originals, which must go through §1's `OriginalWritePolicy` and `InPlaceWriter` rather than a second writer
- -> XREF: D04 T10 §8 -- batch denoise and super resolution runners queue in §1
- -> XREF: D04 T12 §1 -- export naming and destinations consume §2 and §4
- -> XREF: D04 T12 §13 -- export watermarks consume §8
- -> XREF: D04 T13 §1 -- the shared codec registry every operation reads through
- -> XREF: D04 T13 §4 -- the extract-pages suffix §2 turns into a token template
- -> XREF: D04 T13 §5 -- RAW+JPEG pairs §3 renames together
- -> XREF: D04 T13 §6 -- the writers and option profiles §4 writes through, and the save path that consults §1's guard
- -> XREF: D04 T14 §4 -- the preferences page that renders the `Lumen.Originals.*` and `Lumen.Batch.*` keys
- -> XREF: D04 T14 §10 -- the Originals group on the File Handling page that renders §1's `Lumen.Originals.*` keys and locks them off by deployment policy, never a second policy or writer
- -> XREF: D04 T15 §2 -- `lumen-v0.3.0`, which re-proves §1's in-place defaults

## Outcome

- Every batch runs as a job in one Activity Manager with a mandatory dry run, pause, resume, cancel, reorder, and a history with per-file results.
- One token engine names files and fills text for batch rename, export, import, overlays, and captions, and IrfanView's `$`-patterns produce the same names IrfanView would.
- Batch rename, convert, resize, rotate, color, edit, develop, and export each write new files by default; renames and moves undo from a journal.
- In-place writes happen only when the user turned on the setting for that operation and chose the in-place destination, always atomically and, by default, after a verified backup copy.
- The batch dialog starts from the Batch menu, the viewer's `B` key, and Explorer's context menu.

**Adjacency:** list=applicable @ D04 T11 §10; document=applicable @ D04 T11 §4; settings=applicable @ D04 T11 §1; reporting=applicable @ D04 T11 §1; notifications=applicable @ D04 T11 §1; permissions=applicable @ D04 T11 §1; audit=applicable @ D04 T11 §1; exchange=applicable @ D04 T11 §4; reverse=applicable @ D04 T11 §3

**Adjacency rationale:** The lists are the batch file list (§10) and the Activity Manager's queue and history (§1). Every output file is a document the user keeps (§4 and the runners after it). Settings are `Lumen.Batch.*`, `Lumen.Tokens.*`, `Lumen.Overlays.*`, `Lumen.Activity.*`, and `Lumen.Originals.*` keys, each with a default and a named consumer. Completion reports and the per-file history are the reporting, and queued and completed notifications carry error, skip, and warning counts (§1). Read-only destinations, locked files, files open in develop, and an in-place write without the policy are refused by name (§1). One Serilog Information line per job and per output, and the rename journal, are the audit trail (§1, §3). Outputs go to every writable format and batch profiles export and import as JSON (§4, §7). Rename and move journals undo, outputs are new files, and in-place writes keep a restorable backup (§3, §1).

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The batch engine, the original-write policy, and the Activity Manager | D04 T02 §8, D04 T13 §1 |  [ ]   |
|   2   |   §2    | The token engine | §1, D03 T17 §10 |  [ ]   |
|   3   |   §3    | Batch rename | §2, D04 T13 §5 |  [ ]   |
|   4   |   §4    | Batch convert | §1, §2, D04 T13 §6 |  [ ]   |
|   5   |   §5    | Batch resize, rotate, and flip | §4 |  [ ]   |
|   6   |   §6    | Batch color: exposure, profiles, and color depth | §4 |  [ ]   |
|   7   |   §8    | Text overlays and watermarks | §2, D03 T16 §1 |  [ ]   |
|   8   |   §7    | The batch edit pipeline | §5, §6, §8, D01 T07 §7, D01 T09 §2 |  [ ]   |
|   9   |   §9    | Batch develop and batch export | §7, D04 T02 §6 |  [ ]   |
|  10   |   §10   | The batch dialog: file lists, profiles, and running from Explorer and the viewer | §3, §9, D04 T04 §1 |  [ ]   |

---

## 1. The Batch Engine, the Original-Write Policy, and the Activity Manager

Every long job in Lumen (import, export, convert, develop, indexing, faces, similarity, AI keywords) needs one place to queue, run, pause, and report, and every batch needs one guard over the files it writes. This section builds the job engine (a job is an ordered list of `IBatchOperation`s over a file list, with a mandatory dry run), the `OriginalGuard` and `OriginalWritePolicy` that make originals safe by default with opt-in in-place writes (operator decision 2026-09-27: settings to embed metadata into originals and rotate, save, or convert in place like ACDSee and IrfanView, through the suite atomic writer with an optional backup copy), and the Activity Manager pane with notifications and a per-file history. Other sections register their jobs here; idle-time jobs belong to their own sections. Catalog: LP-0471, LP-0752 to LP-0761 (11 features: import progress in the Activity Manager, the activity centre, queued and idle activities, the one pane, idle activities, job control, concurrency, notifications, history, convert status, and originals kept). -> SOURCE: parity-lumen-batch-engine

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/activity-manager/`.
**Job:** a user starts long jobs and keeps working, sees what is queued, running, and done, and finds any output or failure afterward. Consumer: every job runner in Lumen and the history the user reopens.
**Treatment:** ACDSee's Activity Manager pane (Queued, Running, Idle, and History tabs) with a status-bar indicator, Lightroom's activity-centre progress, toasts with Show and Browse output buttons, and a history details view (status, name, source, destination, preset); a first-use confirmation for any in-place write naming what changes and where the backup goes. Cheaper substitute that fails the checkpoint: a modal progress dialog per job.
**Chrome:** consume `Photon.UI` list and toast styles, the settings store, `AtomicFileWriter` (`D01 T02 §5`), and the catalog. Do not add a second job queue or a second progress dialog.

**Requires:** display-session -- the Activity Manager pane and toasts need an interactive desktop

**Freeze check:** `BatchRunner` writes only through `AtomicFileWriter`; `OriginalGuard` refuses any write whose target is an original or a source of the running job unless `OriginalWritePolicy` allows that operation in place; an allowed in-place write copies the original to the backup folder and verifies it by SHA-256 before the atomic replace, then rereads the result; killing the process at any point leaves either the original byte-identical or the new file complete with the backup intact. This in-place path is the operator-approved change of 2026-09-27; with every `Lumen.Originals.InPlace.*` key off (the default) a full job leaves every source's SHA-256 and last-write time unchanged. Fixture source: `tests/fixtures/lumen/batch/` (created by this section).

- [ ] Add `BatchJob`, `BatchItem`, and `IBatchOperation` (`Plan(BatchItem) -> BatchPlanStep`, `Execute(ImageBuffer, BatchContext)`) in `src/Lumen/Photon.Lumen.Core/Batch/`. Done when: a test composes a two-operation job over three fixtures and the plan lists six steps.
- [ ] Add `BatchPlanner.DryRun()` returning a `BatchPlan` with every output path, conflict, and skip and its reason (LP-0761). Done when: `BatchPlannerTests` assert a planted name conflict and a read-only destination appear in the plan before any file is written.
- [ ] Add `BatchRunner`, which executes only a plan the user confirmed, keyed by the plan's fingerprint, and refuses a stale plan when a source changed since the dry run. Done when: a test touching a source after the dry run gets the refusal naming the file. Cheaper substitute: running without a dry run, which the fingerprint check refuses.
- [ ] Add `OriginalGuard` in `src/Lumen/Photon.Lumen.Core/Originals/OriginalGuard.cs`: `IsOriginal(path)` (every catalog original and every source of the running job) and `AssertWritable(path, OriginalWriteKind)` on every write target (LP-0761). Done when: `BatchGuardTests` assert a write over an original is refused naming the file.
- [ ] Add the in-place write policy, `OriginalWritePolicy`, with the settings `Lumen.Originals.InPlace.EmbedMetadata`, `.Rotate`, `.Save`, and `.Convert` (each default false), `Lumen.Originals.BackupBeforeInPlace` (default true), `Lumen.Originals.BackupFolder` (default `%LOCALAPPDATA%\Rizonesoft\Lumen\originals-backup\`, or `.\Data\originals-backup\` in portable mode), and `Lumen.Originals.BackupRetentionDays` (default 30), each registered in `PreferenceKeyRegistry` with the commands it enables and rendered by the Originals group `D04 T14 §10` adds to `D04 T14 §4`'s File Handling page; these are the only `Lumen.Originals.*` keys in the suite. Done when: `OriginalWritePolicyTests` assert every kind is refused by default and allowed only with its key on.
- [ ] Add `InPlaceWriter.Replace(path, writeAction)`: when `Lumen.Originals.BackupBeforeInPlace` is on (the default), copy the original to the backup folder (mirroring its path), verify the copy by SHA-256, write through `AtomicFileWriter`, reread the result through the registry, and journal a "Restore original from backup" entry; when the user has turned the backup off (the operator's 2026-09-27 choice of an optional backup copy, allowed only after the second confirmation `D04 T14 §10` shows), skip the copy, journal the write as not restorable, and name that in the first-use confirmation. Done when: `InPlaceWriterTests` kill the process after the backup and after the replace and find the original or the new file whole with the backup intact, and `InPlaceWriterTests.BackupOff` writes with no backup file and a journal entry marked not restorable.
- [ ] Add the backup retention sweep: backups older than `Lumen.Originals.BackupRetentionDays` go to the Recycle Bin at startup and their journal entries are marked expired. Done when: `InPlaceWriterTests.Retention` sweeps only expired backups and their restore entries read expired.
- [ ] Show a first-use confirmation for each in-place kind ("Lumen will overwrite 120 originals. Backups go to <folder>. Continue?") with Don't Ask Again per kind, and add Restore Original from Backup for any journaled in-place write. Done when: a driven in-place rotate of one file shows the dialog and the restore rereads the original bytes.
- [ ] Add `ActivityManager` in `src/Lumen/Photon.Lumen.Core/Activity/ActivityManager.cs`: a priority queue with pause, resume, cancel, reorder, pause and resume all, and clear all (LP-0753, LP-0756). Done when: `ActivityManagerTests` assert each command's effect on queue order and state.
- [ ] Register every long job with the one `ActivityManager`, starting with import's progress, pause, and cancel from `D04 T01 §6` (LP-0471). Done when: a test starts an import and cancels it from the manager, and the import's partial result is rolled back by its own rules.
- [ ] Add idle activities (LP-0755): job kinds that run when the user is idle (previews `D04 T01 §7`, similarity `D04 T10 §5`, AI keywords `D04 T10 §4`, faces `D04 T10 §2`) with states, per-kind toggles in `Lumen.Activity.Idle.*`, and queue clearing; the jobs themselves belong to their sections. Done when: a test registers a stub idle kind and it runs only after the idle threshold and pauses on input.
- [ ] Add concurrency rules (LP-0757): parallel items bounded by `Lumen.Batch.MaxParallel` (default core count minus one), never two jobs on the same file, files open in develop skipped with a reason, jobs paused while a file command runs, and a restart request blocked with a prompt while a job runs. Done when: `ActivityManagerTests` assert the one-job-per-file lock and the develop skip reason.
- [ ] Refuse by name a read-only destination, a locked source, a full disk, and a path over the Windows limit, as per-item skips that never stop the rest of the job. Done when: a test with a read-only folder and a locked file finishes the other items and lists both skips with reasons.
- [ ] Add the Activity Manager pane in `src/Lumen/Photon.Lumen.Desktop/Views/Activity/ActivityManagerPane.xaml` with Queued, Running, Idle, and History tabs, progress and remaining counts, per-file status for convert jobs, and a status-bar indicator (LP-0752, LP-0754, LP-0760). Done when: a driven 500-file convert shows progress and the capture is committed.
- [ ] Add notifications (LP-0758): queued and completed toasts with error, skip, and warning counts, Show and Browse output buttons, mute options in `Lumen.Activity.Notifications.*`, and a result report text file beside the output on request. Done when: a driven job with two skips shows a toast naming "2 skipped" and the report lists both.
- [ ] Persist completed jobs in the catalog with per-file rows (status, name, source, destination, preset), a details view, clear items, and reopen of a saved search through `D04 T06 §7` once it ships (LP-0759). Done when: `ActivityHistoryTests` restart Lumen and the history shows the job with its per-file rows.
- [ ] Log one Serilog Information line per job start, finish, and output (`{Job} {Operation} {Source} -> {Target} in {ElapsedMs} ms`) and one per in-place write naming the backup. Done when: a Serilog test sink asserts each line.
- [ ] Commit fixtures under `tests/fixtures/lumen/batch/` (JPEG, RAW, TIFF, a read-only folder recipe, a locked-file recipe) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Add the unchanged-sources test: a full job with every in-place key off leaves every source's SHA-256 and last-write time unchanged. Done when: `BatchGuardTests.SourcesUnchanged` passes.
- [ ] Commit captures under `docs/captures/lumen/activity-manager/` and write `docs/user/lumen/activity-manager.md` and `docs/user/lumen/originals.md` (the in-place settings, backups, and restore). Done when: every tab, the toast, and the in-place confirmation appear in captures and the pages document them.
- [ ] Commit: `"lumen: the batch engine, safe in-place writes, and one Activity Manager"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~BatchPlanner|FullyQualifiedName~ActivityManager|FullyQualifiedName~BatchGuard|FullyQualifiedName~OriginalWritePolicy|FullyQualifiedName~InPlaceWriter|FullyQualifiedName~ActivityHistory"` exits 0; a driven run queues a 500-file convert and an import together, pauses and resumes, and the history details and toasts are captured with timings quoted. Cheaper substitute that fails: running jobs without a dry run, which `BatchPlannerTests` refuse, or an in-place write without a verified backup, which `InPlaceWriterTests` catch.

## 2. The Token Engine

Batch rename, export and import naming, output folders, text overlays, and slideshow, print, web, book, and fullscreen captions all build text from a photo's data; one engine does it for all of them, with file, date, image, EXIF, IPTC, XMP, GPS, maker-note, counter, and special tokens, an editor with a live sample, file-name sanitizing, and IrfanView's `$`-patterns accepted as an alias syntax so an IrfanView user's saved patterns keep working. The IrfanView alias list is data (one table and one test table), not one checklist item per token. Catalog: LP-0762 to LP-0774 (13 features: file-name rules, the filename template editor, the text template editor, the rename templates dialog, output naming in runners, and the file, date, image, IPTC, EXIF, special and counter, GPS, and maker-note tokens). -> SOURCE: parity-lumen-token-engine

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/token-editor/`.
**Job:** a user builds any name or caption from the photo's data once and reuses it everywhere, including patterns they wrote in IrfanView. Consumer: batch rename (§3), destinations (§4), overlays (§8), export (`D04 T02 §6`), import (`D04 T07 §2`), and captions.
**Treatment:** Lightroom's Filename Template Editor and Text Template Editor (token pickers by group, typed text, live example, presets), ACDSee's rename template field with `*` and `#` placeholders, and an "IrfanView patterns" help tab listing the `$` aliases. Cheaper substitute that fails the checkpoint: a fixed `{date}-{name}-{seq}` template.
**Chrome:** consume the EXIF and IPTC readers in `Photon.Core/Metadata/` (`D03 T17 §10`), the settings store, and `Photon.UI` dialogs. Do not add a second string-substitution path anywhere in Lumen.

**Requires:** display-session -- the template editors need an interactive desktop

- [ ] Add `TokenEngine` in `src/Lumen/Photon.Lumen.Core/Tokens/TokenEngine.cs` parsing `{group:name|format}` tokens into an AST. Done when: `TokenEngineTests` parse and print back a template with literals, tokens, and formats unchanged.
- [ ] Add `IrfanViewAliases.cs`, a table mapping IrfanView's `$`-patterns (`$N`, `$F`, `$D`, `$E36867`, `$I120`, `$T(%Y-%m-%d)`, `$Wx$H`, `#` counters, and the rest of `hlp_text_patternoptions.htm`) onto the same AST (LP-0763, LP-0766). Done when: `IrfanViewPatternTests` run a table of the help page's examples and every expected output matches.
- [ ] Add `TokenContext` (file, image, catalog record, metadata, counter, job) and evaluation over it. Done when: a test evaluates one template against a fixture with known EXIF and IPTC and gets the committed string.
- [ ] Add file tokens (LP-0767): folder path, last subfolder, name with or without extension, extension, corrected extension from §1 of `D04 T13`, size, folder index, page index, and substring ranges. Done when: each token's test row passes.
- [ ] Add date and time tokens with strftime-style formats over file, capture, and current dates, including weekday and month names in the UI culture (LP-0768). Done when: each format specifier's test row passes in en-US and de-DE.
- [ ] Add image tokens: width, height, bits per pixel, DPI, megapixels, aspect ratio, zoom, print size, compression, and comment (LP-0769). Done when: each token's test row passes.
- [ ] Add EXIF tokens for any standard tag by name or by number (LP-0771) and IPTC tokens for any dataset (LP-0770). Done when: `$E36867` and `{exif:DateTimeOriginal}` produce the same string and every IPTC Core dataset evaluates on the fixture.
- [ ] Add GPS tokens (latitude, longitude, altitude, time, direction, and a combined pair in decimal or DMS) (LP-0773) and Nikon, Canon, and Fuji maker-note tokens as far as the reader decodes them, empty with a sample warning otherwise (LP-0774). Done when: the GPS rows pass and an undecoded maker-note token shows the warning in the editor.
- [ ] Add special tokens and counters (LP-0772): new line, literal `$`, pipe, and hash; counter width, start, and step; numbers or letters; and ACDSee's `*` (original name) and `#` (counter) placeholders. Done when: each row passes, including `###` starting at 7 printing `007`.
- [ ] Declare where each token applies per consumer (`TokenScope`: file name, folder, text), refusing a new line or a path separator in a file name with a message naming the token. Done when: a test asserts the refusal for `{newline}` in a rename template.
- [ ] Add `FileNameSanitizer` (LP-0762): illegal characters and spaces replaced per `Lumen.Tokens.IllegalCharReplacement` (default `_`) and `Lumen.Tokens.SpaceReplacement` (default keep), reserved Windows names (`CON`, `NUL`, `COM1`) refused, and trailing dots and spaces trimmed. Done when: `FileNameSanitizerTests` pass their table.
- [ ] Add the Filename Template Editor in `src/Lumen/Photon.Lumen.Desktop/Views/Tokens/FilenameTemplateEditor.xaml` (LP-0763): token pickers by group, typed text, insert metadata, and a live example from the selected photo. Done when: a driven edit shows the example updating per keystroke and the capture is committed. Cheaper substitute: a free text box without the live example.
- [ ] Add the Text Template Editor for captions (LP-0764), the same control with the text scope and multi-line output. Done when: a caption template with a new line renders two lines in the example.
- [ ] Add the rename templates dialog (LP-0765): system and user templates, the template field with `*`, `#`, and metadata placeholders, and a sample. Done when: saving a user template lists it beside the system ones after a restart.
- [ ] Store presets and recent templates in `Lumen.Tokens.Templates` with a duplicate-name suffix rule (LP-0766). Done when: the ten most recent templates appear in the editor's history after a restart.
- [ ] Convert `D04 T02 §6`'s `{date}-{name}-{seq}` export naming into a token template with no behavior change. Done when: `D04 T02 §6`'s existing export naming tests pass unchanged through `TokenEngine`.
- [ ] Convert `D04 T13 §4`'s `{name}_p{page}` extract-pages suffix into a token template the Extract Pages dialog can edit. Done when: extracting with `{name}-{page:000}` writes `scan-002.png`.
- [ ] Add a guard test that no other type in `src/Lumen/` performs token substitution (a grep for `.Replace("{` outside `Tokens/`). Done when: the test fails on a planted second substitution.
- [ ] Commit captures under `docs/captures/lumen/token-editor/` and write `docs/user/lumen/tokens.md` with the IrfanView patterns table. Done when: both editors and the patterns tab appear in captures and the page lists every alias.
- [ ] Commit: `"lumen: one token engine with IrfanView pattern aliases"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~TokenEngine|FullyQualifiedName~IrfanViewPattern|FullyQualifiedName~FileNameSanitizer"` exits 0 with the IrfanView example table quoted row by row. Cheaper substitute that fails: per-feature string replacement, which the single-engine guard test exposes.

## 3. Batch Rename

Renaming hundreds of photos is where a mistake costs most, so batch rename runs an ordered, checkable list of up to ten operations with a live preview of every old and new name, resolves every conflict before the run, renames sidecars and RAW+JPEG partners together, keeps catalog records attached, and journals the whole batch so one undo reverses it. A rename is a file operation, never an image write. Single-photo Rename Photo uses the same engine, and `D04 T05 §6` later extends this journal to copy, move, and delete. Catalog: LP-0300, LP-0775 to LP-0784 (11 features: rename photo with a template, the operation list, presets and history, and the template, search and replace, case, insert and remove, strip spaces, conflict, destination, and test-rename operations). -> SOURCE: parity-lumen-batch-rename

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/batch-rename/`.
**Job:** a user renames hundreds of photos predictably, sees every new name first, and can undo. Consumer: the files on disk, their sidecars, and the catalog records that follow them.
**Treatment:** ACDSee's Batch Rename dialog with its operation list and preview grid, IrfanView's rename pattern and search-and-replace fields, and Lightroom's Rename Photo with a template. Cheaper substitute that fails the checkpoint: renaming without a preview.
**Chrome:** consume §1's engine and dry run, §2's tokens, the catalog, and `D04 T13 §5`'s pair detection. Do not add a second rename path for single photos.

**Requires:** display-session -- the rename dialog and its preview need an interactive desktop

**Freeze check:** A rename changes names only: every renamed file's SHA-256 is unchanged; a sidecar and a RAW+JPEG partner are renamed in the same journaled step as their photo; a failure part-way rolls back the renames already made from the journal; names changed outside Lumen since the batch are reported on undo, never overwritten. Fixture source: `tests/fixtures/lumen/rename/` (created by this section).

- [ ] Add `RenamePipeline` of `IRenameOperation` in `src/Lumen/Photon.Lumen.Core/Batch/Rename/`: up to ten operations, each checkable and reorderable, applied in order to the base name and extension (LP-0775). Done when: `RenamePipelineTests` assert order matters with two operations swapped.
- [ ] Add `TemplateRenameOperation` (LP-0777): §2 tokens, numbers or letters, a fixed start or auto-detected continuation from existing names in the target folder, and clear templates. Done when: a folder holding `trip-041` continues at `trip-042`.
- [ ] Add `SearchReplaceOperation` (LP-0778): literal text or a metadata value, case-sensitive option, include the extension option. Done when: each option's test row passes.
- [ ] Add `CaseChangeOperation` for name and extension: lower, upper, title, unchanged (LP-0779). Done when: each row passes, including title case over `IMG_0001`.
- [ ] Add `InsertTextOperation` and `RemoveTextOperation` (LP-0780): at prefix, suffix, a position, before or after text, from the right, overwrite, delimiters, and counts. Done when: each mode's test row passes.
- [ ] Add `StripSpacesOperation` (LP-0781): all, trailing, consecutive, or replace with a character. Done when: each mode's test row passes.
- [ ] Add the preview grid (old name, new name, conflict marker) and Test Rename, which computes every name through §1's dry run without touching a file (LP-0784). Done when: a test asserts Test Rename leaves the folder listing unchanged.
- [ ] Resolve conflicts before the run (LP-0782): duplicate target names and extension changes by ask, skip, or rename with a suffix. Done when: `RenameConflictTests` cover each choice and a two-file collision.
- [ ] Rename in two phases through temporary names so swaps and cycles (`a` to `b` and `b` to `a`) succeed. Done when: a test swapping two names ends with the contents exchanged by hash.
- [ ] Rename in place, or copy or move the renamed files to an output folder from §4's destination rules, with `.xmp` and `.thm` sidecars and `D04 T13 §5` RAW+JPEG partners renamed together and catalog records following (LP-0783). Done when: a test renames a pair with sidecars and the catalog paths and sidecar names match.
- [ ] Add `RenameJournal` in `src/Lumen/Photon.Lumen.Core/FileOps/RenameJournal.cs` and Edit, Undo Rename, which reverses the whole batch as one step and reports names changed outside Lumen since. Done when: `RenameJournalTests` undo a 1,000-file batch and every name, sidecar, and pair is restored.
- [ ] Roll back a batch that fails part-way (a locked file) from the journal, or keep the completed part when the user chooses, reporting the failed file by name. Done when: a test with one locked file offers both and each leaves a consistent folder.
- [ ] Add presets, last used settings, pattern history, and saved rename profiles in `Lumen.Batch.Rename.*` (LP-0776). Done when: a saved profile reloads all ten operations after a restart.
- [ ] Add Library, Rename Photo (`F2`) for one or many selected photos, opening the same dialog pre-filled with a template (LP-0300). Done when: renaming one selected photo with `{capture:yyyyMMdd}-{seq}` updates its file and record.
- [ ] Log one Serilog Information line per rename batch and per file. Done when: a Serilog test sink asserts both lines.
- [ ] Commit fixtures under `tests/fixtures/lumen/rename/` (a mixed folder with sidecars, a RAW+JPEG pair, a swap pair) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/lumen/batch-rename/` and write `docs/user/lumen/batch-rename.md`. Done when: every operation and the preview grid appear in captures and the page documents them.
- [ ] Commit: `"lumen: batch rename with preview, pairs, and undo"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~RenamePipeline|FullyQualifiedName~RenameConflict|FullyQualifiedName~RenameJournal"` exits 0; a driven rename of 1,000 files with sidecars is undone and the before and after listings are quoted equal. Cheaper substitute that fails: renaming the image only, which the sidecar and pair assertions catch.

## 4. Batch Convert

Batch convert turns a folder of anything into the format the user needs: any writable format with its `D04 T13 §6` options, destination rules shared by every runner, overwrite rules, metadata and catalog-field carry-over into the new file, file dates, vector and multi-page sources, page extraction and tiles, and thumbnails saved as files. Outputs are new files by default; the "Replace originals" destination is the operator's opt-in in-place path, offered only when `Lumen.Originals.InPlace.Convert` is on and always through §1's `InPlaceWriter` with its verified backup; removing sources after a conversion moves them to the Recycle Bin only after the output is reread and verified. Catalog: LP-0785 to LP-0797 (13 features: output destination, output format and color conversion, metadata and catalog carry-over, file dates, convert format, overwrite rules, remove originals after conversion, vector and multi-page sources, resize output locations, token-driven folders, recreated folder structure, extract pages and tiles, and thumbnails saved as files). -> SOURCE: parity-lumen-batch-convert

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/batch-convert/`.
**Job:** a user turns a folder of anything into the format they need in one pass and trusts the originals are safe. Consumer: the written files, the catalog when outputs are added, and every runner reusing the destination rules.
**Treatment:** IrfanView's batch conversion output settings (format with Options, output folder, subfolder rules, overwrite choice) and ACDSee's Batch Convert destination and options pages, with the dry-run list before Start. Cheaper substitute that fails the checkpoint: converting into the source folder over files with the same name.
**Chrome:** consume §1, §2, the registry, `D04 T13 §6`'s writers and `SaveOptionsPanel`, and `D01 T04 §1`. Do not add a second destination-rule model in any runner.

**Requires:** display-session -- the convert pages need an interactive desktop

**Freeze check:** Every output is written through `AtomicFileWriter`; an overwrite rule of Replace applies to earlier outputs only and `OriginalGuard` refuses any original; the "Replace originals" destination runs only with `Lumen.Originals.InPlace.Convert` on and goes through `InPlaceWriter`'s verified backup; removing sources recycles them only after the output rereads equal within the format's tolerance, and keeps a source whose metadata the output cannot hold. Fixture source: `tests/fixtures/lumen/convert/` (created by this section).

- [ ] Add `ConvertOperation` in `src/Lumen/Photon.Lumen.Core/Batch/Convert/` (LP-0789, LP-0786): output format and options from `D04 T13 §6`, pixel format, and color space conversion through `D01 T04 §1`. Done when: `ConvertOperationTests` convert every fixture to every writable format and reread each through the registry.
- [ ] Add `DestinationRule` shared by every runner (LP-0785, LP-0793): same as source, a new named subfolder, or a specific folder. Done when: `DestinationRuleTests` assert each rule's output path.
- [ ] Add token-driven output folders such as `{exif:DateTimeOriginal|yyyy}\{exif:DateTimeOriginal|MM}` through §2 (LP-0794). Done when: a test sorts fixtures from two months into two folders.
- [ ] Add recreate the source folder structure under the destination (LP-0795). Done when: a nested fixture tree reproduces its relative paths.
- [ ] Add the "Replace originals" destination, enabled only when `Lumen.Originals.InPlace.Convert` is on: a same-format conversion replaces the original through §1's `InPlaceWriter`; a format change writes the new file beside it and recycles the original only under the verified-removal rule below. Done when: `InPlaceConvertTests` assert the refusal with the key off and, with it on, a verified backup and an atomic replace. Cheaper substitute: overwriting the original directly, which the killed-process test catches.
- [ ] Add overwrite rules (LP-0790): ask, skip, replace, rename, or numbered copy; Replace applies to earlier outputs only. Done when: `OverwriteRuleTests` assert an original can never be replaced by the Replace rule.
- [ ] Carry metadata over into the new file (LP-0787): EXIF, IPTC, XMP, ICC profile, and catalog fields (rating, label, keywords) embedded in the output only. Done when: exiftool 13 reads the rating and keywords from a converted JPEG.
- [ ] Keep or set file dates on outputs (LP-0788): keep the source's last-write time, set it from the capture date, or leave the write time. Done when: each choice's test asserts the output's timestamps.
- [ ] Add remove sources after conversion (LP-0791): opt-in, moves sources to the Recycle Bin (`IFileOperation` with `FOFX_RECYCLEONDELETE`) only after the output is reread and verified, keeping any source whose metadata the output cannot hold. Done when: `RecycleAfterVerifyTests` keep the source when the output is corrupted by a fault injector.
- [ ] Rasterize vector sources (SVG, PDF, EPS) at a set size or DPI (LP-0792). Done when: an SVG converts at the set size.
- [ ] Convert multi-page sources (LP-0792): every page to single files, multi-page to multi-page TIFF, or to one multi-page PDF. Done when: a five-page TIFF converts to a five-page PDF whose pages match within tolerance.
- [ ] Extract pages from multi-page files and export image tiles (rows, columns, overlap) for a selection (LP-0796). Done when: a 3 by 2 tile export writes six files that reassemble to the source exactly.
- [ ] Add "Save each thumbnail as an image file" as a convert source mode reading the preview cache of `D04 T01 §7` (LP-0797). Done when: a test writes one JPEG per cached thumbnail at the cache's size.
- [ ] Add the convert pages in `src/Lumen/Photon.Lumen.Desktop/Views/Batch/ConvertPage.xaml`: format with an Options button opening `SaveOptionsPanel`, destination, overwrite rule, metadata, dates, and the dry-run list before Start. Done when: a driven convert of 50 mixed files shows the dry-run list and the capture is committed.
- [ ] Commit fixtures under `tests/fixtures/lumen/convert/` (mixed formats, a nested tree, a five-page TIFF, an SVG, a corrupt-output fault recipe) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Add `ConvertFidelityTests` (`[Trait("Category", "Fidelity")]`): the converted set rereads through the registry within each format's tolerance and every source's SHA-256 is unchanged. Done when: the test quotes the tolerance per format and the source hashes.
- [ ] Commit captures under `docs/captures/lumen/batch-convert/` and write `docs/user/lumen/batch-convert.md`. Done when: every page and option appears in a capture and the page documents it.
- [ ] Commit: `"lumen: batch convert with safe destinations and verified recycling"`

**Test checkpoint:** Unit test and format fidelity proof: `dotnet test Photon.slnx --filter "FullyQualifiedName~ConvertOperation|FullyQualifiedName~DestinationRule|FullyQualifiedName~OverwriteRule|FullyQualifiedName~RecycleAfterVerify|FullyQualifiedName~InPlaceConvert|FullyQualifiedName~ConvertFidelity"` exits 0 with the originals' hashes quoted unchanged. Cheaper substitute that fails: deleting sources after writing, which the corrupt-output test catches.

## 5. Batch Resize, Rotate, and Flip

Sizing and orienting a whole shoot for a destination is the most common batch after convert. Resize works by dimensions, long or short edge, percentage, megapixels, or print size with fit, stretch, and letterbox, enlarge and reduce rules, the full resampling filter list, and presets; rotate and flip include transpose, transverse, EXIF auto-rotate, and lossless JPEG transforms. This section builds the `LosslessJpegTransform` wrapper over libjpeg-turbo 3.1 and the `OrientationCommand` that the viewer's quick edits (`D04 T04 §11`, `D04 T04 §16`) consume later in the same phase, so neither is built twice. Replacing the original is the operator's opt-in in-place path (`Lumen.Originals.InPlace.Rotate` or `.Save`); otherwise the result is a new file or orientation metadata. Catalog: LP-0798 to LP-0807 (10 features: rotate from the file list, resize sizing, resampling filters, resize modes, rotate and flip, rotate options, replace the original, resize presets, fitting methods, and lossless JPEG transform, crop, and comment). -> SOURCE: parity-lumen-batch-resize

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/batch-resize/` and `docs/captures/lumen/batch-rotate/`.
**Job:** a user sizes and orients a whole shoot for a destination in one step. Consumer: the written files, the catalog's orientation, and the sidecars.
**Treatment:** ACDSee's Batch Resize (percentage, width and height, actual print size, resample filter, fit options, presets with shortcuts) and Batch Rotate/Flip (per-image angle with Next Image, force lossless), and IrfanView's resize fields. Cheaper substitute that fails the checkpoint: pixel rotation that re-encodes JPEGs.
**Chrome:** consume §1, §4's destination rules, `D01 T03 §2`, and libjpeg-turbo 3.1 (already a suite dependency through `D03 T17 §11`). Do not add a second JPEG transform wrapper.

**Requires:** display-session -- the resize and rotate pages need an interactive desktop

**Freeze check:** Lossless transforms and resized outputs write new files through `AtomicFileWriter` unless `Lumen.Originals.InPlace.Rotate` (or `.Save` for resize) is on and the user chose Replace the original, which goes through `InPlaceWriter`'s verified backup; orientation from the file list writes only the catalog and, when enabled, the sidecar. Fixture source: `tests/fixtures/lumen/resize/` (created by this section).

- [ ] Add `ResizeOperation` in `src/Lumen/Photon.Lumen.Core/Batch/Resize/` (LP-0799): width and height, long or short edge, percentage, megapixels, and print size with units and resolution, aspect preserved, fit-within rules. Done when: `ResizeOperationTests` assert every mode's output dimensions on a table.
- [ ] Add resize modes (LP-0801): enlarge only, reduce only, or both; minimum and maximum dimensions; and DPI only, which changes the resolution tag without resampling. Done when: each mode's test row passes and DPI only leaves the pixels bit-exact.
- [ ] Add fitting methods (LP-0806): best fit, stretch to exact size, or letterbox with a color. Done when: a letterboxed output has bars of the chosen color on the expected sides.
- [ ] Map the resampling filters through `D01 T03 §2` (LP-0800): box, triangle, Bell, B-spline, bicubic, Mitchell, Lanczos, and a detail-preserving enlarge filter offered for ACDSee's proprietary ClearIQZ name. Done when: `ResamplingFilterTests` match `D01 T03 §2`'s goldens per filter.
- [ ] Add resize presets with keyboard shortcuts, JPEG options, and remember as default in `Lumen.Batch.Resize.Presets` (LP-0805). Done when: a preset bound to `Ctrl+1` runs from the batch dialog.
- [ ] Add `RotateOperation` (LP-0802): 90, 180, flip horizontal and vertical, transpose, transverse, auto-rotate from EXIF, one angle for all or per image with Next Image. Done when: each transform matches the committed golden exactly.
- [ ] Add `LosslessJpegTransform` in `src/Lumen/Photon.Lumen.Core/Imaging/Jpeg/LosslessJpegTransform.cs` over libjpeg-turbo 3.1's `tjTransform` for rotate, flip, transpose, transverse, and crop, with a perfect or trim choice for partial MCUs. Done when: `LosslessRotateTests` compare scan data byte-identical with `jpegtran` 3.1's output.
- [ ] Add force lossless for JPEG (LP-0803) writing a renamed new file beside the source or to a chosen folder, remember the last rotation, auto-close progress, and save as default. Done when: a forced-lossless rotate of a fixture writes `<name>_rot90.jpg` whose DCT coefficients equal the rotated source's.
- [ ] Add lossless crop and comment on a selection (LP-0807). Done when: a lossless crop aligned to MCUs rereads with unchanged coefficients inside the crop.
- [ ] Add `OrientationCommand` in `src/Lumen/Photon.Lumen.Core/Library/OrientationCommand.cs`: rotate left or right from the file list and the auto-rotate overlay action store the orientation in the catalog and, when sidecars are on, the sidecar, as one undo step; no image file written (LP-0798). Done when: `OrientationCommandTests` rotate, undo, and assert the file's hash unchanged.
- [ ] Offer "Replace the original" (LP-0804) only when `Lumen.Originals.InPlace.Rotate` (rotation) or `.Save` (resize) is on, through §1's `InPlaceWriter`; otherwise the dialog offers a new file or orientation metadata and says why. Done when: a test asserts the refusal text with the key off and a verified backup plus replace with it on.
- [ ] Add the resize and rotate pages in `src/Lumen/Photon.Lumen.Desktop/Views/Batch/ResizePage.xaml` and `RotatePage.xaml` with the Next Image preview. Done when: a driven resize of 200 photos to a 2,048 px long edge is captured with its dry-run list.
- [ ] Commit fixtures under `tests/fixtures/lumen/resize/` (JPEGs with each EXIF orientation, non-MCU-aligned sizes, a 16-bit TIFF) with `reference.txt` naming `jpegtran` 3.1. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/lumen/batch-resize/` and `docs/captures/lumen/batch-rotate/` and write `docs/user/lumen/batch-resize.md`. Done when: every mode and option appears in a capture and the page documents it.
- [ ] Commit: `"lumen: batch resize, rotate, and flip"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ResizeOperation|FullyQualifiedName~ResamplingFilter|FullyQualifiedName~LosslessRotate|FullyQualifiedName~OrientationCommand"` exits 0 with `jpegtran` 3.1's output as the lossless oracle (byte-identical scan data). Cheaper substitute that fails: decode and re-encode rotation, which the coefficient comparison catches.

## 6. Batch Color: Exposure, Profiles, and Color Depth

Evening out a set's brightness or converting a delivery set to a client's profile are batch jobs ACDSee users run weekly: batch adjust exposure with shared or per-image values, batch levels and auto levels, batch tone curves, and batch ICC profile conversion with a rendering intent, each an `IBatchOperation` writing through §4's destinations. Color depth changes (grayscale, palette, 16-bit) are §7's advanced operations. Catalog: LP-0808 to LP-0811 (4 features: batch exposure, batch levels and auto levels, batch tone curves, and batch ICC profile conversion). -> SOURCE: parity-lumen-batch-color

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/batch-color/`.
**Job:** a user evens out a set's brightness or converts a delivery set to a client's profile in one pass. Consumer: the written files and their embedded profiles.
**Treatment:** ACDSee's Batch Adjust Exposure (exposure, contrast, fill light, levels, auto levels, and tone curves tabs with Next Image) and Batch Convert ICC Profile (source or embedded, target, intent). Cheaper substitute that fails the checkpoint: a single brightness slider.
**Chrome:** consume §1, §4, `D01 T03 §4`, `D01 T04 §1`, and `D01 T04 §2`. Do not add a second levels or curves kernel.

**Requires:** display-session -- the color pages need an interactive desktop

- [ ] Add `ExposureOperation` in `src/Lumen/Photon.Lumen.Core/Batch/Color/` (LP-0808): exposure, auto, contrast, and fill light, through `D01 T03 §4`. Done when: `BatchColorOperationTests` match `D01 T03 §4`'s goldens per parameter.
- [ ] Add shared or per-image settings with Next Image: `PerImageSettings` stored in the job so each photo keeps its own values. Done when: a test runs a job where two photos carry different exposures and each output matches its own golden.
- [ ] Add `LevelsOperation` (LP-0809): channel, black, gamma, and white points, a clipping readout, eyedroppers, and auto contrast and auto color with strength and tolerance. Done when: auto levels on the fixture matches `D01 T03 §4`'s auto-levels golden.
- [ ] Add `CurvesOperation` (LP-0810): per channel, over a histogram, stored as control points. Done when: a stored four-point curve reloads and renders identically.
- [ ] Add `IccConvertOperation` (LP-0811) through `D01 T04 §1` and `§2`: the source profile or the embedded one, the target profile, rendering intent, black point compensation, the target embedded, and JPEG options for the output. Done when: `IccConvertOperationTests` compare with lcms2 `transicc` within delta E 0.5.
- [ ] Refuse a missing or unreadable profile by name and a source without an embedded profile by the "assume sRGB" choice the user made. Done when: a test asserts both messages.
- [ ] Add presets for each operation in `Lumen.Batch.Color.Presets`. Done when: a saved exposure preset reloads after a restart.
- [ ] Keep 16-bit and float sources at their depth through the operations, writing the output depth the format allows. Done when: a 16-bit TIFF in and out keeps 16 bits and matches the golden within 1/65535.
- [ ] Add the Batch Adjust Exposure page (exposure, levels, auto levels, and tone curves tabs with Next Image) and the Convert ICC Profile page in `src/Lumen/Photon.Lumen.Desktop/Views/Batch/`. Done when: a driven run on 30 photos shows the per-image preview and the capture is committed.
- [ ] Commit fixtures under `tests/fixtures/lumen/batch-color/` (an sRGB set, an Adobe RGB JPEG, a 16-bit TIFF, a profile-less PNG) with `reference.txt` naming lcms2 `transicc`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/lumen/batch-color/` and write `docs/user/lumen/batch-color.md`. Done when: every tab appears in a capture and the page documents it.
- [ ] Commit: `"lumen: batch exposure, levels, curves, and profile conversion"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~BatchColorOperation|FullyQualifiedName~IccConvertOperation"` exits 0 with delta E quoted against `transicc`. Cheaper substitute that fails: assigning a profile instead of converting, which the delta E check catches.

## 7. The Batch Edit Pipeline

ACDSee's Batch Edit wizard and IrfanView's advanced batch options become one ordered edit profile: rotate and straighten, crop, color cast and white point, channel mixer, sepia, grayscale, negative, exposure, Light EQ, noise removal, sharpening, vignette and frame effects, color depth, auto adjust, brightness, contrast, gamma, saturation, color balance, replace color, blur, median, any registry effect, canvas size and border, DPI, and text and watermark, with a before-and-after preview, output options, progress, a completion log, and saved profiles. Every operation calls the suite pixel engine, the effect registry, or the develop engine; no kernel code lives under `src/Lumen/`. The same operations run the viewer's quick edits (`D04 T04 §11` to `§16`). Light EQ calls the tone equalizer stage `D01 T07 §7`, which ships in Phase 36; until then the operation is listed disabled with a tooltip naming that section. Catalog: LP-0812 to LP-0828, LP-1160 (18 features: the wizard, the preview, output and progress pages, rotate, crop, color, channel mixer and tones, exposure, Light EQ, noise removal, sharpening, vignette and frames, advanced options and order, advanced color and tone, advanced filters, canvas and border, set DPI, and Photoshop-compatible plug-in filters as batch steps). -> SOURCE: parity-lumen-batch-edit

**Corrected 2026-09-27:** at authoring the Light EQ operation was registered disabled until `D01 T07 §7` shipped in Phase 36; the Lumen integration placed `D01 T07 §7` in Phase 23, so this section depends on it and ships the operation enabled.

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/batch-edit/`.
**Job:** a user builds a recipe of edits once, previews it on any photo of the set, and runs it on thousands. Consumer: the written files, the saved profiles, and the viewer's quick edits.
**Treatment:** ACDSee's Batch Edit wizard (operation list with presets, preview with original and final, next and previous image, zoom, fit, actual size, output page, progress page with per-image bars, completion log) with IrfanView's advanced options folded in as operations and a custom processing order. Cheaper substitute that fails the checkpoint: a fixed operation order.
**Chrome:** consume §1, §5, §6, §8, the effect registry (`D01 T06 §1`), `D01 T03`, and `D01 T07 §7`. Do not reimplement a kernel in Lumen.

**Requires:** display-session -- the wizard and preview need an interactive desktop

**Freeze check:** The pipeline renders from a decoded copy and writes every output through §4's destination rules and `AtomicFileWriter`; the in-place destination runs only under §1's `OriginalWritePolicy`; the preview never writes. Fixture source: `tests/fixtures/lumen/batch-edit/` (created by this section).

- [ ] Add `EditProfile` in `src/Lumen/Photon.Lumen.Core/Batch/Edit/EditProfile.cs`: ordered operations with parameters, saved in `Lumen.Batch.EditProfiles`, exported and imported as JSON (LP-0812, LP-0824). Done when: a profile round-trips through JSON and runs identically.
- [ ] Add the custom processing order: drag to reorder operations, applied strictly in list order (LP-0824). Done when: `EditProfileTests` assert that crop-then-resize and resize-then-crop give the two expected sizes.
- [ ] Add the wizard in `src/Lumen/Photon.Lumen.Desktop/Views/Batch/BatchEditWizard.xaml`: operations with presets, preview, output, progress, and log pages (LP-0812). Done when: a driven wizard run is captured page by page.
- [ ] Add the preview (LP-0813): original and final side by side, next and previous image, zoom, fit, actual size, rendered at screen size and cancelled on change. Done when: `EditPreviewTests` assert the preview equals the full render downscaled within 1/255.
- [ ] Add the output page, the progress page with per-image bars, the completion log, browse output in Explorer or Lumen, and save as preset (LP-0814). Done when: a driven run's log names every output and skip.
- [ ] Add rotate with presets, custom angle, background color, straighten by a drawn line, automatic crop, and reset (LP-0815), through `D01 T03 §2`. Done when: a straighten by a drawn 3-degree line matches the rotation golden.
- [ ] Add crop by proportion or custom area with automatic, landscape, or portrait orientation, by x, y, width, and height from a corner or the center, and from the current selection (LP-0816). Done when: each mode's test row asserts the crop rectangle.
- [ ] Add canvas size and border or frame (LP-0827) and set DPI (LP-0828). Done when: a 20 px border output measures its size and DPI only changes the resolution tag.
- [ ] Add color cast removal with a picked neutral, white point presets, strength, temperature, tint, and saturation (LP-0817) through `D01 T03 §5`. Done when: the operation matches `D01 T03 §5`'s goldens.
- [ ] Add channel mixer grayscale, sepia, grayscale, and negative (LP-0818) through `D01 T03 §5`. Done when: each matches its golden.
- [ ] Add exposure, contrast, fill light, brightness, and gamma with the exposure warning (LP-0819) through `D01 T03 §4`. Done when: each matches its golden.
- [ ] Add `LightEqOperation` (LP-0820): automatic per image, brighten and darken with compression and amplitude, and the exposure warning, calling the tone equalizer stage of `D01 T07 §7` (built in Phase 23) through `ToneEqualizerModes` and `AutoToneEqualizer`. Done when: `LightEqOperationTests` assert automatic mode applies the settings `AutoToneEqualizer` computes for each image and a brighten run renders equal to the stage within 1/255.
- [ ] Add IrfanView's color depth (through `D01 T03 §3`), auto adjust, brightness, contrast, gamma, saturation, color balance, and replace color (LP-0825). Done when: each matches its engine golden.
- [ ] Add noise removal (despeckle, square, X, plus, hybrid, with luminance and color amounts and presets) (LP-0821) and sharpening (amount, radius, threshold) (LP-0822) through `D01 T03 §6`. Done when: each matches `D01 T03 §6`'s goldens.
- [ ] Add vignette with a focal point, clear and transition zones, round or rectangular shape, and outline, and the frame effects (color, saturation, blur, clouds, edges, radial waves, radial and zoom blur, crayon edges) through the effect registry (LP-0823). Done when: each frame effect resolves to a registry effect id and matches its golden.
- [ ] Add blur, median, and any registry effect chosen from the effects browser (LP-0826) through `D01 T06 §1`. Done when: a profile holding a registry effect by id runs and matches the registry's golden.
- [ ] Include §8's text overlay and watermark operations in the list. Done when: a profile with a caption and a logo renders both.
- [ ] Add a guard test that scans `src/Lumen/` for pixel-kernel code (per-pixel loops over `ImageBuffer` spans outside `Photon.Core`). Done when: the test fails on a planted loop.
- [ ] Commit fixtures under `tests/fixtures/lumen/batch-edit/` (a 200-photo generated set recipe and eight-operation profiles) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/lumen/batch-edit/` and write `docs/user/lumen/batch-edit.md`. Done when: every operation and page appears in a capture and the page documents it.
- [ ] Add `PluginFilterOperation` (LP-1160): a batch step that runs a chosen 8BF or Filter Factory filter through `D01 T09 §2`'s `PluginHostClient` with the `FilterParameterBlob` recorded when the user set it up once (no dialog per file), x86 filters in the x86 host, and a crashed or hung filter recorded as a per-file skip with the host restarted, never stopping the job; JewelScript effects and a Lumen plug-in SDK stay in B-041. Done when: `PluginFilterOperationTests` run the committed parameterized test filter over three fixtures with identical output per file, and a crashing test filter skips its file with the reason while the others complete.
- [ ] Commit: `"lumen: the batch edit pipeline"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~EditProfile|FullyQualifiedName~EditPreview|FullyQualifiedName~BatchEditOperation"` exits 0 with each operation matching its engine golden; a driven profile of eight operations runs on 200 photos with the completion log and captures quoted. Cheaper substitute that fails: operations reimplemented in Lumen, which the kernel guard test exposes.

## 8. Text Overlays and Watermarks

A caption or a logo stamped on many photos, and the same stamp on export, in slideshows, and in print, needs one overlay engine: text with font, style, rotation, size, color, opacity, alignment, symbols, and tokens, a box with border, fill, bevel, shadow, and blend mode, and image watermarks with keyed or alpha transparency, positioned in pixels or percent from an anchor. Text is shaped by the suite text engine, never drawn by GDI. Catalog: LP-0829 to LP-0833 (5 features: text overlay, the overlay box, image watermark, IrfanView's advanced text and watermark, and IrfanView's insert text). -> SOURCE: parity-lumen-overlays

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/overlay-editor/`.
**Job:** a user stamps a caption or logo on many photos exactly where they want it and reuses it on export. Consumer: batch outputs, export (`D04 T12 §13`), the viewer (`D04 T04 §13`), slideshows, and print.
**Treatment:** ACDSee's Batch Edit Text Overlay and Watermark pages and IrfanView's Insert text and Watermark dialogs (start corner, offsets, rectangle size, font scaled to desktop height), with a live preview on a sample photo. Cheaper substitute that fails the checkpoint: text drawn by GDI without shaping.
**Chrome:** consume §2, `Photon.Core/Text/` (the HarfBuzz engine moved by `D03 T16 §1`), `D01 T03` blend math, and `Photon.UI` dialogs. Do not add a second overlay renderer in export or the viewer.

**Requires:** display-session -- the overlay editor needs an interactive desktop

- [ ] Add `OverlaySpec` in `src/Lumen/Photon.Lumen.Core/Overlays/OverlaySpec.cs`: text and image layers, anchor, offsets in pixels or percent, and scale relative to the image or to the desktop height, with JSON presets in `Lumen.Overlays.Presets`. Done when: a spec round-trips through JSON unchanged.
- [ ] Add text layers (LP-0829): font, style, rotation, size, color, opacity, alignment, a symbol picker, and §2 tokens evaluated per image, shaped through `Photon.Core/Text/`. Done when: an Arabic and a Latin caption render to their committed goldens.
- [ ] Add the box (LP-0830): offsets, border and fill with transparency, bevel, drop shadow, and a blend mode for box and text through `D01 T03`'s blend math. Done when: each blend mode matches its golden.
- [ ] Add image watermarks (LP-0831): a file, keep aspect when resizing, the alpha channel or a keyed transparent color with tolerance, position, blend mode, and opacity. Done when: a keyed-white logo on the fixture matches the golden within 1/255.
- [ ] Map IrfanView's insert text and watermark (LP-0832, LP-0833): start corner, offsets, rectangle size, placeholders, and font scaled to the desktop height. Done when: a spec built from IrfanView's example values places the text within 1 px of the golden.
- [ ] Add `OverlayRenderer.Render(ImageBuffer, OverlaySpec, TokenContext)` and the `TextOverlayOperation` and `WatermarkOperation` batch operations over it. Done when: `OverlayRendererTests` assert placement at each of the nine anchors within 1 px.
- [ ] Refuse a missing font (substituting nothing silently) and a missing watermark file by name before the run, in §1's dry run. Done when: the dry run lists both refusals.
- [ ] Add the overlay editor in `src/Lumen/Photon.Lumen.Desktop/Views/Overlays/OverlayEditor.xaml` with a live preview on a sample photo. Done when: a driven edit moves the anchor and the preview follows, captured.
- [ ] Add a guard test that `OverlayRenderer` is the only overlay renderer under `src/Lumen/`. Done when: the test fails on a planted second renderer.
- [ ] Commit fixtures under `tests/fixtures/lumen/overlays/` (sample photos, a logo with alpha, a keyed logo, the goldens) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/lumen/overlay-editor/` and write `docs/user/lumen/overlays.md`. Done when: the editor and a stamped sample appear in captures and the page documents every option.
- [ ] Commit: `"lumen: one text overlay and watermark engine"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~OverlayRenderer|FullyQualifiedName~OverlaySpec"` exits 0 with placement, blend, opacity, and per-image token text asserted against goldens; a driven batch stamps 100 photos with a token caption and a logo and a sample is captured. Cheaper substitute that fails: a second renderer inside export, which the single-renderer guard test exposes.

## 9. Batch Develop and Batch Export

Photographers apply a look to a whole shoot and deliver several sizes and formats without babysitting: develop presets apply to many photos as a background job (RAW included), optionally exported with the full export options, and batch export writes several outputs per photo in one queued pass with one decode. A preset applied while exporting or converting changes only a temporary copy of the settings. Files that are not yet in the catalog get their records through a resolver interface that `D04 T05 §1` implements for browsed files. Catalog: LP-0834 to LP-0838, LP-0978 (6 features: presets across many photos, multi-output export, a preset while exporting or converting, batch develop then export, a preset as a background job, and a preset over RAW files from browse). -> SOURCE: parity-lumen-batch-develop

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/batch-develop/`.
**Job:** a user applies a look to a whole shoot and delivers several sizes and formats without babysitting. Consumer: the photos' edit stacks and the exported files.
**Treatment:** ACDSee's Batch Develop (preset, apply only or apply and export) and Batch Export (multiple output rows), and Lightroom's apply-preset-to-selection. Cheaper substitute that fails the checkpoint: one export run per output size.
**Chrome:** consume `D04 T02 §5` presets, `D04 T02 §6`'s `ExportRunner`, and §1. Do not add a second export runner.

**Requires:** display-session -- the batch develop and export pages need an interactive desktop

**Freeze check:** Batch develop writes only edit stacks in the catalog (and sidecars when enabled), recorded as one undo step; exports are new files through §4's destination rules and `AtomicFileWriter`; no source file is opened for writing. Fixture source: `tests/fixtures/lumen/batch-develop/` (created by this section).

- [ ] Add `ApplyPresetOperation` in `src/Lumen/Photon.Lumen.Core/Batch/Develop/` (LP-0834, LP-0838): apply a `D04 T02 §5` preset to each photo's edit stack as a background job in §1, recorded as one undo step for the whole batch. Done when: `BatchDevelopTests` apply a preset to 50 stacks and one undo restores all of them.
- [ ] Add `ICatalogRecordResolver` so the operation accepts files without a catalog record (LP-0978), which `D04 T05 §1` implements to create browsed records; until then paths outside the catalog are skipped with the reason "not in the catalog". Done when: a test with a stub resolver applies a preset to a RAW file outside the catalog and its new record holds the stack.
- [ ] Add batch develop then export (LP-0837): the preset plus the full `D04 T02 §6` export options in one job. Done when: a job applies and exports ten RAW files and each export matches a single export of the same settings.
- [ ] Apply a preset while exporting or converting (LP-0836) to a temporary settings copy, leaving the edit stack unchanged. Done when: a test asserts the stack's hash before and after an export with a preset.
- [ ] Extend `ExportRunner` to take several output specs (folder, naming, format, size) per photo with one decode (LP-0835). Done when: `MultiOutputExportTests` count one decode per photo for three outputs and reread each output.
- [ ] Keep outputs already written when a job is cancelled, list the rest as not started, and leave applied stacks as the one undo step. Done when: a cancel at 50 percent is asserted by the history's per-file rows.
- [ ] Add the Batch Develop page (preset, apply only or apply and export) and the Batch Export page with output rows in `src/Lumen/Photon.Lumen.Desktop/Views/Batch/`. Done when: a driven batch develop of 300 RAW files with three outputs each is captured with timing quoted.
- [ ] Commit fixtures under `tests/fixtures/lumen/batch-develop/` (a RAW set recipe and a preset) with `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit captures under `docs/captures/lumen/batch-develop/` and write `docs/user/lumen/batch-develop.md`. Done when: both pages appear in captures and the page documents them.
- [ ] Commit: `"lumen: batch develop and multi-output export"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~BatchDevelop|FullyQualifiedName~MultiOutputExport"` exits 0 with the one-undo and one-decode assertions; a driven batch develop of 300 RAW files with three outputs each runs with timing quoted. Cheaper substitute that fails: decoding once per output, which the decode counter in `MultiOutputExportTests` catches.

## 10. The Batch Dialog: File Lists, Profiles, and Running from Explorer and the Viewer

IrfanView users start a batch from wherever they are, including Explorer's context menu, without opening a library. One batch dialog assembles a file list, works in convert, rename, or convert-and-rename mode, saves and applies batch presets, and opens from the Batch menu with the selection, from the viewer's `B` key, and from an Explorer verb that needs no shell extension DLL. Catalog: LP-0839 to LP-0846 (8 features: the Batch menu, tag-then-batch, presets, the image list, opening from the viewer, work modes, the progress dialog and last folder, and Explorer's context menu). -> SOURCE: parity-lumen-batch-dialog

**Fidelity:** new build, no baseline; captured to `docs/captures/lumen/batch-dialog/`.
**Job:** a user starts any batch from wherever they are, including Explorer, without opening the library. Consumer: §1's jobs and the files they write.
**Treatment:** IrfanView's Batch Conversion/Rename dialog (work as convert, rename, or both; input list with sort and preview; output settings; start with a progress dialog) and ACDSee's Batch menu with the tag-then-batch workflow. Cheaper substitute that fails the checkpoint: batch only from the library selection.
**Chrome:** consume §1 to §9, `D01 T02 §3` forwarding, and the registry. Do not add a second file-list model; `D04 T05 §8` reads and writes the same text lists.

**Requires:** display-session -- the dialog and the Explorer verb need an interactive desktop

- [ ] Add the Batch menu with one command per tool, each starting with the current selection (LP-0839). Done when: a driven Batch, Resize on 20 selected photos opens the dialog with 20 files.
- [ ] Add tag-then-batch (LP-0840): Tag with `` ` `` in the grid, then Batch, Tagged Files runs any tool, including renaming non-image files. Done when: a test tags three files including a `.txt` and a rename job lists all three.
- [ ] Add `BatchFileList` in `src/Lumen/Photon.Lumen.Core/Batch/BatchFileList.cs` (LP-0842): add and remove, add all, include subfolders, and preview the selected entry. Done when: `BatchFileListTests` add a folder with subfolders and count its images.
- [ ] Load and save the list as a UTF-8 text file of paths, one per line, in the format `D04 T05 §8` shares (LP-0842). Done when: a round trip keeps order and non-ASCII paths.
- [ ] Sort the list by name, date, size, extension, or EXIF date (LP-0842). Done when: each sort order's test row passes.
- [ ] Add the work modes convert, rename, and convert and rename, each composing §3 and §4 operations in one job (LP-0844). Done when: `BatchModeTests` assert the composed operations per mode.
- [ ] Add batch presets (LP-0841): save, update, delete, apply several export presets together, and convert presets bound to shortcuts, in `Lumen.Batch.Presets`. Done when: applying two export presets together queues one job with two outputs per file.
- [ ] Open the dialog from the viewer with `B` and the viewer's folder list through `D04 T04 §1`'s hand-off (LP-0843). Done when: a driven `B` in the viewer opens the dialog listing the folder.
- [ ] Start with a progress dialog (auto-close option) and remember the last batch folders in `Lumen.Batch.LastFolders` (LP-0845). Done when: the last output folder is preselected after a restart.
- [ ] Parse `Lumen.exe --batch @listfile` (and `--batch <paths>`) into a file list, merging invocations that arrive within 500 ms through `D01 T02 §3` forwarding. Done when: `ExplorerVerbTests` parse a list file and merge three invocations into one list.
- [ ] Register a "Convert with Lumen" static verb for image types (LP-0846) in the installer task of `D04 T04 §3`, with `MultiSelectModel=Player` so the selection arrives as one invocation (Microsoft Learn, "Verbs and File Associations"); no shell extension DLL. Done when: a driven Explorer right-click convert of 50 files queues one job, captured with the Activity Manager entry. Cheaper substitute: a verb that opens the library only, which the driven run catches.
- [ ] Commit captures under `docs/captures/lumen/batch-dialog/` and write `docs/user/lumen/batch.md` covering every entry point. Done when: the dialog, each mode, and the Explorer verb appear in captures and the page documents them.
- [ ] Commit: `"lumen: the batch dialog, reachable from Explorer and the viewer"`

**Test checkpoint:** Unit test and driven run: `dotnet test Photon.slnx --filter "FullyQualifiedName~BatchFileList|FullyQualifiedName~BatchMode|FullyQualifiedName~ExplorerVerb"` exits 0; a driven Explorer right-click convert of 50 files is captured with its Activity Manager entry. Cheaper substitute that fails: a verb that opens the library only, which the driven run catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "FullyQualifiedName~Batch|FullyQualifiedName~Token|FullyQualifiedName~Rename|FullyQualifiedName~Overlay"` exits 0 with this file's test classes reporting
- [ ] `BatchGuardTests.SourcesUnchanged` passes with every in-place key off, and `InPlaceWriterTests` pass their killed-process cases
- [ ] The single-engine guard tests (tokens, overlays, pixel kernels) pass
- [ ] `python scripts/todo-graph.py validate` clean
