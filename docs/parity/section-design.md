# Nodus Parity -- Section Design

The authoring blueprint for the TODO files that bring Nodus to parity with Adobe Illustrator 30.8 and CorelDRAW Graphics Suite 2026 (v27.2), written 2026-09-26 from the unified catalog in [`nodus-parity.md`](nodus-parity.md). Agents who author the TODO files follow this document; the integration commit wires what they write into `todo/`. Nothing here is a section yet: sections exist only once authored under `todo/` and placed in `todo/implementation-plan.md`.

## Summary

- **Operator decisions (2026-09-26):** "For Nodus, we need to add all(and I mean), all CorelDraw features and All Illustrator Features." Budget raise approved: "New parity phases, up to +200".
- **Sources:** 1,294 Illustrator rows (`AI-0001` to `AI-1294`) and 3,041 CorelDRAW rows (`CD-001` to `CD-3041`), 4,335 in all.
- **Catalog:** 2,802 features (`NP-0001` to `NP-2802`), every source id in exactly one row (checked, see "Catalog check" below).
- **New sections:** 180 (179 in the ten new parity phases, including 10 release sections, plus `D00 T01 §6` in Phase 0), in 14 new TODO files and one existing file. Eight existing sections (`D02 T06 §2`, `§3`, `§7`, `§11`, `§12`, `§13`, `§14`, `§17`) move into the parity phases without changing address.
- **Budget:** the ten new phases take 209 sections of ceiling; the emptied old Phase 9 gives back its 9; the net raise is +200, inside the approved +200.

### Catalog features by status

| Status | Features | Source rows | Detail |
| ------ | -------: | ----------: | ------ |
| `plan` | 2,643 | 3,943 | owned by 166 new sections |
| `shipped-scope` | 69 | 150 | owned by 23 existing sections |
| `backlog` | 37 | 55 | B-012 1, B-037 19, B-038 12, B-039 4, B-040 1 |
| `excluded` | 35 | 169 | automation 11, cloud 23, platform 1 |
| `other-app` | 18 | 18 | Imago 9, Lumen 1, none 8 |
| **Total** | **2,802** | **4,335** | |

### Catalog features by category

| Category | Features |
| -------- | -------: |
| core | 2,391 |
| format | 144 |
| print | 138 |
| ai | 69 |
| cloud | 26 |
| companion | 18 |
| automation | 16 |

### New sections per phase

| Phase | Title | New sections | Relocated rows | Section total | Ceiling | Planned features |
| ---: | ----- | ---: | ---: | ---: | ---: | ---: |
| 4 | Nodus parity I: document model, pages, layers, selection, and view | 15 | 1 | 16 | 18 | 321 |
| 5 | Nodus parity II: drawing, paths, shapes, shaping, and transform | 16 | 1 | 17 | 19 | 332 |
| 6 | Nodus parity III: color, fills, strokes, brushes, transparency, styles, and symbols | 25 | 1 | 26 | 29 | 446 |
| 7 | Nodus parity IV: type, tables, and graphs | 16 | 1 | 17 | 19 | 300 |
| 8 | Nodus parity V: interactive and live effects | 20 | 0 | 20 | 22 | 295 |
| 9 | Nodus parity VI: bitmaps, tracing, and the shared pixel engine | 20 | 1 | 21 | 24 | 348 |
| 10 | Nodus parity VII: color management, print, prepress, and PDF | 18 | 0 | 18 | 20 | 180 |
| 11 | Nodus parity VIII: file formats, export, and web | 20 | 0 | 20 | 22 | 175 |
| 12 | Nodus AI: editable, suite-aware, reproducible | 17 | 0 | 17 | 19 | 59 |
| 13 | Nodus parity IX: workspace, customization, preferences, and Nodus 1.0.0 | 12 | 3 | 15 | 17 | 187 |
| **4-13** | | **179** | **8** | **187** | **209** | **2,643** |

Plus `D00 T01 §6` (the catalog validator) in Phase 0, which has room (13 of 15), so the new-section total is 180.

### New files

| File | Frontmatter id | Phases | Sections | Planned features | Batch |
| ---- | -------------- | ------ | ---: | ---: | :---: |
| `todo/01-core/TODO-03-photon-pixel-engine.md` | `photon-pixel-engine` | 9 | 11 | 197 | D |
| `todo/01-core/TODO-04-photon-color-management.md` | `photon-color-management` | 6, 10 | 3 | 10 | B |
| `todo/01-core/TODO-05-photon-ai.md` | `photon-ai` | 12 | 5 | 2 | E |
| `todo/02-nodus/TODO-07-nodus-parity-document.md` | `nodus-parity-document` | 4 | 14 | 321 | A |
| `todo/02-nodus/TODO-08-nodus-parity-paths.md` | `nodus-parity-paths` | 5 | 15 | 332 | A |
| `todo/02-nodus/TODO-09-nodus-parity-color.md` | `nodus-parity-color` | 6 | 22 | 440 | B |
| `todo/02-nodus/TODO-10-nodus-parity-type.md` | `nodus-parity-type` | 7 | 15 | 300 | C |
| `todo/02-nodus/TODO-11-nodus-parity-effects.md` | `nodus-parity-effects` | 8 | 19 | 295 | C |
| `todo/02-nodus/TODO-12-nodus-parity-bitmaps.md` | `nodus-parity-bitmaps` | 9 | 8 | 151 | D |
| `todo/02-nodus/TODO-13-nodus-parity-print.md` | `nodus-parity-print` | 10 | 16 | 176 | D |
| `todo/02-nodus/TODO-14-nodus-parity-formats.md` | `nodus-parity-formats` | 11 | 19 | 175 | E |
| `todo/02-nodus/TODO-15-nodus-ai.md` | `nodus-ai` | 12 | 11 | 57 | E |
| `todo/02-nodus/TODO-16-nodus-parity-workspace.md` | `nodus-parity-workspace` | 13 | 11 | 187 | B |
| `todo/02-nodus/TODO-17-nodus-parity-releases.md` | `nodus-parity-releases` | 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 | 10 | 0 | A |
| `todo/00-workspace/TODO-01-dev-automation.md` (existing, new `§6`) | `dev-automation` | 0 | 1 | 0 | A |

## How to use this blueprint

- Author one file at a time through `create-todo` (the skill's template, frontmatter, Goal, Current state with claims, Inputs, Outcome with the Adjacency line, Implementation Order, sections, Verification), taking the file's frontmatter id and title, its Goal, its Current-state facts, and every section below exactly as numbered, titled, and ordered.
- Each section's **Hints** are the concrete items it must implement; expand them into micro-steps (one action, a named path, Done when, the cheaper substitute on UI and write items, a source cite) under the 30-item cap, add the `Commit:` item, and write the **Proof** as the Test checkpoint. A section that cannot hold its hints in 30 items is split at authoring time only with the operator's budget room; otherwise its lowest-value catalog rows move to the backlog through `add-todo` and the catalog is updated in the same commit.
- Each section's **Catalog** line lists the `NP-` features it owns. The authored section names that range in its context paragraph ("Catalog: NP-0123 to NP-0150") so the catalog, the section, and the validator agree.
- UI sections carry `Fidelity:`, `Job:`, `Treatment:`, and `Chrome:` (`todo/README.md`, "The second layer the runner reads"); library sections say "no surface of its own". Sections that drive the app carry `**Requires:** display-session -- <reason>`; release sections carry `**Needs:** Clean Windows machine (no .NET SDK)`.
- A section that promotes a backlog entry carries that entry's source key as its `-> SOURCE:` line (see "Backlog changes"); the integration commit deletes the entry.
- Cross-file edges: `Depends On` always uses full refs. Where a section's Inputs name another file's section with `-> XREF:`, the integration commit adds the reciprocal line in the target file (one-sided XREFs are FATAL).

## Recorded decisions

### Names and paths

Every parity section runs after `D02 T01 §1` (Phase 1) renames Bezier to Photon.Nodus, so hints and checklist items name the target paths: `src/Nodus/Photon.Nodus.Core/`, `src/Nodus/Photon.Nodus.Desktop/`, `tests/Photon.Nodus.Tests/`, `src/Photon.Core/`, `src/Photon.UI/`, `tests/Photon.Core.Tests/`. Current-state blocks, by contrast, cite today's `src/Nodus/Bezier.*` paths, because a `<!-- claim: -->` must hold on the day the file is authored; `D02 T01 §1`'s claim-rewrite item moves them with the rename. If a file is authored after the rename has shipped, its claims use the new paths directly.

### SVG stays native; live features ride the nodus namespace

`standards/nodus.md` makes SVG the native format. Parity adds live objects SVG cannot express (blends, envelopes, extrusions, live shapes, symbol overrides, multi-page documents, text frames with threading, effect stacks). `D02 T07 §1` defines one contract for all of them: parameters in the `nodus:` XML namespace on the element, the expanded result as ordinary SVG geometry beside them, and a reader that restores the live object when the parameters are present and falls back to the geometry when they are not. Any SVG reader sees the artwork; Nodus sees the live object; a round trip through another editor degrades to expanded art, never to a missing element. This mirrors how Inkscape keeps `inkscape:` data, and it keeps Inkscape the fidelity oracle for the geometry.

### What goes to Photon.Core and Photon.UI

The rule in `AGENTS.md` is that shared code moves to `Photon.Core` only when two apps need it now. The operator made two explicit exceptions on 2026-09-26, and one more follows from them:

- **The pixel engine** (`D01 T03`, `Photon.Core/Imaging/`): operator decision. Nodus parity comes before Imago, so Nodus sections build it; Imago's filter pipeline (`D03 T05 §1`) is its planned second consumer and must consume it rather than grow its own.
- **The AI core** (`D01 T05`, `Photon.Core/AI/` and `Photon.UI/AI/`): operator decision. The OpenRouter client, the DPAPI key store, the explicit-send gate, the provenance record, and the brand kit are built once so Imago and Lumen reuse them.
- **Color management** (`D01 T04`, `Photon.Core/Color/`): the pixel engine needs ICC transforms for its Lab, CMYK, and duotone bitmap modes, so the engine it depends on sits beside it in `Photon.Core`. Imago's ICC work (`D03 T04 §2`) and Lumen's output transform (`D04 T02 §2`) are its next consumers, and backlog B-023's engine-decision part is superseded by `D01 T04 §1` (the integration commit rewords B-023 to consume it).
- **Everything else stays in Nodus** with a note naming the day it would move: text shaping (`Photon.Nodus.Core/Text/`, moves when Imago's text layers, B-018, are promoted), tracing (`Photon.Nodus.Core/Tracing/`), the color picker (moves to `Photon.UI` when Imago's color panel, `D03 T03 §8`, needs it), raster codecs through WIC (move when Imago's codec decision, `D03 T04 §1`, picks the same stack).

The "Shared once, never copied" acceptance aim gains these owners, and each of the three Photon.Core files' Verification block records its pending second consumer instead of claiming two today.

### Formats and licensing

Every dependency is checked against GPL-3.0 in the section that adds it, with a `docs/dev/decisions.md` row.

| Need | Decision | License | Why |
| ---- | -------- | ------- | --- |
| CorelDRAW `.cdr` read | Own managed reader (`D02 T14 §6`, `§7`), libcdr as the reference implementation, Inkscape's libcdr-based import as the golden oracle | libcdr is MPL-2.0; MPL-2.0 section 3.3 permits combination with GPL-3.0 unless a file is marked "Incompatible With Secondary Licenses" (libcdr's are not; verify at build time); any file translated from libcdr keeps its MPL-2.0 header | A native libcdr needs librevenge, ICU, and Boost and hands back drawing callbacks P/Invoke cannot carry cleanly; a managed reader is testable and ships no native code |
| CorelDRAW `.cdr` and `.cmx` write | Own writer targeting the RIFF layout libcdr reads (`D02 T14 §8`) | Own code | No open writer exists; the proof is a read-back through Nodus and through libcdr (Inkscape); opening in CorelDRAW itself is an operator check recorded as a risk, not a gate |
| Illustrator `.ai` read | PDF path through PdfPig plus an own parser for `AIPrivateData` and legacy PostScript AI built from Adobe's published Illustrator File Format specification (v7) (`D02 T14 §3`, `§4`) | PdfPig Apache-2.0 | Modern `.ai` files are PDF with private data; the PDF part gives exact geometry, the private part gives layers, live text, and swatches when present |
| Illustrator `.ai` write | PDF-based `.ai` through the PDF writer (layers as OCGs, artboards as pages) (`D02 T14 §5`) | Own code on PDFsharp (MIT) | Illustrator opens PDF-compatible `.ai`; Illustrator-only live data is expanded with a report |
| PDF write | Own content-stream writer on PDFsharp's object model (`D02 T13 §14`) | PDFsharp MIT | `SKDocument` (today's export, `D02 T04 §4`) cannot write spot colors, separations, OCG layers, or PDF/X output intents |
| PDF read | PdfPig with an own graphics-state interpreter (`D02 T14 §2`) | Apache-2.0 | Managed, and exposes raw content streams and resources |
| EPS and PostScript read | Illustrator-flavored EPS through the AI parser; general PostScript through a user-installed Ghostscript run as an external process, never bundled, refused by name when absent (`D02 T14 §9`) | Ghostscript is AGPL-3.0 | Bundling would pull AGPL terms into the installer; an optional external tool does not |
| DXF and DWG | ACadSharp (`D02 T14 §10`) | MIT | Reads and writes both, managed |
| DOCX, DOC, XLS, XLSX, PPTX, VSDX | DocumentFormat.OpenXml for OOXML, NPOI for binary DOC and XLS (`D02 T14 §14`, `D02 T10 §13`) | MIT, Apache-2.0 | Managed and permissive; binary PPT, PUB, VSD, and WPD go to the backlog (B-037) |
| Raster codecs | WIC through WPF's `BitmapDecoder` and `BitmapEncoder`; own TGA and PCX; own PSD reader and writer against Adobe's specification (`D02 T14 §12`, `§13`) | Part of Windows; own code | No dependency; HEIF and AVIF need the Windows Store extensions and are refused by name when absent |
| Text shaping | HarfBuzzSharp and SkiaSharp.HarfBuzz (`D02 T10 §1`) | MIT | The SkiaSharp family the suite already uses |
| Color management | lcms2 through a thin P/Invoke wrapper, native DLL per RID, WCS recorded as the alternative (`D01 T04 §1`) | MIT | ICC v4, proofing transforms, and black point compensation that WCS handles unevenly |
| Tracing | Port of the potrace algorithm plus own centerline tracing (`D02 T12 §4`, `§5`) | potrace GPL-2.0-or-later, compatible with GPL-3.0 | The reference outline tracer; the combined work stays GPL-3.0 |
| QR codes and barcodes | ZXing.Net (`D02 T16 §11`) | Apache-2.0 | Encode and decode (local validation) |
| Spell checking and thesaurus | Windows Spell Checking API; WordNet 3.1 data (`D02 T10 §13`) | Part of Windows; WordNet license (permissive) | No package for spelling; grammar checking is an AI feature (`D02 T15 §7`) |
| AI | OpenRouter over `HttpClient`, key protected with DPAPI (`System.Security.Cryptography.ProtectedData`) (`D01 T05`) | MIT (.NET) | No SDK; bring-your-own key |
| Color books, materials, content | Not bundled: no PANTONE or other licensed color books (users import ASE, ACB, or CPL books they own), no Adobe Substance materials, no Corel content packs | Proprietary | Redistribution is not licensed |

### AI: Nodus's own, built on three pillars

The Corel and Illustrator AI rows are mapped to the Nodus feature that does the same job; none is cloned. The runtime is OpenRouter with the user's own key (BYOK), model choice per task in settings, the key stored with DPAPI and never written to settings or logs, and nothing sent without an explicit user action and a send preview (`D01 T05 §1`, `§2`, `§4`).

- **Editable, structured output.** A generation asks the model for JSON validated against a schema (a scene of named layers, paths, document swatches, and styles) and applies it as one named undoable command that produces real vector objects; raster results are placed images with their source kept, never flattened into the drawing (`D02 T15 §2`, `§3`, `§4`, `§6`, `§8`, `§9`, `§10`).
- **Suite-aware.** The brand kit (named palettes, type styles, logo assets) lives in `Photon.Core` and is read by Nodus, Imago, and Lumen (`D01 T05 §5`, `D02 T15 §5`); the pipeline Lumen photo, Imago cleanup, Nodus trace runs over files, with hand-offs offered only when the other app is installed and refused by name otherwise (`D02 T15 §11`).
- **Explainable and reproducible.** Every AI action writes a provenance record (prompt, model, parameters, seed, input and output hashes, cost) into the document; the provenance panel re-runs, compares, and reverts (`D01 T05 §3`, `D02 T15 §1`).

Local algorithms that the inventories tag as AI stay local: LiveSketch stroke fitting and shape recognition (`D02 T08 §3`), GPU resampling (`D01 T03 §2`), and the classical parts of tracing (`D02 T12 §4`).

### Out of scope, and other apps

- **Automation** (`excluded: automation`): VBA, VSTA, JavaScript and ExtendScript scripts, the Scripts docker, macro recording, the Actions panel and Batch, plug-in SDKs (C++, CEP, UXP), and MCP or external AI-tool control. Illustrator Actions are excluded as recorded macros: the jobs they are used for are covered natively by Transform Again and Repeat (`D02 T08 §12`, `D02 T07 §13`), Step and Repeat (`D02 T08 §14`), graphic and object styles (`D02 T09 §15`), shortcut sets (`D02 T16 §3`), and the command palette, so a Nodus command recorder is not essential. Illustrator's Variables and data sets are data merge, not scripting, and are planned with Print Merge (`D02 T13 §13`).
- **Cloud and collaboration** (`excluded: cloud`): cloud documents, libraries, Share for Review, comments and markup, co-editing, SharePoint, WordPress export, Adobe Stock and Bridge, Adobe Fonts and Google remote fonts, Get More and content stores, CorelDRAW Web and Go, account services, and cloud-only learning content. Rows tagged `cloud` whose job is local stay planned (Insert QR Code with local validation, the working folder, local template and asset browsers).
- **Platform** (`excluded: platform`): the MacBook Pro Touch Bar.
- **Companion apps** (`other-app`): Corel PHOTO-PAINT features map to Imago, AfterShot to Lumen, and Corel Font Manager, CAPTURE, the application launcher, the Technical Suite, and bundled content to none.
- **Backlog** (`backlog`): obsolete formats (B-037 vector and document, B-038 raster), camera RAW import waiting for Lumen's shared decoder (B-039), 3D models embedded in PDF (B-040), and third-party filter plug-in hosts (B-012).

### The legacy roadmap file (D02 T06): relocated, not superseded

`D02 T06` holds eight born-complete sections that 0.1.0 code already points at: `PlannedCommands.cs` tooltips name `§2`, `§3`, `§13`, and `§14`, and the service triage (`D02 T02 §1`) defers services to `§11`, `§12`, and `§14`. Superseding them would break those owners. They stay at their addresses, the catalog marks their features `shipped-scope`, the parity sections extend them through `Depends On`, and the integration commit moves their plan rows from the old Phase 9 into the parity phases where their dependents need them:

| Section | Moves to | Why there |
| ------- | -------- | --------- |
| `D02 T06 §7` Documents in tabs, saved layouts, nested layers | Phase 4 | Pages, layers, and the Objects panel (`D02 T07 §3`, `§5`) build on per-document scopes and the layer tree |
| `D02 T06 §2` Path editing | Phase 5 | Node editing and the pen extensions (`D02 T08 §1`, `§6`) extend it |
| `D02 T06 §11` Symbols and the asset library | Phase 6 | Dynamic symbols and libraries (`D02 T09 §21`) extend it |
| `D02 T06 §3` Area text, text on a path, text to path | Phase 7 | The text engine (`D02 T10 §1`) builds on it |
| `D02 T06 §14` Placed images, more formats, the export dialog | Phase 9 | Bitmap objects (`D02 T12 §1`) need File, Place; Phase 11 formats extend it |
| `D02 T06 §12` Command palette and HUD | Phase 13 | Menu customization and command search (`D02 T16 §3`) extend it |
| `D02 T06 §13` Preferences and shortcut remapping | Phase 13 | The preference pages and workspaces (`D02 T16 §1` to `§5`) extend it |
| `D02 T06 §17` Accessibility and localization | Phase 13 | Audits every surface once the parity surfaces exist |

The old Phase 9 ("Nodus after 0.1.0") is then empty and leaves the plan with its ceiling; `D02 T06`'s Goal and Current state get one sentence recording the move, and `todo/02-nodus/INDEX.md` changes its phase line to "Phases 1, 2, 3, and 4 to 13".

### Backlog changes

Promoted into parity sections (each promoted entry is deleted from `todo/backlog.md` in the commit that authors its section, which is the integration commit when the batches land together, and its source key rides the section's `-> SOURCE:` line):

| Entry | Source key | Promoted into |
| ----- | ---------- | ------------- |
| B-001 Shape tools | `legacy-nodus-3.2` | `D02 T08 §4` |
| B-002 Clipping, masks, compound paths | `legacy-nodus-1.6-4.4` | `D02 T08 §11` |
| B-003 Appearance, swatches, conic gradients | `legacy-nodus-4.2-1.4` | `D02 T09 §3` |
| B-004 Artboards | `legacy-nodus-4.6` | `D02 T07 §3` |
| B-005 The contextual property bar | `legacy-nodus-2.5` | `D02 T07 §8` |
| B-006 Transform precision and smart selection | `legacy-nodus-3.1` | `D02 T08 §12` |
| B-007 Guides and measurement | `legacy-nodus-3.7-3.8` | `D02 T07 §10` |
| B-008 Freehand tools | `legacy-nodus-3.6` | `D02 T08 §3` |
| B-009 Large documents | `legacy-nodus-12.1` | `D02 T07 §2` |
| B-010 Brushes, patterns, color tools | `legacy-nodus-6` | `D02 T09 §16` |
| B-011 Print and prepress | `legacy-nodus-9` | `D02 T13 §2` |
| B-013 Onboarding and the navigator | `legacy-nodus-5.8-5.9` | `D02 T16 §7` |

Kept: **B-012** (Scripting and plugins) stays, reworded to third-party filter plug-in hosts only (8BF and Corel plug-in filters), since scripting is now excluded by operator decision; its catalog rows point at it.

Reworded: **B-023** (Imago color management) consumes `D01 T04` instead of choosing its own engine; **B-018** (Imago text layers) names `D02 T10 §1` as the shaping code that moves to `Photon.Core` when it is promoted.

New entries (ids taken in order; drafts in the entry grammar):

```
- [B-037] Legacy vector and document formats -- app: nodus -- source: parity-legacy-vector-formats -- added: 2026-09-26 -- summary: FreeHand FH, FXG, SWF export, Macintosh PICT, Micrografx PP4, Frame Vector Metafile, MET, NAP, GEM, Lotus PIC, Corel ArtShow CPX, Presentations SHW, R.A.V.E. CLK, Quattro Pro, Lotus 1-2-3, WordStar, Publisher PUB, binary Visio VSD, binary PowerPoint PPT, WordPerfect WPD, and legacy Corel DESIGNER files, each with a fidelity fixture when promoted -- needs: D02 T14 §11 -- why deferred: obsolete or single-vendor formats with no maintained producer; parity catalog rows point here instead of spending sections -- promote when: a user supplies a real file in one of these formats that Nodus must open
- [B-038] Legacy raster formats -- app: nodus -- source: parity-legacy-raster-formats -- added: 2026-09-26 -- summary: Kodak Photo CD, FlashPix, CALS, SCITEX CT, Wavelet WI, MacPaint, XPM, GEM Paint, Corel Painter RIF, Corel PHOTO-PAINT CPT, GIMP XCF, DCS separations, and icon resources inside EXE files -- needs: D02 T14 §12 -- why deferred: obsolete or niche raster formats; parity catalog rows point here -- promote when: a user supplies a real file in one of these formats, or Imago's codec work adds a reader Nodus can consume
- [B-039] Camera RAW import in Nodus -- app: nodus -- source: parity-nodus-raw-import -- added: 2026-09-26 -- summary: CorelDRAW's RAW Lab job in Nodus: open camera RAW files through Lumen's decoder once it moves to Photon.Core, with white balance, exposure, noise, and sharpness before placing -- needs: D04 T01 §4 -- why deferred: the decoder is Lumen's and moves to Photon.Core only when a second app needs it; Lumen runs after the parity phases -- promote when: Lumen's RAW decoder has shipped and moved to Photon.Core
- [B-040] 3D models embedded in PDF -- app: nodus -- source: parity-pdf-3d -- added: 2026-09-26 -- summary: U3D or PRC 3D annotations in exported PDF from 3D and Materials objects -- needs: D02 T13 §14 -- why deferred: a rarely used PDF feature with no open, maintained writer -- promote when: a user needs interactive 3D in PDF hand-off
```

Backlog count after the integration: 36 minus 12 promoted plus 4 new is 28, against the cap of 150.

## Phase layout and renumbering

The ten parity phases sit after Phase 3 (Nodus 0.1.0) and before the old Phase 4 (Imago foundation). Each ends with a Nodus release section in `D02 T17`. Within a phase, rows run in the order listed in the file designs below, with the relocated `D02 T06` rows first where they move in (except `D02 T06 §17`, the accessibility audit, which runs last in Phase 13 so it covers every parity surface), and the release row last.

| Phase | Rows in order |
| ---: | ----- |
| 4 | `D02 T06 §7`, `D02 T07 §1`, `D02 T07 §2`, `D02 T07 §3`, `D02 T07 §4`, `D02 T07 §5`, `D02 T07 §6`, `D02 T07 §7`, `D02 T07 §8`, `D02 T07 §9`, `D02 T07 §10`, `D02 T07 §11`, `D02 T07 §12`, `D02 T07 §13`, `D02 T07 §14`, `D02 T17 §1` |
| 5 | `D02 T06 §2`, `D02 T08 §1`, `D02 T08 §2`, `D02 T08 §3`, `D02 T08 §4`, `D02 T08 §5`, `D02 T08 §6`, `D02 T08 §7`, `D02 T08 §8`, `D02 T08 §9`, `D02 T08 §10`, `D02 T08 §11`, `D02 T08 §12`, `D02 T08 §13`, `D02 T08 §14`, `D02 T08 §15`, `D02 T17 §2` |
| 6 | `D02 T06 §11`, `D01 T04 §1`, `D01 T04 §2`, `D02 T09 §1`, `D02 T09 §2`, `D02 T09 §3`, `D02 T09 §4`, `D02 T09 §5`, `D02 T09 §6`, `D02 T09 §7`, `D02 T09 §8`, `D02 T09 §9`, `D02 T09 §10`, `D02 T09 §11`, `D02 T09 §12`, `D02 T09 §13`, `D02 T09 §14`, `D02 T09 §15`, `D02 T09 §16`, `D02 T09 §17`, `D02 T09 §18`, `D02 T09 §19`, `D02 T09 §20`, `D02 T09 §21`, `D02 T09 §22`, `D02 T17 §3` |
| 7 | `D02 T06 §3`, `D02 T10 §1`, `D02 T10 §2`, `D02 T10 §3`, `D02 T10 §4`, `D02 T10 §5`, `D02 T10 §6`, `D02 T10 §7`, `D02 T10 §8`, `D02 T10 §9`, `D02 T10 §10`, `D02 T10 §11`, `D02 T10 §12`, `D02 T10 §13`, `D02 T10 §14`, `D02 T10 §15`, `D02 T17 §4` |
| 8 | `D02 T11 §1`, `D02 T11 §2`, `D02 T11 §3`, `D02 T11 §4`, `D02 T11 §5`, `D02 T11 §6`, `D02 T11 §7`, `D02 T11 §8`, `D02 T11 §9`, `D02 T11 §10`, `D02 T11 §11`, `D02 T11 §12`, `D02 T11 §13`, `D02 T11 §14`, `D02 T11 §15`, `D02 T11 §16`, `D02 T11 §17`, `D02 T11 §18`, `D02 T11 §19`, `D02 T17 §5` |
| 9 | `D02 T06 §14`, `D01 T03 §1`, `D01 T03 §2`, `D01 T03 §3`, `D01 T03 §4`, `D01 T03 §5`, `D01 T03 §6`, `D01 T03 §7`, `D01 T03 §8`, `D01 T03 §9`, `D01 T03 §10`, `D01 T03 §11`, `D02 T12 §1`, `D02 T12 §2`, `D02 T12 §3`, `D02 T12 §4`, `D02 T12 §5`, `D02 T12 §6`, `D02 T12 §7`, `D02 T12 §8`, `D02 T17 §6` |
| 10 | `D01 T04 §3`, `D02 T13 §1`, `D02 T13 §2`, `D02 T13 §3`, `D02 T13 §4`, `D02 T13 §5`, `D02 T13 §6`, `D02 T13 §7`, `D02 T13 §8`, `D02 T13 §9`, `D02 T13 §10`, `D02 T13 §11`, `D02 T13 §12`, `D02 T13 §13`, `D02 T13 §14`, `D02 T13 §15`, `D02 T13 §16`, `D02 T17 §7` |
| 11 | `D02 T14 §1`, `D02 T14 §2`, `D02 T14 §3`, `D02 T14 §4`, `D02 T14 §5`, `D02 T14 §6`, `D02 T14 §7`, `D02 T14 §8`, `D02 T14 §9`, `D02 T14 §10`, `D02 T14 §11`, `D02 T14 §12`, `D02 T14 §13`, `D02 T14 §14`, `D02 T14 §15`, `D02 T14 §16`, `D02 T14 §17`, `D02 T14 §18`, `D02 T14 §19`, `D02 T17 §8` |
| 12 | `D01 T05 §1`, `D01 T05 §2`, `D01 T05 §3`, `D01 T05 §4`, `D01 T05 §5`, `D02 T15 §1`, `D02 T15 §2`, `D02 T15 §3`, `D02 T15 §4`, `D02 T15 §5`, `D02 T15 §6`, `D02 T15 §7`, `D02 T15 §8`, `D02 T15 §9`, `D02 T15 §10`, `D02 T15 §11`, `D02 T17 §9` |
| 13 | `D02 T06 §12`, `D02 T06 §13`, `D02 T16 §1`, `D02 T16 §2`, `D02 T16 §3`, `D02 T16 §4`, `D02 T16 §5`, `D02 T16 §6`, `D02 T16 §7`, `D02 T16 §8`, `D02 T16 §9`, `D02 T16 §10`, `D02 T16 §11`, `D02 T06 §17`, `D02 T17 §10` |

**Renumbering of the existing phases:**

| Old | New | Title |
| --- | --- | ----- |
| 0 to 3 | 0 to 3 | unchanged |
| -- | 4 to 13 | the parity phases above |
| 4 | 14 | Imago foundation: snapshot port, WPF-UI out, tiles, rendering |
| 5 | 15 | Imago 0.1.0: editing, files, filters, release |
| 6 | 16 | Lumen foundation: spine, catalog, import, RAW, library |
| 7 | 17 | Lumen 0.1.0: develop, export, Edit in Imago, release |
| 8 | 18 | Distribution and the suite bundle |
| 9 | removed | Nodus after 0.1.0: its eight rows move into Phases 4, 5, 6, 7, 9, and 13 |
| 10 | 19 | Imago after 0.1.0: deferral owners and accessibility |
| 11 | 20 | Lumen after 0.1.0: accessibility |
| 99 | 99 | Manual: operator-only steps |

Prose that names an old phase number (`todo/implementation-plan.md` headings and paragraphs, the domain `INDEX.md` phase lines, `todo/TODO-00-INDEX.md`) is updated in the same commit; no section ref changes.

**Budget.** Each new phase's ceiling is its section count (new sections plus relocated rows) plus 10 percent rounded up, minimum one, the rule of the initial budget:

| Phase | Sections | Ceiling |
| ---: | ---: | ---: |
| 4 | 16 | 18 |
| 5 | 17 | 19 |
| 6 | 26 | 29 |
| 7 | 17 | 19 |
| 8 | 20 | 22 |
| 9 | 21 | 24 |
| 10 | 18 | 20 |
| 11 | 20 | 22 |
| 12 | 17 | 19 |
| 13 | 15 | 17 |
| **Sum** | **187** | **209** |

The emptied old Phase 9 gives back its ceiling of 9, so the net raise is 209 minus 9, which is 200; the total ceiling goes from 154 to 354.

The integration commit appends one history entry (the live values and the snapshot identical):

```json
{
  "date": "2026-09-26",
  "change": "Nodus parity: ten new phases (4 to 13) for the Illustrator and CorelDRAW parity catalog, ceilings at each phase's section count plus 10 percent rounded up with a minimum of one (209 in all); the old Phase 9 (Nodus after 0.1.0) leaves the plan with its ceiling of 9 after its eight D02 T06 rows move into the parity phases; old Phases 4 to 8 become 14 to 18, old 10 and 11 become 19 and 20. Net raise 200, total ceiling 354.",
  "reason": "Operator decision 2026-09-26: \"For Nodus, we need to add all(and I mean), all CorelDraw features and All Illustrator Features.\" Budget raise approved in the operator's words: \"New parity phases, up to +200\".",
  "approved_by": "operator",
  "snapshot": {
    "ceilings": {
      "0": 15,
      "1": 4,
      "2": 18,
      "3": 27,
      "4": 18,
      "5": 19,
      "6": 29,
      "7": 19,
      "8": 22,
      "9": 24,
      "10": 20,
      "11": 22,
      "12": 19,
      "13": 17,
      "14": 10,
      "15": 26,
      "16": 10,
      "17": 13,
      "18": 9,
      "19": 5,
      "20": 2,
      "99": 6
    },
    "backlog_cap": 150,
    "per_run_new_sections": 3
  }
}
```

## Acceptance bar additions

New rows for "The acceptance bar" in `todo/implementation-plan.md`:

| Aim | Owned by |
| --- | -------- |
| Nodus covers every CorelDRAW and Illustrator capability in the parity catalog | `D00 T01 §6` (the catalog gate) · `D02 T17 §1`-`§10` (each release reconciles its phase) |
| Nodus opens and saves Illustrator and CorelDRAW files | `D02 T14 §3` · `D02 T14 §4` · `D02 T14 §5` · `D02 T14 §6` · `D02 T14 §7` · `D02 T14 §8` |
| Print and PDF output are prepress-grade | `D02 T13 §5` · `D02 T13 §7` · `D02 T13 §14` · `D02 T13 §15` |
| AI results are editable, undoable, and reproducible | `D01 T05 §3` · `D02 T15 §1` · `D02 T15 §2` · `D02 T15 §6` |
| Nothing leaves the machine without an explicit user action | `D01 T05 §2` · `D01 T05 §4` |

Existing rows gain owners: "Shared once, never copied" adds `D01 T03 §1` · `D01 T04 §1` · `D01 T05 §1`; "Formats are proven, not assumed" adds `D02 T14 §2` · `D02 T14 §6` · `D02 T14 §12`; "No dependency without a reason and a license" adds `D01 T04 §1` · `D02 T10 §1` · `D02 T13 §14` · `D02 T14 §2` · `D02 T14 §6` · `D02 T14 §10`.

## Authoring batches

Five disjoint file sets of roughly equal size, so five agents can author in parallel. Each batch writes only its own files; every `-> XREF:` it writes into another batch's file, or into an existing file, is listed in its report, and the integration commit adds the reciprocal lines, the index rows, the plan rows, the budget entry, the backlog changes, and the `D02 T06` relocation in one pass.

| Batch | Files | Sections | Subject |
| :---: | ----- | ---: | ------- |
| A | `TODO-07-nodus-parity-document.md`, `TODO-08-nodus-parity-paths.md`, `TODO-17-nodus-parity-releases.md`, `D00 T01 §6` | 40 | document model, drawing and paths, the releases, and the catalog validator |
| B | `TODO-09-nodus-parity-color.md`, `TODO-04-photon-color-management.md`, `TODO-16-nodus-parity-workspace.md` | 36 | color, fills, strokes, brushes, styles, symbols, the color engine, and the workspace |
| C | `TODO-10-nodus-parity-type.md`, `TODO-11-nodus-parity-effects.md` | 34 | type, tables, graphs, and live effects |
| D | `TODO-03-photon-pixel-engine.md`, `TODO-12-nodus-parity-bitmaps.md`, `TODO-13-nodus-parity-print.md` | 35 | the pixel engine, bitmaps and tracing, print, prepress, and PDF |
| E | `TODO-14-nodus-parity-formats.md`, `TODO-05-photon-ai.md`, `TODO-15-nodus-ai.md` | 35 | file formats, the AI core, and Nodus AI |

## Integration commit checklist

- Author or collect the 14 new files and the new `D00 T01 §6`; list each file in its domain `INDEX.md` and in `todo/TODO-00-INDEX.md`.
- Add the ten parity phases to `todo/implementation-plan.md` (heading, one paragraph, one table each, from "Phase paragraphs" below), move the eight `D02 T06` rows, delete the empty old Phase 9, renumber the later phases, and add the acceptance-bar rows.
- Append the budget history entry and update the live ceilings; delete the twelve promoted backlog entries, reword B-012, B-018, and B-023, and add B-037 to B-040.
- Reciprocate every cross-file `-> XREF:`; update `D02 T06`'s Goal and Current state for the relocation; add `D03 T05 §1`'s XREF to `D01 T03 §1`.
- Run `python scripts/todo-graph.py validate`, `plan --sync`, `plan --check`, `query budget`, and `python scripts/todo-claims.py`; all clean.

## Phase paragraphs

### Phase 4 -- Nodus parity I: document model, pages, layers, selection, and view

Parity starts where every later feature stands. This phase fixes how live objects persist in SVG (the `nodus:` namespace with an expanded fallback), gives the canvas a spatial index so documents with thousands of objects stay interactive, unifies CorelDRAW pages and Illustrator artboards into one model with its panel, and completes layers and the Objects panel, selection, isolation and focus mode, the Properties panel and property bar, rulers, guides, grids, snapping, view modes, history, and the New Document dialog with templates. Tabs and nested layers (`D02 T06 §7`) move here first because pages and layers build on them. It ends with `nodus-v0.2.0`.

### Phase 5 -- Nodus parity II: drawing, paths, shapes, shaping, and transform

With the document model settled, the drawing layer catches up: every pen, curve, freehand, and smart-drawing tool, live shapes with editable parameters and live corners, full node editing, cutting and erasing, liquify and shape-editing brushes, Pathfinder and the shape builder, compound paths and clipping masks, precise transforms and Transform Each, align and distribute extensions, and dimensions and connectors. Path editing (`D02 T06 §2`) moves here first because node editing extends it. It ends with `nodus-v0.3.0`.

### Phase 6 -- Nodus parity III: color, fills, strokes, brushes, transparency, styles, and symbols

Appearance comes next because every effect and every format carries it. `Photon.Core` gains its color-management engine first, then Nodus gets the full color model (CMYK, Lab, spot, global), the color panel and pickers, swatches and palettes, color styles and harmonies, Recolor Artwork, every gradient kind including mesh, pattern and texture fills, complete strokes with arrowheads and variable width, the Appearance stack, graphic and object styles, the brush engine with every brush kind, every blend and merge mode with opacity masks, and symbols with overrides and libraries (after `D02 T06 §11`). It ends with `nodus-v0.4.0`.

### Phase 7 -- Nodus parity IV: type, tables, and graphs

Type is its own discipline, so it gets its own phase: HarfBuzz shaping with bidirectional and CJK support, the rich text model, fonts and substitution, character, OpenType, and paragraph formatting, frames, threading and wrap, type on a path, text commands, styles, writing tools and text import, then tables and graphs, which are built from text and appearance. Area text and text on a path (`D02 T06 §3`) move here first. It ends with `nodus-v0.5.0`.

### Phase 8 -- Nodus parity V: interactive and live effects

Effects sit on the Appearance stack and the live-object contract, both shipped by now. This phase builds the effect framework and then every interactive effect both competitors ship: blend, contour, envelope and warp, distort, shadows and glows and bevels, 3D extrude and 3D and Materials, lenses, PowerClip, symmetry, the perspective grid and perspective objects, puppet warp, Live Paint, repeats and objects on a path, and path effects. It ends with `nodus-v0.6.0`.

### Phase 9 -- Nodus parity VI: bitmaps, tracing, and the shared pixel engine

Bitmaps arrive once vectors are complete. `Photon.Core` gains the pixel engine the operator placed there for the whole suite (buffers, resampling, dithering, adjustments, and every bitmap effect family), and Nodus gets bitmap objects, the non-destructive effect stack, the adjustment lab, tracing (Image Trace and PowerTRACE), photo-based artwork, the Links panel, and SVG filters. Placing images (`D02 T06 §14`) moves here first because bitmap objects need it. It ends with `nodus-v0.7.0`.

### Phase 10 -- Nodus parity VII: color management, print, prepress, and PDF

Output comes after everything it has to print exists. Bitmap color modes finish the color engine, then Nodus gets document color settings, the print dialog, marks and bleed, separations, soft proofing, overprint and trapping, flattening, preflight and packaging, PostScript options, imposition and layout styles, print merge with variable data, and its own PDF writer with PDF/X presets and interactivity. It ends with `nodus-v0.8.0`.

### Phase 11 -- Nodus parity VIII: file formats, export, and web

Formats come after the object model they must carry is complete, so each reader and writer maps onto real Nodus objects and owes a fidelity proof: SVG options, PDF import, Illustrator `.ai` import and export, CorelDRAW `.cdr` import and export, EPS, DXF and DWG, metafiles, raster formats, PSD, office documents, Export for Screens and the export list, Export for Web, slices and hyperlinks, pixel-perfect drawing, and clipboard and OLE exchange. It ends with `nodus-v0.9.0`.

### Phase 12 -- Nodus AI: editable, suite-aware, reproducible

The AI features are Nodus's own and come after the object model, formats, and tracing they produce and consume. `Photon.Core` and `Photon.UI` gain the shared AI core (OpenRouter with the user's own key, DPAPI key storage, the explicit-send gate, provenance, and the brand kit), then Nodus maps every competitor AI job to an editable, undoable, reproducible feature: vector generation, patterns and fills, expand and bleed, recolor, the assistant, text rewriting and retyping, image generation and cleanup, concept to vector, and the suite pipeline. It ends with `nodus-v0.10.0`.

### Phase 13 -- Nodus parity IX: workspace, customization, preferences, and Nodus 1.0.0

The last parity phase customizes and audits the whole surface once it exists: the command palette and Preferences (`D02 T06 §12`, `§13`) move here, then workspaces, toolbars, menus and shortcut sets, the preference pages, UI appearance and diagnostics, the welcome screen and navigator, pen and touch input, hints and the project timer, object data and find and replace, QR codes and barcodes, and the accessibility and localization audit (`D02 T06 §17`) over every parity surface. It ends with `nodus-v1.0.0`, which declares the parity catalog complete.

## Integration notes from the design pass

Findings the per-file design agents reported that cross file boundaries; the integration commit resolves each.

- **Color picker ownership.** `D03 T03 §8`'s Chrome line says Imago builds the picker and it moves to `Photon.UI` when Nodus's B-003 work is promoted. This plan reverses that: `D02 T09 §2` builds the picker in Nodus and it moves to `Photon.UI` the day `D03 T03 §8` needs it. Rewrite `D03 T03 §8`'s Chrome line to match.
- **Root `<metadata>`.** Today's `SvgParser.cs` skips the root `<metadata>` element; `D02 T07 §1` puts the `nodus:document` block there and must preserve it, and `D02 T15 §1` embeds AI provenance in it.
- **B-023 claim.** A `D01 T04` Current-state claim quotes B-023's wording; reword B-023 and that claim in the same commit.
- **Controls deferred by name to later phases** (legitimate, each names its owner): `D02 T12 §1`'s Lab, CMYK, and duotone mode commands wait for `D01 T04 §3`; `D02 T13 §3`'s PostScript print-to-file and `§5`'s in-RIP separations wait for `D02 T13 §10`, and overprint flags for `§7`; `D02 T09 §21`'s `.csl` library files wait for `D02 T14 §6` and `§8`; `D02 T12 §7`'s linked CDR, XLS, and EPS sources wait for `D02 T14 §6`, `§9`, and `§14`; `D02 T09 §6` and `§12` build the color and outline replace services that `D02 T16 §10`'s Find and Replace docker consumes; `D02 T10 §13` builds the DOCX, RTF, and DOC text readers that `D02 T14 §14` reuses.
- **Dependencies sharpened after the design pass:** `D02 T09 §20` also depends on `§10` and `§11` (pattern and texture transparency reuse them); `D02 T14 §2` also depends on `D02 T06 §14` (it registers its reader in the import table `D02 T06 §14` wires).
- **Sizing watch list.** These sections carry the most features and are the likeliest to pass 30 checklist items; each design block's "Sizing concerns" names its natural split. A split spends the phase's spare ceiling (every parity phase keeps 2 or 3 slots of room from its +10 percent), never a raise: `D02 T07 §5`, `§6`, `§11`, `§12`; `D02 T08 §4` (the Coordinates panel), `§6`, `§10`; `D02 T09 §4`, `§5`, `§15`, `§18`; `D02 T10 §3`, `§5`, `§8`, `§14`; `D02 T11 §5`, `§7`, `§10`; `D01 T03 §6`, `§8`, `§10`; `D02 T12 §1`, `§5`; `D02 T13 §7`, `§13`, `§15`; `D02 T14 §12`, `§15`, `§17`, `§19`; `D02 T16 §2`, `§4`.
- **Catalog duplicates across bundles.** Merging ran per file, so a capability owned partly by an existing section and partly by a parity section (for example the basic align commands of `D02 T02 §4` and the align extensions of `D02 T08 §14`) appears as two rows with two statuses. That is intended: each row names the section that owns its part.

## Catalog check

`python check_catalog.py` (the scratch check, run 2026-09-26, the rules `D00 T01 §6` turns into validator classes):

- Source ids: 1,294 Illustrator (`AI-0001` to `AI-1294`), 3,041 CorelDRAW (`CD-001` to `CD-3041`), 4,335 in all.
- Catalog rows: 2,802 (`NP-0001` to `NP-2802`), ids unique and sequential.
- Source ids placed: 4,335 exactly once; missing 0; duplicated 0; unknown 0.
- Statuses: plan 2,643; shipped-scope 69; backlog 37; excluded 35; other-app 18; malformed 0.
- Every `plan` ref names a designed section and every `shipped-scope` ref an existing one; designed sections with no catalog row of their own: `D01 T05 §2`, `D01 T05 §3`, `D01 T05 §5` (infrastructure the planned features build on), plus the release sections and `D00 T01 §6`.
- Result: clean.

## File designs

### todo/00-workspace/TODO-01-dev-automation.md -- one new section in an existing file

- **Phase(s):** 0 (the workspace spine; Phase 0 holds 13 sections against a ceiling of 15, so this needs no raise)
- **Why here:** the catalog is plan data like `todo/`, and the acceptance-bar aim "Nodus covers every CorelDRAW and Illustrator capability in the parity catalog" needs a gate before the first parity row runs, so the check joins `validate` beside the budget and backlog checks.

#### §6. The parity catalog validator

- **Deliverable:** `validate` refuses a parity catalog that has drifted from its sources or from the plan, and `query parity` reports per-phase coverage
- **Depends On:** §1
- **Phase:** 0
- **Surface:** no surface of its own
- **Runs:** none
- **Catalog:** owns no catalog rows (it enforces them)
- **Hints:**
  - Add `scripts/todo-parity.py` (stdlib only, like the other TODO tooling): parse every `| AI-#### |` row of `docs/parity/sources/illustrator-30.8.md`, every `| CD-### |` row of `docs/parity/sources/coreldraw-2026.md`, and every `| NP-#### |` row of `docs/parity/nodus-parity.md`.
  - Checks, each a named class: `parity-id-missing` (a source id in no catalog row), `parity-id-duplicate` (a source id in two rows), `parity-id-unknown` (a catalog id no source defines), `parity-np-duplicate` (an `NP-` id used twice), `parity-status-malformed` (a status outside the grammar in `docs/parity/README.md`), `parity-ref-dead` (a `plan` or `shipped-scope` ref that `resolve` cannot find, or that names a Moved section), `parity-backlog-dead` (a `backlog B-NNN` id with no live entry in `todo/backlog.md`).
  - Wire it into `python scripts/todo-graph.py validate` as FATAL classes and add their rows to the per-class table in `todo/README.md` and to `SEVERITY_MAP`, so `self-test` keeps the two in step.
  - Add `python scripts/todo-graph.py query parity [--phase N] [--json]`: per phase, the catalog rows planned to its sections and how many of those sections are stamped; per status kind, the totals. The release sections `D02 T17 §1` to `§10` quote it.
  - Add self-test cases over a tiny fixture catalog: one missing id, one duplicate, one dead ref, one malformed status, one clean catalog.
  - The check runs wherever `validate` runs (commit hook, CI, `scripts/check-all.ps1`); no new CI job.
  - Commit: `"workspace: validate the Nodus parity catalog against its sources and the plan"`.
- **Proof:** unit plus static: `python scripts/todo-graph.py self-test` passes with the new cases; deleting one id from a copy of the catalog makes `validate` exit 1 naming `parity-id-missing`; cheaper substitute that fails: a one-off script outside `validate` that CI never runs.

### todo/01-core/TODO-03-photon-pixel-engine.md -- `photon-pixel-engine`

- **Title:** "TODO-03 -- Photon.Core Pixel Engine: Buffers, Resampling, Adjustments, and Bitmap Effects"
- **Phase(s):** 9
- **Goal:** `Photon.Core/Imaging/` holds one deterministic, golden-tested pixel engine in pure managed C# with `System.Numerics.Vector<T>` SIMD: tiled RGBA8, RGBA16, and float buffers with premultiplied alpha, one effect contract (parameter schema, seed, preview at scale, progress, cancellation, serializable description), resampling and geometric correction, palette quantization and dithering, the tonal and color adjustments, and every bitmap effect family both competitors ship (blur, sharpen, noise, distort, artistic, brush-stroke, sketch, texture, creative, camera, color-transform, edge, custom, pixelate, video); it lives in Photon.Core by operator decision (2026-09-26) although Nodus (`D02 T12`) is its first consumer, and Imago's filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered) is its planned second consumer, so nothing in it references WPF, SkiaSharp views, or a Nodus type.
- **Current-state facts to verify (with claim candidates):**
  - There is no `Photon.Core` project yet; `D01 T02 §1` creates it, and this file adds the `Imaging/` folder to it. `<!-- claim: absent src/Photon.Core -->`
  - Imago already tiles its raster layers at 256 by 256 RGBA8, the tile size the engine adopts so the second consumer needs no re-tiling. `<!-- claim: count "TileSize = 256" src/Imago/src/Imago.Core/Tiles/Tile.cs = 1 -->`
  - Imago's filter commands are logging stubs that the second consumer will route through this engine. `<!-- claim: exists src/Imago/src/Imago.Plugins.Abstractions/IFilterPlugin.cs -->`
  - Nodus's bitmap element holds encoded bytes only (`EmbeddedData`, `MimeType`) with no decoded pixel access. `<!-- claim: lines src/Nodus/Bezier.Core/Models/Elements/SvgImage.cs = 120 -->`
  - Nodus's renderer draws no bitmap element today. `<!-- claim: count "SvgImage" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->`
  - There is no decisions log yet; the first section that adds a package or a reference implementation creates `docs/dev/decisions.md`. `<!-- claim: absent docs/dev/decisions.md -->`
- **Inputs and XREFs:** `standards/shared.md` (logging, settings, determinism); `docs/dev/architecture.md` (what lives in Photon.Core); GIMP 3.0, libvips 8.16, and ImageMagick 7.1 as golden reference implementations (exact versions recorded beside each fixture); -> XREF: D01 T02 §1 (the Photon.Core project this extends); -> XREF: D01 T02 §2 (settings store for engine defaults such as tile cache size); -> XREF: D01 T04 §3 (Lab, CMYK, and duotone bitmap modes that convert through the color engine and hand RGBA buffers to this one); -> XREF: D02 T12 §1, D02 T12 §2, D02 T12 §3, D02 T12 §4 (the Nodus consumers); -> XREF: D03 T05 §1 (Imago's filter pipeline, the planned second consumer, Phase 5 of the old plan, later renumbered).
- **Adjacency:** list=not-applicable (an engine has no browsable records; the effect registry is listed by the Nodus Effects menu in D02 T12 §2); document=not-applicable (no printed output of its own); settings=applicable @ D01 T02 §2; reporting=applicable (histogram computation in §4 and effect timing in the log); notifications=applicable (progress and cancellation through `IProgress<EffectProgress>` and `CancellationToken`, shown by the consumers); permissions=not-applicable (the engine reads and writes no files; loaded texture and displacement maps arrive as buffers from the app); audit=applicable (one Serilog Information line per effect run with id, parameters hash, size, and milliseconds); exchange=applicable (effect descriptions serialize to JSON for the consumers' `nodus:` namespace and presets; Corel `.pst` curve presets read in §4); reverse=not-applicable (effects are pure functions from buffer to buffer; undo belongs to the consumers' history, D01 T02 §4)

#### §1. Pixel buffers, the effect contract, and the golden harness

- **Deliverable:** `Photon.Core/Imaging/` buffers (RGBA8, RGBA16, float, premultiplied, 256-pixel tiles), the `IPixelEffect` contract with its registry and JSON description, bitmap inflation, and the golden-image harness every later section tests through
- **Depends On:** D01 T02 §1
- **Phase:** 9
- **Surface:** no surface of its own (the Nodus effect surfaces are D02 T12 §2 and D02 T12 §3)
- **Runs:** none
- **Catalog:** NP-1824 to NP-1826 (3 features)
- **Hints:**
  - `src/Photon.Core/Imaging/PixelBuffer.cs`: `PixelBuffer<TPixel>` over `Rgba8`, `Rgba16`, and `RgbaF` structs, premultiplied by default with explicit `Premultiply()`/`Unpremultiply()`, width, height, stride, and `Span<TPixel>` row access; no SkiaSharp or WPF type in the public API.
  - `TiledPixelBuffer` with 256 by 256 tiles (Imago's `Tile.TileSize`) and a bounded tile cache whose size is the setting `Photon.Imaging.TileCacheMegabytes` (default 512, read by the cache); budget: a 100-megapixel RGBA8 bitmap processes through a per-pixel effect without allocating a second full-size buffer.
  - `IPixelEffect` in `Imaging/Effects/`: `Id`, `Category`, `EffectParameterSchema` (typed ranges, defaults, units), `Apply(source, destination, parameters, EffectContext)` where `EffectContext` carries `Seed`, `PreviewScale`, `IProgress<EffectProgress>`, and `CancellationToken`; effects slower than one second must observe cancellation at tile granularity.
  - `EffectRegistry` discovers effects by attribute and exposes categories for the consumers' menus; `EffectDescription` (id, version, parameters, seed) serializes with `System.Text.Json` and round-trips byte-identical.
  - `ExpandBounds(Rect)` on the contract: effects that grow bounds (blur, glow, wind) report their margin, and `BitmapInflation.Inflate(buffer, pixels | percent, keepAspect)` implements manual inflation (CD-2109) and auto inflation (CD-2110); the document-level default (CD-2111) is read by the consumer, not stored here.
  - `ColorModeAdapter.ToRgba(buffer, sourceMode)` for RGB-only effects on grayscale, paletted, and 1-bit sources (CD-2108), returning a flag so the consumer can say the mode changed; Lab and CMYK sources arrive through `D01 T04 §3`.
  - SIMD path with `System.Numerics.Vector<T>` plus a scalar reference path in the same class; a test asserts both paths agree bit-exactly on random buffers.
  - Golden harness `tests/Photon.Core.Tests/Imaging/GoldenHarness.cs`: loads `tests/fixtures/imaging/<effect>/input.png`, runs the effect, compares with `expected.png` by max and mean channel delta within a per-effect tolerance, writes a diff image on failure; each fixture folder has `reference.txt` naming the reference implementation, its version, and the exact command.
  - Property-test helpers for effects with no reference: output bounds equal `ExpandBounds`, same seed gives identical bytes, a fully transparent input stays transparent, alpha is preserved where the effect claims it.
  - One Serilog Information line per `Apply` (effect id, parameter hash, pixel count, elapsed milliseconds); record the engine decision (managed C#, SIMD, no native imaging dependency) as a row in `docs/dev/decisions.md`.
  - Second consumer: Imago's filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered) wraps `IPixelEffect` for its layers; add the reciprocal XREF in `todo/03-imago/TODO-05-imago-adjustments.md`.
- **Proof:** unit proof in `tests/Photon.Core.Tests/Imaging/PixelBufferTests.cs` and `EffectContractTests.cs` (SIMD equals scalar, description round-trip, cancellation within one tile, inflation sizes) plus a 100-megapixel budget test with a measured allocation ceiling; cheaper substitute that fails: a single flat `byte[]` buffer with no cancellation and a straight-alpha contract.

#### §2. Resampling, rotation, straighten, perspective, and lens correction

- **Deliverable:** Resamplers (nearest, bilinear, bicubic, Lanczos-3) with resolution and aspect options, arbitrary rotation with crop to the rotated rectangle, perspective correction, and barrel and pincushion correction, each golden-tested against libvips
- **Depends On:** §1
- **Phase:** 9
- **Surface:** no surface of its own (the Resample and Straighten dialogs are D02 T12 §1)
- **Runs:** none
- **Catalog:** NP-1727 to NP-1733 (7 features)
- **Hints:**
  - `Imaging/Geometry/Resampler.cs` with `ResampleMode { NearestNeighbor, Bilinear, Bicubic, Lanczos3 }` using separable kernels on premultiplied float rows; goldens from libvips `vips resize` with the kernel named per fixture (nearest and bicubic are the two Corel modes, CD-1972, CD-1973).
  - `ResampleRequest` (pixel width and height, or physical size plus horizontal and vertical dpi, `MaintainAspect`, `MaintainFileSize`) with a pure `Resolve()` that returns target pixels and dpi (CD-1977, CD-1978, CD-1979); tests cover the three option combinations.
  - GPU resampling decision (CD-1980): record in `docs/dev/decisions.md` that the managed SIMD path is the only resampler and that a GPU path is not built, with the measured time for a 24-megapixel Lanczos resample as the evidence; AI upsampling stays with `D02 T15 §9`.
  - `Imaging/Geometry/Rotator.cs`: rotate by any angle with bicubic sampling and `CropToRotatedRect(angle, keepAspect)` returning the largest axis-aligned rectangle, for the straighten dialog.
  - `Imaging/Geometry/PerspectiveCorrector.cs`: vertical and horizontal keystone correction from two angles and a four-point homography variant (CD-1986, CD-2075's engine).
  - `Imaging/Geometry/LensCorrector.cs`: radial distortion `r' = r(1 + k1 r^2 + k2 r^4)` with a single user amount mapped to `k1` (CD-1982); golden against ImageMagick `-distort Barrel`.
  - Cancellation and progress for every operation on buffers over 16 megapixels; a 100-megapixel Lanczos downsample stays under the §1 memory ceiling.
  - Second consumer: Imago's Image Size and rotate canvas commands through `D03 T05 §1` (Phase 5 of the old plan, later renumbered) reuse `Resampler` and `Rotator`.
- **Proof:** golden proof in `tests/Photon.Core.Tests/Imaging/Geometry/` against libvips 8.16 and ImageMagick 7.1 fixtures in `tests/fixtures/imaging/resample/`, `rotate/`, `perspective/`, `lens/` with stated tolerances (max delta 2 of 255 for bicubic); cheaper substitute that fails: delegating to `SKBitmap.Resize`, which gives no Lanczos mode and no reference match.

#### §3. Palette quantization and dithering

- **Deliverable:** 1-bit conversions (threshold, ordered, halftone, cardinality-distribution, Jarvis, Stucki, Floyd-Steinberg), 8-bit paletted conversion with seven palette types, dithering intensity, range sensitivity, editable processed palettes and presets, the color reduction tracing and web export reuse, and posterize
- **Depends On:** §1
- **Phase:** 9
- **Surface:** no surface of its own (the Black and White and Paletted dialogs are D02 T12 §1)
- **Runs:** none
- **Catalog:** NP-1734 to NP-1752 (19 features)
- **Hints:**
  - `Imaging/Quantize/BilevelConverter.cs` with `BilevelMethod { LineArt, Ordered, Halftone, CardinalityDistribution, Jarvis, Stucki, FloydSteinberg }` and `Intensity` (threshold or bias); halftone takes screen type (round, line, square, cross, ellipse), angle, and lines per inch.
  - One `ErrorDiffuser` class driven by kernel tables (Floyd-Steinberg, Jarvis-Judice-Ninke, Stucki) with serpentine scanning; goldens from ImageMagick `-dither FloydSteinberg` and GIMP 3.0 indexed conversion where the kernel matches, property tests for Jarvis and Stucki.
  - `OrderedDither` with 2x2 to 8x8 Bayer matrices; `CardinalityDistribution` implemented as blue-noise threshold (documented as Nodus's reading of the Corel option) with a committed snapshot golden.
  - `Imaging/Quantize/PaletteBuilder.cs`: `Uniform` (6x7x6 levels), `StandardVga` (fixed 16), `Adaptive` (median cut), `Optimized` (octree over frequency with `RangeSensitivity` focus color and weight), `Grayscale` (256), `System` (the Windows 20-color table), `Custom` (user list or a palette file parsed by the consumer).
  - `PalettedConverter.Convert(buffer, palette, DitherMethod, intensity)` returning an `IndexedBuffer` with an editable `Palette` (processed palette, CD-2019); `QuantizePreset` JSON (palette type, colors, dither, intensity, sensitivity) for save and load (CD-2018).
  - `ColorReducer.Reduce(buffer, maxColors, seed)` as the public entry point `D02 T12 §4` tracing and web export call; deterministic for a seed.
  - `Posterize` effect (levels per channel 2 to 32) registered in the `EffectRegistry`, golden against GIMP 3.0 posterize.
  - Budget: optimized palette of 256 colors on a 24-megapixel image under 2 seconds on the reference machine, cancellable.
  - Second consumer: Imago's Indexed mode and posterize through `D03 T05 §1` (Phase 5 of the old plan, later renumbered).
- **Proof:** golden proof in `tests/Photon.Core.Tests/Imaging/Quantize/` against ImageMagick 7.1 and GIMP 3.0 fixtures in `tests/fixtures/imaging/quantize/`, plus property tests (palette size bound, every output index valid, same seed identical); cheaper substitute that fails: nearest-color mapping with no diffusion, which the Floyd-Steinberg golden rejects.

#### §4. Tonal adjustments

- **Deliverable:** Histogram computation, auto adjust, levels, equalize, sample and target, tone curves with four styles and channel tools, light (brightness, contrast, intensity, highlights, shadows, midtones), gamma, exposure, temperature and tint, and white balance, each a registered adjustment with reference goldens
- **Depends On:** §1
- **Phase:** 9
- **Surface:** no surface of its own (the Nodus adjustment dialogs and Image Adjustment Lab are D02 T12 §3)
- **Runs:** none
- **Catalog:** NP-1827 to NP-1835 (9 features)
- **Hints:**
  - `Imaging/Adjust/Histogram.cs`: per-channel and luminance 256-bin (and 65,536-bin for 16-bit) histograms computed tile-parallel, with percentile queries used by auto adjust and levels.
  - `Levels` (input black, gamma, input white, output black and white per channel) and `AutoAdjust` (clip 0.1 percent per channel, neutralize midtone); goldens from GIMP 3.0 `gimp-drawable-levels` and auto stretch.
  - `Equalize` with the Corel histogram models (flat, normal, and custom target) documented as parameters.
  - `SampleAndTarget`: sampled shadow, midtone, highlight colors mapped to targets per channel, built on the levels lookup.
  - `ToneCurve` with `CurveStyle { Curve, Straight, Freehand, Gamma }` evaluated through monotone cubic splines into 256 and 65,536 entry lookups; `Smooth()`, `Mirror()`, `Reset(channel | all)` on the curve model (CD-2277); a read-only parser for Corel `.pst` curve presets with a committed sample fixture.
  - `Light` (brightness, contrast, intensity, highlights, shadows, midtones), `Gamma`, `Exposure`, `TemperatureTint` (Kelvin shift in linear light), and `WhiteBalance` (auto gray-world or sampled neutral).
  - Every adjustment is a pure lookup or 3x3 matrix when possible, fused per pixel, with SIMD; budget: any single adjustment on a 24-megapixel image under 150 ms on the reference machine.
  - Adjustment presets data: `AdjustmentPreset` (ordered list of `EffectDescription`) serialization that `D02 T12 §3` stores and applies.
  - Second consumer: Imago's levels, curves, and brightness and contrast (`D03 T05 §2`) run on these types through its filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered).
- **Proof:** golden proof in `tests/Photon.Core.Tests/Imaging/Adjust/` against GIMP 3.0 fixtures in `tests/fixtures/imaging/adjust/` (max delta 1 of 255 for levels and curves) plus histogram count tests on synthetic ramps; cheaper substitute that fails: a curve evaluated by linear interpolation, which the spline golden rejects.

#### §5. Color adjustments

- **Deliverable:** Hue, saturation, and lightness, color balance, vibrance, selective color, replace colors (current and legacy parameters), desaturate, channel mixer, black and white, invert, and threshold, golden-tested
- **Depends On:** §4
- **Phase:** 9
- **Surface:** no surface of its own (menus and dialogs are D02 T12 §3)
- **Runs:** none
- **Catalog:** NP-1836 to NP-1846 (11 features)
- **Hints:**
  - `Imaging/Adjust/HueSaturationLightness.cs`: master plus six ranges (reds, yellows, greens, cyans, blues, magentas) with feathered range edges; golden from GIMP 3.0 hue-saturation.
  - `ColorBalance` (cyan-red, magenta-green, yellow-blue for shadows, midtones, highlights, `PreserveLuminance`); golden from GIMP 3.0 color-balance.
  - `Vibrance` (saturation boost weighted by inverse saturation, skin-tone protection off by default, documented) with property tests (already saturated pixels move less).
  - `SelectiveColor` (CMYK percentage shifts for reds, yellows, greens, cyans, blues, magentas, whites, neutrals, blacks; relative and absolute) computed in RGB with the naive CMY conversion documented, pending `D01 T04 §1` for profile-accurate CMYK.
  - `ReplaceColors` (sampled color, hue range ring, saturation range, smoothing, HSL output) and `ReplaceColorsLegacy` mapping the older parameter set onto the same kernel (CD-2287).
  - `Desaturate`, `BlackAndWhite` (six per-color weights plus tint hue and strength), `ChannelMixer` (3x3 plus constant, monochrome flag), `Invert`, and `Threshold` (level, plus band mode).
  - Shared `HslMath` and `RgbMatrix` helpers so each adjustment is a lookup or matrix fused per pixel; budget as §4.
  - Second consumer: Imago's hue and saturation adjustment (`D03 T05 §2`) through the filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered).
- **Proof:** golden proof in `tests/Photon.Core.Tests/Imaging/Adjust/ColorAdjustTests.cs` against GIMP 3.0 fixtures in `tests/fixtures/imaging/color/`, snapshot goldens plus property tests for vibrance and selective color; cheaper substitute that fails: hue shift by rotating RGB channels, which the hue golden rejects.

#### §6. Blur, sharpen, and noise

- **Deliverable:** Gaussian, motion, radial, zoom, smart, bokeh, and tune blur; directional smooth, low pass, soften, smooth, jaggy despeckle; sharpen, unsharp mask, adaptive unsharp, directional sharpen, high pass, tune sharpen; add noise, 3-D stereo noise, median, minimum, maximum, remove noise, dust and scratch, remove moire, tune noise, classical JPEG artifact removal, and local equalization
- **Depends On:** §1
- **Phase:** 9
- **Surface:** no surface of its own (menus, gallery, and FX panel are D02 T12 §2)
- **Runs:** none
- **Catalog:** NP-1847 to NP-1874 (28 features)
- **Hints:**
  - Group the work by kernel family, one checklist item each, so 28 effects fit one section: separable convolution, directional line integral, rank filters, frequency split, and noise generators.
  - `Imaging/Effects/Blur/GaussianBlur.cs` (separable, three-box approximation above radius 32 with the exact kernel below) as the base; `LowPass`, `Soften`, `Smooth` are parameterized presets on it; golden from libvips `gaussblur` and GIMP 3.0.
  - `MotionBlur` (angle, distance), `RadialBlur` (spin, center, quality) and `ZoomBlur` (center, amount) as line-integral samplers; `BokehBlur` (disc kernel with highlight boost); `SmartBlur` (radius, threshold, normal, edge only, overlay edge modes) as a thresholded bilateral.
  - `DirectionalSmooth` and `JaggyDespeckle` as edge-aware smoothing; `TuneBlur` and `TuneSharpen` and `TuneNoise` are parameter-set browsers over the underlying effects, registered as their own ids for the thumbnail pickers in `D02 T12 §2`.
  - `UnsharpMask` (percentage, radius, threshold) golden against GIMP 3.0 and ImageMagick `-unsharp`; `Sharpen` (edge level, threshold, preserve colors by sharpening luminance only), `AdaptiveUnsharp`, `DirectionalSharpen`, `HighPass` derived from the same frequency split.
  - Rank filters `Median`, `Minimum`, `Maximum` with a sliding histogram (O(1) per pixel in radius); `DustAndScratch` (median gated by contrast threshold); `RemoveNoise` (adaptive median); golden against ImageMagick `-statistic`.
  - `AddNoise` (uniform, Gaussian, spike; amount; color or mono) and `ThreeDStereoNoise` (random-dot stereogram from luminance depth) driven by the `EffectContext.Seed` with a counter-based RNG so tiles are order-independent.
  - `RemoveMoire` (notch in a low-pass band), `RemoveJpegArtifacts` (classical 8x8 block deblocking, no model), and `LocalEqualization` (CLAHE with tile size and clip limit).
  - Budget: Gaussian radius 50 on 24 megapixels under 400 ms; every effect cancellable at tile granularity with a test.
  - Second consumer: Imago's Blur and Sharpen menu (`D03 T05 §3`) through its filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered); its stub commands route here.
- **Proof:** golden proof in `tests/Photon.Core.Tests/Imaging/Effects/BlurSharpenNoiseTests.cs` against libvips 8.16, GIMP 3.0, and ImageMagick 7.1 fixtures under `tests/fixtures/imaging/blur/`, `sharpen/`, `noise/` with per-effect tolerances, plus seed-determinism tests for the noise generators; cheaper substitute that fails: a box blur labeled Gaussian, which the Gaussian golden rejects.

#### §7. Distort and 3D-style effects

- **Deliverable:** Blocks, displace, mesh warp, offset, pixelate, ripple, shear, swirl, tile, wet paint, whirlpool, wind, diffuse glow, glass, ocean ripple with texture and glass surface controls, 3-D rotate, cylinder, emboss, page curl, pinch and punch, sphere, and zig zag
- **Depends On:** §2
- **Phase:** 9
- **Surface:** no surface of its own (the mesh warp and 3-D rotate interactive editors are parameter editors in D02 T12 §2)
- **Runs:** none
- **Catalog:** NP-1875 to NP-1897 (23 features)
- **Hints:**
  - One `InverseMapEffect` base in `Imaging/Effects/Distort/`: each effect supplies `Map(x, y) -> (u, v)` and samples the source through the §2 `Resampler` kernels with edge modes (wrap, clamp, color); covers ripple, shear, swirl, pinch and punch, sphere, cylinder, zig zag, whirlpool, ocean ripple, and offset.
  - `Displace` reads a displacement map buffer (the consumer loads the file) with horizontal and vertical scale and tile or stretch fit; `Glass` and the shared `SurfaceTexture` controls (scaling, relief, light direction, invert, load texture, AI-0777) build on it with built-in procedural textures (frosted, blocks, canvas, tiny lens) and no bundled third-party images.
  - `MeshWarp` (up to 10 gridlines, node positions as parameters, savable presets as `EffectDescription` JSON) through bilinear patch inversion; `ThreeDRotate` (yaw and pitch on a plane, best fit) through a projective map.
  - `PageCurl` (corner, vertical or horizontal, opaque or transparent, curl and background colors, width and height percent) as a cylinder projection with shading.
  - `Emboss` (depth, level, direction, original color, gray, black, other) as a directional derivative; `DiffuseGlow` (grain, glow amount, clear amount) combining noise from §1 seed and a highlight blur.
  - `Blocks`, `Pixelate` (square, rectangular, circular), `Tile`, `WetPaint`, `Wind` (strength, direction, opacity) as cell or streak operations with seeded randomness.
  - Snapshot goldens for effects with no reference plus property tests (identity at zero strength, bounds from `ExpandBounds`, seed determinism); ImageMagick `-swirl`, `-implode`, and `-wave` as references for swirl, pinch, and ripple.
  - Second consumer: Imago's Distort filter menu through its filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered).
- **Proof:** snapshot and golden proof in `tests/Photon.Core.Tests/Imaging/Effects/DistortTests.cs` with fixtures in `tests/fixtures/imaging/distort/` (ImageMagick 7.1 references where named, snapshot goldens otherwise) and identity-at-zero property tests; cheaper substitute that fails: forward-mapped distortion that leaves holes, which the identity and coverage tests reject.

#### §8. Artistic and art-stroke effects

- **Deliverable:** Colored pencil, cutout, dry brush, film grain, fresco, neon glow, paint daubs, palette knife, plastic wrap, poster edges, rough pastels, smudge stick, sponge, underpainting, watercolor, charcoal, conte crayon, crayon, cubist, dabble, impressionist, pastels, pen and ink, pointillist, scraperboard, sketch pad, water marker, and wave paper
- **Depends On:** §6
- **Phase:** 9
- **Surface:** no surface of its own (the Effect Gallery that previews these is D02 T12 §2)
- **Runs:** none
- **Catalog:** NP-1898 to NP-1925 (28 features)
- **Hints:**
  - Build three shared primitives first in `Imaging/Effects/Artistic/`: `StrokeField` (structure-tensor orientation from §6 gradients), `StrokeRenderer` (seeded dabs and strokes along the field with size, length, and pressure), and `PaperTexture` (procedural paper and canvas grains); every effect is a parameter set over them plus §3 posterize and §6 filters.
  - Painterly group: dry brush, paint daubs, palette knife, fresco, impressionist, dabble, smudge stick, underpainting, watercolor (granulation and edge darkening), sponge; one checklist item per group, not per effect.
  - Drawing-media group: colored pencil, rough pastels, pastels, crayon, conte crayon (foreground and background colors), charcoal, sketch pad, pen and ink (cross-hatch or stipple), scraperboard, water marker, wave paper.
  - Graphic group: cutout (posterize plus region simplification), poster edges, cubist, pointillist (colored dots with size and lightness), film grain, plastic wrap, neon glow.
  - All randomness through `EffectContext.Seed`; the same effect with the same seed and parameters yields identical bytes on any tile order.
  - No reference implementation exists for these effects: each gets a committed snapshot golden at two parameter sets plus property tests (bounds, determinism by seed, alpha preservation, identity-like output at minimum strength where defined).
  - Budget: any effect on a 12-megapixel image under 3 seconds with progress and cancellation; preview at `PreviewScale` 0.25 under 250 ms for the gallery.
  - Second consumer: Imago's Artistic filter menu through its filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered).
- **Proof:** snapshot proof in `tests/Photon.Core.Tests/Imaging/Effects/ArtisticTests.cs` with fixtures in `tests/fixtures/imaging/artistic/` plus the property suite from §1; cheaper substitute that fails: a posterize relabeled per effect, which the snapshot set and the seed-determinism tests expose as identical outputs.

#### §9. Brush-stroke and sketch effects

- **Deliverable:** Accented edges, angled strokes, crosshatch, dark strokes, ink outlines, spatter, sprayed strokes, sumi-e, bas relief, chalk and charcoal, chrome, graphic pen, halftone pattern, note paper, photocopy, plaster, reticulation, stamp, torn edges, water paper, and glowing edges
- **Depends On:** §6
- **Phase:** 9
- **Surface:** no surface of its own (the Effect Gallery is D02 T12 §2)
- **Runs:** none
- **Catalog:** NP-1926 to NP-1946 (21 features)
- **Hints:**
  - Reuse the §8 `StrokeField` and `StrokeRenderer` (§8 lands first in the same phase; if it has not, build them here and §8 consumes them).
  - Brush-stroke group in `Imaging/Effects/BrushStrokes/`: accented edges, angled strokes, crosshatch, dark strokes, ink outlines, spatter, sprayed strokes, sumi-e.
  - Sketch group in `Imaging/Effects/Sketch/`: two-color effects that map luminance to the document foreground and background colors passed as parameters: bas relief, chalk and charcoal, chrome, graphic pen, halftone pattern (dot, circle, line), note paper, photocopy, plaster, reticulation, stamp, torn edges, water paper.
  - `GlowingEdges` (edge width, brightness, smoothness) from the §6 gradient and blur.
  - Color parameters are RGBA values, never references to a Nodus swatch, so Imago can pass its own foreground and background.
  - Snapshot goldens at two parameter sets per effect plus the §1 property suite; two-color effects additionally assert that every output pixel lies on the segment between the two colors.
  - Second consumer: Imago's Brush Strokes and Sketch filter menus through its filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered).
- **Proof:** snapshot proof in `tests/Photon.Core.Tests/Imaging/Effects/BrushSketchTests.cs` with fixtures in `tests/fixtures/imaging/sketch/` plus the two-color property test; cheaper substitute that fails: grayscale threshold labeled as sketch effects, which the two-color and snapshot tests reject.

#### §10. Texture and creative effects

- **Deliverable:** Craquelure, grain, mosaic tiles, patchwork, stained glass, texturizer, crystallize, fabric, frame, glass block, mosaic, scatter, smoked glass, vignette, vortex, brick wall, bubbles, canvas, cobblestone, elephant skin, etching, plastic, plaster wall, relief sculpture, screen door, stone, and the bitmap bevel (The Boss)
- **Depends On:** §6
- **Phase:** 9
- **Surface:** no surface of its own (the Effect Gallery is D02 T12 §2)
- **Runs:** none
- **Catalog:** NP-1947 to NP-1973 (27 features)
- **Hints:**
  - Shared primitives in `Imaging/Effects/Texture/`: `ReliefLighting` (height map, light direction and elevation, depth) and `CellPartition` (seeded Voronoi and grid cells); most effects are parameter sets over these two.
  - Relief group: craquelure, texturizer (built-in procedural textures or a loaded buffer), canvas (preset or loaded canvas map), brick wall, cobblestone, stone, plaster wall, elephant skin, etching, plastic, relief sculpture, screen door, bubbles, and grain (the eleven Illustrator grain types).
  - Cell group: stained glass (piece size, solder width and color), crystallize (cell size), mosaic tiles, patchwork, mosaic (elliptical pieces), glass block, fabric (needlepoint, rug hooking, quilt, strings, ribbons, tissue collage).
  - Creative group: frame (a frame image supplied by the consumer, opacity, blur and feather, scale, rotation), vignette (ellipse, circle, rectangle, square; color; offset; fade), smoked glass (tint, opacity, blur), scatter (direction, amount), vortex (inner and outer direction).
  - `BitmapBevel` (The Boss: width, height, smoothness, light direction and elevation, color) on the alpha edge via `ReliefLighting`.
  - Ship procedural textures only; loaded canvas maps and frames come from user files, and no Corel or Adobe content is bundled.
  - Snapshot goldens plus the §1 property suite; cell effects additionally assert the cell count scales with cell size and that cells are stable for a seed.
  - Second consumer: Imago's Texture and Stylize filter menus through its filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered).
- **Proof:** snapshot proof in `tests/Photon.Core.Tests/Imaging/Effects/TextureCreativeTests.cs` with fixtures in `tests/fixtures/imaging/texture/` plus cell-count and determinism property tests; cheaper substitute that fails: one tiled bitmap overlay for every texture effect, which the snapshot set exposes.

#### §11. Camera, color-transform, edge, custom, pixelate, and video effects

- **Deliverable:** Colorize, diffuse, lens flare, lighting effects, photo filter, sepia toning, spot filter, time machine, bit planes, color halftone, psychedelic, solarize, edge detect, find edges, trace contour, band pass, bump map, user-defined convolution, mezzotint, de-interlace, and NTSC colors
- **Depends On:** §5, §6
- **Phase:** 9
- **Surface:** no surface of its own (menus and FX panel are D02 T12 §2)
- **Runs:** none
- **Catalog:** NP-1974 to NP-1994 (21 features)
- **Hints:**
  - Camera group in `Imaging/Effects/Camera/`: `Colorize` (hue, saturation) and `SepiaToning` and `PhotoFilter` (color, density, preserve luminosity) as §5 matrices; `Diffuse` and `SpotFilter` (focus ellipse, blur, darken) on §6 Gaussian; `TimeMachine` as seven named parameter sets over §5 and §8 grain.
  - `LensFlare` (brightness, lens type 50-300 mm, 35 mm, 105 mm, position) and `LightingEffects` (spot, flood, sun lights with color, intensity, direction, cone; texture channel embossing; savable presets as `EffectDescription` JSON) through the §10 `ReliefLighting`.
  - Color-transform group: `BitPlanes` (per-channel bit selection), `ColorHalftone` (max radius, per-channel screen angles; golden against GIMP 3.0 newsprint), `Psychedelic`, `Solarize`.
  - Edge group: `EdgeDetect` (background white, black, or other; sensitivity), `FindEdges` (soft or solid; level), `TraceContour` (level, upper or lower edge pixels); Sobel and Prewitt kernels shared with §6.
  - Custom group: `BandPass` (inner and outer radius in the frequency split), `BumpMap` (preset or loaded map, surface and light), and `UserDefinedConvolution` (3x3 to 7x7 kernel, divisor, offset; golden against ImageMagick `-morphology Convolve`).
  - `Mezzotint` (dots, lines, strokes; seeded) and `Deinterlace` (odd or even; duplicate or interpolate) and `NtscColors` (clamp YIQ saturation and luminance to broadcast-safe limits).
  - Budget and cancellation per §1; references named per fixture, snapshot goldens where none exists.
  - Second consumer: Imago's Render, Stylize, and Other filter menus through its filter pipeline (`D03 T05 §1`, Phase 5 of the old plan, later renumbered).
- **Proof:** golden and snapshot proof in `tests/Photon.Core.Tests/Imaging/Effects/CameraColorEdgeTests.cs` with fixtures in `tests/fixtures/imaging/camera/`, `edge/`, `custom/` (ImageMagick 7.1 and GIMP 3.0 where named); cheaper substitute that fails: a fixed 3x3 kernel for user-defined convolution, which the 5x5 golden rejects.

### todo/01-core/TODO-04-photon-color-management.md -- `photon-color-management`

- **Title:** "TODO-04 -- Photon.Core Color Management: ICC Transforms, Proofing, and Bitmap Color Modes"
- **Phase(s):** 6, 10
- **Goal:** Photon.Core gains one color-management engine for the suite under `src/Photon.Core/Color/`: a recorded decision (lcms2, MIT, through a thin `LibraryImport` P/Invoke wrapper with the native DLL bundled per RID, against Windows WCS as the rejected candidate), ICC v2 and v4 profile loading, RGB, CMYK, gray, and Lab transforms with rendering intents, black point compensation, proofing transforms, and a gamut API (§1 and §2, phase 6), then bitmap color modes including duotone and multichannel (§3, phase 10). It lives in Photon.Core, not in an app, because the operator-mandated Photon.Core pixel engine (`D01 T03`) needs it for Lab, CMYK, and duotone bitmaps, and Imago's ICC work (`D03 T04 §2`) and Lumen's output transform (`D04 T02 §2`) are its next consumers; Nodus's color model (`D02 T09 §1`) is its first. The engine part of backlog B-023 (Imago color management) is superseded by this file's §1 decision.
- **Current-state facts to verify (with claim candidates):**
  - Photon.Core does not exist yet; `D01 T02 §1` creates it. `<!-- claim: absent src/Photon.Core/Photon.Core.csproj -->`
  - No ICC code exists anywhere in the tree: no lcms binding, no `ColorContext` use, no profile type. `<!-- claim: count "lcms|IccProfile|ColorContext" src/**/*.cs = 0 -->`
  - Nodus's only color type is sRGB bytes with HSL and HSV math. `<!-- claim: count "public readonly struct Color" src/Nodus/Bezier.Core/Models/Color.cs = 1 -->`
  - Backlog B-023 records the engine decision as undecided (lcms2 wrapper or WCS). `<!-- claim: count "B-023\] Color management and soft proofing" todo/backlog.md = 1 -->`
- **Inputs and XREFs:** `D01 T02 §1` (Photon.Core and its app-data paths); `D01 T02 §2` (settings store for default profiles and intents); `D01 T03 §3` (quantization and pixel buffers §3 converts); conventions decision (lcms2 via P/Invoke, native per RID, WCS recorded, `docs/dev/decisions.md` row); backlog B-023 (engine part superseded; its Assign, Convert, and soft-proof parts stay with Imago); B-011 (its "wrapper moves to Photon.Core" note is fulfilled). Consumers that point back: `D02 T09 §1` and `D02 T09 §2` (conversions and gamut warnings), `D02 T13 §1` (document color settings, profile UI, Load Profile), `D02 T13 §6` (soft proofing and gamut warning), `D02 T13 §14` (PDF output intents), `D03 T04 §2` (embedded profiles in PNG and JPEG), `D04 T02 §2` (Lumen output transform to sRGB, Display P3, Adobe RGB).
- **Adjacency:** list=applicable; document=not-applicable (the engine prints nothing; PDF output intents are written by D02 T13 §15 and print by D02 T13 §2); settings=applicable; reporting=not-applicable (profile details are shown by the consumer's color settings surface, D02 T13 §1); notifications=not-applicable (a library: long bitmap conversions take IProgress and CancellationToken and the consuming app's status strip reports them); permissions=applicable; audit=applicable; exchange=applicable; reverse=applicable
- **Adjacency rationale:** the profile store lists installed and system profiles filterable by class and color space; default profiles, intent, black point compensation, preserve black, and map gray are settings-store keys read by the transform factory; a corrupt or unreadable profile and the read-only system color folder are refused by name; every profile import and removal writes a log line and bitmap mode conversions are undoable commands in the consumer; ICC v2 and v4 profiles and duotone ink files are read and written with fixtures; an imported profile can be removed and every conversion undone.

#### §1. The color-management engine decision and ICC transforms

- **Deliverable:** The recorded engine decision and `Photon.Core/Color/` with the lcms2 wrapper, ICC v2 and v4 profile loading, a profile store with a load command, default profiles, and RGB, CMYK, gray, and Lab transforms.
- **Depends On:** D01 T02 §1
- **Phase:** 6
- **Surface:** no surface of its own (Load Profile and the engine name are surfaced by `D02 T13 §1`)
- **Runs:** `Needs: Windows host (build/test)`
- **Catalog:** NP-2076 to NP-2077 (2 features)
- **Hints:**
  - Decision row in `docs/dev/decisions.md`: lcms2 (MIT, GPL-3.0 compatible, ICC v4, proofing, K-preserving intents) versus Windows WCS (`mscms.dll`, no package, weaker v4 and no K-preserving intents), license URLs, coverage table, cost of changing (one wrapper class); justified default lcms2.
  - Native lcms2 2.16 or later built for `win-x64` and `win-arm64`, shipped as `runtimes/<rid>/native/lcms2.dll` from `src/Photon.Core/Photon.Core.csproj`, with the build script and source hash recorded under `build/native/lcms2/`.
  - `src/Photon.Core/Color/Native/Lcms2.cs`: `LibraryImport` source-generated bindings for `cmsOpenProfileFromMem`, `cmsCreateTransform`, `cmsDoTransform`, `cmsCloseProfile`, `cmsDeleteTransform`, and the built-in `cmsCreate_sRGBProfile`, `cmsCreateLab4Profile`, `cmsCreateGrayProfile`; `SafeHandle` wrappers for profiles and transforms.
  - `IccProfile` (description, class, color space, PCS, version, raw bytes) and `ColorTransformService` (cached transforms keyed by profile pair, intent, and flags; thread-safe) in `src/Photon.Core/Color/`.
  - Value types `ColorValue` in RGB, CMYK, Gray, and Lab with `double` components, and span-based bulk conversion for 8 and 16 bit buffers.
  - Default profiles: sRGB (built in), Lab D50 (built in), gray gamma 2.2 (built in), and one freely redistributable CMYK profile (candidates: ECI ISOcoated_v2 for FOGRA39, or an ICC-registry CRPC profile), license recorded beside the file.
  - `ColorProfileStore`: the suite folder `%LOCALAPPDATA%\Rizonesoft\Photon\Color\Profiles\` plus a read-only enumeration of `%WINDIR%\System32\spool\drivers\color`; `Import(path)` validates by opening the profile, refuses a corrupt file by name, and logs one Information line.
  - The Color engine row (CD-1575) is answered by the decision: settings show the engine name and version, not a choice.
  - Settings keys `color.defaultRgbProfile`, `color.defaultCmykProfile`, `color.defaultGrayProfile` with consumers `ColorTransformService` and `D02 T09 §1`.
  - Tests in `tests/Photon.Core.Tests/Color/`: `IccProfileTests` (v2 and v4 fixtures), `ColorTransformServiceTests`, `ColorProfileStoreTests` (corrupt profile refused).
- **Proof:** Unit tests comparing 100 committed sample colors through sRGB, CMYK, gray, and Lab against lcms2's own `transicc` output (version recorded) within Delta E 2000 0.5, with profile fixtures under `tests/fixtures/core/icc/`; cheaper substitute that fails: hand-written sRGB-to-CMYK formulas, which the CMYK expectations reject.

#### §2. Rendering intents, black point compensation, proofing transforms, and gamut checks

- **Deliverable:** Rendering intents, black point compensation, preserve pure black, map gray to CMYK black, proofing transforms (simulate device, paper color, preserve numbers), and a gamut API with bring-into-gamut.
- **Depends On:** §1
- **Phase:** 6
- **Surface:** no surface of its own (consumed by `D02 T09 §2`'s gamut warning and `D02 T13 §1` and `D02 T13 §6`)
- **Runs:** `Needs: Windows host (build/test)`
- **Catalog:** NP-2078 to NP-2081 (4 features)
- **Hints:**
  - `RenderingIntent` Perceptual, RelativeColorimetric, Saturation, AbsoluteColorimetric mapped to lcms2 intents; `TransformOptions` with `BlackPointCompensation` (`cmsFLAGS_BLACKPOINTCOMPENSATION`).
  - Preserve pure black through lcms2's `INTENT_PRESERVE_K_ONLY_*` intents; map gray to CMYK black as a gray-to-K-only path that bypasses the CMYK profile for neutral input.
  - `ProofTransform` through `cmsCreateProofingTransform` with `cmsFLAGS_SOFTPROOFING`: simulate device, simulate paper color (absolute colorimetric on the proof leg), and preserve numbers (identity for same-space data).
  - Gamut API: `IsInGamut(ColorValue, IccProfile)` through `cmsFLAGS_GAMUTCHECK` plus a Delta E round-trip threshold (setting `color.gamutThreshold`, default 2.0), and `BringIntoGamut` by a relative colorimetric round trip.
  - Bulk gamut mask for a pixel span, for `D02 T13 §6`'s gamut warning overlay.
  - Settings keys `color.renderingIntent`, `color.blackPointCompensation`, `color.preservePureBlack`, `color.mapGrayToK` with the transform factory as consumer.
  - Cancellation and `IProgress<double>` on bulk conversions over one second; a 100-megapixel RGB-to-CMYK conversion budget is measured and recorded.
  - Tests: `RenderingIntentTests`, `ProofTransformTests`, `GamutTests` (known out-of-gamut sRGB green against the CMYK default), `PreserveBlackTests` (0,0,0,100 stays 0,0,0,100).
- **Proof:** Unit tests against `transicc` goldens for every intent with and without black point compensation and for the proof transform, within Delta E 2000 0.5; cheaper substitute that fails: ignoring the intent argument, which the perceptual versus relative expectations reject.

#### §3. Bitmap color modes: grayscale, Lab, CMYK, duotone, and multichannel

- **Deliverable:** Bitmap color mode conversions through ICC (grayscale 8-bit, RGB 24-bit, Lab 24-bit, CMYK 32-bit), duotone (monotone to quadtone with ink curves and overprint colors), and multichannel, with a Nodus Duotone dialog.
- **Depends On:** §2, D01 T03 §3
- **Phase:** 10
- **Surface:** user-facing (the Duotone dialog)
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/duotone/.
  - Job: a print designer can convert a placed bitmap to duotone or another color mode and print its inks as spot plates. Consumer: the bitmap object, separations (`D02 T13 §5`), and PDF DeviceN output (`D02 T13 §14`).
  - Treatment: a Duotone dialog with type (monotone, duotone, tritone, quadtone), per-ink color and tone curve, show all curves, save and load inks, and an overprint colors editor with live preview. Cheaper substitute that fails: a grayscale image tinted with one RGB color.
  - Chrome: consume the engine from §1 and §2, `D01 T03`'s pixel buffers, the Nodus picker from `D02 T09 §2` for ink colors, and the theme. The dialog lives in `Photon.Nodus.Desktop` until a second app needs it.
- **Runs:** `Requires: display-session -- the Duotone dialog needs an interactive desktop`
- **Catalog:** NP-2082 to NP-2085 (4 features)
- **Hints:**
  - `src/Photon.Core/Color/BitmapModes/BitmapModeConverter.cs` converting `D01 T03` pixel buffers between Gray8, Rgb24, Lab24, and Cmyk32 through `ColorTransformService` with the document profiles and intent, cancellable with progress.
  - `DuotoneSpec`: 1 to 4 inks (spot or process `ColorValue` with name), a 0 to 100 tone curve per ink, and an overprint color per ink pair; the image stores the gray channel plus the spec.
  - `DuotoneRenderer` composites the inks for display through the proof transform (§2), with overprint colors overriding pairwise mixes.
  - Save and load ink sets as JSON (`.photonduotone`) and read Photoshop `.ado` duotone files per Adobe's published file format specification.
  - Multichannel mode: channels as named spot plates with no composite conversion.
  - Auto convert for effects: a helper that converts to RGB for an RGB-only effect and back, recording the round trip.
  - `src/Nodus/Photon.Nodus.Desktop/Views/Bitmaps/DuotoneDialog.xaml` reached from Bitmaps > Mode, applying one undoable command with a Serilog Information line.
  - Persistence: Nodus writes the duotone spec as `nodus:duotone` on the image with a composited RGB fallback image; `D02 T14 §2`'s PDF import maps DeviceN duotone images into the same spec.
  - Tests: `BitmapModeConverterTests` (lcms2 `transicc` goldens), `DuotoneRendererTests` (snapshot goldens plus property tests: alpha preserved, determinism), `AdoReaderTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/core/duotone/` (an `.ado` file and a Nodus SVG with a duotone image) round-tripped exactly, plus mode conversion goldens from `transicc` within Delta E 2000 0.5 and duotone snapshot goldens within a stated tolerance; cheaper substitute that fails: an RGB tint, which the per-ink plate assertion rejects.

### todo/01-core/TODO-05-photon-ai.md -- `photon-ai`

- **Title:** "TODO-05 -- Photon.Core AI: OpenRouter Client, Keys, Consent, Provenance, and the Brand Kit"
- **Phase(s):** 12
- **Goal:** The AI plumbing every suite app needs exists once: an OpenRouter client (chat with JSON-schema structured output, image generation and editing, vision, streaming, model catalog, usage), a bring-your-own key stored with DPAPI, a per-task model choice in settings, an explicit-send gate with a send preview, a provenance record every AI action writes into the document, and a suite brand kit of palettes and styles; it lives in `Photon.Core` (`src/Photon.Core/AI/`, `src/Photon.Core/Brand/`) and `Photon.UI` (`src/Photon.UI/AI/`) by operator decision (2026-09-26), not in Nodus, so Imago and Lumen reuse the client, key store, consent gate, provenance, and brand kit instead of growing their own; nothing leaves the machine without an explicit user action, and no key ever reaches `settings.json` or a log.
- **Current-state facts to verify (with claim candidates):**
  - There is no `Photon.Core` project yet; `D01 T02 §1` creates it. `<!-- claim: absent src/Photon.Core -->`
  - No source file in the repository talks to OpenRouter or any HTTP AI endpoint. `<!-- claim: count "OpenRouter" src/Nodus/**/*.cs = 0 -->`
  - Nodus has no HTTP client code at all. `<!-- claim: count "HttpClient" src/Nodus/**/*.cs = 0 -->`
  - Nothing uses DPAPI (`ProtectedData`) for secrets today. `<!-- claim: count "ProtectedData" src/Nodus/**/*.cs = 0 -->`
  - The Nodus SVG reader skips `<metadata>` children at the root, so a provenance record written there would be lost on reopen until the reader keeps it. `<!-- claim: count "\"metadata\"" src/Nodus/Bezier.Core/Services/SvgParser.cs = 1 -->`
  - Nodus's export options strip metadata by default, which provenance export must respect as an explicit choice. `<!-- claim: count "public bool RemoveMetadata \{ get; set; \} = true;" src/Nodus/Bezier.Core/Services/ExportService.cs = 1 -->`
  - Imago keeps its own settings service today (the store `D01 T02 §2` replaces), so AI settings go only through the shared store. `<!-- claim: exists src/Imago/src/Imago.UI/Services/SettingsService.cs -->`
  - Lumen has no source tree yet; its reuse of this file is a stated consumer, not a dependency. `<!-- claim: absent src/Lumen -->`
- **Inputs and XREFs:** `standards/shared.md` (logging, settings, and the no-secrets-in-logs rule); `D01 T02 §1` (app-data paths and the Serilog bootstrap the client logs through); `D01 T02 §2` (the settings store the model choices and timeouts live in); `D01 T01 §3` (the suite theme the send-preview dialog and AI settings page consume); `D01 T02 §4` (the undo history every AI apply records into); `D02 T07 §1` (the live-object contract whose `nodus:` metadata carries provenance in Nodus); `D02 T15 §1` (the first consumer: the Nodus AI menu and provenance panel); `D02 T15 §5` and `D02 T15 §11` (the brand kit's first consumers); `D03 T04 §2` (Imago's save, a later consumer of provenance embedding); OpenRouter API reference (`https://openrouter.ai/docs/api-reference`) for chat completions, `response_format` JSON schema, image output, `/models`, and `/key` usage; Microsoft Learn `ProtectedData.Protect` with `DataProtectionScope.CurrentUser`.
- **Adjacency:** list=applicable (the model catalog is filterable by task capability and price in the AI settings page, §2); document=not-applicable (this file prints nothing; provenance travels inside the app's own document); settings=applicable @ D01 T02 §2; reporting=applicable (usage and credit balance for the user's key, §1 data and §4 indicator); notifications=applicable (generation progress, cancel, and failure toasts through the shared surfaces, §4); permissions=applicable (no key, offline, a rejected key, a refused model, and a declined send preview are refusals by name, §1 and §4); audit=applicable (every request writes one Serilog Information line without the key or prompt body, and every apply writes a provenance record, §3); exchange=applicable (brand kits import and export ASE, §5; provenance serializes to SVG metadata and JSON, §3); reverse=applicable (key removal, brand kit delete, and every AI apply undoable through the suite history)

#### §1. The OpenRouter client: chat, structured output, images, streaming, and the model catalog

- **Deliverable:** `Photon.Core.AI.OpenRouterClient` that sends chat (with JSON-schema structured output and vision input), image generation and edit requests, streams tokens, queries the model catalog and key usage, and maps every failure to a named, user-facing refusal, with a 60 s default timeout, bounded retries, and cancellation.
- **Depends On:** D01 T02 §2
- **Phase:** 12
- **Surface:** no surface of its own
- **Runs:** none (all tests run against a recorded-response `HttpMessageHandler`, never the network)
- **Catalog:** NP-2478 (1 features)
- **Hints:**
  - `src/Photon.Core/AI/IAiClient.cs` interface (`ChatAsync`, `ChatStructuredAsync<T>`, `GenerateImageAsync`, `EditImageAsync`, `StreamChatAsync`, `ListModelsAsync`, `GetUsageAsync`) so apps and tests depend on the interface, not the vendor.
  - `src/Photon.Core/AI/OpenRouterClient.cs` over one `HttpClient` from `IHttpClientFactory`, base URL `https://openrouter.ai/api/v1`, headers `Authorization: Bearer`, `HTTP-Referer`, and `X-Title: Photon <App>`; the key comes only from `IAiKeyStore` (§2) at call time.
  - Structured output: `ChatStructuredAsync<T>(prompt, JsonSchema schema)` sends `response_format = { type: "json_schema", strict: true }`, validates the reply against the schema with `System.Text.Json` plus a small `JsonSchemaValidator` in `src/Photon.Core/AI/Schema/`, and retries once with the validation errors appended before refusing with "The model returned output that does not match the schema".
  - Images: `GenerateImageAsync(ImageRequest)` (prompt, aspect ratio, size, seed, reference images) returns `AiImageResult` (PNG bytes, model id, seed actually used); vision input sends image parts as base64 data URLs with their byte size recorded for the send preview (§4).
  - Streaming via server-sent events parsed into `IAsyncEnumerable<AiChunk>`, honoring `CancellationToken` so a cancel stops the read within 250 ms.
  - Timeouts and retries: `ai.requestTimeoutSeconds` (default 60, the CorelDRAW 27.2 figure) and `ai.maxRetries` (default 2, exponential backoff on 429 and 5xx only, honoring `Retry-After`); both settings keys registered with defaults in the settings store.
  - `AiErrorMapper` maps 401 (key rejected), 402 (no credit), 403 (model refused), 408 or timeout, 429, 5xx, and `HttpRequestException` with no network (offline) to `AiFailure` records with a user sentence and a log category; offline is detected before sending and refused as "No network connection: nothing was sent".
  - `ListModelsAsync` reads `/models` into `AiModelInfo` (id, name, input and output modalities, context length, prompt and completion price, supports structured output) cached for 24 h under `%LOCALAPPDATA%\Rizonesoft\Photon\ai\models.json`; `GetUsageAsync` reads `/key` (usage, limit, remaining).
  - Logging: one Serilog Information line per request with app, task, model id, token counts, duration, and cost; a `LogRedaction` test asserts the key and prompt text never appear in any sink.
  - Tests in `tests/Photon.Core.Tests/AI/OpenRouterClientTests.cs` over recorded fixtures in `tests/fixtures/ai/openrouter/` (chat, structured, invalid-schema reply, image, SSE stream, 401, 402, 429 with Retry-After, timeout).
- **Proof:** Unit test: `OpenRouterClientTests` pass against recorded fixtures, including the timeout (fake clock), retry, schema-retry, cancel-within-250 ms, and redaction cases; cheaper substitute that fails: a client tested only against the live API, which cannot run in CI and cannot prove the refusals.

#### §2. API keys with DPAPI and the AI settings contract

- **Deliverable:** `AiKeyStore` that stores the user's OpenRouter key encrypted with DPAPI (CurrentUser) in app data, never in `settings.json` or a log, plus the `AiSettings` contract of per-task model choices, defaults, test connection, and key removal.
- **Depends On:** §1
- **Phase:** 12
- **Surface:** no surface of its own (the settings page that edits it is §4)
- **Runs:** none
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - `src/Photon.Core/AI/AiKeyStore.cs` implementing `IAiKeyStore` (`HasKey`, `SetKeyAsync`, `GetKey`, `RemoveKey`, `KeyFingerprint`) writing `ProtectedData.Protect(bytes, entropy, DataProtectionScope.CurrentUser)` to `%LOCALAPPDATA%\Rizonesoft\Photon\ai\openrouter.key` through the atomic writer; one key shared by every suite app.
  - The in-memory key is held only for the call; `KeyFingerprint` (last 4 characters) is the only form ever displayed or logged.
  - `src/Photon.Core/AI/AiSettings.cs` settings keys with defaults and consumers: `ai.enabled` (false until a key is set), `ai.model.text`, `ai.model.vision`, `ai.model.image`, `ai.model.vectorJson`, `ai.requestTimeoutSeconds`, `ai.maxRetries`, `ai.sendPreview.alwaysShow` (true), `ai.redactDocumentNames` (true), `ai.defaultSeedMode` (random or fixed).
  - Default models are recorded as justified defaults in `docs/dev/decisions.md` (one structured-output text model, one vision model, one image model), each replaceable in settings without a reinstall.
  - `TestConnectionAsync` calls `GetUsageAsync` and returns ok, rejected key, or offline without sending any document content.
  - A guard test scans `settings.json` and the log folder after a set-key, call, remove-key cycle and asserts the key string appears nowhere.
  - Key removal deletes the file and clears the cache; a corrupt or foreign-user blob (`CryptographicException`) is refused by name as "The saved key cannot be read on this account; enter it again".
  - Tests in `tests/Photon.Core.Tests/AI/AiKeyStoreTests.cs` and `AiSettingsTests.cs`.
- **Proof:** Unit test: `AiKeyStoreTests` round-trips a key through DPAPI, asserts the file bytes do not contain the key, and the leak guard finds no key in settings or logs; cheaper substitute that fails: storing the key in `settings.json` or an environment variable, which the leak guard catches.

#### §3. The AI provenance record

- **Deliverable:** `ProvenanceRecord` capturing action, prompt, system prompt hash, model id and version, parameters, seed, input and output hashes, timestamps, and cost, serialized for SVG metadata embedding and the app history, with re-run and compare support.
- **Depends On:** §1
- **Phase:** 12
- **Surface:** no surface of its own
- **Runs:** none
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - `src/Photon.Core/AI/Provenance/ProvenanceRecord.cs` record: `Id` (Guid), `App`, `Action` (for example `nodus.textToVector`), `Prompt`, `SystemPromptSha256`, `ModelId`, `ModelVersion` (from the response), `Parameters` (ordered dictionary), `Seed`, `InputHashes` and `OutputHashes` (SHA-256 of each input image or selection SVG and each output), `CreatedUtc`, `DurationMs`, `CostUsd`, `ResultObjectIds`, `ParentId` (for re-runs and variations).
  - `ProvenanceSerializer` writes one `<photon:provenance>` element per record in the `https://rizonesoft.com/ns/photon-ai/1` namespace, suitable for an SVG `<metadata>` child, and a JSON form for history and export; both versioned (`schemaVersion="1"`).
  - `ProvenanceStore` (per document) with `Add`, `Remove`, `FindByObject(Guid)`, and `Lineage(id)`; adding and removing are undoable commands through the suite history so an undone generation also drops its record.
  - `RerunRequest ProvenanceRecord.ToRerun(bool sameSeed)` rebuilds the exact request; `ProvenanceDiff.Compare(a, b)` lists parameter, model, and seed differences for the compare view.
  - Privacy: attached images are stored as hashes only, never embedded; the prompt is stored because it is the user's own text, and a setting `ai.provenance.storePrompts` (default true) can store a hash instead.
  - Hand-off rule: the serializer round-trips unknown future fields, so a record written by Imago or Lumen survives a Nodus save (§11 of `D02 T15` relies on it).
  - Fixture `tests/fixtures/photon/provenance/v1-record.svg` with a golden JSON beside it; tests in `tests/Photon.Core.Tests/AI/ProvenanceSerializerTests.cs`.
- **Proof:** Format fidelity proof: the committed `v1-record.svg` metadata block reads and writes back byte-equivalent (canonical XML) and equals its golden JSON, and a record with an unknown field survives the round trip; cheaper substitute that fails: storing provenance in app settings instead of the document, which the fixture round trip cannot see.

#### §4. The explicit-send gate and the shared AI surfaces in Photon.UI

- **Deliverable:** `AiSendGate` plus the shared `Photon.UI` AI surfaces: the send-preview dialog, the AI settings page, generation progress with cancel, the usage indicator, and the AI help page, so nothing is sent without an explicit user action and a preview of exactly what leaves the machine.
- **Depends On:** §2, §3, D01 T01 §3
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/photon-ui/ai-send-preview/ and docs/captures/photon-ui/ai-settings/. Job: a user can see and approve exactly what an AI action sends, and set their key and models once for the suite. Treatment: a modal preview listing the prompt text, each attached image as a thumbnail with pixel size and bytes, the selection SVG size, the model id, and the estimated cost, with Send and Cancel and a per-session "do not ask again for this action" option. Cheaper substitute that fails: a generic "Send to AI?" yes/no box that shows nothing. Chrome: consume `Photon.Dark.xaml`, the icon catalog, the settings store, and the suite toast; do not build a per-app key dialog or a second progress control.
- **Runs:** `Requires: display-session -- the send-preview and settings captures need an interactive desktop`
- **Catalog:** NP-2479 (1 features)
- **Hints:**
  - `src/Photon.Core/AI/AiSendGate.cs`: every `IAiClient` call goes through `AiSendGate.RequestAsync(AiSendPlan plan, IAiConsentPrompt prompt)`, which refuses with "No explicit action" unless the plan carries a `UserActionId` from a command invocation, then shows the preview; a unit test proves no background code path can call the client directly (the client constructor is internal to the gate).
  - `AiSendPlan` lists every outgoing part (text, image bytes, selection SVG, document name) with sizes; `ai.redactDocumentNames` replaces file and layer names with neutral tokens before the preview is built.
  - `src/Photon.UI/AI/SendPreviewDialog.xaml(.cs)` with `SendPreviewViewModel`; the session consent option is per action id and resets on restart, never persisted.
  - `src/Photon.UI/AI/AiSettingsPage.xaml` hosted by each app's preferences: key entry (masked, fingerprint shown), Test connection, Remove key, per-task model pickers filtered by capability from the catalog with price, timeout, and seed mode.
  - `src/Photon.UI/AI/AiProgressPanel.xaml` for long requests: elapsed time, streamed text or stage, Cancel that cancels the token and logs the cancel.
  - `src/Photon.UI/AI/AiUsageIndicator.xaml` showing remaining balance and usage from `GetUsageAsync`, refreshed after each request, hidden when no key is set.
  - Help page `docs/user/photon/ai.md`: what BYOK means, which actions send what, where the key lives, how provenance replaces vendor content credentials, and that there is no regional gating beyond OpenRouter's own.
  - First-use state: with no key, every AI command opens the settings page with the sentence "Add your OpenRouter key to use AI features" instead of failing silently.
  - Tests: `AiSendGateTests` (refuses without an action id, redaction applied, preview contents equal the bytes actually sent), `SendPreviewViewModelTests`.
- **Proof:** Unit test plus driven run with evidence: `AiSendGateTests` prove the preview's listed bytes equal the request body and that a declined preview sends nothing (the fake handler records zero calls); captures of the preview and settings page committed; cheaper substitute that fails: a confirmation dialog that does not list the payload, which the byte-equality test catches.

#### §5. The suite brand kit: shared palettes and styles

- **Deliverable:** A brand kit file format in `Photon.Core` (named palettes, swatches, type styles, logo assets) stored under `%LOCALAPPDATA%\Rizonesoft\Photon\brand-kits`, readable by Nodus, Imago, and Lumen, with ASE import and export, used to constrain AI recolor and generation.
- **Depends On:** D01 T02 §2
- **Phase:** 12
- **Surface:** no surface of its own (each app's swatch and AI panels present it; Nodus's is `D02 T15 §5`)
- **Runs:** none
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - `src/Photon.Core/Brand/BrandKit.cs` record: `Id`, `Name`, `Palettes` (named lists of `BrandColor` with sRGB, optional CMYK and Lab, optional spot name), `TypeStyles` (family, weight, size, tracking, role such as heading or body), `Logos` (relative paths to SVG or PNG assets inside the kit folder), `Rules` (for example minimum contrast, colors never to pair).
  - Storage: one folder per kit, `brand-kits/<slug>/kit.json` plus `assets/`, written with the atomic writer; `BrandKitLibrary` lists, creates, renames, duplicates, deletes (undoable at the library level through a recycle folder), and watches the folder so a kit saved by another app appears live.
  - `AseReader` and `AseWriter` in `src/Photon.Core/Brand/Ase/` for Adobe Swatch Exchange (RGB, CMYK, Lab, gray, global and spot flags, groups), built against the published ASE layout, with fixtures in `tests/fixtures/photon/ase/` and goldens exported by Inkscape's palette import and by Krita (versions recorded).
  - `BrandKitConstraint` turns a kit into an AI prompt fragment and a JSON-schema enum of allowed colors, so structured generation can only return kit colors (consumed by `D02 T15 §2` and `§5`).
  - Settings: `brand.activeKitId` (per app) and `brand.kitsFolder` (default path above) with consumers named.
  - No licensed color books are bundled; the kit only holds colors the user creates or imports.
  - Tests in `tests/Photon.Core.Tests/Brand/BrandKitTests.cs` and `AseRoundTripTests.cs`.
- **Proof:** Format fidelity proof: each committed ASE fixture reads, writes, and rereads with every color, group, and spot flag equal, and matches the reference tools' parse; `BrandKitTests` round-trip `kit.json`; cheaper substitute that fails: a Nodus-only palette file, which Imago cannot read and the cross-app library test catches.

### todo/02-nodus/TODO-07-nodus-parity-document.md -- `nodus-parity-document`

- **Title:** "TODO-07 -- Nodus Parity: Document Model, Pages, Layers, Selection, and View"
- **Phase(s):** 4
- **Goal:** Nodus gains the document foundation every later parity file builds on: a live-object persistence contract in the `nodus:` SVG namespace with plain-SVG fallbacks, a spatial index that keeps a 10,000-object document interactive, one page and artboard model with Corel-style multipage views, full layer and Objects panel control, the Select menu and selection tools, isolation mode, a contextual property bar and Properties panel, rulers, grids, guides, measurement, the full snapping set, view modes and windows, a History panel with paste variants, and a New Document dialog with presets and templates, each edit one undo step and each tunable a setting.
- **Current-state facts to verify (with claim candidates):**
  - The SVG writer and reader know nothing about artboards, so a saved document loses every artboard but the implicit document bounds. `<!-- claim: count "Artboard" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->` `<!-- claim: count "Artboard" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->`
  - No `nodus:` namespace exists yet; the parser reads only `inkscape:label` from a foreign namespace. `<!-- claim: count "nodus:" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->` `<!-- claim: count "inkscape:label|InkscapeNs \+ \"label\"" src/Nodus/Bezier.Core/Services/SvgParser.cs = 1 -->`
  - `ArtboardManager` (412 lines) already models artboards with create, duplicate, rename, resize, move, reorder, navigate, and grid/row/column arrange, and `ArtboardPresets` holds 24 presets; none of it is wired to a surface or persisted. `<!-- claim: lines src/Nodus/Bezier.Core/Services/ArtboardManager.cs = 412 -->` `<!-- claim: count "^        \(\"" src/Nodus/Bezier.Core/Models/Artboard.cs = 24 -->`
  - `VectorDocument` holds a flat `Elements` collection and no layers or guides; `Layer` and `LayerManager` exist beside it unused by the document. `<!-- claim: count "Layer" src/Nodus/Bezier.Core/Models/VectorDocument.cs = 0 -->` `<!-- claim: lines src/Nodus/Bezier.Core/Services/LayerManager.cs = 449 -->`
  - Guides live in a private list inside `SnapManager`, not in the document, so they are never saved. `<!-- claim: count "private readonly List<Guide> _guides" src/Nodus/Bezier.Core/Services/SnapManager.cs = 1 -->` `<!-- claim: count "Guide" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->`
  - `SnapTarget` knows only Grid, Guides, Objects, and SmartGuides; no point, intersection, tangent, or perpendicular modes exist. `<!-- claim: count "SmartGuides = 8" src/Nodus/Bezier.Core/Services/SnapManager.cs = 1 -->`
  - There is no spatial index: the renderer walks every element each frame and hit testing walks the list back to front. `<!-- claim: count "RTree|SpatialIndex|QuadTree" src/Nodus/Bezier.Core/Services/*.cs = 0 -->` `<!-- claim: count "foreach \(var element in document\.Elements\)" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 1 -->`
  - The canvas draws rulers and a grid already (`SkiaCanvas.ShowRulers`, `SkiaRenderer.RenderRulers`, `RenderGrid`) and zoom is clamped to 10 to 6,400 percent. `<!-- claim: count "ShowRulers" src/Nodus/Bezier.Desktop/Controls/Canvas/SkiaCanvas.cs = 9 -->` `<!-- claim: count "MaxZoom = 64\.0" src/Nodus/Bezier.Desktop/Controls/Canvas/CanvasState.cs = 1 -->`
  - No magic wand or lasso tool exists. `<!-- claim: count "Magic|Lasso" src/Nodus/Bezier.Core/Tools/*.cs = 0 -->`
  - Undo is Nodus-local today (`HistoryManager`, 167 lines) until `D01 T02 §4` moves it to `Photon.Core`. `<!-- claim: lines src/Nodus/Bezier.Core/Services/HistoryManager.cs = 167 -->` `<!-- claim: absent src/Photon.Core/History/UndoHistory.cs -->`
- **Inputs and XREFs:** `D02 T05 §4` (Nodus 0.1.0 ships first; every section here follows it); `D02 T01 §1` (the rename to `Photon.Nodus.*` the target paths assume); `D02 T02 §3` (the one selection owner §6 extends); `D02 T02 §6` (the layers panel §5 grows into the Objects panel); `D02 T02 §7` (the basic snapping and `Nodus.Snap.*` toggles §11 extends); `D02 T06 §7` (per-document scopes, tabs, and the nested layer tree §3, §5, and §12 build on); `D02 T04 §1` (atomic save and dirty tracking, which §14's Save a Copy, Revert, and locked-file refusals reuse); `D02 T04 §2` (SVG round-trip fixtures §1 extends with live fixtures); `D02 T04 §3` and `D02 T04 §4` (PNG and PDF export, which §3's artboards and §4's page background feed); `D02 T04 §5` (recent files and autosave, which §14's templates and §2's background save must not break); `D02 T03 §3` and `D02 T03 §4` (clipboard and property commands §13 and §8 extend); `D01 T02 §2` (settings store) and `D01 T02 §4` (suite history); `D02 T06 §12` (the HUD §10's measurement labels share) and `D02 T06 §13` (Preferences pages that list the settings added here); backlog promotions B-004 (`legacy-nodus-4.6`) into §3, B-005 (`legacy-nodus-2.5`) into §8, B-007 (`legacy-nodus-3.7-3.8`) into §10, B-009 (`legacy-nodus-12.1`) into §2, each deleted from `todo/backlog.md` in the authoring commit and the `D02 T06` Adjacency reason that cites B-007 rewritten to point at §10. Consumers that XREF back: `D02 T11 §1` (live-effect framework on §1), `D02 T08 §4` (live shapes on §1), `D02 T09 §21` (symbol overrides on §1), `D02 T13 §2` and `D02 T13 §4` (printing pages and the bleed value from §3 and §4), `D02 T14 §3` and `D02 T14 §6` (AI artboards and CDR pages and master layers landing in §3 and §5), `D02 T16 §4` and `D02 T16 §5` (Preferences pages over the settings added here).
- **Adjacency:** list=applicable (Objects panel search and filter, Artboards and Pages panel find by name, saved views, template browser search); document=applicable @ D02 T13 §2 (pages, bleed, and page background are what print consumes; this file models them); settings=applicable (every toggle and value here is a `Nodus.*` key with a default and a named consumer); reporting=applicable (Info panel, measure tool, document information, History panel); notifications=applicable (status-strip progress and cancel for long operations, background save completion); permissions=applicable (locked or read-only target on save, unreadable template folder, locked layers and artboards refusing edits by name); audit=applicable (every command is one history entry with one Serilog Information line); exchange=applicable (the `nodus:` namespace contract, Inkscape page interop, templates, document presets); reverse=applicable (every create has undo, delete pages and layers restore by undo, Revert to saved)

#### §1. The live-object contract: parameters in the nodus namespace with an expanded SVG fallback

- **Deliverable:** A `Photon.Nodus.Core/Live/` contract that every live feature implements: parameters written in the `nodus:` SVG namespace beside expanded plain-SVG geometry, restored as live objects on reopen, unknown data preserved, and one generic Expand command.
- **Depends On:** D02 T05 §4
- **Phase:** 4
- **Surface:** Object, Expand dialog only. Fidelity: new build, no baseline; captured to docs/captures/nodus/expand/. Job: a designer can turn any live object into plain paths and undo it. Treatment: a modal with Object, Fill, Stroke checkboxes and a Gradient radio pair (Gradient Mesh disabled with a tooltip naming D02 T09 §9, Specify N objects), one history entry "Expand". Cheaper substitute that fails: Expand that only ungroups the fallback. Chrome: consume `Photon.UI` dialog styles and the suite history; do not add a second serializer.
- **Runs:** `Requires: display-session -- the Expand dialog run and the Inkscape open of a live fixture need an interactive desktop`
- **Catalog:** NP-0001 to NP-0002 (2 features)
- **Hints:**
  - Namespace: `xmlns:nodus="https://schemas.rizonesoft.com/nodus/1"`, declared once on the root `<svg>` by `SvgExporter` only when a live object or document data exists; record the URI and the "SVG stays native, Inkscape-style namespace" rationale in `docs/dev/decisions.md`.
  - Contract `ILiveObject` in `Photon.Nodus.Core/Live/ILiveObject.cs`: `string Kind` (lowercase, e.g. `blend`, `envelope`, `rect`), `int SchemaVersion`, `IReadOnlyList<Guid> Sources`, `void WriteParameters(XElement target)`, `IReadOnlyList<VectorElement> Expand()`, plus `LiveObjectRegistry.Register(kind, reader)` wired in the composition root so later files (D02 T08 §4, D02 T11 §1, D02 T09 §21) add kinds without touching the writer.
  - Wire shape: a `<g id="..." nodus:kind="blend" nodus:v="1" nodus:hash="sha1-of-fallback">` whose children are the expanded plain SVG (what browsers and Inkscape render), with one `<nodus:params .../>` child carrying the parameters as attributes and `nodus:src="#id1 #id2"` for source references; invariant cultures and round-trip `R` formatting for numbers.
  - Reader: `SvgImporter` asks the registry for `nodus:kind`; a known kind rebuilds the live object and regenerates; if the fallback's recomputed hash differs from `nodus:hash` (edited in another app) it opens as a plain group and logs a Warning "{Kind} was edited outside Nodus; opened expanded", reported in the open summary.
  - Preservation: an unknown `nodus:kind` or newer `nodus:v` keeps its `XElement` verbatim in `UnknownLiveData`, renders from the fallback, and writes back byte-equivalent; foreign namespaces (`inkscape:`, `sodipodi:`, `i:`, `x:`) on any element are kept in `VectorElement.ForeignAttributes` and re-emitted.
  - Document-level data uses the same namespace: one `<nodus:document>` element inside `<metadata>` holds pages (§3), guides (§10), grids and units (§9), views (§12), and selections (§6), each owned by its section with a `nodus:v` per block.
  - Object metadata: `Name` writes `nodus:label` (and reads `inkscape:label` as a fallback), notes write the standard SVG `<desc>`, the `Guid` identity stays in `id`; setting `Nodus.Svg.IdentifyBy` (`XmlId` default, `Name`) makes `id` a sanitized unique form of the name for web output (AI-1158), consumer `SvgExporter`.
  - `ExpandCommand` in `Photon.Nodus.Core/Commands/` replaces each selected live object with `Expand()`'s result in place (same z-order, layer, and name), one undo step, one Information line `Expanded {Count} live object(s)`; Object, Expand Appearance reuses it for effect stacks when D02 T11 §1 lands.
  - Tests: `LiveObjectContractTests` with a test-only `ProbeLiveObject` kind proving write, reopen as live, hash-mismatch opens expanded, unknown kind preserved byte-equivalent, and `ExpandCommand` undo.
  - Fixtures: `tests/fixtures/nodus/svg-live/` (probe object, unknown future kind, Inkscape-edited fallback) with PNG goldens rendered by Inkscape (version in `goldens/VERSION.txt`), proving the fallback renders the same in Inkscape as the live object in Nodus.
- **Proof:** Format fidelity proof: `SvgLiveRoundTripTests` open, save, and reopen every `tests/fixtures/nodus/svg-live/` file and compare element by element plus the preserved unknown block byte for byte, and Inkscape's rendering of the saved file matches the golden within 1/255; cheaper substitute that fails: writing only the expanded geometry, which the reopen-as-live assertion catches.

#### §2. Spatial index, culling, and dirty-region rendering

- **Deliverable:** An R-tree spatial index over every element's visual bounds that the renderer, hit testing, marquee, and snapping query, with viewport culling, dirty-region redraw over cached pictures, a GPU path with CPU fallback, and cancellable progress, proven on a 10,000-object document. -> SOURCE: legacy-nodus-12.1
- **Depends On:** D02 T05 §4
- **Phase:** 4
- **Surface:** Mostly none of its own; adds View, GPU Preview and Preview on CPU (Ctrl+E), View, Refresh (Ctrl+W), the status-strip progress bar with Cancel, and Preferences, Performance keys. Fidelity: docs/captures/nodus/main-window/ for the menu and status strip. Job: a designer can pan, zoom, select, and drag in a 10,000-object or 1,000-artboard document without stutter. Treatment: 60 fps pan and zoom with a low-resolution cached frame while moving. Cheaper substitute that fails: lowering render quality globally. Chrome: consume the status strip and the settings store; do not add a second progress surface.
- **Runs:** `Requires: display-session -- the frame-time measurement on a live canvas needs an interactive desktop`
- **Catalog:** NP-0188 to NP-0196 (9 features)
- **Hints:**
  - Promoted from backlog B-009 (`-> SOURCE: legacy-nodus-12.1`); delete the B-009 line from `todo/backlog.md` in the authoring commit.
  - API in `Photon.Nodus.Core/Spatial/ISpatialIndex.cs`: `void Insert(Guid id, Rect bounds)`, `void Update(Guid id, Rect bounds)`, `bool Remove(Guid id)`, `void Query(Rect area, List<Guid> results)` (caller-owned list, no allocation), `void HitCandidates(Point p, double tolerance, List<Guid> results)` returned top-most first by z-order, `void Nearest(Point p, double maxDistance, int k, List<Guid> results)` for snapping (§11), `Rect Extent`.
  - `RTreeIndex` (own R*-tree, node capacity 16, STR bulk load on open) in the same folder; `DocumentSpatialIndex` subscribes to the document's element added, removed, and bounds-changed events so no caller updates it by hand; it indexes `GetVisualBounds()` (stroke, markers, effects) with `GetGeometricBounds()` kept for alignment.
  - Consumers rewired in this section: `SkiaRenderer` culls by viewport `Query`, `SelectionManager.HitTestAndSelect` and `SelectInRect` use `HitCandidates` and `Query`, `SnapManager` object candidates use `Nearest`; the old full-list walks are deleted.
  - Dirty regions: `DirtyRegionTracker` unions old and new visual bounds per change; `SkiaCanvas` clips redraw to the dirty rect; each top-level element caches an `SKPicture` keyed by `Id` plus a change version, invalidated by the document's change events (no allocation per frame, `standards/shared.md`).
  - Rendering keys: `Nodus.Render.Gpu` (true; `SKGLElement` with a `GRContext`, falling back to `SKElement` with a Warning when context creation fails), `Nodus.Render.AntiAlias` (true), `Nodus.Render.LivePreviewWhileDragging` (true; off draws an outline during drags), `Nodus.Render.NavigationPreview` (`HideForMouse` default, `Always`, `Never`), each consumed by `SkiaCanvas` and toggled from View or Preferences.
  - Large documents: `VectorDocument.ScaleFactor` (1 or 10, the Large Canvas option) persisted as `nodus:scale` in the §1 document block and applied to displayed units; the artboard and page model (§3) is proven with 1,000 artboards.
  - `LongOperation` in `Photon.Nodus.Desktop/Services/` runs any job expected to exceed one second on a worker with `CancellationToken` and `IProgress<double>` into the status strip; Save snapshots the model to an `XDocument` on the UI thread and writes through `AtomicFileWriter` on the worker so editing continues (CD-196), with a completion line in the status strip.
  - Bitmap drag previews (CD-184) draw the cached decoded `SKImage` under the live transform instead of resampling per frame.
  - Refresh Window (Ctrl+W) drops the picture cache and redraws, logged.
  - Benchmarks: `tests/Photon.Nodus.Benchmarks/` (BenchmarkDotNet, new package decision recorded) over a generated 10,000-element and 1,000-artboard document: viewport render under 16 ms, hit test under 1 ms, open under 2 s on the reference machine, numbers committed in the section's stamp.
  - Tests: `RTreeIndexTests` (insert, update, remove, query equals brute force on 5,000 random rects), `DirtyRegionTrackerTests`, `LongOperationTests` (cancel leaves the document unchanged).
- **Proof:** Unit test `RTreeIndexTests.QueryMatchesBruteForce` plus a driven run on the 10,000-element fixture with the frame-time log quoted before and after; cheaper substitute that fails: a uniform grid bucket that the random-size brute-force comparison and the 1,000-artboard benchmark expose.

#### §3. Pages and artboards: one model, the Artboards and Pages panel, and artboard commands

- **Deliverable:** One page model that is both an Illustrator artboard and a CorelDRAW page, persisted through §1, with the artboard tool, the Artboards and Pages panel, Page Size and Artboard Options dialogs, and every artboard command as an undoable step. -> SOURCE: legacy-nodus-4.6
- **Depends On:** §1, D02 T06 §7
- **Phase:** 4
- **Surface:** Artboards and Pages panel, Artboard tool, Artboard Options and Page Size dialogs, artboard context menu, on-canvas labels. Fidelity: new build, no baseline; captured to docs/captures/nodus/artboards/. Job: a designer can create, size, arrange, rename, reorder, and delete pages or artboards and keep their art with them. Treatment: a panel list with number, name, size, and lock columns, edge plus buttons on the active artboard, and labels renamable in place. Cheaper substitute that fails: a list of rectangles drawn on a layer. Chrome: consume AvalonDock panels, the icon catalog, the settings store, and the suite history; do not add a second list control.
- **Runs:** `Requires: display-session -- the artboard tool, panel drag reorder, and label rename need an interactive desktop`
- **Catalog:** NP-0003 to NP-0031 (29 features)
- **Hints:**
  - Promoted from backlog B-004 (`-> SOURCE: legacy-nodus-4.6`); delete the B-004 line from `todo/backlog.md` in the authoring commit; B-011 (print) keeps its `needs: B-004` rewritten to this section.
  - Model: `Page` replaces `Artboard` in `Photon.Nodus.Core/Models/Page.cs` (name, bounds, orientation, background color, locked, video settings, per-page size flag), `VectorDocument.Pages` owns them with an `ActivePage`; `ArtboardManager` becomes `PageManager` over the document and its arrange math is kept.
  - Persistence: pages write as `<nodus:page>` in the §1 document block and also as Inkscape 1.2+ `<inkscape:page>` elements in `sodipodi:namedview` so Inkscape opens the same pages; the reader accepts either, and `SvgRoundTripTests` gains a three-page fixture with an Inkscape golden.
  - Commands, one each in `Photon.Nodus.Core/Commands/Pages/`: New, Duplicate (with contents), Delete, Delete Empty, Rename (many at once with a numbered pattern), Reorder, Rearrange (grid by row or column, left-to-right or right-to-left, columns, spacing, move artwork), Fit to Artwork Bounds, Fit to Selected Art, Convert to Artboards, Switch Orientation, Set Size (current page or all pages), Lock Content, each with one Information log line.
  - `ArtboardTool` (Shift+O) in `Photon.Nodus.Core/Tools/`: draw, select by click, Shift, or marquee, move with the Move/Copy Artwork option, resize with Scale Artwork, Alt-drag duplicate, Ctrl+D repeat the last artboard action, edge plus buttons, cut, copy, and paste artboards through the `D02 T03 §3` clipboard with contents.
  - Artboard Options dialog: preset, width, height, orientation, X, Y, background color, show center mark, cross hairs, video safe areas, pixel aspect ratio, fade outside, update while dragging (`Nodus.Artboard.*` view keys).
  - Page Size dialog and property-bar boxes: presets from one `PagePresets` table (moved from `ArtboardPresets`; print sizes in points at 72 per inch corrected to document units at 96 DPI), custom sizes up to 1,800 by 1,800 inches, save and delete custom presets in `Nodus.Page.CustomPresets`, Get From Printer through `System.Printing.LocalPrintServer` default queue (refused by name with no printer).
  - Panel: `PagesPanelViewModel` rows (number, name, size, lock), drag reorder, inline rename, find by name, context menu (Duplicate, Rename, Lock, Delete, Export deferred to D02 T14 §15 by name), empty-artboard badge.
  - Canvas: on-canvas labels with double-click rename, active page highlight border, per-artboard background color, paste onto selected artboards (extends `D02 T07 §13`'s Paste on All Artboards).
  - Tests: `PageCommandTests` (each command and undo), `PageSerializationTests` (nodus and inkscape forms), `ArtboardToolTests` (marquee select, repeat).
- **Proof:** Format fidelity proof over `tests/fixtures/nodus/pages/three-pages.svg` (reopened pages equal by name, bounds, order, and background; Inkscape shows three pages, version quoted) plus a driven run creating, reordering, and undoing artboards with log lines quoted; cheaper substitute that fails: pages kept in memory only, which the reopen comparison catches.

#### §4. Multipage views, page background, page numbers, and page navigation

- **Deliverable:** CorelDRAW-style single and multipage views with grid, vertical, horizontal, and free-form layouts, page border, bleed, and printable area display, page backgrounds, page numbering fields, the document navigator, and every page insert, duplicate, delete, rename, and go-to command.
- **Depends On:** §3
- **Phase:** 4
- **Surface:** Document navigator strip under the canvas, Multipage View Settings in the Pages panel, Page Background dialog, Insert Page, Duplicate Page, Delete Page, Go to Page, Insert Page Number, and Page Number Settings dialogs. Fidelity: new build, no baseline; captured to docs/captures/nodus/pages/. Job: a designer can lay out and navigate a multipage document and number its pages. Treatment: page tabs with add-page buttons, pages laid out on one canvas in multipage view, page numbers as live fields. Cheaper substitute that fails: page numbers typed as static text. Chrome: consume the §3 panel, the icon catalog, and Photon.UI dialog styles; do not add a second page list.
- **Runs:** `Requires: display-session -- navigator, multipage layout, and interactive page resize need an interactive desktop`
- **Catalog:** NP-0032 to NP-0061 (30 features)
- **Hints:**
  - `PageLayoutService` in `Photon.Nodus.Core/Pages/` computes page origins for `Single`, `Grid` (columns, spacing), `Vertical`, `Horizontal`, and `Custom` (free positions stored per page) plus facing-page spreads (start on left or right), stored in the §1 document block; `Nodus.Pages.DefaultViewMode` sets new documents.
  - Multipage view renders all pages through the §2 index; single page view shows only the active page; Zoom to Selected Pages and Show Spreads in thumbnails use the same layout.
  - Interactive resize: page-label handles drag like a rectangle (Shift from center) as one `SetPageSizeCommand`; Autofit Page fits content on local layers with a margin.
  - Display toggles (View, Page): page border, bleed (amount in the §1 document block as `nodus:bleed`, shared with D02 T13 §4), printable area from the default printer's imageable area, each a `Nodus.View.*` key; Add Page Frame creates a page-sized rectangle command.
  - Page background: none, solid color, or bitmap (linked path or embedded data URI, tiled default size or custom H and V with aspect lock), with Print and Export Background feeding `D02 T04 §3` and `D02 T04 §4`; written as `<nodus:background>` plus a fallback `<rect>` in a locked `nodus:role="background"` group.
  - Commands: Insert Page (count, before or after, size, orientation), Insert Before or After from tab and label menus, New Page button, Duplicate Page (layers only or with contents, or to a new document named after the page), Delete Page (one, a range with Through, or the panel selection), Rename Page, Go to Page, find page by name; each one undo step.
  - Page numbers: `PageNumberField` is a live text run (a §1 kind `pagenumber`) rendering the page's number, style from `Page Number Settings` (Arabic, Roman, letters, start number); Insert Page Number on the active layer, all pages, odd, or even pages places it on a master layer (§5); hiding it on one page uses §5's Show Master Layers on Pages flag.
  - Document navigator: first, previous, next, last, page tabs with add buttons, and the Pages panel list or grid thumbnails with a size slider.
  - Tests: `PageLayoutServiceTests` (each layout and spreads), `PageNumberFieldTests` (renumber after reorder), `PageCommandTests` extensions.
- **Proof:** Unit tests `PageNumberFieldTests.RenumbersAfterReorder` and `PageLayoutServiceTests` plus a fidelity round trip of a four-page fixture with a bitmap background and page numbers; cheaper substitute that fails: static number text, which the reorder test catches.

#### §5. Layer options, sublayers, master layers, lock and hide commands, and the Objects panel

- **Deliverable:** Layers become part of the document model with sublayers, Layer Options, master layers, and every lock, hide, move, merge, collect, and release command, surfaced in an Objects panel tree of pages, layers, and objects that replaces the `D02 T02 §6` list.
- **Depends On:** §3, D02 T06 §7
- **Phase:** 4
- **Surface:** The Objects panel (tree, search, options menu), Layer Options dialog, Object, Lock and Hide submenus. Fidelity: docs/captures/nodus/main-window/ for the panel dock, new captures to docs/captures/nodus/objects-panel/. Job: a designer can organize, find, lock, hide, and restructure layers and objects. Treatment: one tree (pages, layers, sublayers, groups, objects) with eye, lock, print, and color columns and a target circle. Cheaper substitute that fails: a flat list with an indent. Chrome: consume the `D02 T06 §7` layer tree control, the icon catalog, and the suite history; do not build a second tree.
- **Runs:** `Requires: display-session -- panel drag, search, and per-layer view need an interactive desktop`
- **Catalog:** NP-0096 to NP-0135 (40 features)
- **Hints:**
  - Model: `VectorDocument.Layers` (from the existing `Layer` class) with per-page local layers and document master layers (`MasterScope` All, Odd, Even), a default layer per new page, an `ActiveLayer`; written as `<g nodus:layer="..." inkscape:groupmode="layer">` so Inkscape shows them as layers.
  - Layer Options dialog: name, color, template (locked, dimmed by percent, non-printing), show, preview or outline, lock, print, export, dim images; `LayerOptionsCommand` one step.
  - Commands in `Photon.Nodus.Core/Commands/Layers/`: New Layer, New Sublayer, Duplicate, Delete, Delete Empty, Copy and Paste Layer, Move to Layer, Copy to Layer, Merge Selected, Flatten Artwork, Collect in New Layer, Release to Layers (Sequence, Build), Reverse Order, Change Layer To master or local.
  - Lock and hide set: Lock Selection (Ctrl+2), All Artwork Above, Other Layers, Lock All Deselected, Unlock All (Alt+Ctrl+2); Hide Selection (Ctrl+3), All Artwork Above, Other Layers, Hide Unselected, Show All (Alt+Ctrl+3); panel Hide, Outline, Lock Others; each one step, keys through the `D02 T02 §8` keymap.
  - Per-layer outline or wireframe (Ctrl-click eye) drives the §12 view-mode renderer per layer; layer color tints the selection bounding box and nodes.
  - Objects panel view model `ObjectsPanelViewModel` over pages, layers, and objects with two views (Layers and Objects, or Pages, Layers, and Objects), drag to reorder, drag onto a group to group, fully expand on Ctrl+click, Locate Object and Expand to Show Selection, search and filter by name and type, thumbnail size slider, Panel Options (row size, show thumbnails).
  - Options flags as settings with consumers: `Nodus.Objects.EditAcrossLayers`, `Nodus.Objects.SelectActivatesLayer`, `Nodus.Objects.KeepDesktopObjectsOnLayer`, `Nodus.Objects.ShowMasterLayersOnPages` (read by §4 page numbers), `Nodus.Objects.PasteRemembersLayers` (read by §13).
  - Print and export toggles feed `D02 T04 §3`, `D02 T04 §4`, and later D02 T13 §2 through one `Layer.IsPrintable` and `Layer.IsExportable` check.
  - Tests: `LayerCommandTests` (each command and undo), `MasterLayerTests` (odd and even placement), `ObjectsPanelViewModelTests` (search, locate), and a layered SVG fixture round trip read by Inkscape.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/layers/master-and-sublayers.svg` (layers, sublayers, master scopes, lock and print flags equal after reopen; Inkscape shows the layers, version quoted) plus `LayerCommandTests`; cheaper substitute that fails: layers as plain named groups, which the master-scope and print-flag assertions catch.

#### §6. Selection: the Select menu, Select Same, magic wand, lasso, and saved selections

- **Deliverable:** The full Select menu (All on Active Artboard, Deselect, Reselect, Inverse, Next Above and Below, Same, Object, Save and Edit Selection), the magic wand, lasso, and group selection tools, Corel selection groups, and the modifier behaviors of the selection tool, all reading the `D02 T02 §3` owner.
- **Depends On:** D02 T05 §4
- **Phase:** 4
- **Surface:** Select menu, Magic Wand panel, Lasso and Group Selection tools, Edit Selection dialog. Fidelity: docs/captures/nodus/main-window/ for the menu, new captures to docs/captures/nodus/selection/. Job: a designer can select exactly the objects they mean by attribute, shape, region, or saved set. Treatment: Select Same over a comparer per attribute with tolerances. Cheaper substitute that fails: Select Same matching exact color strings only. Chrome: consume `SelectionManager`, the keymap, and the §2 index; do not add a second selection store.
- **Runs:** `Requires: display-session -- lasso, magic wand, and modifier clicks on the canvas need an interactive desktop`
- **Catalog:** NP-0149 to NP-0183 (35 features)
- **Hints:**
  - `SelectionQueries` in `Photon.Nodus.Core/Selection/` returns element sets for Same (Appearance, Appearance Attribute, Graphic Style, Blending Mode, Fill and Stroke, Fill Color, Opacity, Stroke Color, Stroke Weight, Shape, Symbol Instance, Link Block Series, and the seven Text variants) and Object (All on Same Layers, Direction Handles, Brush Strokes, Clipping Masks, Stray Points, All Text, Point Type, Area Type, Not Aligned to Pixel Grid); kinds whose feature lands later (graphic styles D02 T09 §15, brushes D02 T09 §16, text types D02 T10 §2) return empty and stay enabled.
  - Select menu commands: All on Active Artboard (Ctrl+Alt+A), Deselect (Shift+Ctrl+A), Reselect (Ctrl+6, repeats the last Same or Object query), Inverse, Next Object Above and Below (Alt+Ctrl+] and [).
  - `MagicWandTool` (Y) with a Magic Wand panel: fill color, stroke color, stroke weight, opacity with tolerances, blending mode, Use All Layers, stored as `Nodus.MagicWand.*`.
  - `LassoTool` (Q) and the freehand pick share `LassoSelector` (polygon containment against node positions or bounds through the §2 index); Group Selection tool adds the next enclosing group on each click.
  - Selection tool modifiers: E while dragging selects only fully enclosed, Alt switches to touching, Ctrl+click twice or Alt+click selects behind, Ctrl+click selects inside a group, Tab and Shift+Tab cycle, hold Ctrl for the temporary selection tool, Space toggles the pick tool, Ctrl+` returns to the last selection tool; skip shadows and effect bounds (`Nodus.Selection.IgnoreEffectBounds`).
  - Saved selections: Save Selection and Edit Selection (rename, delete) stored as `<nodus:selection>` in the §1 document block; Corel selection groups Ctrl+0 to 9 assign, digit recalls, digit twice zooms, Alt+digit adds, stored alongside.
  - Global Edit: Start Global Edit selects objects matching the chosen one by appearance and size within the chosen artboards, and edits apply as one composite command.
  - Bounding box: View, Hide or Show Bounding Box (Shift+Ctrl+B) as `Nodus.View.BoundingBox`; Object, Transform, Reset Bounding Box re-aligns a rotated element's box as one command.
  - Objects panel target circle (§5 when present, otherwise the `D02 T02 §6` list) selects the row's contents.
  - Tests: `SelectionQueriesTests` (one per query with tolerances), `LassoSelectorTests`, `SavedSelectionTests` (survives save and reopen).
- **Proof:** Unit tests `SelectionQueriesTests` and `SavedSelectionTests.RoundTrips` plus a driven magic-wand and lasso run with log lines quoted; cheaper substitute that fails: exact-match Select Same, which the tolerance tests catch.

#### §7. Isolation mode and focus mode

- **Deliverable:** One isolation mode that serves as Illustrator isolation and CorelDRAW Focus mode: enter by double-click or command, dim everything else, a breadcrumb bar, step out by level, new objects join the isolated group, and exit.
- **Depends On:** §5
- **Phase:** 4
- **Surface:** The isolation breadcrumb bar at the canvas top-left and Edit, Bring into Focus and Exit commands. Fidelity: new build, no baseline; captured to docs/captures/nodus/isolation/. Job: a designer can edit inside a nested group without disturbing the rest. Treatment: dimmed surroundings with an adjustable overlay and a clickable path of group names. Cheaper substitute that fails: locking every other object, which leaves the layer tree changed. Chrome: consume the canvas overlay layer, the theme, and the Objects panel; do not add a second tree view.
- **Runs:** `Requires: display-session -- double-click entry and the breadcrumb need an interactive desktop`
- **Catalog:** NP-0136 to NP-0143 (8 features)
- **Hints:**
  - `IsolationState` per document (D02 T06 §7 scope) holding the isolated container path; it is view state, not a document edit, so entering and exiting write no history, but edits inside are normal commands.
  - Entry: double-click a group with the selection tool (`Nodus.Isolation.DoubleClickEnters`, true), Edit, Bring into Focus, Isolate Selected Group from the context and Objects panel menus; exit with Shift+Esc, double-click outside, or Exit; Esc steps up one level.
  - Hit testing, marquee, Select All, and snapping (§11 within isolated objects) restrict to the isolated container through a filter on the §2 index queries.
  - Dimming: `Nodus.Isolation.OverlayOpacity` (percent) and `Nodus.Isolation.InactiveVisibility` (dim, hide, normal) consumed by `SkiaRenderer`.
  - Breadcrumb bar lists document, layer, and each nested group; clicking a level moves isolation there.
  - New objects drawn while isolated are inserted into the isolated container; the Objects panel shows the focus container highlighted.
  - Rules: groups, symbols in edit mode (D02 T06 §11), compound paths, clipping groups, and text on a path can be isolated; locked or hidden containers are refused with a status message naming the reason.
  - Tests: `IsolationStateTests` (enter, step up, exit, new element lands in container, hit test filter).
- **Proof:** Unit test `IsolationStateTests.NewElementJoinsIsolatedGroup` plus a driven run isolating a nested group, drawing inside, exiting, and saving (the saved group holds the new element, quoted); cheaper substitute that fails: lock-everything-else, which the Objects panel lock state exposes.

#### §8. The Properties panel and the contextual property bar

- **Deliverable:** A contextual property bar whose template follows the active tool and selection, a Properties panel with document, transform, appearance, and quick-action sections plus Corel scroll and tab modes, and one numeric field control with math, units, stepping, and scroll protection, every edit an undo step. -> SOURCE: legacy-nodus-2.5
- **Depends On:** D02 T05 §4
- **Phase:** 4
- **Surface:** The property bar under the menu, the Properties panel, and the contextual task bar. Fidelity: docs/captures/nodus/main-window/ for the existing context toolbar and properties panel, new captures to docs/captures/nodus/property-bar/. Job: a designer can read and set the exact values of whatever tool or selection is active. Treatment: templates keyed by tool and selection kind. Cheaper substitute that fails: one static toolbar with disabled boxes. Chrome: consume the `CompactNumberBox` control (moved to `Photon.UI` when Imago needs it), the theme, and `D02 T03 §4` property commands; do not add a second numeric box.
- **Runs:** `Requires: display-session -- template switching and field entry need an interactive desktop`
- **Catalog:** NP-2537 to NP-2550 (14 features)
- **Hints:**
  - Promoted from backlog B-005 (`-> SOURCE: legacy-nodus-2.5`); delete the B-005 line from `todo/backlog.md` in the authoring commit.
  - `PropertyBarTemplateSelector` in `Photon.Nodus.Desktop/Views/PropertyBar/` picks a template from (active tool, selection kind): no selection shows page size, orientation, units, and nudge (§3, §9, §13); a selection shows X, Y, W, H, scale factor percent with lock ratio, rotation; tools contribute their options (each later tool registers a template).
  - Position, size, and scale boxes write through `D02 T03 §4` `PropertyChangeCommand` with the reference point from the Transform panel default (center).
  - `CompactNumberBox` gains math (`+ - * /` and parentheses with units such as `10mm+2pt`, evaluated by `UnitExpression` in `Photon.Nodus.Core/Units/`), Up and Down steps (Shift for ten), Shift+Enter applies and keeps focus, Alt+Enter applies as a copy, and ignores the mouse wheel unless focused (`Nodus.Fields.WheelNeedsFocus`, true).
  - Properties panel `PropertiesPanelViewModel` sections: Document (with no selection: page, units, rulers and grid toggles, preferences shortcut), Transform, Appearance summary, Curve (node count, closed, path length for paths), Quick Actions (context buttons such as Expand, Group, Isolate, Arrange), with scroll mode or tab mode (`Nodus.Properties.Mode`) and style indicators marking values that override a style.
  - Contextual task bar: a floating bar near the selection with the three most likely next commands per selection kind, toggled by `Nodus.View.ContextualTaskBar`.
  - The Control panel of Illustrator maps to the property bar; do not build two bars.
  - Tests: `UnitExpressionTests`, `PropertyBarTemplateSelectorTests` (tool and selection matrix), `CompactNumberBoxTests` (wheel refusal unfocused, Shift+Enter).
- **Proof:** Unit tests `UnitExpressionTests` (`10mm+2pt` equals 39.4583 px at 96 DPI) and `PropertyBarTemplateSelectorTests` plus a driven run typing `50%*2` into width and undoing it (log quoted); cheaper substitute that fails: a static bar, which the template-selector tests catch.

#### §9. Rulers, units, drawing scale, and grids

- **Deliverable:** Rulers with global or artboard origin, units, tick divisions, calibration, and video rulers; document units preferences; a drawing scale; and the document grid, pixel grid, baseline grid, and transparency grid, all persisted per document or in settings.
- **Depends On:** §3
- **Phase:** 4
- **Surface:** Rulers on the canvas with a right-click units menu, View, Rulers and Grid toggles, Document Options Rulers and Grid pages, Drawing Scale dialog. Fidelity: docs/captures/nodus/main-window/ for the canvas rulers, new captures to docs/captures/nodus/rulers-grids/. Job: a designer can measure and lay out in the units and scale of the job. Treatment: units flow from one `UnitConverter` into rulers, fields, and the HUD. Cheaper substitute that fails: rulers in pixels only with a label. Chrome: consume `SkiaRenderer.RenderRulers` and `RenderGrid` (extended, not replaced) and the settings store; do not add a second units table.
- **Runs:** `Requires: display-session -- ruler interaction and grid display need an interactive desktop`
- **Catalog:** NP-0238 to NP-0253 (16 features)
- **Hints:**
  - `UnitConverter` in `Photon.Nodus.Core/Units/` (px, pt, pc, in, mm, cm, m, ft, yd, Q, and user units under a drawing scale) is the only conversion path for rulers, `CompactNumberBox`, the §2 HUD, and exporters; `Nodus.Units.General`, `Nodus.Units.Stroke`, `Nodus.Units.Type`, and `Nodus.Units.NumbersWithoutUnitsArePoints` are settings with those consumers.
  - Document ruler state in the §1 document block: units, origin (global or per artboard, AI-0868), tick divisions, drawing scale (for example 1 mm = 1 m), written as `nodus:rulers` and `nodus:scale`.
  - Rulers: Ctrl+R toggle, right-click units menu, drag the corner to set origin and double-click to reset, video rulers when an artboard has video settings (§3), separate show state for desktop and tablet mode (`Nodus.Rulers.ShowInTabletMode`), Calibrate Rulers dialog that sets `Nodus.Rulers.ScreenDpi` from a measured on-screen length so 100 percent matches a physical ruler.
  - Document grid: show (Ctrl+'), lines or dots, spacing and subdivisions, color, grids in back (`nodus:grid` in the document block); snap to grid stays the `D02 T02 §7` toggle.
  - Pixel grid: shown from 800 percent zoom, color and opacity keys, Align Page with Pixel Grid rounds page origins to whole pixels as one command.
  - Baseline grid: spacing, start, color, show toggle; consumed by §11 snap to baseline grid and D02 T10 §6.
  - Transparency grid (Shift+Ctrl+D): checkerboard behind artboards, size and colors as settings.
  - Tests: `UnitConverterTests` (every pair, drawing scale), `UnitExpressionTests` reuse, `RulerStateSerializationTests`.
- **Proof:** Unit tests `UnitConverterTests` and `RulerStateSerializationTests` (drawing scale and origin survive reopen) plus a driven run switching ruler units and origin with a capture; cheaper substitute that fails: a units label over pixel rulers, which the drawing-scale conversion test catches.

#### §10. Guides, the Guides panel, the measure tool, and the Info panel

- **Deliverable:** Guides move into the document (horizontal, vertical, angled, object guides, artboard-level or document-wide) with lock, hide, clear, color, and presets, a Guides panel for numeric entry, a measure tool for distance, angle, and area that writes nothing, and an Info panel. -> SOURCE: legacy-nodus-3.7-3.8
- **Depends On:** §9
- **Phase:** 4
- **Surface:** Guides panel, Measure tool, Info panel, View, Guides submenu. Fidelity: new build, no baseline; captured to docs/captures/nodus/guides/ and docs/captures/nodus/info-panel/. Job: a designer can place exact guides and read exact measurements. Treatment: guides are document objects on a guides layer with numeric editing. Cheaper substitute that fails: guides kept in `SnapManager` memory, which a reopen loses. Chrome: consume the §9 `UnitConverter`, the `D02 T06 §12` HUD label style, and AvalonDock panels; do not add a second measurement readout.
- **Runs:** `Requires: display-session -- dragging guides from rulers and the measure tool need an interactive desktop`
- **Catalog:** NP-0254 to NP-0267 (14 features)
- **Hints:**
  - Promoted from backlog B-007 (`-> SOURCE: legacy-nodus-3.7-3.8`); delete the B-007 line from `todo/backlog.md` in the authoring commit and repoint the `D02 T06` Adjacency reason that cites it.
  - `Guide` gains `Angle`, `Scope` (document or a page id), `IsLocked`, color and style; the list moves from `SnapManager._guides` to `VectorDocument.Guides`, written as `<nodus:guide>` in the §1 document block and as Inkscape `sodipodi:guide` elements for interop.
  - Commands: Add, Move, Rotate, Delete, Lock, Unlock, Clear Guides, Make Guides (Ctrl+5, object outlines become object guides), Release Guides, Select All Guides; one step each.
  - Ruler drag creates a guide (Alt switches orientation), dropped inside an artboard it is artboard-level, outside document-wide (`Nodus.Guides.ArtboardLevelOnDrop`); Show and Hide (Ctrl+;) and Lock (Alt+Ctrl+;) are `Nodus.View.Guides*` keys.
  - Guides panel `GuidesPanelViewModel`: type (horizontal, vertical, angled by two points or angle), numeric position in current units, list with select, move, rotate, delete, lock, color and line style, show guides at drawing scale; presets (built-in margins, columns, grid, and user-defined saved to `Nodus.Guides.Presets`).
  - `MeasureTool` (on the eyedropper flyout): click-drag measures distance and angle, Shift-click builds an area polygon with Shift-click exclusions, results in the Info panel and on the HUD, and the tool records no command.
  - Info panel `InfoPanelViewModel`: cursor X and Y, selection X, Y, W, H, rotation, path length, area (Area Options: units and whether holes subtract), fill and stroke summary, measure-tool results.
  - Tests: `GuideCommandTests`, `GuideSerializationTests` (nodus and sodipodi forms), `MeasureToolTests` (distance, angle, area with exclusion equal to known polygons, no history entry).
- **Proof:** Format fidelity proof over `tests/fixtures/nodus/guides/angled-and-artboard.svg` (guides equal after reopen; Inkscape shows them, version quoted) plus `MeasureToolTests.AreaWithExclusion`; cheaper substitute that fails: in-memory guides, which the reopen comparison catches.

#### §11. Snapping modes, smart guides, and dynamic and alignment guides

- **Deliverable:** `SnapManager` grows from grid, guides, and objects into the full mode set (node, endpoint, midpoint, center, quadrant, intersection, tangent, perpendicular, edge, text baseline, page, pixel, baseline grid, self), smart guides with labels and spacing and distance guides, Corel dynamic and alignment guides, and the Live Guides panel, each mode a setting.
- **Depends On:** §10, D02 T02 §7
- **Phase:** 4
- **Surface:** View, Snap To submenu, the snapping quick-access menu on the property bar, the Live Guides panel, and canvas overlays. Fidelity: docs/captures/nodus/main-window/ for the menu, new captures to docs/captures/nodus/snapping/. Job: a designer can land a point exactly on the geometry they mean and see why it snapped. Treatment: every candidate names its mode in a screen tip and draws its mark. Cheaper substitute that fails: bounding-box snapping labeled as point snapping. Chrome: consume the canvas overlay, the theme accent, the §2 index `Nearest`, and the `D02 T02 §7` toggles; do not add a second snap engine.
- **Runs:** `Requires: display-session -- snapping feedback during drags needs an interactive desktop`
- **Catalog:** NP-0268 to NP-0307 (40 features)
- **Hints:**
  - `SnapMode` flags in `Photon.Nodus.Core/Snapping/` replace `SnapTarget` (Grid, Guides, Objects kept) adding Node, Endpoint, Midpoint, Center, Quadrant, Intersection, Tangent, Perpendicular, Edge, TextBaseline, Page, Pixel, BaselineGrid, Self; each a `Nodus.Snap.<Mode>` key, all read through one `SnapSettings`.
  - Candidate providers, one class per geometry family: `NodeSnapProvider` (nodes, endpoints, midpoints, centers, quadrants), `IntersectionSnapProvider` (segment intersections within the §2 query window), `TangentSnapProvider` and `PerpendicularSnapProvider` (relative to the drag origin), `EdgeSnapProvider`, `PageSnapProvider`, `PixelSnapProvider`, `BaselineSnapProvider`; the manager ranks by screen distance then mode priority.
  - Global controls: Snap Off (Alt+Q) and the toolbar toggle, hold Q to suspend for one drag, snapping radius `Nodus.Snap.RadiusPx`, snap to self (Ctrl+Shift+H), only within the active artboard, only to isolated objects (§7), snap to last location.
  - Feedback: snap marks per mode, screen tips naming the mode (`Nodus.Snap.ShowScreenTips`), consumed by the overlay renderer.
  - Smart guides (Ctrl+U) as `SmartGuideProvider`: object and alignment guides, anchor and path labels, object highlighting, measurement labels, transform-tool guides, equal spacing guides, distance guides, construction guides at up to six angles, tolerance, glyph guides (fed by D02 T10 §5 when present); preferences keys `Nodus.SmartGuides.*`.
  - Corel dynamic guides (Shift+Alt+D) as `DynamicGuideProvider`: angles and custom angles, extend along segment, tick spacing, intersection placement, a snap point queue of recent points, line style and color; alignment guides (Shift+Alt+A) as `AlignmentGuideProvider`: edges, centers, individual objects in a group, margins, intelligent spacing and dimensioning, line style and color.
  - Live Guides panel `LiveGuidesPanelViewModel` over the dynamic and alignment guide keys; automatic alignment toggle on the toolbar; the quick-access menu lists every mode with a check.
  - Budget: candidate search under 2 ms per mouse move on the 10,000-element fixture from §2.
  - Tests: `SnapProviderTests` (one per provider with known geometry), `SmartGuideProviderTests` (equal spacing among three objects), `SnapBenchmark` in the §2 benchmark project.
- **Proof:** Unit tests `SnapProviderTests` (tangent from an external point to a circle lands on the analytic tangent point within 1e-6) plus a driven drag with each mode's screen tip captured; cheaper substitute that fails: bounds-only snapping, which the tangent and intersection tests catch.

#### §12. View modes, zoom commands, rotate view, saved views, and document windows

- **Deliverable:** Every view mode (outline and wireframe, simple wireframe, draft, normal, enhanced, trim, presentation, screen modes, full-screen preview, preview selected only), the full zoom and pan command set with its preferences, rotate view, saved views, and document window arrangement.
- **Depends On:** §2
- **Phase:** 4
- **Surface:** View menu, Window menu, Zoom tool property bar, zoom levels list, Views panel, screen modes. Fidelity: docs/captures/nodus/main-window/ for menus, new captures to docs/captures/nodus/view-modes/. Job: a designer can see the document the way the task needs and get anywhere in it fast. Treatment: view state per window, never written to history. Cheaper substitute that fails: outline mode as zero-width strokes on the real renderer. Chrome: consume `CanvasState`, the keymap, AvalonDock windows from D02 T06 §7, and the settings store; do not add a second zoom model.
- **Runs:** `Requires: display-session -- view modes, zoom, rotation, and window arrangement need an interactive desktop`
- **Catalog:** NP-0197 to NP-0237 (41 features)
- **Hints:**
  - `ViewMode` enum in `CanvasState` (Normal, Enhanced, Draft, Outline, SimpleWireframe) with a renderer strategy per mode in `SkiaRenderer` (outline draws geometry at 1 px with no fills or effects; draft skips effects and bitmap quality; enhanced enables full anti-aliasing and bitmap high quality); Ctrl+Y toggles Outline, Shift+F9 toggles the previous mode, `Nodus.View.DefaultMode` for new documents.
  - Trim view clips to artboards; Presentation Mode shows one artboard full screen with arrow navigation; screen modes (F) cycle normal, full screen with menu, full screen; Full-screen Preview (F9) in normal or enhanced (`Nodus.View.FullScreenPreviewMode`); Preview Selected Only.
  - Zoom commands in `ZoomCommands`: In, Out, To Selection, To All Objects (fit all), To Page and Fit Artboard, To All Pages, Page Width, Page Height, Actual Size (Ctrl+1), zoom levels list box, zoom relative to 1:1 using the §9 calibrated DPI, animated zoom (`Nodus.Zoom.Animated`).
  - Mouse and pan preferences: wheel default action zoom or scroll, center mouse when zooming, zoom rate and alternate (Ctrl+Shift) rate, right-click action of the zoom and pan tools, scroll bars toggle, middle-button quick pan and Space pan kept from `D02 T02 §8`.
  - Rotate View tool (Shift+H) and View, Rotate View presets, Reset, Rotate View to Selection; `CanvasState.Rotation` applied in the view matrix, hit testing and rulers stay correct.
  - Show and hide toggles as `Nodus.View.*` keys: edges (Ctrl+H), artboards, template layers, gradient annotator (D02 T09 §8), corner widget (D02 T08 §4), bounding box (§6).
  - Saved views: New View and Edit Views with the Views panel (zoom, center, rotation, page, view mode) stored as `<nodus:view>` in the §1 document block.
  - Windows: New Window on the same document sharing its scope (D02 T06 §7), Cascade, Tile Horizontally and Vertically, Arrange Icons, undock a document, window list, Close Window, tabbed documents toggle.
  - Text zoom controls (CD-183) scale text readability in the text editing overlay without changing the document zoom, a `Nodus.View.TextZoom` key.
  - Tests: `ZoomCommandsTests` (each fit command against known bounds and rotation), `ViewModeRendererTests` (outline pixel golden), `SavedViewTests` (round trip).
- **Proof:** Unit tests `ZoomCommandsTests` and a committed outline-mode pixel golden in `ViewModeRendererTests` within 1/255, plus a driven run of each view mode with captures; cheaper substitute that fails: outline as hairline strokes over fills, which the pixel golden catches.

#### §13. History panel, repeat, paste variants, and quick duplicates

- **Deliverable:** A History panel over the suite history with click-to-jump and a configurable depth, Repeat, Paste in Front, Back, in Place, on All Artboards, without Formatting, Paste Special, paste remembering layers, and the quick-duplicate gestures and nudge distances.
- **Depends On:** D02 T05 §4
- **Phase:** 4
- **Surface:** History panel, Edit menu additions, right-drag drop menu. Fidelity: docs/captures/nodus/main-window/ for the Edit menu, new captures to docs/captures/nodus/history-panel/. Job: a designer can step back to any earlier state and duplicate or paste exactly where they need. Treatment: the panel lists history entries by description with the current state marked; clicking jumps by undoing or redoing to it. Cheaper substitute that fails: a panel that only displays descriptions. Chrome: consume the `D01 T02 §4` history, the `D02 T03 §3` clipboard service, and the keymap; do not add a second undo stack.
- **Runs:** `Requires: display-session -- panel jumps, drag duplicates, and paste placement need an interactive desktop`
- **Catalog:** NP-0312 to NP-0326 (15 features)
- **Hints:**
  - `HistoryPanelViewModel` over the suite history's `Changed` event: rows with description and time, current row marked, click jumps (a sequence of Undo or Redo), depth `Nodus.History.Levels` consumed by the history limit.
  - Repeat (Ctrl+R in the Corel keymap set, Transform Again stays D02 T08 §12) re-executes the last repeatable command on the current selection through an `IRepeatableCommand.CloneFor(selection)`.
  - Paste variants in `ClipboardService` placement: Paste in Front (Ctrl+F) and Paste in Back (Ctrl+B) relative to the selected object, Paste in Place (Shift+Ctrl+V), Paste on All Artboards (Alt+Shift+Ctrl+V, same offset per artboard), Paste Without Formatting (plain text into text objects), Paste Special listing the clipboard formats present; Paste Remembers Layers reads `Nodus.Objects.PasteRemembersLayers`.
  - Quick duplicates: Alt-drag duplicate, Space drops a copy during a drag, right-click during a drag drops a copy, numeric keypad plus duplicates in place, each one command.
  - Right-drag menu on drop: Move Here, Copy Here, Copy Fill Here, Copy Outline Here, Copy All Properties, Cancel.
  - Move while drawing: right mouse button (or Space) repositions a shape or line during creation; the shape tools consult a shared `DrawGestureState`.
  - Nudge: arrow keys, Ctrl micro, Shift super, distances `Nodus.Nudge.Distance`, `Nodus.Nudge.Micro`, `Nodus.Nudge.Super` in document units (also on the no-selection property bar, §8); consecutive nudges merge into one history entry within the `D01 T02 §4` merge window.
  - Duplicate offset `Nodus.Duplicate.OffsetX` and `OffsetY` replaces the fixed 10 units from `D02 T03 §3`.
  - Tests: `HistoryPanelViewModelTests` (jump back three, forward two), `PasteVariantsTests` (z-order and position per variant), `NudgeTests` (merge).
- **Proof:** Unit tests `PasteVariantsTests` and `HistoryPanelViewModelTests.JumpRestoresState` plus a driven History panel jump with log lines quoted; cheaper substitute that fails: a read-only history list, which the jump test catches.

#### §14. The New Document dialog, document presets, templates, and document information

- **Deliverable:** A New Document dialog with presets, pages, units, size, orientation, color mode, resolution, bleed, and profiles; saved presets; templates with a browser, Save as Template, and open for editing; Document Setup; document information metadata; and Save a Copy, Save Selected Only, Revert, Close All, and locked-file handling.
- **Depends On:** §3
- **Phase:** 4
- **Surface:** New Document dialog with a Templates tab, New from Template browser, Save as Template dialog, Document Setup dialog, Document Information dialog. Fidelity: new build, no baseline; captured to docs/captures/nodus/new-document/ and docs/captures/nodus/templates/. Job: a designer can start the right document in one step and describe it for whoever receives it. Treatment: preset categories on the left, details on the right, blank templates as tiles. Cheaper substitute that fails: a width and height prompt. Chrome: consume `Photon.UI` dialog styles, the settings store, `D02 T04 §1` save paths, and the icon catalog; do not add a second file writer.
- **Runs:** `Requires: display-session -- the dialogs and template browser need an interactive desktop`
- **Catalog:** NP-0062 to NP-0089 (28 features)
- **Hints:**
  - `DocumentSettings` record in `Photon.Nodus.Core/Documents/` (name, page count, units, width, height, orientation, color mode RGB or CMYK, rendering resolution, bleed, RGB, CMYK, and gray profile names, rendering intent, page view mode, scale factor from §2); `DocumentFactory.Create(settings)` builds pages (§3) and layers (§5) as one path used by the dialog, New without Dialog (Alt+Ctrl+N), and templates.
  - Presets: built-in Print, Web, Mobile and Devices, Social, Film and Video, Art and Illustration in `DocumentPresets` with paper types, custom presets saved and deleted in `Nodus.NewDocument.Presets`; Do Not Show Again sets `Nodus.NewDocument.ShowDialog`.
  - Color mode and profiles are recorded in the §1 document block now and consumed by D02 T09 §1 and D02 T13 §1 when they land.
  - Templates: `.svgt` files (SVG with a `<nodus:template>` block carrying name, category, designer notes); Save as Template writes one with template properties; New from Template opens a copy (untitled, with or without contents); Open for Editing opens the template itself; import styles from a template waits for D02 T09 §15 and is disabled with that name.
  - Template browser `TemplateBrowserViewModel`: local folders from `Nodus.Templates.Folders` (add, alias, rename, remove, browse recursively, reindex into a cached index under `%LOCALAPPDATA%\Rizonesoft\Nodus\templates-index.json`), search, category filter, sort, favorites, thumbnail size slider, details pane, properties, delete to the Recycle Bin; unreadable folders are listed with the refusal reason.
  - Document Setup (Alt+Ctrl+P) and Document Options: edits units, bleed, rendering resolution, type options (stored for D02 T10 §2), as one `DocumentSetupCommand`.
  - Document information (File Info, Document Properties, Save As comments and tags): title, author, subject, keywords, rating, notes, tags written to SVG `<title>`, `<metadata>` RDF with Dublin Core, and an XMP packet, read back by the importer; it replaces today's `Title`, `Author`, `Description`, and `License` setters.
  - File commands: Save a Copy (Alt+Ctrl+S) and Save As another registered format, Save Selected Only, Revert (F12, prompts, reloads from disk), Close All; locked or read-only targets refused by name through `D02 T04 §1` with Save As offered.
  - Tests: `DocumentFactoryTests` (each preset), `TemplateRoundTripTests`, `DocumentInfoMetadataTests` (Dublin Core and XMP round trip, Inkscape reads the title and keywords).
- **Proof:** Format fidelity proof over `tests/fixtures/nodus/metadata/doc-info.svg` and a `.svgt` template (metadata and template block equal after reopen; Inkscape's Document Metadata shows the title and keywords, version quoted) plus `DocumentFactoryTests`; cheaper substitute that fails: metadata kept only in memory, which the reopen comparison catches.

#### Sizing concerns

- §5 carries 40 catalog features (lock and hide set, layer commands, master layers, Objects panel); the hints group them into about 28 items, which leaves no room for rework, so the implementer should treat the lock and hide set as one item with numbered sub-steps.
- §11 carries 40 catalog features across about 14 snap modes plus smart, dynamic, and alignment guides; grouping by provider class keeps it near 26 items, but the Corel dynamic and alignment guide providers are the natural split if it overruns.
- §12 carries 41 catalog features; grouping by view modes, zoom commands, preferences, rotate view, toggles, saved views, and windows keeps it near 25 items, with windows the natural split if it overruns.
- §6 carries 35 catalog features; the Select Same and Select Object queries are one `SelectionQueries` class and count as two items.

### todo/02-nodus/TODO-08-nodus-parity-paths.md -- `nodus-parity-paths`

- **Title:** "TODO-08 -- Nodus Parity: Drawing, Paths, Shapes, Shaping, and Transform"
- **Phase(s):** 5
- **Goal:** Give Nodus the full drawing and geometry toolset of Illustrator 30.8 and CorelDRAW 2026: every pen, curve, freehand, and shape tool; parametric live shapes and corners; node-level editing, cutting, and shaping brushes; the complete Pathfinder and shaping set with compound paths and clipping; numeric and interactive transforms, align, arrange, and step and repeat; and associative dimensions and connectors, each edit one undoable command and every live object persisted through the `nodus:` namespace with a plain-SVG fallback.
- **Current-state facts to verify (with claim candidates):**
  - Nine tools derive from `ToolBase` today (select, pen, node edit, rectangle, ellipse, line, text, pan, zoom); there is no polygon, star, spiral, pencil, knife, eraser, transform, dimension, or connector tool. `<!-- claim: count ": ToolBase" src/Nodus/Bezier.Core/Tools/*.cs = 9 -->`
  - No polygon tool file exists. `<!-- claim: absent src/Nodus/Bezier.Core/Tools/PolygonTool.cs -->`
  - No pencil tool file exists. `<!-- claim: absent src/Nodus/Bezier.Core/Tools/PencilTool.cs -->`
  - The pen tool is one 453-line file with Escape, Enter, and Backspace handling and no rubber band, continue, or auto add/delete. `<!-- claim: lines src/Nodus/Bezier.Core/Tools/PenTool.cs = 453 -->`
  - The node edit tool is one 700-line file; keys 1, 2, 3 convert nodes to corner, smooth, symmetric. `<!-- claim: lines src/Nodus/Bezier.Core/Tools/NodeEditTool.cs = 700 -->`
  - `ControlPointType` has exactly three node types (Corner, Smooth, Symmetric). `<!-- claim: count "^    (Corner|Smooth|Symmetric),?$" src/Nodus/Bezier.Core/Models/ControlPoint.cs = 3 -->`
  - `PathOperationsService` has nine public operations and nine placeholder bodies (offset, simplify, stroke to path, bounds, split, flatten among them). `<!-- claim: count "Placeholder" src/Nodus/Bezier.Core/Services/PathOperationsService.cs = 9 -->`
  - `ToolPoint` carries only X and Y: no pressure, tilt, or bearing reaches a tool. `<!-- claim: count "Pressure" src/Nodus/Bezier.Core/Interfaces/ITool.cs = 0 -->`
  - `SvgClipPath` and `SvgMask` model classes exist but the SVG parser never reads `clipPath` and the renderer never clips. `<!-- claim: count "clipPath" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->` `<!-- claim: count "SvgClipPath" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->`
  - `AlignmentService` is ten static methods (align, distribute, gap distribution, combined bounds, offsets) and `TransformService` is 201 lines of resize, rotate, snap-angle, and scale math. `<!-- claim: count "public static" src/Nodus/Bezier.Core/Services/AlignmentService.cs = 10 -->` `<!-- claim: lines src/Nodus/Bezier.Core/Services/TransformService.cs = 201 -->`
  - No connector code exists in core services or tools. `<!-- claim: count "Connector" src/Nodus/Bezier.Core/Services/*.cs = 0 -->`
  - The Object menu's Transform submenu holds only the fixed 90 and 180 degree rotations and the two flips. `<!-- claim: count "Rotate _180" src/Nodus/Bezier.Desktop/Views/MainWindowView.xaml = 1 -->`
- **Inputs and XREFs:** consumes `D02 T06 §2` (continue, join, break, reverse, simplify, stroke to path: the node model every section here extends), `D02 T02 §4` (align, arrange, rotate, flip wired with `CompositeCommand`), `D02 T02 §5` (booleans on `SKPath.Op`, `ElementToPathConverter`), `D02 T03 §1` (resize and rotate drags recorded as undo steps), `D02 T07 §1` (the live-object contract), `D02 T07 §8` (the Properties panel and contextual property bar that host every tool option), `D02 T07 §9` (units and drawing scale for dimensions), `D02 T07 §6` (Select Same and deep select, the selection half of B-006), `D02 T07 §11` (snapping modes the drawing tools consume), `D01 T02 §2` (settings store), `D01 T02 §4` (suite history); consumed by `D02 T09 §16` (brush engine on §3 strokes), `D02 T11 §12` (PowerClip on §11 clipping), `D02 T11 §17` and `D02 T11 §19` (Live Paint and pathfinder effects on §10), `D02 T14 §10` (DXF dimensions from §15), `D02 T16 §8` (pen, touch, and dial input preferences over the stylus fields §3 adds); promotes backlog B-001 (source legacy-nodus-3.2) into §4, B-002 (legacy-nodus-1.6-4.4) into §11, B-006 (legacy-nodus-3.1) into §12, B-008 (legacy-nodus-3.6) into §3.
- **Adjacency:** list=applicable (the Common Shapes picker, Coordinates object list, and Pathfinder operation list are findable by name; tool search rides `D02 T16 §3`); document=not-applicable (this file produces geometry; printing and PDF output are `D02 T13 §2` and `D02 T13 §14`); settings=applicable (every tool default, the constrain angle, node display, eraser and knife defaults, dimension and connector defaults go through the settings store with a named reading tool); reporting=applicable (the status bar length, angle, and node count readouts of §2 and §6; the Clean Up result count of §7); notifications=applicable (Pathfinder, Shape Builder, Divide Objects Below, and Step and Repeat over a second report progress and completion on the status strip with cancel); permissions=applicable (locked layers and locked objects refuse shaping, cutting, and reordering with a named status message; §14 owns the locked layer order rule); audit=applicable (every tool stroke, node edit, shaping operation, and transform is one named history entry and one Serilog Information line); exchange=applicable (live shapes, compound shapes, clipping, intertwine, dimensions, and connectors round-trip through SVG with `nodus:` parameters and plain fallbacks; paths paste as SVG between documents); reverse=applicable (every create has undo; Expand Shape, Release Compound Path, Release Clipping Mask, Release Intertwine, Break Dimension Apart, Break Callout Apart, and Clear Transformations are the explicit reverses).

#### §1. Pen, Bezier, and anchor point tools

- **Deliverable:** The pen tool with rubber-band preview, Space-move, Alt anchor conversion, auto add and delete, continue and connect, a Bezier drawing mode, the Add, Delete, and Anchor Point tools, angle constraint, node tracking, and their defaults.
- **Depends On:** D02 T06 §2
- **Phase:** 5
- **Surface:** Fidelity: extends the canvas and tool rail, `docs/captures/nodus/main-window/`, plus `docs/captures/nodus/pen-tool/` for the overlay states. Job: a designer can draw and correct Bezier paths node by node without switching tools. Treatment: live rubber band and handle overlays drawn by the tool's `RenderOverlay`, one command per finished path; cheaper substitute that fails: committing each click as its own element. Chrome: consume the tool rail flyout, `D02 T07 §8` property bar, shared icon catalog, and history; do not add a second options strip.
- **Runs:** `Requires: display-session -- pen drawing, hover add/delete, and overlay captures need an interactive desktop`
- **Catalog:** NP-0331 to NP-0344 (14 features)
- **Hints:**
  - Extend `src/Nodus/Photon.Nodus.Core/Tools/PenTool.cs` with a rubber-band preview segment from the last anchor to the pointer, on by default, setting `nodus.tools.pen.rubberBand`.
  - Space held during a drag moves the anchor being placed (`PenTool.OnMouseMove` offsets the pending `ControlPoint`); Alt held converts or breaks the current handle as the Anchor Point tool does.
  - Auto add/delete on hover: hit-test segments and anchors of the selected path through the `D02 T06 §2` node model; setting `nodus.tools.pen.autoAddDelete` (default true), Shift suspends it.
  - Continue and connect: clicking an open endpoint of any path continues it; closing onto another path's endpoint joins the two through the `D02 T06 §2` join operation as one `CompositeCommand`.
  - Bezier mode (`PenMode.Bezier`): click places a straight node, drag pulls handles, double-click the last node forces the next segment straight, Space finishes, matching CorelDRAW's Bezier tool without a second engine.
  - `AddAnchorPointTool`, `DeleteAnchorPointTool`, `AnchorPointTool` in `Photon.Nodus.Core/Tools/`, registered in the Pen flyout with `+`, `-`, Shift+C.
  - Constrain: Shift (and Ctrl for CorelDRAW keymaps) snaps segment and handle angles to `nodus.tools.constrainAngle` (default 15) through `TransformService.SnapAngle`.
  - Node tracking: `nodus.tools.nodeTracking` lets pen, Bezier, and select tools grab a hovered node; `nodus.tools.hideBoundingBoxAfterCurve` hides the selection box after curve tools.
  - Freehand/Bezier defaults (smoothing, corner threshold, straight-line threshold, auto-join distance) as one settings group `nodus.tools.curve.*`, read by §1, §2, §3.
  - Tests: `tests/Photon.Nodus.Tests/Tools/PenToolParityTests.cs` covers rubber band state, Space-move, auto add/delete node counts, continue, join, and constrain angles; `AnchorPointToolTests` covers convert and break.
- **Proof:** Unit test (`PenToolParityTests`, `AnchorPointToolTests`) plus a driven run that draws, continues, and joins two paths with undo restoring each step (log lines quoted, capture under `docs/captures/nodus/pen-tool/`); cheaper substitute that fails: a join that groups the two paths, which the node-count assertion catches.

#### §2. Curvature, B-spline, polyline, 3-point curve, line and arc tools, and parallel drawing

- **Deliverable:** The curvature, line segment, arc, 2-point line (with perpendicular and tangential modes), B-spline, polyline, and 3-point curve tools, auto-close, a length and angle readout, and CorelDRAW's parallel drawing mode.
- **Depends On:** §1
- **Phase:** 5
- **Surface:** Fidelity: tool rail flyouts and property bar, `docs/captures/nodus/main-window/`, new dialogs under `docs/captures/nodus/line-arc-options/`. Job: a designer can draw precise lines, arcs, and smooth curves by the method each shape suits. Treatment: each tool owns its overlay and writes one path command; parallel mode writes the source and its offsets as one entry; cheaper substitute that fails: parallel lines drawn as a stroke effect that does not produce separate editable paths. Chrome: consume the `D02 T07 §8` property bar, status bar readout slot, and history.
- **Runs:** `Requires: display-session -- driving each drawing tool and capturing its overlay needs an interactive desktop`
- **Catalog:** NP-0345 to NP-0364 (20 features)
- **Hints:**
  - `CurvatureTool`: interpolating curve through clicked points (Catmull-Rom converted to cubic Beziers), double-click or Alt-click for a corner, drag an existing point to move it.
  - `LineSegmentTool` and `ArcTool` with click-for-options dialogs (`LineSegmentOptionsDialog`: length, angle, fill; `ArcOptionsDialog`: X and Y lengths, open or closed, base axis, slope, fill) and drag modifiers C, F, and arrows.
  - The arc tool closes the arc part of backlog B-001 (`-> SOURCE: legacy-nodus-3.2`); the other B-001 shapes land in §4.
  - `TwoPointLineTool` with perpendicular and tangential modes built on the `D02 T07 §11` perpendicular and tangent snap points; Ctrl extends past the target.
  - `BSplineTool` in `Photon.Nodus.Core/Tools/`: uniform cubic B-spline converted to Bezier segments for rendering; V while clicking clamps a point; the control polygon is stored as `nodus:bspline` so `§6` can edit it (live-object contract `D02 T07 §1`).
  - `PolylineTool`: click straight, drag curve, Alt draws circular arcs, Ctrl+Alt constrains the arc angle, double-click finishes.
  - `ThreePointCurveTool`: start, end, then bend point; Ctrl circular, Shift symmetrical.
  - Auto-close toggle on the property bar (`nodus.tools.curve.autoClose`) and a status bar readout of segment length, angle, and total length in document units from `D02 T07 §9`.
  - Parallel drawing mode (`ParallelDrawingOptions`: count, left, right, both, distance, preview) applied through `PathOperationsService.Offset` after each supported tool finishes; `Create parallel from selected` adds offsets to an existing open path.
  - Tests: `CurvatureToolTests`, `BSplineConversionTests` (control points to Bezier within 0.01 px of a reference evaluation), `PolylineArcTests`, `ThreePointCurveTests`, `ParallelDrawingTests` (offset distance measured at five sample points).
- **Proof:** Unit tests above plus a driven run drawing one of each tool with parallel mode on (capture under `docs/captures/nodus/line-arc-options/`, log lines quoted); cheaper substitute that fails: arcs approximated by polylines, which `ArcGeometryTests` catches by checking the radius at sampled points.

#### §3. Pencil, freehand, smooth, path eraser, join tool, and smart drawing

- **Deliverable:** The pencil and freehand tool with curve fitting, straight segments, extend and connect, erase-back, the Smooth, Path Eraser, and Join tools, shape recognition drawing with the Shaper group, and LiveSketch, all driven by stylus pressure where the input has it.
- **Depends On:** §1
- **Phase:** 5
- **Surface:** Fidelity: tool rail and property bar, `docs/captures/nodus/main-window/`, recognition overlays under `docs/captures/nodus/freehand/`. Job: a designer can sketch by hand and get clean, editable curves and shapes. Treatment: raw input points kept until release (or the LiveSketch timer) then fitted to cubics as one command; cheaper substitute that fails: storing the raw polyline, which the node-count bound catches. Chrome: consume the property bar, the stylus input service, and history; do not build a private stroke recorder in the view.
- **Runs:** `Requires: display-session -- freehand strokes and stylus input need an interactive desktop`
- **Catalog:** NP-0365 to NP-0387 (23 features)
- **Hints:**
  - Promotes backlog B-008 (`-> SOURCE: legacy-nodus-3.6`): the pencil and path eraser land here, the object eraser in §8, and the variable-width brush in `D02 T09 §17`.
  - Add `Pressure`, `Tilt`, and `Bearing` to `ToolPoint` in `Photon.Nodus.Core/Interfaces/ITool.cs`, filled from WPF `StylusPoint` in the canvas input path, defaulting to 1.0 and 0 for mouse input; `D02 T16 §8` reads them for preferences.
  - `Photon.Nodus.Core/Geometry/CurveFitter.cs`: Schneider's least-squares cubic fitting (Graphics Gems, 1990) with an error tolerance mapped from the fidelity or smoothing slider and corner detection by angle threshold.
  - `PencilTool` (Corel Freehand keymap alias): Alt or click-click draws straight, Shift constrains 45, drawing near a selected path's end extends it, drawing over it reshapes it, ending on another end joins; Shift-drag backward erases back; options dialog with `nodus.tools.pencil.*` keys.
  - Live preview: the fitted curve and the element's stroke style render while drawing (`nodus.tools.pencil.livePreview`, default true).
  - `SmoothTool` (refit the scrubbed span with a looser tolerance), `PathEraserTool` (split and remove the scrubbed span), `JoinTool` (scrub over a gap or overlap to extend or trim both ends and join).
  - `Photon.Nodus.Core/Geometry/ShapeRecognizer.cs`: a local recognizer (corner detection plus least-squares fits for line, rectangle, ellipse, triangle, polygon; scribble detection for delete and merge), recognition level and delay settings, no model and no network.
  - Shaper group: the recognizer's merge and punch results persist as a live group (`nodus:shaper`) whose faces can be edited and restored through `D02 T07 §1`.
  - Smart drawing options: recognition level, smart smoothing, outline width, delay 10 ms to 2 s, Esc removes the last curve.
  - `LiveSketchTool`: pending strokes merged after the timer (0 to 5 s), include existing curves within 0 to 40 px, single-curve mode, preview, smoothing, stylus eraser flip, and inherited properties; it reuses `CurveFitter`, no neural network (brief routing rule).
  - Tests: `CurveFitterTests` against a committed input trace under `tests/fixtures/nodus/input-traces/` (max deviation and node-count bound), `ShapeRecognizerTests` (ten recorded gestures to expected shape kinds), `PencilToolTests`, `LiveSketchTests`.
- **Proof:** Unit tests replaying the committed input traces, plus a driven stylus or mouse run whose fitted result is saved and inspected (node count quoted); cheaper substitute that fails: keeping every raw input point, which the node-count bound catches.

#### §4. Live shapes: rectangle, ellipse, polygon, star, spiral, and live corners

- **Deliverable:** Parametric live rectangle, rounded rectangle, 3-point rectangle and ellipse, ellipse with pie and arc, polygon, star (perfect and complex), and spiral with on-canvas widgets, Shape Properties, Convert to Shapes and Expand Shape, live corners on any path with the Corners panel, and the Coordinates panel for numeric creation.
- **Depends On:** D02 T07 §1, D02 T07 §8
- **Phase:** 5
- **Surface:** Fidelity: tool rail, canvas widgets, and property bar, `docs/captures/nodus/main-window/`; new panels under `docs/captures/nodus/corners-panel/` and `docs/captures/nodus/coordinates-panel/`. Job: a designer can draw shapes that stay editable by their parameters and set them by number. Treatment: shapes stored as live objects with parameters and expanded geometry; cheaper substitute that fails: a polygon written as a plain path that loses its side count on reopen. Chrome: consume `D02 T07 §8` Properties panel for Shape Properties, the shared number boxes, dock, and history; do not build a second property grid.
- **Runs:** `Requires: display-session -- widget dragging and panel captures need an interactive desktop`
- **Catalog:** NP-0388 to NP-0425 (38 features)
- **Hints:**
  - Promotes backlog B-001 (`-> SOURCE: legacy-nodus-3.2`): polygon, star, and spiral with parameters editable after creation land here (arc in §2), now persisted through `D02 T07 §1` rather than `data-nodus-*` attributes.
  - `Photon.Nodus.Core/Shapes/LiveShape.cs` hierarchy (`LiveRect` with per-corner type and radius, `LiveEllipse` with start and end angle, arc or pie, direction, `LivePolygon`, `LiveStar` with inner and outer radius, sharpness, complex flag, `LiveSpiral` with revolutions, decay, logarithmic expansion); `SvgRect` and `SvgEllipse` stay native where no extra parameter is set.
  - Tools: `RectangleTool` and `EllipseTool` extended, new `RoundedRectangleTool`, `ThreePointRectangleTool`, `ThreePointEllipseTool`, `PolygonTool`, `StarTool`, `SpiralTool`; modifiers per `standards/nodus.md` (Shift constrains, Alt from center, Space moves while drawing), double-click the rectangle tool for a page-sized rectangle.
  - Click without dragging opens `ShapeOptionsDialog` for exact size, radius, sides, points, or spiral values.
  - Widgets: `LiveShapeWidgetOverlay` draws pie handles, side-count and point-count handles, inner radius handles, and corner widgets; dragging a polygon node symmetrically reshapes it into a star.
  - Live corners on any path: `CornerSet` (round, inverted round, chamfer; absolute or relative rounding; per-corner or together; scale with object) stored as `nodus:corners` with the expanded path as fallback; hide widget above `nodus.selection.cornerWidgetMaxAngle`.
  - Corners panel (`CornersPanel.xaml`): fillet, scallop, chamfer (A and B distances with lock) applied to selected corners of any curve, skipping corners whose segments are too short and smooth or symmetrical nodes.
  - Convert to Shapes (recognize rect, ellipse, regular polygon within tolerance) and Expand Shape (live to plain path) as undoable commands.
  - Coordinates panel (`CoordinatesPanel.xaml`): rectangle, square, ellipse, circle, polygon, regular polygon, star, complex star, 2-point line, multi-point curve with Create or Replace, origin selector, live preview, and set-by-click buttons.
  - Tests: `LiveShapeRoundTripTests` (each shape saved and reopened keeps every parameter), `CornerGeometryTests` (fillet arc radius, chamfer distances, skip rule), `CoordinatesPanelTests` (view model builds the exact geometry for typed values).
  - Format fidelity: `tests/fixtures/nodus/svg/live-shapes/` opened, saved, reopened, compared element by element; the expanded fallback rendered by Inkscape (version recorded) matches within 0.5 px.
- **Proof:** Format fidelity proof on the live-shapes fixture, unit tests above, and a driven run dragging each widget with undo (captures under `docs/captures/nodus/corners-panel/` and `docs/captures/nodus/coordinates-panel/`); cheaper substitute that fails: writing only the expanded path, which the reopen parameter assertion catches.

#### §5. Grid, graph paper, flare, common shapes, and impact tools

- **Deliverable:** Rectangular and polar grid tools with options and modifiers, graph paper, the flare tool, the Common Shapes tool with glyph handles and text inside, and the Impact tool with every style, boundary, width, spacing, and randomization option.
- **Depends On:** §4
- **Phase:** 5
- **Surface:** Fidelity: tool rail, property bar, option dialogs, and the common shapes picker, `docs/captures/nodus/main-window/` and `docs/captures/nodus/common-shapes/`. Job: a designer can generate grids, flares, stock shapes, and comic impact lines as editable objects. Treatment: each generator is a live object with parameters and an expanded group fallback; cheaper substitute that fails: a raster flare or impact bitmap. Chrome: consume the property bar, shared picker and number box controls, palette click behavior from `D02 T09 §4`, and history.
- **Runs:** `Requires: display-session -- generator tools and picker captures need an interactive desktop`
- **Catalog:** NP-0426 to NP-0443 (18 features)
- **Hints:**
  - `RectangularGridTool` and `PolarGridTool` with `GridOptionsDialog` values (size, dividers, skew, frame, fill, compound ellipses) and live modifiers (arrows add or remove dividers, F, V, X, C skew in 10 percent steps).
  - `GraphPaperTool`: columns and rows, Shift from center, Ctrl square cells; output is a group of rectangles that Ungroup splits.
  - `FlareTool` with `FlareOptionsDialog` (center, halo, rays, rings) as a live `nodus:flare` object whose fallback is a group of gradient-filled vector shapes.
  - `CommonShapesTool` and a picker of basic, arrow, flowchart, banner, and callout families defined in `Photon.Nodus.Core/Shapes/CommonShapes/` with parametric glyph handles.
  - Text inside a common shape uses the shape as an area-text frame through `D02 T10 §8` once it ships; until then the item names that owner.
  - `ImpactTool` producing a live `nodus:impact` object: radial or parallel style, inner and outer boundary references, rotation, random start and end, width min, max, steps, randomize, spacing min, max, steps, randomize, line style, widest point.
  - Impact color: palette click sets fill, right-click sets outline, through the palette bar command from `D02 T09 §4`; Break Impact Shape Apart expands to editable paths.
  - Randomization is seeded and the seed stored in the live parameters so reopen reproduces the same lines.
  - Tests: `GridGeneratorTests` (divider counts and skew positions), `ImpactGeneratorTests` (same seed gives identical geometry; boundaries respected), `CommonShapeGlyphTests`.
  - Budget: an impact effect with 1,000 lines regenerates under 50 ms on parameter change.
- **Proof:** Unit tests above plus format fidelity on `tests/fixtures/nodus/svg/generators/` (reopen keeps parameters and seed; Inkscape renders the fallback); cheaper substitute that fails: an unseeded random that changes on reopen, which the identical-geometry test catches.

#### §6. Node editing: node types, node transforms, align, distribute, and reduce

- **Deliverable:** The direct selection and shape tool at parity: node types, handle and segment dragging, node selection modes and navigation, add, delete, reduce, convert line and curve, smoothness, node transforms and reflection, node align and distribute, subpaths, B-spline control points, Convert to Curves, and node display preferences.
- **Depends On:** D02 T06 §2
- **Phase:** 5
- **Surface:** Fidelity: canvas node overlay and property bar, `docs/captures/nodus/main-window/` and `docs/captures/nodus/node-editing/`. Job: a designer can reshape any path precisely at the node level. Treatment: each node operation is one `PathEditCommand` capturing before and after node lists, node shapes by type (circle smooth, square cusp, diamond symmetrical); cheaper substitute that fails: rebuilding the path from flattened points and losing node types. Chrome: consume the `D02 T06 §2` node model, the property bar, `D02 T02 §4` align commands, and history.
- **Runs:** `Requires: display-session -- node dragging and overlay captures need an interactive desktop`
- **Catalog:** NP-0444 to NP-0476 (33 features)
- **Hints:**
  - Extend `NodeEditTool` (Direct Selection, Corel Shape tool keymap alias) with segment drag that adjusts both adjacent handles, handle drag with Alt moving the node too, and `nodus.selection.highlightAnchorsOnHover`.
  - Node types corner (cusp), smooth, symmetrical on the property bar with C and S key toggles; show or hide handles for multiple anchors; node glyph shapes by type; `nodus.selection.nodeColorsSwapped` (Ctrl+Shift+I).
  - Selection: rectangular and freehand node marquee, Ctrl toggles, Shift selects a consecutive run, Select All Nodes, Tab and Shift+Tab next and previous.
  - Add, delete, and remove anchors keeping the path; anchor X and Y fields in the `D02 T07 §8` property bar for the selected nodes.
  - Convert to line, convert to curve, curve smoothness slider (refit selected segments), Reduce Nodes (drop nodes within tolerance), and Convert to Curves for shapes and text (text through `D02 T10 §2` outlines once it ships).
  - Node transforms: stretch or scale and rotate or skew selected nodes with their own handle set; reflect node edits horizontally or vertically onto mirrored counterparts.
  - Node align (left, right, top, bottom, centers) to active nodes, page edge, page center, grid, or a typed point, and node distribute by span or exact spacing, reusing `AlignmentService` math over node positions.
  - Subpaths: extract subpath to its own object, copy, cut, and duplicate selected segments as new objects; holes follow the fill rule from §11.
  - B-spline control points (from §2's `nodus:bspline`): float or clamp, add by double-clicking the control line, delete by double-clicking a point, Shift multi-select.
  - Tests: `NodeTypeTests`, `NodeTransformTests` (scale, rotate, skew of selected nodes against expected coordinates), `NodeAlignTests`, `ReduceNodesTests` (node count drops and max deviation under tolerance), `BSplineEditTests`, extending `tests/Photon.Nodus.Tests/Tools/NodeEditToolTests.cs`.
- **Proof:** Unit tests above plus a driven run converting, aligning, and scaling nodes on a fixture path with undo restoring exact coordinates (log lines quoted); cheaper substitute that fails: flattening to a polyline, which `NodeTypeTests` catches by asserting preserved handle types.

#### §7. Join curves, average, offset path, add anchors, clean up, and split into grid

- **Deliverable:** Average, corner or smooth join, Offset Path, advanced Simplify and the smooth slider, Add and Remove Anchor Points, Divide Objects Below, Split Into Grid, Clean Up, extend curve to close, copy paths between documents, and the Join Curves panel with extend, chamfer, fillet, and Bezier modes.
- **Depends On:** §6
- **Phase:** 5
- **Surface:** Fidelity: Path menu and dialogs, `docs/captures/nodus/main-window/`; Join Curves panel and Offset, Simplify, Split Into Grid dialogs under `docs/captures/nodus/path-commands/`. Job: a designer can repair, offset, and subdivide paths with one command each. Treatment: each command is one history entry with a preview in its dialog; cheaper substitute that fails: Offset Path implemented as a thicker stroke. Chrome: consume the Path menu, shared dialog chrome, dock, and history.
- **Runs:** `Requires: display-session -- dialog previews and the Join Curves panel need an interactive desktop`
- **Catalog:** NP-0477 to NP-0494 (18 features)
- **Hints:**
  - Replace the `Offset` placeholder in `Photon.Nodus.Core/Services/PathOperationsService.cs`: stroke outline via `SKPaint.GetFillPath` at twice the distance with miter, round, or bevel joins and miter limit, then keep the outer or inner contour with `SKPath.Op`; the `Offset Path` dialog previews live.
  - Average (horizontal, vertical, both) and corner or smooth join (Shift+Ctrl+Alt+J) on the `D02 T06 §2` join.
  - Simplify advanced options on top of the `D02 T06 §2` simplify: curve precision, corner angle threshold, convert to straight lines, show original overlay, remember auto-simplify; plus the contextual smooth slider.
  - Add Anchor Points (midpoint of each segment) and Remove Anchor Points (keep path) commands.
  - Divide Objects Below: cut every unlocked object under the selected path with `SKPath.Op` and delete the cutter, one `CompositeCommand`.
  - Split Into Grid dialog: rows, columns, gutters, heights, widths, add guides (guides through `D02 T07 §10`).
  - Clean Up: remove stray points, unpainted objects, and empty text paths; report counts on the status strip.
  - Join Curves panel (`JoinCurvesPanel.xaml`): gap tolerance and modes extend to intersection, chamfer, fillet with radius, Bezier connection; extend curve to close joins two selected end nodes with a straight segment.
  - Copy paths between documents as SVG fragments on the clipboard (the suite clipboard format from `D02 T03 §3`); Photoshop path export is noted as Imago's side.
  - Tests: `OffsetPathTests` (offset of a 100 px square by 10 gives 120 px bounds; round join area within 0.5 percent), `JoinCurvesTests` per mode, `SplitIntoGridTests`, `CleanUpTests`, `DivideObjectsBelowTests`.
- **Proof:** Unit tests above plus a driven run of each dialog with preview and undo (capture under `docs/captures/nodus/path-commands/`); cheaper substitute that fails: offset as a wider stroke, which the bounds assertion on the resulting path catches.

#### §8. Knife, scissors, eraser, virtual segment delete, and the crop tool

- **Deliverable:** Scissors, the knife in freehand, 2-point, and Bezier modes with cut span and outline options, the object eraser with nib, pressure, and reduce-nodes options, virtual segment delete, and the crop tool on vector artwork.
- **Depends On:** §6
- **Phase:** 5
- **Surface:** Fidelity: tool rail flyout and property bar, `docs/captures/nodus/main-window/` and `docs/captures/nodus/cutting-tools/`. Job: a designer can cut, erase, and crop vector artwork directly on the canvas. Treatment: each cut or erase stroke is one command producing closed, filled paths; cheaper substitute that fails: an eraser that paints a white shape over the art. Chrome: consume the property bar, the §3 stylus fields, and history.
- **Runs:** `Requires: display-session -- cutting and erasing strokes need an interactive desktop`
- **Catalog:** NP-0495 to NP-0512 (18 features)
- **Hints:**
  - `ScissorsTool`: split a path at a clicked anchor or segment point via `PathOperationsService.SplitPath` (placeholder today, replaced here).
  - `KnifeTool`: freehand, 2-point (Shift+Ctrl constrains 15), and Bezier modes cycled with A; closed shapes split into closed pieces, cut span gap or overlap of set width, outline options automatic, convert to objects, keep outlines.
  - `EraserTool`: nib size, round or square shape, angle and roundness, pressure, tilt, and bearing from the §3 `ToolPoint` fields; erase is `SKPath.Op` difference with the swept nib outline; straight-line erase (click, click, Ctrl constrains) and double-click area erase; stylus eraser end switches to it.
  - Eraser reduce nodes (default on) and default thickness as `nodus.tools.eraser.*` settings; this is B-008's eraser (`-> SOURCE: legacy-nodus-3.6`, owned by §3).
  - `VirtualSegmentDeleteTool`: delete a segment between intersections on click, many by marquee or an Alt-drawn curve, Shift welds overlapping end points into one node.
  - `CropTool`: crop rectangle with position, size, and rotation on the property bar, Enter crops every unlocked object with `SKPath.Op` intersection, Esc or Clear removes the area; text and live effects are converted to curves first with a status line naming each.
  - Knife and crop on bitmaps defer to `D02 T12 §1` with that ref in the disabled state.
  - Tests: `KnifeToolTests` (a square cut by a diagonal gives two closed paths whose areas sum to the original, gap mode reduces the sum by width times length), `EraserToolTests`, `VirtualSegmentDeleteTests`, `CropToolTests`.
  - Budget: an eraser stroke across a 5,000-node path stays interactive (preview under 16 ms per dab, commit on mouse-up).
- **Proof:** Unit tests above plus a driven run knifing, erasing, and cropping a fixture with undo (capture under `docs/captures/nodus/cutting-tools/`); cheaper substitute that fails: painting background-colored shapes, which the area-sum assertion catches.

#### §9. Liquify and shape-editing brushes

- **Deliverable:** Warp, Twirl, Pucker and Bloat (attract and repel), Scallop, Crystallize, and Wrinkle liquify tools and CorelDRAW's Smooth, Smear, Smudge, and Roughen brushes, with nib, rate, pressure, dryout, tilt, bearing, and control range settings.
- **Depends On:** §6
- **Phase:** 5
- **Surface:** Fidelity: tool rail flyout, property bar, and Liquify options dialog, `docs/captures/nodus/main-window/` and `docs/captures/nodus/shape-brushes/`. Job: a designer can push, twist, and roughen outlines organically with a brush. Treatment: dabs displace or insert nodes along the path each tick, the whole drag recorded as one command on mouse-up; cheaper substitute that fails: a live warp effect that leaves the path's nodes unchanged. Chrome: consume the property bar, the §3 stylus fields, the shared brush cursor overlay, and history.
- **Runs:** `Requires: display-session -- brush drags and stylus input need an interactive desktop`
- **Catalog:** NP-0513 to NP-0535 (23 features)
- **Hints:**
  - `Photon.Nodus.Core/Tools/Shaping/ShapeBrushBase.cs`: nib radius, rate, falloff, pressure mapping, detail (node insertion density), simplify after stroke; dryout, tilt, and bearing inputs from the §3 `ToolPoint` fields.
  - Liquify tools: `WarpTool` (drag displacement), `TwirlTool` (rotation about the nib, clockwise or counterclockwise, rate), `AttractRepelTool` (Pucker and Bloat; Attract and Repel modes), `ScallopTool`, `CrystallizeTool`, `WrinkleTool` (complexity, affect anchors and handles).
  - Liquify Tool Options dialog shared by every liquify tool (width, height, angle, intensity, pressure pen, detail, simplify, twirl rate, complexity, show brush size) stored under `nodus.tools.liquify.*`.
  - CorelDRAW brushes: `SmoothBrushTool` (nib, rate, pressure), `SmearTool` (nib, amount, pressure, smooth or pointy), `SmudgeTool` (nib, pressure, dryout, tilt, bearing), `RoughenTool` (nib, spike frequency, pressure, dryout, tilt, spike direction fixed, stylus, or auto).
  - Auto convert: distortions, envelopes, and perspective objects convert to curves before roughening, with a status line.
  - Control range settings: right-click a property bar slider to set its min and max, persisted per control in the settings store.
  - Shift-drag resizes the nib interactively; Alt-drag shows the rate slider on canvas.
  - Tests: `ShapeBrushTests` (deterministic dab sequence on a circle fixture gives committed goldens under `tests/fixtures/nodus/brush-dabs/`; node count bound; closed paths stay closed), one test per tool's direction of displacement.
  - Budget: 60 dabs per second on a 5,000-node path with preview under 16 ms.
- **Proof:** Unit tests replaying committed dab sequences against goldens plus a driven run of each brush with undo (capture under `docs/captures/nodus/shape-brushes/`); cheaper substitute that fails: a non-destructive effect, which the node-coordinate goldens catch.

#### §10. Pathfinder, shaping, and the shape builder

- **Deliverable:** The Pathfinder panel (and CorelDRAW Shaping panel) with Divide, Trim, Merge, Crop, Outline, Minus Back, Back minus Front, Weld, Intersect, Boundary, target rules, leave-original options, Pathfinder options, repeat last, live compound shapes, and the Shape Builder tool.
- **Depends On:** D02 T02 §5, D02 T07 §1
- **Phase:** 5
- **Surface:** Fidelity: new panel `docs/captures/nodus/pathfinder-panel/` plus the Shape Builder overlay on `docs/captures/nodus/main-window/`. Job: a designer can build complex shapes from overlaps by command or by dragging across regions. Treatment: every operation is one command on `SKPath.Op`; compound shapes stay live; cheaper substitute that fails: grouping the inputs and calling it a merge. Chrome: consume `D02 T02 §5` `ElementToPathConverter` and boolean service, the dock, shared icon catalog, and history; the Path menu entries from `D02 T02 §5` stay and call the same commands.
- **Runs:** `Requires: display-session -- the panel, Shape Builder drags, and captures need an interactive desktop`
- **Catalog:** NP-0541 to NP-0566 (26 features)
- **Hints:**
  - `Photon.Nodus.Core/Shaping/PlanarFaces.cs`: split a set of paths into non-overlapping faces with `SKPath.Op` (used by Divide, Trim, Merge, Outline, and Shape Builder).
  - Pathfinders: Divide, Trim (hidden areas removed, Corel Simplify), Merge (same-fill neighbors united), Crop (to the top object), Outline (edges as stroked segments), Minus Back (Corel Front minus back), Back minus front.
  - CorelDRAW shaping: Trim a target by sources (marquee trims bottom-most, click-select trims last selected), Weld (target attributes; non-overlapping objects form a weld group; a self-intersecting single object breaks into subpaths), Intersect with one or several targets, Boundary (outer outline for keylines).
  - Leave-original source and target options on the Shaping panel; linked effects (shadows, text on path, blends, contours, extrusions) converted to curves first; shaping a PowerClip frame reshapes the frame (with `D02 T11 §12`).
  - Create object from enclosed area: the click-to-fill face picker built on `PlanarFaces`, shared with `D02 T11 §17` smart fill.
  - Pathfinder Options: precision, remove redundant points, remove unpainted artwork after Divide and Outline (`nodus.pathfinder.*`); Repeat last pathfinder on Ctrl+4.
  - Live compound shapes (Alt-click a shape mode): `nodus:compound-shape` with operands kept editable, Make, Release, Expand through `D02 T07 §1`.
  - `ShapeBuilderTool` (Shift+M): hover highlight of faces and edges, drag to merge, Alt-drag to delete, gap detection (small, medium, large, custom), open filled paths treated as closed, stroke click splits in merge mode, color from swatches or artwork with cursor swatch preview, freeform or straight selection, highlight color.
  - Budget: Divide over 200 overlapping paths completes under 1 s; anything slower shows status strip progress with cancel.
  - Tests: `PathfinderTests` with area and face-count assertions per operation on fixture overlaps, `ShapeBuilderTests` (merge and delete faces), `CompoundShapeRoundTripTests` (fidelity on `tests/fixtures/nodus/svg/compound-shapes/` with Inkscape goldens for the fallback).
- **Proof:** Unit tests above, format fidelity on the compound-shapes fixture, and a driven Shape Builder run with undo (capture under `docs/captures/nodus/pathfinder-panel/`); cheaper substitute that fails: grouping inputs, which the face-count assertion catches.

#### §11. Compound paths, clipping masks, draw inside and behind, and intertwine

- **Deliverable:** Compound path make and release (Combine and Break Curve Apart), nonzero and even-odd fill rules, clipping masks at object and layer level with text as a clip, edit mask and edit contents, Draw Normal, Behind, and Inside, Intertwine, and the fill open curves and treat all objects as filled options.
- **Depends On:** §10
- **Phase:** 5
- **Surface:** Fidelity: Object menu, drawing mode toggle on the tool rail, Layers panel commands, `docs/captures/nodus/main-window/` and `docs/captures/nodus/clipping/`. Job: a designer can punch holes, clip artwork, draw inside a shape, and weave objects. Treatment: clipping renders through Skia clip on the real `clipPath` element and round-trips as SVG `clipPath`; cheaper substitute that fails: pre-cutting the content geometry so the mask cannot be released. Chrome: consume the Object menu, `D02 T07 §5` Layers panel, `D02 T07 §7` isolation mode for edit contents, and history.
- **Runs:** `Requires: display-session -- clipping, draw inside, and intertwine need an interactive desktop`
- **Catalog:** NP-0567 to NP-0578 (12 features)
- **Hints:**
  - Promotes backlog B-002 (`-> SOURCE: legacy-nodus-1.6-4.4`): the importer honors `clip-path`, the Object menu makes and releases clipping masks and compound paths; masks proper ride `D02 T09 §20` and markers `D02 T09 §12`.
  - Teach `SvgParser` to read `clipPath` and `clip-path` references into `SvgClipPath`, `SvgExporter` to write them, and `SkiaRenderer` to apply `SKCanvas.ClipPath` with the clip's transform.
  - Compound Path Make (Ctrl+8, Corel Combine Ctrl+L) and Release (Alt+Shift+Ctrl+8, Break Curve Apart Ctrl+K; text breaks into lines, then words, through `D02 T10 §2`).
  - Fill rule nonzero or even-odd on the Attributes section of `D02 T07 §8`, written as `fill-rule`.
  - Clipping Mask Make (Ctrl+7), Release (Alt+Ctrl+7), Edit Mask and Edit Contents (select the clip path or contents; isolation through `D02 T07 §7`), layer-level clipping mask from the Layers panel, live text as a clip path.
  - Draw modes Normal, Behind, Inside (Shift+D cycles): Inside creates a clip group on the selected object and places new art in it.
  - Intertwine: `nodus:intertwine` zones drawn around overlaps switch which object is on top inside the zone (rendered by clipping a duplicate), Edit adds zones, Release restores stacking.
  - Fill open curves (`nodus.document.fillOpenCurves`, document option) and treat all objects as filled (`nodus.selection.treatAllAsFilled`, hit-testing inside unfilled shapes).
  - Tests: `ClipPathRoundTripTests`, `CompoundPathTests` (even-odd versus nonzero area of a ring), `DrawInsideTests`, `IntertwineTests`.
  - Format fidelity: `tests/fixtures/nodus/svg/clipping/` (nested clips, clip with transform, text clip, compound even-odd) compared element by element and rendered against Inkscape goldens (version recorded) within 1 percent pixel difference.
- **Proof:** Format fidelity on the clipping fixture plus unit tests above and a driven run of make, edit contents, and release with undo (capture under `docs/captures/nodus/clipping/`); cheaper substitute that fails: baking the clip into geometry, which the release test catches.

#### §12. The Transform panel, transform dialogs, Transform Again, and Transform Each

- **Deliverable:** The Transform panel and docker with reference point, constrain, scale corners and strokes, pixel-grid alignment, pattern options, math in fields, and copies; Move, Rotate, Reflect, Scale, Shear, Size, and Scale portion by number; Transform Again; Transform Each; nudge; and Clear Transformations.
- **Depends On:** D02 T07 §8
- **Phase:** 5
- **Surface:** Fidelity: new panel `docs/captures/nodus/transform-panel/` and Object > Transform dialogs under `docs/captures/nodus/transform-dialogs/`. Job: a designer can place, size, rotate, and repeat transforms by exact numbers. Treatment: every apply is one command with preview, Copy creates duplicates in the same entry, Transform Again replays the last recorded transform; cheaper substitute that fails: Transform Again that re-applies the last absolute position rather than the delta. Chrome: consume `D02 T07 §8` Properties panel fields, the shared number box with expression parsing, dock, and history; do not grow a second numeric field control.
- **Runs:** `Requires: display-session -- panel and dialog driving needs an interactive desktop`
- **Catalog:** NP-0583 to NP-0605 (23 features)
- **Hints:**
  - Promotes backlog B-006 (`-> SOURCE: legacy-nodus-3.1`): the transform dialog and Transform Again land here; Select Same and deep select are owned by `D02 T07 §6`.
  - `Photon.Nodus.Core/Transforms/TransformSpec.cs` (translate, rotate, scale, reflect, shear about a reference point; flags scale corners, scale strokes and effects, objects, patterns, copies) applied by one `ApplyTransformCommand` built on `TransformService`.
  - Transform panel (`TransformPanel.xaml`): nine-point reference selector, X, Y, W, H, rotate, shear, constrain proportions (or stretch non-proportionally), flip menu, align to pixel grid, use preview bounds, Shape Properties hosted from §4.
  - Number fields accept arithmetic and units (`D02 T07 §9` unit parser); Alt+Enter applies to a copy.
  - Dialogs `MoveDialog`, `RotateDialog`, `ReflectDialog`, `ScaleDialog`, `ShearDialog` with Preview and Copy; the CorelDRAW Transform docker tabs Position (absolute or relative), Rotate (relative center or ruler coordinates), Scale and Mirror, Size, Skew, copies count, and Scale portion with fit to reference, mapped to the same `TransformSpec`.
  - Transform objects, patterns, or both (panel menu and the backquote drag modifier), with pattern transforms written on the pattern fill from `D02 T09 §10`.
  - Transform Again (Ctrl+D) stores the last `TransformSpec` in the document session and replays it on the current selection; Transform Each (random, relative or absolute scaling) applies about each object's own reference point with a seeded random.
  - Nudge by `nodus.editing.keyboardIncrement` (Shift times 10) and move or scale multi-object selections together or each.
  - Clear Transformations resets an element's accumulated `transform` matrix to identity while keeping its position, one command.
  - Tests: `TransformSpecTests` (each operation against expected matrices), `TransformAgainTests` (move then Transform Again three times gives four equally spaced copies), `TransformEachTests`, `TransformPanelViewModelTests`.
- **Proof:** Unit tests above plus a driven run of each dialog with Copy and undo, and a saved file inspected for the resulting matrices (capture under `docs/captures/nodus/transform-panel/`); cheaper substitute that fails: absolute replay, which `TransformAgainTests` catches.

#### §13. Rotate, reflect, scale, shear, reshape, and free transform tools

- **Deliverable:** The Rotate, Reflect, Scale, Shear, and Reshape tools with movable pivots, the Free Transform tool and its modes (including perspective and free distort), CorelDRAW's second-click rotate and skew handles, handle modifiers, mirror by drag, the Scale portion and Fit to Reference tools, and the rotation angle box.
- **Depends On:** §12
- **Phase:** 5
- **Surface:** Fidelity: tool rail, canvas handles, and property bar, `docs/captures/nodus/main-window/` and `docs/captures/nodus/transform-tools/`. Job: a designer can transform objects interactively around any pivot. Treatment: every drag records one `ApplyTransformCommand` on mouse-up through the `D02 T03 §1` pattern; cheaper substitute that fails: live-mutating matrices with nothing recorded. Chrome: consume §12 `TransformSpec`, the `SelectTool` handle overlay, the property bar, and history.
- **Runs:** `Requires: display-session -- interactive transform drags need an interactive desktop`
- **Catalog:** NP-0606 to NP-0621 (16 features)
- **Hints:**
  - `RotateTool`, `ReflectTool`, `ScaleTool`, `ShearTool` in `Photon.Nodus.Core/Tools/Transform/`: click sets the pivot, drag transforms, Alt-click opens the §12 dialog, Alt-drag copies.
  - `SelectTool` second click toggles to rotate and skew handles with a movable center of rotation; corner handles scale proportionally, middle handles stretch, skew arrows slant.
  - Handle modifiers: Shift from center, Ctrl integer multiples (100 percent increments), Alt stretch non-proportionally, Ctrl-drag across mirrors; the CorelDRAW keymap swaps Ctrl and Shift per `D02 T16 §3`.
  - Mirror buttons and the angle-of-rotation box on the property bar, both one command.
  - `ReshapeTool`: stretch selected anchors while neighbors follow by falloff, keeping the overall shape.
  - `FreeTransformTool` (E): widget with Constrain, Free Transform, Perspective Distort, Free Distort; CorelDRAW free rotation, angle reflection, free scale, free skew, relative to object, apply to duplicate.
  - Perspective and free distort on paths map every node through a projective transform (bilinear for free distort) and write plain geometry; distorting live shapes expands them first with a status line.
  - `ScalePortionTool` (drag a known span, type its length, scale the object) and `FitToReferenceTool` (scale and move into another object's bounds).
  - Constrain with Ctrl and draw from center with Shift consistently across drawing and transform tools through one `ModifierPolicy` in `Photon.Nodus.Core/Tools/`.
  - Tests: `TransformToolTests` (rotate about a moved pivot, shear angle, reflect axis), `FreeDistortTests` (corner mapping exact at the four corners), `HandleModifierTests`, `ScalePortionTests`.
- **Proof:** Unit tests above plus a driven run of each tool with undo restoring exact matrices (capture under `docs/captures/nodus/transform-tools/`); cheaper substitute that fails: no recorded command, which the undo assertion catches.

#### §14. Align, distribute, arrange, and step and repeat extensions

- **Deliverable:** The Align panel and docker with key object, artboard, page, grid, and point references, one-click centering, preview bounds and text baselines, full distribute and spacing with preview, align artboards, arrange commands for page and layer order, In Front Of, Behind, Reverse Order, Send to Current Layer, the locked layer rule, and Step and Repeat.
- **Depends On:** §12
- **Phase:** 5
- **Surface:** Fidelity: new panels `docs/captures/nodus/align-panel/` and `docs/captures/nodus/step-and-repeat/`, Object > Arrange on `docs/captures/nodus/main-window/`. Job: a designer can line up, space, stack, and duplicate objects exactly. Treatment: every button is one `CompositeCommand` from `AlignmentService` deltas, spacing previews before apply; cheaper substitute that fails: a panel that only mirrors the `D02 T02 §4` menu. Chrome: consume `D02 T02 §4` `CompositeCommand` and `AlignmentService`, `D02 T07 §5` layers, the dock, shortcut manager, and history.
- **Runs:** `Requires: display-session -- panel driving and click-target arrange commands need an interactive desktop`
- **Catalog:** NP-0622 to NP-0643 (22 features)
- **Hints:**
  - `AlignPanel.xaml` (Align and Distribute docker in the CorelDRAW workspace): align six ways, distribute left, center, right, top, center, bottom, distribute spacing equal or exact, all through `AlignmentService`.
  - Align To: selection, key object (click a selected object to make it key), artboard, page edge, page center, grid (`D02 T07 §9`), or a typed or clicked point; distribute to selection, page, or exact object spacing.
  - One-click center on both axes and Center to Page (P, plus horizontal and vertical variants).
  - Bounds: use preview bounds (stroke included), object outline, or glyph bounds; text references first baseline, last baseline, or bounding box (baselines from `D02 T10 §2`).
  - Distribute spacing preview draws ghost positions before apply.
  - Align selected artboards through the `D02 T07 §3` artboard model.
  - Every align and distribute command registered with the shortcut manager so it can take a shortcut; action recording is excluded automation.
  - Arrange: To Front or Back of Page, To Front or Back of Layer, In Front Of and Behind a clicked object, Reverse Order, Send to Current Layer; moves onto locked layers go to the nearest editable layer with a status message.
  - Step and Repeat panel (Ctrl+Shift+D): copies count, horizontal and vertical modes no offset, spacing between objects with direction, or offset, one `CompositeCommand` for all copies.
  - Tests: `AlignPanelTests` (key object, page, grid, point references), `DistributeSpacingTests` (exact 12 px gaps across five objects), `ArrangeCommandParityTests` (page versus layer order, locked layer rule), `StepAndRepeatTests` (1,000 copies under 1 s).
- **Proof:** Unit tests above plus a driven run aligning to a key object, distributing with preview, reversing order, and stepping ten copies with undo (captures under `docs/captures/nodus/align-panel/` and `docs/captures/nodus/step-and-repeat/`); cheaper substitute that fails: menu-only alignment, which the key-object test catches.

#### §15. Dimensions, connectors, and callouts

- **Deliverable:** Associative linear, angular, radial, segment, successive, and stacked dimensions with a full number format and style, break apart, and defaults; straight, right-angle, and rounded connectors that stay attached, with anchor editing, wrap, and text labels; and the 2-leg callout.
- **Depends On:** D02 T07 §9, D02 T07 §1
- **Phase:** 5
- **Surface:** Fidelity: tool rail flyouts, property bar, and Dimension Tool Options dialog, `docs/captures/nodus/main-window/` and `docs/captures/nodus/dimensions/`. Job: a designer can annotate technical drawings with measurements and diagrams with live connectors. Treatment: dimensions and connectors are live objects bound to the measured or connected elements and update when those move; cheaper substitute that fails: static lines and text that go stale on move. Chrome: consume `D02 T07 §9` units and drawing scale, `D02 T07 §11` snapping, the property bar, `D02 T09 §12` arrowheads, and history.
- **Runs:** `Requires: display-session -- dimension and connector drawing and rerouting need an interactive desktop`
- **Catalog:** NP-0649 to NP-0676 (28 features)
- **Hints:**
  - `Photon.Nodus.Core/Annotations/Dimension.cs`: kinds linear (horizontal, vertical, aligned), angular, radial (radius or diameter), segment; bound to element ids and node indices; stored as `nodus:dimension` with an expanded group of lines, arrows, and text as the SVG fallback.
  - `DimensionTool` (one tool with kind modes plus CorelDRAW flyout aliases), segment dimensions across a marquee of segments, automatic successive dimensioning, stacked chains from a base line.
  - Number format: units, precision, fractional, decimal, or standard style, show units, leading zero, prefix and suffix, drawing scale from `D02 T07 §9`.
  - Style: arrow style and scale (from `D02 T09 §12`), line weight and type, extension line offset and overhang or hidden, label font, size, and position (above, below, centered, inside, outside).
  - Associative (dynamic) dimensions recompute on the measured element's change event; static mode freezes the text; Apply to all and Set as default write `nodus.tools.dimension.*` defaults.
  - Break Dimension Apart and Break Callout Apart expand to plain objects as one command.
  - `Photon.Nodus.Core/Annotations/Connector.cs` and `ConnectorTool`: straight, right-angle, rounded right-angle; endpoints bound to anchors; rerouting on element move with an own orthogonal router (visibility-graph approach after Wybrow, Marriott, and Stuckey 2009; libavoid not ported) that wraps around objects when the object's wrap flag is on.
  - `AnchorEditingTool`: add (double-click), move along the perimeter or to the center, delete, exit direction 0, 90, 180, 270, auto anchor as snap point, position relative to object; connector segment editing (move middle node, slide ends, add or merge corners).
  - Connector text label that follows the connector; connector defaults (geometric anchors as snap points, route distance) as settings.
  - `TwoLegCalloutTool`: leader with two segments, text, callout shape and gap.
  - Tests: `DimensionFormatTests` (units, precision, prefix, leading zero), `AssociativeDimensionTests` (moving the target updates the value), `ConnectorRoutingTests` (orthogonal route avoids an obstacle; 500 connectors reroute under 16 ms after a move), and format fidelity on `tests/fixtures/nodus/svg/annotations/` with Inkscape goldens for the fallback.
- **Proof:** Format fidelity on the annotations fixture, unit tests above, and a driven run moving a connected and dimensioned object with the connector rerouting and the dimension updating, then undo (capture under `docs/captures/nodus/dimensions/`); cheaper substitute that fails: static annotation objects, which `AssociativeDimensionTests` catches.

#### Sizing concerns

- §4 carries 72 inventory rows (38 catalog features): live shapes, live corners, the Corners panel, and the ten-mode Coordinates panel. It fits 30 items only if the Coordinates panel is one item with numbered sub-steps per shape kind; if authoring shows otherwise, the Coordinates panel is the natural split (a new section after §15, depending on §4).
- §6 carries 48 rows (33 features); node align and distribute plus B-spline control point editing are the parts to fold into sub-steps to stay under 30 items.
- §10 bundles the Pathfinder panel and the Shape Builder tool (26 features); it fits because both run on one `PlanarFaces` engine, but the Shape Builder options could overflow if each option becomes its own item.

### todo/02-nodus/TODO-09-nodus-parity-color.md -- `nodus-parity-color`

- **Title:** "TODO-09 -- Nodus Parity: Color, Fills, Strokes, Brushes, Transparency, Styles, and Symbols"
- **Phase(s):** 6
- **Goal:** Nodus paints like Illustrator 30.8 and CorelDRAW 2026: a color model that carries RGB, CMYK, HSB, Lab, grayscale, spot, global, and tint values through Photon.Core color management (`D01 T04 §1`); one Color panel and picker, eyedroppers, swatches, palettes, color styles and harmonies, and Recolor; linear, radial, conical, rectangular, freeform, and mesh gradients; pattern, texture, and procedural fills with a fill library; a full stroke model with arrowheads, dashes, alignment, and variable width; stacked appearances and reusable styles; art, pattern, scatter, calligraphic, bristle, and painterly brushes; every standard blend mode, opacity masks, and fountain transparency; and dynamic, 9-slice, nested, and library-linked symbols with the symbolism tools. Every paint attribute persists in SVG through the live-object contract (`D02 T07 §1`), every edit is one undoable command, and every palette, brush, style, and symbol library a user owns imports and exports. This file promotes backlog B-003 (`legacy-nodus-4.2-1.4`) into §3 and B-010 (`legacy-nodus-6`) into §16.
- **Current-state facts to verify (with claim candidates):**
  - Nodus's color is one 8-bit RGBA struct with HSL, HSV, and hex helpers and no CMYK, Lab, or spot type. `<!-- claim: count "public readonly struct Color" src/Nodus/Bezier.Core/Models/Color.cs = 1 -->` `<!-- claim: count "Cmyk|\bLab\b|Spot" src/Nodus/Bezier.Core/Models/Color.cs = 0 -->`
  - Five fill types exist (solid, linear, radial, pattern, none). `<!-- claim: count "class \w+ : IFill" src/Nodus/Bezier.Core/Models/Fills/*.cs = 5 -->`
  - `PatternFill` exists in the model but the SVG writer never writes it. `<!-- claim: count "PatternFill" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->`
  - `Stroke` holds width, opacity, cap, join, miter limit, and dash array only: no alignment, arrowheads, or width profile. `<!-- claim: lines src/Nodus/Bezier.Core/Models/Stroke.cs = 89 -->` `<!-- claim: count "Alignment|Arrow" src/Nodus/Bezier.Core/Models/Stroke.cs = 0 -->`
  - A 12-member `BlendMode` enum sits on `VectorElement`, but neither the SVG writer nor the Skia renderer reads it, and Hue, Saturation, Color, and Luminosity are missing. `<!-- claim: count "enum BlendMode" src/Nodus/Bezier.Core/Models/VectorElement.cs = 1 -->` `<!-- claim: count "BlendMode" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->` `<!-- claim: count "BlendMode" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->` `<!-- claim: count "Hue|Saturation|Luminosity" src/Nodus/Bezier.Core/Models/VectorElement.cs = 0 -->`
  - The Properties panel's Fill row is a static placeholder showing a literal hex, not a bound color. `<!-- claim: count "#89B4FA" src/Nodus/Bezier.Desktop/Views/MainWindowView.xaml = 1 -->`
  - There is no eyedropper tool; the tool folder holds 10 files. `<!-- claim: absent src/Nodus/Bezier.Core/Tools/EyedropperTool.cs -->`
  - `Symbol` and `SymbolInstance` exist with an `Overrides` dictionary, but the SVG writer never writes an instance. `<!-- claim: count "Dictionary<string, object\?> Overrides" src/Nodus/Bezier.Core/Models/Symbol.cs = 1 -->` `<!-- claim: count "SymbolInstance" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->`
  - Photon.Core does not exist yet, so no color-management engine exists anywhere in the tree. `<!-- claim: absent src/Photon.Core/Photon.Core.csproj -->`
- **Inputs and XREFs:** `standards/nodus.md` (SVG native, one renderer, Inkscape goldens); `D02 T07 §1` (live-object contract every live paint rides); `D02 T07 §8` (Properties panel and property bar the color, fill, stroke, and transparency controls dock into); `D02 T07 §6` (Select Same, extended by §3's tint match); `D02 T07 §7` (isolation mode, reused by §10's pattern editing and §21's symbol editing); `D02 T08 §3` (freehand curve fitting the brush tools reuse); `D02 T08 §10` (`SKPath.Op` union the Blob Brush reuses); `D02 T08 §12` (Transform panel options for patterns and symbol registration); `D01 T04 §1` and `D01 T04 §2` (conversion, gamut, intents); `D01 T02 §2` (settings store) and `D01 T02 §4` (suite history); `D01 T01 §3` (suite theme, extended by §2 and §4 with swatch-well, checkerboard, and gamut-warning tokens added to `standards/shared.md` and `Photon.Dark.xaml`); `D02 T06 §11` (symbols and asset library basics, extended by §21 and §22); `D03 T03 §8` (Imago's color panel: the picker built in §2 moves to `Photon.UI` the day that section needs it); backlog B-003 (promoted into §3) and B-010 (promoted into §16). Consumers that point back: `D02 T11 §1` (effects enter through §14's Add New Effect), `D02 T13 §5` and `D02 T13 §7` (separations and overprint read §1's spot and overprint data), `D02 T13 §14` (PDF Separation and DeviceN from §1), `D02 T14 §7` (CDR fills, outlines, and transparency map onto §7 to §20), `D02 T15 §2`, `D02 T15 §3`, and `D02 T15 §5` (AI writes swatches, patterns, and recolor results through §3, §10, and §6), `D02 T16 §10` (Find and Replace consumes §6's and §12's replace engines).
- **Adjacency:** list=applicable; document=not-applicable (separations, print, and PDF output that carry spot and overprint data are owned by D02 T13 §5 and D02 T13 §14; this file only stores the data they read); settings=applicable; reporting=not-applicable (ink and color usage reports belong to D02 T13 §9 preflight; this file only lists used and unused swatches, styles, brushes, and symbols); notifications=applicable; permissions=applicable; audit=applicable; exchange=applicable; reverse=applicable
- **Adjacency rationale:** swatches, palettes, color styles, fills, brushes, styles, and symbols each get a searchable list with filters; every tunable (recent colors, palette rows, eyedropper sample size, mesh defaults, bristle warning count, fountain display steps) is a settings-store key with a named consumer; long recolor, texture render, pattern render, and painterly re-render runs report progress on the status strip and cancel; locked library palettes, read-only library folders, and broken symbol-library links are refused by name with the recovery action offered; every edit is one logged, undoable command; ASE, ACO, ACB, GPL, Corel XML and CPL palettes, brush, style, fill, and symbol libraries import and export with fidelity fixtures.

#### §1. The color model: RGB, CMYK, HSB, Lab, grayscale, spot, global, and tints

- **Deliverable:** A `PaintColor` model that stores a color in its authored model (RGB, CMYK, HSB, HSL, Lab, grayscale) plus spot, registration, global, and tint references, converts through Photon.Core color management, and round-trips through SVG with `icc-color` and `nodus:` attributes.
- **Depends On:** D02 T07 §1, D01 T04 §1
- **Phase:** 6
- **Surface:** no surface of its own (the color UI is §2; the document color mode command is a menu item wired here with no new panel)
- **Runs:** none
- **Catalog:** NP-0677 to NP-0686 (10 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Color/PaintColor.cs`: an immutable record with `ColorModel` (Rgb, Cmyk, Hsb, Hsl, Lab, Gray), `double[] Components`, `Alpha`, and an optional `SwatchRef` (swatch id plus `Tint` 0 to 100); the existing `Color` struct stays as the display sRGB value `PaintColor.ToDisplay()` returns.
  - `SpotColor` (name, `AlternateSpace` Lab or CMYK, alternate values, `IsDeviceSpot` for names such as `CutContour` and `Thru-cut` that must never be converted), and a singleton `Registration` color that prints on every plate.
  - Conversions go through `Photon.Core/Color/ColorTransformService` (`D01 T04 §1`) using the document's RGB and CMYK profiles; HSB, HSL, CMY, HLS, and YIQ are pure math in `ColorMath.cs` as viewer models only (never a stored model for YIQ).
  - `VectorDocument.ColorMode` (Rgb or Cmyk) plus `SetDocumentColorModeCommand` (File > Document Color Mode) converting every process color once, logged with the object count, one undo step.
  - `ConvertColorsCommand` for Edit > Edit Colors > Convert to CMYK, Grayscale, RGB over the selection (fills, strokes, gradient stops, mesh nodes), skipping spot and device spot colors with a report line.
  - Overprint flags `OverprintFill` and `OverprintStroke` stored on the paint, written as `nodus:overprint-fill`/`nodus:overprint-stroke`, read later by `D02 T13 §7`.
  - SVG write: `fill="#rrggbb icc-color(<profile-name>, c, m, y, k)"` for CMYK (SVG 1.1 paint syntax Inkscape reads), `nodus:paint="lab(l a b)"` or `nodus:spot="<id>"` with `nodus:tint`, and the sRGB hex always present as the plain fallback.
  - `SvgImporter` reads the same attributes back into `PaintColor`, restoring the authored model exactly (no RGB round trip of CMYK values).
  - Defaults: new documents take fill white and stroke black (settings keys `nodus.color.defaultFill`, `nodus.color.defaultStroke`); None stays `NoneFill`.
  - Tests: `PaintColorTests` (conversions against lcms2 `transicc` values within Delta E 2000 0.5), `ColorModeCommandTests` (undo restores every authored value), `ColorPersistenceTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/color-models.svg` (RGB, CMYK, Lab, gray, spot, CutContour, global tint, overprint) opened, saved, reopened, and compared element by element, with the sRGB fallback rendering golden from Inkscape 1.4; cheaper substitute that fails: storing CMYK as converted RGB, which the fixture's exact CMYK comparison rejects.

#### §2. The Color panel, color picker, recent colors, and eyedroppers

- **Deliverable:** The Color panel (docker), fill and stroke wells, the color picker dialog with viewers and palette modes, recent colors, the color and attributes eyedroppers, and drag-and-drop of swatches onto objects.
- **Depends On:** §1, D02 T07 §8
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/color/ (panel, picker, eyedropper loupe).
  - Job: a designer can pick, mix, sample, and apply any color to fill or stroke without leaving the canvas. Consumer: the selection's paint, recorded as commands.
  - Treatment: a docked Color panel with fill and stroke wells, per-model sliders with Shift-drag tandem tint, hex field with Copy Hex, gamut and web-safe warnings, and a picker dialog with 1D and 3D viewers, palette mode, and a sampling loupe. Cheaper substitute that fails: the Windows color dialog.
  - Chrome: consume `Photon.Dark.xaml` (`D01 T01 §3`, extended with swatch-well, checkerboard, and gamut-warning tokens), the icon catalog, the Properties panel host (`D02 T07 §8`), and the settings store; the picker is Nodus-local under `Photon.Nodus.Desktop/Controls/ColorPicker/` and moves to `Photon.UI` the day Imago's color panel (`D03 T03 §8`) needs it. Do not build a second picker in the stroke or gradient panels.
- **Runs:** `Requires: display-session -- the panel, picker, and desktop eyedropper need an interactive desktop`
- **Catalog:** NP-0687 to NP-0712 (26 features)
- **Hints:**
  - `Photon.Nodus.Desktop/Views/Color/ColorPanel.xaml` plus `ColorPanelViewModel` (F6): models Grayscale, RGB, HSB, CMYK, Lab, Web Safe RGB; Invert and Complement menu items; Create New Swatch hands off to §3's `AddSwatchCommand`.
  - `FillStrokeWells` control replacing the static `#89B4FA` placeholder in the Properties panel: X toggles focus, Shift+X swaps, D resets to defaults, `/` sets None, double-click opens the picker.
  - `ColorPickerDialog` with Viewers (1D strip and 3D square per model), Sliders, and Palettes modes (palette chooser plus slider range and color names), reference versus new swatch with Swap, and Add to Palette.
  - Out-of-gamut and non-web-safe warnings computed through `D01 T04 §2`'s gamut API; clicking snaps to the nearest printable or web-safe color.
  - Hex field accepts 3 and 6 digit input; Copy Hex writes to the clipboard; the status bar shows the selection's fill and stroke hex.
  - `RecentColorsService` backed by settings key `nodus.color.recent` (max 20, shared across documents), shown in the panel and picker.
  - Palette interactions from the palette bar (§4 draws the bar): click-and-hold shade pop-up, Ctrl+click mixes 10 percent into the current fill or stroke, Show Color Names toggle.
  - `Photon.Nodus.Core/Tools/EyedropperTool.cs` (I): click samples and applies fill and stroke, Shift samples a single color, Alt applies; sample size 1x1, 3x3 average, 5x5 average (key `nodus.eyedropper.sampleSize`); loupe preview before applying.
  - `DesktopColorSampler` (GDI `GetPixel` over a screen DC through `LibraryImport`) for Select From Desktop; sampled color can be added to the document palette.
  - `AttributesEyedropperTool` with an `AttributeSet` (Outline, Fill, Text; Size, Rotation, Position; effects list) applied as one `ApplyAttributesCommand`; the AI Eyedropper Options dialog edits the same `AttributeSet`.
  - Drag a swatch onto an object's interior to set fill, onto its outline to set stroke, one command per drop.
  - Tests: `ColorPanelViewModelTests` (model round trips, tandem sliders), `EyedropperToolTests` (sample-size averaging on a fixture bitmap), `AttributesEyedropperTests`.
- **Proof:** Unit tests plus a driven run: sample a known pixel with the eyedropper and read its hex from the status bar and the log line, captured to docs/captures/nodus/color/; cheaper substitute that fails: a picker that only edits RGB, which the CMYK and Lab slider tests reject.

#### §3. The Swatches panel, document palette, and color groups

- **Deliverable:** A document swatch library (process, global, spot, registration, tint, gradient, pattern swatches and color groups) stored in SVG `<defs>`, shown as the Swatches panel and the Corel-style document palette, with global swatches in settings.
- **Depends On:** §1
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/swatches/.
  - Job: a designer can save, organize, and reuse colors so that editing one global swatch recolors every object using it. Consumer: every paint reference in the document.
  - Treatment: a Swatches panel with thumbnail and list views, kind filter, sort, color groups, and Swatch Options; the same library drawn as the document palette. Cheaper substitute that fails: swatches that copy their value into objects, so editing one changes nothing.
  - Chrome: consume the theme, icon catalog, settings store, and suite history; one swatch model feeds the panel, the palette bar (§4), and color styles (§5). Do not keep a second color list for the document palette.
- **Runs:** `Requires: display-session -- the panel and drag interactions need an interactive desktop`
- **Catalog:** NP-0713 to NP-0731 (19 features)
- **Hints:**
  - Promoted from backlog B-003: `-> SOURCE: legacy-nodus-4.2-1.4` (its Appearance part lands in §14 and its conic gradients in §7).
  - `Photon.Nodus.Core/Color/Swatch.cs` (id, name, `SwatchKind` Process, Global, Spot, Registration, Gradient, Pattern, `PaintColor`, group id) and `SwatchLibrary` on `VectorDocument`.
  - Persist swatches in `<defs>` as single-stop gradients marked `inkscape:swatch="solid"` (Inkscape's own swatch convention, read by Inkscape 1.4) with `nodus:swatch-kind`, and color groups as `nodus:color-group` elements; objects reference swatches by `url(#id)` plus `nodus:spot`/`nodus:tint`.
  - Global swatches shared across documents live in settings key `nodus.swatches.global` (B-003's summary).
  - Commands: `AddSwatchCommand`, `NewColorGroupCommand`, `AddUsedColorsCommand` (selection or document), `DeleteSwatchesCommand`, `MergeSwatchesCommand`, `DuplicateSwatchCommand`, `ReplaceSwatchCommand` (Alt-drag), `ReorderSwatchCommand`, each logged and undoable.
  - Select All Unused and Refresh (remove unused) share one `SwatchUsageScanner` over fills, strokes, gradients, patterns, and mesh nodes.
  - Swatch Options dialog: name, kind, global flag, model, values, live preview.
  - Document palette auto-add (settings key `nodus.swatches.autoAddUsedColors`, default on), add colors by dragging objects onto the palette, and eyedropper-add from a bitmap (Ctrl picks several; N most frequent colors by exact histogram).
  - Select Same Tint Percentage extends `D02 T07 §6`'s Select Same matcher (settings key `nodus.select.sameTintPercentage`).
  - Tests: `SwatchLibraryTests`, `GlobalSwatchUpdateTests` (editing a global swatch updates 3 objects, one undo restores all), `SwatchUsageScannerTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/swatches.svg` (every swatch kind, tints, groups) round-tripped element by element, with Inkscape 1.4 opening the file and listing the solid swatches; cheaper substitute that fails: copied values, which `GlobalSwatchUpdateTests` rejects.

#### §4. The palette bar, palette editor, color libraries, and palette files

- **Deliverable:** The dockable palette bar, the Palettes docker and palette editor, user and library palettes on disk, user-imported color books, and palette file import and export (ASE, ACO, ACB, GPL, Corel XML, legacy CPL, SVG keywords).
- **Depends On:** §3
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/palettes/ (palette bar docked and floating, Palettes docker, palette editor).
  - Job: a designer can keep palettes and color books beside the canvas and apply a color with one click. Consumer: the selection's fill and stroke, and the document swatch library (§3).
  - Treatment: a palette bar on the right edge (rows, wide borders, large swatches, No Color well, spot marker), left-click fill and right-click outline or menu, a Palettes docker with My palettes folders and locked Palette libraries, and a palette editor. Cheaper substitute that fails: a fixed swatch strip that cannot open a user's ASE file.
  - Chrome: consume the theme, icon catalog, settings store, the §2 picker, and the §3 swatch model. Do not duplicate the picker in the palette editor.
- **Runs:** `Requires: display-session -- docking, drag, and the docker need an interactive desktop`
- **Catalog:** NP-0732 to NP-0757 (26 features)
- **Hints:**
  - `Photon.Nodus.Desktop/Controls/Palettes/PaletteBar.xaml`: dock left, right, top, bottom or float, lock positions, rows 1 to 7, wide borders, large swatches, No Color well, white-square spot marker; settings keys under `nodus.palette.*` (rows, rightClickAction menu or outline, wideBorders, largeSwatches, showNoColorWell, locked, open list, default).
  - Default RGB and CMYK palettes follow the document color mode (§1); Set as Default Palette writes `nodus.palette.default`.
  - `PalettesPanel` (Palettes docker and Window > Color Palettes menu): My palettes under `%LOCALAPPDATA%\Rizonesoft\Nodus\Palettes\` with folders, cut, copy, paste, rename, delete; Palette libraries read-only (edit refused by name with Copy to My palettes offered).
  - New empty palette, Create Palette from Selection, Create Palette from Document, and Add to Palette from the color dialogs, each an undoable library command.
  - `PaletteEditorDialog`: add, edit, delete, rename, sort (hue, lightness, saturation, name, RGB, HSB) and Treat as Spot or Process.
  - `Photon.Nodus.Core/Color/PaletteFiles/`: `AseReader`/`AseWriter` (Adobe Swatch Exchange), `AcoReader` (Photoshop swatches per Adobe's published spec), `AcbReader` (color books), `GplReader`/`GplWriter` (GIMP), `CorelXmlPaletteReader`/`Writer`, `CplReader` (legacy CPL converted to XML on open), and an SVG color-keyword palette (the 147 CSS named colors).
  - Color books and spot libraries are user-imported only: no PANTONE, HKS, TOYO, DIC, Focoltone, or TRUMATCH data ships; the empty state explains how to import a book the user owns.
  - Nodus ships its own process libraries and curated gradient and pattern libraries (the 30.8 refresh row) as SVG palette files in app resources.
  - Save Swatch Library as ASE (and SVG); the Illustrator `.ai` swatch-library form is written by `D02 T14 §5`'s AI exporter.
  - Palette click shortcuts: left-click fill, right-click outline (or menu per setting), Ctrl+click mix, click-and-hold shades (from §2).
  - Tests: `AseRoundTripTests`, `GplRoundTripTests`, `CorelXmlPaletteTests`, `CplReaderTests`, `PaletteLibraryPermissionTests` (edit of a locked palette refused).
- **Proof:** Format fidelity proofs per format under `tests/fixtures/nodus/palettes/<format>/` with goldens from Krita 5.2 (reads ASE, ACB, ACO, GPL) and GIMP 3.0 (GPL, ACO), versions recorded; Corel XML and CPL fixtures carry hand-verified twins; cheaper substitute that fails: an ASE reader that drops spot and Lab entries, which the fixture's element comparison rejects.

#### §5. Color styles, harmonies, and the color guide

- **Deliverable:** Color styles (global colors with harmonies and gradient harmonies) in a Color Styles docker with the harmony editor wheel, plus the Color Guide panel of rule-based suggestions and variations.
- **Depends On:** §3
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/color-styles/ (docker, harmony wheel, Color Guide).
  - Job: a designer can define a harmony once and shift every color that uses it together. Consumer: every object linked to a color style.
  - Treatment: a Color Styles docker listing styles and harmony folders with a harmony wheel (rings, arms, rules, brightness) and a Color Guide panel with a rule menu and a tints and shades, warm and cool, or vivid and muted grid. Cheaper substitute that fails: a static list of suggested colors that does not update linked objects.
  - Chrome: consume the §3 swatch model (a color style is a global swatch; a harmony is a color group with a rule), the §2 picker as the color editor, the theme, and the suite history. Do not create a second global-color store.
- **Runs:** `Requires: display-session -- the harmony wheel and docker need an interactive desktop`
- **Catalog:** NP-0758 to NP-0792 (35 features)
- **Hints:**
  - `Photon.Nodus.Core/Color/Harmonies/HarmonyEngine.cs`: rules Analogous, Accented Analogous, Complementary, Split Complementary, Monochromatic, Shades, Triad, Tetrad, Compound, High Contrast, Pentagram, Custom (the 23 Color Guide rules as data), computed on an HSB wheel with the painter's-wheel hue mapping recorded in the XML doc comment.
  - `ColorHarmony` (rule, base color, arms, brightness) persisted on §3's color group as `nodus:harmony-rule`, `nodus:harmony-brightness`.
  - `ColorStylesPanel.xaml`: New color style (from selected fill, outline, or both; from document; from the color editor or a dropped swatch), with Group into N harmonies and Convert all to a mode options on create.
  - New harmony, Duplicate harmony, New gradient harmony (master plus N linked shades, lighter, darker, or both, shade similarity), each one command.
  - Apply (double-click fill, right-click outline, drag), Rename, Delete, Merge into last selected, Swap fill and outline styles, Select unused, Break link to color styles.
  - Convert a style or harmony to another model, to spot, or to grayscale through `ColorTransformService`.
  - `HarmonyWheel` control: drag rings to rotate all colors, Ctrl keeps saturation, Shift keeps hue, Alt-drag moves a color to another arm, Distribute colors, Switch to opposite, Remove rule, Rule from scratch (seeded five-color harmony), Ctrl+click edits several harmonies together.
  - View options: hint view (outlines objects using the hovered style), large swatches, show empty arms; reorder harmonies by drag.
  - Color styles palette in the palette bar (§4 hosts the bar; this section supplies the palette source).
  - `ColorGuidePanel.xaml` (Shift+F3): harmony rule menu, variation grid (tints and shades, warm and cool, vivid and muted), limit to a swatch library, Save color group to Swatches.
  - Tests: `HarmonyEngineTests` (each rule's hue offsets), `ColorStyleLinkTests` (rotating a harmony recolors 5 linked objects in one undo step).
- **Proof:** Unit tests `HarmonyEngineTests` and `ColorStyleLinkTests`, plus a format fidelity round trip of `tests/fixtures/nodus/svg/color-styles.svg` (harmonies, gradient harmony, links); cheaper substitute that fails: suggestions that do not link, which `ColorStyleLinkTests` rejects.

#### §6. Recolor Artwork, Edit Colors, and find and replace color

- **Deliverable:** The Recolor Artwork dialog (simple and advanced Assign and Edit tabs, themes, theme picker, reduction and colorize methods) and the Edit Colors commands, plus the color replace engine that Find and Replace consumes.
- **Depends On:** §5
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/recolor/.
  - Job: a designer can remap every color in a selection to a new palette or harmony in one step. Consumer: the selection's paints, gradient stops, pattern tiles, mesh nodes, and symbol definitions.
  - Treatment: a Recolor dialog with a color wheel (smooth, segmented, bars), prominent-colors bar, library and count choice, randomize, and an advanced mode with the Assign table (merge, separate, exclude, new row) and Edit tab. Cheaper substitute that fails: a hue-shift slider over the selection.
  - Chrome: consume the §5 `HarmonyWheel` and `HarmonyEngine`, the §3 color groups, the §2 picker, and the suite history. Do not build a second wheel.
- **Runs:** `Requires: display-session -- the dialog's live preview needs an interactive desktop`
- **Catalog:** NP-0793 to NP-0811 (19 features)
- **Hints:**
  - `Photon.Nodus.Core/Color/Recolor/ColorCollector.cs` gathers every color from fills, strokes, gradient stops, pattern tiles, mesh nodes, and symbol definitions, grouped by hue with usage weights.
  - `RecolorEngine` applies a `RecolorMap` (current to new rows, merged and excluded rows) with colorize methods Exact, Preserve Tints, Scale Tints, Tints and Shades, Hue Shift, and preserve white, black, and grays options; one `RecolorCommand` per OK.
  - Color reduction to N colors with Limit to Library and sort options; Randomize order and Randomize saturation and brightness take a seed stored in the command for exact undo and redo.
  - `RecolorArtworkDialog.xaml`: color library, colors count, color themes, prominent colors bar (drag to reweight), link and unlink harmony colors, Recolor Art preview toggle, Get Colors from Selected Art, global or local edits, save changes to the group or a new group, add, remove, and edit colors.
  - Theme picker samples any visible image or art on the canvas into a palette (N most frequent colors by histogram).
  - Recolor quick action: a command-palette entry "Recolor (guided)" opening the dialog on the selection.
  - Edit Colors commands: Adjust Color Balance (model, fill and stroke options), Blend Front to Back, Blend Horizontally, Blend Vertically (three or more filled objects), Invert Colors, Saturate (percent), each one command.
  - `ColorReplaceService` (match by exact color or by model or palette, in fills, outlines, fountain, two-color, and mesh fills, and monochrome bitmaps) with an Edit > Edit Colors > Replace Color dialog; `D02 T16 §10`'s Find and Replace wizard consumes the same service.
  - The Recolor part of backlog B-010's summary ("a Recolor dialog mapping colors through a harmony wheel") is met here; B-010's source key lives on §16.
  - Performance: recolor of a 10,000-object selection under 1 second, otherwise progress on the status strip with Cancel.
  - Tests: `RecolorEngineTests` (each colorize method on a fixture), `EditColorsCommandTests`, `ColorReplaceServiceTests`.
- **Proof:** Unit tests `RecolorEngineTests`, `EditColorsCommandTests`, and `ColorReplaceServiceTests` on `tests/fixtures/nodus/svg/recolor-source.svg` against committed expected SVGs, plus one driven recolor captured; cheaper substitute that fails: a global hue rotate, which the Exact and Preserve Tints expectations reject.

#### §7. The gradient model: linear, radial, conical, rectangular, stops, repeat, and interpolation

- **Deliverable:** A gradient model with linear, radial and elliptical, conical, and rectangular types, rich stops, arrangement, acceleration, blend direction, perceptual interpolation, dither, and steps, rendered by Skia and persisted as SVG gradients with `nodus:` parameters and exact fallbacks, plus the Gradient panel.
- **Depends On:** §1
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/gradient/.
  - Job: a designer can build any gradient type numerically and save it as a swatch. Consumer: fills, strokes, transparency masks (§20), and swatches (§3).
  - Treatment: a Gradient panel with type buttons, stop slider (color, opacity, location, midpoint), angle and aspect ratio, reverse, arrangement, acceleration, smoothing, blend direction, interpolation, dither, steps, and presets. Cheaper substitute that fails: two-stop linear and radial only.
  - Chrome: consume the §2 picker for stop colors, the §3 swatch model for gradient swatches, the theme, and the Properties panel host. Do not duplicate stop editing in §8's annotator; both bind one view model.
- **Runs:** `Requires: display-session -- the panel needs an interactive desktop`
- **Catalog:** NP-0812 to NP-0830 (19 features)
- **Hints:**
  - Extend `LinearGradientFill` and `RadialGradientFill` (radial gains aspect ratio and angle) and add `ConicGradientFill` and `RectangularGradientFill` under `Photon.Nodus.Core/Models/Fills/`; conic gradients are B-003's third item.
  - `GradientStop` gains `PaintColor`, opacity, and `Midpoint` (0 to 100); arrangement maps to the existing `GradientSpreadMode` Pad, Repeat, Reflect.
  - `GradientSampler` computes the color at t with acceleration, midpoints, smooth transitions, blend direction (Linear, Clockwise, Counterclockwise through HSB), and perceptual interpolation (OKLab, recorded in the XML doc comment).
  - Render: Skia linear, two-point conical, and `SKShader.CreateSweepGradient` shaders from a sampled 256-entry ramp; rectangular through an `SKRuntimeEffect` shader; dither through Skia's dithered paint; fountain steps quantize the ramp.
  - SVG write: native `<linearGradient>`/`<radialGradient>` with the sampled ramp as plain stops (so midpoints, acceleration, and HSB direction survive in any viewer), parameters in `nodus:gradient-*`; conic and rectangular fall back to a clipped group of 256 wedge or ring paths per the live-object contract.
  - Fill winding: `fill-rule` nonzero or evenodd surfaced in the panel and property bar.
  - Gradient panel (Ctrl+F9) bound to `GradientViewModel`: type, reverse, angle, aspect ratio, stop add, delete, and drag, presets (own curated JSON in app resources, filtered by the current fill), and Gradient from existing fill (the solid fill becomes the first stop).
  - Gradient swatches: Save to Swatches through §3's `AddSwatchCommand`.
  - Settings: `nodus.display.fountainSteps` (display preview steps, default 256) with a named consumer in `SkiaRenderer`.
  - Tests: `GradientSamplerTests` (acceleration, midpoint, HSB clockwise), `ConicFallbackTests`, `GradientPersistenceTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/gradients.svg` (every type and option) round-tripped element by element, with fallback rendering goldens from Inkscape 1.4 compared pixel by pixel within a stated tolerance; cheaper substitute that fails: writing conic gradients as linear, which the fallback golden rejects.

#### §8. The gradient tool, interactive fill, stroke gradients, and freeform gradients

- **Deliverable:** One on-canvas fill tool (the Gradient tool and the Interactive fill tool) with the annotator, gradients across several objects, stroke gradients within, along, and across, freeform gradients in points and lines modes, fill transforms, and the Edit Fill dialog.
- **Depends On:** §7
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/gradient/ (annotator, freeform, stroke gradient, Edit Fill dialog).
  - Job: a designer can place and shape any fill directly on the object. Consumer: the object's fill or stroke paint.
  - Treatment: a `FillTool` (G) drawing the annotator (drag to set direction, stops on the bar, double-click to add, drag off to delete, palette drops on handles) and freeform points and lines; a property bar fill picker; an Edit Fill dialog. Cheaper substitute that fails: numeric-only gradient editing in the panel.
  - Chrome: consume §7's `GradientViewModel`, the §2 picker, the property bar host (`D02 T07 §8`), and the tool manager. Do not keep a second stop model for the annotator.
- **Runs:** `Requires: display-session -- on-canvas handles need an interactive desktop`
- **Catalog:** NP-0831 to NP-0844 (14 features)
- **Hints:**
  - `Photon.Nodus.Core/Tools/FillTool.cs` (G) with `GradientAnnotatorOverlay`; View > Show Gradient Annotator toggles it (settings key `nodus.view.gradientAnnotator`).
  - Drag across a multi-object selection applies one gradient in user space across the union bounds (`gradientUnits="userSpaceOnUse"`), one command.
  - Stroke gradients: within (native SVG), along and across as `nodus:stroke-gradient` with the fallback of the stroke expanded to a filled outline carrying a mapped gradient or segmented strips.
  - `FreeformGradientFill`: points (color, spread) and lines (curves of stops) interpolated by inverse-distance weighting in an `SKRuntimeEffect` shader; fallback is the fill expanded to a subdivided flat-shaded mesh group.
  - Fill transform: W, H, X, Y, skew, rotate, and free scale and skew written as `gradientTransform`/`patternTransform`.
  - Drop palette colors on a handle to add or replace a stop, Ctrl+drop mixes.
  - `EditFillDialog` with Uniform, Fountain, Pattern, Texture, and Procedural pages (the Pattern and Texture pages bind §10 and §11 models when present, disabled with that section named until then).
  - Uniform fill, No fill, Copy fill (click another object), Save fill as new (hands to §11's fill library when shipped, otherwise to gradient swatches).
  - Default fill for new objects written through `DocumentDefaults` (settings keys `nodus.defaults.fill.*`); §15's Change Document Defaults dialog later owns the chooser.
  - Tests: `FillToolTests` (drag sets endpoints; multi-object uses user space), `FreeformGradientTests`, `StrokeGradientFallbackTests`.
- **Proof:** Unit tests plus a format fidelity round trip of `tests/fixtures/nodus/svg/freeform-and-stroke-gradients.svg` with fallback goldens from Inkscape 1.4, and a driven annotator run captured; cheaper substitute that fails: freeform gradients saved as a flat color, which the golden rejects.

#### §9. Gradient mesh and mesh fill

- **Deliverable:** Mesh objects of Coons patches with per-node color and opacity, the Mesh tool (Illustrator mesh and Corel mesh fill in one tool), Create Gradient Mesh, expand gradient to mesh, and mesh to paths.
- **Depends On:** §7
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/mesh/.
  - Job: a designer can paint photoreal color flow by editing mesh points and patches. Consumer: the object's fill.
  - Treatment: a Mesh tool (U, M) that adds points on click, deletes with Alt-click, reshapes nodes and handles, selects by rectangle or freehand marquee, and takes dropped colors; Create Gradient Mesh dialog. Cheaper substitute that fails: a radial gradient approximation.
  - Chrome: consume the tool manager, the §2 picker, the property bar host, and the suite history. Do not add a second node-editing overlay; derive from the node edit tool's handle overlay.
- **Runs:** `Requires: display-session -- the mesh tool needs an interactive desktop`
- **Catalog:** NP-0845 to NP-0856 (12 features)
- **Hints:**
  - `Photon.Nodus.Core/Models/Fills/MeshFill.cs`: rows by columns grid of nodes (position, two handles per direction, `PaintColor`, opacity), patches derived.
  - Render with Skia `SKCanvas.DrawPatch` (cubic Coons patch with corner colors), subdividing for smooth mesh color (bicubic) versus flat (bilinear).
  - SVG: parameters in `nodus:mesh`; the plain fallback is the mesh expanded to a group of subdivided flat-shaded quads (8 by 8 per patch, setting `nodus.mesh.fallbackSubdivision`).
  - `MeshTool` (U, M): click adds a row and column through the point, Alt-click deletes, drag nodes and handles, rectangular or freehand selection (Alt toggles), drop colors on patches and nodes, Ctrl+drop mixes.
  - Property bar: grid size (columns, rows), add and delete intersection, smooth mesh color, transparency for selected nodes, Clear mesh.
  - `CreateGradientMeshDialog`: rows, columns, appearance Flat, To Center, To Edge, highlight percent.
  - Expand gradient to mesh (linear and radial become fitted meshes) and Convert mesh to paths (outline path) as commands.
  - Settings: `nodus.mesh.defaultRows` and `nodus.mesh.defaultColumns` (default 3 by 3) read by `MeshTool`.
  - Performance: a 20 by 20 mesh redraws within the frame budget while dragging a node.
  - Tests: `MeshFillTests` (node insert keeps colors), `MeshFallbackTests`, `CreateGradientMeshTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/mesh.svg` round-tripped element by element, with the flat-quad fallback rendered by Inkscape 1.4 compared within a stated tolerance; cheaper substitute that fails: saving the mesh as its average color, which the golden rejects.

#### §10. Pattern fills and pattern editing

- **Deliverable:** Vector, bitmap, and two-color pattern fills with grid, brick, and hex tile types, mirror and offset, pattern transforms, and a pattern editing mode with the Pattern Options panel and tile tool, written as native SVG `<pattern>`.
- **Depends On:** §1, D02 T07 §1
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/patterns/.
  - Job: a designer can turn artwork into a seamless repeating fill and edit it in place. Consumer: fills, strokes, pattern transparency (§20), and swatches (§3).
  - Treatment: Object > Pattern > Make opens pattern editing mode with tile copies, dimmed copies, the tile edge, and a Pattern Options panel; the Properties panel edits tile size, origin, skew, rotate, mirror, and offsets. Cheaper substitute that fails: a pattern that only repeats on a grid.
  - Chrome: consume isolation mode (`D02 T07 §7`) for editing, the §3 swatch model, the Transform panel options (`D02 T08 §12`), and the theme. Do not build a second isolation mode.
- **Runs:** `Requires: display-session -- pattern editing mode needs an interactive desktop`
- **Catalog:** NP-0857 to NP-0874 (18 features)
- **Hints:**
  - Extend `PatternFill` with tile content (element list or embedded image), `TileType` Grid, BrickByRow, BrickByColumn, HexByColumn, HexByRow, brick offset, width, height, H and V spacing, overlap order, mirror H and V, row or column offset percent, `TransformWithObject`, origin, skew, rotate.
  - `SvgExporter` writes `<pattern>` (it writes none today); brick, hex, and mirrored layouts are written exactly as a larger native tile containing the offset or mirrored copies, parameters in `nodus:pattern-*`.
  - `MakePatternCommand` (Object > Pattern > Make, Edit > Define Pattern, Object > Create > Pattern Fill) creates a pattern swatch from the selection; Edit Pattern (Shift+Ctrl+F8) reopens it.
  - `PatternEditMode` on isolation mode: copies 3 by 3 or 5 by 5, dim copies percent, show tile edge, show swatch bounds, tile edge color, Save a Copy, Done, Cancel.
  - `PatternOptionsPanel.xaml` and `PatternTileTool` (resize the tile on canvas).
  - New pattern source from a selected document area or an image file; two-color patterns (monochrome tile with front and back colors).
  - Bitmap pattern tile adjustments: radial or linear seamless blend, edge match, brightness, luminance, and color, computed once into the tile image by `BitmapTileAdjuster` (plain SVG then carries the adjusted tile).
  - Transform patterns independently: the Transform panel's Transform Patterns and Transform Objects options, and tilde-drag, writing `patternTransform`.
  - Tests: `PatternTileLayoutTests` (brick and hex offsets), `PatternPersistenceTests`, `MakePatternCommandTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/patterns.svg` (every tile type, mirror, bitmap, two-color) round-tripped element by element, with Inkscape 1.4 render goldens compared within a stated tolerance; cheaper substitute that fails: brick tiles written as a plain grid, which the golden rejects.

#### §11. Texture and procedural fills, and the fill library

- **Deliverable:** Procedural texture fills and procedural pattern fills (the PostScript-fill equivalent) with editable parameters, texture transparency, and a fill library with a picker (sources, search, filter, sort, favorites, tags, aliases) and a saved fill file.
- **Depends On:** §10
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/fills/ (fill picker, texture page).
  - Job: a designer can find, apply, tweak, and save any fill from one picker. Consumer: fills and transparency masks.
  - Treatment: a fill picker popup on the property bar and Properties panel with content source, search, category filter, sort, thumbnail size, recent 25, favorites, and context actions; texture and procedural pages with live parameter previews. Cheaper substitute that fails: a flat list of built-in presets with no search or user folder.
  - Chrome: consume the §8 Edit Fill dialog pages, the theme, the settings store, and the app-data paths. Do not add a second library index next to the asset library (`D02 T06 §11`); the fill index follows its folder conventions.
- **Runs:** `Requires: display-session -- the picker needs an interactive desktop`
- **Catalog:** NP-0875 to NP-0891 (17 features)
- **Hints:**
  - `Photon.Nodus.Core/Fills/Procedural/TextureFill.cs`: noise-based textures (clouds, water, minerals, cells) with per-texture parameters (softness, density, brightness, colors), resolution, and tile size.
  - Persist textures as native SVG filter chains (`feTurbulence`, `feColorMatrix`, `feComponentTransfer`) where they express the texture, parameters in `nodus:texture`, otherwise an embedded tile image at the stated resolution.
  - `ProceduralPatternFill` replaces PostScript fills: parametric vector generators (hatching, bricks, dots, grids, weave) with size, line width, and gray levels, expanding to a native `<pattern>`.
  - Texture transparency: the same texture used as a luminance mask (hooked into §20's mask model when it ships, disabled with §20 named until then).
  - Fill library under `%LOCALAPPDATA%\Rizonesoft\Nodus\Fills\` of `.nodusfill` files (SVG with `nodus:` metadata: title, language, category, tags, favorite) and `fills-index.json`; Reindex rebuilds it.
  - `FillPicker` control: content source (All, a pack, an alias, Recent 25, Favorites), keyword search, category filter, sort by name, created, modified, browse recursively, thumbnail tooltip, thumbnail size slider (key `nodus.fills.thumbnailSize`), resizable popup.
  - Aliases to local, network, or removable folders (Create, Rename, Open folder location, Browse to moved folder, Remove); an unreachable alias is refused by name with Browse offered.
  - Favorite, Properties and tags dialog, Delete (to the Recycle Bin), and Save custom fill or transparency.
  - The Corel `.fill` binary is not read (undocumented); the Nodus fill file is SVG.
  - Tests: `FillIndexTests` (search, filter, recent), `TextureFillPersistenceTests`, `ProceduralPatternTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/fills/` (textures and procedural fills saved as `.nodusfill` and inside an SVG) with Inkscape 1.4 render goldens for the filter-chain textures within a stated tolerance, plus `FillIndexTests`; cheaper substitute that fails: textures saved as an unparameterized bitmap, which the reopen-and-edit assertion rejects.

#### §12. The Stroke panel: caps, joins, alignment, dashes, arrowheads, and line styles

- **Deliverable:** A complete stroke model (weight and units, caps, joins, miter limit, alignment, dashes with three pairs and dash adjustment, arrowheads with attributes and presets, behind fill, scale with object, calligraphic nib, overprint) with the Stroke panel, Outline Pen dialog, and outline commands.
- **Depends On:** §1
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/stroke/.
  - Job: a designer can set every outline property, including arrowheads and dashes, and see it drawn exactly. Consumer: every stroked object and the SVG it saves.
  - Treatment: a Stroke panel (Ctrl+F10) and an Outline Pen dialog (F12) bound to one view model, an outline flyout of preset widths, arrowhead pickers with an attributes dialog, and an Edit Line Style dialog. Cheaper substitute that fails: a width box and a dash string field.
  - Chrome: consume the §2 picker, the Properties panel host, `PresetService.StrokeWidths`, and the theme. Do not give the dialog and the panel separate models.
- **Runs:** `Requires: display-session -- the panel and dialogs need an interactive desktop`
- **Catalog:** NP-0892 to NP-0911 (20 features)
- **Hints:**
  - Extend `Stroke` with `PaintColor`, units, `StrokeAlignment` (Center, Inside, Outside), up to three dash and gap pairs, `DashAdjust` (Default, AlignToCorners, Fixed), `BehindFill`, `ScaleWithObject`, `NibStretch`, `NibAngle`, `Overprint`, and start and end `ArrowheadRef` with scale, align (tip beyond or at end), length, width, offset, mirror, and rotation.
  - SVG write: native `stroke-*`, `paint-order="stroke"` for Behind Fill, `vector-effect="non-scaling-stroke"` when not scaling, `<marker>` for arrowheads; alignment, dash adjust, and calligraphic nibs as `nodus:stroke-*` with the stroke expanded to a filled outline as the fallback.
  - `StrokeRenderer` in Desktop: inside and outside alignment by clipping a doubled stroke, dash adjust by recomputing the dash array per segment, calligraphic nib by sweeping an ellipse along the path.
  - `ArrowheadLibrary`: built-in `Arrowheads.svg` in app resources plus user presets under `%LOCALAPPDATA%\Rizonesoft\Nodus\Arrowheads\`; New, Edit, Delete presets and Object > Create > Arrowhead from the selection.
  - `StrokePanel.xaml` and `OutlinePenDialog.xaml` over `StrokeViewModel`; Swap arrowheads command; outline flyout with preset widths.
  - Line style presets and `EditLineStyleDialog` (click cells to place dashes), saved to settings key `nodus.stroke.lineStyles`.
  - Right-click a palette swatch sets outline color; None removes fill or stroke.
  - Default outline properties for new objects through `DocumentDefaults` (keys `nodus.defaults.stroke.*`).
  - Convert outline to object (Ctrl+Shift+Q) extends the existing Stroke to Path command (`PathOperationsService.StrokeToPath`) to honor alignment, dashes, arrowheads, and nibs.
  - `OutlineReplaceService` (match width, scale-with-object, overprint) for `D02 T16 §10`'s Find and Replace.
  - Tests: `StrokeModelPersistenceTests`, `StrokeAlignmentRenderTests`, `ArrowheadTests`, extend `StrokeConverterTests` and `PathOperationsTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/strokes.svg` (every cap, join, alignment, dash mode, arrowhead, nib) round-tripped element by element, with fallback rendering goldens from Inkscape 1.4 within a stated tolerance; cheaper substitute that fails: ignoring alignment on save, which the fallback golden rejects.

#### §13. The width tool and variable outlines

- **Deliverable:** Variable-width strokes from width points (side 1, side 2) edited with the Width tool and the Variable Outline tool, with saved width profiles and an expanded-outline fallback.
- **Depends On:** §12
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/width/.
  - Job: a designer can drag a stroke thicker or thinner at any point and reuse the shape as a profile. Consumer: the stroke and the width profile library.
  - Treatment: a Width tool (Shift+W, V) that adds width points on drag, Alt-drag for one side, Alt-drag point to copy, Shift for several, Delete removes, and a Width Point Edit dialog; a profile menu in the Stroke panel. Cheaper substitute that fails: a start-to-end taper only.
  - Chrome: consume §12's `StrokeViewModel`, the tool manager, and the settings store. Do not store profiles outside the settings store.
- **Runs:** `Requires: display-session -- the width tool needs an interactive desktop`
- **Catalog:** NP-0912 to NP-0919 (8 features)
- **Hints:**
  - `Photon.Nodus.Core/Models/WidthProfile.cs`: width points (position 0 to 1 along arc length, side 1, side 2, smooth or corner), max 450 pt per side.
  - `VariableStrokeOutliner` builds the filled outline by offsetting along normals from `SKPathMeasure` samples with cubic smoothing.
  - SVG: `nodus:width-profile` on the path; the fallback is the expanded filled outline.
  - `WidthTool` modifiers per the row list and multi-node editing; Width Point Edit dialog with side 1, side 2, total, lock ratio, and Adjust Adjoining Width Points.
  - Property bar: side 1, side 2, lock ratio, total, node position percent, Add node, Remove node, Clear nodes, Copy variable outline, Scale width with stroke.
  - Width profiles: Save, apply, Flip Along, Flip Across; stored under settings key `nodus.stroke.widthProfiles`.
  - Performance: a 1,000-node path with 20 width points re-outlines within the frame budget while dragging.
  - Tests: `WidthProfileTests` (flip, scale with stroke), `VariableStrokeOutlinerTests`, `WidthToolTests`.
- **Proof:** Unit tests plus a format fidelity round trip of `tests/fixtures/nodus/svg/variable-width.svg` whose fallback outline is compared against a committed golden path within 0.01 px; cheaper substitute that fails: a uniform stroke on save, which the golden comparison rejects.

#### §14. The Appearance panel: stacked fills, strokes, and effects

- **Deliverable:** A per-object appearance stack of multiple fills, strokes, and effect entries with its own opacity and blend per item, targeting at object, group, and layer level, the Appearance panel, and Expand Appearance.
- **Depends On:** §12, D02 T07 §1
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/appearance/.
  - Job: a designer can stack several fills and strokes on one path and edit each in place. Consumer: the renderer, the SVG writer, and the effect framework (`D02 T11 §1`).
  - Treatment: an Appearance panel (Shift+F6) listing the target's strokes, fills, opacity, and effects in stacking order with add, duplicate, delete, hide, reorder, clear, and reduce to basic. Cheaper substitute that fails: duplicating the path once per fill.
  - Chrome: consume the §2 picker, §7 gradients, §12 stroke panel, the Layers panel target (`D02 T07 §5`), and the suite history. Do not add a second stroke editor inside the panel; rows open §12's view model.
- **Runs:** `Requires: display-session -- the panel needs an interactive desktop`
- **Catalog:** NP-1038 to NP-1053 (16 features)
- **Hints:**
  - `Photon.Nodus.Core/Models/Appearance/AppearanceStack.cs` with `FillItem`, `StrokeItem`, and `EffectItem` (opacity, blend, visibility, own effects) on `VectorElement`, groups, and layers; the Appearance part of backlog B-003 lands here.
  - Renderer draws items in stack order; SVG writes the basic fill and stroke natively and extra items as a `<g>` of `<use>` copies carrying each paint, parameters in `nodus:appearance`.
  - Commands: Add New Fill (Ctrl+/), Add New Stroke (Ctrl+Alt+/), reorder, duplicate, delete, hide, Clear Appearance, Reduce to Basic Appearance, each one undo step.
  - Add New Effect (fx) is the entry point `D02 T11 §1`'s effect framework registers effects into; this section ships the menu host and the effect row with an empty registry state.
  - Targeting: the Layers panel target circle selects object, group, or layer appearance; layer appearance applies to all contents.
  - New Art Has Basic Appearance (settings key `nodus.appearance.newArtBasic`, default on) read by the drawing tools.
  - Apply Last Effect (Shift+Ctrl+E) and Last Effect (Alt+Shift+Ctrl+E) through a `LastEffectRecord` the effect framework fills.
  - Expand Appearance command turns stacks (and brushes and effects when present) into plain groups.
  - Copy Properties From dialog (outline pen, outline color, fill, text), right-drag menu Copy Fill Here, Copy Outline Here, Copy All Properties, and text fill and outline from the palette (whole object or selected characters).
  - Tests: `AppearanceStackTests`, `AppearancePersistenceTests`, `ExpandAppearanceTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/appearance.svg` (three fills, two strokes, layer opacity) round-tripped element by element, with Inkscape 1.4 render golden of the `<use>` fallback within a stated tolerance; cheaper substitute that fails: duplicated paths, which the reopen assertion (one element with a stack) rejects.

#### §15. Graphic styles, object styles, style sets, and default properties

- **Deliverable:** One style system covering Illustrator graphic styles and Corel object styles (typed styles, style sets, child styles, overrides, source indicators), default object properties per object type, style libraries, and style sheet import and export.
- **Depends On:** §14
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/styles/.
  - Job: a designer can save a look once, apply it everywhere, and change it in one place. Consumer: every linked object and the defaults every new object starts from.
  - Treatment: a Styles panel (Shift+F5) with a graphic-style thumbnail grid and an Object Styles tree (styles, style sets, child styles, default object properties), hover preview, source indicators in the Properties panel, and a Change Document Defaults dialog. Cheaper substitute that fails: styles that copy attributes once and never update.
  - Chrome: consume §14's appearance stack as the style payload, the shortcut manager for style shortcuts, the settings store, and the Properties panel host. Do not keep separate graphic-style and object-style models.
- **Runs:** `Requires: display-session -- the panel, hover preview, and dialogs need an interactive desktop`
- **Catalog:** NP-1054 to NP-1081 (28 features)
- **Hints:**
  - `Photon.Nodus.Core/Styles/StyleDefinition.cs` with typed parts (Outline, Fill, Transparency, Effects, TextFrame), `StyleSet`, parent and child inheritance, and per-object link plus local overrides (the same override pattern as `SymbolInstance`).
  - SVG: style definitions in `<defs>` as `nodus:style` elements; objects carry `nodus:style="id"` and always the resolved attributes, so plain viewers render correctly.
  - Create: New Style From object, New Style Set From object or selection, drag an object onto Style Sets, define from scratch, New Child Style and Child Style Set.
  - Manage: rename, duplicate, delete, merge, Add or remove style type in a set, Copy Properties From into a style, Redefine (Apply to Style) from the selection.
  - Apply: double-click, drag, context menu Apply Style, Alt-click adds to the current appearance, hover preview (transient render, no command).
  - Overrides: editing a styled attribute overrides locally; Revert to Style; Break Link to Style; source indicator squares (styled, unstyled, overridden) in the Properties panel.
  - Default Object Properties per type (artistic text, paragraph text, graphic, callout, dimension, artistic media, painterly brushstroke, QR code) in the document, with Update Defaults When Editing, Apply default properties, Set as New Document Default and Revert (settings keys `nodus.defaults.<type>.*`), and the Change Document Defaults dialog.
  - Select Objects Using Style; Assign Keyboard Shortcut through `ShortcutManager`.
  - Style libraries: Nodus ships its own graphic style library (including retro, neon, and old-school text looks for the quick-action row), Window > Graphic Style Libraries opens it; Override Character Color and text or square preview options.
  - Export and import style sheets as `.nodusstyles` (SVG with `nodus:` metadata) with selectable content; `.cdss` is not read.
  - Tests: `StyleInheritanceTests` (child override), `StyleLinkTests` (edit style updates 10 objects in one undo), `StyleSheetRoundTripTests`, `DefaultPropertiesTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/styles.svg` and `tests/fixtures/nodus/styles/sample.nodusstyles` round-tripped element by element, plus `StyleLinkTests`; cheaper substitute that fails: copy-once styles, which `StyleLinkTests` rejects.

#### §16. The brush engine, art brushes, and pattern brushes

- **Deliverable:** A brush engine that warps art along paths, with art and pattern brushes (corners, fits, colorization), the Brushes panel and options, the Artistic Media tool's preset and vector brush modes, and custom brushstroke files, persisted as `nodus:brush` with expanded-outline fallbacks.
- **Depends On:** §14, D02 T08 §3
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/brushes/.
  - Job: a designer can apply a brush to any path and keep the path editable. Consumer: stroked paths, the renderer, and the SVG writer.
  - Treatment: a Brushes panel (F5) with list and thumbnail views and Brush Options per type; the Artistic Media tool (I) with Preset and Vector Brush modes, category list, browse, save, and delete. Cheaper substitute that fails: brushes expanded at draw time, leaving no editable path.
  - Chrome: consume §14's appearance stack (a brush is a stroke item), the §13 width profiles for preset strokes, the tool manager, and the settings store. Do not build a second path-warp routine for scatter or calligraphic brushes in §17; they extend this engine.
- **Runs:** `Requires: display-session -- the panel and tool need an interactive desktop`
- **Catalog:** NP-0920 to NP-0935 (16 features)
- **Hints:**
  - Promoted from backlog B-010: `-> SOURCE: legacy-nodus-6` (its calligraphic brushes land in §17, SVG pattern fills in §10, and its Recolor dialog in §6).
  - `Photon.Nodus.Core/Brushes/BrushDefinition.cs` with `BrushKind` (Art, Pattern, Calligraphic, Scatter, Bristle, Image), `BrushLibrary` in document `<defs>`.
  - `SkeletalWarp`: maps art x to arc length and y to normal offset from `SKPathMeasure`, with Scale Proportionally, Stretch to Fit, Stretch Between Guides, direction, flip, and overlap adjust.
  - `PatternBrushTiler`: side, outer corner, inner corner, start, and end tiles; auto corners Auto-Centered, Auto-Between, Auto-Sliced, Auto-Overlap; fits Stretch, Add Space, Approximate Path.
  - Colorization None, Tints, Tints and Shades, Hue Shift with key color, applied at render.
  - SVG: `nodus:brush="id"` plus per-object options on the path; fallback is the expanded outlines as a group (B-010's "expanded to outlines on export").
  - `BrushesPanel.xaml`: apply, Brush Options, Options of Selected Object, Remove Brush Stroke; Convert brush strokes to outlines through §14's Expand Appearance.
  - Drawing tools (pen, pencil from `D02 T08 §3`) apply the active brush when one is selected in the panel.
  - `ArtisticMediaTool` (I): Preset mode (width-profile shapes along the drag), Vector Brush mode with category list including Custom, Browse for a brushstroke file, Save artistic media stroke from a selected object or group, Delete custom brushstroke; files under `%LOCALAPPDATA%\Rizonesoft\Nodus\Brushes\` as `.nodusbrush` (SVG).
  - Performance: re-warping a 1,000-segment path with an art brush stays within the frame budget during node drags.
  - Tests: `SkeletalWarpTests`, `PatternBrushTilerTests` (corner generation), `BrushPersistenceTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/brushes.svg` (art and pattern brushes with every corner and fit) round-tripped element by element, with the expanded fallback rendered by Inkscape 1.4 within a stated tolerance; cheaper substitute that fails: saving only the expanded outlines, which the reopen-as-live-brush assertion rejects.

#### §17. Scatter, sprayer, and calligraphic brushes, the paintbrush, and the blob brush

- **Deliverable:** Scatter (sprayer), calligraphic, image, and expression brushes on the §16 engine with stylus pressure, tilt, and bearing, plus the Paintbrush tool and the Blob Brush tool.
- **Depends On:** §16
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/brushes/ (sprayer, calligraphic, blob brush).
  - Job: a designer can paint natural strokes and scatter artwork with a stylus or mouse. Consumer: new brushed paths and filled blob shapes.
  - Treatment: a Paintbrush tool (B) and Blob Brush tool (Shift+B) with options dialogs; Artistic Media Sprayer, Calligraphic, and Expression modes; pressure, tilt, and bearing variations with mouse simulation. Cheaper substitute that fails: fixed-width strokes that ignore the stylus.
  - Chrome: consume §16's engine and panel, the freehand fitter (`D02 T08 §3`), the Pathfinder union (`D02 T08 §10`), and the tool manager. Do not write a second curve fitter.
- **Runs:** `Requires: display-session -- stylus and tool input need an interactive desktop`
- **Catalog:** NP-0936 to NP-0954 (19 features)
- **Hints:**
  - `ScatterBrush`: size, spacing, scatter, rotation, each Fixed, Random, or Pressure with min and max, rotation relative to page or path, seed persisted for determinism.
  - Sprayer options: objects per dab, spacing, spray order (random, sequential, by direction), size and size progression, rotation with increment, offset (alternating, left, random, right); Save custom spray pattern from objects, groups, or symbols.
  - `CalligraphicBrush`: angle, roundness, size with Fixed, Random, Pressure, Stylus Wheel, Tilt, Bearing, Rotation variations; the Artistic Media Calligraphic mode uses the same brush.
  - Image brush: an art brush whose art is an embedded raster.
  - `StylusInput` adapter over WPF `StylusPoint` (`PressureFactor`, `XTiltOrientation`, `YTiltOrientation`, `AzimuthOrientation`); Up and Down arrows simulate pressure with a mouse; Expression mode varies nib size, flatness, and rotation.
  - `PaintbrushTool` (B) with options: fidelity, fill new brush strokes, keep selected, edit selected paths within N pixels.
  - `BlobBrushTool` (Shift+B): outlines the swept nib and unions it with overlapping same-color paths (merge only with selection option), with size, angle, and roundness variations.
  - Stroke width, freehand smoothing, and scale-stroke-with-object options on the property bar (settings keys `nodus.brush.*`).
  - Tests: `ScatterBrushTests` (seeded determinism), `StylusInputTests` (recorded input trace), `BlobBrushTests` (merge with overlap).
- **Proof:** Unit tests over a committed recorded stylus trace (`tests/fixtures/nodus/input/stylus-trace.json`) asserting widths and unions, plus a format fidelity round trip of `tests/fixtures/nodus/svg/scatter-calligraphic.svg`; cheaper substitute that fails: ignoring pressure, which the trace width assertions reject.

#### §18. Bristle and painterly brushes, and brush libraries

- **Deliverable:** Bristle brushes (vector bristle strokes), painterly brushstrokes (pixel marks along an editable vector curve rendered by a Nodus-local Skia dab renderer), the brush picker, and brush libraries.
- **Depends On:** §16
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/painterly/.
  - Job: a designer can paint with natural-media brushes while keeping every stroke's path editable. Consumer: brushstroke objects, the renderer, and the SVG writer.
  - Treatment: a Painterly Brush tool (J) with a brush picker (categories, search, favorites, media tray), a brush-specific property bar and Properties tab, and bristle brush options in the Brushes panel. Cheaper substitute that fails: a fixed raster stamp baked into the document.
  - Chrome: consume §16's panel and engine, §17's `StylusInput`, the Layers panel (`D02 T07 §5`), and the settings store. Do not depend on `Photon.Core/Imaging` here (`D01 T03` ships in phase 9); the dab renderer is Nodus-local.
- **Runs:** `Requires: display-session -- painting and the picker need an interactive desktop`
- **Catalog:** NP-0955 to NP-0989 (35 features)
- **Hints:**
  - `BristleBrush`: shapes (Round Point, Flat Point, Round Blunt, Flat Blunt, Round Curve, Flat Curve, Round Angle, Flat Angle, Fan), size, bristle length, density, thickness, paint opacity, stiffness, expanded into semi-transparent vector strokes.
  - Bristle warning: a count of bristle strokes above settings key `nodus.brush.bristleWarnCount` (default 30) warns before print or flattening export.
  - `Photon.Nodus.Core/Brushes/Painterly/DabRenderer.cs` renders dabs into an `SKBitmap` along the curve with size, transparency, texture and strength, density, glow, and smoothing, deterministic by seed.
  - `PainterlyStroke` object: the vector curve, brush id, seed, dynamics samples, and the cached raster; SVG writes the path plus `nodus:painterly` and an embedded PNG `<image>` fallback.
  - Nodus ships its own brush set per category (acrylic, airbrush, charcoal, digital, fluid, glazing, gouache, inks, markers, oils, particles, pastels, pencils, sponges, watercolor) and paper textures; no Corel content.
  - `BrushPicker` control: collapsible categories, hover stroke preview, live search with count (Esc clears), favorites, media tray of three recent, unavailable-brush indicator.
  - Property bar and Properties tab: color (outline color, with a separate default), size (Shift-drag resize), transparency, texture, strength, density, glow, smoothing, simulate pressure, tilt direction, tilt angle, Reset, bounding box toggle, Clear brushstroke.
  - Behavior: applying a brush to selected paths replaces their outline; scaling rule (proportional 100 percent, non-proportional half); brush cursor; Layers panel icon, lock, rename; editing the curve re-renders; destructive operations (crop, knife, eraser, break apart, trim) split into a curve plus a bitmap with a report.
  - Brush libraries: Window > Brush Libraries (own libraries), Save Brush Library as `.nodusbrushes`, Duplicate, Delete, Select All Unused; the Artistic Media docker lists recently used strokes.
  - Tests: `DabRendererTests` (seeded determinism, alpha preserved, bounds), `PainterlyStrokeTests`, `BristleBrushTests`.
- **Proof:** Unit tests with committed snapshot goldens under `tests/fixtures/nodus/painterly/` (deterministic by seed, compared within a stated tolerance) plus property tests (bounds, alpha preservation), and a format fidelity round trip of a painterly SVG fixture; cheaper substitute that fails: a baked image with no curve, which the reopen-and-edit assertion rejects.

#### §19. Opacity and blend modes

- **Deliverable:** Opacity at object, group, layer, fill, and stroke level, the 16 standard blend modes plus Corel-only merge modes, the Transparency panel, and uniform transparency, rendered and persisted (today `BlendMode` is neither rendered nor saved).
- **Depends On:** §1
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/transparency/.
  - Job: a designer can make any object or paint see-through and blend with what is below. Consumer: the renderer, the SVG writer, and flattening (`D02 T13 §8`).
  - Treatment: a Transparency panel (Shift+Ctrl+F10) with opacity, blend mode menu (grouped like the competitors), and fill-only or outline-only scope. Cheaper substitute that fails: opacity only.
  - Chrome: consume the Properties panel host, the theme, and the suite history. Do not add a second opacity control on the property bar; bind the same view model.
- **Runs:** `Requires: display-session -- the panel needs an interactive desktop`
- **Catalog:** NP-0990 to NP-1018 (29 features)
- **Hints:**
  - Extend `BlendMode` with Hue, Saturation, Color, Luminosity (the W3C Compositing and Blending Level 1 set of 16) and Corel-only Add, Subtract, Divide, Texturize, Invert, LogicalAnd, LogicalOr, LogicalXor, Behind, RedChannel, GreenChannel, BlueChannel.
  - `SkiaRenderer` maps the 16 standard modes to `SKBlendMode` and the Corel-only modes to `SKRuntimeEffect` blenders; If Darker and If Lighter map to Darken and Lighten.
  - SVG write: `mix-blend-mode` (Inkscape 1.4 reads and writes it) and `isolation`; Corel-only modes as `nodus:blend` with the nearest standard mode written as the plain fallback and one line in the export report.
  - `fill-opacity` and `stroke-opacity` for fill-only and outline-only transparency; `opacity` for objects, groups, and layers.
  - `TransparencyPanel.xaml` with opacity slider and field, blend menu, and scope (fill, outline, both); uniform transparency tint from a palette color.
  - Commands: `SetOpacityCommand`, `SetBlendModeCommand`, Copy transparency (click source), No transparency.
  - Tests: `BlendMathTests` (each mode's formula against W3C definitions on known pixel pairs), `BlendPersistenceTests`, `BlendRenderTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/blend-modes.svg` (all 16 standard modes plus Corel-only modes) round-tripped element by element, with Inkscape 1.4 render goldens of the standard modes compared pixel by pixel within a stated tolerance; cheaper substitute that fails: dropping `mix-blend-mode` on save, which today's writer does and the round trip rejects.

#### §20. Opacity masks, fountain and pattern transparency, knockout, and feather

- **Deliverable:** Opacity masks (make, release, clip, invert, disable, unlink, edit), fountain and pattern transparency with the Transparency tool, isolate blending, knockout groups, freeze transparency, and feather.
- **Depends On:** §19, §7, §10, §11
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/transparency/ (masks, transparency tool, feather dialog).
  - Job: a designer can fade, mask, and knock out artwork with editable masks. Consumer: the renderer, the SVG writer, and flattening (`D02 T13 §8`).
  - Treatment: mask thumbnails in the Transparency panel with Make Mask, Release, Clip, Invert, link toggle, and mask editing; a Transparency tool (Corel) with on-object handles for fountain and pattern transparency; a Feather dialog with preview. Cheaper substitute that fails: masks applied as a destructive raster.
  - Chrome: consume §19's panel, §7's gradient model and sampler for fountain masks, the theme, and isolation mode (`D02 T07 §7`) for mask editing. Do not build a second gradient editor for transparency.
- **Runs:** `Requires: display-session -- mask editing and the transparency tool need an interactive desktop`
- **Catalog:** NP-1019 to NP-1037 (19 features)
- **Hints:**
  - `OpacityMask` on `VectorElement`: mask art, clip, invert, enabled, linked; SVG native `<mask>` (luminance), invert through an `feColorMatrix` inside the mask, clip by a mask-bounds `clipPath`, parameters in `nodus:mask-*`.
  - Commands: Make Mask, Release, Clip, Invert, Disable or Enable, Link or Unlink, Edit Mask (enters isolation on the mask art).
  - New masks defaults: settings keys `nodus.transparency.newMasksClip` and `nodus.transparency.newMasksInvert`.
  - Isolate blending writes `isolation: isolate`; knockout group and opacity-and-mask-define-knockout as `nodus:knockout` with a pre-composited `<image>` fallback and a report line.
  - Fountain transparency (linear, elliptical, conical, rectangular) as a gradient mask reusing §7's types with nodes, midpoint, repeat, mirror, reverse, steps, acceleration, smooth, and transform (W, H, X, Y, skew, rotate, free scale).
  - Pattern transparency (vector, bitmap, two-color) and tile options as a pattern mask; binds §10's pattern model when present, disabled with §10 named until then.
  - `TransparencyTool` with on-object handles; palette colors dropped on nodes convert to grayscale opacity.
  - Transparency picker lists presets; saved presets go to §11's fill library when present.
  - Freeze transparency snapshots what lies beneath into a static image the object carries (undoable, with Unfreeze).
  - Feather (Effects > Blur > Feather): width, Linear, Curved, or Gaussian profile, preview; written as a mask with `feGaussianBlur` and an `feComponentTransfer` profile table (plain SVG renders it).
  - Tests: `OpacityMaskTests`, `FountainTransparencyTests`, `FeatherProfileTests`, `KnockoutFallbackTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/masks-and-feather.svg` round-tripped element by element, with Inkscape 1.4 render goldens compared within a stated tolerance; cheaper substitute that fails: masks rasterized into the art, which the reopen-and-release assertion rejects.

#### §21. Symbols: dynamic symbols, 9-slice scaling, registration, nesting, and linked libraries

- **Deliverable:** Dynamic symbols with instance overrides, 9-slice scaling, registration points, nested symbols, clones with a master, symbol management commands, and symbol libraries on disk and linked to documents with sync and broken-link recovery.
- **Depends On:** D02 T06 §11
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/symbols/ (extending `D02 T06 §11`'s Symbols panel capture).
  - Job: a designer can keep a symbol set consistent across documents while still customizing each instance. Consumer: every instance, the linked library files, and the SVG writer.
  - Treatment: the Symbols panel from `D02 T06 §11` gains search, replace, reset, select instances and unused, delete unused, rename, world-unit scaling, library import and link, and a linked-library list with sync, edit, remove, restore, and a broken-link icon. Cheaper substitute that fails: instances that are copied geometry.
  - Chrome: consume `SymbolLibraryService` and the asset library conventions from `D02 T06 §11`, isolation mode (`D02 T07 §7`), the Transform panel's registration option (`D02 T08 §12`), and the drawing scale (`D02 T07 §9`). Do not build a second library folder scheme.
- **Runs:** `Requires: display-session -- the panel and symbol editing need an interactive desktop`
- **Catalog:** NP-1082 to NP-1107 (26 features)
- **Hints:**
  - Dynamic symbols: `SymbolInstance.Overrides` carries appearance overrides; SVG writes `<use>` (today no instance is written) with overridden presentation attributes and `nodus:override`, expanding to a copy only where `<use>` inheritance cannot express the override.
  - 9-slice: `Symbol.SliceGuides` (`nodus:slice`), with instance scaling that keeps corners and stretches edges; fallback expands scaled instances.
  - Registration point on `Symbol` and Transform around it (Use Registration Point for Symbol option).
  - Commands: Replace Symbol, Reset Transformation, Select All Instances, Select All Unused, Delete Symbol (with its instances), Delete Unused, Rename, Revert to Objects, Modify instance properties.
  - Nested symbols: instances inside symbol definitions, cycle refused by name.
  - Corel clones: `Clone` as a single-object `<use>` with per-property override flags; Select Master, Select Clones, Revert to Master dialog (fill, outline, path shape, transformations, bitmap color mask).
  - Symbol libraries are SVG files of `<symbol>` definitions under the asset library folders plus imported local or network folders (recursive, copy locally option); remove a library reference without deleting files.
  - Linked libraries: `nodus:library-link` (path and content hash); Edit opens the library document, Sync updates changed definitions, Remove link, Restore link by browsing, broken-link icon, Break Link makes a linked symbol internal.
  - Copy and paste symbol definitions between drawings and into an open library; Search by name or description; Scale to world units using the drawing scale.
  - Unsupported source objects (OLE, placed PDF or EPS, linked bitmaps, connectors, dimensions, guidelines, locked objects) are refused by name.
  - Corel Symbol Library (CSL) read and write goes through the CDR container code of `D02 T14 §6` and `D02 T14 §8`; this section registers the menu entries disabled with those sections named until they ship.
  - Tests: extend `SymbolTests`; add `NineSliceTests`, `LinkedLibrarySyncTests` (hash change triggers sync), `CloneRevertTests`.
- **Proof:** Format fidelity proof on `tests/fixtures/nodus/svg/symbols-dynamic.svg` (overrides, 9-slice, nested, registration) round-tripped element by element with Inkscape 1.4 render goldens, plus `LinkedLibrarySyncTests`; cheaper substitute that fails: copied geometry, which the reopen assertion (instances are `<use>`) rejects.

#### §22. Symbolism tools and the symbol sprayer

- **Deliverable:** The Symbol Sprayer and the seven symbolism tools (Shifter, Scruncher, Sizer, Spinner, Stainer, Screener, Styler) acting on symbol sets, with the Symbolism Tools Options dialog.
- **Depends On:** §21
- **Phase:** 6
- **Surface:** user-facing
  - Fidelity: new build, no baseline; captured to docs/captures/nodus/symbolism/.
  - Job: a designer can spray and then sculpt many symbol instances as one set. Consumer: the symbol set group and its instances.
  - Treatment: eight tools on one flyout with a circular brush cursor, pressure support, and a shared options dialog. Cheaper substitute that fails: a scatter command with no follow-up editing.
  - Chrome: consume §21's instances, §15's styles for the Styler, §17's `StylusInput`, and the tool manager. Do not duplicate §17's sprayer; symbol spraying places instances, not copies.
- **Runs:** `Requires: display-session -- brush-style tools need an interactive desktop`
- **Catalog:** NP-1108 to NP-1116 (9 features)
- **Hints:**
  - `SymbolSet` group (`nodus:symbol-set`) holding instances; plain SVG is a `<g>` of `<use>`.
  - `SymbolSprayerTool` (Shift+S): sprays the selected symbol by density and intensity; Alt removes.
  - `SymbolShifterTool` (move and restack), `SymbolScruncherTool` (gather, Alt scatter), `SymbolSizerTool` (grow, Alt shrink), `SymbolSpinnerTool` (rotate toward drag), `SymbolStainerTool` (tint toward fill, as an instance override), `SymbolScreenerTool` (opacity), `SymbolStylerTool` (applies the selected §15 style).
  - `SymbolismOptionsDialog`: diameter, intensity, pressure pen, density, method User Defined, Average, or Random per property, show brush size; settings keys `nodus.symbolism.*`.
  - One command per stroke of a tool; seeds stored for determinism.
  - Tests: `SymbolSprayerTests` (seeded placement count), `SymbolismToolTests` (each tool changes only its property).
- **Proof:** Unit tests `SymbolSprayerTests` and `SymbolismToolTests` over a seeded synthetic stroke, plus a format fidelity round trip of a sprayed set; cheaper substitute that fails: spraying copies instead of instances, which the `<use>` assertion rejects.

#### Sizing concerns

- §18 bundles two engines (vector bristles and the Nodus-local painterly dab renderer) with the brush picker and brush libraries; with 35 catalog features it will likely exceed 30 checklist items, and a split between bristle plus libraries and painterly should be considered at authoring.
- §5 (35 features: color styles, harmony editor, and the Color Guide) and §15 (28 features: one style system for graphic and object styles plus default object properties) are near the ceiling; hints group them, but the author should keep numbered sub-steps rather than extra checkboxes.
- §4 carries seven palette file formats, each owing a fidelity proof; if the Corel CPL and ACB readers prove large they are the natural split.

### todo/02-nodus/TODO-10-nodus-parity-type.md -- `nodus-parity-type`

- **Title:** "TODO-10 -- Nodus Parity: Type, Tables, and Graphs"
- **Phase(s):** 7
- **Goal:** Nodus sets type the way Illustrator 30.8 and CorelDRAW 2026 do: a HarfBuzz shaping engine with bidi, script runs, and font fallback under a rich text model of point, area, path, and vertical text; full character, OpenType, and paragraph formatting with composers and hyphenation; frames with columns, threading, and wrap; font management with substitution and embedding; text commands, styles, and writing tools; and live tables and graphs, all persisted in SVG with a `nodus:` live layer and a plain positioned-`<tspan>` fallback that Inkscape renders.
- **Current-state facts to verify (with claim candidates):**
  - Text is one element type, `SvgText`, holding a single `Text` string with one family, size, weight, and italic flag: no runs, no paragraphs, no frames. `<!-- claim: lines src/Nodus/Bezier.Core/Models/Elements/SvgText.cs = 191 -->`
  - The text tool exists (shortcut T) and creates point text only. `<!-- claim: lines src/Nodus/Bezier.Core/Tools/TextTool.cs = 460 -->`
  - The text tool has a test class with 22 tests. `<!-- claim: count "^\s*\[(Fact|Theory)\]" src/Nodus/Bezier.Tests/TextToolTests.cs = 22 -->`
  - The SVG reader flattens `<text>` to `element.Value`; neither the reader nor the writer knows `<tspan>` or `<textPath>`. `<!-- claim: count "tspan|textPath" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->` `<!-- claim: count "tspan|textPath" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->`
  - Rendering calls `canvas.DrawText` with an `SKFont` (5 call sites including rulers): no shaping, no kerning beyond Skia defaults, no fallback. `<!-- claim: count "canvas.DrawText\(" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 5 -->`
  - No shaping package is referenced anywhere and no text folder exists in the core project. `<!-- claim: count "HarfBuzz" Directory.Packages.props = 0 -->` `<!-- claim: absent src/Nodus/Bezier.Core/Text -->`
  - SkiaSharp is already a central package (4.152.1) that every Nodus project references through `src/Nodus/Directory.Build.props`, so HarfBuzzSharp and SkiaSharp.HarfBuzz must match its version line. `<!-- claim: count "SkiaSharp\" Version=\"4\.152\.1\"" Directory.Packages.props = 1 -->`
- **Inputs and XREFs:** D02 T06 §3 (area text, text on a path, text to outlines: this file extends it); D02 T07 §1 (live-object contract for tables, graphs, threads, and path text); D02 T07 §8 (Properties panel and property bar that host the text controls); D02 T07 §9 (rulers, units, baseline grid) and D02 T07 §11 (snapping engine that glyph snapping extends); D02 T09 §1, §7, §10, §12 (fills and strokes applied to text runs); D02 T09 §15 (object styles that character, paragraph, and frame styles join); D01 T02 §2 (settings store); D01 T02 §4 (suite history); D02 T06 §13 (Preferences dialog that surfaces the Type preferences); D02 T06 §17 (localization and screen-reader text); D02 T13 §9 and §14 (font collection and font embedding in PDF); D02 T14 §1 (SVG font handling options), D02 T14 §7 (CDR text import), D02 T14 §14 (office import that reuses §13's readers); D02 T15 §7 (grammar and AI text, not here); standards/nodus.md; Unicode UAX #9, #14, #24, #29 and their conformance test files; OpenType 1.9 specification; SVG 2 text chapter.
- **Adjacency:** list=applicable (font list with filters and search, Glyphs panel, Font Sampler, style panels, find and replace results); document=applicable @ D02 T13 §14 (text reaches print and PDF through the PDF writer with embedded or outlined fonts); settings=applicable @ D02 T06 §13 (every Type, hyphenation, writing-tools, and table preference goes through the settings store and shows in Preferences); reporting=applicable (Find Font list with save, text statistics, font substitution report on open); notifications=applicable (font enumeration, text import, spell check, and fit-text-to-frame progress in the status strip with cancel); permissions=applicable (fsType embedding refusals, missing spelling language refused by name, Type 1 fonts refused by name, read-only placeholder file); audit=applicable (every text edit, format change, substitution, and table or graph edit is one undoable command with one Serilog line); exchange=applicable (SVG text round trip, TXT, RTF, DOC, DOCX import, TXT export, XLS and XLSX tables, tab-delimited graph data, custom placeholder file, user word lists); reverse=applicable (undo for every edit, release threading, unmerge, break apart, remove text frame, revert substitution, straighten text)

#### §1. The text shaping engine: HarfBuzzSharp, bidirectional text, script runs, and font fallback

- **Deliverable:** A Nodus-local shaping and layout core under `Photon.Nodus.Core/Text/` that turns Unicode text plus attributes into positioned glyph runs with bidi, script itemization, line breaking, and font fallback, rendered through `SKTextBlob`.
- **Depends On:** D02 T06 §3
- **Phase:** 7
- **Surface:** no surface of its own (its three preferences surface in the Preferences dialog of D02 T06 §13; the anti-aliasing option surfaces in §4's Character panel)
- **Runs:** none (headless unit tests against committed fonts)
- **Catalog:** NP-1129 to NP-1133 (5 features)
- **Hints:**
  - Add HarfBuzzSharp and SkiaSharp.HarfBuzz (MIT) to `Directory.Packages.props` on the SkiaSharp 4.152 line, with a `docs/dev/decisions.md` row (license checked against GPL-3.0, Nodus-local until Imago text layers in backlog B-018 are promoted, then moved to `Photon.Core/Text/`).
  - `ScriptItemizer` (UAX #24 script runs with common and inherited resolution), `BidiResolver` (UAX #9, own managed implementation), and `LineBreaker` (UAX #14) under `Photon.Nodus.Core/Text/Unicode/`, with the Unicode data tables generated at build from the committed UCD files.
  - `TextShaper` wraps `HarfBuzzSharp.Font` per typeface and size, shapes one run per (script, direction, font, language, features) and returns `ShapedRun` (glyph ids, clusters, advances, offsets); language comes from the run's language attribute.
  - `FontCatalog` enumerates installed fonts through `SKFontManager.Default` on a background task with cancellation and reads OS/2, name, fvar, STAT, GSUB, GPOS, COLR, CPAL, and SVG tables via `Face.ReferenceTable` into a `FontFaceInfo` cache persisted under `%LOCALAPPDATA%\Rizonesoft\Nodus\FontCache\` and invalidated by file timestamp.
  - Supported formats: OTF (CFF and CFF2), TTF, TTC, variable (fvar), COLR v0 and v1, OpenType SVG, and sbix or CBDT emoji; Type 1 (PFB, PFM) is detected and reported by name as unsupported, never silently substituted.
  - `FontFallbackChain`: requested family, then document fallback list, then `SKFontManager.MatchCharacter` per missing cluster; when the setting `Nodus.Type.MissingGlyphProtection` (default true) is on, a cluster the requested font lacks renders from fallback and is flagged for §3's substituted-glyph highlight.
  - `TextLayoutEngine` lays out a paragraph into lines of visual runs, caches shaped paragraphs keyed by content hash and attributes, and re-shapes only the edited paragraph: budget 16 ms per keystroke in a 10,000-character story and 2 s to lay out a 1,000-text-object document.
  - Rendering: `SkiaRenderer` draws text through `SKTextBlob` built from shaped runs instead of `canvas.DrawText`; anti-aliasing per text object maps None, Sharp, Crisp, Strong to `SKFontEdging` plus `SKFontHinting`; `Nodus.Type.FractionalWidths` (default true) toggles `SKFont.Subpixel` and linear metrics versus system layout.
  - Inline IME: a `TextInputBridge` in `Photon.Nodus.Desktop` handles WPF `TextComposition` events so composition strings render inline with underline at the caret when `Nodus.Type.InlineInput` (default true), otherwise in the IME window.
  - Outlines for export and Create Outlines come from the shaped glyph ids through `SKFont.GetGlyphPath`, replacing the per-string `GetTextPath` path of D02 T06 §3.
  - One Serilog Information line per font catalog rebuild (count, elapsed) and per fallback decision summary on document open.
  - Tests in `tests/Photon.Nodus.Tests/Text/`: `BidiConformanceTests` over `BidiCharacterTest.txt`, `LineBreakConformanceTests` over `LineBreakTest.txt`, `ShaperGoldenTests` comparing glyph ids and advances with `hb-shape` output from HarfBuzz (version recorded) for Latin, Arabic, Hebrew, Devanagari, Thai, and CJK fixtures under `tests/fixtures/nodus/text/`, using committed OFL fonts (Noto subsets).
- **Proof:** Unit test: `ShaperGoldenTests`, `BidiConformanceTests`, and `LineBreakConformanceTests` pass against hb-shape and Unicode goldens; cheaper substitute that fails: rendering through `canvas.DrawText` with Skia's default shaping, which breaks Arabic joining and Devanagari reordering in the goldens.

#### §2. The rich text model and text objects: point, area, path, and vertical

- **Deliverable:** A run-based text model (`TextStory` of paragraphs of character runs) behind point, area, and path text objects, with the text editing session, text commands on objects, and SVG persistence through `<text>`, `<tspan>`, `<textPath>`, and `shape-inside`.
- **Depends On:** §1
- **Phase:** 7
- **Surface:** Fidelity: Photon document window, text tool on the canvas -- docs/captures/nodus/main-window/ plus the Edit Text dialog, new build, no baseline; captured to docs/captures/nodus/edit-text/. Job: a designer creates, edits, selects, and converts text objects and styles runs with fill, outline, and background. Treatment: live editable runs with caret, selection, and per-run fill and outline; cheaper substitute that fails: one string per object with object-level formatting (today's `SvgText`). Chrome: consume the shared theme, icon catalog, history, settings store, and `Photon.UI` dialog base; do not duplicate the fill and stroke pickers of D02 T09 §2 and §12.
- **Runs:** Requires: display-session -- caret, drag selection, IME, and on-canvas text editing need an interactive desktop
- **Catalog:** NP-1134 to NP-1146 (13 features)
- **Hints:**
  - Model in `Photon.Nodus.Core/Text/Model/`: `TextStory`, `TextParagraph`, `TextRun`, `CharacterAttributes`, `ParagraphAttributes` (immutable, shared by reference), and `TextObject` (replaces `SvgText`) with `TextKind` Point, Area, Path; migration maps every existing `SvgText` and its tests.
  - Text tool: click creates point text, drag creates an area frame, click on an open or closed path attaches path text (hover cursors for each); Esc commits, Ctrl+Enter commits and returns to selection.
  - `TextEditSession`: caret, selection by drag, Shift+arrows, word and paragraph jumps (Ctrl+arrows), double-click word, triple-click paragraph, clipboard with rich runs, and IME from §1; the Pick tool selects the object and the text tool selects characters.
  - Commands, each an `IEditorCommand` with one Serilog line: `ConvertToAreaTextCommand`, `ConvertToPointTextCommand` (refused by name when the frame overflows or is threaded), `BreakTextApartCommand` (lines, words, characters as separate text objects keeping position), `UpdateLegacyTextCommand` (re-lays out imported flat text with the §1 engine and reports reflow deltas).
  - Edit Text dialog (Ctrl+Shift+T) in `Photon.Nodus.Desktop/Views/Text/EditTextDialog.xaml`: a rich text box bound to a clone of the story with font, size, and B/I/U, applied as one command.
  - Per-run fill (uniform, gradient, pattern from D02 T09) and outline (width, color, pen), and run background highlight, rendered behind glyph boxes; SVG writes run fill and stroke on `<tspan>` and highlight as a `nodus:highlight` run plus a fallback `<rect>` group.
  - Drag selected text within or between objects (move; Ctrl copies), and right-drag with a Copy here, Move here menu that can also create a new text object.
  - Inline graphics: a pasted object becomes an `InlineObjectRun` sized to the line with baseline offset, written as `nodus:inline` with an expanded positioned `<g>` fallback.
  - Hyperlink attribute on runs, written as `<a href>` around the `<tspan>` and exported to PDF link annotations by D02 T13 §16.
  - SVG round trip in `SvgImporter` and `SvgExporter`: `<text>` with `<tspan>` runs and CSS properties, SVG 2 `shape-inside` and `inline-size` for area text with a positioned-`<tspan>` fallback, `<textPath>` with `startOffset` for path text; `xml:space` and `white-space` preserved.
  - Fixtures under `tests/fixtures/nodus/svg-text/` (point, area, path, mixed runs, RTL) with goldens rendered by Inkscape 1.4 (version recorded).
  - Tests: `TextStoryTests` (insert, delete, split, merge runs), `TextEditSessionTests` (caret and selection over bidi text), `TextSvgRoundTripTests`.
- **Proof:** Format fidelity proof: `TextSvgRoundTripTests` opens, saves, and reopens each fixture and compares runs and attributes element by element and renders within tolerance of the Inkscape golden; plus a driven run capturing edit, convert, and break apart; cheaper substitute that fails: flattening runs to one string on save.

#### §3. Fonts: the font list, filters, samples, and missing-font substitution

- **Deliverable:** The font list control with previews, filters, search, and recents; the Font Sampler panel; missing-font detection with PANOSE and manual substitution, exceptions, and highlighting; Find Font; and font embedding on save with fsType permissions.
- **Depends On:** §1
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/font-list/, docs/captures/nodus/font-sampler/, docs/captures/nodus/font-substitution/. Job: find the right font fast and open any document without silent font loss. Treatment: a virtualized font list rendering each name in its face with live preview on hover and a filter pane; cheaper substitute that fails: a plain `ComboBox` of family names. Chrome: consume the shared theme, icon catalog, settings store, and `Photon.UI` list and dialog controls; the list is one `FontPicker` control reused by the property bar, Character panel, styles, and Find Font, never duplicated.
- **Runs:** Requires: display-session -- the font list, hover preview, and substitution dialog are driven surfaces
- **Catalog:** NP-1319 to NP-1352 (34 features)
- **Hints:**
  - `FontPicker` control in `Photon.Nodus.Desktop/Controls/Fonts/` over §1's `FontCatalog`: group by family (toggle), show Latin or native names, names in their own face, preview size slider, resizable popup with a hideable preview area, recent fonts at the top (`Nodus.Type.RecentFontsCount`, default 10, max 20), favorites (star) persisted in settings.
  - Filters: classification (serif, sans, script, display, monospace from PANOSE and OS/2 family class), similar fonts (PANOSE distance), favorites, recently added (install date), technology (OpenType, TrueType, variable, color), weight, width, style, character range (OS/2 Unicode ranges), OpenType feature, embedding rights, document fonts; Clear filters; keyword search across name, designer, and metadata.
  - Live preview: hovering a font applies it to the selected text as a transient render override, never a command, reverted on leave.
  - Change default font: with nothing selected, choosing a font writes the document default for point, area, dimension, and callout text as one command (dialog asks which types).
  - Script filter (All, Latin, Asian, Middle Eastern) limits font changes to runs of that script, and `Nodus.Type.MatchLatinFontForScript` picks a matching font for newly typed Asian or Middle Eastern text.
  - Missing fonts on open and import: `FontSubstitutionService` builds the list, the Substitute Fonts dialog offers PANOSE suggestion, manual choice (same script or all), several at once, permanent (rewrites runs) or session-only (render override stored in `nodus:font-substitute`), and save as exception.
  - Preferences through the settings store: `Nodus.Type.PanosePrompt` (Text, Text and styles, Never), exceptions list editor, `Nodus.Type.HighlightSubstituted` (fonts and glyphs, drawn as a pink overlay on the canvas only).
  - Missing fonts stay editable: runs keep the missing family name and edit with the substitute's metrics until resolved; Resolve Missing Fonts and Find Font (list document fonts with usage count, replace one or all, save list as TXT) share one dialog in `Views/Fonts/FindFontDialog.xaml`; Adobe Fonts activation is excluded (cloud).
  - Type 1 fonts found in a document or installed are reported by name on open with PANOSE or manual substitution; nothing is rasterized silently.
  - Embedding on save: `Nodus.Type.EmbedFontsOnSave` (default false) subsets used glyphs into `@font-face` data in SVG; `FontEmbeddingPolicy` reads OS/2 fsType (installable, editable, preview and print, restricted), refuses restricted fonts by name in a warning list (`Nodus.Warnings.FontsCannotEmbed`), and the Layers panel marks text using a preview-and-print-only embedded font as non-editable.
  - Font Sampler panel in `Views/Fonts/FontSamplerPanel.xaml`: single line, multiline, and waterfall views, zoom, add, remove, reorder, and edit samples, OpenType toggles per sample, copy or drag a sample onto the canvas as point text (one command).
  - Font matching on text import and on CGM, DXF, and PLT import calls the same substitution service with the importer's family and size hints.
  - Tests: `FontSubstitutionServiceTests` (PANOSE ranking, exceptions win, session-only leaves runs unchanged), `FontEmbeddingPolicyTests` (each fsType bit against committed test fonts), `FontFilterTests`.
- **Proof:** Unit test: `FontSubstitutionServiceTests` and `FontEmbeddingPolicyTests`; format fidelity proof: a fixture with a missing font saved with a session substitution reopens with the original family intact; driven run capturing the font list, filters, and substitution dialog; cheaper substitute that fails: silently falling back to Arial.

#### §4. Character formatting

- **Deliverable:** The Character panel and property bar controls for every character attribute, the touch type tool, keyboard increments, and the character straighten, align, and mirror commands, all as run attributes shaped by §1.
- **Depends On:** §2
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/character-panel/ and the text property bar in docs/captures/nodus/main-window/. Job: set any character attribute on a selection and see it immediately. Treatment: a dockable Character panel plus a contextual text property bar and on-canvas spacing handles; cheaper substitute that fails: a modal font dialog. Chrome: consume the Properties panel host of D02 T07 §8, the shared theme, icon catalog, history, settings store, `Photon.UI` numeric and unit boxes; do not duplicate the fill and stroke pickers.
- **Runs:** Requires: display-session -- panel, touch type, and spacing handles are driven on the canvas
- **Catalog:** NP-1147 to NP-1174 (28 features)
- **Hints:**
  - `CharacterPanel` (Ctrl+T, also the Text panel entry in the Window menu) in `Photon.Nodus.Desktop/Views/Text/`: family, style, size, leading (auto or fixed; also % of character height and % of size with `Nodus.Type.VerticalSpacingUnit`), kerning (Auto metrics, Optical, Metrics Roman only, manual, range), tracking, word spacing, horizontal and vertical scale, baseline shift, horizontal offset, rotation, language, and anti-aliasing.
  - Caps: All Caps, Small Caps (OpenType smcp, else synthesized), All Small Caps (c2sc plus smcp), Small Caps from Caps (c2sc), synthesized small caps, Titling Caps (titl); capital spacing (cpsp).
  - Position: superscript and subscript auto (sups, subs, else synthesized) and synthesized; underline styles (single, double, thin, thick), strikethrough (single, double), overline; No Break.
  - Optical kerning computed from glyph outlines in a `OpticalKerner` in `Photon.Nodus.Core/Text/Layout/` with a cached pair table per font and size.
  - Bold, italic, underline toggle buttons on the text property bar pick the family's real bold or italic face, synthesizing only when none exists (flagged in the tooltip).
  - Keyboard: Ctrl+Shift+> and < size, Alt+Up and Down leading, Alt+Left and Right kerning or tracking, Alt+Shift+Up and Down baseline shift, Ctrl+Num8 and Num2 size; increments `Nodus.Type.SizeIncrement`, `Nodus.Type.BaselineShiftIncrement`, `Nodus.Type.TrackingIncrement`; default text unit `Nodus.Type.TextUnit` (pt default).
  - Touch type tool (Shift+T) and shape-tool character nodes: move, scale, and rotate one character while text stays live, stored as per-character offsets and angle attributes.
  - Interactive spacing handles on the selected text object: drag horizontal for character spacing, Shift for word spacing, vertical for line spacing.
  - Commands: `StraightenTextCommand` (clears offsets and rotation), `AlignToBaselineCommand` (clears vertical offset), `MirrorTextCommand` (horizontal, vertical, by property bar or by dragging a middle handle past the opposite side).
  - SVG: run attributes as CSS on `<tspan>` (`letter-spacing`, `word-spacing`, `baseline-shift`, `text-decoration`, `font-variant-caps`, `font-kerning`, `rotate`, `dx` and `dy`), and Nodus-only attributes (optical kerning, synthesized caps, horizontal scale) under `nodus:` with positioned fallback.
  - Every attribute change is one `SetCharacterAttributesCommand` over the selected ranges with one Serilog line naming the attribute count and range count.
  - Tests: `CharacterAttributesLayoutTests` (tracking, kerning modes, scale, and baseline shift change advances as expected), `CapsSynthesisTests`, `CharacterSvgRoundTripTests` over `tests/fixtures/nodus/svg-text/character/` with Inkscape 1.4 goldens.
- **Proof:** Format fidelity proof: `CharacterSvgRoundTripTests` round trips every attribute; unit test `CharacterAttributesLayoutTests`; driven run capturing the Character panel on a selection; cheaper substitute that fails: object-level size and tracking that ignore character ranges.

#### §5. OpenType features, glyphs, variable fonts, and glyph snapping

- **Deliverable:** OpenType feature control per run (panel, on-canvas alternates, interactive indicator), the Glyphs panel, variable font axes, color and emoji fonts, and snap to glyph with glyph guides.
- **Depends On:** §4
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/opentype-panel/ and docs/captures/nodus/glyphs-panel/. Job: reach every typographic feature a font offers without knowing its tag. Treatment: an OpenType panel whose unavailable features are disabled per font, on-canvas alternates under the selection, and a searchable glyph grid; cheaper substitute that fails: a raw text box for feature tags. Chrome: consume the shared theme, icon catalog, history, settings store, `Photon.UI` controls, and the snapping engine of D02 T07 §11; no second snap system.
- **Runs:** Requires: display-session -- panels, on-canvas alternates, and glyph snapping are driven
- **Catalog:** NP-1175 to NP-1201 (27 features)
- **Hints:**
  - `OpenTypePanel` (Alt+Shift+Ctrl+T) and the OpenType group of the Character panel: liga, dlig, clig, hlig, calt, swsh, salt, titl, ordn, frac, numr, dnom, afrc, zero, ornm, case, hist, ss01 to ss20 (with the font's stylistic set names from the name table), figure styles (pnum, tnum, lnum, onum), and position; a feature the font lacks is disabled, read from §1's GSUB and GPOS cache.
  - Features are stored per run as a `FontFeatureSet` passed to HarfBuzz, written in SVG as `font-feature-settings` and `font-variant-*` CSS.
  - On-canvas alternates: selecting one glyph shows up to five alternates (GSUB lookups for that glyph) under it when `Nodus.Type.ShowCharacterAlternates` (default true); the interactive OpenType indicator arrow lists applicable features for a longer selection.
  - `GlyphsPanel` (Ctrl+F11, Text and Window menus): virtualized grid over the font's cmap and unmapped glyphs (gray background), filter by category, script, and OpenType feature, show all alternates, zoom, baseline preview (ascender, x-height, baseline, descender), info (name, glyph id, Unicode, feature, shortcut), jump by code point or key press.
  - Insert by double-click, drag, or copy; unmapped glyphs insert as a run with a glyph-id override (`nodus:glyph`) and a positioned fallback; recently used glyphs keep font and features, with remove and remove all, persisted in settings.
  - Variable fonts: axis sliders for every fvar axis plus named instances in the Character panel and property bar; stored as `font-variation-settings` and applied through `SKFont` variation position and HarfBuzz variations.
  - Color fonts: COLR v0 and v1, OpenType SVG, and sbix or CBDT emoji rendered through Skia, emoji ZWJ sequences shaped as one cluster, and Create Outlines keeping color layers as grouped paths.
  - Snap to glyph (View menu command and Character panel controls): baseline, x-height, cap height, glyph bounds, proximity guides, angular guides, and anchor points registered as a `GlyphSnapProvider` in the D02 T07 §11 engine; glyph guides drawn as smart guides; Japanese em box and ICF lines from the BASE table for CJK fonts.
  - Every feature and axis change is one undoable command with one Serilog line.
  - Tests: `FontFeatureShapingTests` (each feature changes glyph ids against hb-shape goldens on committed OFL fonts), `VariableFontTests` (axis values round trip and change advances), `GlyphSnapProviderTests`, `ColorFontRenderTests` (pixel golden within tolerance).
- **Proof:** Unit test: `FontFeatureShapingTests` against hb-shape goldens and `GlyphSnapProviderTests`; format fidelity proof for `font-feature-settings` and `font-variation-settings` round trip; driven run capturing both panels; cheaper substitute that fails: features that toggle in the panel but never reach HarfBuzz.

#### §6. Paragraph formatting, composers, justification, and hyphenation

- **Deliverable:** Paragraph attributes (alignment, indents, spacing), justification settings, single-line and every-line composers, hyphenation with language patterns and exceptions, hanging punctuation, and optical margin alignment.
- **Depends On:** §2
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/paragraph-panel/ and docs/captures/nodus/hyphenation/. Job: set professional paragraphs with even color and controlled breaks. Treatment: a Paragraph panel plus Hyphenation and Justification dialogs whose settings reflow live; cheaper substitute that fails: greedy line breaking with no hyphenation. Chrome: consume the Properties panel host, the shared theme, icon catalog, history, settings store, and `Photon.UI` controls.
- **Runs:** Requires: display-session -- the panel and dialogs are driven with live reflow
- **Catalog:** NP-1202 to NP-1218 (17 features)
- **Hints:**
  - `ParagraphPanel` (Alt+Ctrl+T): align left, center, right, justify with last line left, center, or right, justify all (force), towards and away from spine; left, right, and first-line indents (negative first line gives a hanging indent); space before and after.
  - `Composer` interface in `Photon.Nodus.Core/Text/Layout/` with `SingleLineComposer` (greedy with look-back) and `EveryLineComposer` (Knuth-Plass total-fit over the paragraph with badness, penalties, and demerits), toggled per paragraph (Alt+Shift+Ctrl+C).
  - Justification dialog: word spacing, letter spacing, and glyph scaling as min, desired, max; auto leading percent; single word justification; the composers honor these ranges.
  - Hyphenation: an own Liang hyphenator over TeX hyph-utf8 pattern files (license per language checked and recorded in `docs/dev/decisions.md`, bundled per language) in `Photon.Nodus.Core/Text/Hyphenation/`; Hyphenate toggle (Alt+Shift+Ctrl+H) per paragraph.
  - Hyphenation dialog: words longer than, after first, before last, hyphen limit, hyphenation zone (hot zone), bias slider, hyphenate capitalized words, hyphenate ALL CAPS words.
  - Default hyphenation language and exceptions in Preferences (`Nodus.Type.HyphenationLanguage`, `Nodus.Type.HyphenationExceptions` per language), plus the Custom Optional Hyphens dialog that stores per-word break points applied when typing, pasting, or importing.
  - Roman hanging punctuation per paragraph and Optical Margin Alignment per story (hangs punctuation and letter edges by a per-glyph protrusion table), drawn by the composer.
  - Language spacing between Latin and Asian characters as percent of a space; default text style: the document's default paragraph and character attributes for new text, edited through §12's styles.
  - SVG: alignment as `text-align` and `text-align-last` on area text, indents and spacing as `nodus:` paragraph attributes, with positioned `<tspan>` lines as the fallback so any renderer shows the composed lines.
  - Every paragraph change is one `SetParagraphAttributesCommand`; reflow of a 10,000-word story under every-line composer stays under 200 ms, cancelled and rescheduled on further typing.
  - Tests: `EveryLineComposerTests` (golden line breaks for a committed paragraph compared with TeX's output, version recorded), `HyphenatorTests` (pattern results against hyph-utf8 test words), `ParagraphSvgRoundTripTests`.
- **Proof:** Unit test: `EveryLineComposerTests` and `HyphenatorTests`; format fidelity proof `ParagraphSvgRoundTripTests` with Inkscape 1.4 renders of the fallback lines; cheaper substitute that fails: justification by stretching only word spaces with no composer.

#### §7. Tabs, drop caps, and bullets and numbering

- **Deliverable:** Tab stops (panel, dialog, ruler) with leaders, drop caps with hanging option, and bulleted, numbered, and multilevel lists with full bullet control.
- **Depends On:** §6
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/tabs-panel/ and docs/captures/nodus/bullets-numbering/. Job: build aligned tables of text, lists, and drop caps inside text objects. Treatment: a Tabs panel docked above the text frame and a Bullets and Numbering dialog with live preview; cheaper substitute that fails: literal bullet characters and spaces typed into the text. Chrome: consume the rulers of D02 T07 §9, the shared theme, icon catalog, history, settings store, and `Photon.UI` controls.
- **Runs:** Requires: display-session -- ruler tab stops and the panel are driven on the canvas
- **Catalog:** NP-1219 to NP-1237 (19 features)
- **Hints:**
  - `TabStop` (position, alignment left, center, right, decimal, align on character, leader string) on `ParagraphAttributes`; the layout engine resolves tabs per line after bidi.
  - Tabs panel (Shift+Ctrl+T) with position above text (snaps to the selected frame), repeat tab, snap to unit; the Tab Settings dialog lists the same stops for keyboard entry.
  - Ruler tab stops on the horizontal ruler of D02 T07 §9 while editing: click to add, drag to move, drag off to delete, each one command.
  - Insert Tab formatting code (also Tab key inside text) from §11's formatting-code menu.
  - Lists: `ListAttributes` (type bullet or number, level 1 to 9, glyph and font or paragraph font, color, size, baseline shift, glyph-to-text and frame-to-list distances, hanging alignment, numbering style 1, a, A, i, I with prefix and suffix, restart and continue) with multilevel by Increase and Decrease Indent.
  - Bullets and Numbering dialog (Text menu) editing one or several levels at once with the glyph picker from §5; bullet color from the palette when the bullet is selected.
  - Save list formatting as a paragraph style through §12 once it ships (the command is present and disabled with its owner named until then).
  - Drop caps: lines dropped, space after, hanging indent option, toggle on the Paragraph panel; laid out as a scaled first cluster with text wrap around it.
  - SVG: tabs, lists, and drop caps in `nodus:` paragraph attributes with the rendered bullets, leaders, and drop cap as positioned `<tspan>` fallback content flagged `nodus:generated` so re-import does not duplicate them.
  - Tests: `TabLayoutTests` (decimal and align-on-character alignment, leaders fill), `ListNumberingTests` (multilevel counters and restart), `DropCapLayoutTests`, `ListSvgRoundTripTests` (generated content never duplicated on reopen).
- **Proof:** Unit test: `TabLayoutTests` and `ListNumberingTests`; format fidelity proof `ListSvgRoundTripTests`; driven run capturing the Tabs panel and the dialog; cheaper substitute that fails: bullets stored as typed characters that break on reflow.

#### §8. Area text frames, columns, threading, and text wrap

- **Deliverable:** Area text frames of any shape with options (size, rows and columns, gutter, inset, first baseline, vertical alignment, auto size), threading across frames and pages, fit text to frame, frame commands, text wrap around objects, and baseline-grid alignment.
- **Depends On:** §6
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/area-type-options/ plus frame handles and thread overlays in docs/captures/nodus/main-window/. Job: lay out body copy across shaped frames, columns, and pages around images. Treatment: frames with in and out ports, overflow marker, flow arrows with page numbers, and draggable column handles; cheaper substitute that fails: separate unlinked text objects the user reflows by hand. Chrome: consume the shared theme, icon catalog, history, settings store, the Properties panel host, and `Photon.UI` dialogs; the live-object contract of D02 T07 §1 for threads.
- **Runs:** Requires: display-session -- ports, threading clicks, column drags, and wrap are driven on the canvas
- **Catalog:** NP-1238 to NP-1267 (30 features)
- **Hints:**
  - `TextFrame` on area `TextObject`: any closed path as the frame (Create Empty Text Frame from object, Insert-in-object pointer, Frame Type context menu and Layout toolbar buttons, Remove Frame), with background fill and border visibility (`Nodus.Type.ShowTextFrames`).
  - Area Type Options dialog: width, height, rows and columns with number, span, gutter, equal width (Column Settings table for per-column width and gutter), text flow order, right-to-left columns, inset spacing, first baseline (Ascent, Cap Height, Leading, x Height, Em Box, Fixed, Legacy) with minimum, vertical alignment (top, center, bottom, justify), auto size.
  - Auto size: `Nodus.Type.AutoSizeNewAreaText` and the frame toggle (bottom widget); auto adjust column width; Alt+corner drag scales text with the frame.
  - Threading: `TextThread` links frames into one story (click out port then a frame, path, or object; across pages via the page navigator), with Release Selection, Remove Threading, Unlink, and Redirect; overflow marker (red port) when text does not fit; thread lines and flow arrows with page numbers when `Nodus.Type.ShowTextThreads`.
  - `Nodus.Type.ApplyFrameFormattingTo` (all linked, selected only, selected and subsequent) governs frame edits on threads.
  - Fit Text to Frame scales point size across the thread by bisection until the last line fits (cancellable, reports the final size).
  - Frame commands: Combine text frames, Break Apart into columns, paragraphs, bullets, lines, words, or characters, Break Text Inside a Path Apart; each one command with one Serilog line.
  - Text wrap: Make and Release on any object with offset and invert, contour (straddle, left, right) or square (straddle, left, right, above and below) styles; the layout engine subtracts wrap regions line by line.
  - Align to Baseline Grid snaps line baselines to the document baseline grid of D02 T07 §9, overriding leading.
  - SVG: frames as SVG 2 `shape-inside` with `shape-padding`, threads as `nodus:thread` next and previous ids, wrap as `shape-subtract` plus `nodus:wrap`, columns as `nodus:columns`; fallback positioned `<tspan>` lines per frame so Inkscape shows the same breaks.
  - Budget: a 20-frame thread with 50,000 characters reflows in under 500 ms after an edit, incremental from the edited frame.
  - Tests: `ThreadLayoutTests` (overflow moves to the next frame, release keeps text), `ColumnLayoutTests`, `TextWrapTests` (contour and square exclusions), `FitTextToFrameTests`, `AreaTextSvgRoundTripTests` over `tests/fixtures/nodus/svg-text/area/` with Inkscape 1.4 goldens.
- **Proof:** Format fidelity proof: `AreaTextSvgRoundTripTests` with threads and wrap round trip and fallback lines matching the golden; unit tests `ThreadLayoutTests` and `TextWrapTests`; driven run capturing threading and overflow; cheaper substitute that fails: threads that break into independent frames on reopen.

#### §9. Type on a path options and effects

- **Deliverable:** Path text with effects (rainbow, skew, 3D ribbon, stair step, gravity), align to path, spacing, distance and offset, tick snapping, flip and mirror, on-canvas brackets, separation from the path, and legacy path text update.
- **Depends On:** §2
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/type-on-path/. Job: set text along any curve with control over orientation and placement. Treatment: live path text with start, center, and end brackets and a property bar mirroring the options dialog; cheaper substitute that fails: path text converted to outlines on placement. Chrome: consume the shared theme, icon catalog, history, settings store, and `Photon.UI` dialogs.
- **Runs:** Requires: display-session -- bracket drags and flip are driven on the canvas
- **Catalog:** NP-1268 to NP-1276 (9 features)
- **Hints:**
  - `PathTextLayout` in `Photon.Nodus.Core/Text/Layout/` places shaped clusters by arc length on the path (`SKPathMeasure`), for open and closed paths, extending the basic attach of D02 T06 §3.
  - Effects: rainbow (rotate to tangent), skew (vertical stays, horizontal follows), 3D ribbon (vertical stays, skew to tangent), stair step (baseline follows, no rotation), gravity (rotate toward the path's center).
  - Options dialog and property bar: effect, align to path (ascender, descender, center, baseline), spacing at curves, flip, distance from path, offset along path, tick snapping with increment, mirror horizontally, vertically, or both.
  - Start, center, and end brackets (Illustrator) and the red handle (CorelDRAW) slide text along or off the path; dragging the center bracket across flips; each drag records one command on mouse-up.
  - Fit Text to Path command and pointer: artistic text to open or closed paths, paragraph text to open paths, with preview while hovering.
  - `SeparateTextFromPathCommand` keeps the shaped appearance as point text with per-character offsets, and Straighten Text from §4 restores it.
  - Update Legacy Type on a Path re-lays out imported path text through the new layout and reports moved characters.
  - SVG: `<textPath href startOffset side method spacing>` for what SVG expresses, effect and distance under `nodus:`, and per-glyph positioned `<tspan>` fallback for skew, stair step, and gravity.
  - Tests: `PathTextLayoutTests` (each effect's glyph transforms against committed goldens), `PathTextSvgRoundTripTests` with Inkscape 1.4 renders.
- **Proof:** Format fidelity proof: `PathTextSvgRoundTripTests` round trips every effect and its fallback; unit test `PathTextLayoutTests`; driven run capturing bracket drag and flip; cheaper substitute that fails: rainbow only, with the other effects ignored on save.

#### §10. Vertical, CJK, and right-to-left type

- **Deliverable:** Vertical point, area, and path text, the Japanese composer with Mojikumi and Kinsoku, East Asian features and OpenType forms, and right-to-left and Indic composition with their Type preferences.
- **Depends On:** §6
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/vertical-cjk/ and docs/captures/nodus/mojikumi-kinsoku/. Job: set Japanese, Chinese, Korean, Arabic, Hebrew, and Indic text correctly, horizontally and vertically. Treatment: vertical layout with vertical alternates and rotation, CJK line-breaking rule sets, and RTL paragraphs with digit and kashida options; cheaper substitute that fails: horizontal text rotated 90 degrees. Chrome: consume the shared theme, icon catalog, history, settings store, `Photon.UI` dialogs; the Character and Paragraph panels gain sections behind `Nodus.Type.ShowAsianOptions` and `Nodus.Type.ShowMiddleEasternOptions`, never a second panel.
- **Runs:** Requires: display-session -- vertical tools, IME input, and the rule dialogs are driven
- **Catalog:** NP-1277 to NP-1290 (14 features)
- **Hints:**
  - Vertical type, vertical area type, and vertical type on a path tools; Type Orientation Horizontal or Vertical command and the property bar toggle, one command each.
  - Vertical layout in `TextLayoutEngine`: HarfBuzz vertical direction with vert and vrt2 features, vhea and vmtx metrics (vpal, halt, vhal alternates), upright CJK and rotated Latin runs.
  - Japanese composer: `JapaneseComposer` implementing Mojikumi spacing classes and Kinsoku Shori (push in or push out first, leading, following, overflow sets) with the Adobe-style presets as data, plus custom sets in the Mojikumi Settings and Kinsoku Shori Settings dialogs persisted in the document and exportable.
  - Corel-style Asian Line-Breaking Rules dialog (leading, following, overflow characters with reset) maps onto the same Kinsoku sets.
  - East Asian features: Tsume, Aki, Wari-Chu, Tate-Chu-Yoko, Moji-Gumi, Kurikaeshi Moji Shori, Burasagari; OpenType Asian widths (fwid, hwid, pwid, twid, qwid), forms (jp78, jp83, jp90, jp04, trad, expt, nlck), kana alternates (hkna, vkna), annotation forms (nalt), and vertical alternates and rotation.
  - Asian default font follows the IME: when the IME is active on new text, the run uses `Nodus.Type.DefaultAsianFont`.
  - Right-to-left: paragraph direction and the Middle Eastern and South Asian composers (digit type Arabic, Hindi, Farsi; kashida insertion for justification; diacritic positioning) and the Indic composer relying on §1's HarfBuzz shaping.
  - Language options preference (East Asian, Indic, Middle Eastern) shows or hides these panel sections without affecting documents.
  - SVG: `writing-mode: vertical-rl`, `text-orientation`, `direction`, `unicode-bidi`, and `text-combine-upright` for Tate-Chu-Yoko; Mojikumi and Kinsoku in `nodus:`; positioned fallback lines.
  - Tests: `VerticalLayoutTests` (vertical metrics and rotated Latin), `KinsokuTests` (no line starts with a prohibited character), `RtlParagraphTests` (kashida justification, digit substitution), `VerticalTextSvgRoundTripTests` with Inkscape 1.4 goldens on committed Noto CJK and Noto Naskh subsets.
- **Proof:** Unit test: `KinsokuTests`, `VerticalLayoutTests`, and `RtlParagraphTests`; format fidelity proof `VerticalTextSvgRoundTripTests`; driven run capturing vertical Japanese with IME input; cheaper substitute that fails: rotating a horizontal text object 90 degrees.

#### §11. Text commands: find and replace, change case, special characters, and placeholder text

- **Deliverable:** Find and replace for text content and text properties, change case, smart punctuation, insert special, whitespace, and break characters with shortcuts, show hidden characters, placeholder text, fit headline, encoding repair, text statistics, the reflow viewer, and imported-text placement.
- **Depends On:** §4
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/find-replace-text/, docs/captures/nodus/text-statistics/, docs/captures/nodus/text-encode/. Job: edit copy across a whole document quickly and precisely. Treatment: a non-modal Find and Replace panel with search range and property replacement, plus menu commands with shortcuts; cheaper substitute that fails: find only within the active text object. Chrome: consume the shared theme, icon catalog, history, settings store, the keymap of D02 T02 §8, and `Photon.UI` controls; object find and replace stays in D02 T16 §10.
- **Runs:** Requires: display-session -- the panel, shortcuts, and hidden-character display are driven
- **Catalog:** NP-1291 to NP-1310 (20 features)
- **Hints:**
  - `TextSearchService` in `Photon.Nodus.Core/Text/Commands/`: match case, whole word, backwards, include hidden and locked layers and objects, special codes (^t tab, ^p paragraph, ^n line break, ^m em dash, ^= en dash, ^- optional hyphen, ^s nonbreaking space), and search range (all pages, page range, pages, selection).
  - Find and Replace panel with Find Next (also Edit menu command), Replace, Replace All as one command; Replace Text Properties finds and replaces font, weight, and size across text objects.
  - Change Case: UPPERCASE, lowercase, Title Case, Sentence case, tOGGLE cASE (Shift+F3 cycles), culture-aware through the run's language.
  - Smart Punctuation dialog: ff, fi, fl ligatures, smart quotes per language, smart spaces, en and em dashes, ellipses, expert fractions, in selection or document, with a report of replacements.
  - Insert Formatting Code menu with shortcuts: em space (Ctrl+Shift+M), en space (Ctrl+Shift+N), quarter em, thin, hair, figure, punctuation spaces, nonbreaking space (Ctrl+Shift+Space), em dash, en dash, nonbreaking hyphen, optional hyphen (Ctrl+-), forced line break (Shift+Enter), column or frame break (Ctrl+Enter), and tab; symbols from the Glyphs panel.
  - Show Hidden Characters (Alt+Ctrl+I): spaces, tabs, returns, breaks, and end-of-story marks drawn as a canvas overlay, never exported.
  - Placeholder text: Fill with Placeholder Text on a selected or empty frame (fills to the frame's end, threads included), custom text from `%LOCALAPPDATA%\Rizonesoft\Nodus\placeholder.rtf` when present, and `Nodus.Type.FillNewWithPlaceholder`.
  - Fit Headline adjusts tracking so a single-line paragraph fills its frame width.
  - Text Encode dialog re-decodes runs from a chosen legacy code page (`System.Text.Encoding.CodePages`) with preview; Text Statistics dialog counts lines, words, characters, fonts, and styles for selection or document with copy to clipboard.
  - Text reflow viewer: a read-only panel showing the reading order that D02 T13 §16 will tag, one story per entry.
  - Imported-text placement cursor: click to place, drag to size a frame, Space for the default position, used by §13's import.
  - Tests: `TextSearchServiceTests` (special codes, whole word across runs, range filters), `ChangeCaseTests` (Turkish dotted i, German sharp s), `SmartPunctuationTests`, `TextStatisticsTests`.
- **Proof:** Unit test: `TextSearchServiceTests` and `ChangeCaseTests`; driven run capturing Replace All across two pages then undo in one step; cheaper substitute that fails: a find that misses matches split across runs.

#### §12. Character, paragraph, and frame styles

- **Deliverable:** Character, paragraph, and text frame styles as types in the object style system, with panels, overrides, redefine, load, keyboard shortcuts, and variable font instances in styles.
- **Depends On:** §6, D02 T09 §15
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/text-styles/. Job: format long documents consistently and change them in one place. Treatment: Character Styles and Paragraph Styles panels with override markers and a style options dialog; cheaper substitute that fails: presets that copy attributes once without a link. Chrome: consume D02 T09 §15's object style store and panel conventions, the shared theme, icon catalog, history, settings store; no second style store.
- **Runs:** Requires: display-session -- the panels, overrides, and shortcuts are driven
- **Catalog:** NP-1311 to NP-1315 (5 features)
- **Hints:**
  - Style types `CharacterStyle`, `ParagraphStyle` (includes indents, tabs, lists, hyphenation, composer, and a default character style), and `TextFrameStyle` (columns, inset, vertical alignment, fill) registered in D02 T09 §15's style store with based-on inheritance.
  - Character Styles and Paragraph Styles panels: new, new from selection, duplicate, delete (with replace-with prompt), apply, edit options dialog, keyboard shortcut per style through the keymap.
  - Runs and paragraphs keep a style reference plus local overrides; a plus marker shows overrides; Clear Overrides and Redefine Style from selection are one command each.
  - Load Styles from another SVG document (Nodus or Illustrator-compatible names) with conflict handling (rename, replace, skip).
  - A variable font instance (axis values) is saved in a character style and applied with it.
  - Save list as paragraph style enables the §7 command.
  - SVG: styles as CSS classes in a `<style>` block (`.nodus-cs-*`, `.nodus-ps-*`) plus `nodus:style` definitions for what CSS cannot express; runs reference classes, overrides stay inline.
  - Tests: `TextStyleInheritanceTests` (based-on chain, override precedence), `TextStyleSvgRoundTripTests` (styles and overrides survive save, Inkscape 1.4 renders match).
- **Proof:** Format fidelity proof: `TextStyleSvgRoundTripTests`; unit test `TextStyleInheritanceTests`; driven run capturing redefine updating every linked paragraph; cheaper substitute that fails: styles applied as copied attributes with no link.

#### §13. Writing tools, and text import and export

- **Deliverable:** Spell checking through the Windows Spell Checking API (dialog, as-you-type, word lists, languages), a WordNet 3.1 thesaurus, QuickCorrect, and text import (TXT, RTF, DOC, DOCX) and TXT export with the Importing and Pasting Text dialog.
- **Depends On:** §11
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/writing-tools/ and docs/captures/nodus/import-text/. Job: catch spelling errors, find better words, and bring copy from word processors without retyping. Treatment: a Writing Tools dialog with Spell Check, Thesaurus, and QuickCorrect tabs, squiggles while typing, and an import dialog choosing formatting treatment; cheaper substitute that fails: a spell check limited to one hard-coded English word list. Chrome: consume the shared theme, icon catalog, history, settings store, and `Photon.UI` dialogs; grammar checking is D02 T15 §7, not here.
- **Runs:** Requires: display-session -- squiggles, the dialogs, and the import cursor are driven; Needs: Windows spelling languages installed for the tested languages
- **Catalog:** NP-1353 to NP-1376 (24 features)
- **Hints:**
  - `ISpellCheckService` in `Photon.Nodus.Core/Text/Writing/` with `WindowsSpellCheckService` in `Photon.Nodus.Desktop` over the Windows Spell Checking API COM interfaces (`ISpellCheckerFactory`, `ISpellChecker2`); decision row: no package, Windows 8+ API; a language that is not installed is refused by name with a link to Windows language settings.
  - Check Spelling dialog (Ctrl+I, Text and Edit menus) over document, page, selection, paragraph, sentence, or word, with Replace, Auto Replace, Skip Once, Skip All, Add, language choice, and options (words with numbers, duplicates, irregular capitalization, recheck all, prompt before auto replace, beep).
  - Auto Spell Check squiggles drawn as a canvas overlay on runs, recomputed per edited paragraph off the UI thread; right-click offers suggestions and Add.
  - User word lists: `%LOCALAPPDATA%\Rizonesoft\Nodus\WordLists\*.txt` (up to 10 active, with replacements), plus Edit Custom Dictionary; main word lists map to installed Windows spelling languages.
  - Language assignment per run (Writing Tools, Language command) shown as a code in the status strip; check in another language.
  - Thesaurus: WordNet 3.1 database parsed by an own reader in `Photon.Nodus.Core/Text/Writing/WordNet/`, data shipped as an optional installer component with the WordNet license in `THIRD-PARTY-NOTICES`; synonyms, antonyms, related, type of, has types, part of, has parts, examples, history, insert or replace, options (auto look up, auto close); English only, refused by name for other languages.
  - QuickCorrect (Text, Writing Tools): capitalize sentences, correct two initial capitals, capitalize day names, auto hyperlinks for URLs, typographic quotes per language with custom pairs, replacement list while typing, add spell-check corrections, and Undo QuickCorrect as its own history entry.
  - Import text: TXT (encoding detection with override, extra carriage returns option), RTF by an own reader, DOCX through DocumentFormat.OpenXml (MIT), DOC through NPOI (Apache-2.0), each package with a decision row; WPD is backlog B-037; embedded WMF and EMF are placed as graphics when D02 T14 §11 ships and reported until then.
  - Importing and Pasting Text dialog: maintain fonts and formatting, maintain formatting only, discard fonts and formatting, force CMYK black, and a do-not-ask setting (`Nodus.Warnings.PasteTextFormatting`) re-enabled from Preferences; fonts pass through §3's matching.
  - Export TXT from the selected text objects (UTF-8 default, ANSI option).
  - Readers live in `Photon.Nodus.Core/Formats/Text/` so D02 T14 §14 reuses them; import of a 200-page DOCX runs with progress and cancel.
  - Tests: `RtfReaderTests`, `DocxTextImportTests`, `DocTextImportTests` against fixtures under `tests/fixtures/nodus/docx/`, `tests/fixtures/nodus/rtf/`, `tests/fixtures/nodus/doc/` with goldens from LibreOffice 25.x plain-text conversion (version recorded); `QuickCorrectTests`; `WordNetReaderTests`; `SpellCheckServiceTests` skipped with a named reason when en-US is not installed.
- **Proof:** Format fidelity proof: each text reader's fixture imports with runs, paragraphs, and fonts matching the LibreOffice golden; unit tests `QuickCorrectTests` and `WordNetReaderTests`; driven run capturing the spell check dialog; cheaper substitute that fails: importing DOCX as plain text with formatting silently dropped.

#### §14. Tables

- **Deliverable:** A live table object with the table tool, row, column, and cell editing, borders, margins, backgrounds, merge and split, cell text and images, text-table conversion, and table import from spreadsheets and word processors.
- **Depends On:** §8
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/tables/. Job: build and edit tabular layouts inside a drawing. Treatment: a table tool with row and column selection bars, a table property bar, and on-canvas cell editing; cheaper substitute that fails: a group of rectangles and text objects. Chrome: consume the shared theme, icon catalog, history, settings store, the Properties panel host, the stroke controls of D02 T09 §12, and `Photon.UI` dialogs; the live-object contract of D02 T07 §1.
- **Runs:** Requires: display-session -- cell selection, drag moves, and typing in cells are driven
- **Catalog:** NP-1377 to NP-1406 (30 features)
- **Hints:**
  - `TableObject` in `Photon.Nodus.Core/Models/Elements/Tables/`: row heights, column widths, cells (each an area text story from §8 or an inline image), merged ranges, per-edge border strokes, cell margins, background fills, separated borders with cell spacing.
  - Table tool and Table menu: Create New Table (rows, columns, size), select table, row, column, cell, and all contents (also by border clicks and the corner arrow), shape-tool cell selection, Ctrl+click for nonadjacent cells.
  - Insert rows above, below, or several (dialog), insert columns left, right, or several (dialog), delete row, column, or table; distribute rows and columns evenly; exact cell width and height; drag a row or column to move it.
  - Border selection (all, outer, inner, top, bottom, left, right, and combinations) with width, color, and line style; cell margins (locked equal by default); table and cell background.
  - Merge and Unmerge Cells (keeps upper-left formatting), Split into Rows and Split into Columns without resizing the table.
  - Cell text: paragraph text with §4 and §6 formatting across several selected cells at once, Tab to the next cell with `Nodus.Table.TabBehavior` (next cell left to right, right to left, or insert tab) and Ctrl+Tab inserting a tab, auto-resize cells while typing.
  - Place an image inside a cell (paste or right-drag) scaled to fit the cell.
  - Convert Text to Table and Table to Text by commas, tabs, paragraphs, or a user character; paste rows and columns into another table (replace, insert above or below, left or right).
  - The table transforms as one object (scale, rotate, mirror, lock) and Break Apart expands it to groups of shapes and text.
  - Import tables: XLSX through DocumentFormat.OpenXml, XLS through NPOI, CSV, DOCX and DOC tables through §13's readers, with the maintain or discard formatting options; Quattro Pro and WordPerfect are backlog B-037.
  - SVG: `<g nodus:table>` carrying the grid model, with expanded cell `<rect>`, border `<path>`, and text as the plain-SVG fallback, restored as a live table on reopen.
  - Every table edit is one command with one Serilog line; a 100 by 100 table edits at interactive speed.
  - Tests: `TableModelTests` (merge, split, insert and delete with merged ranges), `TextTableConversionTests`, `TableSvgRoundTripTests` over `tests/fixtures/nodus/svg-table/`, `XlsxTableImportTests` with a LibreOffice 25.x CSV golden.
- **Proof:** Format fidelity proof: `TableSvgRoundTripTests` reopens a live table with merged cells identical and the fallback renders in Inkscape 1.4; unit test `TableModelTests`; driven run capturing cell editing; cheaper substitute that fails: a table that becomes loose shapes on save.

#### §15. Graphs

- **Deliverable:** Live data graphs (column, stacked column, bar, stacked bar, line, area, scatter, pie, radar) with a data window, data import, type and axis options, legends, combined types, and column and marker designs.
- **Depends On:** §4
- **Phase:** 7
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/graphs/ and docs/captures/nodus/graph-data/. Job: turn a table of numbers into a styled, editable chart that updates when the data changes. Treatment: graph tools that open a spreadsheet-like data window, a Graph Type dialog, and part selection that keeps styling across data edits; cheaper substitute that fails: a one-time chart expanded to plain shapes. Chrome: consume the shared theme, icon catalog, history, settings store, `Photon.UI` grid and dialog controls, and the symbol store of D02 T06 §11 for designs.
- **Runs:** Requires: display-session -- the data window, graph tools, and part selection are driven
- **Catalog:** NP-1407 to NP-1431 (25 features)
- **Hints:**
  - `GraphObject` in `Photon.Nodus.Core/Models/Elements/Graphs/`: data table, row and column labels, graph type per series, options, and a `GraphBuilder` per type producing styled parts (columns, bars, lines, markers, wedges, axes, ticks, labels, legend).
  - Graph tools (J for column) in one flyout: column, stacked column, bar, stacked bar, line, area, scatter, pie, radar; drag or click for size.
  - Graph Data window: cell grid with import from tab-delimited text, transpose, switch x and y, cell style (decimals, column width), revert, apply; labels become legends and categories.
  - Graph Type dialog: type, value axis side (left, right, both with different scales), drop shadow, legend across top or in wedges, first row or column in front, column and cluster width.
  - Value axis options (override min, max, divisions, tick length and count, prefix and suffix) and category axis options (tick marks, draw between labels).
  - Line and scatter options (mark points, connect points, edge-to-edge lines, filled lines with width); pie options (legend, position ratio, even, or stacked, sort).
  - Combine graph types by selecting a series with the group selection tool and changing its type.
  - Graph designs: save selected artwork as a design; column designs vertically scaled, uniformly scaled, repeating (with unit value and fraction handling), sliding; marker designs; import designs from another document.
  - Part styling: the group selection tool selects bars, series, legends, and labels; fills, strokes, and text formatting on parts are stored per part role so they survive data changes.
  - SVG: `<g nodus:graph>` with the data table and options as JSON in `nodus:data`, expanded parts as the fallback, restored live on reopen.
  - Every data or option change is one command with one Serilog line; a 10,000-point scatter regenerates in under 200 ms.
  - Tests: `GraphBuilderTests` per type (part counts and geometry against committed goldens), `GraphDataImportTests`, `GraphSvgRoundTripTests` (styling kept per part role after a data edit and reopen).
- **Proof:** Format fidelity proof: `GraphSvgRoundTripTests` reopens a styled graph live and regenerates after a data change with styling kept; unit test `GraphBuilderTests`; driven run capturing the data window; cheaper substitute that fails: graphs expanded to shapes on creation.

#### Sizing concerns

- §3 carries 34 catalog features across three surfaces (font list and filters, Font Sampler, substitution and embedding); it likely exceeds 30 checklist items and would split cleanly into "font list and Font Sampler" and "missing fonts, substitution, and embedding".
- §8 carries 30 features spanning frames and columns, threading, and text wrap; at 30 items it sits on the limit, and threading plus wrap is the natural second half if it overflows.
- §14 carries 30 features plus spreadsheet and word-processor import; the import rows (XLS, XLSX, CSV, DOC, DOCX tables) could move to D02 T14 §14 to keep the table model in one commit.
- §5 carries 27 features plus glyph snapping into D02 T07 §11; if it overflows, snap to glyph and glyph guides are the separable part.

### todo/02-nodus/TODO-11-nodus-parity-effects.md -- `nodus-parity-effects`

- **Title:** "TODO-11 -- Nodus Parity: Interactive and Live Effects"
- **Phase(s):** 8
- **Goal:** Give Nodus every interactive and live vector effect Illustrator 30.8 and CorelDRAW 2026 users reach for (blend, contour, envelope and warp, distortion, shadows, glows and bevels, classic and modern 3D, lenses, PowerClip, symmetry, perspective, puppet warp, Live Paint and smart fill, repeats, and path effects), each one a live object under the live-object contract (`D02 T07 §1`) that sits in the Appearance stack (`D02 T09 §14`), renders through SkiaSharp at draw time (shadows and glows as Skia image filters, never through the Phase 9 pixel engine), expands to plain SVG geometry, survives a save and reopen as the same editable effect, and is undone by one step of the suite history.
- **Current-state facts to verify (with claim candidates):**
  - No effect model, registry, or effects folder exists in the core project. `<!-- claim: absent src/Nodus/Bezier.Core/Effects -->`
  - The offset operation every contour, offset path, and block shadow needs is a placeholder that returns its input. `<!-- claim: count "Placeholder - actual implementation uses SkiaSharp path effects" src/Nodus/Bezier.Core/Services/PathOperationsService.cs = 1 -->`
  - The boolean operation the live pathfinder effects and Live Paint need is also a placeholder. `<!-- claim: count "This will be implemented with SkiaSharp in the Desktop layer" src/Nodus/Bezier.Core/Services/PathOperationsService.cs = 1 -->`
  - The core project references no SkiaSharp package today, although `standards/nodus.md` allows it for geometry. `<!-- claim: count "SkiaSharp" src/Nodus/Bezier.Core/Bezier.Core.csproj = 0 -->`
  - The renderer uses no Skia image filters (no shadow, glow, or feather path exists). `<!-- claim: count "SKImageFilter" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->`
  - The renderer is one 840-line file that PowerClip, lenses, and effect caching extend. `<!-- claim: lines src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 840 -->`
  - A `clipPath` model element exists but the renderer never applies it, so PowerClip starts from model only. `<!-- claim: exists src/Nodus/Bezier.Core/Models/Elements/SvgClipPath.cs -->` `<!-- claim: count "ClipPath" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->`
  - The SVG writer emits no `nodus:` namespace data yet; `D02 T07 §1` adds it before this file runs. `<!-- claim: count "nodus:" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 0 -->`
  - There are 9 tool classes on `ToolBase` and none is an effect tool. `<!-- claim: count "class \w+Tool\b" src/Nodus/Bezier.Core/Tools/*.cs = 9 -->` `<!-- claim: absent src/Nodus/Bezier.Core/Tools/BlendTool.cs -->`
  - A per-element blend mode enum exists and is what shadow merge modes and glow modes reuse. `<!-- claim: count "public enum BlendMode" src/Nodus/Bezier.Core/Models/VectorElement.cs = 1 -->`
- **Inputs and XREFs:** `D02 T01 §1` (rename to Photon.Nodus), `D02 T07 §1` (live-object contract, Expand), `D02 T07 §2` (dirty-region rendering the effect cache plugs into), `D02 T07 §7` (focus mode), `D02 T07 §8` (property bar hosting effect tool options), `D02 T07 §11` (snapping the perspective grid and symmetry lines join), `D02 T08 §7` (offset path command sharing the offset kernel), `D02 T08 §8` (knife, eraser, crop that flatten perspective), `D02 T08 §10` (pathfinder kernels), `D02 T08 §11` (clipping masks under PowerClip), `D02 T09 §7` (gradients inside blends and extrusions), `D02 T09 §14` (Appearance stack), `D02 T09 §15` (graphic styles carrying effects), `D02 T09 §19` (blend modes), `D02 T10 §2` and `D02 T10 §8` (text objects under envelopes, 3D, and perspective), `D02 T12 §2` (raster effects, the lower half of the Effect menu), `D02 T13 §7` (overprint), `D02 T13 §14` (PDF writer expands effects), `D02 T14 §5` and `D02 T14 §7` (AI and CDR effect interchange), `D01 T02 §2` (settings store), `D01 T02 §4` (suite history), `standards/nodus.md`, Illustrator 30.8 and CorelDRAW 2026 user guides for behavior, Inkscape (LPEs, Interpolate extension, filter rendering) as the golden reference for expanded fallbacks.
- **Adjacency:** list=applicable (every effect family ships a preset list: blend, envelope, distortion, shadow, extrusion, 3D material, bevel profile, perspective grid presets); document=applicable @ D02 T13 §14 (effects print and export as their expanded geometry through the PDF writer); settings=applicable (per-tool defaults, preset folders, 3D render quality, PowerClip preferences, all through the settings store with a named consumer); reporting=not-applicable (effects have no domain summary beyond the Appearance panel and Document Info owned by D02 T07 §14); notifications=applicable (ray-traced render, Live Paint on large art, and 3D export report progress and completion on the status strip); permissions=applicable (a locked layer or locked object refuses Make, Clear, and Break Apart with a status message, and a read-only 3D export target is refused by name); audit=applicable (every create, edit, clear, expand, and break apart is one undoable command with one Serilog Information line); exchange=applicable (nodus: SVG parameters with expanded fallback, 3D export to OBJ, glTF, USDA, presets imported and exported as JSON); reverse=applicable (Clear, Release, Break Apart, and Expand are each undoable, and Release restores the source objects exactly)

#### §1. The live-effect framework: effect stack, parameters, copy, clone, clear, and expand

- **Deliverable:** A vector effect registry and stack evaluator in `Photon.Nodus.Core/Effects/` that every later section plugs into, with the Effect menu, Copy Effect From, Clone Effect From, Clear Effect, Break Apart, Expand, and a render cache.
- **Depends On:** D02 T09 §14
- **Phase:** 8
- **Surface:** UI: Fidelity: extends the main window menus, docs/captures/nodus/main-window/ | Job: a user can add, edit, copy, clone, clear, and expand a live effect from the Effect and Object menus | Treatment: effects evaluate lazily from stored parameters and cache their output per object | Cheaper substitute that fails: applying each effect destructively once and storing only the result | Chrome: consume the Appearance panel of D02 T09 §14, the shared icon catalog, and the suite history; do not invent a second effect list or a second undo stack.
- **Runs:** `Requires: display-session -- the Effect menu and Copy Effect From pick mode are driven and captured on the canvas`
- **Catalog:** NP-1432 to NP-1435 (4 features)
- **Hints:**
  - `IVectorEffect` in `src/Nodus/Photon.Nodus.Core/Effects/IVectorEffect.cs`: `Id`, `Kind` (vector or raster), `Parameters` record, `Evaluate(EffectInput) -> EffectOutput` (geometry plus paint), `Bounds`, and `Expand()`.
  - `EffectRegistry` in `Effects/EffectRegistry.cs` registered through the composition root; the Effect menu is built from it with vector effects on top and raster effects (D02 T12 §2) below a separator.
  - `EffectStackEvaluator` walks the Appearance stack items of D02 T09 §14 in order and feeds each effect the previous output; parameters are in document units so a raster effects resolution change re-evaluates without editing parameters.
  - `EffectCache` in `Photon.Nodus.Desktop/Rendering/EffectCache.cs` keyed by object id plus parameter hash plus source version, invalidated through the document change events and the dirty regions of D02 T07 §2; budget: a 10,000-object document with 500 live effects redraws a pan frame in 16 ms from cache.
  - Persistence: each effect writes `nodus:effect` elements with typed parameters under the D02 T07 §1 contract and its expanded geometry as the plain-SVG fallback; unknown effect kinds are preserved verbatim.
  - `CopyEffectFromCommand` and `CloneEffectFromCommand`: Object > Copy Effect and Object > Clone Effect submenus enter a pick mode (arrow cursor) that copies the parameters or links a clone to its master by id; a master edit propagates to clones in one command.
  - `ClearEffectCommand` removes the top interactive effect (generic, over the registry); `BreakEffectApartCommand` (Ctrl+K on an effect group) turns output into real objects and keeps the source; both undoable.
  - Expand reuses the generic Expand of D02 T07 §1; focus mode (D02 T07 §7) opens an effect group with its control objects editable and the generated parts dimmed.
  - Every mutation is an `IEditorCommand` in the suite history (D01 T02 §4) with one Serilog Information line naming effect kind and object id.
  - Tests: `tests/Photon.Nodus.Tests/Effects/EffectRegistryTests.cs`, `EffectStackEvaluatorTests.cs`, `EffectRoundTripTests.cs` (a registered test effect saves, reopens live, and expands).
- **Proof:** Round-trip proof on `tests/fixtures/nodus/svg/effects/stack-basic.svg`: save, reopen, compare parameters and the expanded fallback element by element; a substitute that only rasterizes the effect output fails because reopening loses the live effect.

#### §2. Blend: tool, steps, spacing, easing, and color acceleration

- **Deliverable:** Live blends between two or more key objects with the Blend tool, Make, Release, Expand, the Blend panel, steps and spacing, easing, rotation and loop, object and color acceleration, and color path.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/blend-panel/ | Job: a user can blend shapes and tune steps, spacing, easing, and color, seeing the blend update live | Treatment: shape interpolation with node correspondence and color interpolation in the document color space, with live preview while dragging sliders | Cheaper substitute that fails: a one-shot duplicate-and-tint that is not live and loses the blend on reopen | Chrome: consume `Photon.UI` sliders and number boxes, the shared color controls of D02 T09 §2, and the property bar of D02 T07 §8; do not invent a second panel dock.
- **Runs:** `Requires: display-session -- the Blend tool is driven on the canvas and the panel is captured`
- **Catalog:** NP-1436 to NP-1451 (16 features)
- **Hints:**
  - `BlendEffect` in `Photon.Nodus.Core/Effects/Blend/BlendEffect.cs`: key object ids, spine id, `Spacing` (smooth color, specified steps, specified distance), `Orientation` (page, path), `Rotation`, `Loop`, `Easing` (none, in, out, in-out, out-in, ramp 0 to 100), `ObjectAcceleration`, `ColorAcceleration`, `AccelerateSizing`, `ColorPath` (direct, clockwise, counterclockwise).
  - `ShapeInterpolator` in `Effects/Blend/ShapeInterpolator.cs`: normalizes both paths to matching node counts (subdivide by arc length), interpolates nodes and handles, and handles compound paths with unequal subpath counts.
  - `ColorInterpolator`: interpolates solid fills and gradient stops; clockwise and counterclockwise travel around HSB hue; bitmap, pattern, and texture fills do not progress (the Corel fill restriction), with a status hint.
  - `BlendTool` (W) in `Photon.Nodus.Core/Tools/BlendTool.cs`: click objects or anchor points in order, drag from one object to another; Object > Blend > Make (Alt+Ctrl+B), Release (Alt+Shift+Ctrl+B), Expand, Reverse Front to Back, Break Blend Apart (Ctrl+K).
  - `BlendPanel` in `Photon.Nodus.Desktop/Views/Panels/BlendPanel.xaml` (Window > Blend and Effects > Blend): Make, Expand, Release, Reverse, steps, spacing, orientation, easing curve preview, appearance shift, rotation, loop, color path.
  - Live editing: moving or recoloring a key object with direct selection re-evaluates the blend through the §1 cache; budget a 1,000-step blend re-evaluates under 50 ms.
  - Settings `Nodus.Blend.DefaultSteps` and `Nodus.Blend.DefaultSpacing` through the settings store (D01 T02 §2), consumed by `BlendTool`.
  - Persistence: `nodus:blend` parameters with the intermediate steps as the expanded fallback group; goldens compared to Inkscape's Interpolate extension for linear step placement (version recorded beside the fixture).
  - Tests: `tests/Photon.Nodus.Tests/Effects/Blend/ShapeInterpolatorTests.cs`, `BlendEasingTests.cs`, `BlendColorPathTests.cs`, `BlendRoundTripTests.cs`.
- **Proof:** Snapshot goldens of step geometry for steps, distance, easing, and color path on `tests/fixtures/nodus/svg/blend/`, plus a round-trip proof; a substitute that stores only expanded steps fails the reopen-as-live check.

#### §3. Blend on a path, node mapping, split, fuse, compound blends, and presets

- **Deliverable:** Blends that follow a spine or freehand path, with replace and reverse spine, full-path and rotate-along, node mapping, show and new start or end, split and fuse, compound blends, copy and clone, clear, and presets.
- **Depends On:** §2
- **Phase:** 8
- **Surface:** UI: Fidelity: extends docs/captures/nodus/blend-panel/ | Job: a user can put a blend on a path, map nodes, split, fuse, and chain blends | Treatment: arc-length parameterized placement along the spine with node correspondence the user can override | Cheaper substitute that fails: placing steps on the straight chord and ignoring the path | Chrome: consume the §2 panel, the shared preset store, and the node overlay of D02 T08 §6; do not invent a second node editor.
- **Runs:** `Requires: display-session -- path blends, node mapping, and split are driven on the canvas`
- **Catalog:** NP-1452 to NP-1468 (17 features)
- **Hints:**
  - `BlendSpine` in `Effects/Blend/BlendSpine.cs`: arc-length table over the spine path, `FullPath`, `RotateAlong`; Object > Blend > Replace Spine and Reverse Spine; property bar New Path (fit blend to path), Show Path, Detach From Path.
  - Freehand path blend: Alt+drag with the Blend tool records a freehand spine; the shape tool edits spine nodes and the blend follows.
  - `NodeMap` parameter: Map Nodes mode picks one node on the start and one on the end; stored as node indices in `nodus:blend`.
  - Start and end: Show Start, Show End select the key objects; New Start, New End pick a replacement object in one command.
  - `SplitBlendCommand` promotes an intermediate step to a key object; `FuseBlendCommand` rejoins split or compound blends; compound blend by dragging onto a start or end object of another blend (shared key object id).
  - Copy Effect Blend From and Clone Effect Blend From use the §1 commands; Clear Blend removes the blend keeping key objects.
  - `BlendPresetStore` in `Effects/Presets/EffectPresetStore.cs` (shared by later sections): JSON files under `%LOCALAPPDATA%\Rizonesoft\Nodus\Presets\Blend\`, apply, save, delete, import and export.
  - Tests: `BlendSpineTests.cs` (equal arc spacing within 0.01 px on a Bezier spine), `BlendSplitFuseTests.cs`, `CompoundBlendTests.cs`, `EffectPresetStoreTests.cs`.
- **Proof:** Snapshot goldens on `tests/fixtures/nodus/svg/blend/path-*.svg` plus round-trip of spine, node map, and compound links; a substitute that bakes the path blend into plain groups fails because Replace Spine after reopen does nothing.

#### §4. Contour

- **Deliverable:** A live contour effect with the Contour tool and panel: to center, inside, outside, steps and offset, acceleration, corner styles, fill and outline end colors, color path, break apart, copy and clone, and cuttable outlines.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/contour-panel/ | Job: a user can add concentric contours and tune their direction, spacing, corners, and colors | Treatment: true geometric offset curves with mitered, round, or bevel joins | Cheaper substitute that fails: scaled copies of the source, which are not equidistant | Chrome: consume the shared color controls, `Photon.UI` number boxes, and the §1 commands; do not invent a second offset routine beside D02 T08 §7.
- **Runs:** `Requires: display-session -- the Contour tool handle drag and panel are driven and captured`
- **Catalog:** NP-1469 to NP-1482 (14 features)
- **Hints:**
  - `OffsetKernel` in `Photon.Nodus.Core/Geometry/OffsetKernel.cs` replacing the `PathOperationsService.Offset` placeholder: stroke-outline based offset (SkiaSharp `SKPaint.GetFillPath` plus `SKPath.Op` cleanup) with joins mitered, round, bevel and a miter limit; shared with D02 T08 §7 and §19.
  - `ContourEffect` in `Effects/Contour/ContourEffect.cs`: `Direction` (to center, inside, outside), `Steps`, `Offset`, `ObjectAcceleration`, `ColorAcceleration`, `Corners`, `FillEndColor` (second color for gradient fills), `OutlineEndColor`, `ColorPath` (linear, clockwise, counterclockwise).
  - `ContourTool` in `Tools/ContourTool.cs`: drag from the object edge sets direction and offset; the end fill handle accepts a palette color drop.
  - `ContourPanel` in `Views/Panels/ContourPanel.xaml` (Effects > Contour, Ctrl+F9).
  - Break Contour Apart separates the source from a group of contour steps; Copy and Clone Effect Contour From via §1.
  - Cuttable outlines: contour steps are closed, non-overlapping curves with fills stacked, so an HPGL or PDF cutter export (D02 T14 §11) sees one cut line per step.
  - Budget: 100 contour steps on a 500-node path evaluate under 200 ms; slower runs off the UI thread with cancellation.
  - Tests: `OffsetKernelTests.cs` (distance from every output sample to the source within 0.05 px), `ContourEffectTests.cs`, `ContourRoundTripTests.cs`.
- **Proof:** Property tests for equidistance plus snapshot goldens on `tests/fixtures/nodus/svg/contour/`, fallback compared with Inkscape's Offset LPE output (version recorded); scaled copies fail the equidistance property.

#### §5. Envelope distort and warp

- **Deliverable:** Envelope distortion (make with warp, mesh, or top object; release; expand; edit contents), Corel envelope modes, presets, node editing and mapping modes, envelopes on paragraph text frames and bitmaps, and the Warp effect with its fifteen styles.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/envelope-panel/ and docs/captures/nodus/warp-dialog/ | Job: a user can bend artwork and text into a shape and keep editing both | Treatment: a bilinear Coons or mesh map applied to every node and handle with adaptive subdivision so curves stay smooth | Cheaper substitute that fails: moving only anchor points, which kinks curves | Chrome: consume the shared node overlay, preset store, and `Photon.UI` dialog chrome; do not invent a second mesh editor beside D02 T09 §9.
- **Runs:** `Requires: display-session -- envelope node drags, mesh editing, and the Warp dialog are driven and captured`
- **Catalog:** NP-1483 to NP-1504 (22 features)
- **Hints:**
  - `EnvelopeEffect` in `Effects/Envelope/EnvelopeEffect.cs`: `Source` (warp, mesh rows by columns, top object, curve), `Mode` (straight line, single arc, double arc, unconstrained), `Mapping` (horizontal, original, putty, vertical), `KeepLines`, `Fidelity`, `DistortAppearance`, `DistortLinearGradients`, `DistortPatternFills`, `PreserveShape` (clip or transparency).
  - `MeshMap` in `Effects/Envelope/MeshMap.cs`: Coons patch per cell, adaptive subdivision of segments by flatness until error is under the fidelity tolerance.
  - `WarpEffect` in `Effects/Warp/WarpEffect.cs`: styles arc, arc lower, arc upper, arch, bulge, shell lower, shell upper, flag, wave, fish, rise, fisheye, inflate, squeeze, twist; horizontal or vertical, bend, distortion H and V; shares `MeshMap`.
  - Commands: Object > Envelope Distort > Make with Warp (Alt+Shift+Ctrl+W), Make with Mesh (Alt+Ctrl+M), Make with Top Object (Alt+Ctrl+C), Release, Expand, Edit Contents or Edit Envelope, Envelope Options dialog; Corel Create Envelope From, Add New Envelope, Clear Envelope.
  - `EnvelopeTool` in `Tools/EnvelopeTool.cs`: double-click adds or deletes nodes, marquee and freehand multi-select, Ctrl, Shift, Ctrl+Shift constrained moves, node types cusp, smooth, symmetrical, segment to line or curve.
  - `EnvelopePanel` (Effects > Envelope, Ctrl+F7) with presets through the §3 `EffectPresetStore` (`Presets\Envelope\`).
  - Text: an envelope on paragraph text shapes the frame (text reflows through D02 T10 §8); on artistic text it maps glyph outlines while text stays editable; warped text is the Warp effect on a text object.
  - Bitmaps: an envelope on a placed image renders as a Skia `SKCanvas.DrawVertices` triangle mesh at draw time and expands to a resampled embedded image; the pixel engine is not used.
  - Tests: `MeshMapTests.cs`, `WarpStyleTests.cs` (one golden per style), `EnvelopeMappingModeTests.cs`, `EnvelopeTextTests.cs`.
- **Proof:** Snapshot goldens for the fifteen warp styles and four mapping modes on `tests/fixtures/nodus/svg/envelope/` plus round-trip; an anchor-only mapper fails the smoothness check (max deviation from the dense-sampled reference).

#### §6. The distort tool and Distort & Transform effects

- **Deliverable:** The Corel Distort tool (push and pull, zipper, twister, center handle, presets, stacked distortions) and the Illustrator Distort & Transform effects (free distort, pucker and bloat, roughen, transform with copies, tweak, twist, zig zag) as live effects.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/distort-effects/ | Job: a user can distort a shape interactively or by numbers and edit it later | Treatment: deterministic seeded randomness for roughen and tweak so reopen shows the same result | Cheaper substitute that fails: unseeded random, which changes the art on every redraw | Chrome: consume `Photon.UI` dialog chrome with live preview, the property bar, and the preset store; do not invent a second transform dialog beside D02 T08 §12.
- **Runs:** `Requires: display-session -- distort tool drags and effect dialogs with preview are driven and captured`
- **Catalog:** NP-1505 to NP-1519 (15 features)
- **Hints:**
  - Effects in `Effects/Distort/`: `FreeDistortEffect` (four corner map), `PuckerBloatEffect` (percent; Corel push and pull maps to it), `RoughenEffect` (size, detail, relative or absolute, smooth or corner, `Seed`), `TransformEffect` (scale, move, rotate, reflect, random, copies, reference point), `TweakEffect` (`Seed`), `TwistEffect` (angle; Corel twister adds direction and rotations), `ZigZagEffect` (size, ridges per segment, smooth or corner; Corel zipper adds frequency).
  - `DistortTool` in `Tools/DistortTool.cs`: mode buttons push and pull, zipper, twister; diamond center handle; Center Distortion command; the zipper frequency slider handle on canvas.
  - Stacked distortions: each drag appends a new entry to the effect stack; Clear Distortion removes the most recent one.
  - Dialogs under `Views/Dialogs/Distort/` with a Preview check box that renders through the §1 cache.
  - Presets through `EffectPresetStore` (`Presets\Distortion\`); Copy and Clone Effect Distortion From via §1; focus mode shows object and distortion together.
  - Fallback: expanded paths; goldens for roughen and zig zag compared with Inkscape's Roughen and Zig Zag LPEs for shape class, own snapshot goldens for exact output.
  - Tests: `DistortEffectTests.cs` (determinism by seed, node count growth, bounds), `StackedDistortionTests.cs`, `DistortRoundTripTests.cs`.
- **Proof:** Snapshot goldens per effect on `tests/fixtures/nodus/svg/distort/` plus determinism property tests (same seed gives byte-equal expansion); an unseeded roughen fails determinism.

#### §7. Drop, inner, perspective, and block shadows

- **Deliverable:** Drop shadows (flat and perspective), inner shadows, and vector block shadows as live effects with presets, color, merge mode, opacity, feathering, offset, angle, stretch, fade, copy and clone, break apart, and clear.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/shadow-tool/ | Job: a user can drag a shadow off an object and tune it on the property bar | Treatment: Skia image filters at render time (`SKImageFilter.CreateDropShadow`, blur, offset, color filter) for drop and inner shadows, vector geometry for block shadows | Cheaper substitute that fails: a baked bitmap copy or routing through the Photon.Core pixel engine (Phase 9) | Chrome: consume the shared color controls, blend modes of D02 T09 §19, the property bar, and the preset store; do not invent a second blur.
- **Runs:** `Requires: display-session -- shadow tool drags and the property bar are driven and captured`
- **Catalog:** NP-1530 to NP-1555 (26 features)
- **Hints:**
  - `ShadowEffect` in `Effects/Shadow/ShadowEffect.cs`: `Kind` (drop, perspective, inner), `Color`, `MergeMode` (the `BlendMode` enum, default Multiply), `Opacity`, `Feather`, `FeatherDirection` (average, inside, outside, Gaussian), `EdgeType` (linear, squared, inverse squared, flat), `Offset`, `Angle`, `Stretch`, `Fade`, `InnerWidth`.
  - `ShadowRenderer` in `Photon.Nodus.Desktop/Rendering/ShadowRenderer.cs`: builds an `SKImageFilter` chain from the parameters; perspective shadows skew the silhouette with a matrix then fade with a gradient shader mask; inner shadow uses the inverted alpha clipped to the shape.
  - `ShadowTool` in `Tools/ShadowTool.cs` (drop and inner modes): drag from center for flat, from an edge for perspective; one shadow per object, refused on blends, contours, bevels, and extrusions with a status message.
  - `BlockShadowEffect` in `Effects/Shadow/BlockShadowEffect.cs`: depth, direction, color, remove holes, from outline, expand, overprint, simplify; geometry is the union of swept copies through the §19 boolean kernel.
  - Commands: Break Drop Shadow Apart (to an embedded bitmap at the raster effects resolution), Break Inner Shadow Apart, Break Block Shadow Apart, Clear Shadow, Clear Block Shadow; Copy and Clone Effect Shadow From via §1; copy shadow properties on the property bar.
  - Presets through `EffectPresetStore` (`Presets\Shadow\`), add and delete.
  - Fallback: drop and inner shadows write an SVG `filter` (`feGaussianBlur`, `feOffset`, `feFlood`, `feComposite`) so any SVG viewer renders them; block shadows write plain paths with overprint carried for D02 T13 §7.
  - Budget: 1,000 shadowed objects redraw from cache at interactive frame rate; shadow bitmaps are cached per zoom bucket.
  - Tests: `ShadowFilterTests.cs` (rendered alpha profile against a reference Gaussian within 2 levels), `BlockShadowTests.cs`, `ShadowRoundTripTests.cs`.
- **Proof:** Rendered snapshot goldens on `tests/fixtures/nodus/svg/shadow/` with the SVG-filter fallback also rendered by Inkscape (version recorded) and compared within tolerance; a baked-bitmap substitute fails the reopen-as-live and zoom-sharpness checks.

#### §8. Glows, feather, scribble, round corners, and bevels

- **Deliverable:** Inner glow, outer glow, feather, round corners, and scribble effects, plus the Corel Bevel effect (soft edge and emboss) with lighting, colors, break apart, copy and clone, and clear.
- **Depends On:** §7
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/stylize-effects/ and docs/captures/nodus/bevel-panel/ | Job: a user can add glows, soft edges, sketchy fills, rounded corners, and bevels and edit them later | Treatment: glows and feather as Skia image filters reusing the §7 filter chain; bevel as shaded vector facets or a lit height field at render time | Cheaper substitute that fails: glow as a thick blurred stroke baked into the file | Chrome: consume the §7 `ShadowRenderer` filter builders, shared color controls, and `Photon.UI` dialog chrome; do not invent a second light-direction control beside §9.
- **Runs:** `Requires: display-session -- effect dialogs with preview and the Bevel panel are driven and captured`
- **Catalog:** NP-1556 to NP-1571 (16 features)
- **Hints:**
  - `GlowEffect` in `Effects/Stylize/GlowEffect.cs`: `Inner` or `Outer`, mode, color, opacity, blur, inner source center or edge; rendered by dilate plus blur filters.
  - `FeatherEffect`: feather radius as a blurred alpha mask; distinct from transparency feather in D02 T09 §20 and shares its mask builder.
  - `RoundCornersEffect`: radius applied to every corner node through the live-corner routine of D02 T08 §4.
  - `ScribbleEffect` in `Effects/Stylize/ScribbleEffect.cs`: angle, path overlap, variation, stroke width, curviness, spacing, `Seed`; presets (Default, Childlike, Dense, Loose, Moiré, Sharp, Sketch, Snarl, Swash, Tight, Zig-zag) as built-in preset files.
  - `BevelEffect` in `Effects/Bevel/BevelEffect.cs`: style soft edge or emboss, offset to center or distance, shadow color, light color, intensity, direction 0 to 360, altitude 0 to 90 (disabled for emboss); spot and process colors are kept as named inks in the facets for print.
  - `BevelPanel` in `Views/Panels/BevelPanel.xaml` (Effects > Bevel); Clear Effect removes it; Break Bevel Apart yields facet objects; Copy and Clone Effect Bevel From via §1.
  - Fallback: glows and feather write SVG filters; bevel writes facet paths (soft edge rendered as stepped facets at a fidelity setting `Nodus.Bevel.FacetSteps`).
  - Tests: `GlowEffectTests.cs`, `ScribbleDeterminismTests.cs`, `BevelFacetTests.cs` (facet shading follows Lambert with the given light vector), `StylizeRoundTripTests.cs`.
- **Proof:** Snapshot goldens on `tests/fixtures/nodus/svg/stylize/` and `bevel/` plus round-trip; a baked glow fails because changing the glow color after reopen has no parameter to edit.

#### §9. 3D extrude and revolve: geometry, lighting, bevels, and vanishing points

- **Deliverable:** Classic vector 3D (extrude and bevel, revolve, rotate with shading and map art) and the Corel Extrude tool and panel (presets, types, rotation, direction, depth, color modes, drape fills, extrusion bevels, three lights, vanishing point locking and sharing, break apart, copy and clone, clear).
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/extrude-panel/ and docs/captures/nodus/3d-classic-dialog/ | Job: a user can give flat art vector 3D depth and light it | Treatment: a real 3D mesh from the profile, projected and hidden-surface sorted into vector faces with flat or smooth shading steps | Cheaper substitute that fails: offset copies of the outline stacked to fake depth | Chrome: consume the shared color controls, `Photon.UI` dialog chrome, and the preset store; the light-direction sphere control lives in `Photon.UI` once and is reused by §8 and §10.
- **Runs:** `Requires: display-session -- the extrude rotation widget, vanishing point drags, and dialogs are driven and captured`
- **Catalog:** NP-1572 to NP-1593 (22 features)
- **Hints:**
  - `Photon.Nodus.Core/ThreeD/`: `Mesh3D`, `ProfileExtruder` (depth, cap on or off, bevel profile), `ProfileRevolver` (angle, offset, from left or right edge), `Camera` (rotation X, Y, Z, perspective), `FaceSorter` (BSP split for intersecting faces, painter order).
  - `Classic3DEffect` in `Effects/ThreeD/Classic3DEffect.cs`: kind extrude and bevel, revolve, rotate; surface wireframe, no shading, diffuse, plastic; lights with intensity, ambient, highlight, blend steps; map art from a symbol onto a chosen surface.
  - `ExtrudeEffect` in `Effects/ThreeD/ExtrudeEffect.cs` (Corel): type (small back, small front, big back, big front, back parallel, front parallel), depth, vanishing point with lock to object or page, shared vanishing point id, rotation, color (object fill, solid, shading), drape fills, bevel (use, depth, angle, show only), up to three numbered lights with intensity.
  - `ExtrudeTool` in `Tools/ExtrudeTool.cs`: drag to extrude, vanishing point handle, depth slider handle, rotation widget; extrusion inside a group; rounded corners on extruded rectangles follow the live rectangle of D02 T08 §4.
  - `ExtrudePanel` (Effects > Extrude) and `Classic3DDialog` (Effect > 3D and Materials > 3D Classic) with preview through the §1 cache.
  - Commands: Clear Extrusion, Break Extrude Apart (faces become paths), Copy VP From, Copy and Clone Effect Extrude From via §1; presets in `Presets\Extrude\`.
  - Fallback: expanded face paths with their shading; parameters in `nodus:extrude` and `nodus:classic3d`.
  - Budget: a 200-node profile extrudes and sorts under 100 ms; revolve with 64 segments under 300 ms with cancellation beyond one second.
  - Tests: `ProfileExtruderTests.cs`, `FaceSorterTests.cs` (no face drawn over a nearer face on the cube and torus fixtures), `ExtrudeVanishingPointTests.cs`, `ThreeDRoundTripTests.cs`.
- **Proof:** Snapshot goldens of expanded faces on `tests/fixtures/nodus/svg/extrude/` plus face-order property tests; stacked-outline fakes fail the rotation golden.

#### §10. 3D and Materials: inflate, plane, materials, mapped art, ray-traced rendering, and 3D export

- **Deliverable:** The 3D and Materials panel (plane, extrude, revolve, inflate, bevels with custom profiles, rotation and perspective, on-canvas widget), built-in parametric materials with no Adobe Substance or cloud library, mapped artwork, lighting and shadows, an own CPU path tracer for the ray-traced render, 3D on live text, and OBJ, glTF, and USDA export.
- **Depends On:** §9
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/3d-materials-panel/ | Job: a user can turn art into a lit, textured 3D object, render it photorealistically, and export it to a 3D app | Treatment: a real-time Skia-rasterized preview plus an own deterministic CPU path tracer for the final render, both from one `Mesh3D` | Cheaper substitute that fails: a shaded vector preview labeled as ray traced, or a dependency on Substance or an online material library | Chrome: consume the §9 mesh and light control, `Photon.UI` tabs and sliders, the status strip progress indicator, and the preset store; do not invent a second renderer beside `SkiaRenderer` for the preview.
- **Runs:** `Requires: display-session -- the rotation widget, panel tabs, and render progress are driven and captured`
- **Catalog:** NP-1594 to NP-1611 (18 features)
- **Hints:**
  - `Materials3DEffect` in `Effects/ThreeD/Materials3DEffect.cs`: object type plane, extrude (depth, twist, taper, caps), revolve (angle, offset, direction), inflate (depth, volume, one or both sides); bevel (shape, width, height, repeats, space, inside or outside) with custom bevel profiles saved as paths in `Presets\Bevel3D\`.
  - Rotation presets and X, Y, Z angles, perspective; `Rotation3DWidget` on canvas in `Photon.Nodus.Desktop/Canvas/Rotation3DWidget.cs`.
  - `MaterialLibrary` in `ThreeD/Materials/`: built-in parametric PBR materials (base color, roughness, metallic, normal from procedural noise, emissive) authored in-repo as JSON; custom materials saved by the user; Substance `.sbsar` is refused by name with a status message.
  - Graphics mapping: Add artwork to the Graphics tab as a symbol reference, placed on a chosen surface with scale, rotation, repeat; UV unwrap per face in `ThreeD/UvMapper.cs`.
  - Lighting: presets Standard, Diffuse, Top Left, Right; per light color, intensity, rotation, height, softness; multiple lights; ambient; cast shadows with position, distance, bounds.
  - Preview: triangle mesh rasterized with `SKCanvas.DrawVertices` and a shading pass, cached per parameter hash; 3D on live text keeps the text object and re-meshes on edit.
  - Ray tracing: `ThreeD/PathTracer/PathTracer.cs`, an own CPU path tracer (BVH, GGX microfacet, area lights, seeded sampling, `Parallel.For` tiles, cancellation and progress); render settings quality levels and a denoise pass; output is an embedded image with the live parameters kept; decision recorded in `docs/dev/decisions.md` (no external renderer, no GPU dependency).
  - Export 3D: `ThreeD/Export/ObjWriter.cs` (with MTL), `GltfWriter.cs` (glTF 2.0 binary), `UsdaWriter.cs`; File > Export > 3D object; fixtures under `tests/fixtures/nodus/obj/`, `gltf/`, `usda/` with goldens validated by the Khronos glTF-Validator and OpenUSD `usdchecker` (versions recorded).
  - Settings `Nodus.ThreeD.RenderQuality`, `Nodus.ThreeD.RenderThreads`, `Nodus.ThreeD.PreviewQuality` with consumers in `PathTracer` and the preview.
  - Budget: preview of a 20,000-triangle mesh under 33 ms; a medium-quality 1,000 by 1,000 render finishes in under 60 s on 8 cores with progress on the status strip and cancel.
  - Tests: `MeshInflateTests.cs`, `UvMapperTests.cs`, `PathTracerDeterminismTests.cs` (same seed gives identical pixels), `PathTracerConvergenceTests.cs` (white furnace test), `GltfWriterTests.cs`, `ObjWriterTests.cs`, `UsdaWriterTests.cs`.
- **Proof:** Format fidelity proof for OBJ, glTF, and USDA against committed fixtures with validator goldens, plus path tracer determinism and furnace tests; a vector-shading substitute fails the furnace test and a Substance dependency fails the license check.

#### §11. Lenses

- **Deliverable:** Live lenses (brighten, color add, color limit, custom color map, fish eye, heat map, invert, magnify, tinted grayscale, transparency, wireframe) with the Lens panel, viewpoint, remove face, frozen, feathered edges, restrictions, copy, and focus mode.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/lens-panel/ | Job: a user can place a shape that changes how the art beneath it looks and move it around live | Treatment: vector-exact lenses re-render the objects beneath through the lens shape as a clip (magnify, wireframe, color lenses as `SKColorFilter`), fish eye as an `SKRuntimeEffect` warp of the backdrop | Cheaper substitute that fails: a screenshot pasted into the lens shape | Chrome: consume the shared color controls, the §1 cache, and the `Photon.UI` panel chrome; do not invent a second color model beside D02 T09 §1.
- **Runs:** `Requires: display-session -- lens drag over art, frozen lens, and viewpoint editing are driven and captured`
- **Catalog:** NP-1612 to NP-1631 (20 features)
- **Hints:**
  - `LensEffect` in `Effects/Lens/LensEffect.cs`: `Type`, rate or amount, color, from and to colors with direct, forward, or reverse rainbow, `Viewpoint`, `RemoveFace`, `Frozen` (captures the beneath objects as a frozen group), `Feather`.
  - `LensRenderer` in `Photon.Nodus.Desktop/Rendering/LensRenderer.cs`: renders the document beneath the lens clipped to the lens path with a color filter (brighten, color add, color limit, invert, heat map, tinted grayscale, custom color map, transparency) or with a transform (magnify) or wireframe paint (wireframe), or an `SKRuntimeEffect` fish eye.
  - `LensPanel` in `Views/Panels/LensPanel.xaml` (Effects > Lens, Alt+F3), live apply, viewpoint edit handle on canvas.
  - Restrictions: lenses refuse contour, bevel, extrude, drop shadow groups, and blends with a status message naming the rule.
  - Lens shape stays editable with every shape tool; lens edges feather through the §8 feather mask; focus mode shows the lens and object together.
  - Copy Effect Lens From via §1; Frozen lens can be ungrouped into its captured objects.
  - Fallback: color lenses expand to recolored vector copies clipped to the lens shape; magnify expands to scaled clipped copies; fish eye expands to node-mapped distorted copies; parameters in `nodus:lens`.
  - Tests: `LensColorFilterTests.cs` (per-type color math against reference formulas), `LensExpandTests.cs`, `LensRoundTripTests.cs`, `LensRestrictionTests.cs`.
- **Proof:** Snapshot goldens per lens type on `tests/fixtures/nodus/svg/lens/` plus expand-versus-render comparison within 1 level; a screenshot substitute fails when the art beneath changes.

#### §12. PowerClip frames

- **Deliverable:** PowerClip frames: place inside frame, nested frames, empty frames, drag content in, remove frame, the floating toolbar, select, center, fit, fill, stretch, copy, edit and finish editing, lock, extract, and the PowerClip preferences.
- **Depends On:** D02 T08 §11
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/powerclip-toolbar/ | Job: a user can put art into a frame shape, position it, and pull it out again | Treatment: a container object whose frame clips its contents at render time and in SVG as a `clipPath`, with contents kept as real editable objects | Cheaper substitute that fails: destructive intersection of contents with the frame | Chrome: consume the clipping-mask renderer of D02 T08 §11, the floating toolbar pattern in `Photon.UI`, and the settings store; do not invent a second clip implementation.
- **Runs:** `Requires: display-session -- drag into frame, the floating toolbar, and edit mode are driven and captured`
- **Catalog:** NP-1632 to NP-1648 (17 features)
- **Hints:**
  - `PowerClipFrame` in `Photon.Nodus.Core/Models/Elements/PowerClipFrame.cs` (a group subtype holding frame path and contents, `LockContents`, `IsEmpty`), written as `g` plus `clipPath` with `nodus:powerclip` parameters.
  - Renderer: `SkiaRenderer` applies `SKCanvas.ClipPath` with anti-aliasing for the frame, including nested frames; empty frames draw an X by the `Nodus.PowerClip.ShowEmptyLines` setting (always, including print and export, or on screen only).
  - Commands in `Commands/PowerClip/`: Place Inside Frame, Create Empty Frame, Remove Frame, Extract Contents, Lock Contents, Center, Fit Proportionally, Fill Proportionally, Stretch to Fill, Copy PowerClip From, Edit PowerClip and Finish Editing (double-click).
  - Drag content onto a frame: `Nodus.PowerClip.DragBehavior` (ignore frame, add content, replace existing), W key adds to a full frame; `Nodus.PowerClip.AutoCenter` (when completely outside, always, never).
  - `PowerClipToolbar` floating control in `Photon.Nodus.Desktop/Canvas/PowerClipToolbar.xaml`: Edit, Select Contents, Extract, Lock, fit and center commands.
  - Edit mode shows the frame in wireframe and contents at full opacity; select contents selects them without entering edit mode.
  - Tests: `PowerClipCommandTests.cs`, `PowerClipFitTests.cs` (fit, fill, stretch bounds math), `PowerClipRoundTripTests.cs` (nested frames reopen as frames and plain viewers show the clip), `PowerClipSettingsTests.cs`.
- **Proof:** Round-trip proof on `tests/fixtures/nodus/svg/powerclip/` with Inkscape rendering the clip fallback (version recorded); a destructive-intersection substitute fails Extract Contents.

#### §13. Symmetry drawing mode

- **Deliverable:** Live symmetry groups: create, edit and finish, mirror line count up to 12, reposition and rotate lines, center X and Y, full preview, show lines, drag objects in, single-entity transforms, snap to symmetry lines, fuse open curves, remove, and break link or apart.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/symmetry-mode/ | Job: a user can draw once and see every mirrored copy update in real time | Treatment: copies are generated live from the primary objects by reflection transforms | Cheaper substitute that fails: duplicating once after drawing | Chrome: consume the snapping of D02 T07 §11, the floating toolbar pattern shared with §12, and the property bar; do not invent a second edit-mode chrome beside focus mode.
- **Runs:** `Requires: display-session -- drawing inside symmetry edit mode is driven and captured`
- **Catalog:** NP-1649 to NP-1661 (13 features)
- **Hints:**
  - `SymmetryGroup` in `Models/Elements/SymmetryGroup.cs`: primary objects, `LineCount` 1 to 12, `Center`, `Angle`, `ShowFullPreview`, `ShowLines`; copies generated on evaluation, never stored except as the fallback.
  - Commands: Object > Symmetry > Create New Symmetry, Edit Symmetry (double-click or Ctrl+click), Finish Editing Symmetry, Remove Symmetry, Break Symmetry Link (to a regular group with copies as real objects), Break Symmetry Apart (Ctrl+K, same result).
  - Edit mode overlay: symmetry lines draggable and rotatable, center handle, outline-only copies unless full preview.
  - Snap to Symmetry Lines in View > Snap To, default on, as a snap provider registered with D02 T07 §11.
  - Fuse Open Curves joins an open curve whose ends touch a mirror line with its reflected copy into one closed path.
  - Drag objects onto a symmetry group adds them as primaries (W key when not empty); transforms, fills, outlines, and transparency on the group apply to all copies.
  - Fallback: expanded copies in a `g` with `nodus:symmetry` parameters.
  - Tests: `SymmetryGroupTests.cs` (12-line copies exact), `FuseOpenCurvesTests.cs`, `SymmetryRoundTripTests.cs`.
- **Proof:** Round-trip proof and snapshot goldens on `tests/fixtures/nodus/svg/symmetry/`; a duplicate-once substitute fails the edit-primary-updates-copies test.

#### §14. The perspective grid and drawing planes

- **Deliverable:** A perspective grid with one, two, and three point types, define grid, presets, show and hide, rulers, snap and lock, on-canvas widgets, active plane switching, Corel Draw in Perspective with field, camera lines, locking, restricted areas, horizon and line display, and snapping to perspective lines.
- **Depends On:** D02 T07 §11
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/perspective-grid/ | Job: a user can set up a perspective and draw shapes that land on its planes | Treatment: a projective grid model with homographies per plane that shape tools draw through | Cheaper substitute that fails: a static guide image | Chrome: consume the snapping providers of D02 T07 §11, the guides color settings of D02 T07 §10, and the preset store; do not invent a second snapping engine.
- **Runs:** `Requires: display-session -- grid widgets, plane switching keys, and drawing on planes are driven and captured`
- **Catalog:** NP-1662 to NP-1678 (17 features)
- **Hints:**
  - `PerspectiveGrid` in `Photon.Nodus.Core/Perspective/PerspectiveGrid.cs`: type (one, two, three point with worm or bird eye), vanishing points, horizon, ground level, viewing angle and distance, gridline spacing, extent, station point, `Locked`; `PlaneHomography` per plane (left, right, horizontal, top, side, orthographic).
  - `PerspectiveGridTool` (Shift+P) in `Tools/PerspectiveGridTool.cs`: widgets for vanishing points, horizon, ground level, extent, cell size, viewport resize, camera lines, hide grid widget.
  - Plane switching widget with keys 1 to 4 (left, horizontal, right, none); shape tools of D02 T08 §4 draw through the active plane homography.
  - View > Perspective Grid: One, Two, Three Point presets, Show or Hide (Ctrl+Shift+I), Show Rulers, Snap to Grid, Lock Grid, Lock Station Point, Define Grid dialog, Save Grid as Preset; Edit > Perspective Grid Presets manager (`Presets\PerspectiveGrid\`).
  - Corel Object > Perspective > Draw in Perspective creates a perspective group with a field (drag or Enter to fill the page) and a floating toolbar for type, plane, lock field, show horizon with opacity and color, show lines with density, opacity, color.
  - Snap To Perspective Lines (default on) as a snap provider; drawing over vanishing points is refused, and draw in perspective is unavailable in focus mode.
  - Grid state persists per document in `nodus:perspective-grid`; display settings in the settings store.
  - Tests: `PlaneHomographyTests.cs` (grid lines converge on vanishing points within 0.01 px), `PerspectiveGridPresetTests.cs`, `PerspectiveSnapTests.cs`.
- **Proof:** Snapshot goldens of grid rendering and of rectangles drawn on each plane on `tests/fixtures/nodus/svg/perspective-grid/`, plus preset round-trip; a static guide image fails the draw-on-plane test.

#### §15. Perspective objects and the Add Perspective effect

- **Deliverable:** Objects attached to perspective planes (perspective selection tool, attach, release, move plane to match, editable text and symbols, perpendicular move and copy, Corel perspective groups) and the Add Perspective envelope-style effect with one and two point node drags, copy, and clear.
- **Depends On:** §14, §5
- **Phase:** 8
- **Surface:** UI: Fidelity: extends docs/captures/nodus/perspective-grid/ | Job: a user can move, scale, and edit art that stays in perspective, or push any object into perspective by dragging corners | Treatment: objects keep their flat source geometry plus a plane binding, projected on render | Cheaper substitute that fails: baking the projected geometry so text stops being editable | Chrome: consume the §14 grid and homographies and the §5 `MeshMap`; do not invent a second projection routine.
- **Runs:** `Requires: display-session -- perspective selection moves, perpendicular moves, and Add Perspective node drags are driven and captured`
- **Catalog:** NP-1679 to NP-1698 (20 features)
- **Hints:**
  - `PerspectiveBinding` in `Perspective/PerspectiveBinding.cs`: plane id, plane offset, flat source geometry; evaluated through `PlaneHomography`.
  - `PerspectiveSelectionTool` (Shift+V) in `Tools/PerspectiveSelectionTool.cs`: move, scale, Alt-drag copy, 5 key perpendicular move, arrow keys move along the plane.
  - Commands Object > Perspective: Attach to Active Plane, Release with Perspective, Move Plane to Match Object, Edit Text (text and symbols stay live); Corel Move to Plane (orthogonal, top, left, right, side), Edit Perspective Group, Break Perspective Group Apart.
  - Perspective group limits: move and proportional scale only; rotate, skew, and non-proportional scale are refused with a status message; the shape tool reshapes on a temporary orthographic plane and re-projects.
  - `AddPerspectiveEffect` in `Effects/Perspective/AddPerspectiveEffect.cs` (Object > Add Perspective): four-corner projective map; Ctrl constrains to one-point, free drag two-point, Ctrl+Shift symmetric node drag, vanishing point handles; applies to contours, blends, and extrusions but not paragraph text or bitmaps where refused.
  - Knife, crop, and eraser (D02 T08 §8) flatten the effect first with a status note; Copy Effect Perspective From via §1; Clear Perspective.
  - Fallback: projected geometry as plain paths so older readers and other viewers get regular groups; parameters in `nodus:perspective`.
  - Tests: `PerspectiveBindingTests.cs`, `AddPerspectiveEffectTests.cs`, `PerspectiveTextEditTests.cs`, `PerspectiveRoundTripTests.cs`.
- **Proof:** Round-trip proof on `tests/fixtures/nodus/svg/perspective/` (text in perspective reopens editable) plus snapshot goldens; a baking substitute fails the editable-text check.

#### §16. Puppet warp

- **Deliverable:** The Puppet Warp tool with pins (add, select all, rotate), show and expand mesh, mesh density, working on vector paths and placed images as a live effect.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/puppet-warp/ | Job: a user can pin art and drag pins to bend it naturally | Treatment: as-rigid-as-possible deformation of a triangulated mesh, with path nodes and handles mapped through barycentric coordinates | Cheaper substitute that fails: moving only the nearest anchors | Chrome: consume the property bar and on-canvas handle overlay; do not invent a second triangulator beside the §10 mesh code.
- **Runs:** `Requires: display-session -- pin placement and drags are driven and captured`
- **Catalog:** NP-1520 to NP-1521 (2 features)
- **Hints:**
  - `PuppetWarpEffect` in `Effects/PuppetWarp/PuppetWarpEffect.cs`: pins (rest and current positions, rotation), `MeshDensity`, `ExpandMesh`, source ids.
  - `ArapSolver` in `Effects/PuppetWarp/ArapSolver.cs`: constrained Delaunay triangulation of the outline, precomputed factorization, iterative local-global solve; budget under 16 ms per drag frame for 2,000 triangles.
  - `PuppetWarpTool` in `Tools/PuppetWarpTool.cs`: click adds a pin, Alt-drag near a pin rotates, Shift adds to selection, Delete removes; property bar Show Mesh, Expand Mesh, Select All Pins.
  - Placed images warp by `SKCanvas.DrawVertices` on the deformed mesh at render time; expand writes a resampled image.
  - Commit on mouse-up as one command capturing pin state.
  - Tests: `ArapSolverTests.cs` (rigid motion preserved with two pins, determinism), `PuppetWarpRoundTripTests.cs`.
- **Proof:** Snapshot goldens on `tests/fixtures/nodus/svg/puppet-warp/` plus solver property tests; an anchor-nudge substitute fails the rigidity test.

#### §17. Live Paint and smart fill

- **Deliverable:** Live Paint groups (make, merge, release, expand) with the Live Paint Bucket and Live Paint Selection tools, gap detection and show gaps, and the Corel Smart Fill tool with fill, outline, and outside-area behavior.
- **Depends On:** D02 T08 §10
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/live-paint/ | Job: a user can color the regions formed by overlapping paths as if they were separate shapes, and keep editing the paths | Treatment: a planar map (arrangement of all path segments into faces and edges) rebuilt on edit, with fills attached to faces by a stable point sample | Cheaper substitute that fails: running Divide once, which loses the live paths | Chrome: consume the D02 T08 §10 boolean and intersection kernels and the swatch cursor preview of D02 T09 §3; do not invent a second curve-intersection routine.
- **Runs:** `Requires: display-session -- bucket clicks, double and triple clicks, and gap preview are driven and captured`
- **Catalog:** NP-1699 to NP-1709 (11 features)
- **Hints:**
  - `PlanarMap` in `Photon.Nodus.Core/Geometry/PlanarMap.cs`: segment intersection (Bezier clipping), half-edge structure, faces with holes, gap closing by a distance tolerance.
  - `LivePaintGroup` in `Models/Elements/LivePaintGroup.cs`: source paths, face fills and edge strokes keyed by sample points so edits keep colors where faces persist.
  - Commands Object > Live Paint: Make (Alt+Ctrl+X), Merge, Release (paths with 0.5 pt black stroke), Expand (faces and edges to paths), Gap Options dialog (small, medium, large, custom, preview color, Close Gaps with Paths); View > Show Live Paint Gaps.
  - `LivePaintBucketTool` (K): paint fills, paint strokes, cursor swatch preview, highlight color and width in options; double-click fills across unstroked edges, triple-click fills all same-colored faces.
  - `LivePaintSelectionTool` (Shift+L) selects faces and edges.
  - `SmartFillTool` in `Tools/SmartFillTool.cs`: creates a new filled object from the enclosed area under the click using the planar map of the visible objects; fill options (default, specify, none), outline options (default, specify width and color, none); clicking outside any area creates an object from the outline of all objects on the page.
  - Budget: planar map of 2,000 segments under 500 ms, off the UI thread beyond one second with cancellation and status strip progress.
  - Fallback: expanded face and edge paths with `nodus:livepaint` parameters.
  - Tests: `PlanarMapTests.cs` (face count on fixtures, Euler characteristic), `LivePaintColorStabilityTests.cs`, `GapDetectionTests.cs`, `SmartFillTests.cs`.
- **Proof:** Round-trip proof and snapshot goldens on `tests/fixtures/nodus/svg/livepaint/`; a one-shot Divide substitute fails the edit-a-path-keeps-colors test.

#### §18. Repeats and objects on a path

- **Deliverable:** Live radial, grid, and mirror repeats with options, release and expand; Objects on Path (tool, attach, pivot, rotate, spacing, shuffle, move all, detach, expand); and the Corel Fit Objects to Path panel with all its distribution and rotation options.
- **Depends On:** §1
- **Phase:** 8
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/repeats/ and docs/captures/nodus/fit-objects-to-path/ | Job: a user can repeat art radially, in a grid, or mirrored, and lay objects along a path, editing the source once | Treatment: repeat instances are generated live from one source through `SvgUse`-style references | Cheaper substitute that fails: static copies made once | Chrome: consume the §3 arc-length table, `Photon.UI` panel chrome, and the on-canvas handle overlay; do not invent a second path-measuring routine.
- **Runs:** `Requires: display-session -- repeat handles, objects-on-path widgets, and the Fit Objects to Path panel are driven and captured`
- **Catalog:** NP-1710 to NP-1726 (17 features)
- **Hints:**
  - `RepeatEffect` in `Effects/Repeat/RepeatEffect.cs`: `Radial` (instances, radius, reverse overlap), `Grid` (horizontal and vertical spacing, grid type grid or brick by row or column, flip rows, flip columns), `Mirror` (axis angle); on-canvas handles for count, radius, spacing, and axis.
  - Object > Repeat > Radial, Grid, Mirror, Options, Release, Expand; editing the source in isolation updates every instance.
  - `ObjectsOnPathEffect` in `Effects/Repeat/ObjectsOnPathEffect.cs`: attach path id, objects, pivot, rotate, spacing, shuffle seed, move all; `ObjectsOnPathTool` with widgets; Object > Objects on Path > Attach, Detach, Expand; tool options dialog for default pivot and rotation.
  - `FitObjectsToPathPanel` in `Views/Panels/FitObjectsToPathPanel.xaml` (Object > Fit Objects to Path): keep originals, duplicates, group all, treat as contiguous, order (selection, reverse, by area, width, height), distribution (uniform gaps or even reference points), reference point, ignore initial rotation, rotation style (uniform, progressive, jitter, progressive jitter), start angle, spin angle, revolutions, range, clockwise; applies as one command producing real objects.
  - Persistence: repeats and objects on path as live `nodus:repeat` and `nodus:objects-on-path` with `use` element fallbacks, so plain viewers draw every instance.
  - Budget: a radial repeat of 360 instances of a 1,000-node source renders from cache at interactive frame rate.
  - Tests: `RepeatEffectTests.cs`, `ObjectsOnPathTests.cs` (even arc-length spacing), `FitObjectsToPathTests.cs` (each rotation style), `RepeatRoundTripTests.cs`.
- **Proof:** Round-trip proof on `tests/fixtures/nodus/svg/repeat/` with Inkscape rendering the `use` fallback (version recorded) plus snapshot goldens; static copies fail the edit-source-updates-instances test.

#### §19. Path effects: convert to shape, offset, outline, and pathfinder effects

- **Deliverable:** The live path effects: Convert to Shape (rectangle, rounded rectangle, ellipse), Offset Path, Outline Object, Outline Stroke, and the Pathfinder effects (add, intersect, exclude, subtract, minus back, divide, trim, merge, crop, outline, hard mix, soft mix).
- **Depends On:** §1, D02 T08 §10
- **Phase:** 8
- **Surface:** UI: Fidelity: extends the Effect menu captured in docs/captures/nodus/main-window/ plus new dialogs captured to docs/captures/nodus/path-effects/ | Job: a user can apply shape and path operations that stay live when the source changes | Treatment: effects that call the same kernels as the destructive commands of D02 T08 §7 and §10 on every evaluation | Cheaper substitute that fails: running the destructive command once and discarding the sources | Chrome: consume the D02 T08 §10 boolean kernels, the §4 `OffsetKernel`, and `Photon.UI` dialog chrome; do not invent a second boolean engine.
- **Runs:** `Requires: display-session -- effect dialogs with preview are driven and captured`
- **Catalog:** NP-1522 to NP-1529 (8 features)
- **Hints:**
  - `ConvertToShapeEffect` in `Effects/Path/ConvertToShapeEffect.cs`: shape rectangle, rounded rectangle, ellipse; size absolute or relative (extra width and height), corner radius.
  - `OffsetPathEffect`: offset, joins, miter limit, through `OffsetKernel`; `OutlineStrokeEffect` through the stroke-to-path kernel replacing the `PathOperationsService.StrokeToPath` stub; `OutlineObjectEffect` treats text as its outlines for alignment and following effects while the text stays live.
  - `PathfinderEffect` in `Effects/Path/PathfinderEffect.cs` on a group: add, intersect, exclude, subtract, minus back, divide, trim, merge, crop, outline; hard mix (component-wise max in overlaps) and soft mix (mixing rate) on fills.
  - Pathfinder options (precision, remove redundant points, divide and outline remove unpainted) shared with D02 T08 §10 settings.
  - Fallback: result geometry as plain paths with the source group kept in `nodus:pathfinder` so reopen restores the live group.
  - Tests: `ConvertToShapeEffectTests.cs`, `OffsetPathEffectTests.cs`, `PathfinderEffectTests.cs` (each operation matches the destructive command output node for node), `MixEffectTests.cs`, `PathEffectRoundTripTests.cs`.
- **Proof:** Equivalence tests against the D02 T08 §10 commands plus round-trip on `tests/fixtures/nodus/svg/path-effects/`; a run-once substitute fails the edit-source-updates-result test.

#### Sizing concerns

- §10 (3D and Materials) carries a new panel, parametric materials, UV mapping, a real-time preview, an own CPU path tracer, and three 3D writers; it likely exceeds 30 items and would split cleanly at authoring into 3D and Materials modeling and preview versus the path tracer and 3D export.
- §5 (Envelope and Warp) carries both Illustrator envelope modes, the fifteen warp styles, the Corel envelope tool with modes, node constraints, and mapping modes, plus text and bitmap envelopes; it is near 30 items and would split into the envelope engine with Illustrator commands versus the Corel envelope tool and panel if it overflows.
- §7 (shadows) holds 26 catalog features across drop, inner, perspective, and block shadows; block shadows are a separate vector engine and are the natural split if the item count passes 30.

### todo/02-nodus/TODO-12-nodus-parity-bitmaps.md -- `nodus-parity-bitmaps`

- **Title:** "TODO-12 -- Nodus Parity: Bitmaps, Tracing, and Raster Effects"
- **Phase(s):** 9
- **Goal:** Nodus treats placed images as first-class bitmap objects: crop, resample, straighten, correct perspective, change color mode, mask colors, and rasterize vector art; it applies every Photon.Core pixel-engine effect and adjustment non-destructively through an FX stack that persists in the `nodus:` namespace with a rasterized SVG fallback; it traces bitmaps into editable vectors with a Nodus-local potrace port (outline) and skeletonization (centerline) behind both an Image Trace panel and a trace dialog; it builds vector and image mosaics and photo mockups; and it manages linked files through a Links panel; `D02 T06 §14` (File, Place for images) is relocated into Phase 9 ahead of §1 so placing images exists before bitmap editing starts.
- **Current-state facts to verify (with claim candidates):**
  - The bitmap element exists as `SvgImage` with position, size, `Href`, `EmbeddedData`, and `MimeType`, and nothing else. `<!-- claim: exists src/Nodus/Bezier.Core/Models/Elements/SvgImage.cs -->`
  - The renderer has no branch for it, so a parsed `<image>` is invisible on the canvas today. `<!-- claim: count "SvgImage" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 0 -->`
  - `ImportService` can build an embedded image element from raster bytes but is referenced by no Desktop file; the triage defers it to `D02 T06 §14`. `<!-- claim: count "ImportRasterImage" src/Nodus/Bezier.Core/Services/ImportService.cs = 5 -->`
  - The SVG reader ignores filters entirely. `<!-- claim: count "filter" src/Nodus/Bezier.Core/Services/SvgParser.cs = 0 -->`
  - There is no tracing code in Nodus. `<!-- claim: absent src/Nodus/Bezier.Core/Tracing -->`
- **Inputs and XREFs:** `standards/nodus.md` (SVG native, one renderer, commands); potrace 1.16 by Peter Selinger (GPL-2.0-or-later, compatible with the suite's GPL-3.0) as the ported algorithm and golden oracle; Inkscape 1.4 Trace Bitmap (potrace-based) as the second oracle; W3C Filter Effects Module Level 1 and SVG 1.1 section 15 for SVG filters; -> XREF: D02 T06 §14 (File, Place for images, relocated into Phase 9 ahead of §1); -> XREF: D01 T03 §1, D01 T03 §2, D01 T03 §3, D01 T03 §4, D01 T03 §5 (the pixel engine this file consumes; Imago's filter pipeline, D03 T05 §1, Phase 5 of the old plan, later renumbered, is that engine's planned second consumer); -> XREF: D02 T07 §1 (live-object contract for the FX stack, live traces, and mosaics); -> XREF: D02 T11 §1 (live-effect framework the FX stack registers in); -> XREF: D02 T11 §5 (envelope mesh the mockups warp through); -> XREF: D02 T11 §11 (lens framework for the bitmap effect lens); -> XREF: D02 T11 §17 (Live Paint for editing trace results); -> XREF: D01 T04 §3 (Lab, CMYK, and duotone conversions the mode commands wait for); -> XREF: D02 T15 §9 and D02 T15 §10 (AI upsampling and AI-assisted tracing that extend §5); -> XREF: D01 T02 §3 (single-instance forwarding used by Edit Bitmap in Imago).
- **Adjacency:** list=applicable (the Links panel with missing, modified, and embedded filters in §7; the trace preset list in §5; the PhotoCocktail library in §6); document=applicable @ D02 T13 §1 (rasterized effects print through the print pipeline; always-overprint-black is honored there); settings=applicable @ D01 T02 §2; reporting=applicable (bitmap info on the status bar in §1, trace statistics in §4 and §5, link file info in §7, the Adjustment Lab histogram in §3); notifications=applicable (progress and cancel in the status strip for effects, traces, and mosaics; missing and modified link prompts in §7); permissions=applicable (a linked file that is missing, locked, or read-only is reported in the Links panel and refused by name on relink or unembed); audit=applicable (every edit is an undoable command logged with one Serilog Information line); exchange=applicable (SVG `<image>` and `<filter>` round trip, color-mask files, trace presets, palette files, unembedded images); reverse=applicable (undo every command; release a trace; flatten is undoable; break link is undoable)

#### §1. Bitmap objects: crop, resample, rasterize, convert to bitmap, color mask, and straighten

- **Deliverable:** Bitmap objects with decoded pixels, mode, and resolution; crop (rectangular and node-edited), resample, straighten, correct perspective, convert to bitmap, color mode commands, color-mask panel, monochrome coloring, and make pixel perfect, each one undoable command
- **Depends On:** D01 T03 §2, D02 T06 §14
- **Phase:** 9
- **Surface:** Fidelity: new build, no baseline; captured to `docs/captures/nodus/bitmaps/` (Bitmaps menu, Resample, Straighten, Convert to Bitmap, Black and White, Paletted dialogs, Bitmap Mask panel), main window changes to `docs/captures/nodus/main-window/`. Job: a designer can place a photo and fix, reduce, and mask it without leaving Nodus. Consumer: the document and the SVG writer. Treatment: modal dialogs with live preview, the mask as a dockable panel, crop and node editing on canvas; cheaper substitute that fails: a single Image Properties dialog with numeric fields and no preview. Chrome: consume the shared theme, icon catalog, history, settings store, and `Photon.UI` numeric and color controls; do not add a second color picker or a Nodus-local undo.
- **Runs:** `Requires: display-session -- the dialogs, on-canvas crop handles, and node editing need an interactive desktop`
- **Catalog:** NP-1753 to NP-1783 (31 features)
- **Hints:**
  - Relocation note: `D02 T06 §14` (File, Place for PNG, JPEG, WebP, embedded or linked, plus `SvgImage` rendering) moves into Phase 9 ahead of this section; this section starts from placed, visible images.
  - `src/Nodus/Photon.Nodus.Core/Models/Elements/SvgImage.cs`: add a lazily decoded `PixelBuffer` cache (WIC decode through `Photon.Nodus.Desktop` service injected behind an interface), `ColorMode`, `PixelWidth`, `PixelHeight`, and effective ppi; status bar shows mode, pixel size, and ppi for a selected bitmap (CD-1968).
  - `CropImageCommand` (Object > Crop Image; on-canvas handles; resolution field, AI-0205, AI-0206) destructively crops pixels; `CropBitmapToShapeCommand` plus Shape tool node editing on the bitmap boundary (CD-1969, CD-1970, CD-2074) keeps pixels and stores the boundary as an SVG `clipPath`.
  - Bitmaps > Resample dialog (`ResampleDialog.xaml`) over `D01 T03 §2` `ResampleRequest` with mode, aspect, file-size, and dpi options; Straighten Image dialog (angle to plus or minus 15 degrees, grid size and color, crop options, remember settings in `Nodus.Bitmaps.Straighten.*` settings) and Correct Perspective over `Rotator` and `PerspectiveCorrector`.
  - Object > Rasterize and Bitmaps > Convert to Bitmap as one `RasterizeCommand` and one dialog (resolution, color mode, anti-aliasing, transparent background, dithered, always overprint black stored as `nodus:overprint-black="true"` for `D02 T13` to honor); the same option set appears in the raster export dialog from `D02 T06 §14` (CD-1966).
  - Bitmaps > Mode submenu: Black and White (1-bit) dialog over `D01 T03 §3` `BilevelConverter`, Grayscale, Paletted dialog (palette type, colors, dithering and intensity, range sensitivity, processed palette editor, presets saved under `%LOCALAPPDATA%\Rizonesoft\Nodus\presets\paletted\`), RGB; Lab, CMYK, and Duotone items present but disabled with a tooltip naming `D01 T04 §3`.
  - Mode changes re-encode the embedded image (1-bit, gray, and indexed PNG) and record `nodus:color-mode`; 1-bit bitmaps take palette clicks as background and right-clicks as foreground color (CD-1988), stored as `nodus:mono-colors` with the recolored PNG as fallback.
  - Bitmap Mask panel (`BitmapMaskPanel.xaml`): up to 10 color slots, hide or show, tolerance per slot, eyedropper, edit color via the shared color picker, save and open (Nodus JSON; reads Corel `.ini` masks) with a committed `.ini` fixture; persisted as `nodus:color-mask` parameters with the masked PNG as fallback.
  - Object > Make Pixel Perfect (`MakePixelPerfectCommand`) snaps path nodes and bitmap bounds to the 1-pixel grid at 72 ppi document units.
  - Every command records one history entry and logs one Serilog Information line; the reopen test restores crop, mode, mask, and mono colors as live values, not as the fallback.
  - Budget: a 24-megapixel placed photo resamples, crops, and changes mode with progress and cancel, never blocking the UI thread.
- **Proof:** round-trip and driven proof: `tests/Photon.Nodus.Tests/Bitmaps/BitmapCommandTests.cs` (each command, undo, and SVG reopen against fixtures in `tests/fixtures/nodus/svg/bitmaps/`) plus a driven session that places, straightens, masks, and converts a photo to paletted with screenshots in `docs/captures/nodus/bitmaps/`; cheaper substitute that fails: mode changes applied only to the on-screen preview, which the reopen test rejects.

#### §2. The effect stack on objects: FX panel, effect gallery, preview, flatten, and effect lenses

- **Deliverable:** A non-destructive bitmap-effect stack on any object, edited in an FX panel and an Effect Gallery, rendered with a cached scaled preview, persisted as live parameters with a rasterized fallback, plus Document Raster Effects Settings, the live Rasterize effect, flatten, and the bitmap effect lens
- **Depends On:** D01 T03 §1, D02 T11 §1
- **Phase:** 9
- **Surface:** Fidelity: new build, no baseline; captured to `docs/captures/nodus/effects-panel/` (FX panel, Effect Gallery, Document Raster Effects Settings) and `docs/captures/nodus/main-window/` (Effects menu). Job: a designer can stack, tune, reorder, hide, and flatten bitmap effects on vector or bitmap objects and keep editing them after reopening. Consumer: the renderer, the SVG writer, and export. Treatment: an FX panel list with eye toggles, drag reorder, per-effect parameter editors, and a split before and after preview; cheaper substitute that fails: a one-shot destructive filter per menu item. Chrome: consume the `D02 T11 §1` effect registry and stack evaluator, the shared theme and icon catalog, history, and settings store; do not build a second effect list beside the appearance stack.
- **Runs:** `Requires: display-session -- the FX panel, gallery, and live preview need an interactive desktop`
- **Catalog:** NP-1995 to NP-2008 (14 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Effects/BitmapEffectNode.cs` registers every `D01 T03` `IPixelEffect` in the `D02 T11 §1` registry as a raster effect; the Effects menu is generated from `EffectRegistry` categories so every engine effect has a menu item without hand wiring.
  - Vector objects rasterize at the Document Raster Effects Settings (color model, resolution 72, 150, 300, or custom; white or transparent background; anti-alias; clipping mask; added margin; preserve spot colors) stored per document as `nodus:raster-effects`, defaults in `Nodus.Effects.RasterResolution` etc. (AI-0644); the auto-inflate document option from `D01 T03 §1` is read here.
  - Rasterize as a live effect (AI-0694) is one registered effect using the same settings.
  - FX panel (`Views/Panels/EffectsPanel.xaml`, a Properties tab): add from a category menu, eye toggle per effect and for all effects of an object (also in the Layers panel), drag reorder, delete, reset to defaults, parameter editor generated from `EffectParameterSchema`, each change one undoable command.
  - Preview: full and split before and after (CD-2105); rendering through an `EffectRenderCache` keyed by object content hash, stack hash, and zoom bucket, preview at `PreviewScale` while a slider moves and full resolution on release; cancel a superseded render.
  - Effect Gallery dialog: thumbnail grid of artistic, brush-stroke, distort, sketch, stylize, and texture effects with a stacked-list builder, plus the Tune blur, Tune sharpen, and Tune noise thumbnail pickers.
  - Persistence: `<nodus:effects>` child with one `<nodus:effect id version seed ...params>` per entry; the fallback is the rasterized result as an `<image>` so other SVG readers see the look; reopen restores the live stack (round-trip fixture under `tests/fixtures/nodus/svg/effects/`).
  - Flatten Effects: replaces the object with an `SvgImage` holding the rendered pixels, undoable.
  - Bitmap effect lens: a lens type in the `D02 T11 §11` lens framework that applies a stack to everything beneath the lens shape (CD-1920, CD-2098).
  - Budget: a 5-effect stack on a 12-megapixel bitmap previews at screen scale under 200 ms per parameter change and renders in full with progress and cancel.
- **Proof:** round-trip and driven proof: `tests/Photon.Nodus.Tests/Effects/EffectStackTests.cs` (add, reorder, hide, flatten, undo; SVG reopen restores the stack; an external reader sees the fallback image) plus a driven FX panel session captured to `docs/captures/nodus/effects-panel/`; cheaper substitute that fails: storing only the rasterized result, which the reopen-as-live test rejects.

#### §3. Adjustments in Nodus: the Image Adjustment Lab and adjustment presets

- **Deliverable:** Effects > Adjust commands for every `D01 T03 §4` and `D01 T03 §5` adjustment with live preview, the Image Adjustment Lab dialog, and multi-filter adjustment presets
- **Depends On:** D01 T03 §5, §2
- **Phase:** 9
- **Surface:** Fidelity: new build, no baseline; captured to `docs/captures/nodus/adjustments/` (Image Adjustment Lab, Levels, Tone Curve, Hue/Saturation/Lightness dialogs). Job: a designer can correct a photo's tone and color inside Nodus with before and after comparison. Consumer: the FX stack of `§2`. Treatment: the Lab as one dialog with auto adjust, white and black point droppers, temperature, tint, saturation, brightness, contrast, highlights, shadows, midtones, live histogram, snapshots, and full, before and after, or split preview; cheaper substitute that fails: sliders with no histogram and no preview. Chrome: consume the shared theme, `Photon.UI` sliders and numeric boxes, history, and settings store; the histogram control stays Nodus-local until Imago's `D03 T05 §2` needs it, then moves to `Photon.UI`.
- **Runs:** `Requires: display-session -- the Lab and adjustment dialogs need an interactive desktop`
- **Catalog:** NP-2009 to NP-2023 (15 features)
- **Hints:**
  - Effects > Adjust submenu with one command per adjustment (auto adjust, levels, equalize, sample and target, tone curve, light, gamma, white balance, color balance, hue saturation lightness, black and white, vibrance, selective color, replace colors, replace colors legacy, desaturate, channel mixer, invert, threshold); each dialog is generated from the schema with a hand-built exception for Levels and Tone Curve.
  - Every adjustment applies as an entry in the `§2` FX stack (non-destructive), and a Live preview toggle (CD-2290) previews on canvas or in the dialog.
  - Tone Curve dialog: curve, straight, freehand, gamma styles; channel selector with all-channels display; smooth, mirror, reset channel and reset all; eyedropper that places a node; import of Corel `.pst` presets through `D01 T03 §4`.
  - `ImageAdjustmentLabDialog.xaml` with `ImageAdjustmentLabViewModel`: controls map to `D01 T03 §4` and `§5` adjustments composed into one ordered stack entry; histogram view bound to `Histogram` recomputed on the preview buffer.
  - Lab snapshots (numbered, clickable to compare), dialog-local undo, redo, and reset to original (the dialog's own stack, committed as one history entry on OK), and Remember settings stored as `Nodus.AdjustmentLab.Remembered` in the settings store.
  - Adjustment presets (CD-2257): Black and White, Color, Tone, and user presets as `AdjustmentPreset` JSON under `%LOCALAPPDATA%\Rizonesoft\Nodus\presets\adjustments\`, applied from the FX panel, with save, rename, delete, import, export.
  - Every committed adjustment is one undoable command with one Serilog Information line.
- **Proof:** unit and driven proof: `tests/Photon.Nodus.Tests/Effects/AdjustmentLabTests.cs` (Lab composition equals the equivalent engine stack bit-exactly; presets round-trip; remember settings persists across restart) plus a driven Lab session with split preview captured to `docs/captures/nodus/adjustments/`; cheaper substitute that fails: a Lab that applies destructively on OK, which the FX-stack reopen test rejects.

#### §4. The tracing engine: outline tracing, color quantization, and stacking

- **Deliverable:** `Photon.Nodus.Core/Tracing/`: a potrace port for outline tracing, multi-color tracing over `D01 T03 §3` quantization with abutting or stacked output, fidelity and cleanup options, stroke output for thin regions, and trace statistics
- **Depends On:** D01 T03 §3
- **Phase:** 9
- **Surface:** no surface of its own (the Image Trace panel and trace dialog are §5)
- **Runs:** none
- **Catalog:** NP-2028 to NP-2041 (14 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Tracing/Potrace/` ports potrace 1.16 (path decomposition, optimal polygon, vertex adjustment, corner detection with `alphamax`, curve optimization with `opttolerance`, speckle suppression `turdsize`); each ported file carries the GPL-2.0-or-later notice crediting Peter Selinger; add the decision row (algorithm port, license compatibility with GPL-3.0) to `docs/dev/decisions.md`.
  - `TraceOptions` record: mode (color, grayscale, black and white with threshold), palette (automatic, limited, full tone, document swatches), colors count, paths, corners, noise (Illustrator names), detail, smoothing, corner smoothness (Corel names, mapped onto the same potrace parameters with a documented table), method (abutting or overlapping), create fills, create strokes with max stroke width, snap curves to lines, ignore white, remove background (auto or sampled color, whole image option), merge adjacent, group by color.
  - `ColorTracer`: quantize through `D01 T03 §3` `ColorReducer` (seeded), split per color, trace each mask with `Potrace`; overlapping mode traces each color unioned with all lighter-ranked colors and stacks bottom up; abutting mode subtracts upper shapes so paths share edges without gaps.
  - Stroke output: regions thinner than max stroke width become centerline strokes through `Tracing/Skeleton/ZhangSuenSkeletonizer.cs`, which `§5` centerline tracing reuses.
  - Post-processing: snap near-straight Beziers to lines within tolerance, drop white and background regions, merge adjacent same-color paths with `SKPath.Op` union, group by color.
  - `TraceResult`: paths, anchors, colors, elapsed time, and the estimate function `§5` shows before tracing.
  - Cancellation per color layer and progress; budget: a 2-megapixel logo at 16 colors under 2 seconds, a 24-megapixel photo at 64 colors cancellable with progress.
  - Tests: goldens from the potrace 1.16 CLI for black-and-white fixtures (rasterized XOR area under 0.5 percent and matching path count) and Inkscape 1.4 Trace Bitmap multiscan colors for color fixtures, committed under `tests/fixtures/nodus/trace/` with versions recorded.
- **Proof:** golden proof in `tests/Photon.Nodus.Tests/Tracing/TracerTests.cs` against potrace 1.16 and Inkscape 1.4 fixtures plus abutting-gap tests (no uncovered pixel between neighboring colors); cheaper substitute that fails: marching-squares polygons with no curve fitting, which the anchor-count and XOR goldens reject.

#### §5. Centerline tracing, the Image Trace panel, and PowerTRACE

- **Deliverable:** Centerline tracing, shape and gradient detection, the Image Trace panel with live trace objects and presets, the trace dialog with preview modes and color editing, Quick, Outline, and Centerline Trace commands with their presets, and trace defaults
- **Depends On:** §4
- **Phase:** 9
- **Surface:** Fidelity: new build, no baseline; captured to `docs/captures/nodus/trace/` (Image Trace panel, trace dialog in each preview mode, Bitmaps > Trace submenu). Job: a designer can turn a logo, sketch, or photo into editable vectors with presets, preview, and color control, and change the settings later on a live trace. Consumer: the document (paths or a live trace object). Treatment: a live trace object with Make, Make and Expand, Release, Expand; a dialog with before and after, large preview, wireframe overlay, zoom, pan, fit, and a colors page; cheaper substitute that fails: a one-shot trace with no preview and no live object. Chrome: consume the shared theme and icon catalog, history, settings store, the swatch and palette file readers from `D02 T09 §4`, and Live Paint from `D02 T11 §17`; do not write a second palette reader.
- **Runs:** `Requires: display-session -- the panel, dialog, and preview modes need an interactive desktop`
- **Catalog:** NP-2042 to NP-2075 (34 features)
- **Hints:**
  - Centerline trace in `Tracing/CenterlineTracer.cs`: skeletonize with the `§4` `ZhangSuenSkeletonizer`, prune spurs, walk skeleton graphs into open and closed polylines, fit Beziers; presets Technical Illustration and Line Drawing.
  - Shape detection (circles, ellipses, rectangles become live shapes from `D02 T08 §4`) and gradient detection (linear gradients with a smoothness slider) as `TraceOptions` flags.
  - `LiveTraceElement` in `Photon.Nodus.Core/Models/Elements/`: source image reference plus `TraceOptions`, persisted as `nodus:trace` parameters with the traced paths as the plain-SVG fallback (`D02 T07 §1`); Make, Make and Expand, Release, Expand commands, each undoable; Expand then Live Paint (`D02 T11 §17`) for editing.
  - Image Trace panel (`Views/Panels/ImageTracePanel.xaml`): one-click preset buttons, preset list, view modes (result, with outlines, outlines, outlines with source, source), mode, palette, colors, advanced options, statistics; trace presets as JSON under `%LOCALAPPDATA%\Rizonesoft\Nodus\presets\trace\` with save, rename, delete, import, export.
  - Built-in presets: the Illustrator enhanced set and classic list, and the Corel outline presets (line art, logo, detailed logo, clipart, low and high quality image) and centerline presets, each a committed JSON file with a snapshot test.
  - Trace dialog (`Views/Dialogs/TraceDialog.xaml`): before and after, large preview, wireframe overlay with opacity slider, zoom, pan, fit; trace type and image type switchers; object, node, and color counts with time estimate; delete original; dialog undo, redo, reset; Settings, Colors, and Adjustments pages.
  - Colors page: sort by similarity or frequency, select by swatch or eyedropper, edit color, merge (average or first selected, from the defaults), delete (replaced by the next color), open and save palette via the `D02 T09 §4` palette readers and writers.
  - Adjustments page: classical pre-trace brightness, contrast, blur, and JPEG artifact removal from `D01 T03 §4` and `D01 T03 §6`; AI upsampling appears disabled with a tooltip naming `D02 T15 §9`.
  - Bitmaps > Quick Trace (settings default from `Nodus.Trace.QuickMethod`), Outline Trace submenu, Centerline Trace submenu; trace defaults page in preferences (quick method, merge behavior).
  - Lettering trace (AI-0423): a Lettering preset that traces text images into outlines grouped per connected glyph.
- **Proof:** round-trip and driven proof: `tests/Photon.Nodus.Tests/Tracing/LiveTraceTests.cs` (live trace reopens with its options; Release restores the image; centerline fixtures against Inkscape 1.4 centerline output) plus a driven session tracing a logo with each preview mode captured to `docs/captures/nodus/trace/`; cheaper substitute that fails: presets that only change the color count, which the per-preset snapshot tests reject.

#### §6. Photo artwork: Pointillizer, PhotoCocktail, Object Mosaic, and mockups

- **Deliverable:** Pointillizer vector mosaics, PhotoCocktail image mosaics, Object Mosaic, and photo mockups with local templates
- **Depends On:** §1, D02 T11 §5
- **Phase:** 9
- **Surface:** Fidelity: new build, no baseline; captured to `docs/captures/nodus/mosaics/` (Pointillizer panel, PhotoCocktail panel, Object Mosaic dialog, Mockup panel). Job: a designer can turn a photo into a vector mosaic, a mosaic of other photos, or place art onto a product photo. Consumer: the document. Treatment: dockable panels with live counts and Apply, Esc cancels a running build; cheaper substitute that fails: fixed-size square tiles only. Chrome: consume the shared theme, icon catalog, history, settings store, and the `D02 T11 §5` envelope mesh; do not write a second mesh warp.
- **Runs:** `Requires: display-session -- the panels and on-canvas mockup editing need an interactive desktop`
- **Catalog:** NP-1784 to NP-1806 (23 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Mosaic/Pointillizer.cs`: density (tiles per square inch), scale, screen angle, limit colors (through `D01 T03 §3`), tracking method (uniform with white matte, size by opacity, size by luminosity), merge adjacent up to N, weld overlapping into clusters, tile shape (circle, square, preset shapes, or a selected closed path), keep original; works on bitmaps and on rasterized vector selections.
  - Pointillizer panel with a live tile count and Esc to cancel; output is a group of real paths with one fill each, one undoable command.
  - `Mosaic/PhotoCocktail.cs`: index a folder of images (average Lab color and a small thumbnail cached as JSON beside the settings), grid columns with auto rows, blending percentage, duplicates with minimum spacing, composition (single bitmap, bitmap stack, bitmap array), edges (remove partial or stretch), priority (document dpi, custom dpi, tile size, output size), keep original.
  - PhotoCocktail panel with the library browser; refuses by name a folder it cannot read; single-bitmap output renders through the engine with progress and cancel.
  - Object > Create Object Mosaic dialog: tile count or size, spacing, color or gray, resize by percent, delete raster; output rectangles grouped.
  - Mockups: a `MockupElement` holding art, target photo, and a user-fitted envelope mesh (`D02 T11 §5`) with shading from the photo's luminance; Edit Content, Edit Mockup, Release; save as local templates under `%LOCALAPPDATA%\Rizonesoft\Nodus\mockups\` and preview on them; no cloud template library and no automatic surface detection (recorded in the section).
  - Persistence: Pointillizer and Object Mosaic output is plain SVG; mockups persist as `nodus:mockup` parameters with the warped, shaded art as fallback.
  - Budget: a 20,000-tile Pointillizer build under 5 seconds with progress.
- **Proof:** unit and driven proof: `tests/Photon.Nodus.Tests/Mosaic/MosaicTests.cs` (tile counts for density and scale, merge and weld reduce counts, PhotoCocktail picks the nearest-color tile, mockup reopen restores live) plus a driven session captured to `docs/captures/nodus/mosaics/`; cheaper substitute that fails: a Pointillizer that ignores tracking method, which the size-distribution test rejects.

#### §7. The Links panel and linked sources

- **Deliverable:** A Links panel and link manager for linked and embedded files with relink, update, embed, unembed, info, placement options, filters, the update policy, edit original, and a Sources view for linked documents and tables
- **Depends On:** §1
- **Phase:** 9
- **Surface:** Fidelity: new build, no baseline; captured to `docs/captures/nodus/links/` (Links panel, Link Info, Placement Options, Sources view). Job: a designer can see every linked file, fix missing ones, update modified ones, and embed or unembed them. Consumer: the document and its SVG `href` values. Treatment: a list with status badges (missing, modified, embedded), filters and sort, and prompts per the update policy; cheaper substitute that fails: a static list with no status and no relink. Chrome: consume the shared theme, icon catalog, history, settings store, and the file dialogs used by File, Place; do not add a second file watcher service.
- **Runs:** `Requires: display-session -- the panel, relink dialogs, and Edit Original launches need an interactive desktop`
- **Catalog:** NP-1807 to NP-1823 (17 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Links/LinkManager.cs`: enumerates linked `SvgImage` elements and other linked sources, resolves relative and absolute paths against the document folder, watches files with one `FileSystemWatcher` per folder, and raises missing and modified states.
  - Links panel (`Views/Panels/LinksPanel.xaml`): status badges, filters (missing, modified, embedded) and sort, Relink (with Relink all instances by default and Auto relink other missing files from the same folder), Update Link, Go To Link, Link File Info (name, format, color space, location, ppi, dimensions, scale, rotation, modified date).
  - Embed (reads bytes into a data URI) and Unembed (writes PNG or TIFF through WIC beside the document and relinks), plus Break link for linked Nodus sources; each undoable; refusal by name for read-only folders.
  - Placement Options for relink (preserve transforms, bounds, fit, fill, center, clip to bounding box).
  - Update links policy `Nodus.Links.UpdateMode` (Automatic, Manual, AskWhenModified) consumed by `LinkManager` on activation; low-resolution proxy for linked EPS as `Nodus.Links.EpsLowResProxy`, consumed when `D02 T14 §9` places EPS.
  - Edit Original (Edit menu and panel) launches the file with the system default app or a chosen app per `Nodus.Links.EditOriginalApp`; Edit Bitmap in Imago launches Imago with the path through single-instance forwarding (`D01 T02 §3`) and updates on save.
  - File, Place and Import gain a Link option (CD-1967, CD-2473, CD-2485); Sources view lists linked Nodus SVG documents and CSV tables (`D02 T10 §14`); CDR and XLS sources appear disabled naming `D02 T14 §6` and `D02 T14 §14`; linked symbol libraries show as a filter (`D02 T09 §21`).
  - Persistence: SVG `href` stays relative when possible; `nodus:link` stores the original absolute path, size, and modified time for relink heuristics.
  - Budget: a document with 500 linked images opens and reports statuses without blocking the UI thread.
- **Proof:** round-trip and driven proof: `tests/Photon.Nodus.Tests/Links/LinkManagerTests.cs` (missing and modified detection with a temp folder, relink all instances, embed and unembed round trip, read-only refusal) plus a driven session with a missing link fixed by auto relink captured to `docs/captures/nodus/links/`; cheaper substitute that fails: absolute `href` values only, which the moved-folder test rejects.

#### §8. SVG filter effects

- **Deliverable:** SVG 1.1 filter primitives read, rendered, written, and applied: Apply SVG Filter, built-in presets, import filter definitions, and a filter code editor, with a round-trip fixture
- **Depends On:** §2
- **Phase:** 9
- **Surface:** Fidelity: new build, no baseline; captured to `docs/captures/nodus/svg-filters/` (Apply SVG Filter dialog and filter code editor). Job: a web designer can apply and edit standard SVG filters that survive in browsers. Consumer: the renderer, the SVG writer, and browsers reading the output. Treatment: filters stay live `<filter>` elements in the SVG, not rasterized; cheaper substitute that fails: rasterizing the filter into an image on save. Chrome: consume the `§2` FX stack entry type, the shared theme, and the raw SVG editor pattern of `RawSvgDialog`; do not write a second XML editor.
- **Runs:** `Requires: display-session -- the dialog and code editor need an interactive desktop`
- **Catalog:** NP-2024 to NP-2026 (3 features)
- **Hints:**
  - `SvgParser` reads `<filter>` and every SVG 1.1 primitive (feGaussianBlur, feOffset, feBlend, feColorMatrix, feComponentTransfer, feComposite, feConvolveMatrix, feDiffuseLighting, feSpecularLighting, feDisplacementMap, feFlood, feImage, feMerge, feMorphology, feTile, feTurbulence) into `Photon.Nodus.Core/Models/Filters/`; unknown primitives preserved verbatim.
  - `SvgFilterRenderer` evaluates the primitive graph with SkiaSharp image filters where exact (`SKImageFilter.CreateBlur`, `CreateColorFilter`, `CreateDisplacementMapEffect`) and through `D01 T03` kernels otherwise, honoring `filterUnits`, `primitiveUnits`, and the filter region.
  - `SvgExporter` writes the filter back unchanged in `<defs>`; the object references it by `filter="url(#id)"`; an applied SVG filter is an FX stack entry of type `svg-filter` in `§2`.
  - Effect > SVG Filters > Apply SVG Filter dialog listing built-in presets (Nodus's own set: blur, drop shadow, bevel, dilate, erode, turbulence, woodgrain, and similar; Adobe preset names are not copied) and document filters.
  - Import SVG Filter reads `<filter>` definitions from any SVG file; New and Edit filter code open the raw XML editor with validation.
  - Round-trip fixtures under `tests/fixtures/nodus/svg/filters/` with goldens rendered by Inkscape 1.4 and Chromium (versions recorded), compared within a stated tolerance.
- **Proof:** format fidelity proof: `tests/Photon.Nodus.Tests/Svg/SvgFilterTests.cs` renders each fixture against the Inkscape 1.4 golden and round-trips it element by element; cheaper substitute that fails: dropping `<filter>` on save, which the round-trip test rejects.

#### Sizing concerns

- `D01 T03 §6`, `§8`, and `§10` carry 27 to 28 effects each; they fit 30 items only because the hints group effects by shared primitive (kernel family, stroke field, relief and cell partition). If a grouped item proves too large at build time, the split is by family into a new section at authoring, not mid-flight.
- `D02 T12 §5` (34 catalog features) is the largest UI section: centerline tracing, live trace object, panel, dialog, color page, presets, and commands. It fits by grouping presets as data files and the color operations as one item; if it does not, the natural split is centerline plus live trace object versus the trace dialog.
- `D02 T12 §1` (31 features) spans the object model, four dialogs, and a panel; the color-mode dialogs are the part to split out if it overflows.

### todo/02-nodus/TODO-13-nodus-parity-print.md -- `nodus-parity-print`

- **Title:** "TODO-13 -- Nodus Parity: Color Management, Print, Prepress, and PDF"
- **Phase(s):** 10
- **Goal:** A Nodus user can take a drawing to a print shop or a desktop printer without leaving Nodus: the document carries its ICC profiles and policies, the screen soft-proofs the press, File, Print drives any Windows printer with tiling, marks, bleed, separations, overprint, trapping, flattening, imposition, and variable data, and Publish to PDF writes exact vector PDF with spot colors, layers, PDF/X and PDF/A presets, and security through Nodus's own content-stream writer on PDFsharp (MIT); this promotes backlog B-011 (source `legacy-nodus-9`) and consumes the Photon.Core color engine of `D01 T04 §1` to `D01 T04 §3`.
- **Current-state facts to verify (with claim candidates):**
  - The document color mode today is a bare enum with RGB, CMYK, and Grayscale and no profile behind it. `<!-- claim: count "^    CMYK,$" src/Nodus/Bezier.Core/Services/FileOperationsService.cs = 1 -->`
  - Print-category document presets exist (A4, A3, Letter, Legal) but nothing prints. `<!-- claim: count "Category = PresetCategory.Print" src/Nodus/Bezier.Core/Services/FileOperationsService.cs = 5 -->`
  - No Nodus source touches WPF or .NET printing. `<!-- claim: count "PrintDialog|System\.Printing|XpsDocumentWriter|PrintVisual" src/Nodus/**/*.cs = 0 -->`
  - The export dialog advertises a "Print" preset described as a high-quality PDF with no writer behind it. `<!-- claim: count "High-quality PDF for printing" src/Nodus/Bezier.Core/Services/ExportDialogService.cs = 1 -->`
  - File, Export, PDF is a status-text stub today; `D02 T04 §4` replaces it with an `SKDocument` exporter that §14 of this file supersedes. `<!-- claim: count "StatusText = \"Export as PDF\.\.\.\";" src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 1 -->`
  - No PDF library is referenced by central package management. `<!-- claim: count "PDFsharp|PdfPig|PdfSharp" Directory.Packages.props = 0 -->`
  - The importer already names the missing PDF library as the blocker. `<!-- claim: count "PDF vector extraction requires a dedicated library like PdfSharp or iText" src/Nodus/Bezier.Core/Services/ImportService.cs = 1 -->`
  - Photon.Core, which will host the color engine this file consumes, does not exist yet. `<!-- claim: absent src/Photon.Core -->`
  - There is no decisions log yet for the printing-path and PDFsharp rows. `<!-- claim: absent docs/dev/decisions.md -->`
  - No capture home exists yet for the print and PDF surfaces. `<!-- claim: absent docs/captures -->`
- **Inputs and XREFs:** `D01 T04 §1` (engine, ICC transforms, default profiles), `D01 T04 §2` (intents, black point compensation, proofing transform, gamut check API), `D01 T04 §3` (bitmap CMYK and duotone modes); `D01 T02 §2` settings store; `D01 T02 §4` suite history; `D01 T03 §3` dithering for print as bitmap; `D02 T04 §4` (the `SKDocument` PDF export §14 replaces, its `PdfExporterTests` kept as regression); `D02 T07 §1` live-object contract (Crop Marks and Trap effects, merge fields); `D02 T07 §3` and `D02 T07 §4` (page and artboard model, page sizes, facing pages); `D02 T09 §1` (spot and registration colors), `D02 T09 §7` to `D02 T09 §10` (gradients, mesh, patterns as PDF shadings and patterns), `D02 T09 §19` and `D02 T09 §20` (blend modes, opacity masks as transparency groups); `D02 T10 §1` and `D02 T10 §2` (shaped text runs for font embedding and text merge fields); `D02 T11 §1` live-effect framework; `D02 T12 §2` document raster effects resolution; `D02 T14 §2` (PdfPig decision, reused test-side), `D02 T14 §9` (EPS handling), `D02 T16 §11` (ZXing.Net QR for merge fields); `D02 T15 §4` consumes §4's bleed box; backlog B-011 promoted (`-> SOURCE: legacy-nodus-9`), B-023 shares the D01 T04 engine; references: ISO 32000-1 (PDF 1.7), ISO 15930-1/-3/-7 (PDF/X), ISO 19005-1/-2 (PDF/A), ISO 14289-1 (PDF/UA), Adobe PostScript Language Reference 3rd edition, DSC 3.0, PPD 4.3, OPI 2.0, Microsoft Learn System.Printing and XpsDocumentWriter.
- **Adjacency:** list=applicable @ D02 T13 §3; document=applicable @ D02 T13 §2; settings=applicable @ D02 T13 §1; reporting=applicable @ D02 T13 §9; notifications=applicable @ D02 T13 §2; permissions=applicable @ D02 T13 §16; audit=applicable @ D02 T13 §7; exchange=applicable @ D02 T13 §14; reverse=applicable @ D02 T13 §1
- **Adjacency rationale:** Print styles, PDF presets, proof presets, and the ink list are the lists; the printed sheet and the PDF are the carried documents; color settings, print styles, and PDF presets are settings with the print and PDF pipelines as consumers; print summary and preflight are the reports; a spooling job shows progress and a completion toast on the status strip; an offline printer, a read-only target, and a password-protected PDF are the refusal cases; overprint, trap, assign, and convert are undoable commands with log lines; PDF, PostScript, ICC, CSV, and XML are the exchange formats; assign and convert profile undo, and every preset delete is reversible until the dialog closes.

#### §1. Document color settings: profiles, policies, assign, convert, and embed

- **Deliverable:** A Color Settings dialog (Default and Document tabs, presets) and the document color profile model: open, import, and paste policies with mismatch dialogs, Assign and Convert to Profile as undoable commands, profile embed and extract on save, open, and import, and Appearance of Black.
- **Depends On:** D01 T04 §2
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/color-settings/. Job: a designer can set the document's RGB, CMYK, and gray profiles and policies and convert or assign without surprise; consumer: every render, print, and PDF path. Treatment: Edit, Color Settings (Shift+Ctrl+K) with Default and Document tabs and the three profile dialogs; cheaper substitute that fails: a CMYK dropdown that relabels the enum without an ICC transform. Chrome: consume the D01 T04 engine, the Photon.UI dialog chrome, the settings store, and the suite history; do not add a second profile loader or a Nodus-local transform cache.
- **Runs:** **Requires:** display-session -- the dialogs and the status-bar flyout are driven and captured on an interactive desktop
- **Catalog:** NP-2086 to NP-2102 (17 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Color/DocumentColorSettings.cs`: RGB, CMYK, gray profile refs, primary color mode (replacing `ColorMode`), intent, black point compensation, spot definition policy (Lab, CMYK, RGB).
  - Persist in SVG as a `<color-profile>` element plus `nodus:color-settings` (profile hash, intent, policy); an embedded profile keeps its bytes, so reopen needs no system profile.
  - Settings keys `nodus.color.defaults.{rgb,cmyk,gray}`, `nodus.color.policy.open.{rgb,cmyk,gray}` (UseEmbedded, AssignDefault, ConvertToDefault), `nodus.color.policy.importPaste.*`, `nodus.color.warnMismatch`, `nodus.color.warnMissing`, `nodus.color.blackOnScreen`, `nodus.color.blackOnOutput`.
  - Presets as JSON under `%LOCALAPPDATA%/Rizonesoft/Photon/nodus/color-presets/`: General Purpose, Prepress, Web, Minimal Color Management, Simulate Color Management Off, built on the freely redistributable profiles D01 T04 §1 bundles; Save and Delete preset.
  - `AssignProfileCommand` (keeps numbers) and `ConvertToProfileCommand` (keeps appearance with a chosen intent, walks every fill, stroke, gradient stop, mesh node, and bitmap via D01 T04 §3) as one undo step each with one Serilog Information line.
  - `ProfileMismatchDialog` and `MissingProfileDialog` for open, import, and paste, driven by the policies; paste across documents applies the import and paste policy.
  - Embed on save and export (SVG, PDF OutputIntent and ICCBased through §14, PNG and TIFF iCCP via WIC); Extract embedded profile writes it into the profile folder named by D01 T04 §1.
  - Safe CMYK workflow: CMYK numbers are never round-tripped through RGB on open, import, paste, or print unless the policy converts; web preset recommends sRGB.
  - Appearance of Black: rich or accurate black on screen and on output, consumed by the canvas renderer and §5 and §14.
  - Status bar flyout showing the document profiles, opening the dialog's Document tab.
  - Canvas renders through the display profile (D01 T04 §1 monitor profile lookup); a changed monitor profile re-renders.
  - Tests `tests/Photon.Nodus.Tests/Color/DocumentColorSettingsTests.cs` and `AssignConvertCommandTests.cs`; fixtures `tests/fixtures/nodus/icc/` (SVG with embedded FOGRA39-class profile, untagged, mismatched).
- **Proof:** Format fidelity: `tests/fixtures/nodus/icc/embedded.svg` opened, converted to the CMYK default, saved, and reopened compares Lab values per swatch against lcms2 `transicc` goldens within dE00 0.5; substitute that fails: storing the profile name without its bytes.

#### §2. The print dialog: printers, range, copies, placement, scaling, and preview

- **Deliverable:** File, Print (Ctrl+P) as Nodus's own print dialog on a recorded printing path (WPF/.NET System.Printing and XPS, or GDI), with printer choice and driver preferences, copies, collate, reverse order, range, media, orientation, layers, placement, scaling, mini and full Print Preview, and Print to PDF.
- **Depends On:** D02 T07 §3
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/print-dialog/ and docs/captures/nodus/print-preview/. Job: a designer can print chosen pages or artboards to any installed printer at the right size and position; consumer: the Windows spooler and Microsoft Print to PDF. Treatment: a category-paged dialog (General, Layout, then pages later sections add) with a live mini preview; cheaper substitute that fails: `System.Windows.Controls.PrintDialog.PrintVisual` of the canvas control, which prints the viewport raster at screen resolution. Chrome: consume Photon.UI dialog chrome, numeric fields with units, the settings store, the status strip progress, and the toast service; do not build a second preview renderer (reuse the canvas scene renderer).
- **Runs:** **Requires:** display-session -- printing to Microsoft Print to PDF and capturing the dialog need an interactive desktop
- **Catalog:** NP-2117 to NP-2127 (11 features)
- **Hints:**
  - `-> SOURCE: legacy-nodus-9`: backlog B-011 is promoted here; remove it from `todo/backlog.md` in the same commit.
  - Decision row in `docs/dev/decisions.md`: WPF `PrintQueue`, `PrintTicket`, and `XpsDocumentWriter` with a `FixedDocument` of vector `DrawingVisual` pages, versus GDI (`StartDoc` with `DOCINFO.lpszOutput`); record vector fidelity, CMYK and spot limits, and how the proof run names the output file without a prompt, measured on this host.
  - `src/Nodus/Photon.Nodus.Core/Print/PrintJobSettings.cs` (printer, copies, collate, reverse, range, media, orientation, layers mode, placement, scale) and `PrintPlanner.cs` (sheets, page to sheet transform, skip blank).
  - `IPrintBackend` with the chosen implementation in `src/Nodus/Photon.Nodus.Desktop/Print/`; scene to WPF geometry via one `NodusDrawingVisualBuilder` (paths, gradients, bitmaps, text as glyph runs).
  - Printer list from `LocalPrintServer.GetPrintQueues()`, capabilities from `PrintQueue.GetPrintCapabilities()` (media sizes, printable area); Preferences button opens the driver sheet through `DocumentPropertiesW` with `PrintTicketConverter` round-tripping DEVMODE.
  - Range: all, current, pages or artboards range string (`1-3,5`), even, odd, selection, ignore artboards, skip blank; print layers visible and printable, visible, all (reads the D02 T02 §6 printable flag, adding it if absent).
  - Media and orientation: media from the queue, auto-rotate, transverse, match orientation; changing size or orientation here updates the page through an undoable `SetPageSizeCommand` when the user opts in.
  - Placement origin (9-point) with drag in the mini preview and numeric X/Y; scaling as in document, fit to page, custom percent, reposition with size; print to fit the paper size requests a custom media size.
  - `PrintPreviewWindow` (File, Print Preview) with zoom and page navigation; the mini preview renders the same `PrintPlanner` output.
  - Print to PDF entry routes through an `IPdfJobWriter` seam backed by D02 T04 §4 `PdfExporter` until §14 replaces it.
  - Progress on the status strip with cancel, a toast on completion, and one Serilog Information line per job (printer, pages, copies).
  - Tests `tests/Photon.Nodus.Tests/Print/PrintPlannerTests.cs` (ranges, skip blank, scaling, placement, orientation) and `PrintToPdfDriverTests` (guarded by the display-session requirement).
- **Proof:** Driven run plus unit test: print `tests/fixtures/nodus/print/two-artboards.svg` to Microsoft Print to PDF, read the output with PdfPig, and assert page count, media box, and vector path operators present with no full-page image; substitute that fails: `PrintVisual` of the canvas (one image XObject per page).

#### §3. Print tiling, print styles, print to file, and print summaries

- **Deliverable:** Tiled printing (full pages or imageable areas, overlap, tiling marks) with the Print Tiling tool and View toggle, saved print styles and presets, print to file with split options, and the print Summary page.
- **Depends On:** §2
- **Phase:** 10
- **Surface:** Fidelity: extends the print dialog; captured to docs/captures/nodus/print-dialog/. Job: a designer can print a poster across sheets and reuse named print settings; consumer: `PrintPlanner` and the saved style files. Treatment: tiling controls on General plus a canvas tiling overlay; cheaper substitute that fails: scaling the poster down to one sheet. Chrome: consume the §2 dialog, the D02 T16 §2 tool rail, and the settings store; do not add a second preset store beside the style files.
- **Runs:** **Requires:** display-session -- the tiling tool and overlay are driven on the canvas
- **Catalog:** NP-2128 to NP-2132 (5 features)
- **Hints:**
  - `PrintPlanner` tiling: none, full pages, imageable areas; overlap in units or percent of page width; tile order row-major with tile labels.
  - Tiling marks (corner ticks and labels) drawn per tile; consumed by §4's mark renderer once it ships.
  - `PrintTilingTool` in the Hand flyout moves the tiling origin; View, Show Print Tiling draws the tile grid overlay; origin persists as `nodus:print-tiling` on the document.
  - `PrintStyle` JSON under `%LOCALAPPDATA%/Rizonesoft/Photon/nodus/print-styles/`: Save As, Load, Delete, Import, Export; Edit, Print Presets dialog lists them; default style name in `nodus.print.defaultStyle`.
  - Print to file: PRN through the driver's spool output, PDF through the §2 seam; PostScript deferred to D02 T13 §10, which adds `PostScriptWriter` and enables the option here.
  - Split options: single file, pages to separate files, plates to separate files (plates enabled by §5).
  - Summary page lists every setting and warning; Save Summary writes a UTF-8 text file.
  - Tests `PrintTilingTests` (tile count and overlap geometry for A1 on A4) and `PrintStyleStoreTests` (round trip, delete, import of a foreign file refused by schema).
- **Proof:** Unit test plus driven run: `PrintTilingTests` asserts an A1 fixture tiles to 8 A4 sheets with 10 mm overlap, and a driven Microsoft Print to PDF run yields 8 pages; substitute that fails: fit-to-page (1 page).

#### §4. Printer's marks and bleed

- **Deliverable:** Printer's marks (crop, trim, fold, registration, calibration bar, densitometer, file information and page numbers, Roman or Japanese style) with bleed and bleed limit, a marks placement tool in Print Preview, marks attached to object bounds, the Crop Marks live effect, and Create Trim Marks.
- **Depends On:** §2
- **Phase:** 10
- **Surface:** Fidelity: extends the print dialog and Print Preview; captured to docs/captures/nodus/print-preview/. Job: a print shop receives sheets it can trim and register; consumer: the printed sheet and §15's PDF marks. Treatment: a Marks and Bleed page plus draggable marks in preview; cheaper substitute that fails: marks drawn at the page edge with no bleed extension of art. Chrome: consume §2's dialog and preview, D02 T11 §1 effect framework, and the suite history; do not duplicate the mark geometry between print and PDF (one `PrinterMarksRenderer`).
- **Runs:** **Requires:** display-session -- the marks placement tool is driven in Print Preview
- **Catalog:** NP-2133 to NP-2144 (12 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Print/PrinterMarksRenderer.cs` emits mark geometry as scene objects in registration color: crop and trim (weight, offset), fold, registration target, CMYK and spot calibration bar, seven-step densitometer with editable densities, file info (job, profile, date, plate), page numbers.
  - Mark style Roman or Japanese (double crop marks); preference `nodus.print.japaneseCropMarks`.
  - Document bleed per side on the page model (`nodus:bleed`), use document bleed, and bleed limit clipping art beyond crop marks.
  - Composite crop marks on all plates preference `nodus.print.compositeCropMarks` (consumed by §5).
  - Marks to objects: marks follow the selection bounding box instead of the page.
  - `MarksPlacementTool` in Print Preview: auto-position or drag against an alignment rectangle; offsets saved in the print style.
  - Crop Marks live effect via D02 T11 §1 (parameters in `nodus:` namespace, expanded marks as fallback).
  - Object, Create Trim Marks as an undoable command creating a grouped, locked-free mark set around the selection.
  - Tests `PrinterMarksRendererTests` (mark positions for Letter with 3 mm bleed and 6 mm offset) and `CreateTrimMarksCommandTests` (undo removes all marks).
- **Proof:** Format fidelity plus driven run: marks for `tests/fixtures/nodus/print/bleed-card.svg` compare element by element with a committed golden SVG, and the Microsoft Print to PDF output shows art extending 3 mm past the trim; substitute that fails: marks with art clipped at trim.

#### §5. Separations, halftone screens, and the ink manager

- **Deliverable:** Composite or separated output (host-based plates, in-RIP for PostScript devices), plate choice and order, the ink manager with per-ink screens, film options, spot-to-process conversion, and print color management (application or printer, printer profile, intent, preserve numbers, output color space, proof settings).
- **Depends On:** §2, §1
- **Phase:** 10
- **Surface:** Fidelity: extends the print dialog with Color and Separations pages; captured to docs/captures/nodus/print-dialog/. Job: a prepress user can output one plate per ink with correct screens; consumer: the printer or the plate files. Treatment: Output page with a plate list (print toggle, frequency, angle, dot shape) and an Ink Manager dialog; cheaper substitute that fails: printing four grayscale conversions of the composite. Chrome: consume D01 T04 transforms, D02 T09 §1 spot colors, and §2's pipeline; do not add a second CMYK conversion path.
- **Runs:** **Requires:** display-session -- plates are printed to Microsoft Print to PDF and the pages captured
- **Catalog:** NP-2145 to NP-2155 (11 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Print/InkSet.cs`: process inks plus document spots, alias, print toggle, frequency, angle, dot shape (round, ellipse, line, square), order; persisted in the print style.
  - `SeparationRenderer` renders one 8-bit plate per ink through the D01 T04 transform (preserve numbers or convert per policy), knocking out by default until D02 T13 §7 adds overprint flags.
  - Host-based separations print each plate as a grayscale page labeled with the ink name; composite prints the converted document.
  - `HalftoneScreen` rasterizer for host plates at printer resolution (AM screen per frequency, angle, dot shape); PostScript `sethalftone` emission wired by D02 T13 §10.
  - In-RIP separations enabled only for a PostScript queue with PPD (§10); otherwise disabled with a reason naming D02 T13 §10.
  - Film: emulsion down (mirror), negative (invert), printer resolution from the queue capabilities.
  - Convert all spot colors to process; output colors native, RGB, CMYK, grayscale; preserve color numbers; document color or proof settings (from §6 when shipped).
  - Color management by Nodus (printer profile plus intent) or by the printer (PostScript CRD pass-through in §10).
  - Spot separations warning threshold `nodus.print.spotWarning` (any, over 1, 2, 3); PostScript halftone screen on a bitmap stored as `nodus:halftone` on the image.
  - Tests `SeparationRendererTests` (plate tone values for C40 M0 Y0 K0 and a PANTONE-free spot fixture) and `InkSetTests` (order, alias merge).
- **Proof:** Format fidelity: plates of `tests/fixtures/nodus/print/cmyk-spot.svg` compare to lcms2-derived golden tone values within 1 percent per patch, and the driven print yields one page per selected ink; substitute that fails: plates derived from an RGB render.

#### §6. Soft proofing, gamut warning, overprint preview, and separations preview

- **Deliverable:** Proof Setup and Proof Colors on the canvas through D01 T04 §2 proofing transforms, the Color Proofing panel with presets, gamut warning, export and print proof, Overprint Preview, the Separations Preview panel, separations in Print Preview, and a rasterize complex effects view.
- **Depends On:** §1, §5
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/color-proofing/. Job: a designer can see on screen how the press and its inks will render; consumer: the canvas renderer and proof exports. Treatment: View menu toggles plus a Color Proofing panel and Separations Preview panel with per-plate eye toggles; cheaper substitute that fails: a desaturation filter over the canvas. Chrome: consume the D01 T04 proofing transform, §5 `SeparationRenderer`, Photon.UI panel chrome; do not render plates a second way.
- **Runs:** **Requires:** display-session -- proof toggles and the overlay are captured on the canvas
- **Catalog:** NP-2103 to NP-2116 (14 features)
- **Hints:**
  - `ProofSettings` (device profile, preserve numbers, intent, simulate paper color and black ink) with presets under `%LOCALAPPDATA%/Rizonesoft/Photon/nodus/proof-presets/`; includes protanopia and deuteranopia simulations.
  - View, Proof Colors toggle (menu and status-bar button); `nodus.proof.onByDefault` preference.
  - Canvas renderer applies the proofing transform as a final pass on the rendered tile; cache per tile and per settings hash.
  - Gamut warning overlay with color and opacity from the panel, using the D01 T04 §2 gamut check.
  - View, Overprint Preview (Alt+Shift+Ctrl+Y) composes §5 plates subtractively (objects knock out until D02 T13 §7 adds overprint flags); spot inks from their Lab values.
  - Separations Preview panel: overprint toggle, per-plate visibility, spot-only view; Print Preview gains composite and per-plate tabs.
  - View, Rasterize Complex Effects renders transparency and effects at output resolution for preview.
  - Export soft proof to JPEG, TIFF (WIC), and PDF (§14 when shipped, D02 T04 §4 before); CPT refused by name.
  - Print proof routes the proofed render through §2.
  - Tests `ProofTransformTests` (FOGRA39-class simulation of sRGB patches against `transicc` goldens) and `OverprintPreviewTests` (C100 over M100 overprint yields blue, knockout yields magenta).
- **Proof:** Unit test plus capture: `OverprintPreviewTests` and `ProofTransformTests` pass within dE00 1.0 and a proof-on capture is committed; substitute that fails: a global saturation reduction.

#### §7. Overprint attributes and trapping

- **Deliverable:** Overprint fill, stroke, bitmap, and text on objects (Attributes panel, Object and context menus, Properties), overprint black by threshold, document overprint handling (ignore, preserve, simulate), per-plate overprint, white overprint discard, the Trap command and Trap effect, auto-spreading trap, and in-RIP trapping settings.
- **Depends On:** §5
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/attributes-panel/. Job: a prepress user can set objects to overprint and add traps so misregistration shows no gaps; consumer: §5 plates, §6 preview, and §14 PDF. Treatment: Window, Attributes (Ctrl+F11) with overprint checkboxes and a Trap dialog; cheaper substitute that fails: a flag that only changes the canvas look. Chrome: consume the suite history, D02 T08 §10 path operations for trap geometry, and D02 T11 §1 effect framework; do not add a second boolean engine.
- **Runs:** **Requires:** display-session -- the Attributes panel and Trap dialog are driven and captured
- **Catalog:** NP-2156 to NP-2168 (13 features)
- **Hints:**
  - Object attributes `OverprintFill`, `OverprintStroke` (bitmaps and text runs included) persisted as `nodus:overprint-fill` and `nodus:overprint-stroke`; `SetOverprintCommand` undoable with one log line.
  - Attributes panel with overprint fill and stroke; its fill rule, reverse direction, image map, and note fields bind to the sections that own them.
  - Object, Overprint Fill, Stroke, Bitmap and the context menu entries call the same command.
  - Edit Colors, Overprint Black: black percentage threshold, fill and stroke, include CMYK and spot blacks.
  - Print options: always overprint black (threshold preference `nodus.print.overprintBlackThreshold`, default 95), document overprints ignore, preserve, or simulate (simulate rasterizes through §6), overprint graphics or text per plate.
  - Discard white overprint on output (document option) with a detection pass listed by §9 preflight.
  - Object, Trap (Pathfinder menu) builds trap objects: width, height, tint reduction, process traps, reverse traps, using lighter-into-darker neutral density; Trap live effect per D02 T07 §1.
  - Auto-spreading trap on print: overprinting outlines of the fill color up to a maximum or fixed width, text above a size.
  - In-RIP trapping settings (widths, image placement, thresholds, ink types, color reduction) stored in the print style and emitted by §10 as trapping parameters and in §14 as the PDF `Trapped` key.
  - Tests `OverprintCommandTests`, `TrapBuilderTests` (trap width and direction for yellow over cyan) and `OverprintBlackTests`.
- **Proof:** Format fidelity: `tests/fixtures/nodus/print/trap.svg` trapped and saved compares element by element with a golden, and §5 plates show the spread; substitute that fails: a stroke added in the canvas only.

#### §8. Transparency flattening and the flattener preview

- **Deliverable:** Object, Flatten Transparency with flattener presets (High, Medium, Low, custom), the Flattener Preview panel, print Advanced options (print as bitmap, overprint mode, flattener preset), compatible gradient and mesh printing, and raster effects resolution in print.
- **Depends On:** §2
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/flattener-preview/. Job: a designer can send transparent art to a device without transparency support and see which regions rasterize; consumer: §2 output, §10 PostScript, and §15 PDF/X-1a. Treatment: a Flattener Preview panel highlighting regions on the canvas; cheaper substitute that fails: rasterizing the whole page. Chrome: consume D02 T08 §10 path operations, D01 T03 raster buffers, the suite history; do not add a second rasterizer.
- **Runs:** **Requires:** display-session -- the preview highlight is captured on the canvas
- **Catalog:** NP-2169 to NP-2174 (6 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Print/TransparencyFlattener.cs`: planar map of overlapping transparent regions, vector atomic regions where raster/vector balance allows, else rasterized at the preset resolution with clip paths.
  - `FlattenerPreset` (raster/vector balance, line art and text resolution, gradient and mesh resolution, text to outlines, strokes to outlines, clip complex regions, anti-alias, preserve alpha, preserve overprints and spots) with High, Medium, Low built-ins and Edit, Transparency Flattener Presets for custom ones, import and export.
  - Flatten Transparency as one undoable command with a log line (object count in and out).
  - Flattener Preview panel: highlight rasterized complex regions, transparent objects, all affected objects, expanded patterns, outlined strokes and text; refresh; overprint mode.
  - Print as bitmap at a set dpi (dithering from D01 T03 §3 for 1-bit devices) and print Advanced overprint preserve, discard, simulate.
  - Compatible gradient and mesh printing rasterizes shadings for older devices; raster effects resolution taken from D02 T12 §2.
  - Banding guidance text in the Summary (steps versus lpi and resolution).
  - Budget: a 2,000-object page with 200 transparent objects flattens under 5 seconds with cancellation.
  - Tests `TransparencyFlattenerTests` (opacity 50 percent overlap flattens to 3 opaque regions with correct blended colors) and `FlattenerPresetStoreTests`.
- **Proof:** Format fidelity: `tests/fixtures/nodus/print/transparency.svg` flattened renders within 1 percent pixel tolerance of the unflattened render and contains no opacity attributes; substitute that fails: one full-page raster.

#### §9. Preflight, Package, and Collect for Output

- **Deliverable:** A preflight engine with savable styles shown in Print, PDF, and export dialogs (missing fonts, RGB in CMYK jobs, banded fountain fills, too many fonts, spot count, white overprint, low-resolution images), and File, Package / Collect for Output gathering the document, links, fonts, and a report.
- **Depends On:** §2
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/preflight/. Job: a designer can see output problems before sending and hand a print shop everything needed; consumer: the print shop folder. Treatment: a Preflight tab with issue list and suggestion per issue, plus a Package dialog; cheaper substitute that fails: copying the SVG alone. Chrome: consume the settings store and the status strip progress; do not write a second link resolver.
- **Runs:** **Requires:** display-session -- the Package dialog and preflight tab are driven
- **Catalog:** NP-2175 to NP-2178 (4 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Preflight/PreflightEngine.cs` with `IPreflightRule` rules and a `PreflightStyle` (enabled rules, thresholds) stored under `%LOCALAPPDATA%/Rizonesoft/Photon/nodus/preflight-styles/`.
  - Rules: missing or non-embeddable fonts, many fonts threshold, banded fountain fill (steps versus span and lpi), spot count, RGB or Lab in a CMYK job, image under effective ppi, white overprint, hairlines, off-page objects.
  - One preflight tab control in `src/Nodus/Photon.Nodus.Desktop/Views/Preflight/` reused by Print, PDF (§15), and the AI export dialog.
  - Package (Alt+Shift+Ctrl+P) and Collect for Output: copy document, copy links (collect in a subfolder, relink to the copy), copy fonts whose OS/2 fsType allows installable or editable embedding, create report.
  - Report as UTF-8 text listing fonts, links, colors, inks, and preflight results; one log line per package.
  - Refusal: a read-only or existing non-empty target folder stops with a named message.
  - Tests `PreflightEngineTests` (each rule fires on its fixture) and `PackageServiceTests` (copies and relinks, skips a restricted font).
- **Proof:** Unit test plus driven run: `PackageServiceTests` produce a folder whose document opens with all links resolved from the package; substitute that fails: absolute links left pointing at the source.

#### §10. PostScript output and driver compatibility options

- **Deliverable:** Nodus's own `PostScriptWriter` (DSC 3.0, level 2 or 3, ASCII or binary, flatness, fountain steps, font download as Type 1 or Type 42, bitmap compression and downsampling, halftones, in-RIP separations and trapping), PPD use, OPI links, and driver compatibility options for non-PostScript printers.
- **Depends On:** §2
- **Phase:** 10
- **Surface:** Fidelity: extends the print dialog with a PostScript page and Printing preferences; captured to docs/captures/nodus/print-dialog/. Job: a prepress user can write device-ready PostScript or print to a PostScript RIP; consumer: the RIP and the `.ps` file. Treatment: PostScript page controls enabled when the queue or file target is PostScript; cheaper substitute that fails: driver-generated PostScript from a GDI print. Chrome: consume §5 inks and screens, §7 trapping settings, and §2's pipeline; do not add a second page renderer.
- **Runs:** **Requires:** display-session -- the PostScript page is driven and captured
- **Catalog:** NP-2179 to NP-2188 (10 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/PostScript/PostScriptWriter.cs` writing DSC-conforming output (`%%BoundingBox`, `%%Pages`, `%%DocumentProcessColors`, `%%PlateColor`), level 2 or 3, ASCII85 or binary.
  - Paths, gradients as `shfill` (level 3) or stepped fills (level 2 with optimize and auto increase steps), flatness with auto increase, bitmaps with Flate or DCT and downsampling thresholds.
  - Fonts: Type 42 for TrueType, CFF as FontType 2 via `StartData`, or text as outlines; the TrueType to Type 1 option documented as Type 42.
  - `sethalftone` type 1 per plate from §5, `setpagedevice` Separations and trapping parameters from §7, CRD pass-through when the printer manages color.
  - PPD parser for `*DefaultResolution`, `*PageSize`, `*ColorDevice`, `*LanguageLevel`; Use PPD option.
  - OPI: import TIFF as an OPI proxy with the high-resolution path (`nodus:opi`), emit `%ALDImageFileName` comments, and the PDF OPI dictionary through §14.
  - Driver compatibility preferences for GDI printers: text as graphics, software clipping, 64k bitmap chunks, send curves; bitmap output threshold and chunk overlap.
  - Enables §3's PostScript print-to-file option and §5's in-RIP separations.
  - Tests `PostScriptWriterTests` asserting DSC structure; format fidelity renders output with a user-installed Ghostscript when present (version recorded) and compares against the canvas within 2 percent, else the structural test alone runs and says so.
- **Proof:** Format fidelity: `tests/fixtures/nodus/postscript/` goldens rendered by Ghostscript (external, AGPL, never bundled, version recorded) compare within 2 percent pixels; substitute that fails: a `.ps` that embeds one page raster.

#### §11. Imposition, binding, and page placement

- **Deliverable:** Imposition layouts in Print Preview: presets and edit and save, the imposition layout tool, pages across and down, single or double sided with a manual-duplex wizard, binding modes, page placement ordering, manual sequence and rotation, gutters with cut and fold marks, and margins.
- **Depends On:** §4
- **Phase:** 10
- **Surface:** Fidelity: extends Print Preview; captured to docs/captures/nodus/print-preview/. Job: a user can print booklets and n-up sheets that fold and cut into the right order; consumer: `PrintPlanner` sheets. Treatment: an imposition layout tool with Basic, Placements, Gutters and Finishing, Margins modes; cheaper substitute that fails: n-up in sequential order only. Chrome: consume §2's preview and §4's fold and cut marks; do not add a second sheet model.
- **Runs:** **Requires:** display-session -- the imposition tool is driven in Print Preview
- **Catalog:** NP-2189 to NP-2196 (8 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Print/Imposition/ImpositionLayout.cs`: across, down, sides, binding (perfect, saddle stitch, collate and cut, custom), placement ordering, gutters, margins.
  - `ImpositionPlanner` maps document pages to signature frames with rotation; saddle stitch nests signatures (page count padded to a multiple of 4).
  - Placement ordering intelligent, sequential, cloned, and manual per-frame sequence number and rotation.
  - Gutters auto or equal with size; cut and fold locations drawn by §4's mark renderer.
  - Presets (2x2 4-up, 2x3 6-up, booklet) and saved layouts as JSON beside print styles.
  - Manual-duplex wizard prints fronts, prompts to reinsert, then backs.
  - Tests `ImpositionPlannerTests` (8-page saddle stitch yields sheet 1 front pages 8 and 1, back 2 and 7).
- **Proof:** Unit test plus driven run: `ImpositionPlannerTests` pass and an 8-page booklet printed to Microsoft Print to PDF yields 4 sheet sides in saddle order; substitute that fails: sequential 2-up.

#### §12. Layout styles, labels, and banners

- **Deliverable:** Layout, Page Layout with layout styles (full page, book, booklet, tent, side-fold, top-fold, tri-fold), label presets and custom label styles, Save as Default, and Layout, Border and Grommet for banner documents.
- **Depends On:** D02 T07 §4
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/page-layout/. Job: a user can design folded cards, brochures, labels, and banners with panels that print in the right place; consumer: the page model and §11's imposition. Treatment: Page Layout dialog with style thumbnails, a label picker with preview, and a Border and Grommet dialog; cheaper substitute that fails: a guide grid with no print mapping. Chrome: consume the D02 T07 §3 page model and settings store; do not add a second page size table.
- **Runs:** **Requires:** display-session -- the dialogs are driven and captured
- **Catalog:** NP-2197 to NP-2206 (10 features)
- **Hints:**
  - `LayoutStyle` on the document (`nodus:layout-style`): each style defines panels per sheet, their order, and rotation; consumed by `PrintPlanner` and §11.
  - Folded styles render fold guides on the canvas; tri-fold auto-orders panels for printing.
  - Label definitions as JSON (sheet size, rows, columns, margins, gutters, label size) with a small public-domain starter set and import of user files; no manufacturer catalog bundled without a data license.
  - Customize label style dialog saves a new definition; labels map to pages at print time.
  - Save as Default writes page size and layout to `nodus.document.defaultPage`.
  - Border and Grommet creates a new banner document from the page or selection: border page color, solid, stretch edges, mirror edges with size; grommet markers by count or spacing at corners and sides with size and margin.
  - Changing layout style is one undoable command.
  - Tests `LayoutStyleTests` (tri-fold panel order) and `GrommetPlacementTests`.
- **Proof:** Format fidelity plus unit test: a tri-fold fixture saves and reopens with its style, and the printed sheet order matches the golden panel map; substitute that fails: panels printed in document order.

#### §13. Print merge and variable data

- **Deliverable:** Print Merge (data sources TXT, CSV, RTF, XLSX, ODBC; columns, records, text, image, and QR fields; print or create a merged document) and the Variables panel (visibility, text, linked file, graph data variables; data sets; XML and CSV libraries; one file per data set).
- **Depends On:** §2, D02 T10 §2
- **Phase:** 10
- **Surface:** Fidelity: new build, no baseline; captured to docs/captures/nodus/print-merge/ and docs/captures/nodus/variables/. Job: a user can produce personalized cards or badges from a spreadsheet; consumer: the printer, the merged document, and per-set exports. Treatment: a Configure Data Source dialog with a record grid and a Variables panel; cheaper substitute that fails: find-and-replace per record by hand. Chrome: consume D02 T10 §2 text runs, D02 T16 §11 QR generation, §2 printing, the suite history; do not add a second CSV parser if D02 T14 §14 ships one first.
- **Runs:** **Requires:** display-session -- the data source dialog and panel are driven
- **Catalog:** NP-2207 to NP-2224 (18 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Core/Merge/MergeDataSource.cs`: columns (text, numeric with format and auto-increment, path), records, selection; persisted in the document as `nodus:merge-data` when `nodus.merge.saveInDocument` is on.
  - Readers: CSV and TXT (RFC 4180), RTF tables (own), XLSX via DocumentFormat.OpenXml (sheet choice), ODBC via `System.Data.Odbc`; save data source to CSV; sync re-reads a changed source.
  - Configure Data Source dialog: add, delete, edit records, browse paths, view all or single, first, previous, next, last, go to record, select all or none, import column, clear merge data.
  - Merge fields as live objects (`nodus:merge-field`): text (inside or standalone text), image placeholder with scaling (actual, fill, fit, stretch, reference point), QR code with type and scaling.
  - Update Field and Find, Print Merge Fields in Find and Replace.
  - Print Merged Document through §2; Create Merged Document writes one page per record.
  - Variables panel: variable types bound to objects, Make Dynamic, Unbind, Select Bound Object; data sets capture, next, previous, rename, delete.
  - Variable library XML (Illustrator variable library schema) and CSV import and export with `@` image path columns.
  - Export one file per data set as a Nodus command (SVG, PDF, PNG) with progress and cancel.
  - Tests `MergeDataSourceTests` (CSV quoting, XLSX sheet, numeric auto-increment), `MergeRenderTests` (3 records produce 3 pages with the right text), `VariableLibraryTests` (XML round trip).
- **Proof:** Format fidelity: `tests/fixtures/nodus/merge/badges.csv` with `badges.svg` creates a merged document compared element by element to a golden, and the variable library XML round-trips byte-equal after normalization; substitute that fails: text replaced in one page only.

#### §14. The PDF writer: spot colors, layers, and exact vector output

- **Deliverable:** Nodus's own PDF content-stream writer on PDFsharp (MIT) replacing the D02 T04 §4 `SKDocument` exporter: exact paths, shadings for gradients and mesh, patterns, transparency groups and soft masks, blend modes, Separation and DeviceN spots, CMYK and ICC output, OCG layers, embedded and subset fonts or text as curves, page boxes, and Publish to PDF with range, page size, and only-on-page options.
- **Depends On:** §1, D02 T04 §4
- **Phase:** 10
- **Surface:** Fidelity: extends the D02 T04 §4 export dialog; captured to docs/captures/nodus/export-pdf/. Job: a designer can send a PDF that a print shop's RIP reproduces exactly; consumer: the PDF file, Acrobat, and RIPs. Treatment: File, Publish to PDF with General and Objects pages; cheaper substitute that fails: the `SKDocument` output, which cannot express spot colors, OCGs, or CMYK. Chrome: consume §1 profiles, the atomic file writer, and the D02 T04 §4 dialog shell; do not keep two PDF writers after this section.
- **Runs:** **Requires:** display-session -- the Publish to PDF dialog is driven and captured
- **Catalog:** NP-2225 to NP-2232 (8 features)
- **Hints:**
  - Add PDFsharp (MIT) to `Directory.Packages.props` with a `docs/dev/decisions.md` row (license versus GPL-3.0, why own content streams); PdfPig as a test-only reader, reusing the D02 T14 §2 decision.
  - `src/Nodus/Photon.Nodus.Core/Pdf/PdfContentWriter.cs` emits operators (`m l c h re`, `cm`, `q Q`, `gs`, `sh`, `Do`) with fixed 4-decimal precision; `PdfResourceBuilder` dedupes ExtGState, ColorSpace, Pattern, Shading, XObject, Font.
  - Gradients as type 2 and 3 shadings with stitching functions; mesh as type 6 or 7 (D02 T09 §9); pattern fills as tiling patterns (D02 T09 §10).
  - Opacity, blend modes (D02 T09 §19), and opacity masks as transparency groups with luminosity soft masks (D02 T09 §20).
  - Spot colors as Separation with a Lab or CMYK alternate and tint transform; multi-ink as DeviceN; CMYK native; ICCBased from §1.
  - Layers as OCGs with visibility and print state (`/OCProperties`); master layers excluded with a note.
  - Fonts: Type0 with CIDFontType2 and a TrueType glyf subset (own subsetter), CFF embedded, ToUnicode CMap; respect OS/2 fsType; subset threshold; export all text as curves; TrueType to Type 1 is a documented no-op.
  - Page boxes MediaBox, TrimBox, and BleedBox from the document bleed once §4 has shipped (BleedBox equals TrimBox before); export range document, several documents, selection, current page, pages; page size from document or selection; only objects on page clips off-page art.
  - Replace `PdfExporter` behind the `IPdfJobWriter` seam used by §2 and §6; keep `PdfExporterTests` green on the new writer.
  - Budget: a 10,000-object page writes under 3 seconds with progress and cancel.
  - Tests `PdfContentWriterTests` (operator stream per primitive), `PdfSpotColorTests`, `PdfOcgTests`, `PdfFontEmbeddingTests`.
- **Proof:** Format fidelity: fixtures under `tests/fixtures/nodus/pdf/` export, read back with PdfPig (paths, Separation names, OCG names, embedded fonts, text), and render against goldens from MuPDF `mutool draw` (external, AGPL, test-time only, version recorded) within 1 percent pixels; substitute that fails: `SKDocument` output (no Separation colorspace).

#### §15. PDF presets and standards: PDF/X, PDF/A, compatibility, compression, and marks

- **Deliverable:** PDF presets (built-in and custom) with PDF/X-1a, X-3, X-4 and PDF/A output, compatibility levels, compression and downsampling, marks and bleeds, output color conversion and profile inclusion, spot conversion, overprint and flattener options, the PDF preflight tab, summary, multi-document PDF, encoding, EPS handling, and complex fills as bitmaps.
- **Depends On:** §14, §4
- **Phase:** 10
- **Surface:** Fidelity: extends the §14 dialog with Preset, Compression, Marks and Bleeds, Output, Advanced, Preflight, Summary pages; captured to docs/captures/nodus/export-pdf/. Job: a designer can pick "PDF/X-4" and get a file the printer's preflight accepts; consumer: print shop preflight and archives. Treatment: preset dropdown with standards compliance; cheaper substitute that fails: setting the version key without enforcing the standard's rules. Chrome: consume §4 marks, §8 flattener, §9 preflight engine, §1 profiles; do not add a second preset store beside print styles.
- **Runs:** **Requires:** display-session -- preset pages are driven and captured
- **Catalog:** NP-2233 to NP-2251 (19 features)
- **Hints:**
  - `PdfExportSettings` and `PdfPreset` JSON under `%LOCALAPPDATA%/Rizonesoft/Photon/nodus/pdf-presets/`: built-ins High Quality Print, Press Quality, Smallest File Size, PDF/X-1a, PDF/X-3, PDF/X-4, Prepress, Archiving CMYK and RGB (PDF/A), Document Distribution, Editing, Web, Current Proof Settings; create, edit, delete, import, export.
  - Standards: `PdfStandardEnforcer` applies ISO 15930 rules (OutputIntent with GTS_PDFX, TrimBox, fonts embedded, no transparency for X-1a and X-3 via §8, no RGB for X-1a) and ISO 19005 rules for PDF/A (XMP metadata, no encryption, embedded profile).
  - Compatibility 1.3 to 1.7 gates features (transparency needs 1.4, OCGs 1.5); conflicts are reported, not silently dropped.
  - Compression: Flate via `ZLibStream`, JPEG via WIC with quality, LZW (own encoder), downsampling average, bicubic, subsample with thresholds; JPEG2000 and CCITT refused by name; compress text and line art; ASCII85 or binary encoding.
  - Marks and bleeds from §4 `PrinterMarksRenderer`, bleed limit.
  - Output: convert to destination, profile inclusion policy, document or proof settings (§6), convert spot colors, preserve overprints, always overprint black; subset threshold and flattener preset in Advanced.
  - PDF preflight tab reuses §9; Summary lists settings and warnings with Save Summary.
  - General: view after saving, thumbnails, layers from top-level layers, one PDF from several open documents, EPS as PostScript XObject or preview, render complex fills as bitmaps.
  - Tests `PdfPresetStoreTests`, `PdfStandardEnforcerTests` (X-1a rejects an RGB image or converts it per preset), `PdfCompressionTests`.
- **Proof:** Format fidelity: PDF/A fixtures validate with veraPDF (version recorded) with zero failures, PDF/X fixtures pass `PdfStandardEnforcerTests` rule checks and carry the OutputIntent read back by PdfPig; substitute that fails: a version key with RGB content in a PDF/X-1a file.

#### §16. PDF interactivity and security: bookmarks, hyperlinks, tagged PDF, and passwords

- **Deliverable:** Hyperlinks, bookmarks, thumbnails, on-start view, comments, symbols as form XObjects, tagged accessible PDF with alt text, open and permissions passwords with print, edit, and copy permissions, and web-optimized (linearized) output.
- **Depends On:** §14
- **Phase:** 10
- **Surface:** Fidelity: extends the §14 dialog with Document and Security pages; captured to docs/captures/nodus/export-pdf/. Job: a designer can send an accessible, navigable, protected PDF; consumer: PDF readers and screen readers. Treatment: Document and Security pages with password fields that never persist; cheaper substitute that fails: a permissions flag without encryption. Chrome: consume §14 writer, the D02 T14 §17 hyperlink model, and D02 T09 §21 symbols; do not store passwords in presets or settings.
- **Runs:** **Requires:** display-session -- the Security page and a password-protected open are driven
- **Catalog:** NP-2252 to NP-2261 (10 features)
- **Hints:**
  - Hyperlinks from object URL attributes as Link annotations with URI actions; bookmarks from pages and named layers (outline tree); on-start view (page only, bookmarks, thumbnails) via `/PageMode`.
  - Page thumbnails as `/Thumb` images from the page render; include comments as Text annotations.
  - Symbols written once as form XObjects and referenced per instance.
  - Tagged PDF: StructTreeRoot, MarkInfo, marked-content IDs per object, `Figure` with `/Alt` from the object's `<desc>` or `nodus:alt`, reading order by layer order.
  - Security through the PDFsharp security handler: open password, permissions password, printing none, low, high; editing none, page assembly, any except extraction; copying; AES where the pinned version supports it, else RC4-128 recorded in the decision row.
  - Passwords never written to presets, settings, or logs (log line records only that encryption was applied).
  - Linearization by an own post-pass (ISO 32000-1 Annex F hint tables) checked with `qpdf --check-linearization` (external, Apache-2.0, test-time only).
  - Tests `PdfLinkBookmarkTests`, `PdfTaggingTests`, `PdfSecurityTests` (PdfPig refuses without the password and opens with it; permission bits match).
- **Proof:** Format fidelity: fixtures validate as PDF/UA-1 in veraPDF (version recorded) and as linearized in qpdf, and `PdfSecurityTests` read permissions back; substitute that fails: `/Alt` missing on figures or a password stored in the preset.

#### Sizing concerns

- §13 carries two data-merge systems (Corel Print Merge with five source readers and a record editor, and the Variables panel with data sets and XML libraries); at one checkbox per micro-step it likely exceeds 30 items; a split along those two lines at authoring time is the natural cut.
- §15 carries 40 inventory rows (presets, PDF/X and PDF/A enforcement, compression, output color, marks, preflight, summary); the standards enforcer plus the compression encoders may push it past 30 items; a split between presets and dialog pages and standards enforcement is the natural cut.
- §7 combines object overprint attributes with a trap geometry builder and in-RIP trapping settings; it is borderline at 30 items.
- §14 owns font subsetting and the content-stream writer together; if the glyf subsetter grows beyond a few items, it is the first candidate to move out.

### todo/02-nodus/TODO-14-nodus-parity-formats.md -- `nodus-parity-formats`

- **Title:** "TODO-14 -- Nodus Parity: File Formats, Export, and Web"
- **Phase(s):** 11
- **Goal:** A Nodus user can open, place, and save the files the rest of the industry sends (SVG with every export option, PDF, Illustrator .ai, CorelDRAW .cdr and .cmx, EPS and PostScript, DWG and DXF, metafiles and plotter files, every common raster format, PSD, office documents), can batch-export artboards, pages, and assets for screens and the web with optimized previews, slices, links, and rollovers, can draw pixel-perfect, and can exchange artwork through the clipboard, placed files, and a scanner, with every reader and writer proven against committed fixtures and goldens from a named reference implementation.
- **Current-state facts to verify (with claim candidates):**
  - `ImportService` refuses PDF outright and routes AI, EPS, and PDF through three stub methods. `<!-- claim: count "PDF import requires additional libraries" src/Nodus/Bezier.Core/Services/ImportService.cs = 1 -->` `<!-- claim: count "ImportFormat\.(Ai|Eps|Pdf) =>" src/Nodus/Bezier.Core/Services/ImportService.cs = 3 -->`
  - The AI and EPS stubs only search the file text for an embedded `<svg` and otherwise fail. `<!-- claim: count "Full AI support requires Adobe Illustrator" src/Nodus/Bezier.Core/Services/ImportService.cs = 1 -->`
  - `ImportService.ImportFromClipboard` already accepts SVG, image, and text clipboard payloads, but no app code calls it. `<!-- claim: count "clipboard\.Has(Svg|Image|Text)" src/Nodus/Bezier.Core/Services/ImportService.cs = 3 -->`
  - `SvgExportOptions` has only minify, IDs, XML declaration, viewBox, decimal precision, and inline styles; no SVGZ, CSS, font, or image options exist. `<!-- claim: count "public (int DecimalPrecision|bool UseInlineStyles)" src/Nodus/Bezier.Core/Services/SvgExporter.cs = 2 -->`
  - `ExportService` knows an ICO format (extension and MIME) that `D02 T06 §14` wires. `<!-- claim: count "ExportFormat\.Ico =>" src/Nodus/Bezier.Core/Services/ExportService.cs = 2 -->`
  - Copy and Paste in the main window only set the status text. `<!-- claim: count "StatusText = \"(Copy|Paste)\";" src/Nodus/Bezier.Desktop/ViewModels/MainWindowViewModel.cs = 2 -->`
  - `RawSvgDialog` shows the document's SVG source and copies it as plain text. `<!-- claim: count "Clipboard\.SetText\(_svgContent\)" src/Nodus/Bezier.Desktop/Views/RawSvgDialog.xaml.cs = 1 -->`
  - `SkiaCanvas` has a `PixelPreview` property passed to the renderer only at zoom 8 or more, and `SkiaRenderer` threads the flag through without using it. `<!-- claim: count "PixelPreview && _state\.Zoom >= 8" src/Nodus/Bezier.Desktop/Controls/Canvas/SkiaCanvas.cs = 1 -->` `<!-- claim: count "pixelPreview" src/Nodus/Bezier.Desktop/Services/SkiaRenderer.cs = 6 -->`
  - No format package (PdfPig, PDFsharp, ACadSharp, NPOI, DocumentFormat.OpenXml) is referenced yet. `<!-- claim: count "PdfPig|PDFsharp|ACadSharp|NPOI|DocumentFormat\.OpenXml" Directory.Packages.props = 0 -->`
  - There is no fixture tree and no decisions log yet. `<!-- claim: absent tests/fixtures -->` `<!-- claim: absent docs/dev/decisions.md -->`
  - No slice, rollover, or hyperlink model exists in Nodus. `<!-- claim: count "Rollover|Hyperlink" src/Nodus/Bezier.Core/Models/VectorElement.cs = 0 -->`
- **Inputs and XREFs:** `standards/nodus.md` (SVG is native, Inkscape is the reference), `standards/shared.md` (atomic saves, refusal messages), `standards/testing.md` (fixtures, goldens, the Fidelity trait); `D02 T04 §2` (SVG round-trip fixtures, extended by §1), `D02 T04 §3` (PNG and JPEG export, extended by §12, §15, §16), `D02 T06 §14` (place, one export dialog, WebP, ICO, XAML writers, extended by §12, §15, §19); `D02 T07 §1` (live-object contract, `nodus:` namespace), `D02 T07 §3` (pages and artboards), `D02 T07 §5` (layers, master layers, export flag), `D02 T07 §12` (view modes); `D02 T08 §15` (dimension objects); `D02 T10 §2` (rich text), `D02 T10 §13` (text import and export), `D02 T10 §14` (tables); `D02 T11 §1` (live-effect framework); `D02 T12 §1` (bitmap objects, convert to bitmap), `D02 T12 §7` (Links panel, Edit Original); `D02 T13 §10` (PostScript output), `D02 T13 §14` (PDF writer on PDFsharp); `D01 T03 §3` (palette quantization and dithering), `D01 T04 §1` and `D01 T04 §3` (ICC transforms, duotone bitmaps); `D01 T02 §2` (settings store), `D01 T02 §4` (suite history); references: PDF 2.0 (ISO 32000-2), Adobe Illustrator File Format Specification v7, Adobe Photoshop File Formats Specification, libcdr source (MPL-2.0), [MS-EMF] and [MS-WMF], ISO 8632 CGM, HP-GL/2 reference, SVG 1.1 and SVG 2.
- **Adjacency:** list=applicable @ D02 T14 §15 (the export list is the list of export assets, searchable and filterable); document=applicable @ D02 T14 §5 (the .ai and PDF a user sends onward); settings=applicable (every format option persists under `Nodus.Formats.<Format>.*` and `Nodus.Export.*` with a default and a reader); reporting=applicable @ D02 T14 §2 (every import and export writes a conversion report listing what was expanded, rasterized, or dropped); notifications=applicable @ D02 T14 §15 (background export progress, cancel, and a completion toast); permissions=applicable (password PDFs, locked or read-only targets, a missing Ghostscript or WIC extension, and a protected CDR are refused by name); audit=applicable (every import, place, and slice or link edit is one undoable command with one Serilog Information line); exchange=applicable (this file is the suite's exchange layer for vector, raster, CAD, and office formats); reverse=applicable (every import undoes as one step; slices, links, and rollovers release; export items delete; no export overwrites without a prompt).

#### §1. SVG options: SVGZ, styling modes, CSS export, and SVG code

- **Deliverable:** SVGZ read and write, Save SVG and Export SVG with the full option set, CSS export with the CSS Properties panel, and SVG code on the clipboard, each proven against Inkscape.
- **Depends On:** D02 T04 §2
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/svg-options/ | Job: a web designer exports SVG in the styling, ID, and precision a hand-off needs and copies CSS for named objects | Treatment: one SVG Options dialog shared by Save As SVG (keeps the `nodus:` namespace) and Export SVG (plain SVG), with a Show Code preview; the cheaper substitute that fails is a minify checkbox on the existing dialog | Chrome: consume the D02 T06 §14 export dialog shell, the settings store, and `Photon.UI` controls; do not add a second code viewer beside `RawSvgDialog`.
- **Runs:** Requires: display-session -- the options dialog, the CSS Properties panel, and clipboard paste need an interactive desktop
- **Catalog:** NP-2263 to NP-2268 (6 features)
- **Hints:**
  - Extend `SvgExportOptions` in `src/Nodus/Photon.Nodus.Core/Services/SvgExporter.cs` with `Styling` (PresentationAttributes, InternalCss, InlineStyle, ExternalCss), `FontMode` (SvgText, Outlines), `ImageMode` (Embed, Link, Preserve), `ObjectIds` (LayerNames, Minimal, Unique), `Responsive`, `Encoding` (UTF-8, UTF-16), and `KeepEditingData` (the `nodus:` namespace on Save, off on Export).
  - Add `SvgzCodec` (GZipStream over the reader and writer); `.svgz` joins `ImportService`'s extension table and the Save As filter.
  - Import options on `SvgImporter`: scaling Automatic, English, or Metric with a drawing scale, `clipPath` to clipping groups, `symbol` and `use` to symbols, linked and embedded images, `<a>` links, and metadata preserved.
  - Export fidelity rules: layers write as `<g id="layer name">`, symbols as `<symbol>`, effects the SVG profile cannot express rasterize through `D02 T12 §1` with a report line, and scope is document, page, or selection.
  - Add `CssExporter` in `Photon.Nodus.Core/Web/` generating class rules for named objects (fill, stroke, opacity, size, position, gradients as `linear-gradient`), and a `CssPropertiesPanel` in `Photon.Nodus.Desktop/Views/Panels/` with copy and export buttons and options (units, include vendor-free only, all named or selected).
  - Copy writes an `image/svg+xml` flavor and a plain-text SVG flavor next to the D02 T03 §3 payload; paste of SVG text creates art as one undoable `PasteSvgCommand`.
  - Show Code opens the SVG the current options would write, read-only, reusing `RawSvgDialog`.
  - Settings `Nodus.Formats.Svg.*` for every option with defaults matching Inkscape plain SVG; named presets stored in the settings store.
  - Log `Exported SVG {Path} ({Styling}, {Precision} dp)` once per export.
  - Fixtures `tests/fixtures/nodus/svg-options/`: one file per styling mode, font mode, ID mode, SVGZ pair, and CSS golden text, with Inkscape `--export-plain-svg` renders as goldens and the Inkscape version in `goldens/VERSION.txt`.
  - Tests: `SvgOptionsRoundTripTests` and `CssExporterTests` in `tests/Photon.Nodus.Tests/Formats/` under `[Trait("Category", "Fidelity")]`.
- **Proof:** Format fidelity: every option combination in `SvgOptionsRoundTripTests` re-imports to the same model and renders within the `D02 T04 §2` tolerance of the Inkscape golden, SVGZ decompresses to the byte-identical SVG, and the CSS golden matches exactly; the cheaper substitute that fails is asserting the output "contains <svg", which a dropped `style` element passes.

#### §2. PDF import

- **Deliverable:** Open and place PDF pages as editable art through PdfPig parsing and Nodus's own graphics-state interpreter, with page, crop-box, text, comments, and crop-to-page options and a fidelity proof against Inkscape with poppler.
- **Depends On:** D02 T07 §3, D02 T06 §14
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/pdf-import/ | Job: a designer opens a client's PDF and edits its paths and text | Treatment: a PDF Import dialog with page thumbnails (single, range, all), crop box, text as text or curves, maintain paragraphs, comments layer, crop to page, and a password prompt; the cheaper substitute that fails is placing the PDF as a rendered bitmap | Chrome: consume the settings store, `Photon.UI` dialogs and thumbnails, and the D02 T07 §3 page model; do not add a PDF renderer.
- **Runs:** Requires: display-session -- the import dialog and page thumbnails need an interactive desktop
- **Catalog:** NP-2269 to NP-2276 (8 features)
- **Hints:**
  - Add the PdfPig (Apache-2.0) package with its `docs/dev/decisions.md` row (license checked against GPL-3.0); PdfPig parses objects, streams, fonts, and encryption, Nodus interprets content streams.
  - `PdfContentInterpreter` in `src/Nodus/Photon.Nodus.Core/Formats/Pdf/`: graphics-state stack (CTM, clip, color spaces, line state, soft masks, blend modes), path operators to `SvgPath`, shading types 2 and 3 to gradients and 4 to 7 to mesh, XObject forms reused two or more times to symbols, images to bitmap objects.
  - `PdfImportOptions`: pages (single, range, all), target (new document pages or grouped objects on the current page), crop box (Bounding, Art, Crop, Trim, Bleed, Media), text as text or curves, maintain paragraphs, comments on a layer, crop content to page; persisted under `Nodus.Formats.Pdf.Import.*`.
  - Text reconstruction: glyph runs merged into lines by baseline and advance, lines into paragraphs by leading and proximity when "maintain paragraphs" is on, otherwise one point-text object per run, into the `D02 T10 §2` rich text model.
  - Optional content groups become layers (visibility kept); annotations (text, line, shape, markup, ink, stamp) land on a non-printing Comments layer grouped by author.
  - Separation and DeviceN images keep their inks through the `D01 T04 §3` duotone model; ICC-based spaces convert through `D01 T04 §1`.
  - Password-protected PDFs prompt once; a refused password or a certificate-encrypted file is refused by name.
  - A conversion report lists what was approximated (unsupported shading, Type 3 fonts to curves) and is shown in the import toast.
  - Budget: a 200-page PDF opens its dialog in under a second; interpretation runs off the UI thread with progress and Cancel.
  - Fixtures `tests/fixtures/nodus/pdf/`: authored PDFs for paths, gradients, transparency groups, OCGs, annotations, text flow, duotone image, and an encrypted file, with goldens rendered by Inkscape with poppler (`inkscape --pdf-poppler --export-type=png`) and versions recorded.
- **Proof:** Format fidelity: `PdfImportFidelityTests` render each imported fixture and compare against the Inkscape with poppler golden within the stated tolerance, and assert text content, layer names, and annotation count; the cheaper substitute that fails is a raster placement, which the text-content assertion catches.

#### §3. Illustrator import: PDF-compatible .ai files

- **Deliverable:** Open and place `.ai` and `.ait` files saved with PDF compatibility through the §2 PDF path, with artboards to pages and layers from OCGs.
- **Depends On:** §2
- **Phase:** 11
- **Surface:** no surface of its own (reuses the §2 import dialog with an Illustrator title and artboard wording)
- **Runs:** none
- **Catalog:** NP-2277 (1 features)
- **Hints:**
  - `AiFileDetector` in `src/Nodus/Photon.Nodus.Core/Formats/Ai/`: `%PDF` header means PDF-compatible, `%!PS-Adobe` with `%%Creator: Adobe Illustrator` means legacy (handed to §4), otherwise refused by name.
  - Replace the `ImportAdobeIllustrator` stub in `ImportService` with the detector plus the §2 reader; `.ait` opens as a new untitled document.
  - Artboards map to pages (`D02 T07 §3`) by the PDF page boxes; OCGs map to layers with visibility and lock.
  - Import options: text as text or curves; unsupported live features (appearance stacks, 3D, brushes) arrive as their PDF expansion with a report line.
  - A file saved without PDF compatibility, and with no `AIPrivateData` reader yet, is refused with the message naming §4's scope.
  - Fixtures `tests/fixtures/nodus/ai/pdf-compatible/`: files authored and saved by Illustrator 30.8 (license note in the README), goldens from Inkscape with poppler, versions recorded.
  - Log `Imported AI {Path} ({Artboards} artboards, {Layers} layers)`.
- **Proof:** Format fidelity: `AiPdfImportTests` compare each fixture's render and layer list with the Inkscape with poppler golden; the cheaper substitute that fails is the current embedded-`<svg` search, which finds nothing in a real `.ai`.

#### §4. Illustrator import: private data and legacy PostScript .ai

- **Deliverable:** Parse `AIPrivateData` and legacy PostScript AI (AI 3 to 8) from the published Illustrator File Format specification to recover native layers, groups, text, swatches, symbols, and gradients, read AICB from the clipboard, and append [Converted] on opening legacy files.
- **Depends On:** §3
- **Phase:** 11
- **Surface:** no surface of its own
- **Runs:** none
- **Catalog:** NP-2278 (1 features)
- **Hints:**
  - `AiPrivateDataReader` in `src/Nodus/Photon.Nodus.Core/Formats/Ai/`: locate `AIPrivateData` streams in the PDF, inflate (zlib) and concatenate, then tokenize the AI PostScript-like operators.
  - `AiPostScriptInterpreter`: the operator subset in the AI File Format spec v7 (path `m l c v y`, paint `f F s S b B`, `u U` groups, `Lb LB` layers, `Xa XA` colors, `Bd Bm` gradients, `To TO Tp TP` text, `Ln` layer names), producing the same model as §3.
  - When private data is present it wins over the PDF layer path, keeping live text, swatches, and symbols; unknown operators are counted in the conversion report, never dropped silently.
  - Legacy files (AI 3 to 8 PostScript) open through the same interpreter; the window title and default save name append " [Converted]" when `Nodus.Formats.Ai.AppendConvertedOnLegacy` is on (default on).
  - AICB clipboard read: a registered clipboard format parsed by the same interpreter so paste from other vector editors keeps paths.
  - Fixtures `tests/fixtures/nodus/ai/private-data/` and `ai/legacy/`: files saved by Illustrator 30.8 (current and AI 8 and AI 3 formats), goldens from Inkscape with poppler for PDF-based files and from Inkscape's PostScript import through Ghostscript for legacy files, versions recorded.
  - Tests: `AiPrivateDataTests` assert layer names, live text strings, and swatch names; `AiLegacyTests` assert geometry against goldens.
- **Proof:** Format fidelity: a fixture with live text imports it as editable text through private data where the §3 path gives curves (asserted), and legacy fixtures match their goldens; the cheaper substitute that fails is falling back to §3 for every file, which the live-text assertion catches.

#### §5. Illustrator .ai export

- **Deliverable:** Save PDF-based `.ai` (layers as OCGs, artboards as pages, AIPrivateData for Nodus-only data it can express) with the Illustrator options, a legacy EPS-based AI 8 writer, the Corel-side export options, and AICB and PDF on the clipboard.
- **Depends On:** D02 T13 §14
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/ai-export/ | Job: a designer hands a file to an Illustrator user who can edit it | Treatment: an Illustrator Options dialog (version, range, PDF compatibility, embed ICC, compression, save each artboard, text as text or curves, conversion and transparency options) with a data-loss report; the cheaper substitute that fails is renaming a PDF to .ai | Chrome: consume the D02 T13 §14 PDF writer, the D02 T06 §14 export dialog shell, and the settings store; do not add a second PDF writer.
- **Runs:** Requires: display-session -- the options dialog and the report need an interactive desktop
- **Catalog:** NP-2279 to NP-2284 (6 features)
- **Hints:**
  - `AiWriter` in `src/Nodus/Photon.Nodus.Core/Formats/Ai/` wraps the D02 T13 §14 `PdfWriter`: pages per artboard, OCG per layer, `/Illustrator` piece info, and an `AIPrivateData` stream written by `AiPrivateDataWriter` for paths, groups, layers, and text.
  - Options (`Nodus.Formats.Ai.Export.*`): version (CC, CS6, legacy AI 8), range (document, artboards, selection), Create PDF Compatible File, Embed ICC, Use Compression, Save Each Artboard Separately, text as text or curves, outlines to objects, simulate complex fills, spot to CMYK, include preview, include placed images or link them.
  - Legacy AI 8 writer (`AiLegacyWriter`) emits EPS-based AI with a transparency choice: rasterize transparent areas (through `D02 T12 §1`) or drop transparency, with a report line per object.
  - Conical and square gradients, which AI 8 cannot express, write as up to 256 filled bands (step count from the gradient's steps setting).
  - Live features Illustrator lacks expand through `D02 T07 §1` fallbacks; the export report lists each expansion.
  - Clipboard write: AICB and PDF flavors next to SVG for paste into other editors and Imago, controlled by §19's clipboard settings.
  - Log `Exported AI {Path} v{Version} ({Artboards} artboards, {Expanded} expanded)`.
  - Fixtures `tests/fixtures/nodus/ai/export/`: a multi-artboard, multi-layer document with spot colors and text; read-back through §3 and §4 and through Inkscape with poppler as goldens.
  - Tests: `AiExportRoundTripTests` (Nodus read-back equals the source model within 1e-3 pt) and `AiLegacyExportTests` (band count, transparency modes).
- **Proof:** Format fidelity: the exported `.ai` re-imports through §4 with the same layers, artboards, and live text, and Inkscape with poppler renders it within tolerance of Nodus's own render; the interoperability risk with Illustrator itself is recorded; the cheaper substitute that fails is a PDF with an `.ai` extension, which the private-data read-back catches.

#### §6. CorelDRAW import: containers, pages, layers, and objects

- **Deliverable:** An own managed CDR reader (libcdr MPL-2.0 as reference, Inkscape with libcdr as the golden oracle) for RIFF CDR v7 to X3, X4+ ZIP containers, CDX, and CDT, with pages, master layers, layers, groups, and basic shapes, and the open and import options.
- **Depends On:** D02 T07 §5
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/cdr-import/ | Job: a CorelDRAW user moving to Nodus opens their drawings with pages and layers intact | Treatment: a CDR Import dialog with maintain layers and pages and a code page list, shown only when the file needs it; the cheaper substitute that fails is asking users to convert through Inkscape | Chrome: consume the settings store and the D02 T07 §3 and §5 page and layer models; do not add a native libcdr dependency.
- **Runs:** Requires: display-session -- the options dialog needs an interactive desktop
- **Catalog:** NP-2285 to NP-2289 (5 features)
- **Hints:**
  - `CdrReader` in `src/Nodus/Photon.Nodus.Core/Formats/Cdr/`: RIFF chunk walker (`CDR7` to `CDRD`), `System.IO.Compression.ZipArchive` for X4+ containers (`content/riffData.cdr` plus `data/`), the `cmpr` compressed-list inflater, and CDX handling; any file translated from libcdr keeps its MPL-2.0 header (recorded in `docs/dev/decisions.md`).
  - Object records: pages, master layers (all, odd, even), layers (visible, printable, locked, export flag), groups, curves, rectangles with corners, ellipses and arcs, polygons and stars, transforms, and object names.
  - Options `Nodus.Formats.Cdr.Import.*`: maintain layers and pages (off merges into one layer), code page (auto from the file, else a list from `Encoding.GetEncodings()` with `CodePagesEncodingProvider` registered).
  - Open makes a document; Import places a group on the current page; CDT opens as a new untitled document.
  - A password-protected or newer-than-known version file is refused by name with the version found.
  - Unknown records are counted in the conversion report and kept in a `nodus:cdr-unknown` note, never silently dropped.
  - Budget: a 10,000-object CDR opens in under five seconds with progress and Cancel.
  - Fixtures `tests/fixtures/nodus/cdr/`: files per version family (v7 to X3 RIFF, X4 to 2026 ZIP, CDX, CDT), authored or obtained with redistribution rights stated in the README, goldens from Inkscape 1.4 with libcdr (version recorded).
  - Tests: `CdrContainerTests` (version detection, pages, layers) and `CdrObjectFidelityTests` (render versus golden).
- **Proof:** Format fidelity: every fixture opens with the golden's page count, layer names, and object count, and renders within the stated tolerance of the Inkscape with libcdr golden; the cheaper substitute that fails is importing only the embedded preview thumbnail, which the object-count assertion catches.

#### §7. CorelDRAW import: fills, outlines, text, effects, and bitmaps; CMX

- **Deliverable:** The CDR reader gains fills, outlines, artistic and paragraph text, effects as live objects or expanded, embedded bitmaps, and Painterly brushstrokes with their fallback, plus the CMX reader.
- **Depends On:** §6, D02 T11 §1, D02 T10 §2
- **Phase:** 11
- **Surface:** no surface of its own (reuses the §6 dialog)
- **Runs:** none
- **Catalog:** NP-2290 (1 features)
- **Hints:**
  - `CdrFillReader`: uniform, fountain (linear, radial, conical, square with steps), two-color, full-color and bitmap patterns, texture (as its stored bitmap), PostScript fill (as a named placeholder pattern with a report line), and mesh.
  - `CdrOutlineReader`: width, color, dashes, caps and joins, arrowheads, calligraphic nib, behind fill, scale with object.
  - `CdrTextReader`: artistic and paragraph text with styles and frames into the `D02 T10 §2` model, fonts matched by name with substitution reported.
  - Effects (blend, contour, envelope, extrude, drop shadow, lens, PowerClip, perspective, distortion) map to the `D02 T11 §1` live effects where Nodus has one, else to the stored expanded geometry with a report line.
  - Embedded bitmaps decode through §12's codecs; Painterly brushstroke objects read as their pre-25 fallback bitmap with transparency, kept as a bitmap object.
  - `CmxReader` in `Formats/Cdr/`: CMX v5 to X6 (16- and 32-bit variants) through the same object model.
  - Corel DESIGNER files that share the CDR container are read where compatible; others are refused by name.
  - Fixtures extend `tests/fixtures/nodus/cdr/` with one file per fill, outline, text, and effect family plus CMX files; goldens from Inkscape with libcdr (CMX via libcdr's CMX import), versions recorded.
  - Tests: `CdrStyleFidelityTests`, `CdrEffectMappingTests` (live versus expanded per effect), `CmxReaderTests`.
- **Proof:** Format fidelity: each style and effect fixture renders within tolerance of its Inkscape with libcdr golden and the live-effect fixtures reopen as live objects (asserted by type); the cheaper substitute that fails is expanding every effect, which the live-type assertion catches.

#### §8. CorelDRAW CDR and CMX export

- **Deliverable:** Write CDR in the RIFF layout libcdr reads and CMX, with save-to-version, keep appearance or editable, advanced save, reference info, and the save-version settings, proven by read-back through Nodus and through Inkscape with libcdr.
- **Depends On:** §7
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/cdr-export/ | Job: a designer returns a file to a CorelDRAW user | Treatment: a CDR Save Options dialog (version, keep appearance or keep editable, advanced compression and rebuild options, save CMX alongside, reference info) and an ask-on-earlier-version prompt; the cheaper substitute that fails is exporting SVG and telling the recipient to import it | Chrome: consume the settings store and the D02 T06 §14 export dialog shell.
- **Runs:** Requires: display-session -- the options dialog and prompt need an interactive desktop
- **Catalog:** NP-2291 to NP-2298 (8 features)
- **Hints:**
  - `CdrWriter` in `src/Nodus/Photon.Nodus.Core/Formats/Cdr/`: RIFF writer for the earliest version libcdr reads fully (recorded after spiking), pages, layers, groups, curves, fills, outlines, text, bitmaps.
  - Save to an earlier version: keep appearance expands features the version lacks (brushstrokes to bitmaps, live effects to curves) or keep editable writes the nearest editable form; the choice is per save.
  - Advanced save options: compress bitmap effects, compress vector objects, store or rebuild texture fills, store or rebuild blends and extrusions, save CMX alongside.
  - Reference info (title, subject, keywords, rating) writes to the CDR `INFO` records and reads back through §6.
  - Settings `Nodus.Formats.Cdr.Export.DefaultVersion` and `Nodus.Formats.Cdr.Export.AskOnEarlierVersion` (default on) with their consumers in the save flow.
  - `CmxWriter`: CMX 32-bit with RGB, CMYK, and named spot colors (no PANTONE data bundled).
  - Interoperability risk with CorelDRAW itself recorded in the section and the user guide; no CorelDRAW-authored golden is claimed.
  - Log `Exported CDR {Path} v{Version} ({Mode})`.
  - Tests: `CdrWriteReadBackTests` (Nodus read-back equals the source model) and `CdrLibcdrReadBackTests` (Inkscape with libcdr imports the written file and renders within tolerance, marked with the Inkscape version).
- **Proof:** Format fidelity: every export fixture reads back through §6 and §7 to the same model and renders through Inkscape with libcdr within tolerance; the cheaper substitute that fails is a writer tested only by Nodus's own reader, which a symmetric bug passes.

#### §9. EPS and PostScript import and export

- **Deliverable:** EPS import (Illustrator EPS through the AI parser, other EPS and PS/PRN through a user-installed Ghostscript run as an external process and refused by name when absent, or placed with its preview) and an own EPS writer with general and advanced options.
- **Depends On:** §3, D02 T13 §10
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/eps/ | Job: a print shop's EPS logo opens as editable art and a designer sends EPS to a legacy RIP | Treatment: an EPS Import dialog (editable or placed with preview, text as text or curves) and an EPS Export dialog with General and Advanced tabs, plus a Ghostscript location setting that says when it is absent; the cheaper substitute that fails is bundling Ghostscript | Chrome: consume the D02 T13 §10 PostScript emitter, the settings store, and `Photon.UI` dialogs.
- **Runs:** Requires: display-session -- the dialogs need an interactive desktop; Needs: Ghostscript 10.x installed for the PostScript fixtures, skipped by name otherwise
- **Catalog:** NP-2299 to NP-2303 (5 features)
- **Hints:**
  - `EpsReader` in `src/Nodus/Photon.Nodus.Core/Formats/Eps/`: DOS EPS binary header (TIFF or WMF preview), `%%BoundingBox`, and `%%Creator: Adobe Illustrator` detection routing to the §4 interpreter.
  - `GhostscriptBridge` in `Formats/Eps/`: finds `gswin64c.exe` from `Nodus.Formats.Ghostscript.Path` or the registry, runs it as an external process with `-dSAFER -sDEVICE=pdfwrite`, then imports the PDF through §2; never bundled (AGPL-3.0, recorded), refused by name when absent.
  - PS and PRN multi-page files import as pages or groups; text as text or curves.
  - Place EPS keeps the file linked with its preview (through `D02 T12 §7`) and prints the original PostScript through `D02 T13 §10`.
  - `EpsWriter`: own writer on the D02 T13 §10 PostScript emitter; general options: color output (Native, RGB, CMYK, Gray), convert spots, preview (None, TIFF 8-bit, TIFF 1-bit, transparent), text as curves, include fonts, PostScript level 2 or 3, transparency flattening.
  - Advanced options: bounding box (objects, page, bleed, crop marks), JPEG bitmap compression, preserve overprints and overprint black, auto-increase fountain steps; OPI links recorded as not written.
  - Settings `Nodus.Formats.Eps.*` with defaults; Illustrator EPS version choice writes the §5 legacy header.
  - Fixtures `tests/fixtures/nodus/eps/`: Illustrator EPS, a generic EPS, a two-page PS, with goldens from Ghostscript 10.x `png16m` renders (version recorded).
  - Tests: `EpsImportTests`, `EpsWriterTests` (re-rendered by Ghostscript and compared), `GhostscriptBridgeTests` (absent path refuses with the named message).
- **Proof:** Format fidelity: EPS written by Nodus renders through Ghostscript within tolerance of Nodus's own render, and each import fixture matches its Ghostscript golden; with Ghostscript absent the import refuses with the named message (asserted); the cheaper substitute that fails is importing only the TIFF preview, which the vector-count assertion catches.

#### §10. DXF and DWG import and export

- **Deliverable:** DXF and DWG read and write through ACadSharp (MIT) with import options (layout, scale, units, lineweights, layers) and export options (version, units, scaling, text, bitmaps, blocks), and dimensions as live dimension objects.
- **Depends On:** D02 T08 §15
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/cad/ | Job: an engineer's drawing opens at true scale with layers and dimensions, and a cut path goes back to CAD | Treatment: a CAD Import dialog (layout, scale, units, scale lineweights, center or fit to artboard, merge layers, auto-reduce nodes) and a CAD Export dialog (version, units, scale, text as curves, bitmap format, unmapped fill color, group as block); the cheaper substitute that fails is DXF R12 only | Chrome: consume the settings store and the D02 T08 §15 dimension model.
- **Runs:** Requires: display-session -- the dialogs need an interactive desktop
- **Catalog:** NP-2304 to NP-2305 (2 features)
- **Hints:**
  - Add ACadSharp (MIT) with its `docs/dev/decisions.md` row.
  - `CadReader` in `src/Nodus/Photon.Nodus.Core/Formats/Cad/`: lines, polylines (bulges to arcs), circles, arcs, ellipses, splines to Beziers, hatches to fills, text and mtext, inserts to symbols, layers with color and linetype, lineweights, model or a paper layout, and 3D entities projected to the XY view.
  - Dimensions (linear, aligned, angular, radial) become `D02 T08 §15` dimension objects keeping associativity where the source has it.
  - Units from `$INSUNITS` with the scale option (Automatic, English, Metric, custom ratio); scale lineweights on or off.
  - `CadWriter`: versions R12 to 2018 as ACadSharp supports, outlines only, text as text or curves, bitmaps embedded as a chosen raster format or dropped, unmapped fills as color or unfilled, groups as blocks, selected art only.
  - Settings `Nodus.Formats.Cad.Import.*` and `Nodus.Formats.Cad.Export.*`.
  - Fixtures `tests/fixtures/nodus/cad/`: DXF and DWG per version family with dimensions, hatches, blocks, and layouts; DXF goldens rendered by LibreCAD 2.2 (GPL-2.0, run as a tool, never bundled; version recorded); DWG proven by ACadSharp round trips since ODA tools' license does not allow redistribution of their output tooling in CI.
  - Tests: `CadImportFidelityTests`, `CadExportRoundTripTests` (write, read back through ACadSharp, compare entity counts and geometry within 1e-6 drawing units), `CadDimensionMappingTests`.
- **Proof:** Format fidelity: DXF fixtures render within tolerance of the LibreCAD golden, DWG and DXF exports round-trip through ACadSharp with identical entity counts and geometry, and dimension fixtures reopen as live dimensions; the cheaper substitute that fails is exploding dimensions to lines, which the type assertion catches.

#### §11. EMF, WMF, CGM, HPGL, and WPG

- **Deliverable:** Own readers and writers for EMF, WMF, CGM, HPGL PLT, and WPG, each with its options and a fidelity proof.
- **Depends On:** D02 T07 §3
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/metafiles/ | Job: clip art, plotter, and cutter files open, and outlines go to a plotter or cutter | Treatment: one small options dialog per format that has options (HPGL import pen mapping, HPGL export pens and origin, CGM version and encoding, WPG version and colors) and none for EMF and WMF; the cheaper substitute that fails is rasterizing metafiles through WPF | Chrome: consume the D02 T06 §14 export dialog shell and the settings store.
- **Runs:** Requires: display-session -- the options dialogs need an interactive desktop
- **Catalog:** NP-2306 to NP-2310 (5 features)
- **Hints:**
  - `EmfReader` and `WmfReader` in `src/Nodus/Photon.Nodus.Core/Formats/Metafile/` from [MS-EMF] and [MS-WMF]: the drawing-record subset (paths, polys, beziers, brushes, pens, text, bitmaps, clipping, world transform), EMF+ records rendered through their EMF fallback with a report line.
  - `EmfWriter` and `WmfWriter` (placeable WMF header); text kept as text, hairlines for thin strokes; EMF is also the §14 Office editing target and a §19 clipboard flavor.
  - `CgmReader` and `CgmWriter`: ISO 8632 binary and clear-text encodings, versions 1, 3, 4, WebCGM 1.0 profile on write.
  - `HpglReader`: HP-GL and HP-GL/2 (PU, PD, PA, PR, AA, CI, SP, LT, PW, VS), scale, curve resolution, 256 pens to colors, widths, and velocity, pen library reset.
  - `HpglWriter`: outlines only, curves flattened to segments at a tolerance, pen table, plotter origin including top left.
  - `WpgReader` and `WpgWriter`: WPG 1.0 and 2.0, 16 or 256 colors, text as text or curves.
  - Settings `Nodus.Formats.<Emf|Wmf|Cgm|Hpgl|Wpg>.*`.
  - Fixtures `tests/fixtures/nodus/metafile/`: EMF, WMF, CGM, PLT, WPG files; goldens from Inkscape 1.4 (EMF, WMF via libUEMF, WPG via libwpg, HPGL export as the writer oracle) and LibreOffice 25.x `soffice --convert-to png` for CGM, versions recorded.
  - Tests: `MetafileFidelityTests` per reader, `MetafileWriterRoundTripTests` per writer (Nodus read-back and the reference import).
- **Proof:** Format fidelity: each reader fixture renders within tolerance of its named golden and each writer's output re-imports through the reference implementation within tolerance; the cheaper substitute that fails is a writer proven only by Nodus's own reader.

#### §12. Raster formats: import and export through WIC

- **Deliverable:** Raster place, open, and export through WIC for BMP, GIF, JPEG, PNG, TIFF, WebP, ICO and CUR, AVIF and HEIF (extension-gated), own TGA and PCX codecs, a recorded JPEG 2000 codec decision, and the import (resample, crop, page and frame selection, combine layers, watermark check) and export (compression, notes, hidden layers) options.
- **Depends On:** D02 T06 §14
- **Phase:** 11
- **Surface:** UI: Fidelity: docs/captures/nodus/export-raster/ (from `D02 T04 §3`), extended, plus new build, no baseline; captured to docs/captures/nodus/raster-import/ | Job: any common image places at the right size and any page exports to the raster format a client asks for | Treatment: Import button split menu (Import, Resample and load, Crop and load) with a crop preview, TIFF page and GIF frame pickers, and per-format export options pages in the one export dialog; the cheaper substitute that fails is one generic PNG-only path | Chrome: consume the D02 T04 §3 `RasterExporter`, the D02 T06 §14 dialog, and `D02 T12 §1` bitmap objects; do not add a second raster pipeline.
- **Runs:** Requires: display-session -- the dialogs and crop preview need an interactive desktop
- **Catalog:** NP-2311 to NP-2331 (21 features)
- **Hints:**
  - `WicCodec` in `src/Nodus/Photon.Nodus.Desktop/Formats/Raster/` over WPF `BitmapDecoder` and `BitmapEncoder` (BMP, GIF, JPEG, PNG, TIFF, ICO, WMP), and WebP through SkiaSharp; decoded frames become `D02 T12 §1` bitmap objects.
  - AVIF and HEIF through the WIC Store extensions, probed at startup; absent extensions are refused by name with the Store link text, never a crash.
  - Own codecs in `src/Nodus/Photon.Nodus.Core/Formats/Raster/`: `TgaCodec` (8-bit gray to 32-bit, RLE, Normal or Enhanced) and `PcxCodec` (2.5 to 3.0, RLE, paletted via `D01 T03 §3`); OS/2 BMP v1.3 and v2.0 read by an own header shim where WIC declines.
  - JPEG 2000: WIC has no JP2 codec; record the choice between CoreJ2K (BSD, managed) and OpenJPEG (BSD-2, native P/Invoke) in `docs/dev/decisions.md`, else JP2 is refused by name.
  - Import options: TIFF page selection, multi-frame load partial file (frame range), combine multi-layer bitmap, resample and load (width, height, percent, resolution, maintain aspect), crop and load (numeric and handles), JPEG EXIF orientation and CMYK through `D01 T04 §1`.
  - Check for watermark reads EXIF, IPTC, and XMP copyright fields and shows them on import (no proprietary watermark detection, recorded).
  - Export options per format (color mode, resolution, anti-alias, transparency, compression type, byte order, embed ICC, JP2 quality and progression) plus export notes written to metadata; hidden layers export unless the `D02 T07 §5` export flag is off.
  - Settings `Nodus.Formats.Raster.<Format>.*`.
  - Budget: a 100-megapixel TIFF places in under three seconds with progress and Cancel.
  - Fixtures `tests/fixtures/nodus/raster/`: one file per format and variant (paletted, 16-bit, CMYK JPEG, multi-page TIFF, animated GIF, OS/2 BMP, RLE TGA, PCX), decode goldens from ImageMagick 7 (`magick x.ext rgba:`) with version recorded.
  - Tests: `RasterDecodeFidelityTests` (pixel-exact or within 1/255 for lossless, PSNR stated for lossy), `RasterEncodeRoundTripTests`, `RasterImportOptionsTests`.
- **Proof:** Format fidelity: every decode fixture matches its ImageMagick golden within the stated tolerance and every writer's output decodes in ImageMagick to the source pixels; the cheaper substitute that fails is testing only PNG, which leaves TGA and PCX unproven.

#### §13. Photoshop PSD import and export

- **Deliverable:** An own PSD reader and writer against Adobe's published specification: import with layers to objects or flattened, comps, hidden layers, blend modes, and spot channels; linked PSD placement; export flat or layered; and path and pixel exchange through the clipboard.
- **Depends On:** §12
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/psd/ | Job: a Photoshop or Imago composition arrives as editable layers and a vector drawing goes back layered | Treatment: a PSD Import dialog (layer comp, layers to objects or flatten, import hidden layers, import slices) and PSD export options in the one export dialog; the cheaper substitute that fails is reading the composite image only | Chrome: consume §12's bitmap path, the D02 T12 §7 Links panel for linked PSD, and the settings store.
- **Runs:** Requires: display-session -- the dialog needs an interactive desktop
- **Catalog:** NP-2332 to NP-2335 (4 features)
- **Hints:**
  - `PsdReader` in `src/Nodus/Photon.Nodus.Core/Formats/Psd/`: header, color modes (bitmap, gray, indexed, RGB 8 and 16, CMYK, Lab, duotone), layer and mask info, RLE and raw channels, layer groups, masks, opacity, blend modes mapped to Nodus blend modes, layer comps, slices, spot channels as `D01 T04 §3` DeviceN bitmaps.
  - Layers become bitmap objects in groups; text layers import as rasters with their string kept in object notes; shape layers import their vector masks as paths.
  - Place linked PSD keeps the link and the chosen comp through `D02 T12 §7`; comps switch from the placed object's properties.
  - `PsdWriter`: flat or layered, color model, resolution, anti-alias, embed ICC, spot channels kept, text rasterized, maximum compatibility composite always written.
  - Clipboard exchange: paths as SVG and AICB flavors (§19), pixels as PNG and DIB; Imago is the first partner.
  - Settings `Nodus.Formats.Psd.*`.
  - Fixtures `tests/fixtures/nodus/psd/`: layered RGB, CMYK, 16-bit, duotone, with comps and masks; goldens are psd-tools (MIT) layer dumps and GIMP 3.0 composites, versions recorded.
  - Tests: `PsdReaderTests` (layer tree, names, blend modes, pixels), `PsdWriterReadBackTests` (Nodus read-back and psd-tools and GIMP read-back).
- **Proof:** Format fidelity: each fixture's layer tree equals the psd-tools dump and its composite matches the GIMP golden within tolerance, and written PSDs open in GIMP with the same layer count; the cheaper substitute that fails is the flattened composite, which the layer-tree assertion catches.

#### §14. Office and text documents, Export For Office, and font export

- **Deliverable:** Import TXT, RTF, DOC, DOCX, XLS, XLSX, and CSV; export text as TXT, RTF, and DOC; the Export For Office dialog (PNG, EMF, WPG targets, optimization, flattening); office copy and insert routes; and TrueType and Type 1 glyph export.
- **Depends On:** D02 T10 §13, D02 T10 §14
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/export-for-office/ | Job: a designer puts artwork into a Word or PowerPoint file and pulls a client's copy deck into a layout | Treatment: an Export For Office dialog (target: compatibility PNG, editing EMF, WordPerfect WPG; optimized for presentation 96, desktop 150, commercial 300 dpi; preview with zoom, pan, and estimated size); the cheaper substitute that fails is a plain PNG export | Chrome: consume §11's EMF and WPG writers, §12's PNG path, the D02 T10 §13 text import dialog, and `Photon.UI` preview controls.
- **Runs:** Requires: display-session -- the dialog and preview need an interactive desktop
- **Catalog:** NP-2336 to NP-2350 (15 features)
- **Hints:**
  - Add DocumentFormat.OpenXml (MIT) and NPOI (Apache-2.0) with `docs/dev/decisions.md` rows.
  - `OfficeTextReader` in `src/Nodus/Photon.Nodus.Core/Formats/Office/`: DOCX through OpenXml, DOC through NPOI HWPF, RTF by an own parser, TXT with encoding detection, into the `D02 T10 §13` importing-text flow (keep fonts and formatting or plain).
  - `SpreadsheetReader`: XLS and XLSX through NPOI, CSV own, into `D02 T10 §14` tables; linked workbooks stay linked through `D02 T12 §7`.
  - Text export: TXT (all text objects in reading order), RTF own writer, DOC through NPOI (Word 97 binary; Word 6/7 recorded as not written).
  - `ExportForOfficeDialog`: targets PNG (§12), EMF (§11), WPG (§11); layers flattened; estimated size from a trial encode.
  - Office copy: the clipboard carries EMF and PNG flavors (§19) so Word and PowerPoint paste editable or faithful art; Insert into office documents is by file or clipboard, and an OLE server is recorded as not built.
  - `GlyphExporter`: a combined curve exported as one unhinted glyph in a TTF (own `glyf`, `cmap`, `hmtx` writer) or a Type 1 PFB (own charstring encoder), fills and outlines ignored, with character code, advance, and family name.
  - The Office Compatibility Pack warning becomes a missing-reader warning with `Nodus.Formats.Office.WarnOnRefused` (re-enabled from settings).
  - VSDX and PPTX import are named in the scope with no catalog row; record them through `add-todo` rather than build them here.
  - Fixtures `tests/fixtures/nodus/office/`: DOCX, DOC, RTF, XLS, XLSX, CSV with text and table goldens from LibreOffice 25.x `--convert-to txt` and `csv`, and glyph fixtures checked with fontTools `ttx` dumps (versions recorded).
  - Tests: `OfficeImportTests`, `ExportForOfficeTests`, `GlyphExportTests` (the TTF loads in `GlyphTypeface` and its outline matches the source curve within 1 font unit).
- **Proof:** Format fidelity: each office fixture imports with text runs and table cells equal to the LibreOffice golden, Export For Office writes the target format at the chosen resolution (dimensions asserted), and exported glyphs round-trip through fontTools; the cheaper substitute that fails is plain-text import, which the formatting-run assertion catches.

#### §15. Export for Screens, asset export, and the export list

- **Deliverable:** Export As with artboards, pages, and range; the Export for Screens dialog (artboards and assets tabs, formats, scales and suffixes, presets, sub-folders); the export list panel with per-item format, destination, and settings bound to objects; and background export with progress.
- **Depends On:** D02 T06 §14, D02 T07 §3
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/export-for-screens/ and docs/captures/nodus/export-list/ | Job: a UI designer exports every artboard and icon at 1x, 2x, and 3x in PNG, SVG, and WebP in one action, and re-exports after edits | Treatment: Export for Screens dialog with Artboards and Assets tabs and a format-scale grid, plus a dockable Export panel listing pages and objects with checkboxes, rename, suffix, format, destination, and settings; the cheaper substitute that fails is repeating Export As per file | Chrome: consume the D02 T06 §14 export dialog and writers, the D02 T07 §3 artboard model, the settings store, and `Photon.UI` panels and progress; do not duplicate the per-format options pages.
- **Runs:** Requires: display-session -- the dialog, panel, and background export need an interactive desktop
- **Catalog:** NP-2407 to NP-2437 (31 features)
- **Hints:**
  - Group A, Export As: `ExportAsCommand` with use artboards or pages, range text (`1-3, 5`), this page only, each page to its own file, selected only, crop to page, and skip the options dialog; settings `Nodus.Export.As.*`.
  - Group B, export items: `ExportItem` (target: page, artboard, object, or selection; name; suffix; format; destination; per-format settings) in `src/Nodus/Photon.Nodus.Core/Export/`, persisted in the document as `nodus:export-item` elements per `D02 T07 §1` and removed when their object is deleted.
  - `ExportListService`: add selection (one item per object), add current page, add all pages (separate pages and a page range), remove, duplicate, add new assets with an item's settings, select all, default format for new items (`Nodus.Export.List.DefaultFormat`), ordering pages first in document order then objects in Objects panel order.
  - `ExportPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/`: inline rename and suffix, format and destination pickers, settings button opening the format page, Export checked or all; Layers panel "Collect for Export" and the artboard context menu "Export Selected Artboards" feed it.
  - Group C, Export for Screens: `ExportForScreensDialog` with Artboards tab (all, range, full document, include bleed) and Assets tab (the list), formats PNG, PNG-8, JPG 100/80/50/20, SVG, PDF, WebP, TIFF, scales 0.5x to 4x or width, height, or resolution with suffixes, iOS and Android presets, sub-folders per scale or format, open location after export.
  - Bitmap bounds are outline-aware (centered and outside strokes and partial pixels included; inside strokes keep size), shared with §16.
  - Duplicate a page into a new document through `D02 T07 §3` and the document window service.
  - `BackgroundExportQueue`: runs PNG and JPEG (and all formats when `Nodus.Export.Background` is on) off the UI thread with a progress strip, Cancel, and a completion toast; no partial file is left on cancel.
  - Log one line per exported file and one summary line per batch.
  - The recommended import and export formats guide is a user guide page listing which Nodus format to use per destination application.
  - Budget: 100 artboards at three scales and three formats export in under a minute on the reference machine.
  - Tests: `ExportListServiceTests` (add, remove, duplicate, ordering, object-bound removal, undo), `ExportForScreensTests` (file names, scales, sub-folders), `OutlineAwareBoundsTests`, `BackgroundExportCancelTests`.
- **Proof:** Driven plus unit: a driven Export for Screens run of a three-artboard fixture writes exactly the expected file set (names, dimensions from headers, quoted) and the unit tests pass; the cheaper substitute that fails is exporting only the first artboard at 1x, which the file-set assertion catches.

#### §16. Export for Web: optimized preview and web formats

- **Deliverable:** The Export for Web dialog for GIF, PNG-8, PNG-24, JPEG, and WebP with 1, 2, or 4 comparison previews, presets, size and download estimates, palette, dither, transparency, matte, resize, color mode and profile, and make text web-compatible.
- **Depends On:** §12
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/export-for-web/ | Job: a web designer compares encodings side by side and ships the smallest file that looks right | Treatment: a dialog with preview layouts (one, two vertical, two horizontal, four), zoom 1:1 and fit, pan, per-pane format settings, color table, size and download estimate, presets, and preview in browser; the cheaper substitute that fails is the plain export dialog with a quality slider | Chrome: consume §12's encoders, `D01 T03 §3` quantization and dithering, and `Photon.UI` zoom and pan controls.
- **Runs:** Requires: display-session -- the preview dialog needs an interactive desktop
- **Catalog:** NP-2438 to NP-2450 (13 features)
- **Hints:**
  - `ExportForWebDialog` and view model in `src/Nodus/Photon.Nodus.Desktop/Views/Export/`: pane layouts, shared zoom and pan, per-pane encoder settings, re-encode debounced and cancellable.
  - `WebEncoderSettings`: GIF and PNG-8 (palette algorithm, colors, dither type and amount, web snap, lossy, transparency, transparent sampled color, matte, interlace), JPEG (quality, optimized, progressive, blur, matte, embed ICC), PNG-24 and WebP (quality, lossless, alpha).
  - Palette editing in the color table: load, sample, add, edit, delete, lock colors, through `D01 T03 §3`.
  - Encoders: GIF and PNG through §12's WIC path, paletted PNG with `BitmapPalette`, WebP through SkiaSharp; progressive JPEG needs an encoder WIC lacks, so record the decision (a small own progressive encoder or refused by name).
  - Transformation: resize by units, width, height, percent, resolution with aspect lock; crop to page; anti-aliased on or off; color mode and embedded profile through `D01 T04 §1`.
  - Estimates: file size from the actual encode and download time at `Nodus.Export.Web.ConnectionSpeed`.
  - Presets: apply, save, load, delete, stored in the settings store (`Nodus.Export.Web.Presets`).
  - Preview in browser writes a temporary HTML page and opens it with the default browser.
  - Make text web-compatible marks paragraph text for HTML output (`nodus:web-text`), used by §17's HTML writer.
  - Tests: `WebEncoderTests` (palette size, transparency index, matte blend, quality versus size monotonic), `ExportForWebPresetTests`, `WebEstimateTests`.
- **Proof:** Format fidelity plus driven: each encoder's output decodes in ImageMagick 7 to the expected palette size and pixels within the stated tolerance, and a driven four-up capture is committed; the cheaper substitute that fails is a single preview pane, which the driven capture shows.

#### §17. Slices, image maps, hyperlinks, rollovers, and SVG interactivity

- **Deliverable:** Slices (tools, commands, options, display, save selected slices), image maps, hyperlinks and bookmarks, rollovers with states and live preview, the Links and Rollovers panel, and the SVG Interactivity panel, carried through SVG, HTML, and PDF output.
- **Depends On:** §1
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/slices/ and docs/captures/nodus/links-rollovers/ | Job: a designer cuts a page into web slices, links objects, and makes hover states without hand-writing HTML | Treatment: Slice and Slice Selection tools with numbered overlays, Object Slice menu, Slice Options dialog, a Links and Rollovers panel (links, bookmarks, hotspot, alt text, rollover states), and an SVG Interactivity panel; the cheaper substitute that fails is a URL field on the object properties only | Chrome: consume the shared icon catalog, the tool registration, the settings store, the suite history, and `Photon.UI` panels.
- **Runs:** Requires: display-session -- tools, overlays, panels, and live preview need an interactive desktop
- **Catalog:** NP-2451 to NP-2472 (22 features)
- **Hints:**
  - Group A, slices: `Slice` model in `src/Nodus/Photon.Nodus.Core/Web/` (user or object-based, type Image, No Image, HTML Text, name, URL, target, message, alt text, background) persisted as `nodus:slice` per `D02 T07 §1`.
  - `SliceTool` (Shift+K) and `SliceSelectionTool` in `Photon.Nodus.Core/Tools/`; commands make, release, create from guides, create from selection, duplicate, combine, divide, delete all, clip to artboard, show or hide, lock; each an undoable command.
  - Slice overlay draws numbers and lines in `Nodus.Slices.ShowNumbers` and `Nodus.Slices.LineColor`; Save Selected Slices writes each slice through §16's encoder settings plus an optional HTML table.
  - Group B, links: `Hyperlink` (http, https, ftp, mailto, file, bookmark) and `Bookmark` on objects and text runs (`D02 T10 §2` hyperlink field); hotspot by shape or bounding box; alt text; verify opens the link, delete removes it; hotspot crosshatch and background colors as settings.
  - Output: SVG `<a>` and `<title>` (§1), HTML image maps (`<map>` with rect or poly areas) with §16's images, and PDF link annotations and named destinations through the D02 T13 §14 writer.
  - Group C, rollovers: `Rollover` group with Normal, Over, and Down states; create, edit, finish editing, delete, duplicate, or extract a state, target frame; live preview toggles hover and press on the canvas; output to HTML with CSS `:hover` and `:active` and to SVG with CSS.
  - `LinksRolloversPanel` in `src/Nodus/Photon.Nodus.Desktop/Views/Panels/`.
  - Group D, SVG interactivity: `SvgInteractivityPanel` attaches event attributes (the SVG 1.1 event list) and links external JavaScript files; Nodus writes them to SVG and never executes them.
  - Tests: `SliceCommandTests` (each command and undo), `SliceExportTests` (file set and HTML table), `HyperlinkExportTests` (SVG, HTML map, PDF annotation read back through PdfPig), `RolloverExportTests`.
- **Proof:** Format fidelity plus driven: sliced and linked fixtures export to SVG, HTML, and PDF whose links read back (PdfPig for PDF, XML parse for SVG and HTML) with the same URLs and regions, and a driven rollover live-preview capture is committed; the cheaper substitute that fails is storing URLs without writing them, which the read-back catches.

#### §18. Pixel-perfect drawing, pixel preview, and object hinting

- **Deliverable:** A real pixel preview mode at document resolution, align to pixel grid per object and as the default for new art, the align command, object hinting, and the pixel-perfect workflow settings.
- **Depends On:** D02 T07 §12
- **Phase:** 11
- **Surface:** UI: Fidelity: docs/captures/nodus/main-window/ extended | Job: an icon designer draws crisp 16 px icons that export without blurry edges | Treatment: View, Pixel Preview (Alt+Ctrl+Y) rendering at 1 px per document unit scaled nearest-neighbour at every zoom, a pixel grid at 600 percent and above, Align to Pixel Grid in the Transform panel and Align panel, and Object Hinting in the Object menu; the cheaper substitute that fails is the existing flag that only activates at zoom 8 | Chrome: consume `SkiaRenderer`, the D02 T07 §12 view-mode switcher, the Align panel, and the settings store.
- **Runs:** Requires: display-session -- pixel preview and snapping need an interactive desktop
- **Catalog:** NP-2473 to NP-2477 (5 features)
- **Hints:**
  - `PixelPreviewRenderer` in `src/Nodus/Photon.Nodus.Desktop/Services/`: render the visible area at document resolution to an offscreen `SKSurface` (anti-aliased as export would) then draw it with nearest-neighbour sampling; replace the unused `pixelPreview` flag in `SkiaRenderer` and the zoom-8 gate in `SkiaCanvas`.
  - Pixel preview is a view mode in the D02 T07 §12 switcher, shared with the export preview of §15 and §16 so preview equals output.
  - `PixelAlign` per object (`nodus:pixel-align`) snaps horizontal and vertical segment edges and nodes to whole or half pixels by stroke width on create and transform; `Nodus.PixelGrid.AlignNewObjects` sets the default.
  - Align to Pixel Grid command realigns selected objects once (undoable); Select Objects Not Aligned to Pixel Grid lives beside it.
  - Object hinting marks an object so export snaps its edges to the pixel grid at render time without changing geometry.
  - Pixel-perfect workflow: pixel units, whole-number sizes in the Transform panel, pixel snapping, and a pixel-aligned page origin, enabled by the web and icon document presets.
  - Setting `Nodus.PixelPreview.AntiAliasBitmaps` controls bitmap smoothing in pixel preview.
  - Tests: `PixelAlignTests` (edges land on integers for 1 px strokes and half-integers for odd widths, rotation disables it), `PixelPreviewTests` (preview bitmap equals the §15 PNG export pixels exactly).
- **Proof:** Unit plus capture: the pixel preview of the icon fixture is pixel-identical to its 1x PNG export and aligned edges hold integer coordinates after move and scale, with a committed capture at 800 percent; the cheaper substitute that fails is a zoomed normal render, which the pixel-identity assertion catches.

#### §19. Clipboard formats, OLE objects, placing multiple files, and scanner acquire

- **Deliverable:** Multi-format clipboard exchange (SVG, PDF, AICB, EMF, bitmap) with its settings, the Import command with placement, search, filter, multiple files, original position, and snapping, the linked-object alternative to OLE, and WIA scanner and camera acquire.
- **Depends On:** D02 T06 §14
- **Phase:** 11
- **Surface:** UI: Fidelity: new build, no baseline; captured to docs/captures/nodus/import-place/ | Job: artwork moves between Nodus, Imago, office apps, and other editors by copy, paste, drag, place, and scan without losing vectors | Treatment: File, Import (Ctrl+I) with a search box, format filter, multi-select, and a place gun (click places at size, drag sizes, Enter centers, Space keeps original position, grid placement), plus Clipboard Handling settings and File, Acquire Image; the cheaper substitute that fails is single-file place with bitmap-only paste | Chrome: consume the D02 T06 §14 place path, `D02 T12 §7` linked files and Edit Original, the snapping engine, the settings store, and `Photon.UI` dialogs.
- **Runs:** Requires: display-session -- the clipboard, drag and drop, place gun, and WIA dialog need an interactive desktop; Needs: a WIA device or the WIA test device for the acquire test, skipped by name otherwise
- **Catalog:** NP-2351 to NP-2366 (16 features)
- **Hints:**
  - `ClipboardService` in `src/Nodus/Photon.Nodus.Desktop/Services/`: copy writes Nodus native SVG, `image/svg+xml`, PDF (D02 T13 §14), AICB (§5), EMF (§11), PNG and DIB; paste picks the richest known flavor in order Nodus, SVG, PDF, AICB (§4), EMF, bitmap, text.
  - Settings `Nodus.Clipboard.CopyAsPdf`, `CopyAsAicb` (preserve paths or appearance and overprints), `IncludeSvgCode`, `PasteTextWithoutFormatting`, each read by `ClipboardService`.
  - `ImportCommand` (Ctrl+I): format filter list and All formats, a search box over file name and metadata (title, subject, author, keywords, comments), multi-select, and skip the options dialog (`Nodus.Import.SkipOptionsDialog`).
  - `PlaceGun` tool state: cycles queued files with arrow keys, click places at original size, drag sizes, Enter centers on the page, Space places at the original position for CDR, AI, and PDF, grid placement by drag with arrow keys; active snapping applies while placing.
  - Format registry settings: enable, disable, and order import and export formats (`Nodus.Formats.Enabled`, `Nodus.Formats.Order`); all readers are built in, and the only optional pieces (Ghostscript, WIC extensions) are named where a format needs them.
  - Drag and drop from other apps accepts the same flavors as paste and files; each drop is one undoable command.
  - OLE decision recorded: no OLE container or server; Paste Link and Insert Object from file create a linked placed file through `D02 T12 §7`, and editing opens the source application with Edit Original and updates on file change.
  - `WiaAcquireService`: WIA 2.0 through the built-in `WIA.CommonDialog` COM automation for select source and acquire from scanners and cameras; TWAIN recorded as not supported.
  - Log `Imported {Count} files ({Formats})`, `Pasted {Flavor}`, and `Acquired image {Width}x{Height} from {Device}`.
  - Tests: `ClipboardFlavorTests` (every flavor round-trips to the same model within tolerance), `ImportCommandTests` (filter, search, multi-file queue, original position), `PlaceGunTests`, `WiaAcquireTests` (skipped by name with no device).
- **Proof:** Unit plus driven: copying a fixture and pasting it back through each flavor yields the same model within tolerance, and a driven multi-file import captures the place gun and the placed result; the cheaper substitute that fails is a bitmap-only clipboard, which the vector flavor assertions catch.

#### Sizing concerns

- §15 carries 31 catalog features across three surfaces (Export As options, the export list panel, and the Export for Screens dialog); grouped as in the hints it fits about 28 items, but it is the section most likely to overrun; a split point, if the author judges it necessary, is Export As plus Export for Screens versus the export list panel.
- §17 carries 22 features across slices, links, rollovers, and SVG interactivity; grouped in four blocks it fits about 26 items, with little slack.
- §12 carries 21 features across a dozen codecs; the hints group codecs by path (WIC, extension-gated, own codecs, JP2 decision) and options by import or export to stay near 25 items.
- §19 mixes clipboard, import dialog, place gun, OLE decision, and WIA; it fits about 24 items only because OLE is recorded as a decision rather than built.

### todo/02-nodus/TODO-15-nodus-ai.md -- `nodus-ai`

- **Title:** "TODO-15 -- Nodus AI: Editable, Suite-Aware, Reproducible"
- **Phase(s):** 12
- **Goal:** Nodus's AI is its own design, not a clone of Firefly or Corel AI, built on three pillars: every result is editable, structured output (the model returns JSON validated against a schema, applied as one named undoable command that creates real vector objects: named layers, document swatches, styles, and constraints; raster results are placed images, never flattened into artwork); it is suite-aware (the shared brand kit from `D01 T05 §5` constrains color and type, and the Lumen photo to Imago cleanup to Nodus trace pipeline works over files, offering a hand-off only when the other app is installed and refusing by name otherwise, with no runtime dependency); and it is explainable and reproducible (every action writes a provenance record with prompt, model, parameters, and seed into the document's SVG metadata, and the provenance panel can re-run, compare, and revert), all through the user's own OpenRouter key with nothing sent without an explicit action and a send preview.
- **Current-state facts to verify (with claim candidates):**
  - Nodus has no AI code and no HTTP client. `<!-- claim: count "HttpClient" src/Nodus/**/*.cs = 0 -->`
  - The SVG reader drops root `<metadata>`, so embedded provenance needs the reader change owned by `D02 T07 §1` before §1 can prove a round trip. `<!-- claim: count "\"metadata\"" src/Nodus/Bezier.Core/Services/SvgParser.cs = 1 -->`
  - The history keeps 100 steps by default, which one AI apply must occupy as a single step. `<!-- claim: count "_maxHistorySize = 100" src/Nodus/Bezier.Core/Services/HistoryManager.cs = 1 -->`
  - Commands exist for add, delete, group, and property change, the building blocks an AI apply composes. `<!-- claim: exists src/Nodus/Bezier.Core/Commands/AddElementCommand.cs -->`
  - The Imago source tree exists, so the Imago hand-off in §11 has a real target to detect. `<!-- claim: exists src/Imago/src/Imago.UI/App.xaml.cs -->`
  - Lumen has no source tree yet, so its hand-off is file-based and refused by name when absent. `<!-- claim: absent src/Lumen -->`
- **Inputs and XREFs:** `D01 T05 §1` to `§5` (client, key store, provenance, send gate, brand kit); `D02 T07 §1` (live-object contract and metadata the provenance rides); `D02 T07 §5` (layers the generated art lands in); `D02 T09 §3` (swatches and color groups generated colors join); `D02 T09 §6` (Recolor Artwork mapping generative recolor drives); `D02 T09 §10` (pattern swatches for text to pattern); `D02 T10 §13` (writing tools rewrite and grammar sit beside); `D02 T12 §1` (placed bitmap objects image results become); `D02 T12 §5` (the local potrace tracer concept to vector drives); `D02 T13 §4` (bleed settings generate bleed fills); `D02 T16 §7` (welcome screen the AI entries appear on); `D02 T07 §14` (New Document dialog); `D03 T05 §1` (Imago's filter pipeline, the cleanup target of the hand-off); `standards/nodus.md` (commands, SVG native format).
- **Adjacency:** list=applicable (generation history and variations are browsable and filterable in the provenance panel, §1 and §2); document=applicable (generated print bleed feeds the printed page, §4; provenance travels in the saved SVG); settings=applicable @ D01 T05 §2; reporting=applicable (usage meter and per-document AI cost summary in the provenance panel, §1); notifications=applicable (progress, cancel, and completion through the shared AI progress panel, §1); permissions=applicable (no key, offline, declined preview, other app not installed are refusals by name, §1 and §11); audit=applicable (each apply is one named history step plus one provenance record and one log line); exchange=applicable (hand-off files to and from Imago and Lumen, §11; brand kit ASE @ D01 T05 §5); reverse=applicable (every AI apply is undoable and revertable from the provenance panel, §1)

#### §1. AI in Nodus: the AI menu, settings, usage, and the provenance panel

- **Deliverable:** The Nodus AI menu and toolbar button, the AI page in Preferences, the usage meter, the content-aware defaults preference, the first-use tutorial, and the Provenance panel that lists, filters, re-runs with the same seed, compares, reverts, and deletes AI actions recorded in the document.
- **Depends On:** D01 T05 §4
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/ai-menu/ and docs/captures/nodus/provenance-panel/. Job: a designer can reach every AI action from one menu and see, repeat, compare, or undo any AI result in the document. Treatment: an AI menu (and a toolbar split button) listing every action with its owner section, and a dockable Provenance panel with one row per record (thumbnail, action, prompt excerpt, model, seed, cost, date) and Re-run, Re-run with new seed, Compare, Select results, Revert, Delete record. Cheaper substitute that fails: a history list without seeds or models, which cannot reproduce anything. Chrome: consume the shared `SendPreviewDialog`, `AiSettingsPage`, `AiProgressPanel`, `AiUsageIndicator`, the dock layout, and the history; do not build a Nodus-only key or progress UI.
- **Runs:** `Requires: display-session -- menu, panel, and tutorial captures need an interactive desktop`
- **Catalog:** NP-2480 to NP-2485 (6 features)
- **Hints:**
  - `src/Nodus/Photon.Nodus.Desktop/Views/Menus/AiMenu.xaml` (Object, Generative submenu and a top-level AI menu) with every item wired or disabled with `Planned: D02 T15 §N` through `PlannedCommands`, and a toolbar split button remembering the last action.
  - Provenance in the document: `Photon.Nodus.Core/AI/NodusProvenanceBinding.cs` writes the `D01 T05 §3` records into the root `<metadata>` and tags result objects with `nodus:provenance-id`, preserved by the reader per `D02 T07 §1`.
  - `Photon.Nodus.Desktop/Views/Panels/ProvenancePanel.xaml` with `ProvenancePanelViewModel`: filter by action, model, and date; search the prompt; per-document total cost.
  - Re-run replays `ToRerun(sameSeed: true)` into a new result beside the old one; Compare shows both side by side with `ProvenanceDiff`; Revert removes the result objects and the record in one undoable `RevertAiResultCommand`.
  - Preferences: host `AiSettingsPage` as the AI category in the `D02 T06 §13` dialog, plus `nodus.ai.contentAwareDefaults` (default on: prefill prompt fields from selection names and document swatches, never sending anything by itself).
  - Usage: `AiUsageIndicator` in the status bar area, refreshed after each request.
  - First use: `AiQuickTutorial` overlay (three steps: add key, try text to vector on a blank document, open Provenance) shown once, reopenable from Help, with `nodus.ai.tutorialSeen`.
  - One Serilog Information line per AI apply with action, model, seed, record id, object count.
  - Tests: `ProvenancePanelViewModelTests` (filter, re-run request equality, revert restores the document), `NodusProvenanceBindingTests` round-tripping a fixture `tests/fixtures/nodus/ai/provenance-two-records.svg`.
- **Proof:** Format fidelity proof plus unit test: the provenance fixture opens, saves, and reopens with both records and their object links intact; `ProvenancePanelViewModelTests` prove Revert restores the pre-generation document element by element; cheaper substitute that fails: provenance kept only in the app session, lost on reopen.

#### §2. Generate vector artwork from a prompt

- **Deliverable:** Text to vector: the model returns a schema-validated JSON scene that Nodus applies as real paths, named layers, document swatches, styles, and live text in one undoable command, with content types, detail level, style reference and presets, model choice, up to 4 variations, generate similar, variation management, turntable views, and new document from a prompt.
- **Depends On:** §1, D02 T09 §3, D02 T07 §5
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/text-to-vector/. Job: a designer can describe an image and get editable, organized vector art in their document. Treatment: a Text to Vector panel (prompt, type Subject, Scene, Icon, Pattern, detail slider 1 to 5, style reference, style presets, brand kit toggle, model, variations 1 to 4) whose results arrive as a variation strip; choosing one inserts it on a named layer with its swatches in the document palette. Cheaper substitute that fails: placing a generated PNG, or one flattened ungrouped path. Chrome: consume the send gate, provenance, the Swatches panel model, layers, and the history.
- **Runs:** `Requires: display-session -- panel and result captures need an interactive desktop`
- **Catalog:** NP-2486 to NP-2498 (13 features)
- **Hints:**
  - Schema `Photon.Nodus.Core/AI/Schemas/vector-scene.v1.json`: `layers[]` (name, children), `shapes` (path data in a 0 to 1000 viewBox, rect, ellipse, polygon, text with font role and content), `swatches[]` (name, sRGB hex, role), `styles[]` (fill and stroke by swatch name, stroke width, opacity), `constraints[]` (align or symmetry hints); strict mode rejects anything else.
  - `VectorSceneValidator` checks path syntax, bounds, swatch references, and an object budget (default 2,000 elements, `nodus.ai.maxElements`), then `VectorSceneApplier` builds `VectorElement`s and composes `AddElementCommand`s, layer creation, and swatch adds into one `CompositeCommand` named "Generate Vector: <prompt excerpt>".
  - Content type and detail map to system-prompt templates in `Photon.Nodus.Core/AI/Prompts/` hashed into provenance; Icon forces a square artboard-fit and at most 3 colors.
  - Style reference: an image (sent as vision input) or the selected art (sent as its SVG plus a rendered PNG), listed in the send preview; style presets (flat, line art, isometric, duotone, woodcut, and so on) and color-tone presets are local JSON in `Photon.Nodus.Core/AI/Presets/`.
  - Brand kit toggle injects `BrandKitConstraint` so swatches can only be kit colors.
  - Models: pickers filtered to models that support structured output; `Auto` picks the configured `ai.model.vectorJson`, and variations 1 to 4 issue parallel requests with distinct recorded seeds.
  - Live text: text nodes become `SvgText` with the kit or a system font, never outlines.
  - Generate similar reuses a record's prompt and parameters with a new seed and `ParentId`; variations are kept in a `VariationSet` on the provenance record so the strip can rate (1 to 5), swap in place (undoable), or place another.
  - Turntable: asks for N views (3 to 8) of the selected art as separate vector scenes on one artboard row, each on a layer named by angle; help text says when to use 3D and Materials (`D02 T11 §10`) instead.
  - New document from a prompt: `File, New from Prompt` and the welcome screen entry (`D02 T16 §7`) create a document sized by the chosen preset, then run text to vector into it.
  - Tests: `VectorSceneValidatorTests` (reject bad path, unknown swatch, over budget), `VectorSceneApplierTests` over fixtures `tests/fixtures/nodus/ai/vector-scene-*.json` asserting layers, swatches, live text, and a single undo step.
- **Proof:** Unit test plus format fidelity proof: `VectorSceneApplierTests` apply committed JSON fixtures and compare the saved SVG element by element with goldens under `tests/fixtures/nodus/ai/`, and one Undo returns the document to its prior state; cheaper substitute that fails: inserting a raster image, which the element comparison rejects.

#### §3. Generate patterns and fill shapes

- **Deliverable:** Text to pattern (a seamless vector pattern swatch), managing and editing generated patterns, and generative shape fill that fills the selected shape with generated vector art clipped to it, with detail and style reference, reusable across repeated shapes.
- **Depends On:** §2, D02 T09 §10
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/ai-pattern/ and docs/captures/nodus/shape-fill/. Job: a designer can make an editable seamless pattern or fill a shape with art that fits it. Treatment: Pattern mode in the Text to Vector panel producing a pattern swatch that opens in Pattern Options, and a Shape Fill command on the contextual bar that clips generated art to the selection. Cheaper substitute that fails: a bitmap pattern fill or art placed over the shape without a clip. Chrome: consume the §2 schema and applier, the pattern swatch model of `D02 T09 §10`, and clipping groups.
- **Runs:** `Requires: display-session -- pattern and fill captures need an interactive desktop`
- **Catalog:** NP-2499 to NP-2502 (4 features)
- **Hints:**
  - Schema extension `vector-pattern.v1.json`: a tile size and tile type (grid, brick, hex) plus the §2 shape list; `PatternTileValidator` checks edge continuity by clipping every shape to the tile and its neighbors so the result is seamless.
  - Applier creates a pattern swatch in the Swatches panel and opens it in the Pattern Options editor of `D02 T09 §10`; variations become sibling swatches in a color group named after the prompt.
  - Manage: regenerate one variation, rename, edit tiles by hand (the swatch is ordinary vector content), delete (undoable).
  - Shape fill: sends the selected shape outline (as SVG path plus its bounding box) as a structured constraint; results land in a clipping group with the original shape as the clip path, named "Shape Fill: <prompt>".
  - Options: detail, style reference (image or art), model, brand kit toggle, same as §2.
  - Repeat: `Apply Shape Fill to Similar` reuses the record (same seed or new seed per shape) across every selected or same-geometry shape, each result linked to the parent record.
  - Tests: `PatternTileValidatorTests` (seam check), `ShapeFillApplierTests` (clip group, one undo step), fixtures under `tests/fixtures/nodus/ai/pattern-*.json`.
- **Proof:** Unit test: `PatternTileValidatorTests` reject a fixture with a broken seam and accept a seamless one; `ShapeFillApplierTests` compare the saved SVG to a golden with the clip path; cheaper substitute that fails: unclipped art overlapping the shape.

#### §4. Generative expand and print bleed

- **Deliverable:** Generative expand for vector artwork (extend the composition to new bounds with editable vectors), its options, generate print bleed (extend backgrounds into the bleed), and generative expand for placed images (outpaint through an image model into a new placed image with provenance).
- **Depends On:** §2, D02 T13 §4
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/generative-expand/. Job: a designer can extend artwork to a new size or into the bleed without redrawing it. Treatment: an Expand dialog with a live frame on the canvas (target bounds, anchor, match style strength, keep original locked), and a Generate Bleed command that reads the document's bleed. Cheaper substitute that fails: scaling the art to the new bounds. Chrome: consume the §2 applier, the send gate, bleed settings of `D02 T13 §4`, and placed images of `D02 T12 §1`.
- **Runs:** `Requires: display-session -- expand frame and result captures need an interactive desktop`
- **Catalog:** NP-2503 to NP-2505 (3 features)
- **Hints:**
  - Vector expand sends the selection SVG, its bounds, and the target bounds; the schema returns only new shapes outside the original bounds; `ExpandValidator` rejects shapes that overlap the original beyond a tolerance so existing art is never altered.
  - Results go on a new layer "Expanded" above or below by option; one undoable command.
  - Generate bleed: computes the bleed band from the artboard and document bleed (`D02 T13 §4`), expands only background-layer art into it, and marks the new objects non-printing-optional with a layer flag.
  - Image expand: sends the placed image with a transparent canvas at the target aspect ratio to an image-edit model, receives a new PNG, places it as a new image object with the original kept hidden underneath and linked by provenance.
  - Options persisted: `nodus.ai.expand.anchor`, `nodus.ai.expand.matchStrength`, `nodus.ai.expand.keepOriginalLocked`.
  - Budget: images over 16 megapixels are downscaled for sending with the size shown in the preview, and the result upscaled back locally.
  - Tests: `ExpandValidatorTests`, `GenerateBleedTests` (band geometry for a 3 mm bleed), `ImageExpandApplierTests` (original kept, new image placed).
- **Proof:** Unit test: `GenerateBleedTests` assert the generated objects lie only inside the bleed band and the original art is unchanged element by element; cheaper substitute that fails: stretching the background to the bleed, which changes the original's geometry.

#### §5. AI recolor and palettes from the brand kit

- **Deliverable:** Generative recolor from a prompt (palette proposals applied through the Recolor Artwork mapping, undoable), brand-kit-constrained recolor, palette generation to swatches and color groups, and AI color palette presets.
- **Depends On:** §1, D02 T09 §6, D01 T05 §5
- **Phase:** 12
- **Surface:** UI. Fidelity: extends the Recolor Artwork dialog -- docs/captures/nodus/recolor-artwork/ (from `D02 T09 §6`). Job: a designer can ask for a color mood and get palette options applied to their art, optionally only from the brand kit. Treatment: a Generative tab in Recolor Artwork with a prompt, sample prompts, "use brand kit" toggle, and 4 palette proposals previewed live on the selection. Cheaper substitute that fails: a random hue shift. Chrome: consume the Recolor Artwork mapping engine, the brand kit library, and the Swatches panel.
- **Runs:** `Requires: display-session -- recolor preview captures need an interactive desktop`
- **Catalog:** NP-2506 to NP-2507 (2 features)
- **Hints:**
  - Only the color list leaves the machine: `RecolorRequestBuilder` sends the selection's unique colors with their roles and area share, never the geometry; the send preview shows the list.
  - Schema `palette-proposal.v1.json`: proposals of `{ name, colors[] (hex, maps-from hex) }`; the mapping feeds `RecolorArtworkEngine` of `D02 T09 §6` so the apply is its existing undoable command.
  - Brand kit mode injects the kit's colors as an enum; the model must choose from them.
  - Save a proposal as a color group in Swatches or as a palette in the active brand kit.
  - Palette presets: local `ai-palette-presets.json` (for example muted, high contrast, pastel, corporate) that constrain generation in §2, §3, and §8.
  - Tests: `RecolorRequestBuilderTests` (no geometry in the payload), `PaletteProposalApplierTests` (brand kit mode rejects a non-kit color, apply is one undo step).
- **Proof:** Unit test: `RecolorRequestBuilderTests` assert the payload holds only colors, and the applier round trip restores original colors on Undo; cheaper substitute that fails: sending the whole document SVG, which the payload test rejects.

#### §6. The AI assistant: prompt to edit with undoable commands

- **Deliverable:** The Assistant panel (chat, multiple chats, follow-up questions, attached files, background tasks), workflow starters, skills as slash commands, and prompt to edit selected artwork, where every assistant action is a named undoable Nodus command with provenance.
- **Depends On:** §1
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/ai-assistant/. Job: a designer can ask for production edits in words and review each resulting command before and after it applies. Treatment: a dockable chat panel where the model answers with a plan of tool calls rendered as a checklist (command name, target objects, parameters) that the user applies all, step by step, or not at all. Cheaper substitute that fails: an assistant that edits the SVG text directly. Chrome: consume the command registry, the keymap command index of `D02 T06 §12`, the send gate, and provenance; do not add a scripting engine.
- **Runs:** `Requires: display-session -- panel and plan captures need an interactive desktop`
- **Catalog:** NP-2508 to NP-2512 (5 features)
- **Hints:**
  - `Photon.Nodus.Core/AI/Assistant/AssistantToolCatalog.cs` exposes a whitelist of existing commands (select by name or style, recolor, align, distribute, rename layers, group, set document size, export preset, fit text) as OpenRouter tool definitions with JSON schemas; nothing outside the whitelist can run.
  - The document is summarized for the model as a structure digest (layers, names, types, counts, colors) rather than full geometry, shown in the send preview.
  - `AssistantPlan` of tool calls is validated then applied as one `CompositeCommand` named "Assistant: <request>" with a provenance record; step mode applies one call per history step.
  - Prompt to edit: with generated art selected, "change the hat to red", "remove the tree" become edits scoped to objects tagged by the §2 record.
  - Chats: multiple named chats per document stored in `nodus:assistant` metadata (opt-out with `nodus.ai.assistant.saveChats`), follow-up questions when the model asks for clarification, attached files listed in the preview.
  - Background tasks: a long plan runs with the shared progress panel while editing stays enabled on other documents; it refuses to apply if the target document changed since planning, by name.
  - Workflow starters: Recolor, Organize Layers, Export Setup, Document Setup, Fit Text as prefilled prompts.
  - Skills: `/prepare-for-print`, `/name-layers`, `/export-icons` defined as JSON in `%LOCALAPPDATA%\Rizonesoft\Nodus\ai\skills\`, each a fixed list of whitelisted commands with parameters (no code).
  - Generate, recolor, and vectorize from the assistant call §2, §5, and §10 through the same gate.
  - Tests: `AssistantPlanValidatorTests` (non-whitelisted command refused), `AssistantPlanApplierTests` (one undo step, provenance written), `SkillLoaderTests`.
- **Proof:** Unit test: `AssistantPlanValidatorTests` refuse a plan calling an unknown command and `AssistantPlanApplierTests` prove the applied plan undoes in one step; cheaper substitute that fails: free-form SVG edits from the model, which the whitelist rejects.

#### §7. AI text: rewrite, translate, proofread, fit, and retype

- **Deliverable:** Rewrite (generate, rephrase, translate, proofread, fit text to frame), model-based grammar checking with options and checking styles, and Retype (identify fonts in an image or outlined text against installed fonts, convert image text to live text).
- **Depends On:** §1, D02 T10 §13
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/ai-rewrite/ and docs/captures/nodus/retype/. Job: a designer can improve or translate copy in place and turn text in an image into live text in a matching installed font. Treatment: a Rewrite panel with before and after preview that keeps character formatting runs, a Grammar dialog listing issues with rule, suggestion, Replace, Skip, and Add, and a Retype panel listing candidate installed fonts with confidence. Cheaper substitute that fails: replacing the text frame's content with plain unformatted text. Chrome: consume the text model, the Windows Spell Checking API integration of `D02 T10 §13`, the send gate, and provenance.
- **Runs:** `Requires: display-session -- panel captures need an interactive desktop`
- **Catalog:** NP-2513 to NP-2517 (5 features)
- **Hints:**
  - Rewrite sends the text as formatting runs (`[{text, runId}]`), and the schema returns runs with the same ids so styling survives translation and rephrasing; missing ids are refused.
  - Fit text: target character count computed from the frame's overflow, the model shortens, and the result is verified locally by re-laying out the frame.
  - Grammar: `GrammarChecker` asks for issues as `{start, length, rule, message, suggestion}`, with checking styles (Quick, Strict, Formal, Informal, Technical, Advertising, Fiction) as prompt templates and options (auto start, prompt before replacement, suggest spelling) as settings; spelling itself stays with the Windows API of `D02 T10 §13`.
  - Every replacement is one undoable text command with provenance.
  - Retype: renders the selected image region or outlined text to PNG, sends it as vision input asking for glyph features (serif, weight, width, x-height ratio, stroke contrast) and the recognized text, then ranks installed fonts locally by comparing rendered samples (perceptual hash distance), so no font list leaves the machine.
  - Convert to live text creates `SvgText` over the image region with the chosen font and hides the source.
  - Tests: `RewriteRunMapperTests`, `GrammarIssueParserTests`, `FontMatcherTests` (a committed sample rendered in a known installed font ranks that font first).
- **Proof:** Unit test: `RewriteRunMapperTests` prove a two-run bold and regular paragraph keeps both runs after a recorded translation reply; `FontMatcherTests` rank the true font first; cheaper substitute that fails: plain-text replacement, which drops the bold run.

#### §8. AI images: generate, remix, and reference images

- **Deliverable:** Text to image placed as a bitmap with provenance, reference image generation, remix of an existing image, aspect ratio and format, style and palette presets, model selection, the quick generate dialog, and the AI Generate panel.
- **Depends On:** §1, D02 T12 §1
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/ai-generate/. Job: a designer can generate or remix a raster image and place it as an ordinary image object. Treatment: an AI Generate panel (prompt, mode Create or Remix, reference image, aspect ratio, style preset, palette preset, model, count) and a one-dialog Quick Generate from File; results arrive as placed images. Cheaper substitute that fails: pasting generated pixels into existing artwork. Chrome: consume placed image objects of `D02 T12 §1`, the send gate, provenance, and the shared progress panel.
- **Runs:** `Requires: display-session -- panel and dialog captures need an interactive desktop`
- **Catalog:** NP-2518 to NP-2524 (7 features)
- **Hints:**
  - `ImageGenerationService` builds `ImageRequest` for image-output models filtered from the catalog; aspect ratios 1:1, 4:3, 3:2, 16:9, 9:16, and a custom size.
  - Results embed as PNG image objects on a layer "Generated", named by prompt excerpt, with `nodus:provenance-id`.
  - Reference image: the selected image or a file, sent as input and listed in the preview; Remix sends the selected image with an edit instruction and places the result beside the original.
  - Style presets and palette presets are local JSON shared with §2 (`nodus.ai.image.stylePreset` remembered per app, independent of Imago).
  - Quick Generate dialog (`File, Quick Generate`) wraps the same service with Create Image, Remix Image, and Create Vector (routes to §2).
  - Timeouts and failures use the §1 mapping of `D01 T05` with a Retry button; cancelled generations place nothing.
  - Tests: `ImageGenerationServiceTests` over recorded fixtures, `GeneratedImagePlacementTests` (placed, not flattened; one undo step).
- **Proof:** Unit test: `GeneratedImagePlacementTests` prove the result is a separate image object and the existing elements are byte-identical after placement; cheaper substitute that fails: merging pixels into an existing image, which the element comparison catches.

#### §9. AI image cleanup: remove background, upscale, repair, and art style

- **Deliverable:** Remove background (mask plus cut-out as a new image), AI upsampling in illustration and photo modes with noise reduction, JPEG artifact removal, and art style transfer with presets, each non-destructive with provenance and the original kept.
- **Depends On:** §8
- **Phase:** 12
- **Surface:** UI. Fidelity: extends the bitmap contextual bar and Resample dialog -- docs/captures/nodus/bitmap-resample/ (from `D02 T12 §1`); new Art Style dialog captured to docs/captures/nodus/art-style/. Job: a designer can clean up a placed image without leaving Nodus and without losing the original. Treatment: Remove Background, Upscale, Remove JPEG Artifacts, and Art Style commands on the image contextual bar, each producing a new image object above the hidden original. Cheaper substitute that fails: overwriting the embedded image. Chrome: consume placed images, the send gate, provenance, and the pixel engine of `D01 T03` for local pre and post steps.
- **Runs:** `Requires: display-session -- before and after captures need an interactive desktop`
- **Catalog:** NP-2525 to NP-2530 (6 features)
- **Hints:**
  - `ImageCleanupService` with one method per operation, all calling image-edit models through the gate with the image size shown in the preview.
  - Remove background returns a cut-out PNG; a local alpha threshold builds the mask, and the result is a new image plus an optional clipping path traced from the mask; the bounding box shrinks to the subject.
  - Upscale: modes Illustration and Photo, factor 2x or 4x, noise reduction 0 to 100 as a prompt parameter; a local Lanczos fallback from `D01 T03` is offered by name when AI is off.
  - JPEG artifact removal as an image-edit call, with a local deblocking fallback noted as lower quality.
  - Art style: Nodus's own preset list (for example Acrylic, Graphite, Pastel, Mosaic, Neon, Woodcut, Watercolor) in local JSON with intensity and detail sliders; applies to images and, by rasterizing, to vector groups, producing a new image and keeping the group hidden.
  - Every result: new object, original hidden and locked beneath, linked by provenance; Revert in the provenance panel restores the original.
  - Tests: `ImageCleanupServiceTests` over recorded fixtures, `CleanupResultPlacementTests` (original unchanged, new object above).
- **Proof:** Unit test: `CleanupResultPlacementTests` prove the original image bytes are unchanged and the result is a new object for each of the four operations; cheaper substitute that fails: replacing the embedded bytes.

#### §10. Concept to vector: sketches and images to structured vectors

- **Deliverable:** Concept to vector (a sketch or photo to a clean structured vector with named parts), up to 8 preset variations, match reference image, raster output option, model choice, an unexpanded trace source, and AI-assisted tracing in which the model proposes palette, segmentation, and cleanup parameters for the local tracer.
- **Depends On:** §2, D02 T12 §5
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/concept-to-vector/. Job: a designer can turn a rough sketch or photo into organized, editable vectors. Treatment: a Concept to Vector panel (source image, style preset strip up to 8, match reference toggle, output Vector or Raster, model) and an "AI prepare" step in the trace dialog of `D02 T12 §5`. Cheaper substitute that fails: sending the image to a model and placing its raster output as the vector result. Chrome: consume the §2 applier, the local potrace port in `Photon.Nodus.Core/Tracing/`, and quantization of `D01 T03 §3`.
- **Runs:** `Requires: display-session -- panel and trace captures need an interactive desktop`
- **Catalog:** NP-2531 to NP-2534 (4 features)
- **Hints:**
  - Two routes, chosen by the user: Structured (vision model returns a §2 vector scene with named parts such as "head", "background") and Trace-assisted (model returns only `TraceParameters` JSON: color count, palette hex list, smoothing, corner threshold, region hints; the local tracer does the geometry).
  - Trace-assisted keeps the trace source unexpanded as a live trace object per `D02 T07 §1`, so the user can retune it without another request.
  - Optional pre-steps: background removal and upscale from §9, each listed in the send preview.
  - Up to 8 variations across style presets; Raster Output places a cleaned image instead (via §8).
  - Match reference: an extra reference image steers style; its hash goes into provenance.
  - Tests: `TraceParametersValidatorTests`, `ConceptToVectorApplierTests` over fixtures `tests/fixtures/nodus/ai/concept-*.json` plus a committed sketch PNG, compared to goldens.
- **Proof:** Format fidelity proof: the trace-assisted route on the committed sketch fixture with recorded parameters produces an SVG matching its golden element by element (deterministic because the tracer is local); cheaper substitute that fails: a raster placed as the result.

#### §11. The suite pipeline: Lumen to Imago to Nodus hand-offs and shared brand kits

- **Deliverable:** Receiving images exported by Lumen and Imago (watched hand-off folder or Open With), sending a placed image to Imago for cleanup and relinking the result (only when Imago is installed, refused by name otherwise), a suite launcher, brand kit sync across apps, provenance carried across the hand-off, and linked variations across documents.
- **Depends On:** §10, D01 T05 §5
- **Phase:** 12
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/suite-handoff/. Job: a designer can move an image from Lumen through Imago into a Nodus trace without manual file juggling. Treatment: an image context command "Edit in Imago" and a suite launcher menu listing installed suite apps; a hand-off inbox panel for files arriving from Lumen or Imago with their provenance. Cheaper substitute that fails: a hard project reference to Imago or a launcher that shows apps that are not installed. Chrome: consume single instance and file-open forwarding of `D01 T02 §3`, the brand kit library, provenance, and linked images.
- **Runs:** `Requires: display-session -- the hand-off round trip with Imago is a driven run`
- **Catalog:** NP-2535 to NP-2536 (2 features)
- **Hints:**
  - `SuiteAppLocator` in `Photon.Core` reads the install registry keys the suite installer writes (`HKCU\Software\Rizonesoft\Photon\Apps\<App>\ExePath`) and verifies the exe exists; absent apps are refused by name ("Imago is not installed").
  - Edit in Imago: writes the placed image to `%LOCALAPPDATA%\Rizonesoft\Photon\handoff\<guid>.png` with a sidecar `<guid>.provenance.json`, launches or forwards to Imago with `--handoff <path>`, watches the file, and relinks the placed image when Imago saves it (undoable relink).
  - Inbox: `FileSystemWatcher` on the hand-off folder; files tagged for Nodus appear in a Hand-off panel with source app, time, and provenance; Place or Trace (§10) from there.
  - Provenance carry: sidecar records from Lumen or Imago are appended to the document with `ParentId` links so the lineage shows the whole chain.
  - Brand kit sync is the shared folder of `D01 T05 §5`; Nodus shows the active kit and refreshes on change.
  - Linked variations: a variation set can be referenced from another document by record id; `Swap Variation` updates every linked instance (undoable per document).
  - No assembly reference to Imago or Lumen; a test asserts `Photon.Nodus.Desktop` references neither.
  - Tests: `SuiteAppLocatorTests` (fake registry), `HandoffRoundTripTests` (sidecar provenance survives, relink undoable), `ProjectReferenceGuardTests`.
- **Proof:** Driven run with evidence plus unit test: a driven Nodus to Imago to Nodus relink produces the log lines and a relinked image, and `HandoffRoundTripTests` prove the provenance chain; with Imago's registry key removed the command refuses by name; cheaper substitute that fails: a direct project reference, which the guard test fails.

### todo/02-nodus/TODO-16-nodus-parity-workspace.md -- `nodus-parity-workspace`

- **Title:** "TODO-16 -- Nodus Parity: Workspace, Customization, Preferences, and Utilities"
- **Phase(s):** 13
- **Goal:** Nodus reaches Illustrator 30.8 and CorelDRAW 2026 parity for the workspace a professional customizes and lives in: named workspaces with presets and import and export, customizable toolbox, toolbars, property bar, status bar, menus, context menus, and shortcut sets, complete Preferences across general, selection and nodes, display, files, performance, and warnings, UI appearance, scaling, and diagnostics, the welcome screen and navigator (promoting backlog B-013, source `legacy-nodus-5.8-5.9`, into §7), pen, touch, and Surface Dial input, hints and a project timer, object data with find and replace objects, and QR codes and barcodes; it extends, never duplicates, the command palette (`D02 T06 §12`), the Preferences dialog and shortcut remapping (`D02 T06 §13`), accessibility (`D02 T06 §17`), and the shortcuts dialog and Help menu (`D02 T05 §2`, `§3`).
- **Current-state facts to verify (with claim candidates):**
  - The main window's Window menu toggles five fixed panels and nothing saves a named arrangement. `<!-- claim: count "IsChecked=\"\{Binding Show[A-Za-z]*Panel\}\"" src/Nodus/Bezier.Desktop/Views/MainWindowView.xaml = 5 -->`
  - AvalonDock is referenced but no view uses a `DockingManager` yet (tabs and dock layouts arrive with `D02 T06 §7`). `<!-- claim: count "Dirkster.AvalonDock\"" src/Nodus/Bezier.Desktop/Bezier.Desktop.csproj = 1 -->`
  - `ShortcutManager` already models profiles including an Illustrator set, remapping, conflicts, and JSON export, which §3 extends rather than replaces. `<!-- claim: count "Illustrator," src/Nodus/Bezier.Core/Services/ShortcutManager.cs = 1 -->`
  - Theming is the Catppuccin `ThemeManager` today, which the suite theme of `D01 T01 §3` replaces before §6 adds brightness levels. `<!-- claim: count "CatppuccinThemes" src/Nodus/Bezier.Core/Services/ThemeManager.cs = 2 -->`
  - Nodus has no welcome screen or navigator (Imago has a placeholder `WelcomeViewModel`). `<!-- claim: count "Navigator" src/Nodus/**/*.cs = 0 -->`
  - No pen, stylus, or touch input handling exists. `<!-- claim: count "Stylus" src/Nodus/**/*.cs = 0 -->`
  - No QR or barcode library is referenced. `<!-- claim: count "ZXing" src/Nodus/**/*.csproj = 0 -->`
  - The status strip shows one bound text. `<!-- claim: count "Text=\"\{Binding StatusText\}\"" src/Nodus/Bezier.Desktop/Views/MainWindowView.xaml = 1 -->`
- **Inputs and XREFs:** `D02 T06 §7` (tabs and saved dock layouts §1 builds on); `D02 T06 §12` (command palette and command index §3 extends); `D02 T06 §13` (Preferences dialog and shortcut remapping §1, §3, §4, §5 extend); `D02 T06 §17` (accessibility and scaling §6 and §8 extend); `D02 T05 §2` and `§3` (shortcuts dialog and Help menu §3 and §9 extend); `D02 T02 §8` (the one keymap); `D02 T07 §5` (Objects panel and object names §10 queries); `D02 T07 §8` (property bar and contextual task bar §2 customizes); `D02 T07 §12` (zoom, view modes, and document windows the view preferences drive); `D02 T07 §14` (New Document dialog and presets the welcome screen uses); `D02 T09 §1` (the color model QR fills use); `D01 T01 §3` (suite theme); `D01 T02 §2` (settings store); `D01 T01 §2` (exception window the error-reporting toggle governs); `todo/backlog.md` B-013 (promoted into §7 and removed from the backlog in the same commit); `docs/legacy/nodus-roadmap.md` phases 5.8 and 5.9.
- **Adjacency:** list=applicable (workspaces, toolbars, shortcut sets, find results, object data, and timer tasks are listed and searchable); document=applicable (printed shortcut list §3, printed object data summary §10, QR and barcodes on the printed page §11); settings=applicable @ D02 T06 §13; reporting=applicable (document info panel and object data totals §10, time sheet export §9, system information §6); notifications=applicable (background save progress §5, inactivity prompt §9, safe mode report §6); permissions=applicable (read-only workspace or shortcut file on import, missing content folder, unavailable GPU refused by name §1, §5, §6); audit=applicable (every document edit such as object data, replace objects, or insert QR is an undoable logged command; customization changes log one line each); exchange=applicable (workspace files, shortcut sets, search criteria, time sheet CSV, object data CSV); reverse=applicable (reset workspace, reset menus, reset shortcuts, reset preferences, F8 factory reset, and undo for every document edit)

#### §1. Workspaces: presets, save, reset, import, and export

- **Deliverable:** A workspace switcher with presets (Default, Lite, Touch, Illustration, Page Layout, Illustrator-style), new, duplicate, rename, delete, and reset, workspace import and export, factory reset with F8 at startup, hide and show all panels (Tab), panel docking, grouping, floating, and collapse to icons, panel lock, and the application bar.
- **Depends On:** D02 T06 §13
- **Phase:** 13
- **Surface:** UI. Fidelity: Nodus main window -- docs/captures/nodus/main-window/, extended with captures per preset under docs/captures/nodus/workspaces/. Job: a designer can switch the whole window arrangement for a task and carry their own arrangement to another machine. Treatment: an application bar workspace switcher and Window, Workspace menu; a workspace is a named bundle of dock layout, visible toolbars and toolbox set, property bar items, menu customization, and shortcut set. Cheaper substitute that fails: saving only the dock layout. Chrome: consume AvalonDock layout serialization from `D02 T06 §7`, the settings store, the keymap, and the theme; do not add a second layout persistence.
- **Runs:** `Requires: display-session -- switching and capturing workspaces needs an interactive desktop`
- **Catalog:** NP-2551 to NP-2566 (16 features)
- **Hints:**
  - `Photon.Nodus.Core/Workspace/WorkspaceDefinition.cs` (id, name, description, basedOn, dockLayoutXml, toolbars, toolboxSet, propertyBarItems, menuCustomization, shortcutSetId, statusBar) and `WorkspaceService` (list, apply, save current, duplicate, rename, delete, reset to its preset).
  - Presets shipped as read-only JSON in `Photon.Nodus.Desktop/Workspaces/`: Default, Lite (reduced toolbox and panels), Touch (enlarged controls, hands off to §8), Illustration, Page Layout, Illustrator-style (panels on the right, Illustrator shortcut profile from `ShortcutManager`); Default cannot be deleted.
  - User workspaces saved under `%LOCALAPPDATA%\Rizonesoft\Nodus\workspaces\<id>.json`; setting `nodus.workspace.current`.
  - Import and export `.nodusws` (zip of the JSON plus referenced icons) with a checkbox list of parts to import (panels, toolbars, menus, shortcuts) into the current or a new workspace; a read-only or malformed file is refused by name.
  - F8 held at startup (checked in `App.OnStartup` with `Keyboard.IsKeyDown`) asks to reset application, workspace, and tool settings to factory defaults, keeping global settings and the AI key; logged.
  - Tab hides or shows all panels, Shift+Tab all except the toolbox and property bar; Window, Hide Panels and Lock Panels toggles; lock disables dock drag.
  - Panels collapse to icon strips with `nodus.ui.autoCollapseIconPanels` (consumed here; the toggle lives in §6).
  - Panel quick customize: a chevron on each dock group listing panels with checkboxes.
  - Application bar: workspace switcher, command search (`D02 T06 §12`), AI usage (`D02 T15 §1`), no account or cloud items.
  - Tests: `WorkspaceServiceTests` (apply restores every part, delete refuses Default), `WorkspaceFileTests` round-tripping a fixture `tests/fixtures/nodus/workspace/illustration.nodusws`.
- **Proof:** Format fidelity proof plus driven run: the committed `.nodusws` fixture imports and re-exports with every part equal, and switching presets in a driven run changes the captured layout; cheaper substitute that fails: a workspace that saves only dock positions, which the part-by-part comparison rejects.

#### §2. Toolbox, toolbars, property bar, and status bar customization

- **Deliverable:** A toolbox with flyouts, tear-off flyouts, Alt-click cycling, single or double column, basic and advanced tool sets, an edit-toolbar drawer, quick customize; named toolbars (Standard, Zoom, Text, Layout, Transform, Web, Document) plus custom toolbars with add, remove, move, copy, appearance, button images, lock, dock and float; property bar positioning and quick customize; and a configurable status bar.
- **Depends On:** §1, D02 T07 §8
- **Phase:** 13
- **Surface:** UI. Fidelity: Nodus main window -- docs/captures/nodus/main-window/, with new captures under docs/captures/nodus/toolbars/. Job: a designer can put the tools and commands they use where they want them. Treatment: toolbars as `ToolBarTray` bands bound to a `CommandBarDefinition` model; drag with Alt to move and Ctrl+Alt to copy buttons; a Customization page listing all commands for drag-in. Cheaper substitute that fails: fixed XAML toolbars with visibility toggles only. Chrome: consume the icon catalog, the keymap's command registry, and the workspace model of §1; one command registry, no per-toolbar command copies.
- **Runs:** `Requires: display-session -- toolbar drag customization is a driven run`
- **Catalog:** NP-2567 to NP-2593 (27 features)
- **Hints:**
  - `Photon.Nodus.Core/Workspace/CommandBarDefinition.cs` (id, caption, items of command id or separator or control id, dock edge, band, floating bounds, button size Small, Medium, Large, style Icon, Caption, Icon and Caption, locked) saved into the current workspace.
  - Built-in bars: Standard, Zoom, Text, Layout, Transform, Web (export for screens commands), Document (tabs and windows); Window, Toolbars menu lists each with a check.
  - Toolbox: `ToolboxDefinition` with flyout groups from `ToolManager`, single or double column, Basic and Advanced sets, tear-off flyouts as floating bars, Alt-click cycling, and an All Tools drawer to drag tools in and out.
  - Quick customize buttons on the toolbox, each toolbar, and the property bar show checkbox lists with Reset.
  - Customization page (in the `D02 T06 §13` dialog): searchable command list with drag onto any bar, New, Rename, Delete toolbar, replace button image from an `.ico`, `.png`, or `.svg` file with Restore Default.
  - Property bar per tool and selection context (from `D02 T07 §8`): dock to any edge or float, items per context toggled.
  - Status bar: sections for tool hint, object details (fill, stroke, size, position, type), cursor coordinates, document color profile, zoom, and artboard navigation; 1 or 2 lines, top or bottom, small to large, items addable by Alt-drag, fill and stroke swatches clickable to open their editors; Reset.
  - Show or hide toolbox bottom controls (fill and stroke, draw mode, screen mode) persisted per workspace.
  - Tests: `CommandBarDefinitionTests` (add, move, copy, remove items; serialization), `ToolboxDefinitionTests` (flyout cycling order), `StatusBarConfigTests`.
- **Proof:** Unit test plus driven run: `CommandBarDefinitionTests` round-trip a customized bar through the workspace file; a driven Ctrl+Alt drag copies a button and the capture shows it after restart; cheaper substitute that fails: toolbars that reset on restart.

#### §3. Menus, context menus, command search, and shortcut sets

- **Deliverable:** Context menus everywhere, menu customization (reorder, rename captions, add and remove items, reset, menu bar mode), command search in customization, shortcut sets saved, loaded, deleted, and cleared, shortcut tables per editing context, view all, reset, export to text or CSV, print, and conflict warnings.
- **Depends On:** §1, D02 T06 §12
- **Phase:** 13
- **Surface:** UI. Fidelity: extends the shortcuts dialog -- docs/captures/nodus/shortcuts/ (from `D02 T05 §2`) and the Preferences dialog -- docs/captures/nodus/preferences/ (from `D02 T06 §13`); context menu captures under docs/captures/nodus/context-menus/. Job: a user can make menus and shortcuts match their habits and take their shortcut set to another machine. Treatment: a Customization dialog with Commands, Menus, and Shortcuts pages; shortcut tables for Main, Text Editing, Node Editing, Table Editing, and Print Preview contexts. Cheaper substitute that fails: a second shortcut list outside `ShortcutManager`. Chrome: consume `ShortcutManager`, the command index of `D02 T06 §12`, the shortcuts dialog of `D02 T05 §2`, and the workspace model.
- **Runs:** `Requires: display-session -- menu customization and context menus are driven runs`
- **Catalog:** NP-2594 to NP-2607 (14 features)
- **Hints:**
  - Context menus: `ContextMenuProvider` builds canvas menus from the selection kind (none, path, text, group, image, artboard, guide) out of registered commands, including isolate, PowerClip-style clip, arrange, and transform entries; each menu listed in a test.
  - `MenuDefinition` (tree of command ids and submenus with caption overrides and `&` access keys) stored in the workspace; `MenuBuilder` renders the main menu from it; Reset Menus restores the default tree.
  - Menu bar mode: Normal or Compact (File, Edit, View, Help only) via `nodus.ui.menuBarMode`.
  - Command search box in the Commands page reuses the `D02 T06 §12` fuzzy index.
  - Shortcut tables: `ShortcutManager` gains a `Context` dimension so the same gesture can differ in text editing and node editing; conflicts are checked within a context and refused by name.
  - Shortcut set files: JSON sets under `%LOCALAPPDATA%\Rizonesoft\Nodus\shortcuts\` with Save As, Load, Delete, Clear All; the Illustrator profile ships as a read-only set.
  - Export to TXT and CSV (context, category, command, gesture); Print extends the `D02 T05 §2` print path with a context column.
  - Tests: `ContextMenuProviderTests`, `MenuDefinitionTests` (reorder, rename, reset), `ShortcutContextTests` (per-context conflict), `ShortcutExportTests` against a golden CSV.
- **Proof:** Unit test: `ShortcutContextTests` refuse a conflicting gesture in one context and allow it in another, and `ShortcutExportTests` match the committed golden CSV; cheaper substitute that fails: one global table, which the per-context test fails.

#### §4. Preferences: general, selection and nodes, display, and units

- **Deliverable:** Preferences pages for general behavior (keyboard increment, constrain angle, corner radius, auto add and delete, precise cursors, anti-aliasing, preview bounds, print size at 100%, double-click to isolate, transform defaults, wheel zoom, reset), selection and anchor display, nodes and handles appearance, Ctrl and Shift convention, type selection residue, save settings as default, the category switcher, and tool default pages.
- **Depends On:** D02 T06 §13
- **Phase:** 13
- **Surface:** UI. Fidelity: extends the Preferences dialog -- docs/captures/nodus/preferences/ (from `D02 T06 §13`). Job: a designer can tune how selection, nodes, snapping distance, and tool defaults behave. Treatment: categories General, Selection and Anchors, Nodes and Handles, Type, Tools (Rectangle, Ellipse, Spiral, Graph Paper, Pick), each control bound to a settings key with a default and a named consumer, and a category switcher of Application, Tools, and Global. Cheaper substitute that fails: controls that persist a value nothing reads. Chrome: consume `NodusSettings`, the settings store, and the `D02 T06 §13` dialog shell; do not open a second options window.
- **Runs:** `Requires: display-session -- preferences captures and driven changes need an interactive desktop`
- **Catalog:** NP-2658 to NP-2698 (41 features)
- **Hints:**
  - General keys: `nodus.edit.keyboardIncrement` (1 px), `nodus.edit.constrainAngle` (0 degrees base, 15 degree step), `nodus.shapes.cornerRadius`, `nodus.pen.autoAddDelete`, `nodus.ui.preciseCursors`, `nodus.render.antialias`, `nodus.geometry.usePreviewBounds`, `nodus.view.printSizeAt100`, `nodus.edit.doubleClickIsolates`, `nodus.transform.patterns`, `.scaleCorners`, `.scaleStrokes`, `nodus.view.wheelZooms`, `nodus.view.invertScroll`; each consumer named in a table in the section.
  - Selection and anchors: `nodus.select.tolerancePx`, `nodus.select.byPathOnly`, `nodus.snap.pointDistancePx` (consumed by the snapping of `D02 T02 §7`), `nodus.select.ctrlClickBehind`, `nodus.artboard.moveLockedHidden`, `nodus.view.zoomToSelection`, `nodus.handles.size`, `nodus.handles.showForMultiple`, `nodus.pen.rubberBand`.
  - Nodes and handles: size, shape per node type (cusp, smooth, symmetric), show curve direction, fill unselected nodes, color scheme Default or Custom with main and secondary colors, show highlight, node types in colors; rendered by the node overlay with a `NodeStyle` record.
  - Type: select type by path only, font names in English, recent fonts count (consumer: the font list of `D02 T10 §3`).
  - Ctrl and Shift convention: Nodus default (Shift constrains, Alt from center per `standards/nodus.md`) or CorelDRAW convention, consumed by `ToolBase` modifier mapping.
  - Tool pages: Rectangle, Ellipse (ellipse, pie, arc, angles, direction), Spiral, Graph Paper defaults read by those tools on creation.
  - Save Settings as Default writes the current document's units, grid, guides, and nudge to the new-document defaults consumed by `D02 T07 §14`.
  - Reset Preferences restores every key on the page (or all) to defaults, applied on OK and logged.
  - Legacy new document dialog key is consumed by `D02 T07 §14`.
  - Tests: `PreferencesCoverageTests` enumerate every key on these pages and assert a control, a default, and a consumer reference; `ModifierConventionTests`; `NodeStyleTests`.
- **Proof:** Unit test plus driven run: `PreferencesCoverageTests` fail if a key lacks a consumer, and a driven change of the node size shows larger handles in a capture and in `settings.json`; cheaper substitute that fails: a settings page whose values nothing reads, which the coverage test catches.

#### §5. Preferences: files, backup, performance, GPU, and warnings

- **Deliverable:** Preferences for file handling (recovery interval and folder, recovery off for complex documents, save and export in the background, recent files count, format filters), backup (back up original, auto-backup interval and location), file and content locations with a missing-folder indicator, scratch and working folders, performance (GPU rendering and memory, animated zoom, undo levels, real-time drawing), warnings and message settings, and the startup action.
- **Depends On:** §4
- **Phase:** 13
- **Surface:** UI. Fidelity: extends the Preferences dialog -- docs/captures/nodus/preferences/. Job: a user can control where Nodus writes, how it recovers, how it performs, and which warnings it shows. Treatment: pages File Handling, Backup, Locations, Performance, Warnings, Startup, each key with a default and a named consumer; background save shows progress and cancel in the status strip. Cheaper substitute that fails: background save that blocks the UI thread. Chrome: consume the settings store, the atomic writer, recovery of `D02 T04 §5`, and the suite history's limit of `D01 T02 §4`.
- **Runs:** `Requires: display-session -- background save progress and warnings are driven runs`
- **Catalog:** NP-2699 to NP-2716 (18 features)
- **Hints:**
  - File handling keys: `nodus.recovery.enabled`, `.intervalMinutes`, `.folder`, `.skipAboveElements` (default 50,000 elements), `nodus.save.background`, `nodus.export.background`, `nodus.recent.count` (consumer: Open Recent of `D02 T04 §5`).
  - Background save and export: `BackgroundSaveService` serializes a document snapshot on the UI thread then writes on a worker through the atomic writer, with status-strip progress and Cancel; editing continues; a 10,000-object document saves without a frame longer than 100 ms.
  - Backup: `nodus.backup.originalBeforeSave` (writes `backup_of_<name>.svg`), `nodus.backup.autoIntervalMinutes` (Never, 5 to 60), `nodus.backup.folder`, consumed by the save path of `D02 T07 §14`.
  - Locations: content folders (brushes, symbols, swatches, templates, fonts) with Change, Reset, and a missing-folder badge naming the path and the fix; scratch folder; working folder for Open and Save dialogs.
  - Import and export filters: order and enable each registered format reader and writer, Reset to Default.
  - Performance: `nodus.render.gpu` (on when a supported GPU is found), `nodus.render.gpuMemoryMb`, `nodus.view.animatedZoom` (consumer: zoom of `D02 T07 §12`), `nodus.history.levels` (consumer: `D01 T02 §4`, default 100), `nodus.edit.realtimeDrawing`.
  - Warnings: every dismissable warning registers a `WarningId`; the Warnings page lists them with checkboxes and Reset All; Help, Message Settings opens the page.
  - Startup: action Welcome screen, New document, Open, New from template, Nothing (consumer: §7), and show New Document dialog (consumer: `D02 T07 §14`).
  - Tests: `BackgroundSaveServiceTests` (snapshot isolation, cancel leaves the old file intact), `WarningRegistryTests`, `ContentFolderTests` (missing folder flagged).
- **Proof:** Unit test plus driven run: `BackgroundSaveServiceTests` prove a cancelled save leaves the previous file byte-identical, and a driven save of a 10,000-object fixture logs progress while the UI keeps responding; cheaper substitute that fails: a synchronous save behind a spinner.

#### §6. UI appearance, scaling, and diagnostics

- **Deliverable:** UI theme and brightness, canvas and desktop color, window border color, UI and cursor scaling, large tabs and documents as tabs, auto-collapse panels, centered dialogs, Windows 11 window conventions, the appearance page, system information, safe mode, GPU compatibility check and GPU choice, the error-reporting toggle, a local-only privacy statement, and a startup time budget.
- **Depends On:** §4
- **Phase:** 13
- **Surface:** UI. Fidelity: Nodus main window -- docs/captures/nodus/main-window/, with brightness and scale captures under docs/captures/nodus/appearance/. Job: a user can make Nodus comfortable on their display and diagnose problems locally. Treatment: an Appearance page (brightness Dark, Medium Dark, Medium Light, Light; canvas color match or white; desktop and border colors; UI scale 100 to 200 percent; cursor scale; large tabs; center dialogs) and Help, System Information and Help, Restart in Safe Mode. Cheaper substitute that fails: theme switching that needs a restart or leaves hardcoded colors. Chrome: consume the suite theme of `D01 T01 §3` (brightness variants as additional token dictionaries), the exception window of `D01 T01 §2`, and `DebugInfoService`; do not keep `CatppuccinThemes`.
- **Runs:** `Requires: display-session -- brightness and scaling captures need an interactive desktop`
- **Catalog:** NP-2608 to NP-2623 (16 features)
- **Hints:**
  - `src/Photon.UI/Themes/Photon.Light.xaml`, `Photon.MediumLight.xaml`, `Photon.MediumDark.xaml` beside `Photon.Dark.xaml` with every token of `standards/shared.md`; `ThemeService.Apply(brightness)` swaps the merged dictionary live; `ThemeTokensTests` extended to all four.
  - Canvas and desktop color keys `nodus.view.canvasColor` (MatchUI or White or custom) and `nodus.view.desktopColor` consumed by `SkiaRenderer` for the area outside artboards; window border color applied through `DwmSetWindowAttribute(DWMWA_BORDER_COLOR)`.
  - UI scaling via a root `LayoutTransform` bound to `nodus.ui.scale` layered over per-monitor DPI; cursor scaling picks 32 or 48 px cursor assets.
  - Windows 11: rounded corners and Mica through `DWMWA_WINDOW_CORNER_PREFERENCE` and `DWMWA_SYSTEMBACKDROP_TYPE`, snap layouts by keeping the standard maximize button hit-test (`WM_NCHITTEST` returning `HTMAXBUTTON`).
  - Center dialogs: `nodus.ui.centerDialogs` or remember last position per dialog.
  - Refreshed icons: active tool highlight token; every tool icon from the catalog.
  - System information dialog: OS, .NET, GPU and driver, displays and DPI, printers, loaded assemblies with versions, settings folder; Copy and Save as TXT.
  - Safe mode: `--safe-mode` or holding Shift at startup disables GPU rendering, custom workspaces, and user fonts beyond system fonts, and writes a report of what was disabled.
  - GPU check: `GpuDiagnostics` probes SkiaSharp GPU context creation, reports adapter and result, and sets `nodus.render.gpu` accordingly; hardware acceleration page picks the adapter.
  - Error reporting toggle `photon.errors.showDialog` consumed by the exception window; privacy page states no telemetry is sent.
  - Startup budget: time to interactive window under 1.5 s on the reference machine, logged by `PerformanceMetricsService` at each start and asserted in a perf test with a recorded baseline.
  - Tests: `ThemeServiceTests`, `SystemInfoReportTests`, `SafeModeTests`, `StartupBudgetTests`.
- **Proof:** Unit test plus driven run: `ThemeTokensTests` pass for all four brightness dictionaries and captures at 100 and 200 percent in Light and Dark are committed; cheaper substitute that fails: a light theme with hardcoded dark literals, which the token test and capture reveal.

#### §7. The welcome screen and the navigator

- **Deliverable:** A welcome screen (new from preset, open, recent files with thumbnails, the quick start guide, discover topics, AI entries, show when no documents are open, show or hide) and a Navigator panel with a live thumbnail and a draggable viewport rectangle, promoting backlog B-013 (`legacy-nodus-5.8-5.9`).
- **Depends On:** D02 T07 §14
- **Phase:** 13
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/welcome/ and docs/captures/nodus/navigator/. Job: a user can start or resume work in one click, and move around a large document without zooming out. Treatment: a welcome tab in the document area with New (presets from `D02 T07 §14`), Open, Recent (thumbnails, pin, remove), Quick Start, Discover, and AI entries (`D02 T15 §2`); a Navigator panel with a thumbnail, a viewport rectangle to drag, a zoom slider, artboards-only option, and view box color, plus the corner pop-up navigator. Cheaper substitute that fails: a static splash image or a navigator that renders a stale thumbnail. Chrome: consume recent files of `D02 T04 §5`, presets of `D02 T07 §14`, `SkiaRenderer` for thumbnails, and the dock; do not write a second renderer.
- **Runs:** `Requires: display-session -- welcome and navigator captures need an interactive desktop`
- **Catalog:** NP-2624 to NP-2628 (5 features)
- **Hints:**
  - Promote B-013: delete its line from `todo/backlog.md` and add the `-> SOURCE: legacy-nodus-5.8-5.9` line to this section in the same commit.
  - `Photon.Nodus.Desktop/Views/WelcomeView.xaml` with `WelcomeViewModel` shown as a document tab when no document is open (`nodus.welcome.showWhenEmpty`, default true) and from Help, Welcome Screen.
  - Recent files with thumbnails rendered by `SkiaRenderer` into a cache under `%LOCALAPPDATA%\Rizonesoft\Nodus\thumbs\`, invalidated by file timestamp; missing files shown struck with Remove.
  - Quick Start opens the local `docs/user/nodus/quick-start.md` rendered in a help viewer; Discover lists local topic cards and quick actions (for example Trace an image, Make a pattern).
  - Startup action from §5 decides whether the welcome tab opens at launch.
  - `NavigatorPanel.xaml`: thumbnail re-rendered at most every 200 ms from document change events at a 256 px budget, viewport rectangle drag pans, zoom slider bound to canvas zoom, artboards-only toggle, `nodus.navigator.boxColor`.
  - Corner pop-up navigator on the canvas scroll corner (click and hold to jump).
  - Performance: navigator refresh on a 10,000-object document stays under 16 ms per frame by rendering from a cached picture.
  - Tests: `WelcomeViewModelTests` (recent list, missing file, presets), `NavigatorViewModelTests` (rectangle to viewport mapping at several zooms).
- **Proof:** Unit test plus driven run: `NavigatorViewModelTests` prove dragging the rectangle maps to the exact canvas pan at 25, 100, and 400 percent, and captures of both surfaces are committed; cheaper substitute that fails: a navigator that only scrolls, which the mapping test fails.

#### §8. Pen, touch, and Surface Dial input

- **Deliverable:** Pen input with pressure, tilt, and bearing through WPF stylus (Real-Time Stylus), pressure calibration and presets, a Devices preferences page, touch gestures (pinch zoom, two-finger pan and rotate), the Touch workspace UI, tablet mode auto-switch, and Surface Dial support.
- **Depends On:** §4
- **Phase:** 13
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/touch/ and docs/captures/nodus/devices/. Job: a designer can draw with a pen and navigate by touch or Dial on a tablet. Treatment: stylus pressure reaching the brush and pen tools, a calibration page with a sample stroke, gestures that zoom around the pinch center, and a Touch workspace with larger controls and an undo, redo, copy, paste, delete strip. Cheaper substitute that fails: treating the pen as a mouse. Chrome: consume the workspace presets of §1, the tools, and the settings store.
- **Runs:** `Requires: display-session -- pen, touch, and Dial are driven on a pen-enabled Windows device`
- **Catalog:** NP-2629 to NP-2635 (7 features)
- **Hints:**
  - `SkiaCanvas` handles `StylusDown`, `StylusMove`, `StylusUp` with `StylusPointCollection` properties `NormalPressure`, `XTiltOrientation`, `YTiltOrientation`, and `TwistOrientation` where the device reports them, feeding a `PenSample` record to tools; WinTab is not supported and the page says so.
  - Pressure curve: `PressureCurve` (min, max, gamma) calibrated from a sample stroke on the Devices page; presets saved as named curves in settings.
  - Stylus eraser end switches to the eraser tool while inverted (`Stylus.Inverted`).
  - Touch: `IsManipulationEnabled` on the canvas, `ManipulationDelta` scale around the pinch center, translation pans, rotation rotates the view (consumer: rotate view of `D02 T07 §12`), tap-and-hold opens flyouts.
  - Touch workspace UI: the §1 Touch preset with 1.5x controls, reduced toolbox, and the action strip in the status bar.
  - Tablet mode: detect with `UIViewSettings.UserInteractionMode` (Touch or Mouse) and switch to the workspace chosen per mode (`nodus.devices.tabletWorkspace`, `nodus.devices.desktopWorkspace`).
  - Surface Dial: `RadialController` through `IRadialControllerInterop.CreateForWindow` with menu items Zoom, Rotate View, Undo and Redo, Brush Size, Opacity; rotation steps change the value, click commits.
  - Tests: `PressureCurveTests`, `PenSampleMappingTests`, `ManipulationMathTests` (zoom around center), `DialMenuTests` with a fake controller.
- **Proof:** Unit test plus driven run: `ManipulationMathTests` prove pinch zoom keeps the pinch center fixed in document space, and a driven pen stroke logs pressure values varying across the stroke; cheaper substitute that fails: mouse-promoted stylus input, which reports constant pressure.

#### §9. Hints, in-app learning, and the project timer

- **Deliverable:** A Hints panel with context hints per tool and back and forward navigation, tooltips and rich tooltips, the Illustrator and CorelDRAW terminology map, and a project timer with tasks, editing, reset, CSV and TXT export, automatic start, inactivity detection and prompt, pause rules, and toolbar appearance.
- **Depends On:** §1
- **Phase:** 13
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/hints/ and docs/captures/nodus/project-timer/. Job: a user can learn the active tool in place, and track time spent per task on a document. Treatment: a Hints panel that follows the active tool with a short description, modifiers, and a Learn more link into the user guide; a Project Timer toolbar (Track button, task name, elapsed) and panel. Cheaper substitute that fails: hints that are static text not following the tool, or a timer that counts idle time. Chrome: consume the tool manager, the user guide under `docs/user/nodus/`, the Help menu of `D02 T05 §3`, and the toolbar model of §2.
- **Runs:** `Requires: display-session -- hints and timer captures need an interactive desktop`
- **Catalog:** NP-2636 to NP-2646 (11 features)
- **Hints:**
  - Hints content: `Photon.Nodus.Desktop/Help/hints/<toolId>.md` per tool, loaded by `HintsService` on tool change with Back and Forward history; a test asserts every registered tool has a hint file.
  - Tooltips: `nodus.ui.showTooltips` and `nodus.ui.richTooltips` (description plus gesture plus an animated or static example image); tooltips read command names and gestures from the keymap.
  - Terminology map: `docs/user/nodus/terminology.md` table (anchor point and node, clipping mask and PowerClip, smart guides and dynamic guides, panel and docker, stroke and outline) linked from Help and searchable in the command palette.
  - `Photon.Nodus.Core/Timer/ProjectTimer.cs` with tasks (add, activate, rename, reorder, delete, edit recorded time and dates, reset counter) stored per document in `nodus:timer` metadata so time travels with the file, plus a global task list option.
  - Automatic start on open, create, or task activation; pause when minimized, when another document is focused, or while the panel is open (each a setting).
  - Inactivity: tolerance minutes (default 5); on return an Inactivity Detected dialog to discard, keep, or log a custom number of minutes, with Remember my choice.
  - Export time sheet as CSV (task, start, end, duration) or TXT through the atomic writer.
  - Toolbar appearance: show Track button, task name, timer (settings).
  - Tests: `HintsCoverageTests`, `ProjectTimerTests` with a fake clock (idle discard, pause rules), `TimeSheetExportTests` against a golden CSV.
- **Proof:** Unit test: `ProjectTimerTests` with a fake clock prove idle time is excluded under Discard and included under Keep, and `TimeSheetExportTests` match the golden CSV; cheaper substitute that fails: a wall-clock timer, which the idle test fails.

#### §10. Object data, the Object Data Manager, and find and replace objects

- **Deliverable:** An Object Data panel (field editor, formats, copy data from, clear), the Object Data Manager spreadsheet (levels, summarize groups, hierarchy, totals, print), a Find and Replace objects panel (query builder, from selection, names or styles, find next, previous, all, all on page, save and load criteria, replace properties, search range), and the Document Info panel.
- **Depends On:** D02 T07 §5
- **Phase:** 13
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/object-data/, docs/captures/nodus/find-replace/, and docs/captures/nodus/document-info/. Job: a designer can attach data to objects, total it, and find or batch-change objects by their properties. Treatment: an Object Data panel with typed fields, a spreadsheet manager with group subtotals, and a Find and Replace panel whose queries select results on canvas and whose Replace is one undoable step. Cheaper substitute that fails: find by name only, or data stored outside the document. Chrome: consume the Objects panel tree and names of `D02 T07 §5`, the selection owner, the history, and the print path.
- **Runs:** `Requires: display-session -- panel captures and the printed summary are driven runs`
- **Catalog:** NP-2719 to NP-2738 (20 features)
- **Hints:**
  - Object data model: `ObjectDataField` (name, type General, DateTime, Linear, Angular, Numeric, format string) and per-element values persisted as `nodus:data-*` attributes per `D02 T07 §1`; field definitions stored in the document with an application default set in settings.
  - Object Data panel: edit values of the selection, Copy Data From (append from a picked object), Clear All Fields; every change an undoable `SetObjectDataCommand`.
  - Object Data Manager: a `DataGrid` over all or selected objects with Show Levels (group depth), Summarize Groups, Show Hierarchy, Show Totals for numeric fields, Export CSV, and Print through `PrintDialog` with page setup.
  - Find model: `ObjectQuery` (type, fill, stroke, effect, name, style name, text content predicates) composed in a query builder dialog; From Selection builds a query from every property of the selected object.
  - Find Next, Previous, All, All on Page; search range Selection, Current artboard, All artboards, listed artboards.
  - Save and load criteria as `.nodusquery` JSON.
  - Replace: color (exact or by color model or palette), stroke properties, text properties on all matches as one `CompositeCommand`.
  - Document Info panel: document settings, object counts by type, styles, brushes, spot colors, patterns, gradients, fonts, linked and embedded images; selection only toggle; Save as TXT.
  - Performance: Find All on a 10,000-object document under 200 ms.
  - Tests: `ObjectDataTests` (round trip through SVG fixture `tests/fixtures/nodus/object-data/fields.svg`), `ObjectQueryTests`, `ReplaceObjectsTests` (one undo step), `DocumentInfoReportTests`.
- **Proof:** Format fidelity proof plus unit test: the object-data fixture round-trips every field and format element by element, and `ReplaceObjectsTests` undo in one step; cheaper substitute that fails: data kept in app memory, lost on reopen.

#### §11. QR codes and barcodes

- **Deliverable:** Insert QR code (URL, email, phone, SMS, vCard or meCard, calendar event, geo, plain text) as a live vector object with pixel fill, background, outline, margin, pixel shape and fill factor, welded pixels, roundness, error correction, styles and defaults; an Insert Barcode wizard (EAN, UPC, Code 128, Code 39, ITF, and more); and local validation of QR codes and barcodes by decoding.
- **Depends On:** D02 T09 §1
- **Phase:** 13
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/nodus/qr-code/ and docs/captures/nodus/barcode/. Job: a designer can place a scannable, styled QR code or barcode that stays editable. Treatment: Object, Insert, QR Code creates a live QR object edited in the Properties panel; Object, Insert, Barcode opens a wizard; Validate decodes the rendered result locally. Cheaper substitute that fails: an embedded bitmap QR code or one that needs a sign-in. Chrome: consume the live-object contract of `D02 T07 §1`, the color model of `D02 T09 §1`, object styles, and the Properties panel of `D02 T07 §8`.
- **Runs:** `Requires: display-session -- Properties panel captures need an interactive desktop`
- **Catalog:** NP-2739 to NP-2750 (12 features)
- **Hints:**
  - Package decision: ZXing.Net (Apache-2.0) for encoding the module matrix and for decoding, recorded in `docs/dev/decisions.md`; Nodus draws the vector geometry itself.
  - `Photon.Nodus.Core/Codes/QrCodeObject.cs` live object: content type and fields, error correction L, M, Q, H, margin in modules, pixel shape (square, circle, diamond, star, rounded), fill factor percent, roundness, weld adjacent modules (union through `SKPath.Op`), pixel fill, background fill, pixel outline; finder markers stay square for scannability.
  - Content encoders: `QrPayload` builders for URL, `mailto:`, `tel:`, `SMSTO:`, vCard 3.0 and MECARD, iCalendar `VEVENT`, `geo:` URI, and plain text, each unit tested against the expected string.
  - Persistence per `D02 T07 §1`: parameters in `nodus:qr-*`, expanded paths as the SVG fallback, restored live on reopen.
  - Styles and defaults: QR objects accept object styles and a document default QR style.
  - Barcode wizard: symbology (EAN-13, EAN-8, UPC-A, UPC-E, Code 128, Code 39, ITF-14, Codabar), data with check digit validation, bar height, human-readable text font and size, quiet zone; produces a live barcode object with vector bars and live text.
  - Validate: renders the object at 300 DPI to a bitmap and decodes it with ZXing.Net; reports the decoded text and whether it matches, for Nodus codes and for any selected code artwork; no network use.
  - Tests: `QrPayloadTests`, `QrCodeObjectTests` (decode round trip for every pixel shape at fill factor 60 to 100 and error correction H), `BarcodeTests` (check digits, decode round trip), fidelity fixture `tests/fixtures/nodus/codes/qr-live.svg`.
- **Proof:** Unit test plus format fidelity proof: every styled QR and barcode fixture decodes back to its payload with ZXing.Net, and `qr-live.svg` reopens as a live QR object with identical parameters; cheaper substitute that fails: a raster QR image, which reopens as a plain image and fails the live-object check.

#### Sizing concerns

- `D02 T16 §4` carries 41 catalog features (50 inventory rows); they are single settings keys, so the hints group them by page (General, Selection and Anchors, Nodes and Handles, Type, Tools, switcher) to fit 30 items, but the coverage table of keys and consumers is long; if review finds it past 30 items, the Tools default pages are the natural split.
- `D02 T16 §2` carries 27 features (45 rows) covering toolbox, toolbars, property bar, and status bar; it fits only because all bars share one `CommandBarDefinition` model; the status bar is the split candidate if needed.
- `D02 T15 §2` carries 13 features including turntable and new document from a prompt; it is dense but cohesive around one schema and applier.

### todo/02-nodus/TODO-17-nodus-parity-releases.md -- `nodus-parity-releases`

- **Title:** "TODO-17 -- Nodus Parity Releases: 0.2.0 to 1.0.0"
- **Phase(s):** 4 to 13 (one section per phase, each the last row of its phase)
- **Goal:** Each parity phase ends in a real, independently installable Nodus release: every section of the phase stamped, every catalog row the phase plans reconciled against its section's stamp, the changelog and user guide current, the installer proven on a clean machine, and a `nodus-v*` tag whose GitHub release carries verified assets; `nodus-v1.0.0` declares parity with the catalog complete.
- **Current-state facts to verify (with claim candidates):**
  - The release checklist the sections run is `standards/release.md`. `<!-- claim: exists standards/release.md -->`
  - The previous release section is `D02 T05 §4` (Nodus 0.1.0); no `nodus-v*` tag exists yet. `<!-- claim: exists todo/02-nodus/TODO-05-nodus-release.md -->`
  - The catalog the releases reconcile exists. `<!-- claim: exists docs/parity/nodus-parity.md -->`
- **Inputs and XREFs:** `standards/release.md`; `CHANGELOG.md`; `docs/parity/nodus-parity.md`; -> XREF: D02 T05 §4 (the 0.1.0 release procedure these repeat); -> XREF: D05 T01 §1 (clean-machine procedure); -> XREF: D00 T01 §6 (the parity query each release quotes); -> XREF: D06 T01 §1 (the Nodus user guide each release extends).
- **Adjacency:** list=not-applicable (a release section adds no browsable records); document=not-applicable (the printed and exported documents are owned by D02 T13 and D02 T14; a release only re-proves them on the installed build); settings=not-applicable (no new settings); reporting=applicable (each release quotes the parity query's per-phase counts); notifications=not-applicable (no long operation of its own); permissions=not-applicable (nothing written but release assets); audit=applicable (the changelog and the tag are the audit); exchange=applicable (each release opens its phase's fidelity fixtures on the installed build); reverse=not-applicable (a release reverses nothing; a bad release is superseded by the next patch tag)

#### §1. Nodus 0.2.0

- **Deliverable:** `nodus-v0.2.0`: Phase 4 (document model, pages, layers, selection, and view) released, every Phase 4 section stamped and its catalog rows reconciled
- **Depends On:** D02 T05 §4, D02 T06 §7, D02 T07 §1, D02 T07 §2, D02 T07 §3, D02 T07 §4, D02 T07 §5, D02 T07 §6, D02 T07 §7, D02 T07 §8, D02 T07 §9, D02 T07 §10, D02 T07 §11, D02 T07 §12, D02 T07 §13, D02 T07 §14
- **Phase:** 4
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 4`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 4 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.2.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 4 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 4 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.2.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.2.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.2.0.
  - Commit: `"release: Nodus 0.2.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.2.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 4 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §2. Nodus 0.3.0

- **Deliverable:** `nodus-v0.3.0`: Phase 5 (drawing, paths, shapes, shaping, and transform) released, every Phase 5 section stamped and its catalog rows reconciled
- **Depends On:** §1, D02 T06 §2, D02 T08 §1, D02 T08 §2, D02 T08 §3, D02 T08 §4, D02 T08 §5, D02 T08 §6, D02 T08 §7, D02 T08 §8, D02 T08 §9, D02 T08 §10, D02 T08 §11, D02 T08 §12, D02 T08 §13, D02 T08 §14, D02 T08 §15
- **Phase:** 5
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 5`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 5 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.3.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 5 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 5 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.3.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.3.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.3.0.
  - Commit: `"release: Nodus 0.3.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.3.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 5 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §3. Nodus 0.4.0

- **Deliverable:** `nodus-v0.4.0`: Phase 6 (color, fills, strokes, brushes, transparency, styles, and symbols) released, every Phase 6 section stamped and its catalog rows reconciled
- **Depends On:** §2, D02 T06 §11, D01 T04 §1, D01 T04 §2, D02 T09 §1, D02 T09 §2, D02 T09 §3, D02 T09 §4, D02 T09 §5, D02 T09 §6, D02 T09 §7, D02 T09 §8, D02 T09 §9, D02 T09 §10, D02 T09 §11, D02 T09 §12, D02 T09 §13, D02 T09 §14, D02 T09 §15, D02 T09 §16, D02 T09 §17, D02 T09 §18, D02 T09 §19, D02 T09 §20, D02 T09 §21, D02 T09 §22
- **Phase:** 6
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 6`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 6 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.4.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 6 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 6 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.4.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.4.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.4.0.
  - Commit: `"release: Nodus 0.4.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.4.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 6 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §4. Nodus 0.5.0

- **Deliverable:** `nodus-v0.5.0`: Phase 7 (type, tables, and graphs) released, every Phase 7 section stamped and its catalog rows reconciled
- **Depends On:** §3, D02 T06 §3, D02 T10 §1, D02 T10 §2, D02 T10 §3, D02 T10 §4, D02 T10 §5, D02 T10 §6, D02 T10 §7, D02 T10 §8, D02 T10 §9, D02 T10 §10, D02 T10 §11, D02 T10 §12, D02 T10 §13, D02 T10 §14, D02 T10 §15
- **Phase:** 7
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 7`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 7 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.5.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 7 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 7 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.5.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.5.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.5.0.
  - Commit: `"release: Nodus 0.5.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.5.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 7 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §5. Nodus 0.6.0

- **Deliverable:** `nodus-v0.6.0`: Phase 8 (interactive and live effects) released, every Phase 8 section stamped and its catalog rows reconciled
- **Depends On:** §4, D02 T11 §1, D02 T11 §2, D02 T11 §3, D02 T11 §4, D02 T11 §5, D02 T11 §6, D02 T11 §7, D02 T11 §8, D02 T11 §9, D02 T11 §10, D02 T11 §11, D02 T11 §12, D02 T11 §13, D02 T11 §14, D02 T11 §15, D02 T11 §16, D02 T11 §17, D02 T11 §18, D02 T11 §19
- **Phase:** 8
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 8`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 8 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.6.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 8 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 8 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.6.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.6.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.6.0.
  - Commit: `"release: Nodus 0.6.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.6.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 8 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §6. Nodus 0.7.0

- **Deliverable:** `nodus-v0.7.0`: Phase 9 (bitmaps, tracing, and raster effects) released, every Phase 9 section stamped and its catalog rows reconciled
- **Depends On:** §5, D02 T06 §14, D01 T03 §1, D01 T03 §2, D01 T03 §3, D01 T03 §4, D01 T03 §5, D01 T03 §6, D01 T03 §7, D01 T03 §8, D01 T03 §9, D01 T03 §10, D01 T03 §11, D02 T12 §1, D02 T12 §2, D02 T12 §3, D02 T12 §4, D02 T12 §5, D02 T12 §6, D02 T12 §7, D02 T12 §8
- **Phase:** 9
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 9`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 9 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.7.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 9 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 9 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.7.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.7.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.7.0.
  - Commit: `"release: Nodus 0.7.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.7.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 9 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §7. Nodus 0.8.0

- **Deliverable:** `nodus-v0.8.0`: Phase 10 (color management, print, prepress, and PDF) released, every Phase 10 section stamped and its catalog rows reconciled
- **Depends On:** §6, D01 T04 §3, D02 T13 §1, D02 T13 §2, D02 T13 §3, D02 T13 §4, D02 T13 §5, D02 T13 §6, D02 T13 §7, D02 T13 §8, D02 T13 §9, D02 T13 §10, D02 T13 §11, D02 T13 §12, D02 T13 §13, D02 T13 §14, D02 T13 §15, D02 T13 §16
- **Phase:** 10
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 10`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 10 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.8.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 10 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 10 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.8.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.8.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.8.0.
  - Commit: `"release: Nodus 0.8.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.8.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 10 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §8. Nodus 0.9.0

- **Deliverable:** `nodus-v0.9.0`: Phase 11 (file formats, export, and web) released, every Phase 11 section stamped and its catalog rows reconciled
- **Depends On:** §7, D02 T14 §1, D02 T14 §2, D02 T14 §3, D02 T14 §4, D02 T14 §5, D02 T14 §6, D02 T14 §7, D02 T14 §8, D02 T14 §9, D02 T14 §10, D02 T14 §11, D02 T14 §12, D02 T14 §13, D02 T14 §14, D02 T14 §15, D02 T14 §16, D02 T14 §17, D02 T14 §18, D02 T14 §19
- **Phase:** 11
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 11`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 11 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.9.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 11 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 11 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.9.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.9.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.9.0.
  - Commit: `"release: Nodus 0.9.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.9.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 11 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §9. Nodus 0.10.0

- **Deliverable:** `nodus-v0.10.0`: Phase 12 (Nodus AI) released, every Phase 12 section stamped and its catalog rows reconciled
- **Depends On:** §8, D01 T05 §1, D01 T05 §2, D01 T05 §3, D01 T05 §4, D01 T05 §5, D02 T15 §1, D02 T15 §2, D02 T15 §3, D02 T15 §4, D02 T15 §5, D02 T15 §6, D02 T15 §7, D02 T15 §8, D02 T15 §9, D02 T15 §10, D02 T15 §11
- **Phase:** 12
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 12`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 12 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v0.10.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 12 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 12 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 0.10.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Push the tag `nodus-v0.10.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 0.10.0.
  - Commit: `"release: Nodus 0.10.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v0.10.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 12 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.

#### §10. Nodus 1.0.0

- **Deliverable:** `nodus-v1.0.0`: Phase 13 (workspace, customization, and preferences, completing parity) released, every Phase 13 section stamped and its catalog rows reconciled
- **Depends On:** §9, D02 T06 §12, D02 T06 §13, D02 T06 §17, D02 T16 §1, D02 T16 §2, D02 T16 §3, D02 T16 §4, D02 T16 §5, D02 T16 §6, D02 T16 §7, D02 T16 §8, D02 T16 §9, D02 T16 §10, D02 T16 §11
- **Phase:** 13
- **Surface:** no surface of its own (it releases the surfaces its phase built)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)`; `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** no catalog rows of its own (infrastructure the planned features build on)
- **Hints:**
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every row `PASS`.
  - Run the parity query from `D00 T01 §6` (`python scripts/todo-graph.py query parity --phase 13`) and quote it: every catalog row whose status is `plan <ref>` for a Phase 13 section resolves to a stamped section; a row that cannot ship is rerouted in the catalog (to a later section, or to the backlog through `add-todo`) in this commit with its reason, never left pointing at an unshipped section.
  - Write the `nodus-v1.0.0` section of `CHANGELOG.md` (Added, Changed, Fixed) from the Phase 13 sections' commits, naming the catalog `NP-` ranges shipped.
  - Confirm the Nodus user guide (`docs/user/nodus/`) has a page for every surface Phase 13 added (each UI section's documentation duty) and that the Help menu links resolve.
  - Build `pwsh scripts/package.ps1 -App Nodus -Version 1.0.0` and run the clean-machine procedure (`D05 T01 §1`): install per-user and all-users, upgrade over the previous `nodus-v*` release keeping settings, launch, open this phase's fidelity fixtures, save, reopen, uninstall.
  - Open a document saved by this release in the previous release and record how the live objects this phase added degrade there (expanded fallback geometry per `D02 T07 §1`, never a lost element).
  - Parity completion: `query parity` reports zero `plan` rows whose section is unshipped across Phases 4 to 13; `README.md` states that Nodus covers the Illustrator 30.8 and CorelDRAW 2026 parity catalog and links the excluded and backlog rows.
  - Record the query output as the evidence of the acceptance-bar aim "Nodus covers every CorelDRAW and Illustrator capability in the parity catalog".
  - Push the tag `nodus-v1.0.0`; the `release` workflow run is `success` (URL quoted); download the assets and verify `SHA256SUMS`; run the portable ZIP from an empty folder.
  - Update `README.md`'s Nodus status line to 1.0.0.
  - Commit: `"release: Nodus 1.0.0"`.
- **Proof:** driven run on the clean machine plus `gh release view nodus-v1.0.0 --json isPrerelease,assets` (three assets, not prerelease) and the Phase 13 parity query output; cheaper substitute that fails: tagging from a developer machine without the clean-machine run, or with catalog rows still pointing at unshipped sections.
