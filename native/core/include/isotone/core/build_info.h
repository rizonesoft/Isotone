#pragma once

#include <string_view>

namespace isotone::core
{

// The version the build reports (the ISOTONE_VERSION cache variable until versioning computes it from the tag).
std::string_view version() noexcept;

// The commit the binary was built from: its first 12 hex digits, plus "-dirty" when tracked files differed from it.
std::string_view build_id() noexcept;

} // namespace isotone::core
