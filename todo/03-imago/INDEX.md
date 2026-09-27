# 03 Imago

> **Phases 1, 14, 15, 16 to 27, 41, and 42 to 44**

Imago, the raster editor, imported under `src/Imago/`. Its rename runs early beside Nodus's; its foundation (the snapshot port, WPF-UI removal, tiles, and rendering) starts after Nodus ships 1.0.0, followed by editing, file I/O, filters, and `imago-v0.1.0`. On 2026-09-26 the operator decided Imago gets every Photoshop feature and those of two other popular raster editors (Affinity Photo and GIMP 3): the catalog in [`../../docs/parity/imago-parity.md`](../../docs/parity/imago-parity.md) routes each one to a section, and TODO-08 to TODO-21 run it in twelve parity phases (16 to 27), each ending in a release from `imago-v0.2.0` to `imago-v1.0.0`. TODO-07 keeps four legacy deferral owners at their addresses: its filter catalog runs in Phase 21, its workspaces and its accessibility audit in Phase 27, and its RAW import in Phase 41 once Lumen's decoder is shared. Later on 2026-09-27, when the operator worried "features will be left behind", the work deferred to after the first release became sections: TODO-22 (actions, scripts, procedures, extensions, batch, and data sets, Phase 42), TODO-23 (video layers, the timeline, audio, render video, frame animation, and animated formats, Phase 43), and TODO-19 §16 and §17 (on-device models, Phase 44), each phase ending in an Imago release from `imago-v1.1.0` to `imago-v1.3.0`. Ideas that are not sections wait in [`../backlog.md`](../backlog.md) and are promoted only through `add-todo`.

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
| [TODO-08](./TODO-08-imago-parity-document.md) | Imago Parity: Document, Canvas, View, History, and the Image Menu | draft |
| [TODO-09](./TODO-09-imago-parity-layers.md) | Imago Parity: Layers, Masks, Blending, Styles, Smart Objects, and Artboards | draft |
| [TODO-10](./TODO-10-imago-parity-selection.md) | Imago Parity: Selection, Refine, Channels, and Quick Mask | draft |
| [TODO-11](./TODO-11-imago-parity-adjustments.md) | Imago Parity: Adjustment Layers, Adjustments, Image Modes, and Color | draft |
| [TODO-12](./TODO-12-imago-parity-painting.md) | Imago Parity: the Brush Engine, Painting Tools, Fills, Gradients, and Patterns | draft |
| [TODO-13](./TODO-13-imago-parity-retouch.md) | Imago Parity: Retouching, Content-Aware Tools, Transform, Warp, and Liquify | draft |
| [TODO-14](./TODO-14-imago-parity-filters.md) | Imago Parity: Smart Filters, the Filter Menu, the Filter Gallery, and Interactive Filter Surfaces | draft |
| [TODO-15](./TODO-15-imago-parity-photo.md) | Imago Parity: the Camera Raw Filter, Develop Studio, Tone Mapping, and Photo Merges | draft |
| [TODO-16](./TODO-16-imago-parity-type-vector.md) | Imago Parity: Type, Paths, Shapes, and Vector Layers | draft |
| [TODO-17](./TODO-17-imago-parity-formats.md) | Imago Parity: the File Menu and Every Format | draft |
| [TODO-18](./TODO-18-imago-parity-output.md) | Imago Parity: Export, Web Output, Color Management, and Print | draft |
| [TODO-19](./TODO-19-imago-ai.md) | Imago AI: Editable, Suite-Aware, Reproducible | draft |
| [TODO-20](./TODO-20-imago-parity-workspace.md) | Imago Parity: Workspace, Customization, Preferences, and Help | draft |
| [TODO-21](./TODO-21-imago-parity-releases.md) | Imago Parity Releases: 0.2.0 to 1.0.0 | draft |
| [TODO-22](./TODO-22-imago-automation.md) | Imago Automation: Actions, Scripts, Procedures, Extensions, Batch, and Data-Driven Graphics | draft |
| [TODO-23](./TODO-23-imago-video-animation.md) | Imago Video, Timeline, Audio, and Frame Animation | draft |

## Completed

| TODO | Title | Completed |
| ---- | ----- | :-------: |

## In scope

- Everything under `src/Imago/` and `tests/Photon.Imago.*`
- Imago's surfaces, tiles, rendering, codecs, filters, and releases
- Parity with Photoshop 27.10, Affinity Photo (Affinity 3.3), and GIMP 3.2.6 as the catalog in `docs/parity/imago-parity.md` routes it

## Out of scope

- Code a second app needs (01-core), installers and signing (05-release), the user guide's content (06-docs)
- Cloud and collaboration (excluded); Affinity document import (backlog B-045) and Content Credentials (backlog B-047)

---

Format spec: [../README.md](../README.md) · Root index: [../TODO-00-INDEX.md](../TODO-00-INDEX.md)
