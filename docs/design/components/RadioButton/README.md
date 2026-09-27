# Radio button

One choice from a small, visible set (two to five). Use a ComboBox for more.

## Anatomy

Box `check-size-compact` 14px circle (`radius-round`, Comfortable 16px), `surface-field` with 1px `border-control`; selected: `state` fill, `state-line` border, 6px `state-on` dot. Label `body` 8px after.

## States

Rest, hover (`border-control-hover`), pressed (`surface-control-pressed`), disabled (`text-disabled` ring, dot and label; selected disabled fills `divider-strong`), focus (ring 1px outside the circle). Selected hover and pressed use `state-hover` and `state-pressed`.

## Keyboard

The group is one tab stop landing on the selected item; arrow keys move and select; Space selects the focused item if none is.

## WPF

`RadioButton` style `Photon.RadioButton`: `Ellipse PART_Ring`, `Ellipse PART_Dot`; group with `GroupName` or a shared parent; put the set in a `StackPanel` with `KeyboardNavigation.DirectionalNavigation="Cycle"` and `TabNavigation="Once"`. Tool rail buttons are RadioButtons with a different style (see Tool rail).
