// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "isotone/core/app_paths.h"
#include "isotone/core/error.h"
#include "temp_folder.h"

#include <filesystem>
#include <fstream>
#include <gtest/gtest.h>
#include <optional>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace
{

using isotone::core::AppFolderSources;
using isotone::core::Error;
using isotone::core::resolve_app_folders;
using isotone::tests::TempFolder;

void touch(const std::filesystem::path& file)
{
    std::ofstream{file} << "x";
}

TEST(AppPaths, ResolvesPerUserAndPortable)
{
    const TempFolder temp;
    const AppFolderSources sources{.local_app_data = temp.path() / "local", .executable_folder = temp.path() / "app"};
    std::filesystem::create_directories(sources.executable_folder);

    const auto per_user = resolve_app_folders("TestApp", sources);
    EXPECT_FALSE(per_user.portable);
    EXPECT_EQ(per_user.root, temp.path() / "local" / "Rizonesoft" / "TestApp");
    EXPECT_EQ(per_user.logs, per_user.root / "logs");
    EXPECT_EQ(per_user.settings, per_user.root / "settings");
    EXPECT_EQ(per_user.recovery, per_user.root / "recovery");
    for (const auto& folder : {per_user.root, per_user.logs, per_user.settings, per_user.recovery})
    {
        EXPECT_TRUE(std::filesystem::is_directory(folder)) << folder;
    }

    touch(sources.executable_folder / isotone::core::kPortableMarker);
    const auto portable = resolve_app_folders("TestApp", sources);
    EXPECT_TRUE(portable.portable);
    EXPECT_EQ(portable.root, sources.executable_folder);
    EXPECT_EQ(portable.logs, sources.executable_folder / "logs");
    EXPECT_TRUE(std::filesystem::is_directory(portable.recovery));

    // The real sources only read Windows: an absolute local app data folder and this test's own folder.
    const auto real = AppFolderSources::from_windows();
    EXPECT_TRUE(real.local_app_data.is_absolute());
    EXPECT_TRUE(std::filesystem::is_directory(real.local_app_data));
    EXPECT_TRUE(std::filesystem::is_directory(real.executable_folder));
}

TEST(AppPaths, TestRootIsolates)
{
    const TempFolder temp;
    const std::string app = "IsotoneTestIsolation";
    const auto real = AppFolderSources::from_windows();
    const auto real_root = real.local_app_data / "Rizonesoft" / app;
    ASSERT_FALSE(std::filesystem::exists(real_root));

    const auto folders = resolve_app_folders(
        app, AppFolderSources{.local_app_data = temp.path(), .executable_folder = temp.path() / "exe"});
    EXPECT_TRUE(std::filesystem::is_directory(folders.settings));
    EXPECT_FALSE(std::filesystem::exists(real_root));
}

// The Error an action throws, or nothing when it throws none.
template <typename Action> std::optional<Error> error_from(Action&& action)
{
    try
    {
        std::forward<Action>(action)();
    }
    catch (const Error& error)
    {
        return error;
    }
    return std::nullopt;
}

TEST(AppPaths, FailureNamesTheCall)
{
    const TempFolder temp;
    const auto blocker = temp.path() / "not-a-folder";
    touch(blocker);
    const AppFolderSources under_a_file{.local_app_data = blocker, .executable_folder = temp.path()};
    const auto error = error_from([&] { (void)resolve_app_folders("TestApp", under_a_file); });
    if (!error.has_value())
    {
        ADD_FAILURE() << "a folder under a file was created";
        return;
    }
    EXPECT_EQ(error->call(), "std::filesystem::create_directories");
    EXPECT_NE(error->code(), 0U);
    EXPECT_TRUE(std::string_view{error->what()}.contains("not-a-folder")) << error->what();

    const AppFolderSources sources{.local_app_data = temp.path(), .executable_folder = temp.path()};
    std::vector<std::string> accepted;
    for (const char* name : {"", ".", "..", "a/b", "a\\b", "a:b", "tab\there"})
    {
        if (!error_from([&] { (void)resolve_app_folders(name, sources); }).has_value())
        {
            accepted.emplace_back(name);
        }
    }
    EXPECT_TRUE(accepted.empty()) << "accepted " << accepted.size()
                                  << " invalid name(s), the first: " << accepted.front();
}

} // namespace
