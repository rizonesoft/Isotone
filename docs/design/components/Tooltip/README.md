# Tooltip

Bezier's rich tooltip: a title, a shortcut chip and one line of description, opening after 400ms.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Surface | max 260px wide, 6px by 10px padding, `radius-sm` | `surface-raised`, 1px `border-popup`, `shadow-tooltip` |
| Title | `body-strong` | `text-primary` |
| Shortcut chip | 8px after the title, mono `caption`, 1px `divider-strong` border, `radius-sm` | `text-secondary` |
| Description | `caption`, one or two lines | `text-secondary` |

## Rules

- Every icon-only control has one: the command name and its shortcut. Tools and complex commands add the description (what it does, the main modifier).
- Disabled controls get a tooltip that says why ("Select two or more layers to align them.").
- Open after `tooltip-delay` 400ms; move between neighbors with no delay; close on pointer leave, click, Escape or after 10s.
- Never interactive, never the only place information lives.
- Placement: right of tool rail buttons, below everything else, flipping at screen edges.

## Keyboard

Keyboard focus shows the tooltip after the same delay; Escape dismisses. Screen readers get the same text through the UI Automation HelpText property.

## Native

A tooltip element in its own popup window, drawing its shadow itself (no system drop shadow), and the rich tooltip content: a title, a shortcut, and a description read from the command's registration. It opens after 400 ms, with no delay between adjacent controls, and also over disabled controls. UI Automation: ToolTip.
