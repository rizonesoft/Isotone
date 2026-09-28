# Adobe Photoshop feature inventory (parity reference for Gesso)

> **Provenance note (2026-09-26):** verbatim copy of the two-part Adobe Photoshop 27.10 inventory compiled for the Gesso parity plan, Part 1 (rows `PS-A-0001` to `PS-A-1750`) followed by Part 2 (rows `PS-B-0001` to `PS-B-1426`, including Camera Raw 18.6). The only edit is that each part's title is demoted to a second-level heading so the file has one title. The ids are stable and each is placed in exactly one row of [`../gesso-parity.md`](../gesso-parity.md). Do not renumber; a future Photoshop version appends new ids after the last id of the matching part (see [`../README.md`](../README.md)).

> **Access limits:** helpx.adobe.com refuses non-browser fetches (HTTP 403), so pages were read through a real browser session; after about 30 page loads Adobe's CDN (Akamai) returned Access Denied for the rest of the session. Rows for long-standing dialogs and option-level detail (Layer Style, Levels, Curves, Brush Settings, Select and Mask, Content-Aware Fill, Image Size, most Filter dialogs, Preferences pages) therefore come from documented product knowledge, each citing the nearest User Guide page for its surface. Check option wording against the running application before treating such a row as a specification.

## Adobe Photoshop feature inventory, Part 1 of 2 (for Gesso parity)

- Product: Adobe Photoshop on desktop (Photoshop 2026 family)
- Version inventoried: 27.10 (August 2026 release). Release notes page last updated Aug 28, 2026; no newer GA build listed as of 2026-09-26. Prior 2026-cycle builds: 27.9.1 (Jul 2026), 27.8 (Jun 2026), 27.7 (May 2026), 27.6 (Apr 2026), 27.5 (Mar 2026), 27.4 (Feb 2026), 27.3 and 27.3.1 (Jan 2026), 27.2 (Dec 2025), 27.1 (Nov 2025), 27.0 (Oct 2025). Current LTS: 26.11.7.
- Compiled: 2026-09-26
- Rows: 1750
- Scope (Part 1): toolbar tools and options bar settings, selection, layers (types, smart objects, masks, panel, blending, styles, comps, align, artboards), blend modes, adjustments, Image menu, Edit menu (transforms, warps, fills), painting (Brush Settings, Brushes, symmetry, color panels), retouching, Channels, Paths, History, Properties panel and Contextual Task Bar, type, shapes and paths, rulers/guides/grids/smart guides, View menu.
- Out of scope (Part 2, separate file): filters incl. Camera Raw, Neural Filters, Liquify, Blur Gallery; actions, automation and scripting; video/timeline/animation; 3D; file formats and export; print; color settings; preferences; workspace/UI; cloud; generative AI. Rows here that touch those areas appear only where a Part 1 surface exposes them (for example a tool option or a Contextual Task Bar action) and are tagged with the matching Category.

## Primary sources

- Release notes: https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html
- What's new: https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html
- User Guide root (new desktop structure): https://helpx.adobe.com/photoshop/desktop/ (legacy https://helpx.adobe.com/photoshop/user-guide.html redirects into it)
- Per-row Source column cites the specific User Guide page. Legacy pages under https://helpx.adobe.com/photoshop/using/ are cited only where they were verified live (HTTP 200) during this session.
- Secondary corroboration for version history: CG Channel Photoshop 27.0/27.6/27.8 articles, PetaPixel (Apr 2026), Fstoppers 27.6 overview.

## Method notes

- helpx.adobe.com rejects WebFetch/curl (403). Pages were read through a real Chrome session (claude-in-chrome): release notes, what's new, the full left-navigation tree of the desktop User Guide (468 page URLs harvested), and individual pages for newer features (Selection Brush, Clarity and dehaze, Grain, Light, Color and vibrance, Contextual Task Bar, hover layer bounds, create new layer when brushing, Rotate Object, Cylinder warp, Dynamic Text, Reflection Removal). Legacy /photoshop/using/ URLs were existence-checked with same-origin HEAD requests.
- After about 30 page loads Adobe's CDN (Akamai) returned Access Denied, so the keyboard-shortcut page and several deep option pages could not be re-read. Option lists for long-standing dialogs (Layer Style, Levels, Curves, Brush Settings, Select and Mask, Content-Aware Fill, Image Size, and similar) come from the documented Photoshop UI. Each row cites the closest User Guide page for that surface.
- One row per feature or per behavior-changing option. Where an option group only switches between closely related modes, the modes are listed inside one row (for example Selective Color Method Relative / Absolute). Removed or legacy features (3D) are listed where they still appear in menus and are marked 3d.
- Kind values: tool, tool-option, command, panel, panel-option, adjustment, dialog-option, blend-mode, layer-style, behavior. Category values: core, ai, cloud, automation, video, 3d, print, format.
- Keyboard shortcuts in Feature names are the Windows defaults.


## A01 Toolbar framework and general tool behavior

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0001 | Toolbar (Tools panel) | panel | Window > Tools | Vertical panel of tools with flyout groups; single or double column layout | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0002 | Tool flyout groups | behavior | Toolbar | Tools sharing a slot appear in a flyout on long-press or right-click; the last-used tool is shown | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0003 | Cycle tools in a group with Shift+shortcut | behavior | Toolbar | Shift plus the group letter cycles through tools in that slot (preference Use Shift Key for Tool Switch) | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0004 | Edit Toolbar (Customize Toolbar dialog) | command | Edit > Toolbar | Drag tools and groups to reorder, regroup, or move to Extra Tools | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0005 | Extra Tools slot | behavior | Toolbar | Last toolbar slot holding tools removed from the main toolbar | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0006 | Customize Toolbar Save Preset | dialog-option | Customize Toolbar dialog | Saves the custom toolbar layout to a file | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0007 | Customize Toolbar Load Preset | dialog-option | Customize Toolbar dialog | Loads a saved toolbar layout | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0008 | Customize Toolbar Restore Defaults | dialog-option | Customize Toolbar dialog | Resets toolbar to the default tool set and grouping | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0009 | Customize Toolbar Clear Tools | dialog-option | Customize Toolbar dialog | Moves all tools into Extra Tools | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0010 | Customize Toolbar show or hide controls | dialog-option | Customize Toolbar dialog | Toggles visibility of Edit Toolbar, Foreground/Background, Quick Mask and Screen Mode buttons at the bottom of the toolbar | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0011 | Toolbar Edit Toolbar button (ellipsis) | behavior | Toolbar | Bottom toolbar button opening the Extra Tools list and Edit Toolbar | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0012 | Foreground and Background color swatches | behavior | Toolbar | Two overlapping swatches showing current foreground and background colors; click to open Color Picker | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0013 | Default colors (D) | command | Toolbar | Resets foreground to black and background to white | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0014 | Switch colors (X) | command | Toolbar | Swaps foreground and background colors | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0015 | Quick Mask mode button (Q) | command | Toolbar | Toggles Edit in Quick Mask Mode | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0016 | Change Screen Mode button (F) | command | Toolbar | Cycles Standard, Full Screen with Menu Bar, and Full Screen modes | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0017 | Tool presets | panel | Window > Tool Presets | Saved tool settings recallable from Tool Presets panel or options bar tool preset picker | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/create-tool-preset.html |
| PS-A-0018 | Tool Preset picker | tool-option | Options bar left end | Dropdown to choose, create, and manage presets for the active tool | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/create-tool-preset.html |
| PS-A-0019 | Current Tool Only filter | panel-option | Tool Presets panel | Shows only presets belonging to the active tool | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/create-tool-preset.html |
| PS-A-0020 | Reset Tool / Reset All Tools | command | Options bar tool icon context menu | Restores default options for the current tool or all tools | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/create-tool-preset.html |
| PS-A-0021 | Spring-loaded tool shortcuts | behavior | Keyboard | Holding a tool shortcut temporarily switches tools and returns on release | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/spring-loaded-shortcuts.html |
| PS-A-0022 | Options bar | panel | Window > Options | Horizontal bar showing settings for the active tool | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/workspace-overview.html |
| PS-A-0023 | Contextual Task Bar | panel | Window > Contextual Task Bar | On-canvas floating bar showing next-step actions based on selection or layer state | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-0024 | Contextual Task Bar pin position | panel-option | Contextual Task Bar menu | Pin bar position, reset position, or hide bar | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-0025 | Tool pointers Standard / Precise / Brush size | behavior | Preferences > Cursors | Selects cursor style for painting and other tools | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/change-tool-pointers.html |
| PS-A-0026 | Show crosshair in brush tip | behavior | Preferences > Cursors | Draws crosshair at center of brush cursor | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/change-tool-pointers.html |
| PS-A-0027 | Show only crosshair while painting | behavior | Preferences > Cursors | Hides brush outline during strokes for performance | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/change-tool-pointers.html |
| PS-A-0028 | Caps Lock precise cursor toggle | behavior | Keyboard | Caps Lock switches painting cursors to precise crosshair | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/change-tool-pointers.html |
| PS-A-0029 | Rich Tooltips | behavior | Preferences > Tools | Animated tool tooltips showing how each tool works | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-0030 | Scrubby sliders | behavior | Options bar and panels | Dragging on a field label changes its numeric value | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/use-simple-math.html |
| PS-A-0031 | Simple math in number fields | behavior | Numeric fields | Evaluates plus, minus, multiply, divide expressions entered in numeric fields | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/use-simple-math.html |
| PS-A-0032 | Unit suffix entry in fields | behavior | Numeric fields | Typing px, in, cm, mm, pt, pica, % converts to the document unit | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/use-simple-math.html |

## A02 Move tool

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0033 | Move tool (V) | tool | Toolbar | Moves selected layers, selections contents, guides; drags layers between documents | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0034 | Auto-Select | tool-option | Options bar > Move tool | Clicking on canvas selects the topmost layer with pixels under the pointer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0035 | Auto-Select target Layer or Group | tool-option | Options bar > Move tool | Chooses whether auto-select picks individual layers or their top-level group | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0036 | Ctrl-click temporary auto-select | behavior | Canvas | Holding Ctrl while clicking with Move tool auto-selects without the option enabled | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0037 | Show Transform Controls | tool-option | Options bar > Move tool | Displays bounding box with handles on the selected layer for direct transforms | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0038 | Align buttons (left, horizontal center, right, top, vertical center, bottom) | tool-option | Options bar > Move tool | Aligns selected layers or layer to selection | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0039 | Distribute buttons | tool-option | Options bar > Move tool | Distributes three or more layers evenly by edges or centers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/distribute-layers-groups-evenly.html |
| PS-A-0040 | Align and Distribute more options (ellipsis) | tool-option | Options bar > Move tool | Popup with Distribute Spacing horizontal and vertical and Align To Selection or Canvas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0041 | Align To Selection / Canvas | tool-option | Options bar > Move tool | Sets reference for alignment to selection bounds or canvas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0042 | Auto-Align Layers button | tool-option | Options bar > Move tool | Opens Auto-Align Layers dialog from options bar | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-image-layers.html |
| PS-A-0043 | 3D Mode buttons (removed) | tool-option | Options bar > Move tool | Legacy 3D orbit/pan/slide controls, removed with 3D feature retirement | 3d | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-A-0044 | Set additional Move tool options (gear) | tool-option | Options bar > Move tool | Popup for hover layer bounds and group expansion options | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0045 | Show hover layer bounds | tool-option | Move tool gear popup | Previews outline of layer under pointer before selecting | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0046 | Show Layers panel highlight on hover | tool-option | Move tool gear popup | Highlights the hovered layer row in the Layers panel | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0047 | Expand groups when selecting from canvas | tool-option | Move tool gear popup | Auto-expands layer groups in Layers panel when a nested layer is selected on canvas | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0048 | Cycle overlapping hover bounds with [ and ] | behavior | Canvas | Steps through stacked layers under the pointer when hover bounds are visible | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0049 | Hover bounds color and thickness | behavior | Preferences > Guides, Grid and Slices | Sets hover boundary color, thickness and panel highlight color | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hover-layer-bounds-in-the-move-tool.html |
| PS-A-0050 | Nudge with arrow keys | behavior | Canvas | Moves selected layer 1 px, or 10 px with Shift | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/control-the-movement-of-a-selection.html |
| PS-A-0051 | Alt-drag duplicate | behavior | Canvas | Alt-dragging with Move tool duplicates the layer or selection contents | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/create-multiple-copies-of-a-selection-within-an-image.html |
| PS-A-0052 | Shift constrain move | behavior | Canvas | Constrains movement to horizontal, vertical or 45 degree direction | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/control-the-movement-of-a-selection.html |
| PS-A-0053 | Drag layer to another document | behavior | Canvas | Copies layer into another open document; Shift centers or registers position | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0054 | Distance measurement readout (Ctrl hover) | behavior | Canvas | Shows smart guide distances between selected layer and others while holding Ctrl | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/work-efficiently-with-smart-guides.html |
| PS-A-0055 | Move tool right-click layer picker | behavior | Canvas | Context menu lists all layers under the pointer for selection | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/select-layers.html |

## A03 Artboard tool

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0056 | Artboard tool | tool | Toolbar (Move group) | Creates, resizes, and moves artboards | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0057 | Artboard Size preset | tool-option | Options bar > Artboard tool | Preset device and paper sizes for the selected artboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0058 | Artboard Width and Height | tool-option | Options bar > Artboard tool | Numeric dimensions for the selected artboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-0059 | Make Portrait / Landscape | tool-option | Options bar > Artboard tool | Swaps orientation of the artboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-0060 | Add New Artboard buttons | tool-option | Options bar > Artboard tool | Plus buttons around a selected artboard add an adjacent artboard of the same size | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/add-artboards-current-document.html |
| PS-A-0061 | Artboard Layout options gear | tool-option | Options bar > Artboard tool | Sets Auto-nest layers, Auto-size canvas, and keep relative positioning when reordering | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-0062 | Auto-nest Layers | tool-option | Options bar > Artboard tool | Moves layers dragged onto an artboard into that artboard group | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0063 | Auto-size Canvas | tool-option | Options bar > Artboard tool | Expands canvas automatically to contain all artboards | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0064 | Alt-drag artboard duplicate | behavior | Canvas | Duplicates an artboard with its contents | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |

## A04 Marquee tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0065 | Rectangular Marquee tool (M) | tool | Toolbar | Draws rectangular selections | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0066 | Elliptical Marquee tool (M) | tool | Toolbar | Draws elliptical selections | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0067 | Single Row Marquee tool | tool | Toolbar | Selects a 1 pixel tall full-width row | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0068 | Single Column Marquee tool | tool | Toolbar | Selects a 1 pixel wide full-height column | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0069 | New Selection mode | tool-option | Options bar > Marquee tools | New selection replaces existing selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0070 | Add to Selection mode | tool-option | Options bar > Marquee tools | New selection area is added; Shift temporarily enables | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0071 | Subtract from Selection mode | tool-option | Options bar > Marquee tools | New selection area is removed; Alt temporarily enables | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0072 | Intersect with Selection mode | tool-option | Options bar > Marquee tools | Result keeps only overlap; Shift+Alt temporarily enables | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/select-area-intersected-by-other-selections.html |
| PS-A-0073 | Feather (px) | tool-option | Options bar > Marquee tools | Softens selection edge by specified radius at creation time | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/define-feathered-edges.html |
| PS-A-0074 | Anti-alias (Elliptical) | tool-option | Options bar > Marquee tools | Smooths jagged elliptical edges with partial selection of edge pixels | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/select-pixels-using-anti-aliasing.html |
| PS-A-0075 | Style Normal | tool-option | Options bar > Marquee tools | Free drag sizing | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0076 | Style Fixed Ratio | tool-option | Options bar > Marquee tools | Constrains marquee to entered width to height ratio | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0077 | Style Fixed Size | tool-option | Options bar > Marquee tools | Creates marquee of exact entered width and height | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0078 | Swap width and height | tool-option | Options bar > Marquee tools | Button swaps Fixed Ratio or Fixed Size values | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0079 | Select and Mask button | tool-option | Options bar > Marquee tools | Opens Select and Mask workspace from any selection tool | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0080 | Shift constrain square or circle | behavior | Canvas | Shift while dragging constrains to square or circle | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0081 | Alt draw from center | behavior | Canvas | Alt while dragging draws marquee from center | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0082 | Spacebar reposition while drawing | behavior | Canvas | Hold Space during drag to move the marquee being drawn | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/move-selection-or-selection-border.html |

## A05 Lasso tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0083 | Lasso tool (L) | tool | Toolbar | Freehand selection border | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/draw-freeform-segments-of-a-selection-border.html |
| PS-A-0084 | Polygonal Lasso tool | tool | Toolbar | Straight-edged segment selection by clicking points | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/draw-straight-edged-segments-of-a-selection-border.html |
| PS-A-0085 | Magnetic Lasso tool | tool | Toolbar | Border snaps to high-contrast edges while dragging | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/snap-to-image-edges-using-magnetic-lasso-tool.html |
| PS-A-0086 | Lasso selection modes | tool-option | Options bar > Lasso tools | New, Add, Subtract, Intersect selection modes | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/draw-freeform-segments-of-a-selection-border.html |
| PS-A-0087 | Lasso Feather | tool-option | Options bar > Lasso tools | Feather radius applied to lasso selections | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/draw-freeform-segments-of-a-selection-border.html |
| PS-A-0088 | Lasso Anti-alias | tool-option | Options bar > Lasso tools | Smooths lasso selection edges | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/draw-freeform-segments-of-a-selection-border.html |
| PS-A-0089 | Alt toggle freehand and straight segments | behavior | Canvas | Alt switches Lasso and Polygonal Lasso behavior mid-selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/draw-straight-edged-segments-of-a-selection-border.html |
| PS-A-0090 | Backspace remove last point | behavior | Canvas | Deletes last polygonal or magnetic point | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/draw-freeform-segments-of-a-selection-border.html |
| PS-A-0091 | Magnetic Lasso Width | tool-option | Options bar > Magnetic Lasso | Edge detection radius from pointer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/snap-to-image-edges-using-magnetic-lasso-tool.html |
| PS-A-0092 | Magnetic Lasso Contrast | tool-option | Options bar > Magnetic Lasso | Minimum edge contrast sensitivity | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/snap-to-image-edges-using-magnetic-lasso-tool.html |
| PS-A-0093 | Magnetic Lasso Frequency | tool-option | Options bar > Magnetic Lasso | Rate at which fastening points are set | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/snap-to-image-edges-using-magnetic-lasso-tool.html |
| PS-A-0094 | Magnetic Lasso Use Tablet Pressure to Change Pen Width | tool-option | Options bar > Magnetic Lasso | Stylus pressure narrows edge width | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/snap-to-image-edges-using-magnetic-lasso-tool.html |
| PS-A-0095 | Magnetic Lasso bracket keys width | behavior | Canvas | [ and ] change edge detection width while drawing | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/snap-to-image-edges-using-magnetic-lasso-tool.html |
| PS-A-0096 | Magnetic Lasso manual point click | behavior | Canvas | Clicking adds fastening point manually | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/snap-to-image-edges-using-magnetic-lasso-tool.html |

## A06 Object Selection tool

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0097 | Object Selection tool (W) | tool | Toolbar | Selects an object by drawing a rectangle or lasso around it or by clicking a hovered object | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0098 | Object Finder (hover highlight) | tool-option | Options bar > Object Selection tool | Automatically detects objects and highlights them on hover for one-click selection | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0099 | Object Finder refresh | tool-option | Options bar > Object Selection tool | Recomputes detected objects after edits | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0100 | Show All Objects | tool-option | Options bar > Object Selection tool | Overlays all detected object masks at once | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0101 | Object Finder overlay settings | tool-option | Options bar > Object Selection tool | Sets overlay color, opacity, outline display for detected objects | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0102 | Mode Rectangle | tool-option | Options bar > Object Selection tool | Drag a rectangle around the object to select it | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0103 | Mode Lasso | tool-option | Options bar > Object Selection tool | Drag a rough lasso around the object to select it | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0104 | Sample All Layers | tool-option | Options bar > Object Selection tool | Detects objects from composite of all layers | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0105 | Hard Edge | tool-option | Options bar > Object Selection tool | Produces hard selection edges instead of soft | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0106 | Object Subtract | tool-option | Options bar > Object Selection tool | When subtracting, finds and removes the object within the drawn region | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0107 | Selection modes (Object Selection) | tool-option | Options bar > Object Selection tool | New, Add, Subtract, Intersect for object selection | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/select-objects-with-object-selection-tool.html |
| PS-A-0108 | Select Subject button | tool-option | Options bar > Object Selection tool | Selects the main subject from the options bar | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/detect-subject-using-select-subject.html |
| PS-A-0109 | Select Subject processing mode | tool-option | Options bar > Object Selection tool | Device (faster local) or Cloud (detailed results) processing choice | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/improved-select-subject-and-remove-background-results.html |
| PS-A-0110 | Mask All Objects | command | Layer > Mask All Objects | Creates masked groups for every detected object in a layer | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/mask-all-objects-in-a-layer.html |

## A07 Quick Selection tool

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0111 | Quick Selection tool (W) | tool | Toolbar | Paints a selection that expands to find edges | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/paint-a-selection-with-quick-selection-tool.html |
| PS-A-0112 | Quick Selection brush picker | tool-option | Options bar > Quick Selection tool | Size, hardness, spacing, angle, roundness, pressure size for the selection brush | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/paint-a-selection-with-quick-selection-tool.html |
| PS-A-0113 | Quick Selection modes (New / Add / Subtract) | tool-option | Options bar > Quick Selection tool | Mode buttons for starting, adding to or subtracting from selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/paint-a-selection-with-quick-selection-tool.html |
| PS-A-0114 | Quick Selection Sample All Layers | tool-option | Options bar > Quick Selection tool | Uses composite image for edge finding | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/paint-a-selection-with-quick-selection-tool.html |
| PS-A-0115 | Auto-Enhance | tool-option | Options bar > Quick Selection tool | Reduces roughness and blockiness of selection boundary | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/paint-a-selection-with-quick-selection-tool.html |
| PS-A-0116 | Hard Edge (Quick Selection) | tool-option | Options bar > Quick Selection tool | Keeps edges hard instead of soft AI-refined edges | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/paint-a-selection-with-quick-selection-tool.html |
| PS-A-0117 | Quick Selection bracket brush size | behavior | Canvas | [ and ] resize the selection brush | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/paint-a-selection-with-quick-selection-tool.html |

## A08 Magic Wand tool

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0118 | Magic Wand tool (W) | tool | Toolbar | Selects similarly colored pixels by clicking | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/select-areas-by-color-with-the-magic-wand-tool.html |
| PS-A-0119 | Magic Wand Sample Size | tool-option | Options bar > Magic Wand tool | Point sample or averaged 3x3 up to 101x101 area sample | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/select-areas-by-color-with-the-magic-wand-tool.html |
| PS-A-0120 | Tolerance (0 to 255) | tool-option | Options bar > Magic Wand tool | Color range similarity for selecting pixels | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/select-areas-by-color-with-the-magic-wand-tool.html |
| PS-A-0121 | Magic Wand Anti-alias | tool-option | Options bar > Magic Wand tool | Smooths selection edges | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/select-areas-by-color-with-the-magic-wand-tool.html |
| PS-A-0122 | Contiguous | tool-option | Options bar > Magic Wand tool | Selects only adjacent pixels; off selects all matching pixels in the layer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/select-areas-by-color-with-the-magic-wand-tool.html |
| PS-A-0123 | Magic Wand Sample All Layers | tool-option | Options bar > Magic Wand tool | Samples merged visible layers | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/select-areas-by-color-with-the-magic-wand-tool.html |
| PS-A-0124 | Magic Wand selection modes | tool-option | Options bar > Magic Wand tool | New, Add, Subtract, Intersect | core | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/select-areas-by-color-with-the-magic-wand-tool.html |

## A09 Selection Brush tool

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0125 | Selection Brush tool | tool | Toolbar | Paints a selection directly as a colored overlay | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/create-quick-selections-with-selection-brush-tool.html |
| PS-A-0126 | Selection Brush Add mode | tool-option | Options bar > Selection Brush tool | Paints to add to the selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/create-quick-selections-with-selection-brush-tool.html |
| PS-A-0127 | Selection Brush Subtract mode | tool-option | Options bar > Selection Brush tool | Paints to remove from the selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/create-quick-selections-with-selection-brush-tool.html |
| PS-A-0128 | Selection Brush Size | tool-option | Options bar > Selection Brush tool | Brush diameter | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/create-quick-selections-with-selection-brush-tool.html |
| PS-A-0129 | Selection Brush Hardness | tool-option | Options bar > Selection Brush tool | Edge softness of painted selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/create-quick-selections-with-selection-brush-tool.html |
| PS-A-0130 | Selection Brush Opacity | tool-option | Options bar > Selection Brush tool | Partial selection strength of painted strokes | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/create-quick-selections-with-selection-brush-tool.html |
| PS-A-0131 | Selection Brush overlay color | tool-option | Options bar settings | Color of the red overlay showing painted selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/create-quick-selections-with-selection-brush-tool.html |

## A10 Crop and Perspective Crop tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0132 | Crop tool (C) | tool | Toolbar | Crops, straightens, expands canvas non-destructively or destructively | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-photos.html |
| PS-A-0133 | Crop aspect ratio preset menu | tool-option | Options bar > Crop tool | Ratio, W x H x Resolution, Original Ratio, preset sizes, New Crop Preset, Delete Crop Preset | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0134 | Crop Width and Height fields | tool-option | Options bar > Crop tool | Constrained ratio or exact size values | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0135 | Crop Resolution field (W x H x Resolution) | tool-option | Options bar > Crop tool | Resamples the result to entered resolution | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0136 | Swap ratio values | tool-option | Options bar > Crop tool | Swaps width and height; X key rotates crop box orientation | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0137 | Clear ratio | tool-option | Options bar > Crop tool | Clears constraints for freeform crop | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0138 | Straighten | tool-option | Options bar > Crop tool | Draw a line along horizon to rotate crop and straighten image | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/straighten-tilted-photos.html |
| PS-A-0139 | Overlay Rule of Thirds | tool-option | Crop overlay menu | Thirds guide overlay | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0140 | Overlay Grid | tool-option | Crop overlay menu | Fine grid overlay | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0141 | Overlay Diagonal | tool-option | Crop overlay menu | Diagonal lines overlay | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0142 | Overlay Triangle | tool-option | Crop overlay menu | Triangle composition overlay | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0143 | Overlay Golden Ratio | tool-option | Crop overlay menu | Phi grid overlay | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0144 | Overlay Golden Spiral | tool-option | Crop overlay menu | Spiral overlay; Shift+O flips orientation | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0145 | Overlay display Always / Auto / Never | tool-option | Crop overlay menu | When overlay shows | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0146 | Cycle overlay (O) | behavior | Canvas | O cycles overlay types | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0147 | Use Classic Mode | tool-option | Crop settings gear | Moves crop box instead of image | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0148 | Show Crop Preview | tool-option | Crop settings gear | Shows cropped-out area during adjustment | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0149 | Auto Center Preview | tool-option | Crop settings gear | Keeps crop centered on canvas | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0150 | Enable Crop Shield | tool-option | Crop settings gear | Dims area outside crop with color and opacity | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0151 | Crop Shield color and opacity | tool-option | Crop settings gear | Shield color Match Canvas or custom and opacity | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0152 | Auto Adjust Opacity | tool-option | Crop settings gear | Lightens shield while editing the crop | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0153 | Delete Cropped Pixels | tool-option | Options bar > Crop tool | When off, cropped pixels are kept outside canvas for later recovery | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0154 | Content-Aware (crop fill) | tool-option | Options bar > Crop tool | Fills transparent areas created by rotation or expansion using content-aware fill | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/apply-content-aware-fill-while-cropping-images.html |
| PS-A-0155 | Generative Expand | tool-option | Crop tool with Contextual Task Bar | Fills expanded canvas using generative AI | ai | https://helpx.adobe.com/photoshop/desktop/create-open-import-images/create-images/explore-beyond-the-canvas-with-generative-expand.html |
| PS-A-0156 | Crop expand canvas | behavior | Canvas | Dragging crop handles outside canvas enlarges the canvas | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/resize-canvas-using-the-crop-tool.html |
| PS-A-0157 | Crop rotate by dragging outside box | behavior | Canvas | Dragging outside crop rectangle rotates it | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0158 | Commit and cancel crop | tool-option | Options bar > Crop tool | Check mark commits, circle cancels; Enter and Esc | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0159 | Perspective Crop tool (C) | tool | Toolbar | Crops with a four-corner quadrilateral and corrects perspective | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/transform-perspective-while-cropping.html |
| PS-A-0160 | Perspective Crop W H Resolution | tool-option | Options bar > Perspective Crop | Output size and resolution | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-tool-options.html |
| PS-A-0161 | Perspective Crop Front Image | tool-option | Options bar > Perspective Crop | Fills fields from the front document dimensions | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/transform-perspective-while-cropping.html |
| PS-A-0162 | Perspective Crop Show Grid | tool-option | Options bar > Perspective Crop | Toggles perspective grid inside crop | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/transform-perspective-while-cropping.html |

## A11 Slice tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0163 | Slice tool | tool | Toolbar (Crop group) | Divides an image into web slices | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0164 | Slice Style Normal / Fixed Aspect Ratio / Fixed Size | tool-option | Options bar > Slice tool | Constrains slice size | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0165 | Slices From Guides | tool-option | Options bar > Slice tool | Creates slices from current guides | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0166 | Slice Select tool | tool | Toolbar (Crop group) | Selects, moves, resizes slices | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0167 | Slice stacking order buttons | tool-option | Options bar > Slice Select | Bring to front, forward, backward, send to back | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0168 | Promote (user slice) | tool-option | Options bar > Slice Select | Converts auto or layer slice to user slice | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0169 | Divide Slice | tool-option | Options bar > Slice Select | Splits slices horizontally or vertically into equal parts | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0170 | Slice align and distribute | tool-option | Options bar > Slice Select | Aligns or distributes selected slices | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0171 | Hide Auto Slices | tool-option | Options bar > Slice Select | Hides automatic slices | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0172 | Slice Options dialog | tool-option | Options bar > Slice Select | Name, URL, target, message, alt tag, dimensions, background type | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0173 | New Layer Based Slice | command | Layer > New Layer Based Slice | Creates slice matching layer pixel bounds | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |

## A12 Frame tool

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0174 | Frame tool (K) | tool | Toolbar | Draws rectangular or elliptical frames as image placeholders | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/draw-frames.html |
| PS-A-0175 | Rectangular frame | tool-option | Options bar > Frame tool | Draws rectangular frames | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/draw-frames.html |
| PS-A-0176 | Elliptical frame | tool-option | Options bar > Frame tool | Draws elliptical frames | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/draw-frames.html |
| PS-A-0177 | Place image into frame | behavior | Canvas | Dragging image or Place Embedded or Linked into a frame masks it to the frame | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/place-image-frame.html |
| PS-A-0178 | Convert to Frame | command | Layer context menu | Converts shape, text or pixel layer into a frame | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/convert-to-frame.html |
| PS-A-0179 | Select frame or frame content | behavior | Canvas | Double-click toggles selection between frame and its contents | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/select-frame-content.html |
| PS-A-0180 | Frame stroke | panel-option | Properties panel > Frame | Adds stroke with color, width, position to a frame | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/add-stroke-to-frame.html |
| PS-A-0181 | Frame Properties W H X Y | panel-option | Properties panel > Frame | Frame size and position fields | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/draw-frames.html |
| PS-A-0182 | Frame placed content status | panel-option | Properties panel > Frame | Shows whether placed frame content is embedded or linked | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/draw-frames.html |

## A13 Eyedropper family

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0183 | Eyedropper tool (I) | tool | Toolbar | Samples a color into foreground or background (Alt) | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0184 | Eyedropper Sample Size | tool-option | Options bar > Eyedropper tool | Point Sample, 3x3, 5x5, 11x11, 31x31, 51x51, 101x101 Average | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0185 | Eyedropper Sample | tool-option | Options bar > Eyedropper tool | Current Layer, Current and Below, All Layers, All Layers No Adjustments, Current and Below No Adjustments | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0186 | Show Sampling Ring | tool-option | Options bar > Eyedropper tool | Shows ring with new versus previous color during sampling | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0187 | Sample outside Photoshop | behavior | Canvas | Dragging from canvas to screen samples any pixel on screen | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0188 | Alt-click samples in painting tools | behavior | Canvas | Alt temporarily switches painting tools to Eyedropper | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-a-color-while-painting.html |
| PS-A-0189 | HUD color picker | behavior | Canvas | Shift+Alt+right-click shows on-canvas Hue Strip or Hue Wheel picker | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-a-color-while-painting.html |
| PS-A-0190 | Color Sampler tool (I) | tool | Toolbar | Places up to 10 persistent color readout points shown in Info panel | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0191 | Color Sampler Sample Size | tool-option | Options bar > Color Sampler | Point or averaged sample for samplers | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0192 | Color Sampler Clear All | tool-option | Options bar > Color Sampler | Removes all samplers | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0193 | Color sampler readout mode | behavior | Info panel | Per sampler readout mode: Actual, Proof, Grayscale, RGB, HSB, Web, CMYK, Lab, Total Ink, Opacity | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0194 | Ruler tool (I) | tool | Toolbar | Measures distance and angle between two points | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-0195 | Ruler readout (X Y W H A L1 L2) | tool-option | Options bar > Ruler tool | Displays start, width, height, angle, lengths | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0196 | Use Measurement Scale | tool-option | Options bar > Ruler tool | Reports lengths in the measurement scale units | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/manage-measurement-scales.html |
| PS-A-0197 | Straighten Layer | tool-option | Options bar > Ruler tool | Rotates layer so the ruler line is level | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0198 | Ruler Clear | tool-option | Options bar > Ruler tool | Removes the ruler line | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0199 | Protractor (Alt drag from endpoint) | behavior | Canvas | Alt-drag from endpoint creates second line and measures angle | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-0200 | Note tool | tool | Toolbar | Adds text notes anchored on canvas | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0201 | Note Author | tool-option | Options bar > Note tool | Author name stored with notes | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0202 | Note Color | tool-option | Options bar > Note tool | Note icon color | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0203 | Note Clear All | tool-option | Options bar > Note tool | Deletes all notes | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0204 | Show or Hide Notes panel | tool-option | Options bar > Note tool | Opens Notes panel to read and navigate notes | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0205 | Notes panel | panel | Window > Notes | Lists note text with previous and next navigation and delete | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-0206 | Count tool | tool | Toolbar | Clicks place numbered count markers | core | https://helpx.adobe.com/photoshop/using/counting-objects-image.html |
| PS-A-0207 | Count Group | tool-option | Options bar > Count tool | Create, rename, delete, show/hide count groups | core | https://helpx.adobe.com/photoshop/using/counting-objects-image.html |
| PS-A-0208 | Count group color | tool-option | Options bar > Count tool | Color for markers and labels | core | https://helpx.adobe.com/photoshop/using/counting-objects-image.html |
| PS-A-0209 | Count Marker Size and Label Size | tool-option | Options bar > Count tool | Visual size of markers and numbers | core | https://helpx.adobe.com/photoshop/using/counting-objects-image.html |
| PS-A-0210 | Count Clear | tool-option | Options bar > Count tool | Resets current count group | core | https://helpx.adobe.com/photoshop/using/counting-objects-image.html |
| PS-A-0211 | Automatic count from selection | command | Image > Analysis > Record Measurements | Counts selected regions via Measurement Log | core | https://helpx.adobe.com/photoshop/using/counting-objects-image.html |

## A14 Healing and removal tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0212 | Spot Healing Brush tool (J) | tool | Toolbar | Paints over blemishes and blends texture from surrounding area automatically | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0213 | Spot Healing brush picker | tool-option | Options bar > Spot Healing Brush tool | Size, hardness, spacing, angle, roundness, pressure size | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0214 | Spot Healing Mode | tool-option | Options bar > Spot Healing Brush tool | Blend mode for healed pixels including Replace, Normal, Screen, Multiply, Darken, Lighten, Color, Luminosity | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0215 | Type Content-Aware | tool-option | Options bar > Spot Healing Brush tool | Synthesizes fill from nearby content | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0216 | Type Create Texture | tool-option | Options bar > Spot Healing Brush tool | Builds texture from pixels in the brushed area | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0217 | Type Proximity Match | tool-option | Options bar > Spot Healing Brush tool | Uses edge pixels around selection to patch | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0218 | Spot Healing Sample All Layers | tool-option | Options bar > Spot Healing Brush tool | Samples all visible layers for healing onto current or empty layer | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0219 | Spot Healing pressure for size | tool-option | Options bar > Spot Healing Brush tool | Stylus pressure controls brush size | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0220 | Spot Healing brush angle | tool-option | Options bar > Spot Healing Brush tool | Sets brush tip angle | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/spot-healing-brush-tool.html |
| PS-A-0221 | Healing Brush tool (J) | tool | Toolbar | Paints with sampled pixels matching texture, lighting and shading of destination | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0222 | Healing Brush Source Sampled | tool-option | Options bar > Healing Brush tool | Uses Alt-clicked source pixels | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0223 | Healing Brush Source Pattern | tool-option | Options bar > Healing Brush tool | Uses a pattern as source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0224 | Healing Brush Aligned | tool-option | Options bar > Healing Brush tool | Keeps source offset continuous between strokes | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0225 | Healing Brush Use Legacy | tool-option | Options bar > Healing Brush tool | Uses the pre-CC 2014 healing algorithm | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0226 | Healing Brush Sample Current Layer / Current and Below / All Layers | tool-option | Options bar > Healing Brush tool | Layers used as source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0227 | Ignore Adjustment Layers when healing | tool-option | Options bar > Healing Brush tool | Excludes adjustment layers from sample | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0228 | Healing Brush Diffusion | tool-option | Options bar > Healing Brush tool | Controls how fast pasted region adapts to surroundings (1 to 7) | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0229 | Healing Brush Mode | tool-option | Options bar > Healing Brush tool | Blend mode for healing strokes, including Replace | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html |
| PS-A-0230 | Healing Brush Clone Source panel toggle | tool-option | Options bar > Healing Brush tool | Opens Clone Source panel | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/clone-source-panel.html |
| PS-A-0231 | Remove tool (J) | tool | Toolbar | AI tool that removes brushed objects and reconstructs background | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-unwanted-objects-and-distractions.html |
| PS-A-0232 | Remove tool Size | tool-option | Options bar > Remove tool | Brush size for painting over distractions | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-unwanted-objects-and-distractions.html |
| PS-A-0233 | Remove after each stroke | tool-option | Options bar > Remove tool | Applies removal on stroke release; off lets you paint multiple strokes then apply | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-unwanted-objects-and-distractions.html |
| PS-A-0234 | Remove Sample All Layers | tool-option | Options bar > Remove tool | Samples from all visible layers | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-unwanted-objects-and-distractions.html |
| PS-A-0235 | Remove tool Mode Generative AI On / Off / Auto | tool-option | Options bar > Remove tool | Chooses generative fill or traditional content-aware engine for removal | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-unwanted-objects-and-distractions.html |
| PS-A-0236 | Remove tool on-device model | behavior | Remove tool | Runs removal with a downloadable local AI model without cloud | ai | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-A-0237 | Find Distractions People | tool-option | Remove tool Contextual Task Bar | Detects and removes people in background | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-wires-people-distractions.html |
| PS-A-0238 | Find Distractions Wires and Cables | tool-option | Remove tool Contextual Task Bar | Detects and removes wires and power lines | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-wires-people-distractions.html |
| PS-A-0239 | Find Distractions General (signs, poles, other) | tool-option | Remove tool Contextual Task Bar | Detects general distractions for review and removal | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/review-and-refine-general-distractions.html |
| PS-A-0240 | Review and refine distractions | behavior | Remove tool | Toggle individual detected distractions before applying | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/review-and-refine-general-distractions.html |
| PS-A-0241 | Remove tool Contextual Task Bar | panel | Contextual Task Bar | Holds Find distractions, brush size and apply controls | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-objects-from-contextual-task-bar.html |
| PS-A-0242 | Lasso or circle to remove | behavior | Canvas | Circling an object with the Remove tool fills the enclosed area | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-unwanted-objects-and-distractions.html |
| PS-A-0243 | Patch tool (J) | tool | Toolbar | Replaces a selected area with pixels from another area or pattern | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0244 | Patch Normal mode | tool-option | Options bar > Patch tool | Classic patch with Source or Destination option | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0245 | Patch Content-Aware mode | tool-option | Options bar > Patch tool | Synthesizes patch with content-aware algorithm | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0246 | Patch Source | tool-option | Options bar > Patch tool | Drag selection to area to use as replacement | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0247 | Patch Destination | tool-option | Options bar > Patch tool | Drag selection to area that will be replaced | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0248 | Patch Transparent | tool-option | Options bar > Patch tool | Extracts texture with transparent background from sample | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0249 | Use Pattern (Patch) | tool-option | Options bar > Patch tool | Fills patch selection with a pattern | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0250 | Patch Diffusion | tool-option | Options bar > Patch tool | Adaptation speed for Normal mode | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0251 | Patch Structure | tool-option | Options bar > Patch tool Content-Aware | 1 to 7 value for how strictly patch preserves existing structure | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0252 | Patch Color | tool-option | Options bar > Patch tool Content-Aware | 0 to 10 value for algorithmic color blending | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0253 | Patch Sample All Layers | tool-option | Options bar > Patch tool Content-Aware | Uses all layers as source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/repair-a-selected-area-with-the-patch-tool.html |
| PS-A-0254 | Content-Aware Move tool (J) | tool | Toolbar | Moves or extends selected objects and fills the hole automatically | core | https://helpx.adobe.com/photoshop/using/content-aware-patch-move.html |
| PS-A-0255 | Content-Aware Move Mode Move | tool-option | Options bar > Content-Aware Move tool | Moves selection and fills original location | core | https://helpx.adobe.com/photoshop/using/content-aware-patch-move.html |
| PS-A-0256 | Content-Aware Move Mode Extend | tool-option | Options bar > Content-Aware Move tool | Duplicates and extends objects such as architecture | core | https://helpx.adobe.com/photoshop/using/content-aware-patch-move.html |
| PS-A-0257 | Content-Aware Move Structure | tool-option | Options bar > Content-Aware Move tool | 1 to 7 structure preservation | core | https://helpx.adobe.com/photoshop/using/content-aware-patch-move.html |
| PS-A-0258 | Content-Aware Move Color | tool-option | Options bar > Content-Aware Move tool | 0 to 10 color blending | core | https://helpx.adobe.com/photoshop/using/content-aware-patch-move.html |
| PS-A-0259 | Content-Aware Move Sample All Layers | tool-option | Options bar > Content-Aware Move tool | Samples all layers | core | https://helpx.adobe.com/photoshop/using/content-aware-patch-move.html |
| PS-A-0260 | Transform On Drop | tool-option | Options bar > Content-Aware Move tool | Allows scaling and rotating the moved content before commit | core | https://helpx.adobe.com/photoshop/using/content-aware-patch-move.html |
| PS-A-0261 | Red Eye tool (J) | tool | Toolbar | Removes red eye from flash photos by clicking | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/remove-red-eye-in-flash-photos.html |
| PS-A-0262 | Pupil Size | tool-option | Options bar > Red Eye tool | Size of darkened pupil area | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/remove-red-eye-in-flash-photos.html |
| PS-A-0263 | Darken Amount | tool-option | Options bar > Red Eye tool | How dark the corrected pupil becomes | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/remove-red-eye-in-flash-photos.html |

## A15 Brush and painting tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0264 | Brush tool (B) | tool | Toolbar | Paints soft or hard strokes in foreground color | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0265 | Brush Preset picker | tool-option | Options bar > Brush tool | Size, hardness, preset list, angle and roundness widget | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/select-a-preset-brush.html |
| PS-A-0266 | Toggle Brush Settings panel button | tool-option | Options bar > Brush tool | Opens Brush Settings panel | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-0267 | Brush Mode (blend mode) | tool-option | Options bar > Brush tool | Painting blend mode including Behind and Clear | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0268 | Brush Opacity | tool-option | Options bar > Brush tool | Maximum paint coverage per stroke | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0269 | Pressure for Opacity | tool-option | Options bar > Brush tool | Stylus pressure overrides opacity | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0270 | Brush Flow | tool-option | Options bar > Brush tool | Rate paint is applied as pointer moves over area | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0271 | Airbrush style build-up | tool-option | Options bar > Brush tool | Paint builds up while holding mouse button | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0272 | Smoothing (0 to 100 percent) | tool-option | Options bar > Brush tool | Stroke smoothing reduces jitter | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/create-smoother-more-polished-brush-strokes-with-stroke-smoothing.html |
| PS-A-0273 | Smoothing Pulled String Mode | tool-option | Smoothing options gear | Paints only when string is pulled taut | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/create-smoother-more-polished-brush-strokes-with-stroke-smoothing.html |
| PS-A-0274 | Smoothing Stroke Catch-up | tool-option | Smoothing options gear | Continues painting to catch up with pointer after pause | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/create-smoother-more-polished-brush-strokes-with-stroke-smoothing.html |
| PS-A-0275 | Smoothing Catch-up on Stroke End | tool-option | Smoothing options gear | Completes stroke to last pointer position | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/create-smoother-more-polished-brush-strokes-with-stroke-smoothing.html |
| PS-A-0276 | Smoothing Adjust for Zoom | tool-option | Smoothing options gear | Reduces smoothing at high zoom and increases when zoomed out | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/create-smoother-more-polished-brush-strokes-with-stroke-smoothing.html |
| PS-A-0277 | Brush Angle | tool-option | Options bar > Brush tool | Sets brush tip angle from options bar | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0278 | Pressure for Size | tool-option | Options bar > Brush tool | Stylus pressure overrides size | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0279 | Symmetry options (butterfly) | tool-option | Options bar > Brush tool | Enables symmetry painting with selectable symmetry paths | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0280 | Paint in HDR mode | behavior | 32-bit documents | Brush supports HDR color values in 32-bit images | core | https://helpx.adobe.com/photoshop/using/bit-depth.html |
| PS-A-0281 | Brush size and hardness on-canvas drag | behavior | Canvas | Alt+right-drag horizontally sizes, vertically hardness or opacity per preference | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0282 | Number keys set opacity | behavior | Canvas | Typing digits sets opacity; Shift+digits sets flow | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0283 | Shift-click straight line | behavior | Canvas | Shift-click draws straight line from previous point | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/painting-tools-overview.html |
| PS-A-0284 | Create new layer when brushing | behavior | Preferences > General | Automatically adds a pixel layer when painting on a non-paintable layer | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/create-a-new-layer-when-brushing.html |
| PS-A-0285 | Pencil tool (B) | tool | Toolbar | Paints hard-edged aliased strokes | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/auto-erase-with-the-pencil-tool.html |
| PS-A-0286 | Auto Erase | tool-option | Options bar > Pencil tool | Paints background color when stroke starts on foreground-colored pixel | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/auto-erase-with-the-pencil-tool.html |
| PS-A-0287 | Pencil Mode, Opacity, Smoothing, Angle, Pressure | tool-option | Options bar > Pencil tool | Same core controls as Brush without flow or airbrush | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/auto-erase-with-the-pencil-tool.html |
| PS-A-0288 | Color Replacement tool (B) | tool | Toolbar | Replaces sampled color with foreground color preserving texture | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0289 | Color Replacement Mode Hue / Saturation / Color / Luminosity | tool-option | Options bar > Color Replacement tool | Which color components get replaced | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0290 | Sampling Continuous | tool-option | Options bar > Color Replacement tool | Samples colors continuously as you drag | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0291 | Sampling Once | tool-option | Options bar > Color Replacement tool | Replaces only the color sampled at stroke start | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0292 | Sampling Background Swatch | tool-option | Options bar > Color Replacement tool | Replaces only areas containing background color | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0293 | Limits Discontiguous | tool-option | Options bar > Color Replacement tool | Replaces sampled color anywhere under pointer | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0294 | Limits Contiguous | tool-option | Options bar > Color Replacement tool | Replaces colors contiguous with color under pointer | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0295 | Limits Find Edges | tool-option | Options bar > Color Replacement tool | Replaces connected areas preserving edge sharpness | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0296 | Color Replacement Tolerance | tool-option | Options bar > Color Replacement tool | Color similarity range | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0297 | Color Replacement Anti-alias | tool-option | Options bar > Color Replacement tool | Smooth edges of corrected area | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0298 | Mixer Brush tool (B) | tool | Toolbar | Simulates real paint mixing with canvas colors and wetness | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0299 | Current brush load swatch | tool-option | Options bar > Mixer Brush tool | Shows reservoir color; Load Brush, Clean Brush, Load Solid Colors Only | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0300 | Load brush after each stroke | tool-option | Options bar > Mixer Brush tool | Reloads reservoir after every stroke | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0301 | Clean brush after each stroke | tool-option | Options bar > Mixer Brush tool | Cleans brush after every stroke | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0302 | Mixer blend presets | tool-option | Options bar > Mixer Brush tool | Dry, Moist, Wet, Very Wet combos with Light, Heavy mix | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0303 | Wet | tool-option | Options bar > Mixer Brush tool | How much paint is picked up from canvas | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0304 | Load | tool-option | Options bar > Mixer Brush tool | Amount of paint loaded in reservoir | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0305 | Mix | tool-option | Options bar > Mixer Brush tool | Ratio of canvas paint to reservoir paint | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0306 | Mixer Flow | tool-option | Options bar > Mixer Brush tool | Paint flow rate | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-0307 | Mixer Sample All Layers | tool-option | Options bar > Mixer Brush tool | Picks up canvas color from all visible layers | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |

## A16 Clone and pattern stamp

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0308 | Clone Stamp tool (S) | tool | Toolbar | Paints with pixels sampled from another area (Alt-click to set source) | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/retouch-images-with-the-clone-stamp-tool.html |
| PS-A-0309 | Clone Stamp Mode, Opacity, Flow, Airbrush | tool-option | Options bar > Clone Stamp tool | Standard paint controls for cloned pixels | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/retouch-images-with-the-clone-stamp-tool.html |
| PS-A-0310 | Clone Aligned | tool-option | Options bar > Clone Stamp tool | Maintains sample offset across strokes | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/retouch-images-with-the-clone-stamp-tool.html |
| PS-A-0311 | Clone Sample Current Layer / Current and Below / All Layers | tool-option | Options bar > Clone Stamp tool | Source layers for cloning | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/set-sample-sources-for-cloning-and-healing.html |
| PS-A-0312 | Ignore adjustment layers when cloning | tool-option | Options bar > Clone Stamp tool | Excludes adjustment layers from sampling | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/set-sample-sources-for-cloning-and-healing.html |
| PS-A-0313 | Clone Source panel | panel | Window > Clone Source | Up to five clone sources with offset, scale, rotation, flip | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/clone-source-panel.html |
| PS-A-0314 | Clone Source offset X Y | panel-option | Clone Source panel | Numeric offset of source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/clone-source-panel.html |
| PS-A-0315 | Clone Source scale W H | panel-option | Clone Source panel | Scales sampled source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/scale-or-rotate-the-sample-source.html |
| PS-A-0316 | Clone Source rotation | panel-option | Clone Source panel | Rotates sampled source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/scale-or-rotate-the-sample-source.html |
| PS-A-0317 | Clone Source flip horizontal and vertical | panel-option | Clone Source panel | Mirrors sampled source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/scale-or-rotate-the-sample-source.html |
| PS-A-0318 | Clone Source frame offset and lock frame | panel-option | Clone Source panel | Video frame offset for cloning across frames | video | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/clone-source-panel.html |
| PS-A-0319 | Show Overlay | panel-option | Clone Source panel | Shows semi-transparent overlay of source | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/adjust-the-sample-source-overlay-options.html |
| PS-A-0320 | Overlay Opacity | panel-option | Clone Source panel | Opacity of overlay | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/adjust-the-sample-source-overlay-options.html |
| PS-A-0321 | Overlay Clipped | panel-option | Clone Source panel | Clips overlay to brush tip | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/adjust-the-sample-source-overlay-options.html |
| PS-A-0322 | Overlay Auto Hide | panel-option | Clone Source panel | Hides overlay while painting | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/adjust-the-sample-source-overlay-options.html |
| PS-A-0323 | Overlay Invert | panel-option | Clone Source panel | Inverts overlay colors | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/adjust-the-sample-source-overlay-options.html |
| PS-A-0324 | Overlay blend mode | panel-option | Clone Source panel | Normal, Darken, Lighten, Difference overlay blend | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/heal-clone/adjust-the-sample-source-overlay-options.html |
| PS-A-0325 | Pattern Stamp tool (S) | tool | Toolbar | Paints with a pattern | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/define-an-image-as-a-preset-pattern.html |
| PS-A-0326 | Pattern Stamp pattern picker | tool-option | Options bar > Pattern Stamp tool | Pattern to paint with | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/define-an-image-as-a-preset-pattern.html |
| PS-A-0327 | Pattern Stamp Aligned | tool-option | Options bar > Pattern Stamp tool | Keeps pattern continuous across strokes | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/define-an-image-as-a-preset-pattern.html |
| PS-A-0328 | Impressionist | tool-option | Options bar > Pattern Stamp tool | Paints pattern with impressionist daubs | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/define-an-image-as-a-preset-pattern.html |

## A17 History brushes

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0329 | History Brush tool (Y) | tool | Toolbar | Paints pixels from a selected history state or snapshot | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/paint-image-states.html |
| PS-A-0330 | History source column | behavior | History panel | Clicking left column of a state sets the history brush source | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/paint-image-states.html |
| PS-A-0331 | Art History Brush tool (Y) | tool | Toolbar | Paints stylized strokes from history source | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/paint-image-states.html |
| PS-A-0332 | Art History Style | tool-option | Options bar > Art History Brush | Tight Short, Tight Medium, Tight Long, Loose Medium, Loose Long, Dab, Tight Curl, Tight Curl Long, Loose Curl, Loose Curl Long | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/paint-image-states.html |
| PS-A-0333 | Art History Area | tool-option | Options bar > Art History Brush | Area covered by strokes | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/paint-image-states.html |
| PS-A-0334 | Art History Tolerance | tool-option | Options bar > Art History Brush | Limits where strokes paint based on difference from source | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/paint-image-states.html |

## A18 Eraser tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0335 | Eraser tool (E) | tool | Toolbar | Erases to transparency or background color | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/erase-parts-of-an-image-with-the-eraser-tool.html |
| PS-A-0336 | Eraser Mode Brush / Pencil / Block | tool-option | Options bar > Eraser tool | Eraser tip behavior | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/erase-parts-of-an-image-with-the-eraser-tool.html |
| PS-A-0337 | Eraser Opacity, Flow, Airbrush, Smoothing | tool-option | Options bar > Eraser tool | Standard paint controls for erasing | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/erase-parts-of-an-image-with-the-eraser-tool.html |
| PS-A-0338 | Erase to History | tool-option | Options bar > Eraser tool | Erases to the selected history state instead | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/erase-parts-of-an-image-with-the-eraser-tool.html |
| PS-A-0339 | Background Eraser tool (E) | tool | Toolbar | Erases sampled background color to transparency while preserving foreground edges | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/change-pixels-to-transparent-with-the-background-eraser-tool.html |
| PS-A-0340 | Background Eraser Sampling Continuous / Once / Background Swatch | tool-option | Options bar > Background Eraser | Which color gets erased | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/change-pixels-to-transparent-with-the-background-eraser-tool.html |
| PS-A-0341 | Background Eraser Limits Discontiguous / Contiguous / Find Edges | tool-option | Options bar > Background Eraser | Extent of erasing | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/change-pixels-to-transparent-with-the-background-eraser-tool.html |
| PS-A-0342 | Background Eraser Tolerance | tool-option | Options bar > Background Eraser | Color range erased | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/change-pixels-to-transparent-with-the-background-eraser-tool.html |
| PS-A-0343 | Protect Foreground Color | tool-option | Options bar > Background Eraser | Prevents erasing of foreground swatch color | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/change-pixels-to-transparent-with-the-background-eraser-tool.html |
| PS-A-0344 | Magic Eraser tool (E) | tool | Toolbar | Clicks erase similar colored areas to transparency | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/change-similar-pixels-with-the-magic-eraser-tool.html |
| PS-A-0345 | Magic Eraser Tolerance, Anti-alias, Contiguous, Sample All Layers, Opacity | tool-option | Options bar > Magic Eraser | Controls selection-like erasing | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/change-similar-pixels-with-the-magic-eraser-tool.html |

## A19 Gradient and Paint Bucket

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0346 | Gradient tool (G) | tool | Toolbar | Creates live editable gradient fill layers or pixel gradients with on-canvas controls | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0347 | Gradient Mode | tool-option | Options bar > Gradient tool | Gradient (live gradient fill layer) or Classic gradient (pixel) | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0348 | Gradient preset picker | tool-option | Options bar > Gradient tool | Chooses from Gradients presets | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0349 | Gradient type Linear | tool-option | Options bar > Gradient tool | Straight-line gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0350 | Gradient type Radial | tool-option | Options bar > Gradient tool | Circular gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0351 | Gradient type Angle | tool-option | Options bar > Gradient tool | Counterclockwise sweep gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0352 | Gradient type Reflected | tool-option | Options bar > Gradient tool | Symmetric linear gradient both sides of start | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0353 | Gradient type Diamond | tool-option | Options bar > Gradient tool | Diamond-shaped gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0354 | Gradient Method Perceptual | tool-option | Options bar > Gradient tool | Interpolates in perceptually uniform way | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0355 | Gradient Method Linear | tool-option | Options bar > Gradient tool | Linear light interpolation | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0356 | Gradient Method Classic | tool-option | Options bar > Gradient tool | Legacy gamma interpolation | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0357 | Gradient Method Smooth | tool-option | Options bar > Gradient tool | Smooth interpolation removing banding at stops | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0358 | Gradient Method Stripes | tool-option | Options bar > Gradient tool | Hard color steps between stops | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0359 | Gradient Reverse | tool-option | Options bar > Gradient tool | Reverses stop order | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0360 | Gradient Dither | tool-option | Options bar > Gradient tool | Adds noise to reduce banding | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0361 | Gradient Transparency | tool-option | Classic gradient | Uses gradient transparency mask | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0362 | Gradient Mode and Opacity (Classic) | tool-option | Classic gradient | Blend mode and opacity of pixel gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0363 | On-canvas gradient stops | behavior | Canvas | Add, move, recolor, delete color stops directly on canvas widget | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0364 | On-canvas midpoint and opacity | behavior | Canvas | Adjust midpoints and stop opacity on canvas | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-0365 | Gradient Editor dialog | dialog-option | Double-click gradient | Edits presets, stops, smoothness, noise gradients | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0366 | Gradient Type Solid / Noise | dialog-option | Gradient Editor | Solid color stops or random noise gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0367 | Gradient Smoothness | dialog-option | Gradient Editor | Smoothness of transitions for solid gradients | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0368 | Noise Roughness | dialog-option | Gradient Editor | Randomness amount of noise gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0369 | Noise Color Model RGB / HSB / LAB | dialog-option | Gradient Editor | Color model and range sliders for noise gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0370 | Noise Restrict Colors | dialog-option | Gradient Editor | Prevents oversaturated colors | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0371 | Noise Add Transparency | dialog-option | Gradient Editor | Adds random transparency | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0372 | Noise Randomize | dialog-option | Gradient Editor | Generates new random noise gradient | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0373 | Color and opacity stops | dialog-option | Gradient Editor | Stops with color, location, opacity; foreground, background, user color stop types | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0374 | Save gradient as preset | dialog-option | Gradient Editor | New button saves gradient to Gradients panel | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-0375 | Paint Bucket tool (G) | tool | Toolbar | Fills contiguous similar-colored pixels with foreground color or pattern | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |
| PS-A-0376 | Paint Bucket Fill Foreground or Pattern | tool-option | Options bar > Paint Bucket tool | Source of fill | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |
| PS-A-0377 | Paint Bucket Mode and Opacity | tool-option | Options bar > Paint Bucket tool | Blend mode and opacity for the fill | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |
| PS-A-0378 | Paint Bucket Tolerance | tool-option | Options bar > Paint Bucket tool | Color range filled | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |
| PS-A-0379 | Paint Bucket Anti-alias | tool-option | Options bar > Paint Bucket tool | Smooths fill edges | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |
| PS-A-0380 | Paint Bucket Contiguous | tool-option | Options bar > Paint Bucket tool | Fills only adjacent pixels | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |
| PS-A-0381 | Paint Bucket All Layers | tool-option | Options bar > Paint Bucket tool | Uses merged layer data for fill region | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |
| PS-A-0382 | 3D Material Drop tool (removed) | tool | Toolbar | Legacy 3D material tool removed with 3D retirement | 3d | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-paint-bucket-tool.html |

## A20 Blur, Sharpen, Smudge, Dodge, Burn, Sponge

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0383 | Blur tool | tool | Toolbar | Softens hard edges by painting | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0384 | Blur Mode | tool-option | Options bar > Blur tool | Normal, Darken, Lighten, Hue, Saturation, Color, Luminosity | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0385 | Blur Strength | tool-option | Options bar > Blur tool | Amount of blur per stroke | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0386 | Blur Sample All Layers | tool-option | Options bar > Blur tool | Uses data from all visible layers | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0387 | Sharpen tool | tool | Toolbar | Increases edge contrast by painting | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/enhance-edge-contrast-with-the-sharpen-tool.html |
| PS-A-0388 | Sharpen Strength and Mode | tool-option | Options bar > Sharpen tool | Amount and blend mode | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/enhance-edge-contrast-with-the-sharpen-tool.html |
| PS-A-0389 | Protect Detail | tool-option | Options bar > Sharpen tool | Minimizes pixelated artifacts while sharpening | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/enhance-edge-contrast-with-the-sharpen-tool.html |
| PS-A-0390 | Sharpen Sample All Layers | tool-option | Options bar > Sharpen tool | Samples all visible layers | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/enhance-edge-contrast-with-the-sharpen-tool.html |
| PS-A-0391 | Smudge tool | tool | Toolbar | Pushes color along the stroke direction like finger painting | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0392 | Smudge Strength and Mode | tool-option | Options bar > Smudge tool | Amount and blend mode | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0393 | Finger Painting | tool-option | Options bar > Smudge tool | Starts each stroke with foreground color | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0394 | Smudge Sample All Layers | tool-option | Options bar > Smudge tool | Smudges using all visible layers | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/blur-sharpen-filters/blur-specific-areas-with-the-blur-tool.html |
| PS-A-0395 | Dodge tool (O) | tool | Toolbar | Lightens areas by painting | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0396 | Burn tool (O) | tool | Toolbar | Darkens areas by painting | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0397 | Range Shadows / Midtones / Highlights | tool-option | Options bar > Dodge and Burn | Tonal range affected | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0398 | Exposure | tool-option | Options bar > Dodge and Burn | Strength of dodge or burn | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0399 | Protect Tones | tool-option | Options bar > Dodge and Burn | Minimizes clipping and hue shifts | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0400 | Sponge tool (O) | tool | Toolbar | Changes color saturation by painting | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0401 | Sponge Mode Saturate / Desaturate | tool-option | Options bar > Sponge | Direction of saturation change | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0402 | Sponge Flow | tool-option | Options bar > Sponge | Strength of saturation change | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |
| PS-A-0403 | Vibrance (Sponge) | tool-option | Options bar > Sponge | Minimizes clipping of fully saturated colors | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |

## A21 Pen and path tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0404 | Pen tool (P) | tool | Toolbar | Draws paths with anchor points and Bezier handles | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0405 | Freeform Pen tool (P) | tool | Toolbar | Draws paths freehand, adding anchors automatically | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0406 | Magnetic Pen option | tool-option | Options bar > Freeform Pen | Snaps freeform path to image edges with width, contrast, frequency, pen pressure settings | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/overview-of-pen-tool-settings.html |
| PS-A-0407 | Freeform Curve Fit | tool-option | Options bar > Freeform Pen gear | Pixel tolerance for anchor placement | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/overview-of-pen-tool-settings.html |
| PS-A-0408 | Content-Aware Tracing tool | tool | Toolbar (tech preview) | Hover detected edges and click to create paths | ai | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/trace-images-easily-with-the-content-aware-tracing-tool.html |
| PS-A-0409 | Content-Aware Tracing Detail | tool-option | Options bar > Content-Aware Tracing | Amount of edges detected | ai | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/trace-images-easily-with-the-content-aware-tracing-tool.html |
| PS-A-0410 | Curvature Pen tool (P) | tool | Toolbar | Draws smooth curves by placing points; double-click toggles corner | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-curves-and-straight-segments-intuitively.html |
| PS-A-0411 | Add Anchor Point tool | tool | Toolbar | Adds anchor to path segment | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0412 | Delete Anchor Point tool | tool | Toolbar | Removes anchor from path | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0413 | Convert Point tool | tool | Toolbar | Converts smooth and corner points, breaks handles | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0414 | Tool mode Shape / Path / Pixels | tool-option | Options bar > Pen tool | Pen output as shape layer, work path or pixel fill (pixels for shapes only) | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/shape-path-and-pixel-mode-options.html |
| PS-A-0415 | Make Selection button | tool-option | Options bar > Pen tool | Converts current path to selection | core | https://helpx.adobe.com/photoshop/using/converting-paths-selection-borders.html |
| PS-A-0416 | Make Mask button | tool-option | Options bar > Pen tool | Creates vector mask from path | core | https://helpx.adobe.com/photoshop/using/masking-layers-vector-masks.html |
| PS-A-0417 | Make Shape button | tool-option | Options bar > Pen tool | Creates shape layer from path | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0418 | Path operations | tool-option | Options bar > Pen tool | New Layer, Combine Shapes, Subtract Front Shape, Intersect Shape Areas, Exclude Overlapping Shapes, Merge Shape Components | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0419 | Path alignment | tool-option | Options bar > Pen tool | Align and distribute path components | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0420 | Path arrangement | tool-option | Options bar > Pen tool | Bring shape to front, forward, backward, send to back | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0421 | Rubber Band | tool-option | Pen settings gear | Previews next segment as pointer moves | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/overview-of-pen-tool-settings.html |
| PS-A-0422 | Path options Thickness and Color | tool-option | Pen settings gear | On-canvas path display thickness and color | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/overview-of-pen-tool-settings.html |
| PS-A-0423 | Auto Add/Delete | tool-option | Options bar > Pen tool | Pen adds or deletes anchors when clicking on paths | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/overview-of-pen-tool-settings.html |
| PS-A-0424 | Align Edges | tool-option | Options bar > Pen tool | Snaps vector edges to pixel grid | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0425 | Pen modifier Alt handles | behavior | Canvas | Alt drags handle independently; Ctrl temporarily gives Direct Selection | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-paths-with-the-pen-tool.html |
| PS-A-0426 | Path Selection tool (A) | tool | Toolbar | Selects and moves whole paths or shape components | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-0427 | Direct Selection tool (A) | tool | Toolbar | Selects and edits individual anchors and segments | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-0428 | Path Selection Select Active Layers / All Layers | tool-option | Options bar > Path Selection tool | Scope for selecting paths | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-0429 | Path Selection Fill, Stroke, W, H | tool-option | Options bar > Path Selection tool | Shape attributes editable when shape selected | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-0430 | Constrain Path Dragging | tool-option | Options bar > Direct Selection gear | Legacy behavior that constrains segment dragging | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/overview-of-pen-tool-settings.html |
| PS-A-0431 | Show Transform Controls (paths) | tool-option | Options bar > Path Selection tool | Bounding box for transforming path components | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-0432 | Combine (path components) | tool-option | Options bar > Path Selection tool | Merges overlapping selected components | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |

## A22 Type tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0433 | Horizontal Type tool (T) | tool | Toolbar | Creates point or paragraph horizontal text layers | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0434 | Vertical Type tool (T) | tool | Toolbar | Creates vertical text layers | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0435 | Vertical Type Mask tool (T) | tool | Toolbar | Creates a vertical text-shaped selection | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/create-text-selection-borders.html |
| PS-A-0436 | Horizontal Type Mask tool (T) | tool | Toolbar | Creates a horizontal text-shaped selection | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/create-text-selection-borders.html |
| PS-A-0437 | Toggle text orientation | tool-option | Options bar > Type tool | Switches layer between horizontal and vertical | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0438 | Font family and style | tool-option | Options bar > Type tool | Font menu with preview, filters, favorites, similar fonts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/about-fonts.html |
| PS-A-0439 | Font size | tool-option | Options bar > Type tool | Size in points or pixels | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0440 | Anti-aliasing method | tool-option | Options bar > Type tool | None, Sharp, Crisp, Strong, Smooth, Windows LCD, Windows | core | https://helpx.adobe.com/photoshop/using/creating-type.html |
| PS-A-0441 | Text alignment | tool-option | Options bar > Type tool | Left, center, right (top, center, bottom for vertical) | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0442 | Text color | tool-option | Options bar > Type tool | Color of selected characters or layer | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/change-text-color.html |
| PS-A-0443 | Create warped text | tool-option | Options bar > Type tool | Opens Warp Text dialog | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/warp-and-unwarp-text.html |
| PS-A-0444 | Toggle Character and Paragraph panels | tool-option | Options bar > Type tool | Opens Character and Paragraph panels | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0445 | 3D from text (removed) | tool-option | Options bar > Type tool | Legacy 3D extrusion removed with 3D retirement | 3d | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0446 | Point text | behavior | Canvas | Click to create a single-line text layer that grows with typing | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0447 | Paragraph text | behavior | Canvas | Drag to create a text box with wrapping | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/edit-text.html |
| PS-A-0448 | Resize paragraph text box | behavior | Canvas | Handles resize box; Ctrl-drag scales text | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/resize-text.html |
| PS-A-0449 | Convert to point or paragraph text | command | Type > Convert to Paragraph Text | Switches between point and paragraph text | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/edit-text.html |
| PS-A-0450 | Fill new type layers with placeholder text | behavior | Preferences > Type | Lorem ipsum placeholder when creating text | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0451 | Commit with Esc or check mark | behavior | Options bar | Commit or cancel text edits | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0452 | Double-click to edit text | behavior | Canvas | Double-clicking type layer with any tool enters text edit | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/edit-text.html |
| PS-A-0453 | Transform while editing text | behavior | Canvas | Bounding box transform available in text edit mode | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/rotate-text.html |

## A23 Shape tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0454 | Rectangle tool (U) | tool | Toolbar | Draws live rectangle shapes with editable corner radii | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-a-circle-square-or-rectangle.html |
| PS-A-0455 | Ellipse tool (U) | tool | Toolbar | Draws live ellipses | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-a-circle-square-or-rectangle.html |
| PS-A-0456 | Triangle tool (U) | tool | Toolbar | Draws live triangles with corner radius | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0457 | Polygon tool (U) | tool | Toolbar | Draws polygons and stars with side count and star ratio | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-star-shapes.html |
| PS-A-0458 | Line tool (U) | tool | Toolbar | Draws lines with stroke weight and arrowheads | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-lines-and-straight-line-segments.html |
| PS-A-0459 | Custom Shape tool (U) | tool | Toolbar | Draws shapes from Shapes presets | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-custom-shapes.html |
| PS-A-0460 | Shape Fill | tool-option | Options bar > Shape tools | Solid, gradient, pattern or none fill | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-0461 | Shape Stroke color | tool-option | Options bar > Shape tools | Solid, gradient, pattern or none stroke | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-0462 | Stroke width | tool-option | Options bar > Shape tools | Stroke weight in px or pt | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-0463 | Stroke Options Align Inside / Center / Outside | tool-option | Options bar > Shape tools | Stroke position relative to path | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-0464 | Stroke Options Caps Butt / Round / Square | tool-option | Options bar > Shape tools | End cap style | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-0465 | Stroke Options Corners Miter / Round / Bevel | tool-option | Options bar > Shape tools | Join style | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-0466 | Stroke Options Dashed Line with dash and gap | tool-option | Options bar > Shape tools | Dash pattern definition, save stroke preset | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-0467 | Shape W and H with link | tool-option | Options bar > Shape tools | Dimensions and constrain proportions | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0468 | Shape corner radius | tool-option | Options bar > Rectangle and Triangle | Radius of rounded corners | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0469 | Polygon Number of sides | tool-option | Options bar > Polygon | Side count | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-star-shapes.html |
| PS-A-0470 | Polygon Star Ratio | tool-option | Options bar > Polygon gear | Indent to create star | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-star-shapes.html |
| PS-A-0471 | Polygon Smooth Star Indents | tool-option | Options bar > Polygon gear | Rounded inner indents | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-star-shapes.html |
| PS-A-0472 | Polygon Smooth Corners | tool-option | Options bar > Polygon gear | Rounded outer corners | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0473 | Line Weight | tool-option | Options bar > Line tool | Stroke thickness of line | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-lines-and-straight-line-segments.html |
| PS-A-0474 | Line Arrowheads Start / End | tool-option | Options bar > Line gear | Arrowhead width, length, concavity | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-an-arrow.html |
| PS-A-0475 | Shape Unconstrained / Square / Fixed Size / Proportional / From Center | tool-option | Options bar gear | Geometry constraints for drawing | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0476 | Custom Shape picker | tool-option | Options bar > Custom Shape | Chooses shape preset | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-custom-shapes.html |
| PS-A-0477 | Legacy Shapes and More | panel-option | Shapes panel menu | Restores legacy custom shape sets | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/add-legacy-custom-shapes.html |
| PS-A-0478 | Live shape on-canvas corner widgets | behavior | Canvas | Drag inner corner widgets to round corners, Alt for single corner | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/draw-a-circle-square-or-rectangle.html |
| PS-A-0479 | Shape Pixels mode | tool-option | Options bar > Shape tools | Draws rasterized shape into current layer | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/shape-path-and-pixel-mode-options.html |

## A24 Navigation tools

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0480 | Hand tool (H) | tool | Toolbar | Pans the view; Space temporary access | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0481 | Scroll All Windows | tool-option | Options bar > Hand tool | Pans all open documents together | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0482 | Hand 100% / Fit Screen / Fill Screen | tool-option | Options bar > Hand tool | Zoom presets buttons | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0483 | Birds-eye view | behavior | Canvas | Hold H and click to zoom out temporarily and jump to another area | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0484 | Flick panning | behavior | Preferences > Tools | Image continues gliding after flick | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0485 | Rotate View tool (R) | tool | Toolbar | Rotates canvas view non-destructively | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0486 | Rotation Angle | tool-option | Options bar > Rotate View | Numeric view rotation | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0487 | Reset View | tool-option | Options bar > Rotate View | Resets rotation to 0 | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0488 | Rotate All Windows | tool-option | Options bar > Rotate View | Rotates all open documents | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/navigation-and-measuring-tools-overview.html |
| PS-A-0489 | Shift snap rotate 15 degrees | behavior | Canvas | Shift constrains view rotation to 15 degree increments | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0490 | Zoom tool (Z) | tool | Toolbar | Zooms in or out (Alt) the view | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0491 | Resize Windows to Fit | tool-option | Options bar > Zoom | Resizes floating window when zooming | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0492 | Zoom All Windows | tool-option | Options bar > Zoom | Zooms all documents simultaneously | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0493 | Scrubby Zoom | tool-option | Options bar > Zoom | Drag left or right to zoom continuously | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0494 | Animated Zoom | behavior | Preferences > Tools | Continuous zoom while holding mouse | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0495 | Zoom with Scroll Wheel | behavior | Preferences > Tools | Scroll wheel zooms instead of scrolls | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0496 | Zoom Clicked Point to Center | behavior | Preferences > Tools | Centers clicked point after zoom | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0497 | Zoom 100 / Fit / Fill buttons | tool-option | Options bar > Zoom | Actual pixels, Fit Screen, Fill Screen | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0498 | Navigator panel | panel | Window > Navigator | Thumbnail with view box and zoom slider | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-0499 | Navigator proxy view color | panel-option | Navigator panel options | Color of view rectangle | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |

## B01 Select menu

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0500 | All (Ctrl+A) | command | Select menu | Selects entire canvas of the layer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0501 | Deselect (Ctrl+D) | command | Select menu | Removes the selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0502 | Reselect (Shift+Ctrl+D) | command | Select menu | Restores last selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0503 | Inverse (Shift+Ctrl+I) | command | Select menu | Inverts selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/inverse-selection.html |
| PS-A-0504 | All Layers (Alt+Ctrl+A) | command | Select menu | Selects all layers in Layers panel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/select-layers.html |
| PS-A-0505 | Deselect Layers | command | Select menu | Deselects all layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/select-layers.html |
| PS-A-0506 | Find Layers (Alt+Shift+Ctrl+F) | command | Select menu | Focuses Layers panel name filter | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0507 | Isolate Layers | command | Select menu | Filters Layers panel to show only selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0508 | Select Subject | command | Select menu | Automatically selects most prominent subject | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/detect-subject-using-select-subject.html |
| PS-A-0509 | Select Sky | command | Select menu | Automatically selects the sky region | ai | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/replace-the-sky-in-images.html |
| PS-A-0510 | Select People | command | Select menu | Detects people and selects whole person or parts such as skin, hair, clothing, facial features | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/make-precise-selections-using-select-people.html |
| PS-A-0511 | Select People part options | dialog-option | Select People | Choose per person Face, Body skin, Hair, Eyes, Teeth, Lips, Clothing, Eyebrows and similar parts | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/make-precise-selections-using-select-people.html |
| PS-A-0512 | Improved hair selection | behavior | Select Subject | Cloud model producing detailed hair edges | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/make-improved-hair-selections.html |
| PS-A-0513 | Color Range | command | Select menu | Selects pixels by sampled or preset color ranges | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0514 | Focus Area | command | Select menu | Selects in-focus areas of image | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0515 | Select and Mask (Alt+Ctrl+R) | command | Select menu | Opens Select and Mask workspace | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0516 | Modify > Border | command | Select menu | Creates selection band of given width around existing border | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/create-selection-around-selection-border.html |
| PS-A-0517 | Modify > Smooth | command | Select menu | Smooths jagged selection edges with sample radius | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/clean-up-stray-pixels-in-color-based-selection.html |
| PS-A-0518 | Modify > Expand | command | Select menu | Grows selection by pixel amount, optional Apply effect at canvas bounds | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/expand-or-contract-selection.html |
| PS-A-0519 | Modify > Contract | command | Select menu | Shrinks selection by pixel amount, optional Apply effect at canvas bounds | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/expand-or-contract-selection.html |
| PS-A-0520 | Modify > Feather (Shift+F6) | command | Select menu | Feathers selection edges by radius, optional Apply effect at canvas bounds | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/define-feathered-edges.html |
| PS-A-0521 | Grow | command | Select menu | Adds adjacent pixels within Magic Wand tolerance | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/adjust-a-selection-manually.html |
| PS-A-0522 | Similar | command | Select menu | Adds pixels anywhere in image within tolerance | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/adjust-a-selection-manually.html |
| PS-A-0523 | Transform Selection | command | Select menu | Free transform on the selection outline only | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/adjust-a-selection-manually.html |
| PS-A-0524 | Edit in Quick Mask Mode | command | Select menu | Toggles Quick Mask | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0525 | Load Selection | command | Select menu | Loads a channel, layer transparency or mask as selection | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0526 | Load Selection Document and Channel | dialog-option | Load Selection dialog | Source document and channel including Transparency and masks | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0527 | Load Selection Invert | dialog-option | Load Selection dialog | Loads inverse of channel | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0528 | Load Selection Operation | dialog-option | Load Selection dialog | New, Add, Subtract, Intersect with existing selection | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0529 | Save Selection | command | Select menu | Saves selection to new or existing alpha channel | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0530 | Save Selection Operation | dialog-option | Save Selection dialog | Replace, Add, Subtract, Intersect with target channel | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |

## B02 Selection behaviors and edit commands

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0531 | Move selection border | behavior | Canvas | Dragging inside selection with selection tool moves the outline only | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/move-selection-or-selection-border.html |
| PS-A-0532 | Arrow nudge selection border | behavior | Canvas | Arrow keys move selection outline 1 or 10 px | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/control-the-movement-of-a-selection.html |
| PS-A-0533 | Hide selection edges (Ctrl+H) | command | View > Extras | Hides marching ants while keeping selection active | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hide-or-show-selection-edges.html |
| PS-A-0534 | Copy (Ctrl+C) | command | Edit menu | Copies selection from current layer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/copy-and-paste-selections.html |
| PS-A-0535 | Copy Merged (Shift+Ctrl+C) | command | Edit menu | Copies merged visible contents of selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/copy-and-paste-selections.html |
| PS-A-0536 | Cut (Ctrl+X) | command | Edit menu | Cuts selection to clipboard | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/delete-or-cut-selected-pixels.html |
| PS-A-0537 | Delete selected pixels | command | Edit > Clear | Deletes selected pixels to transparency or background color | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/delete-or-cut-selected-pixels.html |
| PS-A-0538 | Delete and Fill Selection | command | Edit menu | Removes selected object and fills with content-aware fill in one step | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/remove-objects-with-delete-and-fill-selection.html |
| PS-A-0539 | Paste in Place | command | Edit > Paste Special | Pastes at original coordinates | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/paste-one-selection-into-or-outside-another.html |
| PS-A-0540 | Paste Into | command | Edit > Paste Special | Pastes into selection as new layer with layer mask | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/paste-one-selection-into-or-outside-another.html |
| PS-A-0541 | Paste Outside | command | Edit > Paste Special | Pastes with inverse mask of selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/paste-one-selection-into-or-outside-another.html |
| PS-A-0542 | Paste without formatting | command | Edit > Paste Special | Pastes text without its styling | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/copy-and-paste-selections.html |
| PS-A-0543 | Selection to generative editing | behavior | Contextual Task Bar | Selection defines area for generative fill or prompt edits | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/use-selections-for-generative-editing.html |
| PS-A-0544 | Selection Contextual Task Bar actions | behavior | Contextual Task Bar | Offers Select and Mask, Modify, Invert, Create mask, Fill, Generative Fill after selecting | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-0545 | Defringe | command | Layer > Matting | Replaces fringe pixel colors with nearby pure colors | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/decrease-fringe-on-selection.html |
| PS-A-0546 | Color Decontaminate (Matting) | command | Layer > Matting | Removes color fringe of cut out layers | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/remove-matte-from-selection.html |
| PS-A-0547 | Remove Black Matte | command | Layer > Matting | Removes black edge halo from anti-aliased layers | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/remove-matte-from-selection.html |
| PS-A-0548 | Remove White Matte | command | Layer > Matting | Removes white edge halo from anti-aliased layers | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/remove-matte-from-selection.html |

## B03 Select and Mask workspace

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0549 | Select and Mask workspace | panel | Select > Select and Mask | Dedicated workspace for refining selections and masks | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0550 | Quick Selection tool (in Select and Mask) | tool | Select and Mask toolbar | Paint to build selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0551 | Refine Edge Brush tool | tool | Select and Mask toolbar | Paints areas for edge refinement such as hair | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0552 | Brush tool (in Select and Mask) | tool | Select and Mask toolbar | Paints to add or subtract hard selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0553 | Object Selection tool (in Select and Mask) | tool | Select and Mask toolbar | Draws around objects to add | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0554 | Lasso and Polygonal Lasso (in Select and Mask) | tool | Select and Mask toolbar | Freehand or polygonal selection editing | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0555 | Hand and Zoom (in Select and Mask) | tool | Select and Mask toolbar | Navigation | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0556 | View Mode Onion Skin (O) | panel-option | Properties | Transparency-based onion skin view | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0557 | View Mode Marching Ants (M) | panel-option | Properties | Standard ants view | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0558 | View Mode Overlay (V) | panel-option | Properties | Quick Mask style colored overlay | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0559 | View Mode On Black (A) | panel-option | Properties | Selection over black | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0560 | View Mode On White (T) | panel-option | Properties | Selection over white | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0561 | View Mode Black and White (K) | panel-option | Properties | Mask as grayscale | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0562 | View Mode On Layers (Y) | panel-option | Properties | Selection over underlying layers | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0563 | Show Edge (J) | panel-option | Properties | Displays refinement area | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0564 | Show Original (P) | panel-option | Properties | Shows original selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0565 | Real-time Refinement | panel-option | Properties | Renders refinements live | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0566 | High Quality Preview | panel-option | Properties | Accurate preview rendering | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0567 | Transparency / Opacity slider | panel-option | Properties | Opacity of view mode background | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0568 | Overlay color and indicates masked or selected | panel-option | Properties | Settings for Overlay view mode | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0569 | Refine Mode Color Aware | panel-option | Properties | Refinement for simple or contrasting backgrounds | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0570 | Refine Mode Object Aware | panel-option | Properties | Refinement for hair or fur on complex backgrounds | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0571 | Select Subject button (Select and Mask) | panel-option | Properties | Runs Select Subject inside workspace | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0572 | Refine Hair | panel-option | Properties | Automatically detects and refines hair | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0573 | Edge Detection Radius | panel-option | Properties | Width of refinement border area | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0574 | Smart Radius | panel-option | Properties | Variable width refinement area adapting to edges | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0575 | Global Refinements Smooth | panel-option | Properties | Reduces irregular edge | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0576 | Global Refinements Feather | panel-option | Properties | Blurs selection edge | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0577 | Global Refinements Contrast | panel-option | Properties | Sharpens soft edge transitions | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0578 | Global Refinements Shift Edge | panel-option | Properties | Moves edge inward or outward by percent | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0579 | Clear Selection button | panel-option | Properties | Clears selection in workspace | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0580 | Invert button | panel-option | Properties | Inverts selection in workspace | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0581 | Decontaminate Colors | panel-option | Output Settings | Replaces color fringe with nearby fully selected colors | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0582 | Decontaminate Amount | panel-option | Output Settings | Strength of decontamination | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0583 | Output To Selection | panel-option | Output Settings | Outputs refined selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0584 | Output To Layer Mask | panel-option | Output Settings | Outputs mask on current layer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0585 | Output To New Layer | panel-option | Output Settings | Outputs selected pixels to new layer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0586 | Output To New Layer with Layer Mask | panel-option | Output Settings | Duplicate layer with mask | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0587 | Output To New Document | panel-option | Output Settings | Selected pixels to new document | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0588 | Output To New Document with Layer Mask | panel-option | Output Settings | New document with masked layer | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0589 | Remember Settings | panel-option | Properties | Reuses settings next time | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0590 | Presets (Select and Mask) | panel-option | Properties | Save and load refinement presets | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0591 | Brush modes Add and Subtract | tool-option | Select and Mask options bar | Add or subtract for refine tools | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0592 | Sample All Layers (Select and Mask) | tool-option | Select and Mask options bar | Uses composite for refinement | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-your-selection-and-mask.html |
| PS-A-0593 | Processing mode Device / Cloud | panel-option | Properties | Local or cloud computation for Select Subject and Refine Hair | ai | https://helpx.adobe.com/photoshop/desktop/make-selections/automatic-color-based-selections/improved-select-subject-and-remove-background-results.html |
| PS-A-0594 | Restore Refine Edge dialog | behavior | Preferences > Tools | Shift-click Select and Mask opens legacy Refine Edge | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/refine-and-soften-selection-edges.html |

## B04 Color Range dialog

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0595 | Select Sampled Colors | dialog-option | Color Range dialog | Selects colors sampled with eyedroppers | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0596 | Select preset colors (Reds, Yellows, Greens, Cyans, Blues, Magentas) | dialog-option | Color Range dialog | Selects by hue family | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0597 | Select Highlights / Midtones / Shadows | dialog-option | Color Range dialog | Selects by tonal range with Range sliders | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0598 | Select Skin Tones | dialog-option | Color Range dialog | Selects skin colors; Detect Faces option | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0599 | Detect Faces | dialog-option | Color Range dialog | Improves skin selection by face detection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0600 | Select Out Of Gamut | dialog-option | Color Range dialog | Selects colors not printable in CMYK | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0601 | Localized Color Clusters | dialog-option | Color Range dialog | Uses distance from sample points to limit selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0602 | Fuzziness | dialog-option | Color Range dialog | Tolerance of color range | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0603 | Range (localized) | dialog-option | Color Range dialog | Distance limit for localized clusters | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0604 | Add and Subtract eyedroppers | dialog-option | Color Range dialog | Add or remove sampled colors | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0605 | Selection / Image preview | dialog-option | Color Range dialog | Preview thumbnail as mask or image | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0606 | Selection Preview None / Grayscale / Black Matte / White Matte / Quick Mask | dialog-option | Color Range dialog | Document window preview mode | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0607 | Invert (Color Range) | dialog-option | Color Range dialog | Inverts the resulting selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/select-a-color-range-in-photoshop.html |
| PS-A-0608 | Save / Load Color Range | dialog-option | Color Range dialog | Saves settings including skin tone presets | core | https://helpx.adobe.com/photoshop/desktop/make-selections/freehand-selections/save-skin-tones-settings-as-a-preset.html |

## B05 Focus Area dialog

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0609 | View mode (Focus Area) | dialog-option | Focus Area dialog | Preview modes as in Select and Mask | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0610 | In-Focus Range Parameters | dialog-option | Focus Area dialog | Broadens or narrows in-focus range; Auto option | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0611 | Advanced Image Noise Level | dialog-option | Focus Area dialog | Compensates for noise in focus detection; Auto option | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0612 | Focus Area Add and Subtract brush | dialog-option | Focus Area dialog | Paint to add or remove areas | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0613 | Focus Area Soften Edge | dialog-option | Focus Area dialog | Softens edges of selection | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0614 | Focus Area Output To | dialog-option | Focus Area dialog | Selection, layer mask, new layer, new layer with mask, new document options | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |
| PS-A-0615 | Focus Area Select and Mask button | dialog-option | Focus Area dialog | Sends result to Select and Mask | core | https://helpx.adobe.com/photoshop/desktop/make-selections/get-started-selections/selection-tools-overview.html |

## B06 Quick Mask and channel selections

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0616 | Quick Mask mode | behavior | Toolbar | Paints selection as temporary red overlay channel | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0617 | Quick Mask Options Color Indicates Masked Areas / Selected Areas | dialog-option | Double-click Quick Mask button | Which area overlay tints | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0618 | Quick Mask Options color and opacity | dialog-option | Double-click Quick Mask button | Overlay color and opacity | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0619 | Paint to edit Quick Mask | behavior | Canvas | Black adds mask, white removes, gray partial selection | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-0620 | Ctrl-click channel thumbnail to load | behavior | Channels panel | Loads channel as selection; Shift, Alt, Shift+Alt combine | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-0621 | Ctrl-click layer thumbnail to load transparency | behavior | Layers panel | Loads layer transparency as selection with modifier combinations | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0622 | Load luminosity (Ctrl+Alt+2) | behavior | Keyboard | Loads composite luminosity as selection | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-0623 | Selection from type layer | behavior | Layers panel | Ctrl-click type layer creates selection from glyph outlines | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/create-text-selection-borders.html |
| PS-A-0624 | Selection from path | behavior | Paths panel | Ctrl-click path thumbnail loads it as selection | core | https://helpx.adobe.com/photoshop/using/converting-paths-selection-borders.html |

## C01 Layer menu commands

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0625 | New > Layer (Shift+Ctrl+N) | command | Layer menu | Creates new pixel layer via New Layer dialog | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0626 | New Layer dialog Name, Color, Mode, Opacity | dialog-option | New Layer dialog | Layer name, color label, blend mode, opacity | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0627 | Use Previous Layer to Create Clipping Mask | dialog-option | New Layer dialog | Clips new layer to the layer below | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0628 | Fill with mode-neutral color | dialog-option | New Layer dialog | Fills with neutral color (for example 50 percent gray for Overlay) | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0629 | New > Background from Layer | command | Layer menu | Converts layer to locked Background layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/convert-background-and-regular-layers.html |
| PS-A-0630 | New > Layer from Background | command | Layer menu | Converts Background into normal layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/convert-background-and-regular-layers.html |
| PS-A-0631 | New > Group | command | Layer menu | Creates empty layer group | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/organize-layers-with-layer-groups.html |
| PS-A-0632 | New > Group from Layers | command | Layer menu | Groups selected layers (Ctrl+G) | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/group-and-ungroup-layers.html |
| PS-A-0633 | New > Artboard | command | Layer menu | Creates new artboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/add-artboards-current-document.html |
| PS-A-0634 | New > Artboard from Group | command | Layer menu | Converts group into artboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/add-artboards-current-document.html |
| PS-A-0635 | New > Artboard from Layers | command | Layer menu | Creates artboard containing selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/add-artboards-current-document.html |
| PS-A-0636 | New > Frame from Layers | command | Layer menu | Converts layers into frame | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/convert-to-frame.html |
| PS-A-0637 | Convert to Frame | command | Layer menu | Converts selected layer into frame | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/convert-to-frame.html |
| PS-A-0638 | New > Layer via Copy (Ctrl+J) | command | Layer menu | Copies selection or layer into new layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0639 | New > Layer via Cut (Shift+Ctrl+J) | command | Layer menu | Cuts selection into new layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0640 | Copy CSS | command | Layer menu | Copies CSS properties of shape or text layers | format | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0641 | Copy SVG | command | Layer menu | Copies SVG code of shape layer | format | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0642 | Duplicate Layer | command | Layer menu | Duplicates layer to same or other document | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/duplicate-layers.html |
| PS-A-0643 | Duplicate Layer destination document | dialog-option | Duplicate Layer dialog | Target document including New with name | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/create-document-from-layer-or-group.html |
| PS-A-0644 | Delete > Layer | command | Layer menu | Deletes selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0645 | Delete > Hidden Layers | command | Layer menu | Deletes all hidden layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/clean-up-layers.html |
| PS-A-0646 | Delete > Empty Layers | command | Layer menu | Deletes layers with no pixels | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/clean-up-layers.html |
| PS-A-0647 | Quick Export as PNG | command | Layer menu | Exports selected layer quickly | format | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0648 | Export As (layers) | command | Layer menu | Exports selected layers with settings | format | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0649 | Rename Layer | command | Layer menu | Renames the selected layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0650 | Layer Properties | command | Layer menu | Dialog for layer name and color label | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0651 | Layer Style submenu | command | Layer menu | Blending Options, individual effects, Copy, Paste, Clear, Global Light, Create Layers, Hide All Effects, Scale Effects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/add-layer-styles.html |
| PS-A-0652 | Smart Filter submenu | command | Layer menu | Disable, Delete Filter Mask, Enable, Clear Smart Filters | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-A-0653 | New Fill Layer > Solid Color / Gradient / Pattern | command | Layer menu | Adds live fill layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/create-fill-layers.html |
| PS-A-0654 | New Adjustment Layer submenu | command | Layer menu | Adds any adjustment as a layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/create-adjustment-layers.html |
| PS-A-0655 | Layer Content Options | command | Layer menu | Opens settings of fill or adjustment layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/change-adjustment-and-fill-layer-options.html |
| PS-A-0656 | Layer Mask > Reveal All / Hide All / Reveal Selection / Hide Selection / From Transparency | command | Layer menu | Adds layer mask of chosen type | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0657 | Layer Mask > Delete / Apply / Enable or Disable / Link or Unlink | command | Layer menu | Mask management commands | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/apply-or-delete-layer-masks.html |
| PS-A-0658 | Vector Mask > Reveal All / Hide All / Current Path | command | Layer menu | Adds vector mask | core | https://helpx.adobe.com/photoshop/using/masking-layers-vector-masks.html |
| PS-A-0659 | Vector Mask > Delete / Enable or Disable / Link or Unlink | command | Layer menu | Vector mask management | core | https://helpx.adobe.com/photoshop/using/masking-layers-vector-masks.html |
| PS-A-0660 | Create Clipping Mask (Alt+Ctrl+G) | command | Layer menu | Clips layer to layer below | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0661 | Release Clipping Mask | command | Layer menu | Unclips layer | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0662 | Mask All Objects | command | Layer menu | Generates masks for all detected objects | ai | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/create-layer-masks-for-all-detected-objects-in-a-layer.html |
| PS-A-0663 | Smart Objects submenu | command | Layer menu | Convert, New via Copy, Reveal in Explorer, Update Modified, Update All, Resolve Broken Link, Relink, Edit Contents, Export Contents, Embed, Convert to Linked, Convert to Layers, Package, Replace Contents, Reset Transform, Stack Mode, Rasterize | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0664 | Video Layers submenu | command | Layer menu | New video layer from file and related video layer commands | video | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0665 | Rasterize submenu | command | Layer menu | Type, Shape, Fill Content, Vector Mask, Smart Object, Video, Layer, All Layers, Layer Style | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/rasterize-smart-objects.html |
| PS-A-0666 | New Layer Based Slice | command | Layer menu | Slice from layer bounds | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-0667 | Group Layers (Ctrl+G) | command | Layer menu | Groups selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/group-and-ungroup-layers.html |
| PS-A-0668 | Ungroup Layers (Shift+Ctrl+G) | command | Layer menu | Removes group keeping layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/group-and-ungroup-layers.html |
| PS-A-0669 | Hide Layers (Ctrl+,) | command | Layer menu | Toggles visibility of selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0670 | Arrange > Bring to Front / Forward / Send Backward / to Back / Reverse | command | Layer menu | Changes stacking order | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0671 | Combine Shapes submenu | command | Layer menu | Unite, Subtract Front, Unite at Overlap, Subtract at Overlap on shape layers | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0672 | Align submenu | command | Layer menu | Top, Vertical Centers, Bottom, Left, Horizontal Centers, Right edges | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0673 | Distribute submenu | command | Layer menu | Distribute edges, centers, and spacing | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/distribute-layers-groups-evenly.html |
| PS-A-0674 | Lock Layers | command | Layer menu | Lock options dialog for selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0675 | Link Layers | command | Layer menu | Links selected layers to move together | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/link-and-unlink-layers.html |
| PS-A-0676 | Select Linked Layers | command | Layer menu | Selects all layers linked to current | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/link-and-unlink-layers.html |
| PS-A-0677 | Merge Down / Merge Layers (Ctrl+E) | command | Layer menu | Merges selected or next layer below | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0678 | Merge Visible (Shift+Ctrl+E) | command | Layer menu | Merges all visible layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0679 | Stamp Visible (Shift+Ctrl+Alt+E) | behavior | Keyboard | Creates new merged layer of visible content keeping originals | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0680 | Stamp selected layers (Ctrl+Alt+E) | behavior | Keyboard | Merges copies of selected layers into new layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0681 | Flatten Image | command | Layer menu | Flattens all layers into Background, discarding hidden layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0682 | Matting submenu | command | Layer menu | Color Decontaminate, Defringe, Remove Black Matte, Remove White Matte | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/decrease-fringe-on-selection.html |

## C02 Layer types

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0683 | Background layer | behavior | Layers panel | Locked bottom opaque layer without transparency | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/convert-background-and-regular-layers.html |
| PS-A-0684 | Pixel layer | behavior | Layers panel | Raster layer with transparency | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0685 | Adjustment layer | behavior | Layers panel | Non-destructive adjustment applying to layers below | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-and-fill-layers-overview.html |
| PS-A-0686 | Fill layer Solid Color | behavior | Layers panel | Live solid color fill | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/create-fill-layers.html |
| PS-A-0687 | Fill layer Gradient | behavior | Layers panel | Live gradient fill with style, angle, scale, reverse, dither, align with layer, method | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/create-fill-layers.html |
| PS-A-0688 | Fill layer Pattern | behavior | Layers panel | Live pattern fill with angle, scale, snap to origin, link with layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/create-fill-layers.html |
| PS-A-0689 | Type layer | behavior | Layers panel | Editable vector text | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-0690 | Shape layer | behavior | Layers panel | Vector shape with fill and stroke properties | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-0691 | Smart Object layer | behavior | Layers panel | Container preserving source content for non-destructive transforms and filters | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0692 | Video layer | behavior | Layers panel | Layer containing video frames | video | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/layers-overview.html |
| PS-A-0693 | Frame layer | behavior | Layers panel | Placeholder frame masking placed content | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/draw-frames.html |
| PS-A-0694 | Artboard | behavior | Layers panel | Special group acting as independent canvas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0695 | Layer group | behavior | Layers panel | Folder containing layers with its own blend mode, opacity, mask | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/organize-layers-with-layer-groups.html |
| PS-A-0696 | Pass Through group blend mode | blend-mode | Layers panel | Group default letting layer blends inside interact with layers below | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/organize-layers-with-layer-groups.html |
| PS-A-0697 | Dynamic (Live filter) layer | behavior | Layers panel | Live filter layer applying filters non-destructively in the stack | core | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-A-0698 | Generative layer | behavior | Layers panel | Layer holding generated variations with prompt stored in Properties | ai | https://helpx.adobe.com/photoshop/desktop/create-open-import-images/create-images/edit-images-with-generative-fill.html |

## C03 Smart Objects

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0699 | Convert to Smart Object | command | Layer > Smart Objects | Wraps selected layers in an embedded smart object | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/create-embedded-smart-objects.html |
| PS-A-0700 | New Smart Object via Copy | command | Layer > Smart Objects | Creates independent copy not sharing contents | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/duplicate-an-embedded-smart-object.html |
| PS-A-0701 | Place Embedded | command | File menu | Places file as embedded smart object | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/create-embedded-smart-objects.html |
| PS-A-0702 | Place Linked | command | File menu | Places file as linked smart object referencing external file | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/create-linked-smart-objects.html |
| PS-A-0703 | Edit Contents | command | Layer > Smart Objects | Opens smart object contents as a .psb for editing | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/edit-the-contents-of-a-smart-object.html |
| PS-A-0704 | Update Modified Content | command | Layer > Smart Objects | Refreshes linked smart objects changed on disk | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/update-linked-smart-objects.html |
| PS-A-0705 | Update All Modified Content | command | Layer > Smart Objects | Refreshes all modified linked smart objects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/update-linked-smart-objects.html |
| PS-A-0706 | Resolve Broken Link | command | Layer > Smart Objects | Locates missing linked file | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/update-linked-smart-objects.html |
| PS-A-0707 | Relink to File / Relink to Library Graphic | command | Layer > Smart Objects | Points linked smart object to new source | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/update-linked-smart-objects.html |
| PS-A-0708 | Reveal in Explorer | command | Layer > Smart Objects | Shows linked source file on disk | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/view-linked-smart-object-properties.html |
| PS-A-0709 | Export Contents | command | Layer > Smart Objects | Saves embedded contents to file | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/export-the-contents-of-an-embedded-smart-object.html |
| PS-A-0710 | Embed Linked | command | Layer > Smart Objects | Embeds a linked smart object | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/embed-linked-smart-objects.html |
| PS-A-0711 | Embed All Linked | command | Layer > Smart Objects | Embeds all linked smart objects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/embed-linked-smart-objects.html |
| PS-A-0712 | Convert to Linked | command | Layer > Smart Objects | Converts embedded smart object to linked file | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/convert-embedded-smart-objects-to-linked.html |
| PS-A-0713 | Package | command | File > Package | Collects linked files into a folder with document | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/package-linked-smart-objects.html |
| PS-A-0714 | Convert to Layers | command | Layer > Smart Objects | Unpacks smart object contents to layers in a group | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/convert-smart-objects-to-layers.html |
| PS-A-0715 | Replace Contents | command | Layer > Smart Objects | Replaces source content keeping transforms and filters | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/replace-the-contents-of-a-smart-object.html |
| PS-A-0716 | Reset Transform | command | Layer > Smart Objects | Restores original smart object transform | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/reset-smart-object-transforms.html |
| PS-A-0717 | Rasterize Smart Object | command | Layer > Smart Objects | Converts smart object to pixel layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/rasterize-smart-objects.html |
| PS-A-0718 | Stack Mode Entropy | command | Layer > Smart Objects > Stack Mode | Statistic per pixel across stacked layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0719 | Stack Mode Kurtosis | command | Layer > Smart Objects > Stack Mode | Statistic per pixel across stacked layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0720 | Stack Mode Maximum | command | Layer > Smart Objects > Stack Mode | Maximum value per channel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0721 | Stack Mode Mean | command | Layer > Smart Objects > Stack Mode | Average value for noise reduction | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0722 | Stack Mode Median | command | Layer > Smart Objects > Stack Mode | Median value to remove transient objects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0723 | Stack Mode Minimum | command | Layer > Smart Objects > Stack Mode | Minimum value per channel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0724 | Stack Mode Range | command | Layer > Smart Objects > Stack Mode | Max minus min | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0725 | Stack Mode Skewness | command | Layer > Smart Objects > Stack Mode | Symmetry statistic | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0726 | Stack Mode Standard Deviation | command | Layer > Smart Objects > Stack Mode | Standard deviation per pixel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0727 | Stack Mode Summation | command | Layer > Smart Objects > Stack Mode | Sum of values | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0728 | Stack Mode Variance | command | Layer > Smart Objects > Stack Mode | Variance per pixel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0729 | Stack Mode None | command | Layer > Smart Objects > Stack Mode | Removes stack mode | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-0730 | Smart Object Properties panel | panel-option | Properties panel | Shows W, H, X, Y, source file path, Edit Contents, Embed, Convert to Layers, layer comp selection | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/view-linked-smart-object-properties.html |
| PS-A-0731 | Smart Object layer comp selection | panel-option | Properties panel | Chooses which layer comp of the embedded document is displayed | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0732 | Smart Filters | behavior | Layers panel | Filters applied to smart objects remain editable with mask, blending, visibility | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-A-0733 | Smart Filter Blending Options | dialog-option | Double-click smart filter icon | Mode and opacity per smart filter | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-A-0734 | Filter layers panel by Smart Object type | panel-option | Layers panel filter | Filters for linked, embedded, library, modified, missing | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/filter-the-layers-panel-by-smart-objects.html |
| PS-A-0735 | Linked smart object status badges | behavior | Layers panel | Icons for out-of-date and missing linked content | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/update-linked-smart-objects.html |
| PS-A-0736 | Creative Cloud Library linked graphic | behavior | Layers panel | Smart objects linked to CC Libraries that update automatically | cloud | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/create-linked-smart-objects.html |

## C04 Masks and clipping

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0737 | Add layer mask button | command | Layers panel | Adds reveal-all or reveal-selection mask to layer | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0738 | Alt-click add mask | behavior | Layers panel | Adds hide-all or hide-selection mask | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0739 | Add vector mask (second click) | behavior | Layers panel | Clicking Add Mask again on masked layer adds vector mask | core | https://helpx.adobe.com/photoshop/using/masking-layers-vector-masks.html |
| PS-A-0740 | Layer mask link toggle | behavior | Layers panel | Chain between thumbnail and mask controls whether they move together | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/unlink-layers-and-masks.html |
| PS-A-0741 | Shift-click disable mask | behavior | Layers panel | Shift-click mask thumbnail toggles mask on or off | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/disable-or-enable-layer-masks.html |
| PS-A-0742 | Alt-click view mask | behavior | Layers panel | Alt-click mask thumbnail displays mask in grayscale | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0743 | Shift+Alt-click rubylith | behavior | Layers panel | Displays mask as red overlay | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0744 | Backslash toggle mask overlay | behavior | Keyboard | Shows mask as rubylith overlay | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0745 | Drag mask to other layer | behavior | Layers panel | Moves mask; Alt-drag copies mask | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0746 | Right-click mask menu | behavior | Layers panel | Disable, Delete, Apply, Add to selection, Subtract, Intersect, Select and Mask, Mask options | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/apply-or-delete-layer-masks.html |
| PS-A-0747 | Mask Options overlay color | dialog-option | Mask Options dialog | Color and opacity of mask overlay display | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0748 | Masks Properties Density | panel-option | Properties > Masks | Reduces mask opacity non-destructively | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0749 | Masks Properties Feather | panel-option | Properties > Masks | Non-destructive mask edge feather | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0750 | Masks Properties Select and Mask | panel-option | Properties > Masks | Refines mask in Select and Mask | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0751 | Masks Properties Color Range | panel-option | Properties > Masks | Builds mask from Color Range | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0752 | Masks Properties Invert | panel-option | Properties > Masks | Inverts mask | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0753 | Masks Properties buttons Load as Selection / Apply / Disable / Delete | panel-option | Properties > Masks | Mask utility actions | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-0754 | Masks Properties select pixel mask or vector mask | panel-option | Properties > Masks | Switches between pixel and vector mask | core | https://helpx.adobe.com/photoshop/using/masking-layers-vector-masks.html |
| PS-A-0755 | Vector mask | behavior | Layers panel | Resolution-independent path mask on any layer | core | https://helpx.adobe.com/photoshop/using/masking-layers-vector-masks.html |
| PS-A-0756 | Clipping mask via Alt-click | behavior | Layers panel | Alt-click line between layers creates clipping mask | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0757 | Clipping mask with multiple layers | behavior | Layers panel | Several consecutive layers can clip to a base layer | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0758 | Filter mask | behavior | Layers panel | Mask on smart filters controlling filter visibility | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |

## C05 Layers panel

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0759 | Layers panel | panel | Window > Layers (F7) | Lists layers with thumbnails, visibility, blend controls | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0760 | Blend mode menu | panel-option | Layers panel | Layer blending mode | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0761 | Opacity | panel-option | Layers panel | Overall layer opacity including effects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0762 | Fill opacity | panel-option | Layers panel | Opacity of layer pixels excluding layer effects | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0763 | Visibility eye | panel-option | Layers panel | Shows or hides layer; Alt-click solos | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0764 | Drag across eyes | behavior | Layers panel | Dragging across eye column toggles many layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0765 | Lock Transparent Pixels | panel-option | Layers panel | Restricts editing to opaque pixels | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0766 | Lock Image Pixels | panel-option | Layers panel | Prevents painting on layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0767 | Lock Position | panel-option | Layers panel | Prevents moving layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0768 | Prevent Auto-Nesting into and out of Artboards and Frames | panel-option | Layers panel | Keeps layer from auto-nesting | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0769 | Lock All | panel-option | Layers panel | Locks all properties | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0770 | Lock all layers in group | command | Layers panel menu | Applies locks to all layers in group | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0771 | Filter type Kind | panel-option | Layers panel | Filters by pixel, adjustment, type, shape, smart object | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0772 | Filter type Name | panel-option | Layers panel | Filters by name text | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0773 | Filter type Effect | panel-option | Layers panel | Filters by layer effect type | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0774 | Filter type Mode | panel-option | Layers panel | Filters by blend mode | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0775 | Filter type Attribute | panel-option | Layers panel | Filters by visible, locked, empty, linked, clipped, layer mask, vector mask, effects, advanced blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0776 | Filter type Color | panel-option | Layers panel | Filters by color label | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0777 | Filter type Smart Object | panel-option | Layers panel | Filters by smart object status | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/filter-the-layers-panel-by-smart-objects.html |
| PS-A-0778 | Filter type Selected | panel-option | Layers panel | Shows selected layers only (isolation) | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0779 | Filter type Artboard | panel-option | Layers panel | Filters by artboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0780 | Filtering on/off toggle | panel-option | Layers panel | Enables or disables layer filtering | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0781 | Layer color labels | panel-option | Layer context menu | Red, Orange, Yellow, Green, Blue, Violet, Gray labels | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0782 | Link layers button | panel-option | Layers panel | Links selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/link-and-unlink-layers.html |
| PS-A-0783 | Add layer style button | panel-option | Layers panel | Opens effects menu | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/add-layer-styles.html |
| PS-A-0784 | New fill or adjustment layer button | panel-option | Layers panel | Menu of fill and adjustment layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/create-adjustment-layers.html |
| PS-A-0785 | New group button | panel-option | Layers panel | Creates group | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0786 | New layer button | panel-option | Layers panel | Creates layer; Alt shows dialog | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0787 | Delete layer button | panel-option | Layers panel | Deletes selected layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0788 | Panel Options thumbnail size | panel-option | Layers panel menu > Panel Options | None, small, medium, large thumbnails | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0789 | Thumbnail Contents Layer Bounds / Entire Document | panel-option | Panel Options | Thumbnail cropping | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0790 | Use Default Masks on Fill Layers | panel-option | Panel Options | Adds masks automatically to fill layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0791 | Use Default Masks on Adjustments | panel-option | Panel Options | Adds masks automatically to adjustment layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0792 | Expand New Effects | panel-option | Panel Options | Expands effects list when added | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0793 | Add Copy to Copied Layers and Groups | panel-option | Panel Options | Appends copy suffix to duplicates | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0794 | Show Layer Filtering bar option | panel-option | Panel Options | Shows or hides filter row | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0795 | Layer Properties / Blending Options from context | panel-option | Layer context menu | Access layer properties and blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0796 | Collapse All Groups | command | Layers panel menu | Collapses every group | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0797 | Double-click name to rename | behavior | Layers panel | Inline renaming; Tab moves to next layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0798 | Drag to reorder | behavior | Layers panel | Drag layers to reorder or into groups | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |
| PS-A-0799 | Alt+[ and Alt+] select layers | behavior | Keyboard | Selects next or previous layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/select-layers.html |
| PS-A-0800 | Ctrl+[ and Ctrl+] move layer | behavior | Keyboard | Moves layer up or down in stack | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/select-layers.html |
| PS-A-0801 | Shift-click contiguous and Ctrl-click noncontiguous selection | behavior | Layers panel | Multi-layer selection | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/select-layers.html |
| PS-A-0802 | Select similar layers | command | Select > Similar Layers | Selects layers of same kind | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/select-layers.html |
| PS-A-0803 | Layer bounds and handles display | behavior | View > Show > Layer Edges | Shows outline of layer contents | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/display-layer-edges-and-handles.html |
| PS-A-0804 | Transparency grid settings | behavior | Preferences > Transparency and Gamut | Grid size and colors of checkerboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/change-transparency-preferences.html |
| PS-A-0805 | Sample from all visible layers | behavior | Tools | Sample All Layers options across tools | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/sample-from-all-visible-layers.html |
| PS-A-0806 | Create document from layer or group | command | Layer > Duplicate or Artboards > New Document | Moves content into new document | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/create-document-from-layer-or-group.html |
| PS-A-0807 | Export layers to files | command | File > Export > Layers to Files | Saves each layer as separate file | automation | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/get-started-layers/work-with-the-layers-panel.html |

## C06 Layer Properties / Blending Options dialog

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0808 | General Blending Mode and Opacity | dialog-option | Layer Style > Blending Options | Layer blend mode and opacity | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0809 | Advanced Blending Fill Opacity | dialog-option | Layer Style > Blending Options | Fill opacity excluding effects | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0810 | Advanced Blending Channels R G B | dialog-option | Layer Style > Blending Options | Restricts blending to selected channels | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0811 | Knockout None / Shallow / Deep | dialog-option | Layer Style > Blending Options | Punches through to group bottom or background | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0812 | Blend Interior Effects as Group | dialog-option | Layer Style > Blending Options | Applies blend mode to interior effects such as inner glow, satin, overlays | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0813 | Blend Clipped Layers as Group | dialog-option | Layer Style > Blending Options | Base layer blend mode applies to clipped layers | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0814 | Transparency Shapes Layer | dialog-option | Layer Style > Blending Options | Limits effects to opaque areas of layer | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0815 | Layer Mask Hides Effects | dialog-option | Layer Style > Blending Options | Layer mask hides effects instead of shaping them | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0816 | Vector Mask Hides Effects | dialog-option | Layer Style > Blending Options | Vector mask hides effects instead of shaping them | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0817 | Blend If channel | dialog-option | Layer Style > Blending Options | Gray or individual channel used for Blend If | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0818 | Blend If This Layer sliders | dialog-option | Layer Style > Blending Options | Range of current layer pixels that are visible | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0819 | Blend If Underlying Layer sliders | dialog-option | Layer Style > Blending Options | Range of underlying pixels that show through | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0820 | Blend If split sliders | dialog-option | Layer Style > Blending Options | Alt-drag splits slider triangles for smooth transitions | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |

## C07 Blend modes

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0821 | Normal | blend-mode | Layers panel and painting tools | Result color is the blend color | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0822 | Dissolve | blend-mode | Layers panel and painting tools | Randomly replaces pixels based on opacity | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0823 | Behind | blend-mode | Painting tools only | Paints only on transparent parts of the layer | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0824 | Clear | blend-mode | Painting tools only | Makes pixels transparent like an eraser | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0825 | Darken | blend-mode | Layers panel and painting tools | Keeps darker of base and blend per channel | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0826 | Multiply | blend-mode | Layers panel and painting tools | Multiplies base by blend giving darker result | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0827 | Color Burn | blend-mode | Layers panel and painting tools | Darkens base by increasing contrast | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0828 | Linear Burn | blend-mode | Layers panel and painting tools | Darkens base by decreasing brightness | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0829 | Darker Color | blend-mode | Layers panel and painting tools | Keeps darker of the two composite colors | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0830 | Lighten | blend-mode | Layers panel and painting tools | Keeps lighter of base and blend per channel | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0831 | Screen | blend-mode | Layers panel and painting tools | Multiplies inverse of colors giving lighter result | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0832 | Color Dodge | blend-mode | Layers panel and painting tools | Brightens base by decreasing contrast | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0833 | Linear Dodge (Add) | blend-mode | Layers panel and painting tools | Brightens base by increasing brightness | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0834 | Lighter Color | blend-mode | Layers panel and painting tools | Keeps lighter of the two composite colors | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0835 | Overlay | blend-mode | Layers panel and painting tools | Multiplies or screens depending on base color | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0836 | Soft Light | blend-mode | Layers panel and painting tools | Darkens or lightens depending on blend color like diffused light | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0837 | Hard Light | blend-mode | Layers panel and painting tools | Multiplies or screens depending on blend color like harsh light | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0838 | Vivid Light | blend-mode | Layers panel and painting tools | Burns or dodges by increasing or decreasing contrast | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0839 | Linear Light | blend-mode | Layers panel and painting tools | Burns or dodges by decreasing or increasing brightness | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0840 | Pin Light | blend-mode | Layers panel and painting tools | Replaces colors depending on blend color | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0841 | Hard Mix | blend-mode | Layers panel and painting tools | Posterizes channels to 0 or 255 based on sum | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0842 | Difference | blend-mode | Layers panel and painting tools | Subtracts darker from lighter | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0843 | Exclusion | blend-mode | Layers panel and painting tools | Lower contrast version of Difference | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0844 | Subtract | blend-mode | Layers panel and painting tools | Subtracts blend from base | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0845 | Divide | blend-mode | Layers panel and painting tools | Divides base by blend | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0846 | Hue | blend-mode | Layers panel and painting tools | Base luminance and saturation with blend hue | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0847 | Saturation | blend-mode | Layers panel and painting tools | Base luminance and hue with blend saturation | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0848 | Color | blend-mode | Layers panel and painting tools | Base luminance with blend hue and saturation | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0849 | Luminosity | blend-mode | Layers panel and painting tools | Base hue and saturation with blend luminance | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0850 | Blend mode live preview on hover | behavior | Layers panel | Hovering over a mode in the menu previews it on canvas | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0851 | Cycle blend modes (Shift+plus or minus) | behavior | Keyboard | Steps through blend modes; Shift+Alt+letter sets specific mode | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/blending-mode-descriptions.html |
| PS-A-0852 | Special eight modes Fill vs Opacity | behavior | Layers panel | Color Burn, Linear Burn, Color Dodge, Linear Dodge, Vivid Light, Linear Light, Hard Mix, Difference react differently to Fill than Opacity | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-0853 | 32-bit supported blend modes | behavior | 32 bpc documents | Subset of modes available in 32-bit mode | core | https://helpx.adobe.com/photoshop/using/bit-depth.html |

## C08 Layer styles

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0854 | Layer Style dialog | dialog-option | Layer > Layer Style | Dialog to add and edit effects with preview | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/add-layer-styles.html |
| PS-A-0855 | Styles list in dialog | dialog-option | Layer Style dialog | Pick preset styles inside Layer Style dialog | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/work-with-preset-styles.html |
| PS-A-0856 | Multiple instances of effects | dialog-option | Layer Style dialog | Plus button adds up to 10 instances of Stroke, Inner Shadow, Color, Gradient Overlay, Drop Shadow | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0857 | Reorder effect instances | dialog-option | Layer Style dialog | Up and down arrows reorder effect instances | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0858 | Show All Effects | dialog-option | Layer Style dialog | Effects list shows all or only applied effects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0859 | Make Default / Reset to Default | dialog-option | Layer Style dialog | Saves or restores default values per effect | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0860 | New Style (save preset) | dialog-option | Layer Style dialog | Saves current effects and blending options as style preset | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/work-with-preset-styles.html |
| PS-A-0861 | Preview checkbox | dialog-option | Layer Style dialog | Live preview of effects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0862 | Drop Shadow Blend Mode, Color, Opacity | layer-style | Drop Shadow | Shadow blending and color | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0863 | Drop Shadow Angle and Use Global Light | layer-style | Drop Shadow | Lighting angle, optionally shared | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/set-a-global-lighting-angle-for-all-layers.html |
| PS-A-0864 | Drop Shadow Distance | layer-style | Drop Shadow | Offset of shadow | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0865 | Drop Shadow Spread | layer-style | Drop Shadow | Expands shadow matte before blur | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0866 | Drop Shadow Size | layer-style | Drop Shadow | Blur radius of shadow | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0867 | Drop Shadow Contour and Anti-aliased | layer-style | Drop Shadow | Contour shapes falloff | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0868 | Drop Shadow Noise | layer-style | Drop Shadow | Adds noise to shadow | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0869 | Layer Knocks Out Drop Shadow | layer-style | Drop Shadow | Hides shadow under semitransparent layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0870 | Drag shadow on canvas | behavior | Drop Shadow | Dragging on canvas changes angle and distance | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0871 | Inner Shadow Blend Mode, Color, Opacity | layer-style | Inner Shadow | Shadow inside edges | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0872 | Inner Shadow Angle, Distance, Choke, Size | layer-style | Inner Shadow | Geometry of inner shadow | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0873 | Inner Shadow Contour, Anti-aliased, Noise | layer-style | Inner Shadow | Falloff shape and noise | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0874 | Outer Glow Blend Mode, Opacity, Noise | layer-style | Outer Glow | Glow blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0875 | Outer Glow Color or Gradient | layer-style | Outer Glow | Solid color or gradient glow | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0876 | Outer Glow Technique Softer / Precise | layer-style | Outer Glow | Glow edge technique | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0877 | Outer Glow Spread and Size | layer-style | Outer Glow | Glow extent | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0878 | Outer Glow Contour, Anti-aliased, Range, Jitter | layer-style | Outer Glow | Quality controls for glow | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0879 | Inner Glow Blend Mode, Opacity, Noise, Color or Gradient | layer-style | Inner Glow | Glow inside edges | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0880 | Inner Glow Technique Softer / Precise | layer-style | Inner Glow | Glow technique | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0881 | Inner Glow Source Center / Edge | layer-style | Inner Glow | Glow emanates from center or edge | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0882 | Inner Glow Choke and Size | layer-style | Inner Glow | Glow extent | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0883 | Inner Glow Contour, Anti-aliased, Range, Jitter | layer-style | Inner Glow | Quality controls | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0884 | Bevel and Emboss Style | layer-style | Bevel and Emboss | Outer Bevel, Inner Bevel, Emboss, Pillow Emboss, Stroke Emboss | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0885 | Bevel and Emboss Technique | layer-style | Bevel and Emboss | Smooth, Chisel Hard, Chisel Soft | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0886 | Bevel and Emboss Depth | layer-style | Bevel and Emboss | Depth of bevel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0887 | Bevel and Emboss Direction Up / Down | layer-style | Bevel and Emboss | Raised or sunken look | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0888 | Bevel and Emboss Size and Soften | layer-style | Bevel and Emboss | Size and blur of bevel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0889 | Bevel and Emboss Shading Angle and Altitude | layer-style | Bevel and Emboss | Light source direction and height, Use Global Light | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/set-a-global-lighting-angle-for-all-layers.html |
| PS-A-0890 | Gloss Contour and Anti-aliased | layer-style | Bevel and Emboss | Glossy metallic look | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0891 | Highlight Mode, color, Opacity | layer-style | Bevel and Emboss | Highlight blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0892 | Shadow Mode, color, Opacity | layer-style | Bevel and Emboss | Shadow blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0893 | Bevel Contour sub-effect | layer-style | Bevel and Emboss > Contour | Shapes ridges and valleys with Contour and Range | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0894 | Bevel Texture sub-effect | layer-style | Bevel and Emboss > Texture | Pattern texture with Scale, Depth, Invert, Link with Layer, Snap to Origin | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0895 | Satin Blend Mode, Color, Opacity | layer-style | Satin | Interior satin shading | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0896 | Satin Angle, Distance, Size | layer-style | Satin | Satin geometry | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0897 | Satin Contour, Anti-aliased, Invert | layer-style | Satin | Satin shape controls | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0898 | Color Overlay Blend Mode, Color, Opacity | layer-style | Color Overlay | Fills layer with color | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0899 | Gradient Overlay Blend Mode, Opacity, Dither | layer-style | Gradient Overlay | Gradient blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0900 | Gradient Overlay Gradient and Reverse | layer-style | Gradient Overlay | Gradient choice | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0901 | Gradient Overlay Style | layer-style | Gradient Overlay | Linear, Radial, Angle, Reflected, Diamond | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0902 | Gradient Overlay Align with Layer | layer-style | Gradient Overlay | Uses layer bounds for gradient | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0903 | Gradient Overlay Angle, Scale, Reset Alignment | layer-style | Gradient Overlay | Geometry; drag on canvas repositions | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0904 | Gradient Overlay Method | layer-style | Gradient Overlay | Perceptual, Linear, Classic, Smooth, Stripes interpolation | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0905 | Pattern Overlay Blend Mode, Opacity | layer-style | Pattern Overlay | Pattern blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0906 | Pattern Overlay Pattern, Angle, Scale | layer-style | Pattern Overlay | Pattern choice, rotation and scale | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0907 | Pattern Overlay Link with Layer and Snap to Origin | layer-style | Pattern Overlay | Pattern anchoring | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0908 | Stroke Size | layer-style | Stroke | Stroke width | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0909 | Stroke Position Outside / Inside / Center | layer-style | Stroke | Stroke placement | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0910 | Stroke Blend Mode and Opacity | layer-style | Stroke | Stroke blending | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0911 | Stroke Overprint | layer-style | Stroke | Blends stroke with fill using overprint | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0912 | Stroke Fill Type Color / Gradient / Pattern | layer-style | Stroke | Stroke fill with gradient style Shape Burst option | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/layer-style-effects-and-options-overview.html |
| PS-A-0913 | Contour editor | dialog-option | Contour picker | Edit contour curve points, corner, preset save and load | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/manage-contours.html |
| PS-A-0914 | Contour presets | dialog-option | Contour picker | Linear, Cone, Cove, Gaussian, Half Round, Ring, Rolling Slope, Sawtooth and more | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/manage-contours.html |
| PS-A-0915 | Global Light | command | Layer > Layer Style > Global Light | Document-wide angle and altitude shared by effects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/set-a-global-lighting-angle-for-all-layers.html |
| PS-A-0916 | Copy Layer Style / Paste Layer Style | command | Layer > Layer Style | Copies effects to other layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/copy-and-paste-layer-styles.html |
| PS-A-0917 | Alt-drag fx to copy effects | behavior | Layers panel | Duplicates effects onto another layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/copy-and-paste-layer-styles.html |
| PS-A-0918 | Clear Layer Style | command | Layer > Layer Style | Removes all effects | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/remove-layer-effects.html |
| PS-A-0919 | Hide All Effects / Show All Effects | command | Layer > Layer Style | Toggles effect visibility | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/display-or-hide-layer-styles.html |
| PS-A-0920 | Scale Effects | command | Layer > Layer Style | Scales effects by percent | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/scale-layer-effects.html |
| PS-A-0921 | Create Layer(s) from style | command | Layer > Layer Style | Converts effects into separate layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/convert-layer-styles-to-image-layers.html |
| PS-A-0922 | Rasterize Layer Style | command | Layer > Rasterize > Layer Style | Bakes effects into pixels | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/convert-layer-styles-to-image-layers.html |
| PS-A-0923 | Styles panel | panel | Window > Styles | Style presets in groups; apply by click | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/work-with-preset-styles.html |
| PS-A-0924 | Styles panel Import Styles / Export | panel-option | Styles panel menu | Loads and saves .asl style libraries | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/manage-preset-styles.html |
| PS-A-0925 | Styles panel Legacy Styles and More | panel-option | Styles panel menu | Restores legacy style sets | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/manage-preset-styles.html |
| PS-A-0926 | Styles panel new group and rename | panel-option | Styles panel | Organizes styles into groups | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/manage-preset-styles.html |
| PS-A-0927 | Apply style Shift-click additive | behavior | Styles panel | Shift-click adds style effects to existing ones | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/work-with-preset-styles.html |
| PS-A-0928 | Effects visibility per effect | behavior | Layers panel | Eye icons per effect under layer | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/display-or-hide-layer-styles.html |
| PS-A-0929 | Scale Styles with transforms | behavior | Image Size and Free Transform | Option to scale effects when resizing | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/scale-layer-effects.html |

## C09 Layer comps

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0930 | Layer Comps panel | panel | Window > Layer Comps | Stores snapshots of layer visibility, position, appearance | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0931 | New Layer Comp | command | Layer Comps panel | Creates comp with Visibility, Position, Appearance (Layer Style), Selection for Artboards options | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0932 | Layer comp Comment | dialog-option | New Layer Comp dialog | Text comment stored with comp | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0933 | Apply layer comp | command | Layer Comps panel | Applies comp state to document | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0934 | Previous / Next comp | command | Layer Comps panel | Cycles through comps | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0935 | Update Layer Comp | command | Layer Comps panel | Updates with current state; Update Visibility, Position, Appearance individually | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0936 | Last Document State | command | Layer Comps panel | Restores state before applying comps | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0937 | Warning icon for invalid comps | behavior | Layer Comps panel | Shows when comp cannot be fully restored; Clear Layer Comp Warning | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0938 | Duplicate and Delete Layer Comp | command | Layer Comps panel | Manage comps | core | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0939 | Layer Comps to Files | command | File > Export > Layer Comps to Files | Exports each comp as file | automation | https://helpx.adobe.com/photoshop/using/layer-comps.html |
| PS-A-0940 | Layer comps in smart objects | behavior | Properties panel | Choose comp to display for smart object | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/view-linked-smart-object-properties.html |

## C10 Align, distribute, auto-align, auto-blend

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0941 | Align Top Edges | command | Layer > Align | Aligns top edges | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0942 | Align Vertical Centers | command | Layer > Align | Aligns vertical centers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0943 | Align Bottom Edges | command | Layer > Align | Aligns bottom edges | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0944 | Align Left Edges | command | Layer > Align | Aligns left edges | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0945 | Align Horizontal Centers | command | Layer > Align | Aligns horizontal centers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0946 | Align Right Edges | command | Layer > Align | Aligns right edges | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0947 | Align layers to selection | command | Layer > Align | Aligns to active selection bounds when present | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-content-of-layers-and-groups.html |
| PS-A-0948 | Distribute Top / Vertical Centers / Bottom / Left / Horizontal Centers / Right | command | Layer > Distribute | Evenly distributes edges or centers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/distribute-layers-groups-evenly.html |
| PS-A-0949 | Distribute Vertical Spacing / Horizontal Spacing | command | Layer > Distribute | Equal gaps between layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/distribute-layers-groups-evenly.html |
| PS-A-0950 | Auto-Align Layers | command | Edit > Auto-Align Layers | Aligns layers based on content | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-image-layers.html |
| PS-A-0951 | Auto-Align Projection Auto / Perspective / Collage / Cylindrical / Spherical / Reposition | dialog-option | Auto-Align Layers dialog | Projection model | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-image-layers.html |
| PS-A-0952 | Auto-Align Lens Correction Vignette Removal | dialog-option | Auto-Align Layers dialog | Compensates vignetting | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-image-layers.html |
| PS-A-0953 | Auto-Align Geometric Distortion | dialog-option | Auto-Align Layers dialog | Corrects lens distortion | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-image-layers.html |
| PS-A-0954 | Auto-Blend Layers | command | Edit > Auto-Blend Layers | Creates masks to blend layers | core | https://helpx.adobe.com/photoshop/desktop/create-masks/blend-images/auto-blend-layers-command-overview.html |
| PS-A-0955 | Auto-Blend Panorama | dialog-option | Auto-Blend dialog | Blends overlapping panorama layers | core | https://helpx.adobe.com/photoshop/desktop/create-masks/blend-images/auto-blend-layers-command-overview.html |
| PS-A-0956 | Auto-Blend Stack Images | dialog-option | Auto-Blend dialog | Focus stacking for extended depth of field | core | https://helpx.adobe.com/photoshop/desktop/create-masks/blend-images/create-a-composite-with-extended-depth-of-field.html |
| PS-A-0957 | Auto-Blend Seamless Tones and Colors | dialog-option | Auto-Blend dialog | Matches color and tone across seams | core | https://helpx.adobe.com/photoshop/desktop/create-masks/blend-images/auto-blend-layers-command-overview.html |
| PS-A-0958 | Auto-Blend Content Aware Fill Transparent Areas | dialog-option | Auto-Blend dialog | Fills gaps after blending | core | https://helpx.adobe.com/photoshop/desktop/create-masks/blend-images/auto-blend-layers-command-overview.html |

## C11 Artboards

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0959 | Artboard document preset | command | File > New | New document with Artboards option | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/create-artboard-documents.html |
| PS-A-0960 | Artboard Properties Size preset | panel-option | Properties panel > Artboard | Device and print presets | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-0961 | Artboard W H X Y | panel-option | Properties panel > Artboard | Size and position | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-0962 | Artboard Background Color | panel-option | Properties panel > Artboard | White, Black, Transparent, Other color | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-0963 | Artboard Clip Content | panel-option | Properties panel > Artboard | Clips layers to artboard bounds | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-0964 | Artboard Auto nesting | behavior | Canvas | Layers moved onto artboards become children | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0965 | Artboards to Files | command | File > Export > Artboards to Files | Exports each artboard | automation | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0966 | Artboards to PDF | command | File > Export > Artboards to PDF | Multi-page PDF from artboards | format | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0967 | Artboard name labels | behavior | Canvas | Name labels above artboards; double-click to rename | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-0968 | Artboard canvas color and outline | behavior | Preferences > Interface | Pasteboard color and artboard border display | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |

## D01 Adjustments panel and framework

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0969 | Adjustments panel | panel | Window > Adjustments | Buttons and presets for adding adjustment layers | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-and-fill-layers-overview.html |
| PS-A-0970 | Adjustment Presets section | panel-option | Adjustments panel | Preset groups (Portrait, Landscape, Cinematic, B and W, Creative and more) with hover preview | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-presets-overview.html |
| PS-A-0971 | Hover preview of adjustment presets | behavior | Adjustments panel | Hovering a preset previews result on canvas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-presets-overview.html |
| PS-A-0972 | Save custom adjustment preset | command | Adjustments panel | Saves stack of adjustment layers as a preset | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/create-custom-presets.html |
| PS-A-0973 | Single Adjustments section | panel-option | Adjustments panel | Icons for each adjustment type | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-and-fill-layers-overview.html |
| PS-A-0974 | Adjustment layer with Properties | behavior | Properties panel | Adjustment settings shown in Properties panel | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/work-with-adjustment-and-fill-layers.html |
| PS-A-0975 | Clip to layer button | panel-option | Properties panel | Clips adjustment to layer below | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-layers-options.html |
| PS-A-0976 | View previous state button | panel-option | Properties panel | Press and hold to compare with previous | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-layers-options.html |
| PS-A-0977 | Reset to adjustment defaults | panel-option | Properties panel | Resets settings | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-layers-options.html |
| PS-A-0978 | Toggle layer visibility button | panel-option | Properties panel | Shows or hides the adjustment | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-layers-options.html |
| PS-A-0979 | On-image adjustment tool (targeted adjustment) | panel-option | Properties panel | Drag on image to adjust in Curves, Hue/Saturation, Black and White | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-layers-options.html |
| PS-A-0980 | Adjustment presets menu per adjustment | panel-option | Properties panel | Default and saved presets per adjustment; save and load | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjustment-presets-overview.html |
| PS-A-0981 | Alt-click remembers last settings | behavior | Image > Adjustments | Alt when choosing command opens with last-used settings | core | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-A-0982 | Merge adjustment layers | behavior | Layers panel | Adjustment layers merge into layers below | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/merging-adjustment-or-fill-layers.html |
| PS-A-0983 | Adjustment layer masks target | behavior | Layers panel | Masks limit adjustment to areas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/use-layer-masks-to-target-adjustment-or-fill-layers.html |
| PS-A-0984 | Image > Adjustments direct application | behavior | Image > Adjustments | Destructive application to active pixel layer or smart filter on smart object | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |

## D02 Brightness/Contrast and Light

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0985 | Brightness/Contrast | adjustment | Image > Adjustments | Simple tonal adjustment | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-0986 | Brightness slider | dialog-option | Brightness/Contrast | Raises or lowers overall brightness | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-0987 | Contrast slider | dialog-option | Brightness/Contrast | Expands or compresses tonal range | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-0988 | Use Legacy | dialog-option | Brightness/Contrast | Linear shifting behavior of older versions | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-0989 | Auto (Brightness/Contrast) | dialog-option | Brightness/Contrast | Automatic brightness and contrast | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-0990 | Light adjustment layer | adjustment | New adjustment layer > Light | Non-destructive lighting controls | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |
| PS-A-0991 | Light Exposure | dialog-option | Light | Brightens or darkens the image | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |
| PS-A-0992 | Light Contrast | dialog-option | Light | Difference between light and dark areas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |
| PS-A-0993 | Light Highlights | dialog-option | Light | Detail in lighter areas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |
| PS-A-0994 | Light Shadows | dialog-option | Light | Detail in darker areas | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |
| PS-A-0995 | Light Whites | dialog-option | Light | Brightest tones | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |
| PS-A-0996 | Light Blacks | dialog-option | Light | Darkest tones | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |
| PS-A-0997 | Light version selector | dialog-option | Light Properties menu | Switches to legacy Brightness and Contrast controls | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-image-lighting-with-light.html |

## D03 Levels

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-0998 | Levels | adjustment | Image > Adjustments (Ctrl+L) | Sets black point, white point and gamma per channel | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-0999 | Levels Channel | dialog-option | Levels | Composite or individual channel | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1000 | Input Levels black, gray, white | dialog-option | Levels | Maps input shadow, midtone, highlight | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1001 | Output Levels | dialog-option | Levels | Limits output range | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1002 | Levels histogram | dialog-option | Levels | Histogram display in dialog | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1003 | Levels eyedroppers Black / Gray / White | dialog-option | Levels | Set points by clicking the image | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1004 | Levels Auto | dialog-option | Levels | Applies auto correction with Auto Options | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1005 | Auto Color Correction Options algorithms | dialog-option | Levels | Enhance Monochromatic Contrast, Enhance Per Channel Contrast, Find Dark and Light Colors, Enhance Brightness and Contrast | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1006 | Snap Neutral Midtones | dialog-option | Auto Color Correction Options | Neutralizes nearly neutral midtones | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1007 | Target Colors and Clipping | dialog-option | Auto Color Correction Options | Shadow, midtone, highlight targets and clip percentages; Save as defaults | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1008 | Alt clipping display | behavior | Levels | Alt-dragging black or white slider shows clipped areas | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1009 | Levels Presets | dialog-option | Levels | Default presets such as Darker, Increase Contrast, Lighten Shadows | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |

## D04 Curves

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1010 | Curves | adjustment | Image > Adjustments (Ctrl+M) | Adjusts tonal curve with up to 14 points | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1011 | Curves Channel | dialog-option | Curves | Composite or individual channel curves | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1012 | Point edit mode | dialog-option | Curves | Adds and drags curve points | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1013 | Pencil draw mode | dialog-option | Curves | Draws freeform curve | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1014 | Smooth (pencil curve) | dialog-option | Curves | Smooths a drawn curve | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1015 | Curves Input and Output fields | dialog-option | Curves | Numeric point values | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1016 | Curves eyedroppers | dialog-option | Curves | Black, gray, white point sampling | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1017 | Show Clipping | dialog-option | Curves | Displays clipping while dragging endpoints | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1018 | Curve Display Options Show Amount of Light / Pigment | dialog-option | Curves | Light 0 to 255 or pigment percentage | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1019 | Curve grid size | dialog-option | Curves | 4x4 or 10x10 grid | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1020 | Show Channel Overlays | dialog-option | Curves | Draws individual channel curves on composite | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1021 | Show Histogram | dialog-option | Curves | Histogram behind curve | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1022 | Show Baseline | dialog-option | Curves | Original diagonal line | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1023 | Show Intersection Line | dialog-option | Curves | Crosshair while dragging | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1024 | Curves Auto and Options | dialog-option | Curves | Auto correction with algorithm options | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1025 | Curves Presets | dialog-option | Curves | Color Negative, Cross Process, Darker, Increase Contrast, Lighter, Linear Contrast, Medium Contrast, Negative, Strong Contrast | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1026 | Delete curve point | behavior | Curves | Drag off graph or Ctrl-click | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |
| PS-A-1027 | Ctrl-click image to add point | behavior | Curves | Adds point for clicked tone on composite; Shift+Ctrl adds to each channel | core | https://helpx.adobe.com/photoshop/using/curves-adjustment.html |

## D05 Exposure, Vibrance, Color and vibrance

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1028 | Exposure | adjustment | Image > Adjustments | Linear exposure for HDR and other images | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1029 | Exposure slider | dialog-option | Exposure | Highlight end adjustment in stops | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1030 | Offset slider | dialog-option | Exposure | Darkens shadows and midtones | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1031 | Gamma Correction | dialog-option | Exposure | Power function for midtones | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1032 | Exposure eyedroppers | dialog-option | Exposure | Set Black, Gray, White affecting Offset and Exposure | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1033 | Vibrance | adjustment | Image > Adjustments | Saturation boosting less-saturated colors more | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1034 | Vibrance slider | dialog-option | Vibrance | Increases muted colors, protects skin tones | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1035 | Saturation slider (Vibrance) | dialog-option | Vibrance | Uniform saturation change | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1036 | Color and vibrance adjustment layer | adjustment | New adjustment layer | Temperature, Tint, Vibrance and Saturation controls | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/correct-color-balance-with-color-and-vibrance.html |
| PS-A-1037 | Temperature | dialog-option | Color and vibrance | Warmth or coolness | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/correct-color-balance-with-color-and-vibrance.html |
| PS-A-1038 | Tint | dialog-option | Color and vibrance | Green or magenta shift | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/correct-color-balance-with-color-and-vibrance.html |
| PS-A-1039 | Color and vibrance Vibrance | dialog-option | Color and vibrance | Intensity of muted colors | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/correct-color-balance-with-color-and-vibrance.html |
| PS-A-1040 | Color and vibrance Saturation | dialog-option | Color and vibrance | Overall color intensity | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/correct-color-balance-with-color-and-vibrance.html |
| PS-A-1041 | Clarity and dehaze adjustment layer | adjustment | New adjustment layer | Midtone contrast and haze removal | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-contrast-with-clarity-and-dehaze.html |
| PS-A-1042 | Clarity | dialog-option | Clarity and dehaze | Adds midtone contrast and definition | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-contrast-with-clarity-and-dehaze.html |
| PS-A-1043 | Dehaze | dialog-option | Clarity and dehaze | Reduces or adds haze | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/adjust-contrast-with-clarity-and-dehaze.html |
| PS-A-1044 | Grain adjustment layer | adjustment | New adjustment layer | Adds film-like grain non-destructively | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/enhance-texture-with-grain.html |
| PS-A-1045 | Grain Amount | dialog-option | Grain | Grain intensity | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/enhance-texture-with-grain.html |
| PS-A-1046 | Grain Size | dialog-option | Grain | Particle size | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/enhance-texture-with-grain.html |
| PS-A-1047 | Grain Roughness | dialog-option | Grain | Randomness of grain | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/enhance-texture-with-grain.html |

## D06 Hue/Saturation

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1048 | Hue/Saturation | adjustment | Image > Adjustments (Ctrl+U) | Adjusts hue, saturation, lightness globally or per color range | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1049 | Edit range Master / Reds / Yellows / Greens / Cyans / Blues / Magentas | dialog-option | Hue/Saturation | Target color range | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1050 | Hue slider | dialog-option | Hue/Saturation | Rotates hue | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1051 | Saturation slider | dialog-option | Hue/Saturation | Changes saturation | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1052 | Lightness slider | dialog-option | Hue/Saturation | Changes lightness | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1053 | Colorize | dialog-option | Hue/Saturation | Tints image with single hue | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/colorize-a-grayscale-image-or-create-a-monotone-effect.html |
| PS-A-1054 | Range sliders and color bars | dialog-option | Hue/Saturation | Adjust color range with falloff sliders | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1055 | Range eyedroppers | dialog-option | Hue/Saturation | Sample, add, subtract to define range | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1056 | Hue/Saturation targeted adjustment | dialog-option | Hue/Saturation | Drag in image to change saturation; Ctrl-drag changes hue | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |
| PS-A-1057 | Hue/Saturation presets | dialog-option | Hue/Saturation | Cyanotype, Increase Saturation, Old Style, Red Boost, Sepia, Strong Saturation, Yellow Boost | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-corrections/apply-a-hue-or-saturation-adjustment.html |

## D07 Color Balance, Black and White, Photo Filter

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1058 | Color Balance | adjustment | Image > Adjustments (Ctrl+B) | Shifts color balance by tonal range | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1059 | Color Balance sliders Cyan-Red, Magenta-Green, Yellow-Blue | dialog-option | Color Balance | Color shifts | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1060 | Tone Balance Shadows / Midtones / Highlights | dialog-option | Color Balance | Range affected | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1061 | Preserve Luminosity (Color Balance) | dialog-option | Color Balance | Keeps tonal balance | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1062 | Black and White | adjustment | Image > Adjustments | Converts to grayscale with per-color control | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/convert-a-color-image-to-black-and-white.html |
| PS-A-1063 | Black and White color sliders | dialog-option | Black and White | Reds, Yellows, Greens, Cyans, Blues, Magentas brightness | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/convert-a-color-image-to-black-and-white.html |
| PS-A-1064 | Black and White Tint | dialog-option | Black and White | Applies color tone with Hue and Saturation | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/convert-a-color-image-to-black-and-white.html |
| PS-A-1065 | Black and White Auto | dialog-option | Black and White | Automatic grayscale mix | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/convert-a-color-image-to-black-and-white.html |
| PS-A-1066 | Black and White targeted drag | dialog-option | Black and White | Drag on image to adjust color slider under pointer | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/convert-a-color-image-to-black-and-white.html |
| PS-A-1067 | Black and White presets | dialog-option | Black and White | Blue Filter, Green Filter, High Contrast, Infrared, Maximum Black, Neutral Density, Red Filter, Yellow Filter | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/convert-a-color-image-to-black-and-white.html |
| PS-A-1068 | Photo Filter | adjustment | Image > Adjustments | Simulates colored lens filter | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1069 | Photo Filter Filter preset | dialog-option | Photo Filter | Warming, Cooling, and colored filters | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1070 | Photo Filter Color | dialog-option | Photo Filter | Custom filter color | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1071 | Photo Filter Density | dialog-option | Photo Filter | Amount of color applied | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1072 | Photo Filter Preserve Luminosity | dialog-option | Photo Filter | Maintains brightness | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |

## D08 Channel Mixer and Color Lookup

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1073 | Channel Mixer | adjustment | Image > Adjustments | Mixes source channels into output channel | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1074 | Output Channel | dialog-option | Channel Mixer | Channel being built | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1075 | Source channel sliders | dialog-option | Channel Mixer | Percent contribution of each source channel (-200 to 200) | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1076 | Constant | dialog-option | Channel Mixer | Adds black or white to output channel | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1077 | Total readout | dialog-option | Channel Mixer | Shows total percentage with warning above 100 | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1078 | Monochrome | dialog-option | Channel Mixer | Creates grayscale output | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1079 | Channel Mixer presets | dialog-option | Channel Mixer | Black and White with filters, Infrared presets | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1080 | Color Lookup | adjustment | Image > Adjustments | Applies 3D LUT, abstract, or device link profiles | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1081 | 3DLUT File | dialog-option | Color Lookup | Loads .cube, .3dl, .look, .csp LUTs | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1082 | Abstract profile | dialog-option | Color Lookup | Applies abstract ICC profile | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1083 | Device Link profile | dialog-option | Color Lookup | Applies device link ICC profile | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1084 | Dither (Color Lookup) | dialog-option | Color Lookup | Dithers to reduce banding | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1085 | Data Order and Table Order | dialog-option | Color Lookup | RGB or BGR order for loaded tables | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1086 | Export Color Lookup Tables | command | File > Export > Color Lookup Tables | Exports LUT formats from adjustment stack | format | https://helpx.adobe.com/photoshop/using/color-adjustments.html |

## D09 Invert, Posterize, Threshold, Gradient Map, Selective Color

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1087 | Invert (Ctrl+I) | adjustment | Image > Adjustments | Inverts channel values | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1088 | Posterize | adjustment | Image > Adjustments | Reduces tonal levels per channel | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1089 | Posterize Levels | dialog-option | Posterize | Number of levels 2 to 255 | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1090 | Threshold | adjustment | Image > Adjustments | Converts to high-contrast black and white | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1091 | Threshold Level | dialog-option | Threshold | Cutoff level with histogram | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1092 | Gradient Map | adjustment | Image > Adjustments | Maps grayscale range to a gradient | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1093 | Gradient Map gradient | dialog-option | Gradient Map | Gradient picker and editor | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1094 | Gradient Map Dither | dialog-option | Gradient Map | Adds noise to reduce banding | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1095 | Gradient Map Reverse | dialog-option | Gradient Map | Reverses gradient | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1096 | Gradient Map Method | dialog-option | Gradient Map | Perceptual, Linear, Classic, Smooth, Stripes interpolation | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1097 | Selective Color | adjustment | Image > Adjustments | Adjusts process color amounts per color | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1098 | Selective Color Colors menu | dialog-option | Selective Color | Reds, Yellows, Greens, Cyans, Blues, Magentas, Whites, Neutrals, Blacks | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1099 | Selective Color CMYK sliders | dialog-option | Selective Color | Cyan, Magenta, Yellow, Black amounts | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1100 | Selective Color Method Relative / Absolute | dialog-option | Selective Color | Percentage of existing or absolute change | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |

## D10 Shadows/Highlights and HDR Toning

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1101 | Shadows/Highlights | adjustment | Image > Adjustments | Local tone correction lightening shadows and darkening highlights | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1102 | Shadows Amount / Tone / Radius | dialog-option | Shadows/Highlights | Shadow correction strength, tonal width, neighborhood size | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1103 | Highlights Amount / Tone / Radius | dialog-option | Shadows/Highlights | Highlight correction strength, tonal width, neighborhood size | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1104 | Adjustments Color | dialog-option | Shadows/Highlights | Saturation correction in adjusted areas | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1105 | Adjustments Midtone | dialog-option | Shadows/Highlights | Midtone contrast | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1106 | Black Clip and White Clip | dialog-option | Shadows/Highlights | Clipping percentages | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1107 | Save Defaults and Show More Options | dialog-option | Shadows/Highlights | Saves defaults and expands options | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1108 | HDR Toning | adjustment | Image > Adjustments | Tone maps HDR or flattened images; flattens layers | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1109 | HDR Toning Method | dialog-option | HDR Toning | Local Adaptation, Equalize Histogram, Exposure and Gamma, Highlight Compression | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1110 | HDR Toning Edge Glow Radius and Strength | dialog-option | HDR Toning | Local contrast halo size and strength | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1111 | HDR Toning Smooth Edges | dialog-option | HDR Toning | Reduces halos | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1112 | HDR Toning Tone and Detail Gamma, Exposure, Detail | dialog-option | HDR Toning | Global tone controls | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1113 | HDR Toning Shadow and Highlight | dialog-option | HDR Toning | Local brightness | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1114 | HDR Toning Vibrance and Saturation | dialog-option | HDR Toning | Color intensity | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1115 | HDR Toning Toning Curve and Histogram | dialog-option | HDR Toning | Curve with corner points | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1116 | HDR Toning presets | dialog-option | HDR Toning | Photorealistic, Surrealistic and other presets | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |

## D11 Desaturate, Match Color, Replace Color, Equalize

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1117 | Desaturate (Shift+Ctrl+U) | adjustment | Image > Adjustments | Removes color keeping mode | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1118 | Match Color | adjustment | Image > Adjustments | Matches color between images or layers | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1119 | Match Color Luminance | dialog-option | Match Color | Brightness of result | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1120 | Match Color Color Intensity | dialog-option | Match Color | Saturation of result | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1121 | Match Color Fade | dialog-option | Match Color | Amount of adjustment | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1122 | Match Color Neutralize | dialog-option | Match Color | Removes color cast | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1123 | Match Color Source and Layer | dialog-option | Match Color | Source document and layer | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1124 | Use Selection in Source / Target | dialog-option | Match Color | Computes statistics from selections | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1125 | Match Color Save and Load Statistics | dialog-option | Match Color | Stores color statistics | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/match-color-in-different-images.html |
| PS-A-1126 | Replace Color | adjustment | Image > Adjustments | Selects colors and changes hue, saturation, lightness | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/replace-object-colors-by-applying-a-hue-or-saturation-adjustment.html |
| PS-A-1127 | Replace Color Fuzziness and Localized Clusters | dialog-option | Replace Color | Selection tolerance | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/replace-object-colors-by-applying-a-hue-or-saturation-adjustment.html |
| PS-A-1128 | Replace Color eyedroppers | dialog-option | Replace Color | Sample, add, subtract | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/replace-object-colors-by-applying-a-hue-or-saturation-adjustment.html |
| PS-A-1129 | Replace Color Hue, Saturation, Lightness, Result | dialog-option | Replace Color | Replacement values | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/selective-color-adjustments/replace-object-colors-by-applying-a-hue-or-saturation-adjustment.html |
| PS-A-1130 | Equalize | adjustment | Image > Adjustments | Redistributes brightness values evenly | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1131 | Equalize selected area only / entire image | dialog-option | Equalize | Uses selection histogram for whole image or equalizes selection only | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |

## D12 Auto adjustments

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1132 | Auto Tone (Shift+Ctrl+L) | command | Image menu | Automatic per-channel levels | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1133 | Auto Contrast (Alt+Shift+Ctrl+L) | command | Image menu | Automatic contrast without color shift | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1134 | Auto Color (Shift+Ctrl+B) | command | Image menu | Automatic color correction with neutral midtones | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |

## E01 Image > Mode

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1135 | Bitmap mode | command | Image > Mode | 1-bit black and white | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-an-image-to-bitmap-mode.html |
| PS-A-1136 | Bitmap Output resolution | dialog-option | Bitmap dialog | Resolution of bitmap result | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-an-image-to-bitmap-mode.html |
| PS-A-1137 | Bitmap method 50% Threshold | dialog-option | Bitmap dialog | Hard threshold at 128 | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-an-image-to-bitmap-mode.html |
| PS-A-1138 | Bitmap method Pattern Dither | dialog-option | Bitmap dialog | Geometric dither pattern | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-an-image-to-bitmap-mode.html |
| PS-A-1139 | Bitmap method Diffusion Dither | dialog-option | Bitmap dialog | Error diffusion | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-an-image-to-bitmap-mode.html |
| PS-A-1140 | Bitmap method Halftone Screen | dialog-option | Bitmap dialog | Frequency, angle, shape Round, Diamond, Ellipse, Line, Square, Cross | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-an-image-to-bitmap-mode.html |
| PS-A-1141 | Bitmap method Custom Pattern | dialog-option | Bitmap dialog | Uses a pattern as halftone | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-an-image-to-bitmap-mode.html |
| PS-A-1142 | Grayscale mode | command | Image > Mode | Single channel gray | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-a-color-photo-to-grayscale-mode.html |
| PS-A-1143 | Duotone mode | command | Image > Mode | Monotone, Duotone, Tritone, Quadtone with inks and curves | core | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1144 | Duotone Type and Ink colors | dialog-option | Duotone dialog | Up to four inks with color picker or libraries | core | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1145 | Duotone Ink curves | dialog-option | Duotone dialog | Per ink curve | core | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1146 | Overprint Colors | dialog-option | Duotone dialog | Overprint color display adjustments | core | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1147 | Duotone presets | dialog-option | Duotone dialog | Built-in presets and save and load | core | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1148 | Indexed Color mode | command | Image > Mode | Up to 256 colors with palette | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/convert-a-grayscale-or-rgb-image-to-indexed-color.html |
| PS-A-1149 | Indexed Palette | dialog-option | Indexed Color dialog | Exact, System (Mac/Windows), Web, Uniform, Perceptual, Selective, Adaptive, Custom, Previous | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1150 | Indexed Colors count | dialog-option | Indexed Color dialog | Number of colors | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1151 | Indexed Forced colors | dialog-option | Indexed Color dialog | None, Black and White, Primaries, Web, Custom | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1152 | Indexed Transparency | dialog-option | Indexed Color dialog | Preserves transparency | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1153 | Indexed Matte | dialog-option | Indexed Color dialog | Fill color for anti-aliased edges | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1154 | Indexed Dither None / Diffusion / Pattern / Noise | dialog-option | Indexed Color dialog | Dithering method with amount | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1155 | Preserve Exact Colors | dialog-option | Indexed Color dialog | Prevents dithering exact palette colors | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1156 | Color Table | command | Image > Mode > Color Table | Edits indexed color palette; presets Black Body, Grayscale, Spectrum, System, Custom | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-modes/conversion-options-for-indexed-color-images.html |
| PS-A-1157 | RGB Color mode | command | Image > Mode | Red, green, blue channels | core | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1158 | CMYK Color mode | command | Image > Mode | Cyan, magenta, yellow, black channels | print | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1159 | Lab Color mode | command | Image > Mode | Lightness, a, b channels | core | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1160 | Multichannel mode | command | Image > Mode | 256-level grayscale channels per channel, used for spot printing | print | https://helpx.adobe.com/photoshop/using/color-modes.html |
| PS-A-1161 | 8 Bits/Channel | command | Image > Mode | Standard bit depth | core | https://helpx.adobe.com/photoshop/using/bit-depth.html |
| PS-A-1162 | 16 Bits/Channel | command | Image > Mode | Higher precision editing | core | https://helpx.adobe.com/photoshop/using/bit-depth.html |
| PS-A-1163 | 32 Bits/Channel | command | Image > Mode | HDR floating point | core | https://helpx.adobe.com/photoshop/using/bit-depth.html |
| PS-A-1164 | HDR Toning on 32 to lower conversion | behavior | Image > Mode | Converting 32 to 16 or 8 bits opens HDR Toning | core | https://helpx.adobe.com/photoshop/using/bit-depth.html |
| PS-A-1165 | Discard layers warning on mode change | behavior | Image > Mode | Prompts to merge or flatten when mode requires | core | https://helpx.adobe.com/photoshop/using/color-modes.html |

## E02 Image Size and Canvas Size

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1166 | Image Size (Alt+Ctrl+I) | command | Image menu | Changes pixel dimensions and resolution | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/set-image-size-and-resolution.html |
| PS-A-1167 | Image Size preview window | dialog-option | Image Size dialog | Zoomable preview of resample result | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/set-image-size-and-resolution.html |
| PS-A-1168 | Fit To presets | dialog-option | Image Size dialog | Original Size, Auto Resolution, print and screen presets, Save Preset | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/set-image-size-and-resolution.html |
| PS-A-1169 | Width and Height with units | dialog-option | Image Size dialog | Pixels, percent, inches, cm, mm, points, picas, columns | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/set-image-size-and-resolution.html |
| PS-A-1170 | Constrain Proportions link | dialog-option | Image Size dialog | Keeps aspect ratio | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/set-image-size-and-resolution.html |
| PS-A-1171 | Resolution | dialog-option | Image Size dialog | Pixels per inch or cm | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/set-image-size-and-resolution.html |
| PS-A-1172 | Resample checkbox | dialog-option | Image Size dialog | Changes pixel count; off changes print size only | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resample-option-in-image-size-dialog-box.html |
| PS-A-1173 | Resample Automatic | dialog-option | Image Size dialog | Chooses method by document | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1174 | Resample Preserve Details (enlargement) | dialog-option | Image Size dialog | Preserves detail and sharpness when upscaling with Reduce Noise slider | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1175 | Resample Preserve Details 2.0 | dialog-option | Image Size dialog | AI-based upscaling preserving detail | ai | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1176 | Resample Bicubic Smoother (enlargement) | dialog-option | Image Size dialog | Bicubic for enlargement | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1177 | Resample Bicubic Sharper (reduction) | dialog-option | Image Size dialog | Bicubic for reduction | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1178 | Resample Bicubic (smooth gradients) | dialog-option | Image Size dialog | Standard bicubic | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1179 | Resample Nearest Neighbor (hard edges) | dialog-option | Image Size dialog | No interpolation | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1180 | Resample Bilinear | dialog-option | Image Size dialog | Averaging interpolation | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1181 | Reduce Noise slider | dialog-option | Image Size dialog | Noise reduction with Preserve Details | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/resampling-options.html |
| PS-A-1182 | Scale Styles (Image Size gear) | dialog-option | Image Size dialog | Scales layer effects along with image | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/apply-layer-effects/scale-layer-effects.html |
| PS-A-1183 | Auto Resolution dialog | dialog-option | Image Size dialog | Screen lpi and quality Draft, Good, Best to compute resolution | print | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/change-print-dimensions-and-resolution.html |
| PS-A-1184 | Super Zoom neural filter | command | Filter > Neural Filters | AI enlargement with enhance detail and remove JPEG artifacts | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/enhance-image-quality-with-generative-upscale.html |
| PS-A-1185 | Generative Upscale | command | Image menu or Contextual Task Bar | AI upscaling with Firefly or partner models | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/enhance-image-quality-with-generative-upscale.html |
| PS-A-1186 | Canvas Size (Alt+Ctrl+C) | command | Image menu | Changes canvas dimensions without scaling content | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/resize-canvas-using-the-crop-tool.html |
| PS-A-1187 | Canvas Size Relative | dialog-option | Canvas Size dialog | Adds amount to current size | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/resize-canvas-using-the-crop-tool.html |
| PS-A-1188 | Canvas Size Anchor | dialog-option | Canvas Size dialog | Nine-way anchor for expansion | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/resize-canvas-using-the-crop-tool.html |
| PS-A-1189 | Canvas extension color | dialog-option | Canvas Size dialog | Foreground, Background, White, Black, Gray, Other | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/resize-canvas-using-the-crop-tool.html |

## E03 Rotation, crop, trim, reveal

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1190 | Image Rotation 180 | command | Image > Image Rotation | Rotates canvas 180 degrees | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1191 | Image Rotation 90 Clockwise | command | Image > Image Rotation | Rotates canvas 90 CW | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1192 | Image Rotation 90 Counter Clockwise | command | Image > Image Rotation | Rotates canvas 90 CCW | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1193 | Image Rotation Arbitrary | command | Image > Image Rotation | Rotates canvas by entered angle | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1194 | Flip Canvas Horizontal | command | Image > Image Rotation | Mirrors whole canvas horizontally | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1195 | Flip Canvas Vertical | command | Image > Image Rotation | Mirrors whole canvas vertically | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1196 | Crop (command) | command | Image menu | Crops to selection bounds | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/crop-straighten/crop-photos.html |
| PS-A-1197 | Trim | command | Image menu | Removes border based on transparent pixels, top left or bottom right pixel color | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1198 | Trim sides | dialog-option | Trim dialog | Top, Bottom, Left, Right to trim | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1199 | Reveal All | command | Image menu | Enlarges canvas to show all layer content outside canvas | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1200 | Duplicate (image) | command | Image menu | Duplicates the document, optionally Duplicate Merged Layers Only | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |

## E04 Apply Image and Calculations

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1201 | Apply Image | command | Image menu | Blends a source layer and channel into the active layer | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1202 | Apply Image Source, Layer, Channel, Invert | dialog-option | Apply Image dialog | Source image data selection | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1203 | Apply Image Target | dialog-option | Apply Image dialog | Shows target layer | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1204 | Apply Image Blending and Opacity | dialog-option | Apply Image dialog | Blend mode including Add and Subtract with Scale and Offset | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1205 | Apply Image Preserve Transparency | dialog-option | Apply Image dialog | Keeps target transparency | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1206 | Apply Image Mask | dialog-option | Apply Image dialog | Masks application with image, layer, channel | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1207 | Calculations | command | Image menu | Blends two channels into a new channel, document or selection | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1208 | Calculations Source 1 and Source 2 | dialog-option | Calculations dialog | Image, layer, channel, invert for each source | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1209 | Calculations Blending and Opacity | dialog-option | Calculations dialog | Blend mode, Add and Subtract scale and offset | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1210 | Calculations Mask | dialog-option | Calculations dialog | Optional mask | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1211 | Calculations Result | dialog-option | Calculations dialog | New Document, New Channel, or Selection | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |

## E05 Variables and data sets

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1212 | Variables Define | command | Image > Variables | Defines Visibility, Pixel Replacement, Text Replacement variables per layer | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-A-1213 | Pixel Replacement method | dialog-option | Variables dialog | Fit, Fill, As Is, Conform with alignment and Clip to Bounding Box | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-A-1214 | Data Sets | command | Image > Variables | Creates, imports text or CSV data sets | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-A-1215 | Apply Data Set | command | Image menu | Applies selected data set values to the document | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-A-1216 | Export data sets as files | command | File > Export > Data Sets as Files | Renders each data set to a file | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |

## E06 Analysis and measurement

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1217 | Set Measurement Scale | command | Image > Analysis | Defines pixel length to logical units; presets | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/manage-measurement-scales.html |
| PS-A-1218 | Place Scale Marker | command | Image > Analysis | Adds scale bar with text, font, color, position options | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/manage-scale-markers.html |
| PS-A-1219 | Select Data Points | command | Image > Analysis | Chooses measured properties for Measurement Log | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/measurement-data-points-overview.html |
| PS-A-1220 | Data points list | dialog-option | Select Data Points | Label, Date and Time, Document, Source, Scale, Area, Perimeter, Circularity, Height, Width, Gray Value, Integrated Density, Histogram, Length, Angle, Count | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/measurement-data-points-overview.html |
| PS-A-1221 | Record Measurements | command | Image > Analysis | Records measurements of selection, ruler or count to log | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/measurement-log-for-measurements.html |
| PS-A-1222 | Measurement Log panel | panel | Window > Measurement Log | Table of measurements with export, sort, delete | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/measurement-log-for-measurements.html |
| PS-A-1223 | Ruler tool and Count tool measurement | behavior | Image > Analysis | Measurement sources for recording | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/measure-scale/measurement-log-for-measurements.html |

## F01 Edit menu general

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1224 | Undo (Ctrl+Z) | command | Edit menu | Multi-level undo through history states | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/use-undo-redo-commands.html |
| PS-A-1225 | Redo (Shift+Ctrl+Z) | command | Edit menu | Redo undone step | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/use-undo-redo-commands.html |
| PS-A-1226 | Toggle Last State (Ctrl+Alt+Z) | command | Edit menu | Toggles between last two states | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/use-undo-redo-commands.html |
| PS-A-1227 | Fade (Shift+Ctrl+F) | command | Edit menu | Fades last filter, adjustment or painting with opacity and mode | core | https://helpx.adobe.com/photoshop/using/color-adjustments.html |
| PS-A-1228 | Cut / Copy / Copy Merged / Paste | command | Edit menu | Clipboard commands | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/copy-and-paste-selections.html |
| PS-A-1229 | Paste Special submenu | command | Edit menu | Paste without Formatting, Paste in Place, Paste Into, Paste Outside | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/paste-one-selection-into-or-outside-another.html |
| PS-A-1230 | Clear | command | Edit menu | Deletes selection contents | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/delete-or-cut-selected-pixels.html |
| PS-A-1231 | Search (Ctrl+F) | command | Edit menu | Searches tools, commands, help, stock | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/workspace-overview.html |
| PS-A-1232 | Check Spelling | command | Edit menu | Spell checks text layers | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1233 | Find and Replace Text | command | Edit menu | Finds and replaces text across layers | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1234 | Fill (Shift+F5) | command | Edit menu | Fills selection or layer via Fill dialog | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-selection-layer-color.html |
| PS-A-1235 | Stroke | command | Edit menu | Strokes selection border or layer | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/stroke-selection-layer-color.html |
| PS-A-1236 | Content-Aware Fill workspace | command | Edit menu | Opens Content-Aware Fill workspace | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-objects-with-content-aware-fill.html |
| PS-A-1237 | Generative Fill | command | Edit menu | Fills selection with AI generated content from prompt | ai | https://helpx.adobe.com/photoshop/desktop/create-open-import-images/create-images/edit-images-with-generative-fill.html |
| PS-A-1238 | Prompt to edit | command | Edit menu | Edits image with natural language instructions | ai | https://helpx.adobe.com/photoshop/desktop/create-open-import-images/create-images/edit-images-with-prompt-to-edit.html |
| PS-A-1239 | Content-Aware Scale (Alt+Shift+Ctrl+C) | command | Edit menu | Scales while protecting important content | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/preserve-visual-content-when-scaling-images.html |
| PS-A-1240 | Puppet Warp | command | Edit menu | Mesh-based pin distortion | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1241 | Perspective Warp | command | Edit menu | Plane-based perspective adjustment | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1242 | Free Transform (Ctrl+T) | command | Edit menu | Scales, rotates, skews, distorts, warps with bounding box | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1243 | Transform submenu | command | Edit menu | Again, Scale, Rotate, Skew, Distort, Perspective, Warp, Split Warp, rotations, flips | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1244 | Rotate Object | command | Edit menu | Turns 2D object on pixel layer into rotatable 3D-like object | ai | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-objects.html |
| PS-A-1245 | Reflection Removal | command | Edit menu | Removes glass reflections into separate layers | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/remove-reflections.html |
| PS-A-1246 | Sky Replacement | command | Edit menu | Replaces sky with presets and harmonization | ai | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/replace-the-sky-in-images.html |
| PS-A-1247 | Auto-Align Layers | command | Edit menu | Content-based alignment | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/create-layer-compositions/align-image-layers.html |
| PS-A-1248 | Auto-Blend Layers | command | Edit menu | Content-based blending | core | https://helpx.adobe.com/photoshop/desktop/create-masks/blend-images/auto-blend-layers-command-overview.html |
| PS-A-1249 | Define Brush Preset | command | Edit menu | Creates brush tip from selection or layer grayscale | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/create-brush-tip-image.html |
| PS-A-1250 | Define Pattern | command | Edit menu | Creates pattern preset from selection or image | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/define-an-image-as-a-preset-pattern.html |
| PS-A-1251 | Define Custom Shape | command | Edit menu | Creates custom shape preset from path | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-custom-shapes.html |
| PS-A-1252 | Purge Clipboard / Histories / All / Video Cache | command | Edit > Purge | Frees memory; not undoable | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1253 | Toolbar | command | Edit menu | Customize toolbar dialog | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-A-1254 | Presets > Migrate / Export and Import Presets | command | Edit > Presets | Moves presets between versions or machines | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/import-brushes-brush-packs.html |
| PS-A-1255 | Presets > Preset Manager | command | Edit > Presets | Legacy manager for brushes, swatches, gradients, styles, patterns, contours, shapes, tools | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/import-brushes-brush-packs.html |

## F02 Fill and Stroke dialogs

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1256 | Fill Contents Foreground Color | dialog-option | Fill dialog | Fills with foreground | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-selection-layer-color.html |
| PS-A-1257 | Fill Contents Background Color | dialog-option | Fill dialog | Fills with background | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-selection-layer-color.html |
| PS-A-1258 | Fill Contents Color | dialog-option | Fill dialog | Picks custom color | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-selection-layer-color.html |
| PS-A-1259 | Fill Contents Content-Aware | dialog-option | Fill dialog | Content-aware synthesis fill | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/content-aware-fills.html |
| PS-A-1260 | Content-Aware Color Adaptation | dialog-option | Fill dialog | Blends fill color with surroundings | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/content-aware-fills.html |
| PS-A-1261 | Fill Contents Pattern | dialog-option | Fill dialog | Fills with pattern preset | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/content-aware-fills.html |
| PS-A-1262 | Script pattern fills | dialog-option | Fill dialog | Brick Fill, Cross Weave, Random Fill, Spiral, Symmetry Fill, Place Along Path, Frame scripts | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/content-aware-fills.html |
| PS-A-1263 | Fill Contents History | dialog-option | Fill dialog | Fills from history source | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/content-aware-fills.html |
| PS-A-1264 | Fill Contents Black / 50% Gray / White | dialog-option | Fill dialog | Neutral fills | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-selection-layer-color.html |
| PS-A-1265 | Fill Blending Mode and Opacity | dialog-option | Fill dialog | Fill blend settings | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-selection-layer-color.html |
| PS-A-1266 | Fill Preserve Transparency | dialog-option | Fill dialog | Fills only opaque pixels | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/fill-selection-layer-color.html |
| PS-A-1267 | Stroke Width | dialog-option | Stroke dialog | Stroke thickness px | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/stroke-selection-layer-color.html |
| PS-A-1268 | Stroke Color | dialog-option | Stroke dialog | Stroke color | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/stroke-selection-layer-color.html |
| PS-A-1269 | Stroke Location Inside / Center / Outside | dialog-option | Stroke dialog | Stroke placement | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/stroke-selection-layer-color.html |
| PS-A-1270 | Stroke Blending Mode, Opacity, Preserve Transparency | dialog-option | Stroke dialog | Stroke blending | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/fill-objects-selections-layers/stroke-selection-layer-color.html |

## F03 Content-Aware Fill workspace

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1271 | Sampling Brush tool | tool | CAF toolbar | Paint to add or subtract sampling area | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/tools-to-fine-tune-sampling-and-fill-areas.html |
| PS-A-1272 | Lasso and Polygonal Lasso (CAF) | tool | CAF toolbar | Modify fill area selection | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/tools-to-fine-tune-sampling-and-fill-areas.html |
| PS-A-1273 | Sampling area overlay Show, Opacity, Color, Indicates Sampling or Excluded | panel-option | Content-Aware Fill panel | Display of sampling overlay | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1274 | Sampling Area Auto | panel-option | Content-Aware Fill panel | Uses content similar to fill surroundings | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1275 | Sampling Area Rectangular | panel-option | Content-Aware Fill panel | Rectangular region around fill area | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1276 | Sampling Area Custom | panel-option | Content-Aware Fill panel | Manually painted sampling region | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1277 | Sample All Layers (CAF) | panel-option | Content-Aware Fill panel | Samples from all visible layers | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1278 | Fill Settings Color Adaptation None / Default / High / Very High | panel-option | Content-Aware Fill panel | Contrast and brightness adaptation | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1279 | Fill Settings Rotation Adaptation None / Low / Medium / High / Full | panel-option | Content-Aware Fill panel | Allows rotated samples for curved patterns | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1280 | Fill Settings Scale | panel-option | Content-Aware Fill panel | Allows scaled samples for repeating patterns | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1281 | Fill Settings Mirror | panel-option | Content-Aware Fill panel | Allows horizontally flipped samples | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/adjust-content-aware-fill-settings.html |
| PS-A-1282 | Output To Current Layer / New Layer / Duplicate Layer | panel-option | Content-Aware Fill panel | Where fill result goes | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/apply-or-cancel-fill-changes.html |
| PS-A-1283 | Reset to default fill settings | panel-option | Content-Aware Fill panel | Resets options | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/apply-or-cancel-fill-changes.html |
| PS-A-1284 | Apply and OK and Cancel | panel-option | Content-Aware Fill panel | Apply keeps workspace open for further fills | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/apply-or-cancel-fill-changes.html |
| PS-A-1285 | Preview panel full resolution | panel-option | Preview panel | Full resolution fill preview with zoom | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/view-full-resolution-preview-in-the-preview-panel.html |
| PS-A-1286 | Expand and Contract fill area | panel-option | Options bar (CAF lasso) | Grows or shrinks fill selection | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/tools-to-fine-tune-sampling-and-fill-areas.html |

## F04 Content-Aware Scale

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1287 | Content-Aware Scale reference point | tool-option | Options bar > Content-Aware Scale | Reference point for scaling | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/preserve-visual-content-when-scaling-images.html |
| PS-A-1288 | Amount | tool-option | Options bar > Content-Aware Scale | Ratio of content-aware to normal scaling | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/preserve-visual-content-when-scaling-images.html |
| PS-A-1289 | Protect channel | tool-option | Options bar > Content-Aware Scale | Alpha channel of areas to protect | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/specify-content-to-protect-when-scaling.html |
| PS-A-1290 | Protect skin tones | tool-option | Options bar > Content-Aware Scale | Prevents distorting skin tones | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/specify-content-to-protect-when-scaling.html |
| PS-A-1291 | Content-Aware Scale W and H percent | tool-option | Options bar > Content-Aware Scale | Numeric scale | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/preserve-visual-content-when-scaling-images.html |

## F05 Puppet Warp

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1292 | Puppet Warp Mode Rigid / Normal / Distort | tool-option | Options bar > Puppet Warp | Elasticity of mesh | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1293 | Density Fewer Points / Normal / More Points | tool-option | Options bar > Puppet Warp | Mesh spacing | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1294 | Expansion | tool-option | Options bar > Puppet Warp | Expands or contracts mesh outer edge | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1295 | Show Mesh | tool-option | Options bar > Puppet Warp | Toggles mesh display | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1296 | Pin Depth | tool-option | Options bar > Puppet Warp | Brings pin forward or backward for overlaps | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1297 | Rotate Auto / Fixed | tool-option | Options bar > Puppet Warp | Pin rotation automatic or fixed angle; Alt near pin rotates | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1298 | Remove All Pins | tool-option | Options bar > Puppet Warp | Clears pins | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1299 | Multiple pin selection | behavior | Canvas | Shift-click selects multiple pins to move together | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |

## F06 Perspective Warp

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1300 | Layout mode | tool-option | Options bar > Perspective Warp | Draw quadrilateral planes over image | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1301 | Warp mode | tool-option | Options bar > Perspective Warp | Adjust plane corners to change perspective | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1302 | Automatically straighten near vertical lines | tool-option | Options bar > Perspective Warp | Makes near-vertical edges vertical | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1303 | Automatically level near horizontal lines | tool-option | Options bar > Perspective Warp | Levels near-horizontal edges | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1304 | Automatically straighten horizontal and vertical | tool-option | Options bar > Perspective Warp | Applies both | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1305 | Plane edge Shift-click straighten | behavior | Canvas | Shift-click edge straightens it | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1306 | Perspective Warp keyboard shortcuts | behavior | Canvas | H hides grid, L layout, W warp, Enter commit | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |

## F07 Free Transform and Warp

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1307 | Reference point locator | tool-option | Options bar > Free Transform | Nine-point reference and toggle | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/move-reference-point-for-transformations.html |
| PS-A-1308 | X and Y position | tool-option | Options bar > Free Transform | Reference point coordinates | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1309 | Relative positioning delta | tool-option | Options bar > Free Transform | Uses relative coordinates | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1310 | W and H percent with link | tool-option | Options bar > Free Transform | Scale values and constrain | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1311 | Rotate angle | tool-option | Options bar > Free Transform | Rotation degrees | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1312 | Horizontal and vertical skew | tool-option | Options bar > Free Transform | Skew degrees | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1313 | Interpolation for transform | tool-option | Options bar > Free Transform | Nearest Neighbor, Bilinear, Bicubic, Bicubic Smoother, Bicubic Sharper, Bicubic Automatic | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1314 | Switch between free transform and warp | tool-option | Options bar > Free Transform | Toggles warp mode | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/reshape-and-distort-images-with-transform-warp.html |
| PS-A-1315 | Proportional scaling by default | behavior | Canvas | Scales proportionally unless Shift; Use Legacy Free Transform preference reverses | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/adjust-scale-rotation-and-perspective.html |
| PS-A-1316 | Alt scale from center | behavior | Canvas | Alt scales from reference point | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1317 | Ctrl drag corner distort | behavior | Canvas | Ctrl drags individual corner | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1318 | Ctrl+Shift skew and Ctrl+Alt+Shift perspective | behavior | Canvas | Modifier-based skew and perspective | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1319 | Transform Again (Shift+Ctrl+T) | command | Edit > Transform | Repeats last transform | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/duplicate-objects-as-you-transform.html |
| PS-A-1320 | Duplicate and transform again (Ctrl+Alt+Shift+T) | behavior | Keyboard | Duplicates layer and repeats transform | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/duplicate-objects-as-you-transform.html |
| PS-A-1321 | Scale | command | Edit > Transform | Scale only | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1322 | Rotate | command | Edit > Transform | Rotate only | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1323 | Skew | command | Edit > Transform | Skew only | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1324 | Distort | command | Edit > Transform | Free corner distort | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1325 | Perspective | command | Edit > Transform | Symmetric perspective | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1326 | Warp | command | Edit > Transform | Mesh warp | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/reshape-and-distort-images-with-transform-warp.html |
| PS-A-1327 | Split Warp Horizontally / Vertically / Crosswise | tool-option | Options bar > Warp | Adds split lines to warp grid | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/get-precise-distortions-with-split-warp.html |
| PS-A-1328 | Warp Grid presets 3x3 / 4x4 / 5x5 / Custom | tool-option | Options bar > Warp | Grid density | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/get-precise-distortions-with-split-warp.html |
| PS-A-1329 | Remove Warp Split | tool-option | Options bar > Warp | Removes selected split | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/get-precise-distortions-with-split-warp.html |
| PS-A-1330 | Warp style presets | tool-option | Options bar > Warp | Arc, Arc Lower, Arc Upper, Arch, Bulge, Shell Lower, Shell Upper, Flag, Wave, Fish, Rise, Fisheye, Inflate, Squeeze, Twist | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/reshape-and-distort-images-with-transform-warp.html |
| PS-A-1331 | Warp style Cylinder | tool-option | Options bar > Warp | Wraps artwork around cylinder with curvature and perspective controls | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/warp-a-layer-wth-cylindrical-transform.html |
| PS-A-1332 | Warp Bend, H and V distortion | tool-option | Options bar > Warp | Preset warp parameters | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/reshape-and-distort-images-with-transform-warp.html |
| PS-A-1333 | Warp orientation | tool-option | Options bar > Warp | Horizontal or vertical warp axis | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/reshape-and-distort-images-with-transform-warp.html |
| PS-A-1334 | Warp anchor point selection and multi-point move | behavior | Canvas | Select multiple warp points and move or scale them | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/get-precise-distortions-with-split-warp.html |
| PS-A-1335 | Warp Show Guides and grid color | tool-option | Options bar > Warp | Guide display | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/reshape-and-distort-images-with-transform-warp.html |
| PS-A-1336 | Rotate 180, 90 CW, 90 CCW | command | Edit > Transform | Fixed rotations of layer | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1337 | Flip Horizontal / Flip Vertical | command | Edit > Transform | Mirrors layer | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-or-flip-images.html |
| PS-A-1338 | Commit and cancel transform | tool-option | Options bar > Free Transform | Enter commits, Esc cancels | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/transformation-options-in-adobe-photoshop.html |
| PS-A-1339 | Transform smart object non-destructively | behavior | Smart objects | Transforms preserve source quality | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/smart-objects-overview-and-benefits.html |
| PS-A-1340 | Transform multiple layers | behavior | Canvas | Transforms all selected layers together | core | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/apply-transformations.html |
| PS-A-1341 | Rotate Object on-canvas controls | behavior | Canvas | Drag to rotate or tilt object; Properties panel numeric rotation | ai | https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/transform-manipulate-reshape/rotate-objects.html |

## G01 Brush Settings panel

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1342 | Brush Settings panel | panel | Window > Brush Settings (F5) | Detailed brush tip and dynamics settings | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1343 | Brush Tip Shape Size | panel-option | Brush Tip Shape | Diameter with Restore to Original Size | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1344 | Flip X and Flip Y | panel-option | Brush Tip Shape | Mirrors tip | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1345 | Angle | panel-option | Brush Tip Shape | Rotation of tip | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1346 | Roundness | panel-option | Brush Tip Shape | Ratio of short to long axis | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1347 | Hardness | panel-option | Brush Tip Shape | Edge softness for round brushes | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1348 | Spacing | panel-option | Brush Tip Shape | Distance between dabs as percent of diameter | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1349 | Erodible tip Softness and Shape | panel-option | Brush Tip Shape | Pencil-like tips that wear down; Sharpen Tip button | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1350 | Bristle tip Shape, Bristles, Length, Thickness, Stiffness, Angle | panel-option | Brush Tip Shape | Bristle brush simulation parameters | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1351 | Airbrush tip Hardness, Distortion, Granulation, Spatter Size, Spatter Amount | panel-option | Brush Tip Shape | Airbrush tip parameters | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1352 | Brush tip preview | panel-option | Brush Settings panel | Live stroke preview; bristle brush preview widget | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1353 | Shape Dynamics Size Jitter and Control | panel-option | Shape Dynamics | Random size variation controlled by Fade, Pen Pressure, Pen Tilt, Stylus Wheel, Rotation | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1354 | Minimum Diameter | panel-option | Shape Dynamics | Minimum size under dynamics | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1355 | Tilt Scale | panel-option | Shape Dynamics | Height scale when controlled by pen tilt | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1356 | Angle Jitter and Control | panel-option | Shape Dynamics | Angle variation including Initial Direction and Direction | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1357 | Roundness Jitter and Control | panel-option | Shape Dynamics | Roundness variation with Minimum Roundness | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1358 | Flip X Jitter and Flip Y Jitter | panel-option | Shape Dynamics | Random flipping | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1359 | Brush Projection | panel-option | Shape Dynamics | Applies tilt and rotation to tip shape | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1360 | Scattering Scatter and Both Axes | panel-option | Scattering | Random dab placement perpendicular or both axes with Control | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1361 | Scattering Count | panel-option | Scattering | Dabs per spacing interval | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1362 | Count Jitter and Control | panel-option | Scattering | Varies number of dabs | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1363 | Texture pattern | panel-option | Texture | Pattern applied to strokes with Invert | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1364 | Texture Scale and Brightness and Contrast | panel-option | Texture | Pattern scale and tone | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1365 | Texture Each Tip | panel-option | Texture | Applies texture per dab | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1366 | Texture Mode | panel-option | Texture | Multiply, Subtract, Darken, Overlay, Color Dodge, Color Burn, Linear Burn, Hard Mix, Linear Height, Height | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1367 | Texture Depth, Minimum Depth, Depth Jitter | panel-option | Texture | Paint penetration into texture | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1368 | Dual Brush Mode | panel-option | Dual Brush | Blend mode between primary and second tip | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1369 | Dual Brush tip and Size | panel-option | Dual Brush | Second tip selection and size | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1370 | Dual Brush Spacing, Scatter, Both Axes, Count | panel-option | Dual Brush | Second tip distribution | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1371 | Dual Brush Flip | panel-option | Dual Brush | Flips second tip | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1372 | Color Dynamics Apply Per Tip | panel-option | Color Dynamics | Varies color per dab rather than per stroke | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1373 | Foreground/Background Jitter and Control | panel-option | Color Dynamics | Mixes between fg and bg colors | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1374 | Hue Jitter | panel-option | Color Dynamics | Random hue variation | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1375 | Saturation Jitter | panel-option | Color Dynamics | Random saturation variation | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1376 | Brightness Jitter | panel-option | Color Dynamics | Random brightness variation | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1377 | Purity | panel-option | Color Dynamics | Increases or decreases saturation | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1378 | Transfer Opacity Jitter and Control | panel-option | Transfer | Opacity variation with Minimum | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1379 | Flow Jitter and Control | panel-option | Transfer | Flow variation with Minimum | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1380 | Wetness Jitter and Mix Jitter | panel-option | Transfer | Mixer brush dynamics | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1381 | Brush Pose Override Tilt X | panel-option | Brush Pose | Fixed tilt X for mouse input | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1382 | Brush Pose Override Tilt Y | panel-option | Brush Pose | Fixed tilt Y | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1383 | Brush Pose Override Rotation | panel-option | Brush Pose | Fixed rotation | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1384 | Brush Pose Override Pressure | panel-option | Brush Pose | Fixed pressure | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1385 | Noise | panel-option | Additional options | Adds randomness to soft tip edges | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1386 | Wet Edges | panel-option | Additional options | Watercolor-like buildup at stroke edges | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1387 | Build-up | panel-option | Additional options | Airbrush build-up | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1388 | Smoothing (Brush Settings) | panel-option | Additional options | Smoother curves in strokes | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1389 | Protect Texture | panel-option | Additional options | Applies same pattern and scale to all textured presets | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1390 | Lock brush attribute | panel-option | Brush Settings panel | Lock icons keep section settings when switching presets | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1391 | Create new brush from settings | panel-option | Brush Settings panel | Saves settings as new brush preset | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/create-a-new-preset-brush.html |
| PS-A-1392 | Clear Brush Controls | panel-option | Panel menu | Resets dynamics | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1393 | Reset All Locked Settings | panel-option | Panel menu | Clears locks | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1394 | Copy Texture to Other Tools | panel-option | Panel menu | Propagates texture settings | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |

## G02 Brushes panel and presets

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1395 | Brushes panel | panel | Window > Brushes | Brush presets organized in groups | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/get-started-with-brush-presets.html |
| PS-A-1396 | Brush preset groups and nested groups | panel-option | Brushes panel | Folders for brushes | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/create-preset-brush-groups.html |
| PS-A-1397 | Brush size slider (Brushes panel) | panel-option | Brushes panel | Size for current brush | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/get-started-with-brush-presets.html |
| PS-A-1398 | Brush search | panel-option | Brushes panel | Filters presets by name | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/get-started-with-brush-presets.html |
| PS-A-1399 | Show recent brushes | panel-option | Brushes panel | Recently used row | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/get-started-with-brush-presets.html |
| PS-A-1400 | Preview size slider and view modes | panel-option | Panel menu | Brush Name, Brush Tip, Brush Stroke display options | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/get-started-with-brush-presets.html |
| PS-A-1401 | Import Brushes (.abr) | command | Panel menu | Loads brush packs | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/import-brushes-brush-packs.html |
| PS-A-1402 | Export Selected Brushes | command | Panel menu | Saves presets to .abr | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/import-brushes-brush-packs.html |
| PS-A-1403 | Legacy Brushes | command | Panel menu | Restores legacy brush sets | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/import-brushes-brush-packs.html |
| PS-A-1404 | Converted Legacy Tool Presets | command | Panel menu | Converts tool presets to brushes | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/import-brushes-brush-packs.html |
| PS-A-1405 | Get More Brushes | command | Panel menu | Downloads additional brushes | cloud | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/import-brushes-brush-packs.html |
| PS-A-1406 | Rename and delete brushes | command | Brushes panel | Manage presets | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/create-a-new-preset-brush.html |
| PS-A-1407 | New Brush Preset include tool settings and color | dialog-option | New Brush dialog | Capture size, tool settings and color with preset | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/create-a-new-preset-brush.html |
| PS-A-1408 | Brush presets with Capture Brush Size | dialog-option | New Brush dialog | Stores current size | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/create-a-new-preset-brush.html |
| PS-A-1409 | Brush from image (Define Brush Preset) | behavior | Edit menu | Grayscale sample up to 5000x5000 px | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/create-brush-tip-image.html |
| PS-A-1410 | Brush tool presets vs brushes | behavior | Brushes panel | Tool presets hold full tool options | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/create-tool-preset.html |

## G03 Symmetry painting

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1411 | Symmetry Vertical | tool-option | Options bar > Brush tool > Symmetry | Mirrors across vertical axis | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1412 | Symmetry Horizontal | tool-option | Options bar > Brush tool > Symmetry | Mirrors across horizontal axis | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1413 | Symmetry Dual Axis | tool-option | Options bar > Brush tool > Symmetry | Vertical and horizontal mirror | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1414 | Symmetry Diagonal | tool-option | Options bar > Brush tool > Symmetry | Mirrors across diagonal line | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1415 | Symmetry Wavy | tool-option | Options bar > Brush tool > Symmetry | Wavy symmetry path | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1416 | Symmetry Circle | tool-option | Options bar > Brush tool > Symmetry | Circular symmetry | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1417 | Symmetry Spiral | tool-option | Options bar > Brush tool > Symmetry | Spiral symmetry | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1418 | Symmetry Parallel Lines | tool-option | Options bar > Brush tool > Symmetry | Parallel lines symmetry | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1419 | Symmetry Radial | tool-option | Options bar > Brush tool > Symmetry | Radial segments 2 to 12 | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1420 | Symmetry Mandala | tool-option | Options bar > Brush tool > Symmetry | Mirrored radial segments 2 to 12 | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1421 | Symmetry from path | tool-option | Options bar > Brush tool > Symmetry | Uses custom path as symmetry path | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1422 | Symmetry path transform | behavior | Canvas | Symmetry path can be moved, scaled, rotated before painting | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1423 | Show or hide symmetry | tool-option | Options bar > Brush tool > Symmetry | Hide symmetry path display | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |
| PS-A-1424 | Symmetry works with Brush, Pencil, Eraser, Mixer Brush | behavior | Options bar > Brush tool > Symmetry | Painting tools supported | core | https://helpx.adobe.com/photoshop/using/painting-tools.html |

## G04 Color panels

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1425 | Color panel | panel | Window > Color (F6) | Color selection with sliders or fields | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1426 | Color panel Hue Cube / Brightness Cube / Color Wheel | panel-option | Color panel | Picker modes | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1427 | Color panel sliders modes | panel-option | Color panel menu | Grayscale, RGB, HSB, CMYK, Lab, Web Color sliders | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1428 | Color panel spectrum ramps | panel-option | Color panel menu | RGB, CMYK, Grayscale, Current Colors ramps; Make Ramp Web Safe | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1429 | Out-of-gamut warning and web-safe cube | panel-option | Color panel | Gamut and web warnings | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-a-cmyk-equivalent-for-a-non-printable-color.html |
| PS-A-1430 | Adobe Color Picker | dialog-option | Color Picker dialog | HSB, RGB, Lab, CMYK, hex fields with color field and slider | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-colors-with-the-adobe-color-picker.html |
| PS-A-1431 | Only Web Colors | dialog-option | Color Picker dialog | Restricts to web-safe palette | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-websafe-colors.html |
| PS-A-1432 | Color Libraries | dialog-option | Color Picker dialog | Spot color libraries such as PANTONE | print | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-a-spot-color.html |
| PS-A-1433 | Add to Swatches (Color Picker) | dialog-option | Color Picker dialog | Adds color as swatch | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-colors-with-the-adobe-color-picker.html |
| PS-A-1434 | Color Picker Eyedropper sampling | behavior | Color Picker dialog | Clicking the image while dialog open samples color | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-colors-with-the-adobe-color-picker.html |
| PS-A-1435 | Gamut warning in Color Picker | dialog-option | Color Picker dialog | Triangle warning with nearest in-gamut | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-a-cmyk-equivalent-for-a-non-printable-color.html |
| PS-A-1436 | Swatches panel | panel | Window > Swatches | Color swatches in groups | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1437 | Swatches recent colors | panel-option | Swatches panel | Row of recently used colors | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1438 | Swatches groups and New Swatch | panel-option | Swatches panel | Create swatches and folders | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1439 | Import and Export Swatches | panel-option | Swatches panel menu | .aco, .ase files; Export for exchange | format | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1440 | Legacy Swatches | panel-option | Swatches panel menu | Restores legacy swatch sets | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1441 | Swatch display small, large, list | panel-option | Swatches panel menu | View options | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/set-foreground-and-background-colors.html |
| PS-A-1442 | Gradients panel | panel | Window > Gradients | Gradient presets in groups; drag onto canvas or layer | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/apply-gradient-fill.html |
| PS-A-1443 | Gradients panel Import / Export / Legacy | panel-option | Gradients panel menu | .grd loading and legacy sets | core | https://helpx.adobe.com/photoshop/desktop/adjust-color/color-effects-techniques/edit-a-gradient.html |
| PS-A-1444 | Patterns panel | panel | Window > Patterns | Pattern presets in groups; drag to apply | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/create-fill-with-patterns/create-a-new-pattern.html |
| PS-A-1445 | Patterns panel Import / Export / Legacy | panel-option | Patterns panel menu | .pat files | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/create-fill-with-patterns/create-a-new-pattern.html |
| PS-A-1446 | Pattern Preview | command | View > Pattern Preview | Shows canvas tiled to preview seamless pattern | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/create-fill-with-patterns/pattern-preview-best-practices.html |
| PS-A-1447 | Shapes panel | panel | Window > Shapes | Custom shape presets in groups | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-custom-shapes.html |
| PS-A-1448 | Info panel | panel | Window > Info (F8) | Color values, position, size, document info, samplers | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-1449 | Info panel options | panel-option | Info panel menu | First and second readouts, mouse coordinates units, status info toggles | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-1450 | Histogram panel | panel | Window > Histogram | Tonal distribution with channel, statistics, cache refresh | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1451 | Histogram views Compact / Expanded / All Channels | panel-option | Histogram panel | Display modes with source selector | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |
| PS-A-1452 | Histogram statistics | panel-option | Histogram panel | Mean, Std Dev, Median, Pixels, Level, Count, Percentile, Cache Level | core | https://helpx.adobe.com/photoshop/using/levels-adjustment.html |

## G05 Other retouching features

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1453 | Vignette with selection and fill | behavior | Retouching | Darken edges workflow using feathered selection or Levels | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/darken-the-edges-of-your-image-to-bring-focus-to-its-center.html |
| PS-A-1454 | Vanishing Point | command | Filter > Vanishing Point | Edits in perspective planes with clone, brush, marquee | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-A-1455 | Harmonize | command | Contextual Task Bar or Layer menu | Matches lighting, color and shadows of composited subject to background | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/blend-subjects-with-harmonize.html |
| PS-A-1456 | Remove Background | command | Properties Quick Actions and Contextual Task Bar | Masks out background of layer | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-background-in-your-images.html |
| PS-A-1457 | Generate Background | command | Contextual Task Bar | Replaces background with generated content | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/replace-background-with-generate-background.html |
| PS-A-1458 | Photomerge | command | File > Automate > Photomerge | Panorama stitching | automation | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/retouch-tools-overview.html |
| PS-A-1459 | Dodge and burn with 50 percent gray layer | behavior | Retouching | Non-destructive dodge and burn via Overlay layer | core | https://helpx.adobe.com/photoshop/desktop/repair-retouch/adjust-light-tone/dodge-or-burn-image-areas.html |

## H01 Channels panel

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1460 | Channels panel | panel | Window > Channels | Composite, color, spot and alpha channels with thumbnails | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1461 | Channel visibility and target | panel-option | Channels panel | Eye toggles view; click targets channel for editing | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1462 | Show composite and single channel view shortcuts | behavior | Keyboard | Ctrl+2 composite, Ctrl+3 through Ctrl+5 individual channels | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1463 | Show Channels in Color | behavior | Preferences > Interface | Displays individual channels in their color | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1464 | Load channel as selection button | panel-option | Channels panel | Loads selected channel as selection | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-1465 | Save selection as channel button | panel-option | Channels panel | Saves selection to new alpha channel | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-1466 | Create new channel button | panel-option | Channels panel | New alpha channel | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1467 | Delete channel button | panel-option | Channels panel | Deletes channel | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1468 | New Channel dialog | dialog-option | Channels panel | Name, Color Indicates Masked or Selected Areas, color and opacity | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1469 | Duplicate Channel | command | Panel menu | Copies channel to same, other or new document with Invert option | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1470 | New Spot Channel | command | Panel menu | Adds spot color channel with ink color and Solidity | print | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1471 | Merge Spot Channel | command | Panel menu | Merges spot channel into color channels | print | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1472 | Channel Options | command | Panel menu | Edits alpha or spot channel options | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1473 | Split Channels | command | Panel menu | Splits channels into separate grayscale documents | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1474 | Merge Channels | command | Panel menu | Combines grayscale documents into multichannel image with mode choice | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1475 | Panel Options thumbnail size (Channels) | panel-option | Panel menu | Thumbnail size | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1476 | Rename alpha channel | behavior | Channels panel | Double-click name to rename | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1477 | Reorder alpha channels | behavior | Channels panel | Drag alpha and spot channels to reorder | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |
| PS-A-1478 | Edit alpha channel with painting | behavior | Canvas | Paint in alpha channel to modify saved selection | core | https://helpx.adobe.com/photoshop/using/saving-selections-alpha-channel-masks.html |
| PS-A-1479 | Channel masks in Apply Image and Calculations | behavior | Channels panel | Channels as sources for blending | core | https://helpx.adobe.com/photoshop/using/channel-calculations.html |
| PS-A-1480 | Channel limit 56 | behavior | Channels panel | Maximum channels per document | core | https://helpx.adobe.com/photoshop/using/channel-basics.html |

## H02 Paths panel

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1481 | Paths panel | panel | Window > Paths | Lists saved paths, work path, shape and vector mask paths | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1482 | Work Path | behavior | Paths panel | Temporary path until saved | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1483 | Save Path | command | Panel menu | Saves work path with name | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1484 | New Path | command | Paths panel | Creates new empty path | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1485 | Duplicate Path | command | Panel menu | Copies path | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1486 | Delete Path | command | Paths panel | Deletes path | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1487 | Fill Path | command | Panel menu and button | Fills path with color, pattern, history using mode, opacity, feather, anti-alias | core | https://helpx.adobe.com/photoshop/using/adding-color-paths.html |
| PS-A-1488 | Stroke Path | command | Panel menu and button | Strokes path with selected painting tool; Simulate Pressure | core | https://helpx.adobe.com/photoshop/using/adding-color-paths.html |
| PS-A-1489 | Make Selection from path | command | Panel menu and button | Converts path to selection with feather, anti-alias, operation | core | https://helpx.adobe.com/photoshop/using/converting-paths-selection-borders.html |
| PS-A-1490 | Make Work Path from selection | command | Panel menu and button | Converts selection to path with tolerance | core | https://helpx.adobe.com/photoshop/using/converting-paths-selection-borders.html |
| PS-A-1491 | Add mask from path button | panel-option | Paths panel | Creates vector mask from path | core | https://helpx.adobe.com/photoshop/using/masking-layers-vector-masks.html |
| PS-A-1492 | Clipping Path | command | Panel menu | Sets path as clipping path for export with flatness | print | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1493 | Panel Options (Paths) | panel-option | Panel menu | Thumbnail size | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1494 | Path thumbnail rename | behavior | Paths panel | Double-click to rename | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1495 | Deselect path | behavior | Paths panel | Click empty area to hide path | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1496 | Export paths to Illustrator | command | File > Export > Paths to Illustrator | Saves paths as .ai | format | https://helpx.adobe.com/photoshop/using/editing-paths.html |

## H03 History panel

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1497 | History panel | panel | Window > History | Lists history states for undo and snapshots | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1498 | History states list | panel-option | History panel | Click a state to revert; later states are dimmed | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1499 | Delete state | panel-option | History panel | Deletes state and following states | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1500 | Create new snapshot | panel-option | History panel | Snapshot of current state | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/create-work-snapshots.html |
| PS-A-1501 | Create new document from current state | panel-option | History panel | New document from state | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/manage-image-states.html |
| PS-A-1502 | New Snapshot dialog From Full Document / Merged Layers / Current Layer | dialog-option | History panel | Snapshot content scope | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/create-work-snapshots.html |
| PS-A-1503 | History Options Automatically Create First Snapshot | panel-option | History Options | Snapshot on open | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1504 | History Options Automatically Create New Snapshot When Saving | panel-option | History Options | Snapshot per save | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1505 | History Options Allow Non-Linear History | panel-option | History Options | Keeps later states when editing from earlier state | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1506 | History Options Show New Snapshot Dialog by Default | panel-option | History Options | Prompts for snapshot name | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1507 | History Options Make Layer Visibility Changes Undoable | panel-option | History Options | Records visibility toggles | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1508 | History States count | behavior | Preferences > Performance | Number of states retained (default 50) | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-panel-overview.html |
| PS-A-1509 | History Log | behavior | Preferences > History Log | Saves history to metadata or text file, Sessions Only, Concise, Detailed | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/history-log-preferences.html |
| PS-A-1510 | Set history brush source | panel-option | History panel | Column for History Brush source | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/paint-image-states.html |
| PS-A-1511 | Clear History | command | Panel menu | Clears all states without undo | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/manage-image-states.html |
| PS-A-1512 | Step forward and backward shortcuts | behavior | Keyboard | Ctrl+Z and Shift+Ctrl+Z multi-level undo | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/use-undo-redo-commands.html |
| PS-A-1513 | Restore parts of image from state | behavior | History panel | Use History Brush or Fill with History | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/restore-image-parts.html |

## H04 Properties panel and Contextual Task Bar

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1514 | Properties panel | panel | Window > Properties | Context-sensitive settings for selected layer or document | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-1515 | Document properties | panel-option | Properties panel | Canvas size, resolution, mode, rulers and grids, guide options when no layer selected | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-1516 | Document Quick Actions | panel-option | Properties panel | Trim, Image Size, Crop, Rotate buttons for document | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-1517 | Pixel layer properties Transform | panel-option | Properties panel | W, H, X, Y, angle and flips | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-1518 | Pixel layer Align and Distribute | panel-option | Properties panel | Alignment buttons | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-1519 | Pixel layer Quick Actions | panel-option | Properties panel | Remove Background, Select Subject and similar | ai | https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-background-in-your-images.html |
| PS-A-1520 | Type layer properties | panel-option | Properties panel | Character, paragraph, transform and type options in Properties | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-text.html |
| PS-A-1521 | Shape layer properties | panel-option | Properties panel | Appearance, fill, stroke, live shape geometry | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1522 | Live Shape properties corner radii | panel-option | Shape layer | Per-corner radius with link toggle | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1523 | Pathfinder operations in Properties | panel-option | Shape layer | Combine, Subtract, Intersect, Exclude shape buttons | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1524 | Smart Object properties | panel-option | Properties panel | Linked or embedded info with actions | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/smart-objects/view-linked-smart-object-properties.html |
| PS-A-1525 | Adjustment properties | panel-option | Properties panel | Adjustment controls | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/color-adjustment-fill-layers/work-with-adjustment-and-fill-layers.html |
| PS-A-1526 | Masks properties | panel-option | Properties panel | Density, feather, refine | core | https://helpx.adobe.com/photoshop/desktop/create-masks/layer-masks/add-layer-masks.html |
| PS-A-1527 | Artboard properties | panel-option | Properties panel | Artboard size and background | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/artboard-properties.html |
| PS-A-1528 | Generative layer properties | panel-option | Properties panel | Prompt, variations, Generate Similar | ai | https://helpx.adobe.com/photoshop/desktop/create-open-import-images/create-images/edit-images-with-generative-fill.html |
| PS-A-1529 | Contextual Task Bar selection actions | panel-option | Contextual Task Bar | Select subject, remove background, generative fill, modify selection, mask, fill | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-1530 | Contextual Task Bar layer actions | panel-option | Contextual Task Bar | Transform image, Rotate object, Harmonize, Upscale based on layer | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-A-1531 | Contextual Task Bar type actions | panel-option | Contextual Task Bar | Font, size, color, Dynamic Text presets for text layers | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/dynamic-text-overview.html |
| PS-A-1532 | Contextual Task Bar prompt entry | panel-option | Contextual Task Bar | Natural language editing prompt | ai | https://helpx.adobe.com/photoshop/desktop/create-open-import-images/create-images/edit-images-with-prompt-to-edit.html |
| PS-A-1533 | Contextual Task Bar more options | panel-option | Contextual Task Bar | Hide bar, reset position, pin position | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |

## I01 Character panel

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1534 | Character panel | panel | Window > Character | Character-level formatting | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1535 | Font family | panel-option | Character panel | Font selection with live preview on hover | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1536 | Font style | panel-option | Character panel | Weight and style of family | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1537 | Font size | panel-option | Character panel | Type size | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1538 | Leading | panel-option | Character panel | Line spacing; Auto leading percent in Justification | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1539 | Kerning Metrics / Optical / 0 / value | panel-option | Character panel | Spacing between character pairs | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1540 | Tracking | panel-option | Character panel | Uniform spacing across range | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1541 | Vertical Scale | panel-option | Character panel | Scales glyph height | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1542 | Horizontal Scale | panel-option | Character panel | Scales glyph width | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1543 | Baseline Shift | panel-option | Character panel | Raises or lowers characters | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1544 | Text color (Character) | panel-option | Character panel | Fill color of text | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/change-text-color.html |
| PS-A-1545 | Tsume | panel-option | Character panel | Reduces space around CJK characters | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/update-cjk-text-layers.html |
| PS-A-1546 | Faux Bold | panel-option | Character panel | Simulated bold | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1547 | Faux Italic | panel-option | Character panel | Simulated italic | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1548 | All Caps | panel-option | Character panel | Uppercase display | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1549 | Small Caps | panel-option | Character panel | Small capitals | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1550 | Superscript | panel-option | Character panel | Raised small characters | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1551 | Subscript | panel-option | Character panel | Lowered small characters | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1552 | Underline | panel-option | Character panel | Underline with Left or Right for vertical | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1553 | Strikethrough | panel-option | Character panel | Strikethrough line | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1554 | OpenType buttons in Character panel | panel-option | Character panel | Standard Ligatures, Contextual Alternates, Discretionary Ligatures, Swash, Stylistic Alternates, Titling Alternates, Ordinals, Fractions | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/apply-opentype-features.html |
| PS-A-1555 | Language dictionary | panel-option | Character panel | Hyphenation and spelling language | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1556 | Anti-aliasing (Character) | panel-option | Character panel | Anti-aliasing method | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1557 | Fractional Widths | panel-option | Panel menu | Fractional character spacing | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1558 | System Layout | panel-option | Panel menu | Uses OS text rendering for UI mockups | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1559 | No Break | panel-option | Panel menu | Prevents line breaks within words | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1560 | Change Text Orientation | panel-option | Panel menu | Horizontal or vertical | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1561 | Standard Vertical Roman Alignment | panel-option | Panel menu | Rotation of half-width in vertical text | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/update-cjk-text-layers.html |
| PS-A-1562 | Reset Character | panel-option | Panel menu | Resets formatting | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1563 | Middle Eastern features Digits, Diacritic position | panel-option | Character panel (World-Ready) | Arabic, Hindi digits and diacritic settings | core | https://helpx.adobe.com/photoshop/desktop/text-typography/international-text-languages/create-documents-using-international-languages-scripts-and-type.html |
| PS-A-1564 | Font menu filters | panel-option | Font menu | Filter by classification, favorites, recently added, activated Adobe Fonts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/search-for-and-apply-a-specific-font-style.html |
| PS-A-1565 | Show similar fonts | panel-option | Font menu | Lists visually similar fonts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/search-for-and-apply-a-specific-font-style.html |
| PS-A-1566 | Font preview size | behavior | Type > Font Preview Size | Preview size in font menu | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/about-fonts.html |
| PS-A-1567 | Adobe Fonts activation | behavior | Font menu | Activates cloud fonts | cloud | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/about-fonts.html |
| PS-A-1568 | Replace missing fonts | command | Type > Manage Missing Fonts | Resolves or activates missing fonts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/replace-missing-fonts.html |
| PS-A-1569 | Change font on multiple layers | behavior | Layers panel | Select multiple type layers and change font together | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/change-the-font-on-multiple-layers.html |

## I02 Paragraph panel

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1570 | Paragraph panel | panel | Window > Paragraph | Paragraph formatting | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1571 | Align left, center, right | panel-option | Paragraph panel | Paragraph alignment | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1572 | Justify last left, center, right, all | panel-option | Paragraph panel | Justification variants | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1573 | Left indent | panel-option | Paragraph panel | Left margin | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1574 | Right indent | panel-option | Paragraph panel | Right margin | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1575 | First line indent | panel-option | Paragraph panel | First line indent including hanging | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1576 | Space before paragraph | panel-option | Paragraph panel | Space above | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1577 | Space after paragraph | panel-option | Paragraph panel | Space below | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1578 | Hyphenate | panel-option | Paragraph panel | Auto hyphenation toggle | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1579 | Hyphenation settings | dialog-option | Hyphenation dialog | Words longer than, after first, before last, hyphen limit, zone, hyphenate capitalized words | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1580 | Justification settings | dialog-option | Justification dialog | Word spacing, letter spacing, glyph scaling min desired max, auto leading | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1581 | Composer Adobe Single-line / Every-line | panel-option | Panel menu | Line composition method | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1582 | World-Ready composers | panel-option | Panel menu | Middle Eastern and South Asian composers | core | https://helpx.adobe.com/photoshop/desktop/text-typography/international-text-languages/overview-of-unified-text-engine.html |
| PS-A-1583 | Roman Hanging Punctuation | panel-option | Panel menu | Punctuation outside margins | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |
| PS-A-1584 | Kinsoku and Mojikumi | panel-option | Paragraph panel | CJK line break and spacing rules | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/update-cjk-text-layers.html |
| PS-A-1585 | Paragraph direction LTR / RTL | panel-option | Paragraph panel | Text direction for right-to-left languages | core | https://helpx.adobe.com/photoshop/desktop/text-typography/international-text-languages/create-documents-using-international-languages-scripts-and-type.html |
| PS-A-1586 | Bulleted list | panel-option | Paragraph panel | Adds bullets with style options | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-bulleted-and-numbered-lists.html |
| PS-A-1587 | Numbered list | panel-option | Paragraph panel | Adds numbering with style options | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/add-bulleted-and-numbered-lists.html |
| PS-A-1588 | Reset Paragraph | panel-option | Panel menu | Resets paragraph settings | core | https://helpx.adobe.com/photoshop/using/formatting-paragraphs.html |

## I03 Character and Paragraph styles

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1589 | Character Styles panel | panel | Window > Character Styles | Named character formatting presets | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1590 | Paragraph Styles panel | panel | Window > Paragraph Styles | Named paragraph formatting presets | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1591 | Create new style from selection | panel-option | Styles panels | Captures current formatting | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1592 | Style Options dialog | dialog-option | Styles panels | Basic Character Formats, Advanced, OpenType Features, Indents and Spacing, Composition, Justification, Hyphenation | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1593 | Redefine style / Clear override | panel-option | Styles panels | Syncs style with overrides or clears them | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |
| PS-A-1594 | Load Styles / Save Default Type Styles | panel-option | Panel menu | Import styles from document and defaults | core | https://helpx.adobe.com/photoshop/using/formatting-characters.html |

## I04 OpenType, variable fonts, glyphs

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1595 | OpenType submenu features | panel-option | Character panel menu | Standard and discretionary ligatures, contextual alternates, swash, oldstyle, stylistic alternates, titling, ornaments, ordinals, fractions, stylistic sets, justification alternates | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/apply-opentype-features.html |
| PS-A-1596 | On-canvas glyph alternates | behavior | Canvas | Selecting a character shows alternate glyphs popup | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/use-on-canvas-glyph-alternatives.html |
| PS-A-1597 | Variable fonts | behavior | Properties panel | Sliders for weight, width, slant and other axes | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/use-opentype-variable-fonts.html |
| PS-A-1598 | OpenType SVG fonts | behavior | Type | Multicolor and gradient glyphs, emoji fonts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/work-with-opentype-svg-fonts.html |
| PS-A-1599 | Emoji glyph composition | behavior | Type | Combines emoji with skin tones and flags | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/add-emoji-glyphs.html |
| PS-A-1600 | Glyphs panel | panel | Window > Glyphs | Browse and insert glyphs by font | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/add-glyphs.html |
| PS-A-1601 | Glyphs panel Show filter | panel-option | Glyphs panel | Entire font, alternates, OpenType feature subsets | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/add-glyphs.html |
| PS-A-1602 | Glyphs panel recently used | panel-option | Glyphs panel | Recent glyphs row | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/add-glyphs.html |
| PS-A-1603 | Glyphs panel search | panel-option | Glyphs panel | Search by name or Unicode | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/add-glyphs.html |
| PS-A-1604 | Glyphs panel zoom | panel-option | Glyphs panel | Glyph grid size | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/add-glyphs.html |
| PS-A-1605 | Glyph protection | behavior | Preferences > Type | Prevents missing-glyph substitution with wrong fonts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/characters-glyphs/enable-glyph-protection.html |
| PS-A-1606 | Match Font | command | Type > Match Font | Recognizes font in image region and suggests similar installed or Adobe Fonts | ai | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/match-fonts.html |
| PS-A-1607 | Match Font show fonts available to sync | dialog-option | Match Font dialog | Include Adobe Fonts suggestions | ai | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/match-fonts.html |
| PS-A-1608 | Unified Text Engine | behavior | Preferences > Type | Text engine supporting world scripts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/international-text-languages/overview-of-unified-text-engine.html |
| PS-A-1609 | Text engine options East Asian / Middle Eastern and South Asian | behavior | Preferences > Type | Chooses script feature set | core | https://helpx.adobe.com/photoshop/desktop/text-typography/international-text-languages/create-documents-using-international-languages-scripts-and-type.html |

## I05 Type menu and text commands

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1610 | More from Adobe Fonts | command | Type menu | Browse Adobe Fonts | cloud | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/about-fonts.html |
| PS-A-1611 | Panels submenu | command | Type menu | Character, Paragraph, Glyphs, Styles panels | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1612 | Anti-Alias submenu | command | Type menu | Anti-aliasing methods | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1613 | Orientation Horizontal / Vertical | command | Type menu | Text direction | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1614 | OpenType submenu | command | Type menu | OpenType features | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/apply-opentype-features.html |
| PS-A-1615 | Extrude to 3D (removed) | command | Type menu | Legacy 3D | 3d | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1616 | Create Work Path | command | Type menu | Converts text outlines to work path | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/convert-text-to-shapes-or-work-paths.html |
| PS-A-1617 | Convert to Shape | command | Type menu | Converts text to shape layer | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/convert-text-to-shapes-or-work-paths.html |
| PS-A-1618 | Rasterize Type Layer | command | Type menu | Converts text to pixels | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1619 | Convert Text Shape Type | command | Type menu | Point to paragraph conversion | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1620 | Warp Text | command | Type menu | Opens warp dialog | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/warp-and-unwarp-text.html |
| PS-A-1621 | Match Font | command | Type menu | Font recognition | ai | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/match-fonts.html |
| PS-A-1622 | Font Preview Size | command | Type menu | None, Small, Medium, Large, Extra Large, Huge | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1623 | Language Options | command | Type menu | Text engine choice | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1624 | Update All Text Layers | command | Type menu | Updates layers from older versions | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/update-cjk-text-layers.html |
| PS-A-1625 | Manage Missing Fonts | command | Type menu | Resolve missing fonts | core | https://helpx.adobe.com/photoshop/desktop/text-typography/select-manage-fonts/replace-missing-fonts.html |
| PS-A-1626 | Paste Lorem Ipsum | command | Type menu | Inserts placeholder text | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1627 | Load Default Type Styles / Save Default Type Styles | command | Type menu | Type style defaults | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1628 | Check Spelling dialog | dialog-option | Edit > Check Spelling | Ignore, Ignore All, Change, Change All, Add, language, check all layers | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1629 | Find and Replace Text dialog | dialog-option | Edit > Find and Replace Text | Search All Layers, Forward, Case Sensitive, Whole Word, Ignore Accents | core | https://helpx.adobe.com/photoshop/using/editing-text.html |
| PS-A-1630 | Fill text with image | behavior | Layers panel | Clipping image to text layer | core | https://helpx.adobe.com/photoshop/desktop/text-typography/type-layers-creation/fill-text-with-image.html |
| PS-A-1631 | Text selection borders with type mask | behavior | Type menu | Type mask tools create selections | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/create-text-selection-borders.html |
| PS-A-1632 | Drop shadow on text | behavior | Type menu | Layer styles on type | core | https://helpx.adobe.com/photoshop/using/layer-opacity-blending.html |
| PS-A-1633 | Rotate text | behavior | Type menu | Transform type layer | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/rotate-text.html |
| PS-A-1634 | Resize text by handles | behavior | Type menu | Scales type with transform | core | https://helpx.adobe.com/photoshop/desktop/text-typography/get-started-with-text/resize-text.html |

## I06 Type on path, warp text, Dynamic Text

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1635 | Text on open path | behavior | Type on path | Clicking on path with Type tool flows text along it | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/add-text-along-paths-or-inside-shapes.html |
| PS-A-1636 | Text inside closed path | behavior | Type on path | Clicking inside closed shape creates area type | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/add-text-along-paths-or-inside-shapes.html |
| PS-A-1637 | Flip text across path | behavior | Type on path | Drag across path with Path Selection flips side | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/flip-or-move-text-along-a-path.html |
| PS-A-1638 | Move start and end points on path | behavior | Type on path | Drag start or end markers along path | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/flip-or-move-text-along-a-path.html |
| PS-A-1639 | Edit text path shape | behavior | Type on path | Direct Selection edits type path | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/modify-text-paths.html |
| PS-A-1640 | Text on any shape or path (Flow text) | behavior | Type on path | Apply text to any shape or path with position and direction controls | core | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-A-1641 | Warp Text dialog Style | dialog-option | Warp Text dialog | Arc, Arc Lower, Arc Upper, Arch, Bulge, Shell Lower, Shell Upper, Flag, Wave, Fish, Rise, Fisheye, Inflate, Squeeze, Twist | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/warp-and-unwarp-text.html |
| PS-A-1642 | Warp Text Horizontal / Vertical | dialog-option | Warp Text dialog | Axis of warp | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/warp-and-unwarp-text.html |
| PS-A-1643 | Warp Text Bend | dialog-option | Warp Text dialog | Amount of warp | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/warp-and-unwarp-text.html |
| PS-A-1644 | Warp Text Horizontal and Vertical Distortion | dialog-option | Warp Text dialog | Perspective distortion | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/warp-and-unwarp-text.html |
| PS-A-1645 | Unwarp text (None) | dialog-option | Warp Text dialog | Removes warp | core | https://helpx.adobe.com/photoshop/desktop/text-typography/text-on-paths-shapes/warp-and-unwarp-text.html |
| PS-A-1646 | Dynamic Text presets Block / Circle / Arch / Bow | command | Contextual Task Bar or Type | Wraps and scales text into preset shapes | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/dynamic-text-overview.html |
| PS-A-1647 | Dynamic Text Block word and line spacing | panel-option | Properties panel | Spacing adjustments for Block | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/dynamic-text-overview.html |
| PS-A-1648 | Dynamic Text text position | panel-option | Properties panel | Above, center, below relative to path | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/dynamic-text-overview.html |
| PS-A-1649 | Dynamic Text direction | panel-option | Properties panel | Toggles reading direction | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/dynamic-text-overview.html |
| PS-A-1650 | Dynamic fit | panel-option | Properties panel | Auto-resizes text to fill any path or shape as text changes | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/dynamic-text-overview.html |
| PS-A-1651 | Dynamic Text reposition start and end points | behavior | Canvas | Drag endpoints to set range text spans | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/reposition-start-and-end-points.html |
| PS-A-1652 | Dynamic Text formatting and resize | behavior | Canvas | Resize shape and text reformats to fit | core | https://helpx.adobe.com/photoshop/desktop/text-typography/work-with-dynamic-text/adjust-formatting-and-resize-text-with-dynamic-text.html |

## J01 Shapes and path editing

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1653 | Anchor point types smooth and corner | behavior | Shapes and paths | Smooth points with linked handles, corner points with independent handles | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1654 | Close path | behavior | Shapes and paths | Clicking first anchor closes path | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1655 | Continue open path | behavior | Shapes and paths | Clicking endpoint with Pen continues path | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1656 | Join paths | behavior | Shapes and paths | Connects endpoints of two open paths | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1657 | Select multiple anchors | behavior | Shapes and paths | Shift-click or marquee with Direct Selection | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1658 | Delete anchor or segment | behavior | Shapes and paths | Delete key removes selected anchors or segments | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1659 | Path component duplicate by Alt-drag | behavior | Shapes and paths | Copies path component | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1660 | Transform Path / Free Transform Points | command | Edit menu | Transforms path or selected anchors | core | https://helpx.adobe.com/photoshop/using/editing-paths.html |
| PS-A-1661 | Combine Shapes Unite | command | Properties / Path operations | Merges shapes | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1662 | Combine Shapes Subtract Front | command | Properties / Path operations | Removes front shape area | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1663 | Combine Shapes Intersect | command | Properties / Path operations | Keeps overlapping area | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1664 | Combine Shapes Exclude | command | Properties / Path operations | Removes overlap | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1665 | Merge Shape Components | command | Path operations menu | Permanently merges components | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1666 | Live shape conversion warning | behavior | Shapes and paths | Editing anchors converts live shape to regular path | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1667 | Shape fill gradient options | panel-option | Properties panel | Gradient style, angle, scale, reverse, dither for shape fill | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-1668 | Shape fill pattern options | panel-option | Properties panel | Pattern scale and angle | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-1669 | Stroke presets save | panel-option | Stroke options | Saves custom dashed stroke | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/fill-and-stroke-shapes.html |
| PS-A-1670 | Merge shape layers | command | Layer > Merge Shapes | Merges selected shape layers into one | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1671 | Rasterize shape | command | Layer > Rasterize > Shape | Converts shape to pixels | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1672 | Snap Vector Tools and Transforms to Pixel Grid | behavior | Preferences > Tools | Aligns vector edges to pixel boundaries | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/shape-path-and-pixel-mode-options.html |
| PS-A-1673 | Define Custom Shape from path | command | Edit menu | Saves selected path as shape preset | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/draw-custom-shapes.html |
| PS-A-1674 | Shape Properties Appearance W H X Y | panel-option | Properties panel | Numeric geometry | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |
| PS-A-1675 | Ellipse and triangle live properties | panel-option | Properties panel | Live shape parameters for ellipse, triangle, polygon, line | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/create-shapes/create-shapes.html |

## K01 Rulers, guides, grids, smart guides

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1676 | Rulers (Ctrl+R) | command | View menu | Shows rulers on window edges | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-1677 | Ruler origin drag | behavior | Rulers | Drag ruler corner to set zero point; double-click resets | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-1678 | Ruler units | behavior | Rulers context menu | Pixels, inches, cm, mm, points, picas, percent | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-1679 | New Guide | command | View menu | Adds guide at exact position and orientation with color | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/create-guides.html |
| PS-A-1680 | New Guide Layout | command | View menu | Columns, rows, gutters, margins, center guides, clear existing | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/create-guides.html |
| PS-A-1681 | New Guides From Shape | command | View menu | Creates guides from shape bounds | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/create-guides.html |
| PS-A-1682 | Drag guide from ruler | behavior | Canvas | Drags guides; Alt switches orientation; Shift snaps to ruler ticks | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/create-guides.html |
| PS-A-1683 | Move guide | behavior | Canvas | Move tool drags guide | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/move-guides.html |
| PS-A-1684 | Edit guide by double-click | behavior | Canvas | Opens guide edit dialog with position and color | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/edit-guides.html |
| PS-A-1685 | Lock Guides (Alt+Ctrl+;) | command | View menu | Prevents guide movement | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/edit-guides.html |
| PS-A-1686 | Clear Guides / Clear Selected Artboard Guides / Clear Canvas Guides | command | View menu | Removes guides | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/remove-guides.html |
| PS-A-1687 | Guide color per guide | behavior | Guide dialog | Individual guide colors | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/edit-guides.html |
| PS-A-1688 | Guides on artboards | behavior | Artboards | Guides scoped to artboard or canvas | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/edit-guides.html |
| PS-A-1689 | Show Guides (Ctrl+;) | command | View > Show | Toggles guides | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/show-or-hide-guides-grids-and-smart-guides.html |
| PS-A-1690 | Show Grid (Ctrl+') | command | View > Show | Toggles grid | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/show-or-hide-guides-grids-and-smart-guides.html |
| PS-A-1691 | Show Smart Guides | command | View > Show | Toggles smart guides | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/work-efficiently-with-smart-guides.html |
| PS-A-1692 | Smart Guides alignment and distance | behavior | Canvas | Temporary guides show alignment and spacing between layers | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/work-efficiently-with-smart-guides.html |
| PS-A-1693 | Smart Guides color preference | behavior | Preferences > Guides, Grid and Slices | Smart guide color | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/set-guide-and-grid-preferences.html |
| PS-A-1694 | Guide color and style preference | behavior | Preferences > Guides, Grid and Slices | Canvas and artboard guide color and style Lines or Dashed | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/set-guide-and-grid-preferences.html |
| PS-A-1695 | Grid color, style, gridline every, subdivisions | behavior | Preferences > Guides, Grid and Slices | Grid appearance | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/set-guide-and-grid-preferences.html |
| PS-A-1696 | Slice line color and show numbers | behavior | Preferences > Guides, Grid and Slices | Slice display | format | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/set-guide-and-grid-preferences.html |
| PS-A-1697 | Path options color and thickness | behavior | Preferences > Guides, Grid and Slices | Path display | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/set-guide-and-grid-preferences.html |
| PS-A-1698 | Control on-canvas widgets | behavior | Preferences > Guides, Grid and Slices | Controls size of on-canvas widgets | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/set-guide-and-grid-preferences.html |
| PS-A-1699 | Pixel Grid | command | View > Show | Grid of pixels at high zoom | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1700 | Snap (Shift+Ctrl+;) | command | View menu | Global snapping toggle | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/overview-of-guides-grids-and-smart-guides.html |
| PS-A-1701 | Snap To Guides | command | View > Snap To | Snap to guides | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/overview-of-guides-grids-and-smart-guides.html |
| PS-A-1702 | Snap To Grid | command | View > Snap To | Snap to grid | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/overview-of-guides-grids-and-smart-guides.html |
| PS-A-1703 | Snap To Layers | command | View > Snap To | Snap to layer edges | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/overview-of-guides-grids-and-smart-guides.html |
| PS-A-1704 | Snap To Slices | command | View > Snap To | Snap to slices | format | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/overview-of-guides-grids-and-smart-guides.html |
| PS-A-1705 | Snap To Document Bounds | command | View > Snap To | Snap to canvas edges | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/overview-of-guides-grids-and-smart-guides.html |
| PS-A-1706 | Snap To All / None | command | View > Snap To | Toggle all snap targets | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/overview-of-guides-grids-and-smart-guides.html |
| PS-A-1707 | Snap to pixel for vectors | behavior | View menu | Vector snapping to whole pixels | core | https://helpx.adobe.com/photoshop/desktop/draw-shapes-paths/draw-lines-curves/shape-path-and-pixel-mode-options.html |

## K02 View menu

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-A-1708 | Proof Setup | command | View menu | Soft-proof conditions: Custom, Working CMYK, plates, Macintosh RGB, Windows RGB, Monitor RGB, color blindness | print | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1709 | Proof Colors (Ctrl+Y) | command | View menu | Soft proof toggle | print | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1710 | Gamut Warning (Shift+Ctrl+Y) | command | View menu | Highlights out-of-gamut colors | print | https://helpx.adobe.com/photoshop/desktop/adjust-color/choose-colors/choose-a-cmyk-equivalent-for-a-non-printable-color.html |
| PS-A-1711 | Pixel Aspect Ratio | command | View menu | Non-square pixel preview options | video | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1712 | Pixel Aspect Ratio Correction | command | View menu | Previews non-square pixels corrected | video | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1713 | 32-bit Preview Options | command | View menu | Exposure and Gamma or Highlight Compression preview for HDR | core | https://helpx.adobe.com/photoshop/using/bit-depth.html |
| PS-A-1714 | Zoom In (Ctrl+plus) | command | View menu | Zooms in | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1715 | Zoom Out (Ctrl+minus) | command | View menu | Zooms out | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1716 | Fit on Screen (Ctrl+0) | command | View menu | Fits image in window | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1717 | Fit Artboard on Screen | command | View menu | Fits active artboard | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/layout-design-tools/get-started-artboards.html |
| PS-A-1718 | 100% (Ctrl+1) | command | View menu | Actual pixels | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1719 | 200% | command | View menu | Double zoom | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1720 | Print Size | command | View menu | Approximate print size display | print | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1721 | Actual Size | command | View menu | Physical size based on screen resolution | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1722 | Flip Horizontal (view) | command | View menu | Mirrors display without changing pixels | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1723 | Pattern Preview (view) | command | View menu | Tiled preview | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/create-fill-with-patterns/pattern-preview-best-practices.html |
| PS-A-1724 | Screen Mode Standard / Full with Menu Bar / Full Screen | command | View menu | Window chrome modes | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1725 | Extras (Ctrl+H) | command | View menu | Toggles all enabled extras | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1726 | Show > Layer Edges | command | View menu | Outline of layer content | core | https://helpx.adobe.com/photoshop/desktop/create-manage-layers/transform-manipulate-layers/display-layer-edges-and-handles.html |
| PS-A-1727 | Show > Selection Edges | command | View menu | Marching ants toggle | core | https://helpx.adobe.com/photoshop/desktop/make-selections/refine-modify-selections/hide-or-show-selection-edges.html |
| PS-A-1728 | Show > Target Path | command | View menu | Path display toggle | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1729 | Show > Grid / Guides / Canvas Guides / Artboard Guides / Artboard Names | command | View menu | Guide and label display toggles | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/show-or-hide-guides-grids-and-smart-guides.html |
| PS-A-1730 | Show > Count | command | View menu | Count markers display | core | https://helpx.adobe.com/photoshop/using/counting-objects-image.html |
| PS-A-1731 | Show > Smart Guides | command | View menu | Smart guides toggle | core | https://helpx.adobe.com/photoshop/desktop/use-grids-measurement-guides/alignment-grids-guides/work-efficiently-with-smart-guides.html |
| PS-A-1732 | Show > Slices | command | View menu | Slice display | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-1733 | Show > Notes | command | View menu | Note icons display | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1734 | Show > Pixel Grid | command | View menu | Pixel grid display | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1735 | Show > 3D | command | View menu | Legacy 3D overlays | 3d | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1736 | Show > Brush Preview | command | View menu | Bristle brush preview | core | https://helpx.adobe.com/photoshop/desktop/apply-painting-techniques/brushes-presets/display-brush-panel-brush-options.html |
| PS-A-1737 | Show > Mesh | command | View menu | Puppet warp mesh | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1738 | Show > Edit Pins | command | View menu | Puppet warp pins | core | https://helpx.adobe.com/photoshop/desktop/effects-filters/artistic-stylize-filters/distort-specific-image-areas-with-puppet-warp.html |
| PS-A-1739 | Show > Copy/Paste Guides and other extras | command | View menu | Additional extras toggles | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1740 | Show > All / None / Show Extras Options | command | View menu | Configure which extras display | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1741 | Rulers (View) | command | View menu | Ruler toggle | core | https://helpx.adobe.com/photoshop/using/rulers.html |
| PS-A-1742 | Lock Slices / Clear Slices | command | View menu | Slice management | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-A-1743 | Window > Arrange | command | Window menu | Tile, Consolidate, Float, Match Zoom, Location, Rotation, New Window for document | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/rearrange-document-windows.html |
| PS-A-1744 | New Window for document | command | Window > Arrange | Second view of same document | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/rearrange-document-windows.html |
| PS-A-1745 | Match Zoom and Location | command | Window > Arrange | Syncs views across documents | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/rearrange-document-windows.html |
| PS-A-1746 | Document tabs | behavior | Workspace | Tabbed documents with drag to float | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/rearrange-document-windows.html |
| PS-A-1747 | Status bar information | behavior | Document window | Doc sizes, profile, dimensions, scratch sizes, efficiency, timing, current tool, 32-bit exposure, save progress, smart objects, layer count | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/workspace-overview.html |
| PS-A-1748 | Zoom level field | behavior | Document window status bar | Type zoom percent | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-A-1749 | Precise cursor and brush preview on canvas | behavior | Canvas | Visual brush outline follows pointer | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/change-tool-pointers.html |
| PS-A-1750 | GPU canvas rendering | behavior | Preferences > Performance | OpenGL/GPU drawing for smooth zoom and rotate | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |

## Row counts per area

| Area | Rows |
|---|---|
| A01 Toolbar framework and general tool behavior | 32 |
| A02 Move tool | 23 |
| A03 Artboard tool | 9 |
| A04 Marquee tools | 18 |
| A05 Lasso tools | 14 |
| A06 Object Selection tool | 14 |
| A07 Quick Selection tool | 7 |
| A08 Magic Wand tool | 7 |
| A09 Selection Brush tool | 7 |
| A10 Crop and Perspective Crop tools | 31 |
| A11 Slice tools | 11 |
| A12 Frame tool | 9 |
| A13 Eyedropper family | 29 |
| A14 Healing and removal tools | 52 |
| A15 Brush and painting tools | 44 |
| A16 Clone and pattern stamp | 21 |
| A17 History brushes | 6 |
| A18 Eraser tools | 11 |
| A19 Gradient and Paint Bucket | 37 |
| A20 Blur, Sharpen, Smudge, Dodge, Burn, Sponge | 21 |
| A21 Pen and path tools | 29 |
| A22 Type tools | 21 |
| A23 Shape tools | 26 |
| A24 Navigation tools | 20 |
| B01 Select menu | 31 |
| B02 Selection behaviors and edit commands | 18 |
| B03 Select and Mask workspace | 46 |
| B04 Color Range dialog | 14 |
| B05 Focus Area dialog | 7 |
| B06 Quick Mask and channel selections | 9 |
| C01 Layer menu commands | 58 |
| C02 Layer types | 16 |
| C03 Smart Objects | 38 |
| C04 Masks and clipping | 22 |
| C05 Layers panel | 49 |
| C06 Layer Properties / Blending Options dialog | 13 |
| C07 Blend modes | 33 |
| C08 Layer styles | 76 |
| C09 Layer comps | 11 |
| C10 Align, distribute, auto-align, auto-blend | 18 |
| C11 Artboards | 10 |
| D01 Adjustments panel and framework | 16 |
| D02 Brightness/Contrast and Light | 13 |
| D03 Levels | 12 |
| D04 Curves | 18 |
| D05 Exposure, Vibrance, Color and vibrance | 20 |
| D06 Hue/Saturation | 10 |
| D07 Color Balance, Black and White, Photo Filter | 15 |
| D08 Channel Mixer and Color Lookup | 14 |
| D09 Invert, Posterize, Threshold, Gradient Map, Selective Color | 14 |
| D10 Shadows/Highlights and HDR Toning | 16 |
| D11 Desaturate, Match Color, Replace Color, Equalize | 15 |
| D12 Auto adjustments | 3 |
| E01 Image > Mode | 31 |
| E02 Image Size and Canvas Size | 24 |
| E03 Rotation, crop, trim, reveal | 11 |
| E04 Apply Image and Calculations | 11 |
| E05 Variables and data sets | 5 |
| E06 Analysis and measurement | 7 |
| F01 Edit menu general | 32 |
| F02 Fill and Stroke dialogs | 15 |
| F03 Content-Aware Fill workspace | 16 |
| F04 Content-Aware Scale | 5 |
| F05 Puppet Warp | 8 |
| F06 Perspective Warp | 7 |
| F07 Free Transform and Warp | 35 |
| G01 Brush Settings panel | 53 |
| G02 Brushes panel and presets | 16 |
| G03 Symmetry painting | 14 |
| G04 Color panels | 28 |
| G05 Other retouching features | 7 |
| H01 Channels panel | 21 |
| H02 Paths panel | 16 |
| H03 History panel | 17 |
| H04 Properties panel and Contextual Task Bar | 20 |
| I01 Character panel | 36 |
| I02 Paragraph panel | 19 |
| I03 Character and Paragraph styles | 6 |
| I04 OpenType, variable fonts, glyphs | 15 |
| I05 Type menu and text commands | 25 |
| I06 Type on path, warp text, Dynamic Text | 18 |
| J01 Shapes and path editing | 23 |
| K01 Rulers, guides, grids, smart guides | 32 |
| K02 View menu | 43 |
| TOTAL | 1750 |

## Adobe Photoshop feature inventory, part 2 of 2 (for Gesso parity)

- Product: Adobe Photoshop on desktop (Photoshop 2026 release line)
- Current version: 27.10, released August 2026 (release notes page last updated Aug 28, 2026). No September 2026 release is listed as of 2026-09-26. The current LTS build is 26.11.7.
- Camera Raw version covered: 18.6 (August 2026)
- Compiled: 2026-09-26
- Scope: part 2. It covers the Filter menu with every filter and option, Camera Raw Filter, Neural Filters, generative and AI features, automation, video and animation, legacy 3D (marked removed), File menu, file formats, print and proofing, Color Settings, Assign and Convert Profile, keyboard shortcuts, the toolbar, presets, Preferences, workspace and UI, cloud, and the Help menu. Part 1 covers tools, selections, layers, adjustments, painting, type, shapes and the Edit, Image and View menus. Some rows overlap part 1 where this scope names them, such as Content-Aware Fill and Sky Replacement.

## Primary sources

- Photoshop User Guide: https://helpx.adobe.com/photoshop/user-guide.html
- Release notes: https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html
- What's new: https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html
- Generative AI overview: https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html
- Filter effects reference: https://helpx.adobe.com/photoshop/using/filter-effects-reference.html
- Neural Filters list: https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html
- Preferences: https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html
- Camera Raw user guide: https://helpx.adobe.com/camera-raw/user-guide.html
- Camera Raw what's new: https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html
- CG Channel release coverage for 27.0 to 27.8 (see the Source column)

## Method notes

- helpx.adobe.com blocks WebFetch and curl, so pages were read in a real Chrome session. Seven pages were read in full this way: release notes, What's new, Generative AI overview, Filter effects reference, Neural Filters list, Preferences, and Camera Raw what's new. WebSearch covered release-level details for 27.0 to 27.8.
- Rows outside those pages come from long-standing, documented Photoshop behavior and dialog layouts. Their Source cells use the matching legacy User Guide URL (helpx.adobe.com/photoshop/using/...). These URLs redirect to the new /photoshop/desktop/ help tree, but not every one was opened on its own. Check option wording against the running app before treating a row as a spec.
- The Preferences category list matches the Jul 2026 help page: General, Interface, Workspace, Notifications, Tools, History & Content Credentials, File Handling, Export, Performance, Image Processing, Scratch Disks, Cursors, Transparency & Gamut, Units & Rulers, Guides, Grid & Slices, Plug-ins, Type, Enhanced Controls, Technology Previews. The 3D category was removed with 3D. Product Improvement is listed under General. The individual options inside each category are not listed on that page and come from product knowledge. The contents of Notifications and Enhanced Controls are not documented in detail.
- Removed features, such as legacy 3D and Digimarc, are included and marked removed so Gesso can skip them on purpose.
- Kind values: tool, command, panel, panel-option, filter, filter-option, dialog-option, format, format-option, preference, behavior. Category values: core, ai, cloud, automation, video, 3d, print, format.

## Filter menu: top level, Smart Filters and Filter Gallery

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0001 | Last Filter | command | Filter menu | Reapplies the most recently used filter with its last settings (Ctrl+Alt+F reopens its dialog) | core | https://helpx.adobe.com/photoshop/using/filter-basics.html |
| PS-B-0002 | Convert for Smart Filters | command | Filter menu | Converts the active layer(s) to a Smart Object so filters are applied non-destructively | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0003 | Filter Gallery | command | Filter > Filter Gallery | Opens the Filter Gallery dialog with Artistic, Brush Strokes, Distort, Sketch, Stylize and Texture filters and stackable effect layers | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0004 | Adaptive Wide Angle | command | Filter > Adaptive Wide Angle | Straightens lines bent by wide-angle and fisheye lenses using constraints | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0005 | Camera Raw Filter | command | Filter > Camera Raw Filter | Applies Adobe Camera Raw processing to a pixel or Smart Object layer | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0006 | Lens Correction | command | Filter > Lens Correction | Corrects distortion, chromatic aberration and vignetting with lens profiles or manual controls | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0007 | Liquify | command | Filter > Liquify | Pushes, pulls, rotates, reflects, puckers and bloats pixels with brush tools and face-aware controls | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0008 | Neural Filters | command | Filter > Neural Filters | Opens the Neural Filters workspace with machine-learning filters | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0009 | Vanishing Point | command | Filter > Vanishing Point | Edits with perspective-correct cloning, painting and pasting on defined planes | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0010 | Browse Filters Online | command | Filter > Browse Filters Online | Opens Adobe Exchange to find additional filter plug-ins | core | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0011 | Filter bit-depth support | behavior | Filter menu | Only a subset of filters run in 16-bit and 32-bit documents; others are dimmed | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0012 | Filter unavailable in Bitmap and Indexed modes | behavior | Filter menu | Filters cannot be applied to Bitmap or Indexed Color images | core | https://helpx.adobe.com/photoshop/using/filter-basics.html |
| PS-B-0013 | Filter applies to selection or layer | behavior | Filter menu | Filters affect the active selection or, with none, the whole active layer or channel | core | https://helpx.adobe.com/photoshop/using/filter-basics.html |
| PS-B-0014 | Filter preview in dialog | behavior | Filter dialogs | Most filter dialogs show a zoomable preview (plus and minus buttons) and a Preview checkbox for on-canvas preview | core | https://helpx.adobe.com/photoshop/using/filter-basics.html |
| PS-B-0015 | Filter progress and cancel | behavior | Filter menu | Long-running filters show a progress bar and can be cancelled with Esc | core | https://helpx.adobe.com/photoshop/using/filter-basics.html |
| PS-B-0016 | Alt resets filter dialog | behavior | Filter dialogs | Holding Alt turns Cancel into Reset to restore dialog defaults | core | https://helpx.adobe.com/photoshop/using/filter-basics.html |
| PS-B-0017 | Fade filter | command | Edit > Fade | Edit > Fade changes opacity and blending mode of the last filter, painting or adjustment | core | https://helpx.adobe.com/photoshop/using/filter-basics.html |
| PS-B-0018 | Filters on Smart Object layers become Smart Filters | behavior | Layers panel | Applying a filter to a Smart Object adds it as a re-editable Smart Filter beneath the layer | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0019 | Smart Filter mask | panel-option | Layers panel | Each Smart Object gets one shared filter mask that restricts all Smart Filters | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0020 | Smart Filter blending options | panel-option | Layers panel | Double-clicking the sliders icon sets per-filter mode and opacity | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0021 | Smart Filter reorder | panel-option | Layers panel | Dragging Smart Filters in the list changes their stacking order | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0022 | Smart Filter visibility toggle | panel-option | Layers panel | Eye icons hide individual Smart Filters or all of them at once | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0023 | Edit Smart Filter | panel-option | Layers panel | Double-clicking a Smart Filter reopens its dialog with its saved settings | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0024 | Copy Smart Filters between layers | panel-option | Layers panel | Alt-dragging a Smart Filter or the Smart Filters heading copies it to another Smart Object | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0025 | Disable Filter Mask | command | Layer > Smart Filter | Turns off the Smart Filter mask without deleting it | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0026 | Delete Filter Mask | command | Layer > Smart Filter | Removes the Smart Filter mask | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0027 | Disable Smart Filters | command | Layer > Smart Filter | Hides all Smart Filters on the layer | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0028 | Clear Smart Filters | command | Layer > Smart Filter | Deletes all Smart Filters from the layer | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0029 | Smart Filters rasterize on Rasterize | behavior | Layers panel | Rasterizing a Smart Object bakes its Smart Filters into pixels | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0030 | Smart Filter unsupported filters | behavior | Filter menu | Filters such as Vanishing Point historically could not run as Smart Filters and require a pixel layer | core | https://helpx.adobe.com/photoshop/using/applying-smart-filters.html |
| PS-B-0031 | Filter Gallery preview pane | dialog-option | Filter > Filter Gallery | Large zoomable preview of the stacked effect | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0032 | Filter Gallery category folders | dialog-option | Filter > Filter Gallery | Expandable categories with thumbnail swatches of each filter | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0033 | Show or hide thumbnails | dialog-option | Filter > Filter Gallery | Toggle collapses the thumbnail browser to enlarge the preview | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0034 | Filter pop-up menu | dialog-option | Filter > Filter Gallery | Alphabetical menu of all gallery filters as an alternative to thumbnails | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0035 | Effect layers list | dialog-option | Filter > Filter Gallery | Stack of applied effects that can be reordered, hidden and deleted | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0036 | New effect layer | dialog-option | Filter > Filter Gallery | Adds a copy of the selected effect so multiple gallery filters stack | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0037 | Delete effect layer | dialog-option | Filter > Filter Gallery | Removes the selected effect from the stack | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0038 | Effect layer reorder | dialog-option | Filter > Filter Gallery | Dragging effect layers changes the order filters are applied | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0039 | Effect layer visibility | dialog-option | Filter > Filter Gallery | Eye icon hides an effect layer from the result | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0040 | Zoom menu | dialog-option | Filter > Filter Gallery | Preset zoom levels including Fit in View and Actual Pixels | core | https://helpx.adobe.com/photoshop/using/filter-basics.html#filter_gallery_overview |
| PS-B-0041 | Colored Pencil | filter | Filter > Filter Gallery | Artistic: redraws the image as colored pencil strokes on a solid paper color | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0042 | Colored Pencil: Pencil Width, Stroke Pressure, Paper Brightness | filter-option | Filter > Filter Gallery | Controls stroke width, stroke strength and paper brightness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0043 | Cutout | filter | Filter > Filter Gallery | Artistic: builds the image from roughly cut pieces of colored paper | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0044 | Cutout: Number of Levels, Edge Simplicity, Edge Fidelity | filter-option | Filter > Filter Gallery | Controls color level count and edge simplification | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0045 | Dry Brush | filter | Filter > Filter Gallery | Artistic: paints edges with a dry brush and simplifies color areas | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0046 | Dry Brush: Brush Size, Brush Detail, Texture | filter-option | Filter > Filter Gallery | Controls stroke size, retained detail and texture amount | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0047 | Film Grain | filter | Filter > Filter Gallery | Artistic: applies an even grain pattern to shadows and midtones | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0048 | Film Grain: Grain, Highlight Area, Intensity | filter-option | Filter > Filter Gallery | Controls grain amount and highlight treatment | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0049 | Fresco | filter | Filter > Filter Gallery | Artistic: paints with coarse, short, rounded daubs | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0050 | Fresco: Brush Size, Brush Detail, Texture | filter-option | Filter > Filter Gallery | Controls daub size, detail and texture | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0051 | Neon Glow | filter | Filter > Filter Gallery | Artistic: adds colored glows to objects | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0052 | Neon Glow: Glow Size, Glow Brightness, Glow Color | filter-option | Filter > Filter Gallery | Controls glow extent, brightness and color swatch | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0053 | Paint Daubs | filter | Filter > Filter Gallery | Artistic: painterly daubs with selectable brush types | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0054 | Paint Daubs: Brush Size, Sharpness, Brush Type | filter-option | Filter > Filter Gallery | Brush Type choices Simple, Light Rough, Dark Rough, Wide Sharp, Wide Blurry, Sparkle | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0055 | Palette Knife | filter | Filter > Filter Gallery | Artistic: reduces detail to a thinly painted canvas look | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0056 | Palette Knife: Stroke Size, Stroke Detail, Softness | filter-option | Filter > Filter Gallery | Controls stroke size, detail and softness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0057 | Plastic Wrap | filter | Filter > Filter Gallery | Artistic: coats the image in shiny plastic | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0058 | Plastic Wrap: Highlight Strength, Detail, Smoothness | filter-option | Filter > Filter Gallery | Controls highlight intensity and surface detail | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0059 | Poster Edges | filter | Filter > Filter Gallery | Artistic: posterizes and draws black lines on edges | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0060 | Poster Edges: Edge Thickness, Edge Intensity, Posterization | filter-option | Filter > Filter Gallery | Controls edge line thickness, darkness and levels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0061 | Rough Pastels | filter | Filter > Filter Gallery | Artistic: pastel chalk strokes over a texture | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0062 | Rough Pastels: Stroke Length, Stroke Detail, Texture, Scaling, Relief, Light, Invert | filter-option | Filter > Filter Gallery | Texture choices Brick, Burlap, Canvas, Sandstone or Load Texture with light direction | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0063 | Smudge Stick | filter | Filter > Filter Gallery | Artistic: short diagonal smudging strokes | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0064 | Smudge Stick: Stroke Length, Highlight Area, Intensity | filter-option | Filter > Filter Gallery | Controls stroke length and highlight brightening | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0065 | Sponge | filter | Filter > Filter Gallery | Artistic: textured contrasting color areas like sponge painting | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0066 | Sponge: Brush Size, Definition, Smoothness | filter-option | Filter > Filter Gallery | Controls sponge size and definition | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0067 | Underpainting | filter | Filter > Filter Gallery | Artistic: paints over a textured background | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0068 | Underpainting: Brush Size, Texture Coverage, Texture, Scaling, Relief, Light, Invert | filter-option | Filter > Filter Gallery | Texture and lighting controls shared with Texturizer | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0069 | Watercolor | filter | Filter > Filter Gallery | Artistic: watercolor style with saturated edges | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0070 | Watercolor: Brush Detail, Shadow Intensity, Texture | filter-option | Filter > Filter Gallery | Controls detail, shadow darkness and texture | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0071 | Accented Edges | filter | Filter > Filter Gallery | Brush Strokes: accentuates edges like chalk or ink | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0072 | Accented Edges: Edge Width, Edge Brightness, Smoothness | filter-option | Filter > Filter Gallery | Controls edge accent width and brightness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0073 | Angled Strokes | filter | Filter > Filter Gallery | Brush Strokes: diagonal strokes in opposite directions for lights and darks | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0074 | Angled Strokes: Direction Balance, Stroke Length, Sharpness | filter-option | Filter > Filter Gallery | Controls stroke direction mix, length and sharpness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0075 | Crosshatch | filter | Filter > Filter Gallery | Brush Strokes: pencil hatching texture | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0076 | Crosshatch: Stroke Length, Sharpness, Strength | filter-option | Filter > Filter Gallery | Strength 1 to 3 sets hatching passes | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0077 | Dark Strokes | filter | Filter > Filter Gallery | Brush Strokes: dark short strokes in shadows, long white strokes in lights | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0078 | Dark Strokes: Balance, Black Intensity, White Intensity | filter-option | Filter > Filter Gallery | Controls stroke balance and intensities | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0079 | Ink Outlines | filter | Filter > Filter Gallery | Brush Strokes: pen and ink outline style | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0080 | Ink Outlines: Stroke Length, Dark Intensity, Light Intensity | filter-option | Filter > Filter Gallery | Controls line length and tonal intensity | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0081 | Spatter | filter | Filter > Filter Gallery | Brush Strokes: spatter airbrush effect | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0082 | Spatter: Spray Radius, Smoothness | filter-option | Filter > Filter Gallery | Controls spray spread and smoothness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0083 | Sprayed Strokes | filter | Filter > Filter Gallery | Brush Strokes: angled sprayed strokes in dominant colors | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0084 | Sprayed Strokes: Stroke Length, Spray Radius, Stroke Direction | filter-option | Filter > Filter Gallery | Direction choices Right Diagonal, Horizontal, Left Diagonal, Vertical | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0085 | Sumi-e | filter | Filter > Filter Gallery | Brush Strokes: Japanese ink on rice paper look | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0086 | Sumi-e: Stroke Width, Stroke Pressure, Contrast | filter-option | Filter > Filter Gallery | Controls stroke width, pressure and contrast | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0087 | Diffuse Glow | filter | Filter > Filter Gallery | Distort (gallery): soft diffusion glow with white noise | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0088 | Diffuse Glow: Graininess, Glow Amount, Clear Amount | filter-option | Filter > Filter Gallery | Glow uses the background color | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0089 | Glass | filter | Filter > Filter Gallery | Distort (gallery): view through textured glass | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0090 | Glass: Distortion, Smoothness, Texture, Scaling, Invert | filter-option | Filter > Filter Gallery | Texture choices Blocks, Canvas, Frosted, Tiny Lens or Load Texture | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0091 | Ocean Ripple | filter | Filter > Filter Gallery | Distort (gallery): randomly spaced underwater ripples | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0092 | Ocean Ripple: Ripple Size, Ripple Magnitude | filter-option | Filter > Filter Gallery | Controls ripple scale and strength | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0093 | Bas Relief | filter | Filter > Filter Gallery | Sketch: carved low relief using foreground and background colors | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0094 | Bas Relief: Detail, Smoothness, Light | filter-option | Filter > Filter Gallery | Light direction choices from eight directions | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0095 | Chalk and Charcoal | filter | Filter > Filter Gallery | Sketch: chalk highlights and charcoal shadows | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0096 | Chalk and Charcoal: Charcoal Area, Chalk Area, Stroke Pressure | filter-option | Filter > Filter Gallery | Controls area balance and pressure | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0097 | Charcoal | filter | Filter > Filter Gallery | Sketch: posterized smudged charcoal drawing | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0098 | Charcoal: Charcoal Thickness, Detail, Light/Dark Balance | filter-option | Filter > Filter Gallery | Controls stroke thickness and tonal balance | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0099 | Chrome | filter | Filter > Filter Gallery | Sketch: polished chrome surface | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0100 | Chrome: Detail, Smoothness | filter-option | Filter > Filter Gallery | Controls surface detail and smoothness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0101 | Conte Crayon | filter | Filter > Filter Gallery | Sketch: dense Conte crayon texture | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0102 | Conte Crayon: Foreground Level, Background Level, Texture, Scaling, Relief, Light, Invert | filter-option | Filter > Filter Gallery | Tone levels plus texture controls | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0103 | Graphic Pen | filter | Filter > Filter Gallery | Sketch: fine linear ink strokes | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0104 | Graphic Pen: Stroke Length, Light/Dark Balance, Stroke Direction | filter-option | Filter > Filter Gallery | Direction choices Right Diagonal, Horizontal, Left Diagonal, Vertical | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0105 | Halftone Pattern | filter | Filter > Filter Gallery | Sketch: halftone screen with continuous tones | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0106 | Halftone Pattern: Size, Contrast, Pattern Type | filter-option | Filter > Filter Gallery | Pattern Type choices Circle, Dot, Line | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0107 | Note Paper | filter | Filter > Filter Gallery | Sketch: handmade paper look | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0108 | Note Paper: Image Balance, Graininess, Relief | filter-option | Filter > Filter Gallery | Controls tonal balance, grain and relief | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0109 | Photocopy | filter | Filter > Filter Gallery | Sketch: photocopy look | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0110 | Photocopy: Detail, Darkness | filter-option | Filter > Filter Gallery | Controls retained detail and darkness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0111 | Plaster | filter | Filter > Filter Gallery | Sketch: molded 3D plaster | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0112 | Plaster: Image Balance, Smoothness, Light | filter-option | Filter > Filter Gallery | Controls balance, smoothness and light direction | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0113 | Reticulation | filter | Filter > Filter Gallery | Sketch: shrinking film emulsion clumping | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0114 | Reticulation: Density, Foreground Level, Background Level | filter-option | Filter > Filter Gallery | Controls grain density and tone levels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0115 | Stamp | filter | Filter > Filter Gallery | Sketch: rubber or wood stamp look | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0116 | Stamp: Light/Dark Balance, Smoothness | filter-option | Filter > Filter Gallery | Controls tonal balance and smoothness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0117 | Torn Edges | filter | Filter > Filter Gallery | Sketch: ragged torn paper pieces | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0118 | Torn Edges: Image Balance, Smoothness, Contrast | filter-option | Filter > Filter Gallery | Controls balance, smoothness and contrast | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0119 | Water Paper | filter | Filter > Filter Gallery | Sketch: blotchy daubs on damp fibrous paper | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0120 | Water Paper: Fiber Length, Brightness, Contrast | filter-option | Filter > Filter Gallery | Controls fiber length and tonal range | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0121 | Glowing Edges | filter | Filter > Filter Gallery | Stylize (gallery): neon-like glow on color edges | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0122 | Glowing Edges: Edge Width, Edge Brightness, Smoothness | filter-option | Filter > Filter Gallery | Controls glow edge width and brightness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0123 | Craquelure | filter | Filter > Filter Gallery | Texture: fine network of plaster cracks | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0124 | Craquelure: Crack Spacing, Crack Depth, Crack Brightness | filter-option | Filter > Filter Gallery | Controls crack density and appearance | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0125 | Grain | filter | Filter > Filter Gallery | Texture: simulated grain types | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0126 | Grain: Intensity, Contrast, Grain Type | filter-option | Filter > Filter Gallery | Types Regular, Soft, Sprinkles, Clumped, Contrasty, Enlarged, Stippled, Horizontal, Vertical, Speckle | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0127 | Mosaic Tiles | filter | Filter > Filter Gallery | Texture: small tiles with grout | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0128 | Mosaic Tiles: Tile Size, Grout Width, Lighten Grout | filter-option | Filter > Filter Gallery | Controls tile and grout dimensions | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0129 | Patchwork | filter | Filter > Filter Gallery | Texture: squares filled with predominant color and random depth | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0130 | Patchwork: Square Size, Relief | filter-option | Filter > Filter Gallery | Controls square size and relief depth | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0131 | Stained Glass | filter | Filter > Filter Gallery | Texture: single-color cells outlined in foreground color | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0132 | Stained Glass: Cell Size, Border Thickness, Light Intensity | filter-option | Filter > Filter Gallery | Controls cell size, border and center light | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0133 | Texturizer | filter | Filter > Filter Gallery | Texture: applies a chosen or loaded texture | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0134 | Texturizer: Texture, Scaling, Relief, Light, Invert | filter-option | Filter > Filter Gallery | Texture choices Brick, Burlap, Canvas, Sandstone or Load Texture from a PSD | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0135 | Show all Filter Gallery groups and names preference | behavior | Preferences > Plug-ins | Preferences > Plug-ins option lists gallery filters directly in the Filter menu submenus | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |

## Filter submenus: Blur, Blur Gallery, Distort, Noise, Pixelate

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0136 | Average | filter | Filter > Blur | Fills the selection or layer with its average color | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0137 | Blur | filter | Filter > Blur | Light fixed-strength smoothing of hard edges | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0138 | Blur More | filter | Filter > Blur | Fixed blur three to four times stronger than Blur | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0139 | Box Blur | filter | Filter > Blur | Blurs using the average of neighbors in a square kernel | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0140 | Box Blur: Radius | filter-option | Filter > Blur | Size of the averaging box in pixels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0141 | Gaussian Blur | filter | Filter > Blur | Weighted bell-curve blur by an adjustable radius | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0142 | Gaussian Blur: Radius | filter-option | Filter > Blur | Blur radius 0.1 to 1000 pixels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0143 | Live Gaussian Blur preview | behavior | Filter > Blur | Gaussian Blur previews live on canvas while dragging the slider (GPU accelerated) | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0144 | Lens Blur | filter | Filter > Blur | Depth-of-field blur using a depth map, iris shape and specular highlights | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0145 | Lens Blur: Faster or More Accurate preview | filter-option | Filter > Blur | Chooses preview speed versus accuracy | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0146 | Lens Blur: Depth Map Source | filter-option | Filter > Blur | None, Transparency, Layer Mask or an alpha channel supplies depth | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0147 | Lens Blur: Blur Focal Distance | filter-option | Filter > Blur | Depth value that stays in focus; clicking the image sets it | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0148 | Lens Blur: Invert depth map | filter-option | Filter > Blur | Reverses near and far in the depth map | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0149 | Lens Blur: Iris Shape | filter-option | Filter > Blur | Triangle through Octagon aperture shapes | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0150 | Lens Blur: Iris Radius, Blade Curvature, Rotation | filter-option | Filter > Blur | Controls bokeh size, roundness and rotation | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0151 | Lens Blur: Specular Highlights Brightness and Threshold | filter-option | Filter > Blur | Brightens highlights above the threshold into bokeh | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0152 | Lens Blur: Noise Amount, Uniform or Gaussian, Monochromatic | filter-option | Filter > Blur | Adds noise back to blurred areas to match grain | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0153 | Motion Blur | filter | Filter > Blur | Directional blur simulating subject motion | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0154 | Motion Blur: Angle and Distance | filter-option | Filter > Blur | Angle minus 360 to 360 degrees, distance 1 to 2000 pixels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0155 | Radial Blur | filter | Filter > Blur | Spin or zoom camera-style blur | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0156 | Radial Blur: Amount, Spin or Zoom, Quality Draft/Good/Best, Blur Center | filter-option | Filter > Blur | Blur center set by dragging in the preview box | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0157 | Shape Blur | filter | Filter > Blur | Blurs with a custom shape preset as the kernel | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0158 | Shape Blur: Radius and Shape picker | filter-option | Filter > Blur | Selects the kernel shape and its size | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0159 | Smart Blur | filter | Filter > Blur | Precision blur that ignores dissimilar pixels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0160 | Smart Blur: Radius, Threshold, Quality, Mode | filter-option | Filter > Blur | Mode Normal, Edge Only or Overlay Edge | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0161 | Surface Blur | filter | Filter > Blur | Edge-preserving blur for noise and grain | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0162 | Surface Blur: Radius and Threshold | filter-option | Filter > Blur | Threshold limits which tonal differences blur | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0163 | Field Blur | filter | Filter > Blur Gallery | Graduated blur defined by multiple pins each with its own blur amount | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0164 | Iris Blur | filter | Filter > Blur Gallery | Elliptical focus area with adjustable feather and falloff | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0165 | Tilt-Shift | filter | Filter > Blur Gallery | Linear focus band simulating a tilt-shift lens | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0166 | Path Blur | filter | Filter > Blur Gallery | Motion blur along user-drawn curved paths | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0167 | Spin Blur | filter | Filter > Blur Gallery | Rotational blur around one or more elliptical centers | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0168 | Blur pins | filter-option | Filter > Blur Gallery | Click to add pins; each pin holds settings for its blur; Delete removes a pin | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0169 | Blur ring | filter-option | Filter > Blur Gallery | On-canvas ring sets the blur amount for a pin | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0170 | Field Blur: Blur amount per pin | filter-option | Filter > Blur Gallery | Pixel blur amount interpolated between pins | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0171 | Iris Blur: Ellipse handles and roundness | filter-option | Filter > Blur Gallery | Resizes, rotates and squares the focus ellipse | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0172 | Iris Blur: Feather handles | filter-option | Filter > Blur Gallery | Sets where sharpness starts to fall off inside the ellipse | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0173 | Tilt-Shift: Blur | filter-option | Filter > Blur Gallery | Blur amount outside the focus band | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0174 | Tilt-Shift: Distortion | filter-option | Filter > Blur Gallery | Shapes the blur like a lens distortion on the bottom zone | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0175 | Tilt-Shift: Symmetric Distortion | filter-option | Filter > Blur Gallery | Applies distortion to both sides | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0176 | Tilt-Shift: focus and feather lines | filter-option | Filter > Blur Gallery | Solid and dashed lines set sharp band and transition, with rotation | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0177 | Path Blur: Speed | filter-option | Filter > Blur Gallery | Blur amount along the path | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0178 | Path Blur: Taper | filter-option | Filter > Blur Gallery | Fades the blur toward path ends | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0179 | Path Blur: Centered Blur | filter-option | Filter > Blur Gallery | Blurs both directions from each pixel instead of one | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0180 | Path Blur: Basic Blur or Rear Sync Flash | filter-option | Filter > Blur Gallery | Rear Sync Flash simulates a flash fired at the end of exposure | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0181 | Path Blur: Strobe Strength and Strobe Flashes | filter-option | Filter > Blur Gallery | Simulates strobe exposures along the path | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0182 | Path Blur: Edit Blur Shapes | filter-option | Filter > Blur Gallery | Shows red end-point arrows to shape blur direction per path end | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0183 | Path Blur: End point speed | filter-option | Filter > Blur Gallery | Per-end blur amount | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0184 | Spin Blur: Blur Angle | filter-option | Filter > Blur Gallery | Degrees of rotational blur | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0185 | Spin Blur: Strobe Strength, Strobe Flashes, Strobe Duration | filter-option | Filter > Blur Gallery | Simulates strobe exposures during the spin | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0186 | Spin Blur: movable pivot point | filter-option | Filter > Blur Gallery | Alt-drag moves the rotation center off the ellipse center | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0187 | Effects: Light Bokeh | filter-option | Filter > Blur Gallery | Brightens out-of-focus highlights | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0188 | Effects: Bokeh Color | filter-option | Filter > Blur Gallery | Adds color to bokeh highlights | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0189 | Effects: Light Range | filter-option | Filter > Blur Gallery | Tonal range that receives bokeh brightening | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0190 | Motion Effects: Strobe Strength, Strobe Flashes, Strobe Duration | filter-option | Filter > Blur Gallery | Motion strobe controls for Path and Spin blur | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0191 | Noise: Grain, Uniform or Gaussian | filter-option | Filter > Blur Gallery | Restores noise to blurred areas to match original grain | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0192 | Noise: Amount, Size, Roughness, Color, Highlights | filter-option | Filter > Blur Gallery | Controls the added grain characteristics | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0193 | Selection Bleed | filter-option | Filter > Blur Gallery | Controls how much outside-selection pixels blend into the blurred selection | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0194 | Focus | filter-option | Filter > Blur Gallery | Protects the area inside the pin from blur | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0195 | Save Mask to Channels | filter-option | Filter > Blur Gallery | Stores the blur mask as an alpha channel on apply | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0196 | High Quality | filter-option | Filter > Blur Gallery | Produces more accurate bokeh at the cost of speed | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0197 | Preview | filter-option | Filter > Blur Gallery | Toggles on-canvas preview | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0198 | Remove All Pins | filter-option | Filter > Blur Gallery | Clears every pin | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0199 | Blur Gallery as Smart Filter | behavior | Filter > Blur Gallery | All Blur Gallery filters can be applied as re-editable Smart Filters | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0200 | Blur Gallery on video layers | behavior | Filter > Blur Gallery | Blur Gallery can be applied to video Smart Objects | core | https://helpx.adobe.com/photoshop/using/blur-gallery.html |
| PS-B-0201 | Displace | filter | Filter > Distort | Distorts using a PSD displacement map | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0202 | Displace: Horizontal Scale and Vertical Scale | filter-option | Filter > Distort | Displacement strength per axis | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0203 | Displace: Stretch to Fit or Tile | filter-option | Filter > Distort | How a map of different size is applied | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0204 | Displace: Wrap Around or Repeat Edge Pixels | filter-option | Filter > Distort | How undefined areas are filled | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0205 | Pinch | filter | Filter > Distort | Squeezes the selection inward or outward | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0206 | Pinch: Amount | filter-option | Filter > Distort | Minus 100 to 100 percent | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0207 | Polar Coordinates | filter | Filter > Distort | Converts between rectangular and polar coordinates | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0208 | Polar Coordinates: Rectangular to Polar or Polar to Rectangular | filter-option | Filter > Distort | Chooses conversion direction | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0209 | Ripple | filter | Filter > Distort | Pond-like ripple pattern | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0210 | Ripple: Amount and Size | filter-option | Filter > Distort | Size Small, Medium, Large | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0211 | Shear | filter | Filter > Distort | Distorts along a user-drawn curve | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0212 | Shear: curve editor | filter-option | Filter > Distort | Drag points on the line to shape the shear | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0213 | Shear: Wrap Around or Repeat Edge Pixels | filter-option | Filter > Distort | Undefined area handling | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0214 | Spherize | filter | Filter > Distort | Wraps the selection around a sphere | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0215 | Spherize: Amount and Mode | filter-option | Filter > Distort | Mode Normal, Horizontal Only, Vertical Only | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0216 | Twirl | filter | Filter > Distort | Rotates more sharply in the center | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0217 | Twirl: Angle | filter-option | Filter > Distort | Minus 999 to 999 degrees | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0218 | Wave | filter | Filter > Distort | Wave distortion with generators | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0219 | Wave: Number of Generators, Wavelength, Amplitude, Scale | filter-option | Filter > Distort | Min and max values for wavelength and amplitude, horizontal and vertical scale | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0220 | Wave: Type | filter-option | Filter > Distort | Sine, Triangle or Square | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0221 | Wave: Randomize | filter-option | Filter > Distort | Generates new random values | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0222 | Wave: Wrap Around or Repeat Edge Pixels | filter-option | Filter > Distort | Undefined area handling | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0223 | ZigZag | filter | Filter > Distort | Radial zigzag distortion | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0224 | ZigZag: Amount, Ridges, Style | filter-option | Filter > Distort | Style Pond Ripples, Out From Center, Around Center | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0225 | Add Noise | filter | Filter > Noise | Adds random pixels simulating film grain | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0226 | Add Noise: Amount, Uniform or Gaussian, Monochromatic | filter-option | Filter > Noise | Distribution and color control | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0227 | Despeckle | filter | Filter > Noise | Blurs everything except edges to remove noise | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0228 | Dust and Scratches | filter | Filter > Noise | Replaces dissimilar pixels within a radius | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0229 | Dust and Scratches: Radius and Threshold | filter-option | Filter > Noise | Search radius and difference threshold | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0230 | Median | filter | Filter > Noise | Replaces pixels with the median brightness in a radius | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0231 | Median: Radius | filter-option | Filter > Noise | Search radius in pixels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0232 | Reduce Noise | filter | Filter > Noise | Edge-preserving luminance and color noise reduction | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0233 | Reduce Noise: Basic Strength, Preserve Details, Reduce Color Noise, Sharpen Details | filter-option | Filter > Noise | Global noise controls | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0234 | Reduce Noise: Remove JPEG Artifact | filter-option | Filter > Noise | Removes JPEG block and halo artifacts | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0235 | Reduce Noise: Advanced Per Channel | filter-option | Filter > Noise | Strength and Preserve Details per color channel | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0236 | Reduce Noise: Save settings | filter-option | Filter > Noise | Saves named noise reduction settings | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0237 | Color Halftone | filter | Filter > Pixelate | Simulates an enlarged halftone screen per channel | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0238 | Color Halftone: Max Radius and Screen Angles per channel | filter-option | Filter > Pixelate | Dot size and angle for channels 1 to 4 | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0239 | Crystallize | filter | Filter > Pixelate | Clumps pixels into polygon cells | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0240 | Crystallize: Cell Size | filter-option | Filter > Pixelate | Size of cells | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0241 | Facet | filter | Filter > Pixelate | Clumps similar colors into blocks for a hand-painted look | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0242 | Fragment | filter | Filter > Pixelate | Averages four offset copies of the pixels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0243 | Mezzotint | filter | Filter > Pixelate | Random pattern of black and white or saturated dots | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0244 | Mezzotint: Type | filter-option | Filter > Pixelate | Fine, Medium, Grainy, Coarse Dots; Short, Medium, Long Lines; Short, Medium, Long Strokes | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0245 | Mosaic | filter | Filter > Pixelate | Square blocks of averaged color | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0246 | Mosaic: Cell Size | filter-option | Filter > Pixelate | Block size in pixels | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0247 | Pointillize | filter | Filter > Pixelate | Random dots with background-colored canvas | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0248 | Pointillize: Cell Size | filter-option | Filter > Pixelate | Dot size | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |

## Filter submenus: Render, Sharpen, Stylize, Video, Other, 3D (removed)

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0249 | Flame | filter | Filter > Render | Renders procedural flames along a path | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0250 | Flame: Flame Type | filter-option | Filter > Render | One flame along path, multiple flames along path, directional, multiple directions, candle light and custom | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0251 | Flame: Length, Width, Angle, Interval, Adjust interval for loops | filter-option | Filter > Render | Basic flame geometry | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0252 | Flame: Use Custom Color for Flames | filter-option | Filter > Render | Overrides default flame color | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0253 | Flame: Quality | filter-option | Filter > Render | Draft, Low, Medium, High, Fine | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0254 | Flame: Advanced Turbulent, Jag, Opacity, Flame Lines, Bottom Alignment, Flame Style, Flame Shape, Randomize Shapes, Arrangement | filter-option | Filter > Render | Advanced flame shaping controls | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0255 | Picture Frame | filter | Filter > Render | Renders a decorative frame from presets | core | https://helpx.adobe.com/photoshop/using/picture-frames.html |
| PS-B-0256 | Picture Frame: Frame style presets | filter-option | Filter > Render | Dozens of frame designs such as vines, flowers, grids | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0257 | Picture Frame: Vines Color, Margin, Size, Arrangement | filter-option | Filter > Render | Basic frame parameters | core | https://helpx.adobe.com/photoshop/using/picture-frames.html |
| PS-B-0258 | Picture Frame: Flower and Leaf options | filter-option | Filter > Render | Flower, Flower Color, Flower Size, Leaf Type, Leaf Color, Leaf Size | core | https://helpx.adobe.com/photoshop/using/picture-frames.html |
| PS-B-0259 | Picture Frame: Advanced | filter-option | Filter > Render | Number of Lines, Thickness, Angle, Fade, Invert | core | https://helpx.adobe.com/photoshop/using/picture-frames.html |
| PS-B-0260 | Tree | filter | Filter > Render | Renders procedural trees | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0261 | Tree: Base Tree Type | filter-option | Filter > Render | About 34 species presets | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0262 | Tree: Light Direction, Leaves Amount, Leaves Size, Branches Height, Branches Thickness | filter-option | Filter > Render | Basic tree geometry | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0263 | Tree: Default Leaves or Custom Leaf types | filter-option | Filter > Render | Leaf shape selection | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0264 | Tree: Advanced Camera Tilt, Arrangement, Leaves Color, Branch Color, Flat Shading options, Enhance Contrast | filter-option | Filter > Render | Advanced rendering controls | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0265 | Tree: Randomize Shapes | filter-option | Filter > Render | Changes random seed | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0266 | Clouds | filter | Filter > Render | Renders soft clouds between foreground and background colors; Alt for starker clouds | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0267 | Difference Clouds | filter | Filter > Render | Renders clouds blended in Difference mode | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0268 | Fibers | filter | Filter > Render | Renders woven fibers from foreground and background colors | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0269 | Fibers: Variance, Strength, Randomize | filter-option | Filter > Render | Controls streak length, fiber stringiness and seed | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0270 | Lens Flare | filter | Filter > Render | Simulates a bright light refracting in a lens | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0271 | Lens Flare: Brightness and flare center | filter-option | Filter > Render | 10 to 300 percent and click-to-place center | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0272 | Lens Flare: Lens Type | filter-option | Filter > Render | 50-300mm Zoom, 35mm Prime, 105mm Prime, Movie Prime | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0273 | Lighting Effects | filter | Filter > Render | GPU lighting workspace with lights and textures | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0274 | Lighting Effects: Point light | filter-option | Filter > Render | Omni-directional light with radius | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0275 | Lighting Effects: Spot light | filter-option | Filter > Render | Elliptical cone with hotspot and angle | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0276 | Lighting Effects: Infinite light | filter-option | Filter > Render | Directional light like the sun | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0277 | Lighting Effects: Color, Intensity, Hotspot | filter-option | Filter > Render | Light color, strength and spot hotspot size | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0278 | Lighting Effects: Colorize | filter-option | Filter > Render | Tints overall lighting | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0279 | Lighting Effects: Exposure, Gloss, Metallic, Ambience | filter-option | Filter > Render | Surface and ambient properties | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0280 | Lighting Effects: Texture channel, Height | filter-option | Filter > Render | Uses a channel as a bump map with height | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0281 | Lighting Effects: Presets | filter-option | Filter > Render | Built-in presets such as Flashlight, Five Lights Down, Blue Omni, Triple Spotlight, with Save and Delete | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0282 | Lighting Effects: Lights panel | filter-option | Filter > Render | Lists lights with visibility toggles and delete | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0283 | Lighting Effects: on-canvas widgets | filter-option | Filter > Render | Drag to move light, adjust intensity ring and hotspot | core | https://helpx.adobe.com/photoshop/using/apply-lighting-effects.html |
| PS-B-0284 | Shake Reduction | filter | Filter > Sharpen | Estimates camera-shake blur traces and deconvolves them | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0285 | Shake Reduction: Blur Trace Bounds | filter-option | Filter > Sharpen | Estimated blur size in pixels | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0286 | Shake Reduction: Source Noise | filter-option | Filter > Sharpen | Auto, Low, Medium, High | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0287 | Shake Reduction: Smoothing and Artifact Suppression | filter-option | Filter > Sharpen | Controls noise amplification and ringing | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0288 | Shake Reduction: multiple blur traces | filter-option | Filter > Sharpen | Blur Estimation tool defines regions each with its own trace | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0289 | Shake Reduction: Blur Direction tool | filter-option | Filter > Sharpen | Manually draws blur direction and length | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0290 | Shake Reduction: Detail loupe | filter-option | Filter > Sharpen | Magnified preview that can be docked or applied | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0291 | Shake Reduction: Save and load blur trace | filter-option | Filter > Sharpen | Exports traces for reuse | core | https://helpx.adobe.com/photoshop/using/reduce-camera-shake-blurring.html |
| PS-B-0292 | Sharpen | filter | Filter > Sharpen | Fixed mild sharpening | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0293 | Sharpen Edges | filter | Filter > Sharpen | Sharpens only edges without an amount | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0294 | Sharpen More | filter | Filter > Sharpen | Fixed stronger sharpening | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0295 | Smart Sharpen | filter | Filter > Sharpen | Adaptive sharpening with noise and halo reduction | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0296 | Smart Sharpen: Amount, Radius, Reduce Noise | filter-option | Filter > Sharpen | Main sharpening controls | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0297 | Smart Sharpen: Remove | filter-option | Filter > Sharpen | Gaussian Blur, Lens Blur or Motion Blur with Angle | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0298 | Smart Sharpen: Shadows and Highlights | filter-option | Filter > Sharpen | Fade Amount, Tonal Width and Radius per tonal range | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0299 | Smart Sharpen: Presets and Use Legacy | filter-option | Filter > Sharpen | Save presets or revert to legacy algorithm | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0300 | Unsharp Mask | filter | Filter > Sharpen | Classic edge contrast sharpening | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0301 | Unsharp Mask: Amount, Radius, Threshold | filter-option | Filter > Sharpen | Strength, edge width and minimum difference | core | https://helpx.adobe.com/photoshop/using/adjusting-image-sharpness-blur.html |
| PS-B-0302 | Diffuse | filter | Filter > Stylize | Shuffles pixels to soften focus | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0303 | Diffuse: Mode | filter-option | Filter > Stylize | Normal, Darken Only, Lighten Only, Anisotropic | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0304 | Emboss | filter | Filter > Stylize | Raised gray relief traced in original color | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0305 | Emboss: Angle, Height, Amount | filter-option | Filter > Stylize | Light angle, relief height and color percentage | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0306 | Extrude | filter | Filter > Stylize | Extrudes blocks or pyramids | core | https://helpx.adobe.com/photoshop/using/applying-specific-filters.html |
| PS-B-0307 | Extrude: Type, Size, Depth, Random or Level-based, Solid Front Faces, Mask Incomplete Blocks | filter-option | Filter > Stylize | Block or Pyramids geometry options | core | https://helpx.adobe.com/photoshop/using/applying-specific-filters.html |
| PS-B-0308 | Find Edges | filter | Filter > Stylize | Outlines edges with dark lines on white | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0309 | Oil Paint | filter | Filter > Stylize | Painterly oil paint rendering with lighting | core | https://helpx.adobe.com/photoshop/using/oil-paint-filter.html |
| PS-B-0310 | Oil Paint: Stylization, Cleanliness, Scale, Bristle Detail | filter-option | Filter > Stylize | Brush stroke controls | core | https://helpx.adobe.com/photoshop/using/oil-paint-filter.html |
| PS-B-0311 | Oil Paint: Lighting Angle and Shine | filter-option | Filter > Stylize | Directional light over paint relief | core | https://helpx.adobe.com/photoshop/using/oil-paint-filter.html |
| PS-B-0312 | Solarize | filter | Filter > Stylize | Blends negative and positive image | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0313 | Tiles | filter | Filter > Stylize | Breaks image into offset tiles | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0314 | Tiles: Number of Tiles, Maximum Offset, Fill Empty Area With | filter-option | Filter > Stylize | Background, Foreground, Inverse Image, Unaltered Image | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0315 | Trace Contour | filter | Filter > Stylize | Contour lines at a brightness level | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0316 | Trace Contour: Level and Edge Upper or Lower | filter-option | Filter > Stylize | Threshold and side of transition | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0317 | Wind | filter | Filter > Stylize | Horizontal windblown streaks | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0318 | Wind: Method and Direction | filter-option | Filter > Stylize | Wind, Blast, Stagger; From the Right or Left | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0319 | De-Interlace | filter | Filter > Video | Removes odd or even interlaced lines | video | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0320 | De-Interlace: Eliminate and Create New Fields By | filter-option | Filter > Video | Odd or Even Fields; Duplication or Interpolation | video | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0321 | NTSC Colors | filter | Filter > Video | Restricts colors to the broadcast-safe NTSC gamut | video | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0322 | Custom | filter | Filter > Other | User-defined 5x5 convolution kernel | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0323 | Custom: kernel grid, Scale, Offset, Load, Save | filter-option | Filter > Other | Defines weights, divisor and brightness offset | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0324 | High Pass | filter | Filter > Other | Keeps edge detail within a radius and suppresses low frequencies | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0325 | High Pass: Radius | filter-option | Filter > Other | Radius from 0.1 pixel | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0326 | HSB/HSL | filter | Filter > Other | Converts RGB channel data to HSB or HSL encoding and back | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0327 | HSB/HSL: Input Mode and Row Order | filter-option | Filter > Other | RGB, HSB, HSL input and output selection | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0328 | Maximum | filter | Filter > Other | Dilates light areas (spreads white) | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0329 | Maximum: Radius and Preserve | filter-option | Filter > Other | Preserve Squareness or Roundness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0330 | Minimum | filter | Filter > Other | Erodes light areas (spreads black) | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0331 | Minimum: Radius and Preserve | filter-option | Filter > Other | Preserve Squareness or Roundness | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0332 | Offset | filter | Filter > Other | Shifts the layer by pixel amounts | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0333 | Offset: Horizontal, Vertical, Undefined Areas | filter-option | Filter > Other | Set to Transparent or Background, Repeat Edge Pixels, Wrap Around | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0334 | Digimarc watermark filters (removed) | behavior | Filter > Digimarc | Legacy Digimarc Embed and Read Watermark plug-ins are unsupported in 64-bit builds | core | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0335 | Generate Normal Map | filter | Filter > 3D | Legacy 3D filter that built normal maps from images; removed with 3D in 2024 | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |
| PS-B-0336 | Generate Bump Map | filter | Filter > 3D | Legacy 3D filter that built bump maps from images; removed with 3D in 2024 | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |

## Adaptive Wide Angle, Lens Correction, Liquify, Vanishing Point

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0337 | AWA Constraint tool | tool | Filter > Adaptive Wide Angle | Click two points along a curved line to straighten it | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0338 | AWA Polygon Constraint tool | tool | Filter > Adaptive Wide Angle | Draws polygon constraints that straighten edges of an area | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0339 | AWA Move tool | tool | Filter > Adaptive Wide Angle | Moves the content within the canvas | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0340 | AWA Hand tool | tool | Filter > Adaptive Wide Angle | Pans the preview | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0341 | AWA Zoom tool | tool | Filter > Adaptive Wide Angle | Zooms the preview | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0342 | AWA Correction: Fisheye | filter-option | Filter > Adaptive Wide Angle | Corrects extreme fisheye curvature | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0343 | AWA Correction: Perspective | filter-option | Filter > Adaptive Wide Angle | Corrects lines converging from angle of view and camera tilt | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0344 | AWA Correction: Auto | filter-option | Filter > Adaptive Wide Angle | Detects correction from lens profile metadata | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0345 | AWA Correction: Full Spherical | filter-option | Filter > Adaptive Wide Angle | Corrects 360 degree equirectangular panoramas with 1:2 aspect | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0346 | AWA Scale | filter-option | Filter > Adaptive Wide Angle | Scales image to minimize blank areas after correction | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0347 | AWA Focal Length and Crop Factor | filter-option | Filter > Adaptive Wide Angle | Lens focal length and sensor crop factor for the model | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0348 | AWA As Shot | filter-option | Filter > Adaptive Wide Angle | Uses values from the lens profile | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0349 | AWA Constraint orientation | filter-option | Filter > Adaptive Wide Angle | Shift-click constraints become horizontal or vertical; right-click sets orientation | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0350 | AWA Detail loupe | filter-option | Filter > Adaptive Wide Angle | Magnified view under the cursor for precise constraint placement | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0351 | AWA Show Constraints, Show Mesh | filter-option | Filter > Adaptive Wide Angle | Toggles overlays | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0352 | AWA Save and Load constraints | filter-option | Filter > Adaptive Wide Angle | Stores constraints to a file for reuse | core | https://helpx.adobe.com/photoshop/using/adaptive-wide-angle-filter.html |
| PS-B-0353 | Lens Correction: Auto Correction tab | filter-option | Filter > Lens Correction | Profile-based automatic corrections | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0354 | Auto Correction: Geometric Distortion | filter-option | Filter > Lens Correction | Corrects barrel and pincushion from profile | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0355 | Auto Correction: Chromatic Aberration | filter-option | Filter > Lens Correction | Removes color fringes from profile | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0356 | Auto Correction: Vignette | filter-option | Filter > Lens Correction | Removes lens vignette from profile | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0357 | Auto Correction: Auto Scale Image | filter-option | Filter > Lens Correction | Scales to hide undefined areas | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0358 | Auto Correction: Edge | filter-option | Filter > Lens Correction | Edge Extension, Transparency, Black Color, White Color fill | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0359 | Auto Correction: Search Criteria | filter-option | Filter > Lens Correction | Camera Make, Camera Model, Lens Model filters for profiles | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0360 | Auto Correction: Lens Profiles list | filter-option | Filter > Lens Correction | Selects matching lens profile; Search Online for profiles | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0361 | Lens Correction: Custom tab | filter-option | Filter > Lens Correction | Manual correction controls | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0362 | Custom: Remove Distortion | filter-option | Filter > Lens Correction | Barrel and pincushion slider | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0363 | Custom: Fix Red/Cyan, Green/Magenta, Blue/Yellow Fringe | filter-option | Filter > Lens Correction | Manual chromatic aberration sliders | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0364 | Custom: Vignette Amount and Midpoint | filter-option | Filter > Lens Correction | Manual vignette correction | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0365 | Custom: Vertical and Horizontal Perspective | filter-option | Filter > Lens Correction | Keystone correction sliders | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0366 | Custom: Angle | filter-option | Filter > Lens Correction | Rotation correction | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0367 | Custom: Scale | filter-option | Filter > Lens Correction | Scale up or down after correction | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0368 | Custom: Settings menu | filter-option | Filter > Lens Correction | Lens Default, Previous Correction, Custom, Save and Load settings | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0369 | Lens Correction: Remove Distortion tool | tool | Filter > Lens Correction | Drag toward or away from center to correct distortion | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0370 | Lens Correction: Straighten tool | tool | Filter > Lens Correction | Draw a line to set horizon or vertical | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0371 | Lens Correction: Move Grid tool | tool | Filter > Lens Correction | Aligns the grid overlay | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0372 | Lens Correction: Show Grid, Size, Color | filter-option | Filter > Lens Correction | Grid overlay settings | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0373 | Lens Correction: Preview | filter-option | Filter > Lens Correction | Toggles preview | core | https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html |
| PS-B-0374 | Forward Warp tool | tool | Filter > Liquify | Pushes pixels forward as you drag | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0375 | Reconstruct tool | tool | Filter > Liquify | Reverses distortion where you paint | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0376 | Smooth tool | tool | Filter > Liquify | Smooths jagged distortion | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0377 | Twirl Clockwise tool | tool | Filter > Liquify | Rotates pixels clockwise; Alt for counterclockwise | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0378 | Pucker tool | tool | Filter > Liquify | Moves pixels toward the brush center | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0379 | Bloat tool | tool | Filter > Liquify | Moves pixels away from the brush center | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0380 | Push Left tool | tool | Filter > Liquify | Moves pixels left when dragging up; Alt reverses | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0381 | Freeze Mask tool | tool | Filter > Liquify | Paints a mask that protects areas from distortion | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0382 | Thaw Mask tool | tool | Filter > Liquify | Erases the freeze mask | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0383 | Face tool | tool | Filter > Liquify | Shows on-canvas handles on detected faces for direct adjustment | core | https://helpx.adobe.com/photoshop/using/face-aware-liquify.html |
| PS-B-0384 | Liquify Hand and Zoom tools | tool | Filter > Liquify | Navigation within the dialog | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0385 | Brush Tool Options: Size | filter-option | Filter > Liquify | Brush size up to 15000 pixels | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0386 | Brush Tool Options: Density | filter-option | Filter > Liquify | Feathering falloff from center to edge | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0387 | Brush Tool Options: Pressure | filter-option | Filter > Liquify | Distortion speed while dragging | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0388 | Brush Tool Options: Rate | filter-option | Filter > Liquify | Speed for stationary tools like Twirl and Bloat | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0389 | Brush Tool Options: Stylus Pressure | filter-option | Filter > Liquify | Uses pen pressure | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0390 | Brush Tool Options: Pin Edges | filter-option | Filter > Liquify | Prevents transparent gaps at edges | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0391 | Face-Aware Liquify: Select Face | filter-option | Filter > Liquify | Chooses which detected face to edit | core | https://helpx.adobe.com/photoshop/using/face-aware-liquify.html |
| PS-B-0392 | Face-Aware Liquify: Eyes | filter-option | Filter > Liquify | Eye Size, Eye Height, Eye Width, Eye Tilt, Eye Distance with per-eye link | core | https://helpx.adobe.com/photoshop/using/face-aware-liquify.html |
| PS-B-0393 | Face-Aware Liquify: Nose | filter-option | Filter > Liquify | Nose Height and Nose Width | core | https://helpx.adobe.com/photoshop/using/face-aware-liquify.html |
| PS-B-0394 | Face-Aware Liquify: Mouth | filter-option | Filter > Liquify | Smile, Upper Lip, Lower Lip, Mouth Width, Mouth Height | core | https://helpx.adobe.com/photoshop/using/face-aware-liquify.html |
| PS-B-0395 | Face-Aware Liquify: Face Shape | filter-option | Filter > Liquify | Forehead, Chin Height, Jawline, Face Width | core | https://helpx.adobe.com/photoshop/using/face-aware-liquify.html |
| PS-B-0396 | Face-Aware Liquify: Reset and All | filter-option | Filter > Liquify | Resets face adjustments | core | https://helpx.adobe.com/photoshop/using/face-aware-liquify.html |
| PS-B-0397 | Load Mesh Options: Load Mesh, Load Last Mesh, Save Mesh | filter-option | Filter > Liquify | Saves and reuses distortion meshes | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0398 | Mask Options: Replace, Add, Subtract, Intersect, Invert Selection | filter-option | Filter > Liquify | Combines freeze mask with selection, transparency or layer mask | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0399 | Mask Options: None, Mask All, Invert All | filter-option | Filter > Liquify | Quick freeze mask operations | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0400 | View Options: Show Guides, Show Face Overlay, Show Image, Show Mesh | filter-option | Filter > Liquify | Display toggles with mesh size and color | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0401 | View Options: Show Mask and Mask Color | filter-option | Filter > Liquify | Freeze mask visibility and color | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0402 | View Options: Show Backdrop | filter-option | Filter > Liquify | Shows other layers behind with Use, Mode In Front/Behind/Blend, Opacity | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0403 | Brush Reconstruct Options: Reconstruct amount and Restore All | filter-option | Filter > Liquify | Partial or full reversal of distortion | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0404 | Liquify on Smart Objects | behavior | Filter > Liquify | Liquify can be applied as a Smart Filter | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0405 | Liquify GPU acceleration | behavior | Filter > Liquify | Liquify uses the GPU for real-time distortion | core | https://helpx.adobe.com/photoshop/using/liquify-filter.html |
| PS-B-0406 | VP Create Plane tool | tool | Filter > Vanishing Point | Clicks four corner nodes to define a perspective plane | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0407 | VP Edit Plane tool | tool | Filter > Vanishing Point | Selects, moves and resizes planes | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0408 | VP Marquee tool | tool | Filter > Vanishing Point | Makes perspective selections to move, copy or fill | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0409 | VP Stamp tool | tool | Filter > Vanishing Point | Clones in perspective | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0410 | VP Brush tool | tool | Filter > Vanishing Point | Paints a color in perspective | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0411 | VP Transform tool | tool | Filter > Vanishing Point | Scales, rotates and flips a floating selection | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0412 | VP Eyedropper tool | tool | Filter > Vanishing Point | Picks paint color | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0413 | VP Measure tool | tool | Filter > Vanishing Point | Measures distances in a plane | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0414 | VP Hand and Zoom tools | tool | Filter > Vanishing Point | Navigation | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0415 | VP Grid Size | filter-option | Filter > Vanishing Point | Grid spacing on planes | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0416 | VP Angle | filter-option | Filter > Vanishing Point | Angle for perpendicular child planes pulled from an edge | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0417 | VP plane color coding | filter-option | Filter > Vanishing Point | Blue valid, yellow or red invalid planes | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0418 | VP Marquee Feather, Opacity, Heal | filter-option | Filter > Vanishing Point | Heal Off, Luminance or On blends moved content | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0419 | VP Move Mode | filter-option | Filter > Vanishing Point | Destination or Source fill for selection moves | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0420 | VP Stamp Heal and Aligned | filter-option | Filter > Vanishing Point | Healing blend and aligned sampling | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0421 | VP Brush Heal | filter-option | Filter > Vanishing Point | Healing for painted strokes | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0422 | VP Show Edges and Show Measurements | filter-option | Filter > Vanishing Point | Display toggles | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0423 | VP Render Grids to Photoshop | filter-option | Filter > Vanishing Point | Renders grids onto the layer | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0424 | VP Render Measurements to Photoshop | filter-option | Filter > Vanishing Point | Renders measurements onto the layer | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0425 | VP Export for DXF or 3DS | filter-option | Filter > Vanishing Point | Legacy export of planes, removed with 3D | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0426 | VP Return to Photoshop 3D layer | filter-option | Filter > Vanishing Point | Legacy 3D export, removed | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0427 | VP paste into plane | behavior | Filter > Vanishing Point | Pasted clipboard content can be dragged into a plane and follows perspective | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |
| PS-B-0428 | VP planes saved with document | behavior | Filter > Vanishing Point | Planes persist in PSD when saved | core | https://helpx.adobe.com/photoshop/using/vanishing-point.html |

## Neural Filters

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0429 | Neural Filters workspace | panel | Filter > Neural Filters | Panel listing All filters, Featured and Beta with on/off toggles and a Wait List | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0430 | Neural Filters: Download filter | panel-option | Filter > Neural Filters | Cloud icon downloads a filter model before first use | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0431 | Neural Filters: Output | panel-option | Filter > Neural Filters | Current Layer, New Layer, New Layer Masked, Smart Filter, New Document | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0432 | Neural Filters: Show original | panel-option | Filter > Neural Filters | Toggles before and after | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0433 | Neural Filters: Preview layer toggle | panel-option | Filter > Neural Filters | Shows or hides preview | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0434 | Neural Filters: Feedback | panel-option | Filter > Neural Filters | Thumbs up and down with image submission | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0435 | Neural Filters: Stack multiple filters | panel-option | Filter > Neural Filters | Several filters can be enabled and applied together | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0436 | Neural Filters cloud processing | behavior | Filter > Neural Filters | Some filters process in the cloud and require connectivity | ai | https://helpx.adobe.com/photoshop/using/neural-filters.html |
| PS-B-0437 | Skin Smoothing | filter | Filter > Neural Filters | Smooths blemishes and acne on faces | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0438 | Skin Smoothing: Blur and Smoothness | filter-option | Filter > Neural Filters | Controls amount and smoothness | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0439 | Smart Portrait | filter | Filter > Neural Filters | Generative facial edits | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0440 | Smart Portrait: Featured Happiness, Surprise, Anger, Facial Age, Hair Thickness, Eye Direction | filter-option | Filter > Neural Filters | Expression and feature sliders | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0441 | Smart Portrait: Head Direction, Light Direction | filter-option | Filter > Neural Filters | Pose and light sliders | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0442 | Smart Portrait: Auto balance combinations, Retain unique details, Mask details | filter-option | Filter > Neural Filters | Settings controlling result quality | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0443 | Makeup Transfer | filter | Filter > Neural Filters | Transfers eye and mouth makeup from a reference image | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0444 | Super Zoom | filter | Filter > Neural Filters | Crops and enlarges with generated detail | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0445 | Super Zoom: Enhance image details, Remove JPEG artifacts, Noise reduction, Sharpen, Face enhancement | filter-option | Filter > Neural Filters | Enlargement quality options | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0446 | JPEG Artifacts Removal | filter | Filter > Neural Filters | Removes compression artifacts | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0447 | JPEG Artifacts Removal: Strength | filter-option | Filter > Neural Filters | Low, Medium, High | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0448 | Colorize | filter | Filter > Neural Filters | Colors black and white photos | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0449 | Colorize: Auto color image, focal points, Profile, Saturation, color balance sliders, Color artifact reduction, Noise reduction | filter-option | Filter > Neural Filters | Focal-point color hints and tuning | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0450 | Style Transfer | filter | Filter > Neural Filters | Applies artistic styles from presets or a custom image | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0451 | Style Transfer: Style strength, Brush size, Blur background, Preserve color, Focus subject | filter-option | Filter > Neural Filters | Style application controls | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0452 | Photo Restoration | filter | Filter > Neural Filters | Restores old damaged photos | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0453 | Photo Restoration: Photo enhancement, Enhance face, Scratch reduction, Noise reduction, Color noise, Halftone reduction, JPEG artifact reduction | filter-option | Filter > Neural Filters | Restoration sliders | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0454 | Harmonization | filter | Filter > Neural Filters | Matches color and tone of a layer to a reference layer | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0455 | Harmonization: Reference layer, Strength, Cyan-Red, Magenta-Green, Yellow-Blue, Saturation, Brightness | filter-option | Filter > Neural Filters | Harmonization tuning | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0456 | Landscape Mixer | filter | Filter > Neural Filters | Blends landscape attributes and seasons from presets or a reference | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0457 | Landscape Mixer: Strength, Day, Night, Sunset, Spring, Summer, Autumn, Winter, Preserve Subject, Harmonize Subject | filter-option | Filter > Neural Filters | Mixing controls | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0458 | Depth Blur | filter | Filter > Neural Filters | Depth-map based background blur with haze | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0459 | Depth Blur: Focal point, Focal distance, Focal range, Blur strength, Haze, Warmness, Brightness, Saturation, Grain, Output depth map only | filter-option | Filter > Neural Filters | Depth blur tuning | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0460 | Color Transfer | filter | Filter > Neural Filters | Transfers a color palette from a preset or custom image | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0461 | Color Transfer: Luminance, Color Intensity, Saturation, Hue, Preserve luminance | filter-option | Filter > Neural Filters | Color transfer tuning | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |
| PS-B-0462 | Neural Filters Wait List | panel | Filter > Neural Filters | Voting list of proposed future filters such as Noise reduction, Face cleanup, Photo to Sketch, Sketch to Portrait, Pencil Artwork, Face to Caricature | ai | https://helpx.adobe.com/photoshop/using/neural-filters-list-and-faq.html |

## Camera Raw Filter and Camera Raw 18.6

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0463 | ACR as Smart Filter | behavior | Filter > Camera Raw Filter > Edit | Camera Raw Filter on a Smart Object remains re-editable | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0464 | ACR opens raw files | behavior | File > Open | Opening raw, DNG and optionally JPEG/TIFF/HEIC files routes through the Camera Raw dialog | core | https://helpx.adobe.com/photoshop/using/camera-raw.html |
| PS-B-0465 | Profile browser | panel-option | Filter > Camera Raw Filter > Edit | Grid of Adobe Raw, Camera Matching, Artistic, B and W, Modern, Vintage profiles with favorites | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0466 | Profile Amount | panel-option | Filter > Camera Raw Filter > Edit | Slider to scale creative profile strength | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0467 | Adobe Adaptive profile | panel-option | Filter > Camera Raw Filter > Edit | AI profile that adapts tone and color to each image | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0468 | Treatment Color or Black and White | panel-option | Filter > Camera Raw Filter > Edit | Switches color treatment | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0469 | Auto | panel-option | Filter > Camera Raw Filter > Edit | Automatic tone and color settings (AI-based) | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0470 | HDR Output | panel-option | Filter > Camera Raw Filter > Edit | Edits and displays high dynamic range on HDR displays | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0471 | HDR Visualize and Preview for SDR display | panel-option | Filter > Camera Raw Filter > Edit | Shows HDR areas and SDR rendition controls | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0472 | Light: Exposure | panel-option | Filter > Camera Raw Filter > Edit | Overall brightness in stops | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0473 | Light: Contrast | panel-option | Filter > Camera Raw Filter > Edit | Midtone contrast | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0474 | Light: Highlights | panel-option | Filter > Camera Raw Filter > Edit | Recovers or brightens highlights | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0475 | Light: Shadows | panel-option | Filter > Camera Raw Filter > Edit | Lifts or deepens shadows | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0476 | Light: Whites | panel-option | Filter > Camera Raw Filter > Edit | Sets white clipping point | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0477 | Light: Blacks | panel-option | Filter > Camera Raw Filter > Edit | Sets black clipping point | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0478 | Light: Glow | panel-option | Filter > Camera Raw Filter > Edit | Soft luminous glow spreading from brightest areas (ACR 18.6) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0479 | Light: Tone Curve (Curve panel) | panel-option | Filter > Camera Raw Filter > Edit | Parametric curve plus point curve for RGB, Red, Green, Blue with Refine Saturation | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0480 | Curve: Parametric regions | panel-option | Filter > Camera Raw Filter > Edit | Highlights, Lights, Darks, Shadows sliders with split points | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0481 | Curve: Point curve and targeted adjustment | panel-option | Filter > Camera Raw Filter > Edit | Click-and-drag on image to move curve points | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0482 | Color: White Balance presets | panel-option | Filter > Camera Raw Filter > Edit | As Shot, Auto, Daylight, Cloudy, Shade, Tungsten, Fluorescent, Flash, Custom | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0483 | Color: White Balance eyedropper | panel-option | Filter > Camera Raw Filter > Edit | Click a neutral area to set balance | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0484 | Color: Temperature | panel-option | Filter > Camera Raw Filter > Edit | Kelvin (raw, down to 1500K) or relative scale | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0485 | Color: Tint | panel-option | Filter > Camera Raw Filter > Edit | Green-magenta balance | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0486 | Color: Vibrance | panel-option | Filter > Camera Raw Filter > Edit | Boosts less saturated colors | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0487 | Color: Saturation | panel-option | Filter > Camera Raw Filter > Edit | Uniform saturation | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0488 | Color Mixer: HSL | panel-option | Filter > Camera Raw Filter > Edit | Hue, Saturation, Luminance for eight color ranges | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0489 | Color Mixer: Color mode | panel-option | Filter > Camera Raw Filter > Edit | Per-color H, S, L in one view | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0490 | Color Mixer: Point Color | panel-option | Filter > Camera Raw Filter > Edit | Sample a specific color and shift hue, saturation, luminance with range refinement | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0491 | Color Mixer: Targeted adjustment tool | panel-option | Filter > Camera Raw Filter > Edit | Drag on image to adjust sampled color | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0492 | Color Mixer: B and W Mix | panel-option | Filter > Camera Raw Filter > Edit | Per-color gray conversion in B and W treatment | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0493 | Color Grading: Shadows, Midtones, Highlights wheels | panel-option | Filter > Camera Raw Filter > Edit | Hue and saturation wheels with luminance | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0494 | Color Grading: Global wheel | panel-option | Filter > Camera Raw Filter > Edit | Overall tint | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0495 | Color Grading: Blending and Balance | panel-option | Filter > Camera Raw Filter > Edit | Wheel overlap and shadow to highlight balance | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0496 | Effects: Texture | panel-option | Filter > Camera Raw Filter > Edit | Medium detail enhancement or smoothing | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0497 | Effects: Clarity | panel-option | Filter > Camera Raw Filter > Edit | Local midtone contrast | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0498 | Effects: Dehaze | panel-option | Filter > Camera Raw Filter > Edit | Removes or adds atmospheric haze | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0499 | Effects: Vignette | panel-option | Filter > Camera Raw Filter > Edit | Amount, Midpoint, Roundness, Feather, Highlights, Style (Highlight Priority, Color Priority, Paint Overlay) | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0500 | Effects: Grain | panel-option | Filter > Camera Raw Filter > Edit | Amount, Size, Roughness | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0501 | Detail: Sharpening | panel-option | Filter > Camera Raw Filter > Edit | Amount, Radius, Detail, Masking with Alt preview | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0502 | Detail: Denoise | panel-option | Filter > Camera Raw Filter > Edit | AI denoise of raw files with Amount, creates enhanced DNG | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0503 | Detail: Raw Details | panel-option | Filter > Camera Raw Filter > Edit | AI demosaic improvement for fine detail | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0504 | Detail: Super Resolution | panel-option | Filter > Camera Raw Filter > Edit | AI 2x linear upscale producing an enhanced DNG | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0505 | Detail: Manual Noise Reduction | panel-option | Filter > Camera Raw Filter > Edit | Luminance with Detail and Contrast; Color with Detail and Smoothness | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0506 | Optics (Lens): Remove Chromatic Aberration | panel-option | Filter > Camera Raw Filter > Edit | Automatic lateral CA removal | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0507 | Optics: Use Profile Corrections | panel-option | Filter > Camera Raw Filter > Edit | Applies lens profile distortion and vignette correction with Make, Model, Profile | core | https://helpx.adobe.com/camera-raw/using/lens-profile-support.html |
| PS-B-0508 | Optics: Distortion and Vignetting amounts | panel-option | Filter > Camera Raw Filter > Edit | Scales profile corrections | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0509 | Optics: Manual Distortion and Vignetting | panel-option | Filter > Camera Raw Filter > Edit | Manual Distortion, Vignetting, Midpoint | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0510 | Optics: Defringe | panel-option | Filter > Camera Raw Filter > Edit | Purple and Green Amount and Hue ranges with fringe eyedropper | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0511 | Optics: Lens Blur | panel-option | Filter > Camera Raw Filter > Edit | AI depth-based background blur with bokeh shapes, Blur amount, Focal range, Focus on subject, depth visualization, Refine brush | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0512 | Geometry: Upright | panel-option | Filter > Camera Raw Filter > Edit | Off, Auto, Level, Vertical, Full, Guided | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0513 | Geometry: Guided Upright tool | panel-option | Filter > Camera Raw Filter > Edit | Draw up to four guides to straighten | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0514 | Geometry: Manual Transforms | panel-option | Filter > Camera Raw Filter > Edit | Vertical, Horizontal, Rotate, Aspect, Scale, Offset X, Offset Y | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0515 | Geometry: Constrain Crop | panel-option | Filter > Camera Raw Filter > Edit | Crops out blank areas after transform | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0516 | Geometry: Projection correction | panel-option | Filter > Camera Raw Filter > Edit | Fixes stretched faces near wide-angle edges (ACR 18.3) | ai | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0517 | Geometry: Grid overlay and Loupe | panel-option | Filter > Camera Raw Filter > Edit | Alignment aids | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0518 | Calibration: Process version | panel-option | Filter > Camera Raw Filter > Edit | Selects rendering process version | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0519 | Calibration: Shadows Tint | panel-option | Filter > Camera Raw Filter > Edit | Green-magenta shadow calibration | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0520 | Calibration: Red, Green, Blue Primary Hue and Saturation | panel-option | Filter > Camera Raw Filter > Edit | Primary calibration | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0521 | Crop and Expand panel | panel-option | Filter > Camera Raw Filter > Crop | Crop, straighten angle, aspect presets, constrain to image, Generative Expand, Trim | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0522 | Crop: Generative Expand | panel-option | Filter > Camera Raw Filter > Crop | Extends canvas with AI-generated content (ACR 18.4.1) | ai | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0523 | Crop: Trim to transparent cutout | panel-option | Filter > Camera Raw Filter > Crop | Makes everything outside the crop transparent (ACR 18.6) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0524 | Crop: Anamorphic Desqueeze | panel-option | Filter > Camera Raw Filter > Crop | Corrects anamorphic lens aspect up to 2.0 (ACR 18.3) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0525 | Remove: Generative AI mode | tool | Filter > Camera Raw Filter > Remove | Firefly-generated removal of brushed objects | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0526 | Remove: Content-aware remove | tool | Filter > Camera Raw Filter > Remove | Non-generative removal brush | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0527 | Remove: Heal | tool | Filter > Camera Raw Filter > Remove | Heal spot using a source area | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0528 | Remove: Clone | tool | Filter > Camera Raw Filter > Remove | Clone spot from a source area | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0529 | Remove: Detect objects | panel-option | Filter > Camera Raw Filter > Remove | AI outlines the brushed object for removal | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0530 | Remove: Size, Feather, Opacity | panel-option | Filter > Camera Raw Filter > Remove | Brush controls | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0531 | Remove: Visualize spots | panel-option | Filter > Camera Raw Filter > Remove | High-contrast view to find dust with threshold slider | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0532 | Remove: Distraction Removal People | panel-option | Filter > Camera Raw Filter > Remove | Detects and removes people in the background | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0533 | Remove: Distraction Removal Reflections | panel-option | Filter > Camera Raw Filter > Remove | Removes reflections through glass with Amount | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0534 | Remove: Distraction Removal Dust | panel-option | Filter > Camera Raw Filter > Remove | Automatically detects and removes sensor dust spots | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0535 | Remove: Blemishes | panel-option | Filter > Camera Raw Filter > Remove | AI removal of blemishes, spots, moles, freckles with per-type prominence (ACR 18.5) | ai | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0536 | Remove: Generate variations | panel-option | Filter > Camera Raw Filter > Remove | Cycles three generative variations | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0537 | Red Eye tool | tool | Filter > Camera Raw Filter > Red Eye | Removes red eye or pet eye | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0538 | Red Eye: Pupil Size and Darken | panel-option | Filter > Camera Raw Filter > Red Eye | Red eye correction controls | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0539 | Pet Eye: Pupil Size and Add Catchlight | panel-option | Filter > Camera Raw Filter > Red Eye | Pet eye correction controls | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0540 | Mask: Subject | tool | Filter > Camera Raw Filter > Masking | AI selects the main subject | ai | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0541 | Mask: Sky | tool | Filter > Camera Raw Filter > Masking | AI selects the sky | ai | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0542 | Mask: Background | tool | Filter > Camera Raw Filter > Masking | AI selects the background | ai | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0543 | Mask: Objects | tool | Filter > Camera Raw Filter > Masking | Brush or rectangle around an object to select it | ai | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0544 | Mask: People | tool | Filter > Camera Raw Filter > Masking | Detects people with parts Face Skin, Body Skin, Eyebrows, Eye Sclera, Iris and Pupil, Lips, Teeth, Hair, Clothes | ai | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0545 | Mask: Landscape | tool | Filter > Camera Raw Filter > Masking | Detects Architecture, Water, Mountains, Natural Ground, Vegetation, Artificial Ground, Sky | ai | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0546 | Mask: Brush | tool | Filter > Camera Raw Filter > Masking | Paints a mask with Size, Feather, Flow, Density, Auto Mask | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0547 | Mask: Linear Gradient | tool | Filter > Camera Raw Filter > Masking | Graduated linear mask | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0548 | Mask: Radial Gradient | tool | Filter > Camera Raw Filter > Masking | Elliptical mask with feather and invert | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0549 | Mask: Bidirectional gradient | tool | Filter > Camera Raw Filter > Masking | Two-sided gradient mask (ACR 18.4) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0550 | Mask: Range Color | tool | Filter > Camera Raw Filter > Masking | Selects by sampled color with refine amount | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0551 | Mask: Range Luminance | tool | Filter > Camera Raw Filter > Masking | Selects by luminance range with smoothness | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0552 | Mask: Range Depth | tool | Filter > Camera Raw Filter > Masking | Selects by depth, available on any photo (ACR 18.3) | ai | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0553 | Mask combine: Add, Subtract, Intersect | panel-option | Filter > Camera Raw Filter > Masking | Boolean mask components | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0554 | Mask Invert and Duplicate | panel-option | Filter > Camera Raw Filter > Masking | Inverts or duplicates masks | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0555 | Mask overlay | panel-option | Filter > Camera Raw Filter > Masking | Color overlay, image on B/W, B/W, image on black or white options with color and opacity | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0556 | Mask Feather and Edge sliders | panel-option | Filter > Camera Raw Filter > Masking | Refines AI mask edges (ACR 18.3.1) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0557 | Mask local adjustments | panel-option | Filter > Camera Raw Filter > Masking | Temperature, Tint, Exposure, Contrast, Highlights, Shadows, Whites, Blacks, Texture, Clarity, Dehaze, Hue, Saturation, Sharpness, Noise, Moire, Defringe, Color, Curve | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0558 | Mask local Color Grading | panel-option | Filter > Camera Raw Filter > Masking | Three-way color wheels inside a mask (ACR 18.3.1) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0559 | Mask local Point Color | panel-option | Filter > Camera Raw Filter > Masking | Point color adjustments within a mask | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0560 | Mask Amount | panel-option | Filter > Camera Raw Filter > Masking | Scales all mask adjustments | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0561 | Mask presets and recommended mask presets | panel-option | Filter > Camera Raw Filter > Masking | Saved mask adjustments, adaptive AI mask presets | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0562 | Mask update AI | panel-option | Filter > Camera Raw Filter > Masking | Recomputes AI masks after changes | core | https://helpx.adobe.com/camera-raw/using/masking.html |
| PS-B-0563 | Presets panel | panel | Filter > Camera Raw Filter > Presets | Browse, apply and manage presets with Amount slider | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0564 | Adaptive presets | panel-option | Filter > Camera Raw Filter > Presets | AI presets for Subject, Sky and Portraits (Adaptive: Portrait) | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0565 | Premium presets | panel-option | Filter > Camera Raw Filter > Presets | Built-in style groups including film-inspired Style presets (ACR 18.3) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0566 | Recommended presets | panel-option | Filter > Camera Raw Filter > Presets | AI suggested presets based on the image | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0567 | Create Preset | panel-option | Filter > Camera Raw Filter > Presets | Saves chosen settings groups including masks as a preset | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0568 | Import and Export presets | panel-option | Filter > Camera Raw Filter > Presets | XMP preset import and zip export | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0569 | Hide partially compatible presets | panel-option | Filter > Camera Raw Filter > Presets | Filters presets list | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0570 | Snapshots panel | panel | Filter > Camera Raw Filter | Saves named states of edits | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0571 | Before and after views | panel-option | Filter > Camera Raw Filter | Left/right, top/bottom split and side-by-side comparison | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0572 | Histogram with clipping warnings | panel-option | Filter > Camera Raw Filter | Shows RGB histogram and toggles shadow and highlight clipping | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0573 | Vectorscope | panel-option | Filter > Camera Raw Filter | Hue and saturation distribution display with skin tone line, reference orientation and Lab readout (ACR 18.4, 18.5) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0574 | Metadata Info panel | panel-option | Filter > Camera Raw Filter | Capture settings, camera and file details (ACR 18.6) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0575 | Autofocus points display | panel-option | Camera Raw dialog | Shows AF points for supported Canon, Nikon, Sony raws (ACR 18.4.1) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0576 | Fullscreen Presentation mode | panel-option | Camera Raw dialog | Presents photos full screen with arrow navigation (ACR 18.4.1) | core | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0577 | Render to DNG | panel-option | Camera Raw dialog | Saves a new DNG with edits baked in (ACR 18.5) | format | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0578 | Filmstrip | panel-option | Camera Raw dialog | Multi-image editing with synchronize settings | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0579 | Copy and Paste settings | panel-option | Camera Raw dialog | Copies edit settings between images | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0580 | Reset and toggle panel visibility | panel-option | Filter > Camera Raw Filter | Eye icons disable individual panels | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0581 | Zoom and Hand tools | panel-option | Filter > Camera Raw Filter | Navigation | core | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0582 | Workflow Options | panel-option | Camera Raw dialog | Color space, bit depth, size, resolution, sharpening for raw open, Open in Photoshop as Smart Objects | core | https://helpx.adobe.com/camera-raw/using/camera-raw-preferences.html |
| PS-B-0583 | Save Image | panel-option | Camera Raw dialog | Exports to JPEG, TIFF, DNG, PSD, PNG, JPEG XL, AVIF with metadata and sizing | format | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0584 | Camera Raw Preferences: General | preference | Camera Raw Preferences | Appearance, UI scaling, panel layout options | core | https://helpx.adobe.com/camera-raw/using/camera-raw-preferences.html |
| PS-B-0585 | Camera Raw Preferences: File Handling | preference | Camera Raw Preferences | Sidecar XMP, DNG options, JPEG/HEIC/TIFF handling Automatically open all supported | core | https://helpx.adobe.com/camera-raw/using/camera-raw-preferences.html |
| PS-B-0586 | Camera Raw Preferences: Performance | preference | Camera Raw Preferences | Graphics processor use and cache size | core | https://helpx.adobe.com/camera-raw/using/camera-raw-preferences.html |
| PS-B-0587 | Camera Raw Preferences: Raw Defaults | preference | Camera Raw Preferences | Default settings per camera | core | https://helpx.adobe.com/camera-raw/using/camera-raw-preferences.html |
| PS-B-0588 | Camera Raw Preferences: Technology Previews | preference | Camera Raw Preferences | Experimental features | core | https://helpx.adobe.com/camera-raw/using/camera-raw-preferences.html |
| PS-B-0589 | Camera Raw Preferences: Generative AI toggle | preference | Camera Raw Preferences | Turns Generative AI features on or off (ACR 18.5) | ai | https://helpx.adobe.com/camera-raw/desktop/whats-new/whats-new.html |
| PS-B-0590 | Camera Raw Preferences: HDR editing | preference | Camera Raw Preferences | Enables HDR output | core | https://helpx.adobe.com/camera-raw/using/camera-raw-preferences.html |
| PS-B-0591 | Content Credentials in ACR | behavior | Camera Raw dialog | Generative edits and exports attach content credentials | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |

## Generative and AI features

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0592 | Generative Fill | command | Edit > Generative Fill / Contextual Task Bar | Fills a selection with Firefly or partner model content from an optional text prompt | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0593 | Generative Fill: prompt field | dialog-option | Edit > Generative Fill / Contextual Task Bar | Text describing what to add; empty prompt removes or fills contextually | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0594 | Generative Fill: Generate button | dialog-option | Edit > Generative Fill / Contextual Task Bar | Produces three variations on a new Generative layer | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0595 | Generative layer variations | panel-option | Edit > Generative Fill / Contextual Task Bar | Properties panel thumbnails switch between variations; more can be generated | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0596 | Generate Similar | panel-option | Properties panel | Creates variations resembling a chosen result (Firefly Fill and Expand model since 27.4) | ai | https://www.cgchannel.com/2026/03/adobe-releases-photoshop-27-4/ |
| PS-B-0597 | Rate and report variations | panel-option | Properties panel | Thumbs up or down and report feedback per variation | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0598 | Generative layer mask | panel-option | Edit > Generative Fill / Contextual Task Bar | Generated content is masked to the selection and stored as a layer | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0599 | Reference Image | panel-option | Contextual Task Bar | Uploads or picks an image to guide style and content of generated fill | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0600 | Model picker | panel-option | Contextual Task Bar | Chooses Firefly Image model or partner models for generation | ai | https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html |
| PS-B-0601 | Partner model: Google Gemini (Nano Banana) | panel-option | Contextual Task Bar | Third-party image model usable in Generative Fill | ai | https://www.cgchannel.com/2025/10/adobe-releases-photoshop-27-0/ |
| PS-B-0602 | Partner model: Black Forest Labs FLUX Kontext Pro | panel-option | Contextual Task Bar | Third-party image model usable in Generative Fill | ai | https://www.cgchannel.com/2025/10/adobe-releases-photoshop-27-0/ |
| PS-B-0603 | Firefly Fill and Expand model | panel-option | Contextual Task Bar | Dedicated Firefly model for Fill, Expand and Generate Similar | ai | https://www.cgchannel.com/2026/03/adobe-releases-photoshop-27-4/ |
| PS-B-0604 | Firefly Image 5 model | panel-option | Contextual Task Bar | Latest Firefly image model option for Prompt to edit and generation | ai | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-B-0605 | Generative credits | behavior | Account menu | Generative operations consume credits shown in the Account menu; standard vs premium features | cloud | https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html |
| PS-B-0606 | Generative Fill resolution | behavior | Canvas | Generations are produced at limited resolution and upscaled to the selection size | ai | https://helpx.adobe.com/photoshop/using/generative-fill.html |
| PS-B-0607 | Generative Expand | command | Crop tool > Contextual Task Bar | Extends canvas with the Crop tool and fills new area with generated content | ai | https://helpx.adobe.com/photoshop/using/generative-expand.html |
| PS-B-0608 | Generative Expand: prompt | dialog-option | Crop tool > Contextual Task Bar | Optional prompt for content in the expanded area | ai | https://helpx.adobe.com/photoshop/using/generative-expand.html |
| PS-B-0609 | Crop tool Fill: Background, Content-Aware Fill, Generative Expand | dialog-option | Crop tool options | Chooses how expanded canvas is filled | ai | https://helpx.adobe.com/photoshop/using/generative-expand.html |
| PS-B-0610 | Generate Image | command | Edit > Generate Image | Creates a new image from a text prompt with content type, style and effects | ai | https://helpx.adobe.com/photoshop/using/generate-image.html |
| PS-B-0611 | Generate Image: Content type Photo or Art | dialog-option | Generate Image dialog | Sets output rendering type | ai | https://helpx.adobe.com/photoshop/using/generate-image.html |
| PS-B-0612 | Generate Image: Style Reference | dialog-option | Generate Image dialog | Upload or choose a gallery image to guide style with strength | ai | https://helpx.adobe.com/photoshop/using/generate-image.html |
| PS-B-0613 | Generate Image: Composition Reference | dialog-option | Generate Image dialog | Guides layout from a reference image | ai | https://helpx.adobe.com/photoshop/using/generate-image.html |
| PS-B-0614 | Generate Image: Effects presets | dialog-option | Generate Image dialog | Style effect chips such as painting, 3D, textures | ai | https://helpx.adobe.com/photoshop/using/generate-image.html |
| PS-B-0615 | Generate Image: Visual intensity | dialog-option | Generate Image dialog | Controls stylization strength | ai | https://helpx.adobe.com/photoshop/using/generate-image.html |
| PS-B-0616 | Generate Image: Aspect ratio | dialog-option | Generate Image dialog | Chooses output aspect | ai | https://helpx.adobe.com/photoshop/using/generate-image.html |
| PS-B-0617 | Generate Image: AI model choice | dialog-option | Generate Image dialog | Firefly and partner models selectable (27.8) | ai | https://www.cgchannel.com/2026/06/adobe-releases-photoshop-27-8/ |
| PS-B-0618 | Generate Background | command | Contextual Task Bar | Replaces the background of a subject with a generated scene | ai | https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html |
| PS-B-0619 | Generate Similar command | command | Properties panel | Generates more variations like a selected one | ai | https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html |
| PS-B-0620 | Harmonize | command | Contextual Task Bar / Layer | Adjusts lighting, color, shadows of a composited layer to match background | ai | https://helpx.adobe.com/photoshop/using/harmonize.html |
| PS-B-0621 | Harmonize: variations | dialog-option | Properties panel | Produces variations as a new generative layer | ai | https://helpx.adobe.com/photoshop/using/harmonize.html |
| PS-B-0622 | Generative Upscale | command | Image > Generative Upscale | AI upscaling to higher resolution with Firefly or Topaz models | ai | https://helpx.adobe.com/photoshop/using/generative-upscale.html |
| PS-B-0623 | Generative Upscale: scale factor 2x or 4x | dialog-option | Generative Upscale dialog | Output size choice | ai | https://helpx.adobe.com/photoshop/using/generative-upscale.html |
| PS-B-0624 | Generative Upscale: model choice | dialog-option | Generative Upscale dialog | Firefly Upscaler or Topaz Gigapixel and Bloom partner models | ai | https://www.cgchannel.com/2025/10/adobe-releases-photoshop-27-0/ |
| PS-B-0625 | Prompt to edit | command | Edit > Prompt to edit / Contextual Task Bar | Natural language instruction edits the image; respects current selection as a mask (27.10) | ai | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-B-0626 | Markup | dialog-option | Contextual Task Bar | Draw arrows, circles, color picks and doodles to guide generative edits (27.10) | ai | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-B-0627 | AI Assisted Editor (Beta) | command | Photoshop AI Assisted mode | Firefly creative tools accessible inside Photoshop, conversational editing mode (27.10) | ai | https://helpx.adobe.com/photoshop/desktop/generative-ai/use-ai-assisted-editor.html |
| PS-B-0628 | AI Assistant (beta) | command | Photoshop (Beta) | Chat agent that performs multi-step edits from requests | ai | https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html |
| PS-B-0629 | Send layers to Firefly Boards | command | Layers panel context menu | Sends one or more layers to Firefly Boards for ideation (27.5, 27.9.1) | cloud | https://helpx.adobe.com/photoshop/desktop/generative-ai/use-firefly-boards-with-photoshop.html |
| PS-B-0630 | Remove tool | tool | Toolbar > Remove tool | Brush over distractions to remove them with AI fill | ai | https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html |
| PS-B-0631 | Remove tool: Generative AI mode Auto, On, Off | panel-option | Remove tool options | Chooses generative vs non-generative removal | ai | https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html |
| PS-B-0632 | Remove tool: local model | panel-option | Remove tool options | AI model can run on device instead of cloud (27.7) | ai | https://www.cgchannel.com/2026/05/adobe-releases-photoshop-27-7/ |
| PS-B-0633 | Remove tool: Remove after each stroke | panel-option | Remove tool options | Applies removal on every stroke or waits for confirm | ai | https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html |
| PS-B-0634 | Remove tool: Sample All Layers | panel-option | Remove tool options | Uses content from all layers | ai | https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html |
| PS-B-0635 | Remove tool: Size | panel-option | Remove tool options | Brush size | ai | https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html |
| PS-B-0636 | Find Distractions: People | panel-option | Remove tool options / Contextual Task Bar | Detects and removes background people | ai | https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html |
| PS-B-0637 | Find Distractions: Wires and cables | panel-option | Remove tool options / Contextual Task Bar | Detects and removes wires and power lines | ai | https://helpx.adobe.com/photoshop/using/tool-techniques/remove-tool.html |
| PS-B-0638 | Remove tool Contextual Task Bar | panel-option | Contextual Task Bar | Quick access to Find distractions and brush options (27.9.1) | ai | https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html |
| PS-B-0639 | Remove Background | command | Contextual Task Bar / Properties > Quick Actions | One-click subject isolation producing a layer mask | ai | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-B-0640 | Select Subject | command | Select > Subject | AI selection of the main subject | ai | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-B-0641 | Select Subject processing: Device or Cloud | preference | Preferences > Image Processing | Chooses local or cloud model; cloud gives more detailed results | ai | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-0642 | Sky Replacement | command | Edit > Sky Replacement | Replaces sky with preset or custom skies and relights foreground | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0643 | Sky Replacement: Sky presets and custom import | dialog-option | Sky Replacement dialog | Blue Skies, Spectacular, Sunsets groups and user skies | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0644 | Sky Replacement: Shift Edge and Fade Edge | dialog-option | Sky Replacement dialog | Adjust mask boundary | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0645 | Sky Replacement: Sky Adjustments Brightness, Temperature, Scale, Flip | dialog-option | Sky Replacement dialog | Tunes the new sky | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0646 | Sky Replacement: Foreground Lighting Mode Multiply or Screen | dialog-option | Sky Replacement dialog | Relights foreground with sky color | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0647 | Sky Replacement: Foreground Lighting, Edge Lighting, Color Adjustment | dialog-option | Sky Replacement dialog | Foreground blend controls | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0648 | Sky Replacement: Output to New Layers or Duplicate Layer | dialog-option | Sky Replacement dialog | Output format | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0649 | Sky Brush and Move tools | tool | Sky Replacement dialog | Refine the sky mask and reposition the sky | ai | https://helpx.adobe.com/photoshop/using/replace-sky.html |
| PS-B-0650 | Adjustment Presets (AI) | command | Adjustments panel | One-click looks and adjustment presets in the Adjustments panel, some subject-aware | ai | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0651 | Auto adjustment in Camera Raw (AI) | command | Filter > Camera Raw Filter | AI-based automatic tone and color | ai | https://helpx.adobe.com/camera-raw/user-guide.html |
| PS-B-0652 | Content-Aware Fill workspace | command | Edit > Content-Aware Fill | Fills a selection by sampling surrounding content with editable sampling area | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0653 | Content-Aware Fill: Sampling Area Auto, Rectangular, Custom | dialog-option | Content-Aware Fill workspace | Sets where source pixels come from | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0654 | Content-Aware Fill: Color Adaptation, Rotation Adaptation, Scale, Mirror | dialog-option | Content-Aware Fill workspace | Fill synthesis options | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0655 | Content-Aware Fill: Output To Current, New, Duplicate Layer | dialog-option | Content-Aware Fill workspace | Output target | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0656 | Content Credentials panel | panel | Window > Content Credentials | Attaches provenance (edits, AI use, producer identity) to exports | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |
| PS-B-0657 | Content Credentials: Producer name and connected accounts | panel-option | Content Credentials panel | Adds identity and social accounts to credentials | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |
| PS-B-0658 | Content Credentials: Record edits and activity | panel-option | Content Credentials panel | Captures editing actions in the manifest | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |
| PS-B-0659 | Content Credentials: Export options | panel-option | Export As / Save dialogs | Attach to exported files or publish to cloud | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |
| PS-B-0660 | Generative AI auto credentials | behavior | Export | Files with generative content automatically carry content credentials on export | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |
| PS-B-0661 | Content Credentials default for new documents | preference | Preferences > History & Content Credentials | Enables credentials by default | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |
| PS-B-0662 | Photoshop on web generative extras | behavior | Photoshop on the web | Web version hosts some generative features first such as Generate Image variations and adjustment presets | cloud | https://helpx.adobe.com/photoshop/using/photoshop-web-overview.html |

## Automation: Actions, Batch, Droplets, Scripts, Plug-ins

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0663 | Actions panel | panel | Window > Actions | Lists action sets and actions with recorded steps | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0664 | Actions: List mode and Button mode | panel-option | Window > Actions | Expandable list or one-click colored buttons | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0665 | Actions: toggle item on or off | panel-option | Window > Actions | Checkbox column excludes an action or step from playback | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0666 | Actions: toggle dialog on or off | panel-option | Window > Actions | Modal control column shows dialogs during playback for user input | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0667 | Actions: Stop playing | panel-option | Window > Actions | Stops playback or recording | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0668 | Actions: Begin recording | panel-option | Window > Actions | Records subsequent commands into the selected action | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0669 | Actions: Play selection | panel-option | Window > Actions | Plays the action or starting from selected step | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0670 | Actions: Create new set | panel-option | Window > Actions | Adds a new action set | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0671 | Actions: Create new action | panel-option | Window > Actions | Name, set, function key with Shift/Ctrl, color | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0672 | Actions: Delete | panel-option | Window > Actions | Deletes action, set or step | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0673 | New Action | command | Actions panel menu | Creates an action with name, set, function key and button color | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0674 | New Set | command | Actions panel menu | Creates an action set | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0675 | Duplicate | command | Actions panel menu | Duplicates action, set or step | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0676 | Delete action item | command | Actions panel menu | Deletes the selection | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0677 | Play | command | Actions panel menu | Plays the selected action | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0678 | Start Recording | command | Actions panel menu | Resumes recording into the action | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0679 | Record Again | command | Actions panel menu | Re-records the selected step with new values | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0680 | Insert Menu Item | command | Actions panel menu | Records a menu command that is chosen at playback time | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0681 | Insert Stop | command | Actions panel menu | Adds a stop with a message and optional Continue button | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0682 | Insert Conditional | command | Actions panel menu | Adds an If/Then/Else step based on document state | automation | https://helpx.adobe.com/photoshop/using/conditional-actions.html |
| PS-B-0683 | Insert Path | command | Actions panel menu | Records the current path as a step | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0684 | Action Options | command | Actions panel menu | Renames and changes key and color | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0685 | Playback Options | command | Actions panel menu | Accelerated, Step by Step, Pause For seconds, Pause For Audio Annotation | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0686 | Allow Tool Recording | command | Actions panel menu | Records painting and tool strokes in actions | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0687 | Clear All Actions | command | Actions panel menu | Removes all sets from the panel | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0688 | Reset Actions | command | Actions panel menu | Restores Default Actions | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0689 | Load Actions | command | Actions panel menu | Loads an ATN set | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0690 | Replace Actions | command | Actions panel menu | Replaces all actions with a loaded set | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0691 | Save Actions | command | Actions panel menu | Saves a set to ATN | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0692 | Built-in action sets | command | Actions panel menu | Commands, Frames, Image Effects, LAB Black and White Technique, Production, Stars Trails, Text Effects, Textures, Video Actions | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0693 | Conditional: If Current | panel-option | Conditional Action dialog | Document Is Landscape, Is Portrait, Is Square, Has Selection, Has Layers, Layer Is Visible, Layer Has Pixel Mask, Has Vector Mask, Is Text Layer, Is Adjustment Layer, Is Smart Object, Mode Is RGB or CMYK, Bit Depth, Profile, Is Open, and more | automation | https://helpx.adobe.com/photoshop/using/conditional-actions.html |
| PS-B-0694 | Conditional: Then Play Action and Else Play Action | panel-option | Conditional Action dialog | Chooses actions to run for each branch | automation | https://helpx.adobe.com/photoshop/using/conditional-actions.html |
| PS-B-0695 | Action recording of relative values | behavior | Actions panel | Positions and sizes record in the current ruler units, percent makes them relative | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0696 | Action playback is a single history state option | behavior | Actions panel | Actions can be undone as a unit via history snapshot | automation | https://helpx.adobe.com/photoshop/using/actions-actions-panel.html |
| PS-B-0697 | Quick Actions | command | Properties panel | Properties panel buttons for Remove Background, Select Subject and similar one-click AI tasks | ai | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-B-0698 | Batch | command | File > Automate | Runs an action on a folder of files | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0699 | Batch: Set and Action | dialog-option | File > Automate | Chooses action to play | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0700 | Batch Source: Folder, Import, Opened Files, Bridge | dialog-option | File > Automate | Input selection | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0701 | Batch: Override Action Open Commands | dialog-option | File > Automate | Ignores recorded Open steps | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0702 | Batch: Include All Subfolders | dialog-option | File > Automate | Recurses folders | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0703 | Batch: Suppress File Open Options Dialogs | dialog-option | File > Automate | Suppresses Camera Raw and open dialogs | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0704 | Batch: Suppress Color Profile Warnings | dialog-option | File > Automate | Skips profile mismatch alerts | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0705 | Batch Destination: None, Save and Close, Folder | dialog-option | File > Automate | Output handling | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0706 | Batch: Override Action Save As Commands | dialog-option | File > Automate | Uses destination with the recorded save format | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0707 | Batch: File Naming | dialog-option | File > Automate | Up to six naming tokens: document name, serial number, serial letter, date formats, extension; starting serial number | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0708 | Batch: Compatibility Windows, Mac OS, Unix | dialog-option | File > Automate | Filename compatibility | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0709 | Batch Errors: Stop for Errors or Log Errors to File | dialog-option | File > Automate | Error handling | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0710 | Create Droplet | command | File > Automate | Saves an action as a standalone executable that processes dropped files | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0711 | Droplet: Save Droplet In, action, source and destination options | dialog-option | File > Automate | Same options as Batch | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0712 | PDF Presentation | command | File > Automate | Builds multi-page PDF or slideshow PDF from images | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0713 | PDF Presentation: Source files, Add Open Files, Duplicate, Sort by Name | dialog-option | PDF Presentation dialog | Input list | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0714 | PDF Presentation: Save as Multi-Page Document or Presentation | dialog-option | PDF Presentation dialog | Output type | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0715 | PDF Presentation: Background, Include Filename, Extension, Title, Description, Author, Copyright, EXIF, Notes, Font Size | dialog-option | PDF Presentation dialog | Captions | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0716 | PDF Presentation: Advance every seconds, Loop after last page, Transition | dialog-option | PDF Presentation dialog | Slideshow options | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0717 | Conditional Mode Change | command | File > Automate | Converts mode based on source mode conditions in actions | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0718 | Conditional Mode Change: Source Mode checkboxes and Target Mode | dialog-option | File > Automate | Chooses modes to convert from and to | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0719 | Contact Sheet II | command | File > Automate | Builds a thumbnail sheet of images from a folder | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0720 | Contact Sheet II: Source, Include Subfolders, Group by Folder | dialog-option | Contact Sheet II dialog | Input options | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0721 | Contact Sheet II: Document Units, Width, Height, Resolution, Mode, Bit Depth, Color Profile, Flatten All Layers | dialog-option | Contact Sheet II dialog | Sheet settings | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0722 | Contact Sheet II: Thumbnails Place across or down, Columns, Rows, Use Auto-Spacing, Rotate For Best Fit | dialog-option | Contact Sheet II dialog | Layout | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0723 | Contact Sheet II: Use Filename As Caption, Font, Font Size | dialog-option | Contact Sheet II dialog | Captions | automation | https://helpx.adobe.com/photoshop/using/contact-sheets-pdf-presentations.html |
| PS-B-0724 | Crop and Straighten Photos | command | File > Automate | Detects multiple scanned photos and splits each into a straightened document | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0725 | Fit Image | command | File > Automate | Resizes to fit within width and height preserving aspect | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0726 | Fit Image: Don't Enlarge | dialog-option | File > Automate | Prevents upscaling | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0727 | Lens Correction (batch) | command | File > Automate | Applies profile lens corrections to many files | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0728 | Lens Correction batch: Source Files, Destination, File Type, Lens profile matching, Corrections, Edge fill, Auto Scale | dialog-option | File > Automate | Batch lens options | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0729 | Merge to HDR Pro | command | File > Automate | Merges bracketed exposures into HDR | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0730 | Merge to HDR Pro: Attempt to Automatically Align | dialog-option | Merge to HDR Pro dialog | Aligns bracketed frames | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0731 | Merge to HDR Pro: Remove ghosts | dialog-option | Merge to HDR Pro dialog | Picks a base image to remove movement ghosts | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0732 | Merge to HDR Pro: Mode 32, 16, 8 bit | dialog-option | Merge to HDR Pro dialog | Output bit depth | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0733 | Merge to HDR Pro: Local Adaptation | dialog-option | Merge to HDR Pro dialog | Edge Glow Radius and Strength, Tone and Detail Gamma, Exposure, Detail, Advanced Shadow, Highlight, Vibrance, Saturation, Toning Curve | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0734 | Merge to HDR Pro: Equalize Histogram, Exposure and Gamma, Highlight Compression | dialog-option | Merge to HDR Pro dialog | Other tone mapping methods | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0735 | Merge to HDR Pro: Complete Toning in Adobe Camera Raw | dialog-option | Merge to HDR Pro dialog | Sends 32-bit result to Camera Raw for toning | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0736 | Merge to HDR Pro: 32-bit White Point preview and response curve | dialog-option | Merge to HDR Pro dialog | Preview control and load response curve | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0737 | Merge to HDR Pro: Presets save and load | dialog-option | Merge to HDR Pro dialog | Tone mapping presets | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0738 | HDR Toning | command | Image > Adjustments > HDR Toning | Tone maps a single image with HDR Pro controls | automation | https://helpx.adobe.com/photoshop/using/high-dynamic-range-images.html |
| PS-B-0739 | Photomerge | command | File > Automate | Stitches overlapping photos into a panorama | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0740 | Photomerge Layout: Auto | dialog-option | Photomerge dialog | Analyzes and chooses Perspective, Cylindrical or Spherical | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0741 | Photomerge Layout: Perspective | dialog-option | Photomerge dialog | Reference image in center, others transformed | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0742 | Photomerge Layout: Cylindrical | dialog-option | Photomerge dialog | Reduces bow-tie distortion on a cylinder | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0743 | Photomerge Layout: Spherical | dialog-option | Photomerge dialog | Maps images on a sphere for 360 panoramas | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0744 | Photomerge Layout: Collage | dialog-option | Photomerge dialog | Aligns by rotation and scale only | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0745 | Photomerge Layout: Reposition | dialog-option | Photomerge dialog | Aligns by position only without distortion | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0746 | Photomerge: Blend Images Together | dialog-option | Photomerge dialog | Creates layer masks for seamless blending | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0747 | Photomerge: Vignette Removal | dialog-option | Photomerge dialog | Compensates edge darkening | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0748 | Photomerge: Geometric Distortion Correction | dialog-option | Photomerge dialog | Compensates lens distortion | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0749 | Photomerge: Content Aware Fill Transparent Areas | dialog-option | Photomerge dialog | Fills empty edges automatically | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0750 | Photomerge: Use Files, Folders, Add Open Files | dialog-option | Photomerge dialog | Source selection | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0751 | Auto-Align Layers | command | Edit > Auto-Align Layers | Aligns layers by content with Auto, Perspective, Collage, Cylindrical, Spherical, Reposition | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0752 | Auto-Blend Layers | command | Edit > Auto-Blend Layers | Panorama or Stack Images blending with Seamless Tones and Colors, Content Aware Fill | automation | https://helpx.adobe.com/photoshop/using/create-panoramic-images-photomerge.html |
| PS-B-0753 | Image Processor | command | File > Scripts | Converts and resizes folders of images to JPEG, PSD, TIFF | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0754 | Image Processor: Select images, Open first image to apply settings | dialog-option | File > Scripts | Source options | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0755 | Image Processor: Save in Same Location or Select Folder, Keep folder structure | dialog-option | File > Scripts | Destination | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0756 | Image Processor: Save as JPEG with Quality, Convert Profile to sRGB, Resize to Fit | dialog-option | File > Scripts | JPEG output | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0757 | Image Processor: Save as PSD with Maximize Compatibility, Resize to Fit | dialog-option | File > Scripts | PSD output | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0758 | Image Processor: Save as TIFF with LZW Compression, Resize to Fit | dialog-option | File > Scripts | TIFF output | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0759 | Image Processor: Run Action, Copyright Info, Include ICC Profile | dialog-option | File > Scripts | Preferences section | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0760 | Image Processor: Save and Load settings | dialog-option | File > Scripts | Stores processor settings as XML | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0761 | Delete All Empty Layers | command | File > Scripts | Removes empty layers | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0762 | Flatten All Layer Effects | command | File > Scripts | Rasterizes effects into layers | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0763 | Flatten All Masks | command | File > Scripts | Applies all masks to layers | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0764 | Layer Comps to Files | command | File > Scripts | Exports each layer comp to a file with format options | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0765 | Export Layers to Files | command | File > Scripts | Saves each layer to a separate file | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0766 | Export Layers to Files: Destination, File Name Prefix, Visible Layers Only, Trim Layers | dialog-option | File > Scripts | Export options | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0767 | Export Layers to Files: File Type BMP, JPEG, PDF, PSD, Targa, TIFF, PNG-8, PNG-24 with per-format options and ICC | dialog-option | File > Scripts | Output format | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0768 | Script Events Manager | command | File > Scripts | Runs scripts or actions on application events | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0769 | Script Events Manager: Enable Events to Run Scripts/Actions | dialog-option | File > Scripts | Master switch | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0770 | Script Events Manager: Photoshop Event | dialog-option | File > Scripts | Start Application, New Document, Open Document, Save Document, Close Document, Print Document, Export Document, Everything | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0771 | Script Events Manager: Script or Action choice | dialog-option | File > Scripts | Runs a JSX script or recorded action | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0772 | Load Files into Stack | command | File > Scripts | Opens multiple files as layers of one document | automation | https://helpx.adobe.com/photoshop/using/image-stacks.html |
| PS-B-0773 | Load Files into Stack: Attempt to Automatically Align Source Images | dialog-option | Load Layers dialog | Aligns stacked layers | automation | https://helpx.adobe.com/photoshop/using/image-stacks.html |
| PS-B-0774 | Load Files into Stack: Create Smart Object after Loading Layers | dialog-option | Load Layers dialog | Converts stack to Smart Object | automation | https://helpx.adobe.com/photoshop/using/image-stacks.html |
| PS-B-0775 | Load Multiple DICOM Files | command | File > Scripts | Loads a DICOM folder into a multi-frame document | format | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0776 | Statistics | command | File > Scripts | Creates an image stack Smart Object and applies a stack mode | automation | https://helpx.adobe.com/photoshop/using/image-stacks.html |
| PS-B-0777 | Stack modes | dialog-option | Layer > Smart Objects > Stack Mode | Entropy, Kurtosis, Maximum, Mean, Median, Minimum, Range, Skewness, Standard Deviation, Summation, Variance | automation | https://helpx.adobe.com/photoshop/using/image-stacks.html |
| PS-B-0778 | Browse (scripts) | command | File > Scripts | Runs an arbitrary JSX or JS script file | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0779 | ExtendScript (JSX) scripting | behavior | File > Scripts | JavaScript, AppleScript and VBScript automation through the scripting DOM | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0780 | Action Manager | behavior | File > Scripts | Low-level descriptor API for recording any command in scripts | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0781 | ScriptListener plug-in | behavior | File > Scripts | Logs Action Manager code for performed operations | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0782 | Startup scripts folder | behavior | File > Scripts | Scripts in Presets/Scripts appear in the menu and can auto-run | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0783 | UXP scripts (.psjs) | behavior | File > Scripts | Modern JavaScript scripts using the UXP API run from File > Scripts | automation | https://developer.adobe.com/photoshop/uxp/ |
| PS-B-0784 | UXP batchPlay | behavior | File > Scripts | Runs Action Manager descriptors from UXP code | automation | https://developer.adobe.com/photoshop/uxp/ |
| PS-B-0785 | Plugins panel | panel | Plugins menu | Lists installed UXP plugins and launches their panels | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0786 | Browse Plugins | command | Plugins menu | Opens Creative Cloud marketplace for plugins | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0787 | Manage Plugins | command | Plugins menu | Opens Creative Cloud desktop plugin management | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0788 | UXP plugin panels | behavior | Plugins menu | Plugins add dockable panels, commands and modal dialogs | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0789 | UXP Developer Tool | behavior | Plugins menu | Loads, debugs and packages plugins | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0790 | Legacy 8BF filter plug-ins | behavior | Plugins menu | Third-party C++ filter plug-ins load from the Plug-ins folder | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0791 | Legacy import/export plug-ins | behavior | Plugins menu | Format and acquire plug-ins via Photoshop plug-in SDK | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0792 | Generator | behavior | Preferences > Plug-ins | Node-based Generator plug-ins, used by Generate Image Assets | automation | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-0793 | Data-driven graphics | behavior | Image > Variables | Defines variables on layers and generates files from data sets | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0794 | Variables > Define | command | Image > Variables | Assigns Visibility, Text Replacement or Pixel Replacement variables to layers | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0795 | Pixel Replacement method | dialog-option | Variables dialog | Fit, Fill, As Is, Conform with alignment and Clip to Bounding Box | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0796 | Variables > Data Sets | command | Image > Variables | Creates, edits, imports and navigates data sets | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0797 | Import data set from text file | command | Import Data Set dialog | Loads CSV or tab-delimited data with first column as set names | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0798 | Export Data Sets as Files | command | File > Export | Renders a PSD for every data set | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0799 | Apply Data Set | command | Image > Apply Data Set | Applies current data set values to the document | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |

## Video, animation and legacy 3D

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0800 | Timeline panel | panel | Window > Timeline | Video timeline or frame animation mode panel | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0801 | Create Video Timeline | panel-option | Window > Timeline | Initializes a video timeline for the document | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0802 | Create Frame Animation | panel-option | Window > Timeline | Initializes frame-based animation | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0803 | Convert to Frame Animation or Video Timeline | panel-option | Window > Timeline | Switches modes | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0804 | Timeline: playhead and play controls | panel-option | Window > Timeline | Go to first frame, previous frame, play, next frame | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0805 | Timeline: Mute audio playback | panel-option | Window > Timeline | Toggles audio | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0806 | Timeline: Set playback options Resolution and Loop | panel-option | Window > Timeline | Preview resolution 25 to 100 percent and loop | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0807 | Timeline: Split at Playhead | panel-option | Window > Timeline | Splits the clip at the current time | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0808 | Timeline: Transitions | panel-option | Window > Timeline | Fade, Cross Fade, Fade with Black, Fade with White, Fade with Color with duration | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0809 | Timeline: Zoom slider | panel-option | Window > Timeline | Zooms time scale | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0810 | Timeline: Render Video button | panel-option | Window > Timeline | Opens Render Video | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0811 | Timeline: tracks | panel-option | Window > Timeline | Each layer or group is a track; groups become video groups | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0812 | Timeline: Add Media | panel-option | Window > Timeline | Adds video, image or audio to a track | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0813 | Timeline: Audio track | panel-option | Window > Timeline | Add audio clips with Volume, Fade In, Fade Out, Mute | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0814 | Timeline: Work area | panel-option | Window > Timeline | Start and end markers restrict playback and rendering | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0815 | Timeline: Clip duration and speed | panel-option | Window > Timeline | Right-click a clip to set duration and speed percentage | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0816 | Timeline: Motion | panel-option | Window > Timeline | Pan and Zoom, Rotate, Pan, Zoom, Rotate and Zoom with Resize to Fill Canvas | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0817 | Timeline: keyframes stopwatch | panel-option | Window > Timeline | Enables keyframing per property | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0818 | Keyframe properties | panel-option | Window > Timeline | Position, Opacity, Style, Layer Mask Position, Layer Mask Enable, Vector Mask, Transform, Text Warp, Global Lighting | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0819 | Keyframe interpolation Linear or Hold | panel-option | Window > Timeline | Interpolation per keyframe | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0820 | Timeline: Onion Skin | panel-option | Window > Timeline | Shows adjacent frames for animation | video | https://helpx.adobe.com/photoshop/using/creating-timeline-animations.html |
| PS-B-0821 | Onion Skin Settings | panel-option | Timeline panel menu | Frames before and after, frame spacing, max and min opacity, blend mode | video | https://helpx.adobe.com/photoshop/using/creating-timeline-animations.html |
| PS-B-0822 | Set Timeline Frame Rate | panel-option | Timeline panel menu | 8 to 60 fps presets or custom | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0823 | Timeline panel menu: Enable Timeline Shortcut Keys | panel-option | Window > Timeline | Enables arrow and space shortcuts | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0824 | Timeline panel menu: Allow Frame Skipping | panel-option | Window > Timeline | Skips frames to keep realtime playback | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0825 | Timeline: Comments track | panel-option | Timeline panel menu | Global timeline comments | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0826 | Export timeline comments | panel-option | Timeline panel menu | Exports comments as HTML or text | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0827 | Timeline: Lock and hide tracks | panel-option | Window > Timeline | Per-track lock and visibility | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0828 | New Video Layer from File | command | Layer > Video Layers | Imports a video file as a video layer | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0829 | New Blank Video Layer | command | Layer > Video Layers | Adds an empty video layer for frame-by-frame painting | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0830 | Insert Blank Frame | command | Layer > Video Layers | Inserts a blank frame at the current time | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0831 | Duplicate Frame | command | Layer > Video Layers | Duplicates the current video frame | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0832 | Delete Frame | command | Layer > Video Layers | Deletes the current video frame | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0833 | Replace Footage | command | Layer > Video Layers | Relinks the video layer to another file | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0834 | Interpret Footage | command | Layer > Video Layers | Sets Alpha Channel, Frame Rate, Color Profile, Pixel Aspect Ratio | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0835 | Show Altered Video | command | Layer > Video Layers | Shows or hides edits on video layers | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0836 | Restore Frame | command | Layer > Video Layers | Discards edits to the current frame | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0837 | Restore All Frames | command | Layer > Video Layers | Discards all video layer edits | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0838 | Reload Frame | command | Layer > Video Layers | Reloads the frame from source | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0839 | Rasterize video layer | command | Layer > Video Layers | Converts the current frame to pixels | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0840 | Pixel aspect ratio correction | behavior | View > Pixel Aspect Ratio | View > Pixel Aspect Ratio Correction previews nonsquare pixels | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0841 | Video Preview on external device | command | File > Export > Video Preview | Sends document preview to a connected device | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0842 | Video Frames to Layers | command | File > Import | Imports a range of video frames as layers | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0843 | Video Frames to Layers: From Beginning To End or Selected Range Only, Limit To Every n Frames, Make Frame Animation | dialog-option | File > Import | Import options | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-0844 | Render Video | command | File > Export > Render Video | Exports the timeline to video or image sequence | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0845 | Render Video: Name and Folder, Create New Subfolder | dialog-option | File > Export > Render Video | Output location | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0846 | Render Video: Adobe Media Encoder | dialog-option | File > Export > Render Video | H.264 MP4, DPX, QuickTime formats | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0847 | Render Video: Preset | dialog-option | File > Export > Render Video | High, Medium, Low quality and device presets | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0848 | Render Video: Size, Frame Rate, Field Order, Aspect, Color Manage | dialog-option | File > Export > Render Video | Video settings | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0849 | Render Video: Photoshop Image Sequence | dialog-option | File > Export > Render Video | PNG, JPEG, TIFF, PSD, DPX, OpenEXR, Targa, BMP sequences with Starting Number and Digits | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0850 | Render Video: Range All Frames, Start and End Frame, Work Area | dialog-option | File > Export > Render Video | Frame range | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0851 | Render Video: Render Options Alpha Channel None, Straight, Premultiplied with Black | dialog-option | File > Export > Render Video | Alpha handling | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0852 | Render Video: 3D Quality | dialog-option | File > Export > Render Video | Legacy option for 3D, removed | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0853 | Render Video: Audio Format and Quality | dialog-option | File > Export > Render Video | AAC with bitrate | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0854 | Frame animation: Duplicate selected frames | panel-option | Window > Timeline (frame mode) | Adds a new frame | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0855 | Frame animation: Frame delay | panel-option | Window > Timeline (frame mode) | Per-frame delay time | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0856 | Frame animation: Looping options | panel-option | Window > Timeline (frame mode) | Once, 3 Times, Forever, Other | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0857 | Tween | panel-option | Window > Timeline (frame mode) | Generates in-between frames for Position, Opacity, Effects | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0858 | Tween: Tween With, Frames to Add, Layers All or Selected, Parameters | dialog-option | Window > Timeline (frame mode) | Tween options | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0859 | New Layer Visible in All Frames | panel-option | Window > Timeline (frame mode) | Frame option for new layers | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0860 | Propagate Frame 1 | panel-option | Window > Timeline (frame mode) | Changes in first frame propagate to others | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0861 | Unify layer position, visibility, style buttons | panel-option | Window > Timeline (frame mode) | Layers panel unify options across frames | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0862 | Make Frames From Layers | panel-option | Window > Timeline (frame mode) | Creates one frame per layer | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0863 | Flatten Frames Into Layers | panel-option | Window > Timeline (frame mode) | Creates a layer per frame | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0864 | Match Layer Across Frames | panel-option | Window > Timeline (frame mode) | Copies layer properties to other frames | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0865 | Create New Layer for Each New Frame | panel-option | Window > Timeline (frame mode) | Auto new layer per frame | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0866 | Optimize Animation | panel-option | Window > Timeline (frame mode) | Bounding Box and Redundant Pixel Removal for GIF | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0867 | Reverse Frames | panel-option | Window > Timeline (frame mode) | Reverses frame order | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0868 | Select All Frames and Delete Animation | panel-option | Window > Timeline (frame mode) | Frame management | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0869 | Palette Options | panel-option | Window > Timeline (frame mode) | Frame thumbnail size | video | https://helpx.adobe.com/photoshop/using/creating-frame-animations.html |
| PS-B-0870 | Legacy 3D features removed | behavior | 3D menu (removed) | All 3D features were removed in Photoshop 25.x (July 2024); 3D files open as flattened layers | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |
| PS-B-0871 | 3D menu (removed) | command | 3D menu (removed) | Former commands New 3D Layer from File, Postcard, Mesh from Preset, Depth Map, Extrusion, Render, Export 3D Layer | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |
| PS-B-0872 | 3D panel (removed) | panel | 3D menu (removed) | Former scene, mesh, material and light panel | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |
| PS-B-0873 | 3D Print (removed) | command | 3D menu (removed) | Former 3D print settings and utilities | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |
| PS-B-0874 | 3D file formats (removed) | format | 3D menu (removed) | OBJ, 3DS, DAE, KMZ, U3D, STL, glTF import and export no longer supported | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |
| PS-B-0875 | Substance 3D Viewer integration | behavior | Photoshop (Beta) / Substance 3D Viewer | Adds 3D objects to 2D designs via the Substance 3D Viewer app with linked 3D layers | 3d | https://helpx.adobe.com/photoshop/using/filter-effects-reference.html |
| PS-B-0876 | Substance 3D materials in Photoshop | behavior | Plugins panel | Apply Substance materials to objects via plug-in | 3d | https://helpx.adobe.com/photoshop/using/plug-ins.html |

## File menu commands

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0877 | New | command | File > New | Opens the New Document dialog with presets and templates | core | https://helpx.adobe.com/photoshop/using/create-documents.html |
| PS-B-0878 | New Document: preset categories | dialog-option | New Document dialog | Recent, Saved, Photo, Print, Art and Illustration, Web, Mobile, Film and Video | core | https://helpx.adobe.com/photoshop/using/create-documents.html |
| PS-B-0879 | New Document: Adobe Stock templates | dialog-option | New Document dialog | Search and open templates | cloud | https://helpx.adobe.com/photoshop/using/create-documents.html |
| PS-B-0880 | New Document: Width, Height, Units, Orientation, Artboards | dialog-option | New Document dialog | Canvas settings | core | https://helpx.adobe.com/photoshop/using/create-documents.html |
| PS-B-0881 | New Document: Resolution, Color Mode, Bit Depth, Background Contents | dialog-option | New Document dialog | White, Black, Background Color, Transparent, Custom | core | https://helpx.adobe.com/photoshop/using/create-documents.html |
| PS-B-0882 | New Document: Advanced Color Profile and Pixel Aspect Ratio | dialog-option | New Document dialog | Profile and aspect settings | core | https://helpx.adobe.com/photoshop/using/create-documents.html |
| PS-B-0883 | New Document: Save preset | dialog-option | New Document dialog | Stores a custom document preset | core | https://helpx.adobe.com/photoshop/using/create-documents.html |
| PS-B-0884 | Use Legacy New Document Interface | preference | Preferences > General | Switches to the classic New dialog | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-0885 | Open | command | File menu | Opens files in supported formats | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0886 | Open from Cloud / Cloud Documents | command | File > Open | Browses cloud documents and search cloud files (27.9.1) | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-0887 | Open As | command | File > Open As | Opens a file forcing a specific format (Windows) | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0888 | Open as Smart Object | command | File > Open as Smart Object | Opens a file wrapped in a Smart Object | core | https://helpx.adobe.com/photoshop/using/create-smart-objects.html |
| PS-B-0889 | Open Recent | command | File > Open Recent | Lists recent files with Clear Recent File List | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0890 | Browse in Bridge | command | File > Browse in Bridge | Opens Adobe Bridge | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0891 | Close | command | File > Close | Closes the document | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0892 | Close All | command | File > Close All | Closes all documents | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0893 | Close Others | command | File > Close Others | Closes all but the active document | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0894 | Close and Go to Bridge | command | File > Close and Go to Bridge | Closes and switches to Bridge | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0895 | Save | command | File > Save | Saves to the current format or prompts | core | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-0896 | Save As | command | File > Save As | Saves under a new name or format; cloud or computer | core | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-0897 | Save a Copy | command | File > Save a Copy | Saves a copy in any format including flattening formats | core | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-0898 | Save As: As a Copy, Notes, Alpha Channels, Spot Colors, Layers | dialog-option | Save dialogs | Content inclusion options | core | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-0899 | Save As: Use Proof Setup, ICC Profile embed | dialog-option | Save dialogs | Color options | core | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-0900 | Customize file format list | dialog-option | Save dialogs | Reorder, show or hide formats in Save As and Save a Copy (27.10) | core | https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html |
| PS-B-0901 | Revert | command | File > Revert | Reverts to last saved state | core | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-0902 | Export > Quick Export As | command | File > Export | One-click export using Export preferences format | core | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-0903 | Export > Export As | command | File > Export | Opens the Export As dialog | core | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-0904 | Export > Export Preferences | command | File > Export | Sets quick export format and location | core | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-0905 | Export > Save for Web (Legacy) | command | File > Export | Legacy web optimization dialog | core | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-0906 | Export > Artboards to Files | command | File > Export | Exports each artboard to a file | core | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-0907 | Export > Artboards to PDF | command | File > Export | Exports artboards as PDF pages | core | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-0908 | Export > Layer Comps to Files | command | File > Export | Exports layer comps to files | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0909 | Export > Layer Comps to PDF | command | File > Export | Exports layer comps as a PDF | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0910 | Export > Layers to Files | command | File > Export | Exports layers to files | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0911 | Export > Color Lookup Tables | command | File > Export | Exports 3DL, CUBE, CSP, ICC LUTs from adjustment layers | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0912 | Color Lookup Tables: Description, Copyright, Quality grid points, formats | dialog-option | Export Color Lookup dialog | LUT export options | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0913 | Export > Data Sets as Files | command | File > Export | Exports variable data sets | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0914 | Export > Paths to Illustrator | command | File > Export | Exports paths to an AI file | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0915 | Export > Render Video | command | File > Export | Renders timeline video | video | https://helpx.adobe.com/photoshop/using/export-video-animation.html |
| PS-B-0916 | Export > Zoomify | command | File > Export | Exports tiled zoomable web images with HTML | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0917 | Zoomify: template, output location, image tile options quality, browser width and height | dialog-option | Zoomify dialog | Zoomify options | core | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-0918 | Generate > Image Assets | command | File > Generate | Generates web assets from layer names with suffixes | core | https://helpx.adobe.com/photoshop/using/generate-assets-layers.html |
| PS-B-0919 | Image Assets naming syntax | behavior | Layers panel | Layer names like 200% icon.png, 50x50 thumb.jpg8, folder/name.gif produce files | core | https://helpx.adobe.com/photoshop/using/generate-assets-layers.html |
| PS-B-0920 | Image Assets output folder | behavior | File > Generate | Assets saved to a document-assets folder next to the PSD, updated live | core | https://helpx.adobe.com/photoshop/using/generate-assets-layers.html |
| PS-B-0921 | Image Assets default settings layer | behavior | Layers panel | A layer named default with scale and folder specs sets defaults | core | https://helpx.adobe.com/photoshop/using/generate-assets-layers.html |
| PS-B-0922 | Search Adobe Stock | command | File > Search Adobe Stock | Opens Adobe Stock search panel inside Photoshop (27.10) | cloud | https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html |
| PS-B-0923 | Place Embedded | command | File > Place Embedded | Places a file as an embedded Smart Object | core | https://helpx.adobe.com/photoshop/using/placing-files.html |
| PS-B-0924 | Place Linked | command | File > Place Linked | Places a file as a linked Smart Object | core | https://helpx.adobe.com/photoshop/using/placing-files.html |
| PS-B-0925 | Always Create Smart Objects when Placing | preference | Preferences > General | Placed content becomes Smart Object | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-0926 | Resize Image During Place | preference | Preferences > General | Scales placed images to canvas | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-0927 | Skip Transform when Placing | preference | Preferences > General | Commits placement immediately | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-0928 | Package | command | File > Package | Collects linked files into a folder with the document | core | https://helpx.adobe.com/photoshop/using/create-smart-objects.html |
| PS-B-0929 | Automate submenu | command | File > Automate | Batch, PDF Presentation, Create Droplet, Crop and Straighten Photos, Contact Sheet II, Conditional Mode Change, Fit Image, Lens Correction, Merge to HDR Pro, Photomerge | automation | https://helpx.adobe.com/photoshop/using/processing-batch-files.html |
| PS-B-0930 | Scripts submenu | command | File > Scripts | Image Processor, Delete All Empty Layers, Flatten All Layer Effects, Flatten All Masks, Script Events Manager, Load Files into Stack, Load Multiple DICOM Files, Statistics, Browse | automation | https://helpx.adobe.com/photoshop/using/scripting.html |
| PS-B-0931 | Import > Variable Data Sets | command | File > Import | Imports data sets from text | automation | https://helpx.adobe.com/photoshop/using/creating-data-driven-graphics.html |
| PS-B-0932 | Import > Video Frames to Layers | command | File > Import | Imports video frames as layers | video | https://helpx.adobe.com/photoshop/using/video-animation-overview.html |
| PS-B-0933 | Import > Notes | command | File > Import | Imports annotations from PDF or FDF | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0934 | Import > WIA Support | command | File > Import | Acquires images from WIA scanners and cameras (Windows) | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0935 | Import > Images from Device | command | File > Import | Imports from connected device (macOS) | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0936 | Import from iPhone or iPad | command | File > Import | Continuity camera import (macOS) | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0937 | File Info | command | File > File Info | Metadata editor | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0938 | Version History | command | File > Version History | Shows cloud document versions to revert or save | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-0939 | Print | command | File > Print | Opens Print Settings | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-0940 | Print One Copy | command | File > Print One Copy | Prints with current settings without a dialog | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-0941 | Exit | command | File > Exit | Quits Photoshop | core | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-0942 | Recovery auto-save | behavior | Preferences > File Handling | Automatically saves recovery info at intervals | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-0943 | Background saving | behavior | Preferences > File Handling | Saves in the background allowing continued work | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-0944 | Drag and drop to open or place | behavior | Canvas | Dragging files opens them or places them into the open document | core | https://helpx.adobe.com/photoshop/using/placing-files.html |
| PS-B-0945 | Open multiple files and tabs | behavior | Workspace | Documents open as tabs by default | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-0946 | File Info: Basic | dialog-option | File > File Info | Document Title, Author, Author Title, Description, Rating, Description Writer, Keywords, Copyright Status, Copyright Notice, Copyright Info URL | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0947 | File Info: Camera Data | dialog-option | File > File Info | EXIF camera settings read-only | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0948 | File Info: Origin | dialog-option | File > File Info | Date Created, City, State, Country, Credit, Source, Headline, Instructions, Transmission Reference, Urgency | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0949 | File Info: IPTC | dialog-option | File > File Info | IPTC Core contact and content fields | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0950 | File Info: IPTC Extension | dialog-option | File > File Info | Extended IPTC rights and model release fields | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0951 | File Info: GPS Data | dialog-option | File > File Info | GPS coordinates read-only | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0952 | File Info: Audio Data and Video Data | dialog-option | File > File Info | Media metadata fields | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0953 | File Info: Photoshop | dialog-option | File > File Info | Photoshop-specific history and document info | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0954 | File Info: DICOM | dialog-option | File > File Info | Medical imaging metadata | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0955 | File Info: Raw Data | dialog-option | File > File Info | Raw XMP view | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0956 | File Info: Templates import and export | dialog-option | File > File Info | Save and apply metadata templates | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0957 | Notes tool annotations | behavior | Notes panel | Text notes stored in PSD, PDF | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |
| PS-B-0958 | Notes panel | panel | Window > Notes | Views and navigates notes with author and color | core | https://helpx.adobe.com/photoshop/using/metadata-notes.html |

## File formats and format options

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-0959 | Photoshop PSD | format | File > Save As / Open | Native layered format up to 30000 px, all features preserved | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0960 | PSD: Maximize Compatibility | format-option | Preferences > File Handling | Stores a flattened composite for other apps and older versions | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0961 | PSD: Layers, Alpha Channels, Spot Colors, Notes, ICC | format-option | File > Save As / Open | Content preserved in PSD | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0962 | Large Document Format PSB | format | File > Save As | Layered format up to 300000 px and files beyond 2 GB | format | https://helpx.adobe.com/photoshop/using/saving-large-documents.html |
| PS-B-0963 | Enable Large Document Format | preference | Preferences > File Handling | Historical toggle; PSB now always available | format | https://helpx.adobe.com/photoshop/using/saving-large-documents.html |
| PS-B-0964 | Photoshop Cloud Document PSDC | format | File > Save As | Cloud-synced PSD with versions and offline caching | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-0965 | TIFF | format | File > Save As / Open | Layered or flat tagged image format up to 4 GB | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0966 | TIFF: Image Compression None, LZW, ZIP, JPEG | format-option | File > Save As / Open | Composite compression | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0967 | TIFF: Pixel Order Interleaved or Per Channel | format-option | File > Save As / Open | Channel ordering | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0968 | TIFF: Byte Order IBM PC or Macintosh | format-option | File > Save As / Open | Endianness | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0969 | TIFF: Save Image Pyramid | format-option | File > Save As / Open | Multiresolution pyramid | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0970 | TIFF: Save Transparency | format-option | File > Save As / Open | Stores transparency as alpha | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0971 | TIFF: Layer Compression RLE, ZIP, Discard Layers and Save a Copy | format-option | File > Save As / Open | Layer data handling | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0972 | TIFF: 32-bit float with Predictor | format-option | File > Save As / Open | Floating point and predictor for 16 and 32 bit | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0973 | Ask Before Saving Layered TIFF Files | preference | Preferences > File Handling | Prompts when saving layered TIFF | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0974 | JPEG | format | File > Save As / Open | Lossy 8-bit baseline or progressive format | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0975 | JPEG: Matte | format-option | File > Save As / Open | Background color for transparency | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0976 | JPEG: Quality 0 to 12 | format-option | File > Save As / Open | Low, Medium, High, Maximum presets | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0977 | JPEG: Format Options Baseline Standard, Baseline Optimized, Progressive with Scans 3 to 5 | format-option | File > Save As / Open | Encoding style | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0978 | JPEG: Size estimate | format-option | File > Save As / Open | File size at modem speeds | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0979 | JPEG 2000 JPF | format | File > Save As / Open | Wavelet format with lossless and lossy options (optional plug-in) | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0980 | JPEG 2000: Lossless, Quality, Fast Mode, Include Metadata, Include Transparency, Include Color Profile | format-option | File > Save As / Open | Encoding options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0981 | JPEG 2000: JP2 Compatible, Tile Size, Wavelet Filter, Order Progression, Region of Interest, Advanced Optimization | format-option | File > Save As / Open | Advanced options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0982 | JPEG XL | format | File > Save As | Modern HDR-capable format supported for open and save, including 8, 16, 32 bit | format | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-B-0983 | JPEG XL: Quality, Lossless, Effort | format-option | File > Save As / Open | Encoder settings | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0984 | PNG | format | File > Save As / Open | Lossless raster with transparency | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0985 | PNG: Compression Smallest/Slow, Medium, Fastest/Large | format-option | File > Save As / Open | Compression choice | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0986 | PNG: Interlace None or Interlaced | format-option | File > Save As / Open | Progressive display | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0987 | PNG: Save transparency and metadata | format-option | File > Save As / Open | Content options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0988 | PNG: 16-bit export | format-option | File > Save As / Open | Saves 16 bits per channel | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0989 | PNG HDR (CICP and gain map) | format-option | File > Save As / Open | HDR metadata in PNG | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0990 | GIF | format | File > Save As / Open | Indexed 8-bit with transparency and animation | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0991 | GIF: Indexed Color conversion | format-option | File > Save As / Open | Palette, Colors, Forced, Transparency, Matte, Dither, Amount, Preserve Exact Colors | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0992 | GIF: Row Order Normal or Interlaced | format-option | File > Save As / Open | Interlacing | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0993 | WebP | format | File > Save As / Open | Lossless and lossy web format with transparency | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0994 | WebP: Lossless, Lossy with Quality, Include XMP and EXIF | format-option | File > Save As / Open | Encoding options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0995 | AVIF | format | File > Save As / Open | AV1 image format with HDR support | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0996 | AVIF: Quality, bit depth 8/10/12, HDR PQ or HLG | format-option | File > Save As / Open | Encoding options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0997 | HEIF/HEIC | format | File > Save As / Open | High Efficiency Image Format with 8 and 16 bit | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0998 | HEIF: Quality, bit depth, color profile, HDR | format-option | File > Save As / Open | Encoding options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-0999 | BMP | format | File > Save As / Open | Windows bitmap | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1000 | BMP: File Format Windows or OS/2, Depth 1,4,8,16,24,32, Compress RLE, Flip row order, Advanced Modes | format-option | File > Save As / Open | BMP options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1001 | DICOM | format | File > Save As / Open | Medical imaging format open, edit, save | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1002 | DICOM: Import frames as layers or N-up, Anonymize, Show overlays, Window Width and Level | format-option | File > Save As / Open | DICOM open and save options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1003 | OpenEXR | format | File > Save As / Open | High dynamic range 32-bit format | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1004 | OpenEXR: Compression None, RLE, ZIP, PIZ, PXR24, B44 | format-option | File > Save As / Open | Compression choices | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1005 | OpenEXR: Half or Float, alpha channel | format-option | File > Save As / Open | Data type and alpha | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1006 | Radiance HDR | format | File > Save As / Open | 32-bit HDR format | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1007 | Portable Bit Map | format | File > Save As / Open | PBM, PGM, PPM, PNM, PFM, PAM family | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1008 | Portable Bit Map: Encoding Binary or ASCII | format-option | File > Save As / Open | Encoding choice | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1009 | PCX | format | File > Save As / Open | Legacy PC Paintbrush format | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1010 | Pixar | format | File > Save As / Open | PXR format for Pixar workstations | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1011 | Photoshop Raw | format | File > Save As / Open | Headerless raw bytes format | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1012 | Photoshop Raw: Header size, Interleaved order, Byte order, channels and dimensions on open | format-option | File > Save As / Open | Raw layout options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1013 | Targa | format | File > Save As / Open | TGA format for video and games | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1014 | Targa: Resolution 16, 24, 32 bits per pixel, Compress RLE | format-option | File > Save As / Open | TGA options | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1015 | IFF | format | File > Save As / Open | Amiga Interchange File Format | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1016 | Photoshop PDF | format | File > Save As | PDF preserving Photoshop editing capabilities | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1017 | Photoshop EPS | format | File > Save As | Encapsulated PostScript | format | https://helpx.adobe.com/photoshop/using/saving-files-graphics-formats.html |
| PS-B-1018 | EPS: Preview TIFF 1 bit or 8 bit, None | format-option | EPS Options | Preview options | format | https://helpx.adobe.com/photoshop/using/saving-files-graphics-formats.html |
| PS-B-1019 | EPS: Encoding ASCII, ASCII85, Binary, JPEG | format-option | EPS Options | Data encoding | format | https://helpx.adobe.com/photoshop/using/saving-files-graphics-formats.html |
| PS-B-1020 | EPS: Include Halftone Screen, Transfer Function, PostScript Color Management, Include Vector Data, Image Interpolation | format-option | EPS Options | Print options | format | https://helpx.adobe.com/photoshop/using/saving-files-graphics-formats.html |
| PS-B-1021 | Photoshop DCS 1.0 and 2.0 | format | File > Save As | Desktop Color Separations with spot channels | format | https://helpx.adobe.com/photoshop/using/saving-files-graphics-formats.html |
| PS-B-1022 | DCS 2.0: Single File or Multiple Files, with or without composite | format-option | DCS Options | Separation packaging | format | https://helpx.adobe.com/photoshop/using/saving-files-graphics-formats.html |
| PS-B-1023 | Scitex CT | format | File > Save As | Scitex continuous tone format | format | https://helpx.adobe.com/photoshop/using/saving-files-graphics-formats.html |
| PS-B-1024 | Photoshop 2.0 (Mac) | format | File > Save As / Open | Legacy PSD 2.0 compatible format | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1025 | Multi-Picture Format MPO | format | File > Save As / Open | Stereo image format read support | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1026 | Camera Raw formats | format | File > Open | Raw files from supported cameras open through Camera Raw | format | https://helpx.adobe.com/photoshop/using/camera-raw.html |
| PS-B-1027 | DNG | format | File > Open | Digital Negative raw open, and save via Camera Raw | format | https://helpx.adobe.com/photoshop/using/camera-raw.html |
| PS-B-1028 | PDF open (Import PDF) | format | File > Open | Opens PDF pages or images with crop, resolution, mode | format | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-1029 | Import PDF: Select Pages or Images, Crop To, Anti-aliased, Image Size, Mode, Bit Depth, Suppress Warnings | dialog-option | Import PDF dialog | PDF open options | format | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-1030 | EPS and AI open (rasterize) | format | File > Open | Rasterizes generic EPS, AI with size and anti-aliasing | format | https://helpx.adobe.com/photoshop/using/opening-importing-images.html |
| PS-B-1031 | SVG open | format | File > Open | Opens SVG files as rasterized or vector layers | format | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-B-1032 | SVG export | format | File > Export As | Export As SVG for vector shape layers | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1033 | Video files open | format | File > Open | MOV, MP4, AVI, MPEG open as video layers | video | https://helpx.adobe.com/photoshop/using/video-layers.html |
| PS-B-1034 | 16 and 32 bit format support matrix | behavior | Save dialogs | Each format limits bit depths and modes; unavailable formats hidden in Save As | format | https://helpx.adobe.com/photoshop/using/file-formats.html |
| PS-B-1035 | Save a Copy for flattening formats | behavior | Save dialogs | Formats that cannot store layers appear only in Save a Copy by default | format | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-1036 | Enable legacy Save As | preference | Preferences > File Handling | Restores pre-2021 Save As behavior listing all formats | format | https://helpx.adobe.com/photoshop/using/saving-images.html |
| PS-B-1037 | PDF: Adobe PDF Preset | format-option | File > Save As > Photoshop PDF | High Quality Print, PDF/X-1a, PDF/X-3, PDF/X-4, Press Quality, Smallest File Size and custom | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1038 | PDF: Standard | format-option | File > Save As > Photoshop PDF | None, PDF/X-1a:2001, PDF/X-1a:2003, PDF/X-3:2002, PDF/X-3:2003, PDF/X-4:2010 | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1039 | PDF: Compatibility | format-option | File > Save As > Photoshop PDF | Acrobat 4 to Acrobat 8 (PDF 1.3 to 1.7) | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1040 | PDF General: Preserve Photoshop Editing Capabilities | format-option | File > Save As > Photoshop PDF | Embeds PSD data for reopening | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1041 | PDF General: Embed Page Thumbnails | format-option | File > Save As > Photoshop PDF | Adds thumbnails | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1042 | PDF General: Optimize for Fast Web Preview | format-option | File > Save As > Photoshop PDF | Linearizes the PDF | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1043 | PDF General: View PDF After Saving | format-option | File > Save As > Photoshop PDF | Opens result | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1044 | PDF Compression: downsampling | format-option | File > Save As > Photoshop PDF | Do Not Downsample, Average, Subsampling, Bicubic with target ppi and threshold | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1045 | PDF Compression: None, ZIP, JPEG, JPEG2000 with Image Quality and Tile Size | format-option | File > Save As > Photoshop PDF | Compression choice | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1046 | PDF Compression: Convert 16 Bit/Channel Image to 8 Bits/Channel | format-option | File > Save As > Photoshop PDF | Bit depth reduction | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1047 | PDF Output: Color Conversion and Destination | format-option | File > Save As > Photoshop PDF | No Conversion, Convert to Destination, Convert to Destination Preserve Numbers | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1048 | PDF Output: Profile Inclusion Policy | format-option | File > Save As > Photoshop PDF | Include or omit ICC profiles | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1049 | PDF Output: Output Intent Profile Name, Output Condition, Registry Name | format-option | File > Save As > Photoshop PDF | PDF/X output intent | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1050 | PDF Security: Document Open Password | format-option | File > Save As > Photoshop PDF | Requires password to open | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1051 | PDF Security: Permissions Password, Printing Allowed, Changes Allowed, Enable copying, Enable text access, Enable plaintext metadata | format-option | File > Save As > Photoshop PDF | Restricts actions | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1052 | PDF Security: Encryption Level | format-option | File > Save As > Photoshop PDF | 40-bit RC4 to 256-bit AES per compatibility | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1053 | PDF Summary | format-option | File > Save As > Photoshop PDF | Lists settings and warnings | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1054 | PDF: Save Preset and Load PDF presets | format-option | File > Save As > Photoshop PDF | Manages joboptions presets | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1055 | Adobe PDF Presets | command | Edit > Adobe PDF Presets | Edits shared PDF presets | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1056 | Export As: File Settings Format | dialog-option | File > Export > Export As | PNG, JPG, GIF, SVG, plus newer web formats such as WebP where supported | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1057 | Export As: Transparency | dialog-option | File > Export > Export As | Keeps alpha for PNG and GIF | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1058 | Export As: Smaller File 8-bit PNG | dialog-option | File > Export > Export As | Palette PNG output | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1059 | Export As: JPG Quality | dialog-option | File > Export > Export As | Percentage quality | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1060 | Export As: Image Size Width, Height, Scale, Resample | dialog-option | File > Export > Export As | Resize with Bicubic, Bilinear, Nearest Neighbor, Bicubic Smoother, Sharper | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1061 | Export As: Canvas Size | dialog-option | File > Export > Export As | Changes export canvas | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1062 | Export As: Scale All multiples with suffix | dialog-option | File > Export > Export As | Exports multiple sizes like 1x, 2x, 3x | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1063 | Export As: Metadata None, Copyright and Contact Info | dialog-option | File > Export > Export As | Metadata inclusion | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1064 | Export As: Color Space Convert to sRGB and Embed Color Profile | dialog-option | File > Export > Export As | Color handling | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1065 | Export As: preview and file size | dialog-option | File > Export > Export As | Live preview with estimated size | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1066 | Export As: multiple layers and artboards list | dialog-option | File > Export > Export As | Exports each selected layer or artboard with individual settings | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1067 | Export As: Content Credentials | dialog-option | Export As dialog | Attaches credentials to exported files | ai | https://helpx.adobe.com/photoshop/using/content-credentials.html |
| PS-B-1068 | Export layer via Layers panel context menu | command | Layers panel | Quick Export As PNG or Export As for layers | format | https://helpx.adobe.com/photoshop/using/export-artboards-layers.html |
| PS-B-1069 | Export: Quick Export Format and quality | preference | Preferences > Export | Format for Quick Export | format | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1070 | Export: Quick Export Location | preference | Preferences > Export | Save next to document in assets folder or ask each time | format | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1071 | Export: Metadata and Color Space defaults | preference | Preferences > Export | Default metadata inclusion and sRGB conversion | format | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1072 | Export: Use legacy Export As | preference | Preferences > Export | Uses the older Export As dialog | format | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1073 | SFW: Original, Optimized, 2-Up, 4-Up views | dialog-option | File > Export > Save for Web (Legacy) | Comparison views | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1074 | SFW: Preset menu and optimize to file size | dialog-option | File > Export > Save for Web (Legacy) | Named presets and Optimize to File Size | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1075 | SFW: GIF options | dialog-option | File > Export > Save for Web (Legacy) | Color reduction algorithm Perceptual, Selective, Adaptive, Restrictive, Custom, Black-White, Grayscale, Mac OS, Windows; Colors; Dither method and amount; Transparency; Matte; Transparency dither; Interlaced; Web Snap; Lossy | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1076 | SFW: PNG-8 options | dialog-option | File > Export > Save for Web (Legacy) | Same color table options as GIF without lossy | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1077 | SFW: PNG-24 options | dialog-option | File > Export > Save for Web (Legacy) | Transparency, Matte, Interlaced | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1078 | SFW: JPEG options | dialog-option | File > Export > Save for Web (Legacy) | Quality, Optimized, Progressive, Blur, Matte, Embed Color Profile | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1079 | SFW: WBMP option | dialog-option | File > Export > Save for Web (Legacy) | 1-bit wireless bitmap with dither | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1080 | SFW: Color Table | dialog-option | File > Export > Save for Web (Legacy) | Lock, shift to web, add eyedropper color, delete, sort, save and load palettes | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1081 | SFW: Image Size | dialog-option | File > Export > Save for Web (Legacy) | Resize with quality at export | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1082 | SFW: Animation controls | dialog-option | File > Export > Save for Web (Legacy) | Looping and frame preview for GIF | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1083 | SFW: Metadata None, Copyright, Copyright and Contact Info, All Except Camera Info, All | dialog-option | File > Export > Save for Web (Legacy) | Metadata | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1084 | SFW: Convert to sRGB and Preview | dialog-option | File > Export > Save for Web (Legacy) | Monitor Color, Legacy Macintosh, Internet Standard RGB, Document Profile | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1085 | SFW: Preview in browser and download time | dialog-option | File > Export > Save for Web (Legacy) | Browser preview and connection speed estimate | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1086 | SFW: Slice select and slice options | dialog-option | Save for Web dialog | Per-slice optimization | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |
| PS-B-1087 | SFW: Output Settings | dialog-option | File > Export > Save for Web (Legacy) | HTML, Slices, Background, Saving Files options | format | https://helpx.adobe.com/photoshop/using/optimizing-images.html |
| PS-B-1088 | SFW: Save as HTML and Images | dialog-option | Save for Web dialog | Writes HTML with sliced images | format | https://helpx.adobe.com/photoshop/using/slicing-web-pages.html |

## Print, proofing and color management

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-1089 | Print: Printer selection and Print Settings | dialog-option | File > Print | Chooses printer and opens driver settings | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1090 | Print: Copies | dialog-option | File > Print | Number of copies | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1091 | Print: Layout Portrait or Landscape | dialog-option | File > Print | Page orientation buttons | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1092 | Print: preview with Match Print Colors, Gamut Warning, Show Paper White | dialog-option | Print dialog | Soft proof preview options | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1093 | Print Color Management: Color Handling | dialog-option | Print dialog | Printer Manages Colors, Photoshop Manages Colors, Separations, No Color Management | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1094 | Print Color Management: Printer Profile | dialog-option | Print dialog | ICC profile for printer and paper | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1095 | Print Color Management: Normal Printing or Hard Proofing | dialog-option | Print dialog | Chooses output or simulation of another device | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1096 | Print Color Management: Rendering Intent | dialog-option | Print dialog | Perceptual, Saturation, Relative Colorimetric, Absolute Colorimetric | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1097 | Print Color Management: Black Point Compensation | dialog-option | Print dialog | Maps black points | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1098 | Print Color Management: Proof Setup, Simulate Paper Color, Simulate Black Ink | dialog-option | Print dialog | Hard proof options | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1099 | Print Color Management: 16-bit output (macOS) | dialog-option | Print dialog | Sends 16-bit data to supported drivers | print | https://helpx.adobe.com/photoshop/using/printing-color-management.html |
| PS-B-1100 | Print: Description | dialog-option | File > Print | Explains the selected option | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1101 | Position and Size: Center | dialog-option | File > Print | Centers image on page | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1102 | Position and Size: Top and Left | dialog-option | File > Print | Manual position | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1103 | Position and Size: Scale to Fit Media | dialog-option | File > Print | Fits image to printable area | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1104 | Position and Size: Scale, Height, Width | dialog-option | File > Print | Print size scaling | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1105 | Position and Size: Print Resolution | dialog-option | File > Print | Shows effective ppi | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1106 | Position and Size: Print Selected Area | dialog-option | File > Print | Crop handles to print part of the image | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1107 | Position and Size: Units | dialog-option | File > Print | Measurement units | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1108 | Printing Marks: Corner Crop Marks | dialog-option | File > Print | Marks for trimming corners | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1109 | Printing Marks: Center Crop Marks | dialog-option | File > Print | Marks at center of each edge | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1110 | Printing Marks: Registration Marks | dialog-option | File > Print | Bullseyes and star targets for aligning separations | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1111 | Printing Marks: Description | dialog-option | File > Print | Prints description from File Info | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1112 | Printing Marks: Labels | dialog-option | File > Print | Prints file and channel names | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1113 | Printing Marks: Edit description | dialog-option | File > Print | Edits description text | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1114 | Functions: Emulsion Down | dialog-option | File > Print | Flips emulsion side | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1115 | Functions: Negative | dialog-option | File > Print | Prints inverted output | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1116 | Functions: Background | dialog-option | File > Print | Page color outside the image | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1117 | Functions: Border | dialog-option | File > Print | Black border width | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1118 | Functions: Bleed | dialog-option | File > Print | Crop marks inside the image by bleed width | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1119 | PostScript Options: Calibration Bars | dialog-option | File > Print | 11-step grayscale and color bars | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1120 | PostScript Options: Interpolation | dialog-option | File > Print | Resamples low-res images on PostScript Level 2 printers | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1121 | PostScript Options: Include Vector Data | dialog-option | File > Print | Sends vector data for resolution-independent output | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1122 | PostScript Options: Transfer function | dialog-option | Transfer Functions dialog | Compensates dot gain | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1123 | PostScript Options: Halftone Screen | dialog-option | Halftone Screens dialog | Frequency, angle, dot shape per ink | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1124 | Print: Remember settings and Done | dialog-option | File > Print | Saves settings without printing | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1125 | Print: Send 16-bit data | dialog-option | File > Print | Higher precision output where driver supports | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1126 | Print spot channels | behavior | File > Print | Spot colors print as separate plates in Separations mode | print | https://helpx.adobe.com/photoshop/using/printing-photoshop.html |
| PS-B-1127 | Proof Setup: Custom | command | View > Proof Setup | Defines a proof condition | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1128 | Customize Proof Condition: Device to Simulate | dialog-option | View > Proof Setup | Target output profile | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1129 | Customize Proof Condition: Preserve Numbers | dialog-option | View > Proof Setup | Simulates without conversion | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1130 | Customize Proof Condition: Rendering Intent and Black Point Compensation | dialog-option | View > Proof Setup | Conversion settings | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1131 | Customize Proof Condition: Simulate Paper Color and Simulate Black Ink | dialog-option | View > Proof Setup | Display simulation options | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1132 | Customize Proof Condition: Save and Load | dialog-option | View > Proof Setup | Stores proof presets | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1133 | Proof Setup: Working CMYK | command | View > Proof Setup | Soft proof against working CMYK | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1134 | Proof Setup: Working Cyan, Magenta, Yellow, Black, CMY Plates | command | View > Proof Setup | Proofs individual plates | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1135 | Proof Setup: Legacy Macintosh RGB, Internet Standard RGB, Monitor RGB | command | View > Proof Setup | RGB proof conditions | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1136 | Proof Setup: Color Blindness Protanopia and Deuteranopia | command | View > Proof Setup | Simulates color vision deficiency | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1137 | Proof Colors | command | View > Proof Colors | Toggles soft proofing on the canvas | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1138 | Gamut Warning | command | View > Gamut Warning | Highlights colors outside the proof gamut | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1139 | Gamut Warning color and opacity | preference | Preferences > Transparency & Gamut | Sets overlay appearance | print | https://helpx.adobe.com/photoshop/using/proofing-colors.html |
| PS-B-1140 | Color Settings | command | Edit > Color Settings | Global color management configuration | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1141 | Color Settings: Settings preset | dialog-option | Edit > Color Settings | North America General Purpose 2, Prepress, Web/Internet, Europe, Japan presets and custom | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1142 | Working Spaces: RGB | dialog-option | Edit > Color Settings | sRGB, Adobe RGB, ProPhoto RGB, Display P3, Rec.2020 and others | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1143 | Working Spaces: CMYK | dialog-option | Edit > Color Settings | U.S. Web Coated SWOP, Coated FOGRA39, Japan Color and custom CMYK | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1144 | Working Spaces: Gray | dialog-option | Edit > Color Settings | Dot Gain percentages or Gray Gamma | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1145 | Working Spaces: Spot | dialog-option | Edit > Color Settings | Dot gain for spot channels | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1146 | Color Management Policies: RGB, CMYK, Gray | dialog-option | Edit > Color Settings | Off, Preserve Embedded Profiles, Convert to Working | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1147 | Profile Mismatches: Ask When Opening, Ask When Pasting | dialog-option | Edit > Color Settings | Mismatch prompts | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1148 | Missing Profiles: Ask When Opening | dialog-option | Edit > Color Settings | Prompts to assign profile | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1149 | Conversion Options: Engine | dialog-option | Edit > Color Settings | Adobe ACE or system CMM | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1150 | Conversion Options: Intent | dialog-option | Edit > Color Settings | Default rendering intent | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1151 | Conversion Options: Use Black Point Compensation | dialog-option | Edit > Color Settings | Default BPC | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1152 | Conversion Options: Use Dither (8-bit/channel images) | dialog-option | Edit > Color Settings | Reduces banding in conversions | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1153 | Conversion Options: Compensate for Scene-referred Profiles | dialog-option | Edit > Color Settings | Video profile handling | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1154 | Advanced: Desaturate Monitor Colors By | dialog-option | Edit > Color Settings | Desaturates display for wide gamut | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1155 | Advanced: Blend RGB Colors Using Gamma | dialog-option | Edit > Color Settings | Blends layers with specified gamma | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1156 | Advanced: Blend Text Colors Using Gamma | dialog-option | Edit > Color Settings | Text anti-aliasing gamma | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1157 | Custom CMYK | dialog-option | Edit > Color Settings | Ink Colors, Dot Gain, Separation Type GCR or UCR, Black Generation, Black Ink Limit, Total Ink Limit, UCA Amount | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1158 | Color Settings: Save and Load .csf | dialog-option | Edit > Color Settings | Share settings files | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1159 | Synchronize color settings with Creative Cloud apps | behavior | Edit > Color Settings | Bridge synchronizes Color Settings across apps | core | https://helpx.adobe.com/photoshop/using/color-settings.html |
| PS-B-1160 | Assign Profile | command | Edit > Assign Profile | Changes interpretation without converting pixels | core | https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html |
| PS-B-1161 | Assign Profile: Don't Color Manage, Working RGB, Profile | dialog-option | Assign Profile dialog | Assign choices | core | https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html |
| PS-B-1162 | Convert to Profile | command | Edit > Convert to Profile | Converts pixel values to a destination profile | core | https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html |
| PS-B-1163 | Convert to Profile: Destination Space Profile | dialog-option | Convert to Profile dialog | Target profile | core | https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html |
| PS-B-1164 | Convert to Profile: Engine, Intent, Black Point Compensation, Dither, Flatten Image, Advanced multichannel | dialog-option | Convert to Profile dialog | Conversion settings | core | https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html |
| PS-B-1165 | Embedded profile indicator | behavior | Document window | Status bar and title show the document profile | core | https://helpx.adobe.com/photoshop/using/working-with-color-profiles.html |

## Keyboard Shortcuts and Menus, Toolbar, Presets

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-1166 | Keyboard Shortcuts and Menus dialog | command | Edit > Keyboard Shortcuts | Customizes shortcuts and menu visibility and color | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1167 | Shortcuts For: Application Menus | dialog-option | Edit > Keyboard Shortcuts | Assigns shortcuts to menu commands | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1168 | Shortcuts For: Panel Menus | dialog-option | Edit > Keyboard Shortcuts | Assigns shortcuts to panel menu commands | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1169 | Shortcuts For: Tools | dialog-option | Edit > Keyboard Shortcuts | Assigns single-letter tool shortcuts | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1170 | Shortcuts For: Taskspaces | dialog-option | Edit > Keyboard Shortcuts | Shortcuts for Select and Mask, Content-Aware Fill workspaces | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1171 | Shortcut Set | dialog-option | Edit > Keyboard Shortcuts | Photoshop Defaults or custom named sets; Save, Save As, Delete | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1172 | Accept, Undo, Use Default, Add Shortcut, Delete Shortcut | dialog-option | Edit > Keyboard Shortcuts | Per-command shortcut editing | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1173 | Summarize | dialog-option | Edit > Keyboard Shortcuts | Exports all shortcuts to an HTML file | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1174 | Conflict warning | dialog-option | Edit > Keyboard Shortcuts | Warns when a shortcut is already used and offers to reassign | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1175 | Use Legacy Undo Shortcuts | dialog-option | Edit > Keyboard Shortcuts | Restores Ctrl+Z toggle and Ctrl+Alt+Z step backward | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1176 | Use Legacy Channel Shortcuts | dialog-option | Edit > Keyboard Shortcuts | Ctrl+1 to 5 select channels | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1177 | Menus tab: Visibility | dialog-option | Edit > Menus | Hides individual menu items (Show All Menu Items to reveal) | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1178 | Menus tab: Color | dialog-option | Edit > Menus | Highlights menu items with a color | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1179 | Menu set | dialog-option | Edit > Menus | Saves named menu customization sets | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1180 | Workspace stores shortcuts and menus | behavior | Window > Workspace | New Workspace can capture keyboard shortcuts and menus | core | https://helpx.adobe.com/photoshop/using/customizing-keyboard-shortcuts.html |
| PS-B-1181 | Customize Toolbar | command | Edit > Toolbar | Drag tools between the toolbar and Extra Tools list | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-B-1182 | Toolbar: group and ungroup tools | dialog-option | Edit > Toolbar | Arrange tools into flyout groups | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-B-1183 | Toolbar: Restore Defaults | dialog-option | Edit > Toolbar | Resets tool layout | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-B-1184 | Toolbar: Clear Tools | dialog-option | Edit > Toolbar | Moves all tools to Extra Tools | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-B-1185 | Toolbar: Save Preset and Load Preset | dialog-option | Edit > Toolbar | Stores custom toolbar layouts | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-B-1186 | Toolbar: show or hide Extra Tools, Foreground/Background, Quick Mask, Screen Mode buttons | dialog-option | Edit > Toolbar | Toggles bottom toolbar controls | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-B-1187 | Toolbar single or double column | behavior | Edit > Toolbar | Double arrow toggles toolbar columns | core | https://helpx.adobe.com/photoshop/desktop/get-started/set-up-toolbars-panels/customize-the-toolbar.html |
| PS-B-1188 | Preset Manager | command | Edit > Presets | Manages Brushes, Swatches, Gradients, Styles, Patterns, Contours, Custom Shapes, Tools presets | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1189 | Preset Manager: Preset Type | dialog-option | Edit > Presets | Selects which preset library to manage | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1190 | Preset Manager: Load, Save Set, Rename, Delete | dialog-option | Edit > Presets | Library management | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1191 | Preset Manager: view modes | dialog-option | Edit > Presets | Text only, small and large thumbnails, list views | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1192 | Export/Import Presets | command | Edit > Presets > Export/Import Presets | Exports or imports presets by type to a folder | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1193 | Migrate Presets | command | Edit > Presets > Migrate Presets | Migrates presets from previous Photoshop versions | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1194 | Presets in panels | behavior | Window menu | Brushes, Swatches, Gradients, Patterns, Shapes, Styles panels manage presets with groups | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1195 | Tool Presets panel | panel | Window > Tool Presets | Saves tool settings as presets with Current Tool Only filter | core | https://helpx.adobe.com/photoshop/using/working-with-presets.html |
| PS-B-1196 | Adobe PDF Presets manager | command | Edit > Adobe PDF Presets | Creates and edits PDF presets | format | https://helpx.adobe.com/photoshop/using/saving-pdf-files.html |
| PS-B-1197 | Remote Connections | command | Edit > Remote Connections | Configures Generator remote connection | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |

## Preferences

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-1198 | Color Picker | preference | Edit > Preferences > General | Adobe or Windows color picker | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1199 | HUD Color Picker | preference | Edit > Preferences > General | Hue Strip or Hue Wheel sizes for on-canvas picker | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1200 | Image Interpolation default | preference | Edit > Preferences > Image Processing | Default resampling method | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1201 | Auto-Update Open Documents | preference | Edit > Preferences > General | Reloads documents changed on disk | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1202 | Beep When Done | preference | Edit > Preferences > General | Sound on completion | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1203 | Export Clipboard | preference | Edit > Preferences > General | Keeps clipboard contents available to other apps on switch | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1204 | Use Legacy Free Transform | preference | Edit > Preferences > General | Requires Shift for proportional scaling | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1205 | Auto show the Home Screen | preference | Edit > Preferences > General | Shows Home when no documents are open | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1206 | Reset Preferences On Quit | preference | Edit > Preferences > General | Resets all preferences at next quit | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1207 | Product improvement data sharing | preference | Edit > Preferences > General | Opt in or out of usage data collection | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1208 | Color Theme | preference | Edit > Preferences > Interface | Four UI brightness themes | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1209 | Highlight Color | preference | Edit > Preferences > Interface | Default gray or Blue highlight | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1210 | Screen mode colors and borders | preference | Edit > Preferences > Interface | Color and Border style (Drop Shadow, Line, None) per screen mode | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1211 | Artboards color and border | preference | Edit > Preferences > Interface | Artboard canvas appearance | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1212 | UI Language | preference | Edit > Preferences > Interface | Interface language | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1213 | UI Font Size | preference | Edit > Preferences > Interface | Tiny, Small, Medium, Large | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1214 | Scale UI To Font | preference | Edit > Preferences > Interface | Scales panels with font size | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1215 | UI Scaling | preference | Edit > Preferences > Interface | Auto, 100 percent, 200 percent | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1216 | Show Channels in Color | preference | Edit > Preferences > Interface | Displays channels with their color | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1217 | Dynamic Color Sliders | preference | Edit > Preferences > Interface | Color panel sliders show live colors | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1218 | Show Menu Colors | preference | Edit > Preferences > Interface | Displays menu color highlights | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1219 | Auto-Collapse Iconic Panels | preference | Edit > Preferences > Workspace | Collapses iconic panels on click away | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1220 | Auto-Show Hidden Panels | preference | Edit > Preferences > Workspace | Shows hidden panels on hover at edge | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1221 | Open Documents as Tabs | preference | Edit > Preferences > Workspace | Tabs versus floating windows | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1222 | Enable Floating Document Window Docking | preference | Edit > Preferences > Workspace | Allows docking floating windows | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1223 | Large Tabs | preference | Edit > Preferences > Workspace | Taller document tabs | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1224 | Enable Narrow Options Bar | preference | Edit > Preferences > Workspace | Compacts options bar | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1225 | Notifications | preference | Edit > Preferences > Notifications | Controls in-app notifications and alerts | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1226 | Show Tool Tips | preference | Edit > Preferences > Tools | Hover tooltips | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1227 | Use Rich Tooltips | preference | Edit > Preferences > Tools | Animated tool tips | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1228 | Enable Gestures | preference | Edit > Preferences > Tools | Touch and trackpad gestures | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1229 | Use Shift Key for Tool Switch | preference | Edit > Preferences > Tools | Requires Shift to cycle grouped tools | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1230 | Overscroll | preference | Edit > Preferences > Tools | Scroll past image edges | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1231 | Enable Flick Panning | preference | Edit > Preferences > Tools | Inertial panning | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1232 | Vary Round Brush Hardness based on HUD vertical movement | preference | Edit > Preferences > Tools | Alt-right-drag behavior | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1233 | Double Click Layer Mask Launches Select and Mask Workspace | preference | Edit > Preferences > Tools | Mask double-click behavior | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1234 | Zoom with Scroll Wheel | preference | Edit > Preferences > Tools | Scroll zooms instead of scrolls | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1235 | Zoom Clicked Point to Center | preference | Edit > Preferences > Tools | Centers zoom on clicked point | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1236 | Animated Zoom | preference | Edit > Preferences > Tools | Continuous zoom on press | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1237 | Zoom Resizes Windows | preference | Edit > Preferences > Tools | Floating window resizes on zoom | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1238 | Snap Vector Tools and Transforms to Pixel Grid | preference | Edit > Preferences > Tools | Pixel snapping for vectors | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1239 | Show Transformation Values | preference | Edit > Preferences > Tools | HUD placement for transform readouts | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1240 | Use Legacy Shape Tool | preference | Edit > Preferences > Tools | Legacy shape behavior | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1241 | History Log | preference | Edit > Preferences > History & Content Credentials | Records editing history to metadata, text file or both | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1242 | History Log: Edit Log Items | preference | Edit > Preferences > History & Content Credentials | Sessions Only, Concise, Detailed | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1243 | Content Credentials: enable for documents | preference | Edit > Preferences > History & Content Credentials | Attaches Content Credentials recording | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1244 | History states count | preference | Edit > Preferences > Performance | Number of undo states | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1245 | Image Previews | preference | Edit > Preferences > File Handling | Always Save, Never Save, Ask When Saving | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1246 | Append File Extension and Use Lower Case | preference | Edit > Preferences > File Handling | Extension handling | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1247 | Save As to Original Folder | preference | Edit > Preferences > File Handling | Default save location | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1248 | Save in Background | preference | Edit > Preferences > File Handling | Non-blocking save | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1249 | Automatically Save Recovery Information Every | preference | Edit > Preferences > File Handling | 5, 10, 15, 30, 60 minutes | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1250 | Default File Location | preference | Edit > Preferences > File Handling | On your computer or Creative Cloud | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1251 | Camera Raw Preferences button | preference | Edit > Preferences > File Handling | Opens Camera Raw preferences | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1252 | Use Adobe Camera Raw to Convert Documents from 32 bit | preference | Edit > Preferences > File Handling | HDR conversion via ACR | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1253 | Prefer Adobe Camera Raw for Supported Raw Files | preference | Edit > Preferences > File Handling | Raw open handler | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1254 | Ignore EXIF Profile Tag | preference | Edit > Preferences > File Handling | Ignores EXIF color space | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1255 | Ignore Rotation Metadata | preference | Edit > Preferences > File Handling | Ignores orientation tag | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1256 | Disable Compression of PSD and PSB Files | preference | Edit > Preferences > File Handling | Faster saves, larger files | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1257 | Maximize PSD and PSB File Compatibility | preference | Edit > Preferences > File Handling | Never, Always, Ask | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1258 | Do not append copy to filename when saving a copy | preference | Edit > Preferences > File Handling | Copy naming | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1259 | Recent File List Contains | preference | Edit > Preferences > File Handling | Number of recent files | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1260 | Cloud documents offline storage location | preference | Edit > Preferences > File Handling | Local cache folder | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1261 | Ask before saving layered TIFF | preference | Edit > Preferences > File Handling | Prompt for layered TIFF | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1262 | Memory Usage | preference | Edit > Preferences > Performance | Let Photoshop Use percentage of RAM | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1263 | History and Cache presets | preference | Edit > Preferences > Performance | Default/Web UI Design, Default/Photos, Huge Pixel Dimensions | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1264 | Cache Levels | preference | Edit > Preferences > Performance | Number of cached zoom levels | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1265 | Cache Tile Size | preference | Edit > Preferences > Performance | Tile size for processing | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1266 | Use Graphics Processor | preference | Edit > Preferences > Performance | GPU acceleration | core | https://helpx.adobe.com/photoshop/kb/photoshop-cc-gpu-card-faq.html |
| PS-B-1267 | Advanced Graphics Processor Settings | preference | Edit > Preferences > Performance | Use OpenCL, Anti-alias Guides and Paths, 30 Bit Display | core | https://helpx.adobe.com/photoshop/kb/photoshop-cc-gpu-card-faq.html |
| PS-B-1268 | Deactivate Native Canvas | preference | Edit > Preferences > Performance | Falls back from GPU native canvas | core | https://helpx.adobe.com/photoshop/kb/photoshop-cc-gpu-card-faq.html |
| PS-B-1269 | AMD Zen 4 and Zen 5 optimizations | behavior | Performance | Faster compute on supported CPUs (27.10) | core | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-B-1270 | Select Subject processing mode | preference | Edit > Preferences > Image Processing | Device or Cloud | ai | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1271 | Remove Background processing mode | preference | Edit > Preferences > Image Processing | Device or Cloud | ai | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1272 | Scratch disk list | preference | Edit > Preferences > Scratch Disks | Active drives with free space and order | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1273 | Scratch disk order | preference | Edit > Preferences > Scratch Disks | Reorders drives used for virtual memory | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1274 | Painting Cursors | preference | Edit > Preferences > Cursors | Standard, Precise, Normal Brush Tip, Full Size Brush Tip | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1275 | Show Crosshair in Brush Tip | preference | Edit > Preferences > Cursors | Crosshair within brush outline | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1276 | Show Only Crosshair While Painting | preference | Edit > Preferences > Cursors | Hides outline during strokes | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1277 | Other Cursors | preference | Edit > Preferences > Cursors | Standard or Precise | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1278 | Brush Preview Color | preference | Edit > Preferences > Cursors | Color for HUD brush preview | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1279 | Transparency Grid Size | preference | Edit > Preferences > Transparency & Gamut | None, Small, Medium, Large | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1280 | Transparency Grid Colors | preference | Edit > Preferences > Transparency & Gamut | Light, Medium, Dark, color checkerboards or custom | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1281 | Gamut Warning Color and Opacity | preference | Edit > Preferences > Transparency & Gamut | Overlay color for out-of-gamut | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1282 | Units Rulers | preference | Edit > Preferences > Units & Rulers | Pixels, Inches, Centimeters, Millimeters, Points, Picas, Percent | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1283 | Units Type | preference | Edit > Preferences > Units & Rulers | Pixels, Points, Millimeters | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1284 | Column Size Width and Gutter | preference | Edit > Preferences > Units & Rulers | Column layout units | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1285 | New Document Preset Resolutions | preference | Edit > Preferences > Units & Rulers | Print and Screen defaults | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1286 | Point/Pica Size | preference | Edit > Preferences > Units & Rulers | PostScript 72 or Traditional 72.27 | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1287 | Guides Canvas Color and Style | preference | Edit > Preferences > Guides, Grid & Slices | Lines or dashed | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1288 | Guides Artboard Color | preference | Edit > Preferences > Guides, Grid & Slices | Artboard guide color | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1289 | Smart Guides Color | preference | Edit > Preferences > Guides, Grid & Slices | Smart guide color | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1290 | Grid Color, Style, Gridline Every, Subdivisions | preference | Edit > Preferences > Guides, Grid & Slices | Grid appearance | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1291 | Slices Line Color and Show Slice Numbers | preference | Edit > Preferences > Guides, Grid & Slices | Slice appearance | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1292 | Path Options | preference | Edit > Preferences > Guides, Grid & Slices | Path line width and color | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1293 | Enable Generator | preference | Edit > Preferences > Plug-ins | Enables Generator for Image Assets | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1294 | Enable Remote Connections | preference | Edit > Preferences > Plug-ins | Allows remote apps to connect with service name and password | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1295 | Allow Extensions to Connect to the Internet | preference | Edit > Preferences > Plug-ins | Extension networking | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1296 | Load Extension Panels | preference | Edit > Preferences > Plug-ins | Loads CEP panels | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1297 | Enable Developer Mode | preference | Edit > Preferences > Plug-ins | Allows loading unsigned UXP plugins | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1298 | Use Smart Quotes | preference | Edit > Preferences > Type | Typographer quotes | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1299 | Enable Missing Glyph Protection | preference | Edit > Preferences > Type | Substitutes missing glyphs | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1300 | Show Font Names in English | preference | Edit > Preferences > Type | Latin font names | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1301 | Use ESC key to commit text | preference | Edit > Preferences > Type | Esc commits instead of cancels | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1302 | Fill new type layers with placeholder text | preference | Edit > Preferences > Type | Lorem ipsum | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1303 | Text Engine Options | preference | Edit > Preferences > Type | Unified, East Asian, Middle Eastern and South Asian engines | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1304 | Font Preview Size and Number of Recent Fonts | preference | Edit > Preferences > Type | Font menu options | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1305 | Enable Auto Activation of Adobe Fonts | preference | Edit > Preferences > Type | Activates missing Adobe Fonts | cloud | https://helpx.adobe.com/photoshop/using/fonts.html |
| PS-B-1306 | Enhanced Controls | preference | Edit > Preferences > Enhanced Controls | Enables and manages advanced editing controls | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1307 | Technology Previews list | preference | Edit > Preferences > Technology Previews | Opt-in experimental features that change by release | core | https://helpx.adobe.com/photoshop/using/technology-previews.html |
| PS-B-1308 | Enable Preserve Details 2.0 Upscale | preference | Edit > Preferences > Technology Previews | Improved resampling for enlargements (graduated preview) | core | https://helpx.adobe.com/photoshop/using/technology-previews.html |
| PS-B-1309 | Enable floating tooltips and other previews | preference | Edit > Preferences > Technology Previews | Per-release trial toggles | core | https://helpx.adobe.com/photoshop/using/technology-previews.html |
| PS-B-1310 | 3D preferences (removed) | preference | Edit > Preferences > 3D (removed) | Former VRAM, rich cursor, ground plane and ray tracer settings removed with 3D | 3d | https://helpx.adobe.com/photoshop/kb/3d-faq.html |
| PS-B-1311 | Preferences migration | behavior | Edit > Preferences | Settings migrate from prior versions on upgrade | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1312 | Backup and restore preferences | behavior | Edit > Preferences | Preferences folder can be backed up and restored | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1313 | Reset preferences at launch | behavior | Edit > Preferences | Ctrl+Alt+Shift at startup deletes settings | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |

## Workspace, UI and Window menu

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-1314 | Arrange > Tile All Vertically | command | Window > Arrange | Tiles open documents vertically | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1315 | Arrange > Tile All Horizontally | command | Window > Arrange | Tiles open documents horizontally | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1316 | Arrange > 2-up, 3-up, 4-up, 6-up layouts | command | Window > Arrange | Preset tiled layouts | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1317 | Arrange > Consolidate All to Tabs | command | Window > Arrange | Puts all windows in tabs | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1318 | Arrange > Cascade and Tile | command | Window > Arrange | Floating window layouts | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1319 | Arrange > Float in Window and Float All in Windows | command | Window > Arrange | Detaches documents from tabs | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1320 | Arrange > Match Zoom, Match Location, Match Rotation, Match All | command | Window > Arrange | Syncs views across documents | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1321 | Arrange > New Window for document | command | Window > Arrange | Opens a second view of the same document | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1322 | Workspace presets | command | Window > Workspace | Essentials, 3D (removed), Graphic and Web, Motion, Painting, Photography | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1323 | Reset workspace | command | Window > Workspace | Restores the current workspace layout | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1324 | New Workspace | command | Window > Workspace | Saves panel locations with optional shortcuts, menus and toolbar | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1325 | Delete Workspace | command | Window > Workspace | Removes a saved workspace | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1326 | Keyboard Shortcuts and Menus shortcut entry | command | Window > Workspace | Opens the customization dialog | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1327 | Lock Workspace | command | Window > Workspace | Prevents moving panels | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1328 | Find Extensions on Exchange | command | Window > Find Extensions on Exchange | Opens Adobe Exchange | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1329 | Extensions (legacy) | command | Window > Extensions (legacy) | Lists CEP extension panels | core | https://helpx.adobe.com/photoshop/using/plug-ins.html |
| PS-B-1330 | Contextual Task Bar toggle | command | Window > Contextual Task Bar | Shows or hides the Contextual Task Bar | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-B-1331 | Contextual Task Bar | panel | Canvas | Floating bar with next-step actions for current selection or layer | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-B-1332 | Contextual Task Bar: Pin position, Reset position, Hide bar | panel-option | Contextual Task Bar menu | Placement options | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-B-1333 | Contextual Task Bar: prompt field | panel-option | Contextual Task Bar | Enter generative or Prompt to edit instructions | ai | https://helpx.adobe.com/photoshop/desktop/whats-new/photoshop-on-desktop-release-notes.html |
| PS-B-1334 | Contextual Task Bar per-context actions | behavior | Contextual Task Bar | Differs for selection, pixel layer, type, generative layer, mask | core | https://helpx.adobe.com/photoshop/desktop/get-started/learn-the-basics/boost-workflows-with-the-contextual-task-bar.html |
| PS-B-1335 | Adjustments panel | panel | Window > Adjustments | Adjustment layers and adjustment presets | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1336 | Brush Settings panel | panel | Window > Brush Settings | Brush tip dynamics | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1337 | Brushes panel | panel | Window > Brushes | Brush presets | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1338 | Channels panel | panel | Window > Channels | Color and alpha channels | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1339 | Character panel | panel | Window > Character | Type character formatting | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1340 | Character Styles panel | panel | Window > Character Styles | Saved character styles | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1341 | Clone Source panel | panel | Window > Clone Source | Clone sources and overlays | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1342 | Color panel | panel | Window > Color | Color sliders and wheel | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1343 | Discover panel | panel | Window > Discover / Help | In-app search, tutorials and quick actions | core | https://helpx.adobe.com/photoshop/using/discover-panel.html |
| PS-B-1344 | Glyphs panel | panel | Window > Glyphs | Glyph browser | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1345 | Gradients panel | panel | Window > Gradients | Gradient presets | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1346 | Histogram panel | panel | Window > Histogram | Tonal distribution with channels and statistics | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1347 | History panel | panel | Window > History | Undo states and snapshots | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1348 | Info panel | panel | Window > Info | Color values, coordinates, sizes | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1349 | Layer Comps panel | panel | Window > Layer Comps | Layer state snapshots | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1350 | Layers panel | panel | Window > Layers | Layer stack | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1351 | Measurement Log panel | panel | Window > Measurement Log | Records measurements | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1352 | Navigator panel | panel | Window > Navigator | Overview and zoom | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1353 | Paragraph panel | panel | Window > Paragraph | Paragraph formatting | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1354 | Paragraph Styles panel | panel | Window > Paragraph Styles | Saved paragraph styles | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1355 | Paths panel | panel | Window > Paths | Vector paths | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1356 | Patterns panel | panel | Window > Patterns | Pattern presets | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1357 | Properties panel | panel | Window > Properties | Context properties and Quick Actions | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1358 | Shapes panel | panel | Window > Shapes | Custom shape presets | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1359 | Styles panel | panel | Window > Styles | Layer style presets | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1360 | Swatches panel | panel | Window > Swatches | Color swatches | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1361 | Version History panel | panel | Window > Version History | Cloud document versions | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-1362 | Options bar | panel | Window > Options | Tool options strip | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1363 | Tools panel | panel | Window > Tools | Toolbar | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1364 | Application Frame (macOS) | panel | Window > Application Frame | Unified window frame | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1365 | Adobe Stock panel | panel | File / Window | Browse, preview and place Stock assets (27.10) | cloud | https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html |
| PS-B-1366 | Open documents list | behavior | Window menu | Bottom of Window menu lists open documents to switch | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1367 | Panel docking, stacking and iconic collapse | behavior | Workspace | Panels dock, group into tabs, collapse to icons | core | https://helpx.adobe.com/photoshop/using/manage-panels.html |
| PS-B-1368 | Panel menus | behavior | Workspace | Each panel has a flyout menu of commands | core | https://helpx.adobe.com/photoshop/using/manage-panels.html |
| PS-B-1369 | Document tabs | behavior | Workspace | Tabbed documents with drag-out, close, rearrange, status in tab title | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1370 | Status bar info | behavior | Document window | Document Sizes, Profile, Dimensions, Measurement Scale, Scratch Sizes, Efficiency, Timing, Current Tool, 32-bit Exposure, Save Progress, Smart Objects, Layer Count | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1371 | Screen modes | behavior | View > Screen Mode | Standard, Full Screen with Menu Bar, Full Screen; F cycles | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-B-1372 | Tab hides panels | behavior | Workspace | Tab hides all panels; Shift+Tab hides all except toolbar | core | https://helpx.adobe.com/photoshop/using/workspace-basics.html |
| PS-B-1373 | Search (Ctrl+F) | behavior | Discover panel | Searches UI commands, tutorials, Stock | core | https://helpx.adobe.com/photoshop/using/discover-panel.html |
| PS-B-1374 | Home screen | panel | Home | Start screen with recent files, cloud documents, create new, learn content, quick actions | core | https://helpx.adobe.com/photoshop/using/home-screen.html |
| PS-B-1375 | Home: Recent files filters and views | panel-option | Home | Filter by type, list or thumbnail | core | https://helpx.adobe.com/photoshop/using/home-screen.html |
| PS-B-1376 | Home: Shared with you | panel-option | Home | Cloud documents shared by others | cloud | https://helpx.adobe.com/photoshop/using/home-screen.html |
| PS-B-1377 | Home: Deleted | panel-option | Home | Recover deleted cloud documents | cloud | https://helpx.adobe.com/photoshop/using/home-screen.html |
| PS-B-1378 | Discover: Browse, Quick Actions, Hands-on tutorials, Learn | panel-option | Discover panel | Help and task content | core | https://helpx.adobe.com/photoshop/using/discover-panel.html |
| PS-B-1379 | Discover: Quick Actions | panel-option | Discover panel | Remove Background, Blur Background, Make B and W Background, Smooth Skin, Enhance Image and others | ai | https://helpx.adobe.com/photoshop/using/discover-panel.html |
| PS-B-1380 | Unified Account menu | behavior | Title bar | Account, credits, preferences access in the Edit workspace (27.7) | cloud | https://www.cgchannel.com/2026/05/adobe-releases-photoshop-27-7/ |
| PS-B-1381 | Rotate view and flick panning | behavior | Canvas | Canvas navigation behaviors | core | https://helpx.adobe.com/photoshop/using/viewing-images.html |
| PS-B-1382 | In-app update notifications | behavior | Workspace | Notifies of new features and updates | core | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |

## Cloud, collaboration and web/iPad

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-1383 | Cloud documents | behavior | File / Home / Libraries | PSDC files stored in Creative Cloud, synced across desktop, iPad and web | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-1384 | Cloud documents offline availability | behavior | File / Home / Libraries | Recent cloud files cached locally with Make Available Offline | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-1385 | Cloud documents version history | behavior | Window > Version History | Automatic and named versions, restore and bookmark | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-1386 | Version History: Mark version, Revert, Open version, Save as copy | panel-option | Window > Version History | Version operations | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-1387 | Cloud file search | behavior | Open from Cloud | Keyword search across cloud files, folders and generated assets (27.9.1) | cloud | https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html |
| PS-B-1388 | Save to cloud | behavior | File > Save As | Save As dialog offers Save to Creative Cloud | cloud | https://helpx.adobe.com/photoshop/using/cloud-documents-faq.html |
| PS-B-1389 | Invite to Edit | command | File > Invite | Invites collaborators by email with edit access | cloud | https://helpx.adobe.com/photoshop/using/invite-to-edit.html |
| PS-B-1390 | Share for Review | command | File > Share for Review | Public or restricted link for reviewers to view and comment | cloud | https://helpx.adobe.com/photoshop/using/share-for-review.html |
| PS-B-1391 | Share for Review: Link access settings | panel-option | Share for Review dialog | Anyone with link or invited only, allow comments | cloud | https://helpx.adobe.com/photoshop/using/share-for-review.html |
| PS-B-1392 | Share for Review: Update review link | panel-option | Share for Review dialog | Pushes latest changes to the review copy | cloud | https://helpx.adobe.com/photoshop/using/share-for-review.html |
| PS-B-1393 | Comments panel | panel | Window > Comments | View and reply to review comments pinned to canvas areas | cloud | https://helpx.adobe.com/photoshop/using/share-for-review.html |
| PS-B-1394 | Comments: pins and annotations | panel-option | Comments panel | Comments linked to canvas locations | cloud | https://helpx.adobe.com/photoshop/using/share-for-review.html |
| PS-B-1395 | Comments: resolve, filter, reply | panel-option | Comments panel | Comment management | cloud | https://helpx.adobe.com/photoshop/using/share-for-review.html |
| PS-B-1396 | Libraries panel | panel | Window > Libraries | Stores colors, character styles, graphics, layer styles, brushes, patterns across apps | cloud | https://helpx.adobe.com/photoshop/using/creative-cloud-libraries.html |
| PS-B-1397 | Libraries: Create new library, share, collaborate | panel-option | Libraries panel | Library management | cloud | https://helpx.adobe.com/photoshop/using/creative-cloud-libraries.html |
| PS-B-1398 | Libraries: Add Elements from document | panel-option | Libraries panel | Add Content button captures layer, colors, styles | cloud | https://helpx.adobe.com/photoshop/using/creative-cloud-libraries.html |
| PS-B-1399 | Libraries: linked graphics | panel-option | Libraries panel | Library graphics placed as linked Smart Objects update across documents | cloud | https://helpx.adobe.com/photoshop/using/creative-cloud-libraries.html |
| PS-B-1400 | Libraries: search and Stock | panel-option | Libraries panel | Search libraries and Adobe Stock | cloud | https://helpx.adobe.com/photoshop/using/creative-cloud-libraries.html |
| PS-B-1401 | Libraries: view by type, group | panel-option | Libraries panel | Organization options | cloud | https://helpx.adobe.com/photoshop/using/creative-cloud-libraries.html |
| PS-B-1402 | Adobe Fonts activation | behavior | Character panel | Activate fonts from Adobe Fonts in the Character panel | cloud | https://helpx.adobe.com/photoshop/using/fonts.html |
| PS-B-1403 | Adobe Fonts auto-activation | behavior | Type | Missing fonts auto-activated when available | cloud | https://helpx.adobe.com/photoshop/using/fonts.html |
| PS-B-1404 | Sync settings | behavior | Account | Preferences and presets sync via Creative Cloud | cloud | https://helpx.adobe.com/photoshop/desktop/get-started/settings-and-preferences/adjust-preferences.html |
| PS-B-1405 | Firefly Boards integration | behavior | Layers panel | Send layers to and import from Firefly Boards | cloud | https://helpx.adobe.com/photoshop/desktop/generative-ai/use-firefly-boards-with-photoshop.html |
| PS-B-1406 | Adobe Express integration | behavior | File | Send to or open from Adobe Express | cloud | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-1407 | Lightroom photos access | behavior | Home | Open photos from Lightroom cloud in Photoshop | cloud | https://helpx.adobe.com/photoshop/user-guide.html |
| PS-B-1408 | Photoshop on the web | behavior | Photoshop on the web | Browser version editing cloud documents with core tools and generative features | cloud | https://helpx.adobe.com/photoshop/using/photoshop-web-overview.html |
| PS-B-1409 | Photoshop on the web: Share and comment | behavior | Photoshop on the web | Reviewers comment in browser | cloud | https://helpx.adobe.com/photoshop/using/photoshop-web-overview.html |
| PS-B-1410 | Photoshop on iPad | behavior | Photoshop on iPad | Touch-first version editing cloud documents with Apple Pencil | cloud | https://helpx.adobe.com/photoshop/ipad/user-guide.html |
| PS-B-1411 | Photoshop mobile (iPhone, Android) | behavior | Photoshop mobile | Mobile editor with generative features editing cloud documents | cloud | https://helpx.adobe.com/photoshop/desktop/whats-new/whats-new-in-adobe-photoshop-on-desktop.html |

## Help menu

| ID | Feature | Kind | Where | What it does | Category | Source |
|---|---|---|---|---|---|---|
| PS-B-1412 | Photoshop Help | command | Help menu | Opens online user guide | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1413 | Hands-on Tutorials | command | Help menu | Opens in-app tutorials in Discover | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1414 | About Photoshop | command | Help menu | Version and credits | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1415 | About Plug-ins | command | Help menu | Lists loaded plug-ins | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1416 | System Info | command | Help menu | Displays system and GPU information for support | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1417 | GPU Compatibility | command | Help menu | Reports GPU feature status | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1418 | Manage My Account | command | Help menu | Opens Adobe account | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1419 | Sign Out and sign-in | command | Help menu | Account session | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1420 | Updates | command | Help menu | Checks for updates via Creative Cloud | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1421 | Photoshop Online Forums | command | Help menu | Opens community forums | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1422 | Submit Bug/Feature Request | command | Help menu | Opens feedback portal | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1423 | New Features | command | Help menu | Shows what is new | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1424 | Photoshop Support Center | command | Help menu | Opens support site | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1425 | Legal Notices | command | Help menu | Licenses and third-party notices | core | https://helpx.adobe.com/photoshop/using/photoshop-help.html |
| PS-B-1426 | Help search in Discover | behavior | Discover panel | Help and search share the Discover panel | core | https://helpx.adobe.com/photoshop/using/discover-panel.html |

## Row counts per area

| Area | Rows |
|---|---|
| Filter menu: top level, Smart Filters and Filter Gallery | 135 |
| Filter submenus: Blur, Blur Gallery, Distort, Noise, Pixelate | 113 |
| Filter submenus: Render, Sharpen, Stylize, Video, Other, 3D (removed) | 88 |
| Adaptive Wide Angle, Lens Correction, Liquify, Vanishing Point | 92 |
| Neural Filters | 34 |
| Camera Raw Filter and Camera Raw 18.6 | 129 |
| Generative and AI features | 71 |
| Automation: Actions, Batch, Droplets, Scripts, Plug-ins | 137 |
| Video, animation and legacy 3D | 77 |
| File menu commands | 82 |
| File formats and format options | 130 |
| Print, proofing and color management | 77 |
| Keyboard Shortcuts and Menus, Toolbar, Presets | 32 |
| Preferences | 116 |
| Workspace, UI and Window menu | 69 |
| Cloud, collaboration and web/iPad | 29 |
| Help menu | 15 |
| Total | 1426 |

