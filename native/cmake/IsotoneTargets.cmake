# The target helpers every native library and test goes through, so each one builds with the same flags
# (D00 T05 §3). Nothing adds a target with plain add_library or add_executable.
include_guard(GLOBAL)

# The target architecture, read from the compiler the environment entered (an ARM64 cross build runs on an x64 host,
# so CMAKE_HOST_SYSTEM_PROCESSOR is no guide).
if(CMAKE_CXX_COMPILER_ARCHITECTURE_ID STREQUAL "ARM64")
  set(ISOTONE_TARGET_ARCH arm64)
else()
  set(ISOTONE_TARGET_ARCH x64)
endif()

# The compiler environment is checked on every build, not only at configure: a build can run in another environment
# than the one that configured it.
add_custom_target(isotone_compiler_environment
  COMMAND "${CMAKE_COMMAND}" -P "${CMAKE_CURRENT_LIST_DIR}/CheckCompilerEnvironment.cmake"
  COMMENT "Checking the compiler environment"
  VERBATIM)

function(isotone_apply_flags target)
  add_dependencies(${target} isotone_compiler_environment)
  target_compile_options(${target} PRIVATE
    /W4 /WX /permissive- /utf-8 /Zc:__cplusplus /Zc:preprocessor /EHsc /external:anglebrackets /external:W0
    # Control-flow guard needs the compiler to emit the checks and the linker to set the image flag.
    /guard:cf)
  target_link_options(${target} PRIVATE /guard:cf $<$<CONFIG:Release>:/DEBUG:FULL /OPT:REF /OPT:ICF>)
  if(ISOTONE_TARGET_ARCH STREQUAL "x64")
    # Microsoft Learn documents CET shadow-stack compatibility for x64 only.
    target_link_options(${target} PRIVATE /CETCOMPAT)
  endif()
  if(ISOTONE_ANALYZE)
    # Code analysis of first-party code only: headers included with angle brackets are external (/external:anglebrackets),
    # and /analyze:external- skips them. /WX makes every analysis warning an error.
    target_compile_options(${target} PRIVATE /analyze /analyze:external-)
  endif()
  if(ISOTONE_SANITIZE STREQUAL "address")
    target_compile_options(${target} PRIVATE /fsanitize=address)
    # AddressSanitizer does not support incremental linking (Microsoft Learn, "AddressSanitizer"), which CMake's
    # RelWithDebInfo defaults turn on; the linker takes the last /INCREMENTAL option.
    target_link_options(${target} PRIVATE /INCREMENTAL:NO)
  elseif(NOT ISOTONE_SANITIZE STREQUAL "")
    message(FATAL_ERROR "ISOTONE_SANITIZE is '${ISOTONE_SANITIZE}': only empty or address is supported")
  endif()
  # Keep every linked image at least as new as build.ninja when CMake reconfigures an already-built tree without
  # source changes, so native-artifact-gate --require-built can verify every expected image belongs to the current graph.
  get_target_property(isotone_target_type ${target} TYPE)
  if(isotone_target_type STREQUAL "EXECUTABLE"
     OR isotone_target_type STREQUAL "SHARED_LIBRARY"
     OR isotone_target_type STREQUAL "MODULE_LIBRARY")
    set_property(TARGET ${target} APPEND PROPERTY LINK_DEPENDS "${CMAKE_BINARY_DIR}/build.ninja")
  endif()
endfunction()

# isotone_add_library(<name> <sources>... [PUBLIC_INCLUDE <dir>]): a static library with the suite's flags.
function(isotone_add_library name)
  cmake_parse_arguments(ARG "" "PUBLIC_INCLUDE" "" ${ARGN})
  add_library(${name} STATIC ${ARG_UNPARSED_ARGUMENTS})
  if(ARG_PUBLIC_INCLUDE)
    target_include_directories(${name} PUBLIC ${ARG_PUBLIC_INCLUDE})
  endif()
  set_property(TARGET ${name} PROPERTY ISOTONE_FIRST_PARTY_LIBRARY TRUE)
  set_property(TARGET ${name} PROPERTY ISOTONE_LIBRARY_SOURCES "${ARG_UNPARSED_ARGUMENTS}")
  set_property(TARGET ${name} PROPERTY ISOTONE_LIBRARY_PUBLIC_INCLUDE "${ARG_PUBLIC_INCLUDE}")
  isotone_apply_flags(${name})
endfunction()

