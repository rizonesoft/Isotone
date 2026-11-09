// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/imaging/premultiply.h"

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <cstring>

#if defined(_M_X64) || defined(__x86_64__)
#include <immintrin.h>
#include <intrin.h>
#elif defined(_M_ARM64) || defined(__aarch64__)
#include <arm_neon.h>
#endif

namespace isotone::core::imaging
{
namespace
{

#if defined(_M_X64) || defined(__x86_64__)
[[nodiscard]] bool cpu_has_sse41() noexcept
{
    std::array<int, 4> info{};
    __cpuid(info.data(), 1);
    return (std::get<2>(info) & (1 << 19)) != 0;
}

[[nodiscard]] bool cpu_has_avx2() noexcept
{
    std::array<int, 4> info{};
    __cpuid(info.data(), 0);
    if (std::get<0>(info) < 7)
    {
        return false;
    }
    __cpuid(info.data(), 1);
    constexpr int osxsave_and_avx = (1 << 27) | (1 << 28);
    if ((std::get<2>(info) & osxsave_and_avx) != osxsave_and_avx)
    {
        return false;
    }
    if ((_xgetbv(0) & 0x6U) != 0x6U)
    {
        return false;
    }
    std::array<int, 4> info7{};
    __cpuidex(info7.data(), 7, 0);
    return (std::get<1>(info7) & (1 << 5)) != 0;
}
#endif

} // namespace

bool is_kernel_supported(PremultiplyKernel kernel) noexcept
{
    switch (kernel)
    {
    case PremultiplyKernel::Scalar:
        return true;
    case PremultiplyKernel::Sse41:
#if defined(_M_X64) || defined(__x86_64__)
        return cpu_has_sse41();
#else
        return false;
#endif
    case PremultiplyKernel::Avx2:
#if defined(_M_X64) || defined(__x86_64__)
        return cpu_has_avx2();
#else
        return false;
#endif
    case PremultiplyKernel::Neon:
#if defined(_M_ARM64) || defined(__aarch64__)
        return true;
#else
        return false;
#endif
    }
    return false;
}

std::string_view kernel_name(PremultiplyKernel kernel) noexcept
{
    switch (kernel)
    {
    case PremultiplyKernel::Scalar:
        return "Scalar";
    case PremultiplyKernel::Sse41:
        return "Sse41";
    case PremultiplyKernel::Avx2:
        return "Avx2";
    case PremultiplyKernel::Neon:
        return "Neon";
    }
    return "Unknown";
}

PremultiplyKernel best_supported_kernel() noexcept
{
#if defined(_M_X64) || defined(__x86_64__)
    if (is_kernel_supported(PremultiplyKernel::Avx2))
    {
        return PremultiplyKernel::Avx2;
    }
    if (is_kernel_supported(PremultiplyKernel::Sse41))
    {
        return PremultiplyKernel::Sse41;
    }
    return PremultiplyKernel::Scalar;
#elif defined(_M_ARM64) || defined(__aarch64__)
    return PremultiplyKernel::Neon;
#else
    return PremultiplyKernel::Scalar;
#endif
}

void premultiply_bgra8_scalar(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept
{
    const std::size_t count = std::min(src.size(), dst.size());
    std::ranges::transform(src.first(count), dst.first(count).begin(), premultiply_pixel_scalar);
}

#if defined(_M_X64) || defined(__x86_64__)
[[nodiscard]] __m128i simd_add_epi16(__m128i lhs, __m128i rhs) noexcept
{
    // NOLINTNEXTLINE(portability-simd-intrinsics): architecture-gated SSE4.1 kernel (standards/cpp.md)
    return _mm_add_epi16(lhs, rhs);
}

[[nodiscard]] __m256i simd_add_epi16(__m256i lhs, __m256i rhs) noexcept
{
    // NOLINTNEXTLINE(portability-simd-intrinsics): architecture-gated AVX2 kernel (standards/cpp.md)
    return _mm256_add_epi16(lhs, rhs);
}
#endif

void premultiply_bgra8_sse41(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept
{
#if defined(_M_X64) || defined(__x86_64__)
    const std::size_t count = std::min(src.size(), dst.size());

    const __m128i alpha_shuffle = _mm_setr_epi8(6, 7, 6, 7, 6, 7, -1, -1, 14, 15, 14, 15, 14, 15, -1, -1);
    const __m128i alpha_255 = _mm_setr_epi16(0, 0, 0, 255, 0, 0, 0, 255);
    const __m128i bias_128 = _mm_set1_epi16(128);

    std::size_t idx = 0;
    for (; idx + 4 <= count; idx += 4)
    {
        __m128i packed{};
        std::memcpy(&packed, src.subspan(idx, 4).data(), sizeof(packed));

        const __m128i lo_16 = _mm_cvtepu8_epi16(packed);
        const __m128i hi_16 = _mm_cvtepu8_epi16(_mm_srli_si128(packed, 8));

        const __m128i alpha_lo = _mm_or_si128(_mm_shuffle_epi8(lo_16, alpha_shuffle), alpha_255);
        const __m128i alpha_hi = _mm_or_si128(_mm_shuffle_epi8(hi_16, alpha_shuffle), alpha_255);

        const __m128i prod_lo = simd_add_epi16(_mm_mullo_epi16(lo_16, alpha_lo), bias_128);
        const __m128i prod_hi = simd_add_epi16(_mm_mullo_epi16(hi_16, alpha_hi), bias_128);

        const __m128i res_lo = _mm_srli_epi16(simd_add_epi16(prod_lo, _mm_srli_epi16(prod_lo, 8)), 8);
        const __m128i res_hi = _mm_srli_epi16(simd_add_epi16(prod_hi, _mm_srli_epi16(prod_hi, 8)), 8);

        const __m128i out_packed = _mm_packus_epi16(res_lo, res_hi);
        std::memcpy(dst.subspan(idx, 4).data(), &out_packed, sizeof(out_packed));
    }

    if (idx < count)
    {
        premultiply_bgra8_scalar(src.subspan(idx, count - idx), dst.subspan(idx, count - idx));
    }
#else
    premultiply_bgra8_scalar(src, dst);
#endif
}

void premultiply_bgra8_avx2(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept
{
#if defined(_M_X64) || defined(__x86_64__)
    const std::size_t count = std::min(src.size(), dst.size());

    const __m256i alpha_shuffle = _mm256_setr_epi8(6, 7, 6, 7, 6, 7, -1, -1, 14, 15, 14, 15, 14, 15, -1, -1, 6, 7, 6, 7,
                                                   6, 7, -1, -1, 14, 15, 14, 15, 14, 15, -1, -1);
    const __m256i alpha_255 = _mm256_setr_epi16(0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255);
    const __m256i bias_128 = _mm256_set1_epi16(128);

    std::size_t idx = 0;
    for (; idx + 8 <= count; idx += 8)
    {
        __m128i in_lo{};
        __m128i in_hi{};
        std::memcpy(&in_lo, src.subspan(idx, 4).data(), sizeof(in_lo));
        std::memcpy(&in_hi, src.subspan(idx + 4, 4).data(), sizeof(in_hi));

        const __m256i vec_0 = _mm256_cvtepu8_epi16(in_lo);
        const __m256i vec_1 = _mm256_cvtepu8_epi16(in_hi);

        const __m256i alpha_0 = _mm256_or_si256(_mm256_shuffle_epi8(vec_0, alpha_shuffle), alpha_255);
        const __m256i alpha_1 = _mm256_or_si256(_mm256_shuffle_epi8(vec_1, alpha_shuffle), alpha_255);

        const __m256i prod_0 = simd_add_epi16(_mm256_mullo_epi16(vec_0, alpha_0), bias_128);
        const __m256i prod_1 = simd_add_epi16(_mm256_mullo_epi16(vec_1, alpha_1), bias_128);

        const __m256i res_0 = _mm256_srli_epi16(simd_add_epi16(prod_0, _mm256_srli_epi16(prod_0, 8)), 8);
        const __m256i res_1 = _mm256_srli_epi16(simd_add_epi16(prod_1, _mm256_srli_epi16(prod_1, 8)), 8);

        const __m256i packed = _mm256_packus_epi16(res_0, res_1);
        const __m256i out_vec = _mm256_permute4x64_epi64(packed, _MM_SHUFFLE(3, 1, 2, 0));
        std::memcpy(dst.subspan(idx, 8).data(), &out_vec, sizeof(out_vec));
    }

    if (idx < count)
    {
        premultiply_bgra8_sse41(src.subspan(idx, count - idx), dst.subspan(idx, count - idx));
    }
#else
    premultiply_bgra8_scalar(src, dst);
#endif
}

void premultiply_bgra8_neon(std::span<const Bgra8> src, std::span<Bgra8> dst) noexcept
{
#if defined(_M_ARM64) || defined(__aarch64__)
    const std::size_t count = std::min(src.size(), dst.size());
    const uint16x8_t bias_128 = vdupq_n_u16(0);

    std::size_t idx = 0;
    for (; idx + 8 <= count; idx += 8)
    {
        std::array<std::uint8_t, 32> raw_bytes{};
        std::memcpy(raw_bytes.data(), src.subspan(idx, 8).data(), raw_bytes.size());

        uint8x8x4_t pixels = vld4_u8(raw_bytes.data());
        const uint8x8_t alpha = pixels.val[3];

        const uint16x8_t prod_b = vaddq_u16(vmull_u8(pixels.val[0], alpha), bias_128);
        const uint16x8_t prod_g = vaddq_u16(vmull_u8(pixels.val[1], alpha), bias_128);
        const uint16x8_t prod_r = vaddq_u16(vmull_u8(pixels.val[2], alpha), bias_128);

        pixels.val[0] = vshrn_n_u16(vaddq_u16(prod_b, vshrq_n_u16(prod_b, 8)), 8);
        pixels.val[1] = vshrn_n_u16(vaddq_u16(prod_g, vshrq_n_u16(prod_g, 8)), 8);
        pixels.val[2] = vshrn_n_u16(vaddq_u16(prod_r, vshrq_n_u16(prod_r, 8)), 8);

        vst4_u8(raw_bytes.data(), pixels);
        std::memcpy(dst.subspan(idx, 8).data(), raw_bytes.data(), raw_bytes.size());
    }

    if (idx < count)
    {
        premultiply_bgra8_scalar(src.subspan(idx, count - idx), dst.subspan(idx, count - idx));
    }
#else
    premultiply_bgra8_scalar(src, dst);
#endif
}

void premultiply_bgra8(std::span<const Bgra8> src, std::span<Bgra8> dst, PremultiplyKernel kernel) noexcept
{
    switch (kernel)
    {
    case PremultiplyKernel::Scalar:
        premultiply_bgra8_scalar(src, dst);
        return;
    case PremultiplyKernel::Sse41:
        premultiply_bgra8_sse41(src, dst);
        return;
    case PremultiplyKernel::Avx2:
        premultiply_bgra8_avx2(src, dst);
        return;
    case PremultiplyKernel::Neon:
        premultiply_bgra8_neon(src, dst);
        return;
    }
    premultiply_bgra8_scalar(src, dst);
}

} // namespace isotone::core::imaging
