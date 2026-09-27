# Button

Command buttons: default, primary (the app accent, once per view), subtle, icon-only, split and toggle.

## Anatomy and sizes

| Variant | Size | Tokens |
| --- | --- | --- |
| Default | `control-h-compact` 24px (dialogs `control-h-dialog` 28px, Comfortable 30px), min 64px wide (80px in dialogs), 12px side padding, `radius-sm` | `surface-control`, 1px `divider-strong`, label `body` `text-primary` |
| Primary | as default, `body-strong` label | `accent-<app>` fill and border, label `accent-<app>-on`, hover `accent-<app>-hover` |
| Subtle | as default, no fill or border | hover `surface-hover` |
| Icon | square, 16px icon | `icon`, hover icon `text-primary` |
| Split | main part plus a 20px arrow part divided by 1px | arrow opens a Menu of related commands |
| Toggle | usually icon-only, subtle | on: `state-tint` fill, 1px `state-line` border |

## Rules

- One primary button per view: the dialog's commit button, the Home screen's New, Albumen's Import. It is the only place chrome shows the app accent beside the title-bar mark.
- Labels are verbs in title case in menus and sentence case on buttons: "Save a copy", "Export". OK and Cancel stay short.
- Icon-only buttons always have a tooltip naming the command and shortcut and an `AutomationProperties.Name`.
- Destructive commands are default buttons with a verb that says what goes ("Delete 12 photos"), never red fills.

## States

Rest, hover (`surface-control-hover`), pressed (`surface-control-pressed`), focus (2px `focus-ring` 1px outside), disabled (`surface-control` fill, `divider` border, `text-disabled` label; primary loses its accent). Toggle adds on and on+hover.

## Keyboard

Tab to focus; Enter and Space activate. In dialogs the primary button is `IsDefault` (Enter) and Cancel is `IsCancel` (Escape). A split button's arrow opens with Alt+Down.

## WPF

Styles `Isotone.Button` (implicit), `Isotone.PrimaryButton`, `Isotone.SubtleButton`, `Isotone.IconButton`, `Isotone.SplitButton` (a `Control` with `PART_Main` and `PART_Drop` + `ContextMenu`), and `ToggleButton` style `Isotone.ToggleIconButton`. Template: `Border PART_Chrome` with `CornerRadius="{StaticResource radius-sm}"`, `ContentPresenter`; states via `VisualStateManager` `CommonStates` and `FocusStates` (a separate `Border PART_FocusRing` 1px outside, visible on `IsKeyboardFocused`, never on mouse focus). `FocusVisualStyle="{x:Null}"` so the default dotted rectangle never shows. The primary style binds its brushes to `Isotone.App.Accent`, set once per app.
