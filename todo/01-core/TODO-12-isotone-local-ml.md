---
schema_version: 1
id: isotone-local-ml
domain: 01-core
status: draft
title: "TODO-12 -- Isotone.Core On-Device Models: ONNX Runtime, the Model Catalog, and the Model Manager"
depends_on: []
frozen: false
track: C12
---

# TODO-12 -- Isotone.Core On-Device Models: ONNX Runtime, the Model Catalog, and the Model Manager

> **Goal:** Every suite AI task that a local model can do (segmentation and saliency, inpainting, upscaling, denoise and deblur, depth, and the photo models Gesso adds) can run on the user's own machine, offline, as an alternative to its OpenRouter path: one runtime (ONNX Runtime with the DirectML execution provider and a CPU fallback) behind the same task seam the AI features already use (`D01 T05`), one model catalog whose every entry records its license and is refused unless that license is GPL-compatible or permissive, downloads only on an explicit user action with hash verification, and one Model Manager surface in `Isotone.UI` each app hosts in its AI settings. OpenRouter stays the default; local results write the same provenance record. Tests run on tiny fixture models and never download. This file exists because the operator promoted the on-device model work deferred to after the first release (operator decision 2026-09-27, planned so no feature is "left behind").

> [!IMPORTANT]
> **Current state (verified 2026-09-27):** There is no `src/Isotone.Core/` yet (`D01 T02 §1` creates it), so the AI core of `D01 T05` (`IAiClient`, `AiSendGate`, `ProvenanceRecord`) is planned, not built. No source file references ONNX Runtime or DirectML, and `Directory.Packages.props` has no ONNX package. Every AI task in the plan runs through OpenRouter (`D01 T05 §1`) or a classical algorithm (`D01 T06 §4` shake reduction, `D01 T06 §13` height-based normals, `D03 T15 §14` classical star separation, `D04 T10 §8` classical denoise); Albumen's face detection runs through an OpenRouter vision model (`D04 T10 §2`) and face recognition stays backlog B-052, which this file does not change.
<!-- claim: absent src/Isotone.Core -->
<!-- claim: count "OnnxRuntime" Directory.Packages.props = 0 -->
<!-- claim: count "OnnxRuntime|InferenceSession" src/**/*.cs = 0 -->

## Inputs

