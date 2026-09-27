# Combo box and dropdown

Choose one value from a list (blend modes, resample methods, fonts). The editable form also accepts typed values.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Closed box | `control-h-compact` 24px, 8px left padding, 12px chevron with 4px right padding, `radius-sm` | `surface-control`, 1px `border-control`, `text-primary`, chevron `icon` |
| Editable box | `surface-field` text area plus a 20px drop part divided by 1px `divider-strong` | as TextBox |
| List | at least the box width, `radius-md`, 4px vertical padding, max 16 rows then scrolls | Menu surface: `surface-raised`, `border-popup`, `shadow-popup` |
| Item | `menu-row-h-compact` 24px, 16px check column | `text-primary`; selected shows a check |

## States

- Closed: rest, hover (`surface-control-hover`, `border-control-hover`), open (border `focus-ring`), focus (ring 1px outside), disabled (no fill, `divider-strong` border, `text-disabled`).
- Items: highlighted `state` + `state-on`; selected shows the check (and is highlighted when the list opens); disabled `text-disabled`; separators group related modes (as Photoshop groups blend modes).

## Keyboard

Alt+Down or F4 opens; Up and Down change the value without opening (blend modes preview live, which Photoshop users expect); typing jumps by prefix; Enter picks; Escape closes and reverts. Editable: type, Enter commits.

## WPF

`ComboBox` style `Isotone.ComboBox` (implicit) with parts `PART_EditableTextBox`, `PART_Popup` (`AllowsTransparency`), `ToggleButton` for the drop part; `ComboBoxItem` style shares the MenuItem look. `IsEditable` switches the template via a trigger. `VirtualizingStackPanel` for long lists (fonts).
