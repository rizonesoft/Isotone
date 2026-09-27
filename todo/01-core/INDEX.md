# 01 Core

> **Phases 2, 3, 6, 9, 10, 12, 13, 15, 21 to 23, 36, and 42 to 44**

The two shared libraries: `Photon.Core` (non-UI services) and `Photon.UI` (the WPF house style). Code arrives here only when a second app needs it now, and each move deletes the copies it replaces. Three operator exceptions (2026-09-26) are built here ahead of their second consumer because the Nodus parity phases need them first: the pixel engine (TODO-03, Imago's filter pipeline is its second consumer), color management (TODO-04, which the pixel engine's bitmap color modes need), and the AI core (TODO-05, reused by Imago and Lumen). The Imago parity plan (2026-09-26) adds two more on the same terms: the pixel engine extensions (TODO-06, the filters Imago adds for Photoshop, Affinity, and GIMP parity, which Nodus's effect gallery lists too) and the develop engine (TODO-07, the scene-referred pipeline Imago's Camera Raw filter uses first and Lumen's develop module reuses; the Lumen parity plan of 2026-09-27 adds its tone equalizer in Phase 23 and its soft focus, skin tune, LUT, and blend stages in Phase 36). On 2026-09-27 the operator directed two more ("Group 1: plan them all"): the legacy raster codecs (TODO-08, which Nodus's legacy import consumes first and Imago's and Lumen's format lists reuse) and the plug-in host (TODO-09, the isolated process that runs third-party Photoshop-compatible plug-ins for Nodus and Imago, and later Lumen). Later on 2026-09-27, when the operator worried "features will be left behind", the operator decided to plan the work deferred to after the first release as real sections, and three suite-wide systems land here because all three apps consume them: automation (TODO-10: actions, C# scripting, the automation and MCP servers, extensions, the command line, and batch with droplets, Phase 42), media (TODO-11: Media Foundation decoding, playback, audio, and encoding with an optional external FFmpeg, Phase 43), and on-device models (TODO-12: ONNX Runtime with DirectML, the model catalog with license records, and the Model Manager, Phase 44); the GPU develop path joins TODO-07 as its §10 to §12 (Phase 44).

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-photon-ui.md) | Photon.UI: the Shared WPF Library | draft |
| [TODO-02](./TODO-02-photon-core.md) | Photon.Core: Shared Services | draft |
| [TODO-03](./TODO-03-photon-pixel-engine.md) | Photon.Core Pixel Engine: Buffers, Resampling, Adjustments, and Bitmap Effects | draft |
| [TODO-04](./TODO-04-photon-color-management.md) | Photon.Core Color Management: ICC Transforms, Proofing, and Bitmap Color Modes | draft |
| [TODO-05](./TODO-05-photon-ai.md) | Photon.Core AI: OpenRouter Client, Keys, Consent, Provenance, and the Brand Kit | draft |
| [TODO-06](./TODO-06-photon-imaging-extensions.md) | Photon.Core Pixel Engine Extensions: the Filters Imago Adds for Photoshop, Affinity, and GIMP Parity | draft |
| [TODO-07](./TODO-07-photon-develop.md) | Photon.Core Develop Engine: the Scene-Referred Pipeline for Imago's Camera Raw Filter and Lumen | draft |
| [TODO-08](./TODO-08-photon-legacy-codecs.md) | Photon.Core Legacy Raster Codecs: Bitonal, Kodak, Icon, PICT, and Corel Formats | draft |
| [TODO-09](./TODO-09-photon-plugin-host.md) | Photon.Core Plug-in Host: Photoshop-Compatible Filter, Format, and Acquire Plug-ins | draft |
| [TODO-10](./TODO-10-photon-automation.md) | Photon.Core and Photon.UI Automation: Actions, Scripting, the Automation Server, Extensions, the Command Line, and Batch | draft |
| [TODO-11](./TODO-11-photon-media.md) | Photon.Core Media: Decoding, Playback, Audio, and Encoding for Video and Sound | draft |
| [TODO-12](./TODO-12-photon-local-ml.md) | Photon.Core On-Device Models: ONNX Runtime, the Model Catalog, and the Model Manager | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- `src/Photon.Core/` and `src/Photon.UI/`, their test projects, and every move of duplicated code into them
- App-data paths, logging bootstrap, settings store, single instance, undo history, atomic document writer
- Icon catalog, shared windows and dialogs, the theme resources the design contract names, the implicit control styles, and the shared window chrome (title bar, document tabs, dock theme, status bar)
- The pixel engine and its extensions, the color-management engine, the AI core (OpenRouter client, key store, explicit-send gate, provenance, brand kit), the develop engine, the legacy raster codecs Nodus, Imago, and Lumen share, the isolated host for third-party Photoshop-compatible plug-ins, the suite automation, media, and on-device model systems, and the GPU develop path

## Out of scope

- Anything only one app needs (it stays in that app's domain with a note naming the day it would move)
- The update check's release policy (05), though its code lands in `Photon.Core`

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
