---
schema_version: 1
id: lumen-develop
domain: 04-lumen
status: draft
title: "TODO-02 -- Lumen: Non-Destructive Develop, Export, and 0.1.0"
depends_on: []
frozen: true
track: L2
---

# TODO-02 -- Lumen: Non-Destructive Develop, Export, and 0.1.0

> **Goal:** A Lumen user develops RAW and JPEG photos non-destructively (white balance, exposure, contrast, highlights and shadows, whites and blacks, tone curve, vibrance and saturation, crop and straighten), copies settings across a batch, exports finished files with size, format, color space, and metadata choices, hands a photo to Imago when Imago is installed, and gets all of it as `lumen-v0.1.0`, with the original never written.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Nothing exists: no develop code, no pipeline, no export. The Lumen notes removed on 2026-09-26 asked for "RAW processing and non-destructive editing", "batch adjustments and presets", and "Edit In (send to Imago)" with no technical choices. `standards/lumen.md` sets the contract this file builds to: edits are data in the catalog, the pipeline is float32 linear-light with one output transform at the end, previews and exports of the same settings agree within a stated tolerance, and "Edit in Imago" never loads Imago's assemblies.
<!-- claim: count "Float32 linear-light" standards/lumen.md = 1 -->
<!-- claim: absent src/Lumen/Photon.Lumen.Core/Develop -->

## Inputs

- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard, the pipeline, the hand-off rules
- The competitor survey (`docs/dev/lumen/competitor-survey.md`, from `D04 T01 §1`) -- the develop controls and their order in darktable and Lightroom Classic, which the develop panel matches where they agree
- darktable and LibRaw's `dcraw_emu` -- reference renders for the pipeline goldens, versions recorded
- -> XREF: D04 T01 §5 -- the catalog where §1 stores edit stacks
- -> XREF: D03 T06 §3 -- the Imago release §7 hands photos to
- -> XREF: D06 T01 §3 -- the Lumen user guide §8 requires

## Outcome

- Every develop change is a versioned entry in the catalog's edit stack; undo, redo, history steps, snapshots, and "reset" work per photo; the original is never opened for writing.
- The develop pipeline renders previews under 150 ms for a 24-megapixel RAW on the development machine and full-resolution exports matching the preview within 1/255 at equal scale.
- The develop panel shows a live histogram, before and after, and every control in the Treatment below, keyboard operable.
- Presets, copy and paste settings, and sync apply develop settings to many photos at once, each undoable.
- Export writes JPEG, TIFF (8 or 16 bit), and PNG with resize, sharpening for screen or print, color space (sRGB, Display P3, Adobe RGB), metadata choices, and file naming, in the background with progress.
- "Edit in Imago" renders a 16-bit TIFF, opens it in Imago when installed, and stacks the result beside the original; when Imago is absent the command is disabled with a tooltip saying so.
- `lumen-v0.1.0` is a published release that passes `standards/release.md`.

**Adjacency:** list=not-applicable (the grid in D04 T01 §8 is the list); document=applicable @ D04 T02 §6; settings=applicable @ D04 T02 §5; reporting=applicable; notifications=applicable; permissions=applicable; audit=applicable; exchange=applicable; reverse=applicable @ D04 T02 §1

**Adjacency rationale:** Exports are the documents users carry; presets are settings; the histogram is the develop panel's report; export progress and completion notify; a read-only export folder is refused; the edit stack is both the audit and the reverse; the Imago hand-off is an exchange.

## Implementation Order

| Order | Section | Deliverable                                       | Depends On                                                   | Status |
| :---: | :-----: | ------------------------------------------------- | ------------------------------------------------------------ | :----: |
|   1   |   §1    | The edit stack                                    | D04 T01 §5                                                   |  [ ]   |
|   2   |   §2    | The develop pipeline                              | §1, D04 T01 §4                                               |  [ ]   |
|   3   |   §3    | The develop panel                                 | §2, D04 T01 §9                                               |  [ ]   |
|   4   |   §4    | Crop and straighten                               | §3                                                           |  [ ]   |
|   5   |   §5    | Presets, copy and paste settings, and sync        | §3                                                           |  [ ]   |
|   6   |   §6    | Export                                            | §2, D04 T01 §10                                              |  [ ]   |
|   7   |   §7    | Edit in Imago                                     | §6, D03 T06 §3                                               |  [ ]   |
|   8   |   §8    | Lumen 0.1.0                                       | §4, §5, §7, D04 T01 §11, D06 T01 §3, D05 T01 §1              |  [ ]   |

---

## 1. The Edit Stack

Non-destructive means edits are data. Each photo has an edit stack in the catalog: an ordered list of versioned settings changes, with snapshots and a pointer to the current step. Rendering reads the settings at the current step; nothing reads or writes the original except the decoder, read-only. -> SOURCE: lumen-notes-develop-stack

