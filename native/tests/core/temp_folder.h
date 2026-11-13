// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// A fresh folder under the system temporary folder for one test, removed with everything in it afterwards.

#pragma once

#include <atomic>
#include <chrono>
#include <cstdio>
#include <filesystem>
#include <format>
#include <system_error>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>

namespace isotone::tests
{

class TempFolder
{
  public:
    TempFolder()
    {
        static std::atomic<unsigned> counter{0};
        const auto ticks = std::chrono::steady_clock::now().time_since_epoch().count();
        path_ = std::filesystem::temp_directory_path() / "isotone-tests" /
                std::format("{}-{}-{}", GetCurrentProcessId(), ticks, counter.fetch_add(1));
        std::filesystem::create_directories(path_);
    }
    ~TempFolder()
    {
        try
        {
            std::error_code error;
            std::filesystem::remove_all(path_, error);
        }
        catch (...)
        {
            // A folder left behind stays under the temporary folder; say so rather than fail the test run.
            std::fputs("TempFolder: a test folder could not be removed\n", stderr);
        }
    }
    TempFolder(const TempFolder&) = delete;
    TempFolder& operator=(const TempFolder&) = delete;
    TempFolder(TempFolder&&) = delete;
    TempFolder& operator=(TempFolder&&) = delete;

    [[nodiscard]] const std::filesystem::path& path() const noexcept
    {
        return path_;
    }

  private:
    std::filesystem::path path_;
};

} // namespace isotone::tests
