// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "utf.h"

#include "isotone/core/error.h"

#include <climits>
#include <string>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>

namespace isotone::core::detail
{

std::wstring utf8_to_utf16(const std::string& text)
{
    if (text.empty())
    {
        return {};
    }
    if (text.size() > static_cast<std::size_t>(INT_MAX))
    {
        throw Error{"MultiByteToWideChar", ERROR_INVALID_PARAMETER, "converting text longer than INT_MAX bytes"};
    }
    const int bytes = static_cast<int>(text.size());
    const int units = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, text.data(), bytes, nullptr, 0);
    if (units <= 0)
    {
        throw Error{"MultiByteToWideChar", GetLastError(), "converting UTF-8 to UTF-16"};
    }
    std::wstring out(static_cast<std::size_t>(units), L'\0');
    if (MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, text.data(), bytes, out.data(), units) != units)
    {
        throw Error{"MultiByteToWideChar", GetLastError(), "converting UTF-8 to UTF-16"};
    }
    return out;
}

std::string utf16_to_utf8(const std::wstring& text)
{
    if (text.empty())
    {
        return {};
    }
    if (text.size() > static_cast<std::size_t>(INT_MAX))
    {
        throw Error{"WideCharToMultiByte", ERROR_INVALID_PARAMETER, "converting text longer than INT_MAX units"};
    }
    const int units = static_cast<int>(text.size());
    const int bytes =
        WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, text.data(), units, nullptr, 0, nullptr, nullptr);
    if (bytes <= 0)
    {
        throw Error{"WideCharToMultiByte", GetLastError(), "converting UTF-16 to UTF-8"};
    }
    std::string out(static_cast<std::size_t>(bytes), '\0');
    if (WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, text.data(), units, out.data(), bytes, nullptr, nullptr) !=
        bytes)
    {
        throw Error{"WideCharToMultiByte", GetLastError(), "converting UTF-16 to UTF-8"};
    }
    return out;
}

} // namespace isotone::core::detail
