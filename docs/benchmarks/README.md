# Benchmark Records

Every native performance measurement and SIMD optimization in the Isotone Graphics Suite lands with a committed benchmark record in this folder (`docs/benchmarks/<YYYY-MM-DD>-<name>.md`), governed by [`standards/cpp.md`](../../standards/cpp.md) ("SIMD and performance"), [`standards/testing.md`](../../standards/testing.md) ("Benchmarks"), and [`docs/specs/2026-10-22-native-stack-design.md`](../specs/2026-10-22-native-stack-design.md) ("Goals and how each is measured", `D00 T04 §2`).

## Rules

- **Where records and raw outputs live:** Committed benchmark records live at `docs/benchmarks/<YYYY-MM-DD>-<name>.md`. Raw Google Benchmark console and JSON outputs stay in the gitignored `build/benchmarks/` directory and are never committed as unparsed dumps.
- **Immutability:** A committed benchmark record in `docs/benchmarks/<YYYY-MM-DD>-<name>.md` is never edited in place. A rerun on a newer commit or a newer reference machine configuration is committed as a new dated record.
- **Gates vs. timing runs:** Benchmarks are not timed gates in CI. Only `isotone_benchmarks --smoke` (which runs every registered correctness guard once against its independent reference and `Scalar` baseline and exits `0` or `1`) runs in `pwsh scripts/check-all.ps1` (`native benchmarks smoke`) and in the `x64-release` and `arm64-release` CTest suites.
- **Working sets and separate budgets:** Kernel benchmarks measure across distinct working sets (a cache-resident 256 by 256 tile, an L2-sized 256 by 192 buffer whose 192 KiB input plus 192 KiB output = 384 KiB working set fits comfortably within a single core's 512 KiB L2 cache alongside code and stack, and a 100-megapixel 10,000 by 10,000 whole image) with separate immutable input and output buffers per iteration (`benchmark::DoNotOptimize` and `benchmark::ClobberMemory`). Cache-resident tile budgets and whole-image latency budgets are stated and evaluated separately on their own working-set measurements; neither is derived by multiplying or dividing the other.
- **Acceptance rule:** Every benchmark runs with a stated repetition count (`9` repetitions by default) and records both the `median` and the `spread` (`max - min` across repetitions). A SIMD or algorithmic variant counts as faster than `Scalar` only when its `median` beats `Scalar`'s `median` by more than the `spread` (`Scalar_median - Variant_median > max(Scalar_spread, Variant_spread)`), and when its `median` satisfies the working set's stated budget.
- **App benchmark fixture documents:** The spec's small, typical, and large fixture documents per app (with the large fixture at the plan's documented limits) require each app's native document format, which no app has at Phase 0. Each app's first performance section commits its own three fixture documents under `native/tests/fixtures/<app>/benchmark/`, as required by [`docs/plans/2026-10-23-native-replan.md`](../plans/2026-10-23-native-replan.md) ("What every re-plan section must deliver", item 8) for waves 3 (Stilus), 5 (Gesso), and 6 (Albumen).

## Required Fields in Every Record

Every `docs/benchmarks/<YYYY-MM-DD>-<name>.md` file must carry all of the following fields:

1. **Date:** ISO-8601 date (`YYYY-MM-DD`) the benchmark was executed.
2. **Commit:** The `git rev-parse HEAD` commit (or base commit during the section that introduces the benchmark) of the tree that built `isotone_benchmarks`.
3. **Exact command:** The exact command line used to run `isotone_benchmarks` (including `--benchmark_filter` and any output flags).
4. **Reference machine entry:** Link and heading reference to the exact dated entry in [`docs/dev/reference-machine.md`](../dev/reference-machine.md).
5. **CPU instruction sets:** The instruction sets available on the host and the variants exercised by the run (`Scalar`, `Sse41`, `Avx2` on x64; `Scalar`, `Neon` on ARM64).
6. **Toolset and preset:** The pinned MSVC toolset, Windows SDK version, CMake version, and configure/build preset (`x64-release` or `arm64-release`).
7. **Power plan:** The active Windows power scheme name and GUID at the time of measurement.
8. **Exported table:** The benchmark table quoting every working set and variant, its repetition count, `mean`, `median`, `stddev`, `spread` (`max - min`), throughput, and ratio to `Scalar`.
9. **Budget:** The stated performance budget for each budgeted working set (for example, cache-resident 256 by 256 tile under 20 microseconds; 100-megapixel whole image under 30 milliseconds) recorded before the optimization lands.
10. **Verdict:** Pass/fail evaluation against both the working-set budgets and the median-vs-spread acceptance rule (`Scalar_median - Variant_median > spread`), naming the winning variant and its speedup ratio over `Scalar`.
11. **Owning section:** The TODO section address (`DNN TNN §N`) that owns the benchmark and record.
