---
schema_version: 1
id: stilus-ai
domain: 02-stilus
status: draft
title: "TODO-15 -- Stilus AI: Editable, Suite-Aware, Reproducible"
depends_on: []
frozen: true
track: N15
---

# TODO-15 -- Stilus AI: Editable, Suite-Aware, Reproducible

> **Goal:** Stilus's AI is its own design, not a clone of Firefly or Corel AI, built on three pillars. Every result is editable, structured output: the model returns JSON validated against a schema, applied as one named undoable command that creates real vector objects (named layers, document swatches, styles, and constraints), and raster results are placed images, never flattened into artwork. It is suite-aware: the shared brand kit from `D01 T05 §5` constrains color and type, and the Albumen photo to Pinxit cleanup to Stilus trace pipeline works over files, offering a hand-off only when the other app is installed and refusing by name otherwise, with no runtime dependency. It is explainable and reproducible: every action writes a provenance record with prompt, model, parameters, and seed into the document's SVG metadata, and the provenance panel can re-run, compare, and revert. All of it runs through the user's own OpenRouter key, with nothing sent without an explicit action and a send preview.

> [!IMPORTANT]
> **Current state (verified 2026-09-26):** Stilus has no AI code and no HTTP client anywhere under `src/Stilus/`. The SVG reader (`src/Stilus/Bezier.Core/Services/SvgParser.cs`) drops root `<metadata>`, so embedded provenance needs the reader change owned by `D02 T07 §1` before §1 can prove a round trip. The history (`src/Stilus/Bezier.Core/Services/HistoryManager.cs`) keeps 100 steps by default, and one AI apply must occupy exactly one of them; `D01 T02 §4` replaces it with the suite `UndoHistory` before this file runs. Commands exist for add, delete, group, and property change (`src/Stilus/Bezier.Core/Commands/AddElementCommand.cs` and its siblings), the building blocks an AI apply composes. The Pinxit source tree exists (`src/Pinxit/src/Pinxit.UI/App.xaml.cs`), so the Pinxit hand-off in §11 has a real target to detect; Albumen has no source tree yet, so its hand-off is file-based and refused by name when absent. The shared AI core this file consumes (`D01 T05`) does not exist yet: there is no `src/Isotone.Core/`.
<!-- claim: count "HttpClient" src/Stilus/**/*.cs = 0 -->
<!-- claim: count "OpenRouter" src/Stilus/**/*.cs = 0 -->
<!-- claim: count "\"metadata\"" src/Stilus/Bezier.Core/Services/SvgParser.cs = 1 -->
<!-- claim: count "_maxHistorySize = 100" src/Stilus/Bezier.Core/Services/HistoryManager.cs = 1 -->
<!-- claim: exists src/Stilus/Bezier.Core/Commands/AddElementCommand.cs -->
<!-- claim: exists src/Pinxit/src/Pinxit.UI/App.xaml.cs -->
<!-- claim: absent src/Albumen -->
<!-- claim: absent src/Isotone.Core -->

## Inputs

- [`standards/stilus.md`](../../standards/stilus.md) -- every mutation is an `IEditorCommand` (the suite `IUndoableCommand` after `D01 T02 §4`); SVG is the native format
- [`standards/shared.md`](../../standards/shared.md) -- one Information log line per document change; no app depends on another at runtime
- [`docs/parity/section-design.md`](../../docs/parity/section-design.md) -- "AI: Stilus's own, built on three pillars", the operator decisions this file implements
- [`docs/parity/stilus-parity.md`](../../docs/parity/stilus-parity.md) -- the catalog rows NP-2480 to NP-2536 each section names
- -> XREF: D01 T05 §1 -- the OpenRouter client every generation calls through
- -> XREF: D01 T05 §2 -- the key store and the per-task model settings
- -> XREF: D01 T05 §3 -- the provenance record, store, re-run, and compare this file embeds in the document
- -> XREF: D01 T05 §4 -- the send gate, send preview, AI settings page, progress panel, and usage indicator
- -> XREF: D01 T05 §5 -- the brand kit library and `BrandKitConstraint`
- -> XREF: D02 T07 §1 -- the live-object contract and the root metadata reader provenance rides
- -> XREF: D02 T07 §5 -- layers the generated art lands in
- -> XREF: D02 T07 §14 -- the New Document dialog that New from Prompt extends
- -> XREF: D02 T09 §3 -- swatches and color groups generated colors join
- -> XREF: D02 T09 §6 -- the Recolor Artwork mapping generative recolor drives
- -> XREF: D02 T09 §10 -- pattern swatches and Pattern Options for text to pattern
- -> XREF: D02 T10 §13 -- writing tools and the Windows spell checker the rewrite and grammar features sit beside
- -> XREF: D02 T11 §10 -- 3D and Materials, which turntable help text points to
- -> XREF: D02 T12 §1 -- placed bitmap objects image results become
- -> XREF: D02 T12 §5 -- the local potrace tracer concept to vector drives
- -> XREF: D02 T13 §4 -- bleed settings generate print bleed reads
- -> XREF: D02 T16 §7 -- the welcome screen the AI entries appear on
- -> XREF: D01 T03 §2 -- the local resampler that is the upscale fallback
- -> XREF: D01 T02 §3 -- single instance and file-open forwarding the hand-off inbox receives through
- -> XREF: D02 T06 §12 -- the command index the assistant's tool catalog reads
- -> XREF: D02 T06 §13 -- the Preferences dialog that hosts the AI page
- -> XREF: D03 T05 §1 -- Pinxit's filter pipeline, the cleanup target of the hand-off
- -> XREF: D04 T02 §7 -- Albumen's Edit in Pinxit, which uses the same App Paths lookup §11 moves to `Isotone.Core`
- -> XREF: D03 T19 §11 -- Pinxit AI cites §1: the Stilus precedent for the AI menu and provenance panel whose shared parts stay in `Isotone.UI`; §7: the `FontMatcher` D03 T19 §11 moves to `Isotone.Core/Text/` as its second consumer; §11: `SuiteAppLocator`, the hand-off folder, and sidecar provenance D03 T19 §13 consumes
- -> XREF: D04 T12 §13 -- Albumen parity output cites §11: `SuiteAppLocator`, used by D04 T12 §13's Open in Pinxit post-processing action
- -> XREF: D04 T14 §9 -- Albumen parity workspace cites §11: `SuiteAppLocator`, which D04 T14 §9 consumes for Pinxit

## Outcome

- Every AI action is reachable from one AI menu and toolbar split button, and every unfinished item names its owner section.
- Every AI apply is one named undo step, writes one provenance record into the SVG root metadata, and writes one log line; the provenance panel re-runs with the same seed, compares, reverts, and deletes records, and the records survive save and reopen.
- Text to vector, text to pattern, shape fill, generative expand, and concept to vector produce real, named, editable vector objects validated against committed JSON schemas; raster results (text to image, cleanup, image expand) are new placed images with the original kept.
- Recolor sends only colors, rewrite keeps formatting runs, retype ranks installed fonts locally, and the assistant can run only whitelisted Stilus commands.
- The brand kit constrains colors wherever generation offers it, and hand-offs to Pinxit and from Albumen run over files, only when the other app is installed, with provenance carried across.
- No test needs a live OpenRouter key: every section proves itself against the `D01 T05 §1` recorded transport.

**Adjacency:** list=applicable @ D02 T15 §1; document=applicable @ D02 T15 §4; settings=applicable @ D01 T05 §2; reporting=applicable @ D02 T15 §1; notifications=applicable @ D01 T05 §4; permissions=applicable @ D02 T15 §11; audit=applicable @ D02 T15 §1; exchange=applicable @ D02 T15 §11; reverse=applicable @ D02 T15 §1

**Adjacency rationale:** Generation history and variations are browsable and filterable in the provenance panel (§1, §2). Generated print bleed feeds the printed page (§4), and provenance travels in the saved SVG. Model choices and AI options live in the shared settings contract (`D01 T05 §2`) plus the Stilus keys each section names. The usage meter and the per-document AI cost summary sit in the provenance panel (§1). Progress, cancel, and completion reach the user through the shared progress panel and toast (`D01 T05 §4`). No key, offline, a declined preview, and another app not installed are refusals by name (§1, §11). Each apply is one named history step plus one provenance record and one log line (§1). Hand-off files to and from Pinxit and Albumen are the exchange (§11), with brand kits exchanged as ASE in `D01 T05 §5`. Every AI apply is undoable and revertable from the provenance panel (§1).

