# List and tree

Rows for lists and trees in panels and dialogs: Albumen's folders and collections, Stilus's object tree, History, Presets.

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

## Native

List and tree elements with row elements for their items. A tree row draws its highlight across the full width, with the indent inside the row. The row reads selected plus whether its list has focus, for the unfocused color. Drag feedback is a drop indicator drawn over the list. Rows are always virtualized and recycled, for libraries of 50,000 photos, and UI Automation exposes virtualized items (ItemContainer, VirtualizedItem) with Selection, SelectionItem, ExpandCollapse, and Scroll.
