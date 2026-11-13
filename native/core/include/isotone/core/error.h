// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include <cstdint>
#include <exception>
#include <memory>
#include <string>
#include <string_view>

namespace isotone::core
{

// The error isotone::core throws: the call that failed, its Win32 error or HRESULT, and what it was doing.
// Thrown by value and caught by reference; copying it never throws. Safe to create on any thread.
class Error : public std::exception
{
  public:
    // call names the failing call ("CreateFileW"); code is its Win32 error or HRESULT as an unsigned value;
    // context says what was being done ("creating D:\\data\\logs"). Throws std::bad_alloc only.
    Error(std::string_view call, std::uint32_t code, std::string_view context);

    // "<call> failed with error <code> (0x<hex>) while <context>", in UTF-8.
    [[nodiscard]] const char* what() const noexcept override;

    // The failing call's name, as given.
    [[nodiscard]] std::string_view call() const noexcept;

    // The Win32 error or HRESULT, as given.
    [[nodiscard]] std::uint32_t code() const noexcept;

  private:
    struct Text
    {
        std::string call;
        std::string message;
    };
    // Shared, so copying an Error only copies a pointer and never allocates.
    std::shared_ptr<const Text> text_;
    std::uint32_t code_;
};

} // namespace isotone::core
