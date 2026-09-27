# Albumen Parity Catalog

Every Adobe Lightroom Classic 15.5.1, ACDSee Photo Studio Ultimate 2027, and IrfanView 4.76 feature, merged into Albumen features, each with exactly one status. The sources are [`sources/lightroom-classic-15.5.1.md`](sources/lightroom-classic-15.5.1.md), [`sources/acdsee-ultimate-2027.md`](sources/acdsee-ultimate-2027.md), and [`sources/irfanview-4.76.md`](sources/irfanview-4.76.md); the status grammar and the update rules are in [`README.md`](README.md); the sections that own `plan` rows are designed in [`albumen-section-design.md`](albumen-section-design.md).

**Totals (2026-09-27, integrated the same day, updated for the operator's decisions later that day):** 1,622 features covering 1,857 Lightroom Classic rows, 5,182 ACDSee rows, and 1,880 IrfanView rows (8,919 in all); every source id appears in exactly one row. At integration LP-1045 and LP-1051 were split (the shared `D01 T08` codecs now read CPT and FlashPix; the rest stays in B-050 as LP-1621 and LP-1622), the Explorer preview handler (LP-0031) moved to backlog B-051, and the four former B-012 rows moved onto the suite plug-in host `D01 T09`. ACDSee Edit mode (layered pixel editing) and IrfanView Paint are routed to Pinxit as `other-app: Pinxit` rows naming the Pinxit catalog row that covers each capability; keyboard-shortcut and menu rows are folded into the feature they trigger or into the keymap features of the "Keyboard shortcuts and menus" area. Later on 2026-09-27 the operator's dependency decisions moved face recognition and the People view (LP-0291, LP-0695, LP-0700, LP-0702, LP-0704 to LP-0707, LP-0712 to LP-0714, and LP-0716) to backlog B-052, since the local YuNet and SFace face models were not approved for Albumen; face detection (LP-0420, LP-0693, LP-0694, LP-0696 to LP-0698) stays planned through an OpenRouter vision model on explicit send; slideshow music moved from NAudio to Windows Media Foundation through Vortice; and LP-0953's SFTP option is backlog B-053 while its FTP and FTPS parts stay planned. Later on 2026-09-27 the operator decided to plan the work deferred to after the first release as real sections, because the operator worried "features will be left behind": the 63 rows that pointed at B-041 to B-044 and B-050 are planned, recorded actions, extension points, and the command line in `D04 T17` (Phase 42), video and audio in `D04 T16` (Phase 43), CAD and plotter drawings on Stilus's moved readers in `D04 T13 §9` (Phase 30, whose dependencies are met there), and SWF, the GDAL formats, and the clean-room layered formats in `D04 T13 §10` to `§12` (Phase 45); tethered capture (B-048), self-running slideshows (B-049), the Explorer preview handler (B-051), face recognition (B-052), SFTP (B-053), and Content Credentials (B-047) stay in the backlog.

| Status | Features | Source rows |
| ------ | -------: | ----------: |
| `plan` | 1,126 | 6,654 |
| `shipped-scope` | 52 | 282 |
| `backlog` | 21 | 144 |
| `excluded` | 24 | 209 |
| `other-app` | 399 | 1,630 |
| **Total** | **1,622** | **8,919** |

## Areas

- [Viewer: startup, decoding, and default-app integration](#viewer-startup-decoding-and-default-app-integration) (32)
- [Viewer: display, zoom, and navigation](#viewer-display-zoom-and-navigation) (44)
- [Viewer: fullscreen, slideshow, and information](#viewer-fullscreen-slideshow-and-information) (39)
- [Viewer: quick edits](#viewer-quick-edits) (59)
- [Browsing and file management](#browsing-and-file-management) (77)
- [Library views and culling](#library-views-and-culling) (56)
- [Collections, search, and categories](#collections-search-and-categories) (57)
- [Catalog management](#catalog-management) (67)
- [Import and capture](#import-and-capture) (45)
- [Metadata and keywords](#metadata-and-keywords) (60)
- [Map and places](#map-and-places) (17)
- [Develop: workspace, history, and presets](#develop-workspace-history-and-presets) (62)
- [Develop: tone, color, and detail](#develop-tone-color-and-detail) (31)
- [Develop: lens, geometry, effects, and crop](#develop-lens-geometry-effects-and-crop) (20)
- [Develop: masking and retouching](#develop-masking-and-retouching) (20)
- [Photo merge](#photo-merge) (6)
- [People and faces](#people-and-faces) (24)
- [AI](#ai) (35)
- [Batch processing](#batch-processing) (97)
- [Export and publish](#export-and-publish) (46)
- [Print and contact sheets](#print-and-contact-sheets) (31)
- [Slideshow](#slideshow) (22)
- [Web, books, and documents](#web-books-and-documents) (24)
- [Formats](#formats) (88)
- [Workspace and UI](#workspace-and-ui) (38)
- [Preferences](#preferences) (29)
- [Keyboard shortcuts and menus](#keyboard-shortcuts-and-menus) (7)
- [Help and program](#help-and-program) (11)
- [Automation, plug-ins, and command line](#automation-plug-ins-and-command-line) (22)
- [Video and audio](#video-and-audio) (31)
- [Cloud and online services](#cloud-and-online-services) (20)
- [Routed to Pinxit](#routed-to-pinxit) (405)

## Viewer: startup, decoding, and default-app integration

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0001 | Hand-off between viewer and Albumen: open the photo or group from the library in the viewer, return to the library, open in browse, develop, or edit from the viewer, open the folder as thumbnails | -- | AC-0088, AC-0089, AC-0100, AC-4001 | IV-0087 | core | plan D04 T04 §1 | catalog one keystroke away through D01 T02 §3 forwarding |
| LP-0002 | The Albumen Viewer: a separate lightweight single-image viewer (Quick View) that opens from Explorer while Albumen is closed, closes with Esc, and exits cleanly | -- | AC-1851, AC-3995, AC-4000, AC-4253, AC-4311 | IV-0127 | core | plan D04 T04 §1 |  |
| LP-0003 | Notification area icon | -- | AC-4019 | -- | core | plan D04 T04 §17 | the resident quick-start mode, split from D04 T04 §1 at authoring |
| LP-0004 | Viewer windows: files opened from other apps reuse the viewer or open a new window, open the current file in a new window | -- | AC-4245, AC-4246, AC-4477 | IV-0082, IV-1462 | core | plan D04 T04 §1 |  |
| LP-0005 | Small footprint and fast start | -- | -- | IV-0003 | core | plan D04 T04 §1 |  |
| LP-0006 | Viewer exit behavior: ESC closes, warning on ESC exit, ask to save changes, double-click icon closes | -- | -- | IV-0046, IV-0047, IV-0048, IV-0930, IV-0931, IV-1403 | core | plan D04 T04 §1 |  |
| LP-0007 | Only one viewer instance or several | -- | -- | IV-0929 | core | plan D04 T04 §1 |  |
| LP-0008 | Open a file or several files given on the command line | -- | -- | IV-1259, IV-1377 | automation | plan D04 T04 §1 | only the plain open; other switches are D04 T17 §3 |
| LP-0009 | RAW in the viewer: embedded JPEG preview by default, quick RAW decode on demand or when zooming past the preview, toolbar switch between the two | -- | AC-0124, AC-1862, AC-1863, AC-1864, AC-2053, AC-4631 | -- | core | plan D04 T04 §2 | decodes through D04 T01 §4 |
| LP-0010 | Developed versus original in the viewer: developed RAW and edited images show their developed result, press and hold to show the original | -- | AC-1861, AC-2020, AC-4629 | -- | core | plan D04 T04 §2 |  |
| LP-0011 | DNG opcode geometry: apply embedded distortion correction tags when viewing DNG files | -- | AC-1865 | -- | core | plan D04 T04 §2 |  |
| LP-0012 | Display gamma correction for viewing, including resampled black and white gamma | -- | AC-4012 | IV-0955, IV-0956 | core | plan D04 T04 §2 |  |
| LP-0013 | Auto-rotate JPEG and TIFF by EXIF orientation on display | -- | AC-4015 | IV-0933 | core | plan D04 T04 §2 |  |
| LP-0014 | RAW display: embedded preview, half size, or full decode | -- | AC-4022, AC-4023 | IV-1007, IV-1008 | core | plan D04 T04 §2 | decoder from D04 T01 §4 |
| LP-0015 | Prefetch and caching in the viewer: decode the next image in advance and keep the previous image in memory | -- | AC-4243, AC-4244 | -- | core | plan D04 T04 §2 |  |
| LP-0016 | Progressive instant preview that sharpens as decoding completes | -- | AC-4252 | -- | core | plan D04 T04 §2 |  |
| LP-0017 | Display gamma and color correction while viewing | -- | AC-4312 | -- | core | plan D04 T04 §2 | monitor profile through D01 T04 |
| LP-0018 | Legacy load-as-grayscale display options | -- | -- | IV-0036, IV-0934 | core | plan D04 T04 §2 | display only |
| LP-0019 | Clear error when a file cannot be decoded | -- | -- | IV-0074 | core | plan D04 T04 §2 | typed failure naming the format and decoder |
| LP-0020 | JPEG deblocking on load | -- | -- | IV-0935 | core | plan D04 T04 §2 | consumes D01 T06 §5 artifact removal |
| LP-0021 | Viewer color management: tagged and untagged images, monitor profile, input profile, apply profile to pixels | -- | -- | IV-0970, IV-0971, IV-0972, IV-0973, IV-0974 | core | plan D04 T04 §2 | consumes D01 T04 §1 |
| LP-0022 | Smooth JPEG blocking on load (quantization smoothing) | -- | -- | IV-1076 | core | plan D04 T04 §2 | consumes the JPEG artifact reduction of D01 T06 §5 |
| LP-0023 | Color management for display | -- | -- | IV-1079 | core | plan D04 T04 §2 | consumes D01 T04 (lcms2, MIT) |
| LP-0024 | Make Albumen Viewer the default photo viewer, with a prompt on second launch | -- | AC-4054 | -- | core | plan D04 T04 §3 | registers capabilities and opens Windows Default Apps; Windows forbids setting defaults silently |
| LP-0025 | File association settings per format group (image, RAW, media, archive) with associate and disassociate | -- | AC-5181, AC-5182 | -- | core | plan D04 T04 §3 |  |
| LP-0026 | File associations: choose types, all, images only, clear, custom extensions, Default Apps hand-off, registry attempt, all users, per-format icons | -- | -- | IV-0939, IV-0940, IV-0941, IV-0942, IV-0943, IV-0944, IV-0950, IV-0951 | core | plan D04 T04 §3 | Windows only lets the user confirm defaults in Settings |
| LP-0027 | Explorer integration: Send To, Browse with Albumen on folders and drives, context menu operations for slideshow, thumbnails, lossless rotation, filename list, multipage, panorama | -- | -- | IV-0948, IV-0949, IV-1037, IV-1038, IV-1039, IV-1040, IV-1042, IV-1043, IV-1044 | core | plan D04 T04 §3 |  |
| LP-0028 | Extra icons for file associations | -- | -- | IV-1067 | core | plan D04 T04 §3 |  |
| LP-0029 | External editors from the viewer: up to three configured editors named in the menu, toolbar button | -- | AC-0109 | IV-0080, IV-0081, IV-1478, IV-1479, IV-1480, IV-1481 | core | plan D04 T04 §6 |  |
| LP-0030 | Open the file with the Windows-associated application or the default editor (shell open and shell edit) | -- | AC-2018, AC-2019, AC-4472, AC-4478, AC-4565, AC-4566 | -- | core | plan D04 T04 §6 |  |
| LP-0031 | Explorer context menu preview (PicaView): preview and EXIF in the right-click menu, main or sub-menu placement, size, show original, enable switch | -- | AC-3988, AC-3989, AC-3990, AC-3991, AC-3992, AC-3993, AC-3994, AC-4326, AC-5040 | -- | core | backlog B-051 | needs an in-process COM shell extension; not chosen by the operator on 2026-09-27, kept as B-051 |
| LP-0032 | Dither on 16-bit displays | -- | -- | IV-0954 | core | excluded: platform 16 bpp displays are not supported by Windows 11 |  |

## Viewer: display, zoom, and navigation

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0033 | Magnifying glass: pane or on-image magnifier with magnification, fixed or relative, smooth or pixel display, also in fullscreen | -- | AC-0095, AC-2060, AC-2061, AC-2062, AC-2063, AC-4574, AC-4575, AC-4576 | IV-0748, IV-0799, IV-1531 | core | plan D04 T04 §4 |  |
| LP-0034 | Navigator pane and quick navigator overlay with magnification slider and draggable view marquee | -- | AC-0096, AC-0118, AC-2054, AC-2055, AC-2056, AC-2057, AC-4577 | -- | core | plan D04 T04 §4 |  |
| LP-0035 | Pan: scroll tool, drag, right-button drag, arrow keys with faster and slower modifiers, numeric keypad jumps, horizontal wheel | -- | AC-0105, AC-1852, AC-2058, AC-2059, AC-4624, AC-4632 | IV-0075, IV-0749, IV-0750, IV-1386, IV-1387, IV-1540, IV-1563, IV-1564, IV-1571 | core | plan D04 T04 §4 |  |
| LP-0036 | Zoom in and out, zoom tool, zoom slider, preset list, Zoom To dialog with a typed percentage, click to toggle actual size, Ctrl plus wheel zoom at the pointer | -- | AC-0107, AC-0119, AC-0120, AC-2033, AC-2034, AC-2035, AC-2043, AC-2047, AC-3998, AC-4614, AC-4615, AC-4623, AC-4635, AC-4698, AC-4699 | IV-0740, IV-0741, IV-0742, IV-0743, IV-1383, IV-1384, IV-1385, IV-1568, IV-1569, IV-1570 | core | plan D04 T04 §4 |  |
| LP-0037 | Zoom lock and pan lock: keep zoom and scroll position across images | -- | AC-0121, AC-2040, AC-2041, AC-2048, AC-4621, AC-4622 | IV-0744, IV-0746, IV-1488, IV-1514 | core | plan D04 T04 §4 |  |
| LP-0038 | Actual size and fit modes: fit image, width, height, smaller side, reduce only, enlarge only, reduce or enlarge, default zoom mode, fit toggle key | -- | AC-0122, AC-0123, AC-2036, AC-2037, AC-2038, AC-2039, AC-2042, AC-2044, AC-2045, AC-2046, AC-2049, AC-2050, AC-2051, AC-2052, AC-4317, AC-4318, AC-4617, AC-4618, AC-4619, AC-4620 | IV-0715, IV-0716, IV-0717, IV-0718, IV-0719, IV-0725, IV-0730, IV-0745, IV-1457, IV-1484, IV-1499, IV-1561 | core | plan D04 T04 §4 |  |
| LP-0039 | Temporary view rotation in the viewer without changing the file | -- | AC-3997 | -- | core | plan D04 T04 §4 |  |
| LP-0040 | Viewer zoom defaults: default zoom mode, reset on image change, auto shrink or enlarge, click zooming, pan speed | -- | AC-4268, AC-4269, AC-4270, AC-4271, AC-4272 | -- | core | plan D04 T04 §4 |  |
| LP-0041 | Zoom value box | -- | -- | IV-0062 | core | plan D04 T04 §4 |  |
| LP-0042 | Zoom magnifier window | -- | -- | IV-0961 | core | plan D04 T04 §4 |  |
| LP-0043 | Zoom step, zoom calculation, fixed zoom table, centered zoom | -- | -- | IV-0966, IV-0967, IV-0968, IV-0969 | core | plan D04 T04 §4 |  |
| LP-0044 | Follow a watched folder in the viewer: show new images immediately or append, ignore files still being written, sort by name | -- | AC-2001, AC-2002, AC-2003, AC-2004, AC-2005 | -- | core | plan D04 T04 §5 |  |
| LP-0045 | Next, previous, first, last, and random image, skip by N, browse buttons over the image | -- | AC-3996, AC-4609, AC-4610, AC-4611, AC-4612, AC-4695, AC-4696 | IV-0731, IV-0732, IV-0733, IV-0734, IV-0735, IV-0736, IV-0756, IV-1388, IV-1389, IV-1391, IV-1392, IV-1395, IV-1396, IV-1400, IV-1401, IV-1402, IV-1410, IV-1411, IV-1413, IV-1414, IV-1461, IV-1475, IV-1526, IV-1566, IV-1567, IV-1582, IV-1583 | core | plan D04 T04 §5 |  |
| LP-0046 | Dropped files replace or are added to the viewer list | -- | AC-4247, AC-4248 | IV-1558 | core | plan D04 T04 §5 |  |
| LP-0047 | View all images in the folder of the opened file and continue browsing into another folder | -- | AC-4257 | IV-0737 | core | plan D04 T04 §5 |  |
| LP-0048 | Open dialog with format filter, single-click preview, recent folders, and the modern Windows dialog | -- | AC-4432, AC-4560 | IV-0069, IV-0070, IV-0071, IV-0072, IV-0073, IV-1442 | core | plan D04 T04 §5 |  |
| LP-0049 | Reopen and refresh the current file and folder list | -- | AC-4642 | IV-0076, IV-0738, IV-1420, IV-1421, IV-1494 | core | plan D04 T04 §5 |  |
| LP-0050 | Drag files onto the viewer and drag the current file to another program | -- | -- | IV-0049, IV-0050 | core | plan D04 T04 §5 |  |
| LP-0051 | Folder position box: index of total, jump by index or page, filter the folder by pattern | -- | -- | IV-0058, IV-0059, IV-0060, IV-0061 | core | plan D04 T04 §5 |  |
| LP-0052 | Recent files and recently saved files with clearing of the lists | -- | -- | IV-0077, IV-0078, IV-0079 | core | plan D04 T04 §5 |  |
| LP-0053 | Viewer folder sort: name, natural, date, EXIF date, size, extension, direction, none | -- | -- | IV-0623, IV-0624, IV-0625, IV-0626, IV-0627, IV-0628, IV-0629, IV-0630 | core | plan D04 T04 §5 |  |
| LP-0054 | Hot folder: show new images arriving in a watched folder, with subfolders and clear delay | -- | -- | IV-0701, IV-0702, IV-0703 | core | plan D04 T04 §5 |  |
| LP-0055 | Browse only associated, custom, or minimal file types | -- | -- | IV-0945, IV-0946, IV-0947 | core | plan D04 T04 §5 |  |
| LP-0056 | Keep the pointer on browse buttons after the window moves | -- | -- | IV-0960 | core | plan D04 T04 §5 |  |
| LP-0057 | Browsing options: other files in folder, hidden files, folder end dialog, loop, or stop, beep, wheel browsing, always jump on page or wheel | -- | -- | IV-0975, IV-0976, IV-0977, IV-0978, IV-0979, IV-0980, IV-0981, IV-0982 | core | plan D04 T04 §5 |  |
| LP-0058 | Recent files in the menu and recent folders in dialogs | -- | -- | IV-1016, IV-1017 | core | plan D04 T04 §5 |  |
| LP-0059 | Multi-page images: next, previous, first, last, go to page, page thumbnails with auto show, page view pane, page keys | -- | AC-0097, AC-4585, AC-4650, AC-4651, AC-4652, AC-4653, AC-4700, AC-4701 | IV-0760, IV-0761, IV-0762, IV-0763, IV-0764, IV-0765, IV-0766, IV-0769, IV-1393, IV-1394, IV-1412, IV-1415, IV-1425 | core | plan D04 T04 §10 |  |
| LP-0060 | Animated GIF, ANI, APNG, WebP, AVIF, and MNG playback: stop, resume, step frames, speed, option to show the first frame only | -- | AC-4313 | IV-0770, IV-0771, IV-0772, IV-1435, IV-1527, IV-1528 | core | plan D04 T04 §10 | viewing only; extraction is D04 T16 §3 and authoring is Pinxit's D03 T23 §5 |
| LP-0061 | Play pages of a multi-page file as an animation | -- | -- | IV-0767, IV-0768 | core | plan D04 T04 §10 |  |
| LP-0062 | Viewer window layout: image area, bottom toolbar with icon sizes and add or remove buttons, filmstrip of the folder, hide bottom panels | -- | AC-0083, AC-0084, AC-0085, AC-0116, AC-0117, AC-4581, AC-4626, AC-4627, AC-4628 | -- | core | plan D04 T04 §14 |  |
| LP-0063 | Always on top for the viewer window | -- | AC-4249, AC-4314 | -- | core | plan D04 T04 §14 |  |
| LP-0064 | Display resampling quality: smooth fit and zoom, show pixels above 100 percent, sharpen subsampled and resampled display, refresh with resample | -- | AC-4254, AC-4259 | IV-0726, IV-0727, IV-0728, IV-0739 | core | plan D04 T04 §14 |  |
| LP-0065 | Viewer background: default, custom color, tiled image, main window color | -- | AC-4273, AC-4274, AC-4275 | IV-0964 | core | plan D04 T04 §14 |  |
| LP-0066 | Viewer background color and image centering | -- | AC-4319 | IV-0729, IV-1577 | core | plan D04 T04 §14 |  |
| LP-0067 | Minimize boss key and always on top | -- | AC-4556, AC-4916 | IV-0621, IV-0622, IV-1440 | core | plan D04 T04 §14 |  |
| LP-0068 | Viewer chrome: hide menu or caption permanently or per session, toolbar, thin border | -- | AC-4583, AC-4584 | IV-0028, IV-0029, IV-0054, IV-0055, IV-0056, IV-0057, IV-1504, IV-1505, IV-1506, IV-1507, IV-1508 | core | plan D04 T04 §14 |  |
| LP-0069 | Right button: context menu or scroll | -- | -- | IV-0063, IV-0958, IV-1562 | core | plan D04 T04 §14 |  |
| LP-0070 | Fixed grid overlay on the image | -- | -- | IV-0372 | core | plan D04 T04 §14 |  |
| LP-0071 | Clear the display without closing the file list | -- | -- | IV-0394, IV-1432 | core | plan D04 T04 §14 |  |
| LP-0072 | Show one channel (red, green, blue, or alpha) in color or gray | -- | -- | IV-0518, IV-0519 | core | plan D04 T04 §14 |  |
| LP-0073 | Window sizing to the image or to the desktop: fit window to image, fit to desktop, desktop width, height, or smaller side, only big images | -- | -- | IV-0714, IV-0720, IV-0721, IV-0722, IV-0723, IV-0724, IV-1434, IV-1491 | core | plan D04 T04 §14 |  |
| LP-0074 | Transparency display: checkerboard, window color, or discard; non-animated GIF transparency | -- | -- | IV-0938, IV-0952 | core | plan D04 T04 §14 |  |
| LP-0075 | Window placement: center on load, remember size and position | -- | -- | IV-0962, IV-0963 | core | plan D04 T04 §14 |  |
| LP-0076 | Auto Lens: preview photos in the viewer through a chosen filter without applying it, persisting while browsing | -- | AC-1856, AC-1857, AC-1858, AC-1859 | -- | core | plan D04 T04 §15 |  |

## Viewer: fullscreen, slideshow, and information

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0077 | Fullscreen: toggle with F, Enter, or double-click, exit with Esc, context menu with viewer tools, start in fullscreen | -- | AC-0090, AC-0091, AC-0092, AC-0108, AC-1853, AC-4250, AC-4315, AC-4625, AC-4694 | IV-0773, IV-0774, IV-0802, IV-1404, IV-1565 | core | plan D04 T04 §7 |  |
| LP-0078 | Header and footer captions over the image while viewing: text, metadata placeholders, alignment, font, background color, show or hide | -- | AC-1913, AC-1914, AC-1915, AC-1916, AC-1917, AC-1918, AC-1919, AC-1920, AC-1921, AC-4648, AC-4649 | -- | core | plan D04 T04 §18 | never modifies the file; text through the D04 T11 §2 token engine |
| LP-0079 | Hide the mouse cursor in fullscreen, shown briefly on move | -- | AC-4251, AC-4316 | IV-0794, IV-1426, IV-1585 | core | plan D04 T04 §7 |  |
| LP-0080 | Fullscreen display options: original size, fit large only, fit all, stretch, fit width, height, or smaller side, display multiplier, centering, quick keys 1 to 7 | -- | -- | IV-0775, IV-0776, IV-0777, IV-0778, IV-0779, IV-0780, IV-0781, IV-0782, IV-0783, IV-0800, IV-1533, IV-1534, IV-1535, IV-1536, IV-1537, IV-1538, IV-1539, IV-1578 | core | plan D04 T04 §7 |  |
| LP-0081 | Fullscreen resampling on first display and on zoom | -- | -- | IV-0784, IV-0785 | core | plan D04 T04 §7 |  |
| LP-0082 | Fullscreen backdrop: screen color and blurred image sides | -- | -- | IV-0786, IV-0789 | core | plan D04 T04 §7 |  |
| LP-0083 | Transitions and crossfade between images in fullscreen | -- | -- | IV-0787, IV-0788, IV-1579 | core | plan D04 T04 §7 |  |
| LP-0084 | Fullscreen info text with placeholders: font, box color or transparent, position, toggle | -- | -- | IV-0790, IV-0791, IV-0792, IV-0795, IV-1441, IV-1580 | core | plan D04 T04 §18 | placeholders from the D04 T11 §2 token engine |
| LP-0085 | Fullscreen across all monitors | -- | -- | IV-0793, IV-1523 | core | plan D04 T04 §7 |  |
| LP-0086 | Fullscreen mouse: left or right button scrolling for touch screens, left click previous and right click next | -- | -- | IV-0796, IV-0797, IV-0798, IV-1573, IV-1574, IV-1576 | core | plan D04 T04 §7 |  |
| LP-0087 | Unused keys end fullscreen or slideshow, with an option to disable | -- | -- | IV-0801, IV-1591 | core | plan D04 T04 §7 |  |
| LP-0088 | Slideshow menu and slideshows from a selection: play, save, and append to a slideshow list | -- | AC-0051 | IV-0882, IV-0883, IV-0884 | core | plan D04 T04 §8 |  |
| LP-0089 | Image Advance quick slideshow: next, previous, pause, sequence forward, reverse, or random, repeat, delay | -- | AC-1905, AC-1906, AC-1907, AC-1908, AC-1909, AC-1910, AC-1911, AC-4646 | IV-1407, IV-1482, IV-1581 | core | plan D04 T04 §8 |  |
| LP-0090 | Slideshow from the viewer: append or remove the current file, start with the current folder, automatic viewing, last used folder | -- | AC-4647 | IV-0266, IV-0267, IV-0268, IV-0269, IV-0270, IV-1419, IV-1428, IV-1471 | core | plan D04 T04 §8 |  |
| LP-0091 | Slideshow and automatic viewing keep the system awake | -- | -- | IV-0045 | core | plan D04 T04 §8 |  |
| LP-0092 | Open the quick slideshow dialog from the viewer | -- | -- | IV-0088, IV-1448 | core | plan D04 T04 §8 |  |
| LP-0093 | Quick slideshow file list: add, add all, remove, sort by name, date, size, extension, or EXIF date, insert position, start index remembered | -- | -- | IV-0228, IV-0229, IV-0230, IV-0231, IV-0232, IV-0236, IV-0237 | core | plan D04 T04 §8 |  |
| LP-0094 | Per-image duration and caption text in the slideshow list | -- | -- | IV-0233, IV-0234, IV-0235 | core | plan D04 T04 §8 |  |
| LP-0095 | Slideshow playback rules: loop, close after last, skip unreadable files, advance by timer or key, random without repeats with history, pause | -- | -- | IV-0238, IV-0239, IV-0240, IV-0245, IV-0246, IV-0247, IV-0248, IV-0249, IV-0253, IV-0254, IV-1586, IV-1587, IV-1589, IV-1590 | core | plan D04 T04 §8 |  |
| LP-0096 | Background music in the quick slideshow: audio entries in the list, loop MP3 | -- | -- | IV-0241, IV-0242 | core | plan D04 T04 §8 | Windows Media Foundation through Vortice.MediaFoundation (MIT, approved by the operator 2026-09-27; NAudio was not approved) |
| LP-0097 | Slideshow presentation: fullscreen or window with position and size, hide cursor, info text with placeholders | -- | -- | IV-0243, IV-0244, IV-0250, IV-0251, IV-0252 | core | plan D04 T04 §8 | caption placeholders built by D04 T04 §18 |
| LP-0098 | Slideshow list files: persisted list, load and save TXT lists with comments and relative paths | -- | -- | IV-0255, IV-0256, IV-0257, IV-0258, IV-0259 | core | plan D04 T04 §8 |  |
| LP-0099 | During a slideshow: zoom and scroll, delete, copy, and animated images play | -- | -- | IV-0271, IV-0272, IV-0273, IV-0274 | core | plan D04 T04 §8 |  |
| LP-0100 | Slideshow orientation filter: all, landscape only, or portrait only | -- | -- | IV-0803, IV-1588 | core | plan D04 T04 §8 |  |
| LP-0101 | Status bar with image properties, full path in the title, and clickable rating, color label, and tag | -- | AC-0086, AC-4258 | -- | core | plan D04 T04 §9 |  |
| LP-0102 | Properties pane in the viewer to read and edit metadata | -- | AC-0087, AC-1929, AC-4578, AC-4579, AC-4580, AC-4604 | -- | core | plan D04 T04 §9 | edits go to the catalog and sidecar |
| LP-0103 | Histogram in the viewer: channel toggles R, G, B, lightness, display modes with curves, selection histogram, copy averages | -- | AC-0094, AC-1900, AC-1901, AC-1902, AC-1903, AC-1904, AC-4572, AC-4630 | IV-0529, IV-0530, IV-0531, IV-0532, IV-1486 | core | plan D04 T04 §9 |  |
| LP-0104 | Develop settings pane showing the adjustments applied to the image | -- | AC-0099, AC-4465 | -- | core | plan D04 T04 §9 |  |
| LP-0105 | Status bar date choice | -- | AC-4016 | -- | core | plan D04 T04 §9 |  |
| LP-0106 | Status bar and title bar information: size, bit depth, index, zoom, file size, date, tag marker, pixel coordinates and color, selection, full path, custom status text | -- | AC-4554, AC-4920 | IV-0051, IV-0052, IV-0053, IV-0957, IV-0959, IV-0965 | core | plan D04 T04 §9 | info-text placeholders built by D04 T04 §18 |
| LP-0107 | HEX and ASCII byte view of the current file | -- | -- | IV-0083, IV-0747, IV-1418 | core | plan D04 T04 §9 |  |
| LP-0108 | Selection origin, size, and ratio shown in the title | -- | -- | IV-0373 | core | plan D04 T04 §9 |  |
| LP-0109 | Image information dialog: name, folder, compression, original and current size and colors, unique colors, print size, disk and memory size, folder index, date, load time | -- | -- | IV-0447, IV-0448, IV-0449, IV-0451, IV-0452, IV-0453, IV-0454, IV-0455, IV-0456, IV-0457, IV-0458, IV-1437 | core | plan D04 T04 §9 |  |
| LP-0110 | Read QR codes and barcodes | -- | -- | IV-0706 | core | plan D04 T04 §9 | ZXing.Net, Apache-2.0 |
| LP-0111 | Pixel information: coordinates, color, and palette index on click, copy hex color and coordinates | -- | -- | IV-0751, IV-0752, IV-0753, IV-1516, IV-1556, IV-1557 | core | plan D04 T04 §9 |  |
| LP-0112 | OCR of the displayed image through Tesseract or KADMOS | -- | -- | IV-1086, IV-1087, IV-1119 | ai | plan D04 T04 §9 | user-installed Tesseract (Apache-2.0) run as an external process, refused by name when absent; KADMOS is proprietary and not supported |
| LP-0113 | Tools plug-in: additional utility functions | -- | -- | IV-1102 | core | plan D04 T04 §9 |  |
| LP-0114 | Animated image playback on or off and stop animation | -- | AC-4014 | IV-0641, IV-0937 | core | plan D04 T04 §10 |  |
| LP-0115 | Standalone slideshow EXE or screen saver, discs with autorun, and burning slideshows to CD, DVD, or BD | -- | -- | IV-0262, IV-0263, IV-0264, IV-0265, IV-1601, IV-1602, IV-1603, IV-1604, IV-1605 | core | backlog B-049 |  |

## Viewer: quick edits

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0116 | Wallpaper: set centered, tiled, or stretched, stretch to fit option, restore the previous wallpaper | -- | AC-2006, AC-2007, AC-2008, AC-2009, AC-2010, AC-2011, AC-4002, AC-4003, AC-4004, AC-4005, AC-4416, AC-4455, AC-4480, AC-4481, AC-4605, AC-4606, AC-4607, AC-4608 | IV-1518, IV-1519, IV-1520, IV-1521, IV-1522, IV-1524 | core | plan D04 T04 §6 | IDesktopWallpaper; writes a copy under app data |
| LP-0117 | Set as wallpaper: centered, fill, tiled, stretched, proportional, span, monitor choice, previous wallpaper, confirmation, auto stretch | -- | AC-4013 | IV-0611, IV-0612, IV-0613, IV-0614, IV-0615, IV-0616, IV-0617, IV-0618, IV-0619, IV-0620 | core | plan D04 T04 §6 | writes a wallpaper copy in app data, never the original |
| LP-0118 | Save changes: Save becomes Save As a new file, format choice by type or extension, keep the original date and time, recent save folders | -- | AC-4563 | IV-0110, IV-0111, IV-0112, IV-0113, IV-0115, IV-0116, IV-1445, IV-1467 | core | plan D04 T04 §6 | writes a new file, never the original (original-file guard) |
| LP-0119 | Paste options: proportional into selection, original size, pasted image name pattern | -- | -- | IV-0986, IV-0987, IV-0991 | core | plan D04 T04 §6 |  |
| LP-0120 | File handling in the viewer: default copy and move folders, destination dialogs, ask before delete, Recycle Bin, jump or close after delete, keep index after rename | -- | -- | IV-0992, IV-0993, IV-0994, IV-0995, IV-0996, IV-0997, IV-0998, IV-0999, IV-1004 | core | plan D04 T04 §6 |  |
| LP-0121 | Save behavior: Save always shows a dialog, overwrite prompts for Save and Save As | -- | -- | IV-1001, IV-1002 | core | plan D04 T04 §6 | writes a new file, never the original |
| LP-0122 | Rectangle selection in the viewer: drag, resize with ratio lock, move, zoom into, select all, size from the clipboard image | -- | AC-0106, AC-1922, AC-4616, AC-4633, AC-4634 | IV-0374, IV-0375, IV-0376, IV-0377, IV-0378, IV-0396, IV-1390, IV-1397, IV-1398, IV-1399, IV-1450, IV-1541, IV-1544, IV-1545, IV-1547, IV-1548, IV-1549, IV-1550, IV-1551, IV-1552, IV-1553, IV-1554, IV-1555, IV-1559, IV-1560 | core | plan D04 T04 §11 |  |
| LP-0123 | Selection actions: zoom to, copy, save as a new image, print, set as wallpaper | -- | AC-1923, AC-1924, AC-1925, AC-1926, AC-1927, AC-1928 | IV-0117, IV-1472 | core | plan D04 T04 §11 |  |
| LP-0124 | Undo and redo in the viewer with a configurable number of steps | -- | -- | IV-0355, IV-0356, IV-0357, IV-1459, IV-1474 | core | plan D04 T04 §11 |  |
| LP-0125 | Custom and maximized selections: exact position, size, and ratio with saved presets, maximize for popular ratios, center, restore last selection | -- | -- | IV-0359, IV-0360, IV-0361, IV-0362, IV-0363, IV-0364, IV-1483, IV-1530, IV-1542, IV-1543 | core | plan D04 T04 §11 |  |
| LP-0126 | Selection shapes and grids: rectangle, ellipse, freehand, inverted selection, golden ratio, thirds, and fourths grids | -- | -- | IV-0365, IV-0366, IV-0367, IV-0368, IV-0369, IV-0370, IV-0371 | core | plan D04 T04 §11 |  |
| LP-0127 | Crop to selection, crop to visible window area, auto crop uniform borders with a preview selection, cut and cut outside with a fill color, remove or insert strips | -- | -- | IV-0381, IV-0382, IV-0383, IV-0384, IV-0385, IV-0386, IV-0387, IV-1473, IV-1525 | core | plan D04 T04 §11 |  |
| LP-0128 | Resolution: change DPI, auto adjust DPI on resize, resize by DPI | -- | -- | IV-0450, IV-0496, IV-0497 | core | plan D04 T04 §11 |  |
| LP-0129 | Fine rotation and straighten: any angle, fill color, keep size or best inner rectangle, draw a line for the angle, on a selection, fine-step keys | -- | -- | IV-0470, IV-0471, IV-0472, IV-0473, IV-0474, IV-0475, IV-0476, IV-0477, IV-1469, IV-1529 | core | plan D04 T04 §11 |  |
| LP-0130 | Resize and resample: pixels, cm, inches, percent, megapixels, standard sizes, keep aspect ratio, saved custom sizes | -- | -- | IV-0480, IV-0481, IV-0482, IV-0483, IV-0484, IV-0498, IV-1466 | core | plan D04 T04 §11 | consumes D01 T03 §2 |
| LP-0131 | Resampling filters: fast resize or resample with Lanczos, Mitchell, B-spline, Bell, triangle, Hermite, Catmull-Rom, box, shrink filter, gamma-correct resampling | -- | -- | IV-0485, IV-0486, IV-0487, IV-0488, IV-0489, IV-0490, IV-0491, IV-0492, IV-0493, IV-0494, IV-0495 | core | plan D04 T04 §11 | consumes D01 T03 §2 |
| LP-0132 | Canvas size: per-side sizes including negative crop, new size with anchor, extend to an aspect ratio, color, saved settings | -- | -- | IV-0499, IV-0500, IV-0501, IV-0502, IV-0503, IV-0504, IV-1498 | core | plan D04 T04 §11 |  |
| LP-0133 | Auto adjust colors (brightness and gamma), optionally from the selection statistics | -- | -- | IV-0537, IV-1497 | core | plan D04 T04 §11 |  |
| LP-0134 | Selection and editing options: selection and grid color, border thickness, grid size, auto crop tolerance, cut background color | -- | -- | IV-0983, IV-0985, IV-0988, IV-0989, IV-0990 | core | plan D04 T04 §11 |  |
| LP-0135 | Decrease color depth: 2, 16, 256, or custom colors, black and white and gray palettes, best quality quantizer, dithering, RGB565 | -- | AC-2022, AC-2023, AC-2024, AC-2025, AC-2026, AC-2027, AC-2028, AC-2032, AC-4672, AC-4673, AC-4674, AC-4675, AC-4676 | IV-0513, IV-0514, IV-0515, IV-0516 | core | plan D04 T04 §12 | consumes D01 T03 §3 |
| LP-0136 | Increase color depth to truecolor, 16-bit gray, 48-bit color, or 32 bits with alpha | -- | AC-2029, AC-2030, AC-2031, AC-4677, AC-4678, AC-4679, AC-4680 | IV-0511, IV-0512 | core | plan D04 T04 §12 |  |
| LP-0137 | Convert to grayscale and negative of all or one channel | -- | -- | IV-0517, IV-0520, IV-1456, IV-1513 | core | plan D04 T04 §12 |  |
| LP-0138 | Color corrections: brightness, contrast, gamma, saturation, RGB balance, white balance by clicking a bright area, preview on the image | -- | -- | IV-0521, IV-0522, IV-0523, IV-1485 | core | plan D04 T04 §12 |  |
| LP-0139 | Color correction profiles, saved values, and a dark dialog option | -- | -- | IV-0524, IV-0525, IV-0526 | core | plan D04 T04 §12 |  |
| LP-0140 | Set a transparent color and alpha intensity with tolerance | -- | -- | IV-0527, IV-0528 | core | plan D04 T04 §12 |  |
| LP-0141 | Replace color: tolerance, make transparent, pick the source color from the image | -- | -- | IV-0533, IV-0534, IV-0535, IV-0536 | core | plan D04 T04 §12 |  |
| LP-0142 | Sharpen with a set amount | -- | -- | IV-0538, IV-1495 | core | plan D04 T04 §12 |  |
| LP-0143 | Red eye reduction with gray intensity, and green and yellow pet eye variants | -- | -- | IV-0539, IV-0540, IV-0541, IV-1501 | core | plan D04 T04 §12 |  |
| LP-0144 | Swap color channels: RBG, BGR, BRG, GRB, GBR | -- | -- | IV-0542, IV-0543, IV-0544, IV-0545, IV-0546 | core | plan D04 T04 §12 |  |
| LP-0145 | Palette editing: edit indexed colors, export and import PAL palettes | -- | -- | IV-0547, IV-0548, IV-0549 | core | plan D04 T04 §12 |  |
| LP-0146 | Palette import maps to nearest color | -- | -- | IV-0984 | core | plan D04 T04 §12 |  |
| LP-0147 | Insert text: at a click or in a selection, multi-line with placeholders and tabs, font, size, style, color, alignment, rotation, antialiasing, transparent or colored box | -- | -- | IV-0379, IV-0397, IV-0398, IV-0400, IV-0401, IV-0403, IV-0404, IV-1468 | core | plan D04 T04 §13 | placeholders from D04 T11 §2 |
| LP-0148 | Image watermark overlay: corner and offset or center, click to place with preview, transparency, keeps PNG and GIF transparency, from the selection | -- | -- | IV-0380, IV-0412, IV-0413, IV-0414, IV-0415, IV-0417, IV-0418 | core | plan D04 T04 §13 | engine D04 T11 §8 |
| LP-0149 | Paste into the image or selection, movable and resizable before applying, keep selection | -- | -- | IV-0389, IV-0390, IV-0391, IV-1470, IV-1502, IV-1546 | core | plan D04 T04 §13 |  |
| LP-0150 | Paste special on a side for simple collages, with a paste counter for names | -- | -- | IV-0392, IV-0393 | core | plan D04 T04 §13 |  |
| LP-0151 | Insert text extras: adjust font to zoom, add canvas above or below for the text, shadow and outline effects, preview, profiles, Ctrl-click stamping, pick color from image | -- | -- | IV-0399, IV-0402, IV-0405, IV-0408, IV-0409, IV-0410, IV-0411 | core | plan D04 T04 §13 |  |
| LP-0152 | Color highlight overlay on an area | -- | -- | IV-0416 | core | plan D04 T04 §13 |  |
| LP-0153 | Combine images side by side (panorama image): horizontal or vertical, spacing, file names, and tiled images | -- | -- | IV-0463, IV-0464, IV-0465, IV-0466, IV-0467 | core | plan D04 T04 §13 |  |
| LP-0154 | Borders and frames: up to four parts, presets, inside fading, broken edge and lines, on a selection | -- | -- | IV-0505, IV-0506, IV-0507, IV-0508, IV-0509, IV-0510, IV-1453 | core | plan D04 T04 §13 |  |
| LP-0155 | Speech bubbles | -- | -- | IV-0594 | core | plan D04 T04 §13 |  |
| LP-0156 | Shapes and shadows: drop shadow, rounded corners, snowflake, hexagon, star, heart, cloud, and other shaped crops | -- | -- | IV-0595, IV-0596, IV-0597 | core | plan D04 T04 §13 |  |
| LP-0157 | Export image tiles: count or size, spacing, all pages, format and folder | -- | -- | IV-0709, IV-0710, IV-0711, IV-0712, IV-0713 | core | plan D04 T04 §13 | writes new files |
| LP-0158 | Combine selected images side by side into one image | -- | -- | IV-0905 | core | plan D04 T04 §13 |  |
| LP-0159 | Effects browser: resizable dialog with preview and a value per effect, applied to the selection or the whole image | -- | -- | IV-0550, IV-0551, IV-0552, IV-1454 | core | plan D04 T04 §15 | consumes the D01 T03 effect registry |
| LP-0160 | Blur effects: blur, Gaussian, fast Gaussian, total variation, radial, zoom, motion, tilt-shift | -- | -- | IV-0553, IV-0554, IV-0555, IV-0556, IV-0578, IV-0579, IV-0580, IV-0592 | core | plan D04 T04 §15 | consumes D01 T03 §6 |
| LP-0161 | Sharpen effects: sharpen and unsharp mask | -- | -- | IV-0557, IV-0558 | core | plan D04 T04 §15 | consumes D01 T03 §6 |
| LP-0162 | Stylize effects: 3D button, emboss, oil paint, edge detection, find edges, explosion, pixelize, fragment, solarize, metallic gold and ice, rock, stained glass, blinds | -- | -- | IV-0559, IV-0560, IV-0561, IV-0562, IV-0564, IV-0565, IV-0568, IV-0569, IV-0575, IV-0576, IV-0577, IV-0581, IV-0582, IV-0590, IV-0591 | core | plan D04 T04 §15 | consumes D01 T03 effects |
| LP-0163 | Tone and noise effects: median, add noise, sepia, color temperature, histogram equalize and stretch, chromatic aberration, radial brighten | -- | -- | IV-0563, IV-0566, IV-0583, IV-0584, IV-0585, IV-0588, IV-0589 | core | plan D04 T04 §15 | consumes D01 T03 effects |
| LP-0164 | Distort effects: rain drops, swirl, twirl, fish eye, cylinder, circular waves, horizontal and vertical shift, skew | -- | -- | IV-0567, IV-0570, IV-0571, IV-0572, IV-0573, IV-0574, IV-0586, IV-0587, IV-0593 | core | plan D04 T04 §15 | consumes D01 T03 §7 |
| LP-0165 | Local contrast enhancement (AltaLux-style) | -- | -- | IV-0598 | core | plan D04 T04 §15 | own implementation, not the plug-in |
| LP-0166 | Film simulation from CLUT files | -- | -- | IV-0600 | core | plan D04 T04 §15 | LUT stage from D01 T07 §9 |
| LP-0167 | Curves in quick edits (SmartCurve) | -- | -- | IV-0609 | core | plan D04 T04 §15 |  |
| LP-0168 | Effects plug-in and film simulation looks with CLUT packs | -- | -- | IV-1055, IV-1059, IV-1114 | core | plan D04 T04 §15 | effects from the Isotone.Core registry; Hald CLUT looks through the D01 T07 §9 LUT stage |
| LP-0169 | Rotate left and right and flip horizontally or vertically: orientation stored as metadata, lossless JPEG transforms written to a new file, flip on a selection | -- | AC-0102, AC-0103, AC-1897, AC-1898, AC-1899, AC-4654, AC-4655 | IV-0468, IV-0469, IV-0478, IV-0479, IV-1436, IV-1439, IV-1444, IV-1447, IV-1515, IV-1517 | core | plan D04 T04 §16 | writes a new file, never the original (original-file guard) |
| LP-0170 | Rotate left and right 90 degrees from the toolbar in browse and viewer: orientation stored as metadata, lossless JPEG rotation to a new file | -- | AC-0652, AC-0653, AC-0654 | -- | core | plan D04 T04 §16 | writes a new file or orientation metadata, never the original (original-file guard) |
| LP-0171 | Lossless JPEG transforms: flip, rotate 90, 180, 270, auto rotate by EXIF, orientation reset, edge trimming or perfect transform, hotkeys | -- | -- | IV-0648, IV-0649, IV-0650, IV-0651, IV-0652, IV-0653, IV-0654, IV-0655, IV-0664, IV-0668, IV-0669, IV-0670, IV-0671, IV-0672 | core | plan D04 T04 §16 | writes a new file, never the original |
| LP-0172 | Lossless JPEG options: optimize, progressive, JFIF marker, keep, clean, or choose markers, update EXIF thumbnail, DPI, ICC profile, file date from EXIF or kept | -- | -- | IV-0656, IV-0657, IV-0658, IV-0659, IV-0660, IV-0661, IV-0662, IV-0663, IV-0665, IV-0666, IV-0667, IV-1487 | core | plan D04 T04 §16 | applied to the new file |
| LP-0173 | Lossless JPEG crop to the selection: MCU alignment, output file, EXIF thumbnail | -- | -- | IV-0673, IV-0674, IV-0675, IV-0676, IV-1511 | core | plan D04 T04 §16 | writes a new file, never the original |
| LP-0174 | Lossless JPEG transforms: rotate, crop, clean metadata, EXIF date edit, EXIF thumbnail update | -- | -- | IV-1077 | core | plan D04 T04 §16 | writes a new file, never the original (original-file guard) |

## Browsing and file management

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0175 | Delete from the viewer to the Recycle Bin, optionally with sidecars, permanent delete behind confirmation, return to browse after delete or move | -- | AC-3999, AC-4256, AC-4450, AC-4591 | IV-0108, IV-0109, IV-1408, IV-1409 | core | plan D04 T04 §6 |  |
| LP-0176 | Copy the image or its file name to the clipboard, clear the clipboard | -- | AC-4586, AC-4587, AC-4588 | IV-0388, IV-0395, IV-0754, IV-1452, IV-1477, IV-1492 | core | plan D04 T04 §6 |  |
| LP-0177 | Copy or move the current file to a folder: destination slots, relative paths, shortcut-only copy, duplicate on name clash, replace dialog with previews | -- | AC-4589, AC-4590 | IV-0101, IV-0102, IV-0103, IV-0104, IV-0105, IV-0106, IV-0107, IV-1422, IV-1423, IV-1584 | core | plan D04 T04 §6 |  |
| LP-0178 | Rename the current file, also renaming sidecars with the same base name, retry on failure | -- | AC-4592 | IV-0098, IV-0099, IV-0100, IV-1417 | core | plan D04 T04 §6 |  |
| LP-0179 | Manage-mode browse window: file list pane, contents bar, status bar, task pane, maximized and full-screen file list | -- | AC-0028, AC-0030, AC-0039, AC-0301, AC-0406, AC-0407, AC-0444, AC-0445, AC-4414, AC-4441, AC-4473 | -- | core | plan D04 T05 §1 |  |
| LP-0180 | Browsed folders enter the catalog automatically as browsed images, no import step | -- | AC-0457 | -- | core | plan D04 T05 §1 |  |
| LP-0181 | Catalog records built automatically while browsing, with per-file fields | -- | AC-1725, AC-1726 | -- | core | plan D04 T05 §1 |  |
| LP-0182 | Thumbnails window hand-off: double-click opens the viewer, Tab switches between browser and viewer, Esc hides the viewer | -- | AC-4383, AC-4518, AC-4555, AC-4692 | IV-0835, IV-0836, IV-0925, IV-0926, IV-1405, IV-1406, IV-1446 | core | plan D04 T05 §1 |  |
| LP-0183 | High-quality and develop-aware thumbnails generated in the background to replace embedded ones | -- | AC-0519, AC-0520, AC-0521, AC-4105 | -- | core | plan D04 T05 §2 | extends D04 T01 §7 |
| LP-0184 | Excluded folders from the catalog, with reset to defaults | -- | AC-1728, AC-1729, AC-4215 | -- | core | plan D04 T05 §2 |  |
| LP-0185 | Background indexer for chosen folders while idle and while Albumen is closed | -- | AC-1730 | -- | automation | plan D04 T05 §2 |  |
| LP-0186 | Catalog files dialog: add folders without browsing, file kinds, thumbnails, archive contents, RAW previews | -- | AC-1794, AC-1795, AC-1801, AC-1802, AC-1803, AC-1804, AC-1805, AC-1806 | -- | core | plan D04 T05 §2 |  |
| LP-0187 | Background indexer: index when idle, image files only or all types, target catalog, folders to monitor | -- | AC-4321, AC-4322, AC-4323, AC-4324 | -- | core | plan D04 T05 §2 |  |
| LP-0188 | Toolbar navigation: home folder, back, and forward | -- | AC-0029, AC-4492, AC-4493 | -- | core | plan D04 T05 §3 |  |
| LP-0189 | Folders pane: directory tree with drives, removable devices, common shell folders, new, delete, and rename folder | -- | AC-0031, AC-0455, AC-0458, AC-0460, AC-0461, AC-0462, AC-4418, AC-4431, AC-4458 | IV-0837, IV-0838 | core | plan D04 T05 §3 |  |
| LP-0190 | Shortcuts and favorites pane: shortcuts to files, folders, and programs, folders of shortcuts, drag to create, run, rename, delete | -- | AC-0033, AC-0511, AC-0512, AC-0513, AC-0514, AC-0515, AC-0516, AC-0517, AC-4595 | IV-0845 | core | plan D04 T05 §3 |  |
| LP-0191 | Home page: quick search bar, recently modified and recently added searches with time windows and date basis, tagged and unnamed-face searches | -- | AC-0303, AC-0304, AC-0305, AC-0306, AC-0307, AC-0308, AC-0309, AC-0310, AC-0311, AC-0312, AC-0313, AC-0315, AC-4068, AC-4069, AC-4070, AC-4071 | -- | core | plan D04 T05 §3 |  |
| LP-0192 | Home page action buttons: import, database backup and maintenance, catalog files | -- | AC-0317, AC-0318, AC-0320 | -- | core | plan D04 T05 §3 |  |
| LP-0193 | Multi-folder and recursive browsing: Easy-Select bars, Ctrl-click with subfolders, load all subfolders, tree context menu | -- | AC-0459, AC-4168, AC-4169 | IV-0840, IV-0841, IV-0878, IV-1451, IV-1572 | core | plan D04 T05 §3 |  |
| LP-0194 | Browsing tabs: new, open in new tab, middle-click, duplicate, close, close others, left, right, next and previous tab | -- | AC-0463, AC-0468, AC-0469, AC-0470, AC-0471, AC-0472, AC-0473, AC-0474, AC-0475, AC-0476, AC-0477, AC-0478, AC-0479, AC-0480, AC-4385, AC-4386, AC-4387, AC-4388, AC-4389 | -- | core | plan D04 T05 §3 |  |
| LP-0195 | Startup location: home page, start folder, reopen last or all tabs | -- | AC-0464, AC-0465, AC-0466, AC-0467, AC-4055, AC-4056, AC-4057, AC-4058, AC-4059 | -- | core | plan D04 T05 §3 |  |
| LP-0196 | Per-tab state: panes, filters, groups, and searches per tab, drag files between tabs, last tab restored | -- | AC-0481, AC-0482, AC-0483, AC-0484 | -- | core | plan D04 T05 §3 |  |
| LP-0197 | Address box with typed or pasted paths, recent folders list with count and clear, focus options | -- | -- | IV-0842, IV-0843, IV-0844, IV-0861 | core | plan D04 T05 §3 |  |
| LP-0198 | Preview pane: image, information, histogram, delay, size, progressive instant preview, chosen fields | -- | AC-0036, AC-0631, AC-0632, AC-0633, AC-0634, AC-0635, AC-4159, AC-4160, AC-4163, AC-4164, AC-4165, AC-4166, AC-4167, AC-4495 | -- | core | plan D04 T05 §4 |  |
| LP-0199 | File list views: thumbnails, tiles, thumbs plus details, filmstrip, icons, list, details | -- | AC-0411, AC-0419, AC-0420, AC-0567, AC-0568, AC-0569, AC-0570, AC-0571, AC-0572, AC-0573, AC-4442, AC-4443, AC-4444, AC-4445, AC-4446, AC-4447, AC-4448 | IV-0846, IV-0847, IV-0848, IV-0849 | core | plan D04 T05 §4 | extends D04 T01 §8 |
| LP-0200 | Thumbnail size and cell shape: zoom slider, size presets, portrait, landscape, or custom ratio, spacing | -- | AC-0418, AC-4149, AC-4150, AC-4151, AC-4152, AC-4524, AC-4525 | IV-0857 | core | plan D04 T05 §4 | extends D04 T01 §8 |
| LP-0201 | Thumbnail overlay icons: rating, label, format, category, collection, stack, shortcut, offline, excluded, tagged, rejected, geotagged, auto-rotated, developed, edited, snapshots | -- | AC-0422, AC-0423, AC-0425, AC-0426, AC-0427, AC-0428, AC-0429, AC-0430, AC-0434, AC-0435, AC-0436, AC-0437, AC-0438, AC-0439, AC-0440, AC-0441 | -- | core | plan D04 T05 §4 | extends D04 T01 §8 badges |
| LP-0202 | Overlay display options: overlay modes, color highlight cycling, per-overlay toggles, empty overlays on hover, stack bars | -- | AC-0442, AC-0443, AC-0574, AC-4128, AC-4129, AC-4130, AC-4132, AC-4133, AC-4134, AC-4135, AC-4136, AC-4137, AC-4138, AC-4139, AC-4140, AC-4141, AC-4142, AC-4143, AC-4144 | -- | core | plan D04 T05 §4 |  |
| LP-0203 | Details view columns: choose, add, remove, reorder, reset, grid lines, full row select, auto width, highlight and click-to-sort columns | -- | AC-0575, AC-0576, AC-0577, AC-0578, AC-0579, AC-0580, AC-0581, AC-0582, AC-0583, AC-4154, AC-4155, AC-4156, AC-4157, AC-4158 | -- | core | plan D04 T05 §4 |  |
| LP-0204 | File types shown: images, PDF, folders, archives, Office documents, hidden files, THM and XMP files | -- | AC-0586, AC-0588, AC-0589, AC-0590, AC-0591, AC-0592, AC-0593, AC-0594, AC-4110, AC-4111, AC-4112, AC-4113, AC-4114, AC-4399 | -- | core | plan D04 T05 §4 |  |
| LP-0205 | Thumbnail style: drop shadow, slide background, folder style, borders, colors, high-quality scaling, folder content thumbnails | -- | AC-4106, AC-4145, AC-4146, AC-4147, AC-4148, AC-4153 | IV-0856, IV-0858, IV-0859 | core | plan D04 T05 §4 |  |
| LP-0206 | Hover pop-ups: on hover or with Shift, auto hide, thumbnail and chosen information | -- | AC-4118, AC-4119, AC-4120, AC-4121, AC-4122, AC-4123 | IV-0862 | core | plan D04 T05 §4 |  |
| LP-0207 | Thumbnail and tile info fields: file name, chosen metadata on thumbnails and tiles | -- | AC-4125, AC-4126, AC-4127 | IV-0850 | core | plan D04 T05 §4 |  |
| LP-0208 | Refresh thumbnails and remove items from the list without deleting | -- | AC-4438, AC-4451 | IV-0851, IV-0852, IV-0853 | core | plan D04 T05 §4 |  |
| LP-0209 | Filter by rating, category, label, and advanced filters in the file list | -- | AC-0408, AC-0584, AC-0585 | -- | core | plan D04 T05 §5 |  |
| LP-0210 | Group by attribute or processed state: collapsible groups, hover preview, table of contents, group order, select group by header | -- | AC-0409, AC-0509, AC-0510, AC-0595, AC-0596, AC-0601, AC-0602, AC-0603, AC-0604, AC-0605, AC-0606, AC-0607, AC-0608 | -- | core | plan D04 T05 §5 |  |
| LP-0211 | Sort by name (natural), size, type, dates, EXIF date, dimensions, DPI, megapixels, orientation, caption, rating, tag, any metadata field, direction, full path | -- | AC-0410, AC-0609, AC-0610, AC-0611, AC-0612, AC-0613, AC-0614, AC-0615, AC-0616, AC-0617, AC-0618, AC-0619 | IV-0863, IV-0867, IV-0868, IV-0869, IV-0870, IV-0871, IV-0872, IV-0873, IV-0874, IV-0875 | core | plan D04 T05 §5 | extends D04 T01 §8 |
| LP-0212 | Selection commands: click, Ctrl, Shift, select all, all files, all images, tagged, by rating, clear, invert, auto-select new files | -- | AC-0412, AC-0622, AC-0623, AC-0624, AC-0625, AC-0626, AC-0627, AC-0628, AC-0629, AC-0630, AC-4102, AC-4419, AC-4427, AC-4468, AC-4471, AC-4474, AC-4520, AC-4521, AC-4522 | IV-0854 | core | plan D04 T05 §5 |  |
| LP-0213 | Per-folder sort memory and custom drag order saved per folder | -- | AC-0620, AC-0621, AC-4107 | IV-0876 | core | plan D04 T05 §5 |  |
| LP-0214 | Copy selected files to a folder | -- | AC-0399 | -- | core | plan D04 T05 §6 |  |
| LP-0215 | Delete to Recycle Bin with confirmation settings | -- | AC-0453, AC-4193, AC-4200, AC-4384, AC-4934 | IV-0881 | core | plan D04 T05 §6 |  |
| LP-0216 | Rename a file or folder inline, including click to edit the name | -- | AC-0454, AC-0995, AC-4199, AC-4415 | -- | core | plan D04 T05 §6 | batch rename is D04 T11 §3 |
| LP-0217 | Copy to and move to folder: folder tree, recent folders, create folder, drag onto tree folders | -- | AC-0973, AC-0974, AC-0977, AC-0978, AC-0979, AC-4394, AC-4401 | IV-0839, IV-0879, IV-0880 | core | plan D04 T05 §6 |  |
| LP-0218 | Sidecars, related files, and catalog records travel with copied and moved files | -- | AC-0975, AC-4201 | -- | core | plan D04 T05 §6 |  |
| LP-0219 | Name collision policy: ask, rename with separator, replace, skip | -- | AC-0980, AC-0981, AC-0982, AC-0983, AC-4194, AC-4195, AC-4196, AC-4197 | -- | core | plan D04 T05 §6 |  |
| LP-0220 | Copy image pixels or the file path to the clipboard | -- | AC-0984, AC-0985, AC-4470 | -- | core | plan D04 T05 §6 |  |
| LP-0221 | File clipboard and drag and drop: cut, copy, paste files keeping catalog data, drag to other programs, confirm drag moves | -- | AC-0986, AC-4171, AC-4434, AC-4435, AC-4436 | IV-0924 | core | plan D04 T05 §6 |  |
| LP-0222 | Confirm file replace dialog: both thumbnails, replace, rename to, skip, delete source or destination, apply to all, cancel | -- | AC-0987, AC-0988, AC-0989, AC-0990, AC-0991, AC-0992, AC-0993, AC-0994 | -- | core | plan D04 T05 §6 |  |
| LP-0223 | Keeping catalog links when files move or are renamed | -- | AC-1727 | -- | core | plan D04 T05 §6 | moves inside Albumen keep records; outside moves reconnect through D04 T06 §8 |
| LP-0224 | Windows Explorer context menu in the file list | -- | AC-4124, AC-4457, AC-4523, AC-4613, AC-4697 | -- | core | plan D04 T05 §6 |  |
| LP-0225 | Sidecar files deleted, copied, and moved with the photo | -- | -- | IV-1000 | core | plan D04 T05 §6 |  |
| LP-0226 | Compare images viewer: up to four images, comparison list, send to view, drag in, swap next or previous, remove, layouts | -- | AC-0416, AC-0655, AC-0656, AC-0657, AC-0658, AC-0659, AC-0676, AC-0677, AC-4454 | -- | core | plan D04 T05 §7 | extends D04 T01 §9 |
| LP-0227 | Information palette: camera, lens, dimensions, size, exposure program, white balance, metering, flash, RAW, ISO, aperture, shutter, compensation, focal length, chosen bottom line | -- | AC-0637, AC-0638, AC-0639, AC-0640, AC-0641, AC-0642, AC-0643, AC-0644, AC-0645, AC-0646, AC-0647, AC-0648, AC-0649, AC-0650, AC-0651, AC-4582, AC-4968 | -- | core | plan D04 T05 §7 |  |
| LP-0228 | Culling and file actions in compare: tag, tag all, rate, categories, save as a new file, delete | -- | AC-0660, AC-0661, AC-0662, AC-0663, AC-0678, AC-0679 | -- | core | plan D04 T05 §7 | Save As writes a new file, never the original |
| LP-0229 | Compare zoom and pan: actual size, fit, fit width and height, zoom to, zoom lock, pan lock | -- | AC-0664, AC-0665, AC-0666, AC-0667, AC-0668, AC-0669, AC-0670, AC-0671 | -- | core | plan D04 T05 §7 |  |
| LP-0230 | Compare analysis: exposure warning, property differences in bold, histograms, metadata setup | -- | AC-0672, AC-0673, AC-0674, AC-0675 | -- | core | plan D04 T05 §7 |  |
| LP-0231 | Compare the current image with another: synced zoom and scroll, next and previous, difference image | -- | -- | IV-0118, IV-0119, IV-0120, IV-0121 | core | plan D04 T05 §7 |  |
| LP-0232 | Selective browsing: combine folder, catalog, and date criteria, include toggles, match any or all, remove and clear, auto hide | -- | AC-0037, AC-1119, AC-1120, AC-1121, AC-1122, AC-1123, AC-1124, AC-1125, AC-1126, AC-1127, AC-1128, AC-1129, AC-4475 | -- | core | plan D04 T05 §8 |  |
| LP-0233 | Image basket: up to five baskets, add from browse, viewer, or Explorer, active basket, remove, clear, rename, delete | -- | AC-0042, AC-0413, AC-0680, AC-0681, AC-0682, AC-0683, AC-0684, AC-0685, AC-0686, AC-4417, AC-4420, AC-4462, AC-4466, AC-4467, AC-4593, AC-4594, AC-4935, AC-4936 | -- | core | plan D04 T05 §8 |  |
| LP-0234 | Add the viewed image to the image basket | -- | AC-0101 | -- | core | plan D04 T05 §8 |  |
| LP-0235 | Load and save file lists as text files | -- | -- | IV-0877, IV-0888 | core | plan D04 T05 §8 |  |
| LP-0236 | Private folder: password-protected vault, create, open, close, hidden when closed, no password recovery | -- | AC-0996, AC-0998, AC-0999, AC-1000, AC-1001, AC-1002 | -- | core | plan D04 T05 §9 | encrypted at rest, own code on .NET AES-GCM and PBKDF2 |
| LP-0237 | Private folder contents: add files with warning, restore to a normal folder, delete, catalog data removed on add | -- | AC-0997, AC-1003, AC-1004, AC-1005 | -- | core | plan D04 T05 §9 |  |
| LP-0238 | Calendar pane: events, year, month, day views, photo calendar with hover previews, table of contents, skip empty dates, floating pane | -- | AC-0032, AC-0492, AC-0493, AC-0494, AC-0495, AC-0496, AC-0497, AC-0503, AC-0504, AC-0508, AC-4461, AC-4526, AC-4527, AC-4528, AC-4529, AC-4530, AC-4531, AC-4532, AC-4533, AC-4534 | -- | core | plan D04 T05 §10 |  |
| LP-0239 | Calendar date basis: catalog date, date taken, modified, created, loaded | -- | AC-0498, AC-0499, AC-0500, AC-0501, AC-4180, AC-4181, AC-4182, AC-4183 | -- | core | plan D04 T05 §10 |  |
| LP-0240 | Calendar options: filters, images and media only, start of week, 12 or 24 hour clock | -- | AC-0502, AC-4184, AC-4185, AC-4186, AC-4187 | -- | core | plan D04 T05 §10 |  |
| LP-0241 | Calendar events: description and chosen thumbnail per date, restore default thumbnail | -- | AC-0505, AC-0506, AC-0507 | -- | core | plan D04 T05 §10 |  |
| LP-0242 | Duplicates view: content-identical duplicates grouped as stacks with status, set as original, remove, hide and show hidden | LR-0198, LR-0199, LR-0200, LR-0201, LR-0202, LR-0203, LR-0204, LR-0205, LR-0206, LR-0207, LR-1433 | -- | -- | core | plan D04 T05 §11 | duplicates are content based, not name based |
| LP-0243 | Detect duplicates automatically for all photos (catalog setting) | LR-1317 | -- | -- | core | plan D04 T05 §11 |  |
| LP-0244 | Duplicate finder setup: one list or two lists, add files and folders, subfolders, exact content or same name, images only | -- | AC-0319, AC-1138, AC-1139, AC-1140, AC-1141, AC-1142, AC-1143, AC-1144, AC-1145, AC-1146, AC-1147 | -- | core | plan D04 T05 §11 | visually similar photos are D04 T10 §5 |
| LP-0245 | Duplicate finder review: sort sets, preview, mark for deletion, delete from list 1 or 2, rename, review and finish | -- | AC-1148, AC-1149, AC-1150, AC-1151, AC-1152, AC-1153 | -- | core | plan D04 T05 §11 | deletion goes to the Recycle Bin |
| LP-0246 | Folder sync to a backup location: wizard, source, destination, error and log options, conflicts, name, schedule, edit, run saved syncs | -- | AC-1029, AC-1030, AC-1031, AC-1032, AC-1033, AC-1034, AC-1035, AC-1036, AC-1037 | -- | automation | plan D04 T05 §12 | mirror to a local, network, or external drive |
| LP-0247 | Create archive: format and settings, subfolders, hidden files, password, output file, add to or overwrite existing | -- | AC-1316, AC-1317, AC-1318, AC-1319, AC-1320, AC-1322, AC-1323, AC-1324, AC-1325 | -- | core | plan D04 T05 §12 | SharpCompress (MIT) |
| LP-0248 | Remove source files after a verified archive | -- | AC-1321 | -- | core | plan D04 T05 §12 | moves originals to the Recycle Bin after verification, never an unverified delete |
| LP-0249 | Extract archive to folder with create folder and collision policy | -- | AC-1326, AC-1327, AC-1328, AC-1329, AC-1330, AC-1331 | -- | core | plan D04 T05 §12 |  |
| LP-0250 | Browse inside archives, list archives in the folder tree, group archives with folders | -- | AC-1332, AC-4103, AC-4170 | -- | core | plan D04 T05 §12 |  |
| LP-0251 | Embedded RAW thumbnails shown first and cached in the catalog | -- | AC-0518, AC-0522, AC-4104 | IV-0864 | core | shipped-scope D04 T01 §7 |  |

## Library views and culling

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0252 | Viewer navigation keys Home, End, Page Up, Page Down | -- | AC-0913, AC-0914 | -- | core | plan D04 T04 §5 |  |
| LP-0253 | Rotate and flip photos from the library, non-destructively | LR-0219, LR-0220, LR-1449, LR-1450, LR-1666, LR-1667 | -- | -- | core | plan D04 T04 §11 | orientation stored as metadata, never written into the original (original-file guard) |
| LP-0254 | Filmstrip options: source indicator and recent sources, quick filter, ratings, badges, stack counts, tooltips, navigator hover, unsynced badge | LR-0015, LR-0054, LR-0055, LR-0056, LR-0057, LR-0058, LR-0059, LR-0060, LR-0061, LR-1351 | -- | -- | core | plan D04 T06 §1 | extends D04 T01 §9 filmstrip |
| LP-0255 | Secondary display window: grid, loupe normal, live, or locked, compare, survey, slideshow, preview control, own filter bar, monitor choice, ACDSee second monitor image and file list | LR-0025, LR-0026, LR-0027, LR-0028, LR-0029, LR-1346, LR-1441, LR-1506, LR-1615, LR-1616, LR-1617, LR-1618, LR-1619, LR-1620, LR-1621, LR-1622, LR-1623, LR-1624 | AC-4333, AC-4334, AC-4335, AC-4643, AC-4644, AC-4971, AC-4972 | -- | core | plan D04 T06 §1 |  |
| LP-0256 | Loupe info overlays cycled with I | LR-0038 | -- | -- | core | plan D04 T06 §1 |  |
| LP-0257 | Compare view swap and make select | LR-0194, LR-1659, LR-1660 | -- | -- | core | plan D04 T06 §1 | extends D04 T01 §9 |
| LP-0258 | Survey view: several selected photos together, remove from survey without deselecting | LR-0195, LR-0196, LR-1599 | -- | -- | core | plan D04 T06 §1 |  |
| LP-0259 | Loupe zoom ratios from 1:16 to 11:1, lock zoom position, and the Navigator panel | LR-0210, LR-0212, LR-0213, LR-1486, LR-1487, LR-1612, LR-1661, LR-1662 | -- | -- | core | plan D04 T06 §1 | extends D04 T01 §9 |
| LP-0260 | Loupe overlays: grid, draggable guides, layout image with opacity and matte, overlay edit mode | LR-0214, LR-0215, LR-0216, LR-0217, LR-1492, LR-1609, LR-1610 | -- | -- | core | plan D04 T06 §1 |  |
| LP-0261 | Library sort order: capture, added, edit time, edit count, rating, pick, label, name, extension, type, aspect, with reverse | LR-0221, LR-0222, LR-1489 | -- | -- | core | plan D04 T06 §1 | extends D04 T01 §8 |
| LP-0262 | Custom user order by dragging in folders and collections | LR-0223 | -- | -- | core | plan D04 T06 §1 |  |
| LP-0263 | Selection commands: select all, none, active only, by flag, rating, and label with add, intersect, remove, invert; active versus selected photo | LR-0225, LR-0226, LR-0227, LR-0228, LR-1407, LR-1408, LR-1409, LR-1410, LR-1411, LR-1412, LR-1413, LR-1674, LR-1675, LR-1676, LR-1677, LR-1678, LR-1679, LR-1680, LR-1681, LR-1682 | -- | -- | core | plan D04 T06 §1 | extends D04 T01 §8 |
| LP-0264 | Grid view options: compact and expanded cells, extras, hover-only items, label tint, tooltips, cell icons, index numbers, labels, header and rating footer | LR-0229, LR-0230, LR-0231, LR-0232, LR-0233, LR-0234, LR-0235, LR-0236, LR-0237, LR-0238, LR-0239, LR-0240, LR-0241, LR-0242, LR-0243, LR-1490, LR-1493, LR-1498, LR-1611, LR-1670, LR-1671, LR-1672, LR-1673 | -- | -- | core | plan D04 T06 §1 |  |
| LP-0265 | Loupe info overlay: two configurable info sets, show briefly, loading message, embedded-preview message | LR-0245, LR-0246, LR-0247, LR-0248, LR-0251, LR-1491, LR-1606, LR-1607 | -- | -- | core | plan D04 T06 §1 |  |
| LP-0266 | HDR display of HDR-edited photos in the library, with a toggle | LR-0252, LR-0253, LR-1614 | -- | -- | core | plan D04 T06 §1 | consumes D03 T15 §4 HDR display path |
| LP-0267 | Remember the last selected photo per recent source | LR-0515 | -- | -- | core | plan D04 T06 §1 |  |
| LP-0268 | Increase and decrease flag status | LR-0257, LR-1704, LR-1705 | -- | -- | core | plan D04 T06 §2 |  |
| LP-0269 | Color label sets: rename labels, save, switch, and delete label sets | LR-0261, LR-1468 | AC-0786, AC-0787, AC-0797 | -- | core | plan D04 T06 §2 |  |
| LP-0270 | Refine photos: unflagged become rejects and picks reset for iterative culling | LR-0262, LR-1427, LR-1706 | -- | -- | core | plan D04 T06 §2 |  |
| LP-0271 | Delete rejected photos | LR-0525, LR-1461, LR-1639 | -- | -- | core | plan D04 T06 §2 | removes from catalog or moves to the Recycle Bin |
| LP-0272 | Rating details: hover rating on thumbnails, rate by drag, assign from the catalog pane, set rating command, status bar, Properties rating, clear and reset | LR-1692 | AC-0775, AC-0776, AC-0777, AC-0778, AC-0779, AC-0780, AC-0782, AC-0783, AC-0784 | -- | core | plan D04 T06 §2 |  |
| LP-0273 | Auto advance after tagging, rating, labeling, categorizing, or keywording in the viewer | -- | AC-0114, AC-1854 | -- | core | plan D04 T06 §2 | extends D04 T01 §11 |
| LP-0274 | Auto advance after applying tags, ratings, labels, categories, or keywords | -- | AC-0302, AC-0417 | -- | core | plan D04 T06 §2 | extends D04 T01 §11 |
| LP-0275 | Ratings and labels groups in the catalog pane | -- | AC-0732, AC-0733 | -- | core | plan D04 T06 §2 |  |
| LP-0276 | Color label details: hover label on thumbnails, drag assign, Properties boxes, set label command, status bar, label keys, search and filter by label, clear | -- | AC-0785, AC-0788, AC-0789, AC-0790, AC-0791, AC-0792, AC-0793, AC-0794, AC-0795, AC-0796 | -- | core | plan D04 T06 §2 |  |
| LP-0277 | Auto advance options: toolbar toggle, trigger types per metadata kind, in Manage and View modes, after keyword entry | -- | AC-0898, AC-0899, AC-0910, AC-0912, AC-4024, AC-4025, AC-4026, AC-4027, AC-4028, AC-4029, AC-4030 | -- | core | plan D04 T06 §2 | extends D04 T01 §11 |
| LP-0278 | Numeric keypad culling: tag, labels, ratings, remove rating and label, next and previous | -- | AC-0900, AC-0901, AC-0902, AC-0903, AC-0904, AC-0905, AC-0906, AC-0907, AC-0908, AC-0909 | -- | core | plan D04 T06 §2 |  |
| LP-0279 | Tagging: tag checkbox and reject mark on thumbnails, tagged and rejected lists, tag keys, clear tags, tag in viewer and compare | -- | AC-1006, AC-1007, AC-1008, AC-1009, AC-1010, AC-1011, AC-1012, AC-1013, AC-1014, AC-4390, AC-4391, AC-4392, AC-4597, AC-4598, AC-4599, AC-4941, AC-4942, AC-4943 | -- | core | plan D04 T06 §2 |  |
| LP-0280 | Tag and untag the current file and show tagged files | -- | -- | IV-0755, IV-1449, IV-1493, IV-1500 | core | plan D04 T06 §2 |  |
| LP-0281 | Stack commands: group, unstack, remove from, split, collapse and expand (one or all), move to top, up, and down, member counts | LR-0265, LR-0266, LR-0267, LR-0268, LR-0269, LR-0270, LR-0271, LR-0272, LR-0275, LR-1445, LR-1683, LR-1684, LR-1685, LR-1686, LR-1687 | AC-0798, AC-0800, AC-0801, AC-0806, AC-0807, AC-0808, AC-0809, AC-0810, AC-0811, AC-0812, AC-0813, AC-0814, AC-0815, AC-0816, AC-4482, AC-4483, AC-4485, AC-4486, AC-4487, AC-4488, AC-4489, AC-4490, AC-4491 | -- | core | plan D04 T06 §3 | extends D04 T02 §7 stacks |
| LP-0282 | Auto-stack by capture time and GPS distance with presets, live preview, and replace existing stacks | LR-0273 | AC-0817, AC-0818, AC-0819, AC-0820, AC-0821, AC-0822, AC-0823, AC-0825, AC-0826 | -- | core | plan D04 T06 §3 |  |
| LP-0283 | Stacks in collections | LR-0276 | -- | -- | core | plan D04 T06 §3 |  |
| LP-0284 | Virtual copy name field | LR-0399 | -- | -- | core | plan D04 T06 §3 |  |
| LP-0285 | Virtual copies: create, set copy as master, copy name | LR-0516, LR-0517, LR-0518, LR-1447, LR-1448, LR-1632 | -- | -- | core | plan D04 T06 §3 |  |
| LP-0286 | Stack rules: same-folder members, collapsed stack acts as its head, exclusions, visibility by mode, multi-folder views, stored in the catalog | -- | AC-0799, AC-0802, AC-0803, AC-0804, AC-0805, AC-0827 | -- | core | plan D04 T06 §3 |  |
| LP-0287 | Painter sprays flags, ratings, and labels | LR-0264 | -- | -- | core | plan D04 T06 §13 |  |
| LP-0288 | Painter tool: keywords, labels, flags, ratings, metadata presets, develop presets, rotation, target collection, erase mode | LR-0461, LR-0462, LR-0463, LR-0464, LR-0465, LR-0466, LR-0467, LR-1465, LR-1722 | -- | -- | core | plan D04 T06 §13 |  |
| LP-0289 | Quick Develop panel: saved preset, crop ratio, treatment, white balance, tone control with small and large relative steps, reset all | LR-0476, LR-0477, LR-0478, LR-0479, LR-0480, LR-0481, LR-0482, LR-0483, LR-0484 | -- | -- | core | plan D04 T06 §13 | consumes D01 T07 §1 |
| LP-0290 | Reference view beside the active photo | LR-0209, LR-1496, LR-1608 | -- | -- | core | plan D04 T09 §1 |  |
| LP-0291 | People view in the library | LR-0197, LR-1613 | -- | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach) |
| LP-0292 | Visual search for similar photos from the library | LR-0208, LR-1481, LR-1727 | -- | -- | ai | plan D04 T10 §5 |  |
| LP-0293 | Auto-stack by visual similarity | LR-0274 | AC-0824 | -- | ai | plan D04 T10 §5 | local perceptual features |
| LP-0294 | Assisted culling badges on thumbnails | LR-0244 | -- | -- | ai | plan D04 T10 §6 |  |
| LP-0295 | Assisted culling: background analysis of subject focus, eye focus, eyes open, and exposure with an enable setting and a start or pause control | LR-0279, LR-0280, LR-0281 | -- | -- | ai | plan D04 T10 §6 | focus and exposure scored locally; eyes open through an OpenRouter vision model on face crops, opt-in with send preview |
| LP-0296 | Assisted culling select criteria: subject focus and eye focus thresholds, eyes open, only photos with eyes, include cannot-tell photos | LR-0282, LR-0283, LR-0284, LR-0285, LR-0286 | -- | -- | ai | plan D04 T10 §6 | eye state through an OpenRouter vision model on user action |
| LP-0297 | Assisted culling reject criteria: exposure issues, misfires, documents and receipts | LR-0287, LR-0288, LR-0289 | -- | -- | ai | plan D04 T10 §6 | exposure and misfire metrics local; document detection through the vision model |
| LP-0298 | Assisted culling review and results: selects, rejects, or all, auto stack similar shots, batch flag, rating, and label, add to or remove from a collection, remove rejects from the catalog | LR-0290, LR-0291, LR-0292, LR-0293, LR-0294, LR-0295, LR-0296, LR-0297 | -- | -- | ai | plan D04 T10 §6 | removing rejects deletes catalog records only, never files |
| LP-0299 | Assisted culling info: per-photo scores, per-face eyes open and eye sharpness, badge hover reasons, and manual select or reject override | LR-0298, LR-0299, LR-0300, LR-0301 | -- | -- | ai | plan D04 T10 §6 | every verdict is data the user can override and undo |
| LP-0300 | Rename photo with a filename template | LR-0519, LR-1428, LR-1635 | -- | -- | core | plan D04 T11 §3 |  |
| LP-0301 | Impromptu slideshow of the selection | LR-0218, LR-1499, LR-1665 | -- | -- | core | plan D04 T12 §8 |  |
| LP-0302 | Library grid view with cell badges and the thumbnail size slider | LR-0189, LR-0224, LR-1488, LR-1597, LR-1657, LR-1668 | -- | -- | core | shipped-scope D04 T01 §8 |  |
| LP-0303 | Loupe view with fit and click-to-zoom toggle | LR-0190, LR-0211, LR-1438, LR-1484, LR-1485, LR-1596, LR-1656, LR-1658 | -- | -- | core | shipped-scope D04 T01 §9 |  |
| LP-0304 | Compare view: select and candidate with linked and synced zoom | LR-0191, LR-0192, LR-0193, LR-1598 | -- | -- | core | shipped-scope D04 T01 §9 |  |
| LP-0305 | Pick, reject, and unflag, 0 to 5 stars, color labels, flags global across sources, and auto advance | LR-0254, LR-0255, LR-0256, LR-0258, LR-0259, LR-0260, LR-0263, LR-1451, LR-1452, LR-1688, LR-1689, LR-1690, LR-1691, LR-1693, LR-1694, LR-1695, LR-1696, LR-1697, LR-1698, LR-1699, LR-1700, LR-1701, LR-1702, LR-1703 | AC-4408, AC-4409, AC-4410, AC-4411, AC-4412, AC-4413, AC-4602, AC-4937 | -- | core | shipped-scope D04 T01 §11 |  |
| LP-0306 | Externally edited copies stack with the original | LR-0278 | -- | -- | core | shipped-scope D04 T02 §7 |  |
| LP-0307 | Rating keys Ctrl+0 to 5 and xmp:rating interoperability | -- | AC-0781, AC-4402, AC-4403, AC-4404, AC-4405, AC-4406, AC-4407, AC-4601, AC-4938 | -- | core | shipped-scope D04 T01 §11 |  |

## Collections, search, and categories

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0308 | Attribute filters: flag, edited, rating comparisons, color label, kind (master, virtual copy, video), stacked status | LR-0277, LR-0324, LR-0325, LR-0326, LR-0327, LR-0328, LR-0330, LR-1426 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0309 | Library filter bar: filter none, enable and disable filters, find | LR-0302, LR-0303, LR-0306, LR-0307, LR-1401, LR-1423, LR-1424, LR-1483, LR-1707, LR-1708, LR-1709, LR-1710 | -- | -- | core | plan D04 T06 §4 | extends D04 T01 §8 |
| LP-0310 | Filter presets and lock filters across sources | LR-0304, LR-0305, LR-1425 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0311 | Text filter fields: any field, filename, copy name, title, caption, keywords, searchable metadata, IPTC, EXIF | LR-0308, LR-0309, LR-0310, LR-0311, LR-0312, LR-0313, LR-0314, LR-0315, LR-0316 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0312 | Text filter rules and operators: contains, contains all, words, does not contain, starts and ends with, ! and + operators | LR-0318, LR-0319, LR-0320, LR-0321, LR-0322, LR-0323 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0313 | Metadata browser columns: up to eight cascading columns, flat or hierarchical, multi-select, none | LR-0331, LR-0332, LR-0333, LR-0382 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0314 | Metadata columns for dates: date, year and month, day and month | LR-0334, LR-0335, LR-0336 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0315 | Metadata columns for file and attributes: file type, flag, rating, exported, label, keywords, edit | LR-0337, LR-0338, LR-0339, LR-0340, LR-0341, LR-0342, LR-0343 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0316 | Metadata columns for camera and exposure: camera, serial number, lens, focal length, shutter, aperture, ISO, flash | LR-0344, LR-0345, LR-0346, LR-0347, LR-0348, LR-0349, LR-0350, LR-0351 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0317 | Metadata columns for location: has GPS, GPS location, sublocation, city, state, country | LR-0352, LR-0353, LR-0354, LR-0355, LR-0356, LR-0357 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0318 | Metadata columns for IPTC creator, copyright status, and job | LR-0358, LR-0359, LR-0360 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0319 | Metadata columns for develop state: aspect, HDR mode, depth, masking, remove modes, point color, settings, smart preview, snapshots, treatment, metadata status | LR-0361, LR-0362, LR-0363, LR-0369, LR-0370, LR-0371, LR-0372, LR-0373, LR-0374, LR-0375, LR-0376 | -- | -- | core | plan D04 T06 §4 |  |
| LP-0320 | Metadata columns for AI edits: has AI, generative, needs update, edit type, reflection and people removal, denoise, raw details, super resolution | LR-0364, LR-0365, LR-0366, LR-0367, LR-0368, LR-0377, LR-0378, LR-0379, LR-0380, LR-0381 | -- | -- | ai | plan D04 T06 §4 |  |
| LP-0321 | Target collection and Quick Collection: set target, add with a key, save and clear Quick Collection | LR-0488, LR-0545, LR-0551, LR-0552, LR-0553, LR-0554, LR-1397, LR-1398, LR-1399, LR-1400, LR-1437, LR-1712, LR-1713, LR-1714, LR-1715, LR-1716, LR-1717 | AC-0833, AC-0837, AC-0838 | -- | core | plan D04 T06 §5 |  |
| LP-0322 | Remove from the selected collection or from all collections | LR-0524 | AC-0840, AC-0841 | -- | core | plan D04 T06 §5 |  |
| LP-0323 | Create collection dialog: name, include selected photos, virtual copies, inside a set, add by drag, context menu, or Organize tab, duplicate collection | LR-0542, LR-0543, LR-0559, LR-0561, LR-1419, LR-1711 | AC-0828, AC-0829, AC-0830, AC-0831, AC-0832, AC-0834, AC-0835, AC-0836 | -- | core | plan D04 T06 §5 | extends D04 T01 §10 |
| LP-0324 | Collection sets and nesting | LR-0546, LR-1421 | AC-0842, AC-0843, AC-0844 | -- | core | plan D04 T06 §5 |  |
| LP-0325 | Smart collections: create and edit, match all, any, or none, nested rule groups, criteria operators | LR-0547, LR-0548, LR-0549, LR-1420 | AC-0845, AC-0846, AC-0847, AC-0848, AC-0849, AC-0850, AC-0851 | -- | core | plan D04 T06 §5 | extends D04 T01 §10 |
| LP-0326 | Export and import smart collection settings | LR-0550 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0327 | Collections filter, sort, and color labels | LR-0555, LR-0557 | AC-0839 | -- | core | plan D04 T06 §5 |  |
| LP-0328 | Output creations saved as collections for book, slideshow, print, and web | LR-0558 | -- | -- | core | plan D04 T06 §5 | layouts owned by D04 T12 §4, D04 T12 §7, D04 T12 §9, D04 T12 §10 |
| LP-0329 | Smart collection rules for attributes: rating, flag, label color and text, smart preview, snapshots, adjustments, edits, cropped | LR-0563, LR-0565, LR-0566, LR-0567, LR-0570, LR-0571, LR-0608, LR-0609, LR-0610 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0330 | Smart collection rules for sources: folder, collection, publish collection, published via, exported | LR-0564, LR-0572, LR-0573, LR-0574, LR-0575 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0331 | Smart collection rules for files: filename, copy name, file type, DNG fast load data, dimensions, megapixels, aspect, bit depth, color mode and profile | LR-0576, LR-0577, LR-0578, LR-0579, LR-0626, LR-0627, LR-0628, LR-0629, LR-0630, LR-0631, LR-0632, LR-0633 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0332 | Smart collection rules for dates: capture and edit date with absolute, relative, and range operators | LR-0580, LR-0581 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0333 | Smart collection rules for camera and exposure | LR-0582, LR-0583, LR-0584, LR-0585, LR-0586, LR-0587, LR-0588, LR-0589 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0334 | Smart collection rules for location and GPS | LR-0590, LR-0591, LR-0592, LR-0593, LR-0594 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0335 | Smart collection rules for IPTC text: title, caption, alt text, extended description, keywords, creator, job, copyright status | LR-0595, LR-0596, LR-0597, LR-0598, LR-0599, LR-0600, LR-0601, LR-0602 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0336 | Smart collection rules for searchable text and metadata status | LR-0603, LR-0604, LR-0605, LR-0607, LR-0634 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0337 | Smart collection rules for develop and AI state: HDR, depth, AI, generative, needs update, masking, remove, point color, proof, preset, treatment, lens and CA corrections, AI pipeline order | LR-0611, LR-0612, LR-0613, LR-0614, LR-0615, LR-0616, LR-0617, LR-0618, LR-0619, LR-0620, LR-0621, LR-0622, LR-0623, LR-0624, LR-0625, LR-0635 | -- | -- | core | plan D04 T06 §5 |  |
| LP-0338 | Organize pane collections group | -- | AC-0868 | -- | core | plan D04 T06 §5 |  |
| LP-0339 | Catalog pane: categories, auto categories, people, ratings, labels, keywords, searches, special items | -- | AC-0038, AC-4459 | -- | core | plan D04 T06 §6 |  |
| LP-0340 | Catalog pane with Easy-Select combinations, match all or any, click to search | -- | AC-0726, AC-0750, AC-0751, AC-0752, AC-0754 | -- | core | plan D04 T06 §6 |  |
| LP-0341 | Categories: hierarchical virtual categories, create, edit, delete, move, filter, assign and unassign, uncategorize, set categories command | -- | AC-0727, AC-0755, AC-0756, AC-0757, AC-0758, AC-0759, AC-0760, AC-0761, AC-0766, AC-0767, AC-0768, AC-0769, AC-0770, AC-0771, AC-0772, AC-0773, AC-0774, AC-0911 | -- | core | plan D04 T06 §6 |  |
| LP-0342 | Auto categories from metadata: groupings, commonly used, multi-select, match any or all, combined with ratings, categories, and selective browsing | -- | AC-0734, AC-1130, AC-1131, AC-1132, AC-1133, AC-1134, AC-1135, AC-1136, AC-1137 | -- | core | plan D04 T06 §6 |  |
| LP-0343 | Special items: all images, embed pending, uncategorized, no keywords, unnamed, auto-named, and suggested faces, tagged, rejected | -- | AC-0738, AC-0740, AC-0741, AC-0742, AC-0743, AC-0744, AC-0745, AC-0746, AC-0747, AC-1155, AC-1156, AC-1157 | -- | core | plan D04 T06 §6 | the auto-named and suggested face items need face recognition, backlog B-052, and are not built until it is promoted |
| LP-0344 | Catalog pane options: icons, Easy-Select bar and tooltip, assign by clicking, category delete confirmations | -- | AC-0753, AC-4173, AC-4174, AC-4175, AC-4176, AC-4177, AC-4178, AC-4179 | -- | core | plan D04 T06 §6 |  |
| LP-0345 | Quick category sets: button grid with rows, columns, sub-category syntax, assignment state | -- | AC-0762, AC-0763, AC-0764, AC-0765 | -- | core | plan D04 T06 §6 |  |
| LP-0346 | Organize pane categories group | -- | AC-0867 | -- | core | plan D04 T06 §6 |  |
| LP-0347 | Advanced search pane with saved search presets listed in the catalog pane | -- | AC-0034, AC-0035 | -- | core | plan D04 T06 §7 |  |
| LP-0348 | Saved searches and search templates in the catalog pane, re-run with one click | -- | AC-0735, AC-0736, AC-0737, AC-1081, AC-1154 | -- | core | plan D04 T06 §7 |  |
| LP-0349 | Quick search bar: scope, match types, classic operators, history | -- | AC-1065, AC-1066, AC-1067, AC-1068, AC-1069, AC-1070, AC-1071, AC-1072, AC-1073, AC-1074, AC-1075, AC-4437 | -- | core | plan D04 T06 §7 |  |
| LP-0350 | Quick search fields option: names, metadata, categories, keywords, AI keywords, people with assigned or suggested names, folder contents | -- | AC-1076, AC-4072, AC-4073, AC-4074, AC-4075, AC-4076, AC-4077, AC-4078, AC-4079, AC-4080, AC-4081, AC-4082 | -- | core | plan D04 T06 §7 |  |
| LP-0351 | Advanced search pane: match all, sources (catalog, folders, current view), file types, criteria picker, AND and OR, criterion options, history | -- | AC-1077, AC-1079, AC-1084, AC-1085, AC-1086, AC-1087, AC-1088, AC-1089, AC-1090, AC-1091, AC-4439, AC-4460 | -- | core | plan D04 T06 §7 |  |
| LP-0352 | Search presets: choose, save, delete | -- | AC-1080, AC-1082, AC-1083 | -- | core | plan D04 T06 §7 |  |
| LP-0353 | Advanced search folder handling: folders, folders and contents, contents only | -- | AC-1092, AC-1093, AC-1094 | -- | core | plan D04 T06 §7 |  |
| LP-0354 | Filename criterion: any or all terms, history autocomplete, wildcard pattern match with sets, ranges, escapes | -- | AC-1095, AC-1096, AC-1097, AC-1098, AC-1099, AC-1100, AC-1101, AC-1102, AC-1103, AC-1104, AC-1105, AC-1106 | -- | core | plan D04 T06 §7 |  |
| LP-0355 | Text, people, keyword, category, rating, and label criteria | -- | AC-1107, AC-1108, AC-1111, AC-1112 | -- | core | plan D04 T06 §7 |  |
| LP-0356 | Metadata criterion types: string, date and time, lookup list, integer, rational, literal semicolons | -- | AC-1113, AC-1114, AC-1115, AC-1116, AC-1117, AC-1118 | -- | core | plan D04 T06 §7 |  |
| LP-0357 | Search files on disk: name pattern, start folder with subfolders, file date range, results as thumbnails | -- | -- | IV-0090, IV-0091, IV-0092, IV-0093, IV-0097, IV-1455 | core | plan D04 T06 §7 |  |
| LP-0358 | Search metadata text in files: EXIF, IPTC, comments, exact phrase, any metadata present | -- | -- | IV-0094, IV-0095, IV-0096 | core | plan D04 T06 §7 |  |
| LP-0359 | Search files results shown in the browser | -- | -- | IV-0927 | core | plan D04 T06 §7 |  |
| LP-0360 | Current and previous import in the catalog panel, selected during import | LR-0125, LR-0142 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0361 | People group in the catalog pane with face search options | -- | AC-0728, AC-0729 | -- | ai | plan D04 T10 §3 |  |
| LP-0362 | AI keywords group in the catalog pane | -- | AC-0731 | -- | ai | plan D04 T10 §4 |  |
| LP-0363 | Search for similar images: reverse image search criterion with similarity slider | -- | AC-1078, AC-1109, AC-1110 | -- | ai | plan D04 T10 §5 | local perceptual features |
| LP-0364 | Keywords group in the catalog pane | -- | AC-0730 | -- | core | shipped-scope D04 T01 §10 |  |

## Catalog management

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0365 | Catalog panel: all photographs, previous import, missing photographs, added by previous export, errors and updated photos | LR-0485, LR-0486, LR-0489, LR-0490, LR-0491, LR-0492 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0366 | Folders panel: volumes with free space, counts, and online status | LR-0493, LR-0494 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0367 | Folder operations: add, create, rename, remove from catalog, move by drag, show in Explorer | LR-0495, LR-0496, LR-0497, LR-0498, LR-0499, LR-0506, LR-0520, LR-1422, LR-1439, LR-1631, LR-1633 | -- | -- | core | plan D04 T06 §8 | rename and move are file operations; image bytes untouched |
| LP-0368 | Synchronize folder: import new files, remove missing, rescan metadata | LR-0500, LR-1431 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0369 | Show parent folder and hide this parent | LR-0501, LR-0502 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0370 | Missing folders: update folder location, find missing folder, alert on parent | LR-0503, LR-0504, LR-0505 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0371 | Folder color labels, favorites, and the folder filter | LR-0510, LR-0511, LR-0512 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0372 | Show photos in subfolders and folder path display | LR-0513, LR-0514, LR-1432 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0373 | Go to folder in library and go to collection | LR-0521, LR-0522, LR-1440 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0374 | Remove photos from the catalog or delete them to the Recycle Bin | LR-0523, LR-1459, LR-1460, LR-1636, LR-1637, LR-1638 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0375 | Find missing photos and locate a missing photo | LR-0529, LR-0530, LR-1430 | -- | -- | core | plan D04 T06 §8 |  |
| LP-0376 | Rebind catalog records to files moved outside Albumen | -- | AC-0976 | -- | core | plan D04 T06 §8 |  |
| LP-0377 | Drive mapping when importing or restoring a catalog | -- | AC-1774 | -- | core | plan D04 T06 §8 |  |
| LP-0378 | Photo discs and offline media: new, browse offline, update, identify by serial or label, rebind | -- | AC-2012, AC-2013, AC-2014, AC-2015, AC-2016, AC-2017, AC-4188, AC-4189 | -- | core | plan D04 T06 §8 |  |
| LP-0379 | Optimize catalog and relaunch and optimize | LR-1288, LR-1300 | -- | -- | core | plan D04 T06 §9 |  |
| LP-0380 | Catalog lock against concurrent opening | LR-1290 | -- | -- | core | plan D04 T06 §9 |  |
| LP-0381 | Catalog backup: schedule, folder, integrity test, optimize after, skip, zip compression | LR-1293, LR-1294, LR-1295, LR-1296, LR-1297, LR-1298, LR-1299, LR-1404 | -- | -- | core | plan D04 T06 §9 | promotes B-036 |
| LP-0382 | Optimize catalog from preferences | LR-1338 | -- | -- | core | plan D04 T06 §9 |  |
| LP-0383 | Backup wizard: new or update backup, location, thumbnails choice, image and media files, scopes, daily folders, reminder | -- | AC-1753, AC-1754, AC-1755, AC-1756, AC-1757, AC-1758, AC-1759, AC-1760, AC-1761, AC-1762, AC-1763, AC-1764, AC-4214 | -- | core | plan D04 T06 §9 |  |
| LP-0384 | Restore catalog from a backup | -- | AC-1765 | -- | core | plan D04 T06 §9 |  |
| LP-0385 | Catalog maintenance: per-folder records, remove thumbnails, remove all info, remove orphan folders, change binding | -- | AC-1766, AC-1767, AC-1768, AC-1769, AC-1770 | -- | core | plan D04 T06 §9 |  |
| LP-0386 | Optimize database: shrink, re-index, remove orphans | -- | AC-1771, AC-1772, AC-1773 | -- | core | plan D04 T06 §9 |  |
| LP-0387 | Rebuild thumbnails and metadata for selected files or folders | -- | AC-1775 | -- | core | plan D04 T06 §9 |  |
| LP-0388 | Quarantine files that fail to read, with enable switch | -- | AC-1776, AC-1777 | -- | core | plan D04 T06 §9 |  |
| LP-0389 | Import from a Photoshop Elements catalog | LR-0128 | -- | -- | core | plan D04 T06 §10 | same read-only importer path as the Lightroom catalog |
| LP-0390 | Import from another Albumen catalog: file handling, changed existing photos, preserve old settings as a virtual copy, replace non-raw only | LR-0129, LR-0130, LR-0131, LR-0132, LR-0133, LR-1388 | -- | -- | core | plan D04 T06 §10 |  |
| LP-0391 | Export a folder, a collection, or the selection as a catalog, with negatives, previews, and selected-only options | LR-0507, LR-0560, LR-1283, LR-1284, LR-1286, LR-1287 | -- | -- | core | plan D04 T06 §10 |  |
| LP-0392 | Build standard and 1:1 previews and discard 1:1 previews | LR-0531, LR-0532, LR-0533, LR-1436 | -- | -- | core | plan D04 T06 §10 | extends D04 T01 §7 |
| LP-0393 | Open a recent catalog | LR-1282 | -- | -- | core | plan D04 T06 §10 |  |
| LP-0394 | Catalog settings: location info, show in Explorer, open settings | LR-1301, LR-1302, LR-1320, LR-1417, LR-1628 | -- | -- | core | plan D04 T06 §10 |  |
| LP-0395 | Preview settings: standard preview size, quality, auto-discard 1:1 previews | LR-1303, LR-1304, LR-1305 | -- | -- | core | plan D04 T06 §10 | extends D04 T01 §7 |
| LP-0396 | Catalog settings from preferences | LR-1328 | -- | -- | core | plan D04 T06 §10 |  |
| LP-0397 | Import from a Lightroom Classic catalog: ratings, labels, collections, keywords, catalog location, summary and results | -- | AC-0390, AC-0391, AC-0392, AC-0393, AC-0394, AC-0395, AC-0396 | -- | core | plan D04 T06 §10 | reads the .lrcat SQLite file read-only |
| LP-0398 | Multiple catalogs: new, open, recent, name in the title bar | -- | AC-1731, AC-1732, AC-1733, AC-1734, AC-1735 | -- | core | plan D04 T06 §10 |  |
| LP-0399 | Catalog import and export: compressed catalog of all or selected items, XML text export of chosen fields, location options, optimize after import | -- | AC-1741, AC-1742, AC-1747, AC-1748, AC-1749, AC-1750, AC-1751 | -- | core | plan D04 T06 §10 |  |
| LP-0400 | Generate a file listing as a text table | -- | AC-1752 | -- | core | plan D04 T06 §10 |  |
| LP-0401 | Smart previews: build, discard, status, use for editing, include in catalog export, cache size | LR-0534, LR-0535, LR-0536, LR-0537, LR-1285, LR-1306 | -- | -- | core | plan D04 T06 §11 |  |
| LP-0402 | Dashboard mode with catalog files for accurate statistics | -- | AC-0158, AC-3970, AC-3971, AC-4517, AC-4691, AC-4982 | -- | core | plan D04 T06 §12 | extends D04 T01 §10 statistics |
| LP-0403 | Dashboard overview: photo count by year or month, database, camera, and file summaries | -- | AC-0159, AC-0160, AC-0161, AC-0162, AC-0163, AC-3972, AC-3973, AC-3974, AC-3975, AC-3976 | -- | core | plan D04 T06 §12 |  |
| LP-0404 | Dashboard database tab: size and path, file and folder breakdown, orphans, backup date, thumbnail cache | -- | AC-0164, AC-0165, AC-0166, AC-0167, AC-0168, AC-0169, AC-0170, AC-3977, AC-3978, AC-3979, AC-3980, AC-3981, AC-3982 | -- | core | plan D04 T06 §12 |  |
| LP-0405 | Dashboard cameras tab: most used camera, lens, focal length, aperture, shutter, ISO with charts, graph toggles | -- | AC-0171, AC-0172, AC-0173, AC-0174, AC-0175, AC-3983, AC-3984, AC-3985, AC-3986 | -- | core | plan D04 T06 §12 |  |
| LP-0406 | Dashboard files tab: formats and bit depths charts, top 20 resolutions | -- | AC-0176, AC-0177, AC-0178, AC-3987 | -- | core | plan D04 T06 §12 |  |
| LP-0407 | Import to this folder from the Folders panel | LR-0508 | -- | -- | core | plan D04 T07 §1 |  |
| LP-0408 | Import sequence number counters | LR-1307 | -- | -- | core | plan D04 T07 §2 |  |
| LP-0409 | Convert photo to DNG with options | LR-0526, LR-0527, LR-1429 | -- | -- | format | plan D04 T07 §6 | writes a new DNG; originals go to the Recycle Bin only after a verified conversion when chosen |
| LP-0410 | Metadata stored in the catalog and embedded for relocation, per-format embedding | -- | AC-0748, AC-0749 | -- | format | plan D04 T08 §1 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0411 | Import metadata when cataloging: EXIF and IPTC, IPTC keywords and supplemental categories, embedded catalog metadata, database date from EXIF, embed-pending on tagging | -- | AC-1796, AC-1797, AC-1798, AC-1799, AC-4216, AC-4217, AC-4218 | -- | core | plan D04 T08 §1 |  |
| LP-0412 | Metadata autocomplete suggestions and clearing them | LR-1308, LR-1309 | -- | -- | core | plan D04 T08 §2 |  |
| LP-0413 | Write date and time changes into raw files | LR-1319 | -- | -- | core | plan D04 T08 §4 | sidecar by default and never the raw file; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0414 | Separator conflict dialogs for IPTC keywords and supplemental categories | -- | AC-4219, AC-4220 | -- | core | plan D04 T08 §5 |  |
| LP-0415 | Address lookup (reverse geocoding) and exporting suggested locations | LR-1314, LR-1315 | -- | -- | cloud | plan D04 T08 §7 | offline geocoding |
| LP-0416 | Save metadata for a whole folder | LR-0509 | -- | -- | core | plan D04 T08 §8 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0417 | Sidecar details: split large develop data, fast writes for small edits, metadata conflict badge | LR-1312, LR-1313, LR-1322 | -- | -- | core | plan D04 T08 §8 |  |
| LP-0418 | Import and export descript.ion caption files | -- | AC-1745, AC-1746 | -- | core | plan D04 T08 §8 |  |
| LP-0419 | AI edit pixel data stored beside the catalog, with repair | LR-1291, LR-1292 | -- | -- | ai | plan D04 T10 §1 |  |
| LP-0420 | Face detection automatic or on demand (catalog setting) | LR-1316 | -- | -- | ai | plan D04 T10 §2 | Automatic runs only under an approved send scope; through an OpenRouter vision model on explicit send with the send preview and provenance (operator decision 2026-09-27; the local YuNet model was not approved) |
| LP-0421 | Import face data from ACDSee, Lightroom, or Picasa when cataloging | -- | AC-1800 | -- | ai | plan D04 T10 §12 |  |
| LP-0422 | Assisted culling analysis on or off (catalog setting) | LR-1318 | -- | -- | ai | plan D04 T10 §6 |  |
| LP-0423 | Render to DNG with edits baked in | LR-0528, LR-1462 | -- | -- | format | plan D04 T12 §2 | writes a new file, never the original |
| LP-0424 | Include develop settings in rendered JPEG, TIFF, PNG, and PSD files | LR-1310 | -- | -- | core | plan D04 T12 §13 |  |
| LP-0425 | Presets stored with the catalog | LR-1323 | -- | -- | core | plan D04 T14 §6 |  |
| LP-0426 | New catalog and open catalog | LR-1280, LR-1281, LR-1626 | -- | -- | core | shipped-scope D04 T01 §5 |  |
| LP-0427 | Catalog upgrade keeping the original catalog | LR-1289 | -- | -- | core | shipped-scope D04 T01 §5 | forward migrations with a backup first |
| LP-0428 | Automatically write changes to XMP sidecars | LR-1311, LR-1321 | -- | -- | format | shipped-scope D04 T01 §11 | sidecar for every format, never embedded in the original (original-file guard) |
| LP-0429 | Convert catalogs from older versions | -- | AC-1737, AC-1738, AC-1739, AC-1740 | -- | core | shipped-scope D04 T01 §5 | Albumen forward migrations with a backup |
| LP-0430 | Catalog file location setting | -- | AC-4213 | -- | core | shipped-scope D04 T01 §5 |  |
| LP-0431 | Import legacy ACDSee Photo Disc databases and albums | -- | AC-1743, AC-1744 | -- | core | other-app: none legacy ACDSee 4 and 5 .ddf and .ais files |  |

## Import and capture

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0432 | Import source panel: devices, card readers, removable drives, local and network folders, optical discs, include subfolders, favorite and recent sources | LR-0067, LR-0068, LR-0070, LR-0071, LR-0072, LR-1387, LR-1625 | AC-0329, AC-0378, AC-0379 | -- | core | plan D04 T07 §1 | extends D04 T01 §6 |
| LP-0433 | Move mode and removing items from the source after import | LR-0075 | AC-0370 | -- | core | plan D04 T07 §1 | source files go to the Recycle Bin only after a hash-verified copy |
| LP-0434 | Import candidate grid: check and uncheck photos, check all, import new, all, or custom selection, view all or selected | LR-0077, LR-0078 | AC-0334, AC-0335, AC-0338, AC-0339 | -- | core | plan D04 T07 §1 |  |
| LP-0435 | Import candidate filters and grouping: all, new photos only, by destination folder, by date, by file type, sort order | LR-0079, LR-0080, LR-0081, LR-0082 | AC-0333, AC-0336, AC-0337 | -- | core | plan D04 T07 §1 |  |
| LP-0436 | Import preview: thumbnail size, loupe preview, higher-quality embedded previews, compact dialog | LR-0083, LR-0084, LR-0085, LR-0086 | AC-0340 | -- | core | plan D04 T07 §1 |  |
| LP-0437 | Drag and drop files or folders onto Albumen to import | LR-0140 | -- | -- | core | plan D04 T07 §1 |  |
| LP-0438 | Import menu entry in the browser | -- | AC-0048, AC-4398 | -- | core | plan D04 T07 §1 |  |
| LP-0439 | Import completion: browse the imported photos in a new tab | -- | AC-0332 | -- | core | plan D04 T07 §1 | extends D04 T01 §6 completion summary |
| LP-0440 | Eject device after import | LR-0069 | -- | -- | core | plan D04 T07 §2 |  |
| LP-0441 | Build previews on import: minimal, embedded and sidecar, standard, 1:1, and replace embedded previews when idle | LR-0087, LR-0088, LR-0089, LR-0090, LR-0145 | -- | -- | core | plan D04 T07 §2 | extends D04 T01 §7 |
| LP-0442 | Build smart previews on import | LR-0091 | -- | -- | core | plan D04 T07 §2 | builds through D04 T06 §11 smart previews |
| LP-0443 | Second backup copy on import to another location | LR-0093 | AC-0356, AC-0357 | -- | core | plan D04 T07 §2 | hash-verified like the primary copy |
| LP-0444 | Rename files on import with templates: custom name, sequence, date, filename, shoot name, camera, start number, extension case, sample | LR-0096, LR-0097, LR-0098, LR-0099, LR-0100, LR-0101, LR-0102, LR-0103, LR-0104, LR-0105, LR-0107, LR-0108, LR-0109, LR-0110, LR-0111 | AC-0358, AC-0359, AC-0360, AC-0361, AC-0362, AC-0363, AC-0364, AC-0389 | -- | core | plan D04 T07 §2 | consumes D04 T11 §2 token engine |
| LP-0445 | Import destination organization: destination folder, named subfolder, by original folders, by capture or today date in nested or separate folders, one folder, date formats, preview of new folders | LR-0116, LR-0117, LR-0118, LR-0119, LR-0120, LR-0121, LR-0122 | AC-0322, AC-0347, AC-0348, AC-0349, AC-0350, AC-0351, AC-0352, AC-0353, AC-0354, AC-0355 | -- | core | plan D04 T07 §2 | extends D04 T01 §6 folder pattern |
| LP-0446 | Import folder options: ignore camera-generated folder names, show parent folder | LR-0143, LR-0146 | -- | -- | core | plan D04 T07 §2 |  |
| LP-0447 | RAW+JPEG placement on import: same folder or JPEG or RAW in a named subfolder | -- | AC-0325, AC-0326, AC-0327, AC-0328 | -- | core | plan D04 T07 §2 |  |
| LP-0448 | Add imported photos to a collection | LR-0094 | -- | -- | core | plan D04 T07 §3 |  |
| LP-0449 | Apply during import: develop preset, metadata preset (including inline creation), keywords, categories, and ACDSee-style custom metadata | LR-0112, LR-0113, LR-0114, LR-0115 | AC-0366, AC-0367, AC-0368 | -- | core | plan D04 T07 §3 |  |
| LP-0450 | Import presets: save, update, rename, delete, current, last used, none, recent | LR-0123 | AC-0341, AC-0342, AC-0343, AC-0344, AC-0345, AC-0346 | -- | automation | plan D04 T07 §3 |  |
| LP-0451 | Automatic rotation on import from camera orientation | -- | AC-0369 | -- | core | plan D04 T07 §3 | orientation stored as metadata, never written into the original |
| LP-0452 | Import date source for the catalog: EXIF date, file modified date, or a specific date | -- | AC-0371, AC-0372, AC-0373, AC-0374 | -- | core | plan D04 T07 §3 |  |
| LP-0453 | Show the import dialog when a memory card is detected and AutoPlay handlers for import and browse | LR-0141 | AC-0323, AC-0324 | -- | core | plan D04 T07 §4 |  |
| LP-0454 | Import from WIA and portable devices (cameras, phones) including browsing a phone in the folder tree | -- | AC-0330, AC-0331, AC-0397, AC-0398 | -- | core | plan D04 T07 §4 | Windows Portable Devices, no drive letter needed |
| LP-0455 | Auto import from a watched folder: enable, watched folder, destination and subfolder, naming, develop, metadata and keywords, initial previews | LR-0134, LR-0135, LR-0136, LR-0137, LR-0138, LR-0139 | -- | -- | automation | plan D04 T07 §5 | the tether path through vendor capture utilities |
| LP-0456 | Auto import watched folder | LR-1385, LR-1390 | -- | -- | automation | plan D04 T07 §5 |  |
| LP-0457 | Copy as DNG import mode | LR-0073 | -- | -- | format | plan D04 T07 §6 | consumes D04 T13 §7 DNG writer |
| LP-0458 | DNG conversion options: extension case, JPEG preview size, fast load data, embed original raw, lossy compression, compatibility version | LR-0147, LR-0148, LR-0149, LR-0150, LR-0151, LR-0152 | -- | -- | format | plan D04 T07 §6 |  |
| LP-0459 | Scanning destination folder | -- | AC-0376 | -- | core | plan D04 T07 §7 |  |
| LP-0460 | Scan a single image through TWAIN or WIA, including 32-bit TWAIN drivers from the 64-bit build | -- | AC-0377 | IV-0155, IV-0166, IV-0167 | core | plan D04 T07 §7 | consumes the WIA acquisition moved from D03 T17 §12 |
| LP-0461 | Scanning destination folder | -- | AC-4067 | -- | core | plan D04 T07 §7 |  |
| LP-0462 | TWAIN source selection, acquire and batch scanning, and Copy Shop | -- | -- | IV-0124, IV-0125, IV-0126, IV-1509 | core | plan D04 T07 §7 |  |
| LP-0463 | Batch scanning: file name with placeholders, counter start, step, digits, skip existing, remember counter, destination, format, multipage TIFF or PDF, scanner UI kept open | -- | -- | IV-0156, IV-0157, IV-0158, IV-0159, IV-0160, IV-0161, IV-0162, IV-0163, IV-0164, IV-0165 | core | plan D04 T07 §7 |  |
| LP-0464 | Copy Shop: scan and print copies with scanner, preview, DPI, printer, and number of copies | -- | -- | IV-0168, IV-0169, IV-0170, IV-0171, IV-0172 | print | plan D04 T07 §7 |  |
| LP-0465 | Screen capture utility running from the notification area, with exit and include cursor | -- | AC-1158, AC-1159, AC-1160 | -- | core | plan D04 T07 §8 |  |
| LP-0466 | Screen capture sources: desktop, whole window, window content, fixed or selected region, child window, menu under cursor | -- | AC-1161, AC-1162, AC-1163, AC-1164, AC-1165, AC-1166, AC-1167 | -- | core | plan D04 T07 §8 |  |
| LP-0467 | Screen capture destinations and triggers: clipboard, file, editor, hot key, timer | -- | AC-1168, AC-1169, AC-1170, AC-1171, AC-1172 | -- | core | plan D04 T07 §8 |  |
| LP-0468 | Screen capture: whole desktop, monitor, window, client area, region, object with auto scroll, fixed rectangle | -- | -- | IV-0679, IV-0680, IV-0681, IV-0682, IV-0683, IV-0684, IV-0685, IV-0686, IV-0687, IV-0694, IV-1431, IV-1476 | core | plan D04 T07 §8 |  |
| LP-0469 | Capture triggers and output: hotkey, timer with count and countdown, cursor and highlight, to viewer, clipboard, printer, or file with name pattern, beep on save | -- | -- | IV-0688, IV-0689, IV-0690, IV-0691, IV-0692, IV-0693, IV-0695, IV-0696, IV-0697, IV-0698, IV-0699, IV-0700 | core | plan D04 T07 §8 |  |
| LP-0470 | Region capture: capture a rectangle of the screen | -- | -- | IV-1096 | core | plan D04 T07 §8 |  |
| LP-0471 | Import progress tracked, paused, or cancelled in the Activity Manager | -- | AC-0321 | -- | core | plan D04 T11 §1 |  |
| LP-0472 | Completion sound for import | LR-0188 | -- | -- | core | plan D04 T14 §4 |  |
| LP-0473 | Import modes Copy and Add in place | LR-0074, LR-0076 | -- | -- | core | shipped-scope D04 T01 §6 |  |
| LP-0474 | Skip suspected duplicates on import | LR-0092 | -- | -- | core | shipped-scope D04 T01 §6 |  |
| LP-0475 | Import summary: photo count and total size | LR-0124 | -- | -- | core | shipped-scope D04 T01 §6 |  |
| LP-0476 | Tethered capture: sessions, shot folders, naming, destination, metadata, capture bar, remote camera settings, live view, trigger, vendor plug-ins | LR-0106, LR-0173, LR-0174, LR-0175, LR-0176, LR-0177, LR-0178, LR-0179, LR-0180, LR-0181, LR-0182, LR-0183, LR-0184, LR-0185, LR-0186, LR-0187, LR-1389, LR-1629, LR-1630, LR-1648 | -- | -- | core | backlog B-048 | watched-folder auto import (D04 T07 §5) is the tether path meanwhile |

## Metadata and keywords

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0477 | Keyword hierarchy separators when reading metadata | LR-0153 | -- | -- | core | plan D04 T08 §1 |  |
| LP-0478 | Metadata status: up to date, changed on disk, conflict, and resolution badge | LR-0401, LR-0430 | -- | -- | core | plan D04 T08 §1 |  |
| LP-0479 | IPTC Core and IPTC Extension fields: contact, content, image, status, copyright, persons, locations, artwork, models, releases, licensor, digital source type | LR-0413, LR-0414, LR-0415, LR-0416, LR-0417, LR-0418 | AC-0857 | -- | core | plan D04 T08 §1 |  |
| LP-0480 | MWG mapping between IPTC and EXIF fields (description, creator, copyright, date created) and raw parsing display | -- | AC-0375, AC-0860, AC-0861, AC-0862, AC-0863, AC-0864 | -- | core | plan D04 T08 §1 |  |
| LP-0481 | Albumen caption, notes, author, and database date fields stored in the catalog | -- | AC-0856, AC-0866 | -- | core | plan D04 T08 §1 |  |
| LP-0482 | Import IPTC keywords and supplemental categories into Albumen keywords and categories | -- | AC-0891, AC-0892 | -- | core | plan D04 T08 §1 |  |
| LP-0483 | Metadata read from every source: EXIF in JPEG, TIFF, RAW, HEIC, CR3, WebP, PNG; IPTC in TIFF and RAW; XMP | -- | -- | IV-0825, IV-0827, IV-0831 | core | plan D04 T08 §1 |  |
| LP-0484 | EXIF, IPTC, and comment handling for compatible files | -- | -- | IV-1080 | core | plan D04 T08 §1 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0485 | Metadata panel with field sets: default, EXIF, EXIF and IPTC, IPTC, IPTC Extension, large caption, location, minimal, quick describe, customizable default | LR-0383, LR-0384, LR-0386, LR-0387, LR-0388, LR-0389, LR-0390, LR-0391, LR-0392, LR-0393, LR-0395 | -- | -- | core | plan D04 T08 §2 |  |
| LP-0486 | File fields in the metadata panel: rename the file, folder link | LR-0398, LR-0400 | -- | -- | core | plan D04 T08 §2 |  |
| LP-0487 | Basic fields: title, caption, alt text, extended description, rating and label, capture time with milliseconds, original and cropped dimensions | LR-0402, LR-0403, LR-0404, LR-0405, LR-0406, LR-0407, LR-0408 | -- | -- | core | plan D04 T08 §2 |  |
| LP-0488 | EXIF fields: exposure, focal length, ISO, flash, make, model, serial, lens, GPS, altitude, direction, software, user comment | LR-0409, LR-0410, LR-0411, LR-0412 | AC-0858 | -- | core | plan D04 T08 §2 |  |
| LP-0489 | Editing metadata across a selection: mixed values, apply to all selected, keep field while moving to the next photo, Enter applies, Esc discards, Tab navigation, keyword field focus keys | LR-0419 | AC-0876, AC-0879, AC-0880, AC-0881, AC-0882, AC-0883 | -- | core | plan D04 T08 §2 |  |
| LP-0490 | Metadata jump arrows filter the grid to photos sharing a value | LR-0420 | -- | -- | core | plan D04 T08 §2 |  |
| LP-0491 | Show metadata for the target photo only | LR-0431, LR-1469 | -- | -- | core | plan D04 T08 §2 |  |
| LP-0492 | Properties pane in browse for file properties, metadata, and EXIF | -- | AC-0040, AC-4395, AC-4396, AC-4397 | -- | core | plan D04 T08 §2 |  |
| LP-0493 | Properties pane with metadata views: default, all EXIF, all IPTC, Albumen metadata | -- | AC-0852, AC-0855, AC-0935, AC-0936, AC-0937, AC-0938, AC-0940, AC-4940, AC-4966 | -- | core | plan D04 T08 §2 |  |
| LP-0494 | Adjustable metadata field width in the properties pane | -- | AC-0853 | -- | core | plan D04 T08 §2 |  |
| LP-0495 | Custom metadata views: choose fields in a tree, show maker notes, hide rating, label, and categories rows | -- | AC-0854, AC-0859, AC-0941, AC-0942, AC-4190, AC-4191, AC-4192 | -- | core | plan D04 T08 §2 |  |
| LP-0496 | Organize tab: quick access to metadata, categories, collections, keywords, and AI keywords | -- | AC-0865, AC-4400, AC-4429, AC-4603, AC-4939 | -- | core | plan D04 T08 §2 |  |
| LP-0497 | File tab: file information, image attributes, read-only and hidden attributes | -- | AC-0871 | -- | core | plan D04 T08 §2 | file attributes only, never image bytes |
| LP-0498 | Placeholders, sequence numbers, and append mode in metadata fields | -- | AC-0878 | IV-0828, IV-0829 | core | plan D04 T08 §2 | consumes D04 T11 §2 |
| LP-0499 | Add captions while viewing | -- | AC-1855, AC-4428, AC-4596, AC-4945 | -- | core | plan D04 T08 §2 |  |
| LP-0500 | EXIF, IPTC, and comment dialogs from the information dialog | -- | -- | IV-0459, IV-0460, IV-0461 | core | plan D04 T08 §2 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0501 | EXIF information dialog: modeless, updates while browsing, copy lines, choose tags | -- | -- | IV-0820, IV-0821, IV-0822, IV-0823, IV-1433 | core | plan D04 T08 §2 |  |
| LP-0502 | IPTC edit dialog for the current photo and for selected thumbnails | -- | -- | IV-0826, IV-0830, IV-1458 | core | plan D04 T08 §2 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0503 | Comment dialog with Unicode text | -- | -- | IV-0832, IV-0833, IV-1512 | core | plan D04 T08 §2 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0504 | Metadata presets: apply, create, edit, all field groups, shortcut preset, existing-value token, field placeholders, import and export | LR-0396, LR-0397, LR-1457, LR-1473 | AC-0929, AC-0930, AC-0931, AC-0932, AC-0933, AC-0934, AC-4430, AC-4600, AC-4944 | -- | automation | plan D04 T08 §3 |  |
| LP-0505 | Sync metadata, metadata auto sync, copy and paste metadata with chosen fields | LR-0421, LR-0422, LR-0423, LR-1458, LR-1470, LR-1471, LR-1472, LR-1725 | AC-0884, AC-0885 | -- | core | plan D04 T08 §3 |  |
| LP-0506 | Apply IPTC and comment from the first image to a selection | -- | -- | IV-0890 | core | plan D04 T08 §3 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0507 | Edit capture time: specified date, time zone shift, file creation date, revert to original | LR-0424, LR-0426, LR-1474, LR-1475 | -- | -- | core | plan D04 T08 §4 |  |
| LP-0508 | Write capture time changes into raw files | LR-0425 | -- | -- | core | plan D04 T08 §4 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0509 | Batch adjust time stamp: EXIF original, digitized, modified, file dates, catalog date; use another stamp, a specific date, shift to a new start, shift by an offset; wizard options | -- | AC-1015, AC-1016, AC-1017, AC-1018, AC-1019, AC-1020, AC-1021, AC-1022, AC-1023, AC-1024, AC-1025, AC-1026, AC-1027, AC-1028, AC-4503, AC-4670 | -- | automation | plan D04 T08 §4 | file-system dates are file attributes; image bytes unchanged |
| LP-0510 | Edit EXIF date taken | -- | -- | IV-0678 | core | plan D04 T08 §4 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0511 | Edit EXIF date of a selection | -- | -- | IV-0891 | core | plan D04 T08 §4 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0512 | Keyword entry: comma or space separators and auto-complete | LR-0065, LR-0066 | -- | -- | core | plan D04 T08 §5 |  |
| LP-0513 | Keyword shortcut and toggle keyword | LR-0432, LR-0433, LR-1453, LR-1463, LR-1464, LR-1720, LR-1721 | -- | -- | core | plan D04 T08 §5 |  |
| LP-0514 | Purge unused keywords and remove unused IPTC keywords | LR-0434, LR-1480 | AC-0897, AC-0961 | -- | core | plan D04 T08 §5 |  |
| LP-0515 | Import and export keyword lists as tab-indented text, including Lightroom files | LR-0435, LR-1479 | AC-0970, AC-0971, AC-0972 | -- | core | plan D04 T08 §5 |  |
| LP-0516 | Keywording panel: entry modes (keywords, containing keywords, will export) | LR-0439, LR-0440, LR-1454, LR-1718 | -- | -- | core | plan D04 T08 §5 | extends D04 T01 §10 |
| LP-0517 | Keyword suggestions from nearby and similar photos | LR-0441 | -- | -- | core | plan D04 T08 §5 |  |
| LP-0518 | Keyword sets and quick keyword grids: built-in and custom sets, rows and columns, up to 250 keywords, assignment state display, stored as presets | LR-0442, LR-0443, LR-1466, LR-1467, LR-1723, LR-1724 | AC-0964, AC-0965, AC-0966, AC-0967, AC-0968, AC-0969 | -- | core | plan D04 T08 §5 |  |
| LP-0519 | Keyword list panel: counts, text and people filters, check boxes with partial state, multi-select bars, select all, clear, assign and unassign selected, unassign all | LR-0444, LR-0445, LR-0456 | AC-0943, AC-0946, AC-0947, AC-0952, AC-0957, AC-0958, AC-0959, AC-0960, AC-0962 | -- | core | plan D04 T08 §5 |  |
| LP-0520 | Create keyword with synonyms, parent, default parent, apply on creation, and export flags (include, containing keywords, synonyms) | LR-0446, LR-0447, LR-0448, LR-0449, LR-0450, LR-0452, LR-0453, LR-0455 | AC-0945 | -- | core | plan D04 T08 §5 |  |
| LP-0521 | Keyword tree editing: drag to reorganize, merge by rename, delete, edit, copy and paste | LR-0454, LR-0458, LR-0459, LR-1455, LR-1719 | AC-0953, AC-0954, AC-0955, AC-0956 | -- | core | plan D04 T08 §5 |  |
| LP-0522 | Keyword count arrows and browsing by keyword | LR-0457 | AC-0944 | -- | core | plan D04 T08 §5 |  |
| LP-0523 | Organize pane keywords group | -- | AC-0869 | -- | core | plan D04 T08 §5 |  |
| LP-0524 | IPTC keywords picker with a stored value list | -- | AC-0896 | -- | core | plan D04 T08 §5 |  |
| LP-0525 | Hierarchy entry syntax (Child < Parent) in the keyword field | -- | AC-0950 | -- | core | plan D04 T08 §5 |  |
| LP-0526 | Save metadata to file and read metadata from file | LR-0427, LR-0428, LR-1476, LR-1477, LR-1726 | -- | -- | core | plan D04 T08 §8 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9); extends D04 T01 §11 |
| LP-0527 | Update DNG preview and metadata | LR-0429, LR-1478 | -- | -- | format | plan D04 T08 §8 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9); previews refresh in the cache |
| LP-0528 | Embed pending: overlay, search, and embed or clear for catalog metadata not yet written out | -- | AC-0314, AC-0424, AC-4131 | -- | core | plan D04 T08 §8 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0529 | Embed metadata: all or selected files, pending marker and special item, clear pending, options, reminder, on shutdown, network drives, prompts and summary, sidecars for formats without XMP | -- | AC-0872, AC-0873, AC-0874, AC-1778, AC-1779, AC-1780, AC-1781, AC-1782, AC-1783, AC-1784, AC-1790, AC-1791, AC-1792, AC-4229, AC-4230, AC-4231, AC-4232, AC-4238, AC-4240, AC-4241, AC-4242 | -- | core | plan D04 T08 §8 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9); embedding also goes into exported copies |
| LP-0530 | Rebuild catalog records from metadata embedded in files and sidecars | -- | AC-0875, AC-1793 | -- | core | plan D04 T08 §8 |  |
| LP-0531 | Metadata on read-only media refused by name | -- | AC-0877 | -- | core | plan D04 T08 §8 |  |
| LP-0532 | Write keywords and categories to IPTC keywords and supplemental categories with merge or overwrite | -- | AC-0886, AC-0887, AC-0889, AC-0890, AC-1785, AC-1786, AC-1788, AC-1789, AC-4233, AC-4234, AC-4235, AC-4236 | -- | core | plan D04 T08 §8 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0533 | Remove metadata for privacy: EXIF and IPTC, embedded Albumen metadata | -- | AC-0893, AC-0894, AC-0895 | -- | core | plan D04 T08 §8 | applies to exported or converted copies, never the original |
| LP-0534 | Create EXIF data for JPEGs without it | -- | -- | IV-0677 | core | plan D04 T08 §8 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0535 | Assign and unassign keywords by command or by dragging files onto keywords | -- | AC-0948, AC-0949, AC-0951 | -- | core | shipped-scope D04 T01 §10 |  |
| LP-0536 | Content Credentials on export | LR-0438 | -- | -- | cloud | backlog B-047 |  |

## Map and places

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0537 | Map module | LR-0003 | -- | -- | core | plan D04 T08 §6 |  |
| LP-0538 | Map view: markers, clusters with preview, selecting files by pin, zoom, navigator overview, pin legend and map key | LR-1120, LR-1123, LR-1128, LR-1131, LR-1142 | AC-0915, AC-0918, AC-0928 | -- | core | plan D04 T08 §6 | tile source whose terms allow the use, offline basemap fallback |
| LP-0539 | Map styles: road, satellite, terrain, hybrid, light, dark | LR-1121, LR-1534, LR-1839, LR-1840, LR-1841, LR-1842, LR-1843, LR-1844 | AC-0925 | -- | cloud | plan D04 T08 §6 | user-configurable tile sources |
| LP-0540 | Search places by name on the map | LR-1122, LR-1837 | AC-0924 | -- | cloud | plan D04 T08 §6 | offline gazetteer |
| LP-0541 | Map overlays and locks: lock markers, info overlay, saved-location overlay | LR-1124, LR-1125, LR-1135, LR-1533, LR-1535, LR-1845, LR-1846, LR-1847 | -- | -- | core | plan D04 T08 §6 |  |
| LP-0542 | Map filter bar and location filter | LR-1126, LR-1130 | -- | -- | core | plan D04 T08 §6 |  |
| LP-0543 | Geotag by dragging photos onto the map, save locations, refresh pins | LR-1127 | AC-0917, AC-0919, AC-0920 | -- | core | plan D04 T08 §6 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0544 | Delete GPS coordinates, remove from map, view on map | LR-1129, LR-1532, LR-1838 | AC-0922, AC-0923 | -- | core | plan D04 T08 §6 |  |
| LP-0545 | Saved locations with radius | LR-1132, LR-1134 | -- | -- | core | plan D04 T08 §6 |  |
| LP-0546 | Metadata panel in the map view | LR-1136 | -- | -- | core | plan D04 T08 §6 |  |
| LP-0547 | Map pane showing and marking locations of selected files | -- | AC-0041, AC-4476 | -- | core | plan D04 T08 §6 |  |
| LP-0548 | Formats that can be placed on the map, default map location, and geotags kept independent of develop reset | -- | AC-0916, AC-0921, AC-0926 | -- | core | plan D04 T08 §6 |  |
| LP-0549 | Open the photo GPS position in an external map (Google Earth, Google Maps) | -- | -- | IV-0757, IV-0758, IV-1463, IV-1510 | core | plan D04 T08 §6 | opens the user browser or app |
| LP-0550 | Show a photo location in the map view or a user-chosen web map | -- | -- | IV-0824 | core | plan D04 T08 §6 |  |
| LP-0551 | Reverse geocoding: fill city, state, country, and country code from GPS as suggestions | LR-0436, LR-0437, LR-1141 | AC-0927 | -- | cloud | plan D04 T08 §7 | offline GeoNames data, no online lookup |
| LP-0552 | Private saved locations remove GPS on export | LR-1133 | -- | -- | core | plan D04 T08 §7 |  |
| LP-0553 | Tracklogs: load GPX, auto-tag photos by capture time, time zone offset, next and previous track | LR-1137, LR-1138, LR-1139, LR-1140, LR-1531, LR-1835, LR-1836 | -- | -- | core | plan D04 T08 §7 |  |

## Develop: workspace, history, and presets

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0554 | Original or smart preview indicator under the histogram | LR-0661 | -- | -- | core | plan D04 T06 §11 |  |
| LP-0555 | Apply a develop preset on import | LR-0990 | -- | -- | automation | plan D04 T07 §3 |  |
| LP-0556 | Develop histogram with camera info and drag-to-adjust tone regions | LR-0653, LR-0654 | AC-4965, AC-4975 | -- | core | plan D04 T09 §1 | extends D04 T02 §3 |
| LP-0557 | Pixel value readouts: RGB under the pointer in percent, 0 to 255, or Lab, with original and edited values | LR-0659 | AC-2133 | -- | core | plan D04 T09 §1 |  |
| LP-0558 | Tool strip and edit mode switcher for crop, remove, red eye, masking, and lens blur | LR-0662, LR-0663, LR-1526 | -- | -- | core | plan D04 T09 §1 |  |
| LP-0559 | Before and after modes: left and right split, top and bottom, top and bottom split, draggable split view | LR-0665, LR-0666, LR-0667, LR-1495, LR-1786, LR-1787, LR-1788, LR-1789 | AC-2121, AC-4957 | -- | core | plan D04 T09 §1 |  |
| LP-0560 | Reference view with a locked reference photo, left and right or top and bottom | LR-0671, LR-0672 | -- | -- | core | plan D04 T09 §1 |  |
| LP-0561 | Develop zoom and navigator: fit, fill, 1:1, ratios, zoom slider and preset list | LR-0673, LR-1784, LR-1785, LR-1799 | AC-2105, AC-2119, AC-2120, AC-2122, AC-2123, AC-4949, AC-4950, AC-4951, AC-4952, AC-4953, AC-4954, AC-4955, AC-4958, AC-4960, AC-4984 | -- | core | plan D04 T09 §1 | extends D04 T01 §9 |
| LP-0562 | Develop view options: loupe info overlay and messages | LR-0674, LR-1793 | -- | -- | core | plan D04 T09 §1 |  |
| LP-0563 | Collections panel inside Develop | LR-0685 | -- | -- | core | plan D04 T09 §1 |  |
| LP-0564 | Scrubby numeric value fields | LR-0708 | -- | -- | core | plan D04 T09 §1 |  |
| LP-0565 | Develop grid, guides, and layout overlays, alignment grid, and pin and overlay visibility modes | LR-0725, LR-0726 | AC-2546 | -- | core | plan D04 T09 §1 |  |
| LP-0566 | Develop panel organization: tabs and groups, segmented sections, solo and auto-collapse, expand and collapse all, per-panel eye toggle, changed-tab markers, detachable panes, Basic slider cycling | LR-0753, LR-0754, LR-0755 | AC-0135, AC-2065, AC-2066, AC-2067, AC-2068, AC-2070, AC-2111, AC-2126, AC-2127, AC-2128, AC-2129, AC-2206, AC-2345, AC-2514, AC-2527, AC-2544, AC-4947, AC-4948, AC-4961, AC-4962, AC-4963, AC-4969, AC-4988, AC-4989, AC-4990, AC-4991, AC-4993 | -- | core | plan D04 T09 §1 |  |
| LP-0567 | Develop filmstrip, previous and next photo, and fullscreen in develop | -- | AC-2115, AC-2116, AC-2117, AC-2118, AC-2124, AC-2125, AC-2130, AC-2204, AC-2205, AC-4921, AC-4922, AC-4927, AC-4928, AC-4956, AC-4967 | -- | core | plan D04 T09 §1 | extends D04 T01 §9 |
| LP-0568 | Undo and redo buttons shown at the top of the develop tools pane (option) | -- | AC-4284 | -- | core | plan D04 T09 §1 |  |
| LP-0569 | Before state control: copy after to before, before to after, swap, set before from a history step or snapshot | LR-0669, LR-0670, LR-1737, LR-1738, LR-1739 | -- | -- | core | plan D04 T09 §2 |  |
| LP-0570 | Hover preview of history steps and snapshots, Shift pauses live preview | LR-0675 | -- | -- | core | plan D04 T09 §2 | preset hover preview is shipped in D04 T02 §5 |
| LP-0571 | Snapshot management: update with current settings, rename, delete, create from a history step | LR-0679, LR-0680, LR-0684 | -- | -- | core | plan D04 T09 §2 |  |
| LP-0572 | Clear history and undo all | LR-0683 | AC-2132 | -- | core | plan D04 T09 §2 |  |
| LP-0573 | Per-group reset and settings menu: reset to last saved, default, or last used, save group preset, copy and paste group | LR-1744 | AC-2079, AC-2109, AC-2112, AC-2113, AC-2225, AC-2449, AC-2525, AC-2526 | -- | core | plan D04 T09 §2 |  |
| LP-0574 | Snapshots toolbar in the viewer to switch between saved adjustment states | -- | AC-0113 | -- | core | plan D04 T09 §2 | extends D04 T02 §1 |
| LP-0575 | Restore to original: remove develop settings from one or many photos | -- | AC-0132, AC-0690, AC-1953, AC-1956, AC-2201 | -- | core | plan D04 T09 §17 |  |
| LP-0576 | Done, save, discard, and cancel when leaving develop, with Esc to cancel | -- | AC-0140, AC-2080, AC-2081, AC-2083, AC-2084, AC-2091, AC-2346, AC-2348, AC-2349, AC-2355, AC-4923, AC-4929 | -- | core | plan D04 T09 §17 | save writes the catalog and sidecar, never the original |
| LP-0577 | Developed badge on thumbnails and in the viewer status bar | -- | AC-1950 | -- | core | plan D04 T09 §2 |  |
| LP-0578 | Commit changes: make the developed or edited version the file | -- | AC-2021, AC-4659 | -- | core | plan D04 T09 §17 | a new file with the settings baked in by default; into the original only when the user opts in, after a verified backup (D04 T11 §1) |
| LP-0579 | Save develop state as a rendered new file: save as, save a copy, preserve metadata, catalog information, settings, and embedded profile | -- | AC-2082, AC-2087, AC-2088, AC-2092, AC-2094, AC-2095, AC-2096, AC-2097, AC-2347, AC-2351, AC-2352, AC-2356, AC-4924 | -- | core | plan D04 T09 §17 | writes a new file, never the original |
| LP-0580 | Automatic saving of develop adjustments when switching photos, with background saving for fast RAW switching | -- | AC-2085, AC-2086, AC-2098, AC-2350, AC-4282, AC-4283 | -- | core | plan D04 T09 §17 |  |
| LP-0581 | Copy the developed image to the clipboard | -- | AC-2090, AC-2354 | -- | core | plan D04 T09 §17 |  |
| LP-0582 | Develop settings mirrored to the XMP sidecar for RAW and rendered formats, never the original | -- | AC-2099, AC-2100, AC-2197 | -- | core | plan D04 T09 §17 | consumes D01 T07 §6; sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9); originals are never moved to an [Originals] folder |
| LP-0583 | Snapshot badges on thumbnails, snapshot preview in the viewer, return to last used settings | -- | AC-2210, AC-2211, AC-2212 | -- | core | plan D04 T09 §2 |  |
| LP-0584 | Targeted adjustment by dragging on the image for curves and color mixer | LR-0709, LR-0761, LR-1528, LR-1775, LR-1776, LR-1777, LR-1778, LR-1779, LR-1780 | AC-2274, AC-2408 | -- | core | plan D04 T09 §4 |  |
| LP-0585 | Process versions: choose a version and update to the current process | LR-0700, LR-0701, LR-0835, LR-1518 | -- | -- | core | plan D04 T09 §7 | consumes D01 T07 §1 |
| LP-0586 | Develop defaults: reset to Albumen default, set default settings globally or per camera and ISO, raw defaults, save new sharpening and noise defaults | LR-0688, LR-0689, LR-0993, LR-1517 | AC-2522, AC-2533 | -- | core | plan D04 T09 §11 | consumes D01 T07 §6 |
| LP-0587 | Preset amount slider and stacking of several presets | LR-0977 | AC-2134 | -- | core | plan D04 T09 §11 |  |
| LP-0588 | Preset management: create with a settings checklist, update, rename, delete, move, groups and categories, manage dialog | LR-0978, LR-0979, LR-0980, LR-0982, LR-0988, LR-0989, LR-1515, LR-1516, LR-1791, LR-1792 | AC-2135, AC-2136, AC-2137, AC-2138, AC-2141, AC-2142, AC-2143, AC-2152 | -- | core | plan D04 T09 §11 | extends D04 T02 §5; consumes D01 T07 §6 |
| LP-0589 | Import and export presets (XMP, ZIP, and Albumen files) with tree selection | LR-0981 | AC-2139, AC-2140, AC-2153, AC-2154, AC-2155 | -- | core | plan D04 T09 §11 | consumes D01 T07 §6 crs XMP exchange |
| LP-0590 | Preset visibility: filter by name, show partially compatible presets, store presets with the catalog, restore built-in presets | LR-0983, LR-0991, LR-0992, LR-0994 | -- | -- | core | plan D04 T09 §11 |  |
| LP-0591 | Bundled preset sets and categories (film, cinematic, moody, and similar) | LR-0986, LR-0987 | AC-2144 | -- | core | plan D04 T09 §11 | Albumen ships its own presets; no Adobe or ACDSee presets are bundled |
| LP-0592 | Preset visibility, raw defaults per camera and serial, and the presets folder | LR-1348, LR-1349, LR-1350 | -- | -- | core | plan D04 T09 §11 |  |
| LP-0593 | Apply presets from the filmstrip, library, and viewer | -- | AC-1954, AC-1957, AC-2150 | -- | core | plan D04 T09 §11 |  |
| LP-0594 | Global, tab, and group scoped presets with select-all in the save dialog, and last-used settings preset | -- | AC-1955, AC-2146, AC-2147, AC-2148, AC-2149 | -- | core | plan D04 T09 §11 |  |
| LP-0595 | Share develop settings as files: export and import per-photo settings files | -- | AC-2196, AC-2198, AC-2199, AC-2200 | -- | core | plan D04 T09 §11 | Albumen writes XMP settings files beside the photo, never into the original |
| LP-0596 | Sync snapshots across selected photos | LR-0681, LR-1525 | -- | -- | core | plan D04 T09 §12 |  |
| LP-0597 | Paste settings from the previous photo and the Previous button | LR-0686, LR-0692, LR-1736 | -- | -- | core | plan D04 T09 §12 |  |
| LP-0598 | Copy settings subsets: saved custom subsets and only modified settings | LR-0693 | -- | -- | automation | plan D04 T09 §12 |  |
| LP-0599 | Sync without dialog, auto sync, and match total exposures | LR-0697, LR-0698, LR-0699, LR-1523, LR-1524, LR-1747, LR-1748, LR-1749, LR-1750 | -- | -- | core | plan D04 T09 §12 |  |
| LP-0600 | Develop settings commands from the library and viewer: copy, paste, restore, and the develop settings summary pane | LR-0710, LR-1456 | AC-0687, AC-0688, AC-0689, AC-1949, AC-1951, AC-1952, AC-2213, AC-4661, AC-4662 | -- | core | plan D04 T09 §12 |  |
| LP-0601 | Pasted settings scale to targets of different dimensions | -- | AC-2207 | -- | core | plan D04 T09 §12 |  |
| LP-0602 | Soft proofing: proof profile and intent, simulate paper and ink, monitor and destination gamut warnings, proof copy, proof background | LR-0717, LR-0718, LR-0719, LR-0720, LR-0721, LR-0722, LR-0723, LR-0724, LR-1497, LR-1801, LR-1802 | AC-4946 | -- | print | plan D04 T09 §15 | consumes D01 T04 §2 |
| LP-0603 | Soft proofing toggle with emulated device profile and rendering intents | -- | AC-4207, AC-4208, AC-4209, AC-4210, AC-4211, AC-4212 | -- | print | plan D04 T09 §15 | consumes D01 T04 §2 |
| LP-0604 | Clipping indicators and Alt-drag threshold clipping preview | LR-0655, LR-0656, LR-0657, LR-0658, LR-1494, LR-1781 | AC-2106, AC-4985 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0605 | Before and after: side by side and show-before toggle | LR-0664, LR-0668 | AC-2114, AC-4959, AC-4964 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0606 | Develop presets panel with groups and hover preview | LR-0676 | AC-4973 | -- | automation | shipped-scope D04 T02 §5 |  |
| LP-0607 | Snapshots panel and new snapshot | LR-0677, LR-0678, LR-1514, LR-1790 | AC-2208, AC-2209, AC-4970, AC-4992 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0608 | History panel listing each step with values, click to revert | LR-0682 | AC-2131, AC-4974 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0609 | Reset all develop settings | LR-0687, LR-1519, LR-1745 | AC-2110 | -- | core | shipped-scope D04 T02 §1 |  |
| LP-0610 | Copy and paste develop settings with a settings-group checklist | LR-0690, LR-0691, LR-0694, LR-1522, LR-1735 | AC-2202, AC-2203, AC-4932, AC-4933 | -- | core | shipped-scope D04 T02 §5 |  |
| LP-0611 | Sync settings to the selection | LR-0696, LR-1746 | -- | -- | core | shipped-scope D04 T02 §5 |  |
| LP-0612 | Slider controls: live feedback, arrow-key nudges, double-click and Alt-click group reset, right-click reset | LR-0706, LR-0707, LR-1740, LR-1741, LR-1742, LR-1743 | AC-2215, AC-2344, AC-4994, AC-4995, AC-4996, AC-4997, AC-4998 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0613 | Apply a preset on click with hover preview | LR-0976 | -- | -- | automation | shipped-scope D04 T02 §5 |  |
| LP-0614 | Develop settings are data stored apart from the original and reapplied on open | -- | AC-0131, AC-2064, AC-2069, AC-2093 | -- | core | shipped-scope D04 T02 §1 |  |
| LP-0615 | Undo and redo in develop | -- | AC-2107, AC-2108, AC-4930, AC-4931 | -- | core | shipped-scope D04 T02 §1 |  |

## Develop: tone, color, and detail

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0616 | HDR editing: edit in HDR, visualize HDR ranges, HDR limit, SDR preview and rendition, extended HDR histogram and curve range, HDR by default | LR-0660, LR-0711, LR-0712, LR-0713, LR-0714, LR-0715, LR-0716, LR-0763 | -- | -- | core | plan D04 T09 §3 | consumes D01 T07 §1 and the HDR display path of D03 T15 §4 |
| LP-0617 | Treatment: color or black and white | LR-0727, LR-1521, LR-1732 | -- | -- | core | plan D04 T09 §3 |  |
| LP-0618 | Profile browser: profile groups, favorites, grid and list views, creative profile amount, import DCP and LUT-based profiles | LR-0728, LR-0729, LR-0731, LR-0732, LR-0733, LR-0734 | -- | -- | core | plan D04 T09 §3 | consumes D01 T07 §1; Adobe and camera-matching profiles are not bundled, users import the DCP files they own |
| LP-0619 | White balance picker with loupe and neutral-pixel highlighting, and white balance strength | LR-0735, LR-1527, LR-1751 | AC-2358, AC-2371, AC-2372 | -- | core | plan D04 T09 §3 |  |
| LP-0620 | Texture, clarity, and dehaze | LR-0745, LR-0746, LR-0747 | AC-2077, AC-2078 | -- | core | plan D04 T09 §3 | consumes D01 T07 §2 |
| LP-0621 | Auto tone, auto white balance, and per-slider auto values | LR-0750, LR-0751, LR-0752, LR-1520, LR-1733, LR-1734 | -- | -- | core | plan D04 T09 §3 | classical analysis; AI auto settings are D04 T10 §11 |
| LP-0622 | Output color space for RAW with a default and embedded profile | -- | AC-2511, AC-2512, AC-2513 | -- | core | plan D04 T09 §3 | extends D04 T02 §2 output transform |
| LP-0623 | Tone curve extensions: per-channel curves, curve presets, refine saturation, point readout, black, midtone, and white points with auto, camera or standard base curve, click-to-add point picker | LR-0758, LR-0759, LR-0760, LR-0762 | AC-2439, AC-2440, AC-2441, AC-2442, AC-2443, AC-2444, AC-2445, AC-2446, AC-2447, AC-2448 | -- | core | plan D04 T09 §4 |  |
| LP-0624 | Color mixer: HSL and per-color modes over eight bands with an all view | LR-0764, LR-0765, LR-0766 | -- | -- | core | plan D04 T09 §4 | consumes D01 T07 §2 |
| LP-0625 | Black and white mix with auto mix, and ACDSee advanced black and white with contrast and colorization | LR-0767, LR-0768 | AC-2412, AC-2413, AC-2414, AC-2415, AC-2416 | -- | core | plan D04 T09 §4 |  |
| LP-0626 | Point color: sampled swatches with hue, saturation, and luminance shift, variance, range, visualize range, and use inside masks | LR-0769, LR-0770, LR-0771, LR-0772, LR-0773, LR-0774, LR-0775 | -- | -- | core | plan D04 T09 §4 | consumes D01 T07 §2 |
| LP-0627 | Color grading: three-way and global wheels, single wheel views, luminance, blending, balance, fine wheel control | LR-0776, LR-0777, LR-0778, LR-0779, LR-0780, LR-0781, LR-0782, LR-0783 | -- | -- | core | plan D04 T09 §4 | consumes D01 T07 §2 |
| LP-0628 | Color EQ: per-color saturation, brightness, hue, and contrast in high-quality and standard modes with global slider and curve | -- | AC-2401, AC-2402, AC-2403, AC-2404, AC-2405, AC-2406, AC-2407, AC-2409, AC-2410, AC-2411 | -- | core | plan D04 T09 §4 |  |
| LP-0629 | Color wheel: targeted hue range edits with saturation range, invert, mask preview, smoothness, and several wheels | -- | AC-2417, AC-2418, AC-2419, AC-2420, AC-2421, AC-2422, AC-2423, AC-2424, AC-2425, AC-2426, AC-2427, AC-2428, AC-2429, AC-2430, AC-2431, AC-2432, AC-2433 | -- | core | plan D04 T09 §4 |  |
| LP-0630 | Tone wheels: shadow, midtone, and highlight tint with eyedroppers, saturation, and brightness | -- | AC-2434, AC-2435, AC-2436, AC-2437, AC-2438 | -- | core | plan D04 T09 §4 |  |
| LP-0631 | Split tone: highlight and shadow hue and saturation with balance | -- | AC-2500, AC-2501, AC-2502, AC-2503, AC-2504, AC-2505 | -- | core | plan D04 T09 §4 | maps onto D01 T07 §2 color grading |
| LP-0632 | Sharpening: amount, radius, detail, masking with Alt mask view, threshold | LR-0784, LR-0785, LR-0786, LR-0787 | AC-2516, AC-2517, AC-2518, AC-2519, AC-2520, AC-2521 | -- | core | plan D04 T09 §5 | consumes D01 T07 §3 |
| LP-0633 | Detail zoom preview window with a movable target | LR-0788 | AC-2515 | -- | core | plan D04 T09 §5 |  |
| LP-0634 | Noise reduction: luminance with detail and contrast, color with detail and smoothness, strength, tonal and frequency range, legacy compatibility | LR-0789, LR-0790, LR-0791 | AC-2523, AC-2524, AC-2528, AC-2529, AC-2530, AC-2531, AC-2532 | -- | core | plan D04 T09 §5 | consumes D01 T07 §3 |
| LP-0635 | Auto Light EQ preview toggle in the viewer | -- | AC-0111, AC-4645 | -- | core | plan D04 T09 §13 | consumes D01 T07 §7 |
| LP-0636 | Light EQ instant view in the viewer | -- | AC-1860 | -- | core | plan D04 T09 §13 |  |
| LP-0637 | Light EQ tone equalizer: basic, standard, and advanced modes, tone bands, graph, brighten and darken amplitudes, auto, click and wheel adjustments on the image | -- | AC-2373, AC-2374, AC-2375, AC-2376, AC-2377, AC-2378, AC-2379, AC-2380, AC-2381, AC-2382, AC-2383, AC-2384, AC-2385, AC-2386, AC-2387, AC-2388, AC-2389, AC-2390, AC-2391, AC-2392, AC-2393, AC-2394, AC-2395, AC-2396, AC-2397, AC-2398, AC-2399, AC-2400 | -- | core | plan D04 T09 §13 | stage built by D01 T07 §7 in Isotone.Core |
| LP-0638 | Soft focus: strength, brightness, contrast, tonal width | -- | AC-2450, AC-2451, AC-2452, AC-2453, AC-2454 | -- | core | plan D04 T09 §13 | stage built by D01 T07 §8 |
| LP-0639 | Skin tune: smoothing, glow, radius | -- | AC-2534, AC-2535, AC-2536, AC-2537 | -- | core | plan D04 T09 §13 | stage built by D01 T07 §8 |
| LP-0640 | Develop effects: photo effect looks, color overlay, gradient map, cross process, effect opacity and blend mode | -- | AC-2455, AC-2456, AC-2457, AC-2458, AC-2459, AC-2460, AC-2461, AC-2462, AC-2466 | -- | core | plan D04 T09 §14 | stage built by D01 T07 §9 |
| LP-0641 | Develop blend modes: normal, screen, multiply, dodge, burn, overlay, difference, darken, lighten, hard and soft light, hue, saturation, color, luminosity, dissolve, exclusion, vivid, pin, linear light, hard mix, subtract, divide, darker and lighter color | -- | AC-2467, AC-2468, AC-2469, AC-2470, AC-2471, AC-2472, AC-2473, AC-2474, AC-2475, AC-2476, AC-2477, AC-2478, AC-2479, AC-2480, AC-2481, AC-2482, AC-2483, AC-2484, AC-2485, AC-2486, AC-2487, AC-2488, AC-2489, AC-2490, AC-2491 | -- | core | plan D04 T09 §14 | stage built by D01 T07 §9 |
| LP-0642 | Color LUTs in develop: .cube and .3dl import, remove, refresh, apply from a list | -- | AC-2492, AC-2493, AC-2494, AC-2495, AC-2496, AC-2497, AC-2498, AC-2499 | -- | core | plan D04 T09 §14 | stage built by D01 T07 §9 |
| LP-0643 | White balance presets, temperature, and tint | LR-0736, LR-0737, LR-0738 | AC-2357, AC-2359, AC-2360, AC-2361, AC-2362, AC-2363, AC-2364, AC-2365, AC-2366, AC-2367, AC-2368, AC-2369, AC-2370 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0644 | Basic tone: exposure, contrast, highlights, shadows, whites, blacks, highlight enhancement, fill light | LR-0739, LR-0740, LR-0741, LR-0742, LR-0743, LR-0744 | AC-2071, AC-2072, AC-2073, AC-2074 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0645 | Vibrance and saturation | LR-0748, LR-0749 | AC-2075, AC-2076 | -- | core | shipped-scope D04 T02 §3 |  |
| LP-0646 | Parametric and point tone curves | LR-0756, LR-0757 | -- | -- | core | shipped-scope D04 T02 §3 |  |

## Develop: lens, geometry, effects, and crop

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0647 | Remove chromatic aberration by profile or automatically | LR-0800 | AC-2558 | -- | core | plan D04 T09 §6 |  |
| LP-0648 | Lens profile corrections: enable, auto or custom make, model, and profile, distortion and vignetting amounts, built-in profiles, saved lens defaults and mapped defaults with auto-apply | LR-0801, LR-0802, LR-0803, LR-0804, LR-0809 | AC-2547, AC-2548, AC-2549, AC-2550, AC-2551, AC-2553, AC-2554, AC-2555, AC-2556, AC-2557 | -- | core | plan D04 T09 §6 | consumes D01 T07 §3 and the lensfun and LCP reader |
| LP-0649 | Manual lens corrections: distortion with constrain crop, lens vignetting amount and midpoint, vignette correction strength and radius | LR-0805, LR-0808 | AC-2552, AC-2583, AC-2584, AC-2585 | -- | core | plan D04 T09 §6 |  |
| LP-0650 | Defringe: purple and green amount and hue, fringe picker, red and cyan and blue and yellow shifts, defringe strength, radius, and color | LR-0806, LR-0807 | AC-2538, AC-2539, AC-2540, AC-2541, AC-2542, AC-2543 | -- | core | plan D04 T09 §6 |  |
| LP-0651 | Flat-field correction from a reference frame | LR-0840, LR-0841 | -- | -- | automation | plan D04 T09 §6 | writes a new DNG, never the original |
| LP-0652 | Auto Lens preview filters in the viewer, optionally restored at startup | -- | AC-0112, AC-4255 | -- | core | plan D04 T09 §6 |  |
| LP-0653 | DNG geometric distortion tags applied automatically | -- | AC-2545 | -- | format | plan D04 T09 §6 |  |
| LP-0654 | Upright: off, auto, level, vertical, full, reanalyze, cycle modes | LR-0810, LR-0811, LR-0812, LR-0813, LR-0814, LR-0824, LR-0825, LR-1805 | -- | -- | core | plan D04 T09 §7 | consumes D01 T07 §3 |
| LP-0655 | Guided upright with up to four guides and a loupe | LR-0815, LR-0816, LR-1760 | -- | -- | core | plan D04 T09 §7 |  |
| LP-0656 | Transform sliders: vertical, horizontal, rotate, aspect, scale, offset, shear, constrain crop | LR-0817, LR-0818, LR-0819, LR-0820, LR-0821, LR-0822, LR-0823 | AC-2566, AC-2567, AC-2568, AC-2569, AC-2570 | -- | core | plan D04 T09 §7 |  |
| LP-0657 | Calibration: shadows tint and red, green, and blue primary hue and saturation | LR-0836, LR-0837, LR-0838, LR-0839 | -- | -- | core | plan D04 T09 §7 | consumes D01 T07 §2 |
| LP-0658 | Rotate 90 degrees and nudge by 5 degrees in develop | LR-1782, LR-1783 | AC-2559, AC-2560, AC-2561, AC-2563, AC-2564 | -- | core | plan D04 T09 §7 |  |
| LP-0659 | Perspective correction (the bundled perspective transformation filter) | -- | -- | IV-0608 | core | plan D04 T09 §7 |  |
| LP-0660 | Post-crop vignette: style, amount, midpoint, roundness, feather, highlights | LR-0826, LR-0827, LR-0828, LR-0829, LR-0830, LR-0831 | AC-2506, AC-2507, AC-2508, AC-2509, AC-2510 | -- | core | plan D04 T09 §8 | consumes D01 T07 §3 |
| LP-0661 | Grain: amount, size, roughness, smoothing | LR-0832, LR-0833, LR-0834 | AC-2463, AC-2464, AC-2465 | -- | core | plan D04 T09 §8 | consumes D01 T07 §3 |
| LP-0662 | Crop extensions: custom ratios, previous ratio, crop from center, auto straighten, constrain to image, reset and crop to original | LR-0844, LR-0846, LR-0848, LR-0851, LR-0852, LR-0863, LR-0864, LR-1753, LR-1754, LR-1755, LR-1759, LR-1796 | AC-4987 | -- | core | plan D04 T09 §8 | extends D04 T02 §4 |
| LP-0663 | Crop guide overlays: thirds, grid, diagonal, triangle, golden ratio, golden spiral, aspect frames, cycling, show mode, outside opacity | LR-0853, LR-0854, LR-0855, LR-0856, LR-0857, LR-0858, LR-0859, LR-0860, LR-0861, LR-0862, LR-0865, LR-1529, LR-1756, LR-1757 | AC-4986 | -- | core | plan D04 T09 §8 |  |
| LP-0664 | Exact crop size: width and height, units, resolution, constrain proportion list with defaults, maximize, rotate crop, arrow-key resize, preview cropped | -- | AC-2572, AC-2573, AC-2574, AC-2575, AC-2576, AC-2577, AC-2578, AC-2579, AC-2580, AC-2581, AC-2582 | -- | core | plan D04 T09 §8 |  |
| LP-0665 | Crop overlay, aspect presets, swap orientation, straighten, and angle | LR-0842, LR-0843, LR-0845, LR-0847, LR-0849, LR-0850, LR-1752, LR-1758 | AC-2571 | -- | core | shipped-scope D04 T02 §4 |  |
| LP-0666 | Straighten slider and straighten tool | -- | AC-2562, AC-2565 | -- | core | shipped-scope D04 T02 §4 |  |

## Develop: masking and retouching

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0667 | Delete empty masks | LR-0702, LR-0926 | -- | -- | core | plan D04 T09 §9 |  |
| LP-0668 | Masking tool and masking group with local adjustments | LR-0896, LR-1800 | AC-2214 | -- | core | plan D04 T09 §9 | consumes D01 T07 §4 |
| LP-0669 | Brush masks: A and B brushes and eraser, size, feather, flow, density, pressure, straight lines, faster brushing, delete strokes | LR-0906, LR-0907, LR-0909, LR-0910, LR-0911, LR-0957, LR-1763, LR-1766, LR-1767, LR-1768, LR-1769, LR-1770 | AC-2220, AC-2227, AC-2228, AC-2232, AC-2255, AC-2258, AC-2259, AC-2260, AC-2261, AC-2262, AC-4983, AC-4999, AC-5000 | -- | core | plan D04 T09 §9 |  |
| LP-0670 | Auto mask and smart brushing by color, brightness, or both, with tolerance and several brushes | LR-0908 | AC-2229, AC-2230, AC-2280, AC-2281, AC-2282, AC-2283, AC-2284, AC-2285, AC-2286, AC-2287, AC-2288 | -- | core | plan D04 T09 §9 |  |
| LP-0671 | Linear gradient masks with guides and 45 degree lock | LR-0912, LR-1764 | AC-2221, AC-2289, AC-2290, AC-2291 | -- | core | plan D04 T09 §9 |  |
| LP-0672 | Radial gradient masks with feather, squareness, circle constraint, invert, and expand to image | LR-0913, LR-0914, LR-1794 | AC-2222, AC-2295, AC-2296, AC-2297, AC-2298, AC-2301 | -- | core | plan D04 T09 §9 |  |
| LP-0673 | Brush editing of gradient masks and converting a gradient into a brush mask | LR-0915, LR-1765 | AC-2226 | -- | core | plan D04 T09 §9 |  |
| LP-0674 | Color range and luminance range masks with refine, smoothness, luminance map, and add detail | LR-0916, LR-0917, LR-1795, LR-1797 | AC-2223, AC-2224, AC-2302, AC-2303, AC-2304, AC-2305, AC-2310, AC-2311, AC-2312 | -- | core | plan D04 T09 §9 |  |
| LP-0675 | Mask set operations: add, subtract, intersect, invert, duplicate and invert, duplicate, rename, hide, delete, enable, clear, up to 24 masks, drag components between masks | LR-0919, LR-0920, LR-0921, LR-0922, LR-0923, LR-0924, LR-0925, LR-0930 | AC-2234, AC-2235, AC-2236, AC-2241, AC-2242, AC-2243, AC-2244 | -- | core | plan D04 T09 §9 |  |
| LP-0676 | Mask refinement: feather and edge shift | LR-0928, LR-0929 | AC-2233, AC-2307, AC-2308, AC-2314, AC-2315 | -- | core | plan D04 T09 §9 |  |
| LP-0677 | Masks panel: dock or float, auto hide, component badges | LR-0931, LR-0932, LR-0933 | -- | -- | core | plan D04 T09 §9 |  |
| LP-0678 | Mask overlay: show overlay with color, overlay modes and cycling, pin visibility, hover to reveal strokes | LR-0934, LR-0935, LR-0936, LR-0937, LR-1772, LR-1773, LR-1774, LR-1798 | AC-2231, AC-2256, AC-2257, AC-2263, AC-2292, AC-2299, AC-2306, AC-2313 | -- | core | plan D04 T09 §9 |  |
| LP-0679 | Local adjustment set: amount, temperature, tint, tone, presence, hue, saturation, vibrance, fill light, color tint, color EQ, curve, point color, sharpness, noise, moire, defringe, grain | LR-0938, LR-0940, LR-0941, LR-0942, LR-0943, LR-0944, LR-0945, LR-0946, LR-0947, LR-0948, LR-0949, LR-0950, LR-0951, LR-0952, LR-0953, LR-1771 | AC-2246, AC-2247, AC-2264, AC-2265, AC-2266, AC-2267, AC-2268, AC-2269, AC-2270, AC-2271, AC-2272, AC-2273, AC-2275, AC-2276, AC-2277, AC-2278, AC-2279, AC-2293, AC-2294, AC-2300, AC-2309, AC-2316 | -- | core | plan D04 T09 §9 | consumes D01 T07 §4 |
| LP-0680 | Local adjustment presets | LR-0939 | -- | -- | automation | plan D04 T09 §9 |  |
| LP-0681 | Copy, paste, and duplicate masks between photos | LR-0956, LR-1806 | AC-2237, AC-2238, AC-2239, AC-2240 | -- | core | plan D04 T09 §9 |  |
| LP-0682 | Pixel targeting: restrict a local adjustment by tone and color with tone grabber, color wheels, invert, smoothness, add detail, skin targeting, and presets | -- | AC-2245, AC-2317, AC-2318, AC-2319, AC-2320, AC-2321, AC-2322, AC-2323, AC-2324, AC-2325, AC-2326, AC-2327, AC-2328, AC-2329, AC-2330, AC-2331, AC-2332, AC-2333, AC-2334, AC-2335, AC-2336, AC-2337, AC-2338, AC-2339, AC-2340, AC-2341, AC-2342, AC-2343 | -- | core | plan D04 T09 §9 | maps onto D01 T07 §4 range components |
| LP-0683 | Remove tool with heal and clone modes: size, feather, opacity, source sampling and refresh, stroke-shaped spots, toggle mode, skip auto fill | LR-0866, LR-0875, LR-0876, LR-0877, LR-0878, LR-0879, LR-0880, LR-0881, LR-0882, LR-0883, LR-0886, LR-1761, LR-1762 | -- | -- | core | plan D04 T09 §10 | consumes D01 T07 §5 |
| LP-0684 | Content-aware remove mode | LR-0867 | -- | -- | core | plan D04 T09 §10 | consumes D01 T07 §5 through the content-aware provider seam |
| LP-0685 | Visualize spots and tool overlay modes | LR-0884, LR-0885, LR-1530, LR-1803, LR-1804 | -- | -- | core | plan D04 T09 §10 |  |
| LP-0686 | Red eye and pet eye correction with pupil size, darken, and catchlight | LR-0892, LR-0893, LR-0894, LR-0895 | -- | -- | core | plan D04 T09 §10 | consumes D01 T07 §5 |

## Photo merge

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0687 | HDR merge with auto align, auto settings, deghost amount and overlay, stack with sources, floating point DNG output, headless merge | LR-0995, LR-0996, LR-0997, LR-0998, LR-0999, LR-1000, LR-1001, LR-1002, LR-1443, LR-1651, LR-1652 | AC-1053, AC-1054, AC-1055, AC-1056, AC-1057, AC-1058, AC-1059, AC-4425 | -- | core | plan D04 T09 §16 | consumes D03 T15 §5 and §6 moved to Isotone.Core; results stacked in the catalog instead of layers |
| LP-0688 | Panorama merge: spherical, cylindrical, perspective, auto projection, boundary warp, fill edges, auto crop, auto settings, stack, headless, rotate, several outputs, vignette removal, size limits | LR-1003, LR-1004, LR-1005, LR-1006, LR-1007, LR-1008, LR-1009, LR-1010, LR-1011, LR-1012, LR-1013, LR-1653, LR-1654 | AC-1040, AC-1044, AC-1045, AC-1046, AC-1047, AC-1048, AC-1049, AC-1050, AC-1051, AC-4424 | -- | core | plan D04 T09 §16 | consumes D03 T15 §7 moved to Isotone.Core |
| LP-0689 | HDR panorama in one step | LR-1014, LR-1015 | -- | -- | core | plan D04 T09 §16 |  |
| LP-0690 | Merge to panorama or HDR in the editor | LR-1023, LR-1024 | -- | -- | core | plan D04 T09 §16 | Albumen merges itself |
| LP-0691 | Photomerge hub: image list, output format, location, and metadata retention | -- | AC-1038, AC-1039, AC-1041, AC-1042, AC-1043, AC-4423 | -- | core | plan D04 T09 §16 |  |
| LP-0692 | Focus stacking: all or selected images, auto align, keep sources stacked, limits | -- | AC-1060, AC-1061, AC-1062, AC-1063, AC-1064, AC-4426 | -- | core | plan D04 T09 §16 | consumes D03 T15 §9 moved to Isotone.Core |

## People and faces

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0693 | Face detection across the catalog, automatic or on demand | LR-0468, LR-0469 | -- | -- | ai | plan D04 T10 §2 | through an OpenRouter vision model on explicit send with the send preview and provenance (operator decision 2026-09-27; the local YuNet model was not approved) |
| LP-0694 | Face detection after cataloging with a queue, pause toggle, redetect selected, remove face data, and rerun on changed images | -- | AC-0553, AC-0554, AC-0558, AC-0559, AC-4641 | -- | ai | plan D04 T10 §2 | through an OpenRouter vision model on explicit send with the send preview and provenance (operator decision 2026-09-27; the local YuNet model was not approved) |
| LP-0695 | Face recognition: recognize from named faces, auto naming or suggestions only, rerun recognition keeping manual names, sensitivity conservative, moderate, or aggressive | -- | AC-0560, AC-0561, AC-4091, AC-4092, AC-4093, AC-4094, AC-4095, AC-4097 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach) |
| LP-0696 | Face detection options: enable, detect while idle through the indexer, rerun on changed images, remove all face data | -- | AC-4088, AC-4089, AC-4090, AC-4096 | -- | ai | plan D04 T10 §2 | idle detection runs only under an approved send scope; through an OpenRouter vision model on explicit send with the send preview and provenance (operator decision 2026-09-27; the local YuNet model was not approved) |
| LP-0697 | Face detection on a selection of files | -- | -- | IV-0923 | ai | plan D04 T10 §2 | through an OpenRouter vision model on explicit send with the send preview and provenance (operator decision 2026-09-27; the local YuNet model was not approved) |
| LP-0698 | Face detection from the thumbnails window, CPU or GPU | -- | -- | IV-1058, IV-1115 | ai | plan D04 T10 §2 | detection runs at the model provider, so the settings row names the vision model and its cost instead of a device; through an OpenRouter vision model on explicit send with the send preview and provenance (operator decision 2026-09-27; the local YuNet model was not approved) |
| LP-0699 | Person keywords | LR-0451 | -- | -- | ai | plan D04 T10 §3 |  |
| LP-0700 | People view: named and unnamed people, confirm suggested names, draw and show face regions, rename faces | LR-0470, LR-0471, LR-0472, LR-0473, LR-0474, LR-1446 | -- | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach); drawing and showing face regions and renaming faces are built without the People view by D04 T10 §12 and D04 T10 §3 |
| LP-0701 | Naming faces: name bar with Enter advancing, Name Faces dialog, rename faces, remove name, set profile face | LR-1728 | AC-3925, AC-3926, AC-3927, AC-3928, AC-3929, AC-3930 | -- | ai | plan D04 T10 §3 |  |
| LP-0702 | People mode | -- | AC-0024, AC-4515, AC-4689, AC-4980 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach) |
| LP-0703 | Faces in the viewer: face tool, show face outlines, face detection pane to name faces | -- | AC-0098, AC-0104, AC-0115 | -- | ai | plan D04 T10 §12 |  |
| LP-0704 | People mode: open People view with named, unnamed, and person views, face counts beyond 9999 | -- | AC-0141, AC-0142, AC-0143, AC-0144, AC-0147, AC-3899, AC-3900, AC-3901, AC-3902 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach); the People group of named people with counts is D04 T10 §3 |
| LP-0705 | Unnamed faces grouped by similarity or ungrouped, naming or deleting a whole group | -- | AC-0145, AC-0146, AC-3920, AC-3921, AC-3922 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach) |
| LP-0706 | Face grid interaction: multi-select, face or source thumbnails, send source photos to viewer or develop | -- | AC-0148, AC-0149, AC-3903, AC-3904, AC-3905, AC-3906 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach); the Faces panel of D04 T10 §3 opens a face's source photo |
| LP-0707 | People folders filter: tree or list view, multi-select, refresh | -- | AC-0150, AC-0151, AC-0152, AC-3907, AC-3908, AC-3909, AC-3910 | -- | core | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach) |
| LP-0708 | Faces in the viewer: detection as each photo opens, enable setting, unsupported locations, face pane, show face outlines | -- | AC-0555, AC-0556, AC-1866, AC-1867, AC-1868, AC-1869, AC-1870 | -- | ai | plan D04 T10 §12 | the viewer reads stored faces; detection goes through D04 T10 §2 on explicit send or under an approved viewer send scope |
| LP-0709 | Search photos by named people in the catalog, quick search, and advanced search | -- | AC-0557 | -- | ai | plan D04 T10 §3 |  |
| LP-0710 | Face regions in XMP: face data stored in the catalog and written as MWG regions, import embedded face data from Albumen, Lightroom, or Picasa, including while cataloging | -- | AC-0562, AC-0563, AC-0564, AC-0565, AC-0566, AC-1874 | -- | ai | plan D04 T10 §12 | sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0711 | Face tool in the viewer: name faces with Enter and Tab, edit or draw outlines, name suggestions, confirm, deny, or edit suggestions | -- | AC-1871, AC-1872, AC-1873, AC-1875, AC-1876, AC-1877, AC-1878, AC-1879, AC-4636, AC-4637, AC-4638, AC-4639, AC-4640 | -- | ai | plan D04 T10 §12 | name suggestions wait for face recognition, backlog B-052; drawing, editing, and naming are built here |
| LP-0712 | Named people management: merge people, rename, remove, group by name, face count, or suggestions, sort and collapse groups | -- | AC-3911, AC-3912, AC-3913, AC-3914, AC-3915, AC-3916, AC-3917, AC-3918, AC-3919 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach); renaming and removing a person's name are D04 T10 §3 |
| LP-0713 | Delete face records or source images from People view | -- | AC-3923, AC-3924, AC-3931 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach); rejecting a wrong detection is D04 T10 §3 |
| LP-0714 | Suggested faces: pending-suggestion indicator, confirm, deny, edit name inline, confirm all, deny all | -- | AC-3932, AC-3933, AC-3934, AC-3935, AC-3936, AC-3937, AC-3938 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach) |
| LP-0715 | Embed face regions and names | -- | AC-4237 | -- | ai | plan D04 T10 §12 | MWG regions in the XMP sidecar by default; embedded into supported originals only when the user opts in (D04 T08 §9) |
| LP-0716 | People mode preferences: suppress confirm-all, deny-all, and delete prompts, default thumbnail, folder pane, and unnamed styles, pop-up options | -- | AC-4260, AC-4261, AC-4262, AC-4263, AC-4264, AC-4265, AC-4266, AC-4267 | -- | ai | backlog B-052 | face recognition and the People view are backlog B-052 (operator decision 2026-09-27: no local face models for Albumen, recognition waits for an approved approach) |

## AI

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0717 | AI keywords: automatic descriptive keywords after cataloging with the viewed folder first, run or rerun on selection, clear queue, pause toggle, priority scan of the selection, remove AI keywords | -- | AC-0531, AC-0532, AC-0533, AC-0534, AC-0535, AC-0536, AC-0537, AC-0538 | -- | ai | plan D04 T10 §4 | through an OpenRouter vision model with the user key and an explicit send; automatic runs are opt-in, never on by default |
| LP-0718 | AI keywords in the catalog: hierarchical AI keyword tree, searchable in quick and advanced search | -- | AC-0539, AC-0540 | -- | ai | plan D04 T10 §4 | stored apart from user keywords until accepted |
| LP-0719 | AI keyword review in the Organize tab: select modes, select all, partial-selection italics, assign one, selected, or all to keywords, remove one, selected, or all, filter as you type | -- | AC-0541, AC-0542, AC-0543, AC-0544, AC-0545, AC-0546, AC-0547, AC-0548, AC-0549, AC-0550, AC-0551, AC-0552 | -- | ai | plan D04 T10 §4 | accepting is one undoable command |
| LP-0720 | AI keywords in the organize pane and promotion into the keyword list, embedding AI keywords | -- | AC-0870, AC-0888, AC-0963, AC-1787 | -- | ai | plan D04 T10 §4 |  |
| LP-0721 | AI keywords options: enable, detect while idle, rerun on changed images, suppress remove prompt | -- | AC-4098, AC-4099, AC-4100, AC-4101 | -- | ai | plan D04 T10 §4 | idle runs send only after the user has approved the send scope |
| LP-0722 | Extract text from an image or selection (OCR) with languages and engine location | -- | -- | IV-0704, IV-0705, IV-0707, IV-1015, IV-1424 | ai | plan D04 T10 §4 | vision model through OpenRouter; a user-installed Tesseract (Apache-2.0) as the local path |
| LP-0723 | Visual similarity index: local analysis, idle-time indexing of the viewed folder, reanalyze selected, rerun on changed images, hardware acceleration with CPU fallback | -- | AC-0523, AC-0524, AC-0525, AC-0526, AC-0527 | -- | ai | plan D04 T10 §5 | local perceptual features, no ML model; GPU path not required |
| LP-0724 | Auto-stack by GPS location, capture time, similarity, or a combination, and manual custom stacks | -- | AC-0528, AC-0529, AC-4484 | -- | ai | plan D04 T10 §5 | stacks consume D04 T06 §3 |
| LP-0725 | Reverse image search: find every visually related shot of a selected photo | -- | AC-0530, AC-4510 | -- | ai | plan D04 T10 §5 |  |
| LP-0726 | Group by visual similarity with sensitivity slider and analyze-first prompt | -- | AC-0597, AC-0598, AC-0599, AC-0600 | -- | ai | plan D04 T10 §5 |  |
| LP-0727 | Similarity options: enable, analyze while idle, rerun on changed images, group-by sensitivity slider, stored sensitivity without prompting | -- | AC-4083, AC-4084, AC-4085, AC-4086, AC-4087, AC-4509, AC-4684 | -- | ai | plan D04 T10 §5 |  |
| LP-0728 | Assisted culling analysis at import | LR-0095 | -- | -- | ai | plan D04 T10 §6 |  |
| LP-0729 | AI masks recomputed per photo on copy, sync, presets, and focus on subject, with update all and outdated-mask warnings | LR-0695, LR-0703, LR-0704, LR-0927, LR-0954, LR-1807 | -- | -- | ai | plan D04 T10 §7 |  |
| LP-0730 | AI masks: select subject, sky, and background | LR-0897, LR-0898, LR-0899 | AC-2216, AC-2217, AC-2218 | -- | ai | plan D04 T10 §7 |  |
| LP-0731 | Landscape masks: sky, snow, architecture, vegetation, water, ground, mountains, combined or separate | LR-0900, LR-0901 | -- | -- | ai | plan D04 T10 §7 |  |
| LP-0732 | Object masks by brushing or boxing, with add, subtract, show, feather, and shift refinement | LR-0902, LR-0903 | AC-2219, AC-2248, AC-2249, AC-2250, AC-2251, AC-2252, AC-2253, AC-2254 | -- | ai | plan D04 T10 §7 |  |
| LP-0733 | People masks with parts: entire person, skin, eyebrows, eyes, lips, teeth, hair, clothes, several people | LR-0904, LR-0905 | -- | -- | ai | plan D04 T10 §7 |  |
| LP-0734 | Add a keyword to enhanced images | LR-0156 | -- | -- | ai | plan D04 T10 §8 |  |
| LP-0735 | Enhance dialog and rules: apply once, headless enhance, AI edits running in the background | LR-0705, LR-0797, LR-0798, LR-0799, LR-1444, LR-1649, LR-1650 | -- | -- | ai | plan D04 T10 §8 |  |
| LP-0736 | Denoise as a panel feature with amount, for Bayer, X-Trans, linear DNG, and small raw files | LR-0792, LR-0793, LR-0794 | -- | -- | ai | plan D04 T10 §8 | classical denoise; ML model variant is D04 T10 §13 |
| LP-0737 | Raw details: enhanced demosaic for Bayer and X-Trans | LR-0795 | -- | -- | ai | plan D04 T10 §8 | classical high-quality demosaic; ML model variant is D04 T10 §13 |
| LP-0738 | Super resolution to twice the linear size | LR-0796 | -- | -- | ai | plan D04 T10 §8 | OpenRouter image adapter moved to Isotone.Core, tiled; writes a new DNG, never the original |
| LP-0739 | Denoise dialog for one or many photos: strength, show original, preview zoom, live preview of the first photo, output folder options | -- | AC-1391, AC-1392, AC-1393, AC-1394, AC-1395, AC-1396, AC-1397, AC-1398, AC-1399, AC-4498, AC-4507, AC-4683 | -- | ai | plan D04 T10 §8 | classical denoise; ML model variant is D04 T10 §13; writes a new file, never the original; batch runs on D04 T11 §1 |
| LP-0740 | Super resolution dialog: enhance with strength, show original, preview zoom and fit, live preview, output location, hardware note, 16,000 pixel limit | -- | AC-1400, AC-1401, AC-1403, AC-1404, AC-1405, AC-1406, AC-1407, AC-1413, AC-1880, AC-1881, AC-1882, AC-1883, AC-1884, AC-1885, AC-1887, AC-1888, AC-1889, AC-1890, AC-1891, AC-4449, AC-4508, AC-4660 | -- | ai | plan D04 T10 §8 | OpenRouter image adapter moved to Isotone.Core with a classical detail-preserving fallback; writes a new file |
| LP-0741 | Batch super resolution: many photos at once with preview of the first, output same or chosen folder, subfolder, overwrite rules, preserve dates, metadata, and catalog data, presets with shortcuts | -- | AC-1402, AC-1886, AC-4037, AC-4045, AC-4046, AC-4047, AC-4048, AC-4049, AC-4050, AC-4051, AC-4052, AC-4053, AC-4499 | -- | ai | plan D04 T10 §8 | runs on the batch framework D04 T11 §1; replace-original becomes a new file (original-file guard) |
| LP-0742 | Super resolution target size: percentage, pixels with fit within, print size, long edge, short edge, preserve aspect ratio | -- | AC-1408, AC-1409, AC-1410, AC-1411, AC-1412, AC-1892, AC-1893, AC-1894, AC-1895, AC-1896, AC-4038, AC-4039, AC-4040, AC-4041, AC-4042, AC-4043, AC-4044 | -- | ai | plan D04 T10 §8 | size math shared with D04 T11 §5 batch resize |
| LP-0743 | Generative remove with variations: generate, cycle, delete, and report, and remove mode switching of a selected spot | LR-0868, LR-0869, LR-0870, LR-0871, LR-0874, LR-0891, LR-1729, LR-1731 | -- | -- | ai | plan D04 T10 §9 | OpenRouter image adapter with the user key; costs shown in the send preview; result cached as develop spot data |
| LP-0744 | Detect objects when brushing a removal, with add and subtract | LR-0872, LR-0873, LR-1730 | -- | -- | ai | plan D04 T10 §9 |  |
| LP-0745 | Distraction removal: people, reflections, dust, and rerun per photo on paste | LR-0887, LR-0888, LR-0889, LR-0890 | -- | -- | ai | plan D04 T10 §9 |  |
| LP-0746 | Depth range masks from embedded or estimated depth | LR-0918 | -- | -- | core | plan D04 T10 §10 |  |
| LP-0747 | Lens blur from depth: apply, amount, focus range, subject focus, point or area focus, visualize depth, focus and blur brushes, device depth maps | LR-0958, LR-0959, LR-0965, LR-0968, LR-0969, LR-0970, LR-0971, LR-0972, LR-0973 | -- | -- | ai | plan D04 T10 §10 | estimated depth via the approach of D03 T19 §14; embedded HEIC depth maps read locally |
| LP-0748 | Lens blur bokeh shapes and boost: circle, bubble, five-blade, ring, anamorphic, cat eye | LR-0960, LR-0961, LR-0962, LR-0963, LR-0964, LR-0966, LR-0967 | -- | -- | core | plan D04 T10 §10 |  |
| LP-0749 | Blur background adaptive presets and focus-on-subject recomputed on paste | LR-0974, LR-0975 | -- | -- | ai | plan D04 T10 §10 |  |
| LP-0750 | Adaptive color profile | LR-0730 | -- | -- | ai | plan D04 T10 §11 | Albumen builds a scene-adapted look from local analysis; no Adobe profile is bundled |
| LP-0751 | Adaptive presets: subject, sky, portrait, and landscape presets that build AI masks | LR-0955, LR-0984, LR-0985 | AC-2145 | -- | ai | plan D04 T10 §11 | masks located through an OpenRouter vision model plus the local segmentation engine |

## Batch processing

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0752 | Activity centre: background task progress with pause and resume, background activity indicator | LR-0011, LR-0012 | -- | -- | ai | plan D04 T11 §1 | one Activity Manager for indexing, faces, culling, batch |
| LP-0753 | Activity manager: queued activities with pause and cancel, idle activities, history | -- | AC-0043, AC-0044, AC-0045, AC-0046 | -- | automation | plan D04 T11 §1 |  |
| LP-0754 | Activity Manager: one pane listing queued background jobs (import, export, resize, convert, apply develop) with progress, remaining count, and status bar entry | -- | AC-0691, AC-0692, AC-0694, AC-4463 | -- | automation | plan D04 T11 §1 |  |
| LP-0755 | Activity Manager idle activities: idle-time jobs (similarity, AI keywords, face detection, previews) with states, per-tool toggles, and queue clearing | -- | AC-0693, AC-0710, AC-0711, AC-0712, AC-0721, AC-0722, AC-0723, AC-0724, AC-0725 | -- | ai | plan D04 T11 §1 | the jobs themselves are owned by D04 T10 §2, D04 T10 §4, D04 T10 §5, and D04 T01 §7 |
| LP-0756 | Batch job control: pause, resume, cancel, reorder the queue, pause and resume all, clear all | -- | AC-0695, AC-0696, AC-0697, AC-0699, AC-0719, AC-0720 | IV-0304, IV-0305, IV-0306 | automation | plan D04 T11 §1 |  |
| LP-0757 | Batch concurrency and conflict prevention: parallel jobs by core count, multithreaded conversion, skip files open in develop, never two jobs on the same files, pause during file commands, block restart while running | -- | AC-0698, AC-0700, AC-0701, AC-0702, AC-0703 | IV-0286 | automation | plan D04 T11 §1 |  |
| LP-0758 | Batch notifications: queued and completed toasts with statuses (errors, skipped, warnings), show and browse output buttons, muting options, result reports | -- | AC-0704, AC-0705, AC-0706, AC-0707, AC-0708, AC-0709, AC-4034, AC-4035, AC-4036 | -- | automation | plan D04 T11 §1 |  |
| LP-0759 | Activity history: completed jobs with per-file details view (status, name, source, destination, preset), clear items, reopen searches | -- | AC-0713, AC-0714, AC-0715, AC-0716, AC-0717, AC-0718 | -- | automation | plan D04 T11 §1 | reopening an advanced search consumes D04 T06 §7 |
| LP-0760 | Batch status in the Activity Manager for convert jobs | -- | AC-1473 | -- | automation | plan D04 T11 §1 |  |
| LP-0761 | Batch tools keep originals: outputs are new files so originals can always be restored | -- | AC-4198 | -- | core | plan D04 T11 §1 | originals are never written (original-file guard) |
| LP-0762 | File name generation rules: illegal characters and space replacement | LR-0154, LR-0155 | -- | -- | core | plan D04 T11 §2 | shared by rename, import, and export |
| LP-0763 | Filename template editor and tokens: filename, number suffix, original name, folder, copy name, sequences, image, import, and total numbers, dates, dimensions, metadata fields, custom text, shoot name | LR-0157, LR-0158, LR-0159, LR-0160, LR-0161, LR-0162, LR-0163, LR-0164, LR-0165, LR-0166, LR-0167, LR-0168, LR-0169, LR-0170, LR-0171 | -- | -- | core | plan D04 T11 §2 |  |
| LP-0764 | Text template editor for captions in slideshow, print, web, and book | LR-0172 | -- | -- | core | plan D04 T11 §2 |  |
| LP-0765 | Rename templates dialog: system and user templates, template field with *, # and metadata placeholders, insert metadata, sample | -- | AC-0365, AC-0380, AC-0381, AC-0382, AC-0383, AC-0384, AC-0385, AC-0386, AC-0387, AC-0388 | -- | core | plan D04 T11 §2 |  |
| LP-0766 | Output naming templates in batch runners: original name token, sequence token with numbers or letters and start value, metadata tokens, recent templates, duplicate suffix | -- | AC-1419, AC-1420, AC-1421, AC-1422, AC-1423, AC-1424, AC-1425, AC-1426, AC-1427, AC-1616, AC-1617, AC-1707, AC-1708, AC-1709, AC-1710, AC-1711, AC-1712 | -- | automation | plan D04 T11 §2 | one token engine for rename, export, and overlays |
| LP-0767 | File tokens: folder path, last subfolder, file name with or without extension, extension, corrected extension, size, folder index, page index, substring ranges | -- | -- | IV-1607, IV-1608, IV-1609, IV-1610, IV-1611, IV-1612, IV-1615, IV-1616, IV-1624, IV-1636 | automation | plan D04 T11 §2 |  |
| LP-0768 | Date and time tokens: file date, current date, with strftime-style formats (year, month, day, hour, minute, second, weekday and month names) | -- | -- | IV-1613, IV-1614, IV-1837, IV-1838, IV-1839, IV-1840, IV-1841, IV-1842, IV-1843, IV-1844, IV-1845, IV-1846, IV-1847, IV-1849 | automation | plan D04 T11 §2 |  |
| LP-0769 | Image tokens: width, height, bits per pixel, DPI, megapixels, aspect ratio, zoom, print size, compression, comment | -- | -- | IV-1617, IV-1618, IV-1619, IV-1620, IV-1621, IV-1622, IV-1623, IV-1625, IV-1626, IV-1627 | automation | plan D04 T11 §2 |  |
| LP-0770 | IPTC tokens: all IPTC data or any IPTC dataset (title, keywords, byline, city, country, headline, credit, copyright, caption, and the rest) | -- | -- | IV-1628, IV-1629, IV-1637, IV-1638, IV-1639, IV-1640, IV-1641, IV-1642, IV-1643, IV-1644, IV-1645, IV-1646, IV-1647, IV-1648, IV-1649, IV-1650, IV-1651, IV-1652, IV-1653, IV-1654, IV-1655, IV-1656, IV-1657, IV-1658, IV-1659, IV-1660, IV-1661, IV-1662, IV-1663, IV-1664, IV-1665, IV-1666, IV-1667, IV-1668, IV-1669, IV-1670, IV-1671 | automation | plan D04 T11 §2 |  |
| LP-0771 | EXIF tokens: all EXIF data or any standard EXIF tag (camera, exposure, lens, dates, resolution, and the rest) | -- | -- | IV-1630, IV-1631, IV-1672, IV-1673, IV-1674, IV-1675, IV-1676, IV-1677, IV-1678, IV-1679, IV-1680, IV-1681, IV-1682, IV-1683, IV-1684, IV-1685, IV-1686, IV-1687, IV-1688, IV-1689, IV-1690, IV-1691, IV-1692, IV-1693, IV-1694, IV-1695, IV-1696, IV-1697, IV-1698, IV-1699, IV-1700, IV-1701, IV-1702, IV-1703, IV-1704, IV-1705, IV-1706, IV-1707, IV-1708, IV-1709, IV-1710, IV-1711, IV-1712, IV-1713, IV-1714, IV-1715, IV-1716, IV-1717, IV-1718, IV-1719, IV-1720, IV-1721, IV-1722, IV-1723, IV-1724, IV-1725, IV-1726, IV-1727, IV-1728, IV-1729, IV-1730, IV-1731, IV-1732, IV-1733, IV-1734, IV-1735, IV-1736, IV-1737, IV-1738, IV-1739, IV-1740, IV-1741, IV-1742, IV-1743, IV-1744 | automation | plan D04 T11 §2 |  |
| LP-0772 | Special tokens and counters: new line, literal dollar, pipe, and hash, counter digits, and where tokens apply (text, batch, print, slideshow, fullscreen, contact sheet) | -- | -- | IV-1632, IV-1633, IV-1634, IV-1635, IV-1848, IV-1850 | automation | plan D04 T11 §2 |  |
| LP-0773 | GPS tokens: latitude, longitude, altitude, time, direction, and a combined coordinate pair | -- | -- | IV-1745, IV-1746, IV-1747, IV-1748, IV-1749, IV-1750, IV-1751, IV-1752, IV-1753, IV-1754, IV-1755, IV-1756 | automation | plan D04 T11 §2 |  |
| LP-0774 | Maker-note tokens for Nikon, Canon, and Fuji fields | -- | -- | IV-1757, IV-1758, IV-1759, IV-1760, IV-1761, IV-1762, IV-1763, IV-1764, IV-1765, IV-1766, IV-1767, IV-1768, IV-1769, IV-1770, IV-1771, IV-1772, IV-1773, IV-1774, IV-1775, IV-1776, IV-1777, IV-1778, IV-1779, IV-1780, IV-1781, IV-1782, IV-1783, IV-1784, IV-1785, IV-1786, IV-1787, IV-1788, IV-1789, IV-1790, IV-1791, IV-1792, IV-1793, IV-1794, IV-1795, IV-1796, IV-1797, IV-1798, IV-1799, IV-1800, IV-1801, IV-1802, IV-1803, IV-1804, IV-1805, IV-1806, IV-1807, IV-1808, IV-1809, IV-1810, IV-1811, IV-1812, IV-1813, IV-1814, IV-1815, IV-1816, IV-1817, IV-1818, IV-1819, IV-1820, IV-1821, IV-1822, IV-1823, IV-1824, IV-1825, IV-1826, IV-1827, IV-1828, IV-1829, IV-1830, IV-1831, IV-1832, IV-1833, IV-1834, IV-1835, IV-1836 | automation | plan D04 T11 §2 | maker notes decoded as far as the metadata reader supports them |
| LP-0775 | Batch rename: ordered list of operations (template, search and replace, case change, insert text, remove text, strip spaces), checkable and reorderable, up to ten, live preview | -- | AC-1560, AC-1589, AC-1590, AC-1591, AC-1592, AC-4671 | -- | automation | plan D04 T11 §3 |  |
| LP-0776 | Batch rename presets, last used settings, pattern history, and saved rename profiles | -- | AC-1561 | IV-0295, IV-0300 | automation | plan D04 T11 §3 |  |
| LP-0777 | Rename template operation: text with original-name and sequence tokens, metadata tokens, numbers or letters, fixed start or auto-detected continuation, clear templates | -- | AC-1562, AC-1563, AC-1564, AC-1565, AC-1566, AC-1567, AC-1568, AC-1569 | IV-0291, IV-0292, IV-0293, IV-0294 | automation | plan D04 T11 §3 | tokens from D04 T11 §2 |
| LP-0778 | Rename search and replace: literal text or metadata value, case sensitive, include extension | -- | AC-1570, AC-1571, AC-1572, AC-1573 | IV-0296 | automation | plan D04 T11 §3 |  |
| LP-0779 | Rename case change for name and extension: lower, upper, title, unchanged | -- | AC-1574, AC-1575 | IV-0297, IV-0302 | automation | plan D04 T11 §3 |  |
| LP-0780 | Rename insert and remove text: at prefix, suffix, position, before or after text, from the right, overwrite, delimiters, counts | -- | AC-1576, AC-1577, AC-1578, AC-1579, AC-1580, AC-1581, AC-1582, AC-1583, AC-1584, AC-1585 | -- | automation | plan D04 T11 §3 |  |
| LP-0781 | Rename strip spaces: all, trailing, consecutive, or replace with a character | -- | AC-1586 | -- | automation | plan D04 T11 §3 |  |
| LP-0782 | Rename conflict handling for duplicate names and extension changes: ask, skip, or rename | -- | AC-1587, AC-1588 | -- | automation | plan D04 T11 §3 |  |
| LP-0783 | Rename in place or copy and move renamed files to an output folder, with sidecars and pairs renamed together | -- | -- | IV-0299 | automation | plan D04 T11 §3 | a rename is a file operation; image bytes are never rewritten |
| LP-0784 | Test rename: preview resulting names without renaming | -- | -- | IV-0301 | automation | plan D04 T11 §3 |  |
| LP-0785 | Batch output destination: same as source, a new subfolder, or a specific folder, shared by export, convert, edit, and develop runners | -- | AC-1416, AC-1417, AC-1418, AC-1459, AC-1613, AC-1614, AC-1615, AC-1704, AC-1705, AC-1706 | IV-0287, IV-0288, IV-0289 | automation | plan D04 T11 §4 | outputs are new files; the original is never written |
| LP-0786 | Batch output format, format settings, pixel format, and color space conversion | -- | AC-1428, AC-1429, AC-1430, AC-1431, AC-1458, AC-1618, AC-1619, AC-1713, AC-1714, AC-1715 | IV-0285 | automation | plan D04 T11 §4 | per-format options consume D04 T13 §6 |
| LP-0787 | Preserve metadata, database information (ratings, keywords from the catalog), and color profile in batch outputs | -- | AC-1450, AC-1451, AC-1467, AC-1468, AC-1620, AC-1623, AC-1723 | -- | automation | plan D04 T11 §4 | catalog fields are embedded in the new file only |
| LP-0788 | Preserve or set file dates: keep last-modified date, keep original date on output | -- | AC-1452, AC-1464, AC-1499, AC-1528, AC-1622 | IV-0348 | automation | plan D04 T11 §4 |  |
| LP-0789 | Convert file format: many images to any writable format with per-format settings | -- | AC-1457, AC-4501, AC-4666 | -- | automation | plan D04 T11 §4 |  |
| LP-0790 | Overwrite rules for batch outputs: ask, skip, replace, rename, or create a numbered copy | -- | AC-1460, AC-1461, AC-1462, AC-1463, AC-1495, AC-1496, AC-1497, AC-1498, AC-1527, AC-1624 | IV-0298, IV-0344 | automation | plan D04 T11 §4 | replace applies to earlier outputs only, never to an original |
| LP-0791 | Remove originals after conversion: move to the Recycle Bin only after a verified conversion, kept when the output cannot hold the metadata | -- | AC-1465, AC-1466 | IV-0345 | automation | plan D04 T11 §4 | move to Recycle Bin after verified conversion, never an in-place overwrite (original-file guard) |
| LP-0792 | Convert options for vector sources (rasterization size) and multi-page sources (every page, multi-page output, multi-page to multi-page PDF) | -- | AC-1469, AC-1470, AC-1475 | IV-0308, IV-0347 | automation | plan D04 T11 §4 |  |
| LP-0793 | Batch resize output location options: same folder, specific folder, named subfolder | -- | AC-1524, AC-1525, AC-1526 | -- | automation | plan D04 T11 §4 |  |
| LP-0794 | Placeholder-driven output folders: next to originals, or sorted into folders by date taken | -- | -- | IV-0290 | automation | plan D04 T11 §4 | tokens from D04 T11 §2 |
| LP-0795 | Recreate the source folder structure in the output | -- | -- | IV-0346 | automation | plan D04 T11 §4 |  |
| LP-0796 | Extract pages from multi-page files and export image tiles for a selection | -- | -- | IV-0892, IV-0907 | core | plan D04 T11 §4 |  |
| LP-0797 | Save each thumbnail as an image file | -- | -- | IV-0909 | core | plan D04 T11 §4 |  |
| LP-0798 | Rotate selected images left or right from the file list, auto-rotate overlay action | -- | AC-0414, AC-0415 | -- | core | plan D04 T11 §5 | orientation as metadata or a new file, never the original |
| LP-0799 | Batch resize by width and height, long or short edge, percentage, megapixels, or print size with units and resolution, preserving aspect ratio and fit-within rules | -- | AC-1432, AC-1441, AC-1442, AC-1443, AC-1444, AC-1445, AC-1449, AC-1503, AC-1506, AC-1508, AC-1509, AC-1510, AC-1511, AC-1512, AC-1513, AC-1514, AC-1516, AC-1517, AC-1518, AC-1520, AC-1521, AC-1635, AC-1637, AC-1638, AC-1639, AC-1716, AC-1717, AC-1718, AC-1719, AC-1721, AC-1722, AC-4500, AC-4668 | IV-0312, IV-0313, IV-0314, IV-0315 | automation | plan D04 T11 §5 |  |
| LP-0800 | Resampling filters for batch resize: Box, Triangle, Bell, B-spline, Bicubic, Mitchell, Lanczos, and an enlargement-oriented filter | -- | AC-1433, AC-1434, AC-1435, AC-1436, AC-1437, AC-1438, AC-1439, AC-1440, AC-1532, AC-1533, AC-1534, AC-1535, AC-1536, AC-1537, AC-1538, AC-1539, AC-1643 | IV-0316 | automation | plan D04 T11 §5 | consumes D01 T03 §2 resampling; ClearIQZ is ACDSee proprietary, mapped to the best-quality enlarge filter |
| LP-0801 | Batch resize modes: enlarge only, reduce only, or both; minimal and maximal dimensions; resize by DPI only | -- | AC-1446, AC-1447, AC-1448, AC-1507, AC-1515, AC-1519, AC-1522, AC-1636, AC-1720 | IV-0317, IV-0318, IV-0319, IV-0320, IV-0321 | automation | plan D04 T11 §5 |  |
| LP-0802 | Batch rotate and flip: 90, 180, flip horizontal or vertical, transpose and transverse, auto-rotate from EXIF, one angle for all or per image with Next Image | -- | AC-1474, AC-1476, AC-1477, AC-1479, AC-1480, AC-1481, AC-1482, AC-1483, AC-1484, AC-1485, AC-1486, AC-1487, AC-1488, AC-1489, AC-4502, AC-4667 | IV-0324, IV-0325, IV-0326 | automation | plan D04 T11 §5 |  |
| LP-0803 | Batch rotate options: force lossless JPEG operations, output to a renamed file beside the source or a chosen folder, remember last rotation, auto-close progress, save as default | -- | AC-1478, AC-1490, AC-1491, AC-1493, AC-1494, AC-1500, AC-1501, AC-1502 | -- | automation | plan D04 T11 §5 | lossless JPEG transforms write a new file |
| LP-0804 | Replace the original file with a rotated, resized, or profile-converted version | -- | AC-1492, AC-1523 | -- | automation | plan D04 T11 §5 | a new file or orientation metadata by default; in place only when the user opts in, after a verified backup (D04 T11 §1) |
| LP-0805 | Batch resize presets with keyboard shortcuts, JPEG options, and remember-as-default | -- | AC-1504, AC-1505, AC-1529, AC-1530, AC-1531 | -- | automation | plan D04 T11 §5 |  |
| LP-0806 | Resize fitting methods: best fit, stretch to exact size, or letterbox with colored bars | -- | AC-1640, AC-1641, AC-1642 | -- | automation | plan D04 T11 §5 |  |
| LP-0807 | Lossless JPEG transform, crop, and comment on a selection | -- | -- | IV-0889 | core | plan D04 T11 §5 | writes new files, never the original |
| LP-0808 | Batch adjust exposure: exposure, auto, contrast, fill light, with per-image or shared settings, presets, and Next Image | -- | AC-1540, AC-1541, AC-1542, AC-1543, AC-1544, AC-1545, AC-1546, AC-4504, AC-4669 | -- | automation | plan D04 T11 §6 |  |
| LP-0809 | Batch levels and auto levels: channel, black, gamma, and white points, clipping readout, eyedroppers, auto contrast and color with strength and tolerance | -- | AC-1547, AC-1548, AC-1549, AC-1550, AC-1551, AC-1552, AC-1553, AC-1554, AC-1555, AC-1556, AC-1657, AC-1658, AC-1659, AC-1660, AC-1661, AC-1662 | -- | automation | plan D04 T11 §6 | consumes D01 T03 §4 |
| LP-0810 | Batch tone curves with channel, histogram, and draggable curve | -- | AC-1557, AC-1558, AC-1559, AC-1663 | -- | automation | plan D04 T11 §6 | consumes D01 T03 §4 |
| LP-0811 | Batch convert ICC profile: source profile or embedded profile, target profile, rendering intent, output to new files with JPEG options | -- | AC-1593, AC-1594, AC-1595, AC-1596, AC-1597, AC-1598 | -- | automation | plan D04 T11 §6 | consumes D01 T04 §1 and §2; outputs are new files, never the original |
| LP-0812 | Batch edit wizard: a processing profile of chosen edit operations with presets | -- | AC-1599, AC-1600, AC-1612, AC-4497, AC-4665 | -- | automation | plan D04 T11 §7 |  |
| LP-0813 | Batch edit preview: before and after, original and final image, next and previous image, zoom, fit, and actual size | -- | AC-1601, AC-1602, AC-1603, AC-1604 | -- | automation | plan D04 T11 §7 |  |
| LP-0814 | Batch edit output options page, progress page with per-image bars, completion log, browse output in Explorer or Albumen, save the settings as a preset | -- | AC-1606, AC-1607, AC-1608, AC-1609, AC-1610, AC-1611 | -- | automation | plan D04 T11 §7 |  |
| LP-0815 | Batch edit rotate: presets, custom angle, background color, straighten by drawing a line, automatic crop, reset | -- | AC-1625, AC-1626, AC-1627, AC-1628, AC-1629, AC-1630, AC-1631 | IV-0327 | automation | plan D04 T11 §7 |  |
| LP-0816 | Batch edit crop: proportion or custom area, orientation automatic, landscape, or portrait; crop by x, y, width, height from a corner or center, fill from the current selection | -- | AC-1632, AC-1633, AC-1634 | IV-0310, IV-0311 | automation | plan D04 T11 §7 |  |
| LP-0817 | Batch edit color: color cast removal with a picked neutral, white point presets, strength, temperature, tint, saturation | -- | AC-1644, AC-1645, AC-1646, AC-1647, AC-1648, AC-1649 | -- | automation | plan D04 T11 §7 | consumes D01 T03 §5 |
| LP-0818 | Batch edit channel mixer grayscale, sepia, grayscale, and negative | -- | AC-1650, AC-1651, AC-1652 | IV-0328, IV-0329 | automation | plan D04 T11 §7 | consumes D01 T03 §5 |
| LP-0819 | Batch edit exposure: exposure, contrast, fill light, brightness, gamma, exposure warning | -- | AC-1653, AC-1654, AC-1655, AC-1656 | -- | automation | plan D04 T11 §7 | consumes D01 T03 §4 |
| LP-0820 | Batch edit Light EQ: automatic per image, brighten and darken with compression and amplitude, exposure warning | -- | AC-1664, AC-1665, AC-1666, AC-1667 | -- | automation | plan D04 T11 §7 | consumes the tone equalizer stage D01 T07 §7 |
| LP-0821 | Batch edit noise removal: despeckle, square, X, plus, hybrid with luminance and color, presets | -- | AC-1668, AC-1669, AC-1670, AC-1671 | -- | automation | plan D04 T11 §7 | consumes D01 T03 §6 |
| LP-0822 | Batch edit sharpening: amount, radius, threshold | -- | AC-1672, AC-1673, AC-1674 | IV-0330 | automation | plan D04 T11 §7 | consumes D01 T03 §6 |
| LP-0823 | Batch edit vignette: focal point, clear and transition zones, round or rectangular, outline, frame effects (color, saturation, blur, clouds, edges, radial waves, radial and zoom blur, crayon edges) | -- | AC-1675, AC-1676, AC-1677, AC-1678, AC-1679, AC-1680, AC-1681 | -- | automation | plan D04 T11 §7 | frame effects consume the Isotone.Core effect registry |
| LP-0824 | Advanced batch options: enable an ordered set of image operations, custom processing order, saved option profiles | -- | -- | IV-0309, IV-0349, IV-0351 | automation | plan D04 T11 §7 |  |
| LP-0825 | Advanced batch color and tone operations: color depth, auto adjust, brightness, contrast, gamma, saturation, color balance, replace color | -- | -- | IV-0322, IV-0323, IV-0331, IV-0332, IV-0333, IV-0334, IV-0335, IV-0342 | automation | plan D04 T11 §7 |  |
| LP-0826 | Advanced batch filters: blur, median, and any effect from the effects browser | -- | -- | IV-0336, IV-0337 | automation | plan D04 T11 §7 | consumes the Isotone.Core effect registry |
| LP-0827 | Advanced batch canvas size and border or frame | -- | -- | IV-0338, IV-0339 | automation | plan D04 T11 §7 |  |
| LP-0828 | Batch set DPI | -- | -- | IV-0343 | automation | plan D04 T11 §7 |  |
| LP-0829 | Text overlay: text with font, style, rotation, size, color, opacity, alignment, symbols, and metadata tokens | -- | AC-1682, AC-1683, AC-1684, AC-1685 | -- | automation | plan D04 T11 §8 |  |
| LP-0830 | Text overlay box: position offsets, border and fill with transparency, bevel, drop shadow, and blend mode for box and text | -- | AC-1686, AC-1687, AC-1688, AC-1689, AC-1690, AC-1691, AC-1692, AC-1693 | -- | automation | plan D04 T11 §8 |  |
| LP-0831 | Image watermark: choose a file, keep aspect when resizing, alpha channel or a transparent color, position in pixels or percent, blend mode, opacity | -- | AC-1694, AC-1695, AC-1696, AC-1697, AC-1698, AC-1699, AC-1700 | -- | automation | plan D04 T11 §8 |  |
| LP-0832 | Advanced batch text overlay with placeholders and image watermark with corner, offset, and transparency | -- | -- | IV-0340, IV-0341 | automation | plan D04 T11 §8 |  |
| LP-0833 | Insert text in batch: start corner, offsets, rectangle size, font scaled to desktop height | -- | -- | IV-0406, IV-0407 | automation | plan D04 T11 §8 |  |
| LP-0834 | Develop presets applied across many photos | LR-1386 | -- | -- | automation | plan D04 T11 §9 |  |
| LP-0835 | Batch export: multiple outputs in one pass (folders, names, formats, dimensions) as a queued job | -- | AC-1414, AC-1415, AC-4496 | -- | automation | plan D04 T11 §9 | extends D04 T02 §6 |
| LP-0836 | Apply a develop preset while exporting or converting a batch | -- | AC-1453 | -- | automation | plan D04 T11 §9 | consumes D04 T02 §5 |
| LP-0837 | Batch develop: apply a develop preset to many photos and optionally export them with the full export options | -- | AC-1701, AC-1702, AC-1703, AC-4664 | -- | automation | plan D04 T11 §9 | consumes D04 T02 §5 and D04 T02 §6 |
| LP-0838 | Apply a develop preset to many photos as a background job | -- | AC-2151 | -- | automation | plan D04 T11 §9 |  |
| LP-0839 | Batch menu and start batch with the selected files | -- | AC-0049 | IV-0885 | automation | plan D04 T11 §10 |  |
| LP-0840 | Batch tools menu and the tag-then-batch workflow: batch applies one or many edits to many files, also renames non-image files | -- | AC-1389, AC-1390 | -- | automation | plan D04 T11 §10 |  |
| LP-0841 | Batch presets: save, update, delete, and apply several export presets together; convert presets with keyboard shortcuts | -- | AC-1455, AC-1456, AC-1471, AC-1472, AC-1724 | -- | automation | plan D04 T11 §10 |  |
| LP-0842 | Batch image list: add and remove images, add all, include subfolders, load and save a text list, sort the list by name, date, size, extension, or EXIF date, preview the selected input | -- | AC-1605 | IV-0278, IV-0279, IV-0280, IV-0281, IV-0282, IV-0283, IV-0284 | automation | plan D04 T11 §10 |  |
| LP-0843 | Open the batch conversion and rename dialog from the viewer | -- | -- | IV-0089, IV-1430 | automation | plan D04 T11 §10 |  |
| LP-0844 | Work modes of the batch dialog: convert, rename, or convert and rename | -- | -- | IV-0275, IV-0276, IV-0277 | automation | plan D04 T11 §10 |  |
| LP-0845 | Start batch with a progress dialog and remember the last used batch folder | -- | -- | IV-0303, IV-0307 | automation | plan D04 T11 §10 |  |
| LP-0846 | Convert selected files from the Explorer context menu | -- | -- | IV-1041 | automation | plan D04 T11 §10 |  |
| LP-0847 | Apply a recorded action while exporting a batch | -- | AC-1454 | -- | automation | plan D04 T17 §1 | recorded actions are the suite-wide action system of D01 T10 |
| LP-0848 | Preserve embedded audio in batch outputs | -- | AC-1621 | -- | automation | plan D04 T16 §5 |  |

## Export and publish

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0849 | Export location options: specific folder, same folder as original, choose later, standard user folders, subfolder | LR-1054, LR-1055, LR-1056, LR-1057, LR-1058 | -- | -- | core | plan D04 T12 §1 | extends D04 T02 §6 |
| LP-0850 | Export file naming: rename template with custom text, start number, and extension case | LR-1062, LR-1063 | -- | -- | core | plan D04 T12 §1 | template tokens from D04 T11 §2 |
| LP-0851 | JPEG export limited to a target file size | LR-1069 | -- | -- | format | plan D04 T12 §1 |  |
| LP-0852 | Export color space including ProPhoto, Rec. 2020, and any ICC profile, and bit depth 8, 16, or 32 | LR-1081, LR-1082 | -- | -- | format | plan D04 T12 §1 | extends D04 T02 §6 color space |
| LP-0853 | Export image sizing: width and height, dimensions, units, resolution | LR-1086, LR-1088, LR-1089 | -- | -- | core | plan D04 T12 §1 | extends D04 T02 §6 resize |
| LP-0854 | Export destination: same folder, new subfolder, or a chosen folder | -- | AC-2157, AC-2158, AC-2159 | -- | core | plan D04 T12 §1 |  |
| LP-0855 | Export file format with format settings, pixel format, and color space | -- | AC-2168, AC-2169, AC-2170, AC-2171 | -- | format | plan D04 T12 §1 |  |
| LP-0856 | Export resize: dimensions, width and height, long or short edge, percentage, resolution, enlarge or reduce only, preserve aspect | -- | AC-2172, AC-2181, AC-2182, AC-2183, AC-2184, AC-2185, AC-2186, AC-2187, AC-2188, AC-2189, AC-2190 | -- | core | plan D04 T12 §1 | extends D04 T02 §6 |
| LP-0857 | Export resampling filters: bell, bicubic, box, B-spline, detail-preserving enlarge, Lanczos, Mitchell, triangle | -- | AC-2173, AC-2174, AC-2175, AC-2176, AC-2177, AC-2178, AC-2179, AC-2180 | -- | core | plan D04 T12 §1 | resamplers from D01 T03 §2 |
| LP-0858 | Export PSD and PSB flattened documents | LR-1070, LR-1071 | -- | -- | format | plan D04 T12 §2 | flat composite through the Isotone.Core PSD writer |
| LP-0859 | TIFF export with transparency | LR-1074 | -- | -- | format | plan D04 T12 §2 |  |
| LP-0860 | DNG export with compatibility, preview, fast load data, lossy compression, embedded original | LR-1076, LR-1077 | -- | -- | format | plan D04 T12 §2 | writer from D04 T13 §7 |
| LP-0861 | AVIF and JPEG XL export with quality, lossless, and HDR | LR-1078, LR-1079 | -- | -- | format | plan D04 T12 §2 |  |
| LP-0862 | Export original file with updated XMP sidecar | LR-1080 | -- | -- | format | plan D04 T12 §2 | copies the original bytes, metadata in a sidecar (original-file guard) |
| LP-0863 | HDR output: HDR color spaces and SDR base with gain map for compatibility | LR-1083, LR-1084, LR-1085 | -- | -- | format | plan D04 T12 §2 |  |
| LP-0864 | Publish Services panel with a hard drive publish service: published collections, smart and folder-set groups, publish states, publish, republish, mark up to date, remove on next publish | LR-0636, LR-0637, LR-0641, LR-0642, LR-0643, LR-0644, LR-0645, LR-0646, LR-0647, LR-0648, LR-0649 | -- | -- | automation | plan D04 T12 §3 | local folder destination only |
| LP-0865 | Go to published destination folder and import publish service settings | LR-0651, LR-0652 | -- | -- | cloud | plan D04 T12 §3 | opens the local destination folder in Explorer |
| LP-0866 | FTP transfer of selected files | -- | -- | IV-1065 | core | plan D04 T12 §9 | reuses the gallery uploader (FTP to the user's own server) |
| LP-0867 | Export to email: export then compose in the mail client or send through SMTP | LR-1044, LR-1118, LR-1394 | -- | -- | cloud | plan D04 T12 §12 |  |
| LP-0868 | Send menu and email selected files through the local mail client | -- | AC-0052 | IV-0921 | core | plan D04 T12 §12 | uploads to photo sites are excluded as cloud |
| LP-0869 | Email images: wizard with add and remove, size limit, conversion to JPEG, default mail client or SMTP | -- | AC-1173, AC-1174, AC-1175, AC-1176, AC-1177 | -- | core | plan D04 T12 §12 | mail client through Simple MAPI |
| LP-0870 | Upload images to the user's own FTP server | -- | AC-1277 | -- | automation | plan D04 T12 §12 | FluentFTP (MIT) |
| LP-0871 | FTP transfer of a selection to the user's own server with server, user, password, remote folder, progress | -- | -- | IV-0886, IV-0887 | core | plan D04 T12 §12 |  |
| LP-0872 | Send images by email from the viewer and thumbnails | -- | -- | IV-1056 | core | plan D04 T12 §12 |  |
| LP-0873 | Remove person keywords and face regions on export | LR-0475 | -- | -- | core | plan D04 T12 §13 |  |
| LP-0874 | Export and burn to CD or DVD | LR-1045, LR-1119 | -- | -- | core | plan D04 T12 §13 | burns through the Windows IMAPI2 disc writer |
| LP-0875 | Export with preset and export with previous without the dialog | LR-1047, LR-1048, LR-1392, LR-1393, LR-1643 | -- | -- | automation | plan D04 T12 §13 | extends D04 T02 §6 |
| LP-0876 | Built-in export presets and user preset folders: add, update, remove | LR-1049, LR-1050 | -- | -- | automation | plan D04 T12 §13 | extends D04 T02 §6 export presets |
| LP-0877 | Multi-preset batch export: one file per ticked preset, parent folder, per-preset destinations, conflict suffix | LR-1051, LR-1052, LR-1053 | -- | -- | automation | plan D04 T12 §13 |  |
| LP-0878 | Add exported files to the catalog and stack them with the original | LR-1059, LR-1060 | -- | -- | core | plan D04 T12 §13 |  |
| LP-0879 | Export metadata choices: copyright only, copyright and contact, all except camera or camera raw info, all, remove person info, remove location, hierarchical keywords | LR-1094, LR-1095, LR-1096, LR-1097, LR-1098, LR-1099, LR-1100, LR-1101 | -- | -- | core | plan D04 T12 §13 | extends D04 T02 §6 metadata choices |
| LP-0880 | Export watermark with the watermark editor: text or graphic, effects, presets | LR-1102, LR-1103, LR-1104, LR-1105, LR-1106, LR-1416 | -- | -- | core | plan D04 T12 §13 | consumes the D04 T11 §8 watermark engine |
| LP-0881 | Post-processing after export: nothing, show in Explorer, open in Pinxit or another application, export actions folder | LR-1107, LR-1108, LR-1109, LR-1110, LR-1111, LR-1112 | -- | -- | automation | plan D04 T12 §13 | export actions run programs the user placed in the folder |
| LP-0882 | Export completion sound | LR-1115 | -- | -- | core | plan D04 T12 §13 |  |
| LP-0883 | Export warning when stored AI results need updating | LR-1117 | -- | -- | ai | plan D04 T12 §13 | names photos whose AI masks need recomputing |
| LP-0884 | Export actions folder: programs run after export | LR-1384 | -- | -- | automation | plan D04 T12 §13 |  |
| LP-0885 | Export from develop: several copies with their own format and size | -- | AC-2089, AC-2156, AC-2353, AC-4440, AC-4564, AC-4663, AC-4925 | -- | core | plan D04 T12 §13 | extends D04 T02 §6 |
| LP-0886 | Export rename template with original-name and sequence tokens, metadata fields, recent templates, start number | -- | AC-2160, AC-2161, AC-2162, AC-2163, AC-2164, AC-2165, AC-2166, AC-2167 | -- | core | plan D04 T12 §13 | token engine from D04 T11 §2 |
| LP-0887 | Export metadata options: preserve metadata, catalog information, and last-modified date | -- | AC-2191, AC-2192, AC-2193 | -- | core | plan D04 T12 §13 |  |
| LP-0888 | Export presets: several presets at once, save current, presets listed in the menu | -- | AC-2194, AC-2195 | -- | core | plan D04 T12 §13 | extends D04 T02 §6 export presets |
| LP-0889 | Export dialog to a hard drive destination with progress and cancel | LR-1042, LR-1043, LR-1116, LR-1391, LR-1642 | -- | -- | core | shipped-scope D04 T02 §6 |  |
| LP-0890 | Existing files on export: ask, new name, overwrite, skip | LR-1061 | -- | -- | core | shipped-scope D04 T02 §6 |  |
| LP-0891 | Export JPEG with quality and PNG and TIFF with compression | LR-1067, LR-1068, LR-1072, LR-1073, LR-1075 | -- | -- | format | shipped-scope D04 T02 §6 |  |
| LP-0892 | Export do not enlarge | LR-1087 | -- | -- | core | shipped-scope D04 T02 §6 |  |
| LP-0893 | Output sharpening for screen, matte, or glossy at low, standard, or high | LR-1090, LR-1091, LR-1092, LR-1093 | -- | -- | print | shipped-scope D04 T02 §6 |  |
| LP-0894 | Content Credentials on export | LR-1041 | -- | -- | cloud | backlog B-047 |  |

## Print and contact sheets

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0895 | Print module | LR-0006 | -- | -- | print | plan D04 T12 §4 |  |
| LP-0896 | Print layout single image and contact sheet grid: image settings, units, margins, page grid, cell spacing and size, guides | LR-1216, LR-1219, LR-1220, LR-1221, LR-1222, LR-1223, LR-1224, LR-1225, LR-1226, LR-1227, LR-1228, LR-1551, LR-1826, LR-1827, LR-1828, LR-1829, LR-1830, LR-1831 | -- | -- | print | plan D04 T12 §4 |  |
| LP-0897 | Print job: to printer or JPEG file, draft mode, file resolution, print resolution, JPEG quality, custom file dimensions, 16-bit output | LR-1237, LR-1238, LR-1239, LR-1240, LR-1242, LR-1243, LR-1244, LR-1252 | -- | -- | print | plan D04 T12 §4 |  |
| LP-0898 | Print sharpening for matte or glossy | LR-1241 | -- | -- | print | plan D04 T12 §4 | consumes the export output sharpening of D04 T02 §6 |
| LP-0899 | Print color management: printer profile, rendering intent, print adjustment brightness and contrast | LR-1245, LR-1246, LR-1247 | -- | -- | print | plan D04 T12 §4 | consumes D01 T04 |
| LP-0900 | Page setup, printer settings, print, print one copy | LR-1248, LR-1249, LR-1250, LR-1251, LR-1402, LR-1403, LR-1645, LR-1646, LR-1821, LR-1822, LR-1823 | -- | -- | print | plan D04 T12 §4 |  |
| LP-0901 | Saved print collections, page navigation, and which photos print | LR-1253, LR-1254, LR-1255, LR-1549, LR-1550, LR-1824, LR-1825, LR-1834 | -- | -- | print | plan D04 T12 §4 |  |
| LP-0902 | Print images with live preview from browse and the viewer, print all images | -- | AC-1333, AC-1989, AC-1994, AC-4433, AC-4568 | -- | print | plan D04 T12 §4 |  |
| LP-0903 | Printer options: printer, paper, orientation, copies, page range, resolution | -- | AC-1344, AC-1345, AC-1346, AC-1347, AC-1348, AC-1349, AC-1990 | -- | print | plan D04 T12 §4 |  |
| LP-0904 | Print color management by printer or Albumen with printer profile, rendering intent, soft proof, gamut warning | -- | AC-1358, AC-1359, AC-1360, AC-1361, AC-1362 | -- | print | plan D04 T12 §4 | consumes D01 T04 §2 |
| LP-0905 | Print from the viewer: print dialog, direct print with current settings, Quick View print with captions and headers | -- | AC-4006, AC-4567 | IV-0122, IV-0123, IV-1464, IV-1532 | print | plan D04 T12 §4 |  |
| LP-0906 | Print selected images as single pages | -- | -- | IV-0920 | print | plan D04 T12 §4 |  |
| LP-0907 | Print template browser and saving print templates | LR-1215, LR-1256, LR-1548, LR-1832, LR-1833 | -- | -- | print | plan D04 T12 §5 |  |
| LP-0908 | Picture package and custom package layouts with rulers, grid snap, cells, and auto layout | LR-1217, LR-1218, LR-1234, LR-1235, LR-1236 | -- | -- | print | plan D04 T12 §5 |  |
| LP-0909 | Print page overlays: background color, identity plate, watermark, page numbers, page info, crop marks, photo info captions | LR-1229, LR-1230, LR-1231, LR-1232, LR-1233 | -- | -- | print | plan D04 T12 §5 |  |
| LP-0910 | Print layouts: full page, contact sheet, predefined multi-image layouts, prints per photo | -- | AC-1336, AC-1337, AC-1338, AC-1339, AC-1995, AC-1996, AC-1997 | -- | print | plan D04 T12 §5 |  |
| LP-0911 | Print resampling filters: box, triangle, bicubic, bell, B-spline, Lanczos, Mitchell | -- | AC-1350, AC-1351, AC-1352, AC-1353, AC-1354, AC-1355, AC-1356 | -- | print | plan D04 T12 §5 | consumes D01 T03 §2 resampler |
| LP-0912 | Print gamma and printer exposure, contrast, and sharpness adjustments | -- | AC-1357, AC-1371, AC-1372, AC-1373, AC-1992 | -- | print | plan D04 T12 §5 |  |
| LP-0913 | EXIF print information sharing with printers | -- | AC-1363 | -- | print | plan D04 T12 §5 |  |
| LP-0914 | Custom print formats and page settings: position, margins, number of prints, auto rotate, crop or shrink to fit | -- | AC-1364, AC-1365, AC-1366, AC-1367, AC-1368, AC-1369, AC-1370, AC-1991 | -- | print | plan D04 T12 §5 |  |
| LP-0915 | Print captions, headers, and footers with fonts, metadata, page numbers, alignment, line limits | -- | AC-1374, AC-1375, AC-1376, AC-1377, AC-1378, AC-1379, AC-1380, AC-1381, AC-1382, AC-1383, AC-1993 | -- | print | plan D04 T12 §5 | tokens from D04 T11 §2 |
| LP-0916 | IrfanView print dialog: printer, orientation with auto rotate, setup, default printer, remembered driver values, color or black and white preview | -- | -- | IV-0128, IV-0129, IV-0130, IV-0131, IV-0132, IV-0151, IV-0152 | print | plan D04 T12 §5 |  |
| LP-0917 | Print size modes: original DPI, best fit, fill paper, stretch, custom size and margins, scale, center, negative positions, borderless, no overflow | -- | -- | IV-0133, IV-0134, IV-0135, IV-0136, IV-0137, IV-0138, IV-0139, IV-0140, IV-0141, IV-0142 | print | plan D04 T12 §5 |  |
| LP-0918 | Print profiles and saving print settings without printing | -- | -- | IV-0143, IV-0150 | print | plan D04 T12 §5 |  |
| LP-0919 | Print header and footer text with placeholders | -- | -- | IV-0144 | print | plan D04 T12 §5 | tokens from D04 T11 §2 |
| LP-0920 | Multipage printing: specific pages, odd or even, reverse, all pages, copies, collate | -- | -- | IV-0145, IV-0146, IV-0147, IV-0148, IV-0149, IV-0154 | print | plan D04 T12 §5 |  |
| LP-0921 | Print only the current selection | -- | -- | IV-0153 | print | plan D04 T12 §5 | selection from D04 T04 §11 |
| LP-0922 | Create contact sheet as image files or HTML image maps: output name, columns and rows, spacing, frames, thumbnail effects, page background, text, presets | -- | AC-1299, AC-1300, AC-1301, AC-1302, AC-1303, AC-1304, AC-1305, AC-1306, AC-1307, AC-1308, AC-1309, AC-1310, AC-1311, AC-1312, AC-1313, AC-1314, AC-1315 | -- | print | plan D04 T12 §6 |  |
| LP-0923 | Print contact sheet format: preset, size and spacing, frames, thumbnail effects, page background | -- | AC-1384, AC-1385, AC-1386, AC-1387, AC-1388 | -- | print | plan D04 T12 §6 |  |
| LP-0924 | Contact sheet from a selection: columns and rows, cell size and spacing, paper size, header, footer, captions with placeholders, stretch small, background | -- | -- | IV-0893, IV-0894, IV-0895, IV-0896, IV-0897, IV-0898, IV-0899, IV-0904 | core | plan D04 T12 §6 |  |
| LP-0925 | Contact sheet output: file name pattern, destination, save, print, or show, profiles, one image from selected thumbnails | -- | -- | IV-0900, IV-0901, IV-0902, IV-0903, IV-0908 | print | plan D04 T12 §6 |  |

## Slideshow

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0926 | Slideshow module | LR-0005 | -- | -- | core | plan D04 T12 §7 |  |
| LP-0927 | Slideshow template browser with preview, user templates, folders, import and export, save template | LR-1177, LR-1178, LR-1213, LR-1214, LR-1543, LR-1544, LR-1817, LR-1818, LR-1819 | -- | -- | core | plan D04 T12 §7 |  |
| LP-0928 | Slide options and layout: zoom to fill, stroke border, cast shadow, margins, aspect preview | LR-1180, LR-1181, LR-1182, LR-1183, LR-1184, LR-1813 | -- | -- | core | plan D04 T12 §7 |  |
| LP-0929 | Slideshow overlays: identity plate, watermark, rating stars, text overlays with shadow, add text tool with metadata tokens | LR-1185, LR-1186, LR-1187, LR-1188, LR-1189, LR-1190, LR-1546 | -- | -- | core | plan D04 T12 §7 | tokens from D04 T11 §2 |
| LP-0930 | Slideshow backdrop: color wash, background image, background color | LR-1191, LR-1192, LR-1193 | -- | -- | core | plan D04 T12 §7 |  |
| LP-0931 | Slideshow intro and ending title screens | LR-1194, LR-1195 | -- | -- | core | plan D04 T12 §7 |  |
| LP-0932 | Slideshow header and footer captions with alignment, background, font, and metadata tags | -- | AC-1210, AC-1211, AC-1212, AC-1213, AC-1214, AC-1215, AC-1216 | -- | core | plan D04 T12 §7 | tokens from D04 T11 §2 |
| LP-0933 | Slideshow sources, saved slideshow collections, and which photos play | LR-1179, LR-1211, LR-1212 | -- | -- | core | plan D04 T12 §8 |  |
| LP-0934 | Slideshow music: tracks, fit slides to music | LR-1196, LR-1197 | -- | -- | core | plan D04 T12 §8 | audio playback through Windows Media Foundation over Vortice.MediaFoundation (MIT), the player of D04 T04 §8 |
| LP-0935 | Slideshow playback: manual or auto, duration, fades and color, pan and zoom, random, repeat, screen, quality, preview, play | LR-1199, LR-1200, LR-1201, LR-1202, LR-1203, LR-1204, LR-1205, LR-1206, LR-1207, LR-1547, LR-1808, LR-1809, LR-1810, LR-1811, LR-1812, LR-1820 | -- | -- | core | plan D04 T12 §8 |  |
| LP-0936 | Export slideshow as PDF and as JPEG slides | LR-1208, LR-1209, LR-1545, LR-1814, LR-1815 | -- | -- | core | plan D04 T12 §8 |  |
| LP-0937 | Play slideshow of selected images, a folder, or a folder with subfolders, with the Configure dialog and remembered contents | -- | AC-1183, AC-1184, AC-1185, AC-1186, AC-1187, AC-1188, AC-4494 | -- | core | plan D04 T12 §8 | videos in slideshows are D04 T16 §6 |
| LP-0938 | Slideshow transitions: choose, random, preview | -- | AC-1189, AC-1190 | -- | core | plan D04 T12 §8 |  |
| LP-0939 | Slideshow variations: pan and zoom, 2-up, 4-up, collage | -- | AC-1191, AC-1192, AC-1193, AC-1194, AC-1195 | -- | core | plan D04 T12 §8 |  |
| LP-0940 | Slideshow display effects: black and white, sepia, vivid, soft | -- | AC-1196, AC-1197, AC-1198, AC-1199, AC-1200 | -- | core | plan D04 T12 §8 |  |
| LP-0941 | Slideshow background color, duration, stretch small images, autohide controls, loop, order | -- | AC-1201, AC-1202, AC-1203, AC-1206, AC-1207, AC-1208 | -- | core | plan D04 T12 §8 |  |
| LP-0942 | Slideshow background music from folders | -- | AC-1209 | -- | video | plan D04 T12 §8 |  |
| LP-0943 | Save slideshow settings as default | -- | AC-1217 | -- | core | plan D04 T12 §8 |  |
| LP-0944 | Slideshow project content: images, per-image transitions, durations, captions, timing, order, hidden controls, background audio, transition quality, output size | -- | AC-1223, AC-1224, AC-1225, AC-1227, AC-1228, AC-1229, AC-1230, AC-1231, AC-1232 | -- | core | plan D04 T12 §8 | saved as a Albumen slideshow project |
| LP-0945 | Standalone slideshow executable and screen saver files with the Create Slideshow File wizard and projects | -- | AC-1218, AC-1219, AC-1220, AC-1222 | -- | core | backlog B-049 |  |
| LP-0946 | ACDSee Showroom desktop slideshow windows with options | -- | AC-1233, AC-1234, AC-1235, AC-1236, AC-1237, AC-1238, AC-1239, AC-4296, AC-4297, AC-4298, AC-4299, AC-4300, AC-4301, AC-4302, AC-4303, AC-4304, AC-4305, AC-4306, AC-4307, AC-4308, AC-4309, AC-4310 | -- | core | backlog B-049 |  |
| LP-0947 | Flash slideshow file | -- | AC-1221 | -- | format | excluded: removed Adobe Flash Player |  |

## Web, books, and documents

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0948 | Print PDF and Office documents with page ranges, duplex, pages per sheet, collation, and the mixed file type rule | -- | AC-1334, AC-1335, AC-1340, AC-1341, AC-1342, AC-1343, AC-1998, AC-1999, AC-2000 | -- | print | plan D04 T12 §5 | PDF pages through the D04 T13 §4 PDF reader; Office documents are other-app territory and print through the Windows print verb |
| LP-0949 | Web module | LR-0007 | -- | -- | core | plan D04 T12 §9 |  |
| LP-0950 | Web gallery templates and layout styles with save, update, import, and export | LR-1257, LR-1258, LR-1274, LR-1552, LR-1851, LR-1852 | -- | -- | core | plan D04 T12 §9 | own HTML templates |
| LP-0951 | Web gallery site info, color palette, appearance, and image info with click-to-edit preview | LR-1259, LR-1260, LR-1261, LR-1262, LR-1276 | -- | -- | core | plan D04 T12 §9 |  |
| LP-0952 | Web gallery output settings: JPEG quality, metadata, watermark, sharpening, HDR AVIF images | LR-1263, LR-1264, LR-1265, LR-1266, LR-1277 | -- | -- | core | plan D04 T12 §9 |  |
| LP-0953 | Upload a web gallery to the user's own FTP or SFTP server with presets and subfolder | LR-1267, LR-1268, LR-1272, LR-1557 | -- | -- | cloud | plan D04 T12 §9 | FTP and FTPS through FluentFTP (MIT, approved by the operator 2026-09-27); the SFTP protocol option is backlog B-053 (SSH.NET was not approved) |
| LP-0954 | Web gallery preview in browser, reload, export to folder, advanced settings, web collections, which photos | LR-1269, LR-1270, LR-1271, LR-1273, LR-1275, LR-1278, LR-1553, LR-1554, LR-1555, LR-1556, LR-1848, LR-1849, LR-1850, LR-1853, LR-1854 | -- | -- | core | plan D04 T12 §9 |  |
| LP-0955 | HTML album wizard: gallery styles, preview, generate, title, header and footer with image or text, folder, thumbnail and image settings, slideshow duration, colors and fonts, saved style settings | -- | AC-1257, AC-1258, AC-1259, AC-1260, AC-1261, AC-1262, AC-1263, AC-1264, AC-1265, AC-1266, AC-1267, AC-1268, AC-1269, AC-1270, AC-1271, AC-1272 | -- | core | plan D04 T12 §9 |  |
| LP-0956 | HTML gallery export from thumbnails: title, thumbs and images folders, prefix, captions with placeholders, link target, browsing frames, no-frame thumbs, extra files, editable templates | -- | -- | IV-0910, IV-0911, IV-0912, IV-0913, IV-0914, IV-0915, IV-0916, IV-0917, IV-0918, IV-0919 | core | plan D04 T12 §9 |  |
| LP-0957 | HTML gallery template placeholders: title, background color, image and thumbnail links, previous, next, back and self links, image name parts, size, text, alignment, target, image arrays | -- | -- | IV-1851, IV-1852, IV-1853, IV-1854, IV-1855, IV-1856, IV-1857, IV-1858, IV-1859, IV-1860, IV-1861, IV-1862, IV-1863, IV-1864, IV-1865, IV-1866, IV-1867, IV-1868, IV-1869, IV-1870, IV-1871, IV-1872, IV-1873, IV-1874, IV-1875, IV-1876, IV-1877, IV-1878, IV-1879, IV-1880 | automation | plan D04 T12 §9 | templates use D04 T11 §2 tokens for text |
| LP-0958 | Book module | LR-0004 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0959 | Book settings: PDF or JPEG book output with quality, color profile, resolution, sharpening, media type | LR-1143, LR-1149 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0960 | Book auto layout with layout presets and clear layout | LR-1150, LR-1151, LR-1152, LR-1541 | -- | -- | automation | plan D04 T12 §10 |  |
| LP-0961 | Book pages: page templates, add, remove, duplicate, custom layouts, copy and paste layout | LR-1153, LR-1154, LR-1166, LR-1167, LR-1169, LR-1538, LR-1539, LR-1589, LR-1590, LR-1591 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0962 | Book page numbers and page captions | LR-1155, LR-1156, LR-1588 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0963 | Book guides, cells, and photo zoom in cells | LR-1157, LR-1158, LR-1159, LR-1176, LR-1540, LR-1592, LR-1593, LR-1595 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0964 | Book text: photo and page text from metadata, type settings, style presets, targeted type adjustment, metadata caption refresh | LR-1160, LR-1161, LR-1162, LR-1163, LR-1164, LR-1175, LR-1594 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0965 | Book backgrounds per page or global | LR-1165 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0966 | Book views, saving a book collection, export to PDF and JPEG, book preferences | LR-1168, LR-1170, LR-1172, LR-1173, LR-1174, LR-1536, LR-1537, LR-1542, LR-1582, LR-1583, LR-1584, LR-1585, LR-1586, LR-1587 | -- | -- | print | plan D04 T12 §10 |  |
| LP-0967 | Create menu: slideshow files, PDF, PowerPoint, albums, archives | -- | AC-0050 | -- | core | plan D04 T12 §11 |  |
| LP-0968 | Create PDF: slideshow PDF, one PDF for all images, one per image, order, transitions, background, names and location | -- | AC-1240, AC-1241, AC-1242, AC-1243, AC-1244, AC-1245, AC-1246, AC-1247 | -- | core | plan D04 T12 §11 | Isotone.Core PDF writer |
| LP-0969 | Create PowerPoint: new or existing presentation, slide duration, images per slide, linked images, design template, captions, titles, notes | -- | AC-1248, AC-1249, AC-1250, AC-1251, AC-1252, AC-1253, AC-1254, AC-1255, AC-1256 | -- | core | plan D04 T12 §11 | own OpenXML writer, no PowerPoint needed |
| LP-0970 | Multi-page TIFF or PDF from a selection | -- | -- | IV-0906 | core | plan D04 T12 §11 |  |
| LP-0971 | Send images by email: MAPI or SMTP, address book, downsize large images | -- | -- | IV-0643, IV-0644, IV-0645, IV-0646, IV-0647, IV-1489 | core | plan D04 T12 §12 |  |

## Formats

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-0972 | Animated image viewing: animated GIF, APNG, animated WebP, animated AVIF playback | -- | -- | IV-1223, IV-1224, IV-1225 | format | plan D04 T04 §10 | viewing only; authoring is Pinxit's D03 T23 §5 |
| LP-0973 | Drag a file from Albumen into another application | -- | AC-1962 | -- | format | plan D04 T05 §6 |  |
| LP-0974 | Archive formats: browse and read ZIP, RAR, 7z, ARJ, CAB, GZ, TAR, TGZ like folders, write ZIP | -- | AC-5140, AC-5141, AC-5142, AC-5143, AC-5144, AC-5145, AC-5146, AC-5177 | -- | format | plan D04 T05 §12 | SharpCompress (MIT), read-only for RAR |
| LP-0975 | File descriptions read from descript.ion files | -- | AC-5176 | -- | core | plan D04 T08 §8 | read as captions; Albumen writes descriptions to sidecars |
| LP-0976 | Apply DNG opcode lens and distortion corrections automatically | -- | AC-5175 | -- | core | plan D04 T09 §6 | consumes D01 T07 §3 |
| LP-0977 | Legacy RAW pipeline emulation for photos developed with an older process | -- | AC-5174 | -- | core | plan D04 T09 §7 | Albumen process versions |
| LP-0978 | Apply a develop preset to many RAW files from browse | -- | AC-5173 | -- | automation | plan D04 T11 §9 |  |
| LP-0979 | Save images as PDF: title, subject, author, keywords, per-color-type compression, security passwords and permissions, paper size and fit | -- | -- | IV-0212, IV-0213, IV-0214, IV-0215, IV-1069 | format | plan D04 T12 §11 | consumes the Isotone.Core PDF writer moved by D03 T17 §7 |
| LP-0980 | Export a developed image to several formats at once | -- | AC-5172 | -- | core | plan D04 T12 §13 | extends D04 T02 §6 |
| LP-0981 | Common formats JPEG, PNG, TIFF, GIF, and BMP read and write, including CMYK JPEG, high bit depth and float TIFF, and alpha in every format that carries it | -- | AC-5046, AC-5052, AC-5061, AC-5067, AC-5071, AC-5126, AC-5127, AC-5130, AC-5133, AC-5138 | IV-1126, IV-1145, IV-1154, IV-1168, IV-1183, IV-1232, IV-1245, IV-1246 | format | plan D04 T13 §1 | consumes Pinxit codecs moved to Isotone.Core by D04 T13 §1 |
| LP-0982 | Fix a wrong file extension detected on load | -- | -- | IV-1003 | core | plan D04 T13 §1 | content sniffing |
| LP-0983 | Format support ships in the app: no separate plug-in package, and format handlers can be enabled or disabled | -- | -- | IV-1110, IV-1111, IV-1120 | format | plan D04 T13 §1 |  |
| LP-0984 | Detect the real format by content, offer to fix a wrong extension, and extension rules for header-less formats | -- | -- | IV-1243, IV-1244 | format | plan D04 T13 §1 |  |
| LP-0985 | AVIF and HEIF read and write, including HIF, HEIC through libheif, animated AVIF as first frame | -- | AC-5045, AC-5055, AC-5125, AC-5180 | IV-1045, IV-1123, IV-1147, IV-1234 | format | plan D04 T13 §2 | consumes D03 T17 §5 (libavif BSD-2, libheif LGPL-3.0); AVIF sidecar XMP is read |
| LP-0986 | HDR and scientific formats: OpenEXR, Radiance HDR, FITS, DPX and Cineon | -- | AC-5054 | IV-1053, IV-1057, IV-1134, IV-1140, IV-1141, IV-1213 | format | plan D04 T13 §2 | consumes D03 T17 §6; DPX and Cineon own reader from SMPTE 268M |
| LP-0987 | JPEG 2000 read and write: JP2, JPC, J2K with 48-bit color | -- | AC-5059, AC-5060, AC-5129 | IV-1075, IV-1153 | format | plan D04 T13 §2 | consumes D03 T17 §5 |
| LP-0988 | JPEG XL read and write | -- | AC-5062, AC-5131 | IV-1074, IV-1157 | format | plan D04 T13 §2 | consumes D03 T17 §5 (libjxl BSD-3) |
| LP-0989 | WebP read and write including transparency | -- | AC-5073, AC-5136 | IV-1106, IV-1190 | format | plan D04 T13 §2 | consumes D03 T17 §5 (libwebp BSD-3) |
| LP-0990 | QOI read and write | -- | -- | IV-0226, IV-1173 | format | plan D04 T13 §2 | consumes D03 T17 §5 |
| LP-0991 | JPEG XR and HD Photo read: HDP, JXR, WDP | -- | -- | IV-1066, IV-1146 | format | plan D04 T13 §2 | consumes D03 T17 §5 (jxrlib BSD-2) |
| LP-0992 | Photoshop ABR brush files browsed as images: preview, per-brush navigation | -- | AC-1958, AC-1959, AC-1960, AC-1961 | -- | format | plan D04 T13 §3 | ABR tips decoded by the reader of D03 T12 §3 moved to Isotone.Core |
| LP-0993 | Windows icons and cursors: ICO with every resolution as a page, CUR, animated ANI | -- | AC-5044, AC-5048, AC-5057 | IV-1122, IV-1149, IV-1210 | format | plan D04 T13 §3 | consumes D03 T17 §8 |
| LP-0994 | PCX and multi-page DCX read and write | -- | AC-5050, AC-5065, AC-5132 | IV-1164 | format | plan D04 T13 §3 | consumes D03 T17 §8 |
| LP-0995 | PSD and PSB composite read and flattened PSD write | -- | AC-5068, AC-5134 | IV-1170, IV-1226 | format | plan D04 T13 §3 | consumes D03 T17 §2 and §3 moved to Isotone.Core; layered editing is Pinxit |
| LP-0996 | TGA read and write | -- | AC-5070, AC-5137 | IV-1182 | format | plan D04 T13 §3 | consumes D03 T17 §8 |
| LP-0997 | WBMP read and write | -- | AC-5072, AC-5135 | IV-1189 | format | plan D04 T13 §3 | consumes D03 T17 §8 |
| LP-0998 | DICOM medical images: DCM, ACR, IMA | -- | -- | IV-1051, IV-1131 | format | plan D04 T13 §3 | consumes D03 T17 §6 (own reader; fo-dicom is MS-PL) |
| LP-0999 | Paint Shop Pro PSP, Seattle FilmWorks SFW, and Paint.NET PDN read | -- | -- | IV-1070, IV-1166, IV-1171, IV-1177 | format | plan D04 T13 §3 | PSP and SFW consume D03 T17 §9; PDN own reader |
| LP-1000 | GIMP XCF read (flattened) | -- | -- | IV-1109, IV-1194 | format | plan D04 T13 §3 | consumes D03 T17 §4 moved to Isotone.Core |
| LP-1001 | Game and texture formats: DDS, Dreamcast PVR, WAD3, Quake WAL, Blizzard BLP | -- | -- | IV-1132, IV-1172, IV-1186, IV-1187, IV-1219 | format | plan D04 T13 §3 | DDS and PVR consume D03 T17 §8 and §9 |
| LP-1002 | Icons from EXE, DLL, and ICL icon libraries | -- | -- | IV-1148, IV-1214, IV-1231 | format | plan D04 T13 §3 |  |
| LP-1003 | X11 bitmaps XBM and XPM, PBM, PGM, PPM read | -- | -- | IV-1162, IV-1167, IV-1169, IV-1193, IV-1195 | format | plan D04 T13 §3 | consumes D03 T17 §8 |
| LP-1004 | Documents in the viewer: PDF and XPS viewing with rating, label, and tag, and a per-type choice to open documents in the viewer or their own application | -- | AC-1930, AC-1934, AC-4330, AC-5170 | -- | core | plan D04 T13 §4 | XPS through WPF DocumentViewer; Office documents are other-app: none |
| LP-1005 | PDF viewing: open, page back and forward, zoom, fit page and fit width, page number and magnification readouts, page and scroll keys, next file, open in default app, print | -- | AC-1935, AC-1936, AC-1937, AC-1938, AC-1939, AC-1940, AC-1941, AC-1942, AC-1943, AC-1944, AC-1945, AC-1946, AC-1947, AC-1948, AC-5161 | IV-1165 | format | plan D04 T13 §4 | consumes the PDFium reader of D03 T17 §7, moved to Isotone.Core by D04 T13 §1 |
| LP-1006 | Vector and metafile images rendered as pixels: SVG, EMF, WMF, WordPerfect WPG | -- | AC-5051, AC-5069, AC-5074 | IV-1101, IV-1107, IV-1138, IV-1181, IV-1191, IV-1229 | format | plan D04 T13 §4 | consumes the SVG and metafile readers of D03 T17 §7 |
| LP-1007 | Open a text file and render it as an image, with text font and colors | -- | -- | IV-0084, IV-0759 | core | plan D04 T13 §4 |  |
| LP-1008 | Create and edit multipage TIFF and PDF: build from files or a list, arrange, delete, add pages, append the current image | -- | -- | IV-0631, IV-0632, IV-0633, IV-0634, IV-0635, IV-1465 | core | plan D04 T13 §4 | writes a new file, never the original |
| LP-1009 | Extract pages of multipage files: range, format, name suffix | -- | -- | IV-0636, IV-0637, IV-0638, IV-0639 | core | plan D04 T13 §4 |  |
| LP-1010 | Ghostscript location and antialiasing, PDF engine and render size, SVG render size | -- | -- | IV-1011, IV-1012, IV-1013 | format | plan D04 T13 §4 | user-installed Ghostscript, never bundled (AGPL) |
| LP-1011 | DjVu read with pages | -- | -- | IV-1052, IV-1133 | format | plan D04 T13 §4 | DjVuLibre (GPL-2.0-or-later) |
| LP-1012 | PDF and PostScript reading through the PDF and PostScript plug-ins: PDF, EPS, PS, AI through a user-installed Ghostscript of matching bitness | -- | -- | IV-1090, IV-1092, IV-1118, IV-1139 | format | plan D04 T13 §4 | consumes D03 T17 §7; Ghostscript is AGPL-3.0, run as an external process, never bundled |
| LP-1013 | Text files shown as images | -- | -- | IV-1185 | format | plan D04 T13 §4 |  |
| LP-1014 | Multi-page containers: TIFF, DCX, ICO, PDF, DjVu pages, and MPO multi-picture objects | -- | -- | IV-1217, IV-1242 | format | plan D04 T13 §4 | page navigation is D04 T04 §10 |
| LP-1015 | RAW plus JPEG pairs: treat the JPEG as a sidecar or as a separate photo | LR-0127, LR-0144 | -- | -- | core | plan D04 T13 §5 |  |
| LP-1016 | DNG with JPEG XL compression | -- | AC-5096 | -- | format | plan D04 T13 §5 | needs a decoder release with JXL-compressed DNG support, checked in the coverage table |
| LP-1017 | RAW camera coverage table by maker and model, decoder updates for new cameras, and how to request an unlisted camera | -- | AC-5097, AC-5098, AC-5099, AC-5100, AC-5101, AC-5102, AC-5103, AC-5104, AC-5105, AC-5106, AC-5107, AC-5108, AC-5109, AC-5110, AC-5111, AC-5112, AC-5113, AC-5114, AC-5115, AC-5116, AC-5117, AC-5118, AC-5119, AC-5120, AC-5121, AC-5122, AC-5123 | -- | format | plan D04 T13 §5 | extends D04 T01 §4; unsupported models are reported to the decoder upstream |
| LP-1018 | JPEG save options: quality, progressive, optimized Huffman tables, chroma subsampling, grayscale, saved defaults and named option profiles | -- | AC-4369, AC-4370, AC-4371, AC-4372, AC-4373, AC-4378 | IV-0173, IV-0174, IV-0175, IV-0176, IV-0186 | format | plan D04 T13 §6 | consumes D03 T17 §11 moved to Isotone.Core by D04 T13 §1; shared by export, convert, and Save As |
| LP-1019 | JPEG metadata carry-over on save: keep EXIF, IPTC, XMP, and comment, reset orientation, embedded and DCF thumbnail policy | -- | AC-4374, AC-4375, AC-4376, AC-4377 | IV-0177, IV-0178, IV-0179, IV-0180, IV-0181, IV-0182 | format | plan D04 T13 §6 | writes new files only, never the original (original-file guard) |
| LP-1020 | Format options dialog shown automatically on Save As for formats with options | -- | -- | IV-0114 | core | plan D04 T13 §6 |  |
| LP-1021 | JPEG size targeting: reuse the estimated original quality, target a file size, preview dialog to tune quality | -- | -- | IV-0183, IV-0184, IV-0185 | format | plan D04 T13 §6 |  |
| LP-1022 | GIF save options: interlaced, automatic and custom transparent color, palette index, window color, single frame only | -- | -- | IV-0187, IV-0188, IV-0189, IV-0190, IV-0191, IV-0192 | format | plan D04 T13 §6 | animated GIF authoring is Pinxit's D03 T23 §5 |
| LP-1023 | PNG save options: compression level, automatic and custom transparency, window color, synthetic alpha, optimized PNG | -- | -- | IV-0193, IV-0194, IV-0195, IV-0196, IV-0197, IV-0198, IV-1088 | format | plan D04 T13 §6 | optimization by own zlib pass or oxipng (MIT); OptiPNG is zlib-licensed |
| LP-1024 | Legacy save options: PNM binary or ASCII, ICO transparency and window color, TGA and BMP RLE | -- | -- | IV-0199, IV-0200, IV-0201, IV-0224, IV-0225 | format | plan D04 T13 §6 |  |
| LP-1025 | TIFF save options: color and 1-bit compression, grayscale palette, save all pages | -- | -- | IV-0202, IV-0203, IV-0204, IV-0205 | format | plan D04 T13 §6 | consumes D03 T17 §11 |
| LP-1026 | JPEG 2000 save options: quality, target bytes, lossless | -- | -- | IV-0206, IV-0207, IV-0208 | format | plan D04 T13 §6 | OpenJPEG (BSD-2-Clause) through D03 T17 §5 |
| LP-1027 | WebP and JPEG XL save options: quality, lossless, effort, keep metadata | -- | -- | IV-0216, IV-0217, IV-0218, IV-0219, IV-0220 | format | plan D04 T13 §6 | consumes D03 T17 §5 |
| LP-1028 | Restrict which formats appear in save dialogs | -- | -- | IV-0227 | format | plan D04 T13 §6 |  |
| LP-1029 | GoPro GPR write | -- | AC-5128 | -- | format | plan D04 T13 §7 | GPR is DNG with VC-5; gpr SDK (Apache-2.0 or MIT) |
| LP-1030 | Embedded thumbnails of Affinity and Canvas documents | -- | AC-5043, AC-5047, AC-5049 | -- | format | plan D04 T13 §8 | thumbnail only; opening Affinity files is Pinxit B-045 |
| LP-1031 | Rare and legacy raster formats: Formats plug-in set, Amiga, Atari, C64, ZX Spectrum, GEM IMG, IFF and LBM, Sun raster, SGI and RGBA, SIF, G3 fax, Structured Fax, Casio CAM, Windows clipboard CLP, GLCD, MAKI MAG, Utah RLE, Mosaic, Bio-RAD, ICS, AT&T ICN | -- | AC-5056 | IV-1063, IV-1068, IV-1097, IV-1127, IV-1128, IV-1144, IV-1150, IV-1151, IV-1152, IV-1174, IV-1176, IV-1178, IV-1179, IV-1196, IV-1212, IV-1216, IV-1218, IV-1220, IV-1221, IV-1227 | format | plan D04 T13 §8 | own managed codecs from published descriptions; SGI and Sun raster consume D03 T17 §8 |
| LP-1032 | Kodak Photo CD read up to 16BASE | -- | AC-5064 | IV-1091, IV-1163 | format | plan D04 T13 §8 | own reader from the published format notes |
| LP-1033 | Macintosh PICT and QuickTime image read | -- | AC-5066 | IV-1158 | format | plan D04 T13 §8 | own reader for bitmap opcodes; no QuickTime dependency |
| LP-1034 | Open any file as raw pixel data: width, height, header, bit depth, color order, planar or interleaved, flip | -- | -- | IV-0085, IV-0086 | format | plan D04 T13 §8 |  |
| LP-1035 | JPEG-LS lossless and near-lossless read and write | -- | -- | IV-0221, IV-1073, IV-1155 | format | plan D04 T13 §8 | CharLS (BSD-3-Clause) |
| LP-1036 | Raw binary pixel data and YUV: read and write with header, interleaved or planar, and channel order | -- | -- | IV-0223, IV-1175, IV-1222 | format | plan D04 T13 §8 | consumes the raw image data codec of D03 T17 §6 |
| LP-1037 | Photo CD load resolution | -- | -- | IV-0936 | core | plan D04 T13 §8 |  |
| LP-1038 | TIFF annotations display | -- | -- | IV-0953 | core | plan D04 T13 §8 |  |
| LP-1039 | Font file sample text rendering | -- | -- | IV-1009 | format | plan D04 T13 §8 |  |
| LP-1040 | FLIF, Webshots WBZ and WBC, and WSQ fingerprint images read | -- | -- | IV-1062, IV-1105, IV-1108, IV-1142, IV-1188, IV-1192 | format | plan D04 T13 §8 | WSQ from NIST NBIS (public domain) |
| LP-1041 | MNG and JNG, and Autodesk FLI and FLC read with playback in the viewer | -- | -- | IV-1081, IV-1159, IV-1211 | format | plan D04 T13 §8 | playback through D04 T04 §10; authoring is Pinxit's D03 T23 §5 |
| LP-1042 | TrueType font preview rendered with custom sample text | -- | -- | IV-1184, IV-1230 | format | plan D04 T13 §8 |  |
| LP-1043 | Plain RAW decoding: ARW, CR2, CR3, CRW, cRAW, sRAW, DCR, DNG, ERF, FFF, GPR, MOS, MRW, NEF, NRW, ORF, PEF, RAF, RW2, RWL, SRF, SRW, KDC, CS1, with previews and EXIF | -- | AC-5075, AC-5076, AC-5077, AC-5078, AC-5079, AC-5080, AC-5081, AC-5082, AC-5083, AC-5084, AC-5085, AC-5086, AC-5087, AC-5088, AC-5089, AC-5090, AC-5091, AC-5092, AC-5093, AC-5094, AC-5095 | IV-1050, IV-1116, IV-1130, IV-1161, IV-1215, IV-1233 | format | shipped-scope D04 T01 §4 | through the decoder D04 T01 §3 chooses |
| LP-1044 | RAW originals never modified: develop settings stored in the catalog and sidecar | -- | AC-5171 | -- | core | shipped-scope D04 T02 §1 |  |
| LP-1045 | Corel PHOTO-PAINT CPT read (flattened) | -- | -- | IV-1129 | format | plan D04 T13 §8 | through the shared CPT reader of D01 T08 §5; the other layered formats split to LP-1622 (D04 T13 §12) |
| LP-1046 | JPM (JPEG 2000 Part 6) read and write with profiles, quality, and thumbnail | -- | -- | IV-0209, IV-0210, IV-0211, IV-1078, IV-1156 | format | plan D04 T13 §11 | through an optional user-installed GDAL with a JPM-capable driver, never bundled; reroutes to the backlog if no installable driver opens it |
| LP-1047 | ECW and MrSID wavelet formats: read, write with target compression, extra DLLs | -- | -- | IV-0222, IV-1054, IV-1084, IV-1117, IV-1137, IV-1160 | format | plan D04 T13 §11 | through an optional user-installed GDAL with the vendors' ECW and MrSID plug-ins, never bundled |
| LP-1048 | MrSID and JPM loading options | -- | -- | IV-1014 | format | plan D04 T13 §11 | GDAL overview level and band options |
| LP-1049 | Burn a slideshow to CD, DVD, or Blu-ray | -- | -- | IV-1048, IV-1049, IV-1085 | core | backlog B-049 |  |
| LP-1050 | Flash SWF and FLV | -- | -- | IV-1061, IV-1180 | format | plan D04 T13 §10 | an own SWF parser renders the first frame; FLV plays through D04 T16 §2 with the optional FFmpeg |
| LP-1051 | FlashPix (FPX) read | -- | -- | IV-1064, IV-1143 | format | plan D04 T13 §8 | through the shared FlashPix reader of D01 T08 §2; MRC split to LP-1621 (D04 T13 §11) |
| LP-1052 | Standalone EXE and screen saver slideshows | -- | -- | IV-1098 | core | backlog B-049 |  |
| LP-1053 | CAD formats: DXF, DWG, HPGL, CGM | -- | -- | IV-1135, IV-1136 | format | plan D04 T13 §9 | Stilus's DXF, DWG, CGM, and HPGL readers moved to Isotone.Core |
| LP-1054 | Canon DLLs for CRW and CR2 | -- | -- | IV-1006 | format | excluded: platform 32-bit only vendor DLL |  |
| LP-1055 | Office document viewing: Word, Excel sheet tabs, PowerPoint slides, RTF through installed Microsoft Office | -- | AC-1931, AC-1932, AC-1933, AC-5159, AC-5160, AC-5162, AC-5163, AC-5164, AC-5165, AC-5166, AC-5167, AC-5168, AC-5169, AC-5178 | -- | format | other-app: none office documents need Microsoft Office and are not photos |  |
| LP-1056 | Brush files shown as images: ABR, JBR, PBR | -- | AC-5041, AC-5058, AC-5063 | -- | format | other-app: Pinxit IP-0774 brush files belong to Pinxit's brush import |  |
| LP-1057 | Layers not preserved when saving TIFF, PSD, or GSD from the editor | -- | AC-5179 | -- | core | other-app: Pinxit IP-1842 layered TIFF and PSD saving is Pinxit's job |  |
| LP-1621 | MRC (Mixed Raster Content) read | -- | -- | IV-1083, IV-1228 | format | plan D04 T13 §11 | through an optional user-installed GDAL; reroutes to the backlog if no installable driver opens it; split from LP-1051 on 2026-09-27 |
| LP-1622 | Artweaver, BodyPaint 3D, Gemstone GSD, and ACDSee ACDC layered documents | -- | AC-5042, AC-5053, AC-5124, AC-5139 | IV-1046, IV-1047, IV-1124, IV-1125 | format | plan D04 T13 §12 | clean-room analysis of sample files (operator approval 2026-09-27); a format whose structure cannot be established reroutes to the backlog; split from LP-1045 on 2026-09-27 |

## Workspace and UI

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1058 | Group files by processed state (developed or edited) | -- | AC-0139 | -- | core | plan D04 T05 §5 |  |
| LP-1059 | Module picker: hide or show the picker and individual modules, mode button style, condensed buttons, mode icons | LR-0008, LR-0009 | AC-4020, AC-4031, AC-4032, AC-4033 | -- | core | plan D04 T14 §1 |  |
| LP-1060 | Identity plate: styled text or graphic plate, editor, module picker fonts and colors, presets, reuse in output modules | LR-0010, LR-0030, LR-0031, LR-0032, LR-0033, LR-0034, LR-1415 | -- | -- | core | plan D04 T14 §1 |  |
| LP-1061 | Panel groups: left and right panels, solo mode, end marks, auto hide and show, hide individual panels, hide or show side and bottom groups, swap left and right | LR-0013, LR-0014, LR-0017, LR-0018, LR-0019, LR-0020, LR-0036, LR-1503, LR-1558, LR-1559, LR-1561, LR-1562, LR-1563, LR-1564, LR-1565, LR-1566, LR-1567, LR-1568, LR-1569, LR-1570 | AC-4348 | -- | core | plan D04 T14 §1 |  |
| LP-1062 | Screen modes: normal, full screen with menubar, full screen, hide panels, full screen preview | LR-0021, LR-1505, LR-1603, LR-1604, LR-1605 | -- | -- | core | plan D04 T14 §1 |  |
| LP-1063 | Lights out: dim or black out everything but the selection, with color and dim level | LR-0022, LR-0023, LR-1504, LR-1601, LR-1602 | -- | -- | core | plan D04 T14 §1 |  |
| LP-1064 | Module switching: go to each module by key, back and forward through module history, return to the previous module | LR-1500, LR-1501, LR-1502, LR-1573, LR-1574, LR-1575, LR-1576, LR-1577, LR-1578, LR-1579, LR-1580, LR-1581 | -- | -- | core | plan D04 T14 §1 |  |
| LP-1065 | ACDSee modes mapped to Albumen: Manage to Browse, Media and View to the viewer and library, Develop, Dashboard, and switching modes | -- | AC-0019, AC-0020, AC-0021, AC-0022, AC-0026, AC-0027, AC-4421, AC-4511, AC-4512, AC-4513, AC-4685, AC-4686, AC-4687, AC-4976, AC-4978, AC-4979 | -- | core | plan D04 T14 §1 |  |
| LP-1066 | Toolbar customization: per-module toolbar items, show or hide toolbars, customize dialog, add or remove buttons, text labels, tooltips with shortcuts, reset | LR-0016, LR-0053, LR-1482, LR-1560 | AC-4341, AC-4342, AC-4343, AC-4344, AC-4345, AC-4346, AC-4347, AC-4469, AC-4479 | -- | core | plan D04 T14 §2 |  |
| LP-1067 | Text field editing: cut, copy, and paste in text fields, spelling check, and special characters | LR-1406, LR-1414 | -- | -- | core | plan D04 T14 §2 |  |
| LP-1068 | Workspaces menu and panes menu: save, reset, open or close any pane | -- | AC-0047, AC-0055 | -- | core | plan D04 T14 §2 |  |
| LP-1069 | Dockable panes: move, float to a second monitor, docking compass, stack as tabs, resize, auto hide, return to previous location | -- | AC-0056, AC-0057, AC-0058, AC-0059, AC-0060, AC-0061, AC-4339, AC-4349, AC-4350, AC-4351 | -- | core | plan D04 T14 §2 |  |
| LP-1070 | Saved workspaces: save, load, default workspace, reset layout per mode | -- | AC-0062, AC-4336, AC-4337, AC-4338 | -- | core | plan D04 T14 §2 |  |
| LP-1071 | Touch in the viewer: swipe, hold and swipe, press and hold, double-tap mode switch, pinch zoom, pan | -- | AC-0125, AC-0126, AC-0127, AC-0128, AC-0129, AC-0130, AC-4007, AC-4008, AC-4009, AC-4010 | -- | core | plan D04 T14 §2 |  |
| LP-1072 | Task pane of context-sensitive common tasks | -- | AC-4340, AC-4464 | -- | core | plan D04 T14 §2 |  |
| LP-1073 | Custom menus and button appearance | -- | AC-4352, AC-4353 | -- | core | plan D04 T14 §2 |  |
| LP-1074 | Tablet mode dialog for touch devices | -- | -- | IV-0040, IV-1503 | core | plan D04 T14 §2 |  |
| LP-1075 | Color controls copy and paste through the clipboard | -- | -- | IV-0066 | core | plan D04 T14 §2 |  |
| LP-1076 | Dialogs remember size and position | -- | -- | IV-0068 | core | plan D04 T14 §2 |  |
| LP-1077 | Favorite menus: up to 15 user-picked commands, add from any menu, remove or clear | -- | -- | IV-0352, IV-0353, IV-0354 | core | plan D04 T14 §2 |  |
| LP-1078 | Save browser window size and position | -- | -- | IV-0855 | core | plan D04 T14 §2 |  |
| LP-1079 | Toolbar buttons, position, and zoom box on the toolbar | -- | -- | IV-1023, IV-1024, IV-1025, IV-1496 | core | plan D04 T14 §2 |  |
| LP-1080 | Main window background fill color and panel font size | LR-0024, LR-0035 | -- | -- | core | plan D04 T14 §8 |  |
| LP-1081 | Display theme and dark mode | -- | AC-4354 | IV-0065 | core | plan D04 T14 §8 |  |
| LP-1082 | High DPI rendering | -- | -- | IV-0041 | core | plan D04 T14 §8 |  |
| LP-1083 | Toolbar skins: skin files, bundled and downloadable skins, button size | -- | -- | IV-0042, IV-0043, IV-0044, IV-1022 | core | plan D04 T14 §8 | Isotone theme icon sets, no third-party skin art bundled |
| LP-1084 | Edit in an additional external editor with per-edit copy options: format TIFF, PSD, or PSB, color space, bit depth, resolution, compression | LR-1017, LR-1021, LR-1027, LR-1028, LR-1030, LR-1031, LR-1032, LR-1037, LR-1330, LR-1641 | -- | -- | core | plan D04 T14 §9 |  |
| LP-1085 | Edit choices: a copy with Albumen adjustments, a copy of the original, or the original non-raw file | LR-1018, LR-1019, LR-1020 | -- | -- | core | plan D04 T14 §9 | Edit Original opens the file in the editor; Albumen itself never writes it |
| LP-1086 | Edit in Pinxit as layers or a linked raw document | LR-1022, LR-1025, LR-1026, LR-1655 | -- | -- | core | plan D04 T14 §9 | Pinxit opens several files as layers through its open command |
| LP-1087 | HDR edits handed to an external editor: HDR color spaces and 16 or 32 bit | LR-1029, LR-1036 | -- | -- | core | plan D04 T14 §9 |  |
| LP-1088 | External editor presets, file naming, stack with original, and round trip back into the catalog | LR-1033, LR-1034, LR-1035, LR-1038 | -- | -- | core | plan D04 T14 §9 | extends D04 T02 §7 stacking |
| LP-1089 | Editors menu and open in an external editor | -- | AC-0053 | IV-0922 | core | plan D04 T14 §9 |  |
| LP-1090 | Open in the default external editor (Ctrl+Alt+X) | -- | AC-1963, AC-4456, AC-4656 | -- | core | plan D04 T14 §9 |  |
| LP-1091 | External editors: configure, edit, default, multiple images, remove, open in default or named editor, shortcuts and toolbar buttons, per-extension editors, up to ten editors, short paths, all files in one call | -- | AC-4355, AC-4356, AC-4357, AC-4358, AC-4359, AC-4360, AC-4361, AC-4362, AC-4363 | IV-0032, IV-0033, IV-1019, IV-1020, IV-1021 | core | plan D04 T14 §9 |  |
| LP-1092 | Library and Develop modules in the module switcher | LR-0001, LR-0002, LR-1600 | -- | -- | core | shipped-scope D04 T01 §2 |  |
| LP-1093 | Catalog-wide undo and redo | LR-0039, LR-1405, LR-1571, LR-1572 | -- | -- | core | shipped-scope D01 T02 §4 |  |
| LP-1094 | Edit in the suite editor (Photoshop in Lightroom) | LR-1016, LR-1442, LR-1640 | -- | -- | core | shipped-scope D04 T02 §7 | Pinxit is the suite editor |
| LP-1095 | Edit mode: layered pixel editing hands off to Pinxit | -- | AC-0023, AC-4422, AC-4514, AC-4688, AC-4926, AC-4977 | -- | core | shipped-scope D04 T02 §7 | layered editing is Pinxit; Albumen hands off over files |

## Preferences

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1096 | Startup: splash screen, default catalog at launch (most recent, prompt, specific), catalog chooser with Ctrl at launch | LR-0050, LR-0051, LR-1324 | -- | -- | core | plan D04 T14 §4 |  |
| LP-1097 | Interface tweaks: zoom clicked point to center, system font smoothing, Auto Sync notifications | LR-0062, LR-0063, LR-0064 | -- | -- | core | plan D04 T14 §4 |  |
| LP-1098 | Completion sounds for import, tether transfer, and export, with system sound settings | LR-1325, LR-1326 | -- | -- | core | plan D04 T14 §4 |  |
| LP-1099 | Prompts: reset all warning dialogs | LR-1327 | -- | -- | core | plan D04 T14 §4 |  |
| LP-1100 | Remember last selection per source during the session | LR-1329 | -- | -- | core | plan D04 T14 §4 |  |
| LP-1101 | Network proxy server for internet access | LR-1347 | -- | -- | cloud | plan D04 T14 §4 | used by the AI client and update check |
| LP-1102 | Options dialog with pages for every mode and subsystem | LR-1418, LR-1627 | AC-4011, AC-4381, AC-4558, AC-4918 | IV-0610, IV-1443 | core | plan D04 T14 §4 |  |
| LP-1103 | Date and time output format: system or custom | -- | AC-4017, AC-4018 | -- | core | plan D04 T14 §4 |  |
| LP-1104 | Browse window options: full path and catalog name in title bar, folder tree density and expanders, clear path history on exit, overlay on folders excluded from the catalog | -- | AC-4061, AC-4062, AC-4063, AC-4064, AC-4065, AC-4172 | -- | core | plan D04 T14 §4 |  |
| LP-1105 | Error reporting opt out | -- | AC-4066 | -- | core | plan D04 T14 §4 |  |
| LP-1106 | File list behavior options: Ctrl hot-tracking, animations, image-type highlighting, auto scroll while building, Esc warning | -- | AC-4108, AC-4109, AC-4115, AC-4116, AC-4117 | IV-0865, IV-0866 | core | plan D04 T14 §4 |  |
| LP-1107 | Hide common folders in open and save dialogs | -- | -- | IV-0030 | core | plan D04 T14 §4 |  |
| LP-1108 | Named dialog profiles saved and loaded | -- | -- | IV-0067 | core | plan D04 T14 §4 |  |
| LP-1109 | Viewer start folder | -- | -- | IV-0928 | core | plan D04 T14 §4 |  |
| LP-1110 | Display color management: previews through the monitor profile, engine, default input profile for untagged images, thumbnails managed, profile details | LR-0037 | AC-4202, AC-4203, AC-4204, AC-4205, AC-4206 | -- | core | plan D04 T14 §5 | consumes D01 T04 §1 |
| LP-1111 | GPU acceleration preference: auto, custom, off, GPU preview generation, OpenCL processing | LR-0048, LR-1333, LR-1334 | AC-4021 | -- | core | plan D04 T14 §5 | the GPU develop path itself is D01 T07 §10 to §12; the preference governs display, previews, and that path |
| LP-1112 | Develop cache location, maximum size, and purge | LR-1331 | -- | -- | core | plan D04 T14 §5 |  |
| LP-1113 | Preview generation: previews in parallel, HDR display in Library, hover preview of presets, history, and snapshots | LR-1335, LR-1336, LR-1337 | -- | -- | core | plan D04 T14 §5 |  |
| LP-1114 | GPU selection for image processing: automatic or primary GPU | -- | AC-4278, AC-4279 | -- | core | plan D04 T14 §5 |  |
| LP-1115 | Warning when the display is not true color | -- | -- | IV-0860 | core | plan D04 T14 §5 |  |
| LP-1116 | Reset preferences to defaults at launch or from settings | LR-0052, LR-1352 | -- | -- | core | plan D04 T14 §6 |  |
| LP-1117 | Import settings from a previous installation: options, metadata views and presets, label, category, and keyword sets, search presets and history, new image presets, shortcuts | -- | AC-0001, AC-0002, AC-0003, AC-0004, AC-0005, AC-0006, AC-0007, AC-0013, AC-0014, AC-0015, AC-0016, AC-0018 | -- | core | plan D04 T14 §6 |  |
| LP-1118 | Import presets from a previous installation: develop, export, batch convert, rename, resize presets, and external editors | -- | AC-0008, AC-0009, AC-0010, AC-0011, AC-0012, AC-0017 | -- | automation | plan D04 T14 §6 |  |
| LP-1119 | Import settings from a previous installation on first run and on demand | -- | AC-4331, AC-4332 | -- | core | plan D04 T14 §6 |  |
| LP-1120 | Installer options: silent install, folder, shortcuts, file associations, settings folder, silent uninstall, desktop link with hotkey | -- | -- | IV-0007, IV-0008, IV-0009, IV-0010, IV-0011, IV-0012, IV-0013, IV-0014, IV-0015, IV-0016, IV-1018 | automation | plan D04 T14 §6 | Inno Setup installer from D05 T01 |
| LP-1121 | Portable mode: run from a ZIP or USB stick with settings beside the program | -- | -- | IV-0017, IV-0018 | core | plan D04 T14 §6 |  |
| LP-1122 | Settings file: location shown, copy to another PC, read-only freeze, encoding | -- | -- | IV-0019, IV-0020, IV-0034, IV-0035, IV-0932 | core | plan D04 T14 §6 |  |
| LP-1123 | Deployment settings for administrators: redirected settings folder, default language, locked toolbar, delete disabled, forced browsing, restricted save formats, suppressed association dialog | -- | -- | IV-0021, IV-0022, IV-0023, IV-0024, IV-0025, IV-0026, IV-0031 | automation | plan D04 T14 §6 |  |
| LP-1124 | Display theme choice | -- | AC-4060 | -- | core | plan D04 T14 §8 |  |

## Keyboard shortcuts and menus

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1125 | Module shortcut overlay (Ctrl+/) | LR-0040, LR-1508, LR-1855 | -- | -- | core | plan D04 T14 §3 |  |
| LP-1126 | Library navigation keys: next and previous photo, next in selection, beginning and end of grid, scroll thumbnails, scroll a zoomed photo | LR-1434, LR-1634, LR-1647, LR-1663, LR-1664, LR-1669 | -- | -- | core | plan D04 T14 §3 |  |
| LP-1127 | Shortcut editor: per-mode categories and commands, current keys, assign with conflict warning, remove, reset all, change a menu hotkey by right-click | -- | AC-4364, AC-4365, AC-4366, AC-4367, AC-4368, AC-4380, AC-4557, AC-4917 | IV-0064, IV-1606 | core | plan D04 T14 §3 |  |
| LP-1128 | Application keys: close Albumen, close the current image, close all images | -- | AC-4379, AC-4553, AC-4561, AC-4562, AC-4915 | -- | core | plan D04 T14 §3 | default keymap entries |
| LP-1129 | Keyboard focus and context-menu keys: Tab and Shift+Tab through panes, right-click context menus in browse and the viewer | -- | AC-4452, AC-4453, AC-4519, AC-4693 | -- | core | plan D04 T14 §3 | default keymap entries |
| LP-1130 | Media mode keys: mode switching, rotation, printing, file commands, and full-screen navigation inside Media mode | -- | AC-4535, AC-4536, AC-4537, AC-4538, AC-4539, AC-4540, AC-4541, AC-4542, AC-4543, AC-4544, AC-4545, AC-4546, AC-4547, AC-4548, AC-4549, AC-4550, AC-4551, AC-4552 | -- | core | plan D04 T16 §4 | ACDSee Media mode is video and audio browsing |
| LP-1131 | Video playback keys in the viewer: video context menu, playbar and file name toggles, volume, video zoom, skip by 10, 5, or 1 percent, copy frame | -- | -- | IV-1575, IV-1592, IV-1593, IV-1594, IV-1595, IV-1596, IV-1597, IV-1598, IV-1599, IV-1600 | video | plan D04 T16 §2 |  |

## Help and program

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1132 | Check for updates | LR-0043, LR-1512 | -- | IV-1028 | cloud | plan D04 T14 §7 | consumes the opt-in update check of D05 T01 §4 |
| LP-1133 | System info for troubleshooting: version, OS, GPU, caches, catalog | LR-0045, LR-1511 | -- | -- | core | plan D04 T14 §7 |  |
| LP-1134 | Help, user guide, community, feedback, and support links | LR-0046, LR-0047, LR-1507, LR-1509, LR-1856, LR-1857 | AC-0184, AC-0186, AC-0190, AC-0191 | -- | core | plan D04 T14 §7 | opens the Albumen user guide and project pages |
| LP-1135 | User interface language with on-the-fly switch, language packs, translated help, translation kit | LR-0049 | -- | IV-1005, IV-1033, IV-1034, IV-1035, IV-1036 | core | plan D04 T14 §7 | strings in .resx per D04 T02 §9 |
| LP-1136 | First-run quick start guide: start folder, folders to index, backup reminder interval, show at startup | -- | AC-0179, AC-0180, AC-0181, AC-0182, AC-0183 | -- | core | plan D04 T14 §7 |  |
| LP-1137 | Context help with F1 | -- | AC-0189, AC-4382, AC-4559, AC-4919 | IV-1026, IV-1416 | core | plan D04 T14 §7 |  |
| LP-1138 | Platform: 64-bit and ARM64 builds, supported Windows range, Unicode throughout, Store edition | -- | -- | IV-0001, IV-0002, IV-0005, IV-0006, IV-0037 | core | plan D04 T14 §7 | win-arm64 builds are D05 T01 §3 |
| LP-1139 | Help file and bundled readme files | -- | -- | IV-0038, IV-0039 | core | plan D04 T14 §7 |  |
| LP-1140 | Installed codecs list with versions | -- | -- | IV-1027 | core | plan D04 T14 §7 |  |
| LP-1141 | About dialog and credits | -- | AC-0188 | IV-1031, IV-1032, IV-1429 | core | shipped-scope D04 T01 §2 |  |
| LP-1142 | License registration and usage terms | -- | AC-0187 | IV-0004, IV-0027, IV-1029, IV-1030 | core | other-app: none Albumen is GPL-3.0 free software with no license codes |  |

## Automation, plug-ins, and command line

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1143 | Plug-in defined metadata in text filters and smart collection rules | LR-0317, LR-0606 | -- | -- | automation | plan D04 T17 §2 |  |
| LP-1144 | Plug-in metadata field set | LR-0385 | -- | -- | automation | plan D04 T17 §2 |  |
| LP-1145 | Third-party publish services and export plug-in destinations, filters, and the plug-in manager from Export | LR-0640, LR-1046, LR-1113, LR-1114, LR-1279 | -- | -- | automation | plan D04 T17 §2 | plug-in and extension APIs |
| LP-1146 | Plug-in manager: add, remove, enable, reload, status, autoload folder | LR-1363, LR-1364, LR-1365, LR-1366, LR-1367, LR-1369, LR-1370, LR-1395, LR-1644 | -- | -- | automation | plan D04 T17 §2 |  |
| LP-1147 | Plug-in extras menus in File, Library, and Help | LR-1371, LR-1372, LR-1373, LR-1396, LR-1435 | -- | -- | automation | plan D04 T17 §2 |  |
| LP-1148 | Plug-in SDK: export and publish providers, export filters, metadata providers, catalog access, develop controller, web engines, library filters, external tools, Lua UI | LR-1374, LR-1375, LR-1376, LR-1377, LR-1378, LR-1379, LR-1380, LR-1381, LR-1382, LR-1383 | -- | -- | automation | plan D04 T17 §2 |  |
| LP-1149 | Plug-in help files | LR-1510 | AC-0185 | -- | automation | plan D04 T17 §2 |  |
| LP-1150 | Actions menu: play recorded actions | -- | AC-0054 | -- | automation | plan D04 T17 §1 |  |
| LP-1151 | Actions Browser in the viewer: play and manage recorded actions | -- | AC-0093, AC-0110, AC-4573 | -- | automation | plan D04 T17 §1 |  |
| LP-1152 | Command line switch to open a specific catalog | -- | AC-1736 | -- | core | plan D04 T17 §3 |  |
| LP-1153 | Plug-in settings: decode, encode, archive, camera, command and pane extensions, disable, priority order, properties, help | -- | AC-1807, AC-1808, AC-1809, AC-1810, AC-1811, AC-1812, AC-1813, AC-1814, AC-1815, AC-1816, AC-1817 | -- | automation | plan D04 T17 §2 | formats are built in through the codec registry D04 T13 §1 |
| LP-1154 | Actions: record edits and play them back on other images, actions browser, categories, output options, import and export of action packages | -- | AC-2776, AC-2777, AC-2778, AC-2779, AC-2780, AC-2781, AC-2782, AC-2783, AC-2784, AC-2785, AC-2786, AC-2787, AC-2788, AC-2789, AC-2790, AC-2791, AC-2792, AC-2793, AC-2794, AC-2795, AC-2796, AC-2797, AC-2798, AC-2799, AC-2800, AC-2801, AC-2802, AC-2803, AC-2804, AC-2805, AC-2806, AC-2807, AC-2808, AC-2809, AC-2810, AC-2811, AC-2812, AC-2813, AC-2814, AC-2815 | -- | automation | plan D04 T17 §1 | the suite-wide actions of D01 T10 |
| LP-1155 | Recorded actions folder | -- | AC-4280 | -- | automation | plan D04 T17 §1 |  |
| LP-1156 | Batch option sets stored in the settings file and reused from the command line | -- | -- | IV-0350 | automation | plan D04 T17 §3 |  |
| LP-1157 | Scripted filters, Filter Factory, and Photoshop 8BF plug-in hosting including 32-bit filters | -- | -- | IV-0599, IV-0601, IV-0602, IV-0603, IV-0604, IV-0605, IV-0606, IV-0607, IV-1438, IV-1460 | core | plan D04 T04 §15 | third-party 8BF and Filter Factory filters on the suite plug-in host D01 T09 §2, including 32-bit filters in its x86 host; the batch step is LP-1160 |
| LP-1158 | Write image information to a text or CSV file from the command line | -- | -- | IV-0834 | automation | plan D04 T17 §3 |  |
| LP-1159 | Adobe 8BF filter folder | -- | -- | IV-1010 | core | plan D04 T04 §15 | plug-in folders through the D01 T09 §4 manager |
| LP-1160 | Plug-in hosting: Photoshop 8BF filters, Filter Factory, JewelScript effects, 32-bit plug-in stub loader, plug-in SDK | -- | -- | IV-1060, IV-1071, IV-1093, IV-1100, IV-1112, IV-1113, IV-1121 | automation | plan D04 T11 §7 | 8BF and Filter Factory filters as batch steps on the D01 T09 §2 host; the plug-in SDK is D04 T17 §2 on D01 T10 §7; JewelScript effect scripts are not run (C# scripts of D01 T10 §4 do the job) |
| LP-1161 | Command-line control of the viewer window: only one instance, fullscreen, fit to desktop, title, position, hide chrome, display parameters, page, file pattern | -- | -- | IV-1247, IV-1248, IV-1249, IV-1250, IV-1251, IV-1252, IV-1264, IV-1291, IV-1299, IV-1337, IV-1338, IV-1339, IV-1340, IV-1347, IV-1370 | automation | plan D04 T17 §3 |  |
| LP-1162 | Command-line convert and image operations: convert, make copy, crop, resize, rotate, flip, gray, invert, color depth, swap black and white, sharpen, contrast, brightness, gamma, effect, replace color, transparent color, DPI, JPEG quality, TIFF compression, lossless JPEG rotate, advanced batch, append pages, multipage, panorama | -- | -- | IV-1253, IV-1254, IV-1265, IV-1268, IV-1269, IV-1270, IV-1271, IV-1272, IV-1279, IV-1280, IV-1284, IV-1285, IV-1286, IV-1287, IV-1288, IV-1289, IV-1290, IV-1292, IV-1293, IV-1294, IV-1295, IV-1296, IV-1297, IV-1298, IV-1303, IV-1304, IV-1305, IV-1306, IV-1329, IV-1330, IV-1331, IV-1332, IV-1333, IV-1334, IV-1335, IV-1336, IV-1341, IV-1342, IV-1343, IV-1344, IV-1345, IV-1346, IV-1348, IV-1349, IV-1350, IV-1351, IV-1352, IV-1353, IV-1354, IV-1355, IV-1356, IV-1357, IV-1358, IV-1359, IV-1360, IV-1363, IV-1364, IV-1366, IV-1367, IV-1368, IV-1369 | automation | plan D04 T17 §3 | batch jobs run from the command line through D04 T11's operations |
| LP-1163 | Command-line slideshow, print, capture, scan, wallpaper, clipboard, palette import and export, hot folder, info export, and EXE slideshow switches | -- | -- | IV-1255, IV-1256, IV-1257, IV-1258, IV-1260, IV-1261, IV-1262, IV-1263, IV-1266, IV-1267, IV-1273, IV-1276, IV-1277, IV-1281, IV-1282, IV-1283, IV-1300, IV-1301, IV-1302, IV-1307, IV-1308, IV-1309, IV-1310, IV-1311, IV-1312, IV-1313, IV-1314, IV-1315, IV-1316, IV-1317, IV-1318, IV-1319, IV-1320, IV-1321, IV-1322, IV-1323, IV-1324, IV-1325, IV-1326, IV-1327, IV-1328, IV-1361, IV-1362, IV-1365, IV-1372, IV-1373, IV-1374 | automation | plan D04 T17 §3 | EXE slideshow switches are refused by name (backlog B-049) |
| LP-1164 | Command-line settings file location, silent errors, syntax rules (lowercase, order, wildcards, length limit, exit codes), and Send To shortcuts | -- | -- | IV-1274, IV-1275, IV-1278, IV-1371, IV-1375, IV-1376, IV-1378, IV-1379, IV-1380, IV-1381, IV-1382 | automation | plan D04 T17 §3 |  |

## Video and audio

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1165 | Import video files with photos | LR-0126 | -- | -- | format | plan D04 T16 §1 |  |
| LP-1166 | Video frame numbers and draft-quality HD playback in the loupe | LR-0249, LR-0250 | -- | -- | core | plan D04 T16 §2 |  |
| LP-1167 | Video metadata field set | LR-0394 | AC-0939 | -- | video | plan D04 T16 §1 |  |
| LP-1168 | Video playback, trim, poster frame, video quick develop, and video export | LR-0538, LR-0539, LR-0540, LR-0541 | -- | -- | core | plan D04 T16 §3 |  |
| LP-1169 | Video files in export: include, format, quality | LR-1064, LR-1065, LR-1066 | -- | -- | format | plan D04 T16 §3 |  |
| LP-1170 | Slideshow video audio versus music balance | LR-1198 | -- | -- | core | plan D04 T16 §6 |  |
| LP-1171 | Export slideshow as video | LR-1210, LR-1816 | -- | -- | format | plan D04 T16 §6 |  |
| LP-1172 | Video cache size and purge | LR-1332 | -- | -- | core | plan D04 T16 §1 |  |
| LP-1173 | Media mode shell: database-driven photo and video grid with header bar, refresh, catalog folders, and folders pane | -- | AC-0063, AC-0064, AC-0065, AC-0067, AC-0068, AC-1831, AC-1832, AC-1833, AC-1835, AC-1836 | -- | core | plan D04 T16 §4 | photo browsing parts are covered by the library grid D04 T01 §8 and browse D04 T05 §1 |
| LP-1174 | Media mode orphan files: show missing cataloged files | -- | AC-0066, AC-1834, AC-4221 | -- | core | plan D04 T16 §4 | missing photos in the library are D04 T06 §8 |
| LP-1175 | Media mode full screen: double-click to full screen, videos play in place, edge navigation arrows, grid and full screen toggle | -- | AC-0069, AC-0073, AC-0081, AC-1837, AC-1841, AC-1849 | -- | video | plan D04 T16 §4 |  |
| LP-1176 | Media mode context commands: open in view, develop, or edit mode, rotate, show in Explorer, delete, browse to file in Manage | -- | AC-0070, AC-0071, AC-0072, AC-0082, AC-1838, AC-1839, AC-1840, AC-1850, AC-4222 | -- | core | plan D04 T16 §4 |  |
| LP-1177 | Media mode filter, sort, group, group-by pane, and properties pane | -- | AC-0074, AC-0075, AC-0076, AC-0077, AC-0078, AC-0079, AC-0080, AC-1842, AC-1843, AC-1844, AC-1845, AC-1846, AC-1847, AC-1848 | -- | core | plan D04 T16 §4 |  |
| LP-1178 | Audio and video in browse: sound overlay, media file filter, preview and autoplay of clips | -- | AC-0421, AC-0587, AC-0636, AC-4161, AC-4162, AC-4393 | -- | video | plan D04 T16 §1 |  |
| LP-1179 | Special item listing every video | -- | AC-0739 | -- | video | plan D04 T16 §1 |  |
| LP-1180 | Slideshow video stretch and embedded image audio | -- | AC-1204, AC-1205 | -- | video | plan D04 T16 §6 |  |
| LP-1181 | Per-image audio in slideshows | -- | AC-1226 | -- | video | plan D04 T16 §6 |  |
| LP-1182 | Play audio clips embedded in images during Image Advance | -- | AC-1912 | -- | video | plan D04 T16 §5 |  |
| LP-1183 | Video and audio playback: play and pause, loop, mute, volume, zoom, seek keys, playbar, autoplay, context menu, separate player window, default external player option, DirectShow codecs, QuickTime and FLV toggles | -- | AC-1964, AC-1965, AC-1966, AC-1968, AC-1969, AC-4320 | IV-0804, IV-0805, IV-0806, IV-0807, IV-0808, IV-0809, IV-0810, IV-0811, IV-0813, IV-0814, IV-0815, IV-0816, IV-1072, IV-1094, IV-1103 | video | plan D04 T16 §2 |  |
| LP-1184 | Video frame extraction: copy or save the current frame, extract frames, save options | -- | AC-1967, AC-1970, AC-1971 | IV-0812, IV-0818 | video | plan D04 T16 §3 |  |
| LP-1185 | Image audio: audio embedded in TIFF and JPEG and same-named WAV files kept with the image | -- | AC-1972, AC-1973 | -- | video | plan D04 T16 §5 |  |
| LP-1186 | Edit image audio: attach, trim with markers, truncate, clip, record, mix, insert, append, replace, save as sound file, capture device and format | -- | AC-1974, AC-1975, AC-1976, AC-1977, AC-1978, AC-1979, AC-1980, AC-1981, AC-1982, AC-1983, AC-1984, AC-1985, AC-1986, AC-1987, AC-1988 | -- | video | plan D04 T16 §5 |  |
| LP-1187 | Media mode thumbnail pop-ups: hover or Shift, auto hide, thumbnail, configurable information | -- | AC-4223, AC-4224, AC-4225, AC-4226, AC-4227, AC-4228 | -- | core | plan D04 T16 §4 |  |
| LP-1188 | Audio formats: AAC, ADTS, M4A, MP3, MP2, MP1, WAV, WMA, AIF, AU, MIDI, OGG, FLAC, Real Audio, MED | -- | AC-5147, AC-5148, AC-5151, AC-5154, AC-5156, AC-5157 | IV-1082, IV-1095, IV-1099, IV-1197, IV-1198, IV-1199, IV-1200, IV-1201, IV-1202, IV-1203, IV-1236, IV-1237, IV-1239, IV-1240 | video | plan D04 T16 §1 |  |
| LP-1189 | Video formats: ASF, AVI, M4V, MOV, MP4, MKV, WebM, TS, MTS, MPG, WMV, 3GP, Video CD DAT | -- | AC-5149, AC-5150, AC-5152, AC-5153, AC-5155, AC-5158 | IV-1204, IV-1205, IV-1206, IV-1207, IV-1208, IV-1209, IV-1235, IV-1241 | video | plan D04 T16 §1 |  |
| LP-1190 | Save the slideshow as an MP4 video with music, frame size, frame rate, quality, and transitions | -- | -- | IV-0260, IV-0261 | video | plan D04 T16 §6 |  |
| LP-1191 | Extract all frames of animations and video | -- | -- | IV-0640 | video | plan D04 T16 §3 |  |
| LP-1192 | Multimedia player for video, audio, and audio CD | -- | -- | IV-0642 | video | plan D04 T16 §2 |  |
| LP-1193 | Audio CD playback | -- | -- | IV-0817, IV-1238 | video | plan D04 T16 §2 |  |
| LP-1194 | Video thumbnails through installed codecs | -- | -- | IV-0819 | video | plan D04 T16 §1 |  |
| LP-1195 | Save a slideshow as an MP4 video | -- | -- | IV-1104 | video | plan D04 T16 §6 |  |

## Cloud and online services

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1196 | Online tutorials, learn panel, and new-feature tips | LR-0041, LR-0042 | -- | -- | cloud | excluded: cloud online learning content |  |
| LP-1197 | Account sign in and sign out | LR-0044, LR-1513 | -- | -- | cloud | excluded: cloud vendor account |  |
| LP-1198 | Likes and comments from shared albums in filters and smart collection rules | LR-0329, LR-0568, LR-0569 | -- | -- | cloud | excluded: cloud shared-album likes and comments are an online service |  |
| LP-1199 | Keyword sync with the Lightroom cloud ecosystem | LR-0460 | -- | -- | cloud | excluded: cloud Adobe sync |  |
| LP-1200 | All synced photographs and ecosystem sync of collections, sharing collections on the web | LR-0487, LR-0544, LR-0556, LR-0562 | -- | -- | cloud | excluded: cloud Lightroom ecosystem sync and web sharing |  |
| LP-1201 | Online publish services: Adobe Stock, Flickr, and publisher comments | LR-0638, LR-0639, LR-0650 | -- | -- | cloud | excluded: cloud online publishing services and their comments |  |
| LP-1202 | Add images to Firefly boards | LR-1040 | -- | -- | cloud | excluded: cloud Adobe Firefly boards |  |
| LP-1203 | Blurb book sizes, covers, paper, logo page, price, and upload | LR-1144, LR-1145, LR-1146, LR-1147, LR-1148, LR-1171 | -- | -- | print | excluded: cloud Blurb online print service | the local PDF book is planned |
| LP-1204 | Cloud sync: account, delete synced data, pause, keep awake, sync location and subfolders, status | LR-1339, LR-1340, LR-1341, LR-1342, LR-1343, LR-1344, LR-1345 | -- | -- | cloud | excluded: cloud Lightroom sync |  |
| LP-1205 | Lightroom cloud sync, synced collections, mobile downloads, keyword and format sync, shared web albums, invites, comments, stock contributions | LR-1353, LR-1354, LR-1355, LR-1356, LR-1357, LR-1358, LR-1359, LR-1360, LR-1361, LR-1362 | -- | -- | cloud | excluded: cloud Adobe sync and sharing |  |
| LP-1206 | Online plug-in marketplace | LR-1368 | -- | -- | cloud | excluded: cloud online plug-in exchange |  |
| LP-1207 | 365 mode uploads to ACDSee cloud | -- | AC-0025, AC-4516, AC-4690, AC-4981 | -- | cloud | excluded: cloud ACDSee 365 online sharing |  |
| LP-1208 | ACDSee 365 mode and SeeDrive: account, browsing, transfers, uploads, downloads, public folders, sharing, sync to web, transfer options | -- | AC-0153, AC-0154, AC-0155, AC-0156, AC-0157, AC-1818, AC-1819, AC-1820, AC-1821, AC-1822, AC-1823, AC-1824, AC-1825, AC-1826, AC-1827, AC-1828, AC-1829, AC-1830, AC-3939, AC-3940, AC-3941, AC-3942, AC-3943, AC-3944, AC-3945, AC-3946, AC-3947, AC-3948, AC-3949, AC-3950, AC-3951, AC-3952, AC-3953, AC-3954, AC-3955, AC-3956, AC-3957, AC-3958, AC-3959, AC-3960, AC-3961, AC-3962, AC-3963, AC-3964, AC-3965, AC-3966, AC-3967, AC-3968, AC-3969, AC-4289, AC-4290, AC-4291, AC-4292, AC-4293, AC-4294, AC-4295, AC-5001, AC-5002, AC-5003, AC-5004, AC-5005, AC-5006, AC-5007, AC-5008, AC-5009, AC-5010, AC-5011, AC-5012, AC-5013, AC-5014, AC-5015, AC-5016, AC-5017, AC-5018, AC-5019, AC-5020, AC-5021, AC-5022, AC-5023, AC-5024, AC-5025, AC-5026, AC-5027, AC-5028, AC-5029, AC-5030, AC-5031, AC-5032, AC-5033, AC-5034, AC-5035, AC-5036, AC-5037, AC-5038, AC-5039 | -- | cloud | excluded: cloud ACDSee 365 online storage and sharing |  |
| LP-1209 | ACDSee account, credit purchase, refresh, and no-refund rules for generative tools | -- | AC-0192, AC-0194, AC-0202, AC-0227, AC-0229, AC-0280, AC-0294, AC-2882, AC-2883, AC-2885 | -- | cloud | excluded: cloud ACDSee account and credit store; Pinxit AI uses the user's own OpenRouter key |  |
| LP-1210 | ACDSee Mobile Sync: phone app, sync folders, pairing, notifications, sending, root folder, server name | -- | AC-0400, AC-0401, AC-0402, AC-0403, AC-0404, AC-0405, AC-4327, AC-4328, AC-4329 | -- | cloud | excluded: cloud mobile companion app sync service |  |
| LP-1211 | OneDrive and cloud drives in browse: cloud node, local, always-local, and cloud-only overlays, OneDrive indexing | -- | AC-0431, AC-0432, AC-0433, AC-0456, AC-4325 | -- | cloud | excluded: cloud OneDrive and cloud storage integration |  |
| LP-1212 | OneDrive browsing, keep on device, free up space, auto download, status column, cloud-only metadata, move to OneDrive, embed into online files | -- | AC-0485, AC-0486, AC-0487, AC-0488, AC-0489, AC-0490, AC-0491, AC-4239 | -- | cloud | excluded: cloud OneDrive integration |  |
| LP-1213 | Share by email through ACDSee 365 online albums | -- | AC-1178, AC-1179, AC-1180, AC-1181, AC-1182 | -- | cloud | excluded: cloud ACDSee 365 online albums |  |
| LP-1214 | Upload manager to Flickr, SmugMug, and Zenfolio with the Flickr uploader settings | -- | AC-1273, AC-1274, AC-1275, AC-1276, AC-1278, AC-1279, AC-1280, AC-1281, AC-1282, AC-1283, AC-1284, AC-1285, AC-1286, AC-1287, AC-1288, AC-1289, AC-1290, AC-1291, AC-1292, AC-1293, AC-1294, AC-1295, AC-1296, AC-1297, AC-1298, AC-4569, AC-4570, AC-4571 | -- | cloud | excluded: cloud photo-sharing site uploads |  |
| LP-1215 | Legacy 32-bit OCR engine | -- | -- | IV-0708 | ai | excluded: platform 32-bit only engine |  |

## Routed to Pinxit

| ID | Feature | Lightroom | ACDSee | IrfanView | Category | Status | Notes |
| -- | ------- | --------- | ------ | --------- | -------- | ------ | ----- |
| LP-1216 | Next, previous, first, and last image keys while editing | -- | AC-4708, AC-4709, AC-4714, AC-4715 | -- | core | plan D04 T14 §3 | Albumen filmstrip keys around the Edit in Pinxit hand-off |
| LP-1217 | Tag, reject, metadata, keywords, presets, and caption keys while editing | -- | AC-4725, AC-4726, AC-4727, AC-4728, AC-4729, AC-4730, AC-4731 | -- | core | plan D04 T14 §3 | Albumen keymap; metadata stays in Albumen |
| LP-1218 | Take a developed photo into the editor as a 16-bit rendition, and revert edits to develop or original | -- | AC-0133, AC-0134, AC-2101, AC-2102, AC-2103, AC-2104, AC-4657, AC-4658 | -- | core | shipped-scope D04 T02 §7 | the edited file is a stacked derivative; the original is never moved or written |
| LP-1219 | Pixel editing mode after develop, and the round trip back: revert to the develop result, warn that pixel edits are lost on return, keep develop settings, keep catalog data on the saved file, original moved aside or RAW saved as another format | -- | AC-2586, AC-2625, AC-2629, AC-2630, AC-2639, AC-2640, AC-2641, AC-2642, AC-3228 | -- | core | shipped-scope D04 T02 §7 | Edit in Pinxit renders a new stacked TIFF; the original is never written and develop settings stay in the catalog and sidecar |
| LP-1220 | Restore to developed: discard editor changes and return to the developed photo | -- | AC-3559, AC-3624 | -- | core | shipped-scope D04 T02 §7 | Albumen keeps the developed original; the edited file is a stacked derivative |
| LP-1221 | Leave the editor for Develop, the previous mode, Manage, Media, View, People, or Dashboard | -- | AC-4713, AC-4716, AC-4908, AC-4909, AC-4910, AC-4911, AC-4912, AC-4914 | -- | core | shipped-scope D04 T02 §7 | Albumen and Pinxit are separate apps joined by the Edit in hand-off |
| LP-1222 | Rating and color label keys while editing | -- | AC-4723, AC-4724 | -- | core | shipped-scope D04 T01 §11 | ratings and labels live in Albumen |
| LP-1223 | Recorded actions play back destructively | -- | AC-3503 | -- | automation | plan D04 T17 §1 | playback writes new files unless the originals opt-in is on |
| LP-1224 | Photoshop plug-in folders | -- | AC-4281 | -- | automation | plan D04 T04 §15 | plug-in folders through the D01 T09 §4 manager |
| LP-1225 | Start and stop action recording keys | -- | AC-4906, AC-4907 | -- | automation | plan D04 T17 §1 |  |
| LP-1226 | Switch to 365 mode from the editor | -- | AC-4913 | -- | core | excluded: cloud ACDSee 365 online service |  |
| LP-1227 | Prompt-based generative editing of a photo | LR-1039 | -- | -- | ai | other-app: Pinxit IP-2090 prompt-to-edit is Pinxit D03 T19 §10 |  |
| LP-1228 | Edit mode summary: selections, brush, layers, targeting, repair, and effects | -- | AC-0136 | -- | core | other-app: Pinxit IP-0265 layered pixel editing is Pinxit |  |
| LP-1229 | Edit mode lighting and color tools summary | -- | AC-0137 | -- | core | other-app: Pinxit IP-0565 adjustment layers are Pinxit |  |
| LP-1230 | Edit mode detail tools summary | -- | AC-0138 | -- | core | other-app: Pinxit IP-1099 pixel sharpening and noise filters are Pinxit |  |
| LP-1231 | Estimated cost of a generation shown before it runs, scaled by area | -- | AC-0193, AC-0228, AC-0296, AC-2884 | -- | cloud | other-app: Pinxit IP-1992 AI usage and cost display is Pinxit AI |  |
| LP-1232 | Generative tools offered per mode without leaving the current view, one image at a time | -- | AC-0195, AC-0196, AC-0204 | -- | cloud | other-app: Pinxit IP-1990 AI menu and workspace is Pinxit AI |  |
| LP-1233 | Choice of image-generation model per tool | -- | AC-0197, AC-0198, AC-0199, AC-0200, AC-0216, AC-0273, AC-0290, AC-2881 | -- | cloud | other-app: Pinxit IP-1991 per-task model choice through OpenRouter in Pinxit |  |
| LP-1234 | Generation history: prompt persists, non-deterministic results, saved generation presets and reset | -- | AC-0201, AC-0213, AC-0214, AC-0276, AC-0277, AC-0293 | -- | cloud | other-app: Pinxit IP-1996 generation history for reuse and re-run in Pinxit |  |
| LP-1235 | Generate an image from a text prompt: aspect ratio, resolution, output format and folder, as a new file or a new layer, progress and notification | -- | AC-0203, AC-0209, AC-0210, AC-0211, AC-0212, AC-0217, AC-0218, AC-0219, AC-0224, AC-0225, AC-0226, AC-0230, AC-0231 | -- | cloud | other-app: Pinxit IP-2014 image generation is Pinxit AI |  |
| LP-1236 | Prompt entry with length limit and prompting guidance per tool | -- | AC-0205, AC-0215, AC-0274, AC-0291, AC-0298, AC-0299, AC-0300 | -- | cloud | other-app: Pinxit IP-1998 AI prompt entry is Pinxit AI |  |
| LP-1237 | Reference images for generation: style, character, and composition references | -- | AC-0206, AC-0221, AC-0222, AC-0223, AC-0275, AC-0292 | -- | cloud | other-app: Pinxit IP-2015 reference images for generation in Pinxit |  |
| LP-1238 | Cloud processing disclosure for generation: what is sent and retained | -- | AC-0207 | -- | cloud | other-app: Pinxit IP-1993 send gate and preview in Pinxit AI |  |
| LP-1239 | Invisible AI watermark on generated images | -- | AC-0208 | -- | cloud | other-app: Pinxit IP-1878 provenance marking of generated content (Pinxit, B-047) |  |
| LP-1240 | Visual effect styles for generated images (36 presets, up to five combined) | -- | AC-0220, AC-0232, AC-0233, AC-0234, AC-0235, AC-0236, AC-0237, AC-0238, AC-0239, AC-0240, AC-0241, AC-0242, AC-0243, AC-0244, AC-0245, AC-0246, AC-0247, AC-0248, AC-0249, AC-0250, AC-0251, AC-0252, AC-0253, AC-0254, AC-0255, AC-0256, AC-0257, AC-0258, AC-0259, AC-0260, AC-0261, AC-0262, AC-0263, AC-0264, AC-0265, AC-0266, AC-0267 | -- | cloud | other-app: Pinxit IP-2014 effects presets of Pinxit image generation |  |
| LP-1241 | Generative edit of the selected layer from a prompt: iterate with undo, output as new layer or replace, selection-constrained, generated layer mask | -- | AC-0268, AC-0269, AC-0270, AC-0271, AC-0272, AC-0278, AC-0279, AC-0281, AC-0282, AC-0283, AC-0284, AC-0285, AC-0286 | -- | cloud | other-app: Pinxit IP-2090 prompt to edit and generative edit in Pinxit |  |
| LP-1242 | Generative fill from all layers into a new layer | -- | AC-0287, AC-0288, AC-0289 | -- | cloud | other-app: Pinxit IP-2005 generative fill in Pinxit |  |
| LP-1243 | AI remove: brush over an object and reconstruct the background | -- | AC-0295, AC-0297, AC-2876, AC-2877, AC-2878, AC-2879, AC-2880, AC-2886 | -- | cloud | other-app: Pinxit IP-2004 remove tool with generative mode in Pinxit |  |
| LP-1244 | New blank image dialog: size, units, aspect ratio, DPI, background, bit depth, presets | -- | AC-0316, AC-0446, AC-0447, AC-0448, AC-0449, AC-0450, AC-0451, AC-0452 | -- | core | other-app: Pinxit IP-0016 new blank documents are pixel editing | presets are IP-0015 |
| LP-1245 | Load files into a layer stack | -- | AC-1052 | -- | core | other-app: Pinxit IP-1721 layer stacks are Pinxit |  |
| LP-1246 | Tool groups panel: selections and drawing, AI, enhance, add, geometry, exposure, color, detail | -- | AC-2587, AC-2588, AC-2589, AC-2590, AC-2591, AC-2592, AC-2593, AC-2594 | -- | core | other-app: Pinxit IP-2138 toolbar with tool groups in Pinxit |  |
| LP-1247 | History pane, history drop-down, undo all, undo and redo buttons | -- | AC-2595, AC-2596, AC-2597, AC-2607 | -- | core | other-app: Pinxit IP-0201 undo, redo, and history in Pinxit |  |
| LP-1248 | AI actions tab with one-click AI actions and selection refinement | -- | AC-2598, AC-2599, AC-2816, AC-2817 | -- | ai | other-app: Pinxit IP-1998 AI quick actions in Pinxit |  |
| LP-1249 | Editor histogram with channel toggles and live update | -- | AC-2600, AC-2601, AC-2602, AC-2603, AC-2604, AC-2606 | -- | core | other-app: Pinxit IP-0116 histogram panel in Pinxit |  |
| LP-1250 | Color tab for choosing drawing colors | -- | AC-2605 | -- | core | other-app: Pinxit IP-0732 color panel in Pinxit |  |
| LP-1251 | Reset the image and restore to original | -- | AC-2608, AC-2624 | -- | core | other-app: Pinxit IP-1706 revert in Pinxit |  |
| LP-1252 | Full screen display in the editor | -- | AC-2609 | -- | core | other-app: Pinxit IP-0037 screen modes in Pinxit |  |
| LP-1253 | Editor zoom: actual size, fit, zoom slider and preset list | -- | AC-2610, AC-2613, AC-2615, AC-2616 | -- | core | other-app: Pinxit IP-0026 zoom commands in Pinxit |  |
| LP-1254 | Navigator pane, automatic or manual | -- | AC-2611, AC-2612 | -- | core | other-app: Pinxit IP-0061 navigator panel in Pinxit |  |
| LP-1255 | Show previous to compare with the last saved state | -- | AC-2614 | -- | core | other-app: Pinxit IP-0129 toggle last state in Pinxit |  |
| LP-1256 | Color picker readout of pre-edit and edited values | -- | AC-2617 | -- | core | other-app: Pinxit IP-0109 info panel readouts in Pinxit |  |
| LP-1257 | Right-click a slider to reset it | -- | AC-2618, AC-2928 | -- | core | other-app: Pinxit IP-1018 reset filter dialog values in Pinxit |  |
| LP-1258 | Last-used tool settings reapplied | -- | AC-2619 | -- | core | other-app: Pinxit IP-0576 last-used adjustment settings in Pinxit |  |
| LP-1259 | Tool presets: save, choose, delete | -- | AC-2620, AC-2621, AC-2622 | -- | core | other-app: Pinxit IP-1013 filter and adjustment presets in Pinxit |  |
| LP-1260 | Import and export editor presets as a set | -- | AC-2623 | -- | core | other-app: Pinxit IP-2223 preset export and import in Pinxit |  |
| LP-1261 | Save, discard, cancel, autosave, and save-and-continue of an editing session | -- | AC-2626, AC-2632, AC-2633, AC-2634, AC-2635, AC-2638 | -- | core | other-app: Pinxit IP-1844 save and close semantics in Pinxit |  |
| LP-1262 | Save as and save a copy under a new name or format | -- | AC-2627, AC-2636, AC-2637 | -- | core | other-app: Pinxit IP-1713 save a copy in Pinxit |  |
| LP-1263 | Save options: preserve metadata and embed the color profile | -- | AC-2628, AC-2631 | -- | core | other-app: Pinxit IP-1714 save content options in Pinxit |  |
| LP-1264 | Photoshop 64-bit filter plug-ins | -- | AC-2643 | -- | automation | other-app: Pinxit IP-1033 third-party plug-in host (Pinxit's D03 T14 §11 on the shared D01 T09 host) |  |
| LP-1265 | Edit brush: paint a filter or adjustment into brushed areas with nib width, feathering, pressure, erase, clear, invert, reload, show strokes, per-stroke undo, straight lines | -- | AC-2644, AC-2645, AC-2646, AC-2647, AC-2648, AC-2649, AC-2650, AC-2651, AC-2652, AC-2653, AC-2654, AC-2655, AC-2656, AC-2657, AC-2658 | -- | core | other-app: Pinxit IP-1007 filter brush through a live filter mask in Pinxit |  |
| LP-1266 | Smart brushing: restrict edit-brush strokes by color, brightness, or both with a tolerance | -- | AC-2659, AC-2660, AC-2661, AC-2662, AC-2663, AC-2664 | -- | core | other-app: Pinxit IP-2368 Pinxit gains smart brushing on its filter and adjustment brushes |  |
| LP-1267 | Linear and radial gradient masks for a filter: guides, feathering, squareness, invert, show mask, switch to brush | -- | AC-2665, AC-2666, AC-2667, AC-2668, AC-2669, AC-2670, AC-2671, AC-2672, AC-2673, AC-2674, AC-2675, AC-2676, AC-2677, AC-2678, AC-2679, AC-2680 | -- | core | other-app: Pinxit IP-1004 live filter mask with gradients in Pinxit |  |
| LP-1268 | Filter blend modes and opacity: normal to lighter color | -- | AC-2681, AC-2682, AC-2683, AC-2684, AC-2685, AC-2686, AC-2687, AC-2688, AC-2689, AC-2690, AC-2691, AC-2692, AC-2693, AC-2694, AC-2695, AC-2696, AC-2697, AC-2698, AC-2699, AC-2700, AC-2701, AC-2702, AC-2703, AC-2704, AC-2705, AC-2706, AC-2708 | -- | core | other-app: Pinxit IP-1019 filter blending mode and opacity in Pinxit |  |
| LP-1269 | Blend mode and preset hover preview | -- | AC-2707 | -- | core | other-app: Pinxit IP-0329 blend mode hover preview in Pinxit |  |
| LP-1270 | Layer blend modes: normal to lighter color | -- | AC-2709, AC-2710, AC-2711, AC-2712, AC-2713, AC-2714, AC-2715, AC-2716, AC-2717, AC-2718, AC-2719, AC-2720, AC-2721, AC-2722, AC-2723, AC-2724, AC-2725, AC-2726, AC-2727, AC-2728, AC-2729, AC-2730, AC-2731, AC-2732, AC-2733 | -- | core | other-app: Pinxit IP-0265 layer blend modes in Pinxit |  |
| LP-1271 | Rulers with units, ruler DPI, and resolution from EXIF | -- | AC-2734, AC-2735, AC-4286, AC-4287, AC-4288 | -- | core | other-app: Pinxit IP-0069 rulers and units in Pinxit |  |
| LP-1272 | Guidelines: drag from rulers, move, clear, lock, hide, color | -- | AC-2736, AC-2738, AC-2739, AC-2740, AC-4285 | -- | core | other-app: Pinxit IP-0075 guides in Pinxit |  |
| LP-1273 | Snap to guidelines | -- | AC-2737 | -- | core | other-app: Pinxit IP-0085 snapping in Pinxit |  |
| LP-1274 | Apply a filter to one channel: red, green, blue, hue, saturation, or lightness | -- | AC-2741 | -- | core | other-app: Pinxit IP-0308 blending channel restrictions in Pinxit |  |
| LP-1275 | Filter apply, done, and cancel buttons | -- | AC-2742, AC-2743, AC-2744 | -- | core | other-app: Pinxit IP-1032 filter apply and cancel in Pinxit |  |
| LP-1276 | Pixel targeting: restrict a filter by tone range, color wheels, and detail, with presets and mask preview | -- | AC-2745, AC-2746, AC-2747, AC-2748, AC-2749, AC-2750, AC-2751, AC-2752, AC-2753, AC-2754, AC-2755, AC-2756, AC-2757, AC-2758, AC-2759, AC-2760, AC-2761, AC-2762, AC-2763, AC-2764, AC-2766, AC-2767, AC-2768, AC-2769, AC-2770, AC-2771, AC-2772, AC-2773, AC-2774 | -- | core | other-app: Pinxit IP-0304 tonal and color targeting by blend ranges in Pinxit |  |
| LP-1277 | Skin targeting for filters and selections | -- | AC-2765, AC-2775, AC-2927 | -- | core | other-app: Pinxit IP-0486 skin-tone color range in Pinxit |  |
| LP-1278 | AI denoise action | -- | AC-2818 | -- | ai | other-app: Pinxit IP-2070 AI noise reduction in Pinxit |  |
| LP-1279 | AI select subject and select background | -- | AC-2819, AC-2822, AC-2853, AC-2854 | -- | ai | other-app: Pinxit IP-2028 select subject in Pinxit |  |
| LP-1280 | AI select sky | -- | AC-2820, AC-2855 | -- | ai | other-app: Pinxit IP-2030 select sky in Pinxit |  |
| LP-1281 | AI select hair | -- | AC-2821, AC-2856 | -- | ai | other-app: Pinxit IP-2031 select people parts in Pinxit |  |
| LP-1282 | AI remove background to a mask | -- | AC-2823 | -- | ai | other-app: Pinxit IP-2081 remove background to a layer mask in Pinxit |  |
| LP-1283 | AI blur background | -- | AC-2824 | -- | ai | other-app: Pinxit IP-2061 portrait blur in Pinxit |  |
| LP-1284 | AI black and white background as a masked adjustment layer | -- | AC-2825 | -- | ai | other-app: Pinxit IP-2369 Pinxit gains one-click masked background adjustments |  |
| LP-1285 | Selections restrict edits and filters; use selection toggle and invert for the current edit | -- | AC-2826, AC-2827, AC-2869, AC-2870 | -- | core | other-app: Pinxit IP-1032 filters apply to the selection in Pinxit |  |
| LP-1286 | Selection display: mask preview, marching ants, highlighted or exposed overlay | -- | AC-2828, AC-2845, AC-2846, AC-2847, AC-2848 | -- | core | other-app: Pinxit IP-0508 selection view modes in Pinxit |  |
| LP-1287 | Selection basket: store selections and masks, rename, duplicate, add, subtract, intersect with the selection or the mask | -- | AC-2829, AC-2895, AC-2896, AC-2897, AC-2898, AC-2899, AC-2900, AC-2901, AC-2902, AC-2903, AC-2904, AC-2905, AC-2906, AC-2907, AC-2908, AC-2909 | -- | core | other-app: Pinxit IP-0450 saved selections in channels with combine operations in Pinxit |  |
| LP-1288 | Freehand lasso | -- | AC-2830 | -- | core | other-app: Pinxit IP-0542 lasso in Pinxit |  |
| LP-1289 | Magic wand with threshold, connected, and brightness, color, or RGB types | -- | AC-2831, AC-2832, AC-2833, AC-2834, AC-2835, AC-2836 | -- | core | other-app: Pinxit IP-0470 magic wand in Pinxit |  |
| LP-1290 | Rectangular and elliptical selection | -- | AC-2837, AC-2838 | -- | core | other-app: Pinxit IP-0541 marquee in Pinxit |  |
| LP-1291 | Shape selection with corner and curve nodes | -- | AC-2839, AC-2840 | -- | core | other-app: Pinxit IP-0538 selection from path in Pinxit |  |
| LP-1292 | Brush selection with smart color or brightness tolerance | -- | AC-2841, AC-2842, AC-2843 | -- | core | other-app: Pinxit IP-0498 selection brush in Pinxit |  |
| LP-1293 | AI object selection by loose lasso | -- | AC-2844 | -- | ai | other-app: Pinxit IP-2023 object selection in Pinxit |  |
| LP-1294 | Selection modes: add, subtract, inverse, click to clear, combine tools | -- | AC-2849, AC-2850, AC-2851, AC-2852, AC-2857 | -- | core | other-app: Pinxit IP-0543 selection modes in Pinxit |  |
| LP-1295 | Save, load, and manage selections | -- | AC-2858, AC-2859, AC-2860 | -- | core | other-app: Pinxit IP-0450 saved selections in Pinxit |  |
| LP-1296 | Copy, cut, and delete selected pixels | -- | AC-2861, AC-2863 | -- | core | other-app: Pinxit IP-0176 cut, copy, clear in Pinxit |  |
| LP-1297 | Paste a selection as a new layer | -- | AC-2862 | -- | core | other-app: Pinxit IP-0166 paste as new layer in Pinxit |  |
| LP-1298 | Refine selection: shift edge and feathering, saved as preset | -- | AC-2864, AC-2865, AC-2866 | -- | core | other-app: Pinxit IP-0514 refine selection in Pinxit |  |
| LP-1299 | Selection from pixel targeting | -- | AC-2867 | -- | core | other-app: Pinxit IP-0479 mask from color range in Pinxit |  |
| LP-1300 | Luminosity selection | -- | AC-2868 | -- | core | other-app: Pinxit IP-0491 selection from luminosity in Pinxit |  |
| LP-1301 | Selection feathering | -- | AC-2871 | -- | core | other-app: Pinxit IP-0545 feather selection in Pinxit |  |
| LP-1302 | Show or hide selection edges | -- | AC-2872 | -- | core | other-app: Pinxit IP-0453 marching ants toggle in Pinxit |  |
| LP-1303 | Smart erase: content-aware fill of a selection or a brushed area | -- | AC-2873, AC-2874, AC-2875, AC-3233 | -- | ai | other-app: Pinxit IP-0909 content-aware healing in Pinxit |  |
| LP-1304 | Channel selection: build a selection or mask from an RGB, CMYK, Lab, or HSL channel with levels and invert | -- | AC-2887, AC-2888, AC-2889, AC-2890, AC-2891, AC-2892, AC-2893, AC-2894 | -- | core | other-app: Pinxit IP-0555 channel to selection in Pinxit |  |
| LP-1305 | Luminance and color range pane: tone grabber, color wheels, add detail, smoothness, presets | -- | AC-2910, AC-2911, AC-2912, AC-2913, AC-2914, AC-2915, AC-2916, AC-2917, AC-2918, AC-2919, AC-2920, AC-2921, AC-2922, AC-2923, AC-2924, AC-2925, AC-2926 | -- | core | other-app: Pinxit IP-0294 live luminosity and hue range masks in Pinxit |  |
| LP-1306 | Layers pane basics: blank layer, show and hide, delete, duplicate, reorder, rename, merge down, flatten, blend mode, opacity | -- | AC-2929, AC-2932, AC-2937, AC-2938, AC-2939, AC-2940, AC-2941, AC-2942, AC-2943, AC-2944, AC-2945, AC-2946, AC-2947 | -- | core | other-app: Pinxit IP-0276 layers panel in Pinxit |  |
| LP-1307 | Geometry commands apply to all layers | -- | AC-2930 | -- | core | other-app: Pinxit IP-0215 canvas rotate and flip in Pinxit |  |
| LP-1308 | Watermark placed on its own layer | -- | AC-2931 | -- | core | other-app: Pinxit IP-0398 image layers in Pinxit |  |
| LP-1309 | Add a file or a filmstrip image as a layer | -- | AC-2933, AC-2934, AC-2935 | -- | core | other-app: Pinxit IP-1720 place embedded in Pinxit |  |
| LP-1310 | Load files into a stack as layers | -- | AC-2936 | -- | core | other-app: Pinxit IP-1721 load files into stack in Pinxit |  |
| LP-1311 | Layered native format preserving layers for re-editing | -- | AC-2948 | -- | format | other-app: Pinxit IP-1848 native .pinxit format |  |
| LP-1312 | 16 bits per channel layered documents | -- | AC-2949 | -- | format | other-app: Pinxit IP-0680 bit depth in Pinxit |  |
| LP-1313 | New image: name, dimensions, aspect ratio, resolution, background, bit depth | -- | AC-2950, AC-2951, AC-2952, AC-2953, AC-2954, AC-2955 | -- | core | other-app: Pinxit IP-0016 new document settings in Pinxit |  |
| LP-1314 | New image presets | -- | AC-2956 | -- | core | other-app: Pinxit IP-0009 new document presets in Pinxit |  |
| LP-1315 | Adjustment layers with default masks | -- | AC-2957 | -- | core | other-app: Pinxit IP-0569 adjustment layer model in Pinxit |  |
| LP-1316 | Clip an adjustment layer to the layer below | -- | AC-2958, AC-3051 | -- | core | other-app: Pinxit IP-0299 clipping masks in Pinxit |  |
| LP-1317 | Exposure adjustment layer: exposure and contrast | -- | AC-2959, AC-2960 | -- | core | other-app: Pinxit IP-0596 exposure adjustment in Pinxit |  |
| LP-1318 | Levels adjustment layer | -- | AC-2961, AC-2962, AC-2963 | -- | core | other-app: Pinxit IP-0670 levels in Pinxit |  |
| LP-1319 | Curves adjustment layer | -- | AC-2964 | -- | core | other-app: Pinxit IP-0671 curves in Pinxit |  |
| LP-1320 | Light EQ adjustment layer: brighten and darken | -- | AC-2965, AC-2966 | -- | core | other-app: Pinxit IP-0597 shadows and highlights in Pinxit |  |
| LP-1321 | White balance adjustment layer: temperature, tint, picker | -- | AC-2967, AC-2968, AC-2969 | -- | core | other-app: Pinxit IP-0630 white balance adjustment in Pinxit |  |
| LP-1322 | Vibrance adjustment layer: vibrance, saturation, hue, lightness | -- | AC-2970, AC-2971, AC-2972, AC-2973 | -- | core | other-app: Pinxit IP-0612 color and vibrance adjustment in Pinxit |  |
| LP-1323 | Color EQ adjustment layer: per-color hue, saturation, brightness, vibrance | -- | AC-2974, AC-2975 | -- | core | other-app: Pinxit IP-0608 hue and saturation ranges in Pinxit |  |
| LP-1324 | RGB balance adjustment layer | -- | AC-2976 | -- | core | other-app: Pinxit IP-0610 color balance in Pinxit |  |
| LP-1325 | Split tone adjustment layer | -- | AC-2977, AC-2978, AC-2979, AC-2980, AC-2981 | -- | core | other-app: Pinxit IP-0632 split toning in Pinxit |  |
| LP-1326 | Add color adjustment layer with density | -- | AC-2982 | -- | core | other-app: Pinxit IP-0614 photo filter in Pinxit |  |
| LP-1327 | Black and white adjustment layer | -- | AC-2983 | -- | core | other-app: Pinxit IP-0613 black and white in Pinxit |  |
| LP-1328 | Negative adjustment layer | -- | AC-2984 | -- | core | other-app: Pinxit IP-0642 invert in Pinxit |  |
| LP-1329 | Photo effect adjustment layer: preset photographic looks from a list | -- | AC-2985 | -- | core | other-app: Pinxit IP-2370 Pinxit gains a photo effect look list |  |
| LP-1330 | Skin tune: smoothing, glow, radius, as a tool and an adjustment layer | -- | AC-2986, AC-2987, AC-2988, AC-3240, AC-3241, AC-3242, AC-3243 | -- | core | other-app: Pinxit IP-2044 skin smoothing in Pinxit |  |
| LP-1331 | Filter adjustment layers: sharpen, Gaussian and directional blur, noise reduction | -- | AC-2989, AC-2990, AC-2991, AC-2992, AC-2993, AC-2994, AC-2995, AC-2996, AC-2997 | -- | core | other-app: Pinxit IP-1003 live filter layers in Pinxit |  |
| LP-1332 | Clarity and dehaze adjustment layers with Orton, soft light, tonal width, radius, edge processing | -- | AC-2998, AC-2999, AC-3000, AC-3001, AC-3002, AC-3003, AC-3004 | -- | core | other-app: Pinxit IP-0604 clarity and dehaze adjustment layer in Pinxit |  |
| LP-1333 | Gradient map adjustment layer | -- | AC-3005, AC-3006 | -- | core | other-app: Pinxit IP-0626 gradient map in Pinxit |  |
| LP-1334 | Vignette adjustment layer | -- | AC-3007, AC-3008, AC-3009 | -- | core | other-app: Pinxit IP-1199 vignette in Pinxit |  |
| LP-1335 | Posterize adjustment layer | -- | AC-3010 | -- | core | other-app: Pinxit IP-0641 posterize in Pinxit |  |
| LP-1336 | Threshold adjustment layer | -- | AC-3011 | -- | core | other-app: Pinxit IP-0639 threshold in Pinxit |  |
| LP-1337 | Color LUT adjustment layer with LUT import | -- | AC-3012 | -- | core | other-app: Pinxit IP-0622 color lookup in Pinxit |  |
| LP-1338 | Layer masks: add white or black, add from selection automatically, paste as mask | -- | AC-3013, AC-3014, AC-3015, AC-3016, AC-3030, AC-3031, AC-3035, AC-3052 | -- | core | other-app: Pinxit IP-0282 add layer mask in Pinxit |  |
| LP-1339 | Mask opacity | -- | AC-3017 | -- | core | other-app: Pinxit IP-0287 mask density in Pinxit |  |
| LP-1340 | Edit a mask with any tool | -- | AC-3018 | -- | core | other-app: Pinxit IP-0289 paint masks in Pinxit |  |
| LP-1341 | Apply, disable, and enable a mask | -- | AC-3019, AC-3020, AC-3021 | -- | core | other-app: Pinxit IP-0283 mask commands in Pinxit |  |
| LP-1342 | Mask preview and overlay: highlighted or exposed with color and opacity | -- | AC-3022, AC-3026, AC-3027, AC-3028, AC-3029 | -- | core | other-app: Pinxit IP-0286 mask overlay in Pinxit |  |
| LP-1343 | Mask properties: feathering and invert, non-destructive | -- | AC-3023, AC-3024, AC-3025 | -- | core | other-app: Pinxit IP-0297 masks properties in Pinxit |  |
| LP-1344 | Mask to selection: add, subtract, intersect | -- | AC-3032, AC-3033, AC-3034 | -- | core | other-app: Pinxit IP-0288 mask to selection in Pinxit |  |
| LP-1345 | Text tool with editable text layers | -- | AC-3036 | -- | core | other-app: Pinxit IP-1582 type layers in Pinxit |  |
| LP-1346 | Layer effects on text | -- | AC-3037 | -- | core | other-app: Pinxit IP-0374 layer styles on text in Pinxit |  |
| LP-1347 | Dynamic and frame text types, click or drag to place | -- | AC-3038, AC-3039, AC-3041, AC-3042 | -- | core | other-app: Pinxit IP-1584 point and box text in Pinxit |  |
| LP-1348 | Text on a path with anchor editing | -- | AC-3040, AC-3055 | -- | core | other-app: Pinxit IP-1631 type on a path in Pinxit |  |
| LP-1349 | Text formatting: font, size, style, justification, color | -- | AC-3043, AC-3044, AC-3045, AC-3046 | -- | core | other-app: Pinxit IP-1592 character panel in Pinxit |  |
| LP-1350 | Text layer opacity and blend mode | -- | AC-3047, AC-3048 | -- | core | other-app: Pinxit IP-0265 layer blend and opacity in Pinxit |  |
| LP-1351 | Rasterize text layers, merge text with image layers | -- | AC-3049, AC-3050, AC-3060 | -- | core | other-app: Pinxit IP-1590 rasterize type in Pinxit |  |
| LP-1352 | Text transform handles, editing keys, undo, and symbol entry | -- | AC-3053, AC-3054, AC-3056, AC-3057, AC-3058 | -- | core | other-app: Pinxit IP-1587 on-canvas text editing in Pinxit |  |
| LP-1353 | Text snaps to guidelines | -- | AC-3059 | -- | core | other-app: Pinxit IP-0085 snapping in Pinxit |  |
| LP-1354 | Insert image metadata fields as text | -- | AC-3061, AC-3062 | -- | automation | other-app: Pinxit IP-2371 Pinxit gains metadata text insertion |  |
| LP-1355 | Resize canvas: drag edges or exact size, anchor, aspect ratio, resolution, canvas color and opacity, grid, nudge | -- | AC-3063, AC-3064, AC-3065, AC-3066, AC-3067, AC-3068, AC-3069, AC-3070, AC-3071, AC-3072, AC-3073, AC-3074, AC-3075, AC-3076, AC-3077, AC-3078, AC-3079, AC-3080, AC-3081, AC-3082, AC-3083 | -- | core | other-app: Pinxit IP-0142 canvas size with extension color in Pinxit |  |
| LP-1356 | Layer effects framework on image and text layers | -- | AC-3084 | -- | core | other-app: Pinxit IP-0360 layer style effects framework in Pinxit |  |
| LP-1357 | Inner glow effect | -- | AC-3085, AC-3086, AC-3087, AC-3088, AC-3089 | -- | core | other-app: Pinxit IP-0365 inner glow in Pinxit |  |
| LP-1358 | Inner shadow effect | -- | AC-3090, AC-3091, AC-3092, AC-3093, AC-3094, AC-3095 | -- | core | other-app: Pinxit IP-0363 inner shadow in Pinxit |  |
| LP-1359 | Bevel effect with light source | -- | AC-3096, AC-3097, AC-3098 | -- | core | other-app: Pinxit IP-0377 bevel and emboss in Pinxit |  |
| LP-1360 | Outline effect | -- | AC-3099, AC-3100, AC-3101, AC-3102 | -- | core | other-app: Pinxit IP-0367 stroke effect in Pinxit |  |
| LP-1361 | Blur layer effect | -- | AC-3103 | -- | core | other-app: Pinxit IP-0368 Gaussian blur layer effect in Pinxit |  |
| LP-1362 | Drop shadow effect | -- | AC-3104, AC-3105, AC-3106, AC-3107, AC-3108 | -- | core | other-app: Pinxit IP-0362 drop shadow in Pinxit |  |
| LP-1363 | Clipped adjustments leave layer effects unchanged | -- | AC-3109 | -- | core | other-app: Pinxit IP-0310 blend clipped layers as group in Pinxit |  |
| LP-1364 | Rasterize text while keeping layer effects editable | -- | AC-3110 | -- | core | other-app: Pinxit IP-0373 rasterize layer style in Pinxit |  |
| LP-1365 | Copy, paste, and reset layer effects | -- | AC-3111, AC-3112 | -- | core | other-app: Pinxit IP-0370 copy and paste layer style in Pinxit |  |
| LP-1366 | Frequency separation with blur radius and layer view | -- | AC-3113, AC-3114, AC-3115, AC-3116 | -- | core | other-app: Pinxit IP-0934 frequency separation in Pinxit |  |
| LP-1367 | Focus stack of layers with auto-align and keep stack | -- | AC-3117, AC-3118, AC-3119, AC-3120, AC-3121 | -- | core | other-app: Pinxit IP-1551 focus merge in Pinxit |  |
| LP-1368 | HDR merge of layers with auto-align and keep stack | -- | AC-3122, AC-3123, AC-3124, AC-3125, AC-3126 | -- | core | other-app: Pinxit IP-1524 Merge to HDR in Pinxit |  |
| LP-1369 | Auto-align layers | -- | AC-3127 | -- | core | other-app: Pinxit IP-1522 auto-align layers in Pinxit |  |
| LP-1370 | Auto-blend layers: focus blend and HDR blend | -- | AC-3128, AC-3129, AC-3130 | -- | core | other-app: Pinxit IP-1541 auto-blend layers in Pinxit |  |
| LP-1371 | AI denoise in the editor: strength, pixel targeting, blending, opacity, preview, output | -- | AC-3131, AC-3132, AC-3133, AC-3134, AC-3135, AC-3136, AC-3137, AC-3138, AC-3139, AC-3140 | -- | ai | other-app: Pinxit IP-2070 AI noise reduction in Pinxit; Albumen batch denoise is its own row |  |
| LP-1372 | Face edit framework: detected faces, face selector, feature groups, landmark points to correct, symmetric link, presets, no-face message | -- | AC-3141, AC-3142, AC-3158, AC-3194, AC-3195, AC-3196, AC-3198 | -- | ai | other-app: Pinxit IP-2372 Pinxit gains face landmark editing |  |
| LP-1373 | Face reshaping: face width, jaw, chin, forehead, cheekbones, eyes, eyebrows, nose, smile, lips | -- | AC-3143, AC-3144, AC-3145, AC-3146, AC-3147, AC-3148, AC-3149, AC-3150, AC-3151, AC-3152, AC-3159, AC-3160, AC-3161, AC-3162, AC-3164, AC-3165, AC-3166, AC-3167, AC-3169, AC-3171, AC-3172 | -- | ai | other-app: Pinxit IP-0986 face-aware liquify in Pinxit |  |
| LP-1374 | Eye direction horizontal and vertical | -- | AC-3153, AC-3154 | -- | ai | other-app: Pinxit IP-2045 smart portrait gaze in Pinxit |  |
| LP-1375 | Face color retouching: eye sharpen, whitening, eye color, iris, sclera, eyebrow color, nose contouring, teeth whitening, lip color, blush, eyeshadow | -- | AC-3155, AC-3156, AC-3157, AC-3163, AC-3168, AC-3170, AC-3188, AC-3189, AC-3190, AC-3191, AC-3192, AC-3193 | -- | ai | other-app: Pinxit IP-2373 Pinxit gains face color retouching |  |
| LP-1376 | Hair recolor with automatic hair mask: color wheel, natural colors, temperature, tint, saturation, tones, sharpness, mask editing | -- | AC-3173, AC-3174, AC-3175, AC-3176, AC-3177, AC-3178, AC-3179, AC-3180, AC-3181, AC-3197 | -- | ai | other-app: Pinxit IP-2374 Pinxit gains hair recolor |  |
| LP-1377 | Face skin retouching: wrinkles, crow's feet, smoothing, glow, splotch removal, reflections and shadows | -- | AC-3182, AC-3183, AC-3184, AC-3185, AC-3186, AC-3187 | -- | ai | other-app: Pinxit IP-2044 skin smoothing in Pinxit |  |
| LP-1378 | Sky replacement: sky library and custom skies, position, scale, flip, edge, opacity, brightness, temperature, tint, strength, output as layers, presets | -- | AC-3199, AC-3200, AC-3201, AC-3202, AC-3203, AC-3204, AC-3205, AC-3206, AC-3207, AC-3208, AC-3209, AC-3210, AC-3211, AC-3212, AC-3221, AC-3222 | -- | ai | other-app: Pinxit IP-2099 sky replacement in Pinxit |  |
| LP-1379 | Sky replacement lighting and reflections: blend mode, foreground and edge lighting, color adjustment, reflections | -- | AC-3213, AC-3214, AC-3215, AC-3216, AC-3217, AC-3218, AC-3219, AC-3220 | -- | ai | other-app: Pinxit IP-2100 sky replacement lighting in Pinxit |  |
| LP-1380 | Red eye reduction: size, darkening, outline, delete | -- | AC-3223, AC-3224, AC-3225, AC-3226, AC-3227 | -- | core | other-app: Pinxit IP-0915 red eye tool in Pinxit |  |
| LP-1381 | Repair tool: heal with source, nib width, feathering, pressure, cursor preview, straight lines, presets | -- | AC-3229, AC-3230, AC-3234, AC-3235, AC-3236, AC-3237, AC-3238, AC-3239 | -- | core | other-app: Pinxit IP-0908 healing brush in Pinxit |  |
| LP-1382 | Clone and blended clone | -- | AC-3231, AC-3232 | -- | core | other-app: Pinxit IP-0900 clone stamp in Pinxit |  |
| LP-1383 | Special effects gallery with preview, per-effect options, and exit to the filter list | -- | AC-3244, AC-3245, AC-3424, AC-4793 | -- | core | other-app: Pinxit IP-1027 filter gallery in the layered editor |  |
| LP-1384 | Special effect presets: save and reuse effect settings | -- | AC-3246, AC-3431 | -- | core | other-app: Pinxit IP-1013 filter dialog presets |  |
| LP-1385 | Bathroom window effect: bar width and direction | -- | AC-3247, AC-3248, AC-3249 | -- | core | other-app: Pinxit IP-1145 tile glass filter |  |
| LP-1386 | Blinds effect: width, opacity, angle, blind color | -- | AC-3250, AC-3251, AC-3252, AC-3253, AC-3254 | -- | core | other-app: Pinxit IP-1126 blinds filter |  |
| LP-1387 | One-click photo looks: blue steel, childhood, dramatic, gloom, grunge, lomo, purple haze, seventies, somber | -- | AC-3255, AC-3278, AC-3305, AC-3306, AC-3307, AC-3323, AC-3324, AC-3333, AC-3334, AC-3340, AC-3341, AC-3342, AC-3375, AC-3407, AC-3433 | -- | core | other-app: Pinxit IP-2375 look presets are color treatments on Pinxit adjustments |  |
| LP-1388 | Painted look effect (Bob Ross): brush size, coverage, paint thickness, colorfulness, background, randomize | -- | AC-3256, AC-3257, AC-3258, AC-3259, AC-3260, AC-3261, AC-3262 | -- | core | other-app: Pinxit IP-1352 paint daubs filter |  |
| LP-1389 | Bulge effect: center, radius, strength, background, direction | -- | AC-3263, AC-3264, AC-3265, AC-3266, AC-3267, AC-3268, AC-3269 | -- | core | other-app: Pinxit IP-1109 spherize filter |  |
| LP-1390 | Cartoon effect: shading strength, radius, threshold, smoothness, outline detail and strength, artifact suppression | -- | AC-3270, AC-3271, AC-3272, AC-3273, AC-3274, AC-3275, AC-3276, AC-3277 | -- | core | other-app: Pinxit IP-1268 cartoon filter |  |
| LP-1391 | Clouds render: size, detail, seed | -- | AC-3279, AC-3280, AC-3281, AC-3282 | -- | core | other-app: Pinxit IP-1253 clouds render filter |  |
| LP-1392 | Collage effect: number and size of tiles, background, reshuffle | -- | AC-3283, AC-3284, AC-3285, AC-3286, AC-3287 | -- | core | other-app: Pinxit IP-2376 no Pinxit collage filter |  |
| LP-1393 | Colored edges effect: intensity, edge color, edge detection algorithm, blurring | -- | AC-3288, AC-3289, AC-3290, AC-3291, AC-3292 | -- | core | other-app: Pinxit IP-1256 detect edges filter |  |
| LP-1394 | Contours and topography effects: rounding, line frequency or count, strength, line color | -- | AC-3293, AC-3294, AC-3295, AC-3296, AC-3297, AC-3452, AC-3453, AC-3454 | -- | core | other-app: Pinxit IP-1342 trace contour filter |  |
| LP-1395 | Crayon drawing effect | -- | AC-3298 | -- | core | other-app: Pinxit IP-1362 conte crayon filter |  |
| LP-1396 | Crosshatch effect | -- | AC-3299 | -- | core | other-app: Pinxit IP-1374 crosshatch filter |  |
| LP-1397 | Dauber effect: intensity, frequency, background, randomize | -- | AC-3300, AC-3301, AC-3302, AC-3303, AC-3304 | -- | core | other-app: Pinxit IP-1352 paint daubs filter |  |
| LP-1398 | Edge detect effect | -- | AC-3308 | -- | core | other-app: Pinxit IP-1256 detect edges filter |  |
| LP-1399 | Emboss effect: elevation, weight, azimuth | -- | AC-3309, AC-3310, AC-3311, AC-3312 | -- | core | other-app: Pinxit IP-1255 emboss filter |  |
| LP-1400 | Furry edges effect: frequency, threshold, fur length, variance, direction, edge detection, colors, randomize | -- | AC-3313, AC-3314, AC-3315, AC-3316, AC-3317, AC-3318, AC-3319, AC-3320, AC-3321, AC-3322 | -- | core | other-app: Pinxit IP-2377 no Pinxit fur stroke filter |  |
| LP-1401 | Glowing edges effect: intensity and color | -- | AC-3325, AC-3326, AC-3327 | -- | core | other-app: Pinxit IP-1397 glowing edges filter |  |
| LP-1402 | Gradient map effect: dark and light colors | -- | AC-3328, AC-3329, AC-3330, AC-4872 | -- | core | other-app: Pinxit IP-0626 gradient map adjustment |  |
| LP-1403 | Granite effect: light angle | -- | AC-3331, AC-3332 | -- | core | other-app: Pinxit IP-1336 texturizer filter |  |
| LP-1404 | Jiggle distortion: size, detail, strength, randomize | -- | AC-3335, AC-3336, AC-3337, AC-3338, AC-3339 | -- | core | other-app: Pinxit IP-2378 no Pinxit jiggle distortion |  |
| LP-1405 | Mirror effect: direction and axis position | -- | AC-3343, AC-3344, AC-3345 | -- | core | other-app: Pinxit IP-1119 kaleidoscope and mirrors filter |  |
| LP-1406 | Negative effect for scanned film negatives | -- | AC-3346, AC-4860 | -- | core | other-app: Pinxit IP-0642 invert adjustment |  |
| LP-1407 | Oil paint effect: brush width, variance, vibrance | -- | AC-3347, AC-3348, AC-3349, AC-3350 | -- | core | other-app: Pinxit IP-1263 oil paint filter |  |
| LP-1408 | Old photo effect: age amount | -- | AC-3351, AC-3352 | -- | core | other-app: Pinxit IP-1317 old photo filter |  |
| LP-1409 | Orton glow effect: blur, contrast, brightness | -- | AC-3353, AC-3354, AC-3355, AC-3356 | -- | core | other-app: Pinxit IP-1201 diffuse glow filter |  |
| LP-1410 | Outline effect: line width, threshold, background color | -- | AC-3357, AC-3358, AC-3359, AC-3360 | -- | core | other-app: Pinxit IP-1376 ink outlines filter |  |
| LP-1411 | Pencil drawing effect | -- | AC-3361 | -- | core | other-app: Pinxit IP-1383 graphic pen filter |  |
| LP-1412 | Photo effect filters: choose a photo filter type | -- | AC-3362, AC-3363, AC-4874 | -- | core | other-app: Pinxit IP-0614 photo filter adjustment |  |
| LP-1413 | Pixel explosion effect: center, intensity, direction, randomize | -- | AC-3364, AC-3365, AC-3366, AC-3367, AC-3368, AC-3369 | -- | core | other-app: Pinxit IP-2379 no Pinxit pixel explosion filter |  |
| LP-1414 | Pixelate effect: block width and height, square | -- | AC-3370, AC-3371, AC-3372 | -- | core | other-app: Pinxit IP-1150 pixelize and mosaic filter |  |
| LP-1415 | Posterize effect: brightness levels | -- | AC-3373, AC-3374, AC-4858 | -- | core | other-app: Pinxit IP-0641 posterize adjustment |  |
| LP-1416 | Radial waves effect: center, amplitude, wavelength, light strength, background, direction | -- | AC-3376, AC-3377, AC-3378, AC-3379, AC-3380, AC-3381, AC-3382, AC-3383 | -- | core | other-app: Pinxit IP-1123 concentric waves filter |  |
| LP-1417 | Rain effect: strength, opacity, amount, angle and variances, background blur, color | -- | AC-3384, AC-3385, AC-3386, AC-3387, AC-3388, AC-3389, AC-3390, AC-3391, AC-3392 | -- | core | other-app: Pinxit IP-2380 no Pinxit rain filter |  |
| LP-1418 | Ripple effect: center, amplitude, wavelength, light strength, background, direction | -- | AC-3393, AC-3394, AC-3395, AC-3396, AC-3397, AC-3398, AC-3399, AC-3400 | -- | core | other-app: Pinxit IP-1123 concentric waves filter |  |
| LP-1419 | Scattered tiles effect: tile size, scatter amount, background, randomize | -- | AC-3401, AC-3402, AC-3403, AC-3404, AC-3405 | -- | core | other-app: Pinxit IP-1266 tiles filter |  |
| LP-1420 | Sepia effect | -- | AC-3406 | -- | core | other-app: Pinxit IP-0655 sepia filter |  |
| LP-1421 | Sheet metal effect: rounding, detail, angle, metal color, indented or pushed out | -- | AC-3408, AC-3409, AC-3410, AC-3411, AC-3412, AC-3413 | -- | core | other-app: Pinxit IP-1380 bas relief filter |  |
| LP-1422 | Shift effect: strength, bar width, angle, background | -- | AC-3414, AC-3415, AC-3416, AC-3417, AC-3418 | -- | core | other-app: Pinxit IP-1120 shift rows or columns filter |  |
| LP-1423 | Slant effect: amount, fulcrum, background, direction | -- | AC-3419, AC-3420, AC-3421, AC-3422, AC-3423 | -- | core | other-app: Pinxit IP-1183 shear filter |  |
| LP-1424 | Sobel edges effect with apply and cancel | -- | AC-3425, AC-3426 | -- | core | other-app: Pinxit IP-1257 Sobel directional edges filter |  |
| LP-1425 | Solarize and lunarize effect with threshold | -- | AC-3427, AC-3428, AC-3429, AC-3430 | -- | core | other-app: Pinxit IP-1340 solarize filter |  |
| LP-1426 | Right-click a filter slider to reset it and Reset in filter panels | -- | AC-3432, AC-3541, AC-3623 | -- | core | other-app: Pinxit IP-1018 reset filter dialog values |  |
| LP-1427 | Stained glass effect: fragment size, seed | -- | AC-3434, AC-3435, AC-3436 | -- | core | other-app: Pinxit IP-1335 stained glass filter |  |
| LP-1428 | Sunspot effect: position by click, brightness | -- | AC-3437, AC-3438, AC-3439, AC-3440 | -- | core | other-app: Pinxit IP-1254 lens flare render |  |
| LP-1429 | Swirl effect: center, radius, strength and direction, focus, background, axis | -- | AC-3441, AC-3442, AC-3443, AC-3444, AC-3445, AC-3446, AC-3447, AC-3448, AC-3449 | -- | core | other-app: Pinxit IP-1107 twirl filter |  |
| LP-1430 | Threshold effect to pure black and white | -- | AC-3450, AC-3451, AC-4863 | -- | core | other-app: Pinxit IP-0639 threshold adjustment |  |
| LP-1431 | Water reflection effect: position, amplitude, wavelength, perspective, lighting | -- | AC-3455, AC-3456, AC-3457, AC-3458, AC-3459, AC-3460 | -- | core | other-app: Pinxit IP-2381 no Pinxit water reflection filter |  |
| LP-1432 | Water drops effect: density, radius, height, seed | -- | AC-3461, AC-3462, AC-3463, AC-3464, AC-3465 | -- | core | other-app: Pinxit IP-2382 no Pinxit water drops filter |  |
| LP-1433 | Waves effect: wavelength, amplitude, angle, background | -- | AC-3466, AC-3467, AC-3468, AC-3469, AC-3470 | -- | core | other-app: Pinxit IP-1189 wave filter |  |
| LP-1434 | Weave effect: strip width, gap width, background color | -- | AC-3471, AC-3472, AC-3473, AC-3474 | -- | core | other-app: Pinxit IP-1280 weave filter |  |
| LP-1435 | Wind effect: strength, threshold, chance, edge detection, colors, angle, randomize | -- | AC-3475, AC-3476, AC-3477, AC-3478, AC-3479, AC-3480, AC-3481, AC-3482, AC-3483 | -- | core | other-app: Pinxit IP-1185 wind filter |  |
| LP-1436 | User-defined convolution: kernel matrix, division, bias, clear, sample kernels | -- | AC-3484, AC-3485, AC-3486, AC-3487, AC-3488, AC-3489 | -- | core | other-app: Pinxit IP-1345 custom convolution kernel |  |
| LP-1437 | Drawing tools group: shapes with width, feathering, and blending | -- | AC-3490 | -- | core | other-app: Pinxit IP-1675 geometric figures |  |
| LP-1438 | Hand tool and panning with Space or arrow keys | -- | AC-3491, AC-3631, AC-4744, AC-4826, AC-4880 | -- | core | other-app: Pinxit IP-0127 hand tool |  |
| LP-1439 | Move tool for layers, text, and selections with arrow nudge and rotation handle | -- | AC-3492, AC-3493, AC-3497, AC-4881 | -- | core | other-app: Pinxit IP-0277 move tool |  |
| LP-1440 | Snap a layer to canvas edges, center, and corners | -- | AC-3494 | -- | core | other-app: Pinxit IP-0429 align layers to canvas |  |
| LP-1441 | Placement grid while moving | -- | AC-3495 | -- | core | other-app: Pinxit IP-0080 show grid |  |
| LP-1442 | Lock aspect ratio while resizing a layer | -- | AC-3496 | -- | core | other-app: Pinxit IP-0947 proportional transform |  |
| LP-1443 | Move ruler guidelines with the Move tool | -- | AC-3498 | -- | core | other-app: Pinxit IP-0075 drag and move guides |  |
| LP-1444 | Commit or discard a move | -- | AC-3499 | -- | core | other-app: Pinxit IP-0996 free transform commit and cancel |  |
| LP-1445 | Off-canvas layer data kept until a destructive operation | -- | AC-3500, AC-3501, AC-3502, AC-3504 | -- | core | other-app: Pinxit IP-0040 show all and clip to canvas | low-disk fallback is Pinxit scratch handling |
| LP-1446 | Text tool adds a text layer | -- | AC-3505, AC-4884 | -- | core | other-app: Pinxit IP-1584 type tool |  |
| LP-1447 | Rectangle and ellipse drawing with Shift constraint | -- | AC-3506, AC-3507, AC-4885, AC-4886 | -- | core | other-app: Pinxit IP-1679 rectangle and ellipse tools |  |
| LP-1448 | Line and arrow drawing with Shift constraint | -- | AC-3508, AC-3509, AC-4887, AC-4888 | -- | core | other-app: Pinxit IP-1683 line tool with arrowheads |  |
| LP-1449 | Polygon drawing by clicked corners | -- | AC-3510, AC-4889 | -- | core | other-app: Pinxit IP-1682 polygon tool |  |
| LP-1450 | Curve drawing: drag, bend, click to set | -- | AC-3511, AC-4890 | -- | core | other-app: Pinxit IP-1675 geometric figures with arcs |  |
| LP-1451 | Paint brush: foreground on left click, background on right click, opacity, flow | -- | AC-3512, AC-3513, AC-3514, AC-4891 | -- | core | other-app: Pinxit IP-0838 brush tool |  |
| LP-1452 | Brush settings: shape and color dynamics with jitter | -- | AC-3515, AC-3516 | -- | core | other-app: Pinxit IP-0756 shape and color dynamics |  |
| LP-1453 | Mouse wheel changes brush width, Ctrl or Shift wheel changes feathering | -- | AC-3517 | -- | core | other-app: Pinxit IP-2145 modifier plus wheel adjusts tool size |  |
| LP-1454 | Per-stroke undo and redo | -- | AC-3518 | -- | core | other-app: Pinxit IP-0201 undo and redo |  |
| LP-1455 | Paint bucket fill with threshold and connected option | -- | AC-3519, AC-3520, AC-3521, AC-4892 | -- | core | other-app: Pinxit IP-0897 paint bucket tolerance and contiguous |  |
| LP-1456 | Gradient tool: linear or radial, color, opacity, blend mode, commit or discard | -- | AC-3522, AC-3523, AC-3524, AC-3525, AC-3526, AC-4893 | -- | core | other-app: Pinxit IP-0898 gradient tool |  |
| LP-1457 | Eraser to transparency | -- | AC-3527, AC-4894 | -- | core | other-app: Pinxit IP-0844 eraser tool |  |
| LP-1458 | Eyedropper: foreground or background sample, luminance readout | -- | AC-3528, AC-3530, AC-4897 | -- | core | other-app: Pinxit IP-0733 eyedropper tool |  |
| LP-1459 | Sample colors outside the application window | -- | AC-3529 | -- | core | other-app: Pinxit IP-0698 sample colors anywhere on screen |  |
| LP-1460 | Foreground and background color boxes, reset to black and white, swap, color dialogs | -- | AC-3531, AC-3532, AC-4898, AC-4899, AC-4900 | -- | core | other-app: Pinxit IP-0735 foreground and background swatches |  |
| LP-1461 | Color pane in the layered editor | -- | AC-3533, AC-4753 | -- | core | other-app: Pinxit IP-0715 color panel |  |
| LP-1462 | Brush nib width | -- | AC-3534 | -- | core | other-app: Pinxit IP-0841 paint tool brush size |  |
| LP-1463 | Brush feathering | -- | AC-3535 | -- | core | other-app: Pinxit IP-0842 paint tool hardness |  |
| LP-1464 | Brush spacing and auto spacing | -- | AC-3536, AC-3537 | -- | core | other-app: Pinxit IP-0843 paint tool spacing |  |
| LP-1465 | Fill drawn shapes with color | -- | AC-3538 | -- | core | other-app: Pinxit IP-1686 shape fill |  |
| LP-1466 | Stroke opacity | -- | AC-3539 | -- | core | other-app: Pinxit IP-0840 paint tool opacity |  |
| LP-1467 | Stroke blend mode | -- | AC-3540 | -- | core | other-app: Pinxit IP-0793 paint tool blend mode |  |
| LP-1468 | Straight lines with Shift and Shift-click between points while brushing | -- | AC-3542, AC-3543, AC-3689 | -- | core | other-app: Pinxit IP-0798 straight and constrained lines while painting |  |
| LP-1469 | Watermark placement: saved watermark images, drag with ruler guides, anchor point with offsets, resize with aspect, alpha or keyed transparency color, blend mode, opacity, new layer, presets | -- | AC-3544, AC-3545, AC-3546, AC-3547, AC-3548, AC-3549, AC-3550, AC-3551, AC-3552, AC-3553, AC-3554, AC-3555, AC-3556, AC-3557, AC-4790 | -- | core | other-app: Pinxit IP-2383 placed image with watermark presets |  |
| LP-1470 | Filter panel Apply, Done, Cancel, and Reset buttons, apply keeps the tool open | -- | AC-3558, AC-3696 | -- | core | other-app: Pinxit IP-1032 filter apply and cancel with progress |  |
| LP-1471 | Borders: overall and per-side size with final size readout, color with eyedropper | -- | AC-3560, AC-3561, AC-3562, AC-3563, AC-3564, AC-3575, AC-4791 | -- | core | other-app: Pinxit IP-1313 add border |  |
| LP-1472 | Border textures, irregular edges, edge blur, drop shadow, raised edge, light direction, custom texture and edge folders | -- | AC-3565, AC-3566, AC-3567, AC-3568, AC-3569, AC-3570, AC-3571, AC-3572, AC-3573, AC-3574 | -- | core | other-app: Pinxit IP-2384 textured and irregular border frames |  |
| LP-1473 | Vignette frame: focal point, clear and transition zones, stretch, round or rectangular, outline | -- | AC-3576, AC-3577, AC-3578, AC-3579, AC-3580, AC-3581, AC-3582, AC-3583, AC-4792, AC-4868 | -- | core | other-app: Pinxit IP-1199 vignette filter |  |
| LP-1474 | Vignette frame effects: color, desaturate, blur, clouds, edges, radial waves, radial and zoom blur, crayon, dauber, pixelate, old, glowing edges, ripple | -- | AC-3584, AC-3585, AC-3586, AC-3587, AC-3588, AC-3589, AC-3590, AC-3591, AC-3592, AC-3593, AC-3594, AC-3595, AC-3596, AC-3597, AC-3598 | -- | core | other-app: Pinxit IP-1004 any filter through a live filter mask |  |
| LP-1475 | Tilt-shift: focus band guides, 45 degree lock, lens or gaussian blur, amount, bokeh frequency, brightness, sides, saturation | -- | AC-3599, AC-3600, AC-3601, AC-3602, AC-3603, AC-3604, AC-3605, AC-3606, AC-4794 | -- | core | other-app: Pinxit IP-1083 tilt-shift blur |  |
| LP-1476 | Paint or gradient-mask any filter with the edit brush, linear, and radial gradient | -- | AC-3607, AC-3608, AC-3609, AC-4822, AC-4823, AC-4824, AC-4825 | -- | core | other-app: Pinxit IP-1004 live filter mask paint and gradient |  |
| LP-1477 | Film grain: amount, smoothing, size | -- | AC-3610, AC-3611, AC-3612, AC-3613, AC-4795 | -- | core | other-app: Pinxit IP-0635 grain adjustment layer |  |
| LP-1478 | Rotate tool: preset orientations, fine straightening, crop or preserve with fill color, grid | -- | AC-3614, AC-3615, AC-3616, AC-3619, AC-3620, AC-3621, AC-3622, AC-4796 | -- | core | other-app: Pinxit IP-0144 arbitrary canvas rotation |  |
| LP-1479 | Straighten by drawing a horizontal or vertical line | -- | AC-3617, AC-3618 | -- | core | other-app: Pinxit IP-0185 straighten from a drawn line |  |
| LP-1480 | Flip horizontally and vertically | -- | AC-3625, AC-3626, AC-3627, AC-4797 | -- | core | other-app: Pinxit IP-0211 flip canvas |  |
| LP-1481 | Crop tool with drag handles and darkened outside area | -- | AC-3628, AC-3629, AC-3632, AC-4798 | -- | core | other-app: Pinxit IP-0212 crop tool |  |
| LP-1482 | Crop numeric size, units, dpi, constrained ratio and rotate, relative edge offsets, estimated file size | -- | AC-3630, AC-3633, AC-3634, AC-3635, AC-3636, AC-3637, AC-3638, AC-3639, AC-3640 | -- | core | other-app: Pinxit IP-0195 crop presets and numeric modes |  |
| LP-1483 | Perspective correction by corner and side handles with background fill and grid | -- | AC-3641, AC-3642, AC-3643, AC-4799 | -- | core | other-app: Pinxit IP-1159 perspective filter |  |
| LP-1484 | Distortion correction: barrel, pincushion, fisheye, center, strength, scale, background, grid | -- | AC-3644, AC-3645, AC-3646, AC-3647, AC-3648, AC-3649, AC-3650, AC-3651, AC-4800 | -- | core | other-app: Pinxit IP-1161 custom lens distortion correction |  |
| LP-1485 | Lens correction from the Lensfun database: make, model, lens, EXIF lens info, manual strength, CA, transparency or fill, grid | -- | AC-3652, AC-3653, AC-3654, AC-3655, AC-3656, AC-3657, AC-3658, AC-3659, AC-3660, AC-3661, AC-3662, AC-4801 | -- | core | other-app: Pinxit IP-1169 lens correction filter |  |
| LP-1486 | Resize: pixels, percent, print size with dpi, aspect ratio presets and custom, resampling filter, estimated size | -- | AC-3663, AC-3664, AC-3665, AC-3666, AC-3667, AC-3668, AC-3669, AC-3670, AC-4802 | -- | core | other-app: Pinxit IP-0152 image size with units and constraints |  |
| LP-1487 | Resize rules: enlarge only, reduce only, fit width, height, both, or largest side | -- | AC-3671, AC-3672, AC-3673, AC-3674, AC-3675, AC-3676, AC-3677 | -- | core | other-app: Pinxit IP-0162 fit image with do not enlarge |  |
| LP-1488 | Liquify: shift, pinch, bulge, restore, nib width, density, strength, fill or transparency, reset | -- | AC-3678, AC-3679, AC-3680, AC-3681, AC-3682, AC-3683, AC-3684, AC-3685, AC-3686, AC-3687, AC-3688, AC-4803 | -- | core | other-app: Pinxit IP-0990 liquify distortion tools |  |
| LP-1489 | Exposure tool: exposure, auto, contrast, fill light | -- | AC-3690, AC-3691, AC-3692, AC-3693, AC-3694, AC-4804, AC-4856 | -- | core | other-app: Pinxit IP-0586 light adjustment |  |
| LP-1490 | Exposure warning overlay for clipped pixels | -- | AC-3695, AC-4827 | -- | core | other-app: Pinxit IP-0592 clipping display |  |
| LP-1491 | Levels: channel, shadows, midtones, highlights with auto arrows | -- | AC-3697, AC-3698, AC-3699, AC-3700, AC-3701, AC-4805, AC-4866 | -- | core | other-app: Pinxit IP-0670 levels adjustment |  |
| LP-1492 | Levels auto modes and tolerance | -- | AC-3702, AC-3703, AC-3704, AC-3705 | -- | core | other-app: Pinxit IP-0591 auto color correction options |  |
| LP-1493 | Levels black, mid, and white point pickers with RGB readout | -- | AC-3706, AC-3707, AC-3708, AC-3709 | -- | core | other-app: Pinxit IP-0590 point eyedroppers |  |
| LP-1494 | Auto levels: contrast and color, contrast, color, strength | -- | AC-3710, AC-3711, AC-3712, AC-3713, AC-3714, AC-4806 | -- | core | other-app: Pinxit IP-0599 auto tone, contrast, and color |  |
| LP-1495 | Tone curves: channel, histogram, point editing, node readout | -- | AC-3715, AC-3716, AC-3717, AC-3718, AC-3719, AC-4807, AC-4859 | -- | core | other-app: Pinxit IP-0671 curves adjustment |  |
| LP-1496 | Tone curves color picker adds a point from the image | -- | AC-3720 | -- | core | other-app: Pinxit IP-0577 on-image targeted adjustment |  |
| LP-1497 | Light EQ tone equalizer: auto, 1-step, basic, standard bands, advanced curves, on-image drag, wheel, and keys | -- | AC-3721, AC-3722, AC-3723, AC-3724, AC-3725, AC-3726, AC-3727, AC-3728, AC-3729, AC-3730, AC-3731, AC-3732, AC-3733, AC-3734, AC-3735, AC-3736, AC-3737, AC-3738, AC-3739, AC-3740, AC-3741, AC-3742, AC-3743, AC-3744, AC-3745, AC-4808, AC-4871 | -- | core | other-app: Pinxit IP-2385 tone equalizer on the shared develop stage |  |
| LP-1498 | Dehaze with amount | -- | AC-3746, AC-3747, AC-4809, AC-4876 | -- | core | other-app: Pinxit IP-0604 clarity and dehaze adjustment |  |
| LP-1499 | Dodge and burn brushes: tone target, range preview, nib, feathering, strength | -- | AC-3748, AC-3749, AC-3750, AC-3751, AC-3756, AC-3757, AC-3758, AC-4810 | -- | core | other-app: Pinxit IP-0927 dodge and burn tools |  |
| LP-1500 | Saturate and desaturate brushes with standard or vibrance mode | -- | AC-3752, AC-3753, AC-3754, AC-3755 | -- | core | other-app: Pinxit IP-0928 sponge tool |  |
| LP-1501 | White balance: click reference, temperature, tint, strength, neutral pixel mask | -- | AC-3759, AC-3760, AC-3761, AC-3762, AC-3763, AC-3764, AC-4811, AC-4875 | -- | core | other-app: Pinxit IP-0630 white balance adjustment |  |
| LP-1502 | Color EQ: high quality and standard modes, per-color saturation, brightness, hue, contrast, curve, on-image drag | -- | AC-3765, AC-3766, AC-3767, AC-3769, AC-3770, AC-3771, AC-3772, AC-3773, AC-3780, AC-3781, AC-3782, AC-3783, AC-4812, AC-4870 | -- | core | other-app: Pinxit IP-0608 hue and saturation range extensions |  |
| LP-1503 | Color EQ presets | -- | AC-3768 | -- | core | other-app: Pinxit IP-0567 adjustment presets |  |
| LP-1504 | Color EQ global adjustments: vibrance, saturation, color shift, hue, lightness, RGB balance | -- | AC-3774, AC-3775, AC-3776, AC-3777, AC-3778, AC-3779, AC-4861 | -- | core | other-app: Pinxit IP-0612 color and vibrance adjustment |  |
| LP-1505 | Color wheel: select a hue range, eyedropper, invert, mask preview, smoothness, saturation, hue, brightness, contrast, multiple wheels | -- | AC-3784, AC-3785, AC-3786, AC-3787, AC-3788, AC-3789, AC-3790, AC-3791, AC-3792, AC-3793, AC-3794, AC-3796, AC-3797, AC-3798 | -- | core | other-app: Pinxit IP-0279 live hue range mask with adjustments |  |
| LP-1506 | Show previous: compare with the image before the current edit | -- | AC-3795 | -- | core | other-app: Pinxit IP-0573 adjustment view previous |  |
| LP-1507 | Tone wheels: shadow, midtone, highlight tint with eyedroppers, saturation, brightness | -- | AC-3799, AC-3800, AC-3801, AC-3802, AC-3803 | -- | core | other-app: Pinxit IP-0610 color balance |  |
| LP-1508 | Convert to black and white: per-color brightness, channel percentages, contrast, color amount, tint, hover preview | -- | AC-3804, AC-3805, AC-3806, AC-3807, AC-3808, AC-3809, AC-3810, AC-3811, AC-3812, AC-3813, AC-3814, AC-4813, AC-4862 | -- | core | other-app: Pinxit IP-0613 black and white adjustment |  |
| LP-1509 | Split tone: highlight and shadow hue and saturation, balance | -- | AC-3815, AC-3816, AC-3817, AC-3818, AC-3819, AC-3820, AC-4814, AC-4877 | -- | core | other-app: Pinxit IP-0632 split toning |  |
| LP-1510 | Color LUTs filter with .3dl and .cube files | -- | AC-3821, AC-3822, AC-4815, AC-4879 | -- | core | other-app: Pinxit IP-0622 color lookup |  |
| LP-1511 | LUT list management: import, refresh, remove | -- | AC-3823, AC-3824, AC-3825 | -- | core | other-app: Pinxit IP-0624 LUT library management |  |
| LP-1512 | Create a LUT from the adjustment layer stack with description, copyright, format, quality | -- | AC-3826, AC-3827, AC-3828, AC-3829, AC-3830, AC-3831, AC-3832 | -- | core | other-app: Pinxit IP-0625 export LUT from adjustment stack |  |
| LP-1513 | Histogram pane with R, G, B, L toggles | -- | AC-3833, AC-3834, AC-3835, AC-3836, AC-3837, AC-4750 | -- | core | other-app: Pinxit IP-0116 histogram panel |  |
| LP-1514 | Colors dialog: honeycomb, custom colors, spectrum, HSL and RGB entry, preview | -- | AC-3838, AC-3839, AC-3840, AC-3841, AC-3842, AC-3843, AC-3844 | -- | core | other-app: Pinxit IP-0706 color picker dialog |  |
| LP-1515 | Sharpen: amount, radius, mask with preview, detail, threshold | -- | AC-3845, AC-3846, AC-3847, AC-3848, AC-3849, AC-3850, AC-4816, AC-4869 | -- | core | other-app: Pinxit IP-1105 smart sharpen |  |
| LP-1516 | Blur tool: gaussian blur | -- | AC-3851, AC-3852, AC-4817, AC-4857 | -- | core | other-app: Pinxit IP-1097 gaussian blur |  |
| LP-1517 | Linear motion blur with angle | -- | AC-3853 | -- | core | other-app: Pinxit IP-1101 motion blur |  |
| LP-1518 | Radial spin blur with center and direction | -- | AC-3854, AC-3857 | -- | core | other-app: Pinxit IP-1092 radial blur |  |
| LP-1519 | Spread blur | -- | AC-3855 | -- | core | other-app: Pinxit IP-1080 spread |  |
| LP-1520 | Zoom blur in or out | -- | AC-3856 | -- | core | other-app: Pinxit IP-1045 zoom motion blur |  |
| LP-1521 | Smart blur for skin smoothing | -- | AC-3858 | -- | core | other-app: Pinxit IP-1093 smart blur |  |
| LP-1522 | Lens blur with bokeh shape, frequency, brightness | -- | AC-3859, AC-3860, AC-3861 | -- | core | other-app: Pinxit IP-1053 lens blur |  |
| LP-1523 | Noise removal: camera noise luminance and color, strength, tonal and frequency range, channel, Alt preview, legacy settings | -- | AC-3862, AC-3863, AC-3864, AC-3865, AC-3866, AC-3867, AC-3868, AC-3869, AC-3870, AC-3871, AC-4818, AC-4878 | -- | core | other-app: Pinxit IP-1066 reduce noise |  |
| LP-1524 | Median noise removal: square, X, plus kernels | -- | AC-3872, AC-3873, AC-3874, AC-3875 | -- | core | other-app: Pinxit IP-1035 median |  |
| LP-1525 | Despeckle | -- | AC-3876 | -- | core | other-app: Pinxit IP-1067 despeckle |  |
| LP-1526 | AI denoise with strength | -- | AC-3877, AC-3878, AC-4783 | -- | ai | other-app: Pinxit IP-2070 AI noise reduction |  |
| LP-1527 | Add noise: intensity, color proximity, random, monochrome, adjustable color, placement by color, seed | -- | AC-3879, AC-3880, AC-3881, AC-3882, AC-3883, AC-3884, AC-3885, AC-3886 | -- | core | other-app: Pinxit IP-1103 add noise |  |
| LP-1528 | Detail brush: paint blur or sharpen with radius and threshold | -- | AC-3887, AC-3888, AC-3889, AC-3890, AC-4820 | -- | core | other-app: Pinxit IP-0932 blur and sharpen brush |  |
| LP-1529 | Clarity with strength | -- | AC-3891, AC-3892, AC-4819, AC-4865 | -- | core | other-app: Pinxit IP-1056 clarity |  |
| LP-1530 | Chromatic aberration: red and cyan, blue and yellow shifts | -- | AC-3893, AC-3894, AC-3895, AC-4821 | -- | core | other-app: Pinxit IP-1163 chromatic aberration removal |  |
| LP-1531 | Defringe: strength, radius, color | -- | AC-3896, AC-3897, AC-3898 | -- | core | other-app: Pinxit IP-1164 defringe |  |
| LP-1532 | Edit mode tool icons option | -- | AC-4276 | -- | core | other-app: Pinxit IP-2126 Edit mode panel display is Pinxit |  |
| LP-1533 | Edit mode autosave option | -- | AC-4277 | -- | core | other-app: Pinxit IP-1851 Edit mode saving is Pinxit |  |
| LP-1534 | AI image generation from a text prompt (shortcut entry points in browse and the viewer) | -- | AC-4505, AC-4681 | -- | cloud | other-app: Pinxit IP-2014 generating new images is pixel creation, Pinxit's job |  |
| LP-1535 | AI generative edit of the current image (shortcut entry points in browse and the viewer) | -- | AC-4506, AC-4682 | -- | cloud | other-app: Pinxit IP-2090 prompt-driven pixel edits are Pinxit's job |  |
| LP-1536 | Edit-mode general keys: close, minimize, save, save a copy, export, undo, redo, undo all, copy, paste, delete | -- | AC-4702, AC-4703, AC-4710, AC-4711, AC-4712, AC-4717, AC-4718, AC-4719, AC-4720, AC-4721, AC-4722 | -- | core | other-app: Pinxit IP-2150 default keymap conventions |  |
| LP-1537 | Edit-mode key opens Customize Shortcuts | -- | AC-4704 | -- | core | other-app: Pinxit IP-2147 keyboard shortcuts dialog |  |
| LP-1538 | Edit-mode key opens Options | -- | AC-4705 | -- | core | other-app: Pinxit IP-2233 preferences dialog |  |
| LP-1539 | Edit-mode key opens Help | -- | AC-4706 | -- | core | other-app: Pinxit IP-2249 help opens the manual |  |
| LP-1540 | Toggle the full file path in the status bar | -- | AC-4707 | -- | core | other-app: Pinxit IP-0124 status bar and title format |  |
| LP-1541 | Toggle left, right, and bottom panes, and the Filter menu, Actions, Properties, Filmstrip, Info palette, Layers, Undo History, AI panes | -- | AC-4732, AC-4733, AC-4734, AC-4745, AC-4746, AC-4747, AC-4748, AC-4749, AC-4751, AC-4752, AC-4754, AC-4755 | -- | core | other-app: Pinxit IP-2126 panel show and hide |  |
| LP-1542 | Zoom keys: actual size, fit, zoom in and out | -- | AC-4735, AC-4736, AC-4737, AC-4738 | -- | core | other-app: Pinxit IP-0026 zoom commands |  |
| LP-1543 | Full screen key | -- | AC-4739 | -- | core | other-app: Pinxit IP-0037 screen modes and full screen |  |
| LP-1544 | Toggle the Navigator when zoomed | -- | AC-4740 | -- | core | other-app: Pinxit IP-0067 navigator panel |  |
| LP-1545 | Soft proofing key | -- | AC-4741 | -- | core | other-app: Pinxit IP-1955 soft proof |  |
| LP-1546 | Hold to preview the selected layer mask | -- | AC-4742 | -- | core | other-app: Pinxit IP-0286 view mask alone |  |
| LP-1547 | Hold Z to show the saved version | -- | AC-4743 | -- | core | other-app: Pinxit IP-0129 toggle last state |  |
| LP-1548 | Toggle the toolbar, filters toolbar, and actions toolbar | -- | AC-4756, AC-4757, AC-4758 | -- | core | other-app: Pinxit IP-2134 customize toolbar |  |
| LP-1549 | Full screen image or file list on the second screen | -- | AC-4759, AC-4760 | -- | core | other-app: Pinxit IP-2130 window modes |  |
| LP-1550 | Rulers toggle | -- | AC-4761 | -- | core | other-app: Pinxit IP-0126 rulers display toggle |  |
| LP-1551 | Snap to guidelines toggle | -- | AC-4762 | -- | core | other-app: Pinxit IP-0084 snapping toggle |  |
| LP-1552 | Clear all guidelines | -- | AC-4763 | -- | core | other-app: Pinxit IP-0078 clear guides |  |
| LP-1553 | Lock guidelines | -- | AC-4764 | -- | core | other-app: Pinxit IP-0077 lock guides |  |
| LP-1554 | Show or hide guidelines | -- | AC-4765 | -- | core | other-app: Pinxit IP-0080 show guides |  |
| LP-1555 | Select all, deselect, invert selection keys | -- | AC-4766, AC-4767, AC-4768 | -- | core | other-app: Pinxit IP-0544 select all, deselect, invert |  |
| LP-1556 | AI select subject and background keys | -- | AC-4769, AC-4770 | -- | ai | other-app: Pinxit IP-2028 select subject |  |
| LP-1557 | AI select sky key | -- | AC-4771 | -- | ai | other-app: Pinxit IP-2030 select sky |  |
| LP-1558 | AI select hair key | -- | AC-4772 | -- | ai | other-app: Pinxit IP-2031 select people parts |  |
| LP-1559 | Luminance and color range and pixel targeting selection keys | -- | AC-4773, AC-4777 | -- | core | other-app: Pinxit IP-0481 color range |  |
| LP-1560 | Selection from image brightness key | -- | AC-4774 | -- | core | other-app: Pinxit IP-0491 selection from luminosity |  |
| LP-1561 | Refine selection key | -- | AC-4775 | -- | core | other-app: Pinxit IP-0505 refine selection |  |
| LP-1562 | Smart erase selection key and tool | -- | AC-4776, AC-4895 | -- | ai | other-app: Pinxit IP-0925 delete and fill selection |  |
| LP-1563 | Delete selected pixels key | -- | AC-4778 | -- | core | other-app: Pinxit IP-0176 clear selected pixels |  |
| LP-1564 | Save selection key | -- | AC-4779 | -- | core | other-app: Pinxit IP-0450 save selection |  |
| LP-1565 | Load selection key | -- | AC-4780 | -- | core | other-app: Pinxit IP-0451 load selection |  |
| LP-1566 | Manage selections key | -- | AC-4781 | -- | core | other-app: Pinxit IP-0455 selection editor |  |
| LP-1567 | Selection overlay options key | -- | AC-4782 | -- | core | other-app: Pinxit IP-0562 quick mask options |  |
| LP-1568 | AI face edit key | -- | AC-4784 | -- | ai | other-app: Pinxit IP-2045 smart portrait |  |
| LP-1569 | Sky replacement key | -- | AC-4785 | -- | ai | other-app: Pinxit IP-2102 sky replacement |  |
| LP-1570 | Generative edit key | -- | AC-4786 | -- | cloud | other-app: Pinxit IP-2090 prompt to edit |  |
| LP-1571 | Red eye reduction key | -- | AC-4787 | -- | core | other-app: Pinxit IP-0915 red eye tool |  |
| LP-1572 | Repair tool key | -- | AC-4788 | -- | core | other-app: Pinxit IP-0908 healing brush |  |
| LP-1573 | Skin tune key and adjustment layer key | -- | AC-4789, AC-4873 | -- | core | other-app: Pinxit IP-2044 skin smoothing |  |
| LP-1574 | Import image as layer key | -- | AC-4828 | -- | core | other-app: Pinxit IP-1720 place embedded |  |
| LP-1575 | New blank layer key | -- | AC-4829 | -- | core | other-app: Pinxit IP-0267 new layer |  |
| LP-1576 | Duplicate layer key | -- | AC-4830 | -- | core | other-app: Pinxit IP-0268 duplicate layer |  |
| LP-1577 | Delete layer key | -- | AC-4831 | -- | core | other-app: Pinxit IP-0269 delete layer |  |
| LP-1578 | Rename layer key | -- | AC-4832 | -- | core | other-app: Pinxit IP-0270 rename layer |  |
| LP-1579 | Show or hide layer, show all and hide all layers keys | -- | AC-4833, AC-4837, AC-4838 | -- | core | other-app: Pinxit IP-0229 visibility commands |  |
| LP-1580 | Clipping toggle key | -- | AC-4834 | -- | core | other-app: Pinxit IP-0299 clipping masks |  |
| LP-1581 | Merge down key | -- | AC-4835 | -- | core | other-app: Pinxit IP-0274 merge down |  |
| LP-1582 | Merge all layers key | -- | AC-4836 | -- | core | other-app: Pinxit IP-0264 flatten image |  |
| LP-1583 | Frequency separation key | -- | AC-4839 | -- | core | other-app: Pinxit IP-0934 frequency separation |  |
| LP-1584 | Rasterize text layer key | -- | AC-4840 | -- | core | other-app: Pinxit IP-1590 rasterize type layer |  |
| LP-1585 | HDR merge key | -- | AC-4841 | -- | core | other-app: Pinxit IP-1523 combine exposures into HDR |  |
| LP-1586 | Focus stack key | -- | AC-4842 | -- | core | other-app: Pinxit IP-1551 focus merge |  |
| LP-1587 | Auto-align key | -- | AC-4843 | -- | core | other-app: Pinxit IP-1520 auto-align layers |  |
| LP-1588 | Auto-blend key | -- | AC-4844 | -- | core | other-app: Pinxit IP-1540 auto-blend layers |  |
| LP-1589 | Add white or black layer mask and mask from selection keys | -- | AC-4845, AC-4846, AC-4850 | -- | core | other-app: Pinxit IP-0282 add layer mask |  |
| LP-1590 | Combine mask with selection keys: add, subtract, intersect | -- | AC-4847, AC-4848, AC-4849 | -- | core | other-app: Pinxit IP-0288 mask to selection |  |
| LP-1591 | Invert mask key | -- | AC-4851 | -- | core | other-app: Pinxit IP-0285 mask invert |  |
| LP-1592 | Delete or disable mask keys | -- | AC-4852, AC-4855 | -- | core | other-app: Pinxit IP-0283 mask commands |  |
| LP-1593 | Pixel targeting mask key | -- | AC-4853 | -- | core | other-app: Pinxit IP-0294 live hue and luminosity range masks |  |
| LP-1594 | Paste image layer as luminance mask key | -- | AC-4854 | -- | core | other-app: Pinxit IP-0293 luminosity masks |  |
| LP-1595 | RGB adjustment layer key | -- | AC-4864 | -- | core | other-app: Pinxit IP-0610 color balance |  |
| LP-1596 | Vibrance adjustment layer key | -- | AC-4867 | -- | core | other-app: Pinxit IP-0611 vibrance |  |
| LP-1597 | Resize canvas tool key | -- | AC-4882 | -- | core | other-app: Pinxit IP-0209 canvas size |  |
| LP-1598 | AI object selection tool key | -- | AC-4883 | -- | ai | other-app: Pinxit IP-2020 object selection tool |  |
| LP-1599 | AI remove tool key | -- | AC-4896 | -- | ai | other-app: Pinxit IP-2004 remove tool |  |
| LP-1600 | Rectangle and ellipse selection keys | -- | AC-4901, AC-4902 | -- | core | other-app: Pinxit IP-0541 marquee tools |  |
| LP-1601 | Lasso selection key | -- | AC-4903 | -- | core | other-app: Pinxit IP-0542 lasso |  |
| LP-1602 | Magic wand key | -- | AC-4904 | -- | core | other-app: Pinxit IP-0470 magic wand |  |
| LP-1603 | Brush selection key | -- | AC-4905 | -- | core | other-app: Pinxit IP-0498 selection brush |  |
| LP-1604 | Paint toolbox: show paint dialog, arrow tool, tool switching by wheel, magnetic docking, tooltips | -- | -- | IV-0358, IV-0419, IV-0443, IV-0444, IV-0445, IV-1427 | core | other-app: Pinxit IP-2141 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1605 | Paintbrush with foreground and background colors | -- | -- | IV-0420 | core | other-app: Pinxit IP-0838 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1606 | Eraser to background with right-button restore | -- | -- | IV-0421 | core | other-app: Pinxit IP-0823 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1607 | Clone brush | -- | -- | IV-0422 | core | other-app: Pinxit IP-0900 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1608 | Color replacer brush | -- | -- | IV-0423 | core | other-app: Pinxit IP-0814 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1609 | Paint text tool with rich per-character formatting and preview | -- | -- | IV-0424, IV-0425 | core | other-app: Pinxit IP-1584 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1610 | Line and arrow-line tools | -- | -- | IV-0426, IV-0427 | core | other-app: Pinxit IP-1683 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1611 | Rectangle, rounded rectangle, and ellipse tools with fill, transparent fill, and right-button color | -- | -- | IV-0428, IV-0429, IV-0430, IV-0431, IV-0440, IV-0441 | core | other-app: Pinxit IP-1679 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1612 | Flood fill with tolerance | -- | -- | IV-0432, IV-0439 | core | other-app: Pinxit IP-0897 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1613 | Paint color picker | -- | -- | IV-0433 | core | other-app: Pinxit IP-0710 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1614 | Paint straighten tool | -- | -- | IV-0434 | core | other-app: Pinxit IP-0185 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1615 | Paint measure tool | -- | -- | IV-0435 | core | other-app: Pinxit IP-0095 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1616 | Pen and brush settings: line style, width, endings, joins, hatch, smooth lines | -- | -- | IV-0436, IV-0437, IV-0438 | core | other-app: Pinxit IP-1687 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1617 | Foreground and background swatches with swap | -- | -- | IV-0442 | core | other-app: Pinxit IP-0735 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1618 | Undo of paint operations | -- | -- | IV-0446 | core | other-app: Pinxit IP-0201 IrfanView Paint plug-in drawing is layered pixel editing, Pinxit's job |  |
| LP-1619 | Create a new empty image with size, bit depth, and background color | -- | -- | IV-0462, IV-1490 | core | other-app: Pinxit IP-0015 creating blank documents is Pinxit's job |  |
| LP-1620 | Paint plug-in: lines, circles, arrows, straighten | -- | -- | IV-1089 | core | other-app: Pinxit IP-0838 painting is layered pixel editing |  |