## Implementation Order

| Order | Section | Deliverable                                                                       | Depends On                   | Status |
| :---: | :-----: | --------------------------------------------------------------------------------- | ---------------------------- | :----: |
|   1   |   §1    | AI in Stilus: the AI menu, settings, usage, and the provenance panel               | D01 T05 §4                   |  [ ]   |
|   2   |   §2    | Generate vector artwork from a prompt                                             | §1, D02 T09 §3, D02 T07 §5   |  [ ]   |
|   3   |   §3    | Generate patterns and fill shapes                                                 | §2, D02 T09 §10              |  [ ]   |
|   4   |   §4    | Generative expand and print bleed                                                 | §2, D02 T13 §4               |  [ ]   |
|   5   |   §5    | AI recolor and palettes from the brand kit                                        | §1, D02 T09 §6, D01 T05 §5   |  [ ]   |
|   6   |   §6    | The AI assistant: prompt to edit with undoable commands                           | §1                           |  [ ]   |
|   7   |   §7    | AI text: rewrite, translate, proofread, fit, and retype                           | §1, D02 T10 §13              |  [ ]   |
|   8   |   §8    | AI images: generate, remix, and reference images                                  | §1, D02 T12 §1               |  [ ]   |
|   9   |   §9    | AI image cleanup: remove background, upscale, repair, and art style               | §8                           |  [ ]   |
|  10   |   §10   | Concept to vector: sketches and images to structured vectors                      | §2, D02 T12 §5               |  [ ]   |
|  11   |   §11   | The suite pipeline: Albumen to Pinxit to Stilus hand-offs and shared brand kits       | §10, D01 T05 §5              |  [ ]   |

---

## 1. AI in Stilus: the AI Menu, Settings, Usage, and the Provenance Panel

This section gives Stilus's AI one front door and makes the reproducibility pillar real in the document: an AI menu and toolbar split button listing every AI action (each wired or disabled with its owner section), the shared AI settings page hosted in Preferences with per-task model choice, the usage meter, the content-aware defaults preference, a first-use tutorial, and the Provenance panel that lists, filters, re-runs with the same seed, compares, reverts, and deletes AI actions recorded in the document. Provenance is written into the SVG root `<metadata>` through the reader change `D02 T07 §1` owns, so saving a document now writes more than it did; that is why this file is frozen and this section carries a freeze check. Catalog: NP-2480 (content-aware defaults), NP-2481 (AI menu and generative toolbar button), NP-2482 (usage and credit meter), NP-2483 (generation history and provenance panel), NP-2484 (per-task model selection), NP-2485 (quick tutorial on first use). Admission: the acceptance-bar aim "AI results are editable, undoable, and reproducible".

**Freeze check:** Provenance metadata is written only through the existing atomic save path (`D02 T04 §1`, the shared writer after `D01 T02 §5`); saving a document with no AI records writes bytes identical to the save before this section (no empty `<metadata>` or namespace declaration is added), proven by hashing `tests/fixtures/stilus/svg/bezier-sample.svg` saved before and after; killing the process mid-save of a document with records leaves the original byte-identical. Fixture source: `tests/fixtures/stilus/ai/provenance-two-records.svg` (created by this section).

**Fidelity:** AI in Stilus: the AI Menu, Settings, Usage, and the Provenance Panel -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/ai-menu/, docs/captures/golden/stilus/provenance-panel/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/ToggleSwitch/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/ai-menu/ and docs/captures/stilus/provenance-panel/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can reach every AI action from one menu and see, repeat, compare, or undo any AI result in the document. Consumer: the document's provenance store and history.
**Treatment:** a top-level AI menu (mirrored under Object, Generative) and a toolbar split button remembering the last action; a dockable Provenance panel with one row per record (thumbnail, action, prompt excerpt, model, seed, cost, date) and Re-run, Re-run with New Seed, Compare, Select Results, Revert, and Delete Record. Cheaper substitute that fails the checkpoint: a history list without seeds or models, which cannot reproduce anything.
**Chrome:** consume the shared `SendPreviewDialog`, `AiSettingsPage`, `AiProgressPanel`, and `AiUsageIndicator` from `D01 T05 §4`, the dock layout, and the suite history. Do not build a Stilus-only key or progress UI.

**Requires:** display-session -- menu, panel, and tutorial captures need an interactive desktop

- [ ] Register the shared AI services in the Stilus composition root with `services.AddIsotoneAi()` from `D01 T05 §1`, passing app name `Stilus`. Done when: a composition test resolves `AiSendGate`, `IAiKeyStore`, and `ProvenanceStore` factory from the Stilus container.
- [ ] Add `src/Stilus/Isotone.Stilus.Desktop/Views/Menus/AiMenu.xaml` with every AI action of this file (§2 to §11) as an item, each wired or disabled with `Planned: D02 T15 §N` through `Isotone.Stilus.Desktop/Input/PlannedCommands.cs`, and mirror it under Object, Generative. Done when: `MenuAuditTests` passes with the new items and every planned ref resolves with `python scripts/todo-graph.py resolve`.
- [ ] Add the toolbar split button `AiActionSplitButton` that runs the last-used action and opens the menu from its arrow, remembering the last action in `stilus.ai.lastAction`. Done when: a view-model test asserts the last action is persisted and restored.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/AI/StilusProvenanceBinding.cs` writing the document's `D01 T05 §3` records as `<isotone:provenance>` children of the root `<metadata>` and tagging result elements with a `stilus:provenance-id` attribute, preserved by the reader per `D02 T07 §1`. Done when: `StilusProvenanceBindingTests.RoundTrip` opens `tests/fixtures/stilus/ai/provenance-two-records.svg`, saves, reopens, and asserts both records and every object link are equal.
- [ ] A document with no records writes no metadata element and no `isotone:` namespace declaration. Done when: `StilusProvenanceBindingTests.NoRecords_ByteIdenticalSave` hashes a fixture saved before and after this change and the hashes match.
- [ ] Export respects `ExportService`'s metadata option: plain SVG export strips provenance unless `Stilus.Export.Svg.KeepAiProvenance` (default off) is set. Done when: a test exports the fixture both ways and asserts presence and absence of `isotone:provenance`.
- [ ] Add `src/Stilus/Isotone.Stilus.Desktop/Views/Panels/ProvenancePanel.xaml` with `ProvenancePanelViewModel`: one row per record with thumbnail, action, prompt excerpt, model, seed, cost, and date; filter by action, model, and date range; search the prompt text. Done when: `ProvenancePanelViewModelTests.Filter` asserts row counts for each filter over the fixture.
- [ ] The panel reports a per-document AI cost summary (total cost, request count, models used) above the list. Done when: a view-model test asserts the summary equals the sum over the fixture's records.
- [ ] Re-run replays `ToRerun(sameSeed: true)` through the send gate into a new result beside the old one with `ParentId` set; Re-run with New Seed uses `sameSeed: false`. Done when: `ProvenancePanelViewModelTests.Rerun_RequestEqualsRecord` asserts the gated request equals the recorded request field by field (recorded transport, no network).
- [ ] Compare opens a side-by-side view of two records' results with the `ProvenanceDiff` list beneath. Done when: a view-model test selects two records and asserts the diff rows.
- [ ] Select Results selects every element tagged with the record's id. Done when: a test asserts the selection count equals `ResultObjectIds.Count`.
- [ ] Revert removes the result elements and the record in one undoable `RevertAiResultCommand` in `Isotone.Stilus.Core/AI/Commands/`, restoring any original the action hid. Done when: `RevertAiResultCommandTests` assert the document after Revert equals the pre-generation document element by element, and Undo restores the result.
- [ ] Delete Record removes only the record (the art stays, its `stilus:provenance-id` is cleared) as one undoable command. Done when: a test asserts the element survives and carries no provenance id.
- [ ] Host the shared `AiSettingsPage` as the AI category of the `D02 T06 §13` Preferences dialog, where per-task model choice (text, vision, image, vector JSON) is made. Done when: a driven run opens Preferences, AI, changes the vector-JSON model, and the settings file shows the new value (readback quoted).
- [ ] Add `stilus.ai.contentAwareDefaults` (default on): prefill prompt fields from selection names and document swatch names, never sending anything by itself. Done when: a test asserts the prefill with the setting on, an empty field with it off, and zero gate calls in both cases.
- [ ] Place `AiUsageIndicator` in the status strip, refreshed after each request and hidden with no key. Done when: a driven run against the recorded transport shows the fixture balance (capture committed).
- [ ] Add `AiQuickTutorial` overlay (three steps: add key, try text to vector on a blank document, open Provenance) shown once, reopenable from Help, tracked by `stilus.ai.tutorialSeen`. Done when: a view-model test asserts it shows once and reopens from Help.
- [ ] With no key, every AI menu item opens the AI settings page with the `D01 T05 §4` first-use sentence. Done when: a test invokes each item with no key and asserts navigation and zero gate calls.
- [ ] Log one Information line per AI apply: `AI {Action} applied: record {RecordId}, {ModelId}, seed {Seed}, {ObjectCount} objects`. Done when: `StilusProvenanceBindingTests` assert the line through a captured sink.
- [ ] Update the Stilus user guide with `docs/user/stilus/ai.md` (the menu, the provenance panel, re-run, compare, revert, what is saved in the file) linking to `docs/user/isotone/ai.md`. Done when: the page documents every control of the panel.
- [ ] Commit: `"stilus: the AI menu, AI preferences, usage meter, and the provenance panel"`

**Test checkpoint:** Format fidelity proof plus unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~StilusProvenanceBindingTests|FullyQualifiedName~ProvenancePanelViewModelTests|FullyQualifiedName~RevertAiResultCommandTests"` exits 0: the provenance fixture opens, saves, and reopens with both records and their object links intact, a record-free save is byte-identical to the pre-change save, Revert restores the pre-generation document element by element, and the re-run request equals the recorded one over the recorded transport (no live key); captures of the menu and panel are committed. Cheaper substitute that fails: provenance kept only in the app session, lost on reopen, which the round trip catches.

