# Run an AddressSanitizer probe executable for CTest.
#
# When ASAN_OPTIONS redirects reports through log_path=<prefix>, the runtime writes its
# diagnostic to <prefix>.<pid> instead of stderr. This wrapper keeps that report file on
# disk for CI retention and echoes its text so CTest's PASS_REGULAR_EXPRESSION still
# evaluates the probe against the sanitizer summary.

if(NOT DEFINED PROBE OR NOT EXISTS "${PROBE}")
    message(FATAL_ERROR "RunSanitizerProbe: PROBE executable not found: '${PROBE}'")
endif()

set(log_prefix "")
if("$ENV{ASAN_OPTIONS}" MATCHES "(^|:)log_path=(([A-Za-z]:[/\\\\])?[^:]+)")
    set(log_prefix "${CMAKE_MATCH_2}")
endif()

set(abs_prefix "")
if(NOT log_prefix STREQUAL "")
    get_filename_component(probe_stem "${PROBE}" NAME_WE)
    get_filename_component(base_prefix "${log_prefix}" ABSOLUTE BASE_DIR "${CMAKE_CURRENT_BINARY_DIR}")
    set(abs_prefix "${base_prefix}.${probe_stem}")
    get_filename_component(log_dir "${abs_prefix}" DIRECTORY)
    if(NOT log_dir STREQUAL "")
        file(MAKE_DIRECTORY "${log_dir}")
    endif()
    file(GLOB stale_logs "${abs_prefix}.*")
    if(stale_logs)
        file(REMOVE ${stale_logs})
    endif()
    string(REGEX REPLACE "(^|:)log_path=(([A-Za-z]:[/\\\\])?[^:]+)" "\\1log_path=${log_prefix}.${probe_stem}" probe_asan_options "$ENV{ASAN_OPTIONS}")
    set(ENV{ASAN_OPTIONS} "${probe_asan_options}")
endif()

execute_process(
    COMMAND "${PROBE}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
    RESULT_VARIABLE probe_rc
    OUTPUT_VARIABLE probe_out
    ERROR_VARIABLE probe_err
)

if(NOT probe_out STREQUAL "")
    message("${probe_out}")
endif()
if(NOT probe_err STREQUAL "")
    message("${probe_err}")
endif()

if(NOT abs_prefix STREQUAL "")
    file(GLOB probe_logs "${abs_prefix}.*")
    foreach(report_file IN LISTS probe_logs)
        file(READ "${report_file}" report_text)
        message("${report_text}")
    endforeach()
endif()
