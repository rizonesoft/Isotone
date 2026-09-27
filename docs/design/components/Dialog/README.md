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

## About dialog

Help, About <App> is a Dialog with the app icon master at 128px (`docs/design/app-icons.md`), the app name in `dialog-title`, and these lines in `body`, top to bottom, with no other legal text:

- "Version 0.1.0 (commit 2e87a3d)": the informational version with the short commit, and a "Copy version info" button.
- "Copyright (C) 2025-2026 Rizonetech (Pty) Ltd": the copyright holder is the company, never the brand.
- "Rizonesoft is a brand of Rizonetech (Pty) Ltd.": the publisher users see stays Rizonesoft.
- "Licensed under the GNU General Public License v3.0" with a link opening the license text shipped with the app.
- "Source code: https://github.com/rizonesoft/Isotone/tree/<tag>": the GPL source offer, a link to the exact tag the build came from (`stilus-v0.1.0`); a build with no tag links the commit instead.
- The product page link: one configured value, `https://www.rizonesoft.com/` until the per-app pages are decided, never a hardcoded per-app URL.
- The credits list (package, version, license, link) and the repository and issue links.

The footer has one button, Close, which is the default and the cancel button. Stilus, Pinxit, and Albumen show the same dialog from `Isotone.UI`, filled from the app's identity.

## Keyboard

Focus starts on the first field (or the primary button for confirmations). Tab order follows reading order and wraps inside the dialog. Enter activates the default button unless focus is in a multi-line field; Escape cancels; Alt+underlined letter jumps to a labeled control.

## WPF

`Window` subclass `Isotone.DialogWindow` with `WindowStyle="None"`, `AllowsTransparency="True"` (for the rounded corners and shadow), `Owner` set, `ShowInTaskbar="False"`, `WindowStartupLocation="CenterOwner"`; the owner draws the scrim through an adorner while the dialog is open. Buttons: `IsDefault` on the primary, `IsCancel` on Cancel. `FocusManager.FocusedElement` sets the first focus.