## 2. Generate Vector Artwork from a Prompt

Text to vector is the headline of the editable-output pillar: the model returns a schema-validated JSON scene, and Stilus applies it as real paths, named layers, document swatches, styles, and live text in one undoable command. A generated PNG or a single flattened path is exactly what this section must not produce. Catalog: NP-2486 (text to vector), NP-2487 (content types), NP-2488 (detail level), NP-2489 (style reference), NP-2490 (style, effect, and color-tone presets), NP-2491 (model picker), NP-2492 (auto model and up to 4 variations), NP-2493 (editable live text), NP-2494 (generate similar), NP-2495 (browse, rate, and reuse variations), NP-2496 (turntable), NP-2497 (new document from a prompt), NP-2498 (welcome screen AI entries).

**Fidelity:** Generate Vector Artwork from a Prompt -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/text-to-vector/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/TextBox/README.md, docs/design/components/Slider/README.md, docs/design/components/ListTree/README.md, docs/design/components/Progress/README.md, docs/design/components/Button/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/text-to-vector/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can describe an image and get editable, organized vector art in their document. Consumer: the document (layers, swatches, elements) and its provenance store.
**Treatment:** a Text to Vector panel (prompt, type Subject, Scene, Icon, or Pattern, detail slider 1 to 5, style reference, style presets, brand kit toggle, model, variations 1 to 4) whose results arrive as a variation strip; choosing one inserts it on a named layer with its swatches in the document palette. Cheaper substitute that fails the checkpoint: placing a generated PNG, or one flattened ungrouped path.
**Chrome:** consume the `D01 T05 §4` send gate and progress panel, the `D01 T05 §3` provenance store, the `D02 T09 §3` swatch model, the `D02 T07 §5` layers, and the suite history. Do not add a second SVG importer for generated art.

**Requires:** display-session -- panel and result captures need an interactive desktop

- [ ] Add the schema `src/Stilus/Isotone.Stilus.Core/AI/Schemas/vector-scene.v1.json`: `layers[]` (name, children), shapes (path data in a 0 to 1000 viewBox, rect, ellipse, polygon, and text with a font role and content), `swatches[]` (name, sRGB hex, role), `styles[]` (fill and stroke by swatch name, stroke width, opacity), and `constraints[]` (align or symmetry hints), with `additionalProperties: false` everywhere. Done when: the schema validates the committed `tests/fixtures/stilus/ai/vector-scene-*.json` fixtures through the `D01 T05 §1` validator.
- [ ] Add `VectorSceneValidator` in `Isotone.Stilus.Core/AI/` checking path syntax, bounds, swatch references, and an element budget (`stilus.ai.maxElements`, default 2,000). Done when: `VectorSceneValidatorTests` reject a bad path, an unknown swatch, and an over-budget scene with named messages.
- [ ] Add `VectorSceneApplier` building `VectorElement`s and applying layer creation, swatch adds, and element adds inside one `UndoHistory` transaction named "Generate Vector: <prompt excerpt>". Done when: `VectorSceneApplierTests.OneUndoStep` applies a fixture and a single Undo returns the document to its prior state element by element.
- [ ] Generated swatches join the document palette through the `D02 T09 §3` swatch model, grouped in a color group named after the prompt excerpt. Done when: the applier test asserts the group and its swatch names.
- [ ] Live text: text nodes become `SvgText` with the brand kit's type role font or a system font, never outlines. Done when: `VectorSceneApplierTests.Text_IsLive` asserts the element type and its string.
- [ ] Content type and detail map to system-prompt templates in `Isotone.Stilus.Core/AI/Prompts/`, whose SHA-256 goes into provenance; Icon forces a square fit to the artboard and at most 3 colors. Done when: a test asserts the template hash in the record and the 3-color limit on an Icon fixture.
- [ ] Style reference: an image (sent as vision input) or the selected art (sent as its SVG plus a rendered PNG), both listed in the send preview. Done when: a test asserts the `AiSendPlan` parts for each reference kind.
- [ ] Style, effect, and color-tone presets (flat, line art, isometric, duotone, woodcut, and more) as local JSON in `Isotone.Stilus.Core/AI/Presets/`, applied as prompt fragments. Done when: a test loads every preset and asserts each has a name and a fragment.
- [ ] Brand kit toggle injects `BrandKitConstraint` so swatches can only be kit colors. Done when: a test with the toggle on rejects a recorded reply containing a non-kit color.
- [ ] Model picker filtered to models that support structured output; Auto uses `ai.model.vectorJson`. Done when: a view-model test over the catalog fixture lists only structured-output models.
- [ ] Variations 1 to 4 issue parallel gated requests (one preview listing all) with distinct recorded seeds, each result kept in a `VariationSet` on the parent record. Done when: a test with 3 variations asserts 3 requests, 3 distinct seeds, and one preview.
- [ ] Variation strip: rate 1 to 5, swap the placed variation in place (one undoable command), or place another beside it. Done when: `VariationSetTests` assert the rating persists in the record and the swap undoes in one step.
- [ ] Generate Similar reuses a record's prompt and parameters with a new seed and `ParentId`. Done when: a test asserts the new request differs from the parent only in seed.
- [ ] Turntable: asks for N views (3 to 8) of the selected art as separate scenes on one row, each on a layer named by angle; help text says when to use 3D and Materials (`D02 T11 §10`) instead. Done when: a fixture reply with 4 views applies as 4 named layers in one undo step.
- [ ] New from Prompt: `File, New from Prompt` creates a document sized by a chosen `D02 T07 §14` preset, then runs text to vector into it. Done when: a test asserts document size and one generated layer from a recorded reply.
- [ ] Welcome screen entries (`New from Prompt`, `Text to Vector`) registered with the `D02 T16 §7` welcome screen. Done when: a driven run shows the entries and one opens the panel (capture committed).
- [ ] Commit fixtures `tests/fixtures/stilus/ai/vector-scene-*.json` (subject, scene, icon, text, invalid) with golden SVGs under `tests/fixtures/stilus/ai/goldens/`. Done when: every fixture has a golden or a named expected error.
- [ ] Commit: `"stilus: text to vector with schema-validated scenes, variations, and one-step undo"`

