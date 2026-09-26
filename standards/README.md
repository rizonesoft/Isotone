# Standards

The standards every change in the Photon Graphics Suite answers to. [`AGENTS.md`](../AGENTS.md) holds the binding decisions and the working rules for agents; these files hold the detail. Where a file here and `AGENTS.md` disagree, `AGENTS.md` wins and the file is corrected in the same commit.

| File | Covers |
| ---- | ------ |
| [`shared.md`](shared.md) | Everything all apps share: the stack, C# style, MVVM, DI, logging, errors, documents, performance, commits, and the **design contract** every surface answers to |
| [`nodus.md`](nodus.md) | Nodus, the vector editor: the document model, the canvas, tools, SVG, icons |
| [`imago.md`](imago.md) | Imago, the raster editor: tiles, zero-allocation hot paths, GPU shaders, codecs |
| [`lumen.md`](lumen.md) | Lumen, the darkroom: the original-file guard, the catalog, the develop pipeline |
| [`testing.md`](testing.md) | Test projects, naming, fixtures, fidelity proofs, the quarantine |
| [`release.md`](release.md) | Versions, tags, changelogs, installers, the release checklist |

The legacy per-app standards (`src/Nodus/STANDARDS.md`, `src/Imago/STANDARDS.md`) were merged into these files on 2026-09-26 and removed; git history keeps them.
