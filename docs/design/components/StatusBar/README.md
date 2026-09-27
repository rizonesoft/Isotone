# Status bar

The dense strip along the bottom edge: status on the left, document facts and live readouts on the right (Bezier's status bar).

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Bar | `statusbar-h-compact` 22px (Comfortable 26px), 12px side padding | `frame`, 1px `divider` on top |
| Text | `caption` (Comfortable `caption-comfortable`) | `text-secondary` |
| Separator | 1 x 12px, 12px side margins | `divider-strong` |
| Status dot | 6px circle | `status-success` ready, `status-warning` working, `status-error` failed, always next to a word |
| Coordinates | `mono` | `text-primary` |
| Inline progress | 96px Progress bar with a percent | `state-line` |

Order, left to right: status word, selection summary, color mode, snapping, artboard or layer; right: cursor X and Y, zoom, element count or document size, memory, GPU or CPU.

## Rules

- Values update live but throttle to 10 per second; coordinates use tabular figures and fixed decimals so the text does not jitter.
- Items the user clicks (zoom, color mode, snapping) are subtle buttons 18px tall with the same text style, hover `surface-hover`.
- No icons except where they are the item (the magnet for Snap).

## Keyboard

The bar is not in the tab order; its commands exist in menus. Screen readers get changes through a polite live region on the status word only.

## WPF

`StatusBar` restyled as `Isotone.StatusBar` with `StatusBarItem`s and `Separator` keyed `StatusBar.SeparatorStyleKey` (1 x 12). Coordinates: `TextBlock` with `FontFamily="{DynamicResource font-mono}"` and `Typography.NumeralAlignment="Tabular"`. `AutomationProperties.LiveSetting="Polite"` on the status word.
