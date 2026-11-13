# isotone::core, the shared non-UI library: the build identity, the error type, app-data folders, and the structured log.
set(ISOTONE_BUILD_ID_HEADER "${CMAKE_CURRENT_BINARY_DIR}/generated/isotone/core/build_id.h")
add_custom_target(isotone_build_id
  COMMAND "${CMAKE_COMMAND}" "-DOUT=${ISOTONE_BUILD_ID_HEADER}" "-DSOURCE_DIR=${PROJECT_SOURCE_DIR}/.."
          "-DSTAMP=${PROJECT_SOURCE_DIR}/BUILD_ID.txt" -P "${PROJECT_SOURCE_DIR}/cmake/WriteBuildId.cmake"
  BYPRODUCTS "${ISOTONE_BUILD_ID_HEADER}"
  COMMENT "Writing the build id"
  VERBATIM)

isotone_add_library(isotone_core
  src/app_paths.cpp
  src/build_info.cpp
  src/error.cpp
  src/imaging/premultiply.cpp
  src/log.cpp
  src/utf.cpp
  PUBLIC_INCLUDE "${CMAKE_CURRENT_SOURCE_DIR}/include")
add_library(isotone::core ALIAS isotone_core)
add_dependencies(isotone_core isotone_build_id)
target_include_directories(isotone_core PRIVATE "${CMAKE_CURRENT_BINARY_DIR}/generated")
target_compile_definitions(isotone_core PRIVATE "ISOTONE_VERSION=\"${ISOTONE_VERSION}\"")
# SHGetKnownFolderPath (shell32) and CoTaskMemFree (ole32) resolve the app-data folders (D01 T27 §1).
target_link_libraries(isotone_core PUBLIC shell32 ole32)
