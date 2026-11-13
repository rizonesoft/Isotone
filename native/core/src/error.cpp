// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/error.h"

#include <format>
#include <type_traits>

namespace isotone::core
{

Error::Error(std::string_view call, std::uint32_t code, std::string_view context)
    : text_{std::make_shared<const Text>(
          Text{.call = std::string{call},
               .message = std::format("{} failed with error {} (0x{:08X}) while {}", call, code, code, context)})},
      code_{code}
{
}

static_assert(std::is_nothrow_copy_constructible_v<Error>, "an Error is copied while an exception is in flight");

const char* Error::what() const noexcept
{
    return text_->message.c_str();
}

std::string_view Error::call() const noexcept
{
    return text_->call;
}

std::uint32_t Error::code() const noexcept
{
    return code_;
}

} // namespace isotone::core
