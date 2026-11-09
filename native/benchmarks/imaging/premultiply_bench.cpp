// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "../benchmarks.h"
#include "isotone/core/imaging/premultiply.h"

#include <algorithm>
#include <array>
#include <benchmark/benchmark.h>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <memory>
#include <random>
#include <span>
#include <string>
#include <vector>

namespace isotone::benchmarks
{
namespace
{

using isotone::core::imaging::Bgra8;
using isotone::core::imaging::is_kernel_supported;
using isotone::core::imaging::kernel_name;
using isotone::core::imaging::premultiply_bgra8;
using isotone::core::imaging::PremultiplyKernel;

constexpr std::size_t kCacheLineAlignment = 64;
constexpr std::size_t kTilePixels = 256ULL * 256ULL;
constexpr std::size_t kL2BufferPixels = 512ULL * 512ULL;
constexpr std::size_t kWholeImage100MPPixels = 10000ULL * 10000ULL;
constexpr int kBenchmarkRepetitions = 9;

// 64-byte aligned pixel array owned through std::unique_ptr (standards/cpp.md, Ownership and lifetimes).
template <std::size_t Count> struct alignas(kCacheLineAlignment) AlignedPixelStorage
{
    std::array<Bgra8, Count> pixels;
};

// Independent floating-point reference (`c * a / 255` rounded to nearest, ties away from zero, on 8-bit BGRA with
// alpha last), used by the smoke correctness guard so a Scalar and SIMD pair agreeing on a wrong answer still fail
// (D00-T05-S3-PR9, D00-T04-S1-PR12).
[[nodiscard]] std::uint8_t independent_reference_channel(std::uint8_t channel, std::uint8_t alpha) noexcept
{
    const double exact = (static_cast<double>(channel) * static_cast<double>(alpha)) / 255.0;
    return static_cast<std::uint8_t>(std::lround(exact));
}

[[nodiscard]] Bgra8 independent_reference_pixel(Bgra8 pixel) noexcept
{
    return Bgra8{
        .b = independent_reference_channel(pixel.b, pixel.a),
        .g = independent_reference_channel(pixel.g, pixel.a),
        .r = independent_reference_channel(pixel.r, pixel.a),
        .a = pixel.a,
    };
}

// Populates `dst` with deterministic seeded random BGRA8 pixels where every pixel has distinct b, g, r, and a channel
// values so a channel-order defect always alters the output (D00-T04-S1-PR12).
void fill_seeded_pixels(std::span<Bgra8> dst, std::uint32_t seed = 0x15070E23U)
{
    std::mt19937 rng{seed};
    for (Bgra8& pixel : dst)
    {
        const std::uint32_t word = rng();
        const auto blue = static_cast<std::uint8_t>(word & 0xFFU);
        auto green = static_cast<std::uint8_t>((word >> 8U) & 0xFFU);
        if (green == blue)
        {
            green = static_cast<std::uint8_t>((green + 53U) & 0xFFU);
        }
        auto red = static_cast<std::uint8_t>((word >> 16U) & 0xFFU);
        while (red == blue || red == green)
        {
            red = static_cast<std::uint8_t>((red + 97U) & 0xFFU);
        }
        auto alpha = static_cast<std::uint8_t>((word >> 24U) & 0xFFU);
        while (alpha == blue || alpha == green || alpha == red)
        {
            alpha = static_cast<std::uint8_t>((alpha + 29U) & 0xFFU);
        }
        pixel = Bgra8{.b = blue, .g = green, .r = red, .a = alpha};
    }
}

[[nodiscard]] double compute_spread(const std::vector<double>& values)
{
    if (values.empty())
    {
        return 0.0;
    }
    const auto [min_it, max_it] = std::ranges::minmax_element(values);
    return *max_it - *min_it;
}

template <std::size_t PixelCount> void run_premultiply_benchmark(benchmark::State& state, PremultiplyKernel kernel)
{
    if (!is_kernel_supported(kernel))
    {
        const std::string reason =
            std::string{"CPU does not support "} + std::string{kernel_name(kernel)} + " instruction set";
        std::cerr << "isotone_benchmarks: skipping " << state.name() << " (" << reason << ")\n";
        state.SkipWithMessage(reason);
        return;
    }

    auto src_buf = std::make_unique_for_overwrite<AlignedPixelStorage<PixelCount>>();
    auto dst_buf = std::make_unique_for_overwrite<AlignedPixelStorage<PixelCount>>();
    std::ranges::fill(dst_buf->pixels, Bgra8{.b = 0, .g = 0, .r = 0, .a = 0});
    if constexpr (PixelCount <= kL2BufferPixels)
    {
        fill_seeded_pixels(src_buf->pixels);
    }
    else
    {
        auto pattern = std::make_unique_for_overwrite<AlignedPixelStorage<kTilePixels>>();
        fill_seeded_pixels(pattern->pixels);
        const std::span<const Bgra8> pat_span{pattern->pixels};
        const std::span<Bgra8> full_span{src_buf->pixels};
        for (std::size_t offset = 0; offset < PixelCount; offset += kTilePixels)
        {
            const std::size_t chunk = std::min(kTilePixels, PixelCount - offset);
            std::copy_n(pat_span.data(), chunk, full_span.subspan(offset, chunk).data());
        }
    }

    const std::span<const Bgra8> src{src_buf->pixels};
    const std::span<Bgra8> dst{dst_buf->pixels};
    for (auto iter : state)
    {
        (void)iter;
        const auto* src_ptr = src.data();
        auto* dst_ptr = dst.data();
        benchmark::DoNotOptimize(src_ptr);
        benchmark::DoNotOptimize(dst_ptr);
        premultiply_bgra8(src, dst, kernel);
        benchmark::DoNotOptimize(dst_ptr);
        benchmark::ClobberMemory();
    }

    state.SetBytesProcessed(static_cast<std::int64_t>(state.iterations()) *
                            static_cast<std::int64_t>(PixelCount * sizeof(Bgra8)));
    state.SetItemsProcessed(static_cast<std::int64_t>(state.iterations()) * static_cast<std::int64_t>(PixelCount));
}

template <std::size_t PixelCount> void register_working_set(std::string_view working_set_name, benchmark::TimeUnit unit)
{
#if defined(_M_X64) || defined(__x86_64__)
    constexpr std::array<PremultiplyKernel, 3> kArchKernels = {
        PremultiplyKernel::Scalar,
        PremultiplyKernel::Sse41,
        PremultiplyKernel::Avx2,
    };
#elif defined(_M_ARM64) || defined(__aarch64__)
    constexpr std::array<PremultiplyKernel, 2> kArchKernels = {
        PremultiplyKernel::Scalar,
        PremultiplyKernel::Neon,
    };
#else
    constexpr std::array<PremultiplyKernel, 1> kArchKernels = {
        PremultiplyKernel::Scalar,
    };
#endif

    for (const PremultiplyKernel kernel : kArchKernels)
    {
        const std::string bench_name =
            std::string{"Premultiply/"} + std::string{working_set_name} + "/" + std::string{kernel_name(kernel)};
        benchmark::RegisterBenchmark(
            bench_name, [kernel](benchmark::State& state) { run_premultiply_benchmark<PixelCount>(state, kernel); })
            ->Unit(unit)
            ->Repetitions(kBenchmarkRepetitions)
            ->ComputeStatistics("spread", compute_spread);
    }
}

} // namespace

void register_premultiply_benchmarks()
{
    register_working_set<kTilePixels>("Tile256x256", benchmark::kMicrosecond);
    register_working_set<kL2BufferPixels>("L2Buffer512x512", benchmark::kMicrosecond);
    register_working_set<kWholeImage100MPPixels>("WholeImage100MP", benchmark::kMillisecond);
}

bool run_premultiply_smoke_guard()
{
    auto src_buf = std::make_unique_for_overwrite<AlignedPixelStorage<kTilePixels>>();
    auto scalar_buf = std::make_unique_for_overwrite<AlignedPixelStorage<kTilePixels>>();
    auto variant_buf = std::make_unique_for_overwrite<AlignedPixelStorage<kTilePixels>>();
    fill_seeded_pixels(src_buf->pixels);

    const std::span<const Bgra8> src{src_buf->pixels};
    const std::span<Bgra8> scalar_out{scalar_buf->pixels};
    premultiply_bgra8(src, scalar_out, PremultiplyKernel::Scalar);

    for (std::size_t idx = 0; idx < kTilePixels; ++idx)
    {
        const Bgra8 src_px = src_buf->pixels.at(idx);
        const Bgra8 got_px = scalar_buf->pixels.at(idx);
        const Bgra8 expected = independent_reference_pixel(src_px);
        if (got_px != expected)
        {
            std::cerr << "isotone_benchmarks --smoke: Scalar differed from independent reference at pixel " << idx
                      << " input=(" << static_cast<int>(src_px.b) << "," << static_cast<int>(src_px.g) << ","
                      << static_cast<int>(src_px.r) << "," << static_cast<int>(src_px.a) << ") got=("
                      << static_cast<int>(got_px.b) << "," << static_cast<int>(got_px.g) << ","
                      << static_cast<int>(got_px.r) << "," << static_cast<int>(got_px.a) << ") want=("
                      << static_cast<int>(expected.b) << "," << static_cast<int>(expected.g) << ","
                      << static_cast<int>(expected.r) << "," << static_cast<int>(expected.a) << ")\n";
            return false;
        }
    }

#if defined(_M_X64) || defined(__x86_64__)
    constexpr std::array<PremultiplyKernel, 2> kSimdKernels = {
        PremultiplyKernel::Sse41,
        PremultiplyKernel::Avx2,
    };
#elif defined(_M_ARM64) || defined(__aarch64__)
    constexpr std::array<PremultiplyKernel, 1> kSimdKernels = {
        PremultiplyKernel::Neon,
    };
#else
    constexpr std::array<PremultiplyKernel, 0> kSimdKernels = {};
#endif

    for (const PremultiplyKernel kernel : kSimdKernels)
    {
        if (!is_kernel_supported(kernel))
        {
            std::cout << "isotone_benchmarks --smoke: skipping " << kernel_name(kernel)
                      << " (CPU lacks instruction set)\n";
            continue;
        }
        variant_buf->pixels.fill(Bgra8{});
        premultiply_bgra8(src, variant_buf->pixels, kernel);
        for (std::size_t idx = 0; idx < kTilePixels; ++idx)
        {
            const Bgra8 src_px = src_buf->pixels.at(idx);
            const Bgra8 got_px = variant_buf->pixels.at(idx);
            const Bgra8 want_px = scalar_buf->pixels.at(idx);
            if (got_px != want_px)
            {
                std::cerr << "isotone_benchmarks --smoke: variant " << kernel_name(kernel)
                          << " differed from Scalar at pixel " << idx << " input=(" << static_cast<int>(src_px.b) << ","
                          << static_cast<int>(src_px.g) << "," << static_cast<int>(src_px.r) << ","
                          << static_cast<int>(src_px.a) << ") got=(" << static_cast<int>(got_px.b) << ","
                          << static_cast<int>(got_px.g) << "," << static_cast<int>(got_px.r) << ","
                          << static_cast<int>(got_px.a) << ") want=(" << static_cast<int>(want_px.b) << ","
                          << static_cast<int>(want_px.g) << "," << static_cast<int>(want_px.r) << ","
                          << static_cast<int>(want_px.a) << ")\n";
                return false;
            }
        }
    }

    return true;
}

} // namespace isotone::benchmarks
