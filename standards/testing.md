# Testing Standards

How the suite proves its work. The proofs a TODO checkpoint may cite are defined in [`todo/README.md`](../todo/README.md) ("What counts as proof"), each mapped there to the stage of `pwsh scripts/check-all.ps1` or the CI job that runs it; the gate card sections run is [`.claude/skills/process-todo-section/gates.md`](../.claude/skills/process-todo-section/gates.md). Where this file and the gate card disagree, this file wins and the card is corrected in the same commit. The C++ rules for tests are in [`cpp.md`](cpp.md), "Testing".

## Test targets

- GoogleTest, run through CTest. Every test executable is registered with `isotone_add_test` (`native/cmake/IsotoneTargets.cmake`); configure fails on an executable under `native/tests/` that was not registered, and a test preset with no registered test fails, so a suite cannot silently run nothing.
- One folder per library or app under `native/tests/` (`native/tests/core/`, and `ui/`, `stilus/`, `gesso/`, `albumen/` as their code arrives), mirroring the source it tests.
- Every test runs in every test-capable preset of `native/CMakePresets.json`: `x64-debug`, `x64-release`, `arm64-debug`, `arm64-release`, and the AddressSanitizer presets `x64-asan` and `arm64-asan`. ARM64 executables never run on x64: they are built here and run on ARM64 hardware (`scripts/run-arm64-tests.ps1`, the `native-arm64-tests` CI job), so cross-compiling is never mistaken for running.
- Tests run headless: no window, no message box, no dialog, and a test that runs past 300 seconds fails. A test that needs something a runner lacks (a display, a GPU, a pen) is a driven run with its own proof, never a unit test left to fail.
- Assertions are GoogleTest's own (`EXPECT_*`, `ASSERT_*`), with GoogleMock matchers where they read better. One assertion library in the whole suite.

## Naming and shape

- A case is cited as `Suite.Case`, in the words of the behavior it proves (`BuildInfo.BuildIdShape`, `Save.ReadOnlyTargetRefusesAndKeepsDocumentDirty`). The suite is the unit under test; the case says the scenario and what must hold.
- Arrange, act, assert, one behavior per case. A case that asserts nothing, or only that nothing threw, is not a test.
- No shared mutable state between cases. A case that touches the file system works in its own temporary folder; one that touches settings or app data points the service at that folder. Nothing writes under the real `%LOCALAPPDATA%`, and a test that starts a process stops its whole tree on timeout and teardown.

## Fixtures and fidelity

- Fixtures live under `native/tests/fixtures/<app>/<format>/`, committed, small, and licensed for redistribution (the source and license are recorded in a `README.md` beside them). Each app's performance fixtures (a small, a typical, and a large document, the large one at the plan's documented limits) live under `native/tests/fixtures/<app>/benchmark/`.
- A format reader or writer owes a round trip: open the fixture, save, reopen, and compare against the original or a golden, element by element for vector documents and pixel by pixel within a stated tolerance for raster and RAW output. Goldens produced by a reference implementation record its name and version beside them.
- Fidelity cases are ordinary GoogleTest cases named for the format (`SvgRoundTrip.*`, `PngRoundTrip.*`), so `ctest --preset <preset> -R RoundTrip` runs them all.
- Large corpora (RAW sample sets) are not committed: a script downloads a pinned list with SHA-256 checks into `build/fixtures/`, and at least one small fixture per format is committed so the proof runs on every clone.

## Untrusted input and fuzzing

Every file reader owes two more proofs beside its round trip, and neither substitutes for the other ([`cpp.md`](cpp.md), "Untrusted input"; `D00 T05 §9`):

- **Input safety:** its cases and its malformed-input regression files run clean under AddressSanitizer (`x64-asan`, `arm64-asan`) and under static analysis (`x64-analyze`, `arm64-analyze`, clang-tidy).
- **Fuzzing:** a libFuzzer target registered with `isotone_add_fuzz_target`, a committed seed corpus under `native/tests/fuzz/<reader>/corpus/`, and every crashing input kept under `regressions/`. The regression inputs replay in every test preset (`fuzz.<reader>`), `x64-fuzz-msvc` smoke-checks the targets, and `.github/workflows/fuzz.yml` fuzzes each one nightly.

## Failure paths

Every reader, writer, and user-document path is tested on its failure too: a truncated or corrupt file, a read-only target, a locked file, a full disk (simulated), an unsupported mode. The test asserts the message and that nothing was damaged. Document safety carries its own list of proofs (the spec's "Document safety", Proofs), including the process killed at every step of a save.

## Surfaces

A surface is proven on the rendered interface, never by reading its code:

- **Driven runs:** UI Automation reads and invokes the tree; because invoking through UI Automation bypasses the keyboard, pointer, hit-testing, and input-method paths, those are driven separately, with `SendInput` for the keyboard and mouse, synthetic pointer injection for pen and touch, and a real input method's composition for text. A structured log line, a settings readback, or a saved file inspected is evidence too.
- **Goldens:** the surface rendered offscreen on the WARP software device in the pinned reference environment and compared with its review-approved goldens under `docs/captures/golden/` within the tolerance [`design-contract.md`](design-contract.md) states.
- Both proofs become usable when the foundation that provides them is stamped (`todo/README.md` marks each "unusable for a stamp until" its section lands); until then no section may cite them, and `python scripts/todo-graph.py validate` refuses a checkpoint that does.
- The logic behind a surface (its command, its model, its computed values) is unit tested in the app's core library as well.

## No quarantine

There is no list of excluded tests. A test that fails is fixed, or the code is; a test that cannot run on a runner is a driven run with its own evidence. `noTestsAction: error` and the 300-second limit keep a suite from passing by not running.

## Coverage

Coverage is not gated by a percentage. A section that adds logic adds the tests that pin it; review refuses logic without them, and a mutation that removes the logic must fail a named case.

## Benchmarks

- Native microbenchmarks and working-set benchmarks live under `native/benchmarks/` and build into `isotone_benchmarks` in the test-capable Release presets (`x64-release` and `arm64-release`) only (`D00 T04 §2`), linked against Google Benchmark from the `bench` feature of `native/vcpkg.json` (never installed or linked in `x64-dist` or `arm64-dist`).
- Benchmarks are not timed gates in CI: timing runs execute on the recorded reference machine (`docs/dev/reference-machine.md`), write raw outputs to the gitignored `build/benchmarks/`, and commit an immutable record at `docs/benchmarks/<YYYY-MM-DD>-<name>.md` following `docs/benchmarks/README.md` (`standards/cpp.md`, "SIMD and performance").
- Every benchmark registers a deterministic correctness guard under `isotone_benchmarks --smoke` that compares `Scalar` against an independent reference and every supported SIMD variant (`Sse41` and `Avx2` on x64; `Neon` on ARM64) against `Scalar`. `isotone_benchmarks --smoke` runs in `pwsh scripts/check-all.ps1` (`native benchmarks smoke`) after the native Release build, in the `x64-release` CTest suite, and in the `arm64-release` CTest suite staged by `scripts/run-arm64-tests.ps1` and executed on ARM64 hardware by `.github/workflows/build.yml` (`native-arm64-tests`).
