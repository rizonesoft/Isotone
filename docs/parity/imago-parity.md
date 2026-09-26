# Imago Parity Catalog

Every Adobe Photoshop 27.10 (with Camera Raw 18.6), Affinity by Canva 3.3 (Affinity Photo), and GIMP 3.2.6 feature, merged into Imago features, each with exactly one status. The sources are [`sources/photoshop-27.10.md`](sources/photoshop-27.10.md), [`sources/affinity-3.3.md`](sources/affinity-3.3.md), and [`sources/gimp-3.2.6.md`](sources/gimp-3.2.6.md); the status grammar and the update rules are in [`README.md`](README.md); the sections that own `plan` rows are designed in [`imago-section-design.md`](imago-section-design.md).

**Totals (2026-09-26, rows added 2026-09-27):** 2,385 features covering 3,176 Photoshop rows, 2,762 Affinity rows, and 4,891 GIMP rows (10,829 in all); every source id appears in exactly one row. The 18 rows IP-2368 to IP-2385 were added on 2026-09-27 for ACDSee Edit-mode capabilities that the Lumen catalog ([`lumen-parity.md`](lumen-parity.md)) routes to Imago and no Imago row covered; they carry no Photoshop, Affinity, or GIMP id. On 2026-09-27 the operator also directed the eight rows that pointed at B-012 and B-024, and the G'MIC row, into planned sections (`D03 T14 §11` to `§13` on the `D01 T09` plug-in host). GIMP's inventory lists one row per documented option, so its rows fold into features far more often than the other two.

| Status | Features | Source rows |
| ------ | -------: | ----------: |
| `plan` | 2,024 | 9,558 |
| `shipped-scope` | 204 | 762 |
| `backlog` | 92 | 361 |
| `excluded` | 54 | 129 |
| `other-app` | 11 | 19 |
| **Total** | **2,385** | **10,829** |

## Areas

- [Documents and canvas](#documents-and-canvas) (25)
- [View, guides, and measurement](#view-guides-and-measurement) (103)
- [History, clipboard, and the Image menu](#history-clipboard-and-the-image-menu) (88)
- [Layers and the Layers panel](#layers-and-the-layers-panel) (61)
- [Masks, clipping, and blending](#masks-clipping-and-blending) (81)
- [Layer styles, smart objects, comps, and artboards](#layer-styles-smart-objects-comps-and-artboards) (89)
- [Selection](#selection) (98)
- [Channels and quick mask](#channels-and-quick-mask) (19)
- [Adjustments](#adjustments) (111)
- [Image modes and color](#image-modes-and-color) (22)
- [Color panels, swatches, and palettes](#color-panels-swatches-and-palettes) (42)
- [Brushes and painting](#brushes-and-painting) (109)
- [Fill, gradients, and patterns](#fill-gradients-and-patterns) (54)
- [Retouching](#retouching) (37)
- [Transform, warp, and liquify](#transform-warp-and-liquify) (60)
- [Filter framework](#filter-framework) (39)
- [Blur, sharpen, and noise filters](#blur-sharpen-and-noise-filters) (72)
- [Distort, map, and pixelate filters](#distort-map-and-pixelate-filters) (87)
- [Render, light, and shadow filters](#render-light-and-shadow-filters) (66)
- [Artistic, stylize, edge, and generic filters](#artistic-stylize-edge-and-generic-filters) (148)
- [Develop and tone mapping](#develop-and-tone-mapping) (108)
- [HDR, panorama, stacks, and astrophotography](#hdr-panorama-stacks-and-astrophotography) (74)
- [Type](#type) (56)
- [Paths, shapes, and vectors](#paths-shapes-and-vectors) (67)
- [File menu and formats](#file-menu-and-formats) (157)
- [Metadata](#metadata) (21)
- [Export and web](#export-and-web) (50)
- [Color management](#color-management) (38)
- [Print](#print) (21)
- [AI](#ai) (128)
- [Workspace and UI](#workspace-and-ui) (49)
- [Preferences](#preferences) (71)
- [Help and learning](#help-and-learning) (16)
- [Automation](#automation) (49)
- [Video and animation](#video-and-animation) (32)
- [Cloud and collaboration](#cloud-and-collaboration) (23)
- [3D (removed)](#3d-removed) (8)
- [Companion and other apps](#companion-and-other-apps) (6)

## Documents and canvas

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0001 | Image properties: precision readout | -- | -- | GP-1113 | core | plan D03 T08 §12 |  |
| IP-0002 | Transparent background at creation and as a toggle command | -- | AF-2231, AF-2232 | -- | core | plan D03 T08 §12 | extends D03 T03 §1 (new document background transparent) |
| IP-0003 | Duplicate image, optionally merged layers only | PS-A-1200 | -- | GP-1090 | core | plan D03 T08 §12 |  |
| IP-0004 | Document setup after creation: units, DPI, dimensions with rescale or anchor | -- | AF-2325, AF-2326, AF-2327 | -- | core | plan D03 T08 §12 | Imago Document Properties dialog |
| IP-0005 | Image properties dialog: size, resolution, color space, file, memory, undo and element counts | -- | -- | GP-1105, GP-1106, GP-1109, GP-1111, GP-1112, GP-1114, GP-1115, GP-1116, GP-1117, GP-1118, GP-1119, GP-1120, GP-1121, GP-1122, GP-1123 | core | plan D03 T08 §12 |  |
| IP-0006 | Pixel aspect ratio and aspect-corrected preview | PS-A-1711, PS-A-1712 | -- | -- | video | plan D03 T08 §12 |  |
| IP-0007 | Image properties: color profile and print size tabs | -- | -- | GP-1107, GP-1110 | core | plan D03 T08 §12 | Profile readout from D03 T18 §4 |
| IP-0008 | Pixel aspect ratio correction view | PS-B-0840 | -- | -- | video | plan D03 T08 §12 |  |
| IP-0009 | New document presets: saved presets, categories, favorites, orientation, new from last preset | -- | AF-2311, AF-2312, AF-2321, AF-2322 | -- | core | plan D03 T08 §2 | extends D03 T03 §1 |
| IP-0010 | New document from clipboard (paste as new image) | -- | AF-2323 | GP-0892 | core | plan D03 T08 §2 |  |
| IP-0011 | New document bleed setting | -- | AF-2318 | -- | print | plan D03 T08 §2 | Print bleed used by D03 T18 §6 |
| IP-0012 | Templates: save as template, template folders, edit template, templates dialog | -- | AF-2356, AF-2357, AF-2358 | GP-4068, GP-4069, GP-4070, GP-4072, GP-4073, GP-4074, GP-4075, GP-4076 | core | plan D03 T08 §2 |  |
| IP-0013 | Template settings: size, orientation, resolution, color space, precision, gamma, profiles, fill, comment | -- | -- | GP-4077, GP-4078, GP-4079, GP-4080, GP-4081, GP-4082, GP-4083, GP-4084, GP-4085, GP-4086, GP-4087, GP-4088, GP-4089, GP-4090, GP-4091, GP-4092 | core | plan D03 T08 §2 |  |
| IP-0014 | Open recent list with locate and remove entries | -- | AF-2347 | -- | core | plan D03 T08 §2 | extends D03 T04 §2 recent files |
| IP-0015 | New document dialog: preset categories and saved presets | PS-B-0877, PS-B-0878, PS-B-0883, PS-B-0884 | -- | GP-0842 | core | plan D03 T08 §2 | extends D03 T03 §1 |
| IP-0016 | New document settings: orientation, color mode, precision, gamma, color profile, pixel aspect, fill (incl. middle gray), comment | PS-B-0880, PS-B-0881, PS-B-0882 | -- | GP-0020, GP-0844, GP-0845, GP-0846, GP-0847, GP-0848, GP-0849, GP-0850, GP-0851, GP-0852, GP-0856, GP-0857 | core | plan D03 T08 §2 | extends D03 T03 §1 |
| IP-0017 | Document templates: create template, new from template | -- | AF-2595 | GP-0823, GP-0843 | format | plan D03 T08 §2 | Imago templates are .imago files, Affinity .aftemplate reading follows B-045 |
| IP-0018 | Recent documents list: count and keep record of used files | PS-B-1259 | -- | GP-4265 | core | plan D03 T08 §2 |  |
| IP-0019 | Template editing dialog | -- | -- | GP-4071 | core | plan D03 T08 §2 |  |
| IP-0020 | Documents in tabs with modified marker | PS-A-1746 | AF-2353 | -- | core | shipped-scope D03 T03 §1 | Floating document windows planned in D03 T08 §3 |
| IP-0021 | New document dialog: size, resolution, and units | -- | AF-2310, AF-2314, AF-2315 | -- | core | shipped-scope D03 T03 §1 |  |
| IP-0022 | Multiple documents as tabs | PS-B-0945 | -- | -- | core | shipped-scope D03 T03 §1 |  |
| IP-0023 | Close document | PS-B-0891 | -- | GP-0821 | core | shipped-scope D03 T03 §1 |  |
| IP-0024 | Exit with close prompts | PS-B-0941 | -- | GP-0867 | core | shipped-scope D03 T03 §1 |  |
| IP-0025 | Adobe Stock templates in New Document | PS-B-0879 | -- | -- | cloud | excluded: cloud |  |

## View, guides, and measurement

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0026 | Zoom commands: zoom in and out, fit, fill, 100, 200 percent and preset levels | PS-A-1714, PS-A-1715, PS-A-1716, PS-A-1718, PS-A-1719, PS-A-0482, PS-A-0497 | AF-0379, AF-0380, AF-2399 | GP-0221, GP-1068, GP-1070, GP-1071, GP-1072, GP-1073, GP-1075 | core | plan D03 T08 §3 |  |
| IP-0027 | Zoom to selection, revert zoom, typed and custom zoom factor | PS-A-1748 | -- | GP-1069, GP-1074, GP-1076 | core | plan D03 T08 §3 |  |
| IP-0028 | Scroll wheel zoom and zoom clicked point to center | PS-A-0495, PS-A-0496 | -- | GP-0223 | core | plan D03 T08 §13 |  |
| IP-0029 | Scrubby, animated, and temporary Z-key zoom | PS-A-0493, PS-A-0494 | AF-2397, AF-2398 | -- | core | plan D03 T08 §13 |  |
| IP-0030 | Resize windows to fit when zooming | PS-A-0491 | -- | GP-0224 | core | plan D03 T08 §13 |  |
| IP-0031 | Scroll, zoom, and rotate all windows together | PS-A-0481, PS-A-0492, PS-A-0488 | -- | -- | core | plan D03 T08 §13 |  |
| IP-0032 | Birds-eye view | PS-A-0483 | -- | -- | core | plan D03 T08 §13 |  |
| IP-0033 | Flick panning | PS-A-0484 | -- | -- | core | plan D03 T08 §13 |  |
| IP-0034 | Print size, actual size, and dot for dot views | PS-A-1720, PS-A-1721 | AF-2320 | GP-1027 | print | plan D03 T08 §13 |  |
| IP-0035 | Rotate view tool, rotation angle, 15 degree steps, reset, wheel rotation | PS-A-0485, PS-A-0486, PS-A-0487, PS-A-0489 | AF-2402, AF-2403, AF-2404 | GP-1028, GP-1029, GP-1031, GP-1032, GP-1033, GP-1034, GP-1035, GP-1036 | core | plan D03 T08 §3 |  |
| IP-0036 | Flip view horizontally and vertically | PS-A-1722 | -- | GP-1030 | core | plan D03 T08 §3 |  |
| IP-0037 | Screen modes and full screen | PS-A-1724 | -- | GP-1037 | core | plan D03 T08 §3 |  |
| IP-0038 | Show or hide menubar, scrollbars, and status bar | -- | -- | GP-1055, GP-1058, GP-1060 | core | plan D03 T08 §3 |  |
| IP-0039 | Padding color: theme, checks, custom, keep in show all | -- | -- | GP-1041, GP-1042, GP-1043, GP-1044, GP-1045, GP-1046, GP-1047 | core | plan D03 T08 §3 |  |
| IP-0040 | Show all and clip to canvas (view pixels outside the canvas) | -- | AF-2395 | GP-1049, GP-1050 | core | plan D03 T08 §3 |  |
| IP-0041 | Preview mode hides guides, grids, and margins | -- | AF-2394 | -- | core | plan D03 T08 §3 |  |
| IP-0042 | Extras toggle and show extras options | PS-A-1725, PS-A-1739, PS-A-1740 | -- | -- | core | plan D03 T08 §3 |  |
| IP-0043 | Show layer edges and canvas boundary | PS-A-1726 | -- | GP-1051, GP-1054 | core | plan D03 T08 §3 |  |
| IP-0044 | Pixel grid at high zoom | PS-A-1699, PS-A-1734 | AF-2382 | -- | core | plan D03 T08 §3 |  |
| IP-0045 | Show layer edges | PS-A-0803 | -- | -- | core | plan D03 T08 §3 |  |
| IP-0046 | Rotate document view | -- | AF-0778 | -- | core | plan D03 T08 §13 |  |
| IP-0047 | Screen modes: standard, full screen with menu bar, full screen, F cycles | PS-A-0016, PS-B-1371 | -- | -- | core | plan D03 T08 §3 |  |
| IP-0048 | Canvas navigation preferences: scroll wheel zoom, scrubby and animated zoom, drag-to-zoom speed, zoom to clicked point, space bar pan or move | PS-B-1234, PS-B-1235, PS-B-1236 | AF-2705, AF-2706 | GP-4133, GP-4134, GP-4135, GP-4136 | core | plan D03 T08 §13 |  |
| IP-0049 | Rotate view with trackpad or modifier scroll, flick panning, overscroll | PS-B-1230, PS-B-1231, PS-B-1381 | AF-2708 | -- | core | plan D03 T08 §13 |  |
| IP-0050 | Image window preferences: show all, dot for dot, resize window on zoom or image change, initial zoom ratio, limit initial zoom to 100 percent | PS-B-1237 | AF-2647 | GP-4185, GP-4188, GP-4190, GP-4191, GP-4193, GP-4194, GP-4195 | core | plan D03 T08 §13 |  |
| IP-0051 | Monitor resolution for print-size view: detect, enter manually, calibrate | -- | -- | GP-4164, GP-4165, GP-4166 | core | plan D03 T08 §13 |  |
| IP-0052 | New window for the same document | PS-A-1744 | AF-2389 | GP-1040 | core | plan D03 T08 §10 |  |
| IP-0053 | Arrange windows: tile, consolidate, float, match zoom, location, rotation | PS-A-1743, PS-A-1745 | -- | -- | core | plan D03 T08 §10 |  |
| IP-0054 | Shrink wrap and center image in window | -- | -- | GP-1048, GP-1061, GP-3918 | core | plan D03 T08 §10 |  |
| IP-0055 | View modes: pixels, retina, vector, wireframe, with default mode | -- | AF-2390, AF-2393 | -- | core | plan D03 T08 §10 |  |
| IP-0056 | Split view comparing two view modes | -- | AF-2391 | -- | core | plan D03 T08 §10 |  |
| IP-0057 | Grayscale view | -- | AF-2392 | -- | core | plan D03 T08 §10 |  |
| IP-0058 | Display filters: view-only filter stack | -- | -- | GP-1003, GP-1004 | core | plan D03 T08 §10 |  |
| IP-0059 | Clip warning display filter: shadows, highlights, NaN colors, alpha options | -- | -- | GP-1006, GP-1011, GP-1012, GP-1013, GP-1014, GP-1015, GP-1016, GP-1017, GP-1018 | core | plan D03 T08 §10 |  |
| IP-0060 | Contrast and gamma display filters | -- | -- | GP-1008, GP-1009, GP-1023 | core | plan D03 T08 §10 |  |
| IP-0061 | Navigator panel with view box, zoom slider, buttons, proxy color | PS-A-0498, PS-A-0499 | AF-2405, AF-2447 | GP-1039, GP-3912, GP-3913, GP-3914, GP-3915, GP-3916, GP-3917 | core | plan D03 T08 §10 |  |
| IP-0062 | Navigator saved view points and previous or next view point | -- | AF-2406, AF-2407, AF-2448 | -- | core | plan D03 T08 §10 |  |
| IP-0063 | Arrange documents: tile vertically or horizontally, 2-up to 6-up, consolidate to tabs, cascade, float in window | PS-B-1314, PS-B-1315, PS-B-1316, PS-B-1317, PS-B-1318, PS-B-1319 | -- | -- | core | plan D03 T08 §10 |  |
| IP-0064 | Match zoom, location, rotation across documents and new window for a document | PS-B-1320, PS-B-1321 | -- | -- | core | plan D03 T08 §10 |  |
| IP-0065 | Open documents list in the Window menu and Images panel with raise, new view, list or grid | PS-B-1366 | -- | GP-3869, GP-3870, GP-3871, GP-3872, GP-3873, GP-3874, GP-3875, GP-3876, GP-4320 | core | plan D03 T08 §10 |  |
| IP-0066 | Previous and next view point | -- | AF-2449 | -- | core | plan D03 T08 §10 |  |
| IP-0067 | Navigator panel | PS-B-1352 | -- | -- | core | plan D03 T08 §10 |  |
| IP-0068 | Ruler origin drag and reset | PS-A-1677 | -- | -- | core | plan D03 T08 §4 |  |
| IP-0069 | Document and ruler units: pixels, physical, points, picas, percent | PS-A-1678 | AF-2313, AF-2344, AF-2345, AF-0381 | -- | core | plan D03 T08 §4 |  |
| IP-0070 | Custom units editor | -- | -- | GP-0935, GP-0936, GP-0937 | core | plan D03 T08 §4 |  |
| IP-0071 | New guide at exact position | PS-A-1679 | -- | GP-1093, GP-1262, GP-1263, GP-1264 | core | plan D03 T08 §4 |  |
| IP-0072 | New guide by percent | -- | -- | GP-1259, GP-1260, GP-1261 | core | plan D03 T08 §4 |  |
| IP-0073 | New guide layout: columns, rows, gutters, margins, center guides | PS-A-1680 | AF-2317, AF-2385, AF-2386 | -- | core | plan D03 T08 §4 |  |
| IP-0074 | Guides from shape or selection bounds | PS-A-1681 | -- | GP-1265 | core | plan D03 T08 §4 |  |
| IP-0075 | Drag, move, clone, and delete guides with snapping modifiers | PS-A-1682, PS-A-1683 | AF-2384, AF-2388 | -- | core | plan D03 T08 §4 |  |
| IP-0076 | Guide edit dialog with per-guide color | PS-A-1684, PS-A-1687 | -- | -- | core | plan D03 T08 §4 |  |
| IP-0077 | Lock guides | PS-A-1685 | AF-2387 | -- | core | plan D03 T08 §4 |  |
| IP-0078 | Clear guides | PS-A-1686 | -- | GP-1266 | core | plan D03 T08 §4 |  |
| IP-0079 | Off-canvas guides | -- | -- | GP-0022 | core | plan D03 T08 §4 |  |
| IP-0080 | Show grid and guides toggles | PS-A-1689, PS-A-1690, PS-A-1729 | AF-2379 | GP-1052, GP-1053 | core | plan D03 T08 §14 |  |
| IP-0081 | Grid configuration: spacing, divisions, line style, colors | -- | AF-2380 | GP-1077, GP-1078, GP-1079, GP-1080, GP-1081, GP-1082, GP-1083, GP-1084, GP-1085, GP-1086 | core | plan D03 T08 §14 |  |
| IP-0082 | Angular and non-uniform axis grids | -- | AF-2381 | -- | core | plan D03 T08 §14 |  |
| IP-0083 | Smart guides with alignment and distance labels | PS-A-1691, PS-A-1692, PS-A-1731 | AF-2377 | -- | core | plan D03 T08 §14 |  |
| IP-0084 | Snapping toggle and snap to all or none | PS-A-1700, PS-A-1706 | AF-2364 | -- | core | plan D03 T08 §14 |  |
| IP-0085 | Snap to guides, grid, layers, bounding boxes, canvas edges, margins; crop and selection snapping | PS-A-1701, PS-A-1702, PS-A-1703, PS-A-1705 | AF-2371, AF-2372, AF-2378 | GP-1062, GP-1063, GP-1065, GP-1066 | core | plan D03 T08 §14 |  |
| IP-0086 | Snap to equidistance, gaps, and sizes | -- | AF-2373 | GP-1064 | core | plan D03 T08 §14 |  |
| IP-0087 | Snap to paths and shape key points | -- | AF-2374 | GP-1067 | core | plan D03 T08 §14 |  |
| IP-0088 | Force pixel alignment and move by whole pixels | PS-A-1707 | AF-2369, AF-2370 | -- | core | plan D03 T08 §14 |  |
| IP-0089 | Snapping options: tolerance, presets, candidates, visible only, pixel selection bounds | -- | AF-2365, AF-2366, AF-2367, AF-2368, AF-2375, AF-2376 | -- | core | plan D03 T08 §14 |  |
| IP-0090 | Smart guide distance readout | PS-A-0054 | -- | -- | core | plan D03 T08 §14 |  |
| IP-0091 | Exclude layer from snapping | -- | AF-0934 | -- | core | plan D03 T08 §14 |  |
| IP-0092 | Snapping toggle shortcut and force pixel alignment and snap vectors and transforms to pixel grid | PS-B-1238 | AF-0030, AF-2751 | -- | core | plan D03 T08 §14 |  |
| IP-0093 | Default snapping behavior preferences | -- | -- | GP-4186 | core | plan D03 T08 §14 |  |
| IP-0094 | Protractor angle measurement (Alt-drag from ruler endpoint) | PS-A-0199 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0095 | Measure tool: distance and angle readout, modifiers, info window | PS-A-0194, PS-A-0195, PS-A-0198 | AF-0397, AF-2423 | GP-0139, GP-0140, GP-0142, GP-0143, GP-0144, GP-0145, GP-0147 | core | plan D03 T08 §5 |  |
| IP-0096 | Area measurement of objects and selections | -- | AF-2424 | GP-0141 | core | plan D03 T08 §5 |  |
| IP-0097 | Hover distance readout from selection to objects and edges | -- | AF-2425 | -- | core | plan D03 T08 §5 |  |
| IP-0098 | Measurement scale: set, presets, assign from a measured length | PS-A-0196, PS-A-1217 | AF-0398, AF-0399 | -- | core | plan D03 T08 §5 |  |
| IP-0099 | Place scale marker | PS-A-1218 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0100 | Record measurements with selectable data points | PS-A-1219, PS-A-1220, PS-A-1221, PS-A-1223 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0101 | Measurement log panel with sort, delete, export | PS-A-1222 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0102 | Note tool with author, color, clear all, show notes | PS-A-0200, PS-A-0201, PS-A-0202, PS-A-0203, PS-A-1733 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0103 | Notes panel with navigation | PS-A-0204, PS-A-0205 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0104 | Count tool with marker and label size, clear, show count | PS-A-0206, PS-A-0209, PS-A-0210, PS-A-1730 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0105 | Count groups with colors | PS-A-0207, PS-A-0208 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0106 | Automatic count from selection | PS-A-0211 | -- | -- | core | plan D03 T08 §5 |  |
| IP-0107 | Notes tool and Notes panel | PS-B-0957, PS-B-0958 | -- | -- | core | plan D03 T08 §5 | notes stored in .imago and PSD |
| IP-0108 | Color sampler readout modes per sampler (actual, proof, RGB, HSB, CMYK, Lab, total ink) | PS-A-0193 | -- | -- | core | plan D03 T08 §11 | readouts built here; the color sampler tool is D03 T11 §9 |
| IP-0109 | Info panel with readouts, coordinates units, and status toggles | PS-A-1448, PS-A-1449 | -- | -- | core | plan D03 T08 §11 |  |
| IP-0110 | Histogram panel: channels, compact and expanded views, statistics, unique color count | PS-A-1450, PS-A-1451, PS-A-1452 | -- | GP-1515, GP-0086 | core | plan D03 T08 §11 | Engine D01 T03 §4; unique colors restricted to selection |
| IP-0111 | Info panel samplers: cursor and fixed targets, color model, ink, position | -- | AF-2420, AF-2421, AF-2467, AF-2468, AF-2469, AF-2470 | -- | core | plan D03 T08 §11 | readouts built here; the color sampler tool is D03 T11 §9 |
| IP-0112 | Memory efficiency and pressure readout | -- | AF-2422, AF-2471 | -- | core | plan D03 T08 §11 |  |
| IP-0113 | Status bar readout choices: profile, scratch, efficiency, timing, tool | PS-A-1747 | -- | -- | core | plan D03 T08 §11 | extends D03 T03 §1 status strip |
| IP-0114 | Pointer dialog: position, units, bounding box, channel values, sample merged | -- | -- | GP-4022, GP-4023, GP-4024, GP-4025, GP-4026, GP-4027, GP-4028, GP-4029, GP-4030, GP-4031 | core | plan D03 T08 §11 |  |
| IP-0115 | Sample points with readouts in pixel, RGB, gray, HSV, LCh, Lab, xyY, CMYK | -- | -- | GP-1057, GP-4032, GP-4033, GP-4034, GP-4035, GP-4036, GP-4037, GP-4038, GP-4039, GP-4040, GP-4041, GP-4042, GP-4043, GP-4044 | core | plan D03 T08 §11 | readouts built here; the color sampler tool is D03 T11 §9 |
| IP-0116 | Histogram panel with channel selection | -- | AF-2408, AF-2409, AF-2455, AF-2456 | GP-3852, GP-3853, GP-3854, GP-3855, GP-3856, GP-3857, GP-3858, GP-3859, GP-3860 | core | plan D03 T08 §11 | Uses D03 T05 §2 histogram control |
| IP-0117 | Histogram for layer or selection and range restriction | -- | AF-2410, AF-2457 | GP-3866 | core | plan D03 T08 §11 |  |
| IP-0118 | Histogram statistics, unique colors, 32-bit min and max | -- | AF-2411, AF-2458 | GP-3867, GP-3868 | core | plan D03 T08 §11 |  |
| IP-0119 | Histogram display: linear, logarithmic, TRC modes, clipping warnings, detail refresh | -- | AF-2412, AF-2459 | GP-3861, GP-3862, GP-3863, GP-3864, GP-3865 | core | plan D03 T08 §11 |  |
| IP-0120 | Scope panel with gain | -- | AF-2413, AF-2419, AF-2460, AF-2466 | -- | core | plan D03 T08 §11 |  |
| IP-0121 | Scopes: intensity waveform, RGB waveform, RGB parade | -- | AF-2414, AF-2415, AF-2416, AF-2461, AF-2462, AF-2463 | -- | core | plan D03 T08 §11 |  |
| IP-0122 | Vectorscope with skin tone line | -- | AF-2418, AF-2465 | -- | core | plan D03 T08 §11 |  |
| IP-0123 | Power spectral density scope | -- | AF-2417, AF-2464 | -- | core | plan D03 T08 §11 |  |
| IP-0124 | Status bar and title format: document sizes, profile, dimensions, scratch, efficiency, timing, custom title and status format | PS-B-1370 | -- | GP-4187 | core | plan D03 T08 §11 | extends D03 T03 §1 |
| IP-0125 | Histogram, Info, and Measurement Log panels | PS-B-1346, PS-B-1348, PS-B-1351 | -- | -- | core | plan D03 T08 §11 |  |
| IP-0126 | Rulers display toggle | PS-A-1676, PS-A-1741 | AF-2383 | GP-1056 | core | shipped-scope D03 T01 §2 |  |
| IP-0127 | Hand tool with Space temporary access | PS-A-0480 | AF-0377, AF-2401 | -- | core | shipped-scope D03 T03 §4 |  |
| IP-0128 | Zoom tool: click, Alt or Ctrl reverse, drag rectangle | PS-A-0490 | AF-0378, AF-2396 | GP-0220, GP-0222, GP-0225 | core | shipped-scope D03 T03 §4 |  |

## History, clipboard, and the Image menu

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0129 | Toggle last state | PS-A-1226 | -- | -- | core | plan D03 T08 §6 |  |
| IP-0130 | History slider to scrub states | -- | AF-2436 | -- | core | plan D03 T08 §6 |  |
| IP-0131 | History advanced view with thumbnails and timestamps | -- | AF-2430, AF-2439 | -- | core | plan D03 T08 §6 |  |
| IP-0132 | Delete history state and clear history | PS-A-1499, PS-A-1511 | -- | GP-4132 | core | plan D03 T08 §6 |  |
| IP-0133 | Snapshots: create, name, scope, restore, delete, saved with document | PS-A-1500, PS-A-1502 | AF-2432, AF-2433, AF-2441, AF-2442, AF-2443, AF-2444 | -- | core | plan D03 T08 §6 |  |
| IP-0134 | New document from history state or snapshot | PS-A-1501 | AF-2434, AF-2445 | -- | core | plan D03 T08 §6 |  |
| IP-0135 | History options: auto snapshots, snapshot dialog, undoable visibility | PS-A-1503, PS-A-1504, PS-A-1506, PS-A-1507 | -- | -- | core | plan D03 T08 §6 |  |
| IP-0136 | Non-linear history and redo branches | PS-A-1505 | AF-2428, AF-2438 | -- | core | plan D03 T08 §6 |  |
| IP-0137 | History log to metadata or text file | PS-A-1509 | -- | -- | core | plan D03 T08 §6 |  |
| IP-0138 | Save history with document | -- | AF-2354, AF-2440 | -- | core | plan D03 T08 §6 |  |
| IP-0139 | Save history with document | -- | AF-2596 | -- | format | plan D03 T08 §6 | history stored in .imago |
| IP-0140 | New layer from history snapshot | -- | AF-0935 | -- | core | plan D03 T08 §6 |  |
| IP-0141 | History log to metadata or text file with sessions, concise, or detailed items | PS-B-1241, PS-B-1242 | -- | -- | core | plan D03 T08 §6 |  |
| IP-0142 | Canvas size relative and extension color | PS-A-1187, PS-A-1189 | -- | -- | core | plan D03 T08 §7 | extends D03 T03 §7 |
| IP-0143 | Canvas size offset X and Y and resize layers option | -- | -- | GP-1129, GP-1130, GP-1131 | core | plan D03 T08 §7 | extends D03 T03 §7 |
| IP-0144 | Arbitrary canvas rotation | PS-A-1193 | -- | GP-1270 | core | plan D03 T08 §7 | Engine D01 T03 §2 |
| IP-0145 | Crop to selection | PS-A-1196 | -- | GP-1087, GP-1088 | core | plan D03 T08 §7 |  |
| IP-0146 | Trim and crop to content by transparency or corner color | PS-A-1197, PS-A-1198 | -- | GP-1089 | core | plan D03 T08 §7 |  |
| IP-0147 | Zealous crop | -- | -- | GP-1258 | core | plan D03 T08 §7 |  |
| IP-0148 | Reveal all and fit canvas to layers | PS-A-1199 | AF-2341 | GP-1124 | core | plan D03 T08 §7 |  |
| IP-0149 | Fit canvas to selection | -- | -- | GP-1125 | core | plan D03 T08 §7 |  |
| IP-0150 | Clip canvas to discard content outside the canvas | -- | AF-2340 | -- | core | plan D03 T08 §7 |  |
| IP-0151 | Slice image using guides | -- | -- | GP-1146 | core | plan D03 T08 §7 |  |
| IP-0152 | Image size: constrain proportions and units (percent, points, picas, columns) | PS-A-1169, PS-A-1170 | AF-2330, AF-2331 | -- | core | plan D03 T08 §7 | extends D03 T03 §7 |
| IP-0153 | Image size: resample off for print size, separate X and Y resolution | PS-A-1172 | AF-2329 | GP-1138, GP-1139 | core | plan D03 T08 §7 | extends D03 T03 §7 |
| IP-0154 | Resample method extensions: automatic, bicubic smoother and sharper, Lanczos variants, NoHalo, LoHalo | PS-A-1173, PS-A-1176, PS-A-1177 | AF-2335, AF-2336 | GP-1140 | core | plan D03 T08 §7 | Engine D01 T03 §2 |
| IP-0155 | Preserve Details enlargement with reduce noise | PS-A-1174, PS-A-1181 | -- | -- | core | plan D03 T08 §7 | Classical detail-preserving upscale, engine D01 T03 §2 |
| IP-0156 | Image size preview and Fit To presets | PS-A-1167, PS-A-1168 | -- | -- | core | plan D03 T08 §7 |  |
| IP-0157 | Auto resolution from screen frequency | PS-A-1183 | -- | -- | print | plan D03 T08 §7 |  |
| IP-0158 | Scale styles with image size | PS-A-1182 | -- | -- | core | plan D03 T08 §7 | Layer effects from D03 T09 §7 |
| IP-0159 | Print size dialog: width, height, and X and Y resolution | -- | -- | GP-1100, GP-1101, GP-1102, GP-1103, GP-1104 | print | plan D03 T08 §7 | Changes resolution only, no resampling |
| IP-0160 | Crop to selection | -- | AF-0756 | -- | core | plan D03 T08 §7 |  |
| IP-0161 | Resize pixel art document: XBR and HQX | -- | AF-0772, AF-0773, AF-0774 | -- | core | plan D03 T08 §7 |  |
| IP-0162 | Fit Image with don't enlarge | PS-B-0725, PS-B-0726 | -- | -- | automation | plan D03 T08 §7 |  |
| IP-0163 | Preserve Details 2.0 upscale preview | PS-B-1308 | -- | -- | core | plan D03 T08 §7 |  |
| IP-0164 | Cut, copy, copy merged, and paste | PS-A-1228 | -- | GP-0880, GP-0881, GP-0882, GP-0904 | core | plan D03 T08 §8 |  |
| IP-0165 | Paste in place, paste into, paste outside, paste without formatting | PS-A-1229 | -- | GP-0895, GP-0896, GP-0903 | core | plan D03 T08 §8 |  |
| IP-0166 | Paste as new layer, optionally in place | -- | -- | GP-0889, GP-0890, GP-0891 | core | plan D03 T08 §8 |  |
| IP-0167 | Paste as floating data, optionally in place | -- | -- | GP-0893, GP-0894 | core | plan D03 T08 §8 | Floating selection model D03 T10 §1 |
| IP-0168 | Clear selection contents | PS-A-1230 | -- | GP-0879 | core | plan D03 T08 §8 |  |
| IP-0169 | Named buffers: cut, copy, copy visible named | -- | -- | GP-3667, GP-3668, GP-3669, GP-3776, GP-3777, GP-3778, GP-3779 | core | plan D03 T08 §8 |  |
| IP-0170 | Buffers panel: paste buffer variants, as new layer or image, delete | -- | -- | GP-3664, GP-3665, GP-3666, GP-3670, GP-3671, GP-3672, GP-3673, GP-3674, GP-3675, GP-3676, GP-3677, GP-3678, GP-3780 | core | plan D03 T08 §8 |  |
| IP-0171 | Purge clipboard, histories, and all | PS-A-1252 | -- | -- | core | plan D03 T08 §8 | Video cache purge follows B-043 |
| IP-0172 | Copy merged | -- | AF-0894 | -- | core | plan D03 T08 §8 |  |
| IP-0173 | Paste as new layer and paste inside | -- | AF-0956, AF-0957 | GP-0028 | core | plan D03 T08 §8 |  |
| IP-0174 | Paste special by clipboard format | -- | AF-0960 | -- | core | plan D03 T08 §8 |  |
| IP-0175 | Cut across a layer group | -- | -- | GP-0095 | core | plan D03 T08 §8 |  |
| IP-0176 | Cut, copy, and clear selected pixels | PS-A-0534, PS-A-0536, PS-A-0537 | -- | -- | core | plan D03 T08 §8 |  |
| IP-0177 | Copy merged | PS-A-0535 | -- | -- | core | plan D03 T08 §8 |  |
| IP-0178 | Paste in place, paste into, paste outside | PS-A-0539, PS-A-0540, PS-A-0541 | -- | -- | core | plan D03 T08 §8 |  |
| IP-0179 | Paste without formatting | PS-A-0542 | -- | -- | core | plan D03 T08 §8 | Text paste; type engine D03 T16 §1 |
| IP-0180 | Prefer metafile when pasting from other apps | -- | AF-2655 | -- | core | plan D03 T08 §8 |  |
| IP-0181 | Crop presets: ratio, W x H x resolution, fixed aspect or size, save and delete presets | PS-A-0133, PS-A-0134, PS-A-0135 | -- | GP-0656 | core | plan D03 T08 §9 | extends D03 T03 §7 |
| IP-0182 | Swap and clear crop ratio | PS-A-0136, PS-A-0137 | -- | -- | core | plan D03 T08 §9 |  |
| IP-0183 | Numeric crop position and size | -- | -- | GP-0657, GP-0658 | core | plan D03 T08 §9 |  |
| IP-0184 | Crop options: expand from center, selected layers only | -- | -- | GP-0652, GP-0655 | core | plan D03 T08 §9 |  |
| IP-0185 | Straighten from a drawn line (crop tool and measure tool) | PS-A-0138, PS-A-0197 | -- | GP-0146, GP-0148 | core | plan D03 T08 §9 | Engine D01 T03 §2 |
| IP-0186 | Crop overlays: grid, diagonal, triangle, golden ratio, golden spiral | PS-A-0140, PS-A-0141, PS-A-0142, PS-A-0143, PS-A-0144 | -- | GP-0660 | core | plan D03 T08 §9 | extends D03 T03 §7 thirds |
| IP-0187 | Crop overlay display mode and cycling | PS-A-0145, PS-A-0146 | -- | -- | core | plan D03 T08 §9 |  |
| IP-0188 | Crop classic mode, crop preview, auto center | PS-A-0147, PS-A-0148, PS-A-0149 | -- | -- | core | plan D03 T08 §9 |  |
| IP-0189 | Crop shield color, opacity, and auto adjust | PS-A-0150, PS-A-0151, PS-A-0152 | -- | GP-0659 | core | plan D03 T08 §9 |  |
| IP-0190 | Crop rotate by dragging outside the box | PS-A-0157 | -- | -- | core | plan D03 T08 §9 |  |
| IP-0191 | Crop beyond the canvas to expand it | PS-A-0156 | -- | GP-0654 | core | plan D03 T08 §9 |  |
| IP-0192 | Content-aware crop fill | PS-A-0154 | -- | -- | core | plan D03 T08 §9 | Classical PatchMatch via D03 T13 §3 |
| IP-0193 | Crop auto shrink to content, optionally merged | -- | -- | GP-0661, GP-0662 | core | plan D03 T08 §9 |  |
| IP-0194 | Perspective crop tool with size, front image, grid | PS-A-0159, PS-A-0160, PS-A-0161, PS-A-0162 | -- | -- | core | plan D03 T08 §9 |  |
| IP-0195 | Crop presets and modes: unconstrained, original ratio, custom ratio, resample, dimensions, units, DPI, saved presets | -- | AF-0736, AF-0737, AF-0738, AF-0739, AF-0740, AF-0741, AF-0742, AF-0743, AF-0744, AF-0757 | -- | core | plan D03 T08 §9 | extends D03 T03 §7 |
| IP-0196 | Crop straighten and rotate crop area | -- | AF-0745, AF-0746, AF-0755 | -- | core | plan D03 T08 §9 | extends D03 T03 §7 |
| IP-0197 | Crop overlays, darken border, reveal canvas | -- | AF-0747, AF-0749, AF-0750 | -- | core | plan D03 T08 §9 | extends D03 T03 §7 |
| IP-0198 | Crop modifiers: constrain, nudge, snapping override, recompose around center | -- | AF-0751, AF-0752, AF-0753, AF-0754 | -- | core | plan D03 T08 §9 |  |
| IP-0199 | Crop canvas extension filled by inpainting | -- | AF-0758 | -- | core | plan D03 T08 §9 | Classical fill via D03 T13 §3; generative expand is D03 T19 §4 |
| IP-0200 | Crop overlay cycling shortcut | -- | AF-2750 | -- | core | plan D03 T08 §9 |  |
| IP-0201 | Undo, redo, and step backward and forward | PS-A-1224, PS-A-1225, PS-A-1512 | AF-2426 | GP-0875, GP-0876, GP-0878, GP-0906, GP-0908, GP-4130, GP-4131 | core | shipped-scope D03 T03 §2 |  |
| IP-0202 | History panel listing states, click to revert | PS-A-1497, PS-A-1498 | AF-2427, AF-2435 | GP-0907, GP-4129 | core | shipped-scope D03 T03 §2 |  |
| IP-0203 | History limit setting | PS-A-1508 | AF-2431 | -- | core | shipped-scope D03 T03 §2 |  |
| IP-0204 | History panel | PS-B-1347 | -- | -- | core | shipped-scope D03 T03 §2 |  |
| IP-0205 | History states and undo level limits | PS-B-1244 | AF-2675 | GP-4256 | core | shipped-scope D03 T03 §2 |  |
| IP-0206 | Free Transform command | PS-A-1242 | -- | -- | core | shipped-scope D03 T03 §7 |  |
| IP-0207 | Image size: pixel dimensions and resolution | PS-A-1166, PS-A-1171 | AF-2328 | GP-1134, GP-1135, GP-1136, GP-1137 | core | shipped-scope D03 T03 §7 |  |
| IP-0208 | Resample methods: nearest neighbor, bilinear, bicubic, Lanczos | PS-A-1178, PS-A-1179, PS-A-1180 | AF-2332, AF-2333, AF-2334 | -- | core | shipped-scope D03 T03 §7 |  |
| IP-0209 | Canvas size with anchor and center | PS-A-1186, PS-A-1188 | AF-2338, AF-2339 | GP-1126, GP-1127, GP-1128, GP-1132 | core | shipped-scope D03 T03 §7 |  |
| IP-0210 | Rotate canvas 90 and 180 degrees | PS-A-1190, PS-A-1191, PS-A-1192 | AF-2343 | GP-1133, GP-1141, GP-1268, GP-1269 | core | shipped-scope D03 T03 §7 |  |
| IP-0211 | Flip canvas horizontally and vertically | PS-A-1194, PS-A-1195 | AF-2342 | GP-1092, GP-1267 | core | shipped-scope D03 T03 §7 |  |
| IP-0212 | Crop tool with commit and cancel | PS-A-0132, PS-A-0158 | -- | GP-0651 | core | shipped-scope D03 T03 §7 |  |
| IP-0213 | Delete or hide cropped pixels | PS-A-0153 | -- | GP-0653 | core | shipped-scope D03 T03 §7 |  |
| IP-0214 | Crop overlay rule of thirds | PS-A-0139 | -- | -- | core | shipped-scope D03 T03 §7 |  |
| IP-0215 | Flip and rotate canvas 90 degrees | -- | AF-0768, AF-0769, AF-0770, AF-0771 | -- | core | shipped-scope D03 T03 §7 |  |
| IP-0216 | Crop tool apply, cancel, reset | -- | AF-0733, AF-0734, AF-0735, AF-0748 | -- | core | shipped-scope D03 T03 §7 |  |

## Layers and the Layers panel

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0217 | Layer kinds: pixel, group, fill, adjustment, text, shape, smart object, container, link, vector | -- | AF-0807, AF-0817 | GP-1430 | core | plan D03 T09 §1 | extends D03 T03 §3 |
| IP-0218 | Symbol layers with propagating instances | -- | AF-0849 | -- | core | plan D03 T09 §1 | (Affinity) symbol instances share edits |
| IP-0219 | Layer properties and layer colors | PS-A-0650, PS-A-0795 | AF-0933 | -- | core | plan D03 T09 §1 |  |
| IP-0220 | Lock modes: transparency, pixels, position, visibility, all, artboard nesting, lock in groups | PS-A-0674, PS-A-0765, PS-A-0766, PS-A-0767, PS-A-0768, PS-A-0769, PS-A-0770 | AF-0787, AF-0788, AF-0789 | GP-0018, GP-3707, GP-3708, GP-3709, GP-3710, GP-3711 | core | plan D03 T09 §1 | extends D03 T03 §3 |
| IP-0221 | Layer color labels and tags with select same tag | PS-A-0781 | AF-0921, AF-0922, AF-0923 | GP-3747 | core | plan D03 T09 §1 |  |
| IP-0222 | Layers panel filtering and search: kind, name, effect, mode, attribute, color, smart object, artboard, saved searches | PS-A-0734, PS-A-0771, PS-A-0772, PS-A-0773, PS-A-0774, PS-A-0775, PS-A-0776, PS-A-0777, PS-A-0779, PS-A-0780, PS-A-0794 | -- | GP-0019, GP-1341, GP-3703, GP-3704 | core | plan D03 T09 §1 |  |
| IP-0223 | Isolate layers (solo) and isolated group editing | PS-A-0778 | AF-0919, AF-0920, AF-0930 | -- | core | plan D03 T09 §1 |  |
| IP-0224 | Edit all layers mode | -- | AF-0800 | -- | core | plan D03 T09 §1 | (Affinity) editing and Select All across layers |
| IP-0225 | Solid color fill layer | PS-A-0653, PS-A-0686 | AF-0835 | -- | core | plan D03 T09 §1 |  |
| IP-0226 | Isolate layers | PS-A-0507 | -- | -- | core | plan D03 T09 §1 |  |
| IP-0227 | Layer search pattern syntax with regular expressions | -- | AF-0057 | GP-4237, GP-4238 | core | plan D03 T09 §1 | also used by text find and replace, D03 T16 §4 |
| IP-0228 | New layer dialog: name, color, mode, opacity, size, offset, fill, switches, neutral fill, ask for name | PS-A-0625, PS-A-0626, PS-A-0628 | AF-0816 | GP-1370, GP-1371, GP-1372, GP-1373, GP-1377, GP-1378, GP-1379, GP-1380, GP-1381, GP-1382, GP-1383, GP-3748 | core | plan D03 T09 §2 | extends D03 T03 §3 |
| IP-0229 | Visibility solo, hide or show others, show all, drag across eyes | PS-A-0763, PS-A-0764 | AF-0797, AF-0798, AF-0799 | -- | core | plan D03 T09 §2 | extends D03 T03 §3 |
| IP-0230 | Nested groups: expand and collapse all, group visibility, opacity, and masks, drop out of parent | PS-A-0796 | AF-0791, AF-0792, AF-0793, AF-0886 | GP-1332, GP-1337, GP-1338, GP-1339, GP-1340 | core | plan D03 T09 §2 |  |
| IP-0231 | Arrange order: bring to front, forward, backward, to back, reverse | PS-A-0670, PS-A-0800 | AF-0890 | GP-1343, GP-1344, GP-1394, GP-1395, GP-1422, GP-1439, GP-3729, GP-3730 | core | plan D03 T09 §2 |  |
| IP-0232 | Layer insertion target: inside, behind, top, sticky | -- | AF-0881, AF-0887, AF-0888, AF-0889 | -- | core | plan D03 T09 §2 | (Affinity) insertion behaviors |
| IP-0233 | Layer selection: multi-select, next, previous, top, bottom, parent, all | PS-A-0799, PS-A-0801 | AF-0926, AF-0927 | GP-1322, GP-1384, GP-1393, GP-1427, GP-3702 | core | plan D03 T09 §2 |  |
| IP-0234 | Select similar layers and same name | PS-A-0802 | AF-0925 | -- | core | plan D03 T09 §2 |  |
| IP-0235 | Find layer in the Layers panel from canvas | -- | AF-0814 | -- | core | plan D03 T09 §2 |  |
| IP-0236 | Opacity number-key shortcuts | -- | AF-0783 | -- | core | plan D03 T09 §2 |  |
| IP-0237 | Link layers and select linked layers | PS-A-0675, PS-A-0676, PS-A-0782 | -- | -- | core | plan D03 T09 §2 |  |
| IP-0238 | Linked duplicates with Links panel | -- | AF-0905, AF-0906, AF-0907, AF-0908, AF-0909, AF-0910, AF-2498 | -- | core | plan D03 T09 §2 | (Affinity) duplicate linked, relink, navigate link set |
| IP-0239 | Linkable attributes: transform, pixels, blending, opacity, effects, adjustment and filter parameters, shape style | -- | AF-0911, AF-0912, AF-0913, AF-0914, AF-0915, AF-0916, AF-0917, AF-0918 | -- | core | plan D03 T09 §2 | (Affinity) |
| IP-0240 | Layers panel options: thumbnail size, contents, background, type icons, group thumbnails, auto-scroll, default masks, copy suffix | PS-A-0788, PS-A-0789, PS-A-0790, PS-A-0791, PS-A-0792, PS-A-0793 | AF-0794, AF-0795, AF-0809, AF-0810, AF-0811, AF-0812, AF-0813 | GP-1342 | core | plan D03 T09 §2 |  |
| IP-0241 | Layers panel context menu and full Layer menu | -- | -- | GP-1365, GP-3700, GP-3735 | core | plan D03 T09 §2 |  |
| IP-0242 | Layer attributes dialog | -- | -- | GP-3739, GP-3740 | core | plan D03 T09 §2 |  |
| IP-0243 | Multi-select layers, channels, and paths | -- | -- | GP-0017 | core | plan D03 T09 §2 |  |
| IP-0244 | Context-sensitive delete for layer or mask | -- | -- | GP-0075 | core | plan D03 T09 §2 |  |
| IP-0245 | Insert target: new layers go behind, at top, or inside the selection | -- | AF-0031 | -- | core | plan D03 T09 §2 |  |
| IP-0246 | Ask for a name when creating layers and groups | -- | AF-2699 | -- | core | plan D03 T09 §2 |  |
| IP-0247 | Linked layer attributes: transform, pixels, blend, opacity, effects, adjustment, filter, shape | -- | AF-2499 | -- | core | plan D03 T09 §2 |  |
| IP-0248 | Merge visible layers with options | -- | -- | GP-1095, GP-1096, GP-1097, GP-1098 | core | plan D03 T09 §14 |  |
| IP-0249 | Background layer and conversions to and from a normal layer | PS-A-0629, PS-A-0630, PS-A-0683 | AF-0790 | -- | core | plan D03 T09 §14 |  |
| IP-0250 | Add and remove alpha channel | -- | -- | GP-1313, GP-1314, GP-1429, GP-3766, GP-3767 | core | plan D03 T09 §14 |  |
| IP-0251 | Layer via copy and layer via cut | PS-A-0638, PS-A-0639 | AF-0902, AF-0904 | -- | core | plan D03 T09 §14 |  |
| IP-0252 | Duplicate layer to another or new document | PS-A-0643, PS-A-0806 | -- | -- | core | plan D03 T09 §14 | extends D03 T03 §3 |
| IP-0253 | Delete hidden and empty layers | PS-A-0645, PS-A-0646 | -- | -- | core | plan D03 T09 §14 |  |
| IP-0254 | Merge selected, merge visible, and merge layer groups | PS-A-0678 | AF-0892 | GP-1367, GP-3769 | core | plan D03 T09 §14 | extends D03 T03 §3 |
| IP-0255 | Stamp visible and stamp selected (new from visible) | PS-A-0679, PS-A-0680 | AF-0893 | GP-1368, GP-3754 | core | plan D03 T09 §14 |  |
| IP-0256 | Rasterize layers: type, shape, fill, smart object, styles, trim, automatic | PS-A-0665 | AF-0896, AF-0897, AF-0899, AF-0900 | GP-0051, GP-1425, GP-3755 | core | plan D03 T09 §14 |  |
| IP-0257 | Rasterize to mask | -- | AF-0898 | -- | core | plan D03 T09 §14 | (Affinity) |
| IP-0258 | Revert rasterize to the non-destructive layer | -- | -- | GP-0052 | core | plan D03 T09 §14 | (GIMP 3.2) text, link, and vector layers |
| IP-0259 | Matting: color decontaminate, defringe, remove black and white matte | PS-A-0682 | -- | -- | core | plan D03 T09 §14 |  |
| IP-0260 | Layers to image size, resize to selection, crop layers to content | -- | -- | GP-1324, GP-1396, GP-1397, GP-3757 | core | plan D03 T09 §14 |  |
| IP-0261 | Layer boundary size dialog | -- | -- | GP-1398, GP-1399, GP-1400, GP-1401, GP-1402, GP-1403, GP-1404, GP-1405, GP-1406, GP-1407, GP-1408, GP-1409, GP-1410, GP-1411, GP-3756 | core | plan D03 T09 §14 |  |
| IP-0262 | Duplicate selection to a new layer (layer via copy) | -- | AF-0536 | -- | core | plan D03 T09 §14 |  |
| IP-0263 | Delete all empty layers | PS-B-0761 | -- | -- | automation | plan D03 T09 §14 |  |
| IP-0264 | Flatten image | -- | -- | GP-1091 | core | shipped-scope D03 T03 §3 |  |
| IP-0265 | Layers panel with thumbnails, blend mode, and opacity | PS-A-0759, PS-A-0760, PS-A-0761 | AF-0781, AF-0782, AF-0784 | GP-3699, GP-3705, GP-3721, GP-3723, GP-3724, GP-3725 | core | shipped-scope D03 T03 §3 |  |
| IP-0266 | Pixel layer | PS-A-0684 | AF-0818 | -- | core | shipped-scope D03 T03 §3 |  |
| IP-0267 | New layer command and panel button | PS-A-0786 | AF-0806 | GP-3726, GP-3727 | core | shipped-scope D03 T03 §3 | Alt-click opens the dialog, D03 T09 §2 |
| IP-0268 | Duplicate layer | PS-A-0642 | AF-0901 | GP-1326, GP-3731, GP-3750 | core | shipped-scope D03 T03 §3 |  |
| IP-0269 | Delete layer | PS-A-0644, PS-A-0787 | AF-0808 | GP-1325, GP-3734, GP-3753 | core | shipped-scope D03 T03 §3 |  |
| IP-0270 | Rename layer inline with Tab to next layer | PS-A-0649, PS-A-0797 | AF-0815 | GP-3722 | core | shipped-scope D03 T03 §3 | Tab and Shift+Tab sequential rename added in D03 T09 §2 |
| IP-0271 | Reorder layers by drag | PS-A-0798 | AF-0885 | GP-3736 | core | shipped-scope D03 T03 §3 |  |
| IP-0272 | Hide and show layers | PS-A-0669 | -- | GP-3706 | core | shipped-scope D03 T03 §3 |  |
| IP-0273 | Layer groups: create, ungroup, add, move, delete | PS-A-0631, PS-A-0632, PS-A-0667, PS-A-0668, PS-A-0695, PS-A-0785 | AF-0367, AF-0805, AF-0843, AF-0845, AF-0846, AF-0847 | GP-1329, GP-1330, GP-1331, GP-1333, GP-1334, GP-1336, GP-1369, GP-3728, GP-3749 | core | shipped-scope D03 T03 §3 |  |
| IP-0274 | Merge down | PS-A-0677 | AF-0891 | GP-1366, GP-3751 | core | shipped-scope D03 T03 §3 |  |
| IP-0275 | Flatten image | PS-A-0681 | AF-0895 | GP-3770 | core | shipped-scope D03 T03 §3 |  |
| IP-0276 | Layers panel | PS-B-1350 | -- | -- | core | shipped-scope D03 T03 §3 |  |
| IP-0277 | Move tool | PS-A-0033 | AF-0361 | -- | core | shipped-scope D03 T03 §4 | Affinity rotate, shear handles in D03 T13 §5 |

## Masks, clipping, and blending

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0278 | Live mask layers: framework, create menu, transfer to any layer, re-edit | -- | AF-1299, AF-1300, AF-1301, AF-1302, AF-1303 | -- | core | plan D03 T09 §3 | Affinity live masks; update with the image |
| IP-0279 | Live hue range mask: hue wheel nodes, ramps, picker, blur, invert, presets | -- | AF-1304, AF-1305, AF-1306, AF-1307, AF-1308, AF-1309, AF-1310, AF-1311, AF-1312, AF-1313, AF-1314, AF-1315, AF-1316 | -- | core | plan D03 T09 §3 |  |
| IP-0280 | Live luminosity range mask: luminosity graph, linear, blur, invert, presets | -- | AF-1317, AF-1318, AF-1319, AF-1320, AF-1321, AF-1322, AF-1323, AF-1324, AF-1325, AF-1326 | -- | core | plan D03 T09 §3 | Luminosity masks |
| IP-0281 | Live band-pass mask: low and high band, intensity graph, blur, invert | -- | AF-1327, AF-1328, AF-1329, AF-1330, AF-1331, AF-1332, AF-1333, AF-1334, AF-1335, AF-1336, AF-1337, AF-1338 | -- | core | plan D03 T09 §3 |  |
| IP-0282 | Add layer mask: reveal all, hide all, from selection, transparency, channel, grayscale copy, invert | PS-A-0656, PS-A-0737, PS-A-0738 | AF-0801, AF-0854, AF-0868 | GP-1345, GP-1346, GP-1347, GP-1348, GP-1349, GP-1350, GP-1351, GP-1352, GP-1353, GP-1354, GP-3733, GP-3759 | core | plan D03 T09 §3 | extends D03 T04 §5 mask model |
| IP-0283 | Mask commands: apply, delete, disable, edit mask target | PS-A-0657, PS-A-0741, PS-A-0753 | AF-0857 | GP-1355, GP-1356, GP-1357, GP-1358, GP-1359, GP-3701, GP-3760, GP-3761, GP-3763, GP-3764, GP-3771 | core | plan D03 T09 §3 |  |
| IP-0284 | Mask link and move or copy mask by drag | PS-A-0740, PS-A-0745 | -- | -- | core | plan D03 T09 §3 |  |
| IP-0285 | Mask invert, clear, fill, and release to layer | PS-A-0752 | AF-0860, AF-0861, AF-0862 | -- | core | plan D03 T09 §3 |  |
| IP-0286 | View mask alone and mask overlay with color options | PS-A-0742, PS-A-0743, PS-A-0744, PS-A-0747 | AF-0858 | GP-1364, GP-3762 | core | plan D03 T09 §3 |  |
| IP-0287 | Mask density and feather | PS-A-0748, PS-A-0749 | -- | -- | core | plan D03 T09 §3 |  |
| IP-0288 | Mask to selection: replace, add, subtract, intersect | PS-A-0746 | -- | GP-1360, GP-1361, GP-1362, GP-1363, GP-3765 | core | plan D03 T09 §3 |  |
| IP-0289 | Paint masks with brushes, erasers, and gradients | -- | AF-0139, AF-0170, AF-0829, AF-0855, AF-0856 | -- | core | plan D03 T09 §3 | Color panel switches to grayscale while a mask is targeted |
| IP-0290 | Mask tool: auto-created mask with paint and editable gradient modes | -- | AF-0345, AF-0346, AF-0347, AF-0350, AF-0351 | -- | core | plan D03 T09 §3 | (Affinity 3.3) edge refinement via D03 T10 §7 |
| IP-0291 | Mask layers: opacity, blend mode, parent masks, drag layer to mask | -- | AF-0826, AF-0863, AF-0864, AF-0865, AF-0866, AF-0996 | -- | core | plan D03 T09 §3 | (Affinity) any layer type can take a blend mode |
| IP-0292 | Compound masks with add, subtract, intersect, and xor | -- | AF-0850, AF-0851, AF-0852, AF-0853 | -- | core | plan D03 T09 §3 | (Affinity) |
| IP-0293 | Luminosity masks from layer intensity | -- | AF-0870 | -- | core | plan D03 T09 §3 |  |
| IP-0294 | Live masks: hue range, luminosity range, band pass | -- | AF-0872, AF-0873, AF-0874, AF-0875, AF-0876 | -- | core | plan D03 T09 §3 | (Affinity) invertible and paintable |
| IP-0295 | Edit mask immediately option when adding a layer mask | -- | -- | GP-0074 | core | plan D03 T09 §3 |  |
| IP-0296 | Deleting a selection on image layers masks instead of rasterizing | -- | AF-0535 | -- | core | plan D03 T09 §3 |  |
| IP-0297 | Masks properties page: density, feather, refine | PS-A-1526 | -- | -- | core | plan D03 T09 §3 |  |
| IP-0298 | Flatten all masks | PS-B-0763 | -- | -- | automation | plan D03 T09 §3 |  |
| IP-0299 | Clipping masks: create, release, multiple clipped layers, new layer clipped to previous | PS-A-0627, PS-A-0660, PS-A-0661, PS-A-0756, PS-A-0757 | AF-0867 | -- | core | plan D03 T09 §4 |  |
| IP-0300 | Vector masks: add, from path or pen shape, from selection, delete, disable, link, switch with pixel mask | PS-A-0658, PS-A-0659, PS-A-0739, PS-A-0754, PS-A-0755 | AF-0417, AF-0869, AF-0877, AF-0878 | -- | core | plan D03 T09 §4 |  |
| IP-0301 | Child clipping: move inside and outside, auto-clip brush strokes, isolated child blending, select clipped object | -- | AF-0879, AF-0880, AF-0882, AF-0883, AF-0995 | -- | core | plan D03 T09 §4 | (Affinity) child clipping semantics |
| IP-0302 | Vector mask from path | PS-A-0416, PS-A-1491 | -- | -- | core | plan D03 T09 §4 | Path from D03 T16 §5 |
| IP-0303 | Fill text with an image by clipping | PS-A-1630 | -- | -- | core | plan D03 T09 §4 |  |
| IP-0304 | Adjustment blend options and tonal targeting by blend ranges | -- | AF-1117, AF-1122 | -- | core | plan D03 T09 §5 | Blend If and Affinity blend ranges on adjustment layers |
| IP-0305 | Live tone blend group: strength, color, contrast, low pass, content type | -- | AF-1339, AF-1340, AF-1341, AF-1342, AF-1343, AF-1344, AF-1345 | -- | core | plan D03 T09 §5 | auto tone-matching group has no named home; blending section closest |
| IP-0306 | Blending options dialog: general mode and opacity | PS-A-0808 | -- | -- | core | plan D03 T09 §5 | extends D03 T03 §3 |
| IP-0307 | Fill opacity with special eight modes behavior | PS-A-0762, PS-A-0809, PS-A-0852 | AF-1008, AF-1025 | -- | core | plan D03 T09 §5 |  |
| IP-0308 | Blending channel restrictions | PS-A-0810 | -- | -- | core | plan D03 T09 §5 |  |
| IP-0309 | Knockout none, shallow, deep | PS-A-0811 | -- | -- | core | plan D03 T09 §5 |  |
| IP-0310 | Blend interior effects and clipped layers as group | PS-A-0812, PS-A-0813 | -- | -- | core | plan D03 T09 §5 |  |
| IP-0311 | Transparency shapes layer and mask hides effects | PS-A-0814, PS-A-0815, PS-A-0816 | -- | -- | core | plan D03 T09 §5 |  |
| IP-0312 | Blend If with this layer and underlying layer split sliders | PS-A-0817, PS-A-0818, PS-A-0819, PS-A-0820 | -- | -- | core | plan D03 T09 §5 |  |
| IP-0313 | Blend ranges: source and underlying curves per channel | -- | AF-0786, AF-0997, AF-0998, AF-0999, AF-1000, AF-1001, AF-1002 | -- | core | plan D03 T09 §5 | (Affinity) |
| IP-0314 | Blend gamma per layer and text default | -- | AF-1003, AF-1004 | -- | core | plan D03 T09 §5 | (Affinity) |
| IP-0315 | Per-layer antialiasing and coverage map | -- | AF-1005, AF-1006, AF-1007 | -- | core | plan D03 T09 §5 | (Affinity) |
| IP-0316 | Composite mode, composite space, and blend space | -- | -- | GP-1374, GP-1375, GP-1376, GP-3744, GP-3745, GP-3746 | core | plan D03 T09 §5 | (GIMP) |
| IP-0317 | Per-channel blend ranges | -- | AF-1095 | -- | core | plan D03 T09 §5 |  |
| IP-0318 | Porter-Duff compositing ops: clear, src, dst, in, out, atop, over, xor | -- | -- | GP-3510, GP-3515, GP-3516, GP-3517, GP-3518, GP-3519, GP-3526, GP-3527, GP-3528, GP-3529, GP-3530, GP-3531 | core | plan D03 T09 §6 |  |
| IP-0319 | SVG compositing ops soft-light, hard-light, lighten | -- | -- | GP-3473, GP-3521, GP-3522 | core | plan D03 T09 §6 | GEGL svg ops, misrouted by name |
| IP-0320 | Pass-through group blend mode | PS-A-0696 | AF-0844 | -- | core | plan D03 T09 §6 |  |
| IP-0321 | Erase-type modes: behind, clear, erase, color erase, merge, split | PS-A-0823, PS-A-0824 | AF-0994 | GP-1465, GP-1466, GP-1467, GP-1468 | core | plan D03 T09 §6 |  |
| IP-0322 | Grain extract and grain merge modes | -- | -- | GP-1492, GP-1493 | core | plan D03 T09 §6 | (GIMP) |
| IP-0323 | LCh and HSV value component modes | -- | -- | GP-1487, GP-1495, GP-1496, GP-1497, GP-1498, GP-1499 | core | plan D03 T09 §6 | (GIMP) LCh hue, chroma, color, lightness, HSV value |
| IP-0324 | Luminance and luma darken or lighten only modes | -- | -- | GP-1479, GP-1500, GP-1503 | core | plan D03 T09 §6 | (GIMP) |
| IP-0325 | GIMP legacy layer modes | -- | -- | GP-1440, GP-1441, GP-1442, GP-1443, GP-1444, GP-1445, GP-1446, GP-1447, GP-1448, GP-1449, GP-1450, GP-1451, GP-1452, GP-1453, GP-1454, GP-1455, GP-1456, GP-1457, GP-1458, GP-1459, GP-1460, GP-1461 | core | plan D03 T09 §6 | Kept for XCF fidelity |
| IP-0326 | Affinity modes: average, negation, reflect, glow, contrast negate | -- | AF-0989, AF-0990, AF-0991, AF-0992, AF-0993 | -- | core | plan D03 T09 §6 | (Affinity) |
| IP-0327 | Pigment blend mode (paint-like mixing) | -- | AF-0963 | -- | core | plan D03 T09 §6 | (Affinity) Mixbox-style pigment mixing, own implementation |
| IP-0328 | Blend modes in 32-bit documents | PS-A-0853 | -- | -- | core | plan D03 T09 §6 | Mode subset for float documents, engine D03 T15 §4 |
| IP-0329 | Blend mode menu: grouped families, hover preview, cycling shortcuts | PS-A-0850, PS-A-0851 | AF-0785 | GP-1469, GP-1477, GP-1483, GP-1488, GP-1501 | core | plan D03 T09 §6 |  |
| IP-0330 | Blend mode cycling shortcuts | -- | AF-2753 | -- | core | plan D03 T09 §6 |  |
| IP-0331 | SVG blend ops mapped to existing blend modes | -- | -- | GP-3511, GP-3512, GP-3513, GP-3514, GP-3520, GP-3523, GP-3524, GP-3525 | core | shipped-scope D03 T02 §4 | Op ids map through D01 T06 §1; plus equals linear dodge |
| IP-0332 | Blend mode Normal | PS-A-0821 | AF-0962 | GP-1462, GP-1463 | core | shipped-scope D03 T02 §4 |  |
| IP-0333 | Blend mode Dissolve | PS-A-0822 | -- | GP-1464 | core | shipped-scope D03 T02 §4 |  |
| IP-0334 | Blend mode Darken | PS-A-0825 | AF-0964 | GP-1478 | core | shipped-scope D03 T02 §4 |  |
| IP-0335 | Blend mode Multiply | PS-A-0826 | AF-0965 | GP-1480 | core | shipped-scope D03 T02 §4 |  |
| IP-0336 | Blend mode Color burn | PS-A-0827 | AF-0966 | GP-1481 | core | shipped-scope D03 T02 §4 |  |
| IP-0337 | Blend mode Linear burn | PS-A-0828 | AF-0967 | GP-1482 | core | shipped-scope D03 T02 §4 |  |
| IP-0338 | Blend mode Darker color | PS-A-0829 | AF-0968 | -- | core | shipped-scope D03 T02 §4 |  |
| IP-0339 | Blend mode Lighten | PS-A-0830 | AF-0969 | GP-1502 | core | shipped-scope D03 T02 §4 |  |
| IP-0340 | Blend mode Screen | PS-A-0831 | AF-0970 | GP-1504 | core | shipped-scope D03 T02 §4 |  |
| IP-0341 | Blend mode Color dodge | PS-A-0832 | AF-0971 | GP-1505 | core | shipped-scope D03 T02 §4 |  |
| IP-0342 | Blend mode Linear dodge (add) | PS-A-0833 | AF-0972 | GP-1506 | core | shipped-scope D03 T02 §4 |  |
| IP-0343 | Blend mode Lighter color | PS-A-0834 | AF-0973 | -- | core | shipped-scope D03 T02 §4 |  |
| IP-0344 | Blend mode Overlay | PS-A-0835 | AF-0974 | GP-1470 | core | shipped-scope D03 T02 §4 |  |
| IP-0345 | Blend mode Soft light | PS-A-0836 | AF-0975 | GP-1471 | core | shipped-scope D03 T02 §4 |  |
| IP-0346 | Blend mode Hard light | PS-A-0837 | AF-0976 | GP-1472 | core | shipped-scope D03 T02 §4 |  |
| IP-0347 | Blend mode Vivid light | PS-A-0838 | AF-0977 | GP-1473 | core | shipped-scope D03 T02 §4 |  |
| IP-0348 | Blend mode Linear light | PS-A-0839 | AF-0978 | GP-1475 | core | shipped-scope D03 T02 §4 |  |
| IP-0349 | Blend mode Pin light | PS-A-0840 | AF-0979 | GP-1474 | core | shipped-scope D03 T02 §4 |  |
| IP-0350 | Blend mode Hard mix | PS-A-0841 | AF-0980 | GP-1476 | core | shipped-scope D03 T02 §4 |  |
| IP-0351 | Blend mode Difference | PS-A-0842 | AF-0981 | GP-1489 | core | shipped-scope D03 T02 §4 |  |
| IP-0352 | Blend mode Exclusion | PS-A-0843 | AF-0982 | GP-1490 | core | shipped-scope D03 T02 §4 |  |
| IP-0353 | Blend mode Subtract | PS-A-0844 | AF-0983 | GP-1491 | core | shipped-scope D03 T02 §4 |  |
| IP-0354 | Blend mode Divide | PS-A-0845 | AF-0984 | GP-1494 | core | shipped-scope D03 T02 §4 |  |
| IP-0355 | Blend mode Hue | PS-A-0846 | AF-0985 | GP-1484 | core | shipped-scope D03 T02 §4 | GIMP HSV Hue maps here |
| IP-0356 | Blend mode Saturation | PS-A-0847 | AF-0986 | GP-1485 | core | shipped-scope D03 T02 §4 | GIMP HSV Saturation maps here |
| IP-0357 | Blend mode Color | PS-A-0848 | AF-0987 | GP-1486 | core | shipped-scope D03 T02 §4 | GIMP HSL Color maps here |
| IP-0358 | Blend mode Luminosity | PS-A-0849 | AF-0988 | -- | core | shipped-scope D03 T02 §4 |  |

## Layer styles, smart objects, comps, and artboards

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0359 | Text styling filter: outline, shadow, bevel, inner glow, image overlay | -- | -- | GP-2422, GP-2423, GP-2464, GP-2465, GP-2466, GP-2467, GP-2468, GP-2470, GP-2471, GP-2472, GP-2473, GP-2474, GP-2475, GP-2476, GP-2477, GP-2478, GP-2479, GP-2482, GP-3481 | core | plan D03 T09 §7 | GIMP GEGL Styles maps onto Imago layer effects |
| IP-0360 | Layer Style dialog and effects framework: preview, effect list, fx buttons, Quick FX panel, effect opacity | PS-A-0651, PS-A-0783, PS-A-0854, PS-A-0858, PS-A-0859, PS-A-0861 | AF-0803, AF-1018, AF-1019, AF-1022, AF-1075 | -- | core | plan D03 T09 §7 |  |
| IP-0361 | Multiple effect instances with reorder | PS-A-0856, PS-A-0857 | AF-1020, AF-1021 | -- | core | plan D03 T09 §7 |  |
| IP-0362 | Drop shadow (outer shadow) with on-canvas offset drag and knockout | PS-A-0862, PS-A-0863, PS-A-0864, PS-A-0865, PS-A-0866, PS-A-0867, PS-A-0868, PS-A-0869, PS-A-0870 | AF-1055, AF-1068, AF-1069, AF-1070, AF-1071 | -- | core | plan D03 T09 §7 |  |
| IP-0363 | Inner shadow | PS-A-0871, PS-A-0872, PS-A-0873 | AF-1052, AF-1053, AF-1054, AF-1056 | -- | core | plan D03 T09 §7 |  |
| IP-0364 | Outer glow | PS-A-0874, PS-A-0875, PS-A-0876, PS-A-0877, PS-A-0878 | AF-1066, AF-1067 | -- | core | plan D03 T09 §7 |  |
| IP-0365 | Inner glow | PS-A-0879, PS-A-0880, PS-A-0881, PS-A-0882, PS-A-0883 | AF-1057, AF-1058, AF-1059 | -- | core | plan D03 T09 §7 |  |
| IP-0366 | Satin | PS-A-0895, PS-A-0896, PS-A-0897 | -- | -- | core | plan D03 T09 §7 |  |
| IP-0367 | Stroke and outline effect: size, position, blend, overprint, color, gradient, pattern, contour fill | PS-A-0908, PS-A-0909, PS-A-0910, PS-A-0911, PS-A-0912 | AF-1037, AF-1038, AF-1039, AF-1040, AF-1041 | -- | core | plan D03 T09 §7 |  |
| IP-0368 | Gaussian blur layer effect | -- | AF-1072, AF-1073 | -- | core | plan D03 T09 §7 | (Affinity) preserve alpha option |
| IP-0369 | Global light | PS-A-0915 | -- | -- | core | plan D03 T09 §7 |  |
| IP-0370 | Copy, paste, and clear layer style, paste effects only | PS-A-0916, PS-A-0917, PS-A-0918 | AF-0958, AF-0959 | -- | core | plan D03 T09 §7 |  |
| IP-0371 | Effect visibility per effect, hide all effects, hide effects in view | PS-A-0919, PS-A-0928 | AF-1074 | -- | core | plan D03 T09 §7 |  |
| IP-0372 | Scale effects and scale styles with transforms | PS-A-0920, PS-A-0929 | AF-1024 | -- | core | plan D03 T09 §7 |  |
| IP-0373 | Create layers from effects and rasterize layer style | PS-A-0921, PS-A-0922 | -- | -- | core | plan D03 T09 §7 |  |
| IP-0374 | Layer styles on text | PS-A-1632 | -- | -- | core | plan D03 T09 §7 |  |
| IP-0375 | GEGL Styles text styling filter: outline, shadow, bevel, inner glow | -- | -- | GP-0009 | core | plan D03 T09 §7 | Also listed in the Filter menu via D03 T14 §2 |
| IP-0376 | Flatten all layer effects | PS-B-0762 | -- | -- | automation | plan D03 T09 §7 |  |
| IP-0377 | Bevel and emboss: style, technique, depth, direction, size, soften, shading, gloss, highlight and shadow | PS-A-0884, PS-A-0885, PS-A-0886, PS-A-0887, PS-A-0888, PS-A-0889, PS-A-0890, PS-A-0891, PS-A-0892 | AF-1026, AF-1027, AF-1028, AF-1029, AF-1030, AF-1031, AF-1032, AF-1033, AF-1034, AF-1035, AF-1036 | -- | core | plan D03 T09 §8 |  |
| IP-0378 | Bevel contour and texture sub-effects | PS-A-0893, PS-A-0894 | -- | -- | core | plan D03 T09 §8 |  |
| IP-0379 | Color overlay | PS-A-0898 | AF-1060, AF-1061 | -- | core | plan D03 T09 §8 |  |
| IP-0380 | Gradient overlay: style, angle, scale, offset, align with layer, method | PS-A-0899, PS-A-0900, PS-A-0901, PS-A-0902, PS-A-0903, PS-A-0904 | AF-1062, AF-1063, AF-1064, AF-1065 | -- | core | plan D03 T09 §8 |  |
| IP-0381 | Pattern overlay | PS-A-0905, PS-A-0906, PS-A-0907 | -- | -- | core | plan D03 T09 §8 |  |
| IP-0382 | Contour editor and contour presets | PS-A-0913, PS-A-0914 | -- | -- | core | plan D03 T09 §8 |  |
| IP-0383 | 3D lighting effect with multiple lights and material | -- | AF-1042, AF-1043, AF-1044, AF-1045, AF-1046, AF-1047, AF-1048, AF-1049, AF-1050, AF-1051 | -- | core | plan D03 T09 §8 | (Affinity) diffuse, specular, shininess, ambient |
| IP-0384 | Styles panel: groups, apply, additive apply, legacy sets, save style from layer | PS-A-0855, PS-A-0860, PS-A-0923, PS-A-0925, PS-A-0926, PS-A-0927 | AF-1023, AF-2490, AF-2491 | -- | core | plan D03 T09 §8 |  |
| IP-0385 | Style library import and export (ASL and Affinity styles) | PS-A-0924 | AF-2492 | -- | core | plan D03 T09 §8 | ASL import now; Affinity style files wait for B-045 |
| IP-0386 | Style picker tool with attribute choices | -- | AF-0386, AF-0387, AF-0388, AF-0389, AF-0390, AF-0391, AF-0392, AF-0393, AF-0394, AF-0395, AF-0396 | -- | core | plan D03 T09 §8 | (Affinity) |
| IP-0387 | Styles panel | PS-B-1359 | -- | -- | core | plan D03 T09 §8 |  |
| IP-0388 | Edit or replace embedded document | -- | AF-2602 | -- | format | plan D03 T09 §9 |  |
| IP-0389 | Convert to smart object and smart object layer | PS-A-0691, PS-A-0699, PS-A-0663 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0390 | New smart object via copy | PS-A-0700 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0391 | Edit smart object or placed document contents in a tab | PS-A-0703 | AF-0374, AF-0824 | -- | core | plan D03 T09 §9 |  |
| IP-0392 | Replace contents | PS-A-0715 | AF-0375 | -- | core | plan D03 T09 §9 |  |
| IP-0393 | Export smart object contents | PS-A-0709 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0394 | Convert smart object to layers | PS-A-0714 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0395 | Reset smart object transform | PS-A-0716 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0396 | Rasterize smart object | PS-A-0717 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0397 | Smart object properties panel | PS-A-0730 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0398 | Image layers: placed images at source resolution with DPI, convert to image, rasterize on paint | -- | AF-0373, AF-0819, AF-0820, AF-0821, AF-0822 | -- | core | plan D03 T09 §9 | (Affinity) |
| IP-0399 | Embedded and linked document layers | -- | AF-0823 | -- | core | plan D03 T09 §9 | (Affinity) PDF, PSD, SVG, EPS placed documents |
| IP-0400 | Non-destructive transform of smart objects | PS-A-1339 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0401 | Smart object properties page | PS-A-1524 | -- | -- | core | plan D03 T09 §9 |  |
| IP-0402 | Default image placement: embed or link | -- | AF-2316 | -- | core | plan D03 T09 §10 |  |
| IP-0403 | Open as link layer and change linked image | -- | -- | GP-0049, GP-0050, GP-0859 | core | plan D03 T09 §10 | GIMP 3.2 link layers |
| IP-0404 | Package linked files | PS-B-0928 | -- | -- | core | plan D03 T09 §10 |  |
| IP-0405 | Place linked smart object | PS-A-0702 | -- | -- | core | plan D03 T09 §10 |  |
| IP-0406 | Update modified linked content with status badges | PS-A-0704, PS-A-0705, PS-A-0735 | -- | -- | core | plan D03 T09 §10 |  |
| IP-0407 | Relink, resolve broken links, reveal in Explorer | PS-A-0706, PS-A-0707, PS-A-0708 | -- | -- | core | plan D03 T09 §10 |  |
| IP-0408 | Embed linked and convert to linked | PS-A-0710, PS-A-0711, PS-A-0712 | -- | -- | core | plan D03 T09 §10 |  |
| IP-0409 | Package linked files | PS-A-0713 | -- | -- | core | plan D03 T09 §10 |  |
| IP-0410 | GIMP link layers with relative or absolute paths | -- | -- | GP-3741, GP-3742 | core | plan D03 T09 §10 |  |
| IP-0411 | Resource manager for linked images: locate, update, relink, replace, embed, collect, auto update on change | -- | AF-2500, AF-2501, AF-2502, AF-2651 | -- | core | plan D03 T09 §10 |  |
| IP-0412 | States panel capture scope | -- | AF-2495 | -- | core | plan D03 T09 §11 | Affinity states map to layer comps |
| IP-0413 | Layer comps panel and new comp with visibility, position, appearance, comment | PS-A-0930, PS-A-0931, PS-A-0932 | -- | -- | core | plan D03 T09 §11 |  |
| IP-0414 | Apply layer comps, previous and next, last document state | PS-A-0933, PS-A-0934, PS-A-0936 | -- | -- | core | plan D03 T09 §11 |  |
| IP-0415 | Update, duplicate, and delete layer comps with invalid-comp warnings | PS-A-0935, PS-A-0937, PS-A-0938 | -- | -- | core | plan D03 T09 §11 |  |
| IP-0416 | Smart object layer comp selection | PS-A-0731, PS-A-0940 | -- | -- | core | plan D03 T09 §11 |  |
| IP-0417 | Layer states: captured visibility and effects with scope | -- | AF-0936, AF-0938, AF-0939, AF-0940, AF-0944 | -- | core | plan D03 T09 §11 | (Affinity States panel) |
| IP-0418 | Layer state queries by tag, type, name, lock | -- | AF-0937, AF-0941, AF-0942, AF-0943 | -- | core | plan D03 T09 §11 | (Affinity) regex name match |
| IP-0419 | Layer Comps panel | PS-B-1349 | -- | -- | core | plan D03 T09 §11 |  |
| IP-0420 | States panel: capture visibility and effect states, update and apply, query by tag, type, name, lock | -- | AF-2494, AF-2496, AF-2497 | -- | core | plan D03 T09 §11 |  |
| IP-0421 | Align visible layers | -- | -- | GP-1142, GP-1143, GP-1144, GP-1145 | core | plan D03 T09 §12 |  |
| IP-0422 | Move tool modifiers: nudge, Shift constrain, Alt-drag duplicate | PS-A-0050, PS-A-0051, PS-A-0052 | -- | -- | core | plan D03 T09 §12 | extends D03 T03 §4 |
| IP-0423 | Auto-select layer or group with Ctrl-click override | PS-A-0034, PS-A-0035, PS-A-0036 | AF-0362, AF-0363, AF-0364, AF-0365, AF-0928, AF-0929 | -- | core | plan D03 T09 §12 |  |
| IP-0424 | Right-click layer picker for stacked and nested layers | PS-A-0055 | AF-0848 | -- | core | plan D03 T09 §12 |  |
| IP-0425 | Marquee-select layers on canvas when intersecting | -- | AF-0931 | -- | core | plan D03 T09 §12 | (Affinity) |
| IP-0426 | Show transform controls | PS-A-0037 | -- | -- | core | plan D03 T09 §12 |  |
| IP-0427 | Hover layer bounds, panel highlight, expand groups, cycle overlapping | PS-A-0044, PS-A-0045, PS-A-0046, PS-A-0047, PS-A-0048, PS-A-0049 | -- | -- | core | plan D03 T09 §12 |  |
| IP-0428 | Drag layers or groups to another document | PS-A-0053 | AF-0903 | GP-1335 | core | plan D03 T09 §12 |  |
| IP-0429 | Align layers: edges and centers, to selection, canvas, or key object | PS-A-0038, PS-A-0041, PS-A-0672, PS-A-0941, PS-A-0942, PS-A-0943, PS-A-0944, PS-A-0945, PS-A-0946, PS-A-0947 | AF-0372, AF-0951, AF-0952 | -- | core | plan D03 T09 §12 |  |
| IP-0430 | Distribute layers by edges or centers | PS-A-0039, PS-A-0673, PS-A-0948 | -- | -- | core | plan D03 T09 §12 |  |
| IP-0431 | Distribute spacing: auto or fixed gap | PS-A-0040, PS-A-0949 | AF-0954 | -- | core | plan D03 T09 §12 |  |
| IP-0432 | Alignment handles and make same rotation | -- | AF-0370, AF-0948, AF-0953 | -- | core | plan D03 T09 §12 | (Affinity alignment) |
| IP-0433 | GIMP align and distribute tool: targets, relative to, control points, paths, guides | -- | -- | GP-0632, GP-0633, GP-0634, GP-0635, GP-0636, GP-0637, GP-0638, GP-0639, GP-0640, GP-0641, GP-0642, GP-0643, GP-0644, GP-0645, GP-0646 | core | plan D03 T09 §12 |  |
| IP-0434 | Move tool pick modes: pick layer or guide, move selected layers, pick or move path | -- | -- | GP-0679, GP-0680, GP-0681, GP-0682, GP-0683, GP-0684, GP-0685 | core | plan D03 T09 §12 | extends D03 T03 §4 |
| IP-0435 | Move tool sets the clicked layer or path active | -- | -- | GP-4283 | core | plan D03 T09 §12 |  |
| IP-0436 | New document with artboard | -- | AF-2319 | -- | core | plan D03 T09 §13 |  |
| IP-0437 | Fit artboard on screen | PS-A-1717 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0438 | Guides scoped to artboards | PS-A-1688 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0439 | Constraints panel for child scaling and anchoring | -- | AF-2363 | -- | core | plan D03 T09 §13 | Applies when artboards or groups resize |
| IP-0440 | Artboard tool with size presets, width, height, orientation | PS-A-0056, PS-A-0057, PS-A-0058, PS-A-0059, PS-A-0960, PS-A-0961 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0441 | Add adjacent artboards and Alt-drag duplicate | PS-A-0060, PS-A-0064 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0442 | Artboard layout: auto-nest layers, auto-size canvas | PS-A-0061, PS-A-0062, PS-A-0063, PS-A-0964 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0443 | New artboard, artboard from group or layers | PS-A-0633, PS-A-0634, PS-A-0635, PS-A-0694 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0444 | Artboard document preset | PS-A-0959 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0445 | Artboard background color and clip content | PS-A-0962, PS-A-0963 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0446 | Artboard name labels | PS-A-0967 | -- | -- | core | plan D03 T09 §13 |  |
| IP-0447 | Artboard properties page: size and background | PS-A-1527 | -- | -- | core | plan D03 T09 §13 |  |

## Selection

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0448 | Marching ants options: show or hide selection edges, pause during moves | PS-A-1727 | -- | GP-0109, GP-1059 | core | plan D03 T10 §1 | extends D03 T03 §5 |
| IP-0449 | Anchor floating layer or selection | -- | -- | GP-1320, GP-1321, GP-3732, GP-3752 | core | plan D03 T10 §1 |  |
| IP-0450 | Save selection to a new or existing channel with replace, add, subtract, intersect | PS-A-0529, PS-A-0530, PS-A-1465 | AF-0523, AF-0529, AF-1094 | GP-0991, GP-3567, GP-3599 | core | plan D03 T10 §1 |  |
| IP-0451 | Load selection dialog: document, channel, invert, operation | PS-A-0525, PS-A-0526, PS-A-0527, PS-A-0528 | -- | -- | core | plan D03 T10 §1 |  |
| IP-0452 | Save selection to file and load selection from file | -- | AF-0527, AF-0528 | -- | core | plan D03 T10 §1 | (Affinity) standalone selection file |
| IP-0453 | Show or hide selection edges (marching ants toggle) | PS-A-0533 | AF-0496 | -- | core | plan D03 T10 §1 | Marching ants options |
| IP-0454 | Force pixel alignment and snapping for selection edges | -- | AF-0469, AF-0537 | -- | core | plan D03 T10 §1 |  |
| IP-0455 | Selection editor dialog with selection preview and buttons | -- | -- | GP-0948, GP-0949, GP-0951, GP-0952 | core | plan D03 T10 §1 |  |
| IP-0456 | Marching ants speed | -- | -- | GP-4192 | core | plan D03 T10 §1 |  |
| IP-0457 | Selection tool antialiasing and feather-at-creation options | PS-A-0073, PS-A-0074, PS-A-0087, PS-A-0088, PS-A-0121 | AF-0453, AF-0462, AF-0464, AF-0475, AF-0476 | GP-0244, GP-0245, GP-0256, GP-0257, GP-0270, GP-0280, GP-0281, GP-0284, GP-0285, GP-0296, GP-0297, GP-0304, GP-0305, GP-0331, GP-0332 | core | plan D03 T10 §2 | extends D03 T03 §5; shared across every selection tool |
| IP-0458 | Move selection outline: drag inside, arrow nudge, reposition while drawing, modifier moves | PS-A-0082, PS-A-0531, PS-A-0532 | AF-0468, AF-0534 | GP-0321, GP-0324, GP-0325 | core | plan D03 T10 §2 | extends D03 T03 §5 |
| IP-0459 | Single row and single column marquee with set width or height | PS-A-0067, PS-A-0068 | AF-0458, AF-0459, AF-0465, AF-0466 | -- | core | plan D03 T10 §2 |  |
| IP-0460 | Marquee style: fixed ratio, fixed size, swap width and height | PS-A-0075, PS-A-0076, PS-A-0077, PS-A-0078 | -- | GP-0259, GP-0308, GP-0309, GP-0310, GP-0311, GP-0312 | core | plan D03 T10 §2 |  |
| IP-0461 | Marquee numeric position and size fields | -- | -- | GP-0260, GP-0261, GP-0313, GP-0314 | core | plan D03 T10 §2 |  |
| IP-0462 | Marquee highlight surround and composition guides while drawing | -- | -- | GP-0262, GP-0263, GP-0315, GP-0316 | core | plan D03 T10 §2 |  |
| IP-0463 | Rectangle selection auto shrink and shrink merged | -- | -- | GP-0264, GP-0265, GP-0317, GP-0318 | core | plan D03 T10 §2 |  |
| IP-0464 | Rounded rectangle selection (tool option and Select menu command, concave) | -- | -- | GP-0306, GP-1000, GP-1001, GP-1002 | core | plan D03 T10 §2 |  |
| IP-0465 | Magnetic lasso with width, contrast, frequency, and manual points | PS-A-0085, PS-A-0091, PS-A-0092, PS-A-0093, PS-A-0096 | AF-0473 | -- | core | plan D03 T10 §2 |  |
| IP-0466 | Magnetic lasso pen pressure and bracket keys change edge width | PS-A-0094, PS-A-0095 | -- | -- | core | plan D03 T10 §2 |  |
| IP-0467 | Mixed freehand and polygonal lasso: modifier switching, remove last point, auto-pan | PS-A-0089, PS-A-0090 | AF-0470, AF-0478, AF-0479 | GP-0278 | core | plan D03 T10 §2 | extends D03 T03 §5 |
| IP-0468 | Select pixels by colormap index: replace, add, subtract, intersect | -- | -- | GP-3889, GP-3893, GP-3894, GP-3895, GP-3896 | core | plan D03 T10 §3 | From the colormap dialog (D03 T11 §10) |
| IP-0469 | Sample all layers option | PS-A-0805 | -- | -- | core | plan D03 T10 §3 | Shared option also used by painting and retouching tools |
| IP-0470 | Magic wand with tolerance | PS-A-0118, PS-A-0120 | AF-0448, AF-0451 | GP-0282, GP-0286, GP-0290 | core | plan D03 T10 §3 |  |
| IP-0471 | Magic wand sample size from point to 101 by 101 average | PS-A-0119 | -- | -- | core | plan D03 T10 §3 |  |
| IP-0472 | Contiguous or global matching | PS-A-0122 | AF-0452 | -- | core | plan D03 T10 §3 |  |
| IP-0473 | Sample all layers or chosen source layers for select tools | PS-A-0123 | AF-0450 | GP-0288 | core | plan D03 T10 §3 |  |
| IP-0474 | Select transparent areas option | -- | -- | GP-0246, GP-0287 | core | plan D03 T10 §3 |  |
| IP-0475 | Diagonal neighbors connectivity | -- | -- | GP-0289 | core | plan D03 T10 §3 |  |
| IP-0476 | Select by criterion (composite, channels, hue, saturation, value, alpha, LCh) and draw mask | -- | -- | GP-0249, GP-0250, GP-0291, GP-0292 | core | plan D03 T10 §3 |  |
| IP-0477 | Drag to set tolerance interactively | -- | AF-0455 | -- | core | plan D03 T10 §3 |  |
| IP-0478 | Select by color tool and command (all matching pixels, sample merged, threshold) | -- | -- | GP-0242, GP-0247, GP-0248, GP-0947 | core | plan D03 T10 §3 |  |
| IP-0479 | Mask from Color Range | PS-A-0751 | -- | -- | core | plan D03 T10 §4 | Entry from mask properties |
| IP-0480 | Tonal range selection for masks | -- | AF-0871 | -- | core | plan D03 T10 §4 |  |
| IP-0481 | Color Range dialog: sampled colors, fuzziness, add and subtract eyedroppers, invert | PS-A-0513, PS-A-0595, PS-A-0602, PS-A-0604, PS-A-0607 | -- | -- | core | plan D03 T10 §4 |  |
| IP-0482 | Color Range previews: thumbnail selection or image, document preview grayscale, black matte, white matte, quick mask | PS-A-0605, PS-A-0606 | -- | -- | core | plan D03 T10 §4 |  |
| IP-0483 | Color Range save and load settings | PS-A-0608 | -- | -- | core | plan D03 T10 §4 |  |
| IP-0484 | Color Range: preset hue families (reds, yellows, greens, cyans, blues, magentas) | PS-A-0596 | AF-0506, AF-0507, AF-0508 | -- | core | plan D03 T10 §4 |  |
| IP-0485 | Tonal range selection: highlights, midtones, shadows | PS-A-0597 | AF-0509, AF-0510, AF-0511 | -- | core | plan D03 T10 §4 |  |
| IP-0486 | Color Range: skin tones and face detection | PS-A-0598, PS-A-0599 | -- | -- | core | plan D03 T10 §4 | Classical face detector; AI face detection D03 T19 §6 |
| IP-0487 | Color Range: out of gamut | PS-A-0600 | -- | -- | core | plan D03 T10 §4 | Gamut check from D01 T04 §2 |
| IP-0488 | Color Range: localized color clusters with range | PS-A-0601, PS-A-0603 | -- | -- | core | plan D03 T10 §4 |  |
| IP-0489 | Select sampled color with tolerance and color model | -- | AF-0515, AF-0516, AF-0517 | -- | core | plan D03 T10 §4 |  |
| IP-0490 | Select by alpha range: fully transparent, partially transparent, opaque | -- | AF-0512, AF-0513, AF-0514 | -- | core | plan D03 T10 §4 |  |
| IP-0491 | Selection from layer or composite luminosity | PS-A-0622 | AF-0519 | -- | core | plan D03 T10 §4 |  |
| IP-0492 | Global matting from a trimap | -- | -- | GP-3419 | core | plan D03 T10 §6 |  |
| IP-0493 | Focus Area: in-focus range, image noise level, auto, soften edge, view modes | PS-A-0514, PS-A-0609, PS-A-0610, PS-A-0611, PS-A-0613 | -- | -- | core | plan D03 T10 §6 | Classical focus measure, no ML |
| IP-0494 | Focus Area add and subtract brush, output to, and send to Select and Mask | PS-A-0612, PS-A-0614, PS-A-0615 | -- | -- | core | plan D03 T10 §6 |  |
| IP-0495 | Paint select tool (brush-based progressive selection) | -- | -- | GP-0042 | core | plan D03 T10 §5 |  |
| IP-0496 | Quick selection brush with edge snapping, brush settings, modes, sample all layers | PS-A-0111, PS-A-0112, PS-A-0113, PS-A-0114, PS-A-0117 | AF-0440, AF-0441, AF-0442, AF-0443, AF-0445 | -- | core | plan D03 T10 §5 | Affinity Selection Brush with Snap to edges is this tool |
| IP-0497 | Quick selection auto-enhance and hard or soft edges | PS-A-0115, PS-A-0116 | AF-0446 | -- | core | plan D03 T10 §5 |  |
| IP-0498 | Selection brush painting the selection directly as an overlay | PS-A-0125, PS-A-0126, PS-A-0127, PS-A-0128, PS-A-0129, PS-A-0130, PS-A-0131 | AF-0444 | -- | core | plan D03 T10 §5 | Affinity Snap to edges off behaves the same |
| IP-0499 | Foreground select with draw modes, stroke width, and preview mode | -- | -- | GP-0266, GP-0267, GP-0268, GP-0271, GP-0272, GP-0273 | core | plan D03 T10 §5 |  |
| IP-0500 | Foreground select matting engines (Levin, Global) with levels and iterations | -- | -- | GP-0274, GP-0275, GP-0276, GP-0277 | core | plan D03 T10 §5 | Shares matting code with D03 T10 §6 |
| IP-0501 | Intelligent scissors with auto-edge snap and interactive boundary | -- | -- | GP-0293, GP-0294, GP-0298 | core | plan D03 T10 §5 |  |
| IP-0502 | Paint select tool | -- | -- | GP-4254 | core | plan D03 T10 §5 |  |
| IP-0503 | Remove black matte and remove white matte | -- | AF-1748, AF-1749 | -- | core | plan D03 T09 §14 | Layer > Matting, with IP-0259 |
| IP-0504 | Refine mask edge in Select and Mask | PS-A-0750 | AF-0859 | -- | core | plan D03 T10 §7 | Entry from mask properties and mask context menu |
| IP-0505 | Refine button on every selection tool opens Select and Mask | PS-A-0079 | AF-0447, AF-0454, AF-0461, AF-0477, AF-0484 | -- | ai | plan D03 T10 §7 |  |
| IP-0506 | Select and Mask workspace with quick selection, brush, lasso, hand and zoom | PS-A-0515, PS-A-0549, PS-A-0550, PS-A-0552, PS-A-0554, PS-A-0555, PS-A-0591, PS-A-0592 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0507 | Select and Mask clear selection and invert buttons | PS-A-0579, PS-A-0580 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0508 | Select and Mask view modes: onion skin, marching ants, overlay, on black, on white, black and white, on layers, transparent | PS-A-0556, PS-A-0557, PS-A-0558, PS-A-0559, PS-A-0560, PS-A-0561, PS-A-0562, PS-A-0567, PS-A-0568 | AF-0540, AF-0541, AF-0542, AF-0543, AF-0544 | -- | core | plan D03 T10 §7 | Includes view opacity and overlay color |
| IP-0509 | Show edge and show original | PS-A-0563, PS-A-0564 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0510 | Real-time refinement and high-quality preview | PS-A-0565, PS-A-0566 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0511 | Refine edge brush | PS-A-0551 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0512 | Refine Selection brushes: matte, foreground, background, feather, width | -- | AF-0550, AF-0551, AF-0552, AF-0553, AF-0554 | -- | core | plan D03 T10 §7 |  |
| IP-0513 | Edge detection radius, smart radius, and color-aware refine mode | PS-A-0569, PS-A-0573, PS-A-0574 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0514 | Global refinements: smooth, feather, contrast, shift edge | PS-A-0575, PS-A-0576, PS-A-0577, PS-A-0578 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0515 | Affinity Refine Selection: matte edges, border width, smooth, feather, ramp | -- | AF-0539, AF-0545, AF-0546, AF-0547, AF-0548, AF-0549 | -- | core | plan D03 T10 §7 |  |
| IP-0516 | Decontaminate colors with amount | PS-A-0581, PS-A-0582 | AF-0555 | -- | core | plan D03 T10 §7 |  |
| IP-0517 | Refine output to selection, mask, new layer, layer with mask, new document | PS-A-0583, PS-A-0584, PS-A-0585, PS-A-0586, PS-A-0587, PS-A-0588 | AF-0556, AF-0557, AF-0558, AF-0559 | -- | core | plan D03 T10 §7 |  |
| IP-0518 | Refine an existing layer mask later | -- | AF-0560 | -- | core | plan D03 T10 §7 |  |
| IP-0519 | Select and Mask remember settings and presets | PS-A-0589, PS-A-0590 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0520 | Legacy Refine Edge dialog option | PS-A-0594 | -- | -- | core | plan D03 T10 §7 | One refine engine; the preference opens a compact dialog layout |
| IP-0521 | Layer matting: defringe, color decontaminate, remove black and white matte | PS-A-0545, PS-A-0546, PS-A-0547, PS-A-0548 | -- | -- | core | plan D03 T09 §14 | Layer > Matting, with IP-0259 |
| IP-0522 | Double-clicking a layer mask opens Select and Mask | PS-B-1233 | -- | -- | core | plan D03 T10 §7 |  |
| IP-0523 | Alpha to selection: replace, add, subtract, intersect | -- | -- | GP-1315, GP-1316, GP-1317, GP-1318, GP-3768 | core | plan D03 T10 §8 |  |
| IP-0524 | Border and outline selection with width, alignment, style, and rounding | PS-A-0516 | AF-0502, AF-0503, AF-0504, AF-0505 | GP-0943, GP-0944, GP-0945 | core | plan D03 T10 §8 |  |
| IP-0525 | Smooth selection | PS-A-0517 | AF-0501 | -- | core | plan D03 T10 §8 |  |
| IP-0526 | Expand and contract selection (grow or shrink, circular) | PS-A-0518, PS-A-0519 | AF-0498, AF-0499 | GP-0983, GP-0984, GP-0988, GP-0989 | core | plan D03 T10 §8 |  |
| IP-0527 | Apply effect at canvas bounds option for modify commands | -- | -- | GP-0946, GP-0975, GP-0990 | core | plan D03 T10 §8 |  |
| IP-0528 | Grow and Similar by tolerance | PS-A-0521, PS-A-0522 | -- | -- | core | plan D03 T10 §8 |  |
| IP-0529 | Transform selection outline only | PS-A-0523 | AF-0533 | -- | core | plan D03 T10 §8 |  |
| IP-0530 | Remove holes from selection | -- | -- | GP-0982 | core | plan D03 T10 §8 |  |
| IP-0531 | Sharpen selection (remove antialiasing) | -- | -- | GP-0987 | core | plan D03 T10 §8 |  |
| IP-0532 | Distort selection with threshold, spread, granularity, smoothing | -- | -- | GP-0993, GP-0994, GP-0995, GP-0996, GP-0997, GP-0998, GP-0999 | core | plan D03 T10 §8 |  |
| IP-0533 | Floating selections: cut and float, copy and float, anchor | -- | -- | GP-0976, GP-0977, GP-0978, GP-0979, GP-0980, GP-0981 | core | plan D03 T10 §8 |  |
| IP-0534 | Selection from layer transparency or type glyphs with modifier combinations | PS-A-0621, PS-A-0623 | AF-0518, AF-0520 | -- | core | plan D03 T10 §8 |  |
| IP-0535 | Reselect last selection | PS-A-0502 | AF-0494 | -- | core | plan D03 T10 §9 |  |
| IP-0536 | Select all layers, deselect layers, find layers | PS-A-0504, PS-A-0505, PS-A-0506 | -- | -- | core | plan D03 T10 §9 |  |
| IP-0537 | Select menu organization | -- | -- | GP-0941 | core | plan D03 T10 §9 |  |
| IP-0538 | Selection from path, shape, or curve | PS-A-0624 | AF-0526 | GP-0939 | core | plan D03 T10 §9 | Engine D03 T16 §5 |
| IP-0539 | Selection to path | -- | -- | GP-0992, GP-3964 | core | plan D03 T10 §9 | Engine D03 T16 §5 |
| IP-0540 | Selection to path advanced tracing settings (thresholds, filtering, subdivision, keep knees) | -- | -- | GP-0950, GP-0953, GP-0954, GP-0955, GP-0956, GP-0957, GP-0958, GP-0959, GP-0960, GP-0961, GP-0962, GP-0963, GP-0964, GP-0965, GP-0966, GP-0967, GP-0968, GP-0969, GP-0970, GP-0971, GP-0972 | core | plan D03 T10 §9 | Engine D03 T16 §5 |
| IP-0541 | Rectangular and elliptical marquee (Shift square or circle, Alt from center) | PS-A-0065, PS-A-0066, PS-A-0080, PS-A-0081 | AF-0456, AF-0457, AF-0463, AF-0467 | GP-0251, GP-0252, GP-0253, GP-0254, GP-0258, GP-0299, GP-0300, GP-0301, GP-0302, GP-0307 | core | shipped-scope D03 T03 §5 |  |
| IP-0542 | Lasso and polygonal lasso | PS-A-0083, PS-A-0084 | AF-0471, AF-0472 | -- | core | shipped-scope D03 T03 §5 |  |
| IP-0543 | Selection modes new, add, subtract, intersect with Shift and Alt modifiers | PS-A-0069, PS-A-0070, PS-A-0071, PS-A-0072, PS-A-0086, PS-A-0124 | AF-0449, AF-0460, AF-0474, AF-0538 | GP-0243, GP-0255, GP-0269, GP-0279, GP-0283, GP-0295, GP-0303, GP-0319, GP-0320, GP-0322, GP-0323, GP-0326, GP-0327, GP-0328, GP-0329, GP-0330 | core | shipped-scope D03 T03 §5 | Shared mode row for every selection tool |
| IP-0544 | Select all, deselect, and invert selection | PS-A-0500, PS-A-0501, PS-A-0503 | AF-0028, AF-0492, AF-0493, AF-0495, AF-0525 | GP-0942, GP-0985, GP-0986 | core | shipped-scope D03 T03 §5 |  |
| IP-0545 | Feather selection command | PS-A-0520 | AF-0500 | GP-0973, GP-0974 | core | shipped-scope D03 T03 §5 |  |

## Channels and quick mask

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0546 | Channels panel with thumbnails, visibility, target, reset, and per-mode channel list | PS-A-1460, PS-A-1461, PS-A-1475 | AF-1076, AF-1077, AF-1079, AF-1080, AF-1081 | GP-3565, GP-3566, GP-3572, GP-3573, GP-3574, GP-3579 | core | plan D03 T10 §10 |  |
| IP-0547 | Single channel and composite view shortcuts | PS-A-1462 | -- | -- | core | plan D03 T10 §10 |  |
| IP-0548 | Show channels in color | PS-A-1463 | -- | -- | core | plan D03 T10 §10 |  |
| IP-0549 | Channel lock attributes (pixels, position, visibility, editable) | -- | AF-1078 | GP-3575, GP-3576, GP-3577, GP-3578 | core | plan D03 T10 §10 |  |
| IP-0550 | Alpha and spare channels: new, delete, name | PS-A-1466, PS-A-1467, PS-A-1480 | AF-1084, AF-1085 | GP-3580, GP-3581, GP-3582, GP-3587, GP-3590, GP-3594 | core | plan D03 T10 §10 | Channel limit matches Photoshop 56 for PSD round trip |
| IP-0551 | New channel and channel options dialog: name, masked or selected areas, color, opacity | PS-A-1468, PS-A-1472 | -- | GP-3588 | core | plan D03 T10 §10 |  |
| IP-0552 | Rename and reorder channels (raise, lower, drag) | PS-A-1476, PS-A-1477 | -- | GP-3583, GP-3584, GP-3591, GP-3592 | core | plan D03 T10 §10 |  |
| IP-0553 | Duplicate channel to same, other, or new document with invert | PS-A-1469 | -- | GP-3585, GP-3593 | core | plan D03 T10 §10 |  |
| IP-0554 | Multi-select channels and channel color tags | -- | -- | GP-3571, GP-3589 | core | plan D03 T10 §10 |  |
| IP-0555 | Channel to selection with add, subtract, intersect and modifier clicks | PS-A-0620, PS-A-1464 | AF-0521, AF-0522, AF-1086, AF-1087 | GP-3568, GP-3586, GP-3595, GP-3596, GP-3597, GP-3598 | core | plan D03 T10 §10 |  |
| IP-0556 | Composite alpha channel and live pixel selection channel | -- | AF-1082, AF-1083 | -- | core | plan D03 T10 §10 |  |
| IP-0557 | Load channel into layer channel, mask, adjustment, filter, grayscale or mask layer; invert, clear, fill channel | -- | AF-0524, AF-1088, AF-1089, AF-1090, AF-1091 | -- | core | plan D03 T10 §10 |  |
| IP-0558 | Edit alpha channels with brushes and filters, including non-destructive filters | PS-A-1478 | AF-1092 | GP-0067 | core | plan D03 T10 §10 | Live filters on channels use D03 T14 §1 |
| IP-0559 | Spot channels: new spot channel, solidity, merge spot | PS-A-1470, PS-A-1471 | -- | -- | print | plan D03 T10 §10 |  |
| IP-0560 | Split and merge channels | PS-A-1473, PS-A-1474 | -- | -- | core | plan D03 T10 §10 | Engine shared with D03 T11 §8 |
| IP-0561 | Quick mask mode: paint the selection as an overlay | PS-A-0524, PS-A-0616, PS-A-0619 | AF-0029, AF-0530, AF-1093 | GP-0938, GP-0940, GP-3569, GP-3570 | core | plan D03 T10 §10 |  |
| IP-0562 | Quick mask options: masked or selected areas, color, opacity, view style | PS-A-0617, PS-A-0618 | AF-0531 | -- | core | plan D03 T10 §10 |  |
| IP-0563 | Quick Mask button with mask color and masked or selected area properties | PS-A-0015 | -- | GP-4249, GP-4313 | core | plan D03 T10 §10 |  |
| IP-0564 | Channels panel and show channels in color | PS-B-1216, PS-B-1338 | -- | -- | core | plan D03 T10 §10 |  |

## Adjustments

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0565 | Adjustments panel with adjustment icons, preset groups, and hover preview | PS-A-0969, PS-A-0970, PS-A-0971, PS-A-0973 | AF-1124, AF-1125, AF-1126 | -- | core | plan D03 T11 §1 |  |
| IP-0566 | New adjustment layer from the Layer menu and Layers panel button | -- | AF-1107, AF-1108 | -- | core | plan D03 T11 §1 |  |
| IP-0567 | Custom adjustment presets: save, load, rename, delete, reorder | PS-A-0972, PS-A-0980 | AF-1110, AF-1119, AF-1120, AF-1127 | -- | core | plan D03 T11 §1 | Adjustment preset files (ACV, AHU, ALV) read and written |
| IP-0568 | Built-in presets for Levels, Curves, Hue/Saturation, Black and White, Channel Mixer | PS-A-1009, PS-A-1025, PS-A-1057, PS-A-1067, PS-A-1079 | -- | -- | core | plan D03 T11 §1 |  |
| IP-0569 | Adjustment layer model: non-destructive, built-in mask, auto-mask from selection, child and clipped adjustments, placement | PS-A-0983 | AF-1096, AF-1098, AF-1099, AF-1106 | -- | core | plan D03 T11 §1 |  |
| IP-0570 | Adjustment as child of a layer, group, vector object, or frame content | -- | AF-1097, AF-1101, AF-1121 | -- | core | plan D03 T11 §1 |  |
| IP-0571 | Auto-mask a new adjustment from the active selection | -- | AF-1100 | -- | core | plan D03 T11 §1 |  |
| IP-0572 | New adjustment placement preference: above selected or clipped to it | -- | AF-1102, AF-1103 | -- | core | plan D03 T11 §1 |  |
| IP-0573 | Adjustment Properties: re-edit, clip to layer, view previous, reset, visibility, merge, delete, opacity, blend mode | PS-A-0974, PS-A-0975, PS-A-0976, PS-A-0977, PS-A-0978 | AF-1109, AF-1112, AF-1113, AF-1114, AF-1115, AF-1116, AF-1118, AF-1123 | -- | core | plan D03 T11 §1 | Scrubby sliders and double-click reset |
| IP-0574 | Linked adjustment instances (adjustment symbols) | -- | AF-1104 | -- | core | plan D03 T11 §1 | Imago links settings across instances; the Symbols panel itself is Nodus |
| IP-0575 | Merge adjustment layer into the layer below | PS-A-0982 | AF-1111 | -- | core | plan D03 T11 §1 |  |
| IP-0576 | Destructive Image > Adjustments commands with last-used settings (Alt) | PS-A-0981, PS-A-0984 | -- | -- | core | plan D03 T11 §1 | On a smart object applies as a smart filter (D03 T14 §1) |
| IP-0577 | On-image targeted adjustment tool (Curves, Hue/Saturation, Black and White) | PS-A-0979, PS-A-1056, PS-A-1066 | AF-1146, AF-1169 | -- | core | plan D03 T11 §1 |  |
| IP-0578 | Quick Adjustments panel: sliders creating adjustment layers, auto buttons, reset | -- | AF-1128, AF-1129, AF-1130, AF-1131 | -- | core | plan D03 T11 §1 |  |
| IP-0579 | Adjustment brush tool: adjustment type, width, opacity, flow, hardness, blend mode, erase | -- | AF-0330, AF-0331, AF-0332, AF-0333, AF-0334, AF-0335, AF-0336, AF-0337, AF-1132, AF-1133, AF-1134 | -- | core | plan D03 T11 §1 | Paints the mask of a new adjustment layer |
| IP-0580 | Colors menu organization: Auto, Components, Desaturate, Info, Map, Tone Mapping submenus | -- | -- | GP-1511, GP-1512, GP-1513, GP-1516, GP-1517, GP-1518, GP-1526 | core | plan D03 T11 §1 | GIMP menu names mapped onto Imago Adjustments menu groups |
| IP-0581 | Import Photoshop curves and levels presets (ACV, ALV) | -- | -- | GP-0087, GP-0088 | format | plan D03 T11 §1 |  |
| IP-0582 | Adjustment layers via menu, panel button, and content options | PS-A-0654, PS-A-0655, PS-A-0685, PS-A-0784 | AF-0802, AF-0827 | -- | core | plan D03 T11 §1 |  |
| IP-0583 | Adjustment layer insertion: auto mask from selection, above parent or clipped | -- | AF-0828, AF-0830, AF-0831 | -- | core | plan D03 T11 §1 |  |
| IP-0584 | Adjustments panel, adjustment properties page, and Quick Adjustments panel | PS-A-1525, PS-B-1335 | AF-2504 | -- | core | plan D03 T11 §1 |  |
| IP-0585 | Brightness/Contrast legacy and linear modes, auto, edit as Levels | PS-A-0988, PS-A-0989 | AF-1150 | GP-1677 | core | plan D03 T11 §2 | extends D03 T05 §2 |
| IP-0586 | Light adjustment: exposure, contrast, highlights, shadows, whites, blacks | PS-A-0990, PS-A-0991, PS-A-0992, PS-A-0993, PS-A-0994, PS-A-0995, PS-A-0996, PS-A-0997 | -- | -- | core | plan D03 T11 §2 | Engine D01 T07 §1; version selector switches to legacy Brightness/Contrast |
| IP-0587 | Levels extensions: crossed levels negative, edit as Curves | -- | AF-1208 | GP-1730 | core | plan D03 T11 §2 | extends D03 T05 §2 |
| IP-0588 | Levels and Curves in any color model (RGB, gray, CMYK, Lab) and alpha channel | -- | AF-1105, AF-1164, AF-1165, AF-1199, AF-1200 | GP-1696 | core | plan D03 T11 §2 | extends D03 T05 §2 |
| IP-0589 | Levels and Curves working space (linear, non-linear, perceptual) and linear or log histogram | -- | -- | GP-1698, GP-1699, GP-1700, GP-1701, GP-1702, GP-1722, GP-1723, GP-1724, GP-1725, GP-1726 | core | plan D03 T11 §2 | extends D03 T05 §2 |
| IP-0590 | Black, gray, and white point eyedroppers and pick points from image in Levels and Curves | PS-A-1003, PS-A-1016, PS-A-1027 | AF-1377 | GP-1731, GP-1732 | core | plan D03 T11 §2 | extends D03 T05 §2; sample average and sample merged |
| IP-0591 | Auto color correction options: algorithms, snap neutral midtones, target colors and clipping | PS-A-1005, PS-A-1006, PS-A-1007, PS-A-1024 | -- | -- | core | plan D03 T11 §11 | Engine D01 T03 §4 auto adjust |
| IP-0592 | Clipping display while dragging Levels and Curves endpoints | PS-A-1008, PS-A-1017 | AF-1207 | -- | core | plan D03 T11 §2 |  |
| IP-0593 | Curves pencil and freehand modes with smoothing, smooth or corner point types | PS-A-1013, PS-A-1014 | -- | GP-1706, GP-1707, GP-1708, GP-1709 | core | plan D03 T11 §2 | extends D03 T05 §2 |
| IP-0594 | Curve display options: light or pigment, grid size, channel overlays, baseline, intersection line | PS-A-1018, PS-A-1019, PS-A-1020, PS-A-1022, PS-A-1023 | -- | -- | core | plan D03 T11 §2 | extends D03 T05 §2 |
| IP-0595 | Curves input range min and max for HDR values | -- | AF-1172, AF-1173 | -- | core | plan D03 T11 §2 | extends D03 T05 §2; 32-bit documents D03 T15 §4 |
| IP-0596 | Exposure: exposure, offset, gamma, black level, eyedroppers | PS-A-1028, PS-A-1029, PS-A-1030, PS-A-1031, PS-A-1032 | AF-1175, AF-1176 | GP-1611, GP-1612, GP-1613, GP-3390 | core | plan D03 T11 §11 | Engine D01 T03 §4 |
| IP-0597 | Shadows/Highlights: amount, tone, radius, color, midtone, clipping, white point, compress | PS-A-1101, PS-A-1102, PS-A-1103, PS-A-1104, PS-A-1105, PS-A-1106, PS-A-1107 | AF-1274, AF-1275, AF-1276 | GP-1652, GP-1653, GP-1654, GP-1655, GP-1656, GP-1657, GP-1658, GP-1659, GP-1660, GP-1661, GP-1662, GP-3466, GP-3467 | core | plan D03 T11 §11 | Includes the Affinity Photo 2 only adjustment layer |
| IP-0598 | Equalize with selection options | PS-A-1130, PS-A-1131 | -- | GP-1672 | core | plan D03 T11 §11 | Engine D01 T03 §4 |
| IP-0599 | Auto Tone, Auto Contrast, Auto Color, and auto levels commands | PS-A-1132, PS-A-1133, PS-A-1134 | AF-1135, AF-1136, AF-1137, AF-0027 | -- | core | plan D03 T11 §11 | Engine D01 T03 §4 auto adjust |
| IP-0600 | Auto white balance | -- | AF-1138 | GP-1673 | core | plan D03 T11 §11 | Engine D01 T03 §4 white balance |
| IP-0601 | Stretch contrast and stretch contrast HSV | -- | -- | GP-1668, GP-1669, GP-1670, GP-1671, GP-3479, GP-3480 | core | plan D03 T11 §11 |  |
| IP-0602 | Retinex: uniform, low, high levels, scale, divisions, dynamic | -- | -- | GP-1775, GP-1776, GP-1777, GP-1778, GP-1779, GP-1780, GP-1781, GP-1782 | core | plan D03 T11 §11 |  |
| IP-0603 | Contrast curve for grayscale images | -- | -- | GP-3370 | core | plan D03 T11 §11 | gegl:contrast-curve |
| IP-0604 | Clarity and dehaze adjustment layer | PS-A-1041, PS-A-1042, PS-A-1043 | -- | -- | core | plan D01 T07 §2 | exposed as an adjustment layer through the D03 T11 §1 framework |
| IP-0605 | Auto levels, auto contrast, and auto colors filters | -- | AF-1709, AF-1710, AF-1711 | -- | core | plan D03 T11 §11 |  |
| IP-0606 | Auto white balance filter | -- | AF-1712 | -- | core | plan D03 T11 §11 |  |
| IP-0607 | Shadows and highlights filter with default and 1.6 algorithms | -- | AF-1827, AF-1828, AF-1829, AF-1830, AF-1831, AF-1832, AF-1833, AF-1834 | -- | core | plan D03 T11 §11 | Live filter version via D03 T14 §1 |
| IP-0608 | Hue/Saturation range extensions: range sliders, range eyedroppers, overlap, HSV mode, hue wheel nodes | PS-A-1054, PS-A-1055 | AF-1186, AF-1188, AF-1189 | GP-1712 | core | plan D03 T11 §3 | extends D03 T05 §2 |
| IP-0609 | Saturation and hue curves (hue versus saturation, hue, luma) | -- | AF-1375, AF-1376 | -- | core | plan D03 T11 §3 |  |
| IP-0610 | Color balance: shadows, midtones, highlights, preserve luminosity | PS-A-1058, PS-A-1059, PS-A-1060, PS-A-1061 | AF-1157, AF-1158, AF-1159, AF-1160, AF-1161, AF-1162 | GP-1678, GP-1679, GP-1680, GP-1681, GP-1682 | core | plan D03 T11 §3 | Engine D01 T03 §5 |
| IP-0611 | Vibrance | PS-A-1033, PS-A-1034, PS-A-1035 | AF-1265, AF-1266, AF-1267 | -- | core | plan D03 T11 §3 | Engine D01 T03 §5 |
| IP-0612 | Color and vibrance adjustment: temperature, tint, vibrance, saturation | PS-A-1036, PS-A-1037, PS-A-1038, PS-A-1039, PS-A-1040 | -- | -- | core | plan D03 T11 §3 | Engine D01 T03 §4 and §5 |
| IP-0613 | Black and white: six color sliders, tint, auto | PS-A-1062, PS-A-1063, PS-A-1064, PS-A-1065 | AF-1139, AF-1140, AF-1141, AF-1142, AF-1143, AF-1144, AF-1145 | -- | core | plan D03 T11 §3 | Engine D01 T03 §5 |
| IP-0614 | Photo filter and lens filter: filter presets, color, density, preserve luminosity | PS-A-1068, PS-A-1069, PS-A-1070, PS-A-1071, PS-A-1072 | AF-1194, AF-1195, AF-1196, AF-1197 | -- | core | plan D03 T11 §3 | Engine D01 T03 §11 photo filter |
| IP-0615 | Selective color: nine color families, CMYK sliders, relative or absolute | PS-A-1097, PS-A-1098, PS-A-1099, PS-A-1100 | AF-1243, AF-1244, AF-1245, AF-1246, AF-1247, AF-1248, AF-1249 | -- | core | plan D03 T11 §3 | Engine D01 T03 §5 |
| IP-0616 | Hue-chroma (LCh hue, chroma, lightness) | -- | -- | GP-1619, GP-1620, GP-1621, GP-1622, GP-3402 | core | plan D03 T11 §3 |  |
| IP-0617 | Saturation with interpolation color space | -- | -- | GP-1646, GP-1647, GP-1648, GP-3462 | core | plan D03 T11 §3 |  |
| IP-0618 | Color temperature: original and intended temperature | -- | -- | GP-1575, GP-1576, GP-1577, GP-3366 | core | plan D03 T11 §3 | Engine D01 T03 §4 temperature |
| IP-0619 | Vibrance | -- | -- | GP-0070 | core | plan D03 T11 §3 | Engine D01 T03 §5 |
| IP-0620 | Channel mixer: output channel, source sliders, constant, total, monochrome, preserve luminosity, color model, alpha | PS-A-1073, PS-A-1074, PS-A-1075, PS-A-1076, PS-A-1077, PS-A-1078 | AF-1151, AF-1154, AF-1155 | GP-1552, GP-1553, GP-1554, GP-1555, GP-1556, GP-3359 | core | plan D03 T11 §4 | Engine D01 T03 §5 |
| IP-0621 | Channel mixer in any color model with alpha output for keying | -- | AF-1152, AF-1153, AF-1156 | -- | core | plan D03 T11 §4 |  |
| IP-0622 | Color lookup: 3D LUT files, abstract and device link profiles, dither, table order | PS-A-1080, PS-A-1081, PS-A-1082, PS-A-1083, PS-A-1084, PS-A-1085 | AF-1209, AF-1210 | -- | core | plan D03 T11 §4 | .cube, .3dl, .look, .csp |
| IP-0623 | Infer LUT from a source image and its graded version | -- | AF-1211 | -- | core | plan D03 T11 §4 |  |
| IP-0624 | LUT library management: categories, import, export, sort, rename, move | -- | AF-1212, AF-1213, AF-1214, AF-1215, AF-1216, AF-1217, AF-1218, AF-1219, AF-1220, AF-1221, AF-1222, AF-1223, AF-1224, AF-1225, AF-1226, AF-1227 | -- | core | plan D03 T11 §4 | Affinity .afluts category files read |
| IP-0625 | Export color lookup tables from the adjustment stack | PS-A-1086 | AF-1346, AF-1347, AF-1348, AF-1349, AF-1350 | -- | format | plan D03 T11 §4 | Top-level adjustments only; formats .cube, .3dl, .csp, .look |
| IP-0626 | Gradient map: gradient editor, stops, reverse, dither, interpolation method | PS-A-1092, PS-A-1093, PS-A-1094, PS-A-1095, PS-A-1096 | AF-1177, AF-1178, AF-1179, AF-1180, AF-1181, AF-1182, AF-1183, AF-1184 | GP-1765 | core | plan D03 T11 §4 | Gradient editor shared with D03 T12 §9 |
| IP-0627 | Match color: luminance, intensity, fade, neutralize, source, selections, statistics | PS-A-1118, PS-A-1119, PS-A-1120, PS-A-1121, PS-A-1122, PS-A-1123, PS-A-1124, PS-A-1125 | -- | -- | core | plan D03 T11 §4 |  |
| IP-0628 | Replace color: fuzziness, localized clusters, eyedroppers, hue, saturation, lightness | PS-A-1126, PS-A-1127, PS-A-1128, PS-A-1129 | -- | -- | core | plan D03 T11 §4 | Engine D01 T03 §5 replace colors |
| IP-0629 | Sample colorize: map colors from a sample image onto a grayscale image | -- | -- | GP-1783, GP-1784, GP-1785, GP-1786, GP-1787, GP-1788, GP-1789, GP-1790, GP-1791, GP-1792 | core | plan D03 T11 §4 | Near Match Color |
| IP-0630 | White balance adjustment with click, drag, and marquee pickers | -- | AF-1268, AF-1269, AF-1270, AF-1271, AF-1272, AF-1273 | -- | core | plan D03 T11 §4 | Engine D01 T03 §4 white balance |
| IP-0631 | OCIO adjustment: source and destination color spaces | -- | AF-1233, AF-1234, AF-1235, AF-1236, AF-1378 | -- | core | plan D03 T11 §4 | Needs an OCIO config (D03 T18 §4); OCIO 2.5 |
| IP-0632 | Split toning: highlight and shadow hue and saturation, balance | -- | AF-1257, AF-1258, AF-1259, AF-1260, AF-1261, AF-1262 | -- | core | plan D03 T11 §4 |  |
| IP-0633 | Recolor: hue, saturation, lightness | -- | AF-1239, AF-1240, AF-1241, AF-1242 | -- | core | plan D03 T11 §4 |  |
| IP-0634 | Normals adjustment: rotation, scale, flip X and Y | -- | AF-1228, AF-1229, AF-1230, AF-1231, AF-1232 | -- | core | plan D03 T11 §4 | OpenGL and DirectX normal map conversion |
| IP-0635 | Grain adjustment layer: amount, size, roughness | PS-A-1044, PS-A-1045, PS-A-1046, PS-A-1047 | -- | -- | core | plan D01 T07 §3 | exposed as an adjustment layer through the D03 T11 §1 framework |
| IP-0636 | Color transfer from a preset or reference image: luminance, intensity, saturation, hue, preserve luminance | PS-B-0460, PS-B-0461 | -- | -- | ai | plan D03 T11 §4 | Classical statistical color transfer beside Match Color, no model needed; extends match color |
| IP-0637 | Color lookup table import and export (CUBE, 3DL, CSP, ICC) | PS-B-0911, PS-B-0912 | AF-2637 | -- | core | plan D03 T11 §4 |  |
| IP-0638 | Gradient map from the active gradient | -- | -- | GP-3632 | core | plan D03 T11 §4 |  |
| IP-0639 | Threshold with channel choice and histogram | PS-A-1090, PS-A-1091 | AF-1263, AF-1264 | GP-1733, GP-1734, GP-1735, GP-1736, GP-1737, GP-3489 | core | plan D03 T11 §5 | Engine D01 T03 §5 |
| IP-0640 | Local threshold: radius, antialiasing, levels | -- | -- | GP-1507, GP-1508, GP-1509, GP-1510, GP-3414 | core | plan D03 T11 §5 |  |
| IP-0641 | Posterize | PS-A-1088, PS-A-1089 | AF-1237, AF-1238 | GP-1635, GP-1636, GP-3454 | core | plan D03 T11 §5 | Engine D01 T03 §3 posterize |
| IP-0642 | Invert in perceptual and linear space | PS-A-1087 | AF-1193 | GP-1623, GP-1624, GP-3406, GP-3407 | core | plan D03 T11 §5 | Engine D01 T03 §5 invert |
| IP-0643 | Value invert | -- | -- | GP-1625, GP-3496 | core | plan D03 T11 §5 |  |
| IP-0644 | Desaturate with modes (luminance, luma, lightness, average, value) | PS-A-1117 | -- | GP-1586, GP-1587, GP-1588, GP-1589, GP-1590, GP-1591, GP-3399 | core | plan D03 T11 §5 | Engine D01 T03 §5 desaturate |
| IP-0645 | Color to alpha with transparency and opacity thresholds | -- | -- | GP-1578, GP-1579, GP-1580, GP-1581, GP-3367 | core | plan D03 T11 §5 |  |
| IP-0646 | Color exchange with per-channel thresholds | -- | -- | GP-1558, GP-1559, GP-1560, GP-1561, GP-1562, GP-1563, GP-3363 | core | plan D03 T11 §12 |  |
| IP-0647 | Rotate colors: source and destination hue ranges, gray handling | -- | -- | GP-1564, GP-1565, GP-1566, GP-1567, GP-1568, GP-1569, GP-1570, GP-1571, GP-1572, GP-1573, GP-1574, GP-3365 | core | plan D03 T11 §12 |  |
| IP-0648 | Colorize: hue, saturation, lightness, color | -- | -- | GP-1683, GP-1684, GP-1685, GP-1686, GP-1687 | core | plan D03 T11 §5 | Engine D01 T03 §11 colorize |
| IP-0649 | Color to gray (c2g): radius, samples, iterations, enhance shadows | -- | -- | GP-1547, GP-1548, GP-1549, GP-1550, GP-1551, GP-3356 | core | plan D03 T11 §12 |  |
| IP-0650 | Mono mixer with preserve luminosity | -- | -- | GP-1514, GP-1630, GP-1631, GP-1632, GP-1633, GP-1634, GP-3426 | core | plan D03 T11 §12 |  |
| IP-0651 | Dither: per-channel levels, Floyd-Steinberg, Bayer, random, arithmetic, blue noise, seed | -- | -- | GP-1592, GP-1593, GP-1594, GP-1595, GP-1596, GP-1597, GP-1598, GP-1599, GP-1600, GP-1601, GP-1602, GP-1603, GP-1604, GP-1605, GP-1606, GP-1607, GP-1608, GP-1609, GP-1610, GP-3379 | core | plan D03 T11 §12 | Engine D01 T03 §3 dithering |
| IP-0652 | Extract component with invert and linear output | -- | -- | GP-1582, GP-1583, GP-1584, GP-1585, GP-3369 | core | plan D03 T11 §12 |  |
| IP-0653 | RGB clip: low and high limits | -- | -- | GP-1641, GP-1642, GP-1643, GP-1644, GP-1645, GP-3460 | core | plan D03 T11 §12 |  |
| IP-0654 | Hot: PAL or NTSC safe colors, reduce luminance or saturation, blacken | -- | -- | GP-1766, GP-1767, GP-1768, GP-1769, GP-1770, GP-1771, GP-1772 | core | plan D03 T11 §12 |  |
| IP-0655 | Sepia: strength, sRGB | -- | -- | GP-1649, GP-1650, GP-1651, GP-3465 | core | plan D03 T11 §5 | Engine D01 T03 §11 sepia toning |
| IP-0656 | Alien map: RGB or HSL frequencies, phase shifts, keep components | -- | -- | GP-1527, GP-1528, GP-1529, GP-1530, GP-1531, GP-1532, GP-1533, GP-1534, GP-1535, GP-1536, GP-1537, GP-1538, GP-1539, GP-1540, GP-1541, GP-1542, GP-1543, GP-1544, GP-1545, GP-1546, GP-3345 | core | plan D01 T06 §13 | Imago menu and dialog: D03 T14 §2 |
| IP-0657 | Palette map: recolor from the active palette by value | -- | -- | GP-1773 | core | plan D03 T11 §12 |  |
| IP-0658 | Matte look filter and live filter | -- | AF-1604, AF-1605 | -- | core | plan D03 T11 §5 | Lifted blacks, faded contrast |
| IP-0659 | Erase white paper (white to transparency) | -- | AF-1732 | -- | core | plan D03 T11 §5 | Color to alpha preset |
| IP-0660 | Monochrome dither and web-safe dither filters | -- | AF-1745, AF-1765 | -- | core | plan D03 T11 §12 | Engine D01 T03 §3 |
| IP-0661 | Negative darkroom (film negative enlargement simulation) | -- | -- | GP-3432 | core | plan D03 T11 §12 | Invert variant with film and paper response |
| IP-0662 | Threshold alpha | -- | -- | GP-1311, GP-1312 | core | plan D03 T11 §5 |  |
| IP-0663 | Semi-flatten | -- | -- | GP-1319 | core | plan D03 T11 §5 |  |
| IP-0664 | Color to alpha | -- | -- | GP-1323 | core | plan D03 T11 §5 |  |
| IP-0665 | Color enhance (stretch chroma) | -- | -- | GP-1557, GP-3362 | core | plan D03 T11 §6 |  |
| IP-0666 | Border average | -- | -- | GP-1738, GP-1739, GP-1740 | core | plan D03 T11 §6 |  |
| IP-0667 | Export histogram to a text file | -- | -- | GP-1797, GP-1798, GP-1799, GP-1800, GP-1801 | core | plan D03 T11 §6 |  |
| IP-0668 | Smooth palette: build a striped palette from image colors | -- | -- | GP-1793, GP-1794, GP-1795, GP-1796 | core | plan D03 T11 §6 |  |
| IP-0669 | Brightness/Contrast | PS-A-0985, PS-A-0986, PS-A-0987 | AF-1147, AF-1148, AF-1149 | GP-1674, GP-1675, GP-1676, GP-3354 | core | shipped-scope D03 T05 §2 |  |
| IP-0670 | Levels: per channel input and output, gamma, histogram, auto | PS-A-0998, PS-A-0999, PS-A-1000, PS-A-1001, PS-A-1002, PS-A-1004 | AF-1198, AF-1201, AF-1202, AF-1203, AF-1204, AF-1205, AF-1206 | GP-1718, GP-1719, GP-1720, GP-1721, GP-1727, GP-1728, GP-1729, GP-3411 | core | shipped-scope D03 T05 §2 |  |
| IP-0671 | Curves: per channel point curves, numeric input and output, histogram, delete and nudge points | PS-A-1010, PS-A-1011, PS-A-1012, PS-A-1015, PS-A-1021, PS-A-1026 | AF-1163, AF-1166, AF-1167, AF-1168, AF-1170, AF-1171, AF-1174 | GP-1688, GP-1689, GP-1690, GP-1691, GP-1692, GP-1693, GP-1694, GP-1695, GP-1697, GP-1703, GP-1704, GP-1705 | core | shipped-scope D03 T05 §2 |  |
| IP-0672 | Hue/Saturation: master and six ranges, hue, saturation, lightness, colorize | PS-A-1048, PS-A-1049, PS-A-1050, PS-A-1051, PS-A-1052, PS-A-1053 | AF-1185, AF-1187, AF-1190, AF-1191, AF-1192 | GP-1710, GP-1711, GP-1713, GP-1714, GP-1715, GP-1716, GP-1717 | core | shipped-scope D03 T05 §2 |  |
| IP-2370 | Photo effect adjustment layer: a list of preset photographic looks (sepia, cross-process, and similar) as one adjustment kind | -- | -- | -- | core | plan D03 T11 §5 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1329; AC-2985); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T11 §5 |
| IP-2375 | One-click photo looks (ACDSee special effects: blue steel, childhood, dramatic, gloom, grunge, lomo, purple haze, seventies, somber) as built-in look presets | -- | -- | -- | core | plan D03 T11 §4 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1387; AC-3255, AC-3278, AC-3305 to AC-3307, AC-3323, AC-3324, AC-3333, AC-3334, AC-3340 to AC-3342, AC-3375, AC-3407, AC-3433); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T11 §4 |
| IP-2385 | Light EQ tone equalizer as a filter and adjustment layer: auto, one-step, basic, per-band brightening and darkening, advanced curves, on-image drag | -- | -- | -- | core | plan D03 T11 §11 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1497; AC-3721 to AC-3745, AC-4808, AC-4871); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T11 §11 |

## Image modes and color

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0673 | Bitmap mode: 50 percent threshold, pattern and diffusion dither, halftone screen, custom pattern, output resolution | PS-A-1135, PS-A-1136, PS-A-1137, PS-A-1138, PS-A-1139, PS-A-1140, PS-A-1141 | -- | -- | core | plan D03 T11 §7 | Engine D01 T03 §3 |
| IP-0674 | Grayscale mode | PS-A-1142 | -- | -- | core | plan D03 T11 §7 | Engine D01 T04 §3 |
| IP-0675 | RGB, CMYK, and Lab color modes | PS-A-1157, PS-A-1158, PS-A-1159 | AF-2216 | -- | print | plan D03 T11 §7 | Engine D01 T04 §3 |
| IP-0676 | Multichannel mode | PS-A-1160 | -- | -- | print | plan D03 T11 §7 | Engine D01 T04 §3 |
| IP-0677 | Duotone mode: monotone to quadtone, inks, ink curves, overprint colors, presets | PS-A-1143, PS-A-1144, PS-A-1145, PS-A-1146, PS-A-1147 | -- | -- | core | plan D03 T11 §7 | Engine D01 T04 §3 |
| IP-0678 | Indexed color mode: palettes, color count, forced colors, transparency, matte, dither, preserve exact colors | PS-A-1148, PS-A-1149, PS-A-1150, PS-A-1151, PS-A-1152, PS-A-1153, PS-A-1154, PS-A-1155 | -- | -- | core | plan D03 T11 §7 | Engine D01 T03 §3 |
| IP-0679 | Color table editor and colormap rearrange and set | PS-A-1156 | -- | GP-1741, GP-1802, GP-3897 | core | plan D03 T11 §7 |  |
| IP-0680 | Bit depth 8, 16, and 32 bits per channel | PS-A-1161, PS-A-1162, PS-A-1163 | AF-2217 | -- | core | plan D03 T11 §7 | 32-bit editing D03 T15 §4 |
| IP-0681 | Merge or flatten prompt on mode change | PS-A-1165 | -- | -- | core | plan D03 T11 §7 |  |
| IP-0682 | Mode submenu: RGB and grayscale conversion | -- | -- | GP-1289, GP-1281, GP-1277 | core | plan D03 T11 §7 | Engine D01 T04 §3 |
| IP-0683 | Indexed conversion with colormap and dithering options | -- | -- | GP-1278, GP-1279, GP-1280 | core | plan D03 T11 §7 | Engine D01 T03 §3 |
| IP-0684 | Encoding submenu: precision 8, 16, 32 bit integer and 16, 32 bit float | -- | -- | GP-1282, GP-1283, GP-1284, GP-1285, GP-1301, GP-1302, GP-1303, GP-1304, GP-1305 | core | plan D03 T11 §7 | GIMP precision conversion; document model D03 T08 §1 |
| IP-0685 | Channel encoding: linear light, non-linear, perceptual sRGB | -- | -- | GP-1286, GP-1287, GP-1306, GP-1307, GP-1308 | core | plan D03 T11 §7 | Linear or perceptual precision from D03 T08 §1 |
| IP-0686 | Dithering when reducing precision (layers, text layers, channels) | -- | -- | GP-1288, GP-1309 | core | plan D03 T11 §7 |  |
| IP-0687 | Convert 32-bit to 8 or 16 bit with profile | -- | AF-2027 | -- | core | plan D03 T11 §7 |  |
| IP-0688 | Conditional Mode Change | PS-B-0717, PS-B-0718 | -- | -- | automation | plan D03 T11 §7 |  |
| IP-0689 | Apply Image: source, layer, channel, blending, opacity, mask, preserve transparency, scale to fit | PS-A-1201, PS-A-1202, PS-A-1203, PS-A-1204, PS-A-1205, PS-A-1206 | AF-1547, AF-1548, AF-1549, AF-1550, AF-1551, AF-1552, AF-1553, AF-1554 | -- | core | plan D03 T11 §8 |  |
| IP-0690 | Apply Image equations: per-channel expressions in a chosen color space | -- | AF-1555, AF-1556, AF-1557, AF-1558, AF-1559 | -- | core | plan D03 T11 §8 |  |
| IP-0691 | Calculations: two sources, blending, mask, result to document, channel, or selection | PS-A-1207, PS-A-1208, PS-A-1209, PS-A-1210, PS-A-1211 | -- | -- | core | plan D03 T11 §8 |  |
| IP-0692 | Decompose to RGB, RGBA, alpha, HSV, HSL, CMYK, Lab, LCh, YCbCr layers or images | -- | -- | GP-1745, GP-1746, GP-1747, GP-1748, GP-1749, GP-1750, GP-1751, GP-1752, GP-1753, GP-1754, GP-1755, GP-1756, GP-1757, GP-1758, GP-1759, GP-1760 | core | plan D03 T11 §8 |  |
| IP-0693 | Compose and recompose channels into an image | -- | -- | GP-1742, GP-1743, GP-1744, GP-1774 | core | plan D03 T11 §8 |  |
| IP-0694 | Channels as sources in Apply Image and Calculations | PS-A-1479 | -- | -- | core | plan D03 T11 §8 |  |

## Color panels, swatches, and palettes

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0695 | Eyedropper sample sizes to 101 average and sample layers | PS-A-0184, PS-A-0185 | -- | -- | core | plan D03 T11 §9 | extends D03 T03 §8 |
| IP-0696 | Eyedropper sampling ring | PS-A-0186 | -- | -- | core | plan D03 T11 §9 |  |
| IP-0697 | Temporary eyedropper in painting and fill tools (Alt) | PS-A-0188 | AF-2273 | GP-0122 | core | plan D03 T11 §9 | extends D03 T03 §8 |
| IP-0698 | Sample colors anywhere on screen | PS-A-0187 | AF-2268 | GP-3661 | core | plan D03 T11 §9 |  |
| IP-0699 | HUD color picker (hue strip or wheel on canvas) | PS-A-0189 | -- | -- | core | plan D03 T11 §9 |  |
| IP-0700 | Color sampler tool: multiple persistent samplers, sample size, clear all | PS-A-0190, PS-A-0191, PS-A-0192 | -- | -- | core | plan D03 T11 §9 | Readouts in the Info panel (D03 T08 §5) |
| IP-0701 | Color panel modes: sliders (RGB, HSB, HSL, CMYK, Lab, web, gray), wheel, boxes, cubes, ramps, palette, watercolor | PS-A-1426, PS-A-1427, PS-A-1428 | AF-2257, AF-2258, AF-2260 | GP-3653, GP-3654, GP-3655, GP-3656, GP-3657, GP-3658, GP-3659 | core | plan D03 T11 §9 | extends D03 T03 §8 |
| IP-0702 | Color panel extras: tint slider, opacity and noise, lock slider model, move sliders together, copy hex | -- | AF-2261, AF-2262, AF-2263, AF-2264, AF-2266 | -- | core | plan D03 T11 §9 |  |
| IP-0703 | Intensity slider for unbounded HDR colors | -- | AF-2244 | -- | core | plan D03 T11 §9 | 32-bit documents D03 T15 §4 |
| IP-0704 | Color space shown with color values | -- | -- | GP-0011 | core | plan D03 T11 §9 |  |
| IP-0705 | Gamut and web-safe warnings, only web colors | PS-A-1429, PS-A-1431, PS-A-1435 | -- | -- | core | plan D03 T11 §9 |  |
| IP-0706 | Color picker dialog: HSB, RGB, Lab, CMYK, hex, sample image, add to swatches | PS-A-1430, PS-A-1433, PS-A-1434 | -- | -- | core | plan D03 T11 §9 |  |
| IP-0707 | Color history and recent colors | PS-A-1437 | AF-2265, AF-2282 | GP-3663 | core | plan D03 T11 §9 |  |
| IP-0708 | None (transparent) swatch | -- | AF-2256 | -- | core | plan D03 T11 §9 |  |
| IP-0709 | Color harmonies (chords): types, preview, lock, add chord to swatches | -- | AF-2267, AF-2295, AF-2296, AF-2297 | -- | core | plan D03 T11 §9 |  |
| IP-0710 | Color picker tool: pick target (foreground, background, palette, info only), average radius, sample merged, loupe, apply to selection | -- | AF-0382, AF-0383, AF-0384, AF-0385, AF-2269, AF-2270, AF-2271, AF-2272 | GP-0121, GP-0124, GP-0125, GP-0126, GP-0127, GP-0129, GP-0130 | core | plan D03 T11 §9 |  |
| IP-0711 | Color picker info window (Shift) | -- | -- | GP-0123, GP-0131 | core | plan D03 T11 §9 |  |
| IP-0712 | Color picker samples merged including layer filters | -- | -- | GP-0096 | core | plan D03 T11 §9 |  |
| IP-0713 | Total ink coverage readout in the CMYK color selector | -- | -- | GP-0083 | print | plan D03 T11 §9 |  |
| IP-0714 | Color picker pick target: set foreground color | -- | -- | GP-0128 | core | plan D03 T11 §9 |  |
| IP-0715 | Color panel with dynamic color sliders | PS-B-1217, PS-B-1342 | -- | -- | core | plan D03 T11 §9 |  |
| IP-0716 | Color picker preferences: app or system picker, HUD picker hue strip or wheel and size | PS-B-1198, PS-B-1199 | -- | -- | core | plan D03 T11 §9 |  |
| IP-0717 | Swatches panel: groups, new swatch, add from color or object, edit, search, list view, opacity | PS-A-1436, PS-A-1438, PS-A-1441 | AF-2274, AF-2276, AF-2277, AF-2278, AF-2279, AF-2280, AF-2281, AF-2283, AF-2284 | -- | core | plan D03 T11 §10 |  |
| IP-0718 | Import and export swatches and palettes (ACO, ASE, afpalette), legacy sets | PS-A-1439, PS-A-1440 | AF-2287 | -- | format | plan D03 T11 §10 | Also ACT and GPL |
| IP-0719 | Palette scopes: document, application, system, default per color format | -- | AF-2275, AF-2288 | -- | core | plan D03 T11 §10 |  |
| IP-0720 | Create palette from document, image, or gradient | -- | AF-2285, AF-2286 | GP-3933, GP-3934, GP-3935, GP-3936, GP-3937, GP-3938 | core | plan D03 T11 §10 |  |
| IP-0721 | Global colors and registration color | -- | AF-2289, AF-2290, AF-2291 | -- | print | plan D03 T11 §10 |  |
| IP-0722 | Color libraries (spot color books) in the picker and swatches | PS-A-1432 | AF-2294 | -- | print | plan D03 T11 §10 | Libraries from user files; PANTONE not bundled |
| IP-0723 | Palettes dialog: grid or list, tags, new, duplicate, delete, refresh, show in folder, copy location | -- | -- | GP-3633, GP-3919, GP-3920, GP-3924, GP-3925, GP-3926, GP-3927, GP-3928, GP-3929, GP-3930, GP-3931, GP-3932, GP-3939, GP-3941, GP-3942, GP-3943, GP-3944 | core | plan D03 T11 §10 |  |
| IP-0724 | Palette editor: edit, new from FG or BG, delete color, zoom, edit active palette | -- | -- | GP-3921, GP-3922, GP-3923, GP-3950, GP-3951, GP-3952, GP-3953, GP-3954, GP-3955, GP-3956, GP-3957, GP-3958, GP-3959, GP-3960, GP-3961, GP-3962 | core | plan D03 T11 §10 |  |
| IP-0725 | Palette commands: export as, offset, sort, merge | -- | -- | GP-3940, GP-3945, GP-3946, GP-3949 | core | plan D03 T11 §10 |  |
| IP-0726 | Palette to gradient and repeating gradient | -- | -- | GP-3947, GP-3948 | core | plan D03 T11 §10 | Gradients land in D03 T12 §9 |
| IP-0727 | Colormap dialog for indexed images: edit, add from FG or BG, delete, index and hex | -- | -- | GP-3877, GP-3878, GP-3879, GP-3880, GP-3881, GP-3882, GP-3883, GP-3884, GP-3885, GP-3886, GP-3887, GP-3888, GP-3890, GP-3891, GP-3892 | core | plan D03 T11 §10 |  |
| IP-0728 | Palette import: GPL, ACO, ACT, ACB, ASE, CSS, RIFF, Swatchbooker, CIE Lab, Procreate, text | -- | -- | GP-0037, GP-0091, GP-4874 | format | plan D03 T11 §10 |  |
| IP-0729 | Palette export: GPL, KPL, CSS, PHP, Python, Java, text | -- | -- | GP-4875 | format | plan D03 T11 §10 |  |
| IP-0730 | Krita KPL palette export | -- | -- | GP-0092 | format | plan D03 T11 §10 |  |
| IP-0731 | Swatches panel | PS-B-1360 | -- | -- | core | plan D03 T11 §10 |  |
| IP-0732 | Color panel with foreground and background, swap (X), default (D), hex entry | PS-A-1425 | AF-2253, AF-2254, AF-2255, AF-2259 | GP-0232, GP-0233, GP-3660, GP-3662 | core | shipped-scope D03 T03 §8 |  |
| IP-0733 | Eyedropper tool | PS-A-0183 | -- | -- | core | shipped-scope D03 T03 §8 |  |
| IP-0734 | Toolbox foreground and background color area with swap | -- | -- | GP-0229, GP-0234 | core | shipped-scope D03 T03 §8 |  |
| IP-0735 | Foreground and background swatches with default colors (D) and swap (X) | PS-A-0012, PS-A-0013, PS-A-0014 | AF-2748 | -- | core | shipped-scope D03 T03 §8 |  |
| IP-0736 | macOS screen color picking via ScreenCaptureKit | -- | -- | GP-0111 | core | excluded: platform | macOS only; Windows screen sampling planned in D03 T11 §9 |

## Brushes and painting

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0737 | Bristle brush preview | PS-A-1736 | -- | -- | core | plan D03 T12 §1 |  |
| IP-0738 | Define brush preset from selection | PS-A-1249 | -- | -- | core | plan D03 T12 §1 |  |
| IP-0739 | Brush tip shape: size, angle, roundness, hardness, spacing, flip X and Y | PS-A-0277, PS-A-1343, PS-A-1344, PS-A-1345, PS-A-1346, PS-A-1347, PS-A-1348 | AF-0610, AF-0612, AF-0613, AF-0615, AF-0616 | -- | core | plan D03 T12 §1 | extends D03 T03 §6 |
| IP-0740 | Paint tool brush aspect ratio and angle (shared option across paint tools) | -- | -- | GP-0340, GP-0341, GP-0440, GP-0441, GP-0533, GP-0534, GP-0552, GP-0553, GP-0590, GP-0591, GP-0617, GP-0618 | core | plan D03 T12 §1 | extends D03 T03 §6 |
| IP-0741 | Erodible, bristle, and airbrush tip types | PS-A-1349, PS-A-1350, PS-A-1351 | -- | -- | core | plan D03 T12 §1 |  |
| IP-0742 | Sampled brush tips: define brush from image or selection, intensity and image brushes, new round and square brushes | PS-A-1409 | AF-0597, AF-0598, AF-0599, AF-0600, AF-0601, AF-0667, AF-0673 | -- | core | plan D03 T12 §1 |  |
| IP-0743 | Multi-nozzle brushes with nozzle controller and interpolation | -- | AF-0643, AF-0644, AF-0645, AF-0646, AF-0647 | -- | core | plan D03 T12 §1 |  |
| IP-0744 | Stroke smoothing: amount, pulled string, catch-up, adjust for zoom, GIMP smooth stroke | PS-A-0272, PS-A-0273, PS-A-0274, PS-A-0275, PS-A-0276, PS-A-1388 | -- | GP-0348, GP-0448, GP-0541, GP-0559, GP-0598, GP-0625 | core | plan D03 T12 §1 | Shared smooth stroke option across paint tools |
| IP-0745 | Stroke stabilizer with rope and window modes | -- | AF-0077, AF-0321 | -- | core | plan D03 T12 §1 |  |
| IP-0746 | Build-up and airbrush mode, accumulation | PS-A-0271, PS-A-1387 | AF-0611 | -- | core | plan D03 T12 §1 |  |
| IP-0747 | Wet edges | PS-A-1386 | AF-0618 | -- | core | plan D03 T12 §1 |  |
| IP-0748 | Brush noise and protect texture | PS-A-1385, PS-A-1389 | -- | -- | core | plan D03 T12 §1 |  |
| IP-0749 | Brush flow in the brush preset | -- | AF-0614 | -- | core | plan D03 T12 §1 | extends D03 T03 §6 |
| IP-0750 | Multi-threaded painting | -- | -- | GP-0046 | core | plan D03 T12 §1 | performance behavior; XCF save threading belongs to D03 T17 §4 |
| IP-0751 | Retouch brush stabilizer and wet edges | -- | AF-0178, AF-0184, AF-0192, AF-0198, AF-0205, AF-0209, AF-0231, AF-0242, AF-0247, AF-0258, AF-0269, AF-0277, AF-0285, AF-0292, AF-0312 | -- | core | plan D03 T12 §1 | Shared by every D03 T13 brush-based retouch tool |
| IP-0752 | Stroke stabilizer: rope and window modes | -- | AF-0068, AF-0075, AF-0076, AF-0091, AF-0108, AF-0134, AF-0147 | -- | core | plan D03 T12 §1 |  |
| IP-0753 | Wet edges with custom edge profile | -- | AF-0073, AF-0112, AF-0138, AF-0151 | -- | core | plan D03 T12 §1 |  |
| IP-0754 | Brush HUD hardness by vertical drag | PS-B-1232 | -- | -- | core | plan D03 T12 §1 |  |
| IP-0755 | Stroke stabilization for paint and erase | -- | AF-0060 | -- | core | plan D03 T12 §1 |  |
| IP-0756 | Shape dynamics: size, angle, roundness, flip jitter with minimums and controls | PS-A-1353, PS-A-1354, PS-A-1355, PS-A-1356, PS-A-1357, PS-A-1358 | AF-0620, AF-0623, AF-0624, AF-0625 | -- | core | plan D03 T12 §2 |  |
| IP-0757 | Dynamics controllers: pressure, tilt, azimuth, barrel rotation, velocity, direction, wheel, distance, cyclic, random, with ramp curves | -- | AF-0631, AF-0632, AF-0633, AF-0634, AF-0635, AF-0636, AF-0637, AF-0638, AF-0639, AF-0640, AF-0641, AF-0642 | GP-0097 | core | plan D03 T12 §2 |  |
| IP-0758 | Brush projection and brush pose overrides (tilt, rotation, pressure) | PS-A-1359, PS-A-1381, PS-A-1382, PS-A-1383, PS-A-1384 | -- | -- | core | plan D03 T12 §2 |  |
| IP-0759 | Scattering: scatter, both axes, count, count jitter, GIMP apply jitter | PS-A-1360, PS-A-1361, PS-A-1362 | AF-0629, AF-0630 | GP-0347, GP-0447, GP-0540, GP-0558, GP-0597, GP-0624 | core | plan D03 T12 §2 | Includes the shared GIMP apply jitter option |
| IP-0760 | Brush texture: pattern, invert, scale, brightness, contrast, modes, depth, each tip, copy to other tools | PS-A-1363, PS-A-1364, PS-A-1365, PS-A-1366, PS-A-1367, PS-A-1394 | AF-0648, AF-0649, AF-0650, AF-0651, AF-0652, AF-0653, AF-0654, AF-0655 | -- | core | plan D03 T12 §2 |  |
| IP-0761 | Dual brush and sub brushes | PS-A-1368, PS-A-1369, PS-A-1370, PS-A-1371 | AF-0656, AF-0657, AF-0658, AF-0659, AF-0660, AF-0661, AF-0662, AF-0663 | -- | core | plan D03 T12 §2 |  |
| IP-0762 | Color dynamics: foreground and background, hue, saturation, brightness jitter, purity, per tip | PS-A-1372, PS-A-1373, PS-A-1374, PS-A-1375, PS-A-1376, PS-A-1377 | AF-0626, AF-0627, AF-0628 | -- | core | plan D03 T12 §2 |  |
| IP-0763 | Transfer dynamics: opacity, flow, wetness, and mix jitter | PS-A-1378, PS-A-1379, PS-A-1380 | AF-0621, AF-0622 | -- | core | plan D03 T12 §2 |  |
| IP-0764 | Paint dynamics matrix and editor: inputs to opacity, size, angle, color, hardness, force, aspect, spacing, rate, flow, jitter, fade and color options | -- | -- | GP-4093, GP-4096, GP-4097, GP-4098, GP-4099, GP-4107, GP-4108, GP-4109, GP-4110, GP-4111, GP-4112, GP-4113, GP-4114, GP-4115, GP-4116, GP-4117, GP-4118, GP-4119 | core | plan D03 T12 §2 |  |
| IP-0765 | Paint tool dynamics selector, enable dynamics, and dynamics options (shared across paint tools) | -- | -- | GP-0030, GP-0345, GP-0346, GP-0445, GP-0446, GP-0538, GP-0539, GP-0556, GP-0557, GP-0595, GP-0596, GP-0622, GP-0623 | core | plan D03 T12 §2 |  |
| IP-0766 | Paste as new brush with name, file, spacing | -- | -- | GP-0897, GP-0899, GP-0900, GP-0901 | core | plan D03 T12 §3 |  |
| IP-0767 | Brushes dialog context menu | -- | -- | GP-3539 | core | plan D03 T12 §3 |  |
| IP-0768 | Photoshop ABR brush import | -- | -- | GP-4863 | format | plan D03 T12 §3 |  |
| IP-0769 | Recent brushes per layer | -- | AF-0796 | -- | core | plan D03 T12 §3 | (Affinity) reselect brushes used on a layer |
| IP-0770 | Brush Settings panel and brush editor: live preview, lock attributes, clear controls, reset, create brush from settings | PS-A-0266, PS-A-1342, PS-A-1352, PS-A-1390, PS-A-1391, PS-A-1392, PS-A-1393 | AF-0609, AF-0664, AF-0665, AF-0666 | -- | core | plan D03 T12 §3 |  |
| IP-0771 | Brushes panel: groups and categories, search, recent brushes, list and thumbnail views, default categories | PS-A-1395, PS-A-1396, PS-A-1398, PS-A-1399, PS-A-1400 | AF-0580, AF-0581, AF-0582, AF-0584, AF-0585, AF-0586, AF-0587, AF-0588, AF-0589, AF-0590, AF-0591, AF-0592, AF-0593, AF-0668, AF-2493 | -- | core | plan D03 T12 §3 |  |
| IP-0772 | Brush preset picker and management: size, rename, duplicate, delete, move, update, reset, modified indicator | PS-A-0265, PS-A-1397, PS-A-1406 | AF-0583, AF-0602, AF-0603, AF-0604, AF-0605, AF-0606, AF-0607, AF-0608 | -- | core | plan D03 T12 §3 |  |
| IP-0773 | Brushes switch to associated tools and each tool remembers its last brush | -- | AF-0594, AF-0619, AF-0669 | -- | core | plan D03 T12 §3 |  |
| IP-0774 | Brush import and export: ABR and Affinity brush files | PS-A-1401, PS-A-1402 | AF-0595, AF-0596 | -- | core | plan D03 T12 §3 |  |
| IP-0775 | Legacy brush sets and reset to factory brushes | PS-A-1403 | AF-0676 | -- | core | plan D03 T12 §3 |  |
| IP-0776 | New brush preset options: capture size, tool settings, and color; tool presets versus brushes | PS-A-1404, PS-A-1407, PS-A-1408, PS-A-1410 | -- | -- | core | plan D03 T12 §3 |  |
| IP-0777 | Paint tool brush selector (shared option across paint tools) | -- | -- | GP-0338, GP-0438, GP-0531, GP-0550, GP-0588, GP-0615 | core | plan D03 T12 §3 |  |
| IP-0778 | Brushes dialog: grid and list, tags, previews, spacing, refresh, open as image, copy location, show in folder | -- | -- | GP-3532, GP-3533, GP-3534, GP-3535, GP-3536, GP-3537, GP-3538, GP-3543, GP-3544, GP-3545, GP-3547, GP-3548, GP-3549, GP-3550, GP-3551, GP-3552 | core | plan D03 T12 §3 |  |
| IP-0779 | Clipboard brush (paste as new brush), up to 8192 px | -- | -- | GP-0085, GP-3542 | core | plan D03 T12 §3 |  |
| IP-0780 | Parametric brush editor: circle, square, diamond, radius, spikes, hardness, aspect, angle, spacing (VBR) | -- | -- | GP-3540, GP-3541, GP-3546, GP-3553, GP-3554, GP-3555, GP-3556, GP-3557, GP-3558, GP-3559, GP-3560, GP-3561, GP-3562, GP-3563, GP-3564, GP-3604, GP-3607 | core | plan D03 T12 §3 |  |
| IP-0781 | GIMP brush files: GBR ordinary and color brushes | -- | -- | GP-3600, GP-3601, GP-3602, GP-3605 | core | plan D03 T12 §3 |  |
| IP-0782 | Image hose (GIH) brushes with multiple marks | -- | -- | GP-3603, GP-3606 | core | plan D03 T12 §3 |  |
| IP-0783 | Paint dynamics presets dialog: new, duplicate, delete, refresh, copy location, show in folder | -- | -- | GP-4094, GP-4095, GP-4100, GP-4101, GP-4102, GP-4103, GP-4104, GP-4105, GP-4106 | core | plan D03 T12 §3 |  |
| IP-0784 | Tool presets: save, restore, edit, and delete tool option presets | -- | -- | GP-0235, GP-0236, GP-0237, GP-0239 | core | plan D03 T12 §3 |  |
| IP-0785 | Tool Presets dialog and tool preset editor | -- | -- | GP-4120, GP-4121, GP-4122, GP-4123, GP-4124, GP-4125, GP-4126, GP-4127, GP-4128 | core | plan D03 T12 §3 |  |
| IP-0786 | Tool presets panel and options bar tool preset picker with current tool only filter | PS-A-0017, PS-A-0018, PS-A-0019, PS-B-1195 | -- | -- | core | plan D03 T12 §3 |  |
| IP-0787 | Brushes and Brush Settings panels | PS-B-1336, PS-B-1337 | -- | -- | core | plan D03 T12 §3 |  |
| IP-0788 | MyPaint MYB brush loading | -- | -- | GP-4864 | format | plan D03 T12 §4 |  |
| IP-0789 | MyPaint brush engine v2 with MYB brushes and barrel rotation | -- | -- | GP-0058, GP-0060, GP-0515, GP-0517, GP-3608 | core | plan D03 T12 §4 |  |
| IP-0790 | MyPaint brush options: radius, opacity, base opacity, hardness, gain, smooth stroke, erase, no erasing, follow view zoom and rotation | -- | -- | GP-0059, GP-0061, GP-0516, GP-0518, GP-0519, GP-0520, GP-0521, GP-0522, GP-0523, GP-0524 | core | plan D03 T12 §4 |  |
| IP-0791 | MyPaint Brushes dialog: grid and list, tags, refresh, copy location, show in folder | -- | -- | GP-3898, GP-3899, GP-3900, GP-3901, GP-3902, GP-3903, GP-3904, GP-3905, GP-3906, GP-3907, GP-3908, GP-3909, GP-3910, GP-3911 | core | plan D03 T12 §4 |  |
| IP-0792 | History and undo brush source from state or snapshot | PS-A-1510, PS-A-1513 | AF-2429, AF-2437, AF-2446 | -- | core | plan D03 T12 §5 |  |
| IP-0793 | Paint tool blend mode including Behind, Clear, and Overwrite (shared option across paint tools) | PS-A-0267 | AF-0617 | GP-0062, GP-0336, GP-0355, GP-0437, GP-0456, GP-0502, GP-0529, GP-0548, GP-0613 | core | plan D03 T12 §5 | extends D03 T03 §6 |
| IP-0794 | Paint tool force (brush gain, shared option across paint tools) | -- | -- | GP-0344, GP-0444, GP-0537, GP-0594, GP-0621 | core | plan D03 T12 §5 |  |
| IP-0795 | Lock brush to view (shared option across paint tools) | -- | -- | GP-0349, GP-0449, GP-0542, GP-0560, GP-0599, GP-0626 | core | plan D03 T12 §5 |  |
| IP-0796 | Incremental paint mode (shared option across paint tools) | -- | -- | GP-0450, GP-0543, GP-0561, GP-0627 | core | plan D03 T12 §5 |  |
| IP-0797 | Expand layers while painting: amount, fill with, fill layer mask with | -- | -- | GP-0021, GP-0350, GP-0504, GP-0525, GP-0544, GP-0562, GP-0600, GP-0628, GP-0629, GP-0630, GP-0631 | core | plan D03 T12 §5 | Shared option across paint tools |
| IP-0798 | Straight and constrained lines while painting (Shift, Ctrl plus Shift) | PS-A-0283 | -- | GP-0335, GP-0528, GP-0547, GP-0585, GP-0586, GP-0608, GP-0609, GP-0611, GP-0612 | core | plan D03 T12 §5 |  |
| IP-0799 | Temporary color picker while painting (Ctrl or Alt) | -- | AF-0083 | GP-0334, GP-0435, GP-0501, GP-0527, GP-0546, GP-0607, GP-0610 | core | plan D03 T12 §5 | Uses the eyedropper from D03 T03 §8 |
| IP-0800 | On-canvas brush size and hardness drag, arrow keys rotate the nozzle | PS-A-0281 | AF-0080, AF-0081 | -- | core | plan D03 T12 §5 | extends D03 T03 §6 |
| IP-0801 | Number keys set opacity and Shift plus number sets flow | PS-A-0282 | AF-0079 | -- | core | plan D03 T12 §5 |  |
| IP-0802 | Paint in HDR on 32-bit documents | PS-A-0280 | -- | -- | core | plan D03 T12 §5 | Engine D03 T15 §4 |
| IP-0803 | New layer when painting on a non-paintable layer and protection of text, link, and vector layers | PS-A-0284 | AF-0078 | GP-0107 | core | plan D03 T12 §5 |  |
| IP-0804 | Pencil and pixel tool: hard-edged aliased strokes with auto erase | PS-A-0285, PS-A-0286, PS-A-0287 | AF-0084 | GP-0545 | core | plan D03 T12 §5 |  |
| IP-0805 | Airbrush tool with rate, flow, and motion only | -- | -- | GP-0333, GP-0351, GP-0352, GP-0353 | core | plan D03 T12 §5 |  |
| IP-0806 | Ink tool: size, angle, sensitivity (size, tilt, speed), nib type and shape | -- | -- | GP-0500, GP-0505, GP-0506, GP-0507, GP-0508, GP-0509, GP-0510, GP-0511, GP-0512, GP-0513, GP-0514 | core | plan D03 T12 §5 |  |
| IP-0807 | History brush and undo brush: paint from a history state or snapshot, blend, protect alpha | PS-A-0329, PS-A-0330 | AF-0314, AF-0315, AF-0316, AF-0317, AF-0318, AF-0319, AF-0320, AF-0325, AF-0326, AF-0327, AF-0328 | -- | core | plan D03 T12 §5 | History source from D03 T03 §2 |
| IP-0808 | Art history brush: styles, area, tolerance | PS-A-0331, PS-A-0332, PS-A-0333, PS-A-0334 | -- | -- | core | plan D03 T12 §5 |  |
| IP-0809 | Retouch brush common options: width, opacity, flow, hardness, brush settings, pressure to size | -- | AF-0172, AF-0173, AF-0174, AF-0175, AF-0176, AF-0177, AF-0186, AF-0187, AF-0188, AF-0189, AF-0190, AF-0191, AF-0200, AF-0201, AF-0202, AF-0203, AF-0204, AF-0206, AF-0211, AF-0212, AF-0213, AF-0214, AF-0225, AF-0226, AF-0227, AF-0228, AF-0229, AF-0230, AF-0236, AF-0237, AF-0238, AF-0239, AF-0240, AF-0241, AF-0252, AF-0253, AF-0254, AF-0255, AF-0256, AF-0257, AF-0263, AF-0264, AF-0265, AF-0266, AF-0267, AF-0268, AF-0279, AF-0280, AF-0281, AF-0282, AF-0283, AF-0284, AF-0306, AF-0307, AF-0308, AF-0309, AF-0310, AF-0311 | -- | core | plan D03 T12 §5 | Shared by every D03 T13 brush-based retouch tool |
| IP-0810 | Paint tool common options on retouch tools: mode, opacity, brush, size, aspect, angle, spacing, hardness, force, dynamics, jitter, smooth stroke, lock to view, expand layers, incremental, hard edge | -- | -- | GP-0368, GP-0369, GP-0370, GP-0371, GP-0372, GP-0373, GP-0374, GP-0375, GP-0376, GP-0377, GP-0378, GP-0379, GP-0380, GP-0381, GP-0382, GP-0391, GP-0394, GP-0395, GP-0396, GP-0397, GP-0398, GP-0399, GP-0400, GP-0401, GP-0402, GP-0403, GP-0404, GP-0405, GP-0406, GP-0407, GP-0408, GP-0409, GP-0415, GP-0416, GP-0417, GP-0418, GP-0419, GP-0420, GP-0421, GP-0422, GP-0423, GP-0424, GP-0425, GP-0426, GP-0427, GP-0428, GP-0429, GP-0430, GP-0482, GP-0483, GP-0484, GP-0485, GP-0486, GP-0487, GP-0488, GP-0489, GP-0490, GP-0491, GP-0492, GP-0493, GP-0494, GP-0495, GP-0496, GP-0497, GP-0567, GP-0568, GP-0569, GP-0570, GP-0571, GP-0572, GP-0573, GP-0574, GP-0575, GP-0576, GP-0577, GP-0578, GP-0579, GP-0580, GP-0583 | core | plan D03 T12 §5 | GIMP common options reused by clone, heal, perspective clone, blur/sharpen, dodge/burn |
| IP-0811 | Affinity brush tool common options: width, opacity, flow, hardness, blend mode, force pressure, brush editor | -- | AF-0062, AF-0063, AF-0064, AF-0065, AF-0066, AF-0067, AF-0072, AF-0085, AF-0086, AF-0087, AF-0088, AF-0089, AF-0090, AF-0095, AF-0102, AF-0103, AF-0104, AF-0105, AF-0106, AF-0107, AF-0114, AF-0115, AF-0116, AF-0117, AF-0128, AF-0129, AF-0130, AF-0131, AF-0132, AF-0133, AF-0141, AF-0142, AF-0143, AF-0144, AF-0145, AF-0146 | -- | core | plan D03 T12 §5 | Shared across paint, pixel, color replacement, mixer, erase, background erase brushes |
| IP-0812 | Protect alpha while painting | -- | AF-0074, AF-0096 | -- | core | plan D03 T12 §5 | Same lock as D03 T09 §1 transparency lock |
| IP-0813 | Pixel tool alternate modifier: erase, background color, undo from snapshot | -- | AF-0097, AF-0098, AF-0099, AF-0100 | -- | core | plan D03 T12 §5 |  |
| IP-0814 | Color replacement tool: hue, saturation, color, luminosity modes, tolerance, anti-alias | PS-A-0288, PS-A-0289, PS-A-0296, PS-A-0297 | AF-0101 | -- | core | plan D03 T12 §6 |  |
| IP-0815 | Color replacement sampling (continuous, once, background swatch) and limits (discontiguous, contiguous, find edges) | PS-A-0290, PS-A-0291, PS-A-0292, PS-A-0293, PS-A-0294, PS-A-0295 | -- | -- | core | plan D03 T12 §6 |  |
| IP-0816 | Mixer brush: wet, load, mix, flow, sample all layers | PS-A-0298, PS-A-0303, PS-A-0304, PS-A-0305, PS-A-0306, PS-A-0307 | AF-0113 | -- | core | plan D03 T12 §6 |  |
| IP-0817 | Mixer brush reservoir: load, clean, load after and clean after each stroke, blend presets | PS-A-0299, PS-A-0300, PS-A-0301, PS-A-0302 | -- | -- | core | plan D03 T12 §6 |  |
| IP-0818 | Pigment paint mixing blend mode (Mixbox style) | -- | AF-0579 | -- | core | plan D03 T12 §6 |  |
| IP-0819 | Smudge tool: strength, rate, flow, finger painting, sample merged, no erasing effect | -- | AF-0216, AF-0217, AF-0218, AF-0219, AF-0220 | GP-0584, GP-0602, GP-0603, GP-0604, GP-0605 | core | plan D03 T12 §6 |  |
| IP-0820 | Smudge tool: strength, mode, finger painting, sample all layers | PS-A-0391, PS-A-0392, PS-A-0393, PS-A-0394 | -- | -- | core | plan D03 T12 §6 |  |
| IP-0821 | Color replacement brush: tolerance, sample continuously, contiguous | -- | AF-0109, AF-0110, AF-0111 | -- | core | plan D03 T12 §6 |  |
| IP-0822 | Paint mixer brush: strength, load, clean, auto load, auto clean, mixing model | -- | AF-0118, AF-0119, AF-0120, AF-0121, AF-0122, AF-0123 | -- | core | plan D03 T12 §6 |  |
| IP-0823 | Eraser modes: brush, pencil, block, with flow, airbrush, and smoothing | PS-A-0336, PS-A-0337 | -- | -- | core | plan D03 T12 §7 | extends D03 T03 §6 |
| IP-0824 | Erase to history | PS-A-0338 | -- | -- | core | plan D03 T12 §7 |  |
| IP-0825 | Background eraser: tolerance and protect foreground color | PS-A-0339, PS-A-0342, PS-A-0343 | AF-0140 | -- | core | plan D03 T12 §7 |  |
| IP-0826 | Background eraser sampling and limits | PS-A-0340, PS-A-0341 | -- | -- | core | plan D03 T12 §7 |  |
| IP-0827 | Magic eraser and flood erase: tolerance, anti-alias, contiguous, all layers, opacity | PS-A-0344, PS-A-0345 | AF-0152 | -- | core | plan D03 T12 §7 |  |
| IP-0828 | Anti-erase (Alt) to restore erased alpha | -- | -- | GP-0436, GP-0453 | core | plan D03 T12 §7 |  |
| IP-0829 | Hard edge option for eraser and smudge | -- | -- | GP-0452, GP-0601 | core | plan D03 T12 §7 | Shared option; smudge use in D03 T12 §6 |
| IP-0830 | Background erase brush: tolerance, sample continuously, contiguous | -- | AF-0148, AF-0149, AF-0150 | -- | core | plan D03 T12 §7 |  |
| IP-0831 | Flood erase tolerance | -- | AF-0153 | -- | core | plan D03 T12 §7 |  |
| IP-0832 | Symmetry painting: vertical, horizontal, dual axis, diagonal, wavy, circle, spiral, parallel lines, central mirror, show or hide | PS-A-0279, PS-A-1411, PS-A-1412, PS-A-1413, PS-A-1414, PS-A-1415, PS-A-1416, PS-A-1417, PS-A-1418, PS-A-1423, PS-A-1424 | -- | GP-4045, GP-4046, GP-4047, GP-4048, GP-4049, GP-4050, GP-4051, GP-4052, GP-4053, GP-4054 | core | plan D03 T12 §11 |  |
| IP-0833 | Radial and mandala symmetry with segment count, mirror, kaleidoscope, and lockable center | PS-A-1419, PS-A-1420 | AF-0221, AF-0222, AF-0223, AF-0322, AF-0323, AF-0324, AF-0670 | GP-4061, GP-4062, GP-4063, GP-4064, GP-4065, GP-4066 | core | plan D03 T12 §11 |  |
| IP-0834 | Symmetry from a custom path with path transform | PS-A-1421, PS-A-1422 | -- | -- | core | plan D03 T12 §11 |  |
| IP-0835 | Tiling symmetry: interval, shift, max strokes | -- | -- | GP-4055, GP-4056, GP-4057, GP-4058, GP-4059, GP-4060 | core | plan D03 T12 §11 |  |
| IP-0836 | Retouch brush symmetry, mirror, and lock center | -- | AF-0179, AF-0180, AF-0181, AF-0193, AF-0194, AF-0195, AF-0232, AF-0233, AF-0234, AF-0243, AF-0244, AF-0245, AF-0259, AF-0260, AF-0261 | -- | core | plan D03 T12 §11 | Shared by every D03 T13 brush-based retouch tool |
| IP-0837 | Symmetry painting with axis count, mirror, and lock | -- | AF-0069, AF-0070, AF-0071, AF-0092, AF-0093, AF-0094, AF-0124, AF-0125, AF-0126, AF-0135, AF-0136, AF-0137 | -- | core | plan D03 T12 §11 |  |
| IP-0838 | Brush tool: round brush with size, opacity, flow, and pen pressure to size and opacity | PS-A-0264, PS-A-0268, PS-A-0269, PS-A-0270, PS-A-0278 | AF-0061 | GP-0526, GP-0606 | core | shipped-scope D03 T03 §6 |  |
| IP-0839 | Bracket keys resize the brush, also mid-stroke | -- | AF-0082 | -- | core | shipped-scope D03 T03 §6 |  |
| IP-0840 | Paint tool opacity (shared option across paint tools) | -- | -- | GP-0337, GP-0356, GP-0457, GP-0503, GP-0530, GP-0549, GP-0587, GP-0614 | core | shipped-scope D03 T03 §6 | Bucket and gradient opacity surfaces in D03 T12 §8 and §9 |
| IP-0841 | Paint tool brush size (shared option across paint tools) | -- | -- | GP-0339, GP-0439, GP-0532, GP-0551, GP-0589, GP-0616 | core | shipped-scope D03 T03 §6 |  |
| IP-0842 | Paint tool hardness (shared option across paint tools) | -- | -- | GP-0343, GP-0443, GP-0536, GP-0555, GP-0593, GP-0620 | core | shipped-scope D03 T03 §6 |  |
| IP-0843 | Paint tool spacing (shared option across paint tools) | -- | -- | GP-0342, GP-0442, GP-0535, GP-0554, GP-0592, GP-0619 | core | shipped-scope D03 T03 §6 |  |
| IP-0844 | Eraser tool: erase to transparency or background color with size, hardness, opacity | PS-A-0335 | AF-0127 | GP-0434, GP-0451 | core | shipped-scope D03 T03 §6 | Affinity mask-on-image-layer behavior planned in D03 T12 §5 |
| IP-0845 | Get more brushes online | PS-A-1405 | -- | -- | cloud | excluded: cloud | Adobe download service |

## Fill, gradients, and patterns

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0846 | Fill selection with color, primary or secondary, inpainting, or history | -- | AF-2299, AF-2300 | -- | core | plan D03 T12 §8 |  |
| IP-0847 | Matte: fill transparent areas with a color | -- | AF-2298 | -- | core | plan D03 T12 §8 |  |
| IP-0848 | Flood fill tool: contiguous, tolerance, blend mode, source | -- | AF-2309 | -- | core | plan D03 T12 §8 | extends D03 T03 §8 paint bucket |
| IP-0849 | Fill command | PS-A-1234 | -- | -- | core | plan D03 T12 §8 |  |
| IP-0850 | Stroke command | PS-A-1235 | -- | -- | core | plan D03 T12 §8 |  |
| IP-0851 | Paint bucket source (foreground, background, pattern), mode and opacity, anti-alias, all layers, fill whole selection, similar colors | PS-A-0376, PS-A-0377, PS-A-0379, PS-A-0381 | -- | GP-0357, GP-0358, GP-0359, GP-0360, GP-0361, GP-0362 | core | plan D03 T12 §8 | extends D03 T03 §8 |
| IP-0852 | Bucket fill by line art detection with gap closure and fill borders | -- | -- | GP-0363, GP-0364, GP-0365 | core | plan D03 T12 §8 |  |
| IP-0853 | Fill dialog: foreground, background, color, pattern, history, black, gray, white, blending, preserve transparency | PS-A-1256, PS-A-1257, PS-A-1258, PS-A-1261, PS-A-1263, PS-A-1264, PS-A-1265, PS-A-1266 | -- | GP-0883, GP-0884, GP-0885 | core | plan D03 T12 §8 |  |
| IP-0854 | Scripted pattern fills: brick, cross weave, random, spiral, symmetry, place along path, frame | PS-A-1262 | -- | -- | core | plan D03 T12 §8 |  |
| IP-0855 | Stroke selection: width, color, location, blending, preserve transparency | PS-A-1267, PS-A-1268, PS-A-1269, PS-A-1270 | -- | GP-0934 | core | plan D03 T12 §8 |  |
| IP-0856 | Stroke path or selection with line style: width, cap, join, miter, dash pattern and presets, antialiasing | -- | -- | GP-0916, GP-0917, GP-0918, GP-0919, GP-0920, GP-0921, GP-0922, GP-0923, GP-0924, GP-0925, GP-0926 | core | plan D03 T12 §8 |  |
| IP-0857 | Stroke with a paint tool and emulate brush dynamics | -- | -- | GP-0927, GP-0928 | core | plan D03 T12 §8 |  |
| IP-0858 | Fill selection outline and fill paths with foreground, background, or pattern | -- | -- | GP-0911, GP-0912, GP-0913, GP-0914, GP-0915, GP-0929, GP-0930, GP-0931, GP-0932, GP-0933 | core | plan D03 T12 §8 | Paths host D03 T16 §5 |
| IP-0859 | Flood fill: tolerance, contiguous, blend mode, source layers | -- | AF-0155, AF-0156, AF-0157, AF-0158 | -- | core | plan D03 T12 §8 |  |
| IP-0860 | Default fill with foreground or background shortcuts | -- | AF-2749 | -- | core | plan D03 T12 §8 |  |
| IP-0861 | Gradient editor and gradient types with on-canvas editing on any layer kind | -- | AF-2301, AF-2302, AF-2303, AF-2304 | -- | core | plan D03 T12 §9 |  |
| IP-0862 | Diffusion gradient fill | -- | AF-2305 | -- | core | plan D03 T12 §9 |  |
| IP-0863 | Transparency tool and transparency gradient editor | -- | AF-2307, AF-2308 | -- | core | plan D03 T12 §9 |  |
| IP-0864 | Gradients panel with groups, import, export, legacy sets | PS-A-1442, PS-A-1443 | -- | -- | core | plan D03 T12 §9 |  |
| IP-0865 | Gradient files: GGR and SVG gradient load, POV-Ray export | -- | -- | GP-4876 | format | plan D03 T12 §9 |  |
| IP-0866 | Gradient fill layer with on-canvas editing | PS-A-0687 | AF-0836 | -- | core | plan D03 T12 §9 |  |
| IP-0867 | Live gradient fill layer mode and gradient fills on fill, mask, and adjustment layers | PS-A-0346, PS-A-0347 | AF-0159 | -- | core | plan D03 T12 §9 | extends D03 T03 §8 |
| IP-0868 | Gradient shapes: angle, reflected, diamond, bi-linear, square, shaped, conical, spiral | PS-A-0351, PS-A-0352, PS-A-0353 | -- | GP-0460, GP-0462, GP-0464, GP-0465, GP-0466, GP-0467, GP-0468, GP-0469 | core | plan D03 T12 §9 |  |
| IP-0869 | Gradient interpolation methods and blend color space: perceptual, linear, classic, smooth, stripes | PS-A-0354, PS-A-0355, PS-A-0356, PS-A-0357, PS-A-0358 | -- | GP-0459 | core | plan D03 T12 §9 |  |
| IP-0870 | Gradient options: reverse, transparency, mode and opacity, repeat, offset, adaptive supersampling | PS-A-0359, PS-A-0361, PS-A-0362 | -- | GP-0470, GP-0471, GP-0473 | core | plan D03 T12 §9 |  |
| IP-0871 | On-canvas gradient editing: stops, midpoints, opacity, instant mode, modify active gradient, angle constraint | PS-A-0363, PS-A-0364 | -- | GP-0455, GP-0474, GP-0475, GP-0476, GP-0477 | core | plan D03 T12 §9 |  |
| IP-0872 | Gradient presets and Gradients panel: picker, save preset, tags, grid and list, new, duplicate, delete, refresh, copy location | PS-A-0348, PS-A-0374 | -- | GP-0110, GP-0458, GP-3630, GP-3631, GP-3792, GP-3793, GP-3797, GP-3798, GP-3799, GP-3800, GP-3801, GP-3802, GP-3804, GP-3805, GP-3806 | core | plan D03 T12 §9 |  |
| IP-0873 | Export gradient as CSS or POV-Ray | -- | -- | GP-3803, GP-3807 | core | plan D03 T12 §9 |  |
| IP-0874 | Gradient editor: color and opacity stops, stop types, smoothness, preview, range sliders, zoom | PS-A-0365, PS-A-0367, PS-A-0373 | -- | GP-0478, GP-3794, GP-3795, GP-3796, GP-3808, GP-3809, GP-3810, GP-3811, GP-3812, GP-3813, GP-3814, GP-3815, GP-3816, GP-3851 | core | plan D03 T12 §9 |  |
| IP-0875 | Noise gradients: roughness, color model, restrict colors, add transparency, randomize | PS-A-0366, PS-A-0368, PS-A-0369, PS-A-0370, PS-A-0371, PS-A-0372 | -- | -- | core | plan D03 T12 §9 |  |
| IP-0876 | Gradient segment endpoint colors: fixed, foreground, background, transparent variants, color slots, drag colors | -- | -- | GP-3817, GP-3818, GP-3819, GP-3820, GP-3821, GP-3822, GP-3823, GP-3824, GP-3825, GP-3826, GP-3827, GP-3828, GP-3829, GP-3830 | core | plan D03 T12 §9 |  |
| IP-0877 | Gradient segment blending functions and coloring type (linear, curved, sinusoidal, spherical, step; RGB, HSV) | -- | -- | GP-3831, GP-3832, GP-3833, GP-3834, GP-3835, GP-3836, GP-3837, GP-3838, GP-3839, GP-3840, GP-3841 | core | plan D03 T12 §9 |  |
| IP-0878 | Gradient segment operations: flip, replicate, split, delete, recenter midpoint, redistribute, blend endpoints | -- | -- | GP-3842, GP-3843, GP-3844, GP-3845, GP-3846, GP-3847, GP-3848, GP-3849, GP-3850 | core | plan D03 T12 §9 |  |
| IP-0879 | Gradient tool fill or stroke context, types, stops, rotate, reverse, aspect, on-canvas stop editing | -- | AF-0160, AF-0161, AF-0162, AF-0163, AF-0164, AF-0165, AF-0169 | -- | core | plan D03 T12 §9 |  |
| IP-0880 | Bitmap fill extend, quality, and scale with object | -- | AF-0166, AF-0167, AF-0168 | -- | core | plan D03 T12 §9 | Affinity bitmap fill type |
| IP-0881 | Gradients panel and dither gradients preference | PS-B-1345 | AF-2677 | -- | core | plan D03 T12 §9 |  |
| IP-0882 | Bitmap fill (tiled image fill) | -- | AF-2306 | -- | core | plan D03 T12 §10 |  |
| IP-0883 | Patterns panel with groups, import, export, legacy sets | PS-A-1444, PS-A-1445 | -- | -- | core | plan D03 T12 §10 |  |
| IP-0884 | Pattern preview mode | PS-A-1446 | -- | -- | core | plan D03 T12 §10 |  |
| IP-0885 | Define pattern | PS-A-1250 | -- | -- | core | plan D03 T12 §10 |  |
| IP-0886 | Paste as new pattern | -- | -- | GP-0898, GP-0902 | core | plan D03 T12 §10 |  |
| IP-0887 | Pattern preview view | PS-A-1723 | -- | -- | core | plan D03 T12 §10 |  |
| IP-0888 | Photoshop PAT pattern loading | -- | -- | GP-0089 | format | plan D03 T12 §10 |  |
| IP-0889 | Hatch pattern PAT import | -- | AF-2643 | -- | format | plan D03 T12 §10 | Affinity imports CAD hatch files as swatches, Imago as patterns |
| IP-0890 | Pattern fill layer | PS-A-0688 | -- | -- | core | plan D03 T12 §10 |  |
| IP-0891 | Pattern layer: tile from selection, live tile painting, mirror, tile transform, open as document | -- | AF-0837, AF-0838, AF-0839, AF-0840, AF-0841, AF-0842 | -- | core | plan D03 T12 §10 | (Affinity) |
| IP-0892 | Patterns dialog: grid and list, tags, duplicate, delete, refresh, open as image, copy location, show in folder | -- | -- | GP-3634, GP-4005, GP-4006, GP-4007, GP-4009, GP-4010, GP-4011, GP-4012, GP-4013, GP-4014, GP-4015, GP-4016, GP-4017, GP-4018, GP-4019, GP-4020, GP-4021 | core | plan D03 T12 §10 |  |
| IP-0893 | Pattern files: PAT plus PNG, JPEG, BMP, GIF, TIFF as patterns | -- | -- | GP-3635, GP-3636 | core | plan D03 T12 §10 |  |
| IP-0894 | Clipboard pattern (paste as new pattern) | -- | -- | GP-4008 | core | plan D03 T12 §10 |  |
| IP-0895 | Pattern stamp tool: aligned and impressionist | PS-A-0325, PS-A-0326, PS-A-0327, PS-A-0328 | -- | -- | core | plan D03 T12 §10 |  |
| IP-0896 | Patterns panel | PS-B-1356 | -- | -- | core | plan D03 T12 §10 |  |
| IP-0897 | Paint bucket and flood fill: tolerance and contiguous | PS-A-0375, PS-A-0378, PS-A-0380 | AF-0154 | GP-0354 | core | shipped-scope D03 T03 §8 |  |
| IP-0898 | Gradient tool: linear and radial foreground to background with dither | PS-A-0349, PS-A-0350, PS-A-0360 | -- | GP-0454, GP-0461, GP-0463, GP-0472 | core | shipped-scope D03 T03 §8 |  |
| IP-0899 | 3D material drop tool | PS-A-0382 | -- | -- | 3d | excluded: removed | Removed with Photoshop 3D |

## Retouching

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0900 | Clone stamp: aligned, sample layers, ignore adjustment layers, image or pattern source, alignment modes | PS-A-0308, PS-A-0309, PS-A-0310, PS-A-0311, PS-A-0312 | AF-0262, AF-0270, AF-0271, AF-0272, AF-0274, AF-0275, AF-0276 | GP-0366, GP-0367, GP-0383, GP-0384, GP-0385, GP-0386, GP-0387, GP-0388, GP-0389, GP-0390 | core | plan D03 T13 §1 | Alignment none, aligned, registered, fixed |
| IP-0901 | Clone Source panel and global sources: multiple sources, offset, scale, rotation, flip, define source area | PS-A-0313, PS-A-0314, PS-A-0315, PS-A-0316, PS-A-0317 | AF-0572, AF-0574, AF-0575, AF-0576, AF-0577, AF-0273, AF-0288, AF-0300 | -- | core | plan D03 T13 §1 | Sources can come from other open documents |
| IP-0902 | Clone source overlay: show, opacity, clipped, auto hide, invert, blend mode | PS-A-0319, PS-A-0320, PS-A-0321, PS-A-0322, PS-A-0323, PS-A-0324 | AF-0293, AF-0573 | -- | core | plan D03 T13 §1 |  |
| IP-0903 | Perspective clone with modify-perspective mode | -- | -- | GP-0563, GP-0564, GP-0565, GP-0566, GP-0581, GP-0582 | core | plan D03 T13 §1 |  |
| IP-0904 | Seamless clone paste | -- | -- | GP-0120 | core | plan D03 T13 §1 | Poisson-blended paste of clipboard content; experimental in GIMP |
| IP-0905 | Clone Source panel | PS-B-1341 | -- | -- | core | plan D03 T13 §1 |  |
| IP-0906 | Red eye removal filter | -- | -- | GP-2388, GP-2389, GP-3457 | core | plan D03 T13 §2 | Filter form of the red eye tool |
| IP-0907 | Seamless clone and seamless clone compose | -- | -- | GP-3463, GP-3464 | core | plan D03 T13 §2 | Poisson blending engine for healing |
| IP-0908 | Healing brush: sampled or pattern source, aligned, sample layers, diffusion, mode, legacy algorithm | PS-A-0221, PS-A-0222, PS-A-0223, PS-A-0224, PS-A-0225, PS-A-0226, PS-A-0227, PS-A-0228, PS-A-0229, PS-A-0230 | AF-0278, AF-0286, AF-0287, AF-0289, AF-0290, AF-0291 | GP-0479, GP-0480, GP-0481, GP-0498, GP-0499 | core | plan D03 T13 §2 |  |
| IP-0909 | Spot healing brush: content-aware, create texture, proximity match | PS-A-0212, PS-A-0213, PS-A-0214, PS-A-0215, PS-A-0216, PS-A-0217, PS-A-0218, PS-A-0219, PS-A-0220 | -- | -- | core | plan D03 T13 §2 | Content-aware type uses the D03 T13 §3 engine |
| IP-0910 | Patch tool: source or destination, transparent, pattern, diffusion, scale and rotation | PS-A-0243, PS-A-0244, PS-A-0246, PS-A-0247, PS-A-0248, PS-A-0249, PS-A-0250 | AF-0294, AF-0295, AF-0296, AF-0297, AF-0298, AF-0299, AF-0301 | -- | core | plan D03 T13 §2 |  |
| IP-0911 | Patch content-aware mode: structure, color, sample all layers | PS-A-0251, PS-A-0252, PS-A-0253, PS-A-0245 | -- | -- | core | plan D03 T13 §2 | Uses the D03 T13 §3 engine |
| IP-0912 | Remove tool classical mode: brush or circle, remove after each stroke, sample all layers | PS-A-0231, PS-A-0232, PS-A-0233, PS-A-0234, PS-A-0242 | -- | -- | ai | plan D03 T13 §2 | Generative mode lives in D03 T19 §3 |
| IP-0913 | Blemish removal tool | -- | AF-0302, AF-0303 | -- | core | plan D03 T13 §2 |  |
| IP-0914 | Inpainting brush and Inpaint command | -- | AF-0305, AF-0313, AF-0561, AF-0562 | -- | core | plan D03 T13 §2 | Classical inpainting; rasterizes the target layer |
| IP-0915 | Red eye tool: pupil size and darken amount | PS-A-0261, PS-A-0262, PS-A-0263 | AF-0329 | -- | core | plan D03 T13 §2 |  |
| IP-0916 | Seamless clone tool | -- | -- | GP-4253 | core | plan D03 T13 §2 |  |
| IP-0917 | Content-Aware Fill workspace: sampling area, color, rotation, scale, mirror adaptation, output target | PS-B-0652, PS-B-0653, PS-B-0654, PS-B-0655 | -- | -- | core | plan D03 T13 §3 | Classical PatchMatch, no generation |
| IP-0918 | Content-aware fill workspace | PS-A-1236 | -- | -- | core | plan D03 T13 §3 |  |
| IP-0919 | Content-aware scale | PS-A-1239 | -- | -- | core | plan D03 T13 §3 |  |
| IP-0920 | Content-aware fill from the Fill dialog with color adaptation | PS-A-1259, PS-A-1260 | -- | -- | core | plan D03 T13 §3 |  |
| IP-0921 | Content-Aware Fill workspace: sampling brush, fill-area lasso, expand and contract, sampling area auto, rectangular, custom, overlay, preview | PS-A-1271, PS-A-1272, PS-A-1273, PS-A-1274, PS-A-1275, PS-A-1276, PS-A-1277, PS-A-1285, PS-A-1286 | -- | -- | core | plan D03 T13 §3 |  |
| IP-0922 | Content-Aware Fill settings: color, rotation, scale, mirror adaptation, output to layer, reset, apply | PS-A-1278, PS-A-1279, PS-A-1280, PS-A-1281, PS-A-1282, PS-A-1283, PS-A-1284 | -- | -- | core | plan D03 T13 §3 |  |
| IP-0923 | Content-Aware Scale: amount, protect channel, protect skin tones, reference point | PS-A-1287, PS-A-1288, PS-A-1289, PS-A-1290, PS-A-1291 | -- | -- | core | plan D03 T13 §3 | Skin protection by classical skin-tone range, no AI |
| IP-0924 | Content-Aware Move: move and extend modes, structure, color, transform on drop | PS-A-0254, PS-A-0255, PS-A-0256, PS-A-0257, PS-A-0258, PS-A-0259, PS-A-0260 | -- | -- | core | plan D03 T13 §3 |  |
| IP-0925 | Delete and fill selection in one step | PS-A-0538 | -- | -- | ai | plan D03 T13 §3 | Classical content-aware fill; generative option via D03 T19 §3 |
| IP-0926 | Heal selection by texture synthesis (Resynthesizer) | -- | -- | GP-4887 | automation | plan D03 T13 §3 | native content-aware engine replaces the third-party plug-in |
| IP-0927 | Dodge and burn tools: range, exposure, protect tones, protect hue | PS-A-0395, PS-A-0396, PS-A-0397, PS-A-0398, PS-A-0399 | AF-0171, AF-0182, AF-0183, AF-0185, AF-0196, AF-0197 | GP-0412, GP-0413, GP-0414, GP-0431, GP-0432, GP-0433 | core | plan D03 T13 §4 |  |
| IP-0928 | Sponge tool: saturate or desaturate, flow, vibrance method | PS-A-0400, PS-A-0401, PS-A-0402, PS-A-0403 | AF-0199, AF-0207, AF-0208 | -- | core | plan D03 T13 §4 |  |
| IP-0929 | Tone brush: paint brightness, contrast, and color with sampled nozzles | -- | AF-0210, AF-0215 | -- | core | plan D03 T13 §4 | Affinity 3 feature |
| IP-0930 | Blur tool: strength, mode, sample all layers | PS-A-0383, PS-A-0384, PS-A-0385, PS-A-0386 | AF-0224 | -- | core | plan D03 T13 §4 |  |
| IP-0931 | Sharpen tool: strength, protect detail, clarity, unsharp mask, and harsh modes | PS-A-0387, PS-A-0388, PS-A-0389, PS-A-0390 | AF-0235, AF-0246, AF-0248, AF-0249, AF-0250 | -- | core | plan D03 T13 §4 |  |
| IP-0932 | Blur and sharpen convolve tool with rate and Ctrl toggle | -- | -- | GP-0392, GP-0393, GP-0410, GP-0411 | core | plan D03 T13 §4 |  |
| IP-0933 | Median brush | -- | AF-0251 | -- | core | plan D03 T13 §4 |  |
| IP-0934 | Frequency separation: radius, Gaussian, median, bilateral methods, tolerance, previews, layer switch | -- | AF-0563, AF-0564, AF-0565, AF-0566, AF-0567, AF-0568, AF-0569, AF-0570, AF-0571, AF-1835, AF-1836, AF-1837, AF-1838, AF-1839, AF-1840, AF-1841, AF-1842 | -- | core | plan D03 T13 §10 |  |
| IP-0935 | Retouching studio workspace | -- | AF-0011, AF-0578 | -- | core | plan D03 T13 §10 | Workspace preset via D03 T20 §1 |
| IP-0936 | Retouching workflows: dodge and burn on 50 percent gray layer, vignette by feathered selection | PS-A-1459, PS-A-1453 | -- | -- | core | plan D03 T13 §10 |  |

## Transform, warp, and liquify

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0937 | Transform submenu: again, scale, rotate, skew, distort, perspective, warp, flips | PS-A-1243 | -- | -- | core | plan D03 T13 §5 | extends D03 T03 §7 |
| IP-0938 | Transform clipping: crop to result and crop with aspect | -- | -- | GP-0789, GP-0790 | core | plan D03 T13 §5 |  |
| IP-0939 | Transform panel: position, size, rotation, shear, anchor, aspect link | -- | AF-2450, AF-2451, AF-2452, AF-2453 | -- | core | plan D03 T13 §5 |  |
| IP-0940 | Transform scale override for strokes, effects, and text | -- | AF-2454 | -- | core | plan D03 T13 §5 |  |
| IP-0941 | Move tool rotate and shear with transform origin | -- | AF-0368, AF-0945, AF-0946, AF-0947 | -- | core | plan D03 T13 §5 | extends D03 T03 §4, Affinity move tool transform |
| IP-0942 | Move tool transform options: lock children, hide selection while dragging, transform separately, aspect constrain | -- | AF-0366, AF-0369, AF-0371, AF-0376, AF-0884 | -- | core | plan D03 T13 §5 | (Affinity) |
| IP-0943 | Cycle and set selection box | -- | AF-0932 | -- | core | plan D03 T13 §5 | (Affinity) base or regular bounding box |
| IP-0944 | Rotate and flip layers: 90, 180, arbitrary | -- | AF-0949, AF-0950 | GP-1327, GP-1328, GP-1412, GP-1413, GP-1414, GP-1415, GP-1428 | core | plan D03 T13 §5 |  |
| IP-0945 | Transform modes: skew, distort, perspective with modifier shortcuts | PS-A-1317, PS-A-1318, PS-A-1323, PS-A-1324, PS-A-1325 | -- | -- | core | plan D03 T13 §5 | extends D03 T03 §7 |
| IP-0946 | Transform numeric options: reference point, position, relative, size, angle, skew, interpolation | PS-A-1307, PS-A-1308, PS-A-1309, PS-A-1310, PS-A-1311, PS-A-1312, PS-A-1313 | -- | -- | core | plan D03 T13 §5 | extends D03 T03 §7 |
| IP-0947 | Transform modifiers: proportional by default, scale from center, legacy behavior preference | PS-A-1315, PS-A-1316 | AF-0765 | -- | core | plan D03 T13 §5 | extends D03 T03 §7 |
| IP-0948 | Transform again and duplicate and transform again | PS-A-1319, PS-A-1320 | -- | -- | core | plan D03 T13 §5 |  |
| IP-0949 | Transform multiple selected layers together | PS-A-1340 | -- | -- | core | plan D03 T13 §5 |  |
| IP-0950 | Layer flip and rotate 90 or 180 | PS-A-1336, PS-A-1337 | AF-0766, AF-0767 | -- | core | plan D03 T13 §5 | extends D03 T03 §7 (canvas-level flip and rotate) |
| IP-0951 | Transform panel and move dialog: numeric position, size, rotation, size to key object, scale override, absolute per-object sizing, size to same | -- | AF-0759, AF-0760, AF-0762, AF-0763, AF-0764, AF-0780 | -- | core | plan D03 T13 §5 |  |
| IP-0952 | Move tool transform origin and arrow-key nudge | -- | AF-0779, AF-0761 | -- | core | plan D03 T13 §5 | extends D03 T03 §4 |
| IP-0953 | Transform selected pixels with handles or Transform panel | -- | AF-0532 | -- | core | plan D03 T13 §5 | extends D03 T03 §7 |
| IP-0954 | Transform modifier keys: constrain, 15 degree rotation, resize from center, cancel | -- | AF-2752 | -- | core | plan D03 T13 §5 | extends D03 T03 §7 |
| IP-0955 | Show transformation values HUD | PS-B-1239 | -- | -- | core | plan D03 T13 §5 |  |
| IP-0956 | Scale layer dialog with interpolation | -- | -- | GP-1416, GP-1417, GP-1418, GP-1419, GP-1420, GP-1421, GP-3758 | core | plan D03 T13 §11 |  |
| IP-0957 | Offset layer with edge behavior | -- | -- | GP-1385, GP-1386, GP-1387, GP-1388, GP-1389, GP-1390, GP-1391, GP-1392 | core | plan D03 T13 §11 | GIMP offset, engine D01 T03 §7 |
| IP-0958 | Transform tool common options: transform target (layer, selection, path, image), direction, interpolation (none, linear, cubic, NoHalo, LoHalo), clipping, image preview, composited preview, guides, opacity | -- | -- | GP-0665, GP-0666, GP-0671, GP-0672, GP-0673, GP-0674, GP-0675, GP-0676, GP-0688, GP-0689, GP-0690, GP-0691, GP-0692, GP-0693, GP-0701, GP-0702, GP-0703, GP-0704, GP-0705, GP-0706, GP-0716, GP-0717, GP-0718, GP-0719, GP-0720, GP-0721, GP-0729, GP-0730, GP-0731, GP-0732, GP-0733, GP-0734, GP-0738, GP-0739, GP-0740, GP-0741, GP-0742, GP-0743, GP-0750, GP-0751, GP-0752, GP-0753, GP-0754, GP-0755, GP-0773, GP-0774, GP-0775, GP-0776, GP-0777, GP-0778, GP-0779, GP-0780, GP-0781, GP-0782, GP-0783, GP-0784, GP-0785, GP-0786, GP-0787, GP-0788, GP-0791, GP-0792, GP-0793, GP-0794, GP-0795, GP-0796, GP-0797, GP-0798, GP-0799, GP-0800, GP-0801 | core | plan D03 T13 §11 | Shared by every Imago transform tool |
| IP-0959 | Flip tool with direction toggle and arrow keys | -- | -- | GP-0663, GP-0664, GP-0667, GP-0078 | core | plan D03 T13 §11 |  |
| IP-0960 | Unified transform tool: constrain, from pivot, pivot snap, matrix, readjust | -- | -- | GP-0748, GP-0749, GP-0756, GP-0757, GP-0758, GP-0759, GP-0760 | core | plan D03 T13 §11 |  |
| IP-0961 | Handle transform tool: add, move, remove handles | -- | -- | GP-0668, GP-0669, GP-0670, GP-0677, GP-0678 | core | plan D03 T13 §11 |  |
| IP-0962 | Scale tool: keep aspect, around center, width and height, readjust | -- | -- | GP-0712, GP-0713, GP-0714, GP-0715, GP-0722, GP-0723, GP-0724, GP-0725, GP-0726 | core | plan D03 T13 §11 |  |
| IP-0963 | Rotate tool and arbitrary rotation: angle, center, 15 degree snap, readjust | -- | -- | GP-0698, GP-0699, GP-0700, GP-0707, GP-0708, GP-0709, GP-0710, GP-0711 | core | plan D03 T13 §11 |  |
| IP-0964 | Shear tool: magnitude X and Y, arrow keys | -- | -- | GP-0727, GP-0728, GP-0735, GP-0736, GP-0079 | core | plan D03 T13 §11 |  |
| IP-0965 | Perspective tool: constrain handles, around center, matrix, readjust | -- | -- | GP-0686, GP-0687, GP-0694, GP-0695, GP-0696, GP-0697 | core | plan D03 T13 §11 |  |
| IP-0966 | 3D transform tool: camera, rotate, pan, constrain axis, Z axis, local frame | -- | -- | GP-0737, GP-0744, GP-0745, GP-0746, GP-0747 | core | plan D03 T13 §11 |  |
| IP-0967 | Warp mesh: split warp, grid presets, multi-point selection, guides, switch from free transform | PS-A-1314, PS-A-1326, PS-A-1327, PS-A-1328, PS-A-1329, PS-A-1334, PS-A-1335 | -- | -- | core | plan D03 T13 §6 |  |
| IP-0968 | Warp style presets: arc, arch, bulge, shell, flag, wave, fish, rise, fisheye, inflate, squeeze, twist, cylinder, bend and distortion | PS-A-1330, PS-A-1331, PS-A-1332, PS-A-1333 | -- | -- | core | plan D03 T13 §6 |  |
| IP-0969 | Warp transform brush tool: move, grow, shrink, swirl, erase, smooth, strength, size, hardness, spacing, abyss, previews | -- | -- | GP-0761, GP-0762, GP-0763, GP-0764, GP-0765, GP-0766, GP-0767, GP-0768, GP-0769, GP-0770, GP-0771 | core | plan D03 T13 §6 |  |
| IP-0970 | Mesh warp tool and live filter: source or destination mode, synchronize, add nodes, resampling | -- | AF-0714, AF-0715, AF-0716, AF-0717, AF-0718, AF-0719, AF-0720, AF-0721, AF-0722, AF-0776 | -- | core | plan D03 T13 §6 | Live version via D03 T14 §1 |
| IP-0971 | Puppet warp command | PS-A-1240 | -- | -- | core | plan D03 T13 §7 |  |
| IP-0972 | Show mesh and edit pins | PS-A-1737, PS-A-1738 | -- | -- | core | plan D03 T13 §7 |  |
| IP-0973 | Deform tool with bone-chain pins | -- | AF-1567 | -- | core | plan D03 T13 §7 |  |
| IP-0974 | N-point image deformation op | -- | -- | GP-3444 | core | plan D03 T13 §7 | Engine behind cage and puppet-style deformation |
| IP-0975 | N-point deformation tool | -- | -- | GP-0119 | core | plan D03 T13 §7 | misrouted into FMT, rubber-like pin deformation |
| IP-0976 | Puppet warp: mode, density, expansion, mesh, pin depth, pin rotation, multiple pins | PS-A-1292, PS-A-1293, PS-A-1294, PS-A-1295, PS-A-1296, PS-A-1297, PS-A-1298, PS-A-1299 | -- | -- | core | plan D03 T13 §7 |  |
| IP-0977 | Deform tool and filter: anchor points, strength, rigid or similarity constraints, bones | -- | AF-0355, AF-0356, AF-0357, AF-0358, AF-0359, AF-0360, AF-0775 | -- | core | plan D03 T13 §7 | Bones added in Affinity 3.3 |
| IP-0978 | Cage transform: create cage, deform, fill original position | -- | -- | GP-0647, GP-0648, GP-0649, GP-0650 | core | plan D03 T13 §7 |  |
| IP-0979 | N-point deformation tool | -- | -- | GP-4252 | core | plan D03 T13 §7 |  |
| IP-0980 | Perspective warp command | PS-A-1241 | -- | -- | core | plan D03 T13 §8 |  |
| IP-0981 | Perspective warp: layout and warp modes, auto straighten and level, edge straighten, shortcuts | PS-A-1300, PS-A-1301, PS-A-1302, PS-A-1303, PS-A-1304, PS-A-1305, PS-A-1306 | -- | -- | core | plan D03 T13 §8 |  |
| IP-0982 | Perspective tool and live filter: single or dual plane, source or destination, grid, autoclip, rotate, flip, snap | -- | AF-0723, AF-0724, AF-0725, AF-0726, AF-0727, AF-0728, AF-0729, AF-0730, AF-0731, AF-0732, AF-0777 | -- | core | plan D03 T13 §8 | Live version via D03 T14 §1 |
| IP-0983 | Liquify tools: forward warp, reconstruct, smooth, twirl, pucker, bloat, push left, freeze, thaw, hand, zoom | PS-B-0374, PS-B-0375, PS-B-0376, PS-B-0377, PS-B-0378, PS-B-0379, PS-B-0380, PS-B-0381, PS-B-0382, PS-B-0384, PS-B-0404, PS-B-0405 | -- | -- | core | plan D03 T13 §9 | Smart object hosting via D03 T14 §1; GPU path |
| IP-0984 | Liquify brush options: size, density, pressure, rate, stylus pressure, pin edges | PS-B-0385, PS-B-0386, PS-B-0387, PS-B-0388, PS-B-0389, PS-B-0390 | -- | -- | core | plan D03 T13 §9 |  |
| IP-0985 | Liquify mesh, mask, view, and reconstruct options | PS-B-0397, PS-B-0403, PS-B-0398, PS-B-0399, PS-B-0400, PS-B-0401, PS-B-0402 | -- | -- | core | plan D03 T13 §9 |  |
| IP-0986 | Face-aware liquify: face tool, eyes, nose, mouth, face shape | PS-B-0383, PS-B-0391, PS-B-0392, PS-B-0393, PS-B-0394, PS-B-0395, PS-B-0396 | -- | -- | core | plan D03 T13 §9 | Face landmarks from D03 T19 §11 |
| IP-0987 | Liquify filter command | PS-B-0007 | -- | -- | core | plan D03 T13 §9 |  |
| IP-0988 | Liquify workspace and filter | -- | AF-0008, AF-0677, AF-1600 | -- | core | plan D03 T13 §9 |  |
| IP-0989 | Liquify live filter: edit in workspace, reset mesh | -- | AF-0678, AF-1601, AF-1602, AF-1603 | -- | core | plan D03 T13 §9 | Live filter layer via D03 T14 §1 |
| IP-0990 | Liquify distortion tools: push forward, push left, twirl, pinch, punch | -- | AF-0679, AF-0680, AF-0681, AF-0682, AF-0683 | -- | core | plan D03 T13 §9 |  |
| IP-0991 | Liquify turbulence and mesh clone tools | -- | AF-0684, AF-0685 | -- | core | plan D03 T13 §9 |  |
| IP-0992 | Liquify reconstruct, freeze, and thaw with mask clear, all, invert | -- | AF-0686, AF-0687, AF-0688, AF-0694, AF-0695, AF-0696 | -- | core | plan D03 T13 §9 |  |
| IP-0993 | Liquify brush options: size, hardness, opacity, speed, ramp, drag resize, slow warp | -- | AF-0689, AF-0690, AF-0691, AF-0692, AF-0693, AF-0712, AF-0713 | -- | core | plan D03 T13 §9 |  |
| IP-0994 | Liquify mesh: show, divisions, color, opacity, reconstruct, apply, load, save, reset, last mesh | -- | AF-0697, AF-0698, AF-0699, AF-0700, AF-0701, AF-0702, AF-0703, AF-0704, AF-0705, AF-0706 | -- | core | plan D03 T13 §9 |  |
| IP-0995 | Liquify view modes and commit: none, split, mirror, apply, cancel | -- | AF-0707, AF-0708, AF-0709, AF-0710, AF-0711 | -- | core | plan D03 T13 §9 |  |
| IP-0996 | Free Transform scale, rotate, and move with commit and cancel | PS-A-1321, PS-A-1322, PS-A-1338 | -- | -- | core | shipped-scope D03 T03 §7 |  |

## Filter framework

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-0997 | Filter availability by color mode and bit depth | PS-B-0011, PS-B-0012 | AF-1429 | -- | core | plan D01 T06 §1 | Imago runs every effect in float; only indexed and bitmap modes disable filters |
| IP-0998 | Convert for smart filters | PS-B-0002 | -- | -- | core | plan D03 T14 §1 | Uses smart objects D03 T09 §9 |
| IP-0999 | Smart filter stack: add, re-edit, reorder, hide, clear, rasterize | PS-B-0018, PS-B-0021, PS-B-0022, PS-B-0023, PS-B-0027, PS-B-0028, PS-B-0029, PS-B-0030 | -- | -- | core | plan D03 T14 §1 | Every Imago filter runs as a smart filter, including Vanishing Point |
| IP-1000 | Smart filter mask with disable and delete | PS-B-0019, PS-B-0025, PS-B-0026 | -- | -- | core | plan D03 T14 §1 |  |
| IP-1001 | Per-filter blending options (mode and opacity) in a smart filter stack | PS-B-0020 | -- | -- | core | plan D03 T14 §1 |  |
| IP-1002 | Copy smart filters between layers | PS-B-0024 | -- | -- | core | plan D03 T14 §1 |  |
| IP-1003 | Live filter layers: add from menu or Layers panel, nest, clip, move in the stack, re-edit | -- | AF-1392, AF-1393, AF-1394, AF-1395, AF-1396, AF-1402, AF-1403, AF-1404, AF-1405, AF-1406 | -- | core | plan D03 T14 §1 | Affinity equivalent of GIMP 3 layer filters |
| IP-1004 | Live filter mask: auto from selection, paint, erase, gradient mask | -- | AF-1397, AF-1398, AF-1399, AF-1400, AF-1401 | -- | core | plan D03 T14 §1 |  |
| IP-1005 | Merge or delete a live filter (bake into the layer) | -- | AF-1417, AF-1418 | GP-3310 | core | plan D03 T14 §1 | GIMP 3 Merge Filter option |
| IP-1006 | Blend ranges and blend options on live filter layers | -- | AF-1424, AF-1425 | -- | core | plan D03 T14 §1 | Uses D03 T09 §5 Blend If |
| IP-1007 | Filter brush tool paints a live filter through its mask | -- | AF-0338, AF-0339, AF-0340, AF-0341, AF-0342, AF-0343, AF-0344, AF-1430, AF-1431 | -- | core | plan D03 T14 §1 | Brush engine D03 T12 §1 |
| IP-1008 | Filter tools apply live by default, Alt applies destructively | -- | AF-1411, AF-1412, AF-1413 | -- | core | plan D03 T14 §1 |  |
| IP-1009 | Smart filters on smart objects with filter masks and blending | PS-A-0652, PS-A-0732, PS-A-0733, PS-A-0758 | -- | -- | core | plan D03 T14 §1 |  |
| IP-1010 | Live filter layers | PS-A-0697 | AF-0804, AF-0832, AF-0833, AF-0834 | -- | core | plan D03 T14 §1 | (Affinity) clip to restrict, child of selected object |
| IP-1011 | GIMP non-destructive layer effects: edit, remove, reorder, visibility, merge | -- | -- | GP-0004, GP-0068, GP-0115, GP-1431, GP-1432, GP-1433, GP-1434, GP-1435, GP-1436, GP-1437, GP-1438, GP-3712, GP-3713, GP-3714, GP-3715, GP-3716, GP-3717, GP-3718, GP-3719, GP-3720, GP-3743 | core | plan D03 T14 §1 |  |
| IP-1012 | Filters on pass-through groups as adjustment layers | -- | -- | GP-0069 | core | plan D03 T14 §1 | (GIMP 3.2) |
| IP-1013 | Common filter dialog options: presets, input type, clipping, blending options, preview, split view, merge filter | -- | -- | GP-1519, GP-1520, GP-1521, GP-1522, GP-1523, GP-1524, GP-1525 | core | plan D03 T14 §2 | Merge filter versus non-destructive layer filter: D03 T14 §1 |
| IP-1014 | Fade last filter, adjustment, or paint stroke | PS-A-1227 | -- | -- | core | plan D03 T14 §2 |  |
| IP-1015 | Filter menu categories: blur, sharpen, distort, noise, enhance, map submenus | -- | AF-1383, AF-1384, AF-1385, AF-1386 | GP-1995, GP-2167, GP-2377, GP-2709, GP-2862 | core | plan D03 T14 §2 | Affinity live filter layer versions of each filter via D03 T14 §1 |
| IP-1016 | Filter menu with category submenus | -- | AF-1382, AF-1387, AF-1388, AF-1389 | GP-3313, GP-1850, GP-2353, GP-2421, GP-2108, GP-2076 | core | plan D03 T14 §2 | Categories generated from Photon.Core effect descriptors |
| IP-1017 | Repeat last filter and reshow last filter dialog | PS-B-0001 | -- | GP-3301, GP-3303 | core | plan D03 T14 §2 |  |
| IP-1018 | Reset filter dialog and reset all remembered filter settings | PS-B-0016 | AF-1421 | GP-3302 | core | plan D03 T14 §2 | extends D03 T05 §1 last-used parameters |
| IP-1019 | Common filter dialog options: preview, split view, presets, input type, clipping, blending mode and opacity | PS-B-0014 | AF-1414, AF-1419, AF-1420, AF-1422, AF-1423 | GP-3304, GP-3305, GP-3306, GP-3307, GP-3308, GP-3309, GP-3311 | core | plan D03 T14 §2 | extends D03 T05 §1 preview |
| IP-1020 | Filters on masks, spare channels, adjustment, fill, and live filter layers | -- | AF-1408, AF-1409 | -- | core | plan D03 T14 §2 | extends D03 T05 §1 |
| IP-1021 | Fade last filter with amount and blend mode | PS-B-0017 | AF-1426, AF-1427, AF-1428 | -- | core | plan D03 T14 §2 |  |
| IP-1022 | Drag on canvas to set filter strength beyond the slider maximum | -- | AF-1410 | -- | core | plan D03 T14 §2 | On-canvas control descriptors from D01 T06 §1 |
| IP-1023 | Render, Light and Shadow, and Lighting/Tonal filter submenus | -- | AF-1390 | GP-2518, GP-2908 | core | plan D03 T14 §2 | Menu grouping only |
| IP-1024 | Common filter behaviors: merge filter destructively, return to previous tool, auto alpha for effects that need it | -- | -- | GP-0005, GP-0073, GP-0076 | core | plan D03 T14 §2 | Non-destructive filter stack itself is D03 T14 §1 |
| IP-1025 | Fade last operation | -- | AF-0955 | -- | core | plan D03 T14 §2 |  |
| IP-1026 | Auto commit an open filter dialog when another operation starts | -- | AF-2697 | -- | core | plan D03 T14 §2 |  |
| IP-1027 | Filter Gallery dialog: preview, categories, thumbnails, filter menu, zoom | PS-B-0003, PS-B-0031, PS-B-0032, PS-B-0033, PS-B-0034, PS-B-0040 | -- | -- | core | plan D03 T14 §3 |  |
| IP-1028 | Filter Gallery effect layer stack: new, delete, reorder, hide | PS-B-0035, PS-B-0036, PS-B-0037, PS-B-0038, PS-B-0039 | -- | -- | core | plan D03 T14 §3 |  |
| IP-1029 | Show all Filter Gallery groups and names in the Filter menu | PS-B-0135 | -- | -- | core | plan D03 T14 §3 | Preference lives in D03 T20 §4 |
| IP-1030 | GEGL Operation tool: pick any engine op, generated settings, preview, reset | -- | -- | GP-0132, GP-0133, GP-0134, GP-0135, GP-0136, GP-0137, GP-0138 | core | plan D03 T14 §8 |  |
| IP-1031 | GEGL filter browser searchable by name, title, description | -- | -- | GP-3338, GP-3339, GP-3340, GP-3341 | automation | plan D03 T14 §8 |  |
| IP-1032 | Filter applies to the selection or the whole active layer, with apply, cancel, and progress | PS-B-0013, PS-B-0015 | AF-1391, AF-1407, AF-1415, AF-1416 | -- | core | shipped-scope D03 T05 §1 |  |
| IP-1033 | Photoshop 64-bit plug-in filters | -- | AF-2605 | -- | format | plan D03 T14 §11 |  |
| IP-1034 | Digimarc watermark filters | PS-B-0334 | -- | -- | core | excluded: removed | Removed by Adobe; listed only as removed |
| IP-2368 | Smart brushing on filter and adjustment brushes: restrict strokes to pixels similar in color, brightness, or both within a tolerance, Shift to override | -- | -- | -- | core | plan D03 T14 §1 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1266; AC-2659 to AC-2664); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T14 §1 |

## Blur, sharpen, and noise filters

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1035 | Median with neighborhood shape, percentile, alpha percentile, high precision | PS-B-0230, PS-B-0231 | AF-1491, AF-1492, AF-1493 | GP-2034, GP-2035, GP-2036, GP-2037, GP-2038, GP-2039, GP-2040, GP-2041, GP-2042, GP-3423 | core | plan D01 T06 §2 | extends D03 T07 §3 |
| IP-1036 | Average | PS-B-0136 | AF-1432, AF-1433 | -- | core | plan D01 T06 §2 |  |
| IP-1037 | Blur and blur more | PS-B-0137, PS-B-0138 | -- | -- | core | plan D01 T06 §2 |  |
| IP-1038 | Shape blur with custom shape kernel | PS-B-0157, PS-B-0158 | -- | -- | core | plan D01 T06 §2 | Shape presets shared with D03 T16 §7 custom shapes |
| IP-1039 | Bilateral blur: radius and tolerance | -- | AF-1434, AF-1435, AF-1436, AF-1437 | -- | core | plan D01 T06 §2 |  |
| IP-1040 | Selective gaussian blur with max delta | -- | -- | GP-2012, GP-2013, GP-2014, GP-2015, GP-3397 | core | plan D01 T06 §2 |  |
| IP-1041 | Mean curvature blur | -- | -- | GP-2032, GP-2033, GP-3422 | core | plan D01 T06 §2 |  |
| IP-1042 | Variable blur by mask | -- | -- | GP-2066, GP-2067, GP-2068, GP-2069, GP-2070, GP-3498 | core | plan D01 T06 §2 |  |
| IP-1043 | Tileable blur | -- | -- | GP-2071, GP-2072, GP-2073, GP-2074, GP-2075 | core | plan D01 T06 §2 |  |
| IP-1044 | Circular (spin) motion blur with on-canvas center | -- | AF-1508, AF-1509, AF-1510, AF-1511 | GP-2043, GP-2044, GP-2045, GP-2046, GP-2047, GP-3428 | core | plan D01 T06 §2 | On-canvas center via D03 T14 §2 |
| IP-1045 | Zoom motion blur with on-canvas origin | -- | AF-1512, AF-1513, AF-1514, AF-1515 | GP-2052, GP-2053, GP-2054, GP-2055, GP-2056, GP-3430 | core | plan D01 T06 §2 | On-canvas origin via D03 T14 §2 |
| IP-1046 | Custom blur: matrix, divisor, offset, normalize | -- | AF-1447, AF-1448, AF-1449, AF-1450, AF-1451 | -- | core | plan D01 T06 §2 |  |
| IP-1047 | Maximum blur with circular option | -- | AF-1487, AF-1488, AF-1489, AF-1490 | -- | core | plan D01 T06 §2 | extends D01 T03 §6 maximum |
| IP-1048 | Minimum blur with circular option | -- | AF-1494, AF-1495, AF-1496, AF-1497 | -- | core | plan D01 T06 §2 | extends D01 T03 §6 minimum |
| IP-1049 | Diffuse (edge noise) | -- | AF-1673, AF-1674 | -- | core | plan D01 T06 §2 |  |
| IP-1050 | Diffuse (Affinity) with intensity | -- | AF-1675 | -- | core | plan D01 T06 §2 |  |
| IP-1051 | Bilateral filter | -- | -- | GP-3351 | core | plan D01 T06 §2 |  |
| IP-1052 | Smooth by domain transform (edge-preserving smoothing) | -- | -- | GP-3381 | core | plan D01 T06 §2 | Sits beside bilateral blur |
| IP-1053 | Lens blur: depth map, iris shape, blades, curvature, specular bloom, noise | PS-B-0144, PS-B-0145, PS-B-0146, PS-B-0147, PS-B-0148, PS-B-0149, PS-B-0150, PS-B-0151, PS-B-0152 | AF-1479, AF-1480, AF-1481, AF-1482, AF-1483, AF-1484, AF-1485, AF-1486 | GP-2025, GP-2026, GP-2027, GP-2028, GP-2029, GP-2030, GP-2031, GP-3408 | core | plan D01 T06 §3 | Depth map from alpha, mask, or channel; AI depth via D03 T19 §7 |
| IP-1054 | Focus blur: shape, blur type, highlights, on-canvas geometry | -- | -- | GP-1996, GP-1997, GP-1998, GP-1999, GP-2000, GP-2001, GP-2002, GP-2003, GP-2004, GP-2005, GP-2006, GP-2007, GP-2008, GP-2009, GP-2010, GP-2011, GP-3392 | core | plan D01 T06 §3 | On-canvas controls via D03 T14 §2 |
| IP-1055 | Depth of field blur: elliptical and tilt-shift with vibrance and clarity | -- | AF-1452, AF-1453, AF-1454, AF-1455, AF-1456, AF-1457, AF-1458, AF-1459, AF-1460, AF-1461, AF-1462 | -- | core | plan D01 T06 §3 | On-canvas handles via D03 T14 §4 |
| IP-1056 | Clarity (local contrast) | -- | AF-1521, AF-1522, AF-1523 | -- | core | plan D01 T06 §4 |  |
| IP-1057 | Texture (midtone micro-contrast) | -- | AF-1524, AF-1525 | -- | core | plan D01 T06 §4 |  |
| IP-1058 | Multi-band sharpen | -- | AF-1531, AF-1532, AF-1533 | -- | core | plan D01 T06 §4 |  |
| IP-1059 | Texture (micro-contrast) filter | -- | AF-1526 | -- | core | plan D01 T06 §4 | Affinity Texture filter, detail enhancement family |
| IP-1060 | Sharpen edges and sharpen more | PS-B-0293, PS-B-0294 | -- | -- | core | plan D01 T06 §4 | extends D01 T03 §6 |
| IP-1061 | Smart sharpen removal modes, shadow and highlight fade, presets, legacy mode | PS-B-0297, PS-B-0298, PS-B-0299 | -- | -- | core | plan D01 T06 §4 | extends D03 T07 §3 |
| IP-1062 | Shake reduction: blur trace estimation, source noise, smoothing, artifact suppression | PS-B-0284, PS-B-0285, PS-B-0286, PS-B-0287 | -- | -- | core | plan D01 T06 §4 |  |
| IP-1063 | Shake reduction workspace: multiple blur traces, blur direction tool, detail loupe, save and load traces | PS-B-0288, PS-B-0289, PS-B-0290, PS-B-0291 | -- | -- | core | plan D03 T14 §2 | dialog over the D01 T06 §4 deconvolution |
| IP-1064 | Destripe: width, histogram | -- | -- | GP-1761, GP-1762, GP-1763, GP-1764 | core | plan D01 T06 §5 | Scanner stripe removal |
| IP-1065 | Wavelet denoise brush tool | -- | AF-2169 | -- | core | plan D03 T14 §1 | the filter brush paints the D01 T06 §5 wavelet denoise through a mask |
| IP-1066 | Reduce noise: luminance and color strength, preserve details, per channel, JPEG artifact removal, saved settings | PS-B-0232, PS-B-0233, PS-B-0234, PS-B-0235, PS-B-0236 | AF-1666, AF-1667, AF-1668, AF-1669, AF-1670, AF-1671, AF-1672 | -- | core | plan D01 T06 §5 | extends D03 T07 §3; Affinity Denoise merged |
| IP-1067 | Despeckle: adaptive, recursive, black and white levels | PS-B-0227 | -- | GP-2397, GP-2398, GP-2399, GP-2400, GP-2401, GP-2402, GP-2403, GP-2404, GP-2405, GP-2406 | core | plan D01 T06 §5 |  |
| IP-1068 | Noise reduction (anisotropic smoothing) | -- | -- | GP-2386, GP-2387, GP-3438 | core | plan D01 T06 §5 |  |
| IP-1069 | Symmetric nearest neighbor | -- | -- | GP-2390, GP-2391, GP-2392, GP-3472 | core | plan D01 T06 §5 |  |
| IP-1070 | NL filter: alpha trimmed mean, optimal estimation, edge enhancement | -- | -- | GP-2407, GP-2408, GP-2409, GP-2410, GP-2411, GP-2412, GP-2413, GP-2414, GP-2415, GP-2416 | core | plan D01 T06 §5 | Non-linear pnmnlfilt modes, not NL-means |
| IP-1071 | Denoise DCT | -- | -- | GP-3374 | core | plan D01 T06 §5 |  |
| IP-1072 | Wavelet denoise: luminance and chroma per scale | -- | AF-1700, AF-1701, AF-1702, AF-1703 | -- | core | plan D01 T06 §5 |  |
| IP-1073 | Wavelet decompose into scale layers | -- | -- | GP-2417, GP-2418, GP-2419, GP-2420, GP-3504, GP-3505 | core | plan D01 T06 §5 |  |
| IP-1074 | CIE LCh noise | -- | -- | GP-2863, GP-2864, GP-2865, GP-2866, GP-2867, GP-2868, GP-2869, GP-3434 | core | plan D01 T06 §5 |  |
| IP-1075 | HSV noise | -- | -- | GP-2870, GP-2871, GP-2872, GP-2873, GP-2874, GP-2875, GP-2876, GP-3435 | core | plan D01 T06 §5 |  |
| IP-1076 | Hurl | -- | -- | GP-2877, GP-2878, GP-2879, GP-2880, GP-2881, GP-3436 | core | plan D01 T06 §5 |  |
| IP-1077 | Pick | -- | -- | GP-2882, GP-2883, GP-2884, GP-2885, GP-2886, GP-3437 | core | plan D01 T06 §5 |  |
| IP-1078 | RGB noise: independent, correlated, gaussian | -- | -- | GP-2887, GP-2888, GP-2889, GP-2890, GP-2891, GP-2892, GP-2893, GP-2894, GP-2895, GP-2896, GP-2897, GP-3439 | core | plan D01 T06 §5 |  |
| IP-1079 | Slur | -- | -- | GP-2898, GP-2899, GP-2900, GP-2901, GP-2902, GP-3440 | core | plan D01 T06 §5 |  |
| IP-1080 | Spread | -- | -- | GP-2903, GP-2904, GP-2905, GP-2906, GP-2907, GP-3442 | core | plan D01 T06 §5 |  |
| IP-1081 | Field blur with multiple pins | PS-B-0163, PS-B-0170 | AF-1469, AF-1470, AF-1471, AF-1472, AF-1473, AF-1474 | -- | core | plan D03 T14 §4 | Kernel D01 T06 §3 |
| IP-1082 | Iris blur: ellipse, roundness, feather handles | PS-B-0164, PS-B-0171, PS-B-0172 | -- | -- | core | plan D03 T14 §4 | Kernel D01 T06 §3 |
| IP-1083 | Tilt-shift: focus and feather lines, distortion, symmetric distortion | PS-B-0165, PS-B-0173, PS-B-0174, PS-B-0175, PS-B-0176 | -- | -- | core | plan D03 T14 §4 | Kernel D01 T06 §3 |
| IP-1084 | Path blur: speed, taper, centered, rear sync flash, strobe, end point shapes | PS-B-0166, PS-B-0177, PS-B-0178, PS-B-0179, PS-B-0180, PS-B-0181, PS-B-0182, PS-B-0183 | -- | -- | core | plan D03 T14 §4 | Kernel D01 T06 §3 |
| IP-1085 | Spin blur: angle, strobe, movable pivot | PS-B-0167, PS-B-0184, PS-B-0185, PS-B-0186, PS-B-0190 | -- | -- | core | plan D03 T14 §4 | Kernel D01 T06 §3; motion effects strobe shared with path blur |
| IP-1086 | Blur Gallery pins, blur ring, focus, remove all pins, preview | PS-B-0168, PS-B-0169, PS-B-0194, PS-B-0197, PS-B-0198 | -- | -- | core | plan D03 T14 §4 |  |
| IP-1087 | Blur Gallery effects: light bokeh, bokeh color, light range | PS-B-0187, PS-B-0188, PS-B-0189 | -- | -- | core | plan D03 T14 §4 | Kernel D01 T06 §3 |
| IP-1088 | Blur Gallery noise panel: grain type, amount, size, roughness, color, highlights | PS-B-0191, PS-B-0192 | -- | -- | core | plan D03 T14 §4 |  |
| IP-1089 | Blur Gallery output: selection bleed, save mask to channels, high quality, smart filter | PS-B-0193, PS-B-0195, PS-B-0196, PS-B-0199 | -- | -- | core | plan D03 T14 §4 | Smart filter hosting via D03 T14 §1 |
| IP-1090 | Deinterlace: keep even or odd fields | -- | AF-1664, AF-1665 | GP-2379, GP-2380, GP-2381, GP-2382, GP-3373 | video | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1091 | JPEG artifact removal with low, medium, high strength | PS-B-0446, PS-B-0447 | -- | -- | ai | shipped-scope D01 T03 §6 | Imago menu and dialog: D03 T14 §2; AI variant through D03 T19 §8 |
| IP-1092 | Radial blur: spin or zoom with quality and center | PS-B-0155, PS-B-0156 | -- | -- | core | shipped-scope D01 T03 §6 | Imago menu and dialog: D03 T14 §2 |
| IP-1093 | Smart blur: radius, threshold, quality, normal, edge only, overlay edge | PS-B-0159, PS-B-0160 | -- | -- | core | shipped-scope D01 T03 §6 | Imago menu and dialog: D03 T14 §2 |
| IP-1094 | High pass with monochrome and contrast options | -- | AF-1527, AF-1528, AF-1529, AF-1530 | GP-2383, GP-2384, GP-2385, GP-3401 | core | shipped-scope D01 T03 §6 | Imago menu and dialog: D03 T14 §2 |
| IP-1095 | Sharpen | PS-B-0292 | -- | -- | core | shipped-scope D01 T03 §6 | Imago menu and dialog: D03 T14 §2 |
| IP-1096 | High pass | PS-B-0324, PS-B-0325 | -- | -- | core | shipped-scope D01 T03 §6 | Imago menu and dialog: D03 T14 §2 |
| IP-1097 | Gaussian blur | PS-B-0141, PS-B-0142, PS-B-0143 | AF-1475, AF-1476, AF-1477, AF-1478 | GP-2016, GP-2017, GP-2018, GP-2019, GP-2020, GP-2021, GP-2022, GP-2023, GP-2024, GP-3396, GP-3398 | core | shipped-scope D03 T05 §3 | Separate X and Y size, IIR or FIR, abyss policy via D01 T06 §1 contract; live GPU preview |
| IP-1098 | Box blur | PS-B-0139, PS-B-0140 | AF-1444, AF-1445, AF-1446 | GP-3353 | core | shipped-scope D03 T05 §3 |  |
| IP-1099 | Unsharp mask | -- | AF-1516, AF-1517, AF-1518, AF-1519, AF-1520 | GP-2393, GP-2394, GP-2395, GP-2396, GP-3495 | core | shipped-scope D03 T05 §3 |  |
| IP-1100 | Unsharp mask | PS-B-0300, PS-B-0301 | -- | -- | core | shipped-scope D03 T05 §3 |  |
| IP-1101 | Motion blur (linear) with on-canvas angle and length | PS-B-0153, PS-B-0154 | AF-1498, AF-1499, AF-1500, AF-1501 | GP-2048, GP-2049, GP-2050, GP-2051, GP-3429 | core | shipped-scope D03 T07 §3 | On-canvas controls via D03 T14 §2 |
| IP-1102 | Surface blur | PS-B-0161, PS-B-0162 | -- | -- | core | shipped-scope D03 T07 §3 |  |
| IP-1103 | Add noise: amount, uniform or gaussian, monochromatic | PS-B-0225, PS-B-0226 | AF-1658, AF-1659, AF-1660, AF-1661, AF-1662, AF-1663 | -- | core | shipped-scope D03 T07 §3 |  |
| IP-1104 | Dust and scratches with per-channel tolerance | PS-B-0228, PS-B-0229 | AF-1676, AF-1677, AF-1678, AF-1679, AF-1680 | -- | core | shipped-scope D03 T07 §3 | Affinity channel tolerance is one more option on the shipped filter |
| IP-1105 | Smart sharpen: amount, radius, reduce noise | PS-B-0295, PS-B-0296 | -- | -- | core | shipped-scope D03 T07 §3 |  |
| IP-1106 | Blur Gallery on video layers | PS-B-0200 | -- | -- | video | backlog B-043 |  |

## Distort, map, and pixelate filters

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1107 | Twirl with radius and on-canvas origin | PS-B-0216, PS-B-0217 | AF-1653, AF-1654, AF-1655, AF-1656, AF-1657 | -- | core | plan D01 T06 §6 | extends D03 T07 §3 |
| IP-1108 | Pinch and punch with radius and on-canvas origin | PS-B-0205, PS-B-0206 | AF-1631, AF-1632, AF-1633, AF-1634, AF-1635 | -- | core | plan D01 T06 §6 | extends D03 T07 §3 |
| IP-1109 | Spherize: amount, modes, radius, angle of view, curvature, origin | PS-B-0214, PS-B-0215 | AF-1648, AF-1649, AF-1650, AF-1651, AF-1652 | GP-2265, GP-2266, GP-2267, GP-2268, GP-2269, GP-2270, GP-2271, GP-2272, GP-2273, GP-3475 | core | plan D01 T06 §6 | extends D03 T07 §3 |
| IP-1110 | Ripple: amount, size, amplitude, period, phase, angle, wave type, tileable, origin | PS-B-0209, PS-B-0210 | AF-1641, AF-1642, AF-1643, AF-1644 | GP-2250, GP-2251, GP-2252, GP-2253, GP-2254, GP-2255, GP-2256, GP-2257, GP-2258, GP-2259, GP-3461 | core | plan D01 T06 §6 | extends D03 T07 §3 |
| IP-1111 | Polar coordinates: both directions, circle depth, offset angle, map backwards, from top | PS-B-0207, PS-B-0208 | AF-1639, AF-1640 | GP-2241, GP-2242, GP-2243, GP-2244, GP-2245, GP-2246, GP-2247, GP-2248, GP-2249, GP-3453 | core | plan D01 T06 §6 | extends D03 T07 §3 |
| IP-1112 | ZigZag: amount, ridges, style | PS-B-0223, PS-B-0224 | -- | -- | core | plan D01 T06 §6 | extends D01 T03 §7 |
| IP-1113 | Lens distortion: main, edge, zoom, shift, brighten, on-canvas origin | -- | AF-1596, AF-1597, AF-1598, AF-1599 | GP-2196, GP-2197, GP-2198, GP-2199, GP-2200, GP-2201, GP-2202, GP-2203, GP-3409 | core | plan D01 T06 §6 | extends D01 T03 §2 |
| IP-1114 | Apply lens: refraction index, keep surroundings | -- | -- | GP-2168, GP-2169, GP-2170, GP-2171, GP-3348 | core | plan D01 T06 §6 |  |
| IP-1115 | Affine filter: rotation, scale, offset, extend modes | -- | AF-1538, AF-1539, AF-1540, AF-1541, AF-1542, AF-1543, AF-1544, AF-1545, AF-1546 | -- | core | plan D01 T06 §6 |  |
| IP-1116 | Deform filter with anchor points and rigid or similarity constraints | -- | AF-1560, AF-1561, AF-1562, AF-1563, AF-1564, AF-1565, AF-1566 | -- | core | plan D01 T06 §6 |  |
| IP-1117 | Glitch | -- | AF-1587, AF-1588 | -- | core | plan D01 T06 §6 |  |
| IP-1118 | Mesh warp filter: source and destination modes, node types, resampling | -- | AF-1606, AF-1607, AF-1608, AF-1609, AF-1610, AF-1611, AF-1612, AF-1613, AF-1614, AF-1615 | -- | core | plan D01 T06 §6 | extends D01 T03 §7; mesh editing surface shared with D03 T13 §6 |
| IP-1119 | Kaleidoscope and mirrors: mirror count, rotations, offsets, trim, zoom, expand | -- | AF-1616, AF-1617, AF-1618, AF-1619, AF-1620 | GP-2182, GP-2183, GP-2184, GP-2185, GP-2186, GP-2187, GP-2188, GP-2189, GP-2190, GP-2191, GP-2192, GP-2193, GP-2194, GP-2195, GP-3424 | core | plan D01 T06 §6 |  |
| IP-1120 | Shift rows or columns randomly | -- | -- | GP-2260, GP-2261, GP-2262, GP-2263, GP-2264, GP-3468 | core | plan D01 T06 §6 |  |
| IP-1121 | Value propagate | -- | -- | GP-2274, GP-2275, GP-2276, GP-2277, GP-2278, GP-2279, GP-2280, GP-2281, GP-2282, GP-2283, GP-2284, GP-2285, GP-2286, GP-2287, GP-2288, GP-2289, GP-2290, GP-2291, GP-3497 | core | plan D01 T06 §6 |  |
| IP-1122 | Video degradation | -- | -- | GP-2292, GP-2293, GP-2294, GP-2295 | core | plan D01 T06 §6 |  |
| IP-1123 | Waves (concentric) | -- | -- | GP-2296, GP-2297, GP-2298, GP-2299, GP-2300, GP-2301, GP-2302, GP-2303, GP-2304, GP-3506 | core | plan D01 T06 §6 |  |
| IP-1124 | Whirl and pinch | -- | -- | GP-2305, GP-2306, GP-2307, GP-2308, GP-3508 | core | plan D01 T06 §6 |  |
| IP-1125 | Curve bend with upper and lower curves | -- | -- | GP-2328, GP-2329, GP-2330, GP-2331, GP-2332, GP-2333, GP-2334, GP-2335, GP-2336, GP-2337, GP-2338, GP-2339, GP-2340, GP-2341, GP-2342, GP-2343, GP-2344, GP-2345, GP-2346 | core | plan D01 T06 §6 |  |
| IP-1126 | Blinds | -- | -- | GP-2322, GP-2323, GP-2324, GP-2325, GP-2326, GP-2327 | core | plan D01 T06 §6 | Blinds not named; closest distort extension section |
| IP-1127 | Little planet (stereographic projection) | -- | -- | GP-2754, GP-2755, GP-2756, GP-2757, GP-2758, GP-2759, GP-2760, GP-3477 | core | plan D01 T06 §6 |  |
| IP-1128 | Panorama projection | -- | -- | GP-2761, GP-3447 | core | plan D01 T06 §6 |  |
| IP-1129 | Recursive transform | -- | -- | GP-2762, GP-2763, GP-2764, GP-2765, GP-2766, GP-2767, GP-2768, GP-2769, GP-2770, GP-2771 | core | plan D01 T06 §6 |  |
| IP-1130 | Glitch filter with effect types, stackable | -- | AF-1589, AF-1590 | -- | core | plan D01 T06 §6 |  |
| IP-1131 | Recursive transform | -- | -- | GP-3456 | core | plan D01 T06 §6 |  |
| IP-1132 | Video degradation | -- | -- | GP-3499 | core | plan D01 T06 §6 |  |
| IP-1133 | Displace: map file or layers beneath, scale, stretch or tile, load methods, cartesian and polar modes, edge handling | PS-B-0201, PS-B-0202, PS-B-0203, PS-B-0204 | AF-1568, AF-1569, AF-1570, AF-1571, AF-1572, AF-1573, AF-1574, AF-1575, AF-1576 | GP-2726, GP-2727, GP-2728, GP-2729, GP-2730, GP-2731, GP-2732, GP-2733, GP-2734, GP-2735, GP-2736, GP-2737, GP-2738, GP-2739, GP-3377 | core | plan D01 T06 §7 | extends D03 T07 §3 |
| IP-1134 | Map absolute and map relative sampling ops | -- | -- | GP-3417, GP-3418 | core | plan D01 T06 §7 | GEGL op-id map in D01 T06 §1 |
| IP-1135 | Bump map: map image, azimuth, elevation, depth, offsets, waterlevel, ambient | -- | -- | GP-2710, GP-2711, GP-2712, GP-2713, GP-2714, GP-2715, GP-2716, GP-2717, GP-2718, GP-2719, GP-2720, GP-2721, GP-2722, GP-2723, GP-2724, GP-2725, GP-3355 | core | plan D01 T06 §7 | extends D01 T03 §11 |
| IP-1136 | Engrave | -- | -- | GP-2179, GP-2180, GP-2181 | core | plan D01 T06 §7 |  |
| IP-1137 | Fractal trace | -- | -- | GP-2740, GP-2741, GP-2742, GP-2743, GP-2744, GP-2745, GP-2746, GP-2747, GP-2748, GP-2749, GP-2750 | core | plan D01 T06 §7 |  |
| IP-1138 | Illusion | -- | -- | GP-2751, GP-2752, GP-2753 | core | plan D01 T06 §7 |  |
| IP-1139 | Paper tile | -- | -- | GP-2772, GP-2773, GP-2774, GP-2775, GP-2776, GP-2777, GP-2778, GP-2779, GP-2780, GP-2781, GP-2782, GP-2783, GP-2784, GP-2785, GP-2786, GP-2787, GP-2788, GP-3492 | core | plan D01 T06 §7 |  |
| IP-1140 | Tile seamless | -- | -- | GP-2789, GP-3493 | core | plan D01 T06 §7 |  |
| IP-1141 | Map object: plane, sphere, box, cylinder with lights, material, viewpoint, orientation | -- | -- | GP-2790, GP-2791, GP-2792, GP-2793, GP-2794, GP-2795, GP-2796, GP-2797, GP-2798, GP-2799, GP-2800, GP-2801, GP-2802, GP-2803, GP-2804, GP-2805, GP-2806, GP-2807, GP-2808, GP-2809, GP-2810, GP-2811, GP-2812, GP-2813, GP-2814, GP-2815, GP-2816, GP-2817, GP-2818, GP-2819, GP-2820, GP-2821, GP-2822, GP-2823, GP-2824, GP-2825, GP-2826, GP-2827, GP-2828, GP-2829, GP-2830, GP-2831, GP-2832, GP-2833, GP-2834 | core | plan D01 T06 §7 | Box face and cylinder cap images; preview with wireframe |
| IP-1142 | Small tiles | -- | -- | GP-2835, GP-2836, GP-2837, GP-2838, GP-2839, GP-2840, GP-2841 | core | plan D01 T06 §7 |  |
| IP-1143 | Tile (repeat to a new size) | -- | -- | GP-2842, GP-2843, GP-2844, GP-2845, GP-3490 | core | plan D01 T06 §7 | GIMP Tile not named; closest map extension section |
| IP-1144 | Warp (map warp by displacement iterations) | -- | -- | GP-2846, GP-2847, GP-2848, GP-2849, GP-2850, GP-2851, GP-2852, GP-2853, GP-2854, GP-2855, GP-2856, GP-2857, GP-2858, GP-2859, GP-2860, GP-2861, GP-3501 | core | plan D01 T06 §7 |  |
| IP-1145 | Tile glass | -- | -- | GP-3491 | core | plan D01 T06 §7 |  |
| IP-1146 | Engrave | -- | -- | GP-3388 | core | plan D01 T06 §7 |  |
| IP-1147 | Illusion | -- | -- | GP-3403 | core | plan D01 T06 §7 |  |
| IP-1148 | Fractal trace | -- | -- | GP-3394 | core | plan D01 T06 §7 | GEGL gegl:fractal-trace |
| IP-1149 | Sphere designer: textured, bump-mapped, lit sphere with saved designs | -- | -- | GP-3181, GP-3182, GP-3183, GP-3184, GP-3185, GP-3186, GP-3187, GP-3188, GP-3189, GP-3190, GP-3191, GP-3192, GP-3193, GP-3194, GP-3195, GP-3196, GP-3197, GP-3198, GP-3199, GP-3200, GP-3201, GP-3202, GP-3203, GP-3204, GP-3205, GP-3206 | core | plan D01 T06 §7 | Sphere Designer not named; closest map object sphere with lighting and materials |
| IP-1150 | Pixelize and mosaic: block size, shapes (square, diamond, round, triangle), offset, size ratio | PS-B-0245, PS-B-0246 | AF-1636, AF-1637, AF-1638 | GP-2057, GP-2058, GP-2059, GP-2060, GP-2061, GP-2062, GP-2063, GP-2064, GP-2065, GP-3451 | core | plan D01 T06 §14 | extends D01 T03 §7 |
| IP-1151 | Mezzotint types | PS-B-0243, PS-B-0244 | -- | -- | core | plan D01 T06 §14 | extends D01 T03 §11 |
| IP-1152 | Facet | PS-B-0241 | -- | -- | core | plan D01 T06 §14 |  |
| IP-1153 | Fragment | PS-B-0242 | -- | -- | core | plan D01 T06 §14 |  |
| IP-1154 | Pointillize | PS-B-0247, PS-B-0248 | -- | -- | core | plan D01 T06 §14 |  |
| IP-1155 | Mosaic tiles (GIMP): geometry, size, height, neatness, spacing, joints, light | -- | -- | GP-2204, GP-2205, GP-2206, GP-2207, GP-2208, GP-2209, GP-2210, GP-2211, GP-2212, GP-2213, GP-2214, GP-2215, GP-2216, GP-2217, GP-2218, GP-2219, GP-2220, GP-2221, GP-2222, GP-2223, GP-3427 | core | plan D01 T06 §14 |  |
| IP-1156 | Newsprint halftoning: color models, per-ink pattern, period, angle, black pullout, effects | -- | -- | GP-2224, GP-2225, GP-2226, GP-2227, GP-2228, GP-2229, GP-2230, GP-2231, GP-2232, GP-2233, GP-2234, GP-2235, GP-2236, GP-2237, GP-2238, GP-2239, GP-2240 | core | plan D01 T06 §14 |  |
| IP-1157 | Halftone: screen types, dot shape, cell size, angle, GCR and UCR | -- | AF-1733, AF-1734, AF-1735, AF-1736, AF-1737, AF-1738, AF-1739, AF-1740, AF-1741 | -- | core | plan D01 T06 §14 |  |
| IP-1158 | Newsprint halftoning | -- | -- | GP-3433 | core | plan D01 T06 §14 |  |
| IP-1159 | Perspective filter: single or dual plane, source and destination modes, autoclip | -- | AF-1621, AF-1622, AF-1623, AF-1624, AF-1625, AF-1626, AF-1627, AF-1628, AF-1629, AF-1630 | -- | core | plan D03 T14 §6 | Affinity perspective filter; engine D01 T06 §6 |
| IP-1160 | Lens correction: auto correction from lens profiles (distortion, aberration, vignette, auto scale, edge fill, profile search) | PS-B-0353, PS-B-0354, PS-B-0355, PS-B-0356, PS-B-0357, PS-B-0358, PS-B-0359, PS-B-0360 | AF-1591, AF-1592, AF-1593, AF-1594, AF-1595 | -- | core | plan D03 T14 §6 | Profiles from an open lens database, auto by EXIF; no online Adobe profile search |
| IP-1161 | Lens correction: custom distortion, fringe, vignette, perspective, angle, scale, saved settings | PS-B-0361, PS-B-0362, PS-B-0363, PS-B-0364, PS-B-0365, PS-B-0366, PS-B-0367, PS-B-0368 | -- | -- | core | plan D03 T14 §6 | Engine D01 T03 §2 |
| IP-1162 | Lens correction dialog tools: remove distortion, straighten, move grid, grid overlay, preview | PS-B-0369, PS-B-0370, PS-B-0371, PS-B-0372, PS-B-0373 | -- | -- | core | plan D03 T14 §6 |  |
| IP-1163 | Chromatic aberration removal | -- | AF-1713, AF-1714 | -- | core | plan D03 T14 §6 | Engine D01 T07 §3 |
| IP-1164 | Defringe: fringe color, complementary hue, tolerance, radius, edge threshold | -- | AF-1718, AF-1719, AF-1720, AF-1721, AF-1722, AF-1723, AF-1724 | -- | core | plan D03 T14 §6 | Engine D01 T07 §3 |
| IP-1165 | Adaptive wide angle: constraint and polygon constraint tools, orientation, detail loupe | PS-B-0337, PS-B-0338, PS-B-0349, PS-B-0350 | -- | -- | core | plan D03 T14 §6 |  |
| IP-1166 | Adaptive wide angle corrections: fisheye, perspective, full spherical, auto, scale, focal length, as shot | PS-B-0342, PS-B-0343, PS-B-0344, PS-B-0345, PS-B-0346, PS-B-0347, PS-B-0348 | -- | -- | core | plan D03 T14 §6 |  |
| IP-1167 | Adaptive wide angle: move, hand, zoom, show constraints and mesh, save and load constraints | PS-B-0339, PS-B-0340, PS-B-0341, PS-B-0351, PS-B-0352 | -- | -- | core | plan D03 T14 §6 |  |
| IP-1168 | Adaptive Wide Angle filter | PS-B-0004 | -- | -- | core | plan D03 T14 §6 |  |
| IP-1169 | Lens Correction filter | PS-B-0006 | -- | -- | core | plan D03 T14 §6 | Engine D01 T03 §2 |
| IP-1170 | Remove vignette | -- | AF-1750 | -- | core | plan D03 T14 §6 | Automatic lens vignetting removal |
| IP-1171 | Lens profile import (Lensfun XML, Adobe LCP) | -- | AF-2642 | -- | format | plan D03 T14 §6 |  |
| IP-1172 | Lens Correction on many files with profile matching, corrections, edge fill, auto scale | PS-B-0727, PS-B-0728 | -- | -- | automation | plan D03 T14 §6 | runs over a file list, not the batch engine |
| IP-1173 | Vanishing Point planes: create, edit, grid size, angle, color coding, saved with document | PS-B-0406, PS-B-0407, PS-B-0414, PS-B-0415, PS-B-0416, PS-B-0417, PS-B-0428 | -- | -- | core | plan D03 T14 §7 |  |
| IP-1174 | Vanishing Point marquee, transform, move mode, heal, paste into plane | PS-B-0408, PS-B-0411, PS-B-0418, PS-B-0419, PS-B-0427 | -- | -- | core | plan D03 T14 §7 |  |
| IP-1175 | Vanishing Point stamp and brush with heal, aligned, eyedropper | PS-B-0409, PS-B-0410, PS-B-0412, PS-B-0420, PS-B-0421 | -- | -- | core | plan D03 T14 §7 |  |
| IP-1176 | Vanishing Point measure, show edges, render grids and measurements | PS-B-0413, PS-B-0422, PS-B-0423, PS-B-0424 | -- | -- | core | plan D03 T14 §7 |  |
| IP-1177 | Vanishing Point filter command | PS-B-0009 | -- | -- | core | plan D03 T14 §7 |  |
| IP-1178 | Equirectangular live projection editing | -- | AF-1009, AF-1010, AF-1011, AF-1012, AF-1013, AF-1014 | -- | core | plan D03 T14 §7 | 360 live projection editing, closest is plane-based perspective editing |
| IP-1179 | Perspective live projection with planes | -- | AF-1015, AF-1016, AF-1017 | -- | core | plan D03 T14 §7 | (Affinity) flatten planes to edit then reproject |
| IP-1180 | Vanishing Point | PS-A-1454 | -- | -- | core | plan D03 T14 §7 |  |
| IP-1181 | Crystallize | PS-B-0239, PS-B-0240 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1182 | Color halftone: max radius and per-channel screen angles | PS-B-0237, PS-B-0238 | -- | -- | core | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1183 | Shear with horizontal and vertical curve graphs and edge handling | PS-B-0211, PS-B-0212, PS-B-0213 | AF-1645, AF-1646, AF-1647 | -- | core | shipped-scope D01 T03 §7 | Imago menu and dialog: D03 T14 §2 |
| IP-1184 | Page curl | -- | -- | GP-2347, GP-2348, GP-2349, GP-2350, GP-2351, GP-2352 | core | shipped-scope D01 T03 §7 | Imago menu and dialog: D03 T14 §2 |
| IP-1185 | Wind: wind or blast style, direction, edge, threshold, strength | -- | -- | GP-2309, GP-2310, GP-2311, GP-2312, GP-2313, GP-2314, GP-2315, GP-2316, GP-2317, GP-2318, GP-2319, GP-2320, GP-2321, GP-3509 | core | shipped-scope D01 T03 §7 | Imago menu and dialog: D03 T14 §2 |
| IP-1186 | Diffuse glow | -- | AF-1463, AF-1464 | -- | core | shipped-scope D01 T03 §7 | Imago menu and dialog: D03 T14 §2 |
| IP-1187 | Glass (Filter Gallery) with textures | PS-B-0089, PS-B-0090 | -- | -- | core | shipped-scope D01 T03 §7 | Imago menu and dialog: D03 T14 §2 |
| IP-1188 | Ocean ripple | PS-B-0091, PS-B-0092 | -- | -- | core | shipped-scope D01 T03 §7 | Imago menu and dialog: D03 T14 §2 |
| IP-1189 | Wave: generators, wavelength, amplitude, scale, type, randomize, edge handling | PS-B-0218, PS-B-0219, PS-B-0220, PS-B-0221, PS-B-0222 | -- | -- | core | shipped-scope D03 T07 §3 |  |
| IP-1190 | Vanishing Point export to DXF or 3DS and return to 3D layer | PS-B-0425, PS-B-0426 | -- | -- | 3d | excluded: removed | Removed with Photoshop legacy 3D |
| IP-2378 | Jiggle distortion: random jagged displacement with size, detail, strength, and seed | -- | -- | -- | core | plan D01 T06 §6 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1404; AC-3335 to AC-3339); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D01 T06 §6 |
| IP-2379 | Pixel explosion: pixels scattered outward from a center with intensity, direction, and seed | -- | -- | -- | core | plan D01 T06 §6 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1413; AC-3364 to AC-3369); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D01 T06 §6 |
| IP-2381 | Water reflection: rippled mirror of the subject below a water line with amplitude, wavelength, perspective, and lighting | -- | -- | -- | core | plan D01 T06 §6 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1431; AC-3455 to AC-3460); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D01 T06 §6 |

## Render, light, and shadow filters

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1191 | Bloom | -- | AF-1438, AF-1439 | -- | core | plan D01 T06 §8 |  |
| IP-1192 | Lens flare (GEGL op) | -- | -- | GP-3410 | core | plan D01 T06 §8 | Center placement surface D03 T14 §5 |
| IP-1193 | Lighting effects lights: point, spot, infinite, color, intensity, hotspot, distance, multiple lights, output options | PS-B-0273, PS-B-0274, PS-B-0275, PS-B-0276, PS-B-0277 | AF-1803, AF-1804, AF-1811, AF-1812, AF-1813, AF-1814, AF-1815, AF-1816, AF-1817, AF-1818 | GP-2628, GP-2629, GP-2630, GP-2635, GP-2636, GP-2637, GP-2638, GP-2639, GP-2640, GP-2641, GP-2642, GP-2643, GP-2644, GP-2645, GP-2646, GP-2647 | core | plan D01 T06 §8 | extends D03 T07 §3 and D01 T03 §11; Affinity live filter via D03 T14 §1 |
| IP-1194 | Lighting effects materials: ambient, diffuse, specular, gloss, metallic, exposure, colorize | PS-B-0278, PS-B-0279 | AF-1805, AF-1806, AF-1807, AF-1808, AF-1809, AF-1810 | GP-2631, GP-2650, GP-2651, GP-2652, GP-2653, GP-2654, GP-2655 | core | plan D01 T06 §8 | extends D03 T07 §3 |
| IP-1195 | Lighting effects bump mapping from a channel or image with curve and height | PS-B-0280 | AF-1819 | GP-2632, GP-2656, GP-2657, GP-2658, GP-2659 | core | plan D01 T06 §8 | extends D03 T07 §3 |
| IP-1196 | Lighting effects environment map | -- | -- | GP-2633, GP-2660, GP-2661 | core | plan D01 T06 §8 |  |
| IP-1197 | Lighting effects presets | PS-B-0281 | -- | GP-2649 | core | plan D01 T06 §8 | Flashlight, five lights down, blue omni, and saved user presets |
| IP-1198 | Lens flare lens types: zoom, 35mm prime, 105mm prime, movie prime | PS-B-0272 | -- | -- | core | plan D01 T06 §8 | extends D03 T07 §3 |
| IP-1199 | Vignette with shape, radius, softness, gamma, proportion, squeeze, center, rotation, exposure, on-canvas controls | -- | AF-1755, AF-1756, AF-1757, AF-1758, AF-1759, AF-1760 | GP-2574, GP-2575, GP-2576, GP-2577, GP-2578, GP-2579, GP-2580, GP-2581, GP-2582, GP-2583, GP-2584, GP-3500 | core | plan D01 T06 §8 | extends D01 T03 §10; GEGL gegl:vignette |
| IP-1200 | Bloom with threshold, softness, radius, strength, limit exposure, saturated or desaturated glow | -- | AF-1440, AF-1441, AF-1442, AF-1443 | GP-2541, GP-2542, GP-2543, GP-2544, GP-2545, GP-2546, GP-3352 | core | plan D01 T06 §8 | GEGL gegl:bloom |
| IP-1201 | Diffuse glow (gallery graininess, glow, clear; Affinity radius, intensity, threshold, opacity) | PS-B-0087, PS-B-0088 | AF-1465, AF-1466, AF-1467, AF-1468 | -- | core | plan D01 T06 §8 | extends D01 T03 §7 |
| IP-1202 | Inner glow filter | -- | -- | GP-2532, GP-2533, GP-2534, GP-2535, GP-2536, GP-2537, GP-2538, GP-2539, GP-2540, GP-3405 | core | plan D01 T06 §8 | GEGL gegl:inner-glow |
| IP-1203 | Drop shadow filter with grow shape, blur, color, opacity, allow resizing | -- | -- | GP-2547, GP-2548, GP-2549, GP-2550, GP-2551, GP-2552, GP-2553, GP-2554, GP-2681, GP-2682, GP-2683, GP-2684, GP-2685, GP-2686, GP-2687, GP-3382 | core | plan D01 T06 §8 | Merges GEGL and legacy script versions |
| IP-1204 | Long shadow: finite, infinite, and fading styles, angle, length, midpoint, composition | -- | -- | GP-2558, GP-2559, GP-2560, GP-2561, GP-2562, GP-2563, GP-2564, GP-3415 | core | plan D01 T06 §8 | GEGL gegl:long-shadow |
| IP-1205 | Perspective shadow: angle, horizon distance, length, blur, color, opacity, interpolation | -- | -- | GP-2688, GP-2689, GP-2690, GP-2691, GP-2692, GP-2693, GP-2694, GP-2695, GP-2696 | core | plan D01 T06 §8 |  |
| IP-1206 | Supernova: center, radius, spokes, random hue, color, seed | -- | -- | GP-2565, GP-2566, GP-2567, GP-2568, GP-2569, GP-2570, GP-2571, GP-2572, GP-2573, GP-3483 | core | plan D01 T06 §8 | GEGL gegl:supernova |
| IP-1207 | Gradient flare render: center, radius, rotation, hue rotation, second-flare vector, adaptive supersampling | -- | -- | GP-2585, GP-2586, GP-2594, GP-2595, GP-2596, GP-2597, GP-2598, GP-2599, GP-2600, GP-2601, GP-2602, GP-2603 | core | plan D01 T06 §8 |  |
| IP-1208 | Gradient flare glow, rays, and second flares: paint modes, gradients, spikes, shapes, seed | -- | -- | GP-2589, GP-2590, GP-2591, GP-2592, GP-2608, GP-2609, GP-2610, GP-2611, GP-2612, GP-2613, GP-2614, GP-2615, GP-2616, GP-2617, GP-2618, GP-2619, GP-2620, GP-2621, GP-2622, GP-2623, GP-2624, GP-2625, GP-2626, GP-2627 | core | plan D01 T06 §8 |  |
| IP-1209 | Sparkle: threshold, flare intensity, spikes, transparency, random hue and saturation, color type, border | -- | -- | GP-2662, GP-2663, GP-2664, GP-2665, GP-2666, GP-2667, GP-2668, GP-2669, GP-2670, GP-2671, GP-2672, GP-2673, GP-2674, GP-2675, GP-2676, GP-2677, GP-2678, GP-2679, GP-2680 | core | plan D01 T06 §8 |  |
| IP-1210 | Xach effect: highlight offset, color, opacity, drop shadow, keep selection | -- | -- | GP-2697, GP-2698, GP-2699, GP-2700, GP-2701, GP-2702, GP-2703, GP-2704, GP-2705, GP-2706, GP-2707, GP-2708 | core | plan D01 T06 §8 |  |
| IP-1211 | Bevel filter: chamfer or bump, distance map metric, radius, elevation, depth, light angle, blend mode | -- | -- | GP-2519, GP-2520, GP-2521, GP-2522, GP-2523, GP-2524, GP-2525, GP-2526, GP-2527, GP-2528, GP-2529, GP-2530, GP-2531 | core | plan D01 T06 §8 | GEGL bevel filter not named; closest light-and-shadow section, shares math with D03 T09 §8 |
| IP-1212 | Text styling filter: color overlay, outline, and shadow or glow | -- | -- | GP-2424, GP-2425, GP-2426, GP-2427, GP-2428, GP-2429, GP-2430, GP-2431, GP-2432, GP-2433, GP-2434, GP-2435, GP-2436, GP-2437, GP-2438, GP-2439, GP-2440, GP-2441, GP-2442, GP-2443 | core | plan D03 T09 §7 | the filter form of the text-styling effects of IP-0375, one renderer |
| IP-1213 | Text styling filter: bevel, inner glow, and image overlay levels | -- | -- | GP-2444, GP-2445, GP-2446, GP-2447, GP-2448, GP-2449, GP-2450, GP-2451, GP-2452, GP-2453, GP-2454, GP-2455, GP-2456, GP-2457, GP-2458, GP-2459, GP-2460, GP-2461, GP-2462, GP-2463, GP-2469, GP-2480, GP-2481 | core | plan D03 T09 §7 | the filter form of the text-styling effects of IP-0375, one renderer |
| IP-1214 | Perlin noise: octaves, zoom, persistence, blend mode | -- | AF-1694, AF-1695, AF-1696, AF-1697, AF-1698, AF-1699 | GP-3448 | core | plan D01 T06 §9 |  |
| IP-1215 | Simplex noise | -- | -- | GP-3469 | core | plan D01 T06 §9 |  |
| IP-1216 | Cell noise | -- | -- | GP-3358 | core | plan D01 T06 §9 |  |
| IP-1217 | Solid noise | -- | -- | GP-3441 | core | plan D01 T06 §9 |  |
| IP-1218 | Flame (scripted): flame types along a path, geometry, custom color, quality, advanced shaping | PS-B-0249, PS-B-0250, PS-B-0251, PS-B-0252, PS-B-0253, PS-B-0254 | -- | -- | core | plan D01 T06 §9 | Needs a path, D03 T16 §5 |
| IP-1219 | Picture frame (scripted): frame style presets, vines, flowers, leaves, advanced | PS-B-0255, PS-B-0256, PS-B-0257, PS-B-0258, PS-B-0259 | -- | -- | core | plan D01 T06 §9 |  |
| IP-1220 | Tree (scripted): species presets, light, leaves, branches, camera tilt, randomize | PS-B-0260, PS-B-0261, PS-B-0262, PS-B-0263, PS-B-0264, PS-B-0265 | -- | -- | core | plan D01 T06 §9 |  |
| IP-1221 | Difference clouds with seed, detail, tileable, turbulent, size | PS-B-0267 | -- | GP-3246, GP-3247, GP-3248, GP-3249, GP-3250, GP-3251, GP-3252 | core | plan D01 T06 §9 |  |
| IP-1222 | Fibers: variance, strength, randomize | PS-B-0268, PS-B-0269 | -- | -- | core | plan D01 T06 §9 |  |
| IP-1223 | Voronoi: cell size and line width | -- | AF-1761, AF-1762, AF-1763, AF-1764 | -- | core | plan D01 T06 §9 | Live filter via D03 T14 §1 |
| IP-1224 | Cell noise: scale, shape, rank, iterations, palettize | -- | -- | GP-2959, GP-2960, GP-2961, GP-2962, GP-2963, GP-2964 | core | plan D01 T06 §9 |  |
| IP-1225 | Perlin noise: alpha, scale, z offset, iterations | -- | -- | GP-2965, GP-2966, GP-2967, GP-2968, GP-2969 | core | plan D01 T06 §9 |  |
| IP-1226 | Simplex noise: scale, iterations, seed | -- | -- | GP-2970, GP-2971, GP-2972, GP-2973, GP-2974 | core | plan D01 T06 §9 |  |
| IP-1227 | Solid noise: size, detail, tileable, turbulent, seed | -- | -- | GP-2975, GP-2976, GP-2977, GP-2978, GP-2979, GP-2980, GP-2981, GP-2982 | core | plan D01 T06 §9 |  |
| IP-1228 | Plasma: turbulence and seed | -- | -- | GP-2983, GP-2984, GP-2985, GP-2986, GP-3452 | core | plan D01 T06 §9 | GEGL gegl:plasma |
| IP-1229 | Lava: seed, size, roughness, gradient, separate layer | -- | -- | GP-3253, GP-3254, GP-3255, GP-3256, GP-3257, GP-3258, GP-3259, GP-3260 | core | plan D01 T06 §9 |  |
| IP-1230 | Procedural texture function library: math, range, clamping, geometric, vector, interpolation, stepping, quantize, oscillators | -- | AF-1779, AF-1780, AF-1781, AF-1782, AF-1783, AF-1784, AF-1785, AF-1786, AF-1787, AF-1788, AF-1789, AF-1790 | -- | core | plan D01 T06 §9 | Engine for D03 T14 §10 |
| IP-1231 | Bayer matrix: subdivisions, scale, rotation, reflect, amplitude, offset, exponent | -- | -- | GP-2909, GP-2910, GP-2911, GP-2912, GP-2913, GP-2914, GP-2915, GP-2916, GP-2917, GP-2918, GP-2919, GP-3349 | core | plan D01 T06 §10 |  |
| IP-1232 | Checkerboard: size, offset, colors, psychobilly | -- | -- | GP-2920, GP-2921, GP-2922, GP-2923, GP-2924, GP-2925, GP-2926, GP-3010, GP-3011, GP-3012, GP-3360 | core | plan D01 T06 §10 | Merges GEGL and legacy versions |
| IP-1233 | Diffraction patterns | -- | -- | GP-2927, GP-3376 | core | plan D01 T06 §10 |  |
| IP-1234 | Grid render: spacing, offset, line width, color, intersections | -- | -- | GP-2928, GP-2929, GP-2930, GP-2931, GP-2932, GP-2933, GP-2934, GP-2935, GP-3130, GP-3131, GP-3132, GP-3133, GP-3134, GP-3135, GP-3136, GP-3137, GP-3138, GP-3139, GP-3140, GP-3400 | core | plan D01 T06 §10 | Merges GEGL and legacy versions |
| IP-1235 | Linear sinusoid: period, amplitude, phase, angle, offset, exponent, rotation, supersampling | -- | -- | GP-2936, GP-2937, GP-2938, GP-2939, GP-2940, GP-2941, GP-2942, GP-2943, GP-2944, GP-2945, GP-2946, GP-2947, GP-2948, GP-2949, GP-3413 | core | plan D01 T06 §10 |  |
| IP-1236 | Maze: size, depth-first or Prim algorithm, tileable, seed, colors | -- | -- | GP-2950, GP-2951, GP-2952, GP-2953, GP-2954, GP-2955, GP-2956, GP-2957, GP-2958, GP-3420 | core | plan D01 T06 §10 |  |
| IP-1237 | Sinus: scale, complexity, seed, tiling, distorted, colors, blend, exponent | -- | -- | GP-2987, GP-2988, GP-2989, GP-2990, GP-2991, GP-2992, GP-2993, GP-2994, GP-2995, GP-2996, GP-2997, GP-2998, GP-3470 | core | plan D01 T06 §10 |  |
| IP-1238 | Spiral: type, position, radius, balance, rotation, direction, colors, on-canvas controls | -- | -- | GP-2999, GP-3000, GP-3001, GP-3002, GP-3003, GP-3004, GP-3005, GP-3006, GP-3007, GP-3008, GP-3009, GP-3476 | core | plan D01 T06 §10 |  |
| IP-1239 | CML explorer: hue, saturation, and value functions, composition, diffusion, mutation, seeds | -- | -- | GP-3013, GP-3014, GP-3015, GP-3016, GP-3017, GP-3018, GP-3019, GP-3020, GP-3021, GP-3022, GP-3023, GP-3024, GP-3027, GP-3028, GP-3029, GP-3030, GP-3031, GP-3032, GP-3033, GP-3034, GP-3035, GP-3036, GP-3037, GP-3038, GP-3039, GP-3040, GP-3041, GP-3042, GP-3043, GP-3044, GP-3045, GP-3046, GP-3048, GP-3049, GP-3050, GP-3051, GP-3052, GP-3053, GP-3054 | core | plan D01 T06 §10 | CML explorer not named; closest patterns and fractals |
| IP-1240 | CML explorer settings: open, save, copy settings, selective load, plot graph | -- | -- | GP-3025, GP-3026, GP-3047, GP-3055, GP-3056 | core | plan D03 T14 §10 | dedicated editor over the D01 T06 §10 algorithm |
| IP-1241 | Flame fractal: editor, brightness, contrast, gamma, density, oversample, colormap, zoom, position, open and save | -- | -- | GP-3057, GP-3058, GP-3059, GP-3060, GP-3061, GP-3062, GP-3063, GP-3064, GP-3065, GP-3066, GP-3067, GP-3068, GP-3069, GP-3070 | core | plan D03 T14 §10 | dedicated editor over the D01 T06 §10 algorithm |
| IP-1242 | Fractal explorer: fractal types, bounds, iterations, CX and CY, zoom, saved fractals | -- | -- | GP-3071, GP-3072, GP-3074, GP-3075, GP-3076, GP-3077, GP-3078, GP-3079, GP-3080, GP-3081, GP-3082, GP-3083, GP-3084, GP-3085, GP-3086, GP-3087, GP-3393 | core | plan D01 T06 §10 | GEGL gegl:fractal-explorer |
| IP-1243 | Fractal explorer coloring: number of colors, log smoothing, channel stretch and functions, gradient | -- | -- | GP-3073, GP-3088, GP-3089, GP-3090, GP-3091, GP-3092, GP-3093, GP-3094, GP-3095, GP-3096, GP-3097, GP-3098 | core | plan D01 T06 §10 |  |
| IP-1244 | IFS fractal: transform editing, render options, color transforms, probability | -- | -- | GP-3141, GP-3142, GP-3143, GP-3144, GP-3145, GP-3146, GP-3147, GP-3148, GP-3149, GP-3150, GP-3151, GP-3152, GP-3153, GP-3154, GP-3155, GP-3156, GP-3157, GP-3158, GP-3159, GP-3160, GP-3161, GP-3162, GP-3163, GP-3164, GP-3165, GP-3166, GP-3167 | core | plan D03 T14 §10 | dedicated editor over the D01 T06 §10 algorithm |
| IP-1245 | Jigsaw: tiles, bevel edges, square or curved style | -- | -- | GP-3168, GP-3169, GP-3170, GP-3171, GP-3172, GP-3173, GP-3174, GP-3175 | core | plan D01 T06 §10 |  |
| IP-1246 | Qbist: random textures with anti-aliasing, undo, open and save | -- | -- | GP-3176, GP-3177, GP-3178, GP-3179, GP-3180 | core | plan D03 T14 §10 | dedicated editor over the D01 T06 §10 algorithm |
| IP-1247 | Spyrogimp: spirograph, epitrochoid, sine, Lissajous curves drawn with a paint tool | -- | -- | GP-3207, GP-3208, GP-3209, GP-3210, GP-3211, GP-3212, GP-3213, GP-3214, GP-3215, GP-3216, GP-3217, GP-3218, GP-3219, GP-3220, GP-3221, GP-3222, GP-3223, GP-3224, GP-3225, GP-3226, GP-3227, GP-3228, GP-3229, GP-3230, GP-3231, GP-3232, GP-3233, GP-3234, GP-3235, GP-3236, GP-3237, GP-3238, GP-3239 | core | plan D03 T14 §9 | draws with the D03 T12 painting tools |
| IP-1248 | Circuit: oilify mask, seed, separate layer, keep selection | -- | -- | GP-3240, GP-3241, GP-3242, GP-3243, GP-3244, GP-3245 | core | plan D01 T06 §10 |  |
| IP-1249 | Line nova: lines, sharpness, offset radius, randomness | -- | -- | GP-3261, GP-3262, GP-3263, GP-3264, GP-3265 | core | plan D01 T06 §10 |  |
| IP-1250 | Lighting bump map: load, clear, scale to fit, opacity | -- | AF-1820, AF-1821, AF-1822, AF-1823 | -- | core | plan D03 T14 §5 | Engine D01 T06 §8 |
| IP-1251 | Lighting effects lights panel, on-canvas light widgets, interactive preview, isolate light | PS-B-0282, PS-B-0283 | -- | GP-2634, GP-2648 | core | plan D03 T14 §5 |  |
| IP-1252 | Gradient flare selector and editor: new, edit, copy, delete, preview | -- | -- | GP-2587, GP-2588, GP-2593, GP-2604, GP-2605, GP-2606, GP-2607 | core | plan D03 T14 §5 |  |
| IP-1253 | Clouds | PS-B-0266 | -- | -- | core | shipped-scope D03 T07 §3 |  |
| IP-1254 | Lens flare with brightness and click-to-place center | PS-B-0270, PS-B-0271 | -- | GP-2555, GP-2556, GP-2557 | core | shipped-scope D03 T07 §3 | Also built in D01 T03 §11 |
| IP-2380 | Rain render: streaks with strength, opacity, amount, angle and variance, background blur, and color | -- | -- | -- | core | plan D01 T06 §9 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1417; AC-3384 to AC-3392); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D01 T06 §9 |
| IP-2382 | Water drops: refracting droplets over the photo with density, radius, height, and seed | -- | -- | -- | core | plan D01 T06 §8 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1432; AC-3461 to AC-3465); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D01 T06 §8 |

## Artistic, stylize, edge, and generic filters

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1255 | Emboss: emboss or bumpmap type, azimuth, elevation, depth | -- | -- | GP-2172, GP-2173, GP-2174, GP-2175, GP-2176, GP-2177, GP-2178 | core | plan D01 T06 §11 | extends D03 T07 §3 |
| IP-1256 | Detect edges with algorithm choice (Sobel, Prewitt, gradient, Roberts, differential, Laplace), amount, border | -- | AF-1704 | GP-2365, GP-2366, GP-2367, GP-2368, GP-2369, GP-2370, GP-2371, GP-2372, GP-2373, GP-2374, GP-3383 | core | plan D01 T06 §11 | extends D01 T03 §11 edge detect |
| IP-1257 | Sobel directional edges: horizontal, vertical, keep sign | -- | AF-1705, AF-1706 | GP-2361, GP-2362, GP-2363, GP-2364, GP-3386 | core | plan D01 T06 §11 |  |
| IP-1258 | Difference of Gaussians | -- | -- | GP-2354, GP-2355, GP-2356, GP-3375 | core | plan D01 T06 §11 |  |
| IP-1259 | Laplace edge detection | -- | -- | GP-2357, GP-3384 | core | plan D01 T06 §11 |  |
| IP-1260 | Neon edges with radius and intensity | -- | -- | GP-2358, GP-2359, GP-2360, GP-3385 | core | plan D01 T06 §11 |  |
| IP-1261 | Image gradient with output modes | -- | -- | GP-2375, GP-2376, GP-3404 | core | plan D01 T06 §11 |  |
| IP-1262 | Emboss with radius, amount, angle, monochrome | -- | AF-1727, AF-1728, AF-1729, AF-1730, AF-1731 | GP-3387 | core | plan D01 T06 §11 | extends D03 T07 §3 |
| IP-1263 | Oil paint with stylization, cleanliness, scale, bristle detail, lighting angle and shine | PS-B-0309, PS-B-0310, PS-B-0311 | -- | -- | core | plan D01 T06 §11 | extends D03 T07 §3 |
| IP-1264 | Diffuse modes: normal, darken only, lighten only, anisotropic | PS-B-0302, PS-B-0303 | -- | -- | core | plan D01 T06 §11 | extends D01 T03 §11 |
| IP-1265 | Extrude: blocks or pyramids, size, depth, solid front faces | PS-B-0306, PS-B-0307 | -- | -- | core | plan D01 T06 §11 |  |
| IP-1266 | Tiles: number, maximum offset, fill empty area | PS-B-0313, PS-B-0314 | -- | -- | core | plan D01 T06 §11 |  |
| IP-1267 | Apply canvas (texturize canvas) with direction and depth | -- | -- | GP-1851, GP-1852, GP-1853, GP-3488 | core | plan D01 T06 §12 |  |
| IP-1268 | Cartoon with mask radius and percent black | -- | -- | GP-1854, GP-1855, GP-1856, GP-3357 | core | plan D01 T06 §12 |  |
| IP-1269 | Cubism with tile size, saturation, background, seed | -- | -- | GP-1857, GP-1858, GP-1859, GP-1860, GP-1861, GP-1862, GP-3372 | core | plan D01 T06 §12 |  |
| IP-1270 | Oilify with mask radius, exponent, intensities, auxiliary maps | -- | -- | GP-1863, GP-1864, GP-1865, GP-1866, GP-1867, GP-1868, GP-1869, GP-3445 | core | plan D01 T06 §12 | Photoshop Oil Paint is D03 T07 §3 |
| IP-1271 | Photocopy (GIMP) with mask radius, sharpness, percent black and white | -- | -- | GP-1870, GP-1871, GP-1872, GP-1873, GP-1874, GP-3449 | core | plan D01 T06 §12 |  |
| IP-1272 | SLIC superpixels | -- | -- | GP-1875, GP-1876, GP-1877, GP-1878, GP-3471 | core | plan D01 T06 §12 |  |
| IP-1273 | Glass tile | -- | -- | GP-1883, GP-1884, GP-1885 | core | plan D01 T06 §12 |  |
| IP-1274 | Waterpixels | -- | -- | GP-1886, GP-1887, GP-1888, GP-1889, GP-1890, GP-3502 | core | plan D01 T06 §12 |  |
| IP-1275 | GIMPressionist painterly strokes: paper, brush, placement, color, background, presets | -- | -- | GP-1891, GP-1892, GP-1893, GP-1894, GP-1897, GP-1898, GP-1899, GP-1902, GP-1903, GP-1904, GP-1905, GP-1906, GP-1907, GP-1908, GP-1909, GP-1910, GP-1911, GP-1912, GP-1937, GP-1938, GP-1939, GP-1940, GP-1941, GP-1942, GP-1943, GP-1944, GP-1946, GP-1947, GP-1948, GP-1949, GP-1950, GP-1951, GP-1952, GP-1954, GP-1958 | core | plan D03 T14 §10 | dedicated editor over the D01 T06 §12 algorithm |
| IP-1276 | GIMPressionist stroke orientation and size modes (value, radius, random, radial, flowing, hue, adaptive, manual) | -- | -- | GP-1895, GP-1896, GP-1913, GP-1914, GP-1915, GP-1916, GP-1917, GP-1918, GP-1919, GP-1920, GP-1921, GP-1922, GP-1923, GP-1924, GP-1925, GP-1926, GP-1927, GP-1928, GP-1929, GP-1930, GP-1931, GP-1932, GP-1933, GP-1934, GP-1935, GP-1936 | core | plan D01 T06 §12 |  |
| IP-1277 | GIMPressionist orientation map and size map editors | -- | -- | GP-1900, GP-1901, GP-1959, GP-1960, GP-1961, GP-1963, GP-1964, GP-1965, GP-1966, GP-1967, GP-1968 | core | plan D03 T14 §10 | dedicated editor over the D01 T06 §12 algorithm |
| IP-1278 | Van Gogh (LIC) line integral convolution | -- | -- | GP-1969, GP-1970, GP-1971, GP-1972, GP-1974, GP-1975, GP-1976, GP-1978, GP-1979, GP-1980 | core | plan D01 T06 §12 |  |
| IP-1279 | Clothify | -- | -- | GP-1981, GP-1982, GP-1983, GP-1984, GP-1985, GP-1986 | core | plan D01 T06 §12 |  |
| IP-1280 | Weave | -- | -- | GP-1987, GP-1988, GP-1989, GP-1992, GP-1993, GP-1994 | core | plan D01 T06 §12 |  |
| IP-1281 | Softglow: glow radius, brightness, sharpness | -- | -- | GP-1879, GP-1880, GP-1881, GP-1882, GP-3474 | core | plan D01 T06 §12 | GEGL gegl:softglow |
| IP-1282 | GIMPressionist options: color noise, stroke drop shadow, Voronoi orientation | -- | -- | GP-1945, GP-1953, GP-1955, GP-1956, GP-1957, GP-1962 | core | plan D01 T06 §12 | Options of the GIMPressionist filter row |
| IP-1283 | Van Gogh (LIC) white noise convolve and noise magnitude | -- | -- | GP-1973, GP-1977 | core | plan D01 T06 §12 | Options of the Van Gogh filter row |
| IP-1284 | Weave shadow darkness and depth | -- | -- | GP-1990, GP-1991 | core | plan D01 T06 §12 | Options of the Weave filter row |
| IP-1285 | SVG hue rotate and SVG saturate color matrix ops | -- | -- | GP-3484, GP-3487 | core | plan D01 T06 §13 |  |
| IP-1286 | Color warp | -- | -- | GP-3368 | core | plan D01 T06 §13 |  |
| IP-1287 | Color assimilation grid | -- | -- | GP-3361 | core | plan D01 T06 §13 |  |
| IP-1288 | Color overlay | -- | -- | GP-3364 | core | plan D01 T06 §13 |  |
| IP-1289 | Antialias (Scale3X edge extrapolation) | -- | -- | GP-2378, GP-3347 | core | plan D01 T06 §13 | no section names Scale3X antialias; generic engine section |
| IP-1290 | Normal map from height map | -- | -- | GP-3443 | core | plan D01 T06 §13 |  |
| IP-1291 | Temporal blur (frame accumulation) | -- | -- | GP-3421 | core | backlog B-044 | frame accumulation only matters for frame sequences |
| IP-1292 | Convolution matrix: 5x5 kernel, divisor, offset, channels, normalize, alpha weighting, border | -- | -- | GP-2483, GP-2484, GP-2485, GP-2486, GP-2487, GP-2488, GP-2489, GP-2490, GP-2491, GP-2492, GP-2493, GP-2494, GP-2495, GP-3371 | core | plan D01 T06 §13 | extends D01 T03 §11 custom convolution |
| IP-1293 | Dilate | -- | -- | GP-2496 | core | plan D01 T06 §13 |  |
| IP-1294 | Erode | -- | -- | GP-2507 | core | plan D01 T06 §13 |  |
| IP-1295 | Distance map with metrics, thresholds, normalize | -- | -- | GP-2497, GP-2498, GP-2499, GP-2500, GP-2501, GP-2502, GP-2503, GP-2504, GP-2505, GP-2506, GP-3378 | core | plan D01 T06 §13 |  |
| IP-1296 | Normal map from a height map | -- | -- | GP-2510, GP-2511, GP-2512, GP-2513, GP-2514, GP-2515, GP-2516, GP-2517 | core | plan D01 T06 §13 |  |
| IP-1297 | Premultiply and unpremultiply alpha (divide or multiply by alpha) | -- | AF-1725, AF-1726 | GP-3494 | core | plan D01 T06 §13 |  |
| IP-1298 | Per-pixel math ops: add, subtract, multiply, divide, gamma, absolute | -- | -- | GP-3343, GP-3344, GP-3380, GP-3395, GP-3431, GP-3482 | core | plan D01 T06 §13 | Run from the GEGL browser D03 T14 §8 |
| IP-1299 | Alpha clip and opacity ops | -- | -- | GP-3346, GP-3446 | core | plan D01 T06 §13 |  |
| IP-1300 | Bevel op (chamfer and bump) | -- | -- | GP-3350 | core | plan D01 T06 §13 |  |
| IP-1301 | Linear and radial gradient render ops | -- | -- | GP-3412, GP-3455 | core | plan D01 T06 §13 | User job covered by the gradient tool D03 T12 §9 |
| IP-1302 | Blend ops: mix, weighted blend, piecewise blend by mask | -- | -- | GP-3425, GP-3450, GP-3507 | core | plan D01 T06 §13 |  |
| IP-1303 | Remap by luminance envelopes | -- | -- | GP-3459 | core | plan D01 T06 §13 |  |
| IP-1304 | SVG color matrix and luminance to alpha ops | -- | -- | GP-3485, GP-3486 | core | plan D01 T06 §13 |  |
| IP-1305 | Watershed transform | -- | -- | GP-3503 | core | plan D01 T06 §13 |  |
| IP-1306 | Offset with undefined areas: transparent, repeat edge, wrap around | PS-B-0332, PS-B-0333 | -- | -- | core | plan D01 T06 §13 | extends D01 T03 §7 |
| IP-1307 | HSB and HSL encoding filter | PS-B-0326, PS-B-0327 | -- | -- | core | plan D01 T06 §13 |  |
| IP-1308 | Maximum and minimum with preserve squareness or roundness | PS-B-0328, PS-B-0329, PS-B-0330, PS-B-0331 | -- | -- | core | plan D01 T06 §13 | extends D01 T03 §6 |
| IP-1309 | Depth merge of two sources by depth maps | -- | -- | GP-2077, GP-2078, GP-2079, GP-2080, GP-2081, GP-2082, GP-2083, GP-2084, GP-2085 | core | plan D03 T14 §9 |  |
| IP-1310 | Filmstrip from several images | -- | -- | GP-2086, GP-2087, GP-2088, GP-2089, GP-2090, GP-2091, GP-2092, GP-2093, GP-2094, GP-2095, GP-2096, GP-2097, GP-2098, GP-2099, GP-2100, GP-2101, GP-2102, GP-2103, GP-2104, GP-2105, GP-2106, GP-2107 | core | plan D03 T14 §9 |  |
| IP-1311 | Fog layer with color, turbulence, opacity | -- | -- | GP-2109, GP-2110, GP-2111, GP-2112, GP-2113 | core | plan D03 T14 §9 | Builds layers as one undoable command |
| IP-1312 | Add bevel with bump layer | -- | -- | GP-2114, GP-2115, GP-2116, GP-2117 | core | plan D03 T14 §9 |  |
| IP-1313 | Add border with color delta | -- | -- | GP-2118, GP-2119, GP-2120, GP-2121, GP-2122, GP-2123 | core | plan D03 T14 §9 |  |
| IP-1314 | Stencil carve | -- | -- | GP-2124, GP-2125, GP-2126 | core | plan D03 T14 §9 |  |
| IP-1315 | Coffee stain | -- | -- | GP-2127, GP-2128, GP-2129, GP-2130 | core | plan D03 T14 §9 |  |
| IP-1316 | Fuzzy border | -- | -- | GP-2131, GP-2132, GP-2133, GP-2134, GP-2135, GP-2138, GP-2139 | core | plan D03 T14 §9 |  |
| IP-1317 | Old photo | -- | -- | GP-2140, GP-2141, GP-2142, GP-2143, GP-2144, GP-2145 | core | plan D03 T14 §9 |  |
| IP-1318 | Round corners with shadow and background | -- | -- | GP-2146, GP-2147, GP-2150, GP-2151, GP-2152 | core | plan D03 T14 §9 |  |
| IP-1319 | Slide frame with labels | -- | -- | GP-2153, GP-2154, GP-2155, GP-2156, GP-2157, GP-2158 | core | plan D03 T14 §9 |  |
| IP-1320 | Stencil chrome | -- | -- | GP-2159, GP-2160, GP-2162, GP-2163, GP-2165, GP-2166 | core | plan D03 T14 §9 |  |
| IP-1321 | Fuzzy border: add shadow and shadow weight | -- | -- | GP-2136, GP-2137 | core | plan D03 T14 §9 | Options of the Fuzzy Border script row |
| IP-1322 | Round corners: drop shadow and offset | -- | -- | GP-2148, GP-2149 | core | plan D03 T14 §9 | Options of the Round Corners script row |
| IP-1323 | Stencil chrome: chrome lightness and highlight balance | -- | -- | GP-2161, GP-2164 | core | plan D03 T14 §9 | Options of the Stencil Chrome script row |
| IP-1324 | FFT denoise: paint out peaks on the Fourier spectrum | -- | AF-1681, AF-1682, AF-1683, AF-1684, AF-1685, AF-1686, AF-1687, AF-1688 | -- | core | plan D03 T14 §10 | Engine D01 T06 §5 |
| IP-1325 | Procedural texture noise function sets | -- | AF-1791, AF-1792, AF-1793, AF-1794, AF-1795, AF-1796 | -- | core | plan D03 T14 §10 | Engine D01 T06 §9 |
| IP-1326 | Equations: coordinate expressions, polar system, extend modes | -- | AF-1577, AF-1579, AF-1585 | -- | core | plan D03 T14 §10 | Engine D01 T06 §13 |
| IP-1327 | Equations filter: cartesian expressions, parameters A B C, extend modes | -- | AF-1578, AF-1580, AF-1581, AF-1582, AF-1583, AF-1584, AF-1586 | -- | core | plan D03 T14 §10 | Engine D01 T06 §13 |
| IP-1328 | Procedural texture filter: equation lines, channel targets, variables, built-in variables, origin drag | -- | AF-1746, AF-1747, AF-1766, AF-1767, AF-1768, AF-1769, AF-1770 | -- | core | plan D03 T14 §10 | Engine D01 T06 §9; live filter via D03 T14 §1 |
| IP-1329 | Procedural texture custom inputs: ranges, real, integer, angle, elevation-rotation, rename | -- | AF-1771, AF-1772, AF-1773, AF-1774, AF-1775, AF-1776, AF-1777 | -- | core | plan D03 T14 §10 |  |
| IP-1330 | Procedural texture presets and example recipes | -- | AF-1778, AF-1797, AF-1798 | -- | core | plan D03 T14 §10 |  |
| IP-1331 | Craquelure | PS-B-0123, PS-B-0124 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1332 | Grain with grain types | PS-B-0125, PS-B-0126 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1333 | Mosaic tiles | PS-B-0127 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1334 | Patchwork | PS-B-0129, PS-B-0130 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1335 | Stained glass | PS-B-0131 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1336 | Texturizer | PS-B-0133 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1337 | Mosaic tiles options | PS-B-0128 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1338 | Stained glass options | PS-B-0132 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1339 | Texturizer: texture, scaling, relief, light, invert | PS-B-0134 | -- | -- | core | shipped-scope D01 T03 §10 | Imago menu and dialog: D03 T14 §2 |
| IP-1340 | Solarize | -- | AF-1754 | -- | core | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1341 | Solarize | PS-B-0312 | -- | -- | core | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1342 | Trace contour: level and upper or lower edge | PS-B-0315, PS-B-0316 | -- | -- | core | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1343 | De-interlace: odd or even fields, duplication or interpolation | PS-B-0319, PS-B-0320 | -- | -- | video | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1344 | NTSC colors | PS-B-0321 | -- | -- | video | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1345 | Custom convolution kernel with scale, offset, load, save | PS-B-0322, PS-B-0323 | -- | -- | core | shipped-scope D01 T03 §11 | Imago menu and dialog: D03 T14 §2 |
| IP-1346 | Wind: wind, blast, stagger, direction | PS-B-0317, PS-B-0318 | -- | -- | core | shipped-scope D01 T03 §7 | Imago menu and dialog: D03 T14 §2 |
| IP-1347 | Colored pencil | PS-B-0041, PS-B-0042 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1348 | Cutout | PS-B-0043, PS-B-0044 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1349 | Dry brush | PS-B-0045, PS-B-0046 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1350 | Film grain | PS-B-0047 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1351 | Fresco | PS-B-0049, PS-B-0050 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1352 | Paint daubs with brush types | PS-B-0053, PS-B-0054 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1353 | Palette knife | PS-B-0055, PS-B-0056 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1354 | Plastic wrap | PS-B-0057 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1355 | Poster edges | PS-B-0059, PS-B-0060 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1356 | Rough pastels | PS-B-0061 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1357 | Smudge stick | PS-B-0063 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1358 | Sponge | PS-B-0065, PS-B-0066 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1359 | Underpainting | PS-B-0067 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1360 | Watercolor | PS-B-0069 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1361 | Charcoal | PS-B-0097 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1362 | Conte crayon | PS-B-0101 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1363 | Film grain options: grain, highlight area, intensity | PS-B-0048 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1364 | Neon glow: size, brightness, color | PS-B-0051, PS-B-0052 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1365 | Plastic wrap options | PS-B-0058 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1366 | Rough pastels options with texture | PS-B-0062 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1367 | Smudge stick options | PS-B-0064 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1368 | Underpainting options with texture | PS-B-0068 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1369 | Watercolor options | PS-B-0070 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1370 | Charcoal options | PS-B-0098 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1371 | Conte crayon options with texture | PS-B-0102 | -- | -- | core | shipped-scope D01 T03 §8 | Imago menu and dialog: D03 T14 §2 |
| IP-1372 | Accented edges | PS-B-0071, PS-B-0072 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1373 | Angled strokes | PS-B-0073, PS-B-0074 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1374 | Crosshatch | PS-B-0075, PS-B-0076 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1375 | Dark strokes | PS-B-0077, PS-B-0078 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1376 | Ink outlines | PS-B-0079 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1377 | Spatter | PS-B-0081, PS-B-0082 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1378 | Sprayed strokes | PS-B-0083, PS-B-0084 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1379 | Sumi-e | PS-B-0085, PS-B-0086 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1380 | Bas relief | PS-B-0093 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1381 | Chalk and charcoal | PS-B-0095, PS-B-0096 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1382 | Chrome | PS-B-0099, PS-B-0100 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1383 | Graphic pen | PS-B-0103 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1384 | Halftone pattern | PS-B-0105, PS-B-0106 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1385 | Note paper | PS-B-0107, PS-B-0108 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1386 | Photocopy (Filter Gallery) | PS-B-0109, PS-B-0110 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1387 | Plaster | PS-B-0111 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1388 | Reticulation | PS-B-0113, PS-B-0114 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1389 | Stamp | PS-B-0115 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1390 | Torn edges | PS-B-0117, PS-B-0118 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1391 | Water paper | PS-B-0119, PS-B-0120 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1392 | Ink outlines options | PS-B-0080 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1393 | Bas relief options | PS-B-0094 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1394 | Graphic pen options | PS-B-0104 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1395 | Plaster options | PS-B-0112 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1396 | Stamp options | PS-B-0116 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1397 | Glowing edges: width, brightness, smoothness | PS-B-0121, PS-B-0122 | -- | -- | core | shipped-scope D01 T03 §9 | Imago menu and dialog: D03 T14 §2 |
| IP-1398 | Emboss: angle, height, amount | PS-B-0304, PS-B-0305 | -- | -- | core | shipped-scope D03 T07 §3 |  |
| IP-1399 | Find edges | PS-B-0308 | -- | -- | core | shipped-scope D03 T07 §3 |  |
| IP-2376 | Collage effect: break the photo into scattered smaller copies with count, size, background, and reshuffle | -- | -- | -- | core | plan D01 T06 §11 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1392; AC-3283 to AC-3287); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D01 T06 §11 |
| IP-2377 | Furry edges effect: fur strands grown along detected edges with length, variance, direction, colors, and seed | -- | -- | -- | core | plan D01 T06 §12 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1400; AC-3313 to AC-3322); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D01 T06 §12 |
| IP-2384 | Decorative border frames: tiled textures, irregular edge masks, edge blur, drop shadow, raised edge with light direction, user texture and edge folders | -- | -- | -- | core | plan D03 T14 §9 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1472; AC-3565 to AC-3574); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T14 §9 |

## Develop and tone mapping

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1400 | Camera profiles browser with favorites and profile amount | PS-B-0465, PS-B-0466 | -- | -- | core | plan D01 T07 §1 | surface D03 T15 §1, Imago ships its own profile LUTs |
| IP-1401 | Auto tone and color | PS-B-0469 | -- | -- | core | plan D01 T07 §1 | surface D03 T15 §1, classical statistics, no model |
| IP-1402 | Light: exposure, contrast, highlights, shadows, whites, blacks, brightness, blackpoint | PS-B-0472, PS-B-0473, PS-B-0474, PS-B-0475, PS-B-0476, PS-B-0477 | AF-1904, AF-1905, AF-1906, AF-1907, AF-1913 | -- | core | plan D01 T07 §1 | surface D03 T15 §1 |
| IP-1403 | Tone curve: parametric regions and point curve per channel with refine saturation | PS-B-0479, PS-B-0480 | AF-1946 | -- | core | plan D01 T07 §1 | surface D03 T15 §1 |
| IP-1404 | White balance: presets, temperature, tint, eyedropper and tool | PS-B-0482, PS-B-0483, PS-B-0484, PS-B-0485 | AF-1911, AF-1912, AF-1967 | -- | core | plan D01 T07 §1 | surface D03 T15 §1 |
| IP-1405 | Default tone curves: compressed, natural, high contrast, log, also for merges | -- | AF-1984, AF-2034 | -- | core | plan D01 T07 §1 | surface D03 T15 §1 |
| IP-1406 | Haze removal: distance, strength, exposure correction | -- | AF-1799, AF-1800, AF-1801, AF-1802 | -- | core | plan D01 T07 §2 | Dehaze engine; Imago menu and dialog: D03 T14 §2 |
| IP-1407 | Treatment color or black and white with B and W mix | PS-B-0468, PS-B-0492 | AF-1947 | -- | core | plan D01 T07 §2 | surface D03 T15 §1 |
| IP-1408 | Vibrance and saturation | PS-B-0486, PS-B-0487 | AF-1909, AF-1910 | -- | core | plan D01 T07 §2 | surface D03 T15 §1 |
| IP-1409 | Texture, clarity, and dehaze | PS-B-0496, PS-B-0497, PS-B-0498 | AF-1908 | -- | core | plan D01 T07 §2 | surface D03 T15 §1 |
| IP-1410 | Color mixer HSL and color modes | PS-B-0488, PS-B-0489 | -- | -- | core | plan D01 T07 §2 | surface D03 T15 §1 |
| IP-1411 | Point color with range refinement | PS-B-0490 | -- | -- | core | plan D01 T07 §2 | surface D03 T15 §1 |
| IP-1412 | Color grading wheels, blending, balance, and split toning | PS-B-0493, PS-B-0494, PS-B-0495 | AF-1948 | -- | core | plan D01 T07 §2 | surface D03 T15 §1 |
| IP-1413 | Calibration: process version, shadows tint, primaries hue and saturation | PS-B-0518, PS-B-0519, PS-B-0520 | -- | -- | core | plan D01 T07 §2 | surface D03 T15 §1 |
| IP-1414 | Channel inversion for infrared and film negatives | -- | AF-1949, AF-1950 | -- | core | plan D01 T07 §2 | negative inversion not named in any section, surface D03 T15 §1 |
| IP-1415 | Affinity 3.3 added RAW color, sharpening, and detail adjustments | -- | AF-1951 | -- | core | plan D01 T07 §2 | umbrella row, individual controls land in D01 T07 §1 to §3 |
| IP-1416 | Glow from brightest areas | PS-B-0478 | -- | -- | core | plan D01 T07 §3 | surface D03 T15 §1, ACR 18.6 light slider |
| IP-1417 | Post-crop vignette with style, midpoint, roundness, feather | PS-B-0499 | AF-1931 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1418 | Grain and noise addition: amount, size, roughness, color, gaussian | PS-B-0500 | AF-1942, AF-1943, AF-1944 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1419 | Sharpening: amount, radius, detail, masking with preview | PS-B-0501 | AF-1933, AF-1934 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1420 | Multi-band and high pass sharpening modes | -- | AF-1935, AF-1936 | -- | core | plan D01 T07 §3 | surface D03 T15 §1, kernels D01 T06 §4 |
| IP-1421 | Manual noise reduction: luminance and color with detail, contrast, smoothness, contribution | PS-B-0505 | AF-1937, AF-1938, AF-1939, AF-1940, AF-1941 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1422 | Remove chromatic aberration | PS-B-0506 | AF-1925 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1423 | Lens profile corrections by EXIF with make, model, profile, and amounts | PS-B-0507, PS-B-0508 | AF-1916 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1424 | Manual lens distortion and lens vignetting removal | PS-B-0509 | AF-1919, AF-1930 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1425 | Lens profile database with Lensfun XML and Adobe LCP import | -- | AF-1918, AF-1981 | -- | format | plan D03 T14 §6 | the lens database reader D01 T07 §3 consumes |
| IP-1426 | Defringe: purple and green hue ranges, radius, tolerance, threshold, eyedropper | PS-B-0510 | AF-1926, AF-1927, AF-1928, AF-1929 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1427 | Upright modes and guided upright | PS-B-0512, PS-B-0513 | -- | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1428 | Manual geometry: vertical, horizontal, rotate, aspect, scale, offset, constrain crop | PS-B-0514, PS-B-0515 | AF-1920, AF-1921, AF-1922, AF-1923 | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1429 | Projection correction for stretched faces at wide-angle edges | PS-B-0516 | -- | -- | ai | plan D01 T07 §3 | surface D03 T15 §1, face locations from D03 T19 §11 |
| IP-1430 | Anamorphic desqueeze | PS-B-0524 | -- | -- | core | plan D01 T07 §3 | surface D03 T15 §1 |
| IP-1431 | Mask brush: size, feather, flow, density, hardness, auto mask, erase | PS-B-0546 | AF-1956, AF-1957, AF-1962, AF-1963, AF-1964 | -- | core | plan D01 T07 §4 | surface D03 T15 §2 |
| IP-1432 | Linear, radial, and bidirectional gradient masks | PS-B-0547, PS-B-0548, PS-B-0549 | AF-1955 | -- | core | plan D01 T07 §4 | surface D03 T15 §2 |
| IP-1433 | Color and luminance range masks | PS-B-0550, PS-B-0551 | -- | -- | core | plan D01 T07 §4 | surface D03 T15 §2 |
| IP-1434 | Depth range mask | PS-B-0552 | -- | -- | ai | plan D01 T07 §4 | surface D03 T15 §2, depth estimated, not measured |
| IP-1435 | Mask combine add, subtract, intersect, invert, duplicate | PS-B-0553, PS-B-0554 | -- | -- | core | plan D01 T07 §4 | surface D03 T15 §2 |
| IP-1436 | Mask feather and edge refinement | PS-B-0556 | -- | -- | core | plan D01 T07 §4 | surface D03 T15 §2 |
| IP-1437 | Local adjustment set with mask amount and opacity | PS-B-0557, PS-B-0560 | AF-1966 | -- | core | plan D01 T07 §4 | surface D03 T15 §2 |
| IP-1438 | Local color grading and point color in a mask | PS-B-0558, PS-B-0559 | -- | -- | core | plan D01 T07 §4 | surface D03 T15 §2 |
| IP-1439 | Brush and gradient overlays with opacity | -- | AF-1958, AF-1959, AF-1960, AF-1961 | -- | core | plan D01 T07 §4 | (Affinity Photo 2 only), surface D03 T15 §2 |
| IP-1440 | Spot removal: content-aware remove, heal, clone, size, feather, opacity | PS-B-0526, PS-B-0527, PS-B-0528, PS-B-0530 | AF-1970 | -- | core | plan D01 T07 §5 | surface D03 T15 §1 |
| IP-1441 | Visualize spots with threshold | PS-B-0531 | -- | -- | core | plan D01 T07 §5 | surface D03 T15 §1 |
| IP-1442 | Red eye and pet eye with pupil size, darken, catchlight | PS-B-0537, PS-B-0538, PS-B-0539 | AF-1969 | -- | core | plan D01 T07 §5 | surface D03 T15 §1 |
| IP-1443 | Presets panel with amount, filtering, app-wide presets | PS-B-0563, PS-B-0569 | AF-1899, AF-1900 | -- | core | plan D01 T07 §6 | surface D03 T15 §1 |
| IP-1444 | Create, import, and export presets as XMP | PS-B-0567, PS-B-0568 | -- | -- | core | plan D01 T07 §6 | surface D03 T15 §1 |
| IP-1445 | Built-in style preset groups | PS-B-0565 | -- | -- | core | plan D01 T07 §6 | surface D03 T15 §1, Imago ships its own looks |
| IP-1446 | Mask presets | PS-B-0561 | -- | -- | core | plan D01 T07 §6 | surface D03 T15 §2, recommended presets via D03 T19 §10 |
| IP-1447 | Develop snapshots: add, delete, compare | PS-B-0570 | AF-1975, AF-1976 | -- | core | plan D01 T07 §6 | surface D03 T15 §1 |
| IP-1448 | Copy and paste develop settings | PS-B-0579 | -- | -- | core | plan D01 T07 §6 | surface D03 T15 §1 |
| IP-1449 | Raw defaults per camera | PS-B-0587 | -- | -- | core | plan D01 T07 §6 | surface D03 T15 §1 |
| IP-1450 | Camera Raw filter | PS-B-0005 | -- | -- | core | plan D03 T15 §1 | Engine D01 T07 |
| IP-1451 | Camera Raw filter as a re-editable smart filter | PS-B-0463 | -- | -- | core | plan D03 T15 §1 | runs on smart objects via D03 T14 §1 |
| IP-1452 | Targeted adjustment tool for curve and color mixer | PS-B-0481, PS-B-0491 | -- | -- | core | plan D03 T15 §1 | drag on image; engine D01 T07 §1 and §2 |
| IP-1453 | Before and after views: single, split, mirror, side by side | PS-B-0571 | AF-1880, AF-1881, AF-1882 | -- | core | plan D03 T15 §1 | states from D01 T07 §6 |
| IP-1454 | Before and after sync and swap | -- | AF-1883, AF-1884, AF-1885 | -- | core | plan D03 T15 §1 |  |
| IP-1455 | Develop histogram, scope, and clipping overlays for highlights, shadows, tones | PS-B-0572 | AF-1886, AF-1887, AF-1888, AF-1977 | -- | core | plan D03 T15 §13 | histogram data from D01 T07 §1 |
| IP-1456 | Develop vectorscope with skin tone line and Lab readout | PS-B-0573 | -- | -- | core | plan D03 T15 §13 | scopes engine shared with D03 T08 §11 |
| IP-1457 | Develop metadata info panel | PS-B-0574 | -- | -- | core | plan D03 T15 §13 |  |
| IP-1458 | Autofocus points and focus data panel | PS-B-0575 | AF-1972, AF-1973 | -- | core | plan D03 T15 §13 | only for makers whose raw notes are decoded |
| IP-1459 | Focus peaking overlay with color choice | -- | AF-1982, AF-1983 | -- | core | plan D03 T15 §13 | view only |
| IP-1460 | Render to DNG with edits baked in | PS-B-0577 | -- | -- | format | plan D03 T15 §13 | no DNG writer section; built with the develop surface |
| IP-1461 | Panel reset, active toggles, and double-click slider reset | PS-B-0580 | AF-1879, AF-1901, AF-1902 | -- | core | plan D03 T15 §1 |  |
| IP-1462 | Develop zoom, hand, and view tools | PS-B-0581 | AF-1971 | -- | core | plan D03 T15 §13 |  |
| IP-1463 | Workflow options: color space, output ICC profile, bit depth 16 or 32 float, size, open as smart object | PS-B-0582 | AF-1894, AF-1914 | -- | core | plan D03 T15 §13 | extends D03 T07 §11 |
| IP-1464 | Geometry grid overlay and loupe | PS-B-0517 | -- | -- | core | plan D03 T15 §13 |  |
| IP-1465 | Camera Raw preferences, develop assistant defaults, and develop presets panel | PS-B-1251 | AF-2506, AF-2726 | -- | core | plan D03 T15 §13 |  |
| IP-1466 | Develop studio adjustment set | -- | AF-1381 | -- | core | plan D03 T15 §12 |  |
| IP-1467 | Develop noise reduction: luminance, details, contribution, colors | -- | AF-1277, AF-1278, AF-1279, AF-1280, AF-1281, AF-1282 | -- | core | plan D03 T15 §12 | Engine D01 T07 §3 |
| IP-1468 | Develop noise addition: intensity, color, gaussian | -- | AF-1283, AF-1284, AF-1285, AF-1286 | -- | core | plan D03 T15 §12 | Engine D01 T07 §3 grain |
| IP-1469 | Develop lens correction: profile, favorites, distortion, perspective, rotation, scale | -- | AF-1287, AF-1288, AF-1289, AF-1290, AF-1291, AF-1292, AF-1293, AF-1294 | -- | core | plan D03 T15 §12 | Engine D01 T07 §3 |
| IP-1470 | Develop remove lens vignette: intensity, scale, hardness | -- | AF-1295, AF-1296, AF-1297, AF-1298 | -- | core | plan D03 T15 §12 | Engine D01 T07 §3 |
| IP-1471 | Open RAW into the Develop studio | -- | AF-2350 | -- | core | shipped-scope D03 T07 §11 | RAW opens through the shared decoder; D03 T15 §12 hosts it in the Develop studio once that section has shipped |
| IP-1472 | Develop studio: enter, develop to commit, cancel | -- | AF-0007, AF-1869, AF-1872, AF-1873 | -- | core | plan D03 T15 §12 | Affinity studio maps to the Imago develop workspace |
| IP-1473 | Develop any pixel layer in any color format | -- | AF-1871 | -- | core | plan D03 T15 §12 | converts to the scene-referred develop space and back |
| IP-1474 | Develop output: pixel layer, embedded RAW layer, linked RAW layer | -- | AF-1874, AF-1875, AF-1876 | -- | core | plan D03 T15 §12 | pixel-layer output now; RAW layers once D03 T07 §11 opens RAW files |
| IP-1475 | Redevelop a RAW layer with previous settings and show all layers | -- | AF-1877, AF-1878 | -- | core | plan D03 T15 §12 | pixel-layer output now; RAW layers once D03 T07 §11 opens RAW files |
| IP-1476 | Develop crop, straighten, aspect presets, rotate 90, trim to transparent | PS-B-0521, PS-B-0523 | AF-1968, AF-1889 | -- | core | plan D03 T15 §12 | geometry engine D01 T07 §3 |
| IP-1477 | Save image from the develop dialog | PS-B-0583 | -- | -- | format | plan D03 T15 §12 | writers from D03 T04 and D03 T17 |
| IP-1478 | Develop assistant: lens profile, noise reduction, tone curve, exposure bias on load, alerts, live mode | -- | AF-1890, AF-1892, AF-1893, AF-1895, AF-1896, AF-1897, AF-1952 | -- | core | plan D03 T15 §12 | engine D01 T07 §1 and §3 |
| IP-1479 | Lens profile favorites and auto-profile status | -- | AF-1917, AF-1924 | -- | core | plan D03 T15 §12 |  |
| IP-1480 | Develop history of setting changes | -- | AF-1978 | -- | core | plan D03 T15 §12 | one undo step on commit |
| IP-1481 | Develop panels: basic, lens, details, tones | -- | AF-1903, AF-1915, AF-1932, AF-1945 | -- | core | plan D03 T15 §12 | Affinity panel grouping, controls in D01 T07 |
| IP-1482 | Blemish removal in Develop | -- | AF-0304 | -- | core | plan D03 T15 §12 | Engine D01 T07 §5 |
| IP-1483 | Develop mask paint, gradient, and erase tools | -- | AF-0352, AF-0353, AF-0354 | -- | core | plan D03 T15 §2 |  |
| IP-1484 | Develop masks panel | -- | AF-1954 | -- | core | plan D03 T15 §2 |  |
| IP-1485 | Mask overlay display modes, color, and opacity | PS-B-0555 | AF-1965 | -- | core | plan D03 T15 §2 |  |
| IP-1486 | HDR Toning: methods, edge glow, tone and detail, toning curve, presets; opens on 32 to lower conversion | PS-A-1108, PS-A-1109, PS-A-1110, PS-A-1111, PS-A-1112, PS-A-1113, PS-A-1114, PS-A-1115, PS-A-1116, PS-A-1164 | -- | -- | core | plan D03 T15 §3 |  |
| IP-1487 | Tone compression adjustment (realtime non-spatial tone mapping) | -- | AF-1365, AF-1366, AF-1367 | -- | core | plan D03 T15 §3 |  |
| IP-1488 | Fattal et al. 2002 tone mapping | -- | -- | GP-1614, GP-1615, GP-1616, GP-1617, GP-1618, GP-3391 | core | plan D03 T15 §3 |  |
| IP-1489 | Mantiuk 2006 tone mapping | -- | -- | GP-1626, GP-1627, GP-1628, GP-1629, GP-3416 | core | plan D03 T15 §3 |  |
| IP-1490 | Reinhard 2005 tone mapping | -- | -- | GP-1637, GP-1638, GP-1639, GP-1640, GP-3458 | core | plan D03 T15 §3 |  |
| IP-1491 | Stress (retinex-like envelope) tone mapping | -- | -- | GP-1663, GP-1664, GP-1665, GP-1666, GP-1667, GP-3478 | core | plan D03 T15 §3 |  |
| IP-1492 | Tone mapping studio: enter from any document and apply | -- | AF-0009, AF-1986, AF-1987, AF-2002 | -- | core | plan D03 T15 §3 | 8 and 16 bit documents get an HDR look |
| IP-1493 | Tone mapping presets: built-in, create, import | -- | AF-1988 | -- | core | plan D03 T15 §3 |  |
| IP-1494 | Tone compression and local contrast | -- | AF-1990, AF-1991 | -- | core | plan D03 T15 §3 |  |
| IP-1495 | Clamp to SDR | -- | AF-1989 | -- | core | plan D03 T15 §3 |  |
| IP-1496 | Tone map exposure, black point, brightness, contrast, shadows and highlights | -- | AF-1992, AF-1993, AF-1994, AF-1995, AF-1999 | -- | core | plan D03 T15 §3 |  |
| IP-1497 | Tone map saturation, vibrance, white balance | -- | AF-1996, AF-1997, AF-1998 | -- | core | plan D03 T15 §3 |  |
| IP-1498 | Tone map detail refinement | -- | AF-2000 | -- | core | plan D03 T15 §3 |  |
| IP-1499 | Tone map curves | -- | AF-2001 | -- | core | plan D03 T15 §3 |  |
| IP-1500 | Rasterize layers on entering tone mapping | -- | AF-2003 | -- | core | plan D03 T15 §3 | preference |
| IP-1501 | HDR Toning: local adaptation, equalize histogram, exposure and gamma, highlight compression, presets | PS-B-0733, PS-B-0734, PS-B-0737, PS-B-0738 | -- | -- | automation | plan D03 T15 §3 |  |
| IP-1502 | Camera RAW and DNG open (incl. Apple ProRAW) | PS-B-1026, PS-B-1027 | AF-2628, AF-2629 | GP-4832 | format | shipped-scope D03 T07 §11 | Lumen decoder, full develop filter in D03 T15 §1 |
| IP-1503 | Open camera RAW files through the shared decoder with current camera support | PS-B-0464 | AF-1870, AF-1980, AF-1985 | -- | format | shipped-scope D03 T07 §11 | full dialog routing: D03 T15 §1 |
| IP-1504 | Fullscreen presentation of photos | PS-B-0576 | -- | -- | core | other-app: Lumen multi-photo review |  |
| IP-1505 | Filmstrip multi-image editing with synchronize | PS-B-0578 | -- | -- | core | other-app: Lumen multi-photo sync |  |
| IP-1506 | External raw developer hand-off (ART, darktable, RawTherapee) | -- | -- | GP-0093 | format | other-app: Lumen suite raw developer | Lumen to Imago hand-off replaces third-party raw plug-ins |
| IP-1507 | RAW engine choice with Apple Core Image | -- | AF-1891 | -- | core | excluded: platform | macOS-only engine, Imago has one decoder |

## HDR, panorama, stacks, and astrophotography

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1508 | 32-bit float HDR editing | -- | AF-2233 | -- | core | plan D03 T15 §4 |  |
| IP-1509 | 32-bit preview: display exposure, gamma, ICC, unmanaged, OCIO display transforms | -- | AF-1351, AF-1359, AF-1360, AF-1361, AF-1362, AF-1363, AF-2234, AF-2239, AF-2240 | -- | core | plan D03 T15 §4 |  |
| IP-1510 | HDR display output: enable HDR, clip warning, reference white, clip to peak, default on | -- | AF-1353, AF-1355, AF-1356, AF-1358, AF-1364, AF-2235, AF-2236, AF-2237, AF-2238, AF-2243 | -- | core | plan D03 T15 §4 | Windows HDR displays |
| IP-1511 | 32-bit preview options | PS-A-1713 | -- | -- | core | plan D03 T15 §4 |  |
| IP-1512 | HDR output editing and HDR visualize with SDR preview in develop | PS-B-0470, PS-B-0471 | -- | -- | core | plan D03 T15 §4 | surface D03 T15 §1 |
| IP-1513 | 32-bit float unbounded editing | -- | AF-2004 | -- | core | plan D03 T15 §4 | extends D03 T08 §1 |
| IP-1514 | HDR display output with enable by default | -- | AF-2005, AF-2007, AF-2009 | -- | core | plan D03 T15 §4 | Windows HDR only |
| IP-1515 | Color intensity slider for unbounded colors | -- | AF-2006 | -- | core | plan D03 T15 §4 | in the color panel D03 T11 §9 |
| IP-1516 | 32-bit preview panel: view exposure and gamma | -- | AF-2008, AF-2013, AF-2014 | -- | core | plan D03 T15 §4 |  |
| IP-1517 | HDR clipping warning, reference white nits, clip to peak | -- | AF-2010, AF-2011, AF-2012 | -- | core | plan D03 T15 §4 |  |
| IP-1518 | 32-bit display transform: ICC, unmanaged, OCIO | -- | AF-2015, AF-2016, AF-2017 | -- | core | plan D03 T15 §4 | OCIO config from D03 T18 §4 |
| IP-1519 | Convert 32-bit documents through the develop filter and HDR display by default in 32-bit views | PS-B-1252 | AF-2735 | -- | core | plan D03 T15 §4 |  |
| IP-1520 | Auto-align layers | PS-A-1247 | -- | -- | core | plan D03 T15 §5 |  |
| IP-1521 | Auto-align layers with projections and lens corrections | PS-A-0042, PS-A-0950, PS-A-0951, PS-A-0952, PS-A-0953 | -- | -- | core | plan D03 T15 §5 |  |
| IP-1522 | Auto-Align Layers | PS-B-0751 | -- | -- | automation | plan D03 T15 §5 |  |
| IP-1523 | Combine exposures into HDR | -- | -- | GP-3389 | core | plan D03 T15 §6 | gegl:exp-combine |
| IP-1524 | Merge to HDR with source list and staged preview | -- | AF-2028, AF-2029, AF-2035 | -- | core | plan D03 T15 §6 |  |
| IP-1525 | HDR merge alignment by perspective or scaling | -- | AF-2030 | -- | core | plan D03 T15 §6 | alignment engine D03 T15 §5 |
| IP-1526 | HDR merge ghost removal | -- | AF-2031 | -- | core | plan D03 T15 §6 |  |
| IP-1527 | HDR merge noise reduction | -- | AF-2032 | -- | core | plan D03 T15 §6 |  |
| IP-1528 | After-merge action: tone mapping, tone compression adjustment, or none | -- | AF-2033 | -- | core | plan D03 T15 §6 |  |
| IP-1529 | HDR merge sources for clone retouching | -- | AF-2036 | -- | core | plan D03 T15 §9 | the merge sources join the D03 T15 §9 sources panel |
| IP-1530 | Merge to HDR: auto align, remove ghosts, output bit depth, 32-bit white point preview, response curve, hand-off to the develop filter | PS-B-0729, PS-B-0730, PS-B-0731, PS-B-0732, PS-B-0735, PS-B-0736 | -- | -- | automation | plan D03 T15 §6 |  |
| IP-1531 | New panorama stitching with image list, preview, and navigation | -- | AF-2037, AF-2038, AF-2039, AF-2046 | -- | core | plan D03 T15 §7 |  |
| IP-1532 | Multiple panorama detection in one batch | -- | AF-2040 | -- | core | plan D03 T15 §7 |  |
| IP-1533 | Transform source image tool | -- | AF-2041 | -- | core | plan D03 T15 §7 |  |
| IP-1534 | Panorama source image masks: add and erase | -- | AF-2042, AF-2043 | -- | core | plan D03 T15 §7 |  |
| IP-1535 | Panorama crop and crop to opaque | -- | AF-2044 | -- | core | plan D03 T15 §7 |  |
| IP-1536 | Inpaint missing panorama areas | -- | AF-2045 | -- | core | plan D03 T15 §7 | classical fill via D03 T13 §3 |
| IP-1537 | Photomerge panorama | PS-A-1458 | -- | -- | automation | plan D03 T15 §7 |  |
| IP-1538 | Photomerge panorama layouts: auto, perspective, cylindrical, spherical, collage, reposition, file and folder sources | PS-B-0739, PS-B-0740, PS-B-0741, PS-B-0742, PS-B-0743, PS-B-0744, PS-B-0745, PS-B-0750 | -- | -- | automation | plan D03 T15 §7 |  |
| IP-1539 | Photomerge options: blend images, vignette removal, geometric distortion correction, content-aware fill of transparent areas | PS-B-0746, PS-B-0747, PS-B-0748, PS-B-0749 | -- | -- | automation | plan D03 T15 §7 |  |
| IP-1540 | Auto-blend layers | PS-A-1248 | -- | -- | core | plan D03 T15 §8 |  |
| IP-1541 | Auto-blend layers: panorama, stack, seamless tones, fill transparent areas | PS-A-0954, PS-A-0955, PS-A-0956, PS-A-0957, PS-A-0958 | -- | -- | core | plan D03 T15 §8 | Focus stacking mode shares D03 T15 §9 |
| IP-1542 | Smart object stack modes | PS-A-0718, PS-A-0719, PS-A-0720, PS-A-0721, PS-A-0722, PS-A-0723, PS-A-0724, PS-A-0725, PS-A-0726, PS-A-0727, PS-A-0728, PS-A-0729 | -- | -- | core | plan D03 T15 §8 |  |
| IP-1543 | Live stack group from new stack | -- | AF-2047, AF-2051 | -- | core | plan D03 T15 §8 |  |
| IP-1544 | Stack auto-align with perspective or scaling model | -- | AF-2048, AF-2049 | -- | core | plan D03 T15 §8 | alignment engine D03 T15 §5 |
| IP-1545 | Live alignment filter per stack layer | -- | AF-2050 | -- | core | plan D03 T15 §8 |  |
| IP-1546 | Stack modes: mean, median, outlier, maximum, minimum, range, mid-range, total | -- | AF-2052, AF-2053, AF-2054, AF-2055, AF-2056, AF-2057, AF-2058, AF-2059 | -- | core | plan D03 T15 §8 |  |
| IP-1547 | Analytical stack modes: standard deviation, variance, skewness, kurtosis, entropy | -- | AF-2060, AF-2061, AF-2062, AF-2063, AF-2064 | -- | core | plan D03 T15 §8 |  |
| IP-1548 | Stack recipes: exposure merge, noise reduction, object removal, light trails | -- | AF-2065, AF-2066, AF-2067, AF-2068 | -- | core | plan D03 T15 §8 |  |
| IP-1549 | Auto-Blend Layers: panorama and stack modes, seamless tones | PS-B-0752 | -- | -- | automation | plan D03 T15 §8 |  |
| IP-1550 | Statistics and smart object stack modes | PS-B-0776, PS-B-0777 | -- | -- | automation | plan D03 T15 §8 |  |
| IP-1551 | Focus merge with staged preview | -- | AF-2069, AF-2071 | -- | core | plan D03 T15 §9 |  |
| IP-1552 | Focus merge RAW development preset | -- | AF-2070 | -- | core | plan D03 T15 §9 |  |
| IP-1553 | Focus merge source cloning | -- | AF-2072 | -- | core | plan D03 T15 §9 |  |
| IP-1554 | Sources panel: global clone sources with preview, add, delete | -- | AF-2073, AF-2074, AF-2075, AF-2076 | -- | core | plan D03 T15 §9 | feeds clone, healing, patch in D03 T13 |
| IP-1555 | Tone stretch adjustment: basic, arcsinh, logarithmic, auto for FITS, live stretch | -- | AF-1368, AF-1369, AF-1370, AF-1371, AF-1372, AF-1373, AF-1374 | -- | core | plan D03 T15 §14 |  |
| IP-1556 | Astrophotography background removal with sample handles, radius, gray and RGB subtraction, output black level | -- | AF-1843, AF-1844, AF-1845, AF-1846, AF-1847, AF-1848, AF-1849, AF-1850, AF-1851 | -- | core | plan D03 T15 §14 | Classical gradient and light pollution subtraction, not AI subject removal |
| IP-1557 | Astrophotography: color map mono layers, enhance structure | -- | AF-1852, AF-1859 | -- | core | plan D03 T15 §14 |  |
| IP-1558 | Astrophotography tone filters: linear fit, auto stretch, color calibration | -- | AF-1853, AF-1855, AF-1856 | -- | core | plan D03 T15 §14 |  |
| IP-1559 | Separate luminosity and color, separate stars and background | -- | AF-1854, AF-1857 | -- | core | plan D03 T15 §14 | Classical star detection |
| IP-1560 | Align layers by stars | -- | AF-1860 | -- | core | plan D03 T15 §10 | Uses alignment engine D03 T15 §5 |
| IP-1561 | Astrophotography stack studio | -- | AF-0014, AF-2077 | -- | core | plan D03 T15 §10 |  |
| IP-1562 | Astrophotography studio with align by stars and color map buttons | -- | AF-0015, AF-2078, AF-2106 | -- | core | plan D03 T15 §10 |  |
| IP-1563 | Calibration frames: dark, bias, flat, dark flat | -- | AF-2079 | -- | core | plan D03 T15 §10 |  |
| IP-1564 | Astro files panel: file groups, frame type, add and remove files | -- | AF-2082, AF-2084, AF-2085 | -- | core | plan D03 T15 §10 |  |
| IP-1565 | Narrowband filter tags for simultaneous stacking | -- | AF-2083 | -- | core | plan D03 T15 §10 |  |
| IP-1566 | Select best light frames | -- | AF-2086 | -- | core | plan D03 T15 §10 |  |
| IP-1567 | Background calibration of light frames | -- | AF-2087 | -- | core | plan D03 T15 §10 |  |
| IP-1568 | Astro stacking: mean, median, sigma clipping with threshold and iterations | -- | AF-2088, AF-2089, AF-2090 | -- | core | plan D03 T15 §10 |  |
| IP-1569 | Astro demosaic method, white balance, subtract black level | -- | AF-2091, AF-2092, AF-2093 | -- | core | plan D03 T15 §10 |  |
| IP-1570 | Stack command, stacked images panel, apply as layers | -- | AF-2094, AF-2095, AF-2100 | -- | core | plan D03 T15 §10 |  |
| IP-1571 | Channel color mapping and narrowband compositing | -- | AF-2096, AF-2097, AF-2103 | -- | core | plan D03 T15 §14 |  |
| IP-1572 | Live tone stretch and tone stretch adjustment | -- | AF-2098, AF-2104 | -- | core | plan D03 T15 §14 |  |
| IP-1573 | Bad pixel map tool: automatic hot and cold detection with thresholds | -- | AF-0400, AF-0402, AF-0403, AF-0404, AF-2099 | -- | core | plan D03 T15 §10 |  |
| IP-1574 | Bad pixel map manual marking by pixel or column, show, Bayer view, reset | -- | AF-0405, AF-0406, AF-0407, AF-0408 | -- | core | plan D03 T15 §10 |  |
| IP-1575 | Bad pixel map presets | -- | AF-0401 | -- | core | plan D03 T15 §10 |  |
| IP-1576 | Align by stars | -- | AF-2101 | -- | core | plan D03 T15 §10 |  |
| IP-1577 | Color map mono layers filter | -- | AF-2102 | -- | core | plan D03 T15 §14 |  |
| IP-1578 | Astro filters: auto stretch and background gradient removal | -- | AF-2105 | -- | core | plan D03 T15 §14 |  |
| IP-1579 | Crop and Straighten Photos | PS-B-0724 | -- | -- | automation | plan D03 T15 §11 |  |
| IP-1580 | ML star and background separation | -- | AF-1858 | -- | ai | backlog B-046 | On-device star-removal model; classical separation in D03 T15 §10 |
| IP-1581 | macOS EDR preview options | -- | AF-1352, AF-1354, AF-1357 | -- | core | excluded: platform | macOS EDR only; Windows HDR counterpart planned |

## Type

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1582 | Type layer | PS-A-0689 | -- | -- | core | plan D03 T16 §1 |  |
| IP-1583 | Edit text on canvas from the Layers panel | -- | -- | GP-3737 | core | plan D03 T16 §9 |  |
| IP-1584 | Horizontal type tool with point and paragraph text, resizable text box, and GIMP dynamic or fixed box | PS-A-0433, PS-A-0446, PS-A-0447, PS-A-0448 | AF-0435 | GP-0179, GP-0209 | core | plan D03 T16 §9 | Shaping is the Nodus HarfBuzz engine moved to Photon.Core; Affinity Artistic Text maps to point text |
| IP-1585 | Vertical type tool, toggle orientation, and vertical Roman alignment | PS-A-0434, PS-A-0437, PS-A-1560, PS-A-1561, PS-A-1613 | -- | GP-0215, GP-0216, GP-0217, GP-0218 | core | plan D03 T16 §9 | GIMP mixed and upright vertical orientations included |
| IP-1586 | Horizontal and vertical type mask tools | PS-A-0435, PS-A-0436, PS-A-1631 | -- | -- | core | plan D03 T16 §9 | Result is a selection, not a text layer |
| IP-1587 | On-canvas text editing: commit or cancel, double-click to edit, transform while editing, floating style editor | PS-A-0451, PS-A-0452, PS-A-0453, PS-A-1633, PS-A-1634 | -- | GP-0041, GP-0063, GP-0064, GP-0099, GP-0184 | core | plan D03 T16 §9 | GIMP on-canvas editor is draggable and toggleable; masked text layers stay clickable |
| IP-1588 | Text editor window with load from file and clear all | -- | -- | GP-0180, GP-0183, GP-0211, GP-0212 | core | plan D03 T16 §9 |  |
| IP-1589 | Convert text to work path or shape layer | PS-A-1616, PS-A-1617 | -- | -- | core | plan D03 T16 §9 | Outlines feed paths D03 T16 §5 and shapes §7 |
| IP-1590 | Rasterize type layer | PS-A-1618 | -- | -- | core | plan D03 T16 §1 |  |
| IP-1591 | World-ready text engine and language options | PS-A-1608, PS-A-1609, PS-A-1623 | -- | -- | core | plan D03 T16 §1 | One HarfBuzz engine handles all scripts; the option selects the feature set shown |
| IP-1592 | Character panel with font family, style, and size, panel toggles, and reset | PS-A-0438, PS-A-0439, PS-A-0444, PS-A-1534, PS-A-1535, PS-A-1536, PS-A-1537, PS-A-1562, PS-A-1611 | -- | GP-0181, GP-0182, GP-0219 | core | plan D03 T16 §2 |  |
| IP-1593 | Accurate font face grouping: true bold and italic faces per family | -- | -- | GP-0038 | core | plan D03 T16 §2 |  |
| IP-1594 | Change font on multiple selected type layers | PS-A-1569 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1595 | Leading, kerning (metrics, optical, manual), and tracking | PS-A-1538, PS-A-1539, PS-A-1540 | -- | GP-0207, GP-0208 | core | plan D03 T16 §2 | GIMP line and letter spacing map here |
| IP-1596 | Vertical and horizontal scale and baseline shift | PS-A-1541, PS-A-1542, PS-A-1543 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1597 | Text color with float precision and live preview | PS-A-0442, PS-A-1544 | -- | GP-0039, GP-0065, GP-0187 | core | plan D03 T16 §2 |  |
| IP-1598 | Faux bold and italic, all caps, small caps, superscript, subscript, underline, strikethrough | PS-A-1546, PS-A-1547, PS-A-1548, PS-A-1549, PS-A-1550, PS-A-1551, PS-A-1552, PS-A-1553 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1599 | Text anti-aliasing methods and hinting | PS-A-0440, PS-A-1556, PS-A-1612 | -- | GP-0185, GP-0186 | core | plan D03 T16 §2 |  |
| IP-1600 | Fractional widths, system layout, and no break | PS-A-1557, PS-A-1558, PS-A-1559 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1601 | Language dictionary for hyphenation and spelling | PS-A-1555 | -- | GP-0210 | core | plan D03 T16 §2 |  |
| IP-1602 | Font menu filters, favorites, similar fonts, and preview size | PS-A-1564, PS-A-1565, PS-A-1566, PS-A-1622 | -- | GP-0081 | core | plan D03 T16 §2 | Similar fonts by local font metrics comparison, no cloud |
| IP-1603 | Fonts dialog: grid and list, search, refresh font list, fast font loading | -- | -- | GP-0098, GP-3788, GP-3789, GP-3790, GP-3791 | core | plan D03 T16 §2 |  |
| IP-1604 | OpenType features: Character panel buttons, OpenType submenu, on-canvas glyph alternates | PS-A-1554, PS-A-1595, PS-A-1596, PS-A-1614 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1605 | Variable font axis sliders | PS-A-1597 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1606 | OpenType SVG color fonts and emoji composition | PS-A-1598, PS-A-1599 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1607 | Glyphs panel with show filter, recent glyphs, search, and zoom | PS-A-1600, PS-A-1601, PS-A-1602, PS-A-1603, PS-A-1604 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1608 | Glyph protection against wrong-font substitution | PS-A-1605 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1609 | Non-destructive text outline: filled, outlined, or both, direction, color or pattern, width, caps, joins, miter, dashes | -- | -- | GP-0040, GP-0066, GP-0188, GP-0189, GP-0190, GP-0191, GP-0192, GP-0193, GP-0194, GP-0195, GP-0196, GP-0197, GP-0198, GP-0199, GP-0200, GP-0201, GP-0202, GP-0203, GP-0204 | core | plan D03 T16 §2 | GIMP 3 text outline; stroke options shared with D03 T16 §7 |
| IP-1610 | Character panel and Glyphs panel | PS-B-1339, PS-B-1344 | -- | -- | core | plan D03 T16 §2 |  |
| IP-1611 | Paragraph panel alignment and justification, with reset | PS-A-0441, PS-A-1570, PS-A-1571, PS-A-1572, PS-A-1588 | -- | GP-0205 | core | plan D03 T16 §3 |  |
| IP-1612 | Paragraph indents and space before and after | PS-A-1573, PS-A-1574, PS-A-1575, PS-A-1576, PS-A-1577 | -- | GP-0206 | core | plan D03 T16 §3 |  |
| IP-1613 | Hyphenation and hyphenation settings | PS-A-1578, PS-A-1579 | -- | -- | core | plan D03 T16 §3 |  |
| IP-1614 | Justification settings and single-line, every-line, and world-ready composers | PS-A-1580, PS-A-1581, PS-A-1582 | -- | -- | core | plan D03 T16 §3 |  |
| IP-1615 | Roman hanging punctuation | PS-A-1583 | -- | -- | core | plan D03 T16 §3 |  |
| IP-1616 | Bulleted and numbered lists | PS-A-1586, PS-A-1587 | -- | -- | core | plan D03 T16 §3 |  |
| IP-1617 | Frame text tool with vertical alignment | -- | AF-0436 | -- | core | plan D03 T16 §3 | Affinity frame text; lists share the list row |
| IP-1618 | Paragraph panel | PS-B-1353 | -- | -- | core | plan D03 T16 §3 |  |
| IP-1619 | Check spelling | PS-A-1232 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1620 | Find and replace text | PS-A-1233 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1621 | Text along path and text to path commands | -- | -- | GP-1423, GP-1424, GP-1426 | core | plan D03 T16 §4 |  |
| IP-1622 | Convert between point and paragraph text | PS-A-0449, PS-A-1619 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1623 | Placeholder text: fill new type layers and paste Lorem Ipsum | PS-A-0450, PS-A-1626 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1624 | Character and paragraph styles panels with style options, redefine, clear override, load and default styles | PS-A-1589, PS-A-1590, PS-A-1591, PS-A-1592, PS-A-1593, PS-A-1594, PS-A-1627 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1625 | Find and replace text | PS-A-1629 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1626 | Check spelling | PS-A-1628 | -- | -- | core | plan D03 T16 §4 | Uses the Windows spell checker per language |
| IP-1627 | Manage missing fonts and update all text layers | PS-A-1568, PS-A-1624, PS-A-1625 | -- | -- | core | plan D03 T16 §4 | Replaces with installed fonts only; no Adobe Fonts activation |
| IP-1628 | East Asian options: tsume, kinsoku, and mojikumi | PS-A-1545, PS-A-1584 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1629 | Right-to-left and Middle Eastern options: paragraph direction, digits, diacritic position | PS-A-1563, PS-A-1585 | -- | GP-0213, GP-0214 | core | plan D03 T16 §4 |  |
| IP-1630 | Warp text with styles, axis, bend, and distortion | PS-A-0443, PS-A-1620, PS-A-1641, PS-A-1642, PS-A-1643, PS-A-1644, PS-A-1645 | -- | -- | core | plan D03 T16 §4 | Warp styles shared with D03 T13 §6 |
| IP-1631 | Type on a path: open path, inside closed shape, flip, start and end markers, edit path | PS-A-1635, PS-A-1636, PS-A-1637, PS-A-1638, PS-A-1639, PS-A-1640 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1632 | Dynamic text presets with spacing, position, direction, dynamic fit, and on-canvas endpoints | PS-A-1646, PS-A-1647, PS-A-1648, PS-A-1649, PS-A-1650, PS-A-1651, PS-A-1652 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1633 | Character and paragraph styles panels | PS-B-1340, PS-B-1354 | -- | -- | core | plan D03 T16 §4 |  |
| IP-1634 | Additional spelling dictionary folder | -- | AF-2714 | -- | core | plan D03 T16 §4 |  |
| IP-1635 | Adobe Fonts activation and browsing | PS-A-1567, PS-A-1610 | -- | -- | cloud | excluded: cloud | Adobe cloud font service |
| IP-1636 | 3D extrusion from text | PS-A-0445, PS-A-1615 | -- | -- | 3d | excluded: removed | Legacy 3D removed by Adobe |
| IP-2371 | Insert image metadata fields (EXIF, IPTC, file properties) as text in a text layer | -- | -- | -- | core | plan D03 T16 §4 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1354; AC-3061, AC-3062); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T16 §4 |

## Paths, shapes, and vectors

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1637 | Show target path | PS-A-1728 | -- | -- | core | plan D03 T16 §5 |  |
| IP-1638 | Import SVG paths with scale to fit image | -- | -- | GP-0118 | format | plan D03 T16 §10 |  |
| IP-1639 | Export paths to Illustrator | PS-B-0914 | -- | -- | core | plan D03 T16 §10 | writes a PDF-compatible AI path file |
| IP-1640 | Convert top-level clipping to clipping paths on JPEG and TIFF export | -- | AF-2562 | -- | format | plan D03 T16 §10 |  |
| IP-1641 | Paths panel with work path, thumbnails, rename, deselect, multi-select, and panel options | PS-A-1481, PS-A-1482, PS-A-1493, PS-A-1494, PS-A-1495 | -- | GP-3963, GP-3965, GP-3966, GP-3967, GP-3973, GP-3974, GP-3975, GP-3984, GP-3985 | core | plan D03 T16 §5 | GIMP Paths dialog merged; path geometry in Photon.Core |
| IP-1642 | Path management: new, save work path, duplicate, delete, raise and lower | PS-A-1483, PS-A-1484, PS-A-1485, PS-A-1486 | -- | GP-3976, GP-3977, GP-3978, GP-3979, GP-3983, GP-3987, GP-3988, GP-3989, GP-3990, GP-3991 | core | plan D03 T16 §5 |  |
| IP-1643 | Path visibility, lock attributes, and color tags | -- | -- | GP-3968, GP-3969, GP-3970, GP-3971, GP-3972, GP-3986 | core | plan D03 T16 §5 |  |
| IP-1644 | Fill path with color, pattern, or history | PS-A-1487 | -- | GP-3999 | core | plan D03 T16 §5 | Fill engine D03 T12 §8 |
| IP-1645 | Stroke path with a painting tool or line style, simulate pressure | PS-A-1488 | -- | GP-3982, GP-4000 | core | plan D03 T16 §5 | Stroke engine D03 T12 §8 |
| IP-1646 | Path to selection with replace, add, subtract, intersect | PS-A-1489 | -- | GP-3980, GP-3994, GP-3995, GP-3996, GP-3997 | core | plan D03 T16 §5 |  |
| IP-1647 | Selection to path with tolerance and advanced settings | PS-A-1490 | -- | GP-3981, GP-3998 | core | plan D03 T16 §5 |  |
| IP-1648 | Clipping path with flatness for export | PS-A-1492 | -- | -- | print | plan D03 T16 §5 |  |
| IP-1649 | Export paths to Illustrator | PS-A-1496 | -- | -- | format | plan D03 T16 §10 | Writes paths as a PostScript-based .ai file |
| IP-1650 | Merge visible paths | -- | -- | GP-3992 | core | plan D03 T16 §10 |  |
| IP-1651 | Copy and paste paths between images | -- | -- | GP-4001, GP-4002 | core | plan D03 T16 §10 |  |
| IP-1652 | Import and export paths as SVG | -- | -- | GP-4003, GP-4004 | core | plan D03 T16 §10 |  |
| IP-1653 | Path operations: combine, subtract front, intersect, exclude, merge components | PS-A-0418, PS-A-0432, PS-A-1661, PS-A-1662, PS-A-1663, PS-A-1664, PS-A-1665 | -- | -- | core | plan D03 T16 §10 | Applies to shape layers in D03 T16 §7 |
| IP-1654 | Align, distribute, and arrange path components | PS-A-0419, PS-A-0420 | -- | -- | core | plan D03 T16 §10 |  |
| IP-1655 | Paths panel | PS-B-1355 | -- | -- | core | plan D03 T16 §5 |  |
| IP-1656 | Pen tool with Bezier anchors, close and continue path, modifiers, and add subpaths to selected curves | PS-A-0404, PS-A-0425, PS-A-1653, PS-A-1654, PS-A-1655 | AF-0409, AF-0410, AF-0414, AF-0415 | GP-0149 | core | plan D03 T16 §6 | GIMP Paths tool design mode and Affinity Pen mode |
| IP-1657 | GIMP path tool edit modes: design, edit, move with modifier keys | -- | -- | GP-0151, GP-0152, GP-0153, GP-0154, GP-0155, GP-0156 | core | plan D03 T16 §6 |  |
| IP-1658 | Pen smart, polygon, and line modes | -- | AF-0411, AF-0412, AF-0413 | GP-0157 | core | plan D03 T16 §6 | GIMP polygonal option merged |
| IP-1659 | Freeform pen with curve fit | PS-A-0405, PS-A-0407 | -- | -- | core | plan D03 T16 §6 |  |
| IP-1660 | Magnetic pen with width, contrast, frequency, pressure | PS-A-0406 | -- | -- | core | plan D03 T16 §6 |  |
| IP-1661 | Curvature pen | PS-A-0410 | -- | -- | core | plan D03 T16 §6 |  |
| IP-1662 | Content-aware tracing tool with detail | PS-A-0408, PS-A-0409 | -- | -- | ai | plan D03 T16 §6 | Classical edge detection, no ML model; shares the D03 T10 §5 scissors engine |
| IP-1663 | Add, delete, and convert anchor point tools with auto add or delete and sharp, smooth, smart node types | PS-A-0411, PS-A-0412, PS-A-0413, PS-A-0423 | AF-0419, AF-0425 | GP-0174, GP-0176 | core | plan D03 T16 §6 |  |
| IP-1664 | Curve actions: split, break, close, join, reverse, smooth, shift start, delete segment | PS-A-1656, PS-A-1658 | AF-0420, AF-0426 | GP-0150, GP-0175, GP-0177, GP-0178 | core | plan D03 T16 §6 |  |
| IP-1665 | Pen output mode: shape layer, path, or pixels, with line style and fill while drawing | PS-A-0414 | AF-0423 | -- | core | plan D03 T16 §6 |  |
| IP-1666 | Make selection or shape from the pen options | PS-A-0415, PS-A-0417 | AF-0418 | GP-0158 | core | plan D03 T16 §6 |  |
| IP-1667 | Rubber band preview | PS-A-0421 | AF-0416 | -- | core | plan D03 T16 §6 |  |
| IP-1668 | Path display options: thickness, color, and direction indicator | PS-A-0422 | AF-0422, AF-0430 | -- | core | plan D03 T16 §6 |  |
| IP-1669 | Align vector edges and snap vector tools to the pixel grid | PS-A-0424, PS-A-1672 | -- | -- | core | plan D03 T16 §6 |  |
| IP-1670 | Node and pen snapping options | -- | AF-0421, AF-0429 | -- | core | plan D03 T16 §6 | Snapping engine D03 T08 §4 |
| IP-1671 | Path and direct selection tools with layer scope, marquee, duplicate by drag, transform controls | PS-A-0426, PS-A-0427, PS-A-0428, PS-A-0430, PS-A-0431, PS-A-1657, PS-A-1659 | AF-0424, AF-0428 | -- | core | plan D03 T16 §6 | Affinity Node tool merged |
| IP-1672 | Transform path and selected anchors | PS-A-1660 | AF-0427 | -- | core | plan D03 T16 §6 |  |
| IP-1673 | Shapes panel | PS-A-1447 | -- | -- | core | plan D03 T16 §11 |  |
| IP-1674 | Define custom shape | PS-A-1251 | -- | -- | core | plan D03 T16 §11 |  |
| IP-1675 | Gfig geometric figures: lines, rectangles, circles, ellipses, arcs, polygons, stars, spirals, curves, stroke, fill, grid snap | -- | -- | GP-3099, GP-3100, GP-3101, GP-3102, GP-3103, GP-3104, GP-3105, GP-3106, GP-3107, GP-3108, GP-3109, GP-3110, GP-3111, GP-3112, GP-3113, GP-3114, GP-3115, GP-3116, GP-3117, GP-3118, GP-3119, GP-3120, GP-3121, GP-3122, GP-3123, GP-3124, GP-3125, GP-3126, GP-3127, GP-3128, GP-3129 | core | plan D03 T16 §11 | Gfig job met by shape tools and shape layers, rasterized on demand |
| IP-1676 | Shape layer | PS-A-0690 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1677 | Edit vector layer on canvas | -- | -- | GP-3738 | core | plan D03 T16 §11 | GIMP 3.2 vector layers |
| IP-1678 | Combine shapes: unite, subtract, intersect, exclude | PS-A-0671 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1679 | Rectangle and ellipse tools with per-corner radius and on-canvas corner widgets | PS-A-0454, PS-A-0455, PS-A-0468, PS-A-0478 | AF-0431 | -- | core | plan D03 T16 §7 |  |
| IP-1680 | Corner types: rounded, straight, concave, cutout, absolute or relative | -- | AF-0432 | -- | core | plan D03 T16 §7 |  |
| IP-1681 | Triangle tool with corner radius | PS-A-0456 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1682 | Polygon and star tool with sides, star ratio, smooth indents and corners | PS-A-0457, PS-A-0469, PS-A-0470, PS-A-0471, PS-A-0472 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1683 | Line tool with weight and arrowheads | PS-A-0458, PS-A-0473, PS-A-0474 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1684 | Custom shape tool, shape picker, legacy shapes, define custom shape | PS-A-0459, PS-A-0476, PS-A-0477, PS-A-1673 | -- | -- | core | plan D03 T16 §11 | CSH import |
| IP-1685 | Additional shape tools: rounded rectangle, star variants, diamond, trapezoid, cog, crescent, donut, and more | -- | AF-0434 | -- | core | plan D03 T16 §7 |  |
| IP-1686 | Shape fill and stroke paint: solid, gradient, pattern, none, with gradient and pattern options | PS-A-0460, PS-A-0461, PS-A-0462, PS-A-1667, PS-A-1668 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1687 | Stroke options: align, caps, corners, dashes, and saved stroke presets | PS-A-0463, PS-A-0464, PS-A-0465, PS-A-0466, PS-A-1669 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1688 | Shape geometry: W, H, X, Y, drawing constraints, keep selected | PS-A-0429, PS-A-0467, PS-A-0475, PS-A-1674 | AF-0433 | -- | core | plan D03 T16 §7 |  |
| IP-1689 | Live shape properties and conversion to regular path | PS-A-1666, PS-A-1675 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1690 | Shape pixels mode | PS-A-0479 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1691 | Merge shape layers | PS-A-1670 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1692 | Rasterize shape | PS-A-1671 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1693 | Vector layers from paths with non-destructive transform and drop to fill | -- | -- | GP-0053, GP-0056, GP-0057, GP-0159, GP-3993 | core | plan D03 T16 §11 | GIMP 3.2 vector layers; layer kind in D03 T09 §1 |
| IP-1694 | Vector layer fill and stroke: color or pattern, antialias, width, cap, join, miter, dashes | -- | -- | GP-0054, GP-0055, GP-0160, GP-0161, GP-0162, GP-0163, GP-0164, GP-0165, GP-0166, GP-0167, GP-0168, GP-0169, GP-0170, GP-0171, GP-0172, GP-0173 | core | plan D03 T16 §11 |  |
| IP-1695 | Live shape properties in the Properties panel: per-corner radii and shape operations | PS-A-1522, PS-A-1523 | -- | -- | core | plan D03 T16 §7 |  |
| IP-1696 | Shapes panel and legacy shape tool option | PS-B-1240, PS-B-1358 | -- | -- | core | plan D03 T16 §11 |  |
| IP-1697 | SVG export: vector layers, embed raster layers as PNG or JPEG or omit | PS-B-1032 | -- | GP-4706, GP-4707, GP-4708, GP-4709, GP-4710, GP-4830 | format | plan D03 T16 §8 |  |
| IP-1698 | Frames: frame from layers and convert to frame | PS-A-0636, PS-A-0637, PS-A-0693 | -- | -- | core | plan D03 T16 §8 |  |
| IP-1699 | Copy CSS and SVG from layers | PS-A-0640, PS-A-0641 | AF-0961 | -- | format | plan D03 T16 §8 |  |
| IP-1700 | SVG export options: text spans, hex colors, flatten transforms, viewBox, relative coordinates | -- | AF-2561, AF-2535 | -- | format | plan D03 T16 §8 |  |
| IP-1701 | Frame tool: rectangle and ellipse frames with placed content, convert to frame, frame or content selection | PS-A-0174, PS-A-0175, PS-A-0176, PS-A-0177, PS-A-0178, PS-A-0179 | -- | -- | core | plan D03 T16 §8 |  |
| IP-1702 | Frame properties: stroke, W, H, X, Y, placed content status | PS-A-0180, PS-A-0181, PS-A-0182 | -- | -- | core | plan D03 T16 §8 |  |
| IP-1703 | Copy items as SVG | -- | AF-2654 | -- | core | plan D03 T16 §8 |  |

## File menu and formats

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1704 | Open documents and images, including vector files | -- | AF-2346 | -- | core | plan D03 T17 §1 | extends D03 T04 §2 |
| IP-1705 | Drag a file or asset to open as a new document | -- | AF-2324, AF-2348 | -- | core | plan D03 T17 §1 |  |
| IP-1706 | Revert to saved | -- | -- | GP-0877 | core | plan D03 T17 §1 |  |
| IP-1707 | Close, close others, close all | -- | AF-2355 | -- | core | plan D03 T17 §1 |  |
| IP-1708 | Open dialog: browse, search, bookmarks, columns, hidden files | PS-B-0885 | -- | GP-0803, GP-0804, GP-0805, GP-0807, GP-0808, GP-0809, GP-0810, GP-0811, GP-0812, GP-0813, GP-0814, GP-0815, GP-0816, GP-0817, GP-0818, GP-0841, GP-0866 | core | plan D03 T17 §1 | Windows common file dialog supplies most options |
| IP-1709 | Open As a specific format | PS-B-0887 | -- | -- | core | plan D03 T17 §1 |  |
| IP-1710 | Open as smart object or as layers | PS-B-0888 | -- | GP-0858 | core | plan D03 T17 §1 |  |
| IP-1711 | Open from Windows shell and drag and drop to open or place | PS-B-0944 | -- | GP-0103 | core | plan D03 T17 §1 | single running instance |
| IP-1712 | Close all and close others | PS-B-0892, PS-B-0893 | -- | GP-0820 | core | plan D03 T17 §1 |  |
| IP-1713 | Save a copy and flattening formats in Save a Copy | PS-B-0897, PS-B-1035 | -- | GP-0869 | core | plan D03 T17 §1 |  |
| IP-1714 | Save content options: layers, alpha channels, spot colors, notes | PS-B-0898 | -- | -- | core | plan D03 T17 §1 |  |
| IP-1715 | Format list: bit depth and mode support matrix, customize list, legacy Save As | PS-B-0900, PS-B-1034, PS-B-1036 | -- | -- | format | plan D03 T17 §1 |  |
| IP-1716 | Revert | PS-B-0901 | -- | GP-0868 | core | plan D03 T17 §1 |  |
| IP-1717 | Export and overwrite semantics, save over image formats | -- | AF-2597 | GP-0819, GP-0839, GP-0840, GP-4326 | core | plan D03 T17 §15 |  |
| IP-1718 | Place embedded and place linked with placement preferences, PDF place | PS-B-0923, PS-B-0924, PS-B-0925, PS-B-0926, PS-B-0927 | AF-2611 | -- | core | plan D03 T17 §15 |  |
| IP-1719 | Import notes from PDF or FDF | PS-B-0933 | -- | -- | core | plan D03 T17 §15 |  |
| IP-1720 | Place embedded | PS-A-0701 | -- | -- | core | plan D03 T17 §15 | Creates a D03 T09 §9 smart object |
| IP-1721 | Load files into stack with auto align and convert to smart object | PS-B-0772, PS-B-0773, PS-B-0774 | -- | -- | automation | plan D03 T17 §15 |  |
| IP-1722 | Drop files on the document tab bar to open | -- | -- | GP-0071 | core | plan D03 T17 §12 |  |
| IP-1723 | Open from compressed archives (gz, bz2, xz, zip) | -- | -- | GP-4801 | format | plan D03 T17 §12 |  |
| IP-1724 | Open location (URL, file, http, https, ftp) | -- | -- | GP-0860, GP-0861, GP-0862, GP-0863, GP-0864, GP-4873 | core | plan D03 T17 §12 |  |
| IP-1725 | Scanner and camera acquire via WIA | PS-B-0934 | -- | GP-0108, GP-0827 | core | plan D03 T17 §12 |  |
| IP-1726 | New from clipboard | -- | -- | GP-0825, GP-4872 | core | plan D03 T17 §12 |  |
| IP-1727 | Screenshot: window, screen, region, decorations, pointer, delay, monitor profile | -- | -- | GP-0824, GP-0826, GP-0828, GP-0829, GP-0830, GP-0831, GP-0832, GP-0833, GP-0834, GP-0835, GP-0836, GP-0837, GP-0838, GP-4871 | core | plan D03 T17 §12 | selection delay is not available on Windows |
| IP-1728 | Copy image location and show in file manager | -- | -- | GP-0822, GP-0872, GP-3774, GP-3775 | core | plan D03 T17 §12 |  |
| IP-1729 | Document history dialog | -- | -- | GP-3772, GP-3773 | core | plan D03 T17 §12 |  |
| IP-1730 | Send by email | -- | -- | GP-0102, GP-0874 | core | plan D03 T17 §12 | Windows MAPI email hand-off, closest is the File menu section |
| IP-1731 | Document history multi-select | -- | -- | GP-0080 | core | plan D03 T17 §12 |  |
| IP-1732 | Photoshop PSD write: layers, masks, styles, text, smart objects, maximize compatibility, CMYK, metadata, thumbnail | PS-B-0959, PS-B-0960, PS-B-0961, PS-B-1024 | AF-2599, AF-2604 | GP-4803, GP-4682, GP-4683, GP-4684, GP-4685, GP-4686, GP-4687, GP-4688, GP-4689 | format | plan D03 T17 §2 |  |
| IP-1733 | PSB large document read and write | PS-B-0962, PS-B-0963 | AF-2600 | GP-4804 | format | plan D03 T17 §2 | read side in D03 T17 §3 |
| IP-1734 | PSD export compatibility and smallest file size | -- | AF-2552, AF-2553 | -- | format | plan D03 T17 §13 | Maximize compatibility composite |
| IP-1735 | PSD export editability versus accuracy: rasterize layers, gradients, adjustments, effects, lines, blend ranges, text | -- | AF-2554, AF-2555, AF-2556, AF-2557, AF-2558, AF-2559, AF-2560 | -- | format | plan D03 T17 §13 | Imago writes live text and adjustments where the writer supports them |
| IP-1736 | PSD save preferences: disable compression, maximize compatibility, save over imported PSD | PS-B-1256, PS-B-1257 | AF-2653 | -- | core | plan D03 T17 §13 |  |
| IP-1737 | PSD import with live text and smart objects | -- | AF-2359, AF-2360, AF-2361 | -- | format | plan D03 T17 §3 | extends D03 T04 §5 |
| IP-1738 | PSD read fidelity: layers, groups, masks, paths, guides, layer styles, multichannel | -- | AF-2598 | GP-0090, GP-0116, GP-4802 | format | plan D03 T17 §3 | extends D03 T04 §5 |
| IP-1739 | PSD import options: smart objects as embedded documents, text as editable text | -- | AF-2601, AF-2603 | -- | format | plan D03 T17 §3 |  |
| IP-1740 | PSD smart objects import as editable placed documents | -- | AF-0825 | -- | format | plan D03 T17 §3 |  |
| IP-1741 | GIMP XCF read and write including compressed XCF and saved filter stacks | -- | -- | GP-0006, GP-4799, GP-4800 | format | plan D03 T17 §4 |  |
| IP-1742 | WebP open and export: lossy, lossless, quality, alpha quality, source preset, sharp YUV, metadata | PS-B-0993, PS-B-0994 | AF-2618 | GP-4747, GP-4748, GP-4749, GP-4750, GP-4751, GP-4752, GP-4754, GP-4755, GP-4756, GP-4757, GP-4758, GP-4759, GP-4811 | format | plan D03 T17 §5 | animation in B-044 |
| IP-1743 | AVIF open and export: lossless, quality, pixel format, bit depth, HDR PQ and HLG, speed, metadata | PS-B-0995, PS-B-0996 | -- | GP-4497, GP-4498, GP-4499, GP-4500, GP-4501, GP-4502, GP-4503, GP-4504, GP-4505, GP-4506, GP-4507, GP-4508, GP-4812 | format | plan D03 T17 §5 |  |
| IP-1744 | HEIF and HEIC open and export: quality, pixel format, bit depth, speed, depth map layer, metadata | PS-B-0997, PS-B-0998 | AF-2619 | GP-4509, GP-4510, GP-4511, GP-4512, GP-4513, GP-4514, GP-4515, GP-4516, GP-4517, GP-4518, GP-4519, GP-4520, GP-4813 | format | plan D03 T17 §5 |  |
| IP-1745 | HEJ2 export: JPEG 2000 in HEIF with quality, pixel format, bit depth, metadata | -- | -- | GP-4521, GP-4522, GP-4523, GP-4524, GP-4525, GP-4526, GP-4527, GP-4528, GP-4529, GP-4530, GP-4531, GP-4532, GP-4814 | format | plan D03 T17 §5 |  |
| IP-1746 | JPEG XL open and export: lossless, distance, effort, bit depth, CMYK, metadata | PS-B-0982, PS-B-0983 | AF-2620 | GP-4618, GP-4619, GP-4620, GP-4621, GP-4622, GP-4623, GP-4624, GP-4625, GP-4808 | format | plan D03 T17 §5 |  |
| IP-1747 | JPEG 2000 JP2 open and export: lossless, quality, ICT, resolutions, progression order, cinema profiles, tiles, ROI, metadata | PS-B-0979, PS-B-0980, PS-B-0981 | AF-2621 | GP-4573, GP-4574, GP-4575, GP-4576, GP-4577, GP-4578, GP-4579, GP-4580, GP-4581, GP-4582, GP-4583, GP-4584, GP-4585, GP-4586, GP-4587, GP-4588, GP-4589, GP-4809 | format | plan D03 T17 §5 |  |
| IP-1748 | JPEG 2000 codestream J2K open and export: ICT, CMYK, resolutions, progression order, compliance profile | -- | -- | GP-4558, GP-4559, GP-4560, GP-4561, GP-4562, GP-4563, GP-4564, GP-4565, GP-4566, GP-4567, GP-4568, GP-4569, GP-4570, GP-4571, GP-4572, GP-4810 | format | plan D03 T17 §5 |  |
| IP-1749 | JPEG XR open including HDR | -- | AF-2622 | -- | format | plan D03 T17 §5 | not in the §5 list, add it there |
| IP-1750 | QOI open and export | -- | -- | GP-4690, GP-4834 | format | plan D03 T17 §5 |  |
| IP-1751 | WebP lossless export | -- | AF-2568 | -- | format | plan D03 T17 §5 |  |
| IP-1752 | Gain map HDR JPEG and HEIF open | -- | AF-2026 | -- | format | plan D03 T17 §5 | HDR display via D03 T15 §4 |
| IP-1753 | Refine HEIC depth maps on import | -- | AF-2656 | -- | core | plan D03 T17 §5 |  |
| IP-1754 | OpenEXR alpha association, unpremultiply, perturb zero alpha, multichannel layers, export precision | -- | AF-2248, AF-2249, AF-2250, AF-2251, AF-2252 | -- | format | plan D03 T17 §6 |  |
| IP-1755 | HDR gain maps and CICP in JPEG and PNG, 32-bit PNG | PS-B-0989 | AF-2615, AF-2616 | -- | format | plan D03 T17 §6 | basic JPEG and PNG shipped in D03 T04 §2 |
| IP-1756 | OpenEXR open and export: compression, half or float, alpha, multichannel | PS-B-1003, PS-B-1004, PS-B-1005 | AF-2623 | GP-4476, GP-4816 | format | plan D03 T17 §6 |  |
| IP-1757 | Radiance HDR open and export | PS-B-1006 | AF-2624 | GP-4698, GP-4817 | format | plan D03 T17 §6 |  |
| IP-1758 | PFM open and export | -- | -- | GP-4640, GP-4818 | format | plan D03 T17 §6 |  |
| IP-1759 | PNM family (PBM, PGM, PPM, PAM) open and export, binary or ASCII | PS-B-1007, PS-B-1008 | -- | GP-4659, GP-4660, GP-4661, GP-4662, GP-4663, GP-4664, GP-4665, GP-4839 | format | plan D03 T17 §6 |  |
| IP-1760 | TIFF 32-bit float with predictor | PS-B-0972 | -- | -- | format | plan D03 T17 §6 | extends D03 T04 §3 |
| IP-1761 | FITS open and export | -- | AF-2630 | GP-4478, GP-4833 | format | plan D03 T17 §6 |  |
| IP-1762 | DICOM open and export: frames as layers, anonymize, overlays, window width and level | PS-B-1001, PS-B-1002 | -- | GP-4459, GP-4836 | format | plan D03 T17 §6 |  |
| IP-1763 | Photoshop Raw and raw image data: header, planar or contiguous, byte order, palette layout | PS-B-1011, PS-B-1012 | -- | GP-4691, GP-4692, GP-4693, GP-4694, GP-4695, GP-4696, GP-4697, GP-4870 | format | plan D03 T17 §6 |  |
| IP-1764 | OpenEXR compression and TIFF compression choices on export | -- | AF-2536 | -- | format | plan D03 T17 §6 | TIFF ZIP and LZW already D03 T04 §3; EXR ZIP, RLE, PIZ, PXR24 new |
| IP-1765 | OpenEXR color space from filename affix (OCIO) on import and export | -- | AF-2247, AF-2565 | -- | format | plan D03 T17 §6 | Needs OCIO config from D03 T18 §4 |
| IP-1766 | OpenEXR multichannel layers and half or full float per channel class | -- | AF-2566, AF-2567 | -- | format | plan D03 T17 §6 |  |
| IP-1767 | OpenEXR color space affix conversion on import | -- | AF-2020 | -- | format | plan D03 T17 §6 |  |
| IP-1768 | OpenEXR alpha options: associate, unpremultiply, perturb zero alpha | -- | AF-2021, AF-2022, AF-2023 | -- | format | plan D03 T17 §6 |  |
| IP-1769 | Multichannel OpenEXR import and export as layers | -- | AF-2024, AF-2025 | -- | format | plan D03 T17 §6 |  |
| IP-1770 | FITS open with Bayer pattern | -- | AF-2080, AF-2081 | -- | format | plan D03 T17 §6 | astro use in D03 T15 §10 |
| IP-1771 | Load multiple DICOM files into one document | PS-B-0775 | -- | -- | format | plan D03 T17 §6 |  |
| IP-1772 | PDF import options: pages, DPI, color space, editable text | -- | AF-2362 | -- | format | plan D03 T17 §7 |  |
| IP-1773 | PDF import: pages or images, crop box, size, resolution, reverse order, anti-aliasing, fill transparent | PS-B-1028, PS-B-1029 | AF-2608, AF-2609 | GP-4784, GP-4786, GP-4787, GP-4788, GP-4789, GP-4790, GP-4791, GP-4792, GP-4793, GP-4794, GP-4826 | format | plan D03 T17 §7 |  |
| IP-1774 | PostScript, EPS, and AI import: bounding box, coloring, text and graphic anti-aliasing | PS-B-1030 | AF-2606, AF-2607 | GP-4785, GP-4795, GP-4796, GP-4797, GP-4798, GP-4828 | print | plan D03 T17 §16 | external Ghostscript, AI through its embedded PDF stream, no AI export |
| IP-1775 | Photoshop PDF save: presets, PDF/X standards, compatibility, preserve editing, thumbnails, fast web view, summary | PS-B-1016, PS-B-1037, PS-B-1038, PS-B-1039, PS-B-1040, PS-B-1041, PS-B-1042, PS-B-1043, PS-B-1053, PS-B-1054 | AF-2610 | -- | format | plan D03 T17 §7 |  |
| IP-1776 | PDF presets manager | PS-B-1055 | -- | -- | format | plan D03 T17 §7 |  |
| IP-1777 | PDF compression: downsampling, ZIP, JPEG, JPEG 2000, 16 to 8 bit | PS-B-1044, PS-B-1045, PS-B-1046 | -- | -- | format | plan D03 T17 §7 |  |
| IP-1778 | PDF output: color conversion, profile inclusion, output intent | PS-B-1047, PS-B-1048, PS-B-1049 | -- | -- | format | plan D03 T17 §7 |  |
| IP-1779 | PDF security: open password, permissions, encryption level | PS-B-1050, PS-B-1051, PS-B-1052 | -- | -- | format | plan D03 T17 §7 |  |
| IP-1780 | PDF export: layers as pages, reverse order, root layers, apply masks, vectorize, omit hidden, fill transparent, text as image | -- | -- | GP-4631, GP-4632, GP-4633, GP-4634, GP-4635, GP-4636, GP-4637, GP-4638, GP-4639, GP-4827 | format | plan D03 T17 §7 |  |
| IP-1781 | Photoshop EPS save: preview, encoding, halftone screen, transfer, vector data | PS-B-1017, PS-B-1018, PS-B-1019, PS-B-1020 | AF-2613 | -- | format | plan D03 T17 §16 |  |
| IP-1782 | PostScript and EPS export: size, offset, unit, rotation, level 2, preview | -- | -- | GP-4460, GP-4461, GP-4462, GP-4463, GP-4464, GP-4465, GP-4466, GP-4467, GP-4468, GP-4469, GP-4470, GP-4471, GP-4472, GP-4473, GP-4474, GP-4475, GP-4666, GP-4667, GP-4668, GP-4669, GP-4670, GP-4671, GP-4672, GP-4673, GP-4674, GP-4675, GP-4676, GP-4677, GP-4678, GP-4679, GP-4680, GP-4681 | print | plan D03 T17 §16 |  |
| IP-1783 | SVG import (rasterize) | PS-B-1031 | AF-2612 | GP-4829 | format | plan D03 T17 §16 | SVG export in D03 T16 §8 |
| IP-1784 | WMF import | -- | -- | GP-4831 | format | plan D03 T17 §16 |  |
| IP-1785 | WMF and EMF export | -- | AF-2627 | -- | format | plan D03 T17 §16 | §7 lists metafile import only, add export there |
| IP-1786 | PDF export compatibility and PDF/X standards, open when complete | -- | AF-2542, AF-2551 | -- | print | plan D03 T17 §7 | PDF 1.4 to 2.0, PDF/X-1a, X-3, X-4 |
| IP-1787 | PDF export color: color space, output profile, spot colors, overprint black | -- | AF-2543, AF-2544 | -- | print | plan D03 T17 §7 | Engine D01 T04 |
| IP-1788 | PDF export layers as optional content | -- | AF-2545 | -- | print | plan D03 T17 §7 |  |
| IP-1789 | PDF export text and vectors: embed and subset fonts, text as curves, advanced features, hyperlinks and bookmarks | -- | AF-2548, AF-2549, AF-2534, AF-2546 | -- | print | plan D03 T17 §7 | Text as curves also applies to SVG and EPS |
| IP-1790 | PDF export printer marks: crop, registration, color bars, page information | -- | AF-2547 | -- | print | plan D03 T17 §7 | Mark drawing shared with D03 T18 §6 |
| IP-1791 | PDF export passwords and permissions | -- | AF-2550 | -- | print | plan D03 T17 §7 |  |
| IP-1792 | Vector-format export rasterization: raster DPI, rasterize nothing or everything or unsupported, downsample images | -- | AF-2522, AF-2523, AF-2524 | -- | core | plan D03 T17 §7 | Applies to PDF, SVG, EPS |
| IP-1793 | EPS export PostScript level and minimize size | -- | AF-2564 | -- | format | plan D03 T17 §16 |  |
| IP-1794 | WMF and EMF export with enhanced metafile and clip transparency | -- | AF-2563 | -- | format | plan D03 T17 §16 | skeleton lists WMF and EMF import only; export added here |
| IP-1795 | PDF presets manager | PS-B-1196 | -- | -- | format | plan D03 T17 §7 |  |
| IP-1796 | BMP open and export: RLE, color space info, 16, 24, 32 bit formats, OS/2, flip row order | PS-B-0999, PS-B-1000 | AF-2626 | GP-4356, GP-4357, GP-4358, GP-4359, GP-4360, GP-4361, GP-4362, GP-4363, GP-4364, GP-4365, GP-4824 | format | plan D03 T17 §8 |  |
| IP-1797 | GIF single frame open and export: indexed conversion, interlace, comment | PS-B-0990, PS-B-0991, PS-B-0992 | AF-2617 | GP-4483, GP-4484, GP-4485, GP-4486, GP-4825 | format | plan D03 T17 §8 | animation in B-044 |
| IP-1798 | ICO open and export: per-size save type, PNG compression | -- | -- | GP-4550, GP-4551, GP-4552, GP-4553, GP-4554, GP-4555, GP-4556, GP-4557, GP-4820 | format | plan D03 T17 §8 |  |
| IP-1799 | CUR open and export: save type, PNG compression, hot spot | -- | -- | GP-4383, GP-4384, GP-4385, GP-4386, GP-4387, GP-4388, GP-4389, GP-4390, GP-4391, GP-4392, GP-4821 | format | plan D03 T17 §8 |  |
| IP-1800 | ANI animated cursor open and export: name, author, delay, save type, hot spot | -- | -- | GP-4342, GP-4343, GP-4344, GP-4345, GP-4346, GP-4347, GP-4348, GP-4349, GP-4350, GP-4351, GP-4352, GP-4353, GP-4354, GP-4355, GP-4822 | format | plan D03 T17 §8 |  |
| IP-1801 | ICNS open and export with color profile | -- | -- | GP-4548, GP-4549, GP-4823 | format | plan D03 T17 §8 | not in the §8 list, add it there |
| IP-1802 | DDS open and export: BC1 to BC7 compression, formats, save types (cube, volume, array), flip, transparent index | -- | -- | GP-0036, GP-4393, GP-4394, GP-4395, GP-4396, GP-4397, GP-4398, GP-4399, GP-4400, GP-4401, GP-4402, GP-4403, GP-4404, GP-4405, GP-4406, GP-4407, GP-4408, GP-4409, GP-4410, GP-4411, GP-4412, GP-4413, GP-4414, GP-4415, GP-4416, GP-4417, GP-4418, GP-4419, GP-4420, GP-4421, GP-4422, GP-4423, GP-4424, GP-4425, GP-4426, GP-4427, GP-4428, GP-4429, GP-4430, GP-4435, GP-4436, GP-4819 | format | plan D03 T17 §8 |  |
| IP-1803 | DDS mipmaps: generate or keep, filters, wrap mode, gamma, alpha test coverage | -- | -- | GP-4431, GP-4432, GP-4433, GP-4434, GP-4437, GP-4438, GP-4439, GP-4440, GP-4441, GP-4442, GP-4443, GP-4444, GP-4445, GP-4446, GP-4447, GP-4448, GP-4449, GP-4450, GP-4451, GP-4452, GP-4453, GP-4454, GP-4455, GP-4456, GP-4457, GP-4458 | format | plan D03 T17 §8 |  |
| IP-1804 | TGA open and export: bits per pixel, RLE, origin | PS-B-1013, PS-B-1014 | AF-2625 | GP-4711, GP-4712, GP-4713, GP-4714, GP-4715, GP-4841 | format | plan D03 T17 §8 |  |
| IP-1805 | PCX and DCX open and PCX export | PS-B-1009 | -- | GP-4630, GP-4837, GP-4838 | format | plan D03 T17 §8 |  |
| IP-1806 | XBM open and export: X10, prefix, comment, hot spot, mask file | -- | -- | GP-4760, GP-4761, GP-4762, GP-4763, GP-4764, GP-4765, GP-4766, GP-4767, GP-4768, GP-4769, GP-4844 | format | plan D03 T17 §8 |  |
| IP-1807 | XPM open and export | -- | -- | GP-4782, GP-4845 | format | plan D03 T17 §8 |  |
| IP-1808 | XWD open and export | -- | -- | GP-4783, GP-4846 | format | plan D03 T17 §8 |  |
| IP-1809 | Sun raster open and export, RLE or standard | -- | -- | GP-4704, GP-4705, GP-4843 | format | plan D03 T17 §8 |  |
| IP-1810 | SGI open and export: none, RLE, aggressive RLE | -- | -- | GP-4699, GP-4700, GP-4701, GP-4702, GP-4703, GP-4842 | format | plan D03 T17 §8 |  |
| IP-1811 | Farbfeld open and export | -- | -- | GP-4477, GP-4851 | format | plan D03 T17 §8 |  |
| IP-1812 | WBMP open | -- | -- | GP-4840 | format | plan D03 T17 §8 |  |
| IP-1813 | GIMP 3 format additions: ICNS, CUR, ANI, ILBM, QOI, JPEG XL, DCX, PAM, WBMP | -- | -- | GP-0033 | format | plan D03 T17 §8 | QOI and JPEG XL in D03 T17 §5, ILBM in §9, PAM in §6 |
| IP-1814 | IFF and ILBM open | PS-B-1015 | -- | GP-4835 | format | plan D03 T17 §9 |  |
| IP-1815 | Pixar PXR open and save | PS-B-1010 | -- | -- | format | plan D03 T17 §9 |  |
| IP-1816 | Scitex CT save | PS-B-1023 | -- | -- | format | plan D03 T17 §9 |  |
| IP-1817 | Photoshop DCS 1.0 and 2.0: single or multiple files, composite | PS-B-1021, PS-B-1022 | -- | -- | format | plan D03 T17 §9 |  |
| IP-1818 | MPO multi-picture open | PS-B-1025 | -- | -- | format | plan D03 T17 §9 |  |
| IP-1819 | Paint Shop Pro PSP open with layers and selection shape | -- | -- | GP-0117, GP-4853 | format | plan D03 T17 §9 |  |
| IP-1820 | KiSS CEL open and export | -- | -- | GP-4366, GP-4848 | format | plan D03 T17 §9 |  |
| IP-1821 | Alias PIX open and export | -- | -- | GP-4641, GP-4854 | format | plan D03 T17 §9 |  |
| IP-1822 | PlayStation TIM open and export: type, image and palette origin | -- | -- | GP-4737, GP-4738, GP-4739, GP-4740, GP-4741, GP-4742, GP-4743, GP-4744, GP-4745, GP-4746, GP-4855 | format | plan D03 T17 §9 |  |
| IP-1823 | Game texture import: Dreamcast PVR, Arma PAA | -- | -- | GP-4856, GP-4858 | format | plan D03 T17 §9 |  |
| IP-1824 | Seattle FilmWorks SFW import | -- | -- | GP-4857 | format | plan D03 T17 §9 |  |
| IP-1825 | JIF import | -- | -- | GP-4859 | format | plan D03 T17 §9 |  |
| IP-1826 | C source export: name, comment, GLib types, macros, RLE, alpha, RGB565, opacity | -- | -- | GP-4373, GP-4374, GP-4375, GP-4376, GP-4377, GP-4378, GP-4379, GP-4380, GP-4381, GP-4382, GP-4868 | format | plan D03 T17 §9 |  |
| IP-1827 | C header export | -- | -- | GP-4496, GP-4869 | format | plan D03 T17 §9 |  |
| IP-1828 | HTML table export: full document, cellspan, compress tags, caption, cell content, border, size, padding, spacing | -- | -- | GP-4533, GP-4534, GP-4535, GP-4536, GP-4537, GP-4538, GP-4539, GP-4540, GP-4541, GP-4542, GP-4543, GP-4544, GP-4545, GP-4546, GP-4547, GP-4867 | format | plan D03 T17 §9 |  |
| IP-1829 | Colored HTML text export: characters, file source, font size, separate CSS | -- | -- | GP-4367, GP-4368, GP-4369, GP-4370, GP-4371, GP-4372, GP-4866 | format | plan D03 T17 §9 |  |
| IP-1830 | ASCII art export: text, HTML, ANSI, printer, IRC, man page formats | -- | -- | GP-4329, GP-4330, GP-4331, GP-4332, GP-4333, GP-4334, GP-4335, GP-4336, GP-4337, GP-4338, GP-4339, GP-4340, GP-4341, GP-4865 | format | plan D03 T17 §9 |  |
| IP-1831 | Export as GIMP brush (GBR) | -- | -- | GP-4482, GP-4860 | format | plan D03 T17 §9 |  |
| IP-1832 | Export as GIMP brush pipe (GIH) | -- | -- | GP-4495, GP-4861 | format | plan D03 T17 §9 |  |
| IP-1833 | Export as GIMP pattern (PAT) with description | -- | -- | GP-4628, GP-4629, GP-4862 | format | plan D03 T17 §9 |  |
| IP-1834 | JPEG encoding options: optimize, scans, subsampling, DCT method, arithmetic coding, restart markers, smoothing | PS-B-0977 | -- | GP-4594, GP-4595, GP-4598, GP-4599, GP-4600, GP-4601, GP-4602, GP-4603, GP-4604, GP-4605, GP-4606, GP-4607, GP-4608, GP-4609, GP-4610 | format | plan D03 T17 §11 | extends D03 T04 §2 |
| IP-1835 | JPEG export options: matte, size estimate, live preview, original quality, CMYK, EXIF, IPTC, XMP, thumbnail, comment | PS-B-0975, PS-B-0978 | -- | GP-4592, GP-4593, GP-4597, GP-4611, GP-4612, GP-4613, GP-4614, GP-4616, GP-4617, GP-4807 | format | plan D03 T17 §11 | extends D03 T04 §2 |
| IP-1836 | PNG export options: pixel format, 16 bit, compression, interlace, transparent pixel colors, background, offset, resolution, time, metadata, saved defaults | PS-B-0985, PS-B-0986, PS-B-0987, PS-B-0988 | -- | GP-4643, GP-4644, GP-4645, GP-4646, GP-4647, GP-4648, GP-4649, GP-4650, GP-4652, GP-4653, GP-4654, GP-4655, GP-4656, GP-4657, GP-4658 | format | plan D03 T17 §11 | extends D03 T04 §2 |
| IP-1837 | TIFF export options: JPEG, PackBits, CCITT compression, pixel order, byte order, pyramid, transparent pixels, CMYK, BigTIFF, metadata, GeoTIFF | PS-B-0966, PS-B-0967, PS-B-0968, PS-B-0969, PS-B-0970 | AF-2614 | GP-4720, GP-4722, GP-4723, GP-4724, GP-4727, GP-4728, GP-4729, GP-4730, GP-4731, GP-4732, GP-4733, GP-4734, GP-4735, GP-4736, GP-4815 | format | plan D03 T17 §11 | extends D03 T04 §3 |
| IP-1838 | TIFF layers: save and crop layers, layer compression, layered TIFF prompt | PS-B-0971, PS-B-0973 | -- | GP-4725, GP-4726 | format | plan D03 T17 §11 | extends D03 T04 §3 |
| IP-1839 | Photoshop data in JPEG and TIFF: clipping paths, guides, layers | -- | -- | GP-0035 | format | plan D03 T17 §11 |  |
| IP-1840 | CMYK JPEG, TIFF, PSD, and JPEG XL import and export with a CMYK profile | -- | -- | GP-0034 | format | plan D03 T17 §11 | Engine D01 T04 §3; PSD CMYK in D03 T17 §2 and §3 |
| IP-1841 | PNG export options for HDR: PQ, HLG, BT.709 transfer, primaries, full range (cICP) | -- | AF-2538, AF-2539, AF-2540 | -- | format | plan D03 T17 §11 | Extends D03 T04 §2; HDR display D03 T15 §4 |
| IP-1842 | TIFF export with layers | -- | AF-2541 | -- | format | plan D03 T17 §11 | Writes Photoshop-style TIFF layers, not Affinity private data |
| IP-1843 | Ask before saving layered TIFF | PS-B-1261 | -- | -- | core | plan D03 T17 §11 |  |
| IP-1844 | Save and save over image formats with flatten prompt | -- | AF-2351, AF-2352 | -- | core | shipped-scope D03 T04 §2 | Native save is D03 T04 §4 |
| IP-1845 | PNG and JPEG basic open and save with ICC, JPEG quality and progressive, recent files | PS-B-0889, PS-B-0974, PS-B-0976, PS-B-0984 | -- | GP-0865, GP-4590, GP-4591, GP-4596, GP-4615, GP-4642, GP-4651, GP-4805 | format | shipped-scope D03 T04 §2 |  |
| IP-1846 | JPEG progressive export option | -- | AF-2537 | -- | format | shipped-scope D03 T04 §2 |  |
| IP-1847 | TIFF 8 and 16 bit open and save, none, LZW, Deflate | PS-B-0965 | -- | GP-4716, GP-4717, GP-4718, GP-4719, GP-4721 | format | shipped-scope D03 T04 §3 |  |
| IP-1848 | Open and Save As of native .imago | PS-B-0895, PS-B-0896 | -- | GP-0870, GP-0871, GP-0873 | core | shipped-scope D03 T04 §4 |  |
| IP-1849 | OpenRaster ORA open and export | -- | -- | GP-4627, GP-4852 | format | shipped-scope D03 T04 §4 | .imago uses the ORA layout |
| IP-1850 | Recovery auto-save | PS-B-0942 | -- | -- | core | shipped-scope D03 T04 §6 |  |
| IP-1851 | Autosave and file recovery interval | PS-B-1249 | AF-2679 | -- | core | shipped-scope D03 T04 §6 |  |
| IP-1852 | Affinity .af, .afphoto, .afdesign, .afpub reading | -- | AF-2593, AF-2594 | -- | format | backlog B-045 |  |
| IP-1853 | Browse in Bridge and close and go to Bridge | PS-B-0890, PS-B-0894 | -- | -- | core | other-app: Lumen browsing and catalog |  |
| IP-1854 | CAD, Freehand, InDesign, Publisher, and office document import | -- | AF-2631, AF-2632, AF-2633, AF-2634, AF-2635 | -- | format | other-app: Nodus vector and page layout imports |  |
| IP-1855 | Capture One .af round trip | -- | AF-2639, AF-2645 | -- | format | other-app: none third-party Capture One integration |  |
| IP-1856 | Open from cloud documents, version history, cloud PSDC | PS-B-0886, PS-B-0938, PS-B-0964 | -- | -- | cloud | excluded: cloud |  |
| IP-1857 | Search Adobe Stock | PS-B-0922 | -- | -- | cloud | excluded: cloud |  |
| IP-1858 | Images from device and iPhone or iPad import | PS-B-0935, PS-B-0936 | -- | -- | core | excluded: platform | macOS only |
| IP-1859 | X11 mouse cursor XMC open and export | -- | -- | GP-4770, GP-4771, GP-4772, GP-4773, GP-4774, GP-4775, GP-4776, GP-4777, GP-4778, GP-4779, GP-4780, GP-4781, GP-4847 | format | excluded: platform | X11 cursor themes, Linux only |
| IP-2383 | Watermark placement: saved watermark image list, anchor positions with pixel offsets, keyed transparency color, blend mode, opacity, as a new layer, presets | -- | -- | -- | core | plan D03 T17 §15 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1469; AC-3544 to AC-3557, AC-4790); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T17 §15 |

## Metadata

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1860 | Image comment | -- | -- | GP-1108 | core | plan D03 T17 §10 |  |
| IP-1861 | Document fields: title and imported PDF metadata | -- | AF-2507 | -- | core | plan D03 T17 §10 |  |
| IP-1862 | EXIF orientation on import with rotation dialog | -- | -- | GP-0113 | core | plan D03 T17 §10 |  |
| IP-1863 | Metadata editor: title, author, description writer, rating, keywords, copyright status, notice, URL | PS-B-0937, PS-B-0946 | -- | GP-1147, GP-1148, GP-1149, GP-1155, GP-1156, GP-1157, GP-1158, GP-1159, GP-1160, GP-1161, GP-1162, GP-1163 | core | plan D03 T17 §10 |  |
| IP-1864 | IPTC Core metadata: contact, dates, genre, scene, location, headline, subject, instructions, credit, source, usage terms | PS-B-0948, PS-B-0949 | -- | GP-1150, GP-1164, GP-1165, GP-1166, GP-1167, GP-1168, GP-1169, GP-1170, GP-1171, GP-1172, GP-1173, GP-1174, GP-1175, GP-1176, GP-1177, GP-1178, GP-1179, GP-1180, GP-1181, GP-1182, GP-1183, GP-1184, GP-1185, GP-1186, GP-1187, GP-1188, GP-1189 | core | plan D03 T17 §10 |  |
| IP-1865 | IPTC Extension metadata: persons, locations, artwork, models, releases, supplier, registry, licensor, digital source type | PS-B-0950 | -- | GP-1151, GP-1190, GP-1191, GP-1192, GP-1193, GP-1194, GP-1195, GP-1196, GP-1197, GP-1198, GP-1199, GP-1200, GP-1201, GP-1202, GP-1203, GP-1204, GP-1205, GP-1206, GP-1207, GP-1208, GP-1209, GP-1210, GP-1211, GP-1212, GP-1213, GP-1214, GP-1215, GP-1216, GP-1217, GP-1218, GP-1219, GP-1220, GP-1221, GP-1222, GP-1223, GP-1224, GP-1225, GP-1226, GP-1227, GP-1228, GP-1229, GP-1230, GP-1231, GP-1232, GP-1233, GP-1234, GP-1235, GP-1236 | core | plan D03 T17 §10 |  |
| IP-1866 | GPS metadata view, edit, and removal | PS-B-0951 | -- | GP-1152, GP-1237, GP-1238, GP-1239, GP-1240, GP-1241, GP-1242 | core | plan D03 T17 §10 |  |
| IP-1867 | DICOM metadata: patient, study, series, equipment | PS-B-0954 | -- | GP-1153, GP-1243, GP-1244, GP-1245, GP-1246, GP-1247, GP-1248, GP-1249, GP-1250, GP-1251, GP-1252, GP-1253, GP-1254, GP-1255, GP-1256 | core | plan D03 T17 §10 |  |
| IP-1868 | Metadata viewer: EXIF camera data, IPTC, XMP, raw XMP | PS-B-0947, PS-B-0955 | -- | GP-1099, GP-1257 | core | plan D03 T17 §10 |  |
| IP-1869 | Audio, video, and Photoshop metadata panels | PS-B-0952, PS-B-0953 | -- | -- | core | plan D03 T17 §10 |  |
| IP-1870 | Metadata templates and import and export | PS-B-0956 | -- | GP-1154 | core | plan D03 T17 §10 |  |
| IP-1871 | Embed or strip metadata on export and refresh metadata automatically | -- | AF-2533 | GP-0084 | core | plan D03 T17 §10 | Dimensions and timestamps updated on export |
| IP-1872 | Editable EXIF in develop | -- | AF-1953 | -- | core | plan D03 T17 §10 |  |
| IP-1873 | Location panel with map and GPS editing | -- | AF-1974 | -- | core | plan D03 T17 §10 | map tiles need an online provider |
| IP-1874 | Metadata panel: view and edit File, EXIF, IPTC, rights | -- | AF-2472, AF-2473 | -- | core | plan D03 T17 §10 |  |
| IP-1875 | Strip GPS location and strip all EXIF | -- | AF-2474, AF-2475 | -- | core | plan D03 T17 §10 |  |
| IP-1876 | XMP sidecar export, import, and automatic load on open | -- | AF-2476, AF-2477, AF-2478 | -- | format | plan D03 T17 §10 |  |
| IP-1877 | Content Credentials panel: producer identity, connected accounts, record edits, default for new documents | PS-B-0656, PS-B-0657, PS-B-0658, PS-B-0661 | -- | -- | ai | backlog B-047 | Unsigned provenance already recorded by D01 T05 §3 and exported as XMP in D03 T19 §13 |
| IP-1878 | Content Credentials on export, automatic for generative content | PS-B-0659, PS-B-0660 | -- | -- | ai | backlog B-047 | Cloud publishing part not planned |
| IP-1879 | Content Credentials recording preference | PS-B-1243 | -- | -- | core | backlog B-047 |  |
| IP-1880 | Map default region when no GPS | -- | AF-1898 | -- | core | excluded: platform | macOS-only setting |

## Export and web

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1881 | Export As dialog: format, transparency, 8-bit PNG, quality, image and canvas size, metadata, sRGB, preview with size | PS-B-0903, PS-B-1056, PS-B-1057, PS-B-1058, PS-B-1059, PS-B-1060, PS-B-1061, PS-B-1063, PS-B-1064, PS-B-1065 | -- | -- | format | plan D03 T18 §1 |  |
| IP-1882 | Export As scale multiples with suffixes | PS-B-1062 | -- | -- | format | plan D03 T18 §1 |  |
| IP-1883 | Quick Export As with format, quality, and location | PS-B-0902, PS-B-0904, PS-B-1069, PS-B-1070 | -- | -- | format | plan D03 T18 §1 |  |
| IP-1884 | Export layers to files, from the Export As list and Layers panel | PS-B-0910, PS-B-1066, PS-B-1068 | -- | -- | automation | plan D03 T18 §8 |  |
| IP-1885 | Export artboards to files and PDF | PS-B-0906, PS-B-0907 | -- | -- | core | plan D03 T18 §8 |  |
| IP-1886 | Export layer comps to files and PDF | PS-B-0908, PS-B-0909 | -- | -- | automation | plan D03 T18 §8 |  |
| IP-1887 | Generate image assets from layer names | PS-B-0918, PS-B-0919, PS-B-0920, PS-B-0921 | -- | -- | core | plan D03 T18 §8 |  |
| IP-1888 | Quick export and export as for layers, export layers to files | PS-A-0647, PS-A-0648, PS-A-0807 | -- | -- | automation | plan D03 T18 §8 |  |
| IP-1889 | Layer comps to files | PS-A-0939 | -- | -- | automation | plan D03 T18 §8 |  |
| IP-1890 | Artboards to files and to PDF | PS-A-0965, PS-A-0966 | -- | -- | automation | plan D03 T18 §8 |  |
| IP-1891 | Export dialog: every format in one list, favorites, live zoomable preview, estimated file size | -- | AF-2508, AF-2509, AF-2510, AF-2511, AF-2512 | -- | core | plan D03 T18 §1 | Extends D03 T04 §2 save paths |
| IP-1892 | Export presets: built-in per format, create, rename, delete | -- | AF-2513, AF-2514 | -- | core | plan D03 T18 §1 |  |
| IP-1893 | Export area: whole document, selection area, selection only | -- | AF-2515 | -- | core | plan D03 T18 §1 |  |
| IP-1894 | Export size with aspect lock and resample (nearest, bilinear, bicubic, Lanczos 3 separable and non-separable) | -- | AF-2517, AF-2518, AF-2519, AF-2520, AF-2521 | -- | core | plan D03 T18 §1 | Resamplers from D01 T03 §2; format size limits warn |
| IP-1895 | Export pixel format, bit depth, and DPI override | -- | AF-2525, AF-2526 | -- | core | plan D03 T18 §1 |  |
| IP-1896 | Export quality, matte color, and palettised PNG and GIF | -- | AF-2527, AF-2528, AF-2532 | -- | core | plan D03 T18 §1 | Palette engine D01 T03 §3 |
| IP-1897 | Export color profile: keep, convert, embed, or unprofiled, with installed system profiles | -- | AF-2529, AF-2530, AF-2228, AF-2229 | -- | format | plan D03 T18 §1 | Engine D01 T04 §1 |
| IP-1898 | Export include bleed | -- | AF-2531 | -- | print | plan D03 T18 §1 | Needs a document bleed setting |
| IP-1899 | Quick export button and panel with draggable preview | -- | AF-2569, AF-2570, AF-2571 | -- | core | plan D03 T18 §1 |  |
| IP-1900 | Layer comps to files | PS-B-0764 | -- | -- | automation | plan D03 T18 §8 |  |
| IP-1901 | Export layers to files with destination, prefix, visible only, trim, and per-format options | PS-B-0765, PS-B-0766, PS-B-0767 | -- | -- | automation | plan D03 T18 §8 |  |
| IP-1902 | Image map editor | -- | -- | GP-0104 | core | plan D03 T18 §2 |  |
| IP-1903 | Save for Web dialog: views, presets, optimize to size, image size, metadata, color conversion, browser preview | PS-B-0905, PS-B-1073, PS-B-1074, PS-B-1081, PS-B-1083, PS-B-1084, PS-B-1085 | -- | -- | format | plan D03 T18 §2 |  |
| IP-1904 | Save for Web GIF and PNG-8: color reduction, lossy, dither, color table editing | PS-B-1075, PS-B-1076, PS-B-1080 | -- | -- | format | plan D03 T18 §2 |  |
| IP-1905 | Save for Web PNG-24, JPEG, and WBMP options | PS-B-1077, PS-B-1078, PS-B-1079 | -- | -- | format | plan D03 T18 §2 |  |
| IP-1906 | Save for Web slices and HTML output settings | PS-B-1086, PS-B-1087, PS-B-1088 | -- | -- | format | plan D03 T18 §2 |  |
| IP-1907 | Zoomify tiled export with HTML template | PS-B-0916, PS-B-0917 | -- | -- | core | plan D03 T18 §2 |  |
| IP-1908 | Export studio: slice workspace for layers, groups, and drawn areas | -- | AF-0010, AF-2573 | -- | core | plan D03 T18 §9 | A workspace preset via D03 T20 §1 |
| IP-1909 | Export visibility per item independent of canvas visibility | -- | AF-2577, AF-2516 | -- | core | plan D03 T18 §9 |  |
| IP-1910 | Slices panel: multiple formats and 1x, 2x, 3x or absolute sizes per slice, DPI scaling | -- | AF-2579, AF-2580, AF-2586 | -- | core | plan D03 T18 §9 |  |
| IP-1911 | Export options panel: per-slice or default settings, presets, copy and paste setups | -- | AF-2578, AF-2584 | -- | core | plan D03 T18 §9 |  |
| IP-1912 | Slice file naming tokens and folder paths | -- | AF-2581, AF-2582 | -- | core | plan D03 T18 §9 |  |
| IP-1913 | Continuous export of changed slices | -- | AF-2583 | -- | core | plan D03 T18 §9 |  |
| IP-1914 | App icon presets and Xcode icon set JSON | -- | AF-2585 | -- | core | plan D03 T18 §9 |  |
| IP-1915 | Web filters menu and Semi-flatten with color | -- | -- | GP-3266, GP-3267, GP-3268 | core | plan D03 T18 §2 | Engine D03 T11 §5 semi-flatten |
| IP-1916 | Image map editor: working area, area list, source view, gray view | -- | -- | GP-3269, GP-3270, GP-3271, GP-3272, GP-3273, GP-3281, GP-3282, GP-3283, GP-3284, GP-3285 | core | plan D03 T18 §2 | Writes HTML image map text, not pixels |
| IP-1917 | Image map areas: rectangle, circle, polygon, edit area info, reorder | -- | -- | GP-3279, GP-3280, GP-3286, GP-3287, GP-3288, GP-3289, GP-3290, GP-3298, GP-3299 | core | plan D03 T18 §2 |  |
| IP-1918 | Image map files: open, recent, save, save as, map info (CSIM, NCSA, CERN) | -- | -- | GP-3274, GP-3275, GP-3276, GP-3277, GP-3278, GP-3291 | core | plan D03 T18 §2 |  |
| IP-1919 | Image map grid and guides: grid settings, use guides, create guide areas | -- | -- | GP-3292, GP-3293, GP-3294, GP-3295, GP-3296, GP-3297 | core | plan D03 T18 §2 | Uses Imago guides from D03 T08 §4 |
| IP-1920 | Slice display, snapping, lock, and clear | PS-A-1696, PS-A-1704, PS-A-1732, PS-A-1742 | -- | -- | format | plan D03 T18 §3 |  |
| IP-1921 | New layer-based slice | PS-A-0666 | -- | -- | format | plan D03 T18 §3 |  |
| IP-1922 | Slice tool with style normal, fixed aspect ratio, fixed size | PS-A-0163, PS-A-0164 | AF-2574 | -- | format | plan D03 T18 §3 | Shift square, Alt from center |
| IP-1923 | Slices from guides | PS-A-0165 | -- | -- | format | plan D03 T18 §3 |  |
| IP-1924 | Slice select tool with stacking order, align, and distribute | PS-A-0166, PS-A-0167, PS-A-0170 | -- | -- | format | plan D03 T18 §3 |  |
| IP-1925 | User and auto slices: promote, hide auto slices | PS-A-0168, PS-A-0171 | -- | -- | format | plan D03 T18 §3 |  |
| IP-1926 | Divide slice horizontally or vertically | PS-A-0169 | -- | -- | format | plan D03 T18 §3 |  |
| IP-1927 | Slice options: name, URL, target, message, alt, dimensions, background | PS-A-0172 | -- | -- | format | plan D03 T18 §3 |  |
| IP-1928 | Layer-based slices from layers and groups, revert to auto size | PS-A-0173 | AF-2576, AF-2575 | -- | format | plan D03 T18 §3 |  |
| IP-1929 | Content Credentials on export | PS-B-1067 | -- | -- | ai | backlog B-047 |  |
| IP-1930 | Share to Mail, Messages, AirDrop | -- | AF-2592 | -- | core | excluded: platform | macOS Share sheet |

## Color management

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1931 | Keep any RGB working space end to end | -- | -- | GP-0010 | core | plan D03 T18 §4 |  |
| IP-1932 | Rendering intent and black point compensation for conversions | -- | AF-2223, AF-2224 | -- | core | plan D03 T18 §4 | Engine D01 T04 §2 |
| IP-1933 | Convert opened and placed images to the working space | -- | AF-2225, AF-2227 | -- | core | plan D03 T18 §4 |  |
| IP-1934 | OpenColorIO configuration and display emulation | -- | AF-2245, AF-2242 | -- | core | plan D03 T18 §10 |  |
| IP-1935 | ACES RRT display filter with exposure stops | -- | -- | GP-1005, GP-1010 | core | plan D03 T18 §10 | Display transform via OCIO |
| IP-1936 | Opened file profile handling and convert to working space | -- | AF-2636 | GP-0806 | format | plan D03 T18 §4 |  |
| IP-1937 | Save color options: embed ICC profile, use proof setup | PS-B-0899 | -- | -- | core | plan D03 T18 §4 |  |
| IP-1938 | Color settings dialog with presets and save and load of settings files | PS-B-1140, PS-B-1141, PS-B-1158 | -- | -- | core | plan D03 T18 §4 | Engine D01 T04 |
| IP-1939 | Color settings shared across suite apps | PS-B-1159 | -- | -- | core | plan D03 T18 §4 | Photon shares one settings file with Nodus and Lumen instead of Creative Cloud sync |
| IP-1940 | Working spaces: RGB, CMYK, gray, spot, and 32-bit RGB and Lab defaults | PS-B-1142, PS-B-1143, PS-B-1144, PS-B-1145 | AF-2222 | -- | core | plan D03 T18 §4 |  |
| IP-1941 | Color management policies and profile mismatch and missing profile warnings | PS-B-1146, PS-B-1147, PS-B-1148 | AF-2226 | -- | core | plan D03 T18 §4 |  |
| IP-1942 | Conversion options: engine, intent, black point compensation, dither, scene-referred compensation | PS-B-1149, PS-B-1150, PS-B-1151, PS-B-1152, PS-B-1153 | -- | -- | core | plan D03 T18 §4 | Engine D01 T04 §2; one CMM, no Adobe ACE |
| IP-1943 | Advanced: desaturate monitor colors, blend RGB and text colors using gamma | PS-B-1154, PS-B-1155, PS-B-1156 | -- | -- | core | plan D03 T18 §4 | Blend gamma consumed by render graph D03 T02 §3 |
| IP-1944 | Custom CMYK: inks, dot gain, GCR and UCR, black generation, ink limits, UCA | PS-B-1157 | -- | -- | core | plan D03 T18 §4 | Builds a CMYK profile via D01 T04 |
| IP-1945 | Assign, discard, or use sRGB profile without converting pixels | PS-B-1160, PS-B-1161 | AF-2221, AF-2219 | GP-1272, GP-1274, GP-1276 | core | plan D03 T18 §4 |  |
| IP-1946 | Convert to profile with engine, intent, BPC, dither, flatten, advanced multichannel | PS-B-1162, PS-B-1163, PS-B-1164 | AF-2220 | GP-1273 | core | plan D03 T18 §4 | Engine D01 T04 §1 and §2 |
| IP-1947 | Document color profile in new document and document setup | -- | AF-2218 | -- | core | plan D03 T18 §4 | New document UI D03 T08 §2 |
| IP-1948 | Embedded profile indicator in status bar and title | PS-B-1165 | -- | -- | core | plan D03 T18 §4 |  |
| IP-1949 | Image color management submenu and save profile to file | -- | -- | GP-1271, GP-1275 | core | plan D03 T18 §4 |  |
| IP-1950 | Display color management per view: color-manage this view, as in preferences | -- | -- | GP-1293, GP-1294, GP-1295, GP-1296 | core | plan D03 T18 §10 | Monitor profile from Windows |
| IP-1951 | OCIO display and view transforms, applied to exports from 32-bit | -- | AF-2241, AF-2246 | -- | format | plan D03 T18 §10 | Needs a user OCIO config; 32-bit preview D03 T15 §4 |
| IP-1952 | OpenColorIO configuration with OCIO 2.5 | -- | AF-2018, AF-2019 | -- | core | plan D03 T18 §10 |  |
| IP-1953 | Color settings preferences: default RGB, 32-bit, CMYK, gray, Lab profiles, intent, BPC, convert and warn on open, file open policy, OCIO by filename | -- | AF-2667, AF-2668, AF-2669, AF-2670, AF-2671, AF-2672 | GP-4148, GP-4149, GP-4150, GP-4151 | core | plan D03 T18 §4 |  |
| IP-1954 | Display color management preferences: image display mode, monitor profile, intent, BPC, optimize for speed or fidelity | -- | -- | GP-4140, GP-4141, GP-4142, GP-4143, GP-4144, GP-4145 | core | plan D03 T18 §10 |  |
| IP-1955 | Soft proof adjustment layer: profile, intent, black point compensation, gamut check | -- | AF-1250, AF-1251, AF-1252, AF-1253, AF-1254, AF-1255, AF-1256 | -- | print | plan D03 T18 §5 |  |
| IP-1956 | Proof setup and proof colors | PS-A-1708, PS-A-1709 | -- | -- | print | plan D03 T18 §5 |  |
| IP-1957 | Gamut warning | PS-A-1710 | -- | -- | print | plan D03 T18 §5 |  |
| IP-1958 | Color deficient vision proofing: protanopia, deuteranopia, tritanopia | -- | -- | GP-1007, GP-1019, GP-1020, GP-1021, GP-1022 | core | plan D03 T18 §5 |  |
| IP-1959 | New image soft-proofing profile, intent, and black point compensation | -- | -- | GP-0853, GP-0854, GP-0855 | core | plan D03 T18 §5 |  |
| IP-1960 | CMYK soft proof then CMYK export (GIMP workflow) | -- | -- | GP-1310 | print | plan D03 T18 §5 | CMYK export writers in D03 T17 §11 |
| IP-1961 | Custom proof condition: device, preserve numbers, intent, BPC, simulate paper and black ink, save and load | PS-B-1127, PS-B-1128, PS-B-1129, PS-B-1130, PS-B-1131, PS-B-1132 | -- | -- | print | plan D03 T18 §5 | Engine D01 T04 §2 |
| IP-1962 | Proof presets: working CMYK, individual plates, RGB conditions | PS-B-1133, PS-B-1134, PS-B-1135 | -- | -- | print | plan D03 T18 §5 |  |
| IP-1963 | Color blindness proof: protanopia and deuteranopia | PS-B-1136 | -- | -- | print | plan D03 T18 §5 |  |
| IP-1964 | Proof colors toggle | PS-B-1137 | -- | GP-1300 | print | plan D03 T18 §5 |  |
| IP-1965 | Gamut warning with color and opacity | PS-B-1138, PS-B-1139 | -- | GP-1297 | print | plan D03 T18 §5 | Gamut check D01 T04 §2 |
| IP-1966 | Soft-proof settings: profile, intent, BPC, status bar pop-over | -- | -- | GP-1290, GP-1291, GP-1292, GP-1298, GP-1299, GP-0012 | print | plan D03 T18 §5 |  |
| IP-1967 | Soft proof adjustment layer (multiple coexisting proofs) | -- | AF-2230 | -- | print | plan D03 T18 §5 | Adjustment layer host D03 T11 §1 |
| IP-1968 | Soft-proof preferences and gamut warning color: optimize soft-proofing, mark out-of-gamut colors, warning color and opacity | PS-B-1281 | -- | GP-4146, GP-4147 | core | plan D03 T18 §5 |  |

## Print

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1969 | Print dialog | PS-B-0939 | -- | GP-0802, GP-4877 | print | plan D03 T18 §6 |  |
| IP-1970 | Print one copy | PS-B-0940 | -- | -- | print | plan D03 T18 §6 |  |
| IP-1971 | Print dialog: printer, driver settings, copies, orientation, description, remember settings | PS-B-1089, PS-B-1090, PS-B-1091, PS-B-1100, PS-B-1124 | AF-2589 | -- | print | plan D03 T18 §6 |  |
| IP-1972 | Print preview with match print colors, gamut warning, paper white | PS-B-1092 | -- | -- | print | plan D03 T18 §6 | Proof engine D03 T18 §5 |
| IP-1973 | Print color handling: printer or Imago manages, separations, printer profile, intent, BPC | PS-B-1093, PS-B-1094, PS-B-1096, PS-B-1097 | -- | -- | print | plan D03 T18 §6 |  |
| IP-1974 | Hard proofing: proof setup, simulate paper color and black ink | PS-B-1095, PS-B-1098 | -- | -- | print | plan D03 T18 §6 |  |
| IP-1975 | Position and size: center, top and left, scale to fit, scale, print resolution, units | PS-B-1101, PS-B-1102, PS-B-1103, PS-B-1104, PS-B-1105, PS-B-1107 | -- | -- | print | plan D03 T18 §6 |  |
| IP-1976 | Print selected area | PS-B-1106 | -- | -- | print | plan D03 T18 §6 |  |
| IP-1977 | Printing marks: corner and center crop, registration, description, labels | PS-B-1108, PS-B-1109, PS-B-1110, PS-B-1111, PS-B-1112, PS-B-1113 | -- | -- | print | plan D03 T18 §6 |  |
| IP-1978 | Print functions: emulsion down, negative, background, border, bleed | PS-B-1114, PS-B-1115, PS-B-1116, PS-B-1117, PS-B-1118 | -- | -- | print | plan D03 T18 §6 |  |
| IP-1979 | PostScript options: calibration bars, interpolation, include vector data | PS-B-1119, PS-B-1120, PS-B-1121 | -- | -- | print | plan D03 T18 §6 | PostScript printers only |
| IP-1980 | Tiled and N-up print layouts | -- | AF-2590 | -- | print | plan D03 T18 §6 |  |
| IP-1981 | Paper size mismatch warning | -- | AF-2591 | -- | print | plan D03 T18 §6 |  |
| IP-1982 | Spot and overprint global colors | -- | AF-2292, AF-2293 | -- | print | plan D03 T18 §7 | Feeds spot channels (D03 T10 §10) and separations |
| IP-1983 | Transfer functions | PS-B-1122 | -- | -- | print | plan D03 T18 §7 |  |
| IP-1984 | Halftone screens per ink | PS-B-1123 | -- | -- | print | plan D03 T18 §7 |  |
| IP-1985 | Print separations with spot channel plates | PS-B-1126 | -- | -- | print | plan D03 T18 §7 | Spot channels D03 T10 §10 |
| IP-1986 | Preflight panel with custom rules | -- | AF-2587, AF-2588 | -- | print | plan D03 T18 §7 | no preflight section; closest is print output extras |
| IP-1987 | PDF Presentation: multi-page PDF or slideshow from images with captions and transitions | PS-B-0712, PS-B-0713, PS-B-0714, PS-B-0715, PS-B-0716 | -- | -- | automation | plan D03 T18 §7 |  |
| IP-1988 | Contact Sheet: thumbnail sheet from a folder with layout, sheet settings, and captions | PS-B-0719, PS-B-0720, PS-B-0721, PS-B-0722, PS-B-0723 | -- | -- | automation | plan D03 T18 §7 |  |
| IP-1989 | Send 16-bit data to the printer | PS-B-1099, PS-B-1125 | -- | -- | print | excluded: platform | macOS-only in Photoshop; Windows print path is 8-bit |

## AI

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-1990 | AI workspace and menu: featured AI tools list, toggles, stacking several AI filters | PS-B-0429, PS-B-0435 | AF-0006, AF-2107 | -- | ai | plan D03 T19 §1 | Canva AI Studio maps to an Imago AI workspace preset and the AI menu |
| IP-1991 | Per-task AI model choice including partner image models | PS-B-0600, PS-B-0601, PS-B-0602, PS-B-0603, PS-B-0604, PS-B-0617 | AF-2127 | -- | ai | plan D03 T19 §1 | Firefly, Gemini, FLUX, Premium and Ultra tiers map to OpenRouter models the user picks per task |
| IP-1992 | AI usage and cost display | PS-B-0605 | AF-2109, AF-2110, AF-2111, AF-2120 | -- | ai | plan D03 T19 §1 | Credits and allowances become OpenRouter token and image cost on the user's own key |
| IP-1993 | AI network requirement and send gate | PS-B-0436 | AF-2113 | -- | ai | plan D03 T19 §1 | Every AI call goes online through D01 T05 §4 send gate with preview; offline shows a clear notice |
| IP-1994 | AI privacy and opt-in: no training on user content, AI can be left off | -- | AF-2114, AF-2115 | -- | ai | plan D03 T19 §1 | Imago AI inactive until a key is set; training policy depends on the chosen OpenRouter provider |
| IP-1995 | AI before and after preview: show original, preview toggle, split and mirror views | PS-B-0432, PS-B-0433 | AF-2154 | -- | ai | plan D03 T19 §1 | Compare from the provenance panel |
| IP-1996 | Generation history for reuse and re-run | -- | AF-2132 | -- | ai | plan D03 T19 §1 | Provenance panel records prompt, model, parameters, seed per result |
| IP-1997 | Generative AI on or off setting | PS-B-0589 | -- | -- | ai | plan D03 T19 §1 |  |
| IP-1998 | AI quick actions and prompt entry in the Properties panel, Contextual Task Bar, and Discover panel | PS-A-1519, PS-A-1532, PS-B-0697, PS-B-1333, PS-B-1379 | -- | -- | ai | plan D03 T19 §1 | entries in the Properties panel now; the Contextual Task Bar hosts them from D03 T20 §1 |
| IP-1999 | AI processing mode preferences for select subject and remove background | PS-B-1270, PS-B-1271 | -- | -- | ai | plan D03 T19 §1 | Imago routes through OpenRouter per task; on-device is B-046 |
| IP-2000 | AI result output: current layer, new layer, masked layer, smart filter, new document | PS-B-0431 | -- | -- | ai | plan D03 T19 §2 | Never overwrites pixels; current-layer output becomes a new layer above, one undo step |
| IP-2001 | Generation resolution handling: output size fitting and upscale to the selection | PS-B-0606 | -- | -- | ai | plan D03 T19 §2 | Model output size caps; large areas tiled with context padding |
| IP-2002 | Generation variations: thumbnails to switch, generate more, pick one as a layer | PS-B-0595 | AF-2130 | -- | ai | plan D03 T19 §2 | Variations kept as a layer group; seed not honored by every model |
| IP-2003 | Generative fill in a selection with optional prompt, masked generative layer | PS-B-0592, PS-B-0593, PS-B-0594, PS-B-0598 | AF-2137 | -- | ai | plan D03 T19 §3 | Image-edit model via OpenRouter; empty prompt fills contextually |
| IP-2004 | Remove tool: brush-over removal with generative mode auto, on, off, remove after each stroke, sample all layers, size | PS-B-0630, PS-B-0631, PS-B-0633, PS-B-0634, PS-B-0635 | -- | -- | ai | plan D03 T19 §3 | Off and classical modes via D03 T13 §2 |
| IP-2005 | Generative fill | PS-A-1237 | -- | -- | ai | plan D03 T19 §3 | Image model via OpenRouter; results as new masked layer |
| IP-2006 | Generative layer with stored prompt and variations | PS-A-0698 | -- | -- | ai | plan D03 T19 §3 | Provenance records prompt, model, seed |
| IP-2007 | Remove tool generative mode: on, off, auto | PS-A-0235 | -- | -- | ai | plan D03 T19 §3 | Image model through OpenRouter; result as new layer; model output size caps |
| IP-2008 | Selection to generative editing from the Contextual Task Bar | PS-A-0543 | -- | -- | ai | plan D03 T19 §3 | selection masks the generative fill request; the Contextual Task Bar entry lands with D03 T20 §1 |
| IP-2009 | Generative layer properties: prompt, variations, generate similar | PS-A-1528 | -- | -- | ai | plan D03 T19 §3 |  |
| IP-2010 | Generative expand of the canvas with optional prompt | PS-B-0607, PS-B-0608 | AF-2138 | -- | ai | plan D03 T19 §4 | Expanded strips tiled when beyond model size |
| IP-2011 | Crop tool fill choice for expanded canvas: background, content-aware, generative expand | PS-B-0609 | -- | -- | ai | plan D03 T19 §4 | Content-aware option classical via D03 T08 §9 and D03 T13 §3 |
| IP-2012 | Generative expand from the crop tool | PS-A-0155 | -- | -- | ai | plan D03 T19 §4 | Model output size caps; large areas tiled |
| IP-2013 | Generative expand in develop crop | PS-B-0522 | -- | -- | ai | plan D03 T19 §4 | model output size caps, large areas tiled |
| IP-2014 | Generate image from a text prompt: content type, effects presets, visual intensity, aspect ratio, count | PS-B-0610, PS-B-0611, PS-B-0614, PS-B-0615, PS-B-0616 | AF-2125, AF-2126, AF-2128, AF-2129 | -- | ai | plan D03 T19 §5 | Raster only; vector output via Nodus hand-off D03 T19 §13; 3D output not offered |
| IP-2015 | Reference images for generation: style reference with strength, composition reference, fill reference | PS-B-0599, PS-B-0612, PS-B-0613 | -- | -- | ai | plan D03 T19 §5 | Reference honored only by models that accept image input |
| IP-2016 | Generate similar variations from a chosen result | PS-B-0596, PS-B-0619 | -- | -- | ai | plan D03 T19 §5 | Reuses stored prompt and reference; seed not honored by every model |
| IP-2017 | Generate background behind a subject | PS-B-0618 | -- | -- | ai | plan D03 T19 §9 | subject masked by D03 T19 §6; background generated on a new layer |
| IP-2018 | Generate background | PS-A-1457 | -- | -- | ai | plan D03 T19 §9 | subject masked by D03 T19 §6; background generated on a new layer |
| IP-2019 | Select subject with local or online processing choice | PS-B-0640, PS-B-0641 | AF-2121 | -- | ai | plan D03 T19 §6 | Vision model locates subject, local engine D03 T10 §6 makes the mask; online step optional |
| IP-2020 | Object selection tool: hover or box to select an object | -- | AF-2134 | -- | ai | plan D03 T19 §6 | Vision model plus D03 T10 §6 segmentation |
| IP-2021 | Select sampled depth: select areas at the depth of a clicked point | -- | AF-2160 | -- | ai | plan D03 T19 §14 | depth estimated, not measured; mask from D03 T10 §6 |
| IP-2022 | Object selection tool with modes, sample all layers, and Select and Mask entry | PS-A-0097, PS-A-0104, PS-A-0107, PS-A-0553 | AF-0480, AF-0481 | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2023 | Object selection rectangle and lasso drawing modes, drag for smaller regions | PS-A-0102, PS-A-0103 | AF-0486 | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2024 | Object subtract | PS-A-0106 | -- | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2025 | Object selection hard or soft edges | PS-A-0105 | AF-0483 | -- | ai | plan D03 T19 §6 | Soft edge matte from D03 T10 §6 |
| IP-2026 | Multi-part objects and component separation | -- | AF-0482, AF-0485 | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2027 | Object finder: hover highlight, refresh, show all objects, overlay settings | PS-A-0098, PS-A-0099, PS-A-0100, PS-A-0101 | -- | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask; detections cached per document |
| IP-2028 | Select subject (menu, options bar, Select and Mask) | PS-A-0108, PS-A-0508, PS-A-0571 | AF-0497 | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2029 | AI selection processing mode: fast local or detailed model | PS-A-0109, PS-A-0593 | -- | -- | ai | plan D03 T19 §6 | Local means engine D03 T10 §6 only; detailed adds the OpenRouter vision model |
| IP-2030 | Select sky | PS-A-0509 | -- | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2031 | Select people and parts (face, skin, hair, eyes, teeth, lips, clothing) | PS-A-0510, PS-A-0511 | -- | -- | ai | plan D03 T19 §6 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask; part accuracy model-limited |
| IP-2032 | Hair refinement and object-aware refine mode | PS-A-0512, PS-A-0570, PS-A-0572 | -- | -- | ai | plan D03 T19 §6 | Vision model seeds D03 T10 §6 matting, which produces hair detail |
| IP-2033 | Select sampled depth tool and command | -- | AF-0488, AF-0489 | -- | ai | plan D03 T19 §14 | depth estimated, not measured; mask from D03 T10 §6 |
| IP-2034 | Detected objects and regions: detections panel, select or mask any detection | -- | AF-2135, AF-2136, AF-2180 | -- | ai | plan D03 T19 §15 | Mask all objects; detection by vision model, masks by D03 T10 §6 |
| IP-2035 | Decompose layer into subject, background, and foreground layers with occluded parts filled | -- | AF-2155, AF-2156, AF-2179 | -- | ai | plan D03 T19 §15 | Segments via D03 T10 §6 then fills occlusions via D03 T19 §3; fill is invented content |
| IP-2036 | Mask tool subject seeding: sky and person detection | -- | AF-0348, AF-0349 | -- | ai | plan D03 T19 §15 | Vision model locates, D03 T10 §6 builds the mask |
| IP-2037 | Mask all objects | PS-A-0662 | -- | -- | ai | plan D03 T19 §15 | Vision model finds objects, D03 T10 §6 builds one mask each |
| IP-2038 | AI subject, sky, and background masks in develop | PS-B-0540, PS-B-0541, PS-B-0542 | -- | -- | ai | plan D03 T19 §15 | surface D03 T15 §2 |
| IP-2039 | AI object mask by brush or rectangle | PS-B-0543 | -- | -- | ai | plan D03 T19 §15 | surface D03 T15 §2 |
| IP-2040 | AI people parts and landscape region masks | PS-B-0544, PS-B-0545 | -- | -- | ai | plan D03 T19 §15 | surface D03 T15 §2 |
| IP-2041 | Update AI masks after changes | PS-B-0562 | -- | -- | core | plan D03 T19 §15 | surface D03 T15 §2 |
| IP-2042 | Detections panel listing objects and regions to select or mask | -- | AF-0490, AF-0491 | -- | ai | plan D03 T19 §15 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2043 | Mask all objects into masked groups | PS-A-0110 | -- | -- | ai | plan D03 T19 §15 | Vision model locates, local segmentation engine D03 T10 §6 produces the mask |
| IP-2044 | Skin smoothing with blur and smoothness | PS-B-0437, PS-B-0438 | -- | -- | ai | plan D03 T19 §7 | Face regions from D03 T19 §11 landmarks, smoothing classical on a masked layer |
| IP-2045 | Smart portrait: expression, age, hair, gaze, head and light direction, detail retention | PS-B-0439, PS-B-0440, PS-B-0441, PS-B-0442 | -- | -- | ai | plan D03 T19 §7 | Image-edit model; sliders become graded prompts, identity drift possible |
| IP-2046 | Makeup transfer from a reference image | PS-B-0443 | -- | -- | ai | plan D03 T19 §7 | Needs a model accepting two images |
| IP-2047 | Colorize black and white photos with focal-point hints and tuning | PS-B-0448, PS-B-0449 | AF-1717, AF-2144, AF-2145 | -- | ai | plan D03 T19 §7 | Result as color layer in Color blend mode over the original; colors are guesses |
| IP-2048 | Style transfer from presets or a custom image with strength, preserve color, focus subject | PS-B-0450, PS-B-0451 | -- | -- | ai | plan D03 T19 §7 |  |
| IP-2049 | Photo restoration: enhance, face, scratches, noise, halftone, JPEG artifacts | PS-B-0452, PS-B-0453 | -- | -- | ai | plan D03 T19 §7 | Classical scratch and halftone passes from D01 T03 §6 where they suffice |
| IP-2050 | Harmonization neural filter: match a layer to a reference layer with strength and color sliders | PS-B-0454, PS-B-0455 | -- | -- | ai | plan D03 T19 §7 | Mostly statistical, runs without a model; model optional |
| IP-2051 | Harmonize a composited layer: generative relight and shadows with variations | PS-B-0620, PS-B-0621 | -- | -- | ai | plan D03 T19 §7 | Generated shadow and light on new layers |
| IP-2052 | Landscape mixer: time of day, season, strength, preserve and harmonize subject | PS-B-0456, PS-B-0457 | -- | -- | ai | plan D03 T19 §7 |  |
| IP-2053 | Rotate object | PS-A-1244 | -- | -- | ai | plan D03 T19 §7 | Novel view generated by image model, not true 3D |
| IP-2054 | Neural filters workspace | PS-B-0008 | -- | -- | ai | plan D03 T19 §7 | Imago neural-filter equivalents through OpenRouter; results as new layers |
| IP-2055 | Colorize black and white photos | -- | AF-1715, AF-1716 | -- | ai | plan D03 T19 §7 | Image model result as a new layer; model output size caps |
| IP-2056 | Harmonize composited subject | PS-A-1455 | -- | -- | ai | plan D03 T19 §7 | Adjustment layers plus generated shadow layer; honest limits on lighting match |
| IP-2057 | Rotate object with on-canvas controls | PS-A-1341 | -- | -- | ai | plan D03 T19 §7 | Generated re-render of the object at a new angle; model-limited fidelity |
| IP-2058 | Portrait lighting: add or adjust virtual lights on a portrait | -- | AF-1826, AF-2142 | -- | ai | plan D03 T19 §14 | Generative relight on a new layer, not physically based |
| IP-2059 | Depth blur and portrait blur: focal point, distance, range, blur, haze, grain, depth map output | PS-B-0458, PS-B-0459 | AF-1507, AF-2140, AF-2141 | -- | ai | plan D03 T19 §14 | Depth estimated, not measured; blur by D01 T06 §3 lens blur |
| IP-2060 | Detect depth: create a depth map layer | -- | AF-2123, AF-2124 | -- | ai | plan D03 T19 §14 | Depth map from an image model; estimated, not measured |
| IP-2061 | Portrait blur (AI depth background blur) | -- | AF-1505, AF-1506 | -- | ai | plan D03 T19 §14 | Depth estimated, not measured; blur via D01 T06 §3 lens blur |
| IP-2062 | Depth and normals maps estimated from a photo | -- | AF-1707, AF-1708 | -- | ai | plan D03 T19 §14 | Depth and normals estimated by a model, not measured; output as a new layer |
| IP-2063 | Mixed light correction | -- | AF-1742, AF-1743 | -- | ai | plan D03 T19 §14 | Vision or image model via OpenRouter; result as new layer; model-dependent quality |
| IP-2064 | Portrait lighting (relight a face with point or spot light) | -- | AF-1824, AF-1825 | -- | ai | plan D03 T19 §14 | Image-edit model via OpenRouter as a new layer; depth estimated, not measured |
| IP-2065 | Lens blur by estimated depth with bokeh shapes and focal range | PS-B-0511 | -- | -- | ai | plan D03 T19 §14 | depth estimated, not measured, kernel D01 T06 §3 |
| IP-2066 | Generative upscale 2x and 4x with faithful or creative model and scale document to fit | PS-B-0622, PS-B-0623, PS-B-0624 | AF-2150, AF-2151, AF-2152, AF-2153 | -- | ai | plan D03 T19 §8 | Topaz and Firefly map to OpenRouter models; tiled for large output |
| IP-2067 | Super zoom: crop and enlarge with detail, artifact, noise, sharpen, face options | PS-B-0444, PS-B-0445 | -- | -- | ai | plan D03 T19 §8 |  |
| IP-2068 | Super resolve layer and generated result | -- | AF-1534, AF-1535, AF-2131, AF-2146, AF-2147 | -- | ai | plan D03 T19 §8 | OpenRouter upscale; on-device variant is B-046 |
| IP-2069 | Super resolve document with scale percentage | -- | AF-1536, AF-1537, AF-2148, AF-2149 | -- | ai | plan D03 T19 §8 | Text and vector layers resized natively, pixel layers upscaled |
| IP-2070 | AI noise reduction with luma and chroma strength, live filter and brush forms | -- | AF-1689, AF-1690, AF-1691, AF-1692, AF-1693, AF-2161, AF-2162 | -- | ai | plan D03 T19 §8 | Image models may alter detail; classical D01 T06 §5 fallback; on-device model is B-046 |
| IP-2071 | GIMP third-party AI plug-in equivalents: generation, inpainting, super resolution, segmentation, denoise, colorize, background removal | -- | -- | GP-4889, GP-4890, GP-4891 | ai | plan D03 T19 §8 | GIMP ships none; Imago covers the jobs in D03 T19 §3, §5, §6, §7, §9 |
| IP-2072 | Generative upscale and Preserve Details 2.0 | PS-A-1175, PS-A-1185 | -- | -- | ai | plan D03 T19 §8 | Model output size caps; large images tiled |
| IP-2073 | Super Zoom enlargement with detail enhance and JPEG artifact removal | PS-A-1184 | -- | -- | ai | plan D03 T19 §8 |  |
| IP-2074 | Motion blur reduction (AI deblur) | -- | AF-1502, AF-1503 | -- | ai | plan D03 T19 §8 | Image-edit model via OpenRouter, result as a new layer; classical shake reduction in D01 T06 §4 |
| IP-2075 | SDR to HDR expansion | -- | AF-1751, AF-1752 | -- | ai | plan D03 T19 §8 | Model-predicted highlight expansion into a 32-bit layer; estimated, not recovered |
| IP-2076 | AI denoise in develop | PS-B-0502 | -- | -- | ai | plan D03 T19 §8 | result as a new layer |
| IP-2077 | AI raw detail enhancement | PS-B-0503 | -- | -- | ai | plan D03 T19 §8 | classical demosaic stays in D03 T07 §11 |
| IP-2078 | Super resolution 2x in develop | PS-B-0504 | -- | -- | ai | plan D03 T19 §8 | model output size caps, large images tiled |
| IP-2079 | Mixed light correction and motion blur reduction in RAW | -- | AF-1979 | -- | ai | plan D03 T19 §8 |  |
| IP-2080 | Find distractions: people, wires and cables | PS-B-0636, PS-B-0637, PS-B-0638 | -- | -- | ai | plan D03 T19 §9 | Vision model finds, removal via D03 T19 §3 |
| IP-2081 | Remove background to a layer mask | PS-B-0639 | AF-2119 | -- | ai | plan D03 T19 §9 | Mask, not pixel deletion; Affinity in-place rasterizing not copied |
| IP-2082 | Reflection removal | PS-A-1245 | -- | -- | ai | plan D03 T19 §9 | Reflection returned as a separate layer |
| IP-2083 | Generative remove in develop with variations | PS-B-0525, PS-B-0536 | -- | -- | ai | plan D03 T19 §9 | seed not honored by every model |
| IP-2084 | Detect objects for removal | PS-B-0529 | -- | -- | ai | plan D03 T19 §9 |  |
| IP-2085 | Distraction removal: people and dust | PS-B-0532, PS-B-0534 | -- | -- | ai | plan D03 T19 §9 |  |
| IP-2086 | Reflection removal | PS-B-0533 | -- | -- | ai | plan D03 T19 §9 |  |
| IP-2087 | Blemish removal by type and prominence | PS-B-0535 | -- | -- | ai | plan D03 T19 §9 |  |
| IP-2088 | Find distractions: people, wires and cables, general, with review | PS-A-0237, PS-A-0238, PS-A-0239, PS-A-0240, PS-A-0241 | -- | -- | ai | plan D03 T19 §9 | Vision model locates, D03 T10 §6 masks, D03 T13 §3 or D03 T19 §3 fills |
| IP-2089 | Remove background | PS-A-1456 | -- | -- | ai | plan D03 T19 §9 | Result is a layer mask, not deleted pixels |
| IP-2090 | Prompt to edit and generative edit: natural-language edits respecting the selection | PS-B-0625 | AF-2139 | -- | ai | plan D03 T19 §10 | Structured undoable commands first, image-edit model on a new layer otherwise |
| IP-2091 | Markup guidance: arrows, circles, colors, doodles to steer an edit | PS-B-0626 | -- | -- | ai | plan D03 T19 §10 | Markup sent as an annotated image; needs a vision-capable model |
| IP-2092 | Conversational AI assistant for multi-step edits | PS-B-0627, PS-B-0628 | -- | -- | ai | plan D03 T19 §10 | Every step an undoable command with provenance |
| IP-2093 | AI adjustment presets and auto adjust | PS-B-0650, PS-B-0651 | -- | -- | ai | plan D03 T19 §10 | Adaptive presets as adjustment layers; classical auto tone D01 T07 §1 stays |
| IP-2094 | Ask panel: in-app AI help answering feature questions | -- | AF-2170 | -- | ai | plan D03 T19 §10 | Assistant explains Imago features from bundled help |
| IP-2095 | Prompt to edit | PS-A-1238 | -- | -- | ai | plan D03 T19 §10 | Structured undoable commands |
| IP-2096 | Adaptive profile | PS-B-0467 | -- | -- | ai | plan D03 T19 §10 | vision model suggests settings recorded as develop parameters |
| IP-2097 | Adaptive and recommended presets | PS-B-0564, PS-B-0566 | -- | -- | ai | plan D03 T19 §10 |  |
| IP-2098 | Match Font: recognize a font in an image region and suggest installed fonts | PS-A-1606, PS-A-1607, PS-A-1621 | -- | -- | ai | plan D03 T19 §11 | Vision model via OpenRouter; suggests installed fonts only, no Adobe Fonts sync |
| IP-2099 | Sky replacement with preset and custom skies, brightness, temperature, scale, flip, output layers | PS-B-0642, PS-B-0643, PS-B-0645, PS-B-0648 | -- | -- | ai | plan D03 T19 §12 | User-supplied skies; Adobe preset skies not shipped |
| IP-2100 | Sky replacement edge and foreground lighting: shift and fade edge, lighting mode, edge lighting, color adjustment | PS-B-0644, PS-B-0646, PS-B-0647 | -- | -- | ai | plan D03 T19 §12 |  |
| IP-2101 | Sky brush and sky move tools | PS-B-0649 | -- | -- | ai | plan D03 T19 §12 |  |
| IP-2102 | Sky replacement | PS-A-1246 | -- | -- | ai | plan D03 T19 §12 |  |
| IP-2103 | Brand Kits panel: colors, fonts, logos | -- | AF-2505 | -- | cloud | plan D03 T19 §13 | suite brand kit from D01 T05 §5, no Canva sync |
| IP-2104 | On-device ML model downloads, manager, and system requirements | PS-B-0430 | AF-1504, AF-2112, AF-2117, AF-2118 | -- | ai | backlog B-046 |  |
| IP-2105 | Remove tool on-device model | PS-B-0632 | -- | -- | ai | backlog B-046 | OpenRouter path in D03 T19 §3 meanwhile |
| IP-2106 | Motion blur reduction tool and filter | -- | AF-2163, AF-2164 | -- | ai | backlog B-046 | Classical shake reduction D01 T06 §4 covers the job meanwhile |
| IP-2107 | Mixed light correction tool and filter | -- | AF-1744, AF-2165, AF-2166 | -- | ai | backlog B-046 | No reliable OpenRouter equivalent |
| IP-2108 | SDR to HDR expansion tool and filter | -- | AF-1753, AF-2167, AF-2168 | -- | ai | backlog B-046 | Needs float output no hosted model returns |
| IP-2109 | Normals from image (ML normal map) | -- | AF-2143 | -- | ai | backlog B-046 | Classical height-based normal map in D01 T06 §13 |
| IP-2110 | Remove tool on-device model | PS-A-0236 | -- | -- | ai | backlog B-046 | Local model download; cloud path is D03 T19 §3 |
| IP-2111 | Segmentation model download for object selection | -- | AF-0487 | -- | ai | backlog B-046 | Imago default is OpenRouter vision plus the local classical engine |
| IP-2112 | On-device ML settings: inference device, segmentation and saliency models, model download and uninstall | -- | AF-2664, AF-2665, AF-2666, AF-2734 | -- | ai | backlog B-046 |  |
| IP-2113 | Content credentials on develop edits and exports | PS-B-0591 | -- | -- | ai | backlog B-047 | provenance still recorded via D01 T05 §3 |
| IP-2369 | One-click masked background adjustments from an AI subject mask: black and white background (blur background is IP-2061) | -- | -- | -- | core | plan D03 T19 §15 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1284; AC-2825); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T19 §15 |
| IP-2372 | Face edit framework: detect faces with landmark points, face selector, correctable points, symmetric left and right link, grouped sliders, presets | -- | -- | -- | core | plan D03 T19 §11 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1372; AC-3141, AC-3142, AC-3158, AC-3194 to AC-3196, AC-3198); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T19 §11 |
| IP-2373 | Face color retouching over face landmarks: eye sharpen, whitening, eye and iris color, sclera, eyebrow color, nose contouring, teeth whitening, lip color, blush, eyeshadow | -- | -- | -- | core | plan D03 T19 §11 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1375; AC-3155 to AC-3157, AC-3163, AC-3168, AC-3170, AC-3188 to AC-3193); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T19 §11 |
| IP-2374 | Hair recolor with an automatic hair mask: color wheel limited to natural colors, temperature, tint, saturation, shadows, midtones, highlights, sharpness, hair mask editing | -- | -- | -- | core | plan D03 T19 §11 | Added 2026-09-27 for ACDSee Photo Studio Ultimate 2027 Edit mode, which the Lumen catalog routes here (LP-1376; AC-3173 to AC-3181, AC-3197); no Photoshop, Affinity, or GIMP row; planned as a checklist item in D03 T19 §11 |

## Workspace and UI

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2114 | Compositing and Color Grading studios | -- | AF-1379, AF-1380 | -- | core | plan D03 T20 §1 | Studios as workspace presets |
| IP-2115 | Compositing studio workspace preset | -- | AF-0013 | -- | core | plan D03 T20 §1 |  |
| IP-2116 | Import and export studio configurations | -- | AF-0022 | -- | core | plan D03 T20 §1 |  |
| IP-2117 | Color grading studio preset | -- | AF-0012 | -- | core | plan D03 T20 §1 | Affinity studios as workspace presets |
| IP-2118 | Selection Contextual Task Bar actions | PS-A-0544 | -- | -- | core | plan D03 T20 §1 |  |
| IP-2119 | Typography studio | -- | AF-0016 | -- | core | plan D03 T20 §1 | Affinity studio as a workspace preset over the D03 T16 type panels |
| IP-2120 | Contextual Task Bar framework: on-canvas next-step bar with per-context selection, layer, and type actions, pin, reset, hide | PS-A-0023, PS-A-0024, PS-A-1529, PS-A-1530, PS-A-1531, PS-A-1533, PS-B-1330, PS-B-1331, PS-B-1332, PS-B-1334 | -- | -- | core | plan D03 T20 §1 | AI actions call D03 T19 sections |
| IP-2121 | Properties panel framework with document, pixel layer, and type pages, quick actions, transform, and align | PS-A-1514, PS-A-1515, PS-A-1516, PS-A-1517, PS-A-1518, PS-A-1520, PS-A-1521, PS-B-1357 | -- | -- | core | plan D03 T20 §1 |  |
| IP-2122 | Numeric field behaviors: scrubby labels, math expressions with variables and functions, unit suffix conversion, wheel increments with modifiers | PS-A-0030, PS-A-0031, PS-A-0032 | AF-0037, AF-0038, AF-0039 | GP-0240 | core | plan D03 T20 §1 | shared control behavior across every panel, closest is the panels framework |
| IP-2123 | Workspace presets (Essentials, Graphic and Web, Painting, Photography) and lock workspace | PS-B-1322, PS-B-1327 | -- | -- | core | plan D03 T20 §1 | extends D03 T07 §17 |
| IP-2124 | Workspaces that also store shortcuts, menus, and toolbar | PS-B-1180, PS-B-1324 | -- | -- | core | plan D03 T20 §1 | extends D03 T07 §17 |
| IP-2125 | Studios as workspaces: Pixel studio, switch with function keys, enable, rename, reorder, clone, custom name, icon, and color | -- | AF-0002, AF-0003, AF-0018, AF-0019, AF-0020, AF-0021, AF-2746 | -- | core | plan D03 T20 §1 | Affinity studios mapped to Imago workspace presets |
| IP-2126 | Panel docking, stacking, tab groups, iconic collapse, panel menus, show or hide left and right studio | PS-B-1367, PS-B-1368 | AF-0040 | -- | core | plan D03 T20 §1 |  |
| IP-2127 | Hide all panels with Tab, Shift+Tab keeps the toolbar, hide docks | PS-B-1372 | AF-0041 | GP-4322 | core | plan D03 T20 §1 |  |
| IP-2128 | Workspace preferences: auto-collapse iconic panels, auto-show hidden panels, open documents as tabs or floating, floating window docking, large tabs | PS-B-1219, PS-B-1220, PS-B-1221, PS-B-1222, PS-B-1223 | AF-2648, AF-2649 | -- | core | plan D03 T20 §1 |  |
| IP-2129 | Document tabs: drag out, float, dock back, merge all, tab context menu, show tabs, tab bar position | PS-B-1369 | AF-0044, AF-0058 | GP-4323, GP-4324 | core | plan D03 T20 §1 | extends D03 T03 §1 |
| IP-2130 | Single-window and multi-window modes and windowed or full-screen app frame | -- | AF-0045 | GP-4298, GP-4299, GP-4300, GP-4314, GP-4325 | core | plan D03 T20 §1 |  |
| IP-2131 | Dockable dialogs: organize, tab menu, context menu, add, close, detach, lock tab, move to screen, Windows menu dock lists, recently closed docks | -- | -- | GP-3609, GP-3610, GP-3611, GP-3612, GP-3613, GP-3614, GP-3615, GP-3616, GP-3629, GP-4316, GP-4317, GP-4318, GP-4321 | core | plan D03 T20 §1 |  |
| IP-2132 | Dockable dialog display: tab style, preview size, list or grid view, button bar, image selection, auto follow active image | -- | -- | GP-3617, GP-3618, GP-3619, GP-3620, GP-3621, GP-3622, GP-3623, GP-3624, GP-3625, GP-3626, GP-3627, GP-3628 | core | plan D03 T20 §1 |  |
| IP-2133 | Window management preferences: dock window hints, focus activates image, save and restore window positions, same monitor, reset | -- | -- | GP-4290, GP-4291, GP-4292, GP-4293, GP-4294, GP-4295, GP-4296 | core | plan D03 T20 §1 |  |
| IP-2134 | Customize toolbar | PS-A-1253 | -- | -- | core | plan D03 T20 §2 |  |
| IP-2135 | Toolbox tool grouping toggle | -- | -- | GP-0015 | core | plan D03 T20 §2 |  |
| IP-2136 | Toolbox brush, pattern, and gradient area | -- | -- | GP-0230 | core | plan D03 T20 §2 |  |
| IP-2137 | Floating context toolbar | -- | AF-0438 | -- | core | plan D03 T20 §2 |  |
| IP-2138 | Toolbar with flyout tool groups, single or double column, Extra Tools slot, and Edit Toolbar customization (reorder, group, presets, restore, clear, show or hide controls) | PS-A-0001, PS-A-0002, PS-A-0004, PS-A-0005, PS-A-0006, PS-A-0007, PS-A-0008, PS-A-0009, PS-A-0010, PS-A-0011, PS-B-1181, PS-B-1182, PS-B-1183, PS-B-1184, PS-B-1185, PS-B-1186, PS-B-1187, PS-B-1363 | -- | GP-0227, GP-0228, GP-3695, GP-4289, GP-4319 | core | plan D03 T20 §2 | GIMP toolbox and tool groups included |
| IP-2139 | Per-workspace tool customization: add, remove, reorder tools and flyouts, column count, reset | -- | AF-0023, AF-0024, AF-0437, AF-2503 | -- | core | plan D03 T20 §2 | Affinity Customize Tools |
| IP-2140 | Tools menu listing every tool | -- | -- | GP-0226 | core | plan D03 T20 §2 |  |
| IP-2141 | Tool switching: spring-loaded shortcuts, Shift or repeat-key cycling through a group, swap to previous tool | PS-A-0003, PS-A-0021, PS-B-1229 | AF-0439, AF-2703, AF-2704 | GP-0072 | core | plan D03 T20 §2 | extends D03 T03 §4 |
| IP-2142 | Toolbox indicator areas: foreground and background, active brush, pattern, gradient, active image, drop target | -- | -- | GP-0231, GP-4284, GP-4285, GP-4286, GP-4287, GP-4288 | core | plan D03 T20 §2 |  |
| IP-2143 | Options bar and context toolbar: floating or pinned, hide advanced options, narrow mode, reset tool and reset all tools | PS-A-0020, PS-A-0022, PS-B-1224, PS-B-1362 | AF-0033, AF-0034, AF-0035 | GP-0238 | core | plan D03 T20 §2 |  |
| IP-2144 | Top toolbar customization: drag items on or off, icon only or icon and text, show toolbar | -- | AF-0025, AF-0026 | -- | core | plan D03 T20 §2 |  |
| IP-2145 | Modifier plus scroll wheel on canvas adjusts tool size, opacity, and zoom | -- | -- | GP-0241 | core | plan D03 T20 §2 |  |
| IP-2146 | Command search | PS-A-1231 | -- | -- | core | plan D03 T20 §3 | Stock results excluded as cloud |
| IP-2147 | Keyboard Shortcuts and Menus dialog: shortcuts for menus, panel menus, tools, filters, blend modes, and task workspaces, per-workspace or shared, single-key shortcuts | PS-B-1166, PS-B-1167, PS-B-1168, PS-B-1169, PS-B-1170, PS-B-1171, PS-B-1326 | AF-2738, AF-2739, AF-2740, AF-2741 | GP-0887, GP-0909, GP-4239, GP-4240, GP-4301 | core | plan D03 T20 §3 | extends D03 T07 §17 |
| IP-2148 | Shortcut set files: save, load, save on exit, reset to defaults, alternate default sets, remove all | -- | AF-2743, AF-2744 | GP-4241, GP-4242, GP-4243, GP-4244 | core | plan D03 T20 §3 |  |
| IP-2149 | Shortcuts summary exported to HTML | PS-B-1173 | -- | -- | core | plan D03 T20 §3 |  |
| IP-2150 | Default keymap conventions: resize document and canvas, fill and inpaint, and one menu and shortcut set across the suite | -- | AF-0050, AF-2747 | -- | core | plan D03 T20 §3 |  |
| IP-2151 | Legacy undo and channel shortcut options | PS-B-1175, PS-B-1176 | -- | -- | core | plan D03 T20 §3 |  |
| IP-2152 | Menu customization: hide items, color items, named menu sets, show menu colors | PS-B-1177, PS-B-1178, PS-B-1179, PS-B-1218 | -- | -- | core | plan D03 T20 §3 |  |
| IP-2153 | Command search: search and run any command or filter, with menu path and help button, Feature Finder | PS-B-1373 | AF-0036 | GP-0007, GP-0029, GP-4310 | core | plan D03 T20 §3 |  |
| IP-2154 | Edit, View, and Image menu structure | -- | -- | GP-0888, GP-1038, GP-1094 | core | shipped-scope D03 T06 §2 | Entries owned by their feature rows |
| IP-2155 | Per-command shortcut editing with add, delete, use default, and conflict warning | PS-B-1172, PS-B-1174 | AF-2742, AF-2745 | -- | core | shipped-scope D03 T07 §17 |  |
| IP-2156 | Save, reset, delete workspaces and studio presets | PS-B-1323, PS-B-1325 | AF-0042, AF-0043 | -- | core | shipped-scope D03 T07 §17 |  |
| IP-2157 | Move to another screen | -- | -- | GP-1024, GP-1025, GP-1026 | core | excluded: platform | X11 display selection; Windows moves windows between monitors natively |
| IP-2158 | Distribution through Store, AppImage, Flatpak, Snap | -- | -- | GP-0048 | core | excluded: platform | Linux packages; Imago ships with the suite Windows installer |
| IP-2159 | macOS application frame | PS-B-1364 | -- | -- | core | excluded: platform | macOS only |
| IP-2160 | Pointer and Touch Bar support | -- | AF-2700 | -- | core | excluded: platform | Touch Bar is macOS hardware |
| IP-2161 | Native Wayland support and tablet pad mapping on Wayland | -- | -- | GP-0003, GP-0032 | core | excluded: platform | Linux only |
| IP-2162 | 32-bit Windows builds | -- | -- | GP-0094 | core | excluded: platform | Imago ships 64-bit only |

## Preferences

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2163 | Numeric field math expressions | -- | AF-2337 | -- | core | plan D03 T20 §4 | shared numeric input behavior across all dialogs |
| IP-2164 | Limit initial zoom to 100 percent | -- | AF-2400 | -- | core | plan D03 T20 §4 |  |
| IP-2165 | Precise cursor and brush outline preview | PS-A-1749 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2166 | Guides, grid, and smart guide color and style preferences | PS-A-1693, PS-A-1694, PS-A-1695 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2167 | Path display color and thickness | PS-A-1697 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2168 | On-canvas widget size | PS-A-1698 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2169 | Transparency grid settings | PS-A-0804 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2170 | Artboard canvas color and outline display | PS-A-0968 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2171 | Brush cursor preferences: outline preview and center crosshair | -- | AF-0674, AF-0675 | -- | core | plan D03 T20 §4 |  |
| IP-2172 | Preferences search and category filter | -- | AF-2732 | -- | core | plan D03 T20 §4 | extends D03 T07 §17 |
| IP-2173 | General preferences: auto-update open documents, beep when done, export clipboard, legacy free transform, reopen documents on startup, hide file extension | PS-B-1201, PS-B-1202, PS-B-1203, PS-B-1204 | AF-2646, AF-2650 | -- | core | plan D03 T20 §4 |  |
| IP-2174 | Usage data and crash report opt-in | PS-B-1207 | AF-2660, AF-2731 | -- | core | plan D03 T20 §4 | Imago sends nothing by default |
| IP-2175 | Reset, back up, and migrate preferences: reset on quit, reset at launch, reset defaults, reset app | PS-B-1206, PS-B-1311, PS-B-1312, PS-B-1313 | AF-2730, AF-2736 | -- | core | plan D03 T20 §4 |  |
| IP-2176 | Notifications preference | PS-B-1225 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2177 | Tool tips: show tool tips, rich tooltips, tooltip delay, maximum width | PS-A-0029, PS-B-1226, PS-B-1227 | AF-2691 | GP-0100 | core | plan D03 T20 §4 |  |
| IP-2178 | Cursor preferences: painting cursors, other cursors, crosshair in brush tip, crosshair only while painting, brush preview color, brush outline and snapping, pointer handedness, Caps Lock precise | PS-A-0025, PS-A-0026, PS-A-0027, PS-A-0028, PS-B-1274, PS-B-1275, PS-B-1276, PS-B-1277, PS-B-1278 | AF-2695, AF-2696 | GP-4218, GP-4219, GP-4220, GP-4221, GP-4222 | core | plan D03 T20 §4 |  |
| IP-2179 | Tools preferences: handle size, marquee intersect selects, move aspect constraint, nudge distance, sync tools between documents, edit non-visible layers, save and reset tool options | -- | AF-2701, AF-2702, AF-2710, AF-2712, AF-2713 | GP-4272, GP-4273, GP-4274, GP-4275, GP-4276 | core | plan D03 T20 §4 |  |
| IP-2180 | Share brush, dynamics, pattern, gradient, and expand layers settings between tools | -- | AF-2721 | GP-4278, GP-4279, GP-4280, GP-4281, GP-4282 | core | plan D03 T20 §4 |  |
| IP-2181 | Assistant: automatic actions for painting with no layer, erasing or brushing vector layers, filters on vector layers, adjustment, mask, filter to selection, one undo step, alerts | -- | AF-0032, AF-2715, AF-2716, AF-2717, AF-2718, AF-2719, AF-2720, AF-2722, AF-2723, AF-2724, AF-2725 | -- | core | plan D03 T20 §4 | an automatic-behavior policy, closest is tools preferences |
| IP-2182 | Transparency grid: check size, colors, style | PS-B-1279, PS-B-1280 | -- | GP-4160, GP-4161, GP-4162 | core | plan D03 T20 §4 |  |
| IP-2183 | Units and rulers: ruler and type units, column size, new document resolutions, point size, decimal places, lines and text in points | PS-B-1282, PS-B-1283, PS-B-1284, PS-B-1285, PS-B-1286 | AF-2692, AF-2694 | -- | core | plan D03 T20 §4 |  |
| IP-2184 | Guides, grid, slices, and path colors and styles | PS-B-1287, PS-B-1288, PS-B-1289, PS-B-1290, PS-B-1291, PS-B-1292 | -- | -- | core | plan D03 T20 §4 |  |
| IP-2185 | Type preferences: smart quotes, missing glyph protection, English font names, Esc commits, placeholder text, text engine, font preview size and recent fonts, font menu background | PS-B-1298, PS-B-1299, PS-B-1300, PS-B-1301, PS-B-1302, PS-B-1303, PS-B-1304 | AF-2698 | -- | core | plan D03 T20 §4 |  |
| IP-2186 | Theme follows system color scheme and accent color | -- | -- | GP-0082, GP-0101 | core | plan D03 T20 §9 |  |
| IP-2187 | Scalable SVG icon themes | -- | -- | GP-0025 | core | plan D03 T20 §9 |  |
| IP-2188 | Larger spin-scale sliders with plus and minus buttons | -- | -- | GP-0027 | core | plan D03 T20 §9 | Misrouted into RET |
| IP-2189 | Interface theme: dark, light, gray levels, follow OS, highlight color, CSS custom themes, dark title bar, reload theme | PS-B-1208, PS-B-1209 | AF-0047, AF-0059, AF-2689 | GP-0002, GP-0014, GP-0026, GP-3682, GP-3683, GP-4266, GP-4267, GP-4268, GP-4271 | core | plan D03 T20 §9 |  |
| IP-2190 | Icon style and icon theme: color, monochrome, symbolic, legacy | -- | AF-0048, AF-2690 | GP-0013, GP-3684, GP-3685, GP-4182, GP-4183, GP-4184 | core | plan D03 T20 §9 |  |
| IP-2191 | Merge menu bar into the title bar | -- | -- | GP-0016, GP-3692, GP-3693, GP-4189 | core | plan D03 T20 §9 |  |
| IP-2192 | UI scaling: UI font size, scale UI to font, auto or fixed scaling, HiDPI, icon scaling | PS-B-1213, PS-B-1214, PS-B-1215 | AF-2688 | GP-0001, GP-3686, GP-3687, GP-3688, GP-3689, GP-3690, GP-4269, GP-4270 | core | plan D03 T20 §9 |  |
| IP-2193 | Interface language independent of the OS | PS-B-1212 | AF-2663, AF-2737 | GP-3691, GP-4229, GP-4230 | core | plan D03 T20 §9 | extends D03 T07 §16 |
| IP-2194 | Right-to-left layouts | -- | -- | GP-0023 | core | plan D03 T20 §9 | extends D03 T07 §16 |
| IP-2195 | Accessibility display options: larger UI font, handle size, UI contrast, text contrast, brightness, reduce motion | -- | AF-0049, AF-2686, AF-2687 | GP-0024 | core | plan D03 T20 §9 | extends D03 T07 §16 |
| IP-2196 | Canvas and artboard surround colors and borders per screen mode, pasteboard gray levels, image window appearance | PS-B-1210, PS-B-1211 | AF-2684, AF-2685 | -- | core | plan D03 T20 §9 |  |
| IP-2197 | Interface previews: layer, channel, group, undo, and navigation preview sizes | -- | -- | GP-4231, GP-4232, GP-4233, GP-4234, GP-4235, GP-4236 | core | plan D03 T20 §9 |  |
| IP-2198 | Reopen documents on startup | -- | AF-2349 | -- | core | plan D03 T20 §5 |  |
| IP-2199 | GPU canvas rendering preference | PS-A-1750 | -- | -- | core | plan D03 T20 §5 | extends D03 T02 §5 |
| IP-2200 | Background saving | PS-B-0943 | -- | -- | core | plan D03 T20 §5 |  |
| IP-2201 | Export preferences: metadata and color space defaults, legacy Export As | PS-B-1071, PS-B-1072 | -- | -- | format | plan D03 T20 §5 |  |
| IP-2202 | Develop preferences: appearance, file handling and sidecar XMP, performance, technology previews, HDR editing | PS-B-0584, PS-B-0585, PS-B-0586, PS-B-0588, PS-B-0590 | -- | -- | core | plan D03 T20 §5 | XMP read and write in D01 T07 §6 |
| IP-2203 | Image interpolation default | PS-B-1200 | -- | GP-4277 | core | plan D03 T20 §5 |  |
| IP-2204 | File handling preferences: image previews and thumbnails, extension case, save as to original folder, save in background, no copy suffix, thumbnail size limits | PS-B-1245, PS-B-1246, PS-B-1247, PS-B-1248, PS-B-1258 | AF-2652 | GP-4263, GP-4264 | core | plan D03 T20 §5 |  |
| IP-2205 | Raw file open handler preference | PS-B-1253 | -- | GP-4210 | core | plan D03 T20 §5 | extends D03 T07 §11 |
| IP-2206 | Image import policies: promote to float with dither, add alpha, profile policy, ignore EXIF profile tag, rotation metadata policy, lock background on import | PS-B-1254, PS-B-1255 | AF-2693 | GP-4196, GP-4197, GP-4198, GP-4199, GP-4200, GP-4201 | core | plan D03 T20 §5 |  |
| IP-2207 | Export defaults: include color profile, comment, thumbnail, EXIF, XMP, IPTC, update metadata, default export type | -- | -- | GP-4202, GP-4203, GP-4204, GP-4205, GP-4206, GP-4207, GP-4208, GP-4209 | core | plan D03 T20 §5 |  |
| IP-2208 | Performance: memory usage, RAM limit, history and cache presets, cache levels, tile cache and size, undo memory, maximum new image size, threads, CPU optimizations, precise clipping | PS-B-1262, PS-B-1263, PS-B-1264, PS-B-1265, PS-B-1269 | AF-2673, AF-2678 | GP-4255, GP-4257, GP-4258, GP-4259, GP-4261 | core | plan D03 T20 §5 |  |
| IP-2209 | Graphics processor and display renderer: use GPU, OpenCL, anti-aliased guides, 30-bit display, native canvas, renderer choice, high-DPI rendering, compute acceleration | PS-B-1266, PS-B-1267, PS-B-1268 | AF-0054, AF-2680, AF-2681, AF-2682, AF-2683 | GP-0047, GP-4251 | core | plan D03 T20 §5 | extends D03 T02 §5 |
| IP-2210 | View quality and zoom quality | -- | AF-2676 | GP-4163 | core | plan D03 T20 §5 |  |
| IP-2211 | Scratch disks, disk usage warning, temporary and swap folders, swap compression | PS-B-1272, PS-B-1273 | AF-2674 | GP-4174, GP-4175, GP-4176, GP-4260 | core | plan D03 T20 §5 |  |
| IP-2212 | Default new image and default grid preferences, dialog defaults | -- | -- | GP-4157, GP-4158, GP-4245, GP-4246, GP-4247, GP-4248 | core | plan D03 T20 §5 |  |
| IP-2213 | Technology previews and enhanced controls: experimental feature toggles | PS-B-1306, PS-B-1307, PS-B-1309 | -- | GP-4250 | core | plan D03 T20 §5 |  |
| IP-2214 | Windows Explorer thumbnail and preview extensions for Imago files | -- | AF-0056 | -- | core | plan D03 T20 §5 | OS shell integration, closest is file handling |
| IP-2215 | Canvas mouse-button modifier mapping | -- | -- | GP-0031 | core | plan D03 T20 §6 |  |
| IP-2216 | Pressure-sensitive tablets and Surface Dial for brushes | -- | AF-0671, AF-0672 | -- | core | plan D03 T20 §6 | Windows Ink and WinTab |
| IP-2217 | Pen tablet input: pressure, tilt, rotation, velocity, Windows Ink or WinTab choice | -- | AF-0051, AF-2711 | GP-4223 | core | plan D03 T20 §6 |  |
| IP-2218 | Touch and trackpad gestures, touch for gestures only | PS-B-1228 | AF-0053, AF-2709 | -- | core | plan D03 T20 §6 |  |
| IP-2219 | Surface Dial and Surface Pen support | -- | AF-0052, AF-2707 | -- | core | plan D03 T20 §6 |  |
| IP-2220 | Input devices dialog and device status: per-device tools, share tool options, save and reset device settings | -- | -- | GP-0886, GP-3652, GP-4217, GP-4224, GP-4225, GP-4226, GP-4227, GP-4228 | core | plan D03 T20 §6 |  |
| IP-2221 | Input controllers: mouse wheel event actions, enable, dump events | -- | -- | GP-4211, GP-4212, GP-4213, GP-4214, GP-4215, GP-4216 | core | plan D03 T20 §6 |  |
| IP-2222 | Canvas interaction modifiers per input button with reset | -- | -- | GP-4137, GP-4138, GP-4139 | core | plan D03 T20 §6 |  |
| IP-2223 | Preset migration, export, and import | PS-A-1254 | -- | -- | core | plan D03 T20 §7 |  |
| IP-2224 | Preset manager | PS-A-1255 | -- | -- | core | plan D03 T20 §7 |  |
| IP-2225 | Add-on import and export: brushes, styles, palettes, assets, macros | -- | AF-2644 | -- | format | plan D03 T20 §7 |  |
| IP-2226 | Assets panel: categories, add from selection, place, embed in document | -- | AF-2483, AF-2484, AF-2486, AF-2487, AF-2488, AF-2489 | -- | core | plan D03 T20 §7 | (Affinity) |
| IP-2227 | Assets import and export | -- | AF-2485 | -- | format | plan D03 T20 §7 | Own asset package format, Affinity .afassets read if documented |
| IP-2228 | Resource chooser buttons keyboard mnemonics | -- | -- | GP-0114 | core | plan D03 T20 §7 | accessibility detail of resource choosers; closest is resources |
| IP-2229 | Preset Manager: preset types, load, save set, rename, delete, view modes | PS-B-1188, PS-B-1189, PS-B-1190, PS-B-1191 | -- | -- | core | plan D03 T20 §7 |  |
| IP-2230 | Export, import, and migrate presets | PS-B-1192, PS-B-1193 | -- | -- | core | plan D03 T20 §7 |  |
| IP-2231 | Presets in panels with groups, resource tagging, and linked content categories | PS-B-1194 | AF-2658 | GP-4067 | core | plan D03 T20 §7 |  |
| IP-2232 | Data and resource folders: system and personal folders, add, reorder, delete, open lens profiles and fonts folders | -- | AF-2661, AF-2662 | GP-4167, GP-4168, GP-4169, GP-4170, GP-4171, GP-4172, GP-4173 | core | plan D03 T20 §7 |  |
| IP-2233 | Preferences dialog | -- | -- | GP-0905, GP-4159 | core | shipped-scope D03 T07 §17 |  |

## Help and learning

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2234 | Help menu with user manual sections, local or online manual, help buttons, help history, context help | -- | -- | GP-4177, GP-4178, GP-4179, GP-4180, GP-4181, GP-4302, GP-4303, GP-4311 | core | plan D03 T20 §8 | extends D03 T06 §1 |
| IP-2235 | Online links: forums, bug and feature requests, support, developer site, roadmap, legal notices | PS-B-1421, PS-B-1422, PS-B-1424, PS-B-1425 | -- | GP-4304, GP-4305, GP-4306, GP-4307, GP-4308, GP-4309 | core | plan D03 T20 §8 |  |
| IP-2236 | What's new, release notes, and in-app update notifications | PS-B-1382, PS-B-1423 | -- | -- | core | plan D03 T20 §8 |  |
| IP-2237 | Check for updates with frequency setting | PS-B-1420 | AF-2729 | GP-3694, GP-4262 | core | plan D03 T20 §8 |  |
| IP-2238 | Home and welcome screen: recent files with filters and keyboard shortcuts, create new, release notes, contribute, personalize, auto show | PS-B-1205, PS-B-1374, PS-B-1375 | -- | GP-0077, GP-3679, GP-3680, GP-3681, GP-3696, GP-3697, GP-3698 | core | plan D03 T20 §8 |  |
| IP-2239 | Discover panel: in-app help search, tutorials, hands-on learning | PS-B-1343, PS-B-1378, PS-B-1413, PS-B-1426 | -- | -- | core | plan D03 T20 §8 | bundled content, no online learning feed |
| IP-2240 | Tip of the day | -- | -- | GP-4315 | core | plan D03 T20 §8 |  |
| IP-2241 | Status bar modifier key hints | -- | AF-0046 | -- | core | plan D03 T20 §8 |  |
| IP-2242 | System info and GPU compatibility report | PS-B-1416, PS-B-1417 | -- | -- | core | plan D03 T20 §8 |  |
| IP-2243 | Benchmark | -- | AF-0055 | -- | core | plan D03 T20 §8 |  |
| IP-2244 | Dashboard: cache, swap, CPU, memory, groups, update interval, history, performance log recording with markers, low swap warning | -- | -- | GP-3637, GP-3638, GP-3639, GP-3640, GP-3641, GP-3642, GP-3643, GP-3644, GP-3645, GP-3646, GP-3647, GP-3648, GP-3649, GP-3650, GP-3651 | core | plan D03 T20 §8 |  |
| IP-2245 | Error console: clear, save, select all, highlight message kinds | -- | -- | GP-3781, GP-3782, GP-3783, GP-3784, GP-3785, GP-3786, GP-3787 | core | plan D03 T20 §8 |  |
| IP-2246 | Debugging preferences: when to invoke the crash debugger | -- | -- | GP-4152, GP-4153, GP-4154, GP-4155, GP-4156 | core | plan D03 T20 §8 |  |
| IP-2247 | Published default shortcut list | -- | AF-2754 | -- | core | shipped-scope D03 T06 §1 |  |
| IP-2248 | About dialog | PS-B-1414 | -- | GP-4297 | core | shipped-scope D03 T06 §1 |  |
| IP-2249 | Help opens the user manual | PS-B-1412 | -- | GP-4312 | core | shipped-scope D03 T06 §1 |  |

## Automation

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2250 | Photoshop-compatible 64-bit filter plug-ins | -- | AF-1861 | -- | core | plan D03 T14 §11 |  |
| IP-2251 | Host legacy 8BF filter plug-ins | PS-B-0790 | -- | -- | automation | plan D03 T14 §11 |  |
| IP-2252 | Host Photoshop format and acquire plug-ins | PS-B-0791 | -- | -- | automation | plan D03 T14 §11 |  |
| IP-2253 | Photoshop plug-in settings: default folder, search folders, support folder authorization, detected list with support status, allow unknown, restart | -- | AF-1862, AF-1863, AF-1864, AF-1865, AF-1866, AF-1867, AF-1868, AF-2727 | -- | core | plan D03 T14 §11 |  |
| IP-2254 | Manage installed plug-ins and About Plug-ins list | PS-B-0787, PS-B-1415 | -- | -- | automation | plan D03 T14 §11 | Imago-native plug-in manager |
| IP-2255 | Extension modules manager | -- | -- | GP-0910 | core | plan D03 T14 §12 |  |
| IP-2256 | Third-party engine operations appear as filters | -- | -- | GP-4884 | automation | plan D03 T14 §12 |  |
| IP-2257 | Plug-in API messages only in interactive mode | -- | -- | GP-0106 | automation | backlog B-041 |  |
| IP-2258 | Select subject recordable in macros | -- | AF-2122 | -- | automation | backlog B-041 | Shortcut binding via D03 T20 §3 |
| IP-2259 | MCP server for external AI agents with file, network, script, AI tool, and local memory permissions | -- | AF-2171, AF-2172, AF-2173, AF-2174, AF-2175, AF-2176, AF-2177 | -- | automation | backlog B-041 |  |
| IP-2260 | GEGL Graph filter (op pipeline text) | -- | -- | GP-2508, GP-2509 | automation | backlog B-041 | GEGL graph editing |
| IP-2261 | Filters Development submenu | -- | -- | GP-3312 | automation | backlog B-041 |  |
| IP-2262 | Scripts submenu | PS-B-0930 | -- | -- | automation | backlog B-041 |  |
| IP-2263 | Macro files .afmacro and .afmacros | -- | AF-2638 | -- | automation | backlog B-041 |  |
| IP-2264 | GEGL operations register into menus via metadata | -- | -- | GP-0008 | automation | backlog B-041 |  |
| IP-2265 | Layer tagging recorded in macros | -- | AF-0924 | -- | automation | backlog B-041 |  |
| IP-2266 | Multi-layer plug-in filter API | -- | -- | GP-0045 | automation | backlog B-041 |  |
| IP-2267 | GIMP SDK for plug-in and filter builds | -- | -- | GP-0105 | automation | backlog B-041 |  |
| IP-2268 | Actions panel: list and button modes, record, play, stop, new set and action, duplicate, delete, step and dialog toggles | PS-B-0663, PS-B-0664, PS-B-0665, PS-B-0666, PS-B-0667, PS-B-0668, PS-B-0669, PS-B-0670, PS-B-0671, PS-B-0672, PS-B-0673, PS-B-0674, PS-B-0675, PS-B-0676, PS-B-0677, PS-B-0678 | -- | -- | automation | backlog B-041 |  |
| IP-2269 | Action step editing: record again, insert menu item, insert stop, insert path, action options | PS-B-0679, PS-B-0680, PS-B-0681, PS-B-0683, PS-B-0684 | -- | -- | automation | backlog B-041 |  |
| IP-2270 | Action playback options, tool recording, relative values, and single history state playback | PS-B-0685, PS-B-0686, PS-B-0695, PS-B-0696 | -- | -- | automation | backlog B-041 |  |
| IP-2271 | Action set files: load, replace, save ATN, clear, reset, built-in action sets | PS-B-0687, PS-B-0688, PS-B-0689, PS-B-0690, PS-B-0691, PS-B-0692 | -- | -- | automation | backlog B-041 |  |
| IP-2272 | Macros: record, play, reset, step toggles, edit step settings, exposed parameters, recordable AI, LUT, and color tag steps | -- | AF-2181, AF-2182, AF-2183, AF-2184, AF-2185, AF-2186, AF-2187, AF-2190, AF-2191, AF-2208 | -- | automation | backlog B-041 |  |
| IP-2273 | Macro library panel: categories, search, scaling and alignment on apply, import and export macro files | -- | AF-2188, AF-2189, AF-2192, AF-2193, AF-2194, AF-2195, AF-2196, AF-2197 | -- | automation | backlog B-041 |  |
| IP-2274 | Script events manager: run scripts or actions on application events | PS-B-0768, PS-B-0769, PS-B-0770, PS-B-0771 | -- | -- | automation | backlog B-041 |  |
| IP-2275 | Run a script file and a startup scripts folder listed in the Scripts menu | PS-B-0778, PS-B-0782 | -- | -- | automation | backlog B-041 |  |
| IP-2276 | Scripting object model and low-level command descriptors with a command listener log | PS-B-0779, PS-B-0780, PS-B-0781 | -- | -- | automation | backlog B-041 | Imago equivalent of ExtendScript, Action Manager, ScriptListener |
| IP-2277 | Modern script files and descriptor playback (UXP scripts, batchPlay) | PS-B-0783, PS-B-0784 | -- | -- | automation | backlog B-041 |  |
| IP-2278 | JavaScript scripting workspace: scripts panel, run script, trusted scripts, scripts with their own UI, examples | -- | AF-0017, AF-2209, AF-2210, AF-2211, AF-2212, AF-2213, AF-2215 | -- | automation | backlog B-041 | Affinity Scripting Studio |
| IP-2279 | AI-generated scripts from a natural-language request | -- | AF-2214 | -- | automation | backlog B-041 | would use the Imago assistant (D03 T19 §10) once scripting exists |
| IP-2280 | Model Context Protocol server for external AI agents | -- | AF-2733 | -- | automation | backlog B-041 |  |
| IP-2281 | Extension panels: plug-ins that add dockable panels, commands, and dialogs, with networking, developer mode, and a developer tool | PS-B-0785, PS-B-0788, PS-B-0789, PS-B-1295, PS-B-1296, PS-B-1297, PS-B-1329 | -- | -- | automation | backlog B-041 |  |
| IP-2282 | Generator plug-in platform and remote connections | PS-B-0792, PS-B-1197, PS-B-1293, PS-B-1294 | -- | -- | automation | backlog B-041 | asset generation itself is D03 T18 §1 |
| IP-2283 | Plug-in API: procedure-driven auto dialogs and bindings for Python, JavaScript, Lua, Vala, C | -- | -- | GP-0043, GP-0044, GP-4878, GP-4880, GP-4881 | automation | backlog B-041 |  |
| IP-2284 | Script-Fu scripts registered as menu commands, refresh scripts, scripts applying engine filters | -- | -- | GP-0112, GP-3300, GP-4879, GP-4886 | automation | backlog B-041 |  |
| IP-2285 | Script consoles for Python and Script-Fu with save, clear, and procedure browse | -- | -- | GP-3314, GP-3315, GP-3316, GP-3317, GP-3318, GP-3319, GP-3320, GP-3321, GP-3323, GP-3324, GP-3325, GP-3326 | automation | backlog B-041 |  |
| IP-2286 | Script-Fu server: listen address, port, log file | -- | -- | GP-3322, GP-3327, GP-3328, GP-3329 | automation | backlog B-041 |  |
| IP-2287 | Procedure database and procedure browser searchable by name, description, help, author, copyright, date, type | -- | -- | GP-3330, GP-3331, GP-3332, GP-3333, GP-3334, GP-3335, GP-3336, GP-3337, GP-4882 | automation | backlog B-041 |  |
| IP-2288 | Plug-in browser | -- | -- | GP-3342 | automation | backlog B-041 |  |
| IP-2289 | Demo plug-ins for plug-in authors | -- | -- | GP-4885 | automation | backlog B-041 |  |
| IP-2290 | Automate submenu | PS-B-0929 | -- | -- | automation | backlog B-042 | non-batch items are planned in their own sections |
| IP-2291 | Variable data sets import and export | PS-B-0913, PS-B-0931 | -- | -- | automation | backlog B-042 |  |
| IP-2292 | Variables and data sets: define visibility, text, and pixel replacement variables, import CSV data sets, apply, export data sets as files | PS-A-1212, PS-A-1213, PS-A-1214, PS-A-1215, PS-A-1216, PS-B-0793, PS-B-0794, PS-B-0795, PS-B-0796, PS-B-0797, PS-B-0798, PS-B-0799 | -- | -- | automation | backlog B-042 |  |
| IP-2293 | Conditional actions: if current document state then play or else play | PS-B-0682, PS-B-0693, PS-B-0694 | -- | -- | automation | backlog B-042 |  |
| IP-2294 | Batch: run an action on a folder, opened files, or import with source, destination, naming, override, and error options | PS-B-0698, PS-B-0699, PS-B-0700, PS-B-0701, PS-B-0702, PS-B-0703, PS-B-0704, PS-B-0705, PS-B-0706, PS-B-0707, PS-B-0708, PS-B-0709 | -- | -- | automation | backlog B-042 |  |
| IP-2295 | Droplets: save an action as a standalone processor for dropped files | PS-B-0710, PS-B-0711 | -- | -- | automation | backlog B-042 |  |
| IP-2296 | Batch job: process many files including RAW with develop preset, parallel processing, destination, formats, resize, macros, and a progress panel | -- | AF-2198, AF-2199, AF-2200, AF-2201, AF-2202, AF-2203, AF-2204, AF-2205, AF-2206, AF-2207 | -- | automation | backlog B-042 |  |
| IP-2297 | Image Processor: convert and resize folders to JPEG, PSD, TIFF with action, copyright, ICC, saved settings | PS-B-0753, PS-B-0754, PS-B-0755, PS-B-0756, PS-B-0757, PS-B-0758, PS-B-0759, PS-B-0760 | -- | -- | automation | backlog B-042 |  |
| IP-2298 | Headless batch mode and command line scripting | -- | -- | GP-4883 | automation | backlog B-042 |  |

## Video and animation

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2299 | Render video | PS-B-0915 | -- | -- | video | backlog B-043 |  |
| IP-2300 | Video files open and video frames to layers | PS-B-0932, PS-B-1033 | -- | -- | video | backlog B-043 |  |
| IP-2301 | Video layers | PS-A-0664, PS-A-0692 | -- | -- | video | backlog B-043 |  |
| IP-2302 | Clone source frame offset and lock frame | PS-A-0318 | -- | -- | video | backlog B-043 |  |
| IP-2303 | Video timeline panel: tracks, add media, playhead and play controls, playback resolution and loop, zoom, work area, frame rate, shortcut keys, frame skipping, lock and hide tracks | PS-B-0800, PS-B-0801, PS-B-0803, PS-B-0804, PS-B-0806, PS-B-0809, PS-B-0810, PS-B-0811, PS-B-0812, PS-B-0814, PS-B-0822, PS-B-0823, PS-B-0824, PS-B-0827 | -- | -- | video | backlog B-043 |  |
| IP-2304 | Timeline clip editing: split at playhead, duration and speed, transitions | PS-B-0807, PS-B-0808, PS-B-0815 | -- | -- | video | backlog B-043 |  |
| IP-2305 | Timeline audio tracks: add audio, volume, fades, mute | PS-B-0805, PS-B-0813 | -- | -- | video | backlog B-043 |  |
| IP-2306 | Timeline motion presets and property keyframes with linear or hold interpolation | PS-B-0816, PS-B-0817, PS-B-0818, PS-B-0819 | -- | -- | video | backlog B-043 |  |
| IP-2307 | Timeline comments track and comment export | PS-B-0825, PS-B-0826 | -- | -- | video | backlog B-043 |  |
| IP-2308 | Video layers: new from file, blank, insert, duplicate, delete, restore, reload frames, replace and interpret footage, show altered, rasterize | PS-B-0828, PS-B-0829, PS-B-0830, PS-B-0831, PS-B-0832, PS-B-0833, PS-B-0834, PS-B-0835, PS-B-0836, PS-B-0837, PS-B-0838, PS-B-0839 | -- | -- | video | backlog B-043 |  |
| IP-2309 | Video preview on an external device | PS-B-0841 | -- | -- | video | backlog B-043 |  |
| IP-2310 | Video frames to layers with range, every n frames, make frame animation | PS-B-0842, PS-B-0843 | -- | -- | video | backlog B-043 |  |
| IP-2311 | Render video: encoder presets, size, frame rate, field order, image sequences, range, alpha, audio | PS-B-0844, PS-B-0845, PS-B-0846, PS-B-0847, PS-B-0848, PS-B-0849, PS-B-0850, PS-B-0851, PS-B-0853 | -- | -- | video | backlog B-043 |  |
| IP-2312 | Animated GIF export: loop, repeats, delay, disposal | -- | -- | GP-4487, GP-4488, GP-4489, GP-4490, GP-4491, GP-4492, GP-4493, GP-4494 | video | backlog B-044 |  |
| IP-2313 | Save for Web animation controls | PS-B-1082 | -- | -- | format | backlog B-044 |  |
| IP-2314 | Layer as frame export modes: replace and combine | -- | -- | GP-4327, GP-4328 | format | backlog B-044 |  |
| IP-2315 | Animated WebP export | -- | -- | GP-4753 | video | backlog B-044 |  |
| IP-2316 | APNG open and export | -- | -- | GP-4806 | video | backlog B-044 |  |
| IP-2317 | FLI and FLC animation open and export with frame range | -- | -- | GP-4479, GP-4480, GP-4481, GP-4849 | video | backlog B-044 |  |
| IP-2318 | MNG animation export | -- | -- | GP-4626, GP-4850 | video | backlog B-044 |  |
| IP-2319 | Warp transform animate to frames | -- | -- | GP-0772 | core | backlog B-044 |  |
| IP-2320 | Frame animation panel: create, duplicate frames, delay, looping, new layer visible in all frames, propagate frame 1, unify buttons, reverse, delete, palette options | PS-B-0802, PS-B-0854, PS-B-0855, PS-B-0856, PS-B-0859, PS-B-0860, PS-B-0861, PS-B-0867, PS-B-0868, PS-B-0869 | -- | -- | video | backlog B-044 |  |
| IP-2321 | Tween frames: position, opacity, effects | PS-B-0857, PS-B-0858 | -- | -- | video | backlog B-044 |  |
| IP-2322 | Frames and layers: make frames from layers, flatten frames into layers, match layer across frames, new layer per frame | PS-B-0862, PS-B-0863, PS-B-0864, PS-B-0865 | -- | -- | video | backlog B-044 |  |
| IP-2323 | Optimize and unoptimize animation for GIF: bounding box, redundant pixel removal, difference optimization | PS-B-0866 | -- | GP-1820, GP-1821 | video | backlog B-044 |  |
| IP-2324 | Onion skin with frame count, spacing, opacity, blend mode settings | PS-B-0820, PS-B-0821 | -- | -- | video | backlog B-044 |  |
| IP-2325 | Animation playback of a layered image: combine or replace layers, frame rate, speed, zoom, reload, detach, step and rewind controls | -- | -- | GP-1803, GP-1804, GP-1805, GP-1806, GP-1807, GP-1808, GP-1809, GP-1810, GP-1811, GP-1812, GP-1813, GP-1814, GP-1815, GP-1816, GP-1817, GP-1818, GP-1819 | video | backlog B-044 |  |
| IP-2326 | Animation blend: intermediate frames, max blur radius, looped | -- | -- | GP-1822, GP-1823, GP-1824, GP-1825 | video | backlog B-044 |  |
| IP-2327 | Animation burn-in: glow color, fadeout, corona, after glow, speed, prepare for GIF | -- | -- | GP-1826, GP-1827, GP-1828, GP-1829, GP-1830, GP-1831, GP-1832, GP-1833, GP-1834 | video | backlog B-044 |  |
| IP-2328 | Animation rippling: strength, number of frames, edge behavior | -- | -- | GP-1835, GP-1836, GP-1837, GP-1838 | video | backlog B-044 |  |
| IP-2329 | Animation spinning globe: frames, direction, transparent background, index colors, work on copy | -- | -- | GP-1839, GP-1840, GP-1841, GP-1842, GP-1843, GP-1844 | video | backlog B-044 |  |
| IP-2330 | Animation waves: amplitude, wavelength, number of frames, invert direction | -- | -- | GP-1845, GP-1846, GP-1847, GP-1848, GP-1849 | video | backlog B-044 |  |

## Cloud and collaboration

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2331 | Rate and report AI output to the vendor | PS-B-0434, PS-B-0597 | AF-2116 | -- | cloud | excluded: cloud | Vendor feedback channel |
| IP-2332 | Neural filters wait list voting | PS-B-0462 | -- | -- | ai | excluded: cloud | Vendor online voting |
| IP-2333 | Send layers to Firefly Boards | PS-B-0629 | -- | -- | cloud | excluded: cloud | Adobe web app hand-off |
| IP-2334 | Photoshop on the web generative extras | PS-B-0662 | -- | -- | cloud | excluded: cloud | Web version |
| IP-2335 | Canva premium plan requirement for AI | -- | AF-2108 | -- | cloud | excluded: cloud | Account feature |
| IP-2336 | Share MCP task hints with the vendor | -- | AF-2178 | -- | cloud | excluded: cloud | Vendor telemetry |
| IP-2337 | Browse filters online | PS-B-0010 | -- | -- | core | excluded: cloud | Adobe Exchange marketplace |
| IP-2338 | Creative Cloud Library linked graphics | PS-A-0736 | -- | -- | cloud | excluded: cloud | Adobe cloud libraries |
| IP-2339 | Stock panel | -- | AF-2479, AF-2480, AF-2481, AF-2482 | -- | cloud | excluded: cloud | Online stock services |
| IP-2340 | Export to Canva | -- | AF-2572 | -- | cloud | excluded: cloud |  |
| IP-2341 | Plug-in and extension marketplaces | PS-B-0786, PS-B-1328 | -- | -- | automation | excluded: cloud | Creative Cloud marketplace and Adobe Exchange |
| IP-2342 | Cloud documents: storage, offline availability, cloud search, save to cloud, default file location | PS-B-1250, PS-B-1260, PS-B-1383, PS-B-1384, PS-B-1387, PS-B-1388 | -- | -- | cloud | excluded: cloud |  |
| IP-2343 | Cloud version history panel | PS-B-1361, PS-B-1385, PS-B-1386 | -- | -- | cloud | excluded: cloud |  |
| IP-2344 | Home cloud sections: shared with you, deleted | PS-B-1376, PS-B-1377 | -- | -- | cloud | excluded: cloud |  |
| IP-2345 | Invite to edit, share for review, and comments | PS-B-1389, PS-B-1390, PS-B-1391, PS-B-1392, PS-B-1393, PS-B-1394, PS-B-1395 | -- | -- | cloud | excluded: cloud |  |
| IP-2346 | Creative Cloud Libraries panel | PS-B-1396, PS-B-1397, PS-B-1398, PS-B-1399, PS-B-1400, PS-B-1401 | -- | -- | cloud | excluded: cloud |  |
| IP-2347 | Adobe Fonts activation and auto-activation | PS-B-1305, PS-B-1402, PS-B-1403 | -- | -- | cloud | excluded: cloud |  |
| IP-2348 | Account: sign in, manage account, account menu, settings sync, Canva login | PS-B-1380, PS-B-1404, PS-B-1418, PS-B-1419 | AF-2755, AF-2756 | -- | cloud | excluded: cloud |  |
| IP-2349 | Stock panels and stock search | PS-B-1365 | AF-2657, AF-2761 | -- | cloud | excluded: cloud |  |
| IP-2350 | Firefly Boards, Adobe Express, Lightroom cloud photos, Canva export, Canva integrations | PS-B-1405, PS-B-1406, PS-B-1407 | AF-2757, AF-2762 | -- | cloud | excluded: cloud |  |
| IP-2351 | Canva Brand Kit live sync and premium AI plans | -- | AF-2758, AF-2759 | -- | cloud | excluded: cloud |  |
| IP-2352 | Linked services mapping cloud storage and local network file sharing | -- | AF-2659, AF-2728, AF-2760 | -- | cloud | excluded: cloud |  |
| IP-2353 | Web, iPad, and mobile versions | PS-B-1408, PS-B-1409, PS-B-1410, PS-B-1411 | -- | -- | cloud | excluded: cloud |  |

## 3D (removed)

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2354 | Layer to 3D model with model tool and projection editing | -- | AF-2133, AF-2157, AF-2158, AF-2159 | -- | cloud | excluded: cloud | Canva server 3D reconstruction; Imago has no 3D layers |
| IP-2355 | Show 3D overlays | PS-A-1735 | -- | -- | 3d | excluded: removed | Legacy 3D removed from Photoshop |
| IP-2356 | Generate normal map and generate bump map (legacy 3D filters) | PS-B-0335, PS-B-0336 | -- | -- | 3d | excluded: removed | Removed with Photoshop 3D; normal map lives in D01 T06 §13 |
| IP-2357 | Move tool 3D mode buttons | PS-A-0043 | -- | -- | 3d | excluded: removed | Photoshop legacy 3D retired |
| IP-2358 | Render video 3D quality option | PS-B-0852 | -- | -- | video | excluded: removed | legacy 3D removed |
| IP-2359 | Legacy 3D menu, 3D panel, and 3D print | PS-B-0870, PS-B-0871, PS-B-0872, PS-B-0873 | -- | -- | 3d | excluded: removed | Photoshop removed legacy 3D in 25.x |
| IP-2360 | Legacy 3D file formats: OBJ, 3DS, DAE, KMZ, U3D, STL, glTF | PS-B-0874 | -- | -- | 3d | excluded: removed | Photoshop removed legacy 3D in 25.x |
| IP-2361 | 3D preferences | PS-B-1310 | -- | -- | 3d | excluded: removed | removed with legacy 3D |

## Companion and other apps

| ID | Feature | Photoshop | Affinity | GIMP | Category | Status | Notes |
| -- | ------- | --------- | -------- | ---- | -------- | ------ | ----- |
| IP-2362 | Layout studio | -- | AF-0005 | -- | print | other-app: Nodus page layout and publishing |  |
| IP-2363 | Unified vector, photo, and layout app | -- | AF-0001 | -- | core | other-app: Nodus vector and layout disciplines live in Nodus, Imago is the photo discipline |  |
| IP-2364 | Vector studio | -- | AF-0004 | -- | core | other-app: Nodus vector drawing workspace |  |
| IP-2365 | Substance 3D Viewer integration and Substance 3D materials | PS-B-0875, PS-B-0876 | -- | -- | 3d | other-app: none Adobe Substance 3D companion products |  |
| IP-2366 | G'MIC-Qt third-party filter collection | -- | -- | GP-4888 | automation | plan D03 T14 §13 | G'MIC core (CeCILL-2.1, GPL-compatible) runs in the D01 T09 §1 host process |
| IP-2367 | DaVinci Resolve and Cavalry integration | -- | AF-2640, AF-2641 | -- | video | other-app: none third-party video and animation products |  |