**Test checkpoint:** Unit test plus format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~VectorSceneValidatorTests|FullyQualifiedName~VectorSceneApplierTests|FullyQualifiedName~VariationSetTests"` exits 0: the applier applies each committed JSON fixture and the saved SVG compares element by element with its golden, and one Undo returns the document to its prior state; all requests run against the `D01 T05 §1` recorded transport with no live key; the panel capture is committed. Cheaper substitute that fails: inserting a raster image, which the element comparison rejects.

## 3. Generate Patterns and Fill Shapes

Patterns and shape fills extend text to vector to two jobs where a bitmap would be the tempting shortcut: a seamless pattern must be a real vector pattern swatch the designer can edit, and a shape fill must be art clipped to the chosen shape. Catalog: NP-2499 (text to pattern swatch), NP-2500 (manage and edit generated patterns), NP-2501 (generative shape fill with detail and style reference), NP-2502 (repeat a shape fill across repeated shapes).

**Fidelity:** Generate Patterns and Fill Shapes -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/ai-pattern/, docs/captures/golden/stilus/shape-fill/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/TextBox/README.md, docs/design/components/Progress/README.md, docs/design/components/ListTree/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/ai-pattern/ and docs/captures/stilus/shape-fill/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can make an editable seamless pattern or fill a shape with art that fits it. Consumer: the Swatches panel (pattern swatches) and the document (clipping groups).
**Treatment:** Pattern mode in the Text to Vector panel producing a pattern swatch that opens in Pattern Options, and a Shape Fill command on the contextual bar that clips generated art to the selection. Cheaper substitute that fails the checkpoint: a bitmap pattern fill, or art placed over the shape without a clip.
**Chrome:** consume the §2 schema and applier, the `D02 T09 §10` pattern swatch model and Pattern Options editor, and clipping groups. Do not add a second pattern model.

**Requires:** display-session -- pattern and fill captures need an interactive desktop

- [ ] Add the schema extension `Isotone.Stilus.Core/AI/Schemas/vector-pattern.v1.json`: tile size, tile type (grid, brick, hex), and the §2 shape list. Done when: the pattern fixtures validate and an extra property is rejected.
- [ ] Add `PatternTileValidator` clipping every shape to the tile and its neighbors and checking edge continuity so the result is seamless. Done when: `PatternTileValidatorTests` reject `pattern-broken-seam.json` and accept `pattern-seamless.json`.
- [ ] The pattern applier creates a pattern swatch in the Swatches panel through `D02 T09 §10` and opens it in Pattern Options; variations become sibling swatches in a color group named after the prompt. Done when: a test asserts the swatch count and group name for a 3-variation reply.
- [ ] Manage: regenerate one variation, rename, edit tiles by hand (the swatch is ordinary vector content), and delete (undoable). Done when: a test deletes a generated swatch and Undo restores it.
- [ ] Shape Fill sends the selected shape outline (SVG path plus bounding box) as a structured constraint and lists it in the send preview. Done when: a test asserts the `AiSendPlan` holds the path and no other document content.
- [ ] Results land in a clipping group with the original shape as the clip path, named "Shape Fill: <prompt>", in one undo step. Done when: `ShapeFillApplierTests.ClipGroup` asserts the group structure and one Undo removes it.
- [ ] Options: detail, style reference (image or art), model, and brand kit toggle, shared with §2 through one `GenerationOptions` view model. Done when: a test asserts the options object serialized into provenance equals the panel state.
- [ ] Apply Shape Fill to Similar reuses the record across every selected or same-geometry shape (same seed or a new seed per shape), each result linked to the parent record. Done when: a test with 3 same-geometry shapes asserts 3 clip groups and 3 child records with `ParentId`.
- [ ] Log `Pattern generated {SwatchName}` and `Shape fill applied to {Count} shapes`. Done when: both lines are asserted through a captured sink.
- [ ] Commit fixtures `tests/fixtures/stilus/ai/pattern-*.json` and `shape-fill-*.json` with golden SVGs. Done when: each has a golden.
- [ ] Commit: `"stilus: generated vector patterns and clipped shape fills"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~PatternTileValidatorTests|FullyQualifiedName~ShapeFillApplierTests"` exits 0: the validator rejects the broken-seam fixture and accepts the seamless one, and the saved shape-fill SVG compares element by element with its golden, clip path included; requests run against the recorded transport. Cheaper substitute that fails: unclipped art overlapping the shape, which the clip-group assertion catches.

## 4. Generative Expand and Print Bleed

Extending artwork to a new size or into the bleed is a common production chore; this section does it with editable vectors for vector art and with a new placed image for bitmaps, never altering the original. Catalog: NP-2503 (generative expand for vector artwork), NP-2504 (generate print bleed), NP-2505 (generative expand for placed images).

**Fidelity:** Generative Expand and Print Bleed -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/generative-expand/.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/Progress/README.md, docs/design/components/Canvas/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/generative-expand/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can extend artwork to a new size or into the bleed without redrawing it. Consumer: the document and the printed page.
**Treatment:** an Expand dialog with a live frame on the canvas (target bounds, anchor, match-style strength, keep original locked), and a Generate Bleed command that reads the document's bleed. Cheaper substitute that fails the checkpoint: scaling the art to the new bounds.
**Chrome:** consume the §2 applier, the `D01 T05 §4` send gate, the `D02 T13 §4` bleed settings, and the `D02 T12 §1` placed images. Do not add a second bleed setting.

**Requires:** display-session -- expand frame and result captures need an interactive desktop

- [ ] Add `GenerativeExpandService` in `Isotone.Stilus.Core/AI/` sending the selection SVG, its bounds, and the target bounds, with a schema (`vector-expand.v1.json`) that returns only new shapes. Done when: the request fixture's body carries the three inputs and nothing else.
- [ ] Add `ExpandValidator` rejecting shapes that overlap the original bounds beyond a tolerance (`stilus.ai.expand.overlapTolerance`, default 1 document unit), so existing art is never altered. Done when: `ExpandValidatorTests` reject an overlapping fixture and accept a clean one.
- [ ] Results go on a new layer "Expanded" above or below the source by option, in one undoable command. Done when: a test asserts layer name, position, and one-step undo.
- [ ] Add the Expand dialog and canvas frame adorner (target bounds by handles or numbers, anchor, match strength, keep original locked). Done when: a view-model test asserts the target bounds sent equal the dialog values; capture committed.
- [ ] Generate Bleed computes the bleed band from the artboard and the document bleed (`D02 T13 §4`), expands only background-layer art into it, and flags the new objects' layer "Generated bleed". Done when: `GenerateBleedTests` assert every generated object lies inside the band for a 3 mm bleed and the original art is unchanged element by element.
- [ ] Image expand sends the placed image on a transparent canvas at the target aspect ratio to an image-edit model, places the returned PNG as a new image object, and keeps the original hidden beneath, linked by provenance. Done when: `ImageExpandApplierTests` assert the original's bytes are unchanged and a new image object exists above it.
- [ ] Images over 16 megapixels are downscaled for sending (size shown in the preview) and the result upscaled back locally through `D01 T03 §2`. Done when: a test with a 20-megapixel fixture asserts the sent size and the placed size.
- [ ] Persist `stilus.ai.expand.anchor`, `stilus.ai.expand.matchStrength`, and `stilus.ai.expand.keepOriginalLocked` with defaults and the dialog as consumer. Done when: the values survive a restart (settings readback).
- [ ] Log `Generative expand {Mode} to {Width}x{Height}: {Count} objects`. Done when: the line is asserted.
- [ ] Commit: `"stilus: generative expand for vectors and images, and generated print bleed"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ExpandValidatorTests|FullyQualifiedName~GenerateBleedTests|FullyQualifiedName~ImageExpandApplierTests"` exits 0: generated bleed objects lie only inside the bleed band and the original art is unchanged element by element, and image expand keeps the original bytes; all over the recorded transport. Cheaper substitute that fails: stretching the background to the bleed, which changes the original's geometry and fails the element comparison.

