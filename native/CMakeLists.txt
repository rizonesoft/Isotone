# The native build of the Isotone Graphics Suite (D00 T05 §3; docs/specs/2026-10-22-native-stack-design.md, "Build
# description"). Configure it through the presets in this folder, inside scripts/dev-env.ps1.
cmake_minimum_required(VERSION 4.3)
project(Isotone LANGUAGES C CXX)
if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  # The presets name cl; another compiler here means the build ran outside scripts/dev-env.ps1 or ignored the presets.
  message(FATAL_ERROR "The native build needs MSVC (cl); configured with ${CMAKE_CXX_COMPILER_ID} at ${CMAKE_CXX_COMPILER}")
endif()

# C++23 through the pinned switch. CMake maps CXX_STANDARD 23 on MSVC to /std:c++latest, which the standard decision
# forbids (docs/dev/decisions.md, "2026-10-22: The C++ language standard"); these two make CMake emit /std:c++23preview
# for every C++23 target, and satisfy a lower compile feature (GoogleTest's cxx_std_17) with that same one switch.
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(ISOTONE_CXX_STD_SWITCH "/std:c++23preview" CACHE STRING "The C++23 switch the pinned MSVC toolset takes")
set(CMAKE_CXX23_STANDARD_COMPILE_OPTION "${ISOTONE_CXX_STD_SWITCH}")
set(CMAKE_CXX23_EXTENSION_COMPILE_OPTION "${ISOTONE_CXX_STD_SWITCH}")

# The static runtime, so no app installs a Visual C++ redistributable, and full program databases in every
# configuration, so a Release crash dump resolves to source.
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "ProgramDatabase")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(ISOTONE_VERSION "0.0.0" CACHE STRING "The version the build reports until versioning computes it from the tag")
set(ISOTONE_SANITIZE "" CACHE STRING "A sanitizer every target builds with: empty, or address")

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(IsotoneTargets)

# BUILD_TESTING is on by default; the dist presets an app release builds from turn it off, with the vcpkg test feature
# unrequested, so no test library is installed or linked there.
include(CTest)
if(BUILD_TESTING)
  find_package(GTest CONFIG REQUIRED)
  include(GoogleTest)
endif()

add_subdirectory(core)
if(BUILD_TESTING)
  add_subdirectory(tests)
endif()
