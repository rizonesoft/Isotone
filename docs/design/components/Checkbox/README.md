# Checkbox

A two- or three-state option. The box fills with the Highlight color when checked.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Box | `check-size-compact` 14px (Comfortable 16px), `radius-sm` | `surface-field`, 1px `border-control` |
| Glyph | 12px check or minus, stroke 2.5 | `state-on` |
| Label | 8px after the box, `body` | `text-primary` |

## States

| | Rest | Hover | Pressed | Disabled | Focus |
| --- | --- | --- | --- | --- | --- |
| Unchecked | `surface-field` + `border-control` | border `border-control-hover` | fill `surface-control-pressed` | no fill, `text-disabled` border and label | focus ring 1px outside the box |
| Checked | `state` fill, `state-line` border, check `state-on` | `state-hover` | `state-pressed` | `divider-strong` fill, glyph `text-disabled` | ring |
| Indeterminate | as checked with a minus | `state-hover` | `state-pressed` | as checked disabled | ring |

The `state-line` border keeps the checked box visible in Medium Gray, where the `state` fill alone is only 1.4:1 against the panel; the check itself holds 4.5:1 on the fill in every theme.

## Highlight color

Checked boxes follow Preferences > Interface > Highlight color: Blue (default), Isotone orange (`state-orange` with a near-black check in the dark themes), or the Windows accent. The preview shows all three.

## Keyboard

Space toggles; indeterminate is reachable only when the checkbox represents a mixed selection (clicking it sets all to checked). The label is part of the hit target.

## WPF

`CheckBox` style `Isotone.CheckBox` (implicit). Template: `Grid` with `Border PART_Box` (`CornerRadius` 2), `Path PART_Check` and `Rectangle PART_Indeterminate`, `ContentPresenter` with `Margin="8,0,0,0"`. `IsThreeState` only for mixed selections. Visual states `CheckStates` (Checked, Unchecked, Indeterminate) plus `CommonStates` and `FocusStates`; transitions `duration-fast`.
