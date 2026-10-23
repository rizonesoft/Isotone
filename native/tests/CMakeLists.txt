# The GoogleTest suites, one folder per library or app, and the script tests of the CMake helpers.
add_subdirectory(core)

add_test(NAME cmake.build_id
  COMMAND "${CMAKE_COMMAND}" "-DSCRIPT=${PROJECT_SOURCE_DIR}/cmake/WriteBuildId.cmake"
          "-DWORK=${CMAKE_CURRENT_BINARY_DIR}/build_id_test" -P "${CMAKE_CURRENT_SOURCE_DIR}/cmake/build_id_test.cmake")
add_test(NAME cmake.compiler_environment
  COMMAND "${CMAKE_COMMAND}" "-DSCRIPT=${PROJECT_SOURCE_DIR}/cmake/CheckCompilerEnvironment.cmake"
          -P "${CMAKE_CURRENT_SOURCE_DIR}/cmake/compiler_environment_test.cmake")

if(ISOTONE_SANITIZE STREQUAL "address")
  add_subdirectory(sanitizer)
endif()

isotone_require_registered_tests("${CMAKE_CURRENT_SOURCE_DIR}")
