---
schema_version: 1
id: lumen-ai
domain: 04-lumen
status: draft
title: "TODO-10 -- Lumen AI: Faces, Keywords, Similarity, Culling, and Masks"
depends_on: []
frozen: true
track: L10
---

# TODO-10 -- Lumen AI: Faces, Keywords, Similarity, Culling, and Masks

> **Goal:** Lumen's AI answers every Lightroom Classic and ACDSee AI job on the suite's three pillars. Results are editable, structured, non-destructive data applied as undoable catalog or edit-stack commands: a suggested keyword, name, verdict, or setting is a proposal the user accepts, an AI mask is a develop mask component, generative removal is a develop spot, and enhanced pixels are new files. The features are suite-aware: they run on the shared AI core `D01 T05` (OpenRouter with the user's own key stored with DPAPI, the explicit-send gate and send preview, provenance), and the segmentation engine, vision locator, image-generation adapter, distraction finder, and depth estimator Imago built move to `Photon.Core` on this second consumer. Every action is explainable and reproducible: the prompt, model, parameters, and seed (with whether the model honored it) are recorded in the catalog, shown in the photo's history, re-runnable and comparable, and embedded as XMP in exports. Faces are detected and recognized on the machine (OpenCV's YuNet, model MIT, and SFace, model Apache-2.0, on OpenCvSharp4) and never leave it; similarity is local perceptual hashing; keywords, captions, alt text, OCR, eye-state culling, mask locating, auto settings, super resolution, and generative removal send a downscaled, metadata-stripped copy only after an explicit action and the send preview; denoise is classical, with a machine-learning denoiser in backlog B-046. Code lives in `src/Lumen/Photon.Lumen.Core/AI/` and `src/Lumen/Photon.Lumen.Core/Faces/`, with shared pieces in `src/Photon.Core/AI/` and `src/Photon.Core/Imaging/Segmentation/`. Every test runs over the recorded transport of `D01 T05 §1`; no live key is used in CI.

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** Lumen has no source tree (`src/Lumen/` is absent) and `src/Photon.Core/` does not exist, so the AI core this file consumes (`todo/01-core/TODO-05-photon-ai.md`) is planned, not built, and every Lumen path below is a target path `D04 T01 §2` creates. No source file in the repository talks to OpenRouter, and no OpenCV package is referenced in `Directory.Packages.props` (`D03 T15 §5` adds OpenCvSharp4 for Imago's photo merges before this file runs). On-device models beyond this file's two small face models stay in backlog B-046, which today is one entry. Imago's AI pieces this file moves (`D03 T10 §6`, `D03 T19 §2`, `§6`, `§8`, `§9`, `§14`) are planned in Imago's parity phases, which run before this file.
<!-- claim: absent src/Lumen -->
<!-- claim: absent src/Photon.Core -->
<!-- claim: exists todo/01-core/TODO-05-photon-ai.md -->
<!-- claim: count "OpenRouter" src/**/*.cs = 0 -->
<!-- claim: count "OpenCvSharp" Directory.Packages.props = 0 -->
<!-- claim: count "^- \[B-046\]" todo/backlog.md = 1 -->

## Inputs

- [`standards/lumen.md`](../../standards/lumen.md) -- the original-file guard, the catalog as a user document, forward-only migrations
- [`standards/shared.md`](../../standards/shared.md) -- settings with named consumers, one Information log line per change, the dependency-license rule
- [`docs/parity/lumen-section-design.md`](../../docs/parity/lumen-section-design.md) -- "AI: Lumen's own, on the three pillars, local where it should be", the decisions this file implements
- [`docs/parity/lumen-parity.md`](../../docs/parity/lumen-parity.md) -- the catalog rows LP-0291 to LP-0299, LP-0361 to LP-0363, LP-0419 to LP-0422, and LP-0693 to LP-0751 this file owns (per-section lists in each context paragraph)
- OpenCV Zoo `face_detection_yunet` (model MIT) and `face_recognition_sface` (model Apache-2.0) model cards, and OpenCvSharp4 (Apache-2.0) -- the local face engine of §2
- Metadata Working Group Guidelines for Handling Image Metadata 2.0 (`mwg-rs:Regions`) and Microsoft's `MP:RegionInfo` schema -- face regions in §12
- Zauner 2010 (perceptual hashing) and Burkhard and Keller 1973 (BK-trees) -- the similarity index of §5
- OpenRouter API reference (https://openrouter.ai/docs/api-reference) -- reached only through `D01 T05 §1`
- Tesseract OCR 5 (Apache-2.0) command line -- the optional user-installed local OCR path of §4, never bundled
- -> XREF: D01 T05 §1 -- the client, structured output, image generation, and the recorded transport every test here runs over
- -> XREF: D01 T05 §2 -- the DPAPI key store and per-task model settings
- -> XREF: D01 T05 §3 -- the provenance record, re-run, and compare
- -> XREF: D01 T05 §4 -- the send gate, send preview, AI settings page, progress panel, and usage indicator
- -> XREF: D03 T10 §6 -- the segmentation engine §7 moves to `Photon.Core` (its `GuidedFilter` is already there)
- -> XREF: D03 T19 §2 -- the image-generation adapter §8 moves to `Photon.Core`
- -> XREF: D03 T19 §6 -- the locate schema and `VisionLocator` §7 moves
- -> XREF: D03 T19 §8 -- the upscale service §8 moves
- -> XREF: D03 T19 §9 -- the distraction finder §9 moves
- -> XREF: D03 T19 §14 -- the depth estimator §10 moves
- -> XREF: D03 T19 §15 -- the `AiMaskComponent` kind §7 stores its masks in
- -> XREF: D03 T15 §5 -- OpenCvSharp4, already a suite dependency, which §2 references
- -> XREF: D04 T01 §6 -- import, which §6 and §12 hook for analysis and face-data import
- -> XREF: D04 T01 §10 -- the keyword hierarchy person keywords join (§3)
- -> XREF: D04 T01 §11 -- culling commands §6 applies
- -> XREF: D04 T04 §9 -- the Lumen Viewer's information tools, where §12 shows faces
- -> XREF: D04 T05 §2 -- the background indexer, whose metadata pass §12 hooks to import face data from browsed photos
- -> XREF: D04 T05 §11 -- the duplicate finder §5 extends with visual similarity
- -> XREF: D04 T06 §3 -- stacks §5 and §6 create and §8 outputs join
- -> XREF: D04 T06 §7 -- quick and advanced search, which gain person, AI keyword, and similarity criteria
- -> XREF: D04 T08 §2 -- the metadata panel, where caption and alt text proposals and face names appear
- -> XREF: D04 T08 §5 -- the keyword store accepted AI keywords promote into
- -> XREF: D04 T08 §8 -- `MetadataWriter`, the one path regions and accepted keywords take to sidecars, and to originals only under the opt-in `Lumen.Originals.InPlace.EmbedMetadata`
- -> XREF: D04 T09 §5 -- the detail panel §8's Enhance extends
- -> XREF: D04 T09 §9 -- the masking panel §7's AI masks and §10's depth ranges join
- -> XREF: D04 T09 §10 -- the Remove tool §9's generative option joins
- -> XREF: D04 T09 §11 -- presets, which §11's adaptive presets extend
- -> XREF: D04 T11 §1 -- the background job engine §2, §6, and §8 run on, and its idle activities (`Lumen.Activity.Idle.*`) that §2, §4, and §5 register as idle kinds
- -> XREF: D04 T11 §5 -- the resize size math §8's target sizes share
- -> XREF: D04 T12 §13 -- export metadata options that embed provenance and exclude person keywords
- -> XREF: D04 T13 §7 -- the DNG writer §8's outputs write through
- -> XREF: D06 T01 §3 -- the Lumen user guide every UI section here updates

## Outcome

- Every Lightroom Classic and ACDSee AI job in the catalog maps to a Lumen feature reachable from one AI menu, each wired or disabled with its owner section named.
- No request reaches OpenRouter without an explicit user action and a send preview whose listed bytes are the request body; outgoing images are at most `Lumen.AI.MaxEdge` pixels on the long edge with metadata stripped, proven over the recorded transport.
- Faces are detected, recognized, clustered, and named on the machine; a test runs the whole face pipeline with a recording network handler and it records zero requests.
- Every AI result is data: AI keywords, captions, names, verdicts, and auto settings are proposals accepted as undoable commands; AI masks and generative spots are develop data that re-render and revert; enhanced pixels are new files stacked with their sources, originals unchanged.
- Every AI action writes a provenance record into the catalog with prompt, model, parameters, seed, whether the seed was honored, hashes, and cost, shown in the photo's history, re-runnable and comparable, and embedded as XMP in exports.
- Imago's segmentation engine, vision locator, image-generation adapter, upscale service, distraction finder, and depth estimator live once in `Photon.Core`.

**Adjacency:** list=applicable @ D04 T10 §3; document=not-applicable (this file prints nothing; §8 writes new image files through the DNG writer and export and print are D04 T12); settings=applicable @ D04 T10 §1; reporting=applicable @ D04 T10 §1; notifications=applicable @ D04 T10 §1; permissions=applicable @ D04 T10 §1; audit=applicable @ D04 T10 §1; exchange=applicable @ D04 T10 §12; reverse=applicable @ D04 T10 §4

**Adjacency rationale:** The lists are the People view with named and unnamed groups (§3), the AI keyword review list (§4), similarity groups (§5), and the culling results grid (§6), each filterable. Settings are the `Lumen.AI.*`, `Lumen.Faces.*`, and `Lumen.Similarity.*` keys on the shared AI settings page and Lumen's own rows, every automatic run off by default (§1). Reporting is usage and cost per action and per catalog (§1), culling scores (§6), and similarity distances (§5). Queue progress, send previews, cost warnings, and completion reach the status strip and the suite toast through `D01 T05 §4`. No key, no network, a declined send, a model refusal, a missing Tesseract, and face data under the policy that People features never send faces are refusals by name (§1 owns the gate). Audit is one provenance record and one log line per AI action (§1). Exchange is MWG and Microsoft face regions, Picasa and ACDSee face data, keywords, and captions in XMP (§12, §4). The reverse is that every acceptance, naming, verdict, and apply is one undoable command (§4), AI masks and spots revert like any develop data, and outputs are new files.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | AI in Lumen: the AI menu, the send gate, provenance, and the AI data store | D04 T02 §8, D01 T05 §4 |  [ ]   |
|   2   |   §2    | The local face engine | §1, D04 T11 §1 |  [ ]   |
|   3   |   §3    | People: named faces, suggestions, and person search | §2, D04 T08 §2, D04 T06 §7 |  [ ]   |
|   4   |   §12   | Faces in the viewer and face regions in XMP | §3, D04 T08 §8, D04 T04 §9 |  [ ]   |
|   5   |   §4    | AI keywords, captions, alt text, and OCR | §1, D04 T08 §5 |  [ ]   |
|   6   |   §5    | Similar photos and visual duplicates | §1, D04 T05 §11, D04 T06 §3 |  [ ]   |
|   7   |   §6    | Assisted culling | §2, §5 |  [ ]   |
|   8   |   §7    | AI masks in develop | §1, D04 T09 §9, D03 T10 §6, D03 T19 §6 |  [ ]   |
|   9   |   §8    | Enhance: denoise, raw details, and super resolution | §1, D04 T09 §5, D04 T13 §7, D03 T19 §8, D04 T11 §5 |  [ ]   |
|  10   |   §9    | Generative and distraction removal | §7, §8, D04 T09 §10, D03 T19 §9 |  [ ]   |
|  11   |   §10   | Lens blur and depth | §7, D03 T19 §14, D01 T06 §3 |  [ ]   |
|  12   |   §11   | Adaptive presets, AI auto settings, and natural-language search | §4, §7, D04 T09 §11 |  [ ]   |

---

## 1. AI in Lumen: the AI Menu, the Send Gate, Provenance, and the AI Data Store

Lumen's AI gets one front door and makes the three pillars structural before any feature lands: an AI menu listing every AI command with its owner section, Lumen's rows on the shared AI settings page (every automatic run off by default), a send-plan builder that downscales and strips metadata from every photo before the shared send preview shows it, standing send scopes for queued runs the user approves explicitly, a provenance table in the catalog with re-run and compare, and an AI data store beside the catalog for cached masks, patches, and depth maps, with a repair command. It builds no key dialog, no HTTP code, and no second consent prompt: those are `D01 T05`'s. Catalog: LP-0419 (1 feature). -> SOURCE: parity-lumen-ai-core

**Freeze check:** The `ai_provenance` table and the AI data store change what the catalog holds, so the migration is forward-only, tested on a copy of the previous version's catalog, and preceded by the catalog backup of `D04 T01 §5`; no command here opens an original image for writing, and the unchanged-originals test of `D04 T02 §1` passes with every AI command in this file run over the recorded transport. Fixture source: `tests/fixtures/lumen/import/` and `tests/fixtures/lumen/ai/`.

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/ai/.
**Job:** a user can see what each AI action will send, cost, and change before it runs, and can inspect, re-run, compare, or revert any past AI result. Consumer: `AiSendGate` reads each approval; the catalog stores provenance; later sections read `LumenSendPlanBuilder`, the data store, and the task settings.
**Treatment:** a top-level AI menu grouping every AI command (disabled entries name their owner section), Lumen rows on the shared AI settings page, the shared send preview listing each outgoing downscaled photo with bytes and estimated cost, a Provenance tab in the photo's history with Re-run, Re-run with New Seed, Compare, and Revert, and an AI cost report per task and month. Cheaper substitute that fails the checkpoint: sending on click with no preview, which `LumenAiSendGateTests` refuse.
**Chrome:** consume `D01 T05 §1` to `§4` and their `Photon.UI` surfaces (`SendPreviewDialog`, `AiSettingsPage`, `AiProgressPanel`, `AiUsageIndicator`), the catalog migration pattern of `D04 T01 §5`, and the history panel of `D04 T02 §3`. Do not build a Lumen key dialog, progress control, or consent prompt.

**Requires:** display-session -- the send preview, the AI menu, and the Provenance tab need an interactive desktop

- [ ] Register the shared AI services in Lumen's composition root with `services.AddPhotonAi()` from `D01 T05 §1`, app name `Lumen`. Done when: a composition test resolves `AiSendGate`, `IAiKeyStore`, and `IGatedAiClient` from the Lumen container.
- [ ] Add `LumenAiTask` in `src/Lumen/Photon.Lumen.Core/AI/` (Keywords, Caption, AltText, Ocr, EyeState, DocumentCheck, Locate, AutoSettings, Upscale, Remove, Depth), each resolving to a `D01 T05 §2` task kind with an optional model override `Lumen.AI.Model.<Task>` falling back to the shared `ai.model.*` key. Done when: `LumenAiTaskTests` resolve every task with and without an override.
- [ ] Add Lumen's AI settings with defaults and consumers: `Lumen.AI.MaxEdge` (1024), `Lumen.AI.AllowFaceCrops` (false), and one `Lumen.AI.Auto.<Task>` switch per automatic run, every one false by default, hosted beside the shared `AiSettingsPage` in Lumen's preferences. Done when: `LumenAiSettingsTests` read each default from an empty store and every key names its consumer.
- [ ] Add `LumenSendPlanBuilder`: for each photo, render the preview-cache image, downscale to `Lumen.AI.MaxEdge`, re-encode as JPEG with no EXIF, XMP, IPTC, or GPS segment, and add it to a `D01 T05 §4` `AiSendPlan` with its bytes and a face-crop caution when a part is a face crop. Done when: `LumenSendPlanBuilderTests` parse the outgoing JPEG segments and find no APP1 or APP13, the long edge equals the setting, and the part list matches the request body.
- [ ] Add batch previews: one send preview per batch listing the photo count, total bytes, and total estimated cost with a per-photo expansion. Done when: a view-model test builds a 20-photo plan and the preview totals equal the sum of its parts.
- [ ] Add `AiSendScope` for queued automatic runs: a task, a folder or collection, a daily photo cap, and a cost cap, approved through the send preview by an explicit command that mints the `UserActionId` the gate requires, stored in the catalog, revocable, and paused whenever `ai.sendPreview.alwaysShow` is on. Done when: `AiSendScopeTests` assert no queued request without an approved scope, the caps stop the queue, and revoking stops it.
- [ ] Add the `ai_provenance` catalog table (record JSON, photo id, task, input and output hashes, created) through a forward-only migration with its test on a copy of the previous catalog version. Done when: `ProvenanceCatalogTests.Migration` upgrades the prior fixture catalog and reads a record back.
- [ ] Write one `D01 T05 §3` `ProvenanceRecord` (App `lumen`) per AI action, added and removed by the same catalog command as the action's result, so undoing the action drops its record. Done when: `ProvenanceCatalogTests.UndoDropsRecord` applies, undoes, and redoes a recorded action and asserts the table at each step.
- [ ] Add the AI data store: a folder beside the catalog (`<catalog name>.ai\`) holding cached masks, patches, and depth maps named by content hash and referenced by provenance id, written through `AtomicFileWriter` (LP-0419). Done when: `AiDataStoreTests` store and read an entry by hash and a second store of the same bytes adds no file.
- [ ] Add Repair AI Data: re-link entries found under a moved catalog by hash and purge entries no record references, after a confirmation naming the count and bytes (LP-0419). Done when: `AiDataStoreRepairTests` re-link a moved store and purge exactly the planted orphans.
- [ ] Add the AI menu in `src/Lumen/Photon.Lumen.Desktop/AI/`: every AI command in this file, each wired or disabled with a tooltip naming its owner section until that section ships. Done when: `AiMenuTests` enumerate the menu and every entry is either enabled or names a section that `python scripts/todo-graph.py resolve` resolves.
- [ ] Add the Provenance tab in the photo's history panel: action, prompt excerpt, model, parameters, seed and whether honored, hashes, cost, and date, with Re-run (same seed), Re-run with New Seed through `ProvenanceRecord.ToRerun`, Compare through `ProvenanceDiff`, and Revert (the inverse catalog command). Done when: `ProvenanceTabViewModelTests` re-run a recorded action over the recorded transport and compare two records with the expected differences.
- [ ] Embed provenance as XMP (`photon-ai:` JSON form) in exported copies through `D04 T12 §13`'s metadata options, an Include AI Provenance option on by default. Done when: a test exports a fixture with one record and reads the record back from the copy's XMP.
- [ ] Add the AI usage indicator to Lumen's status bar and an AI cost report per task and month from the provenance table. Done when: a view-model test sums three fixture records into the expected report rows.
- [ ] Notify cost warnings through the suite toast when an action's estimated cost exceeds `Lumen.AI.CostWarningUsd` (default 0.50), before the send preview opens. Done when: a view-model test raises the warning for a plan over the threshold and not for one under it.
- [ ] Enforce the send policy: refuse by name with no key, no network, a declined preview, or a model refusal through `D01 T05 §4`'s mapping, and refuse any plan holding a face crop unless `Lumen.AI.AllowFaceCrops` is on. Done when: `LumenAiSendGateTests.Refusals` assert each sentence and zero requests for each case.
- [ ] Log one Serilog Information line per AI action (`Lumen AI {Task} {Photos} photos {ModelId} {CostUsd} USD`), never the key or prompt text. Done when: a test logger asserts the line and `LogRedactionTests`' check finds no prompt text.
- [ ] Commit the recorded replies this file's tests use under `tests/fixtures/lumen/ai/` in `D01 T05 §1`'s fixture format, each written from the API reference with a README naming what it mirrors and no real key. Done when: the README lists every fixture.
- [ ] Write `docs/user/lumen/ai.md`: what each Lumen AI action sends (a table: task, what leaves the machine, size, whether automatic runs exist), where results land, and that faces never leave the machine. Done when: every AI command in the menu is a row.
- [ ] Commit captures of the AI menu, the send preview for a batch, the Provenance tab, and Lumen's settings rows under `docs/captures/lumen/ai/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: the AI menu, send plans, provenance, and the AI data store"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Lumen.Tests.AI"` exits 0 over the recorded transport with the network unavailable to the test host: `LumenAiSendGateTests` (no request without a confirmed preview), `LumenSendPlanBuilderTests` (no metadata segment in any outgoing image), `AiSendScopeTests`, `ProvenanceCatalogTests`, and `AiDataStoreRepairTests` reporting; a driven send preview for a five-photo batch is captured. Cheaper substitute that fails: implicit sends, which `LumenAiSendGateTests` refuse.

## 2. The Local Face Engine

Face detection and recognition run on the machine and nothing about a face is ever sent anywhere by the People features: OpenCV's YuNet detector (model MIT) finds faces and five landmarks, SFace (model Apache-2.0) turns each aligned face into a 128-dimensional embedding, and clustering by cosine distance groups and names them, all through OpenCvSharp4 (Apache-2.0), which Imago's photo merges already brought into the suite. This section is the engine and its queue; the People surfaces are §3 and §12. Catalog: LP-0420, LP-0693 to LP-0698 (7 features). -> SOURCE: parity-lumen-faces-engine

**Fidelity:** no surface of its own (the People view, the face detection settings rows, and the grid commands are D04 T10 §3; the face tool and viewer faces are D04 T10 §12)

- [ ] Reference OpenCvSharp4 and its Windows runtime package from `src/Lumen/Photon.Lumen.Core/Photon.Lumen.Core.csproj` (central versions already in `Directory.Packages.props` from `D03 T15 §5`), with a `docs/dev/decisions.md` row for Lumen's use recording the Apache-2.0 license check. Done when: `dotnet build Photon.slnx -c Release` exits 0 and the row names the license URL.
- [ ] Bundle `face_detection_yunet_2023mar.onnx` (MIT) and `face_recognition_sface_2021dec.onnx` (Apache-2.0) under `src/Lumen/Photon.Lumen.Core/Faces/Models/` with their license texts and a `models.json` of SHA-256 hashes, copied to the output and the installer, and add both to the third-party notices; a model whose hash differs is refused by name at load. Done when: `FaceModelTests` verify both hashes and refuse a tampered copy by name.
- [ ] Add `FaceDetector` in `src/Lumen/Photon.Lumen.Core/Faces/` over OpenCV's `FaceDetectorYN` (falling back to `CvDnn.ReadNetFromOnnx` with own post-processing if the wrapper lacks it), returning boxes, five landmarks in normalized coordinates, and scores above `Lumen.Faces.DetectionThreshold`. Done when: `FaceDetectorTests` find the expected face count on a committed CC0 group photo and zero on a committed landscape.
- [ ] Add `FaceEmbedder` over `FaceRecognizerSF` (align and crop, then feature), producing L2-normalized 128-dimensional embeddings. Done when: `FaceRecognitionTests` assert same-person pairs are closer by cosine distance than different-person pairs on a small committed CC0 set.
- [ ] Add the `faces` table (photo id, box, landmarks, embedding, person id, state Detected, Suggested, Confirmed, Rejected, or Manual, detector version) and the `people` table (name, profile face id, keyword id) through a forward-only migration tested on the previous catalog version. Done when: `FaceCatalogTests.Migration` upgrades the fixture catalog and round-trips a face.
- [ ] Add `FaceClusterer`: cosine-distance clustering with thresholds for conservative, moderate, and aggressive sensitivity (`Lumen.Faces.Sensitivity`), the moderate threshold recorded against SFace's published value (LP-0695). Done when: `FaceClustererTests` group the committed set into the expected clusters at moderate.
- [ ] Add `FaceNameSuggester`: an unnamed face within the sensitivity threshold of a named person's centroid becomes a suggestion, or is named when `Lumen.Faces.AutoName` is on; rerunning recognition keeps every manual name (LP-0695). Done when: `FaceNameSuggesterTests` assert suggestions, auto naming, and that a manual name survives a rerun.
- [ ] Add `FaceDetectionQueue` on `D04 T11 §1`'s job engine: catalog-wide or a selection (LP-0697), the viewed folder first, pause and resume, redetect selected, rerun on photos whose file hash changed, and remove all face data after a confirmation (LP-0694). Done when: `FaceQueueTests` pause mid-run, resume, and finish with one row per face and none for a removed photo.
- [ ] Add detection modes Off, On Demand, and Automatic (`Lumen.Faces.Detection`, a catalog setting) and idle detection registered as an idle kind in `D04 T11 §1`'s Activity Manager, toggled by `Lumen.Activity.Idle.Faces` (LP-0420, LP-0693, LP-0696). Done when: a test asserts Automatic enqueues newly cataloged photos and Off enqueues nothing.
- [ ] Run on the CPU by default and on OpenCV's OpenCL target when `Lumen.Faces.UseGpu` is on and `Cv2.HaveOpenCL()` reports a device, falling back to the CPU with a log line (LP-0698). Done when: a test with the GPU setting on and no device asserts the CPU path and the log line.
- [ ] Keep faces on the machine: the face engine takes no dependency on `IGatedAiClient`, proven by an architecture test, and the whole queue run with a recording network handler records zero requests. Done when: `FacesNeverSentTests` pass both assertions.
- [ ] Log one Serilog Information line per queue run (`Face detection {Photos} photos, {Faces} faces in {ElapsedMs} ms`). Done when: a test logger asserts the line.
- [ ] Measure and quote detection and embedding on 1,000 photos at 1,024 px on the reference machine, with a budget of 150 ms per photo. Done when: `FaceBudgetTests` (`[Trait("Category", "Budget")]`) print the per-photo time and pass.
- [ ] Commit the CC0 face fixtures under `tests/fixtures/lumen/faces/` with each source and license in `reference.txt`. Done when: every fixture carries its note.
- [ ] Commit: `"lumen: local face detection and recognition"`

**Test checkpoint:** Unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~FaceModelTests|FullyQualifiedName~FaceDetectorTests|FullyQualifiedName~FaceRecognitionTests|FullyQualifiedName~FaceClustererTests|FullyQualifiedName~FaceNameSuggesterTests|FullyQualifiedName~FaceQueueTests|FullyQualifiedName~FacesNeverSentTests|FullyQualifiedName~FaceBudgetTests"` exits 0, with the per-photo time quoted and zero network requests recorded. Cheaper substitute that fails: sending faces to a cloud model, which `FacesNeverSentTests` refuse.

## 3. People: Named Faces, Suggestions, and Person Search

A family photographer names everyone once and finds every photo of a person. This section is the People surface over §2's engine: Lightroom's People view and ACDSee's People mode with named and unnamed groups, naming, suggestions to confirm or deny, people management, person keywords, person search, face deletion, the People preferences, and the face detection settings rows and grid commands. Every naming, confirmation, merge, and deletion is one undoable catalog command. Faces in the viewer and face regions in XMP are §12. Catalog: LP-0291, LP-0361, LP-0699 to LP-0702, LP-0704 to LP-0707, LP-0709, LP-0712 to LP-0714, LP-0716 (15 features), plus the settings and grid surfaces of §2's LP-0420, LP-0693, LP-0695 to LP-0698. -> SOURCE: parity-lumen-people

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/people/.
**Job:** a user can name every person once and find every photo of them. Consumer: the `faces` and `people` tables and the keyword hierarchy.
**Treatment:** Lightroom's People view (O) with named and unnamed stacks and a name field under each face, and ACDSee's People mode with group naming, Confirm All and Deny All, a people list with counts, a People group in the catalog pane, and a People preferences page. Cheaper substitute that fails the checkpoint: naming one face at a time with no suggestions, which `SuggestionCommandTests` catch.
**Chrome:** consume §2's engine, the grid and badges of `D04 T01 §8`, the keyword hierarchy of `D04 T01 §10`, the metadata panel of `D04 T08 §2`, search criteria of `D04 T06 §7`, and the theme. Do not build a second keyword store.

**Requires:** display-session -- the People view and naming need an interactive desktop

- [ ] Add the People view (O) and People mode in `src/Lumen/Photon.Lumen.Desktop/People/` with named, unnamed, and single-person views and face counts formatted beyond 9,999 (LP-0291, LP-0700, LP-0702, LP-0704). Done when: `PeopleViewModelTests` list a fixture catalog's named and unnamed faces with the expected counts.
- [ ] Add the People group in the catalog pane: named people with counts, an unnamed entry, and face search options (named only, unnamed only, a name filter) (LP-0361). Done when: a view-model test filters the pane by name substring.
- [ ] Group unnamed faces by `FaceClusterer` similarity or show them ungrouped (`Lumen.Faces.GroupUnnamed`), and name or delete a whole group as one step (LP-0705). Done when: a test names a three-face group in one step and undo unnames all three.
- [ ] Add face grid interaction: multi-select, face or source thumbnails, and sending the source photos to the loupe or develop (LP-0706). Done when: a view-model test selects two faces and opens their sources in develop.
- [ ] Add the people folders filter: a tree or list of folders, multi-select, and refresh, limiting the People view to faces in those folders (LP-0707). Done when: a test filters a two-folder fixture to one folder's faces.
- [ ] Add naming: a name field under each face with Enter advancing to the next unnamed face and person autocompletion, the Name Faces dialog for bulk naming, rename, remove name, and set profile face (LP-0701). Done when: `NamingTests` name three faces by keyboard alone and set a profile face.
- [ ] Add suggestions: a pending-suggestion indicator, confirm, deny, edit the name inline, and Confirm All and Deny All as one step each (LP-0714). Done when: `SuggestionCommandTests` assert Confirm All is one undo step and a denied suggestion is not suggested again for that person.
- [ ] Add people management: merge people (faces move, one name kept), rename, remove, group by name, face count, or suggestions, sort, and collapse groups (LP-0712). Done when: `MergePeopleTests` merge two people and undo restores both.
- [ ] Add person keywords as a keyword kind in `D04 T01 §10`'s hierarchy, created on naming and renamed with the person, excluded from export when `D04 T12 §13`'s option says so (LP-0699). Done when: `PersonKeywordTests` name a face, find the person keyword, rename the person, and the keyword follows.
- [ ] Add person search: a Person criterion in the catalog pane, quick search, and advanced search through `D04 T06 §7` (LP-0709). Done when: a test finds exactly the fixture photos of one person through each entry point.
- [ ] Add deleting face records, or the source images to the Recycle Bin after a confirmation naming the count (LP-0713). Done when: a test deletes face records only and the files remain, and deleting sources moves them to the Recycle Bin after confirmation.
- [ ] Add the People preferences page: suppress the Confirm All, Deny All, and delete prompts, the default thumbnail (face or source), the folder pane, the unnamed style, and pop-up options (LP-0716). Done when: a view-model test reads back every option after restart.
- [ ] Add the face detection settings rows (Off, On Demand, Automatic, detect while idle, rerun on changed images, sensitivity, auto naming, GPU) bound to §2's settings (LP-0420, LP-0693, LP-0695, LP-0696, LP-0698). Done when: a view-model test asserts each row writes its §2 key.
- [ ] Add Detect Faces on the grid's context menu for a selection, with progress in the Activity Manager of `D04 T11 §1` (LP-0697, LP-0698). Done when: a test invokes the command on two photos and the queue receives exactly those.
- [ ] Log one Serilog Information line per naming, confirmation, merge, and deletion. Done when: a test logger asserts each line.
- [ ] Write `docs/user/lumen/people.md` with the People view, naming, suggestions, management, search, and preferences. Done when: every control is described.
- [ ] Commit captures of the People view, a suggestion group, the Name Faces dialog, and the preferences page under `docs/captures/lumen/people/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: people, face naming, suggestions, and person search"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~PeopleViewModelTests|FullyQualifiedName~NamingTests|FullyQualifiedName~SuggestionCommandTests|FullyQualifiedName~MergePeopleTests|FullyQualifiedName~PersonKeywordTests"` exits 0; a driven session names five faces, confirms a suggestion group, and searches by person, with the log lines quoted and captures committed. Cheaper substitute that fails: one face at a time with no suggestions, which `SuggestionCommandTests` catch.

## 4. AI Keywords, Captions, Alt Text, and OCR

A user tags a large shoot quickly and accepts only the keywords they agree with. AI keywords, captions, and alt text come from an OpenRouter vision model through the shared core with the user's key, as structured JSON validated against a schema, stored apart from the user's keywords as proposals, and promoted only on acceptance, each acceptance one undoable command; automatic runs exist only after the user approves a send scope (§1). OCR uses the vision model or, locally, a Tesseract the user installed. Catalog: LP-0362, LP-0717 to LP-0722 (7 features). -> SOURCE: parity-lumen-ai-keywords

**Freeze check:** Accepted keywords, captions, and alt text reach disk only through `D04 T08 §8`'s `MetadataWriter` (the XMP sidecar by default, a supported original only when `Lumen.Originals.InPlace.EmbedMetadata` is on, through `D04 T08 §9`); unaccepted AI keywords never leave the catalog, and `AiKeywordAcceptanceTests` assert every fixture original's SHA-256 is unchanged after a run, a review, and an acceptance. Fixture source: `tests/fixtures/lumen/import/`.

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/ai-keywords/.
**Job:** a user can tag and describe many photos quickly and accept only what they agree with. Consumer: the `ai_keywords` table, then (on acceptance) the keyword store and the metadata fields.
**Treatment:** ACDSee's AI Keywords group in the Organize pane with assign one, selected, or all, the AI keyword queue controls, a Describe command writing caption and alt text proposals into the metadata panel, and Extract Text. Cheaper substitute that fails the checkpoint: keywords written straight into user keywords, which `AiKeywordAcceptanceTests` refuse.
**Chrome:** consume §1's send plans, scopes, and provenance, `D01 T05 §1` structured output, `D04 T08 §5`'s keyword store, `D04 T08 §2`'s metadata panel, and `D04 T06 §7` search. No second keyword store.

**Requires:** display-session -- the review surface and the Describe proposals need an interactive desktop

- [ ] Add the schema `src/Lumen/Photon.Lumen.Core/AI/Schemas/keywords.v1.json` (keywords with optional parent and confidence, caption, alt text, detected text), validated on every reply by `D01 T05 §1`'s validator. Done when: `KeywordSchemaTests` accept the valid fixture reply and refuse an invalid one with a path-qualified error.
- [ ] Add `AiKeywordService` in `src/Lumen/Photon.Lumen.Core/AI/Keywords/`: one structured request per photo through §1's send plan with a versioned prompt template (its hash in provenance), writing results to the `ai_keywords` table (keyword, parent, photo, provenance id) added by a forward-only migration. Done when: a test runs one photo over the recorded transport and the table holds the fixture's keywords with a provenance id.
- [ ] Add `AiKeywordQueue`: the viewed folder first, run or rerun on a selection, clear queue, pause, a priority scan of the selection, and remove AI keywords (LP-0717). Done when: `AiKeywordQueueTests` pause, prioritize a selection, and clear over the recorded transport.
- [ ] Add AI keyword options: enable, detect while idle as an idle kind in `D04 T11 §1` (`Lumen.Activity.Idle.AiKeywords`), rerun on changed images, and suppress the remove prompt, with automatic runs only inside an approved `AiSendScope` and never on by default (LP-0721). Done when: a test asserts an idle tick sends nothing without a scope and sends within a scope's caps.
- [ ] Add the AI keyword tree stored apart from user keywords and the AI Keywords group in the catalog pane (LP-0718, LP-0362). Done when: a view-model test shows the tree for a fixture and no user keyword exists.
- [ ] Add AI keyword search criteria to quick and advanced search through `D04 T06 §7` (LP-0718). Done when: a test finds the fixture photos by one AI keyword.
- [ ] Add the review panel in the Organize pane: select modes, select all, italics for keywords on only some of the selection, assign one, selected, or all to user keywords, remove one, selected, or all, filter as you type, and undo any assignment as one step (LP-0719). Done when: `AiKeywordAcceptanceTests` assign three keywords to 10 photos as one undoable command and undo removes them.
- [ ] Promote accepted keywords into `D04 T08 §5`'s keyword store with their provenance id, and let them reach sidecars only through `D04 T08 §8` after acceptance (LP-0720). Done when: a test asserts no sidecar change before acceptance and the keyword in the sidecar after it.
- [ ] Add Describe: caption and alt text drafts land as proposals in the `D04 T08 §2` metadata panel fields with Accept and Reject, each acceptance one undoable command, and the description text is kept in `ai_descriptions` for §11's search (LP-0717). Done when: a test accepts a caption proposal and undo restores the prior caption.
- [ ] Add Extract Text for a photo or a selected rectangle: the vision model returns detected text through the schema, or the local path runs a user-installed Tesseract found at `Lumen.AI.TesseractPath` as an external process with the chosen languages, refused by name when absent; the text shows in a dialog with Copy and Save to Caption (LP-0722). Done when: `OcrTests` read the fixture reply, run a fake Tesseract process, and refuse a missing path with "Tesseract was not found at <path>".
- [ ] Log one Serilog Information line per keyword run and per acceptance. Done when: a test logger asserts both.
- [ ] Update `docs/user/lumen/ai.md` with AI keywords, review, Describe, and Extract Text. Done when: every control is described.
- [ ] Commit captures of the review panel, the queue controls, a caption proposal, and the Extract Text dialog under `docs/captures/lumen/ai-keywords/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: AI keywords, captions, alt text, and OCR as reviewed proposals"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~KeywordSchemaTests|FullyQualifiedName~AiKeywordQueueTests|FullyQualifiedName~AiKeywordAcceptanceTests|FullyQualifiedName~OcrTests"` exits 0 over the recorded transport; a driven run over 20 photos with review and one acceptance is captured with its log lines quoted. Cheaper substitute that fails: direct writes to user keywords, which `AiKeywordAcceptanceTests` refuse.

## 5. Similar Photos and Visual Duplicates

A user finds every shot related to one photo and collapses bursts into stacks without any model and without the network. Similarity is local and classical: 64-bit DCT pHash and dHash with an 8 by 8 color layout signature per photo, indexed in a BK-tree over Hamming distance, all own code, computed from the preview cache during idle time. Catalog: LP-0292, LP-0293, LP-0363, LP-0723 to LP-0727 (8 features). -> SOURCE: parity-lumen-similarity

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/similar/.
**Job:** a user can find every related shot of one photo and collapse bursts into stacks. Consumer: the `similarity` table, searches, and stacks.
**Treatment:** Lightroom's visual search from the library, ACDSee's Group by Similarity with a sensitivity slider and an analyze-first prompt, a Similar To search criterion, and auto-stacking by similarity, location, time, or a combination. Cheaper substitute that fails the checkpoint: exact-hash duplicates only, which the recompressed-copy test catches.
**Chrome:** consume the preview cache of `D04 T01 §7`, the idle activities of `D04 T11 §1`, stacks of `D04 T06 §3`, search of `D04 T06 §7`, and the duplicate finder of `D04 T05 §11`. No network, no model.

**Requires:** display-session -- the similarity views need an interactive desktop

- [ ] Add `PerceptualHash` in `src/Lumen/Photon.Lumen.Core/AI/Similarity/`: DCT pHash (Zauner 2010) and dHash, 64 bits each, from a 32 by 32 grayscale of the preview-cache thumbnail, the DCT vectorized with `System.Numerics.Vector<T>`. Done when: `PerceptualHashTests` put resized and recompressed copies within Hamming distance 6 and different committed scenes above 20.
- [ ] Add `ColorLayoutSignature`: an 8 by 8 grid of mean Oklab colors compared by Euclidean distance. Done when: a test ranks a hue-shifted copy farther than a resized one.
- [ ] Add `SimilarityIndex`: a BK-tree over the combined Hamming distance with the layout distance as a tie-breaker, persisted in a `similarity` table (photo id, hashes, layout, source hash) by a forward-only migration. Done when: `BkTreeTests` return exactly the brute-force neighbors within a radius on 5,000 random hashes.
- [ ] Index locally: idle-time indexing of the viewed folder first as an idle kind in `D04 T11 §1` (`Lumen.Activity.Idle.Similarity`), reanalyze selected, and rerun on photos whose file hash changed, on the CPU with the vectorized DCT and no GPU requirement (LP-0723). Done when: a test indexes a fixture folder in idle ticks and a changed file is re-hashed.
- [ ] Add Find Similar and reverse image search from a selected photo: related shots ordered by distance (LP-0292, LP-0725). Done when: `SimilarityGroupingTests.FindSimilar` returns a burst fixture's frames first.
- [ ] Add a Similar To criterion with a similarity slider to advanced search through `D04 T06 §7` (LP-0363). Done when: a test searches with two slider values and the larger returns a superset.
- [ ] Add Group by Similarity with a sensitivity slider and an analyze-first prompt when photos are unindexed, the sensitivity kept in `Lumen.Similarity.Sensitivity` with a do-not-prompt option (LP-0726, LP-0727). Done when: `SimilarityGroupingTests.Groups` assert the expected groups at two sensitivities.
- [ ] Add the similarity options: enable, analyze while idle, rerun on changed images, and the stored sensitivity (LP-0727). Done when: a view-model test reads every option back after restart.
- [ ] Add auto-stacking by visual similarity, GPS distance, capture-time gap, or a combination, previewed then applied through `D04 T06 §3` as one undo step, and custom stacks from a selection of similarity results (LP-0293, LP-0724). Done when: `AutoStackTests` stack a burst fixture by similarity and by time and undo restores the flat list.
- [ ] Extend `D04 T05 §11`'s duplicate finder with a Visually Similar mode reading the index. Done when: a test finds a recompressed copy the exact-hash mode misses.
- [ ] Prove the index never needs the network: a whole index run with a recording network handler records zero requests. Done when: `SimilarityLocalTests` pass.
- [ ] Measure and quote indexing 10,000 photos from cached thumbnails on the reference machine. Done when: `SimilarityBudgetTests` (`[Trait("Category", "Budget")]`) print the time.
- [ ] Update `docs/user/lumen/library.md` with Find Similar, Group by Similarity, the search criterion, and auto-stacking. Done when: every control is described.
- [ ] Commit captures of Find Similar results, Group by Similarity, and the auto-stack preview under `docs/captures/lumen/similar/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: local similarity search, grouping, and auto-stacking"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~PerceptualHashTests|FullyQualifiedName~BkTreeTests|FullyQualifiedName~SimilarityGroupingTests|FullyQualifiedName~AutoStackTests|FullyQualifiedName~SimilarityLocalTests|FullyQualifiedName~SimilarityBudgetTests"` exits 0 with the 10,000-photo time quoted; a driven Group by Similarity on a burst fixture is captured. Cheaper substitute that fails: byte hashes, which the recompressed-copy test catches.

## 6. Assisted Culling

A wedding photographer gets a first cut in minutes and overrides any verdict. Focus, exposure, and misfires are scored locally; eyes-open and document checks send face crops or thumbnails to the vision model only when the user enables them, with that fact in the send preview. Every verdict is data with its reasons, applied through the culling commands as undoable steps; removing rejects deletes catalog records only, never files. Catalog: LP-0294 to LP-0299, LP-0422, LP-0728 (8 features). -> SOURCE: parity-lumen-assisted-culling

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/culling/.
**Job:** a photographer can get a first cut of a large shoot quickly and override any verdict. Consumer: the `culling_scores` table, then flags, ratings, labels, collections, and stacks.
**Treatment:** Lightroom's Assisted Culling dialog with select and reject criteria and a results grid with Selects, Rejects, and All, badges with hover reasons on thumbnails, and per-photo and per-face scores with a manual override. Cheaper substitute that fails the checkpoint: verdicts applied as final flags with no reasons, which `CullingResultCommandTests` catch.
**Chrome:** consume §2's faces and landmarks, §5's similarity for auto-stacking, §1's send plans, the culling commands of `D04 T01 §11`, the grid badges of `D04 T01 §8`, and `D04 T11 §1`'s job engine. No second flag or rating command.

**Requires:** display-session -- the culling dialog and review need an interactive desktop

- [ ] Add `CullingAnalyzer` in `src/Lumen/Photon.Lumen.Core/AI/Culling/`: subject focus as the variance of the Laplacian inside the largest face box from §2 or a center-weighted region, eye focus on landmark crops, exposure clipping statistics, and misfire detection (near-black, near-uniform, or extreme blur frames), all local (LP-0295). Done when: `CullingAnalyzerTests` separate the committed sharp and blurred fixtures and flag the misfire fixtures.
- [ ] Add eyes-open and document checks through the vision model with the schema `culling.v1.json` (per face: open, closed, or cannot tell; per photo: document or not), sending face crops or thumbnails only when `Lumen.AI.Culling.EyeState` or `DocumentCheck` is on, the face-crop caution in the preview (LP-0295, LP-0296, LP-0297). Done when: `EyeStateSendTests` assert nothing is sent with both off and the preview carries the caution with eye state on.
- [ ] Store scores in a `culling_scores` table (photo, face, metric, value, analyzer version, provenance id for model-assisted values) by a forward-only migration. Done when: a test round-trips a photo's scores.
- [ ] Add background analysis on `D04 T11 §1` with an enable setting and start and pause (LP-0295), the catalog setting `Lumen.AI.Culling.Enabled` (LP-0422), and analysis at import through `D04 T01 §6`'s import completion hook (LP-0728). Done when: a test imports three fixtures with analysis on and three score rows exist.
- [ ] Add the Assisted Culling dialog's select criteria (subject and eye focus thresholds, eyes open, only photos with eyes, include cannot-tell) and reject criteria (exposure issues, misfires, documents and receipts) (LP-0296, LP-0297). Done when: a view-model test applies criteria to fixture scores and gets the expected selects and rejects.
- [ ] Add the results grid (Selects, Rejects, All) with auto stack of similar shots through §5, batch flag, rating, and label through `D04 T01 §11`, add to or remove from a collection, and remove rejects from the catalog (records only, after a confirmation), each one undo step (LP-0298). Done when: `CullingResultCommandTests` flag 50 photos in one step, remove rejects, and assert every file's hash is unchanged.
- [ ] Add per-photo information: scores, per-face eyes open and eye sharpness, and a manual select or reject override as an undoable command (LP-0299). Done when: a test overrides a reject and undo restores it.
- [ ] Add culling badges on grid thumbnails through `D04 T01 §8`'s badge slots with hover reasons naming the metrics that decided the verdict (LP-0294). Done when: a view-model test reads a badge's reason text for a blurred fixture.
- [ ] Measure and quote analysis of a 200-photo fixture set on the reference machine. Done when: `CullingBudgetTests` (`[Trait("Category", "Budget")]`) print the time.
- [ ] Update `docs/user/lumen/ai.md` with assisted culling, what it sends when eye state or documents are on, and overrides. Done when: every control is described.
- [ ] Commit captures of the dialog, the results grid, and a badge with its reason under `docs/captures/lumen/culling/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: assisted culling with local scores and optional eye-state checks"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~CullingAnalyzerTests|FullyQualifiedName~EyeStateSendTests|FullyQualifiedName~CullingResultCommandTests|FullyQualifiedName~CullingBudgetTests"` exits 0 over the recorded transport; a driven cull of a 200-photo fixture set is captured with the time quoted. Cheaper substitute that fails: opaque verdicts, which the per-photo score and reason assertions catch.

## 7. AI Masks in Develop

A photographer masks the sky or a person's skin in one click and refines it like any other mask. Vision models locate well and cut poorly, so the model returns only boxes, points, and labels as JSON through the locate schema, and the local segmentation engine Imago built (GrabCut, the guided filter, and the matting solvers, `D03 T10 §6`) cuts the mask at develop resolution. Both move to `Photon.Core` here as their second consumer. The result is an `AiMaskComponent` (the `D01 T07 §4` kind `D03 T19 §15` added) storing the locate reply, the cut parameters, and a cached mask in the AI data store, so it re-renders at any resolution and recomputes only by an explicit send. Catalog: LP-0729 to LP-0733 (5 features). -> SOURCE: parity-lumen-ai-masks

**Fidelity:** Lumen masking panel -- docs/captures/lumen/masking/ (the `D04 T09 §9` baseline); new captures to docs/captures/lumen/ai-masks/.
**Job:** a photographer can mask a subject, the sky, the background, landscape regions, objects, or parts of people in one click and refine them like any mask. Consumer: the edit stack's `DevelopSettings.Masks`.
**Treatment:** Lightroom's Subject, Sky, Background, Objects (brush or box), People (with parts), and Landscape entries in the masking panel's create menu, an Update All command, and outdated-mask warnings. Cheaper substitute that fails the checkpoint: masks returned as model bitmaps at model resolution, which `AiMaskComponentTests` catch.
**Chrome:** consume the moved segmentation engine and `VisionLocator`, `D01 T07 §4`'s `AiMaskComponent`, `D04 T09 §9`'s masking panel, and §1's send plans and data store. No segmentation code in Lumen.

**Requires:** display-session -- the masking entries need an interactive desktop

- [ ] Move first: `GrabCut`, `GlobalMatting`, `ClosedFormMatting`, and the `MaxFlow` graph from `src/Imago/Photon.Imago.Core/Selection/Segmentation/` to `src/Photon.Core/Imaging/Segmentation/` with their tests, consuming the one `GuidedFilter` that `D03 T10 §6` already built in `src/Photon.Core/Imaging/Filters/` (corrected 2026-09-27 at integration: it never lived in Imago); Imago repoints, and `D03 T10 §6` gets a **Corrected 2026-09-27** note naming this section. Done when: `grep -rn "class GrabCut\|class GuidedFilter" src` prints one path each, under `src/Photon.Core/`, and Imago's segmentation tests pass.
- [ ] Move the `locate.v1.json` schema and `VisionLocator` from `src/Imago/Photon.Imago.Core/AI/` to `src/Photon.Core/AI/Vision/`; Imago repoints, and `D03 T19 §6` gets a **Corrected 2026-09-27** note. Done when: `grep -rn "class VisionLocator" src` prints one path, under `src/Photon.Core/`, and Imago's AI selection tests pass over their recorded replies.
- [ ] Add `SegmentationMoveArchitectureTests`: no type under `src/Photon.Core/Imaging/Segmentation/` or `src/Photon.Core/AI/Vision/` references an Imago, Lumen, or WPF type. Done when: the test passes and fails on a planted reference.
- [ ] Add `LumenAiMaskService` in `src/Lumen/Photon.Lumen.Core/AI/Masks/`: build the send plan from the develop preview, request a locate reply, cut with the moved engine at develop resolution, store the reply, cut parameters, and cached mask (by hash in the AI data store) in an `AiMaskComponent`, and write provenance. Done when: `AiMaskComponentTests` turn a recorded locate reply into the same mask at two resolutions within 1/255.
- [ ] Add subject, sky, and background masks (LP-0730). Done when: a test creates each from a recorded reply as one step.
- [ ] Add landscape masks (sky, snow, architecture, vegetation, water, ground, mountains), combined into one mask or separate masks per class (LP-0731). Done when: a test creates the separate form and gets one mask per class present in the recorded reply.
- [ ] Add object masks by brushing or drawing a box, with add, subtract, show, feather, and shift refinement (LP-0732). Done when: a test boxes an object from a recorded reply and subtracting a stroke removes that region.
- [ ] Add people masks with parts (entire person, skin, eyebrows, eyes, lips, teeth, hair, clothes) for one or several people (LP-0733). Done when: a test creates a skin and hair mask for two people from a recorded reply.
- [ ] Enable the AI entries `D04 T09 §9` disabled with "Planned: D04 T10 §7", each creation one send with its preview and one edit-stack step. Done when: `MaskPanelViewModelTests` find the entries enabled and a creation sends exactly one request.
- [ ] Add recompute on copy, sync, presets, and Focus on Subject: pasted AI components are marked "needs recompute" and recompute only through a batched send preview; Update All recomputes the photo's AI masks; a mask whose source hash changed (geometry, crop, or a large exposure change) shows an outdated warning (LP-0729). Done when: `OutdatedMaskTests` and `AiMaskPasteTests` assert nothing is sent on paste and one batched preview on Update All.
- [ ] Render existing AI masks offline from the cache, and refuse creation offline with "AI masks need a network connection; existing masks still render". Done when: a test renders a cached mask with the network probe offline and asserts the refusal for a new one.
- [ ] Update `docs/user/lumen/develop.md` with AI masks, what each sends, and recompute. Done when: every entry is described.
- [ ] Commit captures of each AI mask kind and an outdated warning under `docs/captures/lumen/ai-masks/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: AI masks in develop on the shared segmentation engine"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~SegmentationMoveArchitectureTests|FullyQualifiedName~AiMaskComponentTests|FullyQualifiedName~OutdatedMaskTests|FullyQualifiedName~AiMaskPasteTests|FullyQualifiedName~MaskPanelViewModelTests"` exits 0 over recorded replies and `grep -rn "class GrabCut\|class VisionLocator" src` prints one path each; a driven sky mask is captured. Cheaper substitute that fails: model bitmaps, which the two-resolution test catches.

## 8. Enhance: Denoise, Raw Details, and Super Resolution

A photographer cleans high-ISO raws and enlarges a crop for print without touching the original. Denoise and raw details are classical (the engine's noise reduction and the decoder's best demosaic); super resolution goes through the image-generation adapter and upscale service Imago built, which move to `Photon.Core/AI/Images/` here, with a classical detail-preserving fallback that needs no network. Every output is a new DNG or TIFF stacked with its source; a machine-learning denoiser is backlog B-046. Catalog: LP-0734 to LP-0742 (9 features). -> SOURCE: parity-lumen-enhance

**Freeze check:** Enhance only reads sources and writes new files (`<name>-Enhanced-NR.dng`, `<name>-Enhanced-RD.dng`, `<name>-Enhanced-SR.dng`, or the TIFF form) through the `D04 T13 §7` DNG writer or the TIFF writer over `AtomicFileWriter`; "replace original" in a batch becomes a new file stacked with the original; `EnhanceOutputTests` assert every source's SHA-256 and last-write time are unchanged, including after a cancelled batch, which leaves no partial output. Fixture source: `tests/fixtures/lumen/ai/enhance/`.

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/enhance/.
**Job:** a photographer can denoise, recover raw detail, and enlarge photos as new files without touching the originals. Consumer: new files in the catalog, stacked with their sources.
**Treatment:** Lightroom's Enhance dialog (Denoise, Raw Details, Super Resolution) with a preview of the first photo, show original, zoom, and output options, a headless Enhance with the last settings, and ACDSee's Denoise and Super Resolution dialogs with batch output options and target sizes. Cheaper substitute that fails the checkpoint: replacing the original, which `EnhanceOutputTests` refuse.
**Chrome:** consume the moved adapter and upscale service, `D01 T07 §3`'s noise reduction, `D04 T11 §1`'s jobs and `D04 T11 §5`'s size math, `D04 T13 §7`'s DNG writer, `D04 T06 §3` stacks, and §1's send plans. No upscaler in Lumen.

**Requires:** display-session -- the Enhance dialogs need an interactive desktop

- [ ] Move first: `GenerationRequestBuilder`, `GenerationCompositor`, `ImageModelCaps`, and `UpscaleService` from `src/Imago/Photon.Imago.Core/AI/` to `src/Photon.Core/AI/Images/`, and the `DetailPreservingUpscaler` `D03 T08 §7` built beside the resampler to `src/Photon.Core/Imaging/` if it lives under `src/Imago/`; Imago repoints, and `D03 T19 §2` and `D03 T19 §8` get **Corrected 2026-09-27** notes naming this section. Done when: `grep -rn "class UpscaleService\|class GenerationCompositor" src` prints one path each, under `src/Photon.Core/`, and Imago's upscale tests pass over their recorded replies.
- [ ] Add `UpscaleMoveArchitectureTests`: no type under `src/Photon.Core/AI/Images/` references an Imago or WPF type. Done when: the test passes and fails on a planted reference.
- [ ] Add the Enhance dialog in `src/Lumen/Photon.Lumen.Desktop/AI/Enhance/`: Denoise, Raw Details, and Super Resolution choices, a live preview of the first photo with show original and zoom, output options, apply once, and headless Enhance with the last settings (LP-0735). Done when: `EnhanceDialogViewModelTests` assert each option reaches the job and headless reuses the last settings.
- [ ] Run Enhance as background jobs on `D04 T11 §1` with progress and cancel (LP-0735). Done when: a test cancels a job and no output file exists.
- [ ] Add Denoise for Bayer, X-Trans, linear DNG, and small raw files: `D01 T07 §3`'s noise reduction at the dialog's strength on the demosaiced linear data, written as a linear DNG, with a tooltip naming B-046 for a machine-learning denoiser (LP-0736, LP-0739). Done when: `EnhanceOutputTests.Denoise` writes a DNG whose noise variance on the committed high-ISO fixture is below the source's.
- [ ] Add Raw Details: the decoder's highest-quality demosaic (the option recorded by `D04 T01 §3`'s decoder decision) written as a linear DNG (LP-0737). Done when: a test writes the DNG and its MTF50 on the slanted-edge fixture is at least the default demosaic's.
- [ ] Add Super Resolution to twice the linear size through the moved `UpscaleService`, tiled at `ImageModelCaps` limits with overlap and feathered seams, the tiles and cost in the send preview, the seed recorded with whether it was honored, and a 16,000 pixel limit refused by name (LP-0738, LP-0740). Done when: `SuperResolutionTilingTests` assemble recorded tile replies with seam deltas within the recorded tolerance and refuse an over-limit request.
- [ ] Add the classical fallback: the `DetailPreservingUpscaler` when offline or chosen, labeled in the dialog and in provenance. Done when: a test with the network probe offline produces a 2x output through the fallback and records it.
- [ ] Add target sizes (percentage, pixels to fit within, print size, long edge, short edge, preserve aspect ratio) sharing `D04 T11 §5`'s size math (LP-0742). Done when: `SuperResolutionTargetSizeTests` assert each mode's output dimensions.
- [ ] Add batch Enhance: many photos with a preview of the first, output to the same folder, a chosen folder, or a subfolder, rules for existing outputs (skip, uniquify, replace the earlier output, never the source), preserve dates, metadata, and catalog data, and saved presets with shortcuts (LP-0741). Done when: `EnhanceBatchTests` run five raws and assert five new files with copied ratings and keywords.
- [ ] Add the enhanced keyword (`Lumen.AI.EnhancedKeyword`, default "Enhanced") to outputs (LP-0734). Done when: a test finds the keyword on each output.
- [ ] Catalog and stack every output with its source through `D04 T06 §3`, with a provenance record for super resolution. Done when: `EnhanceOutputTests` assert the stack, the provenance row, and the sources' unchanged hashes.
- [ ] Add a tooltip on the detail panel of `D04 T09 §5` opening the Enhance dialog. Done when: a view-model test asserts the command.
- [ ] Update `docs/user/lumen/ai.md` with Enhance, what super resolution sends, and the classical fallback. Done when: every control is described.
- [ ] Commit captures of the Enhance dialog, the batch options, and a stacked output under `docs/captures/lumen/enhance/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: Enhance with denoise, raw details, and super resolution as new files"`

**Test checkpoint:** Format fidelity proof plus unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~UpscaleMoveArchitectureTests|FullyQualifiedName~EnhanceDialogViewModelTests|FullyQualifiedName~EnhanceOutputTests|FullyQualifiedName~SuperResolutionTilingTests|FullyQualifiedName~SuperResolutionTargetSizeTests|FullyQualifiedName~EnhanceBatchTests"` exits 0 over the recorded transport: output DNGs read back with their expected dimensions and every source's hash unchanged; a driven batch of five raws writes five DNGs stacked with their originals, captured. Cheaper substitute that fails: overwriting originals, which the hash assertions refuse.

## 9. Generative and Distraction Removal

A photographer removes a tourist or a reflection and can switch variations or revert at any time. Generative removal is develop spot data: the region in normalized coordinates, the prompt template hash, the variations as cached patches in the AI data store, and the selected index, composited at render time, so deleting the spot restores the render bit for bit. The distraction finder Imago built moves to `Photon.Core` beside the adapter moved by §8. Catalog: LP-0743 to LP-0745 (3 features). -> SOURCE: parity-lumen-generative-remove

**Fidelity:** Lumen Remove tool -- docs/captures/lumen/remove/ (the `D04 T09 §10` baseline); new captures to docs/captures/lumen/generative-remove/.
**Job:** a photographer can remove a person, a reflection, or dust with generated fill, switch between variations, and revert any time. Consumer: the edit stack's `DevelopSettings.Spots`.
**Treatment:** Lightroom's Remove tool with the Generative AI option, variation arrows, Delete and Report on a variation, object detection while brushing, and Distraction Removal buttons (People, Reflections, Dust) with a review list. Cheaper substitute that fails the checkpoint: generated pixels baked into the photo, which `GenerativeSpotTests` catch.
**Chrome:** consume the moved adapter (§8), `DistractionFinder`, `VisionLocator` and the segmentation engine (§7), `D04 T09 §10`'s Remove tool, and `D04 T09 §10`'s moved content-aware provider. No generation code in Lumen.

**Requires:** display-session -- the Remove tool needs an interactive desktop

- [ ] Move first: `DistractionFinder` from `src/Imago/Photon.Imago.Core/AI/Removal/` to `src/Photon.Core/AI/Removal/`; Imago repoints, and `D03 T19 §9` gets a **Corrected 2026-09-27** note naming this section. Done when: `grep -rn "class DistractionFinder" src` prints one path, under `src/Photon.Core/`, and Imago's distraction tests pass.
- [ ] Add a generative spot kind to `D01 T07 §5`'s spot data in `src/Photon.Core/Develop/Spots/` (engine code): region in normalized coordinates, prompt template hash, variation patch hashes, selected index, and provenance id, composited at render time by `GenerationCompositor`, with a **Corrected 2026-09-27** note in `D01 T07 §5` naming this section (LP-0743). Done when: `GenerativeSpotTests.RevertIsBitIdentical` deletes the spot and the render equals the pre-spot render byte for byte.
- [ ] Enable the Generative option `D04 T09 §10` disabled with "Planned: D04 T10 §9": brushing a region sends a context-padded masked crop through `GenerationRequestBuilder` with its preview and returns three variations cached as PNG patches in the AI data store (LP-0743). Done when: `GenerativeSendPreviewTests` assert only the masked crop's bytes leave and three patches are stored.
- [ ] Add variation controls: previous and next, generate more, delete a variation, and Report (marks the variation unacceptable in its provenance record with a reason, excludes it from cycling, and sends nothing), plus switching a selected spot's mode between heal, clone, remove, and generative (LP-0743). Done when: `VariationCycleTests` cycle, delete, and report variations as undoable steps with zero requests for Report.
- [ ] Add object detection while brushing a removal: locate within the brushed area through `VisionLocator`, cut with the segmentation engine, and refine with add and subtract strokes before generating (LP-0744). Done when: a test brushes over a recorded reply's object and the region equals the cut mask.
- [ ] Add Distraction Removal for people, reflections, and dust through `DistractionFinder`, listed for review with each accepted item removed by a generative or content-aware spot, and rerun per photo on paste only through a send preview (LP-0745). Done when: `DistractionReviewTests` accept two of three recorded detections and two spots result; a paste sends nothing until previewed.
- [ ] Render existing generative spots offline from the cache and refuse new ones offline by name. Done when: a test renders a cached spot with the network probe offline and asserts the refusal.
- [ ] Update `docs/user/lumen/develop.md` with generative removal, variations, and distraction removal, and what each sends. Done when: every control is described.
- [ ] Commit captures of a removal with three variations and the distraction review list under `docs/captures/lumen/generative-remove/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: generative and distraction removal as develop data"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~GenerativeSpotTests|FullyQualifiedName~GenerativeSendPreviewTests|FullyQualifiedName~VariationCycleTests|FullyQualifiedName~DistractionReviewTests"` exits 0 over recorded replies; a driven removal with three variations is captured. Cheaper substitute that fails: baked pixels, which `RevertIsBitIdentical` catches.

## 10. Lens Blur and Depth

A portrait photographer softens the background with believable bokeh and says where focus falls. Depth comes from the photo when it carries one (HEIC depth auxiliary images and portrait depth maps, read locally) and is estimated otherwise through the depth estimator Imago built, moved here to `Photon.Core/AI/Depth/`, and always labeled "estimated, not measured". The blur itself is a develop stage over the bokeh kernels of `D01 T06 §3`, added to the engine because no develop stage may live under `src/Lumen/`. Catalog: LP-0746 to LP-0749 (4 features). -> SOURCE: parity-lumen-lens-blur

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/lens-blur/.
**Job:** a portrait photographer can blur the background with believable bokeh and choose where focus falls. Consumer: the edit stack's `DevelopSettings`.
**Treatment:** Lightroom's Lens Blur panel (the tool strip entry `D04 T09 §1` reserved) with Apply, amount, the focal range on a depth histogram, subject focus, point or area focus, Visualize Depth, focus and blur brushes, and bokeh shapes with boost, plus Depth Range masks in the masking panel. Cheaper substitute that fails the checkpoint: a uniform background blur, which `LensBlurStageTests` catch.
**Chrome:** consume the moved `DepthEstimator`, `D01 T06 §3`'s bokeh kernels, `D01 T07 §4`'s `DepthRange` component, §7's subject masks, and §1's data store. No blur kernel in Lumen.

**Requires:** display-session -- lens blur and Visualize Depth need an interactive desktop

- [ ] Move first: `DepthEstimator` from `src/Imago/Photon.Imago.Core/AI/Depth/` to `src/Photon.Core/AI/Depth/`; Imago repoints, and `D03 T19 §14` gets a **Corrected 2026-09-27** note naming this section. Done when: `grep -rn "class DepthEstimator" src` prints one path, under `src/Photon.Core/`, and Imago's depth tests pass.
- [ ] Add `DepthSource` resolution in `src/Lumen/Photon.Lumen.Core/AI/Depth/`: the HEIC depth auxiliary image through the shared codec registry and a JPEG portrait depth map (`GDepth` XMP) read locally first, the estimator otherwise through a send preview, cached in the AI data store and labeled "Depth is estimated, not measured" when estimated. Done when: `DepthSourceTests` prefer the embedded depth of a committed HEIC fixture and label an estimated one.
- [ ] Add `LensBlurStage` in `src/Photon.Core/Develop/Effects/` (engine code): a depth-driven blur over `D01 T06 §3`'s bokeh kernels with amount, focal range, and brush refinements in normalized coordinates, with a schema group and a **Corrected 2026-09-27** note in `D01 T07 §4` naming this section. Done when: `LensBlurStageTests` assert amount 0 is the identity within 1/65535 and pixels inside the focal range stay within 1/255 while those outside blur.
- [ ] Add the Lens Blur panel: Apply, amount, the focal range dragged on a depth histogram, subject focus from §7's subject mask, point or area focus by clicking, and Visualize Depth as a separate overlay buffer (LP-0747). Done when: `LensBlurSettingsTests` assert each control writes its setting and the overlay never enters the render.
- [ ] Add focus and blur brushes that refine the depth map as vector strokes (LP-0747). Done when: a test paints a focus stroke and the stroke is stored as points and the pixels under it stay sharp.
- [ ] Add bokeh shapes (circle, bubble, five-blade, ring, anamorphic, cat eye) and boost (LP-0748). Done when: `BokehShapeTests` render a point light per shape and match each kernel's footprint.
- [ ] Enable the Depth Range entry `D04 T09 §9` disabled with "Planned: D04 T10 §10": `DepthRange` components over the resolved depth source, flagged estimated where it is (LP-0746). Done when: a test creates a depth range mask on the HEIC fixture and on an estimated one with the flag.
- [ ] Add blur-background adaptive presets and focus on subject recomputed on paste through a send preview when the depth or subject must be re-estimated (LP-0749). Done when: a test pastes onto a second photo and nothing is sent until previewed.
- [ ] Enable the Lens Blur tool strip entry of `D04 T09 §1`. Done when: `DevelopToolStripTests` find the entry enabled.
- [ ] Update `docs/user/lumen/develop.md` with lens blur, depth sources, and depth range masks. Done when: every control is described.
- [ ] Commit captures of a portrait blur, Visualize Depth, and each bokeh shape under `docs/captures/lumen/lens-blur/`, with the depth fixtures in `tests/fixtures/lumen/ai/depth/` and their `reference.txt`. Done when: the folders hold them.
- [ ] Commit: `"lumen: lens blur from embedded or estimated depth"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~DepthSourceTests|FullyQualifiedName~LensBlurStageTests|FullyQualifiedName~LensBlurSettingsTests|FullyQualifiedName~BokehShapeTests"` exits 0; a driven portrait blur with Visualize Depth is captured. Cheaper substitute that fails: a uniform blur, which `LensBlurStageTests` catch by the focal-range assertion.

## 11. Adaptive Presets, AI Auto Settings, and Natural-Language Search

A photographer applies a look that adapts to each photo's subject and finds photos by describing them. Adaptive presets store AI mask recipes that §7 recomputes per photo on apply; the adaptive color profile is local scene analysis over the engine's own profiles, no model and no Adobe profile; AI auto settings propose `DevelopSettings` deltas as JSON validated against a whitelist and applied as one undoable step; natural-language search runs locally over descriptions the user chose to generate (§4), with an optional text-only request that turns a sentence into structured criteria. Catalog: LP-0750, LP-0751 (2 features). -> SOURCE: parity-lumen-adaptive

**Fidelity:** Lumen presets panel -- docs/captures/lumen/presets/ (the `D04 T02 §5` baseline); new captures to docs/captures/lumen/adaptive/.
**Job:** a photographer can apply a look that adapts to each photo's subject and find photos by describing them. Consumer: the edit stack (presets, auto settings) and the search results.
**Treatment:** Lightroom's Adaptive preset groups (Subject, Sky, Portrait, Landscape), an Adaptive entry in the profile browser, an AI Auto button beside the classical Auto of `D04 T09 §3`, and a search field accepting sentences. Cheaper substitute that fails the checkpoint: presets with fixed masks, which `AdaptivePresetRecipeTests` catch.
**Chrome:** consume §7's mask service, §4's descriptions, `D04 T09 §11`'s presets panel, `D04 T06 §7`'s search, and `D01 T05 §1` structured output. No second preset store.

**Requires:** display-session -- adaptive presets and the search field need an interactive desktop

- [ ] Add `AdaptivePreset` in `src/Lumen/Photon.Lumen.Core/AI/Adaptive/`: a `D01 T07 §6` preset plus AI mask recipes (mask kind and its local adjustment set), stored beside the preset in the preset store's folder as JSON (LP-0751). Done when: `AdaptivePresetRecipeTests` round-trip a recipe and list it in the presets panel.
- [ ] Apply an adaptive preset to one or many photos: recompute each recipe's mask through §7 under one batched send preview, then apply the adjustments, as one batch undo step with provenance (LP-0751). Done when: a test applies a portrait preset to three photos over recorded replies and one undo reverts all three.
- [ ] Author Lumen's own adaptive preset groups (Subject, Sky, Portrait, Landscape) in `src/Lumen/Photon.Lumen.Core/AI/Adaptive/Builtin/`, no vendor content (LP-0751). Done when: a test loads every built-in recipe.
- [ ] Add the adaptive color profile: local analysis of the histogram, color statistics, and detected faces choosing and blending the engine's built-in profiles and amount into a per-photo Adaptive entry in the profile browser, with no model call (LP-0750). Done when: `AdaptiveProfileTests` produce deterministic settings for three fixtures and record zero network requests.
- [ ] Add AI auto settings: a vision request with the schema `autosettings.v1.json` returning deltas for a whitelist of global parameters with their ranges, out-of-range values refused by name, applied as one step with provenance, beside the classical Auto. Done when: `AiAutoSettingsValidationTests` apply a valid recorded reply and refuse one with an out-of-range exposure by name.
- [ ] Add natural-language search: an FTS5 index over stored AI descriptions and accepted AI keywords, a sentence query matched locally, a note stating how many photos have descriptions, and an optional Interpret with AI that sends only the sentence text (with its preview) and returns structured `D04 T06 §7` criteria. Done when: `DescriptionSearchTests` find the fixture "red car at night" photo locally and turn a recorded interpretation into criteria.
- [ ] Update `docs/user/lumen/ai.md` with adaptive presets, the adaptive profile, AI auto settings, and natural-language search. Done when: every control is described.
- [ ] Commit captures of the adaptive groups, an adaptive portrait across three photos, and a sentence search under `docs/captures/lumen/adaptive/`. Done when: the folder holds them.
- [ ] Commit: `"lumen: adaptive presets, AI auto settings, and natural-language search"`

**Test checkpoint:** Unit test plus driven run with evidence: `dotnet test Photon.slnx --filter "FullyQualifiedName~AdaptivePresetRecipeTests|FullyQualifiedName~AdaptiveProfileTests|FullyQualifiedName~AiAutoSettingsValidationTests|FullyQualifiedName~DescriptionSearchTests"` exits 0 over recorded replies; a driven adaptive portrait preset across three photos is captured. Cheaper substitute that fails: fixed masks, which `AdaptivePresetRecipeTests` catch.

## 12. Faces in the Viewer and Face Regions in XMP

Split from §3 at authoring (2026-09-27) so the People surface stays reviewable in one pass. Faces are shown and named where the photo is being looked at (the library loupe and the Lumen Viewer), with a face tool to draw or correct outlines, and face data interchanges with other tools: regions are read and written as Metadata Working Group regions in XMP sidecars, and existing face data from Lightroom, digiKam, Picasa, Windows Photo Gallery, and ACDSee is imported when photos are cataloged. Nothing about a face leaves the machine. Catalog: LP-0421, LP-0703, LP-0708, LP-0710, LP-0711, LP-0715 (6 features). -> SOURCE: parity-lumen-face-regions

**Freeze check:** Face regions reach disk only through `D04 T08 §8`'s `MetadataWriter`: the XMP sidecar when `Lumen.Metadata.WriteSidecars` is on or on the explicit Write Face Regions command, a supported original only when `Lumen.Originals.InPlace.EmbedMetadata` is on (`D04 T08 §9`), and exported copies through `D04 T12 §13`; importing face data only reads; `MwgRegionsRoundTripTests` and `FaceImportTests` assert every fixture original's SHA-256 is unchanged. Fixture source: `tests/fixtures/lumen/faces/regions/`.

**Fidelity:** new build, no baseline; captured to docs/captures/lumen/face-tool/.
**Job:** a user can see and name faces while viewing a photo, and keep face names when moving between Lumen and other photo tools. Consumer: the `faces` and `people` tables and XMP sidecars.
**Treatment:** face outlines on the loupe and in the Lumen Viewer, a faces pane, ACDSee's face tool with Enter and Tab naming and suggestion confirm and deny, and Metadata, Write Face Regions; face data imported silently while cataloging with a summary. Cheaper substitute that fails the checkpoint: face tags stored only in Lumen with no MWG exchange, which `MwgRegionsRoundTripTests` catch.
**Chrome:** consume §2's engine and §3's naming commands, `D04 T04 §9`'s viewer information tools, the loupe of `D04 T01 §9`, `D01 T07 §6`'s `XmpPacket`, and `D04 T08 §8`'s writer. No second XMP writer.

**Requires:** display-session -- the face tool and viewer overlays need an interactive desktop

- [ ] Add face outlines in the library loupe and the Lumen Viewer with names, toggled by `Lumen.Faces.ShowOutlines`, and a faces pane listing the current photo's faces (LP-0703, LP-0708). Done when: `ViewerFacesTests` show a fixture's outlines at the stored boxes.
- [ ] Detect faces as each photo opens in the Lumen Viewer (`Lumen.Viewer.DetectFaces`), in the background after the first paint, reading the face index when the photo is cataloged or browsed, with OpenCV loaded lazily so `D04 T04 §1`'s first-paint assembly allow-list is unchanged (LP-0708). Done when: `ViewerFacesTests.AllowListUnchanged` asserts the allow-list and a background detection on an uncataloged fixture.
- [ ] Report unsupported locations: a photo outside the catalog and outside browsed folders shows "Faces can be named for cataloged or browsed photos; add this folder to name faces" (LP-0708). Done when: a test opens an outside file and reads the message.
- [ ] Add the face tool in the loupe and the viewer: draw or edit an outline (a Manual face), name with Enter and Tab to the next face, confirm, deny, or edit suggestions inline, and a note when auto naming is off (LP-0711). Done when: `FaceToolTests` draw and name a face by keyboard and the catalog holds a Manual face with the name.
- [ ] Add `MwgRegionsCodec` in `src/Lumen/Photon.Lumen.Core/Faces/Xmp/`: read and write `mwg-rs:Regions` (region list with normalized `stArea` x, y, w, h, type Face, name, and `AppliedToDimensions`) through `XmpPacket`, keeping unknown fields (LP-0710, LP-0715). Done when: `MwgRegionsRoundTripTests` round-trip a Lightroom-written sidecar with unknown fields byte-stable after canonicalization.
- [ ] Convert between catalog coordinates and MWG's oriented-image coordinates for every EXIF orientation. Done when: a test writes and rereads regions for all eight orientations and each lands on the same face.
- [ ] Add Write Face Regions and automatic writing through `D04 T08 §8` when `Lumen.Metadata.WriteSidecars` is on, and include regions in exported copies through `D04 T12 §13` (LP-0715). Done when: exiftool 13 reads the names from a written sidecar and from an exported copy.
- [ ] Import face data when cataloging (through `D04 T01 §6` import and `D04 T05 §2` indexing): MWG regions (Lightroom, digiKam, Picasa 3.9, Lumen), Microsoft `MP:RegionInfo`, and ACDSee's region namespace as found in committed ACDSee fixtures, creating or matching people and marking the faces Confirmed (LP-0710, LP-0421). Done when: `FaceImportTests` import each fixture's names and none duplicates a person.
- [ ] Import Picasa's `.picasa.ini` face rectangles (`rect64`) with names from `contacts.xml` when present (LP-0421). Done when: `FaceImportTests.PicasaIni` imports the committed fixture's two named faces at their rectangles.
- [ ] Compute embeddings for imported faces locally through §2's queue so recognition learns from them. Done when: a test imports a named face and its embedding row appears after the queue runs.
- [ ] Log one Serilog Information line per region write and per import summary. Done when: a test logger asserts both.
- [ ] Update `docs/user/lumen/people.md` with the face tool, viewer faces, and face region exchange. Done when: every control is described.
- [ ] Commit captures of the face tool in the loupe and the viewer and the faces pane under `docs/captures/lumen/face-tool/`, with the region fixtures and their `reference.txt` naming the writing application and version. Done when: the folders hold them.
- [ ] Commit: `"lumen: faces in the viewer and MWG face regions"`

**Test checkpoint:** Format fidelity proof plus unit test: `dotnet test Photon.slnx --filter "FullyQualifiedName~ViewerFacesTests|FullyQualifiedName~FaceToolTests|FullyQualifiedName~MwgRegionsRoundTripTests|FullyQualifiedName~FaceImportTests"` exits 0: a Lightroom-written sidecar round-trips byte-stable in unknown fields after canonicalization, and every import fixture yields its names; a driven session names five faces in the viewer and exiftool 13 output of the sidecars is quoted. Cheaper substitute that fails: Lumen-only tags, which the MWG round trip catches.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Photon.slnx --filter "FullyQualifiedName~Photon.Lumen.Tests.AI|FullyQualifiedName~Photon.Lumen.Tests.Faces"` exits 0 with the network unavailable to the test host and every test class named in this file reporting
- [ ] No test reads an OpenRouter key from the environment or contacts `openrouter.ai`: `grep -rn "openrouter.ai" tests/` matches only fixture READMEs
- [ ] `grep -rn "class GrabCut\|class VisionLocator\|class UpscaleService\|class DistractionFinder\|class DepthEstimator" src` prints one path each, all under `src/Photon.Core/`
- [ ] `FacesNeverSentTests` and `SimilarityLocalTests` pass, and the unchanged-originals test of `D04 T02 §1` passes with every AI command run over the recorded transport
- [ ] `docs/user/lumen/ai.md` has one row per AI command in the AI menu, and every UI section's captures exist under `docs/captures/lumen/`
- [ ] `python scripts/todo-graph.py validate` clean
