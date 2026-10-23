# Drives native/cmake/WriteBuildId.cmake through each of its paths in a scratch folder (cmake -P, registered with
# CTest by native/tests/CMakeLists.txt). Inputs: SCRIPT (WriteBuildId.cmake), WORK (a scratch folder this test owns).
find_package(Git REQUIRED)
file(REMOVE_RECURSE "${WORK}")
file(MAKE_DIRECTORY "${WORK}")

function(run_script source stamp out)
  execute_process(COMMAND "${CMAKE_COMMAND}" "-DOUT=${out}" "-DSOURCE_DIR=${source}" "-DSTAMP=${stamp}" -P "${SCRIPT}"
                  RESULT_VARIABLE rc OUTPUT_VARIABLE log ERROR_VARIABLE log)
  set(rc "${rc}" PARENT_SCOPE)
  set(log "${log}" PARENT_SCOPE)
endfunction()

function(expect_id out want label)
  file(READ "${out}" header)
  if(NOT header MATCHES "#define ISOTONE_BUILD_ID \"${want}\"")
    message(FATAL_ERROR "${label}: want id ${want}, header reads:\n${header}")
  endif()
  message(STATUS "ok: ${label}")
endfunction()

function(git_in dir)
  execute_process(COMMAND "${GIT_EXECUTABLE}" -C "${dir}" -c user.name=build-id-test -c user.email=test@isotone.invalid
                          -c commit.gpgsign=false -c core.hooksPath=NUL ${ARGN}
                  RESULT_VARIABLE rc OUTPUT_VARIABLE out OUTPUT_STRIP_TRAILING_WHITESPACE ERROR_VARIABLE err)
  if(NOT rc EQUAL 0)
    message(FATAL_ERROR "git ${ARGN} in ${dir} failed: ${err}")
  endif()
  set(git_out "${out}" PARENT_SCOPE)
endfunction()

set(placeholder "$Format:%H$\n")

# A work tree whose top is the source folder: its HEAD, then -dirty after an edit.
set(repo "${WORK}/repo")
file(MAKE_DIRECTORY "${repo}/native")
file(WRITE "${repo}/native/BUILD_ID.txt" "${placeholder}")
file(WRITE "${repo}/file.txt" "one\n")
git_in("${repo}" init -q)
git_in("${repo}" add -A)
git_in("${repo}" commit -q -m one)
git_in("${repo}" rev-parse --short=12 HEAD)
set(head "${git_out}")
run_script("${repo}" "${repo}/native/BUILD_ID.txt" "${WORK}/clean.h")
expect_id("${WORK}/clean.h" "${head}" "a clean checkout reports its HEAD")
file(WRITE "${repo}/file.txt" "two\n")
run_script("${repo}" "${repo}/native/BUILD_ID.txt" "${WORK}/dirty.h")
expect_id("${WORK}/dirty.h" "${head}-dirty" "an edited checkout reports -dirty")

# An archive unpacked inside that work tree: the stamp wins over the enclosing repository.
set(archive "${repo}/unpacked")
file(MAKE_DIRECTORY "${archive}/native")
file(WRITE "${archive}/native/BUILD_ID.txt" "0123456789abcdef0123456789abcdef01234567\n")
run_script("${archive}" "${archive}/native/BUILD_ID.txt" "${WORK}/archive.h")
expect_id("${WORK}/archive.h" "0123456789ab" "a stamped archive inside another work tree reports its stamp")

# An unstamped folder inside a work tree is not that tree's top: refused, never the enclosing commit.
set(stray "${repo}/stray")
file(MAKE_DIRECTORY "${stray}/native")
file(WRITE "${stray}/native/BUILD_ID.txt" "${placeholder}")
run_script("${stray}" "${stray}/native/BUILD_ID.txt" "${WORK}/stray.h")
if(rc EQUAL 0 OR NOT log MATCHES "No build id")
  message(FATAL_ERROR "an unstamped folder inside a work tree: want the No build id refusal, got rc ${rc}:\n${log}")
endif()
message(STATUS "ok: an unstamped folder inside another work tree is refused")

# An unchanged id leaves the header untouched, so a build with nothing new recompiles nothing.
file(TIMESTAMP "${WORK}/archive.h" before "%Y-%m-%dT%H:%M:%S.%f")
execute_process(COMMAND "${CMAKE_COMMAND}" -E sleep 1.1)
run_script("${archive}" "${archive}/native/BUILD_ID.txt" "${WORK}/archive.h")
file(TIMESTAMP "${WORK}/archive.h" after "%Y-%m-%dT%H:%M:%S.%f")
if(NOT before STREQUAL after)
  message(FATAL_ERROR "an unchanged id rewrote the header (${before} -> ${after})")
endif()
message(STATUS "ok: an unchanged id leaves the header untouched")

file(REMOVE_RECURSE "${WORK}")
