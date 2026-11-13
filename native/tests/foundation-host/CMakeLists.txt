# The foundation test host (D01 T15 §1): the one window every native foundation proves itself in. Its logic is a
# library so the unit tests reach it; foundation-host.exe is that library behind wmain, with the suite's application
# manifest embedded. README.md describes the switches, the report, and how a foundation adds a scenario.
isotone_add_library(foundation_host_lib host.cpp PUBLIC_INCLUDE "${CMAKE_CURRENT_SOURCE_DIR}")
target_link_libraries(foundation_host_lib PUBLIC isotone::ui isotone::core nlohmann_json::nlohmann_json gdi32 user32)
set_property(GLOBAL APPEND PROPERTY ISOTONE_DEV_TARGETS foundation_host_lib)

isotone_add_executable(foundation_host main.cpp "${PROJECT_SOURCE_DIR}/ui/app.manifest"
  LINK foundation_host_lib DEV_ONLY)
set_target_properties(foundation_host PROPERTIES OUTPUT_NAME "foundation-host")
# CTest runs this executable through the foundation.* entries below, which is what the tests-folder guard asks of
# every executable here (isotone_require_registered_tests).
set_property(TARGET foundation_host PROPERTY ISOTONE_REGISTERED_TEST TRUE)

isotone_add_test(foundation_host_tests host_tests.cpp LINK foundation_host_lib)

# One CTest entry per case of run_host.cmake, which runs the host and checks its exit code, its console, and its
# report. Exit 77 is the host saying there is no display session: CTest reports the entry as skipped.
# Each entry's scratch folder sits directly in this binary folder: the ARM64 test runner, which runs a tree built on
# another machine, requires the parent of every -DWORK folder to exist there (scripts/run-arm64-tests.ps1).
foreach(case smoke lifecycle unknown-scenario unwritable-report missing-data-root unusable-data-root
        window-failure)
  add_test(NAME "foundation.${case}"
    COMMAND "${CMAKE_COMMAND}" "-DHOST=$<TARGET_FILE:foundation_host>"
            "-DWORK=${CMAKE_CURRENT_BINARY_DIR}/run-${case}" "-DCASE=${case}"
            -P "${CMAKE_CURRENT_SOURCE_DIR}/run_host.cmake")
  set_tests_properties("foundation.${case}" PROPERTIES SKIP_RETURN_CODE 77 TIMEOUT 180)
endforeach()