# isotone_apply_fuzz_flags(<target> <LIBRARY|EXECUTABLE>): coverage and AddressSanitizer instrumentation for a fuzz
# executable or a static library in its first-party closure (D00 T05 §9).
function(isotone_apply_fuzz_flags target kind)
  if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(${target} PRIVATE /fsanitize=address /fsanitize=fuzzer)
    if(kind STREQUAL "EXECUTABLE")
      target_link_options(${target} PRIVATE /INCREMENTAL:NO)
    endif()
  elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
    if(kind STREQUAL "LIBRARY")
      target_compile_options(${target} PRIVATE -fsanitize=fuzzer-no-link,address)
    else()
      target_compile_options(${target} PRIVATE -fsanitize=fuzzer,address)
      target_link_options(${target} PRIVATE -fsanitize=fuzzer,address /INCREMENTAL:NO)
    endif()
  else()
    message(FATAL_ERROR "Unsupported compiler for fuzzing: ${CMAKE_CXX_COMPILER_ID}")
  endif()
endfunction()

# isotone_ensure_fuzz_library(<lib> <out_var>): walks the transitive LINK_LIBRARIES closure of a first-party static
# library (including targets wrapped in CMake generator expressions) and builds each in a `<lib>_fuzz` variant with
# coverage and AddressSanitizer instrumentation while preserving the library's compile, include, and link properties
# (D00-T05-S8-PR10).
function(isotone_ensure_fuzz_library lib out_var)
  if(NOT TARGET "${lib}")
    if("${lib}" MATCHES "\\$<")
      set(rewritten "${lib}")
      string(REGEX MATCHALL "[A-Za-z0-9_.-]+" candidate_tokens "${lib}")
      list(REMOVE_DUPLICATES candidate_tokens)
      foreach(tok IN LISTS candidate_tokens)
        if(TARGET "${tok}")
          isotone_ensure_fuzz_library("${tok}" mapped_tok)
          if(NOT "${mapped_tok}" STREQUAL "${tok}")
            string(REGEX REPLACE "([.+*?^$()\\[\\]{}|\\\\])" "\\\\\\1" tok_escaped "${tok}")
            string(
              REGEX REPLACE
              "(^|[^A-Za-z0-9_.-])${tok_escaped}($|[^A-Za-z0-9_.-])"
              "\\1${mapped_tok}\\2"
              rewritten
              "${rewritten}")
            string(
              REGEX REPLACE
              "(^|[^A-Za-z0-9_.-])${tok_escaped}($|[^A-Za-z0-9_.-])"
              "\\1${mapped_tok}\\2"
              rewritten
              "${rewritten}")
          endif()
        endif()
      endforeach()
      set(${out_var} "${rewritten}" PARENT_SCOPE)
      return()
    endif()
    set(${out_var} "${lib}" PARENT_SCOPE)
    return()
  endif()
  get_target_property(aliased "${lib}" ALIASED_TARGET)
  if(aliased)
    set(lib "${aliased}")
  endif()
  get_target_property(is_first_party "${lib}" ISOTONE_FIRST_PARTY_LIBRARY)
  if(NOT is_first_party)
    set(${out_var} "${lib}" PARENT_SCOPE)
    return()
  endif()

  set(fuzz_lib "${lib}_fuzz")
  if(NOT TARGET "${fuzz_lib}")
    set(mapped_link_libs "")
    get_target_property(link_libs "${lib}" LINK_LIBRARIES)
    if(link_libs)
      foreach(dep IN LISTS link_libs)
        isotone_ensure_fuzz_library("${dep}" mapped_dep)
        list(APPEND mapped_link_libs "${mapped_dep}")
      endforeach()
    endif()

    set(mapped_iface_libs "")
    get_target_property(iface_libs "${lib}" INTERFACE_LINK_LIBRARIES)
    if(iface_libs)
      foreach(dep IN LISTS iface_libs)
        isotone_ensure_fuzz_library("${dep}" mapped_dep)
        list(APPEND mapped_iface_libs "${mapped_dep}")
      endforeach()
    endif()

    get_target_property(lib_source_dir "${lib}" SOURCE_DIR)
    get_target_property(lib_sources "${lib}" ISOTONE_LIBRARY_SOURCES)
    set(resolved_sources "")
    foreach(src IN LISTS lib_sources)
      if(IS_ABSOLUTE "${src}")
        list(APPEND resolved_sources "${src}")
      else()
        list(APPEND resolved_sources "${lib_source_dir}/${src}")
      endif()
    endforeach()

    add_library(${fuzz_lib} STATIC ${resolved_sources})
    get_target_property(manual_deps "${lib}" MANUALLY_ADDED_DEPENDENCIES)
    if(manual_deps)
      add_dependencies(${fuzz_lib} ${manual_deps})
    endif()
    foreach(
      prop_name
      IN ITEMS
        INCLUDE_DIRECTORIES
        INTERFACE_INCLUDE_DIRECTORIES
        INTERFACE_SYSTEM_INCLUDE_DIRECTORIES
        COMPILE_DEFINITIONS
        INTERFACE_COMPILE_DEFINITIONS
        COMPILE_OPTIONS
        INTERFACE_COMPILE_OPTIONS
        COMPILE_FEATURES
        INTERFACE_COMPILE_FEATURES
        LINK_OPTIONS
        INTERFACE_LINK_OPTIONS)
      get_target_property(prop_val "${lib}" ${prop_name})
      if(prop_val)
        set_property(TARGET ${fuzz_lib} PROPERTY ${prop_name} ${prop_val})
      endif()
    endforeach()
    if(mapped_link_libs)
      set_property(TARGET ${fuzz_lib} PROPERTY LINK_LIBRARIES ${mapped_link_libs})
    endif()
    if(mapped_iface_libs)
      set_property(TARGET ${fuzz_lib} PROPERTY INTERFACE_LINK_LIBRARIES ${mapped_iface_libs})
    endif()
    isotone_apply_fuzz_flags(${fuzz_lib} LIBRARY)
    set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS ${fuzz_lib})
  endif()

  set(${out_var} "${fuzz_lib}" PARENT_SCOPE)