**Freeze check:** No develop, undo, snapshot, preset, or sync operation opens an original for writing; a test runs a full session (develop, undo, snapshot, sync to ten photos, export) over the import fixtures and asserts every original's SHA-256 and last-write time are unchanged. Fixture source: `tests/fixtures/lumen/import/`.

- [ ] `DevelopSettings` (an immutable record with every parameter the pipeline reads, with defaults and a schema version) and `EditStack` (append, undo, redo, jump to step, named snapshots, reset) in `Photon.Lumen.Core/Develop/`, persisted in the catalog. Done when: `EditStackTests` cover each operation and survive a catalog reopen.
- [ ] Settings changes from sliders merge within a 1-second window into one step (as Nodus's property edits do). Done when: a scrub test yields one step.
- [ ] One Information log line per committed step (`Develop {Photo}: {Parameter} {Old} to {New}`). Done when: a test logger asserts it.
- [ ] Commit: `"lumen: a versioned, non-destructive edit stack per photo"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `EditStackTests` and the full-session unchanged-originals test reporting. Cheaper substitute that fails: storing the latest settings only, which cannot undo.

## 2. The Develop Pipeline

The pipeline turns a decoded RAW (or a JPEG converted to linear) plus `DevelopSettings` into pixels: white balance, exposure, highlights and shadows, whites and blacks, contrast, tone curve, vibrance and saturation, then the output transform. Float32 linear light throughout, CPU with SIMD, tile-parallel, cancellable. -> SOURCE: lumen-notes-develop-pipeline

- [ ] Implement each stage as a pure function over float32 tiles in `Photon.Lumen.Core/Develop/Pipeline/`, with a scalar reference per stage. Done when: SIMD and scalar outputs match within 1e-5 per stage.
- [ ] White balance from the camera's as-shot values and from temperature and tint (Kelvin to camera multipliers through the decoder's matrix). Done when: a gray-card fixture renders neutral within delta E 2 at its as-shot setting.
- [ ] Output transform to sRGB, Display P3, and Adobe RGB (matrix plus transfer function), with ICC profiles embedded on export. Done when: a test asserts known primaries map correctly.
- [ ] `DevelopPipelineFidelityTests` (`[Trait("Category", "Fidelity")]`): at default settings, the render of each corpus file is compared with `dcraw_emu` at matching white balance and output space within a stated tolerance; with a fixed settings set, the render of the committed DNG is compared with a committed golden. Done when: every comparison reports.
- [ ] Preview rendering at screen resolution from a cached, downscaled demosaic, under 150 ms for a 24-megapixel file after the first decode (measured). Done when: the timing is quoted.
- [ ] Commit: `"lumen: a float32 develop pipeline with fidelity goldens"`

**Test checkpoint:** `dotnet test Photon.slnx --filter "Category=Fidelity"` prints a result per file with its tolerance; the preview timing is quoted with the machine. Cheaper substitute that fails: developing 8-bit JPEG previews, which clips highlights the goldens keep.

## 3. The Develop Panel

The develop module is where the pipeline meets the photographer: the photo large in the center, controls on the right in the order the competitors agree on, a live histogram, and before and after. -> SOURCE: lumen-notes-develop-panel

**Fidelity:** Lumen develop module -- new build, no baseline; follows the window anatomy in `standards/shared.md` and the control order recorded in `docs/dev/lumen/competitor-survey.md`, captured to docs/captures/lumen/develop/.
**Job:** a photographer can adjust a photo's tone and color with immediate visual feedback and compare against the original. Consumer: the edit stack and the pipeline.
**Treatment:** a histogram (RGB and luminance, clipping indicators toggled by J); Basic panel (white balance presets, temperature, tint, exposure, contrast, highlights, shadows, whites, blacks, vibrance, saturation); Tone Curve (parametric and point); a History list and Snapshots; before and after with \ (toggle) and Y (side by side); double-click a slider resets it; Alt-drag on exposure or blacks shows clipping; every slider keyboard adjustable. Cheaper substitute that fails the checkpoint: sliders that apply only on release with no live preview.
**Chrome:** consume the histogram control from Imago moved to `Photon.UI` (filed through `add-todo` when this section starts, since two apps then need it), the theme, and the keymap pattern.

**Requires:** display-session -- the develop module needs an interactive desktop

- [ ] `DevelopViewModel` binding every control to `DevelopSettings` through the edit stack, with preview requests debounced and cancelled on change. Done when: `DevelopViewModelTests` cover reset, merge, and cancellation.
- [ ] The module view with histogram, panels, history, snapshots, and before and after. Done when: captures of each are committed.
- [ ] Update the Lumen user guide's develop page. Done when: every control is described.
- [ ] Commit: `"lumen: the develop module with live preview and history"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `DevelopViewModelTests` reporting; a driven session adjusts exposure by scrubbing, sees the preview follow (frame timing quoted), undoes, and the catalog's step count is one per gesture. Cheaper substitute that fails: apply-on-release sliders.

## 4. Crop and Straighten

Crop, aspect ratios, and straightening are develop settings like any other: stored in the stack, applied at render, never cutting the original. -> SOURCE: lumen-notes-develop-crop

**Fidelity:** Crop overlay -- new build, no baseline; captured to docs/captures/lumen/crop/.
**Job:** a photographer can crop to an aspect ratio and level the horizon, and undo it any time. Consumer: the pipeline and export.
**Treatment:** R enters crop with a rule-of-thirds overlay, aspect presets (original, 1:1, 4:3, 3:2, 16:9, custom), X swaps orientation, an angle slider and a straighten tool (draw along the horizon), Enter commits one step. Cheaper substitute that fails the checkpoint: a crop that resamples the stored preview.
**Chrome:** consume the edit stack and the develop module.

**Requires:** display-session -- the crop overlay needs an interactive desktop

- [ ] Crop and rotation parameters in `DevelopSettings` and the pipeline (applied after demosaic, bicubic resampling). Done when: a test asserts output dimensions for each aspect preset.
- [ ] The crop overlay and straighten tool. Done when: a driven straighten of a tilted fixture yields a level horizon within 0.2 degrees.
- [ ] Commit: `"lumen: non-destructive crop and straighten"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the crop tests reporting; the straighten result is quoted. Cheaper substitute that fails: cropping the preview JPEG.

## 5. Presets, Copy and Paste Settings, and Sync

Batch work is half of Lumen's job: apply a look to hundreds of photos, copy one photo's white balance to its neighbors, and save favorite settings as presets. -> SOURCE: lumen-notes-develop-batch

**Fidelity:** Presets panel and the Copy Settings dialog -- new build, no baseline; captured to docs/captures/lumen/presets/.
**Job:** a photographer can apply saved or copied settings to many photos in one action and undo it. Consumer: the edit stacks of the selected photos.
**Treatment:** a Presets panel (user presets in the app-data folder as JSON with a schema version, hover preview on the current photo); Ctrl+Shift+C opens a checklist of settings groups to copy, Ctrl+Shift+V pastes to the selection; Sync applies the active photo's chosen groups to the selection; each batch is one undo step across all photos. Cheaper substitute that fails the checkpoint: presets that overwrite every setting.
**Chrome:** consume the edit stack, the grid selection, and the settings store.

**Requires:** display-session -- the presets panel needs an interactive desktop

- [ ] Preset storage with versioning and partial application by settings group. Done when: tests apply a white-balance-only preset leaving exposure unchanged.
- [ ] Copy, paste, and sync with batch undo. Done when: undo after syncing 50 photos restores all 50 (test).
- [ ] Commit: `"lumen: presets, copy and paste settings, and sync"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the preset and sync tests reporting; a driven sync to 100 photos completes with progress and a single undo entry. Cheaper substitute that fails: per-photo undo entries for a batch.

## 6. Export

Export is how developed photos leave Lumen: rendered at full resolution through the same pipeline, resized, sharpened for their destination, tagged with a color space, written atomically, in the background. -> SOURCE: lumen-notes-export

**Fidelity:** Export dialog -- new build, no baseline; captured to docs/captures/lumen/export/.
**Job:** a photographer can export a selection to files ready for the web, print, or another editor, and keep working meanwhile. Consumer: the exported files.
**Treatment:** an Export dialog with target folder and subfolder, file naming template (`{date}-{name}-{seq}`), format (JPEG quality, TIFF 8 or 16 bit with compression, PNG), resize (long edge, short edge, megapixels, percentage; don't enlarge), output sharpening (screen, matte paper, glossy paper; low, standard, high), color space, metadata (all, copyright only, none; remove location), and saved export presets; exports run in the background with progress, Cancel, and a completion notification listing failures with reasons; an existing file is never overwritten without choosing Overwrite, Skip, or Unique name. Cheaper substitute that fails the checkpoint: exporting the cached preview JPEG.
**Chrome:** consume the pipeline, `AtomicFileWriter`, the settings store, and the theme.

**Requires:** display-session -- the export dialog needs an interactive desktop

- [ ] `ExportRunner` with the options above, rendering full resolution per photo, cancellable, writing through `AtomicFileWriter`. Done when: `ExportTests` cover each format, resize mode, naming collision choice, a read-only target folder (refused by name), and cancel leaving no partial file.
- [ ] Export fidelity: a full-resolution export of the committed DNG at fixed settings compares with the pipeline golden within 1/255 (8-bit) after the stated resize. Done when: the test passes.
- [ ] The dialog, presets, and background progress with a completion summary. Done when: a driven export of 200 photos shows progress and the summary (time quoted).
- [ ] Commit: `"lumen: export with sizing, sharpening, color space, and metadata choices"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with `ExportTests` and the export fidelity test reporting; the 200-photo timing is quoted; the unchanged-originals assertion holds after export. Cheaper substitute that fails: exporting previews, which the fidelity comparison catches at full resolution.

## 7. Edit in Imago

Lumen is the bridge from the camera to Imago, and the suite's rule is that no app needs another at runtime. So the hand-off is over files: Lumen renders a 16-bit TIFF, asks Windows to open it with Imago if Imago is installed, and watches for the edited file to come back. -> SOURCE: lumen-notes-edit-in

**Fidelity:** Photo, Edit In menu -- docs/captures/lumen/develop/.
**Job:** a photographer can take a developed photo into Imago for pixel work and see the result back in the library. Consumer: Imago (through the file) and the catalog.
**Treatment:** Photo, Edit In, Imago (Ctrl+E) renders a 16-bit ProPhoto or Adobe RGB TIFF (a setting) named `<name>-Edit.tif` beside the original's folder in Lumen's working location, locates Imago through its App Paths registry entry (`HKCU` then `HKLM\Software\Microsoft\Windows\CurrentVersion\App Paths\Imago.exe`, written by the Imago installer), starts it with the path, and adds the TIFF to the catalog stacked with the original; when the file changes on disk the thumbnail refreshes. When Imago is not found, the menu item is disabled with the tooltip "Install Imago to edit photos in it." Cheaper substitute that fails the checkpoint: referencing Imago's assemblies.
**Chrome:** consume the export runner, a `FileSystemWatcher`, and the catalog's stacking.

**Requires:** display-session -- the hand-off drive needs an interactive desktop

- [ ] Confirm or add the App Paths entry in `installer/Imago.iss` (and document it in `docs/dev/build.md`). Done when: after installing Imago, `reg query` shows the entry.
- [ ] `EditInService` (render, locate, launch, stack, watch) with tests using a fake locator and launcher. Done when: tests cover found, not found, and the file-changed refresh.
- [ ] Stacks in the catalog (a stack groups an original and its derivatives; the grid shows a stack badge and expands with S). Done when: the edited TIFF appears stacked.
- [ ] Commit: `"lumen: Edit in Imago over files, never over assemblies"`

**Test checkpoint:** `dotnet test Photon.slnx` exits 0 with the `EditInService` tests reporting; on a machine with Imago installed, a driven Edit In opens the TIFF in Imago, a brush stroke saved in Imago refreshes the thumbnail in Lumen (captures); with Imago uninstalled, the item is disabled with its tooltip; `Photon.Lumen.*.csproj` files reference no Imago project (grep quoted). Cheaper substitute that fails: a project reference to Imago.

## 8. Lumen 0.1.0

Lumen's first release, following `standards/release.md` as Nodus and Imago did, with the original-file guard proven once more on the installed build.

**Needs:** Clean Windows machine (no .NET SDK)

- [ ] `pwsh scripts/check-all.ps1` at the release commit. Done when: every gate is `PASS` (table quoted).
- [ ] Write the `lumen-v0.1.0` section of `CHANGELOG.md`. Done when: it lists every user-visible feature.
- [ ] Confirm the user guide covers every surface. Done when: no surface lacks a page.
- [ ] Package and run the clean-machine procedure from `D05 T01 §1`, including an import of a copied fixture folder, a develop, an export, and a hash check that the originals are unchanged. Done when: every step passes and is quoted.
- [ ] Push `lumen-v0.1.0`; verify the workflow, assets, and `SHA256SUMS`; run the portable ZIP from an empty folder. Done when: all pass (URLs and hashes quoted).
- [ ] Update `README.md`'s Lumen status line. Done when: it names 0.1.0.
- [ ] Commit: `"release: Lumen 0.1.0"`

**Requires:** display-session -- launching the installed app on the clean machine needs an interactive desktop

**Test checkpoint:** `gh release view lumen-v0.1.0 --json isPrerelease,assets` shows a non-prerelease with three assets; every checklist line has quoted evidence, including the unchanged-originals hash table from the installed build. Cheaper substitute that fails: releasing without the installed-build guard check.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "Category=Fidelity"` passes the pipeline and export goldens
- [ ] The freeze check of §1 passes over a full session
- [ ] The `lumen-v0.1.0` release exists with matching checksums
- [ ] `python scripts/todo-graph.py validate` clean
