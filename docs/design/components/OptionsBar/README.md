# Options bar

The context toolbar under the title bar that shows the active tool's settings (Photoshop's options bar, Bezier's context toolbar), with the hint bar beneath it.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Bar | `optionsbar-h-compact` 32px (Comfortable 40px), 12px side padding, 8px gaps | `surface-panel`, 1px `divider` below |
| Tool preset button | subtle button, 16px tool icon plus 10px chevron | opens the tool preset picker |
| Controls | 24px NumberBox, ComboBox, Checkbox, subtle toggle buttons | as those components |
| Labels | before a control, `body` | `text-secondary` |
| Group separator | 1 x 16px, 4px side margins | `divider-strong` |
| Hint bar | `infobar-h` 28px, lightbulb 14px, caption text | `surface-tabstrip`, `text-secondary`, the tool name in `body-strong` `text-primary` |

## Rules

- Content changes with the tool; order: preset, size and shape, blending (Mode, Opacity, Flow), then toggles. Keep Photoshop's order so muscle memory transfers.
- In Stilus with a selection the bar shows the selection's X, Y, W and H (Bezier's document W/H when nothing is selected).
- Controls that do not apply are disabled with a reason tooltip, never hidden, so the bar does not jump.
- The hint bar is one line naming the tool and its modifier keys; View > Show Hints hides it.
- Overflow: controls at the right collapse into a trailing `ellipsis` button menu.

## Keyboard

The bar is a toolbar: F6 cycles focus between rail, options bar, canvas and dock; inside, Tab moves between controls; Enter commits a field and returns focus to the canvas; Escape reverts it.

## WPF

`ToolBar` is not used (its overflow chrome fights the design); the bar is a `DockPanel` with an `ItemsControl` whose `DataTemplateSelector` picks the tool's options view. Style key `Isotone.OptionsBar`; separators `Isotone.ToolbarSeparator`. The hint bar is `Isotone.HintBar` bound to the tool's `Hint` string.
