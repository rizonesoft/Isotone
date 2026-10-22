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
