# Gesso Parity -- Section Design

> **Integrated 2026-09-26.** This file is the record of the design as it stood that day; where the integration deviated (the one filter element name `<gesso:filter kind=...>`, extra dependency edges, notes on existing sections, reciprocal XREFs), the TODO files under `todo/` carry the change with a `**Corrected 2026-09-26:**` note and are the plan. The "Decisions for the operator to confirm at integration" were answered on 2026-09-27: libjpeg-turbo, SharpCompress, FluentFTP, Vortice.Windows, OpenCvSharp4, and the `Isotone.Gesso.ShellThumbnails` project were approved (recorded in `D03 T17 §11`, `D03 T17 §12`, `D03 T15 §4`, `D03 T15 §5`, and `D03 T20 §5`), and reverse engineering Affinity files was declined, so B-045 stays in the backlog.

The authoring blueprint for the TODO files that bring Gesso to parity with Adobe Photoshop 27.10 (with Camera Raw 18.6), Affinity by Canva 3.3 (Affinity Photo), and GIMP 3.2.6, written 2026-09-26 from the unified catalog in [`gesso-parity.md`](gesso-parity.md). It follows the structure of the Stilus design, [`section-design.md`](section-design.md), which is the precedent for every rule below. Agents who author the TODO files follow this document; the integration commit wires what they write into `todo/`. Nothing here is a section yet: sections exist only once authored under `todo/` and placed in `todo/implementation-plan.md`.

## Summary

- **Operator decisions (2026-09-26):** "now, imago, all the photoshop and at least 2 other similar popular programs of the same type. All features without leaving anything behind." The programs are Photoshop, Affinity Photo, and GIMP 3. Budget raise approved in the operator's words: "New Imago parity phases, up to +250", placed after Gesso 0.1.0 (today's Phase 15) and before Albumen's foundation (today's Phase 16). Video and animation, and macros and scripting, are deferred to after the first release, not excluded; macros and scripting become one suite-wide system for Stilus, Gesso, and Albumen. Cloud and collaboration are excluded.
- **Sources:** 3,176 Photoshop rows (`PS-A-0001` to `PS-A-1750`, `PS-B-0001` to `PS-B-1426`), 2,762 Affinity rows (`AF-0001` to `AF-2762`), and 4,891 GIMP rows (`GP-0001` to `GP-4891`), 10,829 in all.
- **Catalog:** 2,367 features (`IP-0001` to `IP-2367`), every source id in exactly one row (checked, see "Catalog check" below). GIMP lists one row per documented option, so 4,891 GIMP rows fold into far fewer features; the catalog is coarser per source row than the Stilus one (0.22 features per source row against 0.65).
- **New sections:** 175 (174 in the twelve new Gesso parity phases, including 12 release sections, plus `D00 T01 §7` in Phase 0), in 16 new TODO files and one existing file. Three existing sections (`D03 T07 §3`, `§16`, `§17`) move into the parity phases without changing address; `D03 T07 §11` stays where it is.
- **Budget:** the twelve new phases take 201 sections of ceiling; no phase leaves the plan and the renumbered phases keep their ceilings, so the net raise is +201, inside the approved +250; the total ceiling goes from 354 to 555.

### Catalog features by status

| Status | Features | Source rows | Detail |
| ------ | -------: | ----------: | ------ |
| `plan` | 1,997 | 9,541 | owned by 161 new sections |
| `shipped-scope` | 204 | 762 | owned by 28 existing sections |
| `backlog` | 100 | 377 | B-012 5, B-024 3, B-041 33, B-042 9, B-043 14, B-044 20, B-045 1, B-046 10, B-047 5 |
| `excluded` | 54 | 129 | cloud 29, platform 14, removed 11 |
| `other-app` | 12 | 20 | Albumen 4, Stilus 4, none 4 |
| **Total** | **2,367** | **10,829** | |

### Catalog features by category

| Category | Features |
| -------- | -------: |
| core | 1,869 |
| format | 163 |
| ai | 135 |
| automation | 75 |
| print | 51 |
| video | 37 |
| cloud | 27 |
| 3d | 10 |

### New sections per phase

| Phase | Title | New sections | Relocated rows | Section total | Ceiling | Planned features |
| ---: | ----- | ---: | ---: | ---: | ---: | ---: |
| 16 | Gesso parity I: document, canvas, view, history, and layers | 19 | 0 | 19 | 21 | 293 |
| 17 | Gesso parity II: selection, channels, styles, smart objects, and artboards | 18 | 0 | 18 | 20 | 201 |
| 18 | Gesso parity III: adjustment layers, adjustments, modes, and color | 11 | 0 | 11 | 13 | 160 |
| 19 | Gesso parity IV: the brush engine, painting, fills, gradients, and patterns | 12 | 0 | 12 | 14 | 152 |
| 20 | Gesso parity V: retouching, content-aware tools, transform, warp, and liquify | 12 | 0 | 12 | 14 | 96 |
| 21 | Gesso parity VI: filters I, the filter surfaces and the engine extensions for blur, sharpen, noise, distort, and pixelate | 15 | 1 | 16 | 18 | 163 |
| 22 | Gesso parity VII: filters II, render, light, stylize, artistic, generic, and GEGL | 11 | 0 | 11 | 13 | 138 |
| 23 | Gesso parity VIII: the develop engine, Camera Raw, HDR, panorama, stacks, and astrophotography | 19 | 0 | 19 | 21 | 174 |
| 24 | Gesso parity IX: type, paths, shapes, and vectors | 9 | 0 | 9 | 10 | 120 |
| 25 | Gesso parity X: formats, export, color management, and print | 22 | 0 | 22 | 25 | 263 |
| 26 | Gesso AI: editable, suite-aware, reproducible | 16 | 0 | 16 | 18 | 114 |
| 27 | Gesso parity XI: workspace, customization, preferences, and Gesso 1.0.0 | 10 | 2 | 12 | 14 | 123 |
| **16-27** | | **174** | **3** | **177** | **201** | **1,997** |

Plus `D00 T01 §7` (the Gesso catalog in the validator) in Phase 0, which has room (14 of 15), so the new-section total is 175.

### New files

| File | Frontmatter id | Phases | Sections | Planned features | Batch |
| ---- | -------------- | ------ | ---: | ---: | :---: |
| `todo/00-workspace/TODO-01-dev-automation.md` (existing, new `§7`) | `dev-automation` | 0 | 1 | 0 | A |
| `todo/01-core/TODO-06-isotone-imaging-extensions.md` | `isotone-imaging-extensions` | 21, 22 | 14 | 201 | C |
| `todo/01-core/TODO-07-isotone-develop.md` | `isotone-develop` | 23 | 6 | 51 | D |
| `todo/03-gesso/TODO-08-gesso-parity-document.md` | `gesso-parity-document` | 16 | 11 | 191 | A |
| `todo/03-gesso/TODO-09-gesso-parity-layers.md` | `gesso-parity-layers` | 16, 17 | 14 | 193 | A |
| `todo/03-gesso/TODO-10-gesso-parity-selection.md` | `gesso-parity-selection` | 17 | 10 | 110 | B |
| `todo/03-gesso/TODO-11-gesso-parity-adjustments.md` | `gesso-parity-adjustments` | 18 | 10 | 160 | B |
| `todo/03-gesso/TODO-12-gesso-parity-painting.md` | `gesso-parity-painting` | 19 | 11 | 152 | B |
| `todo/03-gesso/TODO-13-gesso-parity-retouch.md` | `gesso-parity-retouch` | 20 | 11 | 96 | C |
| `todo/03-gesso/TODO-14-gesso-parity-filters.md` | `gesso-parity-filters` | 21, 22 | 10 | 100 | C |
| `todo/03-gesso/TODO-15-gesso-parity-photo.md` | `gesso-parity-photo` | 23 | 12 | 123 | E |
| `todo/03-gesso/TODO-16-gesso-parity-type-vector.md` | `gesso-parity-type-vector` | 24 | 8 | 120 | D |
| `todo/03-gesso/TODO-17-gesso-parity-formats.md` | `gesso-parity-formats` | 25 | 14 | 157 | D |
| `todo/03-gesso/TODO-18-gesso-parity-output.md` | `gesso-parity-output` | 25 | 7 | 106 | D |
| `todo/03-gesso/TODO-19-gesso-ai.md` | `gesso-ai` | 26 | 15 | 114 | E |
| `todo/03-gesso/TODO-20-gesso-parity-workspace.md` | `gesso-parity-workspace` | 27 | 9 | 123 | E |
| `todo/03-gesso/TODO-21-gesso-parity-releases.md` | `gesso-parity-releases` | 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27 | 12 | 0 | A |

## How to use this blueprint

- Author one file at a time through `create-todo` (the skill's template, frontmatter, Goal, Current state with claims, Inputs, Outcome with the Adjacency line, Implementation Order, sections, Verification), taking the file's frontmatter id and title, its Goal, its Current-state facts, and every section below exactly as numbered, titled, and ordered.
- Each section's **Hints** are the concrete items it must implement; expand them into micro-steps (one action, a named path, Done when, the cheaper substitute on UI and write items, a source cite) under the 30-item cap, add the `Commit:` item, and write the **Proof** as the Test checkpoint. A section that cannot hold its hints in 30 items is split at authoring time only with the phase's spare ceiling; otherwise its lowest-value catalog rows move to the backlog through `add-todo` and the catalog is updated in the same commit.
- Each section's **Catalog** line lists the `IP-` features it owns. The authored section names those ranges in its context paragraph ("Catalog: IP-0123 to IP-0150") so the catalog, the section, and the validator agree.
- UI sections carry `Fidelity:`, `Job:`, `Treatment:`, and `Chrome:` (`todo/README.md`, "The second layer the runner reads"); library sections say "no surface of its own". Sections that drive the app carry `**Requires:** display-session -- <reason>`; release sections carry `**Needs:** Clean Windows machine (no .NET SDK)`.
- A section that promotes a backlog entry carries that entry's source key as its `-> SOURCE:` line (see "Backlog changes"); the integration commit deletes the entry.
- Cross-file edges: `Depends On` always uses full refs. Where a section's Inputs name another file's section with `-> XREF:`, the integration commit adds the reciprocal line in the target file (one-sided XREFs are FATAL).

## Recorded decisions

### Names and paths

Every Gesso parity section runs after `D03 T01 §1` (Phase 1) renames Gesso to `Isotone.Gesso.*` and after Gesso 0.1.0 (`D03 T06 §3`, Phase 15), so hints and checklist items name the target paths: `src/Gesso/Isotone.Gesso.Core/`, `src/Gesso/Isotone.Gesso.Rendering/`, `src/Gesso/Isotone.Gesso.FileFormats/`, `src/Gesso/Isotone.Gesso.Desktop/`, `tests/Isotone.Gesso.Core.Tests/`, `tests/Isotone.Gesso.Rendering.Tests/`, `src/Isotone.Core/`, `src/Isotone.UI/`, `tests/Isotone.Core.Tests/`. Current-state blocks, by contrast, cite today's `src/Gesso/src/Gesso.*` paths, because a `<!-- claim: -->` must hold on the day the file is authored; `D03 T01 §1`'s claim-rewrite item moves them with the rename. If a file is authored after the rename has shipped, its claims use the new paths directly. New Gesso projects are not created, with one recorded exception: the Explorer thumbnail and preview handler (`D03 T20 §5`) is a separate COM in-process project, `Isotone.Gesso.ShellThumbnails`, because Windows loads shell extensions into Explorer and they must not load the app. Otherwise, photo merges live in `Isotone.Gesso.Core/Photo/`, AI in `Isotone.Gesso.Core/AI/` and `Isotone.Gesso.Desktop/AI/`, formats in `Isotone.Gesso.FileFormats/<Format>/`.

### The native format stays the OpenRaster layout

`D03 T04 §4` makes `.gesso` a ZIP on the OpenRaster layout with a Gesso extension namespace. Parity adds document content OpenRaster cannot express (adjustment and fill layers, layer styles, smart objects and linked layers, live and smart filters, text and shape layers, layer comps, artboards, channels, paths, guides, slices, snapshots, AI provenance). `D03 T08 §1` defines one contract for all of it: parameters in the `gesso:` namespace of `stack.xml` beside a rendered PNG for every non-raster layer, so GIMP and Krita open any `.gesso` renamed to `.ora` with every layer visible as pixels, and Gesso restores the live layer when its parameters are present. Every later section that adds a layer kind or document part registers its element and its fallback with that contract; none invents a second container.

### What goes to Isotone.Core and Isotone.UI

The rule in `AGENTS.md` is that shared code moves to `Isotone.Core` only when two apps need it now. The Stilus parity plan built the suite engines first (`D01 T03` pixel engine, `D01 T04` color management, `D01 T05` AI core) with Gesso as their planned second consumer, so the Gesso parity plan consumes them and never grows a second copy:

- **The pixel engine** (`D01 T03`): every effect it already implements appears in Gesso's Filter menu through `D03 T14 §2` with no new algorithm code; the catalog marks those features `shipped-scope D01 T03 §N`. Algorithms Gesso adds (GIMP and GEGL filters, Photoshop and Affinity filters the engine lacks) go into the same `Isotone.Core/Imaging/Effects/` registry through the new `D01 T06` (engine extensions), so Stilus's effect gallery sees them too and there is still one registry.
- **Color management** (`D01 T04`): Gesso's color settings, assign and convert, proofing, and modes (`D03 T18 §4`, `§5`, `D03 T11 §7`) consume it; backlog B-023 is promoted into `D03 T18 §4`.
- **The AI core** (`D01 T05`): Gesso's AI (`D03 T19`) consumes the client, key store, send gate, provenance record, and brand kit; nothing in `D03 T19` talks HTTP.
- **The develop engine** (new `D01 T07`, `Isotone.Core/Develop/`): Photoshop's Camera Raw filter and Affinity's Develop studio need the same scene-referred pipeline Albumen's develop module plans (`D04 T02 §2`), and Gesso's parity phases run before Albumen, so the engine is built once in `Isotone.Core` with Gesso as its first consumer and Albumen as its planned second. The integration commit rewrites `D04 T02 §2` to consume `D01 T07 §1` to `§3` rather than build its own pipeline, and rewords Albumen backlog entries B-028 to B-031 to consume `D01 T07 §3` and `§4`.
- **Code that moves out of Stilus on its second consumer** (each move is the first checklist item of the Gesso section named, never a copy): the HarfBuzz text engine `D02 T10 §1` to `Isotone.Core/Text/` (`D03 T16 §1`, promoting B-018); path geometry and boolean operations from `D02 T08 §10` to `Isotone.Core/Vector/` (`D03 T16 §5`; `D03 T16 §7` promotes B-019); the SVG document reader to `Isotone.Core/Vector/Svg/` (`D03 T16 §5`, which imports SVG paths in Phase 24) and its renderer (`D03 T17 §7`, SVG import as pixels); the PSD writer of `D02 T14 §13` beside the reader `D03 T04 §5` already moved (`D03 T17 §2`); the PDF writer of `D02 T13 §14` to `Isotone.Core/Pdf/` (`D03 T17 §7`); the Ghostscript runner of `D02 T14 §9` to `Isotone.Core/Formats/PostScript/` (`D03 T17 §7`); the print dialog frame of `D02 T13 §2` to `Isotone.UI/Print/` (`D03 T18 §6`, promoting B-021); the workspace, toolbar, menu, and shortcut-set frames of `D02 T16 §1` to `§3` to `Isotone.UI/Workspace/` (`D03 T20 §1` to `§3`); the palette file readers of `D02 T09 §4` to `Isotone.Core/Color/Palettes/` (`D03 T11 §10`). The design pass found more of the same kind, each the first item of the section named: units and the snapping core of `D02 T07 §9` and `§11` (`D03 T08 §4`); the gradient model of `D02 T09 §7` to `Isotone.Core/Paint/Gradients/` (`D03 T09 §8`); the links manager of `D02 T12 §7` (`D03 T09 §10`); the align math of `D02 T08 §14` (`D03 T09 §12`); the color harmony engine of `D02 T09 §5` (`D03 T11 §9`) and the Duotone dialog of `D01 T04 §3` to `Isotone.UI` (`D03 T11 §7`); the warp and mesh math of `D02 T11 §5` (`D03 T13 §6`); the metafile reader of `D02 T14 §11`, the web encoder of `§16`, the slice model and image-map writer of `§17`, and WIA acquisition of `§19` (`D03 T17 §7`, `§12`, `D03 T18 §2`, `§3`); printer's marks, separations, preflight, the PostScript writer, PDF presets, and PDF security of `D02 T13 §4`, `§5`, `§9`, `§10`, `§15`, `§16` (`D03 T17 §7`, `D03 T18 §6`, `§7`); the font matcher of `D02 T15 §7` (`D03 T19 §11`); the preference-key and warning registries, pressure curves and the Dial menu, the welcome screen, system-info and GPU diagnostics, UI-scale helpers, and the contextual task bar host of `D02 T16` (`D03 T20 §1`, `§4`, `§6`, `§8`, `§9`). New shared pieces Gesso is the first to need are built in `Isotone.Core` where a second consumer is already planned: the lens database reader (`D03 T14 §6`, consumed by `D01 T07 §3`), the expression compiler for Apply Image equations (`D03 T11 §8`, extended by `D01 T06 §9`), the FFT (`D03 T08 §11`), and the distance transform (`D03 T09 §14`).
- **Stays in Gesso** with the day it would move: photo merges and alignment (`Isotone.Gesso.Core/Photo/`, moves when Albumen's backlog B-032 is promoted), the content-aware engine (`Isotone.Gesso.Core/Retouch/`), the brush engine (`Isotone.Gesso.Core/Painting/`, never needed by Stilus's vector brushes), the segmentation engine (`Isotone.Gesso.Core/Selection/Segmentation/`, moves when Albumen's local masks B-028 need subject masks).

### Formats and licensing

Every dependency is checked against GPL-3.0 in the section that adds it, with a `docs/dev/decisions.md` row.

| Need | Decision | License | Why |
| ---- | -------- | ------- | --- |
| Photoshop PSD and PSB read and write | Own code in `Isotone.Core/Formats/Psd/` against Adobe's Photoshop File Formats Specification, extending the Stilus reader and writer (`D02 T14 §13`, moved by `D03 T04 §5`) (`D03 T17 §2`, `§3`); psd-tools (MIT, Python) and GIMP 3.2 as reading oracles; opening in Photoshop itself is an operator check recorded as a risk, not a gate | Own code | Full layer, style, adjustment, text, and smart-object fidelity needs the private blocks no library writes |
| GIMP XCF read and write | Own reader and writer from GIMP's published `devel-docs/XCF.md`, GIMP 3.2 `gimp-console` batch export as the golden oracle (`D03 T17 §4`) | Own code; GIMP is GPL-3.0-or-later, so translated logic is compatible | XCF is fully documented and GIMP is the oracle; this also serves Stilus's backlog B-038 |
| Affinity `.af` and `.afphoto` | Not planned: backlog B-045. No public specification, no maintained open reader, and a binary container whose reverse engineering would need an operator decision on the EULA; the interop path is Affinity's own PSD export, which `D03 T17 §3` reads with layers, masks, and adjustments | Proprietary | An honest reader cannot be proven against a specification or an open oracle |
| WebP | libwebp (through SkiaSharp's bundled codec for decode and basic encode, libwebp P/Invoke for alpha quality, presets, and metadata) (`D03 T17 §5`) | BSD-3-Clause | Already shipped inside SkiaSharp |
| AVIF | libavif with dav1d (decode) and libaom (encode) (`D03 T17 §5`) | BSD-2-Clause (AOM patent license for libaom) | Reference implementation |
| HEIF and HEIC | libheif with libde265 (decode) and x265 or kvazaar (encode), native per RID; the WIC HEIF extension recorded as the alternative (`D03 T17 §5`) | LGPL-3.0 (libheif, libde265), GPL-2.0-or-later (x265), BSD-3-Clause (kvazaar); all compatible with GPL-3.0; HEVC patent exposure recorded | The WIC path needs a Store extension many machines lack |
| JPEG XL | libjxl (`D03 T17 §5`) | BSD-3-Clause | Reference implementation |
| JPEG 2000 | OpenJPEG (`D03 T17 §5`) | BSD-2-Clause | Reference implementation |
| OpenEXR | OpenEXR 3 and Imath, native per RID (`D03 T17 §6`) | BSD-3-Clause | Every compression and deep-data variant a managed port would miss |
| Radiance HDR, PFM, PAM and PNM, QOI, farbfeld, XBM, XPM, XWD, SGI, Sun raster, WBMP, ICO, CUR, ANI, IFF ILBM, Pixar, Scitex CT, DCS, HGT, CEL, Paint Shop Pro, FITS, Photoshop Raw | Own managed codecs from each format's published description (`D03 T17 §6`, `§8`, `§9`); TGA and PCX reuse Stilus's own codecs moved to `Isotone.Core` | Own code | Small, documented formats; no dependency is worth its weight |
| DDS | BCnEncoder.Net for BC1 to BC7 (`D03 T17 §8`) | MIT | Managed and complete |
| DICOM | Own reader for the uncompressed and JPEG transfer syntaxes of DICOM PS3.5 (`D03 T17 §6`) | Own code | fo-dicom is MS-PL, which the FSF lists as incompatible with the GPL |
| PDF import (pages as pixels) | PDFium through a thin P/Invoke wrapper (`D03 T17 §7`) | BSD-3-Clause and Apache-2.0 | Gesso needs the reference rasterizer; Stilus's PdfPig path builds vector objects, a different job |
| Photoshop PDF and EPS write | The PDFsharp writer of `D02 T13 §14` moved to `Isotone.Core/Pdf/`; own EPS writer with TIFF preview (`D03 T17 §7`) | MIT | One PDF writer for the suite |
| EPS and PostScript read | User-installed Ghostscript run as an external process, never bundled, refused by name when absent (`D03 T17 §7`), the runner moved from `D02 T14 §9` | Ghostscript is AGPL-3.0 | Bundling would pull AGPL terms into the installer |
| Lens profiles | The lensfun database and user-supplied Adobe LCP files read by own code in `Isotone.Core/Lens/` (no lensfun library), attribution in About; built by `D03 T14 §6`, consumed by `D01 T07 §3` | Data CC BY-SA 3.0 | The only open lens database |
| Image alignment and stitching | OpenCV 4 through OpenCvSharp4, scoped to `Isotone.Gesso.Core/Photo/` (features, homographies, seam finding, multi-band blending) (`D03 T15 §5`) | Apache-2.0 (both), compatible with GPL-3.0 | Robust feature matching and stitching are years of work; pixel filters stay in the managed engine |
| Content-aware fill | Own PatchMatch search and texture synthesis after Barnes et al. 2009 and the resynthesizer plug-in (GPL-3.0-or-later) as reference; the patent check recorded in the decision row (`D03 T13 §3`) | Own code | No library fits the tile store; the algorithm is published |
| OpenColorIO configs | OpenColorIO 2, native per RID (`D03 T11 §4`, `D03 T18 §4`) | BSD-3-Clause | Affinity's OCIO adjustment and configurations |
| MyPaint brushes | libmypaint through P/Invoke, native per RID (`D03 T12 §4`) | ISC | The brush engine MyPaint brush files describe |
| Text shaping | HarfBuzzSharp through the engine `D02 T10 §1` moved to `Isotone.Core/Text/` (`D03 T16 §1`) | MIT | One text engine for the suite |
| JPEG encoding options | libjpeg-turbo 3.1 through P/Invoke for arithmetic coding, restart markers, DCT method, and scan scripts the WIC encoder lacks (`D03 T17 §11`) | IJG, BSD-3-Clause, and zlib | The reference encoder GIMP uses |
| Compressed archives and remote files | SharpCompress for gz, bz2, xz, and zip; FluentFTP for ftp locations; `HttpClient` for http and https (`D03 T17 §12`) | MIT (both) | GIMP opens from archives and URLs |
| HDR display output | Vortice.Windows (DXGI and Direct3D 11 swap chain in advanced color) hosted beside the WPF canvas, SDR tone-mapped preview otherwise (`D03 T15 §4`) | MIT | WPF has no HDR output path |
| Scanner and screenshot | Windows Image Acquisition 2.0 and Windows.Graphics.Capture (`D03 T17 §1`) | Part of Windows | No package |
| Color management | lcms2 through `D01 T04` | MIT | Shared engine |
| AI | OpenRouter over `D01 T05` | MIT (.NET) | Shared client |
| Presets, content, and color books | Not bundled: no Adobe or Affinity brushes, gradients, styles, patterns, skies, LUT packs, PANTONE books, or frames; users import the files they own (ABR, GRD, ASL, PAT, CSH, ACO, ASE, ACB, afbrushes, CUBE) | Proprietary | Redistribution is not licensed |

### AI: Gesso's own, built on three pillars

The Photoshop, Affinity, Canva, and GIMP plug-in AI rows are mapped to the Gesso feature that does the same job; none is cloned. The runtime is OpenRouter with the user's own key (BYOK) through `D01 T05`, model choice per task in settings (a vision model for locating and describing, an image-generation model for pixels), nothing sent without an explicit user action and a send preview.

- **Editable, structured output, never destructive.** A generation lands as a new pixel layer with a layer mask inside a named group ("Generative Fill: <prompt>"), each variation a hidden sibling layer; an AI selection lands as a selection or a layer mask; an AI edit from the assistant lands as adjustment layers, masks, and filter layers built from JSON validated against a schema. Every apply is one named undoable command and no source pixel is overwritten (`D03 T19 §2`, `§3`, `§6`, `§10`).
- **Image generation through OpenRouter, with honest limits.** Generative fill, expand, remove, background, and upscale send a masked crop with context padding to an image model and composite the result through the mask with a feathered seam and a color match (`D03 T19 §2`). Model output sizes are capped, so large regions are tiled and upscaling beyond the model's size is tiled with overlap; not every model honors a seed, so provenance records whether the seed was honored and a re-run may differ; there is no depth sensor, so depth blur uses an estimated depth from a vision model's layered description plus the subject mask, and says so; faces and identities are never sent unless the user includes them in the region, and smart-portrait edits carry a caution in the send preview.
- **Selections by locating, not by guessing pixels.** Vision models are good at finding objects and poor at pixel-exact masks, so `D03 T19 §6` asks the model for boxes, points, and labels as JSON and the local segmentation engine (`D03 T10 §6`: GrabCut, guided-filter matting) turns them into the mask. The same engine serves the classical Quick Selection and Focus Area, and works with no network at all.
- **Suite-aware.** The brand kit (palettes, logos, type styles) from `D01 T05 §5` is read by Gesso's swatches and AI prompts; the pipeline Albumen photo to Gesso cleanup to Stilus trace runs over files through `D02 T15 §11`'s `SuiteAppLocator`, offered only when the other app is installed (`D03 T19 §13`).
- **Explainable and reproducible.** Every AI action writes a provenance record (prompt, model, parameters, seed and whether it was honored, input and output hashes, cost) into the `.gesso` document; the provenance panel re-runs, compares, and reverts (`D03 T19 §1`). Exported files can carry the record as XMP; signed Content Credentials (C2PA) are backlog B-047.

Local algorithms the inventories tag as AI stay local: content-aware fill, move, and scale (`D03 T13 §3`), Focus Area and the matting engine (`D03 T10 §6`), classical denoise and JPEG artifact removal (`D01 T03 §6`, `D01 T06 §5`), auto tone and auto color (`D03 T11 §2`). On-device model inference (ONNX segmentation, inpainting, upscaling) is backlog B-046, so every AI feature has one implementation today.

### Out of scope, deferred, and other apps

- **Cloud and collaboration** (`excluded: cloud`): cloud documents and version history, Creative Cloud and Canva libraries, Share for Review and comments, invite to edit, Adobe Stock and Adobe Express hand-offs, Adobe Fonts activation, Firefly web features, the Photoshop web and iPad apps, Behance, cloud learning content, and account services. Rows tagged `cloud` whose job is local stay planned (local libraries of brushes, swatches, and styles in `D03 T20 §7`).
- **Removed by the vendor** (`excluded: removed`): Photoshop's legacy 3D (removed in 2023; its menu rows are listed only as removed) and Digimarc. Nothing a current version ships is excluded this way.
- **Platform** (`excluded: platform`): macOS-only and Linux-only items (Touch Bar, X11 and Wayland specifics, Linux input devices).
- **Deferred to after the first release** (operator decision 2026-09-26, not excluded): one suite-wide scripting and macro system for Stilus, Gesso, and Albumen (B-041, which absorbs Gesso's B-025), suite-wide batch processing and droplets (B-042), video layers and the timeline (B-043), and frame animation with animated GIF, APNG, WebP, and MNG authoring (B-044). Their catalog rows carry `backlog B-NNN`, and the Stilus catalog's former `excluded: automation` rows now point at B-041 and B-042.
- **Kept in the backlog**: third-party 8BF plug-in hosting, reworded suite-wide (B-012); Gesso's own plug-in assemblies (B-024); Affinity file import (B-045); on-device models (B-046); Content Credentials signing (B-047).
- **Other apps** (`other-app`): Bridge-style browsing, catalogs, and photo downloading map to Albumen; Affinity's vector, layout, and typography studios where they lay out pages rather than edit pixels map to Stilus; third-party products map to none.

### The legacy roadmap file (D03 T07): relocated, not superseded

`D03 T07` holds four sections that 0.1.0 code already points at: `D03 T05 §3`'s disabled filter tooltips name `§3`, `D04 T01` cross-references `§11`, and the acceptance bar names `§16`. Superseding them would break those owners. They stay at their addresses, the catalog marks their features `shipped-scope`, the parity sections extend them through `Depends On`, and the integration commit moves three of the four plan rows into the parity phases:

| Section | Moves to | Why there |
| ------- | -------- | --------- |
| `D03 T07 §3` The rest of the filter catalog | Phase 21 | The filter surfaces and engine extensions (`D03 T14`, `D01 T06`) extend it; it must run first |
| `D03 T07 §17` Workspaces, panels, and preferences | Phase 27 | The workspace and preference sections (`D03 T20 §1` to `§7`) extend it |
| `D03 T07 §16` Accessibility and localization | Phase 27, last before the release | Audits every surface once the parity surfaces exist |
| `D03 T07 §11` RAW import through the shared decoder | stays in its phase (old 19, new 31, and 41 since the Albumen integration of 2026-09-27) | It waits on Albumen's decoder (`D04 T01 §4`), which ships after the Gesso parity phases; the develop filter works on open layers until then |

The old Phase 19 keeps its ceiling of 5 with one row, as renumbered phases keep their ceilings; `D03 T07`'s Goal and Current state get one sentence recording the move, and `todo/03-gesso/INDEX.md` changes its phase line to "Phases 1, 14, 15, 16 to 27, and 31".

### Backlog changes

Promoted into parity sections (each promoted entry is deleted from `todo/backlog.md` in the commit that authors its section, which is the integration commit when the batches land together, and its source key rides the section's `-> SOURCE:` line):

| Entry | Source key | Promoted into |
| ----- | ---------- | ------------- |
| B-014 Adjustment layers | `legacy-gesso-5.1-adjustment-layers` | `D03 T11 §1` |
| B-015 Layer masks, clipping masks, and vector masks | `legacy-gesso-1.6` | `D03 T09 §3` |
| B-016 Layer styles | `legacy-gesso-5.8` | `D03 T09 §7` |
| B-017 Retouching tools | `legacy-gesso-4.6` | `D03 T13 §1` |
| B-018 Text layers | `legacy-gesso-4.8` | `D03 T16 §1` |
| B-019 Shape layers and vector tools | `legacy-gesso-4.7` | `D03 T16 §7` |
| B-020 The brush engine | `legacy-gesso-4.4` | `D03 T12 §1` |
| B-021 Print | `legacy-gesso-7.4` | `D03 T18 §6` |
| B-022 More formats: WebP, HEIC, EXR, GIF, PSD write | `legacy-gesso-7.2-7.3` | `D03 T17 §5` (EXR in `§6`, GIF in `§8`, PSD write in `§2`) |
| B-023 Color management and soft proofing | `legacy-gesso-1.3` | `D03 T18 §4` |
| B-027 Smart selection: magic wand, quick select, color range | `legacy-gesso-4.2-smart-selection` | `D03 T10 §3` |

Merged: **B-025** (Gesso scripting) is deleted and its content folded into the suite-wide B-041, which names it; its catalog rows point at B-041.

Kept: **B-024** (Gesso filter plug-in assemblies) stays as written; Gesso's plug-in manager rows point at it. **B-026** (Gesso performance) stays: no measured failure yet.

Reworded:

- **B-012** (third-party filter plug-in hosts) becomes suite-wide: "app: suite", summary naming Photoshop 8BF plug-ins in Stilus and Gesso (Affinity's Photoshop-plugin support is the same host), one isolated host process in `Isotone.Core`, `needs: D02 T12 §2, D03 T14 §2`. Photoshop and Affinity plug-in rows of the Gesso catalog point at it.
- **B-028** (Albumen local adjustments, `D01 T07 §4`), **B-029** (detail, `D01 T07 §3`), **B-030** (lens corrections, `D01 T07 §3`), **B-031** (color grading and HSL, `D01 T07 §2`): each summary says it consumes that `Isotone.Core/Develop/` section instead of building its own stage, and `needs` gains it. **B-033** (a GPU develop path) names `D01 T07 §1` as the CPU engine it accelerates.
- **B-032** (HDR and panorama merge in Albumen): consumes Gesso's alignment, HDR, and panorama engines (`D03 T15 §5`, `§6`, `§7`), which move from `Isotone.Gesso.Core/Photo/` to `Isotone.Core/Photo/` when the entry is promoted; `needs` gains `D03 T15 §7`.
- **B-038** (legacy raster formats in Stilus): "GIMP XCF" is removed from its list and the summary says Stilus reads XCF through Gesso's reader (`D03 T17 §4`) moved to `Isotone.Core` on promotion.

New entries (ids taken in order; drafts in the entry grammar):

```
- [B-041] Suite-wide scripting and macro recorder -- app: suite -- source: parity-suite-scripting -- added: 2026-09-26 -- summary: one scripting and macro system for Stilus, Gesso, and Albumen on a shared host in Isotone.Core: a documented object model per app, recorded actions and macros with playback and action sets, a scripts menu and console, plug-in and extension APIs, and external control (MCP); it covers Photoshop actions and scripts (UXP, ExtendScript), Affinity macros and scripting, GIMP Script-Fu, Python-Fu, consoles, and procedure browsers, CorelDRAW VBA and VSTA macros, and Illustrator actions and scripts, and absorbs Gesso's former B-025 -- needs: D05 T01 §6 -- why deferred: operator decision 2026-09-26 deferring macros and scripting to after the first release as one suite-wide system -- promote when: after the first release (operator 2026-09-26)
- [B-042] Suite-wide batch processing and droplets -- app: suite -- source: parity-suite-batch -- added: 2026-09-26 -- summary: batch processing of files and folders through recorded actions, droplets, the image processor, conditional actions, and data-driven graphics (variables and data sets) for Stilus, Gesso, and Albumen, built on B-041 -- needs: B-041 -- why deferred: operator decision 2026-09-26 deferring automation to after the first release -- promote when: after the first release (operator 2026-09-26), once B-041 has shipped
- [B-043] Video layers and the timeline -- app: gesso -- source: parity-gesso-video -- added: 2026-09-26 -- summary: video layers, the video timeline with keyframes, transitions, and audio, video frame import to layers, render video, and blur-gallery and clone-source behavior on video frames -- needs: D05 T01 §6 -- why deferred: operator decision 2026-09-26 deferring video and animation to after the first release -- promote when: after the first release (operator 2026-09-26)
- [B-044] Frame animation and animated formats -- app: gesso -- source: parity-gesso-animation -- added: 2026-09-26 -- summary: frame animation with onion skin and playback, GIMP Filters > Animation (blend, burn-in, rippling, spinning globe, waves, optimize, playback), and animated GIF, APNG, WebP, MNG, and FLI authoring with their frame options -- needs: D03 T17 §5 -- why deferred: operator decision 2026-09-26 deferring video and animation to after the first release -- promote when: after the first release (operator 2026-09-26)
- [B-045] Affinity .af and .afphoto import -- app: gesso -- source: parity-gesso-affinity-files -- added: 2026-09-26 -- summary: open Affinity by Canva (.af) and Affinity Photo 1 and 2 (.afphoto, .afdesign) documents with layers, masks, and adjustments -- needs: D03 T17 §3 -- why deferred: the format is proprietary and undocumented with no maintained open reader to prove against, and reverse engineering needs an operator decision on Canva's terms; Affinity's own PSD export (read with full fidelity by D03 T17 §3) is the interop path meanwhile -- promote when: Canva publishes a specification, an open reader appears that can serve as an oracle, or the operator approves a reverse-engineering effort
- [B-046] On-device machine-learning models -- app: suite -- source: parity-local-ml -- added: 2026-09-26 -- summary: optional local inference (ONNX Runtime) for segmentation, inpainting, upscaling, denoise, depth, and star separation, with a model manager for downloads and licenses, so AI features work offline beside their OpenRouter versions -- needs: D03 T19 §2 -- why deferred: every AI job already has one implementation through OpenRouter (D01 T05) or a classical algorithm; a second runtime and model licensing are a separate decision -- promote when: the operator asks for offline AI or an OpenRouter-only feature is shown to fail a user job
- [B-047] Content Credentials (C2PA) -- app: suite -- source: parity-c2pa -- added: 2026-09-26 -- summary: write and verify signed C2PA manifests carrying the suite provenance record in exported JPEG, PNG, TIFF, and PDF, with a signing certificate the user supplies -- needs: D03 T19 §13 -- why deferred: the provenance record is already embedded as XMP (D01 T05 §3, D03 T19 §13); signing needs a certificate decision and a C2PA library decision -- promote when: a user needs verifiable Content Credentials or the suite signing certificate (D99 T01 §3) exists
```

Backlog count after the integration: 28 minus 11 promoted minus 1 merged plus 7 new is 23, against the cap of 150.

### The Stilus catalog follows the same deferral

The operator's 2026-09-26 decision moves macros and scripting from excluded to deferred for the whole suite, so the Stilus catalog's eleven `excluded: automation` rows (`NP-2751` to `NP-2761`) now read `backlog B-041`, except batch processing (`NP-2754`), which reads `backlog B-042`; `stilus-parity.md` is updated in this change and its totals table says so. Cloud rows stay excluded. The Stilus design (`section-design.md`) keeps its original wording as the record of that day.

## Phase layout and renumbering

The twelve Gesso parity phases sit after Phase 15 (Gesso 0.1.0) and before the old Phase 16 (Albumen foundation). Each ends with a Gesso release section in `D03 T21`. Within a phase, rows run in the order listed, with the relocated `D03 T07` rows first where they move in (except `D03 T07 §16`, the accessibility audit, which runs last in Phase 27 so it covers every parity surface), and the release row last.

| Phase | Rows in order |
| ---: | ----- |
| 16 | `D03 T08 §1`, `D03 T08 §2`, `D03 T08 §3`, `D03 T08 §10`, `D03 T08 §4`, `D03 T08 §5`, `D03 T08 §11`, `D03 T08 §6`, `D03 T08 §7`, `D03 T08 §8`, `D03 T08 §9`, `D03 T09 §1`, `D03 T09 §2`, `D03 T09 §14`, `D03 T09 §3`, `D03 T09 §4`, `D03 T09 §5`, `D03 T09 §6`, `D03 T21 §1` |
| 17 | `D03 T10 §1`, `D03 T10 §2`, `D03 T10 §3`, `D03 T10 §4`, `D03 T10 §6`, `D03 T10 §5`, `D03 T10 §7`, `D03 T10 §8`, `D03 T10 §9`, `D03 T10 §10`, `D03 T09 §7`, `D03 T09 §8`, `D03 T09 §9`, `D03 T09 §10`, `D03 T09 §11`, `D03 T09 §12`, `D03 T09 §13`, `D03 T21 §2` |
| 18 | `D03 T11 §1`, `D03 T11 §2`, `D03 T11 §3`, `D03 T11 §4`, `D03 T11 §5`, `D03 T11 §6`, `D03 T11 §7`, `D03 T11 §8`, `D03 T11 §9`, `D03 T11 §10`, `D03 T21 §3` |
| 19 | `D03 T12 §1`, `D03 T12 §2`, `D03 T12 §3`, `D03 T12 §4`, `D03 T12 §5`, `D03 T12 §6`, `D03 T12 §7`, `D03 T12 §8`, `D03 T12 §9`, `D03 T12 §10`, `D03 T12 §11`, `D03 T21 §4` |
| 20 | `D03 T13 §1`, `D03 T13 §2`, `D03 T13 §3`, `D03 T13 §4`, `D03 T13 §5`, `D03 T13 §11`, `D03 T13 §6`, `D03 T13 §7`, `D03 T13 §8`, `D03 T13 §9`, `D03 T13 §10`, `D03 T21 §5` |
| 21 | `D03 T07 §3`, `D01 T06 §1`, `D01 T06 §2`, `D01 T06 §3`, `D01 T06 §4`, `D01 T06 §5`, `D01 T06 §6`, `D01 T06 §7`, `D01 T06 §14`, `D03 T14 §1`, `D03 T14 §2`, `D03 T14 §3`, `D03 T14 §4`, `D03 T14 §6`, `D03 T14 §7`, `D03 T21 §6` |
| 22 | `D01 T06 §8`, `D01 T06 §9`, `D01 T06 §10`, `D01 T06 §11`, `D01 T06 §12`, `D01 T06 §13`, `D03 T14 §5`, `D03 T14 §8`, `D03 T14 §9`, `D03 T14 §10`, `D03 T21 §7` |
| 23 | `D01 T07 §1`, `D01 T07 §2`, `D01 T07 §3`, `D01 T07 §4`, `D01 T07 §5`, `D01 T07 §6`, `D03 T15 §1`, `D03 T15 §12`, `D03 T15 §2`, `D03 T15 §4`, `D03 T15 §3`, `D03 T15 §5`, `D03 T15 §6`, `D03 T15 §7`, `D03 T15 §8`, `D03 T15 §9`, `D03 T15 §10`, `D03 T15 §11`, `D03 T21 §8` |
| 24 | `D03 T16 §1`, `D03 T16 §5`, `D03 T16 §2`, `D03 T16 §3`, `D03 T16 §4`, `D03 T16 §6`, `D03 T16 §7`, `D03 T16 §8`, `D03 T21 §9` |
| 25 | `D03 T17 §1`, `D03 T17 §12`, `D03 T17 §2`, `D03 T17 §13`, `D03 T17 §3`, `D03 T17 §4`, `D03 T17 §14`, `D03 T17 §5`, `D03 T17 §6`, `D03 T17 §7`, `D03 T17 §8`, `D03 T17 §9`, `D03 T17 §11`, `D03 T17 §10`, `D03 T18 §1`, `D03 T18 §2`, `D03 T18 §3`, `D03 T18 §4`, `D03 T18 §5`, `D03 T18 §6`, `D03 T18 §7`, `D03 T21 §10` |
| 26 | `D03 T19 §1`, `D03 T19 §2`, `D03 T19 §3`, `D03 T19 §4`, `D03 T19 §5`, `D03 T19 §6`, `D03 T19 §15`, `D03 T19 §7`, `D03 T19 §14`, `D03 T19 §8`, `D03 T19 §9`, `D03 T19 §10`, `D03 T19 §11`, `D03 T19 §12`, `D03 T19 §13`, `D03 T21 §11` |
| 27 | `D03 T07 §17`, `D03 T20 §1`, `D03 T20 §2`, `D03 T20 §3`, `D03 T20 §4`, `D03 T20 §9`, `D03 T20 §5`, `D03 T20 §6`, `D03 T20 §7`, `D03 T20 §8`, `D03 T07 §16`, `D03 T21 §12` |

**Renumbering of the existing phases:**

| Old | New | Title |
| --- | --- | ----- |
| 0 to 15 | 0 to 15 | unchanged |
| -- | 16 to 27 | the Gesso parity phases above |
| 16 | 28 | Albumen foundation: spine, catalog, import, RAW, library |
| 17 | 29 | Albumen 0.1.0: develop, export, Edit in Gesso, release |
| 18 | 30 | Distribution and the suite bundle |
| 19 | 31 | Gesso after 0.1.0: RAW import through the shared decoder (keeps `D03 T07 §11`; its other three rows move into Phases 21 and 27) |
| 20 | 32 | Albumen after 0.1.0: accessibility |
| 99 | 99 | Manual: operator-only steps |

Prose that names an old phase number (`todo/implementation-plan.md` headings and paragraphs, the domain `INDEX.md` phase lines, `todo/TODO-00-INDEX.md`, `AGENTS.md`) is updated in the same commit; no section ref changes. The old Phase 19 keeps its title prefix and gains one sentence saying three of its rows moved.

**Budget.** Each new phase's ceiling is its section count (new sections plus relocated rows) plus 10 percent rounded up, minimum one, the rule of the initial budget. Renumbered phases keep their ceilings; the old Phase 19 (new 31) keeps its ceiling of 5 with one row, as the operator's rule for renumbered phases says.

| Phase | Sections | Ceiling |
| ---: | ---: | ---: |
| 16 | 19 | 21 |
| 17 | 18 | 20 |
| 18 | 11 | 13 |
| 19 | 12 | 14 |
| 20 | 12 | 14 |
| 21 | 16 | 18 |
| 22 | 11 | 13 |
| 23 | 19 | 21 |
| 24 | 9 | 10 |
| 25 | 22 | 25 |
| 26 | 16 | 18 |
| 27 | 12 | 14 |
| **Sum** | **177** | **201** |

The net raise is 201, inside the approved +250; the total ceiling goes from 354 to 555. Sections in the plan after integration: 314 plus 175 new, 489, against 555.

The integration commit appends one history entry (the live values and the snapshot identical):

```json
{
  "date": "2026-09-26",
  "change": "Gesso parity: twelve new phases (16 to 27) for the Photoshop, Affinity Photo, and GIMP parity catalog, ceilings at each phase's section count plus 10 percent rounded up with a minimum of one (201 in all); D03 T07 §3, §16, and §17 move into Phases 21 and 27 while D03 T07 §11 stays; old Phases 16 to 20 become 28 to 32 with their ceilings unchanged. D00 T01 §7 joins Phase 0 within its ceiling. Net raise 201, total ceiling 555.",
  "reason": "Operator decision 2026-09-26: \"now, imago, all the photoshop and at least 2 other similar popular programs of the same type. All features without leaving anything behind.\" The programs chosen are Photoshop, Affinity Photo, and GIMP 3. Budget raise approved in the operator's words: \"New Imago parity phases, up to +250\".",
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
      "16": 21,
      "17": 20,
      "18": 13,
      "19": 14,
      "20": 14,
      "21": 18,
      "22": 13,
      "23": 21,
      "24": 10,
      "25": 25,
      "26": 18,
      "27": 14,
      "28": 10,
      "29": 13,
      "30": 9,
      "31": 5,
      "32": 2,
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
| Gesso covers every Photoshop, Affinity Photo, and GIMP capability in its parity catalog | `D00 T01 §7` (the catalog gate) · `D03 T21 §1`-`§12` (each release reconciles its phase) |
| Gesso round-trips Photoshop documents: PSD and PSB open and save with layers, masks, adjustments, styles, text, and smart objects live | `D03 T17 §2` · `D03 T17 §13` · `D03 T17 §3` |
| Gesso opens and saves GIMP's XCF | `D03 T17 §4` · `D03 T17 §14` |
| Editing stays non-destructive: adjustment layers, smart and live filters, masks, and linked content never overwrite pixels until the user applies | `D03 T08 §1` · `D03 T09 §3` · `D03 T09 §9` · `D03 T11 §1` · `D03 T14 §1` |
| AI results in Gesso are new layers and masks, undoable, and reproducible | `D03 T19 §1` · `D03 T19 §2` · `D03 T19 §3` · `D03 T19 §6` |

Existing rows gain owners: "Shared once, never copied" adds `D01 T06 §1` · `D01 T07 §1` · `D03 T16 §1` · `D03 T16 §5` · `D03 T17 §2` · `D03 T18 §6`; "Formats are proven, not assumed" adds `D03 T17 §2` · `D03 T17 §4` · `D03 T17 §5` · `D03 T17 §6`; "No dependency without a reason and a license" adds `D03 T15 §5` · `D03 T17 §5` · `D03 T17 §6` · `D03 T17 §7` · `D03 T12 §4`; "AI results are editable, undoable, and reproducible" adds `D03 T19 §1` · `D03 T19 §2`; "Nothing leaves the machine without an explicit user action" adds `D03 T19 §1`; "It works without a mouse or eyes" keeps `D03 T07 §16`, which now runs last in Phase 27.

## Authoring batches

Five disjoint file sets of roughly equal size, so five agents can author in parallel. Each batch writes only its own files; every `-> XREF:` it writes into another batch's file, or into an existing file, is listed in its report, and the integration commit adds the reciprocal lines, the index rows, the plan rows, the budget entry, the backlog changes, and the `D03 T07` relocation in one pass.

| Batch | Files | Sections | Subject |
| :---: | ----- | ---: | ------- |
| A | `TODO-08-gesso-parity-document.md`, `TODO-09-gesso-parity-layers.md`, `TODO-21-gesso-parity-releases.md`, `D00 T01 §7` | 38 | document, view, history, layers, masks, blending, styles, smart objects, the releases, and the catalog validator |
| B | `TODO-10-gesso-parity-selection.md`, `TODO-11-gesso-parity-adjustments.md`, `TODO-12-gesso-parity-painting.md` | 31 | selection, channels, adjustments, modes, color, the brush engine, fills, gradients, and patterns |
| C | `TODO-06-isotone-imaging-extensions.md`, `TODO-13-gesso-parity-retouch.md`, `TODO-14-gesso-parity-filters.md` | 35 | the pixel engine extensions, retouching, transform, warp, liquify, and the filter surfaces |
| D | `TODO-07-isotone-develop.md`, `TODO-16-gesso-parity-type-vector.md`, `TODO-17-gesso-parity-formats.md`, `TODO-18-gesso-parity-output.md` | 35 | the develop engine, type and vectors, every format, export, color management, and print |
| E | `TODO-15-gesso-parity-photo.md`, `TODO-19-gesso-ai.md`, `TODO-20-gesso-parity-workspace.md` | 36 | the Camera Raw filter and photo merges, Gesso AI, and the workspace |

## Integration commit checklist

- Author or collect the 16 new files and the new `D00 T01 §7`; list each file in its domain `INDEX.md` and in `todo/TODO-00-INDEX.md`.
- Add the twelve Gesso parity phases to `todo/implementation-plan.md` (heading, one paragraph, one table each, from "Phase paragraphs" below), move `D03 T07 §3`, `§17`, and `§16` into Phases 21 and 27, renumber the later phases (old 16 to 20 become 28 to 32), add `D00 T01 §7` to Phase 0, and add the acceptance-bar rows.
- Append the budget history entry and update the live ceilings; delete the eleven promoted backlog entries and B-025, reword B-012, B-028 to B-032, and B-038, and add B-041 to B-047.
- Rewrite `D04 T02 §2` (Albumen's develop pipeline) to consume `D01 T07 §1` to `§3` with a reciprocal XREF; its checklist keeps the Albumen-specific edit stack and output transform and drops the pipeline stages the engine now owns.
- Update `D03 T07`'s Goal and Current state for the relocation, add `D03 T20 §8` and `§9` to `D03 T07 §16`'s Depends On so the audit follows every parity surface, and change `todo/03-gesso/INDEX.md`'s phase line to "Phases 1, 14, 15, 16 to 27, and 31".
- Reciprocate every cross-file `-> XREF:` the batch reports list (including the Stilus sections whose code moves: `D02 T10 §1`, `D02 T08 §10`, `D02 T09 §4`, `D02 T13 §2`, `D02 T13 §14`, `D02 T14 §9`, `D02 T14 §13`, `D02 T16 §1`-`§3`, and the engines `D01 T03`, `D01 T04`, `D01 T05`).
- Update `docs/parity/README.md` if a status changes during authoring; the catalog and this design are committed with the integration.
- Run `python scripts/todo-graph.py validate`, `plan --sync`, `plan --check`, `query budget`, and `python scripts/todo-claims.py`; all clean.

## Phase paragraphs

### Phase 16 -- Gesso parity I: document, canvas, view, history, and layers

Parity starts where every later feature stands. This phase fixes how live content persists in `.gesso` (the `gesso:` namespace beside a rendered PNG fallback, so GIMP and Krita still open every file), completes the document model (8, 16, and 32-bit float, precision, pixel aspect), new-document presets and templates, every view (zoom, rotate, flip, screen modes, windows, view modes, display filters, the navigator), rulers, guides, grids, snapping, measurement, the info and histogram panels and scopes, snapshots and non-linear history, the Image menu, paste variants, and crop, then the layer model with every layer kind, the Layers panel and Layer menu, masks, clipping and vector masks, blending options with Blend If, and every blend mode the three competitors ship. It ends with `gesso-v0.2.0`.

### Phase 17 -- Gesso parity II: selection, channels, styles, smart objects, and artboards

With layers and masks in place, selection catches up: soft and saved selections, every marquee and lasso, the magic wand and selection by color, Color Range, the local segmentation engine and Focus Area, quick selection, foreground select and intelligent scissors, Select and Mask, modify and transform selection, and the Channels panel with spot channels and quick mask. The same phase finishes the layer stack's richer content: layer styles, embedded and linked smart objects, layer comps, align and distribute, and artboards. It ends with `gesso-v0.3.0`.

### Phase 18 -- Gesso parity III: adjustment layers, adjustments, modes, and color

Adjustments become non-destructive layers over the suite pixel engine: every tonal and color adjustment of Photoshop, Affinity, and the GIMP Colors menu, auto corrections, analysis, every image mode and bit depth through the suite color engine, channel operations with Apply Image and Calculations, the color panels, pickers, samplers, and swatches with palette files and color libraries from user files. It ends with `gesso-v0.4.0`.

### Phase 19 -- Gesso parity IV: the brush engine, painting, fills, gradients, and patterns

Painting is judged on its brush engine, so it gets its own phase: tips, smoothing, wet media, full dynamics, presets with ABR, Affinity, and GIMP brush import, MyPaint brushes, every painting tool, mixer and smudge, erasers, fill and stroke including GIMP's line-art fill, gradients with an on-canvas editor, patterns, and symmetry painting. It ends with `gesso-v0.5.0`.

### Phase 20 -- Gesso parity V: retouching, content-aware tools, transform, warp, and liquify

Retouching builds on painting: clone and the clone source panel, healing, patch, blemish and inpainting, the content-aware engine for fill, scale, and move, toning tools, every transform tool of the three apps, warp, puppet warp and cage, perspective warp, Liquify, and frequency separation. It ends with `gesso-v0.6.0`.

### Phase 21 -- Gesso parity VI: filters I, the filter surfaces and the engine extensions for blur, sharpen, noise, distort, and pixelate

Filters come once the layer stack can host them non-destructively. The relocated filter-catalog section (`D03 T07 §3`) runs first, then `Isotone.Core` gains the engine extensions contract and the blur, lens-blur, sharpen, denoise, distort, map, and pixelate families, and Gesso gets smart filters and live filter layers, the Filter menu with generated dialogs for every engine effect, the Filter Gallery, the Blur Gallery surface, Lens Correction and Adaptive Wide Angle, and Vanishing Point. It ends with `gesso-v0.7.0`.

### Phase 22 -- Gesso parity VII: filters II, render, light, stylize, artistic, generic, and GEGL

The second filter phase completes the long tail GIMP and GEGL bring: light and shadow, procedural noise, patterns and fractals, edges and stylize, the artistic set, generic and morphology filters, the lighting and flare surfaces, the GEGL operation tool and filter browser, GIMP's decor and combine effects as native commands, and Affinity's filter extras. It ends with `gesso-v0.8.0`.

### Phase 23 -- Gesso parity VIII: the develop engine, Camera Raw, HDR, panorama, stacks, and astrophotography

Photography gets its own phase. `Isotone.Core` gains the scene-referred develop engine that Albumen will reuse, and Gesso gets the Camera Raw filter and Affinity's Develop studio with local masks, 32-bit editing and HDR display, tone mapping, the alignment engine, Merge to HDR, panoramas, image stacks and auto-blend, focus merge, astrophotography stacking, and splitting scanned photos. RAW files themselves open once Albumen's decoder is shared (`D03 T07 §11`, old Phase 19, new 31). It ends with `gesso-v0.9.0`.

### Phase 24 -- Gesso parity IX: type, paths, shapes, and vectors

Type and vectors come after the layer stack and styles they live in. The suite text engine moves from Stilus to `Isotone.Core` as Gesso becomes its second consumer, and Gesso gets text layers, character and paragraph formatting, OpenType and glyphs, styles and text commands, paths with geometry shared with Stilus, every pen and shape tool, vector layers, frames, and SVG output. It ends with `gesso-v0.10.0`.

### Phase 25 -- Gesso parity X: formats, export, color management, and print

Formats come after the document model they must carry is complete, so each reader and writer maps onto real Gesso content and owes a fidelity proof: the File menu, screenshots and scanners, PSD and PSB write with live content and full-fidelity read, XCF read and write, modern web formats, HDR and scientific formats, PDF, EPS, SVG, and metafiles, every common and legacy raster format, format options, and metadata; then export, Save for Web and slices, color settings and soft proofing, and print with its extras. It ends with `gesso-v0.11.0`.

### Phase 26 -- Gesso AI: editable, suite-aware, reproducible

The AI features are Gesso's own and come after the layers, masks, selections, retouching, and formats they produce and consume. On the shared AI core, Gesso maps every competitor AI job to a non-destructive, undoable, reproducible feature: the AI menu and provenance panel, the image-generation adapter, generative fill, remove, and expand, image generation, AI selection and masks, neural-filter equivalents, depth and relighting with honest limits, upscaling, distraction removal, the prompt-to-edit assistant, font matching and face landmarks, sky replacement, and the suite pipeline with the brand kit. It ends with `gesso-v0.12.0`.

### Phase 27 -- Gesso parity XI: workspace, customization, preferences, and Gesso 1.0.0

The last parity phase customizes and audits the whole surface once it exists: workspaces and Preferences (`D03 T07 §17`) move here first, then workspace presets, the toolbar and options bar, menus, shortcuts, and command search, every preference page, interface appearance and language, pen and touch input, the presets manager and resource libraries, help and diagnostics, and the accessibility and localization audit (`D03 T07 §16`) over every parity surface. It ends with `gesso-v1.0.0`, which declares the parity catalog complete.

## Integration notes from the design pass

Findings the per-batch design agents reported that cross file boundaries; the integration commit resolves each.

- **Reciprocal XREFs.** Every file design's "Inputs and XREFs" line lists the sections in other files it consumes or feeds, with the reason. The integration commit adds the reciprocal line in each target, including the existing files `D01 T02`, `D01 T03`, `D01 T04`, `D01 T05`, `D02 T07` to `D02 T16`, `D03 T02` to `D03 T07`, `D04 T01`, `D04 T02`, and `D05 T01` (one-sided XREFs are FATAL).
- **Controls deferred by name to later phases** (legitimate, each names its owner): opening camera RAW files, RAW layers, and redevelop in `D03 T15 §12` wait for `D03 T07 §11` (Phase 31, now 41), with pixel-layer development working from Phase 23; FITS light, dark, and flat frames in `D03 T15 §10` arrive when `D03 T17 §6` (Phase 25) registers its reader with the stack loader, TIFF and PNG frames working before; the Contextual Task Bar entries of `D03 T19 §1` and `§3` appear in the Properties panel first and in the task bar once `D03 T20 §1` (Phase 27) hosts it; spot healing's and patch's content-aware modes in `D03 T13 §2` are wired by `§3` of the same phase; levels in `D03 T11 §2` run on `D01 T03 §4` and switch to the `D01 T07 §1` tone kernel when it lands, with no user-visible change.
- **Shared pieces built by the first section that needs them:** the expression compiler for Apply Image equations is built by `D03 T11 §8` (Phase 18) at `src/Isotone.Core/Imaging/Procedural/Expressions/`, and `D01 T06 §9` (Phase 22) only adds its noise primitives; the lens database reader is built by `D03 T14 §6` (Phase 21) and consumed by `D01 T07 §3` (Phase 23).
- **Dependencies sharpened after the design pass:** `D03 T14 §10` also depends on `D01 T06 §10`, `§12`, and `§13` (its dedicated editors); `D03 T15 §9` also depends on `§8` (the sources panel reuses the stack loader); `D03 T19 §7` also depends on `§6` (subject masks). `D03 T16 §5` rebases today's `VectorMask` (`src/Gesso/src/Gesso.Core/Masks/VectorMask.cs`) on the shared geometry as its first item.
- **Catalog rows rerouted after the design pass** (statuses changed in place, ids unchanged, so a few rows sit in an area table other than their section's): IP-1212 and IP-1213 to `D03 T09 §7` (the filter form of IP-0375); IP-1247 to `D03 T14 §9`; IP-1065 to `D03 T14 §1`; IP-1063 to `D03 T14 §2`; IP-1240, IP-1241, IP-1244, IP-1246, IP-1275, and IP-1277 (dedicated editors) to `D03 T14 §10`; IP-1291 to B-044; IP-2021 and IP-2033 to `D03 T19 §14`; IP-2017 and IP-2018 to `D03 T19 §9`; IP-1529 to `D03 T15 §9`; IP-0604 and IP-0635 to `D01 T07 §2` and `§3` (adjustment layers whose engine lands in Phase 23); IP-0656 to `D01 T06 §13`; IP-0503 and IP-0521 to `D03 T09 §14`; IP-1425 to `D03 T14 §6`; IP-1471 to `shipped-scope D03 T07 §11`.
- **Catalog duplicates across buckets.** Merging ran per topic bucket, so a few capabilities appear as two rows under one owner or two owners (IP-1145 and IP-1273 glass tile, IP-0697 and IP-0799, the matting rows). That is intended, as in the Stilus catalog: each row names the section that owns its part.
- **Decisions for the operator to confirm at integration:** the new dependencies libjpeg-turbo, SharpCompress, FluentFTP, and Vortice.Windows (all GPL-3.0-compatible, rows in "Formats and licensing"); LibTiff.NET (BSD) named by `D03 T17 §11` only as a candidate against WIC; the one new project `Isotone.Gesso.ShellThumbnails`; and the reverse-engineering question behind B-045.
- **AGENTS.md.** Its `docs/parity/` row describes the Stilus evidence only; the integration commit extends it to name the Gesso inventories, catalog, and design.
- **Backlog ids named before they exist.** `gesso-parity.md` and the updated `stilus-parity.md` name B-041 to B-047, which become live entries in the integration commit; until then `D00 T01 §6` is not built, so nothing refuses them.
- **Sizing watch list.** These sections carry the most features or the densest hints and are the likeliest to pass 30 checklist items; each file design's "Sizing concerns" names the natural split. A split spends the phase's spare ceiling (every parity phase keeps 1 to 3 slots of room from its +10 percent), never a raise: `D03 T08 §3`, `§4`; `D03 T09 §3`, `§7`; `D03 T10 §7`, `§10`; `D03 T11 §1`, `§2`, `§5`, `§7`, `§9`; `D03 T12 §1`, `§3`, `§5`, `§9`; `D01 T06 §6`, `§8`, `§13`; `D03 T13 §5`, `§9`; `D03 T14 §1`, `§2`, `§6`; `D03 T15 §10`; `D03 T16 §2`, `§5`, `§7`; `D03 T17 §6`, `§7`, `§8`, `§9`; `D03 T18 §1`, `§2`, `§4`; `D03 T19 §6`; `D03 T20 §1`, `§4`.

## Catalog check

`python check_gesso_catalog.py` (the scratch check, run 2026-09-26 against the files in this folder, the live `todo/` tree, and `todo/backlog.md`; the rules `D00 T01 §7` turns into validator classes):

- Source ids: 3,176 Photoshop, 2,762 Affinity, 4,891 GIMP, 10,829 in all.
- Catalog rows: 2,367 (IP-0001 to IP-2367), ids unique and sequential: True.
- Source ids placed: 10,829 exactly once; missing 0; duplicated 0; unknown 0.
- Statuses: plan 1,997 (9,541 source rows); shipped-scope 204 (762 source rows); backlog 100 (377 source rows); excluded 54 (129 source rows); other-app 12 (20 source rows).
- Plan refs: 161 distinct sections, all designed: True; shipped-scope refs: 28 distinct existing sections, all live: True; backlog ids named: B-012, B-024, B-041, B-042, B-043, B-044, B-045, B-046, B-047. B-012 and B-024 are live today; B-041 to B-047 are the new entries drafted in "Backlog changes".
- Designed sections with no catalog row of their own: D00 T01 §7, D03 T17 §14, D03 T21 §1, D03 T21 §2, D03 T21 §3, D03 T21 §4, D03 T21 §5, D03 T21 §6, D03 T21 §7, D03 T21 §8, D03 T21 §9, D03 T21 §10, D03 T21 §11, D03 T21 §12 (the validator, the XCF writer whose feature row sits with the reader in `D03 T17 §4`, and the release sections).
- Result: clean.

## File designs

### todo/00-workspace/TODO-01-dev-automation.md -- one new section in an existing file

- **Phase(s):** 0 (the workspace spine; Phase 0 holds 14 sections against a ceiling of 15, so §7 takes the last slot and needs no raise)
- **Why here:** the Gesso catalog is plan data like `todo/` and like the Stilus catalog `§6` already polices; the acceptance-bar aim that Gesso covers every Photoshop, Affinity, and GIMP capability in its catalog needs the same gate before the first Gesso parity row (Phase 16) runs, and extending `§6`'s module keeps one validator for both catalogs instead of a second script.

#### §7. The validator reads the Gesso parity catalog

- **Deliverable:** `validate` refuses a Gesso parity catalog that has drifted from its three sources or from the plan, exactly as `§6` does for Stilus, and `query parity --catalog gesso` reports per-phase coverage of the Gesso parity phases.
- **Depends On:** §6
- **Phase:** 0
- **Surface:** no surface of its own (stdlib tooling run by `validate`, the commit hook, and CI)
- **Runs:** none
- **Catalog:** owns no catalog rows (it enforces them)
- **Hints:**
  - Context claims, true today and to be re-measured on the authoring day: `<!-- claim: exists docs/parity/gesso-parity.md -->` `<!-- claim: count "^\| IP-\d{4} \|" docs/parity/gesso-parity.md = 2367 -->` `<!-- claim: count "^\| PS-A-\d{4} \|" docs/parity/sources/photoshop-27.10.md = 1750 -->` `<!-- claim: count "^\| PS-B-\d{4} \|" docs/parity/sources/photoshop-27.10.md = 1426 -->` `<!-- claim: count "^\| AF-\d{4} \|" docs/parity/sources/affinity-3.3.md = 2762 -->` `<!-- claim: count "^\| GP-\d{4} \|" docs/parity/sources/gimp-3.2.6.md = 4891 -->` `<!-- claim: count "IP-" scripts/todo-graph.py = 0 -->`
  - Turn `§6`'s module-level Stilus constants in `scripts/todo-parity.py` into one `CATALOGS` table of `CatalogSpec` entries (name, catalog path, row prefix, and a list of `SourceSpec` (file, id regex, catalog column)): `stilus` = `docs/parity/stilus-parity.md`, `NP-####`, Illustrator `AI-####` and CorelDRAW `CD-###`; `gesso` = `docs/parity/gesso-parity.md`, `IP-####`, Photoshop `PS-A-####` and `PS-B-####` (two id families in one file, `docs/parity/sources/photoshop-27.10.md`), Affinity `AF-####` (`affinity-3.3.md`), GIMP `GP-####` (`gimp-3.2.6.md`). `parse_sources` and `parse_catalog` take a spec and find columns from each area table's header row (`| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |`), so no Stilus code path changes behavior.
  - Self-check on today's files prints 1,750 `PS-A`, 1,426 `PS-B`, 2,762 `AF`, and 4,891 `GP` ids and 2,367 `IP` rows (10,829 source ids in all), beside `§6`'s Stilus figures.
  - Check classes: the six catalog-agnostic classes of `§6` (`parity-id-missing`, `parity-id-duplicate`, `parity-id-unknown`, `parity-status-malformed`, `parity-ref-dead`, `parity-backlog-dead`) run once per catalog and prefix every message with the catalog name (`gesso: IP-0123 ...`), so no class is duplicated; `parity-ip-duplicate` is added as the Gesso counterpart of `parity-np-duplicate` (an `IP-` id used twice).
  - Add `parity-totals-drift` for both catalogs: the header's Totals table (features and source rows per status kind and the grand total) or an Areas-list count disagrees with the counted rows; the message names the table cell and both numbers.
  - Status grammar per `docs/parity/README.md` as it reads after the Gesso decision: `other-app:` accepts `Stilus`, `Gesso`, `Albumen`, or `none` (the Gesso catalog has 4 `other-app: Stilus` rows), and `excluded:` accepts the reasons `cloud`, `platform`, and `removed` (Photoshop's legacy 3D and Digimarc); `shipped-scope` refs into `D01 T03` and `D03 T05` to `D03 T07` resolve like any other ref, and a ref naming `D03 T07 §3`, `§11`, `§16`, or `§17` stays live because those sections are relocated, not Moved.
  - Backlog ids: `parity-backlog-dead` covers the ids the Gesso catalog uses (B-012, B-024, and B-041 to B-047: 99 rows); it reads `todo/backlog.md` through `graph.parse_backlog`, so the integration commit must add B-041 to B-047 before `validate` goes green, and the self-test fixture carries one live and one dead id.
  - `query parity [--catalog stilus|gesso|all] [--phase N] [--json]`: default `all`; per phase the planned rows and how many of their sections are stamped, per status kind the totals, per catalog separately; the Gesso parity phases (16 to 27 after the integration renumbering) quote `--catalog gesso --phase N`, and a section in no phase is reported under `unplaced`.
  - Add `parity-ip-duplicate` and `parity-totals-drift` to `SEVERITY_MAP` in `scripts/todo-graph.py` as `fatal` and their rows to the per-class table in `todo/README.md` in the same commit, so the self-test's README-parity check stays green; skip the Gesso pass when `docs/parity/gesso-parity.md` is absent, as `§6` skips Stilus.
  - Self-test fixtures in the temporary tree: a tiny Photoshop source with one `PS-A` and one `PS-B` row, a tiny Affinity and GIMP source, a three-row Gesso catalog with a Totals table, and a backlog with B-041; cases: one missing `PS-B` id, one duplicate `GP` id, one unknown `AF` id, one duplicate `IP-` id, one `other-app: Stilus` row (clean), one `excluded: removed` row (clean), one malformed status, one dead ref, one dead backlog id (B-099), one totals mismatch, one clean catalog, and one `query parity --catalog gesso --phase N --json` count.
  - Update the Enforcement paragraph of `docs/parity/README.md` to say `D00 T01 §7` is built and to list both new classes and the `--catalog` flag.
  - Commit: `"workspace: validate the Gesso parity catalog against its sources and the plan"`
- **Proof:** unit plus static: `python scripts/todo-graph.py self-test` reports `0 failed` with the Gesso cases counted; `validate` exits 0 on the integrated tree; deleting one `GP-` id from a scratch copy of `gesso-parity.md` makes `validate` exit 1 naming `gesso: parity-id-missing`, and editing one Totals cell makes it exit 1 naming `parity-totals-drift`; `query parity --catalog gesso --phase 16 --json` prints the Phase 16 counts; cheaper substitute that fails: a copy of `§6`'s script hard-wired to the Gesso file, which the self-test's single-module import and the Stilus cases (still passing through the shared `CatalogSpec` path) expose as a second implementation.

### todo/03-gesso/TODO-08-gesso-parity-document.md -- `gesso-parity-document`

- **Title:** "TODO-08 -- Gesso Parity: Document, Canvas, View, History, and the Image Menu"
- **Phase(s):** 16
- **Goal:** Gesso's document foundation reaches Photoshop, Affinity Photo, and GIMP parity: a document model with precision (8-bit, 16-bit, and 32-bit float, perceptual or linear), separate X and Y resolution, pixel aspect ratio, and a transparent-background switch; one native-format contract (`gesso:` parameters in the OpenRaster `stack.xml` beside a rendered PNG for every non-raster layer and document part) that every later live layer kind and document part registers with; the New Document dialog with presets and templates; the full zoom, rotate, flip, screen-mode, window, view-mode, display-filter, and navigator set; rulers, units, guides, grids, and snapping; measurement, count, notes, and the Info, Histogram, and Scope panels; snapshots, non-linear history, and history saved with the document; the Image menu's canvas, trim, reveal, and resampling commands; every clipboard and paste variant; and the crop and perspective-crop extensions. The code lives in `src/Gesso/Isotone.Gesso.Core/` (`Documents/`, `Native/`, `Guides/`, `Snapping/`, `Analysis/`, `History/`), `src/Gesso/Isotone.Gesso.Rendering/` (`Display/`, `Overlays/`), `src/Gesso/Isotone.Gesso.FileFormats/Native/`, and `src/Gesso/Isotone.Gesso.Desktop/`; it consumes the pixel engine (`D01 T03 §2` resampling, rotation, and perspective, `D01 T03 §4` histograms), color management (`D01 T04`), the suite history (`D01 T02 §4`), and the units converter and snapping core it moves out of Stilus on their second consumer; it never writes a second resampler, a second history stack, or a second container format, and view state never enters history.
- **Current-state facts to verify (with claim candidates):**
  - `GessoDocument` holds one `Resolution` (default 72) and no pixel aspect ratio, precision curve, guides, or document parts. `<!-- claim: lines src/Gesso/src/Gesso.Core/Documents/GessoDocument.cs = 98 -->` `<!-- claim: count "private double _resolution = 72\.0" src/Gesso/src/Gesso.Core/Documents/GessoDocument.cs = 1 -->` `<!-- claim: count "PixelAspect" src/Gesso/src/**/*.cs = 0 -->`
  - The bit-depth enum already names 32-bit float, which §1's precision readout labels. `<!-- claim: count "Bpc32 = 32" src/Gesso/src/Gesso.Core/Documents/BitDepth.cs = 1 -->`
  - Undo is two linear lists today, so non-linear history (§6) has no model to extend until `D01 T02 §4` moves it. `<!-- claim: count "private readonly List<ICommand> _redoStack" src/Gesso/src/Gesso.Core/History/CommandHistory.cs = 1 -->` `<!-- claim: lines src/Gesso/src/Gesso.Core/History/HistorySnapshot.cs = 166 -->`
  - Zoom is one scalar clamped at 3,200 percent, and Cut, Copy, and Paste only log. `<!-- claim: count "Math\.Min\(ZoomLevel \* 1\.25, 32\.0\)" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 1 -->` `<!-- claim: count "(Cut|Copy|Paste) requested" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 3 -->`
  - Guides exist only as a view-model flag, and nothing computes a histogram. `<!-- claim: count "private bool _showGuides" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 1 -->` `<!-- claim: count "Guide" src/Gesso/src/Gesso.Core/**/*.cs = 0 -->` `<!-- claim: count "Histogram" src/Gesso/src/**/*.cs = 0 -->`
- **Inputs and XREFs:** `standards/gesso.md` (tiles, premultiplied RGBA, 8, 16, and 32-bit float, zero allocations per frame, SIMD with a scalar reference, GPU parity, fidelity proofs, no silent profile change), `standards/shared.md`, `standards/testing.md`; OpenRaster 0.0.6 specification (`stack.xml`, `composite-op`, `isolation`); Adobe Photoshop File Formats Specification (image resources 1032 grid and guides, 1064 pixel aspect ratio, color samplers, annotations); GIMP 3.2.6 (`gimp-console` batch mode as the `.ora` composite oracle, GEGL 0.4 `nohalo` and `lohalo` samplers under LGPL-3.0-or-later as reference); Krita 5.2 as a second `.ora` oracle; libvips 8.16 and FFmpeg 7.1 (`hqx`, `xbr` filters) as resampling goldens; ImageMagick 7.1 `-distort Perspective`; He, Sun, and Tang 2010 (guided filter); Suzuki and Abe 1985 (border following); numpy 2.x FFT as the FFT golden; -> XREF: D03 T06 §3 (Gesso 0.1.0 ships before every section here); -> XREF: D03 T01 §1 (the rename the target paths assume); -> XREF: D03 T04 §4 (the native format §1 extends with the `gesso:` contract); -> XREF: D03 T04 §2 (recent files §2 extends); -> XREF: D03 T04 §5 (the PSD adapter §1, §4, and §5 extend with resolution, pixel aspect, guide, and note resources); -> XREF: D03 T03 §1 (the New dialog §2 extends and the status strip §11 extends); -> XREF: D03 T03 §2 (the History panel and `TileSnapshotCommand` §6 extends); -> XREF: D03 T03 §4 (the zoom and hand tools and temporary-tool mechanism §3 extends); -> XREF: D03 T03 §7 (Image Size, Canvas Size, and crop §1, §7, and §9 extend); -> XREF: D03 T02 §2 (the viewport and mip cache §3 and §10 extend); -> XREF: D03 T02 §5 (GPU parity for §10's display filters); -> XREF: D03 T01 §2 (the ported `Ruler` control §4 extends); -> XREF: D03 T05 §2 (the histogram control §11 hosts); -> XREF: D01 T02 §4 (the suite history §6 builds its tree over); -> XREF: D01 T02 §5 (atomic writes for templates, logs, and exports); -> XREF: D01 T03 §2 (`Resampler`, `Rotator`, and `PerspectiveCorrector`, which §7 extends in place and §9 consumes); -> XREF: D01 T03 §4 (`Histogram` for §11); -> XREF: D01 T04 §1 (profile names and conversions for §1's profile tab and §11's readouts); -> XREF: D02 T07 §9 (`UnitConverter`, moved to `Isotone.Core` by §4); -> XREF: D02 T07 §11 (the snapping core, moved to `Isotone.Core` by §4); -> XREF: D01 T06 §4 (deconvolution reuses §11's `Fft2D`); -> XREF: D03 T07 §17 (workspaces the panels here dock into); -> XREF: D03 T09 §1 (layer kinds register with §1); -> XREF: D03 T09 §7 (layer effects register with §7's Scale Styles hook); -> XREF: D03 T09 §13 (artboards scope §4's guides and register snap candidates); -> XREF: D03 T10 §1 (selections float into §8's floating layer); -> XREF: D03 T11 §7 (precision and mode conversions over §1's fields); -> XREF: D03 T11 §9 (the Color Sampler tool places §11's sample points); -> XREF: D03 T13 §3 (content-aware crop fill through §9's hook); -> XREF: D03 T16 §1 (Paste without Formatting from §8, the scale-marker label of §5); -> XREF: D03 T16 §5 (paths as a §1 document part and as §4 snap candidates); -> XREF: D03 T17 §2 and D03 T17 §3 (PSD write and read of guides, notes, samplers, pixel aspect); -> XREF: D03 T17 §4 (XCF guides, sample points, and precision); -> XREF: D03 T17 §7 (SVG and metafile readers that enable §8's Paste Special entries); -> XREF: D03 T18 §3 (slices as a §1 document part and §4 snap candidates); -> XREF: D03 T18 §4 (profile readout in §1's profile tab); -> XREF: D03 T18 §6 (print consumes §2's bleed); -> XREF: D03 T19 §1 (provenance as a §1 document part); -> XREF: D03 T19 §4 (generative expand beside §9's crop extension); -> XREF: D03 T19 §8 (AI upscale beside §7's classical Preserve Details); -> XREF: D03 T20 §4 (preference pages over the navigation, units, guide, and grid keys added here).
- **Adjacency:** list=applicable (template browser and recent-documents list in §2, Images panel and navigator view points in §10, Measurement Log in §5, Buffers panel in §8, History panel in §6); document=applicable @ D03 T18 §6 (bleed and print size from §2 and §7 are what print consumes); settings=applicable (every toggle and value is a `Gesso.*` key with a default and a named consumer); reporting=applicable (Image Properties in §1, Info, Histogram, Scope, and Pointer panels in §11, Measurement Log in §5); notifications=applicable (progress and cancel for resampling, rotation, trim, and history save; the open summary names layers opened as pixels); permissions=applicable (read-only template folders, missing recent files, and locked documents refused by name; locked guides refuse edits); audit=applicable (every document-changing command is one history entry with one Serilog Information line); exchange=applicable (the `gesso:` contract, `.ora` interop, templates, measurement CSV export, clipboard formats, PSD and XCF resources through D03 T17); reverse=applicable (every document command undoes; snapshots and history branches restore earlier states; Revert restores the saved file)

#### §1. The document model and the native-format contract for live content

- **Deliverable:** `GessoDocument` carries precision, X and Y resolution, pixel aspect ratio, a transparent-background switch, and document parts, and `Isotone.Gesso.Core/Native/` defines the one contract every later live layer kind and document part registers with (parameters in the `gesso:` namespace of `stack.xml` beside a rendered PNG fallback), with the Image Properties and Document Setup dialogs, Duplicate Image, and pixel-aspect correction.
- **Depends On:** D03 T06 §3, D03 T04 §4
- **Phase:** 16
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/image-properties/ and docs/captures/gesso/document-setup/. Job: a user can read everything about a document (size, print size, resolution, precision, profile, memory, history, element counts) and change its units, resolution, pixel aspect, and background without guessing, and any `.gesso` renamed to `.ora` opens in GIMP and Krita with every layer visible. Treatment: GIMP's tabbed Image Properties (Properties, Color Profile, Comment) and Affinity's Document Setup (dimensions with resample or anchor, DPI, units, transparent background) as modal dialogs; Image, Pixel Aspect Ratio and View, Pixel Aspect Ratio Correction menus; Image, Duplicate. Cheaper substitute that fails: writing only parameters with no fallback PNG, so other editors show blank layers. Chrome: consume `Isotone.UI` dialog styles, the settings store, `D03 T03 §7`'s Image Size and Canvas Size commands, and `D01 T04 §1`'s ICC reader; do not add a second container or serializer.
- **Runs:** `Requires: display-session -- the dialogs and the GIMP and Krita open of a live fixture need an interactive desktop`
- **Catalog:** IP-0001 to IP-0008 (8 features)
- **Hints:**
  - `GessoDocument` in `Isotone.Gesso.Core/Documents/` gains `Precision` (`BitDepth` 8, 16, or 32-float plus `ToneCurve { Perceptual, Linear }`, GIMP 3.2's precision pair, labeled "16-bit integer, perceptual"), `ResolutionX`, `ResolutionY`, `ResolutionUnit`, `PixelAspectRatio` (default 1.0), `TransparentBackground`, `Units`, `Comment`, and `Parts` (the document-part bag); conversion between precisions is `D03 T11 §7`'s, this section models, persists, and reads out.
  - Contract in `Isotone.Gesso.Core/Native/`: `IGessoElement` (`Kind` lowercase such as `fill`, `adjustment`, `text`; `SchemaVersion`; `WriteParameters(XElement target, INativeWriteContext context)` where the context can add ZIP entries under `gesso/`; `RenderFallback(TileGrid target)` for layer kinds) and `GessoElementRegistry.RegisterLayerKind(kind, reader)` plus `RegisterDocumentPart(name, reader)`, wired in the composition root so later sections add kinds without touching `GessoNativeFormat`.
  - Wire shape: every non-raster layer is an ordinary OpenRaster `<layer src="data/<guid>.png">` whose PNG is the rendered fallback at document size (16-bit PNG for 16 and 32-bit documents), carrying `gesso:kind`, `gesso:v`, and `gesso:hash` (SHA-256 of the fallback PNG bytes) and one `<gesso:params>` child; blend modes OpenRaster names use `composite-op="svg:*"`, others write `svg:src-over` plus `gesso:composite-op` and are listed in the fallback report; groups keep OpenRaster `isolation`. Keep the namespace URI `D03 T04 §4` documented in `docs/dev/gesso/native-format.md` (proposed `https://schemas.rizonesoft.com/gesso/1`) and record the contract as a `docs/dev/decisions.md` row.
  - Document parts: one `<gesso:document>` as the first child of `<image>` holds blocks owned by their sections, each with its own `gesso:v` (guides, grid, and units §4; notes, counts, and measurement scale §5; sample points §11; snapshots and saved history §6; view points §10; bleed and template §2; symbols `D03 T09 §1`; comps `D03 T09 §11`; channels `D03 T10 §10`; paths `D03 T16 §5`; slices `D03 T18 §3`; provenance `D03 T19 §1`); large payloads are ZIP entries under `gesso/` referenced by path, and 32-bit float layers store `gesso/float/<guid>.rgbaf` (little-endian RGBA32F in 256-pixel tiles, documented) beside their 16-bit PNG fallback.
  - Reader rules: a known kind whose fallback hash matches reopens live; a hash mismatch (the PNG was edited in GIMP or Krita) opens the PNG as a pixel layer with the Warning "{Kind} layer {Name} was edited outside Gesso; opened as pixels" in the open summary; an unknown kind, a newer `gesso:v`, or an unknown document block is kept verbatim in `UnknownNativeData`, renders from its fallback, and is written back byte-equivalent.
  - Image Properties dialog (IP-0001, IP-0005, IP-0007): pixel and print size, X and Y resolution, color space, precision, file name, path, size, and type, memory from the tile cache, undo and redo step counts, layer, channel, and path counts, pixel count, and "Count unique colors" computed on demand by `UniqueColorCounter` in `Isotone.Gesso.Core/Analysis/` (tile-parallel, 64-bit keys for 16-bit, cancellable; reused by §11); Color Profile tab (description, class, space, version, copyright through `D01 T04 §1`; assign and convert stay `D03 T18 §4`); Comment tab editing `Comment`.
  - Document Setup (IP-0004): units, DPI with Rescale (resamples through `D03 T03 §7`'s Image Size command) or keep pixels, dimensions with an anchor grid (Canvas Size command), and Transparent Background (IP-0002): Image, Transparent Background toggles the flag as one `SetDocumentPropertyCommand`; when off the composite and every flattening export draw over opaque white, as Affinity does; the new-document background choice stays `D03 T03 §1`'s.
  - Pixel aspect ratio (IP-0006, IP-0008): Image, Pixel Aspect Ratio lists Photoshop's values (Square 1.0, D1/DV NTSC 0.9091, D1/DV PAL 1.0940, D1/DV NTSC Widescreen 1.2121, HDV 1080/DVCPRO HD 720 1.3333, D1/DV PAL Widescreen 1.4587, DVCPRO HD 1080 1.5, Anamorphic 2:1 2.0) plus custom values saved in `Gesso.Document.CustomPixelAspects`; View, Pixel Aspect Ratio Correction (`Gesso.View.PixelAspectCorrection`, default on) scales only the view's X axis in §3's view transform; pixels never change; PSD resource 1064 is read by the `D03 T04 §5` adapter now.
  - Duplicate Image (IP-0003): Image, Duplicate with a name and "Duplicate merged layers only", a new untitled tab whose tiles are shared copy-on-write, no entry in the source's history.
  - Undo names "Set Document Properties", "Toggle Transparent Background", and "Set Pixel Aspect Ratio"; one Serilog Information line each with the document id and the changed fields.
  - Tests: `NativeElementContractTests` with a test-only `ProbeLayer` kind and a `probe` document part (write, reopen live, hash mismatch opens as pixels, unknown kind and newer version preserved byte-equivalent), `DocumentPropertiesTests`, `UniqueColorCounterTests` (a 4,096-color ramp counts 4,096).
  - Fixtures `tests/fixtures/gesso/native-live/` (probe layer, unknown future kind, a fallback edited by GIMP, a 32-bit float layer) with composites exported by GIMP 3.2.6 `gimp-console` and Krita 5.2 from the file renamed `.ora`, versions in `VERSION.txt`.
  - Commit: `"gesso: the document model and the gesso namespace contract for live content"`
- **Proof:** format fidelity: `NativeLiveRoundTripTests` open, save, and reopen every `tests/fixtures/gesso/native-live/` file and compare layer by layer and the preserved unknown block byte for byte, and GIMP 3.2.6's composite of each file renamed `.ora` matches Gesso's within 1/255; cheaper substitute that fails: parameters written with no fallback PNG, which the GIMP composite comparison catches as a blank layer.

#### §2. New document, presets, and templates

- **Deliverable:** The New Document dialog gains preset categories, saved presets and favorites, precision, gamma, profile, pixel aspect, fill, comment, and bleed, plus New from Clipboard, settings templates and content templates with their dialogs, and a recent-documents list with count, locate, and remove.
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/new-document/ (baseline from `D03 T03 §1`), new captures to docs/captures/gesso/templates/ and docs/captures/gesso/document-history/. Job: a user starts the right document in one step, reuses their own sizes and templates, and reopens recent work even when it moved. Treatment: preset categories and Saved on the left, details on the right with an orientation swap, templates as tiles, a GIMP-style Templates panel and template editor, and a Document History panel with thumbnails and missing-file badges. Cheaper substitute that fails: a width and height prompt with a hard-coded list. Chrome: consume the `D03 T03 §1` dialog (extended, not replaced), `Isotone.UI` dialog styles, the settings store, `D01 T02 §5` for template writes, and the icon catalog; do not add a second recent-files store.
- **Runs:** `Requires: display-session -- the New dialog, template browser, and Document History panel need an interactive desktop`
- **Catalog:** IP-0009 to IP-0019 (11 features)
- **Hints:**
  - `DocumentPreset` record in `Isotone.Gesso.Core/Documents/Presets/` (IP-0009; name, category, width, height, units, resolution, orientation, color mode, precision, tone curve, profile name, pixel aspect, background fill, bleed, artboard flag read by `D03 T09 §13`, comment); built-in categories Photo, Print, Art and Illustration, Web, Mobile, Film and Video with generic sizes named by paper or pixel size (no vendor content); user presets and favorites in `Gesso.NewDocument.UserPresets` and `Gesso.NewDocument.Favorites`; New from Last Preset reads `Gesso.NewDocument.LastPreset`.
  - Extend `D03 T03 §1`'s dialog (IP-0015, IP-0016): preset rail (Recent, Saved, categories), details with orientation swap, color mode (RGB and Grayscale now; CMYK and Lab rows disabled with a tooltip naming `D03 T11 §7`), precision and tone curve, color profile list from `D01 T04 §1`'s installed-profile enumeration, pixel aspect (§1's list), fill (white, black, background color, transparent, 50 percent gray computed in the document's tone curve, custom), comment, and bleed.
  - `DocumentFactory.Create(DocumentPreset)` is the one creation path for the dialog, New without Dialog (Alt+Ctrl+N), templates, and New from Clipboard; one Serilog Information line per create with preset, size, and precision.
  - New from Clipboard (IP-0010): the dialog's Clipboard preset takes the clipboard image's size and resolution, and Edit, Paste As, New Image (GIMP) creates the document with the pixels; the reader `ClipboardImageReader` (PNG, `CF_DIBV5`, `CF_DIB` into a tile grid) lives in `Isotone.Gesso.Desktop/Clipboard/` and §8 extends it with writing and the paste variants.
  - Bleed (IP-0011) is stored in the `<gesso:document>` block, drawn as a guide line in the view (hidden by §3's Preview mode), and consumed by `D03 T18 §6`.
  - Settings templates (GIMP, IP-0012, IP-0013, IP-0019): a Templates panel listing `DocumentPreset` entries with size, orientation, resolution, color space, precision, gamma, profiles, fill, and comment; New, Duplicate, Edit (the template editing dialog), Delete, and Create Image from the selected template; stored in `%LOCALAPPDATA%\Rizonesoft\Gesso\templates.json` through the atomic writer.
  - Content templates (Affinity and Photoshop, IP-0012, IP-0017): an `.gesso` file with an `<gesso:template>` block (name, category, description); File, Save as Template, File, New from Template (opens an untitled copy), and Edit Template (opens the file itself); template folders in `Gesso.Templates.Folders` (default `%LOCALAPPDATA%\Rizonesoft\Gesso\templates\`), unreadable folders listed with their refusal; Affinity `.aftemplate` files are refused by name as backlog B-045.
  - Recent documents (IP-0014, IP-0018): extend `D03 T04 §2`'s list with a count `Gesso.Files.RecentCount` (default 20, 0 to 100), Keep record of used files `Gesso.Files.KeepRecent`, a Document History panel (thumbnail, path, last opened, missing badge), Locate (repoint an entry through a file dialog), Remove Entry, and Clear; File, Open Recent shows missing entries disabled beside a Locate item.
  - Tests: `DocumentFactoryTests` (every built-in preset's size and resolution; 50 percent gray fills 128 in perceptual and 0.5 in linear), `DocumentPresetStoreTests`, `ContentTemplateRoundTripTests` (template block survives save and New from Template yields an untitled document), `RecentDocumentsTests` (missing detection and Locate with a temp folder).
  - Commit: `"gesso: new-document presets, templates, and recent documents"`
- **Proof:** unit plus driven: `DocumentFactoryTests` and `ContentTemplateRoundTripTests` pass, and a driven run saves a template, creates a document from it, and locates a moved recent file with log lines quoted and captures committed; cheaper substitute that fails: presets stored as a fixed table, which the saved-preset round trip catches.

#### §3. Zoom, rotate view, flip view, and screen modes

- **Deliverable:** A per-window view transform with the full zoom command set and navigation preferences, rotate view, flip view, print-size and dot-for-dot views, birds-eye view, flick panning, screen modes, padding and Show All, Extras, Preview mode, and the pixel grid toggle, none of which enters history.
- **Depends On:** D03 T06 §3
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the View menu and canvas, new captures to docs/captures/gesso/view/. Job: a user sees the image at the zoom, angle, and orientation the task needs and gets anywhere in it fast. Treatment: View menu zoom and screen-mode commands, the Zoom and Rotate View tools with options bars, a typed zoom field in the status strip, and canvas overlays whose visibility Extras governs. Cheaper substitute that fails: rotating the WPF control with a render transform, which leaves rulers, hit testing, and tools in unrotated coordinates. Chrome: consume `D03 T02 §2`'s viewport and mip cache, `D03 T03 §4`'s tool system and temporary-tool mechanism, the keymap, and the settings store; do not add a second zoom model.
- **Runs:** `Requires: display-session -- zoom, rotation, flicks, screen modes, and frame-time measurement need an interactive desktop`
- **Catalog:** IP-0026 to IP-0051 (26 features)
- **Hints:**
  - `ViewState` in `Isotone.Gesso.Desktop/View/` per window (zoom, center in document coordinates, rotation in degrees, flip horizontal and vertical, screen mode, show-all) and `ViewTransform` composing scale, rotation about the view center, flip, and §1's pixel-aspect correction with an exact inverse used by hit testing, rulers, overlays, and every tool; view changes never enter history and log only at Debug.
  - `ZoomCommands` (IP-0026, IP-0027): In and Out on a preset ladder from 1.5625 to 12,800 percent, Fit on Screen (Ctrl+0), Fill, 100 percent (Ctrl+1), 200 percent (Ctrl+2), Zoom to Selection (Shift+Ctrl+J), Revert Zoom (backtick), a Custom Zoom dialog accepting a percent or a ratio such as `3:1`, and the typed zoom field; replaces today's single clamped `ZoomLevel`.
  - Pointer navigation (IP-0028, IP-0029, IP-0048): wheel zooms or scrolls (`Gesso.Navigation.WheelZooms`), zoom to the clicked point (`Gesso.Navigation.ZoomToClickedPoint`), scrubby zoom by dragging with the Zoom tool (`Gesso.Navigation.ScrubbyZoom`), animated zoom while held (`Gesso.Navigation.AnimatedZoom`), drag-to-zoom speed (`Gesso.Navigation.DragZoomSpeed`), hold Z for a temporary zoom through `D03 T03 §4`'s temporary-tool mechanism, and Space pans or moves (`Gesso.Navigation.SpaceBar`).
  - Window-level behaviors (IP-0030, IP-0031): resize floating windows to fit when zooming (`Gesso.View.ResizeWindowOnZoom`), and scroll, zoom, and rotate all windows together when Shift is held or the options-bar checkbox is on.
  - Birds-eye view and flick panning (IP-0032, IP-0033, IP-0049): hold H and press to zoom out to fit with a frame, release to zoom into the framed area (Photoshop); flick panning with exponential decay (`Gesso.Navigation.FlickPanning`), overscroll past the canvas edge (`Gesso.View.Overscroll`).
  - Physical views (IP-0034, IP-0051): Print Size uses `Gesso.View.ScreenPpi` (detected from the monitor's physical size through `GetDeviceCaps` `HORZSIZE` and `HORZRES`, entered manually, or set by a Calibrate dialog that measures an on-screen line), Actual Pixels, and GIMP's Dot for Dot toggle (off shows the image at its physical size using §1's X and Y resolution).
  - Rotate view (IP-0035, IP-0046, IP-0049): the Rotate View tool (R) with an angle field, Shift for 15-degree steps, Reset View (Esc or the button), rotation by modifier-scroll (`Gesso.Navigation.RotateModifier`) and by touchpad rotation through WPF manipulation events; the viewport draws tiles through the rotated matrix without resampling document pixels on both the CPU and GPU paths.
  - Flip view (IP-0036): View, Flip Horizontally and Flip Vertically (GIMP) as view flags that mirror the transform and never touch pixels.
  - Screen modes and chrome (IP-0037, IP-0038, IP-0047): Standard, Full Screen with Menu Bar, and Full Screen (F cycles, Shift+F reverses); show or hide menu bar, scroll bars, status bar, and rulers, each with a separate full-screen default (`Gesso.View.FullScreen.*`).
  - Padding and Show All (IP-0039, IP-0040): padding from the theme, light checks, dark checks, or a custom color (`Gesso.View.PaddingMode`, `Gesso.View.PaddingColor`) with Keep Padding in Show All; View, Show All renders layer pixels beyond the canvas (GIMP 2.10 behavior) and turns off clip-to-canvas for the view only.
  - Extras and Preview mode (IP-0041, IP-0042, IP-0043, IP-0045): Extras (Ctrl+H) is the master toggle over layer edges, selection edges, target path, notes, count, pixel grid, guides, smart guides, slices, and canvas boundary, with a Show Extras Options dialog; Preview mode (Affinity) hides guides, grids, margins, and bleed (`Gesso.View.PreviewMode`).
  - Pixel grid (IP-0044): extend `D03 T02 §2`'s pixel grid with View, Show, Pixel Grid, a threshold `Gesso.View.PixelGridMinZoom` (default 600 percent), and color and opacity keys.
  - Image window preferences (IP-0050): initial zoom (fit or 1:1) with Limit initial zoom to 100 percent, resize window on image change, and Show All by default, as `Gesso.View.*` keys the Preferences pages of `D03 T20 §4` list.
  - Budget: panning a 100-megapixel document at a 37-degree view rotation keeps the median frame under 16 ms (quoted with the machine); tests `ViewTransformTests` (round-trip of 10,000 random points under rotation, flip, and pixel aspect within 1e-9), `ZoomCommandsTests` (fit, fill, and zoom-to-selection against known bounds), `ToolCoordinatesUnderRotationTests`.
  - Commit: `"gesso: zoom, rotate and flip view, and screen modes"`
- **Proof:** unit plus driven: `ViewTransformTests` and `ToolCoordinatesUnderRotationTests` pass (a brush dab placed at a document point lands on that point at 37 degrees with the view flipped), and a driven run captures each screen mode, a rotated view, and Show All with the frame-time median quoted; cheaper substitute that fails: a WPF `RotateTransform` on the canvas control, which the tool-coordinate test catches.

#### §10. Windows, arrangement, view modes, display filters, and the navigator

- **Deliverable:** New windows on the same document, the arrange and match commands, shrink wrap, Affinity's view modes and split view, a view-only display filter stack (grayscale, clip warning, contrast, gamma), the Navigator panel with saved view points, and the Images panel.
- **Depends On:** §3
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the Window menu, new captures to docs/captures/gesso/navigator/, docs/captures/gesso/display-filters/, and docs/captures/gesso/split-view/. Job: a user can look at the same image several ways at once, compare, spot clipping, and jump to saved places. Treatment: Window, Arrange commands over AvalonDock, a split-view divider on the canvas, a Display Filters dialog per view, and dockable Navigator and Images panels. Cheaper substitute that fails: a clip warning drawn by modifying layer pixels, which the unchanged-document hash catches. Chrome: consume AvalonDock, §3's `ViewState`, `D03 T02 §2`'s `MipTileCache` for thumbnails, the GPU path of `D03 T02 §5`, and the icon catalog; do not add a second thumbnail renderer.
- **Runs:** `Requires: display-session -- window arrangement, split view, and panel captures need an interactive desktop`
- **Catalog:** IP-0052 to IP-0067 (16 features)
- **Hints:**
  - New Window (IP-0052, IP-0064): a second view on the same `GessoDocument` with its own `ViewState`, sharing history, selection, and dirty state; titled `name:2`; closing the last view closes the document with the usual prompt.
  - Arrange (IP-0053, IP-0063, IP-0064): Consolidate All to Tabs, Tile All Vertically and Horizontally, 2-up to 6-up layouts, Cascade, Float in Window, Float All in Windows, Match Zoom, Match Location, Match Rotation, and Match All across open documents.
  - Shrink Wrap (Ctrl+J) and Center Image in Window (Shift+J) from GIMP (IP-0054).
  - View modes (IP-0055): `ViewMode { Pixels, RetinaPixels, Vector, Wireframe }` per view with `Gesso.View.DefaultMode`; Retina renders at the monitor's device scale, Vector renders vector and text layer kinds at screen resolution, Wireframe draws their geometry and every layer's bounds; modes that need vector kinds fall back to Pixels until `D03 T16 §7` registers them.
  - Split view (IP-0056): a draggable vertical or horizontal divider (Affinity split and mirrored split) where each side has its own view mode and display filters.
  - `DisplayFilterStack` in `Isotone.Gesso.Rendering/Display/` (IP-0057, IP-0058, IP-0059, IP-0060): applied after compositing on display tiles only, never to document pixels or exports; filters Grayscale (Rec. 709 luminance in the document's tone curve), Clip Warning (shadows, highlights, NaN and infinite float values, and alpha options for partially and fully transparent pixels, each with a color), Contrast, and Gamma; per view, persisted in `Gesso.View.DisplayFilters`, one GPU shader per filter with CPU parity.
  - Navigator panel (IP-0061, IP-0067): thumbnail from the mip cache, draggable view box, zoom slider and buttons, proxy view-box color `Gesso.Navigator.ProxyColor`.
  - View points (IP-0062, IP-0066): named zoom, center, and rotation stored in the §1 block as `gesso:views`, added from the Navigator, with View, Previous View Point and Next View Point.
  - Open documents (IP-0065): the Window menu lists open documents; an Images panel (GIMP) in list or grid shows each with raise and new view.
  - Tests: `ClipWarningDisplayFilterTests` (a 1.0 pixel, a 0.0 pixel, and a NaN float pixel flagged; the document tile hash unchanged), `DisplayFilterGpuParityTests` (within 1/255, skipped without a DirectX 12 device), `ViewPointSerializationTests`, `WindowArrangementTests` over the layout model.
  - Commit: `"gesso: windows, view modes, display filters, and the navigator"`
- **Proof:** unit plus driven: `ClipWarningDisplayFilterTests` and the GPU parity tests pass, and a driven run tiles three documents 3-up, matches zoom, opens a split view with Wireframe on one side, and captures the Navigator with a saved view point; cheaper substitute that fails: a clip warning that writes colored pixels into the composite, which the tile-hash assertion catches.

#### §4. Rulers, units, guides, grids, and snapping

- **Deliverable:** One units converter shared with Stilus, rulers with origin and units, document guides with every Photoshop, Affinity, and GIMP guide command, configurable and axis grids, and a snapping engine on the shared snapping core with every candidate family, smart guides, pixel alignment, and a snapping manager.
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the rulers, new captures to docs/captures/gesso/guides/, docs/captures/gesso/grid/, and docs/captures/gesso/snapping/. Job: a user can place exact guides and grids in the units of the job and land moves, crops, and selections exactly where they mean. Treatment: ruler drags create guides, the View, Guides submenu and dialogs place them numerically, a Grid and Axis Manager configures grids, and a Snapping Manager lists every candidate with a check. Cheaper substitute that fails: guides kept in view-model memory, which a reopen loses. Chrome: consume the ported `Ruler` control (`D03 T01 §2`, extended), §3's `ViewTransform`, the overlay layer, the moved `UnitConverter` and snapping core, and the settings store; do not add a second units table or snap ranking.
- **Runs:** `Requires: display-session -- guide drags, grid display, and snapping feedback need an interactive desktop`
- **Catalog:** IP-0068 to IP-0093 (26 features)
- **Hints:**
  - First item: move `UnitConverter` from `src/Stilus/Isotone.Stilus.Core/Units/` (`D02 T07 §9`) into `src/Isotone.Core/Units/` as its second consumer with its tests into `tests/Isotone.Core.Tests/Units/`, repoint Stilus, and add the document-relative units percent and columns (`Gesso.Units.ColumnWidth`, `Gesso.Units.GutterWidth`) as context conversions; `grep -rn "class UnitConverter" src` finds one definition.
  - Custom units (IP-0070): a GIMP-style Units editor for user units (identifier, factor per inch, digits, symbol, abbreviation, singular, plural) stored in `%LOCALAPPDATA%\Rizonesoft\Gesso\units.json` and registered into the shared converter at startup.
  - Rulers (IP-0068, IP-0069): units from `Gesso.Units.Rulers` with a per-document override (`gesso:units`), a right-click units menu, corner drag to set the origin and double-click to reset, origin persisted in the §1 block, rulers document-aligned under §3's rotation.
  - `Guide` in `Isotone.Gesso.Core/Guides/` (orientation, position in document pixels as a double, optional color, optional `ArtboardId` that `D03 T09 §13` scopes) in `GessoDocument.Guides` with a document-level lock, persisted as `<gesso:guides>`; PSD resource 1032 read by the `D03 T04 §5` adapter now, written by `D03 T17 §2`, XCF by `D03 T17 §4`.
  - Guide commands, each one undoable step (IP-0071 to IP-0074, IP-0077, IP-0078): New Guide (orientation and position in any unit), New Guide by Percent, New Guide Layout (columns and rows by number, width, and gutter, margins, center guides, clear existing, presets in `Gesso.Guides.LayoutPresets`), New Guides from Selection or layer bounds (shape layers join when `D03 T16 §7` lands), Lock Guides (Alt+Ctrl+;), Clear Guides, Clear Selected Guides, Clear Canvas Guides.
  - Guide gestures (IP-0075, IP-0076, IP-0079): drag from a ruler (Alt switches orientation, Shift snaps to ruler ticks), move with the Move tool, Alt-drag clones, drag onto a ruler deletes; guides may sit off-canvas; double-click opens the guide edit dialog with position and per-guide color.
  - Grid (IP-0080, IP-0081, IP-0082): Show Grid (Ctrl+') and Show Guides (Ctrl+;); `GridSettings` (spacing in units, subdivisions, lines, dashed, dots, or intersection crosses, color, opacity, offset) per document as `<gesso:grid>` with `Gesso.Grid.*` defaults; Affinity's Grid and Axis Manager types (basic, advanced with separate X and Y spacing, isometric, dimetric, trimetric, oblique) through `AxisGrid` (axis angles and per-plane spacing); `GridOverlay` in `Isotone.Gesso.Rendering/Overlays/` under 1 ms per 1080p frame.
  - Snapping core move: move the geometry-agnostic parts of `D02 T07 §11` (`SnapCandidate`, `SnapResult`, the radius and priority ranking, and the equal-spacing and distance-label math of `SmartGuideProvider`) from `src/Stilus/Isotone.Stilus.Core/Snapping/` into `src/Isotone.Core/Snapping/` as their second consumer; Stilus's providers stay in Stilus and its snapping tests pass unchanged.
  - Gesso providers in `Isotone.Gesso.Core/Snapping/` (IP-0084, IP-0085, IP-0087): guides, grid (including axis grids), layer visual bounds (non-transparent extent cached per layer version), canvas edges and center, artboard edges and margins (registered by `D03 T09 §13`), selection bounds and pixel selection bounds; the crop tool and selection tools snap through the same engine; path and shape key points are registered by `D03 T16 §5` and `§7`, slices by `D03 T18 §3`.
  - Spacing, smart guides, and labels (IP-0083, IP-0086, IP-0090): equidistance, gap, and size candidates from the shared core; smart guides draw alignment lines and distance labels while moving layers or selections (`Gesso.SmartGuides.Enabled`).
  - Pixel alignment (IP-0088, IP-0092): Force Pixel Alignment (`Gesso.Snap.ForcePixelAlignment`) and Move by Whole Pixels (`Gesso.Snap.MoveByWholePixels`) round transforms and vector geometry to the pixel grid; the snapping toggle shortcut (Shift+Ctrl+;).
  - Snapping Manager (IP-0084, IP-0089, IP-0091, IP-0093): master toggle, Snap To All and None, per-candidate checks, tolerance `Gesso.Snap.TolerancePx` (default 8), presets `Gesso.Snap.Presets`, only visible layers, a per-layer Exclude from Snapping flag persisted through §1, and default snapping behavior keys.
  - Budget and tests: candidate search under 1 ms per pointer move with 500 layers and 200 guides; `GuideCommandTests`, `GuideSerializationTests` (native and PSD resource 1032), `GridSettingsSerializationTests`, `AxisGridTests`, `GessoSnapProviderTests`, and the moved `UnitConverterTests` and snapping-core tests.
  - Commit: `"gesso: rulers, units, guides, grids, and snapping on shared cores"`
- **Proof:** unit plus format fidelity plus driven: `GuideSerializationTests` reopen `tests/fixtures/gesso/guides/layout.gesso` and a Photoshop-produced `guides.psd` (tool and version recorded) with every guide equal, `GessoSnapProviderTests` pass, and a driven guide layout, grid, and snapped layer move are captured; cheaper substitute that fails: a second unit table in Gesso, which the single-definition grep catches.

#### §5. Measure, protractor, count, and notes

- **Deliverable:** A measure tool with protractor and hover distances, area and perimeter measurement, a measurement scale with scale markers, recorded measurements in a Measurement Log panel with CSV export, the Count tool with groups and automatic counting, and the Note tool with a Notes panel, all stored with the document.
- **Depends On:** §4
- **Phase:** 16
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/measure/, docs/captures/gesso/measurement-log/, docs/captures/gesso/count/, and docs/captures/gesso/notes/. Job: a user can measure distances, angles, and areas in real-world units, count features, keep a log they can export, and leave notes on the image. Treatment: the Ruler (measure), Count, and Note tools on one flyout with options-bar readouts, Analysis menu commands, and dockable Measurement Log and Notes panels; markers draw on the overlay, never into pixels. Cheaper substitute that fails: readouts in pixels only, which the scale test catches. Chrome: consume §4's `UnitConverter` and snapping, the overlay layer, the atomic writer for CSV, and AvalonDock; do not add a second readout surface.
- **Runs:** `Requires: display-session -- the measure, count, and note tools on the canvas need an interactive desktop`
- **Catalog:** IP-0094 to IP-0107 (14 features)
- **Hints:**
  - `MeasureTool` in `Isotone.Gesso.Core/Tools/` (IP-0094, IP-0095): drag a line, Alt-drag from an endpoint for a protractor, Shift constrains to 45 degrees; options-bar readouts X, Y, W, H, A, L1, L2 in current units and GIMP's optional info window; records no history; its Straighten Layer button hands the angle to §9's straighten.
  - `RegionMetrics` in `Isotone.Gesso.Core/Analysis/` (IP-0096): area by coverage-weighted pixel count, perimeter by border following (Suzuki and Abe 1985) on the selection or layer alpha, circularity 4 pi A over P squared, height, width, all in scale units.
  - Hover distances (IP-0097): with a layer or selection active, Ctrl-hover shows distances to the layer under the pointer and to the canvas edges (Photoshop).
  - `MeasurementScale` (IP-0098, IP-0099): pixel length, logical length, and logical units in the §1 block; Analysis, Set Measurement Scale with presets (`Gesso.Measure.ScalePresets`) and "from the current measure line"; Place Scale Marker (length, label font and size, text, color, bar) creates a `scale-marker` live layer registered with §1 that re-renders when the scale changes (a text layer once `D03 T16 §1` lands).
  - `MeasurementRecorder` (IP-0100): Analysis, Record Measurements over the selection, measure line, or count, with the data points chosen in `Gesso.Measure.DataPoints` (label, date and time, document, source, scale, scale units and factor, count, area, perimeter, circularity, height, width, gray minimum, maximum, mean, and median, integrated density, histogram).
  - Measurement Log panel (IP-0101): one row per record, sort by column, select, delete, and export CSV (RFC 4180, UTF-8) through the atomic writer; the log is saved with the document as `<gesso:measurements>`.
  - Notes (IP-0102, IP-0103, IP-0107): `Note` (position, author `Gesso.Notes.Author`, color, text, created) in the §1 block; Note tool, Show Notes (an Extras item), Clear All, and a Notes panel with previous and next; the PSD annotations resource maps through `D03 T17 §2` and `§3`.
  - Count (IP-0104, IP-0105, IP-0106): Count tool with numbered markers, count groups (name, color, visibility) with marker and label sizes, Clear, Show Count; Automatic Count from Selection counts 8-connected components of the selection mask above a minimum size (`ConnectedComponents` in `Isotone.Gesso.Core/Analysis/`).
  - Undo names "Add Note", "Add Count Marker", "Set Measurement Scale", "Record Measurement", "Place Scale Marker"; one Information line each; the measure tool writes none.
  - Tests: `MeasureToolTests` (distance and protractor angle on known points), `RegionMetricsTests` (a radius-50 disk's area within 0.5 percent and circularity above 0.99), `ConnectedComponentsTests`, `MeasurementLogExportTests` (CSV quoting), `NotesSerializationTests`.
  - Commit: `"gesso: measure, measurement log, count, and notes"`
- **Proof:** unit plus driven: `RegionMetricsTests` and `MeasurementLogExportTests` pass, and a driven run sets a scale from a measured line, records a selection's area, auto-counts five blobs, and exports the log (CSV committed as evidence); cheaper substitute that fails: a bounding-box area, which the disk-area test catches.

#### §11. Info, histogram, sample points, and scopes

- **Deliverable:** The Info panel with readouts, samplers, and status toggles, GIMP's Pointer dialog and sample points, status-bar readout choices and title and status formats, a Histogram panel with sources, statistics, and unique colors, and a Scope panel with waveforms, parade, vectorscope, and power spectral density.
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the status strip, new captures to docs/captures/gesso/info-panel/, docs/captures/gesso/histogram/, and docs/captures/gesso/scopes/. Job: a user can read exact color values at any point in any model, watch tonal distribution and clipping while editing, and judge color with video-style scopes. Treatment: dockable Info, Histogram, Scope, and Pointer panels in an Analysis group, sample points dragged from the rulers, a status-strip readout menu. Cheaper substitute that fails: an Info panel that shows only 8-bit RGB of the active layer. Chrome: consume `D01 T03 §4`'s `Histogram`, `D03 T05 §2`'s histogram control, `D01 T04 §1` conversions, `D03 T03 §1`'s status strip, and AvalonDock; do not add a second histogram computation.
- **Runs:** `Requires: display-session -- live panels, sample-point drags, and scope captures need an interactive desktop`
- **Catalog:** IP-0108 to IP-0125 (18 features)
- **Hints:**
  - `PixelSampler` in `Isotone.Gesso.Core/Analysis/`: samples the composite or the active layer at a point with sample size (point to 101 by 101 average, shared with `D03 T03 §8`'s eyedropper) and converts through `D01 T04` to RGB, HSB, HSV, LCh, Lab, xyY, CMYK (working CMYK profile), grayscale, web hex, total ink, and opacity; proof color joins when `D03 T18 §5` is active and is otherwise labeled "no proof".
  - `SamplePoint` (IP-0108, IP-0111, IP-0115): position, label, and readout mode per point (pixel, RGB percent or 0 to 255, gray, HSV, LCh, Lab, xyY, CMYK, total ink); placed GIMP-style by Ctrl-dragging from a ruler, moved and deleted with the Move tool, persisted as `<gesso:sample-points>`; the Color Sampler tool that places the same objects is `D03 T11 §9`'s, PSD and XCF mapping is `D03 T17`'s.
  - Info panel (IP-0109, IP-0111): two configurable readouts, pointer position in units, selection width and height, a sample-point list, and status toggles (document sizes, profile, dimensions, measurement scale, scratch sizes, efficiency, timing, current tool) with panel options.
  - Pointer dialog (IP-0114): pointer position in pixels and units, selection bounding box, two channel readouts, and Sample Merged.
  - Status strip and title (IP-0113, IP-0124): extend `D03 T03 §1`'s strip with a readout menu (document sizes as flattened and layered estimates, profile, dimensions, scratch sizes from the tile cache, efficiency as the share of tile reads served without spill, timing of the last operation, current tool) and GIMP-style format strings `Gesso.View.TitleFormat` and `Gesso.View.StatusFormat` (`%f` file, `%D` dirty, `%t` type, `%L` layer count, `%w`, `%h`, `%z` zoom, `%p` profile).
  - Memory readout (IP-0112): efficiency and pressure from `TileCache` hit and spill counters plus `GC.GetGCMemoryInfo()`, colored when spilling.
  - Histogram panel (IP-0110, IP-0116, IP-0117, IP-0118, IP-0119): channels (RGB, R, G, B, luminosity, colors, alpha), compact, expanded, and all-channels views, source (entire image, selected layer, adjustment composite), restriction to the selection and to a dragged range, statistics (mean, standard deviation, median, pixels, level, count, percentile, cache level), unique colors through §1's `UniqueColorCounter` restricted to the selection, 32-bit minimum and maximum, linear or logarithmic scale, linear or perceptual TRC, clipping counts at 0 and maximum, uncached refresh; computed on a worker, cancellable, cached per tile version.
  - Scope panel (IP-0120 to IP-0123): gain control; intensity waveform, RGB waveform, and RGB parade (per-column histograms accumulated into a 256-row image), vectorscope (BT.709 Cb and Cr with 75 percent targets and a skin-tone line at 123 degrees), and power spectral density (log magnitude of the centered 2D FFT of luminance on a 512 by 512 downsample); the FFT goes into `src/Isotone.Core/Imaging/Fourier/Fft2D.cs` (radix-2 with Bluestein for other sizes) so `D01 T06 §4`'s deconvolution reuses it.
  - Panels (IP-0125): Histogram, Info, Scope, and Pointer registered in AvalonDock and the Window menu in an Analysis group that also docks §5's Measurement Log.
  - Budget: a 24-megapixel 16-bit histogram under 150 ms (the `D01 T03 §4` budget), panels throttled to 10 updates per second while painting, zero allocations per update after warm-up.
  - Tests: `PixelSamplerTests` (Lab of sRGB 255, 0, 0 equals the lcms2 value within 0.1 delta E), `SamplePointSerializationTests`, `HistogramStatisticsTests` on synthetic ramps, `ScopeTests` (pure red lands on the vectorscope red target), `Fft2DTests` against a numpy 2.x golden for a 64 by 64 fixture within 1e-9.
  - Commit: `"gesso: info, sample points, histogram, and scopes"`
- **Proof:** unit plus driven: `PixelSamplerTests`, `HistogramStatisticsTests`, and `Fft2DTests` pass, and a driven run drags two sample points from the rulers, switches one to Lab, and captures the Histogram and Scope panels on a fixture photo; cheaper substitute that fails: readouts converted with hand-written sRGB formulas, which the lcms2 Lab comparison catches.

#### §6. History extensions: snapshots, non-linear history, and saved history

- **Deliverable:** A history tree over the suite history with non-linear branches, copy-on-write snapshots saved with the document, New Document and New Layer from a state, toggle last state, a history slider and advanced view, and a history log to metadata or a text file.
- **Depends On:** §1, D01 T02 §4
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/history/ (baseline from `D03 T03 §2`), new captures to docs/captures/gesso/snapshots/. Job: a user can try alternatives, keep named states, come back to them after reopening, and prove what was done to an image. Treatment: the History panel gains a snapshot area, branch rows, thumbnails and timestamps in an advanced view, and a scrub slider; a History Options dialog; File, New from state. Cheaper substitute that fails: snapshots as full-document copies, which the allocation test catches. Chrome: consume the `D01 T02 §4` history and `D03 T03 §2`'s panel and `TileSnapshotCommand` (extended, not replaced); do not add a second undo stack.
- **Runs:** `Requires: display-session -- the History panel, slider, and branch jumps need an interactive desktop`
- **Catalog:** IP-0129 to IP-0141 (13 features)
- **Hints:**
  - `HistoryTree` in `Isotone.Gesso.Core/History/` over the suite `UndoHistory` (`D01 T02 §4` keeps snapshots and persistence in Gesso): linear by default; with Allow Non-Linear History (`Gesso.History.AllowNonLinear`, IP-0136) an edit after an undo keeps the abandoned branch as indented rows, and selecting any state replays undo and redo along the tree path.
  - Snapshots (IP-0133, IP-0135): capture From Full Document, Merged Layers, or Current Layer with a name; tiles are shared copy-on-write through reference counts on the `D03 T02 §1` tile store, so capture copies no pixels; Restore is one history step "Restore Snapshot"; Delete; options: automatically create the first snapshot, new snapshot on save, show the New Snapshot dialog by default, make layer visibility changes undoable (`Gesso.History.VisibilityUndoable`).
  - Saved history (IP-0133, IP-0138, IP-0139): snapshots and, when `Gesso.History.SaveWithDocument` or the per-document flag is on, the full history are written through §1 as `<gesso:history>` with payloads under `gesso/history/`; each command implements `IPersistableCommand` (kind, JSON parameters, tile payload references); a command that cannot persist cuts the saved history before it and the save summary says so.
  - Toggle Last State (IP-0129) and a History slider that scrubs states with a live preview (Affinity, IP-0130).
  - Advanced view (IP-0131): 64-pixel thumbnails taken from the mip cache when a step completes (memory capped by `Gesso.History.ThumbnailBudgetMB`) and timestamps; Delete State (and every later state), Clear History with a confirmation (IP-0132).
  - New Document from a state or snapshot (IP-0134) and New Layer from a snapshot (IP-0140), the latter one undoable step "New Layer from Snapshot".
  - History log (IP-0137, IP-0141): `HistoryLogWriter` writes Sessions Only, Concise, or Detailed entries to the document's XMP history in the §1 block (exported by `D03 T17 §10`), to a text file (`Gesso.History.LogFile`), or both (`Gesso.History.LogTarget`, `Gesso.History.LogDetail`).
  - Budget: a snapshot of a 100-megapixel 16-bit document allocates under 1 MB until tiles diverge; saved history of 50 brush strokes adds at most twice their touched-tile bytes.
  - One Serilog Information line for snapshot create, restore, and delete and for history save; undo names as above.
  - Tests: `HistoryTreeTests` (a branch survives an edit after undo, and jumping to it restores the pixel hash), `SnapshotCopyOnWriteTests` (capture allocates no tile), `SavedHistoryRoundTripTests` (save, reopen, undo three steps equals the pre-edit hash), `HistoryLogWriterTests` (each detail level).
  - Commit: `"gesso: snapshots, non-linear history, and history saved with the document"`
- **Proof:** unit plus format fidelity: `SavedHistoryRoundTripTests` reopens `tests/fixtures/gesso/history/three-strokes.gesso` and undoes to the committed pre-edit hash, and `SnapshotCopyOnWriteTests` measures zero tile allocations at capture; cheaper substitute that fails: a snapshot that deep-copies the document, which the allocation assertion catches.

#### §7. The Image menu: canvas, rotation, trim, reveal, and resampling

- **Deliverable:** Canvas Size with relative size, offsets, extension color, and layer resizing; arbitrary rotation; crop to selection, trim, zealous crop, reveal all, fit canvas, clip canvas, and slice using guides; Image Size with units, separate resolutions, preview, and Fit To presets; Print Size; and the shared resampler extended with Photoshop, Affinity, and GIMP methods, Preserve Details, and pixel-art scalers.
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/image-size/ and docs/captures/gesso/canvas-size/ (baselines from `D03 T03 §7`), new captures to docs/captures/gesso/image-menu/. Job: a user can resize, resample, rotate, trim, and reshape the canvas with the exact method and units the job needs and see the result before committing. Treatment: extended Image Size and Canvas Size dialogs with a 1:1 preview pane, Print Size and Rotate Canvas dialogs, and Image menu commands. Cheaper substitute that fails: resampling through `SKBitmap.Resize`, which has no NoHalo or Lanczos goldens. Chrome: consume `D01 T03 §2`'s `Resampler` and `Rotator` (extended in place), `TileSnapshotCommand`, the §4 converter, and `Isotone.UI` dialog styles; do not add a second resampler in Gesso.
- **Runs:** `Requires: display-session -- the dialogs and their preview need an interactive desktop`
- **Catalog:** IP-0142 to IP-0163 (22 features)
- **Hints:**
  - Canvas Size (IP-0142, IP-0143): Relative, anchor grid, extension color (foreground, background, white, black, gray, other; transparent on non-background layers), GIMP's X and Y offsets with Center and Resize Layers (none, all, image-sized, visible), one command "Canvas Size".
  - Arbitrary rotation (IP-0144): Image, Image Rotation, Arbitrary through `Rotator` (`D01 T03 §2`) per layer, growing the canvas to hold the result; 90 and 180 degrees and flips stay `D03 T03 §7`'s.
  - Crop and trim (IP-0145, IP-0146, IP-0147, IP-0160): Crop to Selection (with Delete Cropped Pixels), Trim by transparent pixels, top-left color, or bottom-right color with per-side checkboxes (also GIMP's Crop to Content), and Zealous Crop (removes uniform rows and columns anywhere in the image).
  - Canvas fitting (IP-0148, IP-0149, IP-0150): Reveal All, Fit Canvas to Layers, Fit Canvas to Selection, and Clip Canvas (discards layer pixels outside the canvas).
  - Slice Using Guides (IP-0151): new untitled documents from the guide cells, refused by name above 500 cells.
  - Image Size (IP-0152, IP-0153, IP-0156, IP-0157, IP-0162): Constrain Proportions, units including percent, points, picas, and columns (§4 converter), Resample off (print size only), separate X and Y resolution, a 1:1 preview of the resampled result, Fit To presets (4 by 6 in, 5 by 7 in, 8 by 10 in at 300 ppi, 1024 by 768, 1280 by 800, 1366 by 768 at 72 ppi, plus saved `Gesso.ImageSize.Presets`), Auto resolution from a screen frequency (lines per inch times 1.5 for Good or 2 for Best), and Fit Image (fit within W by H with Don't Enlarge).
  - Print Size dialog (IP-0159, GIMP): width, height, and X and Y resolution that change resolution only and never resample.
  - Scale Styles (IP-0158): the resize command calls `IScalableLayerContent.Scale(factor)` on every layer's live content; `D03 T09 §7` registers layer effects, and until it ships the checkbox is disabled with a tooltip naming it.
  - Resampler extension (IP-0154): extend `Resampler` in `src/Isotone.Core/Imaging/Geometry/` (`D01 T03 §2`) in place with `Automatic` (Bicubic Sharper when reducing, Preserve Details when enlarging), `BicubicSmoother` (Mitchell-Netravali B = C = 1/3) and `BicubicSharper` (Keys cubic with a = -1), documented as Gesso's readings of Photoshop's options, `Lanczos2`, `Lanczos3NonSeparable` (radial, Affinity), and `NoHalo` and `LoHalo` translated from GEGL 0.4 (LGPL-3.0-or-later, headers kept, decision row); goldens from GIMP 3.2.6 `gimp-console` scaling per interpolation and libvips 8.16 for the Lanczos kernels.
  - Preserve Details (IP-0155, IP-0163): `DetailPreservingUpscaler` beside the resampler: Lanczos-3 upscale plus a guided-filter detail layer (He, Sun, and Tang 2010) boosted with a Reduce Noise slider that smooths the base; the "Preserve Details 2.0" option runs the same classical engine with a 1:1 preview and says so; AI upscaling is `D03 T19 §8`.
  - Pixel-art scalers (IP-0161): hq2x, hq3x, hq4x (Maxim Stepin's algorithm) and xBR 2x, 3x, 4x (Hyllian) as `ResampleMode` values in the same `Resampler`, integer factors only (others refused by name); goldens from FFmpeg 7.1 `hqx` and `xbr` filters.
  - Every command is one undo step through `TileSnapshotCommand`, reports progress and cancels above 16 megapixels, and logs one Information line (command, old and new size, method, milliseconds); a 100-megapixel Lanczos resample stays under the `D01 T03 §2` memory ceiling.
  - Tests: `CanvasCommandTests` (trim, zealous crop, reveal all, fit canvas on known layer bounds), `ResamplerExtensionTests` and golden fixtures under `tests/fixtures/imaging/resample-ext/`, `PrintSizeTests` (pixels unchanged).
  - Commit: `"gesso: the Image menu with canvas, trim, and extended resampling"`
- **Proof:** golden plus unit: `ResamplerExtensionTests` match GIMP 3.2.6 NoHalo and LoHalo within 2/255, libvips 8.16 Lanczos-2 within 2/255, and FFmpeg 7.1 hqx and xBR exactly (reference commands in each fixture's `reference.txt`), and `PrintSizeTests` prove the pixel hash unchanged; cheaper substitute that fails: mapping NoHalo to bicubic, which the NoHalo golden rejects.

#### §8. Clipboard and paste variants

- **Deliverable:** Cut, copy, copy merged, and clear across layers and groups, every paste variant (in place, into, outside, as new layer, as new image, floating), named buffers with a Buffers panel, Paste Special by format, Paste without Formatting, and Purge, through one clipboard service that writes PNG, DIBV5, and a private live-layer format.
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the Edit menu, new captures to docs/captures/gesso/buffers/ and docs/captures/gesso/paste-special/. Job: a user can move pixels and live layers between documents and other apps exactly where they need them. Treatment: Edit menu and Edit, Paste Special submenus, a Paste Special dialog listing the formats present, and a Buffers panel. Cheaper substitute that fails: a clipboard that carries only flattened 8-bit RGB, which the alpha and live-layer tests catch. Chrome: consume §2's `ClipboardImageReader` (extended), §1's contract for live layers, `TileSnapshotCommand`, and AvalonDock; do not add a second clipboard wrapper.
- **Runs:** `Requires: display-session -- clipboard exchange with other apps and the Buffers panel need an interactive desktop`
- **Catalog:** IP-0164 to IP-0180 (17 features)
- **Hints:**
  - `GessoClipboard` in `Isotone.Gesso.Desktop/Clipboard/` writes PNG (straight alpha), `CF_DIBV5`, and a private `Isotone.Gesso.Layers` format (layers serialized through §1 so live layers paste live between Gesso windows), with delayed rendering for large copies and `Gesso.Clipboard.ExportOnExit` to render on exit.
  - Cut, Copy, Copy Merged (Shift+Ctrl+C, GIMP's Copy Visible), and Clear (IP-0164, IP-0168, IP-0172, IP-0176, IP-0177) on the selected layers, and Cut across a layer group (IP-0175) as one step over every layer in the selected group.
  - Paste variants (IP-0165, IP-0166, IP-0173, IP-0178): Paste (centered in the view or selection), Paste in Place (Shift+Ctrl+V), Paste Into (new layer masked by the selection; Affinity's Paste Inside makes it a clipped child), Paste Outside (inverted mask), Paste as New Layer with optional in place, and Paste as New Image through §2.
  - Floating paste (IP-0167): a `FloatingLayer` kind (GIMP's floating selection) attached to its target with Anchor (Ctrl+H) and To New Layer (Shift+Ctrl+N); `D03 T10 §1` floats selections into the same kind.
  - Named buffers (IP-0169, IP-0170): Cut Named, Copy Named, and Copy Visible Named into a `BufferStore` (tiles shared copy-on-write, `Gesso.Clipboard.MaxBuffers`); a Buffers panel in list or grid with paste, paste into, paste as new layer, paste as new image, and delete.
  - Paste Special (IP-0174, IP-0180): lists the formats present (private layers, PNG, DIBV5, DIB, text, SVG, EMF) and pastes the chosen one; SVG and EMF entries and Prefer Metafile When Pasting (`Gesso.Clipboard.PreferMetafile`) are enabled when `D03 T17 §7`'s readers ship and carry a tooltip naming it until then.
  - Paste without Formatting (IP-0165, IP-0179): registered here, pasting plain text into a text layer in edit mode; enabled by `D03 T16 §1`, tooltip until then.
  - Purge (IP-0171): Edit, Purge, Clipboard, Histories (all documents, with a confirmation), and All; the video cache purge follows backlog B-043 and is absent.
  - Undo names "Paste", "Paste in Place", "Paste Into", "Paste Outside", "Cut", "Clear"; one Information line per paste with variant, format, and pixel size.
  - Tests: `ClipboardFormatTests` (PNG alpha round trip, DIBV5 straight and premultiplied conversion), `PasteVariantTests` (Paste Into's mask equals the selection), `BufferStoreTests`, `FloatingLayerTests` (anchor merges into the target in one step), `LiveLayerClipboardTests` (a probe live layer pastes live).
  - Commit: `"gesso: clipboard, paste variants, and named buffers"`
- **Proof:** unit plus driven: `ClipboardFormatTests` and `PasteVariantTests` pass, and a driven run copies a transparent layer from Gesso into another app and back (alpha hash quoted) and pastes a live layer between two Gesso windows; cheaper substitute that fails: copying a flattened 24-bit DIB, which the alpha round trip catches.

#### §9. Crop and straighten extensions

- **Deliverable:** Crop presets and numeric crop, center and selected-layer options, straighten, every overlay with cycling, classic mode and shield options, crop beyond the canvas with a fill hook for content-aware fill, auto shrink, and the Perspective Crop tool.
- **Depends On:** §7
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the crop options bar (baseline from `D03 T03 §7`), new captures to docs/captures/gesso/crop/ and docs/captures/gesso/perspective-crop/. Job: a user can crop to an exact size, ratio, or print format, straighten while cropping, and correct perspective in one step. Treatment: the crop options bar gains presets, swap, clear, numeric fields, overlay and shield menus; the Perspective Crop tool shares the flyout. Cheaper substitute that fails: a straighten that rotates without cropping to the largest rectangle, which the geometry test catches. Chrome: consume `D03 T03 §7`'s crop tool (extended), `D01 T03 §2`'s `Rotator` and `PerspectiveCorrector`, §4's snapping, and the settings store; do not add a second rotation routine.
- **Runs:** `Requires: display-session -- crop interaction and overlays need an interactive desktop`
- **Catalog:** IP-0181 to IP-0200 (20 features)
- **Hints:**
  - Presets (IP-0181, IP-0195): Unconstrained, Original Ratio, ratio, W by H by resolution, fixed aspect or size, units, and DPI with Resample; saved and deleted in `Gesso.Crop.Presets`; Swap (X) and Clear (IP-0182); numeric X, Y, W, H in the options bar (IP-0183).
  - Options (IP-0184, IP-0193): Expand from Center, Selected Layers Only (GIMP's current layer only), Auto Shrink to content with Shrink Merged; Delete Cropped Pixels stays `D03 T03 §7`'s.
  - Straighten (IP-0185, IP-0196, IP-0190): draw a line with the Straighten control or take the angle from §5's Measure tool; `Rotator.CropToRotatedRect` from `D01 T03 §2`; rotate the crop box by dragging outside it.
  - Overlays (IP-0186, IP-0187, IP-0197, IP-0200): thirds (existing), grid, diagonal, triangle, golden ratio, golden spiral; O cycles, Shift+O cycles orientation; display Always, Auto, or Never; Affinity's darken border and reveal canvas.
  - Classic mode, preview, and shield (IP-0188, IP-0189): Classic Mode (the box rotates, not the image), Show Cropped Area, Auto Center Preview, shield color and opacity with Auto Adjust Opacity.
  - Crop beyond the canvas (IP-0191, IP-0192, IP-0199): the canvas grows and the new area fills transparent or with the background; `ICanvasExtensionFill` is the hook `D03 T13 §3` registers for content-aware fill (the Content-Aware checkbox is disabled with a tooltip naming it until then); generative expand is `D03 T19 §4`.
  - Perspective Crop tool (IP-0194): four draggable corners, W, H, and resolution, Front Image, Show Grid; resampled through `PerspectiveCorrector`'s four-point homography (`D01 T03 §2`).
  - Modifiers (IP-0198): Shift constrains, arrows nudge, Ctrl overrides §4's snapping, Alt resizes around the center.
  - One undo step "Crop" or "Perspective Crop" with one Information line (box, angle, size, method).
  - Tests: `CropGeometryTests` (straighten angle yields the largest axis-aligned rectangle; golden-spiral geometry), `PerspectiveCropTests` against an ImageMagick 7.1 `-distort Perspective` golden within 2/255, `CropPresetStoreTests`.
  - Commit: `"gesso: crop presets, straighten, overlays, and perspective crop"`
- **Proof:** golden plus driven: `PerspectiveCropTests` match the ImageMagick 7.1 golden within 2/255 and `CropGeometryTests` pass, and a driven crop with a 4 by 5 preset and a straighten line is captured; cheaper substitute that fails: a perspective crop by affine skew, which the homography golden rejects.

#### Sizing concerns

- §3 carries 26 catalog features; grouping by view transform, zoom commands, navigation, physical views, rotate and flip, screen modes, padding, extras, and preferences keeps it near 25 items, with the window-level behaviors, birds-eye view, and flick panning the natural split if it overruns.
- §4 carries 26 catalog features plus two moves out of Stilus (the units converter and the snapping core); the moves count as two items each, so the grid and axis-grid items are the natural split if it overruns.

### todo/03-gesso/TODO-09-gesso-parity-layers.md -- `gesso-parity-layers`

- **Title:** "TODO-09 -- Gesso Parity: Layers, Masks, Blending, Styles, Smart Objects, and Artboards"
- **Phase(s):** 16, 17
- **Goal:** Gesso's layer stack reaches Photoshop, Affinity Photo, and GIMP parity: every layer kind (pixel, group, fill, container, symbol instance, and the kinds later files register: adjustment, text, shape, vector, smart object, link) with full locks, color labels, tags, filtering, isolation, and linked attributes; every Layer menu command including stamp, rasterize, Revert Rasterize, and matting; a mask stack per layer with pixel, vector, live (hue range, luminosity range, band pass), and compound masks, density, and feather; clipping masks with Affinity child semantics; blending options with fill opacity, knockout, Blend If, and Affinity blend ranges; every GIMP, Affinity, and Porter-Duff blend mode; layer styles with every Photoshop effect, contours, the Styles panel, and ASL import; embedded and linked smart objects and GIMP link layers; layer comps and Affinity states; align, distribute, and move-tool extensions; and artboards. The model lives in `src/Gesso/Isotone.Gesso.Core/Layers/` and `Masks/`, compositing in `src/Gesso/Isotone.Gesso.Rendering/` (render graph, blending, effects) with CPU and GPU parity, panels in `src/Gesso/Isotone.Gesso.Desktop/`; every live element persists through `D03 T08 §1`'s `gesso:` contract with a PNG fallback, every edit is one undoable command, and nothing live is flattened unless the user rasterizes or applies; it consumes the pixel engine (`D01 T03 §4`, `§6`) and moves Stilus's gradient model, link manager, and align math to `Isotone.Core` on their second consumer rather than copying them.
- **Current-state facts to verify (with claim candidates):**
  - `LayerType` names six kinds (raster, adjustment, group, text, shape, smart object) and `Layer` has one lock flag. `<!-- claim: count "^    (Raster|Adjustment|Group|Text|Shape|SmartObject),?$" src/Gesso/src/Gesso.Core/Layers/LayerType.cs = 6 -->` `<!-- claim: count "private bool _isLocked" src/Gesso/src/Gesso.Core/Layers/Layer.cs = 1 -->`
  - `LayerMask` is a whole-image byte buffer with density and feather already modeled, which §3 moves onto tiles. `<!-- claim: count "private byte\[\]\? _data" src/Gesso/src/Gesso.Core/Masks/LayerMask.cs = 1 -->` `<!-- claim: count "private float _density" src/Gesso/src/Gesso.Core/Masks/LayerMask.cs = 1 -->`
  - `VectorMask` keeps its own segment list (291 lines) and clipping is a static helper, not a render-graph node. `<!-- claim: lines src/Gesso/src/Gesso.Core/Masks/VectorMask.cs = 291 -->` `<!-- claim: count "public static class ClippingMask" src/Gesso/src/Gesso.Core/Masks/ClippingMask.cs = 1 -->`
  - `SmartObjectLayer` models embedded or linked with a source path and scale but holds no contents. `<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/SmartObjectLayer.cs = 117 -->` `<!-- claim: count "^    (Embedded|Linked),?$" src/Gesso/src/Gesso.Core/Layers/SmartObjectLayer.cs = 2 -->`
  - `BlendMode` already names GIMP and Affinity modes (grain merge, reflect, glow) that nothing implements, and no layer styles, comps, or artboards exist. `<!-- claim: count "GrainMerge = 91" src/Gesso/src/Gesso.Core/Layers/BlendMode.cs = 1 -->` `<!-- claim: count "LayerStyle|DropShadow|LayerEffect" src/Gesso/src/**/*.cs = 0 -->` `<!-- claim: count "LayerComp|Artboard" src/Gesso/src/**/*.cs = 0 -->`
- **Inputs and XREFs:** `standards/gesso.md`, `standards/shared.md`, `standards/testing.md`; W3C Compositing and Blending Level 1 and Porter and Duff 1984 (compositing operators); GEGL 0.4 operation reference and GIMP 3.2.6 layer modes (legacy and default) as goldens through `gimp-console`; Krita 5.2 composite ops as the golden for Affinity-named modes; Adobe Photoshop File Formats Specification (layer records, blending ranges, `lfx2` effect descriptors, `lsct` section dividers, `knko`, `iOpa`, `lclr`, `SoLd`/`PlLd` placed layers) with psd-tools 1.10 (MIT) as the reading oracle; Felzenszwalb and Huttenlocher 2012 (Euclidean distance transform); Reinhard, Ashikhmin, Gooch, and Shirley 2001 (color transfer); Kubelka and Munk 1931 (pigment mixing); -> XREF: D03 T08 §1 (the native contract every kind here registers with); -> XREF: D03 T08 §4 (guides and the snapping engine §12 and §13 use and register candidates with); -> XREF: D03 T08 §7 (the Scale Styles hook §7 registers); -> XREF: D03 T08 §8 (the floating layer kind and Paste Into masks); -> XREF: D03 T03 §3 (the Layers panel §1 and §2 extend); -> XREF: D03 T03 §4 (the Move tool §12 extends); -> XREF: D03 T02 §3 (the render graph §3 to §8 extend); -> XREF: D03 T02 §4 (blend modes §6 extends); -> XREF: D03 T02 §5 (GPU parity for every compositing path here); -> XREF: D03 T04 §4 (native format); -> XREF: D03 T04 §5 (the PSD adapter §1, §3, §4, and §5 extend with locks, labels, masks, clipping, and blending ranges); -> XREF: D01 T02 §4 (suite history); -> XREF: D01 T03 §4 (`ToneCurve` for contours and blend-range curves); -> XREF: D01 T03 §6 (Gaussian blur for effects and live masks); -> XREF: D02 T09 §7 (Stilus's gradient model, moved to `Isotone.Core` by §8); -> XREF: D02 T12 §7 (Stilus's `LinkManager`, moved to `Isotone.Core` by §10); -> XREF: D02 T08 §14 (Stilus's align and distribute math, moved to `Isotone.Core` by §12); -> XREF: D01 T06 §8 (reuses §8's `SurfaceLighting`); -> XREF: D01 T06 §13 (reuses §14's distance transform); -> XREF: D03 T10 §1 (selections to and from masks); -> XREF: D03 T10 §7 (Refine for §3's masks and §14's decontamination); -> XREF: D03 T11 §1 (adjustment layers register with §1 and take §5's blend ranges); -> XREF: D03 T12 §9 (gradient fill layers and the gradient editor over §8's moved model); -> XREF: D03 T12 §10 (the Patterns panel behind §8's pattern library interface); -> XREF: D03 T13 §6 (warp on §9's smart objects); -> XREF: D03 T14 §1 (smart filters on §9's smart objects); -> XREF: D03 T15 §4 (32-bit editing uses §6's float mode subset); -> XREF: D03 T16 §1 (text layers register with §1 and take §7's styles and §4's clipping); -> XREF: D03 T16 §5 (paths for §4's vector masks, rebasing `VectorMask` on the shared geometry); -> XREF: D03 T16 §7 (shape and vector layer kinds register with §1); -> XREF: D03 T17 §2, D03 T17 §3, and D03 T17 §13 (PSD write and read of everything here); -> XREF: D03 T17 §4 and D03 T17 §14 (XCF modes, link layers, and masks); -> XREF: D03 T19 §1 (AI results land as masked layers in groups).
- **Adjacency:** list=applicable (Layers panel filtering, saved searches, and search patterns in §1; Links panel §2; Styles panel §8; Resource Manager §10; Layer Comps and States panels §11); document=not-applicable (layers print through the composite; print is D03 T18 §6); settings=applicable (every panel option, default, and behavior is a `Gesso.*` key with a named consumer); reporting=applicable (smart-object and resource status in §9 and §10, invalid-comp warnings in §11, the rasterize and fallback report); notifications=applicable (progress and cancel for style rendering, rasterize, merge, and package; modified-link prompts in §10); permissions=applicable (locked layers refuse edits by name in §1; missing, locked, or read-only linked files are reported and refused by name in §10); audit=applicable (every command is one history entry with one Serilog Information line); exchange=applicable (the `gesso:` contract, PSD through D03 T17, ASL styles in §8, Package in §10); reverse=applicable (every command undoes; Revert Rasterize in §14; release, unlink, and ungroup commands)

#### §1. The layer model: every layer kind, locks, labels, and panel filtering

- **Deliverable:** The layer model gains fill, container, and symbol-instance kinds and a registration path for the kinds later files add, full lock modes, color labels and tags, Layers panel filtering and pattern search, isolation, and Edit All Layers.
- **Depends On:** D03 T08 §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/layers/ (baseline from `D03 T03 §3`), new captures to docs/captures/gesso/layers-filter/ and docs/captures/gesso/symbols/. Job: a user can make any kind of layer, protect it exactly as needed, label and tag it, and find any layer in a large document. Treatment: the Layers panel gains lock buttons, label colors, a filter bar with kind and attribute toggles and a pattern search, and an isolate toggle; a Symbols panel. Cheaper substitute that fails: one Locked checkbox, which the per-lock refusal tests catch. Chrome: consume `D03 T03 §3`'s panel (extended), the icon catalog, `D03 T08 §1`'s registry, and the settings store; do not add a second list control.
- **Runs:** `Requires: display-session -- the Layers panel filter, locks, and Symbols panel need an interactive desktop`
- **Catalog:** IP-0217 to IP-0227 (11 features)
- **Hints:**
  - `LayerType` gains `Fill`, `Vector`, `Container`, `Link`, `SymbolInstance`, `Floating` (from `D03 T08 §8`), and `Artboard` (from §13) beside today's six (IP-0217); each non-raster kind registers with `D03 T08 §1`'s `GessoElementRegistry`: this section registers `fill`, `container`, and `symbol-instance`; `adjustment` is `D03 T11 §1`'s, `text` `D03 T16 §1`'s, `shape` and `vector` `D03 T16 §7`'s, `smart-object` §9's, `link` §10's.
  - `FillLayer` with `IFillContent` and `SolidColorFill` (IP-0225): renders into tiles on demand from its parameters, stores no pixels, writes a fallback PNG at save; gradient and pattern contents register in `D03 T12 §9` and `§10`.
  - `ContainerLayer` (Affinity): a group whose children are clipped to the container's own content and mask; `GroupLayer` stays the pass-through or isolated group.
  - Symbols (IP-0218): `SymbolDefinition` (id, name, child tree) in the `D03 T08 §1` document block as `<gesso:symbols>`; `SymbolInstanceLayer` references it with its own transform; with Sync on, an edit inside any instance edits the definition and every instance re-renders as one compound command; Detach, Select All Instances, and a Symbols panel (create from selection, insert, rename, delete).
  - `LayerLocks` flags (IP-0220): Transparency, Pixels, Position, Visibility, ArtboardNesting, and All replace `Layer.IsLocked`; Lock All Layers in Group; every tool and command calls `LockGuard.Require(layer, LockKind)` and refuses by name ("Layer Sky has locked pixels").
  - Properties, labels, and tags (IP-0219, IP-0221): `ColorLabel` (none, red, orange, yellow, green, blue, violet, gray) and a `Tags` set, a Layer Properties dialog (name, label, tags), and Select Same Label or Tag.
  - Filtering (IP-0222): a filter bar by kind, name, effect, mode, attribute (visible, locked, empty, linked, clipped, masked, has effects), color label, smart-object kind (embedded, linked, stale), selected, and artboard, with saved searches in `Gesso.Layers.SavedSearches` and a filter on-off switch.
  - `NamePattern` in `Isotone.Gesso.Core/Search/` (IP-0227): plain text, glob, or regular expression (GIMP 3 layer search syntax) with a 100 ms `MatchTimeout`; `D03 T16 §4`'s text find and replace reuses it.
  - Isolation (IP-0223, IP-0226): Isolate Layers filters the panel to the selection, and Alt-click isolated editing renders one layer or group alone as view-only state that never enters history.
  - Edit All Layers (IP-0224): `Gesso.Layers.EditAllLayers` makes Select All select every layer and makes pixel-sampling selection tools sample all layers.
  - Persistence through `D03 T08 §1` for kinds, locks, labels, tags, and symbols; the `D03 T04 §5` adapter maps PSD lock flags and `lclr` color labels now.
  - Undo names "Set Layer Locks", "Set Label", "Create Symbol", "Detach Symbol"; one Information line each.
  - Tests: `LayerLockTests` (each lock refuses its operation by name), `FillLayerTests` (renders, reopens live), `SymbolSyncTests` (an edit in one instance reaches the others and undoes in one step), `NamePatternTests` (glob, regex, and a catastrophic pattern timing out), `LayerFilterTests`.
  - Commit: `"gesso: every layer kind, locks, labels, and layer filtering"`
- **Proof:** unit plus format fidelity: `SymbolSyncTests` and `LayerLockTests` pass, and `tests/fixtures/gesso/layers/kinds.gesso` (fill, container, symbol instances) reopens live and renders in GIMP 3.2.6 as `.ora` within 1/255 of Gesso's composite; cheaper substitute that fails: symbol instances stored as copies, which the sync test catches.

#### §2. Layers panel extensions: selection, linking, visibility, order, and options

- **Deliverable:** The Layers panel gains the full New Layer dialog, solo visibility and eye drags, nested-group controls, arrange order, insertion targets, keyboard layer selection, select similar, opacity keys, linked layers and Affinity linked duplicates with linkable attributes, panel options, the complete Layer menu, the Layer Attributes dialog, and multi-selection shared with channels and paths.
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/layers/ (baseline from `D03 T03 §3`), new captures to docs/captures/gesso/new-layer/, docs/captures/gesso/links-panel/, and docs/captures/gesso/layers-options/. Job: a user can select, order, show, and relate many layers fast by mouse and keyboard. Treatment: New Layer and Layer Attributes dialogs, eye-column gestures, a Links panel, a Panel Options dialog, and every command in the Layer menu and context menu. Cheaper substitute that fails: linked layers that move together only while selected, which the propagation test catches. Chrome: consume `D03 T03 §3`'s panel and keymap, the suite history, and `Isotone.UI` dialog styles; do not add a second selection model.
- **Runs:** `Requires: display-session -- panel gestures, dialogs, and keyboard selection need an interactive desktop`
- **Catalog:** IP-0228 to IP-0247 (20 features)
- **Hints:**
  - New Layer dialog (IP-0228, IP-0246): name, color label, mode, opacity, Use Previous Layer to Create Clipping Mask, fill with neutral color for the mode, GIMP's size, offset, fill type, and switches (visible, linked, lock pixels, lock position, lock alpha), blend and composite space; Ask for a Name when creating layers and groups (`Gesso.Layers.AskForName`, Alt-click inverts).
  - Visibility (IP-0229): Alt-click solos, Show or Hide Other Layers, Show All Layers, drag across eyes to toggle many.
  - Groups (IP-0230): expand and collapse all, group visibility, opacity, and masks, and drop a layer out of its parent.
  - Order (IP-0231): Bring to Front (Shift+Ctrl+]), Forward (Ctrl+]), Backward (Ctrl+[), Send to Back (Shift+Ctrl+[), Reverse.
  - Insertion target (IP-0232, IP-0245): `Gesso.Layers.InsertTarget` (above the selection, behind it, at the top, inside the selected group) with a sticky option, read by every command that creates a layer.
  - Selection (IP-0233, IP-0234, IP-0235, IP-0243): multi-select with Ctrl and Shift; next and previous (Alt+] and Alt+[), top and bottom, parent, and all layers (Alt+Ctrl+A); Select Similar (same kind) and Same Name; Alt-right-click on the canvas reveals the layer in the panel; an `ItemSelection` model that `D03 T10 §10` (channels) and `D03 T16 §5` (paths) reuse for their multi-selection.
  - Opacity keys (IP-0236): 1 to 9 set 10 to 90 percent, 0 sets 100, two quick digits set exact values, Shift targets fill opacity once §5 lands.
  - Linked layers (IP-0237): Link Layers and Select Linked Layers; a move or transform of one moves all.
  - Linked duplicates (IP-0238, IP-0239, IP-0247): Affinity's Duplicate Linked with a `LinkSet` (id and linked-attribute flags: transform, pixels, blending, opacity, effects, adjustment and filter parameters, shape style); `LinkPropagator` replays an edit on each peer inside one compound command; a Links panel lists sets with relink, unlink, and navigate.
  - Panel options and menus (IP-0240, IP-0241, IP-0244): thumbnail size and contents (layer bounds or document), checkerboard background, type icons, group thumbnails, auto-scroll, add default masks on fill layers, copy name suffix; the full Layer menu and context menu with owner tooltips for commands later files enable; Delete removes the targeted mask when a mask is targeted.
  - Layer Attributes dialog (IP-0242, GIMP): name, color tag, mode, blend space, composite space and mode, opacity, offsets, and switches as one command.
  - Tests: `LinkPropagatorTests` (a transform on one linked duplicate reaches its peers and undoes in one step, pixels unlinked stay separate), `InsertTargetTests`, `LayerSelectionCommandTests`, `NewLayerDialogViewModelTests`.
  - Commit: `"gesso: layers panel selection, linking, visibility, and options"`
- **Proof:** unit plus driven: `LinkPropagatorTests` pass, and a driven run creates linked duplicates, edits one, solos a layer, and reorders with the keyboard, with log lines quoted and captures committed; cheaper substitute that fails: link sets that copy attributes once at creation, which the propagation test catches.

#### §14. Layer menu commands: merge, stamp, rasterize, matting, and boundaries

- **Deliverable:** Merge visible with GIMP's options, merge selected and groups, stamp visible and selected, background conversions, alpha add and remove, layer via copy and cut, duplicate to another document, delete hidden and empty layers, rasterize every live kind with Revert Rasterize, rasterize to mask, matting, and layer boundary commands.
- **Depends On:** §2
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the Layer menu, new captures to docs/captures/gesso/merge-visible/, docs/captures/gesso/layer-boundary/, and docs/captures/gesso/matting/. Job: a user can combine, convert, and clean up layers without losing the live source by accident. Treatment: Layer menu commands with small dialogs (Merge Visible options, Duplicate Layer destination, Layer Boundary Size, Defringe width) and a rasterize confirmation that names what becomes pixels. Cheaper substitute that fails: rasterize that discards the parameters, which Revert Rasterize exposes. Chrome: consume the render graph for merges, `TileSnapshotCommand`, the §1 registry, and `Isotone.UI` dialog styles; do not add a second compositor for merges.
- **Runs:** `Requires: display-session -- the dialogs and driven merges need an interactive desktop`
- **Catalog:** IP-0248 to IP-0263, IP-0503, IP-0521 (18 features)
- **Hints:**
  - Merges (IP-0248, IP-0254): Merge Visible with GIMP's options (expanded as necessary, clipped to image, clipped to bottom layer, discard invisible), Merge Selected (Ctrl+E), Merge Down, and Merge Group, all composited through the render graph so the result equals the composite within 1/255.
  - Stamp (IP-0255): Stamp Visible (Shift+Ctrl+Alt+E) and Stamp Selected into a new layer, sources kept.
  - Background (IP-0249, IP-0250): the Background layer (locked position, no transparency) with Layer from Background and Background from Layer; Add and Remove Alpha Channel (GIMP), removal filling with the background color.
  - Via copy and cut (IP-0251, IP-0262): Layer via Copy (Ctrl+J) and Layer via Cut (Shift+Ctrl+J) from the selection, or the whole layer with no selection.
  - Duplicate (IP-0252): Duplicate Layer or Group with a destination of this document, another open document, or a new document.
  - Cleanup (IP-0253, IP-0263): Delete Hidden Layers and Delete Empty Layers (empty means every tile transparent, found from the tile grid without reading pixels).
  - Rasterize (IP-0256, IP-0257): Rasterize Layer, Style, Fill Content, Vector Mask, Smart Object, All Layers, with Trim (Affinity Rasterize and Trim) and automatic rasterize on paint (`Gesso.Layers.AutoRasterizeOnPaint`, ask, always, or never); Rasterize to Mask turns a layer's luminance or alpha into a mask on the layer below.
  - Revert Rasterize (IP-0258, GIMP 3.2): rasterizing keeps the live parameters in a `RasterizedFrom` record (persisted through `D03 T08 §1` as `<gesso:rasterized-from>`); Layer, Revert Rasterize restores the live layer after a confirmation that names the pixel edits it discards.
  - Matting (IP-0259): `Isotone.Gesso.Core/Layers/Matting/`: Remove Black Matte and Remove White Matte (C = (C_observed minus (1 minus alpha) times M) over alpha), Defringe by width (edge colors replaced from the nearest opaque interior pixel), and Color Decontaminate by amount; `D03 T10 §7`'s Select and Mask output reuses `ColorDecontaminator`.
  - Distance transform: Defringe finds the nearest opaque pixel with an exact Euclidean distance transform (Felzenszwalb and Huttenlocher 2012, with the nearest-site index) added here as `src/Isotone.Core/Imaging/Morphology/DistanceTransform.cs`, because §7's layer effects and `D01 T06 §13`'s morphology filters need the same primitive; `DistanceTransformTests` compare it with brute force on random masks.
  - Boundaries (IP-0260, IP-0261): Layer to Image Size, Resize Layer to Selection, Crop Layer to Content, and GIMP's Layer Boundary Size dialog (size, offsets, fill).
  - Each command is one undo step with one Information line naming the command, layer ids, and result size.
  - Tests: `MergeVisibleTests` (each option's bounds; result equals the composite within 1/255), `RevertRasterizeTests` (a probe live layer rasterizes and reverts to equal parameters), `MattingTests` (black matte removal restores a known straight color within 1/255), `EmptyLayerDetectionTests`.
  - Layer > Matting (IP-0259, IP-0503, IP-0521): defringe, color decontaminate, remove black matte, remove white matte, sharing the decontamination kernel with D03 T10 §7.
  - Commit: `"gesso: merge, stamp, rasterize with revert, matting, and layer boundaries"`
- **Proof:** unit plus driven: `MergeVisibleTests` and `RevertRasterizeTests` pass, and a driven run stamps visible, rasterizes a fill layer, and reverts it with log lines quoted; cheaper substitute that fails: a merge that re-implements blending outside the render graph, which the equals-the-composite assertion catches on the every-mode fixture of `D03 T02 §4`.

#### §3. Layer masks

- **Deliverable:** A mask stack per layer with tiled pixel masks, every add mode, apply, delete, disable, link, invert, view alone and overlay, density and feather, mask to selection, painting on masks, Affinity's mask layers, compound masks, the Mask tool, and live hue-range, luminosity-range, and band-pass masks. -> SOURCE: legacy-gesso-1.6
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/layers/ for mask thumbnails, new captures to docs/captures/gesso/masks/ and docs/captures/gesso/live-masks/. Job: a user can hide and reveal parts of any layer non-destructively, refine the mask at any time, and build masks that follow the image's hue, tone, or detail. Treatment: mask thumbnails beside layer thumbnails, a Masks page in the Properties panel (density, feather, invert, Refine), live mask editors with a hue wheel or curve, a rubylith overlay, and the Mask tool. Cheaper substitute that fails: a mask applied into the pixels when added, which the disable test catches. Chrome: consume the render graph, `D01 T03 §6` blur, the color panel's grayscale mode, `TileSnapshotCommand`, and the icon catalog; do not add a second mask renderer.
- **Runs:** `Requires: display-session -- painting on masks, overlays, and live-mask editors need an interactive desktop`
- **Catalog:** IP-0278 to IP-0298 (21 features)
- **Hints:**
  - Promoted from backlog B-015 (carries `-> SOURCE: legacy-gesso-1.6`); delete the B-015 line from `todo/backlog.md` in the authoring commit, B-016 and B-019, which name B-015 in `needs:`, are promoted in the same integration (by §7 and `D03 T16 §7`), so no live entry is left pointing at it.
  - First item: back `LayerMask` with a one-channel `TileGrid` (8, 16, or 32-bit following the document) instead of today's whole-image `byte[]`, keeping its density, feather, enabled, linked, and inverted properties; `MaskTools` operate per tile.
  - `MaskStack` on every layer: an ordered list of `MaskNode` (pixel mask, vector mask from §4, live mask, compound mask) each with enabled, inverted, density, feather, opacity, and a combine op; the render graph resolves one coverage tile per output tile; density and feather are non-destructive (IP-0287, IP-0297).
  - Add modes (IP-0282, IP-0295): Reveal All, Hide All, from Selection, from Transparency, Transfer Alpha, from Channel, Grayscale Copy of Layer, Invert; Edit Mask Immediately (`Gesso.Masks.EditImmediately`) targets the new mask.
  - Commands (IP-0283, IP-0284, IP-0285, IP-0298): Apply, Delete, Disable (Shift-click), target mask or layer (Ctrl+\ and Ctrl+2), link and unlink, drag to move and Alt-drag to copy a mask, Invert, Clear, Fill, Release to Layer (Affinity), and Flatten All Masks.
  - Viewing and selection (IP-0286, IP-0288): Alt-click views the mask alone; backslash toggles a rubylith overlay with color and opacity (`Gesso.Masks.OverlayColor`, `Gesso.Masks.OverlayOpacity`); Ctrl-click loads the mask as a selection, Ctrl+Shift adds, Ctrl+Alt subtracts, Ctrl+Shift+Alt intersects.
  - Painting (IP-0289): brushes, erasers, fills, and gradients write to the targeted mask; the color panel switches to grayscale while a mask is targeted.
  - Mask layers (IP-0291): Affinity masks as child layers with opacity, blend mode, and their own parent masks; dragging a layer onto another's mask slot converts it.
  - Compound masks (IP-0292): add, subtract, intersect, and xor combine ops across the stack.
  - Mask tool (IP-0290, Affinity 3.3): paints or draws an editable gradient into an auto-created mask; its Refine Edges button is enabled by `D03 T10 §7` and names it until then.
  - Live masks (IP-0278, IP-0279, IP-0280, IP-0281, IP-0293, IP-0294): `LiveMask` nodes computed from the composite below (or the parent's content), recomputed when those tiles change: hue range (hue wheel with nodes and ramps, picker, blur), luminosity range (luminance curve, linear mode, blur), and band pass (difference of Gaussians between a low and a high band radius into an intensity curve, blur); each invertible, paintable over, with presets in `Gesso.Masks.LivePresets`; Luminosity Mask from Layer creates a pixel mask from the layer's luminance; each registers `live-mask` with `D03 T08 §1`.
  - Delete on image layers (IP-0296): with `Gesso.Masks.DeleteMasksImageLayers` on, Delete on an image layer with a selection adds a mask instead of rasterizing.
  - PSD layer masks and user masks, including density and feather, map through the `D03 T04 §5` adapter now.
  - Tests: `MaskStackTests` (density 50 percent halves coverage; disable restores the unmasked composite; compound xor), `LiveMaskTests` (a hue-range mask over a hue ramp selects the chosen band; editing the pixels below updates the mask tiles), `MaskTileBudgetTests` (painting one dab touches only its tiles).
  - Commit: `"gesso: layer masks, mask stacks, and live masks"`
- **Proof:** unit plus format fidelity: `MaskStackTests` and `LiveMaskTests` pass, and a PSD fixture with a layer mask at 60 percent density and 4 px feather (Photoshop-produced, version recorded) composites within 2/255 of its exported PNG; cheaper substitute that fails: masks multiplied into pixels on creation, which the disable assertion catches.

#### §4. Clipping masks and vector masks

- **Deliverable:** Clipping masks with multiple clipped layers and Affinity's child clipping, vector masks from shapes, selections, and (when paths exist) paths, with disable, link, and conversion to a pixel mask, and text filled with an image by clipping.
- **Depends On:** §3
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/layers/ for the clip indicator, new captures to docs/captures/gesso/clipping/. Job: a user can make a layer show only inside another layer's content or inside a resolution-independent outline. Treatment: Alt-click between layers clips, a clip arrow in the panel, Affinity nesting by dragging a layer onto another, and vector-mask thumbnails. Cheaper substitute that fails: clipping by merging, which the release test catches. Chrome: consume §3's mask stack and render graph and `D03 T08 §4`'s snapping; do not add a second path type beyond today's `VectorMask` until `D03 T16 §5` rebases it.
- **Runs:** `Requires: display-session -- clipping gestures and vector mask editing need an interactive desktop`
- **Catalog:** IP-0299 to IP-0303 (5 features)
- **Hints:**
  - `ClipGroupNode` in `Isotone.Gesso.Rendering/RenderGraph/` replaces the static `ClippingMask` helper: a base layer plus the consecutive clipped layers above it, each clipped by the base's alpha and mask.
  - Clipping commands (IP-0299): Create Clipping Mask (Alt+Ctrl+G), Release, Alt-click between layers, and New Layer with Use Previous Layer to Create Clipping Mask from §2.
  - Affinity child clipping (IP-0301): a layer nested inside a pixel or shape layer clips to it; Move Inside and Move Outside; auto-clip brush strokes to the selected child (`Gesso.Layers.ClipBrushToChild`); isolated child blending; Select Clipped Object.
  - Vector masks (IP-0300, IP-0302): Add Vector Mask Reveal All or Hide All, from a rectangle or ellipse drawn with the shape gesture, from the current selection through `SelectionOutliner` (border following plus Douglas-Peucker at `Gesso.Masks.OutlineTolerancePx`, default 2.0, placed in `Isotone.Gesso.Core/Selection/` so `D03 T16 §5`'s Make Work Path reuses it), and from the current path (enabled by `D03 T16 §5`, tooltip until then); Delete, Disable, Link, and Convert to Pixel Mask; rasterized with SkiaSharp at the document's resolution on every render, never stored as pixels.
  - `VectorMask` keeps its segment list here; `D03 T16 §5` rebases it on the shared `Isotone.Core/Vector/` geometry as that section's first item.
  - Fill text with an image (IP-0303): a pixel layer clipped to a text layer works through the same node when `D03 T16 §1` registers text; the fixture here uses a shape-alpha base.
  - PSD clipping flags and vector masks (`vmsk`) map through the `D03 T04 §5` adapter now.
  - One undo step per command; one Information line each.
  - Tests: `ClipGroupNodeTests` (three layers clipped to a base with a mask equal the reference composite), `VectorMaskFromSelectionTests` (an elliptical selection yields an outline within tolerance), `ChildClippingTests`.
  - Commit: `"gesso: clipping masks, child clipping, and vector masks"`
- **Proof:** golden plus unit: `ClipGroupNodeTests` match a GIMP 3.2.6 composite of the same stack (clip to backdrop) within 1/255, and a Photoshop-produced PSD with a clipping group and a vector mask composites within 2/255 of its exported PNG; cheaper substitute that fails: clipping by merging the clipped layers into the base, which the Release test catches.

#### §5. Blending options and Blend If

- **Deliverable:** Blending options per layer (fill opacity with the special eight modes, channel restrictions, knockout, blend interior effects and clipped layers as group, transparency shapes, masks hide effects), Blend If with split sliders, Affinity blend ranges and blend gamma, per-layer antialiasing and coverage map, GIMP composite mode and blend and composite spaces, blend ranges on adjustment layers, and the live tone blend group.
- **Depends On:** §1
- **Phase:** 16
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/blending-options/ and docs/captures/gesso/blend-ranges/. Job: a user can control exactly how a layer combines with what is below it, by channel and tone, without masks. Treatment: the Blending Options page of the Layer Style dialog (Photoshop layout) and an Affinity Blend Ranges dialog with source and underlying curves per channel. Cheaper substitute that fails: Blend If implemented as a hard threshold, which the split-slider ramp test catches. Chrome: consume the render graph, `D01 T03 §4`'s `ToneCurve` for range curves, GPU parity from `D03 T02 §5`, and `Isotone.UI` dialog styles; do not add a second blend path.
- **Runs:** `Requires: display-session -- the dialog and live preview need an interactive desktop`
- **Catalog:** IP-0304 to IP-0317 (14 features)
- **Hints:**
  - `BlendingOptions` record on `Layer` (mode, opacity, fill opacity, channel mask, knockout, flags, blend ranges, blend gamma, composite mode, blend space, composite space, antialiasing); evaluated in `Isotone.Gesso.Rendering/Blending/` on both the CPU and GPU paths.
  - General blending (IP-0306) extends `D03 T03 §3`'s mode and opacity; Fill Opacity (IP-0307) scales content but not effects, with the Photoshop special-eight modes (Color Burn, Linear Burn, Color Dodge, Linear Dodge, Vivid Light, Linear Light, Hard Mix, Difference) blending differently under fill than under opacity.
  - Channels (IP-0308): R, G, B checkboxes restrict the blend per channel.
  - Knockout None, Shallow, Deep (IP-0309), Blend Interior Effects as Group and Blend Clipped Layers as Group (IP-0310), Transparency Shapes Layer, Layer Mask Hides Effects, Vector Mask Hides Effects (IP-0311); knockout resolves against the enclosing group or the background.
  - Blend If (IP-0312): gray, R, G, B ranges for This Layer and Underlying Layer with split sliders (Alt drags) producing a linear ramp between the split points.
  - Affinity blend ranges (IP-0313, IP-0317): per-channel source and underlying curves through `ToneCurve`, and blend gamma per layer with a text default (IP-0314); the PSD round trip keeps the Photoshop-expressible subset and reports curves it cannot express.
  - Adjustment blending (IP-0304): the same ranges apply to adjustment layers for tonal targeting; `D03 T11 §1` exposes them in its Properties page.
  - Antialiasing and coverage map (IP-0315): per-layer antialiasing on or off and a coverage-map curve applied to vector-derived coverage (vector, shape, text kinds when registered).
  - GIMP spaces (IP-0316): composite mode (union, clip to backdrop, clip to layer, intersection), blend space and composite space (auto, RGB linear, RGB perceptual).
  - Live tone blend group (IP-0305): a group whose rendered content is color-matched to the composite beneath within its mask by mean and standard-deviation transfer in Lab (Reinhard and others 2001) with strength, color, contrast, low-pass radius, and content type, registered as a live kind with `D03 T08 §1`.
  - PSD blending ranges, `knko`, `iOpa`, and the interior and clipped-group flags map through the `D03 T04 §5` adapter now.
  - Tests: `BlendIfTests` (split sliders produce the expected ramp on a gray gradient), `FillOpacitySpecialEightTests` (each of the eight differs from opacity as Photoshop documents), `KnockoutTests`, `CompositeModeTests` (goldens from GIMP 3.2.6 per composite mode), GPU parity for every option.
  - Commit: `"gesso: blending options, Blend If, and blend ranges"`
- **Proof:** golden plus format fidelity: `CompositeModeTests` match GIMP 3.2.6 within 1/255, and a Photoshop-produced PSD with Blend If, fill opacity on Linear Burn, and deep knockout composites within 2/255 of its exported PNG; cheaper substitute that fails: fill opacity treated as opacity, which the special-eight test catches.

#### §6. Blend mode extensions

- **Deliverable:** Porter-Duff and SVG compositing ops, proper pass-through groups, erase-type modes, grain extract and merge, GIMP LCh and HSV modes, luminance darken and lighten only, GIMP legacy modes for XCF fidelity, Affinity's extra modes, a pigment mode, the 32-bit mode subset, and a grouped blend-mode menu with hover preview and cycling shortcuts.
- **Depends On:** §5, D03 T02 §4
- **Phase:** 16
- **Surface:** UI. Fidelity: docs/captures/gesso/layers/ for the mode menu, new captures to docs/captures/gesso/blend-modes/. Job: a user can use any blend mode a Photoshop, Affinity, or GIMP document uses and preview modes before choosing. Treatment: a grouped mode menu (Normal, Darken, Lighten, Contrast, Inversion, Component, LCh, Porter-Duff, Legacy) with hover preview on the canvas and Shift+plus and Shift+minus cycling. Cheaper substitute that fails: mapping unknown modes to Normal on import, which the per-mode goldens catch. Chrome: consume `D03 T02 §4`'s mode registry and goldens (extended), GPU parity, and the keymap; do not add a second mode table.
- **Runs:** `Requires: display-session -- hover preview and cycling need an interactive desktop`
- **Catalog:** IP-0318 to IP-0330 (13 features)
- **Hints:**
  - Porter-Duff ops (IP-0318) clear, source, destination, in, out, atop, over, xor (and their destination variants) plus GEGL's SVG soft-light, hard-light, and lighten ops (IP-0319) as modes with W3C and GEGL formulas.
  - Pass-through (IP-0320): groups in Pass Through composite their children directly into the backdrop; any other group mode isolates (`D03 T02 §3`'s `GroupNode`).
  - Erase-type (IP-0321): Behind, Clear, Erase, Color Erase, Merge, and Split (GIMP 2.10 and 3), usable as layer modes and as paint modes for `D03 T12`'s tools.
  - GIMP modes (IP-0322, IP-0323, IP-0324): Grain Extract and Grain Merge, LCh Hue, Chroma, Color, and Lightness, HSV Value, and Luminance or Luma Darken Only and Lighten Only, computed in the blend space §5 selects.
  - GIMP legacy modes (IP-0325): the pre-2.10 perceptual variants kept for XCF fidelity, flagged Legacy in the menu.
  - Affinity modes (IP-0326): Average, Negation, Reflect, Glow, Contrast Negate, with published formulas documented beside each; goldens from Krita 5.2 composite ops where Krita implements the same formula, property tests otherwise.
  - Pigment mode (IP-0327): Kubelka-Munk mixing over a small set of fitted primaries, own implementation (Mixbox is CC BY-NC and not usable), documented as Gesso's reading of Affinity's Pigment mode.
  - 32-bit subset (IP-0328): a `FloatSafe` flag per mode; in 32-bit documents unsafe modes are disabled with a tooltip, and `D03 T15 §4` consumes the list.
  - Menu (IP-0329, IP-0330): grouped families with hover preview (re-composites the affected tiles only, reverting on exit) and Shift+plus, Shift+minus, and Alt+Shift+letter shortcuts.
  - PSD mode keys and XCF mode ids map in one `BlendModeMap` that `D03 T04 §5` and `D03 T17 §2`, `§4` share; unknown keys import as Normal with a report line.
  - Tests: `BlendModeFidelityTests` extended with a golden per new mode (GIMP 3.2.6 for GIMP and Porter-Duff modes, Krita 5.2 for Affinity modes), `PassThroughTests`, GPU parity for every mode.
  - Commit: `"gesso: GIMP, Affinity, and Porter-Duff blend modes"`
- **Proof:** golden: `BlendModeFidelityTests` print a result per new mode within 1/255 of its reference (reference and version in `tests/fixtures/gesso/blend/VERSION.txt`), and swapping Grain Extract and Grain Merge fails both; cheaper substitute that fails: goldens produced by Gesso itself.

#### §7. Layer styles I: the effects framework, shadows, glows, stroke, and satin

- **Deliverable:** A layer-style model of ordered, multi-instance effects rendered by the render graph, the Layer Style dialog, fx buttons and a Quick FX panel, drop and inner shadow, outer and inner glow, satin, stroke, Affinity's Gaussian blur effect, global light, copy and paste style, effect visibility, scale effects, create layers from effects, and styles on text. -> SOURCE: legacy-gesso-5.8
- **Depends On:** §5
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/layer-style/ and docs/captures/gesso/quick-fx/. Job: a user can add editable shadows, glows, strokes, and satin to any layer and change them at any time. Treatment: Photoshop's Layer Style dialog (effect list with plus buttons for multiple instances, a live preview, on-canvas drag of shadow offset) and Affinity's Quick FX panel; effects show under the layer with eye toggles. Cheaper substitute that fails: effects baked into the layer's pixels, which the edit-after-save test catches. Chrome: consume the render graph, `D01 T03 §6` blur, §5's blending, the color panel, and `Isotone.UI` dialog styles; do not add a second compositor.
- **Runs:** `Requires: display-session -- the dialog, on-canvas offset drag, and Quick FX panel need an interactive desktop`
- **Catalog:** IP-0359 to IP-0376, IP-1212 to IP-1213 (20 features)
- **Hints:**
  - Promoted from backlog B-016 (carries `-> SOURCE: legacy-gesso-5.8`); delete the B-016 line from `todo/backlog.md` in the authoring commit.
  - `LayerStyle` in `Isotone.Gesso.Core/Layers/Styles/`: an ordered list of `LayerEffect` with multiple instances of drop shadow, inner shadow, stroke, color overlay, and gradient overlay (up to 10 each, reorderable, IP-0361), per-effect opacity and visibility (IP-0360, IP-0371); persisted as `<gesso:style>` inside the layer's `gesso:params` through `D03 T08 §1`, the fallback PNG including effects.
  - `StyleRenderer` in `Isotone.Gesso.Rendering/Effects/` builds effects from the layer's alpha per output tile with an effect margin; blur through `D01 T03 §6`; spread and choke, stroke width, and glow size through §14's `DistanceTransform` in `src/Isotone.Core/Imaging/Morphology/`; effect results cached per layer version.
  - Effects (IP-0362 to IP-0368): Drop Shadow (mode, color, opacity, angle, distance, spread, size, noise, Layer Knocks Out Drop Shadow, on-canvas offset drag while the dialog is open), Inner Shadow, Outer Glow and Inner Glow (color or gradient, technique softer or precise, source center or edge, range, jitter), Satin, Stroke (size, position outside, inside, or center, blend, opacity, overprint, fill color; gradient and pattern fills enabled when §8's gradient model and pattern interface land in this phase), and Affinity's Gaussian Blur effect with Preserve Alpha.
  - Global Light (IP-0369): document angle and altitude in the §1 block shared by every effect with Use Global Light.
  - Style commands (IP-0370, IP-0373, IP-0376): Copy, Paste, and Clear Layer Style, Paste Effects Only, Create Layers from effects (each effect to a clipped or underlying pixel layer, with a report of what cannot be reproduced), Rasterize Layer Style, Flatten All Layer Effects.
  - Visibility (IP-0371): per-effect eyes, Hide All Effects, and View, Hide Effects in View (display only).
  - Scaling (IP-0372): Scale Effects in `D03 T08 §7`'s Scale Styles hook and in free transform (`D03 T13 §5`), multiplying size-type parameters.
  - Text and GEGL styles (IP-0359, IP-0374, IP-0375): styles apply to text layers when `D03 T16 §1` registers them; GIMP's GEGL Styles filter (outline, shadow, bevel, inner glow, image overlay) maps onto a `LayerStyle` preset and is also listed in the Filter menu by `D03 T14 §2`.
  - Quick FX panel (IP-0360): Affinity's compact panel toggling and editing the common effects on the selected layers.
  - PSD `lfx2` effects descriptors for these effects read through the `D03 T04 §5` adapter's descriptor parser (psd-tools 1.10 as the oracle) and write through `D03 T17 §13`.
  - Budget: a 24-megapixel layer with drop shadow, outer glow, and stroke re-renders a dirty 256-pixel tile in under 5 ms after warm-up, zero allocations per tile.
  - Tests: `LayerEffectGoldenTests` against Photoshop-exported PNGs of fixture PSDs (tool and version recorded) within 3/255, `StyleSerializationTests`, `MultipleInstanceTests`.
  - The Filters menu form of the text-styling effects (IP-1212, IP-1213) runs the same effect renderer as the layer style; no second implementation.
  - Commit: `"gesso: layer styles with shadows, glows, satin, and stroke"`
- **Proof:** format fidelity plus unit: `LayerEffectGoldenTests` open `tests/fixtures/gesso/styles/*.psd` and composite within 3/255 of the Photoshop-exported PNG beside each, and a saved style reopens editable with equal parameters; cheaper substitute that fails: effects rasterized into the layer at apply time, which the reopen-and-edit assertion catches.

#### §8. Layer styles II: bevel, overlays, contours, and the Styles panel

- **Deliverable:** Bevel and emboss with contour and texture, color, gradient, and pattern overlays, the contour editor and presets, Affinity's 3D lighting effect, the Styles panel with additive apply and save from layer, ASL import and export, and the Style Picker tool, with Stilus's gradient model moved to `Isotone.Core`.
- **Depends On:** §7
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/layer-style/ (bevel and overlay pages), docs/captures/gesso/contour-editor/, and docs/captures/gesso/styles-panel/. Job: a user can build dimensional and textured styles, save them, and reuse them across documents and from Photoshop style files they own. Treatment: bevel, overlay, and contour pages in the Layer Style dialog, a Contour Editor, a Styles panel with groups, and a Style Picker tool. Cheaper substitute that fails: bundled Adobe style sets, which no license allows. Chrome: consume §7's framework, the moved gradient model, `D01 T03 §4`'s `ToneCurve`, and AvalonDock; do not add a second curve editor or gradient model.
- **Runs:** `Requires: display-session -- the dialog pages, contour editor, and Styles panel need an interactive desktop`
- **Catalog:** IP-0377 to IP-0387 (11 features)
- **Hints:**
  - First item: move the gradient model of `D02 T09 §7` (`GradientDefinition` with stops, midpoints, opacity stops, interpolation, and repeat) from `src/Stilus/Isotone.Stilus.Core/` into `src/Isotone.Core/Paint/Gradients/` as its second consumer, repoint Stilus, and repoint `D03 T03 §8`'s gradient tool to it; `D03 T12 §9` extends it with the editor and gradient fill layers.
  - `SurfaceLighting` in `src/Isotone.Core/Imaging/Lighting/`: a height field from the distance-transformed alpha shaped by a contour, normals, and Blinn-Phong shading with altitude and angle, so `D01 T06 §8`'s lighting filters reuse it.
  - Bevel and Emboss (IP-0377, IP-0378): styles outer, inner, emboss, pillow, stroke emboss; technique smooth, chisel hard, chisel soft; depth, direction, size, soften, angle, altitude, gloss contour, highlight and shadow mode, color, and opacity; Contour and Texture sub-effects.
  - Overlays (IP-0379, IP-0380, IP-0381): Color Overlay; Gradient Overlay (style linear, radial, angle, reflected, diamond; angle, scale, offset, align with layer, dither, method); Pattern Overlay reading patterns through an `IPatternLibrary` interface whose first implementation holds patterns embedded in opened PSD and ASL files and patterns made from the current layer, replaced by `D03 T12 §10`'s Patterns panel and PAT import behind the same interface.
  - Contours (IP-0382): a Contour Editor over `ToneCurve` with corner points, contour presets saved in `Gesso.Styles.Contours`, used by bevel, glow, shadow, and satin.
  - 3D effect (IP-0383, Affinity): multiple lights (color, direction, elevation), diffuse, specular, shininess, and ambient through `SurfaceLighting`.
  - Styles panel (IP-0384, IP-0387): groups, click to apply (replace), Shift-click to add, New Style from layer (with or without blending options), rename, delete, and import of style files; no bundled Adobe or Affinity styles.
  - Import and export (IP-0385): ASL (Photoshop styles) read and write through the PSD descriptor parser in `Isotone.Core/Formats/Psd/`, with fixtures produced by Photoshop (version recorded) and psd-tools 1.10 as the structure oracle; Affinity style files (`.afstyles`) are refused by name as backlog B-045.
  - Style Picker tool (IP-0386, Affinity): pick a style from one layer and apply chosen attributes (effects, blending, fill) to the selection.
  - Tests: `GradientModelMoveTests` (Stilus's gradient tests pass from `tests/Isotone.Core.Tests/`; `grep -rn "class GradientDefinition" src` finds one), `BevelGoldenTests` against Photoshop-exported PNGs within 3/255, `AslRoundTripTests`, `ContourCurveTests`.
  - Commit: `"gesso: bevel, overlays, contours, the Styles panel, and ASL styles"`
- **Proof:** format fidelity: `AslRoundTripTests` read a Photoshop-produced `styles.asl`, apply each style to a fixture layer within 3/255 of Photoshop's export, and write an ASL that psd-tools 1.10 parses with equal descriptors; cheaper substitute that fails: a private style format, which the Photoshop fixtures cannot load.

#### §9. Smart objects I: embedded smart objects

- **Deliverable:** Embedded smart objects that hold their source document, edit in a linked tab, replace, export, duplicate as instances or independent copies, convert to layers, reset transform, rasterize, and resample from the source on every transform, with Affinity's image layers and placed documents and a smart-object Properties page.
- **Depends On:** §1
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/smart-objects/ and docs/captures/gesso/smart-object-properties/. Job: a user can scale, rotate, and later edit placed content without ever losing quality. Treatment: Layer, Smart Objects submenu, a badge on the layer thumbnail, Edit Contents opening a tab whose save updates the parent, and a Properties page with size, position, source, and actions. Cheaper substitute that fails: a smart object that stores its rendered pixels and resamples those, which the repeated-transform test catches. Chrome: consume `D03 T08 §1` (embedded payloads under `gesso/embedded/`), the render graph, `D01 T03 §2`'s resampler, the document tabs of `D03 T03 §1`, and the suite history; do not add a second document loader.
- **Runs:** `Requires: display-session -- Edit Contents round trips through a second tab need an interactive desktop`
- **Catalog:** IP-0388 to IP-0401 (14 features)
- **Hints:**
  - `SmartObjectLayer` gains `Source` (an `EmbeddedSource` with the original bytes, format, pixel size, and resolution, stored as `gesso/embedded/<guid>.<ext>` through `D03 T08 §1`), a `Placement` transform (matrix plus the warp slot `D03 T13 §6` fills), and a cached render keyed by source hash and transform; registers `smart-object`.
  - Rendering (IP-0400): every transform resamples from the source (vector sources re-render at the needed resolution) so ten successive scale-down and scale-up steps equal one direct transform.
  - Convert and create (IP-0389, IP-0390): Convert to Smart Object from one or many layers (the source is an `.gesso` of those layers), New Smart Object via Copy (independent source) versus Duplicate (shared source instance).
  - Edit contents (IP-0391, IP-0388): opens the source in a new tab linked to the parent; saving the tab updates the parent layer as one undo step "Update Smart Object" in the parent; closing unsaved asks.
  - Replace and export (IP-0392, IP-0393): Replace Contents keeps the transform; Export Contents writes the source file as it was placed.
  - Convert to layers, reset, rasterize (IP-0394, IP-0395, IP-0396): Convert to Layers unpacks into a group with the transform applied, Reset Transform restores the placed size, Rasterize goes through §14 (with Revert Rasterize).
  - Image layers (IP-0398, Affinity): placed images keep source resolution and DPI, Convert to Image Layer and rasterize-on-paint prompts (`Gesso.Layers.AutoRasterizeOnPaint` from §14).
  - Placed documents (IP-0399): PSD sources render through the `Isotone.Core/Formats/Psd/` reader and the Gesso adapter now; SVG, PDF, and EPS sources are placeable when `D03 T17 §7`'s readers ship and are refused by name until then.
  - Properties page (IP-0397, IP-0401): width, height, X, Y, rotation, source name and format, embedded or linked, Edit Contents, Convert to Linked (enabled by §10), layer comp choice (enabled by §11); smart filters on the layer belong to `D03 T14 §1`.
  - PSD `SoLd` and `PlLd` placed-layer records with embedded `lnk2` data read through the `D03 T04 §5` adapter (import report names anything unsupported); write is `D03 T17 §13`.
  - Tests: `SmartObjectResampleTests` (ten transforms equal one within 1/255), `EditContentsRoundTripTests` (edit, save, and parent updates in one undo step), `EmbeddedSourcePersistenceTests`.
  - Commit: `"gesso: embedded smart objects with edit contents and lossless transforms"`
- **Proof:** unit plus format fidelity: `SmartObjectResampleTests` pass and a Photoshop-produced PSD with an embedded smart object opens as a live smart object whose composite matches the exported PNG within 2/255 and whose Export Contents bytes equal the embedded file; cheaper substitute that fails: storing the rendered pixels only, which the ten-transform test catches.

#### §10. Smart objects II: linked smart objects and link layers

- **Deliverable:** Linked smart objects and GIMP link layers with a shared link manager moved out of Stilus: place linked, default placement, status badges and updates, relink and resolve, reveal, embed and convert to linked, package, relative or absolute paths, and Affinity's Resource Manager.
- **Depends On:** §9
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/linked-smart-objects/ and docs/captures/gesso/resource-manager/. Job: a user can build documents from external files that update when those files change, and fix or package them when paths break. Treatment: link badges on thumbnails (up to date, modified, missing), prompts per the update policy, a Resource Manager dialog listing every linked and embedded resource with actions, and File, Package. Cheaper substitute that fails: absolute paths only, which the moved-folder test catches. Chrome: consume `Isotone.Core/Links/` (moved from Stilus), §9's smart-object model, the file dialogs, and the settings store; do not add a second file watcher service.
- **Runs:** `Requires: display-session -- relink dialogs, update prompts, and the Resource Manager need an interactive desktop`
- **Catalog:** IP-0402 to IP-0411 (10 features)
- **Hints:**
  - First item: move the path resolution, status tracking, folder watching, relink search, and package logic of `D02 T12 §7`'s `LinkManager` from `src/Stilus/Isotone.Stilus.Core/Links/` into `src/Isotone.Core/Links/` as its second consumer; Stilus keeps its Links panel over the shared core and its link tests pass unchanged; `grep -rn "class LinkManager" src` finds one definition.
  - `LinkedSource` on `SmartObjectLayer` (absolute path, relative path, `PathMode` relative or absolute (GIMP 3.2 option, IP-0410), last write time, size, SHA-256, status) persisted through `D03 T08 §1` with a cached fallback render, so a missing file still displays.
  - Placement (IP-0402, IP-0405): Place Linked and `Gesso.Place.Default` (embed or link) read by `D03 T17 §1`'s File, Place.
  - GIMP link layers (IP-0403, IP-0410): Open as Link Layers and Layer, Change Linked Image; a link layer is a linked smart object without transform history, registered as `link`.
  - Status and update (IP-0406): badges, Update Modified Content, Update All, and `Gesso.Links.UpdateMode` (automatic, manual, ask) consumed on activation and on the watcher's change events.
  - Relink (IP-0407): Relink to File, Resolve Broken Links searching a chosen folder and the document folder, auto-relink others from the same folder, Reveal in Explorer.
  - Embed and convert (IP-0408): Embed Linked and Convert to Linked (writes the embedded source beside the document, refused by name for read-only folders).
  - Package (IP-0404, IP-0409): File, Package copies the document and every linked file into a chosen folder and rewrites links as relative, with a report.
  - Resource Manager (IP-0411): every linked and embedded resource with status, size, and path; Locate, Update, Relink, Replace, Embed, Collect (package), and auto update on change.
  - Budget: a document with 200 linked smart objects opens and reports statuses without blocking the UI thread; one Information line per relink, embed, update, and package.
  - Tests: `LinkedSmartObjectTests` (modified detection through a temp file, relink, embed and convert round trip, relative path after moving the folder), `PackageTests`, and Stilus's moved `LinkManagerTests`.
  - Commit: `"gesso: linked smart objects, link layers, and the resource manager"`
- **Proof:** unit plus driven: `LinkedSmartObjectTests` pass including the moved-folder case, and a driven run edits a linked file outside Gesso, updates it, packages the document, and reopens the package from another folder with every link resolved (log lines quoted); cheaper substitute that fails: a second watcher and resolver copied from Stilus, which the single-definition grep catches.

#### §11. Layer comps and states

- **Deliverable:** Layer comps with visibility, position, and appearance capture, apply, cycle, update, duplicate, and delete with invalid-comp warnings, smart-object comp selection, and Affinity's States panel with scoped capture and queries by tag, type, name, and lock.
- **Depends On:** §9
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/layer-comps/ and docs/captures/gesso/states/. Job: a user can keep several versions of a layout in one document and switch between them in one click. Treatment: a Layer Comps panel (Photoshop) and a States panel (Affinity) with capture scope and query fields. Cheaper substitute that fails: comps stored as duplicate layer sets, which the size test catches. Chrome: consume the §1 layer model and `NamePattern`, the `D03 T08 §1` document block, and AvalonDock; do not add a second pattern matcher.
- **Runs:** `Requires: display-session -- the panels and apply gestures need an interactive desktop`
- **Catalog:** IP-0412 to IP-0420 (9 features)
- **Hints:**
  - `LayerComp` in `Isotone.Gesso.Core/Layers/Comps/`: name, comment, captured flags (visibility, position, appearance meaning styles and blending, and smart-object comp selection), and per-layer records keyed by layer id; stored as `<gesso:comps>` in the `D03 T08 §1` block.
  - Panel (IP-0413, IP-0419): New Layer Comp with the capture checkboxes and comment, apply (IP-0414), previous and next, and Last Document State.
  - Update, duplicate, delete (IP-0415): Update Comp, Update Visibility, Update Position, Update Appearance, Duplicate, Delete; comps whose layers were deleted or merged show a warning icon, with Clear Warning and a report of the missing ids.
  - Smart object comp selection (IP-0416): a smart object whose source has comps offers the choice in §9's Properties page; the choice is part of appearance.
  - States (IP-0412, IP-0417, IP-0418, IP-0420): Affinity's States panel captures visibility and effect states over a scope defined by a query (tag, layer type, name through `NamePattern` with regex, lock state); update and apply; queries saved in the state.
  - Apply is one undo step "Apply Layer Comp" or "Apply State"; one Information line naming the comp and the changed layer count.
  - PSD layer comps (image resource 1065 and per-layer comp records) map through `D03 T17 §2` and `§3`.
  - Tests: `LayerCompTests` (capture, change, apply restores visibility, position, and style; a deleted layer yields a warning), `StateQueryTests`, `LayerCompSerializationTests`.
  - Commit: `"gesso: layer comps and states"`
- **Proof:** unit plus driven: `LayerCompTests` pass, and a driven run captures three comps, cycles them, and deletes a layer to show the warning, with captures committed; cheaper substitute that fails: comps that duplicate layers, which the file-size assertion in `LayerCompSerializationTests` (under 1 KB per comp for a 50-layer fixture) catches.

#### §12. Align, distribute, and move-tool extensions

- **Deliverable:** Align and distribute layers to selection, canvas, or a key object with spacing, alignment handles and make-same-rotation, GIMP's align tool targets, and Move tool extensions: nudge, constrain, duplicate, auto-select, the layer picker, marquee layer selection, transform controls, hover highlighting, drag to another document, and GIMP's pick modes, on align math moved out of Stilus.
- **Depends On:** §2
- **Phase:** 17
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the Move options bar, new captures to docs/captures/gesso/align/. Job: a user can pick, move, and line up layers precisely with the mouse and keyboard. Treatment: Move options bar with auto-select, transform controls, and align and distribute buttons, the right-click layer picker, and the GIMP align tool's target and relative-to options. Cheaper substitute that fails: aligning by bounding box of the layer's full canvas instead of its visible pixels, which the bounds test catches. Chrome: consume `D03 T03 §4`'s Move tool (extended), `D03 T08 §4`'s snapping and layer bounds, the moved align core, and the keymap; do not add a second align implementation.
- **Runs:** `Requires: display-session -- move gestures, picking, and drags between documents need an interactive desktop`
- **Catalog:** IP-0421 to IP-0435 (15 features)
- **Hints:**
  - First item: move the rectangle align and distribute math of `D02 T08 §14` (edges, centers, key object, distribute by edges, centers, and spacing) from Stilus into `src/Isotone.Core/Layout/AlignDistribute.cs` as its second consumer; Stilus keeps its commands over the shared math and its tests pass.
  - Align and distribute (IP-0421, IP-0429, IP-0430, IP-0431): align edges and centers relative to the selection, canvas, or a key object (click a selected layer), Align Visible Layers, distribute by edges or centers, distribute spacing auto or fixed gap; layer bounds are the visible-pixel bounds from `D03 T08 §4`'s cache.
  - Affinity alignment (IP-0432): alignment handles on the selection and Make Same Rotation.
  - GIMP align tool (IP-0433): targets (first item, image, selection, active layer, channel, path, guide) and relative-to options, aligning paths and guides as well as layers when those kinds exist.
  - Move modifiers (IP-0422): arrows nudge 1 px, Shift+arrows 10 px, Shift constrains to 45 degrees, Alt-drag duplicates.
  - Picking (IP-0423, IP-0424, IP-0434, IP-0435): Auto-Select Layer or Group with Ctrl-click override; right-click lists every layer under the pointer; GIMP pick modes (pick a layer or guide, move the active layer, pick or move a path); the clicked layer or path becomes active.
  - Marquee selection (IP-0425): dragging on empty canvas with the Move tool selects intersecting layers (Affinity).
  - Transform controls and hover (IP-0426, IP-0427): Show Transform Controls, hover highlight of layer bounds with the matching panel row, auto-expand groups, and Alt-click cycles overlapping layers.
  - Drag to another document (IP-0428): dragging layers or groups onto another document's tab or view copies them (live kinds through `D03 T08 §8`'s private `Isotone.Gesso.Layers` format) at the drop point, Shift centers.
  - One undo step per move, align, or distribute with one Information line (command, layer count, offsets); nudges merge within the history merge window.
  - Tests: `AlignDistributeMoveTests` (Stilus's align tests run from `tests/Isotone.Core.Tests/`), `GessoAlignTests` (visible-pixel bounds), `LayerPickerTests`, `MarqueeLayerSelectTests`.
  - Commit: `"gesso: align, distribute, and move-tool extensions"`
- **Proof:** unit plus driven: `GessoAlignTests` pass (three layers with transparent margins align on their visible pixels), and a driven run auto-selects, marquee-selects, distributes spacing, and drags a group into a second document, with log lines quoted; cheaper substitute that fails: a copy of Stilus's align code in Gesso, which `grep -rn "class AlignDistribute" src` finding two definitions catches.

#### §13. Artboards

- **Deliverable:** Artboards as layer containers with the Artboard tool, presets, add-adjacent and duplicate, artboards from groups or layers, auto-nesting and auto-size canvas, background color and clipping, name labels, artboard-scoped guides, constraints for children, and an artboard document preset.
- **Depends On:** §12
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/artboards/ and docs/captures/gesso/constraints/. Job: a user can lay out several screens or formats in one document and keep their contents with them. Treatment: the Artboard tool with presets and orientation, edge plus buttons, labels renamable on the canvas, an Artboard page in the Properties panel, and a Constraints panel. Cheaper substitute that fails: artboards as plain groups with no clipping, which the clip test catches. Chrome: consume the §1 layer model, `D03 T08 §4`'s guides and snapping, `D03 T08 §2`'s presets, and §12's move tool; do not add a second page model.
- **Runs:** `Requires: display-session -- the Artboard tool, auto-nesting, and labels need an interactive desktop`
- **Catalog:** IP-0436 to IP-0447 (12 features)
- **Hints:**
  - `ArtboardLayer` in `Isotone.Gesso.Core/Layers/`: a group with bounds, background (white, black, transparent, custom), and Clip Content (IP-0445), registered as `artboard` with `D03 T08 §1`; the canvas grows to hold all artboards when Auto-Size Canvas is on (IP-0442).
  - Artboard tool (IP-0440, IP-0441): draw, select, and resize artboards with size presets, width, height, and orientation in the options bar; edge plus buttons add adjacent artboards; Alt-drag duplicates with contents.
  - Creation (IP-0443, IP-0436, IP-0444): New Artboard, Artboard from Group, Artboard from Layers, and the Artboard flag in `D03 T08 §2`'s `DocumentPreset` for new documents with an artboard.
  - Auto-nest (IP-0442): layers moved onto an artboard nest inside it and leave when moved off, unless the layer's ArtboardNesting lock from §1 is set.
  - Labels and view (IP-0446, IP-0437): name labels rename in place; View, Fit Artboard on Screen.
  - Guides (IP-0438): guides dragged inside an artboard get `ArtboardId` (`D03 T08 §4`) and move with it; artboard edges register as snap candidates.
  - Constraints (IP-0439, Affinity): per-child anchoring (left, right, top, bottom, center) and scaling (fixed, scale, stretch) applied when an artboard or group resizes, edited in a Constraints panel.
  - Properties page (IP-0447): size, position, background, and clip.
  - PSD artboards (`artb` section records) map through `D03 T17 §2` and `§3`; per-artboard export belongs to `D03 T18 §1`.
  - Each command is one undo step with one Information line.
  - Tests: `ArtboardTests` (clip content hides overflow, auto-nest on move, auto-size canvas bounds), `ConstraintTests` (a right-anchored child keeps its right margin when the artboard widens), `ArtboardSerializationTests`.
  - Commit: `"gesso: artboards with constraints"`
- **Proof:** unit plus format fidelity: `ArtboardTests` and `ConstraintTests` pass, and `tests/fixtures/gesso/artboards/two-boards.gesso` reopens with equal artboards and renders in GIMP 3.2.6 as `.ora` within 1/255 of Gesso's composite (the artboard group's fallback includes background and clip); cheaper substitute that fails: artboards stored only in memory, which the reopen comparison catches.

#### Sizing concerns

- §3 carries 21 catalog features plus the tiled-mask rewrite and the promoted B-015 bookkeeping; the live masks (hue range, luminosity range, band pass) share one `LiveMask` node and count as one item with three sub-steps, and they are the natural split if the section overruns 30 items.
- §7 carries 18 features plus the B-016 bookkeeping; if the effect goldens take more items than expected, the Quick FX panel and the GEGL Styles mapping are the natural split into §8's phase slot.

### todo/03-gesso/TODO-10-gesso-parity-selection.md -- `gesso-parity-selection`

- **Title:** "TODO-10 -- Gesso Parity: Selection, Refine, Channels, and Quick Mask"
- **Phase(s):** 17
- **Goal:** Gesso selects like Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6: a tiled soft selection with floating selections, selections saved to channels and files, and a selection editor; marquee, lasso, and magnetic lasso extensions; the magic wand, select by color, and Color Range with tonal, skin, gamut, and alpha ranges; one local segmentation engine (GrabCut, guided-filter, closed-form, and global matting) behind quick selection, paint select, foreground select, intelligent scissors, and Focus Area; one Select and Mask workspace for every refine path; modify, transform, and float commands; the complete Select menu; and a Channels panel with alpha and spot channels and quick mask options. The code lives in `src/Gesso/Isotone.Gesso.Core/Selection/` (the segmentation engine in `Selection/Segmentation/`, which stays in Gesso until Albumen's local masks B-028 need subject masks) and `src/Gesso/Isotone.Gesso.Desktop/Selection/`; it consumes the `D01 T03` resampler and histogram, `D01 T04 §2` gamut masks, and the `D03 T09 §3` layer masks, and it never re-implements them. Every selection change is one undoable command, every selection and channel persists through the `D03 T08 §1` contract, and nothing here talks to a network: AI selection (`D03 T19 §6`) only seeds this engine.
- **Current-state facts to verify (with claim candidates):**
  - The selection is one flat, untiled 8-bit array the size of the document, so select-all on a large image allocates the whole canvas. `<!-- claim: count "private byte\[\]\? _mask;" src/Gesso/src/Gesso.Core/Selections/Selection.cs = 1 -->` `<!-- claim: lines src/Gesso/src/Gesso.Core/Selections/Selection.cs = 360 -->`
  - `SelectionOperation` already has a GIMP-style Difference mode beside Replace, Add, Subtract, and Intersect. `<!-- claim: count "^    Difference$" src/Gesso/src/Gesso.Core/Selections/Selection.cs = 1 -->`
  - `SelectionTools` offers five static selectors (rectangle, ellipse, polygon, a tolerance magic wand with a contiguous flag, and an RGBA range), none of them a tool. `<!-- claim: count "public static void Select\w+\(" src/Gesso/src/Gesso.Core/Selections/SelectionTools.cs = 5 -->` `<!-- claim: count "bool contiguous = true" src/Gesso/src/Gesso.Core/Selections/SelectionTools.cs = 1 -->`
  - `QuickMask` exists with enter, exit, and cancel but no options and no surface. `<!-- claim: lines src/Gesso/src/Gesso.Core/Selections/QuickMask.cs = 121 -->` `<!-- claim: count "public void (Enter|Exit|Cancel)|public Selection\? (Exit|Cancel)" src/Gesso/src/Gesso.Core/Selections/QuickMask.cs = 3 -->`
  - There is no channel model and no Select menu command in the main window view model. `<!-- claim: count "class \w*Channel" src/Gesso/src/Gesso.Core/**/*.cs = 0 -->` `<!-- claim: count "Select" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 0 -->`
- **Inputs and XREFs:** `standards/gesso.md` (256 px tiles, zero allocations per dab, every edit undoable); `standards/shared.md` (settings, logging); Rother, Kolmogorov, and Blake, "GrabCut" (SIGGRAPH 2004); Boykov and Kolmogorov, "An Experimental Comparison of Min-Cut/Max-Flow Algorithms" (TPAMI 2004); He, Sun, and Tang, "Guided Image Filtering" (TPAMI 2013); Levin, Lischinski, and Weiss, "A Closed-Form Solution to Natural Image Matting" (TPAMI 2008); He et al., "A Global Sampling Method for Alpha Matting" (CVPR 2011); Germer et al., "Fast Multi-Level Foreground Estimation" (ICPR 2020); Mortensen and Barrett, "Intelligent Scissors for Image Composition" (SIGGRAPH 1995); Felzenszwalb and Huttenlocher, "Distance Transforms of Sampled Functions" (2012); Pertuz et al., "Analysis of focus measure operators" (Pattern Recognition 2013); GIMP 3.2.6 and its GEGL (`gegl:matting-levin`, `gegl:matting-global`, `gegl:paint-select`, fuzzy select, `sel2path`) as reference implementations and `gimp-console` goldens; -> XREF: D03 T03 §5 (the marquee, lasso, combine modes, and marching ants this file extends); -> XREF: D03 T08 §1 (the document model and the `gesso:` contract every selection and channel element registers with); -> XREF: D03 T08 §4 (snapping §1's pixel-aligned selection edges use); -> XREF: D03 T09 §1 (the Layers panel search §9's Find Layers focuses); -> XREF: D03 T09 §3 (layer masks that §7 refines and outputs to); -> XREF: D03 T09 §14 (the Layer, Matting operations and `ColorDecontaminator` §7 consumes, and the `Isotone.Core` distance transform §8 consumes); -> XREF: D03 T05 §1 (the filter pipeline §10 runs on alpha channels); -> XREF: D01 T03 §2 (the resampler §1 and §8 transform masks with); -> XREF: D01 T03 §4 (histogram percentiles §4's tonal ranges read); -> XREF: D01 T04 §2 (`GamutMask` behind §4's Out of Gamut); -> XREF: D03 T11 §8 (extends §10's split and merge engine into decompose, compose, Apply Image, and Calculations); -> XREF: D03 T11 §10 (the colormap dialog that calls §3's select-by-index); -> XREF: D03 T12 §8 (Stroke Selection, invoked from §1's selection editor); -> XREF: D03 T14 §1 (live filters on alpha channels, the non-destructive half of IP-0558); -> XREF: D03 T16 §5 (implements §9's selection-to-path bridge); -> XREF: D03 T19 §6 (AI selection seeds §6's engine); -> XREF: D03 T17 §3 and D03 T17 §2 (PSD alpha and spot channels read and written, 56-channel limit); -> XREF: D03 T17 §4 (the XCF selection channel mapped onto §1's persisted selection).
- **Adjacency:** list=applicable (Channels panel rows, saved selection and Select and Mask preset lists, Color Range presets); document=not-applicable (selections print nothing; spot channels reach print through D03 T18 §6); settings=applicable (every tool option and dialog default is a `Gesso.Selection.*` or `Gesso.Channels.*` key with a named consumer); reporting=applicable (Color Range and Focus Area previews, the selection editor thumbnail, selection bounds in the Info panel of D03 T08 §11); notifications=applicable (progress and Cancel for segmentation, matting, and Refine output over one second); permissions=applicable (a size-mismatched selection file, a channel limit of 56, and a locked channel refuse by name); audit=applicable (one Serilog Information line per selection and channel command); exchange=applicable (selection files as annotated grayscale PNG, Color Range and Select and Mask presets as JSON, channels through the `gesso:` contract and PSD); reverse=applicable (every selection, channel, and quick mask change is one undo step; Reselect restores the last selection)

#### §1. The selection model: soft selections, saved selections, and the selection editor

- **Deliverable:** A tiled soft selection mask with floating selections, Save and Load Selection against channels and files, a GIMP-style selection editor, and marching ants options, with the active selection persisted in `.gesso`.
- **Depends On:** D03 T08 §1
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/selection-model/ (Save Selection, Load Selection, selection editor). Job: a user can keep, reload, and inspect selections without losing them to the next click. Treatment: modal Save and Load Selection dialogs with document, channel, name, invert, and operation, and a dockable Selection Editor showing the mask with All, None, Invert, Save to Channel, To Path, and Stroke buttons. Cheaper substitute that fails: a single "last selection" slot. Chrome: consume the `D03 T05 §1` dialog frame styles, the suite history, and the overlay layer of `D03 T02 §2`; do not add a second mask type beside `SelectionMask`.
- **Runs:** `Requires: display-session -- the dialogs, the editor, and ants captures need an interactive desktop`
- **Catalog:** IP-0448 to IP-0456 (9 features)
- **Hints:**
  - Replace `Selection`'s flat `byte[]` with `SelectionMask` in `src/Gesso/Isotone.Gesso.Core/Selection/SelectionMask.cs`: 8-bit coverage in 256 px tiles where empty tiles are null and full tiles share one read-only instance, keeping Replace, Add, Subtract, Intersect, and Difference; budget: Select All on a 20,000 by 20,000 document allocates under 1 MB and combining two full-canvas masks runs under 50 ms.
  - `FloatingSelection` (GIMP): a pixel tile set with an offset attached to its target drawable, listed as a temporary "Floating Selection" row in the Layers panel; Anchor merges it through the `D03 T03 §2` tile snapshot and To New Layer promotes it; while a float exists other edits refuse with "Anchor or convert the floating selection first" (GIMP's behavior); §8 creates floats (IP-0449).
  - `DocumentChannels` in `Isotone.Gesso.Core/Selection/Channels/`: the ordered list of `AlphaChannel { Id, Name, SelectionMask Mask, Color, Opacity, ChannelKind (Alpha, Spot), ShowsSelected }` that §10's panel presents; this section owns the data so Save Selection works before the panel exists.
  - Save Selection dialog (Photoshop and GIMP): document, channel (New or an existing channel), name, operation Replace, Add, Subtract, Intersect; Load Selection dialog: source document of equal pixel size, channel (alpha channels, layer transparency, layer masks), Invert, operation; commands `SaveSelectionCommand` and `LoadSelectionCommand` (IP-0450, IP-0451).
  - Save Selection to File and Load Selection from File (Affinity): an 8-bit grayscale PNG with an `iTXt` chunk keyed `gesso:selection` holding `{ "v": 1, "width", "height", "x", "y" }`; loading a file of another size offers Scale (the `D01 T03 §2` bicubic resampler) or Place at Offset and refuses a non-grayscale PNG by name (IP-0452).
  - Persistence: the active selection writes `<gesso:selection v="1" src="data/selection.png"/>` in the `D03 T08 §1` document metadata (not a stack layer, so GIMP and Krita opening the file as `.ora` ignore it); alpha channels write `<gesso:channel>` elements the same way (§10 adds the panel attributes).
  - Selection Editor panel (GIMP): live mask thumbnail, click-to-select-by-color in the preview (§3's engine), buttons All, None, Invert, Save to Channel, To Path (enabled through §9's bridge once `D03 T16 §5` implements it), and Stroke Selection (enabled when `D03 T12 §8` ships, disabled with that section named until then) (IP-0455).
  - Marching ants options: `Gesso.Selection.ShowEdges` (View, Show, Selection Edges and Ctrl+H in Photoshop), `Gesso.Selection.AntsSpeed` (GIMP's marching ants speed in ms per step, default 200), `Gesso.Selection.PauseAntsWhileMoving`; ants come from a cached 50 percent marching-squares contour rebuilt only on mask change, consumer `SelectionOverlayRenderer` in `Isotone.Gesso.Rendering` (IP-0448, IP-0453, IP-0456).
  - Force pixel alignment (Affinity): `Gesso.Selection.ForcePixelAlignment` (default true) rounds marquee and transform edges to whole pixels, and `Gesso.Snap.SelectionEdges` snaps selection edges to guides and grids through the `D03 T08 §4` snapping service (IP-0454).
  - Undo names "Save Selection", "Load Selection", "Anchor Floating Selection", "Floating Selection to Layer"; one Information line per command, `Selection {Command} {Operation} {Source}`.
  - Tests in `tests/Isotone.Gesso.Core.Tests/Selection/`: `SelectionMaskTests` (every combine mode byte-equal to the old flat implementation on 50 seeded random shapes, full-tile sharing, the allocation budget), `SaveLoadSelectionTests`, `SelectionFileTests` (round trip and mismatch refusal), `FloatingSelectionTests` (edit refusal and anchor undo).
  - Commit: `"gesso: tiled soft selections, saved selections, floating selections, and the selection editor"`
- **Proof:** Unit test and format fidelity: `SelectionMaskTests` and `SaveLoadSelectionTests` pass, and `tests/fixtures/gesso/selection/soft-selection.gesso` (a feathered ellipse plus two alpha channels) saves, reopens, and compares byte-equal per tile; cheaper substitute that fails: keeping the full-size `byte[]`, which the 1 MB allocation assertion on a 20,000 px canvas catches.

#### §2. Marquee and lasso extensions

- **Deliverable:** Single row and column marquees, fixed ratio and fixed size styles with numeric fields, rounded rectangles, GIMP's auto shrink and guides while drawing, the magnetic lasso on a live-wire engine, and mixed freehand and polygonal lasso behavior with shared antialias and feather options.
- **Depends On:** §1
- **Phase:** 17
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the options bar, new captures to docs/captures/gesso/marquee-lasso/. Job: a user can draw a precise geometric or edge-following selection in one gesture. Treatment: marquee options (style Normal, Fixed Ratio, Fixed Size, swap, X, Y, W, H fields, corner radius, auto shrink, guides) and a magnetic lasso that snaps a live path to edges with anchor points. Cheaper substitute that fails: a magnetic lasso that is a plain polygon lasso. Chrome: consume the `D03 T03 §4` tool system and options bar, `SelectionMask`, and the overlay; do not add a second polygon rasterizer beside `SelectionTools.SelectPolygon`.
- **Runs:** `Requires: display-session -- drawing marquees and a magnetic lasso on the canvas needs an interactive desktop`
- **Catalog:** IP-0457 to IP-0467 (11 features)
- **Hints:**
  - Shared `SelectionToolOptions` in `Isotone.Gesso.Core/Selection/Tools/`: Antialias, Feather at creation (radius, applied through the existing Gaussian feather before combine), and the combine mode; every selection tool of this file reads it; keys `Gesso.Selection.Antialias` and `Gesso.Selection.FeatherRadius` (IP-0457).
  - Moving the outline (all three apps): drag inside with a selection tool moves only the mask, arrow keys nudge 1 px and Shift+arrow 10 px, Space while dragging repositions the marquee being drawn, and Ctrl+Alt drag (GIMP) moves the selection contents as a float (§1); one "Move Selection" step per gesture (IP-0458).
  - Single Row and Single Column marquee (Photoshop) plus Affinity's set width or height field; Marquee style Normal, Fixed Ratio, Fixed Size with a swap button and GIMP's numeric position and size fields editable while the marquee is live (IP-0459, IP-0460, IP-0461).
  - Rounded rectangle selection: GIMP's Rounded Corners option and Select, Rounded Rectangle (radius percent, concave), as a signed-distance mask so corners antialias exactly (IP-0464).
  - GIMP extras: highlight (dim outside while drawing), composition guides while drawing (thirds, golden sections, diagonal lines), and Auto Shrink with Shrink Merged (shrink the marquee to the bounding box of the non-transparent region under it) (IP-0462, IP-0463).
  - `LiveWire` in `Isotone.Gesso.Core/Selection/LiveWire/`: Dijkstra over a cost from gradient magnitude, Laplacian zero crossings, and gradient direction (Mortensen and Barrett 1995), computed lazily per 256 px tile; §5's intelligent scissors reuse it.
  - Magnetic Lasso (Photoshop, Affinity): Width (search radius), Contrast (edge threshold), Frequency (auto anchor rate), click to add manual points, Backspace removes the last point, pen pressure changes width when `Gesso.Selection.MagneticPenWidth` is on, `[` and `]` change width by 1 px; budget: path update under 16 ms on a 24-megapixel image (IP-0465, IP-0466).
  - Mixed lasso (all three): Alt switches freehand and polygonal mid-gesture, Backspace or Delete removes the last polygon point, Enter or double-click closes, and the view auto-pans when the pointer reaches the window edge (IP-0467).
  - Undo names "Rectangular Marquee", "Magnetic Lasso", and so on through the existing tool command; one Information line per committed selection (`Selection {Tool} {Operation} {Bounds}`).
  - Tests: `MarqueeStyleTests` (fixed ratio and size, swap, numeric fields), `RoundedRectangleMaskTests` (corner coverage against an analytic disc within 1/255), `LiveWireTests` (the path on a synthetic step edge stays within 1 px of it), `AutoShrinkTests`.
  - Commit: `"gesso: marquee styles, rounded rectangles, and the magnetic lasso"`
- **Proof:** Unit test plus a driven run: `LiveWireTests` and `RoundedRectangleMaskTests` pass, and a driven magnetic lasso around the committed `tests/fixtures/gesso/selection/disc-on-noise.png` produces a mask within 2 px of the disc (IoU above 0.97 quoted); cheaper substitute that fails: a polygon lasso that ignores edges, which the IoU assertion catches.

#### §3. Magic wand and select by color

- **Deliverable:** One flood-select engine behind the magic wand, GIMP's fuzzy select and select by color, and the Affinity flood select, with tolerance, sample size, contiguous or global matching, diagonal connectivity, transparent areas, criteria, source layers, and drag-to-set tolerance.
- **Depends On:** §1
- **Phase:** 17
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the options bar, new captures to docs/captures/gesso/magic-wand/. Job: a user can select a region or every pixel of a color in one click, and tune the tolerance by dragging. Treatment: a Magic Wand tool (W) and a Select by Color tool (Shift+O) sharing one options set; dragging after the click changes tolerance live with the mask preview. Cheaper substitute that fails: an RGB-distance flood fill on the active layer only. Chrome: consume §1's mask and `SelectionToolOptions`; do not keep `SelectionTools.SelectByColor` as a second implementation (it becomes a thin call into the engine).
- **Runs:** `Requires: display-session -- clicking and dragging the wand on the canvas needs an interactive desktop`
- **Catalog:** IP-0468 to IP-0478 (11 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-4.2-smart-selection` (promotes B-027); the integration commit deletes B-027 from `todo/backlog.md`, whose quick selection and Color Range parts land in §5 and §4 of this file.
  - `FloodSelector` in `Isotone.Gesso.Core/Selection/Flood/`: scanline flood (contiguous) or a per-pixel threshold pass (global), 4- or 8-connected (`Diagonal neighbors`, GIMP), antialiased edge from the distance to the threshold, Select Transparent Areas (GIMP), and a `Criterion` of Composite, Red, Green, Blue, Alpha, Hue, Saturation, Value, LCh Lightness, LCh Chroma, LCh Hue (GIMP's criteria); `SelectionTools.SelectByColor` becomes a wrapper (IP-0470, IP-0472, IP-0474, IP-0475, IP-0476).
  - Sample size (Photoshop): Point, 3 by 3, 5 by 5, 11 by 11, 31 by 31, 51 by 51, 101 by 101 average, shared with the eyedropper through one `SampleAverager` that `D03 T11 §9` extends (IP-0471).
  - Sources: Current Layer, All Layers (the flattened composite, Photoshop Sample All Layers and GIMP Sample merged), and Affinity's chosen source layers (Current Layer and Below, a picked list); the `SampleSource` option is one shared type that painting and retouch tools also read (IP-0469) (IP-0469, IP-0473).
  - Drag to set tolerance (Affinity and GIMP): after pressing, horizontal drag changes tolerance 0 to 255 with the mask previewed on the overlay and the value shown in a cursor label; release commits (IP-0477).
  - Draw Mask (GIMP): preview the would-be selection in the quick mask color while the pointer is down.
  - Select by Color (GIMP tool and Select, By Color command): global matching of the clicked color across the image or merged composite with threshold (IP-0478).
  - Select by colormap index (GIMP): `SelectByIndex(IIndexedPixelSource, IndexPredicate, operation)` over an interface that `D03 T11 §7`'s indexed documents implement; the colormap dialog of `D03 T11 §10` calls it with Replace, Add, Subtract, Intersect (IP-0468).
  - Budget: a global select on 24 megapixels under 150 ms, a contiguous fill of 10 megapixels under 200 ms, zero allocations inside the scanline loop (pooled span stack).
  - Undo "Magic Wand" and "Select by Color"; one Information line per commit with tool, tolerance, criterion, and pixel count.
  - Tests: `FloodSelectorTests` (4 against 8 connectivity on a diagonal line fixture, each criterion on a synthetic HSV wheel, transparent areas, sample size averaging), and goldens of GIMP 3.2.6 fuzzy select (threshold 15 and 60, antialias on) on `tests/fixtures/gesso/selection/wand/` compared within 1/255.
  - Commit: `"gesso: magic wand, fuzzy select, and select by color on one flood engine"`
- **Proof:** Format fidelity against GIMP 3.2.6: `FloodSelectorGoldenTests` match `gimp-console` fuzzy-select and by-color masks within 1/255 at two thresholds; cheaper substitute that fails: RGB Euclidean distance only, which the hue-criterion golden rejects.

#### §4. Color Range and tonal selection

- **Deliverable:** A Color Range dialog (sampled colors with fuzziness and localized clusters, hue families, highlights, midtones, shadows, skin tones with face weighting, out of gamut) with previews and presets, plus Affinity's Select Sampled Color, Select Tonal Range, and Select by Alpha, and selections from luminosity.
- **Depends On:** §3
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/color-range/. Job: a user can select every pixel of a color family or tonal band with a soft, previewed falloff, including from a layer mask. Treatment: a modal Color Range dialog with Select list, fuzziness and range sliders, add and subtract eyedroppers, invert, Localized Color Clusters, a thumbnail showing Selection or Image, and a document preview of None, Grayscale, Black Matte, White Matte, Quick Mask; Save and Load. Cheaper substitute that fails: a hard RGB range with no preview. Chrome: consume the §3 `SampleAverager`, the `D03 T05 §1` dialog frame, `D01 T04 §2` `GamutMask`; do not build a second preview compositor (reuse the one §6 builds when §6 exists, otherwise the overlay renderer of §1).
- **Runs:** `Requires: display-session -- the Color Range dialog and its previews need an interactive desktop`
- **Catalog:** IP-0479 to IP-0491 (13 features)
- **Hints:**
  - `ColorRangeSelector` in `Isotone.Gesso.Core/Selection/ColorRange/`: sampled colors matched by distance in Lab with a smooth fuzziness falloff (Photoshop's 0 to 200 scale), add and subtract samples, Invert; Localized Color Clusters multiplies by a spatial falloff from each sample point with the Range percent (IP-0481, IP-0488).
  - Preset families (Photoshop, Affinity): Reds, Yellows, Greens, Cyans, Blues, Magentas as hue windows with feathered edges shared with `D01 T03 §5`'s `HueSaturationLightness` range definitions (reuse the constants, do not re-derive them) (IP-0484).
  - Tonal ranges: Highlights, Midtones, Shadows with Photoshop's fuzziness and range sliders over luminance, band edges from `D01 T03 §4` `Histogram.Percentile`; Affinity's Select Tonal Range command (Highlights, Midtones, Shadows) maps to the same code (IP-0485).
  - Skin Tones: an elliptical skin-color model in YCbCr (Hsu, Abdel-Mottaleb, and Jain 2002) with fuzziness; Detect Faces weights the mask toward face boxes from OpenCV's frontal-face Haar cascade through OpenCvSharp4, which extends that package's recorded scope from `Isotone.Gesso.Core/Photo/` to `Selection/FaceBoxes.cs` with a `docs/dev/decisions.md` row; AI face detection is `D03 T19 §6` (IP-0486).
  - Out of Gamut: `D01 T04 §2` `GamutMask` against the document's CMYK proof profile (the active `D03 T18 §5` proof setup when present, otherwise `color.defaultCmykProfile`) (IP-0487).
  - Previews: thumbnail Selection or Image, document preview None, Grayscale, Black Matte, White Matte, Quick Mask, redrawn at screen resolution first and refined; budget: slider change to updated preview under 60 ms on 24 megapixels (IP-0482).
  - Save and Load settings as `.gessocolorrange` JSON (samples in Lab, fuzziness, range, mode); the Photoshop `.axt` format is not offered (not in the catalog) (IP-0483).
  - Affinity commands: Select Sampled Color (color model RGB, HSL, Lab, and tolerance), Select Alpha Range (Fully Transparent, Partially Transparent, Opaque), and Selection from Layer or composite luminosity (Ctrl+Shift+Alt+2 in Photoshop, luminosity as coverage) (IP-0489, IP-0490, IP-0491).
  - Mask entries: Layer Mask Properties, Color Range writes the result into the active `D03 T09 §3` mask instead of the selection, and Affinity's Tonal Range for masks does the same (IP-0479, IP-0480).
  - Undo "Color Range", "Select Tonal Range", "Select Alpha Range"; one Information line with mode and pixel count.
  - Tests: `ColorRangeSelectorTests` (fuzziness monotonic, localized clusters shrink the mask with range, each family isolates its hue on a wheel fixture), `SkinToneModelTests` on committed synthetic swatches, `GamutRangeTests` (sRGB 0,255,0 selected, 128,128,128 not).
  - Commit: `"gesso: Color Range, tonal ranges, skin tones, and alpha range selection"`
- **Proof:** Unit test plus driven run: the tests above pass and a driven Color Range with two add samples on `tests/fixtures/gesso/selection/color-range/fruit.png` produces a mask whose hash is quoted and whose Black Matte preview is captured; cheaper substitute that fails: a hard RGB box range, which the fuzziness monotonic test catches.

#### §6. The local segmentation engine and Focus Area

- **Deliverable:** `Isotone.Gesso.Core/Selection/Segmentation/` with GrabCut on a max-flow solver, the guided filter, closed-form (Levin) and global-sampling matting from a trimap, foreground estimation, and a shared selection preview renderer, plus the Focus Area dialog built on a classical focus measure.
- **Depends On:** §1
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/focus-area/. Job: a user can select the in-focus subject of a shallow depth-of-field photo, and every later selection tool can turn rough strokes or boxes into a clean matte offline. Treatment: a Focus Area dialog with View (marching ants, overlay, on black, on white, black and white, on layers, reveal layer), In-Focus Range with Auto, Image Noise Level with Auto, Soften Edge, add and subtract brushes, Output To, and a Select and Mask button. Cheaper substitute that fails: a Sobel-threshold mask with no noise compensation. Chrome: consume §1's mask, the `D03 T05 §1` dialog frame, and the overlay; the preview renderer built here is the one §4 and §7 reuse.
- **Runs:** `Requires: display-session -- the Focus Area dialog and its view modes need an interactive desktop`
- **Catalog:** IP-0492 to IP-0494 (3 features)
- **Hints:**
  - `MaxFlow` in `Selection/Segmentation/Graph/`: Boykov-Kolmogorov augmenting paths on a 4- or 8-connected grid graph with pooled node arrays; budget: a 2-megapixel region cut under 400 ms, zero managed allocations per iteration.
  - `GrabCut` (Rother et al. 2004): 5-component full-covariance GMMs for foreground and background, iterative estimation with hard constraints from a box, strokes, or a trimap, run on a downsampled ROI and upsampled with the guided filter; entry `Segment(SegmentationRequest)` taking `Box`, `ForegroundStrokes`, `BackgroundStrokes`, or `Points` (the shape `D03 T19 §6` sends after an AI locate).
  - `GuidedFilter` (He, Sun, Tang 2013, fast variant with subsampling) for edge-aware mask refinement, color-guided, radius and epsilon parameters.
  - `ClosedFormMatting` (Levin et al. 2008): matting Laplacian over 3 by 3 windows solved by preconditioned conjugate gradient with a coarse-to-fine pyramid whose `Levels` and `Iterations` are GIMP's foreground select parameters; golden against GIMP 3.2.6 `gegl:matting-levin` on `tests/fixtures/gesso/selection/matting/`.
  - `GlobalMatting` (He et al. 2011): global sampling of foreground and background pairs with randomized search and `Iterations`; golden against `gegl:matting-global` (IP-0492's Global matting from a trimap).
  - `ForegroundEstimator` (Germer et al. 2020, multi-level) returning the foreground color estimate for a matte band, which §7 passes to `D03 T09 §14`'s `ColorDecontaminator` (no second decontaminator).
  - `SelectionPreviewRenderer` in `Isotone.Gesso.Rendering/Selection/`: marching ants, overlay (color and opacity), on black, on white, black and white, on layers, onion skin, transparent, reveal layer, used by Focus Area, §4, and §7.
  - `FocusMeasure`: variance of the Laplacian over a window (Pertuz et al. 2013) on luminance, noise compensation from a MAD noise estimate (Image Noise Level Auto), In-Focus Range threshold with Auto from Otsu's method, Soften Edge through `GuidedFilter`; add and subtract brushes are hard constraints for a final GrabCut pass (IP-0493).
  - Focus Area Output To: Selection, Layer Mask, New Layer, New Layer with Layer Mask, New Document, New Document with Layer Mask; the Select and Mask button hands the result to §7, which wires it (IP-0494).
  - All engine entry points take `IProgress<double>` and `CancellationToken` at tile or iteration granularity; one Information line per Focus Area apply ("Focus Area {Output} {Pixels}").
  - Tests in `tests/Isotone.Gesso.Core.Tests/Selection/Segmentation/`: `MaxFlowTests` (against a brute-force cut on 8 by 8 graphs), `GrabCutTests` (IoU above 0.95 on a synthetic two-color scene), `MattingGoldenTests` (GIMP goldens within 3/255 mean), `FocusMeasureTests` (a blurred half and a sharp half split within 4 px).
  - Commit: `"gesso: the local segmentation and matting engine and Focus Area"`
- **Proof:** Format fidelity against GIMP 3.2.6 plus unit tests: `MattingGoldenTests` compare closed-form and global matting alphas with `gegl:matting-levin` and `gegl:matting-global` output within a mean delta of 3/255 and a max of 24/255, and `GrabCutTests` quote IoU; cheaper substitute that fails: a thresholded distance transform standing in for matting, which the golden rejects at hair edges.

#### §5. Quick selection, selection brush, foreground select, and intelligent scissors

- **Deliverable:** Photoshop's Quick Selection, Affinity's Selection Brush with and without Snap to Edges, GIMP's Paint Select, Foreground Select, and Intelligent Scissors, all driving the §6 engine or §2's live wire.
- **Depends On:** §6
- **Phase:** 17
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for options bars, new captures to docs/captures/gesso/quick-selection/. Job: a user can paint roughly over a subject and get a clean selection that grows stroke by stroke. Treatment: a brush-driven tool family whose strokes become GrabCut seeds in an expanding ROI, with add and subtract modes, auto-enhance, hard or soft edges, and GIMP's trimap-based foreground select with preview. Cheaper substitute that fails: region growing by color tolerance from the stroke. Chrome: consume the §6 engine and preview renderer, §2's `LiveWire`, §3's `SampleSource`, and the `D03 T03 §6` brush cursor; do not add a segmentation path outside `Selection/Segmentation/`.
- **Runs:** `Requires: display-session -- painting selections on the canvas needs an interactive desktop`
- **Catalog:** IP-0495 to IP-0502 (8 features)
- **Hints:**
  - `QuickSelectionTool` (W group, Photoshop; Affinity Selection Brush with Snap to Edges on): each stroke adds foreground (or background with Alt) seeds, and §6 `GrabCut` re-solves only an ROI dilated around the stroke, merging into the running mask; budget: stroke release to updated mask under 250 ms on a 24-megapixel image (IP-0496).
  - Options: size, hardness, spacing, and pen pressure from the `D03 T03 §6` brush settings, mode New, Add, Subtract, Sample All Layers (the §3 `SampleSource`), Auto-Enhance (a guided-filter pass plus smoothing), and Affinity's Soft Edges toggle (keep the matte) against hard edges (threshold at 50 percent) (IP-0496, IP-0497).
  - Selection brush without snapping (Affinity Snap to Edges off, and Photoshop's plain overlay painting): paints coverage straight into the mask with the brush's hardness, shown as an overlay (IP-0498).
  - `PaintSelectTool` (GIMP 3.2.6 Paint Select, IP-0495 and IP-0502 are the same tool): progressive graph-cut selection from brush strokes with Mode Add or Subtract, stroke width, and a local region size, reusing the same ROI solver as Quick Selection with GIMP's parameters.
  - `ForegroundSelectTool` (GIMP): draw a rough outline (trimap unknown band), then paint Foreground, Background, or Unknown with a stroke width, Preview Mode (Color or Grayscale), and engine Matting Levin or Matting Global with Levels and Iterations (§6's matting engines); Enter commits the matte as the selection (IP-0499, IP-0500).
  - `IntelligentScissorsTool` (GIMP): click anchors, segments follow §2's `LiveWire`, Interactive Boundary shows the live segment while moving, Auto-edge snap nudges anchors to the strongest edge within 5 px, Enter converts to a selection (IP-0501).
  - Each tool commits one undo step ("Quick Selection", "Paint Select", "Foreground Select", "Intelligent Scissors") and one Information line with tool, stroke count, and elapsed milliseconds.
  - Tests: `QuickSelectionSessionTests` (two strokes on a synthetic scene reach IoU above 0.95; a subtract stroke removes a region), `ForegroundSelectTests` (trimap to matte through each engine), `IntelligentScissorsTests` (closed path on a disc fixture within 1 px).
  - Commit: `"gesso: quick selection, paint select, foreground select, and intelligent scissors"`
- **Proof:** Driven run with log line plus unit tests: a driven two-stroke quick selection on `tests/fixtures/gesso/selection/quick/portrait-synthetic.png` logs its elapsed time under the budget and its mask IoU against the committed expected mask is quoted above 0.95; cheaper substitute that fails: color-tolerance region growing from the stroke, which the IoU assertion on a subject with mixed colors rejects.

#### §7. Select and Mask and refine selection

- **Deliverable:** One Select and Mask workspace (Photoshop layout, Affinity Refine Selection, and a compact legacy Refine Edge layout from the same engine) with view modes, refine tools, edge detection, global refinements, decontaminate colors, and every output target, reachable from every selection tool, layer masks, and Focus Area.
- **Depends On:** §6, D03 T09 §3
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/select-and-mask/ (workspace, Affinity layout, legacy layout, each view mode). Job: a user can turn a rough selection or mask of hair or fur into a clean matte with decontaminated colors and send it where they need it. Treatment: a full-window modal workspace with its own toolbar (Quick Selection, Refine Edge brush, Brush, Object lasso, Hand, Zoom), a Properties column (View, Show Edge, Show Original, Real-time and High Quality Preview, Edge Detection, Global Refinements, Output), and presets. Cheaper substitute that fails: a Feather and Contract dialog labeled Refine. Chrome: consume §6's engine and `SelectionPreviewRenderer`, §5's quick selection, the `D03 T09 §3` mask model, and the `D03 T09 §14` matting operations; do not build a second preview compositor or matting routine.
- **Runs:** `Requires: display-session -- the workspace, refine brushes, and view-mode captures need an interactive desktop`
- **Catalog:** IP-0504 to IP-0520, IP-0522 (18 features)
- **Hints:**
  - `RefineSession` in `Isotone.Gesso.Core/Selection/Refine/`: holds the source mask, the refine band, brush edits, and parameters, and produces the matte through §6 (`ClosedFormMatting` inside the band, `GuidedFilter` outside); preview renders at screen resolution in real time and High Quality Preview renders at full resolution on idle (IP-0510).
  - Entry points: the Select and Mask button on every selection tool's options bar (IP-0505), Select, Select and Mask (Alt+Ctrl+R), Layer Mask Properties Refine and the mask context menu (IP-0504), double-click a layer mask when `Gesso.Masks.DoubleClickOpens` is `SelectAndMask` (IP-0522, default `Properties`), refining an existing mask later (IP-0518), and Focus Area's button (§6).
  - Workspace: tools Quick Selection (§5), Refine Edge brush, Brush (add or subtract, hardness), Object Selection as a lasso here (the AI object tool is `D03 T19 §6`), Hand, Zoom; buttons Clear Selection and Invert; view modes from `SelectionPreviewRenderer` with view opacity and overlay color; Show Edge (the band only) and Show Original (IP-0506 to IP-0509, IP-0511).
  - Edge Detection: Radius and Smart Radius (band width adapts to local edge contrast), Refine Mode Color Aware (this engine) and Object Aware routed to `D03 T19 §6` when AI is configured, otherwise disabled with that section named (IP-0513).
  - Global Refinements (Photoshop): Smooth, Feather, Contrast, Shift Edge; Affinity Refine Selection: Matte Edges, Border Width, Smooth, Feather, Ramp, plus Affinity's refine brushes Matte, Foreground, Background, Feather with width (IP-0512) (IP-0514, IP-0515).
  - Decontaminate Colors with Amount (IP-0516): reuse `ColorDecontaminator` from `D03 T09 §14`, feeding it §6's `ForegroundEstimator` output for the refine band, blended by amount; output forces a new layer or document as Photoshop does.
  - Matting cleanup rows IP-0503 and IP-0521: Remove Black Matte, Remove White Matte, and Defringe inside this workspace call the `D03 T09 §14` Layer, Matting operations (IP-0259); this section adds no second implementation (see the integration note on duplicates).
  - Output To: Selection, Layer Mask, New Layer, New Layer with Layer Mask, New Document, New Document with Layer Mask (IP-0517), one undo step "Select and Mask" whatever the target.
  - Remember Settings and presets (IP-0519): `Gesso.SelectAndMask.RememberSettings` plus `.imagerefine` JSON presets in `%LOCALAPPDATA%\Rizonesoft\Gesso\Presets\Refine\`; Legacy Refine Edge (IP-0520): `Gesso.SelectAndMask.Layout` = `Workspace`, `AffinityDialog`, or `LegacyRefineEdge` chooses the layout over the same `RefineSession`.
  - Budget: Real-time preview refresh under 100 ms on a 24-megapixel image at fit zoom; full-resolution output with progress and Cancel.
  - One Information line per output ("Select and Mask {Output} {Radius} {Decontaminate}").
  - Tests: `RefineSessionTests` (shift edge and contrast change coverage monotonically, output targets each produce the right document object), `DecontaminateTests` (a green-screen hair fixture's edge pixels lose green cast by a quoted mean), golden of the matte on `tests/fixtures/gesso/selection/refine/hair.png` against a committed expected alpha within 4/255 mean.
  - Commit: `"gesso: Select and Mask with refine brushes, decontaminate colors, and every output"`
- **Proof:** Driven run with capture plus unit tests: a driven refine of the hair fixture from a rough lasso produces a matte within 4/255 mean of the committed expected alpha, each view mode is captured, and `RefineSessionTests` pass; cheaper substitute that fails: Feather plus Contract labeled Refine, which the hair golden rejects.

#### §8. Modify and transform selection

- **Deliverable:** Border, Smooth, Expand, Contract, Grow, Similar, Remove Holes, Sharpen, Distort, Transform Selection, floating selections by cut and copy, and selections from alpha and layer transparency with every combine modifier.
- **Depends On:** §1
- **Phase:** 17
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the menu, new captures to docs/captures/gesso/modify-selection/ (Border and Distort dialogs, Transform Selection handles). Job: a user can reshape an existing selection numerically or by hand without touching pixels. Treatment: Select, Modify dialogs with live preview on the ants, Transform Selection with free-transform handles on the outline only. Cheaper substitute that fails: Expand by a square dilation. Chrome: consume §1's mask, the `D03 T03 §7` transform handles, and the `D01 T03 §2` resampler; do not write a second transform-handle overlay.
- **Runs:** `Requires: display-session -- the dialogs and on-canvas selection transform need an interactive desktop`
- **Catalog:** IP-0523 to IP-0534 (12 features)
- **Hints:**
  - `SelectionMorphology` in `Isotone.Gesso.Core/Selection/Modify/`: the exact Euclidean distance transform `src/Isotone.Core/Imaging/Morphology/DistanceTransform.cs` that `D03 T09 §14` adds (Felzenszwalb and Huttenlocher 2012; consumed, not re-implemented) behind Expand and Contract (circular, GIMP's Grow and Shrink), Border (width, alignment Inside, Center, Outside, style Hard, Smooth, Feathered, GIMP's lock to selection edge), and Affinity's Outline with rounding (IP-0524, IP-0526).
  - Smooth (Photoshop sample radius) as a median of coverage within a disc; Remove Holes (GIMP) fills enclosed unselected regions by flooding from the border; Sharpen (GIMP) thresholds at 50 percent to remove antialiasing (IP-0525, IP-0530, IP-0531).
  - Apply effect at canvas bounds (GIMP option on Border, Shrink, and Feather): treat outside the canvas as selected instead of unselected; key `Gesso.Selection.ModifyTreatsOutsideAsSelected` (IP-0527).
  - Grow and Similar (Photoshop): §3 `FloodSelector` seeded by every selected pixel with the magic wand tolerance, contiguous for Grow and global for Similar (IP-0528).
  - Distort (GIMP Script-Fu): Threshold, Spread, Granularity, Smoothing with Smooth horizontally and vertically, seeded so the same seed reproduces (IP-0532).
  - Transform Selection (Photoshop, Affinity): scale, rotate, skew, distort, perspective, and warp handles on the outline through the `D03 T03 §7` transform overlay, resampling the mask with the `D01 T03 §2` bicubic resampler, one "Transform Selection" step (IP-0529).
  - Floating selections (GIMP): Edit, Cut and Float and Copy and Float create §1's `FloatingSelection`; Anchor lives in §1 (IP-0533).
  - Alpha to Selection (GIMP) with Replace, Add, Subtract, Intersect; Ctrl+click a layer, mask, or channel thumbnail loads its coverage (Photoshop), Ctrl+Shift adds, Ctrl+Alt subtracts, Ctrl+Shift+Alt intersects; text and shape layers contribute their rendered glyph or shape alpha (IP-0523, IP-0534).
  - Budget: Expand by 50 px on 24 megapixels under 150 ms; every command logs one Information line with the parameters.
  - Tests: `SelectionMorphologyTests` (expand then contract restores a disc within 1 px; border width measured; remove holes on a ring fixture), `DistortSelectionTests` (seeded determinism), goldens of GIMP 3.2.6 Grow, Shrink, and Border on `tests/fixtures/gesso/selection/modify/` within 1/255.
  - Commit: `"gesso: modify, transform, and float selections"`
- **Proof:** Format fidelity against GIMP 3.2.6 plus unit tests: Grow, Shrink, and Border masks match `gimp-console` output within 1/255 and `SelectionMorphologyTests` pass; cheaper substitute that fails: square dilation, which the circular-grow golden rejects at corners.

#### §9. Select menu extensions

- **Deliverable:** The complete Select menu in one organized layout: Reselect, All Layers, Deselect Layers, Find Layers, selection from layer bounds and masks, and the Selection to Path and Path to Selection commands with GIMP's tracing options, wired through a bridge that `D03 T16 §5` implements.
- **Depends On:** §8
- **Phase:** 17
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the menu, new capture of the Selection to Path advanced dialog to docs/captures/gesso/select-menu/. Job: a user finds every selection command where Photoshop, Affinity, or GIMP users expect it. Treatment: a Select menu table grouping All, Deselect, Reselect, Inverse; layer selection; Color Range, Focus Area, and Select and Mask; Modify; Grow and Similar; Transform Selection; Quick Mask; Load, Save, file; To Path and From Path. Cheaper substitute that fails: a flat alphabetical menu. Chrome: consume the command registry and keymap of `D03 T03 §4`; the menu grows through `D03 T20 §3` later without renaming these commands.
- **Runs:** `Requires: display-session -- the menu and dialog captures need an interactive desktop`
- **Catalog:** IP-0535 to IP-0540 (6 features)
- **Hints:**
  - Reselect (Shift+Ctrl+D): `SelectionHistory` keeps the last non-empty mask per document (tile-shared, not a copy) and restores it as one step (IP-0535).
  - Select All Layers (Alt+Ctrl+A), Deselect Layers, and Find Layers (Alt+Shift+Ctrl+F, focusing the `D03 T09 §1` Layers panel search) (IP-0536).
  - Select menu organization (GIMP) as data: `SelectMenuLayout.json` in `Isotone.Gesso.Desktop/Menus/` listing groups and command ids, so `D03 T20 §3` customizes it without code (IP-0537).
  - `ISelectionPathBridge` in `Isotone.Gesso.Core/Selection/Paths/` with `SelectionFromPath(pathId, operation, antialias, feather)` and `PathFromSelection(SelectionToPathOptions)`; `SelectionToPathOptions` carries GIMP's `sel2path` parameters (align threshold, corner always threshold, corner surround, corner threshold, error threshold, filter alternative surround, filter epsilon, filter iteration count, filter percent, keep knees, line reversion threshold, line threshold, reparametrize improvement, reparametrize threshold, subdivide search, subdivide surround, subdivide threshold, tangent surround) with GIMP's defaults.
  - Commands Selection to Path, Selection to Path (Advanced), and Path to Selection (from a path, shape layer, or curve, with the §1 combine modes) exist here, disabled with the tooltip "Planned: D03 T16 §5" until that section registers the bridge implementation; `D03 T16 §5` carries the enabling item and the tracing engine (IP-0538, IP-0539, IP-0540).
  - Every command writes one Information line and one undo step; Reselect after Deselect restores a byte-equal mask.
  - Tests: `ReselectTests`, `SelectMenuLayoutTests` (every command id resolves, no duplicates), `SelectionToPathOptionsTests` (defaults equal GIMP 3.2.6's).
  - Commit: `"gesso: the Select menu, Reselect, layer selection, and the selection-to-path bridge"`
- **Proof:** Unit test plus static check: `ReselectTests` and `SelectMenuLayoutTests` pass and `grep` finds no Select menu command whose handler only logs; cheaper substitute that fails: Reselect storing a full-size copy per selection, which a tile-sharing assertion in `ReselectTests` catches.

#### §10. The Channels panel, spot channels, and quick mask options

- **Deliverable:** A Channels panel with per-mode channel lists, thumbnails, visibility and targeting, alpha and spot channels with options, duplicate, reorder, lock, color tags, channel-to-selection modifiers, Affinity's composite alpha and pixel selection channels and load-into commands, split and merge channels, painting and filtering channels, and Quick Mask with options.
- **Depends On:** §1
- **Phase:** 17
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/channels/ (panel, Channel Options, New Spot Channel, Quick Mask Options, a spot channel in color). Job: a user can store, edit, and combine masks as channels, keep spot inks, and paint a selection in quick mask. Treatment: a dockable Channels panel listing the composite and per-mode color channels (RGB, CMYK, Lab, gray, and the `D03 T11 §7` modes), then alpha and spot channels, with eye, target, thumbnail, name, lock, and color tag, plus Channel Options and Quick Mask Options dialogs. Cheaper substitute that fails: a list of saved selections with no targeting or painting. Chrome: consume `DocumentChannels` from §1, the `D03 T05 §1` filter pipeline, the `D03 T03 §6` brush, and the theme; do not add a second mask store.
- **Runs:** `Requires: display-session -- the panel, dialogs, and quick mask painting need an interactive desktop`
- **Catalog:** IP-0546 to IP-0564 (19 features)
- **Hints:**
  - `ChannelsPanel.xaml` and `ChannelsPanelViewModel` in `Isotone.Gesso.Desktop/Channels/`: composite plus component rows per mode (the `D03 T11 §7` mode list), Ctrl+2 composite and Ctrl+3 onward single channels (IP-0547), Show Channels in Color (`Gesso.Channels.ShowInColor`, IP-0548 and IP-0564), eye and target toggles, reset.
  - Alpha channels (all three): New, Delete, Rename, Duplicate to same, other, or new document with Invert, Raise, Lower, drag reorder, multi-select, color tags (GIMP); limit 56 channels matching Photoshop for PSD round trip, refused by name beyond it (IP-0550, IP-0552, IP-0553, IP-0554).
  - Channel Options and New Channel dialogs: name, Color Indicates Masked or Selected Areas, color, opacity; stored on `AlphaChannel` and written as attributes of §1's `<gesso:channel>` element (IP-0551).
  - Channel lock attributes (Affinity and GIMP): lock pixels, position, visibility, editable, each refusing the matching edit by name (IP-0549).
  - Channel to selection: click the load button or Ctrl+click the thumbnail, Ctrl+Shift add, Ctrl+Alt subtract, Ctrl+Shift+Alt intersect (Photoshop), GIMP's Channel to Selection with Replace, Add, Subtract, Intersect (IP-0555).
  - Affinity channels: composite alpha and a live Pixel Selection channel listed in the panel; context menu Load to (layer red, green, blue, alpha, mask, adjustment, filter, grayscale layer, mask layer), Invert, Clear, Fill (IP-0556, IP-0557).
  - Painting and filtering alpha channels: a targeted channel is a paint target for every `D03 T03 §6` brush and a filter target for the `D03 T05 §1` pipeline (destructive); live filters on channels (IP-0558's non-destructive half) are `D03 T14 §1` (IP-0558).
  - Spot channels (Photoshop): New Spot Channel (ink color from the picker or a user color book, solidity 0 to 100), Spot Channel Options, Merge Spot Channel into the color channels through `D01 T04 §1`; spot channels render in the composite at their solidity and export through PSD in `D03 T17 §2` (IP-0559).
  - `ChannelSplitter` and `ChannelMerger` in `Isotone.Gesso.Core/Channels/`: Split Channels into grayscale documents named `<name>_R` and so on, Merge Channels back by mode and channel mapping; `D03 T11 §8` extends this engine for decompose and compose (IP-0560).
  - Quick Mask (Q): `QuickMask` moves onto `SelectionMask` and is painted by every brush; Quick Mask Options (Masked or Selected Areas, color, opacity, and Affinity's view style overlay, grayscale, or transparent), the toolbox button reflecting the state (IP-0561 to IP-0563).
  - Undo names "New Channel", "Channel Options", "Merge Spot Channel", "Split Channels", "Quick Mask"; one Information line per command.
  - Tests in `tests/Isotone.Gesso.Core.Tests/Channels/`: `ChannelModelTests` (limit, lock refusals, reorder), `ChannelSelectionModifierTests`, `SplitMergeChannelsTests` (split then merge is byte-identical on RGB and CMYK fixtures), `SpotChannelTests` (merge at solidity 100 equals a multiply of the ink).
  - Commit: `"gesso: the Channels panel, alpha and spot channels, split and merge, and quick mask options"`
- **Proof:** Unit test plus format fidelity: `SplitMergeChannelsTests` round-trip byte-identically and `tests/fixtures/gesso/channels/three-alpha-one-spot.gesso` reopens with every channel's name, color, opacity, solidity, and pixels equal; cheaper substitute that fails: storing channels as hidden layers, which the reopen assertion on channel kind and solidity catches.

#### Sizing concerns

- §7 carries 20 catalog features and about 14 hint items; the view modes, global refinements, and Affinity refine controls each expand to three or four checklist items, so it lands near 27; the natural split, if it overruns, is Output and presets (IP-0517 to IP-0520, IP-0522) as a follow-on section.
- §10 carries 19 features across the panel, spot channels, split and merge, and quick mask; spot channels (IP-0559) are the natural split if the checklist passes 28 items.

### todo/03-gesso/TODO-11-gesso-parity-adjustments.md -- `gesso-parity-adjustments`

- **Title:** "TODO-11 -- Gesso Parity: Adjustment Layers, Adjustments, Image Modes, and Color"
- **Phase(s):** 18
- **Goal:** Gesso corrects tone and color like Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6: non-destructive adjustment layers with an Adjustments panel, a Properties page per kind, presets and Photoshop preset files, a targeted adjustment tool, and an adjustment brush; every tonal and color adjustment the three ship, from Levels and Curves extensions to color lookup with LUT files and OpenColorIO, gradient maps, match and replace color, and GIMP's Colors menu operations; image modes (bitmap, grayscale, duotone, indexed, RGB, CMYK, Lab, multichannel) and 8, 16, and 32-bit precision; channel operations (Apply Image, Calculations, decompose, compose); and the color panels, pickers, samplers, swatches, palettes, and color books. Gesso code lives in `src/Gesso/Isotone.Gesso.Core/Adjustments/`, `Color/`, and `Channels/` and `src/Gesso/Isotone.Gesso.Desktop/Adjustments/` and `Color/`; every algorithm Gesso adds joins the one `EffectRegistry` in `src/Isotone.Core/Imaging/Adjust/`, palette files move to `src/Isotone.Core/Color/Palettes/`, and everything consumes `D01 T03 §3` to `§5` and `§11`, `D01 T04 §1` to `§3`, and `D01 T05 §5` rather than growing a second curve, histogram, quantizer, or color conversion. No Adobe or Affinity preset, LUT, or color book is bundled; users import the files they own.
- **Current-state facts to verify (with claim candidates):**
  - `AdjustmentLayer` is a 57-line model holding only an `AdjustmentType` enum of 16 kinds, with no parameters, mask, or rendering. `<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/AdjustmentLayer.cs = 57 -->` `<!-- claim: count "^    [A-Z][A-Za-z]*,?$" src/Gesso/src/Gesso.Core/Layers/AdjustmentLayer.cs = 16 -->`
  - The main window binds no Levels, Curves, or Hue/Saturation command; adjustments arrive with `D03 T05 §2`. `<!-- claim: count "Levels|Curves|HueSaturation" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 0 -->`
  - The document `ColorSpace` enum lists RGB variants, CMYK, Lab, and grayscale but no indexed, bitmap, duotone, or multichannel mode, and `BitDepth` has exactly 8, 16, and 32. `<!-- claim: count "Indexed|Duotone|Multichannel|Bitmap" src/Gesso/src/Gesso.Core/Documents/ColorSpace.cs = 0 -->` `<!-- claim: count "Bpc(8|16|32) = " src/Gesso/src/Gesso.Core/Documents/BitDepth.cs = 3 -->`
  - Gesso carries its own 342-line color converter with Lab and CMYK structs that the suite engine (`D01 T04`) supersedes, so §7 and §9 must convert through `Isotone.Core` instead. `<!-- claim: lines src/Gesso/src/Gesso.Core/Colors/ColorConverter.cs = 342 -->` `<!-- claim: count "public readonly record struct (Lab|Cmyk)Color" src/Gesso/src/Gesso.Core/Colors/ColorModels.cs = 2 -->`
  - There is no palette or swatch code anywhere in Gesso, and no `Isotone.Core` yet to hold the moved palette readers. `<!-- claim: count "Palette|Swatch" src/Gesso/src/**/*.cs = 0 -->` `<!-- claim: absent src/Isotone.Core -->`
- **Inputs and XREFs:** `standards/gesso.md` (premultiplied RGBA working format, 8/16/32 float, SIMD with scalar reference, color never changes profile silently); `standards/shared.md`; Adobe Photoshop File Formats Specification (Curves `.acv`, Levels `.alv`, Hue/Saturation `.ahu`, Color Table `.act`, Swatches `.aco`, Duotone `.ado`, Descriptor structure); Adobe Cube LUT Specification 1.0 (`.cube`), Autodesk `.3dl`, Cinespace `.csp`, IRIDAS `.look`; OpenColorIO 2.4 (BSD-3-Clause) and its `ociobakelut` and `ocioconvert` tools as oracles; GIMP 3.2.6 with its GEGL operations as the golden oracle through `gimp-console`, and its palette, decompose, and color-tool behavior; Krita 5.2 (KPL oracle); Reinhard et al., "Color Transfer between Images" (2001); Jobson, Rahman, and Woodell, "A Multiscale Retinex" (1997) as GIMP's retinex reference; Kolås, Farup, and Rizzi, "STRESS" (2011) for c2g; -> XREF: D01 T03 §3 (quantizer, dithering, posterize behind indexed and bitmap modes and §5's dither); -> XREF: D01 T03 §4 (histogram, levels, tone curve, auto adjust, equalize, exposure, temperature, white balance extended in §2); -> XREF: D01 T03 §5 (hue saturation, color balance, vibrance, selective color, replace colors, desaturate, black and white, channel mixer, invert, threshold used in §3 to §5); -> XREF: D01 T03 §11 (photo filter, colorize, sepia); -> XREF: D01 T04 §1 and D01 T04 §2 (conversions, gamut checks, device links); -> XREF: D01 T04 §3 (mode conversions and duotone, whose dialog §7 moves to `Isotone.UI`); -> XREF: D01 T05 §5 (brand kit palettes and the ASE reader and writer §10 reuses); -> XREF: D01 T06 §9 (extends §8's `ExpressionCompiler` with noise primitives instead of creating it); -> XREF: D01 T06 §13 (alien map, the engine IP-0656 waits on, and the Equations filter that consumes §8's compiler); -> XREF: D01 T07 §1, D01 T07 §2, D01 T07 §3 (the develop kernels the Light, clarity, dehaze, and grain adjustment kinds switch to or wait on; see §2 and §4); -> XREF: D02 T09 §4 (palette file readers moved in §10); -> XREF: D02 T09 §5 (the harmony engine moved in §9); -> XREF: D03 T09 §8 (the `Isotone.Core` gradient model, moved out of Stilus there, that §4's Gradient Map and §10's palette gradients use); -> XREF: D03 T02 §4 (the render graph adjustment nodes join); -> XREF: D03 T03 §8 (the color panel, picker, and eyedropper §9 extends); -> XREF: D03 T05 §1 and D03 T05 §2 (the filter pipeline and the Levels, Curves, Hue/Saturation dialogs and histogram control §1 to §3 grow into Properties pages); -> XREF: D03 T08 §1 (precision and document model §7 extends); -> XREF: D03 T08 §11 (the Info panel that displays §9's sampler readouts); -> XREF: D03 T09 §3 (built-in masks of adjustment layers); -> XREF: D03 T10 §3 (select by colormap index called from §10); -> XREF: D03 T10 §4 (localized color clusters reused by Replace Color); -> XREF: D03 T10 §10 (the split and merge engine §8 extends); -> XREF: D03 T12 §5 (paint tools wiring §9's temporary eyedropper); -> XREF: D03 T12 §9 (the full gradient editor around §4's gradient model; lists §10's palette gradients); -> XREF: D03 T12 §10 (patterns for §7's custom bitmap pattern); -> XREF: D03 T14 §1 (destructive adjustments on smart objects become smart filters; live Shadows/Highlights and Matte Look); -> XREF: D03 T15 §4 (HDR display for §2's HDR curve range and §9's intensity slider); -> XREF: D03 T17 §3 and D03 T17 §13 (PSD adjustment layers read and written); -> XREF: D03 T18 §4 (OCIO configuration management for §4's OCIO adjustment); -> XREF: D03 T20 §7 (the presets manager listing adjustment presets, LUTs, and palettes).
- **Adjacency:** list=applicable (Adjustments panel, preset lists, LUT library, Swatches panel and Palettes dialog with search and tags); document=not-applicable (no printed output; duotone and spot inks reach print through D03 T18 §6); settings=applicable (every default is a `Gesso.Adjustments.*`, `Gesso.Color.*`, or `Gesso.Modes.*` key with a named consumer); reporting=applicable (histograms in Levels, Curves, and Threshold, Match Color statistics, histogram export, total ink readout, Info panel samplers); notifications=applicable (progress and Cancel for mode conversions, LUT inference, and Apply Image over one second); permissions=applicable (unsupported preset or palette files, a device link that does not match the document, and non-global adjustments in LUT export refuse by name); audit=applicable (one Serilog Information line per adjustment, conversion, and color command); exchange=applicable (ACV, ALV, AHU, ACT, ACO, ASE, ACB, GPL, KPL and the GIMP palette formats, CUBE, 3DL, CSP, LOOK, ICC device links); reverse=applicable (every adjustment, mode change, and swatch edit is one undo step; adjustment layers are non-destructive by construction)

#### §1. Adjustment layers and the Adjustments and Properties panels

- **Deliverable:** Non-destructive adjustment layers rendered by the render graph with built-in masks, clipping, child placement, and linked instances, created from the Adjustments panel, Layer menu, Layers panel button, and adjustment brush, edited in Properties pages with presets and Photoshop preset files, plus destructive Image, Adjustments commands.
- **Depends On:** D03 T09 §3, D01 T03 §5
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/adjustments-panel/ (Adjustments panel, Properties page, Quick Adjustments, targeted adjustment drag). Job: a user can stack any adjustment above or inside a layer, re-edit it forever, and reuse settings as presets. Treatment: an Adjustments panel of kind icons and preset groups with hover preview, a Properties host (clip, view previous, reset, visibility, delete, opacity, blend mode, scrubby sliders, double-click reset), and a Quick Adjustments panel of sliders that create layers. Cheaper substitute that fails: an adjustment that bakes pixels on OK. Chrome: consume the `D03 T05 §1` dialog frame's parameter views as Properties pages, the `D03 T05 §2` histogram control, the `D03 T09 §3` mask model, and the suite history; do not build a second parameter-view system.
- **Runs:** `Requires: display-session -- the panels, targeted adjustment, and adjustment brush need an interactive desktop`
- **Catalog:** IP-0565 to IP-0584 (20 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-5.1-adjustment-layers` (promotes B-014); the integration commit deletes B-014 from `todo/backlog.md` and rewrites the `D03 T05 §2` context sentence that points at it.
  - Replace the enum-only model with `AdjustmentLayer { string Kind; EffectDescription Parameters; LayerMask Mask; bool ClippedToBelow; Guid? LinkId }` in `src/Gesso/Isotone.Gesso.Core/Adjustments/`, and an `AdjustmentKindRegistry` mapping each kind id (`levels`, `curves`, `hue-saturation`, and so on) to a `D01 T03` `EffectRegistry` id and a Properties page type, so §2 to §5 register kinds without touching the model.
  - `AdjustmentNode` in `src/Gesso/Isotone.Gesso.Rendering/RenderGraph/`: applies the fused lookup or matrix from the `D01 T03` effect to the composite below (or only the clipped base, or only its parent for Affinity child adjustments of a layer, group, vector object, or frame content, IP-0570), through the built-in mask at the layer's opacity and blend mode; only tiles under a changed region re-render; budget: five stacked adjustment layers on 24 megapixels refresh the viewport under 33 ms at fit zoom.
  - Insertion (IP-0569, IP-0571, IP-0572, IP-0583): auto-mask from the active selection, placement preference `Gesso.Adjustments.NewPlacement` (`AboveSelected` or `ClippedToSelected`, Affinity), Alt+Ctrl+G clips; Layer, New Adjustment Layer, the Layers panel button, and fill and adjustment content options create one (IP-0566, IP-0582).
  - Persistence through `D03 T08 §1`: `<gesso:adjustment kind="curves" v="1">` with a `<gesso:params>` child holding the `EffectDescription` JSON; the stack PNG for the layer is the adjusted composite of everything below, clipped to the mask at the layer's opacity, so GIMP and Krita show the same picture; Gesso discards that PNG on load and restores the live layer.
  - Adjustments panel (IP-0565, IP-0584): kind icons in Photoshop order, preset groups per kind, hover preview that renders the viewport with the preset applied and restores on leave; Quick Adjustments panel (Affinity, IP-0578): sliders for exposure, contrast, saturation, vibrance, and temperature, each creating or editing its adjustment layer, auto buttons, reset.
  - Properties host (IP-0573): re-edit, clip to layer, view previous state (backslash), reset, visibility, merge down, delete, opacity, blend mode; scrubby labels and double-click-to-reset on every slider through one `ScrubbySlider` control in `Isotone.Gesso.Desktop/Controls/`; undo names "New Adjustment Layer", "Edit Adjustment", "Merge Adjustment Down", "Adjustment Brush", and one Information line per command (`Adjustment {Command} {Kind} {Layer}`).
  - Linked instances (Affinity symbols, IP-0574): layers sharing a `LinkId` share parameters, written as `gesso:link-id`; editing one updates all in one command; Unlink copies.
  - Merge Adjustment Down (IP-0575) bakes through the `D03 T03 §2` tile snapshot; destructive Image, Adjustments commands (IP-0576) run the same kinds through the `D03 T05 §1` pipeline with Alt reopening last-used settings; on a smart object they become a smart filter once `D03 T14 §1` ships and until then ask to rasterize.
  - Targeted adjustment tool (IP-0577): on-image drag for Curves (adds a point at the sampled value, vertical drag moves it), Hue/Saturation (drag changes saturation of the sampled range, Ctrl+drag changes hue), and Black and White (drag changes the sampled color's weight).
  - Adjustment brush (Affinity, IP-0579): choose a kind, paint with the `D03 T03 §6` brush (width, opacity, flow, hardness, blend mode, erase) into the mask of a new adjustment layer that starts hidden-all.
  - Presets (IP-0567, IP-0568, IP-0581): `.gessoadj` files holding a `D01 T03 §4` `AdjustmentPreset` in `%LOCALAPPDATA%\Rizonesoft\Gesso\Presets\Adjustments\`, save, load, rename, delete, reorder; read and write Photoshop `.acv`, `.alv`, and `.ahu` per Adobe's specification; built-in presets for Levels, Curves, Hue/Saturation, Black and White, and Channel Mixer authored by Gesso as data (no Adobe preset file is shipped).
  - Colors menu organization (GIMP, IP-0580): `AdjustmentsMenuLayout.json` with groups Auto, Components, Desaturate, Info, Map, and Tone Mapping beside the Photoshop list, so every GIMP Colors command has a home.
  - Tests: `AdjustmentLayerRenderTests` (a levels layer over a fixture equals the destructive result within 1/255; mask, clip, and child placement), `AdjustmentPersistenceTests` (live round trip and the ORA fallback PNG equal to the flattened render), `PhotoshopPresetFileTests` (ACV, ALV, AHU fixtures written by Photoshop 27.10 from Gesso-authored settings, read, written, reread byte-equal).
  - Commit: `"gesso: adjustment layers, the Adjustments and Properties panels, presets, and the adjustment brush"`
- **Proof:** Format fidelity plus unit tests: `tests/fixtures/gesso/adjustments/stack.gesso` (levels, curves, hue-saturation, one clipped, one child, one linked) reopens live with parameters equal, its `.ora` fallback opened by GIMP 3.2.6 `gimp-console` flattens within 1/255 of Gesso's render, and the ACV, ALV, AHU fixtures round-trip byte-equal; cheaper substitute that fails: baking on OK, which the reopen-as-live assertion catches.

#### §2. Tonal adjustment extensions

- **Deliverable:** Levels, Curves, Brightness/Contrast, Exposure, and Shadows/Highlights grown to the three competitors' full option sets, auto corrections with options, GIMP's stretch contrast, retinex, and contrast curve, the Light adjustment, and clarity and dehaze adjustment kinds.
- **Depends On:** §1, D01 T03 §4
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/tonal/ (Levels, Curves with display options, Auto Color Correction Options, Shadows/Highlights, Light). Job: a user can correct tone with every control a Photoshop, Affinity, or GIMP tutorial names. Treatment: Properties pages for each kind with channel and color-model pickers, eyedroppers, clipping display, curve tools and display options, and an Options dialog for auto corrections. Cheaper substitute that fails: an RGB-only Levels with no eyedroppers. Chrome: consume §1's Properties host, the `D03 T05 §2` histogram control and curve editor, and the `D03 T10 §3` `SampleAverager`; do not re-implement any `D01 T03 §4` kernel.
- **Runs:** `Requires: display-session -- the adjustment pages and eyedroppers need an interactive desktop`
- **Catalog:** IP-0585 to IP-0603, IP-0605 to IP-0607 (22 features)
- **Hints:**
  - Brightness/Contrast (IP-0585): legacy and linear modes, Auto, and Edit as Levels (convert the parameters to an equivalent levels layer); built on `D01 T03 §4` `Light` and `Levels`.
  - Light (Photoshop, IP-0586): exposure, contrast, highlights, shadows, whites, blacks composed from `D01 T03 §4` `Exposure`, `Light`, and `Levels` endpoints behind a version selector that switches to legacy Brightness/Contrast; `D01 T07 §1` is phase 23, so its item swaps this composition for the develop tone kernel behind the same parameters (reciprocal XREF).
  - Levels (IP-0587 to IP-0590, IP-0592): crossed levels for negatives and Edit as Curves (Affinity), any color model (RGB, gray, CMYK, Lab, and alpha) through a `ColorModelAdapter` that converts tiles with `D01 T04 §1`, working space linear, non-linear, or perceptual and linear or logarithmic histogram (GIMP), black, gray, and white point eyedroppers and pick-from-image with sample average and sample merged, and Alt-drag clipping display.
  - Curves (IP-0588 to IP-0590, IP-0593 to IP-0595): pencil and freehand modes with smoothing and per-node smooth or corner types (extend `D01 T03 §4` `ToneCurve` with `NodeType`, not a second curve), display options (light or pigment percent, 4 by 4 or 10 by 10 grid, channel overlays, baseline, histogram, intersection line), and an input range min and max enabled on 32-bit float documents (HDR display is `D03 T15 §4`).
  - Auto corrections (IP-0591, IP-0599, IP-0605): Auto Tone, Auto Contrast, Auto Color, auto levels commands and filters, and Photoshop's Auto Color Correction Options (Enhance Monochromatic Contrast, Enhance Per Channel Contrast, Find Dark and Light Colors, Enhance Brightness and Contrast, Snap Neutral Midtones, target shadow, midtone, and highlight colors, clip percentages), added to `D01 T03 §4` `AutoAdjust` as algorithm parameters.
  - Auto White Balance command and filter (IP-0600, IP-0606): `D01 T03 §4` `WhiteBalance` gray-world mode.
  - Exposure (IP-0596): exposure, offset, gamma, black level (GIMP), and eyedroppers on `D01 T03 §4` `Exposure` and `Gamma`, extended with offset and black level.
  - Shadows/Highlights (IP-0597, IP-0607): Photoshop amount, tone, radius, color, midtone, black and white clip, and GIMP's white point adjustment and compress, as `ShadowsHighlights` in `src/Isotone.Core/Imaging/Adjust/` (local luminance through the `D01 T03 §6` Gaussian, then tone curves), also an adjustment kind as in Affinity Photo 2; Affinity's default and 1.6 algorithms are two parameter presets; golden against GIMP 3.2.6 `gegl:shadows-highlights`; the live filter form is `D03 T14 §1`.
  - Equalize with selection options (IP-0598): Equalize Selected Area Only or Entire Image Based on Selection, on `D01 T03 §4` `Equalize`.
  - GIMP operations in the registry (`src/Isotone.Core/Imaging/Adjust/`, each tagged with its GEGL op id for `D01 T06 §1`'s map): `StretchContrast` and `StretchContrastHsv` (IP-0601), `Retinex` (uniform, low, high levels, scale, divisions, dynamic; multiscale retinex as GIMP's plug-in, IP-0602), `ContrastCurve` for grayscale (IP-0603).
  - Clarity and dehaze adjustment kinds (IP-0604): kinds, pages, and `gesso:` elements registered now with their kernels coming from `D01 T07 §2` (phase 23), listed disabled with the tooltip "Planned: D01 T07 §2" until that section enables them.
  - Budget: every page's slider change updates the viewport under 60 ms on 24 megapixels; one Information line per adjustment apply.
  - Tests: goldens against GIMP 3.2.6 in `tests/fixtures/imaging/tonal-ext/` for stretch contrast, retinex, shadows-highlights, levels in linear space, and curves with corner nodes (tolerances in each `reference.txt`), plus `AutoColorOptionsTests` and `ColorModelAdapterTests` (Lab levels on an RGB document round-trips within 1/255 at identity).
  - Commit: `"gesso: tonal adjustment extensions, auto corrections, and GIMP tone operations"`
- **Proof:** Format fidelity against GIMP 3.2.6 plus unit tests: the listed goldens pass within their stated tolerances and `ColorModelAdapterTests` pass; cheaper substitute that fails: Levels only in RGB, which the Lab and CMYK channel tests catch.

#### §3. Color adjustments I: hue, balance, vibrance, black and white, photo filter, selective color

- **Deliverable:** Hue/Saturation range extensions, hue curves, Color Balance, Vibrance, Color and Vibrance, Black and White with auto, Photo Filter and Lens Filter, Selective Color, and GIMP's hue-chroma, saturation, and color temperature, each an adjustment kind and a destructive command.
- **Depends On:** §1
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/color-adjust-1/. Job: a user can shift, saturate, balance, and tint colors by range with the controls they know. Treatment: Properties pages with range bars and eyedroppers for Hue/Saturation, a hue-curve editor, and the preset lists each competitor ships as named data. Cheaper substitute that fails: a master-only Hue/Saturation. Chrome: consume §1's host, the `D03 T05 §2` page, and `D01 T03 §5` kernels; do not add a second HSL helper beside `HslMath`.
- **Runs:** `Requires: display-session -- the adjustment pages need an interactive desktop`
- **Catalog:** IP-0608 to IP-0619 (12 features)
- **Hints:**
  - Hue/Saturation ranges (IP-0608): four-slider range bars with falloff, add and subtract range eyedroppers, GIMP's Overlap, an HSV computation mode, and Affinity's hue wheel with draggable range nodes, as parameters added to `D01 T03 §5` `HueSaturationLightness`.
  - `HueCurves` in `src/Isotone.Core/Imaging/Adjust/` (IP-0609): hue versus saturation, hue versus hue, and hue versus luma on periodic monotone splines, with a page reusing the curve editor.
  - Color Balance (IP-0610) and Vibrance with saturation (IP-0611, IP-0619) pages over `D01 T03 §5`.
  - Color and Vibrance (Photoshop, IP-0612): temperature and tint from `D01 T03 §4` `TemperatureTint` fused with `D01 T03 §5` `Vibrance` and saturation in one kind.
  - Black and White (IP-0613): six sliders, tint hue and saturation, and Auto (weights from the image's hue distribution, documented), over `D01 T03 §5` `BlackAndWhite`.
  - Photo Filter and Lens Filter (IP-0614): `D01 T03 §11` `PhotoFilter` with color, density, preserve luminosity, and a filter preset list of warming, cooling, and color filters authored by Gesso as named colors.
  - Selective Color (IP-0615): `D01 T03 §5` `SelectiveColor` with relative or absolute, passing the document's CMYK profile through `D01 T04 §1` now that it exists.
  - GIMP kinds (IP-0616 to IP-0618) in the registry with GEGL op ids: `HueChroma` (LCh hue, chroma, lightness), `Saturation` with interpolation color space (native, CIE LCh, linear), and color temperature from original to intended Kelvin as a second mode of `TemperatureTint`.
  - Every kind writes its `gesso:adjustment` element through §1; one Information line per apply.
  - Tests: goldens against GIMP 3.2.6 (`gegl:hue-chroma`, `gegl:saturation`, `gegl:color-temperature`, hue-saturation with overlap) in `tests/fixtures/imaging/color-adjust-1/` within 2/255, `HueCurvesTests` (identity curve is exact; wrap at 360 degrees is continuous).
  - Commit: `"gesso: hue, balance, vibrance, black and white, photo filter, selective color, and GIMP hue operations"`
- **Proof:** Format fidelity against GIMP 3.2.6: the listed goldens pass within 2/255 and `HueCurvesTests` pass; cheaper substitute that fails: hue ranges without falloff, which the overlap golden rejects.

#### §4. Color adjustments II: channel mixer, LUTs, gradient map, match and replace color, OCIO

- **Deliverable:** Channel Mixer in any color model, Color Lookup with LUT files, ICC abstract and device-link profiles, LUT inference, a LUT library, LUT export from the adjustment stack, Gradient Map on the suite gradient model, Match Color and color transfer, Replace Color, Sample Colorize, White Balance with pickers, the OCIO adjustment, Split Toning, Recolor, Normals, and a grain adjustment kind.
- **Depends On:** §1, D01 T04 §1
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/color-adjust-2/ (Color Lookup, LUT library, Gradient Map, Match Color, OCIO). Job: a user can grade with LUTs and color transfers, map tones to a gradient, and exchange grades with other tools. Treatment: Properties pages plus a LUT library window with categories and a Match Color dialog with source statistics. Cheaper substitute that fails: a `.cube` reader with trilinear lookup and no export. Chrome: consume §1's host, the `Isotone.Core` gradient model moved by `D03 T09 §8`, the `D01 T04 §1` engine, and `D03 T10 §4`'s localized clusters; do not add a second LUT sampler or gradient sampler.
- **Runs:** `Requires: display-session -- the pages, library window, and Match Color dialog need an interactive desktop`
- **Catalog:** IP-0620 to IP-0634, IP-0636 to IP-0638 (18 features)
- **Hints:**
  - Gradients come from the model `D03 T09 §8` moves out of Stilus into `src/Isotone.Core/Paint/Gradients/` (`GradientDefinition`); this section adds no gradient code of its own, and `D03 T12 §9` extends that model with GIMP segments and the editor.
  - Channel Mixer (IP-0620, IP-0621): output channel, source sliders, constant, total readout, monochrome, preserve luminosity (GIMP), color model RGB, CMYK, Lab, or HSL (Affinity), and alpha as an output for keying, over `D01 T03 §5` `ChannelMixer` plus the §2 `ColorModelAdapter`.
  - LUT files in `src/Isotone.Core/Imaging/Luts/` (IP-0622, IP-0637): readers and writers for `.cube` (1D and 3D, domain min and max), `.3dl`, `.csp` (with prelut), and `.look`, a `ColorLookup` effect with tetrahedral interpolation, dither, and table order (RGB or BGR); ICC abstract and device-link profiles through `D01 T04 §1`, and ICC device-link export through lcms2 `cmsTransform2DeviceLink`.
  - Infer LUT (Affinity, IP-0623): fit a 33-cube lattice from a source and graded image pair by per-cell averaging and Laplacian fill of empty cells; test: a fixture graded by a known LUT reproduces it within 2/255.
  - LUT library (Affinity, IP-0624): `%LOCALAPPDATA%\Rizonesoft\Gesso\LUTs\` with category folders, import, export, sort, rename, move; Affinity `.afluts` category files are read from operator-exported samples, and if their container proves undocumented the row moves to backlog B-045 through `add-todo` in the same commit.
  - Export Color Lookup Tables (IP-0625): sample the identity lattice (17, 33, or 65) through the top-level, unmasked, unclipped adjustment layers only, writing CUBE, 3DL, CSP, and LOOK; any masked or clipped adjustment is listed by name and excluded, as Photoshop does.
  - Gradient Map (IP-0626, IP-0638): stop bar with color and opacity stops, reverse, dither (`D01 T03 §3`), interpolation Perceptual, Linear, Classic, and a From Active Gradient command reading the gradient tool's current gradient; the full editor dialog arrives in `D03 T12 §9`.
  - Match Color and color transfer (IP-0627, IP-0636): Reinhard et al. statistics in Lab with luminance, color intensity, fade, neutralize, source document and layer, use selection in source or target for statistics, save and load statistics as JSON, and a color transfer from a preset or reference image with preserve luminance; Sample Colorize (GIMP, IP-0629) maps a grayscale image through a sample image's luminance-to-color table.
  - Replace Color (IP-0628): `D01 T03 §5` `ReplaceColors` with fuzziness, localized clusters from `D03 T10 §4`, add and subtract eyedroppers, and HSL result.
  - White Balance (Affinity, IP-0630): click, drag, and marquee pickers averaging a neutral through `D01 T03 §4` `WhiteBalance`.
  - OCIO (Affinity, IP-0631): OpenColorIO 2.4 built per RID with a thin C shim `isotone_ocio` (OCIO exposes only C++) under `build/native/opencolorio/`, P/Invoke in `src/Isotone.Core/Color/Ocio/`, a `docs/dev/decisions.md` row (BSD-3-Clause), source and destination color space pickers, and the built-in `ocio://default` config until `D03 T18 §4` adds config management; golden against `ocioconvert`.
  - New kinds in the registry: Split Toning (highlight and shadow hue and saturation, balance, IP-0632), Recolor (hue, saturation, lightness, IP-0633), Normals (rotation, scale, flip X and Y, OpenGL and DirectX conversion, IP-0634); Grain (IP-0635) registered with its page and disabled "Planned: D01 T07 §3" until that section enables it.
  - Tests: `LutFormatTests` (each format round-trips and a CUBE baked by `ociobakelut` applies within 1/255 of `ocioconvert`), `InferLutTests`, `MatchColorTests` (target statistics equal source statistics within 1 percent at full strength), `GradientMapTests`.
  - Commit: `"gesso: channel mixer, color lookup and LUTs, gradient map, match and replace color, and OCIO"`
- **Proof:** Format fidelity against OpenColorIO 2.4: LUT round trips are byte-equal after reread and the OCIO adjustment matches `ocioconvert` output within 1/255 on `tests/fixtures/gesso/color/ocio/`; cheaper substitute that fails: trilinear interpolation, which the tetrahedral OCIO golden rejects at saturated corners.

#### §5. Color adjustments III: threshold, posterize, invert, desaturate, color to alpha, and GIMP color operations

- **Deliverable:** Threshold (with channel choice and local threshold), Posterize, Invert and Value Invert, Desaturate modes, Color to Alpha, and every GIMP Colors menu operation plus Affinity's matte look, erase white paper, and dither filters, as adjustment kinds or destructive commands.
- **Depends On:** §1
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/color-adjust-3/. Job: a user finds every GIMP Colors command and every Affinity color filter with the same controls. Treatment: generated pages from each effect's parameter schema through the `D03 T05 §1` frame, with a histogram on Threshold. Cheaper substitute that fails: disabled menu items with no pages. Chrome: consume §1's host and the generated parameter views; do not hand-build a dialog per operation.
- **Runs:** `Requires: display-session -- the generated pages need an interactive desktop`
- **Catalog:** IP-0639 to IP-0655, IP-0657 to IP-0664 (25 features)
- **Hints:**
  - New operations live in `src/Isotone.Core/Imaging/Adjust/Color/` in the one `EffectRegistry`, each tagged with its GEGL op id for `D01 T06 §1`'s map and golden-tested against GIMP 3.2.6 `gimp-console` in `tests/fixtures/imaging/color-ops/<op>/` with `reference.txt`.
  - Threshold with channel choice (value, red, green, blue, alpha) and histogram on `D01 T03 §5` `Threshold` (IP-0639); `LocalThreshold` (radius, antialiasing, levels, Affinity, IP-0640); Threshold Alpha (IP-0662).
  - Posterize page on `D01 T03 §3` (IP-0641); Invert in perceptual and linear space extending `D01 T03 §5` `Invert` (IP-0642); `ValueInvert` (IP-0643).
  - Desaturate modes Luminance, Luma, Lightness, Average, Value (IP-0644): add Luma and Value to `D01 T03 §5` `Desaturate`.
  - `ColorToAlpha` with transparency and opacity thresholds (IP-0645, IP-0664) and Affinity's Erase White Paper as its white preset (IP-0659).
  - `ColorExchange` with per-channel thresholds (IP-0646), `RotateColors` with source and destination hue ranges and gray handling (IP-0647), Colorize with hue, saturation, lightness, and color on `D01 T03 §11` `Colorize` (IP-0648).
  - `ColorToGray` c2g with radius, samples, iterations, enhance shadows (IP-0649, seeded), `MonoMixer` with preserve luminosity (IP-0650).
  - Dither (IP-0651, IP-0660): extend `D01 T03 §3` with per-channel levels and the methods random, random covariant, arithmetic add and XOR (and covariant), blue noise and covariant, with a seed; Affinity's Monochrome Dither and Web-Safe Dither are presets.
  - `ExtractComponent` (RGB, HSV, HSL, CMYK, YCbCr, Lab, LCh, alpha, with invert and linear output, IP-0652), `RgbClip` (IP-0653), `Hot` (PAL or NTSC, reduce luminance or saturation, blacken, IP-0654), Sepia with strength and sRGB on `D01 T03 §11` `SepiaToning` (IP-0655).
  - `PaletteMap` recoloring by value from the active palette of §10 (IP-0657), `MatteLook` (lifted blacks and faded contrast, Affinity, as a kind; its live filter form is `D03 T14 §1`, IP-0658), `NegativeDarkroom` with GEGL's film and paper response presets (data LGPL-3.0, attributed, IP-0661), `SemiFlatten` against the background color (IP-0663).
  - Alien Map (IP-0656): its engine is `D01 T06 §13` (phase 22), so the Colors, Map entry is registered here disabled with "Planned: D01 T06 §13" and becomes live through `D03 T14 §2`'s generated dialog; see the final report's reroute.
  - Budget: every per-pixel operation under 150 ms on 24 megapixels (c2g and retinex-class spatial ones report progress and cancel); one Information line per apply.
  - Tests: one golden per operation (tolerances quoted), plus property tests from the `D01 T03 §1` harness (transparent stays transparent, same seed identical).
  - Commit: `"gesso: threshold, posterize, invert, desaturate, color to alpha, dither, and the GIMP color operations"`
- **Proof:** Format fidelity against GIMP 3.2.6: every operation's golden passes within its stated tolerance and the property suite passes; cheaper substitute that fails: color to alpha by thresholding alpha against a key color, which the `gegl:color-to-alpha` golden rejects on soft edges.

#### §6. Color analysis

- **Deliverable:** GIMP's Color Enhance, Border Average, Export Histogram, and Smooth Palette.
- **Depends On:** §2
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/color-analysis/. Job: a user can analyze and extract color information the way GIMP's Colors, Info menu does. Treatment: generated parameter pages, a save dialog for the histogram export, and a new-image result for Smooth Palette. Cheaper substitute that fails: a histogram screenshot instead of data. Chrome: consume the `D01 T03 §4` `Histogram`, the generated pages, and the color panel's foreground color.
- **Runs:** `Requires: display-session -- the pages and the export dialog need an interactive desktop`
- **Catalog:** IP-0665 to IP-0668 (4 features)
- **Hints:**
  - `ColorEnhance` (stretch chroma in LCh, IP-0665) in the registry with golden against `gegl:color-enhance`.
  - Border Average (IP-0666): thickness and bucket size, most frequent quantized border color set as the foreground color, one Information line, no document change.
  - Export Histogram (IP-0667): per-channel counts from `D01 T03 §4` `Histogram` for the layer or selection, written as CSV or plain text in GIMP's column layout (value, count per channel), through the atomic writer.
  - Smooth Palette (IP-0668): width, height, search depth, seeded random walk minimizing color distance, opening a new document with the striped palette.
  - Tests: `ColorEnhanceGoldenTests`, `BorderAverageTests` (a framed fixture yields the frame color), `HistogramExportTests` (sums equal pixel count), `SmoothPaletteTests` (seeded determinism).
  - Commit: `"gesso: color enhance, border average, histogram export, and smooth palette"`
- **Proof:** Unit test plus format fidelity: `ColorEnhanceGoldenTests` matches GIMP 3.2.6 within 2/255 and `HistogramExportTests` sums check; cheaper substitute that fails: exporting a 256-bin 8-bit histogram from a 16-bit layer, which the 16-bit fixture's count test catches.

#### §7. Image modes and bit depth

- **Deliverable:** Document color modes bitmap, grayscale, duotone, indexed, RGB, CMYK, Lab, and multichannel with native channel storage for non-RGB modes, precision 8, 16, and 32-bit integer and 16 and 32-bit float with linear, non-linear, and perceptual encodings, dithered precision reduction, the color table editor, and GIMP's Mode and Encoding submenus.
- **Depends On:** D03 T08 §1, D01 T04 §3, D01 T03 §3
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/modes/ (Indexed Color, Bitmap, Duotone, Color Table, Convert Precision, merge prompt). Job: a user can edit in the color mode and precision their output needs and convert between them knowingly. Treatment: Image, Mode (Photoshop list plus GIMP Mode and Encoding submenus) with conversion dialogs and a merge or flatten prompt when layers would change appearance. Cheaper substitute that fails: CMYK stored as RGB with a CMYK label. Chrome: consume `D01 T04 §3` converters and duotone model, `D01 T03 §3` quantizer and dithers, and the Duotone dialog moved from Stilus; do not keep Gesso's own `ColorConverter` for any conversion.
- **Runs:** `Requires: display-session -- the conversion dialogs need an interactive desktop`
- **Catalog:** IP-0673 to IP-0688 (16 features)
- **Hints:**
  - Move `DuotoneDialog.xaml` and `DuotoneDialogViewModel` from `src/Stilus/Isotone.Stilus.Desktop/Views/Bitmaps/` into `src/Isotone.UI/Color/Duotone/` as their second consumer (the `D01 T04 §3` Chrome line says the dialog lives in Stilus until a second app needs it), repoint Stilus, and retire Gesso's `Colors/ColorConverter.cs` conversions in favor of `D01 T04`.
  - Document mode model on the `D03 T08 §1` document: `DocumentColorMode { Bitmap, Grayscale, Duotone, Indexed, Rgb, Cmyk, Lab, Multichannel }`, `Precision { U8, U16, U32, F16, F32 }`, `Encoding { Linear, NonLinear, Perceptual }` (GIMP, IP-0684, IP-0685).
  - Non-RGB storage: grayscale, CMYK, Lab, duotone, and multichannel layers keep native planes in `PlanarTile` stores (N channels plus alpha, 256 px tiles) and composite for display through the `D01 T04` display transform; RGB-only operations run through `D01 T04 §3` `AutoConvertForEffect`; record this as an exception to `standards/gesso.md`'s premultiplied RGBA working format in a `docs/dev/decisions.md` row and add the sentence to the standard in the same commit.
  - Conversions (IP-0674 to IP-0676, IP-0682): RGB, CMYK, Lab, grayscale, multichannel through `D01 T04 §3` `BitmapModeConverter` with the document profiles and intent; the merge or flatten prompt (IP-0681) when adjustment layers, blend modes, or styles would render differently; Conditional Mode Change (IP-0688) with source-mode checkboxes and a target mode, run as one command.
  - Bitmap mode (IP-0673) from grayscale only: 50 Percent Threshold, Pattern Dither, Diffusion Dither, Halftone Screen (frequency, angle, shape), Custom Pattern (any grayscale image, or a library pattern once `D03 T12 §10` ships), output resolution, through `D01 T03 §3` `BilevelConverter` and `HalftoneScreen`.
  - Duotone (IP-0677): monotone to quadtone with inks, curves, overprint colors, and presets (`.ado` and `.isotoneduotone`) through `D01 T04 §3` and the moved dialog; `<gesso:duotone>` stores the spec beside the gray plane.
  - Indexed (IP-0678, IP-0683): palettes Exact, System, Web, Uniform, Adaptive, Optimized, Custom, Previous, GIMP's Generate Optimum, Web, Black and White, Custom palette, color count, forced colors, transparency and matte, dither None, Diffusion (with amount), Pattern, Noise, preserve exact colors, remove unused colors, dither transparency, through `D01 T03 §3` `PaletteBuilder` and `PalettedConverter`; indexed documents implement `D03 T10 §3`'s `IIndexedPixelSource`.
  - Color Table editor (Photoshop, IP-0679) with load and save `.act`, and GIMP's Rearrange Colormap (drag reorder remaps indices) and Set Colormap from a palette.
  - Precision (IP-0680, IP-0684, IP-0686, IP-0687): 8, 16, 32-bit per channel and GIMP's integer and float precisions, dithering when reducing precision on layers, text layers, and channels (`Gesso.Modes.DitherOnReduce`, `D01 T03 §3` ordered or Floyd-Steinberg), and Affinity's 32-bit to 8 or 16-bit conversion with a chosen output profile (HDR toning on conversion is `D03 T15 §3`).
  - Persistence: `<gesso:mode kind="cmyk" precision="u16" encoding="perceptual"/>` in the document metadata, native planes as 16-bit grayscale PNGs under `data/planes/<layer-id>/`, `<gesso:colormap>` for indexed documents, and every layer's stack PNG as its RGBA display conversion so GIMP and Krita show the right picture.
  - Undo "Convert to {Mode}" and "Convert Precision"; one Information line with source and target mode, precision, profile, and intent; budget: 24-megapixel RGB to CMYK under 1.5 seconds with progress and Cancel.
  - Tests: `ModeRoundTripTests` (CMYK document saves and reopens plane-exact; RGB to Lab to RGB within Delta E 2000 0.5 against `transicc`), `IndexedConversionTests` (palette size bound, forced colors present, exact colors preserved), `PrecisionTests` (16 to 8 with dither on a ramp shows no band longer than the golden's).
  - Commit: `"gesso: image modes, native CMYK and Lab planes, indexed and bitmap modes, duotone, and precision"`
- **Proof:** Format fidelity plus unit tests: `tests/fixtures/gesso/modes/` (CMYK, Lab, duotone, indexed, bitmap documents) reopen exactly, conversions match `transicc` goldens within Delta E 2000 0.5 and the indexed conversion matches GIMP 3.2.6 within its recorded tolerance; cheaper substitute that fails: storing CMYK as RGB with a label, which the plane-exact reopen assertion catches.

#### §8. Channel operations: split, merge, decompose, compose, apply image, calculations

- **Deliverable:** Apply Image with equations, Calculations, GIMP's Decompose, Compose, and Recompose in every listed color model, and channels as sources throughout.
- **Depends On:** D03 T10 §10
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/channel-ops/ (Apply Image, equations, Calculations, Decompose). Job: a user can blend channels and layers mathematically and pull an image apart by color model and put it back. Treatment: modal Apply Image and Calculations dialogs with live preview and an equations mode, and Decompose and Compose dialogs. Cheaper substitute that fails: Apply Image limited to Normal blending of RGB composites. Chrome: consume `D03 T10 §10`'s `ChannelSplitter` and `ChannelMerger`, the `D03 T09 §6` blend modes, and the `D03 T05 §1` dialog frame; do not add a second blend-mode implementation.
- **Runs:** `Requires: display-session -- the dialogs and previews need an interactive desktop`
- **Catalog:** IP-0689 to IP-0694 (6 features)
- **Hints:**
  - Apply Image (IP-0689): source document of the same size, layer or Merged, channel (color, alpha, transparency, layer mask, `D03 T10 §10` channels) with invert, blending (every `D03 T09 §6` mode plus Add and Subtract with scale and offset), opacity, preserve transparency, a mask with its own source, layer, channel, and invert, and Affinity's scale to fit; one "Apply Image" step.
  - `ExpressionCompiler` at `src/Isotone.Core/Imaging/Procedural/Expressions/ExpressionCompiler.cs` (the path `D01 T06 §9` names; this phase-18 section is its first builder, IP-0690): a whitelisted parser to `System.Linq.Expressions` delegates compiled once and run over float spans, no Roslyn and no reflection over user text, variables SR, SG, SB, SA, DR, DG, DB, DA, x, y, w, h, functions (sin, cos, tan, pow, sqrt, abs, min, max, clamp, lerp, rand with seed), and a chosen color space (RGB, HSL, Lab); `D01 T06 §9` adds its noise and procedural primitives to this compiler and `D01 T06 §13`'s Equations filter and `D03 T14 §10` consume it, so the suite has one expression engine.
  - Calculations (IP-0691): two sources (document, layer, channel, invert), blending, opacity, mask, result New Document, New Channel, or Selection.
  - Decompose (IP-0692): RGB, RGBA, Alpha, HSV, HSL, CMYK, Lab, LCh, YCbCr (ITU R470, R709, R470 256, R709 256) to layers or separate images, writing `gesso:decompose-source` so Recompose can rebuild the source; Compose and Recompose (IP-0693) through `ChannelMerger`.
  - Channels as sources (IP-0694): every source picker lists alpha and spot channels and layer masks.
  - Budget: Apply Image on 24 megapixels under 200 ms and an equation under 400 ms; one Information line per command.
  - Tests: `ApplyImageTests` (each blend mode equals the `D03 T09 §6` compositor on the same inputs), `ExpressionCompilerTests` (parser errors named with column, identity expressions exact, SIMD equals scalar), goldens of GIMP 3.2.6 decompose and compose for every model in `tests/fixtures/gesso/channel-ops/` within 1/255.
  - Commit: `"gesso: Apply Image, equations, Calculations, and decompose and compose"`
- **Proof:** Format fidelity against GIMP 3.2.6 plus unit tests: decompose then compose returns the source within 1/255 for every model and matches GIMP's layers, and `ExpressionCompilerTests` pass; cheaper substitute that fails: an interpreter walking the tree per pixel, which the 400 ms budget test catches.

#### §9. Color panels, pickers, eyedroppers, and color samplers

- **Deliverable:** Eyedropper, color picker tool, and color sampler extensions, screen sampling, the HUD picker, every color panel mode with dynamic sliders and extras, gamut and web warnings, the Photoshop color picker dialog, color history, the None swatch, and color harmonies.
- **Depends On:** D03 T03 §8, D01 T04 §2
- **Phase:** 18
- **Surface:** UI. Fidelity: docs/captures/gesso/color/ from `D03 T03 §8`, new captures to docs/captures/gesso/color-panels/ (each panel mode, picker dialog, HUD picker, sampler readouts, harmonies). Job: a user can pick, sample, and reason about color in any model with every competitor's convenience. Treatment: the color panel gains model sliders with dynamic tracks, wheel, boxes, cubes, ramps, palette, and watercolor modes; the picker dialog; a HUD picker; a color sampler tool with pinned markers; a harmonies panel. Cheaper substitute that fails: the Windows color dialog. Chrome: consume the `Isotone.UI` `ColorPicker` that `D03 T03 §8` moved, `D01 T04 §1` and `§2`, and the moved harmony engine; do not build a second picker control.
- **Runs:** `Requires: display-session -- panels, dialog, HUD, and screen sampling need an interactive desktop`
- **Catalog:** IP-0695 to IP-0716 (22 features)
- **Hints:**
  - Move `HarmonyEngine` from `src/Stilus/Isotone.Stilus.Core/Color/Harmonies/` (`D02 T09 §5`) into `src/Isotone.Core/Color/Harmonies/` as its second consumer and repoint Stilus; Gesso's Harmonies panel (Affinity chords, IP-0709) offers the types, preview, lock base color, and Add Chord to Swatches.
  - Eyedropper (IP-0695, IP-0696): the `D03 T10 §3` `SampleAverager` sizes to 101 by 101, sample Current Layer, Current and Below, All Layers, All Layers No Adjustments, Current and Below No Adjustments, and the sampling ring (new and current color over a gray ring), `Gesso.Color.SamplingRing`.
  - `TemporaryEyedropperModifier` (IP-0697): Alt in painting and fill tools samples into the foreground; `D03 T12 §5` wires it into every paint tool.
  - Sample anywhere on screen (IP-0698): dragging from the canvas past the window samples desktop pixels through a GDI `BitBlt` of the averaged region under the cursor, per-monitor DPI aware; no capture permission is needed.
  - HUD color picker (IP-0699, IP-0716): Alt+Shift+right-drag shows a hue strip or hue wheel in Small, Medium, or Large per `Gesso.Color.HudPicker`; the app or system picker preference `Gesso.Color.PickerKind`.
  - Color Sampler tool (IP-0700): up to 10 persistent samplers with sample size, move, delete, and Clear All, stored as `<gesso:samplers>`; readouts display in the `D03 T08 §11` Info panel.
  - Panel modes (IP-0701, IP-0715): sliders RGB, HSB, HSL, CMYK, Lab, Web, Grayscale with dynamic tracks, wheel, boxes, cubes, ramps, palette, and GIMP's watercolor selector, added as modes of the `Isotone.UI` picker.
  - Panel extras (Affinity, IP-0702): tint slider for global colors, opacity and noise, lock slider model, move sliders together, copy hex; Intensity slider for unbounded values on 32-bit documents (IP-0703; HDR display is `D03 T15 §4`); the color space name shown with values (GIMP, IP-0704).
  - Warnings (IP-0705): gamut warning through `D01 T04 §2` `IsInGamut` against the proof profile with a click to bring into gamut, web-safe warning, Only Web Colors.
  - Color Picker dialog (Photoshop, IP-0706): HSB, RGB, Lab, CMYK, hex, sample from the image while open, Add to Swatches, Color Libraries (§10); total ink coverage readout in the CMYK selector (GIMP, IP-0713) through `D01 T04 §1`.
  - Color history and recent colors per session and per document (IP-0707) and the None transparent swatch (Affinity, IP-0708).
  - GIMP Color Picker tool (IP-0710 to IP-0712, IP-0714): pick target Set Foreground, Set Background, Add to Palette, Pick Only, average radius, sample merged including layer filters (the merged composite already renders live filters), loupe, apply to the selection's fill, and the Shift info window with pixel, RGB, HSV, LCh, CMYK readouts.
  - One Information line per sampler change and swatch add; picking a color is not a document change and does not log.
  - Tests: `SampleAverageTests` (101 by 101 on a checker gives the exact mean), `ColorSamplerPersistenceTests`, `HarmonyEngineTests` still green after the move, `InkCoverageTests` against `transicc` totals.
  - Commit: `"gesso: color panel modes, the picker dialog, HUD picker, samplers, and harmonies"`
- **Proof:** Unit test plus driven run with capture: the tests pass, a driven sample of a known pixel through each sample size shows the expected hex in the panel, and each panel mode is captured; cheaper substitute that fails: a point-only eyedropper, which the 101 by 101 average test catches.

#### §10. Swatches, palettes, and color libraries

- **Deliverable:** A Swatches panel with document, application, system, and brand-kit palettes, global and registration colors, user-imported color books, GIMP's Palettes dialog, palette editor and commands, palette-to-gradient, the colormap dialog for indexed images, and every palette file format named, on palette readers moved to `Isotone.Core`.
- **Depends On:** §9, D01 T05 §5
- **Phase:** 18
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/swatches/ (Swatches panel, Palettes dialog, palette editor, colormap dialog, color book empty state). Job: a user can keep, import, export, and apply palettes from any tool they came from. Treatment: a Swatches panel with groups, search, grid or list, and scopes, a Palettes dialog and editor, and a Colormap dialog for indexed images. Cheaper substitute that fails: a fixed swatch strip that cannot open a user's ASE or GPL file. Chrome: consume the moved palette readers, the `D01 T05 §5` ASE reader and writer and brand kits, and §9's picker; do not keep a third ASE implementation.
- **Runs:** `Requires: display-session -- the panel, dialogs, and editor need an interactive desktop`
- **Catalog:** IP-0717 to IP-0731 (15 features)
- **Hints:**
  - Move the palette file readers and writers from `src/Stilus/Isotone.Stilus.Core/Color/PaletteFiles/` (`D02 T09 §4`) into `src/Isotone.Core/Color/Palettes/` as their second consumer (the recorded Gesso decision), repoint Stilus, and route ASE through `src/Isotone.Core/Brand/Ase/` from `D01 T05 §5` so the suite has one ASE reader and writer.
  - New formats in `src/Isotone.Core/Color/Palettes/` (IP-0718, IP-0728 to IP-0730): read ACT, CSS, RIFF PAL, Swatchbooker SBZ, CIE Lab text, Procreate `.swatches`, Krita KPL, and plain text; write GPL, KPL, CSS, PHP, Python, Java, text, ACO, and ASE; Affinity `.afpalette` read from operator-exported samples, moving to backlog B-045 through `add-todo` if the container proves undocumented.
  - Swatches panel (IP-0717, IP-0731): groups, New Swatch from the foreground, add from a color or the selected layer's color, edit, search, list and grid, per-swatch opacity; legacy sets and reset.
  - Palette scopes (Affinity, IP-0719): document palette stored as `<gesso:swatches>`, application palettes in `%LOCALAPPDATA%\Rizonesoft\Gesso\Palettes\`, read-only system palettes authored by Gesso, a default per color format, and the active `D01 T05 §5` brand kit palettes as their own scope.
  - Create palette from document, image, or gradient (IP-0720): N most frequent colors through `D01 T03 §3` `ColorReducer`, or sampled gradient stops.
  - Global colors and registration color (Affinity, IP-0721): swatches referenced by id from fill layers and, later, shape and text layers; editing a global swatch updates every reference in one command.
  - Color libraries (IP-0722): user-imported ACB and ASE color books shown in the picker and swatches through the moved `AcbReader`; nothing PANTONE-licensed ships, and the empty state explains importing a book the user owns.
  - GIMP Palettes dialog and editor (IP-0723 to IP-0725): grid or list, tags, new, duplicate, delete, refresh, show in folder, copy location; editor with edit, New from FG or BG, delete color, zoom, edit active palette; Export As, Offset, Sort (hue, saturation, value, luminance, and reverse), Merge.
  - Palette to Gradient and Palette to Repeating Gradient (IP-0726) write gradient resources into `%LOCALAPPDATA%\Rizonesoft\Gesso\Gradients\` on the `Isotone.Core` gradient model moved by `D03 T09 §8`; the Gradients panel listing them is `D03 T12 §9`.
  - Colormap dialog (GIMP, IP-0727) for §7's indexed documents: edit an entry, add from FG or BG, delete unused, index and hex display, and Select by index through `D03 T10 §3`'s `SelectByIndex` with Replace, Add, Subtract, Intersect.
  - Undo "Add Swatch", "Edit Global Color", "Edit Colormap"; one Information line per library change.
  - Tests in `tests/Isotone.Core.Tests/Color/Palettes/`: a round trip per writable format, reads of committed fixtures for every readable one with GIMP 3.2.6 (GPL, ACT, RIFF, CSS, text) and Krita 5.2 (KPL) as import oracles, `StilusPaletteRegressionTests` proving Stilus reads the same palettes after the move.
  - Commit: `"gesso: swatches, palettes, color books, and the colormap dialog on shared palette readers"`
- **Proof:** Format fidelity: every fixture in `tests/fixtures/core/palettes/` reads with every color, name, and group equal to the oracle's import, writable formats round-trip byte-equal, and Stilus's palette tests pass on the moved code; cheaper substitute that fails: a Gesso-local GPL parser, which the `grep` for a second palette reader outside `Isotone.Core` catches.

#### Sizing concerns

- §1 carries 20 catalog features and 16 hint items that include the render node, persistence, three panels, the targeted adjustment tool, the adjustment brush, and preset files; it lands near 28 checklist items, so the natural split is the adjustment brush and Quick Adjustments panel (IP-0578, IP-0579) as a follow-on section.
- §2 carries 23 features; grouping by kind keeps it near 25 items, and the GIMP operations item (IP-0601 to IP-0603) is the natural split.
- §5 carries 26 features; grouped by family it holds about 16 hint items but each operation needs its own golden, so it may reach 30; the natural split is threshold, posterize, invert, desaturate, and dither (IP-0639 to IP-0644, IP-0651, IP-0660, IP-0662) against the GIMP Map and Components operations.
- §7 changes the storage model for non-RGB documents (planar tiles) and adds four conversion dialogs; if the planar storage alone passes 15 items, split indexed, bitmap, and duotone (IP-0673, IP-0677 to IP-0679, IP-0683) into their own section.
- §9 carries 22 features; the GIMP Color Picker tool items (IP-0710 to IP-0714) are the natural split.

### todo/03-gesso/TODO-12-gesso-parity-painting.md -- `gesso-parity-painting`

- **Title:** "TODO-12 -- Gesso Parity: the Brush Engine, Painting Tools, Fills, Gradients, and Patterns"
- **Phase(s):** 19
- **Goal:** Gesso paints like Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6: the brush engine in `src/Gesso/Isotone.Gesso.Core/Painting/` (which stays in Gesso; Stilus's vector brushes never need it) grows computed, sampled, erodible, bristle, airbrush, and multi-nozzle tips, smoothing and stabilizers, build-up, wet edges, texture, dual brushes, and full pen dynamics with GIMP's dynamics matrix; brushes, dynamics, and tool presets live in searchable libraries that import ABR, GBR, GIH, VBR, and MyPaint MYB (painted by libmypaint); the brush, pencil, pixel, airbrush, ink, history, art history, mixer, smudge, color replacement, and eraser tools share one options model that the `D03 T13` retouch tools also consume; fill and stroke cover the Fill dialog, scripted patterns, line-art bucket fill, and stroke styles; gradients get every shape, interpolation, the GIMP segment editor, noise and diffusion gradients, and live gradient fill layers on the suite gradient model; patterns get a library, PAT import, pattern and fill layers, pattern preview, and the pattern stamp; and symmetry painting covers every competitor's modes. Every stroke is one undoable command recorded as tile snapshots, the engine allocates nothing per dab, and no Adobe, Affinity, MyPaint, or GIMP brush, gradient, or pattern pack is bundled; users import the files they own.
- **Current-state facts to verify (with claim candidates):**
  - There is no brush, painting, or tool code in Gesso yet; `D03 T03 §4` and `§6` create the tool system and the round brush this file extends. `<!-- claim: count "Brush" src/Gesso/src/Gesso.Core/**/*.cs = 0 -->` `<!-- claim: absent src/Gesso/src/Gesso.Core/Painting -->` `<!-- claim: absent src/Gesso/src/Gesso.Core/Tools -->`
  - The only gradient in Gesso today is the `GradientMap` adjustment type name, and no pattern type exists. `<!-- claim: count "Gradient" src/Gesso/src/Gesso.Core/**/*.cs = 1 -->` `<!-- claim: count "Pattern" src/Gesso/src/Gesso.Core/**/*.cs = 0 -->`
  - Raster layers tile at 256 px, the unit dab rendering, tile snapshots, and multi-threaded painting lock on. `<!-- claim: count "TileSize = 256" src/Gesso/src/Gesso.Core/Tiles/Tile.cs = 1 -->`
  - The main window binds no brush, gradient, or fill command today. `<!-- claim: count "Brush|Gradient|Fill" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 0 -->`
  - `Isotone.Core` does not exist yet, so the gradient model this file extends arrives by the `D03 T09 §8` move. `<!-- claim: absent src/Isotone.Core -->`
- **Inputs and XREFs:** `standards/gesso.md` (zero allocations per dab, SIMD with scalar reference, tile snapshots, GPU parity where a GPU path exists); `standards/shared.md`; GIMP 3.2.6 `devel-docs` for GBR, GIH, VBR, PAT, and GGR, and its `app/core/gimpbrush-load.c` and `gimpgradient-load.c` as the ABR and GRD reading references; Krita 5.2's ABR loader as the second ABR oracle; Adobe Photoshop File Formats Specification (Descriptor structure, pattern data) for ABR settings, GRD, and Photoshop PAT; psd-tools (MIT) as the pattern-block reading oracle; libmypaint 1.6.1 (ISC) and the MyPaint brush file format v3; Fourey et al., "A fast and efficient semi-guided algorithm for flat coloring line-arts" (2018) as GIMP's line-art fill reference; Orzan et al., "Diffusion Curves" (SIGGRAPH 2008); Autodesk's hatch pattern definition format for CAD `.pat`; -> XREF: D03 T03 §6 (the `BrushEngine`, brush tool, and eraser this file extends); -> XREF: D03 T03 §8 (the paint bucket and gradient tool §8 and §9 extend); -> XREF: D03 T03 §2 (tile snapshots and history states the history brush reads); -> XREF: D03 T08 §6 (snapshots as history brush sources); -> XREF: D03 T09 §1 (transparency lock behind protect alpha and non-paintable layer kinds); -> XREF: D03 T09 §6 (blend modes including Behind and Clear for paint modes); -> XREF: D03 T10 §1 (selections that fill and stroke read); -> XREF: D03 T10 §3 (the flood engine and `SampleSource` behind the bucket, magic eraser, background eraser, and color replacement limits); -> XREF: D03 T10 §8 (the border morphology Stroke Selection uses); -> XREF: D03 T09 §8 (the gradient model moved to `src/Isotone.Core/Paint/Gradients/` that §9 extends, and the `IPatternLibrary` interface §10 implements); -> XREF: D03 T09 §6 (the Kubelka-Munk pigment mode kernel §6's pigment mixing reuses); -> XREF: D03 T11 §9 (the temporary eyedropper §5 wires); -> XREF: D03 T11 §10 (palette gradients §9 lists); -> XREF: D03 T13 §1, D03 T13 §2, D03 T13 §4 (retouch tools consuming §1's stabilizer and wet edges, §5's shared options, and §11's symmetry); -> XREF: D03 T13 §3 (the content-aware engine behind the Fill dialog's content-aware and inpainting contents); -> XREF: D03 T15 §4 (HDR display for §5's 32-bit painting); -> XREF: D03 T16 §5 (paths for stroke path, fill path, place along path, and symmetry from a path); -> XREF: D03 T16 §7 (shape layers that gain gradient fill and stroke contexts); -> XREF: D03 T17 §3 and D03 T17 §13 (PSD gradient and pattern fill layers read and written); -> XREF: D03 T20 §6 (pen, pressure curves, and input devices that feed §2's dynamics); -> XREF: D03 T20 §7 (the presets manager listing brushes, dynamics, tool presets, gradients, and patterns); -> XREF: D01 T03 §3 (ordered and error-diffusion dither for gradients).
- **Adjacency:** list=applicable (Brushes, Tool Presets, MyPaint Brushes, Gradients, and Patterns panels with groups, tags, and search); document=not-applicable (no printed output of its own); settings=applicable (every tool option is a `Gesso.Painting.*`, `Gesso.Tools.<Tool>.*`, `Gesso.Gradients.*`, or `Gesso.Patterns.*` key with a named consumer); reporting=applicable (the ABR and brush import report, stroke previews, the bristle preview); notifications=applicable (progress and Cancel for large fills, line-art fill, diffusion gradients, and library imports); permissions=applicable (unsupported or corrupt brush, pattern, and gradient files refused by name; protected text, link, and vector layers); audit=applicable (one Serilog Information line per stroke, fill, and library change); exchange=applicable (ABR, GBR, GIH, VBR, GDYN, MYB, GGR, GRD, SVG gradients, Photoshop and GIMP PAT, CAD hatch PAT, CSS and POV-Ray gradient export); reverse=applicable (every stroke, fill, and gradient is one undo step; library deletes go to a recycle folder)

#### §1. The brush engine I: tips, spacing, smoothing, and wet media

- **Deliverable:** A brush engine with computed, sampled, erodible, bristle, airbrush, and multi-nozzle tips, Photoshop smoothing and GIMP smooth stroke, Affinity's rope and window stabilizers, build-up, wet edges with a custom profile, noise and protect texture, a HUD for size and hardness, and multi-threaded dab rendering at zero allocations per dab.
- **Depends On:** D03 T03 §6
- **Phase:** 19
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the options bar, new captures to docs/captures/gesso/brush-engine/ (tip types, bristle preview, stabilizer rope, HUD). Job: a painter gets strokes that feel like Photoshop, Affinity, or GIMP at pen speed on large canvases. Treatment: tip types chosen in the brush settings, smoothing and stabilizer controls on the options bar, a bristle preview window, and an Alt+right-drag HUD. Cheaper substitute that fails: one round dab with a hardness falloff. Chrome: consume `D03 T03 §6`'s `BrushEngine`, the tool system, and `TileSnapshotCommand`; do not add a second dab rasterizer.
- **Runs:** `Requires: display-session -- pen strokes, the HUD, and captures need an interactive desktop`
- **Catalog:** IP-0737 to IP-0755 (19 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-4.4` (promotes B-020); the integration commit deletes B-020 from `todo/backlog.md`; its tips land here, dynamics and texture in §2, and presets with ABR import and an import report in §3.
  - `BrushTip` hierarchy in `src/Gesso/Isotone.Gesso.Core/Painting/Tips/`: `ComputedTip` (size, angle, roundness, hardness, spacing, flip X and Y, and GIMP's shared aspect ratio and angle, IP-0739, IP-0740), `SampledTip` (8-bit mask or RGBA color tip, IP-0742), `ErodibleTip` (point, flat, round, square, triangle, softness, wears with stroke length, Sharpen Tip), `BristleTip` (bristles, length, thickness, stiffness, angle), `AirbrushTip` (hardness, distortion, granularity, spatter size and amount) (IP-0741); each rasterizes into a pooled dab buffer.
  - Define Brush Preset from the selection or image and New round and square brushes (IP-0738, IP-0742): grayscale tips up to 5,000 px, color tips kept when the preset is a color brush.
  - `NozzleSet` (IP-0743): several tips with a controller (random, sequential, pressure, direction) and interpolation between nozzles; §3's GIH import maps onto it.
  - `StrokeSmoother` in `Painting/Input/` (IP-0744): Photoshop smoothing 0 to 100 percent with Pulled String, Stroke Catch-up, Catch-up on Stroke End, Adjust for Zoom, and GIMP's Smooth Stroke quality and weight; `StrokeStabilizer` (Affinity, IP-0745, IP-0752, IP-0755) with Rope (length) and Window (size) modes for paint and erase.
  - Build-up and airbrush (IP-0746): timer-driven dabs at `rate` while the pen rests, with accumulation to the flow limit.
  - Wet edges (IP-0747, IP-0753): the dab alpha profile raised at the rim, with Affinity's custom edge profile curve; Noise and Protect Texture (Photoshop, IP-0748); Flow stored in the preset (IP-0749).
  - `PaintThread` (GIMP, IP-0750): stroke events leave the UI thread, dabs render on per-tile workers with tile locks, count from `Gesso.Painting.Threads` (default processor count minus one); XCF save threading is `D03 T17 §4`.
  - HUD (Photoshop, IP-0754): Alt+right-drag horizontal changes size, vertical changes hardness (`Gesso.Painting.HudVertical` = Hardness or Opacity).
  - Shared options for retouching (Affinity, IP-0751): stabilizer and wet edges live in `PaintToolOptions` (§5), which every `D03 T13` brush-based tool consumes.
  - Recorded strokes: `tests/fixtures/gesso/painting/strokes/*.json` hold timestamped pen samples (x, y, pressure, tilt, twist) replayed deterministically; each tip type has a golden PNG within 1/255.
  - Budgets: 0 B allocated per dab (`GC.GetAllocatedBytesForCurrentThread` over 10,000 dabs), a 300 px sampled tip at 10 percent spacing renders 10,000 dabs on a 16-bit 8,000 by 6,000 layer under 1 second; one Information line per stroke (`Painted {Tool} {Dabs} dabs on {Layer} in {Ms} ms`), undo "Brush Stroke".
  - Commit: `"gesso: brush tips, smoothing, stabilizers, build-up, wet edges, and threaded painting"`
- **Proof:** Unit test plus benchmark: `BrushTipGoldenTests` replay each recorded stroke per tip type within 1/255 of its golden, `StrokeSmootherTests` show pulled-string lag equals the set length, and `DabAllocationTests` quote 0 B per dab; cheaper substitute that fails: allocating a dab bitmap per stamp, which the allocation test catches.

#### §2. The brush engine II: dynamics

- **Deliverable:** Pen and stroke dynamics (pressure, tilt, azimuth, barrel rotation, velocity, direction, wheel, distance, fade, random) mapped by curves to shape, scattering, texture, dual brush, color, and transfer, plus brush pose and GIMP's dynamics matrix and editor, all seeded and reproducible.
- **Depends On:** §1
- **Phase:** 19
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/brush-dynamics/ (Brush Settings dynamics pages, GIMP dynamics matrix editor). Job: a painter can make a brush respond to the pen exactly as their Photoshop, Affinity, or GIMP brushes do. Treatment: Brush Settings pages Shape Dynamics, Scattering, Texture, Dual Brush, Color Dynamics, Transfer, Brush Pose, each with jitter, minimum, and control; and a matrix editor of inputs against outputs with curves. Cheaper substitute that fails: pressure to size only. Chrome: consume §1's tips and `PaintThread`, the WPF stylus stack, and the curve editor of `D03 T05 §2`; do not read pen data outside one `PenSample` source.
- **Runs:** `Requires: display-session -- pen dynamics need an interactive desktop and a stylus or a recorded replay`
- **Catalog:** IP-0756 to IP-0765 (10 features)
- **Hints:**
  - `PenSample` source in `Painting/Input/`: pressure, tilt X and Y, azimuth, barrel rotation, and wheel from WPF `StylusPoint` properties (`NormalPressure`, `XTiltOrientation`, `YTiltOrientation`, `TwistOrientation`) and the Windows Ink pointer path, with mouse fallbacks; pressure curves and device settings are `D03 T20 §6`.
  - `DynamicsInput` (Pressure, Tilt, Azimuth, Barrel Rotation, Velocity, Direction, Wheel, Distance, Fade, Cyclic, Random) and `DynamicsMapping { Input, Output, Curve }` with ramp curves (IP-0757); outputs opacity, size, angle, color, hardness, force, aspect ratio, spacing, rate, flow, jitter (GIMP matrix, IP-0764) plus GIMP's fade length and repeat (none, loop, sawtooth, triangle) and color from gradient.
  - Shape Dynamics (IP-0756): size, angle, roundness jitter with minimum and control, flip X and Y jitter; Brush Pose and Brush Projection (Photoshop, IP-0758) override tilt, rotation, and pressure.
  - Scattering (IP-0759): scatter percent, both axes, count, count jitter, and GIMP's shared Apply Jitter amount.
  - Texture (IP-0760): patterns read through `D03 T09 §8`'s `IPatternLibrary` (its first implementation serves PSD, ASL, and layer patterns; §10 replaces it with the library); invert, scale, brightness, contrast, texture each tip, modes (multiply, subtract, darken, overlay, color dodge, color burn, linear burn, hard mix, linear height, height), depth with minimum and jitter, and copy texture to other tools.
  - Dual Brush and Affinity sub-brushes (IP-0761): a second tip (or several) with its own size, spacing, scatter, count, dynamics, and blend mode, masking the primary.
  - Color Dynamics (IP-0762): foreground and background jitter, hue, saturation, brightness jitter, purity, apply per tip; Transfer (IP-0763): opacity, flow, wetness, and mix jitter with controls.
  - Dynamics resources (IP-0765): the paint tool dynamics selector, Enable Dynamics, and dynamics options shared across paint tools, stored as `.gessodyn`; GIMP `.gdyn` read in §3.
  - Determinism: jitter uses the `D01 T03` seeded counter RNG with a per-stroke seed stored in the stroke command, so redo and replay are byte-identical.
  - Budget: all dynamics on add less than 25 percent to §1's 10,000-dab benchmark and keep 0 B per dab.
  - Tests: `DynamicsMatrixTests` (each input to each output on synthetic samples), `JitterDeterminismTests`, recorded pen fixtures with tilt and barrel rotation replayed to goldens within 1/255.
  - Commit: `"gesso: brush dynamics, texture, dual brush, and the dynamics matrix"`
- **Proof:** Unit test plus driven replay: recorded pen strokes with pressure, tilt, and barrel rotation replay to their goldens within 1/255 and replay twice byte-identically; cheaper substitute that fails: unseeded `Random` jitter, which the determinism test catches.

#### §3. Brush presets, libraries, and tool presets

- **Deliverable:** Brush presets and libraries with the Brushes and Brush Settings panels, recent brushes per layer and per tool, ABR and Affinity brush import and export with an import report, GIMP's GBR, GIH, and VBR brushes and parametric editor, clipboard brushes, dynamics presets, and tool presets with their panel and picker.
- **Depends On:** §2
- **Phase:** 19
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/brush-library/ (Brushes panel grid and list, Brush Settings, import report, parametric editor, Tool Presets panel). Job: a painter can bring their brush sets from any of the three apps, find a brush fast, and save tool setups. Treatment: a Brushes panel with groups, search, recent brushes, and stroke-preview thumbnails; a Brush Settings panel with live preview and locks; GIMP's brush and dynamics dialogs as the same panel's commands; a Tool Presets panel with Current Tool Only. Cheaper substitute that fails: a flat list of tip images. Chrome: consume §1 and §2 models, the theme, and the resource folder pattern `D03 T20 §7` manages; do not build a second library store per resource kind.
- **Runs:** `Requires: display-session -- the panels, import report, and editors need an interactive desktop`
- **Catalog:** IP-0766 to IP-0787 (22 features)
- **Hints:**
  - `BrushPreset` (`.gessobrush` JSON: tip, dynamics, texture, dual, color, transfer, and optional tool settings, size, and color) and `ResourceLibrary<T>` in `Isotone.Gesso.Core/Resources/` over `%LOCALAPPDATA%\Rizonesoft\Gesso\Brushes\` with folders as groups, tags, favorites, and a recycle folder; §4, §9, and §10 reuse `ResourceLibrary<T>`.
  - Brushes panel (IP-0771, IP-0787, IP-0778, IP-0767): groups and categories, search, recent brushes, list and thumbnail views with stroke previews, default categories of brushes authored by Gesso, GIMP's grid and list, tags, spacing, refresh, open as image, copy location, show in folder, and the context menu.
  - Brush Settings panel (IP-0770): live stroke preview, lock attributes, clear brush controls, reset, create new brush from settings; preset picker and management (IP-0772, IP-0776): size, rename, duplicate, delete, move, update, reset, modified indicator, and New Brush Preset options capture size, include tool settings, include color.
  - Tool association (Affinity, IP-0773): a brush switches to its associated tool and each tool remembers its last brush in `Gesso.Tools.<Tool>.LastBrush`; recent brushes per layer (Affinity, IP-0769) as `gesso:recent-brushes` on the layer element; the shared paint tool brush selector (GIMP, IP-0777).
  - `AbrReader` and `AbrWriter` in `src/Gesso/Isotone.Gesso.FileFormats/Brushes/Abr/` (IP-0768, IP-0774): ABR v1 and v2 sampled tips and v6 to v10 `samp` tips plus the `desc` descriptor mapped onto tips, dynamics, scattering, texture, dual brush, color, and transfer; export writes v6 with sampled tips and the settings the descriptor maps; an import report lists per preset what mapped, what was approximated, and what was dropped, shown after import and logged at Information.
  - Affinity `.afbrushes` import and export (IP-0774) from operator-exported samples; if the container proves undocumented, those rows move to backlog B-045 through `add-todo` in the same commit and ABR remains the Affinity interchange path.
  - GIMP formats (IP-0780 to IP-0782): GBR v2 grayscale and color brushes, GIH image hose with ranks and selection modes (incremental, angular, random, velocity, pressure, xtilt, ytilt) mapped onto §1's `NozzleSet`, and VBR with a parametric brush editor (circle, square, diamond, radius, spikes, hardness, aspect, angle, spacing).
  - Clipboard brush and Paste as New Brush (GIMP, IP-0766, IP-0779): name, file, spacing, up to 8,192 px.
  - Legacy brush sets and Reset to factory brushes (IP-0775): restores Gesso's authored defaults only.
  - Dynamics presets dialog (GIMP, IP-0783): new, duplicate, delete, refresh, copy location, show in folder over `.gessodyn` plus GIMP `.gdyn` read.
  - Tool presets (IP-0784 to IP-0786): `.gessotoolpreset` JSON of any tool's options, Tool Presets panel and options bar picker with Current Tool Only, save, restore, edit, delete, and GIMP's tool preset editor.
  - Fixtures: ABR v2 and v6 files the operator authors in Photoshop 27.10 from Gesso-drawn tips and GBR, GIH, VBR files authored in GIMP 3.2.6, committed under CC0 in `tests/fixtures/gesso/brushes/` with a README naming the source of each.
  - Undo is at library level (recycle folder); one Information line per import, export, and library change.
  - Tests: `AbrReaderTests` (tips byte-equal to GIMP 3.2.6's loaded tips, settings mapped per the report), `GimpBrushFormatTests` (round trip of GBR, GIH, VBR), `ToolPresetTests`, `BrushLibraryTests` (search, tags, recycle).
  - Commit: `"gesso: brush libraries, ABR and GIMP brush formats, and tool presets"`
- **Proof:** Format fidelity against GIMP 3.2.6 and Krita 5.2: every ABR fixture's tips match both oracles' loaded tips byte-equal and GBR, GIH, VBR round-trip byte-equal; cheaper substitute that fails: importing ABR tips while dropping every setting silently, which the import report assertion on the v6 fixture catches.

#### §4. MyPaint brushes

- **Deliverable:** GIMP's MyPaint Brush tool on libmypaint 1.6.1 with MYB loading (including MyPaint 2.0 settings and barrel rotation), its options, and a MyPaint Brushes dialog.
- **Depends On:** §1
- **Phase:** 19
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/mypaint/. Job: a painter can use their MyPaint brush files in Gesso with the same response. Treatment: a MyPaint Brush tool with GIMP's options and a MyPaint Brushes dialog. Cheaper substitute that fails: converting MYB settings into Gesso presets approximately. Chrome: consume §1's `PaintThread`, tile snapshots, §3's `ResourceLibrary<T>`, and §2's `PenSample`; libmypaint paints only through the tile adapter.
- **Runs:** `Requires: display-session -- MyPaint strokes and the dialog need an interactive desktop`
- **Catalog:** IP-0788 to IP-0791 (4 features)
- **Hints:**
  - Build libmypaint 1.6.1 (ISC) and json-c (MIT) for `win-x64` and `win-arm64` with `build/native/libmypaint/build.ps1`, SHA-256 and compiler recorded in `SOURCE.txt`, binaries under `src/Gesso/Isotone.Gesso.Core/runtimes/<rid>/native/`, licenses in THIRD-PARTY-NOTICES, and a `docs/dev/decisions.md` row.
  - `[LibraryImport("libmypaint")]` bindings in `Painting/MyPaint/Native/` for brush creation, settings, `mypaint_brush_stroke_to` with the 2.0 variant taking barrel rotation, and surface callbacks.
  - `MyPaintSurfaceAdapter` implementing `MyPaintSurface2` `draw_dab` and `get_color` over Gesso's 256 px tiles (converting libmypaint's 15-bit fixed-point premultiplied RGBA per tile) inside one tile-snapshot stroke.
  - MYB loading (IP-0788, IP-0789): JSON version 3 settings and input curves with the `_prev.png` preview, including MyPaint 2.0 settings (barrel rotation input, pigment, posterize, gridmap).
  - Options (IP-0790): radius, opacity, base opacity, hardness, gain (pressure gain), smooth stroke, erase, no erasing, follow view zoom and rotation.
  - MyPaint Brushes dialog (IP-0791) on `ResourceLibrary<T>` over `%LOCALAPPDATA%\Rizonesoft\Gesso\MyPaintBrushes\`: grid and list, tags, refresh, copy location, show in folder; no brush pack is bundled.
  - Determinism: libmypaint's random state is seeded per stroke and the seed stored in the stroke command.
  - Tests: `MybLoaderTests` on MYB fixtures authored in MyPaint 2.0 (CC0), `MyPaintStrokeTests` replaying a recorded stroke against a golden rendered by GIMP 3.2.6's MyPaint tool with the same brush and seed within 2/255.
  - Commit: `"gesso: MyPaint brushes on libmypaint"`
- **Proof:** Format fidelity against GIMP 3.2.6: the replayed stroke matches GIMP's MyPaint Brush output within 2/255 mean; cheaper substitute that fails: translating MYB into Gesso tip settings, which the golden rejects on a smudging MYB brush.

#### §5. Painting tools and history brushes

- **Deliverable:** The shared paint options every paint and retouch tool reads, the pencil, pixel, airbrush, and ink tools, painting conveniences (straight lines, number keys, temporary picker, on-canvas size), HDR painting, non-paintable layer handling, and the history, undo, and art history brushes.
- **Depends On:** §2
- **Phase:** 19
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for options bars, new captures to docs/captures/gesso/paint-tools/ (ink blob editor, history brush source, art history styles). Job: a painter gets every paint tool and shortcut they rely on, with one consistent options model. Treatment: one `PaintToolOptions` rendered on each tool's options bar, the GIMP ink blob editor, the History panel source marker for the history brush. Cheaper substitute that fails: each tool with its own partial copy of options. Chrome: consume §1 and §2, the `D03 T03 §2` history and `D03 T08 §6` snapshots, and `D03 T11 §9`'s temporary eyedropper; do not duplicate option controls per tool.
- **Runs:** `Requires: display-session -- the tools, shortcuts, and captures need an interactive desktop`
- **Catalog:** IP-0792 to IP-0813 (22 features)
- **Hints:**
  - `PaintToolOptions` in `Painting/Tools/` (IP-0809 to IP-0811, IP-0793 to IP-0797): blend mode including Behind, Clear, and Overwrite from `D03 T09 §6`, opacity, flow, force (GIMP brush gain), lock brush to view, incremental, expand layers (amount, fill with transparency, background, foreground, or pattern, and fill the layer mask with white or black), hard edge, smooth stroke, jitter, dynamics, and Affinity's width, hardness, force pressure, and brush editor button; every `D03 T13` brush-based tool binds the same model.
  - Straight and constrained lines (IP-0798): Shift+click draws a line from the last point, Ctrl+Shift constrains to 15 degree steps (GIMP).
  - Temporary color picker (IP-0799): wire `D03 T11 §9`'s `TemporaryEyedropperModifier` (Alt, and Ctrl in GIMP's keymap) into every paint tool.
  - On-canvas size and hardness (IP-0800) through §1's HUD, with arrow keys rotating the nozzle angle; number keys set opacity and Shift+number sets flow (IP-0801).
  - HDR painting (IP-0802): on 32-bit float documents dabs blend in float and keep values above 1.0 (the `D03 T11 §9` intensity slider supplies them); HDR preview is `D03 T15 §4`.
  - Non-paintable layers (IP-0803): painting on a text, shape, smart object, link, or vector layer follows `Gesso.Painting.OnNonPixelLayer` (`NewLayerAbove` as Affinity, `AskRasterize` as Photoshop, `Refuse`), and text, link, and vector layers are never rasterized silently.
  - Pencil and Pixel tool (IP-0804, IP-0813): aliased coverage, Auto Erase (starting on the foreground color paints the background), and Affinity's alternate modifier to erase, paint the background color, or undo from the snapshot.
  - Airbrush tool (GIMP, IP-0805): rate, flow, motion only on §1's build-up; Ink tool (GIMP, IP-0806): size, angle, sensitivity to size, tilt, and speed, nib type circle, square, diamond, and the blob shape editor, rendered as GIMP's convex blob hull between samples.
  - History brush and undo brush (IP-0792, IP-0807): source a history state (`D03 T03 §2`) or a snapshot (`D03 T08 §6`) marked in the History panel, reconstructing only the tiles under the dab, with blend mode and protect alpha.
  - Art History brush (IP-0808): styles Tight Short, Tight Medium, Tight Long, Loose Medium, Loose Long, Dab, Tight Curl, Loose Curl, area, and tolerance, generating seeded strokes that sample the source state's color.
  - Protect alpha (IP-0812): the `D03 T09 §1` transparency lock, one flag not a second lock.
  - Undo names per tool ("Pencil", "Ink", "History Brush"); one Information line per stroke (§1's format).
  - Tests: `PaintToolOptionsTests` (one model serialized per tool, expand layers grows bounds), `AutoEraseTests`, `HistoryBrushTests` (painting from an earlier state restores its pixels under the stroke only), `InkBlobTests` against a golden, `NonPixelLayerPolicyTests`.
  - Commit: `"gesso: shared paint options, pencil, pixel, airbrush, ink, and history brushes"`
- **Proof:** Unit test plus driven run: the tests pass and a driven history-brush stroke over a filtered region restores the pre-filter pixels under the stroke (hash of the region quoted) while outside pixels keep the filter; cheaper substitute that fails: a history brush that reverts the whole layer, which the outside-region hash catches.

#### §6. Mixer brush, smudge, and color replacement

- **Deliverable:** Photoshop's Mixer Brush and Affinity's paint mixer brush with RGB and pigment mixing, GIMP, Photoshop, and Affinity smudge, and the color replacement tools with sampling and limits.
- **Depends On:** §5
- **Phase:** 19
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for options bars, new captures to docs/captures/gesso/mixer/ (reservoir swatch, pigment against RGB mixing). Job: a painter can blend wet paint on canvas and recolor areas while keeping texture. Treatment: options bars with reservoir and pickup previews and mixing presets. Cheaper substitute that fails: a smudge that blurs. Chrome: consume §5's `PaintToolOptions`, §1's engine, and the `D03 T10 §3` flood engine for replacement limits.
- **Runs:** `Requires: display-session -- wet mixing strokes need an interactive desktop`
- **Catalog:** IP-0814 to IP-0822 (9 features)
- **Hints:**
  - `MixerBrush` (Photoshop, IP-0816, IP-0817): reservoir and pickup buffers per stroke, wet, load, mix, flow, sample all layers, load and clean after each stroke, and blend presets (Dry, Moist, Wet, Very Wet and their load and mix variants) as data.
  - Paint mixer brush (Affinity, IP-0822): strength, load, clean, auto load, auto clean, mixing model RGB or Pigment.
  - Pigment mixing (IP-0818): the mixer's reservoir blends through the Kubelka-Munk pigment kernel of `D03 T09 §6`'s Pigment mode (IP-0327), not a second mixer; Mixbox stays rejected (CC BY-NC 4.0 is not GPL-3.0 compatible), as recorded there.
  - Smudge (IP-0819, IP-0820): GIMP strength, rate, flow, no erasing effect, sample merged; Photoshop strength, mode, finger painting, sample all layers; Affinity's options; the shared hard edge option (§7) applies.
  - Color replacement (IP-0814, IP-0815, IP-0821): modes hue, saturation, color, luminosity; sampling continuous, once, background swatch; limits discontiguous, contiguous, find edges through the `D03 T10 §3` flood engine bounded to the dab ROI; tolerance, anti-alias.
  - Budget: mixer strokes at 0 B per dab and within 1.5 times §1's benchmark time.
  - Tests: `MixerBrushTests` (clean after stroke empties the reservoir; wet 0 behaves like the brush), `PigmentMixingTests` (through the shared kernel, blue plus yellow gives green and RGB gives gray), `ColorReplacementTests` (contiguous limit stops at an edge).
  - Commit: `"gesso: mixer brush, pigment mixing, smudge, and color replacement"`
- **Proof:** Unit test plus driven run with capture: the tests pass and a driven pigment mix of blue into yellow is captured beside the RGB mix; cheaper substitute that fails: RGB averaging labeled pigment, which the blue-plus-yellow hue assertion catches.

#### §7. Erasers

- **Deliverable:** Eraser modes, erase to history, anti-erase, the background eraser and Affinity's background erase brush with sampling and limits, and the magic eraser and flood erase.
- **Depends On:** §5
- **Phase:** 19
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for options bars, new captures to docs/captures/gesso/erasers/. Job: a user can remove pixels by brush, by color, or by region, and bring them back. Treatment: eraser options bars and the anti-erase modifier. Cheaper substitute that fails: an eraser that paints white. Chrome: consume §5's options and history source, and the `D03 T10 §3` flood engine.
- **Runs:** `Requires: display-session -- eraser strokes need an interactive desktop`
- **Catalog:** IP-0823 to IP-0831 (9 features)
- **Hints:**
  - Eraser modes (Photoshop, IP-0823): brush, pencil, block, with flow, airbrush, and smoothing; the shared hard edge option for eraser and smudge (GIMP, IP-0829).
  - Erase to History (IP-0824) through §5's history brush source.
  - Anti-erase (GIMP, Alt, IP-0828): because Gesso stores premultiplied pixels, colors under erased alpha come from the most recent history state where the pixel was visible (bounded by the history limit), documented in the tool's help.
  - Background eraser (IP-0825, IP-0826, IP-0830): tolerance, protect foreground color, sampling continuous, once, background swatch, limits discontiguous, contiguous, find edges, and Affinity's background erase brush options.
  - Magic eraser and flood erase (IP-0827, IP-0831): tolerance, anti-alias, contiguous, sample all layers, opacity, through the `D03 T10 §3` flood engine.
  - Background layers without alpha erase to the background color (the existing `D03 T03 §6` rule).
  - Tests: `AntiEraseTests` (erase then anti-erase restores colors byte-equal), `BackgroundEraserTests` (protect foreground keeps the protected color), `MagicEraserTests` against a GIMP 3.2.6 fuzzy-select-and-clear golden.
  - Commit: `"gesso: eraser modes, anti-erase, background eraser, and magic eraser"`
- **Proof:** Unit test: `AntiEraseTests` and `MagicEraserTests` pass; cheaper substitute that fails: anti-erase that raises alpha on black, which the byte-equal color restore catches.

#### §8. Fill and stroke

- **Deliverable:** The Fill dialog and default fill shortcuts, matte fill, scripted pattern fills, paint bucket extensions including fill whole selection and similar colors, GIMP's line-art bucket fill, and Stroke Selection with location, line styles, and stroking with a paint tool.
- **Depends On:** D03 T10 §1
- **Phase:** 19
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/fill-stroke/ (Fill dialog, scripted pattern options, line-art fill, Stroke and Stroke with line style dialogs). Job: a user can fill and outline selections and regions with any content, including flat coloring of line art. Treatment: modal Fill and Stroke dialogs, bucket options on the options bar, and GIMP's Stroke Selection dialog with Line and Paint Tool tabs. Cheaper substitute that fails: a bucket that floods from one layer with an RGB tolerance only. Chrome: consume `D03 T10 §1` selections, the `D03 T10 §3` flood engine, `D03 T10 §8` border morphology, §5's paint tools, and §10's patterns when present; do not add a second flood fill.
- **Runs:** `Requires: display-session -- the dialogs and bucket fills need an interactive desktop`
- **Catalog:** IP-0846 to IP-0860 (15 features)
- **Hints:**
  - Fill dialog (IP-0849, IP-0853, IP-0846): contents Foreground, Background, Color, Pattern (§10), History, Black, 50 Percent Gray, White, and Content-Aware (Affinity's inpainting) through `D03 T13 §3`, listed disabled with "Planned: D03 T13 §3" until that section ships; blending mode, opacity, preserve transparency; one "Fill" step.
  - Default fills (Affinity and Photoshop, IP-0860): Alt+Backspace foreground, Ctrl+Backspace background, Shift+Backspace the dialog, Shift adds preserve transparency.
  - Matte (Affinity, IP-0847): fill transparent areas with a color behind existing pixels.
  - Scripted patterns (IP-0854): Brick Fill, Cross Weave, Random Fill, Spiral, Symmetry Fill, and Frame as seeded native generators in `Painting/Fill/ScriptedPatterns/` (scripting itself is backlog B-041); Place Along Path waits on `D03 T16 §5` and is listed disabled with that section named.
  - Paint bucket (IP-0848, IP-0851, IP-0859): source foreground, background, or pattern, mode and opacity, anti-alias, tolerance, contiguous, all layers or chosen source layers (`D03 T10 §3` `SampleSource`), Fill Whole Selection, Fill Similar Colors, on the `D03 T10 §3` `FloodSelector`.
  - Line-art fill (GIMP, IP-0852): line art detection by threshold with the source layer choice, maximum gap length, automatic closure by splines and segments, and fill borders, after Fourey et al. 2018 as in GIMP; budget: detection on a 24-megapixel line drawing under 1.5 seconds, cached until the source changes.
  - Stroke Selection (Photoshop, IP-0850, IP-0855): width, color, location inside, center, outside, blending, opacity, preserve transparency, through `D03 T10 §8` border morphology.
  - Stroke with a line style (GIMP, IP-0856): width, cap, join, miter limit, dash pattern with presets, antialiasing, rendering the selection boundary contour through SkiaSharp's stroker into the target tiles.
  - Stroke with a paint tool (GIMP, IP-0857): the boundary contour as a synthetic stroke through any §5 tool with Emulate Brush Dynamics (pressure ramps in and out).
  - Fill Selection Outline and fill paths (GIMP, IP-0858): selection now; fill path and stroke path become available when `D03 T16 §5` registers paths.
  - One Information line per fill and stroke; undo "Fill", "Bucket Fill", "Stroke Selection".
  - Tests: `FillDialogTests` (each content, preserve transparency), `LineArtFillTests` (a gap of 5 px closes at maximum gap 6 and not at 4; golden against GIMP 3.2.6 on `tests/fixtures/gesso/fill/lineart/` within 1/255), `StrokeSelectionTests` (location inside keeps every stroked pixel inside the mask).
  - Commit: `"gesso: the Fill and Stroke dialogs, scripted patterns, bucket extensions, and line-art fill"`
- **Proof:** Format fidelity against GIMP 3.2.6 plus unit tests: the line-art fill golden matches within 1/255 and `StrokeSelectionTests` pass; cheaper substitute that fails: a tolerance flood on line art, which leaks through the 5 px gap and fails the gap test.

#### §9. Gradients and the gradient editor

- **Deliverable:** The gradient tool with every shape, interpolation, and option, on-canvas stop editing, live gradient fill layers and gradients on masks and adjustment layers, the Photoshop and GIMP gradient editors with noise gradients, diffusion gradients, the transparency tool, bitmap fills, a Gradients panel, and GGR, SVG, GRD, CSS, and POV-Ray exchange, all on the suite gradient model.
- **Depends On:** D03 T03 §8
- **Phase:** 19
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the tool, new captures to docs/captures/gesso/gradients/ (on-canvas stops, editor, segment editor, noise gradient, diffusion fill, Gradients panel). Job: a user can build any gradient any of the three apps can, edit it on the canvas, and keep it live. Treatment: a gradient line with draggable stops and midpoints, a gradient editor dialog with color and opacity stops, smoothness, and GIMP's segment operations, and a Gradients panel. Cheaper substitute that fails: a two-stop linear and radial tool. Chrome: consume the `Isotone.Core` gradient model moved by `D03 T09 §8`, `D01 T03 §3` dithers, and the fill-layer contract of `D03 T08 §1`; do not keep a second sampler in Gesso.
- **Runs:** `Requires: display-session -- on-canvas editing and the editor need an interactive desktop`
- **Catalog:** IP-0861 to IP-0881 (21 features)
- **Hints:**
  - Extend `GradientDefinition` in `src/Isotone.Core/Paint/Gradients/` (moved by `D03 T09 §8`) with GIMP's segment model: `GradientSegment { Left, Middle, Right, LeftColor, RightColor, EndpointColorType (Fixed, Foreground, ForegroundTransparent, Background, BackgroundTransparent), Blending (Linear, Curved, Sinusoidal, SphericalIncreasing, SphericalDecreasing, Step), Coloring (Rgb, HsvCcw, HsvCw) }`; Stilus's stops map to linear segments, so Stilus's gradient tests stay green.
  - Interpolation and blend color space (IP-0869): Perceptual, Linear, Classic, Smooth, Stripes (Photoshop) and GIMP's perceptual RGB, linear RGB, and CIE Lab.
  - Shapes (IP-0868): linear, radial, angle, reflected, diamond, bi-linear, square, shaped (angular, spherical, dimpled from the selection's distance transform), conical symmetric and asymmetric, spiral clockwise and counterclockwise.
  - Options (IP-0870, IP-0881): reverse, transparency, mode and opacity, repeat none, sawtooth, triangular, truncate, offset, adaptive supersampling (max depth, threshold), dither through `D01 T03 §3` with the preference `Gesso.Gradients.Dither`.
  - On-canvas editing (IP-0861, IP-0871, IP-0879): stops, midpoints, and opacity on the gradient line, GIMP's instant mode and modify active gradient, 15 degree angle constraint, Affinity's rotate, reverse, aspect, and fill or stroke context (stroke applies to shape layers once `D03 T16 §7` ships), on any layer kind.
  - Gradient fill layer (IP-0866, IP-0867): `<gesso:fill kind="gradient" v="1">` with the gradient and geometry as parameters and a rendered PNG fallback, re-editable on canvas, plus live gradients on fill layers, layer masks, and adjustment layer masks.
  - Gradient editor dialog (IP-0874, IP-0876 to IP-0878): Photoshop color and opacity stops, stop types, smoothness, preview, zoom; GIMP endpoint color types, color slots, drag colors, blending functions, coloring type, and segment operations flip, replicate, split at midpoint, split uniformly, delete, recenter midpoint, redistribute, blend endpoint colors and opacity.
  - Noise gradients (Photoshop, IP-0875): roughness, color model RGB, HSB, Lab, restrict colors, add transparency, randomize with a stored seed.
  - Diffusion gradient fill (Affinity, IP-0862): colors at control points diffused by a multigrid Laplace solve (after Orzan et al. 2008) with progress and Cancel; budget: 4,000 by 4,000 under 2 seconds.
  - Transparency tool (Affinity, IP-0863): a transparency gradient on the layer's opacity with its own editor, written as a live gradient mask.
  - Bitmap fill (Affinity, IP-0880): fill type Bitmap with extend none, repeat, reflect, pad, quality, and scale with object, sharing §10's tiled image renderer.
  - Gradients panel (IP-0864, IP-0872): `ResourceLibrary<T>` over `%LOCALAPPDATA%\Rizonesoft\Gesso\Gradients\` (where `D03 T11 §10` writes palette gradients) with groups, import, export, legacy sets, picker, save preset, tags, grid and list, new, duplicate, delete, refresh, copy location.
  - Files (IP-0865, IP-0873): GIMP GGR read and write, SVG `<linearGradient>` and `<radialGradient>` load, Photoshop GRD import (descriptor structure; GIMP 3.2.6's GRD loader as oracle), export as CSS and POV-Ray.
  - Tests: goldens against GIMP 3.2.6's gradient tool for every shape and repeat mode and each segment blending function in `tests/fixtures/gesso/gradients/` within 1/255, `GgrRoundTripTests`, `GrdImportTests`, `NoiseGradientDeterminismTests`.
  - Commit: `"gesso: gradient shapes, the gradient editors, live gradient fills, and gradient files"`
- **Proof:** Format fidelity against GIMP 3.2.6: every shape, repeat mode, and blending-function golden matches within 1/255 and GGR files round-trip byte-equal; cheaper substitute that fails: sampling stops linearly in sRGB only, which the perceptual and GIMP spherical-blending goldens reject.

#### §10. Patterns

- **Deliverable:** A pattern library and Patterns panel, Define Pattern and clipboard patterns, Photoshop and GIMP PAT and CAD hatch import, image files as patterns, pattern fill layers and tiled bitmap fills, Affinity's pattern layer with live tile painting, pattern preview, and the pattern stamp.
- **Depends On:** §8
- **Phase:** 19
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/patterns/ (Patterns panel, pattern layer tile painting, pattern preview, pattern stamp). Job: a user can collect patterns from any source, fill with them live, and design seamless tiles by painting across edges. Treatment: a Patterns panel, a pattern fill layer with scale and angle, Affinity's pattern layer, and View, Pattern Preview. Cheaper substitute that fails: a fill that stamps a pattern once as pixels. Chrome: consume §3's `ResourceLibrary<T>`, `D03 T09 §8`'s `IPatternLibrary`, §8's fill paths, and the `D03 T08 §1` contract; do not add a second resource store.
- **Runs:** `Requires: display-session -- the panel, tile painting, and pattern preview need an interactive desktop`
- **Catalog:** IP-0882 to IP-0896 (15 features)
- **Hints:**
  - `PatternLibrary` implementing `D03 T09 §8`'s `IPatternLibrary` on `ResourceLibrary<PatternResource>` over `%LOCALAPPDATA%\Rizonesoft\Gesso\Patterns\`, replacing that interface's first implementation; Patterns panel and GIMP dialog (IP-0883, IP-0892, IP-0896): groups, import, export, legacy sets, grid and list, tags, duplicate, delete, refresh, open as image, copy location, show in folder.
  - Define Pattern from the selection or document (IP-0885); Paste as New Pattern and the clipboard pattern (GIMP, IP-0886, IP-0894).
  - Readers in `src/Gesso/Isotone.Gesso.FileFormats/Patterns/`, detected by content: Photoshop PAT (`8BPT` header and pattern blocks per Adobe's specification, psd-tools as oracle, IP-0888), GIMP PAT (`GPAT` per `devel-docs/pat.txt`) plus PNG, JPEG, BMP, GIF, and TIFF as patterns (IP-0893), and CAD hatch `.pat` definitions (angle, origin, offset, dashes) rasterized into a tile at a chosen scale and line color (Affinity imports these as swatches, Gesso as patterns, IP-0889).
  - Pattern fill layer (Photoshop, IP-0890): `<gesso:fill kind="pattern" v="1">` with pattern id (the tile embedded under `data/patterns/`), scale, angle, link with layer, snap to origin; tiled bitmap fill (Affinity, IP-0882) is the same renderer with Affinity's mapping options.
  - Pattern layer (Affinity, IP-0891): tile from selection, live tile painting where strokes wrap across tile edges, mirror, tile transform, open the tile as a document, written as `<gesso:pattern-layer>`.
  - Pattern Preview (Photoshop, IP-0884, IP-0887): View, Pattern Preview shows the document tiled 3 by 3 and wraps painting across the canvas edges, `Gesso.View.PatternPreview`.
  - Pattern Stamp tool (Photoshop, IP-0895): Aligned and Impressionist (seeded jittered sampling), on §5's options.
  - One Information line per library change and fill; undo "Define Pattern", "New Pattern Fill Layer", "Pattern Stamp".
  - Tests: `PatReaderTests` (Photoshop PAT fixtures authored by the operator in Photoshop 27.10 from Gesso tiles, GIMP PAT fixtures from GIMP 3.2.6, both under CC0), `HatchPatternTests` (a 45 degree hatch at spacing 10 matches its analytic golden), `TileWrapPaintingTests` (a stroke crossing the right edge appears on the left).
  - Commit: `"gesso: patterns, pattern fill and pattern layers, pattern preview, and the pattern stamp"`
- **Proof:** Format fidelity: Photoshop PAT fixtures decode byte-equal to psd-tools' decoded tiles and GIMP PAT fixtures to GIMP 3.2.6's, and `TileWrapPaintingTests` pass; cheaper substitute that fails: filling with a pattern baked into pixels, which the live `gesso:fill` reopen assertion catches.

#### §11. Symmetry painting

- **Deliverable:** Symmetry painting with every competitor's mode (vertical, horizontal, dual axis, diagonal, wavy, circle, spiral, parallel lines, radial, mandala, central mirror, tiling, and path), axis count, mirror, and lockable center, shared by paint and retouch brushes.
- **Depends On:** §5
- **Phase:** 19
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/symmetry/ (each mode's guide overlay, a mandala stroke). Job: a painter can paint mirrored, radial, and tiled designs in one stroke. Treatment: a symmetry menu on the options bar, on-canvas axis guides with a draggable, lockable center, and show or hide. Cheaper substitute that fails: mirroring the finished stroke as a layer copy. Chrome: consume §5's paint pipeline and the overlay; retouch tools of `D03 T13` read the same `SymmetryModel`.
- **Runs:** `Requires: display-session -- symmetric strokes and guides need an interactive desktop`
- **Catalog:** IP-0832 to IP-0837 (6 features)
- **Hints:**
  - `SymmetryModel` in `Painting/Symmetry/` producing per-dab transforms: vertical, horizontal, dual axis, diagonal, wavy (sine displacement), circle, spiral, parallel lines, central mirror, show or hide guides (IP-0832).
  - Radial and mandala (IP-0833, IP-0837): segment count 2 to 32, mirror within segments, kaleidoscope, lockable center (Photoshop and Affinity axis count, mirror, lock).
  - Tiling (GIMP, IP-0835): interval X and Y, shift, max strokes X and Y.
  - Symmetry from a custom path (Photoshop, IP-0834): the path source lists work paths once `D03 T16 §5` registers them, with path transform; until then the option is disabled with that section named.
  - Retouch brushes (Affinity, IP-0836): symmetry, mirror, and lock center on every `D03 T13` brush-based tool through the same model.
  - Persistence: `<gesso:symmetry mode="mandala" count="12" mirror="true" cx="..." cy="..." locked="true"/>` in the document metadata; the setting survives reopen.
  - Budget: a 32-way mandala with a 200 px brush keeps 0 B per dab and handles each input event under 16 ms; one Information line per symmetric stroke (the stroke line plus mode).
  - Tests: `SymmetryModelTests` (every mode maps a point to the analytic set, mirror parity, tiling counts), `SymmetryStrokeGoldenTests` replaying a recorded stroke per mode within 1/255.
  - Commit: `"gesso: symmetry painting"`
- **Proof:** Unit test: `SymmetryModelTests` and `SymmetryStrokeGoldenTests` pass and the 32-way budget test quotes its time and 0 B per dab; cheaper substitute that fails: mirroring the stroke after it ends, which the live-stroke golden (dabs interleaved per input sample) rejects.

#### Sizing concerns

- §3 carries 22 catalog features across five file formats, three panels, and tool presets; it lands near 28 checklist items, and the natural split is GIMP brush formats plus dynamics and tool presets (IP-0778 to IP-0786) as a follow-on section.
- §5 carries 22 features but most share `PaintToolOptions`; it should hold near 24 items, with the history and art history brushes (IP-0792, IP-0807, IP-0808) the natural split if it overruns.
- §9 carries 21 features and 15 hint items, several of which expand to three checklist items (segment editor, files); the natural split is the gradient editor and files (IP-0864, IP-0865, IP-0872 to IP-0878) against the tool and fill layers.
- §1 carries 19 features over five tip types and the input pipeline; the tip types expand to five items, so it lands near 26.

### todo/01-core/TODO-06-isotone-imaging-extensions.md -- `isotone-imaging-extensions`

- **Title:** "TODO-06 -- Isotone.Core Pixel Engine Extensions: the Filters Gesso Adds for Photoshop, Affinity, and GIMP Parity"
- **Phase(s):** 21, 22
- **Goal:** `src/Isotone.Core/Imaging/` grows every filter algorithm that Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6 ship and the `D01 T03` engine lacks, as effects in the same `EffectRegistry`, behind the same `IPixelEffect` contract, and proven through the same golden harness: a 32-bit float processing contract with linear or perceptual space per effect, GEGL abyss policies, a GEGL op-id map, and on-canvas control descriptors (§1); blur, lens blur and blur-gallery kernels, sharpening and deconvolution, denoise and noise (§2 to §5); distort, projection, map, pixelate, and halftone effects (§6, §7, §14); light and shadow, procedural noise, patterns and fractals, edges and stylize, artistic, and generic morphology and channel math (§8 to §13). Gesso is its first consumer (the Filter menu `D03 T14 §2` and the surfaces `D03 T14 §3` to `§10`), Stilus's effect gallery (`D02 T12 §2`) lists every new effect through the shared registry with no Stilus change, and the develop engine (`D01 T07`) and Gesso AI fallbacks (`D03 T19 §8`, `§14`) consume the kernels later. Nothing in it references WPF, a SkiaSharp view, a Gesso type, or a Stilus type; no dialog lives here; no third-party texture, preset, or image is bundled; every effect is deterministic for a seed, cancellable at tile granularity, logs through the `D01 T03 §1` line, and is proven by a GIMP 3.2.6 or GEGL golden, a libvips or ImageMagick golden, or a committed snapshot golden plus the §1 property suite.
- **Current-state facts to verify (with claim candidates):**
  - There is no `Isotone.Core` project yet, so the `D01 T03` engine this file extends exists only as a plan; every hint below names `D01 T03` types as they will exist when Phase 9 ships. `<!-- claim: absent src/Isotone.Core -->`
  - Gesso's Filter menu holds only three submenus today (Blur, Sharpen, Noise). `<!-- claim: count "Header="_(Blur|Sharpen|Noise)"" src/Gesso/src/Gesso.UI/Views/MainWindow.xaml = 3 -->`
  - Gesso's only filter contract processes 8-bit bytes, so no float processing path exists anywhere in the suite. `<!-- claim: count "void Apply\(Span<byte> imageData" src/Gesso/src/Gesso.Plugins.Abstractions/IFilterPlugin.cs = 1 -->`
  - Gesso already models 32-bit float documents, which the §1 float contract serves. `<!-- claim: count "Bpc32 = 32" src/Gesso/src/Gesso.Core/Documents/BitDepth.cs = 1 -->`
  - No GEGL operation id appears in any source file, so the §1 map is new. `<!-- claim: count "gegl:" src/**/*.cs = 0 -->`
  - Gesso's filter parameter types have no point or curve type, so no filter can describe an on-canvas control today. `<!-- claim: count "Point|Curve" src/Gesso/src/Gesso.Plugins.Abstractions/IFilterPlugin.cs = 0 -->`
- **Inputs and XREFs:** `standards/shared.md` and `standards/gesso.md` (float path, SIMD with a scalar reference, zero allocations per tile, determinism); `docs/parity/gesso-parity.md` (the rows each section owns); GIMP 3.2.6 and the GEGL it bundles (version read from `gegl --info` and recorded in each fixture's `reference.txt`, goldens made with `gegl input.png -o expected.png -- gegl:<op> <props>` or `gimp-console-3.2 -i --batch-interpreter=python-fu-eval`), libvips 8.16, and ImageMagick 7.1 as golden reference implementations, each version recorded beside its fixture; GEGL operation reference (`https://gegl.org/operations/`) for op ids and property names; papers named per hint (Tomasi and Manduchi 1998, Gastal and Oliveira 2011, Buades et al. 2005, Yu and Sapiro 2011, Cho and Lee 2009, Krishnan and Fergus 2009, Burt and Adelson 1983, Perlin 2002, Worley 1996, Draves and Reckase 2003, Cabral and Leedom 1993, Achanta et al. 2012, Machairas et al. 2015, Felzenszwalb and Huttenlocher 2012, Schaefer et al. 2006); -> XREF: D01 T03 §1 (the contract, registry, `EffectDescription`, `TileRunner`, and golden harness this file extends, never duplicates); -> XREF: D01 T03 §2 (the `Resampler`, `InverseMapper`, `PerspectiveCorrector`, and `LensCorrector` the distort and lens kernels sample through); -> XREF: D01 T03 §3 (the dither and screen kernels §14 extends); -> XREF: D01 T03 §6 (Gaussian, motion, radial, zoom, rank filters, smart blur, unsharp, and noise that §2, §4, §5 extend); -> XREF: D01 T03 §7 (`InverseMapEffect`, `Displace`, `MeshWarp`, `Pixelate`, `Offset`, `Emboss`, `DiffuseGlow` that §6, §7, §8, §11, §13, §14 extend); -> XREF: D01 T03 §8 (`StrokeField` and `StrokeRenderer` §11 and §12 reuse); -> XREF: D01 T03 §10 (`ReliefLighting`, `CellPartition`, `Vignette` §8, §9, §14 reuse); -> XREF: D01 T03 §11 (`LightingEffects`, `LensFlare`, `BumpMap`, `Mezzotint`, `ColorHalftone`, edge kernels, `UserDefinedConvolution`, `Diffuse` extended here); -> XREF: D01 T02 §2 (settings store for `Isotone.Imaging.*` keys); -> XREF: D01 T04 §1 (transfer curves the linear processing space converts through) and D01 T04 §3 (Lab and CMYK sources and the halftone GCR and UCR conversion); -> XREF: D02 T12 §2 (Stilus's effect gallery lists the new effects from the registry); -> XREF: D02 T11 §5 (nothing moves from it here; `D03 T13 §6` moves its warp math, which §6's mesh warp filter then reads); -> XREF: D03 T09 §7 and D03 T09 §8 (§8 moves their shadow, glow, stroke, and bevel kernels into `Isotone.Core` as their second consumer and registers `gegl:styles` over them); -> XREF: D03 T12 §9 (§13 moves its gradient evaluator into `Isotone.Core` for the gradient render ops); -> XREF: D03 T13 §4 (§4 enables the Sharpen tool's Clarity mode); -> XREF: D03 T13 §6 (the extended `MeshWarp` §6 registers as a filter); -> XREF: D03 T13 §7 (§6 moves its MLS deformer into `Isotone.Core` for the Deform filter); -> XREF: D03 T14 §1 (live filters and the filter brush run these effects); -> XREF: D03 T14 §2 (the Filter menu and generated dialogs, first consumer of §1's traits and on-canvas descriptors); -> XREF: D03 T14 §3, D03 T14 §4, D03 T14 §5, D03 T14 §6, D03 T14 §8, D03 T14 §10 (the surfaces over §3, §5, §6, §8, §9, §13); -> XREF: D03 T16 §5 (the Gesso command that feeds the active path into §9's flame renderer); -> XREF: D03 T17 §4 and D03 T17 §14 (XCF read and write translate GIMP 3 layer filters through §1's `GeglOpMap`); -> XREF: D03 T19 §8 and D03 T19 §14 (AI fallbacks and depth blur run §4, §5, and §3 kernels); -> XREF: D01 T07 §2 and D01 T07 §3 (the develop engine consumes §4 clarity and texture, §5 denoise, and §6 lens models instead of building its own).
- **Adjacency:** list=not-applicable (an engine has no browsable records; the registry is listed by the Gesso Filter menu D03 T14 §2, the GEGL browser D03 T14 §8, and Stilus's gallery D02 T12 §2); document=not-applicable (no printed output of its own); settings=applicable @ D01 T02 §2 (`Isotone.Imaging.ProcessingSpace` and the §1 defaults); reporting=applicable (per-effect timing in the log and the §1 availability reasons the consumers display); notifications=applicable @ D01 T03 §1 (progress and cancellation through `IProgress<EffectProgress>` and `CancellationToken`, shown by the consumers); permissions=not-applicable (the engine reads and writes no files; maps, lens profiles, kernels, and saved designs arrive as buffers or data from the app); audit=applicable @ D01 T03 §1 (the one Information line per `Apply`, extended with space and depth); exchange=applicable (§1's `GeglOpMap` is the interchange vocabulary for XCF layer filters, and effect descriptions serialize to JSON for the `gesso:` filter elements and presets); reverse=not-applicable (effects are pure functions from buffer to buffer; undo belongs to the consumers' history, D01 T02 §4)

#### §1. The extensions contract: float processing, abyss policies, GEGL op ids, and on-canvas controls

- **Deliverable:** Every registered effect, old and new, runs on premultiplied 32-bit float tiles in its declared linear or perceptual space, reports its availability per color mode and depth, honors a GEGL abyss policy and a clip-or-adjust bounds policy, carries its GEGL op id, and describes its on-canvas controls, all as additions to the `D01 T03 §1` contract.
- **Depends On:** D01 T03 §11
- **Phase:** 21
- **Surface:** no surface of its own (the generated dialogs and on-canvas overlay that read these descriptors are D03 T14 §2)
- **Runs:** none
- **Catalog:** IP-0997 (1 features)
- **Hints:**
  - Extend, never fork: add `src/Isotone.Core/Imaging/Effects/EffectTraitsAttribute.cs` (`ProcessingSpace { Perceptual, Linear }`, `SupportedDepths`, `RequiresAlpha`, `GeglOpId`, `GalleryGroup`, `DefaultClip`) read by the `D01 T03 §1` `EffectRegistry`; an effect without the attribute gets documented defaults, so every `D01 T03` effect keeps compiling and gains the traits in one pass over its folder.
  - `src/Isotone.Core/Imaging/Effects/FloatPipeline.cs`: converts `Rgba8` and `Rgba16` tiles to premultiplied `RgbaF`, linearizes through the `D01 T04 §1` transfer curve when the effect is `Linear` (encoded otherwise), runs the effect through `TileRunner`, and converts back with documented round-half-even; setting `Isotone.Imaging.ProcessingSpace` (`PerEffect` default, `AlwaysLinear`, `AlwaysPerceptual`, the Affinity and GIMP toggle) consumed here.
  - Regression: every `D01 T03` effect run through `FloatPipeline` on its 8-bit fixture matches its existing golden within 1 of 255, so the float path changes no shipped result.
  - IP-0997 availability: `EffectAvailability.For(ColorMode, BitDepth)` returns available for RGB, grayscale, Lab, and CMYK at 8, 16, and 32 bits (Lab and CMYK through the `D01 T04 §3` adapter) and unavailable with the reason "Filters need RGB or Grayscale; convert the indexed or bitmap image first" for indexed and bitmap modes; Gesso is broader than Photoshop's per-filter 8-bit limits because every effect runs in float, and the catalog note says so.
  - `AbyssPolicy { None, Clamp, Loop, Black, White }` in `Imaging/Geometry/AbyssPolicy.cs` mapped onto the `D01 T03 §2` `InverseMapper` edge modes (None to transparent, Clamp to clamp, Loop to wrap, Black and White to color constants); `InverseMapEffect` adds the `abyss` parameter to every subclass schema once, in the base class.
  - `ClipPolicy { Adjust, Clip }` (GIMP's Clipping option) resolved by `EffectOutputBounds.Resolve(inputRect, effect, parameters, policy)` from the `D01 T03 §1` `ExpandBounds`: Adjust grows the output, Clip crops to the input.
  - `src/Isotone.Core/Imaging/Effects/Gegl/GeglOpMap.cs`: bidirectional map between GEGL op ids and property names and registry ids and schema parameter names, with unit conversions (for example `gegl:gaussian-blur std-dev-x` to radius); a table test asserts every registry effect with a GEGL counterpart is mapped and every mapped property exists in both schemas; unmapped GEGL ops return `GeglOpMap.Unsupported(id)` so XCF read (`D03 T17 §4`) can name them.
  - Schema additions to `EffectParameterSchema`: `PointList`, `Matrix` (up to 7 by 7), `GradientStops`, `Polyline`, `Expression` (text validated by §9's compiler), and `AuxBuffer` slots for GEGL aux inputs, each with JSON round-trip in `EffectDescription`.
  - `src/Isotone.Core/Imaging/Effects/OnCanvas/OnCanvasControl.cs` descriptors bound to parameter names and validated against the schema: `PointHandle`, `RadiusRing`, `AngleDial`, `LineSegment`, `EllipseFrame` (center, radii, rotation, feather), `PinSet`, `QuadFrame`, and `StrengthDrag` (parameter, pixels per unit, `AllowBeyondMax` for Affinity's drag past the slider maximum, IP-1022).
  - `IMultiOutputEffect` (an effect that returns named buffers, such as wavelet decompose) so the consumer builds layers; no layer type is referenced here.
  - Logging: add `Space` and `Depth` properties to the `D01 T03 §1` `Applied {EffectId}` line instead of writing a second line.
  - Decision row in `docs/dev/decisions.md`: "Gesso's filters run in premultiplied 32-bit float in `Isotone.Core`, named by GEGL op ids for interchange", with GIMP 3.2.6 and its GEGL recorded as the golden oracle.
  - Tests in `tests/Isotone.Core.Tests/Imaging/Extensions/`: `FloatPipelineTests`, `EffectAvailabilityTests`, `AbyssPolicyTests` (each policy on a one-pixel shift of an edge fixture), `ClipPolicyTests`, `GeglOpMapTests`, `OnCanvasControlTests`, `SchemaExtensionRoundTripTests`.
  - Commit: `"core: float processing, abyss policies, GEGL op ids, and on-canvas descriptors"`
- **Proof:** Format fidelity proof and unit test: a 16-bit fixture through `FloatPipeline` Gaussian matches a GIMP 3.2.6 GEGL `gegl:gaussian-blur` golden within 4 of 65,535, the 8-bit regression over every `D01 T03` golden passes, and `GeglOpMapTests` round-trip op properties through a description and back; cheaper substitute that fails: running every effect in 8-bit and widening the result, which the 16-bit fixture's distinct-level count and the GEGL golden reject.

#### §2. Blur extensions

- **Deliverable:** Median with shapes and percentiles, average, blur and blur more, shape blur, bilateral, selective Gaussian, mean curvature, domain transform smoothing, variable blur by mask, tileable blur, circular and zoom motion options, custom blur, circular maximum and minimum, and diffuse extensions, registered and golden-tested.
- **Depends On:** §1, D01 T03 §6
- **Phase:** 21
- **Surface:** no surface of its own (menus and generated dialogs are D03 T14 §2; on-canvas centers are D03 T14 §2's overlay)
- **Runs:** none
- **Catalog:** IP-1035 to IP-1052 (18 features)
- **Hints:**
  - Extend the `D01 T03 §6` classes in `src/Isotone.Core/Imaging/Effects/Blur/` (Gaussian, motion, radial, zoom, rank filters, smart blur) with new parameters; a new class exists only for a new kernel.
  - Rank family: `Median` gains neighborhood shape (square, circle, diamond, horizontal, vertical), percentile, alpha percentile, and high precision (float histogram bins) on the sliding histogram (IP-1035, `gegl:median-blur`); `Maximum` and `Minimum` gain a circular footprint (IP-1047, IP-1048), the same footprint §13 exposes as Photoshop's preserve roundness.
  - Presets on existing kernels: `Average` (mean of the selection or layer, IP-1036), `Blur` and `BlurMore` (Photoshop's fixed kernels as `UserDefinedConvolution` parameter sets, IP-1037), and `CustomBlur` (matrix, divisor, offset, normalize, IP-1046) on the `D01 T03 §11` convolution.
  - `ShapeBlur` (IP-1038): the kernel is an `AuxBuffer` shape mask supplied by the app (Gesso passes a rasterized custom shape from `D03 T16 §7`); no bundled shape set.
  - Edge-preserving family in `Blur/EdgePreserving/`: `BilateralBlur` (radius, edge preservation; Tomasi and Manduchi 1998; IP-1039, IP-1051 one effect, `gegl:bilateral-filter`), `SelectiveGaussian` (max delta, IP-1040, `gegl:selective-gaussian-blur`), `MeanCurvatureBlur` (iterations, IP-1041, `gegl:mean-curvature-blur`), and `DomainTransformSmooth` (spatial and edge sigma, iterations; Gastal and Oliveira 2011; IP-1052, `gegl:domain-transform`).
  - `VariableBlur` (IP-1042, `gegl:variable-blur`): per-pixel radius from an `AuxBuffer` mask by blending a Gaussian mip stack; this is the primitive §3's lens blur and blur-gallery kernels and `D03 T14 §4` reuse.
  - `TileableBlur` (IP-1043): Gaussian run with `AbyssPolicy.Loop` so the result tiles seamlessly; a test wraps the output and asserts no seam above 1 of 255.
  - Motion options: circular spin (IP-1044, `gegl:motion-blur-circular`: center, angle) and zoom (IP-1045, `gegl:motion-blur-zoom`: center, factor) extend `RadialBlur` and `ZoomBlur` with GEGL parameters and a `PointHandle` for the center.
  - `Diffuse` (`D01 T03 §11`) gains the edge-noise mode (IP-1049) and Affinity's intensity (IP-1050); its normal, darken, lighten, and anisotropic modes are §11's.
  - Goldens from GIMP 3.2.6 GEGL for median, bilateral, selective Gaussian, mean curvature, domain transform, variable blur, circular and zoom motion; snapshot goldens for Photoshop-only presets and shape blur.
  - Budget: bilateral radius 20 and variable blur on 24 megapixels under 2 s and 1.5 s, cancellable within one tile.
  - Commit: `"core: blur extensions"`
- **Proof:** Format fidelity proof: `BlurExtensionTests` match the GIMP 3.2.6 GEGL goldens in `tests/fixtures/imaging/blur-ext/` (max delta 2 of 255, 16-bit fixtures within 8 of 65,535) and the snapshot goldens, with the tileable seam test and budget times quoted; cheaper substitute that fails: a Gaussian relabeled as bilateral, which the hard-edge fixture's edge-preservation assertion rejects.

#### §3. Lens blur, bokeh, and the blur-gallery kernels

- **Deliverable:** Depth-map lens blur with iris shapes and specular highlights, the field, iris, tilt-shift, path, and spin blur kernels with bokeh effects, GIMP's focus blur, and Affinity's depth of field, each declaring its on-canvas controls.
- **Depends On:** §2
- **Phase:** 21
- **Surface:** no surface of its own (the Blur Gallery workspace is D03 T14 §4; focus blur's handles are D03 T14 §2's overlay)
- **Runs:** none
- **Catalog:** IP-1053 to IP-1055 (3 features)
- **Hints:**
  - `src/Isotone.Core/Imaging/Effects/Blur/Lens/LensBlur.cs` (IP-1053): depth `AuxBuffer` (from alpha, a mask, or a channel; an estimated depth from `D03 T19 §14` arrives the same way), focal distance, invert; iris shape (triangle to octagon, blade curvature, rotation) rasterized as a polygon disc kernel; specular highlights (threshold, brightness) boosted in linear light before gathering; noise (amount, uniform or Gaussian, monochromatic) on `CounterRng`.
  - Gathering by depth layers (scatter as gather, sorted near to far, after Potmesil and Chakravarty 1981) so a sharp foreground never bleeds into the background halo; property test on a two-plane fixture.
  - `BokehHighlights` stage shared by every kernel here: light bokeh, bokeh color (saturation of boosted highlights), and light range (low and high), the engine behind `D03 T14 §4`'s Effects panel.
  - Blur-gallery kernels in `Blur/Gallery/`, each producing a radius map fed to §2 `VariableBlur` or `LensBlur`: `FieldBlur` (a `PinSet` of points and blur amounts, radius by inverse-distance weighting), `IrisBlur` (`EllipseFrame` with roundness and feather ring), `TiltShift` (center line, focus and feather bands, distortion, symmetric distortion), `PathBlur` (polylines with speed, taper, centered, end-point blur shapes, rear sync flash, strobe count and strength), and `SpinBlur` (ellipse, angle, strobe, pivot); several kernels combine in one pass as Photoshop does.
  - `FocusBlur` (IP-1054, `gegl:focus-blur`): shape (circle, square, diamond, horizontal, vertical), blur type (Gaussian or lens), radius, focus, midpoint, aspect, rotation, highlights factor, threshold, clip, high quality, with `EllipseFrame` controls; GIMP 3.2.6 golden.
  - `DepthOfField` (IP-1055, Affinity): elliptical and tilt-shift masks with vibrance (the `D01 T03 §5` `Vibrance`) and clarity on the in-focus region; clarity is §4's `Clarity` (same phase: if §4 has not landed, this section builds `DetailBands` in `Sharpen/` and §4 consumes it).
  - Budgets: lens blur radius 50 with a depth map on 24 megapixels under 8 s with progress and cancellation; any gallery kernel at `PreviewScale` 0.25 under 400 ms for the interactive surface.
  - Snapshot goldens for lens, gallery, and depth-of-field kernels (no reference implementation), GEGL golden for focus blur, plus properties: a zero-radius map is the identity, radius is monotone in pin amount, strobe count equals visible copies on a point-light fixture.
  - Commit: `"core: lens blur, bokeh, and the blur-gallery kernels"`
- **Proof:** Format fidelity proof and unit test: `LensBlurTests` and `GalleryKernelTests` match committed snapshots in `tests/fixtures/imaging/lens-blur/`, `FocusBlur` matches its GIMP 3.2.6 golden within 3 of 255, and the no-bleed and identity properties pass; cheaper substitute that fails: a Gaussian weighted by the depth map, which the two-plane no-bleed test and the iris-shape highlight snapshot reject.

#### §4. Sharpen and deconvolution

- **Deliverable:** Clarity, texture, multi-band sharpen, sharpen edges and more, smart sharpen's lens and motion removal with fades, presets, and legacy mode, and shake reduction with blind blur-trace estimation, multiple traces, and saved traces.
- **Depends On:** §1, D01 T03 §6
- **Phase:** 21
- **Surface:** no surface of its own (the Smart Sharpen and Shake Reduction dialogs are drawn by D03 T14 §2's generated dialog frame with its custom-editor slot; see Sizing concerns)
- **Runs:** none
- **Catalog:** IP-1056 to IP-1062 (7 features)
- **Hints:**
  - `src/Isotone.Core/Imaging/Effects/Sharpen/DetailBands.cs`: base layer from §2 `DomainTransformSmooth`, detail as the difference, weighted by a midtone curve; `Clarity` (IP-1056) and `Texture` (IP-1057 and Affinity's Texture filter IP-1059, one effect with two parameter sets on a difference-of-Gaussians mid band) are parameterizations of it; `D01 T07 §2` consumes these rather than building its own.
  - `MultiBandSharpen` (IP-1058): Laplacian pyramid (Burt and Adelson 1983) with a gain per band and a noise floor; reconstruction at unit gains is the identity within 1 of 255.
  - `SharpenEdges` and `SharpenMore` (IP-1060) as named parameter sets on the `D01 T03 §6` `Sharpen`.
  - `src/Isotone.Core/Imaging/Fourier/Fft2D.cs`: own radix-2 plus Bluestein 2-D FFT over float tiles with a scalar reference (decision row: own code, no numeric package); §5's FFT filter reuses it.
  - `SmartSharpen` (IP-1061): remove Gaussian (the `D01 T03 §6` unsharp), lens (disc PSF), or motion (line PSF with angle) by Richardson-Lucy deconvolution with a noise-regularized stop; reduce noise; shadow and highlight fade (amount, tonal width, radius); presets as `EffectDescription` JSON; legacy mode reproducing Photoshop's pre-CC behavior (Gaussian or lens only, no noise reduction); `D03 T07 §3`'s Smart Sharpen menu item routes here, no Gesso-side kernel.
  - `ShakeReduction` (IP-1062): multi-scale blind PSF estimation per region (after Cho and Lee 2009) and non-blind deconvolution with a hyper-Laplacian prior (Krishnan and Fergus 2009); parameters blur trace bounds, source noise (auto, low, medium, high), smoothing, artifact suppression.
  - Trace model (IP-1063): `BlurTrace` (region rectangle, kernel buffer, bounds, enabled) list with multiple traces, a blur-direction trace from a drawn line (length and angle to a line PSF), a detail-loupe request API (`RenderRegion(rect, scale)`), and save and load of traces as a PNG kernel plus JSON; the workspace that edits them is drawn by `D03 T14 §2`.
  - Enable the Clarity mode of Gesso's Sharpen tool, which `D03 T13 §4` ships disabled naming this section, by exposing `Clarity` as a dab-capable effect (`SupportsDab` trait: tile-local, radius bounded).
  - Tests: deconvolving a synthetic known-PSF blur improves PSNR by at least 6 dB for lens and motion modes; shake reduction on a committed synthetic camera-shake fixture recovers the kernel with correlation above 0.8; seed and tile-order determinism.
  - Budget: smart sharpen lens mode on 24 megapixels under 3 s; shake reduction on a 2-megapixel region under 20 s with progress and cancellation.
  - Commit: `"core: clarity, texture, multi-band sharpening, and deconvolution"`
- **Proof:** Unit test with snapshot goldens: `SharpenDeconvolutionTests` report the PSNR gains and kernel correlation, `FftTests` match the scalar DFT within 1e-5, and snapshots in `tests/fixtures/imaging/sharpen-ext/` match; cheaper substitute that fails: unsharp mask relabeled as lens or motion removal, which the known-PSF PSNR test rejects.

#### §5. Noise and denoise extensions

- **Deliverable:** Destripe, despeckle, anisotropic noise reduction, symmetric nearest neighbor, the NL filter modes, DCT and wavelet denoise with decompose, the extended reduce noise, an FFT spectrum filter, and the GEGL noise generators, registered and tested.
- **Depends On:** §1, D01 T03 §6
- **Phase:** 21
- **Surface:** no surface of its own (menus and dialogs are D03 T14 §2; the FFT spectrum dialog is D03 T14 §10; the wavelet denoise brush is the D03 T14 §1 filter brush)
- **Runs:** none
- **Catalog:** IP-1064, IP-1066 to IP-1080 (16 features)
- **Hints:**
  - Denoise family in `src/Isotone.Core/Imaging/Effects/Denoise/`: `Destripe` (width, histogram mode; GIMP `plug-in-destripe`, IP-1064), `Despeckle` (radius, adaptive, recursive, black and white levels; GIMP `plug-in-despeckle`, IP-1067), `NoiseReduction` (iterations; `gegl:noise-reduction`, IP-1068), `SymmetricNearestNeighbor` (radius, pairs; `gegl:snn-mean`, IP-1069), and `NlFilter` (alpha-trimmed mean, optimal estimation, edge enhancement; the pnmnlfilt modes, GIMP `plug-in-nlfilt`, IP-1070).
  - `DenoiseDct` (sigma, patch size; Yu and Sapiro 2011; `gegl:denoise-dct`, IP-1071).
  - `WaveletDenoise` (IP-1072): a trous wavelet transform with luminance and chroma thresholds per scale in YCbCr or RGB (GIMP wavelet-denoise); the brush form of IP-1065 is this effect painted through a mask by the `D03 T14 §1` filter brush, which this section enables with the `SupportsDab` trait.
  - `WaveletDecompose` (IP-1073) as an `IMultiOutputEffect`: N scale buffers plus residual whose sum reproduces the input exactly in float; `D03 T14 §2` turns the outputs into a layer group in Grain Merge mode as GIMP does.
  - `ReduceNoise` extends `D01 T03 §6` `RemoveNoise` (IP-1066): luminance strength (NL-means, Buades et al. 2005, search 21 and patch 7), color strength (chroma bilateral), preserve and sharpen details, per-channel mode, JPEG artifact removal (the `D01 T03 §6` deblocker), and saved settings as `EffectDescription` JSON; Affinity's Denoise luminance, color, and detail sliders map onto it.
  - `FftFilter`: forward §4 `Fft2D`, multiply the spectrum by a painted `AuxBuffer` attenuation mask, inverse; plus `SpectrumImage(buffer)` returning a log-magnitude image, the engine behind `D03 T14 §10`'s FFT denoise.
  - Noise generators in `Effects/Noise/` on `CounterRng`: CIE LCh (IP-1074, `gegl:noise-cie-lch`), HSV (IP-1075, `gegl:noise-hsv`), hurl (IP-1076, `gegl:noise-hurl`), pick (IP-1077, `gegl:noise-pick`), RGB independent, correlated, and Gaussian (IP-1078, `gegl:noise-rgb`), slur (IP-1079, `gegl:noise-slur`), spread (IP-1080, `gegl:noise-spread`); GEGL's own random source is not reproduced, so these are proven by distribution moments and snapshot goldens, stated in each `reference.txt`.
  - Goldens from GIMP 3.2.6 for destripe, despeckle, noise reduction, SNN, NL filter, DCT, and wavelet denoise within 3 of 255.
  - Budgets: NL-means on 12 megapixels under 6 s and DCT denoise under 4 s, cancellable; `D01 T07 §3` and `D03 T19 §8` consume these as their classical denoise.
  - Commit: `"core: denoise, wavelet decompose, FFT filter, and noise generators"`
- **Proof:** Format fidelity proof: `DenoiseTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/denoise/`, `WaveletDecomposeTests` reconstruct exactly, and `NoiseGeneratorTests` pass the moment and determinism properties; cheaper substitute that fails: a median labeled as every denoise mode, which the per-op GIMP goldens reject.

#### §6. Distort and projection extensions

- **Deliverable:** GEGL and Photoshop parameter sets for twirl, pinch, spherize, ripple, polar coordinates, and zigzag; lens distortion and apply lens; the lensfun lens models; affine, deform, mesh warp, kaleidoscope, shift, value propagate, waves, whirl and pinch, curve bend, blinds, glitch, video degradation, little planet, panorama projection, and recursive transform.
- **Depends On:** §1, D01 T03 §7
- **Phase:** 21
- **Surface:** no surface of its own (dialogs are D03 T14 §2; lens correction is D03 T14 §6; the mesh and deform editors are D03 T13 §6 and §7)
- **Runs:** none
- **Catalog:** IP-1107 to IP-1132 (26 features)
- **Hints:**
  - Move first: the MLS deformer `D03 T13 §7` built in `src/Gesso/Isotone.Gesso.Core/Transform/Deform/` moves into `src/Isotone.Core/Imaging/Geometry/Deform/MlsDeformer.cs` as its second consumer (the registry's Deform filter); Gesso's deform tool calls the moved type and `grep` finds one MLS implementation.
  - Parameter extensions on `D01 T03 §7` `InverseMapEffect` subclasses: `Swirl` gains Affinity's twirl radius and origin (IP-1107) and `PinchPunch` gains radius and origin (IP-1108), both proven by snapshot goldens plus the existing ImageMagick 7.1 `-swirl` and `-implode` goldens at the default radius; `Sphere` as spherize with normal, horizontal, vertical modes, angle of view, curvature, radius (IP-1109, `gegl:spherize`), `Ripple` (amount, size, amplitude, period, phase, angle, sine, sawtooth, triangle, tileable; IP-1110, `gegl:ripple`), `PolarCoordinates` (both directions, circle depth, offset angle, map backwards, from top; IP-1111, `gegl:polar-coordinates`), `ZigZag` (amount, ridges, around center, out from center, pond ripples; IP-1112); each origin is a `PointHandle`.
  - `LensDistortion` (main, edge, zoom, x and y shift, brighten; IP-1113, `gegl:lens-distortion`) on the `D01 T03 §2` `LensCorrector` radial model plus the edge term; `ApplyLens` (refraction index, keep surroundings, background; IP-1114, `gegl:apply-lens`).
  - Lens models for `D03 T14 §6` and `D01 T07 §3` in `Imaging/Effects/Lens/`: lensfun distortion (`poly3`, `poly5`, `ptlens`), transverse chromatic aberration (linear and `poly3` per channel), and vignetting (`pa`) as registered effects taking coefficients, so the lens dialog and the develop engine share one implementation.
  - `AffineTransform` (rotation, scale, offset, shear, reflect, abyss; IP-1115, the `gegl:transform` family) on the `D01 T03 §2` resampler.
  - `Deform` filter (anchor points, strength, rigid or similarity constraints; IP-1116) on the moved `MlsDeformer`.
  - `MeshWarpFilter` (IP-1118): registers source and destination modes, node types, and resampling over the `D01 T03 §7` `MeshWarp` that `D03 T13 §6` extended with Bezier nodes; no second mesh implementation.
  - Glitch family (seeded): GEGL-style glitch and Affinity's stackable effect types (row shift, block displacement, channel offset, scanline, pixel sort) (IP-1117, IP-1130 one engine); `Shift` (IP-1120, `gegl:shift`); `VideoDegradation` (IP-1122 and IP-1132 one effect, `gegl:video-degradation` patterns).
  - Pattern warps: `Kaleidoscope` (mirror count, rotations, offsets, trim, zoom, expand; IP-1119, `gegl:mirrors`), `Waves` (IP-1123, `gegl:waves`), `WhirlPinch` (IP-1124, `gegl:whirl-pinch`), `ValuePropagate` (IP-1121, `gegl:value-propagate`), `CurveBend` (upper and lower curves, rotation, smoothing; IP-1125, GIMP `plug-in-curve-bend`), `Blinds` (displacement, segments, orientation, background; IP-1126, GIMP `plug-in-blinds`).
  - Projections: `LittlePlanet` (IP-1127, `gegl:stereographic-projection`), `PanoramaProjection` (pan, tilt, spin, zoom, inverse; IP-1128, `gegl:panorama-projection`, also the engine for `D03 T14 §7` equirectangular live projection), `RecursiveTransform` (IP-1129 and IP-1131 one effect, `gegl:recursive-transform`).
  - Goldens from GIMP 3.2.6 GEGL for every GEGL-named op within 3 of 255, snapshot goldens for Photoshop-only modes, glitch, and Affinity parameter sets, plus identity at zero strength and seed determinism.
  - Commit: `"core: distort, projection, lens model, and deform extensions"`
- **Proof:** Format fidelity proof: `DistortExtensionTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/distort-ext/`, the lens models match lensfun's published coefficient behavior on a synthetic grid (corner error under 0.5 pixel), and `grep -rn "class MlsDeformer" src` prints one path under `src/Isotone.Core/`; cheaper substitute that fails: forward-mapped projections, which leave holes the coverage property catches.

#### §7. Map extensions

- **Deliverable:** GIMP displace modes, map absolute and relative, bump map options, engrave, fractal trace, illusion, paper tile, tile seamless, small tiles, tile to a new size, map warp, tile glass, map object, and sphere designer.
- **Depends On:** §6
- **Phase:** 21
- **Surface:** no surface of its own (dialogs, map-object preview, and the sphere designer editor are hosted by D03 T14 §2)
- **Runs:** none
- **Catalog:** IP-1133 to IP-1149 (17 features)
- **Hints:**
  - `Displace` (`D01 T03 §7`) gains GIMP's cartesian and polar modes, separate X and Y `AuxBuffer` maps, center, and abyss, plus Photoshop's stretch or tile and undefined-area options (IP-1133, `gegl:displace`); Gesso passes the map from a file or the layers beneath.
  - `MapAbsolute` and `MapRelative` (coordinate `AuxBuffer`, scale, sampler, abyss; IP-1134, `gegl:map-absolute`, `gegl:map-relative`) on the `D01 T03 §2` `InverseMapper`.
  - `BumpMap` (`D01 T03 §11`) gains azimuth, elevation, depth, offsets, waterlevel, ambient, compensate, invert, tiled, and linear, spherical, sinusoidal map types (IP-1135, `gegl:bump-map`).
  - One-effect-per-duplicate: `Engrave` (IP-1136 and IP-1146, `gegl:engrave`), `FractalTrace` (Mandelbrot or Julia, IP-1137 and IP-1148, `gegl:fractal-trace`), `Illusion` (IP-1138 and IP-1147, `gegl:illusion`).
  - Tiling family: `PaperTile` (IP-1139, `gegl:tile-paper`), `TileSeamless` (IP-1140, `gegl:tile-seamless`), `SmallTiles` (IP-1142, GIMP `plug-in-small-tiles`), `TileToSize` (IP-1143, GIMP `plug-in-tile`, an output-size-changing effect reporting new bounds through `ExpandBounds`), `TileGlass` (IP-1145, `gegl:tile-glass`; also satisfies §12's IP-1273).
  - `MapWarp` (IP-1144, GIMP `plug-in-warp`): iterations, step size, displacement and magnitude `AuxBuffer` maps, dither, abyss.
  - `src/Isotone.Core/Imaging/Effects/Map/MapObject.cs` (IP-1141, GIMP map object): plane, sphere, box (six face `AuxBuffer` images), cylinder (two cap images), point and directional lights, material (ambient, diffuse, reflectivity, highlight), viewpoint, position, orientation, antialiasing, transparent background, as a ray caster; `WireframePreview()` returns line segments for the dialog's wireframe.
  - `SphereDesigner` (IP-1149): layered textures (solid, checker, marble, lizard, noise, spiral, phong) with scale, turbulence, bump amount, and lighting; designs saved as own JSON through `EffectDescription`, no bundled designs.
  - Goldens from GIMP 3.2.6 for every GEGL or GIMP-named op within 3 of 255; map object against a GIMP 3.2.6 render of the sphere and box fixtures within 4 of 255.
  - Budget: map object sphere at 2,048 pixels square under 2 s with antialiasing.
  - Commit: `"core: map extensions, map object, and sphere designer"`
- **Proof:** Format fidelity proof: `MapExtensionTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/map/` with tolerances quoted and `TileSeamless` passes a wrap-seam property; cheaper substitute that fails: map object as a 2-D spherize, which the box and cylinder goldens reject.

#### §14. Pixelate and halftone extensions

- **Deliverable:** Pixelize shapes, Photoshop's mezzotint types, facet, fragment, pointillize, GIMP mosaic, newsprint halftoning, and Affinity halftone, with color halftone refactored onto the one screen kernel.
- **Depends On:** §1, D01 T03 §3
- **Phase:** 21
- **Surface:** no surface of its own (dialogs are D03 T14 §2)
- **Runs:** none
- **Catalog:** IP-1150 to IP-1158 (9 features)
- **Hints:**
  - `Pixelate` (`D01 T03 §7`) gains square, diamond, round, and triangle shapes, block width and height, offset, size ratio, and background (IP-1150, `gegl:pixelize`).
  - `Mezzotint` (`D01 T03 §11`) gains Photoshop's ten types: fine, medium, grainy, coarse dots; short, medium, long lines; short, medium, long strokes (IP-1151), seeded.
  - Photoshop pixelate trio in `Effects/Pixelate/`: `Facet` (color blocks by local mode, IP-1152), `Fragment` (four offset copies averaged, IP-1153), `Pointillize` (cell size, background color, IP-1154) on the `D01 T03 §10` `CellPartition`.
  - `GimpMosaic` (IP-1155, `gegl:mosaic`): squares, hexagons, octagons, triangles; tile size, height, neatness, color variation, spacing, joints color, light direction, antialiasing, surface; GIMP 3.2.6 golden.
  - `src/Isotone.Core/Imaging/Quantize/ScreenKernel.cs`: one halftone screen (period, angle, spot function line, circle, diamond, square, cross, ellipse, turbulence, anti-alias) extending the `D01 T03 §3` `HalftoneScreen`; `Newsprint` (IP-1156 and IP-1158 one effect, `gegl:newsprint`: white on black, black on white, RGB, CMYK; per-ink pattern, period, angle; black pullout; effects) and Affinity `Halftone` (IP-1157: screen type, dot shape, cell size, angle, GCR and UCR through the `D01 T04 §3` CMYK conversion) are parameterizations, and `D01 T03 §11` `ColorHalftone` becomes a preset over it (its existing golden must still pass).
  - Goldens: pixelize, mosaic, and newsprint from GIMP 3.2.6 within 2 of 255; snapshots for Photoshop types and Affinity halftone; a property asserts newsprint dot pitch and angle measured from output within 1 percent.
  - Commit: `"core: pixelate and halftone extensions on one screen kernel"`
- **Proof:** Format fidelity proof: `PixelateHalftoneTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/pixelate/` and `halftone/`, the refactored `ColorHalftone` still matches its `D01 T03 §11` golden, and the pitch property passes; cheaper substitute that fails: a second halftone kernel beside `ColorHalftone`, which a `grep` for one `ScreenKernel` in the Verification block and the preserved golden catch.

#### §8. Light and shadow

- **Deliverable:** Bloom, GEGL lens flare and Photoshop lens types, the full lighting effects model with materials, bump and environment maps, and presets, vignette options, diffuse glow options, inner glow, drop, long, and perspective shadow filters, supernova, gradient flare, sparkle, Xach effect, the bevel filter, and GEGL styles over kernels moved from Gesso's layer styles.
- **Depends On:** §1, D01 T03 §10
- **Phase:** 22
- **Surface:** no surface of its own (the lighting and gradient flare surfaces are D03 T14 §5; other dialogs D03 T14 §2)
- **Runs:** none
- **Catalog:** IP-1191 to IP-1211 (21 features)
- **Hints:**
  - Move first: the shadow, glow, stroke, and bevel kernels `D03 T09 §7` and `D03 T09 §8` built for layer styles move from `src/Gesso/Isotone.Gesso.Core/` into `src/Isotone.Core/Imaging/Effects/Light/` as their second consumer (these filters and Stilus's gallery); Gesso's layer-style renderers call the moved types, and a `grep` finds one drop-shadow kernel.
  - `Bloom` (threshold, softness, radius, strength, limit exposure, glow saturation; IP-1191 and IP-1200 one effect, `gegl:bloom`) in linear light.
  - `LensFlare` (`D01 T03 §11`) gains the GEGL op form with position (IP-1192, `gegl:lens-flare`, `PointHandle`) and Photoshop's lens types 50 to 300 mm zoom, 35 mm prime, 105 mm prime, movie prime (IP-1198).
  - `LightingEffects` (`D01 T03 §11`) extended on `ReliefLighting`: point, spot, and infinite lights with color, intensity, hotspot, cone, distance, up to 16 lights, output options (IP-1193); materials ambient, diffuse, specular, gloss, metallic, exposure, colorize (IP-1194); bump map from a channel or image `AuxBuffer` with linear, spherical, sinusoidal, logarithmic curve and height (IP-1195); spherical environment map (IP-1196); presets as `EffectDescription` JSON with Gesso's own built-in looks (a flashlight spot, five lights from above, a blue omni) plus user presets (IP-1197); GIMP 3.2.6 `plug-in-lighting` golden.
  - `Vignette` (`D01 T03 §10`) gains circle, square, diamond, horizontal, vertical shapes, radius, softness, gamma, proportion, squeeze, center, rotation (`gegl:vignette`), and Affinity exposure mode, with an `EllipseFrame` (IP-1199); `DiffuseGlow` (`D01 T03 §7`) gains Affinity radius, intensity, threshold, and opacity (IP-1201).
  - Shadow and glow filters on the moved kernels: `InnerGlow` (IP-1202, `gegl:inner-glow`), `DropShadow` filter (grow shape and radius, blur, color, opacity, allow resizing through `ClipPolicy.Adjust`; IP-1203, `gegl:dropshadow` merged with the legacy script), `LongShadow` (finite, infinite, fading, fading fixed length, fading fixed rate; angle, length, midpoint; composition; IP-1204, `gegl:long-shadow`), `PerspectiveShadow` (angle, horizon distance, length, blur, color, opacity, interpolation; IP-1205) as a projective map.
  - Render ops: `Supernova` (center, radius, spokes, random hue, color, seed; IP-1206, `gegl:supernova`) and `Sparkle` (threshold, flare intensity, spikes, transparency, random hue and saturation, color type, border; IP-1209, GIMP `plug-in-sparkle`).
  - `GradientFlare` (IP-1207, IP-1208, GIMP `plug-in-gflare`): center, radius, rotation, hue rotation, second-flare vector, adaptive supersampling; glow, rays, and second flares with paint modes, `GradientStops`, spikes, shapes, seed; `GradientFlareDefinition` reads and writes GIMP's gflare text format for user imports; Gesso ships one own default flare and no GIMP flare files.
  - `XachEffect` (highlight offset, color, opacity, drop shadow, keep selection as a mask `AuxBuffer`; IP-1210).
  - `Bevel` (chamfer or bump, distance metric, radius, elevation, depth, azimuth, blend; IP-1211, `gegl:bevel`) on the moved bevel kernel and §13's `DistanceTransform` (same phase: if §13 has not landed, this section builds `DistanceTransform` in `Imaging/Morphology/` and §13 registers it).
  - `Styles` (IP-1212, IP-1213): registers `gegl:styles` (color overlay, outline, shadow or glow, bevel, inner glow, image overlay) over the moved kernels, the same filter `D03 T09 §7` exposes as IP-0375, so one implementation serves the Filter menu, layer styles, and XCF.
  - Goldens: bloom, lens flare, vignette, inner glow, drop shadow, long shadow, supernova, bevel, and lighting from GIMP 3.2.6 within 3 of 255; snapshots for Photoshop lens types, gradient flare, sparkle, and Xach effect.
  - Commit: `"core: light and shadow filters on the shared style kernels"`
- **Proof:** Format fidelity proof: `LightShadowTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/light/` with tolerances quoted, the moved kernels still pass `D03 T09 §7` and `§8`'s layer-style goldens, and one-implementation `grep` checks pass; cheaper substitute that fails: a second drop-shadow kernel for the filter, which the one-implementation check and the shared golden catch.

#### §9. Procedural noise and nature

- **Deliverable:** Perlin, simplex, cell, and solid noise with GEGL parameters, clouds and difference clouds, fibers, Voronoi, plasma, lava, flame along a path, tree and picture frame renderers, and the procedural texture function library with a safe expression compiler.
- **Depends On:** §1
- **Phase:** 22
- **Surface:** no surface of its own (the procedural texture editor is D03 T14 §10; dialogs D03 T14 §2)
- **Runs:** none
- **Catalog:** IP-1214 to IP-1230 (17 features)
- **Hints:**
  - `src/Isotone.Core/Imaging/Procedural/` noise primitives matched to GEGL by porting GEGL's hash and gradient tables (GPL-3.0-or-later, compatible; decision row): `PerlinNoise` (alpha, scale, z offset, iterations; octaves, zoom, persistence, blend mode; IP-1214 and IP-1225 one effect, `gegl:perlin-noise`), `SimplexNoise` (scale, iterations, seed; IP-1215 and IP-1226, `gegl:simplex-noise`), `CellNoise` (scale, shape as Minkowski exponent, rank, iterations, palettize; Worley 1996; IP-1216 and IP-1224, `gegl:cell-noise`), `SolidNoise` (size, detail, tileable, turbulent, seed; IP-1217 and IP-1227, `gegl:noise-solid`).
  - `Clouds` (foreground and background colors over `SolidNoise`) and `DifferenceClouds` (seed, detail, tileable, turbulent, size; IP-1221) as difference-blended clouds, Photoshop's Render pair.
  - `Fibers` (variance, strength, randomize; IP-1222), `Voronoi` (cell size, line width; IP-1223, Affinity), `Plasma` (turbulence, seed; IP-1228, `gegl:plasma`), `Lava` (seed, size, roughness, `GradientStops`, separate-layer flag returned to the consumer; IP-1229).
  - Nature renderers, procedural only with no bundled images: `Flame` (flame types, geometry, custom color, quality, advanced shaping along a `Polyline` parameter; IP-1218), `Tree` (species presets as parameter sets, light, leaves, branches, camera tilt, randomize; an L-system; IP-1220), `PictureFrame` (frame style presets, vines, flowers, leaves, advanced; IP-1219); the Gesso command that passes the active path to `Flame` is `D03 T16 §5`, and until then the user draws the polyline on canvas in the dialog.
  - `src/Isotone.Core/Imaging/Procedural/Expressions/ExpressionCompiler.cs` (IP-1230), built first by `D03 T11 §8` in Phase 18 for Apply Image equations and extended here with the noise and procedural functions: parses Affinity-style expressions into `System.Linq.Expressions` delegates over a whitelisted function library (math, range, clamping, geometric, vector, interpolation, stepping, quantize, oscillators, and the noise primitives above); no Roslyn, no reflection over user text, length and depth limits, and errors reported with a character position; this is the engine for `D03 T14 §10` and §13's equations.
  - Determinism: every generator is seed-deterministic and tile-order independent on `CounterRng` or the ported GEGL hash.
  - Goldens: GEGL-named generators from GIMP 3.2.6 within 1 of 255 at the same seed; snapshots for Photoshop, Affinity, and nature renderers.
  - Budget: any noise generator at 4,096 pixels square under 500 ms; a compiled three-line expression over 12 megapixels under 1 s.
  - Tests: `ExpressionCompilerTests` (every library function, rejection of unknown identifiers and over-long input by position), `ProceduralNoiseTests`.
  - Commit: `"core: procedural noise, nature renderers, and the expression compiler"`
- **Proof:** Format fidelity proof: `ProceduralNoiseTests` match the GIMP 3.2.6 GEGL goldens in `tests/fixtures/imaging/procedural/` within 1 of 255 at fixed seeds and `ExpressionCompilerTests` pass; cheaper substitute that fails: a generic value noise for every generator, which the per-op GEGL goldens reject.

#### §10. Patterns and fractals

- **Deliverable:** Checkerboard, grid, linear sinusoid, Bayer matrix, sinus, spiral, maze, diffraction patterns, jigsaw, circuit, line nova, fractal explorer with coloring, IFS, flame fractal, Qbist, CML explorer, and Spyrogimp curves, each exposing the model its dedicated editor needs.
- **Depends On:** §9
- **Phase:** 22
- **Surface:** no surface of its own (dedicated editors for IFS, flame, Qbist, and CML explorer are hosted by D03 T14 §2's custom-editor slot; see Sizing concerns)
- **Runs:** none
- **Catalog:** IP-1231 to IP-1239, IP-1242 to IP-1243, IP-1245, IP-1248 to IP-1249 (14 features)
- **Hints:**
  - Pattern renderers in `src/Isotone.Core/Imaging/Render/Patterns/` with GIMP 3.2.6 GEGL goldens: `Checkerboard` (size, offset, colors, psychobilly; IP-1232, `gegl:checkerboard` merged with the legacy plug-in), `Grid` (spacing, offset, line width, color, intersections; IP-1234), `LinearSinusoid` (IP-1235, `gegl:linear-sinusoid`), `BayerMatrix` (IP-1231, `gegl:bayer-matrix`), `Sinus` (IP-1237, `gegl:sinus`), `Spiral` (type, position, radius, balance, rotation, direction, colors, `PointHandle` and `RadiusRing`; IP-1238, `gegl:spiral`).
  - `Maze` (size, depth-first or Prim, tileable, seed, colors; IP-1236, `gegl:maze`), `Diffraction` (IP-1233, `gegl:diffraction-patterns`), `Jigsaw` (tiles, bevel edges, square or curved; IP-1245, GIMP `plug-in-jigsaw`), `LineNova` (lines, sharpness, offset radius, randomness; IP-1249).
  - `Circuit` (oilify mask, seed, separate layer, keep selection; IP-1248) composes `Maze`, §12's `Oilify` (same phase: build `Oilify` here if §12 has not landed and §12 registers it), and the `D01 T03 §11` edge kernels.
  - `FractalExplorer` (Mandelbrot, Julia, Barnsley 1 to 3, Spider, Man-o-war, Lambda, Sierpinski; bounds, iterations, CX, CY, zoom; number of colors, log smoothing, channel stretch and functions, `GradientStops`; IP-1242, IP-1243, `gegl:fractal-explorer`) with saved fractals as `EffectDescription` JSON.
  - `IfsFractal` (IP-1244, GIMP IFS Compose): affine transform list with color transforms and probability, render options; model API for the editor (add, delete, select, transform by matrix) and read and write of IFS Compose settings files the user imports.
  - `FlameFractal` (IP-1241, Draves and Reckase 2003): variations, brightness, contrast, gamma, density estimation, oversample, colormap from `GradientStops`, zoom, position; open and save flam3 XML.
  - `Qbist` (IP-1246): genome of random texture instructions with anti-aliasing, mutation to nine candidates, open and save of GIMP Qbist files; `CmlExplorer` (IP-1239, IP-1240): coupled map lattice with hue, saturation, and value functions, composition, diffusion, mutation, seeds, open and save of settings, selective load, and `PlotFunction(channel)` sample arrays for the graph.
  - `SpyroCurves` (IP-1247): spirograph, epitrochoid, sine, and Lissajous curves emitted as `Polyline` results; stroking them with the brush engine is Gesso's (`D03 T12 §5`), so the paint-tool command lives outside this engine (see the report's routing note).
  - Goldens: GEGL-named renderers from GIMP 3.2.6 within 1 of 255; snapshots for IFS, flame, Qbist, CML, jigsaw, line nova, circuit; the file formats round-trip committed fixtures.
  - Commit: `"core: patterns and fractals"`
- **Proof:** Format fidelity proof: `PatternFractalTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/patterns/` and the flam3, IFS, Qbist, and CML fixtures round-trip byte-equivalent; cheaper substitute that fails: renderers without their settings files, which the round-trip fixtures reject.

#### §11. Edges and stylize

- **Deliverable:** Emboss and edge-detect algorithm choices, directional Sobel, difference of Gaussians, Laplace, neon, image gradient, Photoshop oil paint, diffuse modes, extrude, and tiles.
- **Depends On:** §1, D01 T03 §11
- **Phase:** 22
- **Surface:** no surface of its own (dialogs are D03 T14 §2)
- **Runs:** none
- **Catalog:** IP-1255 to IP-1266 (12 features)
- **Hints:**
  - `Emboss` (`D01 T03 §7`) gains GIMP's emboss or bumpmap type with azimuth, elevation, depth (IP-1255, `gegl:emboss`) and Affinity's radius, amount, angle, monochrome (IP-1262).
  - `EdgeDetect` (`D01 T03 §11`) gains Sobel, Prewitt, gradient, Roberts, differential, and Laplace with amount and border behavior (IP-1256, `gegl:edge`) on the shared kernels.
  - Edge family in `Effects/Edge/`: `SobelDirectional` (horizontal, vertical, keep sign; IP-1257, `gegl:edge-sobel`), `DifferenceOfGaussians` (IP-1258, `gegl:difference-of-gaussians`), `Laplace` (IP-1259, `gegl:edge-laplace`), `NeonEdges` (radius, intensity; IP-1260, `gegl:edge-neon`), `ImageGradient` (magnitude, direction, both; IP-1261, `gegl:image-gradient`).
  - `OilPaint` (stylization, cleanliness, scale, bristle detail, lighting angle, shine; IP-1263): strokes along the `D01 T03 §8` `StrokeField` by line integral smoothing with bristle texture, shaded by the `D01 T03 §10` `ReliefLighting`; `D03 T07 §3`'s legacy oil paint item routes here.
  - `Diffuse` (`D01 T03 §11`) gains normal, darken only, lighten only, and anisotropic modes (IP-1264).
  - `Extrude` (blocks or pyramids, size, random or level-based depth, solid front faces, mask incomplete blocks; IP-1265) and `Tiles` (number, maximum offset, fill background, foreground, inverse, unaltered; IP-1266), seeded.
  - Goldens from GIMP 3.2.6 for every GEGL-named op within 2 of 255; snapshots for oil paint, extrude, tiles, and Affinity emboss; properties: a flat input yields a flat edge output, oil paint is seed-deterministic.
  - Budget: oil paint on 12 megapixels under 3 s cancellable.
  - Commit: `"core: edge and stylize extensions"`
- **Proof:** Format fidelity proof: `EdgeStylizeTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/edge-ext/` and the snapshots, with the flat-input property passing; cheaper substitute that fails: one Sobel kernel for every algorithm choice, which the per-algorithm GEGL goldens reject.

#### §12. Artistic extensions

- **Deliverable:** Apply canvas, cartoon, cubism, oilify, GIMP photocopy, SLIC, glass tile, waterpixels, GIMPressionist with its orientation and size modes and maps, Van Gogh line integral convolution, clothify, weave, and softglow.
- **Depends On:** §11
- **Phase:** 22
- **Surface:** no surface of its own (GIMPressionist's tabbed dialog and its map editors are hosted by D03 T14 §2's custom-editor slot; see Sizing concerns)
- **Runs:** none
- **Catalog:** IP-1267 to IP-1274, IP-1276, IP-1278 to IP-1284 (16 features)
- **Hints:**
  - GEGL artistic ops in `src/Isotone.Core/Imaging/Effects/Artistic/` with GIMP 3.2.6 goldens: `TexturizeCanvas` (direction, depth; IP-1267, `gegl:texturize-canvas`), `Cartoon` (mask radius, percent black; IP-1268, `gegl:cartoon`), `Cubism` (tile size, saturation, background, seed; IP-1269, `gegl:cubism`), `Oilify` (mask radius, exponent, intensity mode, aux radius and exponent maps; IP-1270, `gegl:oilify`), `Photocopy` (IP-1271, `gegl:photocopy`), `Softglow` (glow radius, brightness, sharpness; IP-1281, `gegl:softglow`).
  - Superpixels: `Slic` (IP-1272, `gegl:slic`, Achanta et al. 2012) and `Waterpixels` (IP-1274, `gegl:waterpixels`, Machairas et al. 2015) on §13's watershed (same phase: build `Watershed` in `Imaging/Morphology/` here if §13 has not landed, and §13 registers it).
  - Glass tile (IP-1273) is the same GIMP filter as §7's `TileGlass`; register the GIMP Artistic menu alias to that effect, no second kernel.
  - `Gimpressionist` (IP-1275, IP-1276, IP-1282) on the `D01 T03 §8` `StrokeRenderer`: paper relief, brush `AuxBuffer` (user-loaded brushes and papers only, none bundled), placement (random or evenly distributed, stroke density, centered), color (average or center, color noise), background (keep, solid, transparent), stroke drop shadow, orientation and size modes (value, radius, random, radial, flowing, hue, adaptive, manual), Voronoi orientation; presets as JSON and a reader for GIMPressionist preset text files the user imports.
  - Orientation and size maps (IP-1277): `VectorField` model (a list of vectors with position, angle, strength, type) and `SizeField`, with evaluation APIs and preview rendering the dialog's editors call.
  - `VanGoghLic` (IP-1278, IP-1283, Cabral and Leedom 1993): effect image channel, filter length, noise magnitude, integration steps, minimum and maximum value, white noise convolve, derivative source.
  - Script-derived textures: `Clothify` (IP-1279, blur, azimuth, elevation, depth) and `Weave` (ribbon width, spacing, shadow darkness, shadow depth, thread length, density, intensity; IP-1280, IP-1284) composed from §5 noise, the `D01 T03 §6` blur, and §7 bump map.
  - Snapshot goldens for GIMPressionist, Van Gogh, clothify, weave; GEGL goldens for the rest within 3 of 255; seed determinism for every stroke effect.
  - Budget: GIMPressionist at default density on 12 megapixels under 5 s; preview at 0.25 under 500 ms.
  - Commit: `"core: artistic extensions"`
- **Proof:** Format fidelity proof: `ArtisticExtensionTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/artistic-ext/` and the snapshots, and a pairwise-distinct test across the new effects passes; cheaper substitute that fails: GIMPressionist with random orientation only, which the flowing and manual orientation snapshots reject.

#### §13. Generic, morphology, and channel math

- **Deliverable:** Convolution matrix, dilate, erode, distance map, normal map, offset, HSB and HSL encoding, color matrix ops, color warp, color assimilation grid, color overlay, Scale3X antialias, temporal blur, alpha and per-pixel math, bevel op, gradient render ops, blend ops, luminance remap, watershed, circular maximum and minimum, and the equations engine.
- **Depends On:** §1
- **Phase:** 22
- **Surface:** no surface of its own (the GEGL operation tool is D03 T14 §8; the equations editor is D03 T14 §10)
- **Runs:** none
- **Catalog:** IP-0656, IP-1285 to IP-1290, IP-1292 to IP-1308 (24 features)
- **Hints:**
  - Move first: the two-stop gradient evaluator `D03 T12 §9` built in `src/Gesso/Isotone.Gesso.Core/Painting/` moves to `src/Isotone.Core/Imaging/Render/GradientEvaluator.cs` as its second consumer for `LinearGradient` and `RadialGradient` (IP-1301, `gegl:linear-gradient`, `gegl:radial-gradient`); Gesso's gradient tool calls the moved type.
  - Morphology in `src/Isotone.Core/Imaging/Morphology/`: `Dilate` and `Erode` (IP-1293, IP-1294), `DistanceTransform` (Euclidean, Manhattan, chessboard; edge handling; thresholds; averaging; normalize; Felzenszwalb and Huttenlocher 2012; IP-1295, `gegl:distance-transform`), `Watershed` (IP-1305, `gegl:watershed-transform`), and Photoshop's preserve squareness or roundness on the §2 rank footprint (IP-1308); register these here even when §8 or §12 built the type first.
  - `ConvolutionMatrix` (5 by 5, divisor, offset, channels, normalize, alpha weighting, border; IP-1292, `gegl:convolution-matrix`) on the `D01 T03 §11` `UserDefinedConvolution`.
  - `NormalMap` (scale, x and y components, flip, full z range; IP-1290 and IP-1296 one effect, `gegl:normal-map`); `Offset` (`D01 T03 §7`) gains GIMP's transparent, repeat edge, and wrap around through `AbyssPolicy` and the half-size shortcut (IP-1306, `gegl:offset`).
  - Color ops: SVG hue rotate, saturate, matrix, luminance to alpha (IP-1285, IP-1304, `gegl:svg-*`), `ColorWarp` (IP-1286, `gegl:color-warp`), `ColorAssimilationGrid` (IP-1287), `ColorOverlay` (IP-1288, `gegl:color-overlay`), `HslEncode` and `HsbEncode` with their decodes (IP-1307).
  - Alpha and math ops: premultiply and unpremultiply (IP-1297), add, subtract, multiply, divide, gamma, absolute with a constant or an `AuxBuffer` (IP-1298), alpha clip and opacity (IP-1299), mix, weighted blend, piecewise blend by mask (IP-1302), and remap by luminance envelopes (IP-1303), one small class each on a shared `PointOp` base so the GEGL tool (`D03 T14 §8`) can run them.
  - `Antialias` (IP-1289, `gegl:antialias`, Scale3X edge extrapolation) and `BevelOp` (IP-1300, the op-level id over §8's `Bevel`, no second kernel).
  - `TemporalBlur` (IP-1291, `gegl:temporal-blur`): a stateful accumulator over a sequence of buffers with frame count and decay; registered as graph-only with no menu home because Gesso has no frame sequences until backlog B-044, stated in its XML documentation.
  - `EquationsEffect` for `D03 T14 §10` (IP-1326, IP-1327 are owned there): cartesian `x'`, `y'` and per-channel expressions with parameters A, B, C, a polar system, and extend modes through `AbyssPolicy`, compiled by §9's `ExpressionCompiler` (same phase: if §9 has not landed, build the compiler here and §9 consumes it).
  - Goldens from GIMP 3.2.6 for every GEGL-named op within 1 of 255 (point ops exact in float); snapshots for Photoshop and Affinity forms.
  - Alien map (IP-0656): RGB or HSL frequencies and phase shifts with keep-component switches, registered for the Colors menu through D03 T14 §2.
  - Commit: `"core: morphology, convolution matrix, channel math, and the equations engine"`
- **Proof:** Format fidelity proof: `GenericOpsTests` match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/generic/` with point ops exact on float fixtures, and `DistanceTransformTests` equal a brute-force distance on 1,000 random masks; cheaper substitute that fails: a 3 by 3 convolution for the 5 by 5 matrix, which the GIMP golden rejects.

#### Sizing concerns

- §6 owns 26 features; with the MLS move and the lens models it is near the cap. Natural split: projections and lens (polar, lens distortion, apply lens, lens models, little planet, panorama, recursive transform) versus deformations and patterns (affine, deform, mesh warp filter, glitch, kaleidoscope, waves, curve bend, blinds, video degradation).
- §8 owns 23 features plus the style-kernel move; if it overflows, split lighting and flares (lighting effects, lens flare, supernova, gradient flare, sparkle, bloom) from shadows and bevels (drop, long, perspective shadow, inner glow, bevel, styles, Xach effect).
- §13 owns 24 small features; if the point-op family exceeds one item, split morphology and convolution from GEGL math and blend ops.
- IP-1063, IP-1240, IP-1241, IP-1244, IP-1246, IP-1275, and IP-1277 carry dedicated editors (shake reduction workspace, CML plot, flame, IFS, Qbist, GIMPressionist tabs and map editors) that a library section cannot build; this file supplies their models and `D03 T14 §2` must carry a custom-editor slot; see the report for a recommended owner.

### todo/03-gesso/TODO-13-gesso-parity-retouch.md -- `gesso-parity-retouch`

- **Title:** "TODO-13 -- Gesso Parity: Retouching, Content-Aware Tools, Transform, Warp, and Liquify"
- **Phase(s):** 20
- **Goal:** Gesso has the full retouching and geometry toolset of Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6: clone stamp with the Clone Source panel, perspective and seamless clone, healing, spot healing, patch, blemish, inpainting, and red eye; a classical content-aware engine (PatchMatch fill workspace, content-aware scale and move, delete and fill, heal selection) in `src/Gesso/Isotone.Gesso.Core/Retouch/` that runs with no network; dodge, burn, sponge, tone, blur, sharpen, and median brushes; Free Transform extensions and the GIMP transform tools; warp and mesh warp, puppet warp, cage and N-point deformation, and perspective warp; Liquify with a GPU path and face-aware controls; and frequency separation. Tools run on the `D03 T03 §4` tool system and the `D03 T12` brush engine, geometry samples through the `D01 T03 §2` resampler and inverse mapper, warp-style math moves out of Stilus rather than being copied, every stroke or apply is one undoable command through the suite history with tile snapshots and one Serilog Information line, warps on smart objects stay re-editable, and generative modes belong to `D03 T19`, never to this file.
- **Current-state facts to verify (with claim candidates):**
  - No retouching, content-aware, warp, or liquify code exists in Gesso. `<!-- claim: count "Heal|Liquify|Warp|PatchMatch|CloneSource" src/Gesso/src/**/*.cs = 0 -->`
  - Gesso has no tool folder or tool abstraction yet; `D03 T03 §4` adds it. `<!-- claim: absent src/Gesso/src/Gesso.Core/Tools -->`
  - The history's command categories already name Transform, but no command uses it. `<!-- claim: count "^    Transform,$" src/Gesso/src/Gesso.Core/History/Commands/CommandBase.cs = 1 -->` `<!-- claim: count "CommandCategory\.(Transform|Filter)" src/Gesso/src/**/*.cs = 0 -->`
  - The Image menu's rotate and flip commands only write a Debug line; `D03 T03 §7` wires them before this file extends them to layers. `<!-- claim: count "_logger\.Debug\(\"(Rotate|Flip) " src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 5 -->`
  - Selection tools are a 328-line model that `D03 T10 §1` replaces; the content-aware sampling area reads the replacement. `<!-- claim: lines src/Gesso/src/Gesso.Core/Selections/SelectionTools.cs = 328 -->`
  - Raster layers tile at 256 pixels, the unit every retouch stroke snapshots. `<!-- claim: count "TileSize = 256" src/Gesso/src/Gesso.Core/Tiles/Tile.cs = 1 -->`
- **Inputs and XREFs:** `standards/gesso.md` (zero allocations per dab, GPU path with CPU parity, tiles); `docs/parity/gesso-parity.md`; GIMP 3.2.6 (heal, clone, perspective clone, seamless clone, warp transform, N-point, cage, unified and 3D transform tools) and its GEGL as behavior and golden references; papers named per hint (Perez, Gangnet, and Blake 2003; Farbman et al. 2009; Barnes et al. 2009 and 2010; Wexler, Shechtman, and Irani 2007; Avidan and Shamir 2007; Rubinstein, Shamir, and Avidan 2008; Telea 2004; Igarashi, Moscovich, and Hughes 2005; Schaefer, McPhail, and Warren 2006; Hormann and Floater 2006; Dvoroznak 2014); the resynthesizer plug-in (GPL-3.0-or-later) as the content-aware reference; -> XREF: D03 T03 §2 (tile-snapshot commands every stroke commits through); -> XREF: D03 T03 §4 (the tool system every tool here derives from); -> XREF: D03 T03 §7 (the free transform and canvas rotate §5 extends); -> XREF: D03 T12 §1 and D03 T12 §5 (brush engine and painting tool base with the shared retouch brush options IP-0751, IP-0809); -> XREF: D03 T12 §8 (the Fill dialog's content-aware option §3 adds); -> XREF: D03 T12 §10 (pattern sources for clone and healing); -> XREF: D03 T12 §11 (symmetry the retouch brushes honor); -> XREF: D03 T10 §1 (the selection model the content-aware engine reads); -> XREF: D03 T09 §9 (smart objects that keep transforms and warps re-editable); -> XREF: D03 T08 §1 (the `gesso:` contract for clone sources and warp parameters); -> XREF: D03 T08 §9 (content-aware crop fill consumes §3); -> XREF: D01 T03 §2 and D01 T03 §7 (resampler, inverse mapper, perspective corrector, and `MeshWarp` §5, §6, §8, §11 extend); -> XREF: D01 T06 §4 (enables the Sharpen tool's Clarity mode shipped disabled in §4); -> XREF: D01 T06 §6 (moves §7's MLS deformer into `Isotone.Core` and registers §6's mesh warp as a filter); -> XREF: D02 T11 §5 (the warp-style and mesh-map math §6 moves to `Isotone.Core/Vector/Warp/`); -> XREF: D03 T14 §1 (live-filter forms of mesh warp, puppet warp, perspective warp, and liquify); -> XREF: D03 T14 §7 (Vanishing Point stamps and heals through §1 and §2); -> XREF: D03 T15 §7 (panorama edge fill consumes §3); -> XREF: D03 T16 §4 (warp text consumes §6's moved warp styles); -> XREF: D03 T16 §5 (the Path transform target §11 enables); -> XREF: D03 T19 §3 (generative remove adds its mode to §2's Remove tool); -> XREF: D03 T19 §9 (distraction removal fills through §3); -> XREF: D03 T19 §11 (face landmarks for §9's face-aware liquify); -> XREF: D03 T20 §1 (the retouching studio preset §10 defines); -> XREF: D03 T20 §3 (the GIMP shortcut set §11's tool shortcuts join); -> XREF: D01 T07 §5 (develop spot removal and red eye consume §2 healing and red-eye detection instead of their own).
- **Adjacency:** list=applicable (Clone Source panel source list, warp and liquify mesh files, content-aware output targets); document=not-applicable (no printed output); settings=applicable (every tool option is a `Gesso.<Tool>.*` key with a default and a consumer, and Preferences pages list them through D03 T20 §4); reporting=applicable (transform HUD values and the Transform panel's numeric readout); notifications=applicable (progress and cancel for content-aware fill, scale, and move, liquify commit, and warp renders in the status strip); permissions=applicable (locked layers and pixels refuse strokes by name, a tool that needs pixels on a text or shape layer offers to rasterize, and a missing clone source document is refused by name); audit=applicable (one Serilog Information line per command with tool, layer, and parameters hash); exchange=applicable (liquify mesh and blur-trace files, clone sources and warp parameters in the `gesso:` namespace, GIMP transform tool parity); reverse=applicable (every stroke and apply is one undo step; the liquify and content-aware workspaces keep their own inner undo and cancel restores the layer)

#### §1. Clone stamp and the clone source panel

- **Deliverable:** A clone stamp with every alignment and sampling option, up to five global clone sources from any open document with offset, scale, rotation, and flip, the Clone Source panel with its overlay, GIMP's perspective clone, and a seamless clone paste on a shared gradient-domain blender. -> SOURCE: legacy-gesso-4.6
- **Depends On:** D03 T12 §5
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/clone-source-panel/ and docs/captures/gesso/clone-stamp/. Job: a retoucher can copy texture from anywhere, including another open document, scaled and rotated, and see where it lands before painting. Treatment: Alt-click sets a source, a live overlay of the source follows the cursor clipped to the brush, the Clone Source panel holds five source slots with offset, W and H, angle, flip, and overlay options. Cheaper substitute that fails: a clone that only offsets within the same layer, which the cross-document and scaled-source tests catch. Chrome: consume the `D03 T12 §5` painting-tool base, brush options bar, and canvas overlay layer; do not build a second brush engine or options bar.
- **Runs:** `Requires: display-session -- clone strokes, the source overlay, and the panel are driven and captured`
- **Catalog:** IP-0900 to IP-0905 (6 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-4.6` (promotes B-017); delete the B-017 line from `todo/backlog.md` in the authoring commit.
  - `src/Gesso/Isotone.Gesso.Core/Tools/Retouch/CloneStampTool.cs` on the `D03 T12 §5` painting-tool base (IP-0900): Alt-click source, aligned, sample current layer, current and below, or all layers, ignore adjustment layers, image or pattern source (`D03 T12 §10`), GIMP alignment none, aligned, registered, fixed; shared retouch brush options (width, opacity, flow, hardness, pressure, stabilizer, wet edges, symmetry) come from `D03 T12 §1`, `§5`, and `§11` unchanged.
  - `src/Gesso/Isotone.Gesso.Core/Retouch/CloneSources.cs` (IP-0901): five `CloneSource` slots (document id, layer, sample point, offset, scale W and H, rotation, flip H and V, source area rectangle for Affinity's define-source-area), resolved through the open-document registry so another document can be the source; a closed source document is refused by name.
  - Clone Source panel `src/Gesso/Isotone.Gesso.Desktop/Panels/CloneSourcePanel.xaml` with `CloneSourcePanelViewModel` (IP-0905, IP-0901): five source buttons, offset, W and H with link, angle, flip, reset transform, frame offset hidden (no video), and overlay options show, opacity, clipped, auto hide, invert, blend mode (IP-0902) drawn by the canvas overlay layer.
  - Source transform math: sample through the `D01 T03 §2` `Resampler` (bicubic) with the source's affine matrix per dab; zero allocations per dab through pooled tile spans.
  - `PerspectiveCloneTool` (IP-0903, GIMP): modify-perspective mode edits a four-corner quad whose `D01 T03 §2` `PerspectiveCorrector` homography maps source to destination; clone mode paints through it.
  - `src/Gesso/Isotone.Gesso.Core/Retouch/Blending/SeamlessBlender.cs`: mean-value-coordinates cloning (Farbman et al. 2009, the method GEGL's `gegl:seamless-clone` uses) with a Poisson multigrid refinement (Perez, Gangnet, and Blake 2003) over float tiles; §2's healing and seamless clone tool reuse it.
  - Edit, Paste Special, Seamless Clone (IP-0904): pastes the clipboard as a floating layer and Poisson-blends it on commit; one undo step "Seamless Clone Paste".
  - Native format: clone sources that refer to this document persist as `<gesso:clone-sources>` in the document block (D03 T08 §1), other-document sources persist only by path and are dropped with a Warning when the path is gone.
  - Undo: one tile-snapshot command per stroke named "Clone Stamp" or "Perspective Clone"; log `Clone stroke on {LayerId} from source {Slot} ({Dabs} dabs)`.
  - Budget: a 300-pixel brush on a 24-megapixel document keeps 60 frames per second with zero allocations per dab (benchmark quoted).
  - Tests: `CloneStampTests` (aligned versus fixed offsets, sample all layers, pattern source), `CloneSourceTests` (cross-document, scaled, rotated, flipped), `SeamlessBlenderTests` against a GIMP 3.2.6 `gegl:seamless-clone` golden within 4 of 255.
  - Commit: `"gesso: clone stamp, clone sources, perspective clone, and seamless clone paste"`
- **Proof:** Unit test and driven run: `CloneSourceTests` prove a scaled, rotated source from a second document lands at the expected pixels, `SeamlessBlenderTests` match the GIMP 3.2.6 golden, and a driven clone stroke plus undo restores the layer hash (quoted with captures); cheaper substitute that fails: an offset-only copy, which the scaled-source test rejects.

#### §2. Healing, patch, blemish, inpainting, and red eye

- **Deliverable:** Healing brush, spot healing (proximity match and create texture), patch tool, blemish removal, classical inpainting and the Remove tool's classical mode, GIMP's seamless clone tool, and red eye as a tool and a filter, all on the §1 blender.
- **Depends On:** §1
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/healing/ and docs/captures/gesso/red-eye/. Job: a retoucher can remove blemishes, dust, and small objects so the repair matches surrounding texture and tone. Treatment: brush tools with the shared retouch options, a patch tool that drags a selection, and a red-eye click tool with pupil size and darken amount. Cheaper substitute that fails: a clone relabeled as healing, which the tone-match test catches. Chrome: consume the `D03 T12 §5` painting-tool base, the §1 blender, and the selection model; no second options bar.
- **Runs:** `Requires: display-session -- healing strokes, patch drags, and red-eye clicks are driven and captured`
- **Catalog:** IP-0906 to IP-0916 (11 features)
- **Hints:**
  - `HealingBrushTool` (IP-0908): sampled or pattern source, aligned, sample layers, diffusion 1 to 7, mode, and Photoshop's legacy algorithm, each dab texture from the source with tone solved by the §1 `SeamlessBlender` over the dab's boundary.
  - `SpotHealingBrushTool` (IP-0909): proximity match (best boundary-matching patch in a search ring) and create texture (synthesized from the stroke's neighborhood); the Content-Aware type is wired by §3 when its engine lands, and the type list shows it disabled naming §3 until then.
  - `PatchTool` (IP-0910): source or destination, transparent, pattern, diffusion, and Affinity's scale and rotation on drop; the content-aware mode (IP-0911: structure, color, sample all layers) is wired by §3.
  - `src/Gesso/Isotone.Gesso.Core/Retouch/Inpaint/FastMarchingInpainter.cs` (Telea 2004, managed; OpenCvSharp stays scoped to `Photo/`): Inpaint command and inpainting brush (IP-0914, rasterizes the target layer with a named confirmation), and the Remove tool's classical mode (IP-0912: brush, circle, remove after each stroke, sample all layers); `D03 T19 §3` adds the generative mode toggle to the same tool and §3 swaps regions above `Gesso.Retouch.InpaintPatchThreshold` (default 64 pixels) to content-aware fill.
  - `BlemishRemovalTool` (IP-0913, Affinity): click or drag a radius; the best patch in a ring is healed in with the blender.
  - `SeamlessCloneTool` and seamless clone compose (IP-0907, IP-0916, GIMP): drag pasted content with live gradient-domain blending on the §1 blender.
  - `src/Gesso/Isotone.Gesso.Core/Retouch/RedEye/RedEyeDetector.cs`: redness `r - max(g, b)` threshold in a click box or selection, largest near-circular connected component, desaturate and darken; `RedEyeTool` (pupil size, darken amount, IP-0915) and Filters, Enhance, Red Eye Removal (threshold, IP-0906) share it; `D01 T07 §5` consumes this detector.
  - Undo names "Healing Brush", "Spot Healing", "Patch", "Blemish Removal", "Inpaint", "Remove", "Red Eye"; one Information line each with layer and parameters hash.
  - Budget: a 200-pixel healing dab under 16 ms; inpainting a 100 by 100 region under 300 ms.
  - Fixtures `tests/fixtures/gesso/retouch/` (skin with blemishes, dust on sky, red-eye portrait crop, all original Rizonesoft images, none from third parties); GIMP 3.2.6 heal tool and red-eye goldens where the algorithm matches, property tests otherwise (healed-region mean within 2 of 255 of the ring around it, red-eye pupils lose at least 80 percent of their redness and untouched pixels are unchanged).
  - Commit: `"gesso: healing, patch, blemish, inpainting, remove, and red eye"`
- **Proof:** Unit test and driven run: `HealingTests`, `InpaintTests`, and `RedEyeTests` pass the tone-match and redness properties and the GIMP 3.2.6 goldens, and driven strokes are captured with undo restoring the pixel hash; cheaper substitute that fails: clone-only healing, which the ring tone-match property rejects on the gradient-sky fixture.

#### §3. The content-aware engine: fill, scale, and move

- **Deliverable:** An own PatchMatch completion engine in `Isotone.Gesso.Core/Retouch/ContentAware/` with the Content-Aware Fill workspace, the Fill dialog option, delete and fill, heal selection, content-aware scale by seam carving with protection, and content-aware move and extend, all classical and offline.
- **Depends On:** D03 T10 §1
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/content-aware-fill/ and docs/captures/gesso/content-aware-scale/. Job: a user can remove an object or extend a scene and control which pixels the fill samples from, with no network and no AI. Treatment: a workspace with the document showing the sampling area as a tinted overlay, sampling brush and lasso tools, a live full-resolution preview panel, and adaptation settings, applied to a new layer by default. Cheaper substitute that fails: a blur or smear fill, which the texture-statistics property catches. Chrome: consume the selection model, the tool system, the brush cursor, and the suite dialog chrome; do not add a second preview renderer.
- **Runs:** `Requires: display-session -- the fill workspace, scale handles, and move drags are driven and captured`
- **Catalog:** IP-0917 to IP-0926 (10 features)
- **Hints:**
  - Decision row in `docs/dev/decisions.md`: own PatchMatch (Barnes et al. 2009, generalized with rotation and scale per Barnes et al. 2010) with coarse-to-fine EM completion (Wexler, Shechtman, and Irani 2007), resynthesizer as reference, the patent check recorded; no package.
  - `PatchMatchField.cs` (nearest-neighbor field over float tiles with a sampling mask, seeded, tile-order independent) and `ImageCompletion.cs` (pyramid, voting, color adaptation by per-patch gain and bias, rotation, scale, and mirror adaptation) in `src/Gesso/Isotone.Gesso.Core/Retouch/ContentAware/`.
  - Content-Aware Fill workspace `src/Gesso/Isotone.Gesso.Desktop/Retouch/ContentAwareFillWorkspace.xaml` (IP-0917, IP-0918, IP-0921): sampling brush add and subtract, fill-area lasso, expand and contract, sampling area auto, rectangular, custom, overlay color and opacity, preview panel at 100 percent.
  - Fill settings (IP-0922): color adaptation none, default, high, very high; rotation adaptation none to full; scale; mirror; output to current layer, new layer (default), or duplicate layer; reset; apply and OK; keys `Gesso.ContentAware.ColorAdaptation`, `RotationAdaptation`, `Scale`, `Mirror`, `Output`.
  - Edit, Fill with Content-Aware and color adaptation (IP-0920) added to the `D03 T12 §8` Fill dialog; Delete and Fill Selection (IP-0925) as one command; Heal Selection (IP-0926: sampling width, sample from sides, above and below, or all around, fill order) as the resynthesizer equivalent.
  - Content-Aware Scale (IP-0919, IP-0923): seam carving (Avidan and Shamir 2007) with forward energy (Rubinstein et al. 2008), amount, protect channel (alpha channel mask), protect skin tones by a classical YCbCr skin range, reference point, on the `D03 T03 §7` transform handles.
  - Content-Aware Move (IP-0924): move and extend modes, structure 1 to 7, color 0 to 10, transform on drop; the moved patch is blended by the §1 `SeamlessBlender` and the hole filled by `ImageCompletion`.
  - Wire §2: spot healing's Content-Aware type (IP-0909), the patch tool's content-aware mode (IP-0911), and the Remove tool's large-region fill now call `ImageCompletion`.
  - Consumers named in `src/Gesso/Isotone.Gesso.Core/Retouch/README.md`: `D03 T08 §9` crop fill, `D03 T15 §7` panorama edges, `D03 T19 §3` Remove tool off mode, `D03 T19 §9` distraction removal.
  - Undo names "Content-Aware Fill", "Content-Aware Scale", "Content-Aware Move", "Delete and Fill"; log with area, seed, and milliseconds; long runs report progress and cancel restoring the layer.
  - Budget: a 400 by 400 hole in a 24-megapixel image under 5 s on the reference machine, cancellable within one pyramid level.
  - Tests: `PatchMatchTests` (field converges to the exact match on a shifted-copy fixture), `CompletionTests` (texture statistics of the fill within 10 percent of the sampling area on a brick fixture, seed determinism), `SeamCarvingTests` (protected pixels unchanged, output width exact).
  - Commit: `"gesso: the content-aware engine with fill, scale, and move"`
- **Proof:** Unit test and driven run: `PatchMatchTests`, `CompletionTests`, and `SeamCarvingTests` pass, and a driven workspace fill onto a new layer is captured with its elapsed time quoted; cheaper substitute that fails: diffusion fill labeled content-aware, which the brick texture-statistics property rejects.

#### §4. Toning and focus tools

- **Deliverable:** Dodge, burn, sponge, Affinity's tone brush, blur, sharpen, GIMP's convolve tool, and the median brush, each a brush-driven local operation with one undo step per stroke.
- **Depends On:** D03 T12 §5
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/toning-tools/. Job: a retoucher can lighten, darken, saturate, blur, or sharpen exactly where they paint. Treatment: tools on the painting-tool base with their options in the options bar and the shared brush options. Cheaper substitute that fails: painting white or black at low opacity labeled as dodge and burn, which the protect-tones test catches. Chrome: consume the `D03 T12 §5` base and options bar; do not add a second dab loop.
- **Runs:** `Requires: display-session -- toning strokes are driven and captured`
- **Catalog:** IP-0927 to IP-0933 (7 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Painting/EffectDab.cs`: applies a tile-local operation under the brush mask per dab with the dab's opacity and flow, the one mechanism every tool here uses.
  - `DodgeTool` and `BurnTool` (IP-0927): range shadows, midtones, highlights; exposure; protect tones (Photoshop) and protect hue (Affinity) as a luminance-only adjustment in linear light with hue held.
  - `SpongeTool` (IP-0928): saturate or desaturate, flow, vibrance on the `D01 T03 §5` `Vibrance` math.
  - `ToneBrush` (IP-0929, Affinity 3): paint brightness, contrast, and color offsets with nozzle colors sampled from the canvas.
  - `BlurTool` and `SharpenTool` (IP-0930, IP-0931): strength, mode, sample all layers, protect detail, unsharp mask and harsh modes on the `D01 T03 §6` Gaussian and `UnsharpMask`; the Clarity mode is shown disabled with a tooltip naming `D01 T06 §4`, which enables it.
  - `ConvolveTool` (IP-0932, GIMP): blur or sharpen with rate and Ctrl toggling the direction.
  - `MedianBrush` (IP-0933, Affinity) on the `D01 T03 §6` `Median`.
  - Settings keys `Gesso.Toning.<Tool>.<Option>` per option with defaults matching Photoshop (exposure 50 percent, midtones, protect tones on).
  - Undo names per tool; one Information line per stroke; zero allocations per dab; a 200-pixel dab under 4 ms on 16-bit documents.
  - Tests: `ToningToolTests` (dodge in midtones leaves pure black and white unchanged with protect tones, sponge desaturate reduces chroma monotonically, blur strength 0 is identity, median brush removes an isolated speck).
  - Commit: `"gesso: dodge, burn, sponge, tone, blur, sharpen, convolve, and median brushes"`
- **Proof:** Unit test and driven run: `ToningToolTests` pass and driven strokes are captured with undo restoring the hash; cheaper substitute that fails: overlay painting labeled dodge, which the protect-tones endpoint test rejects.

#### §5. Free Transform and move-tool transform extensions

- **Deliverable:** One `TransformSession` behind Free Transform with every Photoshop mode, modifier, and numeric option, transform again, multi-layer and selected-pixel transforms, clipping options, the Affinity Transform panel and move-tool transforms, layer rotate and flip, scale override, and the transformation HUD.
- **Depends On:** D03 T03 §7, D03 T09 §9
- **Phase:** 20
- **Surface:** UI. Fidelity: extends docs/captures/gesso/main-window/ (transform handles and options bar); new captures to docs/captures/gesso/transform-panel/. Job: a user can scale, rotate, skew, distort, and put layers into perspective by handle or by number, and repeat it. Treatment: handles on the canvas with modifier-driven modes, a numeric options bar with a reference-point grid, a Transform panel, and a HUD near the cursor. Cheaper substitute that fails: a render-transform preview that resamples on every drag step, which the single-resample test catches. Chrome: consume the tool system, options-bar host, the `D01 T03 §2` resampler, and the suite numeric field controls; do not add a second handle renderer.
- **Runs:** `Requires: display-session -- handle drags, modifiers, and the panel are driven and captured`
- **Catalog:** IP-0937 to IP-0955 (19 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Transform/TransformSession.cs` extending `D03 T03 §7`'s free transform: targets (layers, selected pixels floated from the selection, several selected layers together, a smart object's stored matrix per `D03 T09 §9`), a 3 by 3 matrix, and one resample from the original on commit, never cumulative (IP-0949, IP-0953).
  - Modes and submenu (IP-0937, IP-0945): Edit, Transform, Again, Scale, Rotate, Skew, Distort, Perspective, Warp (hands off to §6), Rotate 180, 90 clockwise and counterclockwise, Flip Horizontal and Vertical; modifier keys Ctrl distort, Ctrl+Shift skew, Ctrl+Alt+Shift perspective, Shift proportional toggle, Alt from center, Shift rotate in 15-degree steps, Esc cancel (IP-0954); proportional by default with the legacy preference `Gesso.Transform.LegacyProportional` (IP-0947).
  - Numeric options bar (IP-0946): reference point grid, X and Y absolute or relative, W and H percent with link, angle, H and V skew, interpolation (nearest, bilinear, bicubic, bicubic smoother, bicubic sharper, Lanczos, NoHalo, LoHalo from the `D01 T03 §2` resampler as extended in §11).
  - Transform Again (Shift+Ctrl+T) and duplicate and transform again (Alt+Shift+Ctrl+T) replay the last matrix relative to the current bounds (IP-0948).
  - Clipping (IP-0938): adjust, clip, crop to result, crop with aspect, shared with §11.
  - Transform panel `src/Gesso/Isotone.Gesso.Desktop/Panels/TransformPanel.xaml` (IP-0939, IP-0951): position, size, rotation, shear, anchor, aspect link, size to key object, absolute per-object sizing, size to same; scale override for strokes, effects, and text (IP-0940) as `Gesso.Transform.ScaleEffects`, which scales layer-style parameters of `D03 T09 §7` in the same command.
  - Move tool transforms (IP-0941, IP-0942, IP-0943, IP-0952, Affinity): rotate and shear handles on the move tool, draggable transform origin, arrow nudge 1 pixel and Shift 10, lock children, hide selection while dragging, transform separately, aspect constrain, cycle base or regular selection box.
  - Layer rotate and flip (IP-0944, IP-0950): Layer, Transform, Rotate 90, 180, arbitrary angle, Flip Horizontal and Vertical on the selected layers, distinct from `D03 T03 §7`'s canvas rotate.
  - HUD (IP-0955): width, height, angle, and delta near the cursor, placement setting `Gesso.Transform.HudPlacement` (off, top right, bottom right, top left, bottom left).
  - Smart objects store the matrix, so re-transforming resamples from the embedded source (`<gesso:transform matrix=...>` on the smart-object element owned by `D03 T09 §9`).
  - Undo "Free Transform", "Transform Again", "Rotate Layer", "Flip Layer"; one Information line with the matrix and interpolation.
  - Tests: `TransformSessionTests` (single resample: rotating 10 degrees ten times in one session equals one 100-degree rotate within 1 of 255, modifier modes, transform again), `TransformPanelTests`.
  - Commit: `"gesso: Free Transform modes, numeric options, Transform panel, and move-tool transforms"`
- **Proof:** Unit test and driven run: `TransformSessionTests.SingleResample` passes and a driven perspective transform with Transform Again is captured with undo restoring the hash; cheaper substitute that fails: resampling each drag step, which the single-resample test rejects.

#### §11. The GIMP transform tools

- **Deliverable:** GIMP's unified, handle, scale, rotate, shear, perspective, 3D transform, and flip tools, Scale Layer and Offset Layer, and the common transform options (target, direction, interpolation with NoHalo and LoHalo, clipping, previews, guides), all on §5's `TransformSession`.
- **Depends On:** §5
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/gimp-transform-tools/. Job: a GIMP user finds every transform tool they know with the same options. Treatment: one tool per GIMP transform with its on-canvas widget, the shared options in the options bar, and an on-canvas info dialog with Readjust and the matrix. Cheaper substitute that fails: aliases to Free Transform without the GIMP options, which the corrective-direction and handle-transform tests catch. Chrome: consume §5's `TransformSession` and handle renderer; no second transform implementation.
- **Runs:** `Requires: display-session -- each tool's widget is driven and captured`
- **Catalog:** IP-0956 to IP-0966 (11 features)
- **Hints:**
  - Extend `src/Isotone.Core/Imaging/Geometry/Resampler.cs` (`D01 T03 §2`) with `NoHalo` and `LoHalo` modes (Robidoux's samplers as in GEGL), goldens from GIMP 3.2.6 `gegl:transform sampler=nohalo` and `lohalo` within 2 of 255; §5 lists them too.
  - Common options (IP-0958) in `src/Gesso/Isotone.Gesso.Core/Transform/GimpTransformOptions.cs`: transform target layer, selection, path, or image (Path shown disabled naming `D03 T16 §5`, which enables it), direction normal or corrective (inverse matrix), interpolation none, linear, cubic, NoHalo, LoHalo, clipping adjust, clip, crop to result, crop with aspect, image preview, composited preview, guides (none, center lines, thirds, fifths, golden sections, diagonals, number of lines, spacing), preview opacity.
  - Tools in `src/Gesso/Isotone.Gesso.Core/Tools/Transform/`: `UnifiedTransformTool` (constrain, from pivot, pivot snap, matrix readout, readjust; IP-0960), `HandleTransformTool` (add, move, remove one to four handles solving translation, similarity, affine, or perspective by correspondence; IP-0961), `ScaleTool` (keep aspect, around center, width and height, readjust; IP-0962), `RotateTool` (angle, center, 15-degree snap, readjust; IP-0963), `ShearTool` (magnitude X and Y, arrow keys; IP-0964), `PerspectiveTool` (constrain handles, around center, matrix, readjust; IP-0965), `FlipTool` (direction toggle with Ctrl, arrow keys; IP-0959).
  - `ThreeDTransformTool` (IP-0966): camera field of view, rotate X, Y, Z, pan, constrain axis, Z axis, local frame, composed to a homography for the session.
  - Image, Scale Layer dialog with interpolation (IP-0956) and Layer, Offset (IP-0957) with edge behavior wrap, transparent, repeat edge through the `D01 T03 §7` `Offset` and inverse-mapper edge modes (the catalog note's `D01 T06 §13` lands later and only adds GEGL parameter names).
  - GIMP shortcuts (Shift+T unified, Shift+L handle, Shift+S scale, Shift+R rotate, Shift+H shear, Shift+P perspective, Shift+F flip, Shift+W 3D transform) registered in the GIMP shortcut set that `D03 T20 §3` switches.
  - Undo named after each tool; one Information line with the tool, matrix, and direction.
  - Tests: `GimpTransformToolTests` (corrective direction applies the inverse, handle transform with four handles equals the perspective tool on the same quad, 3D transform at zero angles is identity).
  - Commit: `"gesso: the GIMP transform tools on the shared transform session"`
- **Proof:** Format fidelity proof and driven run: NoHalo and LoHalo match the GIMP 3.2.6 goldens in `tests/fixtures/imaging/resample/`, `GimpTransformToolTests` pass, and each tool is captured; cheaper substitute that fails: Free Transform aliases, which the corrective-direction test rejects.

#### §6. Warp and mesh warp

- **Deliverable:** Photoshop's Bezier warp with split grids, presets, and multi-point selection, the warp style presets on math moved from Stilus, Affinity's mesh warp with source and destination modes on the extended `D01 T03 §7` `MeshWarp`, and GIMP's warp transform brush on a displacement field §9 reuses.
- **Depends On:** §5
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/warp/ and docs/captures/gesso/warp-transform/. Job: a user can bend a layer by a grid, a preset, or a brush and re-edit the warp on a smart object. Treatment: a Bezier grid over the layer with control-point handles, split and grid-size options, a style preset dropdown with bend and distortion, and a warp brush with behaviors. Cheaper substitute that fails: a bilinear grid without Bezier handles, which the curved-edge test catches. Chrome: consume §5's session and handles, the moved warp math, and the `D03 T12` brush cursor; no second mesh.
- **Runs:** `Requires: display-session -- grid drags, presets, and warp brush strokes are driven and captured`
- **Catalog:** IP-0967 to IP-0970 (4 features)
- **Hints:**
  - Move first: `WarpEffect`'s style math and `MeshMap` (Coons patches) from `src/Stilus/Isotone.Stilus.Core/Effects/Warp/` and `Effects/Envelope/` (`D02 T11 §5`) into `src/Isotone.Core/Vector/Warp/` as their second consumer; Stilus calls the moved types, its warp-style goldens still pass, and `D03 T16 §4`'s warp text consumes them later.
  - Extend `src/Isotone.Core/Imaging/Effects/Distort/MeshWarp.cs` (`D01 T03 §7`) with Bezier-patch nodes (sharp, smooth, symmetric), add-node, source and destination modes, and synchronize, so there is one mesh implementation; `D01 T06 §6` later registers its filter form.
  - Photoshop warp (IP-0967) in `src/Gesso/Isotone.Gesso.Core/Transform/Warp/BezierWarp.cs`: grid presets 3 by 3, 4 by 4, 5 by 5, custom; split crosswise, horizontal, vertical; marquee multi-point selection of control points; guides; entered from Free Transform through §5's session.
  - Warp styles (IP-0968): arc, arc lower, arc upper, arch, bulge, shell lower, shell upper, flag, wave, fish, rise, fisheye, inflate, squeeze, twist, and cylinder, with bend and horizontal and vertical distortion on the moved math.
  - Affinity mesh warp tool (IP-0970): source or destination mode, synchronize, add nodes, resampling; the live-filter form is `D03 T14 §1`, and on a smart object the mesh is kept on the smart object (`<gesso:mesh-warp>`) until then.
  - GIMP warp transform (IP-0969): `DisplacementField` (tiled float2) in `src/Gesso/Isotone.Gesso.Core/Transform/Warp/` with behaviors move, grow, shrink, swirl clockwise and counterclockwise, erase, smooth; strength, size, hardness, spacing, abyss (the `D01 T03 §2` edge modes), high-quality and real-time previews, stroke during motion or periodically; §9 Liquify builds on this field.
  - GPU: `src/Gesso/Isotone.Gesso.Rendering/Shaders/WarpFieldShader.cs` (ComputeSharp) applies the field, with CPU fallback parity within 1 of 255 and one Warning on fallback.
  - Undo "Warp", "Mesh Warp", "Warp Transform" (one step per session or stroke); one Information line each.
  - Tests: `BezierWarpTests` (identity grid is identity, curved edges have no kinks against a dense-sampled reference), `WarpStyleRasterTests` (each style maps the grid like Stilus's goldens), `DisplacementFieldTests` (erase restores identity), `WarpFieldShaderParityTests`.
  - Commit: `"gesso: warp, warp styles, mesh warp, and the warp transform brush"`
- **Proof:** Unit test and driven run: `BezierWarpTests`, `WarpStyleRasterTests`, and the GPU parity test pass, `grep -rn "class MeshMap" src` prints one path under `src/Isotone.Core/`, and driven warps are captured; cheaper substitute that fails: copying the Stilus style math into Gesso, which the one-path grep rejects.

#### §7. Puppet warp, cage transform, and pins

- **Deliverable:** Puppet warp with mesh and pins, Affinity's deform tool with bones, GIMP's N-point deformation and cage transform, on one triangle-mesh and sparse-solver core in Gesso.
- **Depends On:** §5
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/puppet-warp/ and docs/captures/gesso/cage/. Job: a user can pose a subject by pins, bones, or a cage while it bends naturally. Treatment: a mesh overlay with pins and rotation rings, a deform tool with anchor points and bone chains, and a cage polygon tool. Cheaper substitute that fails: per-pin radial displacement, which the rigidity test catches. Chrome: consume §5's session, the tool system, and the canvas overlay; no second solver.
- **Runs:** `Requires: display-session -- pin drags and cage edits are driven and captured`
- **Catalog:** IP-0971 to IP-0979 (9 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Transform/Deform/TriangleMesher.cs`: own constrained Delaunay (Bowyer-Watson with boundary constraints) over the layer's alpha with density fewer, normal, more points and expansion in pixels; no package.
  - `SparseSolver.cs` (sparse Cholesky with prefactor on pin add, conjugate gradient fallback) shared by puppet warp, N-point, perspective warp (§8), and adaptive wide angle (`D03 T14 §6`).
  - Puppet warp (IP-0971, IP-0972, IP-0976): as-rigid-as-possible two-step (Igarashi, Moscovich, and Hughes 2005), modes rigid, normal, distort, pin depth order, pin rotation auto or fixed with a rotation ring, multiple pins, show mesh.
  - Deform tool and filter (IP-0973, IP-0977): moving least squares (Schaefer, McPhail, and Warren 2006) rigid, similarity, affine, strength, anchor points, and bones as line-segment handles with bone chains (Affinity 3.3) in `MlsDeformer.cs`; `D01 T06 §6` moves this class to `Isotone.Core` as its second consumer.
  - N-point deformation (IP-0974, IP-0975, IP-0979, GIMP): ARAP on a square lattice (Dvoroznak 2014, the algorithm behind GEGL's `gegl:npd`) with square size, rigidity, ASAP, mesh visibility, on the shared solver.
  - Cage transform (IP-0978, GIMP): create cage, deform, fill original position with a plain color, by mean value coordinates (Hormann and Floater 2006), golden against GIMP 3.2.6 `gegl:cage-transform`.
  - Rendering: per-triangle inverse mapping through the `D01 T03 §2` resampler for commit and a GPU triangle-mesh preview in `Isotone.Gesso.Rendering` with CPU parity.
  - Smart objects keep pins, bones, and cages (`<gesso:puppet-warp>`, `<gesso:deform>`, `<gesso:cage>`) and re-open them for editing; the live-filter form is `D03 T14 §1`.
  - Undo "Puppet Warp", "Deform", "N-Point Deformation", "Cage Transform"; one Information line each; a pin drag re-solves 2,000 vertices under 16 ms.
  - Tests: `PuppetWarpTests` (rigid mode keeps triangle areas within 5 percent under a pin drag), `MlsDeformerTests` (anchors map exactly), `CageTransformTests` (golden), `SparseSolverTests`.
  - Commit: `"gesso: puppet warp, deform with bones, N-point, and cage transform"`
- **Proof:** Unit test and driven run: `PuppetWarpTests.RigidKeepsAreas`, `MlsDeformerTests`, and the GIMP 3.2.6 cage golden pass, and driven pin drags are captured; cheaper substitute that fails: radial falloff per pin, which the area-preservation test rejects.

#### §8. Perspective warp

- **Deliverable:** Photoshop's perspective warp with layout and warp modes, joined planes, auto and edge straightening, and Affinity's perspective tool with single or dual planes and source or destination modes.
- **Depends On:** §5
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/perspective-warp/. Job: a user can change the viewpoint of architecture or match an object to a scene's perspective. Treatment: layout mode draws quads that snap and join on shared edges, warp mode drags corners, and straighten buttons level the edges. Cheaper substitute that fails: independent homographies per plane that tear at shared edges, which the seam-continuity test catches. Chrome: consume §5's session, §7's solver, and the `D01 T03 §2` perspective corrector; no second homography code.
- **Runs:** `Requires: display-session -- layout and warp drags are driven and captured`
- **Catalog:** IP-0980 to IP-0982 (3 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Transform/PerspectiveWarp/PerspectiveWarpSession.cs` (IP-0980): planes as quads, auto-join of edges within 10 screen pixels, each plane's homography from the `D01 T03 §2` `PerspectiveCorrector` four-point variant, and a joined mesh smoothed by §7's `SparseSolver` so shared edges stay continuous.
  - Modes and commands (IP-0981): layout and warp modes, auto straighten near-vertical, auto level near-horizontal, both, edge straighten by Shift-click, Enter commit, Esc cancel, grid visibility.
  - Affinity perspective tool (IP-0982): single or dual plane, source or destination mode, grid, autoclip, rotate, flip, snap; its live-filter form is `D03 T14 §1`, and `D03 T14 §6`'s perspective filter reuses this engine.
  - Smart objects keep planes (`<gesso:perspective-warp>`) for re-editing.
  - Undo "Perspective Warp"; one Information line with plane count.
  - Tests: `PerspectiveWarpTests` (a synthetic building fixture straightened to verticals within 0.2 degree, no seam larger than 0.5 pixel between joined planes).
  - Commit: `"gesso: perspective warp and the perspective tool"`
- **Proof:** Unit test and driven run: `PerspectiveWarpTests` pass the straighten and seam assertions and a driven warp is captured; cheaper substitute that fails: unjoined per-plane homographies, which the seam assertion rejects.

#### §9. Liquify

- **Deliverable:** The Liquify workspace with every Photoshop and Affinity tool, brush option, mask, mesh, reconstruct, view mode, and commit, face-aware controls on manual or AI landmarks, and a GPU path, on §6's displacement field.
- **Depends On:** §6
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/liquify/. Job: a retoucher can push, twirl, pucker, and bloat pixels smoothly at full resolution and reshape faces by slider. Treatment: a full-window workspace with a tool strip, brush and mesh options, mask and view options, face-aware sliders, and its own undo, previewing at display resolution on the GPU. Cheaper substitute that fails: a CPU-only preview that stutters above 12 megapixels, which the frame-time benchmark catches. Chrome: consume §6's `DisplacementField` and shader, the `D03 T12` brush cursor, and the suite dialog chrome; no second field.
- **Runs:** `Requires: display-session -- liquify strokes, face sliders, and the frame-time measurement need an interactive desktop`
- **Catalog:** IP-0983 to IP-0995 (13 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Retouch/LiquifyWorkspace.xaml` with `LiquifyViewModel` over §6's `DisplacementField`; Filter, Liquify (Shift+Ctrl+X) opens it (IP-0987, IP-0988).
  - Tools (IP-0983, IP-0990, IP-0991): forward warp W, reconstruct R, smooth E, twirl clockwise C (Alt counterclockwise), pucker S, bloat B, push left O, freeze mask F, thaw mask D, face A, hand H, zoom Z; Affinity push forward, push left, twirl, pinch, punch, turbulence, and mesh clone.
  - Brush options (IP-0984, IP-0993): size, density, pressure, rate, stylus pressure, pin edges; hardness, opacity, speed, ramp, drag resize, slow warp; keys `Gesso.Liquify.<Option>`.
  - Masks and reconstruct (IP-0985, IP-0992): freeze and thaw with clear, all, invert, and replace, add, subtract, intersect from selection, transparency, or layer mask; reconstruct modes revert, rigid, stiff, smooth, loose with an amount.
  - Mesh (IP-0994): show, divisions, color, opacity, reconstruct, apply, reset, last mesh, and save and load as an own `.imgmesh` file (header plus a half-float field at full resolution, zlib-compressed); Photoshop `.msh` is not read (undocumented), stated in the help page.
  - View and commit (IP-0995): show image, mesh, guides, backdrop (layer, mode in front, behind, blend, opacity), view modes none, split, mirror; OK applies, Cancel restores the layer.
  - Face-aware (IP-0986): eyes (size, height, width, tilt, distance), nose (height, width), mouth (smile, upper and lower lip, width, height), face shape (forehead, chin height, jawline, face width) as parametric displacement fields around landmarks from `IFaceLandmarkSource`; this section ships manual landmark placement (drag 12 points) that works offline, and `D03 T19 §11` supplies AI detection through the same interface.
  - Live filter (IP-0989): on a smart object the mesh is stored with it (`<gesso:liquify mesh="data/<id>.imgmesh">`) so Edit in workspace and Reset mesh work; the smart-filter stack entry is `D03 T14 §1`.
  - GPU: `LiquifyBrushShader` and §6's `WarpFieldShader` (ComputeSharp) with CPU parity within 1 of 255; preview at display resolution, full-resolution resample once on OK.
  - Inner undo inside the workspace (Ctrl+Z and history of strokes); one outer undo step "Liquify" on OK with one Information line (strokes, tools used, milliseconds).
  - Budget: a 200-pixel brush at 60 frames per second on a 24-megapixel layer with a DirectX 12 device; CPU fallback at 30 frames per second on 12 megapixels (benchmark quoted).
  - Tests: `LiquifyToolTests` (reconstruct revert returns to identity, freeze mask blocks displacement, twirl direction), `MeshFileTests` (round trip), `FaceAwareTests` (eye size moves only pixels near the eye landmarks).
  - Commit: `"gesso: Liquify with face-aware controls and a GPU path"`
- **Proof:** Unit test and driven run with evidence: `LiquifyToolTests`, `MeshFileTests`, and `FaceAwareTests` pass, and a driven session on a 24-megapixel fixture logs its frame times (quoted) with captures of each view mode; cheaper substitute that fails: CPU-only per-frame full-resolution resampling, which the frame-time benchmark rejects.

#### §10. Frequency separation and retouching workflows

- **Deliverable:** Affinity's frequency separation with Gaussian, median, and bilateral methods and exact recombination, the retouching studio workspace preset, and the dodge-and-burn layer and feathered-vignette workflow commands.
- **Depends On:** §2
- **Phase:** 20
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/frequency-separation/. Job: a retoucher can split texture from tone and retouch each without changing the other. Treatment: a dialog with radius, method, tolerance, low and high previews, and a layer switch, producing a named group. Cheaper substitute that fails: a Gaussian split whose recombination drifts in 8-bit, which the exact-recombination test catches. Chrome: consume the generated filter dialog frame (`D03 T05 §1`), the layer model, and blend modes; no second dialog frame.
- **Runs:** `Requires: display-session -- the dialog and its previews are driven and captured`
- **Catalog:** IP-0934 to IP-0936 (3 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Retouch/FrequencySeparation.cs` (IP-0934): low pass by the `D01 T03 §6` Gaussian, `Median`, or `SmartBlur` (the thresholded bilateral) with radius and tolerance; high frequency as difference plus 50 percent gray in Linear Light for 8 and 16 bits and exact subtraction in 32-bit float; creates a group "Frequency Separation" with Low and High layers in one command.
  - Dialog previews low, high, and combined, and the layer switch selects which layer becomes active after apply.
  - Exact recombination: 16-bit and float round trips are exact, 8-bit within 1 of 255, asserted on a noise fixture.
  - Retouching studio (IP-0935): a workspace preset file `src/Gesso/Isotone.Gesso.Desktop/Workspaces/retouching.json` (panels Layers, History, Clone Source, Brushes; tools healing, clone, dodge, burn, liquify) that `D03 T20 §1`'s workspace switcher loads; until `D03 T20 §1` ships, Window, Workspace lists it through `D03 T07 §17`'s workspaces.
  - Workflow commands (IP-0936): Layer, New, Dodge and Burn Layer (Overlay, filled 50 percent gray, neutral-color flag) and Vignette from Feathered Selection (an adjustment layer with a feathered elliptical mask), each one undo step.
  - Undo "Frequency Separation", "New Dodge and Burn Layer", "Vignette"; one Information line each.
  - Commit: `"gesso: frequency separation and retouching workflows"`
- **Proof:** Unit test and driven run: `FrequencySeparationTests` prove exact recombination in 16-bit and float and within 1 of 255 in 8-bit for each method, and the dialog is captured; cheaper substitute that fails: Photoshop's 8-bit subtract-and-divide recipe without offset handling, which the recombination test rejects.

#### Sizing concerns

- §5 owns 19 features and eleven hint groups including the Transform panel; if it exceeds 30 items, split the Free Transform session, modes, and numeric options from the Transform panel, move-tool transforms, and HUD.
- §9 carries a workspace, a file format, face-aware controls, and a GPU path for 13 features; the natural split is the liquify tools, masks, and GPU brush versus the mesh file, view modes, face-aware controls, and smart-object hosting.

### todo/03-gesso/TODO-14-gesso-parity-filters.md -- `gesso-parity-filters`

- **Title:** "TODO-14 -- Gesso Parity: Smart Filters, the Filter Menu, the Filter Gallery, and Interactive Filter Surfaces"
- **Phase(s):** 21, 22
- **Goal:** Every pixel effect in the suite engine (`D01 T03` and `D01 T06`) is reachable in Gesso and can stay live: smart filters on smart objects, Affinity live filter layers, and GIMP 3 layer filters with masks, per-filter blending, blend ranges, and a filter brush (§1); a Filter menu, generated dialogs, presets, repeat, recent, and Fade built from effect descriptors (§2); the Filter Gallery (§3); the Blur Gallery (§4); lens correction with lensfun profiles and adaptive wide angle (§6); Vanishing Point and Affinity's live projections (§7); lighting and gradient-flare surfaces (§5); the GEGL operation tool and filter browser (§8); GIMP's decor and combine scripts as native undoable commands (§9); and Affinity's procedural texture, equations, and FFT denoise dialogs (§10). Gesso code lives in `src/Gesso/Isotone.Gesso.Core/Filters/`, `src/Gesso/Isotone.Gesso.Rendering/`, and `src/Gesso/Isotone.Gesso.Desktop/Filters/`; algorithms are consumed from the engine, never re-implemented in Gesso; live filters persist through the `D03 T08 §1` `gesso:` contract with a rendered PNG fallback; every apply is one undo step with one Information line; no Adobe, Affinity, or GIMP presets, flares, textures, or lens profiles beyond the decided lensfun data are bundled.
- **Current-state facts to verify (with claim candidates):**
  - Seven filter commands only log that a dialog would open. `<!-- claim: count "_logger\.Information\(\"Opening (Gaussian|Motion|Surface|Unsharp|Smart|Add Noise|Reduce Noise)" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 7 -->`
  - The Filter menu is hand-written XAML with three submenus, which §2 replaces with a generated menu. `<!-- claim: count "Header="_(Blur|Sharpen|Noise)"" src/Gesso/src/Gesso.UI/Views/MainWindow.xaml = 3 -->`
  - The smart object layer (117 lines) carries no filter stack. `<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/SmartObjectLayer.cs = 117 -->` `<!-- claim: count "Filter" src/Gesso/src/Gesso.Core/Layers/SmartObjectLayer.cs = 0 -->`
  - No layer kind for live filter layers exists. `<!-- claim: count "Filter" src/Gesso/src/Gesso.Core/Layers/LayerType.cs = 0 -->`
  - The only filter contract is the 53-line 8-bit plug-in interface, which §2 does not extend (plug-in hosting is backlog B-024 and B-012). `<!-- claim: lines src/Gesso/src/Gesso.Plugins.Abstractions/IFilterPlugin.cs = 53 -->`
  - An adjustment layer model type exists, the precedent a live filter layer follows. `<!-- claim: exists src/Gesso/src/Gesso.Core/Layers/AdjustmentLayer.cs -->`
- **Inputs and XREFs:** `standards/gesso.md`; `docs/parity/gesso-parity.md`; GIMP 3.2.6 (layer filters, GEGL tool, filter browser, decor and combine scripts), Photoshop 27.10 (smart filters, Filter Gallery, Blur Gallery, Lens Correction, Adaptive Wide Angle, Vanishing Point), and Affinity Photo 3.3 (live filter layers, procedural texture, equations, FFT denoise) as behavior references; the lensfun database (data CC BY-SA 3.0, `https://github.com/lensfun/lensfun`, commit recorded) and the Adobe Lens Correction Profile format for user imports; Carroll, Agrawala, and Agarwala 2009 (content-preserving projections) and Zheng et al. 2009 (single-image vignetting); -> XREF: D03 T05 §1 (the filter pipeline and dialog frame §2 extends); -> XREF: D03 T07 §3 (the legacy filter catalog whose disabled items §2 resolves); -> XREF: D01 T03 §1 (the registry, descriptions, and effects every surface runs); -> XREF: D01 T06 §1 (traits, float pipeline, GEGL op map, and on-canvas descriptors); -> XREF: D01 T06 §3, D01 T06 §5, D01 T06 §6, D01 T06 §8, D01 T06 §9, D01 T06 §13 (the kernels §4, §10, §6, §5, §10, §8 surface); -> XREF: D03 T09 §9 (smart objects hosting smart filters); -> XREF: D03 T09 §5 (Blend If on live filter layers); -> XREF: D03 T09 §6 (per-filter blend modes); -> XREF: D03 T09 §7 (layer styles the decor commands use); -> XREF: D03 T12 §1 (brush engine behind the filter brush); -> XREF: D03 T12 §9 (gradients for the flare editor); -> XREF: D03 T03 §2 (tile snapshots Fade blends against); -> XREF: D03 T08 §1 (the `gesso:` contract for filter stacks, live filter layers, planes, and projections); -> XREF: D03 T10 §10 (filters on channels and saving blur masks to channels); -> XREF: D03 T11 §1 and D03 T11 §2 (adjustments applied to smart objects become smart filters; shadows and highlights live filter); -> XREF: D03 T11 §9 (color pickers in generated dialogs); -> XREF: D03 T13 §1 and D03 T13 §2 (clone and heal inside Vanishing Point); -> XREF: D03 T13 §6, D03 T13 §7, D03 T13 §8, D03 T13 §9 (mesh warp, puppet warp, perspective warp, and liquify as smart filters); -> XREF: D03 T15 §1 (the Camera Raw filter runs as a smart filter through §1); -> XREF: D03 T16 §1 (labels for Slide and Filmstrip); -> XREF: D03 T17 §3, D03 T17 §13 (PSD smart filter read and write); -> XREF: D03 T17 §4, D03 T17 §14 (XCF layer filter read and write through the GEGL op map); -> XREF: D03 T17 §10 (EXIF lens data for profile matching once the metadata reader ships); -> XREF: D03 T20 §3 (command search lists filters); -> XREF: D03 T20 §4 (the Preferences control for showing all gallery groups); -> XREF: D01 T07 §3 (the develop engine consumes §6's lensfun database and defringe rather than its own).
- **Adjacency:** list=applicable (the filter browser §8, filter presets and recent filters §2, gradient flares §5, lens profiles §6); document=not-applicable (no printed output); settings=applicable (`Gesso.Filters.*` keys for recent count, live cache, gallery groups, remembered parameters, with Preferences pages in D03 T20 §4 and §5); reporting=applicable (the smart filter stack in the Layers panel and the lens-profile match report in §6); notifications=applicable (progress and cancel for every filter over one second, Blur Gallery and lens batch progress); permissions=applicable (filters unavailable in indexed and bitmap modes say why, locked layers refuse by name, an unreadable lens profile or map file is refused by name); audit=applicable (one Serilog Information line per filter apply, filter-stack edit, and decor command); exchange=applicable (`gesso:` filter elements, XCF and PSD filter translation, lensfun XML and LCP import, flare files, filter presets, Vanishing Point planes); reverse=applicable (every apply and stack edit is one undo step; Fade and merge-filter are undoable; live filters are removable without loss)

#### §1. Smart filters, live filter layers, and non-destructive layer filters

- **Deliverable:** A filter stack on any layer and on smart objects with a shared or per-filter mask, per-filter blend mode and opacity, re-edit, reorder, hide, copy, merge, and rasterize; Affinity live filter layers with nesting, clipping, masks, and blend ranges; filters on pass-through groups; a filter brush; and live-by-default application, all cached in the render graph and persisted in the `gesso:` namespace.
- **Depends On:** D03 T09 §9, D03 T07 §3
- **Phase:** 21
- **Surface:** UI. Fidelity: extends docs/captures/gesso/main-window/ (Layers panel filter rows); new captures to docs/captures/gesso/smart-filters/. Job: a user can apply any filter without losing the original pixels and change, reorder, mask, or remove it later. Treatment: filter rows nested under the layer in the Layers panel with visibility eyes, a blending-options icon per row, and a mask thumbnail; live filter layers appear as their own rows with a filter badge. Cheaper substitute that fails: storing only the filtered pixels plus a list of names, which the re-edit-after-reopen test catches. Chrome: consume the `D03 T03 §3` Layers panel, the `D03 T09` layer model and blend modes, the brush engine, and the `D03 T05 §1` dialog frame; do not add a second layers list.
- **Runs:** `Requires: display-session -- stack edits, mask painting, and the filter brush are driven and captured`
- **Catalog:** IP-0998 to IP-1012, IP-1065 (16 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Filters/Live/FilterStack.cs`: ordered `FilterEntry` (an `EffectDescription`, blend mode, opacity, visible, id) on any layer (GIMP 3 layer filters, IP-1011) and on smart objects; Filter, Convert for Smart Filters wraps the layer into a `D03 T09 §9` smart object (IP-0998).
  - Stack operations (IP-0999, IP-1002, IP-1005, IP-1009, IP-1011): add, re-edit (double-click reopens the stored dialog), reorder by drag, hide and show, delete, clear, copy between layers (Alt-drag and Copy and Paste Filters), merge a filter into the pixels (GIMP 3 Merge Filter), and rasterize.
  - Masks (IP-1000, IP-1004): one filter mask per smart-filter stack with disable and delete (Photoshop), and one mask per live filter layer created from the selection automatically, painted, erased, or gradient-filled (Affinity).
  - Per-filter blending (IP-1001): mode and opacity per entry through a blending-options dialog, on the `D03 T09 §6` blend modes.
  - `LayerType.LiveFilter` and `src/Gesso/Isotone.Gesso.Core/Layers/LiveFilterLayer.cs` (IP-1003, IP-1010): filters the composite below within its group, nests, clips to the layer beneath, or becomes a child of a layer to restrict it; blend ranges and blend options through `D03 T09 §5` Blend If (IP-1006); filters on pass-through groups act as adjustment layers over what is below (IP-1012, GIMP 3.2).
  - Application behavior (IP-1008): filter commands apply live by default and Alt applies destructively; the `Gesso.Filters.ApplyLiveByDefault` key (default true) is consumed by `D03 T14 §2`'s runner.
  - Filter brush (IP-1007): `FilterBrushTool` on the `D03 T12 §1` brush engine paints a chosen live filter through its mask; this is also the brush form of wavelet denoise (IP-1065) and of any effect with the `SupportsDab` trait.
  - Rendering: `src/Gesso/Isotone.Gesso.Rendering/RenderGraph/FilterStackNode.cs` caches each entry's output tiles keyed by input tile hash and description hash, invalidates only downstream entries, previews at view scale while editing and refines at idle; cache ceiling `Gesso.Filters.LiveCacheMegabytes` (default 1024).
  - Native format: `<gesso:filters>` on the layer element with one `<gesso:filter op="<GEGL op id or effect id>" v= mode= opacity= visible=>` child holding the description JSON and a mask PNG under `data/`, and `<gesso:live-filter-layer>` for the new kind, each with the rendered PNG fallback per the `D03 T08 §1` contract.
  - Undo names "Add Smart Filter", "Edit Smart Filter", "Reorder Filters", "Delete Filter", "Merge Filter", "Paint Filter Mask", "New Live Filter Layer"; one Information line per edit.
  - Budget: re-editing a Gaussian radius 20 on a 24-megapixel smart object re-renders the visible region at view scale under 150 ms.
  - Consumers recorded in `src/Gesso/Isotone.Gesso.Core/Filters/Live/README.md`: `D03 T15 §1` Camera Raw, `D03 T11 §1` and `§2`, `D03 T10 §10` channels, `D03 T13 §6` to `§9` warps and liquify, `D03 T17 §3`, `§4`, `§13`, `§14` format translation.
  - Tests: `FilterStackTests` (re-edit after save and reopen, reorder changes output, hidden entry skipped, merge equals destructive apply), `LiveFilterLayerTests`, `FilterStackNodeCacheTests`, `GessoFilterFormatTests` (GIMP 3.2.6 opens the saved `.ora` with the fallback visible).
  - The wavelet denoise brush (IP-1065) is the filter brush painting D01 T06 §5 wavelet denoise through a mask.
  - Commit: `"gesso: smart filters, live filter layers, layer filters, and the filter brush"`
- **Proof:** Format fidelity proof and driven run: `GessoFilterFormatTests` reopen a committed fixture with a three-filter stack and masks as live, and GIMP 3.2.6 renders the fallback within 1 of 255 of Gesso's composite; the driven stack edit is captured; cheaper substitute that fails: baking pixels with a name list, which the re-edit-after-reopen test rejects.

#### §2. The Filter menu, generated dialogs, presets, and Fade

- **Deliverable:** A Filter menu generated from the registry with every engine effect, dialogs generated from parameter schemas with on-canvas controls, presets, split preview, clipping, blending, merge option, repeat and reshow, recent filters, reset, Fade, filter targets beyond layers, and the common GIMP and Affinity behaviors.
- **Depends On:** D01 T06 §1, D03 T07 §3
- **Phase:** 21
- **Surface:** UI. Fidelity: extends docs/captures/gesso/main-window/ (Filter menu) and docs/captures/gesso/filter-dialog/ (the `D03 T05 §1` frame). Job: a user finds every filter where Photoshop, Affinity, or GIMP put it and adjusts it with sliders or directly on the canvas. Treatment: category submenus generated from effect traits, a generated dialog with typed controls, presets, preview and split view, and an on-canvas overlay for points, rings, lines, ellipses, pins, and strength drags. Cheaper substitute that fails: hand-written XAML per filter, which the menu-coverage test catches. Chrome: consume the `D03 T05 §1` pipeline and dialog frame, the `D03 T11 §9` color picker, the `D03 T12 §9` gradient picker, and the canvas overlay; do not write a dialog per filter.
- **Runs:** `Requires: display-session -- generated dialogs, on-canvas controls, and Fade are driven and captured`
- **Catalog:** IP-1013 to IP-1026, IP-1063 (15 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Filters/EngineFilter.cs`: one `IImageFilter` adapter (the `D03 T05 §1` contract) wrapping any registry `IPixelEffect` through the `D01 T06 §1` `FloatPipeline`; Gesso holds no kernels, and the `D03 T07 §3` disabled items resolve as their effects register.
  - `src/Gesso/Isotone.Gesso.Desktop/Filters/FilterMenuBuilder.cs` (IP-1015, IP-1016, IP-1023): submenus Blur, Blur Gallery, Distort, Noise, Pixelate, Render, Light and Shadow, Sharpen, Stylize, Edge-Detect, Enhance, Generic, Map, Artistic, Decor, Combine, Lighting and Tonal, Other, mapped from each effect's category and traits; unavailable effects greyed with the `D01 T06 §1` reason as tooltip; a `FilterMenuCoverageTests` asserts every registry effect has a menu entry or an explicit hidden flag.
  - `GeneratedFilterDialog.xaml` from `EffectParameterSchema`: sliders with units, integer spinners, checkboxes, enums, `D03 T11 §9` color pickers, curve editor, `GradientStops` picker, point and angle controls, seed with randomize, matrix grid, expression box, and a custom-editor slot for effects with dedicated editors.
  - `OnCanvasControlOverlay` draws the `D01 T06 §1` descriptors (point handles, radius rings, angle dials, line segments, ellipse frames, pin sets, quads) and applies `StrengthDrag` so dragging on the canvas sets strength beyond the slider maximum (IP-1022); §4, §5, and §7 reuse it.
  - Common options (IP-1013, IP-1019): presets per filter (save, load, delete, favorites; `%LOCALAPPDATA%\Rizonesoft\Gesso\Presets\Filters\<effect-id>\<name>.json` as `EffectDescription`), input type, clipping adjust or clip, blending mode and opacity, preview, split view, and the merge-filter checkbox choosing destructive versus `D03 T14 §1` live.
  - Repeat and recent (IP-1017): Filter, Last Filter (Ctrl+Alt+F Photoshop set, Ctrl+F GIMP set), Reshow Last (Shift+Ctrl+F GIMP set), Recently Used submenu with `Gesso.Filters.RecentCount` (default 10).
  - Reset (IP-1018): Reset in every dialog and Filter, Reset All Filter Settings clearing the `D03 T05 §1` remembered parameters after a confirmation.
  - Fade (IP-1014, IP-1021, IP-1025): Edit, Fade <last> (Shift+Ctrl+F Photoshop set) with opacity and blend mode, available right after a filter, adjustment, or paint stroke, blending the `D03 T03 §2` before-tiles of that command; one new history step "Fade <name>".
  - Targets (IP-1020): `IFilterTarget` for layer pixels, layer masks, alpha and spare channels (`D03 T10 §10`), adjustment and fill layer masks, and live filter layer masks.
  - Behaviors (IP-1024, IP-1026): merge destructively, return to the previous tool after a filter (`Gesso.Filters.ReturnToPreviousTool`), add an alpha channel automatically for effects with `RequiresAlpha`, and commit an open filter dialog automatically when another operation starts (Affinity).
  - Multi-output effects (wavelet decompose) create a layer group with the outputs in Grain Merge mode; filter names feed `D03 T20 §3` command search.
  - Undo named after the filter title; one Information line per apply (filter id, target, parameters hash, milliseconds).
  - The Shake Reduction workspace (IP-1063): multiple blur-trace regions, the blur direction tool, and trace preview, hosted by the generated-dialog frame over the D01 T06 §4 deconvolution.
  - Commit: `"gesso: the generated Filter menu, dialogs, presets, repeat, and Fade"`
- **Proof:** Unit test and driven run: `FilterMenuCoverageTests` and `GeneratedDialogTests` (every schema type renders and round-trips) pass, and a driven twirl with an on-canvas origin drag, a preset save and load, and Fade at 50 percent are captured with the pixel hash after undo quoted; cheaper substitute that fails: hand-built dialogs for a subset, which the coverage test rejects.

#### §3. The Filter Gallery

- **Deliverable:** Photoshop's Filter Gallery with categories, thumbnails, a stacked effect-layer list, zoomable preview, and the preference that lists every gallery filter in the Filter menu.
- **Depends On:** §2
- **Phase:** 21
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/filter-gallery/. Job: a user can browse artistic filters by thumbnail and stack several before applying. Treatment: a large preview on the left, category folders with thumbnails in the middle, parameters and an effect-layer stack on the right. Cheaper substitute that fails: a combo box of names without thumbnails or stacking, which the stack-order test catches. Chrome: consume §2's generated parameter panel and the `D01 T03 §8` to `§10` effects; no second parameter UI.
- **Runs:** `Requires: display-session -- the gallery is driven and captured`
- **Catalog:** IP-1027 to IP-1029 (3 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Filters/FilterGalleryDialog.xaml` (IP-1027): preview with zoom 25 to 400 percent, category folders from the `GalleryGroup` trait (Artistic, Brush Strokes, Distort, Sketch, Stylize, Texture), thumbnails, a filter dropdown, and the §2 parameter panel.
  - Effect-layer stack (IP-1028): new, delete, reorder, hide; applied in order and stored as one smart-filter entry `filter-gallery` holding the ordered descriptions, so re-edit reopens the gallery.
  - Thumbnails rendered from a crop of the current document at `PreviewScale` 0.25 and cached under `%LOCALAPPDATA%\Rizonesoft\Gesso\Cache\gallery-thumbs\`; no bundled sample photo.
  - Show all Filter Gallery groups and names (IP-1029): key `Gesso.Filters.ShowAllGalleryGroups` (default false) consumed by §2's menu builder; the Preferences control is `D03 T20 §4`.
  - Undo "Filter Gallery"; one Information line with the stacked ids.
  - Budget: all thumbnails under 3 s cold; a parameter change previews under 250 ms.
  - Commit: `"gesso: the Filter Gallery"`
- **Proof:** Unit test and driven run: `FilterGalleryTests` prove stack order changes output and a re-edit restores the stack, and the dialog is captured with thumbnail timing quoted; cheaper substitute that fails: a single-effect gallery, which the stack test rejects.

#### §4. The Blur Gallery surface

- **Deliverable:** Photoshop's Blur Gallery workspace with field, iris, tilt-shift, path, and spin blurs combined in one session, pins and rings, the effects, motion, and noise panels, and output options including smart-filter hosting.
- **Depends On:** D01 T06 §3, §2
- **Phase:** 21
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/blur-gallery/. Job: a photographer can fake shallow depth of field or motion by placing pins on the image. Treatment: a full-window workspace with on-canvas pins, rings, ellipses, lines, and paths, a Blur Tools panel with one section per blur type, and Effects, Motion Effects, and Noise panels. Cheaper substitute that fails: five separate dialogs, which the combined-session test catches. Chrome: consume §2's on-canvas overlay and generated panels and the `D01 T06 §3` kernels; no Gesso-side kernel.
- **Runs:** `Requires: display-session -- pin placement and the workspace are driven and captured`
- **Catalog:** IP-1081 to IP-1089 (9 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Filters/BlurGallery/BlurGalleryWorkspace.xaml` hosting all five kernels in one session, rendered in one pass through the `D01 T06 §3` gallery kernels.
  - Field blur (IP-1081) with multiple pins, iris blur (IP-1082) with ellipse, roundness, and feather handles, tilt-shift (IP-1083) with focus and feather lines, distortion, symmetric distortion, path blur (IP-1084) with editable curve paths, speed, taper, centered, rear sync flash, strobe, and end-point shapes, spin blur (IP-1085) with angle, strobe, and Alt-drag pivot.
  - Pins (IP-1086): click adds, Delete removes, remove all, the blur ring sets the amount by drag, focus percent, preview toggle, H hides pins.
  - Effects panel (IP-1087): light bokeh, bokeh color, light range, on the `BokehHighlights` stage; Motion Effects panel for strobe shared by path and spin.
  - Noise panel (IP-1088): grain type uniform, Gaussian, grain; amount, size, roughness, color, highlights, on the `D01 T03 §6` `AddNoise` and `D01 T06 §5` generators.
  - Output (IP-1089): selection bleed, save mask to channels (the radius map as an alpha channel through `D03 T10 §10`), high quality, and applying as a smart filter through §1.
  - Undo "Blur Gallery"; one Information line with kernels and pin count; preview at 0.25 under 400 ms and full-resolution commit with progress and cancel.
  - Commit: `"gesso: the Blur Gallery workspace"`
- **Proof:** Unit test and driven run: `BlurGalleryTests` prove a combined field-plus-iris session equals the kernels run together and the saved channel equals the radius map, and the workspace is captured; cheaper substitute that fails: separate dialogs per blur, which the combined-session test rejects.

#### §6. Lens Correction and Adaptive Wide Angle

- **Deliverable:** Lens Correction with lensfun profile matching, custom corrections, and its dialog tools; chromatic aberration removal, defringe, and automatic vignette removal; lens profile import; correction over a file list; Adaptive Wide Angle with constraints; and Affinity's perspective filter, each available as a smart filter.
- **Depends On:** D01 T06 §6, §2
- **Phase:** 21
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/lens-correction/ and docs/captures/gesso/adaptive-wide-angle/. Job: a photographer can remove a lens's distortion, fringes, and vignetting automatically, or straighten a wide-angle shot by drawing lines that should be straight. Treatment: a Lens Correction dialog with Auto and Custom tabs, a grid, and straighten tools, and an Adaptive Wide Angle dialog with constraint tools, a detail loupe, and a mesh view. Cheaper substitute that fails: a single barrel slider, which the profile-match test catches. Chrome: consume §2's dialog frame and on-canvas overlay, the `D01 T06 §6` lens kernels, and `D03 T13 §7`'s sparse solver; no Gesso-side kernel.
- **Runs:** `Requires: display-session -- the dialogs, constraint drawing, and the file-list run are driven and captured`
- **Catalog:** IP-1159 to IP-1172, IP-1425 (15 features)
- **Hints:**
  - `src/Isotone.Core/Lens/LensfunDatabase.cs` and `LensMatcher.cs`: read the lensfun XML database bundled at a recorded commit (data CC BY-SA 3.0, attribution in About and `THIRD-PARTY-NOTICES.md`, decision row), match by make, model, lens, focal length, aperture, and distance with interpolation between calibrations; placed in `Isotone.Core` because `D01 T07 §3` (Phase 23) consumes it, recorded as its pending second consumer.
  - Profile import (IP-1171): `LcpReader` for user-owned Adobe LCP files and lensfun XML into `%LOCALAPPDATA%\Rizonesoft\Gesso\LensProfiles\`; none bundled from Adobe.
  - Lens Correction dialog `src/Gesso/Isotone.Gesso.Desktop/Filters/Lens/LensCorrectionDialog.xaml` (IP-1160, IP-1161, IP-1162, IP-1169): Auto tab (geometric distortion, chromatic aberration, vignette, auto scale, edge fill transparency, edge extension, or background color, search by make, model, lens; no online search) matched by EXIF from the open file's metadata (`D03 T17 §10` once it ships, otherwise manual pick); Custom tab (remove distortion, red-cyan, green-magenta, blue-yellow fringe, vignette amount and midpoint, vertical and horizontal perspective through the `D01 T03 §2` `PerspectiveCorrector`, angle, scale, save and load `.gesso-lens.json`); tools remove distortion, straighten, move grid, hand, zoom; grid overlay; preview.
  - Chromatic aberration removal (IP-1163) on the `D01 T06 §6` TCA model, and `src/Isotone.Core/Imaging/Effects/Lens/Defringe.cs` (IP-1164: purple and green hue ranges, complementary hue, tolerance, radius, edge threshold) as a registry effect `D01 T07 §3` consumes.
  - `AutoVignetteRemoval` (IP-1170): estimate radial falloff from radial-gradient symmetry (Zheng et al. 2009) and invert the `pa` model.
  - Lens Correction on files (IP-1172): pick files or a folder, output folder, format, per-file profile match, corrections, edge fill, auto scale, progress and cancel, never overwriting sources; this runs over a file list and is not the backlog B-042 batch engine.
  - Adaptive Wide Angle (IP-1165 to IP-1168): constraint and polygon constraint tools (lines shown as fitted arcs on fisheye), Shift for horizontal or vertical orientation, correction fisheye, perspective, full spherical, or auto from the profile, scale, focal length, crop factor, as shot, detail loupe, show constraints and mesh, save and load constraints as JSON; solved as a content-preserving projection (Carroll, Agrawala, and Agarwala 2009) on a mesh with `D03 T13 §7`'s `SparseSolver`.
  - Perspective filter (IP-1159): Affinity's single or dual plane, source and destination modes, autoclip, as a generated dialog with `QuadFrame` controls over `D03 T13 §8`'s engine.
  - Every correction applies live through §1 when the target is a smart object or the live default is on; undo "Lens Correction", "Adaptive Wide Angle", "Perspective"; one Information line with profile id and corrections.
  - Tests: `LensfunDatabaseTests` (a committed database slice parses and matches a fixture's EXIF), `LcpReaderTests`, `DefringeTests`, `AdaptiveWideAngleTests` (constrained lines become straight within 0.5 pixel on a synthetic fisheye grid).
  - The lens profile database reader (Lensfun XML and user-supplied Adobe LCP files, IP-1171, IP-1425) lives in `src/Isotone.Core/Lens/` so `D01 T07 §3` (Phase 23) consumes it instead of reading profiles itself.
  - Commit: `"gesso: Lens Correction, lens profiles, defringe, and Adaptive Wide Angle"`
- **Proof:** Format fidelity proof and driven run: a committed synthetic image distorted with a lensfun profile's coefficients is corrected to a straight grid within 0.5 pixel, `LcpReaderTests` parse a committed sample, and the dialogs and a three-file run are captured; cheaper substitute that fails: a manual barrel slider only, which the profile-match test rejects.

#### §7. Vanishing Point and live projections

- **Deliverable:** Vanishing Point with planes, perspective marquee, stamp, brush, heal, paste into planes, measure, and rendered grids, saved with the document and runnable as a smart filter, plus Affinity's equirectangular and perspective live projections.
- **Depends On:** §2, D03 T13 §1
- **Phase:** 21
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/vanishing-point/ and docs/captures/gesso/live-projection/. Job: a user can clone, paint, and paste onto surfaces in perspective, and edit a 360 panorama as a flat view. Treatment: a full-window workspace with plane grids colored by validity, tool strip, and options; a projection layer showing a perspective view of an equirectangular image. Cheaper substitute that fails: a perspective transform of pasted content only, which the stamp-in-plane test catches. Chrome: consume §2's overlay, `D03 T13 §1` cloning and `D03 T13 §2` healing, and the `D01 T06 §6` panorama projection; no second clone engine.
- **Runs:** `Requires: display-session -- plane creation, stamping, and projection editing are driven and captured`
- **Catalog:** IP-1173 to IP-1180 (8 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Filters/VanishingPoint/VanishingPointWorkspace.xaml` (IP-1177, IP-1180): Filter, Vanishing Point (Alt+Ctrl+V), output to the layer or a new layer, and as a smart filter through §1.
  - Planes (IP-1173): create by four clicks, edit corners and edges, grid size, tear off perpendicular planes with an angle by Ctrl-drag, color coding (blue valid, yellow doubtful, red invalid by an aspect and angle test), saved with the document as `<gesso:vanishing-point>` (planes, grid, measurements).
  - Marquee (IP-1174): feather, opacity, heal off, luminance, or on, move mode destination or source, transform (scale, rotate, flip), and paste into plane (clipboard content dragged onto a plane).
  - Stamp and brush (IP-1175): Alt-click source, aligned, heal modes through `D03 T13 §1` and `D03 T13 §2` mapped by each plane's homography, brush color and eyedropper.
  - Measure (IP-1176): distance in plane space, set scale from one known measurement, show edges, render grids and measurements to a layer.
  - `LiveProjectionLayer` (IP-1178): an equirectangular document edited as a perspective view (yaw, pitch, field of view) with edits reprojected on commit through the `D01 T06 §6` panorama projection; perspective live projection with planes (IP-1179): flatten a plane to a rectangle, edit, and reproject.
  - Undo "Vanishing Point", "Live Projection"; one Information line with plane count.
  - Tests: `VanishingPointTests` (a stamp in a plane scales with depth on a synthetic floor grid within 1 pixel, planes round-trip through save and reopen), `LiveProjectionTests` (a view edit reprojects to the right equirectangular pixels).
  - Commit: `"gesso: Vanishing Point and live projections"`
- **Proof:** Unit test and driven run: `VanishingPointTests` and `LiveProjectionTests` pass, and the workspace and projection layer are captured; cheaper substitute that fails: flat cloning without the plane homography, which the depth-scaling test rejects.

#### §5. Lighting and flare surfaces

- **Deliverable:** The lighting effects dialog with on-canvas light widgets, a lights panel, isolate light, interactive preview, and bump-map controls, lens flare center placement, and GIMP's gradient flare selector and editor.
- **Depends On:** D01 T06 §8, §2
- **Phase:** 22
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/lighting-effects/ and docs/captures/gesso/gradient-flare/. Job: a user can place and aim lights directly on the image and design lens flares. Treatment: on-canvas widgets for each light (point center, spot ellipse with hotspot and cone, infinite direction), a lights list, and a flare editor with glow, rays, and second-flare tabs. Cheaper substitute that fails: numeric light positions only, which the widget drive test catches. Chrome: consume §2's overlay and generated panels, the `D03 T12 §9` gradient picker, and the `D01 T06 §8` kernels.
- **Runs:** `Requires: display-session -- light widgets and the flare editor are driven and captured`
- **Catalog:** IP-1250 to IP-1252 (3 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Filters/Lighting/LightingEffectsDialog.xaml` (IP-1251): lights panel (add point, spot, infinite; delete; duplicate; isolate light), on-canvas widgets through the §2 overlay, interactive preview at view scale, material and environment tabs, presets menu over `D01 T06 §8`'s preset JSON.
  - Bump map (IP-1250): load from a channel, layer, or file, clear, scale to fit, opacity, curve type, height; files read through the Gesso codecs and handed as a buffer.
  - Lens flare and supernova center placement with a point handle.
  - Gradient flare selector and editor (IP-1252): list, new, edit (glow, rays, second-flare tabs with `D03 T12 §9` gradients), copy, delete, preview; flares stored as GIMP gflare text files in `%LOCALAPPDATA%\Rizonesoft\Gesso\GFlares\`, user imports accepted, one own default flare shipped.
  - Undo "Lighting Effects", "Gradient Flare"; one Information line each.
  - Commit: `"gesso: lighting effects and gradient flare surfaces"`
- **Proof:** Unit test and driven run: `LightingSurfaceTests` prove a widget drag updates the description's light position and a gflare file round-trips, and both surfaces are captured; cheaper substitute that fails: numeric-only lights, which the widget drive assertion rejects.

#### §8. The GEGL operation tool and the filter browser

- **Deliverable:** GIMP's GEGL Operation tool that runs any engine op by id with generated settings, preview, reset, and presets, and a searchable filter browser.
- **Depends On:** D01 T06 §13, §2
- **Phase:** 22
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/gegl-tool/ and docs/captures/gesso/filter-browser/. Job: an advanced user can run any operation, including graph-only ones, and find a filter by what it does. Treatment: a tool whose options show an op picker and the generated settings, and a browser listing name, title, category, GEGL id, and description with search. Cheaper substitute that fails: a list of menu filters only, which the graph-only-op test catches. Chrome: consume §2's generated dialog and the `D01 T06 §1` op map; no second parameter UI.
- **Runs:** `Requires: display-session -- the tool and browser are driven and captured`
- **Catalog:** IP-1030 to IP-1031 (2 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Tools/GeglOperationTool.cs` (IP-1030): pick any registry effect by GEGL id or effect id, including graph-only ops such as the `D01 T06 §13` point and blend ops, with generated settings, preview, reset, presets, applied to the selection or layer or as a live filter.
  - `FilterBrowserPanel.xaml` (IP-1031): search by name, title, description, category, and GEGL id with ranked results; details show parameters and the reference implementation; double-click opens the op.
  - Ops that an XCF file names but the engine lacks (`GeglOpMap.Unsupported`) appear greyed with their id, linked from the `D03 T17 §4` open report.
  - Undo named after the op; one Information line.
  - Commit: `"gesso: the GEGL operation tool and filter browser"`
- **Proof:** Unit test and driven run: `FilterBrowserTests` rank exact name matches first and list every registry effect, and a driven `gegl:weighted-blend` run is captured; cheaper substitute that fails: a menu-only list, which the graph-only-op assertion rejects.

#### §9. GIMP decor and combine effects as native commands

- **Deliverable:** GIMP's decor scripts (add bevel, add border, coffee stain, fog, fuzzy border, old photo, round corners, slide, stencil carve, stencil chrome) and combine scripts (depth merge, filmstrip) as native C# commands, each building its layers as one undoable command.
- **Depends On:** §2, D03 T09 §7
- **Phase:** 22
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/decor/. Job: a GIMP user finds the decor and combine effects they know, with the same options, working on Gesso layers. Treatment: Filters, Decor and Filters, Combine entries opening §2's generated dialogs; each run adds named layers or a new image. Cheaper substitute that fails: an embedded Script-Fu interpreter, which scripting's backlog B-041 owns and which the one-undo-step test catches. Chrome: consume §2's dialogs, the `D01 T06` effects, and `D03 T09 §7` layer styles.
- **Runs:** `Requires: display-session -- each command is driven and captured`
- **Catalog:** IP-1247, IP-1309 to IP-1323 (16 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Filters/Decor/DecorCommand.cs` base: parameters as an `EffectParameterSchema` (so §2 generates the dialog), a `Run(document)` that builds layers and channels inside one composite undo command named after the effect, and one Information line.
  - Decor (IP-1311 to IP-1323): Add Bevel with bump layer, Add Border with color delta, Coffee Stain (procedural stains from `D01 T06 §9` noise; no bundled brushes), Fog (color, turbulence, opacity on `D01 T06 §9` plasma), Fuzzy Border with shadow and weight, Old Photo (defocus, border, sepia, mottle, work on copy), Round Corners with drop shadow, offset, and background, Stencil Carve, Stencil Chrome with lightness and highlight balance.
  - Combine: Depth Merge (IP-1309: two sources and two depth maps, overlap, offset, scale) and Filmstrip (IP-1310: several images or layers, film height, color, numbering).
  - Labels (Slide IP-1319 labels and Filmstrip numbers) are text layers: until `D03 T16 §1` ships, their fields are disabled with a tooltip naming it, and `D03 T16 §1` enables them.
  - Shadows use the `D01 T06 §8` drop-shadow filter onto a new layer, and bevels use the moved `D03 T09 §8` bevel kernel.
  - Goldens: deterministic commands (add border, round corners, stencil carve, depth merge) against GIMP 3.2.6 script output within 3 of 255; snapshots for seeded ones.
  - Spyrogimp (IP-1247): spirograph, epitrochoid, sine, and Lissajous curves drawn as a path and stroked with the current D03 T12 painting tool.
  - Commit: `"gesso: GIMP decor and combine effects as native commands"`
- **Proof:** Format fidelity proof and driven run: `DecorCommandTests` match the GIMP 3.2.6 goldens where deterministic and prove each command is one undo step restoring the layer structure, with captures; cheaper substitute that fails: an embedded script interpreter, which the one-undo-step and no-interpreter reference tests reject.

#### §10. Dedicated filter editors and Affinity filter extras

- **Deliverable:** Affinity's FFT denoise spectrum painter, the procedural texture filter with equation lines, custom inputs, presets, and example recipes, and the equations filter with cartesian and polar systems.
- **Depends On:** D01 T06 §9, D01 T06 §10, D01 T06 §12, D01 T06 §13, §2
- **Phase:** 22
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/procedural-texture/, docs/captures/gesso/equations/, and docs/captures/gesso/fft-denoise/. Job: an advanced user can generate textures and distortions by typing equations, and remove periodic noise by painting out spectrum peaks. Treatment: an equation list with channel targets and validation messages, an inputs list with typed sliders, an origin handle on the canvas, and a spectrum view with a paint-out brush. Cheaper substitute that fails: a fixed list of textures, which the custom-expression test catches. Chrome: consume §2's dialog frame and overlay, the `D01 T06 §9` compiler, and the `D01 T06 §5` FFT filter.
- **Runs:** `Requires: display-session -- expression editing and spectrum painting are driven and captured`
- **Catalog:** IP-1240 to IP-1241, IP-1244, IP-1246, IP-1275, IP-1277, IP-1324 to IP-1330 (13 features)
- **Hints:**
  - FFT denoise (IP-1324) `src/Gesso/Isotone.Gesso.Desktop/Filters/FftDenoiseDialog.xaml`: log-magnitude spectrum from `D01 T06 §5` `SpectrumImage`, paint-out brush and eraser with size, automatic peak detection, preview; the painted mask is the `FftFilter` `AuxBuffer`.
  - Procedural texture filter (IP-1325, IP-1328): equation lines each targeting R, G, B, A, or a variable, built-in variables (x, y, rx, ry, w, h, and source channels), function-set browser (the `D01 T06 §9` noise functions), origin drag on the canvas; validation errors shown at the character position.
  - Custom inputs (IP-1329): range, real, integer, angle, elevation-rotation, each renamable and exposed as a slider.
  - Presets and example recipes (IP-1330): saved as `EffectDescription` JSON in `%LOCALAPPDATA%\Rizonesoft\Gesso\Presets\Filters\procedural-texture\`, with Gesso's own example recipes (wood, marble, checker, rings) authored here and no Affinity preset content.
  - Equations (IP-1326, IP-1327): cartesian `x'` and `y'` expressions with parameters A, B, C, a polar system, and extend modes, on `D01 T06 §13`'s `EquationsEffect`, which lands in the same phase; confirm it exists before wiring and record the missing Depends On edge in the section context.
  - All three run live through §1; undo named after the filter; one Information line with the expression hash.
  - Dedicated filter editors moved here from the engine sections, so no editor lives in a library section: the CML explorer settings, the flame fractal editor, the IFS fractal transform editor, and Qbist (algorithms in D01 T06 §10), and the GIMPressionist tabbed dialog with its orientation-map and size-map editors (algorithms in D01 T06 §12), each a custom parameter view hosted by the D03 T14 §2 dialog frame, with its settings files read and written as JSON presets.
  - Commit: `"gesso: procedural texture, equations, and FFT denoise"`
- **Proof:** Unit test and driven run: `ProceduralTextureTests` render a committed recipe to a snapshot golden, `EquationsTests` show `x' = x + A` shifts by A pixels, and FFT denoise removes a synthetic periodic pattern by at least 90 percent of its peak energy, with captures; cheaper substitute that fails: a fixed texture list, which the custom-expression test rejects.

#### Sizing concerns

- §1 carries a new layer kind, a render-graph cache, a filter brush, and the native-format elements for 15 features; if it passes 30 items, split the filter stack on layers and smart objects (with masks, blending, and persistence) from live filter layers, pass-through group filters, and the filter brush.
- §2 is the busiest surface (menu builder, generated dialog, on-canvas overlay, presets, Fade, targets); the natural split is the menu and generated dialogs versus Fade, targets, and common behaviors.
- §6 owns 14 features across two workspaces, an Isotone.Core database, and a file-list runner; split Lens Correction (profiles, dialog, defringe, vignette, file list) from Adaptive Wide Angle and the perspective filter if it overflows.

### todo/01-core/TODO-07-isotone-develop.md -- `isotone-develop`

- **Title:** "TODO-07 -- Isotone.Core Develop Engine: the Scene-Referred Pipeline for Gesso's Camera Raw Filter and Albumen"
- **Phase(s):** 23
- **Goal:** `src/Isotone.Core/Develop/` holds the suite's one develop engine: a versioned `DevelopSettings` record and a float32 linear-light, scene-referred pipeline (white balance, exposure and tone, profiles as LUTs, curves, presence, color mixer and grading, calibration, negative inversion, sharpening and noise, grain and vignette, lens profiles and geometry), a resolution-independent local masking engine, spot healing and red eye, and presets, snapshots, and Camera Raw (`crs`) XMP exchange. Gesso's Camera Raw filter and Develop studio (`D03 T15 §1`, `§2`, `§12`) are its first consumer and Albumen's develop module (`D04 T02 §2`) its planned second, which the integration commit rewrites to consume this file instead of building `Isotone.Albumen.Core/Develop/Pipeline/`. The engine references no WPF, no Gesso or Albumen type, and never opens a source file for writing; every stage is a pure function of its input tile and the settings, with a scalar reference beside its SIMD path, and settings are data that the consumers' histories undo.
- **Current-state facts to verify (with claim candidates):**
  - There is no `Isotone.Core` project yet, and so no `Develop/` folder; `D01 T02 §1` creates the project. `<!-- claim: absent src/Isotone.Core -->`
  - Albumen has no source tree, and its develop file still plans a pipeline inside its own assembly, which the integration commit rewrites to consume §1 to §3. `<!-- claim: absent src/Albumen -->` `<!-- claim: count "Isotone.Albumen.Core/Develop/Pipeline/" todo/04-albumen/TODO-02-albumen-develop.md = 1 -->`
  - Gesso has no develop code at all; its adjustment enum names Exposure and Vibrance only as display-referred adjustment layers. `<!-- claim: count "Develop" src/Gesso/src/**/*.cs = 0 -->` `<!-- claim: count "^    (Exposure|Vibrance),$" src/Gesso/src/Gesso.Core/Layers/AdjustmentLayer.cs = 2 -->`
  - No code reads a lens database anywhere in the tree. `<!-- claim: count "lensfun|Lensfun" src/**/*.cs = 0 -->`
  - Albumen's backlog still carries its own lens and color entries with an open data-source choice, which the integration commit rewords to consume §3 and §2. `<!-- claim: count "B-030\] Lens corrections" todo/backlog.md = 1 -->` `<!-- claim: count "B-031\] Color grading and HSL" todo/backlog.md = 1 -->`
- **Inputs and XREFs:** `standards/gesso.md` (float processing, SIMD with scalar reference, zero allocations per tile); `standards/albumen.md` (float32 linear light, one output transform at the end, preview and export agree within a stated tolerance); `standards/shared.md` (settings, logging, cancellation); Adobe DNG Specification 1.7.1.0 (camera profiles: HueSatMap, LookTable, ProfileToneCurve, white balance and the camera-to-XYZ model); Adobe XMP Specification Part 1 (2012) and the Camera Raw settings namespace `http://ns.adobe.com/camera-raw-settings/1.0/` as written by Lightroom Classic 14 and Camera Raw 17 presets; the lensfun 0.3.4 database format (`lensdatabase` XML, data CC BY-SA 3.0) and the Adobe Lens Profile (LCP) XMP layout; Robertson 1968 (correlated color temperature); He, Sun, Tang 2011 (dark channel prior) and He, Sun, Tang 2013 (guided filter); Ottosson 2020 (Oklab and OkLCh); Farbman et al. 2009 (mean-value coordinates cloning); von Gioi et al. 2012 (LSD line segment detector, implemented from the paper); Shih et al. 2019 (distortion-free wide-angle portraits); darktable 5.0 `darktable-cli` and lensfun 0.3.4 `lenstool` as reference renders with versions recorded beside each fixture; -> XREF: D01 T02 §1 (the Isotone.Core project and app-data paths the presets folder uses); -> XREF: D01 T02 §2 (settings keys for favorites, raw defaults, and presets folder); -> XREF: D01 T03 §1 (float tiles, the effect contract, the golden harness, `CounterRng`); -> XREF: D01 T03 §2 (`Resampler`, `LensCorrector`, `PerspectiveCorrector` the geometry stage composes); -> XREF: D01 T03 §4 (`Histogram`, `ToneCurve`, `TemperatureTint`, and `WhiteBalance` math §1 consumes); -> XREF: D01 T03 §5 (`HslMath` and `Vibrance` formulas §2 runs on OkLCh); -> XREF: D01 T03 §6 (`UnsharpMask`, `RemoveNoise`, `AddNoise` §3 consumes); -> XREF: D01 T04 §1 (input and output transforms); -> XREF: D01 T04 §2 (intents and black point compensation on the output transform); -> XREF: D01 T06 §4 (clarity, multi-band, and high-pass kernels); -> XREF: D01 T06 §5 (denoise kernels); -> XREF: D01 T06 §6 (projection math for upright and faces); -> XREF: D03 T13 §2 (the healing solver and red-eye detector §5 moves to Isotone.Core as their second consumer); -> XREF: D03 T13 §3 (the content-aware engine §5 reaches through a provider seam); -> XREF: D03 T14 §2 (the Filter menu lists §2's `isotone.dehaze` effect with no new code); -> XREF: D03 T14 §6 (the lens profile database §3 consumes or moves); -> XREF: D03 T15 §1, D03 T15 §2, D03 T15 §12 (the Gesso surfaces, first consumer); -> XREF: D03 T15 §6 and D03 T15 §7 (Merge to HDR and Panorama read §1's default tone curves); -> XREF: D03 T19 §11 (face boxes for §3's projection correction); -> XREF: D03 T19 §14 (estimated depth for §4's depth range mask); -> XREF: D03 T19 §15 (AI masks arriving as §4 bitmap components); -> XREF: D03 T17 §10 (consumes §6's XMP packet core for File Info and sidecars); -> XREF: D03 T07 §11 (Gesso's RAW open dialog develops through §1 instead of its own exposure and white balance code); -> XREF: D04 T01 §4 (the RAW decoder supplies linear camera RGB and its matrix through §1's `IDevelopSource`); -> XREF: D04 T01 §11 (Albumen's XMP sidecars consume §6's XMP core); -> XREF: D04 T02 §1, D04 T02 §2, D04 T02 §5 (Albumen's edit stack stores `DevelopSettings`, its pipeline section is rewritten to consume §1 to §3, and its presets consume §6); backlog B-028 to B-031 reworded by the integration commit (B-028 local adjustments to §4, B-029 detail to §3, B-030 lens to §3, B-031 color to §2) and B-033 (the GPU develop path) reworded to name this engine.
- **Adjacency:** list=applicable (the profile browser and the presets list are filterable by group, favorites, and support flags, §1 and §6); document=not-applicable (the engine prints nothing; Gesso prints through D03 T18 §6 and Albumen exports through D04 T02 §6); settings=applicable @ D01 T02 §2; reporting=applicable (the develop histogram and clipping statistics, §1, and the crs import report naming unmapped settings, §6); notifications=applicable (every render takes `IProgress<double>` and `CancellationToken`; the consuming app's status strip shows them); permissions=applicable (an unreadable preset, DCP, LCP, or lens XML file is refused by name; the bundled lens data folder is read-only); audit=applicable (one Serilog Information line per full-resolution render and per preset or profile import); exchange=applicable (crs XMP, DNG camera profiles, Adobe LCP, lensfun XML, own JSON presets); reverse=applicable (settings are immutable data with per-group reset; undo belongs to D03 T15's smart filter history and D04 T02 §1's edit stack)

#### §1. The develop pipeline core: white balance, exposure, tone, and curves

- **Deliverable:** `Isotone.Core/Develop/` with the versioned `DevelopSettings` record, the tile-parallel float32 scene-referred `DevelopPipeline`, and its first stages (white balance, light, tone curve, profiles as LUTs, auto tone, histogram and clipping), proven against goldens and a preview budget.
- **Depends On:** D01 T04 §2, D01 T03 §4
- **Phase:** 23
- **Surface:** no surface of its own (the Camera Raw filter dialog is D03 T15 §1; Albumen's develop panel is D04 T02 §3)
- **Runs:** none
- **Catalog:** IP-1400 to IP-1405 (6 features)
- **Hints:**
  - `src/Isotone.Core/Develop/DevelopSettings.cs`: an immutable record of groups (`WhiteBalanceSettings`, `LightSettings`, `ToneCurveSettings`, `ProfileSettings`; later sections add theirs) with `ProcessVersion` (starts at `P1`), `SchemaVersion`, identity defaults, and a System.Text.Json source-generated context; this is the type Albumen's `D04 T02 §1` edit stack stores (integration note for the rewrite).
  - `DevelopPipeline` and `IDevelopStage` (`Id`, `Order`, `IsIdentity(settings)`, `Process(ReadOnlyTile<RgbaF>, Tile<RgbaF>, DevelopContext)`) over `D01 T03 §1` float tiles, identity stages skipped, stages fused per tile; the working space is linear ProPhoto (ROMM) primaries at D50 as Camera Raw uses, values stay unbounded until the single output transform through `D01 T04 §1` and `§2` at the end.
  - `IDevelopSource` abstracts the input: a RAW source hands linear camera RGB plus its camera-to-XYZ matrix (`D04 T01 §4` decoder, reached by Gesso through `D03 T07 §11`), a layer source hands pixels plus their ICC profile (Gesso's Camera Raw filter); the engine linearizes both into the working space.
  - White balance (IP-1404): modes As Shot, Auto, Daylight 5500 K, Cloudy 6500 K, Shade 7500 K, Tungsten 2850 K, Fluorescent 3800 K, Flash 5500 K, Custom; temperature 2,000 to 50,000 K and tint -150 to 150 through Robertson 1968 onto the Planckian locus with Bradford adaptation to D50; non-RAW sources use Camera Raw's relative -100 to 100 scale; `WhiteBalance.FromSample(tile, point)` averages 5 by 5 for the eyedropper and tool; consume `D01 T03 §4` `TemperatureTint` rather than a second Kelvin table.
  - Light (IP-1402): exposure -5 to +5 EV as a linear multiply, contrast as an S-curve about 18 percent gray in log2, highlights and shadows as local tone on a guided-filter base and detail split of log luminance (He et al. 2013, radius proportional to the image diagonal so preview and export agree), whites and blacks as endpoint moves with a soft knee; Affinity's brightness and blackpoint map onto the same stages.
  - Tone curve (IP-1403): parametric regions (shadows, darks, lights, highlights with three split points) then point curves for RGB and each channel, evaluated by `D01 T03 §4` `ToneCurve` (monotone cubic), applied in a hue-preserving RGB-ratio mode with the refine saturation control compensating chroma.
  - Default tone curves (IP-1405): `BaseToneCurve` presets Linear, Natural, Compressed, High Contrast, and Log, readable by `D03 T15 §6` Merge to HDR and `D03 T15 §7` Panorama.
  - Profiles as LUTs (IP-1400): `DevelopProfile` (a 33-cubed 3D LUT with tetrahedral interpolation plus an optional tone curve) under `Isotone.Core/Develop/Profiles/` with Isotone's own set (Standard, Vivid, Neutral, Flat, Landscape, Portrait, Monochrome) generated by a committed script, never Adobe's; profile amount 0 to 200 percent blends the delta; favorites in `Isotone.Develop.Profiles.Favorites`; user DNG camera profiles (`.dcp`: HueSatMap, LookTable, ProfileToneCurve per DNG 1.7) import from the user's files only.
  - Auto tone and color (IP-1401): `AutoTone.Compute(Histogram)` from `D01 T03 §4` percentiles (0.05 and 99.95 percent clip, midtone to 18 percent gray, shadows and highlights from tail mass) and auto white balance by gray-world blended with white-patch; it returns settings deltas, never pixels, and uses no model.
  - `DevelopHistogram` (RGB and luminance, 256 bins) on the output-referred preview plus shadow and highlight clipping masks, the data D03 T15 §1 and Albumen's panel draw.
  - Budgets: SIMD and scalar paths agree within 1e-5 per stage; pooled tiles give zero allocations per tile; cancellation at tile granularity; a 2560 by 1440 preview from a 24-megapixel source through this section's stages under 60 ms and a full-resolution 24-megapixel render under 3 s on the reference machine, numbers recorded; the GPU path is backlog B-033.
  - `docs/dev/develop-engine.md`: process model, stage order, working space, and the rule that any output change at default settings bumps `ProcessVersion`; one Serilog Information line per full-resolution render (source size, stages run, settings hash, milliseconds).
  - Commit: `"core: the develop engine core with white balance, light, curves, profiles, and auto tone"`
- **Proof:** unit and golden proof: `DevelopPipelineTests` (SIMD equals scalar, defaults are identity within 1/65535 after the output transform, determinism), `WhiteBalanceTests` (the committed gray-card fixture renders neutral within Delta E 2000 1.0 at a sampled custom balance; Kelvin to xy within 0.0005 of Robertson's table), `LightAndCurveTests` against `darktable-cli` 5.0 exposure and curve references within 2/255, `AutoToneTests` on three committed fixtures, and the preview budget measured; cheaper substitute that fails: chaining the 8-bit display-referred `D01 T03` adjustments, which clips the highlights that the +2 EV then -2 EV round-trip test (input returned within 1e-4) keeps.

#### §2. Presence and color: texture, clarity, dehaze, color mixer, and grading

- **Deliverable:** Presence (texture, clarity, dehaze), vibrance and saturation, black and white mix, the HSL color mixer, point color, color grading, calibration, and negative and infrared inversion as develop stages, with dehaze also registered as a Filter-menu effect.
- **Depends On:** §1
- **Phase:** 23
- **Surface:** no surface of its own (D03 T15 §1 presents the panels; D03 T14 §2 lists the dehaze effect)
- **Runs:** none
- **Catalog:** IP-0604, IP-1406 to IP-1415 (11 features)
- **Hints:**
  - Texture and clarity (IP-1409): texture as band-pass contrast on a two-level guided pyramid (mid frequencies only), clarity through `D01 T06 §4`'s clarity kernel run on log luminance in the scene-referred buffer, never a second local-contrast implementation.
  - `src/Isotone.Core/Develop/Presence/Dehaze.cs` (IP-1406, IP-1409): dark channel prior (He, Sun, Tang 2011) with the transmission refined by the guided filter, airlight from the brightest 0.1 percent of the dark channel, negative amounts adding haze; Affinity's Haze Removal parameters (distance, strength, exposure correction) map to transmission floor, amount, and a post exposure; also registered as `IPixelEffect` `isotone.dehaze` in the `D01 T03` registry so `D03 T14 §2`'s generated Filter menu shows it.
  - Vibrance and saturation (IP-1408): the `D01 T03 §5` formulas evaluated on OkLCh chroma (Ottosson 2020) in linear data, vibrance weighted by inverse chroma with skin-tone protection for hues 20 to 60 degrees.
  - Treatment and black and white mix (IP-1407): `BlackAndWhiteMix` with eight band weights (red, orange, yellow, green, aqua, blue, purple, magenta) on OkLCh hue with raised-cosine falloff and an auto mix from the hue histogram.
  - Color mixer (IP-1410): hue, saturation, and luminance per the same eight bands; Camera Raw's HSL and Color modes and Affinity's HSL are views of one data set.
  - Point color (IP-1411): up to eight sampled swatches, each with hue, saturation, and luminance shifts and range refinement (hue, saturation, and luminance ranges with falloff) in OkLCh.
  - Color grading (IP-1412): shadows, midtones, highlights, and global wheels (hue, saturation, luminance), blending, and balance; legacy split toning reads into the same data.
  - Calibration (IP-1413): process version choice, shadows tint, and red, green, and blue primary hue and saturation, applied as one 3 by 3 matrix on the working-space primaries built once per settings.
  - Negative and infrared (IP-1414): `NegativeInversion` (film base picked or taken from the frame border, per-channel density inversion in log space, orange mask removal, auto levels on the result; darktable 5.0 negadoctor as the reference, GPL-3.0, read for behavior only) and infrared channel swaps (red and blue, red as luminance).
  - IP-1415 umbrella: the Affinity 3.3 RAW color, sharpening, and detail controls are served by §1 to §3 settings; `docs/dev/develop-engine.md` gains a table mapping each Affinity control to its setting.
  - Every group's defaults are identity and serialize under `DevelopSettings`.
  - Clarity and dehaze as an adjustment layer (IP-0604): the same stages exposed through the D03 T11 §1 adjustment-layer framework, added here because the engine lands in Phase 23.
  - Commit: `"core: presence, color mixer, point color, grading, calibration, and negative inversion in the develop engine"`
- **Proof:** golden and property proof: `DehazeTests` compare a committed hazy fixture with a `darktable-cli` 5.0 haze removal render within 4/255 mean (constants recorded) and assert amount 0 is identity and negative amounts add haze monotonically; `ColorMixerTests` rotate one band of a synthetic hue wheel and assert no pixel beyond that band's falloff moves more than 1 degree; `NegativeInversionTests` match a scanned negative fixture to its committed positive within mean Delta E 2000 3; cheaper substitute that fails: HSL in sRGB HSV, which the hue-wheel test catches when neighbouring bands move.

#### §3. Detail and optics: sharpening, noise, grain, vignette, lens, and geometry

- **Deliverable:** Sharpening, noise reduction, grain, glow, and post-crop vignette stages, lens profile, chromatic aberration, and defringe corrections from the lensfun database, and upright, manual geometry, face projection, and desqueeze, all resampled once through one composed inverse map.
- **Depends On:** §1, D01 T03 §2
- **Phase:** 23
- **Surface:** no surface of its own (D03 T15 §1 presents the Detail, Optics, Geometry, and Effects panels)
- **Runs:** none
- **Catalog:** IP-0635, IP-1416 to IP-1424, IP-1426 to IP-1430 (15 features)
- **Hints:**
  - Lens database (IP-1425), first item: consume `LensProfileDatabase` (lensfun XML and Adobe LCP readers) that `D03 T14 §6` builds; if it sits under `Isotone.Gesso.Core`, move it to `src/Isotone.Core/Develop/Lens/` as its second consumer (the engine serves Albumen) with one definition left. Bundle the lensfun 0.3.4 XML database under `Isotone.Core/Develop/Lens/Data/` with its CC BY-SA 3.0 notice, attribution in each app's About, and a `docs/dev/decisions.md` row (data, not linked code); LCP files are imported from the user's files only.
  - Profile corrections (IP-1423): match by EXIF make, model, lens, focal length, aperture, and distance with lensfun's interpolation; distortion (ptlens, poly3, poly5), TCA (linear, poly3), and vignetting (pa) with amounts 0 to 200 percent.
  - One composed inverse map: lens distortion, TCA, upright, manual geometry, face projection, and desqueeze compose into one per-pixel map resampled once through `D01 T03 §2` `Resampler` (Lanczos3); manual distortion (IP-1424) uses `LensCorrector`'s model and lens vignetting has amount and midpoint.
  - Chromatic aberration (IP-1422): automatic lateral CA by radial scaling of red and blue toward green, minimizing gradient mismatch over detected edge samples; defringe (IP-1426) with purple and green hue ranges, amounts, radius, tolerance, and threshold, the eyedropper returning a hue range around the sampled fringe.
  - Upright (IP-1427) and manual geometry (IP-1428): Auto, Level, Vertical, Full, and Guided (two to four user lines); segments by LSD implemented from von Gioi et al. 2012 (not the AGPL reference code), vanishing points by RANSAC, a homography composed with vertical, horizontal, rotate, aspect, scale, offset, and constrain crop (largest inscribed axis-aligned rectangle); reuse `PerspectiveCorrector` and `D01 T06 §6` projection math.
  - Face projection (IP-1429): a stereographic-to-perspective blend around face boxes after Shih et al. 2019, boxes from an `IFaceLocator` seam: user-drawn today, `D03 T19 §11` detections when that ships; anamorphic desqueeze (IP-1430) 1.33, 1.5, 1.8, 2.0, or custom.
  - Sharpening (IP-1419, IP-1420): amount, radius, detail (halo suppression by blending toward a deconvolution result), and masking (Sobel-magnitude edge mask, exposed as a mask view for Alt-drag previews) on linear luminance through `D01 T03 §6` `UnsharpMask`; multi-band and high-pass modes call `D01 T06 §4` kernels.
  - Noise reduction (IP-1421): luminance by à trous wavelet shrinkage in an opponent space (detail, contrast) and color by chroma smoothing guided by luminance (detail, smoothness), Affinity's contribution as a blend; call `D01 T06 §5` kernels where they exist.
  - Grain (IP-1418): amount, size, roughness, color, and Gaussian mode from `CounterRng` seeded per document so tiles agree between preview and export; glow (IP-1416) screens back a Gaussian-pyramid blur of pixels above a threshold; post-crop vignette (IP-1417) with highlight priority, color priority, and paint overlay styles, midpoint, roundness, feather, and highlights.
  - Grain as an adjustment layer (IP-0635): amount, size, and roughness through the D03 T11 §1 adjustment-layer framework.
  - Commit: `"core: detail, lens profiles, chromatic aberration, upright, and effects in the develop engine"`
- **Proof:** golden proof: `LensProfileTests` compare a committed fixture corrected by lensfun 0.3.4 `lenstool` within 1 px geometric error and 2/255; `UprightTests` recover the verticals of a synthetic facade within 0.2 degrees; `SharpenAndNoiseTests` compare with `darktable-cli` 5.0 references plus property tests (zero amount identity, noise variance falls); cheaper substitute that fails: resampling once per geometric stage, which the test asserting a single `Resampler` call per render and the MTF50 sharpness check both catch.

#### §4. The local masking engine

- **Deliverable:** Resolution-independent develop masks (brush, linear, radial, bidirectional, color, luminance, depth, and external bitmap components) combined by a boolean tree, refined, and driving a local adjustment set that reuses the global stage code.
- **Depends On:** §1
- **Phase:** 23
- **Surface:** no surface of its own (the masking panel and overlays are D03 T15 §2)
- **Runs:** none
- **Catalog:** IP-1431 to IP-1439 (9 features)
- **Hints:**
  - `src/Isotone.Core/Develop/Masking/DevelopMask.cs` components: `BrushStroke` (points in normalized image coordinates with size, feather, flow, density, hardness, erase, auto mask; IP-1431), `LinearGradient`, `RadialGradient` (feather, roundness, invert), and `BidirectionalGradient` (IP-1432), `ColorRange` (sampled OkLab points with tolerance) and `LuminanceRange` (range with falloff; IP-1433), `DepthRange` (IP-1434), and `BitmapComponent` (an external mask such as a `D03 T19 §15` AI mask, stored by hash with its provenance id).
  - Combine (IP-1435): add, subtract, intersect, invert, and duplicate as a boolean tree over float coverage (max, min, product rules recorded in the engine doc).
  - Rasterize at render resolution from the stored geometry so preview and export agree; brush dabs from a precomputed dab table; auto mask limits dabs by an edge-aware guided-filter coverage.
  - Feather and edge refinement (IP-1436): guided filter with radius and epsilon, and the range-mask refine controls.
  - Depth range: enabled only when the source supplies depth (a HEIC depth map from `D03 T17 §5` or the estimated depth of `D03 T19 §14`); otherwise refused by name with "No depth data: this image has no depth map", and the result always carries the flag "depth is estimated, not measured" when it came from `D03 T19 §14`.
  - `LocalAdjustmentSet` (IP-1437, IP-1438): exposure, contrast, highlights, shadows, whites, blacks, temperature, tint, hue, saturation, texture, clarity, dehaze, sharpness, noise, moire, defringe, color overlay, local color grading, and point color, plus mask amount and opacity; evaluated by §1 to §3 stage code with a per-pixel weight, never a second stage implementation.
  - Brush and gradient overlays (IP-1439, Affinity): the same model with its own opacity.
  - Mask rasters cached per mask version; budget: ten local adjustments with brush and gradient masks add under 40 ms to a 2560 by 1440 preview.
  - Commit: `"core: the develop local masking engine and local adjustment sets"`
- **Proof:** unit proof: `DevelopMaskTests` (combine truth tables, rasters at two scales agree after resampling within 1/255, auto mask leaks under 1 percent across the hard edge of a committed fixture), `LocalAdjustmentTests` (a +1 EV local exposure under a full mask equals the global stage within 1e-5); cheaper substitute that fails: storing masks as preview-resolution bitmaps, which the two-scale agreement test catches.

#### §5. Spot removal, red eye, and pet eye

- **Deliverable:** Heal, clone, and content-aware remove spots stored as develop data, a visualize-spots view, and red and pet eye correction, on the healing solver and red-eye detector moved into Isotone.Core.
- **Depends On:** §1
- **Phase:** 23
- **Surface:** no surface of its own (the spot and red-eye tools are D03 T15 §1)
- **Runs:** none
- **Catalog:** IP-1440 to IP-1442 (3 features)
- **Hints:**
  - Move first: the healing solver and red-eye detector `D03 T13 §2` built in `src/Gesso/Isotone.Gesso.Core/Retouch/` into `src/Isotone.Core/Imaging/Retouch/` as their second consumer, Gesso's healing and red-eye tools repointed; a grep finds one `class HealingSolver` and one red-eye detector (reconcile the type names with `D03 T13 §2` as authored).
  - `SpotOperation` (IP-1440): mode Heal, Clone, or Remove; shape circle or brush path; source offset; size, feather, and opacity; stored in `DevelopSettings.Spots` in normalized coordinates and applied after the §3 geometry so a corrected image heals where the user clicked.
  - Auto source: the lowest sum-of-squared-differences patch in a ring around the target on downscaled luminance, excluding other spots; a dragged source is kept.
  - Heal: membrane interpolation of the boundary difference (Farbman et al. 2009), the same solver as Gesso's healing brush.
  - Remove: an `IContentAwareFillProvider` seam in Isotone.Core; Gesso registers the PatchMatch engine of `D03 T13 §3` (which stays in Gesso by decision); with no provider (Albumen today) Remove falls back to Heal and the result says so.
  - Visualize spots (IP-1441): an inverted high-pass edge map with a threshold, a view output only.
  - Red eye and pet eye (IP-1442): detection in a user box by redness ratio (red eye) or bright low-saturation and green-yellow reflection (pet eye); pupil size, darken, and an added catchlight for pet eye.
  - Commit: `"core: develop spot removal and red and pet eye on the shared healing solver"`
- **Proof:** unit and golden proof: `SpotHealTests` heal a committed dust fixture from a fixed source to within 3/255 mean of its clean golden; `RedEyeTests` bring red pixels in the pupil below 2 percent; the single-definition grep passes; cheaper substitute that fails: blurring the spot, which the clean-golden comparison catches.

#### §6. Presets, snapshots, and XMP settings exchange

- **Deliverable:** Develop presets with amount and groups in a suite-wide folder, built-in Isotone looks, mask presets, snapshots, copy and paste, per-camera raw defaults, the Isotone.Core XMP packet core, and Camera Raw `crs` XMP read and write that preserves every field it cannot map.
- **Depends On:** §1
- **Phase:** 23
- **Surface:** no surface of its own (the presets and snapshots panels are D03 T15 §1 and §2)
- **Runs:** none
- **Catalog:** IP-1443 to IP-1449 (7 features)
- **Hints:**
  - `src/Isotone.Core/Metadata/Xmp/XmpPacket.cs`: an RDF/XML reader and writer (XMP Specification Part 1 2012, `x:xmpmeta` wrapper, packet padding) that keeps unknown namespaces verbatim; this file is its first consumer, `D03 T17 §10` and Albumen's `D04 T01 §11` its next.
  - `DevelopPreset` (IP-1443, IP-1444): named partial settings by group with an amount (0 to 200 percent scaling deltas from defaults) and support flags (RAW only, color, black and white) for filtering, stored as JSON in `%LOCALAPPDATA%\Rizonesoft\Isotone\Develop\Presets\`, one app-wide folder shared by Gesso and Albumen; create, import, and export as XMP.
  - `CrsSettingsMap`: read and write `crs:` for the 2012 process set (Exposure2012 through Blacks2012, Texture, Clarity2012, Dehaze, Vibrance, Saturation, Temperature, Tint, the HSL bands, ColorGrade and SplitToning fields, the parametric and PV2012 point curves, Sharpness, SharpenRadius, SharpenDetail, SharpenEdgeMasking, LuminanceSmoothing, ColorNoiseReduction, PostCropVignette and Grain fields, lens and upright switches), mapping numbers through documented curves because the process differs, so a preset carries intent, not identical pixels.
  - Unmapped crs fields are kept and written back unchanged, and the import returns a report ("12 settings have no Isotone equivalent"); Isotone's full settings also write as `isotone-develop:` XMP beside `crs:` so Gesso and Albumen round-trip losslessly.
  - Built-in looks (IP-1445): Isotone's own groups (Portrait, Landscape, Black and White, Vintage, Cinematic, Matte) as JSON in `Isotone.Core/Develop/Presets/Builtin/`; no Adobe preset content is bundled.
  - Mask presets (IP-1446): a `LocalAdjustmentSet` saved without its geometry; recommended presets arrive later through `D03 T19 §10`.
  - Snapshots (IP-1447): named `DevelopSnapshot` records with add, delete, rename, and a per-group diff for compare.
  - Copy and paste (IP-1448): `DevelopClipboard` with a group checklist, paste merging only the chosen groups; reset per group and all.
  - Raw defaults per camera (IP-1449): keyed by make and model (serial optional) in `Isotone.Develop.RawDefaults`, applied when a RAW source first develops, with a reset.
  - Commit: `"core: develop presets, snapshots, and Camera Raw XMP exchange"`
- **Proof:** format fidelity proof: committed crs preset fixtures (authored for the tests, generator recorded, no Adobe content) read into settings and write back with every unmapped field equal after canonical XML; `XmpPacketTests` round-trip packets extracted by exiftool 13 (`-xmp -b`) byte-equivalent after canonicalization; `PresetAmountTests` assert 50 percent halves each delta; cheaper substitute that fails: reading only mapped fields, which the unmapped-field round trip catches.

### todo/03-gesso/TODO-16-gesso-parity-type-vector.md -- `gesso-parity-type-vector`

- **Title:** "TODO-16 -- Gesso Parity: Type, Paths, Shapes, and Vector Layers"
- **Phase(s):** 24
- **Goal:** A Gesso user sets live point, paragraph, and frame text in any script with full character, paragraph, OpenType, and style control, draws and edits paths with the pen family, keeps a Paths panel with clipping paths and path booleans, and builds live shapes, GIMP-style vector layers, and frames, exporting them as SVG; everything stays editable until the user rasterizes. The code is the suite's, not a copy: §1 to §4 move the Stilus text engine, rich-text model, fonts, composers, styles, spell checking, and type panels (`D02 T10 §1` to `§13`) into `src/Isotone.Core/Text/` and `src/Isotone.UI/Text/`, and §5 to §7 move path geometry, booleans, node editing, and live-shape generators (`D02 T08 §1`, `§4`, `§6`, `§7`, `§10`) into `src/Isotone.Core/Vector/`, with Gesso-specific layers in `src/Gesso/Isotone.Gesso.Core/Layers/` and tools in `src/Gesso/Isotone.Gesso.Desktop/Tools/`. Text, shape, vector, and frame layers persist through the `D03 T08 §1` contract as `gesso:` elements beside a rendered PNG, paths as `gesso:paths`; every edit is one undoable command with one Serilog Information line.
- **Current-state facts to verify (with claim candidates):**
  - Gesso's `TextLayer` is a flat single-style model (one font family defaulting to Segoe UI, one size, one color) with no runs, shaping, or paragraphs. `<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/TextLayer.cs = 118 -->` `<!-- claim: count "_fontFamily = .Segoe UI." src/Gesso/src/Gesso.Core/Layers/TextLayer.cs = 1 -->`
  - Gesso's `ShapeLayer` names eight fixed shape kinds and holds no path geometry of its own. `<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/ShapeLayer.cs = 92 -->` `<!-- claim: count "^    RoundedRectangle$" src/Gesso/src/Gesso.Core/Layers/ShapeLayer.cs = 1 -->`
  - Gesso's vector mask keeps its own segment list type, which §5 re-bases on the shared geometry so one path type remains. `<!-- claim: lines src/Gesso/src/Gesso.Core/Masks/VectorMask.cs = 291 -->` `<!-- claim: count "class VectorPathSegment" src/Gesso/src/Gesso.Core/Masks/VectorMask.cs = 1 -->`
  - No shaping package is referenced and Stilus has no text folder yet; `D02 T10 §1` adds both before this file runs. `<!-- claim: count "HarfBuzz" Directory.Packages.props = 0 -->` `<!-- claim: absent src/Stilus/Bezier.Core/Text -->`
  - Stilus's path booleans and SVG reader live today in two services that §5 moves after the Stilus parity sections extend them. `<!-- claim: lines src/Stilus/Bezier.Core/Services/PathOperationsService.cs = 351 -->` `<!-- claim: lines src/Stilus/Bezier.Core/Services/SvgParser.cs = 907 -->`
  - The backlog entries this file promotes still exist. `<!-- claim: count "B-018\] Text layers" todo/backlog.md = 1 -->` `<!-- claim: count "B-019\] Shape layers and vector tools" todo/backlog.md = 1 -->`
- **Inputs and XREFs:** `standards/gesso.md`, `standards/shared.md`; Unicode 16.0 UAX #9, #14, #24 (moved conformance suites); OpenType 1.9.1 (GSUB, GPOS, fvar, STAT, COLR v1, SVG, name IDs 16 and 17); HarfBuzz 10.x `hb-shape` and `hb-view` goldens; W3C SVG 2 path data; Adobe Photoshop File Formats Specification (text engine data and vector mask blocks referenced for later PSD mapping); Adobe Illustrator File Format Specification v7 (the paths-only Illustrator 3 subset Photoshop exports); Schneider 1990 (Graphics Gems curve fitting); Microsoft Learn Windows Spell Checking API; TeX hyph-utf8 patterns (licenses per file); Inkscape 1.4 and resvg 0.45 as SVG render oracles; GIMP 3.2.6 as the vector layer and text behavior reference; -> XREF: D02 T10 §1 (the engine §1 moves); -> XREF: D02 T10 §2 (the rich-text model and edit session §1 moves); -> XREF: D02 T10 §3, D02 T10 §4, D02 T10 §5 (fonts, character formatting, OpenType, glyphs code §2 moves); -> XREF: D02 T10 §6, D02 T10 §7, D02 T10 §8 (composers, hyphenation, lists, frames §3 moves); -> XREF: D02 T10 §9, D02 T10 §10, D02 T10 §11, D02 T10 §12, D02 T10 §13 (path text, CJK composer, search, styles, spell checking §4 moves); -> XREF: D02 T08 §1, D02 T08 §6, D02 T08 §7 (pen math and node operations §6 moves); -> XREF: D02 T08 §4 (live-shape generators §7 moves); -> XREF: D02 T08 §10 (path geometry and booleans §5 moves); -> XREF: D02 T14 §1 (SVG export options §8 shares); -> XREF: D02 T14 §4 (Stilus's legacy AI reader, the read-back oracle for §5's Illustrator paths); -> XREF: D03 T08 §1 (the native-format contract every layer kind here registers with); -> XREF: D03 T08 §4 (snapping for pen and shape tools); -> XREF: D03 T09 §1 (text, shape, vector, and frame layer kinds); -> XREF: D03 T09 §4 (vector masks re-based on §5's geometry); -> XREF: D03 T09 §9 (frame content as smart objects); -> XREF: D03 T10 §1 (path to and from selection; type mask output); -> XREF: D03 T10 §5 (intelligent scissors engine for the magnetic pen and content-aware tracing); -> XREF: D03 T12 §8 (fill and stroke path engine); -> XREF: D03 T12 §9, D03 T12 §10 (gradient and pattern paint for shapes and text outline); -> XREF: D03 T13 §5 (transform handles for paths); -> XREF: D03 T13 §6 (warp envelope math for warp text); -> XREF: D03 T17 §3, D03 T17 §13 (PSD text, shape, and vector mask mapping); -> XREF: D03 T17 §4 (XCF text and vector layers map onto §1 and §7); -> XREF: D03 T17 §7 (moves only the SVG renderer, since §5 moves the reader); -> XREF: D03 T17 §11 (clipping paths written into JPEG and TIFF); -> XREF: D03 T19 §11 (match font on §2's font list); -> XREF: D01 T05 §5 (brand kit type styles shown in §4's styles panels); -> XREF: D03 T20 §4 (type preferences surface the `Gesso.Type.*` keys); backlog B-018 (`legacy-gesso-4.8`) promoted into §1 and B-019 (`legacy-gesso-4.7`) promoted into §7, each deleted from `todo/backlog.md` in the authoring commit.
- **Adjacency:** list=applicable (Paths panel, Shapes panel, Glyphs panel search, font list filters and favorites, character and paragraph styles panels); document=not-applicable (this file prints nothing; print is D03 T18 §6); settings=applicable (`Gesso.Type.*`, `Gesso.Paths.*`, `Gesso.Shapes.*`, each with a default and a named consumer); reporting=applicable (the missing-fonts report and spelling results, §4); notifications=applicable (font list refresh progress and SVG export completion); permissions=applicable (restricted-embedding fonts, unreadable CSH or SVG files, and locked layers are refused by name); audit=applicable (every command is one history entry with one Serilog Information line); exchange=applicable (SVG path import and export, Illustrator paths export, CSH import, copy SVG and CSS); reverse=applicable (every command undoable, rasterize included)

#### §1. Text layers on the shared text engine

- **Deliverable:** Live point and paragraph text layers in any script, created by the four type tools and edited on canvas, rendered by the HarfBuzz engine and rich-text model moved from Stilus into `Isotone.Core/Text/`, persisted as `gesso:text` with a pixel fallback. -> SOURCE: legacy-gesso-4.8
- **Depends On:** D02 T10 §1, D03 T09 §1
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/type/. Job: a designer can add live text in Latin, Arabic, Devanagari, or CJK, edit it on the canvas, and keep it editable until rasterizing. Treatment: the type tool group (horizontal, vertical, horizontal mask, vertical mask; T cycles), click for point text or drag a paragraph box (GIMP dynamic or fixed box), an on-canvas editor with caret, selection, IME underline, commit (Ctrl+Enter or the check) and cancel (Esc), transform handles while editing, GIMP's floating style editor, and a Text Editor window. Cheaper substitute that fails: a modal text dialog that stamps a bitmap. Chrome: consume the moved engine, the tool options strip of `D03 T03 §4`, `Isotone.UI` dialog styles, and the suite history; do not add a second shaper or text model.
- **Runs:** `Requires: display-session -- typing into a layer, IME composition, and the captures need an interactive desktop`
- **Catalog:** IP-1582 to IP-1591 (10 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-4.8` (promotes B-018); delete the B-018 line in the authoring commit.
  - Move first: `src/Stilus/Isotone.Stilus.Core/Text/` Unicode, Shaping, Fonts (`FontCatalog`, `FontFaceInfo` cache, `FontFallbackChain`), Layout (`TextLayoutEngine`), and the story model and `TextEditSession` of `D02 T10 §2` into `src/Isotone.Core/Text/`, tests to `tests/Isotone.Core.Tests/Text/`, `TextInputBridge` to `src/Isotone.UI/Text/`, HarfBuzzSharp and SkiaSharp.HarfBuzz referenced from Isotone.Core, Stilus repointed, the decisions row updated (the move trigger fired), and the font cache moved to `%LOCALAPPDATA%\Rizonesoft\Isotone\FontCache\`; a grep finds one `class TextShaper` and one `class TextLayoutEngine`.
  - Rewrite `src/Gesso/Isotone.Gesso.Core/Layers/TextLayer.cs` over `Isotone.Core.Text.Model.TextStory` (runs of character attributes, paragraphs), `TextKind` Point or Paragraph (box size, GIMP dynamic or fixed), orientation horizontal or vertical (mixed or upright, vertical Roman alignment; IP-1585), transform, and anti-aliasing; tiles re-render from the layout only when story or transform change (IP-1582, IP-1584).
  - Native format: `gesso:text` (story as XML runs, schema version) beside the rendered PNG per `D03 T08 §1`, so GIMP and Krita see pixels and Gesso restores live text.
  - Tools in `src/Gesso/Isotone.Gesso.Desktop/Tools/Type/`: `HorizontalTypeTool`, `VerticalTypeTool`, `HorizontalTypeMaskTool`, `VerticalTypeMaskTool`; mask tools produce a `D03 T10 §1` selection from the glyph outlines, never a layer (IP-1586); a toggle-orientation command.
  - On-canvas editing (IP-1583, IP-1587): double-click a text layer or its Layers-panel thumbnail, caret and selection through the moved `TextEditSession`, commit or cancel, transform while editing, masked text layers stay clickable by layer-bounds hit test, GIMP's floating style editor as a draggable, toggleable overlay (`Gesso.Type.ShowOnCanvasEditor`).
  - Text Editor window (IP-1588): multi-line editing with load from file (UTF-8 and UTF-16) and clear all.
  - Convert to work path or shape layer (IP-1589): glyph outlines from shaped glyph ids through `SKFont.GetGlyphPath` into `Isotone.Core/Vector/PathGeometry`; the command appears here disabled with tooltips naming §5 (work path) and §7 (shape layer), which enable it.
  - Rasterize type layer (IP-1590) as one undo step "Rasterize Type"; world-ready option (IP-1591) `Gesso.Type.TextEngine` (East Asian or World-Ready) choosing which panel feature sets show, while one engine shapes every script.
  - Undo names "Add Text Layer" and "Edit Text"; Serilog line `Text layer {Id} committed ({Chars} chars, {Runs} runs)`; budget 16 ms per keystroke in a 2,000-character paragraph at 300 ppi.
  - Commit: `"gesso: live text layers on the HarfBuzz engine moved to Isotone.Core"`
- **Proof:** unit, format fidelity, and driven proof: the moved `ShaperGoldenTests` and conformance suites pass from `tests/Isotone.Core.Tests/Text/`, `TextLayerRenderTests` render the Arabic and Devanagari fixtures within 1/255 of the Stilus render of the same story, a saved `.gesso` reopens its text live and GIMP 3.2 `gimp-console` opens the renamed `.ora` with the fallback within 1/255, and a driven typing run is captured; cheaper substitute that fails: a Gesso-local `DrawText` path, which the one-definition grep and the Arabic golden catch.

#### §5. Paths, the Paths panel, and path geometry in Isotone.Core

- **Deliverable:** Work and saved paths in the document with the Paths panel, clipping paths, fill and stroke path, path to and from selection, path operations, and SVG and Illustrator path exchange, on path geometry and the SVG reader moved from Stilus into `Isotone.Core/Vector/`.
- **Depends On:** D02 T08 §10, D03 T10 §1
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/paths-panel/. Job: a retoucher can keep, name, and reuse precise outlines as selections, strokes, fills, and clipping paths. Treatment: a Paths panel (work path in italics, thumbnails, rename in place, multi-select, color tags, lock, visibility, panel options) merging GIMP's Paths dialog, with context and panel menus for every command. Cheaper substitute that fails: paths kept only as vector masks. Chrome: consume the dock, the icon catalog, `D03 T10 §1` selections, `D03 T12 §8`'s fill and stroke engine, and the suite history.
- **Runs:** `Requires: display-session -- the Paths panel drive and captures need an interactive desktop`
- **Catalog:** IP-1637 to IP-1655 (19 features)
- **Hints:**
  - Move first: the path model, `PlanarFaces`, and the boolean service of `D02 T08 §10` (and `PathOperationsService`'s geometry) into `src/Isotone.Core/Vector/` as `PathGeometry`, `PathFigure`, cubic `BezierSegment` in double precision, `PathBooleans`, `PlanarFaces`, and `SvgPathData` (parse and format), tests to `tests/Isotone.Core.Tests/Vector/`, Stilus repointed; re-base Gesso's `VectorMask` and `VectorPathSegment` on `PathGeometry` so a grep finds one path type.
  - Also move the Stilus SVG document reader to `src/Isotone.Core/Vector/Svg/` here, one phase before `D03 T17 §7` (which then moves only the renderer), because SVG path import (IP-1638, IP-1652) needs it now.
  - `GessoPathSet` document part: one work path, saved paths with name, color tag, lock, and visibility (IP-1643), and a clipping-path flag with flatness (IP-1648); persisted as `gesso:paths` (SVG path data per path) through `D03 T08 §1`.
  - `src/Gesso/Isotone.Gesso.Desktop/Views/Panels/PathsPanel.xaml` (IP-1641, IP-1655): thumbnails, rename, deselect, multi-select, panel options, show target path (IP-1637).
  - Management (IP-1642, IP-1650, IP-1651): new, save work path, duplicate, delete, raise, lower, merge visible paths, copy and paste between images as an internal flavor plus SVG text.
  - Fill and stroke path (IP-1644, IP-1645): call `D03 T12 §8` with color, pattern, or history source; stroke with a painting tool along the flattened path with simulated pressure tapers, or with a line style.
  - Path to selection (IP-1646) with replace, add, subtract, intersect, feather, and anti-alias; selection to path (IP-1647) by marching squares on the mask then Schneider fitting with tolerance and GIMP's advanced settings (corner threshold, line and curve error).
  - Path operations (IP-1653): combine, subtract front, intersect, exclude, merge components on `PathBooleans`; align, distribute, and arrange components (IP-1654).
  - SVG (IP-1638, IP-1652): import merged or separate with scale to fit the image, export selected or all paths.
  - Illustrator export (IP-1639, IP-1649): one writer for both rows, a PostScript Illustrator 3 path file (the paths-only subset of the Illustrator File Format Specification v7) with the canvas as crop marks.
  - Clipping on export (IP-1640): a top-level clipping flag that `D03 T17 §11`'s JPEG and TIFF writers turn into a clipping path resource.
  - Undo names "New Path", "Save Path", "Stroke Path", "Fill Path", "Make Selection", "Make Work Path"; one Serilog line each.
  - Commit: `"gesso: paths and the Paths panel on path geometry moved to Isotone.Core"`
- **Proof:** unit and format fidelity proof: the moved `PathBooleansTests` pass from `tests/Isotone.Core.Tests/Vector/`, `SelectionToPathTests` fit a circular selection within 0.5 px using at most eight segments, exported SVG paths re-import through Inkscape 1.4 within 0.01 px, and the Illustrator path file reads back through Stilus's `D02 T14 §4` legacy AI reader with equal geometry; cheaper substitute that fails: a second Gesso path type, which the one-path-type grep catches.

#### §2. Character formatting, OpenType, glyphs, and fonts

- **Deliverable:** The Character panel, font list, OpenType and variable font controls, color fonts, the Glyphs panel, glyph protection, and the non-destructive text outline, on font, feature, and panel code moved from Stilus into `Isotone.Core/Text/` and `Isotone.UI/Text/`.
- **Depends On:** §1
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/character-panel/ and docs/captures/gesso/glyphs-panel/. Job: a designer sets every character attribute, OpenType feature, and font on one or many text layers. Treatment: the Character panel with toggles and reset, the font picker with filters, favorites, similar fonts, and preview size, a Fonts dialog in grid and list, the OpenType submenu and on-canvas alternates, variable axis sliders, and a Glyphs panel. Cheaper substitute that fails: a font combo box with bold and italic toggles only. Chrome: consume the moved `CharacterPanel`, `OpenTypePanel`, `GlyphsPanel`, and `FontPicker` from `Isotone.UI/Text/`; do not fork them.
- **Runs:** `Requires: display-session -- the panels and on-canvas alternates need an interactive desktop`
- **Catalog:** IP-1592 to IP-1610 (19 features)
- **Hints:**
  - Move first: `FontFilter` and `FontSubstitutionService` (`D02 T10 §3`), `OpticalKerner` and `FontFeatureSet` (`D02 T10 §4`, `§5`), `GlyphSnapProvider`, and the view models and XAML of `CharacterPanel`, `OpenTypePanel`, `GlyphsPanel`, and `FontPicker` into `src/Isotone.Core/Text/` and `src/Isotone.UI/Text/`, each app binding through an `ITextFormattingTarget` adapter; Stilus repointed; one definition each.
  - Character panel (IP-1592, IP-1610): family, style, size, leading, kerning metrics, optical, or manual, tracking (IP-1595, GIMP line and letter spacing), vertical and horizontal scale and baseline shift (IP-1596), float-precision color with live preview (IP-1597), panel toggles, and reset.
  - Styles and case (IP-1598): faux bold and italic, all caps, small caps, superscript, subscript, underline, strikethrough; faux only when the family lacks the face.
  - Rendering (IP-1599, IP-1600): anti-aliasing None, Sharp, Crisp, Strong, Smooth and hinting mapped to `SKFontEdging` and `SKFontHinting`, fractional widths, system layout, no break; language dictionary per run (IP-1601).
  - True face grouping (IP-1593) by typographic family and subfamily (name IDs 16 and 17); a change on several selected text layers is one compound undo step (IP-1594).
  - Font menu and Fonts dialog (IP-1602, IP-1603): classification filters from PANOSE and OS/2, favorites, similar fonts by a local metrics distance (x-height, cap height, stem weight, width class; no cloud), preview size, grid and list, search, refresh font list, fast loading from the moved cache.
  - OpenType (IP-1604): feature buttons offered per font (liga, dlig, swsh, calt, ordn, frac, titl, ss01 to ss20, cv01 to cv99), the OpenType submenu, on-canvas alternates for the selected glyph; variable fonts (IP-1605) with fvar axis sliders and STAT named instances.
  - Color fonts and emoji (IP-1606): COLR v0 and v1, OpenType SVG, sbix and CBDT through Skia, ZWJ sequences composed by the shaper; Glyphs panel (IP-1607) with filters, recent glyphs, search by name or code point, zoom; glyph protection (IP-1608) `Gesso.Type.GlyphProtection` from the moved missing-glyph logic.
  - Text outline (IP-1609): non-destructive fill, outline, or both, direction inside, center, or outside, color or pattern, width, caps, joins, miter, dashes, stored in `gesso:text`, with the `StrokeStyle` record §7 shares.
  - Settings `Gesso.Type.DefaultAntiAlias`, `Gesso.Type.FontPreviewSize`, `Gesso.Type.Units` with named consumers.
  - Commit: `"gesso: character formatting, OpenType, glyphs, and fonts on the shared type panels"`
- **Proof:** unit and golden proof: `CharacterFormattingTests` render each attribute on the Latin fixture within 1/255 of goldens, `FontGroupingTests` group committed OFL families into true faces, and `VariableFontTests` render three axis settings of an OFL variable font within 1/255 of `hb-view` (HarfBuzz 10) output; cheaper substitute that fails: faux bold and italic for every family, which the true-face test catches.

#### §3. Paragraph formatting and text frames

- **Deliverable:** The Paragraph panel with alignment, indents, spacing, hyphenation, justification and composers, hanging punctuation, lists, and Affinity frame text with vertical alignment, on composer and paragraph code moved from Stilus.
- **Depends On:** §1
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/paragraph-panel/. Job: a designer sets paragraph layout on text layers as in a layout tool. Treatment: the moved `ParagraphPanel` with hyphenation and justification dialogs, bullets and numbering, and the frame text tool. Cheaper substitute that fails: left, center, right buttons only. Chrome: consume `Isotone.UI/Text/` panels and the history.
- **Runs:** `Requires: display-session -- the panel and frame text tool need an interactive desktop`
- **Catalog:** IP-1611 to IP-1618 (8 features)
- **Hints:**
  - Move first: `Hyphenator` with its TeX pattern files (`D02 T10 §6`), `Composer`, `ProtrusionTable`, `ListAttributes` (`D02 T10 §7`), `TextFrame` (`D02 T10 §8`), and `ParagraphPanel.xaml` into `Isotone.Core/Text/` and `Isotone.UI/Text/`; one definition each.
  - Paragraph panel (IP-1611, IP-1612, IP-1618): align left, center, right, justify last left, center, right, justify all; left, right, and first-line indents; space before and after; reset.
  - Hyphenation (IP-1613): on or off, words longer than, after first, before last, limit, zone, capitalized words, per language from the moved patterns.
  - Justification and composers (IP-1614): word, letter, and glyph spacing minimum, desired, maximum; auto leading; single-line, every-line (Knuth and Plass), and world-ready composers.
  - Roman hanging punctuation (IP-1615) through `ProtrusionTable`; bulleted and numbered lists with nesting (IP-1616).
  - Frame text tool (IP-1617): Affinity frame text as paragraph text with vertical alignment top, center, bottom, and justify, sharing the list attributes.
  - All attributes serialize inside `gesso:text` paragraphs.
  - Commit: `"gesso: paragraph formatting, composers, lists, and frame text"`
- **Proof:** unit and golden proof: `ComposerTests` break the committed paragraph at the same points as the Stilus goldens for both composers, `HyphenationTests` pass the pattern fixtures, and paragraph renders match goldens within 1/255; cheaper substitute that fails: greedy breaking under the every-line composer, which the Knuth and Plass break test catches.

#### §4. Type styles and text commands

- **Deliverable:** Character and paragraph styles, find and replace, spell checking with user dictionaries, type on a path, warp text, point and paragraph conversion, placeholder text, missing-font replacement, and East Asian and right-to-left options, on search, style, spell, CJK, and path-text code moved from Stilus.
- **Depends On:** §2, §3, §5
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/type-styles/ and docs/captures/gesso/warp-text/. Job: a designer keeps type consistent across layers and bends it onto paths and shapes. Treatment: character and paragraph styles panels, Find and Replace and Check Spelling dialogs, the Warp Text dialog, the missing fonts dialog, and type-on-path handles. Cheaper substitute that fails: warp by rasterizing the text. Chrome: consume the moved panels and services; do not add a second spell checker.
- **Runs:** `Requires: display-session -- the dialogs, path handles, and captures need an interactive desktop`
- **Catalog:** IP-1619 to IP-1634 (16 features)
- **Hints:**
  - Move first: `TextSearchService` (`D02 T10 §11`), `Text/Styles/` (`D02 T10 §12`), `ISpellCheckService` to Isotone.Core and `WindowsSpellCheckService` to Isotone.UI (`D02 T10 §13`), `JapaneseComposer` with its presets (`D02 T10 §10`), and `PathTextLayout` (`D02 T10 §9`).
  - Spelling (IP-1619, IP-1626, IP-1634): the Windows Spell Checking API per run language, plus user word lists from `Gesso.Type.UserDictionaryFolder`; a missing language is refused by name.
  - Find and replace (IP-1620, IP-1625) across every text layer with case and whole word, one compound undo step.
  - Type on a path (IP-1621, IP-1631): on an open path or inside a closed shape (§5 paths, §7 shapes), flip, start and end markers, edit path; text to path command.
  - Point and paragraph conversion (IP-1622); placeholder text (IP-1623) with `Gesso.Type.FillNewWithPlaceholder` and Paste Lorem Ipsum.
  - Styles (IP-1624, IP-1633): character and paragraph styles panels with options, redefine, clear override, load from another `.gesso` or PSD, default styles; brand kit type styles (`D01 T05 §5`) shown as a read-only group.
  - Missing fonts (IP-1627): an open report and replacement with installed fonts only through `FontSubstitutionService`, update all text layers; no Adobe Fonts activation.
  - East Asian (IP-1628): tsume, kinsoku hard and soft, mojikumi through `JapaneseComposer`; right-to-left (IP-1629): paragraph direction, digit shapes (Arabic, Hindi, Farsi), diacritic position, kashida.
  - Warp text (IP-1630): arc, arc lower, arc upper, arch, bulge, shell lower and upper, flag, wave, fish, rise, fisheye, inflate, squeeze, twist with bend and distortions, on `D03 T13 §6`'s envelope math, stored live in `gesso:text`.
  - Dynamic text presets (IP-1632): path-text presets with spacing, position, direction, dynamic fit, and on-canvas endpoint handles.
  - Commit: `"gesso: type styles, spelling, find and replace, type on a path, and warp text"`
- **Proof:** unit and golden proof: `FindReplaceTests`, `SpellCheckTests` (skipping with the language name where the Windows dictionary is absent), `PathTextTests` within 1/255 of the Stilus render of the same story, and `WarpTextTests` asserting the text stays editable after warp and the render matches `D03 T13 §6`'s envelope applied to the outlines within 1/255; cheaper substitute that fails: warping rasterized text, which the still-editable assertion catches.

#### §6. Pen and path editing tools

- **Deliverable:** The pen family (pen, freeform, magnetic, curvature, content-aware tracing), anchor tools, curve actions, path and direct selection, and pen output modes, on node-editing math moved from Stilus into `Isotone.Core/Vector/Editing/`.
- **Depends On:** §5
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/pen-tools/. Job: a retoucher draws exact outlines and edits their anchors. Treatment: the pen tool group with GIMP Paths tool modes and Affinity pen and node behavior, options for output mode, rubber band, and snapping, and on-canvas anchor and handle editing. Cheaper substitute that fails: a polygon-only path tool. Chrome: consume `D03 T08 §4` snapping, `D03 T10 §5`'s scissors engine, `D03 T13 §5` transform handles, and the history.
- **Runs:** `Requires: display-session -- drawing and editing paths need an interactive desktop`
- **Catalog:** IP-1656 to IP-1672 (17 features)
- **Hints:**
  - Move first: pen anchor placement and handle constraints from `D02 T08 §1` `PenTool` and node operations from `D02 T08 §6` and `§7` (`PathEditCommand`, the node parts of `PathOperationsService`) into `src/Isotone.Core/Vector/Editing/PathEditor.cs` over `PathGeometry`; Stilus tools call it.
  - Pen tool (IP-1656): Bezier anchors, close and continue, Ctrl direct select, Alt convert, Shift 45-degree constraint, add subpaths to selected curves; GIMP modes design, edit, and move with their modifiers (IP-1657); smart, polygon, and line modes (IP-1658).
  - Freeform pen with curve fit (IP-1659) through §5's Schneider fitting; magnetic pen (IP-1660) with width, contrast, frequency, and pressure on `D03 T10 §5`'s live-wire engine; curvature pen (IP-1661); content-aware tracing (IP-1662) from the same engine's edges with a detail slider, classical, no model.
  - Anchor tools (IP-1663): add, delete, convert with auto add and delete and sharp, smooth, and smart node types; curve actions (IP-1664): split, break, close, join, reverse, smooth, shift start, delete segment.
  - Output (IP-1665, IP-1666): shape layer, path, or pixels with line style and fill while drawing; make selection or shape from the options.
  - Display (IP-1667, IP-1668): rubber band, `Gesso.Paths.Thickness`, `Gesso.Paths.Color`, direction indicator.
  - Pixel grid (IP-1669): align vector edges and snap to the pixel grid on create and transform; snapping options (IP-1670) through `D03 T08 §4`.
  - Path and direct selection (IP-1671) with layer scope, marquee, Alt-drag duplicate, transform controls (Affinity Node tool merged); transform path and selected anchors (IP-1672) with `D03 T13 §5` handles.
  - One undo step per gesture with a named command; Serilog line per committed path.
  - Commit: `"gesso: the pen family and path editing on node math moved to Isotone.Core"`
- **Proof:** unit and driven proof: the moved `PathEditorTests` pass, `PenToolTests` replay scripted gestures into expected geometry, `MagneticPenTests` follow a committed edge fixture within 1.5 px, and a driven drawing session is captured; cheaper substitute that fails: a Gesso-only pen editing `VectorPathSegment` lists, which the one-path-type grep catches.

#### §7. Shape layers, shape tools, and vector layers

- **Deliverable:** Live shape layers from every shape tool with per-corner radii, custom shapes, fill and stroke paint, combine and merge, and GIMP 3.2 vector layers bound to paths, persisted as `gesso:shape` and `gesso:vector`. -> SOURCE: legacy-gesso-4.7
- **Depends On:** §5, D03 T09 §4
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/shapes/ and docs/captures/gesso/vector-layers/. Job: a designer draws resolution-independent shapes and vector layers that stay editable. Treatment: the shape tool group with on-canvas corner widgets, the Shapes panel, live shape properties in the Properties panel, fill and stroke paint pickers with stroke presets, and GIMP-style vector layer options. Cheaper substitute that fails: shapes rasterized at creation. Chrome: consume §5 geometry, `D03 T12 §9` gradients, `D03 T12 §10` patterns, the Properties panel, and the history.
- **Runs:** `Requires: display-session -- the shape tools and captures need an interactive desktop`
- **Catalog:** IP-1673 to IP-1696 (24 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-4.7` (promotes B-019); delete the B-019 line in the authoring commit.
  - Move first: live-shape generators and the corner model of `D02 T08 §4` (`LiveShape`: rounded, concave, straight, cutout, absolute or relative radii) into `src/Isotone.Core/Vector/Shapes/`.
  - Rewrite `ShapeLayer` over `PathGeometry` plus an optional `LiveShapeSpec`; persist `gesso:shape` with the PNG fallback (IP-1676).
  - Tools (IP-1679 to IP-1683): rectangle and ellipse with per-corner radius and on-canvas widgets, corner types (IP-1680), triangle, polygon and star (sides, ratio, smooth indents and corners), line with weight and arrowheads; Affinity extras (IP-1685): rounded rectangle, star variants, diamond, trapezoid, cog, crescent, donut, pie, tear, heart, cloud, callouts, arrow.
  - Custom shapes (IP-1673, IP-1674, IP-1684, IP-1696): Shapes panel with Isotone's own set, define custom shape from a path, the legacy shape tool option, CSH import from the user's files only (reader built from the published reverse-engineered layout named in the decisions row; unknown versions refused by name).
  - Paint (IP-1686): solid, gradient, pattern, or none with gradient and pattern options; stroke options (IP-1687): align inside, center, or outside, caps, corners, dashes, saved stroke presets as the `StrokeStyle` §2 shares.
  - Geometry (IP-1688): W, H, X, Y, drawing constraints, keep selected; live properties (IP-1689, IP-1695) with per-corner radii and shape operations, and conversion to a regular path.
  - Combine (IP-1678) as live operations in one layer through `PathBooleans`; merge shape layers (IP-1691); pixels mode (IP-1690); rasterize shape (IP-1692).
  - Vector layers (IP-1677, IP-1693, IP-1694): a `VectorLayer` kind (`D03 T09 §1`) bound to a saved path with fill and stroke (color or pattern, antialias, width, cap, join, miter, dashes), non-destructive transform, on-canvas editing with the §6 tools, and drop to fill; persisted `gesso:vector`.
  - Gfig (IP-1675): the job is met by these tools plus arc and spiral generators and grid snap; no gfig file reader.
  - Commit: `"gesso: live shape layers, custom shapes, and vector layers"`
- **Proof:** format fidelity and unit proof: shape and vector layers round-trip `.gesso` live and GIMP 3.2 renders the fallback within 1/255, `LiveShapeTests` match the moved Stilus corner goldens, and a driven capture of every tool is committed; cheaper substitute that fails: rasterizing on creation, which the reopen-live assertion catches.

#### §8. Frames and vector output

- **Deliverable:** Frame layers with placed content, SVG export of vector, text, and raster layers with options, and Copy SVG and Copy CSS from layers.
- **Depends On:** §7
- **Phase:** 24
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/frames/ and docs/captures/gesso/svg-export/. Job: a designer crops content into frames and hands vector work to the web. Treatment: the frame tool (rectangle and ellipse), Convert to Frame, frame or content selection with properties, an SVG export options page, and Copy SVG and Copy CSS in the layer menu. Cheaper substitute that fails: an SVG that embeds one flattened PNG. Chrome: consume §5's `SvgPathData`, `D03 T09 §9` smart objects, and the export options shell of `D03 T17 §1`.
- **Runs:** `Requires: display-session -- the frame tool and the export dialog need an interactive desktop`
- **Catalog:** IP-1697 to IP-1703 (7 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.FileFormats/Svg/GessoSvgExporter.cs` (IP-1697, IP-1700): vector and shape layers as paths, text as `<text>` spans or outlines, raster layers embedded as PNG or JPEG data or omitted, options for hex colors, flatten transforms, viewBox, and relative coordinates; move the `SvgExportOptions` record of `D02 T14 §1` to `src/Isotone.Core/Vector/Svg/` so both apps share its semantics.
  - Copy SVG and CSS (IP-1699, IP-1703): an `image/svg+xml` clipboard flavor and CSS text (size, position, colors, radii, gradients, box-shadow from mappable styles).
  - `FrameLayer` (IP-1698, IP-1701, IP-1702): a shape plus a content layer (a `D03 T09 §9` smart object), frame from layers, convert to frame, frame or content selection, properties stroke, W, H, X, Y, and placed-content status; persisted `gesso:frame`.
  - Undo names "Convert to Frame" and "Place in Frame"; Serilog line per SVG export.
  - Commit: `"gesso: frames and SVG export"`
- **Proof:** format fidelity proof: the exported SVG of the committed vector fixture renders in Inkscape 1.4 and resvg 0.45 within 1/255 of Gesso's render and contains one element per vector layer; cheaper substitute that fails: one embedded PNG, which the element-count assertion catches.

#### Sizing concerns

- §7 owns 24 features plus a move; if it overruns 25 items, split into shape tools and live shapes (IP-1673 to IP-1692, IP-1695, IP-1696) and GIMP vector layers with Gfig (IP-1677, IP-1693, IP-1694, IP-1675).
- §2 owns 19 features plus a four-part move; the natural split is formatting and fonts (IP-1592 to IP-1603) versus OpenType, variable, color fonts, glyphs, and text outline (IP-1604 to IP-1610).
- §5 owns 19 features plus two moves; the natural split is the Paths panel and path commands versus path exchange (SVG and Illustrator, IP-1638, IP-1639, IP-1649, IP-1652).

### todo/03-gesso/TODO-17-gesso-parity-formats.md -- `gesso-parity-formats`

- **Title:** "TODO-17 -- Gesso Parity: the File Menu and Every Format"
- **Phase(s):** 25
- **Goal:** Gesso's File menu does everything Photoshop, Affinity Photo, and GIMP do to get pixels in and out (open as, place embedded and linked, revert, close all, save a copy, a format matrix, export versus save semantics, clipboard, screenshots, scanners, URLs, archives), and it reads and writes every format those three apps carry: PSD and PSB with live adjustments, styles, text, and smart objects; GIMP XCF; WebP, AVIF, HEIF, JPEG XL, JPEG 2000, JPEG XR, and QOI; OpenEXR, Radiance, PFM, PNM, FITS, and DICOM; PDF, Photoshop PDF, EPS, SVG, WMF, and EMF; the long tail of legacy and resource formats; the full JPEG, PNG, and TIFF option sets; and EXIF, IPTC, and XMP metadata. Every codec registers with one `FormatRegistry` in `src/Gesso/Isotone.Gesso.FileFormats/`, shared codecs live in `src/Isotone.Core/Formats/`, `src/Isotone.Core/Pdf/`, and `src/Isotone.Core/Metadata/` (moved from Stilus on this second use, never copied), native libraries are the ones `docs/dev/decisions.md` records with GPL-3.0 checks, and every reader and writer owes a format fidelity proof against a named reference implementation. Opening never changes a file; saving goes through the atomic writer; what a format cannot carry is reported, never silently dropped.
- **Current-state facts to verify (with claim candidates):**
  - `Gesso.FileFormats` holds only the `IImageFormat` interface; no codec exists. `<!-- claim: lines src/Gesso/src/Gesso.FileFormats/IImageFormat.cs = 42 -->`
  - The File menu has New, Open, Save, Save As, Export, and Exit, with no Place, Revert, Close, Import, or Print. `<!-- claim: count "Header="(Place|Revert|Close|Print|Import)" src/Gesso/src/Gesso.UI/Views/MainWindow.xaml = 0 -->`
  - The open and export filters are hard-coded strings that already list WebP with no codec behind them, which §1's registry replaces. `<!-- claim: count "\*\.webp" src/Gesso/src/Gesso.UI/Services/IFileDialogService.cs = 2 -->`
  - The installer registers a `.psd` association and no Gesso fixture folder exists. `<!-- claim: count "\.psd" installer/Gesso.iss = 7 -->` `<!-- claim: absent tests/fixtures/gesso -->`
  - No PSD reader or writer exists anywhere yet; `D02 T14 §13` builds them and `D03 T04 §5` moves the reader. `<!-- claim: count "PsdReader|PsdWriter" src/Stilus/**/*.cs = 0 -->`
  - Backlog B-022 (more formats and PSD write) is still open for §5 to promote. `<!-- claim: count "B-022\] More formats" todo/backlog.md = 1 -->`
- **Inputs and XREFs:** `standards/gesso.md` (every codec owes a fidelity proof and says what it cannot carry); `standards/testing.md` (fixtures, goldens, the Fidelity trait); Adobe Photoshop File Formats Specification (current edition) with psd-tools 1.10 and GIMP 3.2.6 as reading oracles; GIMP `devel-docs/XCF.md` at the 3.2.6 tag with `gimp-console-3.2` as the golden oracle; OpenRaster; TIFF 6.0, BigTIFF, Adobe TIFF Technical Note 3 (floating-point predictor), and libtiff 4.7 `tiffinfo` and `tiffdump`; PNG Third Edition (W3C, with cICP, mDCV, cLLI) and `pngcheck` 3.0; JFIF 1.02, CIPA DC-008-2023 (Exif 3.0), ISO 21496-1 and Google Ultra HDR 1.1 gain maps; libwebp 1.5, libavif 1.2 with dav1d and libaom, libheif 1.19 with libde265 and x265, libjxl 0.11, OpenJPEG 2.5, OpenEXR 3.3, PDFium, libjpeg-turbo 3.1 and their CLIs as oracles; ISO 32000-2 (PDF 2.0), ISO 15930 (PDF/X-1a, X-3, X-4); Adobe EPS 3.0 (Technical Note 5002); MS-EMF and MS-WMF; DICOM PS3.5, PS3.10, PS3.15 (2025); FITS 4.0; IPTC Photo Metadata Standard 2024.1; XMP Specification Parts 1 to 3; exiftool 13, ImageMagick 7.1, OpenImageIO 3.0 `oiiotool`, dcmtk 3.6 `dcm2pnm`, DirectXTex `texconv`, Ghostscript 10.x, MuPDF `mutool draw` (test time only), Inkscape 1.4; -> XREF: D03 T04 §1 (the codec decision and the WIC codec it placed); -> XREF: D03 T04 §2, D03 T04 §3 (PNG, JPEG, TIFF readers and writers §11 extends); -> XREF: D03 T04 §4 (the native format and its atomic save); -> XREF: D03 T04 §5 (the PSD reader §2 and §3 extend); -> XREF: D03 T08 §1 (the contract live content maps onto); -> XREF: D03 T08 §5 (notes that PDF annotations import into); -> XREF: D03 T09 §5, D03 T09 §7, D03 T09 §8 (blending and styles written to and read from PSD); -> XREF: D03 T09 §9, D03 T09 §10 (smart objects for place, open as smart object, PSD smart objects, XCF link layers); -> XREF: D03 T09 §11 (comps in PSD); -> XREF: D03 T10 §6 (the guided filter that refines HEIC depth maps); -> XREF: D03 T10 §10 (alpha and spot channels in PSD and TIFF); -> XREF: D03 T11 §1 (adjustment layers in PSD); -> XREF: D03 T11 §4 (the OpenColorIO wrapper for EXR color spaces); -> XREF: D03 T11 §7 (image modes and indexed conversion); -> XREF: D03 T12 §3, D03 T12 §10 (GBR, GIH, and PAT readers §9 adds writers beside); -> XREF: D03 T14 §1 and D01 T06 §1 (XCF filter stacks as live filters through the GEGL op-id map); -> XREF: D03 T15 §4 (32-bit documents and HDR display for EXR, HDR, JPEG XR, and gain maps); -> XREF: D03 T15 §5 (auto-align for load into stack); -> XREF: D03 T15 §10 (astro stacking consumes FITS); -> XREF: D03 T15 §12 (editable EXIF in develop); -> XREF: D03 T16 §1, D03 T16 §5, D03 T16 §7 (text, paths with the moved SVG reader, and vector layers in PSD, XCF, TIFF, and PDF); -> XREF: D03 T18 §1 (Export As consumes the registry and every writer here); -> XREF: D03 T18 §4 (OCIO by filename and working spaces); -> XREF: D03 T18 §6 (consumes the printer marks renderer §7 moves); -> XREF: D03 T19 §1 (provenance written as XMP through §10); -> XREF: D01 T03 §2, D01 T03 §3 (mipmap resampling and indexed quantization); -> XREF: D01 T04 §1, D01 T04 §3 (profiles and CMYK buffers); -> XREF: D01 T07 §4 (HEIC depth maps become depth sources); -> XREF: D01 T07 §6 (the XMP packet core §10 consumes); -> XREF: D02 T13 §4 (printer marks §7 moves); -> XREF: D02 T13 §10 (the PostScript writer §7 moves for EPS); -> XREF: D02 T13 §14, D02 T13 §15, D02 T13 §16 (PDF writer, presets, and security §7 moves); -> XREF: D02 T14 §2 (PdfPig, which §1 and §7 reuse for annotations and text); -> XREF: D02 T14 §9 (the Ghostscript runner §7 moves); -> XREF: D02 T14 §11 (EMF and WMF code §7 moves); -> XREF: D02 T14 §12 (TGA, PCX, BMP, CUR codecs §8 moves and the JPEG 2000 decision §5 reconciles); -> XREF: D02 T14 §13 (the PSD writer §2 moves); -> XREF: D02 T14 §16 (Stilus's progressive JPEG path switches to §11's encoder); -> XREF: D02 T14 §19 (the WIA acquire service §12 moves); -> XREF: D04 T01 §11 (Albumen's sidecars consume §10's EXIF and IPTC code); backlog B-022 (`legacy-gesso-7.2-7.3`) promoted into §5 and deleted in the authoring commit.
- **Adjacency:** list=applicable (the format list and matrix, the document history dialog, the PDF presets manager, metadata templates); document=applicable (Photoshop PDF, PDF export, and EPS are the documents a print shop receives; printing itself is D03 T18 §6); settings=applicable (`Gesso.Formats.<Format>.*` per codec and `Gesso.Files.*`, each with a default and a named consumer); reporting=applicable (every import returns a report naming what was rasterized, dropped, or mapped; File Info shows the metadata); notifications=applicable (progress and Cancel on reads and writes over one second, completion toasts for exports); permissions=applicable (read-only targets, absent Ghostscript, missing native codecs, encrypted PDFs, and online reads without a user action are refused by name); audit=applicable (one Serilog Information line per open, save, place, and export with format, size, and milliseconds); exchange=applicable (every format in this file); reverse=applicable (Revert to saved; Save a Copy never changes the document; places and metadata edits are undoable)

#### §1. File menu extensions: open, place, revert, close, and save a copy

- **Deliverable:** A `FormatRegistry` every codec registers with, and the File menu built from it: Open with vector routing, Open As, Open as Smart Object or Layers, Place Embedded and Linked, Revert, Close Others and All, Save a Copy with content options, the format matrix, export and overwrite semantics, PDF notes import, and Load Files into Stack.
- **Depends On:** D03 T08 §1, D03 T09 §10
- **Phase:** 25
- **Surface:** UI. Fidelity: docs/captures/gesso/main-window/ for the File menu, extended; new build, no baseline for the format matrix and Save a Copy dialogs, captured to docs/captures/gesso/file-menu/. Job: a user gets any file in as a document, layer, or smart object and gets copies out without disturbing the open document. Treatment: File menu commands, the Windows common file dialog with a filter per registered format, a Save a Copy dialog with content options, a format matrix dialog with a customize list, and one combined save prompt for Close All. Cheaper substitute that fails: hard-coded filter strings. Chrome: consume the registry, `AtomicFileWriter`, `D03 T09 §9` and `§10` smart objects, and the suite history.
- **Runs:** `Requires: display-session -- driving the File menu, dialogs, and drops needs an interactive desktop`
- **Catalog:** IP-1704 to IP-1721 (18 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.FileFormats/FormatRegistry.cs`: each `IImageFormat` declares extensions, magic bytes, read and write support, modes and depths (the matrix, IP-1715), and what it carries (layers, alpha, spot, notes, ICC; IP-1714); menus and dialogs are generated from it and today's `FileFilters` strings are deleted.
  - Open (IP-1704, IP-1708, IP-1709): the Windows common file dialog with All Readable and per-format filters, vector files (SVG, PDF, EPS, AI) routed to their §7 import dialogs, and Open As forcing a format.
  - Open as smart object or as layers (IP-1710) through `D03 T09 §9`; shell open, drag to open or place, and single-instance forwarding (IP-1705, IP-1711) through `D01 T02 §3`.
  - Revert (IP-1706, IP-1716): reload from disk as one history step "Revert".
  - Close, close others, close all (IP-1707, IP-1712) with one prompt listing every dirty document.
  - Save a Copy (IP-1713, IP-1714): flattening formats and content options (layers, alpha, spot, notes, ICC), the document keeping its path and dirty state.
  - Format list (IP-1715): the matrix dialog, `Gesso.Formats.Visible` to customize the list, `Gesso.Files.LegacySaveAs` for Photoshop's legacy Save As.
  - Export and overwrite semantics (IP-1717): `Gesso.Files.SaveNativeOnly` (GIMP's rule), Overwrite <name> and Export To <name>, and saving over an imported non-native file with the lossy-format notice.
  - Place embedded and linked (IP-1718, IP-1720) through `D03 T09 §9` and `§10` with placement preferences (resize to canvas, always create smart object, skip transform), and a PDF page picker once §7 ships.
  - Notes from PDF or FDF (IP-1719): PDF text annotations read through PdfPig (Apache-2.0, already in the suite since `D02 T14 §2`) into `D03 T08 §5` notes; FDF through a small own parser on PdfPig's tokenizer.
  - Load files into stack (IP-1721): one layer per file, optional auto-align through `D03 T15 §5`, optional convert to smart object.
  - One Serilog line per open, save, and place; undo names "Place Embedded", "Place Linked", "Revert".
  - Commit: `"gesso: the File menu on one format registry"`
- **Proof:** unit and driven proof: `FormatRegistryTests` assert the generated filter lists every registered reader and the matrix matches each codec's declaration, and a driven run opens, places linked, reverts, and saves a copy of fixtures with captures and the unchanged-source hash quoted; cheaper substitute that fails: keeping hard-coded filters, which the registry test catches when a codec is added.

#### §12. Create from clipboard, screenshots, scanners, URLs, and archives

- **Deliverable:** New from clipboard, screenshots, WIA acquire, Open Location, archive opening, drops on the tab bar, the document history dialog, copy location and show in Explorer, and Send by Email.
- **Depends On:** §1
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/acquire/. Job: a user starts a document from whatever is at hand without saving an intermediate file. Treatment: File, New from Clipboard; File, Create, Screenshot with a region overlay and options; File, Acquire from a scanner or camera; Open Location; the Document History dialog. Cheaper substitute that fails: shelling out to external tools. Chrome: consume §1's registry, the moved WIA service, and the settings store.
- **Runs:** `Requires: display-session -- screenshots, WIA dialogs, and drops need an interactive desktop`
- **Catalog:** IP-1722 to IP-1731 (10 features)
- **Hints:**
  - Move first: `WiaAcquireService` of `D02 T14 §19` into `src/Isotone.Core/Acquire/` as its second consumer (IP-1725), Stilus repointed; TWAIN stays unsupported (recorded).
  - Drops on the document tab bar open (IP-1722).
  - Archives (IP-1723): gz through `GZipStream`, zip through `ZipArchive` with an entry picker, bz2 and xz through SharpCompress (MIT; not in `IP/decisions.md`, so a new `docs/dev/decisions.md` row, because .NET reads neither).
  - Open Location (IP-1724): http and https through `HttpClient` only on the user's command, with `Gesso.Files.OpenLocation.MaxMegabytes` (512), a content-type check, progress, and Cancel; file URIs; ftp through FluentFTP (MIT, a decisions row) or, if the row declines it, refused by name.
  - New from clipboard (IP-1726): PNG, DIBV5 with alpha, DIB, and SVG flavors (SVG enabled when §7's rasterizer ships).
  - Screenshot (IP-1727): Windows.Graphics.Capture for window, screen, and monitor, region by overlay, decorations, pointer composited from `GetCursorInfo`, delay, tagged with the monitor profile through `D01 T04 §1`; selection delay is not available on Windows (documented).
  - Copy image location and show in Explorer (IP-1728).
  - Document history (IP-1729, IP-1731): recent documents with thumbnails, multi-select open, remove, clear.
  - Send by email (IP-1730): export a copy through §1, then Simple MAPI `MAPISendMailW` with the attachment; no MAPI client is refused by name.
  - Commit: `"gesso: new from clipboard, screenshots, scanners, URLs, and archives"`
- **Proof:** unit and driven proof: `ArchiveOpenTests` open `.png.gz`, `.png.bz2`, `.png.xz`, and `.zip` fixtures to identical pixels, `OpenLocationTests` fetch from a local `HttpListener` and refuse an oversize response, and a driven screenshot and clipboard run is captured; cheaper substitute that fails: gz-only archives, which the bz2 and xz fixtures catch.

#### §2. PSD and PSB write: structure

- **Deliverable:** PSD and PSB writing of layers, groups, masks, channels, paths, guides, ICC, XMP, thumbnails, every mode and depth, and the compatibility composite, on the Stilus writer moved into Isotone.Core.
- **Depends On:** D03 T04 §5, D03 T09 §9
- **Phase:** 25
- **Surface:** no surface of its own (PSD appears in §1's format list; its options page is §13's)
- **Runs:** none
- **Catalog:** IP-1732 to IP-1733 (2 features)
- **Hints:**
  - Move first: `PsdWriter` from `src/Stilus/Isotone.Stilus.Core/Formats/Psd/` (`D02 T14 §13`) into `src/Isotone.Core/Formats/Psd/` beside the reader `D03 T04 §5` moved; Stilus repointed; a grep finds one `class PsdWriter`.
  - `src/Gesso/Isotone.Gesso.FileFormats/Psd/GessoPsdExporter.cs`: raster layers, groups as `lsct` section dividers (open or closed), layer masks with density and feather, opacity and fill opacity, blend-mode keys (the inverse of the reader's map), clipping, visibility, locks, color labels.
  - Channels: alpha and spot channels from `D03 T10 §10` with Unicode names (resource 1045), alternate spot colors (1067), and display info (1077).
  - Resources: resolution (1005), guides (1032), ICC (1039), XMP (1060), JPEG thumbnail (1036), paths (2000 to 2997) and the clipping path (2999) from `D03 T16 §5`.
  - Modes and depths (IP-1732): RGB, gray, CMYK through `D01 T04 §3`, Lab, indexed, and bitmap; 8, 16, and 32 bit through the `Lr16` and `Lr32` blocks; the maximize-compatibility composite written unless §13's preference says never.
  - PSB (IP-1733): version 2 with 8-byte lengths for the keys the specification lists (LMsk, Lr16, Lr32, Layr, Mt16, Mt32, Mtrn, Alph, FMsk, lnk2, FEid, FXid, PxSD), chosen for documents over 30,000 px or 2 GB; the read side is §3.
  - Compression: RLE per scanline, and ZIP with prediction for 16 and 32 bit.
  - Budget: a 100-layer, 24-megapixel, 16-bit RGB document writes in under 10 s with progress and Cancel through `AtomicFileWriter`; one Serilog line per write.
  - Commit: `"gesso: PSD and PSB structure writing on the shared writer"`
- **Proof:** format fidelity proof: each written fixture reads back through psd-tools 1.10 (layer tree dump equal), GIMP 3.2 `gimp-console` (composite within 1/255), and the moved reader, including a 40,000 px wide PSB; opening in Photoshop is an operator check recorded as a risk; cheaper substitute that fails: a composite-only PSD, which the layer tree dump catches.

#### §13. PSD write: live content and editability options

- **Deliverable:** PSD writing of adjustment and fill layers, layer styles, text engine data, smart objects, comps, vector masks, and blend ranges, with editability-versus-accuracy options, compatibility settings, and an export report.
- **Depends On:** §2, D03 T16 §1, D03 T11 §1, D03 T09 §8, D03 T09 §11
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/psd-options/. Job: a designer sends a PSD a Photoshop user can keep editing, or one that looks exactly right. Treatment: a PSD options page with Preserve Editability and Preserve Accuracy presets, per-class rasterize switches, maximize compatibility (Always, Ask, Never), disable compression, smallest file size, and an export report. Cheaper substitute that fails: rasterizing every live layer. Chrome: consume the §1 options shell and the moved writer.
- **Runs:** `Requires: display-session -- the options page and report need an interactive desktop`
- **Catalog:** IP-1734 to IP-1736 (3 features)
- **Hints:**
  - Adjustment layers (`D03 T11 §1`) as `levl`, `curv`, `brit`, `blnc`, `hue2`, `selc`, `mixr`, `grdm`, `phfl`, `expA`, `vibA`, `blwh`, `clrL`, `nvrt`, `post`, `thrs`; fill layers as `SoCo`, `GdFl`, `PtFl`; each also writes its rendered pixels for readers that ignore the block.
  - Layer styles (`D03 T09 §7`, `§8`) as the `lfx2` descriptor through an action-descriptor encoder in `src/Isotone.Core/Formats/Psd/Descriptors/`.
  - Text (`D03 T16 §1`) as `TySh` with an own EngineData writer (the PostScript-like dictionary) for runs, font set, paragraph runs, and transform; attributes it cannot express are rasterized and reported.
  - Smart objects (`D03 T09 §9`, `§10`) as `SoLd` or `PlLd` with embedded files in `lnk2` and linked files as `lnk3` entries.
  - Comps (`D03 T09 §11`) as resource 1065; vector masks and shape layers (`D03 T16 §7`) as `vmsk` or `vsms` with `vscg` and `vstk`; blend ranges from `D03 T09 §5`.
  - Editability versus accuracy (IP-1735): `PsdExportOptions` with per-class rasterize flags (layers, gradients, adjustments, effects, lines, blend ranges, text) and the two Affinity presets.
  - Compatibility (IP-1734): maximize compatibility, and smallest file size with the composite omitted.
  - Save preferences (IP-1736): `Gesso.Formats.Psd.DisableCompression`, `Gesso.Formats.Psd.MaximizeCompatibility`, `Gesso.Formats.Psd.SaveOverImported`.
  - The export report lists every rasterized item and is logged as one Information line.
  - Commit: `"gesso: live adjustments, styles, text, and smart objects in written PSDs"`
- **Proof:** format fidelity proof: psd-tools 1.10 reads each written live block with parameters equal to the document (curve points, style values, text strings and fonts, smart object bytes), GIMP 3.2 composites within 1/255, and Gesso to PSD to Gesso restores the live layers equal; cheaper substitute that fails: rasterized adjustments, which the psd-tools block assertion catches.

#### §3. PSD read fidelity: live adjustments, styles, text, and smart objects

- **Deliverable:** PSD and PSB import that restores adjustment and fill layers, styles, editable text, smart objects as placed documents, comps, vector masks, guides, and paths, in every mode and depth, with import options and a report limited to features Gesso lacks.
- **Depends On:** §13
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/psd-import/. Job: a Photoshop or Affinity composition opens editable. Treatment: a PSD import options dialog (smart objects embedded or rasterized, text editable or pixels, remember choice) and the shrinking import report. Cheaper substitute that fails: stored pixels for every live layer. Chrome: consume the moved reader, `FontSubstitutionService`, and §1's registry.
- **Runs:** `Requires: display-session -- the import dialog needs an interactive desktop`
- **Catalog:** IP-1737 to IP-1740 (4 features)
- **Hints:**
  - Extend the moved `PsdReader` and the Gesso adapter to map every block §13 writes back to live layers, plus legacy `lrFX` effects.
  - Text (IP-1737): an own EngineData parser into a `TextStory`, fonts matched through the moved `FontSubstitutionService`, unknown fonts reported.
  - Smart objects (IP-1740): embedded `lnk2` files opened through §1's registry as editable placed documents, linked files as `D03 T09 §10` links.
  - Fidelity (IP-1738): layers, groups, masks, paths, guides, styles, comps, fill layers, vector masks; modes bitmap, gray, indexed, RGB, CMYK, Lab, duotone (`D01 T04 §3`), and multichannel; depths 1, 8, 16, 32.
  - Options (IP-1739) under `Gesso.Formats.Psd.Import.*`.
  - The import report shrinks to what Gesso cannot hold (3D, video, unknown blocks), shown once and logged.
  - Affinity interop: fixtures exported from Affinity by Canva 3.3 with Preserve Editability open with their adjustments (the interop path for backlog B-045).
  - Commit: `"gesso: PSD import with live adjustments, styles, text, and smart objects"`
- **Proof:** format fidelity proof: fixtures from Photoshop 27.10, Photopea, and Affinity 3.3 (tool and version recorded) import with each layer's composite within 2/255 of the psd-tools composite and text strings and font names equal to its EngineData dump; cheaper substitute that fails: stored pixels only, which the live-layer-kind assertion catches.

#### §4. GIMP XCF read

- **Deliverable:** An own XCF reader for every version and precision GIMP 3.2 writes, restoring layers, groups, masks, channels, paths, guides, parasites, text, link and vector layers, and non-destructive filter stacks.
- **Depends On:** D03 T08 §1, D03 T14 §1, D03 T16 §7, D03 T09 §10
- **Phase:** 25
- **Surface:** no surface of its own (XCF appears in §1's format list; the import report is §1's)
- **Runs:** none
- **Catalog:** IP-1741 (1 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.FileFormats/Xcf/XcfReader.cs` from `devel-docs/XCF.md` at GIMP 3.2.6 (tag recorded): versions 0 through the version GIMP 3.2 writes, 32- and 64-bit offsets, precisions 8, 16, and 32-bit integer, half, float, and double in linear or perceptual, compression none, RLE, and zlib; 64 px tiles re-tiled to 256.
  - Structure: layers, groups (item paths), masks, channels (selection and saved channels with color and opacity), paths (legacy and current), guides, sample points, grid, resolution, the `icc-profile` parasite, comment, and `gimp-image-metadata`.
  - Layer modes: GIMP legacy and default modes mapped to Gesso blend modes, unmapped modes reported by name.
  - Text: the `gimp-text-layer` parasite (markup) into `D03 T16 §1` text layers, pixels when a font is missing.
  - GIMP 3.2 link layers to `D03 T09 §10` linked layers and vector layers to `D03 T16 §7`.
  - Filter stacks: GIMP 3 non-destructive filters into `D03 T14 §1` live filters through `D01 T06 §1`'s GEGL op-id map; unknown ops stay as pixels with a report line.
  - Compressed XCF (`.xcf.gz`, `.xcf.bz2`, `.xcf.xz`) through §12's archive readers; unknown parasites kept for §14.
  - Commit: `"gesso: read GIMP XCF with layers, text, vector layers, and filter stacks"`
- **Proof:** format fidelity proof: fixtures produced by committed `gimp-console-3.2` batch scripts per version and precision import with the composite within 1/255 of GIMP's own PNG export (1e-4 for float) and a layer tree equal to a Script-Fu dump; cheaper substitute that fails: the flattened preview, which the layer tree check catches.

#### §14. GIMP XCF write

- **Deliverable:** An own XCF writer for the same structures with compression and a GIMP 2.10 or 3.x compatibility choice, writing Gesso-only content as pixels plus `gesso-*` parasites.
- **Depends On:** §4
- **Phase:** 25
- **Surface:** no surface of its own (XCF write options are one page in §1's options shell)
- **Runs:** none
- **Catalog:** owns no catalog rows (IP-1741, owned by §4, covers read and write; this section is its write half)
- **Hints:**
  - `XcfWriter`: zlib compression by default with RLE as an option, writing the lowest version that holds the features used (GIMP's rule).
  - `Gesso.Formats.Xcf.Compatibility` (GIMP 2.10 or GIMP 3.x): 2.10 rasterizes link layers, vector layers, and filter stacks with a report.
  - Adjustment layers, styles, and smart objects write as pixels plus `gesso-*` parasites so Gesso restores them per the `D03 T08 §1` contract while GIMP shows pixels.
  - Unknown parasites read by §4 are written back unchanged.
  - Record that Stilus's backlog B-038 (XCF among legacy raster formats) can consume this reader and writer when promoted.
  - Commit: `"gesso: write GIMP XCF with a compatibility choice"`
- **Proof:** format fidelity proof: written fixtures open in `gimp-console-3.2` and, where installed, `gimp-console-2.10` (skipped with a reason otherwise) with the layer tree equal and the composite within 1/255, and a Gesso round trip restores live content from the parasites; cheaper substitute that fails: always writing the newest version, which the GIMP 2.10 open test catches.

#### §5. Modern web formats: WebP, AVIF, HEIF, JPEG XL, JPEG 2000, QOI, JPEG XR

- **Deliverable:** Decode and encode with full options for WebP, AVIF, HEIF and HEIC (with depth maps and HEJ2), JPEG XL, JPEG 2000 (JP2 and J2K), and QOI, JPEG XR decode including HDR, and gain-map HDR JPEG and HEIF open, through the native libraries the decisions name. -> SOURCE: legacy-gesso-7.2-7.3
- **Depends On:** D03 T04 §1
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/web-formats/. Job: a user opens and exports every modern web and camera format with the options its reference encoder offers. Treatment: one options page per format in §1's shell with a live size estimate. Cheaper substitute that fails: the WIC Store extensions many machines lack. Chrome: consume the registry and the atomic writer.
- **Runs:** `Requires: display-session -- the options pages need an interactive desktop`
- **Catalog:** IP-1742 to IP-1753 (12 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-7.2-7.3` (promotes B-022; its PSD-write part lands in §2 and §13, its EXR part in §6, GIF in §8); delete the entry in the authoring commit.
  - Native packaging: each library built per RID (win-x64, win-arm64) by `build/native/<lib>/build.ps1` with `SOURCE.txt` hashes (the lcms2 pattern of `D01 T04 §1`), shipped under `src/Isotone.Core/runtimes/`, licenses in `THIRD-PARTY-NOTICES.md`, one `docs/dev/decisions.md` row per library (HEVC patent exposure recorded); a missing native is refused by name.
  - WebP (IP-1742, IP-1751): decode through SkiaSharp's bundled libwebp as Stilus does, encode through libwebp 1.5 P/Invoke (lossy or lossless, quality, alpha quality, preset, sharp YUV, method) with EXIF, XMP, and ICC chunks; animation is backlog B-044.
  - AVIF (IP-1743): libavif 1.2 with dav1d and libaom: lossless, quality, 4:4:4, 4:2:2, or 4:2:0, 8, 10, or 12 bit, HDR PQ and HLG through CICP, speed, metadata.
  - HEIF and HEIC (IP-1744, IP-1753): libheif 1.19 with libde265 and x265 (kvazaar recorded as the alternative): quality, chroma, depth, speed, metadata; the depth map auxiliary image opens as a layer or a `D01 T07 §4` depth source and is refined on import with `D03 T10 §6`'s guided filter; HEJ2 (IP-1745) through libheif's OpenJPEG plugin.
  - JPEG XL (IP-1746): libjxl 0.11 lossless, distance, effort, bit depth, CMYK through the K extra channel, metadata boxes.
  - JPEG 2000 (IP-1747, IP-1748): OpenJPEG 2.5 for JP2 and J2K: lossless, quality layers, ICT, resolutions, progression orders, cinema 2K and 4K profiles, tiles, ROI, CMYK, metadata; if `D02 T14 §12` chose OpenJPEG, move its binding to `src/Isotone.Core/Formats/Jpeg2000/`, otherwise Stilus's JP2 path switches to this one.
  - JPEG XR (IP-1749): WIC's built-in JPEG XR decoder including half and float HDR into `D03 T15 §4` 32-bit documents.
  - QOI (IP-1750): an own codec from the QOI 1.0 specification.
  - Gain maps (IP-1752): Ultra HDR JPEG (MPF plus `hdrgm` XMP, ISO 21496-1) and HEIF gain maps opened into a 32-bit document or shown through `D03 T15 §4`.
  - Commit: `"gesso: WebP, AVIF, HEIF, JPEG XL, JPEG 2000, JPEG XR, and QOI"`
- **Proof:** format fidelity proof: each format's fixtures decode within 1/255 (bit-exact for lossless) of the reference CLI (`dwebp`, `avifdec`, `heif-dec`, `djxl`, `opj_decompress`), and written files decode in the same CLI within a stated PSNR or exactly for lossless; the missing-native refusal is asserted; cheaper substitute that fails: the WIC Store extensions, which the refusal test on a clean machine exposes.

#### §6. HDR and scientific formats

- **Deliverable:** OpenEXR with every compression, multichannel and multipart layers, alpha options, and OCIO filename color spaces; Radiance HDR, PFM, and the PNM family; float TIFF with the floating-point predictor; HDR gain-map and CICP writing; FITS with Bayer; DICOM with frames, overlays, window level, anonymize, and multi-file load; and Photoshop Raw.
- **Depends On:** D03 T15 §4
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/hdr-formats/. Job: a VFX, astronomy, or medical user opens and writes their formats with the options their tools expect. Treatment: EXR, FITS, DICOM, and raw data import and export option pages in §1's shell. Cheaper substitute that fails: EXR through an 8-bit path. Chrome: consume the registry, `D03 T15 §4` 32-bit documents, and `D03 T11 §4` OCIO.
- **Runs:** `Requires: display-session -- the option pages need an interactive desktop`
- **Catalog:** IP-1754 to IP-1771 (18 features)
- **Hints:**
  - OpenEXR 3.3 through its C API (`openexr_core`), native per RID: scanline and tiled; none, RLE, ZIP, ZIPS, PIZ, PXR24, B44, B44A, DWAA, DWAB (IP-1756, IP-1764); half or float per channel class (IP-1766); multichannel and multipart as layers (IP-1754, IP-1769); alpha associate, unpremultiply, and perturb zero alpha (IP-1768); export precision.
  - EXR color space from a filename affix through the OCIO config (IP-1765, IP-1767) using `D03 T11 §4`'s wrapper and `D03 T18 §4`'s configuration.
  - Radiance HDR RGBE with RLE (IP-1757), PFM (IP-1758), and PBM, PGM, PPM, and PAM binary and ASCII with 16-bit maxval (IP-1759): own codecs.
  - Float TIFF (IP-1760): verify whether WIC honors predictor 3; if not, `TiffFloatPredictor` in `Isotone.Gesso.FileFormats/Tiff/` applies it on read and write, recorded in decisions.
  - HDR output (IP-1755): Ultra HDR gain-map JPEG, PNG with cICP, and 16-bit PQ PNG for 32-bit documents.
  - FITS 4.0 (IP-1761, IP-1770): primary HDU and image extensions, BITPIX 8, 16, 32, -32, -64, BZERO and BSCALE, `BAYERPAT` debayering (bilinear), header cards kept as metadata; export.
  - DICOM (IP-1762, IP-1771): own PS3.10 reader for implicit and explicit VR little endian, big endian, JPEG baseline, JPEG lossless process 14 (own decoder), and RLE lossless; frames as layers, overlays (60xx) as a layer, window width and level, anonymize per the PS3.15 Basic Profile, multiple files loaded by Instance Number, Secondary Capture export; fo-dicom is not used (MS-PL is GPL-incompatible).
  - Photoshop Raw (IP-1763): header size, planar or interleaved, byte order, and GIMP's palette layouts.
  - Commit: `"gesso: OpenEXR, Radiance, PFM, PNM, FITS, DICOM, and raw data"`
- **Proof:** format fidelity proof: EXR, HDR, PFM, and FITS fixtures decode within 1e-4 of OpenImageIO 3.0 `oiiotool` output and written files re-read equal per channel; DICOM fixtures match dcmtk 3.6 `dcm2pnm` within 1/255 at the same window; PNM round trips are exact; cheaper substitute that fails: one EXR compression, which the per-compression fixtures catch.

#### §7. Document and vector formats: PDF, Photoshop PDF, EPS, SVG, and metafiles

- **Deliverable:** PDF import through PDFium, PostScript, EPS, and AI import through the user's Ghostscript, Photoshop PDF save and PDF export with presets, PDF/X, compression, color, layers, fonts, marks, and security, EPS save, SVG import, and WMF and EMF import and export, on PDF, PostScript, SVG, and metafile code moved from Stilus into Isotone.Core.
- **Depends On:** D03 T16 §5, D02 T13 §14, D02 T14 §9
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/pdf-import/, docs/captures/gesso/pdf-export/, and docs/captures/gesso/eps/. Job: a user rasterizes vector documents in and sends print-ready PDF and EPS out. Treatment: a PDF import dialog (pages with thumbnails or images, crop box, size, resolution, mode, reverse, anti-aliasing, fill transparent, editable text), a PostScript import dialog, a Save Adobe PDF dialog with a presets manager and General, Compression, Output, Security, Marks, and Summary pages, EPS options, and metafile options. Cheaper substitute that fails: `SKDocument` PDF output. Chrome: consume the moved writer and presets, the moved Ghostscript runner, `D01 T04` output intents, and §1's registry.
- **Runs:** `Requires: display-session -- the dialogs and captures need an interactive desktop`
- **Catalog:** IP-1772 to IP-1795 (24 features)
- **Hints:**
  - Moves first, each leaving one definition: the PDF writer of `D02 T13 §14` (`PdfContentWriter`, `PdfResourceBuilder`, `TrueTypeSubsetter`), the presets and standards of `D02 T13 §15` (`PdfPresetStore`, `PdfStandardEnforcer`), and the security of `D02 T13 §16` into `src/Isotone.Core/Pdf/`; `GhostscriptBridge` (`D02 T14 §9`) and `PostScriptWriter` (`D02 T13 §10`) into `src/Isotone.Core/Formats/PostScript/`; the SVG renderer into `src/Isotone.Core/Vector/Svg/` (the reader moved in `D03 T16 §5`); the EMF and WMF readers and writers of `D02 T14 §11` into `src/Isotone.Core/Formats/Metafile/`; `PrinterMarksRenderer` (`D02 T13 §4`) into `src/Isotone.Core/Print/` for `D03 T18 §6` to consume.
  - PDF import (IP-1772, IP-1773): PDFium through a thin P/Invoke (`FPDF_LoadMemDocument`, `FPDF_RenderPageBitmapWithMatrix`) native per RID: pages or embedded images; media, crop, bleed, trim, or art box; size, resolution, mode, reverse order, anti-aliasing, fill transparent, password prompt; editable text from PdfPig text positions as `D03 T16 §1` text layers above the page.
  - PostScript, EPS, and AI import (IP-1774): the moved runner with `-dSAFER`, `-dTextAlphaBits`, `-dGraphicsAlphaBits`, bounding box, and coloring; AI through its embedded PDF stream; absent Ghostscript refused by name; no AI export.
  - Photoshop PDF save (IP-1775 to IP-1779, IP-1795): presets manager, PDF/X-1a, X-3, X-4, compatibility 1.4 to 2.0, preserve editing (the `.gesso` package embedded as an attachment Gesso reopens live), thumbnails, fast web view (linearized if the writer supports it, otherwise recorded as refused), summary; downsampling, ZIP, JPEG, JPEG 2000 (§5's OpenJPEG), 16 to 8 bit; color conversion, profile inclusion, output intent; open password, permissions, AES-256.
  - PDF export (IP-1780, IP-1786 to IP-1791): layers as pages, reverse, root layers, apply masks, vectorize text and shape layers, omit hidden, fill transparent, text as image, open when complete; spot colors and overprint black through `D01 T04`; layers as optional content; embed and subset fonts, text as curves, hyperlinks and bookmarks; printer marks through `PrinterMarksRenderer`; passwords and permissions.
  - Rasterization policy (IP-1792) for PDF, SVG, and EPS: raster DPI, rasterize nothing, everything, or unsupported, downsample images.
  - EPS save (IP-1781, IP-1782, IP-1793) on the moved `PostScriptWriter`: TIFF preview 1 or 8 bit or none, ASCII85, binary, or JPEG encoding, halftone screen and transfer inclusion, vector data, size, offset, unit, rotation, PostScript level 2 or 3, minimize size.
  - SVG import (IP-1783) rasterized at a chosen size by the moved renderer.
  - WMF and EMF (IP-1784, IP-1785, IP-1794): import rasterized at a chosen DPI; export vector layers as records and raster layers as bitmap records, with enhanced metafile and clip transparency options.
  - Commit: `"gesso: PDF, Photoshop PDF, EPS, SVG, and metafiles on the shared writers"`
- **Proof:** format fidelity proof: PDF imports match `pdfium_test --png` at the same DPI within 1/255 and Ghostscript 10.x within a stated tolerance; written PDFs read back with PdfPig (optional content names, output intent, Separation names, encryption) and render against MuPDF `mutool draw` goldens within 1 percent of pixels; written EPS renders through Ghostscript within tolerance of Gesso's render; EMF and WMF re-import through Inkscape 1.4 within tolerance; PDF/X conformance is proven by the moved enforcer's rule tests, with Acrobat preflight an operator check recorded as a risk; cheaper substitute that fails: `SKDocument`, which has no Separation color space or optional content.

#### §8. Common and legacy raster formats I

- **Deliverable:** BMP, single-frame GIF, ICO, CUR, ANI, ICNS, DDS with mipmaps, TGA, PCX and DCX, XBM, XPM, XWD, Sun raster, SGI, farbfeld, and WBMP, on the Stilus raster codecs moved into Isotone.Core.
- **Depends On:** D03 T04 §1
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/legacy-formats/. Job: a user opens and writes icon, texture, and legacy raster files with their format's options. Treatment: one options page per writable format in §1's shell (BMP, GIF, ICO, CUR, ANI, DDS, TGA, XBM, SGI, Sun). Cheaper substitute that fails: routing everything through WIC, which lacks most of these. Chrome: consume the registry and the moved codecs.
- **Runs:** `Requires: display-session -- the option pages need an interactive desktop`
- **Catalog:** IP-1796 to IP-1813 (18 features)
- **Hints:**
  - Move first: `TgaCodec`, `PcxCodec`, the OS/2 BMP shim, and the CUR path of `D02 T14 §12` from `src/Stilus/Isotone.Stilus.Core/Formats/Raster/` into `src/Isotone.Core/Formats/Raster/`; consume the WIC codec where `D03 T04 §1` placed it.
  - BMP (IP-1796): RLE4 and RLE8, V4 and V5 color space info, 16-bit 565 and 555, 24, and 32 with alpha and bitfields, OS/2, row order.
  - GIF single frame (IP-1797): indexed conversion through `D01 T03 §3` and `D03 T11 §7`, interlace, comment; animation is backlog B-044.
  - ICO, CUR, ANI (IP-1798 to IP-1800): per-size BMP or PNG entries, hot spot, ANI RIFF (`anih`, `rate`, `seq`, INFO name and author) with frames as layers.
  - ICNS (IP-1801): own reader and writer for PNG and JPEG 2000 entries (§5's OpenJPEG) with the color profile.
  - DDS (IP-1802, IP-1803): BCnEncoder.Net (MIT) for BC1 to BC7, uncompressed formats, cube, volume, and array, flip, transparent index; mipmaps generated with `D01 T03 §2` filters or kept, wrap mode, gamma-correct filtering, alpha-test coverage preservation.
  - TGA (IP-1804), and PCX with an own DCX container (IP-1805), through the moved codecs.
  - XBM (IP-1806) X10 or X11 with prefix, comment, hot spot, and mask file; XPM (IP-1807) with the X11 color-name table (MIT); XWD (IP-1808); Sun raster (IP-1809) standard or RLE; SGI (IP-1810) none, RLE, aggressive RLE; farbfeld (IP-1811); WBMP (IP-1812) read.
  - IP-1813 umbrella: the GIMP 3 additions land here, with QOI and JPEG XL in §5, ILBM in §9, and PAM in §6.
  - Each codec registers with §1's registry and logs one line per read and write.
  - Commit: `"gesso: common and legacy raster formats on the shared codecs"`
- **Proof:** format fidelity proof: decode goldens from ImageMagick 7.1 (`magick <file> rgba:`), GIMP 3.2 for XBM, XPM, and ANI, and DirectXTex `texconv` for DDS, pixel-exact for lossless formats and within the stated BCn tolerance, with every writer's output decoding in the same oracle; cheaper substitute that fails: WIC only, which the ANI, DDS, and SGI fixtures refuse.

#### §9. Legacy raster formats II and text and resource exports

- **Deliverable:** IFF and ILBM, Pixar, Scitex CT, DCS, MPO, Paint Shop Pro, KiSS CEL, Alias PIX, PlayStation TIM, PVR, PAA, SFW, and JIF, plus C source and header, HTML table, colored HTML text, ASCII art, and GIMP brush, brush pipe, and pattern exports.
- **Depends On:** §8
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/resource-exports/. Job: a user opens old and game files and exports images as code, HTML, text art, or GIMP resources. Treatment: option pages for C source, HTML table, colored HTML, ASCII art, DCS, TIM, and the GIMP resources. Cheaper substitute that fails: skipping the text exports. Chrome: consume the registry and the `D03 T12 §3` and `§10` resource readers.
- **Runs:** `Requires: display-session -- the option pages need an interactive desktop`
- **Catalog:** IP-1814 to IP-1833 (20 features)
- **Hints:**
  - IFF ILBM with HAM and EHB (IP-1814); Pixar PXR read and write (IP-1815); Scitex CT write (IP-1816).
  - Photoshop DCS 1.0 and 2.0 (IP-1817): single or multiple files with composite, on §7's EPS writer.
  - MPO (IP-1818): the MPF index into layers; Paint Shop Pro (IP-1819): layers and selection shape from the published PSP file format description.
  - KiSS CEL (IP-1820), Alias PIX (IP-1821), and PlayStation TIM with type and image and palette origin (IP-1822) read and write; Dreamcast PVR and Arma PAA (IP-1823), SFW (IP-1824), and JIF (IP-1825) read.
  - C source and header (IP-1826, IP-1827): name, comment, GLib types, macros, RLE, alpha, RGB565, opacity, as GIMP's exporter offers.
  - HTML table (IP-1828): full document, cellspan, compressed tags, caption, cell content, border, size, padding, spacing; colored HTML text (IP-1829): characters, file source, font size, separate CSS.
  - ASCII art (IP-1830): an own glyph-density renderer (not aalib) writing text, HTML, ANSI, printer, IRC, and man page formats.
  - GIMP resources (IP-1831 to IP-1833): GBR, GIH, and PAT writers beside the readers `D03 T12 §3` and `§10` added, per GIMP's devel-docs, PAT with its description.
  - Each codec registers with the registry; one Serilog line per read and write.
  - Commit: `"gesso: legacy formats and text and resource exports"`
- **Proof:** format fidelity proof: decode goldens from ImageMagick 7.1 or GIMP 3.2 per format (oracle recorded per fixture), written GBR, GIH, and PAT files load in `gimp-console-3.2` as a brush, pipe, and pattern, and C, HTML, and ASCII outputs match committed golden text; cheaper substitute that fails: read-only support for writable formats, which the writer round trips catch.

#### §11. JPEG, PNG, and TIFF option extensions

- **Deliverable:** Full JPEG encoding and export options on libjpeg-turbo, a chunk-level PNG writer with HDR cICP, a TIFF writer with every compression, BigTIFF, pyramids, GeoTIFF, and Photoshop layers, Photoshop data in JPEG and TIFF, and CMYK files with profiles.
- **Depends On:** D03 T04 §3
- **Phase:** 25
- **Surface:** UI. Fidelity: extends the JPEG options dialog of `D03 T04 §2` (docs/captures/gesso/jpeg-options/); new build, no baseline for PNG and TIFF options, captured to docs/captures/gesso/png-tiff-options/. Job: a user controls exactly how the three most common formats are encoded. Treatment: JPEG, PNG, and TIFF option pages with live preview and a real size estimate, saved defaults, and the layered TIFF prompt. Cheaper substitute that fails: WIC's quality slider only. Chrome: consume the registry, §2's PSD layer section, and `D01 T04`.
- **Runs:** `Requires: display-session -- the option pages need an interactive desktop`
- **Catalog:** IP-1834 to IP-1843 (10 features)
- **Hints:**
  - libjpeg-turbo 3.1 (IJG, BSD-3-Clause, and zlib licenses; not in `IP/decisions.md`, so a new decisions row) native per RID in `src/Isotone.Core/Formats/Jpeg/`: optimize, progressive with scan scripts, subsampling 4:4:4, 4:2:2, 4:2:0, 4:1:1, DCT method, arithmetic coding, restart markers, smoothing (IP-1834); Stilus's progressive JPEG decision (`D02 T14 §16`) switches to it.
  - JPEG export (IP-1835): matte, size estimate from a real encode, live preview, use original quality (estimated from the quantization tables, as GIMP does), CMYK with Adobe APP14, EXIF, IPTC, XMP, thumbnail, comment.
  - `PngWriter` in `src/Isotone.Core/Formats/Png/` over `ZLibStream` (IP-1836, IP-1841): gray, gray-alpha, RGB, RGBA, and indexed at 8 or 16 bit, compression 0 to 9, Adam7, tRNS, bKGD, oFFs, pHYs, tIME, iTXt and zTXt, cICP (PQ, HLG, BT.709, full range), mDCV, cLLI; defaults saved under `Gesso.Formats.Png.*`.
  - TIFF writer (IP-1837): JPEG, PackBits, CCITT G3 and G4, LZW, Deflate; interleaved or planar, byte order, pyramid sub-IFDs, transparent pixel colors, CMYK, BigTIFF, metadata, GeoTIFF tags kept; own writer versus LibTiff.NET (BSD-3-Clause) decided in a decisions row.
  - Layered TIFF (IP-1838, IP-1842, IP-1843): Photoshop-style layers in tag 37724 using §2's PSD layer section, save and crop layers, layer compression, and `Gesso.Formats.Tiff.AskLayered`.
  - Photoshop data (IP-1839): APP13 and tag 34377 image resources for clipping paths (2000 to 2999, from `D03 T16 §5`'s clipping flag) and guides (1032), plus layers in TIFF.
  - CMYK (IP-1840): CMYK JPEG, TIFF, and JPEG XL import and export with a CMYK profile through `D01 T04 §1` and `§3`; PSD CMYK is §2 and §3.
  - Commit: `"gesso: full JPEG, PNG, and TIFF options with layered TIFF and CMYK"`
- **Proof:** format fidelity proof: libjpeg-turbo `djpeg` and exiftool 13 confirm each JPEG option in written files, `pngcheck` 3.0 validates every PNG chunk and libpng decodes it exactly, libtiff 4.7 `tiffdump` confirms each TIFF tag and compression, and ImageMagick 7.1 reads the layered TIFF's layers; cheaper substitute that fails: WIC's encoder, which cannot write arithmetic coding, cICP, or BigTIFF and fails those assertions.

#### §10. Metadata: EXIF, IPTC, XMP, and File Info

- **Deliverable:** EXIF, IPTC IIM, and XMP read and write shared in Isotone.Core, the File Info dialog and Metadata panel with IPTC Core and Extension, GPS and a Location panel, metadata templates, export embedding and stripping, EXIF orientation handling, and XMP sidecars.
- **Depends On:** D03 T08 §1
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/file-info/ and docs/captures/gesso/metadata-panel/. Job: a photographer views, edits, templates, and strips metadata. Treatment: File Info (description, IPTC, IPTC Extension, camera data, GPS, raw XMP, history), a Metadata panel, a Location panel with a map, and export metadata policies. Cheaper substitute that fails: an XMP-only editor. Chrome: consume `D01 T07 §6`'s XMP core, the settings store, and the history.
- **Runs:** `Requires: display-session -- the dialog, panels, and map need an interactive desktop`
- **Catalog:** IP-1860 to IP-1876 (17 features)
- **Hints:**
  - Consume `XmpPacket` from `D01 T07 §6`; add `ExifReader` and `ExifWriter` (IFD0, Exif, GPS, and Interop IFDs per Exif 3.0 including UTF-8) and `IptcIimReader` and `IptcIimWriter` (8BIM 1028) in `src/Isotone.Core/Metadata/` so Albumen's `D04 T01 §11` consumes them.
  - `DocumentMetadata` persisted as `metadata.xmp` in the `.gesso` package, registered with `D03 T08 §1`; image comment (IP-1860) and title and imported PDF metadata (IP-1861).
  - EXIF orientation (IP-1862): `Gesso.Files.ExifOrientation` Ask, Always, or Never with a rotate dialog.
  - Editor (IP-1863 to IP-1865, IP-1874): title, author, description writer, rating, keywords, copyright status, notice, and URL; IPTC Core and IPTC Extension 2024.1 fields including digital source type.
  - Viewer (IP-1868, IP-1869): EXIF camera data, IPTC, XMP, raw XMP, and read-only audio, video, and Photoshop panels; DICOM fields (IP-1867) from §6.
  - GPS (IP-1866, IP-1875): view, edit, strip GPS, strip all EXIF; Location panel (IP-1873) with OpenStreetMap tiles fetched only after the user opens the panel and confirms online use, a tile URL setting, attribution, and a cache.
  - Templates (IP-1870): save, apply (append or replace), import, and export.
  - Export policy (IP-1871): embed or strip per category, and update dimensions, timestamps, software, and thumbnail automatically; editable EXIF in develop (IP-1872) through `D03 T15 §12`.
  - Sidecars (IP-1876): export and import `.xmp` beside the file and auto-load on open.
  - Undo "Edit Metadata"; one Serilog line per edit and strip.
  - Commit: `"gesso: EXIF, IPTC, and XMP metadata with File Info and sidecars"`
- **Proof:** format fidelity proof: exiftool 13 reads back every written field from JPEG, TIFF, PNG, WebP, and PSD fixtures, unknown XMP survives a round trip byte-equivalent after canonicalization, and Strip GPS leaves no GPS tag; cheaper substitute that fails: XMP only, which exiftool's EXIF and IPTC IIM checks catch.

#### Sizing concerns

- §7 owns 24 features and six moves; the natural split is PDF (import, Photoshop PDF save, PDF export, presets, security; IP-1772, IP-1773, IP-1775 to IP-1780, IP-1786 to IP-1792, IP-1795) versus PostScript, EPS, SVG, and metafiles (IP-1774, IP-1781 to IP-1785, IP-1793, IP-1794).
- §9 owns 20 formats and exports at about one item each; if it overruns, split image formats (IP-1814 to IP-1825) from text and resource exports (IP-1826 to IP-1833).
- §8 owns 18 features plus a move; the natural split is Windows and icon formats (BMP, GIF, ICO, CUR, ANI, ICNS, DDS) versus the X11 and workstation formats.
- §6 owns 18 features; the natural split is HDR (EXR, Radiance, PFM, PNM, float TIFF, gain maps) versus scientific (FITS, DICOM, raw data).

### todo/03-gesso/TODO-18-gesso-parity-output.md -- `gesso-parity-output`

- **Title:** "TODO-18 -- Gesso Parity: Export, Web Output, Color Management, and Print"
- **Phase(s):** 25
- **Goal:** A Gesso user exports anything (document, selection, layers, artboards, comps, generated assets) at any size and format from one Export As dialog or Quick Export, optimizes web images in Save for Web and Affinity's Export studio with slices and continuous export, builds image maps, sets suite-wide color settings with working spaces, policies, custom CMYK, assign and convert, display color management, and OpenColorIO, soft-proofs with gamut and deficient-vision views, and prints with Gesso-managed color, marks, functions, separations, halftones, preflight, contact sheets, and PDF presentations. The color engine is `D01 T04` (Gesso's hand-rolled `ColorProfile` and `SoftProofing` classes are retired), the print dialog frame, planner, marks, separations, halftones, and preflight engine move from Stilus (`D02 T13 §2`, `§3`, `§4`, `§5`, `§9`, `§10`) into `src/Isotone.Core/Print/`, `src/Isotone.Core/Preflight/`, and `src/Isotone.UI/Print/`, and the export queue, web encoder, slice model, and image map writer move from Stilus (`D02 T14 §15`, `§16`, `§17`) into `src/Isotone.Core/Export/`; Gesso's surfaces live in `src/Gesso/Isotone.Gesso.Desktop/Views/Export/` and `Views/Print/`. Exporting never changes the document; color operations are undoable commands; nothing prints or converts silently.
- **Current-state facts to verify (with claim candidates):**
  - Export is a logging stub over a five-format filter string. `<!-- claim: count "Export dialog for" src/Gesso/src/Gesso.UI/ViewModels/MainWindowViewModel.cs = 1 -->` `<!-- claim: count "ExportFormats = " src/Gesso/src/Gesso.UI/Services/IFileDialogService.cs = 1 -->`
  - Gesso carries its own hand-rolled color classes (four built-in RGB profiles by primaries and gamma, and a matrix soft proof) that §4 and §5 retire in favor of `D01 T04`. `<!-- claim: lines src/Gesso/src/Gesso.Core/Colors/ColorProfile.cs = 130 -->` `<!-- claim: count "public static ColorProfile \w+ \{ get; \}" src/Gesso/src/Gesso.Core/Colors/ColorProfile.cs = 4 -->` `<!-- claim: lines src/Gesso/src/Gesso.Core/Colors/SoftProofing.cs = 178 -->`
  - No ICC engine exists anywhere in the tree yet; `D01 T04 §1` adds it. `<!-- claim: count "lcms|IccProfile|ColorContext" src/**/*.cs = 0 -->`
  - Gesso has no printing code or menu entry. `<!-- claim: count "Print" src/Gesso/src/**/*.cs = 0 -->` `<!-- claim: count "Print" src/Gesso/src/**/*.xaml = 0 -->`
  - The backlog entries this file promotes still exist. `<!-- claim: count "B-021\] Print" todo/backlog.md = 1 -->` `<!-- claim: count "B-023\] Color management and soft proofing" todo/backlog.md = 1 -->`
- **Inputs and XREFs:** `standards/gesso.md` (color never changes profile silently; GPU path with CPU parity); `standards/shared.md`; ICC.1:2022 and lcms2 2.16 (`transicc` goldens); OpenColorIO 2.5 with its built-in `ocio://` ACES configs; Machado, Oliveira, and Fernandes 2009 (color vision deficiency simulation); Adobe Photoshop Generator asset naming documentation; the Zoomify tile format (ImageProperties.xml, TileGroup folders); GIMP 3.2.6 Image Map plug-in (CSIM, NCSA, CERN map formats); HTML Living Standard `<map>` and `<area>`; Apple asset catalog `Contents.json` format; Microsoft Learn `System.Printing.PrintQueue`, `XpsDocumentWriter`, `DocumentPropertiesW`, `WcsGetDefaultColorProfile`, and Simple MAPI; MuPDF `mutool draw` and PdfPig as print-to-PDF readers; -> XREF: D01 T03 §2 (export resamplers); -> XREF: D01 T03 §3 (palette quantization for PNG-8 and GIF); -> XREF: D01 T04 §1, D01 T04 §2, D01 T04 §3 (profiles, intents, proofing, gamut, and bitmap modes); -> XREF: D02 T13 §2 (the print dialog frame §6 moves); -> XREF: D02 T13 §3 (print tiling §6 consumes); -> XREF: D02 T13 §4 (printer marks, moved by D03 T17 §7 or §6); -> XREF: D02 T13 §5 (separations, halftones, and inks §7 moves); -> XREF: D02 T13 §9 (the preflight engine §7 moves); -> XREF: D02 T13 §10 (the PostScript writer for PostScript printer options); -> XREF: D02 T14 §15 (the export queue §1 moves); -> XREF: D02 T14 §16 (the web encoder §2 moves); -> XREF: D02 T14 §17 (the slice model and image map writer §2 and §3 move); -> XREF: D03 T02 §2, D03 T02 §3, D03 T02 §5 (the viewport display transform, blend gamma in the render graph, and the GPU path with CPU parity); -> XREF: D03 T04 §2 (the save paths Export As extends); -> XREF: D03 T08 §1 (slices, soft proof layers, and document color settings persist through the contract); -> XREF: D03 T08 §2 (document profile and bleed in New Document); -> XREF: D03 T08 §4 (guides for slices and image maps); -> XREF: D03 T09 §11 (comps to files); -> XREF: D03 T09 §13 (artboards to files); -> XREF: D03 T10 §10 (spot channels for separations); -> XREF: D03 T11 §1 (the adjustment host for the soft proof layer); -> XREF: D03 T11 §4 (the OpenColorIO wrapper); -> XREF: D03 T11 §5 (semi-flatten for Web filters); -> XREF: D03 T11 §7 (mode conversions Convert to Profile shares); -> XREF: D03 T15 §4 (the 32-bit preview OCIO views drive); -> XREF: D03 T16 §1 (captions on contact sheets and presentations); -> XREF: D03 T17 §1, D03 T17 §5, D03 T17 §7, D03 T17 §10, D03 T17 §11 (the format registry, web codecs, PDF writer, metadata policy, and CMYK writers exports use); -> XREF: D03 T20 §1 (the Export studio as a workspace preset); -> XREF: D03 T20 §4, D03 T20 §5 (preferences pages that list the `Gesso.Color.*`, `Gesso.Export.*`, and `Gesso.Print.*` keys); backlog B-021 (`legacy-gesso-7.4`) promoted into §6 and B-023 (`legacy-gesso-1.3`) promoted into §4, each deleted in the authoring commit.
- **Adjacency:** list=applicable (export presets, the slices and export options panels, preflight rules, profile lists filtered by class and space); document=applicable @ D03 T18 §6 (print and its extras are this file's printed output); settings=applicable (`Gesso.Export.*`, `Gesso.Color.*`, `Gesso.Print.*`, and the shared suite color-settings file); reporting=applicable (estimated export sizes, profile mismatch and missing-profile warnings, the preflight report); notifications=applicable (export and print progress with Cancel, continuous export status, completion toasts); permissions=applicable (read-only destinations, offline printers, missing or corrupt profiles, and absent OCIO configs are refused by name); audit=applicable (one Serilog Information line per export, conversion, assign, and print job); exchange=applicable (image map files, color settings files, ICC profiles, OCIO configs, Xcode icon sets, PDF presentations); reverse=applicable (assign and convert are undoable; exports and prints never change the document)

#### §1. Export As, Quick Export, and asset export

- **Deliverable:** One Export As dialog and Quick Export over an `ExportJob` model that exports the document, a selection area, layers, artboards, and comps to files and PDF at any scale, format, depth, and profile, plus generated image assets from layer names.
- **Depends On:** D03 T17 §5, D03 T09 §13, D03 T09 §11
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/export-as/ and docs/captures/gesso/quick-export/. Job: a designer exports exactly the pixels, size, format, and profile a client needs in one action, and re-exports after edits. Treatment: an Export As dialog with every registered format in one list, favorites, presets, scale multiples with suffixes, a live zoomable preview of the encoded result with its real size, and per-layer, artboard, and comp lists; Quick Export as one command and an Affinity-style panel with a draggable preview. Cheaper substitute that fails: Save As under another name. Chrome: consume `D03 T17 §1`'s registry and writers, the moved export queue, and the status strip.
- **Runs:** `Requires: display-session -- the dialog, preview, and panel captures need an interactive desktop`
- **Catalog:** IP-1881 to IP-1901 (21 features)
- **Hints:**
  - Move first: `BackgroundExportQueue` and the export naming logic of `D02 T14 §15` into `src/Isotone.Core/Export/` as their second consumer, Stilus repointed.
  - `src/Gesso/Isotone.Gesso.Core/Export/ExportJob.cs`: source (document, selection area, selection only, layer, artboard, comp; IP-1893), size (scale, width, height, aspect lock, nearest, bilinear, bicubic, Lanczos 3 separable and non-separable through `D01 T03 §2`; IP-1894), pixel format, bit depth, DPI override (IP-1895), quality, matte, palettised PNG and GIF through `D01 T03 §3` (IP-1896), profile keep, convert, embed, or unprofiled with installed profiles (IP-1897), include bleed from `D03 T08 §2` (IP-1898), and the `D03 T17 §10` metadata policy.
  - Export As (IP-1881, IP-1891): transparency, 8-bit PNG, quality, image and canvas size, metadata, convert to sRGB, favorites, and a preview re-encoded on change (debounced, cancellable) showing the byte count of the actual encode.
  - Scale multiples with suffixes (IP-1882) and presets per format with create, rename, delete (IP-1892).
  - Quick Export (IP-1883, IP-1899): `Gesso.Export.Quick.Format`, `.Quality`, `.Location` (ask or same folder), a toolbar button, and the panel.
  - Layers to files (IP-1884, IP-1888, IP-1901): destination, prefix, visible only, trim, per-format options, from the dialog list and the Layers panel.
  - Artboards to files and PDF (IP-1885, IP-1890) and comps to files and PDF (IP-1886, IP-1889, IP-1900) through `D03 T09 §13`, `D03 T09 §11`, and the `D03 T17 §7` PDF writer.
  - Generate image assets (IP-1887): Photoshop Generator syntax in layer names (for example `200% hero@2x.png, 80% hero.jpg`, folders, a `default` layer) parsed by `AssetNameParser`, regenerated on change into `<document>-assets/`.
  - Per-format size limits warn by name (for example JPEG's 65,535 px); a read-only destination is refused by name; one Serilog line per exported file.
  - Commit: `"gesso: Export As, Quick Export, and asset export"`
- **Proof:** unit and driven proof: `ExportJobTests` resolve sizes for every mode, `AssetNameParserTests` pass Adobe's documented examples, the preview's shown size equals the written file's byte count, and a driven export of layers, artboards, and comps is captured with the file list quoted; cheaper substitute that fails: Save As reuse, which ignores scale, area, and suffixes and fails those tests.

#### §2. Save for Web and the Export studio

- **Deliverable:** Save for Web with 2-up and 4-up optimization, web palettes, lossy GIF, optimize to size, and Zoomify tiles; Affinity's Export studio with slices, per-slice formats and sizes, naming tokens, continuous export, and app icon sets; Web filters with semi-flatten; and GIMP's Image Map editor with CSIM, NCSA, and CERN files.
- **Depends On:** §1
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/save-for-web/, docs/captures/gesso/export-studio/, and docs/captures/gesso/image-map/. Job: a web designer ships the smallest good-looking files, keeps sliced exports current while editing, and builds clickable image maps. Treatment: a Save for Web dialog (original, optimized, 2-up, 4-up, presets, color table, size, preview in browser), the Export studio workspace (slices, export options, and layers panels with continuous export), and an Image Map editor window (areas list, source and gray views, grid and guides). Cheaper substitute that fails: a quality slider on JPEG export. Chrome: consume §1's job model, the moved web encoder and image map writer, `D03 T20 §1` workspaces, and `D03 T08 §4` guides.
- **Runs:** `Requires: display-session -- the dialogs, the studio, and the editor need an interactive desktop`
- **Catalog:** IP-1902 to IP-1919 (18 features)
- **Hints:**
  - Move first: the encoder half of `D02 T14 §16` (`WebEncoderSettings`, estimates, presets) into `src/Isotone.Core/Export/Web/` and the HTML `<map>` writer of `D02 T14 §17` into `src/Isotone.Core/Export/Web/ImageMap/`, Stilus repointed.
  - Save for Web (IP-1903): views, presets, optimize to size (a search over quality or colors), image size, metadata, sRGB conversion, preview in the default browser from a temporary page.
  - GIF and PNG-8 (IP-1904): perceptual, selective, adaptive, and restrictive reduction through `D01 T03 §3`, lossy LZW (implemented from its published description), dither types and amount, color table lock, add, delete, and web snap; PNG-24, JPEG, and WBMP options (IP-1905).
  - Slices output (IP-1906): images plus HTML table or CSS with output settings; Zoomify (IP-1907): 256 px JPEG pyramid in `TileGroupN` folders with `ImageProperties.xml` and an own HTML template.
  - Export studio (IP-1908 to IP-1912): a workspace preset registered with `D03 T20 §1`, per-item export visibility independent of canvas visibility, slices from layers, groups, and drawn areas (§3's model), multiple formats with 1x, 2x, 3x or absolute sizes and DPI scaling per slice, per-slice or default settings with presets and copy and paste, naming tokens and folder paths.
  - Continuous export (IP-1913): subscribe to document change events, debounce, and re-export only slices whose bounds intersect the change, with a status indicator.
  - App icon presets (IP-1914): iOS, Android, Windows, and macOS sets and Xcode `AppIcon.appiconset/Contents.json`.
  - Web filters and semi-flatten (IP-1915) through `D03 T11 §5`.
  - Image Map editor (IP-1902, IP-1916 to IP-1919): working area, rectangle, circle, and polygon areas, area list with reorder, area info (URL, alt, target, event attributes written, never executed), source and gray views, grid and guides with create guide areas; open, recent, save, save as, and map info in CSIM, NCSA, and CERN formats.
  - Commit: `"gesso: Save for Web, the Export studio, and the Image Map editor"`
- **Proof:** unit and driven proof: `WebEncoderTests` assert palette size, transparency index, and monotonic size with quality, optimize-to-size lands within 5 percent under target, `ZoomifyTests` check tile counts and XML against the format, `ImageMapTests` round-trip all three map formats and parse the HTML, `ContinuousExportTests` rewrite only the changed slice, and captures are committed; cheaper substitute that fails: re-exporting every slice on each change, which the changed-slice test catches.

#### §3. Slices

- **Deliverable:** User, auto, and layer-based slices with the slice and slice select tools, slices from guides, divide, options, display, snapping, and lock, persisted in the document.
- **Depends On:** §2
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/slices/. Job: a web designer cuts a comp into named, linked images. Treatment: the slice tool with styles, the slice select tool with order, align, and distribute, a Slice Options dialog, a Divide Slice dialog, and numbered slice overlays. Cheaper substitute that fails: exporting rectangles typed by hand. Chrome: consume the moved `Slice` model, `D03 T08 §4` guides and snapping, and the history.
- **Runs:** `Requires: display-session -- the slice tools need an interactive desktop`
- **Catalog:** IP-1920 to IP-1928 (9 features)
- **Hints:**
  - Move first: the `Slice` model of `D02 T14 §17` (`src/Stilus/Isotone.Stilus.Core/Web/`) into `src/Isotone.Core/Export/Web/Slice.cs`; Gesso persists slices as `gesso:slices` through `D03 T08 §1`.
  - Slice tool (IP-1922): normal, fixed aspect ratio, fixed size, Shift square, Alt from center; slices from guides (IP-1923).
  - Slice select tool (IP-1924): stacking order, align, distribute; user and auto slices (IP-1925) with promote and hide auto slices.
  - Divide slice (IP-1926) horizontally or vertically into N parts or by pixels.
  - Slice Options (IP-1927): name, URL, target, message, alt, dimensions, background type and color.
  - Layer-based slices (IP-1921, IP-1928) following layer or group bounds, with revert to auto size.
  - Display, snapping, lock, and clear (IP-1920) under `Gesso.Slices.ShowNumbers`, `Gesso.Slices.LineColor`, `Gesso.Slices.Snap`.
  - Every slice edit is one undoable command with a Serilog line.
  - Commit: `"gesso: slices and the slice tools"`
- **Proof:** unit and driven proof: `SliceTests` cover auto-slice generation around user slices, divide, layer-based bounds following a moved layer, and a `.gesso` round trip of every field, plus a driven capture; cheaper substitute that fails: user slices only, which the auto-slice coverage test catches.

#### §4. Color settings, profiles, and display color management

- **Deliverable:** Suite-wide color settings with working spaces, policies, conversion options, custom CMYK, Assign and Convert to Profile, document profiles and indicators, display color management per view, and OpenColorIO configurations and view transforms, all on `D01 T04`, with Gesso's hand-rolled color classes retired. -> SOURCE: legacy-gesso-1.3
- **Depends On:** D01 T04 §2, D03 T08 §1
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/color-settings/, docs/captures/gesso/convert-profile/, and docs/captures/gesso/ocio/. Job: a photographer or prepress user keeps color correct from open to screen to file across the suite. Treatment: a Color Settings dialog (presets, working spaces, policies, conversion options, advanced, custom CMYK) with save and load, Assign Profile and Convert to Profile dialogs, an Image, Color Management submenu, profile indicators in the status bar and title, per-view color management toggles, and OCIO configuration and view pickers. Cheaper substitute that fails: sRGB assumed everywhere. Chrome: consume `D01 T04`, `D03 T11 §4`'s OCIO wrapper, `D03 T02 §2` and `§5` for display, and the history.
- **Runs:** `Requires: display-session -- the dialogs and the display transform on a live view need an interactive desktop`
- **Catalog:** IP-1931 to IP-1954 (24 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-1.3` (promotes B-023); delete the entry in the authoring commit.
  - Retire first: delete `src/Gesso/Isotone.Gesso.Core/Colors/ColorProfile.cs` and `SoftProofing.cs` and route every caller to `D01 T04` (`IccProfile`, `ColorTransformService`, `ProofTransform`); a grep finds no second profile type.
  - `ColorSettings` in `src/Isotone.Core/Color/Settings/`: one file `%LOCALAPPDATA%\Rizonesoft\Isotone\Color\color-settings.json` read by Stilus, Gesso, and Albumen (IP-1939), presets (General Purpose, Prepress Europe FOGRA39, Web sRGB), save and load `.isotonecolor` (IP-1938).
  - Working spaces (IP-1940, IP-1953): RGB, CMYK, gray, spot dot gain, 32-bit linear RGB, and Lab defaults; keep any RGB working space end to end (IP-1931).
  - Policies (IP-1933, IP-1936, IP-1941): off, preserve embedded, convert to working, with mismatch and missing-profile prompts on open and paste, and convert placed images.
  - Conversion options (IP-1932, IP-1942): lcms2 as the one engine, intent, black point compensation, dither for 8-bit, scene-referred compensation for 32-bit; advanced (IP-1943): desaturate monitor colors, and RGB and text blend gamma consumed by `D03 T02 §3`.
  - Custom CMYK (IP-1944): `CmykProfileBuilder` over lcms2's pipeline API (`cmsPipelineAlloc`, `cmsStageAllocCLut16bit`, `cmsSaveProfileToMem`) from inks, dot gain, GCR or UCR, black generation, black and total ink limits, and UCA through a Yule-Nielsen-modified Neugebauer model, writing an ICC v4 output profile.
  - Assign (IP-1945) and Convert to Profile (IP-1946): engine, intent, BPC, dither, flatten, advanced multichannel through `D01 T04 §3`; each one undoable command; GIMP's assign sRGB and discard profile.
  - Document profile (IP-1947) in `D03 T08 §2`'s New Document and Document Setup; status bar and title indicator (IP-1948); Image, Color Management submenu with save profile to file (IP-1949); save options embed profile and use proof setup (IP-1937).
  - Display (IP-1950, IP-1954): the per-monitor profile from `WcsGetDefaultColorProfile`, refreshed on display change and window move, per-view color-manage toggle, intent, BPC, optimize for speed (8-bit LUT) or fidelity (float), applied in `D03 T02 §2` and on the `D03 T02 §5` GPU path with CPU parity.
  - OCIO (IP-1934, IP-1935, IP-1951, IP-1952): built-in `ocio://` configs, a user config file, or `$OCIO`; display and view transforms, ACES display with exposure stops on the `D03 T15 §4` 32-bit preview, applied to exports from 32-bit, and OCIO by filename.
  - Commit: `"gesso: color settings, assign and convert, display color management, and OCIO"`
- **Proof:** unit and driven proof: Convert to Profile matches `transicc` goldens within Delta E 2000 0.5 for every intent with and without BPC, `CmykProfileBuilderTests` prove the total ink limit holds on a gamut sweep and neutrals go K-only under maximum GCR, CPU and GPU display transforms agree within 1/255, and captures are committed; cheaper substitute that fails: keeping `ColorProfile.cs` matrix math, which the CMYK goldens and the single-profile-type grep reject.

#### §5. Soft proofing and gamut warning

- **Deliverable:** Proof setups and presets, Proof Colors per view, gamut warning with color and opacity, deficient-vision proofs, Affinity's soft proof adjustment layer, GIMP's new-image proofing, and the proof status pop-over.
- **Depends On:** §4
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/soft-proof/. Job: a user sees on screen how a print condition or a color-blind viewer will see the image. Treatment: View, Proof Setup and Proof Colors, Gamut Warning, a Customize Proof Condition dialog, a soft proof adjustment layer, and a status-bar pop-over. Cheaper substitute that fails: a matrix tint that ignores the output profile. Chrome: consume `D01 T04 §2`'s `ProofTransform` and `GamutMask`, `D03 T11 §1`'s adjustment host, and the viewport.
- **Runs:** `Requires: display-session -- proofing on a live view needs an interactive desktop`
- **Catalog:** IP-1955 to IP-1968 (14 features)
- **Hints:**
  - `ProofSetup` (profile, intent, BPC, simulate paper color, simulate black ink, preserve numbers) with save and load `.isotoneproof` (IP-1956, IP-1961, IP-1966).
  - Presets (IP-1962): working CMYK, individual plates, and RGB conditions.
  - Proof Colors per view (IP-1964) through `ProofTransform` in the viewport pipeline, with the per-view state shown in the title.
  - Gamut warning (IP-1957, IP-1965, IP-1968): `GamutMask` overlay with `Gesso.Color.GamutWarningColor` and opacity.
  - Deficient vision (IP-1958, IP-1963): protanopia, deuteranopia, and tritanopia by the Machado et al. 2009 matrices at severity 1.0 in linear RGB.
  - Soft proof adjustment layer (IP-1955, IP-1967): a new adjustment kind on `D03 T11 §1`'s host with profile, intent, BPC, and gamut check, several allowed at once, hidden from export by default (`Gesso.Color.ExportSoftProofLayers`).
  - New image proofing (IP-1959) with profile, intent, and BPC, and the CMYK proof then CMYK export workflow (IP-1960) through `D03 T17 §11`'s CMYK writers.
  - Preferences (IP-1968): optimize soft proofing, mark out-of-gamut colors.
  - Commit: `"gesso: soft proofing, gamut warning, and deficient-vision proofs"`
- **Proof:** unit and driven proof: proofed renders match `transicc` proof goldens within Delta E 2000 0.5, the gamut mask of a committed fixture matches `D01 T04 §2`'s bulk mask exactly, the deficient-vision matrices reproduce the published table, and a driven capture shows each view; cheaper substitute that fails: a tint overlay, which the proof goldens reject.

#### §6. Print

- **Deliverable:** File, Print with the dialog frame moved from Stilus into Isotone.UI, preview with proofing, printer- or Gesso-managed color, hard proofing, position and size, selected-area printing, marks, print functions, PostScript options, tiled and N-up layouts, and a paper mismatch warning. -> SOURCE: legacy-gesso-7.4
- **Depends On:** §4, D02 T13 §2
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/print-dialog/ and docs/captures/gesso/print-preview/. Job: a photographer prints at the right size with correct color and marks. Treatment: the shared category-paged print dialog with Gesso pages (Color Management, Position and Size, Printing Marks, Functions, PostScript Options) and a live preview with match print colors, gamut warning, and paper white. Cheaper substitute that fails: `PrintVisual` of the canvas at screen resolution. Chrome: consume the moved frame in `src/Isotone.UI/Print/`, `D01 T04`, §5's proofing, and the status strip.
- **Runs:** `Requires: display-session -- printing to Microsoft Print to PDF and the captures need an interactive desktop`
- **Catalog:** IP-1969 to IP-1981 (13 features)
- **Hints:**
  - Carries `-> SOURCE: legacy-gesso-7.4` (promotes B-021); delete the entry in the authoring commit.
  - Move first: `PrintJobSettings`, `PrintPlanner`, `IPrintBackend` with its XPS implementation, printer listing, and the driver sheet through `DocumentPropertiesW` into `src/Isotone.Core/Print/`, and the dialog shell and mini preview of `D02 T13 §2` into `src/Isotone.UI/Print/`, with an `IPrintPageSource` seam (Stilus supplies vector visuals, Gesso supplies the composited image at print resolution); if `D03 T17 §7` has not already moved `PrinterMarksRenderer`, move it here; Stilus repointed.
  - Dialog (IP-1969, IP-1971): printer, driver settings, copies, orientation, description from `D03 T17 §10` metadata, and remembered settings under `Gesso.Print.*`; Print One Copy (IP-1970).
  - Preview (IP-1972) with match print colors, gamut warning, and paper white through §5.
  - Color handling (IP-1973): printer manages, Gesso manages (an lcms2 transform to the printer profile with intent and BPC), or separations through §7; hard proofing (IP-1974) with a proof setup and simulate paper and black ink.
  - Position and size (IP-1975): center, top and left, scale to fit, scale percent, print resolution, units; print selected area (IP-1976).
  - Marks (IP-1977): corner and center crop marks, registration, description, labels through `PrinterMarksRenderer`.
  - Functions (IP-1978): emulsion down, negative, background, border, bleed.
  - PostScript options (IP-1979): calibration bars, interpolation, include vector data (text and shape layers as vectors) through the moved `PostScriptWriter`, shown only for PostScript printers.
  - Tiled and N-up (IP-1980) through `D02 T13 §3`'s tiling in the moved planner; paper size mismatch warning (IP-1981).
  - The job runs off the UI thread with progress and Cancel; an offline printer is refused by name; one Serilog line per job.
  - Commit: `"gesso: print with Gesso-managed color and marks on the shared print dialog"`
- **Proof:** driven run plus unit test: a driven print of a committed fixture to Microsoft Print to PDF is read with PdfPig, which asserts one page, an image at the requested resolution (pixel size quoted), and marks as vector paths; with Gesso managing color, the printed image equals the `transicc` conversion to the fixture printer profile within 1/255; `PrintPlannerTests` moved from Stilus still pass; cheaper substitute that fails: `PrintVisual` of the canvas, which the resolution assertion catches.

#### §7. Print output extras, contact sheets, PDF presentation, and preflight

- **Deliverable:** Spot and overprint global colors, transfer functions, halftone screens, separations with spot plates, a preflight panel with custom rules, PDF Presentation, and Contact Sheet, on separation, halftone, and preflight engines moved from Stilus.
- **Depends On:** §6, D03 T17 §7
- **Phase:** 25
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/separations/, docs/captures/gesso/preflight/, docs/captures/gesso/contact-sheet/, and docs/captures/gesso/pdf-presentation/. Job: a prepress user sends correct separations and checks a file before it leaves; a photographer builds contact sheets and presentations. Treatment: print pages for transfer, screens, and separations, a Preflight panel with a rule editor, and File, Automate style dialogs for Contact Sheet and PDF Presentation. Cheaper substitute that fails: printing the composite for every plate. Chrome: consume the moved engines, the `D03 T17 §7` PDF writer, `D03 T16 §1` text for captions, and the status strip.
- **Runs:** `Requires: display-session -- the dialogs, panel, and captures need an interactive desktop`
- **Catalog:** IP-1982 to IP-1988 (7 features)
- **Hints:**
  - Move first: `SeparationRenderer`, `HalftoneScreen`, and `InkSet` of `D02 T13 §5` into `src/Isotone.Core/Print/`, and `PreflightEngine` of `D02 T13 §9` into `src/Isotone.Core/Preflight/`, Stilus repointed.
  - Spot and overprint global colors (IP-1982): Affinity-style global colors flagged spot or overprint, feeding `D03 T10 §10` spot channels and the separations.
  - Transfer functions (IP-1983): per-ink curves stored with the document and written to PostScript and PDF (`/TR`).
  - Halftone screens (IP-1984): frequency, angle, and shape per ink, written to EPS and PDF through `D03 T17 §7`.
  - Separations (IP-1985): one plate per process ink and spot channel, printed or saved to files.
  - Preflight (IP-1986): Gesso rules (effective resolution below a threshold, RGB content in CMYK output, out-of-gamut percentage, missing linked smart objects, missing fonts, spot channel count, total ink over limit) plus custom rules as JSON profiles, in a live panel.
  - PDF Presentation (IP-1987): open documents or files into a multi-page PDF with captions, background, and slideshow options (`/Trans`, `/Dur`, full screen) through the moved writer.
  - Contact Sheet (IP-1988): from a folder with columns, rows, sheet size and resolution, spacing, captions (file name) in `D03 T16 §1` text, flattened or layered, as a long operation with progress and Cancel.
  - One Serilog line per separation job, preflight run, and generated sheet or presentation.
  - Commit: `"gesso: separations, halftones, preflight, contact sheets, and PDF presentations"`
- **Proof:** unit and format fidelity proof: plates of a committed CMYK plus spot fixture equal the channel values within 1/255, `PreflightRuleTests` fire each rule on its fixture, a PDF Presentation reads back with PdfPig showing the page count and `/Trans` entries, and a contact sheet of a committed folder matches its golden layout; cheaper substitute that fails: composite-per-plate printing, which the plate value test catches.

#### Sizing concerns

- §4 owns 24 features plus a retirement; the natural split is color settings, policies, custom CMYK, and assign and convert (IP-1931 to IP-1933, IP-1936 to IP-1949, IP-1953) versus display color management and OCIO (IP-1934, IP-1935, IP-1950 to IP-1952, IP-1954).
- §1 owns 21 features plus a move; the natural split is Export As and Quick Export versus layers, artboards, comps, and generated assets (IP-1884 to IP-1890, IP-1900, IP-1901).
- §2 owns 18 features across three subsystems; the natural split is Save for Web with Zoomify and web filters (IP-1903 to IP-1907, IP-1915), the Export studio with continuous export and icon sets (IP-1908 to IP-1914), and the Image Map editor (IP-1902, IP-1916 to IP-1919).

### todo/03-gesso/TODO-15-gesso-parity-photo.md -- `gesso-parity-photo`

- **Title:** "TODO-15 -- Gesso Parity: the Camera Raw Filter, Develop Studio, Tone Mapping, and Photo Merges"
- **Phase(s):** 23
- **Goal:** A photographer can develop any Gesso layer through a Camera Raw filter that stays re-editable as a smart filter, work in an Affinity-style Develop studio that commits to a pixel layer or an embedded or linked RAW layer, edit and view 32-bit unbounded documents on SDR and Windows HDR displays, tone map with the HDR Toning dialog, a tone mapping studio, and the four GIMP operators, and merge photos (auto-align, Merge to HDR, panorama, image stacks, auto-blend, focus merge, astrophotography stacking, and crop and straighten of scanned photos). The develop surfaces consume the shared develop engine `D01 T07` (never a second pipeline), the tone-mapping operators are registered in the one `Isotone.Core/Imaging/Effects/` registry, and the merges live in `src/Gesso/Isotone.Gesso.Core/Photo/` on OpenCV 4 through OpenCvSharp4 (Apache-2.0) scoped to that folder, moving to `Isotone.Core` only when Albumen's backlog B-032 is promoted. Every commit is one undoable command, every live result (develop smart filter, RAW layer, tone map filter layer, stack smart object, live stack group) registers its `gesso:` element and PNG fallback with the `D03 T08 §1` contract, and no merge overwrites a source layer.
- **Current-state facts to verify (with claim candidates):**
  - There is no `Isotone.Core` project yet, so neither the develop engine this file consumes nor the effect registry the tone-mapping operators join exists today; `D01 T02 §1` creates the project and `D01 T07` the engine. `<!-- claim: absent src/Isotone.Core -->`
  - Gesso tiles hold 4 bytes per pixel (RGBA8) only, so 32-bit float HDR documents need the float tiles `D03 T08 §1` adds before §4 can run. `<!-- claim: count "PixelStride = 4" src/Gesso/src/Gesso.Core/Tiles/Tile.cs = 1 -->`
  - `BitDepth.Bpc32` exists but is modeled as a normalized float with a maximum of 1.0, the bounded assumption §4's unbounded editing removes. `<!-- claim: count "Bpc32 => 1\.0" src/Gesso/src/Gesso.Core/Documents/BitDepth.cs = 1 -->`
  - Gesso has no RAW, DNG, or develop code of any kind. `<!-- claim: count "DngReader|RawDecoder|Develop" src/Gesso/**/*.cs = 0 -->`
  - No OpenCV package is referenced anywhere in the solution; §5 adds the first and records the decision. `<!-- claim: count "OpenCvSharp" Directory.Packages.props = 0 -->`
  - No DirectX swap-chain binding is referenced; §4's HDR output adds one with a decision row. `<!-- claim: count "Vortice" Directory.Packages.props = 0 -->`
- **Inputs and XREFs:** `standards/gesso.md` (float tiles, premultiplied RGBA, SIMD with scalar reference, GPU with CPU parity, every codec owes a fidelity proof, color never changes profile silently); `standards/shared.md`; Adobe Camera Raw 18 and Photoshop 27.10 (Camera Raw filter, Merge to HDR Pro, Photomerge, stack modes, HDR Toning, Crop and Straighten Photos) and Affinity Photo 3.3 (Develop, Tone Map, New Panorama, New Stack, Focus Merge, Astrophotography Stack studios) as behavior references; GIMP 3.2.6 with GEGL 0.4.62 (`gegl:fattal02`, `gegl:mantiuk06`, `gegl:reinhard05`, `gegl:stress`, `gegl:exp-combine`) as golden reference implementations run through the `gegl` command line; OpenCV 4.10 documentation for the `detail` stitching pipeline, `AlignMTB`, `CalibrateDebevec`, `MergeDebevec`, `findTransformECC`, and AKAZE features; Debevec and Malik 1997 (radiance maps); Burt and Adelson 1983 (Laplacian pyramid blending); enfuse 4.2 (`--contrast-weight=1 --exposure-weight=0 --saturation-weight=0 --hard-mask`) as the focus-merge oracle; Siril 1.2 (GPL-3.0) as the astro calibration and sigma-clipping oracle; Lupton et al. 2004 (arcsinh stretch); Sanz et al. 2017 RCD demosaic; Adobe DNG Specification 1.7 (LinearRaw DNG writing); Microsoft Learn DXGI HDR (`DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709`, `IDXGIOutput6::GetDesc1`, `DISPLAYCONFIG_SDR_WHITE_LEVEL`); ImageMagick 7.1 `-evaluate-sequence` as the stack-mode oracle; -> XREF: D01 T07 §1 (pipeline, histogram data, auto tone the surfaces present); -> XREF: D01 T07 §2 (presence, color mixer, grading panels); -> XREF: D01 T07 §3 (detail, optics, lens profiles, geometry, crop); -> XREF: D01 T07 §4 (local masks the §2 surface edits); -> XREF: D01 T07 §5 (spot removal and red eye tools in both surfaces); -> XREF: D01 T07 §6 (presets, snapshots, before and after states, crs XMP); -> XREF: D01 T06 §1 (float effect contract the tone-mapping operators implement); -> XREF: D01 T03 §2 (resampler and rotator for workflow size and scan straightening); -> XREF: D01 T04 §2 (working-space and output transforms); -> XREF: D01 T03 §6 (classical denoise pass on merged radiance); -> XREF: D03 T02 §5 (ComputeSharp path the float display transform runs in); -> XREF: D03 T04 §3 (TIFF reader for linear DNG sources and the DNG read-back); -> XREF: D03 T11 §1 (adjustment layers the tone compression adjustment registers with); -> XREF: D03 T11 §2 (curve control reused by HDR Toning and the tone map studio); -> XREF: D03 T08 §1 (32-bit float documents and the `gesso:` contract every live result registers with); -> XREF: D03 T08 §9 (straighten and crop extensions §11 reuses); -> XREF: D03 T08 §11 (histogram and vectorscope engine the develop scopes reuse); -> XREF: D03 T09 §9 (smart objects the stack modes and develop smart filter ride); -> XREF: D03 T09 §10 (relink for linked RAW layers); -> XREF: D03 T09 §12 (align and move-tool extensions auto-align extends); -> XREF: D03 T14 §1 (smart filter host the Camera Raw filter registers in); -> XREF: D03 T11 §4 (the OpenColorIO 2 dependency §4's display transforms consume); -> XREF: D03 T11 §9 (the color panel that gains the color intensity slider); -> XREF: D03 T13 §1 (clone source panel the §9 Sources panel feeds); -> XREF: D03 T13 §3 (content-aware fill for panorama edges and missing areas); -> XREF: D03 T07 §11 (RAW import: opens RAW into §12's studio and supplies camera RAW sources to RAW layers, merges, and astro frames when it ships in Phase 31, now 41); -> XREF: D03 T17 §6 (FITS and OpenEXR codecs astro frames and HDR output use when they ship in Phase 25); -> XREF: D03 T17 §10 (EXIF exposure values for bracket EVs and the metadata panel); -> XREF: D03 T18 §4 (OCIO configuration management that later replaces §4's per-view config file choice); -> XREF: D03 T19 §4 (generative expand in the develop crop, fed by §12); -> XREF: D03 T19 §8 (AI denoise, super resolution, and detail in develop, fed by §1 and §12); -> XREF: D03 T19 §9 (generative remove in develop, fed by §12); -> XREF: D03 T19 §14 (estimated depth maps that enable the §2 depth range mask); -> XREF: D03 T19 §15 (AI develop masks that extend §2); -> XREF: D03 T20 §1 (Develop, Tone Map, Panorama, Stack, and Astro studios become workspace presets); -> XREF: D03 T20 §5 (develop preferences page over the keys §1 and §12 register).
- **Adjacency:** list=applicable (develop presets panel, stack recipes, tone-map presets, astro file groups and stacked-images panel, Sources panel); document=applicable @ D03 T18 §6 (developed, merged, and tone-mapped documents print through the normal print path; this file adds no print surface); settings=applicable (every `Gesso.Develop.*`, `Gesso.Hdr.*`, `Gesso.ToneMap.*`, and `Gesso.Photo.*` key names its consumer, surfaced by D03 T20 §5); reporting=applicable (develop histogram, clipping overlays, vectorscope, metadata and focus panels, merge and stack reports with alignment residuals); notifications=applicable (every merge, stitch, stack, and full-resolution render reports progress and cancels through the shared progress surface); permissions=applicable (missing or unreadable source files, a linked RAW whose file moved, an HDR display that is not in HDR mode, and a camera RAW source before `D03 T07 §11` ships are refusals by name); audit=applicable (each commit is one named history step with one Serilog Information line); exchange=applicable (crs XMP presets through D01 T07 §6, linear DNG render, tone-map and bad-pixel preset JSON, merge outputs as 32-bit documents); reverse=applicable (every commit undoes in one step; develop smart filters, RAW layers, tone-map filter layers, and stack smart objects re-open with their settings)

#### §1. The Camera Raw filter dialog

- **Deliverable:** `Filter, Camera Raw Filter` (Shift+Ctrl+A) opens a develop dialog over the active pixel layer or smart object with every `D01 T07` panel, histogram and clipping overlays, vectorscope, metadata and focus panels, before and after views, targeted adjustment, zoom and view tools, workflow options, presets, and Render to DNG, committing as one undo step or as a re-editable smart filter.
- **Depends On:** D01 T07 §2, D01 T07 §3, D03 T14 §1
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/camera-raw/. Job: a photographer can develop a layer with the full Camera Raw control set and come back to change it later. Treatment: a full-window modal with the image left, a histogram strip and collapsible panels (Basic, Curve, Detail, Color Mixer, Point Color, Color Grading, Optics, Geometry, Effects, Calibration, Presets, Snapshots) right, a filmstrip-free bottom bar (zoom, before and after mode, view toggles), and OK, Cancel, and Done; on a smart object OK writes a smart filter entry. Cheaper substitute that fails: a Levels-style dialog of sliders that bakes pixels and cannot reopen its settings. Chrome: consume the `D01 T07` parameter schemas to generate panels, the `D03 T08 §11` scopes, the `D03 T14 §1` smart filter host, the shared progress surface, and the theme; do not build a second develop pipeline or a second histogram.
- **Runs:** `Requires: display-session -- the dialog, before and after views, and overlay captures need an interactive desktop`
- **Catalog:** IP-1450 to IP-1465 (16 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Develop/CameraRawDialog.xaml(.cs)` with `DevelopSurfaceViewModel` in `Isotone.Gesso.Desktop/Develop/ViewModels/`; the view model owns one `DevelopSession` (source layer snapshot converted to the `D01 T07` scene-referred float space through `D01 T04 §2`, the `DevelopSettings`, preview scale) and is reused by §12's studio, so there is one develop surface for both competitors.
  - Panels are generated from `D01 T07`'s `DevelopParameterSchema` (group, label, range, default, unit) into `Isotone.Gesso.Desktop/Develop/Panels/`; per-panel reset, the active (eye) toggle that bypasses a panel, and double-click on any slider label resetting that slider (IP-1461) live in one `DevelopPanelHost`; no hand-written slider lists.
  - Smart filter (IP-1450, IP-1451): on a smart object, OK registers a `develop` filter kind with the `D03 T14 §1` host, persisted as `<gesso:smart-filter kind="develop" v="1">` whose child holds the `DevelopSettings` as crs XMP from `D01 T07 §6`, with the rendered PNG fallback per the `D03 T08 §1` contract; double-clicking the filter reopens the dialog with the exact settings. On a pixel layer OK is one `ApplyDevelopCommand` named "Camera Raw Filter" over tile snapshots.
  - Targeted adjustment tool (IP-1452, T key): dragging on the image adjusts the Point Curve region or the Color Mixer hue band under the pointer (hue band lookup from `D01 T07 §2`), with the target panel chosen from a flyout like Camera Raw.
  - Before and after (IP-1453, IP-1454): single, left and right split, left and right side by side, top and bottom split and side by side (Q cycles, P toggles preview), from the `D01 T07 §6` before state; Copy current to before, Copy before to current, and Swap, each a session step.
  - Histogram and overlays (IP-1455, IP-1456): histogram from `D01 T07 §1` data with shadow and highlight clipping triangles (U and O toggle overlays in blue and red); a vectorscope with skin-tone line and a Lab readout under the pointer reusing the `D03 T08 §11` scopes engine (not a copy).
  - Info panels (IP-1457, IP-1458): metadata from the document's `ImageMetadata` (camera, lens, exposure, ISO, focal length; "No camera metadata" when absent); autofocus points drawn from `FocusPointData` parsed from Canon and Nikon maker notes by own code against the ExifTool tag documentation, every other maker showing "Focus data is not decoded for <maker>" (honest limit).
  - Overlays (IP-1459, IP-1464): focus peaking (Laplacian magnitude above a threshold on the preview, color from `Gesso.Develop.FocusPeakingColor`, view only), geometry grid with size slider, and a loupe (L) with a 100 percent magnifier and pixel readout.
  - View tools (IP-1462): Zoom (Z), Hand (H and Space), fit, fill, 100 percent, and zoom levels to 1,600 percent, rendered at preview scale with a full-resolution tile pass for the visible region only.
  - Workflow options (IP-1463, extends `D03 T07 §11`): color space (sRGB, Display P3, Adobe RGB, ProPhoto RGB, or any output ICC profile through `D01 T04`), bit depth 8, 16, or 32 float, size by long edge or megapixels through `D01 T03 §2`, sharpen for output, and open as smart object; keys `Gesso.Develop.Workflow.ColorSpace`, `.BitDepth`, `.Size`, `.OpenAsSmartObject`, consumed by `DevelopSession.Commit`.
  - Render to DNG (IP-1460): `src/Gesso/Isotone.Gesso.FileFormats/Dng/LinearDngWriter.cs` writes DNG 1.4 LinearRaw (PhotometricInterpretation 34892, 16-bit or 32-bit float, tiled, `ColorMatrix1` for the working space, `AsShotNeutral` 1,1,1, `BaselineExposure` 0) with the edits baked and the settings stored as crs XMP marked as applied; written through the atomic writer; moves to `Isotone.Core` when Albumen exports DNG.
  - Presets and preferences (IP-1465): a Presets panel over `D01 T07 §6` presets (create, apply, favorites, groups, import XMP presets), Camera Raw defaults per camera from `D01 T07 §6`, and develop assistant defaults shared with §12, stored under `Gesso.Develop.*`.
  - Budgets: preview update after a slider change under 50 ms at screen size for a 24-megapixel source on the reference machine (rendered at preview scale), full-resolution commit under 1.5 s, cancellable; one Serilog Information line `Camera Raw Filter applied to {Layer}: {ChangedCount} settings, {ElapsedMs} ms`.
  - Tests: `DevelopSurfaceViewModelTests` (panel reset, eye toggle, double-click reset, before and after swap), `CameraRawSmartFilterTests` (settings reopen equal, fallback PNG present), `LinearDngWriterTests`.
  - Commit: "gesso: the Camera Raw filter as a develop dialog and re-editable smart filter"
- **Proof:** Unit test plus format fidelity proof plus driven run: `CameraRawSmartFilterTests` reopen a saved smart filter with settings equal field by field; the DNG written from `tests/fixtures/gesso/develop/gray-card.tif` at fixed settings is read back by `exiftool -a -G1` 12.9x into a committed tag dump and its pixels match the committed golden within 1/65535 after reading through the `D03 T04 §3` TIFF reader, and Adobe DNG SDK 1.7 `dng_validate` reports no errors (operator-run, recorded as a check); driven captures of the dialog, split view, and clipping overlays; cheaper substitute that fails: a dialog that bakes pixels, which the reopen-equal test catches.

#### §12. The Develop studio and RAW layers

- **Deliverable:** An Affinity-style Develop studio entered from any pixel layer (and from RAW files once `D03 T07 §11` ships) with Basic, Lens, Details, and Tones panels, develop assistant, lens profile favorites, crop and straighten, blemish removal, in-studio history, save from the studio, and output to a pixel layer, an embedded RAW layer, or a linked RAW layer that can be redeveloped with its previous settings.
- **Depends On:** §1, D01 T07 §6
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/develop-studio/. Job: a photographer can develop a photo in a dedicated studio and keep the develop editable as a layer. Treatment: a studio (workspace mode) with the §1 develop surface, Affinity panel grouping (Basic, Lens, Details, Tones, Overlays), a toolbar (view, crop, straighten, red eye, blemish, overlay tools), a context bar with Develop, Cancel, Output (Pixel layer, RAW layer embedded, RAW layer linked), and Develop Assistant; a History panel of settings changes inside the studio. Cheaper substitute that fails: a second develop dialog with its own sliders, or a "RAW layer" that stores only baked pixels. Chrome: consume the §1 `DevelopSession` and panel host, `D01 T07`, the `D03 T09 §10` relink, the `D03 T08 §1` contract, and the dock; do not add a second develop view model.
- **Runs:** `Requires: display-session -- entering, developing, and redeveloping in the studio are driven runs`
- **Catalog:** IP-1466 to IP-1470, IP-1472 to IP-1482 (16 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Develop/DevelopStudioView.xaml` hosting §1's `DevelopSurfaceViewModel` with the Affinity panel set (IP-1466, IP-1481): Basic (exposure, black point, brightness, contrast, saturation, vibrance, white balance, shadows and highlights), Lens (profile, favorites, distortion, perspective, rotation, scale, chromatic aberration, defringe, remove lens vignette with intensity, scale, hardness), Details (noise reduction luminance, details, contribution, colors; noise addition intensity, color, gaussian; detail refinement), Tones (curves, split toning); every control maps to a `D01 T07 §1` to `§3` parameter, so no new math (IP-1467 to IP-1470).
  - Enter, commit, cancel (IP-1472): `Develop` studio entered from the Photo studio toolbar or `Layer, Develop`; Develop commits one `DevelopCommitCommand` named "Develop" (IP-1480: the studio's History panel lists each settings change as a session step, and the commit is one document undo step); Cancel discards the session and restores the layer.
  - Any layer in any format (IP-1473): the session converts 8-bit, 16-bit, 32-bit, grayscale, Lab, or CMYK layers to the scene-referred linear float space through `D01 T04 §2` and back to the document's format on commit, with the conversion named in the commit log line.
  - `src/Gesso/Isotone.Gesso.Core/Layers/RawLayer.cs` (IP-1474, IP-1475): source bytes plus `DevelopSettings`, persisted as `<gesso:raw-layer v="1" source="data/raw/<sha256>.<ext>" | href="<path>" hash="...">` with the settings as crs XMP and the rendered PNG fallback per `D03 T08 §1`; linked sources reuse the `D03 T09 §10` relink and missing-link refusal; Redevelop reopens the studio with the previous settings; `Show all layers` toggles showing the other layers composited while developing.
  - Sources supported in this phase: any format Gesso opens (TIFF 16 and 32 bit, PNG, JPEG, and linear DNG through the `D03 T04 §3` TIFF reader); camera RAW files open into the studio when `D03 T07 §11` ships the shared decoder (IP-1471), until then `File, Open RAW into Develop` is disabled with `Planned: D03 T07 §11` through `PlannedCommands`, and a RAW layer whose source needs the decoder refuses by name.
  - Crop and geometry (IP-1476): crop with aspect presets (original, 1:1, 4:5, 5:7, 2:3, 16:9, custom), straighten by drawn line, rotate 90 either way, and trim to transparent, all through the `D01 T07 §3` geometry stage so they stay parametric in the RAW layer.
  - Save from the studio (IP-1477): `Save Image` writes the developed result through the `D03 T04` writers (and `D03 T17` formats once shipped) without committing to the document, logged.
  - Develop assistant (IP-1478, IP-1479): defaults on load (apply lens profile automatically, noise reduction off or default, tone curve "Take no action" or "Apply", exposure bias 0 EV), live mode, and alerts when a panel change is overridden (for example a tone curve reapplied); lens profile favorites and an auto-profile status line ("Profile: <maker> <lens> (lensfun)" or "No profile found"), keys `Gesso.Develop.Assistant.*` and `Gesso.Develop.LensFavorites`.
  - Blemish removal (IP-1482): the `D01 T07 §5` spot heal and clone as a studio tool with size, feather, opacity, and visualize spots.
  - One Serilog Information line per commit `Develop committed to {Output} ({Layer}): {ChangedCount} settings`; tests `DevelopStudioTests` (commit is one undo step, cancel restores bytes, any-format round trip), `RawLayerSerializationTests` (embedded and linked forms reopen with equal settings and the fallback PNG renders in GIMP 3.2.6 when renamed to `.ora`).
  - Commit: "gesso: the Develop studio and embedded and linked RAW layers"
- **Proof:** Format fidelity proof plus unit test: `RawLayerSerializationTests` save and reopen `tests/fixtures/gesso/develop/raw-layer-embedded.gesso` and `raw-layer-linked.gesso` with settings equal field by field and the embedded bytes' SHA-256 unchanged, the renamed `.ora` renders in `gimp-console` 3.2.6 within 1/255 of the fallback PNG; `DevelopStudioTests.Commit_IsOneUndoStep`; cheaper substitute that fails: a RAW layer holding only baked pixels, which the settings reopen test catches.

#### §2. Develop masking and local adjustments surface

- **Deliverable:** The masks panel, mask paint, linear gradient, radial gradient, and erase tools, range masks, add, subtract, intersect, and invert, and overlay display modes with color and opacity, editing the `D01 T07 §4` masks inside both develop surfaces.
- **Depends On:** §1, D01 T07 §4
- **Phase:** 23
- **Surface:** UI. Fidelity: extends the Camera Raw dialog -- docs/captures/gesso/camera-raw/ (from §1); new captures to docs/captures/gesso/develop-masks/. Job: a photographer can make and refine local adjustments in the develop surfaces. Treatment: a Masks panel listing masks with their components (add, subtract, intersect, invert, rename, hide, delete, duplicate) and a local adjustment slider set per mask, with brush, linear, radial, and range tools and an overlay toggle. Cheaper substitute that fails: painting a pixel layer mask outside the develop settings, which cannot travel with the smart filter or RAW layer. Chrome: consume `D01 T07 §4`'s mask model and parameter set, §1's surface, and the theme; do not add a second mask model.
- **Runs:** `Requires: display-session -- mask painting and overlay captures need an interactive desktop`
- **Catalog:** IP-1483 to IP-1485 (3 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/Develop/Masks/MasksPanel.xaml` with `MasksPanelViewModel` over the `D01 T07 §4` `DevelopMask` list (IP-1484): masks with components, per-component add, subtract, intersect, invert, rename, show or hide, delete, and duplicate and invert mask, each a session step.
  - Tools (IP-1483) in `Isotone.Gesso.Desktop/Develop/Masks/Tools/`: `DevelopBrushTool` (size, feather, flow, density, auto mask by edge awareness from `D01 T07 §4`, A and B brushes, erase mode with Alt), `LinearGradientMaskTool`, `RadialGradientMaskTool` (feather, invert, fit to bounds), and range masks (color with sample points, luminance with range and smoothness, depth disabled with `Planned: D03 T19 §14` until an estimated depth map exists).
  - Brush strokes are stored as vector strokes with pressure in the `D01 T07 §4` mask record, never as rasterized pixels, so masks survive re-opening a smart filter or RAW layer and resample with crop.
  - Overlay display modes (IP-1485): color overlay, color overlay on black and white, image on black, image on white, white on black, with color and opacity; keys `Gesso.Develop.MaskOverlay.Mode`, `.Color`, `.Opacity`, and auto show overlay, consumed by the overlay renderer.
  - AI mask entries (subject, sky, background, objects, people, landscape) appear in the Add menu disabled with `Planned: D03 T19 §15`.
  - Budget: a brush stroke updates the masked preview within 33 ms at screen size on a 24-megapixel source.
  - One Serilog Information line per mask add or delete inside the session log summary at commit; tests `MasksPanelViewModelTests` (component math, invert, rename) and `DevelopMaskPersistenceTests` (strokes round-trip inside the crs XMP of §1's smart filter).
  - Commit: "gesso: develop masks and local adjustments in the Camera Raw filter and Develop studio"
- **Proof:** Unit test plus driven run: `DevelopMaskPersistenceTests` save a smart filter with a brush, a radial, and a luminance range mask, reopen, and compare mask records and the rendered preview within 1/255; captures of each overlay mode; cheaper substitute that fails: rasterized mask pixels, which the reopen-and-resample test catches after a crop change.

#### §4. 32-bit HDR editing and HDR display

- **Deliverable:** 32-bit float documents edit with unbounded values, show through a 32-bit preview (exposure, gamma, ICC, unmanaged, or OCIO display and view), and render on Windows HDR displays through an FP16 swap chain with clip warning, reference white, and clip to peak, on by default in 32-bit views.
- **Depends On:** D03 T08 §1
- **Phase:** 23
- **Surface:** UI. Fidelity: extends the Gesso main window -- docs/captures/gesso/main-window/; new captures to docs/captures/gesso/hdr/. Job: a photographer can edit HDR images with values above 1.0 and see them as they are on an HDR display, or tone-previewed on an SDR one. Treatment: a 32-bit Preview panel (exposure, gamma, display transform ICC, unmanaged, or OCIO with display and view pickers), View, 32-bit Preview Options, and an HDR section in the View menu (Enable HDR output, clip warning, reference white nits, clip to peak). Cheaper substitute that fails: clamping float values to 1.0 on every operation, which the unbounded tests catch. Chrome: consume the `D03 T08 §1` float tiles, the `D03 T11 §4` OpenColorIO dependency, `D01 T04` transforms, and the canvas host; do not add a second color pipeline.
- **Runs:** `Requires: display-session -- HDR output needs a Windows HDR display and captures of the preview panel need an interactive desktop`
- **Catalog:** IP-1508 to IP-1519 (12 features)
- **Hints:**
  - Unbounded float (IP-1508, IP-1513): replace the normalized `Bpc32` assumption with scene-linear float where 1.0 is reference white and values above 1.0 and below 0.0 are kept by every layer operation, blend (clamped only where a blend mode's formula is undefined above 1.0, documented per mode), and filter declared float-safe by the `D01 T06 §1` contract; filters that are not float-safe are disabled in 32-bit with their tooltip.
  - `src/Gesso/Isotone.Gesso.Rendering/Hdr/FloatDisplayTransform.cs` (IP-1509, IP-1511, IP-1516, IP-1518): display exposure (EV) and gamma applied to the view only, then ICC through `D01 T04`, unmanaged, or OCIO display and view through the `D03 T11 §4` binding from a config file chosen per document (`D03 T18 §4` later manages configs); stored in the document's `gesso:view` block per `D03 T08 §1` so views reopen the same.
  - `src/Gesso/Isotone.Gesso.Rendering/Hdr/HdrSwapChainHost.cs` (IP-1510, IP-1514, IP-1517): an `HwndHost` child with a DXGI flip-model swap chain in `R16G16B16A16_FLOAT` and `DXGI_COLOR_SPACE_RGB_FULL_G10_NONE_P709` through Vortice.Windows (MIT, new decision row: WPF composition is 8-bit sRGB and has no HDR path), HDR detected with `IDXGIOutput6::GetDesc1` and the SDR white level from `DISPLAYCONFIG_SDR_WHITE_LEVEL`; falls back to the SDR canvas with a Warning when the display is not in HDR mode.
  - HDR controls: `Gesso.Hdr.Output.Enabled` (default true, IP-1514), `Gesso.Hdr.ReferenceWhiteNits` (default the system SDR white level), `Gesso.Hdr.ClipToPeak`, `Gesso.Hdr.ClipWarning` (zebra over values above the display peak), consumed by `HdrSwapChainHost`.
  - Color intensity (IP-1515): the `D03 T11 §9` color panel gains an intensity slider (EV, -10 to +10) that multiplies the picked linear color by 2^intensity for unbounded paint colors in 32-bit documents.
  - HDR in develop (IP-1512): the §1 surface gains an HDR toggle that edits in the extended range, a "visualize HDR range" overlay, and an SDR preview with its own tone settings, stored with the develop settings.
  - 32 to 16 or 8 conversion (IP-1519): `Image, Mode, 16 Bits` from a 32-bit document offers Develop (the §1 Camera Raw dialog as the tone mapper), HDR Toning (§3), or Exposure and Gamma, and remembers the choice in `Gesso.Hdr.ConvertMethod`; the conversion is one undo step "Convert to 16 Bits".
  - GPU parity: the float display transform runs in the `D03 T02 §5` ComputeSharp path with a CPU reference, parity within 1e-4 in linear values.
  - One Serilog Information line per HDR output state change and per bit-depth conversion; tests `UnboundedFloatTests` (a +2 EV value survives levels, normal blend, move, and save to `.gesso`), `FloatDisplayTransformTests` (exposure, gamma, OCIO with a committed config), `HdrCapabilityTests` (fake DXGI output reporting SDR falls back).
  - Commit: "gesso: unbounded 32-bit editing, the 32-bit preview, and HDR display output"
- **Proof:** Unit test plus driven run: `UnboundedFloatTests.ValueAboveOne_Survives` saves and reopens a 32-bit document with a 4.0 pixel through five operations exactly; `FloatDisplayTransformTests` match an `ociocheck`-validated config's `ocioconvert` 2.3 output within 1e-4; on an HDR display a driven run logs the swap-chain color space and captures the clip warning (operator machine recorded); cheaper substitute that fails: clamping at 1.0, which the round-trip test catches.

#### §3. Tone mapping and HDR Toning

- **Deliverable:** The HDR Toning dialog (Local Adaptation, Equalize Histogram, Exposure and Gamma, Highlight Compression) that opens on 32-to-lower conversion, the tone compression adjustment, the Fattal 2002, Mantiuk 2006, Reinhard 2005, and Stress operators, and a tone mapping studio with presets, enterable from any document.
- **Depends On:** §4
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/hdr-toning/ and docs/captures/gesso/tone-map-studio/. Job: a photographer can compress an HDR image into a displayable one with local contrast control, or give an 8 or 16-bit image an HDR look. Treatment: an HDR Toning modal (method, edge glow radius and strength, tone and detail gamma, exposure, detail, advanced shadow, highlight, vibrance, saturation, toning curve with histogram, presets) and a Tone Map studio (tone compression, local contrast, clamp to SDR, exposure, black point, brightness, contrast, shadows, highlights, saturation, vibrance, white balance, detail refinement, curves, presets) whose Apply creates a live tone-map filter layer. Cheaper substitute that fails: a global gamma curve labeled tone mapping, which the operator goldens reject. Chrome: consume the effect registry and `D01 T06 §1` contract, the `D03 T14 §1` live filter host, the `D03 T11 §2` curve control, and the progress surface.
- **Runs:** `Requires: display-session -- the dialog and studio captures need an interactive desktop`
- **Catalog:** IP-1486 to IP-1501 (16 features)
- **Hints:**
  - Operators in the one registry, `src/Isotone.Core/Imaging/Effects/ToneMapping/`: `Fattal02` (gradient-domain compression with alpha, beta, saturation, noise, solved by a multigrid Poisson solver), `Mantiuk06` (contrast mapping with contrast, saturation, detail), `Reinhard05` (brightness, chromatic adaptation, light adaptation), `Stress` (retinex-like envelope with radius, samples, iterations, enhance shadows), each a translation of the GEGL 0.4.62 operation (`operations/common/fattal02.c` and siblings, LGPL-3.0-or-later, compatible) implementing the `D01 T06 §1` float contract (IP-1488 to IP-1491).
  - `ToneCompression` (IP-1487, IP-1494): a realtime non-spatial operator (Reinhard 2002 global curve with a white point) usable as an adjustment layer at any bit depth, registered with `D03 T11 §1` as the Tone Compression adjustment, plus local contrast through a guided-filter base and detail split (Durand and Dorsey 2002 structure, guided filter after He et al. 2010).
  - `HdrToning` (IP-1486, IP-1501) in `Isotone.Gesso.Core/Photo/ToneMap/HdrToning.cs`: Local Adaptation (edge glow radius and strength over a bilateral base, gamma, exposure, detail, shadow, highlight, vibrance, saturation, toning curve), Equalize Histogram, Exposure and Gamma, Highlight Compression; presets as own JSON under `%LOCALAPPDATA%\Rizonesoft\Gesso\presets\hdr-toning\` (Photoshop `.hdt` files are not read: no published layout); the dialog opens when a 32-bit document converts to 16 or 8 bit through §4's convert hook.
  - Tone Map studio (IP-1492, IP-1495 to IP-1499) in `src/Gesso/Isotone.Gesso.Desktop/Photo/ToneMapStudioView.xaml`: tone compression, local contrast, clamp to SDR, exposure, black point, brightness, contrast, shadows, highlights, saturation, vibrance, white balance, detail refinement (multi-scale unsharp), and curves; 8 and 16-bit documents get the HDR look by expanding to float first; Apply creates a `<gesso:live-filter kind="tonemap" v="1">` layer through `D03 T14 §1` with the PNG fallback, and Rasterize bakes it.
  - Rasterize on enter (IP-1500): `Gesso.ToneMap.RasterizeOnEnter` (default false) merges visible layers into one float layer before entering, as its own undo step; off keeps a live filter over a merged snapshot.
  - Presets (IP-1493): built-in presets authored for the suite (Natural, Detailed, Dramatic, Monochrome, Surreal), create, rename, delete, import and export own JSON; no competitor preset files bundled.
  - Budgets: `Fattal02` on a 24-megapixel float image under 4 s, `ToneCompression` under 150 ms (live adjustment), studio preview under 100 ms at screen size; all cancellable.
  - One Serilog Information line per apply `Tone map {Operator} applied: {ParameterHash}, {ElapsedMs} ms`; tests `ToneMappingGoldenTests` and `HdrToningTests`.
  - Commit: "gesso: HDR Toning, tone compression, the GIMP tone-mapping operators, and the tone map studio"
- **Proof:** Golden proof: `ToneMappingGoldenTests` run each operator on `tests/fixtures/imaging/tonemap/memorial-small.exr` (a suite-authored HDR render, not a third-party image) and compare with `gegl` 0.4.62 CLI outputs committed with their exact commands in `reference.txt`, within mean delta 1/255 and max 4/255 after an sRGB encode; cheaper substitute that fails: a global gamma curve, which the Fattal and Mantiuk goldens reject.

#### §5. The image alignment engine and auto-align layers

- **Deliverable:** An OpenCV-backed alignment engine in `Isotone.Gesso.Core/Photo/Alignment/` (features, matching, translation, similarity, affine, perspective, cylindrical, and spherical models, ECC refinement, lens correction before matching) and `Edit, Auto-Align Layers` with Auto, Perspective, Collage, Cylindrical, Reposition, and Spherical projections.
- **Depends On:** D03 T09 §12
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/auto-align/. Job: a photographer can line up bracketed, handheld, or overlapping layers before merging them. Treatment: an Auto-Align Layers dialog with projection radio buttons (Auto, Perspective, Collage, Cylindrical, Reposition, Spherical) and Lens Correction checkboxes (Vignette Removal, Geometric Distortion), applying one undo step named "Auto-Align Layers" and a report of residual error per layer. Cheaper substitute that fails: aligning by phase correlation translation only, which the rotation and scale fixtures reject. Chrome: consume the `D03 T09 §12` align commands and move tool transforms, the `D01 T07 §3` lens profiles, and the progress surface.
- **Runs:** `Requires: display-session -- the dialog capture and a driven align of the committed fixture need an interactive desktop`
- **Catalog:** IP-1520 to IP-1522 (3 features)
- **Hints:**
  - Dependency: add OpenCvSharp4 and OpenCvSharp4.runtime.win 4.10 (Apache-2.0 both, OpenCV 4.10 Apache-2.0) to `Directory.Packages.props`, referenced only by `Isotone.Gesso.Core`; a `docs/dev/decisions.md` row with the GPL-3.0 check, the installer size delta, and the rule that pixel filters stay in the managed engine; an architecture test asserts no `OpenCvSharp` type is used outside `Isotone.Gesso.Core/Photo/`.
  - `Photo/OpenCv/MatBridge.cs`: tile store to `Mat` (CV_32FC3 or CV_16UC3) and back with pooled buffers, downscaled to a 2-megapixel working copy for feature detection; no `Mat` escapes the Photo namespace.
  - `Photo/Alignment/ImageAligner.cs` with `AlignmentModel { Translation, Euclidean, Similarity, Affine, Perspective, Cylindrical, Spherical }`: AKAZE features by default (SIFT optional), brute-force matching with Lowe's 0.75 ratio test, RANSAC through `findHomography` or `estimateAffinePartial2D`, then sub-pixel refinement with `findTransformECC` (Evangelidis and Psarakis 2008) on the full-resolution luminance.
  - Lens correction before matching (IP-1521): vignette and distortion from the `D01 T07 §3` lensfun profile applied to the working copies (and to the layers when the checkbox asks), recorded per layer.
  - `AutoAlignLayersCommand` (IP-1520, IP-1522): the reference is the selected top layer or the one with most matches; results apply as each layer's transform (smart objects keep a live transform, pixel layers resample through `D01 T03 §2` bicubic) in one undo step; cylindrical and spherical warp through the OpenCV warpers.
  - Refusals by name: fewer than 12 inlier matches ("<Layer> has too little overlap to align"), mixed bit depths resolved by converting working copies only.
  - Budget: 5 layers of 24 megapixels aligned under 6 s on the reference machine, peak working memory under 1 GB, cancellable between layers.
  - One Serilog Information line `Auto-aligned {Count} layers ({Model}): residual {MeanPx} px`; tests `ImageAlignerTests` over synthetic fixtures with known transforms and `OpenCvScopeGuardTests`.
  - Commit: "gesso: the OpenCV alignment engine and Auto-Align Layers"
- **Proof:** Unit test: `ImageAlignerTests` recover committed transforms (shift, 3 degree rotation, 4 percent scale, and a homography) applied to `tests/fixtures/gesso/photo/align-base.png` (suite-authored) within 0.25 px mean corner error, and Hugin 2023 `align_image_stack` results on the same inputs are recorded in `reference.txt` as the comparison; cheaper substitute that fails: translation-only phase correlation, which the rotation and scale fixtures reject.

#### §6. Merge to HDR

- **Deliverable:** `File, Automate, Merge to HDR` and an Affinity-style HDR merge with a source list, bracket EVs, auto align, ghost removal, noise reduction, response-curve recovery, 32-bit white point preview, output bit depth, a staged preview, an after-merge action, and hand-off to the develop filter.
- **Depends On:** §5, §3
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/merge-to-hdr/. Job: a photographer can combine bracketed exposures into one HDR image without ghosts. Treatment: a dialog with the source list (files or open documents, thumbnails, EV per source), options (auto align, remove ghosts with base image choice, noise reduction, response curve Linear or Recovered), a staged preview, a white point slider for the 32-bit preview, output (32-bit, or 16 or 8 through §3), and after-merge action (Tone Map studio, tone compression adjustment, Camera Raw filter, none). Cheaper substitute that fails: averaging the brackets, which the radiance fixture rejects. Chrome: consume the §5 aligner, §3's HDR Toning and studio, §1's dialog, §4's float preview, and the progress surface.
- **Runs:** `Requires: display-session -- the merge dialog and staged preview are driven runs`
- **Catalog:** IP-1523 to IP-1528, IP-1530 (7 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Photo/Hdr/HdrMerger.cs` (IP-1523, IP-1524): exposure values from EXIF (`ExposureTime`, `FNumber`, `ISOSpeedRatings`) when present or entered per source; response curve recovered with OpenCV `CalibrateDebevec` for display-referred inputs or taken as linear for linear inputs; radiance merged with `MergeDebevec` weights (Debevec and Malik 1997); output a new 32-bit document.
  - Alignment (IP-1525): §5 with the perspective or scaling (similarity) model chosen in the dialog.
  - Ghost removal (IP-1526): after radiance normalization, pixels where sources disagree beyond a threshold (default 10 percent in log radiance) take only the chosen base exposure, with the ghost mask shown in the staged preview and feathered 8 px.
  - Noise reduction (IP-1527): weighting that favors mid-tone samples of the longest exposure for shadows, plus an optional `D01 T03 §6` denoise pass on the merged radiance.
  - Options and preview (IP-1530): staged preview at screen size, 32-bit white point preview slider feeding §4's display exposure, output bit depth 32, 16, or 8 (16 and 8 run §3's HDR Toning), and "Complete toning in the Camera Raw filter" opening §1 on the result.
  - After-merge action (IP-1528): `Gesso.Photo.Hdr.AfterMerge` (ToneMapStudio, ToneCompression, CameraRaw, None).
  - Merge sources (IP-1529): the aligned sources are kept in the result document as a `<gesso:merge-sources v="1">` set (embedded PNG or TIFF per source, EV, transform) per `D03 T08 §1`; the Sources panel that lists them for clone retouching is built by §9, which reads this set.
  - Budget: 5 brackets of 24 megapixels merged under 12 s with peak memory under 3 GB, cancellable; one Serilog Information line `Merged {Count} exposures to HDR ({Response}, ghosts {GhostPercent} percent)`.
  - Tests: `HdrMergerTests` over a synthetic bracket rendered from `tests/fixtures/imaging/tonemap/memorial-small.exr` with a known response curve, and `GhostRemovalTests` with a moving square.
  - Commit: "gesso: Merge to HDR with alignment, ghost removal, and response recovery"
- **Proof:** Golden proof plus unit test: `HdrMergerTests` recover the source radiance within 2 percent relative error on well-exposed pixels and compare with `gegl` 0.4.62 `gegl:exp-combine` output (command in `reference.txt`) within 3 percent; `GhostRemovalTests` show no ghost of the moving square; cheaper substitute that fails: averaging display values, which the radiance comparison rejects.

#### §7. Panorama

- **Deliverable:** Photomerge and an Affinity-style panorama studio that stitch images from files, folders, or open documents with Auto, Perspective, Cylindrical, Spherical, Collage, and Reposition layouts, blending, vignette removal, distortion correction, source transforms and masks, multiple panorama detection, crop to opaque, and content-aware fill of transparent edges.
- **Depends On:** §5
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/panorama/. Job: a photographer can stitch overlapping photos into one panorama and fix its seams and edges. Treatment: a Photomerge dialog (layout radio buttons, source list with Browse and Add Open Files, Blend Images Together, Vignette Removal, Geometric Distortion Correction, Content-Aware Fill Transparent Areas) and a Panorama studio (image list with preview, navigation, transform source image tool, source mask add and erase, crop and crop to opaque, inpaint missing areas, Apply). Cheaper substitute that fails: laying images side by side by translation only. Chrome: consume the §5 engine and OpenCV `detail` pipeline, the `D03 T13 §3` content-aware fill, `D01 T07 §3` lens profiles, and the progress surface.
- **Runs:** `Requires: display-session -- the studio and a driven stitch of the fixture need an interactive desktop`
- **Catalog:** IP-1531 to IP-1539 (9 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Photo/Panorama/PanoramaStitcher.cs` over the OpenCV `detail` API: AKAZE features, `BestOf2NearestMatcher` (affine variants for Collage and Reposition), `BundleAdjusterRay`, plane, cylindrical, and spherical warpers for Perspective, Cylindrical, and Spherical, wave correction, `GraphCutSeamFinder`, `BlocksGainCompensator` (vignette and exposure), and `MultiBandBlender` (IP-1537, IP-1538, IP-1539).
  - Auto layout picks Perspective when the field of view is under 120 degrees and Cylindrical otherwise; Reposition aligns without distortion; Collage allows rotation and scale only.
  - Multiple panoramas (IP-1532): the match graph is split into connected components above a confidence threshold, each stitched as its own result, listed in the studio.
  - Sources (IP-1531, IP-1538): files, a folder, or open documents; the studio image list with preview and navigation; geometric distortion correction applies the `D01 T07 §3` lens profile before matching.
  - Studio tools (IP-1533, IP-1534): Transform Source Image moves, rotates, and scales one source's placement and re-blends; Source Image Mask brush adds or erases a source's contribution; both stored in the stitch session until Apply.
  - Output (IP-1535, IP-1536): Photomerge output is a new document with one masked pixel layer per source (seam masks) so the user can refine seams; the studio's Apply outputs one pixel layer plus an optional source-layer group; crop, crop to opaque (largest inscribed rectangle), and inpaint missing areas through `D03 T13 §3` as a separate undoable step on a new layer.
  - Budget: 10 sources of 24 megapixels stitched under 60 s with composition in 16-bit bands and peak memory under 3 times the output's float size, cancellable per stage with progress.
  - One Serilog Information line `Panorama stitched {Count} sources ({Layout}) to {Width}x{Height}`; tests `PanoramaStitcherTests` and `PanoramaGroupingTests`.
  - Commit: "gesso: Photomerge and the panorama studio"
- **Proof:** Unit test plus driven run: `PanoramaStitcherTests` cut three overlapping crops with known offsets and a 2 degree rotation from `tests/fixtures/gesso/photo/pano-source.png` (suite-authored), stitch them, and recover placements within 1 px and seam delta under 3/255 on the overlap band; `PanoramaGroupingTests` split two unrelated sets into two panoramas; cheaper substitute that fails: translation-only placement, which the rotated crop rejects.

#### §8. Image stacks and auto-blend layers

- **Deliverable:** Smart object stack modes (mean, median, outlier, maximum, minimum, range, mid-range, total, standard deviation, variance, skewness, kurtosis, entropy), Affinity live stack groups with a per-layer alignment filter, stack recipes, and Auto-Blend Layers with Panorama and Stack Images modes, seamless tones, and fill of transparent areas.
- **Depends On:** §5, D03 T09 §9
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/stacks/ and docs/captures/gesso/auto-blend/. Job: a photographer can combine many frames statistically to remove noise or people, or blend overlapping layers seamlessly. Treatment: `Layer, Smart Objects, Stack Mode` submenu, `File, New Stack` creating a live stack group with an operator combo in the Layers panel, stack recipes in a menu, and an Auto-Blend Layers dialog (Panorama or Stack Images, Seamless Tones and Colors, Content Aware Fill Transparent Areas). Cheaper substitute that fails: flattening the frames into one pixel layer, which loses the ability to change the mode. Chrome: consume `D03 T09 §9` smart objects, the §5 aligner, `D03 T13 §3`, and the Layers panel.
- **Runs:** `Requires: display-session -- the stack menu, live stack group, and dialog captures need an interactive desktop`
- **Catalog:** IP-1540 to IP-1550 (11 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Photo/Stacks/StackReducer.cs` with `StackMode` for every mode (IP-1546, IP-1547, IP-1550): tile-streamed over N layers (reads one 256 px tile per layer at a time), SIMD per pixel with a scalar reference, median by quickselect for N up to 256, outlier as mean after rejecting samples beyond 2 sigma (Affinity's outlier rejection), entropy over a 256-bin histogram per pixel.
  - Smart object stack mode (IP-1542): stored on the smart object as `gesso:stack-mode="median"` in its `D03 T09 §9` element with the rendered fallback; changing the mode is one undo step "Stack Mode: Median".
  - Live stack group (IP-1543, IP-1545): `File, New Stack` builds `<gesso:live-stack v="1" operator="median">` group whose children each carry a live alignment filter (the §5 transform stored as a `D03 T14 §1` live filter), so frames can be toggled, re-aligned, and removed live.
  - Stack auto-align (IP-1544): §5 with perspective or scaling models chosen at creation.
  - Recipes (IP-1548): Exposure Merge (mean), Noise Reduction (median), Object Removal (median with outlier), Light Trails (maximum), as own JSON presets with the operator and alignment model.
  - `Photo/Blend/AutoBlender.cs` (IP-1540, IP-1541, IP-1549): Panorama mode computes seam masks by graph cut on the overlaps and blends with Laplacian pyramids (Burt and Adelson 1983) with gain compensation for seamless tones; Stack Images mode computes per-pixel sharpness (Laplacian energy in a 5 px window) and selects with hard masks blended through pyramids; results are layer masks on the source layers (Photoshop's output), never baked pixels; Fill Transparent Areas runs `D03 T13 §3` on a new layer. §9's focus merge reuses this Stack Images engine.
  - Budget: median of 20 layers of 24-megapixel 16-bit frames under 10 s with memory bounded to one tile per layer plus the output tile.
  - One Serilog Information line per stack mode change and per auto-blend; tests `StackReducerTests` and `AutoBlenderTests`.
  - Commit: "gesso: stack modes, live stacks, and Auto-Blend Layers"
- **Proof:** Golden proof plus unit test: `StackReducerTests` compare mean, median, maximum, and minimum of `tests/fixtures/gesso/stacks/frames-*.png` with ImageMagick 7.1 `-evaluate-sequence` outputs (commands in `reference.txt`) exactly for 8-bit integer modes, and the statistical modes with a committed `reference.py` (numpy 2.x) golden within 1e-5; `AutoBlenderTests` prove the source layers' pixels are byte-identical after blending (masks only); cheaper substitute that fails: flattening to one layer, which the byte-identity test catches.

#### §9. Focus merge

- **Deliverable:** Affinity-style focus merge with staged preview, a RAW development preset applied to sources, the Sources panel of global clone sources (preview, add, delete) that also lists HDR merge sources, and cloning from any source into the result.
- **Depends On:** §5, §8
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/focus-merge/ and docs/captures/gesso/sources-panel/. Job: a macro or product photographer can merge a focus bracket into one sharp image and retouch halos from the original frames. Treatment: `File, New Focus Merge` with a file list, develop preset, and staged preview; the result opens with a Sources panel (thumbnails, preview on hover, Add, Delete) whose selected source is the clone tool's source. Cheaper substitute that fails: a merge that discards the frames, leaving nothing to clone halos from. Chrome: consume §8's Stack Images engine, the §5 aligner, the `D03 T13 §1` clone source model, `D01 T07 §6` presets, and the dock.
- **Runs:** `Requires: display-session -- the focus merge and source cloning are driven runs`
- **Catalog:** IP-1529, IP-1551 to IP-1554 (5 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Photo/Focus/FocusMerger.cs` (IP-1551): §5 alignment with the similarity model (focus breathing), then §8's `AutoBlender` Stack Images mode (sharpness selection plus pyramid blending) into a new document; staged preview at screen size before full resolution.
  - RAW development preset (IP-1552): a `D01 T07 §6` preset applied to every source through `DevelopSession` before merging (camera RAW sources arrive with `D03 T07 §11`).
  - Sources (IP-1554): `<gesso:sources v="1">` in the document (embedded frames with their alignment transforms) per `D03 T08 §1`, listed by `src/Gesso/Isotone.Gesso.Desktop/Panels/SourcesPanel.xaml` with thumbnails, hover preview, Add (file or layer), and Delete (undoable); the panel also lists the `gesso:merge-sources` set §6 writes (the IP-1529 retouching path).
  - Source cloning (IP-1553): selecting a source sets the `D03 T13 §1` clone tool's source to that frame in aligned coordinates, so healing, patch, and clone paint from it; this section adds the `GlobalCloneSource` kind to the `D03 T13 §1` source model rather than a second clone tool.
  - Budget: 15 frames of 24 megapixels merged under 40 s, sources stored at full resolution with the document size shown before saving.
  - One Serilog Information line `Focus merged {Count} frames`; tests `FocusMergerTests`, `SourcesPanelViewModelTests`, `GlobalCloneSourceTests`.
  - HDR merge sources (IP-1529) join the same sources panel, so the retouch-from-source brushes work after Merge to HDR too.
  - Commit: "gesso: focus merge and the Sources panel"
- **Proof:** Golden proof plus unit test: `FocusMergerTests` merge `tests/fixtures/gesso/photo/focus-*.png` (suite-rendered synthetic depth-of-field bracket with a known all-in-focus truth) and reach mean absolute error under 2/255 against the truth, compared also with enfuse 4.2 (`--contrast-weight=1 --exposure-weight=0 --saturation-weight=0 --hard-mask`, command in `reference.txt`); `GlobalCloneSourceTests` clone one stroke from frame 3 and match its pixels; cheaper substitute that fails: picking the sharpest whole frame, which the truth comparison rejects.

#### §10. Astrophotography stacking

- **Deliverable:** An astrophotography stack studio with file groups for lights, darks, flats, biases, and dark flats, narrowband tags, calibration, bad pixel maps, best-frame selection, background calibration, star alignment, mean, median, and sigma-clipped stacking, and astro filters (tone stretch, background removal, linear fit, color calibration, star and luminosity separation, color mapping, structure enhancement).
- **Depends On:** §8
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/astro-stack/. Job: an astrophotographer can calibrate, align, and stack sub-exposures and stretch the faint result without leaving Gesso. Treatment: an Astrophotography Stack studio with a Files panel (groups, frame type, narrowband tag, add and remove), options (demosaic method, white balance, subtract black level, stacking method with threshold and iterations, best-frame percentage), a Bad Pixel Map tool, a Stacked Images panel, Stack and Apply as layers, with Align by Stars and Color Map buttons; astro filters in `Filter, Astrophotography`. Cheaper substitute that fails: a mean of uncalibrated frames, which the synthetic hot-pixel and vignetting fixture rejects. Chrome: consume §8's `StackReducer`, the §5 aligner for refinement, the `D03 T14 §1` live filter host for stretches, the progress surface, and the dock.
- **Runs:** `Requires: display-session -- the studio run on the synthetic star field and captures need an interactive desktop`
- **Catalog:** IP-1555 to IP-1578 (24 features)
- **Hints:**
  - Studio and files (IP-1561, IP-1562, IP-1564, IP-1565, IP-1570): `src/Gesso/Isotone.Gesso.Desktop/Photo/AstroStackStudioView.xaml` with the Files panel (groups, frame type Light, Dark, Flat, Bias, Dark Flat, narrowband tag L, R, G, B, Ha, OIII, SII for simultaneous per-tag stacks), a Stacked Images panel, Stack, and Apply as layers (one layer per tag); frames load through the open formats (TIFF, PNG, linear DNG now; FITS when `D03 T17 §6` ships and camera RAW when `D03 T07 §11` ships, both through one `IAstroFrameSource` registry).
  - Calibration (IP-1563, IP-1567): `Photo/Astro/CalibrationMasterBuilder.cs` builds master bias, dark (bias-subtracted), dark flat, and flat (normalized) by median or sigma clip, then light = (L - D) / F times mean(F), with background calibration normalizing light backgrounds by median and MAD.
  - Bad pixels (IP-1573 to IP-1575): `Photo/Astro/BadPixelMap.cs` detects hot and cold pixels from the master dark by thresholds on median plus k times MAD, manual marking by pixel or column, show, Bayer view, reset, and presets as own JSON; corrected by CFA-aware median of same-color neighbors.
  - Demosaic and white balance (IP-1569): CFA frames with a declared Bayer pattern (from DNG `CFAPattern` or a user setting) demosaic after calibration with bilinear, super-pixel, or RCD (Sanz et al. 2017, as in Siril and RawTherapee), because calibration must happen in the CFA domain before any decoder demosaic; white balance multipliers and subtract black level options.
  - Best frames (IP-1566): score each light by star count, median FWHM, and background noise, keep the top percentage (`Gesso.Photo.Astro.KeepBestPercent`, default 90).
  - Star alignment (IP-1560, IP-1576): `Photo/Astro/StarDetector.cs` (local maxima above background plus 5 sigma, centroid, FWHM) and `StarAligner.cs` (triangle similarity matching after Valdes et al. 1995, then the §5 engine's `estimateAffinePartial2D` refinement).
  - Stacking (IP-1568): mean, median, and sigma clipping (threshold and iterations) through §8's `StackReducer` with a `SigmaClip` mode added there.
  - Tone stretch (IP-1555, IP-1572, IP-1578): `Photo/Astro/ToneStretch.cs` with basic (midtones transfer function), arcsinh (Lupton et al. 2004), logarithmic, and auto (median plus 2.8 MAD target, used for FITS), as a live filter layer and as a display-only live stretch in the studio.
  - Background and color (IP-1556, IP-1558, IP-1571, IP-1577): `BackgroundExtractor` (sample handles on a grid or placed by hand, radius, polynomial degree 1 to 4 or RBF surface, gray or RGB subtraction, output black level; classical gradient and light pollution subtraction), linear fit (per-channel regression to a reference channel, as Siril's linear match), color calibration (background neutralization plus a white reference from a selection), and color map mono layers (hue per layer, additive composite, HOO and SHO presets).
  - Separation and structure (IP-1557, IP-1559): separate luminosity and color into two layers, separate stars and background (classical star mask from `StarDetector` dilated, starless layer by local median inpainting; not a neural star remover), and enhance structure by multi-scale local contrast on the starless layer; each output is new layers.
  - Budget: 50 lights of 24 megapixels plus 20 of each calibration type stacked under 5 minutes, tile-streamed so memory stays under 2 GB, cancellable per stage; one Serilog Information line per stack `Astro stacked {Lights} lights ({Method}), rejected {Rejected} frames`.
  - Tests: `CalibrationTests`, `BadPixelMapTests`, `StarAlignerTests`, `AstroStackTests`, `ToneStretchTests` over a deterministic synthetic star field generator in `tests/Isotone.Gesso.Core.Tests/Photo/Astro/StarFieldGenerator.cs` (Gaussian PSFs, read noise, hot pixels, vignetting flat, known shifts).
  - Commit: "gesso: the astrophotography stack studio and astro filters"
- **Proof:** Golden proof plus unit test: `AstroStackTests` stack 30 synthetic lights with darks and flats and recover the noiseless truth within a stated SNR gain (at least 4.5 times the single-frame SNR) with every planted hot pixel removed; the sigma-clipped stack of the committed small set `tests/fixtures/gesso/astro/` matches Siril 1.2 output (script in `reference.txt`) within 1e-3 normalized; cheaper substitute that fails: a mean of uncalibrated frames, which leaves the planted hot pixels and vignetting.

#### §11. Crop and straighten scanned photos

- **Deliverable:** `File, Automate, Crop and Straighten Photos` finds each photo on a scanned page, straightens it, and opens each as a new document.
- **Depends On:** D03 T08 §9
- **Phase:** 23
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/crop-straighten-photos/. Job: a user can split a scanner bed of several photos into straight separate images in one command. Treatment: a menu command that runs with progress and opens one document per detected photo, with a selection limiting detection to one photo (Alt-click in Photoshop terms). Cheaper substitute that fails: cropping to the bounding box of all content. Chrome: consume the `D03 T08 §9` straighten, `D01 T03 §2` rotator, the OpenCV bridge of §5, and the document tabs.
- **Runs:** `Requires: display-session -- a driven run on the committed scan fixture opens the documents`
- **Catalog:** IP-1579 (1 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Photo/Scans/ScanPhotoSplitter.cs`: estimate the scanner background from the border (median color), threshold the difference, close gaps morphologically, find connected components above 2 percent of the page, fit `minAreaRect`, and refine the angle from the dominant edge direction.
  - Each photo is rotated and cropped through the `D01 T03 §2` rotator with bicubic sampling into a new document named `<scan> (1)`, `<scan> (2)`, keeping resolution and profile; the source document is unchanged.
  - With an active selection, only the photo inside it is processed.
  - The Automate submenu holds only this command and Merge to HDR until batch processing (B-042) arrives.
  - One Serilog Information line `Crop and Straighten Photos found {Count} photos in {Document}`; tests `ScanPhotoSplitterTests`.
  - Commit: "gesso: Crop and Straighten Photos"
- **Proof:** Unit test: `ScanPhotoSplitterTests` run on `tests/fixtures/gesso/photo/scan-three.png` (suite-authored: three photos rotated by 4, -7, and 12 degrees on a textured bed) and find three documents with angles within 0.3 degree and edges within 3 px of the truth; cheaper substitute that fails: one crop around all content, which the count assertion rejects.

#### Sizing concerns

- §10 owns 24 features across two jobs (calibration, alignment, and stacking; then post-stack astro filters) and its hints will expand to about 28 items; the natural split is §10 "Astrophotography stacking" (IP-1560 to IP-1570, IP-1573 to IP-1576) and a new "Astrophotography filters" section (IP-1555 to IP-1559, IP-1571, IP-1572, IP-1577, IP-1578) depending on §10.
- §1 (16 features) and §12 (17 features) each include a file writer or a new layer kind beside the surface; if §1 exceeds 30 items at authoring, move Render to DNG (IP-1460) to §12, which already owns the develop output paths.

### todo/03-gesso/TODO-19-gesso-ai.md -- `gesso-ai`

- **Title:** "TODO-19 -- Gesso AI: Editable, Suite-Aware, Reproducible"
- **Phase(s):** 26
- **Goal:** Gesso's AI is its own design built on the suite's pillars, not a clone of Firefly, Canva AI, or GIMP plug-ins. Every result is editable and never destructive: a generation lands as a new pixel layer with a layer mask inside a named group, variations as hidden siblings; an AI selection lands as a selection or a layer mask; an assistant edit lands as adjustment layers, masks, and filter layers built from schema-validated JSON; each apply is one named undoable command and no source pixel is overwritten. Image generation runs through OpenRouter's image models with honest limits stated in the UI and the help: masked crops with context padding, size caps with tiling and overlap, seeds recorded with whether the model honored them, estimated (never measured) depth, and cautions before faces are sent. Selections come from locating, not guessing pixels: a vision model returns boxes, points, and labels as JSON and the local segmentation engine `D03 T10 §6` makes the pixel mask, so the same selections work offline in Local mode. It is suite-aware (the `D01 T05 §5` brand kit in a Brand Kits panel and in prompts, file hand-offs with Albumen and Stilus through `SuiteAppLocator`) and reproducible (a provenance record per action inside the `.gesso` document, a panel that re-runs, compares, and reverts, optional XMP export). All of it lives in `src/Gesso/Isotone.Gesso.Core/AI/` and `src/Gesso/Isotone.Gesso.Desktop/AI/`, consumes the `D01 T05` client, key store, send gate, provenance, and brand kit, never talks HTTP itself, and sends nothing without an explicit action and a send preview.
- **Current-state facts to verify (with claim candidates):**
  - Gesso contains no HTTP client and no OpenRouter code; every request in this file goes through `D01 T05`. `<!-- claim: count "HttpClient" src/Gesso/**/*.cs = 0 -->` `<!-- claim: count "OpenRouter" src/Gesso/**/*.cs = 0 -->`
  - There is no segmentation or matting code in Gesso today; the local engine AI selections feed is `D03 T10 §6`. `<!-- claim: count "GrabCut|Segmentation" src/Gesso/**/*.cs = 0 -->`
  - Selections and layer masks are already 8-bit byte masks, the form every AI selection and mask result must land in. `<!-- claim: count "private byte\[\]\? _mask;" src/Gesso/src/Gesso.Core/Selections/Selection.cs = 1 -->` `<!-- claim: count "private byte\[\]\? _data;" src/Gesso/src/Gesso.Core/Masks/LayerMask.cs = 1 -->`
  - An `AdjustmentLayer` model type exists (57 lines) that the assistant's structured edits will instantiate once `D03 T11 §1` makes it live. `<!-- claim: lines src/Gesso/src/Gesso.Core/Layers/AdjustmentLayer.cs = 57 -->`
  - The shared AI core does not exist yet: there is no `Isotone.Core`. `<!-- claim: absent src/Isotone.Core -->`
- **Inputs and XREFs:** `standards/gesso.md`; `standards/shared.md` (one Information line per document change, no app depends on another at runtime); the recorded decision "AI: Gesso's own, built on three pillars" in `docs/parity/gesso-parity.md`; the OpenRouter API reference (image output, image input, structured output) through `D01 T05 §1`; Rother, Kolmogorov, and Blake 2004 (GrabCut) and He, Sun, and Tang 2010 (guided filter) as the local engine references behind `D03 T10 §6`; Reinhard et al. 2001 (color transfer) for seam color match and harmonization; Hou and Zhang 2007 (spectral residual saliency) for the Local-mode subject seed; Banterle et al. 2006 (inverse tone mapping) for SDR to HDR; -> XREF: D01 T05 §1 (client, image generate and edit, structured output); -> XREF: D01 T05 §2 (key store and per-task model settings Gesso extends); -> XREF: D01 T05 §3 (provenance record, store, re-run, and diff embedded in the `.gesso` document); -> XREF: D01 T05 §4 (send gate, send preview, AI settings page, progress panel, usage indicator); -> XREF: D01 T05 §5 (brand kit library and `BrandKitConstraint`); -> XREF: D02 T15 §1 (the Stilus precedent for the AI menu and provenance panel whose shared parts stay in `Isotone.UI`); -> XREF: D02 T15 §7 (the `FontMatcher` §11 moves to `Isotone.Core/Text/` as its second consumer); -> XREF: D02 T15 §11 (`SuiteAppLocator`, the hand-off folder, and sidecar provenance §13 consumes); -> XREF: D04 T02 §7 (Albumen's Edit in Gesso, which §13 receives); -> XREF: D03 T08 §1 (the `gesso:` contract for provenance, generative layers, and AI smart filters); -> XREF: D03 T08 §7 (canvas and image size for expand and super resolve document); -> XREF: D03 T08 §9 (the crop tool's content-aware fill hook generative expand joins); -> XREF: D03 T09 §1 (layer kinds and groups results land in); -> XREF: D03 T09 §3 (layer masks every result carries); -> XREF: D03 T09 §9 (smart objects for placed brand logos); -> XREF: D03 T10 §1 (the selection model AI selections return into); -> XREF: D03 T10 §6 (the local segmentation engine every AI selection and mask uses); -> XREF: D03 T10 §7 (Select and Mask, the refine entry of object selection and sky edges); -> XREF: D03 T11 §1 (adjustment layers and the Properties panel the assistant and quick actions use); -> XREF: D03 T11 §2 (classical auto tone and auto color beside AI adjust); -> XREF: D03 T11 §10 (swatches the brand kit palettes join); -> XREF: D03 T13 §2 (classical Remove and healing, the off and auto modes of generative remove, blemish healing); -> XREF: D03 T13 §3 (content-aware fill, the classical fill of distraction removal and crop fill); -> XREF: D03 T13 §9 (face-aware liquify, fed by §11's landmarks); -> XREF: D03 T14 §1 (the live filter host AI smart filters register with); -> XREF: D03 T15 §1 (develop surface for adaptive profile and develop enhance); -> XREF: D03 T15 §2 (develop masks panel §15's AI masks extend); -> XREF: D03 T15 §4 (32-bit documents SDR to HDR writes into); -> XREF: D03 T15 §12 (develop crop and studio for generative expand, remove, and enhance in develop); -> XREF: D03 T16 §1 (text layers brand type styles apply to); -> XREF: D03 T16 §2 (the font list Match Font ranks); -> XREF: D03 T17 §10 (XMP writing for provenance export); -> XREF: D01 T03 §2 (Lanczos resampler for local fitting and the upscale fallback); -> XREF: D01 T03 §6 (classical scratch, dust, and JPEG artifact passes in restoration and super zoom); -> XREF: D01 T06 §2 (surface blur for skin smoothing); -> XREF: D01 T06 §3 (lens blur kernel depth blur drives); -> XREF: D01 T06 §4 (classical shake reduction offered beside AI deblur); -> XREF: D01 T06 §5 (classical denoise fallback); -> XREF: D01 T06 §8 (lighting effects for the normals-based relight preview); -> XREF: D01 T07 §4 (the mask component kinds §15 adds AI masks to); -> XREF: D03 T20 §1 (the Contextual Task Bar and Properties pages that read the AI quick-action registry); -> XREF: D03 T20 §8 (the Discover panel that lists AI quick actions beside the Ask panel).
- **Adjacency:** list=applicable @ D03 T19 §1 (the provenance panel filters by action, model, and date; the detections panel lists objects; the variations strip); document=not-applicable (AI results are ordinary layers that print through D03 T18 §6; this file adds no printed output); settings=applicable @ D01 T05 §2 (plus the `Gesso.AI.*` keys each section names); reporting=applicable @ D03 T19 §1 (usage, the per-document AI cost summary, the find-distractions review list); notifications=applicable @ D01 T05 §4 (progress, cancel, and failure through the shared panel and toast); permissions=applicable @ D03 T19 §1 (no key, offline, generative AI switched off, a declined preview, a model refusal, a reference image to a model without image input, another app not installed are refusals by name); audit=applicable @ D03 T19 §1 (each apply is one named history step, one provenance record, and one log line); exchange=applicable @ D03 T19 §13 (hand-off files with Albumen and Stilus, provenance XMP export, brand kit ASE through D01 T05 §5); reverse=applicable @ D03 T19 §1 (every apply undoes in one step and reverts from the provenance panel)

#### §1. AI in Gesso: the AI menu, settings, usage, and the provenance panel

- **Deliverable:** The Gesso AI menu and AI workspace entry, per-task model choice, usage and cost display, the send gate with the offline notice, the generative on or off switch, the Local or Detailed processing mode, the AI quick-action registry, and the Provenance panel that records, filters, re-runs, compares with before and after views, and reverts every AI action stored in the `.gesso` document.
- **Depends On:** D01 T05 §4, D03 T08 §1
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/ai-menu/ and docs/captures/gesso/provenance-panel/. Job: a user can reach every AI action from one place, choose models per task, see cost, and repeat, compare, or undo any AI result in the document. Treatment: a top-level AI menu listing each action with its owner section, a Provenance panel (thumbnail, action, prompt excerpt, model, seed and whether honored, cost, date) with Re-run, Re-run with New Seed, Compare (show original, preview toggle, split, mirror), Select Result Layers, Revert, and Delete Record, and the Gesso keys on the shared AI settings page. Cheaper substitute that fails: a history list without models or seeds, which cannot reproduce anything. Chrome: consume the shared `SendPreviewDialog`, `AiSettingsPage`, `AiProgressPanel`, and `AiUsageIndicator` from `D01 T05 §4`, the dock, and the suite history; do not build a Gesso key dialog or progress control.
- **Runs:** `Requires: display-session -- menu, panel, and compare captures need an interactive desktop`
- **Catalog:** IP-1990 to IP-1999 (10 features)
- **Hints:**
  - Register `services.AddIsotoneAi()` with app name `Gesso` in the composition root; add `src/Gesso/Isotone.Gesso.Desktop/AI/AiMenu.xaml` listing every AI action of §2 to §15, each wired or disabled with `Planned: D03 T19 §N` through `PlannedCommands`, plus an "AI" workspace preset (IP-1990, the Canva AI Studio mapping: featured AI tools, toggles, stacked AI filters) that `D03 T20 §1` shows as a studio.
  - Per-task models (IP-1991): `GessoAiTask` (Locate, Describe, Fill, Expand, Generate, Upscale, EditImage, Relight, Assistant) each resolving to a shared `D01 T05 §2` task with an optional override key `Gesso.AI.Model.<Task>`, pickers filtered by capability (image output, image input, structured output) from the catalog; Firefly, Gemini, FLUX, Premium, and Ultra tiers are simply OpenRouter models the user picks.
  - Model capabilities: `src/Gesso/Isotone.Gesso.Core/AI/ImageModelCaps.cs` built from the `D01 T05 §1` catalog plus a local override JSON (maximum edge, allowed aspect ratios, size multiple, accepts image input, accepts a mask, accepts multiple images, honors seed); every later section reads caps from here and never hard-codes a model.
  - Usage and cost (IP-1992): `AiUsageIndicator` in the status bar and a per-document cost summary (total, requests, models) above the Provenance panel list; credits and allowances are the user's own OpenRouter balance.
  - Gate and privacy (IP-1993, IP-1994, IP-1997): every call goes through `AiSendGate`; offline refuses before sending with the `D01 T05 §1` sentence; `ai.enabled` stays false until a key is set; `Gesso.AI.GenerativeEnabled` (default true once a key exists) hides every generative command when off while locate-only features keep working; the help page states that training policy depends on the chosen OpenRouter provider.
  - Provenance in the document: `src/Gesso/Isotone.Gesso.Core/AI/GessoProvenanceBinding.cs` writes the `D01 T05 §3` records into an `<gesso:provenance v="1">` block in `stack.xml` per the `D03 T08 §1` contract and tags result layers with `gesso:provenance-id`; a document with no records writes no block, so its save is byte-identical.
  - Provenance panel (IP-1995, IP-1996): `src/Gesso/Isotone.Gesso.Desktop/AI/ProvenancePanel.xaml` with filter by action, model, and date, prompt search, re-run through `ToRerun(sameSeed)` into a new result beside the old one with `ParentId`, Compare with show original, preview toggle, split, and mirror views over the result and its hidden original, and Revert as one `RevertAiResultCommand` removing the result layers and the record.
  - Quick actions (IP-1998): `src/Gesso/Isotone.Gesso.Core/AI/QuickActions/AiQuickActionRegistry.cs` (id, label, context predicate on selection and layer kind, command) with Remove Background, Blur Background, Select Subject, Generative Fill, and Enhance; the `D03 T11 §1` Properties panel shows them now, and the Contextual Task Bar (`D03 T20 §1`) and Discover panel (`D03 T20 §8`) read the same registry when they ship in Phase 27.
  - Processing mode (IP-1999): `Gesso.AI.Selection.ProcessingMode` (Local, Detailed; default Local) consumed by §6; on-device models are backlog B-046 and the settings page says so.
  - One Serilog Information line per AI apply `AI {Action} applied: record {RecordId}, {ModelId}, seed {Seed} (honored {SeedHonored}), {LayerCount} layers`; tests `GessoProvenanceBindingTests` (round trip, byte-identical save without records), `ProvenancePanelViewModelTests` (filter, re-run request equality, revert restores layers), `AiQuickActionRegistryTests`.
  - Commit: "gesso: the AI menu, AI settings, usage, quick actions, and the provenance panel"
- **Proof:** Format fidelity proof plus unit test: `tests/fixtures/gesso/ai/provenance-two-records.gesso` opens, saves, and reopens with both records and their layer links equal, the same file renamed `.ora` opens in `gimp-console` 3.2.6 with every layer, a record-free save hashes equal to the pre-change save, and `RevertAiResultCommandTests` restore the pre-generation layer stack tile by tile; the re-run request equals the recorded one over the `D01 T05 §1` recorded transport; cheaper substitute that fails: provenance kept only in the session, which the reopen test catches.

#### §2. The image-generation adapter

- **Deliverable:** `ImageGenerationAdapter` that turns a region, mask, and prompt into model requests (masked crop with context padding, size fitting, tiling with overlap), composites results through the mask with a feathered seam and a color match, records seed honesty, maps refusals, and lands results as a group with variations as hidden siblings in any of five output targets.
- **Depends On:** §1, D01 T05 §1
- **Phase:** 26
- **Surface:** UI (small). Fidelity: new build, no baseline; captured to docs/captures/gesso/ai-variations/. Job: every generative feature in Gesso gets the same honest, non-destructive result handling. Treatment: an output target choice (new layer, current layer as a new layer above, masked layer, smart filter, new document) and a variations strip in the Properties panel (thumbnails, Generate More, Use as Layer). Cheaper substitute that fails: pasting the model's image over the layer, which the outside-mask byte test catches. Chrome: consume the gate, `ImageModelCaps`, `D01 T03 §2` resampling, `D03 T09 §3` masks, and the `D03 T14 §1` live filter host.
- **Runs:** `Requires: display-session -- the variations strip capture needs an interactive desktop`
- **Catalog:** IP-2000 to IP-2002 (3 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Generation/GenerationRequestBuilder.cs`: crop the region's bounds plus context padding (`Gesso.AI.ContextPaddingPercent`, default 25 percent, at least 64 px), fit to the model's caps (aspect snapped to an allowed ratio, edge to the maximum, size multiple), downscale when larger and record the scale, and send the mask as a separate image only when the model accepts masks (otherwise as a transparent hole plus instruction).
  - Tiling (IP-2001): regions beyond the cap split into tiles with 128 px overlap, generated in raster order with already generated neighbors as context, blended across overlaps with linear ramps; "upscale to the selection" fits the result back with `D01 T03 §2` Lanczos and states the upscale factor in the Properties panel.
  - `GenerationCompositor.cs`: composite through the mask with a feathered seam (`Gesso.AI.SeamFeatherPx`, default 8) and a mean and standard-deviation color match in Lab over the seam ring (Reinhard et al. 2001); pixels outside the mask stay byte-identical by construction.
  - Output targets (IP-2000): new layer (default), current layer (becomes a new layer directly above, never an overwrite), masked layer, smart filter (an `<gesso:ai-filter v="1">` entry through `D03 T14 §1` holding the request and the cached result, re-run only by explicit action), and new document; each apply is one `AiGenerationCommand` named "<Action>: <prompt excerpt>".
  - Result structure: a group "Generative Fill: <prompt>" holding the chosen masked pixel layer and each variation as a hidden sibling (IP-2002); the strip switches the visible sibling (one undo step), Generate More appends with new seeds, Use as Layer copies one out of the group.
  - Seed honesty: the returned seed is compared with the requested one and with `ImageModelCaps.HonorsSeed`; the record stores `seedHonored`, and the UI says "This model does not honor seeds; a re-run may differ".
  - Refusals: a model that returns text instead of an image, an empty image, or a policy refusal maps to "The model declined this request: <reason>" with nothing applied; faces found by §6 inside the region add a send-preview caution.
  - Budget: request building and compositing for a 4096 by 4096 region under 400 ms excluding network; the apply log line is §1's.
  - Tests: `GenerationRequestBuilderTests` (padding, aspect snap, downscale factor, tile grid for three caps), `GenerationCompositorTests` (outside-mask bytes identical, seam delta under 2/255 on a flat field), `VariationGroupTests`, all over recorded image fixtures in `tests/fixtures/gesso/ai/`.
  - Commit: "gesso: the image-generation adapter with tiling, seams, variations, and seed honesty"
- **Proof:** Unit test: `GenerationCompositorTests.OutsideMask_ByteIdentical` hashes every tile outside the mask before and after composing a recorded model result, and `GenerationRequestBuilderTests` assert the exact crop, scale, and tile grid for three recorded caps; cheaper substitute that fails: pasting the returned image over the layer, which the hash comparison catches.

#### §3. Generative fill and generative remove

- **Deliverable:** Generative fill in a selection with an optional prompt producing a masked generative layer with stored prompt and variations, generative layer properties with generate similar, selection to generative editing, and the Remove tool's generative mode (auto, on, off, remove after each stroke, sample all layers).
- **Depends On:** §2, D03 T09 §3
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/generative-fill/ and docs/captures/gesso/remove-tool/. Job: a user can fill or remove content in a selection with a prompt and keep every variation editable. Treatment: `Edit, Generative Fill` (Ctrl+Shift+F) with a prompt bar (empty fills contextually), a generative layer whose Properties page shows prompt, variations, Generate, and Generate Similar; the Remove tool options bar gains Generative mode Auto, On, Off, Remove after each stroke, Sample all layers, and Size. Cheaper substitute that fails: a fill that merges into the source layer. Chrome: consume the §2 adapter, the `D03 T13 §2` classical Remove, the `D03 T09 §3` masks, and the Properties panel.
- **Runs:** `Requires: display-session -- fill and remove are driven runs on the canvas`
- **Catalog:** IP-2003 to IP-2009 (7 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Generative/GenerativeFillService.cs` (IP-2003, IP-2005): the selection becomes the §2 mask, an empty prompt sends a contextual-fill instruction, and the result is a generative layer with a layer mask equal to the selection.
  - Generative layer kind (IP-2006, IP-2009): `src/Gesso/Isotone.Gesso.Core/Layers/GenerativeLayer.cs` persisted as `<gesso:generative v="1" prompt-hash="..." provenance-id="..." variant="2">` with the rendered PNG fallback per `D03 T08 §1`; its Properties page edits the prompt and regenerates (one step), shows variations, and Generate Similar reuses the record with a new seed and `ParentId`.
  - Selection to generative editing (IP-2008): the selection quick action "Generative Fill" registered in §1's registry (and on the Contextual Task Bar when `D03 T20 §1` ships) opens the prompt bar with the selection as the mask.
  - Remove tool generative mode (IP-2004, IP-2007): the `D03 T13 §2` Remove tool gains `Gesso.Tools.Remove.GenerativeMode` (Auto, On, Off); Off uses the classical engine only; On sends the stroke's dilated mask through §2; Auto uses classical for strokes under `Gesso.AI.Remove.AutoThresholdPixels` (default 65,536 masked pixels) and generative above; remove after each stroke or on Apply; Sample all layers uses the visible composite as the source; results land on a new layer "Remove" above the target.
  - Size caps and tiling come from §2; the remove layer's mask is the dilated stroke, so nothing outside the stroke changes.
  - Apply log line via §1; tests `GenerativeFillServiceTests`, `GenerativeLayerSerializationTests`, `RemoveToolModeTests` (Auto picks classical below the threshold with zero gate calls).
  - Commit: "gesso: generative fill, generative layers, and the Remove tool's generative mode"
- **Proof:** Unit test plus format fidelity proof: `RemoveToolModeTests.Auto_SmallStroke_NoNetwork` asserts zero gate calls for a small stroke and one generative request for a large one; `GenerativeLayerSerializationTests` reopen `tests/fixtures/gesso/ai/generative-layer.gesso` with prompt hash, variants, and provenance link equal and the fallback PNG rendered by `gimp-console` 3.2.6; cheaper substitute that fails: generative results merged into the source layer, which the source-tile hash test catches.

#### §4. Generative expand

- **Deliverable:** Generative expand of the canvas with an optional prompt, the crop tool's fill choice (background, content-aware, generative expand) for expanded canvas, and generative expand from the develop crop, tiling expanded strips beyond the model's size.
- **Depends On:** §3, D03 T08 §9
- **Phase:** 26
- **Surface:** UI. Fidelity: extends the crop tool options bar -- docs/captures/gesso/crop/ (from `D03 T08 §9`); new captures to docs/captures/gesso/generative-expand/. Job: a user can widen a photo beyond its edges and fill the new area plausibly. Treatment: a Fill combo on the crop tool options bar (Background, Content-Aware, Generative Expand) with an optional prompt field, `Image, Generative Expand` with anchor and size, and an Expand option in the develop crop. Cheaper substitute that fails: stretching edge pixels into the new area. Chrome: consume the `D03 T08 §9` crop hook, the `D03 T13 §3` content-aware fill, §2's tiling, and the `D03 T15 §12` develop crop.
- **Runs:** `Requires: display-session -- a driven crop-expand run captures the result`
- **Catalog:** IP-2010 to IP-2013 (4 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Generative/GenerativeExpandService.cs` (IP-2010): the canvas grows through the `D03 T08 §7` canvas size command, then each new strip (top, right, bottom, left, corners) is a §2 region with the original border as context; results land in a group "Generative Expand: <prompt>" masked to the new area only.
  - Strips longer than the model's edge cap are tiled with overlap (§2) and generated from the original outward so each tile has real context (IP-2012).
  - Crop fill choice (IP-2011): `Gesso.Tools.Crop.ExpandFill` (Background, ContentAware, Generative) consumed by the `D03 T08 §9` crop hook; ContentAware runs `D03 T13 §3` locally with no network.
  - Develop crop (IP-2013): the `D03 T15 §12` crop gains an Expand option; the expansion is applied on commit as a generative group above the developed layer, never inside the RAW layer's settings.
  - The whole expand (canvas change plus fill) is one undoable command "Generative Expand"; the apply log line is §1's.
  - Tests: `GenerativeExpandServiceTests` (strip geometry for each anchor, tile counts beyond caps, original tiles unchanged).
  - Commit: "gesso: generative expand from the canvas, the crop tool, and the develop crop"
- **Proof:** Unit test: `GenerativeExpandServiceTests` expand a 1000 by 800 fixture to 1600 by 800 with a 1024 px cap and assert four tiles in outward order, original tiles hash-equal, and one undo step restoring the canvas size; cheaper substitute that fails: edge stretching, which the recorded-result comparison rejects.

#### §5. Generate image, background, and similar

- **Deliverable:** Generate image from a text prompt (content type, style presets, visual intensity, aspect ratio, count) with style, composition, and fill reference images, generate similar, and generate background behind a subject, all landing as new layers or documents.
- **Depends On:** §2
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/generate-image/. Job: a user can create a raster image or a background from a prompt and refine it by reference. Treatment: a Generate Image panel (prompt, content type Photo or Art, style preset strip, visual intensity, aspect ratio, count 1 to 4, reference slots Style with strength, Composition, and Fill, model) producing a variations group on a new layer or in a new document; Generate Background on a layer with transparency or a mask. Cheaper substitute that fails: a single image with no reference or variation handling. Chrome: consume the §2 adapter and variations, `ImageModelCaps`, the brand kit toggle, and the send gate.
- **Runs:** `Requires: display-session -- panel and result captures need an interactive desktop`
- **Catalog:** IP-2014 to IP-2016 (3 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/AI/GenerateImagePanel.xaml` with `GenerateImageViewModel` (IP-2014): content type and style presets from own JSON `Isotone.Gesso.Core/AI/Presets/styles.json` (authored for the suite, no vendor presets), visual intensity 1 to 10 mapped to prompt templates hashed into provenance, aspect ratios 1:1, 4:3, 3:2, 16:9, and 9:16 snapped to caps, count 1 to 4 as parallel requests with distinct recorded seeds; raster only, vector output handed to Stilus through §13, 3D output not offered.
  - Reference images (IP-2015): style reference with strength, composition reference, and fill reference, each sent as image input only to models whose caps accept images; otherwise the slot is disabled with "This model does not accept reference images".
  - Generate similar (IP-2016): reuses the record's prompt, references, and parameters with a new seed and `ParentId`; §2's seed-honesty note applies.
  - Generate background (IP-2017, IP-2018): the subject is the active layer's alpha or layer mask (a cut-out); the background is generated on a new layer directly below with the subject area masked out of the request; the one-click "Detect subject and generate background" quick action is registered by §6, which runs Select Subject and then calls this service.
  - Brand kit toggle injects the `D01 T05 §5` prompt fragment (palette names and roles).
  - Output: a new layer group in the current document, or a new document sized from the aspect ratio and the model's maximum edge; one undo step; the apply log line is §1's.
  - Tests: `GenerateImageViewModelTests` (count, distinct seeds, disabled reference slot), `GenerateBackgroundTests` (subject tiles unchanged, background layer directly below).
  - Commit: "gesso: generate image, reference images, generate similar, and generate background"
- **Proof:** Unit test: `GenerateBackgroundTests` apply a recorded background under a cut-out subject fixture and assert the subject layer's tiles are hash-equal and the new layer sits directly below it; `GenerateImageViewModelTests` assert four requests with four distinct recorded seeds; cheaper substitute that fails: flattening the background into the subject layer, which the hash test catches.

#### §6. AI selection: subject, sky, objects, and people

- **Deliverable:** Select Subject, Select Sky, the Object Selection tool (hover, rectangle, lasso, subtract, hard or soft edges, sample all layers), the object finder, multi-part objects, Select People with parts, hair refinement, and Select Sampled Depth, each built by a vision model locating (boxes, points, labels) and the local `D03 T10 §6` engine making the mask, with a Local mode that needs no network.
- **Depends On:** §1, D03 T10 §6
- **Phase:** 26
- **Surface:** UI. Fidelity: extends the selection tools -- docs/captures/gesso/selection-tools/ (from `D03 T10 §5`); new captures to docs/captures/gesso/object-selection/. Job: a user can select a subject, the sky, people and their parts, or any object with one click or a box, with pixel-accurate edges. Treatment: `Select, Subject`, `Select, Sky`, `Select, People` with part checkboxes, the Object Selection tool (W group) with Mode Rectangle or Lasso, Object Finder hover highlight with Refresh and Show All Objects, Sample All Layers, Hard Edge, a Select and Mask entry, a Local or Detailed processing combo, and the Select Sampled Depth tool. Cheaper substitute that fails: asking an image model to paint a mask, which misses edges and cannot run offline. Chrome: consume the gate, the `D03 T10 §6` engine, the `D03 T10 §1` selection model, and `D03 T10 §7` Select and Mask.
- **Runs:** `Requires: display-session -- the object finder hover and selection captures need an interactive desktop`
- **Catalog:** IP-2019 to IP-2020, IP-2022 to IP-2032 (13 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Vision/VisionLocator.cs`: sends a downscaled composite (long edge `Gesso.AI.Locate.MaxEdge`, default 1536) with a structured request against `Isotone.Gesso.Core/AI/Schemas/locate.v1.json` (`objects[]` of label, box in 0 to 1000 coordinates, positive and negative points, confidence, optional parts with their own boxes) and validates the reply; nothing else is asked of the model.
  - `LocateToMask.cs`: each located object seeds the `D03 T10 §6` engine at full resolution (box as the GrabCut rectangle, points as definite foreground and background), then guided-filter matting for soft edges (IP-2025 hard or soft edge; IP-2032 hair refinement where the model labels hair); the result is a `D03 T10 §1` selection or, from the Layers panel, a layer mask.
  - Processing mode (IP-2019, IP-2029): Local runs the engine alone (spectral residual saliency after Hou and Zhang 2007 plus a center prior as the subject seed, a bright upper-region color model for sky) with no network; Detailed adds the vision locate first; the options bar shows which ran.
  - Object Selection tool (IP-2020, IP-2022 to IP-2024, IP-2026): Rectangle and Lasso modes (the drawn region is the seed; a local GrabCut runs first and the vision model only in Detailed mode to split the region into objects), Add, Subtract (IP-2024), Intersect, Sample All Layers, and multi-part objects kept as separate components the user can pick.
  - Object finder (IP-2027): detections cached per document keyed by the composite's hash; hover highlights a detection's outline, click selects, Shift adds, Refresh re-locates by explicit action, Show All Objects overlays every detection; overlay color and opacity in `Gesso.AI.ObjectFinder.*`.
  - Menu commands (IP-2028, IP-2030, IP-2031): Select Subject from the menu, options bar, and Select and Mask; Select Sky; Select People with parts (face, skin, hair, eyes, teeth, lips, clothing) located as part boxes and segmented locally, the help stating that part accuracy is model-limited.
  - Sampled depth (IP-2021, IP-2033): `src/Gesso/Isotone.Gesso.Core/AI/Depth/DepthEstimator.cs` builds an estimated depth map from a vision model's layered description (`depth-layers.v1.json`: ordered regions with labels, boxes, near-to-far rank, and ground-plane hints) plus the engine's segments, ground planes as vertical gradients, smoothed by a guided filter; the Select Sampled Depth tool selects pixels within a depth tolerance of the clicked point; the map is cached per document and labeled "estimated, not measured"; §14 reuses this estimator.
  - Registers the "Detect subject and generate background" quick action that runs Select Subject and calls §5's service.
  - Budget: Local Select Subject on a 24-megapixel image under 2 s; mask building after a locate reply under 1.5 s; one Serilog Information line `AI selection {Kind}: {ObjectCount} objects, {Mode}`.
  - Tests: `VisionLocatorTests` (schema rejects, coordinate mapping), `LocateToMaskTests` over recorded locate replies with ground-truth masks, `LocalModeTests` (zero gate calls), `DepthEstimatorTests`.
  - Commit: "gesso: AI selection by locating objects and segmenting locally"
- **Proof:** Unit test plus golden proof: `LocateToMaskTests` turn recorded locate replies for `tests/fixtures/gesso/ai/select/*.png` (suite-authored photos with hand-made ground-truth masks) into masks with IoU of at least 0.92 and boundary F-score of at least 0.85; `LocalModeTests` prove zero gate calls; cheaper substitute that fails: an image-model-painted mask, whose IoU on the committed fixtures falls below the bar and which cannot run offline.

#### §15. AI masks everywhere: detections, mask all objects, and develop masks

- **Deliverable:** A Detections panel listing detected objects and regions to select or mask, Mask All Objects into masked groups, Decompose Layer into subject, background, and foreground layers with occluded parts filled, and AI subject, sky, background, object, people-part, and landscape masks in the develop surfaces with Update AI Masks.
- **Depends On:** §6, D03 T15 §2
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/detections-panel/; extends the develop Masks panel -- docs/captures/gesso/develop-masks/ (from `D03 T15 §2`). Job: a user can turn every detected object into a mask or layer in one step, and use AI masks for local develop adjustments. Treatment: a Detections panel (thumbnail, label, confidence, Select, Mask, Mask All into groups), `Layer, Decompose Layer`, and Add AI mask entries in the develop Masks panel (Subject, Sky, Background, Object by brush or rectangle, People parts, Landscape regions) with an Update button when stale. Cheaper substitute that fails: one merged mask for all objects. Chrome: consume §6's locator and mask builder, §3's fill, the `D01 T07 §4` mask model, and the dock.
- **Runs:** `Requires: display-session -- panel, decompose, and develop mask captures need an interactive desktop`
- **Catalog:** IP-2034 to IP-2043 (10 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/AI/DetectionsPanel.xaml` (IP-2034, IP-2042): lists §6's cached detections with thumbnail, label, and confidence; Select sets the selection and Mask adds a layer mask on the active layer, each one undo step.
  - Mask All Objects (IP-2037, IP-2043): one masked group per detection (a copy of the layer, or an empty group carrying the mask for adjustment use), named by label, in one `MaskAllObjectsCommand`.
  - Mask tool seeding (IP-2036): sky and person detections seed the mask brush's auto-mask so a stroke snaps to the detected region.
  - Decompose Layer (IP-2035): segments subject, background, and foreground through §6 and the `D03 T10 §6` engine into separate layers, fills each layer's occluded area through §3 with the fill marked "(filled, generated)" in the layer name and in provenance, and hides the original.
  - Develop AI masks (IP-2038 to IP-2040): a new `D01 T07 §4` component kind `AiMaskComponent` (Subject, Sky, Background, Object, PeoplePart, LandscapeRegion; a stored raster mask at develop resolution; the locate record id) added from the `D03 T15 §2` panel, located on the develop-rendered image and segmented locally; landscape regions (sky, water, vegetation, mountains, architecture, ground) come from the locate labels.
  - Update AI masks (IP-2041): a mask whose source image hash changed (geometry, crop, or a large exposure change) shows Stale with an Update button; updating is an explicit gated action that re-locates and rebuilds only the stale masks.
  - One Serilog Information line per mask-all, decompose, and update; tests `MaskAllObjectsCommandTests`, `DecomposeLayerTests` (original hidden, filled parts named), `AiMaskComponentTests` (persistence inside develop settings, stale detection).
  - Commit: "gesso: detections, Mask All Objects, Decompose Layer, and AI develop masks"
- **Proof:** Unit test: `MaskAllObjectsCommandTests` create one masked group per recorded detection with masks equal to `LocateToMask` output and undo in one step; `AiMaskComponentTests` reopen a smart filter holding an AI mask and flag it stale after a crop change; cheaper substitute that fails: one merged mask, which the per-group count assertion rejects.

#### §7. Neural-filter equivalents

- **Deliverable:** A Neural Filters workspace with skin smoothing, smart portrait, makeup transfer, colorize, style transfer, photo restoration, harmonization, harmonize with generated relight and shadows, landscape mixer, and rotate object, each producing new layers with provenance and stated limits.
- **Depends On:** §2, §6
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/neural-filters/. Job: a user can apply portrait, restoration, color, and scene transformations and keep the original untouched. Treatment: a Neural Filters workspace (filter list with on toggles, per-filter sliders, before and after preview, output New Layer, Masked Layer, Smart Filter, or New Document) and on-canvas yaw and pitch handles for Rotate Object. Cheaper substitute that fails: applying the model output over the layer. Chrome: consume the §2 adapter, §6 masks, the `D01 T03` and `D01 T06` classical effects, and the gate with its caution text.
- **Runs:** `Requires: display-session -- workspace and before and after captures need an interactive desktop`
- **Catalog:** IP-2044 to IP-2057 (14 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/AI/NeuralFiltersView.xaml` (IP-2054) over a registry `Isotone.Gesso.Core/AI/Neural/INeuralFilter.cs` (id, parameter schema, model or classical, output kind); several enabled filters run in order into one result group.
  - Skin smoothing (IP-2044): classical, no model: face and skin masks from §6's people parts (Local mode works), `D01 T06 §2` surface blur with blur and smoothness on a masked new layer; nothing leaves the machine unless Detailed mode locates the face.
  - Smart portrait and makeup (IP-2045, IP-2046): the image-edit model with sliders (expression, age, hair thickness, gaze, head direction, light direction, detail retention) turned into graded prompt templates hashed in provenance; makeup transfer only on models whose caps accept multiple images; the send preview carries the caution "This sends a face to <model>; identity may drift".
  - Colorize (IP-2047, IP-2055): the model result supplies chroma only, as a Color blend-mode layer over the original so luminance is untouched; focal-point hints become prompt text; the help says colors are guesses.
  - Style transfer (IP-2048): presets from own JSON or a custom style image (models with image input only), strength by opacity, preserve color by Luminosity blend, focus subject by §6's subject mask.
  - Photo restoration (IP-2049): classical passes first (`D01 T03 §6` dust and scratch and JPEG artifact removal, `D01 T06 §5` denoise, halftone removal by an FFT notch), then an optional model enhance and face pass, each its own layer.
  - Harmonization (IP-2050, IP-2051, IP-2056): a statistical Lab color transfer from a reference layer (Reinhard et al. 2001) as clipped Curves and Color Balance adjustment layers with no model; generated shadow (Multiply) and relight layers from the image-edit model with variations are an option, with the help stating that lighting match is approximate.
  - Landscape mixer (IP-2052): time of day, season, and strength as prompt templates; preserve subject by masking §6's subject out of the edit; harmonize subject by the statistical pass.
  - Rotate object (IP-2053, IP-2057): yaw and pitch handles on the selected object become an instruction to the image-edit model; the result is a new layer labeled "generated view, not 3D".
  - Apply log line via §1; tests `NeuralFilterRegistryTests`, `SkinSmoothingTests` (no gate call in Local mode), `ColorizeCompositeTests` (the composite's luminance equals the original within 1/255).
  - Commit: "gesso: neural-filter equivalents as layered, provenance-recorded results"
- **Proof:** Unit test: `ColorizeCompositeTests` prove the composite's L channel equals the original's within 1/255 after applying a recorded colorize reply, and `SkinSmoothingTests` prove zero gate calls in Local mode; cheaper substitute that fails: using the model's image directly, whose luminance drift the L-channel test catches.

#### §14. Depth, portrait blur, and relighting

- **Deliverable:** Detect Depth into a depth map layer, depth and normals maps, depth blur and portrait blur by estimated depth through the `D01 T06 §3` lens blur kernel with bokeh shapes, focal range, haze, and grain, portrait lighting with point or spot lights, and mixed light correction, each stating that depth is estimated, not measured.
- **Depends On:** §6, D01 T06 §3
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/depth-blur/ and docs/captures/gesso/portrait-lighting/. Job: a user can blur a background by distance and relight a portrait while seeing that the depth is an estimate. Treatment: a Depth Blur dialog (focal point pick, focal distance, focal range, blur strength, iris shape, haze, grain, output depth map, output New Layer or Smart Filter), `Filter, Render, Detect Depth`, and a Portrait Lighting dialog with draggable point and spot lights on the canvas. Cheaper substitute that fails: a radial gradient blur centered on the subject. Chrome: consume §6's `DepthEstimator` and masks, the `D01 T06 §3` kernel, `D01 T06 §8` lighting, and the §2 adapter.
- **Runs:** `Requires: display-session -- blur and lighting dialogs are driven runs`
- **Catalog:** IP-2021, IP-2033, IP-2058 to IP-2065 (10 features)
- **Hints:**
  - Detect Depth (IP-2060, IP-2062): §6's `DepthEstimator` writes a 16-bit grayscale layer named "Depth (estimated)"; normals are derived locally from its Sobel gradients into an RGB layer "Normals (estimated)"; both new layers carry provenance.
  - Depth blur and portrait blur (IP-2059, IP-2061, IP-2065): the `D01 T06 §3` lens blur kernel driven by the estimated depth with focal point, distance, range, blur, iris shapes (triangle to octagon, blade curvature, rotation), haze, and grain; subject edges come from §6's matte so hair keeps its edge; output as a new layer or a `D03 T14 §1` smart filter storing the depth map.
  - Portrait lighting (IP-2058, IP-2064): two paths, both new layers: a local preview relight from the normals layer through `D01 T06 §8` (point and spot lights, color, intensity) and an optional generative relight through the image-edit model with the lights described in the prompt; both labeled "not physically based".
  - Mixed light correction (IP-2063): an image-edit model result on a new layer, masked to §6's subject when chosen, quality stated as model-dependent.
  - Every dialog's help text and the depth layer's name say "estimated, not measured".
  - Apply log line via §1; tests `DepthBlurTests` (focal-plane pixels unchanged within 1/255, blur grows with depth distance), `NormalsFromDepthTests`.
  - Select sampled depth (IP-2021, IP-2033): click a point and select the areas at its estimated depth, from the same depth map, output through the D03 T10 §6 engine; the send preview says the depth is estimated.
  - Commit: "gesso: estimated depth, depth and portrait blur, and relighting"
- **Proof:** Unit test: `DepthBlurTests` apply the kernel with a recorded depth description to `tests/fixtures/gesso/ai/depth-scene.png` (suite-authored) and assert focal-plane pixels unchanged within 1/255 while background local variance drops by at least half; cheaper substitute that fails: a radial gradient blur, which blurs an off-center in-focus object the fixture places on the focal plane.

#### §8. Upscale and enhance

- **Deliverable:** Generative upscale 2x and 4x (faithful or creative), super zoom, super resolve for layers and documents, AI noise reduction as a filter and a brush, motion blur reduction, SDR to HDR expansion into a 32-bit layer, and AI denoise, detail, super resolution, mixed light, and deblur in the develop surfaces, all tiled for large output with classical fallbacks offered by name.
- **Depends On:** §2, D01 T03 §2
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/upscale/ and docs/captures/gesso/ai-denoise/. Job: a user can enlarge or clean an image with AI and keep the original. Treatment: an Upscale dialog (2x or 4x, Faithful or Creative, model, scale document to fit), Super Zoom (crop then enlarge with detail, artifact, noise, sharpen, and face options), `Image, Super Resolve Document` (percentage), AI Denoise (luma and chroma strength, as a live filter or a brush), Reduce Motion Blur, SDR to HDR, and an Enhance section in the develop surfaces. Cheaper substitute that fails: Lanczos labeled AI. Chrome: consume §2's tiling, `D01 T03 §2`, the `D01 T06 §4` and `D01 T06 §5` classical fallbacks, the `D03 T15 §1` and `D03 T15 §12` surfaces, and `D03 T15 §4` float documents.
- **Runs:** `Requires: display-session -- dialogs and before and after captures need an interactive desktop`
- **Catalog:** IP-2066 to IP-2079 (14 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Enhance/UpscaleService.cs` (IP-2066, IP-2068, IP-2072): tiles at the model's edge cap with 64 px overlap, each upscaled by the model and blended by linear ramps; Faithful and Creative map to prompt templates and a model choice (Topaz and Firefly class tools map to OpenRouter models); scale document to fit resizes the canvas and non-pixel layers natively.
  - Super Zoom (IP-2067, IP-2073): crop to the view or selection, then upscale with detail enhance, JPEG artifact removal (classical `D01 T03 §6` pre-pass), noise, sharpen, and face options as prompt parameters, into a new document.
  - Super resolve document (IP-2069): text, shape, and vector layers resized natively through `D03 T08 §7`, pixel layers upscaled, smart objects re-rendered from their source.
  - AI noise reduction (IP-2070): luma and chroma strength; as a `gesso:ai-filter` smart filter (cached result, re-run on demand) and as a brush painting a mask onto a denoised result layer; the classical `D01 T06 §5` denoise is offered beside it and runs when AI is off; on-device models are B-046.
  - Motion blur reduction (IP-2074): an image-edit model result on a new layer, with the classical `D01 T06 §4` shake reduction offered beside it.
  - SDR to HDR (IP-2075): a local inverse tone map (Banterle et al. 2006 expand map) into a new 32-bit layer, with light sources and sky located by §6's vision model given extra expansion; labeled "estimated, not recovered"; requires a 32-bit document and offers the `D03 T15 §4` conversion.
  - Develop enhance (IP-2076 to IP-2079): AI denoise, raw detail enhance (classical demosaic stays with `D03 T07 §11`), super resolution 2x, mixed light correction, and motion blur reduction run on the develop output at commit and land as a new layer above the developed layer or RAW layer, never inside the develop settings.
  - GIMP plug-in equivalents (IP-2071): `docs/user/gesso/ai.md` gains a table mapping the jobs of GIMP's third-party AI plug-ins (generation, inpainting, super resolution, segmentation, denoise, colorize, background removal) to §3, §5, §6, §7, §8, and §9.
  - Budget: request planning and seam blending for an 8K output under 2 s excluding network; progress per tile, and a cancel keeps finished tiles out of the document.
  - Tests: `UpscaleServiceTests` (tile grid, seam delta under 2/255 on recorded tiles, cancel leaves the document unchanged), `SdrToHdrTests` (values above 1.0 only inside expanded regions).
  - Commit: "gesso: generative upscale, super resolve, AI denoise and deblur, and SDR to HDR"
- **Proof:** Unit test: `UpscaleServiceTests` assemble recorded 2x tiles of `tests/fixtures/gesso/ai/upscale-src.png` and assert seam delta under 2/255 across every overlap, exact 2x dimensions, and that a mid-way cancel leaves the document hash unchanged; cheaper substitute that fails: Lanczos presented as AI, which the provenance and gate-call assertions reject.

#### §9. Distraction and object removal

- **Deliverable:** Find Distractions (people, wires and cables, dust, general) with a review list, detect objects for removal, remove background to a layer mask, reflection removal returning the reflection as its own layer, blemish removal by type and prominence, and generative remove in develop with variations.
- **Depends On:** §6, §3, D03 T13 §3
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/find-distractions/ and docs/captures/gesso/remove-background/. Job: a user can find and remove distractions or the background in one pass and review each change. Treatment: a Find Distractions panel (categories People, Wires and Cables, Dust, General; a review list with thumbnails and checkboxes; Classical or Generative fill per item; Remove Selected), a Remove Background quick action producing a layer mask, Reflection Removal, and Blemish Removal with type and prominence. Cheaper substitute that fails: deleting background pixels. Chrome: consume §6's locator and masks, §3's generative fill, the `D03 T13 §2` and `D03 T13 §3` classical engines, and §1's quick-action registry.
- **Runs:** `Requires: display-session -- review and removal are driven runs`
- **Catalog:** IP-2017 to IP-2018, IP-2080 to IP-2089 (12 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Removal/DistractionFinder.cs` (IP-2080, IP-2084, IP-2085, IP-2088): the vision model locates candidates per category (`distractions.v1.json`: label, category, box, and a polyline for wires); masks come from `D03 T10 §6`, wires from a ridge-following thin mask along the polyline dilated to the measured width, dust from local difference-of-Gaussian spots; the review list lets the user uncheck items before anything is filled.
  - Fill per item: Classical (`D03 T13 §3` PatchMatch, no network) or Generative (§3); accepted items land on one new layer "Distractions removed" masked to their union, one undo step.
  - Remove background (IP-2081, IP-2089): §6 Select Subject, then a layer mask on the layer (never deleted pixels; Affinity's in-place rasterizing is not copied); quick action registered with §1.
  - Reflection removal (IP-2082, IP-2086): the image-edit model returns the transmission image; the result is two new layers, "Without reflection" and "Reflection" (original minus result in linear light, blended Linear Dodge (Add) so the pair recomposes the original).
  - Blemish removal by type and prominence (IP-2087): local detection (skin mask from §6's people parts, difference-of-Gaussian spots classed small, medium, and large, prominence by contrast), healed through `D03 T13 §2` onto a new layer; no model needed in Local mode.
  - Generative remove in develop (IP-2083): a brush in the `D03 T15 §12` studio collects strokes; on commit the generative removal with variations lands as a group above the developed layer; seed honesty per §2.
  - Apply log line via §1; tests `DistractionFinderTests` (recorded locate, unchecked items untouched), `ReflectionLayersTests` (the pair recomposes the original within 1/255), `RemoveBackgroundTests` (mask only, pixels unchanged).
  - Generate background (IP-2017, IP-2018): mask the subject with D03 T19 §6, generate a new background through the §2 adapter on a new layer beneath it, with variations.
  - Commit: "gesso: find distractions, remove background to a mask, and reflection and blemish removal"
- **Proof:** Unit test: `ReflectionLayersTests` recompose the original within 1/255 from the two layers built from a recorded reply, and `RemoveBackgroundTests` hash the source tiles before and after; cheaper substitute that fails: deleting background pixels, which the hash test catches.

#### §10. The Gesso assistant: prompt to edit

- **Deliverable:** Prompt to edit that respects the selection (structured undoable commands first, an image-edit layer otherwise), markup guidance, a conversational assistant for multi-step edits, AI adjustment presets and auto adjust as adjustment layers, adaptive profiles and recommended presets as develop parameters, and an Ask panel answering feature questions from bundled help.
- **Depends On:** §1, D03 T11 §1
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/assistant/. Job: a user can describe an edit in words, review the plan, and get layered, undoable results, or ask how a feature works. Treatment: a dockable Assistant panel (chat, a plan checklist of commands with targets and parameters, Apply All, Step, Discard, markup pen), a Prompt to Edit bar, AI Adjust presets in the Adjustments panel, Adaptive Profile and Recommended Presets in the develop Presets panel, and an Ask tab. Cheaper substitute that fails: sending every request to an image model that repaints the photo. Chrome: consume the command registry, `D03 T11 §1` adjustment layers, the `D01 T07` parameter schemas, the gate, and provenance; do not add a scripting engine (that is B-041).
- **Runs:** `Requires: display-session -- assistant plan captures need an interactive desktop`
- **Catalog:** IP-2090 to IP-2097 (8 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Assistant/GessoEditPlan.cs` and `Schemas/gesso-edit-plan.v1.json` (IP-2090, IP-2095): a whitelist of structured steps (add an adjustment layer of a kind with parameters, add a mask from the selection or from a §6 locate, add a live filter with parameters, select subject or sky, set blend mode and opacity, crop and straighten); validated, then applied as one `CompositeCommand` "Assistant: <request>" scoped to the selection when one exists.
  - Fallback: when the reply sets `needsPixels: true` (the request cannot be expressed as steps), the user confirms and §2's image-edit path produces a new masked layer.
  - Markup (IP-2091): a non-printing markup overlay (arrows, circles, colors, doodles) drawn with a markup pen, sent as an annotated copy only to vision-capable models and listed in the send preview.
  - Conversation (IP-2092): chats per document stored in `<gesso:assistant v="1">` (opt-out `Gesso.AI.Assistant.SaveChats`), follow-up questions, and step mode applying one plan step per history entry, each with provenance.
  - AI adjust (IP-2093): the vision model proposes adjustment-layer parameters as JSON for Auto Adjust and for adaptive presets (portrait, landscape, product, night), applied as adjustment layers; classical Auto Tone and Auto Color from `D03 T11 §2` stay one click away.
  - Adaptive profile and recommended presets (IP-2096, IP-2097): the vision model suggests `D01 T07` develop parameters, recorded in the develop settings with provenance, and ranks the user's presets by fit.
  - Ask panel (IP-2094): a local BM25 index over the shipped `docs/user/gesso/` pages picks the top passages; the question plus those passages go to the text model; offline, the local search hits are shown alone.
  - One Serilog Information line per applied plan; tests `GessoEditPlanValidatorTests` (unknown step refused), `GessoEditPlanApplierTests` (one undo step, selection-scoped masks), `AskIndexTests`.
  - Commit: "gesso: the assistant with structured edit plans, markup, adaptive presets, and Ask"
- **Proof:** Unit test: `GessoEditPlanApplierTests` apply a recorded plan for "warm the sky and darken the foreground" to a fixture and assert two masked adjustment layers, untouched pixel tiles, and one undo step; `GessoEditPlanValidatorTests` refuse a non-whitelisted step; cheaper substitute that fails: an image model repainting the photo, which the untouched-tiles assertion rejects.

#### §11. AI type and faces

- **Deliverable:** Match Font that recognizes a font in an image region and ranks installed fonts, and face landmarks that feed face-aware liquify, both on the vision model with local refinement.
- **Depends On:** §1, D03 T16 §2, D03 T13 §9
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/match-font/; extends Liquify -- docs/captures/gesso/liquify/ (from `D03 T13 §9`). Job: a user can identify an installed font that matches text in a photo, and use face-aware sliders in Liquify. Treatment: `Type, Match Font` with a crop box and a ranked list of installed fonts with sample renders and Apply to the active text layer; Liquify's face-aware panel receives landmarks with draggable manual correction. Cheaper substitute that fails: sending the installed font list to the model. Chrome: consume the moved `FontMatcher`, the `D03 T16 §2` font list, the `D03 T13 §9` face-aware hook, and the gate.
- **Runs:** `Requires: display-session -- Match Font and face-aware liquify are driven runs`
- **Catalog:** IP-2098 (1 features)
- **Hints:**
  - Move `FontMatcher` from `src/Stilus/Isotone.Stilus.Core/AI/` (`D02 T15 §7`) into `src/Isotone.Core/Text/FontMatching/` as its second consumer, Stilus consuming it unchanged and its tests moving to `tests/Isotone.Core.Tests/Text/`; nothing is copied.
  - Match Font (IP-2098): the cropped region goes to the vision model asking for glyph features (serif, weight, width, x-height ratio, contrast) and the recognized text; installed fonts are ranked locally by rendering the recognized text in each candidate and comparing perceptual hashes; no font list leaves the machine, and there is no Adobe Fonts sync.
  - Face landmarks: `src/Gesso/Isotone.Gesso.Core/AI/Faces/FaceLandmarkLocator.cs` asks for per-face boxes and approximate landmarks (eyes, brows, nose, mouth corners, jaw points) as JSON, refines them locally (eye centers by dark-blob fit, mouth corners by edge search), and hands them to the `D03 T13 §9` face-aware liquify hook; offline, the user places the same points by hand.
  - One Serilog Information line per match and per landmark locate; tests `FontMatcherTests` (moved; a committed sample rendered in a known font ranks it first), `FaceLandmarkRefinerTests`.
  - Commit: "gesso: Match Font on the shared font matcher and face landmarks for Liquify"
- **Proof:** Unit test: `FontMatcherTests` rank Segoe UI first for the committed sample rendered in it, `grep -rn "class FontMatcher" src` prints one path under `src/Isotone.Core/`, and `FaceLandmarkRefinerTests` move recorded approximate eye points to within 2 px of hand-marked centers on `tests/fixtures/gesso/ai/face.png` (suite-authored); cheaper substitute that fails: a Gesso copy of the matcher, which the single-class grep rejects.

#### §12. Sky replacement

- **Deliverable:** Sky Replacement with user-supplied skies, brightness, temperature, scale, flip, edge shift and fade, foreground and edge lighting, color adjustment, output to new layers or a duplicate layer, and the Sky Brush and Sky Move tools.
- **Depends On:** §6
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/sky-replacement/. Job: a user can swap the sky of a photo and keep the result layered and adjustable. Treatment: an `Edit, Sky Replacement` dialog (sky picker over the user's skies folder with Import, Shift Edge, Fade Edge, Brightness, Temperature, Scale, Flip, Lighting Mode Multiply or Screen, Lighting Adjustment, Edge Lighting, Color Adjustment, Output New Layers or Duplicate Layer) with Sky Move and Sky Brush tools inside it. Cheaper substitute that fails: pasting a sky through a hard mask. Chrome: consume §6's Select Sky (Local or Detailed), `D03 T10 §7` edge refinement, adjustment layers, and masks.
- **Runs:** `Requires: display-session -- the dialog and result captures need an interactive desktop`
- **Catalog:** IP-2099 to IP-2102 (4 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/AI/Sky/SkyReplacer.cs` (IP-2099, IP-2102): the sky mask comes from §6 Select Sky (Local mode works offline); skies are images the user imports into `%LOCALAPPDATA%\Rizonesoft\Gesso\skies\` (no Adobe preset skies are shipped); brightness, temperature, scale, and flip transform the sky layer.
  - Edge and lighting (IP-2100): shift edge and fade edge refine the mask; foreground lighting puts the sky's average color on a clipped layer in Multiply or Screen with a lighting adjustment; edge lighting adds a soft glow along the horizon; color adjustment harmonizes the foreground with §7's statistical transfer.
  - Tools (IP-2101): Sky Move drags the sky inside the dialog; Sky Brush grows or shrinks the sky mask with the engine's edge awareness.
  - Output: a group "Sky Replacement" with the masked sky layer, a foreground lighting layer, and a color adjustment layer clipped to the foreground, or a duplicate merged layer; one undo step; one Serilog Information line `Sky replaced with {Sky} ({Output})`.
  - Tests: `SkyReplacerTests` (layer structure, mask from a recorded locate, zero gate calls in Local mode).
  - Commit: "gesso: sky replacement with user skies and layered output"
- **Proof:** Unit test: `SkyReplacerTests` build the output group from a fixture and a committed suite-authored sky image and assert the group's layers and blend modes and that the source layer's tiles are hash-equal; cheaper substitute that fails: a flattened sky paste, which the layer-structure assertion rejects.

#### §13. The suite pipeline and the brand kit in Gesso

- **Deliverable:** A Brand Kits panel (colors, fonts, logos) over the shared kits, brand-constrained prompts, hand-offs received from Albumen and Stilus and sent to Stilus for tracing with provenance carried in sidecars, and optional provenance export as XMP.
- **Depends On:** §1, D02 T15 §11, D01 T05 §5
- **Phase:** 26
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/brand-kits/ and docs/captures/gesso/suite-handoff/. Job: a user can apply brand colors, fonts, and logos, and move images between Albumen, Gesso, and Stilus without file juggling. Treatment: a Brand Kits panel (active kit, palettes as swatches, type styles applied to text layers, logos placed as smart objects), `File, Send to Stilus` shown only when Stilus is installed, a Hand-off panel listing arriving files with source app and provenance, and an Include AI provenance checkbox in export. Cheaper substitute that fails: a Gesso-only palette file or a project reference to Stilus. Chrome: consume the `D01 T05 §5` library, `SuiteAppLocator` and the hand-off folder from `D02 T15 §11`, `D03 T11 §10` swatches, `D03 T16 §1` text layers, `D03 T09 §9` smart objects, and `D03 T17 §10` XMP.
- **Runs:** `Requires: display-session -- the hand-off round trip with the stub editor is a driven run`
- **Catalog:** IP-2103 (1 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Desktop/AI/BrandKitsPanel.xaml` (IP-2103): the active kit from `brand.activeKitId`, palettes shown as swatch groups (added to the `D03 T11 §10` document swatches on request), type styles applied to the selected text layer, logos placed as embedded smart objects, refreshed on `KitsChanged`; no Canva sync.
  - Brand-constrained prompts: the §3, §5, and §7 panels show a Use brand kit toggle that injects `BrandKitConstraint`'s prompt fragment.
  - Receive: a second launch with a path (Albumen's Edit in Gesso, `D04 T02 §7`) opens it through single-instance forwarding; files in `%LOCALAPPDATA%\Rizonesoft\Isotone\handoff\inbox\gesso\` with a `.provenance.json` sidecar appear in a Hand-off panel; on save the sidecar records are appended to the document with `ParentId` links and the file is written back for the sender to relink.
  - Send to Stilus: writes the flattened PNG and sidecar to `handoff\inbox\stilus\` and launches Stilus through `SuiteAppLocator`; an absent Stilus hides the command and a forced invocation refuses by name.
  - Provenance XMP export: `Gesso.Export.IncludeAiProvenance` (default off, offered in the export dialog) writes the records as XMP through `D03 T17 §10`; signed Content Credentials are B-047.
  - `ProjectReferenceGuardTests` assert no Gesso project references Stilus or Albumen.
  - One Serilog Information line per hand-off sent, received, and relinked; tests `GessoHandoffTests` (a three-record sidecar lineage), `BrandKitsPanelViewModelTests`.
  - Commit: "gesso: the Brand Kits panel, suite hand-offs, and provenance XMP export"
- **Proof:** Driven run plus unit test: a driven hand-off from the `tests/Isotone.HandoffStub/` editor (from `D02 T15 §11`) registered under App Paths into Gesso and back produces the three log lines (quoted) and a three-record lineage in the saved `.gesso`; with the App Paths entry removed, Send to Stilus refuses by name; `ProjectReferenceGuardTests` pass; cheaper substitute that fails: a project reference to Stilus, which the guard test fails.

#### Sizing concerns

- §6 (15 features) carries the locator, the Local-mode seeds, the Object Selection tool, the object finder, people parts, and the depth estimator; if authoring exceeds 30 items, move the depth estimator and Select Sampled Depth (IP-2021, IP-2033) to §14, which already owns depth and runs after §6.
- §7 and §8 (14 features each) span many small filters and fit only because each is one registry entry over the §2 adapter; keep them as registry items, not separate dialogs.

### todo/03-gesso/TODO-20-gesso-parity-workspace.md -- `gesso-parity-workspace`

- **Title:** "TODO-20 -- Gesso Parity: Workspace, Customization, Preferences, and Help"
- **Phase(s):** 27
- **Goal:** Gesso reaches Photoshop 27.10, Affinity Photo 3.3, and GIMP 3.2.6 parity for the workspace a professional customizes and lives in: workspaces and studios as presets (Essentials, Photography, Painting, Graphic and Web, Compositing, Color Grading, Typography, Develop, and the AI workspace), docking, tabs, single and multi-window modes, GIMP dockable dialogs, the Properties panel pages and the Contextual Task Bar, numeric field behaviors, a customizable toolbar and options bar, menus, shortcut sets, and command search, complete Preferences (general, tools, cursors, units, guides, type, interface, language, accessibility display, files, performance, GPU, scratch, input devices), the presets manager and resource folders, and help, learning, and local diagnostics. The workspace, toolbar, menu, and shortcut-set frames of `D02 T16 §1` to `§3` move to `src/Isotone.UI/Workspace/` on this second use (each move the first item of its section, Stilus consuming the moved type unchanged), and the other Stilus pieces Gesso needs again (`PreferenceKeyRegistry`, `WarningRegistry`, `PressureCurve`, the Surface Dial menu, `SystemInfoReport`, `GpuDiagnostics`, and the welcome frame) move the same way; nothing is copied. It extends `D03 T07 §17` (workspaces and the Preferences dialog) and feeds `D03 T07 §16` (the accessibility and localization audit that runs last), sends nothing anywhere by default, and every document edit stays one undo step.
- **Current-state facts to verify (with claim candidates):**
  - The Window menu toggles five fixed panels and offers only Reset Workspace; nothing saves a named arrangement. `<!-- claim: count "IsChecked=\"\{Binding Show[A-Za-z]*Panel\}\"" src/Gesso/src/Gesso.UI/Views/MainWindow.xaml = 5 -->` `<!-- claim: count "ResetWorkspaceCommand" src/Gesso/src/Gesso.UI/Views/MainWindow.xaml = 1 -->`
  - AvalonDock is referenced by the Gesso UI project but no `DockingManager` is used anywhere yet. `<!-- claim: count "Dirkster.AvalonDock\"" src/Gesso/src/Gesso.UI/Gesso.UI.csproj = 1 -->` `<!-- claim: count "DockingManager" src/Gesso/**/*.xaml = 0 -->`
  - Gesso's own settings service writes under `%LOCALAPPDATA%\Gesso` rather than `Rizonesoft\Gesso`, the store `D01 T02 §2` replaces before any preference here is added. `<!-- claim: count "\"Gesso\"\);" src/Gesso/src/Gesso.UI/Services/SettingsService.cs = 1 -->`
  - Edit, Preferences is bound to a command with no dialog behind it until `D03 T07 §17`. `<!-- claim: count "Command=\"\{Binding PreferencesCommand\}\"" src/Gesso/src/Gesso.UI/Views/MainWindow.xaml = 1 -->`
  - There is no pen, stylus, or touch handling in Gesso. `<!-- claim: count "Stylus" src/Gesso/**/*.cs = 0 -->`
  - The welcome view model is a 12-line stub with a message and a version string. `<!-- claim: lines src/Gesso/src/Gesso.UI/ViewModels/WelcomeViewModel.cs = 12 -->`
- **Inputs and XREFs:** `standards/gesso.md`; `standards/shared.md` (settings, logging, atomic writes, refusal messages); Photoshop 27.10 Preferences, Workspace, Keyboard Shortcuts and Menus, Preset Manager, and Contextual Task Bar; Affinity Photo 3.3 studios, Customize Tools, Assets panel, and Settings; GIMP 3.2.6 Preferences, Dockable Dialogs, Input Devices, Input Controllers, Dashboard, and Error Console as behavior references; Microsoft Learn `RadialController`, `StylusPlugIn`, Windows Ink, and `IThumbnailProvider`; the Wacom WinTab 1.4 specification (`wintab32.dll`, installed by tablet drivers, never bundled); -> XREF: D02 T16 §1 (the workspace frame this file moves to `Isotone.UI`); -> XREF: D02 T16 §2 (the toolbar, toolbox, and status bar frame this file moves); -> XREF: D02 T16 §3 (the menu, context menu, and shortcut-set frame this file moves); -> XREF: D02 T16 §4 (`PreferenceKeyRegistry` and the coverage test moved to `Isotone.Core/Settings/`); -> XREF: D02 T16 §5 (`WarningRegistry` moved to `Isotone.UI`); -> XREF: D02 T16 §6 (brightness themes and `ThemeService` consumed, `SystemInfoReport` and `GpuDiagnostics` moved); -> XREF: D02 T16 §7 (the welcome frame moved to `Isotone.UI/Welcome/`); -> XREF: D02 T16 §8 (`PressureCurve` and the Surface Dial menu moved); -> XREF: D02 T16 §9 (rich tooltips consumed); -> XREF: D02 T06 §12 (the command index command search reads); -> XREF: D02 T07 §8 (`CompactNumberBox`, `UnitExpression`, and the contextual task bar host); -> XREF: D03 T07 §17 (workspaces and the Preferences dialog this file extends); -> XREF: D03 T07 §16 (the accessibility and localization audit that consumes §9's settings); -> XREF: D03 T03 §1 (document tabs §1 extends); -> XREF: D03 T03 §2 (history and undo memory §5 limits); -> XREF: D03 T03 §4 (the tool system and keymap §2 and §3 customize); -> XREF: D03 T02 §1 (the tile cache and swap §5 tunes); -> XREF: D03 T02 §5 (the ComputeSharp GPU path §5 toggles); -> XREF: D03 T04 §6 (autosave and recovery §5 configures); -> XREF: D03 T06 §1 (the Help menu, About, and shortcuts dialog §8 extends); -> XREF: D03 T08 §4 (rulers, units, guides, and grids whose display keys §4 exposes); -> XREF: D03 T08 §3 (screen modes whose surround colors §9 sets); -> XREF: D03 T08 §10 (windows arrangement and the navigator §1's window modes extend); -> XREF: D03 T11 §1 (the Adjustments and Properties panels §1 generalizes into Properties pages); -> XREF: D03 T11 §10 (swatches in the presets manager); -> XREF: D03 T09 §8 (styles in the presets manager); -> XREF: D03 T12 §3 (brush and tool presets §7 depends on); -> XREF: D03 T12 §9 (gradients in the presets manager); -> XREF: D03 T12 §10 (patterns in the presets manager); -> XREF: D03 T16 §7 (custom shapes in the presets manager); -> XREF: D03 T15 §12 (the Develop studio that becomes a studio preset); -> XREF: D03 T17 §10 (metadata defaults on export); -> XREF: D03 T18 §1 (export defaults); -> XREF: D03 T19 §1 (the AI quick-action registry the Contextual Task Bar shows); -> XREF: D03 T19 §10 (the Ask panel beside the Discover panel); -> XREF: D05 T01 §4 (the opt-in `UpdateChecker` §8 consumes); -> XREF: D01 T01 §2 (the exception window the debugging preference governs); -> XREF: D01 T01 §3 (the suite theme); -> XREF: D01 T01 §4 (the shared About and Shortcuts dialogs); -> XREF: D01 T02 §2 (the settings store every preference writes through).
- **Adjacency:** list=applicable @ D03 T20 §1 (workspaces, studios, shortcut sets, presets, assets, and resource folders are listed, searched, and tagged); document=applicable @ D03 T20 §3 (the shortcuts summary exported to HTML is the printed reference); settings=applicable @ D03 T07 §17 (the Preferences dialog this file fills, every key with a control, a default, and a consumer); reporting=applicable @ D03 T20 §8 (system information, GPU report, benchmark, dashboard, error console); notifications=applicable @ D03 T20 §8 (update notifications, what's new, low swap warning, background save progress in §5); permissions=applicable @ D03 T20 §5 (read-only or missing folders, an unreachable scratch disk, a malformed workspace or preset package, and an absent WinTab driver are refusals by name); audit=applicable @ D03 T20 §1 (each customization change logs one line; document edits stay one undo step each); exchange=applicable @ D03 T20 §7 (workspace, shortcut-set, preset, and asset packages import and export); reverse=applicable @ D03 T20 §4 (reset workspace, menus, shortcuts, tools, preferences, and factory reset at launch)

#### §1. Workspaces, panels, the Properties panel, and the Contextual Task Bar

- **Deliverable:** Gesso workspaces and studios as presets on the moved `Isotone.UI` workspace frame (switch, save, clone, rename, reorder, lock, import and export, function-key switching), panel docking and tab groups, hide all panels, document tabs that float and dock, single-window and multi-window modes, GIMP dockable dialogs, the Properties panel pages, the Contextual Task Bar, and shared numeric field behaviors.
- **Depends On:** D03 T07 §17, D02 T16 §1
- **Phase:** 27
- **Surface:** UI. Fidelity: Gesso main window -- docs/captures/gesso/main-window/, extended with one capture per preset under docs/captures/gesso/workspaces/ and docs/captures/gesso/contextual-task-bar/. Job: a user can switch the whole window for a task, carry the arrangement to another machine, and act on the current selection from a bar next to it. Treatment: a workspace and studio switcher (studios with name, icon, color, and function key), Window, Workspace menu, AvalonDock panels with tab groups, iconic collapse, and panel menus, document tabs with drag out and dock back, Window, Single-Window Mode, the Properties panel with Document, Pixel Layer, and Type pages, and a floating Contextual Task Bar with pin, reset, and hide. Cheaper substitute that fails: saving only the dock layout, which the part-by-part workspace comparison rejects. Chrome: consume the moved `Isotone.UI/Workspace/` frame, AvalonDock, the settings store, the keymap, `CompactNumberBox`, and the theme; do not add a second layout persistence or a second numeric box.
- **Runs:** `Requires: display-session -- switching, docking, floating tabs, and bar captures need an interactive desktop`
- **Catalog:** IP-2114 to IP-2133 (20 features)
- **Hints:**
  - First item, the move: `WorkspaceDefinition`, `WorkspaceService`, the workspace package reader and writer, panel visibility (Tab, Shift+Tab), lock panels, and panel quick customize move from `src/Stilus/Isotone.Stilus.Core/Workspace/` and `Isotone.Stilus.Desktop` (`D02 T16 §1`) into `src/Isotone.UI/Workspace/`, parameterized by app (package extension `.stilusws` or `.gessows`, preset folder, settings prefix); Stilus consumes them unchanged, tests move to `tests/Isotone.UI.Tests/Workspace/`, and the contextual task bar host from `D02 T07 §8` moves to `Isotone.UI/Workspace/ContextualTaskBarHost.cs` the same way.
  - Presets (IP-2114, IP-2115, IP-2117, IP-2119, IP-2123) as read-only JSON in `src/Gesso/Isotone.Gesso.Desktop/Workspace/Presets/`: Essentials, Photography, Painting, Graphic and Web, Compositing, Color Grading, Typography (over the `D03 T16` type panels), Develop (`D03 T15 §12`), and AI (`D03 T19 §1`); `Lock Workspace` stops drag and float; setting `Gesso.Workspace.Current`.
  - Studios (IP-2125): a studio is a workspace with a name, icon, color, enabled flag, order, and function key (F1 to F12 through `Gesso.Workspace.StudioKeys`); clone, rename, reorder, and enable or disable from a Studios page; workspaces also store shortcuts, menus, and toolbar (IP-2124) through the moved frame's parts.
  - Import and export (IP-2116): `.gessows` packages (JSON plus button images) with a part checklist on import; malformed or newer-schema packages refused by name with no partial import.
  - Docking (IP-2126, IP-2127): AvalonDock anchorables with tab groups, stacking, iconic collapse, panel menus, show or hide left and right docks; Tab hides all panels, Shift+Tab keeps the toolbar and options bar.
  - Workspace preferences (IP-2128, IP-2133): auto-collapse iconic panels, auto-show hidden panels on edge hover, open documents as tabs or floating, enable floating window docking, large tabs, focus activates image, save and restore window positions, open windows on the same monitor, reset saved positions; keys `Gesso.Workspace.*` consumed by the dock host.
  - Document tabs and window modes (IP-2129, IP-2130): drag a tab out to float, dock it back, Consolidate All to Tabs, a tab context menu (close others, reveal in Explorer, duplicate), show tabs, tab bar top or bottom, single-window and multi-window modes (multi-window floats docks as tool windows around image windows, GIMP style), windowed or full-screen app frame; extends `D03 T03 §1` and `D03 T08 §10`.
  - GIMP dockable dialogs (IP-2131, IP-2132): every panel is a dockable with a tab menu (add tab, close tab, detach, lock tab to dock, move to screen), tab style (icon, text, icon and text, automatic), preview size, list or grid view, button bar, image selection menu with auto follow active image, the Windows menu listing docks, and Recently Closed Docks.
  - Properties panel framework (IP-2121): generalize the `D03 T11 §1` Properties panel into registered pages keyed by context (Document with size, resolution, mode, and canvas; Pixel Layer with transform, align, and quick actions; Type with character and paragraph essentials), with a quick-actions strip reading the `D03 T19 §1` registry.
  - Contextual Task Bar (IP-2118, IP-2120): the moved host shows per-context actions (selection: select and mask, feather, invert, fill, generative fill; layer: mask, adjust, remove background; type: font, size, warp), with pin position, reset position, hide, and `Gesso.View.ContextualTaskBar`; AI actions come from the `D03 T19 §1` registry.
  - Numeric fields (IP-2122): consume `CompactNumberBox` and `UnitExpression` from `Isotone.UI` and `Isotone.Core/Units/` (moved from `D02 T07 §8` by the first Gesso section that needed a numeric field; if still in Stilus when this section is authored, the move is this section's second item) and extend them with scrubby labels (drag the label, Shift for ten times, Alt for a tenth), variables (`w`, `h`, `x`, `y`) and functions (`min`, `max`, `sqrt`, `round`), unit suffix conversion, and wheel increments with modifiers.
  - One Serilog Information line per workspace switch, save, import, and studio change; tests `GessoWorkspacePresetsTests` (every preset loads, part equality after package round trip), `PropertiesPagesTests`, `ContextualTaskBarTests`, `UnitExpressionVariablesTests`.
  - Commit: "gesso: workspaces and studios on the shared frame, docking, window modes, Properties pages, and the Contextual Task Bar"
- **Proof:** Format fidelity proof plus driven run: `tests/fixtures/gesso/workspace/photography.gessows` imports and re-exports with every part equal, a Stilus workspace test still passes against the moved type (`grep -rn "class WorkspaceService" src` prints one path under `src/Isotone.UI/`), and a driven run switches three presets with captures and one log line each; cheaper substitute that fails: a second Gesso copy of the workspace model, which the single-class grep rejects.

#### §2. The toolbar and the options bar

- **Deliverable:** A customizable toolbar (flyout groups, single or double column, Extra Tools slot, Edit Toolbar, per-workspace tool customization, grouping toggle, GIMP toolbox indicator areas), the Tools menu, tool switching conventions, an options bar and context toolbar (floating or pinned, narrow, reset), a customizable top toolbar, and modifier-plus-wheel canvas adjustments, on the moved `CommandBarDefinition` frame.
- **Depends On:** §1, D02 T16 §2
- **Phase:** 27
- **Surface:** UI. Fidelity: Gesso main window -- docs/captures/gesso/main-window/, with new captures under docs/captures/gesso/toolbar/. Job: a user can put the tools and commands they use where they want them and switch tools by habit. Treatment: an Edit Toolbar dialog (drag tools between the toolbar and Extra Tools, regroup, presets, Restore Defaults, Clear Tools, show or hide the foreground and background, quick mask, and screen mode controls), a Customize Toolbar page for the top toolbar (drag on or off, icon only or icon and text), and an options bar with pin and float. Cheaper substitute that fails: a fixed XAML toolbar with visibility toggles. Chrome: consume the moved `CommandBarDefinition`, `ToolboxDefinition`, and `CommandBarHost`, the keymap command registry, and the §1 workspace parts.
- **Runs:** `Requires: display-session -- toolbar drag customization and tool cycling are driven runs`
- **Catalog:** IP-2134 to IP-2145 (12 features)
- **Hints:**
  - First item, the move: `CommandBarDefinition`, `CommandBarHost`, `ToolboxDefinition`, and `StatusBarConfig` move from `src/Stilus/Isotone.Stilus.Core/Workspace/` and `Isotone.Stilus.Desktop/Controls/CommandBars/` (`D02 T16 §2`) into `src/Isotone.UI/Workspace/`, Stilus consuming them unchanged; tests move with them.
  - Toolbar (IP-2134, IP-2135, IP-2138): Gesso's `ToolboxDefinition` preset with flyout groups from the `D03 T03 §4` tool system, single or double column, an Extra Tools slot, a grouping toggle (GIMP: groups on or off), and the Edit Toolbar dialog (reorder, group, save presets, Restore Defaults, Clear Tools, show or hide the bottom controls).
  - Per-workspace tools (IP-2139): the toolbar definition is a §1 workspace part, so each workspace or studio has its own tools, flyouts, and column count with Reset.
  - GIMP toolbox areas (IP-2136, IP-2142): foreground and background swatches, active brush, pattern, and gradient previews (clicking opens their choosers), active image thumbnail, and a drop target that opens dropped files, each toggleable.
  - Tools menu (IP-2140): a Tools top-level menu listing every registered tool by group with its shortcut.
  - Tool switching (IP-2141): spring-loaded shortcuts (hold a tool key to use it temporarily, release to return), Shift plus the key or repeated key to cycle a group (`Gesso.Tools.ShiftCyclesGroup`), and swap to previous tool; extends the `D03 T03 §4` keymap.
  - Options bar (IP-2137, IP-2143): the options bar and a floating context toolbar, pinned or floating, hide advanced options, narrow mode, and Reset Tool and Reset All Tools from its tool icon menu.
  - Top toolbar (IP-2144): a `CommandBarDefinition` of commands with drag on or off, icon only or icon and text, and Show Toolbar.
  - Wheel on canvas (IP-2145): configurable modifier plus wheel mappings for brush size, opacity, zoom, and rotate view (`Gesso.Input.WheelModifiers`), with the default set Ctrl for zoom, Alt for size, Shift for opacity.
  - One Serilog Information line per customization change naming the bar and item; tests `GessoToolboxDefinitionTests` (group cycling order, per-workspace toolbar), `SpringLoadedToolTests`, `WheelModifierMapTests`.
  - Commit: "gesso: the customizable toolbar, options bar, top toolbar, and tool switching on the shared frame"
- **Proof:** Unit test plus driven run: `SpringLoadedToolTests` hold and release a tool key and assert the previous tool returns, `GessoToolboxDefinitionTests` round-trip a customized toolbar through a workspace package, and a driven Edit Toolbar drag survives restart (capture); cheaper substitute that fails: a toolbar that resets on restart, which the capture after restart rejects.

#### §3. Menus, shortcuts, and command search

- **Deliverable:** The Keyboard Shortcuts and Menus dialog (shortcuts for menus, panel menus, tools, filters, blend modes, and task workspaces; per-workspace or shared; single-key shortcuts), shortcut set files and an HTML summary, suite default keymap conventions, legacy undo and channel shortcut options, menu customization (hide, color, named sets), and command search with menu path and help, on the moved `MenuDefinition` and `ShortcutManager` frame.
- **Depends On:** §1, D02 T16 §3
- **Phase:** 27
- **Surface:** UI. Fidelity: extends the shortcuts dialog -- docs/captures/gesso/shortcuts/ (from `D03 T06 §1`) and the Preferences dialog -- docs/captures/gesso/preferences/ (from `D03 T07 §17`); new captures under docs/captures/gesso/command-search/. Job: a user can make menus and shortcuts match their habits, carry them between machines, and run any command by name. Treatment: a Keyboard Shortcuts and Menus dialog with Menus, Shortcuts, and Summarize tabs, set picker with Save, Save As, Delete, and Reset, a shortcut table per area (application menus, panel menus, tools, filters, blend modes, task workspaces), and a command search overlay (Ctrl+F) showing command, menu path, shortcut, and a help button. Cheaper substitute that fails: a second shortcut list outside the shared `ShortcutManager`. Chrome: consume the moved `MenuDefinition`, `MenuBuilder`, `ShortcutManager`, and the `D02 T06 §12` command index; do not build a second command list.
- **Runs:** `Requires: display-session -- menu customization and command search are driven runs`
- **Catalog:** IP-2146 to IP-2153 (8 features)
- **Hints:**
  - First item, the move: `MenuDefinition`, `MenuBuilder`, the `ContextMenuProvider` framework (the selection kinds stay per app), `ShortcutManager` with its context dimension, shortcut set files, and the TXT and CSV export move from Stilus (`D02 T16 §3`) into `src/Isotone.UI/Workspace/`, and the `D02 T06 §12` command index moves beside them as `Isotone.UI/Workspace/CommandIndex.cs`; Stilus consumes them unchanged.
  - Shortcut areas (IP-2147): Gesso contexts Main, TextEditing, Painting (tool modifiers), and Develop, plus per-area tables for application menus, panel menus, tools, filters, blend modes (Shift+Alt+letter), and task workspaces; per-workspace or shared sets (`Gesso.Shortcuts.PerWorkspace`); single-key shortcuts with a conflict refusal naming the holder.
  - Set files (IP-2148): save, load, save on exit, reset to defaults, alternate default sets (Photoshop-like, Affinity-like, GIMP-like, shipped read-only), remove all.
  - Summary (IP-2149): Summarize writes an HTML table (area, command, shortcut) through the atomic writer and opens it.
  - Suite conventions (IP-2150): one menu and shortcut set across the suite where commands coincide (resize document Ctrl+Alt+I, resize canvas Ctrl+Alt+C, fill Shift+F5, content-aware fill and inpaint), recorded in `docs/user/isotone/shortcuts.md` and asserted by a cross-app test over the three default sets.
  - Legacy options (IP-2151): `Gesso.Shortcuts.LegacyUndo` (Ctrl+Z toggles undo and redo) and `Gesso.Shortcuts.LegacyChannels` (Ctrl+1 to Ctrl+5 select channels), consumed by the keymap.
  - Menu customization (IP-2152): hide items, color items, named menu sets saved in the workspace, and Show Menu Colors, rendered by `MenuBuilder`.
  - Command search (IP-2146, IP-2153): an overlay over the command index returning commands and filters with menu path, shortcut, and a help button opening the command's user-guide anchor; stock and cloud results are not offered.
  - One Serilog Information line per shortcut or menu change and per set load; tests `GessoShortcutAreasTests`, `ShortcutSummaryHtmlTests` (golden HTML), `SuiteKeymapConventionTests`, `CommandSearchTests`.
  - Commit: "gesso: shortcut sets, menu customization, and command search on the shared frame"
- **Proof:** Unit test plus format fidelity proof: `ShortcutSummaryHtmlTests` match `tests/fixtures/gesso/shortcuts/default-summary.html`, `SuiteKeymapConventionTests` prove the shared commands have the same gesture in the Stilus and Gesso default sets, and `grep -rn "class ShortcutManager" src` prints one path under `src/Isotone.UI/`; cheaper substitute that fails: a Gesso-only shortcut table, which the single-class grep and the cross-app test reject.

#### §4. Preferences I: general, tools, cursors, units, guides, and type

- **Deliverable:** The General, Tools, Cursors, Transparency, Units and Rulers, Guides and Grid, Type, Tooltips, Notifications, and Assistant preference pages, each key with a control, a default, and a named consumer proven by a coverage test, plus preferences search, reset, backup, and migrate.
- **Depends On:** D03 T07 §17
- **Phase:** 27
- **Surface:** UI. Fidelity: extends the Preferences dialog -- docs/captures/gesso/preferences/ (from `D03 T07 §17`). Job: a user can tune how Gesso behaves and find any preference by name. Treatment: pages General, Tools, Cursors, Transparency, Units and Rulers, Guides, Grid, and Slices, Type, Tooltips, Notifications, and Assistant, with a search box filtering controls and a category filter, Reset per page and all, and Back Up and Migrate. Cheaper substitute that fails: controls that persist a value nothing reads. Chrome: consume the `D03 T07 §17` dialog shell, the moved `PreferenceKeyRegistry`, the settings store, and rich tooltips; do not open a second options window.
- **Runs:** `Requires: display-session -- preference captures and driven changes need an interactive desktop`
- **Catalog:** IP-2163 to IP-2185 (23 features)
- **Hints:**
  - First item, the moves: `PreferenceKeyRegistry` and the coverage test pattern move from `src/Stilus/Isotone.Stilus.Core/Settings/` (`D02 T16 §4`) to `src/Isotone.Core/Settings/PreferenceKeyRegistry.cs`, and `WarningRegistry` from `D02 T16 §5` to `src/Isotone.UI/Warnings/`; Stilus consumes both unchanged; Gesso registers its keys and generates `docs/dev/gesso/preference-keys.md`.
  - General (IP-2164, IP-2173, IP-2176): limit initial zoom to 100 percent, auto-update open documents changed on disk, beep when done, export clipboard on exit, legacy free transform, reopen documents on startup (the key shared with §5), hide file extensions in titles, and notification toasts on or off; each key `Gesso.General.*` with its consumer named.
  - Tools (IP-2179, IP-2180): handle size, marquee intersect selects, move aspect constraint, nudge distance, sync tools between documents, edit non-visible layers, save tool options on exit, reset tool options, and share brush, dynamics, pattern, gradient, and expand-layers settings between tools (GIMP), consumed by the tool system and brush engine.
  - Cursors (IP-2165, IP-2171, IP-2178): standard, precise, or brush-size painting cursors, full-size tip, crosshair in brush tip, crosshair only while painting, brush preview color, brush outline snapping, pointer handedness, and Caps Lock for precise, consumed by the cursor service.
  - Display (IP-2166, IP-2167, IP-2168, IP-2169, IP-2170, IP-2182, IP-2184): guides, grid, smart guides, slices, and path colors and styles and path thickness, on-canvas widget size, transparency grid check size, colors, and style, artboard canvas color and outline; each consumed by the `D03 T08 §4` overlays and the canvas renderer.
  - Units and rulers (IP-2183): ruler and type units, column size and gutter, new document preset resolutions for print and screen, point size (PostScript 72 or traditional 72.27), decimal places, and lines and text in points.
  - Type (IP-2185): smart quotes, missing glyph protection, English font names, Esc commits text, placeholder text, text engine choice (default or world-ready layout, both HarfBuzz through `D03 T16 §1`), font preview size, recent fonts count, font menu background.
  - Tooltips (IP-2177): show tooltips, rich tooltips (the `D02 T16 §9` rich tooltip control, moved to `Isotone.UI` if still in Stilus), tooltip delay, and maximum width.
  - Numeric math (IP-2163): the preference that enables math expressions and variables in every numeric field of §1 (on by default).
  - Assistant (IP-2181): automatic behavior policies for painting with no layer (create one), brushing or erasing on vector layers (rasterize, new layer, or refuse), filters on vector layers, adjustments and filters applied to the selection, one undo step for automatic actions, and alerts through `WarningRegistry`.
  - Privacy (IP-2174): usage data and crash report opt-in, both off by default, the page stating that Gesso sends nothing unless enabled; with the crash opt-in off, the `D01 T01 §2` exception window offers to save the report locally only.
  - Search, reset, back up, migrate (IP-2172, IP-2175): a search box filtering controls by label and key, reset on quit, reset at next launch (Ctrl+Alt+Shift held at startup, Photoshop convention), reset defaults per page and for all, back up and restore settings as a ZIP through the atomic writer, and migrate settings from an earlier Gesso version folder.
  - One Serilog Information line per preference change naming the key and new value; tests `GessoPreferencesCoverageTests` (every key has a control, default, and existing consumer), `PreferencesSearchTests`, `PreferencesBackupTests`.
  - Commit: "gesso: general, tools, cursor, display, units, type, tooltip, assistant, and privacy preferences"
- **Proof:** Unit test plus driven run: `GessoPreferencesCoverageTests` fail when a registered key loses its consumer, `PreferencesBackupTests` round-trip a backup ZIP and restore every key, and a driven change of the transparency grid colors shows in a canvas capture and in `settings.json`; cheaper substitute that fails: a page whose values nothing reads, which the coverage test rejects.

#### §9. Interface appearance, language, and accessibility display preferences

- **Deliverable:** Themes (dark, light, gray levels, follow the OS scheme and accent, highlight color, custom themes), icon themes, UI scaling and font size, larger spin-scale sliders, merged title and menu bar, interface language independent of the OS with right-to-left layouts, accessibility display options, canvas and artboard surround colors, and preview sizes.
- **Depends On:** §4
- **Phase:** 27
- **Surface:** UI. Fidelity: Gesso main window -- docs/captures/gesso/main-window/, with new captures under docs/captures/gesso/appearance/. Job: a user can make Gesso comfortable and readable on their display and in their language. Treatment: an Interface page (theme, follow system, accent and highlight color, custom theme file, dark title bar, reload theme, icon theme and style, icon scale, UI font size, scale UI to font, UI scale, larger sliders, merge menu into title bar), a Language page, an Accessibility display page, and a Canvas page (surround color per screen mode, border, pasteboard gray levels, preview sizes). Cheaper substitute that fails: a theme switch that needs a restart or leaves hardcoded colors. Chrome: consume the `D01 T01 §3` suite theme and the `D02 T16 §6` brightness dictionaries and `ThemeService` in `Isotone.UI`, the icon catalog, and the settings store.
- **Runs:** `Requires: display-session -- theme, scale, language, and right-to-left captures need an interactive desktop`
- **Catalog:** IP-2186 to IP-2197 (12 features)
- **Hints:**
  - Themes (IP-2186, IP-2189): consume `ThemeService` and the four brightness dictionaries in `src/Isotone.UI/Themes/`; follow the Windows app mode and accent through `UISettings.ColorValuesChanged`; highlight color token override; custom themes as a token override XAML file validated against the token list (the Gesso equivalent of GIMP CSS themes), Reload Theme, and a dark title bar through `DWMWA_USE_IMMERSIVE_DARK_MODE`.
  - Icons (IP-2187, IP-2190): the icon catalog renders vector icons at any scale; icon style color, monochrome, or symbolic as catalog variants, with the legacy set not shipped (documented); `Gesso.UI.IconStyle` and icon scale consumed by `VectorIcon`.
  - Scaling (IP-2192): UI font size, scale UI to font, auto (per-monitor DPI) or fixed scale 100 to 200 percent through the root `LayoutTransform` helper that moves from `D02 T16 §6` into `src/Isotone.UI/Windowing/UiScale.cs` with the Windows 11 chrome helpers, as their second consumer.
  - Sliders (IP-2188): a `SpinScale` control (GIMP spin scale: a slider with inline value, plus and minus buttons, larger height option `Gesso.UI.LargeSliders`) in `Isotone.UI/Controls/` built on `CompactNumberBox`.
  - Title bar (IP-2191): merge the menu bar into the title bar with a custom caption area that keeps snap layouts (the helper moved above).
  - Language and right-to-left (IP-2193, IP-2194): `Gesso.UI.Language` (a culture or Follow Windows) applied at startup through resource lookups, with the pseudo-locale and the `.resx` extraction owned by `D03 T07 §16`; `FlowDirection.RightToLeft` for RTL cultures with the canvas and rulers kept left-to-right.
  - Accessibility display (IP-2195): larger UI font, handle size, UI contrast (high-contrast tokens), text contrast, UI brightness, and reduce motion (disables animated zoom and panel animations), each consumed by the theme or canvas; `D03 T07 §16`'s audit runs over them.
  - Canvas (IP-2196, IP-2197): surround color per screen mode (standard, full screen with menus, full screen), border style (drop shadow, line, none), pasteboard gray levels, image window appearance, and layer, channel, group, undo, and navigator preview sizes consumed by the panels.
  - One Serilog Information line per appearance change; tests `CustomThemeValidatorTests`, `UiScaleTests` (moved), `RightToLeftLayoutTests` (canvas stays left-to-right), `SpinScaleTests`.
  - Commit: "gesso: themes, icon styles, UI scaling, language and right-to-left, accessibility display, and canvas appearance"
- **Proof:** Unit test plus driven run: `CustomThemeValidatorTests` reject a theme missing a token and accept a complete one, `RightToLeftLayoutTests` assert panel flow is right-to-left while the canvas transform is unchanged, and captures in Light and Dark at 100 and 200 percent plus one right-to-left capture are committed; cheaper substitute that fails: a restart-only theme switch, which the live `ThemeService` test rejects.

#### §5. Preferences II: files, performance, memory, and resources

- **Deliverable:** File handling, import policy, export default, develop, and new-image preferences, background saving, performance (memory, history and cache levels, tile cache, threads), GPU and display renderer settings, view and zoom quality, scratch disks and swap, experimental feature toggles, and Windows Explorer thumbnails for `.gesso` files.
- **Depends On:** §4
- **Phase:** 27
- **Surface:** UI. Fidelity: extends the Preferences dialog -- docs/captures/gesso/preferences/ (from `D03 T07 §17`). Job: a user can control how Gesso reads and writes files, uses memory, disk, and the GPU, and how its files look in Explorer. Treatment: pages File Handling, Import, Export, Develop, Performance, Graphics Processor, Scratch Disks, New Image, and Technology Previews, each key with a default and consumer; a memory slider with the ideal range; history and cache presets; background save with progress and Cancel in the status bar. Cheaper substitute that fails: a background save that blocks the UI thread. Chrome: consume the §4 registry, the settings store, the atomic writer, the `D03 T04 §6` recovery, the `D03 T02 §1` tile cache, the `D03 T02 §5` GPU path, and `D05 T01`'s installer for shell registration.
- **Runs:** `Requires: display-session -- background save progress, GPU settings, and Explorer thumbnails are driven runs`
- **Catalog:** IP-2198 to IP-2214 (17 features)
- **Hints:**
  - File handling (IP-2198, IP-2204): reopen documents on startup, image previews in saved files, extension case, save as to original folder, no copy suffix, thumbnail size limits, and recent files count; keys `Gesso.Files.*` consumed by the save path and `D03 T04 §6`.
  - Background saving (IP-2200): `src/Gesso/Isotone.Gesso.Desktop/Services/BackgroundSaveService.cs` snapshots the document by tile copy-on-write through the `D03 T03 §2` snapshot mechanism (the Stilus service serializes an SVG model, so only its UI pattern is shared), writes through the atomic writer on a worker, reports progress with Cancel, and keeps the previous file byte-identical on cancel or failure.
  - Import policies (IP-2206): promote to float with dither on import, add alpha, color profile policy (keep, convert to working, ask), ignore EXIF color space tag, rotation metadata policy, lock background on import; consumed by the open path.
  - Export defaults (IP-2201, IP-2207): include color profile, comment, thumbnail, EXIF, XMP, and IPTC, update metadata, default export type, and legacy Export As, consumed by `D03 T18 §1` and `D03 T17 §10`.
  - Develop preferences (IP-2202, IP-2205): appearance, sidecar XMP read and write through `D01 T07 §6`, performance (preview cache size), technology previews, HDR editing default, and the RAW open handler (Develop studio or Camera Raw dialog, consumed by `D03 T07 §11`).
  - Performance (IP-2203, IP-2208, IP-2210): default interpolation, memory usage with RAM limit (percent of physical with the ideal range shown), history and cache presets (small documents, default, huge pixel dimensions) setting history states, cache levels, and tile size, tile cache size, undo memory limit (`D03 T03 §2`), maximum new image size, worker threads, SIMD optimizations toggle for diagnosis, precise clipping, view quality, and zoom quality.
  - Graphics processor (IP-2199, IP-2209): use GPU (ComputeSharp through `D03 T02 §5`, falling back to CPU with a Warning), adapter choice, anti-aliased guides, 30-bit display through the `D03 T15 §4` swap-chain host in `R10G10B10A2`, native canvas, high-DPI rendering, and compute acceleration; OpenCL is not used and the page says so; the moved `GpuDiagnostics` (§8) supplies the adapter list.
  - Scratch (IP-2211): scratch disks for tile swap in priority order with free space, disk usage warning threshold, temporary and swap folders, swap compression; a read-only or missing folder refused by name when chosen.
  - New image and grid defaults (IP-2212): default new image size and fill, default grid, and dialog defaults consumed by `D03 T08 §2` and `D03 T08 §4`.
  - Technology previews (IP-2213): `Gesso.Experimental.*` toggles listed from a registry with a warning banner.
  - Explorer thumbnails (IP-2214): a COM-hosted `IThumbnailProvider` and `IInitializeWithStream` in a new class library `src/Gesso/Isotone.Gesso.ShellThumbnails/` (`EnableComHosting`) that reads `Thumbnails/thumbnail.png` from the `.gesso` ZIP (the OpenRaster thumbnail), registered by the Gesso installer under the thumbnail handler key; this is the one new Gesso project, recorded as a decision because Explorer loads handlers only from a separate COM server.
  - One Serilog Information line per preference change and per background save start, completion, and cancel; tests `GessoBackgroundSaveTests` (cancel leaves the file byte-identical), `ScratchFolderTests`, `ThumbnailProviderTests` (extracts the fixture thumbnail from a stream).
  - Commit: "gesso: file, import, export, develop, performance, GPU, scratch, and new-image preferences, background save, and Explorer thumbnails"
- **Proof:** Unit test plus driven run: `GessoBackgroundSaveTests` compare SHA-256 of the previous file before and after a cancelled save and edit the document during a save, `ThumbnailProviderTests` return the committed fixture's thumbnail bytes, and a driven run after installing shows `.gesso` thumbnails in Explorer (capture); cheaper substitute that fails: a synchronous save, which the edit-during-save test rejects.

#### §6. Pen, touch, and input devices

- **Deliverable:** Pen input with pressure, tilt, rotation, and velocity through Windows Ink or WinTab, calibrated pressure curves, touch and trackpad gestures with a touch-for-gestures-only mode, Surface Dial and Surface Pen, an Input Devices dialog with per-device tools and settings, GIMP input controllers, and canvas mouse-button and modifier mapping.
- **Depends On:** §4
- **Phase:** 27
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/input-devices/. Job: a painter can use a pen, touch, and Dial naturally and map every button to their habit. Treatment: an Input Devices dialog (devices list with status, API Windows Ink or WinTab, pressure curve editor, per-device current tool and tool options, save and reset), a Controllers page (mouse wheel events to actions, enable, dump events), a Canvas Interaction page (mouse buttons and modifiers to actions, reset), and gestures on the canvas. Cheaper substitute that fails: treating the pen as a mouse. Chrome: consume the moved `PressureCurve` and Dial menu, the `D03 T12 §2` dynamics that read pressure, the canvas view transform, and the settings store; do not add a second stylus reader.
- **Runs:** `Requires: display-session -- pen, touch, and Dial are driven on a pen-enabled Windows device`
- **Catalog:** IP-2215 to IP-2222 (8 features)
- **Hints:**
  - First item, the move: `PressureCurve` from `src/Stilus/Isotone.Stilus.Core/Input/` and the Surface Dial menu helper from `D02 T16 §8` move to `src/Isotone.Core/Input/PressureCurve.cs` and `src/Isotone.UI/Input/DialMenu.cs`; Stilus consumes them unchanged.
  - `src/Gesso/Isotone.Gesso.Desktop/Input/PenInputSource.cs` (IP-2216, IP-2217): Windows Ink through WPF stylus events with pressure, tilt (X and Y), twist, and computed velocity into the canvas tool point, the only stylus reader in Gesso.
  - WinTab (IP-2217): `WinTabInputSource` P/Invoking `wintab32.dll` (installed by tablet drivers, never bundled) with packet queue reading, selected by `Gesso.Input.PenApi` (WindowsInk, WinTab); an absent driver is refused by name ("WinTab is not installed; using Windows Ink").
  - Calibration: the pressure curve editor (points and gamma) per device, saved under `Gesso.Input.Devices.<Id>.PressureCurve`.
  - Input Devices dialog (IP-2220): devices with status, per-device tool and tool options (GIMP: each device remembers its tool), share tool options toggle, save and reset device settings.
  - Touch and trackpad (IP-2218): pinch zoom around the pinch center, two-finger pan and rotate, tap-and-hold for flyouts, and touch-for-gestures-only so fingers never paint (`Gesso.Input.TouchGesturesOnly`, default true).
  - Surface Dial and Pen (IP-2219): the moved Dial menu with Zoom, Rotate View, Brush Size, Opacity, and Undo items, and Surface Pen barrel button and eraser end mapped to actions.
  - Controllers (IP-2221): mouse wheel and extra-button events mapped to actions, enable per controller, and Dump Events writing raw events to the log at Debug.
  - Canvas interaction (IP-2215, IP-2222): mouse button plus modifier to action mappings (pan, zoom, rotate view, pick color, resize brush) with reset, consumed by the canvas input router.
  - One Serilog Information line per device setting change; tests `PenInputMappingTests` (synthetic stylus points to tool points with calibrated pressure), `WinTabPacketParserTests`, `CanvasInteractionMapTests`, `GestureMathTests` (pinch center fixed in document space).
  - Commit: "gesso: pen input through Windows Ink or WinTab, touch gestures, the Surface Dial, and input device settings"
- **Proof:** Unit test plus driven run: `GestureMathTests` prove pinch zoom keeps the pinch center fixed in document space, `PenInputMappingTests` prove calibrated pressure reaches a fake brush, and a driven pen stroke on a pen device logs varying pressure (Debug lines quoted) with `grep -rn "StylusPoint" src/Gesso` finding one reader; cheaper substitute that fails: mouse-only input, which the pressure mapping test rejects.

#### §7. The presets manager and resource libraries

- **Deliverable:** A Preset Manager over every preset type (brushes, swatches, gradients, styles, patterns, contours, custom shapes, tools), preset migration, import, and export, add-on packages, the Assets panel with its own package format, presets in panels with groups and tags, and GIMP data and resource folders.
- **Depends On:** §4, D03 T12 §3
- **Phase:** 27
- **Surface:** UI. Fidelity: new build, no baseline; captured to docs/captures/gesso/preset-manager/ and docs/captures/gesso/assets-panel/. Job: a user can organize, move, back up, and share their presets and assets. Treatment: a Preset Manager (type picker, list or thumbnail view, load, save set, rename, delete, groups, tags), Export and Import Presets and Migrate Presets commands, an Assets panel (categories, subcategories, add from selection, drag to place, embed or link), and a Folders page (per resource type, system and personal folders, add, reorder, delete, open). Cheaper substitute that fails: one folder per type with no manager, tags, or export. Chrome: consume each resource type's own reader and library (`D03 T12 §3`, `D03 T11 §10`, `D03 T12 §9`, `D03 T09 §8`, `D03 T12 §10`, `D03 T16 §7`), the smart objects of `D03 T09 §9`, and the atomic writer; add no second reader for any format.
- **Runs:** `Requires: display-session -- manager, assets panel, and package round-trip captures need an interactive desktop`
- **Catalog:** IP-2223 to IP-2232 (10 features)
- **Hints:**
  - `src/Gesso/Isotone.Gesso.Core/Resources/IResourceLibrary.cs` implemented by each existing library (brushes, swatches, gradients, styles, patterns, contours, shapes, tool presets) so the Preset Manager (IP-2224, IP-2229) lists, loads, saves sets, renames, deletes, and switches list or thumbnail views through one interface.
  - Groups and tags (IP-2231): groups inside each panel and GIMP-style resource tags stored in `%LOCALAPPDATA%\Rizonesoft\Gesso\resources\tags.json`, with tag filtering in every chooser and linked content categories.
  - Export, import, migrate (IP-2223, IP-2230): `.gessopresets` packages (ZIP with a manifest per type) written through the atomic writer; Migrate Presets imports from an earlier Gesso version's folder; competitor preset files come in through each type's own importer (ABR, GRD, ASL, PAT, ACO, ASE, CSH), none bundled.
  - Add-ons (IP-2225): an add-on package is a `.gessopresets` with brushes, styles, palettes, and assets; macros are not included until B-041.
  - Assets panel (IP-2226, IP-2227): categories and subcategories, add from selection (layers become a stored asset), drag or click to place as an embedded or linked smart object through `D03 T09 §9`, and `.gessoassets` import and export; Affinity `.afassets` is not read because its layout is not published (recorded in the decision row).
  - Data folders (IP-2232): per resource type, the system folder (read-only, install directory) and personal folders (writable), add, reorder, and delete folders, with Open Lens Profiles Folder (the lensfun user database folder of `D01 T07 §3`) and Open Fonts Folder buttons; a read-only personal folder is refused by name.
  - Keyboard mnemonics (IP-2228): every resource chooser button has an access key and an automation name.
  - One Serilog Information line per import, export, migrate, and asset add; tests `PresetPackageTests` (round trip for every type), `ResourceTagTests`, `AssetsLibraryTests`.
  - Commit: "gesso: the Preset Manager, preset packages, tags, the Assets panel, and resource folders"
- **Proof:** Format fidelity proof: `PresetPackageTests` export a package with one preset of every type from `tests/fixtures/gesso/presets/`, import it into an empty profile, and compare each preset byte for byte or field by field; cheaper substitute that fails: a package that only copies brush files, which the per-type comparison rejects.

#### §8. Help, learning, and diagnostics

- **Deliverable:** The Help menu with the local or online manual, context help, and help history, online links, what's new and release notes, the opt-in update check, the Home screen, the Discover panel, tip of the day, status bar modifier hints, system information and GPU report, a benchmark, a dashboard with performance log recording, an error console, and the debugging preference.
- **Depends On:** §1
- **Phase:** 27
- **Surface:** UI. Fidelity: extends the Help menu and About -- docs/captures/gesso/help/ (from `D03 T06 §1`); new captures under docs/captures/gesso/home/, docs/captures/gesso/dashboard/, and docs/captures/gesso/error-console/. Job: a user can learn Gesso in place, see what is new, and diagnose problems locally without sending anything. Treatment: Help menu entries, F1 context help, a Home screen (recent files with filters and keys, create new, release notes, contribute, personalize, auto show), a Discover panel (search the bundled help, tutorials, hands-on steps), a Dashboard panel, an Error Console panel, and System Information and Benchmark dialogs. Cheaper substitute that fails: a Help menu of web links only. Chrome: consume the moved welcome frame, `SystemInfoReport`, and `GpuDiagnostics`, the `D05 T01 §4` `UpdateChecker`, the `D01 T01 §2` exception window, the shared About dialog, and the dock.
- **Runs:** `Requires: display-session -- help, Home, dashboard, and console captures need an interactive desktop`
- **Catalog:** IP-2234 to IP-2246 (13 features)
- **Hints:**
  - First item, the moves: the welcome frame (`WelcomeView`, recent-with-thumbnails, pin, remove) from `D02 T16 §7` to `src/Isotone.UI/Welcome/`, and `SystemInfoReport` and `GpuDiagnostics` from `D02 T16 §6` to `src/Isotone.UI/Diagnostics/`; Stilus consumes them unchanged; Gesso's 12-line `WelcomeViewModel` is replaced.
  - Help menu (IP-2234): user manual sections from `docs/user/gesso/` shipped as HTML in the install (local) or opened on the repository docs site (online, `Gesso.Help.Source`), help buttons in dialogs and F1 context help through a `HelpTopic` attached property, and help history (back and forward in the viewer).
  - Links (IP-2235): forums (GitHub Discussions), bug and feature requests (GitHub Issues), support, developer site, roadmap, and legal notices (licenses of every bundled dependency and the lensfun attribution).
  - What's new and updates (IP-2236, IP-2237): What's New and release notes from the bundled changelog shown once after an update; the opt-in `UpdateChecker` of `D05 T01 §4` with frequency (never, daily, weekly; default never) and an in-app notification when a newer release exists.
  - Home screen (IP-2238): the moved frame with Gesso's recent files (thumbnails from the `.gesso` ZIP thumbnail, filters by type, keyboard navigation), create new from presets, release notes, contribute, personalize, and auto show (`Gesso.Home.ShowWhenEmpty`).
  - Discover panel (IP-2239): search over the bundled help with a local index, tutorials and hands-on step lists from bundled JSON that highlight the relevant control; no online learning feed; the `D03 T19 §10` Ask tab and the `D03 T19 §1` AI quick actions appear here when AI is enabled.
  - Tip of the day and modifier hints (IP-2240, IP-2241): a tip dialog from bundled tips with show at startup, and the status bar showing the active tool's modifier hints (Shift, Alt, Ctrl) as the keys are held.
  - Diagnostics (IP-2242, IP-2243): System Information with GPU compatibility (adapter, driver, DirectX 12 feature level, ComputeSharp support, HDR capability) and Copy and Save; Benchmark running fixed workloads (composite, Gaussian blur, brush strokes, open and save) on a generated document with results saved as JSON beside a committed baseline.
  - Dashboard (IP-2244): cache, swap, CPU, memory, and thread groups with update interval and history length, performance log recording with markers to a JSON file, and a low swap warning.
  - Error console and debugging (IP-2245, IP-2246): an Error Console panel over a Serilog in-memory sink (Warning and above by default) with clear, save, select all, and highlight by kind; `Gesso.Debug.CrashDebugger` (never, warnings, errors, always) choosing when the `D01 T01 §2` exception window offers the debugger.
  - One Serilog Information line per update check, benchmark run, and performance log start and stop; tests `HelpTopicTests` (every dialog has a topic resolving to a page), `ErrorConsoleSinkTests`, `BenchmarkRunnerTests`, `DashboardSamplerTests`.
  - Commit: "gesso: Help, the Home screen, Discover, tips, and local diagnostics"
- **Proof:** Unit test plus driven run: `HelpTopicTests` resolve every registered dialog's F1 topic to an existing heading in `docs/user/gesso/`, `ErrorConsoleSinkTests` capture a Warning and save it, and a driven Benchmark run writes a result JSON compared against the committed baseline with the delta quoted; cheaper substitute that fails: help as web links only, which the offline topic-resolution test rejects.

#### Sizing concerns

- §1 owns 20 features across two jobs (workspaces, studios, Properties pages, and the Contextual Task Bar; then docking, tabs, window modes, and GIMP dockable dialogs) plus two moves, and its hints will expand to about 30 items; the natural split is §1 for workspaces, studios, Properties pages, the Contextual Task Bar, and numeric fields (IP-2114 to IP-2125) and a new section for docking, document tabs, window modes, and dockable dialogs (IP-2126 to IP-2133) depending on it.
- §4 owns 23 features and two moves; if it passes 30 items, the Assistant and privacy rows (IP-2174, IP-2181) move to §5, which already holds the policy-style preferences.

### todo/03-gesso/TODO-21-gesso-parity-releases.md -- `gesso-parity-releases`

- **Title:** "TODO-21 -- Gesso Parity Releases: 0.2.0 to 1.0.0"
- **Phase(s):** 16 to 27, one release section at the end of each
- **Goal:** Each Gesso parity phase ends with a published, independently installable Gesso release on its own `gesso-v*` tag, proven on a clean machine, whose release notes list the parity catalog features the phase completed, so progress is shipped rather than accumulated; `gesso-v1.0.0` at the end of Phase 27 declares the catalog complete (every `plan` row stamped, every other row carrying its recorded status).
- **Current-state facts to verify (with claim candidates):**
  - Gesso's only planned release so far is 0.1.0 (`D03 T06 §3`), and no `gesso-v*` tag exists yet. `<!-- claim: exists todo/03-gesso/TODO-06-gesso-release.md -->`
  - The release standard the sections follow is `standards/release.md`. `<!-- claim: exists standards/release.md -->`
  - The Gesso installer script exists and registers the `.psd` association the parity formats extend. `<!-- claim: count "\.psd" installer/Gesso.iss = 7 -->`
- **Inputs and XREFs:** `standards/release.md`; `docs/parity/gesso-parity.md` (the catalog each release reconciles); -> XREF: D03 T06 §3 (the 0.1.0 release procedure every section repeats); -> XREF: D05 T01 §1 (the clean-machine procedure); -> XREF: D00 T01 §7 (`query parity --catalog gesso`, quoted by each release); -> XREF: D06 T01 §2 (the Gesso user guide each release extends).
- **Adjacency:** list=not-applicable (releases are listed by GitHub Releases); document=applicable (release notes and user-guide pages); settings=not-applicable (no settings of its own); reporting=applicable @ D00 T01 §7 (the per-phase parity report each release quotes); notifications=not-applicable (no runtime surface); permissions=not-applicable (no files written by the app); audit=applicable (the tag, the release notes, and the stamped rows are the audit trail); exchange=not-applicable (no formats of its own); reverse=applicable (a failed clean-machine install blocks the tag; the previous release stays current)

Every section below has the same shape; only the phase, the version, and the dependency list differ.

- **Depends On:** the previous release section (`§1` depends on `D03 T06 §3`) plus every other row of its phase, in the phase order of "Phase layout and renumbering".
- **Surface:** no surface of its own (the release artifacts are the installer, the notes, and the tag)
- **Runs:** `Needs: Clean Windows machine (no .NET SDK)` and `Requires: display-session -- launching the installed app on the clean machine needs an interactive desktop`
- **Catalog:** owns no catalog rows (it reconciles them)
- **Hints:**
  - Run `python scripts/todo-graph.py query parity --catalog gesso --phase <N>` and quote it: every catalog row planned to a section of the phase is owned by a stamped section; a row that cannot ship is moved to the backlog through `add-todo` with the catalog updated in the same commit, never left planned and unshipped.
  - Run `pwsh scripts/check-all.ps1` at the release commit and quote the gate table; every gate `PASS`.
  - Write the `gesso-v<version>` section of `CHANGELOG.md` listing the phase's user-visible features by catalog area, and add or update the user-guide pages under `docs/user/` for every new surface.
  - Package locally and run the clean-machine procedure from `D05 T01 §1` (install per-user and all-users, open each fixture format the phase added, save, uninstall; file associations opt-in), plus one driven action per new surface with captures under `docs/captures/gesso/release-<version>/`.
  - Confirm no Gesso menu item is disabled without naming a planned section or a backlog id, as `D03 T06 §2` established.
  - Push `gesso-v<version>`; verify the workflow, the assets, and `SHA256SUMS`; run the portable ZIP from an empty folder; update `README.md`'s Gesso status line; no other app's version moves.
  - Commit: `"release: Gesso <version>"`.
- **Proof:** driven run with evidence: the clean-machine install log, the smoke captures, the quoted `query parity` output with zero unshipped planned rows for the phase, and `gh release view gesso-v<version> --json isPrerelease,assets` showing a non-prerelease with its assets; cheaper substitute that fails: tagging from a developer machine, which the clean-machine log requirement refuses.

| Section | Title | Phase | Version |
| ------- | ----- | ---: | ------- |
| §1 | Gesso 0.2.0 (Phase 16) | 16 | `gesso-v0.2.0` |
| §2 | Gesso 0.3.0 (Phase 17) | 17 | `gesso-v0.3.0` |
| §3 | Gesso 0.4.0 (Phase 18) | 18 | `gesso-v0.4.0` |
| §4 | Gesso 0.5.0 (Phase 19) | 19 | `gesso-v0.5.0` |
| §5 | Gesso 0.6.0 (Phase 20) | 20 | `gesso-v0.6.0` |
| §6 | Gesso 0.7.0 (Phase 21) | 21 | `gesso-v0.7.0` |
| §7 | Gesso 0.8.0 (Phase 22) | 22 | `gesso-v0.8.0` |
| §8 | Gesso 0.9.0 (Phase 23) | 23 | `gesso-v0.9.0` |
| §9 | Gesso 0.10.0 (Phase 24) | 24 | `gesso-v0.10.0` |
| §10 | Gesso 0.11.0 (Phase 25) | 25 | `gesso-v0.11.0` |
| §11 | Gesso 0.12.0 (Phase 26) | 26 | `gesso-v0.12.0` |
| §12 | Gesso 1.0.0 (Phase 27): the parity catalog complete | 27 | `gesso-v1.0.0` |

§12 adds three items: `query parity --catalog gesso` over every phase reports zero `plan` rows owned by an unstamped section; the README and the Gesso user guide state parity with Photoshop 27.10, Affinity 3.3, and GIMP 3.2.6 with the catalog link; and the accessibility audit `D03 T07 §16` is among its dependencies, so 1.0.0 never ships an unaudited surface.
