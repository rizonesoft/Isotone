# Standards

The standards every change in the Isotone Graphics Suite answers to. [`AGENTS.md`](../AGENTS.md) holds the binding decisions and the working rules for agents; these files hold the detail. Where a file here and `AGENTS.md` disagree, `AGENTS.md` wins and the file is corrected in the same commit.

| File | Covers |
| ---- | ------ |
| [`shared.md`](shared.md) | Everything all apps share: the stack, C# style, MVVM, DI, logging, errors, documents, performance, commits, and a pointer to the design contract |
| [`design-contract.md`](design-contract.md) | The **design contract**, binding: docs/design is the source and code implements it 1:1, what fidelity means (exact tokens, geometry within 1 DIP, every state and theme, approved goldens), deviations, the enforcement gates, and the definition of done for a UI section |
| [`ui.md`](ui.md) | The **UI standard** every surface answers to: themes, the Highlight color and app accents, type, density, focus, icons, window anatomy, accessibility, and the WPF mapping, summarizing the design system in [`docs/design/`](../docs/design/README.md) |
| [`stilus.md`](stilus.md) | Stilus, the vector editor: the document model, the canvas, tools, SVG, icons |
| [`gesso.md`](gesso.md) | Gesso, the raster editor: tiles, zero-allocation hot paths, GPU shaders, codecs |
| [`albumen.md`](albumen.md) | Albumen, the darkroom: the original-file guard, the catalog, the develop pipeline |
| [`testing.md`](testing.md) | Test projects, naming, fixtures, fidelity proofs, the quarantine |
| [`release.md`](release.md) | Versions, tags, changelogs, installers, the release checklist |

The legacy per-app standards (`src/Nodus/STANDARDS.md`, `src/Imago/STANDARDS.md`, their paths before the 2026-09-27 rename) were merged into these files on 2026-09-26 and removed; git history keeps them.
