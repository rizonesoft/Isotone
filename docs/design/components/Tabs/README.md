# Tabs

Two tab styles: the panel tab strip (grouped panels, Photoshop style) and underline tabs for dialogs (Preferences, Export settings).

## Panel tabs

`panel-tab-h-compact` 26px strip on `surface-tabstrip`; each tab 12px side padding, `body`, 1px `divider` right edge. Rest `text-secondary`; hover `surface-hover` + `text-primary`; selected `surface-panel` joined to the body (covers the strip's bottom line) + `text-primary`; focus inset ring. Tabs can be dragged to regroup or float (see Panel).

## Dialog tabs

A row with 16px gaps over a 1px `divider` line; labels `body`, 6px top and 8px bottom padding. Rest `text-secondary`; hover `text-primary`; selected `body-strong` `text-primary` with a 2px `state-line` underline; disabled `text-disabled` (with a tooltip saying why). For more than 7 sections use a list on the left instead.

## Keyboard

The tab row is one tab stop; Left and Right move and select (automatic activation); Ctrl+Tab and Ctrl+Shift+Tab switch from inside the content; Home and End jump.

## WPF

`TabControl` styles `Photon.PanelTabControl` and `Photon.DialogTabControl`; `TabItem` templates with `Border PART_Chrome` and, for dialog tabs, `Rectangle PART_Underline` visible on `IsSelected`. `TabStripPlacement="Top"`, `KeyboardNavigation.TabNavigation="Once"` on the header panel.
