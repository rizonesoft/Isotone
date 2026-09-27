# Layers row

The Layers panel row (Pinxit; Stilus uses the same row for objects): visibility eye, thumbnail, optional linked mask, name, trailing badges, over the blend mode and opacity controls.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Row | `layer-row-h-compact` 36px (Comfortable 44px), 1px `divider` below | `text-primary` `body` name |
| Visibility | 28px column with a 1px `divider` right edge, 14px `eye` | `icon`; empty column when hidden |
| Thumbnail | 28px (Comfortable 36px), 1px `divider-strong` frame, 8px checkerboard | `checker-light`, `checker-dark` |
| Mask link | 14px column with a 12px `link` glyph, then the mask thumbnail | `icon` |
| Group | 12px chevron and 16px folder instead of a thumbnail; children indent 24px | `icon` |
| Badges | `fx` in `caption`, 14px `lock` | `text-secondary`, `icon` |
| Header controls | blend ComboBox (132px) + Opacity NumberBox; Lock toggles (20px subtle toggle buttons) + Fill NumberBox | as those components |
| Footer | 22px subtle icon buttons: link, fx, mask, adjustment, new group, new layer, delete | `icon` |

## States

- Hover `surface-hover`; selected `state-subtle`; selected while the panel lacks focus `selection-inactive`; multi-select uses the same fill.
- Hidden: no eye, thumbnail at 45%, name in `text-secondary`.
- Locked: `lock` badge; a fully locked Background layer sets its name in italics (Photoshop convention).
- Dragging: 2px `state-line` insertion line between rows (starting after the visibility column); dropping on a group highlights it with Drop into from List and tree.
- Keyboard focus: inset focus ring.

## Keyboard

Alt+[ and Alt+] move the selection down and up; Ctrl+[ and Ctrl+] move the layer; the eye toggles with a click, Alt+click soloes; F2 or double-click the name renames; Ctrl+G groups; Delete deletes. Clicking the eye never changes the selection.

## WPF

`ListBox` (or `TreeView` for groups) with `ItemTemplate` `Isotone.LayerRowTemplate`: a `Grid` with columns 28 | Auto | Auto | * | Auto. The thumbnail is an `Image` over a `DrawingBrush` checkerboard (`TileMode="Tile"`, `Viewport="0,0,8,8"` absolute). Thumbnails render off the UI thread at the row's device pixel size. The eye is a `ToggleButton` with `Focusable` true and `AutomationProperties.Name` "Show layer" / "Hide layer".
