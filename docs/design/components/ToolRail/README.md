# Tool rail

The single-column tool palette on the left of every document window, with flyout groups and the foreground and background color chips at the bottom.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Rail | `toolrail-w-compact` 40px (Comfortable `toolrail-w-comfortable` 48px), 4px top and bottom | `surface-panel`, 1px `divider` on the right |
| Tool button | `tool-button-compact` 32px square (Comfortable 40px), 2px gap, `radius-sm` | 20px icon (`icon-md`) in `icon` |
| Group triangle | 4px, 3px from the bottom-right corner | `currentColor` at 80% |
| Group separator | 24 x 1px, 4px above and below | `divider-strong` |
| Color chips | two `color-chip` squares offset 10px, swap and default glyphs at 12px | 1px `text-primary` edge plus 1px `frame` halo so white and black chips both read |

## States

| State | Look |
| --- | --- |
| Rest | transparent, icon `icon` |
| Hover | `surface-hover`, icon `text-primary` |
| Pressed | `surface-control-pressed` |
| Checked (active tool) | `state-tint` fill, 1px `state-line` border, `glow-state` shadow (Bezier signature); widen the glow to blur 10 at 60% on hover |
| Disabled | icon `text-disabled` (for example Crop on a locked document) |
| Focus | focus ring, 1px outside |

## Flyout groups

- A grouped tool shows the triangle. Press and hold (300ms), right-click, or Alt+click cycles; the flyout is a Menu listing the group with shortcut letters and a 4px square marking the tool shown on the rail.
- Choosing a tool from the flyout replaces the rail button's icon and checks it.
- Shift+letter cycles the tools of a group (Photoshop default).

## Rich tooltip

After `tooltip-delay` (400ms) the Tooltip component opens right of the button: tool name, shortcut chip, one-line description. Moving to a neighboring tool while a tooltip is open switches it with no delay.

## Keyboard

- The rail is one tab stop (the arrow keys cycle within it); Up and Down move, Enter or Space selects, Shift+F10 opens the flyout.
- Single-letter shortcuts work anywhere the canvas has focus and never when a text field has focus.

## Native

- A column of tool buttons in one group, populated from the registered tools. Each button draws its chrome (fill, border, and the glow as a zero-offset shadow), its icon, and a group triangle when the tool has a group.
- States: common (normal, hover, pressed, disabled), checked and unchecked, and focus.
- The tooltip opens after 400 ms, with no delay between adjacent buttons, and is the rich tooltip.
- UI Automation Name: "Brush Tool (B)"; RadioButton with SelectionItem.
