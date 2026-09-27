# Document tabs

One tab per open document, on the `frame` strip between the options bar and the canvas.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Strip | `doctab-h-compact` 28px (Comfortable 32px) | `frame`, 1px `divider` below |
| Tab | 12px left and 4px right padding, max `doctab-w-max` 240px, 1px `divider` on the right | label `body` in `text-secondary` |
| Close | 18px square, 12px `x` glyph, `radius-sm` | `icon`; hover `surface-control-hover` |
| Overflow | subtle icon button at the right, `chevrons-right` | opens a list of all documents |

Label format (Photoshop): `name.ext @ zoom (mode/depth)` plus ` *` when unsaved. Long names truncate in the middle so the extension and zoom stay visible.

## States

- Rest: `text-secondary`, close hidden.
- Hover: `surface-hover`, `text-primary`, close visible.
- Selected: `surface-panel` (joins the canvas area), `body-strong` `text-primary`, 2px `state-line` along the top edge, close visible.
- Focus: inset focus ring.
- Dragging: the tab follows the pointer; a 2px `state-line` insertion bar shows the drop slot; dragging out floats the document.

## Keyboard

Ctrl+Tab and Ctrl+Shift+Tab cycle documents; Ctrl+W or Ctrl+F4 closes; with a tab focused, Left and Right move, Delete closes, the Menu key opens Close, Close Others, Reveal in Explorer.

## WPF

`TabControl` over the documents collection (or AvalonDock `LayoutDocumentPane` with the Isotone theme), `TabItem` style `Isotone.DocumentTab`. Template parts: `Border PART_Chrome`, `Rectangle PART_Indicator` (visible when `IsSelected`), `TextBlock` with a middle-ellipsis converter, `Button PART_Close` bound to `CloseDocumentCommand`. Middle-click closes.
