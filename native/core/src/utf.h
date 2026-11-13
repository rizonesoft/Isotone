// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// Private to isotone::core: UTF-8 and UTF-16 conversion at a Windows call (standards/shared.md, C++ style).

#pragma once

#include <string>

namespace isotone::core::detail
{

// Converts UTF-8 to UTF-16 for a Windows call. Throws Error (MultiByteToWideChar) on invalid UTF-8. Any thread.
[[nodiscard]] std::wstring utf8_to_utf16(const std::string& text);

// Converts UTF-16 from a Windows call to UTF-8. Throws Error (WideCharToMultiByte) on an unpaired surrogate.
// Any thread.
[[nodiscard]] std::string utf16_to_utf8(const std::wstring& text);

} // namespace isotone::core::detail
