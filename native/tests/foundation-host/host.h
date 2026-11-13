// Copyright (C) 2025-2026 Rizonetech (Pty) Ltd. All rights reserved.
// Licensed under the GNU General Public License v3.0 (GPL-3.0-or-later).

// The foundation test host: the one window every native foundation proves itself in (D01 T15 §1). main.cpp is its
// entry point; everything it does is here so the tests can reach it. README.md describes the switches, the report,
// and how a foundation adds a scenario.

#pragma once

#include <cstdint>
#include <filesystem>
#include <nlohmann/json.hpp>
#include <optional>
#include <span>
#include <string>
#include <string_view>
#include <vector>

namespace isotone::foundation_host
{

// The host's exit codes. NoDisplay is the code CTest reads as "skipped" (SKIP_RETURN_CODE).
inline constexpr int kExitPass = 0;
inline constexpr int kExitFail = 1;
inline constexpr int kExitUsage = 2;
inline constexpr int kExitNoDisplay = 77;

// Whether this process has a display to put a window on: the window station it runs in is the visible one.
enum class DisplaySession : std::uint8_t
{
    Visible,
    Absent,
};

// Reads the process's window station (GetProcessWindowStation, UOI_FLAGS). A station that cannot be read counts as
// Visible, so a failure there is never mistaken for a missing display.
[[nodiscard]] DisplaySession display_session() noexcept;

// The exit code for a window that could not be created or driven: a skip only when the display session is
// positively absent, a failure on a working display.
[[nodiscard]] constexpr int exit_code_without_window(DisplaySession session) noexcept
{
    return session == DisplaySession::Absent ? kExitNoDisplay : kExitFail;
}

// What the command line asked for.
struct Arguments
{
    // Empty: the interactive host, a visible window until the user closes it.
    std::string scenario;
    std::filesystem::path report;
    // Where the host keeps its log and settings. Required: a run never writes the user's real app-data folder.
    std::filesystem::path data_root;
    // Test switch: the window's creation fails as if CreateWindowExW had refused.
    bool fail_window = false;
};

// Parses the switches (--scenario <name>, --report <path>, --data-root <folder>, --fail-window). The arguments
// exclude the program's own name. Returns the sentence to print when they cannot be used.
[[nodiscard]] std::optional<std::string> parse_arguments(std::span<const std::wstring> arguments, Arguments& parsed);

// One run's report: README.md, "The report".
struct Report
{
    std::string scenario;
    // "pass", "fail", or "no-display".
    std::string result = "pass";
    // One sentence for each thing that was wrong; empty exactly when the result is "pass".
    std::vector<std::string> failures;
    nlohmann::ordered_json measurements = nlohmann::ordered_json::object();

    // Records one measurement under its key.
    void measure(const std::string& key, nlohmann::ordered_json value);
    // Records a failure and makes the result "fail".
    void fail(std::string sentence);
};

// The names of the scenarios the host knows, in alphabetical order.
[[nodiscard]] std::vector<std::string_view> scenario_names();

// Runs the host: parses the arguments, runs the scenario (or the interactive window), writes the report, and
// returns the exit code. Diagnostics go to standard error. Never throws.
[[nodiscard]] int run_host(std::span<const std::wstring> arguments) noexcept;

} // namespace isotone::foundation_host
