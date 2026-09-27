---
schema_version: 1
id: pinxit-files
domain: 03-pinxit
status: draft
title: "TODO-04 -- Pinxit File I/O"
depends_on: []
frozen: true
track: I4
---

# TODO-04 -- Pinxit File I/O

> **Goal:** Pinxit opens and saves the files people actually have: PNG and JPEG (8 and 16 bit where the format allows, with color profiles kept), TIFF, a native layered format that keeps every layer, mask, and blend mode, and PSD for reading layered work from Photoshop; every reader and writer is proven by a round trip against committed fixtures, every save is atomic, and a crash offers recovery. The codec libraries are a recorded decision with their licenses checked against GPL-3.0.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** `Pinxit.FileFormats` holds one interface, `IImageFormat` (42 lines), and a `GlobalUsings.cs` that imports only `System.Buffers` (**Corrected 2026-09-26:** said "importing SixLabors.ImageSharp, which no code uses (`D00 T02 §4` removes it)"; the toolchain upgrade removed the package and the usings, `D00 T02 §4` verifies). `DocumentService.OpenDocumentAsync` and `SaveDocumentAsync` are stand-ins that log and return true. No fixture exists under `tests/fixtures/pinxit/`. The installer registers optional `.png`, `.jpg`/`.jpeg`, and `.psd` associations (`installer/Pinxit.iss`), so today those open an empty Pinxit. The legacy roadmap's file phase (7, 34 items) is entirely open.
<!-- claim: lines src/Pinxit/src/Pinxit.FileFormats/IImageFormat.cs = 42 -->
<!-- claim: count "\.psd" installer/Pinxit.iss = 7 -->
<!-- claim: absent tests/fixtures/pinxit -->

## Inputs

