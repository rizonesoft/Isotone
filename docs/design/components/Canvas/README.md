# Canvas surround, rulers and guides

The document area: the pasteboard around the image or artboard, rulers, guides, selection outlines, transform handles and the transparency checkerboard. The artwork is the brightest thing on screen; everything here is thin and neutral or fixed-color so it reads over any image.

## Parts

| Part | Size | Tokens |
| --- | --- | --- |
| Surround (pasteboard) | fills the view | `canvas-surround` (distinct from `frame` and `surface-panel`); user can override per document |
| Document edge | 1px outside the image | `divider-strong` |
| Rulers | `ruler-w` 18px, top and left, square corner cell | `ruler-surface`, major ticks every 100 units in `text-secondary` with 9px numbers, minor ticks `divider-strong`, 1px `divider-strong` edge |
| Cursor marker on rulers | 1px line | `state-line` |
| Guides | 1px, full view | `guide` (cyan); locked guides the same color |
| Smart guides | 1px, only while dragging, with distance labels | `guide-smart` (magenta) |
| Marching ants | 1px, 4px dashes alternating, animated 4px per 150ms | `ants-dark`, `ants-light` |
| Bounding box | 1px | `handle-stroke` (follows the Highlight color) |
| Transform handles | `handle-size` 7px squares at corners and midpoints; rotate zone 12px outside the corners | fill `handle-fill`, 1px `handle-stroke` |
| Checkerboard | 8px squares (`checker-tile`) at 100%, fixed screen size | `checker-light`, `checker-dark` |
| Artboard (Stilus) | document color | `artboard` |

## Rules

- Guide, ants, handle and checker colors are the same in every theme on purpose: they sit on artwork, not on chrome.
- Handles scale with the display (7px at 100%, 14px at 200%), never with zoom.
- Pixel grid appears above 800% zoom as 1px lines in `ants-dark` at 15% opacity.
- Reduced motion: marching ants stop and show a static dashed outline.

## WPF

The canvas is SkiaSharp (`SKElement` / `SKGLElement`); read these colors from the theme once per theme change into `SKColor` fields (an `Isotone.UI.CanvasPalette` singleton), never per frame. Rulers are WPF `FrameworkElement`s with `OnRender` and `GuidelineSet`s for crisp 1px lines at every scale. The surround color is a document setting defaulting to `canvas-surround`.