## 5. AI Recolor and Palettes from the Brand Kit

Recolor shows the suite-aware pillar at its smallest: only the color list leaves the machine, proposals apply through the existing Recolor Artwork mapping as its own undoable command, and brand kit mode restricts the model to kit colors. Catalog: NP-2506 (generative recolor from a prompt), NP-2507 (palette-constrained generation from presets and brand kits).

**Fidelity:** extends the Recolor Artwork dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/recolor-artwork/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Swatches/README.md, docs/design/components/TextBox/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the Recolor Artwork dialog -- docs/captures/stilus/recolor-artwork/ (from `D02 T09 §6`). The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can ask for a color mood and get palette options applied to their art, optionally only from the brand kit. Consumer: the selection's colors through `RecolorArtworkEngine`, and the Swatches panel.
**Treatment:** a Generative tab in Recolor Artwork with a prompt, sample prompts, a "Use brand kit" toggle, and 4 palette proposals previewed live on the selection. Cheaper substitute that fails the checkpoint: a random hue shift.
**Chrome:** consume the `D02 T09 §6` Recolor Artwork mapping engine, the `D01 T05 §5` brand kit library, and the Swatches panel. Do not add a second recolor engine.

**Requires:** display-session -- recolor preview captures need an interactive desktop

- [ ] Add `RecolorRequestBuilder` in `Isotone.Stilus.Core/AI/` sending the selection's unique colors with their roles and area share, never geometry; the send preview lists the colors. Done when: `RecolorRequestBuilderTests` assert the payload contains no path data and no element names.
- [ ] Add the schema `palette-proposal.v1.json`: proposals of `{ name, colors[] (hex, mapsFrom hex) }`. Done when: the proposal fixtures validate and one with an unmapped source color is rejected.
- [ ] Feed a chosen proposal's mapping into `RecolorArtworkEngine` so the apply is its existing undoable command, with a provenance record attached. Done when: `PaletteProposalApplierTests.OneUndoStep` asserts Undo restores the original colors exactly.
- [ ] Live preview of each proposal on the selection without committing until Apply. Done when: a view-model test asserts the document is unchanged after previewing all 4 and cancelling.
- [ ] Brand kit mode injects the kit's colors as the schema enum; the model must choose from them. Done when: a test rejects a recorded reply with a non-kit color.
- [ ] Save a proposal as a color group in Swatches or as a palette in the active brand kit (`BrandKitLibrary`). Done when: tests assert the group and the kit palette after each save.
- [ ] Palette presets in `Isotone.Stilus.Core/AI/Presets/ai-palette-presets.json` (muted, high contrast, pastel, corporate, and more) that constrain generation in §2, §3, and §8. Done when: a test asserts each preset produces its prompt fragment and, where it lists colors, its enum.
- [ ] Log `Generative recolor applied: {Proposal} to {ColorCount} colors`. Done when: the line is asserted.
- [ ] Commit: `"stilus: generative recolor and brand-kit palettes through Recolor Artwork"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~RecolorRequestBuilderTests|FullyQualifiedName~PaletteProposalApplierTests"` exits 0: the payload holds only colors, the applier round trip restores original colors on Undo, and brand kit mode rejects a non-kit color, all over the recorded transport. Cheaper substitute that fails: sending the whole document SVG, which the payload test rejects.

## 6. The AI Assistant: Prompt to Edit with Undoable Commands

The assistant turns words into production edits without becoming a scripting engine (scripting is excluded by operator decision): the model may only call a whitelist of existing Stilus commands, its plan is shown as a checklist before anything applies, and every applied plan is one named undoable step with provenance. Catalog: NP-2508 (prompt to edit selected artwork), NP-2509 (assistant panel with chats, attachments, and follow-ups), NP-2510 (workflow starters), NP-2511 (skills as slash commands), NP-2512 (assistant generate, recolor, and vectorize).

**Fidelity:** The AI Assistant: Prompt to Edit with Undoable Commands -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/ai-assistant/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/TextBox/README.md, docs/design/components/ListTree/README.md, docs/design/components/Button/README.md, docs/design/components/Progress/README.md, new surface: docs/design/components/AssistantPanel/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/ai-assistant/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can ask for production edits in words and review each resulting command before and after it applies. Consumer: the document through the command registry, and the provenance store.
**Treatment:** a dockable chat panel where the model answers with a plan of tool calls rendered as a checklist (command name, target objects, parameters) that the user applies all at once, step by step, or not at all. Cheaper substitute that fails the checkpoint: an assistant that edits the SVG text directly.
**Chrome:** consume the command registry, the `D02 T06 §12` command index, the `D01 T05 §4` send gate, and provenance. Do not add a scripting engine.

**Requires:** display-session -- panel and plan captures need an interactive desktop

- [ ] Write the design spec `docs/design/components/AssistantPanel/README.md` and its `docs/design/components/AssistantPanel/preview.html` card (anatomy, every state, tokens, sizes) before any XAML is written, and regenerate the design page. Done when: the spec exists and `python scripts/build-design-site.py --check` passes.
- [ ] Add `src/Stilus/Isotone.Stilus.Core/AI/Assistant/AssistantToolCatalog.cs` exposing a whitelist of existing commands (select by name or style, recolor, align, distribute, rename layers, group, set document size, apply export preset, fit text) as OpenRouter tool definitions with JSON schemas. Done when: a test asserts every tool maps to a registered command and nothing else is exposed.
- [ ] The document is summarized for the model as a structure digest (layers, names, types, counts, colors), never full geometry, and the digest is shown in the send preview. Done when: `DocumentDigestTests` assert no path data appears in the digest of the fixture.
- [ ] Add `AssistantPlanValidator` refusing any tool call outside the whitelist, any unknown target id, and any parameter failing its schema, each by name. Done when: `AssistantPlanValidatorTests` refuse a plan calling an unknown command.
- [ ] Add `AssistantPlanApplier` applying a validated plan as one `UndoHistory` transaction named "Assistant: <request>" with a provenance record; step mode applies one call per history step. Done when: `AssistantPlanApplierTests` assert one undo step in all-at-once mode and N steps in step mode.
- [ ] Add `src/Stilus/Isotone.Stilus.Desktop/Views/Panels/AssistantPanel.xaml` with the chat and the plan checklist (Apply All, Apply Step, Discard). Done when: a view-model test asserts Discard leaves the document unchanged; capture committed.
- [ ] Prompt to edit: with generated art selected, requests such as "change the hat to red" become edits scoped to objects tagged by the §2 record. Done when: a recorded reply produces a plan whose targets are only tagged elements.
- [ ] Multiple named chats per document stored in `stilus:assistant` metadata, opt-out with `stilus.ai.assistant.saveChats`. Done when: a round-trip test saves and reopens two chats, and with the setting off nothing is written.
- [ ] Follow-up questions: when the model asks for clarification, the panel shows the question and sends nothing until the user answers. Done when: a recorded clarification reply produces a question row and zero further requests.
- [ ] Attached files are listed in the send preview with their sizes. Done when: a test asserts an attached PNG appears in the `AiSendPlan`.
- [ ] Background tasks: a long plan runs with the shared progress panel while other documents stay editable, and it refuses to apply by name if the target document changed since planning ("The document changed after the plan was made; plan again"). Done when: a test edits the document mid-plan and asserts the refusal.
- [ ] Workflow starters (Recolor, Organize Layers, Export Setup, Document Setup, Fit Text) as prefilled prompts. Done when: a view-model test asserts each starter fills the prompt.
- [ ] Skills: `/prepare-for-print`, `/name-layers`, and `/export-icons` defined as JSON in `%LOCALAPPDATA%\Rizonesoft\Stilus\ai\skills\`, each a fixed list of whitelisted commands with parameters (no code). Done when: `SkillLoaderTests` load the three and refuse a skill naming a non-whitelisted command.
- [ ] Generate, recolor, and vectorize from the assistant call §2, §5, and §10 through the same gate. Done when: a test asserts a "vectorize this" plan routes to the §10 service.
- [ ] Log `Assistant plan applied: {Request}, {StepCount} steps, record {RecordId}`. Done when: the line is asserted.
- [ ] Commit: `"stilus: the AI assistant with whitelisted, undoable command plans"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~AssistantPlanValidatorTests|FullyQualifiedName~AssistantPlanApplierTests|FullyQualifiedName~SkillLoaderTests|FullyQualifiedName~DocumentDigestTests"` exits 0: a plan calling an unknown command is refused, an applied plan undoes in one step, and the digest carries no geometry, all over the recorded transport. Cheaper substitute that fails: free-form SVG edits from the model, which the whitelist rejects.

