#include "isotone/core/build_info.h"

#include "isotone/core/build_id.h"

namespace isotone::core {

std::string_view version() noexcept { return ISOTONE_VERSION; }

std::string_view build_id() noexcept { return ISOTONE_BUILD_ID; }

}  // namespace isotone::core
