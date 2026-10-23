# Refuses MSVC's CL and _CL_ environment variables, which cl adds before and after its own command line on every
# compile (Microsoft Learn, "CL environment variables"): `_CL_=/std:c++20` would override the pinned /std:c++23preview,
# and nothing in compile_commands.json would show it (D00 T05 §3). Included at configure time by native/CMakeLists.txt
# and run on every build by the isotone_compiler_environment target (cmake -P), because the build's environment can
# differ from the one that configured it. scripts/dev-env.ps1 clears both on entry.
foreach(name IN ITEMS CL _CL_)
  if(NOT "$ENV{${name}}" STREQUAL "")
    message(FATAL_ERROR "${name} is set to '$ENV{${name}}': MSVC adds it to every compile, outside the build "
                        "description. Clear it, or build inside scripts/dev-env.ps1, which clears it.")
  endif()
endforeach()
