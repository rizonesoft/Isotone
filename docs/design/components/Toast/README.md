# Toast and info bar

Two ways to report outcomes: toasts for finished background work and failures after the fact; info bars for conditions that persist while the user works.

## Toast

| Part | Size | Tokens |
| --- | --- | --- |
| Surface | 320px, 10px by 16px padding (12px left), `radius-lg` | `surface-raised`, 1px `border-popup`, `shadow-dialog` |
| Icon | 16px status icon | `status-error`, `status-success`, `status-warning` or `status-info` |
| Title | `body-strong` | `text-primary` |
| Message | `caption` | `text-secondary` |
| Action | a link | `state-text` |
| Dismiss | 20px subtle icon button | `icon` |

Toasts stack bottom right above the status bar, 8px apart, at most three. They slide in 20px and fade over `duration-standard`, stay 6s (errors stay until dismissed), and pause while hovered. Error text names the action, the file and what it needed (Bezier's error toast, now neutral with a colored icon instead of an orange fill).

## Info bar

Full width under the options bar, `infobar-h` 28px min, 12px side padding, `caption` text; the lead phrase in `body-strong` `text-primary`.

| Kind | Fill | Icon |
| --- | --- | --- |
| Info | `status-info-subtle` | `info` in `status-info` |
| Warning | `status-warning-subtle` | `alert` in `status-warning` |
| Error | `status-error-subtle` | `error` in `status-error` |
| Success | `status-success-subtle` | `success` in `status-success` |
| Hint (Bezier info bar) | `surface-tabstrip` | `bulb` in `icon`, text `text-secondary` |

Text on every subtle fill is `text-primary` (4.5:1 checked in all four themes). Status always pairs color with an icon and a word.

## Keyboard

Toasts are announced through a live region (assertive for errors, polite otherwise) and never take focus; F6 reaches the toast stack; Escape dismisses the focused toast. Info bar actions are ordinary tab stops.

## WPF

`Isotone.ToastHost` (an `ItemsControl` in an adorner layer over the window) with `Isotone.Toast` items and `Isotone.InfoBar` (`Control` with `Severity`, `Title`, `Message`, `ActionCommand`, `IsClosable`). `AutomationProperties.LiveSetting` per severity.