## 7. AI Text: Rewrite, Translate, Proofread, Fit, and Retype

Text features keep the designer's formatting and fonts: rewriting and translation preserve formatting runs, grammar checking reports issues the user accepts one at a time, and retype matches glyphs against installed fonts locally so no font list leaves the machine. Spelling stays with the Windows Spell Checking API that `D02 T10 §13` wires. Catalog: NP-2513 (retype: identify fonts), NP-2514 (retype: convert image text to live text), NP-2515 (rewrite: generate, rephrase, translate, proofread, fit text), NP-2516 (grammar check), NP-2517 (grammar check options and checking styles). **Pinxit second consumer (2026-09-26):** the `FontMatcher` built here moves to `Isotone.Core/Text/` in `D03 T19 §11`, Stilus consuming it unchanged.

**Fidelity:** AI Text: Rewrite, Translate, Proofread, Fit, and Retype -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/ai-rewrite/, docs/captures/golden/stilus/retype/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Progress/README.md, docs/design/components/ContextMenu/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/ai-rewrite/ and docs/captures/stilus/retype/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can improve or translate copy in place and turn text in an image into live text in a matching installed font. Consumer: the text model and the document.
**Treatment:** a Rewrite panel with before and after preview that keeps character formatting runs, a Grammar dialog listing issues with rule, suggestion, Replace, Skip, and Add, and a Retype panel listing candidate installed fonts with confidence. Cheaper substitute that fails the checkpoint: replacing the text frame's content with plain unformatted text.
**Chrome:** consume the `D02 T10` text model, the Windows Spell Checking API integration of `D02 T10 §13`, the send gate, and provenance. Do not add a second spell checker.

**Requires:** display-session -- panel captures need an interactive desktop

- [ ] Add `RewriteRunMapper` in `Isotone.Stilus.Core/AI/Text/` sending text as formatting runs (`[{text, runId}]`) and requiring the reply's runs to carry the same ids; missing or extra ids are refused by name. Done when: `RewriteRunMapperTests` keep a bold and a regular run after a recorded translation reply, and refuse a reply with a missing id.
- [ ] Rewrite modes (generate, rephrase, translate with a target language, proofread) as prompt templates hashed into provenance. Done when: a test asserts each mode's template hash in the record.
- [ ] Fit text: the target character count comes from the frame's overflow, the model shortens, and the result is verified locally by re-laying out the frame; a result that still overflows is shown with a warning, not applied silently. Done when: `FitTextTests` assert the relaid frame has no overflow for the recorded fixture and the warning for the overflowing one.
- [ ] Add the Rewrite panel with before and after preview; Apply writes one undoable text command with provenance. Done when: a view-model test asserts Undo restores the original runs; capture committed.
- [ ] Add `GrammarChecker` asking for issues as `{start, length, rule, message, suggestion}`, with checking styles (Quick, Strict, Formal, Informal, Technical, Advertising, Fiction) as prompt templates. Done when: `GrammarIssueParserTests` parse the fixture reply into issues with exact offsets.
- [ ] Grammar options as settings: `stilus.ai.grammar.autoStart`, `stilus.ai.grammar.promptBeforeReplace`, `stilus.ai.grammar.suggestSpelling`, and `stilus.ai.grammar.style`, each read by `GrammarChecker` or the dialog. Done when: a settings readback test asserts each default and its consumer.
- [ ] Add the Grammar dialog (issue list, rule, suggestion, Replace, Skip, Add to the user dictionary through `D02 T10 §13`); each Replace is one undoable text command. Done when: a view-model test replaces two issues and asserts two history steps.
- [ ] Retype: render the selected image region or outlined text to PNG and send it as vision input asking for glyph features (serif, weight, width, x-height ratio, stroke contrast) and the recognized text. Done when: a test asserts the `AiSendPlan` holds only the region PNG and no font list.
- [ ] Add `FontMatcher` ranking installed fonts locally by rendering the recognized text in each candidate and comparing perceptual hash distance to the source. Done when: `FontMatcherTests` rank the true font first for a committed sample rendered in a known installed font.
- [ ] Convert to live text creates `SvgText` over the image region in the chosen font and hides the source, in one undoable command with provenance. Done when: a test asserts the new text element, the hidden source, and one-step undo.
- [ ] Log `AI text {Mode} applied to {RunCount} runs` and `Retype matched {Font} ({Confidence})`. Done when: both lines are asserted.
- [ ] Commit: `"stilus: AI rewrite, grammar, fit text, and retype with formatting kept"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~RewriteRunMapperTests|FullyQualifiedName~GrammarIssueParserTests|FullyQualifiedName~FontMatcherTests|FullyQualifiedName~FitTextTests"` exits 0: a two-run bold and regular paragraph keeps both runs after a recorded translation reply, the grammar parser yields exact offsets, and the font matcher ranks the true font first; no test needs a live key. Cheaper substitute that fails: plain-text replacement, which drops the bold run and fails the run-mapper test.

## 8. AI Images: Generate, Remix, and Reference Images

Raster generation stays outside the drawing: results are placed as ordinary image objects with their provenance, never merged into existing artwork. Catalog: NP-2518 (quick generate dialog), NP-2519 (AI Generate panel), NP-2520 (text to image as a placed image), NP-2521 (reference image generation), NP-2522 (remix image), NP-2523 (aspect ratio and image format), NP-2524 (image style presets).

**Fidelity:** AI Images: Generate, Remix, and Reference Images -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/ai-generate/.
**Design:** docs/design/components/Panel/README.md, docs/design/components/Dialog/README.md, docs/design/components/TextBox/README.md, docs/design/components/Slider/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/ai-generate/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can generate or remix a raster image and place it as an ordinary image object. Consumer: the document's placed image objects and provenance store.
**Treatment:** an AI Generate panel (prompt, mode Create or Remix, reference image, aspect ratio, style preset, palette preset, model, count) and a one-dialog Quick Generate from the File menu; results arrive as placed images. Cheaper substitute that fails the checkpoint: pasting generated pixels into existing artwork.
**Chrome:** consume the `D02 T12 §1` placed image objects, the send gate, provenance, and the shared progress panel. Do not add a second image-placement path.

**Requires:** display-session -- panel and dialog captures need an interactive desktop

- [ ] Add `ImageGenerationService` in `Isotone.Stilus.Core/AI/Images/` building `ImageRequest` for image-output models filtered from the catalog, with aspect ratios 1:1, 4:3, 3:2, 16:9, 9:16, and a custom size. Done when: `ImageGenerationServiceTests` assert the request fixture for each ratio.
- [ ] Results embed as PNG image objects on a layer "Generated", named by prompt excerpt, carrying `stilus:provenance-id`. Done when: `GeneratedImagePlacementTests` assert the layer, name, and attribute.
- [ ] Placement is one undoable command and leaves every existing element byte-identical. Done when: `GeneratedImagePlacementTests.ExistingUnchanged` hashes every other element before and after.
- [ ] Reference image: the selected image or a file, sent as input and listed in the preview. Done when: a test asserts the `AiSendPlan` part and its byte count.
- [ ] Remix sends the selected image with an edit instruction and places the result beside the original. Done when: a test asserts the original is untouched and the result is offset beside it.
- [ ] Style presets and palette presets are local JSON shared with §2 and §5; `stilus.ai.image.stylePreset` is remembered per app, independent of Pinxit. Done when: a settings readback asserts the remembered preset.
- [ ] Add the AI Generate panel (`Views/Panels/AiGeneratePanel.xaml`) with mode, reference, ratio, presets, model, and count. Done when: a view-model test asserts the request built from the panel state; capture committed.
- [ ] Add the Quick Generate dialog (`File, Quick Generate`) wrapping the same service with Create Image, Remix Image, and Create Vector (routing to §2). Done when: a test asserts Create Vector opens the §2 flow.
- [ ] Failures use the `D01 T05 §1` mapping with a Retry button; a cancelled generation places nothing. Done when: a test cancels mid-request and asserts no element was added.
- [ ] Log `Generated image placed: {Width}x{Height}, record {RecordId}`. Done when: the line is asserted.
- [ ] Commit: `"stilus: AI image generation and remix as placed images with provenance"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ImageGenerationServiceTests|FullyQualifiedName~GeneratedImagePlacementTests"` exits 0 over the recorded image fixtures: the result is a separate image object and every existing element is byte-identical after placement; no live key is used. Cheaper substitute that fails: merging pixels into an existing image, which the element comparison catches.

