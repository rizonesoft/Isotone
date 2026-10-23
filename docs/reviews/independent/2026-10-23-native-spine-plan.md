## Round 1: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T23:39:58Z
- Effort: xhigh
- Lines: 34
- Digest: e89870146a74df7c

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-05-native-spine.md:124`: `WILL_FAIL TRUE` reverses the result of `PASS_REGULAR_EXPRESSION`. For a normally exiting process, matching the ASan report makes this test fail; missing the report can make it pass, including an uninstrumented probe returning zero. This defeats §5’s checkpoint. [CTest implementation](https://github.com/Kitware/CMake/blob/v4.3.1/Source/CTest/cmCTestRunTest.cxx#L110-L186).
2. P1 `todo/00-workspace/TODO-04-native-code-policy.md:65`: The register gate checks direct manifest names and populated cells, without checking resolved versions or transitive libraries. Adding `libpng` with one complete row leaves its statically linked zlib dependency unregistered; changing the baseline while retaining an old register version also passes. The advisory job consequently checks an incomplete or incorrect inventory. [libpng’s dependencies](https://github.com/microsoft/vcpkg/blob/master/ports/libpng/vcpkg.json).
3. P1 `todo/00-workspace/TODO-05-native-spine.md:135`: Checking that a decision heading exists does not authorize the budget’s value. Change `default_mb` from 30 to 300 while retaining `"decision": "The output size budget"`: every prescribed check still passes without a decision approving that increase.

### consistency: needs-attention

4. P1 `todo/00-workspace/TODO-04-native-code-policy.md:64`: §1 requires a complete Google Benchmark row and zero `orphan-row` findings, but Benchmark enters the manifest only in §2, which depends on §1. Following the dependency order makes §1’s checkpoint fail. Move the row’s creation alongside its manifest dependency.
5. P1 `todo/00-workspace/TODO-05-native-spine.md:145`: Neither check-all nor its prescribed CI stages builds ARM64 Debug. An error guarded by `_M_ARM64` and `_DEBUG` escapes every required run, despite the spec requiring Debug and Release on both architectures.
6. P2 `todo/00-workspace/TODO-04-native-code-policy.md:64`: The rewrite drops the existing native-payload inventory and required notices and architecture-payload evidence, without assigning successors. Compare the parent’s §1 items at lines 74 and 76. The new register covers vcpkg entries only, leaving the surviving C# apps’ native assets outside the inventory. This violates the spec’s preservation requirement and the re-plan’s retention of acceptance requirements.
7. P2 `todo/00-workspace/TODO-05-native-spine.md:158`: The permitted local ARM64 fallback cannot satisfy the section’s unconditional checkpoint at line 162 or file verification at line 192, both demanding green `native-arm64-tests` jobs. When runner availability triggers the fallback, the section remains unstampable despite completing the specified alternative.

### integration: needs-attention

8. P1 `todo/00-workspace/TODO-05-native-spine.md:112`: Formatting every source and header under `native/` also formats the GoogleTest installation left under `native/vcpkg_installed/` by §2. GoogleTest’s headers do not follow the prescribed Microsoft style, so §4 cannot obtain its required clean result without changing or excluding dependency files. The source-selection rule needs to distinguish maintained sources from installed dependencies.
9. P2 `todo/00-workspace/TODO-04-native-code-policy.md:78`: Adding the `bench` feature does not enable it. §3’s presets select only `VCPKG_MANIFEST_FEATURES=test`, and this section never updates that selection. On a clean clone, the Release benchmark target lacks its dependency and check-all cannot run the required smoke executable. [vcpkg feature selection](https://learn.microsoft.com/en-us/vcpkg/users/buildsystems/cmake-integration#vcpkg_manifest_features).
10. P2 `todo/00-workspace/TODO-05-native-spine.md:162`: Pushing the negative probe to a throwaway branch does not trigger the existing build workflow, whose push filter is `main`. The checklist neither changes that filter nor dispatches the workflow on the probe ref, so the demanded failing run is absent.
11. P2 `todo/00-workspace/TODO-05-native-spine.md:99`: `git describe --always --dirty` returns an annotated tag name when one is reachable, while `BuildInfo.BuildIdShape` accepts only hexadecimal hashes. The first annotated app release tag therefore breaks the test, and subsequent descriptions retain the tag prefix. [Git’s documented output](https://git-scm.com/docs/git-describe#_description).

### source-defect: needs-attention

12. P1 `todo/00-workspace/TODO-05-native-spine.md:100`: The configure-time check reads a file generated after configuration. On a clean build, `compile_commands.json` does not exist; on reconfiguration, it describes the previous generation and can miss the newly planted standard violation. The prescribed configure-failure checkpoint cannot reliably work this way. [CMake generation timing](https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html).
13. P1 `todo/00-workspace/TODO-05-native-spine.md:97`: `gtest_discover_tests` defaults to executing the test binary immediately after building it. The required ARM64 cross-build on x64 therefore tries to launch an ARM64 executable before §8 transfers it to ARM64. Specify deferred discovery or another executable cross-compilation strategy. [GoogleTest integration documentation](https://cmake.org/cmake/help/latest/module/GoogleTest.html#command:gtest_discover_tests).
14. P1 `todo/00-workspace/TODO-05-native-spine.md:85`: Adding `/fsanitize=address` alone leaves incompatible Debug runtime checks enabled. The installed vcpkg Windows toolchain explicitly supplies `/RTC1` in its Debug flags, so the demanded sanitizer-triplet installation fails before §5 can complete it. The sanitizer configuration must disable those checks in dependency builds too. [MSVC incompatibilities](https://learn.microsoft.com/en-us/cpp/sanitizers/asan-known-issues#incompatible-options-and-functionality).
15. P2 `todo/00-workspace/TODO-05-native-spine.md:85`: Entering the pinned developer environment does not pin vcpkg’s compiler selection. Its Windows triplets select Visual Studio and default to the latest installed toolset minor version. Install a newer toolset alongside the pin: dev-env can pass while dependencies use another compiler, contrary to the spec’s ABI containment. [vcpkg selection rules](https://learn.microsoft.com/en-us/vcpkg/users/triplets#vcpkg_visual_studio_path).
16. P2 `todo/00-workspace/TODO-05-native-spine.md:96`: The common flags apply `/CETCOMPAT` to ARM64 targets, although Microsoft documents that switch as x64-only. The target helper needs architecture-specific linker options. [Microsoft’s supported architecture](https://learn.microsoft.com/en-us/cpp/build/reference/cetcompat).

### record: needs-attention

17. P2 `todo/00-workspace/TODO-04-native-code-policy.md:16`: The Current state says the 2026-09-30 decision remains in `docs/dev/decisions.md`, and line 68 requires annotating that existing entry. It does not exist. The parent TODO still owed its creation. Searching the decision log for `2026-09-30` returns no match, leaving the runner to invent the missing historical-record step.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 1

Every finding was verified against the repository or the cited documentation and is real.

1. P1, `WILL_FAIL` inverts the probe's regular expression: verified against CTest's `cmCTestRunTest`. The probe keeps `PASS_REGULAR_EXPRESSION` and drops `WILL_FAIL`.
2. P1, the register missed transitive ports and resolved versions: verified (libpng pulls zlib). The lint reads the installed tree for every triplet and feature, checks each port's version, and the register gains a Pulled in by column.
3. P1, a budget heading did not authorize its value: verified. The decision entry carries `**Budget:** 30 MB` and the gate compares it with `default_mb`; a probe of 300 must fail.
4. P1, the benchmark row came before its manifest entry: verified. §1 creates only the GoogleTest row; §2 adds the benchmark port and its row together.
5. P1, ARM64 Debug was never built: verified. `arm64-debug` joins the workflow presets, check-all, CI, and the ARM64 test job.
6. P2, the shipped-native inventory and its notice and architecture evidence were dropped: verified. The C# payload inventory is recorded as superseded (no C# app ships again), and the register gains Notices shipped and Architectures columns; the supersession map names where they went.
7. P2, the local ARM64 fallback could never satisfy the checkpoint: verified. The checkpoint and Verification accept whichever path the decision log names.
8. P1, formatting would touch installed dependencies: verified. Installs go to `artifacts/vcpkg_installed`, and the format gate reads only `git ls-files` under `native/`.
9. P2, the `bench` feature was never enabled: verified. The Release presets add it to `VCPKG_MANIFEST_FEATURES`.
10. P2, a throwaway branch push does not trigger the build workflow: verified (`branches: [main]`). The probe runs with `gh workflow run build.yml --ref <branch>`.
11. P2, `git describe` prints tag names: verified. The build id is `git rev-parse --short=12 HEAD` plus `-dirty`, tested on a tagged commit.
12. P1, `compile_commands.json` is written after configure-time code: verified. The standard switch is checked by `scripts/native-std-check.py` after generation, with a self-test.
13. P1, `gtest_discover_tests` runs test executables after the build: verified. `DISCOVERY_MODE PRE_TEST`.
14. P1, vcpkg's Debug flags carry `/RTC1`, which AddressSanitizer refuses: verified. The sanitizer triplet builds release only and the asan preset uses `RelWithDebInfo`.
15. P2, built-in triplets do not pin the toolset minor version: verified. Overlay triplets set `VCPKG_PLATFORM_TOOLSET_VERSION`, and dev-env checks them against the pin.
16. P2, `/CETCOMPAT` is x64-only: verified. Applied on x64 only, with a check on the ARM64 link line.
17. P2, the 2026-09-30 decision entry does not exist: verified. §1 now writes it as history with its supersession line.

## Round 2: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-22T23:54:25Z
- Effort: xhigh
- Lines: 26
- Digest: 125da222e70a9bca

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-05-native-spine.md:100`: The standard checker accepts `/std:c++23preview /std:c++20`: the pinned switch is present and `c++latest` is absent, but MSVC selects C++20. Verified read-only with `cl /Zs /W4 /WX /std:c++23preview /std:c++20 /TP todo/.warning-baseline`: D9025, exit 0. The checker must reject conflicting switches or validate the effective one. [MSVC precedence](https://learn.microsoft.com/en-us/cpp/error-messages/tool-errors/command-line-warning-d9025).
2. P1 `todo/00-workspace/TODO-05-native-spine.md:146`: The prescribed artifact stage invokes the import gate without requiring size enforcement. Section 6 makes the size check conditional on `--budget-mb`; its only explicit size invocation is the negative probe. An oversized folder can therefore pass the prescribed check-all stages. Require the normal invocation to enforce the approved budget and prove that with an oversized fixture.
3. P1 `todo/00-workspace/TODO-05-native-spine.md:169`: The fuzz helper and qualification never require coverage and sanitizer instrumentation in the libraries being fuzzed. Instrumenting only the executable containing the qualification parser satisfies every checkpoint, while a reader compiled into `isotone_core` can remain uninstrumented. Qualify a parser in a separately compiled library and require instrumented library variants. [LLVM instrumentation requirements](https://llvm.org/docs/LibFuzzer.html#fuzzer-usage).
4. P2 `todo/00-workspace/TODO-04-native-code-policy.md:94`: The OSV algorithm omits pagination despite requiring every advisory to be reported. A first response carrying `next_page_token`, with an advisory on the second page, escapes the prescribed single-query implementation and fixtures. Require token traversal until exhaustion, including failure handling for subsequent pages. [OSV pagination](https://google.github.io/osv.dev/post-v1-query/#pagination).

### consistency: needs-attention

5. P1 `todo/00-workspace/TODO-05-native-spine.md:146`: Section 7 narrows §6’s explicit requirement to inspect every `.exe` and `.dll` in Debug and Release to Release executables alone. A Debug-only `/MDd` dependency or a prohibited import in a DLL escapes check-all and the CI job that repeats its stages. The two sections specify different acceptance boundaries.

### integration: needs-attention

6. P1 `todo/00-workspace/TODO-05-native-spine.md:104`: The checkpoint runs bare `cmake --workflow --preset ...`, but §3 creates the presets under `native/`. The existing check-all explicitly works from the repository root, and neither dev-env nor these commands establishes `native/` as the working directory. Following the commands there fails to find the presets. The runner needs an explicit directory convention or root preset entry point. [CMake preset lookup](https://cmake.org/cmake/help/v4.3/manual/cmake.1.html#run-a-workflow-preset).
7. P1 `todo/00-workspace/TODO-04-native-code-policy.md:70`: This wires the installed-tree lint into both workflows without providing its configure/install prerequisite. Its section depends only on `D00 T05 §4`; native CI setup arrives in §8. At this boundary, `build.yml` builds only .NET, while `plan.yml` runs its Python gates on Ubuntu without the Windows installed tree. A fresh workflow checkout cannot satisfy the live lint as specified. Separate portable self-tests from live inventory checks and supply the latter’s prerequisites.

### source-defect: needs-attention

8. P1 `todo/00-workspace/TODO-05-native-spine.md:98`: The Ninja presets never explicitly set `CMAKE_BUILD_TYPE` for Debug and Release. Preset names and matching build presets do not select configurations for single-configuration Ninja. Both named workflows can build the same default configuration and pass the checkpoint without proving Debug plus Release. Require the cache values and verify the resulting configuration. [CMake build types](https://cmake.org/cmake/help/v4.3/variable/CMAKE_BUILD_TYPE.html).
9. P1 `todo/00-workspace/TODO-05-native-spine.md:84`: Naming the overlay path `native/triplets/` inside `native/vcpkg-configuration.json` resolves to `native/native/triplets/`. The manual install command can conceal this through its separate command-line overlay, leaving the committed configuration broken. Configuration-relative spelling must be `triplets/`. [vcpkg path resolution](https://learn.microsoft.com/en-us/vcpkg/reference/vcpkg-configuration-json#overlay-triplets).
10. P2 `todo/00-workspace/TODO-04-native-code-policy.md:65`: The proposed `vcpkg list --x-json` alternative points at `artifacts/vcpkg_installed/<triplet>` as the installed root. The shared database belongs at `artifacts/vcpkg_installed/vcpkg/status`, beside the triplet directories. Pointing list at a triplet directory queries a different, empty database and produces false orphan findings. Query the common installation root and filter its triplet records. [vcpkg installed-tree layout](https://github.com/microsoft/vcpkg-tool/blob/main/include/vcpkg/installedpaths.h).

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 2

Every finding was verified against the repository or the cited documentation and is real.

1. P1, the standard check accepted a conflicting later switch: verified (MSVC D9025, the last switch wins). `native-std-check.py` requires exactly one `/std:` switch, the pinned one, with a duplicated-switch fixture.
2. P1, the size budget was enforced only with a flag: verified. `--publish` reads the budget from `native/size-budget.json` by default, check-all's `native artifacts` stage runs it over every named app's publish folder, and the self-test has an oversized folder failing with no flag.
3. P1, the fuzzed library was not instrumented: verified against libFuzzer's requirements. `isotone_add_fuzz_target` builds every library it names with coverage and AddressSanitizer, and the qualification parser lives in its own library whose compile lines must show the options.
4. P2, OSV pagination: verified. The job follows `next_page_token` to the end, a failed page counts as `unchecked`, and fixtures cover both.
5. P1, check-all narrowed the import check to Release executables: verified. The stage covers every `.exe` and `.dll` in all four build folders, as §6 says.
6. P1, presets live in `native/` but commands ran from the root: verified. §3 fixes the convention: every native command runs inside dev-env with `native/` as its working directory.
7. P1, the live dependency lint was wired before its installed tree existed: verified. `D00 T04 §1` now depends on `D00 T05 §7`; its self-test goes to the portable gates, the live lint to check-all after the native configure, and `D00 T05 §8` (now depending on `D00 T04 §1`) adds it to CI's native job.
8. P1, Ninja presets never set the build type: verified. Each configure preset sets `CMAKE_BUILD_TYPE`, checked in `CMakeCache.txt`.
9. P1, the overlay path in `vcpkg-configuration.json` resolves relative to the file: verified. It is `triplets`, and a configure without a command-line overlay must find the triplets.
10. P2, `vcpkg list` pointed at a triplet folder: verified. The lint reads the common root's database and filters by triplet.

## Round 3: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T00:05:59Z
- Effort: xhigh
- Lines: 23
- Digest: 84bd1e2bf39f76be

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-05-native-spine.md:100`: The standard checker specifies `/std:` switches, but CMake actually emits `-std:c++latest`. A command containing `/std:c++23preview -std:c++latest` satisfies the prescribed slash-only check while selecting the forbidden standard. Verified with the installed compiler using `/Zs /W4 /WX`: D9025, exit 0. Normalize both switch prefixes and test the spelling CMake generates. [CMake implementation](https://github.com/Kitware/CMake/blob/v4.3.1/Modules/Compiler/MSVC-CXX.cmake#L40-L43).
2. P1 `todo/00-workspace/TODO-04-native-code-policy.md:94`: Advisory identities are not checked against the installed source version. Demonstration: register installed libwebp 1.3.1 with Version `1.3.1`, but Released tag and advisory identity pointing to `v1.3.2`. The prescribed dependency lint accepts the matching Version; the advisory checker queries the patched tag and can miss CVE-2023-4863. The existing fixture supplies a correct identity and cannot expose this mismatch. Derive or validate the advisory identity against the resolved port source. [OSV queries use the supplied tag](https://google.github.io/osv.dev/post-v1-query/#queries-for-git-records).

### consistency: needs-attention

3. P1 `todo/00-workspace/TODO-05-native-spine.md:146`: ARM64 sanitizer execution disappears from the integration contract. Section 5 conditionally creates `arm64-asan`, but check-all lists only `native x64-asan`, and section 8 transfers only ARM64 Debug and Release executables. All prescribed checkpoints can pass without executing ARM64 sanitized tests, contrary to the spec’s requirement at line 118. This affects the stated toolchain: Microsoft documents ARM64 ASan support in Visual Studio 2026. Add its build, runtime transfer, execution, and negative probe to the ARM64 path. [Microsoft announcement](https://devblogs.microsoft.com/cppblog/introducing-msvc-addresssanitizer-for-arm64-targets/).
4. P2 `todo/00-workspace/TODO-04-native-code-policy.md:94`: The scheduled dependency job implements advisory queries but omits the vcpkg baseline check required by the spec’s “Dependencies and their upkeep”. Changing the committed baseline while leaving register versions unchanged is invisible to this job because it neither resolves that baseline nor compares its versions. Add the comparison and a baseline/register mismatch fixture.
5. P2 `todo/00-workspace/TODO-04-native-code-policy.md:83`: The first benchmark section never identifies or commits the document fixtures required by the spec at line 31: small, typical, and large documents per app, with the large ones at documented limits. Every checklist item and checkpoint here can pass with only the generated premultiply tile. Add the document fixture paths, limits, and existence verification, or explicitly assign an approved successor.

### integration: needs-attention

6. P1 `todo/00-workspace/TODO-05-native-spine.md:83`: The literal install command conflicts with section 3’s working-directory convention at line 94. Inside dev-env’s default `native/` directory, `--x-manifest-root=native` resolves to `native/native`, while `--x-install-root=artifacts/vcpkg_installed` places output under `native/artifacts`. The manifest lookup fails and the installation destination violates this item’s own requirement. Specify repository-root `-WorkingDirectory` for this command or correct its paths for execution from `native/`.

### source-defect: needs-attention

7. P1 `todo/00-workspace/TODO-05-native-spine.md:98`: All presets share one manifest installation root, but manifest installs synchronize that entire root rather than accumulate independent triplets. Demonstration: configure x64, then ARM64, then ASan against that root; each subsequent installation removes packages outside its current plan, leaving earlier build folders pointing at removed dependencies. Release-only `bench` selection adds another incompatible installation state. Isolate installation roots by configuration requirements and aggregate their inventories explicitly. The pinned vcpkg implementation removes installed packages whose ABIs are absent from the new plan. [Manifest-mode behavior](https://learn.microsoft.com/en-us/vcpkg/commands/install#manifest-mode), [pinned removal logic](https://github.com/microsoft/vcpkg-tool/blob/98d7cb0cf1f4686a3e43aa5672b6230c1d56bce8/src/vcpkg/commands.set-installed.cpp#L127-L150).

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 3

Every finding was verified against the repository or the cited documentation and is real.

1. P1, CMake emits `-std:`, which a slash-only check misses: verified against CMake's MSVC module. `native-std-check.py` reads both spellings, with a `/std:c++23preview -std:c++latest` fixture.
2. P1, an advisory identity could name a different tag than the installed source: verified. `native-deps-lint` gains `identity-mismatch`, comparing the register's repository and tag with the installed port's `vcpkg.spdx.json`, with a libwebp 1.3.1 row naming `v1.3.2` as its fixture.
3. P1, ARM64 sanitized tests were never run: verified (Microsoft announced AddressSanitizer for ARM64 with Visual Studio 2026). For every architecture §5 finds supported, the lane is required: `arm64-asan` is built in check-all and CI, and its tests, its probe, and the ARM64 runtime run on ARM64.
4. P2, the scheduled job omitted the baseline check: verified against the spec. §3 adds `baseline-mismatch` against the committed baseline's `versions/baseline.json`, and reports newer fixing versions in the current registry.
5. P2, the per-app fixture documents had no owner: verified. They need each app's document format, so the spec is amended to place them in each app's first performance section; the re-plan records the requirement for waves 3, 5, and 6, and `docs/benchmarks/README.md` will name the path.
6. P1, the manual install command's paths assumed the root while dev-env defaults to `native/`: verified. The command runs with `-WorkingDirectory .` and its own install root.
7. P1, a shared manifest install root removes other presets' packages: verified against vcpkg's manifest-mode install. Each preset has its own installed root, the lint aggregates them, and the checkpoint shows the x64 root intact after an ARM64 install.

## Round 4: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T00:19:47Z
- Effort: xhigh
- Lines: 22
- Digest: b01ef3985500cd40

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-04-native-code-policy.md:65`: `test-only-shipped` checks feature placement, not which executable links the library. An app can link `GTest::gtest` while GoogleTest remains in the `test` feature with `Linked by: tests`; every prescribed dependency rule still passes. Require verification of the app’s dependency closure and a negative fixture for this case.
2. P1 `todo/00-workspace/TODO-04-native-code-policy.md:86`: No required execution covers the NEON correctness guard. The smoke stage runs locally on x64, while the ARM64 job transfers test executables, not `isotone_benchmarks`. Change NEON’s rounding: the x64 smoke checkpoint and prescribed ARM64 tests can remain green. Add ARM64 smoke execution and its failing mutation probe.

### consistency: approve

### integration: needs-attention

3. P1 `todo/00-workspace/TODO-05-native-spine.md:158`: Running transferred executables with only `--gtest_output=xml` does not preserve the CTest contract. Section 9 adds replay tests requiring committed corpus and regression files, but neither those files nor their CTest arguments and working directories are transferred. Demonstrate this with a replay test whose corpus directory is supplied through `add_test`: the ARM64 invocation cannot reproduce it. Require a portable test package that preserves these inputs and invocation metadata. [CTest invocation options](https://cmake.org/cmake/help/latest/module/GoogleTest.html).

### source-defect: needs-attention

4. P1 `todo/00-workspace/TODO-05-native-spine.md:96`: Applying the explicit standard switch through the prescribed helpers does not tell CMake that targets use C++23. GoogleTest exports `cxx_std_17`; CMake can therefore add `-std:c++17` to the consuming test target alongside `/std:c++23preview`, making the normal skeleton fail §3’s exactly-one-switch checker. Generate the prescribed GoogleTest consumer and inspect its compile database. Specify how CMake’s feature negotiation and the pinned switch are reconciled. [GoogleTest requirement](https://github.com/google/googletest/blob/v1.18.0/googletest/cmake/internal_utils.cmake#L205), [CMake feature propagation](https://cmake.org/cmake/help/latest/manual/cmake-compile-features.7.html).
5. P2 `todo/00-workspace/TODO-04-native-code-policy.md:65`: The new provenance comparison lacks a rule for registry-owned helper ports. GoogleTest necessarily installs `vcpkg-cmake` and `vcpkg-cmake-config`; these contain registry scripts rather than separately downloaded upstream releases. Their provenance cannot satisfy the required upstream released-tag comparison as written. Define their registry provenance and advisory mapping, with fixtures, instead of leaving the runner to invent an exception. [GoogleTest dependencies](https://github.com/microsoft/vcpkg/blob/master/ports/gtest/vcpkg.json), [helper recipe](https://github.com/microsoft/vcpkg/blob/master/ports/vcpkg-cmake/portfile.cmake).
6. P2 `todo/00-workspace/TODO-05-native-spine.md:84`: Specifying both the manifest’s `builtin-baseline` and the configuration’s `default-registry` produces a warning and makes the manifest baseline ineffective. This contradicts §3’s warning-free configure requirement; it also makes T04 §3’s advisory job read a field that does not control installation. The pinned vcpkg implementation explicitly warns and retains the configured registry. Choose one authoritative baseline and make the advisory check read it. [Pinned selection logic](https://github.com/microsoft/vcpkg-tool/blob/98d7cb0cf1f4686a3e43aa5672b6230c1d56bce8/src/vcpkg/vcpkgpaths.cpp#L170-L194).

### record: approve

HIGHEST: P1

OVERALL: needs-attention

## Response to round 4

Every finding was verified against the repository or the cited documentation and is real.

1. P1, a test-only library linked by an app escaped the feature check: verified. `native-deps-lint` gains `test-only-linked`, reading the `x64-release` link graph from `cmake --graphviz`, with a fixture of an app linking `GTest::gtest`.
2. P1, the NEON guard never ran on ARM64: verified. `D00 T04 §2` runs the benchmark smoke in the ARM64 CI job, with a failing NEON probe on a dispatched branch.
3. P1, transferred executables lost CTest's arguments, working directories, and inputs: verified. The ARM64 job restores whole build folders into the same workspace path GitHub's Windows runners share, beside a checkout of the same commit, checks the recorded path, and runs `ctest --test-dir` with the image's CTest.
4. P1, GoogleTest's `cxx_std_17` would add a second standard switch: verified against CMake's compile-feature propagation. The build uses `CMAKE_CXX_STANDARD 23` with `CMAKE_CXX23_STANDARD_COMPILE_OPTION` set to the pinned switch, so feature negotiation is satisfied by the one switch; the standard check proves it on the GoogleTest consumer.
5. P2, registry helper ports have no upstream release: verified. The register carries them as build-time helpers with `microsoft/vcpkg` at the baseline commit and no advisory identity, checked exactly, with fixtures.
6. P2, `builtin-baseline` and `default-registry` together make the manifest baseline ineffective: verified against the pinned vcpkg tool. `vcpkg-configuration.json` holds only the overlay triplets, and the configure must show no baseline warning.

## Round 5: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:04:47Z
- Effort: xhigh
- Lines: 28
- Digest: dc28074ed9b2fc0a

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-05-native-spine.md:98`: The x64 test presets lack an empty-suite failure policy. Suppress test registration for x64 Debug and Release while retaining the executable builds and ARM64 registration: ordinary CTest can return success with no tests, leaving these check-all stages green. Require `execution.noTestsAction: "error"` and an empty-suite negative probe. [CTest behavior](https://cmake.org/cmake/help/v4.3/manual/ctest.1.html#cmdoption-ctest-no-tests).

### consistency: needs-attention

2. P1 `todo/00-workspace/TODO-04-native-code-policy.md:95`: Round 4 introduces mandatory helper rows with Advisory identity `none: build-time helper, not linked`, but §3 still requires an OSV or feed query for every row and rejects missing identities. GoogleTest’s helper rows therefore cannot satisfy the real-register checkpoint as written. Carry the validated helper exemption into the advisory algorithm and its fixtures.
3. P1 `todo/00-workspace/TODO-06-retire-csharp.md:97`: The checkpoint requires no active-stack references outside history and parked TODOs, but line 16 explicitly leaves standards and developer-document rewrites to `D00 T07 §2`, which depends transitively on this section. Following those ownership assignments leaves references in `standards/` and `docs/dev/build.md`, making this checkpoint impossible before its dependent work runs.
4. P2 `todo/00-workspace/TODO-07-native-replan.md:114`: The checkpoint demands empty stack-grep output over every owned file, while §2 owns developer documentation containing preserved decision history. Line 107 permits history matches, but the checkpoint does not. Running the prescribed expression against `docs/dev/decisions.md` demonstrates the contradiction. Apply the history exception consistently.
5. P2 `todo/00-workspace/TODO-07-native-replan.md:675`: The last re-plan section omits the terminal `groom-plan` sweep and whole-tree plan review required by the governing plan’s Acceptance section. Every listed checkpoint can pass without that final review returning no P1 or P2. Assign both requirements an explicit step and checkpoint.

### integration: needs-attention

6. P1 `todo/00-workspace/TODO-06-retire-csharp.md:62`: Deleting `src/` precedes the gate repairs assigned to §3. Evaluating the unchanged design baseline against the removed sources produces 1,479 stale entries covering 2,046 findings, so the commit hook refuses §1; parked source claims also fail check-all until §3. Removing `global.json` additionally breaks the still-scheduled .NET pin jobs until §2. These dependent changes must share the removal boundary to keep the campaign running.
7. P1 `todo/00-workspace/TODO-06-retire-csharp.md:88`: Excluding blocked and superseded files from coverage leaves five Current state blocks against the existing absolute `COVERAGE_FLOOR = 78`. The specified filtering therefore fails even with every eligible block covered, and the governing rules forbid simply lowering the floor to pass. Define the coverage migration and test it against the actual parked-tree shape.
8. P1 `todo/00-workspace/TODO-04-native-code-policy.md:54`: Round 4 adds a mandatory ARM64 CI smoke run and failing NEON probe to §2, but its dependencies still stop at `D00 T05 §7`. After those prerequisites ship, §2 is graph-ready while the required ARM64 job from `D00 T05 §8` may not exist. Add §8 as a prerequisite.
9. P2 `todo/00-workspace/TODO-06-retire-csharp.md:77`: The cleanup never assigns removal of the SDK branch in `scripts/check-local-tools.py`. That retained script unconditionally reads `global.json`; a read-only simulation of its removal raises `Unreadable`. The mixed CLI/Python/SDK task must be retargeted explicitly, with its SDK fixtures updated, rather than only changing automation descriptions or deleting whole tasks.

### source-defect: needs-attention

10. P2 `todo/00-workspace/TODO-05-native-spine.md:98`: The preset still sets `VCPKG_OVERLAY_TRIPLETS` to `native/triplets`, although commands run from `native/`. This command-line overlay resolves to `<repo>/native/native/triplets`. The corrected configuration-file overlay can conceal the invalid preset value, so existing successful-install checkpoints do not prove it works. Use `${sourceDir}/triplets` or remove the duplicate override. [CMake integration](https://learn.microsoft.com/en-us/vcpkg/users/buildsystems/cmake-integration#vcpkg_overlay_triplets), [pinned path resolution](https://github.com/microsoft/vcpkg-tool/blob/98d7cb0cf1f4686a3e43aa5672b6230c1d56bce8/src/vcpkg/vcpkgpaths.cpp#L92-L130).

### record: needs-attention

11. P2 `todo/00-workspace/TODO-06-retire-csharp.md:68`: The required readback names `csharp-final:src/Stilus/Bezier.sln`, but that file is absent from the candidate. `git ls-files '*.sln' '*.slnx'` lists only `Isotone.slnx`, and no preceding spine section creates the named solution. Tagging the prescribed HEAD cannot make this checkpoint pass. Read back an existing tracked reference file.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 5

This record's round 5 covers `D00 T05` and `D00 T04` after round 4, and the new `D00 T06` and `D00 T07`. Every finding was verified against the files, the repository, or the cited documentation and is real.

1. P1, an empty test suite passes CTest: verified. Every test preset sets `execution.noTestsAction` to `error`, with a probe that registers no test and must fail.
2. P1, helper rows would fail the advisory job as unmapped: verified. A validated helper row with the exact `none: build-time helper, not linked` identity is reported `helper` and not queried; a non-helper row with that identity stays `unmapped`; fixtures cover both.
3. P1, `D00 T06`'s grep would hit the standards and developer docs `D00 T07 §2` rewrites later: verified. The Outcome and checkpoint exclude `standards/` and `docs/dev/`, which `D00 T07 §2` owns.
4. P2, the re-plan checkpoint forbade the history lines its item allows: verified. Every `D00 T07` checkpoint now accepts lines that name the C# code as history and requires them to be listed.
5. P2, the final groom and whole-tree plan review had no owner: verified. The last re-plan section runs `groom-plan` over the whole tree and a whole-tree plan review to a round with no P1 or P2.
6. P1, deleting `src/` first would make the commit hook, the claims gate, and the .NET pin jobs fail before their repairs: verified (1,479 stale baseline entries). `D00 T06` is reordered so every commit stays green: §1 retargets design-lint with an empty baseline and defers parked claims while the sources exist, §2 retires the .NET automations while `global.json` exists, and §3 tags and deletes last.
7. P1, excluding parked files from coverage would break the absolute floor: verified (`COVERAGE_FLOOR = 78`). Deferred claims are not re-measured but still count toward coverage, so the floor holds unchanged; self-test cases and mutants cover both halves.
8. P1, the benchmark section needs the ARM64 CI job: verified. `D00 T04 §2` now depends on `D00 T05 §8`.
9. P2, `check-local-tools.py` reads `global.json` unconditionally: verified. `D00 T06 §2` removes its SDK branch with fixtures and proves it on a tree without `global.json`.
10. P2, the preset's overlay path resolved against `native/`: verified. The preset sets no `VCPKG_OVERLAY_TRIPLETS`; the configuration file's relative overlay is the one source.
11. P2, the readback named a solution that does not exist: verified. It reads `csharp-final:src/Stilus/Bezier.Core/Bezier.Core.csproj`, which is tracked and claimed.

## Round 6: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:18:41Z
- Effort: xhigh
- Lines: 26
- Digest: c0153b649bd72af8

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-06-retire-csharp.md:63`: Retargeting design-lint while keeping its existing rules creates a gate that passes native token violations. An in-memory probe using the current scanner returned zero findings for literal `D2D1::ColorF` colors and `D2D1::RectF` geometry. Native rules arrive only in T07 §5, after §3’s UI foundations. Require native rules and failing literal probes before those foundations run.

### consistency: needs-attention

2. P1 `todo/00-workspace/TODO-06-retire-csharp.md:100`: The repository-wide empty-grep checkpoint still matches the retirement TODO itself. T06 is neither parked nor among the excluded history paths; its instructions contain `dotnet`, `nuget`, `xaml`, and other prohibited terms. Running the specified pattern against this file demonstrates the contradiction. Define an executable-content scope or explicitly permit recorded migration instructions.

3. P2 `todo/00-workspace/TODO-07-native-replan.md:670`: The final groom requires every parked file to be unparked, and the following whole-tree review requires Acceptance to hold, but this section unparks its last owned file only at line 672. Executing the checklist in order reaches both audits with `TODO-12-isotone-local-ml.md` still parked. Move the final audits after its rewrite, map update, and validation.

### integration: needs-attention

4. P1 `todo/00-workspace/TODO-07-native-replan.md:138`: Unparking rewritten files is not coupled to a dependency on their owning re-plan section’s verification. If §4’s review is parked after its implementation commit, rewritten work can run before that plan is approved. An in-memory graph check showed D01 T02 §1 has no unmet dependencies once its earlier prerequisites complete, while T07 §4 remains unchecked. Require dependency edges from the rewritten entry rows to their re-plan owner.

5. P1 `todo/00-workspace/TODO-06-retire-csharp.md:73`: This removes both existing `pins.yml` jobs while retaining the native advisory job only “if that section has landed.” T06 does not depend on T04 §3. Park that advisory section during review and continue with otherwise-ready retirement work: the prescribed edit leaves a workflow with no jobs, making its required successful dispatch impossible. Require the replacement job first or provide an explicit valid retirement path.

### source-defect: needs-attention

6. P2 `todo/00-workspace/TODO-05-native-spine.md:71`: The required component list omits `Microsoft.VisualStudio.Component.VC.CMake.Project`, although the environment requires Visual Studio’s bundled CMake and Ninja. Installing only the declared components can therefore leave `-Check` failing without provisioning identifying the missing CMake component. Include it in the pin and prerequisite checks. [Microsoft’s component catalog](https://learn.microsoft.com/en-us/visualstudio/install/workload-component-id-vs-community?view=vs-2026).

7. P2 `todo/00-workspace/TODO-05-native-spine.md:86`: The triplets pin MSVC but do not carry or verify the Windows SDK pin inside dependency builds. vcpkg constructs an isolated environment and invokes its own `vcvarsall`; checking the parent shell’s SDK does not establish the SDK used there. With an older pinned SDK and a newer installed SDK, inspect dependency include/library paths: this can drift while `dev-env -Check` passes. Require SDK selection and readback inside that build environment. [vcpkg environment rules](https://learn.microsoft.com/en-us/vcpkg/users/triplets#vcpkg_env_passthrough), [pinned tool implementation](https://github.com/microsoft/vcpkg-tool/blob/98d7cb0cf1f4686a3e43aa5672b6230c1d56bce8/src/vcpkg/commands.build.cpp#L653-L676).

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 6

Every finding was verified against the files, the scripts, or the cited documentation and is real.

1. P1, design-lint retargeted without C++ rules would pass native literals: verified (the current scanner finds nothing in `D2D1::ColorF` or `D2D1::RectF`). `D00 T06 §1` now adds the C++ rules (literal colors, geometry, and fonts in UI sources, with token reads passing) and failing probes, before any foundation draws; the UI toolkit's re-plan adds only what the components need beyond them.
2. P1, the repository-wide grep matched `D00 T06` itself: verified. The Outcome and checkpoint exclude `todo/`, whose files are parked or name the retired stack only as migration instructions; the command states its exclusions as pathspecs.
3. P2, the final audits ran before the last file was unparked: verified. The last re-plan section rewrites, maps, edges, and validates its file first, then runs `groom-plan` and the whole-tree review.
4. P1, rewritten rows could run before their re-plan section was stamped: verified. Each re-plan section adds itself to the Depends On of every entry section of the files it rewrites, so `resolve` exits 4 on them until it is stamped, even when its review is parked.
5. P1, retiring the .NET pins jobs could leave `pins.yml` with no jobs: verified. `D00 T06 §2` now depends on `D00 T04 §3`, so the native advisory job exists first.
6. P2, the CMake component was missing from the pin: verified against Microsoft's component catalog. `Microsoft.VisualStudio.Component.VC.CMake.Project` is in the required components.
7. P2, vcpkg's dependency builds can take a different Windows SDK: verified (vcpkg runs its own `vcvarsall`). `dev-env -Check` fails when an SDK newer than the pin is installed, so the pin is the newest on every build machine, and the §2 checkpoint reads the SDK version in the dependency builds' include and library paths.

## Round 7: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:36:38Z
- Effort: xhigh
- Lines: 24
- Digest: 7e83a281d92f2712

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-07-native-replan.md:97`: Gating only sections without internal dependencies leaves open successors of stamped sections unguarded. Applying this rule in memory leaves `D00 T01 §5`, `§7`, `§9`, and `§10` resolving with exit 0 while `D00 T07 §1` remains unstamped. Their stamped prerequisites do not propagate the new dependency. Gate the open entry points without changing stamped sections.
2. P2 `todo/00-workspace/TODO-05-native-spine.md:72`: The environment check omits `clang-cl`, although line 71 explicitly pins it and §9 uses it for fallback fuzzing. Selecting a different `clang-cl` while retaining matching `clang-tidy` and `clang-format` passes the prescribed comparisons. Require its version check and a mismatch fixture.

### consistency: needs-attention

3. P1 `todo/00-workspace/TODO-07-native-replan.md:151`: The checkpoint requires rewritten work in `query ready` before its owner can be stamped, while line 147 requires that work to remain blocked until that stamp. An in-memory `D01 T02 §1` check returns 4 before the owner’s stamp and 0 afterward. This repeated checkpoint needs separate pre-stamp and post-stamp expectations.
4. P2 `todo/00-workspace/TODO-07-native-replan.md:717`: Requiring the plan document’s entire Acceptance to hold makes the final audit impossible. Its line 51 still requires `query ready` to start with the native spine, which will already be completed by Phase 44. Replace that initial-state condition with a completion-state condition.

### integration: needs-attention

5. P2 `todo/00-workspace/TODO-06-retire-csharp.md:95`: This consumes the proof standard from `D00 T05 §10` without depending on it. With §9 and §10 unfinished and the other prerequisites completed, `D00 T06 §3` resolves with exit 0. A parked fuzzing review can therefore let retirement switch the authoring skills before their canonical proof migration lands. Add the prerequisite edge.

### source-defect: needs-attention

6. P2 `todo/00-workspace/TODO-05-native-spine.md:71`: The pin conflates the compiler’s reported version with the toolset selector passed to `-vcvars_ver` and vcpkg. Here, `cl` reports `19.51.36260`, while its toolset directory is `14.51.36231`. Microsoft requires `-vcvars_ver` to match the toolset directory version. Record the selector and expected compiler version separately. [Microsoft’s selection rules](https://learn.microsoft.com/en-us/cpp/overview/acquire-msvc?view=msvc-170#visual-studio-command-prompt).

### record: needs-attention

7. P3 `todo/00-workspace/TODO-05-native-spine.md:16`: The Current state records 19 Python gates, but `scripts/check-all.ps1` contains 20 `Invoke-PythonGate` invocations. Counting those calls reproduces the discrepancy.

HIGHEST: P1
OVERALL: needs-attention

## Response to round 7

Every finding was verified against the files, the machine, or the cited documentation and is real.

1. P1, gating only internal entry sections left open successors of stamped sections unguarded: verified (`D00 T01 §5`, `§7`, `§9`, `§10`). The edge now goes on every open section whose Depends On names no other open section of its own file, stamped sections untouched.
2. P2, `clang-cl` was pinned but never checked: verified. `dev-env -Check` reads its version, with a mismatch fixture.
3. P1, the re-plan checkpoint required a row to be ready before the stamp that unblocks it: verified. Before the stamp, `resolve` on each open entry point must exit 4 naming the section; the stamp step re-runs it afterwards.
4. P2, the final audit required an initial-state condition: verified. The plan document's Acceptance now states completion conditions (no parked file, no pending map row, every listed ready row native), and the final audit checks those.
5. P2, the C# removal consumed the C++ proof standard without depending on it: verified. `D00 T06 §3` depends on `D00 T05 §10`.
6. P2, the pin conflated the toolset selector with the compiler version: verified on this machine (`cl.exe` in toolset folder 14.51.36231 reports 19.51.36260). `native/toolchain.json` records the selector, which `-vcvars_ver` and the triplets take, and the compiler version `cl` prints, and `dev-env` checks each against its own source.
7. P3, the Python gate count was 19: verified (20 since `ci_watch.py` joined). Corrected.

## Round 8: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T01:53:05Z
- Effort: xhigh
- Lines: 22
- Digest: 4c251485c9e0d1ac

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-04-native-code-policy.md:65`: `test-only-linked` inspects only the `x64-release` link graph. An ARM64-only link from an app to `GTest::gtest` leaves that graph unchanged; registration, feature placement, and system-import checks still accept it. Require link-closure checks and negative fixtures for both architectures.

### consistency: needs-attention

2. P1 `todo/00-workspace/TODO-07-native-replan.md:122`: Phase 1 must build menu-bar and docking foundations, but §4 leaves their layout maps in Phase 2 and the conformance helpers in Phase 3. Requirement 4 of the re-plan demands maps and conformance tests for every such surface. Following both instructions requires later-phase prerequisites. Move the necessary map work earlier or explicitly define the foundation test-host exemption.

### integration: needs-attention

3. P2 `todo/00-workspace/TODO-06-retire-csharp.md:97`: Retirement leaves the tracked `tests/Isotone.runsettings` behind. Neither §3’s deletion list, the `managed-source` extensions, nor the final filename scan includes `.runsettings`. All prescribed checks can therefore pass with .NET test configuration remaining, contradicting the Goal. Remove it and cover its reintroduction.

4. P2 `todo/00-workspace/TODO-06-retire-csharp.md:75`: The required `python scripts/check-local-tools.py` invocation lacks its mandatory mode. Running it returns exit 2: “the following arguments are required: mode”. Removing the SDK branch does not change that parser contract. Specify `check` in this item and its checkpoint.

### source-defect: needs-attention

5. P2 `todo/00-workspace/TODO-05-native-spine.md:159`: The ARM64 command ends with `--output-junit` without its required filename, leaving the promised report invocation incomplete. Specify a distinct report path per configuration and upload those paths. [CTest’s documented syntax](https://cmake.org/cmake/help/latest/manual/ctest.1.html#cmdoption-ctest-output-junit) is `--output-junit <file>`.

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 8

Every finding was verified against the files and the cited documentation and is real.

1. P1, the test-only link check read only the x64 graph: verified. `test-only-linked` reads both the `x64-release` and `arm64-release` link graphs, with fixtures failing on an x64-only and an ARM64-only link.
2. P1, the Phase 1 foundations would need layout maps that come later: verified. The re-plan rules now scope requirement 4 to product sections (app sections, and Isotone UI controls and docking as an app uses them); the foundations prove their mechanisms in a test host with placeholder menus and panels and cite no map, as `D00 T07 §3` now says.
3. P2, `tests/Isotone.runsettings` survived the removal: verified (the only .NET-only file outside `src/` and the root .NET files). It is in the deletion list and the Outcome's `git ls-files` check, and `managed-source` also refuses `.runsettings`, `.ruleset`, `.nuspec`, and `packages.lock.json`.
4. P2, `check-local-tools.py` needs its mode: verified (`mode` is required). The item and checkpoint run `check-local-tools.py check`.
5. P2, `--output-junit` needs a file: verified against CTest. Each configuration writes `<folder>/junit-<configuration>.xml`.

## Round 9: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T05:51:02Z
- Effort: xhigh
- Lines: 20
- Digest: 8c12a16f8ce2b5e1

### adversarial: needs-attention

1. P1 `todo/00-workspace/TODO-07-native-replan.md:127`: The stamp dependency covers files this section “re-plans”, but §3 also authors new foundation files. Its checkpoint likewise checks only rewritten files. Park §3’s review after committing a new foundation: that foundation can run before its authoring section is approved. An in-memory check of `unmet_dependencies` confirmed this; explicitly adding `D00 T07 §3` blocks it.

### consistency: needs-attention

2. P1 `docs/plans/2026-10-23-native-replan.md:45`: “A section with genuinely nothing to exceed says why” exempts feature sections from the mandatory improvement required by `AGENTS.md:51` and `docs/dev/decisions.md:77`. A feature can declare that matching its competitor is sufficient and supply no improvement checkpoint. Completion review item 11 checks what was promised, so this exemption defeats enforcement. Restrict exemptions to non-feature work.

### integration: needs-attention

3. P2 `todo/00-workspace/TODO-06-retire-csharp.md:101`: The final repository scan includes active `docs/design/` instructions, but their conversion has no assigned step. For example, `components/Canvas/README.md:30` requires SkiaSharp and WPF, `components/Panel/README.md:30` requires AvalonDock, and `shell-layout.md:76` requires XAML. Following the listed retirement edits leaves this checkpoint failing; T07 §2 assigns only standards and developer documentation.

### source-defect: needs-attention

4. P2 `todo/00-workspace/TODO-05-native-spine.md:159`: Matching workspace paths does not make deferred GoogleTest discovery portable. The installed CMake module embeds an absolute `${CMAKE_ROOT}/Modules/GoogleTestAddTests.cmake` include. Transfer the build to ARM64 with the same workspace but a different CMake installation prefix: the workspace check passes, then discovery fails before running tests. The plan must cover the producer’s discovery-module dependency. [CMake implementation](https://github.com/Kitware/CMake/blob/master/Modules/GoogleTest.cmake).

### record: approve

HIGHEST: P1
OVERALL: needs-attention

## Response to round 9

Every finding was verified against the files and the cited documentation and is real.

1. P1, new foundation files were not gated on their authoring section: verified. `D00 T07 §3` now makes every open entry section of each new foundation file depend on it, and its Done when checks `resolve` exits 4 on them.
2. P1, the "nothing to exceed" exemption let a feature skip the improvement: verified. Every feature section must name an improvement; only non-feature work (tooling, infrastructure, documentation, release mechanics) carries no `**Exceed:**` paragraph and says so, in the re-plan rules and in `process-todo-section`.
3. P2, `docs/design/` still names WPF, XAML, SkiaSharp, and AvalonDock with no owner: verified (`components/Canvas/README.md`, `components/Panel/README.md`, `shell-layout.md`). `D00 T07 §2` rewrites the design-system implementation notes for the native toolkit with every token and value unchanged and regenerates the design page; `D00 T06`'s scan excludes `docs/design/` like the other paths that section owns.
4. P2, deferred test discovery embeds the producer's CMake path: verified against CMake's GoogleTest module. The ARM64 job reads `CMAKE_ROOT` and the CMake version from each restored cache and installs the pinned CMake at exactly that prefix when the image lacks it, failing when it cannot.

## Round 10: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T06:13:15Z
- Effort: xhigh
- Lines: 14
- Digest: c215b2b7831b8db0

### adversarial: needs-attention

1. P2 `todo/00-workspace/TODO-04-native-code-policy.md:65`: `test-only-linked` checks only the two Release graphs. Link an app to `GTest::gtest` inside `if(CMAKE_BUILD_TYPE STREQUAL "Debug")`: both inspected graphs remain unchanged, registration and feature-placement checks pass, and static linking introduces no prohibited DLL import. The required gate therefore accepts a forbidden app dependency in Debug. Check Debug and Release on both architectures, with a Debug-only negative fixture. [CMake configuration semantics](https://cmake.org/cmake/help/v4.3/variable/CMAKE_BUILD_TYPE.html).

### consistency: approve

### integration: approve

### source-defect: approve

### record: approve

HIGHEST: P2
OVERALL: needs-attention

## Response to round 10

The finding was verified and is real; the other four lenses approved.

1. P2, the test-only link check read only the Release graphs: verified (a link inside `if(CMAKE_BUILD_TYPE STREQUAL "Debug")` changes neither). `test-only-linked` reads the link graphs of all four configurations (`x64-debug`, `x64-release`, `arm64-debug`, `arm64-release`), with a Debug-only fixture failing beside the x64-only and ARM64-only ones.

## Round 11: sol (`gpt-6.1-sol` via `codex`)

- Writer: claude
- Run: 2026-10-23T06:36:26Z
- Effort: xhigh
- Lines: 14
- Digest: c6d4bda950a4a986

### adversarial: needs-attention

1. P2 `todo/00-workspace/TODO-06-retire-csharp.md:63`: The prescribed design-lint scan covers only `.h`, `.hpp`, and `.cpp`, leaving ordinary C++ extensions outside the gate. Demonstration: compile `native/ui/probe.cc` containing `D2D1::ColorF(D2D1::ColorF::Red)`. CMake accepts `.cc`, but the required scan omits it, so every prescribed negative probe can pass while this hardcoded color escapes detection. Cover all supported native source and header extensions, including included `.inl` files, and require a failing fixture outside `.cpp`. [CMake’s recognized extensions](https://github.com/Kitware/CMake/blob/v4.3.1/Modules/CMakeCXXCompiler.cmake.in#L48-L49).

### consistency: approve

### integration: approve

### source-defect: approve

### record: approve

HIGHEST: P2
OVERALL: needs-attention

## Response to round 11

The finding was verified and is real; the other four lenses approved.

1. P2, design-lint's native scan covered only `.h`, `.hpp`, and `.cpp`: verified against CMake's recognized C++ extensions. The scan covers every C and C++ source and header extension CMake compiles plus included implementation files (`.c`, `.cc`, `.cpp`, `.cxx`, `.c++`, `.h`, `.hh`, `.hpp`, `.hxx`, `.h++`, `.inl`, `.ipp`), and the probes now include a `.cc` and an `.inl` file.
