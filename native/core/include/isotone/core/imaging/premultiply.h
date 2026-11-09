// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include <cstdint>
#include <span>
#include <string_view>

namespace isotone::core::imaging
{

// Canonical 8-bit BGRA pixel layout with alpha in the fourth byte (offset 3), matching Direct2D's
// DXGI_FORMAT_B8G8R8A8_UNORM and the suite's pixel buffers (D01 T03 §1, D00-T05-S3-PR9, D00-T04-S1-PR12).
struct Bgra8
{
    std::uint8_t b;
    std::uint8_t g;
    std::uint8_t r;
    std::uint8_t a;

    friend constexpr bool operator==(const Bgra8&, const Bgra8&) = default;
};

static_assert(sizeof(Bgra8) == 4, "Bgra8 must be a packed 4-byte pixel");
static_assert(alignof(Bgra8) == 1, "Bgra8 must allow unaligned buffer starts");

enum class PremultiplyKernel : std::uint8_t
{
    Scalar,
    Sse41,
    Avx2,
    Neon,
};

// Premultiplies a single 8-bit color channel by 8-bit alpha using exact integer arithmetic:
// round(c * a / 255) with ties away from zero ((c * a + 127) / 255).
[[nodiscard]] constexpr std::uint8_t premultiply_channel_scalar(std::uint8_t channel, std::uint8_t alpha) noexcept
{
    return static_cast<std::uint8_t>(
        ((static_cast<std::uint32_t>(channel) * static_cast<std::uint32_t>(alpha)) + 127U) / 255U);
}

[[nodiscard]] constexpr Bgra8 premultiply_pixel_scalar(Bgra8 pixel) noexcept
{
    return Bgra8{
        .b = premultiply_channel_scalar(pixel.b, pixel.a),
        .g = premultiply_channel_scalar(pixel.g, pixel.a),
        .r = premultiply_channel_scalar(pixel.r, pixel.a),
        .a = pixel.a,
    };
}

[[nodiscard]] bool is_kernel_supported(PremultiplyKernel kernel) noexcept;
[[nodiscard]] std::string_view kernel_name(PremultiplyKernel kernel) noexcept;
[[nodiscard]] PremultiplyKernel best_supported_kernel() noexcept;

void premultiply_bgra8_scalar(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept;
void premultiply_bgra8_sse41(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept;
void premultiply_bgra8_avx2(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept;
void premultiply_bgra8_neon(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept;

void premultiply_bgra8(std::span<const Bgra8> src, std::span<Bgra8> dst, PremultiplyKernel kernel) noexcept;

} // namespace isotone::core::imaging