## 9. AI Image Cleanup: Remove Background, Upscale, Repair, and Art Style

Cleanup operations are non-destructive by construction: each produces a new image object above the hidden, locked original, linked by provenance so Revert restores it. Local fallbacks from the pixel engine are offered by name when AI is off. Catalog: NP-2525 (remove background), NP-2526 (AI upsampling in illustration and photo modes), NP-2527 (upsample noise reduction), NP-2528 (remove JPEG artifacts), NP-2529 (art style transfer), NP-2530 (art style presets).

**Fidelity:** extends the bitmap contextual bar and Resample dialog -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/bitmap-resample/, docs/captures/golden/stilus/art-style/.
**Design:** docs/design/components/OptionsBar/README.md, docs/design/components/Dialog/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: extends the bitmap contextual bar and Resample dialog -- docs/captures/stilus/bitmap-resample/ (from `D02 T12 §1`); the new Art Style dialog is new build, no baseline, captured to docs/captures/stilus/art-style/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can clean up a placed image without leaving Stilus and without losing the original. Consumer: the document's image objects and provenance store.
**Treatment:** Remove Background, Upscale, Remove JPEG Artifacts, and Art Style commands on the image contextual bar, each producing a new image object above the hidden original. Cheaper substitute that fails the checkpoint: overwriting the embedded image.
**Chrome:** consume the `D02 T12 §1` placed images, the send gate, provenance, and the `D01 T03` pixel engine for local pre and post steps. Do not add a second resampler.

**Requires:** display-session -- before and after captures need an interactive desktop

- [ ] Add `ImageCleanupService` in `Isotone.Stilus.Core/AI/Images/` with one method per operation, each calling an image-edit model through the gate with the image size shown in the preview. Done when: `ImageCleanupServiceTests` assert one recorded request per operation.
- [ ] Remove Background returns a cut-out PNG; a local alpha threshold builds the mask, the result is a new image with its bounds shrunk to the subject, and an optional clipping path is traced from the mask. Done when: a test asserts the new image's bounds and the optional path's existence.
- [ ] Upscale: modes Illustration and Photo, factor 2x or 4x, noise reduction 0 to 100 as a request parameter. Done when: a test asserts the parameters in the request and the result's pixel size.
- [ ] When AI is off or no key is set, Upscale offers the local Lanczos resampler from `D01 T03 §2` by name ("Upscale locally (Lanczos)"). Done when: a test with no key asserts the local path runs and zero gate calls happen.
- [ ] Remove JPEG Artifacts as an image-edit call, with a local deblocking fallback labeled lower quality. Done when: a test asserts both paths and the label.
- [ ] Art Style: Stilus's own preset list (Acrylic, Graphite, Pastel, Mosaic, Neon, Woodcut, Watercolor, and more) in local JSON with intensity and detail sliders, in an Art Style dialog. Done when: a test loads every preset and asserts intensity and detail reach the request.
- [ ] Art Style on a vector group rasterizes the group locally, produces a new image, and keeps the group hidden. Done when: a test asserts the group is hidden and unchanged element by element.
- [ ] Every result is a new object with the original hidden and locked beneath, linked by provenance, so Revert in the provenance panel restores the original. Done when: `CleanupResultPlacementTests` assert the original image bytes are unchanged for each of the four operations and Revert restores visibility.
- [ ] Log `Image cleanup {Operation} on {ObjectId}: record {RecordId}`. Done when: the line is asserted.
- [ ] Commit: `"stilus: non-destructive AI image cleanup with local fallbacks"`

**Test checkpoint:** Unit test: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ImageCleanupServiceTests|FullyQualifiedName~CleanupResultPlacementTests"` exits 0 over the recorded transport: the original image bytes are unchanged and the result is a new object for each of the four operations, and the no-key path runs the local resampler with zero gate calls. Cheaper substitute that fails: replacing the embedded bytes, which the byte comparison catches.

## 10. Concept to Vector: Sketches and Images to Structured Vectors

A sketch or photo becomes organized vectors by one of two user-chosen routes: Structured, where a vision model returns a §2 vector scene with named parts, and Trace-assisted, where the model returns only tracing parameters and the local potrace port (`D02 T12 §5`) does the geometry, deterministically. Catalog: NP-2531 (concept to vector from sketches and photos), NP-2532 (variations, reference match, and raster output), NP-2533 (trace with AI background removal first), NP-2534 (AI-assisted trace preparation).

**Fidelity:** Concept to Vector: Sketches and Images to Structured Vectors -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/concept-to-vector/.
**Design:** docs/design/components/Dialog/README.md, docs/design/components/Slider/README.md, docs/design/components/ComboBox/README.md, docs/design/components/Progress/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/concept-to-vector/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can turn a rough sketch or photo into organized, editable vectors. Consumer: the document and the live trace object.
**Treatment:** a Concept to Vector panel (source image, a style preset strip of up to 8, match reference toggle, output Vector or Raster, model) and an "AI Prepare" step in the `D02 T12 §5` trace dialog. Cheaper substitute that fails the checkpoint: sending the image to a model and placing its raster output as the vector result.
**Chrome:** consume the §2 applier, the local potrace port in `Isotone.Stilus.Core/Tracing/`, and the `D01 T03 §3` quantization. Do not add a second tracer.

**Requires:** display-session -- panel and trace captures need an interactive desktop

- [ ] Add `ConceptToVectorService` in `Isotone.Stilus.Core/AI/` with two routes chosen by the user: Structured (vision model returns a `vector-scene.v1` scene with named parts such as "head" or "background") and Trace-assisted. Done when: a test asserts the route choice selects the schema sent.
- [ ] Add the schema `trace-parameters.v1.json` (color count, palette hex list, smoothing, corner threshold, region hints) and `TraceParametersValidator` bounding each value to the tracer's accepted range. Done when: `TraceParametersValidatorTests` reject out-of-range values and accept the fixture.
- [ ] Trace-assisted: the model returns only `TraceParameters`; the local tracer does the geometry and keeps the trace source unexpanded as a live trace object per `D02 T07 §1`, so the user can retune without another request. Done when: a test asserts the live trace object carries the recorded parameters and no second request is made on retune.
- [ ] Add the AI Prepare button to the `D02 T12 §5` trace dialog, filling its fields from the returned parameters. Done when: a view-model test asserts every field is filled from the fixture reply.
- [ ] Optional pre-steps: background removal and upscale from §9, each listed in the send preview. Done when: a test with both enabled asserts three parts in the plan in order.
- [ ] Up to 8 variations across style presets in one preview; Raster Output places a cleaned image instead through §8. Done when: a test asserts 8 requests for 8 presets and a placed image for Raster Output.
- [ ] Match reference: an extra reference image steers style, and its hash goes into provenance. Done when: a test asserts the hash in the record.
- [ ] Add the Concept to Vector panel. Done when: a view-model test asserts the request built from the panel; capture committed.
- [ ] Commit the sketch fixture `tests/fixtures/stilus/ai/concept-sketch.png`, recorded replies `concept-*.json`, and golden SVGs. Done when: each route has a fixture and a golden.
- [ ] Log `Concept to vector ({Route}): {ElementCount} elements, record {RecordId}`. Done when: the line is asserted.
- [ ] Commit: `"stilus: concept to vector through structured scenes or AI-prepared local tracing"`

