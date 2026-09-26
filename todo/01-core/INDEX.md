# 01 Core

> **Phases 2, 3, 6, 9, 10, 12, and 15**

The two shared libraries: `Photon.Core` (non-UI services) and `Photon.UI` (the WPF house style). Code arrives here only when a second app needs it now, and each move deletes the copies it replaces. Three operator exceptions (2026-09-26) are built here ahead of their second consumer because the Nodus parity phases need them first: the pixel engine (TODO-03, Imago's filter pipeline is its second consumer), color management (TODO-04, which the pixel engine's bitmap color modes need), and the AI core (TODO-05, reused by Imago and Lumen).

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-photon-ui.md) | Photon.UI: the Shared WPF Library | draft |
| [TODO-02](./TODO-02-photon-core.md) | Photon.Core: Shared Services | draft |
| [TODO-03](./TODO-03-photon-pixel-engine.md) | Photon.Core Pixel Engine: Buffers, Resampling, Adjustments, and Bitmap Effects | draft |
| [TODO-04](./TODO-04-photon-color-management.md) | Photon.Core Color Management: ICC Transforms, Proofing, and Bitmap Color Modes | draft |
| [TODO-05](./TODO-05-photon-ai.md) | Photon.Core AI: OpenRouter Client, Keys, Consent, Provenance, and the Brand Kit | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- `src/Photon.Core/` and `src/Photon.UI/`, their test projects, and every move of duplicated code into them
- App-data paths, logging bootstrap, settings store, single instance, undo history, atomic document writer
- Icon catalog, shared windows and dialogs, the theme resources the design contract names
- The pixel engine, the color-management engine, and the AI core (OpenRouter client, key store, explicit-send gate, provenance, brand kit)

## Out of scope

- Anything only one app needs (it stays in that app's domain with a note naming the day it would move)
- The update check's release policy (05), though its code lands in `Photon.Core`

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
