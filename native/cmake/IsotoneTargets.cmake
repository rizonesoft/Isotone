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
  if(ISOTONE_SANITIZE STREQUAL "address")
    target_compile_options(${target} PRIVATE /fsanitize=address)
  elseif(NOT ISOTONE_SANITIZE STREQUAL "")
    message(FATAL_ERROR "ISOTONE_SANITIZE is '${ISOTONE_SANITIZE}': only empty or address is supported")
  endif()
endfunction()

# isotone_add_library(<name> <sources>... [PUBLIC_INCLUDE <dir>]): a static library with the suite's flags.
function(isotone_add_library name)
  cmake_parse_arguments(ARG "" "PUBLIC_INCLUDE" "" ${ARGN})
  add_library(${name} STATIC ${ARG_UNPARSED_ARGUMENTS})
  if(ARG_PUBLIC_INCLUDE)
    target_include_directories(${name} PUBLIC ${ARG_PUBLIC_INCLUDE})
  endif()
  isotone_apply_flags(${name})
endfunction()

# isotone_add_test(<name> <sources>... LINK <libraries>...): a GoogleTest executable registered with CTest. Discovery
# runs at test time (PRE_TEST), so a build never runs a test executable: an ARM64 one cross-built on x64 cannot run
# there (CMake GoogleTest module, DISCOVERY_MODE).
function(isotone_add_test name)
  cmake_parse_arguments(ARG "" "" "LINK" ${ARGN})
  add_executable(${name} ${ARG_UNPARSED_ARGUMENTS})
  target_link_libraries(${name} PRIVATE ${ARG_LINK} GTest::gtest GTest::gtest_main)
  isotone_apply_flags(${name})
  gtest_discover_tests(${name} DISCOVERY_MODE PRE_TEST)
  set_property(TARGET ${name} PROPERTY ISOTONE_REGISTERED_TEST TRUE)
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
