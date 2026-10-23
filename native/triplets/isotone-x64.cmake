# isotone-x64: static libraries and the static CRT, built with the pinned MSVC toolset for x64.
set(VCPKG_TARGET_ARCHITECTURE x64)
# The toolset is the pin's selector (native/toolchain.json), not the newest minor installed, which a built-in Windows
# triplet would take (vcpkg "Triplet files", VCPKG_PLATFORM_TOOLSET_VERSION). scripts/dev-env.ps1 -Check refuses a
# triplet whose toolset version differs from the pin.
set(VCPKG_LIBRARY_LINKAGE static)
set(VCPKG_CRT_LINKAGE static)
set(VCPKG_PLATFORM_TOOLSET v145)
set(VCPKG_PLATFORM_TOOLSET_VERSION 14.51.36231)
if(DEFINED ENV{VSINSTALLDIR})
  # The Visual Studio installation scripts/dev-env.ps1 entered, so every port builds with the same installation.
  # vcvarsall leaves a trailing separator, which vcpkg's instance list does not carry.
  string(REGEX REPLACE "[\\/]+$" "" VCPKG_VISUAL_STUDIO_PATH "$ENV{VSINSTALLDIR}")
endif()
