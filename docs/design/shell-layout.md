# Shell layout

Every Photon document window has the same anatomy, top to bottom and left to right. A feature adds to it; it never invents a second one. Sizes are Compact, with Comfortable in parentheses.

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│ [■] File Edit Image Layer Select Filter View Window Help               ─   □   ✕    │ title bar 32, frame
├───────────────────────────────────────────────────────────────────────────────────────┤
│ [brush ▾] │ Size 24 px  Hard 80 % │ Mode Normal ▾  Opacity 100 %  Flow 65 %  [≈]     │ options bar 32 (40), surface-panel
├───────────────────────────────────────────────────────────────────────────────────────┤
│ (i) Brush: Click to paint. Shift-click paints a straight line.                         │ hint bar 28, surface-tabstrip (optional)
├────┬──────────────────────────────────────────────────────────────┬───────────────────┤
│    │ Harbor at dusk.psd @ 66.7% (RGB/8) * │ Untitled-1 @ 100%  │ │ Properties│Adjust  │ doc tabs 28 (32) frame │ panel tabs 26
│ ▣  ├──────────────────────────────────────────────────────────────┤  APPEARANCE        │
│ ▢  │ ruler 18                                                     │  TRANSFORM         │
│ ◌  │   ┌───────────────────────────────┐                          ├───────────────────┤
│ ✂  │   │                               │                          │ Layers│Channels    │
│ ── │   │          document             │     canvas-surround      │  Normal ▾  100 %   │
│ ✎  │   │                               │                          │  ◉ ▦ Title         │
│ ⌫  │   └───────────────────────────────┘                          │  ◉ ▦ Retouch       │
│ …  │                                                              │  ◉ ▦ Background [L]│
│ ■□ │                                                              │                   │
├────┴──────────────────────────────────────────────────────────────┴───────────────────┤
│ ● Ready │ 2 objects selected │ RGB │ Snap on          X 1204.5 Y 388.0 │ 66.7% │ GPU  │ status bar 22 (26), frame
└───────────────────────────────────────────────────────────────────────────────────────┘
  tool rail 40 (48)                                                    right dock 280 (260 to 300)
