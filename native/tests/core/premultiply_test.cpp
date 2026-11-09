// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/imaging/premultiply.h"

#include <array>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <gtest/gtest.h>
#include <span>
#include <vector>

namespace isotone::core::imaging
{
namespace
{

// Independent floating-point reference (`c * a / 255` rounded to nearest, ties away from zero, on 8-bit BGRA with
// alpha last), written without sharing any integer formula with premultiply_channel_scalar (D00-T05-S3-PR9).
[[nodiscard]] std::uint8_t reference_channel(std::uint8_t channel, std::uint8_t alpha) noexcept
{
    const double exact = (static_cast<double>(channel) * static_cast<double>(alpha)) / 255.0;
    return static_cast<std::uint8_t>(std::lround(exact));
}

[[nodiscard]] Bgra8 reference_pixel(Bgra8 pixel) noexcept
{
    return Bgra8{
        .b = reference_channel(pixel.b, pixel.a),
        .g = reference_channel(pixel.g, pixel.a),
        .r = reference_channel(pixel.r, pixel.a),
        .a = pixel.a,
    };
}

constexpr std::array<PremultiplyKernel, 4> kAllKernels = {
    PremultiplyKernel::Scalar,
    PremultiplyKernel::Sse41,
    PremultiplyKernel::Avx2,
    PremultiplyKernel::Neon,
};

} // namespace

TEST(Premultiply, AlphaBoundaryLiteralVectors)
{
    struct VectorCase
    {
        Bgra8 input;
        Bgra8 expected;
    };

    // Literal vectors at alpha boundaries 0, 1, 127, 128, 254, and 255 with distinct b, g, r, a values so any channel
    // swap or truncation-toward-zero defect fails immediately (D00-T05-S3-PR9, D00-T04-S1-PR12).
    constexpr std::array<VectorCase, 6> kVectors = {{
        {.input = Bgra8{.b = 200, .g = 128, .r = 1, .a = 0}, .expected = Bgra8{.b = 0, .g = 0, .r = 0, .a = 0}},
        {.input = Bgra8{.b = 200, .g = 128, .r = 1, .a = 1}, .expected = Bgra8{.b = 1, .g = 1, .r = 0, .a = 1}},
        {.input = Bgra8{.b = 201, .g = 128, .r = 2, .a = 127}, .expected = Bgra8{.b = 100, .g = 64, .r = 1, .a = 127}},
        {.input = Bgra8{.b = 199, .g = 127, .r = 1, .a = 128}, .expected = Bgra8{.b = 100, .g = 64, .r = 1, .a = 128}},
        {.input = Bgra8{.b = 200, .g = 128, .r = 1, .a = 254}, .expected = Bgra8{.b = 199, .g = 127, .r = 1, .a = 254}},
        {.input = Bgra8{.b = 200, .g = 128, .r = 1, .a = 255}, .expected = Bgra8{.b = 200, .g = 128, .r = 1, .a = 255}},
    }};

    std::array<Bgra8, kVectors.size()> inputs{};
    for (std::size_t idx = 0; idx < kVectors.size(); ++idx)
    {
        inputs.at(idx) = kVectors.at(idx).input;
        EXPECT_EQ(reference_pixel(kVectors.at(idx).input), kVectors.at(idx).expected) << "vector index " << idx;
    }

    for (const PremultiplyKernel kernel : kAllKernels)
    {
        if (!is_kernel_supported(kernel))
        {
            continue;
        }
        std::array<Bgra8, kVectors.size()> actual{};
        premultiply_bgra8(inputs, actual, kernel);
        for (std::size_t idx = 0; idx < kVectors.size(); ++idx)
        {
            const Bgra8 got = actual.at(idx);
            EXPECT_EQ(got, kVectors.at(idx).expected)
                << "kernel=" << kernel_name(kernel) << " index=" << idx << " actual=(" << static_cast<int>(got.b) << ","
                << static_cast<int>(got.g) << "," << static_cast<int>(got.r) << "," << static_cast<int>(got.a) << ")";
        }
    }
}

TEST(Premultiply, ZeroLengthDoesNotTouchDestination)
{
    constexpr Bgra8 kSentinel{.b = 0xAA, .g = 0xBB, .r = 0xCC, .a = 0xDD};
    const std::array<Bgra8, 4> src = {
        Bgra8{.b = 10, .g = 20, .r = 30, .a = 40},
        Bgra8{.b = 50, .g = 60, .r = 70, .a = 80},
        Bgra8{.b = 90, .g = 100, .r = 110, .a = 120},
        Bgra8{.b = 130, .g = 140, .r = 150, .a = 160},
    };

    for (const PremultiplyKernel kernel : kAllKernels)
    {
        if (!is_kernel_supported(kernel))
        {
            continue;
        }
        std::array<Bgra8, 4> dst = {kSentinel, kSentinel, kSentinel, kSentinel};
        premultiply_bgra8(std::span<const Bgra8>{src}.first(0), std::span<Bgra8>{dst}.first(0), kernel);
        for (const Bgra8& pixel : dst)
        {
            EXPECT_EQ(pixel, kSentinel) << "kernel=" << kernel_name(kernel);
        }
    }
}

void verify_tail_for_kernel(std::span<const Bgra8> src, PremultiplyKernel kernel)
{
    constexpr Bgra8 kGuard{.b = 0xDE, .g = 0xAD, .r = 0xBE, .a = 0xEF};
    const std::size_t len = src.size();
    std::vector<Bgra8> dst(len + 2, kGuard);
    const auto dst_slice = std::span<Bgra8>{dst}.subspan(1, len);
    premultiply_bgra8(src, dst_slice, kernel);

    EXPECT_EQ(dst.front(), kGuard) << "kernel=" << kernel_name(kernel) << " len=" << len;
    EXPECT_EQ(dst.back(), kGuard) << "kernel=" << kernel_name(kernel) << " len=" << len;
    for (std::size_t idx = 0; idx < len; ++idx)
    {
        EXPECT_EQ(dst.at(idx + 1), reference_pixel(src.subspan(idx, 1).front()))
            << "kernel=" << kernel_name(kernel) << " len=" << len << " idx=" << idx;
    }
}

TEST(Premultiply, TailShorterThanOneVectorMatchesReference)
{
    constexpr std::array<std::size_t, 9> kLengths = {1, 2, 3, 5, 6, 7, 9, 13, 15};

    for (const std::size_t len : kLengths)
    {
        std::vector<Bgra8> src(len);
        for (std::size_t idx = 0; idx < len; ++idx)
        {
            src.at(idx) = Bgra8{
                .b = static_cast<std::uint8_t>(((idx * 41U) + 17U) & 0xFFU),
                .g = static_cast<std::uint8_t>(((idx * 73U) + 53U) & 0xFFU),
                .r = static_cast<std::uint8_t>(((idx * 131U) + 97U) & 0xFFU),
                .a = static_cast<std::uint8_t>(((idx * 193U) + 1U) & 0xFFU),
            };
        }

        for (const PremultiplyKernel kernel : kAllKernels)
        {
            if (is_kernel_supported(kernel))
            {
                verify_tail_for_kernel(src, kernel);
            }
        }
    }
}

TEST(Premultiply, UnalignedStartMatchesReference)
{
    constexpr std::size_t kPixelCount = 37;
    constexpr std::size_t kStorageCount = 48; // 48 * 4 = 192 bytes (multiple of 64).

    alignas(64) std::array<Bgra8, kStorageCount> src_storage{};
    for (std::size_t idx = 0; idx < src_storage.size(); ++idx)
    {
        src_storage.at(idx) = Bgra8{
            .b = static_cast<std::uint8_t>(((idx * 29U) + 11U) & 0xFFU),
            .g = static_cast<std::uint8_t>(((idx * 83U) + 101U) & 0xFFU),
            .r = static_cast<std::uint8_t>(((idx * 149U) + 211U) & 0xFFU),
            .a = static_cast<std::uint8_t>(((idx * 67U) + 127U) & 0xFFU),
        };
    }

    for (std::size_t pixel_offset = 1; pixel_offset < 8; ++pixel_offset)
    {
        const auto unaligned_src = std::span<const Bgra8>{src_storage}.subspan(pixel_offset, kPixelCount);
        for (const PremultiplyKernel kernel : kAllKernels)
        {
            if (!is_kernel_supported(kernel))
            {
                continue;
            }
            alignas(64) std::array<Bgra8, kStorageCount> dst_storage{};
            const auto unaligned_dst = std::span<Bgra8>{dst_storage}.subspan(pixel_offset, kPixelCount);
            premultiply_bgra8(unaligned_src, unaligned_dst, kernel);
            for (std::size_t idx = 0; idx < kPixelCount; ++idx)
            {
                EXPECT_EQ(dst_storage.at(pixel_offset + idx), reference_pixel(src_storage.at(pixel_offset + idx)))
                    << "kernel=" << kernel_name(kernel) << " pixel_offset=" << pixel_offset << " idx=" << idx;
            }
        }
    }
}

TEST(Premultiply, ForcedInstructionSetsMatchScalarAcrossAllBytePairs)
{
    constexpr std::size_t kPairCount = 256ULL * 256ULL;
    std::vector<Bgra8> src(kPairCount);
    std::vector<Bgra8> scalar_out(kPairCount);

    for (std::size_t alpha = 0; alpha < 256; ++alpha)
    {
        for (std::size_t chan = 0; chan < 256; ++chan)
        {
            const std::size_t idx = (alpha << 8U) | chan;
            src.at(idx) = Bgra8{
                .b = static_cast<std::uint8_t>(chan),
                .g = static_cast<std::uint8_t>(((chan * 73U) + 19U) & 0xFFU),
                .r = static_cast<std::uint8_t>(((chan * 151U) + 103U) & 0xFFU),
                .a = static_cast<std::uint8_t>(alpha),
            };
        }
    }

    premultiply_bgra8(src, scalar_out, PremultiplyKernel::Scalar);
    for (std::size_t idx = 0; idx < kPairCount; ++idx)
    {
        ASSERT_EQ(scalar_out.at(idx), reference_pixel(src.at(idx))) << "scalar vs reference at index=" << idx;
    }

    for (const PremultiplyKernel kernel : kAllKernels)
    {
        if (kernel == PremultiplyKernel::Scalar || !is_kernel_supported(kernel))
        {
            continue;
        }
        std::vector<Bgra8> simd_out(kPairCount);
        premultiply_bgra8(src, simd_out, kernel);
        for (std::size_t idx = 0; idx < kPairCount; ++idx)
        {
            ASSERT_EQ(simd_out.at(idx), scalar_out.at(idx)) << "kernel=" << kernel_name(kernel) << " index=" << idx;
        }
    }
}

} // namespace isotone::core::imaging
