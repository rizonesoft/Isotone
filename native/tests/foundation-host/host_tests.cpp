// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

#include "host.h"

#include <filesystem>
#include <gtest/gtest.h>
#include <optional>
#include <string>
#include <vector>

namespace
{

using isotone::foundation_host::Arguments;
using isotone::foundation_host::DisplaySession;
using isotone::foundation_host::exit_code_without_window;
using isotone::foundation_host::parse_arguments;

// A window that cannot be created is a skip only when the display session is positively absent: on a working
// display it is a failure, never a quiet skip.
TEST(HostDisplay, OnlyAnAbsentSessionIsASkip)
{
    EXPECT_EQ(exit_code_without_window(DisplaySession::Absent), isotone::foundation_host::kExitNoDisplay);
    EXPECT_EQ(exit_code_without_window(DisplaySession::Visible), isotone::foundation_host::kExitFail);
    EXPECT_NE(isotone::foundation_host::kExitNoDisplay, isotone::foundation_host::kExitFail);
    // Reading the window station never throws, and gives one of the two answers.
    const DisplaySession here = isotone::foundation_host::display_session();
    EXPECT_TRUE(here == DisplaySession::Visible || here == DisplaySession::Absent);
}

TEST(HostArguments, EverySwitchIsRead)
{
    Arguments parsed;
    const std::vector<std::wstring> arguments{L"--scenario",  L"smoke",     L"--report",     L"out\\report.json",
                                              L"--data-root", L"out\\data", L"--fail-window"};
    EXPECT_FALSE(parse_arguments(arguments, parsed).has_value());
    EXPECT_EQ(parsed.scenario, "smoke");
    EXPECT_EQ(parsed.report, std::filesystem::path{L"out\\report.json"});
    EXPECT_EQ(parsed.data_root, std::filesystem::path{L"out\\data"});
    EXPECT_TRUE(parsed.fail_window);
}

TEST(HostArguments, UnusableArgumentsAreNamed)
{
    Arguments parsed;
    const auto missing_root = parse_arguments(std::vector<std::wstring>{L"--scenario", L"smoke"}, parsed);
    EXPECT_TRUE(missing_root.value_or("").contains("--data-root"));
    const auto unknown = parse_arguments(std::vector<std::wstring>{L"--data-root", L"d", L"--verbose"}, parsed);
    EXPECT_TRUE(unknown.value_or("").contains("--verbose"));
    const auto no_value = parse_arguments(std::vector<std::wstring>{L"--data-root"}, parsed);
    EXPECT_TRUE(no_value.value_or("").contains("needs a value"));
}

TEST(HostScenarios, AreListedInOrder)
{
    const auto names = isotone::foundation_host::scenario_names();
    ASSERT_EQ(names.size(), 2U);
    EXPECT_EQ(names.front(), "lifecycle");
    EXPECT_EQ(names.back(), "smoke");
}

} // namespace