```

(The diagram uses text glyphs as placeholders; the product draws catalog icons.)

## Regions

| Region | Size | Tokens | Notes |
| --- | --- | --- | --- |
| Title bar | `titlebar-h` 32 | `frame` | App mark (40px zone), menu bar, drag area, caption buttons `caption-button-w` 46. See Window chrome. |
| Options bar | `optionsbar-h-compact` 32 (40) | `surface-panel`, `divider` below | Active tool's settings. See Options bar. |
| Hint bar | `infobar-h` 28 | `surface-tabstrip` | Optional (View > Show Hints). Info bars for status stack here too. |
| Tool rail | `toolrail-w-compact` 40 (48) | `surface-panel`, `divider` right | One column of 32px (40px) tools, groups separated, color chips at the bottom. Can float or switch to two columns (Photoshop's double arrow) when the window is shorter than the rail. |
| Document tabs | `doctab-h-compact` 28 (32) | `frame` | One per document; selected tab is `surface-panel` with a 2px `state-line` top edge. |
| Rulers | `ruler-w` 18 | `ruler-surface` | Toggle with Ctrl+R. |
| Canvas | the rest | `canvas-surround` | The only region with saturated color: the user's content. |
| Right dock | `panel-w-default` 280 (`panel-w-min` 260 to `panel-w-max` 300, user resizable) | panels `surface-panel` on `frame` with 1px gaps | Panel groups stacked vertically, each with a tab strip; collapsible to a `panel-iconstrip-w` 36px icon strip. |
| Status bar | `statusbar-h-compact` 22 (26) | `frame`, `divider` above | See Status bar. |

Minimum window size 1024 x 640; default 1400 x 900 (Bezier's), restored per app from settings.

## Per app

### Nodus (vector)

- Menus: File, Edit, Object, Path, Type, Select, View, Window, Help.
- Tool rail: Selection, Direct Selection, Pen (group: Pen, Add Anchor, Delete Anchor, Convert), Type, Rectangle (group: shapes), Line, Pencil, Eyedropper, Artboard, Hand, Zoom; fill and stroke chips replace foreground/background.
- Options bar: with nothing selected, the document W/H and units; with a selection, X, Y, W, H, rotation, and the object's fill and stroke (Bezier's context toolbar).
- Dock: Properties (Appearance, Transform), Layers (object tree), Artboards, Swatches, History.
- Canvas: white `artboard` pages on `canvas-surround`; smart guides in `guide-smart`.

### Imago (raster)

- Menus: File, Edit, Image, Layer, Select, Filter, View, Window, Help.
- Tool rail in Photoshop's order: Move, Marquee, Lasso, Quick Selection / Magic Wand, Crop, Eyedropper | Healing, Brush, Clone Stamp, History Brush, Eraser, Gradient / Paint Bucket, Blur, Dodge | Pen, Type, Path Selection, Shape | Hand, Zoom | color chips, Quick Mask.
- Dock (Photoshop's default arrangement): Color / Swatches, Properties / Adjustments, Layers / Channels / Paths, History.
- Canvas: transparency shows the checkerboard at `checker-tile` 8px.

The previous Imago layout (Layers on the left, Properties on the right) moves to this single right dock.

### Lumen (darkroom and photo manager)

- Two workspaces switched by tabs in the title bar area after the menus: **Library** and **Develop** (Lightroom Classic's modules), each keeping the same regions.
- Library: left dock (folders and collections, a List and tree) instead of the tool rail; grid of thumbnails in the canvas region on `canvas-surround`; right dock with Metadata and Keywords; a filmstrip 96px tall above the status bar on `frame`.
- Develop: tool rail with Crop, Spot Removal, Red Eye, Masking, Before/After; right dock with the Histogram and the develop panels as sections (Basic, Tone Curve, HSL, Detail, Lens, Effects) using Sliders paired with NumberBoxes.
- Selected thumbnails use a 2px `state-line` outline and `state-subtle` cell fill; the Import button is Lumen's primary (`accent-lumen`).

## Splash and Home

- Home (no document open): the canvas region shows New and Open (New is the primary button), recent documents as a list with 96px thumbnails, and nothing else.
- Splash: the Suite card (operator decision 2026-09-27), built in XAML so the version, status and progress are live; `<app>-splash.svg` is its reference design and a marketing image, never shown by the app. The full spec is the Splash component guide (`components/Splash/README.md`); the table below is its summary.

### Splash spec

| Aspect | Spec |
| --- | --- |
| Size | 640 x 360 DIPs, radius 8, centred on the monitor that holds the cursor; no title bar, not in the taskbar |
| Card | vertical gradient #303136 to #1A1B1E, a 1px inner highlight of white at 8 percent; the same in every brightness theme |
| Layout grid | icon column x 56 to 192 centred on y 160; text column from x 230 to x 610; text positions are baselines |
| Icon | the Direction C master at 136 x 136, x 56, y 92, over a radial halo of `accent-<app>` at 20 percent (centre 128, 160, radius 150) |
| App name | Segoe UI Variable Display 46px semibold, letter spacing -0.5px, #F4F4F5, x 228, baseline 148 |
| Role | 16px regular #B7B8BD, baseline 178 ("Vector editor", "Raster and photo editor", "Digital darkroom and photo manager") |
| Suite and version | 13px regular #8C8D93, baseline 212: "Photon Graphics Suite · Version 0.1.0", the dot in #6C6D73 |
| Status | Segoe UI Variable Text 12px #A3A4AA, baseline 272, live from startup ("Loading tools…", "Loading brushes…", "Opening the catalog…") |
| Progress | 340 x 3 track #3A3B41 at x 230, y 284, radius 1.5; fill `accent-<app>`, determinate, advanced by the startup steps |
| Copyright | 11px #6E6F75, right-aligned at x 610, baseline 312: "© 2026 Rizonetech (Pty) Ltd · Free and open source (GPL-3.0)" |
| Band | the spectrum as a gentle wave along the bottom edge (the seven app icon stops), with a 1.5px white crest at 35 percent |
| Glow | Bezier's `BorderGlowAnimator` in `accent-<app>`: a 1.5px highlight travelling around the edge, one lap per 6 s while loading, fading in over 300ms and out over 500ms; none when Windows animation effects are off |
| Timing | shown from process start until the main window is ready, then fades out over `duration-standard` 200ms; no minimum display time and no artificial delay; closes at once when animations are off |
