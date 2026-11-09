# Benchmark Record: Premultiply (8-bit BGRA)

- **Date:** `2026-11-09`
- **Commit:** `eb80b9ce7fbcd6cb70c50a3b3ff3ac90c5628f4d` (base of `D00 T04 §2`)
- **Exact command:** `.\artifacts\native\x64-release\benchmarks\isotone_benchmarks.exe --benchmark_filter=Premultiply --benchmark_out=build/benchmarks/2026-11-09-premultiply.json --benchmark_out_format=json`
- **Reference machine entry:** [`docs/dev/reference-machine.md#2026-11-09`](../dev/reference-machine.md#2026-11-09) (`11th Gen Intel(R) Core(TM) i5-11600K @ 3.90GHz`, 6 cores / 12 threads, L1d 6 x 48 KiB, L2 6 x 512 KiB, L3 12,288 KiB, 32 GiB DDR4-2133, Windows 11 26H2 build `26300.9818`)
- **CPU instruction sets:** Host supports SSE2, SSE4.1, SSE4.2, AVX, AVX2, FMA, and AVX-512; run exercises `Scalar`, `Sse41`, and `Avx2` on x64 (`Neon` runs on ARM64 via `isotone_benchmarks_smoke`).
- **Toolset and preset:** MSVC `19.51.36260` (toolset `14.51.36231`), Windows SDK `10.0.26100.0`, CMake `4.3.1`, Ninja `1.13.2`, Google Benchmark `1.9.5`, preset `x64-release` (`/O2 /W4 /WX /permissive- /std:c++23preview /MT /guard:cf /CETCOMPAT`).
- **Power plan:** `Balanced` (`381b4222-f694-41f0-9685-ff5bb260df2e`)
- **Owning section:** `D00 T04 §2`

## Budgets

Each working set is budgeted and evaluated independently on its own measurement (`D00-T04-S1-PR15`); the whole-image latency claim rests solely on the `WholeImage100MP` run and is never extrapolated by multiplying the cache-resident tile time:

1. **Cache-resident tile (`Tile256x256`, 256 x 256 `Bgra8` pixels = 65,536 pixels = 256 KiB input + 256 KiB output = 512 KiB working set):** under `20.0 us` median on one core.
2. **L2-sized buffer (`L2Buffer256x192`, 256 x 192 `Bgra8` pixels = 49,152 pixels = 192 KiB input + 192 KiB output = 384 KiB working set, fitting strictly inside a single core's 512 KiB unified L2 cache on the reference machine alongside code and stack):** under `16.0 us` median on one core.
3. **Whole-image buffer (`WholeImage100MP`, 10,000 x 10,000 `Bgra8` pixels = 100,000,000 pixels = 400 MB input + 400 MB output):** under `100.0 ms` single-core DRAM-bound median (whereas a naive extrapolation of `1,526 x 16.4 us = 25.0 ms` from L1/L2 tile speed ignores DRAM read/write-allocate bandwidth once the 800 MB working set spills past the 12 MiB L3 cache).

## Exported Table (9 Repetitions per Variant)

Raw console and JSON outputs were written to `build/benchmarks/2026-11-09-premultiply.txt` and `build/benchmarks/2026-11-09-premultiply.json`.

| Benchmark | Repetitions | Mean (Wall) | Median (Wall) | Median (CPU) | Stddev (Wall) | Spread (`max - min`) | Throughput (Median) | Speedup vs. `Scalar` (Median Wall) |
| --------- | :---------: | ----------: | ------------: | -----------: | ------------: | -------------------: | ------------------: | ---------------------------------: |
| `Premultiply/Tile256x256/Scalar` | 9 | `140 us` | `139 us` | `135 us` | `12.0 us` | `35.1 us` | `1.81 GiB/s` (`485.6 MP/s`) | `1.00x` |
| `Premultiply/Tile256x256/Sse41` | 9 | `30.9 us` | `30.4 us` | `30.1 us` | `1.67 us` | `6.11 us` | `8.10 GiB/s` (`2.17 GP/s`) | `4.57x` |
| `Premultiply/Tile256x256/Avx2` | 9 | `16.4 us` | `16.4 us` | `16.0 us` | `0.533 us` | `1.85 us` | `15.22 GiB/s` (`4.08 GP/s`) | `8.48x` (`8.44x` CPU) |
| `Premultiply/L2Buffer256x192/Scalar` | 9 | `120 us` | `120 us` | `120 us` | `3.38 us` | `9.04 us` | `1.53 GiB/s` (`410.9 MP/s`) | `1.00x` |
| `Premultiply/L2Buffer256x192/Sse41` | 9 | `23.7 us` | `23.1 us` | `23.1 us` | `1.76 us` | `5.71 us` | `7.92 GiB/s` (`2.13 GP/s`) | `5.19x` |
| `Premultiply/L2Buffer256x192/Avx2` | 9 | `13.3 us` | `13.1 us` | `13.2 us` | `0.761 us` | `2.39 us` | `13.89 GiB/s` (`3.73 GP/s`) | `9.16x` (`9.09x` CPU) |
| `Premultiply/WholeImage100MP/Scalar` | 9 | `272 ms` | `246 ms` | `245 ms` | `47.5 ms` | `142 ms` | `1.52 GiB/s` (`408.5 MP/s`) | `1.00x` |
| `Premultiply/WholeImage100MP/Sse41` | 9 | `97.5 ms` | `101 ms` | `88.5 ms` | `10.3 ms` | `30.7 ms` | `4.21 GiB/s` (`1.13 GP/s`) | `2.44x` (`2.77x` CPU) |
| `Premultiply/WholeImage100MP/Avx2` | 9 | `97.6 ms` | `95.7 ms` | `78.1 ms` | `7.69 ms` | `22.2 ms` | `4.77 GiB/s` (`1.28 GP/s`) | `2.57x` (`3.14x` CPU) |

## Verdict

- **Acceptance rule (`Scalar_median - Variant_median > max(Scalar_spread, Variant_spread)`):**
  - `Tile256x256`: `Sse41` beats `Scalar` by `139 - 30.4 = 108.6 us > 35.1 us` (`4.57x`); `Avx2` beats `Scalar` by `139 - 16.4 = 122.6 us > 35.1 us` (`8.48x` wall, `8.44x` CPU) and beats `Sse41` by `30.4 - 16.4 = 14.0 us > 6.11 us` (`1.85x`).
  - `L2Buffer256x192`: `Sse41` beats `Scalar` by `120 - 23.1 = 96.9 us > 9.04 us` (`5.19x`); `Avx2` beats `Scalar` by `120 - 13.1 = 106.9 us > 9.04 us` (`9.16x` wall, `9.09x` CPU) and beats `Sse41` by `23.1 - 13.1 = 10.0 us > 5.71 us` (`1.76x`).
  - `WholeImage100MP`: `Sse41` beats `Scalar` by `246 - 101 = 145 ms > 142 ms` (`2.44x` wall; `245 - 88.5 = 156.5 ms > 78.1 ms`, `2.77x` CPU); `Avx2` beats `Scalar` by `246 - 95.7 = 150.3 ms > 142 ms` (`2.57x` wall; `245 - 78.1 = 166.9 ms > 78.1 ms`, `3.14x` CPU).
- **Budget check:**
  - `Tile256x256`: `Avx2` median `16.4 us` (`16.0 us` CPU) is under the `20.0 us` tile budget (**PASS**).
  - `L2Buffer256x192`: `Avx2` median `13.1 us` (`13.2 us` CPU) is under the `16.0 us` L2 buffer budget (**PASS**).
  - `WholeImage100MP`: `Avx2` median `95.7 ms` (`78.1 ms` CPU) is under the `100.0 ms` single-core DRAM-bound whole-image budget (**PASS**).
- **Overall verdict:** **PASS** (`Avx2` is the winning x64 variant across all three working sets, at `8.48x` `Scalar` on `Tile256x256`, `9.16x` on `L2Buffer256x192`, and `2.57x` wall / `3.14x` CPU on `WholeImage100MP`, with bit-exact agreement verified by `isotone_benchmarks --smoke` and `Premultiply.*`).
