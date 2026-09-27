# Toggle switch

An on/off setting that applies immediately, used in Preferences and panel menus. Settings that wait for OK are checkboxes.

## Anatomy

Track `toggle-w` 32 x 16px, `radius-round`, `surface-field` with 1px `border-control`; thumb 10px `text-secondary`, 2px inset. On: track `state` with `state-line` border, thumb `state-on` at the right. Label `body` 8px after (or before in a settings row with the label left aligned).

## States

Off and on, each rest, hover (border `border-control-hover`, thumb `text-primary`; on: `state-hover`), disabled (`text-disabled` track border and thumb; on fills `divider-strong`), focus (ring 1px outside the track). The thumb slides in `duration-fast` with `ease-out`; no slide when animations are off.

## Keyboard

Space toggles. Arrow keys do not.

## WPF

`ToggleButton` style `Isotone.ToggleSwitch` (no third-party control): `Border PART_Track`, `Ellipse PART_Thumb` with a `TranslateTransform` animated between 0 and 16. `AutomationProperties.Name` is the label; UIA exposes the Toggle pattern.