endfunction()

# isotone_add_fuzz_target(<name> SOURCES <sources>... LIBRARIES <libraries>...): in a fuzz preset (ISOTONE_FUZZ=ON),
# builds a libFuzzer executable `<name>_fuzz` and compiles the transitive first-party static library closure of
# LIBRARIES in `<lib>_fuzz` variants with coverage and AddressSanitizer instrumentation; in every other test-capable
# preset (BUILD_TESTING=ON, never the dist presets), builds a deterministic replay executable `<name>_fuzz_replay` that
# runs LLVMFuzzerTestOneInput once on every file under `native/tests/fuzz/<name>/corpus/` and `regressions/`, registered
# with CTest as `fuzz.<name>` (D00 T05 §9, D00-T05-S8-PR9, D00-T05-S8-PR10).
function(isotone_add_fuzz_target name)
  cmake_parse_arguments(ARG "" "" "SOURCES;LIBRARIES" ${ARGN})
  if(NOT ARG_SOURCES)
    message(FATAL_ERROR "isotone_add_fuzz_target(${name}): SOURCES is required")
  endif()
  set(corpus_dir "${PROJECT_SOURCE_DIR}/tests/fuzz/${name}/corpus")
  set(regressions_dir "${PROJECT_SOURCE_DIR}/tests/fuzz/${name}/regressions")

  if(ISOTONE_FUZZ)
    set(fuzz_libs "")
    foreach(lib IN LISTS ARG_LIBRARIES)
      isotone_ensure_fuzz_library("${lib}" mapped_lib)
      list(APPEND fuzz_libs "${mapped_lib}")
    endforeach()
    set(exe_target "${name}_fuzz")
    add_executable(${exe_target} ${ARG_SOURCES})
    set_target_properties(
      ${exe_target}
      PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/${exe_target}.dir")
    if(fuzz_libs)
      target_link_libraries(${exe_target} PRIVATE ${fuzz_libs})
    endif()
    isotone_apply_flags(${exe_target})
    isotone_apply_fuzz_flags(${exe_target} EXECUTABLE)
    add_test(
      NAME "fuzz.${name}"
      COMMAND "${exe_target}" -runs=0 "${corpus_dir}" "${regressions_dir}")
    set_property(TARGET ${exe_target} PROPERTY ISOTONE_REGISTERED_TEST TRUE)
    set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS ${exe_target})
    set_property(
      GLOBAL APPEND PROPERTY ISOTONE_FUZZ_TARGETS
      "${name}|$<TARGET_FILE:${exe_target}>|${corpus_dir}|${regressions_dir}")
  elseif(BUILD_TESTING)
    if(NOT TARGET isotone_fuzz_replay_main)
      isotone_add_library(
        isotone_fuzz_replay_main
        "${PROJECT_SOURCE_DIR}/tests/fuzz/fuzz_replay_main.cpp")
      set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS isotone_fuzz_replay_main)
    endif()
    set(exe_target "${name}_fuzz_replay")
    add_executable(${exe_target} ${ARG_SOURCES})
    target_link_libraries(${exe_target} PRIVATE ${ARG_LIBRARIES} isotone_fuzz_replay_main)
    isotone_apply_flags(${exe_target})
    add_test(
      NAME "fuzz.${name}"
      COMMAND "${exe_target}" "${corpus_dir}" "${regressions_dir}")
    set_property(TARGET ${exe_target} PROPERTY ISOTONE_REGISTERED_TEST TRUE)
    set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS ${exe_target})
  endif()
endfunction()

