# Nodus Parity Catalog

Every Adobe Illustrator 30.8 and CorelDRAW Graphics Suite 2026 (v27.2) feature, merged into Nodus features, each with exactly one status. The sources are [`sources/illustrator-30.8.md`](sources/illustrator-30.8.md) and [`sources/coreldraw-2026.md`](sources/coreldraw-2026.md); the status grammar and the update rules are in [`README.md`](README.md); the sections that own `plan` rows are designed in [`section-design.md`](section-design.md).

**Totals (2026-09-26):** 2,802 features covering 1,294 Illustrator rows and 3,041 CorelDRAW rows (4,335 in all); every source id appears in exactly one row.

| Status | Features | Source rows |
| ------ | -------: | ----------: |
| `plan` | 2,643 | 3,943 |
| `shipped-scope` | 69 | 150 |
| `backlog` | 37 | 55 |
| `excluded` | 35 | 169 |
| `other-app` | 18 | 18 |
| **Total** | **2,802** | **4,335** |

## Areas

- [Documents, pages, and artboards](#documents-pages-and-artboards) (95)
- [Layers and objects](#layers-and-objects) (53)
- [Selection](#selection) (39)
- [View and navigation](#view-and-navigation) (50)
- [Rulers, guides, grids, and snapping](#rulers-guides-grids-and-snapping) (74)
- [Edit, history, and clipboard](#edit-history-and-clipboard) (19)
- [Drawing tools](#drawing-tools) (57)
- [Shapes](#shapes) (56)
- [Path editing](#path-editing) (97)
- [Shaping and compound paths](#shaping-and-compound-paths) (42)
- [Transform, align, and arrange](#transform-align-and-arrange) (66)
- [Dimensions and connectors](#dimensions-and-connectors) (28)
- [Color](#color) (36)
- [Swatches, palettes, and color styles](#swatches-palettes-and-color-styles) (99)
- [Gradients, mesh, patterns, and fills](#gradients-mesh-patterns-and-fills) (80)
- [Strokes and outlines](#strokes-and-outlines) (28)
- [Brushes](#brushes) (70)
- [Transparency and blending](#transparency-and-blending) (48)
- [Appearance and styles](#appearance-and-styles) (44)
- [Symbols](#symbols) (47)
- [Type](#type) (190)
- [Fonts and writing tools](#fonts-and-writing-tools) (58)
- [Tables and graphs](#tables-and-graphs) (55)
- [Blend, contour, envelope, and distort](#blend-contour-envelope-and-distort) (98)
- [3D, shadows, glows, and bevels](#3d-shadows-glows-and-bevels) (82)
- [Lenses, PowerClip, perspective, symmetry, and repeats](#lenses-powerclip-perspective-symmetry-and-repeats) (115)
- [Bitmaps and placed images](#bitmaps-and-placed-images) (97)
- [Raster effects and adjustments](#raster-effects-and-adjustments) (204)
- [Tracing](#tracing) (48)
- [Color management](#color-management) (41)
- [Print and prepress](#print-and-prepress) (108)
- [PDF output](#pdf-output) (38)
- [Import and export formats](#import-and-export-formats) (144)
- [Export for screens and web](#export-for-screens-and-web) (71)
- [AI](#ai) (59)
- [Workspace and UI](#workspace-and-ui) (121)
- [Preferences](#preferences) (61)
- [Utilities](#utilities) (32)
- [Automation](#automation) (11)
- [Cloud and collaboration](#cloud-and-collaboration) (23)
- [Companion apps](#companion-apps) (18)

## Documents, pages, and artboards

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0001 | Expand live objects to plain paths, with expand options | AI-0212, AI-0213 | -- | core | plan D02 T07 §1 | the generic Expand command every live feature registers with; gradient-to-mesh expansion waits for D02 T09 §9 |
| NP-0002 | Identify objects by object name or XML ID | AI-1158 | -- | automation | plan D02 T07 §1 | governs how SVG id attributes are written from names; no variables panel |
| NP-0003 | Artboard tool | AI-0129 | -- | core | plan D02 T07 §3 |  |
| NP-0004 | Artboards and Pages panel | AI-0841 | CD-2338, CD-2375 | core | plan D02 T07 §3 | CD-2338 and CD-2375 moved from D02 T07 §4: the panel is built in D02 T07 §3 |
| NP-0005 | New and duplicate artboard | AI-0842 | -- | core | plan D02 T07 §3 |  |
| NP-0006 | Add or duplicate buttons on artboard edges | AI-0843 | -- | core | plan D02 T07 §3 |  |
| NP-0007 | Artboard Options dialog | AI-0844 | -- | core | plan D02 T07 §3 |  |
| NP-0008 | Fit artboard to artwork bounds or selected art | AI-0845 | -- | core | plan D02 T07 §3 |  |
| NP-0009 | Scale artwork with the artboard | AI-0846 | -- | core | plan D02 T07 §3 |  |
| NP-0010 | Convert rectangles to artboards | AI-0847 | -- | core | plan D02 T07 §3 |  |
| NP-0011 | Rearrange all or selected artboards | AI-0848, AI-0849 | -- | core | plan D02 T07 §3 |  |
| NP-0012 | Reorder artboards and pages | AI-0850 | CD-2357 | core | plan D02 T07 §3 |  |
| NP-0013 | Rename one or many artboards | AI-0851 | -- | core | plan D02 T07 §3 |  |
| NP-0014 | Delete artboards and delete empty artboards | AI-0852 | -- | core | plan D02 T07 §3 |  |
| NP-0015 | Move or copy artwork with the artboard | AI-0853 | -- | core | plan D02 T07 §3 |  |
| NP-0016 | Cut, copy, and paste artboards with contents | AI-0854 | -- | core | plan D02 T07 §3 |  |
| NP-0017 | Repeat the last artboard action | AI-0855 | -- | core | plan D02 T07 §3 |  |
| NP-0018 | Artboard context menu | AI-0856 | -- | core | plan D02 T07 §3 |  |
| NP-0019 | Lock artboard content | AI-0857 | -- | core | plan D02 T07 §3 |  |
| NP-0020 | Artboard background color | AI-0858 | -- | core | plan D02 T07 §3 |  |
| NP-0021 | On-canvas artboard labels with inline rename | AI-0859 | -- | core | plan D02 T07 §3 |  |
| NP-0022 | Active artboard or page highlight | AI-0860 | CD-2351 | core | plan D02 T07 §3 |  |
| NP-0023 | Paste onto selected artboards | AI-0862 | -- | core | plan D02 T07 §3 | extends Paste on All Artboards from D02 T07 §13 |
| NP-0024 | Video safe areas and pixel aspect ratio on artboards | AI-0864 | -- | core | plan D02 T07 §3 |  |
| NP-0025 | Select artboards and pages by click, Shift, or marquee | AI-0866 | CD-2350 | core | plan D02 T07 §3 |  |
| NP-0026 | Page size: presets and custom width and height | -- | CD-2299, CD-2300, CD-2302 | core | plan D02 T07 §3 |  |
| NP-0027 | Get page size from the printer | -- | CD-2301 | print | plan D02 T07 §3 | reads the default printer through System.Printing; the print dialog is D02 T13 §2 |
| NP-0028 | Page orientation and switch orientation | -- | CD-2303, CD-2309 | core | plan D02 T07 §3 |  |
| NP-0029 | Apply a size to the current page or all pages | -- | CD-2304, CD-2353 | core | plan D02 T07 §3 |  |
| NP-0030 | Save and delete custom page size presets | -- | CD-2310 | core | plan D02 T07 §3 |  |
| NP-0031 | Page dimensions on the property bar | -- | CD-2352 | core | plan D02 T07 §3 |  |
| NP-0032 | Document navigator: page tabs and first, previous, next, last | AI-0863 | CD-176, CD-2298 | core | plan D02 T07 §4 |  |
| NP-0033 | Show spreads in page thumbnails | -- | CD-2292 | core | plan D02 T07 §4 |  |
| NP-0034 | Resize pages interactively in multipage view | -- | CD-2293, CD-2354 | core | plan D02 T07 §4 |  |
| NP-0035 | Autofit page to content with a margin | -- | CD-2294, CD-2355 | core | plan D02 T07 §4 |  |
| NP-0036 | Page border display | -- | CD-2295, CD-2305 | core | plan D02 T07 §4 |  |
| NP-0037 | Bleed area display and amount | -- | CD-2296, CD-2308, CD-2369 | print | plan D02 T07 §4 | the bleed value is shared with printer's marks in D02 T13 §4 |
| NP-0038 | Printable area display | -- | CD-2297 | print | plan D02 T07 §4 |  |
| NP-0039 | Add a page frame | -- | CD-2306 | core | plan D02 T07 §4 |  |
| NP-0040 | Page background: none or solid color | -- | CD-2322, CD-2323, CD-2328 | core | plan D02 T07 §4 |  |
| NP-0041 | Bitmap page background: linked or embedded, default or custom size | -- | CD-2324, CD-2325, CD-2327 | core | plan D02 T07 §4 |  |
| NP-0042 | Print and export the page background | -- | CD-2326 | core | plan D02 T07 §4 |  |
| NP-0043 | Multipage view | -- | CD-2329 | core | plan D02 T07 §4 |  |
| NP-0044 | Single page view | -- | CD-2330 | core | plan D02 T07 §4 |  |
| NP-0045 | Default page view mode | -- | CD-2331 | core | plan D02 T07 §4 |  |
| NP-0046 | Multipage layout: grid, vertical, horizontal, and spacing | -- | CD-2332, CD-2333, CD-2334, CD-2336 | core | plan D02 T07 §4 |  |
| NP-0047 | Free-form page placement | -- | CD-2335, CD-2356 | core | plan D02 T07 §4 |  |
| NP-0048 | Zoom to selected pages | -- | CD-2337 | core | plan D02 T07 §4 |  |
| NP-0049 | Page thumbnails as list or grid with a size slider | -- | CD-2339, CD-2340 | core | plan D02 T07 §4 |  |
| NP-0050 | Facing pages and start side | -- | CD-2341, CD-2342 | core | plan D02 T07 §4 |  |
| NP-0051 | Insert pages before or after, with size and orientation | -- | CD-2343, CD-2344, CD-2345 | core | plan D02 T07 §4 |  |
| NP-0052 | Duplicate page with layers or contents | -- | CD-2346 | core | plan D02 T07 §4 |  |
| NP-0053 | Duplicate a page to a new document | -- | CD-2347 | core | plan D02 T07 §4 |  |
| NP-0054 | Delete one, a range, or selected pages | -- | CD-2348, CD-2349 | core | plan D02 T07 §4 |  |
| NP-0055 | Rename page | -- | CD-2358 | core | plan D02 T07 §4 |  |
| NP-0056 | Find a page by name | -- | CD-2359 | core | plan D02 T07 §4 |  |
| NP-0057 | Go to page | -- | CD-2360 | core | plan D02 T07 §4 |  |
| NP-0058 | Insert page number on the active layer, all, odd, or even pages | -- | CD-2362, CD-2363, CD-2364, CD-2365, CD-2370, CD-2371, CD-2372, CD-2373 | core | plan D02 T07 §4 |  |
| NP-0059 | Page number field | -- | CD-2366 | core | plan D02 T07 §4 |  |
| NP-0060 | Hide the page number on one page | -- | CD-2367 | core | plan D02 T07 §4 |  |
| NP-0061 | Page number settings | -- | CD-2368 | core | plan D02 T07 §4 |  |
| NP-0062 | The New Document dialog | AI-0957 | CD-213, CD-305 | core | plan D02 T07 §14 |  |
| NP-0063 | Document settings: name, page count, units, size, and orientation | AI-0958 | CD-214, CD-215, CD-217, CD-218, CD-219 | core | plan D02 T07 §14 |  |
| NP-0064 | Save and delete custom document presets | AI-0959 | CD-226 | core | plan D02 T07 §14 |  |
| NP-0065 | Blank templates | AI-0960 | -- | core | plan D02 T07 §14 |  |
| NP-0066 | New document without the dialog | AI-0963 | CD-227 | core | plan D02 T07 §14 |  |
| NP-0067 | New from template | AI-0964 | CD-279, CD-282 | core | plan D02 T07 §14 |  |
| NP-0068 | Save as template with template properties | AI-0965 | CD-299, CD-300 | core | plan D02 T07 §14 | Nodus templates are .svgt: SVG with nodus:template metadata |
| NP-0069 | Close and close all | AI-0968 | CD-133, CD-258 | core | plan D02 T07 §14 | CD-133 moved from D02 T07 §12: Window Close All closes documents |
| NP-0070 | Save a copy and save as another format | AI-0969 | CD-302 | core | plan D02 T07 §14 | Save and Save As themselves ship in D02 T04 §1 |
| NP-0071 | Revert to saved | AI-0971 | CD-240 | core | plan D02 T07 §14 |  |
| NP-0072 | Document Setup and document options | AI-0973 | CD-2897, CD-2909 | core | plan D02 T07 §14 |  |
| NP-0073 | Document Setup type options | AI-0974 | -- | core | plan D02 T07 §14 | stored here; consumed by the text engine in D02 T10 §2 |
| NP-0074 | Document information: title, subject, keywords, rating, notes, tags | AI-0976 | CD-256, CD-304 | core | plan D02 T07 §14 | written as SVG metadata with RDF and XMP |
| NP-0075 | Primary color mode | -- | CD-216 | core | plan D02 T07 §14 | the document records RGB or CMYK; the color model is D02 T09 §1 |
| NP-0076 | Rendering resolution | -- | CD-220, CD-2307 | core | plan D02 T07 §14 |  |
| NP-0077 | Document presets: print, web, devices, social, paper types | -- | CD-221, CD-225 | core | plan D02 T07 §14 |  |
| NP-0078 | Page view mode at creation | -- | CD-222 | core | plan D02 T07 §14 |  |
| NP-0079 | Bleed at creation | -- | CD-223 | core | plan D02 T07 §14 |  |
| NP-0080 | Document color profiles and rendering intent at creation | -- | CD-224 | core | plan D02 T07 §14 | profiles are stored by name until D02 T13 §1 applies them |
| NP-0081 | Save selected only | -- | CD-243, CD-303 | core | plan D02 T07 §14 |  |
| NP-0082 | Locked and read-only file handling on save | -- | CD-254 | core | plan D02 T07 §14 |  |
| NP-0083 | Template folders: sources, aliases, recursive browse, and reindex | -- | CD-281, CD-288, CD-289, CD-290, CD-292, CD-295 | core | plan D02 T07 §14 | local folders only; no content packs |
| NP-0084 | Open a template as a new document, with or without contents | -- | CD-283 | core | plan D02 T07 §14 |  |
| NP-0085 | Import styles from a template | -- | CD-284 | core | plan D02 T07 §14 | the style import itself is D02 T09 §15 |
| NP-0086 | Template browser search, filter, and sort | -- | CD-285, CD-286, CD-287 | core | plan D02 T07 §14 |  |
| NP-0087 | Template browser thumbnails and details pane | -- | CD-293, CD-294 | core | plan D02 T07 §14 |  |
| NP-0088 | Template favorites, properties, and delete | -- | CD-296, CD-297, CD-298 | core | plan D02 T07 §14 |  |
| NP-0089 | Open a template for editing | -- | CD-301 | core | plan D02 T07 §14 |  |
| NP-0090 | Exit application | AI-0990 | CD-013 | core | shipped-scope D02 T04 §1 |  |
| NP-0091 | Save and Save As | -- | CD-241, CD-242 | core | shipped-scope D02 T04 §1 |  |
| NP-0092 | Unsaved changes marker | -- | CD-253 | core | shipped-scope D02 T04 §1 |  |
| NP-0093 | Close document | -- | CD-257 | core | shipped-scope D02 T04 §1 |  |
| NP-0094 | Open recent and clear recent list | AI-0966 | CD-232, CD-306 | core | shipped-scope D02 T04 §5 |  |
| NP-0095 | Auto backup and crash recovery | AI-0988, AI-0989 | CD-255 | core | shipped-scope D02 T04 §5 |  |

## Layers and objects

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0096 | Lock selection | AI-0064 | CD-489 | core | plan D02 T07 §5 |  |
| NP-0097 | Lock all artwork above | AI-0065 | -- | core | plan D02 T07 §5 |  |
| NP-0098 | Lock other layers | AI-0066 | -- | core | plan D02 T07 §5 |  |
| NP-0099 | Unlock and unlock all | AI-0067 | CD-490, CD-555, CD-556 | core | plan D02 T07 §5 |  |
| NP-0100 | Hide selection | AI-0068 | CD-499 | core | plan D02 T07 §5 |  |
| NP-0101 | Hide all artwork above | AI-0069 | -- | core | plan D02 T07 §5 |  |
| NP-0102 | Hide other layers | AI-0070 | -- | core | plan D02 T07 §5 |  |
| NP-0103 | Show and show all | AI-0071 | CD-500, CD-557 | core | plan D02 T07 §5 |  |
| NP-0104 | Lock all deselected artwork | AI-0072 | -- | core | plan D02 T07 §5 |  |
| NP-0105 | Hide unselected artwork | AI-0073 | -- | core | plan D02 T07 §5 |  |
| NP-0106 | Layer color and selection color from the layer | AI-0076 | CD-518 | core | plan D02 T07 §5 |  |
| NP-0107 | New layer and new sublayer | AI-0823 | CD-502 | core | plan D02 T07 §5 |  |
| NP-0108 | Layer Options dialog | AI-0824 | -- | core | plan D02 T07 §5 |  |
| NP-0109 | Per-layer outline or wireframe view | AI-0825 | CD-517 | core | plan D02 T07 §5 |  |
| NP-0110 | Template layers | AI-0827 | -- | core | plan D02 T07 §5 |  |
| NP-0111 | Printable and exportable layer toggles | AI-0828 | CD-521 | print | plan D02 T07 §5 |  |
| NP-0112 | Move or copy objects to another layer | AI-0829 | CD-528 | core | plan D02 T07 §5 |  |
| NP-0113 | Duplicate and delete layer | AI-0830 | CD-510 | core | plan D02 T07 §5 |  |
| NP-0114 | Merge selected layers and flatten artwork | AI-0831 | -- | core | plan D02 T07 §5 |  |
| NP-0115 | Collect in new layer | AI-0832 | -- | core | plan D02 T07 §5 |  |
| NP-0116 | Release to layers: sequence or build | AI-0833 | -- | core | plan D02 T07 §5 |  |
| NP-0117 | Reverse layer order | AI-0834 | -- | core | plan D02 T07 §5 |  |
| NP-0118 | Hide, outline, or lock others from the panel menu | AI-0835 | -- | core | plan D02 T07 §5 |  |
| NP-0119 | Locate object and expand to show selection | AI-0836 | CD-514 | core | plan D02 T07 §5 |  |
| NP-0120 | Find and filter in the Objects panel | AI-0837 | CD-525 | core | plan D02 T07 §5 |  |
| NP-0121 | Objects panel options and thumbnail size | AI-0838 | CD-519 | core | plan D02 T07 §5 |  |
| NP-0122 | Group by drag in the Objects panel | -- | CD-486 | core | plan D02 T07 §5 |  |
| NP-0123 | The Objects panel: pages, layers, and objects tree | -- | CD-501, CD-575, CD-577 | core | plan D02 T07 §5 |  |
| NP-0124 | Master layers for all, odd, or even pages | -- | CD-503, CD-504, CD-505 | core | plan D02 T07 §5 |  |
| NP-0125 | Change a layer to master or local | -- | CD-506 | core | plan D02 T07 §5 |  |
| NP-0126 | Default layers | -- | CD-507 | core | plan D02 T07 §5 |  |
| NP-0127 | Active layer | -- | CD-508 | core | plan D02 T07 §5 |  |
| NP-0128 | Select object to activate its layer | -- | CD-509 | core | plan D02 T07 §5 |  |
| NP-0129 | Delete empty layers | -- | CD-511 | core | plan D02 T07 §5 |  |
| NP-0130 | Objects panel views: layers and objects, or pages, layers, and objects | -- | CD-512, CD-513 | core | plan D02 T07 §5 |  |
| NP-0131 | Show master layers on pages | -- | CD-515 | core | plan D02 T07 §5 |  |
| NP-0132 | Fully expand the tree | -- | CD-516 | core | plan D02 T07 §5 |  |
| NP-0133 | Edit across layers | -- | CD-523 | core | plan D02 T07 §5 |  |
| NP-0134 | Copy and paste a layer | -- | CD-527 | core | plan D02 T07 §5 |  |
| NP-0135 | Keep desktop objects on their layer | -- | CD-529 | core | plan D02 T07 §5 |  |
| NP-0136 | Isolation mode: enter and exit | AI-0017, AI-0018 | CD-309, CD-425, CD-429, CD-543 | core | plan D02 T07 §7 |  |
| NP-0137 | Dimming of objects outside the isolated group | -- | CD-310, CD-2870 | core | plan D02 T07 §7 |  |
| NP-0138 | Isolation breadcrumb bar | -- | CD-311, CD-427 | core | plan D02 T07 §7 |  |
| NP-0139 | Isolated group in the Objects panel | -- | CD-426 | core | plan D02 T07 §7 |  |
| NP-0140 | Step out one isolation level | -- | CD-428 | core | plan D02 T07 §7 |  |
| NP-0141 | New objects join the isolated group | -- | CD-430 | core | plan D02 T07 §7 |  |
| NP-0142 | Which objects can be isolated, including text on a path | -- | CD-431, CD-1018 | core | plan D02 T07 §7 |  |
| NP-0143 | Double-click to enter isolation mode | -- | CD-2871 | core | plan D02 T07 §7 |  |
| NP-0144 | Layers panel | AI-0822 | -- | core | shipped-scope D02 T02 §6 |  |
| NP-0145 | Lock layers and objects | AI-0826 | CD-522 | core | shipped-scope D02 T02 §6 |  |
| NP-0146 | Rename layers and objects | AI-0839 | CD-524 | core | shipped-scope D02 T02 §6 |  |
| NP-0147 | Show or hide layer | -- | CD-520 | core | shipped-scope D02 T02 §6 |  |
| NP-0148 | Reorder layers by dragging | -- | CD-526 | core | shipped-scope D02 T02 §6 |  |

## Selection

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0149 | Group selection tool | AI-0003 | -- | core | plan D02 T07 §6 |  |
| NP-0150 | Magic wand tool and selecting by color | AI-0004, AI-0484 | -- | core | plan D02 T07 §6 |  |
| NP-0151 | Magic wand options: fill, stroke, weight, opacity, blend mode, and all layers | AI-0005, AI-0006, AI-0007, AI-0008, AI-0009, AI-0010 | -- | core | plan D02 T07 §6 |  |
| NP-0152 | Lasso and freehand pick tools | AI-0011 | CD-315 | core | plan D02 T07 §6 |  |
| NP-0153 | Marquee enclosure modes: completely inside or touching | AI-0013 | CD-324 | core | plan D02 T07 §6 |  |
| NP-0154 | Select behind or hidden objects | AI-0015 | CD-328 | core | plan D02 T07 §6 |  |
| NP-0155 | Skip shadows and effect bounds when selecting | AI-0016 | -- | core | plan D02 T07 §6 |  |
| NP-0156 | Select all on the active artboard | AI-0020 | -- | core | plan D02 T07 §6 |  |
| NP-0157 | Deselect | AI-0021 | -- | core | plan D02 T07 §6 |  |
| NP-0158 | Reselect | AI-0022 | -- | core | plan D02 T07 §6 |  |
| NP-0159 | Inverse selection | AI-0023 | -- | core | plan D02 T07 §6 |  |
| NP-0160 | Next object above or below | AI-0024, AI-0025 | -- | core | plan D02 T07 §6 |  |
| NP-0161 | Select Same appearance, appearance attribute, and graphic style | AI-0026, AI-0027, AI-0034 | -- | core | plan D02 T07 §6 |  |
| NP-0162 | Select Same fill, stroke, stroke weight, opacity, and blend mode | AI-0028, AI-0029, AI-0030, AI-0031, AI-0032, AI-0033 | -- | core | plan D02 T07 §6 |  |
| NP-0163 | Select Same shape | AI-0035 | -- | core | plan D02 T07 §6 |  |
| NP-0164 | Select Same symbol instance | AI-0036 | -- | core | plan D02 T07 §6 |  |
| NP-0165 | Select Same link block series | AI-0037 | -- | core | plan D02 T07 §6 |  |
| NP-0166 | Select Same text attributes: font family, style, size, fill, and stroke | AI-0038, AI-0039, AI-0040, AI-0041, AI-0042, AI-0043, AI-0044 | -- | core | plan D02 T07 §6 |  |
| NP-0167 | Select all on the same layers | AI-0045 | -- | core | plan D02 T07 §6 |  |
| NP-0168 | Select direction handles | AI-0046 | -- | core | plan D02 T07 §6 |  |
| NP-0169 | Select brush strokes | AI-0047, AI-0048 | -- | core | plan D02 T07 §6 |  |
| NP-0170 | Select clipping masks | AI-0049 | -- | core | plan D02 T07 §6 |  |
| NP-0171 | Select stray points | AI-0050 | -- | core | plan D02 T07 §6 |  |
| NP-0172 | Select text objects: all, point, or area | AI-0051, AI-0052, AI-0053 | CD-403 | core | plan D02 T07 §6 |  |
| NP-0173 | Select objects not aligned to the pixel grid | AI-0054 | -- | core | plan D02 T07 §6 |  |
| NP-0174 | Global edit of similar objects | AI-0055, AI-0056 | -- | core | plan D02 T07 §6 |  |
| NP-0175 | Save and edit named selections | AI-0057, AI-0058 | -- | core | plan D02 T07 §6 |  |
| NP-0176 | Switch to the last-used selection tool | AI-0059 | -- | core | plan D02 T07 §6 |  |
| NP-0177 | Temporary selection tool | AI-0060 | CD-188 | core | plan D02 T07 §6 |  |
| NP-0178 | Select objects from the Objects panel target | AI-0061 | -- | core | plan D02 T07 §6 |  |
| NP-0179 | Show or hide the bounding box | AI-0074 | -- | core | plan D02 T07 §6 |  |
| NP-0180 | Reset bounding box | AI-0075 | -- | core | plan D02 T07 §6 |  |
| NP-0181 | Tab and Shift+Tab object cycling | -- | CD-189, CD-325 | core | plan D02 T07 §6 |  |
| NP-0182 | Select an object inside a group | -- | CD-327 | core | plan D02 T07 §6 |  |
| NP-0183 | Selection groups 0 to 9 | -- | CD-329, CD-330, CD-331 | core | plan D02 T07 §6 |  |
| NP-0184 | Selection (pick) tool | AI-0001 | CD-314, CD-322 | core | shipped-scope D02 T02 §3 |  |
| NP-0185 | Marquee selection | AI-0012 | CD-323 | core | shipped-scope D02 T02 §3 |  |
| NP-0186 | Shift-click add, subtract, and click-away deselect | AI-0014 | CD-332 | core | shipped-scope D02 T02 §3 |  |
| NP-0187 | Move by dragging | -- | CD-369 | core | shipped-scope D02 T02 §3 |  |

## View and navigation

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0188 | Large canvas and up to 1,000 artboards | AI-0865, AI-0962 | -- | core | plan D02 T07 §2 | AI-0865 moved from D02 T07 §3: the scale budget is the spatial index's job |
| NP-0189 | GPU or CPU rendering with a preview toggle | AI-0908 | CD-200 | core | plan D02 T07 §2 | Skia GPU (GRContext) with CPU fallback; no OpenCL |
| NP-0190 | Anti-aliased artwork display | AI-0928 | -- | core | plan D02 T07 §2 |  |
| NP-0191 | Live preview while dragging and editing | AI-0930 | -- | core | plan D02 T07 §2 |  |
| NP-0192 | Smooth pan and zoom on large documents | -- | CD-015 | core | plan D02 T07 §2 |  |
| NP-0193 | Refresh window | -- | CD-131 | core | plan D02 T07 §2 |  |
| NP-0194 | Interactive bitmap transform previews | -- | CD-184 | core | plan D02 T07 §2 |  |
| NP-0195 | Keep editing during background save, print, and export | -- | CD-196 | core | plan D02 T07 §2 | save snapshots the document model and writes on a worker |
| NP-0196 | Low-resolution preview while panning and zooming | -- | CD-2833 | core | plan D02 T07 §2 |  |
| NP-0197 | Hand tool, Space pan, and middle-button quick pan | AI-0898 | CD-031, CD-032, CD-185 | core | plan D02 T07 §12 |  |
| NP-0198 | Rotate view tool and rotate view commands | AI-0899, AI-0906 | -- | core | plan D02 T07 §12 |  |
| NP-0199 | Zoom tool | AI-0901 | CD-022 | core | plan D02 T07 §12 |  |
| NP-0200 | Zoom in and zoom out | AI-0902 | CD-023, CD-122, CD-123 | core | plan D02 T07 §12 |  |
| NP-0201 | Fit artboard, fit page, all pages, and all objects in window | AI-0903 | CD-025, CD-026, CD-027, CD-125, CD-126 | core | plan D02 T07 §12 |  |
| NP-0202 | Actual size | AI-0904 | CD-129 | core | plan D02 T07 §12 |  |
| NP-0203 | Zoom to selection | AI-0905 | CD-024, CD-124 | core | plan D02 T07 §12 |  |
| NP-0204 | Outline and wireframe view | AI-0907 | CD-038, CD-115 | core | plan D02 T07 §12 |  |
| NP-0205 | Trim view | AI-0911 | -- | core | plan D02 T07 §12 |  |
| NP-0206 | Presentation mode | AI-0912 | -- | core | plan D02 T07 §12 |  |
| NP-0207 | Screen modes | AI-0913 | -- | core | plan D02 T07 §12 |  |
| NP-0208 | Hide and show edges | AI-0916 | -- | core | plan D02 T07 §12 |  |
| NP-0209 | Hide and show artboards | AI-0917 | -- | core | plan D02 T07 §12 |  |
| NP-0210 | Show and hide template layers | AI-0919 | -- | core | plan D02 T07 §12 |  |
| NP-0211 | Show and hide the gradient annotator | AI-0921 | -- | core | plan D02 T07 §12 | the annotator itself is D02 T09 §8 |
| NP-0212 | Show and hide the corner widget | AI-0922 | -- | core | plan D02 T07 §12 | the widget itself is D02 T08 §4 |
| NP-0213 | Saved views: new view, edit views, Views panel | AI-0923 | CD-045, CD-160 | core | plan D02 T07 §12 |  |
| NP-0214 | New window on the same document | AI-0924 | CD-130 | core | plan D02 T07 §12 |  |
| NP-0215 | Animated zoom | AI-0929 | -- | core | plan D02 T07 §12 |  |
| NP-0216 | Undock a document window | -- | CD-017 | core | plan D02 T07 §12 |  |
| NP-0217 | Cascade, tile, and arrange windows | -- | CD-018, CD-019, CD-020, CD-134 | core | plan D02 T07 §12 |  |
| NP-0218 | Window list switching | -- | CD-021 | core | plan D02 T07 §12 |  |
| NP-0219 | Zoom to page width and page height | -- | CD-028, CD-029, CD-127, CD-128 | core | plan D02 T07 §12 |  |
| NP-0220 | Zoom levels list | -- | CD-030 | core | plan D02 T07 §12 |  |
| NP-0221 | Mouse wheel: zoom or scroll by default | -- | CD-034, CD-2831 | core | plan D02 T07 §12 |  |
| NP-0222 | Scroll bars | -- | CD-035 | core | plan D02 T07 §12 |  |
| NP-0223 | Full-screen preview and its mode | -- | CD-036, CD-2834 | core | plan D02 T07 §12 |  |
| NP-0224 | Preview selected only | -- | CD-037 | core | plan D02 T07 §12 |  |
| NP-0225 | Normal view | -- | CD-039, CD-117 | core | plan D02 T07 §12 |  |
| NP-0226 | Enhanced view | -- | CD-040, CD-118 | core | plan D02 T07 §12 |  |
| NP-0227 | Toggle the previous view mode | -- | CD-044 | core | plan D02 T07 §12 |  |
| NP-0228 | Simple wireframe view | -- | CD-114 | core | plan D02 T07 §12 |  |
| NP-0229 | Draft view | -- | CD-116 | core | plan D02 T07 §12 |  |
| NP-0230 | Close window | -- | CD-132 | core | plan D02 T07 §12 |  |
| NP-0231 | Tabbed documents toggle | -- | CD-135 | core | plan D02 T07 §12 |  |
| NP-0232 | Text zoom controls | -- | CD-183 | core | plan D02 T07 §12 |  |
| NP-0233 | Right-click action of the zoom and pan tools | -- | CD-2828 | core | plan D02 T07 §12 |  |
| NP-0234 | Zoom relative to 1:1 | -- | CD-2829 | core | plan D02 T07 §12 |  |
| NP-0235 | Center the mouse when zooming with the wheel | -- | CD-2830 | core | plan D02 T07 §12 |  |
| NP-0236 | Zoom rate and alternate zoom rate | -- | CD-2832 | core | plan D02 T07 §12 |  |
| NP-0237 | Default view mode | -- | CD-2835 | core | plan D02 T07 §12 |  |

## Rulers, guides, grids, and snapping

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0238 | Transparency grid | AI-0582 | -- | core | plan D02 T07 §9 |  |
| NP-0239 | Show and hide rulers | AI-0867 | CD-2414 | core | plan D02 T07 §9 |  |
| NP-0240 | Global or artboard rulers | AI-0868 | -- | core | plan D02 T07 §9 |  |
| NP-0241 | Ruler origin and ruler units | AI-0869 | CD-2415, CD-2416 | core | plan D02 T07 §9 |  |
| NP-0242 | Video rulers | AI-0870 | -- | core | plan D02 T07 §9 |  |
| NP-0243 | Show the document grid | AI-0875 | CD-2421 | core | plan D02 T07 §9 |  |
| NP-0244 | Grid settings: lines or dots, spacing, color, and subdivisions | AI-0877, AI-1159 | CD-2422, CD-2423 | core | plan D02 T07 §9 |  |
| NP-0245 | Units for general, stroke, and type | AI-1156 | -- | core | plan D02 T07 §9 |  |
| NP-0246 | Numbers without units are points | AI-1157 | -- | core | plan D02 T07 §9 |  |
| NP-0247 | Ruler tick divisions | -- | CD-2417 | core | plan D02 T07 §9 |  |
| NP-0248 | Rulers per desktop and tablet mode | -- | CD-2419, CD-2844 | core | plan D02 T07 §9 |  |
| NP-0249 | Calibrate rulers | -- | CD-2420 | core | plan D02 T07 §9 |  |
| NP-0250 | Pixel grid: color, opacity, and show at 800 percent | -- | CD-2424, CD-2425, CD-2445 | core | plan D02 T07 §9 |  |
| NP-0251 | Align the page with the pixel grid | -- | CD-2426 | core | plan D02 T07 §9 |  |
| NP-0252 | Baseline grid: spacing, start, and color | -- | CD-2427, CD-2428 | core | plan D02 T07 §9 |  |
| NP-0253 | Drawing scale | -- | CD-2444 | core | plan D02 T07 §9 |  |
| NP-0254 | Measure tool: distance and angle | AI-0290, AI-0896 | -- | core | plan D02 T07 §10 |  |
| NP-0255 | Measure area with exclusions | AI-0291 | -- | core | plan D02 T07 §10 |  |
| NP-0256 | Info panel area options | AI-0292 | -- | core | plan D02 T07 §10 |  |
| NP-0257 | Horizontal and vertical guides from the rulers | AI-0871 | CD-2431, CD-2432 | core | plan D02 T07 §10 |  |
| NP-0258 | Show, hide, lock, and clear guides | AI-0872 | CD-2429, CD-2442 | core | plan D02 T07 §10 |  |
| NP-0259 | Guide color and style | AI-0873 | CD-2443 | core | plan D02 T07 §10 |  |
| NP-0260 | Artboard-level and document-wide guides | AI-0874 | CD-2435 | core | plan D02 T07 §10 |  |
| NP-0261 | Info panel | AI-0897 | -- | core | plan D02 T07 §10 |  |
| NP-0262 | Select all guides | -- | CD-404, CD-2440 | core | plan D02 T07 §10 |  |
| NP-0263 | Guides panel: numeric add, move, rotate, and delete | -- | CD-2430, CD-2438, CD-2441, CD-2454 | core | plan D02 T07 §10 |  |
| NP-0264 | Angled guides | -- | CD-2433 | core | plan D02 T07 §10 |  |
| NP-0265 | Make and release guides from objects | -- | CD-2434 | core | plan D02 T07 §10 |  |
| NP-0266 | Guide presets: built-in and user-defined | -- | CD-2436, CD-2437 | core | plan D02 T07 §10 |  |
| NP-0267 | Show guides at the drawing scale | -- | CD-2439 | core | plan D02 T07 §10 |  |
| NP-0268 | Snap to pixel | AI-0878 | CD-2381, CD-2446 | core | plan D02 T07 §11 |  |
| NP-0269 | Snap to point and node | AI-0879 | CD-2388 | core | plan D02 T07 §11 |  |
| NP-0270 | Snapping quick access menu | AI-0881 | CD-2387 | core | plan D02 T07 §11 |  |
| NP-0271 | Smart guides toggle and preferences | AI-0882, AI-1160 | -- | core | plan D02 T07 §11 |  |
| NP-0272 | Smart guides: object and alignment guides | AI-0883 | -- | core | plan D02 T07 §11 |  |
| NP-0273 | Smart guides: glyph guides | AI-0884 | -- | core | plan D02 T07 §11 | glyph bounds come from the text engine in D02 T10 §5 |
| NP-0274 | Smart guides: anchor and path labels, object highlighting, measurement labels | AI-0885 | -- | core | plan D02 T07 §11 |  |
| NP-0275 | Smart guides for transform tools | AI-0886 | -- | core | plan D02 T07 §11 |  |
| NP-0276 | Equal spacing guides | AI-0887 | CD-2410 | core | plan D02 T07 §11 |  |
| NP-0277 | Distance guides and intelligent dimensioning | AI-0888 | CD-2411 | core | plan D02 T07 §11 |  |
| NP-0278 | Snap to last location | AI-0889 | -- | core | plan D02 T07 §11 |  |
| NP-0279 | Construction guide angles | AI-0890 | CD-2405 | core | plan D02 T07 §11 |  |
| NP-0280 | Snapping tolerance | AI-0891 | CD-2875 | core | plan D02 T07 §11 |  |
| NP-0281 | Snap to endpoint, midpoint, and center | AI-0892 | CD-2390, CD-2395 | core | plan D02 T07 §11 |  |
| NP-0282 | Snap only within the active artboard or isolated group | AI-0893 | -- | core | plan D02 T07 §11 |  |
| NP-0283 | Snap to tangent | AI-0894 | CD-2392 | core | plan D02 T07 §11 |  |
| NP-0284 | Snap to perpendicular | AI-0895 | CD-2393 | core | plan D02 T07 §11 |  |
| NP-0285 | Snap objects to themselves | -- | CD-2376, CD-2876 | core | plan D02 T07 §11 |  |
| NP-0286 | Turn all snapping off | -- | CD-2377, CD-2385 | core | plan D02 T07 §11 |  |
| NP-0287 | Automatic alignment toggle | -- | CD-2378 | core | plan D02 T07 §11 |  |
| NP-0288 | Snap to page | -- | CD-2380, CD-2451 | core | plan D02 T07 §11 |  |
| NP-0289 | Snap to baseline grid | -- | CD-2383, CD-2448 | core | plan D02 T07 §11 |  |
| NP-0290 | Hold Q to suspend snapping | -- | CD-2386 | core | plan D02 T07 §11 |  |
| NP-0291 | Snap to intersection | -- | CD-2389 | core | plan D02 T07 §11 |  |
| NP-0292 | Snap to quadrant | -- | CD-2391 | core | plan D02 T07 §11 |  |
| NP-0293 | Snap to edge | -- | CD-2394 | core | plan D02 T07 §11 |  |
| NP-0294 | Snap to text baseline | -- | CD-2396 | core | plan D02 T07 §11 |  |
| NP-0295 | Dynamic guides toggle | -- | CD-2397 | core | plan D02 T07 §11 |  |
| NP-0296 | Dynamic guide intersection placement | -- | CD-2398 | core | plan D02 T07 §11 |  |
| NP-0297 | Dynamic guide snap point queue | -- | CD-2399 | core | plan D02 T07 §11 |  |
| NP-0298 | Live Guides panel | -- | CD-2400, CD-2455 | core | plan D02 T07 §11 |  |
| NP-0299 | Live guide line style and color | -- | CD-2401, CD-2413 | core | plan D02 T07 §11 |  |
| NP-0300 | Snap mode and guide screen tips | -- | CD-2402, CD-2878 | core | plan D02 T07 §11 |  |
| NP-0301 | Extend dynamic guides along a segment | -- | CD-2403 | core | plan D02 T07 §11 |  |
| NP-0302 | Snap to dynamic guide tick spacing | -- | CD-2404 | core | plan D02 T07 §11 |  |
| NP-0303 | Alignment guides toggle | -- | CD-2406 | core | plan D02 T07 §11 |  |
| NP-0304 | Alignment guides to object edges and centers | -- | CD-2407, CD-2408 | core | plan D02 T07 §11 |  |
| NP-0305 | Alignment guides to objects inside a group | -- | CD-2409 | core | plan D02 T07 §11 |  |
| NP-0306 | Margin alignment guides | -- | CD-2412 | core | plan D02 T07 §11 |  |
| NP-0307 | Show snap location marks | -- | CD-2877 | core | plan D02 T07 §11 |  |
| NP-0308 | Snap to grid | AI-0876 | CD-2382, CD-2447 | core | shipped-scope D02 T02 §7 |  |
| NP-0309 | Snap to objects | -- | CD-2379, CD-2450 | core | shipped-scope D02 T02 §7 |  |
| NP-0310 | Snap to guidelines | -- | CD-2384 | core | shipped-scope D02 T02 §7 |  |
| NP-0311 | Snap to modify-guidelines | -- | CD-2449 | core | shipped-scope D02 T02 §7 |  |

## Edit, history, and clipboard

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0312 | Duplicate by Alt-drag | AI-0246 | -- | core | plan D02 T07 §13 |  |
| NP-0313 | Paste in front and paste in back | AI-0250, AI-0251 | -- | core | plan D02 T07 §13 |  |
| NP-0314 | Paste in place | AI-0252 | -- | core | plan D02 T07 §13 |  |
| NP-0315 | Paste on all artboards | AI-0253 | -- | core | plan D02 T07 §13 |  |
| NP-0316 | Paste without formatting | AI-0254 | -- | core | plan D02 T07 §13 |  |
| NP-0317 | Paste remembers layers | AI-0255 | -- | core | plan D02 T07 §13 |  |
| NP-0318 | History panel | AI-1101 | CD-161, CD-239 | core | plan D02 T07 §13 |  |
| NP-0319 | Nudge, micro nudge, and super nudge with their distances | -- | CD-187, CD-371, CD-372, CD-373, CD-2418, CD-2873 | core | plan D02 T07 §13 |  |
| NP-0320 | Right-drag menu: move, copy here, copy fill, outline, or all properties | -- | CD-191, CD-368, CD-599 | core | plan D02 T07 §13 |  |
| NP-0321 | Repeat the last command | -- | CD-238 | core | plan D02 T07 §13 |  |
| NP-0322 | Paste special | -- | CD-343 | core | plan D02 T07 §13 | offers the clipboard formats Nodus reads; OLE and foreign formats are D02 T14 §19 |
| NP-0323 | Drop a copy while dragging: Space or right-click | -- | CD-349, CD-351 | core | plan D02 T07 §13 |  |
| NP-0324 | Duplicate in place with numeric keypad plus | -- | CD-350 | core | plan D02 T07 §13 |  |
| NP-0325 | Move or reposition a shape while drawing | -- | CD-370, CD-593 | core | plan D02 T07 §13 |  |
| NP-0326 | Duplicate offset | -- | CD-2872 | core | plan D02 T07 §13 |  |
| NP-0327 | Undo and redo | AI-1100 | CD-236, CD-237 | core | shipped-scope D01 T02 §4 | multi-level undo stack already covered |
| NP-0328 | Select all | AI-0019 | CD-326, CD-402 | core | shipped-scope D02 T03 §3 |  |
| NP-0329 | Cut, copy, paste, and delete | AI-1102 | CD-340, CD-341, CD-342, CD-352 | core | shipped-scope D02 T03 §3 |  |
| NP-0330 | Duplicate with offset | -- | CD-344 | core | shipped-scope D02 T03 §3 |  |

## Drawing tools

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0331 | Pen tool: click for corners, drag for smooth anchors | AI-0077 | CD-585 | core | plan D02 T08 §1 |  |
| NP-0332 | Pen rubber-band preview of the next segment | AI-0078 | CD-605 | core | plan D02 T08 §1 |  |
| NP-0333 | Move the anchor being placed (Space-drag) | AI-0079 | -- | core | plan D02 T08 §1 |  |
| NP-0334 | Alt toggles the anchor point tool while drawing | AI-0080 | -- | core | plan D02 T08 §1 |  |
| NP-0335 | Pen auto add and delete anchors on hover | AI-0081 | CD-606 | core | plan D02 T08 §1 |  |
| NP-0336 | Continue or connect open paths from the pen | AI-0082 | -- | core | plan D02 T08 §1 |  |
| NP-0337 | Add Anchor Point tool | AI-0083 | -- | core | plan D02 T08 §1 |  |
| NP-0338 | Delete Anchor Point tool | AI-0084 | -- | core | plan D02 T08 §1 |  |
| NP-0339 | Anchor Point (convert) tool | AI-0085 | -- | core | plan D02 T08 §1 |  |
| NP-0340 | Bezier tool and segment control (click straight, drag curve, Space finishes) | -- | CD-584, CD-604 | core | plan D02 T08 §1 | Corel Bezier tool kept as a pen mode, not a second engine |
| NP-0341 | Constrain segment and handle angles | -- | CD-595 | core | plan D02 T08 §1 |  |
| NP-0342 | Hide bounding box after curve tools | -- | CD-609 | core | plan D02 T08 §1 |  |
| NP-0343 | Node tracking from drawing and selection tools | -- | CD-657 | core | plan D02 T08 §1 |  |
| NP-0344 | Freehand and Bezier tool defaults | -- | CD-2846 | core | plan D02 T08 §1 |  |
| NP-0345 | Curvature tool | AI-0086 | -- | core | plan D02 T08 §2 |  |
| NP-0346 | Line segment tool and options (length, angle, fill) | AI-0087, AI-0088 | -- | core | plan D02 T08 §2 |  |
| NP-0347 | Arc tool and Arc options | AI-0089, AI-0090 | -- | core | plan D02 T08 §2 |  |
| NP-0348 | Arc drawing modifiers (open or closed, flip, slope) | AI-0091 | -- | core | plan D02 T08 §2 |  |
| NP-0349 | Parallel drawing mode | -- | CD-155, CD-610 | core | plan D02 T08 §2 |  |
| NP-0350 | 2-point line tool | -- | CD-583 | core | plan D02 T08 §2 |  |
| NP-0351 | B-spline tool | -- | CD-586 | core | plan D02 T08 §2 |  |
| NP-0352 | Polyline tool with mixed straight and curved segments | -- | CD-587, CD-597 | core | plan D02 T08 §2 |  |
| NP-0353 | 3-point curve tool | -- | CD-588 | core | plan D02 T08 §2 |  |
| NP-0354 | Polyline arc mode | -- | CD-598 | core | plan D02 T08 §2 |  |
| NP-0355 | Auto-close curve on finish | -- | CD-600 | core | plan D02 T08 §2 |  |
| NP-0356 | Length and angle readout while drawing | -- | CD-601 | core | plan D02 T08 §2 |  |
| NP-0357 | Perpendicular 2-point line | -- | CD-602 | core | plan D02 T08 §2 |  |
| NP-0358 | Tangential 2-point line | -- | CD-603 | core | plan D02 T08 §2 |  |
| NP-0359 | B-spline clamped and floating control points while drawing | -- | CD-607 | core | plan D02 T08 §2 |  |
| NP-0360 | 3-point curve circular and symmetrical modifiers | -- | CD-608 | core | plan D02 T08 §2 |  |
| NP-0361 | Parallel lines count and side (left, right, both) | -- | CD-611 | core | plan D02 T08 §2 |  |
| NP-0362 | Parallel lines distance | -- | CD-612 | core | plan D02 T08 §2 |  |
| NP-0363 | Parallel lines preview | -- | CD-613 | core | plan D02 T08 §2 |  |
| NP-0364 | Create parallel lines from a selected path | -- | CD-614 | core | plan D02 T08 §2 |  |
| NP-0365 | Pencil and freehand tool with curve fitting | AI-0112 | CD-582 | core | plan D02 T08 §3 |  |
| NP-0366 | Pencil fidelity and freehand smoothing options | AI-0113 | CD-592 | core | plan D02 T08 §3 |  |
| NP-0367 | Straight segments while drawing freehand | AI-0114 | CD-591 | core | plan D02 T08 §3 |  |
| NP-0368 | Extend, reshape, and connect paths with the pencil | AI-0115 | CD-594 | core | plan D02 T08 §3 |  |
| NP-0369 | Pencil live preview and live curve fitting | AI-0116 | -- | core | plan D02 T08 §3 |  |
| NP-0370 | Smooth tool | AI-0117 | -- | core | plan D02 T08 §3 | the Corel nib-based Smooth brush is §9 |
| NP-0371 | Path Eraser tool | AI-0118 | -- | core | plan D02 T08 §3 |  |
| NP-0372 | Join tool (scrub to join and trim ends) | AI-0119 | -- | core | plan D02 T08 §3 |  |
| NP-0373 | Shape recognition drawing (Shaper, smart drawing) | AI-0120 | CD-589, CD-623 | core | plan D02 T08 §3 | local recognizer, no model |
| NP-0374 | Shaper Group: live faces that can be edited and restored | AI-0121 | -- | core | plan D02 T08 §3 |  |
| NP-0375 | LiveSketch tool: stroke adjustment into curves | -- | CD-590, CD-615, CD-3029 | ai | plan D02 T08 §3 | local stroke-fitting algorithm, no neural model (brief routing rule) |
| NP-0376 | Erase back while drawing (Shift-drag backward) | -- | CD-596 | core | plan D02 T08 §3 |  |
| NP-0377 | LiveSketch timer | -- | CD-616 | ai | plan D02 T08 §3 |  |
| NP-0378 | LiveSketch include curves and distance from curve | -- | CD-617 | ai | plan D02 T08 §3 |  |
| NP-0379 | LiveSketch create single curve | -- | CD-618 | ai | plan D02 T08 §3 |  |
| NP-0380 | LiveSketch preview mode | -- | CD-619 | ai | plan D02 T08 §3 |  |
| NP-0381 | LiveSketch curve smoothing | -- | CD-620 | ai | plan D02 T08 §3 |  |
| NP-0382 | Stylus eraser flip erases sketched curves | -- | CD-621 | core | plan D02 T08 §3 |  |
| NP-0383 | LiveSketch re-sketch inherits curve properties | -- | CD-622 | ai | plan D02 T08 §3 |  |
| NP-0384 | Shape recognition level and delay | -- | CD-624, CD-2855 | ai | plan D02 T08 §3 |  |
| NP-0385 | Smart smoothing level for unrecognized strokes | -- | CD-625 | ai | plan D02 T08 §3 |  |
| NP-0386 | Smart drawing corrections (erase back, Esc removes last) | -- | CD-626 | core | plan D02 T08 §3 |  |
| NP-0387 | Smart drawing outline width | -- | CD-627 | core | plan D02 T08 §3 |  |

## Shapes

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0388 | Spiral tool and Spiral options | AI-0092, AI-0093 | CD-817 | core | plan D02 T08 §4 |  |
| NP-0389 | Rectangle tool | AI-0099 | CD-811 | core | plan D02 T08 §4 |  |
| NP-0390 | Rounded Rectangle tool | AI-0100 | -- | core | plan D02 T08 §4 |  |
| NP-0391 | Ellipse tool | AI-0101 | CD-813 | core | plan D02 T08 §4 |  |
| NP-0392 | Polygon tool | AI-0102 | CD-815 | core | plan D02 T08 §4 |  |
| NP-0393 | Star tool | AI-0103 | CD-816 | core | plan D02 T08 §4 |  |
| NP-0394 | Shape options dialog on click | AI-0106 | -- | core | plan D02 T08 §4 |  |
| NP-0395 | Shape draw modifiers (constrain, from center, move while drawing) | AI-0107 | CD-821, CD-830, CD-836 | core | plan D02 T08 §4 | includes the page-sized rectangle on tool double-click |
| NP-0396 | Live shapes: parametric shapes with on-canvas widgets | AI-0170 | -- | core | plan D02 T08 §4 |  |
| NP-0397 | Live corner widget on any path corner | AI-0171 | CD-829 | core | plan D02 T08 §4 |  |
| NP-0398 | Corner types: round, inverted round (scallop), chamfer | AI-0172 | CD-824, CD-825, CD-826 | core | plan D02 T08 §4 |  |
| NP-0399 | Rounding absolute or relative | AI-0173 | -- | core | plan D02 T08 §4 |  |
| NP-0400 | Hide corner widget above an angle | AI-0174, AI-1142 | -- | core | plan D02 T08 §4 |  |
| NP-0401 | Live shape move, rotate, and scale keep parameters | AI-0175 | -- | core | plan D02 T08 §4 |  |
| NP-0402 | Ellipse pie and arc with start and end angles | AI-0176 | CD-831, CD-832, CD-833, CD-835 | core | plan D02 T08 §4 |  |
| NP-0403 | Polygon sides and star points count and widget | AI-0177 | CD-837 | core | plan D02 T08 §4 |  |
| NP-0404 | Star inner and outer radius widgets | AI-0178 | -- | core | plan D02 T08 §4 |  |
| NP-0405 | Shape Properties: numeric shape parameters | AI-0179 | -- | core | plan D02 T08 §4 |  |
| NP-0406 | Convert to Shapes | AI-0180 | -- | core | plan D02 T08 §4 |  |
| NP-0407 | Expand Shape | AI-0181 | -- | core | plan D02 T08 §4 |  |
| NP-0408 | Coordinates panel: create or replace objects by numbers | -- | CD-353, CD-363, CD-645 | core | plan D02 T08 §4 |  |
| NP-0409 | Coordinates: rectangle and square | -- | CD-354, CD-355 | core | plan D02 T08 §4 |  |
| NP-0410 | Coordinates: ellipse and circle | -- | CD-356, CD-357 | core | plan D02 T08 §4 |  |
| NP-0411 | Coordinates: polygon and regular polygon | -- | CD-358, CD-359 | core | plan D02 T08 §4 |  |
| NP-0412 | Coordinates: 2-point line | -- | CD-360 | core | plan D02 T08 §4 |  |
| NP-0413 | Coordinates: multi-point curve | -- | CD-361, CD-658 | core | plan D02 T08 §4 |  |
| NP-0414 | Coordinates: star and complex star | -- | CD-362 | core | plan D02 T08 §4 |  |
| NP-0415 | Corners panel: fillet, scallop, chamfer on any path | -- | CD-700, CD-850, CD-851, CD-852, CD-853 | core | plan D02 T08 §4 |  |
| NP-0416 | 3-point rectangle tool with baseline constraint | -- | CD-812, CD-822 | core | plan D02 T08 §4 |  |
| NP-0417 | 3-point ellipse tool | -- | CD-814 | core | plan D02 T08 §4 |  |
| NP-0418 | Per-corner radius and edit corners together | -- | CD-827 | core | plan D02 T08 §4 |  |
| NP-0419 | Scale corners with the object | -- | CD-828 | core | plan D02 T08 §4 |  |
| NP-0420 | Change pie or arc direction | -- | CD-834 | core | plan D02 T08 §4 |  |
| NP-0421 | Reshape a polygon into a star | -- | CD-838 | core | plan D02 T08 §4 |  |
| NP-0422 | Perfect and complex stars | -- | CD-839, CD-840, CD-855 | core | plan D02 T08 §4 | complex star kept as a star option, not a second tool |
| NP-0423 | Star sharpness | -- | CD-841 | core | plan D02 T08 §4 |  |
| NP-0424 | Spiral revolutions, symmetrical and logarithmic expansion | -- | CD-842, CD-843, CD-844 | core | plan D02 T08 §4 |  |
| NP-0425 | Corner skip rule for short segments and smooth nodes | -- | CD-854 | core | plan D02 T08 §4 |  |
| NP-0426 | Rectangular Grid tool and options | AI-0094, AI-0095 | -- | core | plan D02 T08 §5 |  |
| NP-0427 | Polar Grid tool and options | AI-0096, AI-0097 | -- | core | plan D02 T08 §5 |  |
| NP-0428 | Grid drawing modifiers (dividers and skew keys) | AI-0098 | -- | core | plan D02 T08 §5 |  |
| NP-0429 | Flare tool and Flare options | AI-0104, AI-0105 | -- | core | plan D02 T08 §5 |  |
| NP-0430 | Impact tool | -- | CD-628, CD-819 | core | plan D02 T08 §5 |  |
| NP-0431 | Impact radial and parallel styles | -- | CD-629, CD-630 | core | plan D02 T08 §5 |  |
| NP-0432 | Impact inner and outer boundaries | -- | CD-631, CD-632 | core | plan D02 T08 §5 |  |
| NP-0433 | Impact rotation | -- | CD-633 | core | plan D02 T08 §5 |  |
| NP-0434 | Impact random start and end points | -- | CD-634 | core | plan D02 T08 §5 |  |
| NP-0435 | Impact line widths: min, max, steps, random order | -- | CD-635, CD-636, CD-637 | core | plan D02 T08 §5 |  |
| NP-0436 | Impact line spacing: min, max, steps, random order | -- | CD-638, CD-639, CD-640 | core | plan D02 T08 §5 |  |
| NP-0437 | Impact line style and widest point | -- | CD-641, CD-642 | core | plan D02 T08 §5 |  |
| NP-0438 | Break impact shape apart | -- | CD-643 | core | plan D02 T08 §5 |  |
| NP-0439 | Impact line color from the palette | -- | CD-644 | core | plan D02 T08 §5 |  |
| NP-0440 | Common shapes tool and shape picker | -- | CD-818, CD-847 | core | plan D02 T08 §5 |  |
| NP-0441 | Graph paper tool: columns, rows, ungroup into cells | -- | CD-820, CD-845, CD-846 | core | plan D02 T08 §5 |  |
| NP-0442 | Common shape glyph handles | -- | CD-848 | core | plan D02 T08 §5 |  |
| NP-0443 | Text inside a common shape | -- | CD-849 | core | plan D02 T08 §5 |  |

## Path editing

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0444 | Direct selection and shape tool for anchors and segments | AI-0002 | CD-646, CD-651 | core | plan D02 T08 §6 |  |
| NP-0445 | Corner (cusp) nodes | AI-0135 | CD-688 | core | plan D02 T08 §6 |  |
| NP-0446 | Smooth nodes | AI-0136 | CD-689 | core | plan D02 T08 §6 |  |
| NP-0447 | Show or hide handles for multiple selected anchors | AI-0137 | -- | core | plan D02 T08 §6 |  |
| NP-0448 | Remove selected anchors | AI-0138 | CD-684 | core | plan D02 T08 §6 |  |
| NP-0449 | Align selected anchors | AI-0141 | CD-659, CD-666 | core | plan D02 T08 §6 |  |
| NP-0450 | Anchor X and Y fields | AI-0142 | -- | core | plan D02 T08 §6 |  |
| NP-0451 | Reshape a segment by dragging it | AI-0143 | -- | core | plan D02 T08 §6 |  |
| NP-0452 | Highlight anchors on hover | AI-0167 | -- | core | plan D02 T08 §6 |  |
| NP-0453 | Select all nodes | -- | CD-405, CD-655 | core | plan D02 T08 §6 |  |
| NP-0454 | B-spline control points: float or clamp | -- | CD-647 | core | plan D02 T08 §6 |  |
| NP-0455 | B-spline control points: add, delete, multi-select | -- | CD-648 | core | plan D02 T08 §6 |  |
| NP-0456 | Convert to curves | -- | CD-649 | core | plan D02 T08 §6 |  |
| NP-0457 | Rectangular and freehand node marquee | -- | CD-652, CD-653 | core | plan D02 T08 §6 |  |
| NP-0458 | Multi-node and consecutive node selection | -- | CD-654 | core | plan D02 T08 §6 |  |
| NP-0459 | Next and previous node (Tab, Shift+Tab) | -- | CD-656 | core | plan D02 T08 §6 |  |
| NP-0460 | Align nodes to active nodes, page, grid, or a point | -- | CD-660, CD-661, CD-662, CD-663, CD-664 | core | plan D02 T08 §6 |  |
| NP-0461 | Distribute nodes by span or spacing | -- | CD-667, CD-668 | core | plan D02 T08 §6 |  |
| NP-0462 | Drag control handles (Alt moves node too) | -- | CD-670 | core | plan D02 T08 §6 |  |
| NP-0463 | Convert segment to line | -- | CD-671 | core | plan D02 T08 §6 |  |
| NP-0464 | Convert segment to curve | -- | CD-672 | core | plan D02 T08 §6 |  |
| NP-0465 | Curve smoothness slider | -- | CD-673 | core | plan D02 T08 §6 |  |
| NP-0466 | Copy, cut, and duplicate curve segments | -- | CD-682 | core | plan D02 T08 §6 |  |
| NP-0467 | Add node on a segment | -- | CD-683 | core | plan D02 T08 §6 |  |
| NP-0468 | Reduce nodes | -- | CD-685 | core | plan D02 T08 §6 |  |
| NP-0469 | Symmetrical nodes | -- | CD-690 | core | plan D02 T08 §6 |  |
| NP-0470 | Node shapes by type | -- | CD-691 | core | plan D02 T08 §6 |  |
| NP-0471 | Stretch and scale selected nodes | -- | CD-692 | core | plan D02 T08 §6 |  |
| NP-0472 | Rotate and skew selected nodes | -- | CD-693 | core | plan D02 T08 §6 |  |
| NP-0473 | Extract subpath | -- | CD-695 | core | plan D02 T08 §6 |  |
| NP-0474 | Subpaths and holes in one curve | -- | CD-696 | core | plan D02 T08 §6 |  |
| NP-0475 | Reflect node edits horizontally and vertically | -- | CD-697, CD-698 | core | plan D02 T08 §6 |  |
| NP-0476 | Swap main and secondary node colors | -- | CD-2866 | core | plan D02 T08 §6 |  |
| NP-0477 | Average anchors | AI-0145 | -- | core | plan D02 T08 §7 |  |
| NP-0478 | Corner or smooth join | AI-0146 | -- | core | plan D02 T08 §7 |  |
| NP-0479 | Offset Path | AI-0148 | -- | core | plan D02 T08 §7 |  |
| NP-0480 | Simplify options: precision, corner threshold, straight lines, show original | AI-0151, AI-0152 | -- | core | plan D02 T08 §7 |  |
| NP-0481 | Smooth slider on selected segments | AI-0153 | -- | core | plan D02 T08 §7 |  |
| NP-0482 | Add Anchor Points (midpoints) | AI-0154 | -- | core | plan D02 T08 §7 |  |
| NP-0483 | Remove Anchor Points | AI-0155 | -- | core | plan D02 T08 §7 |  |
| NP-0484 | Divide Objects Below | AI-0156 | -- | core | plan D02 T08 §7 |  |
| NP-0485 | Split Into Grid | AI-0157 | -- | core | plan D02 T08 §7 |  |
| NP-0486 | Clean Up: stray points, unpainted objects, empty text | AI-0158 | -- | core | plan D02 T08 §7 |  |
| NP-0487 | Refine path segments in place | AI-0168 | -- | core | plan D02 T08 §7 |  |
| NP-0488 | Copy paths between documents and apps | AI-0169 | -- | core | plan D02 T08 §7 | pastes as SVG and editable paths; Photoshop shape layers are Imago's side |
| NP-0489 | Join Curves panel with gap tolerance | -- | CD-675, CD-680, CD-699, CD-701 | core | plan D02 T08 §7 |  |
| NP-0490 | Join Curves: extend to intersection | -- | CD-676 | core | plan D02 T08 §7 |  |
| NP-0491 | Join Curves: chamfer | -- | CD-677 | core | plan D02 T08 §7 |  |
| NP-0492 | Join Curves: fillet with radius | -- | CD-678, CD-681 | core | plan D02 T08 §7 |  |
| NP-0493 | Join Curves: Bezier connection | -- | CD-679 | core | plan D02 T08 §7 |  |
| NP-0494 | Extend curve to close | -- | CD-687 | core | plan D02 T08 §7 |  |
| NP-0495 | Scissors tool | AI-0159 | -- | core | plan D02 T08 §8 |  |
| NP-0496 | Knife tool | AI-0160 | CD-874 | core | plan D02 T08 §8 |  |
| NP-0497 | Eraser tool | AI-0161 | CD-876 | core | plan D02 T08 §8 |  |
| NP-0498 | Eraser nib: size, shape, angle, roundness | AI-0162 | CD-881, CD-882 | core | plan D02 T08 §8 |  |
| NP-0499 | Crop tool on vectors | -- | CD-873 | core | plan D02 T08 §8 |  |
| NP-0500 | Virtual segment delete tool | -- | CD-875 | core | plan D02 T08 §8 |  |
| NP-0501 | Crop area position, size, and rotation | -- | CD-877, CD-878 | core | plan D02 T08 §8 |  |
| NP-0502 | Clear crop area | -- | CD-879 | core | plan D02 T08 §8 |  |
| NP-0503 | Crop auto conversion of text and live effects | -- | CD-880 | core | plan D02 T08 §8 |  |
| NP-0504 | Eraser pen pressure, tilt, and bearing | -- | CD-883 | core | plan D02 T08 §8 |  |
| NP-0505 | Eraser reduce nodes and default settings | -- | CD-884, CD-2856 | core | plan D02 T08 §8 |  |
| NP-0506 | Eraser straight-line and double-click erase | -- | CD-885 | core | plan D02 T08 §8 |  |
| NP-0507 | Stylus eraser end switches to erase | -- | CD-886 | core | plan D02 T08 §8 |  |
| NP-0508 | Virtual segment delete by marquee or Alt curve | -- | CD-887 | core | plan D02 T08 §8 |  |
| NP-0509 | Virtual segment delete weld line segments | -- | CD-888 | core | plan D02 T08 §8 |  |
| NP-0510 | Knife modes: 2-point, freehand, Bezier, and mode cycle | -- | CD-889, CD-890, CD-891, CD-894 | core | plan D02 T08 §8 |  |
| NP-0511 | Knife cut span: gap or overlap width | -- | CD-892 | core | plan D02 T08 §8 |  |
| NP-0512 | Knife outline options | -- | CD-893 | core | plan D02 T08 §8 |  |
| NP-0513 | Warp tool | AI-0282 | -- | core | plan D02 T08 §9 |  |
| NP-0514 | Twirl tool | AI-0283 | CD-704, CD-739 | core | plan D02 T08 §9 |  |
| NP-0515 | Attract and repel (pucker and bloat) | AI-0284, AI-0285 | CD-705, CD-735, CD-736, CD-737 | core | plan D02 T08 §9 |  |
| NP-0516 | Scallop tool | AI-0286 | -- | core | plan D02 T08 §9 |  |
| NP-0517 | Crystallize tool | AI-0287 | -- | core | plan D02 T08 §9 |  |
| NP-0518 | Wrinkle tool | AI-0288 | -- | core | plan D02 T08 §9 |  |
| NP-0519 | Liquify tool options | AI-0289 | -- | core | plan D02 T08 §9 |  |
| NP-0520 | Smooth brush tool | -- | CD-702, CD-731 | core | plan D02 T08 §9 |  |
| NP-0521 | Smear tool | -- | CD-703, CD-715 | core | plan D02 T08 §9 |  |
| NP-0522 | Smudge tool | -- | CD-706, CD-708 | core | plan D02 T08 §9 |  |
| NP-0523 | Roughen tool | -- | CD-707, CD-721 | core | plan D02 T08 §9 |  |
| NP-0524 | Smudge nib, pressure, and dryout | -- | CD-709, CD-710, CD-711 | core | plan D02 T08 §9 |  |
| NP-0525 | Smudge tilt and bearing | -- | CD-712, CD-713 | core | plan D02 T08 §9 |  |
| NP-0526 | Control range settings for shaping-tool controls | -- | CD-714 | core | plan D02 T08 §9 |  |
| NP-0527 | Smear nib, amount, and pen pressure | -- | CD-716, CD-717, CD-718 | core | plan D02 T08 §9 |  |
| NP-0528 | Smooth or pointy smear | -- | CD-719, CD-720 | core | plan D02 T08 §9 |  |
| NP-0529 | Roughen nib size and spike frequency | -- | CD-722, CD-723 | core | plan D02 T08 §9 |  |
| NP-0530 | Roughen pressure and dryout | -- | CD-724, CD-725 | core | plan D02 T08 §9 |  |
| NP-0531 | Roughen tilt and spike direction | -- | CD-726, CD-727, CD-728, CD-729 | core | plan D02 T08 §9 |  |
| NP-0532 | Auto convert before roughen | -- | CD-730 | core | plan D02 T08 §9 |  |
| NP-0533 | Smooth brush nib, rate, and pressure | -- | CD-732, CD-733, CD-734 | core | plan D02 T08 §9 |  |
| NP-0534 | Attract and repel nib, rate, and pressure | -- | CD-738 | core | plan D02 T08 §9 |  |
| NP-0535 | Twirl radius, rate, direction, and pressure | -- | CD-740, CD-741, CD-742, CD-743 | core | plan D02 T08 §9 |  |
| NP-0536 | Join endpoints and close path | AI-0139, AI-0144 | CD-686 | core | shipped-scope D02 T06 §2 |  |
| NP-0537 | Break path at anchor | AI-0140 | CD-694 | core | shipped-scope D02 T06 §2 |  |
| NP-0538 | Outline stroke | AI-0147 | -- | core | shipped-scope D02 T06 §2 |  |
| NP-0539 | Reverse path direction | AI-0149 | CD-674 | core | shipped-scope D02 T06 §2 |  |
| NP-0540 | Simplify path | AI-0150 | -- | core | shipped-scope D02 T06 §2 |  |

## Shaping and compound paths

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0541 | Shape Builder tool | AI-0182 | -- | core | plan D02 T08 §10 |  |
| NP-0542 | Shape Builder gap detection | AI-0183 | -- | core | plan D02 T08 §10 |  |
| NP-0543 | Shape Builder open filled paths as closed | AI-0184 | -- | core | plan D02 T08 §10 |  |
| NP-0544 | Shape Builder stroke click splits in merge mode | AI-0185 | -- | core | plan D02 T08 §10 |  |
| NP-0545 | Shape Builder color source and cursor swatch preview | AI-0186 | -- | core | plan D02 T08 §10 |  |
| NP-0546 | Shape Builder selection style and highlight | AI-0187 | -- | core | plan D02 T08 §10 |  |
| NP-0547 | Pathfinder panel and Shaping panel | AI-0188 | CD-871, CD-872 | core | plan D02 T08 §10 | leave-original options live on the panel |
| NP-0548 | Live compound shapes: make, release, expand | AI-0193, AI-0194, AI-0202 | -- | core | plan D02 T08 §10 |  |
| NP-0549 | Divide | AI-0195 | -- | core | plan D02 T08 §10 |  |
| NP-0550 | Trim hidden areas (Pathfinder Trim, Corel Simplify) | AI-0196 | CD-860 | core | plan D02 T08 §10 |  |
| NP-0551 | Merge same-color objects | AI-0197 | -- | core | plan D02 T08 §10 |  |
| NP-0552 | Crop to the top object | AI-0198 | -- | core | plan D02 T08 §10 |  |
| NP-0553 | Outline into stroked segments | AI-0199 | -- | core | plan D02 T08 §10 |  |
| NP-0554 | Front minus back (Minus Back) | AI-0200 | CD-858 | core | plan D02 T08 §10 |  |
| NP-0555 | Pathfinder options: precision, redundant points, unpainted artwork | AI-0201 | -- | core | plan D02 T08 §10 |  |
| NP-0556 | Repeat last pathfinder | AI-0203 | -- | core | plan D02 T08 §10 |  |
| NP-0557 | Trim a target by source objects and the target rule | -- | CD-856, CD-857 | core | plan D02 T08 §10 |  |
| NP-0558 | Back minus front | -- | CD-859 | core | plan D02 T08 §10 |  |
| NP-0559 | Shaping on a PowerClip frame | -- | CD-861 | core | plan D02 T08 §10 |  |
| NP-0560 | Linked effects converted before shaping | -- | CD-862 | core | plan D02 T08 §10 |  |
| NP-0561 | Weld, including weld groups | -- | CD-863 | core | plan D02 T08 §10 | plain union ships in D02 T02 §5 |
| NP-0562 | Weld a self-intersecting object | -- | CD-864 | core | plan D02 T08 §10 |  |
| NP-0563 | Intersect with the target's attributes | -- | CD-865 | core | plan D02 T08 §10 |  |
| NP-0564 | Intersect multiple targets | -- | CD-866 | core | plan D02 T08 §10 |  |
| NP-0565 | Create object from an enclosed area | -- | CD-867 | core | plan D02 T08 §10 | click-to-fill overlaps D02 T11 §17 smart fill |
| NP-0566 | Boundary | -- | CD-868 | core | plan D02 T08 §10 |  |
| NP-0567 | Draw Normal, Behind, and Inside | AI-0122 | -- | core | plan D02 T08 §11 |  |
| NP-0568 | Make compound path (Combine) | AI-0163 | CD-869 | core | plan D02 T08 §11 |  |
| NP-0569 | Release compound path (Break Curve Apart) | AI-0164 | CD-870 | core | plan D02 T08 §11 |  |
| NP-0570 | Fill rule: nonzero or even-odd | AI-0165 | -- | core | plan D02 T08 §11 |  |
| NP-0571 | Intertwine: make | AI-0207 | -- | core | plan D02 T08 §11 |  |
| NP-0572 | Intertwine: edit and release | AI-0208 | -- | core | plan D02 T08 §11 |  |
| NP-0573 | Clipping mask make and release | AI-0215, AI-0216 | -- | core | plan D02 T08 §11 |  |
| NP-0574 | Edit mask or edit contents | AI-0217 | -- | core | plan D02 T08 §11 |  |
| NP-0575 | Layer clipping mask | AI-0218 | -- | core | plan D02 T08 §11 |  |
| NP-0576 | Text as a clipping path | AI-0219 | -- | core | plan D02 T08 §11 |  |
| NP-0577 | Treat all objects as filled | -- | CD-2869 | core | plan D02 T08 §11 | a pick-tool hit-test preference; could sit with D02 T07 §6 |
| NP-0578 | Fill open curves | -- | CD-2886 | core | plan D02 T08 §11 |  |
| NP-0579 | Boolean union | AI-0189 | -- | core | shipped-scope D02 T02 §5 |  |
| NP-0580 | Boolean subtract front | AI-0190 | -- | core | shipped-scope D02 T02 §5 |  |
| NP-0581 | Boolean intersect | AI-0191 | -- | core | shipped-scope D02 T02 §5 |  |
| NP-0582 | Boolean exclude | AI-0192 | -- | core | shipped-scope D02 T02 §5 |  |

## Transform, align, and arrange

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0583 | Transform Again | AI-0229 | -- | core | plan D02 T08 §12 |  |
| NP-0584 | Move by exact offset or position | AI-0230 | CD-376, CD-377, CD-406 | core | plan D02 T08 §12 |  |
| NP-0585 | Rotate by angle around a center | AI-0231 | CD-392, CD-393, CD-407 | core | plan D02 T08 §12 |  |
| NP-0586 | Reflect dialog | AI-0232 | -- | core | plan D02 T08 §12 |  |
| NP-0587 | Scale and mirror by percentage | AI-0233 | CD-388, CD-408 | core | plan D02 T08 §12 |  |
| NP-0588 | Shear and skew by angle | AI-0234 | CD-394, CD-410 | core | plan D02 T08 §12 |  |
| NP-0589 | Transform Each | AI-0235 | -- | core | plan D02 T08 §12 |  |
| NP-0590 | Transform Each relative or absolute scaling | AI-0236 | -- | core | plan D02 T08 §12 |  |
| NP-0591 | Transform panel and Transform docker | AI-0237 | CD-422 | core | plan D02 T08 §12 |  |
| NP-0592 | Constrain width and height, or stretch non-proportionally | AI-0238 | CD-320 | core | plan D02 T08 §12 |  |
| NP-0593 | Scale corners and scale strokes and effects | AI-0239 | -- | core | plan D02 T08 §12 |  |
| NP-0594 | Align to pixel grid | AI-0240 | -- | core | plan D02 T08 §12 |  |
| NP-0595 | Flip horizontal and vertical from the Transform panel | AI-0241 | -- | core | plan D02 T08 §12 |  |
| NP-0596 | Transform objects, patterns, or both | AI-0242, AI-0245 | -- | core | plan D02 T08 §12 |  |
| NP-0597 | Math in fields and apply to a copy | AI-0243 | -- | core | plan D02 T08 §12 |  |
| NP-0598 | Nudge by keyboard increment | AI-0247 | -- | core | plan D02 T08 §12 |  |
| NP-0599 | Move multiple objects together | AI-0269 | -- | core | plan D02 T08 §12 |  |
| NP-0600 | Scale multiple objects together or each | AI-0270 | -- | core | plan D02 T08 §12 |  |
| NP-0601 | Clear transformations | -- | CD-339, CD-411 | core | plan D02 T08 §12 |  |
| NP-0602 | Reference point selector | -- | CD-374 | core | plan D02 T08 §12 |  |
| NP-0603 | Transform copies | -- | CD-378 | core | plan D02 T08 §12 |  |
| NP-0604 | Size by exact width and height | -- | CD-389, CD-409 | core | plan D02 T08 §12 |  |
| NP-0605 | Scale portion and fit to reference in the Transform docker | -- | CD-390, CD-391 | core | plan D02 T08 §12 |  |
| NP-0606 | Rotate tool, rotation handles, and movable pivot | AI-0220 | CD-337, CD-395 | core | plan D02 T08 §13 |  |
| NP-0607 | Reflect tool and mirror buttons | AI-0221 | CD-401 | core | plan D02 T08 §13 |  |
| NP-0608 | Scale tool | AI-0222 | -- | core | plan D02 T08 §13 |  |
| NP-0609 | Shear tool and skew handles | AI-0223 | CD-319, CD-336 | core | plan D02 T08 §13 |  |
| NP-0610 | Reshape tool | AI-0224 | -- | core | plan D02 T08 §13 |  |
| NP-0611 | Free transform tool | AI-0225 | CD-316 | core | plan D02 T08 §13 |  |
| NP-0612 | Free transform modes: constrain, rotate, scale, skew, perspective, free distort | AI-0226 | CD-317, CD-384, CD-385 | core | plan D02 T08 §13 |  |
| NP-0613 | Scale portion tool | -- | CD-312 | core | plan D02 T08 §13 |  |
| NP-0614 | Fit to Reference tool | -- | CD-313 | core | plan D02 T08 §13 |  |
| NP-0615 | Free transform relative to object | -- | CD-318, CD-386 | core | plan D02 T08 §13 |  |
| NP-0616 | Handle-drag modifiers: from center, integer multiples, stretch | -- | CD-321, CD-379, CD-380, CD-381 | core | plan D02 T08 §13 |  |
| NP-0617 | Selection handles: scale by corner, stretch by side | -- | CD-333, CD-334, CD-335 | core | plan D02 T08 §13 |  |
| NP-0618 | Mirror by Ctrl-dragging a handle | -- | CD-338 | core | plan D02 T08 §13 |  |
| NP-0619 | Free transform apply to duplicate | -- | CD-387 | core | plan D02 T08 §13 |  |
| NP-0620 | Angle of rotation box | -- | CD-396 | core | plan D02 T08 §13 |  |
| NP-0621 | Constrain and draw-from-center modifiers across tools | -- | CD-399, CD-400 | core | plan D02 T08 §13 |  |
| NP-0622 | Send to current layer | AI-0249 | -- | core | plan D02 T08 §14 |  |
| NP-0623 | Align panel and Align and Distribute docker | AI-0256 | CD-421, CD-423, CD-436 | core | plan D02 T08 §14 |  |
| NP-0624 | Center to page in one action | AI-0259 | CD-418, CD-419, CD-420, CD-448 | core | plan D02 T08 §14 |  |
| NP-0625 | Distribute top, center, bottom | AI-0260 | CD-460, CD-462 | core | plan D02 T08 §14 |  |
| NP-0626 | Distribute left, center, right | AI-0261 | CD-456, CD-458 | core | plan D02 T08 §14 |  |
| NP-0627 | Distribute spacing equal or by exact distance | AI-0262 | CD-455, CD-459, CD-463 | core | plan D02 T08 §14 |  |
| NP-0628 | Distribute spacing preview | AI-0263 | -- | core | plan D02 T08 §14 |  |
| NP-0629 | Align to selection, key object, or artboard | AI-0264, AI-0265 | CD-437 | core | plan D02 T08 §14 |  |
| NP-0630 | Use preview bounds, object outline, or glyph bounds | AI-0266 | CD-449 | core | plan D02 T08 §14 |  |
| NP-0631 | Align and distribute shortcuts | AI-0267 | -- | core | plan D02 T08 §14 | shortcuts only; action recording is excluded automation |
| NP-0632 | Align selected artboards | AI-0268 | -- | core | plan D02 T08 §14 |  |
| NP-0633 | Step and Repeat: copies with offset, spacing, or no offset | -- | CD-345, CD-346, CD-347, CD-348, CD-541, CD-578 | core | plan D02 T08 §14 |  |
| NP-0634 | Align to page edge or page center | -- | CD-438, CD-439 | core | plan D02 T08 §14 |  |
| NP-0635 | Align to grid | -- | CD-440 | core | plan D02 T08 §14 |  |
| NP-0636 | Align to a specified point | -- | CD-441 | core | plan D02 T08 §14 |  |
| NP-0637 | Text alignment reference: first baseline, last baseline, bounding box | -- | CD-450, CD-451, CD-452, CD-665, CD-1046 | core | plan D02 T08 §14 |  |
| NP-0638 | Distribute to selection or page | -- | CD-453, CD-454 | core | plan D02 T08 §14 |  |
| NP-0639 | To front or back of page | -- | CD-464, CD-465 | core | plan D02 T08 §14 |  |
| NP-0640 | To front or back of layer | -- | CD-466, CD-467 | core | plan D02 T08 §14 |  |
| NP-0641 | In front of or behind a clicked object | -- | CD-470, CD-471 | core | plan D02 T08 §14 |  |
| NP-0642 | Reverse order | -- | CD-472 | core | plan D02 T08 §14 |  |
| NP-0643 | Locked layer order rule | -- | CD-473 | core | plan D02 T08 §14 |  |
| NP-0644 | Group, ungroup, and ungroup all | AI-0062, AI-0063 | CD-485, CD-487, CD-488 | core | shipped-scope D02 T02 §4 |  |
| NP-0645 | Stacking order (front, forward, backward, back) | AI-0248 | CD-468, CD-469 | core | shipped-scope D02 T02 §4 |  |
| NP-0646 | Align edges and centers | AI-0257, AI-0258 | CD-412, CD-413, CD-414, CD-415, CD-416, CD-417, CD-442, CD-443, CD-444, CD-445, CD-446, CD-447 | core | shipped-scope D02 T02 §4 |  |
| NP-0647 | Mirror horizontally and vertically | -- | CD-397, CD-398 | core | shipped-scope D02 T02 §4 |  |
| NP-0648 | Distribute centers | -- | CD-457, CD-461 | core | shipped-scope D02 T02 §4 |  |

## Dimensions and connectors

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0649 | Dimension tool | AI-0132 | -- | core | plan D02 T08 §15 |  |
| NP-0650 | Linear dimensions: horizontal, vertical, aligned | AI-0293 | CD-1292, CD-1293 | core | plan D02 T08 §15 |  |
| NP-0651 | Angular dimensions | AI-0294 | CD-1294 | core | plan D02 T08 §15 |  |
| NP-0652 | Radial dimensions | AI-0295 | -- | core | plan D02 T08 §15 |  |
| NP-0653 | Dimension number format: units, precision, style, unit label, leading zero | AI-0296 | CD-1316, CD-1317, CD-1318, CD-1319, CD-1323 | core | plan D02 T08 §15 |  |
| NP-0654 | Dimension arrows and line style | AI-0297 | -- | core | plan D02 T08 §15 |  |
| NP-0655 | Dimension extension lines | AI-0298 | CD-1325 | core | plan D02 T08 §15 |  |
| NP-0656 | Dimension label font and position | AI-0299 | CD-1320, CD-1321 | core | plan D02 T08 §15 |  |
| NP-0657 | Associative (dynamic) dimensions | AI-0300 | CD-1324 | core | plan D02 T08 §15 |  |
| NP-0658 | Stacked dimensions | AI-0301 | -- | core | plan D02 T08 §15 |  |
| NP-0659 | Break dimension apart | -- | CD-553 | core | plan D02 T08 §15 |  |
| NP-0660 | Segment dimensions across one or more segments | -- | CD-1295, CD-1314 | core | plan D02 T08 §15 |  |
| NP-0661 | 2-leg callout tool with shape and gap | -- | CD-1296, CD-1312 | core | plan D02 T08 §15 |  |
| NP-0662 | Connector tool: straight connectors | -- | CD-1297, CD-1299 | core | plan D02 T08 §15 |  |
| NP-0663 | Anchor editing tool: add, move, delete anchors | -- | CD-1298, CD-1305, CD-1308, CD-1309 | core | plan D02 T08 §15 |  |
| NP-0664 | Right-angle and rounded right-angle connectors | -- | CD-1300, CD-1301 | core | plan D02 T08 §15 |  |
| NP-0665 | Edit connector segments | -- | CD-1302 | core | plan D02 T08 §15 |  |
| NP-0666 | Connectors stay attached when objects move | -- | CD-1303 | core | plan D02 T08 §15 |  |
| NP-0667 | Anchor exit direction | -- | CD-1304 | core | plan D02 T08 §15 |  |
| NP-0668 | Auto anchor as a snap point | -- | CD-1306 | core | plan D02 T08 §15 |  |
| NP-0669 | Anchor position relative to object | -- | CD-1307 | core | plan D02 T08 §15 |  |
| NP-0670 | Wrap connector around objects | -- | CD-1310 | core | plan D02 T08 §15 |  |
| NP-0671 | Connector text label | -- | CD-1311 | core | plan D02 T08 §15 |  |
| NP-0672 | Break callout apart | -- | CD-1313 | core | plan D02 T08 §15 |  |
| NP-0673 | Automatic successive dimensioning | -- | CD-1315 | core | plan D02 T08 §15 |  |
| NP-0674 | Dimension prefix and suffix | -- | CD-1322 | core | plan D02 T08 §15 |  |
| NP-0675 | Connector defaults | -- | CD-2847 | core | plan D02 T08 §15 |  |
| NP-0676 | Dimension defaults | -- | CD-2848 | core | plan D02 T08 §15 |  |

## Color

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0677 | Spot colors defined by Lab or CMYK values | AI-0443 | -- | print | plan D02 T09 §1 |  |
| NP-0678 | Tints of global and spot colors | AI-0445 | -- | core | plan D02 T09 §1 |  |
| NP-0679 | Convert selected colors to CMYK, grayscale, or RGB | AI-0479 | -- | core | plan D02 T09 §1 |  |
| NP-0680 | Document color mode RGB or CMYK | AI-0483 | -- | core | plan D02 T09 §1 |  |
| NP-0681 | Device-named cut spot colors (CutContour) | -- | CD-1480 | print | plan D02 T09 §1 | named spot preserved to PDF as a Separation |
| NP-0682 | CMYK color model | -- | CD-1502 | core | plan D02 T09 §1 |  |
| NP-0683 | RGB color model | -- | CD-1503 | core | plan D02 T09 §1 |  |
| NP-0684 | HSB color model | -- | CD-1504 | core | plan D02 T09 §1 |  |
| NP-0685 | Grayscale color model | -- | CD-1505 | core | plan D02 T09 §1 |  |
| NP-0686 | Lab, CMY, HLS, YIQ, and registration color models | -- | CD-1506 | core | plan D02 T09 §1 | YIQ kept as a viewer-only model |
| NP-0687 | Fill and stroke wells with swap, default, and none | AI-0426 | -- | core | plan D02 T09 §2 |  |
| NP-0688 | Toggle fill or stroke focus (X) | AI-0427 | -- | core | plan D02 T09 §2 |  |
| NP-0689 | Color panel and Color docker | AI-0428 | CD-1515, CD-1559 | core | plan D02 T09 §2 | menu and docker rows of one panel |
| NP-0690 | Hex field, hex entry, and Copy Hex | AI-0429 | CD-1521 | core | plan D02 T09 §2 |  |
| NP-0691 | Invert and complement color | AI-0430 | -- | core | plan D02 T09 §2 |  |
| NP-0692 | Out-of-gamut and web-safe warnings | AI-0431 | -- | core | plan D02 T09 §2 | gamut test through D01 T04 §2 |
| NP-0693 | Create swatch from the Color panel | AI-0432 | -- | core | plan D02 T09 §2 |  |
| NP-0694 | Shift-drag sliders in tandem | AI-0433 | -- | core | plan D02 T09 §2 |  |
| NP-0695 | Recent colors | AI-0434 | -- | core | plan D02 T09 §2 |  |
| NP-0696 | Color picker dialog | AI-0435 | -- | core | plan D02 T09 §2 | Nodus-local picker; moves to Photon.UI when D03 T03 §8 needs it |
| NP-0697 | Picker sampling with a loupe preview | AI-0436 | -- | core | plan D02 T09 §2 |  |
| NP-0698 | Eyedropper tool (color) | AI-0437 | CD-1500 | core | plan D02 T09 §2 |  |
| NP-0699 | Eyedropper attribute choices: properties, transformations, effects | AI-0438 | CD-365, CD-366, CD-367 | core | plan D02 T09 §2 |  |
| NP-0700 | Attributes eyedropper | -- | CD-364, CD-1501 | core | plan D02 T09 §2 | toolbox and flyout rows of one tool |
| NP-0701 | Color shade pop-up on a swatch | -- | CD-1508 | core | plan D02 T09 §2 |  |
| NP-0702 | Mix colors with Ctrl+click | -- | CD-1509 | core | plan D02 T09 §2 |  |
| NP-0703 | Show color names on palettes | -- | CD-1510 | core | plan D02 T09 §2 |  |
| NP-0704 | Color palettes mode in color dialogs | -- | CD-1512 | core | plan D02 T09 §2 |  |
| NP-0705 | Color viewers mode | -- | CD-1513 | core | plan D02 T09 §2 |  |
| NP-0706 | Swap reference and new color | -- | CD-1514 | core | plan D02 T09 §2 |  |
| NP-0707 | Eyedropper sample size | -- | CD-1516 | core | plan D02 T09 §2 |  |
| NP-0708 | Sample colors from the desktop | -- | CD-1517 | core | plan D02 T09 §2 |  |
| NP-0709 | Apply sampled color to fill or outline | -- | CD-1518 | core | plan D02 T09 §2 |  |
| NP-0710 | Add sampled color to a palette | -- | CD-1519 | core | plan D02 T09 §2 |  |
| NP-0711 | Drag color swatches onto objects | -- | CD-1520 | core | plan D02 T09 §2 |  |
| NP-0712 | Hex values on the status bar and in dialogs | -- | CD-1522 | core | plan D02 T09 §2 |  |

## Swatches, palettes, and color styles

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0713 | Swatches panel | AI-0439 | -- | core | plan D02 T09 §3 |  |
| NP-0714 | Process color swatches | AI-0440 | -- | core | plan D02 T09 §3 |  |
| NP-0715 | Global process swatches | AI-0441 | -- | core | plan D02 T09 §3 |  |
| NP-0716 | Spot color swatches | AI-0442 | -- | print | plan D02 T09 §3 |  |
| NP-0717 | Registration swatch | AI-0444 | -- | print | plan D02 T09 §3 |  |
| NP-0718 | Swatch Options dialog | AI-0446 | -- | core | plan D02 T09 §3 |  |
| NP-0719 | New swatch and new color group | AI-0447 | -- | core | plan D02 T09 §3 |  |
| NP-0720 | Add selected, used, or document colors | AI-0448 | CD-1529, CD-1530 | core | plan D02 T09 §3 |  |
| NP-0721 | Delete, merge, duplicate, and select unused swatches | AI-0449 | CD-1531 | core | plan D02 T09 §3 |  |
| NP-0722 | Replace a swatch by Alt-drag | AI-0450 | -- | core | plan D02 T09 §3 |  |
| NP-0723 | Sort and filter swatches by name or kind | AI-0451 | -- | core | plan D02 T09 §3 |  |
| NP-0724 | Swatch thumbnail and list views | AI-0452 | -- | core | plan D02 T09 §3 |  |
| NP-0725 | Select Same matches tint percentage | AI-1121 | -- | core | plan D02 T09 §3 |  |
| NP-0726 | Document palette | -- | CD-1525 | core | plan D02 T09 §3 |  |
| NP-0727 | Auto-add used colors to the document palette | -- | CD-1526, CD-2881 | core | plan D02 T09 §3 | docker toggle and preference of one setting |
| NP-0728 | Add bitmap colors to a palette with the eyedropper | -- | CD-1527 | core | plan D02 T09 §3 |  |
| NP-0729 | Add colors by dragging objects onto a palette | -- | CD-1528 | core | plan D02 T09 §3 |  |
| NP-0730 | Refresh document palette (remove unused) | -- | CD-1532 | core | plan D02 T09 §3 |  |
| NP-0731 | Reorder swatches by dragging | -- | CD-1533 | core | plan D02 T09 §3 |  |
| NP-0732 | Swatch and palette libraries browser | AI-0453 | CD-1558 | core | plan D02 T09 §4 |  |
| NP-0733 | Color books and spot libraries (user-imported) | AI-0454 | CD-1499, CD-1549 | core | plan D02 T09 §4 | no bundled PANTONE or other licensed books; users import ASE, ACB, or CPL they own |
| NP-0734 | Gradient and pattern swatch libraries | AI-0455 | -- | core | plan D02 T09 §4 | Nodus ships its own curated set |
| NP-0735 | Save swatch library as ASE or SVG | AI-0456 | -- | core | plan D02 T09 §4 | ASE written; the Illustrator .ai library form is exported through the AI writer |
| NP-0736 | Edit user-defined swatch libraries | AI-0457 | -- | core | plan D02 T09 §4 |  |
| NP-0737 | Palette click shortcuts (fill, outline, mix, shades) | -- | CD-190 | core | plan D02 T09 §4 |  |
| NP-0738 | Default color palette bar (RGB or CMYK) | -- | CD-1507, CD-1554, CD-1555 | core | plan D02 T09 §4 |  |
| NP-0739 | Spot swatch marker | -- | CD-1511 | core | plan D02 T09 §4 |  |
| NP-0740 | Palettes docker (palette manager) | -- | CD-1534, CD-1553, CD-1560 | core | plan D02 T09 §4 | menu, docker, and inspector rows of one docker |
| NP-0741 | New empty color palette | -- | CD-1535 | core | plan D02 T09 §4 |  |
| NP-0742 | Create palette from selection or document | -- | CD-1536, CD-1537 | core | plan D02 T09 §4 |  |
| NP-0743 | Palette editor with sort | -- | CD-1538, CD-1540 | core | plan D02 T09 §4 |  |
| NP-0744 | Treat palette color as spot or process | -- | CD-1539 | core | plan D02 T09 §4 |  |
| NP-0745 | Rename or delete a custom palette | -- | CD-1541 | core | plan D02 T09 §4 |  |
| NP-0746 | Add to palette from color dialogs | -- | CD-1542 | core | plan D02 T09 §4 |  |
| NP-0747 | Show, hide, and close palettes | -- | CD-1543, CD-1556 | core | plan D02 T09 §4 |  |
| NP-0748 | Set as default palette | -- | CD-1544 | core | plan D02 T09 §4 |  |
| NP-0749 | Open palette files (XML, CPL, ASE, ACO, GPL) | -- | CD-1545 | format | plan D02 T09 §4 | CPL converted on open |
| NP-0750 | Palette folders | -- | CD-1546 | core | plan D02 T09 §4 |  |
| NP-0751 | Copy a locked library palette for editing | -- | CD-1547 | core | plan D02 T09 §4 |  |
| NP-0752 | Process palette libraries | -- | CD-1548 | core | plan D02 T09 §4 |  |
| NP-0753 | Dock, float, and lock palette bars | -- | CD-1550, CD-1557 | core | plan D02 T09 §4 |  |
| NP-0754 | Palette rows | -- | CD-1551 | core | plan D02 T09 §4 |  |
| NP-0755 | SVG color keyword palette | -- | CD-1552 | core | plan D02 T09 §4 |  |
| NP-0756 | Right mouse button action for swatches | -- | CD-2882 | core | plan D02 T09 §4 |  |
| NP-0757 | Wide borders, large swatches, and the No Color well | -- | CD-2883 | core | plan D02 T09 §4 |  |
| NP-0758 | Color Guide panel | AI-0458 | -- | core | plan D02 T09 §5 |  |
| NP-0759 | Harmony rules: analogous, accented, complementary, monochromatic, triad, tetrad, and more | AI-0459 | CD-1666, CD-1667, CD-1668, CD-1669, CD-1670, CD-1671 | core | plan D02 T09 §5 |  |
| NP-0760 | Color Guide variations: tints and shades, warm and cool, vivid and muted | AI-0460 | -- | core | plan D02 T09 §5 |  |
| NP-0761 | Limit Color Guide to a swatch library | AI-0461 | -- | core | plan D02 T09 §5 |  |
| NP-0762 | Save harmony as a color group | AI-0462 | -- | core | plan D02 T09 §5 |  |
| NP-0763 | Color Styles docker | -- | CD-1642, CD-1684 | core | plan D02 T09 §5 | docker and inspector rows of one docker |
| NP-0764 | Global color styles | -- | CD-1643 | core | plan D02 T09 §5 |  |
| NP-0765 | New color style from selected | -- | CD-1644 | core | plan D02 T09 §5 |  |
| NP-0766 | Group new color styles into harmonies | -- | CD-1645 | core | plan D02 T09 §5 |  |
| NP-0767 | Convert color styles to a mode while creating | -- | CD-1646 | core | plan D02 T09 §5 |  |
| NP-0768 | New color style from the color editor | -- | CD-1647 | core | plan D02 T09 §5 |  |
| NP-0769 | New color styles from document | -- | CD-1648 | core | plan D02 T09 §5 |  |
| NP-0770 | New color harmony | -- | CD-1649 | core | plan D02 T09 §5 |  |
| NP-0771 | Duplicate harmony | -- | CD-1650 | core | plan D02 T09 §5 |  |
| NP-0772 | Gradient harmony with shade options | -- | CD-1651, CD-1652 | core | plan D02 T09 §5 |  |
| NP-0773 | Apply color style to fill or outline | -- | CD-1653 | core | plan D02 T09 §5 |  |
| NP-0774 | Rename and delete color styles | -- | CD-1654, CD-1660 | core | plan D02 T09 §5 |  |
| NP-0775 | Merge color styles | -- | CD-1655 | core | plan D02 T09 §5 |  |
| NP-0776 | Swap fill and outline color styles | -- | CD-1656 | core | plan D02 T09 §5 |  |
| NP-0777 | Select unused color styles | -- | CD-1657 | core | plan D02 T09 §5 |  |
| NP-0778 | Color styles palette | -- | CD-1658 | core | plan D02 T09 §5 |  |
| NP-0779 | Edit color style | -- | CD-1659 | core | plan D02 T09 §5 |  |
| NP-0780 | Convert color style to a mode, spot, or grayscale | -- | CD-1661, CD-1662, CD-1663 | core | plan D02 T09 §5 |  |
| NP-0781 | Harmony editor wheel | -- | CD-1664 | core | plan D02 T09 §5 |  |
| NP-0782 | Harmony brightness | -- | CD-1665 | core | plan D02 T09 §5 |  |
| NP-0783 | Custom harmony and remove harmony rule | -- | CD-1672, CD-1675 | core | plan D02 T09 §5 |  |
| NP-0784 | Rule-based harmony from scratch | -- | CD-1673 | core | plan D02 T09 §5 |  |
| NP-0785 | Distribute harmony colors | -- | CD-1674 | core | plan D02 T09 §5 |  |
| NP-0786 | Switch to opposite color | -- | CD-1676 | core | plan D02 T09 §5 |  |
| NP-0787 | Move color to another harmony arm | -- | CD-1677 | core | plan D02 T09 §5 |  |
| NP-0788 | Edit multiple harmonies together | -- | CD-1678 | core | plan D02 T09 §5 |  |
| NP-0789 | Reorder harmonies | -- | CD-1679 | core | plan D02 T09 §5 |  |
| NP-0790 | Color style hint view | -- | CD-1680 | core | plan D02 T09 §5 |  |
| NP-0791 | Large swatches and empty arms view options | -- | CD-1681, CD-1682 | core | plan D02 T09 §5 |  |
| NP-0792 | Break link to color styles | -- | CD-1683 | core | plan D02 T09 §5 |  |
| NP-0793 | Recolor Artwork dialog | AI-0463 | -- | core | plan D02 T09 §6 |  |
| NP-0794 | Recolor library limit, color count, and themes | AI-0464, AI-0472 | -- | core | plan D02 T09 §6 |  |
| NP-0795 | Recolor theme picker sampling image or art | AI-0465 | -- | core | plan D02 T09 §6 |  |
| NP-0796 | Recolor prominent colors bar | AI-0466 | -- | core | plan D02 T09 §6 |  |
| NP-0797 | Recolor color wheel with linked harmony | AI-0467 | -- | core | plan D02 T09 §6 |  |
| NP-0798 | Randomize color order, saturation, and brightness | AI-0468 | -- | core | plan D02 T09 §6 |  |
| NP-0799 | Recolor Assign tab | AI-0469 | -- | core | plan D02 T09 §6 |  |
| NP-0800 | Recolor Edit tab | AI-0470 | -- | core | plan D02 T09 §6 |  |
| NP-0801 | Color reduction options and colorize methods | AI-0471 | -- | core | plan D02 T09 §6 |  |
| NP-0802 | Recolor preview toggle and get colors from selection | AI-0473 | -- | core | plan D02 T09 §6 |  |
| NP-0803 | Global or local recolor changes | AI-0474 | -- | core | plan D02 T09 §6 |  |
| NP-0804 | Recolor color groups: save, add, remove, edit | AI-0475, AI-0476 | -- | core | plan D02 T09 §6 |  |
| NP-0805 | Adjust Color Balance | AI-0477 | -- | core | plan D02 T09 §6 |  |
| NP-0806 | Blend colors front to back, horizontally, vertically | AI-0478 | -- | core | plan D02 T09 §6 |  |
| NP-0807 | Invert Colors | AI-0480 | -- | core | plan D02 T09 §6 |  |
| NP-0808 | Saturate | AI-0482 | -- | core | plan D02 T09 §6 |  |
| NP-0809 | Recolor quick action | AI-1202 | -- | core | plan D02 T09 §6 | the convert-sketch half of the row is a tracing quick action |
| NP-0810 | Find and replace fill and outline colors | -- | CD-1497, CD-1523 | core | plan D02 T09 §6 |  |
| NP-0811 | Find and replace color model or palette | -- | CD-1524 | core | plan D02 T09 §6 |  |

## Gradients, mesh, patterns, and fills

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0812 | Gradient panel | AI-0486 | -- | core | plan D02 T09 §7 |  |
| NP-0813 | Linear gradient | AI-0487 | CD-1332 | core | plan D02 T09 §7 |  |
| NP-0814 | Radial and elliptical gradient | AI-0488 | CD-1333 | core | plan D02 T09 §7 |  |
| NP-0815 | Gradient stops: color, opacity, location, midpoint | AI-0491 | CD-1337, CD-1338, CD-1339 | core | plan D02 T09 §7 |  |
| NP-0816 | Gradient angle and aspect ratio | AI-0492 | -- | core | plan D02 T09 §7 |  |
| NP-0817 | Reverse gradient | AI-0493 | CD-1341 | core | plan D02 T09 §7 |  |
| NP-0818 | Gradient dither | AI-0497 | -- | core | plan D02 T09 §7 |  |
| NP-0819 | Perceptual gradient interpolation | AI-0498 | -- | core | plan D02 T09 §7 |  |
| NP-0820 | Gradient presets | AI-0499 | -- | core | plan D02 T09 §7 |  |
| NP-0821 | Gradient from the existing fill | AI-0500 | -- | core | plan D02 T09 §7 |  |
| NP-0822 | Gradient swatches | AI-0501 | -- | core | plan D02 T09 §7 |  |
| NP-0823 | Conical gradient | -- | CD-1334 | core | plan D02 T09 §7 | promoted from backlog B-003; SVG fallback is an expanded mesh or image |
| NP-0824 | Rectangular gradient | -- | CD-1335 | core | plan D02 T09 §7 |  |
| NP-0825 | Gradient arrangement: default, repeat, repeat and mirror | -- | CD-1340 | core | plan D02 T09 §7 |  |
| NP-0826 | Gradient acceleration | -- | CD-1342 | core | plan D02 T09 §7 |  |
| NP-0827 | Smooth gradient transitions | -- | CD-1343 | core | plan D02 T09 §7 |  |
| NP-0828 | Color blend direction: linear, clockwise, counterclockwise | -- | CD-1344 | core | plan D02 T09 §7 |  |
| NP-0829 | Fill winding rule | -- | CD-1347 | core | plan D02 T09 §7 |  |
| NP-0830 | Fountain steps and display preview steps | -- | CD-1349, CD-2884 | core | plan D02 T09 §7 |  |
| NP-0831 | Gradient tool and annotator | AI-0131, AI-0495 | -- | core | plan D02 T09 §8 |  |
| NP-0832 | Freeform gradient: points | AI-0489 | -- | core | plan D02 T09 §8 |  |
| NP-0833 | Freeform gradient: lines | AI-0490 | -- | core | plan D02 T09 §8 |  |
| NP-0834 | Stroke gradient: within, along, across | AI-0494 | -- | core | plan D02 T09 §8 |  |
| NP-0835 | Gradient across multiple objects | AI-0496 | -- | core | plan D02 T09 §8 |  |
| NP-0836 | Interactive fill tool | -- | CD-1326, CD-1330 | core | plan D02 T09 §8 | two toolbox rows of one tool |
| NP-0837 | Uniform fill | -- | CD-1329 | core | plan D02 T09 §8 |  |
| NP-0838 | Edit fill dialog | -- | CD-1331 | core | plan D02 T09 §8 |  |
| NP-0839 | Fill transform with free scale and skew | -- | CD-1345, CD-1346 | core | plan D02 T09 §8 |  |
| NP-0840 | Drop palette colors on fill handles | -- | CD-1350 | core | plan D02 T09 §8 |  |
| NP-0841 | Save fill as new | -- | CD-1351 | core | plan D02 T09 §8 |  |
| NP-0842 | Default fill for new objects | -- | CD-1383 | core | plan D02 T09 §8 |  |
| NP-0843 | No fill | -- | CD-1384 | core | plan D02 T09 §8 |  |
| NP-0844 | Copy fill from another object | -- | CD-1385 | core | plan D02 T09 §8 |  |
| NP-0845 | Mesh tool | AI-0130 | CD-1328, CD-1370 | core | plan D02 T09 §9 | toolbox rows of one tool |
| NP-0846 | Mesh object | AI-0502 | -- | core | plan D02 T09 §9 |  |
| NP-0847 | Create Gradient Mesh dialog | AI-0503 | -- | core | plan D02 T09 §9 |  |
| NP-0848 | Mesh editing: add, delete, move, and shape points | AI-0504 | CD-1372, CD-1373 | core | plan D02 T09 §9 |  |
| NP-0849 | Mesh transparency | AI-0505 | CD-1377 | core | plan D02 T09 §9 |  |
| NP-0850 | Expand gradient to mesh | AI-0506 | -- | core | plan D02 T09 §9 |  |
| NP-0851 | Convert mesh to paths | AI-0507 | -- | core | plan D02 T09 §9 |  |
| NP-0852 | Mesh grid size and default rows and columns | -- | CD-1371, CD-2885 | core | plan D02 T09 §9 |  |
| NP-0853 | Mesh node selection: rectangular or freehand | -- | CD-1374 | core | plan D02 T09 §9 |  |
| NP-0854 | Color mesh patches and nodes | -- | CD-1375 | core | plan D02 T09 §9 |  |
| NP-0855 | Smooth mesh color | -- | CD-1376 | core | plan D02 T09 §9 |  |
| NP-0856 | Clear mesh | -- | CD-1378 | core | plan D02 T09 §9 |  |
| NP-0857 | Make pattern from selection | AI-0508, AI-0515 | CD-1365, CD-1400 | core | plan D02 T09 §10 | legacy Define Pattern and Corel Create Pattern Fill are the same capability |
| NP-0858 | Pattern editing mode | AI-0509 | -- | core | plan D02 T09 §10 |  |
| NP-0859 | Pattern tile edge color | AI-0510 | -- | core | plan D02 T09 §10 |  |
| NP-0860 | Pattern Options panel | AI-0511 | -- | core | plan D02 T09 §10 |  |
| NP-0861 | Pattern tile types: grid, brick, hex | AI-0512 | -- | core | plan D02 T09 §10 |  |
| NP-0862 | Pattern tile tool | AI-0513 | -- | core | plan D02 T09 §10 |  |
| NP-0863 | Save a copy, done, or cancel pattern editing | AI-0514 | -- | core | plan D02 T09 §10 |  |
| NP-0864 | Transform patterns with or without the object | AI-0516 | CD-1360 | core | plan D02 T09 §10 |  |
| NP-0865 | Vector pattern fill | -- | CD-1352 | core | plan D02 T09 §10 |  |
| NP-0866 | Bitmap pattern fill | -- | CD-1353 | core | plan D02 T09 §10 |  |
| NP-0867 | New pattern source from document area or file | -- | CD-1354, CD-1355 | core | plan D02 T09 §10 |  |
| NP-0868 | Mirror pattern tiles | -- | CD-1356 | core | plan D02 T09 §10 |  |
| NP-0869 | Pattern tile size | -- | CD-1357 | core | plan D02 T09 §10 |  |
| NP-0870 | Pattern origin, skew, and rotate | -- | CD-1358 | core | plan D02 T09 §10 |  |
| NP-0871 | Pattern row or column offset | -- | CD-1359 | core | plan D02 T09 §10 |  |
| NP-0872 | Bitmap pattern seamless blend and edge match | -- | CD-1361, CD-1362 | core | plan D02 T09 §10 |  |
| NP-0873 | Bitmap pattern brightness, luminance, and color | -- | CD-1363 | core | plan D02 T09 §10 |  |
| NP-0874 | Two-color pattern fill | -- | CD-1364 | core | plan D02 T09 §10 |  |
| NP-0875 | Fill picker with thumbnails and resize | -- | CD-1336, CD-1394 | core | plan D02 T09 §11 |  |
| NP-0876 | Texture fill | -- | CD-1366 | core | plan D02 T09 §11 | Nodus procedural textures, not Corel texture libraries |
| NP-0877 | Texture parameters | -- | CD-1367 | core | plan D02 T09 §11 |  |
| NP-0878 | Texture resolution and tile size | -- | CD-1368 | core | plan D02 T09 §11 |  |
| NP-0879 | Procedural fill (PostScript fill equivalent) | -- | CD-1369 | core | plan D02 T09 §11 | Nodus procedural patterns replace PostScript code fills |
| NP-0880 | Fill picker content source | -- | CD-1386 | core | plan D02 T09 §11 |  |
| NP-0881 | Fill search | -- | CD-1387 | core | plan D02 T09 §11 |  |
| NP-0882 | Browse fills recursively | -- | CD-1388 | core | plan D02 T09 §11 |  |
| NP-0883 | Reindex fill folder | -- | CD-1389 | core | plan D02 T09 §11 |  |
| NP-0884 | Filter fills by category | -- | CD-1390 | core | plan D02 T09 §11 |  |
| NP-0885 | Sort fills | -- | CD-1391 | core | plan D02 T09 §11 |  |
| NP-0886 | Fill folder aliases and pack management | -- | CD-1393, CD-1395 | core | plan D02 T09 §11 |  |
| NP-0887 | Favorite fills | -- | CD-1396 | core | plan D02 T09 §11 |  |
| NP-0888 | Fill properties and tags | -- | CD-1397 | core | plan D02 T09 §11 |  |
| NP-0889 | Delete fill | -- | CD-1398 | core | plan D02 T09 §11 |  |
| NP-0890 | Save custom fills and transparencies to a fill file | -- | CD-1399, CD-2652 | format | plan D02 T09 §11 | Nodus fill file is SVG with nodus metadata; Corel .fill import is not planned (undocumented binary) |
| NP-0891 | Texture transparency | -- | CD-1422 | core | plan D02 T09 §11 |  |

## Strokes and outlines

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0892 | Stroke panel and Outline Pen dialog | AI-0524 | CD-1456, CD-1475 | core | plan D02 T09 §12 |  |
| NP-0893 | Stroke weight and units | AI-0525 | CD-1457 | core | plan D02 T09 §12 |  |
| NP-0894 | Stroke caps: butt, round, projecting | AI-0526 | CD-1462, CD-1463, CD-1464 | core | plan D02 T09 §12 |  |
| NP-0895 | Corner joins and miter limit | AI-0527 | CD-1459, CD-1460, CD-1461, CD-1468 | core | plan D02 T09 §12 |  |
| NP-0896 | Align stroke: center, inside, outside | AI-0528 | CD-1469, CD-1470, CD-1471 | core | plan D02 T09 §12 |  |
| NP-0897 | Dashed lines and line style presets | AI-0529 | CD-1458 | core | plan D02 T09 §12 |  |
| NP-0898 | Dash alignment: default, align to corners, fixed | AI-0530 | CD-1465, CD-1466, CD-1467 | core | plan D02 T09 §12 |  |
| NP-0899 | Start and end arrowheads with swap | AI-0531 | CD-1481, CD-1483 | core | plan D02 T09 §12 |  |
| NP-0900 | Arrowhead scale, alignment, and attributes | AI-0532 | CD-1482 | core | plan D02 T09 §12 |  |
| NP-0901 | Custom arrowheads and arrowhead presets | AI-0533 | CD-1484, CD-1485, CD-1498 | core | plan D02 T09 §12 | create from object is one capability in two menus |
| NP-0902 | Remove fill or stroke (none) | AI-0536 | CD-1495 | core | plan D02 T09 §12 |  |
| NP-0903 | Outline tool flyout | -- | CD-1454 | core | plan D02 T09 §12 |  |
| NP-0904 | Outline color by right-clicking a swatch | -- | CD-1455 | core | plan D02 T09 §12 |  |
| NP-0905 | Outline behind fill | -- | CD-1472 | core | plan D02 T09 §12 |  |
| NP-0906 | Scale outline with object | -- | CD-1473 | core | plan D02 T09 §12 |  |
| NP-0907 | Edit line style dialog | -- | CD-1476 | core | plan D02 T09 §12 |  |
| NP-0908 | Calligraphic outline: stretch and tilt nib | -- | CD-1477, CD-1478 | core | plan D02 T09 §12 |  |
| NP-0909 | Default outline properties for new objects | -- | CD-1479 | core | plan D02 T09 §12 |  |
| NP-0910 | Convert outline to object | -- | CD-1494 | core | plan D02 T09 §12 | extends the existing Stroke to Path command |
| NP-0911 | Find and replace outline width, scaling, and overprint | -- | CD-1496 | core | plan D02 T09 §12 |  |
| NP-0912 | Width tool and variable outline tool | AI-0278 | CD-1453 | core | plan D02 T09 §13 |  |
| NP-0913 | Width point side 1, side 2, lock ratio, and total | AI-0279 | CD-1487 | core | plan D02 T09 §13 |  |
| NP-0914 | Width tool modifiers and multi-node edit | AI-0280 | CD-1488 | core | plan D02 T09 §13 |  |
| NP-0915 | Variable width profiles: save, apply, flip | AI-0281, AI-0534 | -- | core | plan D02 T09 §13 |  |
| NP-0916 | Width nodes: add, remove, clear | -- | CD-1486, CD-1492 | core | plan D02 T09 §13 |  |
| NP-0917 | Copy variable outline | -- | CD-1489 | core | plan D02 T09 §13 |  |
| NP-0918 | Width node position along the path | -- | CD-1490 | core | plan D02 T09 §13 |  |
| NP-0919 | Scale widths with stroke weight | -- | CD-1491 | core | plan D02 T09 §13 |  |

## Brushes

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0920 | Brushes panel | AI-0537 | -- | core | plan D02 T09 §16 | promoted from backlog B-010 |
| NP-0921 | Art brush | AI-0540 | -- | core | plan D02 T09 §16 |  |
| NP-0922 | Pattern brush | AI-0545 | -- | core | plan D02 T09 §16 | promoted from backlog B-010 |
| NP-0923 | Pattern brush auto corners | AI-0546 | -- | core | plan D02 T09 §16 |  |
| NP-0924 | Pattern brush fit: stretch, add space, approximate | AI-0547 | -- | core | plan D02 T09 §16 |  |
| NP-0925 | Brush colorization: none, tints, tints and shades, hue shift | AI-0548 | -- | core | plan D02 T09 §16 |  |
| NP-0926 | Brush options and options of selected object | AI-0549 | -- | core | plan D02 T09 §16 |  |
| NP-0927 | Remove brush stroke | AI-0550 | -- | core | plan D02 T09 §16 |  |
| NP-0928 | Convert brush strokes to outlines | AI-0554 | -- | core | plan D02 T09 §16 |  |
| NP-0929 | Draw paths with the current brush | AI-0555 | -- | core | plan D02 T09 §16 |  |
| NP-0930 | Artistic media tool | -- | CD-745 | core | plan D02 T09 §16 |  |
| NP-0931 | Artistic media preset strokes | -- | CD-751, CD-793 | core | plan D02 T09 §16 |  |
| NP-0932 | Vector brush mode | -- | CD-796, CD-808 | core | plan D02 T09 §16 |  |
| NP-0933 | Brush category list | -- | CD-797 | core | plan D02 T09 §16 |  |
| NP-0934 | Browse for a brushstroke file | -- | CD-801 | core | plan D02 T09 §16 |  |
| NP-0935 | Save and delete custom brushstrokes | -- | CD-802, CD-803 | core | plan D02 T09 §16 |  |
| NP-0936 | Paintbrush tool | AI-0108 | -- | core | plan D02 T09 §17 |  |
| NP-0937 | Paintbrush tool options | AI-0109 | -- | core | plan D02 T09 §17 |  |
| NP-0938 | Blob Brush tool | AI-0110 | -- | core | plan D02 T09 §17 |  |
| NP-0939 | Blob Brush tool options | AI-0111 | -- | core | plan D02 T09 §17 |  |
| NP-0940 | Calligraphic brush and calligraphic mode | AI-0538 | CD-746, CD-747, CD-795 | core | plan D02 T09 §17 |  |
| NP-0941 | Scatter brush and sprayer mode | AI-0539 | CD-753, CD-794 | core | plan D02 T09 §17 |  |
| NP-0942 | Image brush | AI-0541 | -- | core | plan D02 T09 §17 |  |
| NP-0943 | Brush stroke width | -- | CD-748, CD-798 | core | plan D02 T09 §17 |  |
| NP-0944 | Brush freehand smoothing | -- | CD-749, CD-799 | core | plan D02 T09 §17 |  |
| NP-0945 | Scale brush stroke with object | -- | CD-750, CD-800 | core | plan D02 T09 §17 |  |
| NP-0946 | Sprayer objects per dab and spacing | -- | CD-754 | core | plan D02 T09 §17 |  |
| NP-0947 | Sprayer spray order | -- | CD-755 | core | plan D02 T09 §17 |  |
| NP-0948 | Sprayer size and size progression | -- | CD-756 | core | plan D02 T09 §17 |  |
| NP-0949 | Sprayer rotation | -- | CD-757 | core | plan D02 T09 §17 |  |
| NP-0950 | Sprayer offset | -- | CD-758 | core | plan D02 T09 §17 |  |
| NP-0951 | Create custom spray pattern | -- | CD-759 | core | plan D02 T09 §17 |  |
| NP-0952 | Pressure-sensitive brush input | -- | CD-760, CD-805 | core | plan D02 T09 §17 |  |
| NP-0953 | Pen tilt and bearing for brushes | -- | CD-761, CD-806, CD-807 | core | plan D02 T09 §17 |  |
| NP-0954 | Expression brush mode | -- | CD-804 | core | plan D02 T09 §17 |  |
| NP-0955 | Bristle brush | AI-0542 | -- | core | plan D02 T09 §18 |  |
| NP-0956 | Bristle brush shapes | AI-0543 | -- | core | plan D02 T09 §18 |  |
| NP-0957 | Bristle stroke rasterization warning | AI-0544 | -- | core | plan D02 T09 §18 |  |
| NP-0958 | Duplicate, delete, and select unused brushes | AI-0551 | -- | core | plan D02 T09 §18 |  |
| NP-0959 | Brush libraries | AI-0552 | -- | core | plan D02 T09 §18 |  |
| NP-0960 | Save brush library | AI-0553 | -- | core | plan D02 T09 §18 |  |
| NP-0961 | Painterly brush tool | -- | CD-744 | core | plan D02 T09 §18 | pixel marks rendered by the Photon.Core pixel engine |
| NP-0962 | Artistic Media docker | -- | CD-752, CD-809, CD-810 | core | plan D02 T09 §18 | menu, docker, and inspector rows of one docker |
| NP-0963 | Painterly brushstroke model (vector path, pixel marks) | -- | CD-762 | core | plan D02 T09 §18 |  |
| NP-0964 | Painterly stylus dynamics | -- | CD-763 | core | plan D02 T09 §18 |  |
| NP-0965 | Painterly brush picker | -- | CD-764 | core | plan D02 T09 §18 |  |
| NP-0966 | Painterly brush categories | -- | CD-765 | core | plan D02 T09 §18 | Nodus ships its own brush set; no Corel content |
| NP-0967 | Brush search | -- | CD-766 | core | plan D02 T09 §18 |  |
| NP-0968 | Brush favorites | -- | CD-767 | core | plan D02 T09 §18 |  |
| NP-0969 | Brush media tray | -- | CD-768 | core | plan D02 T09 §18 |  |
| NP-0970 | Apply a brushstroke to existing objects | -- | CD-770 | core | plan D02 T09 §18 |  |
| NP-0971 | Clear brushstroke | -- | CD-771 | core | plan D02 T09 §18 |  |
| NP-0972 | Brushstroke bounding box toggle | -- | CD-772 | core | plan D02 T09 §18 |  |
| NP-0973 | Painterly brush properties tab | -- | CD-773 | core | plan D02 T09 §18 |  |
| NP-0974 | Brushstroke color and default brushstroke color | -- | CD-774 | core | plan D02 T09 §18 |  |
| NP-0975 | Painterly brush size | -- | CD-775 | core | plan D02 T09 §18 |  |
| NP-0976 | Brushstroke scaling rule | -- | CD-776 | core | plan D02 T09 §18 |  |
| NP-0977 | Brush paint transparency | -- | CD-777 | core | plan D02 T09 §18 |  |
| NP-0978 | Brush paper texture and strength | -- | CD-778, CD-779 | core | plan D02 T09 §18 |  |
| NP-0979 | Brush density | -- | CD-780 | core | plan D02 T09 §18 |  |
| NP-0980 | Brush glow | -- | CD-781 | core | plan D02 T09 §18 |  |
| NP-0981 | Painterly brush smoothing | -- | CD-782 | core | plan D02 T09 §18 |  |
| NP-0982 | Simulate pen pressure and tilt with a mouse | -- | CD-783, CD-784, CD-785 | core | plan D02 T09 §18 |  |
| NP-0983 | Reset brush to defaults | -- | CD-786 | core | plan D02 T09 §18 |  |
| NP-0984 | Painterly brush cursor | -- | CD-787 | core | plan D02 T09 §18 |  |
| NP-0985 | Brush-specific property bar | -- | CD-788 | core | plan D02 T09 §18 |  |
| NP-0986 | Brushstrokes in the Layers panel (icon, lock, rename) | -- | CD-789 | core | plan D02 T09 §18 |  |
| NP-0987 | Edit painterly vector curves | -- | CD-790 | core | plan D02 T09 §18 |  |
| NP-0988 | Painterly compatibility with destructive operations | -- | CD-791 | core | plan D02 T09 §18 |  |
| NP-0989 | Unavailable brush indicator | -- | CD-792 | core | plan D02 T09 §18 |  |

## Transparency and blending

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-0990 | Transparency panel | AI-0556 | -- | core | plan D02 T09 §19 |  |
| NP-0991 | Opacity and uniform transparency | AI-0557 | CD-1406 | core | plan D02 T09 §19 |  |
| NP-0992 | Blend mode: Normal | AI-0558 | CD-1426 | core | plan D02 T09 §19 |  |
| NP-0993 | Blend mode: Darken (If darker) | AI-0559 | CD-1433 | core | plan D02 T09 §19 | Corel If darker is the same result as Darken |
| NP-0994 | Blend mode: Multiply | AI-0560 | CD-1430 | core | plan D02 T09 §19 |  |
| NP-0995 | Blend mode: Color Burn | AI-0561 | CD-1449 | core | plan D02 T09 §19 |  |
| NP-0996 | Blend mode: Lighten (If lighter) | AI-0562 | CD-1432 | core | plan D02 T09 §19 | Corel If lighter is the same result as Lighten |
| NP-0997 | Blend mode: Screen | AI-0563 | CD-1444 | core | plan D02 T09 §19 |  |
| NP-0998 | Blend mode: Color Dodge | AI-0564 | CD-1448 | core | plan D02 T09 §19 |  |
| NP-0999 | Blend mode: Overlay | AI-0565 | CD-1445 | core | plan D02 T09 §19 |  |
| NP-1000 | Blend mode: Soft Light | AI-0566 | CD-1446 | core | plan D02 T09 §19 |  |
| NP-1001 | Blend mode: Hard Light | AI-0567 | CD-1447 | core | plan D02 T09 §19 |  |
| NP-1002 | Blend mode: Difference | AI-0568 | CD-1429 | core | plan D02 T09 §19 |  |
| NP-1003 | Blend mode: Exclusion | AI-0569 | CD-1450 | core | plan D02 T09 §19 |  |
| NP-1004 | Blend mode: Hue | AI-0570 | CD-1436 | core | plan D02 T09 §19 |  |
| NP-1005 | Blend mode: Saturation | AI-0571 | CD-1437 | core | plan D02 T09 §19 |  |
| NP-1006 | Blend mode: Color | AI-0572 | CD-1435 | core | plan D02 T09 §19 |  |
| NP-1007 | Blend mode: Luminosity (Lightness) | AI-0573 | CD-1438 | core | plan D02 T09 §19 |  |
| NP-1008 | Transparency on fill only or outline only | -- | CD-1407 | core | plan D02 T09 §19 |  |
| NP-1009 | Copy transparency | -- | CD-1423 | core | plan D02 T09 §19 |  |
| NP-1010 | No transparency | -- | CD-1425 | core | plan D02 T09 §19 |  |
| NP-1011 | Merge mode: Add | -- | CD-1427 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1012 | Merge mode: Subtract | -- | CD-1428 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1013 | Merge mode: Divide | -- | CD-1431 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1014 | Merge mode: Texturize | -- | CD-1434 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1015 | Merge mode: Invert | -- | CD-1439 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1016 | Merge modes: logical AND, OR, XOR | -- | CD-1440, CD-1441, CD-1442 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1017 | Merge mode: Behind | -- | CD-1443 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1018 | Merge mode: red, green, or blue channel | -- | CD-1451 | core | plan D02 T09 §19 | nodus: attribute with a flattened image fallback |
| NP-1019 | Opacity mask: make and release | AI-0574, AI-0575 | -- | core | plan D02 T09 §20 |  |
| NP-1020 | Opacity mask: clip and invert | AI-0576 | -- | core | plan D02 T09 §20 |  |
| NP-1021 | Opacity mask: disable, unlink, and edit mask | AI-0577 | -- | core | plan D02 T09 §20 |  |
| NP-1022 | New opacity masks are clipping or inverted | AI-0578 | -- | core | plan D02 T09 §20 |  |
| NP-1023 | Isolate blending | AI-0579 | -- | core | plan D02 T09 §20 |  |
| NP-1024 | Knockout group and opacity-defined knockout | AI-0580, AI-0581 | -- | core | plan D02 T09 §20 |  |
| NP-1025 | Transparency tool | -- | CD-1401 | core | plan D02 T09 §20 |  |
| NP-1026 | Feather | -- | CD-1402 | core | plan D02 T09 §20 | blur through the Photon.Core pixel engine |
| NP-1027 | Feather profiles: linear, curved, Gaussian | -- | CD-1403, CD-1404, CD-1405 | core | plan D02 T09 §20 |  |
| NP-1028 | Fountain transparency: linear, elliptical, conical, rectangular | -- | CD-1408, CD-1409, CD-1410, CD-1411 | core | plan D02 T09 §20 |  |
| NP-1029 | Transparency nodes and midpoint | -- | CD-1412 | core | plan D02 T09 §20 |  |
| NP-1030 | Transparency repeat, mirror, and reverse | -- | CD-1413 | core | plan D02 T09 §20 |  |
| NP-1031 | Transparency steps, acceleration, and smoothing | -- | CD-1414 | core | plan D02 T09 §20 |  |
| NP-1032 | Transparency transform | -- | CD-1415 | core | plan D02 T09 §20 |  |
| NP-1033 | Transparency picker | -- | CD-1416 | core | plan D02 T09 §20 |  |
| NP-1034 | Drop palette colors on transparency nodes | -- | CD-1417 | core | plan D02 T09 §20 |  |
| NP-1035 | Pattern transparency: vector, bitmap, two-color | -- | CD-1418, CD-1419, CD-1420 | core | plan D02 T09 §20 |  |
| NP-1036 | Pattern transparency tile options | -- | CD-1421 | core | plan D02 T09 §20 |  |
| NP-1037 | Freeze transparency | -- | CD-1424 | core | plan D02 T09 §20 |  |

## Appearance and styles

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1038 | Expand Appearance | AI-0214 | -- | core | plan D02 T09 §14 |  |
| NP-1039 | Multiple fills and strokes | AI-0535, AI-0626 | -- | core | plan D02 T09 §14 | promoted from backlog B-003 |
| NP-1040 | Appearance panel | AI-0625 | -- | core | plan D02 T09 §14 | promoted from backlog B-003 |
| NP-1041 | Add new effect from the Appearance panel | AI-0627 | -- | core | plan D02 T09 §14 |  |
| NP-1042 | Reorder, duplicate, delete, and hide appearance items | AI-0628 | -- | core | plan D02 T09 §14 |  |
| NP-1043 | Clear appearance | AI-0629 | -- | core | plan D02 T09 §14 |  |
| NP-1044 | Reduce to basic appearance | AI-0630 | -- | core | plan D02 T09 §14 |  |
| NP-1045 | New art has basic appearance | AI-0631 | -- | core | plan D02 T09 §14 |  |
| NP-1046 | Appearance targeting: object, group, layer, fill, stroke | AI-0632 | -- | core | plan D02 T09 §14 |  |
| NP-1047 | Appearance on layers | AI-0633 | -- | core | plan D02 T09 §14 |  |
| NP-1048 | Edit an effect from its appearance row | AI-0634 | -- | core | plan D02 T09 §14 |  |
| NP-1049 | Apply last effect | AI-0642 | -- | core | plan D02 T09 §14 |  |
| NP-1050 | Reopen last effect dialog | AI-0643 | -- | core | plan D02 T09 §14 |  |
| NP-1051 | Copy properties from another object | -- | CD-542 | core | plan D02 T09 §14 |  |
| NP-1052 | Text fill and outline from the palette | -- | CD-1021, CD-1022 | core | plan D02 T09 §14 |  |
| NP-1053 | Copy outline or fill by right-drag | -- | CD-1493 | core | plan D02 T09 §14 |  |
| NP-1054 | Style presets quick actions (retro, neon, old school text) | AI-0425 | -- | core | plan D02 T09 §15 | shipped as graphic styles in the Nodus style library |
| NP-1055 | Graphic Styles panel | AI-0635 | -- | core | plan D02 T09 §15 |  |
| NP-1056 | New, duplicate, rename, delete, and merge styles | AI-0636 | CD-1618 | core | plan D02 T09 §15 |  |
| NP-1057 | Break link to style | AI-0637 | CD-1641 | core | plan D02 T09 §15 |  |
| NP-1058 | Redefine style from the selection (apply to style) | AI-0638 | CD-1626 | core | plan D02 T09 §15 |  |
| NP-1059 | Alt-click to add a style to the appearance | AI-0639 | -- | core | plan D02 T09 §15 |  |
| NP-1060 | Override character color and style preview options | AI-0640 | -- | core | plan D02 T09 §15 |  |
| NP-1061 | Graphic style libraries | AI-0641 | -- | core | plan D02 T09 §15 |  |
| NP-1062 | Object Styles docker | -- | CD-1606, CD-1685 | core | plan D02 T09 §15 | docker and inspector rows of one docker |
| NP-1063 | Style types: outline, fill, and text frame | -- | CD-1607, CD-1608 | core | plan D02 T09 §15 |  |
| NP-1064 | New style from object | -- | CD-1612 | core | plan D02 T09 §15 |  |
| NP-1065 | Style set from object, selection, or drag | -- | CD-1613, CD-1614, CD-1615 | core | plan D02 T09 §15 |  |
| NP-1066 | Define style or style set from scratch | -- | CD-1616, CD-1617 | core | plan D02 T09 §15 |  |
| NP-1067 | Child styles and child style sets | -- | CD-1619 | core | plan D02 T09 §15 |  |
| NP-1068 | Apply style to selection | -- | CD-1620, CD-1623 | core | plan D02 T09 §15 |  |
| NP-1069 | Style hover preview | -- | CD-1621 | core | plan D02 T09 §15 |  |
| NP-1070 | Style source indicators | -- | CD-1622 | core | plan D02 T09 §15 |  |
| NP-1071 | Edit style in the docker | -- | CD-1624 | core | plan D02 T09 §15 |  |
| NP-1072 | Add or remove style types in a style set | -- | CD-1625 | core | plan D02 T09 §15 |  |
| NP-1073 | Copy properties into a style | -- | CD-1627 | core | plan D02 T09 §15 |  |
| NP-1074 | Style override and revert to style | -- | CD-1628, CD-1629 | core | plan D02 T09 §15 |  |
| NP-1075 | Default object properties | -- | CD-1630, CD-1636 | core | plan D02 T09 §15 |  |
| NP-1076 | Change Document Defaults dialog | -- | CD-1631 | core | plan D02 T09 §15 |  |
| NP-1077 | Set or revert new-document defaults | -- | CD-1632, CD-1633, CD-1635 | core | plan D02 T09 §15 |  |
| NP-1078 | Update defaults when editing objects | -- | CD-1634 | core | plan D02 T09 §15 |  |
| NP-1079 | Export and import style sheets | -- | CD-1637, CD-1638 | core | plan D02 T09 §15 | Nodus style sheet is SVG with nodus metadata; .cdss is not read |
| NP-1080 | Keyboard shortcut for a style | -- | CD-1639 | core | plan D02 T09 §15 |  |
| NP-1081 | Select objects using a style | -- | CD-1640 | core | plan D02 T09 §15 |  |

## Symbols

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1082 | Replace symbol | AI-0609 | -- | core | plan D02 T09 §21 |  |
| NP-1083 | Dynamic symbols and instance overrides | AI-0612 | CD-1728 | core | plan D02 T09 §21 |  |
| NP-1084 | Reset transformation, select instances, select unused symbols | AI-0613 | -- | core | plan D02 T09 §21 |  |
| NP-1085 | 9-slice scaling | AI-0614 | -- | core | plan D02 T09 §21 |  |
| NP-1086 | Symbol registration point | AI-0615 | -- | core | plan D02 T09 §21 |  |
| NP-1087 | Symbol libraries: open and save | AI-0616 | CD-1733 | core | plan D02 T09 §21 | a Nodus symbol library is an SVG file of symbol definitions |
| NP-1088 | Clone (linked copy with overrides) | -- | CD-432 | core | plan D02 T09 §21 |  |
| NP-1089 | Select master and select clones | -- | CD-433, CD-434 | core | plan D02 T09 §21 |  |
| NP-1090 | Revert clone to master | -- | CD-435 | core | plan D02 T09 §21 |  |
| NP-1091 | Link a symbol library to the document | -- | CD-1687 | core | plan D02 T09 §21 |  |
| NP-1092 | Edit a linked symbol library | -- | CD-1688 | core | plan D02 T09 §21 |  |
| NP-1093 | Sync linked symbol libraries | -- | CD-1689 | core | plan D02 T09 §21 |  |
| NP-1094 | Remove a linked library from the document | -- | CD-1690 | core | plan D02 T09 §21 |  |
| NP-1095 | Restore a broken library link and its indicator | -- | CD-1691, CD-1692 | core | plan D02 T09 §21 |  |
| NP-1096 | Nested symbols | -- | CD-1720 | core | plan D02 T09 §21 |  |
| NP-1097 | Rename symbol | -- | CD-1721 | core | plan D02 T09 §21 |  |
| NP-1098 | Break link: make a linked symbol internal | -- | CD-1722, CD-1744 | core | plan D02 T09 §21 |  |
| NP-1099 | Delete symbol | -- | CD-1723 | core | plan D02 T09 §21 |  |
| NP-1100 | Delete unused symbols | -- | CD-1724 | core | plan D02 T09 §21 |  |
| NP-1101 | Search symbols | -- | CD-1725 | core | plan D02 T09 §21 |  |
| NP-1102 | Scale symbols to world units | -- | CD-1727 | core | plan D02 T09 §21 |  |
| NP-1103 | Revert symbol instance to objects | -- | CD-1729 | core | plan D02 T09 §21 |  |
| NP-1104 | Import symbol library folders (local or network) | -- | CD-1730, CD-1735 | core | plan D02 T09 §21 |  |
| NP-1105 | Copy symbols between drawings and libraries | -- | CD-1731, CD-1736 | core | plan D02 T09 §21 |  |
| NP-1106 | Corel Symbol Library (CSL) read and write | -- | CD-1732, CD-2581 | format | plan D02 T09 §21 | CSL is CDR-based; read and written through the Nodus CDR reader and writer |
| NP-1107 | Unsupported symbol source objects refused by name | -- | CD-1737 | core | plan D02 T09 §21 |  |
| NP-1108 | Symbol Sprayer tool | AI-0125 | -- | core | plan D02 T09 §22 |  |
| NP-1109 | Symbol Shifter tool | AI-0617 | -- | core | plan D02 T09 §22 |  |
| NP-1110 | Symbol Scruncher tool | AI-0618 | -- | core | plan D02 T09 §22 |  |
| NP-1111 | Symbol Sizer tool | AI-0619 | -- | core | plan D02 T09 §22 |  |
| NP-1112 | Symbol Spinner tool | AI-0620 | -- | core | plan D02 T09 §22 |  |
| NP-1113 | Symbol Stainer tool | AI-0621 | -- | core | plan D02 T09 §22 |  |
| NP-1114 | Symbol Screener tool | AI-0622 | -- | core | plan D02 T09 §22 |  |
| NP-1115 | Symbol Styler tool | AI-0623 | -- | core | plan D02 T09 §22 |  |
| NP-1116 | Symbolism tools options | AI-0624 | -- | core | plan D02 T09 §22 |  |
| NP-1117 | Symbols panel | AI-0606 | CD-1717, CD-1745, CD-1747 | core | shipped-scope D02 T06 §11 |  |
| NP-1118 | Create new symbol | AI-0607 | CD-1718, CD-1741 | core | shipped-scope D02 T06 §11 |  |
| NP-1119 | Place symbol instance | AI-0608 | CD-1726 | core | shipped-scope D02 T06 §11 |  |
| NP-1120 | Break link to symbol | AI-0610 | -- | core | shipped-scope D02 T06 §11 |  |
| NP-1121 | Edit and finish editing symbol | AI-0611 | CD-1719, CD-1742, CD-1743 | core | shipped-scope D02 T06 §11 |  |
| NP-1122 | Asset content types | -- | CD-259 | core | shipped-scope D02 T06 §11 |  |
| NP-1123 | Assets browser with local and network folders | -- | CD-260, CD-261, CD-264, CD-265, CD-266, CD-267, CD-268, CD-269, CD-1746 | core | shipped-scope D02 T06 §11 |  |
| NP-1124 | Asset search, filter, and sort | -- | CD-270, CD-271, CD-272 | core | shipped-scope D02 T06 §11 |  |
| NP-1125 | Open asset in associated app | -- | CD-275 | core | shipped-scope D02 T06 §11 |  |
| NP-1126 | Asset tags, categories, and favorites | -- | CD-276 | core | shipped-scope D02 T06 §11 |  |
| NP-1127 | Tray for collecting content across documents | -- | CD-277, CD-278, CD-581 | core | shipped-scope D02 T06 §11 |  |
| NP-1128 | Insert asset into the document | -- | CD-2462 | core | shipped-scope D02 T06 §11 |  |

## Type

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1129 | Text anti-aliasing modes (none, sharp, crisp, strong) | AI-0375 | -- | core | plan D02 T10 §1 | maps to SkiaSharp edging and hinting per text object |
| NP-1130 | Fractional glyph widths and system layout toggle | AI-0377 | -- | core | plan D02 T10 §1 |  |
| NP-1131 | Supported font formats: OpenType, TrueType, variable, SVG and color fonts, Type 1 detection | AI-0411 | -- | core | plan D02 T10 §1 | Adobe Fonts sync excluded (cloud); Type 1 is detected and refused by name because Windows and Skia no longer render it |
| NP-1132 | Missing glyph protection and font fallback | AI-1148 | -- | core | plan D02 T10 §1 |  |
| NP-1133 | Inline IME input for non-Latin text | AI-1149 | -- | core | plan D02 T10 §1 |  |
| NP-1134 | Type tool: click for point text, drag for area text, click a path for path text | AI-0319 | CD-947 | core | plan D02 T10 §2 |  |
| NP-1135 | Point (artistic) and area (paragraph) text object types | AI-0326 | CD-948 | core | plan D02 T10 §2 |  |
| NP-1136 | Convert between point and area text | AI-0328 | CD-955, CD-956 | core | plan D02 T10 §2 |  |
| NP-1137 | Update legacy text to the current engine | AI-0363 | CD-1020 | core | plan D02 T10 §2 | re-lays out imported plain SVG, AI, and CDR text with the shaping engine |
| NP-1138 | Break text apart into lines, words, and characters | -- | CD-551, CD-552 | core | plan D02 T10 §2 |  |
| NP-1139 | Hyperlink on a text run | -- | CD-954 | core | plan D02 T10 §2 |  |
| NP-1140 | Select a text object versus characters | -- | CD-988 | core | plan D02 T10 §2 |  |
| NP-1141 | Edit Text dialog | -- | CD-993, CD-1061 | core | plan D02 T10 §2 |  |
| NP-1142 | Drag text within and between text objects (move, copy here) | -- | CD-1002, CD-1003 | core | plan D02 T10 §2 |  |
| NP-1143 | Inline graphics embedded in text | -- | CD-1019 | core | plan D02 T10 §2 |  |
| NP-1144 | Per-character text fill (uniform, gradient, pattern) | -- | CD-1023 | core | plan D02 T10 §2 |  |
| NP-1145 | Text background highlight fill | -- | CD-1024 | core | plan D02 T10 §2 |  |
| NP-1146 | Per-character text outline | -- | CD-1025 | core | plan D02 T10 §2 |  |
| NP-1147 | Touch type: move, scale, and rotate individual characters | AI-0325 | CD-1004 | core | plan D02 T10 §4 |  |
| NP-1148 | Character panel (Text panel) | AI-0364 | CD-1059, CD-1081 | core | plan D02 T10 §4 |  |
| NP-1149 | Font family, style, and size | AI-0365 | CD-1096 | core | plan D02 T10 §4 |  |
| NP-1150 | Leading (line spacing) | AI-0366 | CD-1144 | core | plan D02 T10 §4 |  |
| NP-1151 | Kerning: auto, optical, metrics, manual, and range | AI-0367 | CD-1107 | core | plan D02 T10 §4 |  |
| NP-1152 | Tracking (character spacing) | AI-0368 | CD-1141 | core | plan D02 T10 §4 |  |
| NP-1153 | Horizontal and vertical character scale | AI-0369 | -- | core | plan D02 T10 §4 |  |
| NP-1154 | Baseline shift (vertical character offset) | AI-0370 | CD-996 | core | plan D02 T10 §4 |  |
| NP-1155 | Character rotation | AI-0371 | CD-997 | core | plan D02 T10 §4 |  |
| NP-1156 | All caps and small caps (auto, synthesized, all small caps, from caps) | AI-0372 | CD-1109, CD-1111, CD-1112, CD-1113, CD-1114 | core | plan D02 T10 §4 |  |
| NP-1157 | Underline and strikethrough styles | AI-0373 | CD-1104, CD-1105 | core | plan D02 T10 §4 |  |
| NP-1158 | Character language | AI-0374 | -- | core | plan D02 T10 §4 |  |
| NP-1159 | No Break | AI-0378 | -- | core | plan D02 T10 §4 |  |
| NP-1160 | Text keyboard shortcuts for size, leading, kerning, tracking, and baseline shift | AI-0421 | CD-1099 | core | plan D02 T10 §4 |  |
| NP-1161 | Type keyboard increments | AI-0422, AI-1143 | CD-1100 | core | plan D02 T10 §4 |  |
| NP-1162 | Horizontal character offset | -- | CD-995 | core | plan D02 T10 §4 |  |
| NP-1163 | Straighten text | -- | CD-998 | core | plan D02 T10 §4 |  |
| NP-1164 | Align characters to baseline | -- | CD-999 | core | plan D02 T10 §4 |  |
| NP-1165 | Mirror text by command or drag | -- | CD-1000, CD-1001 | core | plan D02 T10 §4 |  |
| NP-1166 | Bold, italic, and underline buttons | -- | CD-1098 | core | plan D02 T10 §4 |  |
| NP-1167 | Default text units | -- | CD-1101 | core | plan D02 T10 §4 |  |
| NP-1168 | Superscript and subscript (OpenType or synthesized) | -- | CD-1102, CD-1103 | core | plan D02 T10 §4 |  |
| NP-1169 | Overline | -- | CD-1106 | core | plan D02 T10 §4 |  |
| NP-1170 | Titling caps | -- | CD-1110 | core | plan D02 T10 §4 |  |
| NP-1171 | Capital spacing | -- | CD-1115 | core | plan D02 T10 §4 |  |
| NP-1172 | Word spacing | -- | CD-1142 | core | plan D02 T10 §4 |  |
| NP-1173 | Interactive character, word, and line spacing handles | -- | CD-1143, CD-1146 | core | plan D02 T10 §4 |  |
| NP-1174 | Vertical spacing units | -- | CD-1145 | core | plan D02 T10 §4 |  |
| NP-1175 | Snap to glyph (baseline, x-height, bounds, proximity, angular, anchor) | AI-0376, AI-0415, AI-0880 | -- | core | plan D02 T10 §5 |  |
| NP-1176 | OpenType panel | AI-0396 | CD-1116 | core | plan D02 T10 §5 |  |
| NP-1177 | Standard, discretionary, contextual, and historical ligatures | AI-0397 | CD-1133, CD-1134, CD-1135, CD-1136 | core | plan D02 T10 §5 |  |
| NP-1178 | Swash, stylistic, and titling alternates | AI-0398 | CD-1128, CD-1130 | core | plan D02 T10 §5 |  |
| NP-1179 | Fractions, numerators, denominators, and ordinals | AI-0399 | CD-1121, CD-1122, CD-1123, CD-1124, CD-1125 | core | plan D02 T10 §5 |  |
| NP-1180 | Stylistic sets | AI-0400 | CD-1129 | core | plan D02 T10 §5 |  |
| NP-1181 | Figure styles and OpenType position | AI-0401 | CD-1117, CD-1118, CD-1119, CD-1120 | core | plan D02 T10 §5 |  |
| NP-1182 | On-canvas alternates and the interactive OpenType indicator | AI-0402, AI-1154 | CD-1138 | core | plan D02 T10 §5 |  |
| NP-1183 | Glyphs panel | AI-0403 | CD-1060, CD-1082, CD-1085 | core | plan D02 T10 §5 |  |
| NP-1184 | Variable font axes and named instances | AI-0409 | CD-1139 | core | plan D02 T10 §5 |  |
| NP-1185 | Color, SVG, and emoji fonts | AI-0410 | -- | core | plan D02 T10 §5 |  |
| NP-1186 | Glyph guides | AI-0416 | -- | core | plan D02 T10 §5 |  |
| NP-1187 | Japanese glyph snapping (em box, ICF) | AI-0417 | -- | core | plan D02 T10 §5 |  |
| NP-1188 | Glyph filter by category, script, and OpenType feature | -- | CD-1086 | core | plan D02 T10 §5 |  |
| NP-1189 | Show all glyph alternates | -- | CD-1087 | core | plan D02 T10 §5 |  |
| NP-1190 | Glyph baseline preview | -- | CD-1088 | core | plan D02 T10 §5 |  |
| NP-1191 | Glyph info (name, ID, Unicode, feature) | -- | CD-1089 | core | plan D02 T10 §5 |  |
| NP-1192 | Glyph zoom | -- | CD-1090 | core | plan D02 T10 §5 |  |
| NP-1193 | Navigate glyphs by code or key | -- | CD-1091 | core | plan D02 T10 §5 |  |
| NP-1194 | Drag or copy a glyph | -- | CD-1092 | core | plan D02 T10 §5 |  |
| NP-1195 | Recently used glyphs | -- | CD-1093 | core | plan D02 T10 §5 |  |
| NP-1196 | Insert unmapped glyphs | -- | CD-1094 | core | plan D02 T10 §5 |  |
| NP-1197 | Slashed zero | -- | CD-1126 | core | plan D02 T10 §5 |  |
| NP-1198 | Ornaments | -- | CD-1127 | core | plan D02 T10 §5 |  |
| NP-1199 | Contextual alternates | -- | CD-1131 | core | plan D02 T10 §5 |  |
| NP-1200 | Case-sensitive forms | -- | CD-1132 | core | plan D02 T10 §5 |  |
| NP-1201 | Historical forms | -- | CD-1137 | core | plan D02 T10 §5 |  |
| NP-1202 | Optical margin alignment | AI-0352 | -- | core | plan D02 T10 §6 |  |
| NP-1203 | Paragraph panel | AI-0379 | -- | core | plan D02 T10 §6 |  |
| NP-1204 | Paragraph alignment and justification with last-line options | AI-0380, AI-0381 | CD-1044 | core | plan D02 T10 §6 |  |
| NP-1205 | Align towards or away from spine | AI-0382 | -- | core | plan D02 T10 §6 |  |
| NP-1206 | Left, right, and first-line indents | AI-0383 | CD-1051, CD-1052, CD-1053 | core | plan D02 T10 §6 |  |
| NP-1207 | Space before and after paragraphs | AI-0384 | CD-1147 | core | plan D02 T10 §6 |  |
| NP-1208 | Hyphenate toggle | AI-0385 | -- | core | plan D02 T10 §6 |  |
| NP-1209 | Hyphenation settings dialog | AI-0386 | CD-1080, CD-1148 | core | plan D02 T10 §6 |  |
| NP-1210 | Justification settings: word, letter, glyph scaling, auto leading | AI-0387 | -- | core | plan D02 T10 §6 |  |
| NP-1211 | Single-line and every-line composers | AI-0388 | -- | core | plan D02 T10 §6 |  |
| NP-1212 | Roman hanging punctuation | AI-0389 | -- | core | plan D02 T10 §6 |  |
| NP-1213 | Hyphenation language, exceptions, and custom optional hyphens | AI-1162 | CD-1070, CD-1155 | core | plan D02 T10 §6 | CD-1070 moved here from §11: it is the menu command that opens the same dialog |
| NP-1214 | Default text style for new text | -- | CD-1054 | core | plan D02 T10 §6 |  |
| NP-1215 | Language spacing between Latin and Asian text | -- | CD-1057 | core | plan D02 T10 §6 |  |
| NP-1216 | Hyphenate capitalized and all-caps words | -- | CD-1149, CD-1150 | core | plan D02 T10 §6 |  |
| NP-1217 | Minimum word length and characters before and after the hyphen | -- | CD-1151, CD-1152 | core | plan D02 T10 §6 |  |
| NP-1218 | Hyphenation zone (distance from the right margin) | -- | CD-1153 | core | plan D02 T10 §6 |  |
| NP-1219 | Bulleted and numbered lists | AI-0353 | CD-1026, CD-1027 | core | plan D02 T10 §7 |  |
| NP-1220 | Tabs panel and Tab Settings dialog | AI-0394 | CD-1047 | core | plan D02 T10 §7 |  |
| NP-1221 | Repeat tab, snap to unit, and position the Tabs panel above text | AI-0395 | -- | core | plan D02 T10 §7 |  |
| NP-1222 | Multilevel lists and list level selection | -- | CD-1028, CD-1031 | core | plan D02 T10 §7 |  |
| NP-1223 | Bullet color | -- | CD-1029 | core | plan D02 T10 §7 |  |
| NP-1224 | Bullets and Numbering dialog | -- | CD-1030, CD-1075 | core | plan D02 T10 §7 |  |
| NP-1225 | Bullet uses the paragraph font or its own | -- | CD-1032 | core | plan D02 T10 §7 |  |
| NP-1226 | Bullet glyph picker | -- | CD-1033 | core | plan D02 T10 §7 |  |
| NP-1227 | Numbering style, prefix, and suffix | -- | CD-1034 | core | plan D02 T10 §7 |  |
| NP-1228 | Bullet size and baseline shift | -- | CD-1035, CD-1036 | core | plan D02 T10 §7 |  |
| NP-1229 | Bullet spacing: glyph to text and frame to list | -- | CD-1037, CD-1038 | core | plan D02 T10 §7 |  |
| NP-1230 | Align wrapped lines in a list item | -- | CD-1039 | core | plan D02 T10 §7 |  |
| NP-1231 | Save a list as a paragraph style | -- | CD-1040 | core | plan D02 T10 §7 |  |
| NP-1232 | Drop caps: dialog and toggle | -- | CD-1041, CD-1043, CD-1076 | core | plan D02 T10 §7 |  |
| NP-1233 | Hanging drop cap | -- | CD-1042 | core | plan D02 T10 §7 |  |
| NP-1234 | Tab alignment types: left, center, right, decimal, align on character | -- | CD-1048 | core | plan D02 T10 §7 |  |
| NP-1235 | Tab leaders | -- | CD-1049 | core | plan D02 T10 §7 |  |
| NP-1236 | Tab stops on the ruler | -- | CD-1050 | core | plan D02 T10 §7 |  |
| NP-1237 | Insert a tab character | -- | CD-1071 | core | plan D02 T10 §7 |  |
| NP-1238 | Auto-size area text frames | AI-0329, AI-1153 | CD-986 | core | plan D02 T10 §8 |  |
| NP-1239 | Area Type Options dialog | AI-0330 | -- | core | plan D02 T10 §8 |  |
| NP-1240 | Inset spacing and first baseline | AI-0331 | -- | core | plan D02 T10 §8 |  |
| NP-1241 | Vertical alignment in the frame | AI-0332 | CD-1045 | core | plan D02 T10 §8 |  |
| NP-1242 | Thread text between frames | AI-0333 | CD-977, CD-1073 | core | plan D02 T10 §8 |  |
| NP-1243 | Release, unlink, and remove threading | AI-0334 | CD-981, CD-982 | core | plan D02 T10 §8 |  |
| NP-1244 | Show text threads and flow indicators | AI-0335 | CD-979, CD-983 | core | plan D02 T10 §8 |  |
| NP-1245 | Text wrap make and release | AI-0336 | CD-1005 | core | plan D02 T10 §8 |  |
| NP-1246 | Text wrap offset and invert | AI-0337 | CD-1008 | core | plan D02 T10 §8 |  |
| NP-1247 | Drag to create a text frame | -- | CD-957 | core | plan D02 T10 §8 |  |
| NP-1248 | Overflow indicator | -- | CD-958 | core | plan D02 T10 §8 |  |
| NP-1249 | Fit text to frame | -- | CD-959 | core | plan D02 T10 §8 |  |
| NP-1250 | Automatically adjust column width | -- | CD-960 | core | plan D02 T10 §8 |  |
| NP-1251 | Text frame background color | -- | CD-961 | core | plan D02 T10 §8 |  |
| NP-1252 | Create or remove a text frame on an object | -- | CD-962, CD-964, CD-965, CD-1072 | core | plan D02 T10 §8 |  |
| NP-1253 | Insert-in-object pointer | -- | CD-963 | core | plan D02 T10 §8 |  |
| NP-1254 | Break text inside a path apart | -- | CD-966 | core | plan D02 T10 §8 |  |
| NP-1255 | Scale text with its frame (Alt resize) | -- | CD-969 | core | plan D02 T10 §8 |  |
| NP-1256 | Number of columns | -- | CD-970, CD-1074 | core | plan D02 T10 §8 |  |
| NP-1257 | Column Settings dialog and equal width | -- | CD-971, CD-972 | core | plan D02 T10 §8 |  |
| NP-1258 | Right-to-left columns | -- | CD-973 | core | plan D02 T10 §8 |  |
| NP-1259 | Interactive column and gutter resize | -- | CD-974 | core | plan D02 T10 §8 |  |
| NP-1260 | Combine text frames | -- | CD-975 | core | plan D02 T10 §8 |  |
| NP-1261 | Break a frame apart into columns, paragraphs, lines, words, or characters | -- | CD-976 | core | plan D02 T10 §8 |  |
| NP-1262 | Create a linked frame on another page | -- | CD-978 | core | plan D02 T10 §8 |  |
| NP-1263 | Redirect text flow | -- | CD-980 | core | plan D02 T10 §8 |  |
| NP-1264 | Apply frame formatting to linked frames | -- | CD-984 | core | plan D02 T10 §8 |  |
| NP-1265 | Show text frame borders | -- | CD-985 | core | plan D02 T10 §8 |  |
| NP-1266 | Align lines to the baseline grid | -- | CD-987 | core | plan D02 T10 §8 |  |
| NP-1267 | Wrap styles: contour and square | -- | CD-1006, CD-1007 | core | plan D02 T10 §8 |  |
| NP-1268 | Type on a path effects and orientation: rainbow, skew, 3D ribbon, stair step, gravity | AI-0338 | CD-1011 | core | plan D02 T10 §9 |  |
| NP-1269 | Type on a Path Options dialog: align to path, spacing, flip | AI-0339 | -- | core | plan D02 T10 §9 |  |
| NP-1270 | Move or flip path text by its brackets or handle | AI-0340 | CD-1015 | core | plan D02 T10 §9 |  |
| NP-1271 | Update legacy type on a path | AI-0341 | -- | core | plan D02 T10 §9 |  |
| NP-1272 | Fit text to path command and pointer | -- | CD-1009, CD-1010 | core | plan D02 T10 §9 |  |
| NP-1273 | Distance from and offset along the path | -- | CD-1012, CD-1013 | core | plan D02 T10 §9 |  |
| NP-1274 | Tick snapping for path text | -- | CD-1014 | core | plan D02 T10 §9 |  |
| NP-1275 | Mirror text on the path | -- | CD-1016 | core | plan D02 T10 §9 |  |
| NP-1276 | Separate text from its path | -- | CD-1017 | core | plan D02 T10 §9 |  |
| NP-1277 | Vertical point, area, and path type tools | AI-0322, AI-0323, AI-0324 | -- | core | plan D02 T10 §10 |  |
| NP-1278 | Text orientation: horizontal or vertical | AI-0349 | CD-1055 | core | plan D02 T10 §10 |  |
| NP-1279 | Right-to-left direction and Middle Eastern and South Asian composers | AI-0390 | CD-1056 | core | plan D02 T10 §10 |  |
| NP-1280 | Japanese composer, Mojikumi, and Kinsoku presets | AI-0391 | -- | core | plan D02 T10 §10 |  |
| NP-1281 | Mojikumi and Kinsoku settings dialogs | AI-0392 | -- | core | plan D02 T10 §10 |  |
| NP-1282 | Asian type features: Tsume, Aki, Wari-Chu, Tate-Chu-Yoko, Moji-Gumi, Kurikaeshi, Burasagari | AI-0393 | -- | core | plan D02 T10 §10 |  |
| NP-1283 | Language options for East Asian, Indic, and Middle Eastern type | AI-1144 | -- | core | plan D02 T10 §10 |  |
| NP-1284 | Asian line-breaking rules | -- | CD-1079, CD-1160 | core | plan D02 T10 §10 |  |
| NP-1285 | Asian default font through the IME | -- | CD-1159 | core | plan D02 T10 §10 |  |
| NP-1286 | Asian widths | -- | CD-1161 | core | plan D02 T10 §10 |  |
| NP-1287 | Asian forms | -- | CD-1162 | core | plan D02 T10 §10 |  |
| NP-1288 | Vertical metrics, vertical alternates, and rotation | -- | CD-1163, CD-1165 | core | plan D02 T10 §10 |  |
| NP-1289 | Kana alternates | -- | CD-1164 | core | plan D02 T10 §10 |  |
| NP-1290 | Annotation forms | -- | CD-1166 | core | plan D02 T10 §10 |  |
| NP-1291 | Fit headline | AI-0343 | -- | core | plan D02 T10 §11 |  |
| NP-1292 | Fill with placeholder text | AI-0344 | CD-967 | core | plan D02 T10 §11 |  |
| NP-1293 | Insert special characters: dashes and hyphens | AI-0345 | CD-1067, CD-1068, CD-1069, CD-1154 | core | plan D02 T10 §11 |  |
| NP-1294 | Insert whitespace characters | AI-0346 | CD-1062, CD-1063, CD-1064, CD-1065 | core | plan D02 T10 §11 |  |
| NP-1295 | Insert line, column, and frame breaks | AI-0347 | CD-1066 | core | plan D02 T10 §11 |  |
| NP-1296 | Show hidden characters | AI-0348 | CD-1158 | core | plan D02 T10 §11 |  |
| NP-1297 | Change case | AI-0350 | CD-1077, CD-1108 | core | plan D02 T10 §11 |  |
| NP-1298 | Smart punctuation | AI-0351 | -- | core | plan D02 T10 §11 |  |
| NP-1299 | Find and replace text | AI-0354 | CD-989 | core | plan D02 T10 §11 |  |
| NP-1300 | Find next | AI-0355 | -- | core | plan D02 T10 §11 |  |
| NP-1301 | Text reflow viewer | AI-0420 | -- | core | plan D02 T10 §11 | possibly better owned by D02 T13 §16 (tagged PDF reading order) |
| NP-1302 | Fill new text objects with placeholder text | AI-1152 | -- | core | plan D02 T10 §11 |  |
| NP-1303 | Imported-text placement cursor | -- | CD-952 | core | plan D02 T10 §11 |  |
| NP-1304 | Custom placeholder text file | -- | CD-968 | core | plan D02 T10 §11 |  |
| NP-1305 | Find special characters | -- | CD-990 | core | plan D02 T10 §11 |  |
| NP-1306 | Search range | -- | CD-991 | core | plan D02 T10 §11 |  |
| NP-1307 | Replace text properties (font, weight, size) | -- | CD-992 | core | plan D02 T10 §11 |  |
| NP-1308 | Text encoding repair (Encode) | -- | CD-1058, CD-1078 | core | plan D02 T10 §11 |  |
| NP-1309 | Insert Formatting Code menu and shortcuts | -- | CD-1156, CD-1157 | core | plan D02 T10 §11 |  |
| NP-1310 | Text statistics | -- | CD-1224 | core | plan D02 T10 §11 |  |
| NP-1311 | Character styles | AI-0404 | CD-1609 | core | plan D02 T10 §12 |  |
| NP-1312 | Paragraph styles | AI-0405 | CD-1610 | core | plan D02 T10 §12 |  |
| NP-1313 | Style overrides: clear, redefine, load | AI-0406 | -- | core | plan D02 T10 §12 |  |
| NP-1314 | Variable font instance saved in a style | -- | CD-1140 | core | plan D02 T10 §12 |  |
| NP-1315 | Text frame styles | -- | CD-1611 | core | plan D02 T10 §12 |  |
| NP-1316 | Area type | AI-0320, AI-0327 | -- | core | shipped-scope D02 T06 §3 |  |
| NP-1317 | Type on a path | AI-0321 | -- | core | shipped-scope D02 T06 §3 |  |
| NP-1318 | Convert text to outlines | AI-0342 | CD-994 | core | shipped-scope D02 T06 §3 |  |

## Fonts and writing tools

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1319 | Find Font: list and replace document fonts | AI-0359 | -- | core | plan D02 T10 §3 |  |
| NP-1320 | Resolve missing fonts by replacement | AI-0360 | -- | cloud | plan D02 T10 §3 | Adobe Fonts activation excluded (cloud); local replacement only |
| NP-1321 | Edit text set in a missing font without replacing it | AI-0361 | -- | core | plan D02 T10 §3 |  |
| NP-1322 | Highlight substituted fonts and glyphs | AI-0362, AI-1150 | -- | core | plan D02 T10 §3 |  |
| NP-1323 | Font list: family and style picker | AI-0407 | CD-1095, CD-1097 | core | plan D02 T10 §3 | Adobe Fonts discovery and CC Libraries excluded (cloud) |
| NP-1324 | Font filters: classification, similar, favorites, technology, variable, weight, width, style, range, OpenType, clear | AI-0408 | CD-1192, CD-1193, CD-1194 | core | plan D02 T10 §3 | Adobe Fonts activated filter excluded (cloud) |
| NP-1325 | Recently used fonts and their count | AI-0412 | CD-1188, CD-1189 | core | plan D02 T10 §3 | More from Adobe Fonts excluded (cloud) |
| NP-1326 | Font name previews in their own face and preview size | AI-1151 | CD-1184, CD-1187 | core | plan D02 T10 §3 |  |
| NP-1327 | Type 1 font detection and warning | -- | CD-235, CD-1179 | core | plan D02 T10 §3 |  |
| NP-1328 | Embed fonts on save (option and default) | -- | CD-244, CD-1180 | core | plan D02 T10 §3 | SVG embeds font data in @font-face; CDR embedding follows D02 T14 §8 |
| NP-1329 | Match the Latin font when inserting text in another script | -- | CD-1167 | core | plan D02 T10 §3 |  |
| NP-1330 | Script filter for font changes | -- | CD-1168 | core | plan D02 T10 §3 |  |
| NP-1331 | Change the default font for new text | -- | CD-1169 | core | plan D02 T10 §3 |  |
| NP-1332 | Substitute missing fonts dialog on open and import | -- | CD-1170, CD-1227 | core | plan D02 T10 §3 |  |
| NP-1333 | PANOSE suggested match | -- | CD-1171 | core | plan D02 T10 §3 |  |
| NP-1334 | Manual font substitution | -- | CD-1172 | core | plan D02 T10 §3 |  |
| NP-1335 | Permanent or session-only substitution | -- | CD-1173 | core | plan D02 T10 §3 |  |
| NP-1336 | Font substitution exceptions list | -- | CD-1174, CD-1176 | core | plan D02 T10 §3 |  |
| NP-1337 | PANOSE font matching preferences | -- | CD-1175 | core | plan D02 T10 §3 |  |
| NP-1338 | Font embedding permissions (fsType) | -- | CD-1181 | core | plan D02 T10 §3 |  |
| NP-1339 | Fonts cannot be embedded warning | -- | CD-1182 | core | plan D02 T10 §3 |  |
| NP-1340 | Non-editable embedded font indicator | -- | CD-1183 | core | plan D02 T10 §3 |  |
| NP-1341 | Group fonts by family | -- | CD-1185 | core | plan D02 T10 §3 |  |
| NP-1342 | Show Latin names for non-Latin fonts | -- | CD-1186 | core | plan D02 T10 §3 |  |
| NP-1343 | Live font preview on hover | -- | CD-1190 | core | plan D02 T10 §3 |  |
| NP-1344 | Font list preview area and resize | -- | CD-1191 | core | plan D02 T10 §3 |  |
| NP-1345 | Font keyword search | -- | CD-1195 | core | plan D02 T10 §3 |  |
| NP-1346 | Font Sampler panel | -- | CD-1197, CD-1233 | core | plan D02 T10 §3 |  |
| NP-1347 | Font Sampler views and zoom | -- | CD-1198, CD-1199 | core | plan D02 T10 §3 |  |
| NP-1348 | Font Sampler samples: add, remove, reorder, edit text | -- | CD-1200 | core | plan D02 T10 §3 |  |
| NP-1349 | Font Sampler copy or drag a sample to the document | -- | CD-1201 | core | plan D02 T10 §3 |  |
| NP-1350 | Font Sampler OpenType on samples | -- | CD-1202 | core | plan D02 T10 §3 |  |
| NP-1351 | Font matching on text import | -- | CD-1226 | format | plan D02 T10 §3 |  |
| NP-1352 | Font List Options command | -- | CD-1228 | core | plan D02 T10 §3 |  |
| NP-1353 | Check spelling dialog | AI-0356 | CD-1212 | core | plan D02 T10 §13 | Windows Spell Checking API |
| NP-1354 | Auto spell check while typing | AI-0357 | -- | core | plan D02 T10 §13 |  |
| NP-1355 | Custom dictionary and user word lists | AI-0358 | CD-1222 | core | plan D02 T10 §13 |  |
| NP-1356 | Import text files into frames (TXT, RTF, DOC, DOCX) | AI-0418 | CD-949, CD-2583 | format | plan D02 T10 §13 | WPD is backlog B-037; D02 T14 §14 reuses these readers |
| NP-1357 | Plain text (TXT) export and ANSI text transfer | AI-0419 | CD-2631 | format | plan D02 T10 §13 |  |
| NP-1358 | Importing and Pasting Text dialog | -- | CD-950 | core | plan D02 T10 §13 |  |
| NP-1359 | Force CMYK black on imported text | -- | CD-951 | print | plan D02 T10 §13 |  |
| NP-1360 | Pasting and importing text warning | -- | CD-953 | core | plan D02 T10 §13 |  |
| NP-1361 | QuickCorrect dialog | -- | CD-1203, CD-1230 | core | plan D02 T10 §13 |  |
| NP-1362 | QuickCorrect capitalization: sentences, two initial caps, day names | -- | CD-1204, CD-1205, CD-1206 | core | plan D02 T10 §13 |  |
| NP-1363 | Automatic hyperlinks for web addresses | -- | CD-1207 | core | plan D02 T10 §13 |  |
| NP-1364 | Typographic quotes per language | -- | CD-1208 | core | plan D02 T10 §13 |  |
| NP-1365 | Replace text while typing | -- | CD-1209 | core | plan D02 T10 §13 |  |
| NP-1366 | Add spelling corrections to QuickCorrect | -- | CD-1210 | core | plan D02 T10 §13 |  |
| NP-1367 | Undo QuickCorrect | -- | CD-1211 | core | plan D02 T10 §13 |  |
| NP-1368 | Writing tools actions: replace, auto replace, skip once, skip all, add | -- | CD-1214 | core | plan D02 T10 §13 |  |
| NP-1369 | Check in another language | -- | CD-1215 | core | plan D02 T10 §13 |  |
| NP-1370 | Thesaurus | -- | CD-1216 | core | plan D02 T10 §13 | WordNet 3.1 data, English only |
| NP-1371 | Assign a language to text | -- | CD-1217, CD-1231 | core | plan D02 T10 §13 |  |
| NP-1372 | Spell checker options | -- | CD-1218 | core | plan D02 T10 §13 |  |
| NP-1373 | Thesaurus options | -- | CD-1220 | core | plan D02 T10 §13 |  |
| NP-1374 | Main word lists | -- | CD-1223 | core | plan D02 T10 §13 | maps to the installed Windows spelling languages |
| NP-1375 | Writing tools language coverage | -- | CD-1225 | core | plan D02 T10 §13 | grammar belongs to D02 T15 §7 |
| NP-1376 | Writing tools settings | -- | CD-1232 | core | plan D02 T10 §13 |  |

## Tables and graphs

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1377 | Table tool | -- | CD-1234 | core | plan D02 T10 §14 |  |
| NP-1378 | Create a new table | -- | CD-1235 | core | plan D02 T10 §14 |  |
| NP-1379 | Convert text to a table | -- | CD-1236 | core | plan D02 T10 §14 |  |
| NP-1380 | Select table, row, column, cell, or all contents | -- | CD-1237, CD-1238, CD-1239, CD-1240, CD-1241, CD-1283, CD-1284, CD-1285, CD-1286 | core | plan D02 T10 §14 |  |
| NP-1381 | Select cells with the shape tool | -- | CD-1242 | core | plan D02 T10 §14 |  |
| NP-1382 | Move a row or column by drag | -- | CD-1243 | core | plan D02 T10 §14 |  |
| NP-1383 | Paste rows and columns into another table | -- | CD-1244, CD-1245 | core | plan D02 T10 §14 |  |
| NP-1384 | Tab to the next cell and Tab key options | -- | CD-1246, CD-1247 | core | plan D02 T10 §14 |  |
| NP-1385 | Insert rows above, below, or several | -- | CD-1248, CD-1249, CD-1250, CD-1279, CD-1280 | core | plan D02 T10 §14 |  |
| NP-1386 | Insert columns left, right, or several | -- | CD-1251, CD-1252, CD-1253, CD-1281, CD-1282 | core | plan D02 T10 §14 |  |
| NP-1387 | Delete row, column, or table | -- | CD-1254, CD-1255, CD-1256, CD-1287, CD-1288, CD-1289 | core | plan D02 T10 §14 |  |
| NP-1388 | Cell width and height | -- | CD-1257 | core | plan D02 T10 §14 |  |
| NP-1389 | Distribute rows and columns evenly | -- | CD-1258, CD-1259, CD-1290, CD-1291 | core | plan D02 T10 §14 |  |
| NP-1390 | Border selection | -- | CD-1260 | core | plan D02 T10 §14 |  |
| NP-1391 | Border width, color, and line style | -- | CD-1261 | core | plan D02 T10 §14 |  |
| NP-1392 | Cell margins | -- | CD-1262 | core | plan D02 T10 §14 |  |
| NP-1393 | Separated cell borders and cell spacing | -- | CD-1263 | core | plan D02 T10 §14 |  |
| NP-1394 | Paragraph text in cells | -- | CD-1264 | core | plan D02 T10 §14 |  |
| NP-1395 | Format text across several cells | -- | CD-1265 | core | plan D02 T10 §14 |  |
| NP-1396 | Insert a tab in a cell | -- | CD-1266 | core | plan D02 T10 §14 |  |
| NP-1397 | Resize cells automatically while typing | -- | CD-1267 | core | plan D02 T10 §14 |  |
| NP-1398 | Convert a table to text | -- | CD-1268 | core | plan D02 T10 §14 |  |
| NP-1399 | Merge and unmerge cells | -- | CD-1269, CD-1270 | core | plan D02 T10 §14 |  |
| NP-1400 | Split cells into rows or columns | -- | CD-1271, CD-1272 | core | plan D02 T10 §14 |  |
| NP-1401 | Table as a transformable object | -- | CD-1273 | core | plan D02 T10 §14 |  |
| NP-1402 | Place an image in a cell | -- | CD-1274 | core | plan D02 T10 §14 |  |
| NP-1403 | Table and cell background | -- | CD-1275 | core | plan D02 T10 §14 |  |
| NP-1404 | Import tables from spreadsheets | -- | CD-1276 | core | plan D02 T10 §14 | XLS via NPOI, XLSX via OpenXml, CSV; Quattro Pro is backlog B-037; overlaps D02 T14 §14 |
| NP-1405 | Import tables from word processors | -- | CD-1277 | core | plan D02 T10 §14 | DOCX and DOC tables; WordPerfect is backlog B-037 |
| NP-1406 | Import and paste table formatting options | -- | CD-1278 | core | plan D02 T10 §14 |  |
| NP-1407 | Column and stacked column graphs | AI-0126, AI-0795 | -- | core | plan D02 T10 §15 |  |
| NP-1408 | Bar and stacked bar graphs | AI-0796, AI-0797 | -- | core | plan D02 T10 §15 |  |
| NP-1409 | Line and area graphs | AI-0798, AI-0799 | -- | core | plan D02 T10 §15 |  |
| NP-1410 | Scatter graph | AI-0800 | -- | core | plan D02 T10 §15 |  |
| NP-1411 | Pie graph | AI-0801 | -- | core | plan D02 T10 §15 |  |
| NP-1412 | Radar graph | AI-0802 | -- | core | plan D02 T10 §15 |  |
| NP-1413 | Graph Data window | AI-0803 | -- | core | plan D02 T10 §15 |  |
| NP-1414 | Import graph data from tab-delimited text | AI-0804 | -- | core | plan D02 T10 §15 |  |
| NP-1415 | Graph labels and data sets | AI-0805 | -- | core | plan D02 T10 §15 |  |
| NP-1416 | Graph Type dialog | AI-0806 | -- | core | plan D02 T10 §15 |  |
| NP-1417 | Value axis options | AI-0807 | -- | core | plan D02 T10 §15 |  |
| NP-1418 | Category axis options | AI-0808 | -- | core | plan D02 T10 §15 |  |
| NP-1419 | Different scales on left and right value axes | AI-0809 | -- | core | plan D02 T10 §15 |  |
| NP-1420 | Legend position | AI-0810 | -- | core | plan D02 T10 §15 |  |
| NP-1421 | Combine graph types | AI-0811 | -- | core | plan D02 T10 §15 |  |
| NP-1422 | Graph drop shadow | AI-0812 | -- | core | plan D02 T10 §15 |  |
| NP-1423 | Line and scatter options: mark, connect, edge-to-edge, filled lines | AI-0813 | -- | core | plan D02 T10 §15 |  |
| NP-1424 | Pie options: legend, position, sort | AI-0814 | -- | core | plan D02 T10 §15 |  |
| NP-1425 | Graph designs | AI-0815 | -- | core | plan D02 T10 §15 |  |
| NP-1426 | Column designs: vertically scaled, uniformly scaled, repeating, sliding | AI-0816 | -- | core | plan D02 T10 §15 |  |
| NP-1427 | Marker designs | AI-0817 | -- | core | plan D02 T10 §15 |  |
| NP-1428 | Select parts of a graph | AI-0818 | -- | core | plan D02 T10 §15 |  |
| NP-1429 | Format graph text | AI-0819 | -- | core | plan D02 T10 §15 |  |
| NP-1430 | Reuse graph designs across documents | AI-0820 | -- | core | plan D02 T10 §15 |  |
| NP-1431 | Column and cluster width | AI-0821 | -- | core | plan D02 T10 §15 |  |

## Blend, contour, envelope, and distort

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1432 | Resolution-independent effect parameters | AI-0645 | -- | core | plan D02 T11 §1 | parameters stored in document units and re-evaluated when the raster effects resolution changes |
| NP-1433 | Vector and raster effect split in the Effect menu | AI-0646 | -- | core | plan D02 T11 §1 | vector effects render through SkiaSharp; raster effects arrive with D02 T12 §2 |
| NP-1434 | Clear Effect | -- | CD-574 | core | plan D02 T11 §1 | one generic command over the effect registry; per-effect clear rows stay in their sections |
| NP-1435 | Effects in focus mode | -- | CD-1802 | core | plan D02 T11 §1 | focus mode itself is D02 T07 §7 |
| NP-1436 | Blend tool | AI-0583 | CD-1749 | core | plan D02 T11 §2 |  |
| NP-1437 | Make blend | AI-0584 | -- | core | plan D02 T11 §2 |  |
| NP-1438 | Release blend | AI-0585 | -- | core | plan D02 T11 §2 |  |
| NP-1439 | Blend steps, spacing, and smooth color | AI-0586 | CD-1758, CD-1759 | core | plan D02 T11 §2 |  |
| NP-1440 | Blend orientation: align to page or path | AI-0587 | -- | core | plan D02 T11 §2 |  |
| NP-1441 | Expand blend and break blend apart | AI-0588 | CD-547 | core | plan D02 T11 §2 |  |
| NP-1442 | Reverse blend front to back | AI-0591 | CD-1771 | core | plan D02 T11 §2 |  |
| NP-1443 | Blend panel and docker | AI-0592 | CD-1750, CD-1779, CD-1780 | core | plan D02 T11 §2 | one Blend panel serves both vocabularies |
| NP-1444 | Blend easing with ramp | AI-0593 | -- | core | plan D02 T11 §2 |  |
| NP-1445 | Blend object and color acceleration | AI-0594 | CD-1762 | core | plan D02 T11 §2 | appearance shift and Corel color acceleration are one parameter |
| NP-1446 | Live blend editing through key objects and spine | AI-0595 | -- | core | plan D02 T11 §2 |  |
| NP-1447 | Blend rotation | -- | CD-1760 | core | plan D02 T11 §2 |  |
| NP-1448 | Loop blend | -- | CD-1761 | core | plan D02 T11 §2 |  |
| NP-1449 | Blend accelerate sizing | -- | CD-1763 | core | plan D02 T11 §2 |  |
| NP-1450 | Blend color path: direct, clockwise, counterclockwise | -- | CD-1764, CD-1765, CD-1766 | core | plan D02 T11 §2 |  |
| NP-1451 | Blend fill restriction for bitmap and pattern fills | -- | CD-1778 | core | plan D02 T11 §2 |  |
| NP-1452 | Replace spine and fit blend to path | AI-0589 | CD-1752 | core | plan D02 T11 §3 |  |
| NP-1453 | Reverse spine | AI-0590 | -- | core | plan D02 T11 §3 |  |
| NP-1454 | Copy blend effect from | -- | CD-563, CD-1756 | core | plan D02 T11 §3 |  |
| NP-1455 | Clone blend effect from | -- | CD-568, CD-1757 | core | plan D02 T11 §3 |  |
| NP-1456 | Freehand path blend and editing the blend path | -- | CD-1751, CD-1774 | core | plan D02 T11 §3 |  |
| NP-1457 | Blend along full path | -- | CD-1753 | core | plan D02 T11 §3 |  |
| NP-1458 | Rotate all blend objects along path | -- | CD-1754 | core | plan D02 T11 §3 |  |
| NP-1459 | Compound blends | -- | CD-1755 | core | plan D02 T11 §3 |  |
| NP-1460 | Map nodes between blend ends | -- | CD-1767 | core | plan D02 T11 §3 |  |
| NP-1461 | Show blend start and end objects | -- | CD-1768 | core | plan D02 T11 §3 |  |
| NP-1462 | New blend start and end objects | -- | CD-1769 | core | plan D02 T11 §3 |  |
| NP-1463 | Fuse blend start and end | -- | CD-1770 | core | plan D02 T11 §3 |  |
| NP-1464 | Show blend path | -- | CD-1772 | core | plan D02 T11 §3 |  |
| NP-1465 | Detach blend from path | -- | CD-1773 | core | plan D02 T11 §3 |  |
| NP-1466 | Split blend | -- | CD-1775 | core | plan D02 T11 §3 |  |
| NP-1467 | Clear blend | -- | CD-1776 | core | plan D02 T11 §3 |  |
| NP-1468 | Blend presets | -- | CD-1777 | core | plan D02 T11 §3 |  |
| NP-1469 | Copy contour effect from | -- | CD-565, CD-1798 | core | plan D02 T11 §4 |  |
| NP-1470 | Clone contour effect from | -- | CD-569, CD-1799 | core | plan D02 T11 §4 |  |
| NP-1471 | Contour tool | -- | CD-1781 | core | plan D02 T11 §4 |  |
| NP-1472 | Contour panel | -- | CD-1782, CD-1803, CD-1804 | core | plan D02 T11 §4 |  |
| NP-1473 | Contour direction: to center, inside, outside | -- | CD-1783, CD-1784, CD-1785 | core | plan D02 T11 §4 |  |
| NP-1474 | Contour steps | -- | CD-1786 | core | plan D02 T11 §4 |  |
| NP-1475 | Contour offset | -- | CD-1787 | core | plan D02 T11 §4 |  |
| NP-1476 | Contour object and color acceleration | -- | CD-1788 | core | plan D02 T11 §4 |  |
| NP-1477 | Contour corners: mitered, round, bevel | -- | CD-1789, CD-1790, CD-1791 | core | plan D02 T11 §4 |  |
| NP-1478 | Contour fill and outline end colors | -- | CD-1792, CD-1793 | core | plan D02 T11 §4 |  |
| NP-1479 | Contour end fill handle | -- | CD-1794 | core | plan D02 T11 §4 |  |
| NP-1480 | Contour color path: linear, clockwise, counterclockwise | -- | CD-1795, CD-1796, CD-1797 | core | plan D02 T11 §4 |  |
| NP-1481 | Break contour apart | -- | CD-1800 | core | plan D02 T11 §4 |  |
| NP-1482 | Contour cuttable outlines | -- | CD-1801 | core | plan D02 T11 §4 |  |
| NP-1483 | Envelope make with warp | AI-0271 | -- | core | plan D02 T11 §5 |  |
| NP-1484 | Envelope make with mesh and mesh editing | AI-0272, AI-0277 | -- | core | plan D02 T11 §5 |  |
| NP-1485 | Envelope from a top object or another curve | AI-0273 | CD-1816 | core | plan D02 T11 §5 |  |
| NP-1486 | Envelope release and expand | AI-0274 | -- | core | plan D02 T11 §5 |  |
| NP-1487 | Edit envelope contents or envelope | AI-0275 | -- | core | plan D02 T11 §5 |  |
| NP-1488 | Envelope options: anti-alias, fidelity, distort appearance, fills | AI-0276 | -- | core | plan D02 T11 §5 |  |
| NP-1489 | Warped text with envelopes | AI-0424 | -- | core | plan D02 T11 §5 | text in shapes is D02 T10 §8, 3D text is §10 |
| NP-1490 | Warp options: horizontal or vertical, bend, distortion | AI-0704 | -- | core | plan D02 T11 §5 |  |
| NP-1491 | Warp styles: arc, arch, bulge, shell, flag, wave, fish, rise, fisheye, inflate, squeeze, twist | AI-0705, AI-0706, AI-0707, AI-0708, AI-0709, AI-0710, AI-0711, AI-0712, AI-0713, AI-0714, AI-0715, AI-0716, AI-0717, AI-0718, AI-0719 | -- | core | plan D02 T11 §5 | fifteen presets of one parametric warp |
| NP-1492 | Copy envelope from | -- | CD-558, CD-1817 | core | plan D02 T11 §5 |  |
| NP-1493 | Envelope tool | -- | CD-1805 | core | plan D02 T11 §5 |  |
| NP-1494 | Envelope panel | -- | CD-1806, CD-1827, CD-1828 | core | plan D02 T11 §5 |  |
| NP-1495 | Envelope modes: straight line, single arc, double arc, unconstrained | -- | CD-1807, CD-1808, CD-1809, CD-1810 | core | plan D02 T11 §5 |  |
| NP-1496 | Envelope presets and saving presets | -- | CD-1811, CD-1812 | core | plan D02 T11 §5 | presets in the Nodus preset store, not Corel PST files |
| NP-1497 | Add new envelope over an existing one | -- | CD-1813 | core | plan D02 T11 §5 |  |
| NP-1498 | Clear envelope | -- | CD-1814 | core | plan D02 T11 §5 |  |
| NP-1499 | Envelope keep lines | -- | CD-1815 | core | plan D02 T11 §5 |  |
| NP-1500 | Envelope node editing and node types | -- | CD-1818, CD-1820 | core | plan D02 T11 §5 |  |
| NP-1501 | Envelope constrained node moves | -- | CD-1819 | core | plan D02 T11 §5 |  |
| NP-1502 | Envelope mapping modes: horizontal, original, putty, vertical | -- | CD-1821, CD-1822, CD-1823, CD-1824 | core | plan D02 T11 §5 |  |
| NP-1503 | Envelope on paragraph text frames | -- | CD-1825 | core | plan D02 T11 §5 |  |
| NP-1504 | Envelope on bitmaps | -- | CD-1826 | core | plan D02 T11 §5 | bitmap mesh warp resampled through SkiaSharp at render time |
| NP-1505 | Free distort effect | AI-0675 | -- | core | plan D02 T11 §6 |  |
| NP-1506 | Pucker and bloat, push and pull distortion | AI-0676 | CD-1858 | core | plan D02 T11 §6 |  |
| NP-1507 | Roughen effect | AI-0677 | -- | core | plan D02 T11 §6 |  |
| NP-1508 | Transform effect with copies | AI-0678 | -- | core | plan D02 T11 §6 |  |
| NP-1509 | Tweak effect | AI-0679 | -- | core | plan D02 T11 §6 |  |
| NP-1510 | Twist effect and twister distortion | AI-0680 | CD-1860 | core | plan D02 T11 §6 |  |
| NP-1511 | Zig zag effect and zipper distortion | AI-0681 | CD-1859, CD-1863 | core | plan D02 T11 §6 |  |
| NP-1512 | Copy distortion from | -- | CD-561, CD-1867 | core | plan D02 T11 §6 |  |
| NP-1513 | Clone distortion from | -- | CD-571 | core | plan D02 T11 §6 |  |
| NP-1514 | Distort tool | -- | CD-1857 | core | plan D02 T11 §6 |  |
| NP-1515 | Center of distortion handle and command | -- | CD-1861, CD-1862 | core | plan D02 T11 §6 |  |
| NP-1516 | Distortion presets | -- | CD-1864 | core | plan D02 T11 §6 |  |
| NP-1517 | Stacked distortions | -- | CD-1865 | core | plan D02 T11 §6 |  |
| NP-1518 | Clear distortion | -- | CD-1866 | core | plan D02 T11 §6 |  |
| NP-1519 | Distortion in focus mode | -- | CD-1868 | core | plan D02 T11 §6 |  |
| NP-1520 | Puppet warp tool and pins | AI-0227 | -- | core | plan D02 T11 §16 |  |
| NP-1521 | Puppet warp mesh options: show, expand, select all pins | AI-0228 | -- | core | plan D02 T11 §16 |  |
| NP-1522 | Convert to shape effect: rectangle, rounded rectangle, ellipse | AI-0670, AI-0671, AI-0672 | -- | core | plan D02 T11 §19 |  |
| NP-1523 | Offset path effect | AI-0682 | -- | core | plan D02 T11 §19 |  |
| NP-1524 | Outline object effect | AI-0683 | -- | core | plan D02 T11 §19 |  |
| NP-1525 | Outline stroke effect | AI-0684 | -- | core | plan D02 T11 §19 |  |
| NP-1526 | Live shape modes: add, intersect, exclude, subtract, minus back | AI-0685, AI-0686, AI-0687, AI-0688, AI-0689 | -- | core | plan D02 T11 §19 |  |
| NP-1527 | Live pathfinders: divide, trim, merge, crop, outline | AI-0690 | -- | core | plan D02 T11 §19 |  |
| NP-1528 | Hard mix effect | AI-0691 | -- | core | plan D02 T11 §19 |  |
| NP-1529 | Soft mix effect | AI-0692 | -- | core | plan D02 T11 §19 |  |

## 3D, shadows, glows, and bevels

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1530 | Flat drop shadow | AI-0695 | CD-1873 | core | plan D02 T11 §7 | Skia image filter at render time |
| NP-1531 | Break block shadow apart | -- | CD-548 | core | plan D02 T11 §7 |  |
| NP-1532 | Copy shadow from | -- | CD-562, CD-1889, CD-1890 | core | plan D02 T11 §7 |  |
| NP-1533 | Clone shadow from | -- | CD-572, CD-1891 | core | plan D02 T11 §7 |  |
| NP-1534 | Shadow merge mode | -- | CD-1452, CD-1879 | core | plan D02 T11 §7 |  |
| NP-1535 | Shadow tool: drop and inner | -- | CD-1869, CD-1870, CD-1872 | core | plan D02 T11 §7 |  |
| NP-1536 | Block shadow tool | -- | CD-1871 | core | plan D02 T11 §7 | vector geometry, not a bitmap |
| NP-1537 | Perspective drop shadow: angle, stretch, fade | -- | CD-1874, CD-1886, CD-1887, CD-1888 | core | plan D02 T11 §7 |  |
| NP-1538 | Inner shadow and width | -- | CD-1875, CD-1884 | core | plan D02 T11 §7 |  |
| NP-1539 | Shadow presets: apply, add, delete | -- | CD-1876, CD-1877 | core | plan D02 T11 §7 |  |
| NP-1540 | Shadow color | -- | CD-1878 | core | plan D02 T11 §7 |  |
| NP-1541 | Shadow opacity | -- | CD-1880 | core | plan D02 T11 §7 |  |
| NP-1542 | Shadow feathering | -- | CD-1881 | core | plan D02 T11 §7 |  |
| NP-1543 | Shadow feather direction and edge type | -- | CD-1882, CD-1883 | core | plan D02 T11 §7 |  |
| NP-1544 | Shadow offset | -- | CD-1885 | core | plan D02 T11 §7 |  |
| NP-1545 | Break drop or inner shadow apart | -- | CD-1892, CD-1893 | core | plan D02 T11 §7 |  |
| NP-1546 | Clear shadow | -- | CD-1894 | core | plan D02 T11 §7 |  |
| NP-1547 | One shadow per object rule | -- | CD-1895 | core | plan D02 T11 §7 |  |
| NP-1548 | Block shadow depth and direction | -- | CD-1896, CD-1897 | core | plan D02 T11 §7 |  |
| NP-1549 | Block shadow color | -- | CD-1898 | core | plan D02 T11 §7 |  |
| NP-1550 | Block shadow remove holes | -- | CD-1899 | core | plan D02 T11 §7 |  |
| NP-1551 | Block shadow from object outline | -- | CD-1900 | core | plan D02 T11 §7 |  |
| NP-1552 | Expand block shadow | -- | CD-1901 | core | plan D02 T11 §7 |  |
| NP-1553 | Overprint block shadow | -- | CD-1902 | print | plan D02 T11 §7 | overprint output honored by D02 T13 §7 |
| NP-1554 | Simplify block shadow | -- | CD-1903 | print | plan D02 T11 §7 |  |
| NP-1555 | Clear block shadow | -- | CD-1904 | core | plan D02 T11 §7 |  |
| NP-1556 | Feather effect | AI-0696 | -- | core | plan D02 T11 §8 |  |
| NP-1557 | Inner glow | AI-0697 | -- | core | plan D02 T11 §8 |  |
| NP-1558 | Outer glow | AI-0698 | -- | core | plan D02 T11 §8 |  |
| NP-1559 | Round corners effect | AI-0699 | -- | core | plan D02 T11 §8 |  |
| NP-1560 | Scribble effect | AI-0700 | -- | core | plan D02 T11 §8 |  |
| NP-1561 | Break bevel apart | -- | CD-550 | core | plan D02 T11 §8 |  |
| NP-1562 | Copy bevel from | -- | CD-566 | core | plan D02 T11 §8 |  |
| NP-1563 | Clone bevel from | -- | CD-573 | core | plan D02 T11 §8 |  |
| NP-1564 | Bevel panel | -- | CD-1905, CD-1917, CD-1918 | core | plan D02 T11 §8 |  |
| NP-1565 | Soft edge bevel | -- | CD-1906 | core | plan D02 T11 §8 |  |
| NP-1566 | Emboss bevel | -- | CD-1907 | core | plan D02 T11 §8 |  |
| NP-1567 | Bevel offset: to center or distance | -- | CD-1908, CD-1909 | core | plan D02 T11 §8 |  |
| NP-1568 | Bevel shadow and light colors | -- | CD-1910, CD-1911 | core | plan D02 T11 §8 |  |
| NP-1569 | Bevel light intensity, direction, and altitude | -- | CD-1912, CD-1913, CD-1914 | core | plan D02 T11 §8 |  |
| NP-1570 | Bevel spot and process colors | -- | CD-1915 | print | plan D02 T11 §8 |  |
| NP-1571 | Clear bevel | -- | CD-1916 | core | plan D02 T11 §8 |  |
| NP-1572 | Classic vector extrude | AI-0666 | CD-1829 | core | plan D02 T11 §9 |  |
| NP-1573 | Classic revolve | AI-0667 | -- | core | plan D02 T11 §9 |  |
| NP-1574 | Classic 3D rotate | AI-0668 | -- | core | plan D02 T11 §9 |  |
| NP-1575 | Classic surface shading, lighting, and map art | AI-0669 | -- | core | plan D02 T11 §9 |  |
| NP-1576 | Break extrude apart | -- | CD-549 | core | plan D02 T11 §9 |  |
| NP-1577 | Copy extrude from | -- | CD-564, CD-1839 | core | plan D02 T11 §9 |  |
| NP-1578 | Clone extrude from | -- | CD-570, CD-1840 | core | plan D02 T11 §9 |  |
| NP-1579 | Extrude panel | -- | CD-1830, CD-1855, CD-1856 | core | plan D02 T11 §9 |  |
| NP-1580 | Extrusion presets | -- | CD-1831 | core | plan D02 T11 §9 |  |
| NP-1581 | Extrusion type | -- | CD-1832 | core | plan D02 T11 §9 |  |
| NP-1582 | Extrusion inside a group | -- | CD-1833 | core | plan D02 T11 §9 |  |
| NP-1583 | Extrude rotation widget | -- | CD-1834 | core | plan D02 T11 §9 |  |
| NP-1584 | Extrusion direction by vanishing point drag | -- | CD-1835 | core | plan D02 T11 §9 |  |
| NP-1585 | Extrusion depth | -- | CD-1836 | core | plan D02 T11 §9 |  |
| NP-1586 | Rounded corners on extruded rectangles | -- | CD-1837 | core | plan D02 T11 §9 |  |
| NP-1587 | Clear extrusion | -- | CD-1838 | core | plan D02 T11 §9 |  |
| NP-1588 | Extrusion color: object fill, solid, shading | -- | CD-1841, CD-1842, CD-1843 | core | plan D02 T11 §9 |  |
| NP-1589 | Drape fills over extrusions | -- | CD-1844 | core | plan D02 T11 §9 |  |
| NP-1590 | Extrusion bevel: use, depth, angle, show only | -- | CD-1845, CD-1846, CD-1847, CD-1848 | core | plan D02 T11 §9 |  |
| NP-1591 | Extrusion lighting: three lights and intensity | -- | CD-1849, CD-1850 | core | plan D02 T11 §9 |  |
| NP-1592 | Vanishing point locked to object or page | -- | CD-1851, CD-1852 | core | plan D02 T11 §9 |  |
| NP-1593 | Copy and share vanishing points | -- | CD-1853, CD-1854 | core | plan D02 T11 §9 |  |
| NP-1594 | 3D and Materials panel | AI-0647 | -- | core | plan D02 T11 §10 |  |
| NP-1595 | 3D plane | AI-0648 | -- | core | plan D02 T11 §10 |  |
| NP-1596 | 3D extrude with twist, taper, and caps | AI-0649 | -- | core | plan D02 T11 §10 |  |
| NP-1597 | 3D revolve | AI-0650 | -- | core | plan D02 T11 §10 |  |
| NP-1598 | 3D inflate | AI-0651 | -- | core | plan D02 T11 §10 |  |
| NP-1599 | 3D bevels | AI-0652 | -- | core | plan D02 T11 §10 |  |
| NP-1600 | Custom 3D bevel profiles | AI-0653 | -- | core | plan D02 T11 §10 |  |
| NP-1601 | 3D rotation presets, angles, and perspective | AI-0654 | -- | core | plan D02 T11 §10 |  |
| NP-1602 | On-canvas 3D rotation widget | AI-0655 | -- | core | plan D02 T11 §10 |  |
| NP-1603 | 3D materials: built-in parametric materials | AI-0656 | -- | cloud | plan D02 T11 §10 | own parametric materials; no Adobe Substance or cloud material library |
| NP-1604 | Custom 3D materials | AI-0657 | -- | core | plan D02 T11 §10 | user-saved parametric materials; Substance .sbsar is not read |
| NP-1605 | Map artwork onto 3D surfaces | AI-0658, AI-0659 | -- | core | plan D02 T11 §10 |  |
| NP-1606 | 3D lighting presets | AI-0660 | -- | core | plan D02 T11 §10 |  |
| NP-1607 | 3D lighting parameters, multiple lights, and ambient | AI-0661 | -- | core | plan D02 T11 §10 |  |
| NP-1608 | 3D cast shadows | AI-0662 | -- | core | plan D02 T11 §10 |  |
| NP-1609 | Ray-traced 3D render | AI-0663 | -- | core | plan D02 T11 §10 | own CPU path tracer, deterministic by seed |
| NP-1610 | Export 3D objects: OBJ, glTF, USDA | AI-0664 | -- | format | plan D02 T11 §10 | own writers; glTF proven with the Khronos validator |
| NP-1611 | 3D on live text | AI-0665 | -- | core | plan D02 T11 §10 |  |

## Lenses, PowerClip, perspective, symmetry, and repeats

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1612 | Copy lens from | -- | CD-559, CD-1932 | core | plan D02 T11 §11 |  |
| NP-1613 | Lens panel | -- | CD-1919, CD-1940, CD-1941 | core | plan D02 T11 §11 |  |
| NP-1614 | Brighten lens | -- | CD-1921 | core | plan D02 T11 §11 |  |
| NP-1615 | Color add lens | -- | CD-1922 | core | plan D02 T11 §11 |  |
| NP-1616 | Color limit lens | -- | CD-1923 | core | plan D02 T11 §11 |  |
| NP-1617 | Custom color map lens | -- | CD-1924 | core | plan D02 T11 §11 |  |
| NP-1618 | Fish eye lens | -- | CD-1925 | core | plan D02 T11 §11 |  |
| NP-1619 | Heat map lens | -- | CD-1926 | core | plan D02 T11 §11 |  |
| NP-1620 | Invert lens | -- | CD-1927 | core | plan D02 T11 §11 |  |
| NP-1621 | Magnify lens | -- | CD-1928 | core | plan D02 T11 §11 |  |
| NP-1622 | Tinted grayscale lens | -- | CD-1929 | core | plan D02 T11 §11 |  |
| NP-1623 | Transparency lens | -- | CD-1930 | core | plan D02 T11 §11 |  |
| NP-1624 | Wireframe lens | -- | CD-1931 | core | plan D02 T11 §11 |  |
| NP-1625 | Lens restrictions | -- | CD-1933 | core | plan D02 T11 §11 |  |
| NP-1626 | Lens viewpoint | -- | CD-1934 | core | plan D02 T11 §11 |  |
| NP-1627 | Lens remove face | -- | CD-1935 | core | plan D02 T11 §11 |  |
| NP-1628 | Frozen lens | -- | CD-1936 | core | plan D02 T11 §11 |  |
| NP-1629 | Edit lens shape | -- | CD-1937 | core | plan D02 T11 §11 |  |
| NP-1630 | Feather lens edges | -- | CD-1938 | core | plan D02 T11 §11 |  |
| NP-1631 | Lens in focus mode | -- | CD-1939 | core | plan D02 T11 §11 |  |
| NP-1632 | Copy PowerClip from | -- | CD-567, CD-1953 | core | plan D02 T11 §12 |  |
| NP-1633 | Place inside frame | -- | CD-1942, CD-1957 | core | plan D02 T11 §12 |  |
| NP-1634 | Nested PowerClip frames | -- | CD-1943 | core | plan D02 T11 §12 |  |
| NP-1635 | Create empty PowerClip frame | -- | CD-1944 | core | plan D02 T11 §12 |  |
| NP-1636 | Drag content into a frame and drop behavior | -- | CD-1945, CD-2857 | core | plan D02 T11 §12 |  |
| NP-1637 | Remove frame | -- | CD-1946 | core | plan D02 T11 §12 |  |
| NP-1638 | PowerClip floating toolbar | -- | CD-1947 | core | plan D02 T11 §12 |  |
| NP-1639 | Select PowerClip contents | -- | CD-1948 | core | plan D02 T11 §12 |  |
| NP-1640 | Center PowerClip contents | -- | CD-1949, CD-1960 | core | plan D02 T11 §12 |  |
| NP-1641 | Fit contents proportionally | -- | CD-1950 | core | plan D02 T11 §12 |  |
| NP-1642 | Fill frame proportionally | -- | CD-1951 | core | plan D02 T11 §12 |  |
| NP-1643 | Stretch contents to fill | -- | CD-1952 | core | plan D02 T11 §12 |  |
| NP-1644 | Edit PowerClip and finish editing | -- | CD-1954, CD-1958, CD-1959 | core | plan D02 T11 §12 |  |
| NP-1645 | Lock contents to PowerClip | -- | CD-1955 | core | plan D02 T11 §12 |  |
| NP-1646 | Extract PowerClip contents | -- | CD-1956 | core | plan D02 T11 §12 |  |
| NP-1647 | Auto-center new PowerClip content | -- | CD-2858 | core | plan D02 T11 §12 |  |
| NP-1648 | Show lines in empty PowerClip frames | -- | CD-2859 | core | plan D02 T11 §12 |  |
| NP-1649 | Break symmetry link and break symmetry apart | -- | CD-554, CD-909 | core | plan D02 T11 §13 | both leave a regular group of real objects |
| NP-1650 | Symmetry drawing mode: create new symmetry | -- | CD-895, CD-896 | core | plan D02 T11 §13 |  |
| NP-1651 | Edit and finish editing symmetry | -- | CD-897, CD-901 | core | plan D02 T11 §13 |  |
| NP-1652 | Symmetry mirror line count | -- | CD-898 | core | plan D02 T11 §13 |  |
| NP-1653 | Reposition and rotate symmetry lines | -- | CD-899 | core | plan D02 T11 §13 |  |
| NP-1654 | Symmetry center X and Y | -- | CD-900 | core | plan D02 T11 §13 |  |
| NP-1655 | Symmetry full preview | -- | CD-902 | core | plan D02 T11 §13 |  |
| NP-1656 | Show symmetry lines | -- | CD-903 | core | plan D02 T11 §13 |  |
| NP-1657 | Drag objects into a symmetry group | -- | CD-904 | core | plan D02 T11 §13 |  |
| NP-1658 | Symmetry group as a single entity | -- | CD-905 | core | plan D02 T11 §13 |  |
| NP-1659 | Snap to symmetry lines | -- | CD-906, CD-2452 | core | plan D02 T11 §13 |  |
| NP-1660 | Fuse open curves in symmetry | -- | CD-907 | core | plan D02 T11 §13 |  |
| NP-1661 | Remove symmetry | -- | CD-908 | core | plan D02 T11 §13 |  |
| NP-1662 | Perspective grid tool | AI-0123 | -- | core | plan D02 T11 §14 |  |
| NP-1663 | Perspective types: one, two, and three point | AI-0306 | CD-911, CD-912, CD-913, CD-914 | core | plan D02 T11 §14 | three-point covers worm and bird eye views |
| NP-1664 | Show or hide the perspective grid | AI-0307 | -- | core | plan D02 T11 §14 |  |
| NP-1665 | Perspective grid rulers, snap, lock grid, lock station point | AI-0308 | -- | core | plan D02 T11 §14 |  |
| NP-1666 | Define perspective grid | AI-0309 | -- | core | plan D02 T11 §14 |  |
| NP-1667 | Perspective grid presets: save and manage | AI-0310 | -- | core | plan D02 T11 §14 |  |
| NP-1668 | Perspective grid widgets: vanishing points, horizon, extent, viewport | AI-0311 | CD-920, CD-921, CD-922 | core | plan D02 T11 §14 |  |
| NP-1669 | Active drawing plane and plane switching | AI-0312 | CD-916, CD-917, CD-918, CD-919 | core | plan D02 T11 §14 |  |
| NP-1670 | Hide perspective grid widget | AI-0318 | -- | core | plan D02 T11 §14 |  |
| NP-1671 | Draw in perspective | -- | CD-910 | core | plan D02 T11 §14 |  |
| NP-1672 | Perspective field fill page | -- | CD-915 | core | plan D02 T11 §14 |  |
| NP-1673 | Perspective camera lines | -- | CD-923 | core | plan D02 T11 §14 |  |
| NP-1674 | Lock perspective field | -- | CD-924 | core | plan D02 T11 §14 |  |
| NP-1675 | Restricted perspective drawing areas | -- | CD-925 | core | plan D02 T11 §14 |  |
| NP-1676 | Snap to perspective lines | -- | CD-932, CD-2453 | core | plan D02 T11 §14 |  |
| NP-1677 | Horizon display: show, opacity, color | -- | CD-934 | core | plan D02 T11 §14 |  |
| NP-1678 | Perspective line display: show, density, opacity, color | -- | CD-935 | core | plan D02 T11 §14 |  |
| NP-1679 | Perspective selection tool | AI-0124 | -- | core | plan D02 T11 §15 |  |
| NP-1680 | Attach to active plane and move to plane | AI-0313 | CD-929 | core | plan D02 T11 §15 |  |
| NP-1681 | Release with perspective and break perspective group apart | AI-0314 | CD-936 | core | plan D02 T11 §15 |  |
| NP-1682 | Move plane to match object | AI-0315 | -- | core | plan D02 T11 §15 |  |
| NP-1683 | Editable text and symbols in perspective | AI-0316 | CD-931 | core | plan D02 T11 §15 |  |
| NP-1684 | Perpendicular move and copy in perspective | AI-0317 | -- | core | plan D02 T11 §15 |  |
| NP-1685 | Copy perspective from | -- | CD-560, CD-945 | core | plan D02 T11 §15 |  |
| NP-1686 | Perspective groups written as plain groups for older readers | -- | CD-926 | core | plan D02 T11 §15 | the expanded SVG fallback of D02 T07 §1 |
| NP-1687 | Edit perspective group | -- | CD-927 | core | plan D02 T11 §15 |  |
| NP-1688 | Move object along a perspective plane | -- | CD-928 | core | plan D02 T11 §15 |  |
| NP-1689 | Reshape an object on a perspective plane | -- | CD-930 | core | plan D02 T11 §15 |  |
| NP-1690 | Perspective group transform limits | -- | CD-933 | core | plan D02 T11 §15 |  |
| NP-1691 | Add perspective effect | -- | CD-937 | core | plan D02 T11 §15 |  |
| NP-1692 | One-point and two-point perspective node drags | -- | CD-938, CD-939 | core | plan D02 T11 §15 |  |
| NP-1693 | Symmetric perspective node drag | -- | CD-940 | core | plan D02 T11 §15 |  |
| NP-1694 | Perspective vanishing point drag | -- | CD-941 | core | plan D02 T11 §15 |  |
| NP-1695 | Edit perspective with the shape tool | -- | CD-942 | core | plan D02 T11 §15 |  |
| NP-1696 | Perspective on linked groups | -- | CD-943 | core | plan D02 T11 §15 |  |
| NP-1697 | Perspective flattened by split, crop, or erase | -- | CD-944 | core | plan D02 T11 §15 |  |
| NP-1698 | Clear perspective | -- | CD-946 | core | plan D02 T11 §15 |  |
| NP-1699 | Live Paint make | AI-0596 | -- | core | plan D02 T11 §17 |  |
| NP-1700 | Live Paint bucket with double and triple click | AI-0597, AI-0599 | -- | core | plan D02 T11 §17 |  |
| NP-1701 | Live Paint bucket options | AI-0598 | -- | core | plan D02 T11 §17 |  |
| NP-1702 | Live Paint selection tool | AI-0600 | -- | core | plan D02 T11 §17 |  |
| NP-1703 | Live Paint merge | AI-0601 | -- | core | plan D02 T11 §17 |  |
| NP-1704 | Live Paint release | AI-0602 | -- | core | plan D02 T11 §17 |  |
| NP-1705 | Live Paint expand | AI-0603 | -- | core | plan D02 T11 §17 |  |
| NP-1706 | Live Paint gap options and show gaps | AI-0604, AI-0605 | -- | core | plan D02 T11 §17 |  |
| NP-1707 | Smart fill tool | -- | CD-1327, CD-1379 | core | plan D02 T11 §17 | two toolbox listings of one tool |
| NP-1708 | Smart fill fill and outline options | -- | CD-1380, CD-1381 | core | plan D02 T11 §17 |  |
| NP-1709 | Smart fill outside area | -- | CD-1382 | core | plan D02 T11 §17 |  |
| NP-1710 | Objects on path tool and attach | AI-0133, AI-0302 | -- | core | plan D02 T11 §18 |  |
| NP-1711 | Objects on path options: pivot, rotate, spacing, shuffle, move all | AI-0303 | -- | core | plan D02 T11 §18 |  |
| NP-1712 | Objects on path tool options | AI-0304 | -- | core | plan D02 T11 §18 |  |
| NP-1713 | Objects on path detach and expand | AI-0305 | -- | core | plan D02 T11 §18 |  |
| NP-1714 | Radial repeat and options | AI-0517, AI-0518 | -- | core | plan D02 T11 §18 |  |
| NP-1715 | Grid repeat and options | AI-0519, AI-0520 | -- | core | plan D02 T11 §18 |  |
| NP-1716 | Mirror repeat and options | AI-0521, AI-0522 | -- | core | plan D02 T11 §18 |  |
| NP-1717 | Release and expand repeats | AI-0523 | -- | core | plan D02 T11 §18 |  |
| NP-1718 | Fit objects to path panel | -- | CD-424, CD-474 | core | plan D02 T11 §18 |  |
| NP-1719 | Fit objects to path: keep originals | -- | CD-475 | core | plan D02 T11 §18 |  |
| NP-1720 | Fit objects to path: duplicates | -- | CD-476 | core | plan D02 T11 §18 |  |
| NP-1721 | Fit objects to path: group all objects | -- | CD-477 | core | plan D02 T11 §18 |  |
| NP-1722 | Fit objects to path: treat as contiguous | -- | CD-478 | core | plan D02 T11 §18 |  |
| NP-1723 | Fit objects to path: order | -- | CD-479 | core | plan D02 T11 §18 |  |
| NP-1724 | Fit objects to path: distribution | -- | CD-480 | core | plan D02 T11 §18 |  |
| NP-1725 | Fit objects to path: reference point | -- | CD-481 | core | plan D02 T11 §18 |  |
| NP-1726 | Fit objects to path rotation: ignore initial, style, start, spin, revolutions, range | -- | CD-482, CD-483, CD-484 | core | plan D02 T11 §18 |  |

## Bitmaps and placed images

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1727 | Resample interpolation (nearest neighbor, bilinear, bicubic, Lanczos) | -- | CD-1972, CD-1973 | core | plan D01 T03 §2 | adds bilinear and Lanczos beyond the two Corel modes |
| NP-1728 | Resample: maintain aspect ratio | -- | CD-1977 | core | plan D01 T03 §2 |  |
| NP-1729 | Resample: maintain original file size | -- | CD-1978 | core | plan D01 T03 §2 |  |
| NP-1730 | Resample: resolution change (horizontal and vertical dpi) | -- | CD-1979 | core | plan D01 T03 §2 |  |
| NP-1731 | GPU resampling path decision | -- | CD-1980 | ai | plan D01 T03 §2 | managed SIMD CPU path is the default; AI upsampling itself is D02 T15 §9 |
| NP-1732 | Lens distortion correction (barrel and pincushion) | -- | CD-1982 | core | plan D01 T03 §2 |  |
| NP-1733 | Vertical and horizontal perspective correction | -- | CD-1986 | core | plan D01 T03 §2 |  |
| NP-1734 | 1-bit conversion: line art threshold | -- | CD-1996 | core | plan D01 T03 §3 |  |
| NP-1735 | 1-bit conversion: ordered dither | -- | CD-1997 | core | plan D01 T03 §3 |  |
| NP-1736 | 1-bit conversion: halftone screen (type, angle, frequency) | -- | CD-1998 | core | plan D01 T03 §3 |  |
| NP-1737 | 1-bit conversion: cardinality-distribution dither | -- | CD-1999 | core | plan D01 T03 §3 |  |
| NP-1738 | 1-bit conversion: Jarvis error diffusion | -- | CD-2000 | core | plan D01 T03 §3 |  |
| NP-1739 | 1-bit conversion: Stucki error diffusion | -- | CD-2001 | core | plan D01 T03 §3 |  |
| NP-1740 | 1-bit conversion: Floyd-Steinberg error diffusion | -- | CD-2002 | core | plan D01 T03 §3 |  |
| NP-1741 | Palette: uniform colors | -- | CD-2010 | core | plan D01 T03 §3 |  |
| NP-1742 | Palette: standard VGA 16 colors | -- | CD-2011 | core | plan D01 T03 §3 |  |
| NP-1743 | Palette: adaptive | -- | CD-2012 | core | plan D01 T03 §3 |  |
| NP-1744 | Palette: optimized (most frequent colors) | -- | CD-2013 | core | plan D01 T03 §3 |  |
| NP-1745 | Palette: grayscale 256 | -- | CD-2014 | core | plan D01 T03 §3 |  |
| NP-1746 | Palette: system | -- | CD-2015 | core | plan D01 T03 §3 | the Windows 20-color system palette recorded as a fixed table |
| NP-1747 | Palette: custom (built or opened palette file) | -- | CD-2016 | core | plan D01 T03 §3 |  |
| NP-1748 | Paletted dithering method and intensity | -- | CD-2017 | core | plan D01 T03 §3 |  |
| NP-1749 | Paletted conversion presets (save and load) | -- | CD-2018 | core | plan D01 T03 §3 |  |
| NP-1750 | Processed palette editing and save | -- | CD-2019 | core | plan D01 T03 §3 |  |
| NP-1751 | Color range sensitivity for the optimized palette | -- | CD-2020 | core | plan D01 T03 §3 |  |
| NP-1752 | Posterize | -- | CD-2224 | core | plan D01 T03 §3 |  |
| NP-1753 | Crop image (on-canvas handles) | AI-0205 | -- | core | plan D02 T12 §1 |  |
| NP-1754 | Crop image resolution | AI-0206 | -- | core | plan D02 T12 §1 |  |
| NP-1755 | Make pixel perfect | AI-0210 | -- | core | plan D02 T12 §1 |  |
| NP-1756 | Rasterize or convert to bitmap (resolution, color mode) | AI-0211 | CD-1961 | core | plan D02 T12 §1 |  |
| NP-1757 | Convert to bitmap: dithered | -- | CD-1962 | core | plan D02 T12 §1 |  |
| NP-1758 | Convert to bitmap: always overprint black | -- | CD-1963 | print | plan D02 T12 §1 |  |
| NP-1759 | Convert to bitmap: anti-aliasing | -- | CD-1964 | core | plan D02 T12 §1 |  |
| NP-1760 | Convert to bitmap: transparent background | -- | CD-1965 | core | plan D02 T12 §1 |  |
| NP-1761 | Convert to bitmap on export (size, resolution, mode, dithering) | -- | CD-1966 | format | plan D02 T12 §1 |  |
| NP-1762 | Bitmap info on the status bar | -- | CD-1968 | core | plan D02 T12 §1 |  |
| NP-1763 | Crop bitmap to an irregular shape | -- | CD-1969, CD-2074 | core | plan D02 T12 §1 |  |
| NP-1764 | Shape tool node editing of the bitmap boundary | -- | CD-1970 | core | plan D02 T12 §1 |  |
| NP-1765 | Resample dialog | -- | CD-1971 | core | plan D02 T12 §1 |  |
| NP-1766 | Straighten image (rotate up to 15 degrees with preview) | -- | CD-1981 | core | plan D02 T12 §1 |  |
| NP-1767 | Straighten crop options | -- | CD-1983 | core | plan D02 T12 §1 |  |
| NP-1768 | Straighten grid size and color | -- | CD-1984 | core | plan D02 T12 §1 |  |
| NP-1769 | Straighten remember settings | -- | CD-1985 | core | plan D02 T12 §1 |  |
| NP-1770 | Color a monochrome bitmap from the palette | -- | CD-1988 | core | plan D02 T12 §1 |  |
| NP-1771 | Bitmap color mask panel | -- | CD-1990, CD-2076, CD-2093 | core | plan D02 T12 §1 | menu and docker listings of one panel |
| NP-1772 | Bitmap mask: hide or show selected colors | -- | CD-1991 | core | plan D02 T12 §1 |  |
| NP-1773 | Bitmap mask tolerance | -- | CD-1992 | core | plan D02 T12 §1 |  |
| NP-1774 | Save and open a bitmap color mask | -- | CD-1993 | core | plan D02 T12 §1 | reads the Corel .ini mask; saves Nodus JSON |
| NP-1775 | Edit a masked color | -- | CD-1994 | core | plan D02 T12 §1 |  |
| NP-1776 | Bitmap mode: black and white (1-bit) | -- | CD-1995, CD-2077 | core | plan D02 T12 §1 |  |
| NP-1777 | Bitmap mode: grayscale (8-bit) | -- | CD-2003, CD-2078 | core | plan D02 T12 §1 |  |
| NP-1778 | Bitmap mode: duotone (8-bit) | -- | CD-2004, CD-2079 | print | plan D02 T12 §1 | command lands here; the conversion is D01 T04 §3 (Phase 10), disabled until then |
| NP-1779 | Bitmap mode: paletted (8-bit) | -- | CD-2009, CD-2080 | core | plan D02 T12 §1 |  |
| NP-1780 | Bitmap mode: RGB (24-bit) | -- | CD-2021, CD-2081 | core | plan D02 T12 §1 |  |
| NP-1781 | Bitmap mode: Lab (24-bit) | -- | CD-2022, CD-2082 | core | plan D02 T12 §1 | command lands here; the conversion is D01 T04 §3 (Phase 10), disabled until then |
| NP-1782 | Bitmap mode: CMYK (32-bit) | -- | CD-2023, CD-2083 | print | plan D02 T12 §1 | command lands here; the conversion is D01 T04 §3 (Phase 10), disabled until then |
| NP-1783 | Correct perspective | -- | CD-2075 | core | plan D02 T12 §1 |  |
| NP-1784 | Object mosaic (raster to vector tiles) | AI-0209 | -- | core | plan D02 T12 §6 |  |
| NP-1785 | Create mockup on a photo surface | AI-0953 | -- | core | plan D02 T12 §6 |  |
| NP-1786 | Mockup templates: save locally and preview | AI-0954, AI-0956 | -- | core | plan D02 T12 §6 | local templates only, no cloud template library |
| NP-1787 | Edit mockup content, edit mockup, release | AI-0955 | -- | core | plan D02 T12 §6 |  |
| NP-1788 | Pointillizer vector mosaic panel | -- | CD-2226, CD-2248, CD-2255 | core | plan D02 T12 §6 | menu and docker listings of one panel |
| NP-1789 | Pointillizer density | -- | CD-2227 | core | plan D02 T12 §6 |  |
| NP-1790 | Pointillizer scale | -- | CD-2228 | core | plan D02 T12 §6 |  |
| NP-1791 | Pointillizer screen angle | -- | CD-2229 | core | plan D02 T12 §6 |  |
| NP-1792 | Pointillizer keep original | -- | CD-2230 | core | plan D02 T12 §6 |  |
| NP-1793 | Pointillizer limit colors | -- | CD-2231 | core | plan D02 T12 §6 |  |
| NP-1794 | Pointillizer tracking methods (uniform, opacity, luminosity) | -- | CD-2232, CD-2233, CD-2234 | core | plan D02 T12 §6 |  |
| NP-1795 | Pointillizer merge adjacent tiles | -- | CD-2235 | core | plan D02 T12 §6 |  |
| NP-1796 | Pointillizer weld adjacent overlap | -- | CD-2236 | core | plan D02 T12 §6 |  |
| NP-1797 | Pointillizer tile shape (preset or custom) | -- | CD-2237 | core | plan D02 T12 §6 |  |
| NP-1798 | PhotoCocktail image mosaic panel | -- | CD-2238, CD-2247, CD-2256 | core | plan D02 T12 §6 | menu and docker listings of one panel |
| NP-1799 | PhotoCocktail tile library folder | -- | CD-2239 | core | plan D02 T12 §6 |  |
| NP-1800 | PhotoCocktail keep original | -- | CD-2240 | core | plan D02 T12 §6 |  |
| NP-1801 | PhotoCocktail grid columns and rows | -- | CD-2241 | core | plan D02 T12 §6 |  |
| NP-1802 | PhotoCocktail blending | -- | CD-2242 | core | plan D02 T12 §6 |  |
| NP-1803 | PhotoCocktail duplicates and spacing | -- | CD-2243 | core | plan D02 T12 §6 |  |
| NP-1804 | PhotoCocktail composition (single bitmap, stack, array) | -- | CD-2244 | core | plan D02 T12 §6 |  |
| NP-1805 | PhotoCocktail edges | -- | CD-2245 | core | plan D02 T12 §6 |  |
| NP-1806 | PhotoCocktail output priority (DPI or dimensions) | -- | CD-2246 | core | plan D02 T12 §6 |  |
| NP-1807 | Links panel | AI-0933 | CD-1748 | core | plan D02 T12 §7 |  |
| NP-1808 | Relink, update link, and go to link | AI-0934 | CD-2487 | core | plan D02 T12 §7 | CD-2487 is the Corel sync of the same update |
| NP-1809 | Relink all instances at once | AI-0935 | -- | core | plan D02 T12 §7 |  |
| NP-1810 | Auto relink missing files from the same folder | AI-0936 | -- | core | plan D02 T12 §7 |  |
| NP-1811 | Edit original | AI-0937, AI-1103 | CD-2486 | core | plan D02 T12 §7 |  |
| NP-1812 | Embed, unembed, and break link | AI-0938 | CD-2488 | core | plan D02 T12 §7 |  |
| NP-1813 | Link file info | AI-0939 | -- | core | plan D02 T12 §7 |  |
| NP-1814 | Placement options | AI-0940 | -- | core | plan D02 T12 §7 |  |
| NP-1815 | Links filters and sort (missing, modified, embedded) | AI-0941 | -- | core | plan D02 T12 §7 |  |
| NP-1816 | Update links preference (automatic, manual, ask) | AI-0942, AI-1178 | -- | core | plan D02 T12 §7 |  |
| NP-1817 | Low resolution proxy for linked EPS | AI-1176 | -- | core | plan D02 T12 §7 |  |
| NP-1818 | Edit original with the system default app | AI-1179 | -- | core | plan D02 T12 §7 |  |
| NP-1819 | Linked symbol libraries view | -- | CD-263 | core | plan D02 T12 §7 |  |
| NP-1820 | Sources panel (linked sources and attribution) | -- | CD-580, CD-2484 | core | plan D02 T12 §7 |  |
| NP-1821 | Linked documents and spreadsheet tables as sources | -- | CD-1686 | core | plan D02 T12 §7 | CDR sources read through the D02 T14 reader; XLS through NPOI |
| NP-1822 | Place or import as a linked file | -- | CD-1967, CD-2463, CD-2473, CD-2485 | core | plan D02 T12 §7 |  |
| NP-1823 | Edit bitmap in Imago and return on save | -- | CD-2073 | core | plan D02 T12 §7 | Imago stands in for PHOTO-PAINT |

## Raster effects and adjustments

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-1824 | Automatic conversion to RGB for RGB-only effects | -- | CD-2108 | core | plan D01 T03 §1 | the engine works on RGBA buffers; the source mode comes back on flatten only where lossless |
| NP-1825 | Inflate bitmap manually (by pixels or percent, keep aspect) | -- | CD-2109 | core | plan D01 T03 §1 |  |
| NP-1826 | Auto inflate bitmaps for effects (command and document default) | -- | CD-2110, CD-2111 | core | plan D01 T03 §1 | merges the command and the document option |
| NP-1827 | Auto adjust (tone and color) | -- | CD-2271 | core | plan D01 T03 §4 |  |
| NP-1828 | Levels with histogram and sampling | -- | CD-2272 | core | plan D01 T03 §4 |  |
| NP-1829 | Equalize | -- | CD-2273 | core | plan D01 T03 §4 |  |
| NP-1830 | Sample and target | -- | CD-2274 | core | plan D01 T03 §4 |  |
| NP-1831 | Tone curve (curve, straight, freehand, gamma styles; presets) | -- | CD-2275, CD-2276 | core | plan D01 T03 §4 | Corel .pst curve presets read for import only |
| NP-1832 | Tone curve: all channels display, smooth, mirror, reset | -- | CD-2277 | core | plan D01 T03 §4 |  |
| NP-1833 | Light (brightness, contrast, intensity, highlights, shadows, midtones) | -- | CD-2278 | core | plan D01 T03 §4 |  |
| NP-1834 | Gamma | -- | CD-2280 | core | plan D01 T03 §4 |  |
| NP-1835 | White balance | -- | CD-2281 | core | plan D01 T03 §4 |  |
| NP-1836 | Invert colors | -- | CD-2223 | core | plan D01 T03 §5 |  |
| NP-1837 | Threshold | -- | CD-2225 | core | plan D01 T03 §5 |  |
| NP-1838 | Color balance with preserve luminance | -- | CD-2279 | core | plan D01 T03 §5 |  |
| NP-1839 | Hue, saturation, lightness (master and per range) | -- | CD-2282 | core | plan D01 T03 §5 |  |
| NP-1840 | Black and white (per-color intensity and tint) | -- | CD-2283, CD-2291 | core | plan D01 T03 §5 | two listings of one adjustment |
| NP-1841 | Vibrance | -- | CD-2284 | core | plan D01 T03 §5 |  |
| NP-1842 | Selective color | -- | CD-2285 | core | plan D01 T03 §5 |  |
| NP-1843 | Replace colors (hue ring, saturation range, smoothing) | -- | CD-2286 | core | plan D01 T03 §5 |  |
| NP-1844 | Replace colors (legacy parameters) | -- | CD-2287 | core | plan D01 T03 §5 | reads legacy parameter sets and maps them onto the current filter |
| NP-1845 | Desaturate | -- | CD-2288 | core | plan D01 T03 §5 |  |
| NP-1846 | Channel mixer | -- | CD-2289 | core | plan D01 T03 §5 |  |
| NP-1847 | Gaussian blur | AI-0736 | CD-2142 | core | plan D01 T03 §6 |  |
| NP-1848 | Radial blur (spin) with quality and center | AI-0737 | CD-2146 | core | plan D01 T03 §6 | the Illustrator Zoom mode is served by the Zoom blur feature |
| NP-1849 | Smart blur (radius, threshold, edge modes) | AI-0738 | CD-2148 | core | plan D01 T03 §6 |  |
| NP-1850 | Tune blur (four variants with softer or sharper preview) | -- | CD-2140 | core | plan D01 T03 §6 |  |
| NP-1851 | Directional smooth | -- | CD-2141 | core | plan D01 T03 §6 |  |
| NP-1852 | Jaggy despeckle | -- | CD-2143 | core | plan D01 T03 §6 |  |
| NP-1853 | Low pass | -- | CD-2144 | core | plan D01 T03 §6 |  |
| NP-1854 | Motion blur | -- | CD-2145 | core | plan D01 T03 §6 |  |
| NP-1855 | Smooth | -- | CD-2149 | core | plan D01 T03 §6 |  |
| NP-1856 | Soften | -- | CD-2150 | core | plan D01 T03 §6 |  |
| NP-1857 | Zoom blur | -- | CD-2151, CD-2252 | core | plan D01 T03 §6 | two listings of one effect |
| NP-1858 | Local equalization | -- | CD-2167 | core | plan D01 T03 §6 |  |
| NP-1859 | Dust and scratch | -- | CD-2168 | core | plan D01 T03 §6 |  |
| NP-1860 | Tune sharpen | -- | CD-2169 | core | plan D01 T03 §6 |  |
| NP-1861 | Add noise (type and amount) | -- | CD-2197 | core | plan D01 T03 §6 |  |
| NP-1862 | 3-D stereo noise | -- | CD-2198 | core | plan D01 T03 §6 |  |
| NP-1863 | Maximum | -- | CD-2199 | core | plan D01 T03 §6 |  |
| NP-1864 | Median | -- | CD-2200 | core | plan D01 T03 §6 |  |
| NP-1865 | Minimum | -- | CD-2201 | core | plan D01 T03 §6 |  |
| NP-1866 | Tune noise (nine variants) | -- | CD-2202 | core | plan D01 T03 §6 |  |
| NP-1867 | Remove moire | -- | CD-2203 | core | plan D01 T03 §6 |  |
| NP-1868 | Remove noise | -- | CD-2204 | core | plan D01 T03 §6 |  |
| NP-1869 | Adaptive unsharp | -- | CD-2205 | core | plan D01 T03 §6 |  |
| NP-1870 | Directional sharpen | -- | CD-2206 | core | plan D01 T03 §6 |  |
| NP-1871 | High pass | -- | CD-2207 | core | plan D01 T03 §6 |  |
| NP-1872 | Sharpen (edge level, threshold, preserve colors) | -- | CD-2208 | core | plan D01 T03 §6 |  |
| NP-1873 | Unsharp mask | -- | CD-2209 | core | plan D01 T03 §6 |  |
| NP-1874 | Bokeh blur | -- | CD-2251 | core | plan D01 T03 §6 |  |
| NP-1875 | Diffuse glow | AI-0747 | -- | core | plan D01 T03 §7 |  |
| NP-1876 | Glass distortion | AI-0748 | -- | core | plan D01 T03 §7 |  |
| NP-1877 | Ocean ripple | AI-0749 | -- | core | plan D01 T03 §7 |  |
| NP-1878 | Texture and glass surface controls (scaling, relief, light, invert, load texture) | AI-0777 | -- | core | plan D01 T03 §7 |  |
| NP-1879 | 3-D rotate with best fit | -- | CD-2115 | core | plan D01 T03 §7 |  |
| NP-1880 | Cylinder | -- | CD-2117 | core | plan D01 T03 §7 |  |
| NP-1881 | Emboss (depth, level, direction, color modes) | -- | CD-2118 | core | plan D01 T03 §7 |  |
| NP-1882 | Page curl | -- | CD-2120 | core | plan D01 T03 §7 |  |
| NP-1883 | Pinch and punch | -- | CD-2121 | core | plan D01 T03 §7 |  |
| NP-1884 | Sphere | -- | CD-2122 | core | plan D01 T03 §7 |  |
| NP-1885 | Zig zag (bitmap) | -- | CD-2124 | core | plan D01 T03 §7 |  |
| NP-1886 | Blocks | -- | CD-2185 | core | plan D01 T03 §7 |  |
| NP-1887 | Displace (displacement map image) | -- | CD-2186 | core | plan D01 T03 §7 |  |
| NP-1888 | Mesh warp with presets | -- | CD-2187 | core | plan D01 T03 §7 |  |
| NP-1889 | Offset (tile, stretch, or color fill) | -- | CD-2188 | core | plan D01 T03 §7 |  |
| NP-1890 | Pixelate (square, rectangular, circular cells) | -- | CD-2189 | core | plan D01 T03 §7 |  |
| NP-1891 | Ripple | -- | CD-2190 | core | plan D01 T03 §7 |  |
| NP-1892 | Shear | -- | CD-2191 | core | plan D01 T03 §7 |  |
| NP-1893 | Swirl | -- | CD-2192 | core | plan D01 T03 §7 |  |
| NP-1894 | Tile | -- | CD-2193 | core | plan D01 T03 §7 |  |
| NP-1895 | Wet paint | -- | CD-2194 | core | plan D01 T03 §7 |  |
| NP-1896 | Whirlpool with savable styles | -- | CD-2195 | core | plan D01 T03 §7 |  |
| NP-1897 | Wind | -- | CD-2196 | core | plan D01 T03 §7 |  |
| NP-1898 | Colored pencil | AI-0721 | -- | core | plan D01 T03 §8 |  |
| NP-1899 | Cutout | AI-0722 | -- | core | plan D01 T03 §8 |  |
| NP-1900 | Dry brush | AI-0723 | -- | core | plan D01 T03 §8 |  |
| NP-1901 | Film grain | AI-0724 | -- | core | plan D01 T03 §8 |  |
| NP-1902 | Fresco | AI-0725 | -- | core | plan D01 T03 §8 |  |
| NP-1903 | Neon glow | AI-0726 | -- | core | plan D01 T03 §8 |  |
| NP-1904 | Paint daubs (brush size and type) | AI-0727 | -- | core | plan D01 T03 §8 |  |
| NP-1905 | Palette knife | AI-0728 | CD-2131 | core | plan D01 T03 §8 |  |
| NP-1906 | Plastic wrap | AI-0729 | -- | core | plan D01 T03 §8 |  |
| NP-1907 | Poster edges | AI-0730 | -- | core | plan D01 T03 §8 |  |
| NP-1908 | Rough pastels | AI-0731 | -- | core | plan D01 T03 §8 |  |
| NP-1909 | Smudge stick | AI-0732 | -- | core | plan D01 T03 §8 |  |
| NP-1910 | Sponge | AI-0733 | -- | core | plan D01 T03 §8 |  |
| NP-1911 | Underpainting | AI-0734 | CD-2221 | core | plan D01 T03 §8 | CD-2221 moved here from D01 T03 §10: same effect in both apps |
| NP-1912 | Watercolor | AI-0735 | CD-2137 | core | plan D01 T03 §8 |  |
| NP-1913 | Pointillist and pointillize (colored dots) | AI-0753 | CD-2134 | core | plan D01 T03 §8 | AI-0753 moved here from D01 T03 §11: same effect in both apps |
| NP-1914 | Charcoal | AI-0756 | CD-2125 | core | plan D01 T03 §8 | AI-0756 moved here from D01 T03 §9: same effect in both apps |
| NP-1915 | Conte crayon | AI-0758 | CD-2126 | core | plan D01 T03 §8 | AI-0758 moved here from D01 T03 §9: same effect in both apps |
| NP-1916 | Crayon | -- | CD-2127 | core | plan D01 T03 §8 |  |
| NP-1917 | Cubist | -- | CD-2128 | core | plan D01 T03 §8 |  |
| NP-1918 | Dabble | -- | CD-2129 | core | plan D01 T03 §8 |  |
| NP-1919 | Impressionist | -- | CD-2130 | core | plan D01 T03 §8 |  |
| NP-1920 | Pastels | -- | CD-2132 | core | plan D01 T03 §8 |  |
| NP-1921 | Pen and ink (cross-hatch or stipple) | -- | CD-2133, CD-2250 | core | plan D01 T03 §8 | two listings of one effect |
| NP-1922 | Scraperboard | -- | CD-2135 | core | plan D01 T03 §8 |  |
| NP-1923 | Sketch pad | -- | CD-2136 | core | plan D01 T03 §8 |  |
| NP-1924 | Water marker | -- | CD-2138 | core | plan D01 T03 §8 |  |
| NP-1925 | Wave paper | -- | CD-2139 | core | plan D01 T03 §8 |  |
| NP-1926 | Accented edges | AI-0739 | -- | core | plan D01 T03 §9 |  |
| NP-1927 | Angled strokes | AI-0740 | -- | core | plan D01 T03 §9 |  |
| NP-1928 | Crosshatch | AI-0741 | -- | core | plan D01 T03 §9 |  |
| NP-1929 | Dark strokes | AI-0742 | -- | core | plan D01 T03 §9 |  |
| NP-1930 | Ink outlines | AI-0743 | -- | core | plan D01 T03 §9 |  |
| NP-1931 | Spatter | AI-0744 | -- | core | plan D01 T03 §9 |  |
| NP-1932 | Sprayed strokes | AI-0745 | -- | core | plan D01 T03 §9 |  |
| NP-1933 | Sumi-e | AI-0746 | -- | core | plan D01 T03 §9 |  |
| NP-1934 | Bas relief | AI-0754 | -- | core | plan D01 T03 §9 |  |
| NP-1935 | Chalk and charcoal | AI-0755 | -- | core | plan D01 T03 §9 |  |
| NP-1936 | Chrome | AI-0757 | -- | core | plan D01 T03 §9 |  |
| NP-1937 | Graphic pen | AI-0759 | -- | core | plan D01 T03 §9 |  |
| NP-1938 | Halftone pattern (sketch) | AI-0760 | -- | core | plan D01 T03 §9 |  |
| NP-1939 | Note paper | AI-0761 | -- | core | plan D01 T03 §9 |  |
| NP-1940 | Photocopy | AI-0762 | -- | core | plan D01 T03 §9 |  |
| NP-1941 | Plaster | AI-0763 | -- | core | plan D01 T03 §9 |  |
| NP-1942 | Reticulation | AI-0764 | -- | core | plan D01 T03 §9 |  |
| NP-1943 | Stamp | AI-0765 | -- | core | plan D01 T03 §9 |  |
| NP-1944 | Torn edges | AI-0766 | -- | core | plan D01 T03 §9 |  |
| NP-1945 | Water paper | AI-0767 | -- | core | plan D01 T03 §9 |  |
| NP-1946 | Glowing edges | AI-0768 | -- | core | plan D01 T03 §9 |  |
| NP-1947 | Crystallize | AI-0751 | CD-2172 | core | plan D01 T03 §10 | AI-0751 moved here from D01 T03 §11: same effect in both apps |
| NP-1948 | Craquelure | AI-0769 | -- | core | plan D01 T03 §10 |  |
| NP-1949 | Grain (eleven grain types) | AI-0770 | -- | core | plan D01 T03 §10 |  |
| NP-1950 | Mosaic tiles | AI-0771 | -- | core | plan D01 T03 §10 |  |
| NP-1951 | Patchwork | AI-0772 | -- | core | plan D01 T03 §10 |  |
| NP-1952 | Stained glass (cells with solder) | AI-0773 | CD-2179 | core | plan D01 T03 §10 |  |
| NP-1953 | Texturizer (built-in or loaded texture) | AI-0774 | -- | core | plan D01 T03 §10 |  |
| NP-1954 | Fabric | -- | CD-2173 | core | plan D01 T03 §10 |  |
| NP-1955 | Frame (preset or custom frame image) | -- | CD-2174 | core | plan D01 T03 §10 | own frame and canvas images only, no Corel content packs |
| NP-1956 | Glass block | -- | CD-2175 | core | plan D01 T03 §10 |  |
| NP-1957 | Mosaic (elliptical pieces) | -- | CD-2176 | core | plan D01 T03 §10 |  |
| NP-1958 | Scatter | -- | CD-2177 | core | plan D01 T03 §10 |  |
| NP-1959 | Smoked glass | -- | CD-2178 | core | plan D01 T03 §10 |  |
| NP-1960 | Vignette | -- | CD-2180 | core | plan D01 T03 §10 |  |
| NP-1961 | Vortex | -- | CD-2181 | core | plan D01 T03 §10 |  |
| NP-1962 | Brick wall | -- | CD-2210 | core | plan D01 T03 §10 |  |
| NP-1963 | Bubbles | -- | CD-2211 | core | plan D01 T03 §10 |  |
| NP-1964 | Canvas (preset or loaded canvas map) | -- | CD-2212 | core | plan D01 T03 §10 | own frame and canvas images only, no Corel content packs |
| NP-1965 | Cobblestone | -- | CD-2213 | core | plan D01 T03 §10 |  |
| NP-1966 | Elephant skin | -- | CD-2214 | core | plan D01 T03 §10 |  |
| NP-1967 | Etching | -- | CD-2215 | core | plan D01 T03 §10 |  |
| NP-1968 | Plastic | -- | CD-2216 | core | plan D01 T03 §10 |  |
| NP-1969 | Plaster wall | -- | CD-2217 | core | plan D01 T03 §10 |  |
| NP-1970 | Relief sculpture | -- | CD-2218 | core | plan D01 T03 §10 |  |
| NP-1971 | Screen door | -- | CD-2219 | core | plan D01 T03 §10 |  |
| NP-1972 | Stone | -- | CD-2220 | core | plan D01 T03 §10 |  |
| NP-1973 | The Boss (bitmap bevel) | -- | CD-2249 | core | plan D01 T03 §10 |  |
| NP-1974 | Color halftone (max radius, screen angles) | AI-0750 | CD-2161 | core | plan D01 T03 §11 |  |
| NP-1975 | Mezzotint | AI-0752 | -- | core | plan D01 T03 §11 |  |
| NP-1976 | De-interlace | AI-0775 | CD-2222 | core | plan D01 T03 §11 |  |
| NP-1977 | NTSC colors (broadcast-safe gamut) | AI-0776 | -- | core | plan D01 T03 §11 |  |
| NP-1978 | Colorize | -- | CD-2152 | core | plan D01 T03 §11 |  |
| NP-1979 | Diffuse | -- | CD-2153 | core | plan D01 T03 §11 |  |
| NP-1980 | Lens flare | -- | CD-2154 | core | plan D01 T03 §11 |  |
| NP-1981 | Lighting effects with savable presets | -- | CD-2155 | core | plan D01 T03 §11 |  |
| NP-1982 | Photo filter | -- | CD-2156 | core | plan D01 T03 §11 |  |
| NP-1983 | Sepia toning | -- | CD-2157 | core | plan D01 T03 §11 |  |
| NP-1984 | Spot filter | -- | CD-2158 | core | plan D01 T03 §11 |  |
| NP-1985 | Time machine (historic photo styles) | -- | CD-2159 | core | plan D01 T03 §11 |  |
| NP-1986 | Bit planes | -- | CD-2160 | core | plan D01 T03 §11 |  |
| NP-1987 | Psychedelic | -- | CD-2162 | core | plan D01 T03 §11 |  |
| NP-1988 | Solarize | -- | CD-2163 | core | plan D01 T03 §11 |  |
| NP-1989 | Edge detect | -- | CD-2164 | core | plan D01 T03 §11 |  |
| NP-1990 | Find edges | -- | CD-2165 | core | plan D01 T03 §11 |  |
| NP-1991 | Trace contour | -- | CD-2166 | core | plan D01 T03 §11 |  |
| NP-1992 | Band pass | -- | CD-2182 | core | plan D01 T03 §11 |  |
| NP-1993 | Bump map | -- | CD-2183 | core | plan D01 T03 §11 |  |
| NP-1994 | User-defined convolution kernel | -- | CD-2184, CD-2254 | core | plan D01 T03 §11 | two listings of one effect |
| NP-1995 | Document raster effects settings | AI-0644 | -- | core | plan D02 T12 §2 |  |
| NP-1996 | Rasterize as a live effect | AI-0694 | -- | core | plan D02 T12 §2 | moved here from D02 T12 §1: a live effect needs the stack this section builds |
| NP-1997 | Effect gallery | AI-0720 | -- | core | plan D02 T12 §2 |  |
| NP-1998 | Bitmap effect lens over an image area | -- | CD-1920, CD-2098 | core | plan D02 T12 §2 |  |
| NP-1999 | Non-destructive effect stack in the FX panel | -- | CD-2094, CD-2095, CD-2099 | core | plan D02 T12 §2 |  |
| NP-2000 | Bitmap effects on vector and bitmap objects | -- | CD-2096, CD-2097 | core | plan D02 T12 §2 |  |
| NP-2001 | Add effect | -- | CD-2100 | core | plan D02 T12 §2 |  |
| NP-2002 | Show or hide one effect | -- | CD-2101 | core | plan D02 T12 §2 |  |
| NP-2003 | Show or hide all effects of an object | -- | CD-2102 | core | plan D02 T12 §2 |  |
| NP-2004 | Reorder applied effects | -- | CD-2103 | core | plan D02 T12 §2 |  |
| NP-2005 | Delete an applied effect | -- | CD-2104 | core | plan D02 T12 §2 |  |
| NP-2006 | Effect before and after preview (full and split) | -- | CD-2105 | core | plan D02 T12 §2 |  |
| NP-2007 | Reset effect settings | -- | CD-2106 | core | plan D02 T12 §2 |  |
| NP-2008 | Flatten effects | -- | CD-2107 | core | plan D02 T12 §2 |  |
| NP-2009 | Adjustment presets (multi-filter) | -- | CD-2257 | core | plan D02 T12 §3 |  |
| NP-2010 | Image Adjustment Lab | -- | CD-2258 | core | plan D02 T12 §3 |  |
| NP-2011 | Adjustment Lab: auto adjust | -- | CD-2259 | core | plan D02 T12 §3 |  |
| NP-2012 | Adjustment Lab: white point and black point tools | -- | CD-2260 | core | plan D02 T12 §3 |  |
| NP-2013 | Adjustment Lab: temperature | -- | CD-2261 | core | plan D02 T12 §3 |  |
| NP-2014 | Adjustment Lab: tint | -- | CD-2262 | core | plan D02 T12 §3 |  |
| NP-2015 | Adjustment Lab: saturation | -- | CD-2263 | core | plan D02 T12 §3 |  |
| NP-2016 | Adjustment Lab: brightness and contrast | -- | CD-2264 | core | plan D02 T12 §3 |  |
| NP-2017 | Adjustment Lab: highlights, shadows, midtones | -- | CD-2265 | core | plan D02 T12 §3 |  |
| NP-2018 | Adjustment Lab: histogram | -- | CD-2266 | core | plan D02 T12 §3 |  |
| NP-2019 | Adjustment Lab: snapshots | -- | CD-2267 | core | plan D02 T12 §3 |  |
| NP-2020 | Adjustment Lab: undo, redo, reset to original | -- | CD-2268 | core | plan D02 T12 §3 |  |
| NP-2021 | Adjustment Lab: remember settings | -- | CD-2269 | core | plan D02 T12 §3 |  |
| NP-2022 | Adjustment Lab: preview modes (full, before and after, split) | -- | CD-2270 | core | plan D02 T12 §3 |  |
| NP-2023 | Live preview of adjustments | -- | CD-2290 | core | plan D02 T12 §3 |  |
| NP-2024 | Apply SVG filter | AI-0701 | -- | format | plan D02 T12 §8 |  |
| NP-2025 | Import SVG filters and edit filter code | AI-0702 | -- | format | plan D02 T12 §8 |  |
| NP-2026 | Built-in SVG filter presets | AI-0703 | -- | format | plan D02 T12 §8 | own preset set; Adobe AI_ preset names not copied |
| NP-2027 | Third-party bitmap plug-in filters | AI-0778 | CD-2092, CD-2112, CD-2113 | core | backlog B-012 | 8BF-style plug-in host |

## Tracing

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2028 | Trace color mode (color, grayscale, black and white) | AI-0784 | CD-2051 | core | plan D02 T12 §4 |  |
| NP-2029 | Trace palette (automatic, limited, full tone, document swatches) | AI-0785 | -- | core | plan D02 T12 §4 |  |
| NP-2030 | Trace paths, corners, and noise fidelity | AI-0786 | -- | core | plan D02 T12 §4 |  |
| NP-2031 | Trace method: abutting or overlapping (remove overlap) | AI-0787 | CD-2047 | core | plan D02 T12 §4 |  |
| NP-2032 | Trace output: fills, strokes, and maximum stroke width | AI-0788 | -- | core | plan D02 T12 §4 |  |
| NP-2033 | Snap curves to lines and ignore white | AI-0791 | -- | core | plan D02 T12 §4 |  |
| NP-2034 | Trace statistics (paths, anchors, colors) | AI-0792 | -- | core | plan D02 T12 §4 |  |
| NP-2035 | Trace detail | -- | CD-2042 | core | plan D02 T12 §4 |  |
| NP-2036 | Trace smoothing | -- | CD-2043 | core | plan D02 T12 §4 |  |
| NP-2037 | Corner smoothness | -- | CD-2044 | core | plan D02 T12 §4 |  |
| NP-2038 | Remove background (automatic or sampled color) | -- | CD-2046 | core | plan D02 T12 §4 |  |
| NP-2039 | Group traced objects by color | -- | CD-2048 | core | plan D02 T12 §4 |  |
| NP-2040 | Merge adjacent same-color objects | -- | CD-2049 | core | plan D02 T12 §4 |  |
| NP-2041 | Number of trace colors | -- | CD-2052 | core | plan D02 T12 §4 |  |
| NP-2042 | Trace lettering images into type outlines | AI-0423 | -- | core | plan D02 T12 §5 |  |
| NP-2043 | Image Trace panel (live trace object) | AI-0779 | -- | core | plan D02 T12 §5 |  |
| NP-2044 | Make, make and expand, release, and expand a trace | AI-0780 | -- | core | plan D02 T12 §5 |  |
| NP-2045 | One-click trace presets (auto color, high color, low color, grayscale, black and white, outline) | AI-0781 | -- | core | plan D02 T12 §5 |  |
| NP-2046 | Classic trace preset list | AI-0782 | -- | core | plan D02 T12 §5 |  |
| NP-2047 | Trace preview and view modes (result, outlines, overlay, source, side by side) | AI-0783 | CD-2036, CD-2037, CD-2038 | core | plan D02 T12 §5 |  |
| NP-2048 | Trace gradients with smoothness | AI-0789 | -- | core | plan D02 T12 §5 |  |
| NP-2049 | Trace basic shapes as live shapes | AI-0790 | -- | core | plan D02 T12 §5 |  |
| NP-2050 | Save and manage trace presets (import and export) | AI-0793 | -- | core | plan D02 T12 §5 |  |
| NP-2051 | Edit trace results (expand, Live Paint) | AI-0794 | -- | core | plan D02 T12 §5 |  |
| NP-2052 | Quick trace with default settings | -- | CD-2024, CD-2072 | core | plan D02 T12 §5 | CD-2072 lists the three trace commands together |
| NP-2053 | Centerline trace | -- | CD-2025 | core | plan D02 T12 §5 |  |
| NP-2054 | Centerline preset: technical illustration | -- | CD-2026, CD-2090 | core | plan D02 T12 §5 |  |
| NP-2055 | Centerline preset: line drawing | -- | CD-2027, CD-2091 | core | plan D02 T12 §5 |  |
| NP-2056 | Outline trace | -- | CD-2028 | core | plan D02 T12 §5 |  |
| NP-2057 | Outline preset: line art | -- | CD-2029, CD-2084 | core | plan D02 T12 §5 |  |
| NP-2058 | Outline preset: logo | -- | CD-2030, CD-2085 | core | plan D02 T12 §5 |  |
| NP-2059 | Outline preset: detailed logo | -- | CD-2031, CD-2086 | core | plan D02 T12 §5 |  |
| NP-2060 | Outline preset: clipart | -- | CD-2032, CD-2087 | core | plan D02 T12 §5 |  |
| NP-2061 | Outline preset: low quality image | -- | CD-2033, CD-2088 | core | plan D02 T12 §5 |  |
| NP-2062 | Outline preset: high quality image | -- | CD-2034, CD-2089 | core | plan D02 T12 §5 |  |
| NP-2063 | Trace dialog with settings, colors, and adjustments pages | -- | CD-2035 | core | plan D02 T12 §5 |  |
| NP-2064 | Trace dialog zoom, pan, and fit | -- | CD-2039 | core | plan D02 T12 §5 |  |
| NP-2065 | Switch trace type and image type in the dialog | -- | CD-2040 | core | plan D02 T12 §5 |  |
| NP-2066 | Trace result details and time estimate | -- | CD-2041 | core | plan D02 T12 §5 |  |
| NP-2067 | Delete or keep the original bitmap | -- | CD-2045 | core | plan D02 T12 §5 |  |
| NP-2068 | Trace dialog undo, redo, reset | -- | CD-2050 | core | plan D02 T12 §5 |  |
| NP-2069 | Sort trace colors by similarity or frequency | -- | CD-2053 | core | plan D02 T12 §5 |  |
| NP-2070 | Select and edit trace colors | -- | CD-2054 | core | plan D02 T12 §5 |  |
| NP-2071 | Merge trace colors | -- | CD-2055 | core | plan D02 T12 §5 |  |
| NP-2072 | Delete a trace color | -- | CD-2056 | core | plan D02 T12 §5 |  |
| NP-2073 | Open and save a trace color palette | -- | CD-2057 | core | plan D02 T12 §5 |  |
| NP-2074 | Pre-trace adjustments page | -- | CD-2058 | ai | plan D02 T12 §5 | classical adjustments and JPEG cleanup here; AI upsampling is D02 T15 §9 |
| NP-2075 | Trace defaults (quick trace method, merge colors behavior) | -- | CD-2889 | core | plan D02 T12 §5 |  |

## Color management

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2076 | Load ICC color profiles | -- | CD-1571 | core | plan D01 T04 §1 |  |
| NP-2077 | Color engine choice | -- | CD-1575 | core | plan D01 T04 §1 | one engine (lcms2) with WCS recorded as the rejected candidate; the setting shows the engine, not a choice |
| NP-2078 | Bring color into gamut | -- | CD-1561 | core | plan D01 T04 §2 |  |
| NP-2079 | Rendering intents: perceptual, relative, absolute, saturation | -- | CD-1565, CD-1566, CD-1567, CD-1568 | core | plan D01 T04 §2 |  |
| NP-2080 | Preserve pure black | -- | CD-1576 | core | plan D01 T04 §2 |  |
| NP-2081 | Map gray to CMYK black | -- | CD-1577 | print | plan D01 T04 §2 |  |
| NP-2082 | Duotone types: monotone to quadtone | -- | CD-2005 | print | plan D01 T04 §3 |  |
| NP-2083 | Duotone ink tone curves | -- | CD-2006 | print | plan D01 T04 §3 |  |
| NP-2084 | Duotone save and load inks | -- | CD-2007 | print | plan D01 T04 §3 |  |
| NP-2085 | Duotone overprint colors | -- | CD-2008 | print | plan D01 T04 §3 |  |
| NP-2086 | Color Settings dialog: default and document settings | AI-1095 | CD-1562, CD-1603, CD-1604 | core | plan D02 T13 §1 | Edit, Color Settings (Shift+Ctrl+K) with Default and Document tabs; Bridge sync excluded |
| NP-2087 | Assign profile (keep color numbers) | AI-1096 | CD-1573 | print | plan D02 T13 §1 |  |
| NP-2088 | Appearance of black on screen and in output | AI-1097, AI-1183 | -- | print | plan D02 T13 §1 | rich versus accurate black |
| NP-2089 | Extract an embedded ICC profile on open or import | -- | CD-229, CD-2476 | core | plan D02 T13 §1 |  |
| NP-2090 | Keep an embedded ICC profile as the document profile on open | -- | CD-233 | core | plan D02 T13 §1 |  |
| NP-2091 | Default working profiles for RGB, CMYK, and grayscale | -- | CD-1563 | core | plan D02 T13 §1 |  |
| NP-2092 | Primary color mode | -- | CD-1564 | core | plan D02 T13 §1 | extends the existing ColorMode enum |
| NP-2093 | Spot color definition policy (Lab, CMYK, or RGB values) | -- | CD-1569 | print | plan D02 T13 §1 |  |
| NP-2094 | Document color settings on the status bar | -- | CD-1570 | core | plan D02 T13 §1 |  |
| NP-2095 | Embed color profiles on save and export | -- | CD-1572 | core | plan D02 T13 §1 | SVG color-profile element, PDF OutputIntent and ICCBased |
| NP-2096 | Convert to profile (keep appearance, chosen intent) | -- | CD-1574 | core | plan D02 T13 §1 |  |
| NP-2097 | Color management presets with save and delete | -- | CD-1587, CD-1588 | core | plan D02 T13 §1 | regional presets rebuilt on bundled freely redistributable profiles |
| NP-2098 | Open policy per color mode | -- | CD-1589 | core | plan D02 T13 §1 |  |
| NP-2099 | Import and paste policy per color mode | -- | CD-1590 | core | plan D02 T13 §1 |  |
| NP-2100 | Missing and mismatched profile warnings on open, import, and paste | -- | CD-1591, CD-1592, CD-1593, CD-1594 | core | plan D02 T13 §1 |  |
| NP-2101 | Safe CMYK workflow (preserve CMYK numbers) | -- | CD-1596 | print | plan D02 T13 §1 |  |
| NP-2102 | Web color management (sRGB recommendation) | -- | CD-1597 | core | plan D02 T13 §1 |  |
| NP-2103 | Overprint preview (simulate overprints) | AI-0909 | CD-042, CD-120 | print | plan D02 T13 §6 |  |
| NP-2104 | Proof setup: device to simulate | AI-0914 | CD-1580 | print | plan D02 T13 §6 | color-blindness simulations included |
| NP-2105 | Proof colors toggle | AI-0915 | CD-1578, CD-1602 | core | plan D02 T13 §6 | View menu and status bar button |
| NP-2106 | Separations Preview panel | AI-1086 | -- | print | plan D02 T13 §6 |  |
| NP-2107 | Rasterize complex effects view | -- | CD-043, CD-121 | print | plan D02 T13 §6 |  |
| NP-2108 | Color Proofing panel | -- | CD-1579, CD-1605 | core | plan D02 T13 §6 |  |
| NP-2109 | Preserve numbers in the soft proof | -- | CD-1581 | core | plan D02 T13 §6 |  |
| NP-2110 | Proof rendering intent | -- | CD-1582 | core | plan D02 T13 §6 |  |
| NP-2111 | Gamut warning overlay | -- | CD-1583 | core | plan D02 T13 §6 |  |
| NP-2112 | Proof presets | -- | CD-1584 | core | plan D02 T13 §6 |  |
| NP-2113 | Export soft proof | -- | CD-1585 | format | plan D02 T13 §6 | JPEG, TIFF, PDF; CPT refused by name |
| NP-2114 | Print proof | -- | CD-1586 | print | plan D02 T13 §6 |  |
| NP-2115 | Preview separations in Print Preview | -- | CD-2668, CD-2791 | print | plan D02 T13 §6 |  |
| NP-2116 | Proof colors on by default | -- | CD-2887 | core | plan D02 T13 §6 |  |

## Print and prepress

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2117 | Print dialog and the Print command | AI-1066 | CD-2659, CD-2789 | print | plan D02 T13 §2 | Ctrl+P; category pages owned by later sections of this file |
| NP-2118 | Copies, collate, reverse order, and print range | AI-1067 | CD-2662, CD-2663 | print | plan D02 T13 §2 | pages, artboards, even, odd, selection, skip blank |
| NP-2119 | Media size and orientation from the print dialog | AI-1068, AI-1085 | CD-2661 | print | plan D02 T13 §2 | auto-rotate, transverse, match orientation |
| NP-2120 | Print layers: visible and printable, visible, all | AI-1069 | -- | print | plan D02 T13 §2 |  |
| NP-2121 | Art placement origin and drag in preview | AI-1070 | -- | print | plan D02 T13 §2 |  |
| NP-2122 | Scaling: as in document, fit to page, custom | AI-1071 | CD-2664 | print | plan D02 T13 §2 |  |
| NP-2123 | Print to PDF through the Nodus PDF writer | -- | CD-2658, CD-2721 | print | plan D02 T13 §2 | no virtual printer driver; the job goes to the D02 T13 §14 writer |
| NP-2124 | Printer selection and driver preferences | -- | CD-2660 | print | plan D02 T13 §2 | System.Printing PrintQueue and PrintTicket, or GDI per the recorded decision |
| NP-2125 | Print Preview window | -- | CD-2666 | print | plan D02 T13 §2 |  |
| NP-2126 | Mini preview in the Print dialog | -- | CD-2667 | print | plan D02 T13 §2 |  |
| NP-2127 | Print to fit the paper size (driver compatibility) | -- | CD-2675 | print | plan D02 T13 §2 |  |
| NP-2128 | Print tiling tool and show or hide tiling | AI-0900, AI-0918 | -- | print | plan D02 T13 §3 |  |
| NP-2129 | Tiled pages: full pages or imageable areas with overlap and tiling marks | AI-1072 | CD-2665 | print | plan D02 T13 §3 |  |
| NP-2130 | Print summary and save summary | AI-1082 | -- | print | plan D02 T13 §3 |  |
| NP-2131 | Print presets and print styles | AI-1083 | CD-2670 | print | plan D02 T13 §3 | saved as JSON files, import and export |
| NP-2132 | Print to file: PostScript, PDF, or PRN with split options | AI-1084 | CD-2722, CD-2723 | print | plan D02 T13 §3 | PostScript written by Nodus |
| NP-2133 | Crop marks live effect | AI-0673 | -- | print | plan D02 T13 §4 | live object per D02 T07 §1 |
| NP-2134 | Create trim marks as objects | AI-0674 | -- | print | plan D02 T13 §4 |  |
| NP-2135 | Printer's marks: crop and trim marks with weight, offset, and style | AI-1073 | CD-2739 | print | plan D02 T13 §4 | fold marks and exterior-only option included |
| NP-2136 | Japanese crop marks preference | AI-1098, AI-1128 | -- | print | plan D02 T13 §4 |  |
| NP-2137 | Composite crop marks on all plates | -- | CD-2740 | print | plan D02 T13 §4 |  |
| NP-2138 | Bleed and bleed limit | -- | CD-2741 | print | plan D02 T13 §4 |  |
| NP-2139 | Registration marks | -- | CD-2742 | print | plan D02 T13 §4 |  |
| NP-2140 | Color calibration bar | -- | CD-2743 | print | plan D02 T13 §4 |  |
| NP-2141 | Densitometer scales | -- | CD-2744 | print | plan D02 T13 §4 |  |
| NP-2142 | File information and page number marks | -- | CD-2745, CD-2746 | print | plan D02 T13 §4 |  |
| NP-2143 | Marks placement tool | -- | CD-2747 | print | plan D02 T13 §4 |  |
| NP-2144 | Marks attached to the object bounding box | -- | CD-2748 | print | plan D02 T13 §4 |  |
| NP-2145 | Composite or separations output (host-based and in-RIP) with plate choice | AI-1074 | CD-2750 | print | plan D02 T13 §5 | in-RIP only for PostScript devices |
| NP-2146 | Film output: emulsion down, negative, printer resolution | AI-1075 | CD-2769, CD-2770 | print | plan D02 T13 §5 |  |
| NP-2147 | Convert spot colors to process when printing | AI-1076 | CD-2682 | print | plan D02 T13 §5 | the overprint black half of AI-1076 is built with D02 T13 §7 |
| NP-2148 | Ink manager and halftone screens per plate | AI-1077 | CD-2752 | print | plan D02 T13 §5 | frequency, angle, dot shape, ink aliases |
| NP-2149 | Print color management: application or printer, printer profile, intent | AI-1080 | CD-1595, CD-2680, CD-2683, CD-2685 | print | plan D02 T13 §5 |  |
| NP-2150 | PostScript halftone screen on a bitmap | -- | CD-1989 | print | plan D02 T13 §5 |  |
| NP-2151 | Print with document color or proof settings | -- | CD-2679 | print | plan D02 T13 §5 |  |
| NP-2152 | Output colors: native, RGB, CMYK, or grayscale | -- | CD-2681 | print | plan D02 T13 §5 |  |
| NP-2153 | Preserve color numbers when printing | -- | CD-2684 | print | plan D02 T13 §5 |  |
| NP-2154 | Spot color separations warning threshold | -- | CD-2694 | print | plan D02 T13 §5 |  |
| NP-2155 | Separation order | -- | CD-2751 | print | plan D02 T13 §5 |  |
| NP-2156 | Trap command | AI-0204, AI-1089 | -- | print | plan D02 T13 §7 |  |
| NP-2157 | Overprint black by percentage (Edit Colors) | AI-0481 | -- | print | plan D02 T13 §7 |  |
| NP-2158 | Trap live effect | AI-0693 | -- | print | plan D02 T13 §7 | live object per D02 T07 §1 |
| NP-2159 | White overprint detection and discard | AI-0975, AI-1090 | -- | print | plan D02 T13 §7 |  |
| NP-2160 | Overprint fill and stroke on objects | AI-1087 | CD-544, CD-545, CD-1348, CD-1474, CD-2755, CD-2756 | print | plan D02 T13 §7 | Attributes panel, Object menu, context menu, Properties |
| NP-2161 | Attributes panel | AI-1088 | -- | core | plan D02 T13 §7 | overprint here; fill rule, reverse direction, image map, and note fields reuse their owning sections |
| NP-2162 | Overprint bitmap | -- | CD-546, CD-2757 | print | plan D02 T13 §7 |  |
| NP-2163 | Document overprints: ignore, preserve, or simulate | -- | CD-2753, CD-2754 | print | plan D02 T13 §7 |  |
| NP-2164 | Text overprint | -- | CD-2758 | print | plan D02 T13 §7 |  |
| NP-2165 | Overprint graphics or text per separation | -- | CD-2759 | print | plan D02 T13 §7 |  |
| NP-2166 | Always overprint black and the black threshold | -- | CD-2760, CD-2761 | print | plan D02 T13 §7 |  |
| NP-2167 | Auto-spreading trap | -- | CD-2762 | print | plan D02 T13 §7 |  |
| NP-2168 | In-RIP trapping and its settings | -- | CD-2763, CD-2764, CD-2765, CD-2766, CD-2767, CD-2768 | print | plan D02 T13 §7 | written as PostScript trapping parameters and the PDF Trapped key |
| NP-2169 | Compatible gradient and mesh printing and raster effects resolution | AI-1079 | -- | print | plan D02 T13 §8 |  |
| NP-2170 | Print as bitmap and print flattening options | AI-1081 | CD-2677 | print | plan D02 T13 §8 | CD-2677 moved here from D02 T13 §5: same rasterize-the-page capability |
| NP-2171 | Flatten Transparency command | AI-1091 | -- | print | plan D02 T13 §8 |  |
| NP-2172 | Flattener Preview panel | AI-1092 | -- | print | plan D02 T13 §8 |  |
| NP-2173 | Transparency flattener presets and preset libraries | AI-1093, AI-1104 | -- | print | plan D02 T13 §8 | perspective grid presets stay with D02 T11 §14 |
| NP-2174 | Gradient banding guidance | AI-1094 | -- | print | plan D02 T13 §8 |  |
| NP-2175 | Package and Collect for Output | AI-0977, AI-0978 | CD-2790 | print | plan D02 T13 §9 | copies fonts only when the embedding flags allow |
| NP-2176 | Preflight in Print, PDF, and export dialogs with savable styles | -- | CD-2669, CD-2696, CD-2781, CD-2788 | print | plan D02 T13 §9 |  |
| NP-2177 | Banded fountain fill check | -- | CD-2693 | print | plan D02 T13 §9 |  |
| NP-2178 | Many fonts preflight threshold | -- | CD-2695 | print | plan D02 T13 §9 |  |
| NP-2179 | PostScript level and data format | AI-1078 | CD-2687 | print | plan D02 T13 §10 | PostScript written by Nodus |
| NP-2180 | OPI proxies and maintained OPI links | -- | CD-2474, CD-2749, CD-2782 | print | plan D02 T13 §10 | OPI comments in PostScript and the PDF OPI dictionary |
| NP-2181 | Driver compatibility for non-PostScript printers | -- | CD-2671, CD-2672, CD-2673, CD-2674 | print | plan D02 T13 §10 | text as graphics, software clipping, 64k chunks, send curves |
| NP-2182 | Bitmap output threshold and chunk overlap | -- | CD-2676 | print | plan D02 T13 §10 |  |
| NP-2183 | Bitmap downsampling on print | -- | CD-2678 | print | plan D02 T13 §10 |  |
| NP-2184 | Use a PPD file | -- | CD-2686 | print | plan D02 T13 §10 |  |
| NP-2185 | PostScript bitmap compression | -- | CD-2688 | print | plan D02 T13 §10 |  |
| NP-2186 | Optimize fountain fills and auto increase steps | -- | CD-2689, CD-2690 | print | plan D02 T13 §10 |  |
| NP-2187 | Auto increase flatness | -- | CD-2691 | print | plan D02 T13 §10 |  |
| NP-2188 | Font download and TrueType to Type 1 | -- | CD-2692 | print | plan D02 T13 §10 | Type 42 for TrueType instead of conversion |
| NP-2189 | Imposition layout presets, edit, and save | -- | CD-2724, CD-2725 | print | plan D02 T13 §11 |  |
| NP-2190 | Imposition layout tool | -- | CD-2726 | print | plan D02 T13 §11 |  |
| NP-2191 | Pages across and down, single or double sided | -- | CD-2727 | print | plan D02 T13 §11 | manual-duplex wizard included |
| NP-2192 | Binding modes: perfect, saddle stitch, collate and cut, custom | -- | CD-2728, CD-2729, CD-2730, CD-2731 | print | plan D02 T13 §11 |  |
| NP-2193 | Page placement auto-ordering: intelligent, sequential, cloned | -- | CD-2732, CD-2733, CD-2734 | print | plan D02 T13 §11 |  |
| NP-2194 | Manual page sequence and rotation | -- | CD-2735 | print | plan D02 T13 §11 |  |
| NP-2195 | Gutters, cut and fold locations | -- | CD-2736, CD-2737 | print | plan D02 T13 §11 |  |
| NP-2196 | Imposition margins | -- | CD-2738 | print | plan D02 T13 §11 |  |
| NP-2197 | Page Layout dialog and full page style | -- | CD-2311, CD-2312, CD-2374 | core | plan D02 T13 §12 |  |
| NP-2198 | Book and booklet layout styles | -- | CD-2313, CD-2314 | print | plan D02 T13 §12 |  |
| NP-2199 | Folded card layout styles: tent, side-fold, top-fold | -- | CD-2315, CD-2316, CD-2317 | print | plan D02 T13 §12 |  |
| NP-2200 | Tri-fold brochure layout style | -- | CD-2318 | print | plan D02 T13 §12 |  |
| NP-2201 | Label presets | -- | CD-2319 | print | plan D02 T13 §12 | no manufacturer catalog bundled without a data license; users import label definitions |
| NP-2202 | Custom label styles | -- | CD-2320 | print | plan D02 T13 §12 |  |
| NP-2203 | Save page layout as default | -- | CD-2321 | core | plan D02 T13 §12 |  |
| NP-2204 | Border and Grommet banner document | -- | CD-2771 | print | plan D02 T13 §12 |  |
| NP-2205 | Banner border types | -- | CD-2772 | print | plan D02 T13 §12 |  |
| NP-2206 | Grommet size, margin, placement, and distribution | -- | CD-2773, CD-2774 | print | plan D02 T13 §12 |  |
| NP-2207 | Variables panel and variable types | AI-1234, AI-1235 | -- | automation | plan D02 T13 §13 | visibility, text, linked file, graph data |
| NP-2208 | Make dynamic, unbind, and select bound object | AI-1236 | -- | automation | plan D02 T13 §13 |  |
| NP-2209 | Data sets: capture, next, previous, rename, delete | AI-1237 | -- | automation | plan D02 T13 §13 |  |
| NP-2210 | Variable library XML and CSV data sources | AI-1238, AI-1239 | -- | automation | plan D02 T13 §13 |  |
| NP-2211 | Export one file per data set | AI-1240 | -- | automation | plan D02 T13 §13 | a Nodus command, not an Actions batch |
| NP-2212 | Print Merge: create, load, and edit | -- | CD-2697, CD-2698, CD-2699 | print | plan D02 T13 §13 |  |
| NP-2213 | Merge data source formats | -- | CD-2700 | print | plan D02 T13 §13 | TXT, CSV, RTF, XLSX |
| NP-2214 | Merge columns: types, configure, and import a column | -- | CD-2701, CD-2702, CD-2710 | print | plan D02 T13 §13 |  |
| NP-2215 | Merge records: add, edit, view, browse, and select | -- | CD-2703, CD-2704, CD-2705, CD-2706 | print | plan D02 T13 §13 |  |
| NP-2216 | Clear merge data and keep it in the document | -- | CD-2707, CD-2890 | print | plan D02 T13 §13 |  |
| NP-2217 | Save, import, and sync the data source | -- | CD-2708, CD-2709, CD-2712 | print | plan D02 T13 §13 |  |
| NP-2218 | ODBC data source | -- | CD-2711 | print | plan D02 T13 §13 | System.Data.Odbc |
| NP-2219 | Merge text field | -- | CD-2713 | print | plan D02 T13 §13 |  |
| NP-2220 | Merge image field and scaling | -- | CD-2714, CD-2715 | print | plan D02 T13 §13 |  |
| NP-2221 | Merge QR code field | -- | CD-2716 | print | plan D02 T13 §13 | ZXing.Net through D02 T16 §11 |
| NP-2222 | Update and find merge fields | -- | CD-2717, CD-2718 | print | plan D02 T13 §13 |  |
| NP-2223 | Print merged document | -- | CD-2719 | print | plan D02 T13 §13 |  |
| NP-2224 | Create merged document | -- | CD-2720 | print | plan D02 T13 §13 |  |

## PDF output

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2225 | Publish to PDF | -- | CD-2518 | core | plan D02 T13 §14 | own content-stream writer on PDFsharp (MIT) replaces the SKDocument exporter |
| NP-2226 | PDF export range | -- | CD-2525 | core | plan D02 T13 §14 | document, several documents, selection, current page, pages |
| NP-2227 | PDF page size from the document or the selection | -- | CD-2526 | core | plan D02 T13 §14 |  |
| NP-2228 | Export only objects on the page | -- | CD-2539 | core | plan D02 T13 §14 |  |
| NP-2229 | Embed and subset fonts | -- | CD-2540, CD-2542 | core | plan D02 T13 §14 |  |
| NP-2230 | Convert TrueType to Type 1 | -- | CD-2541 | core | plan D02 T13 §14 | not needed: TrueType and CFF embed directly; the option is a documented no-op |
| NP-2231 | Export all text as curves | -- | CD-2543 | core | plan D02 T13 §14 |  |
| NP-2232 | Preserve layers as optional content groups | -- | CD-2552 | core | plan D02 T13 §14 |  |
| NP-2233 | Save as PDF dialog and its categories | AI-1008 | -- | format | plan D02 T13 §15 |  |
| NP-2234 | PDF presets: built-in and custom, create, edit, delete | AI-1055 | CD-2528 | format | plan D02 T13 §15 |  |
| NP-2235 | PDF/X standards and prepress presets | AI-1056 | CD-2775, CD-2776, CD-2777 | print | plan D02 T13 §15 | PDF/X-1a, X-3, X-4 |
| NP-2236 | PDF compatibility levels | AI-1057 | CD-2551 | format | plan D02 T13 §15 | PDF 1.3 to 1.7 |
| NP-2237 | PDF general options | AI-1058 | -- | format | plan D02 T13 §15 | view after saving, thumbnails, layers from top-level layers, multipage |
| NP-2238 | PDF compression and downsampling | AI-1059 | CD-2536, CD-2537, CD-2538 | core | plan D02 T13 §15 | JPEG2000 and CCITT refused by name unless a codec is recorded |
| NP-2239 | PDF marks and bleeds | AI-1060 | CD-2783, CD-2784, CD-2785, CD-2786, CD-2787 | print | plan D02 T13 §15 | reuses the D02 T13 §4 marks |
| NP-2240 | PDF output color conversion and profile inclusion | AI-1061 | CD-1598, CD-1601 | core | plan D02 T13 §15 |  |
| NP-2241 | PDF advanced: overprints, always overprint black, flattener, subset threshold | AI-1062 | CD-2778, CD-2779 | print | plan D02 T13 §15 |  |
| NP-2242 | PDF summary and save summary | AI-1064 | -- | format | plan D02 T13 §15 |  |
| NP-2243 | PDF with the current proof settings | -- | CD-1599, CD-2521 | core | plan D02 T13 §15 |  |
| NP-2244 | PDF convert spot colors | -- | CD-1600 | print | plan D02 T13 §15 |  |
| NP-2245 | PDF/A archiving presets (CMYK and RGB) | -- | CD-2519, CD-2520 | core | plan D02 T13 §15 |  |
| NP-2246 | Document distribution, editing, and web presets | -- | CD-2522, CD-2523, CD-2524 | core | plan D02 T13 §15 |  |
| NP-2247 | Export several documents to one PDF | -- | CD-2527 | core | plan D02 T13 §15 |  |
| NP-2248 | PDF encoding: ASCII85 or binary | -- | CD-2544 | core | plan D02 T13 §15 |  |
| NP-2249 | EPS files in PDF: PostScript or preview | -- | CD-2545 | core | plan D02 T13 §15 |  |
| NP-2250 | Render complex fills as bitmaps in PDF | -- | CD-2554 | core | plan D02 T13 §15 |  |
| NP-2251 | PDF preflight tab | -- | CD-2780 | print | plan D02 T13 §15 | reuses the D02 T13 §9 engine |
| NP-2252 | PDF security: open and permissions passwords | AI-1063 | CD-2546, CD-2550 | core | plan D02 T13 §16 | AES through the PDFsharp security handler |
| NP-2253 | Tagged accessible PDF with alt text | AI-1065 | -- | format | plan D02 T13 §16 |  |
| NP-2254 | Symbols as reusable PDF objects | -- | CD-2530 | core | plan D02 T13 §16 | form XObjects |
| NP-2255 | PDF hyperlinks | -- | CD-2531 | core | plan D02 T13 §16 |  |
| NP-2256 | PDF bookmarks | -- | CD-2532 | core | plan D02 T13 §16 |  |
| NP-2257 | PDF page thumbnails | -- | CD-2533 | core | plan D02 T13 §16 |  |
| NP-2258 | PDF on-start view | -- | CD-2534 | core | plan D02 T13 §16 |  |
| NP-2259 | PDF include comments | -- | CD-2535 | core | plan D02 T13 §16 |  |
| NP-2260 | PDF printing, editing, and copying permissions | -- | CD-2547, CD-2548, CD-2549 | core | plan D02 T13 §16 |  |
| NP-2261 | Optimize PDF for web (linearize) | -- | CD-2553 | core | plan D02 T13 §16 |  |
| NP-2262 | Interactive 3D models in PDF | -- | CD-2529 | core | backlog B-040 |  |

## Import and export formats

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2263 | Open and import SVG and SVGZ with scaling and clip, symbol, image, and link preservation | AI-1002 | CD-2615 | format | plan D02 T14 §1 | SVGZ is gzip over the native reader |
| NP-2264 | Save as SVG or SVGZ with SVG options and show code | AI-1009 | -- | format | plan D02 T14 §1 | no SVG profiles or Adobe Graphics Server data; the nodus: namespace carries editing data |
| NP-2265 | CSS export and the CSS Properties panel for named objects | AI-1014, AI-1051 | -- | format | plan D02 T14 §1 |  |
| NP-2266 | Export SVG: styling mode, fonts, images, object IDs, precision, minify, responsive, encoding, presets | AI-1019 | CD-2616 | format | plan D02 T14 §1 | plain SVG with no nodus: namespace |
| NP-2267 | Copy SVG code to the clipboard and paste SVG text as art | AI-1045 | -- | format | plan D02 T14 §1 | extends the SVG clipboard of D02 T03 §3 |
| NP-2268 | SVG export fidelity: layers as named groups, symbols as symbol, unsupported effects rasterized, page or selection scope | -- | CD-2617 | format | plan D02 T14 §1 |  |
| NP-2269 | PDF place crop box: bounding, art, crop, trim, bleed, media | AI-0945 | -- | format | plan D02 T14 §2 |  |
| NP-2270 | Open or place PDF pages: single, range, or all, into pages or grouped objects, password prompt | AI-0946, AI-0992 | CD-2602 | format | plan D02 T14 §2 | PdfPig parsing, own graphics-state interpreter |
| NP-2271 | Keep spot inks of monotone, duotone, and tritone images from PDF | AI-0947 | -- | print | plan D02 T14 §2 | Separation and DeviceN images map to the D01 T04 §3 duotone model |
| NP-2272 | PDF import maintain paragraphs, text flow, and formatting | -- | CD-2458, CD-2604 | format | plan D02 T14 §2 |  |
| NP-2273 | PDF import text as text or as curves | -- | CD-2603 | format | plan D02 T14 §2 |  |
| NP-2274 | PDF import annotations onto a non-printing Comments layer by author | -- | CD-2605 | format | plan D02 T14 §2 |  |
| NP-2275 | PDF import crop content to the drawing page | -- | CD-2606 | format | plan D02 T14 §2 |  |
| NP-2276 | PDF import fidelity: transparency, soft masks, OCG layers, XObjects as symbols, annotation types | -- | CD-2607 | format | plan D02 T14 §2 | goldens from Inkscape with poppler |
| NP-2277 | Open and place PDF-compatible Illustrator .ai and .ait: artboards to pages, OCG layers, text as text or curves | AI-0991 | CD-2569 | format | plan D02 T14 §3 | through the §2 PDF path |
| NP-2278 | Append [Converted] to the name on opening legacy .ai files | AI-1126 | -- | core | plan D02 T14 §4 | legacy PostScript AI and AIPrivateData parsed from the published AI File Format spec v7 |
| NP-2279 | Save as .ai: version, range, PDF compatibility, embed ICC, compression, save each artboard, text as text or curves | AI-1005 | CD-2570 | format | plan D02 T14 §5 | PDF-based .ai written through the D02 T13 §14 PDF writer |
| NP-2280 | Save down to legacy AI versions with a data-loss report | AI-1006 | -- | format | plan D02 T14 §5 | EPS-based AI 8 writer |
| NP-2281 | Use Nodus artwork in other editors via .ai, PDF, and the clipboard | AI-1043 | -- | format | plan D02 T14 §5 | Photoshop smart-object paste is out of reach; Imago consumes the PDF and SVG flavors |
| NP-2282 | Legacy AI transparency handling: rasterize transparent areas or drop transparency | -- | CD-2571 | format | plan D02 T14 §5 |  |
| NP-2283 | AI export conversion options: outlines to objects, complex fills, spot to CMYK, preview image, placed images linked or embedded | -- | CD-2572 | format | plan D02 T14 §5 |  |
| NP-2284 | Conical and square gradients exported to AI as up to 256 bands | -- | CD-2573 | format | plan D02 T14 §5 |  |
| NP-2285 | Open and import CorelDRAW .cdr (RIFF v7 to X3 and X4+ ZIP) as a document or a group | AI-0997 | CD-2578 | format | plan D02 T14 §6 | own managed reader with libcdr (MPL-2.0) as reference |
| NP-2286 | Maintain layers and pages on CDR open and import | -- | CD-230, CD-2479 | core | plan D02 T14 §6 |  |
| NP-2287 | Select the code page for non-Unicode text in legacy CDR files | -- | CD-231, CD-2469 | core | plan D02 T14 §6 |  |
| NP-2288 | Import compressed CorelDRAW .cdx | -- | CD-2636 | format | plan D02 T14 §6 |  |
| NP-2289 | Open CorelDRAW templates .cdt as new untitled documents | -- | CD-2637 | format | plan D02 T14 §6 | save as .cdt is out of scope; Nodus templates are SVG |
| NP-2290 | Painterly brushstroke objects read from CDR, with the pre-25 bitmap fallback kept | -- | CD-2566 | format | plan D02 T14 §7 | read side here; the write fallback is §8 keep appearance |
| NP-2291 | Save reference info (title, subject, keywords, rating) into CDR | -- | CD-245 | core | plan D02 T14 §8 |  |
| NP-2292 | Save CDR to an earlier version | -- | CD-246 | format | plan D02 T14 §8 | Nodus writes the RIFF layout libcdr reads; CorelDRAW round trip is a recorded risk |
| NP-2293 | Save to an earlier version: keep appearance or keep editable | -- | CD-247 | format | plan D02 T14 §8 |  |
| NP-2294 | CMX import and export, and save CMX alongside CDR | -- | CD-248, CD-2579 | format | plan D02 T14 §8 |  |
| NP-2295 | Advanced save: compress bitmap effects and vector objects | -- | CD-249, CD-250 | core | plan D02 T14 §8 |  |
| NP-2296 | Advanced save: store or rebuild texture fills, blends, and extrusions | -- | CD-251, CD-252 | core | plan D02 T14 §8 |  |
| NP-2297 | Default CDR save version setting | -- | CD-2825 | core | plan D02 T14 §8 |  |
| NP-2298 | Ask when saving to an earlier version setting | -- | CD-2836 | core | plan D02 T14 §8 |  |
| NP-2299 | Open, import, or place EPS: Illustrator EPS as editable art, other EPS through Ghostscript, or placed with its preview | AI-0951, AI-0998 | CD-2589 | format | plan D02 T14 §9 | DCS is backlog B-038; AutoCAD is §10 |
| NP-2300 | EPS export general options: version, color output, preview TIFF or none, text as curves, fonts, PostScript level, flattening | AI-1007 | CD-2590 | format | plan D02 T14 §9 | own EPS writer |
| NP-2301 | EPS export advanced options: bounding box, JPEG compression, overprint and trapping flags, fountain steps | -- | CD-2591 | format | plan D02 T14 §9 | OPI links recorded as not written |
| NP-2302 | Ghostscript interpreter location and detection | -- | CD-2592 | format | plan D02 T14 §9 | AGPL-3.0, external process, never bundled |
| NP-2303 | Import PostScript PS and PRN, multi-page, text as text or curves | -- | CD-2593, CD-2653 | format | plan D02 T14 §9 | through a user-installed Ghostscript, refused by name when absent |
| NP-2304 | Open and import DWG and DXF: layout, scale, units, lineweights, layers, dimensions as live dimensions | AI-0949, AI-0993 | CD-2587 | format | plan D02 T14 §10 | ACadSharp (MIT) |
| NP-2305 | Export DWG and DXF: version, units, scale, text as curves or text, bitmap format, unmapped fills, blocks | AI-1012 | CD-2588 | format | plan D02 T14 §10 | ACadSharp (MIT) |
| NP-2306 | CGM import and export (v1, v3, v4, WebCGM, binary or text) | AI-0996 | CD-2577 | format | plan D02 T14 §11 | own reader and writer |
| NP-2307 | EMF and WMF import and export | AI-0999, AI-1015 | CD-2629, CD-2630 | format | plan D02 T14 §11 | own record parser and writer |
| NP-2308 | HPGL PLT import with scale, curve resolution, and pen mapping | -- | CD-2608 | format | plan D02 T14 §11 |  |
| NP-2309 | HPGL PLT export of outlines with pen settings and plotter origin | -- | CD-2609 | format | plan D02 T14 §11 |  |
| NP-2310 | WordPerfect Graphic WPG import and export | -- | CD-2626 | format | plan D02 T14 §11 | own codec |
| NP-2311 | Place and open raster images through WIC (GIF, JPEG, JP2, PNG, TIFF, TGA, PCX, WebP) | AI-0950, AI-1000 | -- | format | plan D02 T14 §12 | PICT and Pixar are backlog B-037 and B-038 |
| NP-2312 | Open and place AVIF | AI-0994 | -- | format | plan D02 T14 §12 | WIC AV1 extension, refused by name when absent |
| NP-2313 | BMP import and export: Windows BMP, DIB, RLE, OS/2 v1.3 and v2.0 | AI-0995, AI-1013 | CD-2575, CD-2576 | format | plan D02 T14 §12 |  |
| NP-2314 | TGA import and export with RLE | AI-1020 | CD-2619 | format | plan D02 T14 §12 | own codec |
| NP-2315 | TIFF import and export: compression, byte order, embed ICC | AI-1021 | CD-2620 | format | plan D02 T14 §12 |  |
| NP-2316 | Combine the layers of a multi-layer bitmap on import | -- | CD-2475 | core | plan D02 T14 §12 |  |
| NP-2317 | Check for watermark or copyright metadata on import | -- | CD-2477 | core | plan D02 T14 §12 | reads EXIF and XMP copyright, no Digimarc |
| NP-2318 | Import TIFF page selection | -- | CD-2480 | format | plan D02 T14 §12 |  |
| NP-2319 | Load partial file: import a frame range from a multi-frame image | -- | CD-2481 | format | plan D02 T14 §12 |  |
| NP-2320 | Resample and load | -- | CD-2482 | core | plan D02 T14 §12 |  |
| NP-2321 | Crop and load | -- | CD-2483 | core | plan D02 T14 §12 |  |
| NP-2322 | Export compression type where the format supports it | -- | CD-2495 | core | plan D02 T14 §12 |  |
| NP-2323 | Export notes into file metadata | -- | CD-2496 | core | plan D02 T14 §12 |  |
| NP-2324 | Hidden layers export unless the layer export flag is off | -- | CD-2497 | core | plan D02 T14 §12 |  |
| NP-2325 | Cursor CUR import | -- | CD-2582 | format | plan D02 T14 §12 | the ICO decoder covers CUR; backlog B-038 also lists CUR |
| NP-2326 | GIF import (including animated frames) and GIF export with transparency | -- | CD-2594, CD-2595 | format | plan D02 T14 §12 |  |
| NP-2327 | Import HEIF and HEIC key image | -- | CD-2596 | format | plan D02 T14 §12 | WIC HEIF extension, refused by name when absent |
| NP-2328 | JPEG import in gray, RGB, and CMYK with EXIF orientation | -- | CD-2597 | format | plan D02 T14 §12 |  |
| NP-2329 | JPEG 2000 import and export with quality and progression options | -- | CD-2598 | format | plan D02 T14 §12 | WIC has no JP2 codec; the codec decision is recorded in the section |
| NP-2330 | PCX import and export with RLE | -- | CD-2601 | format | plan D02 T14 §12 | own codec |
| NP-2331 | PNG import with masks and transparency | -- | CD-2610 | format | plan D02 T14 §12 |  |
| NP-2332 | Open and place PSD: layers to objects or flatten, layer comps, hidden layers, blend modes, spot channels | AI-0943, AI-1001 | CD-2612 | format | plan D02 T14 §13 | own reader against the published PSD spec |
| NP-2333 | Place linked PSD with a chosen layer comp | AI-0944 | -- | format | plan D02 T14 §13 |  |
| NP-2334 | Exchange paths and pixels with raster editors through the clipboard | AI-0952 | -- | format | plan D02 T14 §13 | Imago is the first partner |
| NP-2335 | Export PSD: color model, resolution, flat or layered, anti-alias, embed ICC, spot channels | AI-1018 | CD-2613 | format | plan D02 T14 §13 | text rasterized; own writer |
| NP-2336 | Import office and text documents: TXT, RTF, DOC, DOCX | AI-1003 | CD-2555 | format | plan D02 T14 §14 | DocumentFormat.OpenXml and NPOI; WPD is backlog B-037 |
| NP-2337 | Export text as TXT | AI-1022 | -- | format | plan D02 T14 §14 |  |
| NP-2338 | Export For Office dialog with preview, zoom, pan, and estimated size | -- | CD-2498, CD-2563 | core | plan D02 T14 §14 |  |
| NP-2339 | Export For Office: compatibility target as PNG | -- | CD-2499 | core | plan D02 T14 §14 |  |
| NP-2340 | Export For Office: editing target as EMF | -- | CD-2500 | core | plan D02 T14 §14 |  |
| NP-2341 | Export For Office: WordPerfect target as WPG | -- | CD-2501 | core | plan D02 T14 §14 |  |
| NP-2342 | Export For Office optimization: presentation, desktop, or commercial print resolution | -- | CD-2502 | core | plan D02 T14 §14 |  |
| NP-2343 | Layers flattened on Office export | -- | CD-2503 | core | plan D02 T14 §14 |  |
| NP-2344 | Copy artwork for pasting into office documents (EMF, PNG, SVG flavors) | -- | CD-2556 | core | plan D02 T14 §14 |  |
| NP-2345 | Insert Nodus artwork into office documents | -- | CD-2557 | core | plan D02 T14 §14 | by EMF or PNG file or clipboard; no OLE server, recorded |
| NP-2346 | Export a curve as a Type 1 PFB glyph | -- | CD-2574 | format | plan D02 T14 §14 |  |
| NP-2347 | Export text objects as DOC or RTF | -- | CD-2584 | format | plan D02 T14 §14 |  |
| NP-2348 | Export a curve as a TrueType TTF glyph | -- | CD-2621 | format | plan D02 T14 §14 |  |
| NP-2349 | Import XLS, XLSX, and CSV data as tables | -- | CD-2649 | format | plan D02 T14 §14 | NPOI for XLS |
| NP-2350 | Missing-reader warning for office documents, re-enabled from settings | -- | CD-2891 | format | plan D02 T14 §14 | no compatibility pack needed; the warning covers a refused format |
| NP-2351 | Place or import multiple files one by one or in a grid | AI-0932 | CD-2472 | core | plan D02 T14 §19 |  |
| NP-2352 | Clipboard formats: PDF, AICB, SVG, EMF, bitmap, with preserve paths or appearance | AI-1044, AI-1181 | CD-2657 | core | plan D02 T14 §19 | AICB write is §5, read is §4 |
| NP-2353 | Clipboard settings: include SVG code, paste text without formatting | AI-1182 | -- | core | plan D02 T14 §19 |  |
| NP-2354 | Enable, disable, and order import and export formats | -- | CD-207 | core | plan D02 T14 §19 |  |
| NP-2355 | Acquire image from a WIA scanner or camera, and select source | -- | CD-307, CD-308, CD-2456 | core | plan D02 T14 §19 | WIA only; TWAIN recorded as not supported |
| NP-2356 | Paste link to a source file that stays connected | -- | CD-1694 | core | plan D02 T14 §19 | as a linked placed file, not an OLE link; recorded |
| NP-2357 | Insert object from file, linked or embedded | -- | CD-1695, CD-1740 | core | plan D02 T14 §19 | as a placed file with Edit Original; no OLE container, recorded |
| NP-2358 | Drag and drop content from other applications | -- | CD-1696 | core | plan D02 T14 §19 |  |
| NP-2359 | Edit a linked or embedded object in its source application and update | -- | CD-1697 | core | plan D02 T14 §19 | through Edit Original and file watching |
| NP-2360 | Import at the original position | -- | CD-2464, CD-2470 | core | plan D02 T14 §19 |  |
| NP-2361 | Import command: click to place, drag to size, Enter to center, with import options | -- | CD-2466, CD-2560 | core | plan D02 T14 §19 |  |
| NP-2362 | Import dialog search by name and metadata | -- | CD-2467 | core | plan D02 T14 §19 |  |
| NP-2363 | Import format filter list | -- | CD-2468 | core | plan D02 T14 §19 |  |
| NP-2364 | Snapping applies while placing an import | -- | CD-2471 | core | plan D02 T14 §19 |  |
| NP-2365 | Skip the format options dialog on import | -- | CD-2478 | core | plan D02 T14 §19 |  |
| NP-2366 | All readers built in; optional external components named where a format needs one | -- | CD-2568 | format | plan D02 T14 §19 | Ghostscript and WIC extensions are the only optional pieces |
| NP-2367 | Open document | -- | CD-228 | core | shipped-scope D02 T04 §2 | native format open already covered |
| NP-2368 | JPEG export | AI-1016 | -- | format | shipped-scope D02 T04 §3 |  |
| NP-2369 | PNG export | AI-1017 | CD-2611 | format | shipped-scope D02 T04 §3 |  |
| NP-2370 | Place (import) linked or embedded | AI-0931 | -- | core | shipped-scope D02 T06 §14 |  |
| NP-2371 | WebP import and export | AI-1023 | CD-2623, CD-2624 | format | shipped-scope D02 T06 §14 |  |
| NP-2372 | FreeHand file import | AI-1004 | CD-2646 | format | backlog B-037 | legacy format |
| NP-2373 | FXG save | AI-1010 | -- | format | backlog B-037 | removed from current Illustrator |
| NP-2374 | Macintosh PICT import and export | AI-1024 | CD-2600 | format | backlog B-037 | legacy format |
| NP-2375 | SWF (Flash) export | AI-1025 | CD-2618 | format | backlog B-037 | deprecated format |
| NP-2376 | Microsoft Publisher (PUB) import | -- | CD-2585 | format | backlog B-037 |  |
| NP-2377 | Corel DESIGNER and Micrografx Designer import | -- | CD-2586 | format | backlog B-037 |  |
| NP-2378 | Visio (VSD) import | -- | CD-2622 | format | backlog B-037 |  |
| NP-2379 | WordPerfect document text import and export | -- | CD-2625 | format | backlog B-037 |  |
| NP-2380 | Corel ArtShow (CPX) import | -- | CD-2633 | format | backlog B-037 |  |
| NP-2381 | Corel Presentations (SHW) import | -- | CD-2634 | format | backlog B-037 |  |
| NP-2382 | Corel R.A.V.E. (CLK) import | -- | CD-2635 | format | backlog B-037 |  |
| NP-2383 | Frame Vector Metafile (FMV) import and export | -- | CD-2641 | format | backlog B-037 |  |
| NP-2384 | GEM Paint and GEM File import and export | -- | CD-2642 | format | backlog B-037 |  |
| NP-2385 | Lotus PIC import | -- | CD-2644 | format | backlog B-037 |  |
| NP-2386 | OS/2 MET metafile import and export | -- | CD-2647 | format | backlog B-037 |  |
| NP-2387 | Picture Publisher 4 (PP4) import | -- | CD-2648 | format | backlog B-037 |  |
| NP-2388 | PowerPoint (PPT) import | -- | CD-2650 | format | backlog B-037 |  |
| NP-2389 | NAPLPS (NAP) metafile import | -- | CD-2651 | format | backlog B-037 |  |
| NP-2390 | Legacy spreadsheet and word processor import (WB, WK, WSD) | -- | CD-2655 | format | backlog B-037 |  |
| NP-2391 | DCS (Desktop Color Separation) import and export | AI-0948 | CD-2638 | print | backlog B-038 |  |
| NP-2392 | Corel PHOTO-PAINT (CPT) import and export | -- | CD-2580 | format | backlog B-038 |  |
| NP-2393 | Kodak Photo CD (PCD) import | -- | CD-2599 | format | backlog B-038 |  |
| NP-2394 | Corel Painter (RIF) import | -- | CD-2614 | format | backlog B-038 |  |
| NP-2395 | Wavelet Compressed Bitmap (WI) import and export | -- | CD-2628 | format | backlog B-038 |  |
| NP-2396 | CALS Compressed Bitmap (CAL) import and export | -- | CD-2632 | format | backlog B-038 |  |
| NP-2397 | Windows icon (ICO, EXE resource) import and export | -- | CD-2639 | format | backlog B-038 |  |
| NP-2398 | FlashPix (FPX) import | -- | CD-2640 | format | backlog B-038 |  |
| NP-2399 | GIMP (XCF) import with layers | -- | CD-2643 | format | backlog B-038 |  |
| NP-2400 | MacPaint (MAC) import and export | -- | CD-2645 | format | backlog B-038 |  |
| NP-2401 | Scitex CT (SCT) import | -- | CD-2654 | format | backlog B-038 |  |
| NP-2402 | X PixMap (XPM) import and export | -- | CD-2656 | format | backlog B-038 |  |
| NP-2403 | RAW develop dialog with previews, snapshots, and apply to all | -- | CD-2059, CD-2060, CD-2061, CD-2068, CD-2071 | core | backlog B-039 |  |
| NP-2404 | RAW white balance, tone, and histogram | -- | CD-2062, CD-2063, CD-2064, CD-2065, CD-2066, CD-2067 | core | backlog B-039 |  |
| NP-2405 | RAW sharpening and noise reduction | -- | CD-2069, CD-2070 | core | backlog B-039 |  |
| NP-2406 | Camera RAW file import | -- | CD-2567, CD-2627 | format | backlog B-039 |  |

## Export for screens and web

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2407 | Collect layers or objects for export from the Layers panel | AI-0840 | -- | format | plan D02 T14 §15 |  |
| NP-2408 | Export selected artboards from the canvas context menu | AI-0861 | -- | format | plan D02 T14 §15 |  |
| NP-2409 | Export As with format-specific options, artboards or pages, and range | AI-1011 | CD-2489, CD-2561 | core | plan D02 T14 §15 |  |
| NP-2410 | Export Selection: add selected objects to the export list as assets | AI-1026 | CD-2505 | format | plan D02 T14 §15 |  |
| NP-2411 | Export for Screens dialog | AI-1027 | -- | format | plan D02 T14 §15 |  |
| NP-2412 | Export for Screens artboards tab: all, range, full document, include bleed | AI-1028 | -- | format | plan D02 T14 §15 |  |
| NP-2413 | Export for Screens assets tab | AI-1029 | -- | format | plan D02 T14 §15 |  |
| NP-2414 | Export for Screens formats: PNG, PNG-8, JPG qualities, SVG, PDF, WebP, TIFF | AI-1030 | -- | format | plan D02 T14 §15 |  |
| NP-2415 | Export scales and suffixes with iOS and Android presets | AI-1031 | -- | format | plan D02 T14 §15 |  |
| NP-2416 | Export sub-folders, open location after export, and per-format settings | AI-1032 | -- | format | plan D02 T14 §15 |  |
| NP-2417 | Export in background with progress | AI-1034 | -- | format | plan D02 T14 §15 |  |
| NP-2418 | The export list panel (asset export and export docker) | AI-1035 | CD-2504, CD-2565 | core | plan D02 T14 §15 |  |
| NP-2419 | Add the current page to the export list | -- | CD-2361, CD-2506 | core | plan D02 T14 §15 |  |
| NP-2420 | Crop to page on export | -- | CD-2457, CD-2494 | core | plan D02 T14 §15 |  |
| NP-2421 | Duplicate a page into a new document | -- | CD-2459 | core | plan D02 T14 §15 |  |
| NP-2422 | Export a page range with each page to its own file | -- | CD-2460, CD-2491 | core | plan D02 T14 §15 |  |
| NP-2423 | Rename export items, filename suffix, and select all | -- | CD-2461, CD-2511 | core | plan D02 T14 §15 |  |
| NP-2424 | Export selected objects only | -- | CD-2465, CD-2492 | format | plan D02 T14 §15 |  |
| NP-2425 | Export this page only | -- | CD-2490 | core | plan D02 T14 §15 |  |
| NP-2426 | Skip the format options dialog on export | -- | CD-2493 | core | plan D02 T14 §15 |  |
| NP-2427 | Add all pages to the export list with separate pages and a page range | -- | CD-2507 | core | plan D02 T14 §15 |  |
| NP-2428 | Remove export items | -- | CD-2508 | core | plan D02 T14 §15 |  |
| NP-2429 | Duplicate an export item for alternate settings | -- | CD-2509 | core | plan D02 T14 §15 |  |
| NP-2430 | Add new assets reusing an item's export settings | -- | CD-2510 | core | plan D02 T14 §15 |  |
| NP-2431 | Per-item format and destination folder | -- | CD-2512 | core | plan D02 T14 §15 |  |
| NP-2432 | Per-item format settings | -- | CD-2513 | core | plan D02 T14 §15 |  |
| NP-2433 | Export checked items or all items | -- | CD-2514 | core | plan D02 T14 §15 |  |
| NP-2434 | Default format for new export items | -- | CD-2515 | core | plan D02 T14 §15 |  |
| NP-2435 | Export list ordering and settings bound to objects | -- | CD-2516 | core | plan D02 T14 §15 |  |
| NP-2436 | Outline-aware bitmap export bounds | -- | CD-2517 | core | plan D02 T14 §15 |  |
| NP-2437 | Recommended import and export formats guide | -- | CD-2558, CD-2559 | format | plan D02 T14 §15 | a user guide page |
| NP-2438 | Export for Web dialog for GIF, PNG, JPEG, WebP | AI-1036 | CD-2562, CD-2795 | core | plan D02 T14 §16 |  |
| NP-2439 | Export for Web comparison previews (1, 2, or 4 up), zoom, pan, color table, preview in browser | AI-1037 | CD-2796 | format | plan D02 T14 §16 |  |
| NP-2440 | GIF and PNG-8 options: palette, colors, dither, web snap, lossy, palette editing | AI-1038 | CD-2805 | format | plan D02 T14 §16 | quantization from D01 T03 §3 |
| NP-2441 | Web JPEG options: quality, progressive, optimized, blur, embed ICC | AI-1039 | CD-2802 | format | plan D02 T14 §16 |  |
| NP-2442 | Export for Web presets: apply, save, load, delete | -- | CD-2797 | core | plan D02 T14 §16 |  |
| NP-2443 | Connection speed download estimate | -- | CD-2798 | core | plan D02 T14 §16 |  |
| NP-2444 | Web export color mode and embedded profile | -- | CD-2799 | core | plan D02 T14 §16 |  |
| NP-2445 | Export for Web crop to page | -- | CD-2800 | core | plan D02 T14 §16 |  |
| NP-2446 | Export for Web resize: units, width, height, percent, resolution | -- | CD-2801 | core | plan D02 T14 §16 |  |
| NP-2447 | Matte color for anti-aliased edges | -- | CD-2803 | core | plan D02 T14 §16 |  |
| NP-2448 | Anti-aliased and interlaced web output | -- | CD-2804 | core | plan D02 T14 §16 |  |
| NP-2449 | Transparent background or sampled color in paletted output | -- | CD-2806 | core | plan D02 T14 §16 |  |
| NP-2450 | Make text web-compatible for HTML export | -- | CD-2807 | core | plan D02 T14 §16 |  |
| NP-2451 | Slice tool | AI-0127 | -- | format | plan D02 T14 §17 |  |
| NP-2452 | Slice Selection tool | AI-0128 | -- | format | plan D02 T14 §17 |  |
| NP-2453 | Show, hide, and lock slices | AI-0920 | -- | format | plan D02 T14 §17 |  |
| NP-2454 | Save selected slices as images | AI-1040 | -- | format | plan D02 T14 §17 |  |
| NP-2455 | Make, release, and create slices from guides or selection | AI-1046 | -- | format | plan D02 T14 §17 |  |
| NP-2456 | Duplicate, combine, divide, and delete all slices | AI-1047 | -- | format | plan D02 T14 §17 |  |
| NP-2457 | Slice options: type, name, URL, target, message, alt text, background | AI-1048 | -- | format | plan D02 T14 §17 |  |
| NP-2458 | Clip slices to the artboard | AI-1049 | -- | format | plan D02 T14 §17 |  |
| NP-2459 | Image maps: hotspot by shape or bounds with URL | AI-1050 | CD-2816 | format | plan D02 T14 §17 |  |
| NP-2460 | SVG Interactivity panel with event handlers | AI-1052, AI-1053 | -- | format | plan D02 T14 §17 |  |
| NP-2461 | Link JavaScript files for SVG output | AI-1054 | -- | format | plan D02 T14 §17 | links only; Nodus never runs the scripts |
| NP-2462 | Slice numbers and line color preferences | AI-1161 | -- | format | plan D02 T14 §17 |  |
| NP-2463 | Create rollover with Normal, Over, and Down states | -- | CD-2808 | core | plan D02 T14 §17 |  |
| NP-2464 | Edit rollover states and finish editing | -- | CD-2809, CD-2819, CD-2820 | core | plan D02 T14 §17 |  |
| NP-2465 | Rollover state delete, duplicate, extract, and target frame | -- | CD-2810 | core | plan D02 T14 §17 |  |
| NP-2466 | Rollover live preview | -- | CD-2811 | core | plan D02 T14 §17 |  |
| NP-2467 | Links and Rollovers panel | -- | CD-2812, CD-2821 | core | plan D02 T14 §17 |  |
| NP-2468 | Bookmarks for internal links | -- | CD-2813 | core | plan D02 T14 §17 |  |
| NP-2469 | Hyperlinks on objects and text | -- | CD-2814 | core | plan D02 T14 §17 |  |
| NP-2470 | Verify and delete links and bookmarks | -- | CD-2815 | core | plan D02 T14 §17 |  |
| NP-2471 | Hotspot crosshatch and background indicator colors | -- | CD-2817 | core | plan D02 T14 §17 |  |
| NP-2472 | Alternate text on linked objects | -- | CD-2818 | core | plan D02 T14 §17 |  |
| NP-2473 | Align to pixel grid: per object, default for new art, and the align command | AI-0134 | CD-669, CD-2792 | core | plan D02 T14 §18 |  |
| NP-2474 | Pixel preview view mode at document resolution | AI-0910 | CD-041, CD-119 | core | plan D02 T14 §18 |  |
| NP-2475 | Display bitmaps anti-aliased in pixel preview setting | AI-1177 | -- | core | plan D02 T14 §18 |  |
| NP-2476 | Object hinting for crisp bitmap export | -- | CD-2793 | core | plan D02 T14 §18 |  |
| NP-2477 | Pixel-perfect workflow: pixel units, whole-number sizes, pixel snapping, pixel-aligned page | -- | CD-2794 | core | plan D02 T14 §18 |  |

## AI

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2478 | Generation timeout, retries, and cancellation | -- | CD-3023 | ai | plan D01 T05 §1 | 60 s default request timeout as a setting, every request cancellable |
| NP-2479 | AI availability and data-use help page | AI-1289 | -- | ai | plan D01 T05 §4 | local help: BYOK, what each action sends, provenance instead of vendor content credentials |
| NP-2480 | Content-aware defaults preference | AI-1131 | -- | ai | plan D02 T15 §1 |  |
| NP-2481 | AI menu and generative toolbar button | AI-1254 | -- | ai | plan D02 T15 §1 |  |
| NP-2482 | AI usage and credit meter for the user's key | AI-1255 | CD-3022 | ai | plan D02 T15 §1 | OpenRouter usage and balance for the user's own key; no vendor credit plan |
| NP-2483 | Generation history and provenance panel | AI-1268 | -- | ai | plan D02 T15 §1 | re-run with same seed, compare, revert from the provenance embedded in the document |
| NP-2484 | Per-task AI model selection | -- | CD-3012 | ai | plan D02 T15 §1 | OpenRouter model per task (text, vision, image, vector JSON) |
| NP-2485 | AI quick tutorial on first use | -- | CD-3024 | ai | plan D02 T15 §1 |  |
| NP-2486 | Text to vector from a prompt | AI-1256 | CD-3016, CD-3017 | ai | plan D02 T15 §2 | model returns schema-validated JSON applied as named layers, paths, swatches, one undo step |
| NP-2487 | Text to vector content types: subject, scene, icon, pattern | AI-1257 | -- | ai | plan D02 T15 §2 |  |
| NP-2488 | Text to vector detail level | AI-1258 | -- | ai | plan D02 T15 §2 |  |
| NP-2489 | Style reference from an image or selected art | AI-1259 | -- | ai | plan D02 T15 §2 |  |
| NP-2490 | Style, effect, and color-tone presets for vector generation | AI-1260 | -- | ai | plan D02 T15 §2 |  |
| NP-2491 | Model picker for vector generation | AI-1261, AI-1262 | -- | ai | plan D02 T15 §2 | OpenRouter models chosen by the user; no vendor-exclusive models |
| NP-2492 | Auto model recommendation and up to 4 variations | AI-1263 | -- | ai | plan D02 T15 §2 |  |
| NP-2493 | Editable live text in generated vectors | AI-1264 | -- | ai | plan D02 T15 §2 |  |
| NP-2494 | Generate similar variations | AI-1265 | -- | ai | plan D02 T15 §2 |  |
| NP-2495 | Browse, rate, and reuse generated variations | AI-1266 | -- | ai | plan D02 T15 §2 |  |
| NP-2496 | Turntable: alternate views of 2D art | AI-1280, AI-1281 | -- | ai | plan D02 T15 §2 | guidance text on when to use 3D instead folded in |
| NP-2497 | New document from a prompt | AI-1286 | -- | ai | plan D02 T15 §2 |  |
| NP-2498 | Welcome screen AI entries | AI-1287 | CD-3019 | ai | plan D02 T15 §2 | board ideation is cloud-only and not built |
| NP-2499 | Text to pattern swatch | AI-1269 | -- | ai | plan D02 T15 §3 |  |
| NP-2500 | Manage and edit generated patterns | AI-1270 | -- | ai | plan D02 T15 §3 |  |
| NP-2501 | Generative shape fill with detail and style reference | AI-1271, AI-1272 | -- | ai | plan D02 T15 §3 |  |
| NP-2502 | Repeat a shape fill across repeated shapes | AI-1273 | -- | ai | plan D02 T15 §3 |  |
| NP-2503 | Generative expand for vector artwork | AI-1275, AI-1276 | -- | ai | plan D02 T15 §4 |  |
| NP-2504 | Generate print bleed | AI-1277 | -- | ai | plan D02 T15 §4 |  |
| NP-2505 | Generative expand for placed images | AI-1278 | -- | ai | plan D02 T15 §4 | result is a new placed image with provenance, original kept |
| NP-2506 | Generative recolor from a prompt | AI-1274 | -- | ai | plan D02 T15 §5 | palette proposals applied through Recolor Artwork mapping |
| NP-2507 | Palette-constrained generation from presets and brand kits | -- | CD-3015 | ai | plan D02 T15 §5 |  |
| NP-2508 | Prompt to edit selected artwork | AI-1284 | -- | ai | plan D02 T15 §6 | each change a named undoable command with provenance |
| NP-2509 | AI assistant panel with chats, attachments, and follow-ups | AI-1290, AI-1293 | -- | ai | plan D02 T15 §6 |  |
| NP-2510 | Assistant workflow starters | AI-1291 | -- | ai | plan D02 T15 §6 |  |
| NP-2511 | Assistant skills as slash commands | AI-1292 | -- | ai | plan D02 T15 §6 | named sequences of Nodus commands, not scripting |
| NP-2512 | Assistant generate, recolor, and vectorize | AI-1294 | -- | ai | plan D02 T15 §6 |  |
| NP-2513 | Retype: identify fonts in images and outlined text | AI-0413, AI-1288 | -- | ai | plan D02 T15 §7 | matches against installed fonts only |
| NP-2514 | Retype: convert image text to live text | AI-0414 | -- | ai | plan D02 T15 §7 |  |
| NP-2515 | Rewrite: generate, rephrase, translate, proofread, fit text | AI-1285 | -- | ai | plan D02 T15 §7 |  |
| NP-2516 | Grammar check | -- | CD-1213, CD-1229 | core | plan D02 T15 §7 | model-based checker, not the Grammatik engine |
| NP-2517 | Grammar check options and checking styles | -- | CD-1219, CD-1221 | core | plan D02 T15 §7 |  |
| NP-2518 | Quick generate dialog | -- | CD-3005, CD-3018 | ai | plan D02 T15 §8 |  |
| NP-2519 | AI Generate panel | -- | CD-3007, CD-3008 | ai | plan D02 T15 §8 |  |
| NP-2520 | Text to image as a placed image | -- | CD-3009 | ai | plan D02 T15 §8 |  |
| NP-2521 | Reference image generation | -- | CD-3010 | ai | plan D02 T15 §8 |  |
| NP-2522 | Remix image | -- | CD-3011 | ai | plan D02 T15 §8 |  |
| NP-2523 | Aspect ratio and image format | -- | CD-3013 | ai | plan D02 T15 §8 |  |
| NP-2524 | Image style presets | -- | CD-3014 | ai | plan D02 T15 §8 |  |
| NP-2525 | Remove background | AI-1279 | CD-3006, CD-3020 | ai | plan D02 T15 §9 | cut-out as a new image plus mask, original kept |
| NP-2526 | AI upsampling: illustration and photo modes | -- | CD-1974, CD-1975, CD-3025 | ai | plan D02 T15 §9 |  |
| NP-2527 | Upsample noise reduction | -- | CD-1976 | ai | plan D02 T15 §9 |  |
| NP-2528 | Remove JPEG artifacts | -- | CD-1987, CD-3026 | ai | plan D02 T15 §9 |  |
| NP-2529 | Art style transfer | -- | CD-2170, CD-2253, CD-3027 | ai | plan D02 T15 §9 | CD-2253 was core; merged as ai |
| NP-2530 | Art style presets | -- | CD-2171 | ai | plan D02 T15 §9 | Nodus's own named presets, not Corel's |
| NP-2531 | Concept to vector from sketches and photos | AI-1282 | -- | ai | plan D02 T15 §10 |  |
| NP-2532 | Concept to vector variations, reference match, and raster output | AI-1283 | -- | ai | plan D02 T15 §10 |  |
| NP-2533 | Trace with AI background removal first | -- | CD-3021 | ai | plan D02 T15 §10 | the local tracer stays in D02 T12 §5 |
| NP-2534 | AI-assisted trace preparation | -- | CD-3028 | ai | plan D02 T15 §10 | model proposes palette and cleanup; the potrace port does the tracing |
| NP-2535 | Linked variations across documents | AI-1267 | -- | ai | plan D02 T15 §11 |  |
| NP-2536 | Suite launcher and hand-offs to Imago and Lumen | -- | CD-172 | core | plan D02 T15 §11 | offered only when the app is installed, refused by name otherwise |

## Workspace and UI

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2537 | Math in numeric fields | AI-1110 | -- | core | plan D02 T07 §8 |  |
| NP-2538 | Scroll-proof numeric fields | AI-1111 | -- | core | plan D02 T07 §8 |  |
| NP-2539 | Numeric field keys: Shift+Enter keeps focus, arrows step | AI-1112 | -- | core | plan D02 T07 §8 |  |
| NP-2540 | The Properties panel | AI-1196 | CD-072, CD-158, CD-576 | core | plan D02 T07 §8 |  |
| NP-2541 | Properties panel quick actions | AI-1197 | -- | core | plan D02 T07 §8 |  |
| NP-2542 | Document properties with nothing selected | AI-1198 | -- | core | plan D02 T07 §8 |  |
| NP-2543 | The contextual property bar | AI-1199 | CD-060, CD-173 | core | plan D02 T07 §8 |  |
| NP-2544 | Contextual task bar | AI-1200 | -- | core | plan D02 T07 §8 |  |
| NP-2545 | Properties panel scroll and tab modes | -- | CD-073 | core | plan D02 T07 §8 |  |
| NP-2546 | Properties panel style indicators | -- | CD-074 | core | plan D02 T07 §8 |  |
| NP-2547 | Position boxes | -- | CD-375 | core | plan D02 T07 §8 |  |
| NP-2548 | Object size boxes | -- | CD-382, CD-823 | core | plan D02 T07 §8 |  |
| NP-2549 | Scale factor boxes | -- | CD-383 | core | plan D02 T07 §8 |  |
| NP-2550 | Curve properties in the Properties panel | -- | CD-650 | core | plan D02 T07 §8 |  |
| NP-2551 | Workspace switcher | AI-1185 | CD-064 | core | plan D02 T16 §1 |  |
| NP-2552 | New, duplicate, rename, and delete workspaces | AI-1186 | CD-084, CD-085, CD-145, CD-209, CD-2907 | core | plan D02 T16 §1 |  |
| NP-2553 | Panel docking, grouping, floating, and collapse to icons | AI-1187 | CD-061 | core | plan D02 T16 §1 |  |
| NP-2554 | Hide and show all panels (Tab) | AI-1188 | CD-163 | core | plan D02 T16 §1 |  |
| NP-2555 | Application bar | AI-1189 | -- | cloud | plan D02 T16 §1 | local items only: workspace switcher, search, AI usage, assistant |
| NP-2556 | Application window layout | -- | CD-047 | core | plan D02 T16 §1 |  |
| NP-2557 | Panel quick customize | -- | CD-062 | core | plan D02 T16 §1 |  |
| NP-2558 | Lite workspace | -- | CD-065, CD-138 | core | plan D02 T16 §1 |  |
| NP-2559 | Touch workspace preset | -- | CD-066, CD-139 | core | plan D02 T16 §1 | touch behavior itself is §8 |
| NP-2560 | Illustration workspace | -- | CD-067, CD-141 | core | plan D02 T16 §1 |  |
| NP-2561 | Page layout workspace | -- | CD-068, CD-140 | core | plan D02 T16 §1 |  |
| NP-2562 | Illustrator-style workspace | -- | CD-069, CD-142 | core | plan D02 T16 §1 | panel placement and shortcut set familiar to Illustrator users |
| NP-2563 | Reset to factory defaults at startup (F8) | -- | CD-083, CD-211, CD-2842 | core | plan D02 T16 §1 |  |
| NP-2564 | Import and export workspace files | -- | CD-086, CD-087, CD-143, CD-144, CD-210 | core | plan D02 T16 §1 | own .nodusws JSON, not .cdws |
| NP-2565 | Default workspace | -- | CD-137 | core | plan D02 T16 §1 |  |
| NP-2566 | Lock panels | -- | CD-164 | core | plan D02 T16 §1 |  |
| NP-2567 | Status bar: selection details, cursor position, color profile | AI-0927 | CD-063, CD-108, CD-175 | core | plan D02 T16 §2 |  |
| NP-2568 | Basic and advanced tool sets | AI-1190 | -- | core | plan D02 T16 §2 |  |
| NP-2569 | Edit toolbar drawer (all tools) | AI-1191 | -- | core | plan D02 T16 §2 |  |
| NP-2570 | Custom toolbars: new, rename, delete | AI-1192 | CD-102 | core | plan D02 T16 §2 |  |
| NP-2571 | Toolbox single or double column and tear-off flyouts | AI-1193 | -- | core | plan D02 T16 §2 |  |
| NP-2572 | Show or hide toolbox fill, draw mode, and screen mode controls | AI-1194 | -- | core | plan D02 T16 §2 |  |
| NP-2573 | Alt-click cycles hidden tools | AI-1195 | -- | core | plan D02 T16 §2 |  |
| NP-2574 | Standard toolbar | -- | CD-048, CD-147, CD-171 | core | plan D02 T16 §2 |  |
| NP-2575 | Zoom toolbar | -- | CD-050, CD-149 | core | plan D02 T16 §2 |  |
| NP-2576 | Text toolbar | -- | CD-051, CD-148 | core | plan D02 T16 §2 |  |
| NP-2577 | Layout toolbar | -- | CD-052, CD-150 | core | plan D02 T16 §2 |  |
| NP-2578 | Transform toolbar | -- | CD-053, CD-151 | core | plan D02 T16 §2 |  |
| NP-2579 | Web toolbar | -- | CD-055, CD-153 | core | plan D02 T16 §2 | export-for-screens commands; rollovers not built |
| NP-2580 | Lock toolbars | -- | CD-057 | core | plan D02 T16 §2 |  |
| NP-2581 | Toolbox with flyouts | -- | CD-058, CD-146 | core | plan D02 T16 §2 |  |
| NP-2582 | Toolbox quick customize | -- | CD-059, CD-174, CD-204 | core | plan D02 T16 §2 |  |
| NP-2583 | Move, dock, float, and resize toolbars | -- | CD-100 | core | plan D02 T16 §2 |  |
| NP-2584 | Show or hide toolbars | -- | CD-101 | core | plan D02 T16 §2 |  |
| NP-2585 | Add, remove, move, and copy toolbar items | -- | CD-103 | core | plan D02 T16 §2 |  |
| NP-2586 | Toolbar button size and style | -- | CD-104 | core | plan D02 T16 §2 |  |
| NP-2587 | Replace a toolbar button image | -- | CD-105 | core | plan D02 T16 §2 |  |
| NP-2588 | Property bar positioning | -- | CD-106 | core | plan D02 T16 §2 |  |
| NP-2589 | Property bar quick customize | -- | CD-107, CD-205 | core | plan D02 T16 §2 |  |
| NP-2590 | Status bar lines, items, and size | -- | CD-109, CD-110 | core | plan D02 T16 §2 |  |
| NP-2591 | Status bar position and reset | -- | CD-111, CD-206 | core | plan D02 T16 §2 |  |
| NP-2592 | Document management toolbar | -- | CD-156 | core | plan D02 T16 §2 |  |
| NP-2593 | Command bar customization page | -- | CD-157, CD-203 | core | plan D02 T16 §2 |  |
| NP-2594 | Export shortcuts to text or CSV | AI-1106 | CD-093 | core | plan D02 T16 §3 |  |
| NP-2595 | Delete a shortcut and conflict warnings | AI-1107 | CD-090 | core | plan D02 T16 §3 |  |
| NP-2596 | Shortcut set files | AI-1108 | -- | core | plan D02 T16 §3 | own JSON set files, not .kys |
| NP-2597 | Context menus | AI-1209 | CD-192 | core | plan D02 T16 §3 |  |
| NP-2598 | Shortcut tables per editing context | -- | CD-089 | core | plan D02 T16 §3 |  |
| NP-2599 | View all shortcuts and reset all | -- | CD-091 | core | plan D02 T16 §3 |  |
| NP-2600 | Print shortcuts | -- | CD-092 | core | plan D02 T16 §3 | extends the print path of D02 T05 §2 |
| NP-2601 | Reorder menus and commands | -- | CD-094 | core | plan D02 T16 §3 |  |
| NP-2602 | Rename a menu or command caption | -- | CD-095 | core | plan D02 T16 §3 |  |
| NP-2603 | Add or remove menu items | -- | CD-096 | core | plan D02 T16 §3 |  |
| NP-2604 | Command search in customization | -- | CD-097 | core | plan D02 T16 §3 | reuses the D02 T06 §12 command index |
| NP-2605 | Menu bar mode | -- | CD-098 | core | plan D02 T16 §3 |  |
| NP-2606 | Reset menus | -- | CD-099 | core | plan D02 T16 §3 |  |
| NP-2607 | Customization dialog: commands, shortcuts, and menus | -- | CD-201, CD-202, CD-2911 | core | plan D02 T16 §3 |  |
| NP-2608 | UI theme and brightness | AI-1164 | CD-2903 | core | plan D02 T16 §6 |  |
| NP-2609 | Canvas and desktop color | AI-1165 | CD-2905 | core | plan D02 T16 §6 |  |
| NP-2610 | Auto-collapse panels, documents as tabs, large tabs | AI-1166 | -- | core | plan D02 T16 §6 |  |
| NP-2611 | UI scaling and cursor scaling | AI-1167 | CD-2902 | core | plan D02 T16 §6 |  |
| NP-2612 | GPU compatibility check | AI-1212 | -- | core | plan D02 T16 §6 |  |
| NP-2613 | Safe mode | AI-1213 | -- | core | plan D02 T16 §6 |  |
| NP-2614 | Error reporting dialog toggle | -- | CD-012 | core | plan D02 T16 §6 |  |
| NP-2615 | Windows 11 window conventions | -- | CD-014 | core | plan D02 T16 §6 |  |
| NP-2616 | System information | -- | CD-046, CD-195 | core | plan D02 T16 §6 |  |
| NP-2617 | Refreshed icons and active-tool highlight | -- | CD-181 | core | plan D02 T16 §6 |  |
| NP-2618 | Fast launch budget | -- | CD-182 | core | plan D02 T16 §6 |  |
| NP-2619 | Appearance preferences page | -- | CD-208, CD-2894 | core | plan D02 T16 §6 |  |
| NP-2620 | Privacy: local-only usage data | -- | CD-2898 | core | plan D02 T16 §6 | no telemetry is sent; the page states it |
| NP-2621 | Hardware acceleration and GPU choice | -- | CD-2899 | core | plan D02 T16 §6 |  |
| NP-2622 | Center dialog boxes | -- | CD-2901 | core | plan D02 T16 §6 |  |
| NP-2623 | Window border color | -- | CD-2904 | core | plan D02 T16 §6 |  |
| NP-2624 | Navigator panel | AI-0925 | CD-033 | core | plan D02 T16 §7 |  |
| NP-2625 | Welcome screen | AI-0981 | CD-006, CD-177 | core | plan D02 T16 §7 | local only: new from preset, open, recent, guide |
| NP-2626 | Show the welcome screen when no documents are open | AI-0982, AI-1122 | -- | core | plan D02 T16 §7 |  |
| NP-2627 | Discover panel | AI-1201 | -- | core | plan D02 T16 §7 | local help topics and quick actions |
| NP-2628 | Quick start guide | -- | CD-007 | core | plan D02 T16 §7 |  |
| NP-2629 | Devices preferences page | AI-1184 | -- | core | plan D02 T16 §8 |  |
| NP-2630 | Touch workspace UI | AI-1203 | CD-071, CD-179 | core | plan D02 T16 §8 |  |
| NP-2631 | Surface Dial support | AI-1204 | CD-198 | core | plan D02 T16 §8 |  |
| NP-2632 | Touch gestures: pinch zoom, two-finger pan and rotate | -- | CD-070, CD-199 | core | plan D02 T16 §8 |  |
| NP-2633 | Tablet mode workspace auto-switch | -- | CD-180, CD-2843 | core | plan D02 T16 §8 |  |
| NP-2634 | Pen pressure, tilt, and bearing | -- | CD-197, CD-2850 | core | plan D02 T16 §8 | WPF stylus (Real-Time Stylus); no WinTab |
| NP-2635 | Pen pressure calibration and presets | -- | CD-2849 | core | plan D02 T16 §8 |  |
| NP-2636 | Tooltips and rich tooltips | AI-1119 | CD-005, CD-193 | core | plan D02 T16 §9 | AI-1119 moved here from §4 to merge with the tooltip rows |
| NP-2637 | Hints panel | -- | CD-002, CD-162, CD-165 | core | plan D02 T16 §9 | local hints, no cloud video |
| NP-2638 | Project timer toolbar | -- | CD-056, CD-154 | core | plan D02 T16 §9 |  |
| NP-2639 | Project timer tasks | -- | CD-075 | core | plan D02 T16 §9 |  |
| NP-2640 | Edit the active task and reset its counter | -- | CD-076 | core | plan D02 T16 §9 |  |
| NP-2641 | Export time sheet to CSV or TXT | -- | CD-077 | core | plan D02 T16 §9 |  |
| NP-2642 | Project timer automatic start | -- | CD-078 | core | plan D02 T16 §9 |  |
| NP-2643 | Inactivity detection and prompt | -- | CD-079, CD-082 | core | plan D02 T16 §9 |  |
| NP-2644 | Pause recording rules | -- | CD-080 | core | plan D02 T16 §9 |  |
| NP-2645 | Project timer toolbar appearance | -- | CD-081 | core | plan D02 T16 §9 |  |
| NP-2646 | Illustrator and CorelDRAW terminology map | -- | CD-112 | core | plan D02 T16 §9 |  |
| NP-2647 | Single-key tool shortcuts | -- | CD-186 | core | shipped-scope D02 T02 §8 |  |
| NP-2648 | About dialog | -- | CD-170 | core | shipped-scope D02 T05 §1 |  |
| NP-2649 | Help menu | AI-1211 | -- | core | shipped-scope D02 T05 §3 |  |
| NP-2650 | Cycle to next document | AI-0926 | CD-136 | core | shipped-scope D02 T06 §7 |  |
| NP-2651 | Tabbed and floating documents | AI-1208 | CD-016, CD-178 | core | shipped-scope D02 T06 §7 |  |
| NP-2652 | Accessible exported content (alt text, reading order) | AI-1099 | -- | core | shipped-scope D02 T06 §17 |  |
| NP-2653 | Screen reader and keyboard accessibility | AI-1206, AI-1207 | -- | core | shipped-scope D02 T06 §17 |  |
| NP-2654 | UI language | -- | CD-212, CD-2822 | core | shipped-scope D02 T06 §17 |  |
| NP-2655 | Check for updates | -- | CD-166 | core | shipped-scope D05 T01 §4 |  |
| NP-2656 | Product help and user guide | -- | CD-003, CD-004 | core | shipped-scope D06 T01 §1 |  |
| NP-2657 | Touch Bar controls | AI-1205 | -- | core | excluded: platform (hardware or OS feature Nodus cannot run on Windows) | macOS hardware only |

## Preferences

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2658 | Anchor, handle, and bounding box display size | AI-0166, AI-1139 | CD-2860 | core | plan D02 T16 §4 |  |
| NP-2659 | Use preview bounds | AI-0244, AI-1124 | -- | core | plan D02 T16 §4 |  |
| NP-2660 | Keyboard increment | AI-1114 | -- | core | plan D02 T16 §4 |  |
| NP-2661 | Constrain angle | AI-1115 | CD-2880 | core | plan D02 T16 §4 |  |
| NP-2662 | Default corner radius | AI-1116 | -- | core | plan D02 T16 §4 |  |
| NP-2663 | Disable pen auto add and delete | AI-1117 | -- | core | plan D02 T16 §4 |  |
| NP-2664 | Precise cursors | AI-1118 | -- | core | plan D02 T16 §4 |  |
| NP-2665 | Anti-aliased artwork | AI-1120 | -- | core | plan D02 T16 §4 |  |
| NP-2666 | Legacy new document dialog | AI-1123 | -- | core | plan D02 T16 §4 | consumer is the New Document dialog of D02 T07 §14 |
| NP-2667 | Display print size at 100% zoom | AI-1125 | -- | core | plan D02 T16 §4 |  |
| NP-2668 | Double-click to isolate | AI-1127 | -- | core | plan D02 T16 §4 |  |
| NP-2669 | Transform pattern tiles, scale corners, scale strokes defaults | AI-1129 | -- | core | plan D02 T16 §4 |  |
| NP-2670 | Zoom with mouse wheel and scroll direction | AI-1130 | -- | core | plan D02 T16 §4 | consumer is the zoom of D02 T07 §12 |
| NP-2671 | Reset preferences | AI-1132 | -- | core | plan D02 T16 §4 |  |
| NP-2672 | Selection tolerance | AI-1133 | -- | core | plan D02 T16 §4 |  |
| NP-2673 | Object selection by path only | AI-1134 | -- | core | plan D02 T16 §4 |  |
| NP-2674 | Snap to point distance | AI-1135 | -- | core | plan D02 T16 §4 | consumer is the snapping of D02 T02 §7 |
| NP-2675 | Ctrl+click to select objects behind | AI-1136 | -- | core | plan D02 T16 §4 |  |
| NP-2676 | Move locked and hidden artwork with artboards | AI-1137 | -- | core | plan D02 T16 §4 |  |
| NP-2677 | Zoom to selection | AI-1138 | -- | core | plan D02 T16 §4 |  |
| NP-2678 | Show handles for multiple selected anchors | AI-1140 | -- | core | plan D02 T16 §4 |  |
| NP-2679 | Rubber band preview for pen and curvature | AI-1141 | -- | core | plan D02 T16 §4 |  |
| NP-2680 | Type object selection by path only | AI-1145 | -- | core | plan D02 T16 §4 |  |
| NP-2681 | Show font names in English | AI-1146 | -- | core | plan D02 T16 §4 |  |
| NP-2682 | Number of recent fonts | AI-1147 | -- | core | plan D02 T16 §4 |  |
| NP-2683 | Rectangle tool defaults | -- | CD-2851 | core | plan D02 T16 §4 |  |
| NP-2684 | Ellipse tool defaults | -- | CD-2852 | core | plan D02 T16 §4 |  |
| NP-2685 | Spiral tool defaults | -- | CD-2853 | core | plan D02 T16 §4 |  |
| NP-2686 | Graph paper tool defaults | -- | CD-2854 | core | plan D02 T16 §4 |  |
| NP-2687 | Node shape per node type | -- | CD-2861 | core | plan D02 T16 §4 |  |
| NP-2688 | Show curve direction when editing | -- | CD-2862 | core | plan D02 T16 §4 |  |
| NP-2689 | Show unselected nodes filled | -- | CD-2863 | core | plan D02 T16 §4 |  |
| NP-2690 | Node and handle color scheme with main and secondary colors | -- | CD-2864, CD-2865 | core | plan D02 T16 §4 |  |
| NP-2691 | Show highlight on vector previews | -- | CD-2867 | core | plan D02 T16 §4 |  |
| NP-2692 | Show node types in different colors | -- | CD-2868 | core | plan D02 T16 §4 |  |
| NP-2693 | Save settings as default for new documents | -- | CD-2874, CD-2900 | core | plan D02 T16 §4 |  |
| NP-2694 | Ctrl and Shift key convention | -- | CD-2879 | core | plan D02 T16 §4 |  |
| NP-2695 | Preferences category switcher | -- | CD-2892 | core | plan D02 T16 §4 |  |
| NP-2696 | Application preferences page | -- | CD-2893, CD-2908 | core | plan D02 T16 §4 |  |
| NP-2697 | Tool preferences page | -- | CD-2895 | core | plan D02 T16 §4 |  |
| NP-2698 | Global suite preferences page | -- | CD-2896, CD-2910 | core | plan D02 T16 §4 |  |
| NP-2699 | Save and export in the background | AI-0970, AI-1174 | CD-2840 | core | plan D02 T16 §5 |  |
| NP-2700 | Scratch folder | AI-1163 | -- | core | plan D02 T16 §5 | plug-in folders excluded with automation |
| NP-2701 | GPU rendering and GPU memory | AI-1168 | -- | core | plan D02 T16 §5 |  |
| NP-2702 | Animated zoom | AI-1169 | -- | core | plan D02 T16 §5 | consumer is the zoom of D02 T07 §12 |
| NP-2703 | Undo levels | AI-1170 | CD-2827 | core | plan D02 T16 §5 | limit enforced by the history of D01 T02 §4 |
| NP-2704 | Real-time drawing and editing | AI-1171 | -- | core | plan D02 T16 §5 |  |
| NP-2705 | Recovery data interval and folder | AI-1172 | -- | core | plan D02 T16 §5 | consumer is the recovery of D02 T04 §5 |
| NP-2706 | Turn off recovery for complex documents | AI-1173 | -- | core | plan D02 T16 §5 |  |
| NP-2707 | Number of recent files | AI-1175 | -- | core | plan D02 T16 §5 |  |
| NP-2708 | Warnings and message settings | -- | CD-167, CD-194, CD-2839 | core | plan D02 T16 §5 |  |
| NP-2709 | Startup action | -- | CD-2823 | core | plan D02 T16 §5 |  |
| NP-2710 | Show the New Document dialog | -- | CD-2824 | core | plan D02 T16 §5 | consumer is the New Document dialog of D02 T07 §14 |
| NP-2711 | Missing content folder indicator | -- | CD-2826 | core | plan D02 T16 §5 |  |
| NP-2712 | Back up original file before saving | -- | CD-2837 | core | plan D02 T16 §5 | consumer is the save path of D02 T07 §14 |
| NP-2713 | Auto-backup interval and location | -- | CD-2838 | core | plan D02 T16 §5 |  |
| NP-2714 | Content folder locations | -- | CD-2841 | core | plan D02 T16 §5 |  |
| NP-2715 | Working folder | -- | CD-2845 | cloud | plan D02 T16 §5 | a local folder; no document management service |
| NP-2716 | Import and export format filters | -- | CD-2906 | core | plan D02 T16 §5 |  |
| NP-2717 | Keyboard shortcut editor | AI-1105 | CD-088 | core | shipped-scope D02 T06 §13 |  |
| NP-2718 | Preferences dialog with search | AI-1113 | -- | core | shipped-scope D02 T06 §13 |  |

## Utilities

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2719 | Document info panel | AI-1214 | -- | core | plan D02 T16 §10 |  |
| NP-2720 | Find and replace objects panel | -- | CD-113, CD-159, CD-491 | core | plan D02 T16 §10 |  |
| NP-2721 | Find query builder | -- | CD-492 | core | plan D02 T16 §10 |  |
| NP-2722 | Find from selection | -- | CD-493 | core | plan D02 T16 §10 |  |
| NP-2723 | Find by name or style | -- | CD-494 | core | plan D02 T16 §10 |  |
| NP-2724 | Find next, previous, all, and all on page | -- | CD-495 | core | plan D02 T16 §10 |  |
| NP-2725 | Save and load search criteria | -- | CD-496 | core | plan D02 T16 §10 | own JSON criteria file, not FIN |
| NP-2726 | Replace object properties | -- | CD-497 | core | plan D02 T16 §10 |  |
| NP-2727 | Find and replace search range | -- | CD-498 | core | plan D02 T16 §10 |  |
| NP-2728 | Object data panel | -- | CD-530, CD-579 | core | plan D02 T16 §10 |  |
| NP-2729 | Object data field editor | -- | CD-531 | core | plan D02 T16 §10 |  |
| NP-2730 | Object data field formats | -- | CD-532 | core | plan D02 T16 §10 |  |
| NP-2731 | Copy object data from another object | -- | CD-533 | core | plan D02 T16 §10 |  |
| NP-2732 | Clear all object data fields | -- | CD-534 | core | plan D02 T16 §10 |  |
| NP-2733 | Object data manager spreadsheet | -- | CD-535 | core | plan D02 T16 §10 |  |
| NP-2734 | Object data manager: show levels | -- | CD-536 | core | plan D02 T16 §10 |  |
| NP-2735 | Object data manager: summarize groups | -- | CD-537 | core | plan D02 T16 §10 |  |
| NP-2736 | Object data manager: show hierarchy | -- | CD-538 | core | plan D02 T16 §10 |  |
| NP-2737 | Object data manager: show totals | -- | CD-539 | core | plan D02 T16 §10 |  |
| NP-2738 | Print object data summary | -- | CD-540 | print | plan D02 T16 §10 |  |
| NP-2739 | Insert barcode | -- | CD-1693, CD-1738 | core | plan D02 T16 §11 | EAN, UPC, Code 128, Code 39, ITF, and more via ZXing.Net |
| NP-2740 | Insert QR code | -- | CD-1698, CD-1739 | core | plan D02 T16 §11 | generated locally with ZXing.Net, no sign-in |
| NP-2741 | QR code content types | -- | CD-1699, CD-1700, CD-1701, CD-1702, CD-1703, CD-1704, CD-1705, CD-1706 | core | plan D02 T16 §11 | URL, email, phone, SMS, vCard or meCard, event, geo, text |
| NP-2742 | QR pixel fill and background fill | -- | CD-1707 | core | plan D02 T16 §11 |  |
| NP-2743 | QR pixel outline | -- | CD-1708 | core | plan D02 T16 §11 |  |
| NP-2744 | QR quiet-zone margin | -- | CD-1709 | core | plan D02 T16 §11 |  |
| NP-2745 | QR pixel shape and fill factor | -- | CD-1710 | core | plan D02 T16 §11 |  |
| NP-2746 | QR weld pixels | -- | CD-1711 | core | plan D02 T16 §11 |  |
| NP-2747 | QR pixel roundness | -- | CD-1712 | core | plan D02 T16 §11 |  |
| NP-2748 | QR error correction level | -- | CD-1713 | core | plan D02 T16 §11 |  |
| NP-2749 | QR code styles and defaults | -- | CD-1714 | core | plan D02 T16 §11 |  |
| NP-2750 | Validate QR codes and barcodes | -- | CD-1715, CD-1716 | cloud | plan D02 T16 §11 | decoded locally with ZXing.Net, no online check |

## Automation

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2751 | Extension panels and plug-in SDKs | AI-1210, AI-1233 | -- | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2752 | Record and play back actions or macros | AI-1218, AI-1220, AI-1221, AI-1222, AI-1223, AI-1224, AI-1225, AI-1226, AI-1241 | CD-2114, CD-2930, CD-2931, CD-2932, CD-2935, CD-2937, CD-2942, CD-2944, CD-2947, CD-2948, CD-2949, CD-2950 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2753 | Action sets and recording project management | AI-1219, AI-1227, AI-1228 | CD-2933 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2754 | Batch processing of files | AI-1229, AI-1230 | -- | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2755 | Scripts menu and scripts docker | AI-1231 | CD-054, CD-152, CD-2920, CD-2923, CD-2924, CD-2925, CD-2927, CD-2928, CD-2929, CD-2936, CD-2941, CD-2943, CD-2945, CD-2952 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2756 | Scripting languages and macro runtimes (JavaScript, VBA, VSTA) | AI-1232 | CD-2913, CD-2914, CD-2915, CD-2940 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2757 | MCP server for external AI tools | AI-1242, AI-1243 | -- | ai | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2758 | Macro projects embedded in documents | -- | CD-2912, CD-2926 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2759 | Macro security and trusted publishers | -- | CD-2916, CD-2917, CD-2918, CD-2919, CD-2951 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2760 | Script editor and object model reference | -- | CD-2921, CD-2922, CD-2938, CD-2939, CD-2946 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |
| NP-2761 | Save undo history as a script | -- | CD-2934 | automation | excluded: automation (scripting, macros, recorded actions, and plug-in SDKs are out of scope, operator decision 2026-09-26) |  |

## Cloud and collaboration

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2762 | Cloud asset libraries | AI-0485, AI-1216, AI-1217, AI-1253 | CD-262, CD-1734, CD-2955 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2763 | Online templates | AI-0961, AI-0987 | CD-234, CD-280, CD-2993 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2764 | Launch external asset browser (Bridge) | AI-0967 | -- | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2765 | Cloud document version history | AI-0972 | -- | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2766 | Stock image search | AI-0979 | -- | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2767 | Share and invite to edit or review | AI-0980, AI-1244, AI-1245 | CD-2991 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2768 | Cloud documents with sync and dashboard | AI-0983, AI-1180, AI-1247, AI-1248 | CD-2953, CD-2963, CD-2964, CD-2965, CD-2966, CD-2990 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2769 | Shared cloud projects | AI-0984, AI-0985, AI-0986 | -- | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2770 | Export to cloud storage | AI-1033, AI-1041 | -- | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2771 | Export to Firefly Boards | AI-1042 | -- | ai | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2772 | Settings sync | AI-1109 | -- | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2773 | Online fonts and remote font activation | AI-1155, AI-1250, AI-1251, AI-1252 | CD-1083, CD-1084, CD-1177, CD-1178, CD-2994 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2774 | Review comments | AI-1215, AI-1246 | CD-2968, CD-2969, CD-2970, CD-2971, CD-2972, CD-2980, CD-2981, CD-2982, CD-2983, CD-2989 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2775 | Round-trip with other Creative Cloud apps | AI-1249 | -- | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2776 | Online learning docker and tutorials | -- | CD-001, CD-008, CD-009, CD-010 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2777 | Submit ideas and feedback | -- | CD-011, CD-169 | core | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2778 | Account sign-in and settings | -- | CD-168, CD-2967, CD-3003 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2779 | Content store and Get More downloads | -- | CD-273, CD-274, CD-291, CD-769, CD-1196, CD-1392, CD-3004 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2780 | Export to WordPress | -- | CD-2564, CD-2984, CD-2985 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2781 | Browser version of the editor | -- | CD-2954, CD-2995, CD-2996, CD-2997, CD-2998, CD-2999, CD-3000 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2782 | SharePoint document management and check-in | -- | CD-2956, CD-2957, CD-2958, CD-2959, CD-2960, CD-2961, CD-2962, CD-2986, CD-2987, CD-2988, CD-3002 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2783 | Comment markup and annotation tools | -- | CD-2973, CD-2974, CD-2975, CD-2976, CD-2977, CD-2978, CD-2979, CD-2992 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |
| NP-2784 | CorelDRAW Go web app | -- | CD-3001 | cloud | excluded: cloud (cloud documents, libraries, sharing, accounts, stores, and online services are out of scope, operator decision 2026-09-26) |  |

## Companion apps

| ID | Feature | Illustrator | CorelDRAW | Category | Status | Notes |
| -- | ------- | ----------- | --------- | -------- | ------ | ----- |
| NP-2785 | Application launcher | -- | CD-049 | companion | other-app: none launcher for other Corel applications, plug-ins, and the Get More store is outside the suite's scope |  |
| NP-2786 | Bevel effect on an editable area | -- | CD-2116 | companion | other-app: Imago PHOTO-PAINT effect needing an editable area or mask is raster editing, Imago's job |  |
| NP-2787 | Glass effect on an editable area | -- | CD-2119 | companion | other-app: Imago PHOTO-PAINT effect needing an editable area or mask is raster editing, Imago's job |  |
| NP-2788 | Mask-edge emboss effect (The Boss) | -- | CD-2123 | companion | other-app: Imago PHOTO-PAINT effect needing an editable area or mask is raster editing, Imago's job |  |
| NP-2789 | Bokeh blur outside an editable area | -- | CD-2147 | companion | other-app: Imago PHOTO-PAINT effect needing an editable area or mask is raster editing, Imago's job |  |
| NP-2790 | Double-click bitmap to edit in raster editor | -- | CD-2888 | companion | other-app: Imago double-click round-trip editing of bitmaps in a raster editor is Imago's job |  |
| NP-2791 | Standalone font manager | -- | CD-3030 | companion | other-app: none standalone font manager outside the suite's scope |  |
| NP-2792 | Round-trip bitmap editing in a raster editor | -- | CD-3031 | companion | other-app: Imago Corel PHOTO-PAINT bitmap round-trip editing is Imago's job |  |
| NP-2793 | Raster image editor | -- | CD-3032 | companion | other-app: Imago Corel PHOTO-PAINT raster editing is Imago's job |  |
| NP-2794 | Mask from subject | -- | CD-3033 | companion | other-app: Imago PHOTO-PAINT subject masking is Imago's job |  |
| NP-2795 | Quick AI image generation in the raster editor | -- | CD-3034 | companion | other-app: Imago PHOTO-PAINT AI image generation is Imago's job |  |
| NP-2796 | Standalone font manager with online font services | -- | CD-3035 | companion | other-app: none standalone font manager with online font services outside the suite's scope |  |
| NP-2797 | Screen capture utility | -- | CD-3036 | companion | other-app: none screen capture utility outside the suite's scope |  |
| NP-2798 | RAW and HDR photo processing app | -- | CD-3037 | companion | other-app: Lumen AfterShot RAW and HDR photo workflow is Lumen's job |  |
| NP-2799 | CorelDRAW Web | -- | CD-3038 | companion | other-app: none browser version of CorelDRAW is a cloud product outside the suite's scope |  |
| NP-2800 | CorelDRAW Go | -- | CD-3039 | companion | other-app: none separately sold web design app outside the suite's scope |  |
| NP-2801 | Technical suite edition | -- | CD-3040 | companion | other-app: none sibling technical suite product outside the suite's scope |  |
| NP-2802 | Bundled clipart, photo, and font content | -- | CD-3041 | companion | other-app: none bundled clipart, photo, and font content library outside the suite's scope |  |
