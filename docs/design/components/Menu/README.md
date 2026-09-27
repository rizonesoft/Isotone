# Menu bar and menus

Drop-down menus from the menu bar inside the title bar. Highlighted items use the Highlight color (`state`), so the menu reads like Photoshop's.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Menu title | 24px tall, 8px side padding, `radius-sm` | `text-primary`; hover `surface-hover`; open `surface-control-hover` |
| Menu | min `menu-w-min` (200px), 4px vertical padding, `radius-md` | `surface-raised`, 1px `border-popup`, `shadow-popup` |
| Item row | `menu-row-h-compact` 24px (Comfortable 30px), inset 4px, `radius-sm` | label `text-primary` in `body` |
| Icon column | 20px | 16px icon in `icon`; also holds the check or radio dot |
| Shortcut | right aligned, 16px gap before it | `text-secondary` |
| Submenu arrow | 16px column, 12px chevron-right | `icon` |
| Separator | 1px, 4px above and below | `divider-strong` |
| Group header | caps, `section-header` | `text-secondary` |

## States

- Rest: as above.
- Highlighted (pointer or keyboard): fill `state`, label, shortcut, icon and arrow in `state-on`.
- Submenu open (pointer moved into the submenu): `surface-hover`, so the path stays visible without a second blue bar.
- Disabled: label, shortcut and icon `text-disabled`; still highlightable by keyboard with no fill so the reason tooltip can show.
- Checked (toggle command): check glyph in the icon column; the item's own icon is dropped.
- Radio (one of a set): 6px dot in the icon column; the set sits between separators, optionally under a group header.

## Keyboard

- Down and Up move the highlight and wrap; Home and End jump; letters jump by access key, then by first letter.
- Right opens a submenu, Left closes it (or moves to the previous menu title from a top-level menu).
- Enter or Space runs the item; Escape closes one level; Alt closes all.
- Shortcut text uses Windows naming: Ctrl, Shift, Alt, then the key (`Shift+Ctrl+Z` in Photoshop order is acceptable across the suite as long as one order is used everywhere; Isotone uses Shift+Ctrl+key).

## WPF

- `Menu` and `MenuItem` restyled in `Isotone.UI/Themes/Controls/Menu.xaml`. The `MenuItem` template is a 4-column `Grid` with `SharedSizeGroup`s (`Icon`, `Label`, `Gesture`, `Arrow`) and parts `PART_Popup` and `PART_SubmenuPopup` (a `Popup` with `AllowsTransparency` so the shadow and radius render).
- Triggers: `Role` (TopLevelHeader, TopLevelItem, SubmenuHeader, SubmenuItem), `IsHighlighted`, `IsChecked`, `IsEnabled`, `IsSubmenuOpen`.
- `InputGestureText` feeds the shortcut column; commands carry their `KeyGesture` so the text never drifts.
- Radio items: `IsCheckable` plus an attached `Isotone.MenuItem.Group`, drawing the dot instead of the check.
- `Separator` keyed `MenuItem.SeparatorStyleKey`.
