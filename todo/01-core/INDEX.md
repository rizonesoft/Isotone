# 01 Core

> **Phases 2, 3, and 5**

The two shared libraries: `Photon.Core` (non-UI services) and `Photon.UI` (the WPF house style). Code arrives here only when a second app needs it now, and each move deletes the copies it replaces.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-photon-ui.md) | Photon.UI: the Shared WPF Library | draft |
| [TODO-02](./TODO-02-photon-core.md) | Photon.Core: Shared Services | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- `src/Photon.Core/` and `src/Photon.UI/`, their test projects, and every move of duplicated code into them
- App-data paths, logging bootstrap, settings store, single instance, undo history, atomic document writer
- Icon catalog, shared windows and dialogs, the theme resources the design contract names

## Out of scope

- Anything only one app needs (it stays in that app's domain with a note naming the day it would move)
- The update check's release policy (05), though its code lands in `Photon.Core`

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
