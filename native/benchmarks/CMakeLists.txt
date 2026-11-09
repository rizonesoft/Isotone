# The native benchmark suite (D00 T04 §2), built only in the test-capable Release presets where Google Benchmark is
# installed through the vcpkg bench feature. Benchmarks never run as timed gates in CI; only `--smoke` (which runs
# every registered correctness guard once) is registered with CTest.
isotone_add_executable(isotone_benchmarks
  main.cpp
  imaging/premultiply_bench.cpp
  LINK isotone::core benchmark::benchmark
  DEV_ONLY)

add_test(NAME isotone_benchmarks_smoke COMMAND isotone_benchmarks --smoke)
