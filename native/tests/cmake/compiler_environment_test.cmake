# Drives native/cmake/CheckCompilerEnvironment.cmake (cmake -P, registered with CTest by native/tests/CMakeLists.txt):
# it passes with CL and _CL_ unset and refuses each of them set. Input: SCRIPT (CheckCompilerEnvironment.cmake).
function(run_check)
  execute_process(COMMAND "${CMAKE_COMMAND}" -E env --unset=CL --unset=_CL_ ${ARGN} "${CMAKE_COMMAND}" -P "${SCRIPT}"
                  RESULT_VARIABLE rc OUTPUT_VARIABLE log ERROR_VARIABLE log)
  set(rc "${rc}" PARENT_SCOPE)
  set(log "${log}" PARENT_SCOPE)
endfunction()

run_check()
if(NOT rc EQUAL 0)
  message(FATAL_ERROR "with CL and _CL_ unset the check failed:\n${log}")
endif()
message(STATUS "ok: CL and _CL_ unset pass")

foreach(case IN ITEMS "_CL_=/std:c++20" "CL=/nologo")
  string(REGEX MATCH "^[^=]+" name "${case}")
  run_check("${case}")
  if(rc EQUAL 0 OR NOT log MATCHES "${name} is set to")
    message(FATAL_ERROR "with ${case} the check passed or named nothing (rc ${rc}):\n${log}")
  endif()
  message(STATUS "ok: ${case} is refused")
endforeach()