# isotone_add_test(<name> <sources>... LINK <libraries>...): a GoogleTest executable registered with CTest. Discovery
# runs at test time (PRE_TEST), so a build never runs a test executable: an ARM64 one cross-built on x64 cannot run
# there (CMake GoogleTest module, DISCOVERY_MODE).
function(isotone_add_test name)
  cmake_parse_arguments(ARG "" "" "LINK" ${ARGN})
  add_executable(${name} ${ARG_UNPARSED_ARGUMENTS})
  target_link_libraries(${name} PRIVATE ${ARG_LINK} GTest::gtest GTest::gtest_main)
  isotone_apply_flags(${name})
  if(ISOTONE_ANALYZE)
    # WORKAROUND: GoogleTest's assertion macros expand `switch (0) case 0: default:` into the test's own source, which
    # /analyze reports as C6326 (a constant compared with a constant) on every assertion; /analyze:external- covers
    # external headers, not macro expansions, so the one warning is off for test executables only.
    target_compile_options(${name} PRIVATE /wd6326)
  endif()
  gtest_discover_tests(${name} DISCOVERY_MODE PRE_TEST)
  set_property(TARGET ${name} PROPERTY ISOTONE_REGISTERED_TEST TRUE)
  set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS ${name})
endfunction()

# isotone_add_sanitizer_probe(<name> <source> <report>): an executable that commits one memory error on purpose, registered with
# CTest under the asan-probe label. It passes only when <report>, AddressSanitizer's report for that error, appears in its output
# (PASS_REGULAR_EXPRESSION, without WILL_FAIL, which would invert the verdict), so an uninstrumented build, which runs
# to its end without a report, fails. Built only in the sanitizer presets (native/tests/CMakeLists.txt).
function(isotone_add_sanitizer_probe name source report)
  add_executable(${name} ${source})
  isotone_apply_flags(${name})
  add_test(
    NAME ${name}
    COMMAND
      "${CMAKE_COMMAND}"
      "-DPROBE=$<TARGET_FILE:${name}>"
      -P "${CMAKE_CURRENT_FUNCTION_LIST_DIR}/RunSanitizerProbe.cmake")
  set_tests_properties(${name} PROPERTIES LABELS asan-probe PASS_REGULAR_EXPRESSION "${report}")
  set_property(TARGET ${name} PROPERTY ISOTONE_REGISTERED_TEST TRUE)
  set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS ${name})
endfunction()

# isotone_write_dev_targets(): the developer-only targets (tests, probes, and benchmarks) into
# ${CMAKE_BINARY_DIR}/isotone-dev-targets.txt, one per line, which scripts/native-deps-lint.py reads: only these may link a
# test-only or developer-only library (D00 T04 §1, test-only-linked). Called at the end of native/CMakeLists.txt.
function(isotone_write_dev_targets)
  get_property(targets GLOBAL PROPERTY ISOTONE_DEV_TARGETS)
  list(SORT targets)
  string(JOIN "\n" text ${targets})
  file(WRITE "${CMAKE_BINARY_DIR}/isotone-dev-targets.txt" "${text}\n")
endfunction()

# isotone_write_fuzz_targets(): in a fuzz preset, writes ${CMAKE_BINARY_DIR}/isotone-fuzz-targets.txt with one line per
# registered fuzz target (`<name>|<executable>|<corpus_dir>|<regressions_dir>`) for the nightly fuzz workflow.
function(isotone_write_fuzz_targets)
  get_property(entries GLOBAL PROPERTY ISOTONE_FUZZ_TARGETS)
  if(entries)
    string(JOIN "\n" text ${entries})
    file(GENERATE OUTPUT "${CMAKE_BINARY_DIR}/isotone-fuzz-targets.txt" CONTENT "${text}\n")
  endif()
endfunction()

# isotone_require_registered_tests(<dir>): every executable under a tests folder went through isotone_add_test. A test
# executable added any other way builds and never runs, and CTest still passes on the other tests, so noTestsAction
# alone cannot see it. Called at the end of native/tests/CMakeLists.txt.
function(isotone_require_registered_tests dir)
  get_property(targets DIRECTORY "${dir}" PROPERTY BUILDSYSTEM_TARGETS)
  foreach(target IN LISTS targets)
    get_target_property(type ${target} TYPE)
    get_target_property(registered ${target} ISOTONE_REGISTERED_TEST)
    if(type STREQUAL "EXECUTABLE" AND NOT registered)
      message(FATAL_ERROR "${target} is an executable under ${dir} that isotone_add_test did not register, so its "
                          "tests would never run")
    endif()
  endforeach()
  get_property(subdirs DIRECTORY "${dir}" PROPERTY SUBDIRECTORIES)
  foreach(subdir IN LISTS subdirs)
    isotone_require_registered_tests("${subdir}")
  endforeach()
endfunction()
