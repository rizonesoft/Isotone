// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#pragma once

#include <filesystem>
#include <string_view>

namespace isotone::core
{

// The file whose presence beside the executable puts an app in portable mode (D01 T27 §1, a recorded default).
inline constexpr std::wstring_view kPortableMarker{L"portable"};

// Where an app's folders are resolved from. A test builds its own, so no test touches the user's real folders.
struct AppFolderSources
{
    // The user's local application data folder (FOLDERID_LocalAppData).
    std::filesystem::path local_app_data;
    // The folder holding the running executable.
    std::filesystem::path executable_folder;

    // Reads FOLDERID_LocalAppData with SHGetKnownFolderPath and this process's executable with GetModuleFileNameW.
    // Throws Error naming the failing call. Any thread.
    [[nodiscard]] static AppFolderSources from_windows();
};

// An app's folders: the data root and the logs, settings, and recovery folders inside it (standards/shared.md).
struct AppFolders
{
    std::filesystem::path root;
    std::filesystem::path logs;
    std::filesystem::path settings;
    std::filesystem::path recovery;
    // True when the root is the executable's folder because the portable marker sits there.
    bool portable = false;
};

// Resolves the folders for app_name (UTF-8, such as "Stilus": not empty, not "." or "..", no path separator,
// reserved character, or control character): <local app data>\Rizonesoft\<app>\, or the executable's folder when
// kPortableMarker is a file there. Creates every folder that does not exist. Throws Error naming the failing call
// for an invalid name, a portable marker that cannot be inspected (only an absent marker means per-user), or a folder
// that cannot be created. Any thread.
[[nodiscard]] AppFolders resolve_app_folders(std::string_view app_name, const AppFolderSources& sources);

} // namespace isotone::core
