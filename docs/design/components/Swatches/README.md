# Swatches and color

Color selection pieces: foreground and background chips, the swatch grid, the color field with hue slider, and the hex field.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| FG/BG chips | two `color-chip` 24px squares offset 10px, `radius-sm` | 1px `text-primary` edge + 1px `frame` halo; swap (`swap`) and default (`square`) glyphs 12 and 10px in `icon` |
| Swatch grid | `swatch-compact` 16px cells (Comfortable 20px), 2px gap, `radius-sm` | 1px inner shade line so white and black cells keep an edge |
| None swatch | a cell with a diagonal | `surface-field` with a `status-error` stroke |
| Color field | 176 x 112px, `radius-sm`, 1px `border-control` inner edge | a 10px ring: 2px `checker-light` with a 1px `ants-dark` outline, visible on any color |
| Hue strip | 10px tall under the field, triangle thumb | as Gradient slider |
| Hex field | 108px TextBox, `#` prefix in `text-secondary`, value in `mono-body` | as TextBox |

## States

Swatch: rest, hover (1px `text-primary` outline 1px outside), selected (2px `state-line` outline 1px outside), focus (focus ring). Chips: hover shows a tooltip with the hex value; click opens the Color Picker dialog.

## Keyboard

The grid is one tab stop; arrows move; Enter sets the foreground color, Alt+Enter the background; Delete removes (with undo). X swaps chips, D resets to black and white. The hex field accepts 3 or 6 digits, with or without #.

## WPF

`ListBox` with a `WrapPanel` items host and `ListBoxItem` style `Photon.Swatch`; chips are `Photon.ColorChips` (`Control` with `Foreground`/`Background` color DPs, `PART_Swap`, `PART_Reset`). Color field: `Photon.ColorField` rendering the gradient with two `LinearGradientBrush`es in a `Grid`; hue: `Photon.GradientSlider`. Swatch colors are document content and are not theme resources.
