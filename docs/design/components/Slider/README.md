# Slider

Photoshop-style slider: a thin track with a fill, a round thumb, and a paired NumberBox for exact entry. Gradient sliders show the value's color range (hue, saturation, opacity).

## Anatomy

| Part | Size | Tokens |
| --- | --- | --- |
| Track | `slider-track-h` 2px, full width minus the thumb | `border-control` |
| Fill | from the minimum to the thumb | `state-line` |
| Thumb | `slider-thumb` 10px circle (12px Comfortable) with a 1px `frame` halo | `text-primary` |
| Paired number box | 72px NumberBox with grip and unit | see NumberBox |
| Gradient slider | 10px ramp, `radius-sm`, 1px `border-control` inner edge, a 7px triangle thumb under it | the ramp is content (hue, saturation, alpha over the checkerboard); triangle `text-primary` |

## States

Rest; hover (thumb scales 1.2 in `duration-fast`); pressed or dragging (thumb `state-line`); focus (ring 2px outside the thumb; on gradient sliders the triangle turns `focus-ring`); disabled (track `divider-strong`, fill and thumb `text-disabled`).

## Keyboard

Left and Down decrease, Right and Up increase by SmallChange (1); Page keys by LargeChange (10); Home and End jump to the ends. Shift+arrow uses LargeChange. The number box and slider stay in sync; dragging is one undo step.

## WPF

`Slider` style `Photon.Slider`: `Track PART_Track` with `RepeatButton`s (`DecreaseRepeatButton` draws the fill, `IncreaseRepeatButton` the track) and a `Thumb` template (`Ellipse`). `IsMoveToPointEnabled="True"` (click jumps, Photoshop behavior). Gradient slider: `Photon.GradientSlider` with a `Brush Ramp` property and a `Polygon` thumb. Pair with a NumberBox bound two-way to the same `Value`.
