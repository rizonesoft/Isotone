# Scroll bar

A thin overlay scroll bar that stays out of the way and widens on hover, used in panels, lists and dialogs. The canvas uses its own scroll bars with the same look.

## Anatomy and states

| State | Look |
| --- | --- |
| Rest | `scrollbar-w-rest` 4px thumb, `radius-round`, `scroll-thumb`, 2px from the edge, no track |
| Hover (pointer within 10px) | bar widens to `scrollbar-w-hover` 10px in `duration-fast`: track `surface-tabstrip`, thumb 6px `scroll-thumb-hover`, 8px arrow glyphs in `text-secondary` at both ends |
| Dragging | thumb `text-secondary` |
| Idle | fades to 0 after 1s without scrolling or hover when Windows "Always show scrollbars" is off; always visible when it is on |

Minimum thumb length 24px. The bar overlays content; lists reserve 4px right padding so text never sits under the thumb.

## Keyboard

Scroll bars are not tab stops; the scrolled control handles arrows, Page Up/Down, Home, End.

## WPF

`ScrollBar` and `ScrollViewer` styles `Isotone.ScrollBar` / `Isotone.ScrollViewer` (implicit): the `ScrollViewer` template overlays `PART_VerticalScrollBar` and `PART_HorizontalScrollBar` in the same `Grid` cell as `ScrollContentPresenter`. The bar's template: `Track PART_Track` with a `Thumb` (`Border` with `CornerRadius`) and `RepeatButton` arrows collapsed until `IsMouseOver`. Read `UISettings.AutoHideScrollBars` for the fade.
