# 03 Imago

> **Phases 1, 14, 15, and 19**

Imago, the raster editor, imported under `src/Imago/`. Its rename runs early beside Nodus's; its foundation (the snapshot port, WPF-UI removal, tiles, and rendering) starts after Nodus ships 0.1.0, followed by editing, file I/O, filters, and `imago-v0.1.0`. After the suite release, TODO-07 ships the filter catalog, RAW import, workspaces, and accessibility the plan already names; the rest of the legacy roadmap waits in [`../backlog.md`](../backlog.md) (B-014 to B-027) and is promoted only through `add-todo`.

## TODOs

| TODO | Title | Status |
| ---- | ----- | :----: |
| [TODO-01](./TODO-01-imago-structure.md) | Imago Layout, Names, the Snapshot Port, and WPF-UI Removal | draft |
| [TODO-02](./TODO-02-imago-rendering.md) | Imago Tiles, Viewport, and the Render Pipeline | draft |
| [TODO-03](./TODO-03-imago-editing.md) | Imago Documents, Layers, Tools, and History | draft |
| [TODO-04](./TODO-04-imago-files.md) | Imago File I/O | draft |
| [TODO-05](./TODO-05-imago-adjustments.md) | Imago Filters and Adjustments for 0.1.0 | draft |
| [TODO-06](./TODO-06-imago-release.md) | Imago 0.1.0 | draft |
| [TODO-07](./TODO-07-imago-roadmap.md) | Imago after 0.1.0: Deferral Owners and Accessibility | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- Everything under `src/Imago/` and `tests/Photon.Imago.*`
- Imago's surfaces, tiles, rendering, codecs, filters, and release

## Out of scope

- Code a second app needs (01-core), installers and signing (05-release), the user guide's content (06-docs)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
