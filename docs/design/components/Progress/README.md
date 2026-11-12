# Progress

Bars and rings for work that takes longer than a second. Anything slower than a second shows progress and can be cancelled.

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Bar | 4px tall, 2px radius, width from the host | track `surface-field` with a 1px `divider-strong` inner edge; fill `state-line` |
| Launch bar | 340 x 3px, 1.5px radius, splash screen only (see Splash) | track #3A3B41 with no edge, fill `accent-<app>` |
| Failed | fill stops where it failed | `status-error` fill and a helper line |
| Ring | 16px (stroke 2) inline, 32px (stroke 3) in empty states | track `divider-strong`, arc `state-line` |
| Label | `caption`: percent and counts ("42% · 104 of 248") | `text-secondary` |

## Rules

- Determinate whenever the total is known; indeterminate (a 30% segment sliding in 1.6s) only while counting.
- Pair long operations with Cancel (subtle button) next to the bar.
- Status bar progress uses a 96px bar with the percent after it.
- Reduced motion: indeterminate bars show a static 30% segment and the label says "Working…"; rings stop spinning and show a static arc.

## Keyboard

Not focusable; Cancel is. Screen readers get the value through UIA `RangeValue` and a polite live region at 10% steps.

## Native

A progress bar element (a track, an indicator, and a moving segment when indeterminate) and a progress ring element (an arc drawn as Direct2D geometry, rotated by an animation that stops when Windows reports client-area animation off, `SPI_GETCLIENTAREAANIMATION`). UI Automation: ProgressBar with RangeValue.
