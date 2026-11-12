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

## Native

Scroll bar and scroll view elements: the scroll view overlays its vertical and horizontal bars on its content. A bar is a track with a thumb (rounded by its radius token) and arrow repeat buttons hidden until the pointer is over the bar. The fade follows the Windows "Always show scrollbars" setting. UI Automation: ScrollBar with RangeValue, and the Scroll pattern on the view.
