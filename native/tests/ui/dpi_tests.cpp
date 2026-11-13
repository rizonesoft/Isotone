// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/ui/dpi.h"

#include <array>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <gtest/gtest.h>

namespace
{

using isotone::ui::Dip;
using isotone::ui::DipRect;
using isotone::ui::PixelRect;
using isotone::ui::to_dips;
using isotone::ui::to_pixels;

// 100, 125, 150, 175, 200, 250, and 300 percent.
constexpr std::array<std::uint32_t, 7> kDpis{96, 120, 144, 168, 192, 240, 288};
constexpr std::array<std::uint32_t, 7> kPercents{100, 125, 150, 175, 200, 250, 300};
// Layout coordinates in DIPs: whole, halves, the 1.5 of the icon stroke, a negative, and large ones.
constexpr std::array<float, 12> kEdges{0.0F,  0.5F,  1.0F,   1.5F,   2.0F,     7.0F,
                                       22.0F, 24.5F, 280.0F, 959.5F, 1919.25F, -3.5F};

// How far a converted edge sits from where the layout put it: at most half a physical pixel, which at 100 percent
// and above is at most half a DIP, inside the design contract's 1 DIP.
float moved_dips(float edge, std::uint32_t dpi)
{
    return std::fabs(to_dips(to_pixels(Dip{edge}, dpi), dpi).value - edge);
}

TEST(Dpi, RoundTripAtEveryScale)
{
    constexpr float kHalfDip = 0.5F;
    constexpr float kTolerance = 1e-4F;
    for (std::size_t scale = 0; scale < kDpis.size(); ++scale)
    {
        const std::uint32_t dpi = kDpis.at(scale);
        EXPECT_EQ(isotone::ui::scale_percent(dpi), kPercents.at(scale));
        for (const float edge : kEdges)
        {
            EXPECT_LE(moved_dips(edge, dpi), kHalfDip + kTolerance) << edge << " DIP at " << dpi << " DPI";
            // A pixel edge is a fixed point: converting it to DIPs and back gives the same pixel.
            const std::int32_t pixel = to_pixels(Dip{edge}, dpi);
            EXPECT_EQ(to_pixels(to_dips(pixel, dpi), dpi), pixel) << edge << " DIP at " << dpi << " DPI";
        }
    }
}

// floor(dips * dpi / 96 + 0.5): a half rounds up, on both sides of zero, at every scale.
TEST(Dpi, HalvesRoundUpOnBothSidesOfZero)
{
    constexpr std::uint32_t kFull = 96;
    EXPECT_EQ(to_pixels(Dip{1.0F}, kFull), 1);
    EXPECT_EQ(to_pixels(Dip{0.5F}, kFull), 1);
    EXPECT_EQ(to_pixels(Dip{0.49F}, kFull), 0);
    EXPECT_EQ(to_pixels(Dip{-0.5F}, kFull), 0);
    EXPECT_EQ(to_pixels(Dip{-0.51F}, kFull), -1);
    EXPECT_EQ(to_pixels(Dip{-3.5F}, kFull), -3);
}

TEST(Dpi, OneRuleAtEveryScale)
{
    constexpr std::uint32_t k125 = 120;
    constexpr std::uint32_t k150 = 144;
    constexpr std::uint32_t k175 = 168;
    constexpr std::uint32_t k250 = 240;
    constexpr std::uint32_t k300 = 288;
    EXPECT_EQ(to_pixels(Dip{1.0F}, k125), 1);
    EXPECT_EQ(to_pixels(Dip{2.0F}, k125), 3);
    EXPECT_EQ(to_pixels(Dip{1.0F}, k150), 2);
    EXPECT_EQ(to_pixels(Dip{1.0F}, k175), 2);
    EXPECT_EQ(to_pixels(Dip{24.0F}, k250), 60);
    EXPECT_EQ(to_pixels(Dip{1.5F}, k300), 5);
}

// Two rectangles that share an edge in DIPs share it in pixels: no gap and no overlap, at every scale, because a
// rectangle converts by its edges and never by its width.
void expect_shared_edges(std::uint32_t dpi)
{
    constexpr float kNeighbourWidth = 40.0F;
    constexpr float kHeight = 10.0F;
    float edge = 0.0F;
    for (const float width : {22.0F, 0.5F, 1.5F, 280.0F, 7.25F, 24.5F})
    {
        const PixelRect left =
            to_pixels(DipRect{.left = edge, .top = 0.0F, .right = edge + width, .bottom = kHeight}, dpi);
        const PixelRect right = to_pixels(
            DipRect{.left = edge + width, .top = 0.0F, .right = edge + width + kNeighbourWidth, .bottom = kHeight},
            dpi);
        EXPECT_EQ(left.right, right.left) << width << " DIP wide at " << dpi << " DPI";
        EXPECT_GE(left.width(), 0);
        edge += width;
    }
}

TEST(Dpi, SharedEdgesStayShared)
{
    for (const std::uint32_t dpi : kDpis)
    {
        expect_shared_edges(dpi);
    }
}

} // namespace
