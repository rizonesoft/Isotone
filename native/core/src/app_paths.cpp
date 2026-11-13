// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/app_paths.h"

#include "isotone/core/error.h"
#include "utf.h"

#include <cstdint>
#include <memory>
#include <string>
#include <system_error>

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
// windows.h first: the shell and COM headers need its types.
#include <combaseapi.h>
#include <knownfolders.h>
#include <shlobj_core.h>

namespace isotone::core
{
namespace
{

// The publisher folder every app's data lives under (AGENTS.md: the publisher users see is Rizonesoft).
constexpr std::wstring_view kPublisherFolder{L"Rizonesoft"};
constexpr std::wstring_view kLogsFolder{L"logs"};
constexpr std::wstring_view kSettingsFolder{L"settings"};
constexpr std::wstring_view kRecoveryFolder{L"recovery"};
// GetModuleFileNameW reports truncation by filling the buffer; long paths can reach 32,767 UTF-16 units.
constexpr std::size_t kMaxPathUnits = 32'768;

struct CoTaskMemDeleter
{
    void operator()(wchar_t* text) const noexcept
    {
        CoTaskMemFree(text);
    }
};

void check_app_name(std::string_view app_name)
{
    constexpr std::string_view kReserved{"\\/:*?\"<>|"};
    bool valid = !app_name.empty() && app_name != "." && app_name != "..";
    for (const char character : app_name)
    {
        if (static_cast<unsigned char>(character) < 0x20U || kReserved.contains(character))
        {
            valid = false;
        }
    }
    if (!valid)
    {
        throw Error{"resolve_app_folders", ERROR_INVALID_NAME,
                    std::string{"checking the app name \""} + std::string{app_name} + "\""};
    }
}

void create_folder(const std::filesystem::path& folder)
{
    std::error_code error;
    std::filesystem::create_directories(folder, error);
    if (error)
    {
        throw Error{"std::filesystem::create_directories", static_cast<std::uint32_t>(error.value()),
                    "creating " + detail::utf16_to_utf8(folder.native())};
    }
}

} // namespace

AppFolderSources AppFolderSources::from_windows()
{
    AppFolderSources sources;

    PWSTR raw = nullptr;
    const HRESULT result = SHGetKnownFolderPath(FOLDERID_LocalAppData, KF_FLAG_DEFAULT, nullptr, &raw);
    const std::unique_ptr<wchar_t, CoTaskMemDeleter> owned{raw};
    if (FAILED(result))
    {
        throw Error{"SHGetKnownFolderPath", static_cast<std::uint32_t>(result), "reading FOLDERID_LocalAppData"};
    }
    sources.local_app_data = std::filesystem::path{owned.get()};

    std::wstring module(kMaxPathUnits, L'\0');
    const DWORD length = GetModuleFileNameW(nullptr, module.data(), static_cast<DWORD>(module.size()));
    if (length == 0 || length >= module.size())
    {
        const DWORD code = length == 0 ? GetLastError() : static_cast<DWORD>(ERROR_INSUFFICIENT_BUFFER);
        throw Error{"GetModuleFileNameW", code, "reading the executable's path"};
    }
    module.resize(length);
    sources.executable_folder = std::filesystem::path{module}.parent_path();
    return sources;
}

AppFolders resolve_app_folders(std::string_view app_name, const AppFolderSources& sources)
{
    check_app_name(app_name);
    AppFolders folders;
    const auto marker = sources.executable_folder / kPortableMarker;
    std::error_code error;
    const auto marker_status = std::filesystem::status(marker, error);
    if (error && marker_status.type() != std::filesystem::file_type::not_found)
    {
        throw Error{"std::filesystem::status", static_cast<std::uint32_t>(error.value()),
                    "checking the portable marker " + detail::utf16_to_utf8(marker.native())};
    }
    folders.portable = std::filesystem::is_regular_file(marker_status);
    if (folders.portable)
    {
        folders.root = sources.executable_folder;
    }
    else
    {
        folders.root = sources.local_app_data / kPublisherFolder / detail::utf8_to_utf16(std::string{app_name});
    }
    folders.logs = folders.root / kLogsFolder;
    folders.settings = folders.root / kSettingsFolder;
    folders.recovery = folders.root / kRecoveryFolder;
    for (const auto* folder : {&folders.root, &folders.logs, &folders.settings, &folders.recovery})
    {
        create_folder(*folder);
    }
    return folders;
}

} // namespace isotone::core
