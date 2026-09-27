# Dialog

A modal window for a focused task (Image Size, Export, Preferences, confirmations). Enter does what the primary button says; Escape does what Cancel says.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Scrim | the owner window's client area | `scrim` |
| Surface | 360 to 640px wide, `radius-lg` | `surface-raised`, 1px `border-popup`, `shadow-dialog` |
| Header | 12px top, 16px left, title `dialog-title`; 24px close button | `text-primary`; close `icon` |
| Body | 12px top, 16px sides and bottom, 8px row gap, 72px label column | labels `text-secondary` |
| Footer | 12px by 16px padding, 1px `divider` above, buttons right aligned with 8px gap | primary last (rightmost), then Cancel to its left |
| Controls | `control-h-dialog` 28px | as components |

## Rules

- The title is the command without the ellipsis ("Image Size"); the primary button is a verb ("Resize", "Export") or OK.
- The primary button uses the app accent; there is exactly one.
- Confirmations name what, how many and how large: "Delete 12 photos (84 MB) from disk?"; the destructive verb is the button label.
- Dialogs that preview changes show a Preview checkbox and apply live to the canvas.
- Open with a `duration-slow` pop from scale 0.95 and fade; close in `duration-fast`; none when animations are off.

## Keyboard

Focus starts on the first field (or the primary button for confirmations). Tab order follows reading order and wraps inside the dialog. Enter activates the default button unless focus is in a multi-line field; Escape cancels; Alt+underlined letter jumps to a labeled control.

## WPF

`Window` subclass `Photon.DialogWindow` with `WindowStyle="None"`, `AllowsTransparency="True"` (for the rounded corners and shadow), `Owner` set, `ShowInTaskbar="False"`, `WindowStartupLocation="CenterOwner"`; the owner draws the scrim through an adorner while the dialog is open. Buttons: `IsDefault` on the primary, `IsCancel` on Cancel. `FocusManager.FocusedElement` sets the first focus.
