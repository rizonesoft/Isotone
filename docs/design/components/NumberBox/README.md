# Number box

Bezier's CompactNumberBox: a numeric field whose label is a scrub handle. Drag left or right on the label to change the value, as in Photoshop's scrubby sliders.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Box | `control-h-compact` 24px, width set by the host (72 to 120px), `radius-sm` | `surface-field`, 1px `border-control` |
| Scrub zone | label (X, W, Opacity) or a grip of two 1px lines at 50%, 6px left padding, 3px gap | `text-secondary`, cursor SizeWE |
| Value | right aligned, `caption`, tabular figures | `text-primary` |
| Unit | 3px after the value | `text-secondary` |
| Spinners (optional) | 14 x 10px each, 1px `divider-strong` left edge | 8px chevrons in `icon` |

## Scrubbing

- 1 unit per pixel; Shift x10; Alt x0.1 (values with decimals).
- The pointer is captured and hidden after 4px of travel and wraps at screen edges, so a long drag never stops.
- Each drag is one undo step; the document previews live.
- While scrubbing the label turns `state-text` and the border `border-control-hover`.

## States

Rest, hover (`border-control-hover`), scrubbing, focus (`focus-ring` border plus inner line), disabled (no fill, `text-disabled` everywhere), out of range (`status-error` border and line, a helper line naming the range "0 to 100"; the last valid value is kept on commit).

## Keyboard

Up and Down step by 1 (Shift 10, Alt 0.1); Page Up and Down by 10; Enter commits; Escape reverts. Math is accepted ("1920/2"), and units convert ("2in" in a px field).

## WPF

`Photon.UI.Controls.NumberBox` (`Control`, from Bezier CompactNumberBox) with dependency properties `Value`, `Minimum`, `Maximum`, `SmallChange`, `LargeChange`, `Decimals`, `Label`, `Unit`, `ShowSpinners`, `ShowGrip`. Template parts: `PART_ScrubZone` (`Cursor="SizeWE"`, handles `PreviewMouseLeftButtonDown` and `CaptureMouse`), `PART_TextBox`, `PART_Up` / `PART_Down` (`RepeatButton`). Visual states `CommonStates`, `FocusStates`, `ValidationStates` (Valid, OutOfRange), `ScrubStates` (Idle, Scrubbing).
