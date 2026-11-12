# Context menu

The right-click menu: the same item template as Menu, opened at the pointer and scoped to the thing under it. It names its subject with a group header when the target is not obvious (a layer, a guide, a photo).

## Anatomy and sizes

Identical to Menu: `surface-raised`, 1px `border-popup`, `radius-md`, `shadow-popup`, rows `menu-row-h-compact`, icons 16px, shortcut in `text-secondary`, separators `divider-strong`, group header in `section-header`.

## Rules

- Order: the most frequent command first, then edits, then destructive commands last and separated. Show a disabled item rather than removing it when users expect to find it there (Rasterize on a pixel layer).
- Opening a context menu on an unselected row selects that row first; on a selected row it acts on the whole selection.
- Right-click on the canvas lists commands for the active tool (Photoshop behavior), not a generic list.

## States

As Menu: highlighted `state` with `state-on` text, disabled `text-disabled`, checked, radio, submenu.

## Keyboard

Shift+F10 or the Menu key opens it at the focused element (top-left of the focused row), with the first enabled item highlighted. Arrows, Enter and Escape as in Menu.

## Native

The menu element of the Menu spec, opened as a popup: it shares the menu item drawing, and draws `shadow-popup` itself (no system drop shadow). It opens at the pointer for pointer opening and at the focused element for keyboard opening (Shift+F10 and the Menu key). UI Automation: Menu with MenuItem children.
