// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/error.h"

#include <format>

namespace isotone::core
{

Error::Error(std::string_view call, std::uint32_t code, std::string_view context)
    : call_{call}, message_{std::format("{} failed with error {} (0x{:08X}) while {}", call, code, code, context)},
      code_{code}
{
}

const char* Error::what() const noexcept
{
    return message_.c_str();
}

std::string_view Error::call() const noexcept
{
    return call_;
}

std::uint32_t Error::code() const noexcept
{
    return code_;
}

} // namespace isotone::core
