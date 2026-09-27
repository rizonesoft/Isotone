# List and tree

Rows for lists and trees in panels and dialogs: Lumen's folders and collections, Nodus's object tree, History, Presets.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Row | `row-h-compact` 22px (Comfortable 28px), 8px left padding plus 16px per level | `body` in `text-primary` |
| Expand chevron | 12px box, chevron-right (collapsed) or chevron-down (expanded) | `icon` |
| Icon | 14px, 6px gaps | `icon` |
| Meta | right aligned, `caption` | `text-secondary` (counts, sizes, "offline") |

## States

| State | Look |
| --- | --- |
| Hover | `surface-hover` |
| Selected, focused list | `state-subtle` (text stays `text-primary`) |
| Selected, list not focused | `selection-inactive` |
| Keyboard focus | 2px inset focus ring on the focused row (drawn over the selection) |
| Disabled | `text-disabled` text, icon and meta |
| Drop into | `state-tint` fill + 1px inset `state-line` |
| Drop before or after | 2px `state-line` bar between rows, inset 4px |

## Keyboard

Up and Down move; Shift extends; Ctrl+Space toggles; Right expands then moves to the first child; Left collapses then moves to the parent; `*` expands all below; F2 renames; Delete deletes with undo; typing jumps by prefix.

## WPF

`ListBox`, `ListView` and `TreeView` styles `Photon.ListBox`, `Photon.TreeView` with item containers `Photon.ListRow` / `Photon.TreeRow`. The tree row template draws full-width highlights (a `Grid` spanning the row with the indent inside, not WPF's default indented highlight). Triggers use `IsSelected` plus `Selector.IsSelectionActive` for the unfocused color. Drag feedback via an `Adorner` (`Photon.DropIndicatorAdorner`). Always `VirtualizingPanel.IsVirtualizing="True"` and `VirtualizationMode="Recycling"` for libraries of 50,000 photos.
