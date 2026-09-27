# Focus ring

One keyboard focus indicator for the whole suite: a 2px solid `focus-ring` stroke. It only appears for keyboard focus, never for mouse clicks.

## Spec

| Where | Ring |
| --- | --- |
| Buttons, tool buttons, caption buttons, swatches, checkbox and radio boxes, toggle tracks, slider thumbs | `focus-ring-w` 2px, 1px outside the element, following its radius |
| Text boxes, number boxes, editable combo boxes | the 1px border turns `focus-ring` plus a 1px inner `focus-ring` line, so the field does not grow |
| Rows (lists, trees, layers, menu items), tabs, document tabs, menu titles | 2px inset, drawn over the selection fill |

`focus-ring` aliases `state-line`, so it follows the Highlight color. Contrast: at least 3:1 against `frame`, `surface-panel`, `surface-tabstrip`, `surface-raised`, `surface-field`, `surface-control`, `surface-control-hover` and `ruler-surface`, and against `state-subtle` for focused selected rows, in all four themes (checked by script, see README).

## Rules

- Never remove focus visuals; never show them on mouse focus.
- Focus moves predictably: F6 cycles the main regions (tool rail, options bar, document, dock, status toasts); Tab moves within a region.
- Windows high contrast: the ring uses `SystemColors.HighlightBrush`.

## WPF

Set `FocusVisualStyle="{x:Null}"` in every Photon style and draw the ring in the template (`Border PART_FocusRing`, `Margin="-3"`, `BorderThickness="2"`, `CornerRadius` = element radius + 2), shown by a trigger on `IsKeyboardFocused` (`IsKeyboardFocusWithin` for composite controls) combined with the attached `Photon.Focus.IsKeyboardInitiated`, which tracks the last input device through `InputManager.Current.PreNotifyInput`.
