# Radio button

One choice from a small, visible set (two to five). Use a ComboBox for more.

## Anatomy

Box `check-size-compact` 14px circle (`radius-round`, Comfortable 16px), `surface-field` with 1px `border-control`; selected: `state` fill, `state-line` border, 6px `state-on` dot. Label `body` 8px after.

## States

Rest, hover (`border-control-hover`), pressed (`surface-control-pressed`), disabled (`text-disabled` ring, dot and label; selected disabled fills `divider-strong`), focus (ring 1px outside the circle). Selected hover and pressed use `state-hover` and `state-pressed`.

## Keyboard

The group is one tab stop landing on the selected item; arrow keys move and select; Space selects the focused item if none is.

## Native

One radio button element: a ring and a dot. Buttons are grouped by a shared group; inside a group the arrow keys cycle and Tab enters and leaves once. Tool rail buttons are radio buttons with a different drawing (see Tool rail). UI Automation: RadioButton with SelectionItem.