**Test checkpoint:** Format fidelity proof: `dotnet test Isotone.slnx --filter "FullyQualifiedName~ConceptToVectorApplierTests|FullyQualifiedName~TraceParametersValidatorTests"` exits 0: the trace-assisted route on the committed sketch fixture with recorded parameters produces an SVG matching its golden element by element (deterministic because the tracer is local), and the structured route's saved SVG matches its golden; no live key is used. Cheaper substitute that fails: a raster placed as the result, which the element comparison catches.

## 11. The Suite Pipeline: Albumen to Pinxit to Stilus Hand-offs and Shared Brand Kits

The suite works as one pipeline without any app depending on another at runtime: images arrive from Albumen and Pinxit through a watched hand-off folder or Open With, a placed image goes to Pinxit for cleanup and is relinked when Pinxit saves it, provenance travels across in sidecar files, and brand kits sync through the shared folder of `D01 T05 §5`. Other apps are located through their Windows App Paths entries, the same lookup Albumen's Edit in Pinxit (`D04 T02 §7`) uses, so this section adds `SuiteAppLocator` to `Isotone.Core` with Stilus as its first consumer and `D04 T02 §7` as its second. Pinxit can open and save PNG only after `D03 T04 §2`, which runs after this phase, so the driven round trip here uses a stub editor registered under App Paths, and the real Pinxit round trip is checked when `D03 T04 §2` ships. Catalog: NP-2535 (linked variations across documents), NP-2536 (suite launcher and hand-offs to Pinxit and Albumen).

**Fidelity:** The Suite Pipeline: Albumen to Pinxit to Stilus Hand-offs and Shared Brand Kits -- the design named on the Design line below, per standards/design-contract.md; goldens under docs/captures/golden/stilus/suite-handoff/.
**Design:** docs/design/components/Menu/README.md, docs/design/components/Dialog/README.md, docs/design/components/Panel/README.md, docs/design/components/ListTree/README.md, docs/design/components/Toast/README.md -- states: all in spec -- themes: all four -- density: both
**Corrected 2026-09-27:** the design contract (`standards/design-contract.md`, operator decisions that day: "Exact tokens + ±1 DIP geometry + approved goldens", golden sign-off by the review panel only) replaces the capture comparison. The Fidelity line said: new build, no baseline; captured to docs/captures/stilus/suite-handoff/. The source is now the design named on the Design line; the captures under `docs/captures/stilus/` are before records only, and the approved renders land under `docs/captures/golden/stilus/`.
**Job:** a designer can move an image from Albumen through Pinxit into a Stilus trace without manual file juggling. Consumer: the placed image's link, the provenance store, and the other app through the file.
**Treatment:** an image context command "Edit in Pinxit", a suite launcher menu listing only installed suite apps, and a Hand-off panel listing files arriving from Albumen or Pinxit with their source app, time, and provenance, with Place and Trace actions. Cheaper substitute that fails the checkpoint: a hard project reference to Pinxit, or a launcher that shows apps that are not installed.
**Chrome:** consume the `D01 T02 §3` single instance and file-open forwarding, the `D01 T05 §5` brand kit library, provenance, and the `D02 T12 §7` linked images. Do not add a second file watcher service.

**Requires:** display-session -- the hand-off round trip is a driven run

- [ ] Add `src/Isotone.Core/Suite/SuiteAppLocator.cs` reading each suite app's App Paths entry (`HKCU`, then `HKLM\Software\Microsoft\Windows\CurrentVersion\App Paths\<App>.exe`) and verifying the exe exists, behind an `IRegistryReader` for tests. Done when: `SuiteAppLocatorTests` (fake registry) assert found, missing key, and key pointing at a deleted exe.
- [ ] Absent apps are refused by name ("Pinxit is not installed") and their launcher entries are hidden, not disabled. Done when: a view-model test with Pinxit absent asserts the refusal sentence and no launcher entry.
- [ ] Add the suite launcher menu (Window, Suite Apps) listing installed apps and starting them with the current selection exported when chosen. Done when: a view-model test with a fake locator lists exactly the installed apps.
- [ ] Edit in Pinxit writes the placed image to `%LOCALAPPDATA%\Rizonesoft\Isotone\handoff\<guid>.png` through the atomic writer with a sidecar `<guid>.provenance.json`, and starts Pinxit with the file path. Done when: `HandoffRoundTripTests.Export` asserts both files and the launch arguments through a fake launcher.
- [ ] Refuse a hand-off whose folder permissions deny writing (read-only or locked) with "Cannot write the hand-off file to <folder>: <reason>", leaving the document unchanged. Done when: `HandoffRoundTripTests.ReadOnlyFolder_Refuses` asserts the sentence and no launch.
- [ ] Watch the hand-off file and relink the placed image when it changes, as one undoable relink command. Done when: `HandoffRoundTripTests.Relink` modifies the file and asserts the new bytes are linked and Undo restores the old link.
- [ ] Add the hand-off inbox: a `FileSystemWatcher` on `handoff\inbox\stilus\`; files appear in a Hand-off panel with source app, time, and provenance, with Place and Trace (§10). Done when: a test drops a file and sidecar and asserts the panel row.
- [ ] Open With forwarding: a second launch with a file path opens it in the running Stilus through `D01 T02 §3`. Done when: a driven run forwards a PNG and the log line `Hand-off received {Path} from {SourceApp}` is quoted.
- [ ] Provenance carry: sidecar records from Albumen or Pinxit are appended to the document with `ParentId` links so the lineage shows the whole chain, with `App` preserved. Done when: `HandoffRoundTripTests.ProvenanceChain` asserts a three-record lineage.
- [ ] Brand kit sync: the Hand-off panel header shows the active kit from the shared folder and refreshes on `KitsChanged`. Done when: a test writes a kit from a second library instance and asserts the refresh.
- [ ] Linked variations: a variation set can be referenced from another document by record id; `Swap Variation` updates every linked instance, undoable per document. Done when: `LinkedVariationTests` swap in one document and assert the other updates on reload.
- [ ] Add `ProjectReferenceGuardTests` asserting `Isotone.Stilus.Desktop` and `Isotone.Stilus.Core` reference no Pinxit or Albumen project or assembly. Done when: the test parses the csproj files and passes.
- [ ] Add the stub editor `tests/Isotone.HandoffStub/` (a console app that opens a PNG, inverts one pixel, and saves it) used by the driven run through a temporary App Paths entry. Done when: the stub builds in `Isotone.slnx` and is excluded from every installer.
- [ ] Log `Hand-off sent {Path} to {App}`, `Hand-off relinked {ObjectId}`, and `Hand-off refused: {App} is not installed`. Done when: all three lines appear across the tests and the driven run.
- [ ] Commit: `"stilus: file-based suite hand-offs, the suite launcher, and linked variations"`

**Test checkpoint:** Driven run with evidence plus unit test: a driven Edit in Pinxit against the stub editor registered under App Paths produces the three log lines (quoted) and a relinked image, and with the App Paths entry removed the command refuses by name; `dotnet test Isotone.slnx --filter "FullyQualifiedName~SuiteAppLocatorTests|FullyQualifiedName~HandoffRoundTripTests|FullyQualifiedName~ProjectReferenceGuardTests|FullyQualifiedName~LinkedVariationTests"` exits 0, proving the provenance chain and that no Pinxit or Albumen reference exists. Cheaper substitute that fails: a direct project reference to Pinxit, which the guard test fails.

## Verification

- [ ] `pwsh scripts/check-all.ps1` -- exits 0: Debug and Release build with warnings as errors, tests pass, TODO gates green
- [ ] `dotnet test Isotone.slnx --filter "FullyQualifiedName~Isotone.Stilus.Tests.AI"` exits 0 with the network unavailable to the test host: every section proves itself on the `D01 T05 §1` recorded transport, and no test reads a key
- [ ] Every AI apply in a driven session of all eleven sections shows exactly one history step, one provenance record in the saved SVG, and one log line (the session log quoted)
- [ ] `tests/fixtures/stilus/ai/provenance-two-records.svg` and every AI golden round-trip element by element
- [ ] Every AI menu item is wired; `PlannedCommands.cs` holds no `D02 T15` ref
- [ ] Captures under `docs/captures/stilus/` exist for every surface named in a Fidelity line, and `docs/user/stilus/ai.md` documents each
- [ ] `python scripts/todo-graph.py validate` clean