- [`standards/pinxit.md`](../../standards/pinxit.md) -- formats owe fidelity proofs and must say what they cannot carry
- [`standards/testing.md`](../../standards/testing.md) -- fixtures, goldens, the fidelity trait
- The PNG (https://www.w3.org/TR/png-3/), TIFF 6.0, JPEG/JFIF, OpenRaster (https://www.openraster.org/), and Adobe Photoshop File Formats specifications -- the sources of truth for §2 to §5
- -> XREF: D00 T02 §4 -- removed ImageSharp and left the codec choice to §1
- -> XREF: D01 T02 §5 -- the shared atomic writer §2 is the second consumer of
- -> XREF: D03 T03 §2 -- the history recovery must restore into
- -> XREF: D01 T04 §1 -- the suite color engine whose next consumer is §2's embedded PNG and JPEG profiles
- -> XREF: D01 T05 §3 -- the AI provenance record §2's save may later embed
- -> XREF: D02 T14 §12 -- Stilus's WIC codec, which moves to `Isotone.Core` if §1 picks WIC; `D02 T14 §13`'s PSD reader moves to `Isotone.Core` for §5
- -> XREF: D03 T08 §1 -- Pinxit parity document and view cites §4: the native format D03 T08 §1 extends with the `pinxit:` contract; §2: recent files D03 T08 §2 extends; §5: the PSD adapter D03 T08 §1, D03 T08 §4, and D03 T08 §5 extend with resolution, pixel aspect, guide, and note resources
- -> XREF: D03 T09 §1 -- Pinxit parity layers cites §4: the native format whose fixtures every freeze check re-saves byte-identical; §5: the PSD adapter D03 T09 §1, D03 T09 §3, D03 T09 §4, D03 T09 §5, D03 T09 §7, and D03 T09 §9 extend with locks, labels, masks, clipping, blending ranges, effects, and placed layers
- -> XREF: D03 T15 §1 -- Pinxit parity photo (Camera Raw and merges) cites §3: the TIFF reader for linear DNG sources and the DNG read-back
- -> XREF: D03 T17 §11 -- Pinxit parity formats cites §1: the codec decision and the WIC codec it placed; §2: PNG and JPEG readers and writers and the JPEG options dialog D03 T17 §11 extends; §3: the TIFF reader and writer D03 T17 §11 extends; §4: the native format and its atomic save; §5: the PSD reader D03 T17 §2 and D03 T17 §3 extend
- -> XREF: D03 T18 §1 -- Pinxit parity export, color management, and print cites §2: the save paths Export As extends
- -> XREF: D03 T20 §5 -- Pinxit parity workspace cites §6: autosave and recovery D03 T20 §5 configures

## Outcome

- `docs/dev/decisions.md` records the codec choice per format with licenses and evidence.
- PNG, JPEG, and TIFF open into layers and save through the atomic writer, keeping bit depth and embedded ICC profiles; each has a fidelity fixture set.
- The native `.pinxit` format round-trips every layer type Pinxit edits, with masks, blend modes, and opacity, and is OpenRaster-compatible for its raster layers.
- PSD files open with their layers, blend modes, opacity, visibility, and layer masks, or say exactly what was flattened.
- Autosave writes recovery drafts in the native format; a crash offers them on the next start.
- `todo/README.md` lists Pinxit's save path and autosave in the frozen set.

**Adjacency:** list=not-applicable (recent files are listed by §2's File menu, which is the same list pattern Stilus uses); document=not-applicable (printing is a roadmap item); settings=applicable @ D03 T04 §2; reporting=not-applicable (no summaries); notifications=applicable @ D03 T17 §1; permissions=applicable @ D03 T04 §2; audit=applicable @ D03 T17 §1; exchange=applicable @ D03 T04 §5; reverse=applicable @ D03 T04 §6

**Adjacency rationale:** JPEG quality and recent files are settings; saves of large files show progress; read-only targets are refused; every open and save logs; PSD is the foreign exchange format; recovery reverses a crash.

## Implementation Order

| Order | Section | Deliverable                                          | Depends On                          | Status |
| :---: | :-----: | ---------------------------------------------------- | ----------------------------------- | :----: |
|   1   |   §1    | The codec decision                                   | D00 T02 §5                          |  [ ]   |
|   2   |   §2    | PNG and JPEG open and save                           | §1, D01 T02 §5, D03 T03 §1          |  [ ]   |
|   3   |   §3    | TIFF open and save                                   | §2                                  |  [ ]   |
|   4   |   §4    | The native layered format                            | §2, D03 T03 §3                      |  [ ]   |
|   5   |   §5    | PSD import                                           | §4, D03 T02 §4, D02 T14 §13         |  [ ]   |
|   6   |   §6    | Autosave and crash recovery                          | §4, D03 T03 §2                      |  [ ]   |

---

## 1. The Codec Decision

Pinxit needs decoders and encoders for PNG, JPEG, TIFF, and PSD, with 16-bit and ICC profile support. The candidates, with the facts the decision must verify at the time it is made: **WIC** through WPF's `System.Windows.Media.Imaging` (part of Windows; PNG, JPEG, TIFF, BMP, GIF with 16-bit and `ColorContext` profiles; no PSD; Windows-only, which Pinxit is); **SkiaSharp** (BSD-3-Clause, already in the suite; PNG, JPEG, WebP; no TIFF or PSD; 8-bit oriented encoders); **Magick.NET** (Apache-2.0 wrapper over ImageMagick's own license; every format including PSD; tens of megabytes of native code); **LibTiff.NET** (BSD; TIFF only); **SixLabors.ImageSharp** (Six Labors Split License; 4.x needs a paid key; removed by `D00 T02 §4`); and a **hand-written PSD reader** against Adobe's published file format specification. **Justified default:** WIC for PNG, JPEG, and TIFF (no new dependency, 16-bit and profiles supported), a hand-written PSD reader (the layer structure is what Pinxit needs, and a reader is testable against Photoshop-produced fixtures), SkiaSharp for WebP later. Cost of changing: each codec sits behind `IImageFormat`, so a swap is one class per format.

**Corrected 2026-09-26:** the Stilus parity plan runs before Pinxit's foundation, so Stilus builds its raster codecs first: `D02 T14 §12` adds a `WicCodec` over WPF's `BitmapDecoder` and `BitmapEncoder` (plus own TGA and PCX codecs), and `D02 T14 §13` adds a `PsdReader` against Adobe's specification. This decision therefore also records whether Pinxit picks the same WIC stack; if it does, the Stilus `WicCodec` moves to `Isotone.Core` (the shared-once rule) and Pinxit consumes it rather than writing a second WIC wrapper, and the PSD choice is the reader `D02 T14 §13` built (see §5).

- [ ] For each candidate, record license (with the license text URL), GPL-3.0 compatibility, format coverage including 16-bit and ICC support, installed size, and a decode-time measurement of the same 24-megapixel PNG and JPEG (a small benchmark in `tests/Isotone.Pinxit.Benchmarks`; **Groomed 2026-09-28:** `D03 T02 §1` creates that project, and if this section runs first it creates it the same way). Done when: `docs/dev/decisions.md` carries the table with every cell filled.
- [ ] Decide per format and record the choice, the evidence, and the cost of change, including whether the WIC choice reuses the Stilus `WicCodec` from `D02 T14 §12` (moved to `Isotone.Core`) and that PSD uses the `D02 T14 §13` reader. Done when: the decision entry names a codec for PNG, JPEG, TIFF, and PSD, and names the shared Stilus codec it moves or the reason it does not.
- [ ] Add any chosen package to `Directory.Packages.props` with its license noted in the package table of `docs/dev/build.md`. Done when: restore is green, or the entry says no package was needed.
- [ ] Commit: `"pinxit: decide the codecs with licenses and measurements"`

**Test checkpoint:** `docs/dev/decisions.md` has the codec entry with a license URL and a measured decode time per candidate that can run on Windows; `dotnet build Isotone.slnx -c Release` exits 0. Cheaper substitute that fails: choosing a library without measuring or checking its license, which the empty table cells expose.

## 2. PNG and JPEG Open and Save

The two formats most images arrive in. Opening creates a one-layer document at the file's bit depth with its ICC profile attached; saving flattens (with a notice when there are several layers) and writes through the shared atomic writer. This section adds Pinxit's save path to the frozen set.

**Freeze check:** Save writes through `Isotone.Core` `AtomicFileWriter`: a temp file in the target folder, flushed, then replaced; killing the process after the temp write leaves the original byte-identical; a read-only or locked target is refused with the document still open and dirty. Fixture source: `tests/fixtures/save-over/` and `tests/fixtures/pinxit/png/`.

**Fidelity:** Pinxit File menu, Open and Save As, and the JPEG options dialog -- docs/design/components/ (Menu, Dialog, Slider, NumberBox, Checkbox, Progress, Button), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/main-window/, docs/captures/golden/pinxit/jpeg-options/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/Slider/README.md, docs/design/components/NumberBox/README.md, docs/design/components/Checkbox/README.md, docs/design/components/Progress/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can open PNG and JPEG files, edit them, and save them back without losing bit depth or color profile, and is told before a save flattens layers. Consumer: the file on disk and every app that reads it.
**Treatment:** File, Open with a filter per format; Save and Save As choosing the format by extension; a JPEG options dialog (quality 0 to 12 mapped to 1 to 100, progressive, keep metadata); saving a multi-layer document to PNG or JPEG shows "This format cannot keep layers. Save a flattened copy? Your layers stay in the open document." with Save Flattened and Cancel; 16-bit documents saved as JPEG show the 8-bit conversion notice. Cheaper substitute that fails the checkpoint: silently flattening.
**Chrome:** consume the chosen codec, `AtomicFileWriter`, `DialogService`, and the settings store (last JPEG options, recent files).

**Requires:** display-session -- driving open, save, and the options dialog needs an interactive desktop

- [ ] Add `PngFormat` and `JpegFormat` implementing `IImageFormat` in `Isotone.Pinxit.FileFormats/`, reading 8 and 16 bit (PNG) and 8 bit (JPEG) into tiles and carrying the ICC profile. Done when: unit tests open each fixture's expected dimensions, depth, and profile name.
- [ ] Build the fixture set under `tests/fixtures/pinxit/png/` and `jpeg/` (8-bit RGB, 8-bit RGBA, 16-bit RGBA, grayscale, palette, interlaced PNG, a PNG with an sRGB and one with a Display P3 profile; baseline and progressive JPEG, CMYK JPEG), authored or taken from the PngSuite (license recorded) with a README. Done when: the README lists each file, its source, and license.
- [ ] `PinxitCodecFidelityTests` (`[Trait("Category", "Fidelity")]`): PNG round trip is pixel-exact; JPEG open matches a libjpeg-turbo decode (via `djpeg`, version recorded) within 1/255; JPEG re-save at quality 95 stays within a stated PSNR of 40 dB. Done when: every fixture reports.
- [ ] Wire File, Open (also from the command line and the single-instance forwarder), Save, Save As, and recent files; the flatten and bit-depth notices. Done when: a driven save of a two-layer document to PNG shows the notice.
- [ ] Unsupported or corrupt files show "Pinxit cannot open <name>: <reason>." and log a Warning; nothing is left half-open. Done when: truncated-file tests pass for both formats.
- [ ] Add "Pinxit document save path" to the frozen set in `todo/README.md`. Done when: the paragraph names it with this section's ref.
- [ ] A save to a read-only, locked, or missing-folder target shows "Pinxit could not save <name>: <reason>." with the document still open and dirty, logs one Warning, and leaves the target byte-identical; every successful open and save logs one Information line (path, format, bit depth, layer count, bytes) and re-reads the written file's header to confirm format and dimensions before clearing the dirty flag (**Groomed 2026-09-28:** the Freeze check and the Adjacency rationale require it, and no item built it). Done when: `PinxitSaveRefusalTests` cover the three refusals over `tests/fixtures/save-over/` and a test logger asserts the open and save lines.
- [ ] Commit: `"pinxit: open and save PNG and JPEG with profiles and fidelity proofs"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` prints a result per PNG and JPEG fixture, all within their stated tolerances; the interrupted-save test leaves the fixture's hash unchanged; a driven open, edit, save, and reopen of the 16-bit PNG keeps 16 bits (quote the IHDR bit depth read from the saved file). Cheaper substitute that fails: saving 16-bit documents as 8-bit PNG, which the IHDR check catches.

## 3. TIFF Open and Save

TIFF is the exchange format of print and of Albumen's "Edit in Pinxit" hand-off (16-bit TIFF). Pinxit must open and save 8 and 16 bit RGB and RGBA TIFFs with LZW or ZIP compression and keep the profile.

- [ ] Add `TiffFormat` (chosen codec) with 8 and 16 bit, uncompressed, LZW, and Deflate, single page; multi-page files open their first page with a notice naming the page count. Done when: tests cover each variant.
- [ ] Fixtures under `tests/fixtures/pinxit/tiff/` with a README, and fidelity tests: round trip pixel-exact for each compression. Done when: every fixture passes.
- [ ] A TIFF with layers from Photoshop (layer data in the ImageSourceData tag) opens its composite with a notice that layers were not read (PSD is the layered path). Done when: a fixture proves the notice.
- [ ] TIFF saves go through the §2 save path: the refusal, the log line, and the readback (**Groomed 2026-09-28**). Done when: `PinxitSaveRefusalTests` gains a TIFF case.
- [ ] Commit: `"pinxit: open and save 8 and 16 bit TIFF"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes every TIFF fixture pixel-exact; the Photoshop-layered fixture opens with its notice logged. Cheaper substitute that fails: 8-bit only.

## 4. The Native Layered Format

A document with layers needs a format that keeps them. The native format is a ZIP container on the OpenRaster layout (`mimetype`, `stack.xml`, one PNG per raster layer, `mergedimage.png`, `Thumbnails/thumbnail.png`), with Pinxit-specific attributes (blend modes beyond OpenRaster's set, masks, adjustment and text layer data) in a namespaced extension, and the `.pinxit` extension. Renaming a `.pinxit` to `.ora` opens its raster layers in GIMP and Krita, which is the fidelity oracle.

**Freeze check:** Saving `.pinxit` writes the whole ZIP to a temp file through `AtomicFileWriter` and replaces the target; killing the process mid-save leaves the previous file byte-identical; a document never saves a layer it could not encode without refusing the whole save. Fixture source: `tests/fixtures/pinxit/native/`.

- [ ] Add `PinxitNativeFormat` (reader and writer) with a schema version in `stack.xml` and a documented extension namespace in `docs/dev/pinxit/native-format.md`. Done when: the spec page describes every element and attribute.
- [ ] Round-trip tests for every layer type the editor makes (raster at 8 and 16 bit, group, with masks, every blend mode, hidden, locked, opacity). Done when: `NativeFormatFidelityTests` pass pixel-exact and property-exact.
- [ ] An OpenRaster compatibility test: open a saved file with GIMP in batch mode (`gimp-console` with a Script-Fu export of the composite, version recorded) and compare the composite within 1/255. Done when: the test runs where GIMP is installed and skips with a reason elsewhere, and the result is quoted here.
- [ ] Forward compatibility: a file with a newer schema version opens read-only with a notice; unknown extension elements are preserved on save. Done when: a fixture with an unknown element round-trips it.
- [ ] Native-format saves go through the §2 save path: the refusal, the log line, and the readback (**Groomed 2026-09-28**). Done when: `PinxitSaveRefusalTests` gains a native-format case.
- [ ] Commit: `"pinxit: a native layered format on the OpenRaster layout"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes every native fixture; the GIMP comparison result is quoted with GIMP's version; the interrupted-save test leaves the previous file's hash unchanged. Cheaper substitute that fails: a private binary format, which no other application can check.

## 5. PSD Import

Layered work from Photoshop arrives as PSD, and the installer offers a `.psd` association. Pinxit reads the layer structure: raster layers, groups, blend modes, opacity, visibility, and layer masks, 8 and 16 bit RGB. Everything it cannot represent (adjustment layers, smart objects, text engine data, layer effects) is either rasterized from the layer's stored pixels or reported, never silently dropped. -> SOURCE: legacy-pinxit-7.2

**Corrected 2026-09-26:** this section no longer writes its own PSD reader. Stilus's `PsdReader` (`D02 T14 §13`, in `src/Stilus/Isotone.Stilus.Core/Formats/Psd/`, against the same Adobe specification) ships first; this section moves it into `Isotone.Core` as its second consumer and maps its output onto Pinxit's layers. A second PSD parser in `Isotone.Pinxit.FileFormats/` would be a copy the shared-once rule forbids.

- [ ] Move `PsdReader` from `src/Stilus/Isotone.Stilus.Core/Formats/Psd/` into `src/Isotone.Core/Formats/Psd/` with its tests, repoint Stilus's PSD import to it, and add the Pinxit adapter in `Isotone.Pinxit.FileFormats/Psd/` that maps its layers, groups, and channels (RLE and raw; 8 and 16 bit) onto Pinxit's document. Done when: `PsdReaderTests` run from `tests/Isotone.Core.Tests/`, Stilus's PSD tests still pass, and `grep -rn "class PsdReader" src` finds exactly one definition. Cheaper substitute: a second reader in Pinxit, which the single-definition grep refuses.
- [ ] Map PSD blend-mode keys to `BlendMode`, and layer masks to `LayerMask`. Done when: a fixture with one layer per mode opens with the right modes.
- [ ] Unsupported features produce a per-file import report ("3 adjustment layers were rasterized; text layers are pixels") shown once and logged. Done when: a fixture with an adjustment layer shows the report.
- [ ] Fixtures under `tests/fixtures/pinxit/psd/`, produced by Photoshop or Photopea (tool and version recorded), each with the composite exported beside it as PNG; `PsdFidelityTests` compare Pinxit's composite of the imported layers with that PNG within 2/255. Done when: every fixture passes or names its gap's section.
- [ ] Commit: `"pinxit: import layered PSD files with an honest import report"`

**Test checkpoint:** `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes every PSD fixture within 2/255 of its exported composite; a truncated PSD shows the cannot-open message without a crash. Cheaper substitute that fails: opening the PSD's merged image only, which the per-layer fixture catches.

## 6. Autosave and Crash Recovery

Autosave writes recovery drafts of dirty documents in the native format to the app-data folder on an interval; the next start after a crash offers them. It joins the frozen set. -> SOURCE: legacy-pinxit-3.1-autosave

**Freeze check:** Autosave writes only to `%LOCALAPPDATA%\Rizonesoft\Pinxit\recovery\` through `AtomicFileWriter`, never to a document's path; a draft is deleted only after its document saves or the user discards it; killing the process mid-autosave leaves the previous draft readable. Fixture source: `tests/fixtures/pinxit/native/`.

**Fidelity:** Pinxit crash recovery prompt -- docs/design/components/ (Dialog, ListTree, Button), per standards/design-contract.md; goldens under docs/captures/golden/pinxit/recovery/. **Corrected 2026-09-27:** this line cited `docs/captures/pinxit/` folders as the baseline or capture target; the design is the source and approved renders land as goldens (standards/design-contract.md), and a legacy capture is a before record only, never the thing to match.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user gets unsaved work back after a crash. Consumer: the recovery prompt.
**Treatment:** drafts every 5 minutes (setting `Pinxit.Autosave.IntervalMinutes`, 0 turns it off) for dirty documents, written off the UI thread from a copy-on-write tile snapshot so painting never stalls; a session marker detects a crash; the prompt lists drafts with Recover, Discard, and Later. Cheaper substitute that fails the checkpoint: saving over the user's file.
**Chrome:** consume `AppDataPaths`, `AtomicFileWriter`, `PinxitNativeFormat`, and the theme; the prompt follows Stilus's recovery prompt pattern (move it to `Isotone.UI` through `add-todo` if it is identical).

**Requires:** display-session -- the kill-and-recover drive needs an interactive desktop

- [ ] `PinxitAutosaveService` with snapshot, interval, and marker. Done when: tests cover interval, clean-document skip, and deletion after save.
- [ ] The recovery prompt at startup. Done when: a driven kill-and-restart offers the draft and Recover restores all layers (layer count and a pixel hash quoted).
- [ ] Add "Pinxit autosave and recovery" to the frozen set in `todo/README.md`. Done when: the paragraph names it.
- [ ] Remove `Isotone.Pinxit.Core/History/HistoryPersistence.cs` (an unused, non-atomic `File.WriteAllText` recovery timer under `%LOCALAPPDATA%\Pinxit\recovery`) or fold what it records into `PinxitAutosaveService`, so one recovery store remains (**Groomed 2026-09-28:** found with no owner). Done when: `grep -rn "class HistoryPersistence" src` prints nothing and the decision is in the commit body.
- [ ] Commit: `"pinxit: autosave drafts and crash recovery"`

**Test checkpoint:** `dotnet test Isotone.slnx` exits 0 with the autosave tests reporting; the driven kill-and-restart recovers the document with identical layers, and the original file's hash is unchanged. Cheaper substitute that fails: autosaving over the document.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx --filter "Category=Fidelity"` passes every Pinxit format fixture
- [ ] The freeze checks of §2, §4, and §6 pass
- [ ] `docs/dev/decisions.md` records the codec decision
- [ ] `python scripts/todo-graph.py validate` clean
