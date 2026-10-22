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
