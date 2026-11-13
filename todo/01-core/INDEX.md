# 01 Core

> **Phases 1, 2, 3, 6, 9, 10, 12, 13, 15, 21 to 23, 36, and 48 to 50**

The two shared libraries: `isotone::core` (non-UI services, `native/core/`) and `isotone::ui` (the native UI toolkit on Win32, Direct2D, DirectWrite, and Direct3D, `native/ui/`). Code arrives here only when a second app needs it now, and each move deletes the copies it replaces. The fourteen foundation files (TODO-14 to TODO-27, Phase 1, authored by `D00 T07 §3` on 2026-11-13) prove the mechanisms the native stack spec's "The order of work" step 2 lists, each in the one shared foundation test host with placeholder menus and panels, before any control or app section depends on them; TODO-01 to TODO-13 are the C#-era plans the later re-plan sections of `D00 T07` rewrite onto the native stack. Three operator exceptions (2026-09-26) are built here ahead of their second consumer because the Stilus parity phases need them first: the pixel engine (TODO-03, Gesso's filter pipeline is its second consumer), color management (TODO-04, which the pixel engine's bitmap color modes need), and the AI core (TODO-05, reused by Gesso and Albumen). The Gesso parity plan (2026-09-26) adds two more on the same terms: the pixel engine extensions (TODO-06, the filters Gesso adds for Photoshop, Affinity, and GIMP parity, which Stilus's effect gallery lists too) and the develop engine (TODO-07, the scene-referred pipeline Gesso's Camera Raw filter uses first and Albumen's develop module reuses; the Albumen parity plan of 2026-09-27 adds its tone equalizer in Phase 23 and its soft focus, skin tune, LUT, and blend stages in Phase 36). On 2026-09-27 the operator directed two more ("Group 1: plan them all"): the legacy raster codecs (TODO-08, which Stilus's legacy import consumes first and Gesso's and Albumen's format lists reuse) and the plug-in host (TODO-09, the isolated process that runs third-party Photoshop-compatible plug-ins for Stilus and Gesso, and later Albumen). Later on 2026-09-27, when the operator worried "features will be left behind", the operator decided to plan the work deferred to after the first release as real sections, and three suite-wide systems land here because all three apps consume them: automation (TODO-10: actions, C# scripting, the automation and MCP servers, extensions, the command line, and batch with droplets, Phase 48), media (TODO-11: Media Foundation decoding, playback, audio, and encoding with an optional external FFmpeg, Phase 49), and on-device models (TODO-12: ONNX Runtime with DirectML, the model catalog with license records, and the Model Manager, Phase 50); the GPU develop path joins TODO-07 as its §10 to §12 (Phase 50).

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-isotone-ui.md) | Isotone.UI: the Shared WPF Library | draft |
| [TODO-02](./TODO-02-isotone-core.md) | Isotone.Core: Shared Services | draft |
| [TODO-03](./TODO-03-isotone-pixel-engine.md) | Isotone.Core Pixel Engine: Buffers, Resampling, Adjustments, and Bitmap Effects | draft |
| [TODO-04](./TODO-04-isotone-color-management.md) | Isotone.Core Color Management: ICC Transforms, Proofing, and Bitmap Color Modes | draft |
| [TODO-05](./TODO-05-isotone-ai.md) | Isotone.Core AI: OpenRouter Client, Keys, Consent, Provenance, and the Brand Kit | draft |
| [TODO-06](./TODO-06-isotone-imaging-extensions.md) | Isotone.Core Pixel Engine Extensions: the Filters Gesso Adds for Photoshop, Affinity, and GIMP Parity | draft |
| [TODO-07](./TODO-07-isotone-develop.md) | Isotone.Core Develop Engine: the Scene-Referred Pipeline for Gesso's Camera Raw Filter and Albumen | draft |
| [TODO-08](./TODO-08-isotone-legacy-codecs.md) | Isotone.Core Legacy Raster Codecs: Bitonal, Kodak, Icon, PICT, and Corel Formats | draft |
| [TODO-09](./TODO-09-isotone-plugin-host.md) | Isotone.Core Plug-in Host: Photoshop-Compatible Filter, Format, and Acquire Plug-ins | draft |
| [TODO-10](./TODO-10-isotone-automation.md) | Isotone.Core and Isotone.UI Automation: Actions, Scripting, the Automation Server, Extensions, the Command Line, and Batch | draft |
| [TODO-11](./TODO-11-isotone-media.md) | Isotone.Core Media: Decoding, Playback, Audio, and Encoding for Video and Sound | draft |
| [TODO-12](./TODO-12-isotone-local-ml.md) | Isotone.Core On-Device Models: ONNX Runtime, the Model Catalog, and the Model Manager | draft |
| [TODO-13](./TODO-13-isotone-layout-maps.md) | Layout Maps: Menus, Tools, Panels, and Buttons Where an Adobe User Expects Them | draft |
| [TODO-14](./TODO-14-foundation-theming.md) | Foundation: Runtime Theming from the Design Tokens | draft |
| [TODO-15](./TODO-15-foundation-window.md) | Foundation: a Window with the Isotone Title Bar on the Swap Chain and Partial-Redraw Contract | draft |
| [TODO-16](./TODO-16-foundation-device-loss.md) | Foundation: Device-Loss Recovery and the WARP Fallback | draft |
| [TODO-17](./TODO-17-foundation-display-color.md) | Foundation: the Display Color Pipeline in SDR, Advanced Color SDR, and HDR | draft |
| [TODO-18](./TODO-18-foundation-tasks.md) | Foundation: the Task System and Threading | draft |
| [TODO-19](./TODO-19-foundation-document-safety.md) | Foundation: Document Safety -- the Save Sequence, Secondary Copies, Checkpoints, and Recovery | draft |
| [TODO-20](./TODO-20-foundation-localization.md) | Foundation: Localization Services | draft |
| [TODO-21](./TODO-21-foundation-text.md) | Foundation: the Text Editing Model with the Text Services Framework | draft |
| [TODO-22](./TODO-22-foundation-accessibility.md) | Foundation: UI Automation, the Driven-Input Runner, and the Screen Reader Scenarios | draft |
| [TODO-23](./TODO-23-foundation-docking.md) | Foundation: a Docked Panel That Floats and Redocks | draft |
| [TODO-24](./TODO-24-foundation-canvas.md) | Foundation: the GPU Canvas Meeting the Frame Cadence and Pen Latency Goals | draft |
| [TODO-25](./TODO-25-foundation-goldens.md) | Foundation: the Goldens Environment and Its Repeatability Proof | draft |
| [TODO-26](./TODO-26-foundation-crash-diagnostics.md) | Foundation: Crash Diagnostics by an Out-of-Process Watcher | draft |
| [TODO-27](./TODO-27-foundation-core-services.md) | Foundation: App-Data Paths, Structured Logging, Atomic Writes, and the Settings Store | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- `native/core/` and `native/ui/`, their GoogleTest suites, the shared foundation test host `native/tests/foundation-host/`, and every move of duplicated code into them
- The Phase 1 foundations: app-data paths, structured logging, atomic writes, and the settings store, runtime theming, the window and its swap chain contract, device loss and WARP, display color, tasks and threading, document safety, localization, text with TSF, UI Automation with the driven-input runner, docking, the GPU canvas, the goldens environment, and crash diagnostics
- App-data paths, logging bootstrap, settings store, single instance, undo history, atomic document writer
- Icon catalog, shared windows and dialogs, the theme resources the design contract names, the implicit control styles, and the shared window chrome (title bar, document tabs, dock theme, status bar)
- The pixel engine and its extensions, the color-management engine, the AI core (OpenRouter client, key store, explicit-send gate, provenance, brand kit), the develop engine, the legacy raster codecs Stilus, Gesso, and Albumen share, the isolated host for third-party Photoshop-compatible plug-ins, the suite automation, media, and on-device model systems, and the GPU develop path

## Out of scope

- Anything only one app needs (it stays in that app's domain with a note naming the day it would move)
- The update check's release policy (05), though its code lands in `Isotone.Core`

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