- [`standards/shared.md`](../../standards/shared.md) -- a dependency is a decision, settings with named consumers, progress and Cancel over one second, one log line per action
- [`docs/parity/gesso-parity.md`](../../docs/parity/gesso-parity.md) -- the on-device rows `D03 T19 §16` and `D03 T19 §17` own
- ONNX Runtime documentation (https://onnxruntime.ai/docs/) and the DirectML execution provider (https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html); DirectML (https://learn.microsoft.com/windows/ai/directml/dml)
- Model sources, each license re-verified by §2 at authoring of the manifest: MobileSAM (https://github.com/ChaoningZhang/MobileSAM, Apache-2.0), Segment Anything ViT-B (https://github.com/facebookresearch/segment-anything, Apache-2.0), U-2-Net (https://github.com/xuebinqin/U-2-Net, Apache-2.0), LaMa (https://github.com/advimman/lama, Apache-2.0), Real-ESRGAN (https://github.com/xinntao/Real-ESRGAN, BSD-3-Clause), NAFNet (https://github.com/megvii-research/NAFNet, MIT), Depth Anything V2 Small (https://github.com/DepthAnything/Depth-Anything-V2, Apache-2.0 for Small only), MiDaS (https://github.com/isl-org/MiDaS, MIT)
- -> XREF: D01 T05 §1 -- the AI client and task seam §1 routes beside
- -> XREF: D01 T05 §3 -- the provenance record local runs write
- -> XREF: D01 T05 §4 -- the AI settings page the Model Manager (§3) is embedded in
- -> XREF: D01 T02 §2 -- the settings store for backends, device, and the models folder
- -> XREF: D05 T01 §6 -- the first suite release, after which this file runs
- -> XREF: D03 T19 §16 -- Gesso on-device models cites §3: the Model Manager hosted in Gesso; §4: the segmentation and inpaint tasks behind select subject and the Remove tool
- -> XREF: D03 T19 §17 -- Gesso on-device photo models cites §1: the runner and §2: the catalog entries for deblur, mixed light, and SDR to HDR
- -> XREF: D04 T10 §13 -- Albumen on-device models cites §3: the Model Manager hosted in Albumen; §4: the denoise task
- -> XREF: D03 T21 §15 -- Gesso 1.3.0 releases this file's runtime, catalog, and Model Manager in Gesso
- -> XREF: D04 T15 §13 -- Albumen 1.3.0 releases this file's runtime, catalog, and Model Manager in Albumen

## Outcome

- `LocalModelRunner` runs any cataloged ONNX model on the DirectML device or the CPU, tiled with seams under 1/255 on flat fields, cancellable, and reports the device used.
- Each AI task has a backend setting (OpenRouter by default, or Local) and consumers call one API; a local run sends nothing over the network and writes a provenance record naming the model, version, SHA-256, license, and device.
- `models.json` lists every model with its task, source, size, SHA-256, and license, and a build-time test fails on any license outside the allow-list.
- Models download only on an explicit user action, verify their hash, and can be removed; `docs/dev/models.md` is generated from the manifest.
- The Model Manager in `Isotone.UI` lists models, their licenses, state, and disk use, and chooses the inference device and each task's backend.
- Segmentation, inpainting, upscaling, denoise, and depth adapters pass on tiny fixture models, and against the real model when it is installed.

**Adjacency:** list=applicable @ D01 T12 §3; document=not-applicable (nothing here prints; results land in the consuming app's document); settings=applicable @ D01 T12 §1; reporting=applicable @ D01 T12 §3; notifications=applicable @ D01 T12 §3; permissions=applicable @ D01 T12 §2; audit=applicable @ D01 T12 §1; exchange=not-applicable (model files are downloaded artifacts, not user documents; no user format is read or written here); reverse=applicable @ D01 T12 §2

**Adjacency rationale:** The model list with filters by task and state is the Model Manager (§3). Settings are `Isotone.AI.Backend.<Task>`, `Isotone.AI.Local.Device`, `Isotone.AI.Local.ModelsFolder`, and `Isotone.AI.Local.TileSize`, each read by the runner or router. Reporting is disk use per model and in total and the system requirements readout (§3). Download progress, completion, and failure reach the user through the shared progress and toast (§3). A refused license, a hash mismatch, too little disk space, and a device that fails to initialize are refusals by name (§2, §1). Every local run writes one Serilog Information line and a provenance record (§1). Removing a model is the reverse of downloading it (§2); results themselves are undone in the consuming app's history.

## Implementation Order

| Order | Section | Deliverable | Depends On | Status |
| :---: | :-----: | ----------- | ---------- | :----: |
|   1   |   §1    | The local inference runtime | D05 T01 §6, D01 T05 §1, D01 T05 §3 |  [ ]   |
|   2   |   §2    | The model catalog, downloads, and license records | §1 |  [ ]   |
|   3   |   §3    | The Model Manager surface in Isotone.UI | §2, D01 T05 §4 |  [ ]   |
|   4   |   §4    | Task adapters: segmentation, inpainting, upscaling, denoise, and depth | §1, §2 |  [ ]   |

---

## 1. The Local Inference Runtime

The AI features of all three apps run through OpenRouter today, which needs a network, a key, and a send preview. A user who works offline, or will not send an image anywhere, needs the same tasks on their own machine. This section records the runtime decision and builds the runner and the task router: ONNX Runtime with the DirectML execution provider (`Microsoft.ML.OnnxRuntime.DirectML`, MIT; DirectML itself MIT), with the CPU execution provider as the fallback, behind the task seam of `D01 T05` so each consumer calls one API and a per-task setting chooses OpenRouter (the default) or Local. A local run needs no send gate, because nothing leaves the machine, and a test with the network blocked proves it; it writes the same provenance record as a remote run. Tests use tiny fixture models generated by a committed script, never a download. Catalog: none of its own (`D03 T19 §16` and `D03 T19 §17` own the rows). -> SOURCE: parity-local-ml

**Fidelity:** no surface of its own (the device and backend choices are rendered by the Model Manager of §3)

- [ ] Record the runtime in `docs/dev/decisions.md`: ONNX Runtime with DirectML (MIT) and the CPU execution provider, why (one runtime for every model format the candidates publish, DirectX 12 GPUs of every vendor through DirectML, a CPU fallback in the same package), and the rejected options (TorchSharp with LibTorch, a 2 GB payload; Windows ML, which pins the ONNX opset to the OS build; per-model native runtimes). Done when: the row names both licenses and this section.
- [ ] Add `Microsoft.ML.OnnxRuntime.DirectML` to `Directory.Packages.props`, referenced by `Isotone.Core` only, with its native payload per runtime identifier (win-x64 and win-arm64) checked in the publish output. Done when: `dotnet publish` of each app lists `onnxruntime.dll` and `DirectML.dll` and the build is green.
- [ ] Add `src/Isotone.Core/AI/Local/LocalModelRunner.cs`: one `InferenceSession` per model id and version (cached, disposed on idle after `Isotone.AI.Local.IdleUnloadSeconds`, default 300), created with `AppendExecutionProvider_DML(adapterIndex)` then CPU, with `SessionOptions` for memory pattern off under DirectML as the docs require (https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html). Done when: `LocalModelRunnerTests.RunsFixtureModel` runs the identity fixture model and returns the input tensor unchanged.
- [ ] Select the device: `Isotone.AI.Local.Device` (Auto, a DirectML adapter by LUID, or CPU); Auto picks the adapter with the most dedicated memory, and a DirectML initialization failure falls back to CPU with one Warning line naming the adapter and the error. Done when: a test forcing a failing DirectML provider through a fake session factory asserts the CPU fallback and the log line.
- [ ] Add tiling in `LocalTiler`: tiles of `Isotone.AI.Local.TileSize` (default 512) with 32 px overlap blended by linear ramps, padding by reflection at image edges, for models with a fixed or bounded input size. Done when: `LocalTilerTests` run the identity model over a flat field three tiles wide and assert the seam delta is 0 and the output equals the input.
- [ ] Take `IProgress<double>` per tile and a `CancellationToken` observed between tiles (`RunOptions.Terminate` for a long single tile). Done when: `LocalModelRunnerTests.CancelStopsWithinOneTile` cancels after the first report and at most one more tile completes.
- [ ] Add `src/Isotone.Core/AI/AiTaskBackend.cs`: the task list (`Segmentation`, `Saliency`, `Inpaint`, `Upscale`, `Denoise`, `Deblur`, `Depth`, `StarSeparation`, `Normals`, `MixedLight`, `SdrToHdr`, `Tagging`, `Embedding`) and `Isotone.AI.Backend.<Task>` settings (OpenRouter by default; Local only when an installed model serves the task). Done when: `AiTaskBackendTests` assert the defaults and that choosing Local with no installed model reads back as OpenRouter with a reason.
- [ ] Add `src/Isotone.Core/AI/Local/LocalTaskRouter.cs`: given a task request, route to the OpenRouter path of `D01 T05 §1` or to the local adapter (§4), so consumers call `IAiTaskService.RunAsync(task, input)` and never branch themselves. Done when: a test with both fakes asserts the route follows the setting per task.
- [ ] Prove local runs send nothing: the local path never constructs the gated client and never calls `AiSendGate`, asserted with an `HttpMessageHandler` that fails the test on any call and with a socket-level guard in the test host. Done when: `LocalRunNetworkTests.NoNetwork` runs every task through fixture models with the network blocked and passes.
- [ ] Write a provenance record for every local run through `D01 T05 §3` with `origin: local`, the model id, version, SHA-256, license SPDX id, device (adapter name or CPU), tile size, and the input size; a re-run from the record reproduces the result bit-exactly on the same device. Done when: `LocalProvenanceTests` rebuild a run from its record and compare output hashes.
- [ ] Validate model inputs and outputs against the manifest's declared shapes and element types before running, refusing a mismatched model by name ("The model <id> does not match its catalog entry"). Done when: a test with a fixture model whose shape differs from its entry asserts the refusal.
- [ ] Commit `tests/fixtures/core/ml/make-fixtures.py` generating tiny ONNX models (identity, a 3 by 3 blur, a two-class threshold segmenter, a 2x nearest upscaler, a constant depth) with the `onnx` Python package at authoring time only (version recorded), and the generated `.onnx` files, each under 50 KB. Done when: rerunning the script reproduces every model byte-identically and `reference.txt` names the package version.
- [ ] Log one Serilog Information line per local run as the audit trail beside the provenance record (`AI local {Task} {Model} {Version} on {Device} {Width}x{Height} in {ElapsedMs} ms`), never an image or a path outside the log policy. Done when: a Serilog test logger asserts the line.
- [ ] Commit: `"core: the local inference runtime on ONNX Runtime with DirectML and a CPU fallback"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~LocalModelRunnerTests|FullyQualifiedName~LocalTilerTests|FullyQualifiedName~AiTaskBackendTests|FullyQualifiedName~LocalRunNetworkTests|FullyQualifiedName~LocalProvenanceTests"` exits 0 on the fixture models with the network blocked, proving zero network calls, seamless tiling, CPU fallback, and bit-exact re-runs from provenance. Cheaper substitute that fails: calling the local model from each consumer directly, which the router test and the provenance test catch.

## 2. The Model Catalog, Downloads, and License Records

A model is a dependency whose license travels with its weights, and Isotone is GPL-3.0: a model whose license is non-commercial or otherwise incompatible must never be offered, and every model the user installs must say where it came from. This section builds the manifest, the license policy that fails the build on an unapproved license, the explicit-action downloader with hash verification and removal, and the generated model table, and it verifies each candidate model per task. A task whose candidates all fail the license check does not get a quietly substituted model: its catalog rows are rerouted through `add-todo` with the evidence. Catalog: none of its own. -> SOURCE: parity-local-ml-catalog

**Fidelity:** no surface of its own (the Model Manager of §3 renders the catalog)

- [ ] Add `src/Isotone.Core/AI/Local/models.json` and `ModelManifest.cs`: per entry id, task, version, download URL, SHA-256, size, input and output tensor spec, preprocessing (normalization, channel order), license SPDX id, license URL, upstream repository, and notes. Done when: `ModelManifestTests` parse the manifest and every entry has every field.
- [ ] Add `ModelLicensePolicy` with the allow-list MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, CC0-1.0, Unlicense, Zlib, and GPL-compatible copyleft (GPL-3.0-only, GPL-3.0-or-later, LGPL-3.0-or-later), and a build-time test failing on any other SPDX id, including CC-BY-NC-4.0 and "OpenRAIL" variants. Done when: `ModelLicensePolicyTests` pass on the manifest and fail on a test manifest carrying CC-BY-NC-4.0.
- [ ] Verify and enter the segmentation candidates: MobileSAM (Apache-2.0) as the default point and box segmenter, Segment Anything ViT-B (Apache-2.0) as the higher-quality option, and U-2-Net (Apache-2.0) for saliency, each with its ONNX export's SHA-256 and the license text's URL checked by hand and recorded in the entry's notes with the date. Done when: three entries exist and pass the policy.
- [ ] Verify and enter the inpainting, upscaling, denoise, and deblur candidates: LaMa (Apache-2.0), Real-ESRGAN x2 and x4 (BSD-3-Clause), NAFNet SIDD denoise and NAFNet GoPro deblur (MIT). Done when: five entries exist and pass the policy.
- [ ] Verify and enter the depth candidates: Depth Anything V2 Small (Apache-2.0; the Base and Large weights are CC-BY-NC-4.0 and a test asserts they are refused) and MiDaS v3.1 small (MIT). Done when: two entries exist and the refusal test passes.
- [ ] Search for GPL-compatible or permissive candidates for star separation, normals from image, mixed-light correction, SDR-to-HDR expansion, image tagging, and image embeddings (for embeddings, OpenAI CLIP ViT-B/32, MIT), record each candidate examined with its license in `docs/dev/models.md`, and enter those that pass. Done when: every one of the six tasks has either a passing entry or a recorded "no candidate passed" line with the candidates and their licenses.
- [ ] Exit item: for each task left with no passing candidate, reroute its catalog rows (star separation IP-1580, normals IP-2109, mixed light IP-2107, SDR to HDR IP-2108) in `docs/parity/gesso-parity.md` through `add-todo` to a backlog entry with the evidence, in this section's commit, and tell the consuming sections `D03 T19 §16` and `D03 T19 §17` by that note. Done when: `python scripts/todo-graph.py validate` exits 0 and no catalog row names a local model that does not exist.
- [ ] Add `src/Isotone.Core/AI/Local/ModelDownloader.cs`: download only on an explicit user action (`UserActionId` from `D01 T05 §4`), over HTTPS with resume through `Range`, a disk-space check before starting, SHA-256 verification before the file is moved into place, and the license text saved beside the weights as `LICENSE.txt`. Done when: `ModelDownloaderTests` over a local test server assert resume, a hash mismatch refused and deleted, and no download without an action id.
- [ ] Store models under `Isotone.AI.Local.ModelsFolder` (default `%LOCALAPPDATA%\Rizonesoft\Isotone\models\<id>\<version>\`), shared by every app, with an `installed.json` index written atomically. Done when: a test installs a fixture model, reopens the index, and finds it; a second app instance reads the same index.
- [ ] Add remove (deleting the model folder and its index entry after a confirmation naming the model and size) and update (a newer manifest version offered, the old kept until the new verifies). Done when: tests assert removal frees the folder and a failed update leaves the old version working.
- [ ] Add `ModelSystemCheck`: DirectX 12 feature level and dedicated video memory per adapter, system RAM, and free disk, against each entry's recorded minimums. Done when: a test with fake adapters reports which models can run on the GPU and which only on the CPU.
- [ ] Refuse by name: unapproved license, hash mismatch, too little disk space, no network ("Downloading needs a connection; installed models keep working offline"). Done when: `ModelRefusalTests` assert each message.
- [ ] Generate `docs/dev/models.md` (task, model, version, license with link, size, source) from the manifest through `python scripts/gen-models-doc.py`, checked in CI with `--check`. Done when: the script regenerates the committed page byte-identically.
- [ ] Log one Serilog Information line per download, verification, and removal. Done when: a Serilog test logger asserts each.
- [ ] Commit: `"core: the model catalog with license records, verified downloads, and removal"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ModelManifestTests|FullyQualifiedName~ModelLicensePolicyTests|FullyQualifiedName~ModelDownloaderTests|FullyQualifiedName~ModelRefusalTests"` exits 0, proving every manifest license is on the allow-list, a CC-BY-NC entry fails the build test, downloads need an action id, and a hash mismatch leaves nothing installed; `python scripts/gen-models-doc.py --check` exits 0. Cheaper substitute that fails: a hard-coded model URL with no license record, which the policy test catches.

## 3. The Model Manager Surface in Isotone.UI

A user who wants offline AI needs to see which models exist, what each is for, how big it is, and what license it carries, and to install, remove, and choose where it runs, in one place shared by all three apps. This section designs and builds the Model Manager page in `Isotone.UI`, embedded in each app's AI settings page (`D01 T05 §4`). Catalog: none of its own (`D03 T19 §16` hosts it for IP-2104 and IP-2112). -> SOURCE: parity-local-ml-manager

**Fidelity:** Isotone.UI Model Manager -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/isotone-ui/ModelManager/.
**Design:** new surface: docs/design/components/ModelManager/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md, docs/design/components/Progress/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Toast/README.md, docs/design/components/Dialog/README.md -- states: all in spec -- themes: all four -- density: both
**Job:** a user can install, remove, and choose on-device models and decide per task whether AI runs locally or through OpenRouter. Consumer: `ModelDownloader` and the `Isotone.AI.Backend.<Task>` and `Isotone.AI.Local.Device` settings read by §1.
**Treatment:** a page with a model list grouped by task (name, version, size, license linked, state: not installed, downloading with progress and Cancel, installed, update available, failed with the reason), Download, Remove, and Update per row, a total disk-use readout, an inference device picker (each DirectML adapter by name, or CPU) with the system requirements readout, and a per-task backend picker that offers Local only when an installed model serves the task. Cheaper substitute that fails the checkpoint: a single "Use local AI" checkbox with no license or state shown, which the license-column and per-task tests catch.
**Chrome:** consume the generated theme dictionaries of `D01 T01 §3`, the AI settings page and progress panel of `D01 T05 §4`, the suite toast, and the settings store. Do not add a model list to any app.

**Requires:** display-session -- the page renders and its captures need an interactive desktop

- [ ] Write the design spec `docs/design/components/ModelManager/README.md` and its `preview.html` card (anatomy: task groups, model rows, license link, state chip, progress, device picker, backend pickers; every state: rest, hover, focus, disabled, downloading, installed, update available, failed, empty; tokens and sizes in both densities) before any XAML is written, and regenerate the design page with `python scripts/build-design-site.py`. Done when: the spec and its card exist and `python scripts/build-design-site.py --check` passes.
- [ ] Add `src/Isotone.UI/AI/ModelManagerViewModel.cs` (CommunityToolkit.Mvvm) over `ModelManifest`, the installed index, `ModelDownloader`, and `ModelSystemCheck`, taking an app scope so each app lists the tasks it consumes. Done when: `ModelManagerViewModelTests` list the fixture manifest grouped by task for the Gesso and Albumen scopes.
- [ ] Add `src/Isotone.UI/AI/ModelManagerView.xaml` implementing the spec 1:1 with token keys only. Done when: `python scripts/design-lint.py --baseline docs/design/.lint-baseline.json` reports 0 new violations over the file.
- [ ] Show each row's license as its SPDX id with a link opening the license URL and the local `LICENSE.txt` once installed. Done when: a view-model test asserts the license text and link for each fixture entry.
- [ ] Add Download with progress and Cancel through the `D01 T05 §4` progress panel, a confirmation stating size and license before the first download of a model, and completion and failure notifications through the suite toast. Done when: a view-model test over a fake downloader asserts the confirmation text, progress, cancel, and the toast.
- [ ] Add Remove with a confirmation naming the model and the space freed, and Update keeping the old version until the new verifies. Done when: view-model tests assert both flows.
- [ ] Show total disk use and per-model size, refreshed after each change, as the page's reporting of what on-device AI costs. Done when: a test asserts the total after an install and a removal.
- [ ] Add the inference device picker (Auto, each DirectML adapter by name, CPU) writing `Isotone.AI.Local.Device`, with the system requirements readout per adapter. Done when: a test asserts the setting written and the readout for fake adapters.
- [ ] Add the per-task backend pickers writing `Isotone.AI.Backend.<Task>`, offering Local only when an installed model serves the task and stating "Local results are not sent anywhere" beside it. Done when: a test asserts Local is disabled with a reason until a serving model is installed.
- [ ] Embed the page in the AI settings page of `D01 T05 §4` as an "On-device models" section each app shows. Done when: a test resolves the section from the settings page for each app scope.
- [ ] Give every control an `AutomationProperties.Name`, tooltips on icon buttons, and a logical tab order. Done when: a UI automation test walks the tab order and reads each name.
- [ ] Render every spec state, theme, Highlight, and density through the visual harness of `D01 T01 §9` into `build/wpf-renders/ModelManager/`. Done when: the harness produces one render per state, theme, Highlight, and density.
- [ ] Write `docs/user/isotone/on-device-ai.md`: what on-device models are, where they are stored, their licenses, how to remove them, and that OpenRouter stays the default. Done when: the page exists and lists every manifest entry through the generated table.
- [ ] Commit: `"ui: the Model Manager for on-device models"`

**Test checkpoint:** Unit test and driven run with evidence: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ModelManagerViewModelTests"` exits 0; a driven run of the Isotone.UI test host installs a fixture model from a local test server, shows its license and disk use, switches the segmentation backend to Local, and removes the model, with the settings readback and the log lines quoted and the renders under `build/wpf-renders/ModelManager/` compared with `build/design-reference/ModelManager/`. Cheaper substitute that fails: a single local-AI checkbox, which cannot show a license or choose per task.

## 4. Task Adapters: Segmentation, Inpainting, Upscaling, Denoise, and Depth

A model is only useful once its input is prepared and its output interpreted the way its authors did: normalization, channel order, prompt encoding, mask thresholds, tiling for a fixed input size, and a depth map's scale. This section builds one adapter per shared task in `Isotone.Core`, so Gesso's select subject and Remove tool and Albumen's denoise call the same code, each proven on the tiny fixture models for shapes and tiling and, when the real model is installed, against the upstream reference output. Catalog: none of its own. -> SOURCE: parity-local-ml-adapters

**Fidelity:** no surface of its own (the consuming tools are `D03 T19 §16`, `D03 T19 §17`, and `D04 T10 §13`)

- [ ] Add `src/Isotone.Core/AI/Local/Tasks/ILocalTask.cs` (`Task`, `Prepare(input) -> tensors`, `Interpret(outputs) -> result`, `RequiredModel`) with preprocessing driven by the manifest entry (mean, standard deviation, channel order, input size policy: fixed, multiple-of, or free). Done when: a test prepares a known image for a fixture entry and asserts the tensor values.
- [ ] Add `SegmentationTask` for MobileSAM and SAM ViT-B: the image encoder run once per image and cached by content hash, the prompt decoder run per point or box prompt (positive and negative points), and the mask upsampled to image size and thresholded at `Isotone.AI.Local.MaskThreshold` (default 0.0 logit). Done when: `SegmentationTaskTests` on the fixture segmenter return the expected mask for a box prompt and reuse the cached embedding on a second prompt.
- [ ] Add a saliency mode for U-2-Net returning a soft mask for select subject without a prompt. Done when: a fixture test returns the expected soft mask range.
- [ ] Add `InpaintTask` for LaMa: image and mask at the model's multiple-of-8 size, the crop around the mask with context padding, the result composited back only inside the mask. Done when: `InpaintTaskTests` assert pixels outside the mask are byte-identical and the crop math for an edge-touching mask.
- [ ] Add `UpscaleTask` for Real-ESRGAN x2 and x4, tiled through `LocalTiler` with the overlap scaled by the factor. Done when: `UpscaleTaskTests` on the 2x fixture upscaler return exact output dimensions and seamless tiles.
- [ ] Add `DenoiseTask` and `DeblurTask` for NAFNet with a strength that blends the result with the input in linear light. Done when: tests assert strength 0 returns the input exactly and strength 1 the model output.
- [ ] Add `DepthTask` for Depth Anything V2 Small and MiDaS returning a 16-bit relative depth map (near is high) resized to the image, with the model's output normalized per image. Done when: `DepthTaskTests` on the constant fixture return a uniform map at full resolution.
- [ ] Accept linear-light and display-referred inputs: convert to the model's expected sRGB 8-bit or float range and back through `D01 T04 §1`, never feeding linear values to an sRGB-trained model. Done when: a test asserts the conversion for a linear float input.
- [ ] Add real-model tests with `[Trait("Requires", "model")]` for each adapter: when the model is installed on the test machine, compare against the committed upstream reference output of the same input (produced by the upstream repository's own inference script, command and version recorded) within the stated tolerance, skipped with a reason otherwise. Done when: each test exists, and on a machine with the models installed each passes with its tolerance printed.
- [ ] Commit the reference inputs and outputs under `tests/fixtures/core/ml/reference/` with `reference.txt` naming each upstream script, commit, and command. Done when: every adapter has one reference pair.
- [ ] Record per adapter in `docs/dev/models.md` the preprocessing, the tolerance, and the known limits (for example "SAM masks are binary; refine with Select and Mask"). Done when: the page has one paragraph per adapter.
- [ ] Commit: `"core: local task adapters for segmentation, inpainting, upscaling, denoise, deblur, and depth"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~Isotone.Core.Tests.AI.Local.Tasks"` exits 0 on the fixture models (shapes, crops, outside-mask bytes identical, seamless tiling, strength endpoints); with the real models installed, the `Requires=model` tests pass within their printed tolerances against the upstream reference outputs, and report skipped with a reason otherwise. Cheaper substitute that fails: feeding the whole image unpadded to every model, which the edge-crop and tile-seam tests catch.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx --filter "FullyQualifiedName~Isotone.Core.Tests.AI.Local|FullyQualifiedName~Isotone.UI.Tests.AI"` exits 0 with the network blocked and no model downloaded
- [ ] `ModelLicensePolicyTests` pass and `docs/dev/models.md` equals its generated form
- [ ] No installer payload contains a model file: `scripts/package.ps1`'s file list has no `.onnx` file
- [ ] `python scripts/todo-graph.py validate` clean
