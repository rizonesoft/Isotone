// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include <cstdint>

namespace isotone::ui
{

// The DPI at which one DIP is one physical pixel (100 percent).
inline constexpr std::uint32_t kBaseDpi = 96;

// A length or a coordinate in device-independent pixels: what every design token and every layout is written in.
struct Dip
{
    float value = 0.0F;

    friend constexpr bool operator==(Dip left, Dip right) = default;
};

// A width and a height in DIPs.
struct DipSize
{
    float width = 0.0F;
    float height = 0.0F;

    friend constexpr bool operator==(const DipSize& left, const DipSize& right) = default;
};

// A rectangle by its four edges, in DIPs.
struct DipRect
{
    float left = 0.0F;
    float top = 0.0F;
    float right = 0.0F;
    float bottom = 0.0F;

    friend constexpr bool operator==(const DipRect& left, const DipRect& right) = default;
};

// A rectangle by its four edges, in physical pixels (right and bottom are exclusive, as in RECT).
struct PixelRect
{
    std::int32_t left = 0;
    std::int32_t top = 0;
    std::int32_t right = 0;
    std::int32_t bottom = 0;

    [[nodiscard]] constexpr std::int32_t width() const noexcept
    {
        return right - left;
    }
    [[nodiscard]] constexpr std::int32_t height() const noexcept
    {
        return bottom - top;
    }

    friend constexpr bool operator==(const PixelRect& left, const PixelRect& right) = default;
};

// The one rounding rule of the suite: a DIP edge is the physical pixel floor(dips * dpi / 96 + 0.5). Every layout
// edge at every scale goes through it, so an edge two elements share in DIPs is one pixel edge.
[[nodiscard]] constexpr std::int32_t to_pixels(Dip dips, std::uint32_t dpi) noexcept
{
    constexpr double kHalf = 0.5;
    const double scaled =
        (static_cast<double>(dips.value) * static_cast<double>(dpi) / static_cast<double>(kBaseDpi)) + kHalf;
    const auto truncated = static_cast<std::int32_t>(scaled);
    // Truncation rounds toward zero; a negative value with a fraction needs one more step down to be the floor.
    return static_cast<double>(truncated) > scaled ? truncated - 1 : truncated;
}

// A rectangle converts by its edges, never by its width and height.
[[nodiscard]] constexpr PixelRect to_pixels(const DipRect& rect, std::uint32_t dpi) noexcept
{
    return PixelRect{.left = to_pixels(Dip{rect.left}, dpi),
                     .top = to_pixels(Dip{rect.top}, dpi),
                     .right = to_pixels(Dip{rect.right}, dpi),
                     .bottom = to_pixels(Dip{rect.bottom}, dpi)};
}

// The DIP position of a physical pixel edge: exact, with no rounding.
[[nodiscard]] constexpr Dip to_dips(std::int32_t pixels, std::uint32_t dpi) noexcept
{
    return Dip{
        static_cast<float>(static_cast<double>(pixels) * static_cast<double>(kBaseDpi) / static_cast<double>(dpi))};
}

[[nodiscard]] constexpr DipRect to_dips(const PixelRect& rect, std::uint32_t dpi) noexcept
{
    return DipRect{.left = to_dips(rect.left, dpi).value,
                   .top = to_dips(rect.top, dpi).value,
                   .right = to_dips(rect.right, dpi).value,
                   .bottom = to_dips(rect.bottom, dpi).value};
}

// The display scale as Windows shows it: 96 DPI is 100, 144 DPI is 150.
[[nodiscard]] constexpr std::uint32_t scale_percent(std::uint32_t dpi) noexcept
{
    constexpr std::uint32_t kPercent = 100;
    return ((dpi * kPercent) + (kBaseDpi / 2)) / kBaseDpi;
}

} // namespace isotone::ui
