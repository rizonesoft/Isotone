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

1. **Cache-resident tile (`Tile256x256`, 256 x 256 `Bgra8` pixels = 65,536 pixels = 256 KiB input + 256 KiB output):** under `20.0 us` median on one core.
2. **L2-sized buffer (`L2Buffer512x512`, 512 x 512 `Bgra8` pixels = 262,144 pixels = 1 MiB input + 1 MiB output):** under `80.0 us` median on one core.
3. **Whole-image buffer (`WholeImage100MP`, 10,000 x 10,000 `Bgra8` pixels = 100,000,000 pixels = 400 MB input + 400 MB output):** under `100.0 ms` single-core DRAM-bound median (whereas a naive extrapolation of `1,526 x 16.3 us = 24.9 ms` from L1/L2 tile speed ignores DRAM read/write-allocate bandwidth once the 800 MB working set spills past the 12 MiB L3 cache).

## Exported Table (9 Repetitions per Variant)

Raw console and JSON outputs were written to `build/benchmarks/2026-11-09-premultiply.txt` and `build/benchmarks/2026-11-09-premultiply.json`.

| Benchmark | Repetitions | Mean (Wall) | Median (Wall) | Median (CPU) | Stddev (Wall) | Spread (`max - min`) | Throughput (Median) | Speedup vs. `Scalar` (Median Wall) |
| --------- | :---------: | ----------: | ------------: | -----------: | ------------: | -------------------: | ------------------: | ---------------------------------: |
| `Premultiply/Tile256x256/Scalar` | 9 | `145 us` | `149 us` | `148 us` | `16.8 us` | `51.4 us` | `1.65 GiB/s` (`443.2 MP/s`) | `1.00x` |
| `Premultiply/Tile256x256/Sse41` | 9 | `33.1 us` | `33.1 us` | `33.0 us` | `2.05 us` | `6.36 us` | `7.40 GiB/s` (`1.99 GP/s`) | `4.50x` |
| `Premultiply/Tile256x256/Avx2` | 9 | `16.4 us` | `16.3 us` | `16.0 us` | `0.420 us` | `1.24 us` | `15.25 GiB/s` (`4.09 GP/s`) | `9.14x` (`9.25x` CPU) |
| `Premultiply/L2Buffer512x512/Scalar` | 9 | `641 us` | `629 us` | `628 us` | `30.3 us` | `103 us` | `1.56 GiB/s` (`417.6 MP/s`) | `1.00x` |
| `Premultiply/L2Buffer512x512/Sse41` | 9 | `128 us` | `126 us` | `127 us` | `6.87 us` | `20.2 us` | `7.69 GiB/s` (`2.06 GP/s`) | `4.99x` |
| `Premultiply/L2Buffer512x512/Avx2` | 9 | `63.5 us` | `64.1 us` | `61.4 us` | `3.11 us` | `8.52 us` | `15.91 GiB/s` (`4.27 GP/s`) | `9.81x` (`10.23x` CPU) |
| `Premultiply/WholeImage100MP/Scalar` | 9 | `271 ms` | `273 ms` | `260 ms` | `8.35 ms` | `27.5 ms` | `1.43 GiB/s` (`384.0 MP/s`) | `1.00x` |
| `Premultiply/WholeImage100MP/Sse41` | 9 | `95.4 ms` | `95.5 ms` | `91.5 ms` | `1.45 ms` | `4.48 ms` | `4.07 GiB/s` (`1.09 GP/s`) | `2.86x` |
| `Premultiply/WholeImage100MP/Avx2` | 9 | `83.5 ms` | `83.1 ms` | `81.6 ms` | `3.11 ms` | `9.59 ms` | `4.57 GiB/s` (`1.23 GP/s`) | `3.29x` (`3.19x` CPU) |

## Verdict

- **Acceptance rule (`Scalar_median - Variant_median > max(Scalar_spread, Variant_spread)`):**
  - `Tile256x256`: `Sse41` beats `Scalar` by `149 - 33.1 = 115.9 us > 51.4 us` (`4.50x`); `Avx2` beats `Scalar` by `149 - 16.3 = 132.7 us > 51.4 us` (`9.14x` wall, `9.25x` CPU) and beats `Sse41` by `33.1 - 16.3 = 16.8 us > 6.36 us` (`2.03x`).
  - `L2Buffer512x512`: `Sse41` beats `Scalar` by `629 - 126 = 503 us > 103 us` (`4.99x`); `Avx2` beats `Scalar` by `629 - 64.1 = 564.9 us > 103 us` (`9.81x` wall, `10.23x` CPU) and beats `Sse41` by `126 - 64.1 = 61.9 us > 20.2 us` (`1.97x`).
  - `WholeImage100MP`: `Sse41` beats `Scalar` by `273 - 95.5 = 177.5 ms > 27.5 ms` (`2.86x`); `Avx2` beats `Scalar` by `273 - 83.1 = 189.9 ms > 27.5 ms` (`3.29x` wall, `3.19x` CPU) and beats `Sse41` by `95.5 - 83.1 = 12.4 ms > 9.59 ms` (`1.15x`).
- **Budget check:**
  - `Tile256x256`: `Avx2` median `16.3 us` (`16.0 us` CPU) is under the `20.0 us` tile budget (**PASS**).
  - `L2Buffer512x512`: `Avx2` median `64.1 us` (`61.4 us` CPU) is under the `80.0 us` L2 buffer budget (**PASS**).
  - `WholeImage100MP`: `Avx2` median `83.1 ms` (`81.6 ms` CPU) is under the `100.0 ms` single-core DRAM-bound whole-image budget (**PASS**).
- **Overall verdict:** **PASS** (`Avx2` is the winning x64 variant across all three working sets, at `9.14x` `Scalar` on `Tile256x256`, `9.81x` on `L2Buffer512x512`, and `3.29x` on `WholeImage100MP`, with bit-exact agreement verified by `isotone_benchmarks --smoke` and `Premultiply.*`).
